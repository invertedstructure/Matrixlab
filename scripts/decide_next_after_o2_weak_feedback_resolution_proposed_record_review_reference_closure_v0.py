#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_proposed_record_review_post_closure_decision.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_POST_CLOSURE_DECISION"
MODE = "DECIDE_ONLY / SELECT_FINAL_RESOLUTION_CLOSURE / NO_FINAL_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_POST_CLOSURE_DECISION_ONLY"

SOURCE_CLOSURE_RECEIPT_ID = "2f793867"

SOURCE_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0_receipts/2f793867.json"
CLOSURE_RECORD_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_reviewed_reference_v0.json"
REVIEWED_ARTIFACT_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_reviewed_artifact_inventory_freeze_v0.json"
REVIEWED_RESOLUTION_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_reviewed_weak_feedback_resolution_record_freeze_v0.json"
REVIEWED_ROUTE_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_reviewed_route_map_freeze_v0.json"
FINAL_BOUNDARY_LOCK_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_final_resolution_boundary_lock_v0.json"
UNRESOLVED_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_unresolved_status_freeze_v0.json"
C5_BLOCK_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_c5_block_freeze_v0.json"
RECEIPT_CHAIN_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_receipt_chain_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_closure_downstream_decision_table_v0.json"
CLOSURE_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_closure_authority_boundary_v0.json"
CLOSURE_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_closure_classification_v0.json"
CLOSURE_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_closure_rollup_v0.json"
CLOSURE_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_closure_profile_v0.json"
CLOSURE_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_closure_report.json"
CLOSURE_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_closure_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_CLOSURE_RECEIPT_PATH,
    CLOSURE_RECORD_PATH,
    REVIEWED_REFERENCE_PATH,
    REVIEWED_ARTIFACT_FREEZE_PATH,
    REVIEWED_RESOLUTION_FREEZE_PATH,
    REVIEWED_ROUTE_FREEZE_PATH,
    FINAL_BOUNDARY_LOCK_PATH,
    UNRESOLVED_FREEZE_PATH,
    C5_BLOCK_FREEZE_PATH,
    RECEIPT_CHAIN_PATH,
    DOWNSTREAM_DECISION_TABLE_PATH,
    CLOSURE_AUTHORITY_PATH,
    CLOSURE_CLASSIFICATION_PATH,
    CLOSURE_ROLLUP_PATH,
    CLOSURE_PROFILE_PATH,
    CLOSURE_REPORT_PATH,
    CLOSURE_TRACE_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "o2_post_review_reference_closure_decision_basis_v0.json"
DECISION_TABLE_PATH = OUT_DIR / "o2_post_review_reference_closure_decision_table_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "o2_final_resolution_closure_selected_branch_v0.json"
FINAL_CLOSURE_AUTHORIZATION_PATH = OUT_DIR / "o2_final_resolution_closure_authorization_v0.json"
FINAL_CLOSURE_INPUT_SCOPE_PATH = OUT_DIR / "o2_final_resolution_closure_input_scope_v0.json"
UNRESOLVED_CONTINUATION_PATH = OUT_DIR / "o2_post_review_reference_closure_unresolved_continuation_v0.json"
C5_BLOCK_CONTINUATION_PATH = OUT_DIR / "o2_post_review_reference_closure_c5_block_continuation_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "o2_post_review_reference_closure_deferred_branches_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_post_review_reference_closure_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_post_review_reference_closure_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_post_review_reference_closure_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_post_review_reference_closure_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_post_review_reference_closure_decision_report.json"
TRACE_PATH = OUT_DIR / "o2_post_review_reference_closure_decision_transition_trace.json"

EXPECTED_CLOSURE_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSED_AS_REVIEWED_REFERENCE_FINAL_RESOLUTION_DECISION_READY"
EXPECTED_CLOSURE_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSED_AS_REVIEWED_REFERENCE_FINAL_RESOLUTION_DECISION_READY"
EXPECTED_CLOSURE_NEXT = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REFERENCE_CLOSURE_V0"

SELECTED_BRANCH = "EXECUTE_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE"
SELECTED_NEXT_UNIT = "EXECUTE_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_V0"

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

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    receipt = read_json(SOURCE_CLOSURE_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_resolution_proposed_record_review_closure_summary", {})
    closure_record = read_json(CLOSURE_RECORD_PATH)
    reviewed_reference = read_json(REVIEWED_REFERENCE_PATH)
    artifact_freeze = read_json(REVIEWED_ARTIFACT_FREEZE_PATH)
    resolution_freeze = read_json(REVIEWED_RESOLUTION_FREEZE_PATH)
    route_freeze = read_json(REVIEWED_ROUTE_FREEZE_PATH)
    boundary_lock = read_json(FINAL_BOUNDARY_LOCK_PATH)
    unresolved_freeze = read_json(UNRESOLVED_FREEZE_PATH)
    c5_freeze = read_json(C5_BLOCK_FREEZE_PATH)
    receipt_chain = read_json(RECEIPT_CHAIN_PATH)
    downstream_table = read_json(DOWNSTREAM_DECISION_TABLE_PATH)
    closure_authority = read_json(CLOSURE_AUTHORITY_PATH)
    closure_classification = read_json(CLOSURE_CLASSIFICATION_PATH)
    closure_rollup = read_json(CLOSURE_ROLLUP_PATH)
    closure_profile = read_json(CLOSURE_PROFILE_PATH)
    closure_report = read_json(CLOSURE_REPORT_PATH)
    closure_trace = read_json(CLOSURE_TRACE_PATH)

    if receipt.get("receipt_id") != SOURCE_CLOSURE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_closure_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_CLOSURE_STOP:
        failures.append("source_closure_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_closure_hidden_next_command")
    if summary.get("status") != EXPECTED_CLOSURE_STATUS:
        failures.append(f"source_closure_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_CLOSURE_NEXT:
        failures.append(f"source_closure_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "proposed_record_review_closed_as_reviewed_reference",
        "reviewed_reference_emitted",
        "post_closure_decision_ready",
        "reviewed_artifacts_frozen",
        "reviewed_resolution_records_exist",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "reviewed_question_answer_records_frozen_count": 3,
        "reviewed_source_ref_satisfaction_records_frozen_count": 2,
        "reviewed_under_typed_acceptance_records_frozen_count": 2,
        "reviewed_parking_continuation_records_frozen_count": 3,
        "reviewed_resolution_records_frozen_count": 3,
        "reviewed_route_records_frozen_count": 3,
        "resolution_records_emitted_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    for key in [
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
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

    if closure_record.get("closure_status") != "CLOSED_AS_REVIEWED_REFERENCE_REVIEWED_ARTIFACTS_NOT_FINAL":
        failures.append("closure_record_status_wrong")
    if reviewed_reference.get("reviewed_artifacts_exist") is not True or reviewed_reference.get("reviewed_resolution_records_exist") is not True:
        failures.append("reviewed_reference_missing_reviewed_artifacts")
    if reviewed_reference.get("final_resolution_boundary_crossed") is not False or reviewed_reference.get("weak_feedback_resolved") is not False:
        failures.append("reviewed_reference_final_boundary_wrong")
    if artifact_freeze.get("reviewed_weak_feedback_resolution_records_frozen_count") != 3:
        failures.append("artifact_freeze_count_wrong")
    if resolution_freeze.get("reviewed_resolution_records_frozen_count") != 3:
        failures.append("resolution_freeze_count_wrong")
    if resolution_freeze.get("final_resolution_records_emitted_count") != 0 or resolution_freeze.get("weak_feedback_resolved") is not False:
        failures.append("resolution_freeze_final_wrong")
    if route_freeze.get("all_reviewed_not_closed") is not True:
        failures.append("route_freeze_not_reviewed_not_closed")
    if boundary_lock.get("final_resolution_boundary_crossed") is not False or boundary_lock.get("weak_feedback_resolved") is not False:
        failures.append("boundary_lock_wrong")
    if boundary_lock.get("requires_decision_before_final_resolution_closure") is not True:
        failures.append("boundary_lock_missing_decision_requirement")
    if unresolved_freeze.get("weak_feedback_resolved") is not False or unresolved_freeze.get("reviewed_resolution_records_exist") is not True:
        failures.append("unresolved_freeze_wrong")
    if c5_freeze.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_freeze.get("c5_opened") is not False:
        failures.append("c5_freeze_wrong")
    if receipt_chain.get("chain_status") != "RECEIPT_CHAIN_PRESERVED":
        failures.append("receipt_chain_wrong")
    if downstream_table.get("decision_status") != "POST_CLOSURE_DECISION_READY":
        failures.append("downstream_decision_table_not_ready")
    if closure_authority.get("may_decide_next_after_proposed_record_review_reference_closure") is not True:
        failures.append("closure_authority_no_decide")
    if closure_authority.get("may_close_final_weak_feedback_resolution_now") is not False or closure_authority.get("may_open_c5") is not False:
        failures.append("closure_authority_allows_final_or_c5")
    if closure_classification.get("recommended_next") != EXPECTED_CLOSURE_NEXT:
        failures.append("closure_classification_next_wrong")
    if closure_rollup.get("post_closure_decision_ready_count") != 1 or closure_rollup.get("weak_feedback_resolved_count") != 0:
        failures.append("closure_rollup_wrong")
    if closure_profile.get("next_command_goal") is not None or closure_profile.get("weak_feedback_resolved") is not False:
        failures.append("closure_profile_wrong")
    if closure_report.get("recommended_next_handling") != EXPECTED_CLOSURE_NEXT:
        failures.append("closure_report_next_wrong")
    if closure_trace.get("terminal", {}).get("stop_code") != EXPECTED_CLOSURE_STOP:
        failures.append("closure_trace_stop_wrong")

    return failures, {
        "summary": summary,
        "reviewed_reference": reviewed_reference,
        "artifact_freeze": artifact_freeze,
        "resolution_freeze": resolution_freeze,
        "route_freeze": route_freeze,
        "boundary_lock": boundary_lock,
        "unresolved_freeze": unresolved_freeze,
        "c5_freeze": c5_freeze,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    decision_pass = not failures
    status = "TYPED_O2_PROPOSED_RECORD_REVIEW_POST_CLOSURE_DECISION_SELECTED_FINAL_RESOLUTION_CLOSURE_READY" if decision_pass else "TYPED_O2_PROPOSED_RECORD_REVIEW_POST_CLOSURE_DECISION_GATE_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_O2_PROPOSED_RECORD_REVIEW_POST_CLOSURE_DECISION_V0"

    reason_codes = [
        "POST_REVIEW_REFERENCE_CLOSURE_DECISION_COMPLETE",
        "PROPOSED_RECORD_REVIEW_CLOSURE_RECEIPT_CONSUMED",
        "REVIEWED_ARTIFACT_REFERENCE_CONFIRMED",
        "REVIEWED_RESOLUTION_RECORDS_FROZEN_CONFIRMED",
        "FINAL_RESOLUTION_BOUNDARY_LOCK_CONFIRMED",
        "UNRESOLVED_STATUS_CONFIRMED",
        "C5_BLOCK_CONFIRMED",
        "FINAL_RESOLUTION_CLOSURE_SELECTED_NEXT",
        "NO_FINAL_RESOLUTION_EMITTED_IN_DECISION",
        "NO_WEAK_FEEDBACK_RESOLUTION_RECORDED_IN_DECISION",
        "NO_C5_RECONSIDERATION_READY",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if decision_pass else failures

    decision_basis = {
        "schema_version": "o2_post_review_reference_closure_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_proposed_record_review_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "reviewed_artifacts_frozen": decision_pass,
        "reviewed_resolution_records_exist": decision_pass,
        "reviewed_resolution_records_frozen_count": 3 if decision_pass else 0,
        "final_resolution_boundary_locked_not_crossed": decision_pass,
        "requires_decision_before_final_resolution_closure": decision_pass,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "final_resolution_boundary_crossed": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    decision_table = {
        "schema_version": "o2_post_review_reference_closure_decision_table_v0",
        "decision_status": "NEXT_BRANCH_SELECTED" if decision_pass else "NO_BRANCH_SELECTED",
        "records": [
            {
                "branch": SELECTED_BRANCH,
                "selected": decision_pass,
                "next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
                "why": "Reviewed resolution records are frozen as a reviewed reference and the final-resolution boundary explicitly requires a later decision before closure.",
            },
            {
                "branch": "MARK_WEAK_FEEDBACK_RESOLVED_NOW",
                "selected": False,
                "next_unit": None,
                "why": "This decision only selects final-resolution closure; it does not itself emit final resolution records.",
            },
            {
                "branch": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 remains blocked until final weak-feedback resolution closure exists and a later C5 decision explicitly selects reconsideration.",
            },
            {
                "branch": "RUN_LIVE_FEEDBACK_AUDIT_NOW",
                "selected": False,
                "next_unit": None,
                "why": "This is still the reviewed-artifact/final-resolution closure path, not a live feedback audit path.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "o2_final_resolution_closure_selected_branch_v0",
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "selection_scope": "final weak-feedback resolution closure only",
        "selection_reason": "Reviewed weak-feedback resolution records are frozen as a reviewed reference, but final weak-feedback resolution has not been closed.",
        "selected_branch_does_not": [
            "open C5",
            "run live feedback audit",
            "repair",
            "retry",
            "patch runtime",
            "mutate sources",
            "mutate prior receipts",
            "change architecture",
        ],
    }

    final_closure_authorization = {
        "schema_version": "o2_final_resolution_closure_authorization_v0",
        "authorization_status": "FINAL_RESOLUTION_CLOSURE_AUTHORIZED_NEXT" if decision_pass else "NOT_AUTHORIZED",
        "authorized_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "authorized_execution_mode": "FINAL_RESOLUTION_CLOSURE_FROM_FROZEN_REVIEWED_REFERENCE / NO_C5" if decision_pass else None,
        "authorized_scope": [
            "consume frozen reviewed weak-feedback resolution records",
            "verify reviewed question-answer/source-ref/under-typed records are enough for final closure",
            "emit explicit final-resolution closure artifacts only if gates pass",
            "preserve C5 as blocked unless a later C5 decision explicitly changes it",
        ],
        "not_authorized_in_this_decision": [
            "emit final resolution records",
            "mark weak feedback resolved",
            "set C5 reconsideration ready",
            "open C5",
            "run live feedback audit",
            "repair",
            "retry",
            "patch runtime",
            "mutate sources",
            "mutate prior receipts",
        ],
    }

    input_scope = {
        "schema_version": "o2_final_resolution_closure_input_scope_v0",
        "scope_status": "FROZEN_REVIEWED_REFERENCE_ELIGIBLE_FOR_FINAL_CLOSURE_EXECUTION",
        "source_closure_receipt": rel(SOURCE_CLOSURE_RECEIPT_PATH),
        "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
        "reviewed_artifact_freeze": rel(REVIEWED_ARTIFACT_FREEZE_PATH),
        "reviewed_resolution_freeze": rel(REVIEWED_RESOLUTION_FREEZE_PATH),
        "reviewed_route_freeze": rel(REVIEWED_ROUTE_FREEZE_PATH),
        "final_boundary_lock": rel(FINAL_BOUNDARY_LOCK_PATH),
        "unresolved_status_freeze": rel(UNRESOLVED_FREEZE_PATH),
        "c5_block_freeze": rel(C5_BLOCK_FREEZE_PATH),
        "reviewed_resolution_records_frozen_count": 3,
    }

    unresolved_continuation = {
        "schema_version": "o2_post_review_reference_closure_unresolved_continuation_v0",
        "unresolved_status_continues": True,
        "final_resolution_closure_executed_in_decision": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "final_resolution_boundary_crossed": False,
        "reviewed_resolution_records_exist": True,
    }

    c5_continuation = {
        "schema_version": "o2_post_review_reference_closure_c5_block_continuation_v0",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "block_continues": True,
        "block_reason": "Final-resolution closure has only been selected next, not executed; C5 requires a later explicit decision even after final closure.",
    }

    deferred_branches = {
        "schema_version": "o2_post_review_reference_closure_deferred_branches_v0",
        "deferred": [
            "OPEN_C5",
            "LIVE_FEEDBACK_AUDIT",
            "REPAIR",
            "RETRY",
            "RUNTIME_PATCH",
            "SOURCE_MUTATION",
            "ARCHITECTURE_CHANGE",
        ],
        "why": "This unit only selects the final-resolution closure execution branch.",
    }

    authority_boundary = {
        "schema_version": "o2_post_review_reference_closure_decision_authority_boundary_v0",
        "status": status,
        "may_execute_final_resolution_closure_next": decision_pass,
        "may_emit_final_resolution_records_now_in_decision_unit": False,
        "may_resolve_weak_feedback_now": False,
        "may_set_c5_reconsideration_ready": False,
        "may_open_c5": False,
        "may_run_live_feedback_audit_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_change_architecture": False,
    }

    classification = {
        "schema_version": "o2_post_review_reference_closure_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_closure_decision_complete": decision_pass,
        "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": recommended_next,
        "final_resolution_closure_authorized_next": decision_pass,
        "reviewed_resolution_records_exist": True,
        "reviewed_resolution_records_frozen_count": 3,
        "final_resolution_closure_executed_in_decision": False,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "final_resolution_boundary_crossed": False,
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
        "schema_version": "o2_post_review_reference_closure_decision_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "decision_count": 1 if decision_pass else 0,
        "selected_final_resolution_closure_count": 1 if decision_pass else 0,
        "final_resolution_closure_authorized_next_count": 1 if decision_pass else 0,
        "reviewed_resolution_records_exist_count": 1,
        "reviewed_resolution_records_frozen_count": 3,
        "weak_feedback_resolved_count": 0,
        "resolution_records_emitted_count": 0,
        "final_resolution_boundary_crossed_count": 0,
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
        "final_resolution_boundary_crossed_count",
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
        "schema_version": "o2_post_review_reference_closure_decision_profile_v0",
        "profile_id": "o2_post_review_reference_closure_decision_profile_" + sha8(rollup),
        "status": status,
        "selected_next_unit": recommended_next,
        "decision": "execute final weak-feedback resolution closure next",
        "reviewed_resolution_records_exist": True,
        "reviewed_resolution_records_frozen_count": 3,
        "final_resolution_closure_executed_in_decision": False,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "final_resolution_boundary_crossed": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Execute final-resolution closure next. Do not treat this decision as final resolution or C5 readiness.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_post_review_reference_closure_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The post-closure decision selected final weak-feedback resolution closure as the next branch. This decision does not itself resolve weak feedback and does not unblock C5.",
        "reviewed_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "final_resolution_boundary_crossed": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_post_review_reference_closure_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_reviewed_artifact_reference_closure",
                "question": "is the reviewed-artifact reference closed cleanly",
                "answer": "yes" if decision_pass else "no",
                "taken": "evaluate final-resolution closure branch",
            },
            {
                "step": "select_final_resolution_closure",
                "question": "what is the next lawful edge",
                "answer": SELECTED_NEXT_UNIT if decision_pass else recommended_next,
                "taken": "authorize final-resolution closure execution next",
            },
            {
                "step": "preserve_c5_boundary",
                "question": "does this decision open C5",
                "answer": "no",
                "taken": "keep C5 blocked",
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
        (FINAL_CLOSURE_AUTHORIZATION_PATH, final_closure_authorization),
        (FINAL_CLOSURE_INPUT_SCOPE_PATH, input_scope),
        (UNRESOLVED_CONTINUATION_PATH, unresolved_continuation),
        (C5_BLOCK_CONTINUATION_PATH, c5_continuation),
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
        "POST_REVIEW_CLOSURE_DECIDE_0_SOURCE_CLOSURE_RECEIPT_CONSUMED": SOURCE_CLOSURE_RECEIPT_PATH.exists(),
        "POST_REVIEW_CLOSURE_DECIDE_1_DECISION_BASIS_EMITTED": DECISION_BASIS_PATH.exists(),
        "POST_REVIEW_CLOSURE_DECIDE_2_REVIEWED_REFERENCE_CONFIRMED": decision_basis["reviewed_artifacts_frozen"] is True,
        "POST_REVIEW_CLOSURE_DECIDE_3_REVIEWED_RESOLUTION_RECORDS_CONFIRMED": decision_basis["reviewed_resolution_records_exist"] is True and decision_basis["reviewed_resolution_records_frozen_count"] == 3,
        "POST_REVIEW_CLOSURE_DECIDE_4_FINAL_BOUNDARY_LOCK_CONFIRMED": decision_basis["final_resolution_boundary_locked_not_crossed"] is True,
        "POST_REVIEW_CLOSURE_DECIDE_5_C5_BLOCK_CONFIRMED": decision_basis["c5_opened"] is False and decision_basis["c5_reconsideration_ready"] is False,
        "POST_REVIEW_CLOSURE_DECIDE_6_FINAL_RESOLUTION_CLOSURE_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_REVIEW_CLOSURE_DECIDE_7_FINAL_CLOSURE_AUTHORIZATION_EMITTED": final_closure_authorization["authorized_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_REVIEW_CLOSURE_DECIDE_8_NO_FINAL_RESOLUTION_EMITTED_IN_DECISION": rollup["resolution_records_emitted_count"] == 0 and rollup["weak_feedback_resolved_count"] == 0,
        "POST_REVIEW_CLOSURE_DECIDE_9_C5_NOT_OPENED": rollup["c5_opened_count"] == 0 and rollup["c5_reconsideration_ready_count"] == 0,
        "POST_REVIEW_CLOSURE_DECIDE_10_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "POST_REVIEW_CLOSURE_DECIDE_11_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "POST_REVIEW_CLOSURE_DECIDE_12_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "POST_REVIEW_CLOSURE_DECIDE_13_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "POST_REVIEW_CLOSURE_DECIDE_14_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_PROPOSED_RECORD_REVIEW_POST_CLOSURE_DECISION_GATE_FAIL",
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
        "schema_version": "o2_post_review_reference_closure_decision_receipt_v0",
        "receipt_type": "TYPED_O2_POST_REVIEW_REFERENCE_CLOSURE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_proposed_record_review_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "machine_readable_o2_post_review_reference_closure_decision_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_closure_decision_complete": decision_pass,
            "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
            "selected_next_unit": recommended_next,
            "final_resolution_closure_authorized_next": decision_pass,
            "reviewed_resolution_records_exist": True,
            "reviewed_resolution_records_frozen_count": 3,
            "final_resolution_closure_executed_in_decision": False,
            "resolution_records_emitted_count": 0,
            "weak_feedback_resolved": False,
            "final_resolution_boundary_crossed": False,
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
            "final_resolution_closure_authorization": rel(FINAL_CLOSURE_AUTHORIZATION_PATH),
            "final_resolution_closure_input_scope": rel(FINAL_CLOSURE_INPUT_SCOPE_PATH),
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
    print(f"post_review_reference_closure_decision_receipt_id={receipt_id}")
    print(f"post_review_reference_closure_decision_receipt_path={rel(receipt_path)}")
    print(f"post_review_reference_closure_decision_basis_path={rel(DECISION_BASIS_PATH)}")
    print(f"final_resolution_closure_selected_branch_path={rel(SELECTED_BRANCH_PATH)}")
    print(f"final_resolution_closure_authorization_path={rel(FINAL_CLOSURE_AUTHORIZATION_PATH)}")
    print(f"post_review_reference_closure_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"post_review_reference_closure_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
