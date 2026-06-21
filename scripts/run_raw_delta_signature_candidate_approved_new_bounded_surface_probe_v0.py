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

PROBE_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_PROBE_V0"
POLICY_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_PROBE_POLICY_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"

EXPECTED_POLICY_ID = "a4e4d744"
EXPECTED_POLICY_RECEIPT_ID = "9061c1fb"
SOURCE_SURFACE_ID = "4427ba4b"
SOURCE_SURFACE_RECEIPT_ID = "e5022cd2"
SOURCE_RUN_ID = "run_20260621_183812_136149"

POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_probe_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_probe_policy_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_probe_results"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_probe_receipts"

REQUIRED_PAYLOAD_FIELDS = [
    "cv",
    "state_hash_before",
    "move_id",
    "state_hash_after",
    "raw_compression_ratio_sig6",
]

FORBIDDEN_PAYLOAD_FIELDS = [
    "case_id",
    "cycle_n",
    "rowid",
    "receipt_hash",
    "receipt_path",
    "audit_pointer",
    "debug_payload",
    "full_occurrence_key",
    "registry_rowid",
]

FORBIDDEN_AUTHORITY_TRUE = [
    "runner_executed",
    "candidate_accepted",
    "scale_mode_authorized",
    "registry_inserted",
    "registry_written",
    "registry_sqlite_read",
    "full_registry_scan_used",
    "runtime_semantic_changed",
    "runtime_code_changed",
    "runtime_receipt_emission_changed",
    "latest_or_mtime_selection_used",
    "ambient_workspace_inference_used",
    "case_id_or_cycle_n_identity_patch_used",
    "rowid_or_receipt_hash_truth_surface_used",
    "full_occurrence_key_in_signature_payload",
    "audit_or_debug_payload_in_signature_payload",
    "microhash_as_proof_used",
    "synthetic_fake_validation_rows_used",
]

NEXT_REVIEW_GOAL = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_REVIEW_POLICY_V0"
NEXT_DIAGNOSTIC_GOAL = "DIAGNOSE_RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_PROBE_FAILURE_V0"


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def sha8(obj: Any) -> str:
    return hashlib.sha256(blob(obj)).hexdigest()[:8]


def rel(path: Path) -> str:
    try:
        return str(path.relative_to(ROOT))
    except ValueError:
        return str(path)


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing json: {path}")
    return json.loads(path.read_text())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"missing jsonl: {path}")
    rows: list[dict[str, Any]] = []
    for i, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        obj = json.loads(line)
        if not isinstance(obj, dict):
            raise SystemExit(f"jsonl row {i} in {path} is not object")
        rows.append(obj)
    return rows


def stable_json_key(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":"))


def validate_policy(policy: dict[str, Any], policy_receipt: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy.get("policy_receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if policy_receipt.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_receipt_policy_id_wrong:{policy_receipt.get('policy_id')}")
    if policy_receipt.get("receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy_receipt.get('receipt_id')}")

    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if policy_receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{policy_receipt.get('gate')}")
    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy.get('policy_status')}")
    if policy_receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_receipt_status_wrong:{policy_receipt.get('policy_status')}")

    terminal = policy.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != "RUN_RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_PROBE_V0":
        failures.append(f"policy_terminal_next_wrong:{terminal.get('next_command_goal')}")

    source = policy.get("source_surface") or {}
    if source.get("surface_id") != SOURCE_SURFACE_ID:
        failures.append(f"source_surface_id_wrong:{source.get('surface_id')}")
    if source.get("surface_receipt_id") != SOURCE_SURFACE_RECEIPT_ID:
        failures.append(f"source_surface_receipt_id_wrong:{source.get('surface_receipt_id')}")
    if source.get("source_run_id") != SOURCE_RUN_ID:
        failures.append(f"source_run_id_wrong:{source.get('source_run_id')}")

    contract = policy.get("probe_contract") or {}
    if contract.get("truth_surface") != "full_occurrence_key_to_candidate_delta_signature":
        failures.append(f"truth_surface_wrong:{contract.get('truth_surface')}")
    if contract.get("comparison") != "full_occurrence_key_to_candidate_delta_signature":
        failures.append(f"comparison_wrong:{contract.get('comparison')}")
    if contract.get("required_payload_fields") != REQUIRED_PAYLOAD_FIELDS:
        failures.append(f"required_payload_fields_wrong:{contract.get('required_payload_fields')}")
    if contract.get("required_candidate_version") != CANDIDATE_DESIGN_ID:
        failures.append(f"required_candidate_version_wrong:{contract.get('required_candidate_version')}")
    if contract.get("rows_expected") != 500:
        failures.append(f"rows_expected_wrong:{contract.get('rows_expected')}")

    allowed = policy.get("authorized_operations_next") or {}
    for key in [
        "read_source_surface_rows_file",
        "read_source_surface_manifest_file",
        "read_source_surface_receipt_file",
        "write_probe_result",
        "write_probe_receipt",
        "run_existing_candidate_probe_logic_on_fixed_surface",
    ]:
        if allowed.get(key) is not True:
            failures.append(f"authorized_next_not_true:{key}:{allowed.get(key)}")

    forbidden = policy.get("forbidden_operations") or {}
    for key, value in forbidden.items():
        if value is not True:
            failures.append(f"forbidden_operation_not_true:{key}:{value}")

    guards = policy_receipt.get("authority_guards") or {}
    for key in [
        "runner_executed",
        "candidate_rows_created",
        "candidate_accepted",
        "scale_mode_authorized",
        "registry_inserted",
        "registry_written",
        "registry_sqlite_read",
        "full_registry_scan_used",
        "runtime_semantic_changed",
        "runtime_code_changed",
        "runtime_receipt_emission_changed",
        "latest_or_mtime_selection_used",
        "ambient_workspace_inference_used",
        "case_id_or_cycle_n_identity_patch_used",
        "rowid_or_receipt_hash_truth_surface_used",
        "full_occurrence_key_in_signature_payload",
        "audit_or_debug_payload_in_signature_payload",
        "microhash_as_proof_used",
        "synthetic_fake_validation_rows_used",
        "transition_compression_probe_run",
    ]:
        if guards.get(key) is not False:
            failures.append(f"policy_receipt_authority_guard_not_false:{key}:{guards.get(key)}")

    return failures


def validate_source_files(policy: dict[str, Any], rows: list[dict[str, Any]], surface_manifest: dict[str, Any], surface_receipt: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if surface_manifest.get("surface_id") != SOURCE_SURFACE_ID:
        failures.append(f"surface_manifest_id_wrong:{surface_manifest.get('surface_id')}")
    if surface_manifest.get("gate") != "PASS":
        failures.append(f"surface_manifest_gate_not_PASS:{surface_manifest.get('gate')}")

    if surface_receipt.get("surface_id") != SOURCE_SURFACE_ID:
        failures.append(f"surface_receipt_id_wrong:{surface_receipt.get('surface_id')}")
    if surface_receipt.get("receipt_id") != SOURCE_SURFACE_RECEIPT_ID:
        failures.append(f"surface_receipt_receipt_id_wrong:{surface_receipt.get('receipt_id')}")
    if surface_receipt.get("gate") != "PASS":
        failures.append(f"surface_receipt_gate_not_PASS:{surface_receipt.get('gate')}")
    if surface_receipt.get("hold_code") is not None:
        failures.append(f"surface_receipt_hold_not_null:{surface_receipt.get('hold_code')}")
    if surface_receipt.get("rows_created") != 500:
        failures.append(f"surface_rows_created_wrong:{surface_receipt.get('rows_created')}")
    if surface_receipt.get("new_bands_created") != 500:
        failures.append(f"surface_new_bands_wrong:{surface_receipt.get('new_bands_created')}")
    if surface_receipt.get("candidate_signature_distinct_count") != 500:
        failures.append(f"surface_candidate_signature_distinct_count_wrong:{surface_receipt.get('candidate_signature_distinct_count')}")

    guards = surface_receipt.get("authority_guards") or {}
    for key in [
        "runner_executed",
        "candidate_accepted",
        "scale_mode_authorized",
        "registry_inserted",
        "registry_written",
        "registry_sqlite_read",
        "full_registry_scan_used",
        "runtime_semantic_changed",
        "runtime_code_changed",
        "runtime_receipt_emission_changed",
        "latest_or_mtime_selection_used",
        "ambient_workspace_inference_used",
        "case_id_or_cycle_n_identity_patch_used",
        "rowid_or_receipt_hash_truth_surface_used",
        "full_occurrence_key_in_signature_payload",
        "audit_or_debug_payload_in_signature_payload",
        "microhash_as_proof_used",
        "synthetic_fake_validation_rows_used",
        "transition_compression_probe_run",
    ]:
        if guards.get(key) is not False:
            failures.append(f"surface_authority_guard_not_false:{key}:{guards.get(key)}")

    if len(rows) != 500:
        failures.append(f"rows_total_wrong:{len(rows)}")

    return failures


def analyze_rows(rows: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[str] = []
    warnings: list[str] = []

    full_to_sigs: dict[str, set[str]] = defaultdict(set)
    sig_to_fulls: dict[str, set[str]] = defaultdict(set)
    sig_to_rows: dict[str, list[int]] = defaultdict(list)
    full_to_rows: dict[str, list[int]] = defaultdict(list)
    payload_shapes: Counter[str] = Counter()
    cv_values: Counter[str] = Counter()
    cv_sources: Counter[str] = Counter()

    payload_bytes = 0
    row_bytes = 0
    candidate_signature_payload_bytes = 0

    sample_rows = []
    violation_sample = []

    for idx, row in enumerate(rows):
        row_bytes += len(blob(row))
        payload = row.get("signature_payload")
        if not isinstance(payload, dict):
            failures.append(f"row[{idx}]:signature_payload_not_object")
            violation_sample.append({"row_index": idx, "issue": "signature_payload_not_object"})
            continue

        payload_bytes += len(blob(payload))
        candidate_signature_payload_bytes += len(blob({
            "candidate_delta_signature": row.get("candidate_delta_signature"),
            "signature_payload": payload,
        }))

        payload_shape = tuple(sorted(payload.keys()))
        payload_shapes[str(payload_shape)] += 1
        cv_values[str(payload.get("cv"))] += 1
        cv_sources[str(row.get("cv_source"))] += 1

        if set(payload.keys()) != set(REQUIRED_PAYLOAD_FIELDS):
            failures.append(f"row[{idx}]:payload_fields_wrong:{sorted(payload.keys())}")
            violation_sample.append({"row_index": idx, "issue": "payload_fields_wrong", "payload_keys": sorted(payload.keys())})

        for field in REQUIRED_PAYLOAD_FIELDS:
            if payload.get(field) is None or str(payload.get(field)) == "":
                failures.append(f"row[{idx}]:payload_field_empty:{field}")
                violation_sample.append({"row_index": idx, "issue": f"payload_field_empty:{field}"})

        for forbidden in FORBIDDEN_PAYLOAD_FIELDS:
            if forbidden in payload:
                failures.append(f"row[{idx}]:forbidden_payload_field:{forbidden}")
                violation_sample.append({"row_index": idx, "issue": f"forbidden_payload_field:{forbidden}"})

        if payload.get("cv") != CANDIDATE_DESIGN_ID:
            failures.append(f"row[{idx}]:cv_wrong:{payload.get('cv')}")
            violation_sample.append({"row_index": idx, "issue": "cv_wrong", "cv": payload.get("cv")})

        full_key = row.get("full_occurrence_key")
        sig = row.get("candidate_delta_signature")
        if not full_key:
            failures.append(f"row[{idx}]:missing_full_occurrence_key")
            violation_sample.append({"row_index": idx, "issue": "missing_full_occurrence_key"})
            continue
        if not sig:
            failures.append(f"row[{idx}]:missing_candidate_delta_signature")
            violation_sample.append({"row_index": idx, "issue": "missing_candidate_delta_signature"})
            continue

        full_key_s = stable_json_key(full_key)
        sig_s = str(sig)

        full_to_sigs[full_key_s].add(sig_s)
        sig_to_fulls[sig_s].add(full_key_s)
        sig_to_rows[sig_s].append(idx)
        full_to_rows[full_key_s].append(idx)

        if len(sample_rows) < 5:
            sample_rows.append({
                "row_index": idx,
                "candidate_delta_signature": sig_s,
                "full_occurrence_key": full_key,
                "signature_payload": payload,
                "cv_source": row.get("cv_source"),
            })

    false_merge_groups = {
        sig: sorted(list(fulls))
        for sig, fulls in sig_to_fulls.items()
        if len(fulls) > 1
    }
    false_split_groups = {
        full: sorted(list(sigs))
        for full, sigs in full_to_sigs.items()
        if len(sigs) > 1
    }

    distinct_full_occurrence_keys = len(full_to_sigs)
    distinct_candidate_signatures = len(sig_to_fulls)
    rows_total = len(rows)

    collision_count = len(false_merge_groups)
    false_merge_count = sum(len(fulls) - 1 for fulls in false_merge_groups.values())
    false_split_count = len(false_split_groups)

    retention = (
        distinct_candidate_signatures / distinct_full_occurrence_keys
        if distinct_full_occurrence_keys
        else 0.0
    )

    false_merge_sample = []
    for sig, fulls in list(false_merge_groups.items())[:10]:
        false_merge_sample.append({
            "candidate_delta_signature": sig,
            "distinct_full_occurrence_keys": len(fulls),
            "row_indices": sig_to_rows.get(sig, [])[:20],
            "full_occurrence_key_sample": [json.loads(v) for v in fulls[:3]],
        })

    false_split_sample = []
    for full, sigs in list(false_split_groups.items())[:10]:
        false_split_sample.append({
            "full_occurrence_key": json.loads(full),
            "distinct_candidate_delta_signatures": len(sigs),
            "row_indices": full_to_rows.get(full, [])[:20],
            "candidate_delta_signature_sample": sigs[:5],
        })

    if rows_total != 500:
        failures.append(f"rows_total_not_500:{rows_total}")
    if distinct_full_occurrence_keys != rows_total:
        failures.append(f"full_occurrence_keys_not_distinct:{distinct_full_occurrence_keys}/{rows_total}")
    if distinct_candidate_signatures != rows_total:
        failures.append(f"candidate_signatures_not_distinct:{distinct_candidate_signatures}/{rows_total}")
    if collision_count != 0:
        failures.append(f"collision_count_not_zero:{collision_count}")
    if false_merge_count != 0:
        failures.append(f"false_merge_count_not_zero:{false_merge_count}")
    if false_split_count != 0:
        failures.append(f"false_split_count_not_zero:{false_split_count}")
    if retention != 1.0:
        failures.append(f"retention_not_1:{retention}")

    return {
        "rows_total": rows_total,
        "distinct_full_occurrence_keys": distinct_full_occurrence_keys,
        "distinct_candidate_delta_signatures": distinct_candidate_signatures,
        "false_merge_count": false_merge_count,
        "collision_count": collision_count,
        "false_split_count": false_split_count,
        "retention": retention,
        "payload_shapes": dict(payload_shapes),
        "cv_values": dict(cv_values),
        "cv_sources": dict(cv_sources),
        "signature_payload_bytes": payload_bytes,
        "row_bytes": row_bytes,
        "candidate_signature_payload_bytes": candidate_signature_payload_bytes,
        "false_merge_sample": false_merge_sample,
        "false_split_sample": false_split_sample,
        "sample_rows": sample_rows,
        "violation_sample": violation_sample[:20],
        "failures": failures,
        "warnings": warnings,
    }


def build_probe(policy_id: str, write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    if policy_id != EXPECTED_POLICY_ID:
        raise SystemExit(f"unsupported policy_id for this fixed probe: {policy_id}")

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy_path = POLICY_DIR / f"{policy_id}.json"
    policy_receipt_path = POLICY_RECEIPT_DIR / f"{policy_id}.json"

    policy = load_json(policy_path)
    policy_receipt = load_json(policy_receipt_path)

    failures = validate_policy(policy, policy_receipt)

    contract = policy.get("probe_contract") or {}
    rows_path = ROOT / contract.get("allowed_input_rows_path", "")
    manifest_path = ROOT / contract.get("allowed_input_manifest_path", "")
    receipt_path = ROOT / contract.get("allowed_input_receipt_path", "")

    rows = load_jsonl(rows_path)
    source_manifest = load_json(manifest_path)
    source_receipt = load_json(receipt_path)

    failures.extend(validate_source_files(policy, rows, source_manifest, source_receipt))

    analysis = analyze_rows(rows)
    failures.extend(analysis["failures"])
    warnings = analysis["warnings"]

    source_rows_bytes_from_policy = policy_receipt.get("source_rows_bytes")
    signature_payload_bytes_from_policy = policy_receipt.get("signature_payload_bytes")

    source_rows_bytes = (
        int(source_rows_bytes_from_policy)
        if isinstance(source_rows_bytes_from_policy, int)
        else analysis["row_bytes"]
    )
    signature_payload_bytes = analysis["signature_payload_bytes"]

    burden_ratio_payload_to_source_rows = (
        signature_payload_bytes / source_rows_bytes
        if source_rows_bytes
        else None
    )
    burden_ratio_candidate_payload_to_source_rows = (
        analysis["candidate_signature_payload_bytes"] / source_rows_bytes
        if source_rows_bytes
        else None
    )

    pass_conditions = {
        "rows_equal_500": analysis["rows_total"] == 500,
        "full_occurrence_keys_equal_rows": analysis["distinct_full_occurrence_keys"] == analysis["rows_total"],
        "candidate_signatures_equal_rows": analysis["distinct_candidate_delta_signatures"] == analysis["rows_total"],
        "false_merge_count_zero": analysis["false_merge_count"] == 0,
        "collision_count_zero": analysis["collision_count"] == 0,
        "false_split_count_zero": analysis["false_split_count"] == 0,
        "retention_equal_1": analysis["retention"] == 1.0,
        "payload_schema_valid": not any("payload_" in f for f in analysis["failures"]),
        "authority_guards_clean": not any("authority_guard" in f for f in failures),
        "policy_valid": not any(f.startswith("policy") for f in failures),
        "source_valid": not any(f.startswith("source") or f.startswith("surface") for f in failures),
    }

    gate = "PASS" if not failures and all(pass_conditions.values()) else "FAIL"

    if gate == "PASS":
        terminal = {
            "type": "ADVANCE",
            "stop_code": None,
            "next_command_goal": NEXT_REVIEW_GOAL,
        }
        terminal_class = "PASS_APPROVED_NEW_BOUNDED_SURFACE_PROBE"
    else:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_APPROVED_NEW_BOUNDED_SURFACE_PROBE_FAILED",
            "next_command_goal": NEXT_DIAGNOSTIC_GOAL,
        }
        terminal_class = "FAIL_APPROVED_NEW_BOUNDED_SURFACE_PROBE"

    probe_seed = {
        "probe_name": PROBE_NAME,
        "policy_id": policy_id,
        "policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_surface_id": SOURCE_SURFACE_ID,
        "rows_total": analysis["rows_total"],
        "distinct_full_occurrence_keys": analysis["distinct_full_occurrence_keys"],
        "distinct_candidate_delta_signatures": analysis["distinct_candidate_delta_signatures"],
        "false_merge_count": analysis["false_merge_count"],
        "collision_count": analysis["collision_count"],
        "false_split_count": analysis["false_split_count"],
        "retention": analysis["retention"],
        "gate": gate,
    }
    probe_id = sha8(probe_seed)

    result = {
        "schema_version": "raw_delta_signature_candidate_approved_new_bounded_surface_probe_result_v0",
        "probe_name": PROBE_NAME,
        "probe_id": probe_id,
        "probe_status": "FIXED_SURFACE_OBSERVER_PROBE_COMPLETE",
        "policy_id": policy_id,
        "policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_surface_id": SOURCE_SURFACE_ID,
        "source_surface_receipt_id": SOURCE_SURFACE_RECEIPT_ID,
        "source_run_id": SOURCE_RUN_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
        "comparison": "full_occurrence_key_to_candidate_delta_signature",
        "analysis": analysis,
        "pass_conditions": pass_conditions,
        "burden": {
            "source_rows_bytes": source_rows_bytes,
            "source_rows_bytes_from_policy": source_rows_bytes_from_policy,
            "signature_payload_bytes": signature_payload_bytes,
            "signature_payload_bytes_from_policy": signature_payload_bytes_from_policy,
            "candidate_signature_payload_bytes": analysis["candidate_signature_payload_bytes"],
            "row_bytes_measured": analysis["row_bytes"],
            "burden_ratio_payload_to_source_rows": burden_ratio_payload_to_source_rows,
            "burden_ratio_candidate_payload_to_source_rows": burden_ratio_candidate_payload_to_source_rows,
        },
        "authority_guards": {
            "runner_executed": False,
            "candidate_rows_created": False,
            "candidate_accepted": False,
            "scale_mode_authorized": False,
            "registry_inserted": False,
            "registry_written": False,
            "registry_sqlite_read": False,
            "full_registry_scan_used": False,
            "runtime_semantic_changed": False,
            "runtime_code_changed": False,
            "runtime_receipt_emission_changed": False,
            "latest_or_mtime_selection_used": False,
            "ambient_workspace_inference_used": False,
            "case_id_or_cycle_n_identity_patch_used": False,
            "rowid_or_receipt_hash_truth_surface_used": False,
            "full_occurrence_key_in_signature_payload": False,
            "audit_or_debug_payload_in_signature_payload": False,
            "microhash_as_proof_used": False,
            "synthetic_fake_validation_rows_used": False,
            "transition_compression_probe_run": True,
        },
        "terminal_class": terminal_class,
        "terminal": terminal,
        "gate": gate,
        "failures": failures,
        "warnings": warnings,
        "created_at": now_iso(),
    }

    receipt = {
        "schema_version": "raw_delta_signature_candidate_approved_new_bounded_surface_probe_receipt_v0",
        "receipt_type": "APPROVED_NEW_BOUNDED_SURFACE_PROBE_RECEIPT",
        "probe_name": PROBE_NAME,
        "probe_id": probe_id,
        "policy_id": policy_id,
        "policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_surface_id": SOURCE_SURFACE_ID,
        "source_surface_receipt_id": SOURCE_SURFACE_RECEIPT_ID,
        "source_run_id": SOURCE_RUN_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "rows_total": analysis["rows_total"],
        "distinct_full_occurrence_keys": analysis["distinct_full_occurrence_keys"],
        "distinct_candidate_delta_signatures": analysis["distinct_candidate_delta_signatures"],
        "false_merge_count": analysis["false_merge_count"],
        "collision_count": analysis["collision_count"],
        "false_split_count": analysis["false_split_count"],
        "retention": analysis["retention"],
        "signature_payload_bytes": signature_payload_bytes,
        "source_rows_bytes": source_rows_bytes,
        "burden_ratio_payload_to_source_rows": burden_ratio_payload_to_source_rows,
        "candidate_signature_payload_bytes": analysis["candidate_signature_payload_bytes"],
        "burden_ratio_candidate_payload_to_source_rows": burden_ratio_candidate_payload_to_source_rows,
        "pass_conditions": pass_conditions,
        "terminal_class": terminal_class,
        "terminal": terminal,
        "authority_guards": result["authority_guards"],
        "gate": gate,
        "failures": failures,
        "warnings": warnings,
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id
    result["receipt_id"] = receipt_id

    if write_outputs:
        (OUT_DIR / f"{probe_id}.json").write_text(json.dumps(result, indent=2, sort_keys=True))
        (OUT_RECEIPT_DIR / f"{probe_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return result, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-id", default=EXPECTED_POLICY_ID)
    args = parser.parse_args()

    result, receipt = build_probe(args.policy_id, write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"probe_id={result['probe_id']}")
    print(f"probe_receipt_id={receipt['receipt_id']}")
    print(f"probe_path=data/raw_delta_signature_candidate_approved_new_bounded_surface_probe_results/{result['probe_id']}.json")
    print(f"probe_receipt_path=data/raw_delta_signature_candidate_approved_new_bounded_surface_probe_receipts/{result['probe_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
