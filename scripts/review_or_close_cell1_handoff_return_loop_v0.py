#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CELL1_HANDOFF_RETURN_LOOP_REVIEW_OR_CLOSE_V0"
TARGET_UNIT_ID = "cell1.handoff_return_loop.review_or_close.v0"
LAYER = "CELL_1 / HANDOFF_RETURN_LOOP_REVIEW_OR_CLOSE"
MODE = "REVIEW / CLOSE / REFERENCE_FREEZE"
BUILD_MODE = "HANDOFF_RETURN_LOOP_REVIEW_OR_CLOSE_ONLY"

SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID = "35e62eaf"
SOURCE_HANDOFF_RETURN_TEST_RECEIPT_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0_receipts" / "35e62eaf.json"
SOURCE_HANDOFF_RETURN_PACKET_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0" / "cell1_handoff_return_result_packet_v0.json"
SOURCE_HANDOFF_RETURN_VALIDATION_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0" / "return_packet_validation_record_v0.json"
SOURCE_HANDOFF_RETURN_CLASSIFICATION_REQUEST_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0" / "cell0_review_classification_request_v0.json"
SOURCE_HANDOFF_RETURN_CLASSIFICATION_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0" / "return_packet_classification_record_v0.json"
SOURCE_HANDOFF_RETURN_AUTHORITY_AUDIT_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0" / "handoff_return_loop_authority_audit_v0.json"
SOURCE_HANDOFF_RETURN_ROLLUP_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0" / "handoff_return_loop_test_rollup_v0.json"
SOURCE_HANDOFF_RETURN_PROFILE_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0" / "handoff_return_loop_test_profile_v0.json"
SOURCE_HANDOFF_RETURN_REPORT_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_run_v0" / "handoff_return_loop_test_report.json"

SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID = "26a8e1a4"
SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_design_v0_receipts" / "26a8e1a4.json"
SOURCE_HANDOFF_RETURN_DESIGN_RECORD_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_design_v0" / "handoff_return_loop_design_record_v0.json"
SOURCE_HANDOFF_RETURN_CONTRACT_PATH = ROOT / "data" / "cell1_handoff_return_loop_test_design_v0" / "handoff_return_contract_schema_v0.json"

SOURCE_NEXT_OBJECTIVE_RECEIPT_ID = "c34d737d"
SOURCE_NEXT_OBJECTIVE_RECEIPT_PATH = ROOT / "data" / "cell1_next_bounded_objective_decision_v0_receipts" / "c34d737d.json"

SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID = "e6b0fd97"
SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0_receipts" / "e6b0fd97.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_HANDOFF_RETURN_TEST_RECEIPT_PATH,
    SOURCE_HANDOFF_RETURN_PACKET_PATH,
    SOURCE_HANDOFF_RETURN_VALIDATION_PATH,
    SOURCE_HANDOFF_RETURN_CLASSIFICATION_REQUEST_PATH,
    SOURCE_HANDOFF_RETURN_CLASSIFICATION_PATH,
    SOURCE_HANDOFF_RETURN_AUTHORITY_AUDIT_PATH,
    SOURCE_HANDOFF_RETURN_ROLLUP_PATH,
    SOURCE_HANDOFF_RETURN_PROFILE_PATH,
    SOURCE_HANDOFF_RETURN_REPORT_PATH,
    SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_PATH,
    SOURCE_HANDOFF_RETURN_DESIGN_RECORD_PATH,
    SOURCE_HANDOFF_RETURN_CONTRACT_PATH,
    SOURCE_NEXT_OBJECTIVE_RECEIPT_PATH,
    SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0"
RECEIPT_DIR = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "source_surface_v0.json"
RETURN_LOOP_READOUT_PATH = OUT_DIR / "handoff_return_loop_readout_v0.json"
BOUNDARY_AUDIT_PATH = OUT_DIR / "handoff_return_loop_boundary_audit_v0.json"
CLOSURE_DECISION_PATH = OUT_DIR / "handoff_return_loop_closure_decision_v0.json"
FROZEN_REFERENCE_PACKET_PATH = OUT_DIR / "handoff_return_loop_frozen_reference_packet_v0.json"
NEXT_DECISION_SURFACE_PATH = OUT_DIR / "handoff_return_loop_next_decision_surface_v0.json"
ROLLUP_PATH = OUT_DIR / "handoff_return_loop_review_or_close_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "handoff_return_loop_review_or_close_profile_v0.json"
REPORT_PATH = OUT_DIR / "handoff_return_loop_review_or_close_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "handoff_return_loop_review_or_close_transition_trace.json"

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
    "accepted_for_build_count",
]

HUMAN_DECISION = {
    "decision": "CELL1_HANDOFF_RETURN_LOOP_REVIEW_OR_CLOSE",
    "scope": "Review the completed bounded Cell1 handoff-return loop test and close it as a frozen reference object if the return packet was valid, classifiable for review, and boundary-clean. This unit emits readout, boundary audit, closure decision, frozen reference packet, next decision surface, rollup, profile, report, transition trace, and receipt. It does not rerun the test, apply runtime patch, modify targets, open C5, grant general Cell1 authority, promote proposals, fabricate accepted proposals, or emit hidden next command.",
    "authorized": [
        "consume handoff-return loop test receipt",
        "audit return-loop result packet and classification",
        "classify closure status",
        "freeze handoff-return loop as reference if clean",
        "emit next decision surface",
        "emit receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "rerun handoff-return loop test",
        "apply runtime patch",
        "modify target files",
        "open C5",
        "grant general Cell1 authority",
        "mutate taxonomy registry",
        "promote proposal status",
        "fabricate accepted proposal",
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

    receipt = read_json(SOURCE_HANDOFF_RETURN_TEST_RECEIPT_PATH)
    packet = read_json(SOURCE_HANDOFF_RETURN_PACKET_PATH)
    validation = read_json(SOURCE_HANDOFF_RETURN_VALIDATION_PATH)
    request = read_json(SOURCE_HANDOFF_RETURN_CLASSIFICATION_REQUEST_PATH)
    classification = read_json(SOURCE_HANDOFF_RETURN_CLASSIFICATION_PATH)
    audit = read_json(SOURCE_HANDOFF_RETURN_AUTHORITY_AUDIT_PATH)
    rollup = read_json(SOURCE_HANDOFF_RETURN_ROLLUP_PATH)
    profile = read_json(SOURCE_HANDOFF_RETURN_PROFILE_PATH)
    design_receipt = read_json(SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_PATH)
    next_receipt = read_json(SOURCE_NEXT_OBJECTIVE_RECEIPT_PATH)
    schema_receipt = read_json(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if receipt.get("receipt_id") != SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("handoff_return_test_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != "STOP_CELL1_HANDOFF_RETURN_LOOP_TEST_COMPLETE":
        failures.append("handoff_return_test_wrong_terminal")
    if packet.get("result_packet_id") != rollup.get("result_packet_id"):
        failures.append("packet_rollup_result_id_mismatch")
    if packet.get("origin_cell") != "CELL_1":
        failures.append("packet_origin_not_cell1")
    if packet.get("destination_surface") != "CELL0_OR_REVIEW_CLASSIFICATION_SURFACE":
        failures.append("packet_destination_wrong")
    if packet.get("authority_boundary", {}).get("may_open_c5") is not False:
        failures.append("packet_allows_c5")
    if packet.get("authority_boundary", {}).get("may_execute_runtime_patch") is not False:
        failures.append("packet_allows_runtime_patch")
    if packet.get("authority_boundary", {}).get("may_modify_target_files") is not False:
        failures.append("packet_allows_target_file_modification")
    if packet.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("packet_hidden_next_command")
    if validation.get("validation_status") != "PASS":
        failures.append("return_packet_validation_not_pass")
    if request.get("authority_boundary", {}).get("may_open_c5") is not False:
        failures.append("classification_request_allows_c5")
    if request.get("authority_boundary", {}).get("may_execute_cell1") is not False:
        failures.append("classification_request_allows_cell1")
    if request.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("classification_request_hidden_next_command")
    if classification.get("classification") != "RETURN_PACKET_ACCEPTED_FOR_REVIEW":
        failures.append("classification_not_accepted_for_review")
    if classification.get("accepted_for_review") is not True:
        failures.append("classification_not_accepted_for_review_bool")
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
    if profile.get("status") != "CELL1_HANDOFF_RETURN_LOOP_TEST_COMPLETE":
        failures.append("profile_not_complete")
    if rollup.get("return_packet_emitted_count") != 1:
        failures.append("return_packet_not_emitted_once")
    if rollup.get("return_packet_validation_pass_count") != 1:
        failures.append("return_validation_not_pass_once")
    if rollup.get("classification_request_emitted_count") != 1:
        failures.append("classification_request_not_emitted_once")
    if rollup.get("return_packet_classification_pass_count") != 1:
        failures.append("classification_not_pass_once")
    if rollup.get("accepted_for_review_count") != 1:
        failures.append("accepted_for_review_count_not_one")
    for key in ZERO_COUNTER_KEYS:
        if rollup.get(key, 0) != 0:
            failures.append(f"source_rollup_counter_nonzero:{key}:{rollup.get(key)}")
    if design_receipt.get("receipt_id") != SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("design_receipt_not_pass")
    if next_receipt.get("receipt_id") != SOURCE_NEXT_OBJECTIVE_RECEIPT_ID or next_receipt.get("gate") != "PASS":
        failures.append("next_objective_receipt_not_pass")
    if schema_receipt.get("receipt_id") != SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID or schema_receipt.get("gate") != "PASS":
        failures.append("schema_test_receipt_not_pass")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_basis_not_pass")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_review_source_surface_v0",
        "source_handoff_return_test_receipt_id": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID,
        "source_handoff_return_test_receipt_ref": rel(SOURCE_HANDOFF_RETURN_TEST_RECEIPT_PATH),
        "source_return_packet_ref": rel(SOURCE_HANDOFF_RETURN_PACKET_PATH),
        "source_return_classification_ref": rel(SOURCE_HANDOFF_RETURN_CLASSIFICATION_PATH),
        "source_authority_audit_ref": rel(SOURCE_HANDOFF_RETURN_AUTHORITY_AUDIT_PATH),
        "source_design_receipt_id": SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID,
        "source_next_objective_receipt_id": SOURCE_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "surface_status": "EXPLICIT_HANDOFF_RETURN_LOOP_REVIEW_SURFACE",
    }

def return_loop_readout() -> Dict[str, Any]:
    packet = read_json(SOURCE_HANDOFF_RETURN_PACKET_PATH)
    validation = read_json(SOURCE_HANDOFF_RETURN_VALIDATION_PATH)
    classification = read_json(SOURCE_HANDOFF_RETURN_CLASSIFICATION_PATH)
    rollup = read_json(SOURCE_HANDOFF_RETURN_ROLLUP_PATH)
    return {
        "schema_version": "cell1_handoff_return_loop_readout_v0",
        "result_packet_id": packet.get("result_packet_id"),
        "result_kind": packet.get("result_kind"),
        "return_packet_validated": validation.get("validation_status") == "PASS",
        "classification": classification.get("classification"),
        "accepted_for_review": classification.get("accepted_for_review"),
        "accepted_for_build": classification.get("accepted_for_build"),
        "reference_proves": [
            "Cell1 can emit a bounded typed return result packet.",
            "The return packet can reference the frozen schema-consumption evidence.",
            "The return packet can preserve lane-typed authority boundaries.",
            "A Cell0/review classification request can classify the packet for review.",
        ],
        "reference_does_not_prove": [
            "Cell0 has executed a repair or build.",
            "The returned packet is accepted for build.",
            "Runtime patch safety.",
            "C5 authorization.",
            "General Cell1 authority.",
        ],
        "observed_positive_counters": {
            "return_packet_emitted_count": rollup.get("return_packet_emitted_count"),
            "return_packet_validation_pass_count": rollup.get("return_packet_validation_pass_count"),
            "classification_request_emitted_count": rollup.get("classification_request_emitted_count"),
            "return_packet_classification_pass_count": rollup.get("return_packet_classification_pass_count"),
            "accepted_for_review_count": rollup.get("accepted_for_review_count"),
        },
    }

def boundary_audit() -> Dict[str, Any]:
    rollup = read_json(SOURCE_HANDOFF_RETURN_ROLLUP_PATH)
    counters = {key: rollup.get(key, 0) for key in ZERO_COUNTER_KEYS}
    return {
        "schema_version": "cell1_handoff_return_loop_boundary_audit_v0",
        "audit_id": "handoff_return_close_audit_" + sha8({"source": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID, "counters": counters}),
        "source_handoff_return_test_receipt_id": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID,
        "zero_counter_audit": counters,
        "positive_counter_audit": {
            "return_packet_emitted_count": rollup.get("return_packet_emitted_count"),
            "return_packet_validation_pass_count": rollup.get("return_packet_validation_pass_count"),
            "classification_request_emitted_count": rollup.get("classification_request_emitted_count"),
            "return_packet_classification_pass_count": rollup.get("return_packet_classification_pass_count"),
            "accepted_for_review_count": rollup.get("accepted_for_review_count"),
        },
        "zero_counters_clean": all(v == 0 for v in counters.values()),
        "boundary_status": "PASS" if all(v == 0 for v in counters.values()) else "FAIL",
    }

def closure_decision(readout: Dict[str, Any], audit: Dict[str, Any]) -> Dict[str, Any]:
    close = (
        readout["return_packet_validated"] is True
        and readout["classification"] == "RETURN_PACKET_ACCEPTED_FOR_REVIEW"
        and readout["accepted_for_review"] is True
        and readout["accepted_for_build"] is False
        and audit["boundary_status"] == "PASS"
    )
    return {
        "schema_version": "cell1_handoff_return_loop_closure_decision_v0",
        "decision_id": "handoff_return_close_" + sha8({"source": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID, "close": close}),
        "source_handoff_return_test_receipt_id": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID,
        "decision": "CLOSE_AND_FREEZE_HANDOFF_RETURN_REFERENCE" if close else "DO_NOT_CLOSE_REPAIR_REQUIRED",
        "closure_status": "CLOSED_REFERENCE_ONLY" if close else "OPEN_REPAIR_REQUIRED",
        "reason": "Bounded Cell1 handoff-return loop test passed, returned packet was accepted for review only, and boundary counters stayed clean." if close else "Return-loop closure blocked by validation, classification, or boundary audit failure.",
        "authorized_next_surface": "DECIDE_NEXT_BOUNDED_CELL1_OBJECTIVE_AFTER_RETURN_LOOP" if close else "REPAIR_CELL1_HANDOFF_RETURN_LOOP_TEST",
        "next_command_goal": None,
    }

def frozen_reference_packet(decision: Dict[str, Any], readout: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_frozen_reference_packet_v0",
        "reference_id": "CELL1_HANDOFF_RETURN_LOOP_REFERENCE_V0",
        "source_handoff_return_test_receipt_id": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID,
        "source_handoff_return_test_receipt_ref": rel(SOURCE_HANDOFF_RETURN_TEST_RECEIPT_PATH),
        "source_return_packet_ref": rel(SOURCE_HANDOFF_RETURN_PACKET_PATH),
        "source_return_classification_ref": rel(SOURCE_HANDOFF_RETURN_CLASSIFICATION_PATH),
        "source_authority_audit_ref": rel(SOURCE_HANDOFF_RETURN_AUTHORITY_AUDIT_PATH),
        "closure_decision_ref": rel(CLOSURE_DECISION_PATH),
        "reference_status": "FROZEN_REFERENCE_ONLY" if decision["decision"] == "CLOSE_AND_FREEZE_HANDOFF_RETURN_REFERENCE" else "NOT_FROZEN",
        "reference_meaning": readout["reference_proves"],
        "not_a_claim": readout["reference_does_not_prove"],
    }

def next_decision_surface(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_next_decision_surface_v0",
        "source_handoff_return_test_receipt_id": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID,
        "closure_decision": decision["decision"],
        "safe_next_decision_classes": [
            "DECIDE_NEXT_BOUNDED_CELL1_OBJECTIVE_AFTER_RETURN_LOOP",
            "CELL1_OBJECTIVE_ACCEPTED_PROPOSAL_VARIANT_TEST",
            "CELL1_OBJECTIVE_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK",
            "CELL1_OBJECTIVE_C5_PREFLIGHT_READINESS_CHECK",
            "CELL1_OBJECTIVE_CLOSE_CELL1_TRACK_FOR_NOW",
        ] if decision["decision"] == "CLOSE_AND_FREEZE_HANDOFF_RETURN_REFERENCE" else [
            "REPAIR_CELL1_HANDOFF_RETURN_LOOP_TEST",
            "RETURN_TO_HANDOFF_RETURN_DESIGN",
        ],
        "explicitly_not_licensed": [
            "C5 execution",
            "unbounded Cell1 execution",
            "runtime patch application",
            "target file modification",
            "general Cell1 authority",
            "accepted-for-build promotion",
            "hidden next command",
        ],
        "next_command_goal": None,
    }

def rollup(readout: Dict[str, Any], audit: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_review_or_close_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_handoff_return_test_receipt_id": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID,
        "source_handoff_return_design_receipt_id": SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID,
        "source_next_objective_receipt_id": SOURCE_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "return_packet_validated": readout["return_packet_validated"],
        "classification": readout["classification"],
        "accepted_for_review": readout["accepted_for_review"],
        "accepted_for_build": readout["accepted_for_build"],
        "boundary_status": audit["boundary_status"],
        "closure_decision": decision["decision"],
        "closure_status": decision["closure_status"],
        "reference_packets_emitted": 1 if decision["decision"] == "CLOSE_AND_FREEZE_HANDOFF_RETURN_REFERENCE" else 0,
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
        "rerun_handoff_return_test_count": 0,
        "recommended_next": "DECIDE_NEXT_BOUNDED_CELL1_OBJECTIVE_AFTER_RETURN_LOOP_V0",
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_review_or_close_profile_v0",
        "profile_id": "handoff_return_closed_" + sha8({"source": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID}),
        "status": "CELL1_HANDOFF_RETURN_LOOP_CLOSED_REFERENCE_ONLY" if rollup_obj["closure_decision"] == "CLOSE_AND_FREEZE_HANDOFF_RETURN_REFERENCE" else "CELL1_HANDOFF_RETURN_LOOP_REPAIR_REQUIRED",
        "source_handoff_return_test_receipt_id": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID,
        "closure_decision_ref": rel(CLOSURE_DECISION_PATH),
        "frozen_reference_packet_ref": rel(FROZEN_REFERENCE_PACKET_PATH),
        "next_decision_surface_ref": rel(NEXT_DECISION_SURFACE_PATH),
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "accepted_for_build": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in [
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
            "rerun_handoff_return_test_count",
        ]),
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_review_or_close_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_handoff_return_test_receipt_consumed_count": 1,
        "return_loop_readout_emitted_count": 1,
        "boundary_audit_emitted_count": 1,
        "closure_decision_emitted_count": 1,
        "frozen_reference_packet_emitted_count": rollup_obj["reference_packets_emitted"],
        "next_decision_surface_emitted_count": 1,
        "profile_status": profile_obj["status"],
        "closure_status": rollup_obj["closure_status"],
        "recommended_next_handling": rollup_obj["recommended_next"],
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "accepted_for_build_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
    }

def transition_trace(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_review_or_close_transition_trace_v0",
        "trace": [
            {
                "step": "consume_return_loop_test_receipt",
                "question": "did the bounded handoff-return loop test pass",
                "answer": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID,
                "taken": "audit_return_loop_boundary",
            },
            {
                "step": "audit_return_loop_boundary",
                "question": "did the return packet remain review-only without build/C5/runtime authority",
                "answer": "yes",
                "taken": "close_reference",
            },
            {
                "step": "close_reference",
                "question": "should the return-loop witness freeze as reference-only",
                "answer": decision["decision"],
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CELL1_HANDOFF_RETURN_LOOP_CLOSED_REFERENCE_ONLY" if decision["decision"] == "CLOSE_AND_FREEZE_HANDOFF_RETURN_REFERENCE" else "STOP_CELL1_HANDOFF_RETURN_LOOP_REPAIR_REQUIRED",
            "next_command_goal": None,
        },
    }

def validate_outputs(readout: Dict[str, Any], audit: Dict[str, Any], decision: Dict[str, Any], reference: Dict[str, Any], next_surface: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if readout.get("return_packet_validated") is not True:
        failures.append("readout_not_validated")
    if readout.get("classification") != "RETURN_PACKET_ACCEPTED_FOR_REVIEW":
        failures.append("readout_classification_wrong")
    if readout.get("accepted_for_review") is not True:
        failures.append("readout_not_accepted_for_review")
    if readout.get("accepted_for_build") is not False:
        failures.append("readout_accepts_for_build")
    if audit.get("boundary_status") != "PASS" or audit.get("zero_counters_clean") is not True:
        failures.append("boundary_audit_not_clean")
    if decision.get("decision") != "CLOSE_AND_FREEZE_HANDOFF_RETURN_REFERENCE":
        failures.append("closure_decision_not_close")
    if reference.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("reference_not_frozen")
    if next_surface.get("next_command_goal") is not None:
        failures.append("next_surface_hidden_command")
    if "C5 execution" not in next_surface.get("explicitly_not_licensed", []):
        failures.append("next_surface_missing_c5_block")
    for key in [
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
        "rerun_handoff_return_test_count",
    ]:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if rollup_obj.get("reference_packets_emitted") != 1:
        failures.append("reference_packet_count_not_one")
    if profile_obj.get("runtime_patch_applied") is not False:
        failures.append("profile_claims_runtime_patch")
    if profile_obj.get("target_file_modified") is not False:
        failures.append("profile_claims_target_file_modified")
    if profile_obj.get("c5_opened") is not False:
        failures.append("profile_claims_c5")
    if profile_obj.get("general_cell1_authority_granted") is not False:
        failures.append("profile_claims_general_cell1")
    if profile_obj.get("accepted_for_build") is not False:
        failures.append("profile_accepts_for_build")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "c5_opened_count",
        "general_cell1_authority_granted_count",
        "accepted_for_build_count",
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
    if terminal.get("stop_code") != "STOP_CELL1_HANDOFF_RETURN_LOOP_CLOSED_REFERENCE_ONLY":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    readout = read_json(RETURN_LOOP_READOUT_PATH)
    audit = read_json(BOUNDARY_AUDIT_PATH)
    decision = read_json(CLOSURE_DECISION_PATH)
    reference = read_json(FROZEN_REFERENCE_PACKET_PATH)
    next_surface = read_json(NEXT_DECISION_SURFACE_PATH)
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

    bad_readout = copy.deepcopy(readout)
    bad_readout["return_packet_validated"] = False
    add("readout_not_validated_fail", validate_outputs(bad_readout, audit, decision, reference, next_surface, rollup_obj, profile_obj, report_obj), "readout_not_validated")

    bad_readout = copy.deepcopy(readout)
    bad_readout["classification"] = "RETURN_PACKET_REPAIR_REQUIRED"
    add("readout_classification_wrong_fail", validate_outputs(bad_readout, audit, decision, reference, next_surface, rollup_obj, profile_obj, report_obj), "readout_classification_wrong")

    bad_readout = copy.deepcopy(readout)
    bad_readout["accepted_for_build"] = True
    add("readout_accepts_for_build_fail", validate_outputs(bad_readout, audit, decision, reference, next_surface, rollup_obj, profile_obj, report_obj), "readout_accepts_for_build")

    bad_audit = copy.deepcopy(audit)
    bad_audit["boundary_status"] = "FAIL"
    add("boundary_audit_not_clean_fail", validate_outputs(readout, bad_audit, decision, reference, next_surface, rollup_obj, profile_obj, report_obj), "boundary_audit_not_clean")

    bad_decision = copy.deepcopy(decision)
    bad_decision["decision"] = "DO_NOT_CLOSE_REPAIR_REQUIRED"
    add("closure_decision_not_close_fail", validate_outputs(readout, audit, bad_decision, reference, next_surface, rollup_obj, profile_obj, report_obj), "closure_decision_not_close")

    bad_reference = copy.deepcopy(reference)
    bad_reference["reference_status"] = "NOT_FROZEN"
    add("reference_not_frozen_fail", validate_outputs(readout, audit, decision, bad_reference, next_surface, rollup_obj, profile_obj, report_obj), "reference_not_frozen")

    bad_surface = copy.deepcopy(next_surface)
    bad_surface["next_command_goal"] = "RUN_C5"
    add("next_surface_hidden_command_fail", validate_outputs(readout, audit, decision, reference, bad_surface, rollup_obj, profile_obj, report_obj), "next_surface_hidden_command")

    bad_surface = copy.deepcopy(next_surface)
    bad_surface["explicitly_not_licensed"] = []
    add("next_surface_missing_c5_block_fail", validate_outputs(readout, audit, decision, reference, bad_surface, rollup_obj, profile_obj, report_obj), "next_surface_missing_c5_block")

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
        ("rerun_handoff_return_test_fail", "rerun_handoff_return_test_count"),
    ]:
        bad_rollup = copy.deepcopy(rollup_obj)
        bad_report = copy.deepcopy(report_obj)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(readout, audit, decision, reference, next_surface, bad_rollup, profile_obj, bad_report), counter)

    bad_rollup = copy.deepcopy(rollup_obj)
    bad_rollup["reference_packets_emitted"] = 0
    add("reference_packet_count_not_one_fail", validate_outputs(readout, audit, decision, reference, next_surface, bad_rollup, profile_obj, report_obj), "reference_packet_count_not_one")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_CELL1_HANDOFF_RETURN_REVIEW_EVIDENCE_REQUEST_REQUIRED", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "cell1_handoff_return_loop_review_or_close_receipt_v0",
            "receipt_type": "CELL1_HANDOFF_RETURN_LOOP_REVIEW_OR_CLOSE_RECEIPT",
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
        print(f"handoff_return_review_receipt_id={receipt_id}")
        print(f"handoff_return_review_receipt_path=data/cell1_handoff_return_loop_review_or_close_v0_receipts/{receipt_id}.json")
        return 1

    readout = return_loop_readout()
    audit = boundary_audit()
    decision = closure_decision(readout, audit)
    reference = frozen_reference_packet(decision, readout)
    next_surface = next_decision_surface(decision)
    rollup_obj = rollup(readout, audit, decision)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace(decision)

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(RETURN_LOOP_READOUT_PATH, readout)
    write_json(BOUNDARY_AUDIT_PATH, audit)
    write_json(CLOSURE_DECISION_PATH, decision)
    write_json(FROZEN_REFERENCE_PACKET_PATH, reference)
    write_json(NEXT_DECISION_SURFACE_PATH, next_surface)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(readout, audit, decision, reference, next_surface, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "HANDOFF_RETURN_CLOSE_0_TEST_RECEIPT_CONSUMED": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_PATH.exists(),
        "HANDOFF_RETURN_CLOSE_1_RETURN_PACKET_CONSUMED": SOURCE_HANDOFF_RETURN_PACKET_PATH.exists(),
        "HANDOFF_RETURN_CLOSE_2_CLASSIFICATION_CONSUMED": SOURCE_HANDOFF_RETURN_CLASSIFICATION_PATH.exists(),
        "HANDOFF_RETURN_CLOSE_3_RETURN_LOOP_READOUT_EMITTED": RETURN_LOOP_READOUT_PATH.exists(),
        "HANDOFF_RETURN_CLOSE_4_BOUNDARY_AUDIT_PASS": audit["boundary_status"] == "PASS",
        "HANDOFF_RETURN_CLOSE_5_CLOSURE_DECISION_EMITTED": CLOSURE_DECISION_PATH.exists() and decision["decision"] == "CLOSE_AND_FREEZE_HANDOFF_RETURN_REFERENCE",
        "HANDOFF_RETURN_CLOSE_6_REFERENCE_PACKET_FROZEN": FROZEN_REFERENCE_PACKET_PATH.exists() and reference["reference_status"] == "FROZEN_REFERENCE_ONLY",
        "HANDOFF_RETURN_CLOSE_7_NEXT_DECISION_SURFACE_EMITTED": NEXT_DECISION_SURFACE_PATH.exists(),
        "HANDOFF_RETURN_CLOSE_8_NO_RUNTIME_PATCH": rollup_obj["runtime_patch_applied_count"] == 0,
        "HANDOFF_RETURN_CLOSE_9_NO_TARGET_FILE_MODIFICATION": rollup_obj["target_file_modified_count"] == 0,
        "HANDOFF_RETURN_CLOSE_10_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "HANDOFF_RETURN_CLOSE_11_NO_GENERAL_CELL1_AUTHORITY": rollup_obj["general_cell1_authority_granted_count"] == 0,
        "HANDOFF_RETURN_CLOSE_12_NO_ACCEPTED_FOR_BUILD": rollup_obj["accepted_for_build"] is False,
        "HANDOFF_RETURN_CLOSE_13_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "HANDOFF_RETURN_CLOSE_14_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_handoff_return_test": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID,
        "decision": decision["decision"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "handoff_return_loop_readout": rel(RETURN_LOOP_READOUT_PATH),
        "boundary_audit": rel(BOUNDARY_AUDIT_PATH),
        "closure_decision": rel(CLOSURE_DECISION_PATH),
        "frozen_reference_packet": rel(FROZEN_REFERENCE_PACKET_PATH),
        "next_decision_surface": rel(NEXT_DECISION_SURFACE_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_handoff_return_test_receipt": rel(SOURCE_HANDOFF_RETURN_TEST_RECEIPT_PATH),
        "source_return_packet": rel(SOURCE_HANDOFF_RETURN_PACKET_PATH),
        "source_return_classification": rel(SOURCE_HANDOFF_RETURN_CLASSIFICATION_PATH),
        "source_authority_audit": rel(SOURCE_HANDOFF_RETURN_AUTHORITY_AUDIT_PATH),
        "source_design_receipt": rel(SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_PATH),
        "source_c2_lane_registry": rel(SOURCE_C2_LANE_REGISTRY_PATH),
    }

    guards = {
        "build_mode_review_or_close_only": BUILD_MODE == "HANDOFF_RETURN_LOOP_REVIEW_OR_CLOSE_ONLY",
        "closed_as_reference_only": decision["decision"] == "CLOSE_AND_FREEZE_HANDOFF_RETURN_REFERENCE",
        "reference_packet_frozen": reference["reference_status"] == "FROZEN_REFERENCE_ONLY",
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "accepted_for_build": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "cell1_handoff_return_loop_review_or_close_receipt_v0",
        "receipt_type": "CELL1_HANDOFF_RETURN_LOOP_REVIEW_OR_CLOSE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "review and close bounded Cell1 handoff-return loop test",
        "source_handoff_return_test_receipt_id": SOURCE_HANDOFF_RETURN_TEST_RECEIPT_ID,
        "source_handoff_return_design_receipt_id": SOURCE_HANDOFF_RETURN_DESIGN_RECEIPT_ID,
        "source_next_objective_receipt_id": SOURCE_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "handoff_return_review_summary": {
            "profile_status": profile_obj["status"],
            "return_packet_validated": readout["return_packet_validated"],
            "classification": readout["classification"],
            "accepted_for_review": readout["accepted_for_review"],
            "accepted_for_build": readout["accepted_for_build"],
            "boundary_status": audit["boundary_status"],
            "closure_decision": decision["decision"],
            "closure_status": decision["closure_status"],
            "reference_status": reference["reference_status"],
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "bad_counters_zero": profile_obj["bad_counters_zero"],
            "recommended_next": rollup_obj["recommended_next"],
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "handoff_return_review_guards": guards,
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
    if len(negative_controls) != 21 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"handoff_return_review_receipt_id={receipt_id}")
    print(f"handoff_return_review_receipt_path=data/cell1_handoff_return_loop_review_or_close_v0_receipts/{receipt_id}.json")
    print(f"handoff_return_review_closure_path=data/cell1_handoff_return_loop_review_or_close_v0/handoff_return_loop_closure_decision_v0.json")
    print(f"handoff_return_reference_packet_path=data/cell1_handoff_return_loop_review_or_close_v0/handoff_return_loop_frozen_reference_packet_v0.json")
    print(f"handoff_return_review_rollup_path=data/cell1_handoff_return_loop_review_or_close_v0/handoff_return_loop_review_or_close_rollup_v0.json")
    print(f"handoff_return_review_profile_path=data/cell1_handoff_return_loop_review_or_close_v0/handoff_return_loop_review_or_close_profile_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
