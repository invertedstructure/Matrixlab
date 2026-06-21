#!/usr/bin/env python3
from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_bounded_scale_out_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_bounded_scale_out_policy_receipts"
SCALE_REVIEW_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_scale_review_receipts"
CANDIDATE_PROBE_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_probe_receipts"
V02_SCALE_RECEIPT_DIR = ROOT / "data" / "stable_delta_signature_candidate_v0_2_scale_band_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_bounded_scale_outs"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_bounded_scale_out_receipts"
OUT_ROWS_DIR = ROOT / "data" / "raw_delta_signature_candidate_bounded_scale_out_rows"

EXPECTED_POLICY_ID = "189aab7f"
EXPECTED_POLICY_RECEIPT_ID = "7f51bc70"
EXPECTED_SCALE_REVIEW_ID = "6539838c"
EXPECTED_SCALE_REVIEW_RECEIPT_ID = "0c85a6f1"
EXPECTED_CANDIDATE_PROBE_ID = "6a33c978"
EXPECTED_CANDIDATE_PROBE_RECEIPT_ID = "99c90fe3"
EXPECTED_V02_SCALE_PROBE_ID = "227e9426"

SCALE_OUT_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_SCALE_OUT_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
MODE = "OUTER_OBSERVER_ONLY"

SELECTED_ENCODING_ID = "raw_decimal_sig6"
TARGET_RAW_DELTA_FIELD = "compression_ratio"

CANDIDATE_PAYLOAD_FIELDS = [
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
    "microhash",
}

FORBIDDEN_AUTHORITY_TRUE = [
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
    "authorizes_case_id_or_cycle_n_primary_identity_patch",
    "authorizes_rowid_or_receipt_hash_patch",
    "authorizes_raw_receipt_hash_truth_surface",
    "authorizes_full_occurrence_key_in_payload",
    "authorizes_audit_pointer_in_payload",
    "authorizes_debug_payload_in_payload",
    "authorizes_microhash_as_proof",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def canonical_bytes(obj: Any) -> int:
    return len(blob(obj))


def sha8(obj: Any) -> str:
    return hashlib.sha256(blob(obj)).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"missing required jsonl: {path}")
    rows: list[dict[str, Any]] = []
    for i, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict):
            obj["_source_jsonl_line"] = i
            rows.append(obj)
    return rows


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def verify_policy(policy: dict[str, Any], policy_receipt: dict[str, Any], scale_review_receipt: dict[str, Any], candidate_probe_receipt: dict[str, Any]) -> list[str]:
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
    if policy.get("scale_out_name") != SCALE_OUT_NAME:
        failures.append(f"scale_out_name_wrong:{policy.get('scale_out_name')}")
    if policy.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"candidate_design_wrong:{policy.get('candidate_design_id')}")
    if policy.get("terminal", {}).get("next_command_goal") != "IMPLEMENT_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_SCALE_OUT_V0":
        failures.append(f"policy_next_goal_wrong:{policy.get('terminal', {}).get('next_command_goal')}")

    contract = policy.get("scale_out_contract") or {}
    if contract.get("scale_out_name") != SCALE_OUT_NAME:
        failures.append(f"contract_scale_out_name_wrong:{contract.get('scale_out_name')}")
    if contract.get("scale_out_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"contract_status_wrong:{contract.get('scale_out_status')}")
    if contract.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"contract_candidate_design_wrong:{contract.get('candidate_design_id')}")
    if contract.get("selected_encoding_id") != SELECTED_ENCODING_ID:
        failures.append(f"contract_encoding_wrong:{contract.get('selected_encoding_id')}")
    if contract.get("selected_target_raw_delta_field") != TARGET_RAW_DELTA_FIELD:
        failures.append(f"contract_target_wrong:{contract.get('selected_target_raw_delta_field')}")
    if contract.get("candidate_payload_fields") != CANDIDATE_PAYLOAD_FIELDS:
        failures.append(f"contract_payload_wrong:{contract.get('candidate_payload_fields')}")
    if contract.get("truth_surface") != "full_occurrence_key_to_candidate_delta_signature":
        failures.append(f"contract_truth_surface_wrong:{contract.get('truth_surface')}")

    selection = contract.get("scale_out_selection_rule") or {}
    if selection.get("must_include_prior_candidate_probe_rows_path") != "data/raw_delta_signature_candidate_probe_rows/6a33c978.jsonl":
        failures.append(f"prior_rows_path_wrong:{selection.get('must_include_prior_candidate_probe_rows_path')}")
    if selection.get("must_include_prior_bands_total") != 266:
        failures.append(f"prior_bands_total_wrong:{selection.get('must_include_prior_bands_total')}")
    if selection.get("must_include_prior_selected_rows_total") != 3298:
        failures.append(f"prior_selected_rows_total_wrong:{selection.get('must_include_prior_selected_rows_total')}")
    if selection.get("must_add_new_validation_surface") is not True:
        failures.append("must_add_new_validation_surface_not_true")
    if selection.get("new_surface_must_be_file_backed_existing_artifacts") is not True:
        failures.append("new_surface_file_backed_not_true")
    if selection.get("must_stop_if_no_additional_bounded_inventory") != "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY":
        failures.append(f"hold_class_wrong:{selection.get('must_stop_if_no_additional_bounded_inventory')}")
    if selection.get("max_additional_candidate_rows") != 10000:
        failures.append(f"max_rows_wrong:{selection.get('max_additional_candidate_rows')}")
    if selection.get("max_additional_bands") != 512:
        failures.append(f"max_bands_wrong:{selection.get('max_additional_bands')}")
    if selection.get("max_additional_source_files") != 64:
        failures.append(f"max_files_wrong:{selection.get('max_additional_source_files')}")
    for key in [
        "must_record_inventory_summary",
        "must_record_selected_inventory_paths",
        "must_record_excluded_inventory_paths_or_counts",
        "must_not_read_registry_sqlite",
        "must_not_full_registry_scan",
        "must_not_accept_candidate",
        "must_not_authorize_scale_mode",
        "must_not_change_runtime",
        "must_not_write_registry",
    ]:
        if selection.get(key) is not True:
            failures.append(f"selection_flag_not_true:{key}:{selection.get(key)}")

    auth = policy.get("authority") or {}
    if auth.get("observer_only") is not True:
        failures.append("policy_not_observer_only")
    if auth.get("authorizes_next_bounded_scale_out_implementation") is not True:
        failures.append("next_scale_out_not_authorized")
    if auth.get("authorizes_bounded_file_backed_inventory_inspection") is not True:
        failures.append("bounded_inventory_not_authorized")
    if auth.get("authorizes_bounded_candidate_scale_out_execution") is not True:
        failures.append("bounded_candidate_scale_out_not_authorized")
    for key in FORBIDDEN_AUTHORITY_TRUE:
        if auth.get(key) is not False:
            failures.append(f"illegal_authority:{key}:{auth.get(key)}")

    constraints = policy.get("implementation_constraints") or {}
    if constraints.get("must_touch_only_files") != ["scripts/raw_delta_signature_candidate_bounded_scale_out_v0.py"]:
        failures.append(f"touch_scope_wrong:{constraints.get('must_touch_only_files')}")
    for key in [
        "must_reuse_existing_receipts_and_rows",
        "must_include_prior_266_band_surface",
        "must_define_inventory_before_evaluating",
        "must_not_read_registry_sqlite",
        "must_not_full_registry_scan",
        "must_not_accept_candidate",
        "must_not_authorize_scale_mode",
        "must_not_change_runtime_receipt_emission",
        "must_not_write_registry",
    ]:
        if constraints.get(key) is not True:
            failures.append(f"constraint_not_true:{key}:{constraints.get(key)}")

    if scale_review_receipt.get("review_id") != EXPECTED_SCALE_REVIEW_ID:
        failures.append(f"scale_review_id_wrong:{scale_review_receipt.get('review_id')}")
    if scale_review_receipt.get("receipt_id") != EXPECTED_SCALE_REVIEW_RECEIPT_ID:
        failures.append(f"scale_review_receipt_id_wrong:{scale_review_receipt.get('receipt_id')}")
    if scale_review_receipt.get("gate") != "PASS":
        failures.append(f"scale_review_gate_not_PASS:{scale_review_receipt.get('gate')}")
    if scale_review_receipt.get("terminal_class") != "ADVANCE_TO_BOUNDED_SCALE_OUT_POLICY":
        failures.append(f"scale_review_terminal_wrong:{scale_review_receipt.get('terminal_class')}")

    if candidate_probe_receipt.get("probe_id") != EXPECTED_CANDIDATE_PROBE_ID:
        failures.append(f"candidate_probe_id_wrong:{candidate_probe_receipt.get('probe_id')}")
    if candidate_probe_receipt.get("receipt_id") != EXPECTED_CANDIDATE_PROBE_RECEIPT_ID:
        failures.append(f"candidate_probe_receipt_id_wrong:{candidate_probe_receipt.get('receipt_id')}")
    if candidate_probe_receipt.get("gate") != "PASS":
        failures.append(f"candidate_probe_gate_not_PASS:{candidate_probe_receipt.get('gate')}")
    if candidate_probe_receipt.get("terminal_decision") != "PASS_RAW_DELTA_SIGNATURE_CANDIDATE_BOUNDED_PROBE":
        failures.append(f"candidate_probe_terminal_wrong:{candidate_probe_receipt.get('terminal_decision')}")

    source_evidence = contract.get("source_bounded_pass_evidence") or {}
    if source_evidence.get("bands_total") != 266 or source_evidence.get("bands_passed") != 266 or source_evidence.get("bands_failed") != 0:
        failures.append(f"source_bounded_bands_wrong:{source_evidence}")
    if source_evidence.get("all_band_false_merge_count") != 0:
        failures.append(f"source_bounded_false_merges_wrong:{source_evidence.get('all_band_false_merge_count')}")
    if source_evidence.get("worst_distinguishability_retention_ratio") != 1.0:
        failures.append(f"source_bounded_retention_wrong:{source_evidence.get('worst_distinguishability_retention_ratio')}")
    if not (source_evidence.get("total_burden_ratio_projected", 999) < 1.0):
        failures.append(f"source_bounded_burden_wrong:{source_evidence.get('total_burden_ratio_projected')}")
    if source_evidence.get("identity_leak_count") != 0:
        failures.append(f"source_bounded_identity_leak_wrong:{source_evidence.get('identity_leak_count')}")
    if source_evidence.get("source_surface_regression_count") != 0:
        failures.append(f"source_bounded_surface_regression_wrong:{source_evidence.get('source_surface_regression_count')}")

    return failures


def payload_has_identity_leak(payload: dict[str, Any]) -> bool:
    text = json.dumps(payload, sort_keys=True, default=str).lower()
    return any(k.lower() in text for k in FORBIDDEN_PAYLOAD_KEYS)


def candidate_signature(payload: dict[str, Any]) -> str:
    return sha8(payload)


def validate_candidate_payload(payload: dict[str, Any]) -> bool:
    if set(payload.keys()) != set(CANDIDATE_PAYLOAD_FIELDS):
        return False
    if payload.get("cv") != "raw_delta_signature_v0":
        return False
    if payload.get("raw_compression_ratio_sig6") in (None, ""):
        return False
    if payload_has_identity_leak(payload):
        return False
    return True


def row_to_candidate(row: dict[str, Any], source_path: Path) -> tuple[dict[str, Any] | None, str | None]:
    # Already projected candidate row.
    if row.get("candidate_design_id") == CANDIDATE_DESIGN_ID and isinstance(row.get("signature_payload"), dict):
        payload = row["signature_payload"]
        if not validate_candidate_payload(payload):
            return None, "invalid_candidate_payload"
        full_key = row.get("full_occurrence_key")
        band_id = row.get("source_band_id")
        if not full_key or not band_id:
            return None, "missing_truth_or_band"
        return {
            "source_path": rel(source_path),
            "source_line": row.get("_source_jsonl_line"),
            "source_kind": "candidate_probe_row",
            "source_band_id": str(band_id),
            "full_occurrence_key": str(full_key),
            "candidate_delta_signature": candidate_signature(payload),
            "signature_payload": payload,
            "signature_payload_bytes": canonical_bytes(payload),
            "projected_scale_row_bytes": canonical_bytes({
                "candidate_delta_signature": candidate_signature(payload),
                "source_band_id": str(band_id),
                "source_path": rel(source_path),
                "source_line": row.get("_source_jsonl_line"),
            }),
        }, None

    # Raw-delta compactness diagnostic row for selected encoding.
    if row.get("encoding_id") == SELECTED_ENCODING_ID and isinstance(row.get("signature_payload"), dict):
        source_payload = row.get("signature_payload") or {}
        raw_enc = source_payload.get("raw_delta_encoding") or {}
        if raw_enc.get("target_field") != TARGET_RAW_DELTA_FIELD:
            return None, "wrong_target_field"
        if raw_enc.get("encoding_id") != SELECTED_ENCODING_ID:
            return None, "wrong_encoding"
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
        if not validate_candidate_payload(payload):
            return None, "invalid_candidate_payload"

        full_key = row.get("full_occurrence_key")
        band_id = row.get("source_band_id")
        if not full_key or not band_id:
            return None, "missing_truth_or_band"

        return {
            "source_path": rel(source_path),
            "source_line": row.get("_source_jsonl_line"),
            "source_kind": "raw_delta_compactness_row",
            "source_band_id": str(band_id),
            "full_occurrence_key": str(full_key),
            "candidate_delta_signature": candidate_signature(payload),
            "signature_payload": payload,
            "signature_payload_bytes": canonical_bytes(payload),
            "projected_scale_row_bytes": canonical_bytes({
                "candidate_delta_signature": candidate_signature(payload),
                "source_band_id": str(band_id),
                "source_path": rel(source_path),
                "source_line": row.get("_source_jsonl_line"),
            }),
        }, None

    return None, "not_candidate_surface"


def excluded_path(path: Path, explicit_exclusions: list[str]) -> str | None:
    rp = rel(path)
    for pattern in explicit_exclusions:
        if pattern.endswith("/"):
            if pattern.rstrip("/") in rp.split("/"):
                return pattern
        elif fnmatch.fnmatch(rp, pattern):
            return pattern

    if path.suffix in {".sqlite", ".db"}:
        return "suffix_sqlite_or_db"
    if "registry.sqlite" in rp or "registry.db" in rp:
        return "registry_file"

    return None


def inventory_files(policy: dict[str, Any]) -> tuple[list[Path], dict[str, Any]]:
    selection = policy["scale_out_contract"]["scale_out_selection_rule"]
    roots = [ROOT / root for root in selection["allowed_inventory_roots"]]
    explicit_exclusions = selection["explicit_exclusions"]
    max_files = selection["max_additional_source_files"]

    candidates: list[Path] = []
    excluded_counts: Counter[str] = Counter()
    seen: set[str] = set()

    for root in roots:
        if not root.exists():
            excluded_counts["root_missing"] += 1
            continue
        for path in sorted(root.rglob("*")):
            if not path.is_file():
                continue
            rp = rel(path)
            if rp in seen:
                continue
            seen.add(rp)

            reason = excluded_path(path, explicit_exclusions)
            if reason:
                excluded_counts[reason] += 1
                continue

            if not (path.suffix == ".jsonl" or path.suffix == ".json"):
                excluded_counts["unsupported_suffix"] += 1
                continue

            # Avoid consuming own future outputs as input inventory.
            if "raw_delta_signature_candidate_bounded_scale_out" in rp:
                excluded_counts["own_scale_out_output"] += 1
                continue

            candidates.append(path)

    candidates = sorted(candidates, key=lambda p: (p.suffix, rel(p)))[:max_files]

    summary = {
        "allowed_roots": selection["allowed_inventory_roots"],
        "candidate_files_total_after_exclusions": len(candidates),
        "candidate_files_considered_limit": max_files,
        "selected_inventory_paths": [rel(p) for p in candidates],
        "excluded_counts": dict(excluded_counts),
        "registry_sqlite_read": False,
        "full_registry_scan_used": False,
    }
    return candidates, summary


def load_prior_rows(policy: dict[str, Any]) -> tuple[list[dict[str, Any]], str]:
    prior_path = ROOT / policy["scale_out_contract"]["scale_out_selection_rule"]["must_include_prior_candidate_probe_rows_path"]
    rows = load_jsonl(prior_path)
    projected: list[dict[str, Any]] = []
    failures = Counter()
    for row in rows:
        candidate, failure = row_to_candidate(row, prior_path)
        if candidate is None:
            failures[failure or "unknown"] += 1
            continue
        candidate["surface_role"] = "prior_266_band_replay"
        projected.append(candidate)

    if len(projected) != 3298:
        raise SystemExit(f"prior rows replay count mismatch: {len(projected)} expected 3298 failures={dict(failures)}")

    return projected, rel(prior_path)


def evaluate_rows(rows: list[dict[str, Any]], full_receipt_bytes_by_band: dict[str, int]) -> dict[str, Any]:
    by_band: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        by_band[row["source_band_id"]].append(row)

    band_measurements: list[dict[str, Any]] = []
    failure_counts = Counter()

    for band_id, band_rows in sorted(by_band.items()):
        sig_to_full: dict[str, set[str]] = defaultdict(set)
        full_to_sig: dict[str, set[str]] = defaultdict(set)
        payload_bytes = 0
        projected_bytes = 0
        identity_leak_count = 0
        audit_recoverability_failures = 0

        for row in band_rows:
            payload = row["signature_payload"]
            if payload_has_identity_leak(payload):
                identity_leak_count += 1
            sig_to_full[row["candidate_delta_signature"]].add(row["full_occurrence_key"])
            full_to_sig[row["full_occurrence_key"]].add(row["candidate_delta_signature"])
            payload_bytes += int(row.get("signature_payload_bytes") or canonical_bytes(payload))
            projected_bytes += int(row.get("projected_scale_row_bytes") or 0)
            if not row.get("source_path") or row.get("source_line") is None:
                audit_recoverability_failures += 1

        collision_groups = {sig: keys for sig, keys in sig_to_full.items() if len(keys) > 1}
        false_split_groups = {key: sigs for key, sigs in full_to_sig.items() if len(sigs) > 1}

        full_receipt_bytes = full_receipt_bytes_by_band.get(band_id, 0)
        source_surface_regression_count = 0 if full_receipt_bytes > 0 else 1
        if source_surface_regression_count:
            failure_counts["missing_full_receipt_bytes"] += 1

        projected_plus_payload = payload_bytes + projected_bytes
        burden_ratio = projected_plus_payload / full_receipt_bytes if full_receipt_bytes else 0.0
        retention = len(sig_to_full) / len(full_to_sig) if full_to_sig else 0.0

        band_passed = (
            identity_leak_count == 0
            and audit_recoverability_failures == 0
            and len(collision_groups) == 0
            and len(false_split_groups) == 0
            and source_surface_regression_count == 0
            and burden_ratio < 1.0
        )

        band_measurements.append({
            "band_id": band_id,
            "rows_total": len(band_rows),
            "distinct_full_occurrence_keys": len(full_to_sig),
            "distinct_candidate_signatures": len(sig_to_full),
            "false_merge_count": len(collision_groups),
            "false_split_count": len(false_split_groups),
            "collision_count": len(collision_groups),
            "distinguishability_retention_ratio": retention,
            "signature_payload_bytes": payload_bytes,
            "projected_scale_row_bytes": projected_bytes,
            "projected_plus_signature_payload_bytes": projected_plus_payload,
            "full_receipt_bytes": full_receipt_bytes,
            "burden_ratio_projected": burden_ratio,
            "identity_leak_count": identity_leak_count,
            "source_surface_regression_count": source_surface_regression_count,
            "audit_recoverability_failures": audit_recoverability_failures,
            "band_passed": band_passed,
            "failure_reasons": [
                name for name, cond in [
                    ("identity_leak", identity_leak_count > 0),
                    ("audit_recoverability", audit_recoverability_failures > 0),
                    ("false_merge", len(collision_groups) > 0),
                    ("false_split", len(false_split_groups) > 0),
                    ("source_surface", source_surface_regression_count > 0),
                    ("burden", full_receipt_bytes <= 0 or burden_ratio >= 1.0),
                ] if cond
            ],
            "collision_gallery": [
                {
                    "candidate_delta_signature": sig,
                    "distinct_full_occurrence_keys": len(keys),
                    "full_occurrence_keys": sorted(keys)[:20],
                }
                for sig, keys in sorted(collision_groups.items(), key=lambda kv: (-len(kv[1]), kv[0]))[:10]
            ],
        })

    total_full = sum(m["full_receipt_bytes"] for m in band_measurements)
    total_payload = sum(m["signature_payload_bytes"] for m in band_measurements)
    total_projected = sum(m["projected_scale_row_bytes"] for m in band_measurements)
    total_projected_plus_payload = sum(m["projected_plus_signature_payload_bytes"] for m in band_measurements)

    aggregate = {
        "bands_total": len(band_measurements),
        "bands_passed": sum(1 for m in band_measurements if m["band_passed"]),
        "bands_failed": sum(1 for m in band_measurements if not m["band_passed"]),
        "rows_total": len(rows),
        "all_band_false_merge_count": sum(1 for m in band_measurements if m["false_merge_count"] > 0),
        "all_band_false_split_count": sum(1 for m in band_measurements if m["false_split_count"] > 0),
        "all_band_burden_regression_count": sum(1 for m in band_measurements if m["burden_ratio_projected"] >= 1.0 or m["full_receipt_bytes"] <= 0),
        "worst_false_merge_count": max((m["false_merge_count"] for m in band_measurements), default=0),
        "worst_false_split_count": max((m["false_split_count"] for m in band_measurements), default=0),
        "worst_collision_count": max((m["collision_count"] for m in band_measurements), default=0),
        "worst_distinguishability_retention_ratio": min((m["distinguishability_retention_ratio"] for m in band_measurements), default=0.0),
        "worst_burden_ratio_projected": max((m["burden_ratio_projected"] for m in band_measurements), default=0.0),
        "worst_identity_leak_count": max((m["identity_leak_count"] for m in band_measurements), default=0),
        "worst_source_surface_regression_count": max((m["source_surface_regression_count"] for m in band_measurements), default=0),
        "worst_audit_recoverability_failures": max((m["audit_recoverability_failures"] for m in band_measurements), default=0),
        "total_full_receipt_bytes": total_full,
        "total_signature_payload_bytes": total_payload,
        "total_projected_scale_row_bytes": total_projected,
        "total_projected_plus_signature_payload_bytes": total_projected_plus_payload,
        "total_burden_ratio_projected": total_projected_plus_payload / total_full if total_full else 0.0,
    }

    return {
        "aggregate": aggregate,
        "band_measurements": band_measurements,
        "failure_counts": dict(failure_counts),
    }


def full_receipt_bytes_map() -> dict[str, int]:
    v02 = load_json(V02_SCALE_RECEIPT_DIR / f"{EXPECTED_V02_SCALE_PROBE_ID}.json")
    out: dict[str, int] = {}
    for band in v02.get("band_measurements", []):
        band_id = band.get("band_id")
        full = band.get("full_receipt_bytes")
        if band_id and isinstance(full, int) and full > 0:
            out[str(band_id)] = int(full)
    return out


def run_scale_out(policy_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    start = time.perf_counter()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_ROWS_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")
    scale_review_receipt = load_json(SCALE_REVIEW_RECEIPT_DIR / f"{EXPECTED_SCALE_REVIEW_ID}.json")
    candidate_probe_receipt = load_json(CANDIDATE_PROBE_RECEIPT_DIR / f"{EXPECTED_CANDIDATE_PROBE_ID}.json")

    policy_failures = verify_policy(policy, policy_receipt, scale_review_receipt, candidate_probe_receipt)

    prior_rows, prior_path = load_prior_rows(policy)
    prior_band_ids = {row["source_band_id"] for row in prior_rows}
    prior_row_keys = {(row["source_band_id"], row["full_occurrence_key"], row["candidate_delta_signature"]) for row in prior_rows}

    files, inventory_summary = inventory_files(policy)
    selection = policy["scale_out_contract"]["scale_out_selection_rule"]

    candidate_rows_by_file: dict[str, int] = {}
    rejected_candidate_surface_counts: Counter[str] = Counter()
    additional_rows: list[dict[str, Any]] = []

    for path in files:
        if rel(path) == prior_path:
            inventory_summary.setdefault("skipped_paths", {})[rel(path)] = "prior_candidate_probe_rows"
            continue
        if path.suffix != ".jsonl":
            continue

        rows = load_jsonl(path)
        selected_from_file = 0
        for row in rows:
            candidate, failure = row_to_candidate(row, path)
            if candidate is None:
                rejected_candidate_surface_counts[failure or "unknown"] += 1
                continue

            row_key = (candidate["source_band_id"], candidate["full_occurrence_key"], candidate["candidate_delta_signature"])
            if row_key in prior_row_keys:
                rejected_candidate_surface_counts["duplicate_of_prior_surface"] += 1
                continue

            # A new validation surface must add at least one new band, not merely duplicate the prior 266-band band IDs.
            if candidate["source_band_id"] in prior_band_ids:
                rejected_candidate_surface_counts["same_prior_band_not_new_surface"] += 1
                continue

            candidate["surface_role"] = "additional_bounded_file_backed_surface"
            additional_rows.append(candidate)
            selected_from_file += 1

            if len(additional_rows) >= selection["max_additional_candidate_rows"]:
                break

        if selected_from_file:
            candidate_rows_by_file[rel(path)] = selected_from_file

        if len(additional_rows) >= selection["max_additional_candidate_rows"]:
            break

    # Enforce band/file limits deterministically.
    additional_by_band: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in additional_rows:
        additional_by_band[row["source_band_id"]].append(row)

    selected_additional_band_ids = sorted(additional_by_band)[: selection["max_additional_bands"]]
    selected_additional_rows: list[dict[str, Any]] = []
    for band_id in selected_additional_band_ids:
        selected_additional_rows.extend(additional_by_band[band_id])

    full_by_band = full_receipt_bytes_map()

    prior_eval = evaluate_rows(prior_rows, full_by_band)
    combined_rows = prior_rows + selected_additional_rows
    combined_eval = evaluate_rows(combined_rows, full_by_band)

    additional_inventory_selected = len(selected_additional_rows) > 0
    new_bands_evaluated = len(set(row["source_band_id"] for row in selected_additional_rows))

    if policy_failures:
        terminal_class = "FAIL_BOUNDED_SCALE_OUT_AUTHORITY"
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": terminal_class}
    elif prior_eval["aggregate"]["bands_total"] != 266 or prior_eval["aggregate"]["bands_failed"] != 0:
        terminal_class = "FAIL_BOUNDED_SCALE_OUT_SOURCE_SURFACE"
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": terminal_class}
    elif not additional_inventory_selected:
        terminal_class = "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY"
        terminal = {"type": "HOLD", "next_command_goal": None, "stop_code": terminal_class}
    elif combined_eval["aggregate"]["worst_identity_leak_count"] > 0:
        terminal_class = "FAIL_BOUNDED_SCALE_OUT_AUTHORITY"
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": terminal_class}
    elif combined_eval["aggregate"]["all_band_false_merge_count"] > 0:
        terminal_class = "FAIL_BOUNDED_SCALE_OUT_FALSE_MERGE"
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": terminal_class}
    elif combined_eval["aggregate"]["all_band_false_split_count"] > 0:
        terminal_class = "FAIL_BOUNDED_SCALE_OUT_FALSE_SPLIT"
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": terminal_class}
    elif combined_eval["aggregate"]["worst_source_surface_regression_count"] > 0:
        terminal_class = "FAIL_BOUNDED_SCALE_OUT_SOURCE_SURFACE"
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": terminal_class}
    elif combined_eval["aggregate"]["all_band_burden_regression_count"] > 0:
        terminal_class = "FAIL_BOUNDED_SCALE_OUT_BURDEN"
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": terminal_class}
    else:
        terminal_class = "PASS_BOUNDED_SCALE_OUT_CLEAN"
        terminal = {
            "type": "ADVANCE",
            "next_command_goal": "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_POST_SCALE_OUT_REVIEW_POLICY_V0",
            "stop_code": None,
        }

    authority_guards = {
        "observer_only": True,
        "candidate_accepted": False,
        "candidate_acceptance_authorized": False,
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

    pass_gates = {
        "policy_preconditions": not policy_failures,
        "authority_containment": all([
            authority_guards["observer_only"] is True,
            authority_guards["candidate_accepted"] is False,
            authority_guards["candidate_acceptance_authorized"] is False,
            authority_guards["scale_mode_authorized"] is False,
            authority_guards["full_registry_scan_used"] is False,
            authority_guards["registry_sqlite_read"] is False,
            authority_guards["runtime_receipt_emission_changed"] is False,
            authority_guards["registry_write_authorized"] is False,
        ]),
        "inventory_defined_before_evaluation": True,
        "prior_266_band_surface_replayed": prior_eval["aggregate"]["bands_total"] == 266 and prior_eval["aggregate"]["bands_failed"] == 0,
        "larger_surface_or_hold": additional_inventory_selected or terminal_class == "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY",
        "truth_surface": True,
        "no_identity_leak": combined_eval["aggregate"]["worst_identity_leak_count"] == 0,
        "no_false_merge": combined_eval["aggregate"]["all_band_false_merge_count"] == 0,
        "no_false_split": combined_eval["aggregate"]["all_band_false_split_count"] == 0,
        "burden_reduction_or_hold": terminal_class == "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY" or combined_eval["aggregate"]["all_band_burden_regression_count"] == 0,
        "source_surface_clean_or_hold": terminal_class == "HOLD_NO_ADDITIONAL_BOUNDED_INVENTORY" or combined_eval["aggregate"]["worst_source_surface_regression_count"] == 0,
        "candidate_not_accepted": True,
        "scale_mode_not_authorized": True,
    }

    elapsed_ms = int(round((time.perf_counter() - start) * 1000))

    out_rows = []
    for row in combined_rows:
        r = dict(row)
        r["candidate_payload_forbidden_fields_present"] = False
        r["truth_surface"] = {
            "primary_comparison": "full_occurrence_key_to_candidate_delta_signature",
            "raw_full_receipt_hash_used_as_truth_surface": False,
            "full_receipt_hash_compared_to_delta_signature": False,
        }
        out_rows.append(r)

    scale_out = {
        "schema_version": "raw_delta_signature_candidate_bounded_scale_out_v0",
        "scale_out_name": SCALE_OUT_NAME,
        "mode": MODE,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_scale_review_id": EXPECTED_SCALE_REVIEW_ID,
        "source_scale_review_receipt_id": EXPECTED_SCALE_REVIEW_RECEIPT_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "source_candidate_probe_receipt_id": EXPECTED_CANDIDATE_PROBE_RECEIPT_ID,
        "selected_encoding_id": SELECTED_ENCODING_ID,
        "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
        "candidate_payload_fields": CANDIDATE_PAYLOAD_FIELDS,
        "inventory_summary": inventory_summary | {
            "candidate_rows_by_file": candidate_rows_by_file,
            "rejected_candidate_surface_counts": dict(rejected_candidate_surface_counts),
            "additional_candidate_rows_selected": len(selected_additional_rows),
            "additional_bands_selected": new_bands_evaluated,
            "prior_candidate_rows_replayed": len(prior_rows),
            "prior_bands_replayed": len(prior_band_ids),
        },
        "prior_surface_evaluation": prior_eval,
        "additional_surface_summary": {
            "additional_inventory_selected": additional_inventory_selected,
            "additional_candidate_rows_selected": len(selected_additional_rows),
            "new_bands_evaluated": new_bands_evaluated,
            "selected_additional_band_ids": selected_additional_band_ids,
        },
        "combined_surface_evaluation": combined_eval,
        "authority_guards": authority_guards,
        "pass_gates": pass_gates,
        "decision": {
            "candidate_accepted": False,
            "candidate_acceptance_authorized": False,
            "scale_mode_authorized": False,
            "bounded_scale_out_only": True,
            "do_not_accept_candidate": True,
            "do_not_full_registry_scan": True,
            "do_not_read_registry_sqlite": True,
            "do_not_change_runtime": True,
            "do_not_write_registry": True,
            "do_not_use_case_id_or_cycle_n_as_primary_identity": True,
            "do_not_use_rowid_or_receipt_hash": True,
            "terminal_class": terminal_class,
            "additional_inventory_selected": additional_inventory_selected,
        },
        "terminal_class": terminal_class,
        "terminal": terminal,
        "gate": "PASS" if not policy_failures else "FAIL",
        "failures": policy_failures,
        "warnings": [],
        "created_at": now_iso(),
        "actual_observer_overhead_ms": elapsed_ms,
    }

    scale_out_id = sha8({
        "scale_out_name": SCALE_OUT_NAME,
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_scale_review_id": EXPECTED_SCALE_REVIEW_ID,
        "terminal_class": terminal_class,
        "inventory_summary": scale_out["inventory_summary"],
        "prior_aggregate": prior_eval["aggregate"],
        "combined_aggregate": combined_eval["aggregate"],
    })
    scale_out["scale_out_id"] = scale_out_id
    scale_out["scale_out_sig8"] = scale_out_id
    scale_out["scale_out_rows_path"] = f"data/raw_delta_signature_candidate_bounded_scale_out_rows/{scale_out_id}.jsonl"

    rows_path = OUT_ROWS_DIR / f"{scale_out_id}.jsonl"
    with rows_path.open("w") as f:
        for row in out_rows:
            f.write(json.dumps(row, sort_keys=True, default=str) + "\n")

    receipt = {
        "schema_version": "raw_delta_signature_candidate_bounded_scale_out_receipt_v0",
        "scale_out_id": scale_out_id,
        "scale_out_sig8": scale_out_id,
        "scale_out_name": SCALE_OUT_NAME,
        "mode": MODE,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "scale_out_path": f"data/raw_delta_signature_candidate_bounded_scale_outs/{scale_out_id}.json",
        "scale_out_rows_path": scale_out["scale_out_rows_path"],
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_scale_review_id": EXPECTED_SCALE_REVIEW_ID,
        "source_scale_review_receipt_id": EXPECTED_SCALE_REVIEW_RECEIPT_ID,
        "source_candidate_probe_id": EXPECTED_CANDIDATE_PROBE_ID,
        "source_candidate_probe_receipt_id": EXPECTED_CANDIDATE_PROBE_RECEIPT_ID,
        "selected_encoding_id": SELECTED_ENCODING_ID,
        "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
        "candidate_payload_fields": CANDIDATE_PAYLOAD_FIELDS,
        "inventory_summary": scale_out["inventory_summary"],
        "prior_surface_aggregate": prior_eval["aggregate"],
        "additional_surface_summary": scale_out["additional_surface_summary"],
        "combined_surface_aggregate": combined_eval["aggregate"],
        "authority_guards": authority_guards,
        "pass_gates": pass_gates,
        "decision": scale_out["decision"],
        "terminal_class": terminal_class,
        "terminal": terminal,
        "gate": scale_out["gate"],
        "failures": policy_failures,
        "warnings": [],
        "created_at": now_iso(),
        "actual_observer_overhead_ms": elapsed_ms,
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    (OUT_DIR / f"{scale_out_id}.json").write_text(json.dumps(scale_out, indent=2, sort_keys=True))
    (OUT_RECEIPT_DIR / f"{scale_out_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return scale_out, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-id", default=EXPECTED_POLICY_ID)
    args = parser.parse_args()

    scale_out, receipt = run_scale_out(args.policy_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"scale_out_id={scale_out['scale_out_id']}")
    print(f"scale_out_json_path=data/raw_delta_signature_candidate_bounded_scale_outs/{scale_out['scale_out_id']}.json")
    print(f"scale_out_receipt_path=data/raw_delta_signature_candidate_bounded_scale_out_receipts/{scale_out['scale_out_id']}.json")
    print(f"scale_out_rows_path={scale_out['scale_out_rows_path']}")

    return 0 if scale_out["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
