#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CELL1_SCHEMA_CONSUMPTION_TEST_REVIEW_OR_CLOSE_V0"
TARGET_UNIT_ID = "cell1.schema_consumption_test.review_or_close.v0"
LAYER = "CELL_1 / REVIEW_OR_CLOSE"
MODE = "REVIEW / CLOSURE / REFERENCE_FREEZE"
BUILD_MODE = "REVIEW_OR_CLOSE_ONLY"

SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID = "e6b0fd97"
SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0_receipts" / "e6b0fd97.json"
SOURCE_CELL1_SCHEMA_TEST_PROFILE_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0" / "cell1_schema_consumption_test_profile_v0.json"
SOURCE_CELL1_SCHEMA_TEST_ROLLUP_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0" / "cell1_schema_consumption_test_rollup_v0.json"
SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0" / "cell1_schema_consumption_verification_record_v0.json"
SOURCE_CELL1_SCHEMA_TEST_EXECUTION_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0" / "cell1_schema_consumption_execution_record_v0.json"
SOURCE_CELL1_AUTHORITY_CHECK_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0" / "cell1_authority_check_v0.json"
SOURCE_CELL1_INTAKE_CHECK_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0" / "cell1_intake_check_v0.json"
SOURCE_CELL1_SCHEMA_BINDING_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0" / "cell1_schema_binding_record_v0.json"
SOURCE_CELL1_PROBE_RESULT_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0" / "cell1_schema_consumption_probe_result_v0.json"
SOURCE_CELL1_NO_PATCH_OBSERVATION_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0" / "cell1_no_runtime_patch_observation_v0.json"
SOURCE_CELL1_HANDOFF_RESULT_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0" / "cell1_schema_test_handoff_result_v0.json"

SOURCE_C4_CONSUMPTION_RECEIPT_ID = "c56792b7"
SOURCE_C4_CONSUMPTION_RECEIPT_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0_receipts" / "c56792b7.json"
SOURCE_CELL1_INTAKE_PACKET_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "cell1_intake_packet_v0.json"
SOURCE_C4_HANDOFF_PACKET_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "cell1_handoff_packet_v0.json"

SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID = "71bd1d92"
SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0_receipts" / "71bd1d92.json"
SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "accepted_proposal_packet_v0.json"
SOURCE_REVIEW_DECISION_RECORD_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "review_decision_record_v0.json"

SOURCE_C1_PATCH_RECEIPT_ID = "fffa3dd5"
SOURCE_C1_PATCH_RECEIPT_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0_receipts" / "fffa3dd5.json"
SOURCE_C1_PATCH_SCHEMA_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "proposal_packet_schema_v0_1.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH,
    SOURCE_CELL1_SCHEMA_TEST_PROFILE_PATH,
    SOURCE_CELL1_SCHEMA_TEST_ROLLUP_PATH,
    SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH,
    SOURCE_CELL1_SCHEMA_TEST_EXECUTION_PATH,
    SOURCE_CELL1_AUTHORITY_CHECK_PATH,
    SOURCE_CELL1_INTAKE_CHECK_PATH,
    SOURCE_CELL1_SCHEMA_BINDING_PATH,
    SOURCE_CELL1_PROBE_RESULT_PATH,
    SOURCE_CELL1_NO_PATCH_OBSERVATION_PATH,
    SOURCE_CELL1_HANDOFF_RESULT_PATH,
    SOURCE_C4_CONSUMPTION_RECEIPT_PATH,
    SOURCE_CELL1_INTAKE_PACKET_PATH,
    SOURCE_C4_HANDOFF_PACKET_PATH,
    SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH,
    SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH,
    SOURCE_REVIEW_DECISION_RECORD_PATH,
    SOURCE_C1_PATCH_RECEIPT_PATH,
    SOURCE_C1_PATCH_SCHEMA_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0"
RECEIPT_DIR = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "cell1_schema_test_review_source_surface_v0.json"
REVIEW_CLASSIFICATION_PATH = OUT_DIR / "cell1_schema_test_review_classification_v0.json"
BOUNDARY_AUDIT_PATH = OUT_DIR / "cell1_schema_test_boundary_audit_v0.json"
CLOSURE_DECISION_PATH = OUT_DIR / "cell1_schema_test_closure_decision_v0.json"
FROZEN_REFERENCE_PACKET_PATH = OUT_DIR / "cell1_schema_test_frozen_reference_packet_v0.json"
NEXT_DECISION_SURFACE_PATH = OUT_DIR / "cell1_schema_test_next_decision_surface_v0.json"
ROLLUP_PATH = OUT_DIR / "cell1_schema_test_review_or_close_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "cell1_schema_test_review_or_close_profile_v0.json"
REPORT_PATH = OUT_DIR / "cell1_schema_test_review_or_close_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "cell1_schema_test_review_or_close_transition_trace.json"

ZERO_COUNTER_KEYS = [
    "runtime_patch_applied_count",
    "target_file_modified_count",
    "taxonomy_registry_mutation_count",
    "c5_opened_count",
    "general_cell1_authority_granted_count",
    "unbounded_payload_inspection_count",
    "proposal_status_promoted_count",
    "accepted_proposal_fabricated_count",
    "proposed_only_consumed_as_accepted_count",
    "hidden_next_command_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "unexpected_builder_command_count",
    "runtime_build_artifact_emitted_count",
    "new_cell1_execution_count",
    "rerun_cell1_schema_test_count",
]

HUMAN_DECISION = {
    "decision": "CELL1_SCHEMA_CONSUMPTION_TEST_REVIEW_OR_CLOSE",
    "scope": "Review the completed bounded Cell 1 schema-consumption test and either close it as a reference object or return a specific repair packet. This unit consumes the accepted Cell 1 schema-consumption test receipt and artifacts, audits the boundary counters, classifies the result, emits a closure decision, freezes the test as a reference packet, emits a next decision surface, and stops. It does not rerun Cell 1, does not apply runtime patches, does not modify targets, does not open C5, and does not emit a hidden next command.",
    "authorized": [
        "consume Cell 1 schema-consumption test receipt",
        "audit boundary counters",
        "classify schema-consumption test result",
        "emit closure decision",
        "freeze bounded Cell 1 schema-consumption test as reference",
        "emit next decision surface",
        "emit receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "rerun Cell 1",
        "apply runtime patch",
        "modify target files",
        "open C5",
        "grant general Cell 1 authority",
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

    receipt = read_json(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH)
    profile = read_json(SOURCE_CELL1_SCHEMA_TEST_PROFILE_PATH)
    rollup = read_json(SOURCE_CELL1_SCHEMA_TEST_ROLLUP_PATH)
    verification = read_json(SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH)
    execution = read_json(SOURCE_CELL1_SCHEMA_TEST_EXECUTION_PATH)
    authority = read_json(SOURCE_CELL1_AUTHORITY_CHECK_PATH)
    intake = read_json(SOURCE_CELL1_INTAKE_CHECK_PATH)
    binding = read_json(SOURCE_CELL1_SCHEMA_BINDING_PATH)
    probe = read_json(SOURCE_CELL1_PROBE_RESULT_PATH)
    no_patch = read_json(SOURCE_CELL1_NO_PATCH_OBSERVATION_PATH)
    handoff = read_json(SOURCE_CELL1_HANDOFF_RESULT_PATH)
    c4_receipt = read_json(SOURCE_C4_CONSUMPTION_RECEIPT_PATH)
    accepted_receipt = read_json(SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH)
    c1_receipt = read_json(SOURCE_C1_PATCH_RECEIPT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if receipt.get("receipt_id") != SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("cell1_schema_test_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != "STOP_CELL1_SCHEMA_CONSUMPTION_TEST_COMPLETE_REVIEW_OR_CLOSE":
        failures.append("cell1_schema_test_wrong_terminal")
    if profile.get("status") != "CELL1_SCHEMA_CONSUMPTION_TEST_COMPLETE":
        failures.append("cell1_schema_test_profile_not_complete")
    if rollup.get("cell1_schema_consumption_tests_run") != 1:
        failures.append("schema_test_run_count_not_one")
    if rollup.get("cell1_schema_consumption_tests_passed") != 1:
        failures.append("schema_test_pass_count_not_one")
    if rollup.get("cell1_bounded_execution_opened_count") != 1:
        failures.append("bounded_execution_count_not_one")
    if rollup.get("schema_consumption_verification_pass_count") != 1:
        failures.append("schema_verification_count_not_one")
    for key in ZERO_COUNTER_KEYS:
        if rollup.get(key, 0) != 0:
            failures.append(f"source_rollup_counter_nonzero:{key}:{rollup.get(key)}")
    if verification.get("verification_status") != "PASS" or verification.get("verification_scope") != "SCHEMA_CONSUMPTION_TEST_ONLY":
        failures.append("verification_not_schema_only_pass")
    if verification.get("runtime_patch_verified") is not False:
        failures.append("verification_claims_runtime_patch_verified")
    if verification.get("target_file_change_verified") is not False:
        failures.append("verification_claims_target_file_change_verified")
    if execution.get("execution_status") != "PASS" or execution.get("cell1_bounded_execution_opened") is not True:
        failures.append("execution_not_bounded_pass")
    if execution.get("runtime_patch_applied") is not False:
        failures.append("execution_claims_runtime_patch")
    if execution.get("target_file_modified") is not False:
        failures.append("execution_claims_target_file_modified")
    if authority.get("authority_status") != "PASS":
        failures.append("authority_check_not_pass")
    if intake.get("intake_status") != "PASS":
        failures.append("intake_check_not_pass")
    if binding.get("binding_status") != "PASS":
        failures.append("schema_binding_not_pass")
    if probe.get("probe_status") != "PASS":
        failures.append("probe_result_not_pass")
    if no_patch.get("observation_status") != "PASS":
        failures.append("no_patch_observation_not_pass")
    if handoff.get("handoff_result_status") != "CELL1_SCHEMA_CONSUMPTION_TEST_COMPLETE":
        failures.append("handoff_result_not_complete")
    if handoff.get("next_command_goal") is not None:
        failures.append("handoff_result_has_hidden_next_command")
    if c4_receipt.get("receipt_id") != SOURCE_C4_CONSUMPTION_RECEIPT_ID or c4_receipt.get("gate") != "PASS":
        failures.append("c4_consumption_basis_not_pass")
    if accepted_receipt.get("receipt_id") != SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID or accepted_receipt.get("gate") != "PASS":
        failures.append("accepted_proposal_basis_not_pass")
    if c1_receipt.get("receipt_id") != SOURCE_C1_PATCH_RECEIPT_ID or c1_receipt.get("gate") != "PASS":
        failures.append("c1_patch_basis_not_pass")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_basis_not_pass")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_schema_test_review_source_surface_v0",
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_cell1_schema_test_receipt_ref": rel(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH),
        "source_cell1_schema_test_profile_ref": rel(SOURCE_CELL1_SCHEMA_TEST_PROFILE_PATH),
        "source_cell1_schema_test_rollup_ref": rel(SOURCE_CELL1_SCHEMA_TEST_ROLLUP_PATH),
        "source_cell1_schema_test_verification_ref": rel(SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH),
        "source_cell1_schema_test_execution_ref": rel(SOURCE_CELL1_SCHEMA_TEST_EXECUTION_PATH),
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "surface_status": "EXPLICIT_CELL1_SCHEMA_TEST_REVIEW_SURFACE",
    }

def review_classification() -> Dict[str, Any]:
    rollup = read_json(SOURCE_CELL1_SCHEMA_TEST_ROLLUP_PATH)
    verification = read_json(SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH)
    profile = read_json(SOURCE_CELL1_SCHEMA_TEST_PROFILE_PATH)
    closure_ready = (
        rollup.get("cell1_schema_consumption_tests_run") == 1
        and rollup.get("cell1_schema_consumption_tests_passed") == 1
        and rollup.get("schema_consumption_verification_pass_count") == 1
        and verification.get("verification_status") == "PASS"
        and verification.get("verification_scope") == "SCHEMA_CONSUMPTION_TEST_ONLY"
        and profile.get("bad_counters_zero") is True
    )
    return {
        "schema_version": "cell1_schema_test_review_classification_v0",
        "classification_id": "cell1_schema_review_" + sha8({"receipt": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID, "closure_ready": closure_ready}),
        "source_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "classification": "CLOSE_AS_BOUNDED_REFERENCE_OBJECT" if closure_ready else "RETURN_REPAIR_PACKET",
        "classification_basis": {
            "test_run_count": rollup.get("cell1_schema_consumption_tests_run"),
            "test_pass_count": rollup.get("cell1_schema_consumption_tests_passed"),
            "bounded_execution_count": rollup.get("cell1_bounded_execution_opened_count"),
            "verification_pass_count": rollup.get("schema_consumption_verification_pass_count"),
            "verification_scope": verification.get("verification_scope"),
            "bad_counters_zero": profile.get("bad_counters_zero"),
        },
        "must_not_infer": [
            "runtime patch capability",
            "target file build correctness",
            "general Cell 1 authority",
            "C5 authorization",
        ],
    }

def boundary_audit() -> Dict[str, Any]:
    rollup = read_json(SOURCE_CELL1_SCHEMA_TEST_ROLLUP_PATH)
    counters = {key: rollup.get(key, 0) for key in ZERO_COUNTER_KEYS}
    expected_positive = {
        "cell1_schema_consumption_tests_run": rollup.get("cell1_schema_consumption_tests_run"),
        "cell1_schema_consumption_tests_passed": rollup.get("cell1_schema_consumption_tests_passed"),
        "cell1_bounded_execution_opened_count": rollup.get("cell1_bounded_execution_opened_count"),
        "schema_consumption_verification_pass_count": rollup.get("schema_consumption_verification_pass_count"),
    }
    return {
        "schema_version": "cell1_schema_test_boundary_audit_v0",
        "audit_id": "cell1_boundary_audit_" + sha8({"receipt": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID, "counters": counters}),
        "source_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "expected_positive_counters": expected_positive,
        "zero_counter_audit": counters,
        "zero_counters_clean": all(v == 0 for v in counters.values()),
        "boundary_status": "PASS" if all(v == 0 for v in counters.values()) else "FAIL",
    }

def closure_decision(classification: Dict[str, Any], audit: Dict[str, Any]) -> Dict[str, Any]:
    close = classification["classification"] == "CLOSE_AS_BOUNDED_REFERENCE_OBJECT" and audit["boundary_status"] == "PASS"
    return {
        "schema_version": "cell1_schema_test_closure_decision_v0",
        "decision_id": "cell1_schema_closure_" + sha8({"classification": classification["classification"], "audit": audit["boundary_status"]}),
        "source_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "decision": "CLOSE_AND_FREEZE_REFERENCE" if close else "DO_NOT_CLOSE_REPAIR_REQUIRED",
        "closure_status": "CLOSED_REFERENCE_ONLY" if close else "OPEN_REPAIR_REQUIRED",
        "reason": "Bounded Cell 1 schema-consumption test passed with clean boundaries and schema-only verification." if close else "Closure blocked by failed classification or boundary audit.",
        "authorized_next_surface": "DECIDE_NEXT_BOUNDED_CELL1_OBJECTIVE" if close else "REPAIR_CELL1_SCHEMA_CONSUMPTION_TEST",
        "next_command_goal": None,
    }

def frozen_reference_packet(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_schema_test_frozen_reference_packet_v0",
        "reference_id": "CELL1_SCHEMA_CONSUMPTION_TEST_REFERENCE_V0",
        "source_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_receipt_ref": rel(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH),
        "source_profile_ref": rel(SOURCE_CELL1_SCHEMA_TEST_PROFILE_PATH),
        "source_rollup_ref": rel(SOURCE_CELL1_SCHEMA_TEST_ROLLUP_PATH),
        "source_verification_ref": rel(SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH),
        "closure_decision_ref": rel(CLOSURE_DECISION_PATH),
        "reference_status": "FROZEN_REFERENCE_ONLY" if decision["decision"] == "CLOSE_AND_FREEZE_REFERENCE" else "NOT_FROZEN",
        "reference_meaning": [
            "Cell 1 executed once in a bounded schema-consumption-only test.",
            "The schema-consumption test passed.",
            "The verification scope is schema-consumption-only.",
            "No runtime patch was applied.",
            "No target file was modified.",
            "No C5 transition was authorized.",
            "No general Cell 1 authority was granted.",
        ],
        "not_a_claim": [
            "runtime patch capability",
            "target file build correctness",
            "general builder correctness",
            "future domain-shift readiness",
            "C5 authorization",
        ],
    }

def next_decision_surface(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_schema_test_next_decision_surface_v0",
        "source_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "closure_decision": decision["decision"],
        "safe_next_decision_classes": [
            "CLOSE_BRANCH_AND_WAIT_FOR_NEXT_OBJECTIVE",
            "DESIGN_NEXT_BOUNDED_CELL1_OBJECTIVE",
            "DESIGN_RUNTIME_PATCH_TEST_PRECHECK",
            "DESIGN_CELL1_TO_CELL0_FEEDBACK_SURFACE",
        ] if decision["decision"] == "CLOSE_AND_FREEZE_REFERENCE" else [
            "REPAIR_CELL1_SCHEMA_CONSUMPTION_TEST",
            "RETURN_TO_C4_CONSUMPTION_BOUNDARY",
        ],
        "explicitly_not_licensed": [
            "C5 domain shift",
            "unbounded Cell 1 execution",
            "runtime patch application",
            "taxonomy registry mutation",
            "hidden next command",
        ],
        "next_command_goal": None,
    }

def rollup(classification: Dict[str, Any], audit: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_schema_test_review_or_close_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "review_classification": classification["classification"],
        "boundary_status": audit["boundary_status"],
        "closure_decision": decision["decision"],
        "closure_status": decision["closure_status"],
        "reference_packets_emitted": 1 if decision["decision"] == "CLOSE_AND_FREEZE_REFERENCE" else 0,
        "new_cell1_execution_count": 0,
        "rerun_cell1_schema_test_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "unbounded_payload_inspection_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "proposed_only_consumed_as_accepted_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "unexpected_builder_command_count": 0,
        "runtime_build_artifact_emitted_count": 0,
        "recommended_next": "DECIDE_NEXT_BOUNDED_CELL1_OBJECTIVE",
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_schema_test_review_or_close_profile_v0",
        "profile_id": "cell1_schema_review_close_" + sha8({"source": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID, "decision": rollup_obj["closure_decision"]}),
        "status": "CELL1_SCHEMA_CONSUMPTION_TEST_CLOSED_REFERENCE_ONLY" if rollup_obj["closure_decision"] == "CLOSE_AND_FREEZE_REFERENCE" else "CELL1_SCHEMA_CONSUMPTION_TEST_REPAIR_REQUIRED",
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "closure_decision_ref": rel(CLOSURE_DECISION_PATH),
        "frozen_reference_packet_ref": rel(FROZEN_REFERENCE_PACKET_PATH),
        "next_decision_surface_ref": rel(NEXT_DECISION_SURFACE_PATH),
        "new_cell1_execution_performed": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_schema_test_review_or_close_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_cell1_schema_test_consumed_count": 1,
        "review_classification_emitted_count": 1,
        "boundary_audit_emitted_count": 1,
        "closure_decision_emitted_count": 1,
        "frozen_reference_packet_emitted_count": rollup_obj["reference_packets_emitted"],
        "next_decision_surface_emitted_count": 1,
        "profile_status": profile_obj["status"],
        "closure_status": rollup_obj["closure_status"],
        "new_cell1_execution_count": 0,
        "rerun_cell1_schema_test_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "c5_opened_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "recommended_next_handling": rollup_obj["recommended_next"],
    }

def transition_trace(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_schema_test_review_or_close_transition_trace_v0",
        "trace": [
            {
                "step": "consume_cell1_schema_test_receipt",
                "question": "did the bounded Cell 1 schema-consumption test pass",
                "answer": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
                "taken": "audit_boundary",
            },
            {
                "step": "audit_boundary",
                "question": "did runtime patch, target modification, taxonomy mutation, C5, or hidden continuation occur",
                "answer": "NO",
                "taken": "classify_for_closure",
            },
            {
                "step": "classify_for_closure",
                "question": "should the branch close as a reference object",
                "answer": decision["decision"],
                "taken": "freeze_reference_and_stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CELL1_SCHEMA_CONSUMPTION_TEST_CLOSED_REFERENCE_ONLY" if decision["decision"] == "CLOSE_AND_FREEZE_REFERENCE" else "STOP_CELL1_SCHEMA_CONSUMPTION_TEST_REPAIR_REQUIRED",
            "next_command_goal": None,
        },
    }

def validate_outputs(classification: Dict[str, Any], audit: Dict[str, Any], decision: Dict[str, Any], reference: Dict[str, Any], next_surface: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if classification.get("classification") != "CLOSE_AS_BOUNDED_REFERENCE_OBJECT":
        failures.append("classification_not_close")
    if audit.get("boundary_status") != "PASS" or audit.get("zero_counters_clean") is not True:
        failures.append("boundary_audit_not_clean")
    if decision.get("decision") != "CLOSE_AND_FREEZE_REFERENCE":
        failures.append("closure_decision_not_close")
    if reference.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("reference_not_frozen")
    if next_surface.get("next_command_goal") is not None:
        failures.append("next_surface_hidden_command")
    if "C5 domain shift" not in next_surface.get("explicitly_not_licensed", []):
        failures.append("next_surface_missing_c5_block")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if rollup_obj.get("reference_packets_emitted") != 1:
        failures.append("reference_packet_count_not_one")
    if profile_obj.get("new_cell1_execution_performed") is not False:
        failures.append("profile_claims_new_cell1_execution")
    if profile_obj.get("runtime_patch_applied") is not False:
        failures.append("profile_claims_runtime_patch")
    if profile_obj.get("target_file_modified") is not False:
        failures.append("profile_claims_target_file_modified")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "new_cell1_execution_count",
        "rerun_cell1_schema_test_count",
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "taxonomy_registry_mutation_count",
        "c5_opened_count",
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
    if terminal.get("stop_code") != "STOP_CELL1_SCHEMA_CONSUMPTION_TEST_CLOSED_REFERENCE_ONLY":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    classification = read_json(REVIEW_CLASSIFICATION_PATH)
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

    bad_classification = copy.deepcopy(classification)
    bad_classification["classification"] = "RETURN_REPAIR_PACKET"
    add("classification_not_close_fail", validate_outputs(bad_classification, audit, decision, reference, next_surface, rollup_obj, profile_obj, report_obj), "classification_not_close")

    bad_audit = copy.deepcopy(audit)
    bad_audit["boundary_status"] = "FAIL"
    add("boundary_audit_not_clean_fail", validate_outputs(classification, bad_audit, decision, reference, next_surface, rollup_obj, profile_obj, report_obj), "boundary_audit_not_clean")

    bad_decision = copy.deepcopy(decision)
    bad_decision["decision"] = "DO_NOT_CLOSE_REPAIR_REQUIRED"
    add("closure_decision_not_close_fail", validate_outputs(classification, audit, bad_decision, reference, next_surface, rollup_obj, profile_obj, report_obj), "closure_decision_not_close")

    bad_reference = copy.deepcopy(reference)
    bad_reference["reference_status"] = "NOT_FROZEN"
    add("reference_not_frozen_fail", validate_outputs(classification, audit, decision, bad_reference, next_surface, rollup_obj, profile_obj, report_obj), "reference_not_frozen")

    bad_surface = copy.deepcopy(next_surface)
    bad_surface["next_command_goal"] = "OPEN_C5"
    add("next_surface_hidden_command_fail", validate_outputs(classification, audit, decision, reference, bad_surface, rollup_obj, profile_obj, report_obj), "next_surface_hidden_command")

    bad_surface = copy.deepcopy(next_surface)
    bad_surface["explicitly_not_licensed"] = []
    add("next_surface_missing_c5_block_fail", validate_outputs(classification, audit, decision, reference, bad_surface, rollup_obj, profile_obj, report_obj), "next_surface_missing_c5_block")

    for case, counter in [
        ("runtime_patch_applied_fail", "runtime_patch_applied_count"),
        ("target_file_modified_fail", "target_file_modified_count"),
        ("taxonomy_registry_mutated_fail", "taxonomy_registry_mutation_count"),
        ("c5_opened_fail", "c5_opened_count"),
        ("general_cell1_authority_granted_fail", "general_cell1_authority_granted_count"),
        ("unbounded_payload_inspection_fail", "unbounded_payload_inspection_count"),
        ("proposal_status_promoted_fail", "proposal_status_promoted_count"),
        ("accepted_proposal_fabricated_fail", "accepted_proposal_fabricated_count"),
        ("proposed_only_consumed_as_accepted_fail", "proposed_only_consumed_as_accepted_count"),
        ("hidden_next_command_fail", "hidden_next_command_count"),
        ("source_mutation_fail", "source_mutation_count"),
        ("prior_receipt_mutation_fail", "prior_receipt_mutation_count"),
        ("unexpected_builder_command_fail", "unexpected_builder_command_count"),
        ("runtime_build_artifact_emitted_fail", "runtime_build_artifact_emitted_count"),
        ("new_cell1_execution_fail", "new_cell1_execution_count"),
        ("rerun_cell1_schema_test_fail", "rerun_cell1_schema_test_count"),
    ]:
        bad_rollup = copy.deepcopy(rollup_obj)
        bad_report = copy.deepcopy(report_obj)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(classification, audit, decision, reference, next_surface, bad_rollup, profile_obj, bad_report), counter)

    bad_rollup = copy.deepcopy(rollup_obj)
    bad_rollup["reference_packets_emitted"] = 0
    add("reference_packet_count_not_one_fail", validate_outputs(classification, audit, decision, reference, next_surface, bad_rollup, profile_obj, report_obj), "reference_packet_count_not_one")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_CELL1_SCHEMA_REVIEW_DEPENDENCY_MISSING", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "cell1_schema_test_review_or_close_receipt_v0",
            "receipt_type": "CELL1_SCHEMA_TEST_REVIEW_OR_CLOSE_RECEIPT",
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
        print(f"cell1_schema_review_receipt_id={receipt_id}")
        print(f"cell1_schema_review_receipt_path=data/cell1_schema_consumption_test_review_or_close_v0_receipts/{receipt_id}.json")
        return 1

    classification = review_classification()
    audit = boundary_audit()
    decision = closure_decision(classification, audit)
    reference = frozen_reference_packet(decision)
    next_surface = next_decision_surface(decision)
    rollup_obj = rollup(classification, audit, decision)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace(decision)

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(REVIEW_CLASSIFICATION_PATH, classification)
    write_json(BOUNDARY_AUDIT_PATH, audit)
    write_json(CLOSURE_DECISION_PATH, decision)
    write_json(FROZEN_REFERENCE_PACKET_PATH, reference)
    write_json(NEXT_DECISION_SURFACE_PATH, next_surface)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(classification, audit, decision, reference, next_surface, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "CELL1_REVIEW_0_CELL1_SCHEMA_TEST_RECEIPT_CONSUMED": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH.exists(),
        "CELL1_REVIEW_1_CELL1_SCHEMA_TEST_RECEIPT_PASS": read_json(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH).get("gate") == "PASS",
        "CELL1_REVIEW_2_VERIFICATION_SCHEMA_ONLY_PASS": read_json(SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH).get("verification_status") == "PASS" and read_json(SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH).get("verification_scope") == "SCHEMA_CONSUMPTION_TEST_ONLY",
        "CELL1_REVIEW_3_BOUNDARY_AUDIT_PASS": audit["boundary_status"] == "PASS",
        "CELL1_REVIEW_4_CLASSIFIED_FOR_CLOSURE": classification["classification"] == "CLOSE_AS_BOUNDED_REFERENCE_OBJECT",
        "CELL1_REVIEW_5_CLOSURE_DECISION_EMITTED": CLOSURE_DECISION_PATH.exists() and decision["decision"] == "CLOSE_AND_FREEZE_REFERENCE",
        "CELL1_REVIEW_6_REFERENCE_PACKET_FROZEN": FROZEN_REFERENCE_PACKET_PATH.exists() and reference["reference_status"] == "FROZEN_REFERENCE_ONLY",
        "CELL1_REVIEW_7_NEXT_DECISION_SURFACE_EMITTED": NEXT_DECISION_SURFACE_PATH.exists(),
        "CELL1_REVIEW_8_NO_NEW_CELL1_EXECUTION": rollup_obj["new_cell1_execution_count"] == 0,
        "CELL1_REVIEW_9_NO_CELL1_RERUN": rollup_obj["rerun_cell1_schema_test_count"] == 0,
        "CELL1_REVIEW_10_NO_RUNTIME_PATCH": rollup_obj["runtime_patch_applied_count"] == 0,
        "CELL1_REVIEW_11_NO_TARGET_FILE_MODIFIED": rollup_obj["target_file_modified_count"] == 0,
        "CELL1_REVIEW_12_NO_TAXONOMY_MUTATION": rollup_obj["taxonomy_registry_mutation_count"] == 0,
        "CELL1_REVIEW_13_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "CELL1_REVIEW_14_NO_GENERAL_CELL1_AUTHORITY": rollup_obj["general_cell1_authority_granted_count"] == 0,
        "CELL1_REVIEW_15_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "CELL1_REVIEW_16_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_cell1_schema_test": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "closure_decision": decision["decision"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "review_classification": rel(REVIEW_CLASSIFICATION_PATH),
        "boundary_audit": rel(BOUNDARY_AUDIT_PATH),
        "closure_decision": rel(CLOSURE_DECISION_PATH),
        "frozen_reference_packet": rel(FROZEN_REFERENCE_PACKET_PATH),
        "next_decision_surface": rel(NEXT_DECISION_SURFACE_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_cell1_schema_test_receipt": rel(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH),
        "source_cell1_schema_test_verification": rel(SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH),
        "source_cell1_schema_test_rollup": rel(SOURCE_CELL1_SCHEMA_TEST_ROLLUP_PATH),
        "source_c4_consumption_receipt": rel(SOURCE_C4_CONSUMPTION_RECEIPT_PATH),
        "source_accepted_proposal_packet": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "source_c1_patch_schema": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c2_lane_registry": rel(SOURCE_C2_LANE_REGISTRY_PATH),
    }

    guards = {
        "build_mode_review_or_close_only": BUILD_MODE == "REVIEW_OR_CLOSE_ONLY",
        "closed_as_reference_only": decision["decision"] == "CLOSE_AND_FREEZE_REFERENCE",
        "reference_packet_frozen": reference["reference_status"] == "FROZEN_REFERENCE_ONLY",
        "no_new_cell1_execution": True,
        "no_rerun": True,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "taxonomy_registry_mutated": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "cell1_schema_test_review_or_close_receipt_v0",
        "receipt_type": "CELL1_SCHEMA_TEST_REVIEW_OR_CLOSE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "review and close completed bounded Cell 1 schema-consumption test",
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "cell1_schema_review_summary": {
            "profile_status": profile_obj["status"],
            "review_classification": classification["classification"],
            "boundary_status": audit["boundary_status"],
            "closure_decision": decision["decision"],
            "closure_status": decision["closure_status"],
            "reference_status": reference["reference_status"],
            "new_cell1_execution_count": 0,
            "rerun_cell1_schema_test_count": 0,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "recommended_next": rollup_obj["recommended_next"],
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "cell1_schema_review_guards": guards,
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
    print(f"cell1_schema_review_receipt_id={receipt_id}")
    print(f"cell1_schema_review_receipt_path=data/cell1_schema_consumption_test_review_or_close_v0_receipts/{receipt_id}.json")
    print(f"cell1_schema_review_profile_path=data/cell1_schema_consumption_test_review_or_close_v0/cell1_schema_test_review_or_close_profile_v0.json")
    print(f"cell1_schema_review_rollup_path=data/cell1_schema_consumption_test_review_or_close_v0/cell1_schema_test_review_or_close_rollup_v0.json")
    print(f"cell1_schema_reference_packet_path=data/cell1_schema_consumption_test_review_or_close_v0/cell1_schema_test_frozen_reference_packet_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
