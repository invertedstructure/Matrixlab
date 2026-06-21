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

SOURCE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_receipts"
OUT_DIR = ROOT / "data" / "bounded_scale_false_merge_diagnostics"
OUT_RECEIPT_DIR = ROOT / "data" / "bounded_scale_false_merge_diagnostic_receipts"

EXPECTED_SOURCE_PROBE_ID = "227e9426"
EXPECTED_SOURCE_RECEIPT_ID = "0ae57255"
EXPECTED_SOURCE_POLICY_ID = "b79955ce"
EXPECTED_SOURCE_V02_PROBE_ID = "bcdb3d93"

DIAGNOSTIC_NAME = "DIAGNOSE_BOUNDED_SCALE_FALSE_MERGES_V0"
NEXT_COMMAND_GOAL = "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_3_POLICY"


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
        raise SystemExit(f"missing required jsonl: {path}")
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def verify_source_receipt(source: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if source.get("probe_id") != EXPECTED_SOURCE_PROBE_ID:
        failures.append(f"source_probe_id_wrong:{source.get('probe_id')}")
    if source.get("receipt_id") != EXPECTED_SOURCE_RECEIPT_ID:
        failures.append(f"source_receipt_id_wrong:{source.get('receipt_id')}")
    if source.get("source_policy_id") != EXPECTED_SOURCE_POLICY_ID:
        failures.append(f"source_policy_id_wrong:{source.get('source_policy_id')}")
    if source.get("source_v02_probe_id") != EXPECTED_SOURCE_V02_PROBE_ID:
        failures.append(f"source_v02_probe_id_wrong:{source.get('source_v02_probe_id')}")
    if source.get("gate") != "PASS":
        failures.append(f"source_gate_not_PASS:{source.get('gate')}")
    if source.get("mode") != "OUTER_OBSERVER_ONLY":
        failures.append(f"source_mode_wrong:{source.get('mode')}")
    if source.get("terminal_decision") != "FAIL_SCALE_FALSE_MERGE":
        failures.append(f"source_terminal_not_FAIL_SCALE_FALSE_MERGE:{source.get('terminal_decision')}")
    if source.get("terminal", {}).get("type") != "STOP":
        failures.append(f"source_terminal_type_not_STOP:{source.get('terminal', {}).get('type')}")
    if source.get("terminal", {}).get("stop_code") != "FAIL_SCALE_FALSE_MERGE":
        failures.append(f"source_stop_code_wrong:{source.get('terminal', {}).get('stop_code')}")

    selection = source.get("bounded_scale_band_selection") or {}
    if selection.get("selection_mode") != "BOUNDED_BY_DEFAULT":
        failures.append(f"selection_mode_wrong:{selection.get('selection_mode')}")
    if selection.get("full_registry_used") is not False:
        failures.append("source_used_full_registry")
    if selection.get("source_run_included") is not True:
        failures.append("source_run_not_included")
    if selection.get("latest_compatible_runs_requested") != 10:
        failures.append(f"latest_compatible_runs_not_10:{selection.get('latest_compatible_runs_requested')}")
    if selection.get("selected_run_count", 10**9) > selection.get("bounded_default_max_registry_runs_touched", 0):
        failures.append("selected_run_count_exceeds_bound")

    agg = source.get("aggregate_measurements") or {}
    if agg.get("bands_failed", 0) <= 0:
        failures.append(f"source_has_no_failed_bands:{agg.get('bands_failed')}")
    if agg.get("worst_false_merge_count", 0) <= 0:
        failures.append(f"source_has_no_false_merge:{agg.get('worst_false_merge_count')}")
    if agg.get("worst_collision_count", 0) <= 0:
        failures.append(f"source_has_no_collision:{agg.get('worst_collision_count')}")
    if agg.get("worst_distinguishability_retention_ratio", 1.0) >= 1.0:
        failures.append(f"source_retention_not_degraded:{agg.get('worst_distinguishability_retention_ratio')}")
    if agg.get("worst_burden_ratio_projected", 1.0) >= 1.0:
        failures.append(f"source_burden_not_reduced:{agg.get('worst_burden_ratio_projected')}")
    if agg.get("worst_source_surface_regression_count") != 0:
        failures.append(f"source_surface_regression_present:{agg.get('worst_source_surface_regression_count')}")
    if agg.get("worst_identity_leak_count") != 0:
        failures.append(f"identity_leak_present:{agg.get('worst_identity_leak_count')}")
    if agg.get("worst_audit_recoverability_failures") != 0:
        failures.append(f"audit_recoverability_failure_present:{agg.get('worst_audit_recoverability_failures')}")

    gates = source.get("pass_gates") or {}
    expected_true = [
        "authority_containment",
        "bounded_selection",
        "burden_reduction_all_bands",
        "local_precondition_preserved",
        "source_surface_regression",
        "truth_surface",
        "no_identity_leak",
        "audit_recoverability",
        "scale_coverage_honesty",
    ]
    for key in expected_true:
        if gates.get(key) is not True:
            failures.append(f"source_gate_expected_true:{key}:{gates.get(key)}")
    if gates.get("no_false_merge_all_bands") is not False:
        failures.append(f"source_false_merge_gate_not_false:{gates.get('no_false_merge_all_bands')}")

    auth = source.get("authority_guards") or {}
    if auth.get("observer_only") is not True:
        failures.append("observer_only_not_true")
    for key in [
        "registry_sqlite_changed",
        "runtime_receipt_emission_changed",
        "scale_mode_authorized",
        "scale_band_run_authorized",
        "candidate_acceptance_authorized",
        "registry_write_authorized",
        "receipt_replacement_authorized",
        "receipt_deletion_authorized",
        "receipt_compression_authorized",
        "raw_receipt_hash_used_as_truth_surface",
        "full_registry_scan_used",
    ]:
        if auth.get(key) is not False:
            failures.append(f"source_authority_or_mutation_not_false:{key}:{auth.get(key)}")

    return failures


def rows_by_band(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        out[row.get("band_id", "")].append(row)
    return dict(out)


def debug_projection(row: dict[str, Any]) -> dict[str, Any]:
    dbg = row.get("debug_sidecar") or {}
    audit = row.get("audit_pointer") or {}
    sig = row.get("signature_payload") or {}
    return {
        "source_run_id": row.get("source_run_id"),
        "full_occurrence_key": row.get("full_occurrence_key"),
        "candidate_delta_signature": row.get("candidate_delta_signature"),
        "signature_payload": sig,
        "audit_pointer": audit,
        "case_id_debug_only": dbg.get("case_id_debug_only"),
        "cycle_n_debug_only": dbg.get("cycle_n_debug_only"),
        "depth_debug_only": dbg.get("depth_debug_only"),
        "family_debug_only": dbg.get("family_debug_only"),
        "halt_reason": dbg.get("halt_reason"),
        "move_profile_id": dbg.get("move_profile_id"),
        "compact_delta_debug": dbg.get("compact_delta_debug"),
    }


def differing_fields(records: list[dict[str, Any]], fields: list[str]) -> dict[str, list[Any]]:
    diffs: dict[str, list[Any]] = {}
    for field in fields:
        values = []
        seen = set()
        for record in records:
            value = record.get(field)
            key = json.dumps(value, sort_keys=True, default=str)
            if key not in seen:
                seen.add(key)
                values.append(value)
        if len(values) > 1:
            diffs[field] = values
    return diffs


def collision_groups_for_band(band_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_sig: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in band_rows:
        by_sig[row.get("candidate_delta_signature")].append(row)

    groups: list[dict[str, Any]] = []
    for sig, records in by_sig.items():
        full_keys = sorted({r.get("full_occurrence_key") for r in records})
        if len(full_keys) <= 1:
            continue

        projections = [debug_projection(r) for r in records]
        diffs = differing_fields(
            projections,
            [
                "source_run_id",
                "full_occurrence_key",
                "case_id_debug_only",
                "cycle_n_debug_only",
                "depth_debug_only",
                "family_debug_only",
                "halt_reason",
                "move_profile_id",
                "compact_delta_debug",
            ],
        )
        audit_rowids = sorted({
            str((r.get("audit_pointer") or {}).get("receipt_rowid"))
            for r in records
            if (r.get("audit_pointer") or {}).get("receipt_rowid") is not None
        })

        groups.append({
            "candidate_delta_signature": sig,
            "collision_record_count": len(records),
            "distinct_full_occurrence_keys": len(full_keys),
            "full_occurrence_keys": full_keys[:20],
            "audit_receipt_rowids": audit_rowids[:20],
            "signature_payload": records[0].get("signature_payload"),
            "differing_debug_fields": diffs,
            "records_preview": projections[:10],
        })

    groups.sort(key=lambda g: (-g["distinct_full_occurrence_keys"], g["candidate_delta_signature"]))
    return groups


def classify_false_merge(groups: list[dict[str, Any]]) -> dict[str, Any]:
    field_counter: Counter[str] = Counter()
    all_have_same_signature_payload = True

    for group in groups:
        payloads = {
            json.dumps(record.get("signature_payload"), sort_keys=True, default=str)
            for record in group.get("records_preview", [])
        }
        if len(payloads) > 1:
            all_have_same_signature_payload = False
        for field in group.get("differing_debug_fields", {}):
            field_counter[field] += 1

    if not groups:
        primary_class = "NO_COLLISION_GROUPS_FOUND"
    elif all_have_same_signature_payload and any(field in field_counter for field in [
        "case_id_debug_only",
        "cycle_n_debug_only",
        "source_run_id",
        "full_occurrence_key",
    ]):
        primary_class = "REPEATED_TRANSITION_SIGNATURE_COLLAPSES_DISTINCT_OCCURRENCES"
    elif all_have_same_signature_payload:
        primary_class = "REPEATED_TRANSITION_SIGNATURE_COLLAPSE_UNRESOLVED_DEBUG_SURFACE"
    else:
        primary_class = "SIGNATURE_PAYLOAD_VARIANCE_OR_DIAGNOSTIC_BUG"

    return {
        "primary_class": primary_class,
        "all_collision_records_share_candidate_signature_payload": all_have_same_signature_payload,
        "differing_debug_field_frequency": dict(field_counter),
        "interpretation": (
            "v0.2 encodes transition identity, not occurrence identity, when the same state_before/move/state_after tuple recurs within a bounded scale band."
            if primary_class == "REPEATED_TRANSITION_SIGNATURE_COLLAPSES_DISTINCT_OCCURRENCES"
            else "False-merge source needs deeper inspection before candidate extension."
        ),
    }


def build_diagnostic(source_probe_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_path = SOURCE_RECEIPT_DIR / f"{source_probe_id}.json"
    source = load_json(source_path)
    source_failures = verify_source_receipt(source)

    rows_path = ROOT / source.get("scale_band_rows_path", "")
    scale_rows = load_jsonl(rows_path)
    band_rows = rows_by_band(scale_rows)

    failed_bands = [
        band for band in source.get("band_measurements", [])
        if not band.get("band_passed")
    ]

    failed_axis_counts = Counter(str(b.get("axis")) for b in failed_bands)
    failed_run_counts = Counter(str(b.get("run_id")) for b in failed_bands)
    failed_reason_counts = Counter(
        reason
        for band in failed_bands
        for reason in band.get("failure_reasons", [])
    )

    failed_band_diagnostics: list[dict[str, Any]] = []
    all_collision_groups: list[dict[str, Any]] = []

    for band in failed_bands:
        bid = band.get("band_id")
        groups = collision_groups_for_band(band_rows.get(bid, []))
        for group in groups:
            group_with_band = dict(group)
            group_with_band.update({
                "band_id": bid,
                "axis": band.get("axis"),
                "axis_value": band.get("axis_value"),
                "run_id": band.get("run_id"),
            })
            all_collision_groups.append(group_with_band)

        failed_band_diagnostics.append({
            "band_id": bid,
            "axis": band.get("axis"),
            "axis_value": band.get("axis_value"),
            "run_id": band.get("run_id"),
            "occurrences_total": band.get("occurrences_total"),
            "distinct_full_occurrence_keys": band.get("distinct_full_occurrence_keys"),
            "distinct_candidate_signatures": band.get("distinct_candidate_signatures"),
            "collision_count": band.get("collision_count"),
            "false_merge_count": band.get("false_merge_count"),
            "false_split_count": band.get("false_split_count"),
            "distinguishability_retention_ratio": band.get("distinguishability_retention_ratio"),
            "burden_ratio_projected": band.get("burden_ratio_projected"),
            "failure_reasons": band.get("failure_reasons"),
            "collision_groups": groups,
        })

    classification = classify_false_merge(all_collision_groups)

    source_aggregate = source.get("aggregate_measurements", {})
    summary = {
        "source_probe_id": source.get("probe_id"),
        "source_receipt_id": source.get("receipt_id"),
        "source_policy_id": source.get("source_policy_id"),
        "source_terminal_decision": source.get("terminal_decision"),
        "bounded_default_used": source.get("scale_coverage", {}).get("bounded_default_used"),
        "full_registry_used": source.get("scale_coverage", {}).get("full_registry_used"),
        "compatible_run_count": source_aggregate.get("compatible_run_count"),
        "bands_total": source_aggregate.get("bands_total"),
        "bands_passed": source_aggregate.get("bands_passed"),
        "bands_failed": source_aggregate.get("bands_failed"),
        "worst_false_merge_count": source_aggregate.get("worst_false_merge_count"),
        "worst_collision_count": source_aggregate.get("worst_collision_count"),
        "worst_distinguishability_retention_ratio": source_aggregate.get("worst_distinguishability_retention_ratio"),
        "worst_burden_ratio_projected": source_aggregate.get("worst_burden_ratio_projected"),
        "failed_axis_counts": dict(failed_axis_counts),
        "failed_run_counts": dict(failed_run_counts),
        "failed_reason_counts": dict(failed_reason_counts),
        "collision_group_count": len(all_collision_groups),
        "collision_signature_count": len({g.get("candidate_delta_signature") for g in all_collision_groups}),
        "collision_rows_total": sum(g.get("collision_record_count", 0) for g in all_collision_groups),
    }

    diagnosis_status = "SOURCE_VERIFICATION_FAILED" if source_failures else "DIAGNOSED"
    terminal_type = "STOP" if source_failures else "ADVANCE"

    diagnostic = {
        "schema_version": "bounded_scale_false_merge_diagnostic_v0",
        "diagnostic_name": DIAGNOSTIC_NAME,
        "diagnosis_status": diagnosis_status,
        "source_probe_id": EXPECTED_SOURCE_PROBE_ID,
        "source_receipt_id": EXPECTED_SOURCE_RECEIPT_ID,
        "source_policy_id": EXPECTED_SOURCE_POLICY_ID,
        "source_v02_probe_id": EXPECTED_SOURCE_V02_PROBE_ID,
        "source_rows_path": source.get("scale_band_rows_path"),
        "summary": summary,
        "classification": classification,
        "failed_band_diagnostics": failed_band_diagnostics,
        "collision_groups_top20": all_collision_groups[:20],
        "decision": {
            "candidate_v0_2_rejected_for_scale_acceptance": True,
            "burden_side_remains_viable": source_aggregate.get("worst_burden_ratio_projected", 1.0) < 1.0,
            "authority_side_clean": source.get("pass_gates", {}).get("authority_containment") is True,
            "source_surface_clean": source.get("pass_gates", {}).get("source_surface_regression") is True,
            "identity_leak_absent": source.get("pass_gates", {}).get("no_identity_leak") is True,
            "primary_blocker": "FALSE_MERGE_UNDER_BOUNDED_SCALE",
            "do_not_full_registry_scan": True,
            "do_not_accept_candidate": True,
            "do_not_change_runtime": True,
            "do_not_patch_by_adding_case_id_or_cycle_n_as_primary_identity": True,
            "recommended_next_command_goal": NEXT_COMMAND_GOAL,
            "next_design_pressure": "Need a lawful occurrence-level discriminator or equivalence policy; v0.2 transition tuple alone is insufficient across bounded scale.",
        },
        "authority": {
            "observer_only": True,
            "authorizes_candidate_acceptance": False,
            "authorizes_scale_mode": False,
            "authorizes_full_registry_scan": False,
            "authorizes_runtime_receipt_emission_change": False,
            "authorizes_registry_write": False,
            "authorizes_receipt_replacement": False,
            "authorizes_receipt_compression": False,
            "authorizes_raw_receipt_hash_truth_surface": False,
            "authorizes_case_id_or_cycle_n_primary_identity_patch": False,
        },
        "terminal": {
            "type": terminal_type,
            "next_command_goal": NEXT_COMMAND_GOAL if not source_failures else None,
            "stop_code": None if not source_failures else "STOP_SOURCE_SCALE_FAILURE_RECEIPT_INVALID",
        },
        "gate": "PASS" if not source_failures else "FAIL",
        "failures": source_failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    diagnostic_id = sha8({
        "diagnostic_name": DIAGNOSTIC_NAME,
        "source_probe_id": diagnostic["source_probe_id"],
        "source_receipt_id": diagnostic["source_receipt_id"],
        "summary": diagnostic["summary"],
        "classification": diagnostic["classification"],
        "decision": diagnostic["decision"],
    })
    diagnostic["diagnostic_id"] = diagnostic_id
    diagnostic["diagnostic_sig8"] = diagnostic_id

    receipt = {
        "schema_version": "bounded_scale_false_merge_diagnostic_receipt_v0",
        "diagnostic_id": diagnostic_id,
        "diagnostic_sig8": diagnostic_id,
        "diagnostic_name": DIAGNOSTIC_NAME,
        "diagnosis_status": diagnosis_status,
        "diagnostic_path": f"data/bounded_scale_false_merge_diagnostics/{diagnostic_id}.json",
        "source_probe_id": diagnostic["source_probe_id"],
        "source_receipt_id": diagnostic["source_receipt_id"],
        "source_policy_id": diagnostic["source_policy_id"],
        "source_v02_probe_id": diagnostic["source_v02_probe_id"],
        "summary": summary,
        "classification": classification,
        "decision": diagnostic["decision"],
        "authority": diagnostic["authority"],
        "terminal": diagnostic["terminal"],
        "gate": diagnostic["gate"],
        "failures": source_failures,
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
    parser.add_argument("--source-probe-id", default=EXPECTED_SOURCE_PROBE_ID)
    args = parser.parse_args()

    diagnostic, receipt = build_diagnostic(args.source_probe_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"diagnostic_id={diagnostic['diagnostic_id']}")
    print(f"diagnostic_json_path=data/bounded_scale_false_merge_diagnostics/{diagnostic['diagnostic_id']}.json")
    print(f"diagnostic_receipt_path=data/bounded_scale_false_merge_diagnostic_receipts/{diagnostic['diagnostic_id']}.json")

    return 0 if diagnostic["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
