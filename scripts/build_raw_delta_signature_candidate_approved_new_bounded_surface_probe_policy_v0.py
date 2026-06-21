#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

SOURCE_SURFACE_ID = "4427ba4b"
SOURCE_SURFACE_RECEIPT_ID = "e5022cd2"
SOURCE_POLICY_ID = "3b22a690"
SOURCE_POLICY_RECEIPT_ID = "36177050"
SOURCE_RUN_ID = "run_20260621_183812_136149"
SOURCE_IMPLEMENTATION_COMMIT = "5e9363ca1"

CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
POLICY_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_PROBE_POLICY_V0"
POLICY_STATUS = "POLICY_ONLY_NOT_IMPLEMENTED"
PROBE_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_PROBE_V0"

SURFACE_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_receipts"
SURFACE_MANIFEST_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_manifests"
SURFACE_ROWS_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_rows"

POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_probe_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_probe_policy_receipts"

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
]

NEXT_IMPLEMENTATION_GOAL = "RUN_RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_PROBE_V0"


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
        raise SystemExit(f"missing required json: {path}")
    return json.loads(path.read_text())


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"missing required jsonl: {path}")
    out = []
    for i, line in enumerate(path.read_text().splitlines(), start=1):
        if not line.strip():
            continue
        try:
            obj = json.loads(line)
        except Exception as exc:
            raise SystemExit(f"bad jsonl line {i} in {path}: {exc}") from exc
        if not isinstance(obj, dict):
            raise SystemExit(f"jsonl line {i} is not object in {path}")
        out.append(obj)
    return out


def validate_source_surface(receipt: dict[str, Any], manifest: dict[str, Any], rows: list[dict[str, Any]]) -> list[str]:
    failures: list[str] = []

    if receipt.get("surface_id") != SOURCE_SURFACE_ID:
        failures.append(f"surface_id_wrong:{receipt.get('surface_id')}")
    if receipt.get("receipt_id") != SOURCE_SURFACE_RECEIPT_ID:
        failures.append(f"receipt_id_wrong:{receipt.get('receipt_id')}")
    if receipt.get("policy_id") != SOURCE_POLICY_ID:
        failures.append(f"policy_id_wrong:{receipt.get('policy_id')}")
    if receipt.get("policy_receipt_id") != SOURCE_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{receipt.get('policy_receipt_id')}")
    if receipt.get("explicit_run_id") != SOURCE_RUN_ID:
        failures.append(f"explicit_run_id_wrong:{receipt.get('explicit_run_id')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"source_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("hold_code") is not None:
        failures.append(f"source_hold_code_not_null:{receipt.get('hold_code')}")
    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"source_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_APPROVED_NEW_BOUNDED_SURFACE_PROBE_POLICY_V0":
        failures.append(f"source_terminal_next_wrong:{terminal.get('next_command_goal')}")

    if manifest.get("surface_id") != SOURCE_SURFACE_ID:
        failures.append(f"manifest_surface_id_wrong:{manifest.get('surface_id')}")
    if manifest.get("gate") != "PASS":
        failures.append(f"manifest_gate_not_PASS:{manifest.get('gate')}")

    if receipt.get("rows_created") != 500:
        failures.append(f"rows_created_wrong:{receipt.get('rows_created')}")
    if receipt.get("new_bands_created") != 500:
        failures.append(f"new_bands_created_wrong:{receipt.get('new_bands_created')}")
    if receipt.get("candidate_signature_distinct_count") != 500:
        failures.append(f"candidate_signature_distinct_count_wrong:{receipt.get('candidate_signature_distinct_count')}")
    if len(rows) != 500:
        failures.append(f"rows_file_count_wrong:{len(rows)}")

    if receipt.get("candidate_field_alias_patch") != "PATCH_APPROVED_RECIPE_CANDIDATE_FIELD_ALIAS_EXTRACTOR_V0":
        failures.append(f"candidate_field_alias_patch_wrong:{receipt.get('candidate_field_alias_patch')}")
    if receipt.get("cv_fallback_rule_id") != "CV_EQUALS_CANDIDATE_DESIGN_ID_WHEN_NATIVE_CV_ABSENT_V0":
        failures.append(f"cv_fallback_rule_id_wrong:{receipt.get('cv_fallback_rule_id')}")
    cv_rule = receipt.get("cv_fallback_rule") or {}
    if cv_rule.get("cv_value") != CANDIDATE_DESIGN_ID:
        failures.append(f"cv_rule_value_wrong:{cv_rule.get('cv_value')}")
    if cv_rule.get("cv_semantics") != "candidate_version_identity_not_occurrence_identity":
        failures.append(f"cv_rule_semantics_wrong:{cv_rule.get('cv_semantics')}")
    if cv_rule.get("does_not_add_occurrence_identity") is not True:
        failures.append("cv_rule_adds_occurrence_identity")
    if cv_rule.get("does_not_change_payload_schema") is not True:
        failures.append("cv_rule_changes_payload_schema")

    guards = receipt.get("authority_guards") or {}
    for key in FORBIDDEN_AUTHORITY_TRUE:
        if guards.get(key) is not False:
            failures.append(f"authority_guard_not_false:{key}:{guards.get(key)}")
    if guards.get("runner_executed") is not False:
        failures.append(f"runner_executed_not_false:{guards.get('runner_executed')}")
    if guards.get("runner_executions_total") != 0:
        failures.append(f"runner_executions_total_not_zero:{guards.get('runner_executions_total')}")
    if guards.get("candidate_rows_created") is not True:
        failures.append(f"candidate_rows_created_not_true:{guards.get('candidate_rows_created')}")
    if guards.get("candidate_rows_created_total") != 500:
        failures.append(f"candidate_rows_created_total_wrong:{guards.get('candidate_rows_created_total')}")

    full_keys = set()
    signatures = set()
    payload_shapes = Counter()
    cv_values = Counter()
    cv_sources = Counter()

    for idx, row in enumerate(rows):
        prefix = f"row[{idx}]"
        if row.get("row_type") != "RAW_DELTA_SIGNATURE_CANDIDATE_V0_ROW":
            failures.append(f"{prefix}:row_type_wrong:{row.get('row_type')}")
        if row.get("source_run_id") != SOURCE_RUN_ID:
            failures.append(f"{prefix}:source_run_id_wrong:{row.get('source_run_id')}")
        if row.get("source_surface_id") != SOURCE_SURFACE_ID:
            failures.append(f"{prefix}:source_surface_id_wrong:{row.get('source_surface_id')}")
        if row.get("truth_surface") != "full_occurrence_key_to_candidate_delta_signature":
            failures.append(f"{prefix}:truth_surface_wrong:{row.get('truth_surface')}")

        full_key = row.get("full_occurrence_key")
        sig = row.get("candidate_delta_signature")
        if not full_key:
            failures.append(f"{prefix}:missing_full_occurrence_key")
        else:
            full_keys.add(json.dumps(full_key, sort_keys=True, default=str))
        if not sig:
            failures.append(f"{prefix}:missing_candidate_delta_signature")
        else:
            signatures.add(str(sig))

        payload = row.get("signature_payload")
        if not isinstance(payload, dict):
            failures.append(f"{prefix}:signature_payload_not_object")
            continue
        payload_shapes[tuple(payload.keys())] += 1
        if set(payload.keys()) != set(REQUIRED_PAYLOAD_FIELDS):
            failures.append(f"{prefix}:payload_fields_wrong:{list(payload.keys())}")
        for field in REQUIRED_PAYLOAD_FIELDS:
            value = payload.get(field)
            if value is None or str(value) == "":
                failures.append(f"{prefix}:payload_field_empty:{field}")
        for forbidden in FORBIDDEN_PAYLOAD_FIELDS:
            if forbidden in payload:
                failures.append(f"{prefix}:forbidden_payload_field:{forbidden}")

        cv_values[payload.get("cv")] += 1
        cv_sources[row.get("cv_source")] += 1
        if payload.get("cv") != CANDIDATE_DESIGN_ID:
            failures.append(f"{prefix}:cv_wrong:{payload.get('cv')}")
        if row.get("cv_source") != "CV_EQUALS_CANDIDATE_DESIGN_ID_WHEN_NATIVE_CV_ABSENT_V0":
            failures.append(f"{prefix}:cv_source_wrong:{row.get('cv_source')}")

    if len(full_keys) != 500:
        failures.append(f"full_occurrence_keys_not_distinct_500:{len(full_keys)}")
    if len(signatures) != 500:
        failures.append(f"candidate_signatures_not_distinct_500:{len(signatures)}")

    return failures


def build_policy(surface_id: str, write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    if write_outputs:
        POLICY_DIR.mkdir(parents=True, exist_ok=True)
        POLICY_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    if surface_id != SOURCE_SURFACE_ID:
        raise SystemExit(f"unsupported surface_id for this frozen policy builder: {surface_id}")

    surface_receipt_path = SURFACE_RECEIPT_DIR / f"{surface_id}.json"
    surface_manifest_path = SURFACE_MANIFEST_DIR / f"{surface_id}.json"
    surface_rows_path = SURFACE_ROWS_DIR / f"{surface_id}.jsonl"

    source_receipt = load_json(surface_receipt_path)
    source_manifest = load_json(surface_manifest_path)
    rows = load_jsonl(surface_rows_path)

    failures = validate_source_surface(source_receipt, source_manifest, rows)

    full_keys = {json.dumps(row.get("full_occurrence_key"), sort_keys=True, default=str) for row in rows}
    candidate_sigs = {str(row.get("candidate_delta_signature")) for row in rows}
    payload_bytes = sum(len(json.dumps(row.get("signature_payload", {}), sort_keys=True, separators=(",", ":")).encode("utf-8")) for row in rows)
    row_bytes = sum(len(json.dumps(row, sort_keys=True, separators=(",", ":")).encode("utf-8")) for row in rows)

    policy_seed = {
        "policy_name": POLICY_NAME,
        "source_surface_id": SOURCE_SURFACE_ID,
        "source_surface_receipt_id": SOURCE_SURFACE_RECEIPT_ID,
        "source_policy_id": SOURCE_POLICY_ID,
        "source_policy_receipt_id": SOURCE_POLICY_RECEIPT_ID,
        "source_run_id": SOURCE_RUN_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "rows": len(rows),
        "candidate_sigs": len(candidate_sigs),
        "full_keys": len(full_keys),
        "payload_fields": REQUIRED_PAYLOAD_FIELDS,
        "implementation_commit": SOURCE_IMPLEMENTATION_COMMIT,
    }
    policy_id = sha8(policy_seed)

    policy = {
        "schema_version": "raw_delta_signature_candidate_approved_new_bounded_surface_probe_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_id": policy_id,
        "policy_status": POLICY_STATUS,
        "probe_name": PROBE_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_surface": {
            "surface_id": SOURCE_SURFACE_ID,
            "surface_receipt_id": SOURCE_SURFACE_RECEIPT_ID,
            "surface_manifest_path": rel(surface_manifest_path),
            "surface_receipt_path": rel(surface_receipt_path),
            "surface_rows_path": rel(surface_rows_path),
            "source_policy_id": SOURCE_POLICY_ID,
            "source_policy_receipt_id": SOURCE_POLICY_RECEIPT_ID,
            "source_run_id": SOURCE_RUN_ID,
            "source_implementation_commit": SOURCE_IMPLEMENTATION_COMMIT,
            "rows_created": source_receipt.get("rows_created"),
            "new_bands_created": source_receipt.get("new_bands_created"),
            "candidate_signature_distinct_count": source_receipt.get("candidate_signature_distinct_count"),
            "cv_fallback_rule_id": source_receipt.get("cv_fallback_rule_id"),
            "candidate_field_alias_patch": source_receipt.get("candidate_field_alias_patch"),
        },
        "probe_contract": {
            "input_surface_kind": "APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_ROWS",
            "allowed_input_rows_path": rel(surface_rows_path),
            "allowed_input_manifest_path": rel(surface_manifest_path),
            "allowed_input_receipt_path": rel(surface_receipt_path),
            "rows_expected": 500,
            "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
            "comparison": "full_occurrence_key_to_candidate_delta_signature",
            "required_payload_fields": REQUIRED_PAYLOAD_FIELDS,
            "forbidden_payload_fields": FORBIDDEN_PAYLOAD_FIELDS,
            "required_candidate_version": CANDIDATE_DESIGN_ID,
            "cv_source_rule": "CV_EQUALS_CANDIDATE_DESIGN_ID_WHEN_NATIVE_CV_ABSENT_V0",
            "acceptance_gates": {
                "gate_must_pass": True,
                "rows_must_equal": 500,
                "full_occurrence_keys_must_equal_rows": True,
                "candidate_signatures_must_equal_rows": True,
                "false_merge_count_must_equal": 0,
                "collision_count_must_equal": 0,
                "false_split_count_must_equal": 0,
                "retention_must_equal": 1.0,
                "payload_schema_must_match": True,
                "forbidden_payload_fields_absent": True,
                "authority_guards_clean": True,
            },
            "burden_measurement": {
                "measure_rows_bytes": True,
                "measure_signature_payload_bytes": True,
                "measure_source_surface_bytes": True,
                "report_burden_ratio_if_source_bytes_available": True,
                "do_not_use_receipt_hash_as_truth_surface": True,
            },
        },
        "authorized_operations_next": {
            "read_source_surface_rows_file": True,
            "read_source_surface_manifest_file": True,
            "read_source_surface_receipt_file": True,
            "write_probe_result": True,
            "write_probe_receipt": True,
            "run_existing_candidate_probe_logic_on_fixed_surface": True,
        },
        "forbidden_operations": {
            "candidate_acceptance": True,
            "scale_mode": True,
            "registry_insert": True,
            "registry_write": True,
            "registry_sqlite_read": True,
            "full_registry_scan": True,
            "runtime_code_change": True,
            "runtime_semantic_change": True,
            "runtime_receipt_emission_change": True,
            "runner_execution": True,
            "latest_or_mtime_selection": True,
            "ambient_workspace_inference": True,
            "synthetic_fake_rows": True,
            "payload_identity_patch": True,
            "case_id_or_cycle_n_in_signature_payload": True,
            "rowid_or_receipt_hash_truth_surface": True,
            "full_occurrence_key_in_signature_payload": True,
            "audit_or_debug_payload_in_signature_payload": True,
            "microhash_as_proof": True,
        },
        "source_surface_summary": {
            "rows_total": len(rows),
            "distinct_full_occurrence_keys": len(full_keys),
            "distinct_candidate_delta_signatures": len(candidate_sigs),
            "signature_payload_bytes": payload_bytes,
            "source_rows_bytes": row_bytes,
            "pre_policy_local_distinguishability": {
                "full_occurrence_keys_equal_rows": len(full_keys) == len(rows),
                "candidate_signatures_equal_rows": len(candidate_sigs) == len(rows),
                "already_distinct_on_candidate_signature": len(candidate_sigs) == len(rows),
            },
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "stop_code": None if not failures else "STOP_APPROVED_NEW_SURFACE_PROBE_POLICY_INVALID_SOURCE",
            "next_command_goal": NEXT_IMPLEMENTATION_GOAL if not failures else None,
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
            "transition_compression_probe_run": False,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt = {
        "schema_version": "raw_delta_signature_candidate_approved_new_bounded_surface_probe_policy_receipt_v0",
        "receipt_type": "APPROVED_NEW_BOUNDED_SURFACE_PROBE_POLICY_RECEIPT",
        "policy_id": policy_id,
        "policy_name": POLICY_NAME,
        "policy_status": POLICY_STATUS,
        "probe_name": PROBE_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_surface_id": SOURCE_SURFACE_ID,
        "source_surface_receipt_id": SOURCE_SURFACE_RECEIPT_ID,
        "source_policy_id": SOURCE_POLICY_ID,
        "source_policy_receipt_id": SOURCE_POLICY_RECEIPT_ID,
        "source_run_id": SOURCE_RUN_ID,
        "source_implementation_commit": SOURCE_IMPLEMENTATION_COMMIT,
        "rows_total": len(rows),
        "distinct_full_occurrence_keys": len(full_keys),
        "distinct_candidate_delta_signatures": len(candidate_sigs),
        "signature_payload_bytes": payload_bytes,
        "source_rows_bytes": row_bytes,
        "required_payload_fields": REQUIRED_PAYLOAD_FIELDS,
        "forbidden_payload_fields": FORBIDDEN_PAYLOAD_FIELDS,
        "authorized_next": policy["authorized_operations_next"],
        "forbidden_operations": policy["forbidden_operations"],
        "terminal": policy["terminal"],
        "authority_guards": policy["authority_guards"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id
    policy["policy_receipt_id"] = receipt_id

    if write_outputs:
        (POLICY_DIR / f"{policy_id}.json").write_text(json.dumps(policy, indent=2, sort_keys=True))
        (POLICY_RECEIPT_DIR / f"{policy_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return policy, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--surface-id", default=SOURCE_SURFACE_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.surface_id, write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_receipt_id={receipt['receipt_id']}")
    print(f"policy_path=data/raw_delta_signature_candidate_approved_new_bounded_surface_probe_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/raw_delta_signature_candidate_approved_new_bounded_surface_probe_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
