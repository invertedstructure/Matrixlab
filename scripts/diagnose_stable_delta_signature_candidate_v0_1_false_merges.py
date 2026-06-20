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

CANDIDATE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_1_receipts"
POLICY_DIR = ROOT / "data" / "stable_delta_signature_candidate_policies"
DIAGNOSTIC_DIR = ROOT / "data" / "stable_delta_signature_diagnostics"

OUT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_1_false_merge_diagnostics"
OUT_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_1_false_merge_diagnostic_receipts"

EXPECTED_CANDIDATE_PROBE_ID = "a097b68f"
EXPECTED_CANDIDATE_RECEIPT_ID = "08b4ac55"
EXPECTED_POLICY_ID = "c3dcd5d1"
EXPECTED_SOURCE_DIAGNOSTIC_ID = "21878f3c"
EXPECTED_TERMINAL_DECISION = "FAIL_FALSE_MERGE"

DIAGNOSTIC_NAME = "diagnose_stable_delta_signature_candidate_v0_1_false_merges"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def sha8(obj: Any) -> str:
    return hashlib.sha256(blob(obj)).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def norm(value: Any) -> str:
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True, default=str, separators=(",", ":"))
    return repr(value)


def safe_int(value: Any) -> int | None:
    try:
        return int(value)
    except Exception:
        return None


def verify_source(candidate: dict[str, Any], policy: dict[str, Any], source_diag: dict[str, Any], rows: list[dict[str, Any]]) -> list[str]:
    failures: list[str] = []

    if candidate.get("candidate_probe_id") != EXPECTED_CANDIDATE_PROBE_ID:
        failures.append(f"candidate_probe_id_mismatch:{candidate.get('candidate_probe_id')}")
    if candidate.get("receipt_id") != EXPECTED_CANDIDATE_RECEIPT_ID:
        failures.append(f"candidate_receipt_id_mismatch:{candidate.get('receipt_id')}")
    if candidate.get("gate") != "PASS":
        failures.append(f"candidate_gate_not_PASS:{candidate.get('gate')}")
    if candidate.get("mode") != "OUTER_OBSERVER_ONLY":
        failures.append(f"candidate_mode_wrong:{candidate.get('mode')}")
    if candidate.get("terminal_decision") != EXPECTED_TERMINAL_DECISION:
        failures.append(f"candidate_terminal_not_FAIL_FALSE_MERGE:{candidate.get('terminal_decision')}")
    if candidate.get("source_policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"source_policy_id_wrong:{candidate.get('source_policy_id')}")
    if candidate.get("source_diagnostic_id") != EXPECTED_SOURCE_DIAGNOSTIC_ID:
        failures.append(f"source_diagnostic_id_wrong:{candidate.get('source_diagnostic_id')}")
    if candidate.get("failures") != []:
        failures.append(f"candidate_harness_failures_not_empty:{candidate.get('failures')}")
    if len(rows) != candidate.get("burden_measurements", {}).get("candidate_signature_count"):
        failures.append(f"rows_count_mismatch:{len(rows)}!={candidate.get('burden_measurements', {}).get('candidate_signature_count')}")

    auth = candidate.get("authority_guards") or {}
    if auth.get("observer_only") is not True:
        failures.append("observer_only_guard_missing")
    for key in [
        "runtime_receipt_emission_changed",
        "full_receipts_suppressed",
        "scale_mode_authorized",
        "receipt_replacement_authorized",
        "receipt_deletion_authorized",
        "receipt_compression_authorized",
        "raw_receipt_hash_truth_surface_authorized",
        "theorem_content_authorized",
        "scale_band_run_authorized",
    ]:
        if auth.get(key) is not False:
            failures.append(f"authority_guard_failed:{key}:{auth.get(key)}")

    truth = candidate.get("truth_surface") or {}
    if truth.get("primary_comparison") != "full_occurrence_key_to_candidate_delta_signature":
        failures.append(f"truth_surface_wrong:{truth.get('primary_comparison')}")
    if truth.get("raw_full_receipt_hash_used_as_truth_surface") is not False:
        failures.append("raw_hash_truth_surface_used")
    if truth.get("full_receipt_hash_compared_to_delta_signature") is not False:
        failures.append("full_receipt_hash_compared")

    gates = candidate.get("pass_gates") or {}
    if gates.get("no_silent_collapse_local") is not False:
        failures.append("expected_no_silent_collapse_local_false")
    if gates.get("real_projected_burden_reduction") is not True:
        failures.append("expected_real_projected_burden_reduction_true")
    if gates.get("source_surface_honesty") is not True:
        failures.append("source_surface_honesty_not_true")
    if gates.get("scale_bands_forbidden_until_no_silent_collapse") is not True:
        failures.append("scale_band_guard_not_true")
    for key in [
        "audit_recoverability",
        "debug_payload_not_counted_as_signature",
        "no_rowid_identity_leak",
        "observer_only_containment",
        "raw_hash_truth_surface_forbidden",
        "signature_payload_measured_separately",
    ]:
        if gates.get(key) is not True:
            failures.append(f"expected_pass_gate_true:{key}:{gates.get(key)}")

    dist = candidate.get("distinguishability_measurements") or {}
    if dist.get("false_merge_count") != 10:
        failures.append(f"false_merge_count_expected_10:{dist.get('false_merge_count')}")
    if dist.get("collision_count") != 10:
        failures.append(f"collision_count_expected_10:{dist.get('collision_count')}")
    if dist.get("distinct_full_occurrence_keys") != 176:
        failures.append(f"distinct_full_occurrence_keys_expected_176:{dist.get('distinct_full_occurrence_keys')}")
    if dist.get("distinct_candidate_signatures") != 20:
        failures.append(f"distinct_candidate_signatures_expected_20:{dist.get('distinct_candidate_signatures')}")
    if dist.get("distinguishability_retention_ratio", 1.0) >= 0.5:
        failures.append(f"retention_expected_low:{dist.get('distinguishability_retention_ratio')}")

    burden = candidate.get("burden_measurements") or {}
    if burden.get("burden_ratio_projected", 1.0) >= 1.0:
        failures.append(f"projected_burden_ratio_expected_under_1:{burden.get('burden_ratio_projected')}")
    if burden.get("burden_ratio_signature_payload", 1.0) >= burden.get("burden_ratio_projected", 0.0):
        failures.append("signature_payload_ratio_not_less_than_projected_ratio")

    if policy.get("policy_id") != EXPECTED_POLICY_ID or policy.get("gate") != "PASS":
        failures.append("policy_source_invalid")
    if policy.get("authority", {}).get("authorizes_scale_band_run_now") is not False:
        failures.append("policy_wrongly_authorizes_scale_bands")

    if source_diag.get("diagnostic_id") != EXPECTED_SOURCE_DIAGNOSTIC_ID or source_diag.get("gate") != "PASS":
        failures.append("source_diagnostic_invalid")

    return failures


def group_rows(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        groups[str(row.get("candidate_delta_signature"))].append(row)
    return groups


def analyze_collision_group(sig: str, group: list[dict[str, Any]]) -> dict[str, Any]:
    full_keys = sorted({str(r.get("full_occurrence_key")) for r in group})
    case_ids = sorted({str(r.get("case_id")) for r in group})
    occurrence_ids = sorted({str(r.get("occurrence_id")) for r in group})
    payloads = [r.get("signature_payload") or {} for r in group]
    payload_fingerprints = sorted({norm(p) for p in payloads})
    rowids = [
        safe_int((r.get("audit_pointer_or_full_receipt_ref") or {}).get("receipt_rowid"))
        for r in group
    ]
    rowids_int = sorted(x for x in rowids if x is not None)

    occurrence_equals_audit_rowid = []
    for r in group:
        occ = safe_int(r.get("occurrence_id"))
        rid = safe_int((r.get("audit_pointer_or_full_receipt_ref") or {}).get("receipt_rowid"))
        occurrence_equals_audit_rowid.append(occ is not None and rid is not None and occ == rid)

    signature_payload_keys = sorted({k for payload in payloads for k in payload.keys()})

    return {
        "candidate_delta_signature": sig,
        "group_size": len(group),
        "distinct_full_occurrence_keys": len(full_keys),
        "full_occurrence_keys_sample": full_keys[:12],
        "case_ids": case_ids[:20],
        "case_id_count": len(case_ids),
        "occurrence_ids_sample": occurrence_ids[:20],
        "occurrence_id_count": len(occurrence_ids),
        "audit_receipt_rowid_min": min(rowids_int) if rowids_int else None,
        "audit_receipt_rowid_max": max(rowids_int) if rowids_int else None,
        "audit_receipt_rowid_count": len(rowids_int),
        "occurrence_id_equals_audit_rowid_all": all(occurrence_equals_audit_rowid) if occurrence_equals_audit_rowid else False,
        "signature_payload_keys": signature_payload_keys,
        "signature_payload_distinct_forms": len(payload_fingerprints),
        "signature_payload_sample": payloads[0] if payloads else {},
        "root_cause_hint": (
            "Full occurrence separability is audit-locator-level while candidate signature has identical lawful payload inside the group."
            if len(payload_fingerprints) == 1 and all(occurrence_equals_audit_rowid)
            else "Candidate signature collapses multiple full occurrence keys; inspect payload form and audit locator usage."
        ),
    }


def build_field_cause(candidate: dict[str, Any], collision_gallery: list[dict[str, Any]]) -> dict[str, Any]:
    surface = candidate.get("source_surface") or {}
    stats = surface.get("stats") or {}

    missing_or_non_discriminative = {}
    for field, stat in stats.items():
        present = stat.get("present", 0)
        distinct = stat.get("distinct_present_values", 0)
        missing_rate = stat.get("missing_rate", 0)
        if present == 0 or distinct <= 1 or missing_rate >= 0.9:
            missing_or_non_discriminative[field] = stat

    payload_key_counter = Counter()
    for item in collision_gallery:
        for key in item.get("signature_payload_keys") or []:
            payload_key_counter[key] += 1

    return {
        "transition_sufficient": surface.get("transition_sufficient"),
        "canonical_discriminator_sufficient": surface.get("canonical_discriminator_sufficient"),
        "weak_metric_discriminator_available": surface.get("weak_metric_discriminator_available"),
        "surface_honesty_status": surface.get("honesty_status"),
        "missing_or_non_discriminative_fields": missing_or_non_discriminative,
        "collision_payload_key_frequency": dict(sorted(payload_key_counter.items())),
        "critical_observation": [
            "state_hash_before and state_hash_after are absent across the source surface.",
            "move_id is present but constant, so it cannot separate occurrences.",
            "case_id has only 10 values across 176 occurrences; it separates cases, not within-case occurrences.",
            "halt_reason is sparse and only present for 10 receipts.",
            "false merges are therefore expected unless a lawful within-case occurrence discriminator is extracted.",
        ],
    }


def decide_next(candidate: dict[str, Any], collision_gallery: list[dict[str, Any]], field_cause: dict[str, Any]) -> dict[str, Any]:
    dist = candidate.get("distinguishability_measurements") or {}
    burden = candidate.get("burden_measurements") or {}
    source = candidate.get("source_surface") or {}
    stats = source.get("stats") or {}

    audit_locator_used_as_full_key = all(
        item.get("occurrence_id_equals_audit_rowid_all") is True
        for item in collision_gallery
    )

    transition_missing = (
        stats.get("state_hash_before", {}).get("present", 0) == 0
        and stats.get("state_hash_after", {}).get("present", 0) == 0
    )

    case_only_discriminator = (
        source.get("canonical_discriminator_sufficient") is True
        and source.get("transition_sufficient") is False
        and source.get("weak_metric_discriminator_available") is False
    )

    if dist.get("false_merge_count", 0) > 0 and transition_missing and case_only_discriminator:
        recommended = "BUILD_CANONICAL_TRANSITION_SURFACE_PROBE_POLICY_V0"
        reason = "v0.1 payload is small and burden-positive, but source surface lacks lawful transition/within-case occurrence identity."
    elif dist.get("false_merge_count", 0) > 0:
        recommended = "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_2_POLICY"
        reason = "false merges remain; next candidate may refine extraction if lawful fields exist."
    elif burden.get("burden_ratio_projected", 1.0) >= 1.0:
        recommended = "DIAGNOSE_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1_BURDEN"
        reason = "false merges cleared but projected burden is not lower than full receipts."
    else:
        recommended = "DESIGN_STABLE_DELTA_SIGNATURE_SCALE_BANDS_V0"
        reason = "local no-silent-collapse and projected burden reduction both passed."

    return {
        "do_not_scale_current_candidate": True,
        "do_not_accept_current_candidate": True,
        "do_not_authorize_scale_mode": True,
        "do_not_authorize_receipt_replacement": True,
        "burden_side_progress_confirmed": burden.get("burden_ratio_projected", 1.0) < 1.0,
        "distinguishability_blocker_confirmed": dist.get("false_merge_count", 0) > 0,
        "audit_locator_distinguishability_detected": audit_locator_used_as_full_key,
        "transition_surface_missing": transition_missing,
        "case_only_discriminator": case_only_discriminator,
        "recommended_next_command_goal": recommended,
        "reason": reason,
    }


def build_diagnostic(candidate_probe_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    candidate = load_json(CANDIDATE_RECEIPT_DIR / f"{candidate_probe_id}.json")
    policy = load_json(POLICY_DIR / f"{EXPECTED_POLICY_ID}.json")
    source_diag = load_json(DIAGNOSTIC_DIR / f"{EXPECTED_SOURCE_DIAGNOSTIC_ID}.json")
    rows = load_jsonl(ROOT / candidate["rows_path"])

    failures = verify_source(candidate, policy, source_diag, rows)

    groups = group_rows(rows)
    collision_groups = {
        sig: group
        for sig, group in groups.items()
        if len({str(r.get("full_occurrence_key")) for r in group}) > 1
    }

    if len(collision_groups) != candidate.get("distinguishability_measurements", {}).get("false_merge_count"):
        failures.append(
            f"collision_group_count_mismatch:{len(collision_groups)}!={candidate.get('distinguishability_measurements', {}).get('false_merge_count')}"
        )

    collision_gallery = [
        analyze_collision_group(sig, group)
        for sig, group in sorted(collision_groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))
    ]

    collision_summary = {
        "collision_group_count": len(collision_groups),
        "largest_collision_group_size": max((len(group) for group in collision_groups.values()), default=0),
        "collision_group_sizes_top10": sorted([len(group) for group in collision_groups.values()], reverse=True)[:10],
        "collision_rows_total": sum(len(group) for group in collision_groups.values()),
        "total_candidate_signature_groups": len(groups),
        "non_collision_signature_groups": sum(1 for group in groups.values() if len({str(r.get("full_occurrence_key")) for r in group}) == 1),
    }

    field_cause = build_field_cause(candidate, collision_gallery)
    decision = decide_next(candidate, collision_gallery, field_cause)

    diagnostic = {
        "schema_version": "stable_delta_signature_candidate_v0_1_false_merge_diagnostic_v0",
        "diagnostic_name": DIAGNOSTIC_NAME,
        "source_candidate_probe_id": candidate_probe_id,
        "source_candidate_receipt_id": candidate.get("receipt_id"),
        "source_policy_id": candidate.get("source_policy_id"),
        "source_diagnostic_id": candidate.get("source_diagnostic_id"),
        "mode": "OUTER_OBSERVER_ONLY_DIAGNOSTIC",
        "scope": {
            "read_only": True,
            "runtime_receipt_system_changed": False,
            "candidate_probe_changed": False,
            "scale_mode_authorized": False,
            "receipt_replacement_authorized": False,
            "receipt_deletion_authorized": False,
            "receipt_compression_authorized": False,
            "scale_bands_authorized": False,
            "theorem_content_authorized": False,
        },
        "source_candidate_summary": {
            "terminal_decision": candidate.get("terminal_decision"),
            "gate": candidate.get("gate"),
            "full_receipt_count": candidate.get("burden_measurements", {}).get("full_receipt_count"),
            "candidate_signature_count": candidate.get("burden_measurements", {}).get("candidate_signature_count"),
            "full_receipt_bytes": candidate.get("burden_measurements", {}).get("full_receipt_bytes"),
            "signature_payload_bytes": candidate.get("burden_measurements", {}).get("signature_payload_bytes"),
            "projected_scale_row_bytes": candidate.get("burden_measurements", {}).get("projected_scale_row_bytes"),
            "burden_ratio_projected": candidate.get("burden_measurements", {}).get("burden_ratio_projected"),
            "burden_ratio_signature_payload": candidate.get("burden_measurements", {}).get("burden_ratio_signature_payload"),
            "distinct_full_occurrence_keys": candidate.get("distinguishability_measurements", {}).get("distinct_full_occurrence_keys"),
            "distinct_candidate_signatures": candidate.get("distinguishability_measurements", {}).get("distinct_candidate_signatures"),
            "distinguishability_retention_ratio": candidate.get("distinguishability_measurements", {}).get("distinguishability_retention_ratio"),
            "collision_count": candidate.get("distinguishability_measurements", {}).get("collision_count"),
            "false_merge_count": candidate.get("distinguishability_measurements", {}).get("false_merge_count"),
        },
        "collision_summary": collision_summary,
        "collision_gallery": collision_gallery,
        "field_cause_analysis": field_cause,
        "root_cause": {
            "primary_failure": "LAWFUL_PAYLOAD_TOO_COARSE_FOR_WITHIN_CASE_OCCURRENCE_SEPARABILITY",
            "burden_status": "BURDEN_SIDE_PROGRESS_CONFIRMED",
            "distinguishability_status": "FAILED_LOCAL_NO_SILENT_COLLAPSE",
            "diagnosis": "v0.1 separated signature/debug/audit burden correctly, but the lawful signature payload lacks transition or within-case occurrence fields needed to preserve all full occurrence keys.",
        },
        "decision": decision,
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": decision["recommended_next_command_goal"] if not failures else None,
            "stop_code": None if not failures else "STOP_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_1_FALSE_MERGE_DIAGNOSTIC_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    diagnostic_id = sha8({
        "diagnostic_name": diagnostic["diagnostic_name"],
        "source_candidate_probe_id": candidate_probe_id,
        "root_cause": diagnostic["root_cause"],
        "collision_summary": collision_summary,
        "field_cause_analysis": field_cause,
        "decision": decision,
    })
    diagnostic["diagnostic_id"] = diagnostic_id
    diagnostic["diagnostic_sig8"] = diagnostic_id

    receipt = {
        "schema_version": "stable_delta_signature_candidate_v0_1_false_merge_diagnostic_receipt_v0",
        "diagnostic_id": diagnostic_id,
        "diagnostic_sig8": diagnostic_id,
        "diagnostic_path": f"data/stable_delta_signature_candidate_v0_1_false_merge_diagnostics/{diagnostic_id}.json",
        "source_candidate_probe_id": candidate_probe_id,
        "source_candidate_receipt_id": candidate.get("receipt_id"),
        "source_policy_id": candidate.get("source_policy_id"),
        "source_diagnostic_id": candidate.get("source_diagnostic_id"),
        "source_terminal_decision": candidate.get("terminal_decision"),
        "root_cause": diagnostic["root_cause"],
        "collision_summary": collision_summary,
        "decision": decision,
        "terminal": diagnostic["terminal"],
        "gate": diagnostic["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    (OUT_DIR / f"{diagnostic_id}.json").write_text(json.dumps(diagnostic, indent=2, sort_keys=True))
    (OUT_RECEIPT_DIR / f"{diagnostic_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return diagnostic, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--candidate-probe-id", default=EXPECTED_CANDIDATE_PROBE_ID)
    args = parser.parse_args()

    diagnostic, receipt = build_diagnostic(args.candidate_probe_id)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"diagnostic_id={diagnostic['diagnostic_id']}")
    print(f"diagnostic_json_path=data/stable_delta_signature_candidate_v0_1_false_merge_diagnostics/{diagnostic['diagnostic_id']}.json")
    print(f"diagnostic_receipt_path=data/stable_delta_signature_candidate_v0_1_false_merge_diagnostic_receipts/{diagnostic['diagnostic_id']}.json")
    return 0 if diagnostic["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
