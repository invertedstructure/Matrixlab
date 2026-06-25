#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_target_post_closure_decision.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_TARGET_POST_CLOSURE_DECISION"
MODE = "DECIDE_ONLY / SELECT_NEXT_BRANCH / NO_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_TARGET_POST_CLOSURE_DECISION_ONLY"

RT_CLOSURE_RECEIPT_ID = "32419538"
RT_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0_receipts/32419538.json"
RT_CLOSURE_RECORD_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_closure_record_v0.json"
RT_REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_reviewed_reference_v0.json"
RT_SKELETON_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_skeleton_freeze_v0.json"
RT_ROUTE_MAP_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_route_map_freeze_v0.json"
RT_NONRESOLUTION_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_nonresolution_freeze_v0.json"
RT_C5_BLOCK_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_c5_block_freeze_v0.json"
RT_RECEIPT_CHAIN_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_receipt_chain_v0.json"
RT_BOUNDARY_LOCK_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_closure_boundary_lock_v0.json"
RT_CLOSURE_DECISION_TABLE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_closure_downstream_decision_table_v0.json"
RT_CLOSURE_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_closure_authority_boundary_v0.json"
RT_CLOSURE_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_closure_classification_v0.json"
RT_CLOSURE_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_closure_rollup_v0.json"
RT_CLOSURE_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_closure_profile_v0.json"
RT_CLOSURE_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_closure_report.json"
RT_CLOSURE_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_closure_transition_trace.json"

RT_BUILD_QA_SKELS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_question_packet_answer_record_skeletons_v0.jsonl"
RT_BUILD_SOURCE_REF_SKELS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_source_ref_satisfaction_record_skeletons_v0.jsonl"
RT_BUILD_UNDERTYPED_SKELS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_under_typed_acceptance_review_record_skeletons_v0.jsonl"
RT_BUILD_PARKING_SKELS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_parking_continuation_record_skeletons_v0.jsonl"
RT_BUILD_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_route_map_v0.jsonl"
RT_BUILD_GATE_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_gate_readout_v0.json"
RT_BUILD_C5_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_c5_reconsideration_readout_v0.json"

REQUIRED_SOURCE_FILES = [
    RT_CLOSURE_RECEIPT_PATH,
    RT_CLOSURE_RECORD_PATH,
    RT_REVIEWED_REFERENCE_PATH,
    RT_SKELETON_FREEZE_PATH,
    RT_ROUTE_MAP_FREEZE_PATH,
    RT_NONRESOLUTION_FREEZE_PATH,
    RT_C5_BLOCK_FREEZE_PATH,
    RT_RECEIPT_CHAIN_PATH,
    RT_BOUNDARY_LOCK_PATH,
    RT_CLOSURE_DECISION_TABLE_PATH,
    RT_CLOSURE_AUTHORITY_PATH,
    RT_CLOSURE_CLASSIFICATION_PATH,
    RT_CLOSURE_ROLLUP_PATH,
    RT_CLOSURE_PROFILE_PATH,
    RT_CLOSURE_REPORT_PATH,
    RT_CLOSURE_TRACE_PATH,
    RT_BUILD_QA_SKELS_PATH,
    RT_BUILD_SOURCE_REF_SKELS_PATH,
    RT_BUILD_UNDERTYPED_SKELS_PATH,
    RT_BUILD_PARKING_SKELS_PATH,
    RT_BUILD_ROUTE_MAP_PATH,
    RT_BUILD_GATE_READOUT_PATH,
    RT_BUILD_C5_READOUT_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "o2_rt_post_closure_decision_basis_v0.json"
DECISION_TABLE_PATH = OUT_DIR / "o2_rt_post_closure_decision_table_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "o2_rt_selected_next_branch_v0.json"
EXECUTION_TARGET_AUTH_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_authorization_v0.json"
UNRESOLVED_CONTINUATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_unresolved_continuation_v0.json"
C5_BLOCK_CONTINUATION_PATH = OUT_DIR / "o2_rt_c5_block_continuation_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "o2_rt_deferred_branches_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_rt_post_closure_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_rt_post_closure_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_rt_post_closure_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_rt_post_closure_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_rt_post_closure_decision_report.json"
TRACE_PATH = OUT_DIR / "o2_rt_post_closure_decision_transition_trace.json"

EXPECTED_CLOSURE_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED_DECISION_READY"
EXPECTED_CLOSURE_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED_DECISION_READY"
EXPECTED_CLOSURE_NEXT = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_REFERENCE_CLOSURE_V0"
SELECTED_BRANCH = "DESIGN_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET"
SELECTED_NEXT_UNIT = "DESIGN_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_V0"

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

    receipt = read_json(RT_CLOSURE_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_resolution_target_closure_summary", {})
    closure_record = read_json(RT_CLOSURE_RECORD_PATH)
    reviewed_reference = read_json(RT_REVIEWED_REFERENCE_PATH)
    skeleton_freeze = read_json(RT_SKELETON_FREEZE_PATH)
    route_freeze = read_json(RT_ROUTE_MAP_FREEZE_PATH)
    nonresolution_freeze = read_json(RT_NONRESOLUTION_FREEZE_PATH)
    c5_freeze = read_json(RT_C5_BLOCK_FREEZE_PATH)
    boundary_lock = read_json(RT_BOUNDARY_LOCK_PATH)
    closure_decision_table = read_json(RT_CLOSURE_DECISION_TABLE_PATH)
    closure_authority = read_json(RT_CLOSURE_AUTHORITY_PATH)
    closure_classification = read_json(RT_CLOSURE_CLASSIFICATION_PATH)
    closure_rollup = read_json(RT_CLOSURE_ROLLUP_PATH)
    closure_profile = read_json(RT_CLOSURE_PROFILE_PATH)
    closure_report = read_json(RT_CLOSURE_REPORT_PATH)
    closure_trace = read_json(RT_CLOSURE_TRACE_PATH)

    question_skeletons = read_jsonl(RT_BUILD_QA_SKELS_PATH)
    source_ref_skeletons = read_jsonl(RT_BUILD_SOURCE_REF_SKELS_PATH)
    undertyped_skeletons = read_jsonl(RT_BUILD_UNDERTYPED_SKELS_PATH)
    parking_skeletons = read_jsonl(RT_BUILD_PARKING_SKELS_PATH)
    route_map = read_jsonl(RT_BUILD_ROUTE_MAP_PATH)
    gate_readout = read_json(RT_BUILD_GATE_READOUT_PATH)
    c5_readout = read_json(RT_BUILD_C5_READOUT_PATH)

    if receipt.get("receipt_id") != RT_CLOSURE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("resolution_target_closure_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_CLOSURE_STOP:
        failures.append("resolution_target_closure_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("resolution_target_closure_hidden_next_command")
    if summary.get("status") != EXPECTED_CLOSURE_STATUS:
        failures.append(f"resolution_target_closure_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_CLOSURE_NEXT:
        failures.append(f"resolution_target_closure_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "resolution_target_closed_as_reviewed_reference",
        "reviewed_reference_emitted",
        "post_closure_decision_ready",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "question_answer_skeletons_frozen_count": 3,
        "source_ref_satisfaction_skeletons_frozen_count": 2,
        "under_typed_acceptance_review_skeletons_frozen_count": 2,
        "parking_continuation_skeletons_frozen_count": 3,
        "route_map_records_frozen_count": 3,
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
    if closure_record.get("closure_status") != "CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED":
        failures.append("closure_record_wrong")
    if reviewed_reference.get("weak_feedback_resolved") is not False or reviewed_reference.get("resolution_records_emitted_count") != 0:
        failures.append("reviewed_reference_wrong")
    if skeleton_freeze.get("question_answer_skeletons_frozen_count") != 3:
        failures.append("skeleton_freeze_question_count_wrong")
    if route_freeze.get("all_route_map_records_unresolved") is not True or route_freeze.get("resolution_records_emitted_count") != 0:
        failures.append("route_freeze_wrong")
    if nonresolution_freeze.get("weak_feedback_resolved") is not False or nonresolution_freeze.get("resolution_records_emitted_count") != 0:
        failures.append("nonresolution_freeze_wrong")
    if c5_freeze.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_freeze.get("c5_reconsideration_ready") is not False or c5_freeze.get("c5_opened") is not False:
        failures.append("c5_freeze_wrong")
    if boundary_lock.get("weak_feedback_resolved") is not False or boundary_lock.get("c5_opened") is not False:
        failures.append("boundary_lock_wrong")
    if closure_authority.get("may_decide_next_after_resolution_target_reference_closure") is not True:
        failures.append("closure_authority_no_decide")
    if closure_authority.get("may_open_c5") is not False:
        failures.append("closure_authority_allows_c5")
    if closure_classification.get("recommended_next") != EXPECTED_CLOSURE_NEXT:
        failures.append("classification_next_wrong")
    if closure_rollup.get("post_closure_decision_ready_count") != 1:
        failures.append("closure_rollup_decision_ready_wrong")
    if closure_profile.get("post_closure_decision_ready") is not True or closure_profile.get("next_command_goal") is not None:
        failures.append("closure_profile_wrong")
    if closure_report.get("recommended_next_handling") != EXPECTED_CLOSURE_NEXT:
        failures.append("closure_report_next_wrong")
    if closure_trace.get("terminal", {}).get("stop_code") != EXPECTED_CLOSURE_STOP:
        failures.append("closure_trace_stop_wrong")

    if len(question_skeletons) != 3 or len(source_ref_skeletons) != 2 or len(undertyped_skeletons) != 2 or len(parking_skeletons) != 3 or len(route_map) != 3:
        failures.append("build_surface_counts_wrong")
    for row in route_map:
        if row.get("current_resolution_state") != "UNRESOLVED":
            failures.append(f"route_not_unresolved:{row.get('route_map_record_id')}")
        if row.get("c5_reconsideration_ready") is not False:
            failures.append(f"route_c5_ready:{row.get('route_map_record_id')}")
    if gate_readout.get("weak_feedback_resolved") is not False or gate_readout.get("resolution_records_emitted_count") != 0:
        failures.append("gate_readout_wrong")
    if c5_readout.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_readout.get("c5_opened") is not False:
        failures.append("c5_readout_wrong")

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

    decision_pass = not failures
    status = "TYPED_O2_RT_POST_CLOSURE_DECISION_SELECTED_RESOLUTION_EXECUTION_TARGET_DESIGN_READY" if decision_pass else "TYPED_O2_RT_POST_CLOSURE_DECISION_BASIS_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_O2_RT_POST_CLOSURE_DECISION_BASIS_V0"

    reason_codes = [
        "RT_POST_CLOSURE_DECISION_EMITTED",
        "RESOLUTION_TARGET_CLOSURE_RECEIPT_CONSUMED",
        "REVIEWED_RESOLUTION_TARGET_REFERENCE_CONFIRMED",
        "ZERO_RESOLUTION_RECORDS_CONFIRMED",
        "UNRESOLVED_ROUTE_MAP_CONFIRMED",
        "SKELETON_SURFACES_CONFIRMED",
        "C5_BLOCK_CONFIRMED",
        "RESOLUTION_EXECUTION_TARGET_DESIGN_SELECTED_NEXT",
        "NO_WEAK_FEEDBACK_RESOLUTION_ATTEMPTED",
        "NO_QUESTION_PACKET_ANSWERED",
        "NO_SOURCE_REF_REQUEST_SATISFIED",
        "NO_UNDER_TYPED_ACCEPTANCE_APPROVED",
        "NO_PARKING_COUNTED_AS_RESOLUTION",
        "NO_C5_RECONSIDERATION_READY",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_TARGET_SELECTED_FOR_BUILD",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if decision_pass else failures

    decision_basis = {
        "schema_version": "o2_rt_post_closure_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_resolution_target_closure_receipt_id": RT_CLOSURE_RECEIPT_ID,
        "resolution_target_closed_as_reviewed_reference": summary.get("resolution_target_closed_as_reviewed_reference"),
        "reviewed_reference_emitted": summary.get("reviewed_reference_emitted"),
        "question_answer_skeletons_available_count": len(question_skeletons),
        "source_ref_satisfaction_skeletons_available_count": len(source_ref_skeletons),
        "under_typed_acceptance_review_skeletons_available_count": len(undertyped_skeletons),
        "parking_continuation_skeletons_available_count": len(parking_skeletons),
        "route_map_records_available_count": len(route_map),
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    decision_table = {
        "schema_version": "o2_rt_post_closure_decision_table_v0",
        "decision_status": "NEXT_BRANCH_SELECTED" if decision_pass else "NO_BRANCH_SELECTED",
        "records": [
            {
                "branch": SELECTED_BRANCH,
                "selected": decision_pass,
                "next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
                "why": "The resolution-target reference is closed; the next lawful edge is to design the bounded execution target that can later emit proposed resolution records without executing resolution in this decision unit.",
            },
            {
                "branch": "EXECUTE_RESOLUTION_NOW",
                "selected": False,
                "next_unit": None,
                "why": "This decision unit only selects the next branch. It may not answer, satisfy, approve, resolve, or emit resolution records.",
            },
            {
                "branch": "RUN_LIVE_FEEDBACK_AUDIT_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Live audit may become a subtarget only if the execution-target design requires source traces.",
            },
            {
                "branch": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 remains blocked because zero resolution records exist and C5 reconsideration is false.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "o2_rt_selected_next_branch_v0",
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "selection_scope": "target design only",
        "selection_reason": "Reviewed resolution-target reference exists, but no resolution records exist. Execution-target design is needed before any proposed resolution execution.",
        "selected_branch_does_not": [
            "emit resolution records now",
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

    execution_target_auth = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_authorization_v0",
        "authorization_status": "TARGET_DESIGN_AUTHORIZED" if decision_pass else "NOT_AUTHORIZED",
        "authorized_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "authorized_design_mode": "DESIGN_ONLY / WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET / NO_EXECUTION_NO_C5" if decision_pass else None,
        "target_goal": "Design a bounded execution target that will later turn reviewed skeletons and route maps into proposed resolution records under explicit review gates.",
        "target_should_define": [
            "which skeleton surfaces are eligible for proposed resolution execution",
            "how proposed question-answer records may be produced or remain missing",
            "how proposed source-ref satisfaction records may be produced or remain missing",
            "how proposed under-typed review records may be produced or remain candidate-only",
            "how parking continuation remains explicit unresolved status unless reviewed otherwise",
            "how proposed weak-feedback resolution records are formed",
            "what prevents proposed records from becoming reviewed resolution",
            "what prevents C5 reconsideration until reviewed closure",
        ],
        "target_may_not": [
            "execute resolution during design",
            "answer question packets during design",
            "satisfy source-ref requests during design",
            "approve under-typed acceptance during design",
            "emit reviewed resolution records during design",
            "run live audit",
            "repair",
            "retry",
            "patch runtime",
            "mutate sources",
            "open C5",
        ],
    }

    unresolved_continuation = {
        "schema_version": "o2_weak_feedback_resolution_target_unresolved_continuation_v0",
        "unresolved_status_continues": True,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "why": "Decision selected an execution-target design branch only.",
    }

    c5_block_continuation = {
        "schema_version": "o2_rt_c5_block_continuation_v0",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "block_continues": True,
        "block_reason": "No reviewed resolution records exist and this unit does not execute resolution.",
    }

    deferred_branches = {
        "schema_version": "o2_rt_deferred_branches_v0",
        "deferred": [
            "EXECUTE_RESOLUTION",
            "ANSWER_QUESTION_PACKETS",
            "SATISFY_SOURCE_REF_REQUESTS",
            "APPROVE_UNDER_TYPED_ACCEPTANCE",
            "COUNT_PARKING_AS_RESOLUTION",
            "LIVE_FEEDBACK_AUDIT",
            "REPAIR",
            "RETRY",
            "RUNTIME_PATCH",
            "C5",
        ],
        "why": "This unit only selects the next design target.",
    }

    authority_boundary = {
        "schema_version": "o2_rt_post_closure_decision_authority_boundary_v0",
        "status": status,
        "may_design_o2_weak_feedback_resolution_execution_target_next": decision_pass,
        "may_execute_resolution_now": False,
        "may_emit_resolution_records_now": False,
        "may_resolve_weak_feedback_now": False,
        "may_answer_question_packets_now": False,
        "may_satisfy_source_ref_requests_now": False,
        "may_approve_under_typed_acceptance_now": False,
        "may_count_parking_as_resolution": False,
        "may_run_live_feedback_audit_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_select_target_for_build": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_open_c5": False,
    }

    classification = {
        "schema_version": "o2_rt_post_closure_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_closure_decision_complete": decision_pass,
        "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": recommended_next,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
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
        "schema_version": "o2_rt_post_closure_decision_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "decision_count": 1 if decision_pass else 0,
        "selected_execution_target_design_count": 1 if decision_pass else 0,
        "question_answer_skeletons_available_count": len(question_skeletons),
        "source_ref_satisfaction_skeletons_available_count": len(source_ref_skeletons),
        "under_typed_acceptance_review_skeletons_available_count": len(undertyped_skeletons),
        "parking_continuation_skeletons_available_count": len(parking_skeletons),
        "route_map_records_available_count": len(route_map),
        "c5_block_continuation_count": 1 if decision_pass else 0,
        "weak_feedback_resolved_count": 0,
        "resolution_records_emitted_count": 0,
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
        "schema_version": "o2_rt_post_closure_decision_profile_v0",
        "profile_id": "o2_rt_post_closure_decision_profile_" + sha8(rollup),
        "status": status,
        "selected_next_unit": recommended_next,
        "decision": "design weak-feedback resolution execution target next",
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Design the weak-feedback resolution execution target next. Continue preserving zero-resolution state and C5 block.",
        "must_not_infer": [
            "weak feedback resolved",
            "resolution records emitted",
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
        "schema_version": "o2_rt_post_closure_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The post-closure decision selected weak-feedback resolution execution target design as the next branch. This is a design authorization only. It does not emit resolution records, answer question packets, satisfy source-ref requests, approve under-typed acceptance, count parking as resolution, run live audit, repair, retry, patch runtime, mutate sources, or open C5.",
        "selected_next_unit": recommended_next,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_rt_post_closure_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_resolution_target_closure",
                "question": "is resolution target closed as reviewed reference",
                "answer": "yes" if decision_pass else "no",
                "taken": "evaluate next branch table",
            },
            {
                "step": "inspect_zero_resolution_state",
                "question": "what remains after closure",
                "answer": "reviewed skeletons and route maps exist, but zero resolution records exist",
                "taken": "preserve unresolved status",
            },
            {
                "step": "select_next_branch",
                "question": "what next branch is lawful",
                "answer": SELECTED_NEXT_UNIT if decision_pass else recommended_next,
                "taken": "authorize resolution execution target design next",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (DECISION_BASIS_PATH, decision_basis),
        (DECISION_TABLE_PATH, decision_table),
        (SELECTED_BRANCH_PATH, selected_branch),
        (EXECUTION_TARGET_AUTH_PATH, execution_target_auth),
        (UNRESOLVED_CONTINUATION_PATH, unresolved_continuation),
        (C5_BLOCK_CONTINUATION_PATH, c5_block_continuation),
        (DEFERRED_BRANCHES_PATH, deferred_branches),
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
        "RT_DECIDE_0_CLOSURE_RECEIPT_CONSUMED": RT_CLOSURE_RECEIPT_PATH.exists(),
        "RT_DECIDE_1_DECISION_BASIS_EMITTED": DECISION_BASIS_PATH.exists(),
        "RT_DECIDE_2_DECISION_TABLE_EMITTED": DECISION_TABLE_PATH.exists(),
        "RT_DECIDE_3_REVIEWED_REFERENCE_CONFIRMED": summary.get("resolution_target_closed_as_reviewed_reference") is True,
        "RT_DECIDE_4_ZERO_RESOLUTION_RECORDS_CONFIRMED": summary.get("resolution_records_emitted_count") == 0,
        "RT_DECIDE_5_ROUTE_MAP_SURFACE_CONFIRMED": len(route_map) == 3,
        "RT_DECIDE_6_SKELETON_SURFACES_CONFIRMED": len(question_skeletons) == 3 and len(source_ref_skeletons) == 2 and len(undertyped_skeletons) == 2 and len(parking_skeletons) == 3,
        "RT_DECIDE_7_C5_BLOCK_CONFIRMED": summary.get("c5_feedback_readiness") == "BLOCKED_BY_WEAK_FEEDBACK" and summary.get("c5_reconsideration_ready") is False,
        "RT_DECIDE_8_EXECUTION_TARGET_DESIGN_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "RT_DECIDE_9_EXECUTION_TARGET_AUTHORIZATION_EMITTED": execution_target_auth["authorized_next_unit"] == SELECTED_NEXT_UNIT,
        "RT_DECIDE_10_NO_RESOLUTION_RECORDS_EMITTED": rollup["resolution_records_emitted_count"] == 0,
        "RT_DECIDE_11_NO_RESOLUTION_ANSWER_SATISFY_APPROVE": rollup["weak_feedback_resolved_count"] == 0 and rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "RT_DECIDE_12_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "RT_DECIDE_13_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "RT_DECIDE_14_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "RT_DECIDE_15_NO_C5_RECONSIDERATION_READY": rollup["c5_reconsideration_ready_count"] == 0,
        "RT_DECIDE_16_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "RT_DECIDE_17_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "RT_DECIDE_18_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_RT_POST_CLOSURE_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "selected": recommended_next,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_rt_post_closure_decision_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_POST_CLOSURE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_resolution_target_closure_receipt_id": RT_CLOSURE_RECEIPT_ID,
        "machine_readable_o2_rt_post_closure_decision_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_closure_decision_complete": decision_pass,
            "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
            "selected_next_unit": recommended_next,
            "resolution_target_reference_closed": summary.get("resolution_target_closed_as_reviewed_reference"),
            "question_answer_skeletons_available_count": len(question_skeletons),
            "source_ref_satisfaction_skeletons_available_count": len(source_ref_skeletons),
            "under_typed_acceptance_review_skeletons_available_count": len(undertyped_skeletons),
            "parking_continuation_skeletons_available_count": len(parking_skeletons),
            "route_map_records_available_count": len(route_map),
            "weak_feedback_resolved": False,
            "resolution_records_emitted_count": 0,
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
            "decision_basis": rel(DECISION_BASIS_PATH),
            "decision_table": rel(DECISION_TABLE_PATH),
            "selected_branch": rel(SELECTED_BRANCH_PATH),
            "execution_target_authorization": rel(EXECUTION_TARGET_AUTH_PATH),
            "unresolved_continuation": rel(UNRESOLVED_CONTINUATION_PATH),
            "c5_block_continuation": rel(C5_BLOCK_CONTINUATION_PATH),
            "deferred_branches": rel(DEFERRED_BRANCHES_PATH),
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
    print(f"rt_post_closure_decision_receipt_id={receipt_id}")
    print(f"rt_post_closure_decision_receipt_path={rel(receipt_path)}")
    print(f"rt_post_closure_decision_basis_path={rel(DECISION_BASIS_PATH)}")
    print(f"rt_post_closure_decision_table_path={rel(DECISION_TABLE_PATH)}")
    print(f"rt_selected_next_branch_path={rel(SELECTED_BRANCH_PATH)}")
    print(f"weak_feedback_resolution_execution_target_authorization_path={rel(EXECUTION_TARGET_AUTH_PATH)}")
    print(f"rt_unresolved_continuation_path={rel(UNRESOLVED_CONTINUATION_PATH)}")
    print(f"rt_c5_block_continuation_path={rel(C5_BLOCK_CONTINUATION_PATH)}")
    print(f"rt_post_closure_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"rt_post_closure_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
