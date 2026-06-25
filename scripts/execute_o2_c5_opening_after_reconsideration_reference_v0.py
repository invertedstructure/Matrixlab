#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXECUTE_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_V0"
TARGET_UNIT_ID = "observation.o2_c5_opening_after_reconsideration_reference.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / C5_OPENING_AFTER_RECONSIDERATION_REFERENCE"
MODE = "EXECUTE / EMIT_C5_OPENED / NO_LIVE_AUDIT_NO_BUILD_TARGET"
BUILD_MODE = "O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_ONLY"

SOURCE_DECISION_RECEIPT_ID = "06d082d7"

SOURCE_DECISION_RECEIPT_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0_receipts/06d082d7.json"
DECISION_BASIS_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_post_reconsideration_reference_decision_basis_v0.json"
DECISION_TABLE_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_post_reconsideration_reference_decision_table_v0.json"
SELECTED_BRANCH_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_opening_selected_branch_v0.json"
C5_OPENING_AUTH_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_opening_authorization_v0.json"
C5_OPENING_INPUT_SCOPE_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_opening_input_scope_v0.json"
C5_RECONSIDERATION_CONTINUATION_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_reconsideration_reference_continuation_v0.json"
C5_OPENING_GUARD_CONTINUATION_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_opening_guard_continuation_until_execution_v0.json"
DEFERRED_BRANCHES_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_post_reconsideration_reference_deferred_branches_v0.json"
DECISION_AUTHORITY_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_post_reconsideration_reference_decision_authority_boundary_v0.json"
DECISION_CLASSIFICATION_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_post_reconsideration_reference_decision_classification_v0.json"
DECISION_ROLLUP_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_post_reconsideration_reference_decision_rollup_v0.json"
DECISION_PROFILE_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_post_reconsideration_reference_decision_profile_v0.json"
DECISION_REPORT_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_post_reconsideration_reference_decision_report.json"
DECISION_TRACE_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0/o2_c5_post_reconsideration_reference_decision_transition_trace.json"

REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0_receipts/3167d93a.json"
REVIEWED_REFERENCE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_reviewed_reference_v0.json"
READY_STATUS_REFERENCE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_ready_status_reference_v0.json"
OPENING_GUARD_REFERENCE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_opening_guard_reference_v0.json"
OPEN_DECISION_CANDIDATE_REFERENCE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_open_decision_candidate_reference_v0.json"
WEAK_FEEDBACK_BASIS_REFERENCE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_weak_feedback_basis_reference_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_DECISION_RECEIPT_PATH,
    DECISION_BASIS_PATH,
    DECISION_TABLE_PATH,
    SELECTED_BRANCH_PATH,
    C5_OPENING_AUTH_PATH,
    C5_OPENING_INPUT_SCOPE_PATH,
    C5_RECONSIDERATION_CONTINUATION_PATH,
    C5_OPENING_GUARD_CONTINUATION_PATH,
    DEFERRED_BRANCHES_PATH,
    DECISION_AUTHORITY_PATH,
    DECISION_CLASSIFICATION_PATH,
    DECISION_ROLLUP_PATH,
    DECISION_PROFILE_PATH,
    DECISION_REPORT_PATH,
    DECISION_TRACE_PATH,
    REFERENCE_CLOSURE_RECEIPT_PATH,
    REVIEWED_REFERENCE_PATH,
    READY_STATUS_REFERENCE_PATH,
    OPENING_GUARD_REFERENCE_PATH,
    OPEN_DECISION_CANDIDATE_REFERENCE_PATH,
    WEAK_FEEDBACK_BASIS_REFERENCE_PATH,
]

OUT_DIR = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0"
RECEIPT_DIR = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0_receipts"

EXECUTION_RECORD_PATH = OUT_DIR / "o2_c5_opening_execution_record_v0.json"
OPEN_STATUS_PATH = OUT_DIR / "o2_c5_open_status_v0.json"
OPENING_RECORD_PATH = OUT_DIR / "o2_c5_opening_record_v0.json"
AUTH_CONSUMPTION_PATH = OUT_DIR / "o2_c5_opening_authorization_consumption_v0.json"
INPUT_CONFIRMATION_PATH = OUT_DIR / "o2_c5_opening_input_confirmation_v0.json"
RECONSIDERATION_REFERENCE_BASIS_PATH = OUT_DIR / "o2_c5_opening_reconsideration_reference_basis_v0.json"
LIVE_AUDIT_GUARD_PATH = OUT_DIR / "o2_c5_live_audit_deferred_guard_v0.json"
BUILD_TARGET_GUARD_PATH = OUT_DIR / "o2_c5_build_target_guard_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_c5_opening_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_c5_opening_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_c5_opening_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_c5_opening_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_c5_opening_report.json"
TRACE_PATH = OUT_DIR / "o2_c5_opening_transition_trace.json"

EXPECTED_DECISION_STATUS = "TYPED_O2_POST_C5_RECONSIDERATION_REFERENCE_DECISION_SELECTED_C5_OPENING_EXECUTION_READY"
EXPECTED_DECISION_STOP = "STOP_TYPED_O2_POST_C5_RECONSIDERATION_REFERENCE_DECISION_SELECTED_C5_OPENING_EXECUTION_READY"
EXPECTED_DECISION_NEXT = "EXECUTE_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_V0"
RECOMMENDED_NEXT = "REVIEW_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_V0"

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

    decision_receipt = read_json(SOURCE_DECISION_RECEIPT_PATH)
    decision_summary = decision_receipt.get("machine_readable_o2_c5_post_reconsideration_reference_decision_summary", {})
    decision_basis = read_json(DECISION_BASIS_PATH)
    selected_branch = read_json(SELECTED_BRANCH_PATH)
    opening_auth = read_json(C5_OPENING_AUTH_PATH)
    opening_input_scope = read_json(C5_OPENING_INPUT_SCOPE_PATH)
    reconsideration_continuation = read_json(C5_RECONSIDERATION_CONTINUATION_PATH)
    guard_continuation = read_json(C5_OPENING_GUARD_CONTINUATION_PATH)
    decision_authority = read_json(DECISION_AUTHORITY_PATH)
    decision_rollup = read_json(DECISION_ROLLUP_PATH)
    decision_profile = read_json(DECISION_PROFILE_PATH)
    decision_report = read_json(DECISION_REPORT_PATH)
    decision_trace = read_json(DECISION_TRACE_PATH)

    reference_receipt = read_json(REFERENCE_CLOSURE_RECEIPT_PATH)
    reviewed_reference = read_json(REVIEWED_REFERENCE_PATH)
    ready_reference = read_json(READY_STATUS_REFERENCE_PATH)
    guard_reference = read_json(OPENING_GUARD_REFERENCE_PATH)
    candidate_reference = read_json(OPEN_DECISION_CANDIDATE_REFERENCE_PATH)
    weak_feedback_basis = read_json(WEAK_FEEDBACK_BASIS_REFERENCE_PATH)

    if decision_receipt.get("receipt_id") != SOURCE_DECISION_RECEIPT_ID or decision_receipt.get("gate") != "PASS":
        failures.append("source_decision_receipt_not_pass")
    if decision_receipt.get("terminal", {}).get("stop_code") != EXPECTED_DECISION_STOP:
        failures.append("source_decision_stop_wrong")
    if decision_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_decision_hidden_next")
    if decision_summary.get("status") != EXPECTED_DECISION_STATUS:
        failures.append(f"source_decision_status_wrong:{decision_summary.get('status')}")
    if decision_summary.get("recommended_next") != EXPECTED_DECISION_NEXT:
        failures.append(f"source_decision_next_wrong:{decision_summary.get('recommended_next')}")

    for key in [
        "post_c5_reconsideration_reference_decision_complete",
        "c5_opening_authorized_next",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
        "c5_reconsideration_ready",
        "c5_open_decision_candidate_ready",
        "bad_counters_zero",
    ]:
        if decision_summary.get(key) is not True:
            failures.append(f"decision_summary_required_true_missing:{key}")

    if decision_summary.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("decision_selected_next_wrong")
    if decision_summary.get("c5_opened") is not False or decision_summary.get("c5_opening_executed_in_decision") is not False:
        failures.append("decision_already_opened_c5")
    if decision_summary.get("live_feedback_audit_executed") is not False:
        failures.append("decision_ran_live_audit")

    if decision_basis.get("c5_reconsideration_ready") is not True or decision_basis.get("c5_opened") is not False:
        failures.append("decision_basis_c5_wrong")
    if selected_branch.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("selected_branch_wrong")
    if opening_auth.get("authorization_status") != "C5_OPENING_EXECUTION_AUTHORIZED_NEXT":
        failures.append("opening_authorization_status_wrong")
    if opening_auth.get("authorized_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("opening_authorization_next_wrong")
    if "open C5" not in opening_auth.get("not_authorized_in_this_decision", []):
        failures.append("opening_authorization_missing_decision_boundary")
    if opening_input_scope.get("scope_status") != "C5_RECONSIDERATION_REVIEWED_REFERENCE_ELIGIBLE_FOR_OPENING_EXECUTION":
        failures.append("opening_input_scope_wrong")
    if reconsideration_continuation.get("c5_reconsideration_ready") is not True or reconsideration_continuation.get("c5_opened") is not False:
        failures.append("reconsideration_continuation_wrong")
    if guard_continuation.get("c5_opened") is not False:
        failures.append("guard_continuation_already_open")
    if decision_authority.get("may_execute_c5_opening_next") is not True:
        failures.append("decision_authority_no_execute")
    if decision_authority.get("may_open_c5_now_in_decision") is not False:
        failures.append("decision_authority_allows_decision_open")
    if decision_rollup.get("selected_c5_opening_execution_count") != 1 or decision_rollup.get("c5_opened_count") != 0:
        failures.append("decision_rollup_wrong")
    if decision_profile.get("selected_next_unit") != EXPECTED_DECISION_NEXT or decision_profile.get("c5_opened") is not False:
        failures.append("decision_profile_wrong")
    if decision_report.get("recommended_next_handling") != EXPECTED_DECISION_NEXT:
        failures.append("decision_report_next_wrong")
    if decision_trace.get("terminal", {}).get("stop_code") != EXPECTED_DECISION_STOP:
        failures.append("decision_trace_stop_wrong")

    if reference_receipt.get("receipt_id") != "3167d93a" or reference_receipt.get("gate") != "PASS":
        failures.append("reference_receipt_not_pass")
    if reviewed_reference.get("c5_reconsideration_ready") is not True or reviewed_reference.get("c5_opened") is not False:
        failures.append("reviewed_reference_wrong")
    if ready_reference.get("c5_reconsideration_ready") is not True or ready_reference.get("c5_opened") is not False:
        failures.append("ready_reference_wrong")
    if guard_reference.get("guard_status") != "C5_OPENING_GUARD_FROZEN_AS_REFERENCE" and guard_reference.get("guard_status") != "C5_OPENING_GUARD_HELD":
        failures.append("guard_reference_status_wrong")
    if guard_reference.get("may_open_c5_now") is not False:
        failures.append("guard_reference_allows_open")
    if candidate_reference.get("c5_open_decision_candidate_ready") is not True or candidate_reference.get("c5_opened") is not False:
        failures.append("candidate_reference_wrong")
    if weak_feedback_basis.get("weak_feedback_resolved") is not True or weak_feedback_basis.get("resolution_records_emitted_count") != 3:
        failures.append("weak_feedback_basis_wrong")

    return failures, {
        "decision_summary": decision_summary,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, _ = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    execute_pass = not failures
    status = "TYPED_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_EXECUTED_OPENED_REVIEW_READY" if execute_pass else "TYPED_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if execute_pass else "REPAIR_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_V0"

    reason_codes = [
        "C5_OPENING_EXECUTED",
        "POST_C5_RECONSIDERATION_REFERENCE_DECISION_RECEIPT_CONSUMED",
        "C5_RECONSIDERATION_REVIEWED_REFERENCE_CONSUMED",
        "C5_OPEN_DECISION_CANDIDATE_CONFIRMED",
        "C5_OPENING_AUTHORIZATION_CONSUMED",
        "C5_OPENED_RECORD_EMITTED",
        "C5_OPEN_STATUS_EMITTED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_BUILD_TARGET_SELECTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if execute_pass else failures

    execution_record = {
        "schema_version": "o2_c5_opening_execution_record_v0",
        "execution_status": "C5_OPENING_EXECUTED_REVIEW_READY" if execute_pass else "C5_OPENING_EXECUTION_FAIL",
        "source_post_c5_reconsideration_reference_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "c5_opening_executed": execute_pass,
        "c5_opened": execute_pass,
        "c5_feedback_readiness_before_opening": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_feedback_readiness_after_opening": "C5_OPENED_PENDING_REVIEW" if execute_pass else "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "live_feedback_audit_executed": False,
        "target_selected_for_build": False,
        "review_required_next": execute_pass,
    }

    open_status = {
        "schema_version": "o2_c5_open_status_v0",
        "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW" if execute_pass else "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
        "c5_open_decision_candidate_ready": True,
        "c5_opened": execute_pass,
        "c5_opening_review_required": execute_pass,
        "live_feedback_audit_executed": False,
        "c5_live_branch_executed": False,
    }

    opening_record = {
        "schema_version": "o2_c5_opening_record_v0",
        "opening_status": "C5_OPENED_FOR_REVIEW" if execute_pass else "C5_NOT_OPENED",
        "opening_basis": "reviewed C5 reconsideration reference plus post-reference opening authorization",
        "c5_opened": execute_pass,
        "opening_does_not_mean": [
            "live C5 audit executed",
            "C5 build target selected",
            "runtime patched",
            "source mutated",
            "architecture changed",
        ],
    }

    auth_consumption = {
        "schema_version": "o2_c5_opening_authorization_consumption_v0",
        "authorization_consumed": execute_pass,
        "source_authorization": rel(C5_OPENING_AUTH_PATH),
        "authorized_next_unit": UNIT_ID,
        "authorization_result": "C5_OPENING_EXECUTED" if execute_pass else "C5_OPENING_NOT_EXECUTED",
    }

    input_confirmation = {
        "schema_version": "o2_c5_opening_input_confirmation_v0",
        "input_status": "C5_OPENING_INPUTS_CONFIRMED",
        "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "source_reconsideration_reference_closure_receipt_id": "3167d93a",
        "c5_reconsideration_ready": True,
        "c5_open_decision_candidate_ready": True,
        "c5_opened_before_execution": False,
    }

    reconsideration_basis = {
        "schema_version": "o2_c5_opening_reconsideration_reference_basis_v0",
        "basis_status": "C5_RECONSIDERATION_REFERENCE_BASIS_CONFIRMED",
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_reconsideration_ready": True,
        "c5_open_decision_candidate_ready": True,
    }

    live_audit_guard = {
        "schema_version": "o2_c5_live_audit_deferred_guard_v0",
        "guard_status": "LIVE_AUDIT_NOT_EXECUTED",
        "c5_opened": execute_pass,
        "live_feedback_audit_executed": False,
        "may_run_live_feedback_audit_now": False,
        "requires_explicit_post_opening_review_decision": True,
    }

    build_target_guard = {
        "schema_version": "o2_c5_build_target_guard_v0",
        "guard_status": "BUILD_TARGET_NOT_SELECTED",
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "architecture_change": False,
    }

    authority_boundary = {
        "schema_version": "o2_c5_opening_authority_boundary_v0",
        "status": status,
        "may_review_c5_opening_next": execute_pass,
        "may_run_live_feedback_audit_now": False,
        "may_select_build_target_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_change_architecture": False,
    }

    classification = {
        "schema_version": "o2_c5_opening_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c5_opening_executed": execute_pass,
        "review_ready": execute_pass,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW" if execute_pass else "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
        "c5_open_decision_candidate_ready": True,
        "c5_opened": execute_pass,
        "live_feedback_audit_executed": False,
        "c5_live_branch_executed": False,
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
        "schema_version": "o2_c5_opening_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "c5_opening_executed_count": 1 if execute_pass else 0,
        "review_ready_count": 1 if execute_pass else 0,
        "weak_feedback_resolved_count": 1,
        "final_resolution_boundary_crossed_count": 1,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_reconsideration_ready_count": 1,
        "c5_open_decision_candidate_ready_count": 1,
        "c5_opened_count": 1 if execute_pass else 0,
        "live_feedback_audit_executed_count": 0,
        "c5_live_branch_executed_count": 0,
        "repair_applied_count": 0,
        "retry_executed_count": 0,
        "target_selected_for_build_count": 0,
        "runtime_patch_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "architecture_change_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "live_feedback_audit_executed_count",
        "c5_live_branch_executed_count",
        "repair_applied_count",
        "retry_executed_count",
        "target_selected_for_build_count",
        "runtime_patch_count",
        "source_mutated_count",
        "prior_receipt_mutated_count",
        "architecture_change_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "o2_c5_opening_profile_v0",
        "profile_id": "o2_c5_opening_profile_" + sha8(rollup),
        "status": status,
        "c5_opening_executed": execute_pass,
        "review_ready": execute_pass,
        "weak_feedback_resolved": True,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW" if execute_pass else "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_opened": execute_pass,
        "live_feedback_audit_executed": False,
        "target_selected_for_build": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Review C5 opening next. Do not treat opening as live audit or build execution.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_c5_opening_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C5 opening was executed from the reviewed reconsideration reference. This opened C5 for review only; live audit and build target selection did not run.",
        "weak_feedback_resolved": True,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW" if execute_pass else "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_opened": execute_pass,
        "live_feedback_audit_executed": False,
        "target_selected_for_build": False,
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_c5_opening_transition_trace_v0",
        "trace": [
            {
                "step": "consume_post_c5_reconsideration_decision",
                "question": "is C5 opening execution authorized",
                "answer": "yes" if execute_pass else "no",
                "taken": "consume reviewed C5 reconsideration reference",
            },
            {
                "step": "emit_c5_opening_record",
                "question": "may C5 be opened for review",
                "answer": "yes" if execute_pass else "no",
                "taken": "emit C5 opened pending review",
            },
            {
                "step": "hold_live_audit_guard",
                "question": "does this execution run live audit or build target",
                "answer": "no",
                "taken": "defer live audit/build until later explicit decision",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (EXECUTION_RECORD_PATH, execution_record),
        (OPEN_STATUS_PATH, open_status),
        (OPENING_RECORD_PATH, opening_record),
        (AUTH_CONSUMPTION_PATH, auth_consumption),
        (INPUT_CONFIRMATION_PATH, input_confirmation),
        (RECONSIDERATION_REFERENCE_BASIS_PATH, reconsideration_basis),
        (LIVE_AUDIT_GUARD_PATH, live_audit_guard),
        (BUILD_TARGET_GUARD_PATH, build_target_guard),
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
        "C5_OPEN_0_DECISION_RECEIPT_CONSUMED": SOURCE_DECISION_RECEIPT_PATH.exists(),
        "C5_OPEN_1_OPENING_AUTHORIZATION_CONSUMED": auth_consumption["authorization_consumed"] is True,
        "C5_OPEN_2_RECONSIDERATION_REFERENCE_CONFIRMED": reconsideration_basis["c5_reconsideration_ready"] is True,
        "C5_OPEN_3_OPEN_DECISION_CANDIDATE_CONFIRMED": reconsideration_basis["c5_open_decision_candidate_ready"] is True,
        "C5_OPEN_4_C5_OPENED_RECORD_EMITTED": opening_record["c5_opened"] is True,
        "C5_OPEN_5_C5_OPEN_STATUS_EMITTED": open_status["c5_opened"] is True,
        "C5_OPEN_6_REVIEW_READY": execution_record["review_required_next"] is True,
        "C5_OPEN_7_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0 and rollup["c5_live_branch_executed_count"] == 0,
        "C5_OPEN_8_NO_BUILD_TARGET": rollup["target_selected_for_build_count"] == 0,
        "C5_OPEN_9_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "C5_OPEN_10_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C5_OPEN_11_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "C5_OPEN_12_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "c5_opened": execute_pass,
        "live_feedback_audit_executed": False,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_c5_opening_after_reconsideration_reference_receipt_v0",
        "receipt_type": "TYPED_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_post_c5_reconsideration_reference_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "machine_readable_o2_c5_opening_after_reconsideration_reference_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c5_opening_executed": execute_pass,
            "review_ready": execute_pass,
            "weak_feedback_resolved": True,
            "final_resolution_boundary_crossed": True,
            "final_resolution_records_frozen_count": 3,
            "resolution_records_emitted_count": 3,
            "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW" if execute_pass else "C5_RECONSIDERATION_READY_PENDING_REVIEW",
            "c5_reconsideration_ready": True,
            "c5_open_decision_candidate_ready": True,
            "c5_opened": execute_pass,
            "live_feedback_audit_executed": False,
            "c5_live_branch_executed": False,
            "target_selected_for_build": False,
            "repair_applied": False,
            "retry_executed": False,
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
            "execution_record": rel(EXECUTION_RECORD_PATH),
            "open_status": rel(OPEN_STATUS_PATH),
            "opening_record": rel(OPENING_RECORD_PATH),
            "authorization_consumption": rel(AUTH_CONSUMPTION_PATH),
            "input_confirmation": rel(INPUT_CONFIRMATION_PATH),
            "reconsideration_reference_basis": rel(RECONSIDERATION_REFERENCE_BASIS_PATH),
            "live_audit_guard": rel(LIVE_AUDIT_GUARD_PATH),
            "build_target_guard": rel(BUILD_TARGET_GUARD_PATH),
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
    print(f"c5_opening_receipt_id={receipt_id}")
    print(f"c5_opening_receipt_path={rel(receipt_path)}")
    print(f"c5_opening_execution_record_path={rel(EXECUTION_RECORD_PATH)}")
    print(f"c5_open_status_path={rel(OPEN_STATUS_PATH)}")
    print(f"c5_opening_record_path={rel(OPENING_RECORD_PATH)}")
    print(f"c5_live_audit_guard_path={rel(LIVE_AUDIT_GUARD_PATH)}")
    print(f"c5_opening_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c5_opening_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
