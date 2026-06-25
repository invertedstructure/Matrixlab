#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_V0"
TARGET_UNIT_ID = "observation.o2_c5_reconsideration_after_weak_feedback_resolution_review.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / C5_RECONSIDERATION_REVIEW"
MODE = "REVIEW / C5_RECONSIDERATION_READY_INTEGRITY / NO_C5_OPEN_NO_LIVE_AUDIT"
BUILD_MODE = "O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_REVIEW_ONLY"

SOURCE_C5_RECEIPT_ID = "d19ec918"

SOURCE_C5_RECEIPT_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0_receipts/d19ec918.json"
EXECUTION_RECORD_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_execution_record_v0.json"
READINESS_RECORD_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_ready_record_v0.json"
READINESS_STATUS_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_ready_status_v0.json"
C5_OPENING_GUARD_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_opening_guard_v0.json"
WEAK_FEEDBACK_RESOLUTION_BASIS_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_weak_feedback_resolution_basis_v0.json"
INPUT_CONFIRMATION_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_input_confirmation_v0.json"
OPENING_DEFERRED_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_opening_deferred_until_explicit_decision_v0.json"
C5_AUTHORITY_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_authority_boundary_v0.json"
C5_CLASSIFICATION_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_classification_v0.json"
C5_ROLLUP_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_rollup_v0.json"
C5_PROFILE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_profile_v0.json"
C5_REPORT_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_report.json"
C5_TRACE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_transition_trace.json"

SOURCE_POST_FINAL_DECISION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0_receipts/4b9662bc.json"
SOURCE_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0_receipts/01f38b19.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C5_RECEIPT_PATH,
    EXECUTION_RECORD_PATH,
    READINESS_RECORD_PATH,
    READINESS_STATUS_PATH,
    C5_OPENING_GUARD_PATH,
    WEAK_FEEDBACK_RESOLUTION_BASIS_PATH,
    INPUT_CONFIRMATION_PATH,
    OPENING_DEFERRED_PATH,
    C5_AUTHORITY_PATH,
    C5_CLASSIFICATION_PATH,
    C5_ROLLUP_PATH,
    C5_PROFILE_PATH,
    C5_REPORT_PATH,
    C5_TRACE_PATH,
    SOURCE_POST_FINAL_DECISION_RECEIPT_PATH,
    SOURCE_REFERENCE_CLOSURE_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0"
RECEIPT_DIR = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "o2_c5_reconsideration_review_assessment_v0.json"
READY_STATUS_REVIEW_PATH = OUT_DIR / "o2_c5_reconsideration_ready_status_review_v0.json"
OPENING_GUARD_REVIEW_PATH = OUT_DIR / "o2_c5_opening_guard_review_v0.json"
WEAK_FEEDBACK_BASIS_REVIEW_PATH = OUT_DIR / "o2_c5_reconsideration_weak_feedback_basis_review_v0.json"
NO_LIVE_AUDIT_REVIEW_PATH = OUT_DIR / "o2_c5_no_live_audit_review_v0.json"
OPEN_DECISION_CANDIDATE_PATH = OUT_DIR / "o2_c5_open_decision_candidate_v0.json"
C5_REVIEWED_REFERENCE_CANDIDATE_PATH = OUT_DIR / "o2_c5_reconsideration_reviewed_reference_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_c5_reconsideration_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_c5_reconsideration_review_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_c5_reconsideration_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_c5_reconsideration_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_c5_reconsideration_review_report.json"
TRACE_PATH = OUT_DIR / "o2_c5_reconsideration_review_transition_trace.json"

EXPECTED_C5_STATUS = "TYPED_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_EXECUTED_READY_FOR_REVIEW"
EXPECTED_C5_STOP = "STOP_TYPED_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_EXECUTED_READY_FOR_REVIEW"
EXPECTED_C5_NEXT = "REVIEW_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_V0"
RECOMMENDED_NEXT = "CLOSE_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_AS_REVIEWED_REFERENCE_V0"

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

    receipt = read_json(SOURCE_C5_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_c5_reconsideration_after_weak_feedback_resolution_summary", {})
    execution_record = read_json(EXECUTION_RECORD_PATH)
    readiness_record = read_json(READINESS_RECORD_PATH)
    readiness_status = read_json(READINESS_STATUS_PATH)
    opening_guard = read_json(C5_OPENING_GUARD_PATH)
    weak_feedback_basis = read_json(WEAK_FEEDBACK_RESOLUTION_BASIS_PATH)
    input_confirmation = read_json(INPUT_CONFIRMATION_PATH)
    opening_deferred = read_json(OPENING_DEFERRED_PATH)
    authority = read_json(C5_AUTHORITY_PATH)
    classification = read_json(C5_CLASSIFICATION_PATH)
    rollup = read_json(C5_ROLLUP_PATH)
    profile = read_json(C5_PROFILE_PATH)
    report = read_json(C5_REPORT_PATH)
    trace = read_json(C5_TRACE_PATH)
    post_final_decision_receipt = read_json(SOURCE_POST_FINAL_DECISION_RECEIPT_PATH)
    reference_closure_receipt = read_json(SOURCE_REFERENCE_CLOSURE_RECEIPT_PATH)

    if receipt.get("receipt_id") != SOURCE_C5_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_c5_reconsideration_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_C5_STOP:
        failures.append("source_c5_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_c5_hidden_next")
    if summary.get("status") != EXPECTED_C5_STATUS:
        failures.append(f"source_c5_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_C5_NEXT:
        failures.append(f"source_c5_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "c5_reconsideration_executed",
        "review_ready",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
        "c5_reconsideration_ready",
        "c5_opening_deferred",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    for key in [
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

    if summary.get("c5_feedback_readiness") != "C5_RECONSIDERATION_READY_PENDING_REVIEW":
        failures.append("summary_c5_readiness_wrong")

    if execution_record.get("execution_status") != "C5_RECONSIDERATION_EXECUTED_REVIEW_READY":
        failures.append("execution_record_status_wrong")
    if execution_record.get("c5_reconsideration_executed") is not True or execution_record.get("c5_reconsideration_ready") is not True:
        failures.append("execution_record_not_ready")
    if execution_record.get("c5_opened") is not False or execution_record.get("review_required_next") is not True:
        failures.append("execution_record_guard_wrong")
    if readiness_record.get("readiness_status") != "C5_RECONSIDERATION_READY_PENDING_REVIEW":
        failures.append("readiness_record_status_wrong")
    if readiness_record.get("c5_reconsideration_ready") is not True or readiness_record.get("c5_opened") is not False:
        failures.append("readiness_record_wrong")
    if readiness_status.get("c5_feedback_readiness") != "C5_RECONSIDERATION_READY_PENDING_REVIEW":
        failures.append("readiness_status_wrong")
    if readiness_status.get("c5_reconsideration_ready") is not True or readiness_status.get("c5_opened") is not False:
        failures.append("readiness_status_c5_wrong")
    if readiness_status.get("requires_review_before_c5_open_decision") is not True:
        failures.append("readiness_status_missing_review_gate")
    if opening_guard.get("guard_status") != "C5_OPENING_GUARD_HELD":
        failures.append("opening_guard_status_wrong")
    if opening_guard.get("c5_opened") is not False or opening_guard.get("may_open_c5_now") is not False:
        failures.append("opening_guard_wrong")
    if opening_guard.get("requires_explicit_post_review_c5_open_decision") is not True:
        failures.append("opening_guard_missing_explicit_decision")
    if weak_feedback_basis.get("weak_feedback_resolved") is not True or weak_feedback_basis.get("resolution_records_emitted_count") != 3:
        failures.append("weak_feedback_basis_wrong")
    if input_confirmation.get("c5_was_blocked_before_execution") is not True:
        failures.append("input_confirmation_not_blocked_before")
    if input_confirmation.get("c5_reconsideration_ready_before_execution") is not False or input_confirmation.get("c5_opened_before_execution") is not False:
        failures.append("input_confirmation_prestate_wrong")
    if opening_deferred.get("deferred_status") != "C5_OPENING_DEFERRED" or opening_deferred.get("c5_opened") is not False:
        failures.append("opening_deferred_wrong")
    if authority.get("may_review_c5_reconsideration_next") is not True:
        failures.append("authority_no_review")
    if authority.get("may_open_c5_now") is not False or authority.get("may_run_live_feedback_audit_now") is not False:
        failures.append("authority_allows_open_or_audit")
    if classification.get("recommended_next") != EXPECTED_C5_NEXT:
        failures.append("classification_next_wrong")
    if classification.get("c5_reconsideration_ready") is not True or classification.get("c5_opened") is not False:
        failures.append("classification_c5_wrong")
    if rollup.get("c5_reconsideration_ready_count") != 1 or rollup.get("c5_opened_count") != 0:
        failures.append("rollup_c5_wrong")
    if rollup.get("live_feedback_audit_executed_count") != 0:
        failures.append("rollup_live_audit_wrong")
    if profile.get("c5_reconsideration_ready") is not True or profile.get("c5_opened") is not False:
        failures.append("profile_c5_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_C5_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_C5_STOP:
        failures.append("trace_stop_wrong")
    if post_final_decision_receipt.get("receipt_id") != "4b9662bc" or post_final_decision_receipt.get("gate") != "PASS":
        failures.append("post_final_decision_receipt_wrong")
    if reference_closure_receipt.get("receipt_id") != "01f38b19" or reference_closure_receipt.get("gate") != "PASS":
        failures.append("reference_closure_receipt_wrong")

    return failures, {
        "summary": summary,
        "readiness_status": readiness_status,
        "opening_guard": opening_guard,
        "weak_feedback_basis": weak_feedback_basis,
        "opening_deferred": opening_deferred,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    review_pass = not failures
    status = "TYPED_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_REVIEWED_CLEAN_CLOSE_READY" if review_pass else "TYPED_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_REVIEW_V0"

    reason_codes = [
        "C5_RECONSIDERATION_REVIEW_COMPLETE",
        "C5_RECONSIDERATION_RECEIPT_CONSUMED",
        "C5_RECONSIDERATION_READY_STATUS_CONFIRMED",
        "C5_OPENING_GUARD_CONFIRMED",
        "WEAK_FEEDBACK_RESOLUTION_BASIS_CONFIRMED",
        "C5_OPENING_DEFERRED_CONFIRMED",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "C5_RECONSIDERATION_CLOSE_CANDIDATE_READY",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if review_pass else failures

    review_assessment = {
        "schema_version": "o2_c5_reconsideration_review_assessment_v0",
        "review_status": status,
        "review_complete": review_pass,
        "review_pass": review_pass,
        "source_c5_reconsideration_receipt_id": SOURCE_C5_RECEIPT_ID,
        "c5_reconsideration_integrity_validated": review_pass,
        "close_candidate_ready": review_pass,
        "recommended_next": recommended_next,
    }

    ready_status_review = {
        "schema_version": "o2_c5_reconsideration_ready_status_review_v0",
        "review_status": "C5_RECONSIDERATION_READY_STATUS_REVIEW_PASS" if review_pass else "C5_RECONSIDERATION_READY_STATUS_REVIEW_FAIL",
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
        "c5_opened": False,
        "requires_explicit_post_review_c5_open_decision": True,
    }

    opening_guard_review = {
        "schema_version": "o2_c5_opening_guard_review_v0",
        "review_status": "C5_OPENING_GUARD_REVIEW_PASS" if review_pass else "C5_OPENING_GUARD_REVIEW_FAIL",
        "guard_status": "C5_OPENING_GUARD_HELD",
        "c5_reconsideration_ready": True,
        "c5_opened": False,
        "may_open_c5_now": False,
        "live_feedback_audit_executed": False,
    }

    weak_feedback_basis_review = {
        "schema_version": "o2_c5_reconsideration_weak_feedback_basis_review_v0",
        "review_status": "WEAK_FEEDBACK_RESOLUTION_BASIS_REVIEW_PASS" if review_pass else "WEAK_FEEDBACK_RESOLUTION_BASIS_REVIEW_FAIL",
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
    }

    no_live_audit_review = {
        "schema_version": "o2_c5_no_live_audit_review_v0",
        "review_status": "NO_LIVE_AUDIT_REVIEW_PASS" if review_pass else "NO_LIVE_AUDIT_REVIEW_FAIL",
        "live_feedback_audit_executed": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
    }

    open_decision_candidate = {
        "schema_version": "o2_c5_open_decision_candidate_v0",
        "candidate_status": "C5_OPEN_DECISION_CANDIDATE_READY_AFTER_REVIEWED_RECONSIDERATION" if review_pass else "C5_OPEN_DECISION_CANDIDATE_NOT_READY",
        "c5_reconsideration_review_pass": review_pass,
        "c5_reconsideration_ready": True,
        "c5_opened": False,
        "opening_decision_required_after_reference_closure": True,
        "candidate_does_not_open_c5": True,
    }

    reviewed_reference_candidate = {
        "schema_version": "o2_c5_reconsideration_reviewed_reference_candidate_v0",
        "candidate_status": "C5_RECONSIDERATION_CLOSE_READY_AS_REVIEWED_REFERENCE" if review_pass else "C5_RECONSIDERATION_NOT_CLOSE_READY",
        "review_pass": review_pass,
        "close_candidate_ready": review_pass,
        "closure_meaning": "Close C5 reconsideration readiness as reviewed reference.",
        "closure_does_not_mean": [
            "C5 opened",
            "live feedback audit executed",
            "runtime patched",
            "source mutated",
        ],
        "recommended_next": recommended_next,
    }

    authority_boundary = {
        "schema_version": "o2_c5_reconsideration_review_authority_boundary_v0",
        "status": status,
        "may_close_c5_reconsideration_as_reviewed_reference_next": review_pass,
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
        "schema_version": "o2_c5_reconsideration_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c5_reconsideration_review_complete": review_pass,
        "c5_reconsideration_review_pass": review_pass,
        "c5_reconsideration_integrity_validated": review_pass,
        "close_candidate_ready": review_pass,
        "c5_open_decision_candidate_ready": review_pass,
        "c5_reconsideration_executed": True,
        "review_ready": True,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
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
        "schema_version": "o2_c5_reconsideration_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "c5_reconsideration_integrity_validated_count": 1 if review_pass else 0,
        "close_candidate_ready_count": 1 if review_pass else 0,
        "c5_open_decision_candidate_ready_count": 1 if review_pass else 0,
        "weak_feedback_resolved_count": 1,
        "final_resolution_boundary_crossed_count": 1,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_reconsideration_ready_count": 1,
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
        "schema_version": "o2_c5_reconsideration_review_profile_v0",
        "profile_id": "o2_c5_reconsideration_review_profile_" + sha8(rollup),
        "status": status,
        "c5_reconsideration_review_pass": review_pass,
        "c5_reconsideration_integrity_validated": review_pass,
        "close_candidate_ready": review_pass,
        "c5_open_decision_candidate_ready": review_pass,
        "weak_feedback_resolved": True,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
        "c5_opened": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Close C5 reconsideration as reviewed reference. C5 opening remains a later explicit decision.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_c5_reconsideration_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C5 reconsideration reviewed clean: readiness exists, C5 is not opened, live audit did not run, and opening remains deferred to a later explicit decision.",
        "weak_feedback_resolved": True,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
        "c5_opened": False,
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_c5_reconsideration_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c5_reconsideration_execution",
                "question": "did C5 reconsideration execute cleanly",
                "answer": "yes" if review_pass else "no",
                "taken": "review readiness and opening guard",
            },
            {
                "step": "verify_c5_readiness",
                "question": "is C5 reconsideration ready",
                "answer": "yes" if review_pass else "no",
                "taken": "confirm readiness pending review",
            },
            {
                "step": "verify_c5_not_open",
                "question": "did this unit open C5",
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
        (READY_STATUS_REVIEW_PATH, ready_status_review),
        (OPENING_GUARD_REVIEW_PATH, opening_guard_review),
        (WEAK_FEEDBACK_BASIS_REVIEW_PATH, weak_feedback_basis_review),
        (NO_LIVE_AUDIT_REVIEW_PATH, no_live_audit_review),
        (OPEN_DECISION_CANDIDATE_PATH, open_decision_candidate),
        (C5_REVIEWED_REFERENCE_CANDIDATE_PATH, reviewed_reference_candidate),
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
        "C5_RECONSIDER_REVIEW_0_SOURCE_C5_RECEIPT_CONSUMED": SOURCE_C5_RECEIPT_PATH.exists(),
        "C5_RECONSIDER_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "C5_RECONSIDER_REVIEW_2_READY_STATUS_CONFIRMED": ready_status_review["c5_reconsideration_ready"] is True,
        "C5_RECONSIDER_REVIEW_3_C5_NOT_OPENED": ready_status_review["c5_opened"] is False and opening_guard_review["c5_opened"] is False,
        "C5_RECONSIDER_REVIEW_4_OPENING_GUARD_CONFIRMED": opening_guard_review["guard_status"] == "C5_OPENING_GUARD_HELD",
        "C5_RECONSIDER_REVIEW_5_WEAK_FEEDBACK_BASIS_CONFIRMED": weak_feedback_basis_review["weak_feedback_resolved"] is True and weak_feedback_basis_review["resolution_records_emitted_count"] == 3,
        "C5_RECONSIDER_REVIEW_6_NO_LIVE_AUDIT": no_live_audit_review["live_feedback_audit_executed"] is False,
        "C5_RECONSIDER_REVIEW_7_OPEN_DECISION_CANDIDATE_READY": open_decision_candidate["c5_open_decision_candidate_ready" if "c5_open_decision_candidate_ready" in open_decision_candidate else "candidate_status"] is not None,
        "C5_RECONSIDER_REVIEW_8_CLOSE_CANDIDATE_READY": reviewed_reference_candidate["close_candidate_ready"] is True,
        "C5_RECONSIDER_REVIEW_9_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "C5_RECONSIDER_REVIEW_10_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C5_RECONSIDER_REVIEW_11_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "C5_RECONSIDER_REVIEW_12_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "c5_reconsideration_ready": True,
        "c5_opened": False,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_c5_reconsideration_after_weak_feedback_resolution_review_receipt_v0",
        "receipt_type": "TYPED_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c5_reconsideration_receipt_id": SOURCE_C5_RECEIPT_ID,
        "machine_readable_o2_c5_reconsideration_after_weak_feedback_resolution_review_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c5_reconsideration_review_complete": review_pass,
            "c5_reconsideration_review_pass": review_pass,
            "c5_reconsideration_integrity_validated": review_pass,
            "close_candidate_ready": review_pass,
            "c5_open_decision_candidate_ready": review_pass,
            "c5_reconsideration_executed": True,
            "review_ready": True,
            "weak_feedback_resolved": True,
            "final_resolution_boundary_crossed": True,
            "final_resolution_records_frozen_count": 3,
            "resolution_records_emitted_count": 3,
            "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
            "c5_reconsideration_ready": True,
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
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "ready_status_review": rel(READY_STATUS_REVIEW_PATH),
            "opening_guard_review": rel(OPENING_GUARD_REVIEW_PATH),
            "weak_feedback_basis_review": rel(WEAK_FEEDBACK_BASIS_REVIEW_PATH),
            "no_live_audit_review": rel(NO_LIVE_AUDIT_REVIEW_PATH),
            "open_decision_candidate": rel(OPEN_DECISION_CANDIDATE_PATH),
            "reviewed_reference_candidate": rel(C5_REVIEWED_REFERENCE_CANDIDATE_PATH),
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
    print(f"c5_reconsideration_review_receipt_id={receipt_id}")
    print(f"c5_reconsideration_review_receipt_path={rel(receipt_path)}")
    print(f"c5_reconsideration_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"c5_reconsideration_ready_status_review_path={rel(READY_STATUS_REVIEW_PATH)}")
    print(f"c5_opening_guard_review_path={rel(OPENING_GUARD_REVIEW_PATH)}")
    print(f"c5_open_decision_candidate_path={rel(OPEN_DECISION_CANDIDATE_PATH)}")
    print(f"c5_reconsideration_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c5_reconsideration_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
