#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import shlex
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PROVIDE_OPERATOR_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_evidence_operator_values.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_EVIDENCE_OPERATOR_VALUES"
MODE = "INTAKE / OPERATOR_EXPLICIT_VALUES / NO_TARGET_SELECTION_FOR_BUILD"
BUILD_MODE = "OPERATOR_TARGET_EVIDENCE_VALUES_INTAKE_ONLY"

SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_ID = "f3d0ae10"
SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_provider_materialization_v0_receipts/f3d0ae10.json"
SOURCE_INPUT_REQUEST_RECEIPT_ID = "ad527bfd"
SOURCE_INPUT_REQUEST_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_input_request_v0_receipts/ad527bfd.json"
SOURCE_INPUT_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_input_request_v0/explicit_runtime_patch_target_evidence_input_contract_v0.json"
SOURCE_ENV_TEMPLATE_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_input_request_v0/explicit_runtime_patch_target_evidence_env_template.sh"
SOURCE_REVIEW_RECEIPT_ID = "76b44fed"
SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_packet_review_v0_receipts/76b44fed.json"
SOURCE_REVIEW_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_packet_review_v0/target_evidence_packet_review_classification_v0.json"
SOURCE_SCHEMA_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/runtime_patch_target_evidence_packet_schema_v0.json"
SOURCE_HINT_INVENTORY_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_request_v0/target_hint_inventory_v0.json"
PROVIDER_SCRIPT_PATH = ROOT / "scripts/provide_explicit_runtime_patch_target_evidence_packet_v0.py"

REQUIRED_SOURCE_FILES = [
    SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_PATH,
    SOURCE_INPUT_REQUEST_RECEIPT_PATH,
    SOURCE_INPUT_CONTRACT_PATH,
    SOURCE_ENV_TEMPLATE_PATH,
    SOURCE_REVIEW_RECEIPT_PATH,
    SOURCE_REVIEW_CLASSIFICATION_PATH,
    SOURCE_SCHEMA_PATH,
    SOURCE_HINT_INVENTORY_PATH,
    PROVIDER_SCRIPT_PATH,
]

REQUIRED_ENV_FIELDS = [
    "SELECTED_TARGET_REF",
    "SELECTED_TARGET_KIND",
    "WHY_THIS_TARGET_IS_LOAD_BEARING",
    "WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON",
    "SOURCE_EVIDENCE_REFS_JSON",
    "VERIFICATION_GATE_REF",
    "ROLLBACK_OR_STOP_BOUNDARY_REF",
]

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_evidence_operator_values_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_evidence_operator_values_v0_receipts"

VALUES_PACKET_PATH = OUT_DIR / "operator_runtime_patch_target_evidence_values_packet_v0.json"
VALUES_ENV_EXPORT_PATH = OUT_DIR / "operator_runtime_patch_target_evidence_values_env_exports.sh"
VALUES_READOUT_PATH = OUT_DIR / "operator_runtime_patch_target_evidence_values_readout_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "operator_runtime_patch_target_evidence_values_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "operator_runtime_patch_target_evidence_values_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "operator_runtime_patch_target_evidence_values_profile_v0.json"
REPORT_PATH = OUT_DIR / "operator_runtime_patch_target_evidence_values_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "operator_runtime_patch_target_evidence_values_transition_trace.json"

ZERO_COUNTER_KEYS = [
    "target_candidate_declared_for_review_count",
    "target_selected_for_build_count",
    "accepted_for_build_count",
    "runtime_patch_applied_count",
    "target_file_modified_count",
    "c5_opened_count",
    "general_cell1_authority_granted_count",
    "taxonomy_registry_mutation_count",
    "proposal_status_promoted_count",
    "accepted_proposal_fabricated_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "hidden_next_command_count",
    "unbounded_payload_inspection_count",
    "latest_file_guessing_count",
    "mtime_selection_count",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def safe_local_bounded_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    if "EDIT_ME" in value or "FILL_ME" in value:
        return False
    if value.startswith("exact/"):
        return False
    p = Path(value)
    if p.is_absolute():
        return False
    if ".." in p.parts:
        return False
    if value.startswith(".git/"):
        return False
    return True

def parse_json_list_env(name: str, failures: List[str]) -> List[str]:
    raw = os.environ.get(name, "")
    if not raw:
        return []
    try:
        parsed = json.loads(raw)
    except Exception as exc:
        failures.append(f"env_invalid_json:{name}:{exc}")
        return []
    if not isinstance(parsed, list) or not parsed:
        failures.append(f"env_json_not_nonempty_list:{name}")
        return []
    if not all(isinstance(x, str) and x.strip() for x in parsed):
        failures.append(f"env_json_list_contains_non_string_or_blank:{name}")
        return []
    return parsed

def validate_source_basis() -> List[str]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    provider = read_json(SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_PATH)
    input_receipt = read_json(SOURCE_INPUT_REQUEST_RECEIPT_PATH)
    contract = read_json(SOURCE_INPUT_CONTRACT_PATH)
    review = read_json(SOURCE_REVIEW_RECEIPT_PATH)
    review_classification = read_json(SOURCE_REVIEW_CLASSIFICATION_PATH)
    schema = read_json(SOURCE_SCHEMA_PATH)
    inventory = read_json(SOURCE_HINT_INVENTORY_PATH)

    if provider.get("receipt_id") != SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_ID or provider.get("gate") != "PASS":
        failures.append("provider_materialization_receipt_not_pass")
    if provider.get("terminal", {}).get("stop_code") != "STOP_EXPLICIT_TARGET_EVIDENCE_PROVIDER_MATERIALIZED":
        failures.append("provider_materialization_wrong_terminal")
    if provider.get("provider_materialization_summary", {}).get("status") != "EXPLICIT_TARGET_EVIDENCE_PROVIDER_MATERIALIZED":
        failures.append("provider_not_materialized")

    if input_receipt.get("receipt_id") != SOURCE_INPUT_REQUEST_RECEIPT_ID or input_receipt.get("gate") != "PASS":
        failures.append("input_request_receipt_not_pass")
    if input_receipt.get("terminal", {}).get("stop_code") != "STOP_EXPLICIT_TARGET_EVIDENCE_INPUTS_REQUESTED":
        failures.append("input_request_wrong_terminal")
    if contract.get("required_env_fields") != REQUIRED_ENV_FIELDS:
        failures.append("input_contract_required_fields_changed")
    if contract.get("target_selected_for_build") is not False:
        failures.append("input_contract_selects_target_for_build")
    if contract.get("runtime_patch_authorized") is not False:
        failures.append("input_contract_authorizes_runtime_patch")

    if review.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID or review.get("gate") != "PASS":
        failures.append("review_receipt_not_pass")
    if review.get("terminal", {}).get("stop_code") != "STOP_TARGET_EVIDENCE_PACKET_MISSING":
        failures.append("review_wrong_terminal")
    if review_classification.get("review_status") != "TARGET_EVIDENCE_PACKET_MISSING":
        failures.append("review_status_not_missing")
    if review_classification.get("target_selected_for_build") is not False:
        failures.append("review_selected_target_for_build")
    if review_classification.get("accepted_for_build") is not False:
        failures.append("review_accepted_for_build")
    if review_classification.get("runtime_patch_authorized") is not False:
        failures.append("review_authorized_runtime_patch")

    if schema.get("packet_object_type") != "NARROWER_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET":
        failures.append("schema_wrong_packet_object_type")
    if inventory.get("hint_count") != 13:
        failures.append(f"hint_count_not_13:{inventory.get('hint_count')}")
    if inventory.get("target_selected") is not False:
        failures.append("inventory_target_selected_unexpectedly")

    return failures

def collect_operator_values() -> Tuple[Dict[str, Any], List[str], List[str]]:
    failures: List[str] = []
    missing: List[str] = []

    raw_values = {field: os.environ.get(field, "") for field in REQUIRED_ENV_FIELDS}

    for field, value in raw_values.items():
        if not value:
            missing.append(field)
            failures.append(f"env_missing:{field}")
        elif "EDIT_ME" in value or "FILL_ME" in value or value.startswith("exact/"):
            failures.append(f"env_placeholder:{field}:{value}")

    why_other = parse_json_list_env("WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON", failures)
    source_refs = parse_json_list_env("SOURCE_EVIDENCE_REFS_JSON", failures)

    for field in ["SELECTED_TARGET_REF", "VERIFICATION_GATE_REF", "ROLLBACK_OR_STOP_BOUNDARY_REF"]:
        value = raw_values.get(field, "")
        if value and not safe_local_bounded_path(value):
            failures.append(f"env_not_local_bounded_path:{field}:{value}")

    for ref in source_refs:
        if not safe_local_bounded_path(ref):
            failures.append(f"source_evidence_ref_not_local_bounded:{ref}")

    values = {
        "selected_target_ref": raw_values["SELECTED_TARGET_REF"],
        "selected_target_kind": raw_values["SELECTED_TARGET_KIND"],
        "why_this_target_is_load_bearing": raw_values["WHY_THIS_TARGET_IS_LOAD_BEARING"],
        "why_other_hints_are_not_targets": why_other,
        "source_evidence_refs": source_refs,
        "verification_gate_ref": raw_values["VERIFICATION_GATE_REF"],
        "rollback_or_stop_boundary_ref": raw_values["ROLLBACK_OR_STOP_BOUNDARY_REF"],
    }

    return values, missing, failures

def write_env_exports(values: Dict[str, Any]) -> None:
    lines = [
        "# Source this file before rerunning PROVIDE_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_V0.",
        "# This file records explicit operator-supplied values only. It does not authorize build acceptance or patching.",
        f"export SELECTED_TARGET_REF={shlex.quote(values['selected_target_ref'])}",
        f"export SELECTED_TARGET_KIND={shlex.quote(values['selected_target_kind'])}",
        f"export WHY_THIS_TARGET_IS_LOAD_BEARING={shlex.quote(values['why_this_target_is_load_bearing'])}",
        f"export WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON={shlex.quote(json.dumps(values['why_other_hints_are_not_targets']))}",
        f"export SOURCE_EVIDENCE_REFS_JSON={shlex.quote(json.dumps(values['source_evidence_refs']))}",
        f"export VERIFICATION_GATE_REF={shlex.quote(values['verification_gate_ref'])}",
        f"export ROLLBACK_OR_STOP_BOUNDARY_REF={shlex.quote(values['rollback_or_stop_boundary_ref'])}",
        "",
    ]
    VALUES_ENV_EXPORT_PATH.write_text("\n".join(lines))

def values_packet(values: Dict[str, Any], status: str, missing: List[str], failures: List[str]) -> Dict[str, Any]:
    ready = status == "OPERATOR_TARGET_EVIDENCE_VALUES_READY"
    return {
        "schema_version": "operator_runtime_patch_target_evidence_values_packet_v0",
        "packet_type": "OPERATOR_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES",
        "operator_values_packet_id": "operator_values_" + sha8({"values": values, "status": status}),
        "status": status,
        "missing_fields": missing,
        "failures": failures,
        "source_provider_materialization_receipt_id": SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_ID,
        "source_input_request_receipt_id": SOURCE_INPUT_REQUEST_RECEIPT_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "values": values if ready else {},
        "operator_supplied_target_ref": values.get("selected_target_ref") if ready else None,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": "RERUN_PROVIDE_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_WITH_RECORDED_OPERATOR_VALUES_V0" if ready else "PROVIDE_OPERATOR_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_V0",
    }

def authority_boundary(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "operator_runtime_patch_target_evidence_values_authority_boundary_v0",
        "status": status,
        "may_record_operator_supplied_values": True,
        "may_emit_env_exports_if_values_ready": status == "OPERATOR_TARGET_EVIDENCE_VALUES_READY",
        "may_declare_target_candidate_for_review": False,
        "may_select_target_for_build": False,
        "may_accept_for_build": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "must_not_infer": [
            "operator values mean accepted for build",
            "operator target ref means selected target for build",
            "values packet authorizes patching",
            "missing values may be guessed from the 13 hints"
        ],
    }

def rollup(status: str) -> Dict[str, Any]:
    ready = status == "OPERATOR_TARGET_EVIDENCE_VALUES_READY"
    missing = status == "OPERATOR_TARGET_EVIDENCE_VALUES_MISSING_OR_INVALID"
    return {
        "schema_version": "operator_runtime_patch_target_evidence_values_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_provider_materialization_receipt_id": SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_ID,
        "source_input_request_receipt_id": SOURCE_INPUT_REQUEST_RECEIPT_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "operator_values_ready_count": 1 if ready else 0,
        "operator_values_missing_or_invalid_count": 1 if missing else 0,
        "env_exports_emitted_count": 1 if ready else 0,
        "target_candidate_declared_for_review_count": 0,
        "target_selected_for_build_count": 0,
        "accepted_for_build_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "unbounded_payload_inspection_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": "RERUN_PROVIDE_EXPLICIT_RUNTIME_PATCH_TARGET_EVIDENCE_PACKET_WITH_RECORDED_OPERATOR_VALUES_V0" if ready else "PROVIDE_OPERATOR_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_V0",
    }

def profile(status: str, values: Dict[str, Any], roll: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "operator_runtime_patch_target_evidence_values_profile_v0",
        "profile_id": "operator_values_" + sha8({"status": status, "values": values}),
        "status": status,
        "operator_supplied_target_ref": values.get("selected_target_ref") if status == "OPERATOR_TARGET_EVIDENCE_VALUES_READY" else None,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(roll.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "recommended_next": roll["recommended_next"],
        "next_command_goal": None,
    }

def report(status: str, packet: Dict[str, Any], roll: Dict[str, Any], prof: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "operator_runtime_patch_target_evidence_values_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "missing_fields": packet["missing_fields"],
        "operator_supplied_target_ref": prof["operator_supplied_target_ref"],
        "recommended_next_handling": prof["recommended_next"],
        "target_candidate_declared_for_review_count": 0,
        "target_selected_for_build_count": 0,
        "accepted_for_build_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
    }

def trace(status: str, missing: List[str], failures: List[str]) -> Dict[str, Any]:
    if status == "OPERATOR_TARGET_EVIDENCE_VALUES_READY":
        stop_code = "STOP_OPERATOR_TARGET_EVIDENCE_VALUES_RECORDED"
        taken = "record_values_and_emit_env_exports"
    else:
        stop_code = "STOP_OPERATOR_TARGET_EVIDENCE_VALUES_MISSING_OR_INVALID"
        taken = "record_missing_or_invalid_fields_without_guessing"

    return {
        "schema_version": "operator_runtime_patch_target_evidence_values_transition_trace_v0",
        "trace": [
            {
                "step": "consume_provider_materialization_and_input_contract",
                "question": "can operator values be accepted without guessing",
                "answer": "only if all seven explicit fields are present and valid",
                "taken": "inspect_declared_env_values_only",
            },
            {
                "step": "classify_operator_values",
                "question": "are all seven fields present and valid",
                "answer": status,
                "missing_fields": missing,
                "failures": failures,
                "taken": taken,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": stop_code,
            "next_command_goal": None,
        },
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    source_failures = validate_source_basis()

    values, missing, value_failures = collect_operator_values()
    failures = source_failures + value_failures

    status = "OPERATOR_TARGET_EVIDENCE_VALUES_READY" if not failures else "OPERATOR_TARGET_EVIDENCE_VALUES_MISSING_OR_INVALID"

    packet = values_packet(values, status, missing, failures)
    boundary = authority_boundary(status)
    roll = rollup(status)
    prof = profile(status, values, roll)
    rep = report(status, packet, roll, prof)
    tr = trace(status, missing, failures)

    write_json(VALUES_PACKET_PATH, packet)
    if status == "OPERATOR_TARGET_EVIDENCE_VALUES_READY":
        write_env_exports(values)
    elif VALUES_ENV_EXPORT_PATH.exists():
        VALUES_ENV_EXPORT_PATH.unlink()

    readout = {
        "schema_version": "operator_runtime_patch_target_evidence_values_readout_v0",
        "status": status,
        "required_env_fields": REQUIRED_ENV_FIELDS,
        "missing_fields": missing,
        "failures": failures,
        "operator_supplied_target_ref": prof["operator_supplied_target_ref"],
        "env_exports_ref": rel(VALUES_ENV_EXPORT_PATH) if VALUES_ENV_EXPORT_PATH.exists() else None,
        "recommended_next": prof["recommended_next"],
    }

    write_json(VALUES_READOUT_PATH, readout)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, roll)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(TRANSITION_TRACE_PATH, tr)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        roll["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, roll)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "OPERATOR_VALUES_0_PROVIDER_MATERIALIZATION_RECEIPT_CONSUMED": SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_PATH.exists(),
        "OPERATOR_VALUES_1_INPUT_REQUEST_RECEIPT_CONSUMED": SOURCE_INPUT_REQUEST_RECEIPT_PATH.exists(),
        "OPERATOR_VALUES_2_VALUES_PACKET_EMITTED": VALUES_PACKET_PATH.exists(),
        "OPERATOR_VALUES_3_VALUES_READOUT_EMITTED": VALUES_READOUT_PATH.exists(),
        "OPERATOR_VALUES_4_AUTHORITY_BOUNDARY_EMITTED": AUTHORITY_BOUNDARY_PATH.exists(),
        "OPERATOR_VALUES_5_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": prof["target_candidate_declared_for_review"] is False,
        "OPERATOR_VALUES_6_NO_TARGET_SELECTED_FOR_BUILD": prof["target_selected_for_build"] is False,
        "OPERATOR_VALUES_7_NO_ACCEPTED_FOR_BUILD": prof["accepted_for_build"] is False,
        "OPERATOR_VALUES_8_NO_RUNTIME_PATCH": prof["runtime_patch_applied"] is False,
        "OPERATOR_VALUES_9_NO_TARGET_FILE_MODIFICATION": prof["target_file_modified"] is False,
        "OPERATOR_VALUES_10_NO_C5_OPENED": prof["c5_opened"] is False,
        "OPERATOR_VALUES_11_NO_GENERAL_CELL1_AUTHORITY": prof["general_cell1_authority_granted"] is False,
        "OPERATOR_VALUES_12_NO_LATEST_FILE_GUESSING": prof["latest_file_guessing"] is False,
        "OPERATOR_VALUES_13_NO_MTIME_SELECTION": prof["mtime_selection"] is False,
        "OPERATOR_VALUES_14_NO_HIDDEN_NEXT_COMMAND": prof["next_command_goal"] is None,
        "OPERATOR_VALUES_15_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        status = "OPERATOR_TARGET_EVIDENCE_VALUES_MISSING_OR_INVALID"
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not source_failures else "FAIL"
    terminal = tr["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_OPERATOR_TARGET_EVIDENCE_VALUES_SOURCE_BASIS_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "values": values if status == "OPERATOR_TARGET_EVIDENCE_VALUES_READY" else {},
        "failures": failures,
        "terminal": terminal,
        "gate": gate,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "operator_runtime_patch_target_evidence_values_receipt_v0",
        "receipt_type": "OPERATOR_RUNTIME_PATCH_TARGET_EVIDENCE_VALUES_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_provider_materialization_receipt_id": SOURCE_PROVIDER_MATERIALIZATION_RECEIPT_ID,
        "source_input_request_receipt_id": SOURCE_INPUT_REQUEST_RECEIPT_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "operator_values_summary": {
            "status": status,
            "required_env_field_count": len(REQUIRED_ENV_FIELDS),
            "missing_fields": missing,
            "operator_supplied_target_ref": prof["operator_supplied_target_ref"],
            "target_candidate_declared_for_review": False,
            "target_selected_for_build": False,
            "accepted_for_build": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": prof["bad_counters_zero"],
            "recommended_next": prof["recommended_next"],
        },
        "aggregate_metrics": rep,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "values_packet": rel(VALUES_PACKET_PATH),
            "values_env_exports": rel(VALUES_ENV_EXPORT_PATH) if VALUES_ENV_EXPORT_PATH.exists() else None,
            "values_readout": rel(VALUES_READOUT_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"operator_values_receipt_id={receipt_id}")
    print(f"operator_values_receipt_path={rel(receipt_path)}")
    print(f"operator_values_packet_path={rel(VALUES_PACKET_PATH)}")
    print(f"operator_values_env_exports_path={rel(VALUES_ENV_EXPORT_PATH) if VALUES_ENV_EXPORT_PATH.exists() else ''}")
    print(f"operator_values_rollup_path={rel(ROLLUP_PATH)}")
    print(f"operator_values_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
