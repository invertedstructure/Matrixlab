#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXECUTE_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_V0"
TARGET_UNIT_ID = "observation.o2_c5_reconsideration_after_weak_feedback_resolution.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION"
MODE = "EXECUTE / EMIT_C5_RECONSIDERATION_READY / NO_C5_OPEN_NO_LIVE_AUDIT"
BUILD_MODE = "O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_ONLY"

SOURCE_DECISION_RECEIPT_ID = "4b9662bc"

SOURCE_DECISION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0_receipts/4b9662bc.json"
DECISION_BASIS_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_post_final_resolution_reference_decision_basis_v0.json"
DECISION_TABLE_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_post_final_resolution_reference_decision_table_v0.json"
SELECTED_BRANCH_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_c5_reconsideration_selected_branch_v0.json"
C5_AUTH_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_c5_reconsideration_authorization_v0.json"
C5_INPUT_SCOPE_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_c5_reconsideration_input_scope_v0.json"
RESOLVED_CONTINUATION_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_resolved_weak_feedback_reference_continuation_v0.json"
C5_BLOCK_CONTINUATION_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_c5_block_continuation_until_execution_v0.json"
DEFERRED_BRANCHES_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_post_final_resolution_reference_deferred_branches_v0.json"
DECISION_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_post_final_resolution_reference_decision_authority_boundary_v0.json"
DECISION_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_post_final_resolution_reference_decision_classification_v0.json"
DECISION_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_post_final_resolution_reference_decision_rollup_v0.json"
DECISION_PROFILE_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_post_final_resolution_reference_decision_profile_v0.json"
DECISION_REPORT_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_post_final_resolution_reference_decision_report.json"
DECISION_TRACE_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0/o2_post_final_resolution_reference_decision_transition_trace.json"

REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0_receipts/01f38b19.json"
REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_resolution_closure_reviewed_reference_v0.json"
FINAL_RESOLUTION_RECORDS_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_weak_feedback_resolution_records_reference_v0.json"
RESOLVED_STATUS_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_weak_feedback_resolved_status_reference_v0.json"
FINAL_BOUNDARY_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_resolution_boundary_crossing_reference_v0.json"
C5_BLOCK_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_c5_block_pending_decision_reference_v0.json"
POST_REFERENCE_DECISION_READINESS_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_post_final_resolution_closure_reference_decision_readiness_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_DECISION_RECEIPT_PATH,
    DECISION_BASIS_PATH,
    DECISION_TABLE_PATH,
    SELECTED_BRANCH_PATH,
    C5_AUTH_PATH,
    C5_INPUT_SCOPE_PATH,
    RESOLVED_CONTINUATION_PATH,
    C5_BLOCK_CONTINUATION_PATH,
    DEFERRED_BRANCHES_PATH,
    DECISION_AUTHORITY_PATH,
    DECISION_CLASSIFICATION_PATH,
    DECISION_ROLLUP_PATH,
    DECISION_PROFILE_PATH,
    DECISION_REPORT_PATH,
    DECISION_TRACE_PATH,
    REFERENCE_CLOSURE_RECEIPT_PATH,
    REVIEWED_REFERENCE_PATH,
    FINAL_RESOLUTION_RECORDS_REFERENCE_PATH,
    RESOLVED_STATUS_REFERENCE_PATH,
    FINAL_BOUNDARY_REFERENCE_PATH,
    C5_BLOCK_REFERENCE_PATH,
    POST_REFERENCE_DECISION_READINESS_PATH,
]

OUT_DIR = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0"
RECEIPT_DIR = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0_receipts"

EXECUTION_RECORD_PATH = OUT_DIR / "o2_c5_reconsideration_execution_record_v0.json"
READINESS_RECORD_PATH = OUT_DIR / "o2_c5_reconsideration_ready_record_v0.json"
READINESS_STATUS_PATH = OUT_DIR / "o2_c5_reconsideration_ready_status_v0.json"
C5_OPENING_GUARD_PATH = OUT_DIR / "o2_c5_opening_guard_v0.json"
WEAK_FEEDBACK_RESOLUTION_BASIS_PATH = OUT_DIR / "o2_c5_reconsideration_weak_feedback_resolution_basis_v0.json"
INPUT_CONFIRMATION_PATH = OUT_DIR / "o2_c5_reconsideration_input_confirmation_v0.json"
OPENING_DEFERRED_PATH = OUT_DIR / "o2_c5_opening_deferred_until_explicit_decision_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_c5_reconsideration_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_c5_reconsideration_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_c5_reconsideration_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_c5_reconsideration_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_c5_reconsideration_report.json"
TRACE_PATH = OUT_DIR / "o2_c5_reconsideration_transition_trace.json"

EXPECTED_DECISION_STATUS = "TYPED_O2_POST_FINAL_RESOLUTION_REFERENCE_DECISION_SELECTED_C5_RECONSIDERATION_READY"
EXPECTED_DECISION_STOP = "STOP_TYPED_O2_POST_FINAL_RESOLUTION_REFERENCE_DECISION_SELECTED_C5_RECONSIDERATION_READY"
EXPECTED_DECISION_NEXT = "EXECUTE_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_V0"
RECOMMENDED_NEXT = "REVIEW_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_V0"

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
    decision_summary = decision_receipt.get("machine_readable_o2_post_final_resolution_reference_decision_summary", {})
    decision_basis = read_json(DECISION_BASIS_PATH)
    selected_branch = read_json(SELECTED_BRANCH_PATH)
    c5_auth = read_json(C5_AUTH_PATH)
    c5_input_scope = read_json(C5_INPUT_SCOPE_PATH)
    resolved_continuation = read_json(RESOLVED_CONTINUATION_PATH)
    c5_block_continuation = read_json(C5_BLOCK_CONTINUATION_PATH)
    deferred = read_json(DEFERRED_BRANCHES_PATH)
    decision_authority = read_json(DECISION_AUTHORITY_PATH)
    decision_classification = read_json(DECISION_CLASSIFICATION_PATH)
    decision_rollup = read_json(DECISION_ROLLUP_PATH)
    decision_profile = read_json(DECISION_PROFILE_PATH)
    decision_report = read_json(DECISION_REPORT_PATH)
    decision_trace = read_json(DECISION_TRACE_PATH)

    reference_receipt = read_json(REFERENCE_CLOSURE_RECEIPT_PATH)
    reviewed_reference = read_json(REVIEWED_REFERENCE_PATH)
    final_resolution_reference = read_json(FINAL_RESOLUTION_RECORDS_REFERENCE_PATH)
    resolved_reference = read_json(RESOLVED_STATUS_REFERENCE_PATH)
    boundary_reference = read_json(FINAL_BOUNDARY_REFERENCE_PATH)
    c5_reference = read_json(C5_BLOCK_REFERENCE_PATH)
    post_reference_readiness = read_json(POST_REFERENCE_DECISION_READINESS_PATH)

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
        "post_final_resolution_reference_decision_complete",
        "c5_reconsideration_authorized_next",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
        "bad_counters_zero",
    ]:
        if decision_summary.get(key) is not True:
            failures.append(f"decision_summary_required_true_missing:{key}")

    if decision_summary.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("decision_selected_next_wrong")
    if decision_summary.get("final_resolution_records_frozen_count") != 3:
        failures.append("decision_final_record_count_wrong")
    if decision_summary.get("resolution_records_emitted_count") != 3:
        failures.append("decision_resolution_count_wrong")

    for key in [
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
        if decision_summary.get(key) is not False:
            failures.append(f"decision_summary_forbidden_true:{key}")

    if decision_basis.get("weak_feedback_resolved") is not True:
        failures.append("decision_basis_not_resolved")
    if selected_branch.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("selected_branch_wrong")
    if c5_auth.get("authorization_status") != "C5_RECONSIDERATION_AUTHORIZED_NEXT":
        failures.append("c5_authorization_status_wrong")
    if c5_auth.get("authorized_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("c5_authorization_next_wrong")
    if "open C5" not in c5_auth.get("not_authorized_in_this_decision", []):
        failures.append("c5_authorization_missing_no_open")
    if c5_input_scope.get("scope_status") != "FROZEN_FINAL_RESOLUTION_REFERENCE_ELIGIBLE_FOR_C5_RECONSIDERATION_EXECUTION":
        failures.append("c5_input_scope_wrong")
    if resolved_continuation.get("weak_feedback_resolved") is not True:
        failures.append("resolved_continuation_wrong")
    if c5_block_continuation.get("c5_opened") is not False or c5_block_continuation.get("c5_reconsideration_ready") is not False:
        failures.append("c5_block_continuation_wrong")
    if "OPEN_C5_NOW" not in deferred.get("deferred", []):
        failures.append("deferred_missing_open_c5")
    if decision_authority.get("may_execute_c5_reconsideration_next") is not True:
        failures.append("decision_authority_no_execute")
    if decision_authority.get("may_set_c5_reconsideration_ready_now_in_decision") is not False or decision_authority.get("may_open_c5_now") is not False:
        failures.append("decision_authority_allows_now")
    if decision_classification.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("decision_classification_next_wrong")
    if decision_rollup.get("selected_c5_reconsideration_count") != 1:
        failures.append("decision_rollup_selection_wrong")
    if decision_rollup.get("c5_opened_count") != 0 or decision_rollup.get("c5_reconsideration_ready_count") != 0:
        failures.append("decision_rollup_c5_wrong")
    if decision_profile.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("decision_profile_next_wrong")
    if decision_report.get("recommended_next_handling") != EXPECTED_DECISION_NEXT:
        failures.append("decision_report_next_wrong")
    if decision_trace.get("terminal", {}).get("stop_code") != EXPECTED_DECISION_STOP:
        failures.append("decision_trace_stop_wrong")

    if reference_receipt.get("receipt_id") != "01f38b19" or reference_receipt.get("gate") != "PASS":
        failures.append("reference_receipt_not_pass")
    if reviewed_reference.get("weak_feedback_resolved") is not True:
        failures.append("reviewed_reference_not_resolved")
    if reviewed_reference.get("c5_opened") is not False or reviewed_reference.get("c5_reconsideration_ready") is not False:
        failures.append("reviewed_reference_c5_wrong")
    if final_resolution_reference.get("final_resolution_records_count") != 3:
        failures.append("final_resolution_reference_count_wrong")
    if final_resolution_reference.get("all_weak_feedback_resolved") is not True:
        failures.append("final_resolution_reference_not_resolved")
    if resolved_reference.get("weak_feedback_resolved") is not True or resolved_reference.get("resolution_records_emitted_count") != 3:
        failures.append("resolved_reference_wrong")
    if boundary_reference.get("final_resolution_boundary_crossed") is not True:
        failures.append("boundary_reference_wrong")
    if c5_reference.get("c5_opened") is not False or c5_reference.get("c5_reconsideration_ready") is not False:
        failures.append("c5_reference_wrong")
    if c5_reference.get("post_final_resolution_reference_decision_required") is not True:
        failures.append("c5_reference_decision_requirement_missing")
    if post_reference_readiness.get("decision_ready") is not True:
        failures.append("post_reference_readiness_wrong")

    return failures, {
        "decision_summary": decision_summary,
        "reference_receipt": reference_receipt,
        "reviewed_reference": reviewed_reference,
        "resolved_reference": resolved_reference,
        "boundary_reference": boundary_reference,
        "c5_reference": c5_reference,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    execute_pass = not failures
    status = "TYPED_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_EXECUTED_READY_FOR_REVIEW" if execute_pass else "TYPED_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if execute_pass else "REPAIR_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_V0"

    reason_codes = [
        "C5_RECONSIDERATION_EXECUTED",
        "POST_FINAL_RESOLUTION_REFERENCE_DECISION_RECEIPT_CONSUMED",
        "WEAK_FEEDBACK_RESOLVED_REFERENCE_CONFIRMED",
        "FINAL_RESOLUTION_BOUNDARY_REFERENCE_CONFIRMED",
        "FINAL_RESOLUTION_RECORDS_REFERENCE_CONFIRMED",
        "C5_BLOCK_REFERENCE_CONSUMED",
        "C5_RECONSIDERATION_READY_EMITTED",
        "C5_OPENING_DEFERRED_PENDING_EXPLICIT_DECISION",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if execute_pass else failures

    execution_record = {
        "schema_version": "o2_c5_reconsideration_execution_record_v0",
        "execution_status": "C5_RECONSIDERATION_EXECUTED_REVIEW_READY" if execute_pass else "C5_RECONSIDERATION_EXECUTION_FAIL",
        "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "resolution_records_emitted_count": 3,
        "c5_reconsideration_executed": execute_pass,
        "c5_reconsideration_ready": execute_pass,
        "c5_opened": False,
        "review_required_next": execute_pass,
    }

    readiness_record = {
        "schema_version": "o2_c5_reconsideration_ready_record_v0",
        "readiness_status": "C5_RECONSIDERATION_READY_PENDING_REVIEW" if execute_pass else "C5_RECONSIDERATION_NOT_READY",
        "c5_reconsideration_ready": execute_pass,
        "c5_reconsideration_basis": "weak feedback final-resolution closure frozen as reviewed reference",
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "c5_opened": False,
        "live_feedback_audit_executed": False,
        "review_required_next": execute_pass,
    }

    readiness_status = {
        "schema_version": "o2_c5_reconsideration_ready_status_v0",
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW" if execute_pass else "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": execute_pass,
        "c5_opened": False,
        "c5_execution_authorized_next": False,
        "requires_review_before_c5_open_decision": True,
    }

    opening_guard = {
        "schema_version": "o2_c5_opening_guard_v0",
        "guard_status": "C5_OPENING_GUARD_HELD",
        "c5_reconsideration_ready": execute_pass,
        "c5_opened": False,
        "may_open_c5_now": False,
        "requires_explicit_post_review_c5_open_decision": True,
        "live_feedback_audit_executed": False,
    }

    weak_feedback_basis = {
        "schema_version": "o2_c5_reconsideration_weak_feedback_resolution_basis_v0",
        "basis_status": "WEAK_FEEDBACK_RESOLUTION_BASIS_CONFIRMED",
        "source_reference_closure_receipt_id": "01f38b19",
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
    }

    input_confirmation = {
        "schema_version": "o2_c5_reconsideration_input_confirmation_v0",
        "input_status": "POST_FINAL_RESOLUTION_REFERENCE_DECISION_CONSUMED",
        "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "source_reference_closure_receipt_id": "01f38b19",
        "weak_feedback_resolved": True,
        "c5_was_blocked_before_execution": True,
        "c5_reconsideration_ready_before_execution": False,
        "c5_opened_before_execution": False,
    }

    opening_deferred = {
        "schema_version": "o2_c5_opening_deferred_until_explicit_decision_v0",
        "deferred_status": "C5_OPENING_DEFERRED",
        "c5_reconsideration_ready": execute_pass,
        "c5_opened": False,
        "recommended_future_scope": "review C5 reconsideration, then decide whether C5 opening is lawful",
    }

    authority_boundary = {
        "schema_version": "o2_c5_reconsideration_authority_boundary_v0",
        "status": status,
        "may_review_c5_reconsideration_next": execute_pass,
        "may_open_c5_now": False,
        "may_run_live_feedback_audit_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_change_architecture": False,
    }

    classification = {
        "schema_version": "o2_c5_reconsideration_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c5_reconsideration_executed": execute_pass,
        "review_ready": execute_pass,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW" if execute_pass else "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": execute_pass,
        "c5_opened": False,
        "c5_opening_deferred": True,
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
        "schema_version": "o2_c5_reconsideration_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "c5_reconsideration_executed_count": 1 if execute_pass else 0,
        "review_ready_count": 1 if execute_pass else 0,
        "weak_feedback_resolved_count": 1,
        "final_resolution_boundary_crossed_count": 1,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_reconsideration_ready_count": 1 if execute_pass else 0,
        "c5_opened_count": 0,
        "c5_opening_deferred_count": 1,
        "live_feedback_audit_executed_count": 0,
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
        "c5_opened_count",
        "live_feedback_audit_executed_count",
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
        "schema_version": "o2_c5_reconsideration_profile_v0",
        "profile_id": "o2_c5_reconsideration_profile_" + sha8(rollup),
        "status": status,
        "c5_reconsideration_executed": execute_pass,
        "review_ready": execute_pass,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW" if execute_pass else "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": execute_pass,
        "c5_opened": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Review C5 reconsideration next. Do not treat this as C5 opening.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_c5_reconsideration_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C5 reconsideration readiness was emitted after weak-feedback final-resolution reference closure. C5 itself remains unopened pending review and a later explicit opening decision.",
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW" if execute_pass else "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": execute_pass,
        "c5_opened": False,
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_c5_reconsideration_transition_trace_v0",
        "trace": [
            {
                "step": "consume_post_final_reference_decision",
                "question": "is C5 reconsideration authorized next",
                "answer": "yes" if execute_pass else "no",
                "taken": "consume resolved weak-feedback reference",
            },
            {
                "step": "emit_c5_reconsideration_ready",
                "question": "may C5 be reconsidered now that weak feedback is resolved",
                "answer": "yes" if execute_pass else "no",
                "taken": "emit C5 reconsideration ready pending review",
            },
            {
                "step": "hold_c5_opening_guard",
                "question": "does this execution open C5",
                "answer": "no",
                "taken": "defer C5 opening until explicit post-review decision",
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
        (READINESS_RECORD_PATH, readiness_record),
        (READINESS_STATUS_PATH, readiness_status),
        (C5_OPENING_GUARD_PATH, opening_guard),
        (WEAK_FEEDBACK_RESOLUTION_BASIS_PATH, weak_feedback_basis),
        (INPUT_CONFIRMATION_PATH, input_confirmation),
        (OPENING_DEFERRED_PATH, opening_deferred),
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
        "C5_RECONSIDER_0_DECISION_RECEIPT_CONSUMED": SOURCE_DECISION_RECEIPT_PATH.exists(),
        "C5_RECONSIDER_1_WEAK_FEEDBACK_RESOLUTION_BASIS_CONFIRMED": weak_feedback_basis["weak_feedback_resolved"] is True and weak_feedback_basis["resolution_records_emitted_count"] == 3,
        "C5_RECONSIDER_2_C5_BLOCK_REFERENCE_CONSUMED": C5_BLOCK_REFERENCE_PATH.exists(),
        "C5_RECONSIDER_3_C5_RECONSIDERATION_READY_EMITTED": readiness_status["c5_reconsideration_ready"] is True,
        "C5_RECONSIDER_4_C5_NOT_OPENED": readiness_status["c5_opened"] is False and opening_guard["c5_opened"] is False,
        "C5_RECONSIDER_5_C5_OPENING_DEFERRED": opening_deferred["c5_opened"] is False and opening_deferred["deferred_status"] == "C5_OPENING_DEFERRED",
        "C5_RECONSIDER_6_REVIEW_READY": execution_record["review_required_next"] is True,
        "C5_RECONSIDER_7_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "C5_RECONSIDER_8_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "C5_RECONSIDER_9_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C5_RECONSIDER_10_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "C5_RECONSIDER_11_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "c5_reconsideration_ready": execute_pass,
        "c5_opened": False,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_c5_reconsideration_after_weak_feedback_resolution_receipt_v0",
        "receipt_type": "TYPED_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_post_final_resolution_reference_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "machine_readable_o2_c5_reconsideration_after_weak_feedback_resolution_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c5_reconsideration_executed": execute_pass,
            "review_ready": execute_pass,
            "weak_feedback_resolved": True,
            "final_resolution_boundary_crossed": True,
            "final_resolution_records_frozen_count": 3,
            "resolution_records_emitted_count": 3,
            "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW" if execute_pass else "BLOCKED_PENDING_C5_DECISION",
            "c5_reconsideration_ready": execute_pass,
            "c5_opened": False,
            "c5_opening_deferred": True,
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
            "execution_record": rel(EXECUTION_RECORD_PATH),
            "readiness_record": rel(READINESS_RECORD_PATH),
            "readiness_status": rel(READINESS_STATUS_PATH),
            "c5_opening_guard": rel(C5_OPENING_GUARD_PATH),
            "weak_feedback_resolution_basis": rel(WEAK_FEEDBACK_RESOLUTION_BASIS_PATH),
            "input_confirmation": rel(INPUT_CONFIRMATION_PATH),
            "opening_deferred": rel(OPENING_DEFERRED_PATH),
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
    print(f"c5_reconsideration_receipt_id={receipt_id}")
    print(f"c5_reconsideration_receipt_path={rel(receipt_path)}")
    print(f"c5_reconsideration_execution_record_path={rel(EXECUTION_RECORD_PATH)}")
    print(f"c5_reconsideration_ready_status_path={rel(READINESS_STATUS_PATH)}")
    print(f"c5_opening_guard_path={rel(C5_OPENING_GUARD_PATH)}")
    print(f"c5_reconsideration_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c5_reconsideration_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
