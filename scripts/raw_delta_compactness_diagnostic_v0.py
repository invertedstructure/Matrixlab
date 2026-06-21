#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

POLICY_DIR = ROOT / "data" / "raw_delta_compactness_diagnostic_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_compactness_diagnostic_policy_receipts"
V03_FAILURE_DIAG_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_failure_diagnostics"
V03_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_3_receipts"
V02_SCALE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_compactness_diagnostics"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_compactness_diagnostic_receipts"
ROWS_DIR = ROOT / "data" / "raw_delta_compactness_rows"

EXPECTED_POLICY_ID = "445bdd02"
EXPECTED_POLICY_RECEIPT_ID = "25a019a1"
EXPECTED_V03_FAILURE_DIAG_ID = "d0132dd4"
EXPECTED_V03_PROBE_ID = "bd1beabe"
EXPECTED_V02_SCALE_PROBE_ID = "227e9426"

DIAGNOSTIC_NAME = "RAW_DELTA_COMPACTNESS_DIAGNOSTIC_V0"
MODE = "OUTER_OBSERVER_ONLY"

ENCODING_ORDER = [
    "raw_decimal_string_exact",
    "raw_decimal_sig6",
    "raw_decimal_sig9",
    "raw_decimal_sig12",
    "raw_delta_microhash_32",
]
TARGET_RAW_DELTA_FIELD = "compression_ratio"

FORBIDDEN_PAYLOAD_KEYS = {
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
    "case_id",
    "cycle_n",
    "case_id_as_primary_identity",
    "cycle_n_as_primary_identity",
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


def verify_sources(policy: dict[str, Any], policy_receipt: dict[str, Any], v03_diag: dict[str, Any], v03_probe: dict[str, Any], v02_scale: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy_receipt.get("receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy_receipt.get('receipt_id')}")
    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if policy_receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{policy_receipt.get('gate')}")
    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy.get('policy_status')}")
    if policy.get("terminal", {}).get("next_command_goal") != "IMPLEMENT_RAW_DELTA_COMPACTNESS_DIAGNOSTIC_V0":
        failures.append(f"policy_next_goal_wrong:{policy.get('terminal', {}).get('next_command_goal')}")

    contract = policy.get("diagnostic_contract") or {}
    if contract.get("diagnostic_name") != DIAGNOSTIC_NAME:
        failures.append(f"diagnostic_name_wrong:{contract.get('diagnostic_name')}")
    if contract.get("target_raw_delta_fields") != [TARGET_RAW_DELTA_FIELD]:
        failures.append(f"target_raw_delta_fields_wrong:{contract.get('target_raw_delta_fields')}")
    if [e.get("encoding_id") for e in contract.get("encoding_candidates_to_measure", [])] != ENCODING_ORDER:
        failures.append("encoding_candidate_order_wrong")
    if contract.get("truth_surface") != "full_occurrence_key_to_candidate_delta_signature":
        failures.append(f"truth_surface_wrong:{contract.get('truth_surface')}")
    for key in [
        "must_inspect_collision_groups",
        "must_focus_known_failed_bands",
        "must_measure_all_bands_for_burden_context",
        "must_not_create_candidate",
        "must_not_accept_candidate",
    ]:
        if contract.get(key) is not True:
            failures.append(f"contract_flag_missing:{key}:{contract.get(key)}")

    surface = contract.get("bounded_source_surface") or {}
    if surface.get("v02_scale_probe_id") != EXPECTED_V02_SCALE_PROBE_ID:
        failures.append(f"surface_v02_scale_probe_wrong:{surface.get('v02_scale_probe_id')}")
    if surface.get("v03_probe_id") != EXPECTED_V03_PROBE_ID:
        failures.append(f"surface_v03_probe_wrong:{surface.get('v03_probe_id')}")
    if surface.get("v03_failure_diagnostic_id") != EXPECTED_V03_FAILURE_DIAG_ID:
        failures.append(f"surface_v03_diag_wrong:{surface.get('v03_failure_diagnostic_id')}")
    if surface.get("bounded_default_required") is not True:
        failures.append("bounded_default_required_not_true")
    if surface.get("full_registry_forbidden") is not True:
        failures.append("full_registry_forbidden_not_true")
    if surface.get("known_failed_bands_total") != 10:
        failures.append(f"known_failed_bands_total_not_10:{surface.get('known_failed_bands_total')}")
    if surface.get("all_bands_total") != 266:
        failures.append(f"all_bands_total_not_266:{surface.get('all_bands_total')}")

    auth = policy.get("authority") or {}
    if auth.get("observer_only") is not True:
        failures.append("policy_not_observer_only")
    if auth.get("authorizes_next_diagnostic_implementation") is not True:
        failures.append("policy_does_not_authorize_next_diagnostic")
    if auth.get("authorizes_raw_delta_compactness_measurement") is not True:
        failures.append("policy_does_not_authorize_raw_delta_measurement")
    for key in [
        "authorizes_candidate_design",
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
        "authorizes_rowid_or_receipt_hash_patch",
    ]:
        if auth.get(key) is not False:
            failures.append(f"policy_illegal_authority:{key}:{auth.get(key)}")

    constraints = policy.get("implementation_constraints") or {}
    if constraints.get("must_touch_only_files") != ["scripts/raw_delta_compactness_diagnostic_v0.py"]:
        failures.append(f"touch_scope_wrong:{constraints.get('must_touch_only_files')}")
    for key in [
        "must_reuse_existing_bounded_rows",
        "must_not_read_registry_sqlite",
        "must_not_full_registry_scan",
        "must_not_accept_candidate",
        "must_not_authorize_scale_mode",
        "must_not_change_runtime_receipt_emission",
    ]:
        if constraints.get(key) is not True:
            failures.append(f"constraint_missing:{key}:{constraints.get(key)}")

    if v03_diag.get("diagnostic_id") != EXPECTED_V03_FAILURE_DIAG_ID:
        failures.append(f"v03_failure_diag_id_wrong:{v03_diag.get('diagnostic_id')}")
    if v03_diag.get("gate") != "PASS":
        failures.append(f"v03_failure_diag_gate_not_PASS:{v03_diag.get('gate')}")
    if v03_diag.get("classification", {}).get("primary_class") != "BUCKETIZATION_COLLAPSED_RAW_DELTA_DIFFERENCE":
        failures.append(f"v03_failure_class_wrong:{v03_diag.get('classification', {}).get('primary_class')}")
    if v03_diag.get("classification", {}).get("burden_class") != "BURDEN_REGRESSION_CONFIRMED":
        failures.append(f"v03_failure_burden_class_wrong:{v03_diag.get('classification', {}).get('burden_class')}")
    if v03_diag.get("decision", {}).get("recommended_next_command_goal") != "BUILD_RAW_DELTA_COMPACTNESS_DIAGNOSTIC_POLICY_V0":
        failures.append(f"v03_failure_next_goal_wrong:{v03_diag.get('decision', {}).get('recommended_next_command_goal')}")
    if v03_diag.get("summary", {}).get("raw_delta_differing_column_counts", {}).get(TARGET_RAW_DELTA_FIELD) != 10:
        failures.append(f"v03_raw_compression_ratio_evidence_missing:{v03_diag.get('summary', {}).get('raw_delta_differing_column_counts')}")
    if v03_diag.get("summary", {}).get("bucket_delta_differing_column_counts") not in ({}, None):
        failures.append(f"v03_bucket_difference_unexpected:{v03_diag.get('summary', {}).get('bucket_delta_differing_column_counts')}")

    if v03_probe.get("probe_id") != EXPECTED_V03_PROBE_ID:
        failures.append(f"v03_probe_id_wrong:{v03_probe.get('probe_id')}")
    if v03_probe.get("terminal_decision") != "FAIL_V0_3_FALSE_MERGE_PERSISTS":
        failures.append(f"v03_probe_terminal_wrong:{v03_probe.get('terminal_decision')}")
    if v03_probe.get("bounded_source_surface", {}).get("full_registry_used") is not False:
        failures.append("v03_probe_used_full_registry")
    if v03_probe.get("authority_guards", {}).get("candidate_acceptance_authorized") is not False:
        failures.append("v03_candidate_acceptance_authorized")

    if v02_scale.get("probe_id") != EXPECTED_V02_SCALE_PROBE_ID:
        failures.append(f"v02_scale_probe_id_wrong:{v02_scale.get('probe_id')}")
    if v02_scale.get("terminal_decision") != "FAIL_SCALE_FALSE_MERGE":
        failures.append(f"v02_scale_terminal_wrong:{v02_scale.get('terminal_decision')}")
    if v02_scale.get("scale_coverage", {}).get("full_registry_used") is not False:
        failures.append("v02_scale_used_full_registry")
    if v02_scale.get("pass_gates", {}).get("no_false_merge_all_bands") is not False:
        failures.append("v02_false_merge_gate_not_false")

    return failures


def rows_by_band(rows: list[dict[str, Any]], *, id_field: str) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        out[row.get(id_field, "")].append(row)
    return dict(out)


def v02_rows_by_scale_row_id(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    out: dict[str, dict[str, Any]] = {}
    for row in rows:
        rid = row.get("scale_band_row_id")
        if rid:
            out[str(rid)] = row
    return out


def decimal_exact_string(value: Any) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    if text == "":
        return None
    try:
        dec = Decimal(text)
    except InvalidOperation:
        return text
    if not dec.is_finite():
        return text
    return format(dec.normalize(), "f")


def decimal_sig_string(value: Any, sig_digits: int) -> str | None:
    exact = decimal_exact_string(value)
    if exact is None:
        return None
    try:
        dec = Decimal(exact)
    except InvalidOperation:
        return exact

    if dec.is_zero():
        return "0"

    # Python format on Decimal with g gives compact significant-digit canonical-ish output.
    return format(dec, f".{sig_digits}g")


def encode_raw_delta(value: Any, encoding_id: str) -> dict[str, Any]:
    exact = decimal_exact_string(value)
    if exact is None:
        return {
            "status": "absent",
            "encoding_id": encoding_id,
            "target_field": TARGET_RAW_DELTA_FIELD,
            "value": None,
        }

    if encoding_id == "raw_decimal_string_exact":
        encoded = exact
        kind = "exact_decimal_string"
    elif encoding_id == "raw_decimal_sig6":
        encoded = decimal_sig_string(value, 6)
        kind = "significant_decimal_string"
    elif encoding_id == "raw_decimal_sig9":
        encoded = decimal_sig_string(value, 9)
        kind = "significant_decimal_string"
    elif encoding_id == "raw_decimal_sig12":
        encoded = decimal_sig_string(value, 12)
        kind = "significant_decimal_string"
    elif encoding_id == "raw_delta_microhash_32":
        encoded = hashlib.sha256(exact.encode("utf-8")).hexdigest()[:8]
        kind = "raw_value_microhash_32"
    else:
        raise ValueError(f"unknown encoding_id: {encoding_id}")

    return {
        "status": "present",
        "encoding_id": encoding_id,
        "target_field": TARGET_RAW_DELTA_FIELD,
        "encoding_kind": kind,
        "value": encoded,
    }


def source_v02_row_for_v03_row(v03_row: dict[str, Any], v02_by_id: dict[str, dict[str, Any]]) -> dict[str, Any] | None:
    source_row_id = ((v03_row.get("debug_sidecar") or {}).get("source_scale_band_row_id"))
    if not source_row_id:
        return None
    return v02_by_id.get(str(source_row_id))


def raw_compression_ratio_from_v02_row(v02_row: dict[str, Any] | None) -> Any:
    if not v02_row:
        return None
    debug = ((v02_row.get("debug_sidecar") or {}).get("compact_delta_debug") or {})
    entry = debug.get(TARGET_RAW_DELTA_FIELD)
    if isinstance(entry, dict):
        return entry.get("raw")
    return None


def measured_signature_payload(v03_row: dict[str, Any], raw_delta_encoding: dict[str, Any]) -> dict[str, Any]:
    old_payload = v03_row.get("signature_payload") or {}
    return {
        "cv": "raw_delta_compactness_v0",
        "state_hash_before": old_payload.get("state_hash_before"),
        "move_id": old_payload.get("move_id"),
        "state_hash_after": old_payload.get("state_hash_after"),
        "raw_delta_encoding": raw_delta_encoding,
    }


def payload_has_identity_leak(payload: dict[str, Any]) -> bool:
    text = json.dumps(payload, sort_keys=True, default=str).lower()
    return any(key.lower() in text for key in FORBIDDEN_PAYLOAD_KEYS)


def projected_row(candidate_delta_signature: str, source_v03_row: dict[str, Any]) -> dict[str, Any]:
    audit_pointer = source_v03_row.get("audit_pointer") or {}
    return {
        "candidate_delta_signature": candidate_delta_signature,
        "source_run_id": source_v03_row.get("source_run_id"),
        "compression_version": "raw_delta_compactness_diagnostic_v0",
        "audit_pointer": audit_pointer,
    }


def measure_encoding_for_band(encoding_id: str, source_band: dict[str, Any], v03_rows: list[dict[str, Any]], v02_by_id: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    sig_to_full: dict[str, set[str]] = defaultdict(set)
    full_to_sig: dict[str, set[str]] = defaultdict(set)

    source_surface_regression_count = 0
    raw_delta_missing_count = 0
    identity_leak_count = 0
    audit_recoverability_failures = 0

    full_receipt_bytes = int(source_band.get("full_receipt_bytes") or 0)
    signature_payload_bytes = 0
    projected_scale_row_bytes = 0
    encoded_value_counter: Counter[str] = Counter()

    out_rows: list[dict[str, Any]] = []

    for row in v03_rows:
        full_key = row.get("full_occurrence_key")
        if not full_key:
            source_surface_regression_count += 1
            continue

        v02_row = source_v02_row_for_v03_row(row, v02_by_id)
        raw_value = raw_compression_ratio_from_v02_row(v02_row)
        raw_delta_encoding = encode_raw_delta(raw_value, encoding_id)
        if raw_delta_encoding["status"] != "present":
            raw_delta_missing_count += 1

        payload = measured_signature_payload(row, raw_delta_encoding)

        if any(payload.get(k) in (None, "") for k in ["state_hash_before", "move_id", "state_hash_after"]):
            source_surface_regression_count += 1
        if payload_has_identity_leak(payload):
            identity_leak_count += 1

        candidate_delta_signature = sha8(payload)
        projected = projected_row(candidate_delta_signature, row)
        if not projected.get("audit_pointer"):
            audit_recoverability_failures += 1

        sig_to_full[candidate_delta_signature].add(str(full_key))
        full_to_sig[str(full_key)].add(candidate_delta_signature)

        payload_bytes = canonical_bytes(payload)
        projected_bytes = canonical_bytes(projected)
        signature_payload_bytes += payload_bytes
        projected_scale_row_bytes += projected_bytes
        if raw_delta_encoding["value"] is not None:
            encoded_value_counter[str(raw_delta_encoding["value"])] += 1

        out_rows.append({
            "raw_delta_compactness_row_id": sha8({
                "encoding_id": encoding_id,
                "source_band_id": source_band.get("band_id"),
                "full_occurrence_key": full_key,
                "candidate_delta_signature": candidate_delta_signature,
            }),
            "encoding_id": encoding_id,
            "source_band_id": source_band.get("band_id"),
            "axis": source_band.get("axis"),
            "axis_value": source_band.get("axis_value"),
            "source_run_id": row.get("source_run_id"),
            "full_occurrence_key": full_key,
            "candidate_delta_signature": candidate_delta_signature,
            "signature_payload": payload,
            "signature_payload_bytes": payload_bytes,
            "projected_scale_row_bytes": projected_bytes,
            "raw_compression_ratio": {
                "source_status": "present" if raw_value is not None else "absent",
                "raw_value": raw_value,
                "encoded": raw_delta_encoding,
            },
            "truth_surface": {
                "primary_comparison": "full_occurrence_key_to_candidate_delta_signature",
                "raw_full_receipt_hash_used_as_truth_surface": False,
                "full_receipt_hash_compared_to_delta_signature": False,
            },
            "authority_guards": {
                "observer_only": True,
                "candidate_created": False,
                "candidate_accepted": False,
                "scale_mode_authorized": False,
                "full_registry_scan_used": False,
                "registry_sqlite_read": False,
                "registry_sqlite_changed": False,
                "runtime_receipt_emission_changed": False,
            },
        })

    collision_groups = {sig: keys for sig, keys in sig_to_full.items() if len(keys) > 1}
    false_split_groups = {key: sigs for key, sigs in full_to_sig.items() if len(sigs) > 1}

    distinct_full = len(full_to_sig)
    distinct_sig = len(sig_to_full)
    burden_basis_bytes = signature_payload_bytes + projected_scale_row_bytes
    burden_ratio_projected = burden_basis_bytes / full_receipt_bytes if full_receipt_bytes else 0.0
    retention = distinct_sig / distinct_full if distinct_full else 0.0

    measurement = {
        "encoding_id": encoding_id,
        "band_id": source_band.get("band_id"),
        "axis": source_band.get("axis"),
        "axis_value": source_band.get("axis_value"),
        "run_id": source_band.get("run_id"),
        "was_known_failed_band": bool(source_band.get("band_id") in source_band.get("_known_failed_band_ids", set())),
        "occurrences_total": len(v03_rows),
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
        "burden_ratio_projected": burden_ratio_projected,
        "source_surface_regression_count": source_surface_regression_count,
        "raw_delta_missing_count": raw_delta_missing_count,
        "identity_leak_count": identity_leak_count,
        "audit_recoverability_failures": audit_recoverability_failures,
        "encoded_value_distinct_count": len(encoded_value_counter),
        "encoded_value_counts_top20": dict(encoded_value_counter.most_common(20)),
        "band_passed_for_diagnostic": (
            source_surface_regression_count == 0
            and raw_delta_missing_count == 0
            and identity_leak_count == 0
            and audit_recoverability_failures == 0
            and len(collision_groups) == 0
            and len(false_split_groups) == 0
            and burden_ratio_projected < 1.0
            and full_receipt_bytes > 0
        ),
        "failure_reasons": [
            reason
            for reason, condition in [
                ("source_surface_regression", source_surface_regression_count > 0),
                ("raw_delta_missing", raw_delta_missing_count > 0),
                ("identity_leak", identity_leak_count > 0),
                ("audit_recoverability", audit_recoverability_failures > 0),
                ("false_merge", len(collision_groups) > 0),
                ("false_split", len(false_split_groups) > 0),
                ("burden_regression", not (burden_ratio_projected < 1.0 and full_receipt_bytes > 0)),
            ]
            if condition
        ],
        "collision_gallery": [
            {
                "candidate_delta_signature": sig,
                "distinct_full_occurrence_keys": len(keys),
                "full_occurrence_keys": sorted(keys)[:20],
            }
            for sig, keys in sorted(collision_groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:10]
        ],
    }
    return measurement, out_rows


def aggregate_encoding(encoding_id: str, band_measurements: list[dict[str, Any]]) -> dict[str, Any]:
    known = [m for m in band_measurements if m.get("was_known_failed_band")]
    all_bands = band_measurements

    known_false_merge_bands = sum(1 for m in known if m["false_merge_count"] > 0)
    known_burden_regression_bands = sum(1 for m in known if m["burden_ratio_projected"] >= 1.0)
    all_false_merge_bands = sum(1 for m in all_bands if m["false_merge_count"] > 0)
    all_burden_regression_bands = sum(1 for m in all_bands if m["burden_ratio_projected"] >= 1.0)

    return {
        "encoding_id": encoding_id,
        "bands_total": len(all_bands),
        "known_failed_bands_total": len(known),
        "known_failed_false_merge_bands": known_false_merge_bands,
        "known_failed_burden_regression_bands": known_burden_regression_bands,
        "known_failed_all_clear": known_false_merge_bands == 0 and known_burden_regression_bands == 0 and len(known) == 10,
        "all_band_false_merge_bands": all_false_merge_bands,
        "all_band_burden_regression_bands": all_burden_regression_bands,
        "all_bands_clear": all_false_merge_bands == 0 and all_burden_regression_bands == 0 and len(all_bands) == 266,
        "worst_false_merge_count": max((m["false_merge_count"] for m in all_bands), default=0),
        "worst_collision_count": max((m["collision_count"] for m in all_bands), default=0),
        "worst_distinguishability_retention_ratio": min((m["distinguishability_retention_ratio"] for m in all_bands), default=0.0),
        "worst_burden_ratio_projected": max((m["burden_ratio_projected"] for m in all_bands), default=0.0),
        "worst_raw_delta_missing_count": max((m["raw_delta_missing_count"] for m in all_bands), default=0),
        "worst_identity_leak_count": max((m["identity_leak_count"] for m in all_bands), default=0),
        "worst_source_surface_regression_count": max((m["source_surface_regression_count"] for m in all_bands), default=0),
        "total_signature_payload_bytes": sum(m["signature_payload_bytes"] for m in all_bands),
        "total_projected_scale_row_bytes": sum(m["projected_scale_row_bytes"] for m in all_bands),
        "total_projected_plus_signature_payload_bytes": sum(m["projected_plus_signature_payload_bytes"] for m in all_bands),
        "total_full_receipt_bytes": sum(m["full_receipt_bytes"] for m in all_bands),
    }


def classify(encoding_summaries: dict[str, dict[str, Any]]) -> dict[str, Any]:
    viable = [
        enc for enc, s in encoding_summaries.items()
        if s["known_failed_false_merge_bands"] == 0
        and s["known_failed_burden_regression_bands"] == 0
        and s["worst_identity_leak_count"] == 0
        and s["worst_raw_delta_missing_count"] == 0
        and s["worst_source_surface_regression_count"] == 0
    ]
    clears_false_merges = [
        enc for enc, s in encoding_summaries.items()
        if s["known_failed_false_merge_bands"] == 0
    ]
    compact_viable = [enc for enc in viable if enc in {"raw_decimal_sig6", "raw_decimal_sig9", "raw_decimal_sig12", "raw_delta_microhash_32"}]
    exact_viable = "raw_decimal_string_exact" in viable

    if compact_viable:
        terminal_class = "RAW_DELTA_COMPACT_ENCODING_POSSIBLY_VIABLE"
        recommended_next = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_POLICY_V0"
        interpretation = "At least one compact raw compression_ratio encoding cleared known false merges and stayed below full-receipt burden. This is diagnostic only, not acceptance."
    elif exact_viable or ("raw_decimal_string_exact" in clears_false_merges and not compact_viable):
        terminal_class = "RAW_DELTA_ONLY_EXACT_VIABLE_BUT_TOO_HEAVY"
        recommended_next = "DIAGNOSE_RAW_DELTA_PRECISION_BURDEN_FRONTIER_V0"
        interpretation = "Raw compression_ratio can separate the collisions only at exact or burden-problematic precision; measure the precision/burden frontier before candidate design."
    elif clears_false_merges:
        terminal_class = "RAW_DELTA_ONLY_EXACT_VIABLE_BUT_TOO_HEAVY"
        recommended_next = "DIAGNOSE_RAW_DELTA_PRECISION_BURDEN_FRONTIER_V0"
        interpretation = "Some raw encoding clears false merges but fails burden; no candidate yet."
    else:
        terminal_class = "RAW_DELTA_NOT_VIABLE"
        recommended_next = "BUILD_RECURRENCE_AWARE_OCCURRENCE_SIGNATURE_POLICY_V0"
        interpretation = "Raw compression_ratio does not clear known false merges even before candidate acceptance; recurrence-aware occurrence structure is needed."

    return {
        "terminal_class": terminal_class,
        "recommended_next_command_goal": recommended_next,
        "interpretation": interpretation,
        "encodings_viable_on_known_failed_bands": viable,
        "encodings_clearing_known_false_merges": clears_false_merges,
        "compact_viable_encodings": compact_viable,
        "exact_viable": exact_viable,
    }


def build_diagnostic(policy_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    start = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    ROWS_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")
    v03_diag = load_json(V03_FAILURE_DIAG_DIR / f"{EXPECTED_V03_FAILURE_DIAG_ID}.json")
    v03_probe = load_json(V03_RECEIPT_DIR / f"{EXPECTED_V03_PROBE_ID}.json")
    v02_scale = load_json(V02_SCALE_RECEIPT_DIR / f"{EXPECTED_V02_SCALE_PROBE_ID}.json")

    failures = verify_sources(policy, policy_receipt, v03_diag, v03_probe, v02_scale)

    v03_rows = load_jsonl(ROOT / v03_probe["v03_rows_path"])
    v02_rows = load_jsonl(ROOT / v02_scale["scale_band_rows_path"])
    v02_by_id = v02_rows_by_scale_row_id(v02_rows)
    v03_by_band = rows_by_band(v03_rows, id_field="source_band_id")

    known_failed_band_ids = {
        b.get("band_id")
        for b in v02_scale.get("band_measurements", [])
        if not b.get("band_passed")
    }

    source_bands = []
    for b in v02_scale.get("band_measurements", []):
        bb = dict(b)
        bb["_known_failed_band_ids"] = known_failed_band_ids
        source_bands.append(bb)

    encoding_band_measurements: dict[str, list[dict[str, Any]]] = {enc: [] for enc in ENCODING_ORDER}
    diagnostic_rows: list[dict[str, Any]] = []

    for enc in ENCODING_ORDER:
        for band in source_bands:
            rows = v03_by_band.get(band.get("band_id"), [])
            measurement, out_rows = measure_encoding_for_band(enc, band, rows, v02_by_id)
            encoding_band_measurements[enc].append(measurement)
            diagnostic_rows.extend(out_rows)

    encoding_summaries = {
        enc: aggregate_encoding(enc, measurements)
        for enc, measurements in encoding_band_measurements.items()
    }

    classification = classify(encoding_summaries)

    policy_contract = policy.get("diagnostic_contract") or {}
    elapsed_ms = int(round((time.perf_counter() - start) * 1000))

    authority_guards = {
        "observer_only": True,
        "candidate_created": False,
        "candidate_accepted": False,
        "candidate_design_authorized": False,
        "scale_mode_authorized": False,
        "full_registry_scan_used": False,
        "registry_sqlite_read": False,
        "registry_sqlite_changed": False,
        "registry_write_authorized": False,
        "runtime_receipt_emission_changed": False,
        "raw_receipt_hash_used_as_truth_surface": False,
        "case_id_or_cycle_n_primary_identity_patch_used": False,
        "rowid_or_receipt_hash_patch_used": False,
    }

    pass_gates = {
        "authority_containment": all([
            authority_guards["observer_only"] is True,
            authority_guards["candidate_created"] is False,
            authority_guards["candidate_accepted"] is False,
            authority_guards["scale_mode_authorized"] is False,
            authority_guards["full_registry_scan_used"] is False,
            authority_guards["registry_sqlite_read"] is False,
            authority_guards["runtime_receipt_emission_changed"] is False,
        ]),
        "policy_preconditions": not failures,
        "bounded_rows_reused": True,
        "raw_delta_coverage": all(s["worst_raw_delta_missing_count"] == 0 for s in encoding_summaries.values()),
        "truth_surface": True,
        "no_identity_leak": all(s["worst_identity_leak_count"] == 0 for s in encoding_summaries.values()),
        "candidate_not_created": True,
        "candidate_not_accepted": True,
        "diagnostic_only": True,
    }

    diagnostic = {
        "schema_version": "raw_delta_compactness_diagnostic_v0",
        "diagnostic_name": DIAGNOSTIC_NAME,
        "mode": MODE,
        "diagnosis_status": "DIAGNOSED" if not failures else "SOURCE_VERIFICATION_FAILED",
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_v03_failure_diagnostic_id": EXPECTED_V03_FAILURE_DIAG_ID,
        "source_v03_probe_id": EXPECTED_V03_PROBE_ID,
        "source_v02_scale_probe_id": EXPECTED_V02_SCALE_PROBE_ID,
        "source_question": policy_contract.get("source_question"),
        "bounded_source_surface": {
            "v02_scale_rows_path": v02_scale.get("scale_band_rows_path"),
            "v03_rows_path": v03_probe.get("v03_rows_path"),
            "known_failed_bands_total": len(known_failed_band_ids),
            "all_bands_total": len(source_bands),
            "full_registry_used": False,
            "registry_sqlite_read": False,
        },
        "encoding_summaries": encoding_summaries,
        "classification": classification,
        "comparison_to_v02_v03": {
            "v02_terminal_decision": v02_scale.get("terminal_decision"),
            "v02_worst_false_merge_count": v02_scale.get("aggregate_measurements", {}).get("worst_false_merge_count"),
            "v02_worst_burden_ratio_projected": v02_scale.get("aggregate_measurements", {}).get("worst_burden_ratio_projected"),
            "v03_terminal_decision": v03_probe.get("terminal_decision"),
            "v03_worst_false_merge_count": v03_probe.get("aggregate_measurements", {}).get("worst_false_merge_count"),
            "v03_worst_burden_ratio_projected": v03_probe.get("aggregate_measurements", {}).get("worst_burden_ratio_projected"),
        },
        "band_measurement_gallery": {
            enc: measurements[:20]
            for enc, measurements in encoding_band_measurements.items()
        },
        "failed_collision_gallery": {
            enc: [
                m for m in measurements
                if m["false_merge_count"] > 0 or m["burden_ratio_projected"] >= 1.0
            ][:20]
            for enc, measurements in encoding_band_measurements.items()
        },
        "authority_guards": authority_guards,
        "pass_gates": pass_gates,
        "decision": {
            "diagnostic_only": True,
            "candidate_created": False,
            "candidate_accepted": False,
            "do_not_accept_candidate": True,
            "do_not_full_registry_scan": True,
            "do_not_change_runtime": True,
            "do_not_use_case_id_or_cycle_n_as_primary_identity": True,
            "do_not_use_rowid_or_receipt_hash": True,
            "primary_result": classification["terminal_class"],
            "recommended_next_command_goal": classification["recommended_next_command_goal"],
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": classification["recommended_next_command_goal"] if not failures else None,
            "stop_code": None if not failures else "STOP_RAW_DELTA_COMPACTNESS_SOURCE_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
        "actual_observer_overhead_ms": elapsed_ms,
    }

    diagnostic_id = sha8({
        "diagnostic_name": DIAGNOSTIC_NAME,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_v03_failure_diagnostic_id": EXPECTED_V03_FAILURE_DIAG_ID,
        "encoding_summaries": encoding_summaries,
        "classification": classification,
        "decision": diagnostic["decision"],
    })
    diagnostic["diagnostic_id"] = diagnostic_id
    diagnostic["diagnostic_sig8"] = diagnostic_id

    rows_path = ROWS_DIR / f"{diagnostic_id}.jsonl"
    with rows_path.open("w") as f:
        for row in diagnostic_rows:
            f.write(json.dumps(row, sort_keys=True, default=str) + "\n")
    diagnostic["diagnostic_rows_path"] = f"data/raw_delta_compactness_rows/{diagnostic_id}.jsonl"

    receipt = {
        "schema_version": "raw_delta_compactness_diagnostic_receipt_v0",
        "diagnostic_id": diagnostic_id,
        "diagnostic_sig8": diagnostic_id,
        "diagnostic_name": DIAGNOSTIC_NAME,
        "diagnosis_status": diagnostic["diagnosis_status"],
        "diagnostic_path": f"data/raw_delta_compactness_diagnostics/{diagnostic_id}.json",
        "diagnostic_rows_path": diagnostic["diagnostic_rows_path"],
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_v03_failure_diagnostic_id": EXPECTED_V03_FAILURE_DIAG_ID,
        "source_v03_probe_id": EXPECTED_V03_PROBE_ID,
        "source_v02_scale_probe_id": EXPECTED_V02_SCALE_PROBE_ID,
        "bounded_source_surface": diagnostic["bounded_source_surface"],
        "encoding_summaries": encoding_summaries,
        "classification": classification,
        "comparison_to_v02_v03": diagnostic["comparison_to_v02_v03"],
        "decision": diagnostic["decision"],
        "authority_guards": authority_guards,
        "pass_gates": pass_gates,
        "terminal": diagnostic["terminal"],
        "gate": diagnostic["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
        "actual_observer_overhead_ms": elapsed_ms,
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    (OUT_DIR / f"{diagnostic_id}.json").write_text(json.dumps(diagnostic, indent=2, sort_keys=True))
    (OUT_RECEIPT_DIR / f"{diagnostic_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return diagnostic, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-id", default=EXPECTED_POLICY_ID)
    args = parser.parse_args()

    diagnostic, receipt = build_diagnostic(args.policy_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"diagnostic_id={diagnostic['diagnostic_id']}")
    print(f"diagnostic_json_path=data/raw_delta_compactness_diagnostics/{diagnostic['diagnostic_id']}.json")
    print(f"diagnostic_receipt_path=data/raw_delta_compactness_diagnostic_receipts/{diagnostic['diagnostic_id']}.json")
    print(f"diagnostic_rows_path={diagnostic['diagnostic_rows_path']}")

    return 0 if diagnostic["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
