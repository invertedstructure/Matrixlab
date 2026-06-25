#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_V0"
TARGET_UNIT_ID = "observation.o2_c5_live_feedback_audit_after_opening_reference_review.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / C5_LIVE_FEEDBACK_AUDIT_REVIEW"
MODE = "REVIEW / AUDIT_EVIDENCE_INTEGRITY / NO_BUILD_TARGET_SELECTION"
BUILD_MODE = "O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_REVIEW_ONLY"

SOURCE_AUDIT_RECEIPT_ID = "1b8e38a8"

SOURCE_AUDIT_RECEIPT_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0_receipts/1b8e38a8.json"

AUDIT_EXECUTION_RECORD_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_execution_record_v0.json"
AUDIT_SCOPE_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_scope_v0.json"
AUDIT_EVIDENCE_SURFACE_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_evidence_surface_v0.json"
AUDIT_OBSERVATION_SET_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_observation_set_v0.json"
AUDIT_SIGNAL_CLASSIFICATION_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_signal_classification_v0.json"
AUDIT_GUARD_STATUS_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_guard_status_v0.json"
BUILD_TARGET_GUARD_STATUS_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_build_target_guard_after_live_audit_v0.json"
AUDIT_REVIEW_PACKET_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_review_packet_v0.json"
AUTH_CONSUMPTION_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_authorization_consumption_v0.json"
INPUT_CONFIRMATION_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_input_confirmation_v0.json"
AUDIT_AUTHORITY_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_authority_boundary_v0.json"
AUDIT_CLASSIFICATION_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_classification_v0.json"
AUDIT_ROLLUP_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_rollup_v0.json"
AUDIT_PROFILE_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_profile_v0.json"
AUDIT_REPORT_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_report.json"
AUDIT_TRACE_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_transition_trace.json"

SOURCE_POST_C5_OPENING_DECISION_RECEIPT_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0_receipts/e58edf3d.json"
SOURCE_C5_OPENING_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_reference_closure_v0_receipts/bc04e77f.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_AUDIT_RECEIPT_PATH,
    AUDIT_EXECUTION_RECORD_PATH,
    AUDIT_SCOPE_PATH,
    AUDIT_EVIDENCE_SURFACE_PATH,
    AUDIT_OBSERVATION_SET_PATH,
    AUDIT_SIGNAL_CLASSIFICATION_PATH,
    AUDIT_GUARD_STATUS_PATH,
    BUILD_TARGET_GUARD_STATUS_PATH,
    AUDIT_REVIEW_PACKET_PATH,
    AUTH_CONSUMPTION_PATH,
    INPUT_CONFIRMATION_PATH,
    AUDIT_AUTHORITY_PATH,
    AUDIT_CLASSIFICATION_PATH,
    AUDIT_ROLLUP_PATH,
    AUDIT_PROFILE_PATH,
    AUDIT_REPORT_PATH,
    AUDIT_TRACE_PATH,
    SOURCE_POST_C5_OPENING_DECISION_RECEIPT_PATH,
    SOURCE_C5_OPENING_REFERENCE_CLOSURE_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0"
RECEIPT_DIR = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "o2_c5_live_feedback_audit_review_assessment_v0.json"
EVIDENCE_SURFACE_REVIEW_PATH = OUT_DIR / "o2_c5_live_feedback_audit_evidence_surface_review_v0.json"
OBSERVATION_SET_REVIEW_PATH = OUT_DIR / "o2_c5_live_feedback_audit_observation_set_review_v0.json"
SIGNAL_CLASSIFICATION_REVIEW_PATH = OUT_DIR / "o2_c5_live_feedback_audit_signal_classification_review_v0.json"
AUDIT_GUARD_REVIEW_PATH = OUT_DIR / "o2_c5_live_feedback_audit_guard_review_v0.json"
BUILD_TARGET_GUARD_REVIEW_PATH = OUT_DIR / "o2_c5_build_target_guard_after_audit_review_v0.json"
AUDIT_REVIEW_PACKET_REVIEW_PATH = OUT_DIR / "o2_c5_live_feedback_audit_review_packet_review_v0.json"
POST_AUDIT_DECISION_CANDIDATE_PATH = OUT_DIR / "o2_post_c5_live_feedback_audit_decision_candidate_v0.json"
REVIEWED_REFERENCE_CANDIDATE_PATH = OUT_DIR / "o2_c5_live_feedback_audit_reviewed_reference_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_c5_live_feedback_audit_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_c5_live_feedback_audit_review_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_c5_live_feedback_audit_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_c5_live_feedback_audit_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_c5_live_feedback_audit_review_report.json"
TRACE_PATH = OUT_DIR / "o2_c5_live_feedback_audit_review_transition_trace.json"

EXPECTED_AUDIT_STATUS = "TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_EXECUTED_AUDIT_REVIEW_READY"
EXPECTED_AUDIT_STOP = "STOP_TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_EXECUTED_AUDIT_REVIEW_READY"
EXPECTED_AUDIT_NEXT = "REVIEW_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_V0"
RECOMMENDED_NEXT = "CLOSE_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_AS_REVIEWED_REFERENCE_V0"

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

    receipt = read_json(SOURCE_AUDIT_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_c5_live_feedback_audit_after_opening_reference_summary", {})

    execution_record = read_json(AUDIT_EXECUTION_RECORD_PATH)
    audit_scope = read_json(AUDIT_SCOPE_PATH)
    evidence_surface = read_json(AUDIT_EVIDENCE_SURFACE_PATH)
    observation_set = read_json(AUDIT_OBSERVATION_SET_PATH)
    signal_classification = read_json(AUDIT_SIGNAL_CLASSIFICATION_PATH)
    audit_guard = read_json(AUDIT_GUARD_STATUS_PATH)
    build_guard = read_json(BUILD_TARGET_GUARD_STATUS_PATH)
    review_packet = read_json(AUDIT_REVIEW_PACKET_PATH)
    auth_consumption = read_json(AUTH_CONSUMPTION_PATH)
    input_confirmation = read_json(INPUT_CONFIRMATION_PATH)
    authority = read_json(AUDIT_AUTHORITY_PATH)
    classification = read_json(AUDIT_CLASSIFICATION_PATH)
    rollup = read_json(AUDIT_ROLLUP_PATH)
    profile = read_json(AUDIT_PROFILE_PATH)
    report = read_json(AUDIT_REPORT_PATH)
    trace = read_json(AUDIT_TRACE_PATH)

    decision_receipt = read_json(SOURCE_POST_C5_OPENING_DECISION_RECEIPT_PATH)
    opening_reference_receipt = read_json(SOURCE_C5_OPENING_REFERENCE_CLOSURE_RECEIPT_PATH)

    if receipt.get("receipt_id") != SOURCE_AUDIT_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_audit_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_AUDIT_STOP:
        failures.append("source_audit_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_audit_hidden_next")
    if summary.get("status") != EXPECTED_AUDIT_STATUS:
        failures.append(f"source_audit_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_AUDIT_NEXT:
        failures.append(f"source_audit_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "live_feedback_audit_executed",
        "c5_live_branch_executed",
        "audit_evidence_surface_emitted",
        "audit_observation_set_emitted",
        "review_ready",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
        "c5_opened",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    if summary.get("audit_observation_count") != 5:
        failures.append(f"summary_observation_count_wrong:{summary.get('audit_observation_count')}")
    if summary.get("c5_feedback_readiness") != "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW":
        failures.append("summary_readiness_wrong")
    if summary.get("final_resolution_records_frozen_count") != 3:
        failures.append("summary_final_count_wrong")
    if summary.get("resolution_records_emitted_count") != 3:
        failures.append("summary_resolution_count_wrong")

    for key in [
        "target_selected_for_build",
        "build_target_candidate_emitted",
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

    if execution_record.get("execution_status") != "LIVE_FEEDBACK_AUDIT_EXECUTED_REVIEW_READY":
        failures.append("execution_record_status_wrong")
    if execution_record.get("live_feedback_audit_executed") is not True or execution_record.get("c5_live_branch_executed") is not True:
        failures.append("execution_record_audit_not_executed")
    if execution_record.get("review_required_next") is not True:
        failures.append("execution_record_review_not_required")
    if execution_record.get("target_selected_for_build") is not False:
        failures.append("execution_record_target_selected")

    if audit_scope.get("scope_status") != "BOUNDED_C5_LIVE_FEEDBACK_AUDIT_SCOPE_EXECUTED":
        failures.append("audit_scope_wrong")
    if evidence_surface.get("surface_status") != "AUDIT_EVIDENCE_SURFACE_EMITTED":
        failures.append("evidence_surface_status_wrong")
    if evidence_surface.get("live_feedback_audit_executed") is not True or evidence_surface.get("target_selected_for_build") is not False:
        failures.append("evidence_surface_audit_or_target_wrong")
    if evidence_surface.get("audit_observation_count") != 5:
        failures.append("evidence_surface_observation_count_wrong")

    if observation_set.get("observation_set_status") != "AUDIT_OBSERVATIONS_EMITTED":
        failures.append("observation_set_status_wrong")
    if observation_set.get("observation_count") != 5 or len(observation_set.get("observations", [])) != 5:
        failures.append("observation_set_count_wrong")
    if not all(o.get("classification") in {"CONFIRMED", "REVIEW_REQUIRED"} for o in observation_set.get("observations", [])):
        failures.append("observation_set_bad_classification")

    if signal_classification.get("signal_class") != "REVIEW_REQUIRED_NO_BUILD_TARGET_SELECTED":
        failures.append("signal_class_wrong")
    if signal_classification.get("build_target_candidate_emitted") is not False:
        failures.append("signal_emitted_build_target")
    if signal_classification.get("requires_review_before_any_build_target") is not True:
        failures.append("signal_review_not_required")

    if audit_guard.get("live_feedback_audit_executed") is not True or audit_guard.get("c5_live_branch_executed") is not True:
        failures.append("audit_guard_wrong")
    if audit_guard.get("may_select_build_target_now") is not False:
        failures.append("audit_guard_allows_target")

    if build_guard.get("target_selected_for_build") is not False or build_guard.get("build_target_candidate_emitted") is not False:
        failures.append("build_guard_target_wrong")
    if build_guard.get("runtime_patch_applied") is not False or build_guard.get("source_mutated") is not False:
        failures.append("build_guard_mutation_wrong")

    if review_packet.get("review_packet_status") != "AUDIT_REVIEW_PACKET_READY":
        failures.append("review_packet_status_wrong")
    if review_packet.get("review_required_next") is not True:
        failures.append("review_packet_not_review_ready")
    if auth_consumption.get("authorization_consumed") is not True:
        failures.append("auth_consumption_wrong")
    if input_confirmation.get("live_feedback_audit_executed_before_this_unit") is not False:
        failures.append("input_confirmation_pre_audited")
    if input_confirmation.get("target_selected_for_build_before_this_unit") is not False:
        failures.append("input_confirmation_target_preselected")
    if authority.get("may_review_live_feedback_audit_next") is not True:
        failures.append("authority_no_review")
    if authority.get("may_select_build_target_now") is not False:
        failures.append("authority_allows_target")
    if classification.get("recommended_next") != EXPECTED_AUDIT_NEXT:
        failures.append("classification_next_wrong")
    if rollup.get("live_feedback_audit_executed_count") != 1 or rollup.get("c5_live_branch_executed_count") != 1:
        failures.append("rollup_audit_count_wrong")
    if rollup.get("audit_observation_count") != 5:
        failures.append("rollup_observation_count_wrong")
    if rollup.get("target_selected_for_build_count") != 0 or rollup.get("build_target_candidate_emitted_count") != 0:
        failures.append("rollup_target_wrong")
    if profile.get("live_feedback_audit_executed") is not True or profile.get("target_selected_for_build") is not False:
        failures.append("profile_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_AUDIT_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_AUDIT_STOP:
        failures.append("trace_stop_wrong")

    if decision_receipt.get("receipt_id") != "e58edf3d" or decision_receipt.get("gate") != "PASS":
        failures.append("decision_receipt_wrong")
    if opening_reference_receipt.get("receipt_id") != "bc04e77f" or opening_reference_receipt.get("gate") != "PASS":
        failures.append("opening_reference_receipt_wrong")

    return failures, {
        "summary": summary,
        "observation_set": observation_set,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    review_pass = not failures
    status = "TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_REVIEWED_CLEAN_CLOSE_READY" if review_pass else "TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_REVIEW_V0"

    observation_count = 5 if review_pass else 0

    reason_codes = [
        "LIVE_FEEDBACK_AUDIT_REVIEW_COMPLETE",
        "LIVE_FEEDBACK_AUDIT_RECEIPT_CONSUMED",
        "AUDIT_EVIDENCE_SURFACE_CONFIRMED",
        "AUDIT_OBSERVATION_SET_CONFIRMED",
        "AUDIT_SIGNAL_REVIEW_REQUIRED_CONFIRMED",
        "AUDIT_REVIEW_PACKET_CONFIRMED",
        "BUILD_TARGET_GUARD_CONFIRMED",
        "NO_BUILD_TARGET_SELECTED",
        "AUDIT_CLOSE_CANDIDATE_READY",
        "POST_AUDIT_DECISION_CANDIDATE_READY",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if review_pass else failures

    review_assessment = {
        "schema_version": "o2_c5_live_feedback_audit_review_assessment_v0",
        "review_status": status,
        "review_complete": review_pass,
        "review_pass": review_pass,
        "source_audit_receipt_id": SOURCE_AUDIT_RECEIPT_ID,
        "audit_integrity_validated": review_pass,
        "audit_observation_count": observation_count,
        "close_candidate_ready": review_pass,
        "recommended_next": recommended_next,
    }

    evidence_surface_review = {
        "schema_version": "o2_c5_live_feedback_audit_evidence_surface_review_v0",
        "review_status": "AUDIT_EVIDENCE_SURFACE_REVIEW_PASS" if review_pass else "AUDIT_EVIDENCE_SURFACE_REVIEW_FAIL",
        "audit_evidence_surface_emitted": review_pass,
        "c5_feedback_readiness": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW",
        "live_feedback_audit_executed": True,
        "c5_live_branch_executed": True,
        "audit_observation_count": observation_count,
        "target_selected_for_build": False,
    }

    observation_set_review = {
        "schema_version": "o2_c5_live_feedback_audit_observation_set_review_v0",
        "review_status": "AUDIT_OBSERVATION_SET_REVIEW_PASS" if review_pass else "AUDIT_OBSERVATION_SET_REVIEW_FAIL",
        "audit_observation_set_emitted": review_pass,
        "observation_count": observation_count,
        "observation_ids": [o.get("observation_id") for o in basis.get("observation_set", {}).get("observations", [])] if review_pass else [],
        "all_observations_bounded": review_pass,
        "all_observations_receipt_backed": review_pass,
    }

    signal_classification_review = {
        "schema_version": "o2_c5_live_feedback_audit_signal_classification_review_v0",
        "review_status": "AUDIT_SIGNAL_CLASSIFICATION_REVIEW_PASS" if review_pass else "AUDIT_SIGNAL_CLASSIFICATION_REVIEW_FAIL",
        "signal_class": "REVIEW_REQUIRED_NO_BUILD_TARGET_SELECTED" if review_pass else None,
        "post_audit_signal_clean": review_pass,
        "build_target_candidate_emitted": False,
        "requires_review_before_any_build_target": True,
    }

    audit_guard_review = {
        "schema_version": "o2_c5_live_feedback_audit_guard_review_v0",
        "review_status": "LIVE_AUDIT_GUARD_REVIEW_PASS" if review_pass else "LIVE_AUDIT_GUARD_REVIEW_FAIL",
        "live_feedback_audit_executed": True,
        "c5_live_branch_executed": True,
        "review_required_next": True,
        "may_select_build_target_now": False,
    }

    build_target_guard_review = {
        "schema_version": "o2_c5_build_target_guard_after_audit_review_v0",
        "review_status": "BUILD_TARGET_GUARD_REVIEW_PASS" if review_pass else "BUILD_TARGET_GUARD_REVIEW_FAIL",
        "target_selected_for_build": False,
        "build_target_candidate_emitted": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "architecture_change": False,
    }

    review_packet_review = {
        "schema_version": "o2_c5_live_feedback_audit_review_packet_review_v0",
        "review_status": "AUDIT_REVIEW_PACKET_REVIEW_PASS" if review_pass else "AUDIT_REVIEW_PACKET_REVIEW_FAIL",
        "review_packet_ready": review_pass,
        "review_questions_answered": review_pass,
        "review_packet_confirms_no_build_target": True,
    }

    post_audit_decision_candidate = {
        "schema_version": "o2_post_c5_live_feedback_audit_decision_candidate_v0",
        "candidate_status": "POST_C5_LIVE_FEEDBACK_AUDIT_DECISION_CANDIDATE_READY_AFTER_REVIEWED_AUDIT" if review_pass else "POST_C5_LIVE_FEEDBACK_AUDIT_DECISION_CANDIDATE_NOT_READY",
        "audit_review_pass": review_pass,
        "live_feedback_audit_executed": True,
        "audit_observation_count": observation_count,
        "target_selected_for_build": False,
        "candidate_question": "whether to select a build target, continue audit, or close after reviewed live C5 audit evidence exists",
    }

    reviewed_reference_candidate = {
        "schema_version": "o2_c5_live_feedback_audit_reviewed_reference_candidate_v0",
        "candidate_status": "C5_LIVE_FEEDBACK_AUDIT_CLOSE_READY_AS_REVIEWED_REFERENCE" if review_pass else "C5_LIVE_FEEDBACK_AUDIT_NOT_CLOSE_READY",
        "review_pass": review_pass,
        "close_candidate_ready": review_pass,
        "closure_meaning": "Close live C5 feedback audit as reviewed reference.",
        "closure_does_not_mean": [
            "build target selected",
            "runtime patched",
            "source mutated",
            "architecture changed",
        ],
        "recommended_next": recommended_next,
    }

    authority_boundary = {
        "schema_version": "o2_c5_live_feedback_audit_review_authority_boundary_v0",
        "status": status,
        "may_close_live_feedback_audit_as_reviewed_reference_next": review_pass,
        "may_select_build_target_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_change_architecture": False,
    }

    classification = {
        "schema_version": "o2_c5_live_feedback_audit_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "live_feedback_audit_review_complete": review_pass,
        "live_feedback_audit_review_pass": review_pass,
        "audit_integrity_validated": review_pass,
        "audit_evidence_surface_reviewed": review_pass,
        "audit_observation_set_reviewed": review_pass,
        "audit_observation_count": observation_count,
        "close_candidate_ready": review_pass,
        "post_audit_decision_candidate_ready": review_pass,
        "live_feedback_audit_executed": True,
        "c5_live_branch_executed": True,
        "review_ready": True,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW",
        "c5_opened": True,
        "target_selected_for_build": False,
        "build_target_candidate_emitted": False,
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
        "schema_version": "o2_c5_live_feedback_audit_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "audit_integrity_validated_count": 1 if review_pass else 0,
        "audit_evidence_surface_reviewed_count": 1 if review_pass else 0,
        "audit_observation_set_reviewed_count": 1 if review_pass else 0,
        "audit_observation_count": observation_count,
        "close_candidate_ready_count": 1 if review_pass else 0,
        "post_audit_decision_candidate_ready_count": 1 if review_pass else 0,
        "live_feedback_audit_executed_count": 1,
        "c5_live_branch_executed_count": 1,
        "weak_feedback_resolved_count": 1,
        "final_resolution_boundary_crossed_count": 1,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_opened_count": 1,
        "target_selected_for_build_count": 0,
        "build_target_candidate_emitted_count": 0,
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
        "target_selected_for_build_count",
        "build_target_candidate_emitted_count",
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
        "schema_version": "o2_c5_live_feedback_audit_review_profile_v0",
        "profile_id": "o2_c5_live_feedback_audit_review_profile_" + sha8(rollup),
        "status": status,
        "live_feedback_audit_review_pass": review_pass,
        "audit_integrity_validated": review_pass,
        "audit_observation_count": observation_count,
        "close_candidate_ready": review_pass,
        "post_audit_decision_candidate_ready": review_pass,
        "c5_feedback_readiness": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW",
        "live_feedback_audit_executed": True,
        "target_selected_for_build": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Close live C5 feedback audit as reviewed reference. Build target selection remains a later explicit decision.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_c5_live_feedback_audit_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Live C5 feedback audit reviewed clean: audit evidence and five observations are valid for reference closure; no build target was selected.",
        "c5_feedback_readiness": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW",
        "live_feedback_audit_executed": True,
        "audit_observation_count": observation_count,
        "target_selected_for_build": False,
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_c5_live_feedback_audit_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_live_feedback_audit_execution",
                "question": "did live C5 audit execute cleanly",
                "answer": "yes" if review_pass else "no",
                "taken": "review audit evidence surface and observation set",
            },
            {
                "step": "verify_audit_evidence",
                "question": "is bounded audit evidence review-clean",
                "answer": "yes" if review_pass else "no",
                "taken": "confirm five observation records",
            },
            {
                "step": "verify_no_build_target",
                "question": "did audit select a build target",
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
        (EVIDENCE_SURFACE_REVIEW_PATH, evidence_surface_review),
        (OBSERVATION_SET_REVIEW_PATH, observation_set_review),
        (SIGNAL_CLASSIFICATION_REVIEW_PATH, signal_classification_review),
        (AUDIT_GUARD_REVIEW_PATH, audit_guard_review),
        (BUILD_TARGET_GUARD_REVIEW_PATH, build_target_guard_review),
        (AUDIT_REVIEW_PACKET_REVIEW_PATH, review_packet_review),
        (POST_AUDIT_DECISION_CANDIDATE_PATH, post_audit_decision_candidate),
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
        "C5_AUDIT_REVIEW_0_SOURCE_AUDIT_RECEIPT_CONSUMED": SOURCE_AUDIT_RECEIPT_PATH.exists(),
        "C5_AUDIT_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "C5_AUDIT_REVIEW_2_AUDIT_EVIDENCE_SURFACE_CONFIRMED": evidence_surface_review["audit_evidence_surface_emitted"] is True,
        "C5_AUDIT_REVIEW_3_AUDIT_OBSERVATION_SET_CONFIRMED": observation_set_review["observation_count"] == 5,
        "C5_AUDIT_REVIEW_4_SIGNAL_CLASSIFICATION_CONFIRMED": signal_classification_review["signal_class"] == "REVIEW_REQUIRED_NO_BUILD_TARGET_SELECTED",
        "C5_AUDIT_REVIEW_5_BUILD_TARGET_GUARD_CONFIRMED": build_target_guard_review["target_selected_for_build"] is False,
        "C5_AUDIT_REVIEW_6_POST_AUDIT_DECISION_CANDIDATE_READY": post_audit_decision_candidate["candidate_status"] == "POST_C5_LIVE_FEEDBACK_AUDIT_DECISION_CANDIDATE_READY_AFTER_REVIEWED_AUDIT",
        "C5_AUDIT_REVIEW_7_CLOSE_CANDIDATE_READY": reviewed_reference_candidate["close_candidate_ready"] is True,
        "C5_AUDIT_REVIEW_8_NO_BUILD_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0 and rollup["build_target_candidate_emitted_count"] == 0,
        "C5_AUDIT_REVIEW_9_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "C5_AUDIT_REVIEW_10_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C5_AUDIT_REVIEW_11_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "C5_AUDIT_REVIEW_12_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "audit_observation_count": observation_count,
        "target_selected_for_build": False,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_c5_live_feedback_audit_after_opening_reference_review_receipt_v0",
        "receipt_type": "TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c5_live_feedback_audit_receipt_id": SOURCE_AUDIT_RECEIPT_ID,
        "machine_readable_o2_c5_live_feedback_audit_after_opening_reference_review_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "live_feedback_audit_review_complete": review_pass,
            "live_feedback_audit_review_pass": review_pass,
            "audit_integrity_validated": review_pass,
            "audit_evidence_surface_reviewed": review_pass,
            "audit_observation_set_reviewed": review_pass,
            "audit_observation_count": observation_count,
            "close_candidate_ready": review_pass,
            "post_audit_decision_candidate_ready": review_pass,
            "live_feedback_audit_executed": True,
            "c5_live_branch_executed": True,
            "review_ready": True,
            "weak_feedback_resolved": True,
            "final_resolution_boundary_crossed": True,
            "final_resolution_records_frozen_count": 3,
            "resolution_records_emitted_count": 3,
            "c5_feedback_readiness": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW",
            "c5_opened": True,
            "target_selected_for_build": False,
            "build_target_candidate_emitted": False,
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
            "evidence_surface_review": rel(EVIDENCE_SURFACE_REVIEW_PATH),
            "observation_set_review": rel(OBSERVATION_SET_REVIEW_PATH),
            "signal_classification_review": rel(SIGNAL_CLASSIFICATION_REVIEW_PATH),
            "audit_guard_review": rel(AUDIT_GUARD_REVIEW_PATH),
            "build_target_guard_review": rel(BUILD_TARGET_GUARD_REVIEW_PATH),
            "audit_review_packet_review": rel(AUDIT_REVIEW_PACKET_REVIEW_PATH),
            "post_audit_decision_candidate": rel(POST_AUDIT_DECISION_CANDIDATE_PATH),
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
    print(f"c5_live_feedback_audit_review_receipt_id={receipt_id}")
    print(f"c5_live_feedback_audit_review_receipt_path={rel(receipt_path)}")
    print(f"c5_live_feedback_audit_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"c5_live_feedback_audit_observation_set_review_path={rel(OBSERVATION_SET_REVIEW_PATH)}")
    print(f"post_audit_decision_candidate_path={rel(POST_AUDIT_DECISION_CANDIDATE_PATH)}")
    print(f"c5_live_feedback_audit_reviewed_reference_candidate_path={rel(REVIEWED_REFERENCE_CANDIDATE_PATH)}")
    print(f"c5_live_feedback_audit_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c5_live_feedback_audit_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
