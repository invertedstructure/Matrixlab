#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PROVIDE_OR_REVIEW_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_packet_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_PACKET_REVIEW"
MODE = "SOURCE_PACKET_INTAKE_OR_REVIEW / NO_METADATA_FILL / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "TYPED_METADATA_SOURCE_PACKET_REVIEW_ONLY"

SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID = "68a12602"
SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0_receipts/68a12602.json"
SOURCE_METADATA_SOURCE_BRIDGE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_bridge_v0.json"
SOURCE_METADATA_SOURCE_FIELD_POLICY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_field_policy_v0.json"
SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_packet_template_v0.json"
SOURCE_METADATA_ROW_SOURCE_REQUIREMENTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_row_source_requirements_v0.json"
SOURCE_METADATA_HUMAN_SCHEMA_ONLY_FIELDS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_human_schema_only_fields_v0.json"
SOURCE_METADATA_SOURCE_BRIDGE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_bridge_classification_v0.json"
SOURCE_METADATA_SOURCE_BRIDGE_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_bridge_rollup_v0.json"
SOURCE_METADATA_SOURCE_BRIDGE_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_bridge_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_review_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_review_v0_receipts"

SOURCE_PACKET_CONTRACT_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_contract_v0.json"
SOURCE_PACKET_REVIEW_REQUEST_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_review_request_v0.json"
SOURCE_PACKET_REVIEW_RESULT_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_review_result_v0.json"
SOURCE_PACKET_MISSING_VALUES_TEMPLATE_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_missing_values_template_v0.json"
SOURCE_PACKET_FIELD_REVIEW_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_field_review_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_review_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_review_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_value_source_metadata_source_packet_review_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_PATH,
    SOURCE_METADATA_SOURCE_BRIDGE_PATH,
    SOURCE_METADATA_SOURCE_FIELD_POLICY_PATH,
    SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH,
    SOURCE_METADATA_ROW_SOURCE_REQUIREMENTS_PATH,
    SOURCE_METADATA_HUMAN_SCHEMA_ONLY_FIELDS_PATH,
    SOURCE_METADATA_SOURCE_BRIDGE_CLASSIFICATION_PATH,
    SOURCE_METADATA_SOURCE_BRIDGE_ROLLUP_PATH,
    SOURCE_METADATA_SOURCE_BRIDGE_PROFILE_PATH,
]

EXPECTED_BRIDGE_STATUS = "TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_BUILT_REQUIRES_SOURCE_PACKET"
EXPECTED_BRIDGE_STOP = "STOP_TYPED_VALUE_SOURCE_METADATA_SOURCE_BRIDGE_BUILT_REQUIRES_SOURCE_PACKET"
EXPECTED_NEXT = "PROVIDE_OR_REVIEW_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_V0"

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

def normalize_optional_packet_path() -> Path | None:
    raw = os.environ.get("TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_PATH", "").strip()
    if not raw:
        return None
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / path
    return path

def validate_source_basis() -> List[str]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    bridge_receipt = read_json(SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_PATH)
    bridge = read_json(SOURCE_METADATA_SOURCE_BRIDGE_PATH)
    template = read_json(SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH)
    field_policy = read_json(SOURCE_METADATA_SOURCE_FIELD_POLICY_PATH)
    human_schema = read_json(SOURCE_METADATA_HUMAN_SCHEMA_ONLY_FIELDS_PATH)
    classif = read_json(SOURCE_METADATA_SOURCE_BRIDGE_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_METADATA_SOURCE_BRIDGE_ROLLUP_PATH)
    prof = read_json(SOURCE_METADATA_SOURCE_BRIDGE_PROFILE_PATH)

    summary = bridge_receipt.get("typed_metadata_source_bridge_summary", {})

    if bridge_receipt.get("receipt_id") != SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID or bridge_receipt.get("gate") != "PASS":
        failures.append("metadata_source_bridge_receipt_not_pass")
    if summary.get("status") != EXPECTED_BRIDGE_STATUS:
        failures.append(f"source_bridge_status_not_expected:{summary.get('status')}")
    if bridge_receipt.get("terminal", {}).get("stop_code") != EXPECTED_BRIDGE_STOP:
        failures.append("source_bridge_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"source_bridge_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("source_packet_template_emitted") is not True:
        failures.append("source_packet_template_not_emitted")
    if summary.get("metadata_source_packet_provided") is not False:
        failures.append("source_packet_already_provided")
    if summary.get("metadata_populated") is not False:
        failures.append("bridge_populated_metadata")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("bridge_ready_discriminator_nonzero")
    if summary.get("rule_refined") is not False:
        failures.append("bridge_refined_rule")
    if summary.get("tie_broken") is not False:
        failures.append("bridge_broke_tie")
    if summary.get("candidate_values_filled") is not False:
        failures.append("bridge_filled_candidate_values")

    if bridge.get("bridge_status") != EXPECTED_BRIDGE_STATUS:
        failures.append("source_bridge_artifact_status_wrong")
    if template.get("object_type") != "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET":
        failures.append("source_packet_template_object_type_wrong")
    if template.get("template_status") != "SOURCE_PACKET_TEMPLATE_EMITTED":
        failures.append("source_packet_template_status_wrong")
    if field_policy.get("field_policy_status") != "TYPED_METADATA_FIELD_SOURCE_POLICIES_EMITTED":
        failures.append("field_policy_status_wrong")
    if human_schema.get("status") != "HUMAN_OR_SCHEMA_ONLY_FIELDS_IDENTIFIED":
        failures.append("human_schema_only_fields_status_wrong")
    if classif.get("classification_status") != EXPECTED_BRIDGE_STATUS:
        failures.append("source_bridge_classification_status_wrong")
    if roll.get("metadata_source_packet_provided_count") != 0:
        failures.append("rollup_source_packet_provided_nonzero")
    if prof.get("metadata_source_packet_provided") is not False:
        failures.append("profile_source_packet_provided_true")

    return failures

def expected_template_rows() -> List[Dict[str, Any]]:
    template = read_json(SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH)
    rows = template.get("rows", [])
    return [r for r in rows if isinstance(r, dict)]

def field_policies_by_field() -> Dict[str, Dict[str, Any]]:
    policy = read_json(SOURCE_METADATA_SOURCE_FIELD_POLICY_PATH)
    policies = policy.get("field_policies", [])
    out = {}
    for p in policies:
        if isinstance(p, dict) and p.get("field"):
            out[str(p["field"])] = p
    return out

def build_contract() -> Dict[str, Any]:
    template = read_json(SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH)
    field_policy = read_json(SOURCE_METADATA_SOURCE_FIELD_POLICY_PATH)
    human_schema = read_json(SOURCE_METADATA_HUMAN_SCHEMA_ONLY_FIELDS_PATH)

    return {
        "schema_version": "typed_value_source_metadata_source_packet_contract_v0",
        "contract_id": "metadata_source_packet_contract_" + sha8({
            "template": template.get("template_id"),
            "field_policy": field_policy.get("field_policy_id"),
        }),
        "object_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
        "source_bridge_receipt_id": SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID,
        "required_packet_schema_version": "typed_value_source_metadata_source_packet_v0",
        "required_packet_object_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
        "required_row_count": template.get("row_count"),
        "required_rows_must_preserve_row_uid": True,
        "required_fields": [
            {
                "field": p.get("field"),
                "source_class": p.get("source_class"),
                "human_schema_only": p.get("human_schema_only"),
                "allowed_sources": p.get("allowed_sources"),
                "required_source_object": p.get("required_source_object"),
            }
            for p in field_policy.get("field_policies", [])
            if p.get("currently_missing")
        ],
        "human_schema_only_fields": [f.get("field") for f in human_schema.get("fields", [])],
        "forbidden_packet_behaviors": [
            "select target",
            "accept target for build",
            "apply runtime patch",
            "modify target files",
            "open C5",
            "refine dominance rule",
            "break tie",
            "fill candidate values",
            "use latest-file guessing",
            "use mtime selection",
            "use untyped semantic inference"
        ],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def build_review_request(packet_path: Path | None) -> Dict[str, Any]:
    template = read_json(SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH)
    bridge = read_json(SOURCE_METADATA_SOURCE_BRIDGE_PATH)

    return {
        "schema_version": "typed_value_source_metadata_source_packet_review_request_v0",
        "request_id": "metadata_source_packet_review_request_" + sha8({
            "bridge": bridge.get("source_bridge_id"),
            "template": template.get("template_id"),
            "packet_path": packet_path.as_posix() if packet_path else None,
        }),
        "request_status": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_REVIEW_REQUESTED",
        "source_bridge_receipt_id": SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID,
        "source_packet_template_ref": rel(SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH),
        "packet_path_env": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_PATH",
        "provided_packet_path": packet_path.as_posix() if packet_path else None,
        "required_object_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
        "required_contract_ref": rel(SOURCE_PACKET_CONTRACT_PATH),
        "if_packet_missing": "emit typed missing-packet halt; do not synthesize metadata",
        "recommended_next_if_missing": "PROVIDE_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_V0",
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def build_missing_values_template() -> Dict[str, Any]:
    template = read_json(SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH)
    return {
        "schema_version": "typed_value_source_metadata_source_packet_missing_values_template_v0",
        "template_id": "metadata_source_packet_missing_values_" + sha8(template),
        "source_packet_template_ref": rel(SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH),
        "object_type_to_provide": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
        "packet_schema_version_to_provide": "typed_value_source_metadata_source_packet_v0",
        "copyable_packet_skeleton": {
            "schema_version": "typed_value_source_metadata_source_packet_v0",
            "object_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
            "source_bridge_receipt_id": SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID,
            "rows": template.get("rows", []),
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
                "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required"
            }
        },
        "fill_rule": "Only replace null field values from explicit typed source refs, human review packet, or prevalidated schema packet.",
        "forbidden_fill_rule": "Do not infer missing field values from vibes, row order, latest file, mtime, or hidden preference.",
        "recommended_next": "PROVIDE_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_V0",
    }

def packet_row_map(packet: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
    rows = packet.get("rows", [])
    out = {}
    if isinstance(rows, list):
        for row in rows:
            if isinstance(row, dict) and row.get("row_uid"):
                out[str(row["row_uid"])] = row
    return out

def validate_packet(packet: Dict[str, Any], packet_path: Path) -> Tuple[List[Dict[str, Any]], List[str], bool]:
    failures: List[str] = []
    field_reviews: List[Dict[str, Any]] = []

    contract = build_contract()
    expected_rows = expected_template_rows()
    policy = field_policies_by_field()
    rows_by_uid = packet_row_map(packet)

    if packet.get("schema_version") != contract["required_packet_schema_version"]:
        failures.append(f"packet_schema_version_wrong:{packet.get('schema_version')}")
    if packet.get("object_type") != contract["required_packet_object_type"]:
        failures.append(f"packet_object_type_wrong:{packet.get('object_type')}")
    if packet.get("source_bridge_receipt_id") != SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID:
        failures.append(f"packet_source_bridge_receipt_id_wrong:{packet.get('source_bridge_receipt_id')}")
    if not isinstance(packet.get("rows"), list):
        failures.append("packet_rows_missing_or_not_list")

    for expected_row in expected_rows:
        row_uid = expected_row.get("row_uid")
        provided_row = rows_by_uid.get(str(row_uid))
        if provided_row is None:
            failures.append(f"missing_row_uid:{row_uid}")
            continue

        missing_items = expected_row.get("missing_metadata_to_supply", [])
        provided_items = provided_row.get("missing_metadata_to_supply", [])
        provided_by_field = {
            str(item.get("field")): item
            for item in provided_items
            if isinstance(item, dict) and item.get("field")
        }

        for expected_item in missing_items:
            field = str(expected_item.get("field"))
            provided_item = provided_by_field.get(field)
            pol = policy.get(field, {})

            if provided_item is None:
                failures.append(f"missing_field_for_row:{row_uid}:{field}")
                field_reviews.append({
                    "row_uid": row_uid,
                    "field": field,
                    "status": "MISSING_FIELD_ENTRY",
                    "usable_for_population": False,
                })
                continue

            value = provided_item.get("value")
            source_ref = provided_item.get("source_ref")
            source_class = provided_item.get("source_class")
            evidence_or_review_ref = provided_item.get("evidence_or_review_ref")

            item_failures = []
            if value in (None, ""):
                item_failures.append("value_missing")
            if source_ref in (None, "") and evidence_or_review_ref in (None, ""):
                item_failures.append("source_or_review_ref_missing")
            if source_class != expected_item.get("source_class"):
                item_failures.append(f"source_class_mismatch:{source_class}!={expected_item.get('source_class')}")
            if pol.get("human_schema_only") is True and evidence_or_review_ref in (None, ""):
                item_failures.append("human_schema_field_requires_review_ref")

            status = "FIELD_REVIEW_PASS" if not item_failures else "FIELD_REVIEW_FAIL"
            if item_failures:
                failures.extend([f"field_review_fail:{row_uid}:{field}:{x}" for x in item_failures])

            field_reviews.append({
                "row_uid": row_uid,
                "field": field,
                "status": status,
                "item_failures": item_failures,
                "value_present": value not in (None, ""),
                "source_ref_present": source_ref not in (None, ""),
                "evidence_or_review_ref_present": evidence_or_review_ref not in (None, ""),
                "source_class": source_class,
                "human_schema_only": pol.get("human_schema_only"),
                "usable_for_population": status == "FIELD_REVIEW_PASS",
            })

    assertion_failures = []
    assertions = packet.get("assertions", {})
    expected_false = [
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
    ]
    for key in expected_false:
        if assertions.get(key) is not False:
            assertion_failures.append(key)
    if assertions.get("acceptance_boundary") != "human_or_prevalidated_schema_acceptance_required":
        assertion_failures.append("acceptance_boundary")

    if assertion_failures:
        failures.extend([f"packet_assertion_invalid:{x}" for x in assertion_failures])

    valid = len(failures) == 0
    return field_reviews, failures, valid

def review_packet(packet_path: Path | None) -> Tuple[Dict[str, Any], Dict[str, Any], str, List[str], str]:
    if packet_path is None:
        result = {
            "schema_version": "typed_value_source_metadata_source_packet_review_result_v0",
            "review_status": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_NOT_PROVIDED",
            "provided_packet_path": None,
            "packet_present": False,
            "packet_valid": False,
            "field_review_count": 0,
            "field_review_pass_count": 0,
            "field_review_fail_count": 0,
            "review_failures": ["metadata_source_packet_path_not_provided"],
            "metadata_source_packet_provided": False,
            "metadata_source_packet_valid": False,
            "metadata_populated": False,
            "ready_discriminator_count": 0,
            "recommended_next": "PROVIDE_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_V0",
        }
        field_review = {
            "schema_version": "typed_value_source_metadata_source_packet_field_review_v0",
            "field_review_status": "PACKET_NOT_PROVIDED",
            "field_reviews": [],
        }
        status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_NOT_PROVIDED"
        reason_codes = [
            "SOURCE_PACKET_TEMPLATE_EXISTS",
            "SOURCE_PACKET_PATH_NOT_PROVIDED",
            "METADATA_SOURCE_PACKET_REQUIRED_BEFORE_POPULATION",
        ]
        next_edge = "PROVIDE_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_V0"
        return result, field_review, status, reason_codes, next_edge

    if not packet_path.exists():
        result = {
            "schema_version": "typed_value_source_metadata_source_packet_review_result_v0",
            "review_status": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_PATH_MISSING",
            "provided_packet_path": packet_path.as_posix(),
            "packet_present": False,
            "packet_valid": False,
            "field_review_count": 0,
            "field_review_pass_count": 0,
            "field_review_fail_count": 0,
            "review_failures": [f"provided_packet_path_missing:{packet_path.as_posix()}"],
            "metadata_source_packet_provided": False,
            "metadata_source_packet_valid": False,
            "metadata_populated": False,
            "ready_discriminator_count": 0,
            "recommended_next": "PROVIDE_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_V0",
        }
        field_review = {
            "schema_version": "typed_value_source_metadata_source_packet_field_review_v0",
            "field_review_status": "PACKET_PATH_MISSING",
            "field_reviews": [],
        }
        status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_PATH_MISSING"
        reason_codes = [
            "SOURCE_PACKET_TEMPLATE_EXISTS",
            "PROVIDED_SOURCE_PACKET_PATH_MISSING",
            "METADATA_SOURCE_PACKET_REQUIRED_BEFORE_POPULATION",
        ]
        next_edge = "PROVIDE_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_VALUES_V0"
        return result, field_review, status, reason_codes, next_edge

    try:
        packet = read_json(packet_path)
    except Exception as exc:
        result = {
            "schema_version": "typed_value_source_metadata_source_packet_review_result_v0",
            "review_status": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_JSON_INVALID",
            "provided_packet_path": packet_path.as_posix(),
            "packet_present": True,
            "packet_valid": False,
            "field_review_count": 0,
            "field_review_pass_count": 0,
            "field_review_fail_count": 0,
            "review_failures": [f"json_parse_error:{exc}"],
            "metadata_source_packet_provided": True,
            "metadata_source_packet_valid": False,
            "metadata_populated": False,
            "ready_discriminator_count": 0,
            "recommended_next": "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_V0",
        }
        field_review = {
            "schema_version": "typed_value_source_metadata_source_packet_field_review_v0",
            "field_review_status": "PACKET_JSON_INVALID",
            "field_reviews": [],
        }
        status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_JSON_INVALID"
        reason_codes = ["SOURCE_PACKET_JSON_INVALID"]
        next_edge = "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_V0"
        return result, field_review, status, reason_codes, next_edge

    field_reviews, review_failures, valid = validate_packet(packet, packet_path)
    pass_count = sum(1 for item in field_reviews if item.get("status") == "FIELD_REVIEW_PASS")
    fail_count = sum(1 for item in field_reviews if item.get("status") != "FIELD_REVIEW_PASS")

    if valid:
        status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_REVIEWED_VALID"
        reason_codes = [
            "SOURCE_PACKET_PROVIDED",
            "SOURCE_PACKET_CONFORMS_TO_TEMPLATE",
            "ALL_REQUIRED_FIELD_SOURCES_PRESENT",
            "READY_FOR_METADATA_POPULATION_FROM_REVIEWED_SOURCE_PACKET",
        ]
        next_edge = "POPULATE_TYPED_VALUE_SOURCE_METADATA_FROM_SOURCE_PACKET_V0"
    else:
        status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_REVIEWED_INVALID"
        reason_codes = [
            "SOURCE_PACKET_PROVIDED",
            "SOURCE_PACKET_FAILED_REVIEW",
            "REPAIR_SOURCE_PACKET_REQUIRED",
        ]
        next_edge = "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_V0"

    result = {
        "schema_version": "typed_value_source_metadata_source_packet_review_result_v0",
        "review_status": status,
        "provided_packet_path": packet_path.as_posix(),
        "packet_present": True,
        "packet_valid": valid,
        "field_review_count": len(field_reviews),
        "field_review_pass_count": pass_count,
        "field_review_fail_count": fail_count,
        "review_failures": review_failures,
        "metadata_source_packet_provided": True,
        "metadata_source_packet_valid": valid,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "recommended_next": next_edge,
    }

    field_review = {
        "schema_version": "typed_value_source_metadata_source_packet_field_review_v0",
        "field_review_status": "FIELD_REVIEW_PASS" if valid else "FIELD_REVIEW_FAIL",
        "provided_packet_path": packet_path.as_posix(),
        "field_reviews": field_reviews,
    }

    return result, field_review, status, reason_codes, next_edge

def classification_obj(status: str, reason_codes: List[str], next_edge: str, result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "packet_present": result.get("packet_present"),
        "packet_valid": result.get("packet_valid"),
        "field_review_count": result.get("field_review_count"),
        "field_review_pass_count": result.get("field_review_pass_count"),
        "field_review_fail_count": result.get("field_review_fail_count"),
        "metadata_source_packet_provided": result.get("metadata_source_packet_provided"),
        "metadata_source_packet_valid": result.get("metadata_source_packet_valid"),
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
        "schema_version": "typed_value_source_metadata_source_packet_review_authority_boundary_v0",
        "status": status,
        "may_review_source_packet": True,
        "may_emit_missing_values_template": True,
        "may_validate_source_packet_shape": True,
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

def rollup_obj(status: str, result: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "contract_emitted_count": 1,
        "review_request_emitted_count": 1,
        "review_result_emitted_count": 1,
        "missing_values_template_emitted_count": 1,
        "packet_present_count": 1 if result.get("packet_present") else 0,
        "packet_valid_count": 1 if result.get("packet_valid") else 0,
        "field_review_count": result.get("field_review_count", 0),
        "field_review_pass_count": result.get("field_review_pass_count", 0),
        "field_review_fail_count": result.get("field_review_fail_count", 0),
        "metadata_source_packet_provided_count": 1 if result.get("metadata_source_packet_provided") else 0,
        "metadata_source_packet_valid_count": 1 if result.get("metadata_source_packet_valid") else 0,
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
        "schema_version": "typed_value_source_metadata_source_packet_review_profile_v0",
        "profile_id": "metadata_source_packet_review_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "source_packet_reviewed": True,
        "metadata_source_packet_provided": roll["metadata_source_packet_provided_count"] == 1,
        "metadata_source_packet_valid": roll["metadata_source_packet_valid_count"] == 1,
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

def report_obj(status: str, reason_codes: List[str], result: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_source_packet_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Source bridge requires a typed metadata source packet; this unit only reviews/proves whether that packet is present and valid.",
        "packet_present": result.get("packet_present"),
        "packet_valid": result.get("packet_valid"),
        "field_review_count": result.get("field_review_count"),
        "field_review_pass_count": result.get("field_review_pass_count"),
        "field_review_fail_count": result.get("field_review_fail_count"),
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
        "schema_version": "typed_value_source_metadata_source_packet_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_source_bridge",
                "question": "what does the bridge require",
                "answer": "typed metadata source packet",
                "taken": "review provided packet path or emit missing-packet halt",
            },
            {
                "step": "review_source_packet",
                "question": "is source packet present and valid",
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

    packet_path = normalize_optional_packet_path()

    contract = build_contract() if not failures else {
        "schema_version": "typed_value_source_metadata_source_packet_contract_v0",
        "contract_id": "metadata_source_packet_contract_source_fail_" + sha8(failures),
        "object_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
        "source_bridge_receipt_id": SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID,
        "required_packet_schema_version": "typed_value_source_metadata_source_packet_v0",
        "required_packet_object_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
        "required_row_count": 0,
        "required_fields": [],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }
    review_request = build_review_request(packet_path) if not failures else {
        "schema_version": "typed_value_source_metadata_source_packet_review_request_v0",
        "request_status": "SOURCE_BASIS_FAIL",
        "provided_packet_path": packet_path.as_posix() if packet_path else None,
        "recommended_next_if_missing": "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_REVIEW_BASIS_V0",
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }
    missing_template = build_missing_values_template() if not failures else {
        "schema_version": "typed_value_source_metadata_source_packet_missing_values_template_v0",
        "template_id": "metadata_source_packet_missing_values_source_fail_" + sha8(failures),
        "object_type_to_provide": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET",
        "recommended_next": "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_REVIEW_BASIS_V0",
    }

    if failures:
        result = {
            "schema_version": "typed_value_source_metadata_source_packet_review_result_v0",
            "review_status": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_REVIEW_SOURCE_BASIS_FAIL",
            "provided_packet_path": packet_path.as_posix() if packet_path else None,
            "packet_present": False,
            "packet_valid": False,
            "field_review_count": 0,
            "field_review_pass_count": 0,
            "field_review_fail_count": 0,
            "review_failures": failures,
            "metadata_source_packet_provided": False,
            "metadata_source_packet_valid": False,
            "metadata_populated": False,
            "ready_discriminator_count": 0,
            "recommended_next": "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_REVIEW_BASIS_V0",
        }
        field_review = {
            "schema_version": "typed_value_source_metadata_source_packet_field_review_v0",
            "field_review_status": "SOURCE_BASIS_FAIL",
            "field_reviews": [],
        }
        status = "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_REVIEW_SOURCE_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_REVIEW_BASIS_V0"
    else:
        result, field_review, status, reason_codes, next_edge = review_packet(packet_path)

    classif = classification_obj(status, reason_codes, next_edge, result)
    boundary = authority_boundary_obj(status)
    roll = rollup_obj(status, result, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, result, next_edge)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    write_json(SOURCE_PACKET_CONTRACT_PATH, contract)
    write_json(SOURCE_PACKET_REVIEW_REQUEST_PATH, review_request)
    write_json(SOURCE_PACKET_REVIEW_RESULT_PATH, result)
    write_json(SOURCE_PACKET_MISSING_VALUES_TEMPLATE_PATH, missing_template)
    write_json(SOURCE_PACKET_FIELD_REVIEW_PATH, field_review)
    write_json(CLASSIFICATION_PATH, classif)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, roll)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(TRANSITION_TRACE_PATH, trace)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        roll["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, roll)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "SOURCE_PACKET_REVIEW_0_BRIDGE_RECEIPT_CONSUMED": SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_PATH.exists(),
        "SOURCE_PACKET_REVIEW_1_SOURCE_PACKET_TEMPLATE_CONSUMED": SOURCE_METADATA_SOURCE_PACKET_TEMPLATE_PATH.exists(),
        "SOURCE_PACKET_REVIEW_2_CONTRACT_EMITTED": SOURCE_PACKET_CONTRACT_PATH.exists(),
        "SOURCE_PACKET_REVIEW_3_REVIEW_REQUEST_EMITTED": SOURCE_PACKET_REVIEW_REQUEST_PATH.exists(),
        "SOURCE_PACKET_REVIEW_4_REVIEW_RESULT_EMITTED": SOURCE_PACKET_REVIEW_RESULT_PATH.exists(),
        "SOURCE_PACKET_REVIEW_5_MISSING_VALUES_TEMPLATE_EMITTED": SOURCE_PACKET_MISSING_VALUES_TEMPLATE_PATH.exists(),
        "SOURCE_PACKET_REVIEW_6_FIELD_REVIEW_EMITTED": SOURCE_PACKET_FIELD_REVIEW_PATH.exists(),
        "SOURCE_PACKET_REVIEW_7_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "SOURCE_PACKET_REVIEW_8_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "SOURCE_PACKET_REVIEW_9_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "SOURCE_PACKET_REVIEW_10_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "SOURCE_PACKET_REVIEW_11_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "SOURCE_PACKET_REVIEW_12_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classif["target_candidate_declared_for_review"] is False,
        "SOURCE_PACKET_REVIEW_13_NO_TARGET_SELECTED_FOR_BUILD": classif["target_selected_for_build"] is False,
        "SOURCE_PACKET_REVIEW_14_NO_ACCEPTED_FOR_BUILD": classif["accepted_for_build"] is False,
        "SOURCE_PACKET_REVIEW_15_NO_RUNTIME_PATCH": classif["runtime_patch_authorized"] is False,
        "SOURCE_PACKET_REVIEW_16_NO_TARGET_FILE_MODIFICATION": classif["target_file_modification_authorized"] is False,
        "SOURCE_PACKET_REVIEW_17_NO_C5_OPENED": classif["c5_authorized"] is False,
        "SOURCE_PACKET_REVIEW_18_NO_GENERAL_CELL1_AUTHORITY": classif["general_cell1_authority_granted"] is False,
        "SOURCE_PACKET_REVIEW_19_NO_LATEST_FILE_GUESSING": classif["latest_file_guessing"] is False,
        "SOURCE_PACKET_REVIEW_20_NO_MTIME_SELECTION": classif["mtime_selection"] is False,
        "SOURCE_PACKET_REVIEW_21_NO_HIDDEN_NEXT_COMMAND": classif["next_command_goal"] is None,
        "SOURCE_PACKET_REVIEW_22_ACCEPTANCE_BOUNDARY_RETAINED": classif["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "SOURCE_PACKET_REVIEW_23_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "packet_path": packet_path.as_posix() if packet_path else None,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_value_source_metadata_source_packet_review_receipt_v0",
        "receipt_type": "TYPED_VALUE_SOURCE_METADATA_SOURCE_PACKET_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_metadata_source_bridge_receipt_id": SOURCE_METADATA_SOURCE_BRIDGE_RECEIPT_ID,
        "typed_metadata_source_packet_review_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "provided_packet_path": packet_path.as_posix() if packet_path else None,
            "packet_present": result.get("packet_present"),
            "packet_valid": result.get("packet_valid"),
            "field_review_count": result.get("field_review_count"),
            "field_review_pass_count": result.get("field_review_pass_count"),
            "field_review_fail_count": result.get("field_review_fail_count"),
            "metadata_source_packet_provided": result.get("metadata_source_packet_provided"),
            "metadata_source_packet_valid": result.get("metadata_source_packet_valid"),
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
            "source_packet_contract": rel(SOURCE_PACKET_CONTRACT_PATH),
            "source_packet_review_request": rel(SOURCE_PACKET_REVIEW_REQUEST_PATH),
            "source_packet_review_result": rel(SOURCE_PACKET_REVIEW_RESULT_PATH),
            "source_packet_missing_values_template": rel(SOURCE_PACKET_MISSING_VALUES_TEMPLATE_PATH),
            "source_packet_field_review": rel(SOURCE_PACKET_FIELD_REVIEW_PATH),
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
    print(f"metadata_source_packet_review_receipt_id={receipt_id}")
    print(f"metadata_source_packet_review_receipt_path={rel(receipt_path)}")
    print(f"metadata_source_packet_contract_path={rel(SOURCE_PACKET_CONTRACT_PATH)}")
    print(f"metadata_source_packet_review_request_path={rel(SOURCE_PACKET_REVIEW_REQUEST_PATH)}")
    print(f"metadata_source_packet_review_result_path={rel(SOURCE_PACKET_REVIEW_RESULT_PATH)}")
    print(f"metadata_source_packet_missing_values_template_path={rel(SOURCE_PACKET_MISSING_VALUES_TEMPLATE_PATH)}")
    print(f"metadata_source_packet_field_review_path={rel(SOURCE_PACKET_FIELD_REVIEW_PATH)}")
    print(f"metadata_source_packet_review_classification_path={rel(CLASSIFICATION_PATH)}")
    print(f"metadata_source_packet_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"metadata_source_packet_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
