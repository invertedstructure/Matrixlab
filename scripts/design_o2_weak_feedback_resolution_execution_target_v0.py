#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DESIGN_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_execution_target.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_DESIGN"
MODE = "DESIGN_ONLY / WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET / NO_EXECUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_DESIGN_ONLY"

RT_DECISION_RECEIPT_ID = "1100f482"
RT_DECISION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0_receipts/1100f482.json"
RT_DECISION_BASIS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0/o2_rt_post_closure_decision_basis_v0.json"
RT_DECISION_TABLE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0/o2_rt_post_closure_decision_table_v0.json"
RT_SELECTED_BRANCH_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0/o2_rt_selected_next_branch_v0.json"
RT_EXECUTION_AUTH_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0/o2_weak_feedback_resolution_execution_target_authorization_v0.json"
RT_UNRESOLVED_CONTINUATION_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0/o2_weak_feedback_resolution_target_unresolved_continuation_v0.json"
RT_C5_BLOCK_CONTINUATION_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0/o2_rt_c5_block_continuation_v0.json"
RT_DEFERRED_BRANCHES_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0/o2_rt_deferred_branches_v0.json"
RT_DECISION_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0/o2_rt_post_closure_decision_authority_boundary_v0.json"
RT_DECISION_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0/o2_rt_post_closure_decision_classification_v0.json"
RT_DECISION_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0/o2_rt_post_closure_decision_rollup_v0.json"
RT_DECISION_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0/o2_rt_post_closure_decision_profile_v0.json"
RT_DECISION_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0/o2_rt_post_closure_decision_report.json"

RT_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0_receipts/32419538.json"
RT_REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_reviewed_reference_v0.json"
RT_SKELETON_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_skeleton_freeze_v0.json"
RT_ROUTE_MAP_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_route_map_freeze_v0.json"
RT_NONRESOLUTION_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_nonresolution_freeze_v0.json"
RT_C5_BLOCK_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_c5_block_freeze_v0.json"

RT_QUESTION_SKELETONS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_question_packet_answer_record_skeletons_v0.jsonl"
RT_SOURCE_REF_SKELETONS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_source_ref_satisfaction_record_skeletons_v0.jsonl"
RT_UNDERTYPED_SKELETONS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_under_typed_acceptance_review_record_skeletons_v0.jsonl"
RT_PARKING_SKELETONS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_parking_continuation_record_skeletons_v0.jsonl"
RT_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_route_map_v0.jsonl"
RT_GATE_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_gate_readout_v0.json"
RT_C5_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_c5_reconsideration_readout_v0.json"

REQUIRED_SOURCE_FILES = [
    RT_DECISION_RECEIPT_PATH,
    RT_DECISION_BASIS_PATH,
    RT_DECISION_TABLE_PATH,
    RT_SELECTED_BRANCH_PATH,
    RT_EXECUTION_AUTH_PATH,
    RT_UNRESOLVED_CONTINUATION_PATH,
    RT_C5_BLOCK_CONTINUATION_PATH,
    RT_DEFERRED_BRANCHES_PATH,
    RT_DECISION_AUTHORITY_PATH,
    RT_DECISION_CLASSIFICATION_PATH,
    RT_DECISION_ROLLUP_PATH,
    RT_DECISION_PROFILE_PATH,
    RT_DECISION_REPORT_PATH,
    RT_CLOSURE_RECEIPT_PATH,
    RT_REVIEWED_REFERENCE_PATH,
    RT_SKELETON_FREEZE_PATH,
    RT_ROUTE_MAP_FREEZE_PATH,
    RT_NONRESOLUTION_FREEZE_PATH,
    RT_C5_BLOCK_FREEZE_PATH,
    RT_QUESTION_SKELETONS_PATH,
    RT_SOURCE_REF_SKELETONS_PATH,
    RT_UNDERTYPED_SKELETONS_PATH,
    RT_PARKING_SKELETONS_PATH,
    RT_ROUTE_MAP_PATH,
    RT_GATE_READOUT_PATH,
    RT_C5_READOUT_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0_receipts"

TARGET_DEFINITION_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_definition_v0.json"
INPUT_SURFACE_INVENTORY_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_input_surface_inventory_v0.json"
PROPOSED_QUESTION_ANSWER_CONTRACT_PATH = OUT_DIR / "o2_proposed_question_answer_execution_contract_v0.json"
PROPOSED_SOURCE_REF_CONTRACT_PATH = OUT_DIR / "o2_proposed_source_ref_satisfaction_execution_contract_v0.json"
PROPOSED_UNDERTYPED_REVIEW_CONTRACT_PATH = OUT_DIR / "o2_proposed_under_typed_acceptance_review_execution_contract_v0.json"
PROPOSED_PARKING_CONTRACT_PATH = OUT_DIR / "o2_parking_execution_continuation_contract_v0.json"
PROPOSED_RESOLUTION_RECORD_CONTRACT_PATH = OUT_DIR / "o2_proposed_weak_feedback_resolution_record_contract_v0.json"
EXECUTION_GATE_CONTRACT_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_gate_contract_v0.json"
PROPOSAL_REVIEW_BOUNDARY_PATH = OUT_DIR / "o2_resolution_proposal_review_boundary_v0.json"
C5_BLOCK_CONTRACT_PATH = OUT_DIR / "o2_resolution_execution_c5_block_contract_v0.json"
NEGATIVE_CONTROLS_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_negative_controls_v0.json"
BUILD_AUTHORIZATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_build_authorization_v0.json"
UNRESOLVED_CONTINUATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_unresolved_continuation_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_report.json"
TRACE_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_transition_trace.json"

EXPECTED_DECISION_STATUS = "TYPED_O2_RT_POST_CLOSURE_DECISION_SELECTED_RESOLUTION_EXECUTION_TARGET_DESIGN_READY"
EXPECTED_DECISION_STOP = "STOP_TYPED_O2_RT_POST_CLOSURE_DECISION_SELECTED_RESOLUTION_EXECUTION_TARGET_DESIGN_READY"
EXPECTED_DECISION_NEXT = "DESIGN_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_V0"
AUTHORIZED_BUILD_UNIT = "BUILD_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_V0"

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

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(RT_DECISION_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_rt_post_closure_decision_summary", {})
    basis = read_json(RT_DECISION_BASIS_PATH)
    selected = read_json(RT_SELECTED_BRANCH_PATH)
    auth = read_json(RT_EXECUTION_AUTH_PATH)
    unresolved = read_json(RT_UNRESOLVED_CONTINUATION_PATH)
    c5_block = read_json(RT_C5_BLOCK_CONTINUATION_PATH)
    decision_authority = read_json(RT_DECISION_AUTHORITY_PATH)
    decision_rollup = read_json(RT_DECISION_ROLLUP_PATH)
    decision_profile = read_json(RT_DECISION_PROFILE_PATH)

    closure_receipt = read_json(RT_CLOSURE_RECEIPT_PATH)
    reviewed_reference = read_json(RT_REVIEWED_REFERENCE_PATH)
    skeleton_freeze = read_json(RT_SKELETON_FREEZE_PATH)
    route_freeze = read_json(RT_ROUTE_MAP_FREEZE_PATH)
    nonresolution_freeze = read_json(RT_NONRESOLUTION_FREEZE_PATH)
    c5_freeze = read_json(RT_C5_BLOCK_FREEZE_PATH)

    question_skeletons = read_jsonl(RT_QUESTION_SKELETONS_PATH)
    source_ref_skeletons = read_jsonl(RT_SOURCE_REF_SKELETONS_PATH)
    undertyped_skeletons = read_jsonl(RT_UNDERTYPED_SKELETONS_PATH)
    parking_skeletons = read_jsonl(RT_PARKING_SKELETONS_PATH)
    route_map = read_jsonl(RT_ROUTE_MAP_PATH)
    gate_readout = read_json(RT_GATE_READOUT_PATH)
    c5_readout = read_json(RT_C5_READOUT_PATH)

    if receipt.get("receipt_id") != RT_DECISION_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("rt_post_closure_decision_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_DECISION_STOP:
        failures.append("rt_post_closure_decision_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("rt_post_closure_decision_hidden_next_command")
    if summary.get("status") != EXPECTED_DECISION_STATUS:
        failures.append(f"rt_post_closure_decision_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_DECISION_NEXT:
        failures.append(f"rt_post_closure_decision_next_wrong:{summary.get('recommended_next')}")
    if summary.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("selected_next_unit_wrong")
    if summary.get("selected_next_branch") != "DESIGN_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET":
        failures.append("selected_next_branch_wrong")

    for key in ["post_closure_decision_complete", "resolution_target_reference_closed", "bad_counters_zero"]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "question_answer_skeletons_available_count": 3,
        "source_ref_satisfaction_skeletons_available_count": 2,
        "under_typed_acceptance_review_skeletons_available_count": 2,
        "parking_continuation_skeletons_available_count": 3,
        "route_map_records_available_count": 3,
        "resolution_records_emitted_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    for key in [
        "weak_feedback_resolved",
        "question_packets_answered",
        "source_ref_requests_satisfied",
        "under_typed_acceptance_approved",
        "parking_counted_as_resolution",
        "c5_reconsideration_ready",
        "c5_opened",
        "live_feedback_audit_executed",
        "repair_applied",
        "retry_executed",
        "target_selected_for_build",
        "runtime_patch_applied",
        "source_mutated",
        "prior_receipt_mutated",
        "architecture_change",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if summary.get(key) is not False:
            failures.append(f"summary_forbidden_true:{key}")

    if summary.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("summary_c5_not_blocked")
    if basis.get("basis_status") != "BASIS_ACCEPTED":
        failures.append("basis_not_accepted")
    if selected.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("selected_branch_artifact_wrong")
    if auth.get("authorized_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("execution_auth_next_wrong")
    if unresolved.get("weak_feedback_resolved") is not False or unresolved.get("resolution_records_emitted_count") != 0:
        failures.append("unresolved_continuation_wrong")
    if c5_block.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_block.get("c5_opened") is not False:
        failures.append("c5_block_continuation_wrong")
    if decision_authority.get("may_design_o2_weak_feedback_resolution_execution_target_next") is not True:
        failures.append("decision_authority_no_design_next")
    if decision_authority.get("may_execute_resolution_now") is not False:
        failures.append("decision_authority_allows_execution")
    if decision_rollup.get("selected_execution_target_design_count") != 1:
        failures.append("decision_rollup_selected_wrong")
    if decision_profile.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("decision_profile_next_wrong")

    if closure_receipt.get("receipt_id") != "32419538":
        failures.append("closure_receipt_wrong")
    if reviewed_reference.get("weak_feedback_resolved") is not False or reviewed_reference.get("resolution_records_emitted_count") != 0:
        failures.append("reviewed_reference_wrong")
    if skeleton_freeze.get("question_answer_skeletons_frozen_count") != 3:
        failures.append("skeleton_freeze_wrong")
    if route_freeze.get("all_route_map_records_unresolved") is not True or route_freeze.get("resolution_records_emitted_count") != 0:
        failures.append("route_freeze_wrong")
    if nonresolution_freeze.get("weak_feedback_resolved") is not False or nonresolution_freeze.get("resolution_records_emitted_count") != 0:
        failures.append("nonresolution_freeze_wrong")
    if c5_freeze.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_freeze.get("c5_reconsideration_ready") is not False:
        failures.append("c5_freeze_wrong")

    if len(question_skeletons) != 3 or len(source_ref_skeletons) != 2 or len(undertyped_skeletons) != 2 or len(parking_skeletons) != 3 or len(route_map) != 3:
        failures.append("surface_counts_wrong")
    if gate_readout.get("weak_feedback_resolved") is not False or gate_readout.get("resolution_records_emitted_count") != 0:
        failures.append("gate_readout_wrong")
    if c5_readout.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_readout.get("c5_opened") is not False:
        failures.append("c5_readout_wrong")
    for row in route_map:
        if row.get("current_resolution_state") != "UNRESOLVED":
            failures.append(f"route_not_unresolved:{row.get('route_map_record_id')}")
        if row.get("c5_reconsideration_ready") is not False:
            failures.append(f"route_c5_ready:{row.get('route_map_record_id')}")

    return failures, {
        "summary": summary,
        "question_skeletons": question_skeletons,
        "source_ref_skeletons": source_ref_skeletons,
        "undertyped_skeletons": undertyped_skeletons,
        "parking_skeletons": parking_skeletons,
        "route_map": route_map,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    summary = src.get("summary", {})
    question_skeletons = src.get("question_skeletons", [])
    source_ref_skeletons = src.get("source_ref_skeletons", [])
    undertyped_skeletons = src.get("undertyped_skeletons", [])
    parking_skeletons = src.get("parking_skeletons", [])
    route_map = src.get("route_map", [])

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    design_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_DESIGNED_BUILD_READY" if design_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_DESIGN_BASIS_FAIL"
    recommended_next = AUTHORIZED_BUILD_UNIT if design_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_DESIGN_BASIS_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_DESIGNED",
        "RT_POST_CLOSURE_DECISION_RECEIPT_CONSUMED",
        "REVIEWED_RESOLUTION_TARGET_REFERENCE_CONFIRMED",
        "EXECUTION_INPUT_SURFACES_CONFIRMED",
        "PROPOSED_QUESTION_ANSWER_CONTRACT_FROZEN",
        "PROPOSED_SOURCE_REF_SATISFACTION_CONTRACT_FROZEN",
        "PROPOSED_UNDER_TYPED_ACCEPTANCE_REVIEW_CONTRACT_FROZEN",
        "PARKING_EXECUTION_CONTINUATION_CONTRACT_FROZEN",
        "PROPOSED_WEAK_FEEDBACK_RESOLUTION_RECORD_CONTRACT_FROZEN",
        "EXECUTION_GATE_CONTRACT_FROZEN",
        "PROPOSAL_REVIEW_BOUNDARY_FROZEN",
        "C5_BLOCK_CONTRACT_FROZEN",
        "BUILD_EXECUTION_TARGET_AUTHORIZED_NEXT",
        "NO_RESOLUTION_EXECUTION_ATTEMPTED",
        "NO_RESOLUTION_RECORDS_EMITTED",
        "NO_QUESTION_PACKET_ANSWERED",
        "NO_SOURCE_REF_REQUEST_SATISFIED",
        "NO_UNDER_TYPED_ACCEPTANCE_APPROVED",
        "NO_PARKING_COUNTED_AS_RESOLUTION",
        "NO_C5_RECONSIDERATION_READY",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if design_pass else failures

    target_definition = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_definition_v0",
        "target_status": "DESIGNED_BUILD_READY" if design_pass else "NOT_READY",
        "source_rt_post_closure_decision_receipt_id": RT_DECISION_RECEIPT_ID,
        "target_unit_to_build_next": AUTHORIZED_BUILD_UNIT if design_pass else None,
        "target_unit_id_to_build": "observation.o2_weak_feedback_resolution_execution_target_build.v0",
        "target_mode_for_build": "STATIC_RESOLUTION_EXECUTION_TARGET_BUILD_ONLY",
        "active_object": "closed reviewed resolution-target reference with unresolved route map and zero resolution records",
        "goal": "Define a bounded future execution target that can later produce proposed resolution records from reviewed skeleton and route-map surfaces.",
        "design_does_not_execute": True,
        "proposed_records_do_not_equal_reviewed_resolution": True,
        "c5_unblock_requires_later_reviewed_resolution_closure": True,
        "not_goal": [
            "emit proposed records now",
            "emit reviewed resolution records now",
            "answer question packets now",
            "satisfy source-ref requests now",
            "approve under-typed acceptance now",
            "count parking as resolution",
            "run live audit now",
            "repair",
            "retry",
            "patch runtime",
            "mutate sources",
            "open C5",
        ],
    }

    input_inventory = {
        "schema_version": "o2_weak_feedback_resolution_execution_input_surface_inventory_v0",
        "inventory_status": "INPUT_SURFACES_AVAILABLE_FOR_EXECUTION_TARGET_BUILD",
        "question_answer_skeletons_available_count": len(question_skeletons),
        "source_ref_satisfaction_skeletons_available_count": len(source_ref_skeletons),
        "under_typed_acceptance_review_skeletons_available_count": len(undertyped_skeletons),
        "parking_continuation_skeletons_available_count": len(parking_skeletons),
        "route_map_records_available_count": len(route_map),
        "resolution_records_emitted_count": 0,
        "source_refs": {
            "question_answer_skeletons": rel(RT_QUESTION_SKELETONS_PATH),
            "source_ref_satisfaction_skeletons": rel(RT_SOURCE_REF_SKELETONS_PATH),
            "under_typed_acceptance_review_skeletons": rel(RT_UNDERTYPED_SKELETONS_PATH),
            "parking_continuation_skeletons": rel(RT_PARKING_SKELETONS_PATH),
            "route_map": rel(RT_ROUTE_MAP_PATH),
        },
    }

    proposed_question_contract = {
        "schema_version": "o2_proposed_question_answer_execution_contract_v0",
        "contract_status": "PROPOSED_QUESTION_ANSWER_CONTRACT_FROZEN",
        "eligible_skeleton_count": len(question_skeletons),
        "proposed_record_schema": {
            "schema_version": "o2_proposed_question_answer_record_v0",
            "proposed_answer_id": "proposed_question_answer_<sig8>",
            "source_answer_skeleton_ref": None,
            "source_question_packet_ref": None,
            "answer_payload_or_ref": None,
            "evidence_refs": [],
            "proposal_status": "PROPOSED | BLOCKED_MISSING_SOURCE | OUT_OF_SCOPE",
            "review_status": "UNREVIEWED",
            "counts_as_answer": False,
            "counts_as_resolution_input": False,
        },
        "design_unit_emits_proposed_answers": False,
        "proposed_answer_counts_as_answer_without_review": False,
    }

    proposed_source_ref_contract = {
        "schema_version": "o2_proposed_source_ref_satisfaction_execution_contract_v0",
        "contract_status": "PROPOSED_SOURCE_REF_SATISFACTION_CONTRACT_FROZEN",
        "eligible_skeleton_count": len(source_ref_skeletons),
        "proposed_record_schema": {
            "schema_version": "o2_proposed_source_ref_satisfaction_record_v0",
            "proposed_satisfaction_id": "proposed_source_ref_satisfaction_<sig8>",
            "source_satisfaction_skeleton_ref": None,
            "source_ref_request_ref": None,
            "proposed_source_refs": [],
            "proposal_status": "PROPOSED | BLOCKED_SOURCE_MISSING | OUT_OF_SCOPE",
            "review_status": "UNREVIEWED",
            "counts_as_satisfied": False,
            "counts_as_resolution_input": False,
        },
        "design_unit_emits_proposed_source_refs": False,
        "proposed_source_ref_counts_as_satisfied_without_review": False,
    }

    proposed_undertyped_contract = {
        "schema_version": "o2_proposed_under_typed_acceptance_review_execution_contract_v0",
        "contract_status": "PROPOSED_UNDER_TYPED_ACCEPTANCE_REVIEW_CONTRACT_FROZEN",
        "eligible_skeleton_count": len(undertyped_skeletons),
        "proposed_record_schema": {
            "schema_version": "o2_proposed_under_typed_acceptance_review_record_v0",
            "proposed_review_id": "proposed_under_typed_review_<sig8>",
            "source_review_skeleton_ref": None,
            "proposed_decision": "APPROVE_BOUNDED | REJECT | KEEP_CANDIDATE_ONLY | BLOCKED_NEEDS_DISCRIMINATOR",
            "proposal_status": "PROPOSED",
            "review_status": "UNREVIEWED",
            "counts_as_approved": False,
            "c5_unblock_allowed": False,
        },
        "design_unit_emits_proposed_under_typed_reviews": False,
        "proposed_review_counts_as_approval_without_review": False,
    }

    parking_contract = {
        "schema_version": "o2_parking_execution_continuation_contract_v0",
        "contract_status": "PARKING_EXECUTION_CONTINUATION_CONTRACT_FROZEN",
        "eligible_skeleton_count": len(parking_skeletons),
        "proposed_record_schema": {
            "schema_version": "o2_parking_execution_continuation_record_v0",
            "parking_execution_id": "parking_execution_<sig8>",
            "source_parking_skeleton_ref": None,
            "continue_parking": True,
            "proposal_status": "PARKED_UNRESOLVED",
            "review_status": "UNREVIEWED",
            "counts_as_resolution": False,
            "c5_unblock_allowed": False,
        },
        "design_unit_counts_parking_as_resolution": False,
    }

    proposed_resolution_contract = {
        "schema_version": "o2_proposed_weak_feedback_resolution_record_contract_v0",
        "contract_status": "PROPOSED_WEAK_FEEDBACK_RESOLUTION_RECORD_CONTRACT_FROZEN",
        "eligible_route_map_record_count": len(route_map),
        "proposed_resolution_record_schema": {
            "schema_version": "o2_proposed_weak_feedback_resolution_record_v0",
            "proposed_resolution_id": "proposed_weak_feedback_resolution_<sig8>",
            "source_route_map_ref": None,
            "proposed_question_answer_refs": [],
            "proposed_source_ref_satisfaction_refs": [],
            "proposed_under_typed_review_refs": [],
            "parking_continuation_refs": [],
            "proposed_resolution_decision": "PROPOSE_RESOLVED | REMAINS_UNRESOLVED | PARKED_UNRESOLVED | BLOCKED_MISSING_SOURCE",
            "proposal_status": "PROPOSED | BLOCKED",
            "review_status": "UNREVIEWED",
            "counts_as_reviewed_resolution": False,
            "c5_reconsideration_ready": False,
        },
        "design_unit_emits_proposed_resolution_records": False,
        "proposed_resolution_counts_as_resolved_without_review": False,
    }

    execution_gate_contract = {
        "schema_version": "o2_weak_feedback_resolution_execution_gate_contract_v0",
        "contract_status": "EXECUTION_GATE_CONTRACT_FROZEN",
        "future_execution_unit_may_emit": [
            "proposed question-answer records",
            "proposed source-ref satisfaction records",
            "proposed under-typed acceptance review records",
            "parking continuation records",
            "proposed weak-feedback resolution records",
        ],
        "future_execution_unit_may_not_emit": [
            "reviewed resolution records",
            "C5 unblock records",
            "runtime patches",
            "source mutations",
        ],
        "execution_pass_requires": [
            "all emitted records are proposed or blocked, not reviewed",
            "all proposed resolution records remain review_status=UNREVIEWED",
            "weak_feedback_resolved remains false in execution target build/design layer",
            "c5_reconsideration_ready remains false",
            "c5_opened remains false",
        ],
        "design_unit_executes_gate": False,
    }

    proposal_review_boundary = {
        "schema_version": "o2_resolution_proposal_review_boundary_v0",
        "boundary_status": "PROPOSAL_REVIEW_BOUNDARY_FROZEN",
        "proposal_layer": "may create candidate/proposed records in a later explicitly authorized execution unit",
        "review_layer": "must separately review proposed records before any resolution can count",
        "closure_layer": "must close reviewed resolution before any C5 reconsideration can be selected",
        "design_unit_crosses_boundary": False,
    }

    c5_block_contract = {
        "schema_version": "o2_resolution_execution_c5_block_contract_v0",
        "contract_status": "C5_BLOCK_CONTRACT_FROZEN",
        "current_c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "current_c5_reconsideration_ready": False,
        "current_c5_opened": False,
        "c5_may_be_reconsidered_only_after": [
            "proposed resolution records are emitted by an authorized execution unit",
            "proposed resolution records are reviewed",
            "reviewed resolution is closed",
            "post-resolution decision explicitly selects C5 reconsideration",
        ],
        "design_unit_can_unblock_c5": False,
    }

    negative_controls = {
        "schema_version": "o2_weak_feedback_resolution_execution_negative_controls_v0",
        "negative_control_status": "NEGATIVE_CONTROLS_FROZEN",
        "negative_controls": [
            "design_emits_proposed_resolution_records_fail",
            "design_answers_question_packet_fail",
            "design_satisfies_source_ref_fail",
            "design_approves_under_typed_acceptance_fail",
            "design_counts_parking_as_resolution_fail",
            "design_marks_weak_feedback_resolved_fail",
            "design_sets_c5_reconsideration_ready_fail",
            "design_opens_c5_fail",
            "design_runs_live_audit_fail",
            "design_repairs_or_retries_fail",
            "design_patches_runtime_fail",
            "design_mutates_source_fail",
            "hidden_next_command_fail",
            "latest_or_mtime_selection_fail",
        ],
    }

    build_authorization = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_build_authorization_v0",
        "authorization_status": "BUILD_UNIT_AUTHORIZED_NEXT" if design_pass else "NOT_AUTHORIZED",
        "authorized_next_unit": AUTHORIZED_BUILD_UNIT if design_pass else None,
        "authorized_build_mode": "STATIC_RESOLUTION_EXECUTION_TARGET_BUILD_ONLY" if design_pass else None,
        "authorized_scope": [
            "materialize proposed-record schemas",
            "materialize execution input mapping",
            "materialize proposed resolution record templates",
            "materialize proposal/review boundary checks",
            "materialize C5-block enforcement readout",
            "preserve zero emitted records",
        ],
        "not_authorized": [
            "emit proposed records during design",
            "emit reviewed resolution records",
            "answer question packets",
            "satisfy source-ref requests",
            "approve under-typed acceptance",
            "count parking as resolution",
            "run live audit",
            "repair",
            "retry",
            "patch runtime",
            "mutate sources",
            "open C5",
        ],
    }

    unresolved_continuation = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_unresolved_continuation_v0",
        "unresolved_status_continues": True,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    authority_boundary = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_authority_boundary_v0",
        "status": status,
        "may_build_o2_weak_feedback_resolution_execution_target_next": design_pass,
        "may_execute_resolution_now": False,
        "may_emit_proposed_resolution_records_now": False,
        "may_emit_reviewed_resolution_records_now": False,
        "may_resolve_weak_feedback_now": False,
        "may_answer_question_packets_now": False,
        "may_satisfy_source_ref_requests_now": False,
        "may_approve_under_typed_acceptance_now": False,
        "may_count_parking_as_resolution": False,
        "may_set_c5_reconsideration_ready": False,
        "may_open_c5": False,
        "may_run_live_feedback_audit_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_select_target_for_build": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
    }

    classification = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "resolution_execution_target_designed": design_pass,
        "build_authorized_next": design_pass,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "live_feedback_audit_executed": False,
        "repair_applied": False,
        "retry_executed": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "architecture_change": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "execution_target_design_count": 1 if design_pass else 0,
        "build_authorized_next_count": 1 if design_pass else 0,
        "question_answer_skeletons_available_count": len(question_skeletons),
        "source_ref_satisfaction_skeletons_available_count": len(source_ref_skeletons),
        "under_typed_acceptance_review_skeletons_available_count": len(undertyped_skeletons),
        "parking_continuation_skeletons_available_count": len(parking_skeletons),
        "route_map_records_available_count": len(route_map),
        "weak_feedback_resolved_count": 0,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "question_packets_answered_count": 0,
        "source_ref_requests_satisfied_count": 0,
        "under_typed_acceptance_approved_count": 0,
        "parked_records_counted_as_resolved_count": 0,
        "live_feedback_audit_executed_count": 0,
        "repair_applied_count": 0,
        "retry_executed_count": 0,
        "target_selected_for_build_count": 0,
        "runtime_patch_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "architecture_change_count": 0,
        "c5_opened_count": 0,
        "c5_reconsideration_ready_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "weak_feedback_resolved_count",
        "resolution_records_emitted_count",
        "proposed_resolution_records_emitted_count",
        "question_packets_answered_count",
        "source_ref_requests_satisfied_count",
        "under_typed_acceptance_approved_count",
        "parked_records_counted_as_resolved_count",
        "live_feedback_audit_executed_count",
        "repair_applied_count",
        "retry_executed_count",
        "target_selected_for_build_count",
        "runtime_patch_count",
        "source_mutated_count",
        "prior_receipt_mutated_count",
        "architecture_change_count",
        "c5_opened_count",
        "c5_reconsideration_ready_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_profile_v0",
        "profile_id": "o2_wf_resolution_execution_target_profile_" + sha8(rollup),
        "status": status,
        "resolution_execution_target_designed": design_pass,
        "authorized_next_unit": recommended_next,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Build the weak-feedback resolution execution target next; do not execute resolution yet.",
        "must_not_infer": [
            "weak feedback resolved",
            "proposed resolution records emitted",
            "reviewed resolution records emitted",
            "question packet answered",
            "source-ref request satisfied",
            "under-typed acceptance approved",
            "parking resolved weak feedback",
            "C5 reconsideration ready",
            "C5 opened",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The weak-feedback resolution execution target was designed. It defines proposed-record contracts, execution gates, proposal/review boundary, and C5-block contract for a future execution target build. It emits no proposed or reviewed resolution records and does not answer, satisfy, approve, resolve, run live audit, repair, retry, patch runtime, mutate sources, or open C5.",
        "authorized_next_unit": recommended_next,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_transition_trace_v0",
        "trace": [
            {
                "step": "consume_rt_post_closure_decision",
                "question": "is resolution execution target design authorized",
                "answer": "yes" if design_pass else "no",
                "taken": "design execution target",
            },
            {
                "step": "define_proposed_record_layer",
                "question": "can proposed records be designed without executing resolution",
                "answer": "yes",
                "taken": "freeze proposed-record contracts and proposal/review boundary",
            },
            {
                "step": "preserve_zero_resolution_state",
                "question": "did design emit resolution records or unblock C5",
                "answer": "no",
                "taken": "authorize static execution target build next",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (TARGET_DEFINITION_PATH, target_definition),
        (INPUT_SURFACE_INVENTORY_PATH, input_inventory),
        (PROPOSED_QUESTION_ANSWER_CONTRACT_PATH, proposed_question_contract),
        (PROPOSED_SOURCE_REF_CONTRACT_PATH, proposed_source_ref_contract),
        (PROPOSED_UNDERTYPED_REVIEW_CONTRACT_PATH, proposed_undertyped_contract),
        (PROPOSED_PARKING_CONTRACT_PATH, parking_contract),
        (PROPOSED_RESOLUTION_RECORD_CONTRACT_PATH, proposed_resolution_contract),
        (EXECUTION_GATE_CONTRACT_PATH, execution_gate_contract),
        (PROPOSAL_REVIEW_BOUNDARY_PATH, proposal_review_boundary),
        (C5_BLOCK_CONTRACT_PATH, c5_block_contract),
        (NEGATIVE_CONTROLS_PATH, negative_controls),
        (BUILD_AUTHORIZATION_PATH, build_authorization),
        (UNRESOLVED_CONTINUATION_PATH, unresolved_continuation),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, trace),
    ]
    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "EXEC_TARGET_DESIGN_0_RT_DECISION_RECEIPT_CONSUMED": RT_DECISION_RECEIPT_PATH.exists(),
        "EXEC_TARGET_DESIGN_1_TARGET_DEFINITION_EMITTED": TARGET_DEFINITION_PATH.exists(),
        "EXEC_TARGET_DESIGN_2_INPUT_SURFACE_INVENTORY_EMITTED": INPUT_SURFACE_INVENTORY_PATH.exists(),
        "EXEC_TARGET_DESIGN_3_PROPOSED_QUESTION_CONTRACT_EMITTED": PROPOSED_QUESTION_ANSWER_CONTRACT_PATH.exists(),
        "EXEC_TARGET_DESIGN_4_PROPOSED_SOURCE_REF_CONTRACT_EMITTED": PROPOSED_SOURCE_REF_CONTRACT_PATH.exists(),
        "EXEC_TARGET_DESIGN_5_PROPOSED_UNDERTYPED_CONTRACT_EMITTED": PROPOSED_UNDERTYPED_REVIEW_CONTRACT_PATH.exists(),
        "EXEC_TARGET_DESIGN_6_PARKING_CONTRACT_EMITTED": PROPOSED_PARKING_CONTRACT_PATH.exists(),
        "EXEC_TARGET_DESIGN_7_PROPOSED_RESOLUTION_RECORD_CONTRACT_EMITTED": PROPOSED_RESOLUTION_RECORD_CONTRACT_PATH.exists(),
        "EXEC_TARGET_DESIGN_8_EXECUTION_GATE_CONTRACT_EMITTED": EXECUTION_GATE_CONTRACT_PATH.exists(),
        "EXEC_TARGET_DESIGN_9_PROPOSAL_REVIEW_BOUNDARY_EMITTED": PROPOSAL_REVIEW_BOUNDARY_PATH.exists(),
        "EXEC_TARGET_DESIGN_10_C5_BLOCK_CONTRACT_EMITTED": C5_BLOCK_CONTRACT_PATH.exists(),
        "EXEC_TARGET_DESIGN_11_BUILD_AUTHORIZATION_EMITTED": build_authorization["authorized_next_unit"] == AUTHORIZED_BUILD_UNIT,
        "EXEC_TARGET_DESIGN_12_NO_RESOLUTION_RECORDS_EMITTED": rollup["resolution_records_emitted_count"] == 0 and rollup["proposed_resolution_records_emitted_count"] == 0,
        "EXEC_TARGET_DESIGN_13_NO_RESOLUTION_ANSWER_SATISFY_APPROVE": rollup["weak_feedback_resolved_count"] == 0 and rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "EXEC_TARGET_DESIGN_14_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "EXEC_TARGET_DESIGN_15_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "EXEC_TARGET_DESIGN_16_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "EXEC_TARGET_DESIGN_17_NO_C5_RECONSIDERATION_READY": rollup["c5_reconsideration_ready_count"] == 0,
        "EXEC_TARGET_DESIGN_18_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "EXEC_TARGET_DESIGN_19_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "EXEC_TARGET_DESIGN_20_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_DESIGN_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "next": recommended_next,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_design_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_DESIGN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_rt_post_closure_decision_receipt_id": RT_DECISION_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_resolution_execution_target_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "resolution_execution_target_designed": design_pass,
            "build_authorized_next": design_pass,
            "authorized_next_unit": recommended_next,
            "authorized_build_mode": "STATIC_RESOLUTION_EXECUTION_TARGET_BUILD_ONLY" if design_pass else None,
            "question_answer_skeletons_available_count": len(question_skeletons),
            "source_ref_satisfaction_skeletons_available_count": len(source_ref_skeletons),
            "under_typed_acceptance_review_skeletons_available_count": len(undertyped_skeletons),
            "parking_continuation_skeletons_available_count": len(parking_skeletons),
            "route_map_records_available_count": len(route_map),
            "proposed_question_answer_contract_frozen": design_pass,
            "proposed_source_ref_satisfaction_contract_frozen": design_pass,
            "proposed_under_typed_acceptance_review_contract_frozen": design_pass,
            "parking_execution_continuation_contract_frozen": design_pass,
            "proposed_resolution_record_contract_frozen": design_pass,
            "execution_gate_contract_frozen": design_pass,
            "proposal_review_boundary_frozen": design_pass,
            "c5_block_contract_frozen": design_pass,
            "weak_feedback_resolved": False,
            "resolution_records_emitted_count": 0,
            "proposed_resolution_records_emitted_count": 0,
            "question_packets_answered": False,
            "source_ref_requests_satisfied": False,
            "under_typed_acceptance_approved": False,
            "parking_counted_as_resolution": False,
            "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
            "c5_reconsideration_ready": False,
            "c5_opened": False,
            "live_feedback_audit_executed": False,
            "repair_applied": False,
            "retry_executed": False,
            "target_selected_for_build": False,
            "runtime_patch_applied": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "architecture_change": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": recommended_next,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "target_definition": rel(TARGET_DEFINITION_PATH),
            "input_surface_inventory": rel(INPUT_SURFACE_INVENTORY_PATH),
            "proposed_question_answer_contract": rel(PROPOSED_QUESTION_ANSWER_CONTRACT_PATH),
            "proposed_source_ref_satisfaction_contract": rel(PROPOSED_SOURCE_REF_CONTRACT_PATH),
            "proposed_under_typed_acceptance_review_contract": rel(PROPOSED_UNDERTYPED_REVIEW_CONTRACT_PATH),
            "parking_execution_continuation_contract": rel(PROPOSED_PARKING_CONTRACT_PATH),
            "proposed_resolution_record_contract": rel(PROPOSED_RESOLUTION_RECORD_CONTRACT_PATH),
            "execution_gate_contract": rel(EXECUTION_GATE_CONTRACT_PATH),
            "proposal_review_boundary": rel(PROPOSAL_REVIEW_BOUNDARY_PATH),
            "c5_block_contract": rel(C5_BLOCK_CONTRACT_PATH),
            "negative_controls": rel(NEGATIVE_CONTROLS_PATH),
            "build_authorization": rel(BUILD_AUTHORIZATION_PATH),
            "unresolved_continuation": rel(UNRESOLVED_CONTINUATION_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"weak_feedback_resolution_execution_target_receipt_id={receipt_id}")
    print(f"weak_feedback_resolution_execution_target_receipt_path={rel(receipt_path)}")
    print(f"weak_feedback_resolution_execution_target_definition_path={rel(TARGET_DEFINITION_PATH)}")
    print(f"weak_feedback_resolution_execution_input_surface_inventory_path={rel(INPUT_SURFACE_INVENTORY_PATH)}")
    print(f"proposed_question_answer_execution_contract_path={rel(PROPOSED_QUESTION_ANSWER_CONTRACT_PATH)}")
    print(f"proposed_source_ref_satisfaction_execution_contract_path={rel(PROPOSED_SOURCE_REF_CONTRACT_PATH)}")
    print(f"proposed_under_typed_acceptance_review_execution_contract_path={rel(PROPOSED_UNDERTYPED_REVIEW_CONTRACT_PATH)}")
    print(f"proposed_weak_feedback_resolution_record_contract_path={rel(PROPOSED_RESOLUTION_RECORD_CONTRACT_PATH)}")
    print(f"weak_feedback_resolution_execution_gate_contract_path={rel(EXECUTION_GATE_CONTRACT_PATH)}")
    print(f"weak_feedback_resolution_execution_target_rollup_path={rel(ROLLUP_PATH)}")
    print(f"weak_feedback_resolution_execution_target_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
