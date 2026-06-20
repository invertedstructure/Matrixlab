#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

PROBE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_probe_receipts"
DIAG_DIR = ROOT / "data" / "stable_delta_signature_diagnostics"
DIAG_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_diagnostic_receipts"

EXPECTED_PROBE_ID = "a729e00e"
EXPECTED_RECEIPT_ID = "0ce90f3f"
EXPECTED_COMPRESSION_VERSION = "stable_delta_signature_v0.2"
EXPECTED_MODE = "OUTER_OBSERVER_ONLY"

DIAGNOSTIC_NAME = "diagnose_stable_delta_signature_failure_v0"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_bytes(obj: Any) -> int:
    return len(json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8"))


def sha8(obj: Any) -> str:
    blob = json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(blob).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    rows = []
    for line in path.read_text().splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows


def flatten(obj: Any, prefix: str = "", out: dict[str, Any] | None = None) -> dict[str, Any]:
    if out is None:
        out = {}
    if isinstance(obj, dict):
        for key, value in obj.items():
            name = f"{prefix}.{key}" if prefix else str(key)
            out[name] = value
            if isinstance(value, (dict, list)):
                flatten(value, name, out)
    elif isinstance(obj, list):
        for i, value in enumerate(obj):
            name = f"{prefix}.{i}" if prefix else str(i)
            out[name] = value
            if isinstance(value, (dict, list)):
                flatten(value, name, out)
    return out


def normalize_value(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, default=str, separators=(",", ":"))
    return repr(value)


def minimal_required_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "signature_id": row.get("signature_id"),
        "source_run_id": row.get("source_run_id"),
        "case_id": row.get("case_id"),
        "occurrence_id": row.get("occurrence_id"),
        "full_occurrence_key": row.get("full_occurrence_key"),
        "state_hash_before": row.get("state_hash_before"),
        "state_hash_after": row.get("state_hash_after"),
        "move_id": row.get("move_id"),
        "delta_signature": row.get("delta_signature"),
        "compression_version": row.get("compression_version"),
        "audit_pointer_or_full_receipt_ref": row.get("audit_pointer_or_full_receipt_ref"),
    }


def projected_scale_row(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "signature_id": row.get("signature_id"),
        "source_run_id": row.get("source_run_id"),
        "case_id": row.get("case_id"),
        "occurrence_id": row.get("occurrence_id"),
        "delta_signature": row.get("delta_signature"),
        "compression_version": row.get("compression_version"),
        "audit_pointer_or_full_receipt_ref": row.get("audit_pointer_or_full_receipt_ref"),
    }


def summarize_missing(rows: list[dict[str, Any]], field_path: str) -> dict[str, Any]:
    missing = 0
    values = []
    for row in rows:
        flat = flatten(row)
        value = flat.get(field_path)
        if value in (None, ""):
            missing += 1
        else:
            values.append(value)
    return {
        "field": field_path,
        "missing": missing,
        "present": len(rows) - missing,
        "missing_rate": round(missing / len(rows), 6) if rows else 0.0,
        "distinct_present_values": len({normalize_value(v) for v in values}),
    }


def collision_diagnostics(rows: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row.get("delta_signature"))].append(row)

    collision_groups = [group for group in groups.values() if len({r.get("full_occurrence_key") for r in group}) > 1]

    gallery: list[dict[str, Any]] = []
    for group in sorted(collision_groups, key=lambda g: (-len(g), str(g[0].get("delta_signature"))))[:25]:
        sig = group[0].get("delta_signature")
        keys = sorted({r.get("full_occurrence_key") for r in group})
        case_ids = sorted({str(r.get("case_id")) for r in group})
        occurrence_ids = sorted({str(r.get("occurrence_id")) for r in group})
        source_runs = sorted({str(r.get("source_run_id")) for r in group})
        moves = sorted({str(r.get("move_id")) for r in group})
        states_before = sorted({str(r.get("state_hash_before")) for r in group})
        states_after = sorted({str(r.get("state_hash_after")) for r in group})

        flat_payloads = [flatten(r.get("delta_payload") or {}) for r in group]
        varied_delta_fields = []
        for field in sorted({k for flat in flat_payloads for k in flat.keys()}):
            vals = {normalize_value(flat.get(field)) for flat in flat_payloads}
            if len(vals) > 1:
                varied_delta_fields.append({"field": field, "distinct": len(vals), "examples": sorted(vals)[:5]})

        gallery.append({
            "delta_signature": sig,
            "group_size": len(group),
            "distinct_full_occurrence_keys": len(keys),
            "full_occurrence_keys_sample": keys[:10],
            "source_runs": source_runs[:10],
            "case_ids_sample": case_ids[:10],
            "occurrence_ids_sample": occurrence_ids[:10],
            "move_ids": moves[:10],
            "state_hash_before_values": states_before[:10],
            "state_hash_after_values": states_after[:10],
            "varied_delta_fields_inside_collision": varied_delta_fields[:20],
            "diagnosis_hint": (
                "collision survives because compressed delta payload does not include fields that separate these full occurrence keys"
                if not varied_delta_fields
                else "collision group contains external occurrence variation not represented in delta signature identity"
            ),
        })

    summary = {
        "total_delta_signature_groups": len(groups),
        "collision_group_count": len(collision_groups),
        "largest_collision_group_size": max((len(g) for g in collision_groups), default=0),
        "collision_group_sizes_top10": sorted([len(g) for g in collision_groups], reverse=True)[:10],
    }
    return gallery, summary


def entropy_diagnostics(rows: list[dict[str, Any]]) -> dict[str, Any]:
    flats = [flatten(r.get("delta_payload") or {}) for r in rows]
    fields = sorted({k for flat in flats for k in flat.keys()})

    field_rows = []
    for field in fields:
        values = [flat.get(field) for flat in flats]
        normalized = [normalize_value(v) for v in values]
        distinct = len(set(normalized))
        missing = sum(1 for v in values if v in (None, ""))
        field_rows.append({
            "field": field,
            "distinct": distinct,
            "missing": missing,
            "missing_rate": round(missing / len(rows), 6) if rows else 0.0,
            "examples": sorted(set(normalized))[:8],
        })

    low_entropy = [r for r in field_rows if r["distinct"] <= 1]
    high_entropy = sorted(field_rows, key=lambda r: (-r["distinct"], r["missing_rate"], r["field"]))[:25]
    high_missing = sorted(field_rows, key=lambda r: (-r["missing_rate"], -r["distinct"], r["field"]))[:25]

    return {
        "delta_payload_field_count": len(fields),
        "low_entropy_field_count": len(low_entropy),
        "low_entropy_fields_sample": low_entropy[:40],
        "high_entropy_fields_top25": high_entropy,
        "high_missing_fields_top25": high_missing,
    }


def byte_bloat_diagnostics(rows: list[dict[str, Any]], full_receipt_bytes: int) -> dict[str, Any]:
    total_row_bytes = sum(canonical_bytes(r) for r in rows)
    total_delta_payload_bytes = sum(canonical_bytes(r.get("delta_payload") or {}) for r in rows)
    total_audit_pointer_bytes = sum(canonical_bytes(r.get("audit_pointer_or_full_receipt_ref") or {}) for r in rows)
    total_observer_notes_bytes = sum(canonical_bytes(r.get("observer_notes") or {}) for r in rows)
    total_minimal_required_bytes = sum(canonical_bytes(minimal_required_row(r)) for r in rows)
    total_projected_scale_bytes = sum(canonical_bytes(projected_scale_row(r)) for r in rows)

    return {
        "full_receipt_bytes": full_receipt_bytes,
        "current_compressed_row_bytes_recomputed": total_row_bytes,
        "current_vs_full_ratio": total_row_bytes / full_receipt_bytes if full_receipt_bytes else None,
        "delta_payload_bytes": total_delta_payload_bytes,
        "audit_pointer_bytes": total_audit_pointer_bytes,
        "observer_notes_bytes": total_observer_notes_bytes,
        "minimal_required_row_bytes": total_minimal_required_bytes,
        "minimal_required_vs_full_ratio": total_minimal_required_bytes / full_receipt_bytes if full_receipt_bytes else None,
        "projected_scale_row_bytes": total_projected_scale_bytes,
        "projected_scale_vs_full_ratio": total_projected_scale_bytes / full_receipt_bytes if full_receipt_bytes else None,
        "estimated_debug_sidecar_bytes": max(0, total_row_bytes - total_projected_scale_bytes),
        "bloat_sources_ranked": sorted(
            [
                {"source": "delta_payload", "bytes": total_delta_payload_bytes},
                {"source": "audit_pointer", "bytes": total_audit_pointer_bytes},
                {"source": "observer_notes", "bytes": total_observer_notes_bytes},
                {"source": "minimal_required_projection", "bytes": total_minimal_required_bytes},
                {"source": "projected_scale_projection", "bytes": total_projected_scale_bytes},
            ],
            key=lambda x: -x["bytes"],
        ),
    }


def build_candidate_v01_design(diag: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_design_id": "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1",
        "design_status": "PROPOSED_BY_FAILURE_DIAGNOSTIC_NOT_IMPLEMENTED",
        "core_correction": "Separate tiny signature payload from observer/debug/audit sidecar.",
        "do_not_repeat": [
            "Do not include full delta_payload JSON in every compressed row as scale payload.",
            "Do not count observer debug fields as compressed burden.",
            "Do not run scale bands on a signature with false merges.",
            "Do not compare against raw receipt hashes.",
            "Do not authorize receipt replacement or scale mode.",
        ],
        "proposed_signature_payload": {
            "compression_version": "stable_delta_signature_v0.1_candidate",
            "signature_basis": [
                "canonical transition tuple if present: state_hash_before, move_id, state_hash_after, halt_reason/status",
                "case-local occurrence discriminator only if it is canonical and audit-derived, not rowid packaging noise",
                "compact shape/event buckets only if they increase separability without increasing projected burden above full burden",
            ],
            "forbidden_in_signature_payload": [
                "full_occurrence_key",
                "audit_pointer",
                "observer_notes",
                "full debug delta_payload",
                "raw receipt hash",
                "receipt rowid as primary identity",
                "timestamps",
                "paths",
                "run packaging fields",
            ],
        },
        "required_next_probe_behavior": [
            "Measure signature payload bytes separately from audit/debug sidecar bytes.",
            "Report current_compressed_row_bytes, minimal_required_row_bytes, and projected_scale_row_bytes separately.",
            "Use collision diagnosis before any scale-band run.",
            "Only advance to scale bands after no_silent_collapse is true on the local probe.",
        ],
        "next_command_goal": "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1_POLICY",
    }


def verify_probe_receipt(receipt: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if receipt.get("probe_id") != EXPECTED_PROBE_ID:
        failures.append(f"probe_id_mismatch:{receipt.get('probe_id')}")
    if receipt.get("receipt_id") != EXPECTED_RECEIPT_ID:
        failures.append(f"receipt_id_mismatch:{receipt.get('receipt_id')}")
    if receipt.get("gate") != "STABLE_DELTA_SIGNATURE_PROBE_EXECUTION_PASS":
        failures.append(f"probe_execution_gate_not_pass:{receipt.get('gate')}")
    if receipt.get("compression_version") != EXPECTED_COMPRESSION_VERSION:
        failures.append(f"compression_version_mismatch:{receipt.get('compression_version')}")
    if receipt.get("mode") != EXPECTED_MODE:
        failures.append(f"mode_mismatch:{receipt.get('mode')}")
    if receipt.get("terminal_decision") != "FAIL":
        failures.append(f"terminal_decision_expected_FAIL:{receipt.get('terminal_decision')}")
    if receipt.get("full_receipt_count") != 176:
        failures.append(f"full_receipt_count_unexpected:{receipt.get('full_receipt_count')}")
    if receipt.get("compressed_signature_count") != 176:
        failures.append(f"compressed_signature_count_unexpected:{receipt.get('compressed_signature_count')}")
    if receipt.get("distinct_full_occurrence_keys") != 176:
        failures.append(f"distinct_full_keys_unexpected:{receipt.get('distinct_full_occurrence_keys')}")
    if receipt.get("distinct_compressed_signatures") != 21:
        failures.append(f"distinct_compressed_unexpected:{receipt.get('distinct_compressed_signatures')}")
    if receipt.get("collision_count") != 19:
        failures.append(f"collision_count_unexpected:{receipt.get('collision_count')}")
    if receipt.get("false_merge_count") != 19:
        failures.append(f"false_merge_count_unexpected:{receipt.get('false_merge_count')}")
    if receipt.get("burden_ratio_bytes", 0) <= 1.0:
        failures.append(f"burden_ratio_expected_over_1:{receipt.get('burden_ratio_bytes')}")
    if receipt.get("distinguishability_retention_ratio", 1) >= 0.5:
        failures.append(f"retention_expected_low:{receipt.get('distinguishability_retention_ratio')}")

    gates = receipt.get("pass_gates") or {}
    if gates.get("audit_recoverability") is not True:
        failures.append("audit_recoverability_not_true")
    if gates.get("observer_only_containment") is not True:
        failures.append("observer_only_containment_not_true")
    if gates.get("raw_receipt_hash_not_used_as_truth_surface") is not True:
        failures.append("raw_hash_guard_not_true")
    if gates.get("no_silent_collapse") is not False:
        failures.append("no_silent_collapse_expected_false")
    if gates.get("burden_reduction_real") is not False:
        failures.append("burden_reduction_expected_false")
    if gates.get("stability_across_scale") is not False:
        failures.append("stability_across_scale_expected_false")

    truth = receipt.get("truth_surface") or {}
    if truth.get("primary_comparison") != "full_occurrence_key_to_compressed_delta_signature":
        failures.append(f"truth_surface_wrong:{truth.get('primary_comparison')}")
    if truth.get("raw_full_receipt_hash_used_as_truth_surface") is not False:
        failures.append("raw_hash_truth_surface_used")
    if truth.get("full_receipt_hash_compared_to_delta_signature") is not False:
        failures.append("full_receipt_hash_compared_to_delta_signature")

    auth = receipt.get("authority_guards") or {}
    if auth.get("observer_only") is not True:
        failures.append("observer_only_guard_missing")
    for key in [
        "runtime_receipt_emission_changed",
        "full_receipts_suppressed",
        "scale_mode_authorized",
        "compressed_signature_promoted_to_theorem_content",
        "receipt_replacement_authorized",
        "receipt_deletion_authorized",
        "receipt_compression_authorized",
    ]:
        if auth.get(key) is not False:
            failures.append(f"authority_guard_failed:{key}:{auth.get(key)}")

    return failures


def build_diagnostic(probe_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    DIAG_DIR.mkdir(parents=True, exist_ok=True)
    DIAG_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    receipt = load_json(PROBE_RECEIPT_DIR / f"{probe_id}.json")
    rows = load_jsonl(ROOT / receipt["rows_path"])

    failures = verify_probe_receipt(receipt)

    if len(rows) != receipt.get("compressed_signature_count"):
        failures.append(f"row_count_mismatch:{len(rows)}!={receipt.get('compressed_signature_count')}")

    collision_gallery, collision_summary = collision_diagnostics(rows)
    entropy = entropy_diagnostics(rows)
    byte_bloat = byte_bloat_diagnostics(rows, int(receipt.get("full_receipt_bytes") or 0))

    missing_core_fields = [
        summarize_missing(rows, "state_hash_before"),
        summarize_missing(rows, "state_hash_after"),
        summarize_missing(rows, "move_id"),
        summarize_missing(rows, "delta_payload.transition.state_hash_before"),
        summarize_missing(rows, "delta_payload.transition.state_hash_after"),
        summarize_missing(rows, "delta_payload.transition.move_id"),
        summarize_missing(rows, "delta_payload.transition.halt_reason"),
        summarize_missing(rows, "delta_payload.transition.status"),
        summarize_missing(rows, "delta_payload.case_surface.family"),
        summarize_missing(rows, "delta_payload.case_surface.probe_id"),
        summarize_missing(rows, "delta_payload.case_surface.slot_id"),
        summarize_missing(rows, "delta_payload.case_surface.burden_class"),
    ]

    root_cause = {
        "primary_failure": "FALSE_MERGES_AND_NO_BURDEN_REDUCTION",
        "false_merge_diagnosis": {
            "distinct_full_occurrence_keys": receipt.get("distinct_full_occurrence_keys"),
            "distinct_compressed_signatures": receipt.get("distinct_compressed_signatures"),
            "distinguishability_retention_ratio": receipt.get("distinguishability_retention_ratio"),
            "collision_count": receipt.get("collision_count"),
            "false_merge_count": receipt.get("false_merge_count"),
            "diagnosis": "The candidate signature is too coarse for local occurrence separability.",
        },
        "burden_diagnosis": {
            "full_receipt_bytes": receipt.get("full_receipt_bytes"),
            "compressed_signature_bytes": receipt.get("compressed_signature_bytes"),
            "burden_ratio_bytes": receipt.get("burden_ratio_bytes"),
            "diagnosis": "The observer row stores too much debug/signature payload, making compressed rows larger than full receipt baseline.",
        },
        "containment_diagnosis": {
            "observer_only_valid": True,
            "audit_recoverability_valid": True,
            "truth_surface_valid": True,
            "diagnosis": "The observer harness is lawful; the signature candidate failed.",
        },
    }

    candidate_v01 = build_candidate_v01_design({})

    diagnostic = {
        "schema_version": "stable_delta_signature_failure_diagnostic_v0",
        "diagnostic_name": DIAGNOSTIC_NAME,
        "source_probe_id": probe_id,
        "source_receipt_id": receipt.get("receipt_id"),
        "source_probe_terminal_decision": receipt.get("terminal_decision"),
        "source_probe_gate": receipt.get("gate"),
        "mode": "OUTER_OBSERVER_ONLY_DIAGNOSTIC",
        "diagnostic_scope": {
            "read_only": True,
            "runtime_receipt_system_changed": False,
            "probe_script_changed": False,
            "scale_mode_authorized": False,
            "receipt_replacement_authorized": False,
            "receipt_deletion_authorized": False,
            "receipt_compression_authorized": False,
            "theorem_content_authorized": False,
        },
        "source_probe_summary": {
            "full_receipt_count": receipt.get("full_receipt_count"),
            "compressed_signature_count": receipt.get("compressed_signature_count"),
            "full_receipt_bytes": receipt.get("full_receipt_bytes"),
            "compressed_signature_bytes": receipt.get("compressed_signature_bytes"),
            "burden_ratio_bytes": receipt.get("burden_ratio_bytes"),
            "distinct_full_occurrence_keys": receipt.get("distinct_full_occurrence_keys"),
            "distinct_compressed_signatures": receipt.get("distinct_compressed_signatures"),
            "distinguishability_retention_ratio": receipt.get("distinguishability_retention_ratio"),
            "collision_count": receipt.get("collision_count"),
            "collision_rate": receipt.get("collision_rate"),
            "false_merge_count": receipt.get("false_merge_count"),
            "scale_value": receipt.get("scale_value"),
            "pass_gates": receipt.get("pass_gates"),
        },
        "root_cause": root_cause,
        "missing_core_fields": missing_core_fields,
        "collision_summary": collision_summary,
        "collision_gallery": collision_gallery,
        "entropy_diagnostics": entropy,
        "byte_bloat_diagnostics": byte_bloat,
        "candidate_v0_1_design_target": candidate_v01,
        "decision": {
            "do_not_scale_current_signature": True,
            "do_not_accept_probe_candidate": True,
            "do_not_authorize_scale_mode": True,
            "do_not_authorize_receipt_replacement": True,
            "diagnose_before_new_probe": True,
            "recommended_next_command_goal": "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1_POLICY",
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1_POLICY" if not failures else None,
            "stop_code": None if not failures else "STOP_STABLE_DELTA_SIGNATURE_FAILURE_DIAGNOSTIC_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    diagnostic_id = sha8({
        "diagnostic_name": diagnostic["diagnostic_name"],
        "source_probe_id": probe_id,
        "root_cause": root_cause,
        "collision_summary": collision_summary,
        "byte_bloat": byte_bloat,
        "candidate_v0_1_design_target": candidate_v01,
    })
    diagnostic["diagnostic_id"] = diagnostic_id
    diagnostic["diagnostic_sig8"] = diagnostic_id

    receipt_out = {
        "schema_version": "stable_delta_signature_failure_diagnostic_receipt_v0",
        "diagnostic_id": diagnostic_id,
        "diagnostic_sig8": diagnostic_id,
        "diagnostic_path": f"data/stable_delta_signature_diagnostics/{diagnostic_id}.json",
        "source_probe_id": probe_id,
        "source_receipt_id": receipt.get("receipt_id"),
        "source_probe_terminal_decision": receipt.get("terminal_decision"),
        "root_cause": root_cause,
        "collision_summary": collision_summary,
        "byte_bloat_summary": {
            "full_receipt_bytes": byte_bloat["full_receipt_bytes"],
            "current_compressed_row_bytes_recomputed": byte_bloat["current_compressed_row_bytes_recomputed"],
            "current_vs_full_ratio": byte_bloat["current_vs_full_ratio"],
            "minimal_required_row_bytes": byte_bloat["minimal_required_row_bytes"],
            "minimal_required_vs_full_ratio": byte_bloat["minimal_required_vs_full_ratio"],
            "projected_scale_row_bytes": byte_bloat["projected_scale_row_bytes"],
            "projected_scale_vs_full_ratio": byte_bloat["projected_scale_vs_full_ratio"],
            "estimated_debug_sidecar_bytes": byte_bloat["estimated_debug_sidecar_bytes"],
        },
        "decision": diagnostic["decision"],
        "terminal": diagnostic["terminal"],
        "gate": diagnostic["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt_out)
    receipt_out["receipt_id"] = receipt_id
    receipt_out["receipt_sig8"] = receipt_id

    (DIAG_DIR / f"{diagnostic_id}.json").write_text(json.dumps(diagnostic, indent=2, sort_keys=True))
    (DIAG_RECEIPT_DIR / f"{diagnostic_id}.json").write_text(json.dumps(receipt_out, indent=2, sort_keys=True))

    return diagnostic, receipt_out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--probe-id", default=EXPECTED_PROBE_ID)
    args = parser.parse_args()

    diagnostic, receipt = build_diagnostic(args.probe_id)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"diagnostic_id={diagnostic['diagnostic_id']}")
    print(f"diagnostic_json_path=data/stable_delta_signature_diagnostics/{diagnostic['diagnostic_id']}.json")
    print(f"diagnostic_receipt_path=data/stable_delta_signature_diagnostic_receipts/{diagnostic['diagnostic_id']}.json")

    return 0 if diagnostic["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
