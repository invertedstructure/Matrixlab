#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "observation.o2_c5_opening_after_reconsideration_reference_reference_closure.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / C5_OPENING_REFERENCE_CLOSURE"
MODE = "CLOSE / FREEZE_C5_OPENING_AS_REVIEWED_REFERENCE / LIVE_AUDIT_DECISION_PENDING"
BUILD_MODE = "O2_C5_OPENING_REFERENCE_CLOSURE_ONLY"

SOURCE_REVIEW_RECEIPT_ID = "772bea3b"

SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0_receipts/772bea3b.json"
REVIEW_ASSESSMENT_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_c5_opening_review_assessment_v0.json"
OPEN_STATUS_REVIEW_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_c5_open_status_review_v0.json"
OPENING_RECORD_REVIEW_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_c5_opening_record_review_v0.json"
LIVE_AUDIT_GUARD_REVIEW_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_c5_live_audit_guard_review_v0.json"
BUILD_TARGET_GUARD_REVIEW_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_c5_build_target_guard_review_v0.json"
RECONSIDERATION_BASIS_REVIEW_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_c5_opening_reconsideration_basis_review_v0.json"
POST_OPENING_DECISION_CANDIDATE_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_post_c5_opening_decision_candidate_v0.json"
REVIEWED_REFERENCE_CANDIDATE_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_c5_opening_reviewed_reference_candidate_v0.json"
REVIEW_AUTHORITY_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_c5_opening_review_authority_boundary_v0.json"
REVIEW_CLASSIFICATION_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_c5_opening_review_classification_v0.json"
REVIEW_ROLLUP_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_c5_opening_review_rollup_v0.json"
REVIEW_PROFILE_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_c5_opening_review_profile_v0.json"
REVIEW_REPORT_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_c5_opening_review_report.json"
REVIEW_TRACE_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_review_v0/o2_c5_opening_review_transition_trace.json"

SOURCE_OPENING_RECEIPT_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0_receipts/4390230f.json"
OPEN_STATUS_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_open_status_v0.json"
OPENING_RECORD_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_opening_record_v0.json"
LIVE_AUDIT_GUARD_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_live_audit_deferred_guard_v0.json"
BUILD_TARGET_GUARD_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_v0/o2_c5_build_target_guard_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_REVIEW_RECEIPT_PATH,
    REVIEW_ASSESSMENT_PATH,
    OPEN_STATUS_REVIEW_PATH,
    OPENING_RECORD_REVIEW_PATH,
    LIVE_AUDIT_GUARD_REVIEW_PATH,
    BUILD_TARGET_GUARD_REVIEW_PATH,
    RECONSIDERATION_BASIS_REVIEW_PATH,
    POST_OPENING_DECISION_CANDIDATE_PATH,
    REVIEWED_REFERENCE_CANDIDATE_PATH,
    REVIEW_AUTHORITY_PATH,
    REVIEW_CLASSIFICATION_PATH,
    REVIEW_ROLLUP_PATH,
    REVIEW_PROFILE_PATH,
    REVIEW_REPORT_PATH,
    REVIEW_TRACE_PATH,
    SOURCE_OPENING_RECEIPT_PATH,
    OPEN_STATUS_PATH,
    OPENING_RECORD_PATH,
    LIVE_AUDIT_GUARD_PATH,
    BUILD_TARGET_GUARD_PATH,
]

OUT_DIR = ROOT / "data/o2_c5_opening_after_reconsideration_reference_reference_closure_v0"
RECEIPT_DIR = ROOT / "data/o2_c5_opening_after_reconsideration_reference_reference_closure_v0_receipts"

CLOSURE_RECORD_PATH = OUT_DIR / "o2_c5_opening_reference_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "o2_c5_opening_reviewed_reference_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "o2_c5_opening_reference_index_v0.json"
OPEN_STATUS_REFERENCE_PATH = OUT_DIR / "o2_c5_open_status_reference_v0.json"
OPENING_RECORD_REFERENCE_PATH = OUT_DIR / "o2_c5_opening_record_reference_v0.json"
LIVE_AUDIT_GUARD_REFERENCE_PATH = OUT_DIR / "o2_c5_live_audit_guard_reference_v0.json"
BUILD_TARGET_GUARD_REFERENCE_PATH = OUT_DIR / "o2_c5_build_target_guard_reference_v0.json"
POST_OPENING_DECISION_READINESS_PATH = OUT_DIR / "o2_post_c5_opening_reference_decision_readiness_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_c5_opening_reference_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_c5_opening_reference_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_c5_opening_reference_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_c5_opening_reference_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_c5_opening_reference_closure_report.json"
TRACE_PATH = OUT_DIR / "o2_c5_opening_reference_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_REVIEWED_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_REVIEWED_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_AS_REVIEWED_REFERENCE_V0"
RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_O2_C5_OPENING_REFERENCE_CLOSURE_V0"

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
    review_summary = review_receipt.get("machine_readable_o2_c5_opening_after_reconsideration_reference_review_summary", {})
    assessment = read_json(REVIEW_ASSESSMENT_PATH)
    open_status_review = read_json(OPEN_STATUS_REVIEW_PATH)
    opening_record_review = read_json(OPENING_RECORD_REVIEW_PATH)
    live_guard_review = read_json(LIVE_AUDIT_GUARD_REVIEW_PATH)
    build_guard_review = read_json(BUILD_TARGET_GUARD_REVIEW_PATH)
    post_candidate = read_json(POST_OPENING_DECISION_CANDIDATE_PATH)
    ref_candidate = read_json(REVIEWED_REFERENCE_CANDIDATE_PATH)
    authority = read_json(REVIEW_AUTHORITY_PATH)
    classification = read_json(REVIEW_CLASSIFICATION_PATH)
    rollup = read_json(REVIEW_ROLLUP_PATH)
    profile = read_json(REVIEW_PROFILE_PATH)
    report = read_json(REVIEW_REPORT_PATH)
    trace = read_json(REVIEW_TRACE_PATH)

    opening_receipt = read_json(SOURCE_OPENING_RECEIPT_PATH)
    open_status = read_json(OPEN_STATUS_PATH)
    opening_record = read_json(OPENING_RECORD_PATH)
    live_guard = read_json(LIVE_AUDIT_GUARD_PATH)
    build_guard = read_json(BUILD_TARGET_GUARD_PATH)

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
        "c5_opening_review_complete",
        "c5_opening_review_pass",
        "c5_opening_integrity_validated",
        "close_candidate_ready",
        "post_c5_opening_decision_candidate_ready",
        "c5_opening_executed",
        "review_ready",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
        "c5_opened",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_summary_required_true_missing:{key}")

    if review_summary.get("c5_feedback_readiness") != "C5_OPENED_PENDING_REVIEW":
        failures.append("review_summary_readiness_wrong")
    if review_summary.get("final_resolution_records_frozen_count") != 3:
        failures.append("review_summary_final_count_wrong")
    if review_summary.get("resolution_records_emitted_count") != 3:
        failures.append("review_summary_resolution_count_wrong")

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
        if review_summary.get(key) is not False:
            failures.append(f"review_summary_forbidden_true:{key}")

    if assessment.get("close_candidate_ready") is not True or assessment.get("review_pass") is not True:
        failures.append("assessment_not_close_ready")
    if open_status_review.get("c5_opened") is not True or open_status_review.get("c5_feedback_readiness") != "C5_OPENED_PENDING_REVIEW":
        failures.append("open_status_review_wrong")
    if opening_record_review.get("c5_opened") is not True:
        failures.append("opening_record_review_wrong")
    if live_guard_review.get("live_feedback_audit_executed") is not False or live_guard_review.get("c5_live_branch_executed") is not False:
        failures.append("live_guard_review_wrong")
    if build_guard_review.get("target_selected_for_build") is not False or build_guard_review.get("runtime_patch_applied") is not False:
        failures.append("build_guard_review_wrong")
    if post_candidate.get("candidate_status") != "POST_C5_OPENING_DECISION_CANDIDATE_READY_AFTER_REVIEWED_OPENING":
        failures.append("post_opening_candidate_wrong")
    if ref_candidate.get("close_candidate_ready") is not True:
        failures.append("reference_candidate_wrong")
    if authority.get("may_close_c5_opening_as_reviewed_reference_next") is not True:
        failures.append("authority_no_close")
    if authority.get("may_run_live_feedback_audit_now") is not False or authority.get("may_select_build_target_now") is not False:
        failures.append("authority_allows_live_or_build")
    if classification.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append("classification_next_wrong")
    if rollup.get("review_pass_count") != 1 or rollup.get("close_candidate_ready_count") != 1:
        failures.append("rollup_review_wrong")
    if rollup.get("c5_opened_count") != 1:
        failures.append("rollup_c5_not_opened")
    if rollup.get("live_feedback_audit_executed_count") != 0 or rollup.get("target_selected_for_build_count") != 0:
        failures.append("rollup_live_or_build_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_REVIEW_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("trace_stop_wrong")

    if opening_receipt.get("receipt_id") != "4390230f" or opening_receipt.get("gate") != "PASS":
        failures.append("opening_receipt_not_pass")
    if open_status.get("c5_opened") is not True:
        failures.append("source_open_status_wrong")
    if opening_record.get("c5_opened") is not True:
        failures.append("source_opening_record_wrong")
    if live_guard.get("live_feedback_audit_executed") is not False:
        failures.append("source_live_guard_wrong")
    if build_guard.get("target_selected_for_build") is not False:
        failures.append("source_build_guard_wrong")

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
    status = "TYPED_O2_C5_OPENING_CLOSED_AS_REVIEWED_REFERENCE_POST_OPENING_DECISION_READY" if close_pass else "TYPED_O2_C5_OPENING_REFERENCE_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if close_pass else "REPAIR_O2_C5_OPENING_REFERENCE_CLOSURE_V0"

    reason_codes = [
        "C5_OPENING_CLOSED_AS_REVIEWED_REFERENCE",
        "C5_OPENING_REVIEW_RECEIPT_CONSUMED",
        "C5_OPEN_STATUS_FROZEN_AS_REFERENCE",
        "C5_OPENING_RECORD_FROZEN_AS_REFERENCE",
        "LIVE_AUDIT_GUARD_FROZEN_AS_REFERENCE",
        "BUILD_TARGET_GUARD_FROZEN_AS_REFERENCE",
        "POST_C5_OPENING_DECISION_CANDIDATE_FROZEN_AS_REFERENCE",
        "POST_C5_OPENING_REFERENCE_DECISION_READY",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_BUILD_TARGET_SELECTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if close_pass else failures

    closure_record = {
        "schema_version": "o2_c5_opening_reference_closure_record_v0",
        "closure_status": "C5_OPENING_CLOSED_AS_REVIEWED_REFERENCE" if close_pass else "C5_OPENING_REFERENCE_CLOSURE_FAIL",
        "source_c5_opening_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "closure_meaning": "C5 opening is frozen as a reviewed reference.",
        "closure_does_not_mean": [
            "live feedback audit executed",
            "C5 live branch executed",
            "C5 build target selected",
            "runtime patched",
            "source mutated",
            "architecture changed",
        ],
    }

    reviewed_reference = {
        "schema_version": "o2_c5_opening_reviewed_reference_v0",
        "reference_status": "FROZEN_C5_OPENING_REVIEWED_REFERENCE" if close_pass else "REFERENCE_NOT_FROZEN",
        "reference_object_id": "o2_c5_opening_reviewed_reference_" + sha8({
            "source_review_receipt": SOURCE_REVIEW_RECEIPT_ID,
            "c5_opened": True,
            "live_feedback_audit_executed": False,
            "target_selected_for_build": False,
        }),
        "source_c5_opening_receipt_id": "4390230f",
        "source_c5_opening_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW",
        "c5_opened": True,
        "live_feedback_audit_executed": False,
        "c5_live_branch_executed": False,
        "target_selected_for_build": False,
        "post_c5_opening_reference_decision_ready": close_pass,
    }

    reference_index = {
        "schema_version": "o2_c5_opening_reference_index_v0",
        "index_status": "REFERENCE_INDEX_EMITTED" if close_pass else "REFERENCE_INDEX_NOT_EMITTED",
        "reference_paths": {
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "closure_record": rel(CLOSURE_RECORD_PATH),
            "open_status_reference": rel(OPEN_STATUS_REFERENCE_PATH),
            "opening_record_reference": rel(OPENING_RECORD_REFERENCE_PATH),
            "live_audit_guard_reference": rel(LIVE_AUDIT_GUARD_REFERENCE_PATH),
            "build_target_guard_reference": rel(BUILD_TARGET_GUARD_REFERENCE_PATH),
            "post_opening_decision_readiness": rel(POST_OPENING_DECISION_READINESS_PATH),
        },
    }

    open_status_reference = {
        "schema_version": "o2_c5_open_status_reference_v0",
        "reference_status": "C5_OPEN_STATUS_FROZEN_AS_REFERENCE",
        "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW",
        "c5_opened": True,
        "live_feedback_audit_executed": False,
        "target_selected_for_build": False,
        "requires_explicit_post_opening_reference_decision": True,
    }

    opening_record_reference = {
        "schema_version": "o2_c5_opening_record_reference_v0",
        "reference_status": "C5_OPENING_RECORD_FROZEN_AS_REFERENCE",
        "opening_status": "C5_OPENED_FOR_REVIEW",
        "c5_opened": True,
        "opening_does_not_mean_live_audit": True,
        "opening_does_not_mean_build_target": True,
    }

    live_audit_guard_reference = {
        "schema_version": "o2_c5_live_audit_guard_reference_v0",
        "reference_status": "LIVE_AUDIT_GUARD_FROZEN_AS_REFERENCE",
        "guard_status": "LIVE_AUDIT_NOT_EXECUTED",
        "c5_opened": True,
        "live_feedback_audit_executed": False,
        "c5_live_branch_executed": False,
        "may_run_live_feedback_audit_now": False,
    }

    build_target_guard_reference = {
        "schema_version": "o2_c5_build_target_guard_reference_v0",
        "reference_status": "BUILD_TARGET_GUARD_FROZEN_AS_REFERENCE",
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "architecture_change": False,
    }

    post_opening_decision_readiness = {
        "schema_version": "o2_post_c5_opening_reference_decision_readiness_v0",
        "decision_ready": close_pass,
        "recommended_next": recommended_next,
        "eligible_decision_scope": "decide next after C5 opening reviewed reference closure",
        "allowed_next_question": "whether to select live C5 audit / next C5 handling after reviewed opening reference exists",
        "not_authorized_here": [
            "run live feedback audit",
            "select build target",
            "patch runtime",
            "mutate source",
            "change architecture",
        ],
    }

    authority_boundary = {
        "schema_version": "o2_c5_opening_reference_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_c5_opening_reference_closure": close_pass,
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
        "schema_version": "o2_c5_opening_reference_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c5_opening_closed_as_reviewed_reference": close_pass,
        "reviewed_reference_emitted": close_pass,
        "post_c5_opening_reference_decision_ready": close_pass,
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
        "schema_version": "o2_c5_opening_reference_closure_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "reference_closure_count": 1 if close_pass else 0,
        "reviewed_reference_emitted_count": 1 if close_pass else 0,
        "post_c5_opening_reference_decision_ready_count": 1 if close_pass else 0,
        "weak_feedback_resolved_count": 1,
        "final_resolution_boundary_crossed_count": 1,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
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
        "schema_version": "o2_c5_opening_reference_closure_profile_v0",
        "profile_id": "o2_c5_opening_reference_closure_profile_" + sha8(rollup),
        "status": status,
        "c5_opening_closed_as_reviewed_reference": close_pass,
        "post_c5_opening_reference_decision_ready": close_pass,
        "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW",
        "c5_opened": True,
        "live_feedback_audit_executed": False,
        "target_selected_for_build": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Decide next after C5 opening reference closure. Live C5 audit remains separate.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_c5_opening_reference_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C5 opening is closed as a reviewed reference. C5 is open, but live audit and build target selection have not run.",
        "c5_feedback_readiness": "C5_OPENED_PENDING_REVIEW",
        "c5_opened": True,
        "live_feedback_audit_executed": False,
        "target_selected_for_build": False,
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_c5_opening_reference_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c5_opening_review",
                "question": "is C5 opening reviewed clean",
                "answer": "yes" if close_pass else "no",
                "taken": "freeze C5 opening reviewed reference",
            },
            {
                "step": "freeze_open_status",
                "question": "is C5 open",
                "answer": "yes",
                "taken": "freeze C5 opened status as reference",
            },
            {
                "step": "preserve_live_audit_guard",
                "question": "did reference closure run live audit or choose build target",
                "answer": "no",
                "taken": "emit post-opening decision readiness",
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
        (OPEN_STATUS_REFERENCE_PATH, open_status_reference),
        (OPENING_RECORD_REFERENCE_PATH, opening_record_reference),
        (LIVE_AUDIT_GUARD_REFERENCE_PATH, live_audit_guard_reference),
        (BUILD_TARGET_GUARD_REFERENCE_PATH, build_target_guard_reference),
        (POST_OPENING_DECISION_READINESS_PATH, post_opening_decision_readiness),
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
        "C5_OPEN_REF_CLOSURE_0_REVIEW_RECEIPT_CONSUMED": SOURCE_REVIEW_RECEIPT_PATH.exists(),
        "C5_OPEN_REF_CLOSURE_1_CLOSURE_RECORD_EMITTED": CLOSURE_RECORD_PATH.exists(),
        "C5_OPEN_REF_CLOSURE_2_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists(),
        "C5_OPEN_REF_CLOSURE_3_OPEN_STATUS_FROZEN": open_status_reference["c5_opened"] is True,
        "C5_OPEN_REF_CLOSURE_4_OPENING_RECORD_FROZEN": opening_record_reference["c5_opened"] is True,
        "C5_OPEN_REF_CLOSURE_5_LIVE_AUDIT_GUARD_FROZEN": live_audit_guard_reference["live_feedback_audit_executed"] is False and live_audit_guard_reference["c5_live_branch_executed"] is False,
        "C5_OPEN_REF_CLOSURE_6_BUILD_TARGET_GUARD_FROZEN": build_target_guard_reference["target_selected_for_build"] is False,
        "C5_OPEN_REF_CLOSURE_7_POST_OPENING_DECISION_READY": post_opening_decision_readiness["decision_ready"] is True,
        "C5_OPEN_REF_CLOSURE_8_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0 and rollup["c5_live_branch_executed_count"] == 0,
        "C5_OPEN_REF_CLOSURE_9_NO_BUILD_TARGET": rollup["target_selected_for_build_count"] == 0,
        "C5_OPEN_REF_CLOSURE_10_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "C5_OPEN_REF_CLOSURE_11_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C5_OPEN_REF_CLOSURE_12_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "C5_OPEN_REF_CLOSURE_13_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_C5_OPENING_REFERENCE_CLOSURE_GATE_FAIL",
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
        "schema_version": "o2_c5_opening_reference_closure_receipt_v0",
        "receipt_type": "TYPED_O2_C5_OPENING_REFERENCE_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c5_opening_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "machine_readable_o2_c5_opening_reference_closure_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c5_opening_closed_as_reviewed_reference": close_pass,
            "reviewed_reference_emitted": close_pass,
            "post_c5_opening_reference_decision_ready": close_pass,
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
            "closure_record": rel(CLOSURE_RECORD_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "reference_index": rel(REFERENCE_INDEX_PATH),
            "open_status_reference": rel(OPEN_STATUS_REFERENCE_PATH),
            "opening_record_reference": rel(OPENING_RECORD_REFERENCE_PATH),
            "live_audit_guard_reference": rel(LIVE_AUDIT_GUARD_REFERENCE_PATH),
            "build_target_guard_reference": rel(BUILD_TARGET_GUARD_REFERENCE_PATH),
            "post_opening_decision_readiness": rel(POST_OPENING_DECISION_READINESS_PATH),
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
    print(f"c5_opening_reference_closure_receipt_id={receipt_id}")
    print(f"c5_opening_reference_closure_receipt_path={rel(receipt_path)}")
    print(f"c5_opening_reference_closure_record_path={rel(CLOSURE_RECORD_PATH)}")
    print(f"c5_opening_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"c5_open_status_reference_path={rel(OPEN_STATUS_REFERENCE_PATH)}")
    print(f"post_c5_opening_reference_decision_readiness_path={rel(POST_OPENING_DECISION_READINESS_PATH)}")
    print(f"c5_opening_reference_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c5_opening_reference_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
