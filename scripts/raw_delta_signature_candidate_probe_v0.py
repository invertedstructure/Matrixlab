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

POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_policy_receipts"
RAW_DELTA_DIAG_DIR = ROOT / "data" / "raw_delta_compactness_diagnostics"
RAW_DELTA_DIAG_RECEIPT_DIR = ROOT / "data" / "raw_delta_compactness_diagnostic_receipts"
V02_SCALE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_receipts"

OUT_ROWS_DIR = ROOT / "data" / "raw_delta_signature_candidate_probe_rows"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_probe_receipts"

EXPECTED_POLICY_ID = "3b8eb867"
EXPECTED_POLICY_RECEIPT_ID = "6778ef03"
EXPECTED_RAW_DELTA_DIAGNOSTIC_ID = "74caa0f4"
EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID = "129e9a76"
EXPECTED_RAW_DELTA_POLICY_ID = "445bdd02"
EXPECTED_V03_FAILURE_DIAGNOSTIC_ID = "d0132dd4"
EXPECTED_V03_PROBE_ID = "bd1beabe"
EXPECTED_V02_SCALE_PROBE_ID = "227e9426"

PROBE_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_PROBE_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
COMPRESSION_VERSION = "raw_delta_signature_candidate_v0"
MODE = "OUTER_OBSERVER_ONLY"

SELECTED_ENCODING_ID = "raw_decimal_sig6"
TARGET_RAW_DELTA_FIELD = "compression_ratio"

REQUIRED_PAYLOAD_FIELDS = [
    "cv",
    "state_hash_before",
    "move_id",
    "state_hash_after",
    "raw_compression_ratio_sig6",
]

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
    "raw_delta_microhash_32_as_proof",
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


def verify_sources(policy: dict[str, Any], policy_receipt: dict[str, Any], raw_diag: dict[str, Any], raw_diag_receipt: dict[str, Any]) -> list[str]:
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
    if policy.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"candidate_design_id_wrong:{policy.get('candidate_design_id')}")
    if policy.get("terminal", {}).get("next_command_goal") != "IMPLEMENT_RAW_DELTA_SIGNATURE_CANDIDATE_PROBE_V0":
        failures.append(f"policy_next_goal_wrong:{policy.get('terminal', {}).get('next_command_goal')}")

    contract = policy.get("candidate_contract") or {}
    if contract.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"contract_candidate_design_wrong:{contract.get('candidate_design_id')}")
    if contract.get("selected_encoding_id") != SELECTED_ENCODING_ID:
        failures.append(f"selected_encoding_wrong:{contract.get('selected_encoding_id')}")
    if contract.get("selected_target_raw_delta_field") != TARGET_RAW_DELTA_FIELD:
        failures.append(f"selected_target_field_wrong:{contract.get('selected_target_raw_delta_field')}")
    if contract.get("signature_payload_required_fields") != REQUIRED_PAYLOAD_FIELDS:
        failures.append(f"required_payload_fields_wrong:{contract.get('signature_payload_required_fields')}")
    if contract.get("truth_surface") != "full_occurrence_key_to_candidate_delta_signature":
        failures.append(f"truth_surface_wrong:{contract.get('truth_surface')}")

    for forbidden in [
        "full_occurrence_key",
        "raw_full_receipt_hash",
        "receipt_hash",
        "receipt_rowid",
        "rowid",
        "audit_pointer",
        "debug_payload",
        "case_id",
        "cycle_n",
        "raw_delta_microhash_32_as_proof",
    ]:
        if forbidden not in set(contract.get("signature_payload_forbidden_fields") or []):
            failures.append(f"forbidden_field_missing_from_contract:{forbidden}")

    evidence = (contract.get("source_evidence") or {}).get("selected_encoding_summary") or {}
    if evidence.get("encoding_id") != SELECTED_ENCODING_ID:
        failures.append(f"evidence_encoding_wrong:{evidence.get('encoding_id')}")
    if evidence.get("all_bands_clear") is not True:
        failures.append(f"evidence_all_bands_not_clear:{evidence.get('all_bands_clear')}")
    if evidence.get("known_failed_all_clear") is not True:
        failures.append(f"evidence_known_failed_not_clear:{evidence.get('known_failed_all_clear')}")
    if evidence.get("worst_false_merge_count") != 0:
        failures.append(f"evidence_false_merge_not_0:{evidence.get('worst_false_merge_count')}")
    if evidence.get("worst_collision_count") != 0:
        failures.append(f"evidence_collision_not_0:{evidence.get('worst_collision_count')}")
    if evidence.get("worst_distinguishability_retention_ratio") != 1.0:
        failures.append(f"evidence_retention_not_1:{evidence.get('worst_distinguishability_retention_ratio')}")
    if not (evidence.get("worst_burden_ratio_projected", 999) < 1.0):
        failures.append(f"evidence_burden_not_below_1:{evidence.get('worst_burden_ratio_projected')}")
    if evidence.get("worst_identity_leak_count") != 0:
        failures.append(f"evidence_identity_leak:{evidence.get('worst_identity_leak_count')}")
    if evidence.get("worst_raw_delta_missing_count") != 0:
        failures.append(f"evidence_raw_delta_missing:{evidence.get('worst_raw_delta_missing_count')}")
    if evidence.get("worst_source_surface_regression_count") != 0:
        failures.append(f"evidence_source_surface_regression:{evidence.get('worst_source_surface_regression_count')}")

    bounded = contract.get("bounded_probe_surface") or {}
    if bounded.get("must_reuse_raw_delta_diagnostic_rows_path") != "data/raw_delta_compactness_rows/74caa0f4.jsonl":
        failures.append(f"raw_delta_rows_path_wrong:{bounded.get('must_reuse_raw_delta_diagnostic_rows_path')}")
    if bounded.get("must_reuse_v02_scale_rows_path") != "data/stable_delta_signature_candidate_v0_2_scale_band_rows/227e9426.jsonl":
        failures.append(f"v02_rows_path_wrong:{bounded.get('must_reuse_v02_scale_rows_path')}")
    if bounded.get("must_reuse_v03_rows_path") != "data/stable_delta_signature_candidate_v0_3_rows/bd1beabe.jsonl":
        failures.append(f"v03_rows_path_wrong:{bounded.get('must_reuse_v03_rows_path')}")
    if bounded.get("known_failed_bands_total") != 10:
        failures.append(f"known_failed_bands_total_not_10:{bounded.get('known_failed_bands_total')}")
    if bounded.get("all_bands_total") != 266:
        failures.append(f"all_bands_total_not_266:{bounded.get('all_bands_total')}")
    if bounded.get("full_registry_forbidden") is not True:
        failures.append("full_registry_not_forbidden")
    if bounded.get("registry_sqlite_read_forbidden") is not True:
        failures.append("registry_sqlite_read_not_forbidden")

    for key in [
        "all_band_false_merge_count",
        "known_failed_false_merge_count",
        "distinguishability_retention_ratio",
        "projected_burden_ratio",
        "signature_payload_bytes",
        "raw_delta_coverage",
        "identity_leak_check",
        "comparison_to_v02_v03_and_raw_delta_diagnostic",
    ]:
        if (contract.get("candidate_probe_required_measurements") or {}).get(key) is not True:
            failures.append(f"required_measurement_missing:{key}")

    auth = policy.get("authority") or {}
    if auth.get("observer_only") is not True:
        failures.append("policy_not_observer_only")
    if auth.get("authorizes_bounded_candidate_probe_execution") is not True:
        failures.append("bounded_candidate_probe_not_authorized")
    if auth.get("authorizes_next_candidate_probe_implementation") is not True:
        failures.append("next_candidate_probe_not_authorized")
    for key in [
        "authorizes_candidate_acceptance",
        "authorizes_scale_mode",
        "authorizes_full_registry_scan",
        "authorizes_registry_sqlite_read",
        "authorizes_runtime_receipt_emission_change",
        "authorizes_registry_write",
        "authorizes_receipt_replacement",
        "authorizes_receipt_deletion",
        "authorizes_receipt_compression",
        "authorizes_receipt_suppression",
        "authorizes_raw_receipt_hash_truth_surface",
        "authorizes_case_id_or_cycle_n_primary_identity_patch",
        "authorizes_rowid_or_receipt_hash_patch",
        "authorizes_full_occurrence_key_in_payload",
        "authorizes_audit_pointer_in_payload",
        "authorizes_debug_payload_in_payload",
        "authorizes_microhash_as_proof",
    ]:
        if auth.get(key) is not False:
            failures.append(f"policy_illegal_authority:{key}:{auth.get(key)}")

    constraints = policy.get("implementation_constraints") or {}
    if constraints.get("must_touch_only_files") != ["scripts/raw_delta_signature_candidate_probe_v0.py"]:
        failures.append(f"touch_scope_wrong:{constraints.get('must_touch_only_files')}")
    for key in [
        "must_reuse_existing_bounded_rows",
        "must_not_read_registry_sqlite",
        "must_not_full_registry_scan",
        "must_not_accept_candidate",
        "must_not_authorize_scale_mode",
        "must_not_change_runtime_receipt_emission",
        "must_not_write_registry",
    ]:
        if constraints.get(key) is not True:
            failures.append(f"constraint_missing:{key}:{constraints.get(key)}")

    if raw_diag.get("diagnostic_id") != EXPECTED_RAW_DELTA_DIAGNOSTIC_ID:
        failures.append(f"raw_diag_id_wrong:{raw_diag.get('diagnostic_id')}")
    if raw_diag_receipt.get("receipt_id") != EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID:
        failures.append(f"raw_diag_receipt_id_wrong:{raw_diag_receipt.get('receipt_id')}")
    if raw_diag.get("gate") != "PASS":
        failures.append(f"raw_diag_gate_not_PASS:{raw_diag.get('gate')}")
    if raw_diag.get("diagnosis_status") != "DIAGNOSED":
        failures.append(f"raw_diag_status_wrong:{raw_diag.get('diagnosis_status')}")
    if raw_diag.get("classification", {}).get("terminal_class") != "RAW_DELTA_COMPACT_ENCODING_POSSIBLY_VIABLE":
        failures.append(f"raw_diag_terminal_class_wrong:{raw_diag.get('classification', {}).get('terminal_class')}")
    if raw_diag.get("decision", {}).get("candidate_created") is not False:
        failures.append("raw_diag_candidate_created")
    if raw_diag.get("decision", {}).get("candidate_accepted") is not False:
        failures.append("raw_diag_candidate_accepted")
    if raw_diag.get("authority_guards", {}).get("full_registry_scan_used") is not False:
        failures.append("raw_diag_full_registry_used")
    if raw_diag.get("authority_guards", {}).get("registry_sqlite_read") is not False:
        failures.append("raw_diag_registry_sqlite_read")

    return failures


def payload_has_identity_leak(payload: dict[str, Any]) -> bool:
    text = json.dumps(payload, sort_keys=True, default=str).lower()
    return any(key.lower() in text for key in FORBIDDEN_PAYLOAD_KEYS)


def candidate_payload_from_raw_delta_row(row: dict[str, Any]) -> tuple[dict[str, Any] | None, str | None]:
    if row.get("encoding_id") != SELECTED_ENCODING_ID:
        return None, "wrong_encoding"

    source_payload = row.get("signature_payload") or {}
    raw_enc = source_payload.get("raw_delta_encoding") or {}
    raw_field = raw_enc.get("target_field")
    if raw_field != TARGET_RAW_DELTA_FIELD:
        return None, f"wrong_target_field:{raw_field}"
    if raw_enc.get("encoding_id") != SELECTED_ENCODING_ID:
        return None, f"wrong_raw_encoding:{raw_enc.get('encoding_id')}"
    if raw_enc.get("status") != "present":
        return None, "raw_delta_absent"

    value = raw_enc.get("value")
    if value in (None, ""):
        return None, "raw_delta_value_empty"

    payload = {
        "cv": "raw_delta_signature_v0",
        "state_hash_before": source_payload.get("state_hash_before"),
        "move_id": source_payload.get("move_id"),
        "state_hash_after": source_payload.get("state_hash_after"),
        "raw_compression_ratio_sig6": str(value),
    }

    missing = [k for k in REQUIRED_PAYLOAD_FIELDS if payload.get(k) in (None, "")]
    if missing:
        return None, f"missing_required_payload_fields:{','.join(missing)}"
    if payload_has_identity_leak(payload):
        return None, "identity_leak"

    return payload, None


def projected_candidate_row(candidate_delta_signature: str, row: dict[str, Any]) -> dict[str, Any]:
    return {
        "candidate_delta_signature": candidate_delta_signature,
        "source_run_id": row.get("source_run_id"),
        "compression_version": COMPRESSION_VERSION,
        "audit_pointer": {
            "source_raw_delta_compactness_row_id": row.get("raw_delta_compactness_row_id"),
            "source_band_id": row.get("source_band_id"),
            "source_run_id": row.get("source_run_id"),
        },
    }


def group_rows_by_band(rows: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    out: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        band_id = row.get("source_band_id")
        if band_id:
            out[str(band_id)].append(row)
    return dict(out)


def measure_band(band_id: str, rows: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    sig_to_full: dict[str, set[str]] = defaultdict(set)
    full_to_sig: dict[str, set[str]] = defaultdict(set)
    encoded_values: Counter[str] = Counter()

    failures_by_reason = Counter()
    signature_payload_bytes = 0
    projected_scale_row_bytes = 0
    full_receipt_bytes_values: list[int] = []

    out_rows: list[dict[str, Any]] = []

    for row in rows:
        full_key = row.get("full_occurrence_key")
        if not full_key:
            failures_by_reason["missing_full_occurrence_key"] += 1
            continue

        payload, failure = candidate_payload_from_raw_delta_row(row)
        if failure:
            failures_by_reason[failure] += 1
            continue

        candidate_delta_signature = sha8(payload)
        projected = projected_candidate_row(candidate_delta_signature, row)
        if not projected.get("audit_pointer"):
            failures_by_reason["audit_recoverability"] += 1

        sig_to_full[candidate_delta_signature].add(str(full_key))
        full_to_sig[str(full_key)].add(candidate_delta_signature)
        encoded_values[payload["raw_compression_ratio_sig6"]] += 1

        payload_bytes = canonical_bytes(payload)
        projected_bytes = canonical_bytes(projected)
        signature_payload_bytes += payload_bytes
        projected_scale_row_bytes += projected_bytes

        # All rows in a source band carry the same full_receipt_bytes from the raw-delta diagnostic measurement.
        source_full = row.get("source_band_full_receipt_bytes")
        if isinstance(source_full, int):
            full_receipt_bytes_values.append(source_full)

        out_rows.append({
            "raw_delta_signature_candidate_row_id": sha8({
                "band_id": band_id,
                "full_occurrence_key": full_key,
                "candidate_delta_signature": candidate_delta_signature,
            }),
            "candidate_design_id": CANDIDATE_DESIGN_ID,
            "compression_version": COMPRESSION_VERSION,
            "source_band_id": band_id,
            "axis": row.get("axis"),
            "axis_value": row.get("axis_value"),
            "source_run_id": row.get("source_run_id"),
            "full_occurrence_key": full_key,
            "candidate_delta_signature": candidate_delta_signature,
            "signature_payload": payload,
            "signature_payload_bytes": payload_bytes,
            "projected_scale_row_bytes": projected_bytes,
            "audit_pointer": projected["audit_pointer"],
            "truth_surface": {
                "primary_comparison": "full_occurrence_key_to_candidate_delta_signature",
                "raw_full_receipt_hash_used_as_truth_surface": False,
                "full_receipt_hash_compared_to_delta_signature": False,
            },
            "authority_guards": {
                "observer_only": True,
                "candidate_accepted": False,
                "scale_mode_authorized": False,
                "full_registry_scan_used": False,
                "registry_sqlite_read": False,
                "registry_sqlite_changed": False,
                "runtime_receipt_emission_changed": False,
                "registry_write_authorized": False,
            },
        })

    collision_groups = {sig: keys for sig, keys in sig_to_full.items() if len(keys) > 1}
    false_split_groups = {key: sigs for key, sigs in full_to_sig.items() if len(sigs) > 1}

    distinct_full = len(full_to_sig)
    distinct_sig = len(sig_to_full)

    # The raw-delta rows do not repeat full_receipt_bytes per row, so reconstruct per-band basis from row-level diagnostics.
    # If unavailable, use the max/0 fallback and let source-surface fail rather than inventing a pass.
    source_full_receipt_bytes = max(full_receipt_bytes_values) if full_receipt_bytes_values else 0
    if source_full_receipt_bytes == 0:
        # Backward-compatible fallback: per raw-delta row lacks this field; estimate from bytes ratios cannot be lawful.
        # Classify as missing burden basis for the band.
        failures_by_reason["missing_full_receipt_bytes"] += 1

    projected_plus_payload_bytes = signature_payload_bytes + projected_scale_row_bytes
    burden_ratio_projected = projected_plus_payload_bytes / source_full_receipt_bytes if source_full_receipt_bytes else 0.0
    retention = distinct_sig / distinct_full if distinct_full else 0.0

    band_measurement = {
        "band_id": band_id,
        "axis": rows[0].get("axis") if rows else None,
        "axis_value": rows[0].get("axis_value") if rows else None,
        "run_id": rows[0].get("source_run_id") if rows else None,
        "occurrences_total": len(rows),
        "measured_rows_total": len(out_rows),
        "distinct_full_occurrence_keys": distinct_full,
        "distinct_candidate_signatures": distinct_sig,
        "collision_count": len(collision_groups),
        "false_merge_count": len(collision_groups),
        "false_split_count": len(false_split_groups),
        "distinguishability_retention_ratio": retention,
        "full_receipt_bytes": source_full_receipt_bytes,
        "signature_payload_bytes": signature_payload_bytes,
        "projected_scale_row_bytes": projected_scale_row_bytes,
        "projected_plus_signature_payload_bytes": projected_plus_payload_bytes,
        "burden_ratio_projected": burden_ratio_projected,
        "encoded_value_distinct_count": len(encoded_values),
        "encoded_value_counts_top20": dict(encoded_values.most_common(20)),
        "identity_leak_count": failures_by_reason.get("identity_leak", 0),
        "raw_delta_missing_count": (
            failures_by_reason.get("raw_delta_absent", 0)
            + failures_by_reason.get("raw_delta_value_empty", 0)
        ),
        "source_surface_regression_count": (
            failures_by_reason.get("missing_required_payload_fields:cv,state_hash_before,move_id,state_hash_after,raw_compression_ratio_sig6", 0)
            + failures_by_reason.get("missing_full_occurrence_key", 0)
            + failures_by_reason.get("missing_full_receipt_bytes", 0)
        ),
        "audit_recoverability_failures": failures_by_reason.get("audit_recoverability", 0),
        "failure_reason_counts": dict(failures_by_reason),
        "band_passed": (
            not failures_by_reason
            and len(collision_groups) == 0
            and len(false_split_groups) == 0
            and source_full_receipt_bytes > 0
            and burden_ratio_projected < 1.0
        ),
        "failure_reasons": [
            reason
            for reason, condition in [
                ("source_surface_regression", bool(failures_by_reason)),
                ("false_merge", len(collision_groups) > 0),
                ("false_split", len(false_split_groups) > 0),
                ("burden_regression", not (source_full_receipt_bytes > 0 and burden_ratio_projected < 1.0)),
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
    return band_measurement, out_rows


def enrich_raw_delta_rows_with_band_burden(raw_rows: list[dict[str, Any]], raw_diag: dict[str, Any]) -> list[dict[str, Any]]:
    # Source-surface patch v0:
    # The raw-delta diagnostic galleries are intentionally truncated for receipt readability.
    # The complete lawful burden basis lives in the bounded v02 scale-band receipt's
    # full band_measurements array. Recover full_receipt_bytes from that complete
    # bounded receipt; do not use registry.sqlite, do not scan full registry, and do
    # not invent missing burden values.
    full_by_band: dict[str, int] = {}

    v02_scale = load_json(V02_SCALE_RECEIPT_DIR / f"{EXPECTED_V02_SCALE_PROBE_ID}.json")
    for band in v02_scale.get("band_measurements", []):
        band_id = band.get("band_id")
        full = band.get("full_receipt_bytes")
        if band_id and isinstance(full, int) and full > 0:
            full_by_band[str(band_id)] = int(full)

    out = []
    for row in raw_rows:
        rr = dict(row)
        band_id = rr.get("source_band_id")
        if band_id in full_by_band:
            rr["source_band_full_receipt_bytes"] = full_by_band[str(band_id)]
            rr["source_band_full_receipt_bytes_source"] = "v02_scale_band_receipt_full_band_measurements"
        else:
            rr["source_band_full_receipt_bytes_missing"] = True
        out.append(rr)

    return out


def aggregate(band_measurements: list[dict[str, Any]]) -> dict[str, Any]:
    total_full = sum(m["full_receipt_bytes"] for m in band_measurements)
    total_payload = sum(m["signature_payload_bytes"] for m in band_measurements)
    total_projected = sum(m["projected_scale_row_bytes"] for m in band_measurements)
    total_projected_plus_payload = sum(m["projected_plus_signature_payload_bytes"] for m in band_measurements)

    return {
        "bands_total": len(band_measurements),
        "bands_passed": sum(1 for m in band_measurements if m["band_passed"]),
        "bands_failed": sum(1 for m in band_measurements if not m["band_passed"]),
        "all_band_false_merge_count": sum(1 for m in band_measurements if m["false_merge_count"] > 0),
        "all_band_burden_regression_count": sum(1 for m in band_measurements if m["burden_ratio_projected"] >= 1.0 or m["full_receipt_bytes"] <= 0),
        "worst_false_merge_count": max((m["false_merge_count"] for m in band_measurements), default=0),
        "worst_collision_count": max((m["collision_count"] for m in band_measurements), default=0),
        "worst_false_split_count": max((m["false_split_count"] for m in band_measurements), default=0),
        "worst_distinguishability_retention_ratio": min((m["distinguishability_retention_ratio"] for m in band_measurements), default=0.0),
        "worst_burden_ratio_projected": max((m["burden_ratio_projected"] for m in band_measurements), default=0.0),
        "worst_identity_leak_count": max((m["identity_leak_count"] for m in band_measurements), default=0),
        "worst_raw_delta_missing_count": max((m["raw_delta_missing_count"] for m in band_measurements), default=0),
        "worst_source_surface_regression_count": max((m["source_surface_regression_count"] for m in band_measurements), default=0),
        "worst_audit_recoverability_failures": max((m["audit_recoverability_failures"] for m in band_measurements), default=0),
        "total_full_receipt_bytes": total_full,
        "total_signature_payload_bytes": total_payload,
        "total_projected_scale_row_bytes": total_projected,
        "total_projected_plus_signature_payload_bytes": total_projected_plus_payload,
        "total_burden_ratio_projected": total_projected_plus_payload / total_full if total_full else 0.0,
    }


def build_probe(policy_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    start = time.perf_counter()
    OUT_ROWS_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")
    raw_diag = load_json(RAW_DELTA_DIAG_DIR / f"{EXPECTED_RAW_DELTA_DIAGNOSTIC_ID}.json")
    raw_diag_receipt = load_json(RAW_DELTA_DIAG_RECEIPT_DIR / f"{EXPECTED_RAW_DELTA_DIAGNOSTIC_ID}.json")

    source_failures = verify_sources(policy, policy_receipt, raw_diag, raw_diag_receipt)

    raw_rows_path = ROOT / policy["candidate_contract"]["bounded_probe_surface"]["must_reuse_raw_delta_diagnostic_rows_path"]
    raw_rows_all = load_jsonl(raw_rows_path)

    selected_rows = [r for r in raw_rows_all if r.get("encoding_id") == SELECTED_ENCODING_ID]
    enriched_rows = enrich_raw_delta_rows_with_band_burden(selected_rows, raw_diag)
    by_band = group_rows_by_band(enriched_rows)

    band_measurements = []
    out_rows = []
    for band_id in sorted(by_band):
        measurement, rows = measure_band(band_id, by_band[band_id])
        band_measurements.append(measurement)
        out_rows.extend(rows)

    aggregate_measurements = aggregate(band_measurements)

    pass_gates = {
        "authority_containment": True,
        "policy_preconditions": not source_failures,
        "bounded_surface_reused": True,
        "raw_delta_coverage": aggregate_measurements["worst_raw_delta_missing_count"] == 0,
        "source_surface": aggregate_measurements["worst_source_surface_regression_count"] == 0,
        "truth_surface": True,
        "no_identity_leak": aggregate_measurements["worst_identity_leak_count"] == 0,
        "audit_recoverability": aggregate_measurements["worst_audit_recoverability_failures"] == 0,
        "no_false_merge_all_bands": aggregate_measurements["all_band_false_merge_count"] == 0,
        "no_false_split_all_bands": aggregate_measurements["worst_false_split_count"] == 0,
        "burden_reduction": aggregate_measurements["all_band_burden_regression_count"] == 0 and aggregate_measurements["worst_burden_ratio_projected"] < 1.0,
        "candidate_not_accepted": True,
        "scale_mode_not_authorized": True,
    }

    failure_conditions = []
    if source_failures:
        failure_conditions.append("source_verification")
    if not pass_gates["raw_delta_coverage"] or not pass_gates["source_surface"]:
        failure_conditions.append("source_surface")
    if not pass_gates["no_identity_leak"]:
        failure_conditions.append("identity_leak")
    if not pass_gates["no_false_merge_all_bands"]:
        failure_conditions.append("false_merge")
    if not pass_gates["burden_reduction"]:
        failure_conditions.append("burden")
    if not pass_gates["authority_containment"]:
        failure_conditions.append("authority")

    if not failure_conditions:
        terminal_decision = "PASS_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_PROBE"
        terminal = {
            "type": "ADVANCE",
            "next_command_goal": "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_SCALE_REVIEW_POLICY_V0",
            "stop_code": None,
        }
    elif "authority" in failure_conditions:
        terminal_decision = "FAIL_RAW_DELTA_SIGNATURE_AUTHORITY"
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": terminal_decision}
    elif "identity_leak" in failure_conditions:
        terminal_decision = "FAIL_RAW_DELTA_SIGNATURE_IDENTITY_LEAK"
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": terminal_decision}
    elif "source_surface" in failure_conditions or "source_verification" in failure_conditions:
        terminal_decision = "FAIL_RAW_DELTA_SIGNATURE_SOURCE_SURFACE"
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": terminal_decision}
    elif "false_merge" in failure_conditions:
        terminal_decision = "FAIL_RAW_DELTA_SIGNATURE_FALSE_MERGE"
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": terminal_decision}
    else:
        terminal_decision = "FAIL_RAW_DELTA_SIGNATURE_BURDEN"
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": terminal_decision}

    authority_guards = {
        "observer_only": True,
        "candidate_accepted": False,
        "scale_mode_authorized": False,
        "full_registry_scan_used": False,
        "registry_sqlite_read": False,
        "registry_sqlite_changed": False,
        "runtime_receipt_emission_changed": False,
        "registry_write_authorized": False,
        "receipt_replacement_authorized": False,
        "receipt_deletion_authorized": False,
        "receipt_compression_authorized": False,
        "receipt_suppression_authorized": False,
        "raw_receipt_hash_used_as_truth_surface": False,
        "case_id_or_cycle_n_primary_identity_patch_used": False,
        "rowid_or_receipt_hash_patch_used": False,
        "full_occurrence_key_in_payload": False,
        "audit_pointer_in_payload": False,
        "debug_payload_in_payload": False,
        "microhash_as_proof_used": False,
    }

    elapsed_ms = int(round((time.perf_counter() - start) * 1000))

    probe = {
        "schema_version": "raw_delta_signature_candidate_probe_v0",
        "probe_name": PROBE_NAME,
        "mode": MODE,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "compression_version": COMPRESSION_VERSION,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_raw_delta_diagnostic_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_ID,
        "source_raw_delta_diagnostic_receipt_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID,
        "source_raw_delta_policy_id": EXPECTED_RAW_DELTA_POLICY_ID,
        "source_v03_failure_diagnostic_id": EXPECTED_V03_FAILURE_DIAGNOSTIC_ID,
        "source_v03_probe_id": EXPECTED_V03_PROBE_ID,
        "source_v02_scale_probe_id": EXPECTED_V02_SCALE_PROBE_ID,
        "candidate_contract": {
            "selected_encoding_id": SELECTED_ENCODING_ID,
            "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
            "signature_payload_required_fields": REQUIRED_PAYLOAD_FIELDS,
            "signature_payload_forbidden_fields": sorted(FORBIDDEN_PAYLOAD_KEYS),
            "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
        },
        "bounded_source_surface": {
            "raw_delta_diagnostic_rows_path": str(raw_rows_path.relative_to(ROOT)),
            "selected_encoding_rows_total": len(selected_rows),
            "bands_total": len(by_band),
            "full_registry_used": False,
            "registry_sqlite_read": False,
        },
        "aggregate_measurements": aggregate_measurements,
        "band_measurements": band_measurements,
        "comparison_to_source_evidence": {
            "raw_delta_diagnostic_selected_encoding": (policy.get("candidate_contract") or {}).get("source_evidence", {}).get("selected_encoding_summary"),
            "raw_delta_candidate_probe": aggregate_measurements,
        },
        "authority_guards": authority_guards,
        "pass_gates": pass_gates,
        "decision": {
            "candidate_accepted": False,
            "candidate_acceptance_authorized": False,
            "diagnostic_probe_only": True,
            "do_not_accept_candidate": True,
            "do_not_full_registry_scan": True,
            "do_not_read_registry_sqlite": True,
            "do_not_change_runtime": True,
            "do_not_write_registry": True,
            "do_not_use_case_id_or_cycle_n_as_primary_identity": True,
            "do_not_use_rowid_or_receipt_hash": True,
            "terminal_decision": terminal_decision,
        },
        "terminal_decision": terminal_decision,
        "terminal": terminal,
        "gate": "PASS" if not source_failures else "FAIL",
        "failures": source_failures,
        "warnings": [],
        "created_at": now_iso(),
        "actual_observer_overhead_ms": elapsed_ms,
    }

    probe_id = sha8({
        "probe_name": PROBE_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_policy_id": EXPECTED_POLICY_ID,
        "aggregate_measurements": aggregate_measurements,
        "terminal_decision": terminal_decision,
    })
    probe["probe_id"] = probe_id
    probe["probe_sig8"] = probe_id

    rows_path = OUT_ROWS_DIR / f"{probe_id}.jsonl"
    with rows_path.open("w") as f:
        for row in out_rows:
            f.write(json.dumps(row, sort_keys=True, default=str) + "\n")
    probe["candidate_probe_rows_path"] = f"data/raw_delta_signature_candidate_probe_rows/{probe_id}.jsonl"

    receipt = {
        "schema_version": "raw_delta_signature_candidate_probe_receipt_v0",
        "probe_id": probe_id,
        "probe_sig8": probe_id,
        "probe_name": PROBE_NAME,
        "mode": MODE,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "compression_version": COMPRESSION_VERSION,
        "candidate_probe_rows_path": probe["candidate_probe_rows_path"],
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_raw_delta_diagnostic_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_ID,
        "source_raw_delta_diagnostic_receipt_id": EXPECTED_RAW_DELTA_DIAGNOSTIC_RECEIPT_ID,
        "source_v03_failure_diagnostic_id": EXPECTED_V03_FAILURE_DIAGNOSTIC_ID,
        "source_v03_probe_id": EXPECTED_V03_PROBE_ID,
        "source_v02_scale_probe_id": EXPECTED_V02_SCALE_PROBE_ID,
        "candidate_contract": probe["candidate_contract"],
        "bounded_source_surface": probe["bounded_source_surface"],
        "aggregate_measurements": aggregate_measurements,
        "comparison_to_source_evidence": probe["comparison_to_source_evidence"],
        "authority_guards": authority_guards,
        "pass_gates": pass_gates,
        "decision": probe["decision"],
        "terminal_decision": terminal_decision,
        "terminal": terminal,
        "gate": probe["gate"],
        "failures": source_failures,
        "warnings": [],
        "created_at": now_iso(),
        "actual_observer_overhead_ms": elapsed_ms,
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    (OUT_RECEIPT_DIR / f"{probe_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return probe, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-id", default=EXPECTED_POLICY_ID)
    args = parser.parse_args()

    probe, receipt = build_probe(args.policy_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"probe_id={probe['probe_id']}")
    print(f"probe_receipt_path=data/raw_delta_signature_candidate_probe_receipts/{probe['probe_id']}.json")
    print(f"candidate_probe_rows_path={probe['candidate_probe_rows_path']}")

    return 0 if probe["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
