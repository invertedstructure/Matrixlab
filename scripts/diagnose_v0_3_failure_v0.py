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

V03_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_receipts"
V03_ROWS_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_rows"
V02_SCALE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_receipts"
DIAG_DIR = ROOT / "data" / "bounded_scale_false_merge_diagnostics"

OUT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_failure_diagnostics"
OUT_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_failure_diagnostic_receipts"

EXPECTED_V03_PROBE_ID = "bd1beabe"
EXPECTED_V03_RECEIPT_ID = "c598371b"
EXPECTED_V03_POLICY_ID = "78a6fbec"
EXPECTED_V02_SCALE_PROBE_ID = "227e9426"
EXPECTED_DIAGNOSTIC_ID = "62c8d96c"

DIAGNOSTIC_NAME = "DIAGNOSE_V0_3_FAILURE_V0"
NEXT_COMMAND_GOAL = "BUILD_RECURRENCE_AWARE_OCCURRENCE_SIGNATURE_POLICY_V0"

ALLOWED_DELTA_BUCKET_COLUMNS = [
    "row_delta",
    "col_delta",
    "rank_delta",
    "support_delta",
    "distinct_column_types_before",
    "distinct_column_types_after",
    "new_column_types_added",
    "compression_ratio",
]


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


def verify_v03_source(v03: dict[str, Any], v02_scale: dict[str, Any], prior_diag: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if v03.get("probe_id") != EXPECTED_V03_PROBE_ID:
        failures.append(f"v03_probe_id_wrong:{v03.get('probe_id')}")
    if v03.get("receipt_id") != EXPECTED_V03_RECEIPT_ID:
        failures.append(f"v03_receipt_id_wrong:{v03.get('receipt_id')}")
    if v03.get("source_policy_id") != EXPECTED_V03_POLICY_ID:
        failures.append(f"v03_policy_id_wrong:{v03.get('source_policy_id')}")
    if v03.get("source_diagnostic_id") != EXPECTED_DIAGNOSTIC_ID:
        failures.append(f"v03_source_diagnostic_wrong:{v03.get('source_diagnostic_id')}")
    if v03.get("source_scale_probe_id") != EXPECTED_V02_SCALE_PROBE_ID:
        failures.append(f"v03_source_scale_wrong:{v03.get('source_scale_probe_id')}")
    if v03.get("gate") != "PASS":
        failures.append(f"v03_gate_not_PASS:{v03.get('gate')}")
    if v03.get("mode") != "OUTER_OBSERVER_ONLY":
        failures.append(f"v03_mode_wrong:{v03.get('mode')}")
    if v03.get("terminal_decision") != "FAIL_V0_3_FALSE_MERGE_PERSISTS":
        failures.append(f"v03_terminal_wrong:{v03.get('terminal_decision')}")
    if v03.get("terminal", {}).get("type") != "STOP":
        failures.append(f"v03_terminal_type_wrong:{v03.get('terminal', {}).get('type')}")

    agg = v03.get("aggregate_measurements") or {}
    if agg.get("known_failed_bands_cleared") is not False:
        failures.append("v03_claims_known_failed_bands_cleared")
    if agg.get("known_failed_remaining_false_merge_bands") != 10:
        failures.append(f"known_failed_remaining_false_merge_bands_not_10:{agg.get('known_failed_remaining_false_merge_bands')}")
    if agg.get("bands_failed") != 266:
        failures.append(f"v03_bands_failed_not_266:{agg.get('bands_failed')}")
    if agg.get("bands_passed") != 0:
        failures.append(f"v03_bands_passed_not_0:{agg.get('bands_passed')}")
    if agg.get("worst_false_merge_count") != 1:
        failures.append(f"v03_worst_false_merge_not_1:{agg.get('worst_false_merge_count')}")
    if agg.get("worst_burden_ratio_projected", 0) <= 1.0:
        failures.append(f"v03_burden_not_regressed:{agg.get('worst_burden_ratio_projected')}")
    if agg.get("worst_identity_leak_count") != 0:
        failures.append(f"v03_identity_leak:{agg.get('worst_identity_leak_count')}")
    if agg.get("worst_source_surface_regression_count") != 0:
        failures.append(f"v03_source_surface_regression:{agg.get('worst_source_surface_regression_count')}")
    if agg.get("worst_delta_bucket_coverage_failures") != 0:
        failures.append(f"v03_delta_bucket_coverage_failure:{agg.get('worst_delta_bucket_coverage_failures')}")

    gates = v03.get("pass_gates") or {}
    for key in [
        "authority_containment",
        "bounded_selection_reused",
        "source_surface_regression",
        "delta_bucket_coverage",
        "truth_surface",
        "no_identity_leak",
        "audit_recoverability",
        "candidate_not_accepted",
        "scale_mode_not_authorized",
    ]:
        if gates.get(key) is not True:
            failures.append(f"v03_gate_expected_true:{key}:{gates.get(key)}")
    for key in [
        "known_failed_bands_cleared",
        "no_false_merge_all_bands",
        "burden_reduction_all_bands",
    ]:
        if gates.get(key) is not False:
            failures.append(f"v03_gate_expected_false:{key}:{gates.get(key)}")

    auth = v03.get("authority_guards") or {}
    if auth.get("observer_only") is not True:
        failures.append("v03_not_observer_only")
    for key in [
        "registry_sqlite_changed",
        "runtime_receipt_emission_changed",
        "full_registry_scan_used",
        "scale_mode_authorized",
        "candidate_acceptance_authorized",
        "registry_write_authorized",
        "receipt_replacement_authorized",
        "receipt_deletion_authorized",
        "receipt_compression_authorized",
        "raw_receipt_hash_used_as_truth_surface",
        "case_id_or_cycle_n_primary_identity_patch_used",
        "rowid_identity_patch_used",
        "audit_pointer_in_signature_payload",
        "debug_payload_in_signature_payload",
    ]:
        if auth.get(key) is not False:
            failures.append(f"v03_authority_or_mutation_not_false:{key}:{auth.get(key)}")

    if v02_scale.get("probe_id") != EXPECTED_V02_SCALE_PROBE_ID:
        failures.append(f"v02_scale_probe_wrong:{v02_scale.get('probe_id')}")
    if v02_scale.get("terminal_decision") != "FAIL_SCALE_FALSE_MERGE":
        failures.append(f"v02_scale_terminal_wrong:{v02_scale.get('terminal_decision')}")

    if prior_diag.get("diagnostic_id") != EXPECTED_DIAGNOSTIC_ID:
        failures.append(f"prior_diag_wrong:{prior_diag.get('diagnostic_id')}")
    if prior_diag.get("classification", {}).get("primary_class") != "REPEATED_TRANSITION_SIGNATURE_COLLAPSES_DISTINCT_OCCURRENCES":
        failures.append(f"prior_diag_class_wrong:{prior_diag.get('classification', {}).get('primary_class')}")

    return failures


def rows_by_band(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        out[row.get("source_band_id") or row.get("band_id") or ""].append(row)
    return dict(out)


def v02_rows_by_scale_row_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out = {}
    for row in rows:
        rid = row.get("scale_band_row_id")
        if rid:
            out[rid] = row
    return out


def collision_groups(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_sig: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_sig[row.get("candidate_delta_signature")].append(row)

    groups = []
    for sig, records in by_sig.items():
        full_keys = sorted({r.get("full_occurrence_key") for r in records})
        if len(full_keys) <= 1:
            continue
        groups.append({
            "candidate_delta_signature": sig,
            "records": records,
            "distinct_full_occurrence_keys": len(full_keys),
            "full_occurrence_keys": full_keys,
        })
    groups.sort(key=lambda g: (-g["distinct_full_occurrence_keys"], str(g["candidate_delta_signature"])))
    return groups


def extract_v02_compact_delta_debug(v03_row: dict[str, Any], v02_by_row_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    source_id = ((v03_row.get("debug_sidecar") or {}).get("source_scale_band_row_id"))
    v02 = v02_by_row_id.get(source_id or "")
    if not v02:
        return {}
    return ((v02.get("debug_sidecar") or {}).get("compact_delta_debug") or {})


def raw_delta_signature_from_v02_debug(compact_debug: dict[str, Any]) -> dict[str, Any]:
    out = {}
    for col in ALLOWED_DELTA_BUCKET_COLUMNS:
        entry = compact_debug.get(col)
        if isinstance(entry, dict):
            out[col] = {
                "raw": entry.get("raw"),
                "bucket": entry.get("bucket"),
            }
        else:
            out[col] = {
                "raw": None,
                "bucket": None,
            }
    return out


def analyze_collision_group(group: dict[str, Any], v02_by_row_id: dict[str, dict[str, Any]]) -> dict[str, Any]:
    records = group["records"]
    payloads = [r.get("signature_payload") for r in records]
    payload_unique = {
        json.dumps(p, sort_keys=True, default=str)
        for p in payloads
    }

    bucket_payloads = [
        (r.get("signature_payload") or {}).get("transition_delta_buckets")
        for r in records
    ]
    bucket_payload_unique = {
        json.dumps(p, sort_keys=True, default=str)
        for p in bucket_payloads
    }

    v02_delta_debugs = [extract_v02_compact_delta_debug(r, v02_by_row_id) for r in records]
    v02_raw_delta_signatures = [raw_delta_signature_from_v02_debug(d) for d in v02_delta_debugs]

    raw_unique = {
        json.dumps(sig, sort_keys=True, default=str)
        for sig in v02_raw_delta_signatures
    }
    bucket_unique_from_raw = {
        json.dumps({k: v.get("bucket") for k, v in sig.items()}, sort_keys=True, default=str)
        for sig in v02_raw_delta_signatures
    }

    differing_raw_cols = []
    differing_bucket_cols = []
    for col in ALLOWED_DELTA_BUCKET_COLUMNS:
        raw_vals = {
            json.dumps(sig.get(col, {}).get("raw"), sort_keys=True, default=str)
            for sig in v02_raw_delta_signatures
        }
        bucket_vals = {
            json.dumps(sig.get(col, {}).get("bucket"), sort_keys=True, default=str)
            for sig in v02_raw_delta_signatures
        }
        if len(raw_vals) > 1:
            differing_raw_cols.append(col)
        if len(bucket_vals) > 1:
            differing_bucket_cols.append(col)

    audit_pointers = [r.get("audit_pointer") for r in records]
    source_scale_row_ids = [
        (r.get("debug_sidecar") or {}).get("source_scale_band_row_id")
        for r in records
    ]

    return {
        "candidate_delta_signature": group["candidate_delta_signature"],
        "distinct_full_occurrence_keys": group["distinct_full_occurrence_keys"],
        "full_occurrence_keys": group["full_occurrence_keys"][:20],
        "record_count": len(records),
        "v03_payload_unique_count": len(payload_unique),
        "v03_transition_delta_bucket_payload_unique_count": len(bucket_payload_unique),
        "v02_raw_delta_signature_unique_count": len(raw_unique),
        "v02_bucket_signature_unique_count": len(bucket_unique_from_raw),
        "differing_raw_delta_columns": differing_raw_cols,
        "differing_bucket_delta_columns": differing_bucket_cols,
        "source_scale_band_row_ids": source_scale_row_ids[:20],
        "audit_pointers": audit_pointers[:20],
        "records_preview": [
            {
                "source_run_id": r.get("source_run_id"),
                "full_occurrence_key": r.get("full_occurrence_key"),
                "candidate_delta_signature": r.get("candidate_delta_signature"),
                "signature_payload": r.get("signature_payload"),
                "source_scale_band_row_id": (r.get("debug_sidecar") or {}).get("source_scale_band_row_id"),
                "v02_compact_delta_debug": extract_v02_compact_delta_debug(r, v02_by_row_id),
            }
            for r in records[:10]
        ],
    }


def classify_failure(group_analyses: list[dict[str, Any]], v03: dict[str, Any]) -> dict[str, Any]:
    if not group_analyses:
        primary = "NO_V03_COLLISION_GROUPS_FOUND"
    else:
        v03_payload_constant = all(g["v03_payload_unique_count"] == 1 for g in group_analyses)
        v03_bucket_constant = all(g["v03_transition_delta_bucket_payload_unique_count"] == 1 for g in group_analyses)
        v02_raw_differs_somewhere = any(g["v02_raw_delta_signature_unique_count"] > 1 for g in group_analyses)
        v02_bucket_differs_somewhere = any(g["v02_bucket_signature_unique_count"] > 1 for g in group_analyses)

        if v03_payload_constant and v03_bucket_constant and v02_raw_differs_somewhere and not v02_bucket_differs_somewhere:
            primary = "BUCKETIZATION_COLLAPSED_RAW_DELTA_DIFFERENCE"
        elif v03_payload_constant and v03_bucket_constant and not v02_raw_differs_somewhere:
            primary = "TRANSITION_AND_DELTA_BUCKETS_RECUR_IDENTICALLY"
        elif v03_payload_constant and v03_bucket_constant and v02_bucket_differs_somewhere:
            primary = "V03_PAYLOAD_CONSTRUCTION_LOST_AVAILABLE_BUCKET_DIFFERENCE"
        else:
            primary = "MIXED_OR_UNRESOLVED_V03_FAILURE"

    burden_ratio = (v03.get("aggregate_measurements") or {}).get("worst_burden_ratio_projected")
    burden_class = "BURDEN_REGRESSION_CONFIRMED" if isinstance(burden_ratio, (int, float)) and burden_ratio > 1.0 else "BURDEN_STATUS_UNCLEAR"

    return {
        "primary_class": primary,
        "burden_class": burden_class,
        "interpretation": {
            "NO_V03_COLLISION_GROUPS_FOUND": "The v0.3 receipt says false merges persisted, but collision groups were not reconstructed from rows.",
            "BUCKETIZATION_COLLAPSED_RAW_DELTA_DIFFERENCE": "The prior debug difference likely lived in raw delta values, but v0.3 promoted only coarse buckets, collapsing the useful distinction.",
            "TRANSITION_AND_DELTA_BUCKETS_RECUR_IDENTICALLY": "The same transition and bucketized delta structure recurs across distinct occurrences; transition-local deltas are not enough.",
            "V03_PAYLOAD_CONSTRUCTION_LOST_AVAILABLE_BUCKET_DIFFERENCE": "The source rows expose bucket-level differences, but v0.3 payload construction failed to preserve them.",
            "MIXED_OR_UNRESOLVED_V03_FAILURE": "Multiple collision mechanisms appear; inspect collision gallery before designing the next candidate.",
        }.get(primary, "unclassified"),
    }


def build_diagnostic(source_probe_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    v03 = load_json(V03_RECEIPT_DIR / f"{source_probe_id}.json")
    v03_rows = load_jsonl(ROOT / v03["v03_rows_path"])

    v02_scale = load_json(V02_SCALE_RECEIPT_DIR / f"{EXPECTED_V02_SCALE_PROBE_ID}.json")
    v02_rows = load_jsonl(ROOT / v02_scale["scale_band_rows_path"])
    prior_diag = load_json(DIAG_DIR / f"{EXPECTED_DIAGNOSTIC_ID}.json")

    source_failures = verify_v03_source(v03, v02_scale, prior_diag)

    v03_by_band = rows_by_band(v03_rows)
    v02_by_row_id = v02_rows_by_scale_row_id(v02_rows)

    source_failed_band_ids = {
        b.get("band_id")
        for b in v02_scale.get("band_measurements", [])
        if not b.get("band_passed")
    }

    v03_failed_bands = [b for b in v03.get("band_measurements", []) if not b.get("band_passed")]
    v03_known_failed_bands = [b for b in v03.get("band_measurements", []) if b.get("was_known_failed_band")]

    group_analyses = []
    failed_band_gallery = []
    axis_counts = Counter()
    reason_counts = Counter()
    known_failed_axis_counts = Counter()

    for band in v03_failed_bands:
        band_id = band.get("band_id")
        rows = v03_by_band.get(band_id, [])
        groups = collision_groups(rows)
        analyses = [analyze_collision_group(g, v02_by_row_id) for g in groups]
        group_analyses.extend([
            dict(a, band_id=band_id, axis=band.get("axis"), axis_value=band.get("axis_value"), run_id=band.get("run_id"))
            for a in analyses
        ])
        axis_counts[str(band.get("axis"))] += 1
        reason_counts.update(band.get("failure_reasons", []))
        if band.get("was_known_failed_band"):
            known_failed_axis_counts[str(band.get("axis"))] += 1

        if len(failed_band_gallery) < 20:
            failed_band_gallery.append({
                "band_id": band_id,
                "axis": band.get("axis"),
                "axis_value": band.get("axis_value"),
                "run_id": band.get("run_id"),
                "was_known_failed_band": band.get("was_known_failed_band"),
                "false_merge_count": band.get("false_merge_count"),
                "burden_ratio_projected": band.get("burden_ratio_projected"),
                "failure_reasons": band.get("failure_reasons"),
                "collision_groups": analyses[:5],
            })

    classification = classify_failure(group_analyses, v03)

    raw_diff_col_counts = Counter()
    bucket_diff_col_counts = Counter()
    for g in group_analyses:
        raw_diff_col_counts.update(g.get("differing_raw_delta_columns", []))
        bucket_diff_col_counts.update(g.get("differing_bucket_delta_columns", []))

    summary = {
        "source_v03_probe_id": v03.get("probe_id"),
        "source_v03_receipt_id": v03.get("receipt_id"),
        "source_v03_policy_id": v03.get("source_policy_id"),
        "source_terminal_decision": v03.get("terminal_decision"),
        "source_v02_scale_probe_id": v02_scale.get("probe_id"),
        "prior_diagnostic_id": prior_diag.get("diagnostic_id"),
        "bands_total": v03.get("aggregate_measurements", {}).get("bands_total"),
        "bands_passed": v03.get("aggregate_measurements", {}).get("bands_passed"),
        "bands_failed": v03.get("aggregate_measurements", {}).get("bands_failed"),
        "known_failed_bands_total": v03.get("aggregate_measurements", {}).get("known_failed_bands_total"),
        "known_failed_bands_cleared": v03.get("aggregate_measurements", {}).get("known_failed_bands_cleared"),
        "known_failed_remaining_false_merge_bands": v03.get("aggregate_measurements", {}).get("known_failed_remaining_false_merge_bands"),
        "worst_false_merge_count": v03.get("aggregate_measurements", {}).get("worst_false_merge_count"),
        "worst_burden_ratio_projected": v03.get("aggregate_measurements", {}).get("worst_burden_ratio_projected"),
        "worst_distinguishability_retention_ratio": v03.get("aggregate_measurements", {}).get("worst_distinguishability_retention_ratio"),
        "failed_axis_counts": dict(axis_counts),
        "known_failed_axis_counts": dict(known_failed_axis_counts),
        "failed_reason_counts": dict(reason_counts),
        "collision_group_count_reconstructed": len(group_analyses),
        "raw_delta_differing_column_counts": dict(raw_diff_col_counts),
        "bucket_delta_differing_column_counts": dict(bucket_diff_col_counts),
    }

    if classification["primary_class"] == "BUCKETIZATION_COLLAPSED_RAW_DELTA_DIFFERENCE":
        recommended_next = "BUILD_RAW_DELTA_COMPACTNESS_DIAGNOSTIC_POLICY_V0"
        next_pressure = "Determine whether a smaller raw-delta encoding can preserve separability without exceeding burden."
    elif classification["primary_class"] == "TRANSITION_AND_DELTA_BUCKETS_RECUR_IDENTICALLY":
        recommended_next = "BUILD_RECURRENCE_AWARE_OCCURRENCE_SIGNATURE_POLICY_V0"
        next_pressure = "Need lawful recurrence/occurrence layer beyond transition-local structure."
    elif classification["primary_class"] == "V03_PAYLOAD_CONSTRUCTION_LOST_AVAILABLE_BUCKET_DIFFERENCE":
        recommended_next = "PATCH_V0_3_PAYLOAD_CONSTRUCTION_POLICY_V0"
        next_pressure = "Patch payload construction before new candidate design."
    else:
        recommended_next = NEXT_COMMAND_GOAL
        next_pressure = "Need a focused diagnostic or recurrence-aware policy before v0.4."

    decision = {
        "candidate_v0_3_rejected_for_scale_acceptance": True,
        "candidate_v0_3_rejected_for_burden": True,
        "authority_side_clean": True,
        "source_surface_clean": True,
        "identity_leak_absent": True,
        "delta_bucket_coverage_clean": True,
        "primary_blocker": "FALSE_MERGE_PERSISTS_AND_BURDEN_REGRESSED",
        "do_not_accept_candidate": True,
        "do_not_full_registry_scan": True,
        "do_not_change_runtime": True,
        "do_not_patch_by_adding_case_id_or_cycle_n_as_primary_identity": True,
        "do_not_patch_by_adding_rowid_or_receipt_hash": True,
        "recommended_next_command_goal": recommended_next,
        "next_design_pressure": next_pressure,
    }

    authority = {
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
        "authorizes_rowid_or_receipt_hash_patch": False,
    }

    terminal_type = "STOP" if source_failures else "ADVANCE"
    diagnostic = {
        "schema_version": "stable_delta_signature_candidate_v0_3_failure_diagnostic_v0",
        "diagnostic_name": DIAGNOSTIC_NAME,
        "diagnosis_status": "DIAGNOSED" if not source_failures else "SOURCE_VERIFICATION_FAILED",
        "source_v03_probe_id": EXPECTED_V03_PROBE_ID,
        "source_v03_receipt_id": EXPECTED_V03_RECEIPT_ID,
        "source_v03_policy_id": EXPECTED_V03_POLICY_ID,
        "source_v02_scale_probe_id": EXPECTED_V02_SCALE_PROBE_ID,
        "prior_diagnostic_id": EXPECTED_DIAGNOSTIC_ID,
        "summary": summary,
        "classification": classification,
        "decision": decision,
        "authority": authority,
        "failed_band_gallery": failed_band_gallery,
        "collision_group_gallery_top20": group_analyses[:20],
        "terminal": {
            "type": terminal_type,
            "next_command_goal": recommended_next if not source_failures else None,
            "stop_code": None if not source_failures else "STOP_V03_SOURCE_RECEIPT_INVALID",
        },
        "gate": "PASS" if not source_failures else "FAIL",
        "failures": source_failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    diagnostic_id = sha8({
        "diagnostic_name": DIAGNOSTIC_NAME,
        "source_v03_probe_id": EXPECTED_V03_PROBE_ID,
        "source_v03_receipt_id": EXPECTED_V03_RECEIPT_ID,
        "summary": summary,
        "classification": classification,
        "decision": decision,
    })
    diagnostic["diagnostic_id"] = diagnostic_id
    diagnostic["diagnostic_sig8"] = diagnostic_id

    receipt = {
        "schema_version": "stable_delta_signature_candidate_v0_3_failure_diagnostic_receipt_v0",
        "diagnostic_id": diagnostic_id,
        "diagnostic_sig8": diagnostic_id,
        "diagnostic_name": DIAGNOSTIC_NAME,
        "diagnosis_status": diagnostic["diagnosis_status"],
        "diagnostic_path": f"data/stable_delta_signature_candidate_v0_3_failure_diagnostics/{diagnostic_id}.json",
        "source_v03_probe_id": EXPECTED_V03_PROBE_ID,
        "source_v03_receipt_id": EXPECTED_V03_RECEIPT_ID,
        "source_v03_policy_id": EXPECTED_V03_POLICY_ID,
        "source_v02_scale_probe_id": EXPECTED_V02_SCALE_PROBE_ID,
        "prior_diagnostic_id": EXPECTED_DIAGNOSTIC_ID,
        "summary": summary,
        "classification": classification,
        "decision": decision,
        "authority": authority,
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
    parser.add_argument("--source-probe-id", default=EXPECTED_V03_PROBE_ID)
    args = parser.parse_args()

    diagnostic, receipt = build_diagnostic(args.source_probe_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"diagnostic_id={diagnostic['diagnostic_id']}")
    print(f"diagnostic_json_path=data/stable_delta_signature_candidate_v0_3_failure_diagnostics/{diagnostic['diagnostic_id']}.json")
    print(f"diagnostic_receipt_path=data/stable_delta_signature_candidate_v0_3_failure_diagnostic_receipts/{diagnostic['diagnostic_id']}.json")

    return 0 if diagnostic["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
