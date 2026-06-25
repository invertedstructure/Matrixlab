#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "observation.o2_c5_live_feedback_audit_after_opening_reference_reference_closure.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / C5_LIVE_FEEDBACK_AUDIT_REFERENCE_CLOSURE"
MODE = "CLOSE / FREEZE_LIVE_C5_AUDIT_AS_REVIEWED_REFERENCE / BUILD_TARGET_DECISION_PENDING"
BUILD_MODE = "O2_C5_LIVE_FEEDBACK_AUDIT_REFERENCE_CLOSURE_ONLY"

SOURCE_REVIEW_RECEIPT_ID = "466a7747"

SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0_receipts/466a7747.json"
REVIEW_ASSESSMENT_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_live_feedback_audit_review_assessment_v0.json"
EVIDENCE_SURFACE_REVIEW_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_live_feedback_audit_evidence_surface_review_v0.json"
OBSERVATION_SET_REVIEW_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_live_feedback_audit_observation_set_review_v0.json"
SIGNAL_CLASSIFICATION_REVIEW_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_live_feedback_audit_signal_classification_review_v0.json"
AUDIT_GUARD_REVIEW_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_live_feedback_audit_guard_review_v0.json"
BUILD_TARGET_GUARD_REVIEW_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_build_target_guard_after_audit_review_v0.json"
AUDIT_REVIEW_PACKET_REVIEW_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_live_feedback_audit_review_packet_review_v0.json"
POST_AUDIT_DECISION_CANDIDATE_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_post_c5_live_feedback_audit_decision_candidate_v0.json"
REVIEWED_REFERENCE_CANDIDATE_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_live_feedback_audit_reviewed_reference_candidate_v0.json"
REVIEW_AUTHORITY_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_live_feedback_audit_review_authority_boundary_v0.json"
REVIEW_CLASSIFICATION_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_live_feedback_audit_review_classification_v0.json"
REVIEW_ROLLUP_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_live_feedback_audit_review_rollup_v0.json"
REVIEW_PROFILE_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_live_feedback_audit_review_profile_v0.json"
REVIEW_REPORT_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_live_feedback_audit_review_report.json"
REVIEW_TRACE_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_review_v0/o2_c5_live_feedback_audit_review_transition_trace.json"

SOURCE_AUDIT_RECEIPT_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0_receipts/1b8e38a8.json"
AUDIT_EVIDENCE_SURFACE_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_evidence_surface_v0.json"
AUDIT_OBSERVATION_SET_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_observation_set_v0.json"
AUDIT_SIGNAL_CLASSIFICATION_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_live_feedback_audit_signal_classification_v0.json"
BUILD_TARGET_GUARD_STATUS_PATH = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0/o2_c5_build_target_guard_after_live_audit_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_REVIEW_RECEIPT_PATH,
    REVIEW_ASSESSMENT_PATH,
    EVIDENCE_SURFACE_REVIEW_PATH,
    OBSERVATION_SET_REVIEW_PATH,
    SIGNAL_CLASSIFICATION_REVIEW_PATH,
    AUDIT_GUARD_REVIEW_PATH,
    BUILD_TARGET_GUARD_REVIEW_PATH,
    AUDIT_REVIEW_PACKET_REVIEW_PATH,
    POST_AUDIT_DECISION_CANDIDATE_PATH,
    REVIEWED_REFERENCE_CANDIDATE_PATH,
    REVIEW_AUTHORITY_PATH,
    REVIEW_CLASSIFICATION_PATH,
    REVIEW_ROLLUP_PATH,
    REVIEW_PROFILE_PATH,
    REVIEW_REPORT_PATH,
    REVIEW_TRACE_PATH,
    SOURCE_AUDIT_RECEIPT_PATH,
    AUDIT_EVIDENCE_SURFACE_PATH,
    AUDIT_OBSERVATION_SET_PATH,
    AUDIT_SIGNAL_CLASSIFICATION_PATH,
    BUILD_TARGET_GUARD_STATUS_PATH,
]

OUT_DIR = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_reference_closure_v0"
RECEIPT_DIR = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_reference_closure_v0_receipts"

CLOSURE_RECORD_PATH = OUT_DIR / "o2_c5_live_feedback_audit_reference_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "o2_c5_live_feedback_audit_reviewed_reference_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "o2_c5_live_feedback_audit_reference_index_v0.json"
EVIDENCE_SURFACE_REFERENCE_PATH = OUT_DIR / "o2_c5_live_feedback_audit_evidence_surface_reference_v0.json"
OBSERVATION_SET_REFERENCE_PATH = OUT_DIR / "o2_c5_live_feedback_audit_observation_set_reference_v0.json"
SIGNAL_REFERENCE_PATH = OUT_DIR / "o2_c5_live_feedback_audit_signal_reference_v0.json"
BUILD_TARGET_GUARD_REFERENCE_PATH = OUT_DIR / "o2_c5_build_target_guard_after_audit_reference_v0.json"
POST_AUDIT_DECISION_READINESS_PATH = OUT_DIR / "o2_post_c5_live_feedback_audit_reference_decision_readiness_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_c5_live_feedback_audit_reference_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_c5_live_feedback_audit_reference_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_c5_live_feedback_audit_reference_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_c5_live_feedback_audit_reference_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_c5_live_feedback_audit_reference_closure_report.json"
TRACE_PATH = OUT_DIR / "o2_c5_live_feedback_audit_reference_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_REVIEWED_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_REVIEWED_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_AS_REVIEWED_REFERENCE_V0"
RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_O2_C5_LIVE_FEEDBACK_AUDIT_REFERENCE_CLOSURE_V0"

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
    review_summary = review_receipt.get("machine_readable_o2_c5_live_feedback_audit_after_opening_reference_review_summary", {})

    review_assessment = read_json(REVIEW_ASSESSMENT_PATH)
    evidence_surface_review = read_json(EVIDENCE_SURFACE_REVIEW_PATH)
    observation_set_review = read_json(OBSERVATION_SET_REVIEW_PATH)
    signal_review = read_json(SIGNAL_CLASSIFICATION_REVIEW_PATH)
    build_guard_review = read_json(BUILD_TARGET_GUARD_REVIEW_PATH)
    post_audit_candidate = read_json(POST_AUDIT_DECISION_CANDIDATE_PATH)
    reviewed_ref_candidate = read_json(REVIEWED_REFERENCE_CANDIDATE_PATH)
    authority = read_json(REVIEW_AUTHORITY_PATH)
    classification = read_json(REVIEW_CLASSIFICATION_PATH)
    rollup = read_json(REVIEW_ROLLUP_PATH)
    profile = read_json(REVIEW_PROFILE_PATH)
    report = read_json(REVIEW_REPORT_PATH)
    trace = read_json(REVIEW_TRACE_PATH)

    audit_receipt = read_json(SOURCE_AUDIT_RECEIPT_PATH)
    evidence_surface = read_json(AUDIT_EVIDENCE_SURFACE_PATH)
    observation_set = read_json(AUDIT_OBSERVATION_SET_PATH)
    signal_classification = read_json(AUDIT_SIGNAL_CLASSIFICATION_PATH)
    build_guard_status = read_json(BUILD_TARGET_GUARD_STATUS_PATH)

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
        "live_feedback_audit_review_complete",
        "live_feedback_audit_review_pass",
        "audit_integrity_validated",
        "audit_evidence_surface_reviewed",
        "audit_observation_set_reviewed",
        "close_candidate_ready",
        "post_audit_decision_candidate_ready",
        "live_feedback_audit_executed",
        "c5_live_branch_executed",
        "review_ready",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
        "c5_opened",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_summary_required_true_missing:{key}")

    if review_summary.get("audit_observation_count") != 5:
        failures.append("review_summary_observation_count_wrong")
    if review_summary.get("c5_feedback_readiness") != "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW":
        failures.append("review_summary_readiness_wrong")
    if review_summary.get("final_resolution_records_frozen_count") != 3:
        failures.append("review_summary_final_count_wrong")
    if review_summary.get("resolution_records_emitted_count") != 3:
        failures.append("review_summary_resolution_count_wrong")

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
        if review_summary.get(key) is not False:
            failures.append(f"review_summary_forbidden_true:{key}")

    if review_assessment.get("close_candidate_ready") is not True or review_assessment.get("review_pass") is not True:
        failures.append("review_assessment_not_close_ready")
    if evidence_surface_review.get("audit_evidence_surface_emitted") is not True:
        failures.append("evidence_surface_review_wrong")
    if observation_set_review.get("observation_count") != 5 or observation_set_review.get("all_observations_bounded") is not True:
        failures.append("observation_set_review_wrong")
    if signal_review.get("signal_class") != "REVIEW_REQUIRED_NO_BUILD_TARGET_SELECTED":
        failures.append("signal_review_wrong")
    if build_guard_review.get("target_selected_for_build") is not False or build_guard_review.get("build_target_candidate_emitted") is not False:
        failures.append("build_guard_review_wrong")
    if post_audit_candidate.get("candidate_status") != "POST_C5_LIVE_FEEDBACK_AUDIT_DECISION_CANDIDATE_READY_AFTER_REVIEWED_AUDIT":
        failures.append("post_audit_candidate_wrong")
    if reviewed_ref_candidate.get("close_candidate_ready") is not True:
        failures.append("reviewed_reference_candidate_wrong")
    if authority.get("may_close_live_feedback_audit_as_reviewed_reference_next") is not True:
        failures.append("authority_no_close")
    if authority.get("may_select_build_target_now") is not False:
        failures.append("authority_allows_build_target")
    if classification.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append("classification_next_wrong")
    if rollup.get("review_pass_count") != 1 or rollup.get("close_candidate_ready_count") != 1:
        failures.append("rollup_review_wrong")
    if rollup.get("audit_observation_count") != 5:
        failures.append("rollup_observation_count_wrong")
    if rollup.get("target_selected_for_build_count") != 0 or rollup.get("build_target_candidate_emitted_count") != 0:
        failures.append("rollup_target_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_REVIEW_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("trace_stop_wrong")

    if audit_receipt.get("receipt_id") != "1b8e38a8" or audit_receipt.get("gate") != "PASS":
        failures.append("audit_receipt_not_pass")
    if evidence_surface.get("audit_observation_count") != 5 or evidence_surface.get("target_selected_for_build") is not False:
        failures.append("source_evidence_surface_wrong")
    if observation_set.get("observation_count") != 5:
        failures.append("source_observation_set_wrong")
    if signal_classification.get("build_target_candidate_emitted") is not False:
        failures.append("source_signal_target_wrong")
    if build_guard_status.get("target_selected_for_build") is not False:
        failures.append("source_build_guard_wrong")

    return failures, {
        "review_summary": review_summary,
        "observation_set": observation_set,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    close_pass = not failures
    status = "TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_CLOSED_AS_REVIEWED_REFERENCE_POST_AUDIT_DECISION_READY" if close_pass else "TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_REFERENCE_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if close_pass else "REPAIR_O2_C5_LIVE_FEEDBACK_AUDIT_REFERENCE_CLOSURE_V0"

    reason_codes = [
        "LIVE_FEEDBACK_AUDIT_CLOSED_AS_REVIEWED_REFERENCE",
        "LIVE_FEEDBACK_AUDIT_REVIEW_RECEIPT_CONSUMED",
        "AUDIT_EVIDENCE_SURFACE_FROZEN_AS_REFERENCE",
        "AUDIT_OBSERVATION_SET_FROZEN_AS_REFERENCE",
        "AUDIT_SIGNAL_FROZEN_AS_REFERENCE",
        "BUILD_TARGET_GUARD_FROZEN_AS_REFERENCE",
        "POST_AUDIT_DECISION_CANDIDATE_FROZEN_AS_REFERENCE",
        "POST_AUDIT_REFERENCE_DECISION_READY",
        "NO_BUILD_TARGET_SELECTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if close_pass else failures

    observations = basis.get("observation_set", {}).get("observations", []) if close_pass else []

    closure_record = {
        "schema_version": "o2_c5_live_feedback_audit_reference_closure_record_v0",
        "closure_status": "LIVE_FEEDBACK_AUDIT_CLOSED_AS_REVIEWED_REFERENCE" if close_pass else "LIVE_FEEDBACK_AUDIT_REFERENCE_CLOSURE_FAIL",
        "source_c5_live_feedback_audit_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "closure_meaning": "Live C5 feedback audit evidence is frozen as a reviewed reference.",
        "closure_does_not_mean": [
            "build target selected",
            "build target candidate emitted",
            "runtime patched",
            "source mutated",
            "architecture changed",
        ],
    }

    reviewed_reference = {
        "schema_version": "o2_c5_live_feedback_audit_reviewed_reference_v0",
        "reference_status": "FROZEN_C5_LIVE_FEEDBACK_AUDIT_REVIEWED_REFERENCE" if close_pass else "REFERENCE_NOT_FROZEN",
        "reference_object_id": "o2_c5_live_feedback_audit_reviewed_reference_" + sha8({
            "source_review_receipt": SOURCE_REVIEW_RECEIPT_ID,
            "audit_observation_count": 5,
            "target_selected_for_build": False,
        }),
        "source_c5_live_feedback_audit_receipt_id": "1b8e38a8",
        "source_c5_live_feedback_audit_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW",
        "c5_opened": True,
        "live_feedback_audit_executed": True,
        "c5_live_branch_executed": True,
        "audit_observation_count": 5 if close_pass else 0,
        "target_selected_for_build": False,
        "build_target_candidate_emitted": False,
        "post_audit_reference_decision_ready": close_pass,
    }

    reference_index = {
        "schema_version": "o2_c5_live_feedback_audit_reference_index_v0",
        "index_status": "REFERENCE_INDEX_EMITTED" if close_pass else "REFERENCE_INDEX_NOT_EMITTED",
        "reference_paths": {
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "closure_record": rel(CLOSURE_RECORD_PATH),
            "evidence_surface_reference": rel(EVIDENCE_SURFACE_REFERENCE_PATH),
            "observation_set_reference": rel(OBSERVATION_SET_REFERENCE_PATH),
            "signal_reference": rel(SIGNAL_REFERENCE_PATH),
            "build_target_guard_reference": rel(BUILD_TARGET_GUARD_REFERENCE_PATH),
            "post_audit_decision_readiness": rel(POST_AUDIT_DECISION_READINESS_PATH),
        },
    }

    evidence_surface_reference = {
        "schema_version": "o2_c5_live_feedback_audit_evidence_surface_reference_v0",
        "reference_status": "AUDIT_EVIDENCE_SURFACE_FROZEN_AS_REFERENCE",
        "c5_feedback_readiness": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW",
        "live_feedback_audit_executed": True,
        "c5_live_branch_executed": True,
        "audit_observation_count": 5,
        "target_selected_for_build": False,
        "build_target_candidate_emitted": False,
    }

    observation_set_reference = {
        "schema_version": "o2_c5_live_feedback_audit_observation_set_reference_v0",
        "reference_status": "AUDIT_OBSERVATION_SET_FROZEN_AS_REFERENCE",
        "observation_count": 5 if close_pass else 0,
        "observations": observations,
        "all_observations_bounded": close_pass,
        "all_observations_receipt_backed": close_pass,
    }

    signal_reference = {
        "schema_version": "o2_c5_live_feedback_audit_signal_reference_v0",
        "reference_status": "AUDIT_SIGNAL_FROZEN_AS_REFERENCE",
        "signal_class": "REVIEW_REQUIRED_NO_BUILD_TARGET_SELECTED",
        "post_audit_signal_clean": close_pass,
        "build_target_candidate_emitted": False,
        "requires_decision_before_any_build_target": True,
    }

    build_target_guard_reference = {
        "schema_version": "o2_c5_build_target_guard_after_audit_reference_v0",
        "reference_status": "BUILD_TARGET_GUARD_FROZEN_AS_REFERENCE",
        "target_selected_for_build": False,
        "build_target_candidate_emitted": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "architecture_change": False,
    }

    post_audit_decision_readiness = {
        "schema_version": "o2_post_c5_live_feedback_audit_reference_decision_readiness_v0",
        "decision_ready": close_pass,
        "recommended_next": recommended_next,
        "eligible_decision_scope": "decide next after reviewed live C5 audit reference closure",
        "allowed_next_question": "whether to select a build target, continue audit, or close after reviewed live C5 audit evidence exists",
        "not_authorized_here": [
            "select build target",
            "emit build target candidate",
            "patch runtime",
            "mutate source",
            "change architecture",
        ],
    }

    authority_boundary = {
        "schema_version": "o2_c5_live_feedback_audit_reference_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_live_feedback_audit_reference_closure": close_pass,
        "may_select_build_target_now": False,
        "may_emit_build_target_candidate_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_change_architecture": False,
    }

    classification = {
        "schema_version": "o2_c5_live_feedback_audit_reference_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "live_feedback_audit_closed_as_reviewed_reference": close_pass,
        "reviewed_reference_emitted": close_pass,
        "post_audit_reference_decision_ready": close_pass,
        "live_feedback_audit_executed": True,
        "c5_live_branch_executed": True,
        "audit_observation_count": 5 if close_pass else 0,
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
        "schema_version": "o2_c5_live_feedback_audit_reference_closure_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "reference_closure_count": 1 if close_pass else 0,
        "reviewed_reference_emitted_count": 1 if close_pass else 0,
        "post_audit_reference_decision_ready_count": 1 if close_pass else 0,
        "live_feedback_audit_executed_count": 1,
        "c5_live_branch_executed_count": 1,
        "audit_observation_count": 5 if close_pass else 0,
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
        "schema_version": "o2_c5_live_feedback_audit_reference_closure_profile_v0",
        "profile_id": "o2_c5_live_feedback_audit_reference_closure_profile_" + sha8(rollup),
        "status": status,
        "live_feedback_audit_closed_as_reviewed_reference": close_pass,
        "post_audit_reference_decision_ready": close_pass,
        "live_feedback_audit_executed": True,
        "audit_observation_count": 5 if close_pass else 0,
        "c5_feedback_readiness": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW",
        "target_selected_for_build": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Decide next after live C5 audit reference closure. Build target selection remains separate.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_c5_live_feedback_audit_reference_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Live C5 feedback audit is closed as a reviewed reference. Five audit observations are frozen; no build target was selected.",
        "c5_feedback_readiness": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW",
        "live_feedback_audit_executed": True,
        "audit_observation_count": 5 if close_pass else 0,
        "target_selected_for_build": False,
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_c5_live_feedback_audit_reference_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_live_feedback_audit_review",
                "question": "is live C5 audit reviewed clean",
                "answer": "yes" if close_pass else "no",
                "taken": "freeze live C5 audit reviewed reference",
            },
            {
                "step": "freeze_audit_observations",
                "question": "are five audit observations available",
                "answer": "yes" if close_pass else "no",
                "taken": "freeze observation set as reference",
            },
            {
                "step": "preserve_build_target_guard",
                "question": "did reference closure select a build target",
                "answer": "no",
                "taken": "emit post-audit decision readiness",
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
        (EVIDENCE_SURFACE_REFERENCE_PATH, evidence_surface_reference),
        (OBSERVATION_SET_REFERENCE_PATH, observation_set_reference),
        (SIGNAL_REFERENCE_PATH, signal_reference),
        (BUILD_TARGET_GUARD_REFERENCE_PATH, build_target_guard_reference),
        (POST_AUDIT_DECISION_READINESS_PATH, post_audit_decision_readiness),
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
        "C5_AUDIT_REF_CLOSURE_0_REVIEW_RECEIPT_CONSUMED": SOURCE_REVIEW_RECEIPT_PATH.exists(),
        "C5_AUDIT_REF_CLOSURE_1_CLOSURE_RECORD_EMITTED": CLOSURE_RECORD_PATH.exists(),
        "C5_AUDIT_REF_CLOSURE_2_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists(),
        "C5_AUDIT_REF_CLOSURE_3_EVIDENCE_SURFACE_FROZEN": EVIDENCE_SURFACE_REFERENCE_PATH.exists() and evidence_surface_reference["live_feedback_audit_executed"] is True,
        "C5_AUDIT_REF_CLOSURE_4_OBSERVATION_SET_FROZEN": OBSERVATION_SET_REFERENCE_PATH.exists() and observation_set_reference["observation_count"] == 5,
        "C5_AUDIT_REF_CLOSURE_5_SIGNAL_FROZEN": SIGNAL_REFERENCE_PATH.exists() and signal_reference["signal_class"] == "REVIEW_REQUIRED_NO_BUILD_TARGET_SELECTED",
        "C5_AUDIT_REF_CLOSURE_6_BUILD_TARGET_GUARD_FROZEN": build_target_guard_reference["target_selected_for_build"] is False and build_target_guard_reference["build_target_candidate_emitted"] is False,
        "C5_AUDIT_REF_CLOSURE_7_POST_AUDIT_DECISION_READY": post_audit_decision_readiness["decision_ready"] is True,
        "C5_AUDIT_REF_CLOSURE_8_NO_BUILD_TARGET": rollup["target_selected_for_build_count"] == 0 and rollup["build_target_candidate_emitted_count"] == 0,
        "C5_AUDIT_REF_CLOSURE_9_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "C5_AUDIT_REF_CLOSURE_10_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C5_AUDIT_REF_CLOSURE_11_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "C5_AUDIT_REF_CLOSURE_12_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_REFERENCE_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "audit_observation_count": 5 if close_pass else 0,
        "target_selected_for_build": False,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_c5_live_feedback_audit_reference_closure_receipt_v0",
        "receipt_type": "TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_REFERENCE_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c5_live_feedback_audit_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "machine_readable_o2_c5_live_feedback_audit_reference_closure_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "live_feedback_audit_closed_as_reviewed_reference": close_pass,
            "reviewed_reference_emitted": close_pass,
            "post_audit_reference_decision_ready": close_pass,
            "live_feedback_audit_executed": True,
            "c5_live_branch_executed": True,
            "audit_observation_count": 5 if close_pass else 0,
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
            "closure_record": rel(CLOSURE_RECORD_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "reference_index": rel(REFERENCE_INDEX_PATH),
            "evidence_surface_reference": rel(EVIDENCE_SURFACE_REFERENCE_PATH),
            "observation_set_reference": rel(OBSERVATION_SET_REFERENCE_PATH),
            "signal_reference": rel(SIGNAL_REFERENCE_PATH),
            "build_target_guard_reference": rel(BUILD_TARGET_GUARD_REFERENCE_PATH),
            "post_audit_decision_readiness": rel(POST_AUDIT_DECISION_READINESS_PATH),
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
    print(f"c5_live_feedback_audit_reference_closure_receipt_id={receipt_id}")
    print(f"c5_live_feedback_audit_reference_closure_receipt_path={rel(receipt_path)}")
    print(f"c5_live_feedback_audit_reference_closure_record_path={rel(CLOSURE_RECORD_PATH)}")
    print(f"c5_live_feedback_audit_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"c5_live_feedback_audit_observation_set_reference_path={rel(OBSERVATION_SET_REFERENCE_PATH)}")
    print(f"post_audit_reference_decision_readiness_path={rel(POST_AUDIT_DECISION_READINESS_PATH)}")
    print(f"c5_live_feedback_audit_reference_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c5_live_feedback_audit_reference_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
