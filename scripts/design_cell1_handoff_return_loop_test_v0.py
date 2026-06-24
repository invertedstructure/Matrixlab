#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DESIGN_CELL1_HANDOFF_RETURN_LOOP_TEST_V0"
TARGET_UNIT_ID = "cell1.handoff_return_loop_test.design.v0"
LAYER = "CELL_1 / HANDOFF_RETURN_LOOP_DESIGN"
MODE = "DESIGN / TEST_SPEC / NO_EXECUTION"
BUILD_MODE = "HANDOFF_RETURN_LOOP_DESIGN_ONLY"

SOURCE_NEXT_OBJECTIVE_RECEIPT_ID = "c34d737d"
SOURCE_NEXT_OBJECTIVE_RECEIPT_PATH = ROOT / "data" / "cell1_next_bounded_objective_decision_v0_receipts" / "c34d737d.json"
SOURCE_NEXT_OBJECTIVE_DECISION_PATH = ROOT / "data" / "cell1_next_bounded_objective_decision_v0" / "objective_decision_record_v0.json"
SOURCE_NEXT_OBJECTIVE_AUTHORITY_PATH = ROOT / "data" / "cell1_next_bounded_objective_decision_v0" / "objective_authority_boundary_v0.json"
SOURCE_NEXT_OBJECTIVE_ROLLUP_PATH = ROOT / "data" / "cell1_next_bounded_objective_decision_v0" / "objective_rollup_v0.json"
SOURCE_NEXT_OBJECTIVE_PROFILE_PATH = ROOT / "data" / "cell1_next_bounded_objective_decision_v0" / "objective_profile_v0.json"
SOURCE_REFERENCE_READOUT_PATH = ROOT / "data" / "cell1_next_bounded_objective_decision_v0" / "reference_object_readout_v0.json"

SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID = "e1bc0ed0"
SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0_receipts" / "e1bc0ed0.json"
SOURCE_CELL1_REFERENCE_PACKET_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_frozen_reference_packet_v0.json"
SOURCE_CELL1_REVIEW_ROLLUP_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_review_or_close_rollup_v0.json"

SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID = "e6b0fd97"
SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0_receipts" / "e6b0fd97.json"
SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0" / "cell1_schema_consumption_verification_record_v0.json"

SOURCE_C4_CONSUMPTION_RECEIPT_ID = "c56792b7"
SOURCE_C4_CONSUMPTION_RECEIPT_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0_receipts" / "c56792b7.json"
SOURCE_CELL1_INTAKE_PACKET_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "cell1_intake_packet_v0.json"
SOURCE_C4_HANDOFF_PACKET_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "cell1_handoff_packet_v0.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_NEXT_OBJECTIVE_RECEIPT_PATH,
    SOURCE_NEXT_OBJECTIVE_DECISION_PATH,
    SOURCE_NEXT_OBJECTIVE_AUTHORITY_PATH,
    SOURCE_NEXT_OBJECTIVE_ROLLUP_PATH,
    SOURCE_NEXT_OBJECTIVE_PROFILE_PATH,
    SOURCE_REFERENCE_READOUT_PATH,
    SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_PATH,
    SOURCE_CELL1_REFERENCE_PACKET_PATH,
    SOURCE_CELL1_REVIEW_ROLLUP_PATH,
    SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH,
    SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH,
    SOURCE_C4_CONSUMPTION_RECEIPT_PATH,
    SOURCE_CELL1_INTAKE_PACKET_PATH,
    SOURCE_C4_HANDOFF_PACKET_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "cell1_handoff_return_loop_test_design_v0"
RECEIPT_DIR = ROOT / "data" / "cell1_handoff_return_loop_test_design_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "source_surface_v0.json"
OBJECTIVE_READOUT_PATH = OUT_DIR / "objective_readout_v0.json"
RETURN_LOOP_DESIGN_PATH = OUT_DIR / "handoff_return_loop_design_record_v0.json"
RETURN_CONTRACT_PATH = OUT_DIR / "handoff_return_contract_schema_v0.json"
TEST_PLAN_PATH = OUT_DIR / "handoff_return_loop_test_plan_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "handoff_return_loop_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "handoff_return_loop_design_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "handoff_return_loop_design_profile_v0.json"
REPORT_PATH = OUT_DIR / "handoff_return_loop_design_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "handoff_return_loop_design_transition_trace.json"

SELECTED_DECISION_CLASS = "CELL1_OBJECTIVE_HANDOFF_RETURN_LOOP_TEST"
FUTURE_TEST_UNIT = "RUN_CELL1_HANDOFF_RETURN_LOOP_TEST_FROM_DESIGN_V0"

ZERO_COUNTER_KEYS = [
    "test_executed_count",
    "cell1_execution_count",
    "cell0_execution_count",
    "c5_opened_count",
    "runtime_patch_applied_count",
    "target_file_modified_count",
    "general_cell1_authority_granted_count",
    "proposal_status_promoted_count",
    "accepted_proposal_fabricated_count",
    "taxonomy_registry_mutation_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "hidden_next_command_count",
]

HUMAN_DECISION = {
    "decision": "DESIGN_CELL1_HANDOFF_RETURN_LOOP_TEST",
    "scope": "Design the bounded Cell 1 handoff-return loop test selected by the next-objective decision. Emit a source surface, objective readout, return-loop design record, return contract schema, test plan, authority boundary, rollup, profile, report, transition trace, and receipt. Do not execute the test, do not open C5, do not run Cell 1 or Cell 0, do not apply runtime patches, do not modify targets, and do not emit hidden next command.",
    "authorized": [
        "consume next-objective decision receipt",
        "consume frozen Cell 1 reference readout",
        "design one bounded handoff-return loop test",
        "emit return contract schema",
        "emit future test plan",
        "emit authority boundary",
        "emit receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "execute handoff-return loop test",
        "run Cell 1",
        "run Cell 0",
        "open C5",
        "grant general Cell 1 authority",
        "apply runtime patch",
        "modify target files",
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

    next_receipt = read_json(SOURCE_NEXT_OBJECTIVE_RECEIPT_PATH)
    decision = read_json(SOURCE_NEXT_OBJECTIVE_DECISION_PATH)
    authority = read_json(SOURCE_NEXT_OBJECTIVE_AUTHORITY_PATH)
    next_rollup = read_json(SOURCE_NEXT_OBJECTIVE_ROLLUP_PATH)
    next_profile = read_json(SOURCE_NEXT_OBJECTIVE_PROFILE_PATH)
    readout = read_json(SOURCE_REFERENCE_READOUT_PATH)
    review_receipt = read_json(SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_PATH)
    reference = read_json(SOURCE_CELL1_REFERENCE_PACKET_PATH)
    schema_receipt = read_json(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH)
    verification = read_json(SOURCE_CELL1_SCHEMA_TEST_VERIFICATION_PATH)
    c4_receipt = read_json(SOURCE_C4_CONSUMPTION_RECEIPT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if next_receipt.get("receipt_id") != SOURCE_NEXT_OBJECTIVE_RECEIPT_ID or next_receipt.get("gate") != "PASS":
        failures.append("next_objective_receipt_not_pass")
    if next_receipt.get("terminal", {}).get("stop_code") != "STOP_CELL1_NEXT_BOUNDED_OBJECTIVE_DECIDED":
        failures.append("next_objective_wrong_terminal")
    if decision.get("selected_decision_class") != SELECTED_DECISION_CLASS:
        failures.append("selected_decision_not_handoff_return_loop")
    if decision.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("decision_has_hidden_next_command")
    if authority.get("may_execute_next_unit") is not False:
        failures.append("source_authority_allows_execution")
    if authority.get("may_open_c5") is not False:
        failures.append("source_authority_allows_c5")
    if authority.get("may_grant_general_cell1_authority") is not False:
        failures.append("source_authority_allows_general_cell1")
    if next_rollup.get("selected_decision_class") != SELECTED_DECISION_CLASS:
        failures.append("rollup_selected_decision_not_handoff_return_loop")
    if next_rollup.get("candidate_count") != 9:
        failures.append("candidate_count_not_nine")
    for key in [
        "c5_opened_count",
        "general_cell1_authority_granted_count",
        "new_cell1_execution_count",
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "hidden_next_command_count",
        "next_unit_executed_count",
    ]:
        if next_rollup.get(key) != 0:
            failures.append(f"source_next_rollup_counter_nonzero:{key}:{next_rollup.get(key)}")
    if next_profile.get("status") != "CELL1_NEXT_BOUNDED_OBJECTIVE_DECIDED":
        failures.append("next_objective_profile_not_decided")
    if readout.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("reference_readout_not_frozen")
    if review_receipt.get("receipt_id") != SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("cell1_review_receipt_not_pass")
    if reference.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("frozen_reference_not_frozen")
    if schema_receipt.get("receipt_id") != SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID or schema_receipt.get("gate") != "PASS":
        failures.append("schema_test_receipt_not_pass")
    if verification.get("verification_status") != "PASS" or verification.get("verification_scope") != "SCHEMA_CONSUMPTION_TEST_ONLY":
        failures.append("schema_verification_not_schema_only_pass")
    if c4_receipt.get("receipt_id") != SOURCE_C4_CONSUMPTION_RECEIPT_ID or c4_receipt.get("gate") != "PASS":
        failures.append("c4_consumption_receipt_not_pass")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_lane_basis_not_pass")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_design_source_surface_v0",
        "source_next_objective_receipt_id": SOURCE_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_next_objective_receipt_ref": rel(SOURCE_NEXT_OBJECTIVE_RECEIPT_PATH),
        "source_next_objective_decision_ref": rel(SOURCE_NEXT_OBJECTIVE_DECISION_PATH),
        "source_next_objective_authority_ref": rel(SOURCE_NEXT_OBJECTIVE_AUTHORITY_PATH),
        "source_reference_readout_ref": rel(SOURCE_REFERENCE_READOUT_PATH),
        "source_cell1_schema_review_receipt_id": SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID,
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "surface_status": "EXPLICIT_HANDOFF_RETURN_LOOP_DESIGN_SURFACE",
    }

def objective_readout() -> Dict[str, Any]:
    decision = read_json(SOURCE_NEXT_OBJECTIVE_DECISION_PATH)
    reference_readout = read_json(SOURCE_REFERENCE_READOUT_PATH)
    return {
        "schema_version": "cell1_handoff_return_loop_objective_readout_v0",
        "selected_decision_class": decision.get("selected_decision_class"),
        "why_selected": decision.get("why_selected"),
        "why_not_c5_yet": decision.get("why_not_c5_yet"),
        "why_not_general_cell1_authority": decision.get("why_not_general_cell1_authority"),
        "reference_proves": reference_readout.get("reference_proves", []),
        "reference_does_not_prove": reference_readout.get("reference_does_not_prove", []),
        "missing_edge_to_test": "Cell 1 returns a typed result object through review/Cell0 without ambiguity, authority leakage, hidden continuation, or label confusion.",
    }

def return_contract_schema() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_contract_schema_v0",
        "contract_id": "cell1_return_contract_" + sha8({"source": SOURCE_NEXT_OBJECTIVE_RECEIPT_ID}),
        "return_object_type": "CELL1_HANDOFF_RETURN_RESULT_PACKET",
        "required_fields": [
            "source_design_receipt_id",
            "source_cell1_reference_id",
            "result_packet_id",
            "origin_cell",
            "destination_surface",
            "result_kind",
            "bounded_test_scope",
            "claim_lanes",
            "evidence_refs",
            "authority_boundary",
            "negative_boundary_counters",
            "classification_request",
            "terminal",
        ],
        "allowed_result_kinds": [
            "SCHEMA_RESULT_RETURNED",
            "PROBE_RESULT_RETURNED",
            "VERIFICATION_RESULT_RETURNED",
            "REPAIR_REQUEST_RETURNED",
            "HALT_RETURNED",
        ],
        "destination_surface": "CELL0_OR_REVIEW_CLASSIFICATION_SURFACE",
        "authority_boundary": {
            "may_return_result_packet": True,
            "may_execute_runtime_patch": False,
            "may_modify_target_files": False,
            "may_open_c5": False,
            "may_grant_general_cell1_authority": False,
            "may_mutate_taxonomy": False,
        },
        "must_not_infer": [
            "returned result is accepted by Cell0",
            "runtime patch safety",
            "C5 authorization",
            "general Cell1 authority",
        ],
    }

def design_record(contract: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_design_record_v0",
        "design_id": "cell1_return_loop_design_" + sha8({"source": SOURCE_NEXT_OBJECTIVE_RECEIPT_ID, "contract": contract["contract_id"]}),
        "selected_decision_class": SELECTED_DECISION_CLASS,
        "future_test_unit": FUTURE_TEST_UNIT,
        "design_goal": "Design one bounded test that checks whether Cell1 can return a typed result packet to review/Cell0 and whether that returned object is classifiable without authority leakage.",
        "input_surface": {
            "source_next_objective_receipt_ref": rel(SOURCE_NEXT_OBJECTIVE_RECEIPT_PATH),
            "source_frozen_reference_packet_ref": rel(SOURCE_CELL1_REFERENCE_PACKET_PATH),
            "source_c2_lane_registry_ref": rel(SOURCE_C2_LANE_REGISTRY_PATH),
        },
        "return_contract_schema_ref": rel(RETURN_CONTRACT_PATH),
        "test_edges": [
            "Cell1 result packet emitted",
            "result packet references source Cell1 schema-consumption reference",
            "result packet declares bounded scope",
            "result packet preserves C2 label lanes",
            "result packet requests classification by review/Cell0",
            "result packet stops without hidden command",
        ],
        "failure_classes_to_detect": [
            "RETURN_PACKET_MISSING_SOURCE_REFERENCE",
            "RETURN_PACKET_LABEL_LANE_AMBIGUITY",
            "RETURN_PACKET_AUTHORITY_LEAK",
            "RETURN_PACKET_HIDDEN_NEXT_COMMAND",
            "RETURN_PACKET_CLAIMS_RUNTIME_PATCH",
            "RETURN_PACKET_CLAIMS_C5_AUTHORITY",
            "RETURN_PACKET_UNCLASSIFIABLE_BY_CELL0",
        ],
        "non_goals": [
            "runtime patch",
            "target file modification",
            "C5 opening",
            "general Cell1 authority",
            "taxonomy mutation",
            "automatic Cell0 acceptance",
        ],
    }

def test_plan(contract: Dict[str, Any], design: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_test_plan_v0",
        "test_plan_id": "cell1_return_loop_plan_" + sha8({"design": design["design_id"]}),
        "future_test_unit": FUTURE_TEST_UNIT,
        "design_record_ref": rel(RETURN_LOOP_DESIGN_PATH),
        "contract_schema_ref": rel(RETURN_CONTRACT_PATH),
        "test_mode": "BOUNDED_RETURN_LOOP_TEST_ONLY",
        "steps": [
            "load design receipt and contract",
            "construct one Cell1 return result packet from the frozen schema-consumption reference",
            "validate required fields and lane typing",
            "emit Cell0/review classification request surface",
            "classify returned packet as accepted-for-review, repair-required, or blocked",
            "emit rollup/profile/receipt",
            "stop",
        ],
        "acceptance_requirements": [
            "return packet emitted exactly once",
            "source reference preserved",
            "C2 lanes preserved",
            "authority boundary explicit",
            "classification request emitted",
            "no runtime patch",
            "no target file modification",
            "no C5",
            "no general Cell1 authority",
            "no hidden next command",
        ],
        "recommended_next_after_design": "RUN_CELL1_HANDOFF_RETURN_LOOP_TEST_FROM_DESIGN_V0",
        "next_command_goal": None,
    }

def authority_boundary() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_design_authority_boundary_v0",
        "authority_boundary_id": "handoff_return_design_authority_" + sha8({"source": SOURCE_NEXT_OBJECTIVE_RECEIPT_ID}),
        "may_emit_design_artifacts": True,
        "may_emit_future_test_plan": True,
        "may_emit_executable_command": False,
        "may_execute_test_now": False,
        "may_run_cell1": False,
        "may_run_cell0": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_promote_proposal_status": False,
        "may_fabricate_accepted_proposal": False,
        "must_not_infer": [
            "handoff-return loop test has executed",
            "Cell0 accepted the returned packet",
            "runtime patch safety",
            "C5 authorization",
            "general Cell1 authority",
        ],
    }

def rollup(contract: Dict[str, Any], design: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_design_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_next_objective_receipt_id": SOURCE_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_cell1_schema_review_receipt_id": SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID,
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "selected_decision_class": SELECTED_DECISION_CLASS,
        "future_test_unit": FUTURE_TEST_UNIT,
        "contract_schema_emitted_count": 1,
        "design_record_emitted_count": 1,
        "test_plan_emitted_count": 1,
        "authority_boundary_emitted_count": 1,
        "test_executed_count": 0,
        "cell1_execution_count": 0,
        "cell0_execution_count": 0,
        "c5_opened_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "general_cell1_authority_granted_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next": FUTURE_TEST_UNIT,
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_design_profile_v0",
        "profile_id": "cell1_return_loop_design_" + sha8({"source": SOURCE_NEXT_OBJECTIVE_RECEIPT_ID}),
        "status": "CELL1_HANDOFF_RETURN_LOOP_TEST_DESIGNED",
        "selected_decision_class": rollup_obj["selected_decision_class"],
        "future_test_unit": rollup_obj["future_test_unit"],
        "test_executed": False,
        "cell1_executed": False,
        "cell0_executed": False,
        "c5_opened": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_design_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_next_objective_receipt_consumed_count": 1,
        "objective_readout_emitted_count": 1,
        "contract_schema_emitted_count": 1,
        "design_record_emitted_count": 1,
        "test_plan_emitted_count": 1,
        "authority_boundary_emitted_count": 1,
        "profile_status": profile_obj["status"],
        "future_test_unit": rollup_obj["future_test_unit"],
        "test_executed_count": 0,
        "cell1_execution_count": 0,
        "cell0_execution_count": 0,
        "c5_opened_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "general_cell1_authority_granted_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "recommended_next_handling": rollup_obj["recommended_next"],
    }

def transition_trace(plan: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_handoff_return_loop_design_transition_trace_v0",
        "trace": [
            {
                "step": "consume_next_objective_decision",
                "question": "was handoff-return loop test selected",
                "answer": SELECTED_DECISION_CLASS,
                "taken": "read_missing_edge",
            },
            {
                "step": "read_missing_edge",
                "question": "what edge is missing after schema-consumption reference",
                "answer": "Cell1 return packet to review/Cell0",
                "taken": "design_contract",
            },
            {
                "step": "design_contract",
                "question": "what must a returned result packet contain",
                "answer": rel(RETURN_CONTRACT_PATH),
                "taken": "emit_test_plan",
            },
            {
                "step": "emit_test_plan",
                "question": "did the unit avoid execution and authority widening",
                "answer": "yes",
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CELL1_HANDOFF_RETURN_LOOP_TEST_DESIGNED",
            "next_command_goal": None,
        },
    }

def validate_outputs(contract: Dict[str, Any], design: Dict[str, Any], plan: Dict[str, Any], boundary: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if contract.get("return_object_type") != "CELL1_HANDOFF_RETURN_RESULT_PACKET":
        failures.append("contract_wrong_return_object_type")
    if contract.get("authority_boundary", {}).get("may_open_c5") is not False:
        failures.append("contract_allows_c5")
    if contract.get("authority_boundary", {}).get("may_execute_runtime_patch") is not False:
        failures.append("contract_allows_runtime_patch")
    if contract.get("authority_boundary", {}).get("may_modify_target_files") is not False:
        failures.append("contract_allows_target_file_modification")
    if design.get("selected_decision_class") != SELECTED_DECISION_CLASS:
        failures.append("design_wrong_selected_class")
    if design.get("future_test_unit") != FUTURE_TEST_UNIT:
        failures.append("design_wrong_future_unit")
    if "runtime patch" not in design.get("non_goals", []):
        failures.append("design_missing_runtime_patch_nongoal")
    if plan.get("future_test_unit") != FUTURE_TEST_UNIT:
        failures.append("plan_wrong_future_unit")
    if plan.get("next_command_goal") is not None:
        failures.append("plan_hidden_next_command")
    if boundary.get("may_emit_executable_command") is not False:
        failures.append("authority_allows_executable_command")
    if boundary.get("may_execute_test_now") is not False:
        failures.append("authority_allows_test_execution")
    if boundary.get("may_run_cell1") is not False:
        failures.append("authority_allows_cell1_run")
    if boundary.get("may_run_cell0") is not False:
        failures.append("authority_allows_cell0_run")
    if boundary.get("may_open_c5") is not False:
        failures.append("authority_allows_c5")
    if boundary.get("may_apply_runtime_patch") is not False:
        failures.append("authority_allows_runtime_patch")
    if boundary.get("may_modify_target_files") is not False:
        failures.append("authority_allows_target_file_modification")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if rollup_obj.get("contract_schema_emitted_count") != 1:
        failures.append("contract_schema_count_not_one")
    if rollup_obj.get("design_record_emitted_count") != 1:
        failures.append("design_record_count_not_one")
    if rollup_obj.get("test_plan_emitted_count") != 1:
        failures.append("test_plan_count_not_one")
    if profile_obj.get("test_executed") is not False:
        failures.append("profile_claims_test_executed")
    if profile_obj.get("cell1_executed") is not False:
        failures.append("profile_claims_cell1_executed")
    if profile_obj.get("cell0_executed") is not False:
        failures.append("profile_claims_cell0_executed")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "test_executed_count",
        "cell1_execution_count",
        "cell0_execution_count",
        "c5_opened_count",
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "general_cell1_authority_granted_count",
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
    if terminal.get("stop_code") != "STOP_CELL1_HANDOFF_RETURN_LOOP_TEST_DESIGNED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    contract = read_json(RETURN_CONTRACT_PATH)
    design = read_json(RETURN_LOOP_DESIGN_PATH)
    plan = read_json(TEST_PLAN_PATH)
    boundary = read_json(AUTHORITY_BOUNDARY_PATH)
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

    bad_contract = copy.deepcopy(contract)
    bad_contract["authority_boundary"]["may_open_c5"] = True
    add("contract_allows_c5_fail", validate_outputs(bad_contract, design, plan, boundary, rollup_obj, profile_obj, report_obj), "contract_allows_c5")

    bad_contract = copy.deepcopy(contract)
    bad_contract["authority_boundary"]["may_execute_runtime_patch"] = True
    add("contract_allows_runtime_patch_fail", validate_outputs(bad_contract, design, plan, boundary, rollup_obj, profile_obj, report_obj), "contract_allows_runtime_patch")

    bad_contract = copy.deepcopy(contract)
    bad_contract["authority_boundary"]["may_modify_target_files"] = True
    add("contract_allows_target_file_modification_fail", validate_outputs(bad_contract, design, plan, boundary, rollup_obj, profile_obj, report_obj), "contract_allows_target_file_modification")

    bad_design = copy.deepcopy(design)
    bad_design["selected_decision_class"] = "CELL1_OBJECTIVE_C5_PREFLIGHT_READINESS_CHECK"
    add("design_wrong_selected_class_fail", validate_outputs(contract, bad_design, plan, boundary, rollup_obj, profile_obj, report_obj), "design_wrong_selected_class")

    bad_plan = copy.deepcopy(plan)
    bad_plan["next_command_goal"] = "RUN_HANDOFF_RETURN_LOOP"
    add("plan_hidden_next_command_fail", validate_outputs(contract, design, bad_plan, boundary, rollup_obj, profile_obj, report_obj), "plan_hidden_next_command")

    for case, field, expected in [
        ("authority_allows_executable_command_fail", "may_emit_executable_command", "authority_allows_executable_command"),
        ("authority_allows_test_execution_fail", "may_execute_test_now", "authority_allows_test_execution"),
        ("authority_allows_cell1_run_fail", "may_run_cell1", "authority_allows_cell1_run"),
        ("authority_allows_cell0_run_fail", "may_run_cell0", "authority_allows_cell0_run"),
        ("authority_allows_c5_fail", "may_open_c5", "authority_allows_c5"),
        ("authority_allows_runtime_patch_fail", "may_apply_runtime_patch", "authority_allows_runtime_patch"),
        ("authority_allows_target_file_modification_fail", "may_modify_target_files", "authority_allows_target_file_modification"),
    ]:
        bad_boundary = copy.deepcopy(boundary)
        bad_boundary[field] = True
        add(case, validate_outputs(contract, design, plan, bad_boundary, rollup_obj, profile_obj, report_obj), expected)

    for case, counter in [
        ("test_executed_fail", "test_executed_count"),
        ("cell1_execution_fail", "cell1_execution_count"),
        ("cell0_execution_fail", "cell0_execution_count"),
        ("c5_opened_fail", "c5_opened_count"),
        ("runtime_patch_applied_fail", "runtime_patch_applied_count"),
        ("target_file_modified_fail", "target_file_modified_count"),
        ("general_cell1_authority_granted_fail", "general_cell1_authority_granted_count"),
        ("proposal_status_promoted_fail", "proposal_status_promoted_count"),
        ("accepted_proposal_fabricated_fail", "accepted_proposal_fabricated_count"),
        ("taxonomy_registry_mutated_fail", "taxonomy_registry_mutation_count"),
        ("source_mutation_fail", "source_mutation_count"),
        ("prior_receipt_mutation_fail", "prior_receipt_mutation_count"),
        ("hidden_next_command_fail", "hidden_next_command_count"),
    ]:
        bad_rollup = copy.deepcopy(rollup_obj)
        bad_report = copy.deepcopy(report_obj)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(contract, design, plan, boundary, bad_rollup, profile_obj, bad_report), counter)

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_CELL1_HANDOFF_RETURN_DESIGN_EVIDENCE_REQUEST_REQUIRED", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "cell1_handoff_return_loop_design_receipt_v0",
            "receipt_type": "CELL1_HANDOFF_RETURN_LOOP_DESIGN_RECEIPT",
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
        print(f"cell1_handoff_return_design_receipt_id={receipt_id}")
        print(f"cell1_handoff_return_design_receipt_path=data/cell1_handoff_return_loop_test_design_v0_receipts/{receipt_id}.json")
        return 1

    objective = objective_readout()
    contract = return_contract_schema()
    design = design_record(contract)
    plan = test_plan(contract, design)
    boundary = authority_boundary()
    rollup_obj = rollup(contract, design, plan)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace(plan)

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(OBJECTIVE_READOUT_PATH, objective)
    write_json(RETURN_CONTRACT_PATH, contract)
    write_json(RETURN_LOOP_DESIGN_PATH, design)
    write_json(TEST_PLAN_PATH, plan)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(contract, design, plan, boundary, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "HANDOFF_RETURN_DESIGN_0_NEXT_OBJECTIVE_RECEIPT_CONSUMED": SOURCE_NEXT_OBJECTIVE_RECEIPT_PATH.exists(),
        "HANDOFF_RETURN_DESIGN_1_SELECTED_OBJECTIVE_CONFIRMED": objective["selected_decision_class"] == SELECTED_DECISION_CLASS,
        "HANDOFF_RETURN_DESIGN_2_SOURCE_REFERENCE_READOUT_CONSUMED": SOURCE_REFERENCE_READOUT_PATH.exists(),
        "HANDOFF_RETURN_DESIGN_3_OBJECTIVE_READOUT_EMITTED": OBJECTIVE_READOUT_PATH.exists(),
        "HANDOFF_RETURN_DESIGN_4_RETURN_CONTRACT_SCHEMA_EMITTED": RETURN_CONTRACT_PATH.exists(),
        "HANDOFF_RETURN_DESIGN_5_DESIGN_RECORD_EMITTED": RETURN_LOOP_DESIGN_PATH.exists(),
        "HANDOFF_RETURN_DESIGN_6_TEST_PLAN_EMITTED": TEST_PLAN_PATH.exists(),
        "HANDOFF_RETURN_DESIGN_7_AUTHORITY_BOUNDARY_EMITTED": AUTHORITY_BOUNDARY_PATH.exists(),
        "HANDOFF_RETURN_DESIGN_8_NO_TEST_EXECUTED": rollup_obj["test_executed_count"] == 0,
        "HANDOFF_RETURN_DESIGN_9_NO_CELL1_EXECUTION": rollup_obj["cell1_execution_count"] == 0,
        "HANDOFF_RETURN_DESIGN_10_NO_CELL0_EXECUTION": rollup_obj["cell0_execution_count"] == 0,
        "HANDOFF_RETURN_DESIGN_11_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "HANDOFF_RETURN_DESIGN_12_NO_RUNTIME_PATCH": rollup_obj["runtime_patch_applied_count"] == 0,
        "HANDOFF_RETURN_DESIGN_13_NO_TARGET_FILE_MODIFICATION": rollup_obj["target_file_modified_count"] == 0,
        "HANDOFF_RETURN_DESIGN_14_NO_GENERAL_AUTHORITY": rollup_obj["general_cell1_authority_granted_count"] == 0,
        "HANDOFF_RETURN_DESIGN_15_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "HANDOFF_RETURN_DESIGN_16_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_next_objective": SOURCE_NEXT_OBJECTIVE_RECEIPT_ID,
        "future_test_unit": FUTURE_TEST_UNIT,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "objective_readout": rel(OBJECTIVE_READOUT_PATH),
        "handoff_return_contract_schema": rel(RETURN_CONTRACT_PATH),
        "handoff_return_loop_design_record": rel(RETURN_LOOP_DESIGN_PATH),
        "handoff_return_loop_test_plan": rel(TEST_PLAN_PATH),
        "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_next_objective_receipt": rel(SOURCE_NEXT_OBJECTIVE_RECEIPT_PATH),
        "source_next_objective_decision": rel(SOURCE_NEXT_OBJECTIVE_DECISION_PATH),
        "source_cell1_reference_packet": rel(SOURCE_CELL1_REFERENCE_PACKET_PATH),
        "source_c2_lane_registry": rel(SOURCE_C2_LANE_REGISTRY_PATH),
    }

    guards = {
        "build_mode_handoff_return_design_only": BUILD_MODE == "HANDOFF_RETURN_LOOP_DESIGN_ONLY",
        "future_test_unit_declared": FUTURE_TEST_UNIT,
        "test_executed": False,
        "cell1_executed": False,
        "cell0_executed": False,
        "c5_opened": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "general_cell1_authority_granted": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "cell1_handoff_return_loop_design_receipt_v0",
        "receipt_type": "CELL1_HANDOFF_RETURN_LOOP_DESIGN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "bounded Cell 1 handoff-return loop test design",
        "source_next_objective_receipt_id": SOURCE_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_cell1_schema_review_receipt_id": SOURCE_CELL1_SCHEMA_REVIEW_RECEIPT_ID,
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "handoff_return_design_summary": {
            "profile_status": profile_obj["status"],
            "selected_decision_class": SELECTED_DECISION_CLASS,
            "future_test_unit": FUTURE_TEST_UNIT,
            "contract_schema_emitted_count": 1,
            "design_record_emitted_count": 1,
            "test_plan_emitted_count": 1,
            "test_executed": False,
            "cell1_executed": False,
            "cell0_executed": False,
            "c5_opened": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "recommended_next": FUTURE_TEST_UNIT,
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "handoff_return_design_guards": guards,
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
    if len(negative_controls) != 25 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
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
    print(f"cell1_handoff_return_design_receipt_id={receipt_id}")
    print(f"cell1_handoff_return_design_receipt_path=data/cell1_handoff_return_loop_test_design_v0_receipts/{receipt_id}.json")
    print(f"cell1_handoff_return_design_record_path=data/cell1_handoff_return_loop_test_design_v0/handoff_return_loop_design_record_v0.json")
    print(f"cell1_handoff_return_contract_path=data/cell1_handoff_return_loop_test_design_v0/handoff_return_contract_schema_v0.json")
    print(f"cell1_handoff_return_test_plan_path=data/cell1_handoff_return_loop_test_design_v0/handoff_return_loop_test_plan_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
