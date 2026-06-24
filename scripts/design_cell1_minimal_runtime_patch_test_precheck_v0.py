#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DESIGN_CELL1_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK_V0"
TARGET_UNIT_ID = "cell1.minimal_runtime_patch_test_precheck.design.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TEST_PRECHECK_DESIGN"
MODE = "DESIGN / PRECHECK_SPEC / NO_EXECUTION"
BUILD_MODE = "MINIMAL_RUNTIME_PATCH_TEST_PRECHECK_DESIGN_ONLY"

SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID = "f595a9a6"
SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_PATH = ROOT / "data" / "cell1_next_bounded_objective_after_return_loop_v0_receipts" / "f595a9a6.json"
SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_DECISION_PATH = ROOT / "data" / "cell1_next_bounded_objective_after_return_loop_v0" / "objective_decision_record_v0.json"
SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_AUTHORITY_PATH = ROOT / "data" / "cell1_next_bounded_objective_after_return_loop_v0" / "objective_authority_boundary_v0.json"
SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_ROLLUP_PATH = ROOT / "data" / "cell1_next_bounded_objective_after_return_loop_v0" / "objective_rollup_v0.json"
SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_PROFILE_PATH = ROOT / "data" / "cell1_next_bounded_objective_after_return_loop_v0" / "objective_profile_v0.json"
SOURCE_REFERENCE_STACK_READOUT_PATH = ROOT / "data" / "cell1_next_bounded_objective_after_return_loop_v0" / "reference_stack_readout_v0.json"

SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID = "1d7c0a9b"
SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0_receipts" / "1d7c0a9b.json"
SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH = ROOT / "data" / "cell1_handoff_return_loop_review_or_close_v0" / "handoff_return_loop_frozen_reference_packet_v0.json"

SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID = "e1bc0ed0"
SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0_receipts" / "e1bc0ed0.json"
SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH = ROOT / "data" / "cell1_schema_consumption_test_review_or_close_v0" / "cell1_schema_test_frozen_reference_packet_v0.json"

SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID = "e6b0fd97"
SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH = ROOT / "data" / "cell1_schema_consumption_test_from_c4_handoff_v0_receipts" / "e6b0fd97.json"

SOURCE_C4_CONSUMPTION_RECEIPT_ID = "c56792b7"
SOURCE_C4_CONSUMPTION_RECEIPT_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0_receipts" / "c56792b7.json"
SOURCE_CELL1_INTAKE_PACKET_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "cell1_intake_packet_v0.json"
SOURCE_C4_HANDOFF_PACKET_PATH = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0" / "cell1_handoff_packet_v0.json"

SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID = "71bd1d92"
SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0_receipts" / "71bd1d92.json"
SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "accepted_proposal_packet_v0.json"
SOURCE_ACCEPTED_PROPOSAL_REVIEW_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "review_decision_record_v0.json"

SOURCE_C1_PATCH_RECEIPT_ID = "fffa3dd5"
SOURCE_C1_PATCH_RECEIPT_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0_receipts" / "fffa3dd5.json"
SOURCE_C1_PATCH_SCHEMA_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "proposal_packet_schema_v0_1.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_PATH,
    SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_DECISION_PATH,
    SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_AUTHORITY_PATH,
    SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_ROLLUP_PATH,
    SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_PROFILE_PATH,
    SOURCE_REFERENCE_STACK_READOUT_PATH,
    SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH,
    SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH,
    SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH,
    SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH,
    SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH,
    SOURCE_C4_CONSUMPTION_RECEIPT_PATH,
    SOURCE_CELL1_INTAKE_PACKET_PATH,
    SOURCE_C4_HANDOFF_PACKET_PATH,
    SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH,
    SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH,
    SOURCE_ACCEPTED_PROPOSAL_REVIEW_PATH,
    SOURCE_C1_PATCH_RECEIPT_PATH,
    SOURCE_C1_PATCH_SCHEMA_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0"
RECEIPT_DIR = ROOT / "data" / "cell1_minimal_runtime_patch_test_precheck_design_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "source_surface_v0.json"
REFERENCE_STACK_READOUT_PATH = OUT_DIR / "reference_stack_readout_v0.json"
PRECHECK_DESIGN_RECORD_PATH = OUT_DIR / "runtime_patch_precheck_design_record_v0.json"
ELIGIBILITY_CONTRACT_PATH = OUT_DIR / "runtime_patch_precheck_eligibility_contract_v0.json"
PRECHECK_TEST_PLAN_PATH = OUT_DIR / "runtime_patch_precheck_test_plan_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "runtime_patch_precheck_design_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_patch_precheck_design_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_patch_precheck_design_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_patch_precheck_design_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "runtime_patch_precheck_design_transition_trace.json"

SELECTED_DECISION_CLASS = "CELL1_OBJECTIVE_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK"
FUTURE_PRECHECK_UNIT = "RUN_CELL1_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK_FROM_DESIGN_V0"

ZERO_COUNTER_KEYS = [
    "precheck_executed_count",
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
    "decision": "DESIGN_CELL1_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK",
    "scope": "Design the bounded precheck selected by the post-return-loop objective decision. The design asks whether the current Cell1 stack has the accepted proposal, bounded target, verification gate, rollback/stop boundary, and authority surface required to be eligible for a later minimal runtime patch test. This unit emits design artifacts only. It does not run the precheck, does not apply a runtime patch, does not modify target files, does not open C5, and does not grant general Cell1 authority.",
    "authorized": [
        "consume post-return-loop next-objective decision",
        "consume frozen schema-intake reference",
        "consume frozen handoff-return reference",
        "consume accepted proposal packet",
        "design one bounded runtime-patch eligibility precheck",
        "emit eligibility contract",
        "emit future precheck test plan",
        "emit authority boundary",
        "emit receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "run eligibility precheck now",
        "apply runtime patch",
        "modify target files",
        "open C5",
        "grant general Cell1 authority",
        "promote accepted-for-review into accepted-for-build",
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

    next_receipt = read_json(SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_PATH)
    next_decision = read_json(SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_DECISION_PATH)
    next_authority = read_json(SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_AUTHORITY_PATH)
    next_rollup = read_json(SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_ROLLUP_PATH)
    next_profile = read_json(SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_PROFILE_PATH)
    stack_readout = read_json(SOURCE_REFERENCE_STACK_READOUT_PATH)
    return_close_receipt = read_json(SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_PATH)
    return_reference = read_json(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH)
    schema_close_receipt = read_json(SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_PATH)
    schema_reference = read_json(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH)
    schema_test_receipt = read_json(SOURCE_CELL1_SCHEMA_TEST_RECEIPT_PATH)
    c4_receipt = read_json(SOURCE_C4_CONSUMPTION_RECEIPT_PATH)
    accepted_receipt = read_json(SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH)
    accepted_packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    accepted_review = read_json(SOURCE_ACCEPTED_PROPOSAL_REVIEW_PATH)
    c1_receipt = read_json(SOURCE_C1_PATCH_RECEIPT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if next_receipt.get("receipt_id") != SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID or next_receipt.get("gate") != "PASS":
        failures.append("after_return_next_objective_receipt_not_pass")
    if next_receipt.get("terminal", {}).get("stop_code") != "STOP_CELL1_NEXT_BOUNDED_OBJECTIVE_AFTER_RETURN_LOOP_DECIDED":
        failures.append("after_return_next_objective_wrong_terminal")
    if next_decision.get("selected_decision_class") != SELECTED_DECISION_CLASS:
        failures.append("selected_decision_not_runtime_patch_precheck")
    if next_decision.get("recommended_next") != UNIT_ID:
        failures.append("recommended_next_not_this_design_unit")
    if next_decision.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("next_decision_hidden_next_command")
    if next_authority.get("may_apply_runtime_patch") is not False:
        failures.append("source_authority_allows_runtime_patch")
    if next_authority.get("may_modify_target_files") is not False:
        failures.append("source_authority_allows_target_modification")
    if next_authority.get("may_open_c5") is not False:
        failures.append("source_authority_allows_c5")
    if next_authority.get("may_execute_selected_objective") is not False:
        failures.append("source_authority_allows_selected_objective_execution")
    if next_rollup.get("selected_decision_class") != SELECTED_DECISION_CLASS:
        failures.append("rollup_selected_decision_wrong")
    if next_rollup.get("recommended_next") != UNIT_ID:
        failures.append("rollup_recommended_next_wrong")
    if next_profile.get("status") != "CELL1_NEXT_OBJECTIVE_AFTER_RETURN_LOOP_DECIDED":
        failures.append("next_profile_not_decided")
    if stack_readout.get("schema_consumption_reference", {}).get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("stack_schema_reference_not_frozen")
    if stack_readout.get("handoff_return_reference", {}).get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("stack_return_reference_not_frozen")
    if stack_readout.get("return_loop_observed", {}).get("accepted_for_review") is not True:
        failures.append("return_loop_not_review_accepted")
    if stack_readout.get("return_loop_observed", {}).get("accepted_for_build") is not False:
        failures.append("return_loop_accepted_for_build")
    if return_close_receipt.get("receipt_id") != SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID or return_close_receipt.get("gate") != "PASS":
        failures.append("handoff_return_close_receipt_not_pass")
    if return_reference.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("handoff_return_reference_not_frozen")
    if schema_close_receipt.get("receipt_id") != SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID or schema_close_receipt.get("gate") != "PASS":
        failures.append("schema_close_receipt_not_pass")
    if schema_reference.get("reference_status") != "FROZEN_REFERENCE_ONLY":
        failures.append("schema_reference_not_frozen")
    if schema_test_receipt.get("receipt_id") != SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID or schema_test_receipt.get("gate") != "PASS":
        failures.append("schema_test_receipt_not_pass")
    if c4_receipt.get("receipt_id") != SOURCE_C4_CONSUMPTION_RECEIPT_ID or c4_receipt.get("gate") != "PASS":
        failures.append("c4_consumption_receipt_not_pass")
    if accepted_receipt.get("receipt_id") != SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID or accepted_receipt.get("gate") != "PASS":
        failures.append("accepted_proposal_receipt_not_pass")
    if accepted_packet.get("status") != "ACCEPTED_FOR_BUILD":
        failures.append("accepted_packet_not_accepted_for_build")
    if accepted_review.get("review_decision") not in {"ACCEPTED_FOR_BUILD", "ACCEPT"} and accepted_review.get("decision") not in {"ACCEPTED_FOR_BUILD", "ACCEPT"}:
        failures.append("accepted_review_decision_not_accept")
    if c1_receipt.get("receipt_id") != SOURCE_C1_PATCH_RECEIPT_ID or c1_receipt.get("gate") != "PASS":
        failures.append("c1_patch_receipt_not_pass")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_receipt_not_pass")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_design_source_surface_v0",
        "source_after_return_next_objective_receipt_id": SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_after_return_next_objective_receipt_ref": rel(SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_PATH),
        "source_after_return_next_objective_decision_ref": rel(SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_DECISION_PATH),
        "source_schema_reference_packet_ref": rel(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH),
        "source_handoff_return_reference_packet_ref": rel(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH),
        "source_accepted_proposal_packet_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "source_c1_patch_schema_ref": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c2_lane_registry_ref": rel(SOURCE_C2_LANE_REGISTRY_PATH),
        "surface_status": "EXPLICIT_MINIMAL_RUNTIME_PATCH_PRECHECK_DESIGN_SURFACE",
    }

def reference_stack_readout() -> Dict[str, Any]:
    stack = read_json(SOURCE_REFERENCE_STACK_READOUT_PATH)
    proposal = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_reference_stack_readout_v0",
        "schema_consumption_reference": stack.get("schema_consumption_reference"),
        "handoff_return_reference": stack.get("handoff_return_reference"),
        "accepted_proposal": {
            "proposal_id": proposal.get("proposal_id"),
            "status": proposal.get("status"),
            "receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
            "packet_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        },
        "stack_now_proves": [
            "C4 to Cell1 schema intake was witnessed and frozen.",
            "Cell1 to review/Cell0 handoff-return was witnessed and frozen.",
            "An accepted proposal packet exists as a build-facing input candidate.",
        ],
        "stack_does_not_prove": [
            "runtime patch eligibility",
            "runtime patch safety",
            "target file modification authority",
            "C5 authorization",
            "general Cell1 builder authority",
            "that a patch target has been selected",
            "that rollback/stop semantics have been verified",
        ],
    }

def eligibility_contract() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_eligibility_contract_v0",
        "contract_id": "runtime_patch_precheck_contract_" + sha8({"source": SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID}),
        "precheck_object_type": "CELL1_MINIMAL_RUNTIME_PATCH_TEST_ELIGIBILITY_PRECHECK",
        "required_eligibility_fields": [
            "accepted_proposal_ref",
            "bounded_patch_target_ref",
            "target_file_write_scope",
            "verification_gate",
            "rollback_or_stop_boundary",
            "authority_boundary",
            "return_packet_or_review_surface",
            "negative_boundary_counters",
        ],
        "eligibility_questions": [
            "Does an accepted proposal packet exist and remain accepted-for-build?",
            "Is there exactly one bounded runtime patch target candidate?",
            "Is target modification forbidden during the precheck itself?",
            "Is the later patch test guarded by an explicit verification gate?",
            "Is rollback-or-stop behavior explicit before any target modification?",
            "Can the result return through the established Cell1 handoff-return surface?",
            "Does the precheck avoid C5 and general Cell1 authority?",
        ],
        "allowed_precheck_outcomes": [
            "ELIGIBLE_FOR_MINIMAL_RUNTIME_PATCH_TEST_DESIGN",
            "BLOCKED_MISSING_BOUNDED_TARGET",
            "BLOCKED_MISSING_VERIFICATION_GATE",
            "BLOCKED_MISSING_ROLLBACK_OR_STOP_BOUNDARY",
            "BLOCKED_AUTHORITY_BOUNDARY",
            "BLOCKED_ACCEPTED_PROPOSAL_GAP",
            "REQUEST_NARROWER_EVIDENCE",
        ],
        "authority_boundary": {
            "may_run_precheck_later": True,
            "may_apply_runtime_patch": False,
            "may_modify_target_files": False,
            "may_open_c5": False,
            "may_grant_general_cell1_authority": False,
            "may_promote_proposal_status": False,
            "may_fabricate_accepted_proposal": False,
        },
        "must_not_infer": [
            "precheck pass equals patch authorization",
            "accepted proposal equals target-write authority",
            "review acceptance equals build acceptance",
            "runtime patch safety",
            "C5 readiness",
            "general Cell1 authority",
        ],
    }

def design_record(contract: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_design_record_v0",
        "design_id": "runtime_patch_precheck_design_" + sha8({"source": SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID, "contract": contract["contract_id"]}),
        "selected_decision_class": SELECTED_DECISION_CLASS,
        "future_precheck_unit": FUTURE_PRECHECK_UNIT,
        "design_goal": "Design a bounded eligibility precheck for a later minimal runtime patch test. The precheck may inspect whether required ingredients exist, but may not apply a patch or modify targets.",
        "input_surface": {
            "source_after_return_next_objective_decision_ref": rel(SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_DECISION_PATH),
            "source_schema_reference_packet_ref": rel(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH),
            "source_handoff_return_reference_packet_ref": rel(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH),
            "source_accepted_proposal_packet_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
            "source_c1_patch_schema_ref": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
            "source_c2_lane_registry_ref": rel(SOURCE_C2_LANE_REGISTRY_PATH),
        },
        "eligibility_contract_ref": rel(ELIGIBILITY_CONTRACT_PATH),
        "precheck_edges": [
            "accepted proposal exists",
            "bounded target candidate declared",
            "verification gate declared",
            "rollback-or-stop boundary declared",
            "target modification remains forbidden during precheck",
            "C5 remains blocked",
            "general Cell1 authority remains blocked",
            "result can return through review/Cell0 surface",
        ],
        "failure_classes_to_detect": [
            "PRECHECK_ACCEPTED_PROPOSAL_GAP",
            "PRECHECK_BOUNDED_TARGET_MISSING",
            "PRECHECK_TARGET_SCOPE_UNBOUNDED",
            "PRECHECK_VERIFICATION_GATE_MISSING",
            "PRECHECK_ROLLBACK_OR_STOP_BOUNDARY_MISSING",
            "PRECHECK_AUTHORITY_LEAK_RUNTIME_PATCH",
            "PRECHECK_AUTHORITY_LEAK_TARGET_MODIFICATION",
            "PRECHECK_AUTHORITY_LEAK_C5",
            "PRECHECK_HIDDEN_NEXT_COMMAND",
        ],
        "non_goals": [
            "runtime patch application",
            "target file modification",
            "C5 opening",
            "general Cell1 authority",
            "proposal status promotion",
            "accepted proposal fabrication",
            "patch verification execution",
        ],
    }

def precheck_test_plan(contract: Dict[str, Any], design: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_test_plan_v0",
        "test_plan_id": "runtime_patch_precheck_plan_" + sha8({"design": design["design_id"]}),
        "future_precheck_unit": FUTURE_PRECHECK_UNIT,
        "design_record_ref": rel(PRECHECK_DESIGN_RECORD_PATH),
        "eligibility_contract_ref": rel(ELIGIBILITY_CONTRACT_PATH),
        "test_mode": "BOUNDED_RUNTIME_PATCH_ELIGIBILITY_PRECHECK_ONLY",
        "steps": [
            "load design receipt and eligibility contract",
            "load accepted proposal packet",
            "load frozen schema-intake and handoff-return references",
            "inspect for one bounded runtime patch target candidate",
            "inspect for verification gate shape",
            "inspect for rollback-or-stop boundary shape",
            "emit eligibility classification",
            "emit rollup/profile/receipt",
            "stop",
        ],
        "acceptance_requirements": [
            "accepted proposal preserved",
            "bounded target either declared or explicit missing",
            "verification gate either declared or explicit missing",
            "rollback-or-stop boundary either declared or explicit missing",
            "no runtime patch applied",
            "no target file modified",
            "no C5 opened",
            "no general Cell1 authority",
            "no hidden next command",
        ],
        "recommended_next_after_design": FUTURE_PRECHECK_UNIT,
        "next_command_goal": None,
    }

def authority_boundary() -> Dict[str, Any]:
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_design_authority_boundary_v0",
        "authority_boundary_id": "runtime_patch_precheck_design_authority_" + sha8({"source": SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID}),
        "may_emit_design_artifacts": True,
        "may_emit_future_precheck_plan": True,
        "may_emit_executable_command": False,
        "may_run_precheck_now": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_mutate_taxonomy": False,
        "may_promote_proposal_status": False,
        "may_fabricate_accepted_proposal": False,
        "must_not_infer": [
            "precheck has executed",
            "runtime patch is authorized",
            "target file modification is authorized",
            "C5 is authorized",
            "Cell1 is a general builder",
            "accepted proposal status may be changed",
        ],
    }

def rollup(contract: Dict[str, Any], design: Dict[str, Any], plan: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_design_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_after_return_next_objective_receipt_id": SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_handoff_return_close_receipt_id": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID,
        "source_schema_close_receipt_id": SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "selected_decision_class": SELECTED_DECISION_CLASS,
        "future_precheck_unit": FUTURE_PRECHECK_UNIT,
        "eligibility_contract_emitted_count": 1,
        "design_record_emitted_count": 1,
        "precheck_test_plan_emitted_count": 1,
        "authority_boundary_emitted_count": 1,
        "precheck_executed_count": 0,
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
        "recommended_next": FUTURE_PRECHECK_UNIT,
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_design_profile_v0",
        "profile_id": "runtime_patch_precheck_design_" + sha8({"source": SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID}),
        "status": "CELL1_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK_DESIGNED",
        "selected_decision_class": rollup_obj["selected_decision_class"],
        "future_precheck_unit": rollup_obj["future_precheck_unit"],
        "precheck_executed": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_design_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_after_return_next_objective_receipt_consumed_count": 1,
        "reference_stack_readout_emitted_count": 1,
        "eligibility_contract_emitted_count": rollup_obj["eligibility_contract_emitted_count"],
        "design_record_emitted_count": rollup_obj["design_record_emitted_count"],
        "precheck_test_plan_emitted_count": rollup_obj["precheck_test_plan_emitted_count"],
        "authority_boundary_emitted_count": rollup_obj["authority_boundary_emitted_count"],
        "profile_status": profile_obj["status"],
        "future_precheck_unit": rollup_obj["future_precheck_unit"],
        "recommended_next_handling": rollup_obj["recommended_next"],
        "precheck_executed_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
    }

def transition_trace(plan: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "cell1_minimal_runtime_patch_precheck_design_transition_trace_v0",
        "trace": [
            {
                "step": "consume_post_return_next_objective_decision",
                "question": "was minimal runtime patch test precheck selected",
                "answer": SELECTED_DECISION_CLASS,
                "taken": "read_reference_stack",
            },
            {
                "step": "read_reference_stack",
                "question": "are intake and return references both frozen",
                "answer": "yes",
                "taken": "design_eligibility_contract",
            },
            {
                "step": "design_eligibility_contract",
                "question": "what must be checked before a minimal runtime patch test can be designed",
                "answer": rel(ELIGIBILITY_CONTRACT_PATH),
                "taken": "emit_precheck_plan",
            },
            {
                "step": "emit_precheck_plan",
                "question": "did the unit avoid precheck execution and runtime patch authority",
                "answer": "yes",
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CELL1_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK_DESIGNED",
            "next_command_goal": None,
        },
    }

def validate_outputs(contract: Dict[str, Any], design: Dict[str, Any], plan: Dict[str, Any], boundary: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if contract.get("precheck_object_type") != "CELL1_MINIMAL_RUNTIME_PATCH_TEST_ELIGIBILITY_PRECHECK":
        failures.append("contract_wrong_precheck_object_type")
    if contract.get("authority_boundary", {}).get("may_apply_runtime_patch") is not False:
        failures.append("contract_allows_runtime_patch")
    if contract.get("authority_boundary", {}).get("may_modify_target_files") is not False:
        failures.append("contract_allows_target_file_modification")
    if contract.get("authority_boundary", {}).get("may_open_c5") is not False:
        failures.append("contract_allows_c5")
    if design.get("selected_decision_class") != SELECTED_DECISION_CLASS:
        failures.append("design_wrong_selected_class")
    if design.get("future_precheck_unit") != FUTURE_PRECHECK_UNIT:
        failures.append("design_wrong_future_precheck_unit")
    if "runtime patch application" not in design.get("non_goals", []):
        failures.append("design_missing_runtime_patch_nongoal")
    if plan.get("future_precheck_unit") != FUTURE_PRECHECK_UNIT:
        failures.append("plan_wrong_future_precheck_unit")
    if plan.get("next_command_goal") is not None:
        failures.append("plan_hidden_next_command")
    if boundary.get("may_emit_executable_command") is not False:
        failures.append("authority_allows_executable_command")
    if boundary.get("may_run_precheck_now") is not False:
        failures.append("authority_allows_precheck_execution")
    if boundary.get("may_apply_runtime_patch") is not False:
        failures.append("authority_allows_runtime_patch")
    if boundary.get("may_modify_target_files") is not False:
        failures.append("authority_allows_target_file_modification")
    if boundary.get("may_open_c5") is not False:
        failures.append("authority_allows_c5")
    if boundary.get("may_grant_general_cell1_authority") is not False:
        failures.append("authority_allows_general_cell1")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if rollup_obj.get("eligibility_contract_emitted_count") != 1:
        failures.append("eligibility_contract_count_not_one")
    if rollup_obj.get("design_record_emitted_count") != 1:
        failures.append("design_record_count_not_one")
    if rollup_obj.get("precheck_test_plan_emitted_count") != 1:
        failures.append("precheck_plan_count_not_one")
    if profile_obj.get("precheck_executed") is not False:
        failures.append("profile_claims_precheck_executed")
    if profile_obj.get("runtime_patch_applied") is not False:
        failures.append("profile_claims_runtime_patch")
    if profile_obj.get("target_file_modified") is not False:
        failures.append("profile_claims_target_file_modified")
    if profile_obj.get("c5_opened") is not False:
        failures.append("profile_claims_c5")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "precheck_executed_count",
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "c5_opened_count",
        "general_cell1_authority_granted_count",
        "taxonomy_registry_mutation_count",
        "proposal_status_promoted_count",
        "accepted_proposal_fabricated_count",
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
    if terminal.get("stop_code") != "STOP_CELL1_MINIMAL_RUNTIME_PATCH_TEST_PRECHECK_DESIGNED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    contract = read_json(ELIGIBILITY_CONTRACT_PATH)
    design = read_json(PRECHECK_DESIGN_RECORD_PATH)
    plan = read_json(PRECHECK_TEST_PLAN_PATH)
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
    bad_contract["authority_boundary"]["may_apply_runtime_patch"] = True
    add("contract_allows_runtime_patch_fail", validate_outputs(bad_contract, design, plan, boundary, rollup_obj, profile_obj, report_obj), "contract_allows_runtime_patch")

    bad_contract = copy.deepcopy(contract)
    bad_contract["authority_boundary"]["may_modify_target_files"] = True
    add("contract_allows_target_file_modification_fail", validate_outputs(bad_contract, design, plan, boundary, rollup_obj, profile_obj, report_obj), "contract_allows_target_file_modification")

    bad_contract = copy.deepcopy(contract)
    bad_contract["authority_boundary"]["may_open_c5"] = True
    add("contract_allows_c5_fail", validate_outputs(bad_contract, design, plan, boundary, rollup_obj, profile_obj, report_obj), "contract_allows_c5")

    bad_design = copy.deepcopy(design)
    bad_design["selected_decision_class"] = "CELL1_OBJECTIVE_C5_PREFLIGHT_READINESS_CHECK"
    add("design_wrong_selected_class_fail", validate_outputs(contract, bad_design, plan, boundary, rollup_obj, profile_obj, report_obj), "design_wrong_selected_class")

    bad_plan = copy.deepcopy(plan)
    bad_plan["next_command_goal"] = "RUN_PRECHECK"
    add("plan_hidden_next_command_fail", validate_outputs(contract, design, bad_plan, boundary, rollup_obj, profile_obj, report_obj), "plan_hidden_next_command")

    for case, field, expected in [
        ("authority_allows_executable_command_fail", "may_emit_executable_command", "authority_allows_executable_command"),
        ("authority_allows_precheck_execution_fail", "may_run_precheck_now", "authority_allows_precheck_execution"),
        ("authority_allows_runtime_patch_fail", "may_apply_runtime_patch", "authority_allows_runtime_patch"),
        ("authority_allows_target_file_modification_fail", "may_modify_target_files", "authority_allows_target_file_modification"),
        ("authority_allows_c5_fail", "may_open_c5", "authority_allows_c5"),
        ("authority_allows_general_cell1_fail", "may_grant_general_cell1_authority", "authority_allows_general_cell1"),
    ]:
        bad_boundary = copy.deepcopy(boundary)
        bad_boundary[field] = True
        add(case, validate_outputs(contract, design, plan, bad_boundary, rollup_obj, profile_obj, report_obj), expected)

    for case, counter in [
        ("precheck_executed_fail", "precheck_executed_count"),
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
        add(case, validate_outputs(contract, design, plan, boundary, bad_rollup, profile_obj, bad_report), counter)

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_CELL1_MINIMAL_RUNTIME_PATCH_PRECHECK_DESIGN_EVIDENCE_REQUEST_REQUIRED", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "cell1_minimal_runtime_patch_precheck_design_receipt_v0",
            "receipt_type": "CELL1_MINIMAL_RUNTIME_PATCH_PRECHECK_DESIGN_RECEIPT",
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
        print(f"minimal_runtime_patch_precheck_design_receipt_id={receipt_id}")
        print(f"minimal_runtime_patch_precheck_design_receipt_path=data/cell1_minimal_runtime_patch_test_precheck_design_v0_receipts/{receipt_id}.json")
        return 1

    stack = reference_stack_readout()
    contract = eligibility_contract()
    design = design_record(contract)
    plan = precheck_test_plan(contract, design)
    boundary = authority_boundary()
    rollup_obj = rollup(contract, design, plan)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace(plan)

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(REFERENCE_STACK_READOUT_PATH, stack)
    write_json(ELIGIBILITY_CONTRACT_PATH, contract)
    write_json(PRECHECK_DESIGN_RECORD_PATH, design)
    write_json(PRECHECK_TEST_PLAN_PATH, plan)
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
        "RUNTIME_PATCH_PRECHECK_DESIGN_0_NEXT_OBJECTIVE_RECEIPT_CONSUMED": SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_DESIGN_1_SELECTED_CLASS_CONFIRMED": design["selected_decision_class"] == SELECTED_DECISION_CLASS,
        "RUNTIME_PATCH_PRECHECK_DESIGN_2_REFERENCE_STACK_CONSUMED": SOURCE_REFERENCE_STACK_READOUT_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_DESIGN_3_ACCEPTED_PROPOSAL_CONSUMED": SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_DESIGN_4_STACK_READOUT_EMITTED": REFERENCE_STACK_READOUT_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_DESIGN_5_ELIGIBILITY_CONTRACT_EMITTED": ELIGIBILITY_CONTRACT_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_DESIGN_6_DESIGN_RECORD_EMITTED": PRECHECK_DESIGN_RECORD_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_DESIGN_7_PRECHECK_TEST_PLAN_EMITTED": PRECHECK_TEST_PLAN_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_DESIGN_8_AUTHORITY_BOUNDARY_EMITTED": AUTHORITY_BOUNDARY_PATH.exists(),
        "RUNTIME_PATCH_PRECHECK_DESIGN_9_NO_PRECHECK_EXECUTED": rollup_obj["precheck_executed_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_DESIGN_10_NO_RUNTIME_PATCH": rollup_obj["runtime_patch_applied_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_DESIGN_11_NO_TARGET_FILE_MODIFICATION": rollup_obj["target_file_modified_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_DESIGN_12_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_DESIGN_13_NO_GENERAL_CELL1_AUTHORITY": rollup_obj["general_cell1_authority_granted_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_DESIGN_14_NO_PROPOSAL_PROMOTION": rollup_obj["proposal_status_promoted_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_DESIGN_15_NO_ACCEPTED_PROPOSAL_FABRICATION": rollup_obj["accepted_proposal_fabricated_count"] == 0,
        "RUNTIME_PATCH_PRECHECK_DESIGN_16_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "RUNTIME_PATCH_PRECHECK_DESIGN_17_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_after_return_next_objective": SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID,
        "future_precheck_unit": FUTURE_PRECHECK_UNIT,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "reference_stack_readout": rel(REFERENCE_STACK_READOUT_PATH),
        "eligibility_contract": rel(ELIGIBILITY_CONTRACT_PATH),
        "precheck_design_record": rel(PRECHECK_DESIGN_RECORD_PATH),
        "precheck_test_plan": rel(PRECHECK_TEST_PLAN_PATH),
        "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_after_return_next_objective_receipt": rel(SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_PATH),
        "source_after_return_next_objective_decision": rel(SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_DECISION_PATH),
        "source_schema_reference_packet": rel(SOURCE_CELL1_SCHEMA_REFERENCE_PACKET_PATH),
        "source_handoff_return_reference_packet": rel(SOURCE_HANDOFF_RETURN_REFERENCE_PACKET_PATH),
        "source_accepted_proposal_packet": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "source_c1_patch_schema": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c2_lane_registry": rel(SOURCE_C2_LANE_REGISTRY_PATH),
    }

    guards = {
        "build_mode_precheck_design_only": BUILD_MODE == "MINIMAL_RUNTIME_PATCH_TEST_PRECHECK_DESIGN_ONLY",
        "selected_runtime_patch_precheck": design["selected_decision_class"] == SELECTED_DECISION_CLASS,
        "future_precheck_unit": FUTURE_PRECHECK_UNIT,
        "precheck_executed": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "proposal_status_promoted": False,
        "accepted_proposal_fabricated": False,
        "hidden_next_command": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "cell1_minimal_runtime_patch_precheck_design_receipt_v0",
        "receipt_type": "CELL1_MINIMAL_RUNTIME_PATCH_PRECHECK_DESIGN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "bounded Cell1 minimal runtime patch test eligibility precheck design",
        "source_after_return_next_objective_receipt_id": SOURCE_AFTER_RETURN_NEXT_OBJECTIVE_RECEIPT_ID,
        "source_handoff_return_close_receipt_id": SOURCE_HANDOFF_RETURN_CLOSE_RECEIPT_ID,
        "source_schema_close_receipt_id": SOURCE_CELL1_SCHEMA_CLOSE_RECEIPT_ID,
        "source_cell1_schema_test_receipt_id": SOURCE_CELL1_SCHEMA_TEST_RECEIPT_ID,
        "source_c4_consumption_receipt_id": SOURCE_C4_CONSUMPTION_RECEIPT_ID,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "minimal_runtime_patch_precheck_design_summary": {
            "profile_status": profile_obj["status"],
            "selected_decision_class": SELECTED_DECISION_CLASS,
            "future_precheck_unit": FUTURE_PRECHECK_UNIT,
            "eligibility_contract_emitted_count": rollup_obj["eligibility_contract_emitted_count"],
            "design_record_emitted_count": rollup_obj["design_record_emitted_count"],
            "precheck_test_plan_emitted_count": rollup_obj["precheck_test_plan_emitted_count"],
            "precheck_executed": False,
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
        "minimal_runtime_patch_precheck_design_guards": guards,
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
    print(f"minimal_runtime_patch_precheck_design_receipt_id={receipt_id}")
    print(f"minimal_runtime_patch_precheck_design_receipt_path=data/cell1_minimal_runtime_patch_test_precheck_design_v0_receipts/{receipt_id}.json")
    print(f"minimal_runtime_patch_precheck_design_record_path=data/cell1_minimal_runtime_patch_test_precheck_design_v0/runtime_patch_precheck_design_record_v0.json")
    print(f"minimal_runtime_patch_precheck_contract_path=data/cell1_minimal_runtime_patch_test_precheck_design_v0/runtime_patch_precheck_eligibility_contract_v0.json")
    print(f"minimal_runtime_patch_precheck_test_plan_path=data/cell1_minimal_runtime_patch_test_precheck_design_v0/runtime_patch_precheck_test_plan_v0.json")
    print(f"minimal_runtime_patch_precheck_rollup_path=data/cell1_minimal_runtime_patch_test_precheck_design_v0/runtime_patch_precheck_design_rollup_v0.json")
    print(f"minimal_runtime_patch_precheck_profile_path=data/cell1_minimal_runtime_patch_test_precheck_design_v0/runtime_patch_precheck_design_profile_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
