#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_V0"
TARGET_UNIT_ID = "observation.o2_c5_opening_after_reconsideration_reference_review.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / C5_OPENING_REVIEW"
MODE = "REVIEW / C5_OPENED_INTEGRITY / NO_LIVE_AUDIT_NO_BUILD_TARGET"
BUILD_MODE = "O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_REVIEW_ONLY"

SOURCE_C5_OPENING_RECEIPT_ID = "4390230f"

SOURCE_C5_OPENING_RECEIPT_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0_receipts/4390230f.json"

EXECUTION_RECORD_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_opening_execution_record_v0.json"
OPEN_STATUS_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_open_status_v0.json"
OPENING_RECORD_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_opening_record_v0.json"
AUTH_CONSUMPTION_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_opening_authorization_consumption_v0.json"
INPUT_CONFIRMATION_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_opening_input_confirmation_v0.json"
RECONSIDERATION_REFERENCE_BASIS_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_opening_reconsideration_reference_basis_v0.json"
LIVE_AUDIT_GUARD_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_live_audit_deferred_guard_v0.json"
BUILD_TARGET_GUARD_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_build_target_guard_v0.json"
OPENING_AUTHORITY_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_opening_authority_boundary_v0.json"
OPENING_CLASSIFICATION_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_opening_classification_v0.json"
OPENING_ROLLUP_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_opening_rollup_v0.json"
OPENING_PROFILE_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_opening_profile_v0.json"
OPENING_REPORT_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_opening_report.json"
OPENING_TRACE_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_opening_transition_trace.json"

SOURCE_POST_C5_DECISION_RECEIPT_PATH = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0_receipts/06d082d7.json"
SOURCE_C5_RECONSIDERATION_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0_receipts/3167d93a.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C5_OPENING_RECEIPT_PATH,
    EXECUTION_RECORD_PATH,
    OPEN_STATUS_PATH,
    OPENING_RECORD_PATH,
    AUTH_CONSUMPTION_PATH,
    INPUT_CONFIRMATION_PATH,
    RECONSIDERATION_REFERENCE_BASIS_PATH,
    LIVE_AUDIT_GUARD_PATH,
    BUILD_TARGET_GUARD_PATH,
    OPENING_AUTHORITY_PATH,
    OPENING_CLASSIFICATION_PATH,
    OPENING_ROLLUP_PATH,
    OPENING_PROFILE_PATH,
    OPENING_REPORT_PATH,
    OPENING_TRACE_PATH,
    SOURCE_POST_C5_DECISION_RECEIPT_PATH,
    SOURCE_C5_RECONSIDERATION_REFERENCE_CLOSURE_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0"
RECEIPT_DIR = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "o2_c5_opening_review_assessment_v0.json"
OPEN_STATUS_REVIEW_PATH = OUT_DIR / "o2_c5_open_status_review_v0.json"
OPENING_RECORD_REVIEW_PATH = OUT_DIR / "o2_c5_opening_record_review_v0.json"
LIVE_AUDIT_GUARD_REVIEW_PATH = OUT_DIR / "o2_c5_live_audit_guard_review_v0.json"
BUILD_TARGET_GUARD_REVIEW_PATH = OUT_DIR / "o2_c5_build_target_guard_review_v0.json"
RECONSIDERATION_BASIS_REVIEW_PATH = OUT_DIR / "o2_c5_opening_reconsideration_basis_review_v0.json"
POST_OPENING_DECISION_CANDIDATE_PATH = OUT_DIR / "o2_post_c5_opening_decision_candidate_v0.json"
REVIEWED_REFERENCE_CANDIDATE_PATH = OUT_DIR / "o2_c5_opening_reviewed_reference_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_c5_opening_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_c5_opening_review_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_c5_opening_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_c5_opening_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_c5_opening_review_report.json"
TRACE_PATH = OUT_DIR / "o2_c5_opening_review_transition_trace.json"

EXPECTED_OPENING_STATUS = "TYPED_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_EXECUTED_OPENED_REVIEW_READY"
EXPECTED_OPENING_STOP = "STOP_TYPED_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_EXECUTED_OPENED_REVIEW_READY"
EXPECTED_OPENING_NEXT = "REVIEW_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_V0"
RECOMMENDED_NEXT = "CLOSE_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_AS_REVIEWED_REFERENCE_V0"

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

    receipt = read_json(SOURCE_C5_OPENING_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_c5_opening_after_reconsideration_reference_summary", {})

    execution_record = read_json(EXECUTION_RECORD_PATH)
    open_status = read_json(OPEN_STATUS_PATH)
    opening_record = read_json(OPENING_RECORD_PATH)
    auth_consumption = read_json(AUTH_CONSUMPTION_PATH)
    input_confirmation = read_json(INPUT_CONFIRMATION_PATH)
    reconsideration_basis = read_json(RECONSIDERATION_REFERENCE_BASIS_PATH)
    live_guard = read_json(LIVE_AUDIT_GUARD_PATH)
    build_guard = read_json(BUILD_TARGET_GUARD_PATH)
    authority = read_json(OPENING_AUTHORITY_PATH)
    classification = read_json(OPENING_CLASSIFICATION_PATH)
    rollup = read_json(OPENING_ROLLUP_PATH)
    profile = read_json(OPENING_PROFILE_PATH)
    report = read_json(OPENING_REPORT_PATH)
    trace = read_json(OPENING_TRACE_PATH)

    post_c5_decision_receipt = read_json(SOURCE_POST_C5_DECISION_RECEIPT_PATH)
    reconsideration_reference_receipt = read_json(SOURCE_C5_RECONSIDERATION_REFERENCE_CLOSURE_RECEIPT_PATH)

    if receipt.get("receipt_id") != SOURCE_C5_OPENING_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_c5_opening_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_OPENING_STOP:
        failures.append("source_c5_opening_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_c5_opening_hidden_next")
    if summary.get("status") != EXPECTED_OPENING_STATUS:
        failures.append(f"source_c5_opening_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_OPENING_NEXT:
        failures.append(f"source_c5_opening_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "c5_opening_executed",
        "review_ready",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
        "c5_reconsideration_ready",
        "c5_open_decision_candidate_ready",
        "c5_opened",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    if summary.get("c5_feedback_readiness") != "C5_OPENED_PENDING_REVIEW":
        failures.append("summary_c5_readiness_wrong")
    if summary.get("final_resolution_records_frozen_count") != 3 or summary.get("resolution_records_emitted_count") != 3:
        failures.append("summary_resolution_counts_wrong")

    for key in [
        "live_feedback_audit_executed",
        "c5_live_branch_executed",
        "target_selected_for_build",
        "repair_applied",
        "retry_executed",
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

    if execution_record.get("execution_status") != "C5_OPENING_EXECUTED_REVIEW_READY":
        failures.append("execution_record_status_wrong")
    if execution_record.get("c5_opening_executed") is not True or execution_record.get("c5_opened") is not True:
        failures.append("execution_record_not_opened")
    if execution_record.get("live_feedback_audit_executed") is not False or execution_record.get("target_selected_for_build") is not False:
        failures.append("execution_record_guard_wrong")
    if execution_record.get("review_required_next") is not True:
        failures.append("execution_record_review_not_required")

    if open_status.get("c5_feedback_readiness") != "C5_OPENED_PENDING_REVIEW" or open_status.get("c5_opened") is not True:
        failures.append("open_status_wrong")
    if open_status.get("live_feedback_audit_executed") is not False or open_status.get("c5_live_branch_executed") is not False:
        failures.append("open_status_live_audit_wrong")

    if opening_record.get("opening_status") != "C5_OPENED_FOR_REVIEW" or opening_record.get("c5_opened") is not True:
        failures.append("opening_record_wrong")
    if auth_consumption.get("authorization_consumed") is not True:
        failures.append("auth_consumption_wrong")
    if input_confirmation.get("c5_opened_before_execution") is not False:
        failures.append("input_confirmation_preopened")
    if reconsideration_basis.get("c5_reconsideration_ready") is not True or reconsideration_basis.get("c5_open_decision_candidate_ready") is not True:
        failures.append("reconsideration_basis_wrong")
    if live_guard.get("live_feedback_audit_executed") is not False or live_guard.get("may_run_live_feedback_audit_now") is not False:
        failures.append("live_guard_wrong")
    if build_guard.get("target_selected_for_build") is not False or build_guard.get("runtime_patch_applied") is not False:
        failures.append("build_guard_wrong")
    if authority.get("may_review_c5_opening_next") is not True:
        failures.append("authority_no_review")
    if authority.get("may_run_live_feedback_audit_now") is not False or authority.get("may_select_build_target_now") is not False:
        failures.append("authority_allows_live_or_build")
    if classification.get("recommended_next") != EXPECTED_OPENING_NEXT:
        failures.append("classification_next_wrong")
    if rollup.get("c5_opening_executed_count") != 1 or rollup.get("c5_opened_count") != 1:
        failures.append("rollup_opening_wrong")
    if rollup.get("live_feedback_audit_executed_count") != 0 or rollup.get("c5_live_branch_executed_count") != 0:
        failures.append("rollup_live_audit_wrong")
    if rollup.get("target_selected_for_build_count") != 0:
        failures.append("rollup_build_target_wrong")
    if profile.get("c5_opened") is not True or profile.get("live_feedback_audit_executed") is not False:
        failures.append("profile_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_OPENING_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_OPENING_STOP:
        failures.append("trace_stop_wrong")

    if post_c5_decision_receipt.get("receipt_id") != "06d082d7" or post_c5_decision_receipt.get("gate") != "PASS":
        failures.append("post_c5_decision_receipt_wrong")
    if reconsideration_reference_receipt.get("receipt_id") != "3167d93a" or reconsideration_reference_receipt.get("gate") != "PASS":
        failures.append("reconsideration_reference_receipt_wrong")

    return failures, {
        "summary": summary,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, _ = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    review_pass = not failures
    status = "TYPED_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_REVIEWED_CLEAN_CLOSE_READY" if review_pass else "TYPED_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_REVIEW_V0"

    reason_codes = [
        "C5_OPENING_REVIEW_COMPLETE",
        "C5_OPENING_RECEIPT_CONSUMED",
        "C5_OPEN_STATUS_CONFIRMED",
        "C5_OPENING_RECORD_CONFIRMED",
        "LIVE_AUDIT_GUARD_CONFIRMED",
        "BUILD_TARGET_GUARD_CONFIRMED",
        "RECONSIDERATION_REFERENCE_BASIS_CONFIRMED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_BUILD_TARGET_SELECTED",
        "C5_OPENING_CLOSE_CANDIDATE_READY",
        "POST_C5_OPENING_DECISION_CANDIDATE_READY",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if review_pass else failures

    review_assessment = {
        "schema_version": "o2_c5_opening_review_assessment_v0",
        "review_status": status,
        "review_complete": review_pass,
        "review_pass": review_pass,
        "source_c5_opening_receipt_id": SOURCE_C5_OPENING_RECEIPT_ID,
        "c5_opening_integrity_validated": review_pass,
        "close_candidate_ready": review_pass,
        "recommended_next": recommended_next,
    }

    open_status_review = {
        "schema_version": "o2_c5_open_status_review_v0",
        "review_status": "C5_OPEN_STATUS_REVIEW_PASS" if review_pass else "C5_OPEN_STATUS_REVIEW_FAIL",
        "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW",
        "c5_opened": True,
        "c5_opening_executed": True,
        "live_feedback_audit_executed": False,
        "target_selected_for_build": False,
    }

    opening_record_review = {
        "schema_version": "o2_c5_opening_record_review_v0",
        "review_status": "C5_OPENING_RECORD_REVIEW_PASS" if review_pass else "C5_OPENING_RECORD_REVIEW_FAIL",
        "opening_status": "C5_OPENED_FOR_REVIEW",
        "c5_opened": True,
        "opening_does_not_mean_live_audit": True,
        "opening_does_not_mean_build_target": True,
    }

    live_audit_guard_review = {
        "schema_version": "o2_c5_live_audit_guard_review_v0",
        "review_status": "LIVE_AUDIT_GUARD_REVIEW_PASS" if review_pass else "LIVE_AUDIT_GUARD_REVIEW_FAIL",
        "guard_status": "LIVE_AUDIT_NOT_EXECUTED",
        "c5_opened": True,
        "live_feedback_audit_executed": False,
        "c5_live_branch_executed": False,
        "requires_explicit_post_opening_reference_decision": True,
    }

    build_target_guard_review = {
        "schema_version": "o2_c5_build_target_guard_review_v0",
        "review_status": "BUILD_TARGET_GUARD_REVIEW_PASS" if review_pass else "BUILD_TARGET_GUARD_REVIEW_FAIL",
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "architecture_change": False,
    }

    reconsideration_basis_review = {
        "schema_version": "o2_c5_opening_reconsideration_basis_review_v0",
        "review_status": "RECONSIDERATION_REFERENCE_BASIS_REVIEW_PASS" if review_pass else "RECONSIDERATION_REFERENCE_BASIS_REVIEW_FAIL",
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_reconsideration_ready": True,
        "c5_open_decision_candidate_ready": True,
    }

    post_opening_decision_candidate = {
        "schema_version": "o2_post_c5_opening_decision_candidate_v0",
        "candidate_status": "POST_C5_OPENING_DECISION_CANDIDATE_READY_AFTER_REVIEWED_OPENING" if review_pass else "POST_C5_OPENING_DECISION_CANDIDATE_NOT_READY",
        "c5_opening_review_pass": review_pass,
        "c5_opened": True,
        "live_feedback_audit_executed": False,
        "target_selected_for_build": False,
        "candidate_question": "whether to select live C5 audit / next C5 handling after reviewed opening reference exists",
    }

    reviewed_reference_candidate = {
        "schema_version": "o2_c5_opening_reviewed_reference_candidate_v0",
        "candidate_status": "C5_OPENING_CLOSE_READY_AS_REVIEWED_REFERENCE" if review_pass else "C5_OPENING_NOT_CLOSE_READY",
        "review_pass": review_pass,
        "close_candidate_ready": review_pass,
        "closure_meaning": "Close C5 opening as reviewed reference.",
        "closure_does_not_mean": [
            "live feedback audit executed",
            "C5 build target selected",
            "runtime patched",
            "source mutated",
        ],
        "recommended_next": recommended_next,
    }

    authority_boundary = {
        "schema_version": "o2_c5_opening_review_authority_boundary_v0",
        "status": status,
        "may_close_c5_opening_as_reviewed_reference_next": review_pass,
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
        "schema_version": "o2_c5_opening_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c5_opening_review_complete": review_pass,
        "c5_opening_review_pass": review_pass,
        "c5_opening_integrity_validated": review_pass,
        "close_candidate_ready": review_pass,
        "post_c5_opening_decision_candidate_ready": review_pass,
        "c5_opening_executed": True,
        "review_ready": True,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW",
        "c5_opened": True,
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
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "o2_c5_opening_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "c5_opening_integrity_validated_count": 1 if review_pass else 0,
        "close_candidate_ready_count": 1 if review_pass else 0,
        "post_c5_opening_decision_candidate_ready_count": 1 if review_pass else 0,
        "weak_feedback_resolved_count": 1,
        "final_resolution_boundary_crossed_count": 1,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_opening_executed_count": 1,
        "c5_opened_count": 1,
        "live_feedback_audit_executed_count": 0,
        "c5_live_branch_executed_count": 0,
        "target_selected_for_build_count": 0,
        "repair_applied_count": 0,
        "retry_executed_count": 0,
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
        "target_selected_for_build_count",
        "repair_applied_count",
        "retry_executed_count",
        "runtime_patch_count",
        "source_mutated_count",
        "prior_receipt_mutated_count",
        "architecture_change_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "o2_c5_opening_review_profile_v0",
        "profile_id": "o2_c5_opening_review_profile_" + sha8(rollup),
        "status": status,
        "c5_opening_review_pass": review_pass,
        "c5_opening_integrity_validated": review_pass,
        "close_candidate_ready": review_pass,
        "post_c5_opening_decision_candidate_ready": review_pass,
        "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW",
        "c5_opened": True,
        "live_feedback_audit_executed": False,
        "target_selected_for_build": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Close C5 opening as reviewed reference. Live audit remains a later explicit decision.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_c5_opening_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C5 opening reviewed clean: C5 is opened pending review, but live audit and build target selection did not run.",
        "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW",
        "c5_opened": True,
        "live_feedback_audit_executed": False,
        "target_selected_for_build": False,
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_c5_opening_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c5_opening_execution",
                "question": "did C5 opening execute cleanly",
                "answer": "yes" if review_pass else "no",
                "taken": "review C5 opened status and guards",
            },
            {
                "step": "verify_c5_opened_for_review",
                "question": "is C5 opened pending review",
                "answer": "yes" if review_pass else "no",
                "taken": "confirm opened status",
            },
            {
                "step": "verify_no_live_audit_or_build",
                "question": "did live audit or build target run",
                "answer": "no",
                "taken": "emit close-ready reviewed reference candidate",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (REVIEW_ASSESSMENT_PATH, review_assessment),
        (OPEN_STATUS_REVIEW_PATH, open_status_review),
        (OPENING_RECORD_REVIEW_PATH, opening_record_review),
        (LIVE_AUDIT_GUARD_REVIEW_PATH, live_audit_guard_review),
        (BUILD_TARGET_GUARD_REVIEW_PATH, build_target_guard_review),
        (RECONSIDERATION_BASIS_REVIEW_PATH, reconsideration_basis_review),
        (POST_OPENING_DECISION_CANDIDATE_PATH, post_opening_decision_candidate),
        (REVIEWED_REFERENCE_CANDIDATE_PATH, reviewed_reference_candidate),
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
        "C5_OPEN_REVIEW_0_SOURCE_C5_OPENING_RECEIPT_CONSUMED": SOURCE_C5_OPENING_RECEIPT_PATH.exists(),
        "C5_OPEN_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "C5_OPEN_REVIEW_2_OPEN_STATUS_CONFIRMED": open_status_review["c5_opened"] is True and open_status_review["c5_feedback_readiness"] == "C5_OPENED_PENDING_REVIEW",
        "C5_OPEN_REVIEW_3_OPENING_RECORD_CONFIRMED": opening_record_review["c5_opened"] is True,
        "C5_OPEN_REVIEW_4_NO_LIVE_AUDIT_CONFIRMED": live_audit_guard_review["live_feedback_audit_executed"] is False and live_audit_guard_review["c5_live_branch_executed"] is False,
        "C5_OPEN_REVIEW_5_NO_BUILD_TARGET_CONFIRMED": build_target_guard_review["target_selected_for_build"] is False,
        "C5_OPEN_REVIEW_6_RECONSIDERATION_BASIS_CONFIRMED": reconsideration_basis_review["c5_reconsideration_ready"] is True and reconsideration_basis_review["c5_open_decision_candidate_ready"] is True,
        "C5_OPEN_REVIEW_7_POST_OPENING_DECISION_CANDIDATE_READY": post_opening_decision_candidate["candidate_status"] == "POST_C5_OPENING_DECISION_CANDIDATE_READY_AFTER_REVIEWED_OPENING",
        "C5_OPEN_REVIEW_8_CLOSE_CANDIDATE_READY": reviewed_reference_candidate["close_candidate_ready"] is True,
        "C5_OPEN_REVIEW_9_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "C5_OPEN_REVIEW_10_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C5_OPEN_REVIEW_11_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "C5_OPEN_REVIEW_12_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "c5_opened": True,
        "live_feedback_audit_executed": False,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_c5_opening_after_reconsideration_reference_review_receipt_v0",
        "receipt_type": "TYPED_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c5_opening_receipt_id": SOURCE_C5_OPENING_RECEIPT_ID,
        "machine_readable_o2_c5_opening_after_reconsideration_reference_review_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c5_opening_review_complete": review_pass,
            "c5_opening_review_pass": review_pass,
            "c5_opening_integrity_validated": review_pass,
            "close_candidate_ready": review_pass,
            "post_c5_opening_decision_candidate_ready": review_pass,
            "c5_opening_executed": True,
            "review_ready": True,
            "weak_feedback_resolved": True,
            "final_resolution_boundary_crossed": True,
            "final_resolution_records_frozen_count": 3,
            "resolution_records_emitted_count": 3,
            "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW",
            "c5_opened": True,
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
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "open_status_review": rel(OPEN_STATUS_REVIEW_PATH),
            "opening_record_review": rel(OPENING_RECORD_REVIEW_PATH),
            "live_audit_guard_review": rel(LIVE_AUDIT_GUARD_REVIEW_PATH),
            "build_target_guard_review": rel(BUILD_TARGET_GUARD_REVIEW_PATH),
            "reconsideration_basis_review": rel(RECONSIDERATION_BASIS_REVIEW_PATH),
            "post_opening_decision_candidate": rel(POST_OPENING_DECISION_CANDIDATE_PATH),
            "reviewed_reference_candidate": rel(REVIEWED_REFERENCE_CANDIDATE_PATH),
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
    print(f"c5_opening_review_receipt_id={receipt_id}")
    print(f"c5_opening_review_receipt_path={rel(receipt_path)}")
    print(f"c5_opening_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"c5_open_status_review_path={rel(OPEN_STATUS_REVIEW_PATH)}")
    print(f"c5_live_audit_guard_review_path={rel(LIVE_AUDIT_GUARD_REVIEW_PATH)}")
    print(f"post_c5_opening_decision_candidate_path={rel(POST_OPENING_DECISION_CANDIDATE_PATH)}")
    print(f"c5_opening_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c5_opening_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
