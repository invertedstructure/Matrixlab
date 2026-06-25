#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "observation.o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / C5_RECONSIDERATION_REFERENCE_CLOSURE"
MODE = "CLOSE / FREEZE_C5_RECONSIDERATION_AS_REVIEWED_REFERENCE / C5_OPEN_DECISION_PENDING"
BUILD_MODE = "O2_C5_RECONSIDERATION_REFERENCE_CLOSURE_ONLY"

SOURCE_REVIEW_RECEIPT_ID = "41999f02"

SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0_receipts/41999f02.json"
REVIEW_ASSESSMENT_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0/o2_c5_reconsideration_review_assessment_v0.json"
READY_STATUS_REVIEW_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0/o2_c5_reconsideration_ready_status_review_v0.json"
OPENING_GUARD_REVIEW_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0/o2_c5_opening_guard_review_v0.json"
WEAK_FEEDBACK_BASIS_REVIEW_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0/o2_c5_reconsideration_weak_feedback_basis_review_v0.json"
NO_LIVE_AUDIT_REVIEW_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0/o2_c5_no_live_audit_review_v0.json"
OPEN_DECISION_CANDIDATE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0/o2_c5_open_decision_candidate_v0.json"
REVIEWED_REFERENCE_CANDIDATE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0/o2_c5_reconsideration_reviewed_reference_candidate_v0.json"
REVIEW_AUTHORITY_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0/o2_c5_reconsideration_review_authority_boundary_v0.json"
REVIEW_CLASSIFICATION_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0/o2_c5_reconsideration_review_classification_v0.json"
REVIEW_ROLLUP_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0/o2_c5_reconsideration_review_rollup_v0.json"
REVIEW_PROFILE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0/o2_c5_reconsideration_review_profile_v0.json"
REVIEW_REPORT_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0/o2_c5_reconsideration_review_report.json"
REVIEW_TRACE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0/o2_c5_reconsideration_review_transition_trace.json"

SOURCE_EXECUTION_RECEIPT_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0_receipts/d19ec918.json"
EXECUTION_RECORD_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_execution_record_v0.json"
READY_STATUS_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_ready_status_v0.json"
OPENING_GUARD_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_opening_guard_v0.json"
EXECUTION_ROLLUP_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_rollup_v0.json"
EXECUTION_PROFILE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0/o2_c5_reconsideration_profile_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_REVIEW_RECEIPT_PATH,
    REVIEW_ASSESSMENT_PATH,
    READY_STATUS_REVIEW_PATH,
    OPENING_GUARD_REVIEW_PATH,
    WEAK_FEEDBACK_BASIS_REVIEW_PATH,
    NO_LIVE_AUDIT_REVIEW_PATH,
    OPEN_DECISION_CANDIDATE_PATH,
    REVIEWED_REFERENCE_CANDIDATE_PATH,
    REVIEW_AUTHORITY_PATH,
    REVIEW_CLASSIFICATION_PATH,
    REVIEW_ROLLUP_PATH,
    REVIEW_PROFILE_PATH,
    REVIEW_REPORT_PATH,
    REVIEW_TRACE_PATH,
    SOURCE_EXECUTION_RECEIPT_PATH,
    EXECUTION_RECORD_PATH,
    READY_STATUS_PATH,
    OPENING_GUARD_PATH,
    EXECUTION_ROLLUP_PATH,
    EXECUTION_PROFILE_PATH,
]

OUT_DIR = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0"
RECEIPT_DIR = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0_receipts"

CLOSURE_RECORD_PATH = OUT_DIR / "o2_c5_reconsideration_reference_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "o2_c5_reconsideration_reviewed_reference_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "o2_c5_reconsideration_reference_index_v0.json"
READY_STATUS_REFERENCE_PATH = OUT_DIR / "o2_c5_reconsideration_ready_status_reference_v0.json"
OPENING_GUARD_REFERENCE_PATH = OUT_DIR / "o2_c5_opening_guard_reference_v0.json"
OPEN_DECISION_CANDIDATE_REFERENCE_PATH = OUT_DIR / "o2_c5_open_decision_candidate_reference_v0.json"
WEAK_FEEDBACK_BASIS_REFERENCE_PATH = OUT_DIR / "o2_c5_reconsideration_weak_feedback_basis_reference_v0.json"
NO_LIVE_AUDIT_REFERENCE_PATH = OUT_DIR / "o2_c5_no_live_audit_reference_v0.json"
POST_C5_RECONSIDERATION_DECISION_READINESS_PATH = OUT_DIR / "o2_post_c5_reconsideration_reference_decision_readiness_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_c5_reconsideration_reference_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_c5_reconsideration_reference_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_c5_reconsideration_reference_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_c5_reconsideration_reference_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_c5_reconsideration_reference_closure_report.json"
TRACE_PATH = OUT_DIR / "o2_c5_reconsideration_reference_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_REVIEWED_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_REVIEWED_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_AS_REVIEWED_REFERENCE_V0"
RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_O2_C5_RECONSIDERATION_REFERENCE_CLOSURE_V0"

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

    review_receipt = read_json(SOURCE_REVIEW_RECEIPT_PATH)
    review_summary = review_receipt.get("machine_readable_o2_c5_reconsideration_after_weak_feedback_resolution_review_summary", {})
    assessment = read_json(REVIEW_ASSESSMENT_PATH)
    ready_review = read_json(READY_STATUS_REVIEW_PATH)
    guard_review = read_json(OPENING_GUARD_REVIEW_PATH)
    basis_review = read_json(WEAK_FEEDBACK_BASIS_REVIEW_PATH)
    audit_review = read_json(NO_LIVE_AUDIT_REVIEW_PATH)
    open_candidate = read_json(OPEN_DECISION_CANDIDATE_PATH)
    reference_candidate = read_json(REVIEWED_REFERENCE_CANDIDATE_PATH)
    authority = read_json(REVIEW_AUTHORITY_PATH)
    classification = read_json(REVIEW_CLASSIFICATION_PATH)
    rollup = read_json(REVIEW_ROLLUP_PATH)
    profile = read_json(REVIEW_PROFILE_PATH)
    report = read_json(REVIEW_REPORT_PATH)
    trace = read_json(REVIEW_TRACE_PATH)

    execution_receipt = read_json(SOURCE_EXECUTION_RECEIPT_PATH)
    execution_summary = execution_receipt.get("machine_readable_o2_c5_reconsideration_after_weak_feedback_resolution_summary", {})
    execution_record = read_json(EXECUTION_RECORD_PATH)
    ready_status = read_json(READY_STATUS_PATH)
    opening_guard = read_json(OPENING_GUARD_PATH)
    execution_rollup = read_json(EXECUTION_ROLLUP_PATH)
    execution_profile = read_json(EXECUTION_PROFILE_PATH)

    if review_receipt.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("review_receipt_not_pass")
    if review_receipt.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("review_stop_wrong")
    if review_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("review_hidden_next")
    if review_summary.get("status") != EXPECTED_REVIEW_STATUS:
        failures.append(f"review_status_wrong:{review_summary.get('status')}")
    if review_summary.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append(f"review_next_wrong:{review_summary.get('recommended_next')}")

    for key in [
        "c5_reconsideration_review_complete",
        "c5_reconsideration_review_pass",
        "c5_reconsideration_integrity_validated",
        "close_candidate_ready",
        "c5_open_decision_candidate_ready",
        "c5_reconsideration_executed",
        "review_ready",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
        "c5_reconsideration_ready",
        "c5_opening_deferred",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_summary_required_true_missing:{key}")

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
        if review_summary.get(key) is not False:
            failures.append(f"review_summary_forbidden_true:{key}")

    if review_summary.get("c5_feedback_readiness") != "C5_RECONSIDERATION_READY_PENDING_REVIEW":
        failures.append("review_summary_readiness_wrong")
    if review_summary.get("final_resolution_records_frozen_count") != 3 or review_summary.get("resolution_records_emitted_count") != 3:
        failures.append("review_summary_resolution_counts_wrong")

    if assessment.get("close_candidate_ready") is not True or assessment.get("review_pass") is not True:
        failures.append("assessment_not_close_ready")
    if ready_review.get("c5_reconsideration_ready") is not True or ready_review.get("c5_opened") is not False:
        failures.append("ready_review_wrong")
    if guard_review.get("guard_status") != "C5_OPENING_GUARD_HELD" or guard_review.get("may_open_c5_now") is not False:
        failures.append("guard_review_wrong")
    if basis_review.get("weak_feedback_resolved") is not True or basis_review.get("resolution_records_emitted_count") != 3:
        failures.append("basis_review_wrong")
    if audit_review.get("live_feedback_audit_executed") is not False:
        failures.append("audit_review_wrong")
    if open_candidate.get("candidate_status") != "C5_OPEN_DECISION_CANDIDATE_READY_AFTER_REVIEWED_RECONSIDERATION":
        failures.append("open_candidate_wrong")
    if reference_candidate.get("close_candidate_ready") is not True:
        failures.append("reference_candidate_wrong")
    if authority.get("may_close_c5_reconsideration_as_reviewed_reference_next") is not True:
        failures.append("authority_no_close")
    if authority.get("may_open_c5_now") is not False or authority.get("may_run_live_feedback_audit_now") is not False:
        failures.append("authority_allows_open_or_audit")
    if classification.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append("classification_next_wrong")
    if rollup.get("review_pass_count") != 1 or rollup.get("close_candidate_ready_count") != 1:
        failures.append("rollup_review_wrong")
    if rollup.get("c5_open_decision_candidate_ready_count") != 1:
        failures.append("rollup_open_candidate_wrong")
    if rollup.get("c5_opened_count") != 0 or rollup.get("live_feedback_audit_executed_count") != 0:
        failures.append("rollup_open_or_audit_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_REVIEW_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("trace_stop_wrong")

    if execution_receipt.get("receipt_id") != "d19ec918" or execution_receipt.get("gate") != "PASS":
        failures.append("execution_receipt_not_pass")
    if execution_summary.get("c5_reconsideration_ready") is not True or execution_summary.get("c5_opened") is not False:
        failures.append("execution_summary_c5_wrong")
    if execution_record.get("c5_reconsideration_ready") is not True or execution_record.get("c5_opened") is not False:
        failures.append("execution_record_c5_wrong")
    if ready_status.get("c5_reconsideration_ready") is not True or ready_status.get("c5_opened") is not False:
        failures.append("ready_status_c5_wrong")
    if opening_guard.get("c5_opened") is not False or opening_guard.get("may_open_c5_now") is not False:
        failures.append("opening_guard_wrong")
    if execution_rollup.get("c5_reconsideration_ready_count") != 1 or execution_rollup.get("c5_opened_count") != 0:
        failures.append("execution_rollup_wrong")
    if execution_profile.get("c5_reconsideration_ready") is not True or execution_profile.get("c5_opened") is not False:
        failures.append("execution_profile_wrong")

    return failures, {
        "review_summary": review_summary,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, _ = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    close_pass = not failures
    status = "TYPED_O2_C5_RECONSIDERATION_CLOSED_AS_REVIEWED_REFERENCE_C5_OPEN_DECISION_READY" if close_pass else "TYPED_O2_C5_RECONSIDERATION_REFERENCE_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if close_pass else "REPAIR_O2_C5_RECONSIDERATION_REFERENCE_CLOSURE_V0"

    reason_codes = [
        "C5_RECONSIDERATION_CLOSED_AS_REVIEWED_REFERENCE",
        "C5_RECONSIDERATION_REVIEW_RECEIPT_CONSUMED",
        "C5_RECONSIDERATION_READY_STATUS_FROZEN_AS_REFERENCE",
        "C5_OPENING_GUARD_FROZEN_AS_REFERENCE",
        "WEAK_FEEDBACK_RESOLUTION_BASIS_FROZEN_AS_REFERENCE",
        "C5_OPEN_DECISION_CANDIDATE_FROZEN_AS_REFERENCE",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "POST_C5_RECONSIDERATION_REFERENCE_DECISION_READY",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if close_pass else failures

    closure_record = {
        "schema_version": "o2_c5_reconsideration_reference_closure_record_v0",
        "closure_status": "C5_RECONSIDERATION_CLOSED_AS_REVIEWED_REFERENCE" if close_pass else "C5_RECONSIDERATION_REFERENCE_CLOSURE_FAIL",
        "source_c5_reconsideration_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "closure_meaning": "C5 reconsideration readiness is frozen as a reviewed reference.",
        "closure_does_not_mean": [
            "C5 opened",
            "live feedback audit executed",
            "runtime patched",
            "source mutated",
            "architecture changed",
        ],
    }

    reviewed_reference = {
        "schema_version": "o2_c5_reconsideration_reviewed_reference_v0",
        "reference_status": "FROZEN_C5_RECONSIDERATION_REVIEWED_REFERENCE" if close_pass else "REFERENCE_NOT_FROZEN",
        "reference_object_id": "o2_c5_reconsideration_reviewed_reference_" + sha8({
            "source_review_receipt": SOURCE_REVIEW_RECEIPT_ID,
            "c5_reconsideration_ready": True,
            "c5_opened": False,
        }),
        "source_c5_reconsideration_receipt_id": "d19ec918",
        "source_c5_reconsideration_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
        "c5_opened": False,
        "c5_opening_deferred": True,
        "live_feedback_audit_executed": False,
        "post_c5_reconsideration_reference_decision_ready": close_pass,
    }

    reference_index = {
        "schema_version": "o2_c5_reconsideration_reference_index_v0",
        "index_status": "REFERENCE_INDEX_EMITTED" if close_pass else "REFERENCE_INDEX_NOT_EMITTED",
        "reference_paths": {
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "closure_record": rel(CLOSURE_RECORD_PATH),
            "ready_status_reference": rel(READY_STATUS_REFERENCE_PATH),
            "opening_guard_reference": rel(OPENING_GUARD_REFERENCE_PATH),
            "open_decision_candidate_reference": rel(OPEN_DECISION_CANDIDATE_REFERENCE_PATH),
            "post_decision_readiness": rel(POST_C5_RECONSIDERATION_DECISION_READINESS_PATH),
        },
    }

    ready_status_reference = {
        "schema_version": "o2_c5_reconsideration_ready_status_reference_v0",
        "reference_status": "C5_RECONSIDERATION_READY_STATUS_FROZEN_AS_REFERENCE",
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
        "c5_opened": False,
        "requires_explicit_post_reference_open_decision": True,
    }

    opening_guard_reference = {
        "schema_version": "o2_c5_opening_guard_reference_v0",
        "reference_status": "C5_OPENING_GUARD_FROZEN_AS_REFERENCE",
        "guard_status": "C5_OPENING_GUARD_HELD",
        "c5_reconsideration_ready": True,
        "c5_opened": False,
        "may_open_c5_now": False,
        "live_feedback_audit_executed": False,
    }

    open_decision_candidate_reference = {
        "schema_version": "o2_c5_open_decision_candidate_reference_v0",
        "reference_status": "C5_OPEN_DECISION_CANDIDATE_FROZEN_AS_REFERENCE",
        "c5_open_decision_candidate_ready": True,
        "c5_reconsideration_ready": True,
        "c5_opened": False,
        "candidate_does_not_open_c5": True,
    }

    weak_feedback_basis_reference = {
        "schema_version": "o2_c5_reconsideration_weak_feedback_basis_reference_v0",
        "reference_status": "WEAK_FEEDBACK_RESOLUTION_BASIS_FROZEN_AS_REFERENCE",
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
    }

    no_live_audit_reference = {
        "schema_version": "o2_c5_no_live_audit_reference_v0",
        "reference_status": "NO_LIVE_AUDIT_FROZEN_AS_REFERENCE",
        "live_feedback_audit_executed": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
    }

    decision_readiness = {
        "schema_version": "o2_post_c5_reconsideration_reference_decision_readiness_v0",
        "decision_ready": close_pass,
        "recommended_next": recommended_next,
        "eligible_decision_scope": "decide next after C5 reconsideration reviewed reference closure",
        "allowed_next_question": "whether C5 opening may be selected after reviewed C5 reconsideration reference exists",
        "not_authorized_here": [
            "open C5",
            "run live feedback audit",
            "patch runtime",
            "mutate source",
            "change architecture",
        ],
    }

    authority_boundary = {
        "schema_version": "o2_c5_reconsideration_reference_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_c5_reconsideration_reference_closure": close_pass,
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
        "schema_version": "o2_c5_reconsideration_reference_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c5_reconsideration_closed_as_reviewed_reference": close_pass,
        "reviewed_reference_emitted": close_pass,
        "post_c5_reconsideration_reference_decision_ready": close_pass,
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
        "schema_version": "o2_c5_reconsideration_reference_closure_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "reference_closure_count": 1 if close_pass else 0,
        "reviewed_reference_emitted_count": 1 if close_pass else 0,
        "post_c5_reconsideration_reference_decision_ready_count": 1 if close_pass else 0,
        "weak_feedback_resolved_count": 1,
        "final_resolution_boundary_crossed_count": 1,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_reconsideration_ready_count": 1,
        "c5_open_decision_candidate_ready_count": 1,
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
        "schema_version": "o2_c5_reconsideration_reference_closure_profile_v0",
        "profile_id": "o2_c5_reconsideration_reference_closure_profile_" + sha8(rollup),
        "status": status,
        "c5_reconsideration_closed_as_reviewed_reference": close_pass,
        "post_c5_reconsideration_reference_decision_ready": close_pass,
        "weak_feedback_resolved": True,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
        "c5_opened": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Decide next after C5 reconsideration reference closure. C5 opening remains separate.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_c5_reconsideration_reference_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C5 reconsideration readiness is closed as a reviewed reference. C5 remains unopened and live audit has not run; opening requires a later explicit decision.",
        "weak_feedback_resolved": True,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
        "c5_opened": False,
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_c5_reconsideration_reference_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c5_reconsideration_review",
                "question": "is C5 reconsideration reviewed clean",
                "answer": "yes" if close_pass else "no",
                "taken": "freeze C5 reconsideration reviewed reference",
            },
            {
                "step": "freeze_c5_readiness",
                "question": "is C5 reconsideration ready",
                "answer": "yes",
                "taken": "freeze readiness status as reference",
            },
            {
                "step": "preserve_opening_guard",
                "question": "does reference closure open C5",
                "answer": "no",
                "taken": "emit post-reference decision readiness",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (CLOSURE_RECORD_PATH, closure_record),
        (REVIEWED_REFERENCE_PATH, reviewed_reference),
        (REFERENCE_INDEX_PATH, reference_index),
        (READY_STATUS_REFERENCE_PATH, ready_status_reference),
        (OPENING_GUARD_REFERENCE_PATH, opening_guard_reference),
        (OPEN_DECISION_CANDIDATE_REFERENCE_PATH, open_decision_candidate_reference),
        (WEAK_FEEDBACK_BASIS_REFERENCE_PATH, weak_feedback_basis_reference),
        (NO_LIVE_AUDIT_REFERENCE_PATH, no_live_audit_reference),
        (POST_C5_RECONSIDERATION_DECISION_READINESS_PATH, decision_readiness),
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
        "C5_REF_CLOSURE_0_REVIEW_RECEIPT_CONSUMED": SOURCE_REVIEW_RECEIPT_PATH.exists(),
        "C5_REF_CLOSURE_1_CLOSURE_RECORD_EMITTED": CLOSURE_RECORD_PATH.exists(),
        "C5_REF_CLOSURE_2_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists(),
        "C5_REF_CLOSURE_3_READY_STATUS_FROZEN": ready_status_reference["c5_reconsideration_ready"] is True,
        "C5_REF_CLOSURE_4_OPENING_GUARD_FROZEN": opening_guard_reference["c5_opened"] is False and opening_guard_reference["may_open_c5_now"] is False,
        "C5_REF_CLOSURE_5_OPEN_DECISION_CANDIDATE_FROZEN": open_decision_candidate_reference["c5_open_decision_candidate_ready"] is True,
        "C5_REF_CLOSURE_6_NO_LIVE_AUDIT_FROZEN": no_live_audit_reference["live_feedback_audit_executed"] is False,
        "C5_REF_CLOSURE_7_POST_REFERENCE_DECISION_READY": decision_readiness["decision_ready"] is True,
        "C5_REF_CLOSURE_8_NO_C5_OPEN": rollup["c5_opened_count"] == 0,
        "C5_REF_CLOSURE_9_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "C5_REF_CLOSURE_10_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C5_REF_CLOSURE_11_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "C5_REF_CLOSURE_12_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_C5_RECONSIDERATION_REFERENCE_CLOSURE_GATE_FAIL",
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
        "schema_version": "o2_c5_reconsideration_reference_closure_receipt_v0",
        "receipt_type": "TYPED_O2_C5_RECONSIDERATION_REFERENCE_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c5_reconsideration_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "machine_readable_o2_c5_reconsideration_reference_closure_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c5_reconsideration_closed_as_reviewed_reference": close_pass,
            "reviewed_reference_emitted": close_pass,
            "post_c5_reconsideration_reference_decision_ready": close_pass,
            "weak_feedback_resolved": True,
            "final_resolution_boundary_crossed": True,
            "final_resolution_records_frozen_count": 3,
            "resolution_records_emitted_count": 3,
            "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
            "c5_reconsideration_ready": True,
            "c5_open_decision_candidate_ready": True,
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
            "closure_record": rel(CLOSURE_RECORD_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "reference_index": rel(REFERENCE_INDEX_PATH),
            "ready_status_reference": rel(READY_STATUS_REFERENCE_PATH),
            "opening_guard_reference": rel(OPENING_GUARD_REFERENCE_PATH),
            "open_decision_candidate_reference": rel(OPEN_DECISION_CANDIDATE_REFERENCE_PATH),
            "weak_feedback_basis_reference": rel(WEAK_FEEDBACK_BASIS_REFERENCE_PATH),
            "no_live_audit_reference": rel(NO_LIVE_AUDIT_REFERENCE_PATH),
            "post_c5_reconsideration_decision_readiness": rel(POST_C5_RECONSIDERATION_DECISION_READINESS_PATH),
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
    print(f"c5_reconsideration_reference_closure_receipt_id={receipt_id}")
    print(f"c5_reconsideration_reference_closure_receipt_path={rel(receipt_path)}")
    print(f"c5_reconsideration_reference_closure_record_path={rel(CLOSURE_RECORD_PATH)}")
    print(f"c5_reconsideration_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"c5_reconsideration_ready_status_reference_path={rel(READY_STATUS_REFERENCE_PATH)}")
    print(f"c5_open_decision_candidate_reference_path={rel(OPEN_DECISION_CANDIDATE_REFERENCE_PATH)}")
    print(f"post_c5_reconsideration_reference_decision_readiness_path={rel(POST_C5_RECONSIDERATION_DECISION_READINESS_PATH)}")
    print(f"c5_reconsideration_reference_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c5_reconsideration_reference_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
