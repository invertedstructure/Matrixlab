#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PROVIDE_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_packet_values.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES"
MODE = "SOURCE_PACKET_VALUES_INPUT_CONTRACT / NO_METADATA_FILL / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "TYPED_METADATA_SOURCE_PACKET_VALUES_CONTRACT_ONLY"

SOURCE_PACKET_REVIEW_RECEIPT_ID = "90cb2053"
SOURCE_PACKET_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_review_v0_receipts/90cb2053.json"
SOURCE_PACKET_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_review_v0/typed_value_source_metadata_source_packet_contract_v0.json"
SOURCE_PACKET_REVIEW_REQUEST_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_review_v0/typed_value_source_metadata_source_packet_review_request_v0.json"
SOURCE_PACKET_REVIEW_RESULT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_review_v0/typed_value_source_metadata_source_packet_review_result_v0.json"
SOURCE_PACKET_MISSING_VALUES_TEMPLATE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_review_v0/typed_value_source_metadata_source_packet_missing_values_template_v0.json"
SOURCE_PACKET_FIELD_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_review_v0/typed_value_source_metadata_source_packet_field_review_v0.json"
SOURCE_PACKET_REVIEW_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_review_v0/typed_value_source_metadata_source_packet_review_classification_v0.json"
SOURCE_PACKET_REVIEW_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_review_v0/typed_value_source_metadata_source_packet_review_rollup_v0.json"
SOURCE_PACKET_REVIEW_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_review_v0/typed_value_source_metadata_source_packet_review_profile_v0.json"

SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID = "68a12602"
SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0_receipts/68a12602.json"
SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_packet_template_v0.json"
SOURCE_METADATA_SOURCE_FIELD_POLICY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_field_policy_v0.json"
SOURCE_METADATA_ROW_SOURCE_REQUIREMENTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_row_source_requirements_v0.json"
SOURCE_METADATA_HUMAN_SCHEMA_ONLY_FIELDS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_human_schema_only_fields_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_v0_receipts"

VALUES_INPUT_CONTRACT_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_input_contract_v0.json"
VALUES_REQUEST_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_request_v0.json"
VALUES_ENV_TEMPLATE_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_env_template_v0.sh"
VALUES_PACKET_DRAFT_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_packet_draft_v0.json"
VALUES_MISSING_FIELDS_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_missing_fields_v0.json"
VALUES_REVIEW_INTENT_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_review_intent_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_values_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_PACKET_REVIEW_RECEIPT_PATH,
    SOURCE_PACKET_CONTRACT_PATH,
    SOURCE_PACKET_REVIEW_REQUEST_PATH,
    SOURCE_PACKET_REVIEW_RESULT_PATH,
    SOURCE_PACKET_MISSING_VALUES_TEMPLATE_PATH,
    SOURCE_PACKET_FIELD_REVIEW_PATH,
    SOURCE_PACKET_REVIEW_CLASSIFICATION_PATH,
    SOURCE_PACKET_REVIEW_ROLLUP_PATH,
    SOURCE_PACKET_REVIEW_PROFILE_PATH,
    SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_PATH,
    SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH,
    SOURCE_METADATA_SOURCE_FIELD_POLICY_PATH,
    SOURCE_METADATA_ROW_SOURCE_REQUIREMENTS_PATH,
    SOURCE_METADATA_HUMAN_SCHEMA_ONLY_FIELDS_PATH,
]

EXPECTED_REVIEW_STATUS = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_NOT_PROVIDED"
EXPECTED_REVIEW_STOP = "STOP_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_NOT_PROVIDED"
EXPECTED_NEXT = "PROVIDE_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_V0"

VALUES_ENV_JSON = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_JSON"
VALUES_ENV_PATH = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_PATH"

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

def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text)

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_source_basis() -> List[str]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    review_receipt = read_json(SOURCE_PACKET_REVIEW_RECEIPT_PATH)
    review_result = read_json(SOURCE_PACKET_REVIEW_RESULT_PATH)
    review_class = read_json(SOURCE_PACKET_REVIEW_CLASSIFICATION_PATH)
    review_roll = read_json(SOURCE_PACKET_REVIEW_ROLLUP_PATH)
    review_profile = read_json(SOURCE_PACKET_REVIEW_PROFILE_PATH)
    contract = read_json(SOURCE_PACKET_CONTRACT_PATH)
    missing_template = read_json(SOURCE_PACKET_MISSING_VALUES_TEMPLATE_PATH)
    bridge_receipt = read_json(SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_PATH)
    source_template = read_json(SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH)
    field_policy = read_json(SOURCE_METADATA_SOURCE_FIELD_POLICY_PATH)

    summary = review_receipt.get("typed_metadata_source_packet_review_summary", {})
    bridge_summary = bridge_receipt.get("typed_metadata_source_bridge_summary", {})

    if review_receipt.get("receipt_id") != SOURCE_PACKET_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("source_packet_review_receipt_not_pass")
    if summary.get("status") != EXPECTED_REVIEW_STATUS:
        failures.append(f"source_packet_review_status_not_expected:{summary.get('status')}")
    if review_receipt.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("source_packet_review_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"source_packet_review_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("metadata_source_packet_provided") is not False:
        failures.append("source_packet_already_provided")
    if summary.get("packet_present") is not False:
        failures.append("packet_present_unexpectedly")
    if summary.get("metadata_populated") is not False:
        failures.append("metadata_populated_unexpectedly")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")
    if summary.get("rule_refined") is not False:
        failures.append("rule_refined_unexpectedly")
    if summary.get("tie_broken") is not False:
        failures.append("tie_broken_unexpectedly")
    if summary.get("candidate_values_filled") is not False:
        failures.append("candidate_values_filled_unexpectedly")

    if review_result.get("review_status") != EXPECTED_REVIEW_STATUS:
        failures.append("review_result_status_wrong")
    if review_class.get("classification_status") != EXPECTED_REVIEW_STATUS:
        failures.append("review_classification_status_wrong")
    if review_roll.get("metadata_populated_count") != 0:
        failures.append("review_rollup_metadata_populated_nonzero")
    if review_profile.get("metadata_populated") is not False:
        failures.append("review_profile_metadata_populated_true")

    if contract.get("object_type") != "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET":
        failures.append("contract_object_type_wrong")
    if contract.get("required_packet_schema_version") != "typed_value_source_metadata_source_packet_v0":
        failures.append("contract_packet_schema_wrong")
    if missing_template.get("object_type_to_provide") != "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET":
        failures.append("missing_template_object_type_wrong")
    if source_template.get("object_type") != "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET":
        failures.append("source_packet_template_object_type_wrong")
    if field_policy.get("field_policy_status") != "TYPED_METADATA_FIELD_SOURCE_POLICIES_EMITTED":
        failures.append("field_policy_status_wrong")

    if bridge_receipt.get("receipt_id") != SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID or bridge_receipt.get("gate") != "PASS":
        failures.append("bridge_receipt_not_pass")
    if bridge_summary.get("status") != "TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_BUILT_REQUIRES_SOURCE_PACKET":
        failures.append("bridge_summary_status_wrong")

    return failures

def load_optional_values() -> Tuple[Dict[str, Any] | None, str | None, List[str]]:
    raw_json = os.environ.get(VALUES_ENV_JSON, "").strip()
    raw_path = os.environ.get(VALUES_ENV_PATH, "").strip()
    failures: List[str] = []

    if raw_json and raw_path:
        failures.append("both_values_json_and_values_path_provided")
        return None, None, failures

    if raw_json:
        try:
            return json.loads(raw_json), VALUES_ENV_JSON, []
        except Exception as exc:
            return None, VALUES_ENV_JSON, [f"values_json_parse_error:{exc}"]

    if raw_path:
        path = Path(raw_path)
        if not path.is_absolute():
            path = ROOT / path
        if not path.exists():
            return None, VALUES_ENV_PATH, [f"values_path_missing:{path.as_posix()}"]
        try:
            return read_json(path), path.as_posix(), []
        except Exception as exc:
            return None, path.as_posix(), [f"values_path_json_parse_error:{exc}"]

    return None, None, []

def source_packet_skeleton() -> Dict[str, Any]:
    missing_template = read_json(SOURCE_PACKET_MISSING_VALUES_TEMPLATE_PATH)
    skeleton = missing_template.get("copyable_packet_skeleton")
    if isinstance(skeleton, dict):
        return skeleton
    source_template = read_json(SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH)
    return {
        "schema_version": "typed_value_source_metadata_source_packet_v0",
        "object_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
        "source_bridge_receipt_id": SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID,
        "rows": source_template.get("rows", []),
        "assertions": {
            "target_selected_for_build": False,
            "accepted_for_build": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "rule_refined": False,
            "tie_broken": False,
            "candidate_values_filled": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        },
    }

def missing_field_inventory(packet: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = packet.get("rows", [])
    inventory: List[Dict[str, Any]] = []
    if not isinstance(rows, list):
        return inventory

    for row in rows:
        if not isinstance(row, dict):
            continue
        for item in row.get("missing_metadata_to_supply", []):
            if not isinstance(item, dict):
                continue
            inventory.append({
                "row_uid": row.get("row_uid"),
                "row_index": row.get("row_index"),
                "source_ref": row.get("source_ref"),
                "json_path": row.get("json_path"),
                "row_value": row.get("value"),
                "field": item.get("field"),
                "value": item.get("value"),
                "source_ref_for_field": item.get("source_ref"),
                "source_class": item.get("source_class"),
                "required_source_object": item.get("required_source_object"),
                "human_schema_only": item.get("human_schema_only"),
                "evidence_or_review_ref": item.get("evidence_or_review_ref"),
                "is_value_missing": item.get("value") in (None, ""),
                "is_source_ref_missing": item.get("source_ref") in (None, "") and item.get("evidence_or_review_ref") in (None, ""),
            })
    return inventory

def merge_values_into_skeleton(skeleton: Dict[str, Any], values: Dict[str, Any] | None) -> Tuple[Dict[str, Any], List[str], int]:
    if values is None:
        return skeleton, ["values_payload_not_provided"], 0

    merged = json.loads(json.dumps(skeleton))
    failures: List[str] = []
    filled = 0

    # Accepted shapes:
    # 1. full source packet object, already containing rows.
    # 2. {"rows": [...]} compatible with packet rows.
    # 3. {"values_by_row_uid": {"row_uid": {"field": {...}}}}
    if values.get("object_type") == "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET" and isinstance(values.get("rows"), list):
        merged = values
        inv = missing_field_inventory(merged)
        filled = sum(1 for item in inv if not item["is_value_missing"] and not item["is_source_ref_missing"])
        return merged, [], filled

    if isinstance(values.get("rows"), list):
        merged["rows"] = values["rows"]
        inv = missing_field_inventory(merged)
        filled = sum(1 for item in inv if not item["is_value_missing"] and not item["is_source_ref_missing"])
        return merged, [], filled

    by_uid = values.get("values_by_row_uid")
    if not isinstance(by_uid, dict):
        return merged, ["values_payload_shape_not_supported"], 0

    rows = merged.get("rows", [])
    if not isinstance(rows, list):
        return merged, ["skeleton_rows_not_list"], 0

    for row in rows:
        if not isinstance(row, dict):
            continue
        row_uid = str(row.get("row_uid"))
        row_values = by_uid.get(row_uid)
        if not isinstance(row_values, dict):
            continue
        items = row.get("missing_metadata_to_supply", [])
        if not isinstance(items, list):
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            field = str(item.get("field"))
            field_values = row_values.get(field)
            if not isinstance(field_values, dict):
                continue
            for key in ["value", "source_ref", "source_class", "evidence_or_review_ref", "notes"]:
                if key in field_values:
                    item[key] = field_values[key]
            if item.get("value") not in (None, "") and (item.get("source_ref") not in (None, "") or item.get("evidence_or_review_ref") not in (None, "")):
                filled += 1

    return merged, [], filled

def packet_shape_review(packet: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if packet.get("schema_version") != "typed_value_source_metadata_source_packet_v0":
        failures.append(f"packet_schema_version_wrong:{packet.get('schema_version')}")
    if packet.get("object_type") != "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET":
        failures.append(f"packet_object_type_wrong:{packet.get('object_type')}")
    if packet.get("source_bridge_receipt_id") != SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID:
        failures.append(f"source_bridge_receipt_id_wrong:{packet.get('source_bridge_receipt_id')}")
    if not isinstance(packet.get("rows"), list):
        failures.append("packet_rows_not_list")

    assertions = packet.get("assertions", {})
    for key in [
        "target_selected_for_build",
        "accepted_for_build",
        "runtime_patch_applied",
        "target_file_modified",
        "c5_opened",
        "rule_refined",
        "tie_broken",
        "candidate_values_filled",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if assertions.get(key) is not False:
            failures.append(f"packet_assertion_not_false:{key}:{assertions.get(key)}")
    if assertions.get("acceptance_boundary") != "human_or_prevalidated_schema_acceptance_required":
        failures.append("packet_acceptance_boundary_wrong")

    return failures

def field_fill_review(packet: Dict[str, Any]) -> Dict[str, Any]:
    inventory = missing_field_inventory(packet)
    total = len(inventory)
    value_present = sum(1 for item in inventory if not item["is_value_missing"])
    source_present = sum(1 for item in inventory if not item["is_source_ref_missing"])
    complete = sum(1 for item in inventory if not item["is_value_missing"] and not item["is_source_ref_missing"])

    missing_items = [
        item for item in inventory
        if item["is_value_missing"] or item["is_source_ref_missing"]
    ]

    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_missing_fields_v0",
        "missing_fields_status": "SOURCE_PACKET_VALUES_MISSING" if missing_items else "SOURCE_PACKET_VALUES_COMPLETE",
        "total_required_value_slots": total,
        "value_present_count": value_present,
        "source_present_count": source_present,
        "complete_value_slot_count": complete,
        "missing_value_slot_count": total - complete,
        "missing_items": missing_items,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def build_input_contract() -> Dict[str, Any]:
    contract = read_json(SOURCE_PACKET_CONTRACT_PATH)
    template = read_json(SOURCE_PACKET_MISSING_VALUES_TEMPLATE_PATH)
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_input_contract_v0",
        "contract_id": "source_packet_values_contract_" + sha8({
            "review": SOURCE_PACKET_REVIEW_RECEIPT_ID,
            "contract": contract.get("contract_id"),
            "template": template.get("template_id"),
        }),
        "source_packet_review_receipt_id": SOURCE_PACKET_REVIEW_RECEIPT_ID,
        "required_input_options": [
            {
                "env": VALUES_ENV_JSON,
                "type": "json_string",
                "description": "Full TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET, rows object, or values_by_row_uid map.",
            },
            {
                "env": VALUES_ENV_PATH,
                "type": "json_file_path",
                "description": "Path to a JSON object containing full source packet values.",
            },
        ],
        "required_packet_object_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
        "required_packet_schema_version": "typed_value_source_metadata_source_packet_v0",
        "source_packet_missing_values_template_ref": rel(SOURCE_PACKET_MISSING_VALUES_TEMPLATE_PATH),
        "forbidden_value_sources": [
            "latest-file guessing",
            "mtime selection",
            "row order",
            "untyped semantic inference",
            "hidden preference",
            "dominance rank score",
        ],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def build_request(values_source: str | None, values_errors: List[str]) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_request_v0",
        "request_id": "source_packet_values_request_" + sha8({
            "values_source": values_source,
            "errors": values_errors,
        }),
        "request_status": "SOURCE_PACKET_VALUES_REQUESTED",
        "values_source": values_source,
        "values_errors": values_errors,
        "required_env_json": VALUES_ENV_JSON,
        "required_env_path": VALUES_ENV_PATH,
        "missing_values_template_ref": rel(SOURCE_PACKET_MISSING_VALUES_TEMPLATE_PATH),
        "source_packet_contract_ref": rel(SOURCE_PACKET_CONTRACT_PATH),
        "recommended_next_if_missing": "PROVIDE_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUTS_V0",
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def build_review_intent(status: str, next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_review_intent_v0",
        "intent_status": status,
        "review_direction": "Only after values packet exists should the source-packet review runner be re-run with TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_PATH.",
        "next_review_unit": "PROVIDE_OR_REVIEW_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_V0",
        "next_edge": next_edge,
        "no_metadata_population": True,
        "no_discriminator_evaluation": True,
        "no_rule_refinement": True,
        "no_tie_break": True,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def classify(values_source: str | None, values_errors: List[str], shape_failures: List[str], missing: Dict[str, Any], filled_slots: int) -> Tuple[str, List[str], str]:
    reason_codes: List[str] = []

    if values_errors:
        status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUT_INVALID"
        reason_codes.extend(["SOURCE_PACKET_VALUES_INPUT_INVALID"] + values_errors)
        next_edge = "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUTS_V0"
        return status, reason_codes, next_edge

    if values_source is None:
        status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_NOT_PROVIDED"
        reason_codes.extend([
            "SOURCE_PACKET_VALUES_INPUT_CONTRACT_EMITTED",
            "SOURCE_PACKET_VALUES_JSON_OR_PATH_NOT_PROVIDED",
            "SOURCE_PACKET_VALUES_REQUIRED_BEFORE_PACKET_REVIEW",
        ])
        next_edge = "PROVIDE_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUTS_V0"
        return status, reason_codes, next_edge

    if shape_failures:
        status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_SHAPE_INVALID"
        reason_codes.extend(["SOURCE_PACKET_VALUES_SHAPE_INVALID"] + shape_failures)
        next_edge = "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUTS_V0"
        return status, reason_codes, next_edge

    if missing.get("missing_value_slot_count", 0) > 0:
        status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INCOMPLETE"
        reason_codes.extend([
            "SOURCE_PACKET_VALUES_PARTIALLY_PROVIDED",
            "SOURCE_PACKET_VALUES_STILL_MISSING_SLOTS",
            "SOURCE_PACKET_NOT_READY_FOR_REVIEW",
        ])
        next_edge = "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_INPUTS_V0"
        return status, reason_codes, next_edge

    status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_PACKET_MATERIALIZED_FOR_REVIEW"
    reason_codes.extend([
        "SOURCE_PACKET_VALUES_PROVIDED",
        "SOURCE_PACKET_VALUES_COMPLETE",
        "SOURCE_PACKET_READY_FOR_REVIEW_NOT_METADATA_POPULATION",
    ])
    next_edge = "RERUN_PROVIDE_OR_REVIEW_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_WITH_VALUES_PATH_V0"
    return status, reason_codes, next_edge

def classification_obj(status: str, reason_codes: List[str], next_edge: str, values_source: str | None, packet_present: bool, missing: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "values_source": values_source,
        "values_packet_present": packet_present,
        "complete_value_slot_count": missing.get("complete_value_slot_count", 0),
        "missing_value_slot_count": missing.get("missing_value_slot_count", 0),
        "metadata_source_packet_materialized_for_review": status == "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_PACKET_MATERIALIZED_FOR_REVIEW",
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "real_tie_proven": False,
        "rule_refined": False,
        "tie_broken": False,
        "candidate_values_filled": False,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_authority_boundary_v0",
        "status": status,
        "may_emit_values_input_contract": True,
        "may_emit_values_request": True,
        "may_materialize_source_packet_for_review_from_explicit_values": True,
        "may_populate_metadata": False,
        "may_evaluate_discriminators": False,
        "may_refine_rule": False,
        "may_break_tie": False,
        "may_emit_candidate_values": False,
        "may_declare_target_candidate_for_review": False,
        "may_select_target_for_build": False,
        "may_accept_for_build": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def rollup_obj(status: str, values_source: str | None, missing: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "input_contract_emitted_count": 1,
        "values_request_emitted_count": 1,
        "values_packet_draft_emitted_count": 1,
        "missing_fields_emitted_count": 1,
        "values_input_present_count": 1 if values_source else 0,
        "source_packet_materialized_for_review_count": 1 if status == "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_PACKET_MATERIALIZED_FOR_REVIEW" else 0,
        "complete_value_slot_count": missing.get("complete_value_slot_count", 0),
        "missing_value_slot_count": missing.get("missing_value_slot_count", 0),
        "metadata_populated_count": 0,
        "ready_discriminator_count": 0,
        "rule_refined_count": 0,
        "tie_broken_count": 0,
        "candidate_values_filled_count": 0,
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
        "recommended_next": next_edge,
    }

def profile_obj(roll: Dict[str, Any]) -> Dict[str, Any]:
    zero_keys = [
        "metadata_populated_count",
        "ready_discriminator_count",
        "rule_refined_count",
        "tie_broken_count",
        "candidate_values_filled_count",
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
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_profile_v0",
        "profile_id": "metadata_source_packet_values_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "values_input_contract_emitted": True,
        "values_input_present": roll["values_input_present_count"] == 1,
        "source_packet_materialized_for_review": roll["source_packet_materialized_for_review_count"] == 1,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "rule_refined": False,
        "tie_broken": False,
        "candidate_values_filled": False,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(roll.get(k) == 0 for k in zero_keys),
        "recommended_next": roll["recommended_next"],
        "next_command_goal": None,
    }

def report_obj(status: str, reason_codes: List[str], values_source: str | None, missing: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Packet review proved source packet was not provided; this unit emits the values input contract and materializes a packet only from explicit supplied values.",
        "values_source": values_source,
        "complete_value_slot_count": missing.get("complete_value_slot_count", 0),
        "missing_value_slot_count": missing.get("missing_value_slot_count", 0),
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "metadata_populated_count": 0,
        "ready_discriminator_count": 0,
        "rule_refined_count": 0,
        "tie_broken_count": 0,
        "candidate_values_filled_count": 0,
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

def transition_trace_obj(status: str, reason_codes: List[str], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_values_transition_trace_v0",
        "trace": [
            {
                "step": "consume_missing_packet_review",
                "question": "what did the packet review prove",
                "answer": "source packet template exists but values packet was not provided",
                "taken": "emit values input contract",
            },
            {
                "step": "check_values_input",
                "question": "were explicit source-packet values supplied",
                "answer": status,
                "reason_codes": reason_codes,
                "taken": next_edge,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    input_contract = build_input_contract() if not failures else {
        "schema_version": "typed_value_source_metadata_source_packet_values_input_contract_v0",
        "contract_id": "source_packet_values_contract_source_fail_" + sha8(failures),
        "source_packet_review_receipt_id": SOURCE_PACKET_REVIEW_RECEIPT_ID,
        "required_input_options": [],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    values, values_source, values_errors = load_optional_values()
    skeleton = source_packet_skeleton() if not failures else {
        "schema_version": "typed_value_source_metadata_source_packet_v0",
        "object_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
        "source_bridge_receipt_id": SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID,
        "rows": [],
        "assertions": {
            "target_selected_for_build": False,
            "accepted_for_build": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "rule_refined": False,
            "tie_broken": False,
            "candidate_values_filled": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        },
    }

    packet, merge_failures, filled_slots = merge_values_into_skeleton(skeleton, values)
    shape_failures = packet_shape_review(packet) if values is not None and not merge_failures else []
    missing = field_fill_review(packet)

    if failures:
        status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_SOURCE_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_BASIS_V0"
    else:
        status, reason_codes, next_edge = classify(values_source, values_errors + merge_failures, shape_failures, missing, filled_slots)

    request = build_request(values_source, values_errors + merge_failures + shape_failures)
    review_intent = build_review_intent(status, next_edge)
    classif = classification_obj(status, reason_codes, next_edge, values_source, values is not None, missing)
    boundary = authority_boundary_obj(status)
    roll = rollup_obj(status, values_source, missing, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, values_source, missing, next_edge)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    write_json(VALUES_INPUT_CONTRACT_PATH, input_contract)
    write_json(VALUES_REQUEST_PATH, request)
    write_json(VALUES_PACKET_DRAFT_PATH, packet)
    write_json(VALUES_MISSING_FIELDS_PATH, missing)
    write_json(VALUES_REVIEW_INTENT_PATH, review_intent)
    write_json(CLASSIFICATION_PATH, classif)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, roll)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(TRANSITION_TRACE_PATH, trace)

    env_text = f'''# typed value-source metadata source packet values v0
# Provide exactly one of these before re-running {UNIT_ID}.
# JSON string form:
# export {VALUES_ENV_JSON}='{{"values_by_row_uid":{{}}}}'
#
# File path form:
# export {VALUES_ENV_PATH}="{rel(VALUES_PACKET_DRAFT_PATH)}"
#
# After a complete packet is materialized, re-run packet review using:
# export TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_PATH="{rel(VALUES_PACKET_DRAFT_PATH)}"
'''
    write_text(VALUES_ENV_TEMPLATE_PATH, env_text)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        roll["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, roll)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "SOURCE_PACKET_VALUES_0_REVIEW_RECEIPT_CONSUMED": SOURCE_PACKET_REVIEW_RECEIPT_PATH.exists(),
        "SOURCE_PACKET_VALUES_1_CONTRACT_CONSUMED": SOURCE_PACKET_CONTRACT_PATH.exists(),
        "SOURCE_PACKET_VALUES_2_MISSING_TEMPLATE_CONSUMED": SOURCE_PACKET_MISSING_VALUES_TEMPLATE_PATH.exists(),
        "SOURCE_PACKET_VALUES_3_VALUES_INPUT_CONTRACT_EMITTED": VALUES_INPUT_CONTRACT_PATH.exists(),
        "SOURCE_PACKET_VALUES_4_VALUES_REQUEST_EMITTED": VALUES_REQUEST_PATH.exists(),
        "SOURCE_PACKET_VALUES_5_VALUES_PACKET_DRAFT_EMITTED": VALUES_PACKET_DRAFT_PATH.exists(),
        "SOURCE_PACKET_VALUES_6_VALUES_MISSING_FIELDS_EMITTED": VALUES_MISSING_FIELDS_PATH.exists(),
        "SOURCE_PACKET_VALUES_7_VALUES_REVIEW_INTENT_EMITTED": VALUES_REVIEW_INTENT_PATH.exists(),
        "SOURCE_PACKET_VALUES_8_ENV_TEMPLATE_EMITTED": VALUES_ENV_TEMPLATE_PATH.exists(),
        "SOURCE_PACKET_VALUES_9_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "SOURCE_PACKET_VALUES_10_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "SOURCE_PACKET_VALUES_11_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "SOURCE_PACKET_VALUES_12_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "SOURCE_PACKET_VALUES_13_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "SOURCE_PACKET_VALUES_14_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classif["target_candidate_declared_for_review"] is False,
        "SOURCE_PACKET_VALUES_15_NO_TARGET_SELECTED_FOR_BUILD": classif["target_selected_for_build"] is False,
        "SOURCE_PACKET_VALUES_16_NO_ACCEPTED_FOR_BUILD": classif["accepted_for_build"] is False,
        "SOURCE_PACKET_VALUES_17_NO_RUNTIME_PATCH": classif["runtime_patch_authorized"] is False,
        "SOURCE_PACKET_VALUES_18_NO_TARGET_FILE_MODIFICATION": classif["target_file_modification_authorized"] is False,
        "SOURCE_PACKET_VALUES_19_NO_C5_OPENED": classif["c5_authorized"] is False,
        "SOURCE_PACKET_VALUES_20_NO_GENERAL_CELL1_AUTHORITY": classif["general_cell1_authority_granted"] is False,
        "SOURCE_PACKET_VALUES_21_NO_LATEST_FILE_GUESSING": classif["latest_file_guessing"] is False,
        "SOURCE_PACKET_VALUES_22_NO_MTIME_SELECTION": classif["mtime_selection"] is False,
        "SOURCE_PACKET_VALUES_23_NO_HIDDEN_NEXT_COMMAND": classif["next_command_goal"] is None,
        "SOURCE_PACKET_VALUES_24_ACCEPTANCE_BOUNDARY_RETAINED": classif["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "SOURCE_PACKET_VALUES_25_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "values_source": values_source,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_value_source_metadata_source_packet_values_receipt_v0",
        "receipt_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_packet_review_receipt_id": SOURCE_PACKET_REVIEW_RECEIPT_ID,
        "source_metadata_source_bridge_receipt_id": SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID,
        "typed_metadata_source_packet_values_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "values_source": values_source,
            "values_input_present": values_source is not None,
            "values_errors": values_errors + merge_failures + shape_failures,
            "complete_value_slot_count": missing.get("complete_value_slot_count", 0),
            "missing_value_slot_count": missing.get("missing_value_slot_count", 0),
            "source_packet_materialized_for_review": status == "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_PACKET_MATERIALIZED_FOR_REVIEW",
            "metadata_populated": False,
            "ready_discriminator_count": 0,
            "real_tie_proven": False,
            "rule_refined": False,
            "tie_broken": False,
            "candidate_values_filled": False,
            "target_candidate_declared_for_review": False,
            "target_selected_for_build": False,
            "accepted_for_build": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
            "bad_counters_zero": prof["bad_counters_zero"],
            "recommended_next": next_edge,
        },
        "aggregate_metrics": rep,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "values_input_contract": rel(VALUES_INPUT_CONTRACT_PATH),
            "values_request": rel(VALUES_REQUEST_PATH),
            "values_env_template": rel(VALUES_ENV_TEMPLATE_PATH),
            "values_packet_draft": rel(VALUES_PACKET_DRAFT_PATH),
            "values_missing_fields": rel(VALUES_MISSING_FIELDS_PATH),
            "values_review_intent": rel(VALUES_REVIEW_INTENT_PATH),
            "classification": rel(CLASSIFICATION_PATH),
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
    print(f"metadata_source_packet_values_receipt_id={receipt_id}")
    print(f"metadata_source_packet_values_receipt_path={rel(receipt_path)}")
    print(f"metadata_source_packet_values_input_contract_path={rel(VALUES_INPUT_CONTRACT_PATH)}")
    print(f"metadata_source_packet_values_request_path={rel(VALUES_REQUEST_PATH)}")
    print(f"metadata_source_packet_values_env_template_path={rel(VALUES_ENV_TEMPLATE_PATH)}")
    print(f"metadata_source_packet_values_packet_draft_path={rel(VALUES_PACKET_DRAFT_PATH)}")
    print(f"metadata_source_packet_values_missing_fields_path={rel(VALUES_MISSING_FIELDS_PATH)}")
    print(f"metadata_source_packet_values_review_intent_path={rel(VALUES_REVIEW_INTENT_PATH)}")
    print(f"metadata_source_packet_values_rollup_path={rel(ROLLUP_PATH)}")
    print(f"metadata_source_packet_values_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
