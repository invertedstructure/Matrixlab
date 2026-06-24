#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RUN_CELL1_HANDOFF_RETURN_LOOP_TEST_FROM_DESIGN_V0"
TARGET_UNIT_ID = "cell1.handoff_return_loop_test.run_from_design.v0"
LAYER = "CELL_1 / HANDOFF_RETURN_LOOP_TEST"
MODE = "RUN / RETURN_PACKET / CLASSIFICATION_REQUEST"
BUILD_MODE = "BOUNDED_HANDOFF_RETURN_LOOP_TEST_ONLY"

SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID = "26a8e1a4"
SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_design_v0_receipts" / "26a8e1a4.json"
SOURCE_HANDOFF_RETURN_DESIGN_RECORD_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_design_v0" / "handoff_return_loop_design_record_v0.json"
SOURCE_HANDOFF_RETURN_CONTRACT_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_design_v0" / "handoff_return_contract_schema_v0.json"
SOURCE_HANDOFF_RETURN_TEST_PLAN_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_design_v0" / "handoff_return_loop_test_plan_v0.json"
SOURCE_HANDOFF_RETURN_AUTHORITY_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_design_v0" / "handoff_return_loop_authority_boundary_v0.json"
SOURCE_HANDOFF_RETURN_ROLLUP_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_design_v0" / "handoff_return_loop_design_rollup_v0.json"
SOURCE_HANDOFF_RETURN_PROFILE_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_design_v0" / "handoff_return_loop_design_profile_v0.json"

SOURCE_NEXT_OBJECTIVE_RECEIPT_ID = "c34d737d"
SOURCE_NEXT_OBJECTIVE_RECEIPT_PATH = ROOT / "data" / "cell1_next_bounded_objective_decision_v0_receipts" / "c34d737d.json"
SOURCE_NEXT_OBJECTIVE_DECISION_PATH = ROOT / "data" / "cell1_next_bounded_objective_decision_v0" / "objective_decision_record_v0.json"

SOURCE_CELL1_REFERENCE_PACKET_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_frozen_reference_packet_v0.json"
SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID = "e6b0fd97"
SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0_receipts" / "e6b0fd97.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_PATH,
    SOURCE_HANDOFF_RETURN_DESIGN_RECORD_PATH,
    SOURCE_HANDOFF_RETURN_CONTRACT_PATH,
    SOURCE_HANDOFF_RETURN_TEST_PLAN_PATH,
    SOURCE_HANDOFF_RETURN_AUTHORITY_PATH,
    SOURCE_HANDOFF_RETURN_ROLLUP_PATH,
    SOURCE_HANDOFF_RETURN_PROFILE_PATH,
    SOURCE_NEXT_OBJECTIVE_RECEIPT_PATH,
    SOURCE_NEXT_OBJECTIVE_DECISION_PATH,
    SOURCE_CELL1_REFERENCE_PACKET_PATH,
    SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0"
RECEIPT_DIR = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "source_surface_v0.json"
DESIGN_READOUT_PATH = OUT_DIR / "design_readout_v0.json"
RETURN_RESULT_PACKET_PATH = OUT_DIR / "cell1_handoff_return_result_packet_v0.json"
RETURN_PACKET_VALIDATION_PATH = OUT_DIR / "return_packet_validation_record_v0.json"
CLASSIFICATION_REQUEST_PATH = OUT_DIR / "cell0_review_classification_request_v0.json"
RETURN_CLASSIFICATION_PATH = OUT_DIR / "return_packet_classification_record_v0.json"
AUTHORITY_AUDIT_PATH = OUT_DIR / "handoff_return_loop_authority_audit_v0.json"
ROLLUP_PATH = OUT_DIR / "handoff_return_loop_test_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "handoff_return_loop_test_profile_v0.json"
REPORT_PATH = OUT_DIR / "handoff_return_loop_test_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "handoff_return_loop_test_transition_trace.json"

RESULT_KIND = "VERIFICATION_RESULT_RETURNED"
RETURN_CLASSIFICATION = "RETURN_PACKET_ACCEPTED_FOR_REVIEW"
RECOMMENDED_NEXT = "CELL1_HANDOFF_RETURN_LOOP_REVIEW_OR_CLOSE_V0"

ZERO_COUNTER_KEYS = [
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
]

HUMAN_DECISION = {
    "decision": "RUN_CELL1_HANDOFF_RETURN_LOOP_TEST_FROM_DESIGN",
    "scope": "Run one bounded handoff-return loop test from the accepted design. Construct one Cell1 return result packet from the frozen schema-consumption reference, validate the return contract, emit a Cell0/review classification request surface, classify the returned packet for review, emit rollup/profile/report/receipt, and stop. Do not apply runtime patches, modify targets, open C5, grant general Cell1 authority, mutate taxonomy, promote proposal status, fabricate an accepted proposal, or emit hidden next command.",
    "authorized": [
        "consume handoff-return loop design receipt",
        "consume return contract schema",
        "construct one bounded Cell1 return result packet",
        "validate return packet fields and lane typing",
        "emit Cell0/review classification request surface",
        "emit return-packet classification record",
        "emit receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "apply runtime patch",
        "modify target files",
        "open C5",
        "grant general Cell1 authority",
        "mutate taxonomy registry",
        "promote proposal status",
        "fabricate accepted proposal",
        "inspect unbounded payload",
        "emit hidden next command",
    ],
}

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
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    design_receipt = read_json(SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_PATH)
    design = read_json(SOURCE_HANDOFF_RETURN_DESIGN_RECORD_PATH)
    contract = read_json(SOURCE_HANDOFF_RETURN_CONTRACT_PATH)
    plan = read_json(SOURCE_HANDOFF_RETURN_TEST_PLAN_PATH)
    authority = read_json(SOURCE_HANDOFF_RETURN_AUTHORITY_PATH)
    design_rollup = read_json(SOURCE_HANDOFF_RETURN_ROLLUP_PATH)
    design_profile = read_json(SOURCE_HANDOFF_RETURN_PROFILE_PATH)
    next_receipt = read_json(SOURCE_NEXT_OBJECTIVE_RECEIPT_PATH)
    next_decision = read_json(SOURCE_NEXT_OBJECTIVE_DECISION_PATH)
    reference = read_json(SOURCE_CELL1_REFERENCE_PACKET_PATH)
    schema_receipt = read_json(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if design_receipt.get("receipt_id") != SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("handoff_return_design_receipt_not_pass")
    if design_receipt.get("terminal", {}).get("stop_code") != "STOP_CELL1_HANDOFF_RETURN_LOOP_TEST_DESIGNED":
        failures.append("handoff_return_design_wrong_terminal")
    if design.get("future_test_unit") != UNIT_ID:
        failures.append("design_future_test_unit_wrong")
    if contract.get("return_object_type") != "CELL1_HANDOFF_RETURN_RESULT_PACKET":
        failures.append("contract_return_type_wrong")
    if contract.get("authority_boundary", {}).get("may_open_c5") is not False:
        failures.append("contract_allows_c5")
    if contract.get("authority_boundary", {}).get("may_execute_runtime_patch") is not False:
        failures.append("contract_allows_runtime_patch")
    if contract.get("authority_boundary", {}).get("may_modify_target_files") is not False:
        failures.append("contract_allows_target_file_modification")
    if plan.get("future_test_unit") != UNIT_ID:
        failures.append("plan_future_test_unit_wrong")
    if plan.get("test_mode") != "BOUNDED_RETURN_LOOP_TEST_ONLY":
        failures.append("plan_test_mode_wrong")
    if plan.get("next_command_goal") is not None:
        failures.append("plan_has_hidden_next_command")
    if authority.get("may_execute_test_now") is not False:
        failures.append("design_authority_claims_execution")
    if authority.get("may_run_cell1") is not False:
        failures.append("design_authority_claims_cell1_run")
    if authority.get("may_run_cell0") is not False:
        failures.append("design_authority_claims_cell0_run")
    if design_rollup.get("test_executed_count") != 0:
        failures.append("design_rollup_already_executed")
    if design_profile.get("status") != "CELL1_HANDOFF_RETURN_LOOP_TEST_DESIGNED":
        failures.append("design_profile_not_designed")
    if next_receipt.get("receipt_id") != SOURCE_NEXT_OBJECTIVE_RECEIPT_ID or next_receipt.get("gate") != "PASS":
        failures.append("next_objective_receipt_not_pass")
    if next_decision.get("selected_decision_class") != "CELL1_OBJECTIVE_HANDOFF_RETURN_LOOP_TEST":
        failures.append("next_decision_not_handoff_return_loop")
    if reference.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("cell1_reference_not_frozen")
    if schema_receipt.get("receipt_id") != SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID or schema_receipt.get("gate") != "PASS":
        failures.append("schema_test_receipt_not_pass")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_basis_not_pass")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_test_source_surface_v0",
        "source_design_receipt_id": SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID,
        "source_design_receipt_ref": rel(SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_PATH),
        "source_contract_ref": rel(SOURCE_HANDOFF_RETURN_CONTRACT_PATH),
        "source_test_plan_ref": rel(SOURCE_HANDOFF_RETURN_TEST_PLAN_PATH),
        "source_cell1_reference_packet_ref": rel(SOURCE_CELL1_REFERENCE_PACKET_PATH),
        "source_c2_lane_registry_ref": rel(SOURCE_C2_LANE_REGISTRY_PATH),
        "surface_status": "EXPLICIT_HANDOFF_RETURN_LOOP_RUN_SURFACE",
    }

def design_readout() -> Dict[str, Any]:
    design = read_json(SOURCE_HANDOFF_RETURN_DESIGN_RECORD_PATH)
    plan = read_json(SOURCE_HANDOFF_RETURN_TEST_PLAN_PATH)
    contract = read_json(SOURCE_HANDOFF_RETURN_CONTRACT_PATH)
    return {
        "schema_version": "cell1_handoff_return_loop_test_design_readout_v0",
        "design_id": design.get("design_id"),
        "contract_id": contract.get("contract_id"),
        "future_test_unit": plan.get("future_test_unit"),
        "return_object_type": contract.get("return_object_type"),
        "test_mode": plan.get("test_mode"),
        "test_edges": design.get("test_edges", []),
        "failure_classes_to_detect": design.get("failure_classes_to_detect", []),
    }

def build_return_packet() -> Dict[str, Any]:
    contract = read_json(SOURCE_HANDOFF_RETURN_CONTRACT_PATH)
    reference = read_json(SOURCE_CELL1_REFERENCE_PACKET_PATH)
    lanes = read_json(SOURCE_C2_LANE_REGISTRY_PATH)
    packet_seed = {
        "source_design_receipt_id": SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID,
        "source_cell1_reference_id": reference.get("reference_id"),
        "result_kind": RESULT_KIND,
    }
    return {
        "schema_version": "cell1_handoff_return_result_packet_v0",
        "source_design_receipt_id": SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID,
        "source_cell1_reference_id": reference.get("reference_id"),
        "result_packet_id": "cell1_return_" + sha8(packet_seed),
        "origin_cell": "CELL_1",
        "destination_surface": contract.get("destination_surface"),
        "result_kind": RESULT_KIND,
        "bounded_test_scope": "HANDOFF_RETURN_LOOP_TEST_ONLY",
        "claim_lanes": {
            "workflow_position": "RETURNED_FOR_REVIEW",
            "pressure_class": "RETURN_LOOP_EVIDENCE",
            "evidence_status": "REFERENCE_BACKED",
            "object_identity": "CELL1_HANDOFF_RETURN_RESULT_PACKET",
            "authority_status": "BOUNDED_RETURN_ONLY",
            "next_required_move": "CLASSIFY_RETURN_PACKET",
        },
        "lane_registry_ref": rel(SOURCE_C2_LANE_REGISTRY_PATH),
        "lane_registry_receipt_id": SOURCE_C2_RECEIPT_ID,
        "lane_registry_schema_version": lanes.get("schema_version"),
        "evidence_refs": [
            rel(SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_PATH),
            rel(SOURCE_CELL1_REFERENCE_PACKET_PATH),
            rel(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH),
        ],
        "authority_boundary": {
            "may_return_result_packet": True,
            "may_request_review_classification": True,
            "may_execute_runtime_patch": False,
            "may_modify_target_files": False,
            "may_open_c5": False,
            "may_grant_general_cell1_authority": False,
            "may_mutate_taxonomy": False,
            "may_emit_hidden_next_command": False,
        },
        "negative_boundary_counters": {
            "runtime_patch_applied_count": 0,
            "target_file_modified_count": 0,
            "c5_opened_count": 0,
            "general_cell1_authority_granted_count": 0,
            "taxonomy_registry_mutation_count": 0,
            "hidden_next_command_count": 0,
        },
        "classification_request": {
            "requested_surface": "CELL0_OR_REVIEW_CLASSIFICATION_SURFACE",
            "requested_classification": "RETURN_PACKET_CLASSIFICATION",
            "allowed_classifications": [
                "RETURN_PACKET_ACCEPTED_FOR_REVIEW",
                "RETURN_PACKET_REPAIR_REQUIRED",
                "RETURN_PACKET_BLOCKED",
            ],
        },
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CELL1_RETURN_PACKET_EMITTED_FOR_REVIEW",
            "next_command_goal": None,
        },
    }

def validate_return_packet(packet: Dict[str, Any]) -> Dict[str, Any]:
    contract = read_json(SOURCE_HANDOFF_RETURN_CONTRACT_PATH)
    failures: List[str] = []
    for field in contract.get("required_fields", []):
        if field not in packet:
            failures.append(f"missing_required_field:{field}")
    if packet.get("return_object_type") is not None:
        failures.append("unexpected_return_object_type_field")
    if packet.get("result_kind") not in contract.get("allowed_result_kinds", []):
        failures.append("result_kind_not_allowed")
    lanes = packet.get("claim_lanes", {})
    required_lanes = ["workflow_position", "pressure_class", "evidence_status", "object_identity", "authority_status", "next_required_move"]
    for lane in required_lanes:
        if lane not in lanes:
            failures.append(f"missing_claim_lane:{lane}")
    boundary = packet.get("authority_boundary", {})
    if boundary.get("may_execute_runtime_patch") is not False:
        failures.append("return_packet_claims_runtime_patch")
    if boundary.get("may_modify_target_files") is not False:
        failures.append("return_packet_claims_target_modification")
    if boundary.get("may_open_c5") is not False:
        failures.append("return_packet_claims_c5")
    if boundary.get("may_grant_general_cell1_authority") is not False:
        failures.append("return_packet_claims_general_cell1")
    if boundary.get("may_emit_hidden_next_command") is not False:
        failures.append("return_packet_hidden_next_command")
    if packet.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("return_packet_terminal_hidden_next_command")
    return {
        "schema_version": "cell1_handoff_return_packet_validation_record_v0",
        "validation_id": "return_validation_" + sha8({"packet": packet.get("result_packet_id"), "failures": failures}),
        "result_packet_id": packet.get("result_packet_id"),
        "validation_status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "required_fields_checked": contract.get("required_fields", []),
        "lane_typing_checked": True,
        "authority_boundary_checked": True,
    }

def classification_request(packet: Dict[str, Any], validation: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell0_review_classification_request_v0",
        "request_id": "return_classification_request_" + sha8({"packet": packet["result_packet_id"]}),
        "source_return_packet_id": packet["result_packet_id"],
        "source_return_packet_ref": rel(RETURN_RESULT_PACKET_PATH),
        "source_validation_ref": rel(RETURN_PACKET_VALIDATION_PATH),
        "destination_surface": "CELL0_OR_REVIEW_CLASSIFICATION_SURFACE",
        "requested_classification": "RETURN_PACKET_CLASSIFICATION",
        "allowed_classifications": [
            "RETURN_PACKET_ACCEPTED_FOR_REVIEW",
            "RETURN_PACKET_REPAIR_REQUIRED",
            "RETURN_PACKET_BLOCKED",
        ],
        "classification_inputs": {
            "validation_status": validation["validation_status"],
            "result_kind": packet["result_kind"],
            "object_identity_lane": packet["claim_lanes"]["object_identity"],
            "authority_status_lane": packet["claim_lanes"]["authority_status"],
            "next_required_move_lane": packet["claim_lanes"]["next_required_move"],
        },
        "authority_boundary": {
            "may_classify_return_packet": True,
            "may_accept_as_build": False,
            "may_execute_cell0_repair": False,
            "may_execute_cell1": False,
            "may_open_c5": False,
        },
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_RETURN_PACKET_CLASSIFICATION_REQUEST_EMITTED",
            "next_command_goal": None,
        },
    }

def classify_return_packet(packet: Dict[str, Any], validation: Dict[str, Any], request: Dict[str, Any]) -> Dict[str, Any]:
    failures: List[str] = []
    if validation["validation_status"] != "PASS":
        failures.append("return_packet_validation_not_pass")
    if request["authority_boundary"]["may_open_c5"] is not False:
        failures.append("classification_request_allows_c5")
    if request["authority_boundary"]["may_execute_cell1"] is not False:
        failures.append("classification_request_allows_cell1_execution")
    classification = RETURN_CLASSIFICATION if not failures else "RETURN_PACKET_REPAIR_REQUIRED"
    return {
        "schema_version": "cell1_handoff_return_packet_classification_record_v0",
        "classification_id": "return_classification_" + sha8({"packet": packet["result_packet_id"], "classification": classification}),
        "source_return_packet_id": packet["result_packet_id"],
        "source_classification_request_ref": rel(CLASSIFICATION_REQUEST_PATH),
        "classification": classification,
        "classification_status": "PASS" if not failures else "FAIL",
        "failures": failures,
        "meaning": "Cell1 return packet is classifiable by review/Cell0 surface without authority leakage." if not failures else "Returned packet requires repair before review acceptance.",
        "accepted_for_review": not failures,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_RETURN_PACKET_CLASSIFIED_FOR_REVIEW",
            "next_command_goal": None,
        },
    }

def authority_audit(packet: Dict[str, Any], request: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
    counters = {
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "hidden_next_command_count": 0,
        "unbounded_payload_inspection_count": 0,
    }
    return {
        "schema_version": "cell1_handoff_return_loop_authority_audit_v0",
        "audit_id": "return_loop_audit_" + sha8({"packet": packet["result_packet_id"], "classification": classification["classification"]}),
        "source_return_packet_id": packet["result_packet_id"],
        "return_packet_boundary": packet["authority_boundary"],
        "classification_request_boundary": request["authority_boundary"],
        "classification_boundary": {
            "accepted_for_build": classification["accepted_for_build"],
            "runtime_patch_authorized": classification["runtime_patch_authorized"],
            "c5_authorized": classification["c5_authorized"],
            "general_cell1_authority_granted": classification["general_cell1_authority_granted"],
        },
        "negative_boundary_counters": counters,
        "audit_status": "PASS" if all(v == 0 for v in counters.values()) else "FAIL",
    }

def rollup(packet: Dict[str, Any], validation: Dict[str, Any], request: Dict[str, Any], classification: Dict[str, Any], audit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_test_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_design_receipt_id": SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID,
        "source_next_objective_receipt_id": SOURCE_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "result_packet_id": packet["result_packet_id"],
        "result_kind": packet["result_kind"],
        "return_packet_emitted_count": 1,
        "return_packet_validation_pass_count": 1 if validation["validation_status"] == "PASS" else 0,
        "classification_request_emitted_count": 1,
        "return_packet_classification_pass_count": 1 if classification["classification_status"] == "PASS" else 0,
        "accepted_for_review_count": 1 if classification["accepted_for_review"] else 0,
        "accepted_for_build_count": 0,
        "authority_audit_pass_count": 1 if audit["audit_status"] == "PASS" else 0,
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
        "recommended_next": RECOMMENDED_NEXT,
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_test_profile_v0",
        "profile_id": "cell1_return_loop_run_" + sha8({"source": SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID}),
        "status": "CELL1_HANDOFF_RETURN_LOOP_TEST_COMPLETE",
        "result_packet_id": rollup_obj["result_packet_id"],
        "result_kind": rollup_obj["result_kind"],
        "return_packet_emitted": True,
        "return_packet_validated": rollup_obj["return_packet_validation_pass_count"] == 1,
        "classification_request_emitted": True,
        "return_packet_classified": rollup_obj["return_packet_classification_pass_count"] == 1,
        "accepted_for_review": rollup_obj["accepted_for_review_count"] == 1,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_test_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_design_receipt_consumed_count": 1,
        "return_packet_emitted_count": rollup_obj["return_packet_emitted_count"],
        "return_packet_validation_pass_count": rollup_obj["return_packet_validation_pass_count"],
        "classification_request_emitted_count": rollup_obj["classification_request_emitted_count"],
        "return_packet_classification_pass_count": rollup_obj["return_packet_classification_pass_count"],
        "accepted_for_review_count": rollup_obj["accepted_for_review_count"],
        "accepted_for_build_count": 0,
        "authority_audit_pass_count": rollup_obj["authority_audit_pass_count"],
        "profile_status": profile_obj["status"],
        "recommended_next_handling": rollup_obj["recommended_next"],
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
    }

def transition_trace(packet: Dict[str, Any], validation: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_test_transition_trace_v0",
        "trace": [
            {
                "step": "load_design",
                "question": "is a valid return-loop design available",
                "answer": SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID,
                "taken": "construct_return_packet",
            },
            {
                "step": "construct_return_packet",
                "question": "can Cell1 emit a bounded typed return result packet",
                "answer": packet["result_packet_id"],
                "taken": "validate_contract",
            },
            {
                "step": "validate_contract",
                "question": "does the return packet satisfy the contract and lane typing",
                "answer": validation["validation_status"],
                "taken": "emit_classification_request",
            },
            {
                "step": "emit_classification_request",
                "question": "can review/Cell0 classify the returned packet without authority leakage",
                "answer": classification["classification"],
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CELL1_HANDOFF_RETURN_LOOP_TEST_COMPLETE",
            "next_command_goal": None,
        },
    }

def validate_outputs(packet: Dict[str, Any], validation: Dict[str, Any], request: Dict[str, Any], classification: Dict[str, Any], audit: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if packet.get("origin_cell") != "CELL_1":
        failures.append("return_packet_origin_not_cell1")
    if packet.get("destination_surface") != "CELL0_OR_REVIEW_CLASSIFICATION_SURFACE":
        failures.append("return_packet_wrong_destination")
    if packet.get("result_kind") != RESULT_KIND:
        failures.append("return_packet_wrong_result_kind")
    if packet.get("authority_boundary", {}).get("may_execute_runtime_patch") is not False:
        failures.append("return_packet_allows_runtime_patch")
    if packet.get("authority_boundary", {}).get("may_modify_target_files") is not False:
        failures.append("return_packet_allows_target_file_modification")
    if packet.get("authority_boundary", {}).get("may_open_c5") is not False:
        failures.append("return_packet_allows_c5")
    if packet.get("authority_boundary", {}).get("may_grant_general_cell1_authority") is not False:
        failures.append("return_packet_allows_general_cell1")
    if packet.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("return_packet_hidden_next_command")
    if validation.get("validation_status") != "PASS":
        failures.append("validation_not_pass")
    if request.get("authority_boundary", {}).get("may_open_c5") is not False:
        failures.append("classification_request_allows_c5")
    if request.get("authority_boundary", {}).get("may_execute_cell1") is not False:
        failures.append("classification_request_allows_cell1")
    if request.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("classification_request_hidden_next_command")
    if classification.get("classification") != RETURN_CLASSIFICATION:
        failures.append("classification_wrong")
    if classification.get("accepted_for_build") is not False:
        failures.append("classification_accepts_for_build")
    if classification.get("runtime_patch_authorized") is not False:
        failures.append("classification_authorizes_runtime_patch")
    if classification.get("c5_authorized") is not False:
        failures.append("classification_authorizes_c5")
    if classification.get("general_cell1_authority_granted") is not False:
        failures.append("classification_grants_general_cell1")
    if classification.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("classification_hidden_next_command")
    if audit.get("audit_status") != "PASS":
        failures.append("authority_audit_not_pass")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if rollup_obj.get("return_packet_emitted_count") != 1:
        failures.append("return_packet_emitted_count_not_one")
    if rollup_obj.get("return_packet_validation_pass_count") != 1:
        failures.append("return_packet_validation_pass_count_not_one")
    if rollup_obj.get("classification_request_emitted_count") != 1:
        failures.append("classification_request_emitted_count_not_one")
    if rollup_obj.get("return_packet_classification_pass_count") != 1:
        failures.append("return_packet_classification_pass_count_not_one")
    if rollup_obj.get("accepted_for_review_count") != 1:
        failures.append("accepted_for_review_count_not_one")
    if rollup_obj.get("accepted_for_build_count") != 0:
        failures.append("accepted_for_build_count_nonzero")
    if profile_obj.get("accepted_for_build") is not False:
        failures.append("profile_accepts_for_build")
    if profile_obj.get("runtime_patch_applied") is not False:
        failures.append("profile_claims_runtime_patch")
    if profile_obj.get("target_file_modified") is not False:
        failures.append("profile_claims_target_file_modified")
    if profile_obj.get("c5_opened") is not False:
        failures.append("profile_claims_c5")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "c5_opened_count",
        "general_cell1_authority_granted_count",
        "taxonomy_registry_mutation_count",
        "hidden_next_command_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
    ]:
        if report_obj.get(key) != 0:
            failures.append(f"report_counter_nonzero:{key}:{report_obj.get(key)}")
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    for gate, ok in receipt.get("acceptance_gate_results", {}).items():
        if ok is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{ok}")
    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_CELL1_HANDOFF_RETURN_LOOP_TEST_COMPLETE":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    packet = read_json(RETURN_RESULT_PACKET_PATH)
    validation = read_json(RETURN_PACKET_VALIDATION_PATH)
    request = read_json(CLASSIFICATION_REQUEST_PATH)
    classification = read_json(RETURN_CLASSIFICATION_PATH)
    audit = read_json(AUTHORITY_AUDIT_PATH)
    rollup_obj = read_json(ROLLUP_PATH)
    profile_obj = read_json(PROFILE_PATH)
    report_obj = read_json(REPORT_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    bad_packet = copy.deepcopy(packet)
    bad_packet["authority_boundary"]["may_open_c5"] = True
    add("return_packet_allows_c5_fail", validate_outputs(bad_packet, validation, request, classification, audit, rollup_obj, profile_obj, report_obj), "return_packet_allows_c5")

    bad_packet = copy.deepcopy(packet)
    bad_packet["authority_boundary"]["may_execute_runtime_patch"] = True
    add("return_packet_allows_runtime_patch_fail", validate_outputs(bad_packet, validation, request, classification, audit, rollup_obj, profile_obj, report_obj), "return_packet_allows_runtime_patch")

    bad_packet = copy.deepcopy(packet)
    bad_packet["authority_boundary"]["may_modify_target_files"] = True
    add("return_packet_allows_target_file_modification_fail", validate_outputs(bad_packet, validation, request, classification, audit, rollup_obj, profile_obj, report_obj), "return_packet_allows_target_file_modification")

    bad_packet = copy.deepcopy(packet)
    bad_packet["terminal"]["next_command_goal"] = "RUN_C5"
    add("return_packet_hidden_next_command_fail", validate_outputs(bad_packet, validation, request, classification, audit, rollup_obj, profile_obj, report_obj), "return_packet_hidden_next_command")

    bad_validation = copy.deepcopy(validation)
    bad_validation["validation_status"] = "FAIL"
    add("validation_not_pass_fail", validate_outputs(packet, bad_validation, request, classification, audit, rollup_obj, profile_obj, report_obj), "validation_not_pass")

    bad_request = copy.deepcopy(request)
    bad_request["authority_boundary"]["may_open_c5"] = True
    add("classification_request_allows_c5_fail", validate_outputs(packet, validation, bad_request, classification, audit, rollup_obj, profile_obj, report_obj), "classification_request_allows_c5")

    bad_request = copy.deepcopy(request)
    bad_request["authority_boundary"]["may_execute_cell1"] = True
    add("classification_request_allows_cell1_fail", validate_outputs(packet, validation, bad_request, classification, audit, rollup_obj, profile_obj, report_obj), "classification_request_allows_cell1")

    bad_classification = copy.deepcopy(classification)
    bad_classification["accepted_for_build"] = True
    add("classification_accepts_for_build_fail", validate_outputs(packet, validation, request, bad_classification, audit, rollup_obj, profile_obj, report_obj), "classification_accepts_for_build")

    bad_classification = copy.deepcopy(classification)
    bad_classification["runtime_patch_authorized"] = True
    add("classification_authorizes_runtime_patch_fail", validate_outputs(packet, validation, request, bad_classification, audit, rollup_obj, profile_obj, report_obj), "classification_authorizes_runtime_patch")

    bad_classification = copy.deepcopy(classification)
    bad_classification["c5_authorized"] = True
    add("classification_authorizes_c5_fail", validate_outputs(packet, validation, request, bad_classification, audit, rollup_obj, profile_obj, report_obj), "classification_authorizes_c5")

    bad_classification = copy.deepcopy(classification)
    bad_classification["terminal"]["next_command_goal"] = "RUN_NEXT"
    add("classification_hidden_next_command_fail", validate_outputs(packet, validation, request, bad_classification, audit, rollup_obj, profile_obj, report_obj), "classification_hidden_next_command")

    for case, counter in [
        ("runtime_patch_applied_fail", "runtime_patch_applied_count"),
        ("target_file_modified_fail", "target_file_modified_count"),
        ("c5_opened_fail", "c5_opened_count"),
        ("general_cell1_authority_granted_fail", "general_cell1_authority_granted_count"),
        ("taxonomy_registry_mutated_fail", "taxonomy_registry_mutation_count"),
        ("proposal_status_promoted_fail", "proposal_status_promoted_count"),
        ("accepted_proposal_fabricated_fail", "accepted_proposal_fabricated_count"),
        ("source_mutation_fail", "source_mutation_count"),
        ("prior_receipt_mutation_fail", "prior_receipt_mutation_count"),
        ("hidden_next_command_fail", "hidden_next_command_count"),
        ("unbounded_payload_inspection_fail", "unbounded_payload_inspection_count"),
    ]:
        bad_rollup = copy.deepcopy(rollup_obj)
        bad_report = copy.deepcopy(report_obj)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(packet, validation, request, classification, audit, bad_rollup, profile_obj, bad_report), counter)

    bad_rollup = copy.deepcopy(rollup_obj)
    bad_rollup["accepted_for_build_count"] = 1
    add("accepted_for_build_count_nonzero_fail", validate_outputs(packet, validation, request, classification, audit, bad_rollup, profile_obj, report_obj), "accepted_for_build_count_nonzero")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_CELL1_HANDOFF_RETURN_RUN_EVIDENCE_REQUEST_REQUIRED", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "cell1_handoff_return_loop_test_receipt_v0",
            "receipt_type": "CELL1_HANDOFF_RETURN_LOOP_TEST_RECEIPT",
            "receipt_id": receipt_id,
            "unit_id": UNIT_ID,
            "target_unit_id": TARGET_UNIT_ID,
            "gate": "FAIL",
            "failures": failures,
            "terminal": terminal,
            "created_at": now_iso(),
        }
        write_json(receipt_path, receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        print(f"cell1_handoff_return_test_receipt_id={receipt_id}")
        print(f"cell1_handoff_return_test_receipt_path=data/cell1_handoff_return_loop_test_run_v0_receipts/{receipt_id}.json")
        return 1

    design_readout_obj = design_readout()
    packet = build_return_packet()
    validation = validate_return_packet(packet)
    request = classification_request(packet, validation)
    classification = classify_return_packet(packet, validation, request)
    audit = authority_audit(packet, request, classification)
    rollup_obj = rollup(packet, validation, request, classification, audit)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace(packet, validation, classification)

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(DESIGN_READOUT_PATH, design_readout_obj)
    write_json(RETURN_RESULT_PACKET_PATH, packet)
    write_json(RETURN_PACKET_VALIDATION_PATH, validation)
    write_json(CLASSIFICATION_REQUEST_PATH, request)
    write_json(RETURN_CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_AUDIT_PATH, audit)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(packet, validation, request, classification, audit, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "HANDOFF_RETURN_RUN_0_DESIGN_RECEIPT_CONSUMED": SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_PATH.exists(),
        "HANDOFF_RETURN_RUN_1_CONTRACT_CONSUMED": SOURCE_HANDOFF_RETURN_CONTRACT_PATH.exists(),
        "HANDOFF_RETURN_RUN_2_TEST_PLAN_CONSUMED": SOURCE_HANDOFF_RETURN_TEST_PLAN_PATH.exists(),
        "HANDOFF_RETURN_RUN_3_RETURN_PACKET_EMITTED": RETURN_RESULT_PACKET_PATH.exists() and rollup_obj["return_packet_emitted_count"] == 1,
        "HANDOFF_RETURN_RUN_4_RETURN_PACKET_VALIDATED": validation["validation_status"] == "PASS",
        "HANDOFF_RETURN_RUN_5_CLASSIFICATION_REQUEST_EMITTED": CLASSIFICATION_REQUEST_PATH.exists() and rollup_obj["classification_request_emitted_count"] == 1,
        "HANDOFF_RETURN_RUN_6_RETURN_PACKET_CLASSIFIED": classification["classification_status"] == "PASS",
        "HANDOFF_RETURN_RUN_7_ACCEPTED_FOR_REVIEW_NOT_BUILD": classification["accepted_for_review"] is True and classification["accepted_for_build"] is False,
        "HANDOFF_RETURN_RUN_8_AUTHORITY_AUDIT_PASS": audit["audit_status"] == "PASS",
        "HANDOFF_RETURN_RUN_9_NO_RUNTIME_PATCH": rollup_obj["runtime_patch_applied_count"] == 0,
        "HANDOFF_RETURN_RUN_10_NO_TARGET_FILE_MODIFICATION": rollup_obj["target_file_modified_count"] == 0,
        "HANDOFF_RETURN_RUN_11_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "HANDOFF_RETURN_RUN_12_NO_GENERAL_CELL1_AUTHORITY": rollup_obj["general_cell1_authority_granted_count"] == 0,
        "HANDOFF_RETURN_RUN_13_NO_TAXONOMY_MUTATION": rollup_obj["taxonomy_registry_mutation_count"] == 0,
        "HANDOFF_RETURN_RUN_14_NO_PROPOSAL_PROMOTION": rollup_obj["proposal_status_promoted_count"] == 0,
        "HANDOFF_RETURN_RUN_15_NO_ACCEPTED_PROPOSAL_FABRICATION": rollup_obj["accepted_proposal_fabricated_count"] == 0,
        "HANDOFF_RETURN_RUN_16_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "HANDOFF_RETURN_RUN_17_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_design": SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID,
        "result_packet_id": packet["result_packet_id"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "design_readout": rel(DESIGN_READOUT_PATH),
        "return_result_packet": rel(RETURN_RESULT_PACKET_PATH),
        "return_packet_validation": rel(RETURN_PACKET_VALIDATION_PATH),
        "classification_request": rel(CLASSIFICATION_REQUEST_PATH),
        "return_packet_classification": rel(RETURN_CLASSIFICATION_PATH),
        "authority_audit": rel(AUTHORITY_AUDIT_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_design_receipt": rel(SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_PATH),
        "source_contract": rel(SOURCE_HANDOFF_RETURN_CONTRACT_PATH),
        "source_test_plan": rel(SOURCE_HANDOFF_RETURN_TEST_PLAN_PATH),
        "source_cell1_reference_packet": rel(SOURCE_CELL1_REFERENCE_PACKET_PATH),
        "source_c2_lane_registry": rel(SOURCE_C2_LANE_REGISTRY_PATH),
    }

    guards = {
        "build_mode_bounded_handoff_return_loop_only": BUILD_MODE == "BOUNDED_HANDOFF_RETURN_LOOP_TEST_ONLY",
        "return_packet_emitted": True,
        "return_packet_validated": validation["validation_status"] == "PASS",
        "classification_request_emitted": True,
        "return_packet_classified_for_review": classification["classification"] == RETURN_CLASSIFICATION,
        "accepted_for_review": classification["accepted_for_review"],
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "taxonomy_registry_mutated": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "cell1_handoff_return_loop_test_receipt_v0",
        "receipt_type": "CELL1_HANDOFF_RETURN_LOOP_TEST_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "bounded Cell1 handoff-return result packet and classification request",
        "source_handoff_return_design_receipt_id": SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID,
        "source_next_objective_receipt_id": SOURCE_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "handoff_return_test_summary": {
            "profile_status": profile_obj["status"],
            "result_packet_id": packet["result_packet_id"],
            "result_kind": packet["result_kind"],
            "return_packet_emitted_count": rollup_obj["return_packet_emitted_count"],
            "return_packet_validation_pass_count": rollup_obj["return_packet_validation_pass_count"],
            "classification_request_emitted_count": rollup_obj["classification_request_emitted_count"],
            "return_packet_classification_pass_count": rollup_obj["return_packet_classification_pass_count"],
            "classification": classification["classification"],
            "accepted_for_review": classification["accepted_for_review"],
            "accepted_for_build": classification["accepted_for_build"],
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "recommended_next": rollup_obj["recommended_next"],
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "handoff_return_test_guards": guards,
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_receipt(receipt)
    failures.extend(receipt_failures)
    receipt["failures"] = failures
    receipt["gate"] = "PASS" if not failures else "FAIL"
    if failures:
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}

    write_json(receipt_path, receipt)

    negative_controls = run_negative_controls(receipt_path)
    if len(negative_controls) != 23 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
        receipt = read_json(receipt_path)
        receipt["gate"] = "FAIL"
        receipt["failures"].append("negative_controls_failed")
        receipt["negative_controls"] = negative_controls
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}
        write_json(receipt_path, receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 1

    receipt = read_json(receipt_path)
    receipt["negative_controls"] = negative_controls
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"cell1_handoff_return_test_receipt_id={receipt_id}")
    print(f"cell1_handoff_return_test_receipt_path=data/cell1_handoff_return_loop_test_run_v0_receipts/{receipt_id}.json")
    print(f"cell1_handoff_return_packet_path=data/cell1_handoff_return_loop_test_run_v0/cell1_handoff_return_result_packet_v0.json")
    print(f"cell1_handoff_return_classification_path=data/cell1_handoff_return_loop_test_run_v0/return_packet_classification_record_v0.json")
    print(f"cell1_handoff_return_rollup_path=data/cell1_handoff_return_loop_test_run_v0/handoff_return_loop_test_rollup_v0.json")
    print(f"cell1_handoff_return_profile_path=data/cell1_handoff_return_loop_test_run_v0/handoff_return_loop_test_profile_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
