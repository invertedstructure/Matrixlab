#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

POLICY_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_policy_receipts"
DIAGNOSTIC_DIR = ROOT / "data" / "bounded_scale_false_merge_diagnostics"
SOURCE_SCALE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_receipts"

ROWS_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_rows"
RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_receipts"

EXPECTED_POLICY_ID = "78a6fbec"
EXPECTED_POLICY_RECEIPT_ID = "d8c99bbc"
EXPECTED_DIAGNOSTIC_ID = "62c8d96c"
EXPECTED_SOURCE_SCALE_PROBE_ID = "227e9426"
EXPECTED_SOURCE_SCALE_RECEIPT_ID = "0ae57255"

PROBE_KIND = "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_3_PROBE"
CANDIDATE_DESIGN_ID = "STABLE_DELTA_SIGNATURE_CANDIDATE_V0_3"
COMPRESSION_VERSION = "stable_delta_signature_v0.3_candidate"
MODE = "OUTER_OBSERVER_ONLY"

BASE_TRANSITION_FIELDS = ["cv", "state_hash_before", "move_id", "state_hash_after"]
REQUIRED_SIGNATURE_FIELDS = ["cv", "state_hash_before", "move_id", "state_hash_after", "transition_delta_buckets"]

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

FORBIDDEN_SIGNATURE_KEYS = {
    "full_occurrence_key",
    "raw_full_receipt_hash",
    "full_receipt_hash",
    "receipt_hash",
    "receipt_sig8",
    "receipt_rowid",
    "rowid",
    "audit_pointer",
    "debug_payload",
    "observer_notes",
    "created_at",
    "created_utc",
    "timestamp",
    "path",
    "receipt_path",
    "file_path",
    "case_id_as_primary_identity",
    "cycle_n_as_primary_identity",
    "case_id",
    "cycle_n",
    "depth_as_primary_identity",
}


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def canonical_blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def canonical_bytes(obj: Any) -> int:
    return len(canonical_blob(obj))


def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_blob(obj)).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"missing required jsonl: {path}")
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]


def verify_policy(policy: dict[str, Any], receipt: dict[str, Any], diagnostic: dict[str, Any], source_scale: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if receipt.get("receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{receipt.get('receipt_id')}")
    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{receipt.get('gate')}")
    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy.get('policy_status')}")
    if policy.get("terminal", {}).get("next_command_goal") != "IMPLEMENT_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_3_PROBE":
        failures.append(f"policy_next_goal_wrong:{policy.get('terminal', {}).get('next_command_goal')}")

    design = policy.get("candidate_design") or {}
    if design.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"candidate_design_id_wrong:{design.get('candidate_design_id')}")
    if design.get("v0_2_rejected_for_scale_acceptance") is not True:
        failures.append("v0_2_not_rejected_for_scale_acceptance")
    if design.get("base_transition_tuple_retained") != BASE_TRANSITION_FIELDS:
        failures.append(f"base_transition_tuple_wrong:{design.get('base_transition_tuple_retained')}")
    if design.get("signature_payload_required_fields") != REQUIRED_SIGNATURE_FIELDS:
        failures.append(f"signature_payload_required_fields_wrong:{design.get('signature_payload_required_fields')}")
    if design.get("truth_surface") != "full_occurrence_key_to_candidate_delta_signature":
        failures.append(f"truth_surface_wrong:{design.get('truth_surface')}")

    discriminator = design.get("new_lawful_discriminator") or {}
    if discriminator.get("name") != "transition_delta_buckets":
        failures.append(f"discriminator_name_wrong:{discriminator.get('name')}")
    if discriminator.get("kind") != "LAWFUL_TRANSITION_DELTA_DISCRIMINATOR":
        failures.append(f"discriminator_kind_wrong:{discriminator.get('kind')}")
    if discriminator.get("source") != "existing registry receipt delta columns only":
        failures.append(f"discriminator_source_wrong:{discriminator.get('source')}")
    if discriminator.get("allowed_source_columns") != ALLOWED_DELTA_BUCKET_COLUMNS:
        failures.append(f"allowed_delta_columns_wrong:{discriminator.get('allowed_source_columns')}")
    for key in [
        "must_be_measured_as_signature_payload",
        "must_be_measured_separately_from_debug_sidecar",
        "must_report_delta_bucket_coverage",
        "must_report_delta_bucket_discriminative_power",
    ]:
        if discriminator.get(key) is not True:
            failures.append(f"discriminator_required_flag_missing:{key}:{discriminator.get(key)}")

    for forbidden in FORBIDDEN_SIGNATURE_KEYS:
        if forbidden not in set(design.get("signature_payload_forbidden_fields") or []):
            failures.append(f"forbidden_signature_field_missing:{forbidden}")

    surface = design.get("bounded_evaluation_surface") or {}
    if surface.get("source_scale_probe_id") != EXPECTED_SOURCE_SCALE_PROBE_ID:
        failures.append(f"surface_source_probe_wrong:{surface.get('source_scale_probe_id')}")
    if surface.get("source_scale_receipt_id") != EXPECTED_SOURCE_SCALE_RECEIPT_ID:
        failures.append(f"surface_source_receipt_wrong:{surface.get('source_scale_receipt_id')}")
    if surface.get("bounded_default_required") is not True:
        failures.append("bounded_default_required_not_true")
    if surface.get("full_registry_forbidden") is not True:
        failures.append("full_registry_forbidden_not_true")
    if surface.get("compatible_run_count") != 10:
        failures.append(f"surface_compatible_run_count_not_10:{surface.get('compatible_run_count')}")
    if surface.get("failed_bands_to_retest") != 10:
        failures.append(f"failed_bands_to_retest_not_10:{surface.get('failed_bands_to_retest')}")

    auth = policy.get("authority") or {}
    if auth.get("observer_only") is not True:
        failures.append("observer_only_not_true")
    if auth.get("authorizes_next_candidate_probe_implementation") is not True:
        failures.append("does_not_authorize_next_probe")
    if auth.get("authorizes_bounded_v0_3_probe_execution") is not True:
        failures.append("does_not_authorize_bounded_probe_execution")
    for key in [
        "authorizes_candidate_acceptance",
        "authorizes_scale_mode",
        "authorizes_full_registry_scan",
        "authorizes_runtime_receipt_emission_change",
        "authorizes_registry_write",
        "authorizes_receipt_replacement",
        "authorizes_receipt_deletion",
        "authorizes_receipt_compression",
        "authorizes_raw_receipt_hash_truth_surface",
        "authorizes_case_id_or_cycle_n_primary_identity_patch",
        "authorizes_rowid_identity_patch",
        "authorizes_audit_pointer_in_signature_payload",
        "authorizes_debug_payload_in_signature_payload",
    ]:
        if auth.get(key) is not False:
            failures.append(f"illegal_policy_authority:{key}:{auth.get(key)}")

    constraints = policy.get("implementation_constraints") or {}
    if constraints.get("must_touch_only_files") != ["scripts/stable_delta_signature_candidate_v0_3_probe.py"]:
        failures.append(f"touch_scope_wrong:{constraints.get('must_touch_only_files')}")
    for key in [
        "must_not_full_registry_scan",
        "must_reuse_bounded_source_probe_surface",
        "must_not_accept_candidate",
        "must_not_authorize_scale_mode",
        "must_not_change_registry_sqlite",
        "must_not_change_runtime_receipt_emission",
    ]:
        if constraints.get(key) is not True:
            failures.append(f"constraint_missing:{key}:{constraints.get(key)}")

    if diagnostic.get("diagnostic_id") != EXPECTED_DIAGNOSTIC_ID:
        failures.append(f"diagnostic_id_wrong:{diagnostic.get('diagnostic_id')}")
    if diagnostic.get("gate") != "PASS":
        failures.append(f"diagnostic_gate_not_PASS:{diagnostic.get('gate')}")
    if diagnostic.get("classification", {}).get("primary_class") != "REPEATED_TRANSITION_SIGNATURE_COLLAPSES_DISTINCT_OCCURRENCES":
        failures.append(f"diagnostic_classification_wrong:{diagnostic.get('classification', {}).get('primary_class')}")
    if diagnostic.get("decision", {}).get("recommended_next_command_goal") != "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_3_POLICY":
        failures.append(f"diagnostic_next_goal_wrong:{diagnostic.get('decision', {}).get('recommended_next_command_goal')}")
    if diagnostic.get("decision", {}).get("do_not_patch_by_adding_case_id_or_cycle_n_as_primary_identity") is not True:
        failures.append("diagnostic_allows_case_cycle_identity_patch")

    if source_scale.get("probe_id") != EXPECTED_SOURCE_SCALE_PROBE_ID:
        failures.append(f"source_scale_probe_id_wrong:{source_scale.get('probe_id')}")
    if source_scale.get("receipt_id") != EXPECTED_SOURCE_SCALE_RECEIPT_ID:
        failures.append(f"source_scale_receipt_id_wrong:{source_scale.get('receipt_id')}")
    if source_scale.get("terminal_decision") != "FAIL_SCALE_FALSE_MERGE":
        failures.append(f"source_scale_terminal_not_false_merge:{source_scale.get('terminal_decision')}")
    if source_scale.get("scale_coverage", {}).get("bounded_default_used") is not True:
        failures.append("source_scale_not_bounded_default")
    if source_scale.get("scale_coverage", {}).get("full_registry_used") is not False:
        failures.append("source_scale_used_full_registry")
    if source_scale.get("pass_gates", {}).get("no_false_merge_all_bands") is not False:
        failures.append("source_scale_false_merge_gate_not_false")

    return failures


def rows_by_band(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        out[row.get("band_id", "")].append(row)
    return dict(out)


def transition_delta_buckets(row: dict[str, Any]) -> dict[str, dict[str, Any]]:
    compact_delta_debug = ((row.get("debug_sidecar") or {}).get("compact_delta_debug") or {})
    buckets: dict[str, dict[str, Any]] = {}

    for col in ALLOWED_DELTA_BUCKET_COLUMNS:
        entry = compact_delta_debug.get(col)
        if isinstance(entry, dict) and entry.get("bucket") is not None:
            buckets[col] = {
                "status": "present",
                "bucket": entry.get("bucket"),
            }
        else:
            buckets[col] = {
                "status": "absent",
                "bucket": None,
            }
    return buckets


def candidate_signature_payload_v03(row: dict[str, Any]) -> dict[str, Any]:
    old_payload = row.get("signature_payload") or {}
    return {
        "cv": "v0.3",
        "state_hash_before": old_payload.get("state_hash_before"),
        "move_id": old_payload.get("move_id"),
        "state_hash_after": old_payload.get("state_hash_after"),
        "transition_delta_buckets": transition_delta_buckets(row),
    }


def signature_has_identity_leak(sig_payload: dict[str, Any]) -> bool:
    text = json.dumps(sig_payload, sort_keys=True, default=str).lower()
    return any(key.lower() in text for key in FORBIDDEN_SIGNATURE_KEYS)


def bucket_coverage_for_payload(sig_payload: dict[str, Any]) -> dict[str, Any]:
    buckets = sig_payload.get("transition_delta_buckets") or {}
    present = [k for k, v in buckets.items() if isinstance(v, dict) and v.get("status") == "present"]
    absent = [k for k, v in buckets.items() if isinstance(v, dict) and v.get("status") == "absent"]
    malformed = [
        k for k, v in buckets.items()
        if k not in ALLOWED_DELTA_BUCKET_COLUMNS or not isinstance(v, dict) or v.get("status") not in {"present", "absent"}
    ]
    return {
        "allowed_column_count": len(ALLOWED_DELTA_BUCKET_COLUMNS),
        "present_count": len(present),
        "absent_count": len(absent),
        "malformed_count": len(malformed),
        "present_columns": sorted(present),
        "absent_columns": sorted(absent),
        "malformed_columns": sorted(malformed),
    }


def projected_scale_row_v03(signature_id: str, candidate_delta_signature: str, source_row: dict[str, Any]) -> dict[str, Any]:
    audit_pointer = source_row.get("audit_pointer") or {}
    return {
        "signature_id": signature_id,
        "source_run_id": source_row.get("source_run_id"),
        "candidate_delta_signature": candidate_delta_signature,
        "compression_version": COMPRESSION_VERSION,
        "audit_pointer": audit_pointer,
    }


def measure_band_v03(source_band: dict[str, Any], source_rows: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    sig_to_full: dict[str, set[str]] = defaultdict(set)
    full_to_sig: dict[str, set[str]] = defaultdict(set)

    full_receipt_bytes = int(source_band.get("full_receipt_bytes") or 0)
    signature_payload_bytes = 0
    projected_scale_row_bytes = 0
    audit_sidecar_bytes = 0
    debug_sidecar_bytes = 0

    identity_leak_count = 0
    source_surface_regression_count = 0
    audit_recoverability_failures = 0
    delta_bucket_coverage_failures = 0

    present_counter: Counter[str] = Counter()
    absent_counter: Counter[str] = Counter()
    bucket_value_counter: Counter[str] = Counter()

    out_rows: list[dict[str, Any]] = []

    for source_row in source_rows:
        full_key = source_row.get("full_occurrence_key")
        old_payload = source_row.get("signature_payload") or {}
        audit_pointer = source_row.get("audit_pointer") or {}

        if not full_key:
            source_surface_regression_count += 1
            continue
        if not all(old_payload.get(k) not in (None, "") for k in ["state_hash_before", "move_id", "state_hash_after"]):
            source_surface_regression_count += 1
            continue
        if not audit_pointer:
            audit_recoverability_failures += 1

        sig_payload = candidate_signature_payload_v03(source_row)
        coverage = bucket_coverage_for_payload(sig_payload)

        if coverage["malformed_count"] > 0:
            delta_bucket_coverage_failures += 1
        if coverage["present_count"] == 0:
            delta_bucket_coverage_failures += 1

        for col in coverage["present_columns"]:
            present_counter[col] += 1
            bucket_value = sig_payload["transition_delta_buckets"][col]["bucket"]
            bucket_value_counter[f"{col}:{bucket_value}"] += 1
        for col in coverage["absent_columns"]:
            absent_counter[col] += 1

        if signature_has_identity_leak(sig_payload):
            identity_leak_count += 1

        candidate_delta_signature = sha8(sig_payload)
        signature_id = sha8({
            "compression_version": COMPRESSION_VERSION,
            "candidate_delta_signature": candidate_delta_signature,
            "source_run_id": source_row.get("source_run_id"),
            "audit_pointer": audit_pointer,
        })
        projected = projected_scale_row_v03(signature_id, candidate_delta_signature, source_row)

        sig_bytes = canonical_bytes(sig_payload)
        proj_bytes = canonical_bytes(projected)
        audit_bytes = canonical_bytes(audit_pointer)
        debug_bytes = canonical_bytes({
            "bucket_coverage": coverage,
            "source_v02_candidate_delta_signature": source_row.get("candidate_delta_signature"),
            "source_axis": source_row.get("axis"),
            "source_axis_value": source_row.get("axis_value"),
        })

        signature_payload_bytes += sig_bytes
        projected_scale_row_bytes += proj_bytes
        audit_sidecar_bytes += audit_bytes
        debug_sidecar_bytes += debug_bytes

        sig_to_full[candidate_delta_signature].add(full_key)
        full_to_sig[full_key].add(candidate_delta_signature)

        out_rows.append({
            "v03_row_id": sha8({
                "band_id": source_band.get("band_id"),
                "source_run_id": source_row.get("source_run_id"),
                "full_occurrence_key": full_key,
                "candidate_delta_signature": candidate_delta_signature,
            }),
            "source_band_id": source_band.get("band_id"),
            "axis": source_band.get("axis"),
            "axis_value": source_band.get("axis_value"),
            "source_run_id": source_row.get("source_run_id"),
            "full_occurrence_key": full_key,
            "candidate_delta_signature": candidate_delta_signature,
            "signature_payload": sig_payload,
            "signature_payload_bytes": sig_bytes,
            "transition_delta_bucket_coverage": coverage,
            "audit_pointer": audit_pointer,
            "audit_sidecar_bytes": audit_bytes,
            "debug_sidecar": {
                "source_v02_candidate_delta_signature": source_row.get("candidate_delta_signature"),
                "source_scale_band_row_id": source_row.get("scale_band_row_id"),
                "bucket_coverage": coverage,
            },
            "debug_sidecar_bytes": debug_bytes,
            "projected_scale_row_bytes": proj_bytes,
            "truth_surface": {
                "primary_comparison": "full_occurrence_key_to_candidate_delta_signature",
                "raw_full_receipt_hash_used_as_truth_surface": False,
                "full_receipt_hash_compared_to_delta_signature": False,
            },
            "authority_guards": {
                "observer_only": True,
                "runtime_receipt_emission_changed": False,
                "registry_sqlite_changed": False,
                "scale_mode_authorized": False,
                "candidate_acceptance_authorized": False,
                "full_registry_scan_used": False,
            },
        })

    collision_groups = {sig: keys for sig, keys in sig_to_full.items() if len(keys) > 1}
    false_split_groups = {key: sigs for key, sigs in full_to_sig.items() if len(sigs) > 1}

    distinct_full = len(full_to_sig)
    distinct_sig = len(sig_to_full)
    burden_basis_bytes = projected_scale_row_bytes + signature_payload_bytes
    burden_ratio_projected = burden_basis_bytes / full_receipt_bytes if full_receipt_bytes else 0.0
    burden_ratio_signature_payload = signature_payload_bytes / full_receipt_bytes if full_receipt_bytes else 0.0
    retention = distinct_sig / distinct_full if distinct_full else 0.0

    passed = (
        source_surface_regression_count == 0
        and identity_leak_count == 0
        and audit_recoverability_failures == 0
        and delta_bucket_coverage_failures == 0
        and len(collision_groups) == 0
        and len(false_split_groups) == 0
        and burden_ratio_projected < 1.0
        and full_receipt_bytes > 0
    )

    measurement = {
        "band_id": source_band.get("band_id"),
        "run_id": source_band.get("run_id"),
        "axis": source_band.get("axis"),
        "axis_value": source_band.get("axis_value"),
        "occurrences_total": len(source_rows),
        "distinct_full_occurrence_keys": distinct_full,
        "distinct_candidate_signatures": distinct_sig,
        "collision_count": len(collision_groups),
        "false_merge_count": len(collision_groups),
        "false_split_count": len(false_split_groups),
        "distinguishability_retention_ratio": retention,
        "full_receipt_bytes": full_receipt_bytes,
        "signature_payload_bytes": signature_payload_bytes,
        "projected_scale_row_bytes": projected_scale_row_bytes,
        "projected_plus_signature_payload_bytes": burden_basis_bytes,
        "audit_sidecar_bytes": audit_sidecar_bytes,
        "debug_sidecar_bytes": debug_sidecar_bytes,
        "burden_ratio_projected": burden_ratio_projected,
        "burden_ratio_signature_payload": burden_ratio_signature_payload,
        "source_surface_regression_count": source_surface_regression_count,
        "identity_leak_count": identity_leak_count,
        "audit_recoverability_failures": audit_recoverability_failures,
        "delta_bucket_coverage_failures": delta_bucket_coverage_failures,
        "transition_delta_bucket_present_counts": dict(sorted(present_counter.items())),
        "transition_delta_bucket_absent_counts": dict(sorted(absent_counter.items())),
        "transition_delta_bucket_value_counts_top20": dict(bucket_value_counter.most_common(20)),
        "observer_overhead_ms": 0,
        "band_passed": passed,
        "failure_reasons": [
            reason
            for reason, condition in [
                ("source_surface_regression", source_surface_regression_count > 0),
                ("identity_leak", identity_leak_count > 0),
                ("audit_recoverability", audit_recoverability_failures > 0),
                ("delta_bucket_coverage", delta_bucket_coverage_failures > 0),
                ("false_merge", len(collision_groups) > 0),
                ("false_split", len(false_split_groups) > 0),
                ("burden_regression", not (burden_ratio_projected < 1.0 and full_receipt_bytes > 0)),
            ]
            if condition
        ],
    }
    return measurement, out_rows


def build_probe(policy_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    start = time.perf_counter()
    ROWS_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")
    diagnostic = load_json(DIAGNOSTIC_DIR / f"{EXPECTED_DIAGNOSTIC_ID}.json")
    source_scale = load_json(SOURCE_SCALE_RECEIPT_DIR / f"{EXPECTED_SOURCE_SCALE_PROBE_ID}.json")

    failures = verify_policy(policy, policy_receipt, diagnostic, source_scale)

    source_rows_path = ROOT / source_scale.get("scale_band_rows_path", "")
    source_rows = load_jsonl(source_rows_path)
    source_rows_by_band = rows_by_band(source_rows)

    source_bands = source_scale.get("band_measurements") or []
    source_failed_band_ids = {
        b.get("band_id")
        for b in source_bands
        if not b.get("band_passed")
    }

    band_measurements: list[dict[str, Any]] = []
    v03_rows: list[dict[str, Any]] = []

    for source_band in source_bands:
        band_start = time.perf_counter()
        rows = source_rows_by_band.get(source_band.get("band_id"), [])
        measurement, out_rows = measure_band_v03(source_band, rows)
        measurement["observer_overhead_ms"] = int(round((time.perf_counter() - band_start) * 1000))
        measurement["source_v02_band_passed"] = bool(source_band.get("band_passed"))
        measurement["source_v02_false_merge_count"] = source_band.get("false_merge_count")
        measurement["was_known_failed_band"] = source_band.get("band_id") in source_failed_band_ids
        band_measurements.append(measurement)
        v03_rows.extend(out_rows)

    known_failed_band_measurements = [b for b in band_measurements if b["was_known_failed_band"]]
    all_bands_passed = all(b["band_passed"] for b in band_measurements)
    known_failed_cleared = all(b["false_merge_count"] == 0 and b["band_passed"] for b in known_failed_band_measurements)

    bands_total = len(band_measurements)
    bands_passed = sum(1 for b in band_measurements if b["band_passed"])
    bands_failed = bands_total - bands_passed

    worst_false_merge_count = max((b["false_merge_count"] for b in band_measurements), default=0)
    worst_collision_count = max((b["collision_count"] for b in band_measurements), default=0)
    worst_retention = min((b["distinguishability_retention_ratio"] for b in band_measurements), default=0.0)
    worst_burden_ratio = max((b["burden_ratio_projected"] for b in band_measurements), default=0.0)
    worst_identity_leak = max((b["identity_leak_count"] for b in band_measurements), default=0)
    worst_source_surface_regression = max((b["source_surface_regression_count"] for b in band_measurements), default=0)
    worst_audit_failures = max((b["audit_recoverability_failures"] for b in band_measurements), default=0)
    worst_delta_bucket_coverage_failures = max((b["delta_bucket_coverage_failures"] for b in band_measurements), default=0)

    known_failed_remaining_false_merges = sum(1 for b in known_failed_band_measurements if b["false_merge_count"] > 0)
    known_failed_remaining_failed_bands = sum(1 for b in known_failed_band_measurements if not b["band_passed"])

    global_present_counter: Counter[str] = Counter()
    global_absent_counter: Counter[str] = Counter()
    for b in band_measurements:
        global_present_counter.update(b.get("transition_delta_bucket_present_counts", {}))
        global_absent_counter.update(b.get("transition_delta_bucket_absent_counts", {}))

    pass_gates = {
        "authority_containment": True,
        "bounded_selection_reused": (
            source_scale.get("scale_coverage", {}).get("bounded_default_used") is True
            and source_scale.get("scale_coverage", {}).get("full_registry_used") is False
        ),
        "source_surface_regression": worst_source_surface_regression == 0,
        "delta_bucket_coverage": worst_delta_bucket_coverage_failures == 0,
        "truth_surface": True,
        "no_identity_leak": worst_identity_leak == 0,
        "audit_recoverability": worst_audit_failures == 0,
        "known_failed_bands_cleared": known_failed_cleared,
        "no_false_merge_all_bands": worst_false_merge_count == 0,
        "burden_reduction_all_bands": worst_burden_ratio < 1.0 and bands_total > 0,
        "candidate_not_accepted": True,
        "scale_mode_not_authorized": True,
    }

    if not pass_gates["authority_containment"]:
        terminal_decision = "FAIL_V0_3_OBSERVER_INTERFERENCE"
        next_command_goal = None
    elif not pass_gates["bounded_selection_reused"]:
        terminal_decision = "FAIL_V0_3_OBSERVER_INTERFERENCE"
        next_command_goal = None
    elif not pass_gates["source_surface_regression"]:
        terminal_decision = "FAIL_V0_3_SOURCE_SURFACE_REGRESSION"
        next_command_goal = None
    elif not pass_gates["delta_bucket_coverage"]:
        terminal_decision = "FAIL_V0_3_SOURCE_SURFACE_REGRESSION"
        next_command_goal = None
    elif not pass_gates["no_identity_leak"]:
        terminal_decision = "FAIL_V0_3_IDENTITY_LEAK"
        next_command_goal = None
    elif not pass_gates["audit_recoverability"]:
        terminal_decision = "FAIL_V0_3_OBSERVER_INTERFERENCE"
        next_command_goal = None
    elif not pass_gates["known_failed_bands_cleared"]:
        terminal_decision = "FAIL_V0_3_FALSE_MERGE_PERSISTS"
        next_command_goal = None
    elif not pass_gates["no_false_merge_all_bands"]:
        terminal_decision = "FAIL_V0_3_FALSE_MERGE_PERSISTS"
        next_command_goal = None
    elif not pass_gates["burden_reduction_all_bands"]:
        terminal_decision = "FAIL_V0_3_BURDEN_REGRESSION"
        next_command_goal = None
    else:
        terminal_decision = "PASS_V0_3_BOUNDED_FALSE_MERGE_REPAIR"
        next_command_goal = "BUILD_STABLE_DELTA_SIGNATURE_CANDIDATE_V0_3_BOUNDED_REVIEW_POLICY"

    elapsed_ms = int(round((time.perf_counter() - start) * 1000))

    aggregate = {
        "bands_total": bands_total,
        "bands_passed": bands_passed,
        "bands_failed": bands_failed,
        "known_failed_bands_total": len(known_failed_band_measurements),
        "known_failed_bands_cleared": known_failed_cleared,
        "known_failed_remaining_false_merge_bands": known_failed_remaining_false_merges,
        "known_failed_remaining_failed_bands": known_failed_remaining_failed_bands,
        "worst_false_merge_count": worst_false_merge_count,
        "worst_collision_count": worst_collision_count,
        "worst_distinguishability_retention_ratio": worst_retention,
        "worst_burden_ratio_projected": worst_burden_ratio,
        "worst_identity_leak_count": worst_identity_leak,
        "worst_source_surface_regression_count": worst_source_surface_regression,
        "worst_audit_recoverability_failures": worst_audit_failures,
        "worst_delta_bucket_coverage_failures": worst_delta_bucket_coverage_failures,
        "transition_delta_bucket_present_counts": dict(sorted(global_present_counter.items())),
        "transition_delta_bucket_absent_counts": dict(sorted(global_absent_counter.items())),
        "actual_observer_overhead_ms": elapsed_ms,
    }

    authority_guards = {
        "observer_only": True,
        "registry_sqlite_changed": False,
        "runtime_receipt_emission_changed": False,
        "full_registry_scan_used": False,
        "scale_mode_authorized": False,
        "candidate_acceptance_authorized": False,
        "registry_write_authorized": False,
        "receipt_replacement_authorized": False,
        "receipt_deletion_authorized": False,
        "receipt_compression_authorized": False,
        "raw_receipt_hash_used_as_truth_surface": False,
        "case_id_or_cycle_n_primary_identity_patch_used": False,
        "rowid_identity_patch_used": False,
        "audit_pointer_in_signature_payload": False,
        "debug_payload_in_signature_payload": False,
    }

    probe = {
        "schema_version": "stable_delta_signature_candidate_v0_3_probe_receipt_v0",
        "probe_kind": PROBE_KIND,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "compression_version": COMPRESSION_VERSION,
        "mode": MODE,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_diagnostic_id": EXPECTED_DIAGNOSTIC_ID,
        "source_scale_probe_id": EXPECTED_SOURCE_SCALE_PROBE_ID,
        "source_scale_receipt_id": EXPECTED_SOURCE_SCALE_RECEIPT_ID,
        "bounded_source_surface": {
            "reused_source_scale_probe_rows_path": source_scale.get("scale_band_rows_path"),
            "bounded_default_used": source_scale.get("scale_coverage", {}).get("bounded_default_used"),
            "full_registry_used": source_scale.get("scale_coverage", {}).get("full_registry_used"),
            "compatible_run_count": source_scale.get("scale_coverage", {}).get("compatible_run_count"),
            "bands_total": source_scale.get("scale_coverage", {}).get("bands_total"),
            "source_failed_bands_total": len(source_failed_band_ids),
        },
        "signature_contract": {
            "candidate_signature_payload_required_fields": REQUIRED_SIGNATURE_FIELDS,
            "candidate_signature_payload_forbidden_fields": sorted(FORBIDDEN_SIGNATURE_KEYS),
            "transition_delta_bucket_columns": ALLOWED_DELTA_BUCKET_COLUMNS,
            "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
            "case_id_in_signature_payload": False,
            "cycle_n_in_signature_payload": False,
            "rowid_in_signature_payload": False,
            "audit_pointer_in_signature_payload": False,
            "debug_payload_in_signature_payload": False,
            "raw_receipt_hash_truth_surface": False,
        },
        "aggregate_measurements": aggregate,
        "band_measurements": band_measurements,
        "failed_band_gallery": [b for b in band_measurements if not b["band_passed"]][:20],
        "known_failed_band_retest_gallery": known_failed_band_measurements[:20],
        "pass_gates": pass_gates,
        "authority_guards": authority_guards,
        "negative_claims": {
            "does_not_accept_candidate": True,
            "does_not_authorize_scale_mode": True,
            "does_not_full_registry_scan": True,
            "does_not_change_runtime_receipt_emission": True,
            "does_not_write_registry_sqlite": True,
            "does_not_use_raw_receipt_hash_as_truth_surface": True,
            "does_not_use_case_id_or_cycle_n_as_primary_identity": True,
            "does_not_use_rowid_as_signature_identity": True,
            "does_not_include_audit_pointer_in_signature_payload": True,
            "does_not_include_debug_payload_in_signature_payload": True,
            "does_not_include_full_occurrence_key_in_signature_payload": True,
        },
        "terminal_decision": terminal_decision,
        "terminal": {
            "type": "ADVANCE" if next_command_goal else "STOP",
            "next_command_goal": next_command_goal,
            "stop_code": None if next_command_goal else terminal_decision,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    probe_id = sha8({
        "probe_kind": PROBE_KIND,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_diagnostic_id": EXPECTED_DIAGNOSTIC_ID,
        "source_scale_probe_id": EXPECTED_SOURCE_SCALE_PROBE_ID,
        "signature_contract": probe["signature_contract"],
        "aggregate_measurements": aggregate,
        "terminal_decision": terminal_decision,
    })
    probe["probe_id"] = probe_id
    probe["probe_sig8"] = probe_id

    rows_path = ROWS_DIR / f"{probe_id}.jsonl"
    with rows_path.open("w") as f:
        for row in v03_rows:
            f.write(json.dumps(row, sort_keys=True, default=str) + "\n")
    probe["v03_rows_path"] = f"data/stable_delta_signature_candidate_v0_3_rows/{probe_id}.jsonl"

    receipt_id = sha8(probe)
    receipt = dict(probe)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    receipt_path = RECEIPT_DIR / f"{probe_id}.json"
    receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return probe, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-id", default=EXPECTED_POLICY_ID)
    args = parser.parse_args()

    probe, receipt = build_probe(args.policy_id)

    print(json.dumps({
        "probe_id": receipt["probe_id"],
        "receipt_id": receipt["receipt_id"],
        "gate": receipt["gate"],
        "mode": receipt["mode"],
        "candidate_design_id": receipt["candidate_design_id"],
        "compression_version": receipt["compression_version"],
        "source_policy_id": receipt["source_policy_id"],
        "source_diagnostic_id": receipt["source_diagnostic_id"],
        "source_scale_probe_id": receipt["source_scale_probe_id"],
        "bounded_source_surface": receipt["bounded_source_surface"],
        "signature_contract": receipt["signature_contract"],
        "aggregate_measurements": receipt["aggregate_measurements"],
        "pass_gates": receipt["pass_gates"],
        "authority_guards": receipt["authority_guards"],
        "negative_claims": receipt["negative_claims"],
        "terminal_decision": receipt["terminal_decision"],
        "terminal": receipt["terminal"],
        "failures": receipt["failures"],
        "warnings": receipt["warnings"],
    }, indent=2, sort_keys=True))
    print(f"probe_id={receipt['probe_id']}")
    print(f"v03_rows_path={receipt['v03_rows_path']}")
    print(f"v03_receipt_path=data/stable_delta_signature_candidate_v0_3_receipts/{receipt['probe_id']}.json")

    return 0 if receipt["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
