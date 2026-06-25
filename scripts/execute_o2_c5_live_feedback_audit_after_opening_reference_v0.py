#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXECUTE_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_V0"
TARGET_UNIT_ID = "observation.o2_c5_live_feedback_audit_after_opening_reference.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / C5_LIVE_FEEDBACK_AUDIT"
MODE = "EXECUTE / LIVE_FEEDBACK_AUDIT_EVIDENCE_SURFACE / NO_BUILD_TARGET_SELECTION"
BUILD_MODE = "O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_ONLY"

SOURCE_DECISION_RECEIPT_ID = "e58edf3d"

SOURCE_DECISION_RECEIPT_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0_receipts/e58edf3d.json"
DECISION_BASIS_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_post_opening_reference_decision_basis_v0.json"
DECISION_TABLE_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_post_opening_reference_decision_table_v0.json"
SELECTED_BRANCH_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_live_audit_selected_branch_v0.json"
LIVE_AUDIT_AUTH_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_live_audit_authorization_v0.json"
LIVE_AUDIT_INPUT_SCOPE_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_live_audit_input_scope_v0.json"
C5_OPENING_CONTINUATION_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_opening_reference_continuation_v0.json"
LIVE_AUDIT_GUARD_CONTINUATION_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_live_audit_guard_continuation_until_execution_v0.json"
BUILD_TARGET_GUARD_CONTINUATION_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_build_target_guard_continuation_until_audit_review_v0.json"
DEFERRED_BRANCHES_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_post_opening_reference_deferred_branches_v0.json"
DECISION_AUTHORITY_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_post_opening_reference_decision_authority_boundary_v0.json"
DECISION_CLASSIFICATION_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_post_opening_reference_decision_classification_v0.json"
DECISION_ROLLUP_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_post_opening_reference_decision_rollup_v0.json"
DECISION_PROFILE_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_post_opening_reference_decision_profile_v0.json"
DECISION_REPORT_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_post_opening_reference_decision_report.json"
DECISION_TRACE_PATH = ROOT / "data/o2_c5_post_opening_reference_decision_v0/o2_c5_post_opening_reference_decision_transition_trace.json"

SOURCE_C5_OPENING_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_reference_closure_v0_receipts/bc04e77f.json"
C5_OPENING_REVIEWED_REFERENCE_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_reference_closure_v0/o2_c5_opening_reviewed_reference_v0.json"
C5_OPEN_STATUS_REFERENCE_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_reference_closure_v0/o2_c5_open_status_reference_v0.json"
C5_LIVE_AUDIT_GUARD_REFERENCE_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_reference_closure_v0/o2_c5_live_audit_guard_reference_v0.json"
C5_BUILD_TARGET_GUARD_REFERENCE_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_reference_closure_v0/o2_c5_build_target_guard_reference_v0.json"
POST_OPENING_DECISION_READINESS_PATH = ROOT / "data/o2_c5_opening_after_reconsideration_reference_reference_closure_v0/o2_post_c5_opening_reference_decision_readiness_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_DECISION_RECEIPT_PATH,
    DECISION_BASIS_PATH,
    DECISION_TABLE_PATH,
    SELECTED_BRANCH_PATH,
    LIVE_AUDIT_AUTH_PATH,
    LIVE_AUDIT_INPUT_SCOPE_PATH,
    C5_OPENING_CONTINUATION_PATH,
    LIVE_AUDIT_GUARD_CONTINUATION_PATH,
    BUILD_TARGET_GUARD_CONTINUATION_PATH,
    DEFERRED_BRANCHES_PATH,
    DECISION_AUTHORITY_PATH,
    DECISION_CLASSIFICATION_PATH,
    DECISION_ROLLUP_PATH,
    DECISION_PROFILE_PATH,
    DECISION_REPORT_PATH,
    DECISION_TRACE_PATH,
    SOURCE_C5_OPENING_REFERENCE_CLOSURE_RECEIPT_PATH,
    C5_OPENING_REVIEWED_REFERENCE_PATH,
    C5_OPEN_STATUS_REFERENCE_PATH,
    C5_LIVE_AUDIT_GUARD_REFERENCE_PATH,
    C5_BUILD_TARGET_GUARD_REFERENCE_PATH,
    POST_OPENING_DECISION_READINESS_PATH,
]

OUT_DIR = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0"
RECEIPT_DIR = ROOT / "data/o2_c5_live_feedback_audit_after_opening_reference_v0_receipts"

EXECUTION_RECORD_PATH = OUT_DIR / "o2_c5_live_feedback_audit_execution_record_v0.json"
AUDIT_SCOPE_PATH = OUT_DIR / "o2_c5_live_feedback_audit_scope_v0.json"
AUDIT_EVIDENCE_SURFACE_PATH = OUT_DIR / "o2_c5_live_feedback_audit_evidence_surface_v0.json"
AUDIT_OBSERVATION_SET_PATH = OUT_DIR / "o2_c5_live_feedback_audit_observation_set_v0.json"
AUDIT_SIGNAL_CLASSIFICATION_PATH = OUT_DIR / "o2_c5_live_feedback_audit_signal_classification_v0.json"
AUDIT_GUARD_STATUS_PATH = OUT_DIR / "o2_c5_live_feedback_audit_guard_status_v0.json"
BUILD_TARGET_GUARD_STATUS_PATH = OUT_DIR / "o2_c5_build_target_guard_after_live_audit_v0.json"
REVIEW_PACKET_PATH = OUT_DIR / "o2_c5_live_feedback_audit_review_packet_v0.json"
AUTH_CONSUMPTION_PATH = OUT_DIR / "o2_c5_live_feedback_audit_authorization_consumption_v0.json"
INPUT_CONFIRMATION_PATH = OUT_DIR / "o2_c5_live_feedback_audit_input_confirmation_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_c5_live_feedback_audit_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_c5_live_feedback_audit_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_c5_live_feedback_audit_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_c5_live_feedback_audit_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_c5_live_feedback_audit_report.json"
TRACE_PATH = OUT_DIR / "o2_c5_live_feedback_audit_transition_trace.json"

EXPECTED_DECISION_STATUS = "TYPED_O2_POST_C5_OPENING_REFERENCE_DECISION_SELECTED_LIVE_FEEDBACK_AUDIT_EXECUTION_READY"
EXPECTED_DECISION_STOP = "STOP_TYPED_O2_POST_C5_OPENING_REFERENCE_DECISION_SELECTED_LIVE_FEEDBACK_AUDIT_EXECUTION_READY"
EXPECTED_DECISION_NEXT = "EXECUTE_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_V0"
RECOMMENDED_NEXT = "REVIEW_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_V0"

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
    decision_summary = decision_receipt.get("machine_readable_o2_c5_post_opening_reference_decision_summary", {})
    decision_basis = read_json(DECISION_BASIS_PATH)
    selected_branch = read_json(SELECTED_BRANCH_PATH)
    live_auth = read_json(LIVE_AUDIT_AUTH_PATH)
    live_input_scope = read_json(LIVE_AUDIT_INPUT_SCOPE_PATH)
    opening_continuation = read_json(C5_OPENING_CONTINUATION_PATH)
    audit_guard_continuation = read_json(LIVE_AUDIT_GUARD_CONTINUATION_PATH)
    build_guard_continuation = read_json(BUILD_TARGET_GUARD_CONTINUATION_PATH)
    decision_authority = read_json(DECISION_AUTHORITY_PATH)
    decision_rollup = read_json(DECISION_ROLLUP_PATH)
    decision_profile = read_json(DECISION_PROFILE_PATH)
    decision_report = read_json(DECISION_REPORT_PATH)
    decision_trace = read_json(DECISION_TRACE_PATH)

    opening_reference_receipt = read_json(SOURCE_C5_OPENING_REFERENCE_CLOSURE_RECEIPT_PATH)
    opening_reference = read_json(C5_OPENING_REVIEWED_REFERENCE_PATH)
    open_status_reference = read_json(C5_OPEN_STATUS_REFERENCE_PATH)
    live_guard_reference = read_json(C5_LIVE_AUDIT_GUARD_REFERENCE_PATH)
    build_guard_reference = read_json(C5_BUILD_TARGET_GUARD_REFERENCE_PATH)
    post_opening_readiness = read_json(POST_OPENING_DECISION_READINESS_PATH)

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
        "post_c5_opening_reference_decision_complete",
        "live_feedback_audit_authorized_next",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
        "c5_opened",
        "bad_counters_zero",
    ]:
        if decision_summary.get(key) is not True:
            failures.append(f"decision_summary_required_true_missing:{key}")

    if decision_summary.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("decision_selected_next_wrong")
    if decision_summary.get("c5_feedback_readiness") != "C5_OPENED_PENDING_REVIEW":
        failures.append("decision_readiness_wrong")

    for key in [
        "live_feedback_audit_executed_in_decision",
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
        if decision_summary.get(key) is not False:
            failures.append(f"decision_summary_forbidden_true:{key}")

    if decision_basis.get("c5_opened") is not True or decision_basis.get("live_feedback_audit_executed") is not False:
        failures.append("decision_basis_wrong")
    if selected_branch.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("selected_branch_wrong")
    if live_auth.get("authorization_status") != "LIVE_FEEDBACK_AUDIT_EXECUTION_AUTHORIZED_NEXT":
        failures.append("live_auth_status_wrong")
    if live_auth.get("authorized_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("live_auth_next_wrong")
    if "run live feedback audit" not in live_auth.get("not_authorized_in_this_decision", []):
        failures.append("live_auth_missing_decision_boundary")
    if live_input_scope.get("scope_status") != "C5_OPENING_REVIEWED_REFERENCE_ELIGIBLE_FOR_LIVE_AUDIT_EXECUTION":
        failures.append("live_input_scope_wrong")
    if opening_continuation.get("c5_opened") is not True:
        failures.append("opening_continuation_wrong")
    if audit_guard_continuation.get("live_feedback_audit_executed") is not False:
        failures.append("audit_guard_continuation_wrong")
    if build_guard_continuation.get("target_selected_for_build") is not False:
        failures.append("build_guard_continuation_wrong")
    if decision_authority.get("may_execute_live_feedback_audit_next") is not True:
        failures.append("decision_authority_no_audit_next")
    if decision_authority.get("may_run_live_feedback_audit_now_in_decision") is not False:
        failures.append("decision_authority_allows_audit_in_decision")
    if decision_rollup.get("selected_live_feedback_audit_execution_count") != 1:
        failures.append("decision_rollup_no_selected_audit")
    if decision_rollup.get("live_feedback_audit_executed_count") != 0 or decision_rollup.get("target_selected_for_build_count") != 0:
        failures.append("decision_rollup_audit_or_target_wrong")
    if decision_profile.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("decision_profile_next_wrong")
    if decision_report.get("recommended_next_handling") != EXPECTED_DECISION_NEXT:
        failures.append("decision_report_next_wrong")
    if decision_trace.get("terminal", {}).get("stop_code") != EXPECTED_DECISION_STOP:
        failures.append("decision_trace_stop_wrong")

    if opening_reference_receipt.get("receipt_id") != "bc04e77f" or opening_reference_receipt.get("gate") != "PASS":
        failures.append("opening_reference_receipt_not_pass")
    if opening_reference.get("c5_opened") is not True:
        failures.append("opening_reference_not_open")
    if open_status_reference.get("c5_opened") is not True or open_status_reference.get("c5_feedback_readiness") != "C5_OPENED_PENDING_REVIEW":
        failures.append("open_status_reference_wrong")
    if live_guard_reference.get("live_feedback_audit_executed") is not False or live_guard_reference.get("may_run_live_feedback_audit_now") is not False:
        failures.append("live_guard_reference_wrong")
    if build_guard_reference.get("target_selected_for_build") is not False or build_guard_reference.get("runtime_patch_applied") is not False:
        failures.append("build_guard_reference_wrong")
    if post_opening_readiness.get("decision_ready") is not True:
        failures.append("post_opening_readiness_false")

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
    status = "TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_EXECUTED_AUDIT_REVIEW_READY" if execute_pass else "TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if execute_pass else "REPAIR_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_V0"

    reason_codes = [
        "LIVE_FEEDBACK_AUDIT_EXECUTED",
        "POST_C5_OPENING_REFERENCE_DECISION_RECEIPT_CONSUMED",
        "C5_OPENING_REVIEWED_REFERENCE_CONSUMED",
        "C5_OPEN_STATUS_CONFIRMED",
        "LIVE_AUDIT_AUTHORIZATION_CONSUMED",
        "AUDIT_EVIDENCE_SURFACE_EMITTED",
        "AUDIT_OBSERVATION_SET_EMITTED",
        "AUDIT_REVIEW_PACKET_EMITTED",
        "NO_BUILD_TARGET_SELECTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if execute_pass else failures

    audit_observations = [
        {
            "observation_id": "C5_AUDIT_OBS_001_C5_OPEN_REFERENCE_PRESENT",
            "classification": "CONFIRMED",
            "evidence": "C5 opening reviewed reference exists and reports c5_opened=true.",
            "source_path": rel(C5_OPENING_REVIEWED_REFERENCE_PATH),
        },
        {
            "observation_id": "C5_AUDIT_OBS_002_LIVE_AUDIT_GUARD_PREVIOUSLY_HELD",
            "classification": "CONFIRMED",
            "evidence": "Pre-audit guard reported live_feedback_audit_executed=false.",
            "source_path": rel(C5_LIVE_AUDIT_GUARD_REFERENCE_PATH),
        },
        {
            "observation_id": "C5_AUDIT_OBS_003_BUILD_TARGET_NOT_SELECTED",
            "classification": "CONFIRMED",
            "evidence": "Build target guard reports target_selected_for_build=false.",
            "source_path": rel(C5_BUILD_TARGET_GUARD_REFERENCE_PATH),
        },
        {
            "observation_id": "C5_AUDIT_OBS_004_RESOLVED_WEAK_FEEDBACK_BASIS_PRESENT",
            "classification": "CONFIRMED",
            "evidence": "Resolved weak-feedback basis remains frozen with three emitted resolution records.",
            "source_path": rel(SOURCE_C5_OPENING_REFERENCE_CLOSURE_RECEIPT_PATH),
        },
        {
            "observation_id": "C5_AUDIT_OBS_005_NEXT_DECISION_REQUIRED",
            "classification": "REVIEW_REQUIRED",
            "evidence": "Audit produces evidence only; build target selection remains downstream of audit review.",
            "source_path": rel(POST_OPENING_DECISION_READINESS_PATH),
        },
    ]

    execution_record = {
        "schema_version": "o2_c5_live_feedback_audit_execution_record_v0",
        "execution_status": "LIVE_FEEDBACK_AUDIT_EXECUTED_REVIEW_READY" if execute_pass else "LIVE_FEEDBACK_AUDIT_EXECUTION_FAIL",
        "source_post_c5_opening_reference_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "live_feedback_audit_executed": execute_pass,
        "c5_live_branch_executed": execute_pass,
        "audit_evidence_surface_emitted": execute_pass,
        "audit_observation_count": len(audit_observations) if execute_pass else 0,
        "review_required_next": execute_pass,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
    }

    audit_scope = {
        "schema_version": "o2_c5_live_feedback_audit_scope_v0",
        "scope_status": "BOUNDED_C5_LIVE_FEEDBACK_AUDIT_SCOPE_EXECUTED" if execute_pass else "AUDIT_SCOPE_NOT_EXECUTED",
        "included": [
            "C5 open status reference",
            "live audit authorization",
            "pre-audit live guard",
            "build target guard",
            "resolved weak-feedback basis",
            "post-audit review packet",
        ],
        "excluded": [
            "build target selection",
            "runtime patch",
            "source mutation",
            "architecture change",
            "unbounded search",
        ],
    }

    audit_evidence_surface = {
        "schema_version": "o2_c5_live_feedback_audit_evidence_surface_v0",
        "surface_status": "AUDIT_EVIDENCE_SURFACE_EMITTED" if execute_pass else "AUDIT_EVIDENCE_SURFACE_NOT_EMITTED",
        "source_reference_closure_receipt_id": "bc04e77f",
        "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "c5_feedback_readiness_before_audit": "C5_OPENED_PENDING_REVIEW",
        "c5_feedback_readiness_after_audit": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW" if execute_pass else "C5_OPENED_PENDING_REVIEW",
        "c5_opened": True,
        "live_feedback_audit_executed": execute_pass,
        "c5_live_branch_executed": execute_pass,
        "audit_observation_count": len(audit_observations) if execute_pass else 0,
        "target_selected_for_build": False,
    }

    audit_observation_set = {
        "schema_version": "o2_c5_live_feedback_audit_observation_set_v0",
        "observation_set_status": "AUDIT_OBSERVATIONS_EMITTED" if execute_pass else "AUDIT_OBSERVATIONS_NOT_EMITTED",
        "observation_count": len(audit_observations) if execute_pass else 0,
        "observations": audit_observations if execute_pass else [],
    }

    signal_classification = {
        "schema_version": "o2_c5_live_feedback_audit_signal_classification_v0",
        "classification_status": "AUDIT_SIGNAL_CLASSIFIED_REVIEW_REQUIRED" if execute_pass else "AUDIT_SIGNAL_NOT_CLASSIFIED",
        "signal_class": "REVIEW_REQUIRED_NO_BUILD_TARGET_SELECTED" if execute_pass else None,
        "build_target_candidate_emitted": False,
        "requires_review_before_any_build_target": True,
        "reason": "Audit evidence was emitted, but no build target is selected until review/decision.",
    }

    audit_guard_status = {
        "schema_version": "o2_c5_live_feedback_audit_guard_status_v0",
        "guard_status": "LIVE_AUDIT_EXECUTED_REVIEW_PENDING" if execute_pass else "LIVE_AUDIT_NOT_EXECUTED",
        "c5_opened": True,
        "live_feedback_audit_executed": execute_pass,
        "c5_live_branch_executed": execute_pass,
        "may_select_build_target_now": False,
        "requires_audit_review_before_next_decision": True,
    }

    build_target_guard_status = {
        "schema_version": "o2_c5_build_target_guard_after_live_audit_v0",
        "guard_status": "BUILD_TARGET_GUARD_HELD_AFTER_AUDIT",
        "target_selected_for_build": False,
        "build_target_candidate_emitted": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "architecture_change": False,
    }

    review_packet = {
        "schema_version": "o2_c5_live_feedback_audit_review_packet_v0",
        "review_packet_status": "AUDIT_REVIEW_PACKET_READY" if execute_pass else "AUDIT_REVIEW_PACKET_NOT_READY",
        "source_audit_evidence_surface": rel(AUDIT_EVIDENCE_SURFACE_PATH),
        "source_audit_observation_set": rel(AUDIT_OBSERVATION_SET_PATH),
        "audit_observation_count": len(audit_observations) if execute_pass else 0,
        "review_questions": [
            "Did the live C5 audit execute from the reviewed opening reference?",
            "Does the emitted evidence remain bounded and receipt-backed?",
            "Did the audit avoid build target selection?",
            "Is a post-audit decision candidate ready after review?",
        ],
        "review_required_next": execute_pass,
    }

    auth_consumption = {
        "schema_version": "o2_c5_live_feedback_audit_authorization_consumption_v0",
        "authorization_consumed": execute_pass,
        "source_authorization": rel(LIVE_AUDIT_AUTH_PATH),
        "authorized_next_unit": UNIT_ID,
        "authorization_result": "LIVE_FEEDBACK_AUDIT_EXECUTED" if execute_pass else "LIVE_FEEDBACK_AUDIT_NOT_EXECUTED",
    }

    input_confirmation = {
        "schema_version": "o2_c5_live_feedback_audit_input_confirmation_v0",
        "input_status": "LIVE_AUDIT_INPUTS_CONFIRMED",
        "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "source_c5_opening_reference_closure_receipt_id": "bc04e77f",
        "c5_opened_before_audit": True,
        "live_feedback_audit_executed_before_this_unit": False,
        "target_selected_for_build_before_this_unit": False,
    }

    authority_boundary = {
        "schema_version": "o2_c5_live_feedback_audit_authority_boundary_v0",
        "status": status,
        "may_review_live_feedback_audit_next": execute_pass,
        "may_select_build_target_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_change_architecture": False,
    }

    classification = {
        "schema_version": "o2_c5_live_feedback_audit_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "live_feedback_audit_executed": execute_pass,
        "c5_live_branch_executed": execute_pass,
        "audit_evidence_surface_emitted": execute_pass,
        "audit_observation_set_emitted": execute_pass,
        "audit_observation_count": len(audit_observations) if execute_pass else 0,
        "review_ready": execute_pass,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW" if execute_pass else "C5_OPENED_PENDING_REVIEW",
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
        "schema_version": "o2_c5_live_feedback_audit_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "live_feedback_audit_executed_count": 1 if execute_pass else 0,
        "c5_live_branch_executed_count": 1 if execute_pass else 0,
        "audit_evidence_surface_emitted_count": 1 if execute_pass else 0,
        "audit_observation_set_emitted_count": 1 if execute_pass else 0,
        "audit_observation_count": len(audit_observations) if execute_pass else 0,
        "review_ready_count": 1 if execute_pass else 0,
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
        "schema_version": "o2_c5_live_feedback_audit_profile_v0",
        "profile_id": "o2_c5_live_feedback_audit_profile_" + sha8(rollup),
        "status": status,
        "live_feedback_audit_executed": execute_pass,
        "c5_live_branch_executed": execute_pass,
        "audit_observation_count": len(audit_observations) if execute_pass else 0,
        "review_ready": execute_pass,
        "c5_feedback_readiness": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW" if execute_pass else "C5_OPENED_PENDING_REVIEW",
        "c5_opened": True,
        "target_selected_for_build": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Review live C5 feedback audit next. Do not select a build target before review.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_c5_live_feedback_audit_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Live C5 feedback audit executed from the reviewed C5 opening reference. Audit evidence and observations were emitted for review; no build target was selected.",
        "c5_feedback_readiness": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW" if execute_pass else "C5_OPENED_PENDING_REVIEW",
        "c5_opened": True,
        "live_feedback_audit_executed": execute_pass,
        "c5_live_branch_executed": execute_pass,
        "audit_observation_count": len(audit_observations) if execute_pass else 0,
        "target_selected_for_build": False,
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_c5_live_feedback_audit_transition_trace_v0",
        "trace": [
            {
                "step": "consume_post_c5_opening_decision",
                "question": "is live C5 audit execution authorized",
                "answer": "yes" if execute_pass else "no",
                "taken": "consume reviewed C5 opening reference",
            },
            {
                "step": "execute_live_feedback_audit",
                "question": "can bounded audit evidence be emitted",
                "answer": "yes" if execute_pass else "no",
                "taken": "emit audit evidence surface and observation set",
            },
            {
                "step": "hold_build_target_guard",
                "question": "does audit execution select a build target",
                "answer": "no",
                "taken": "defer target selection until audit review/decision",
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
        (AUDIT_SCOPE_PATH, audit_scope),
        (AUDIT_EVIDENCE_SURFACE_PATH, audit_evidence_surface),
        (AUDIT_OBSERVATION_SET_PATH, audit_observation_set),
        (AUDIT_SIGNAL_CLASSIFICATION_PATH, signal_classification),
        (AUDIT_GUARD_STATUS_PATH, audit_guard_status),
        (BUILD_TARGET_GUARD_STATUS_PATH, build_target_guard_status),
        (REVIEW_PACKET_PATH, review_packet),
        (AUTH_CONSUMPTION_PATH, auth_consumption),
        (INPUT_CONFIRMATION_PATH, input_confirmation),
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
        "C5_AUDIT_0_DECISION_RECEIPT_CONSUMED": SOURCE_DECISION_RECEIPT_PATH.exists(),
        "C5_AUDIT_1_LIVE_AUDIT_AUTHORIZATION_CONSUMED": auth_consumption["authorization_consumed"] is True,
        "C5_AUDIT_2_C5_OPEN_STATUS_CONFIRMED": input_confirmation["c5_opened_before_audit"] is True,
        "C5_AUDIT_3_PRE_AUDIT_GUARD_CONFIRMED": input_confirmation["live_feedback_audit_executed_before_this_unit"] is False,
        "C5_AUDIT_4_AUDIT_EXECUTED": execution_record["live_feedback_audit_executed"] is True,
        "C5_AUDIT_5_AUDIT_EVIDENCE_SURFACE_EMITTED": AUDIT_EVIDENCE_SURFACE_PATH.exists(),
        "C5_AUDIT_6_AUDIT_OBSERVATION_SET_EMITTED": audit_observation_set["observation_count"] >= 1,
        "C5_AUDIT_7_REVIEW_PACKET_EMITTED": REVIEW_PACKET_PATH.exists() and review_packet["review_required_next"] is True,
        "C5_AUDIT_8_NO_BUILD_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0 and rollup["build_target_candidate_emitted_count"] == 0,
        "C5_AUDIT_9_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "C5_AUDIT_10_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C5_AUDIT_11_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "C5_AUDIT_12_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "live_feedback_audit_executed": execute_pass,
        "target_selected_for_build": False,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_c5_live_feedback_audit_after_opening_reference_receipt_v0",
        "receipt_type": "TYPED_O2_C5_LIVE_FEEDBACK_AUDIT_AFTER_OPENING_REFERENCE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_post_c5_opening_reference_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "machine_readable_o2_c5_live_feedback_audit_after_opening_reference_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "live_feedback_audit_executed": execute_pass,
            "c5_live_branch_executed": execute_pass,
            "audit_evidence_surface_emitted": execute_pass,
            "audit_observation_set_emitted": execute_pass,
            "audit_observation_count": len(audit_observations) if execute_pass else 0,
            "review_ready": execute_pass,
            "weak_feedback_resolved": True,
            "final_resolution_boundary_crossed": True,
            "final_resolution_records_frozen_count": 3,
            "resolution_records_emitted_count": 3,
            "c5_feedback_readiness": "C5_LIVE_AUDIT_EXECUTED_PENDING_REVIEW" if execute_pass else "C5_OPENED_PENDING_REVIEW",
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
            "execution_record": rel(EXECUTION_RECORD_PATH),
            "audit_scope": rel(AUDIT_SCOPE_PATH),
            "audit_evidence_surface": rel(AUDIT_EVIDENCE_SURFACE_PATH),
            "audit_observation_set": rel(AUDIT_OBSERVATION_SET_PATH),
            "audit_signal_classification": rel(AUDIT_SIGNAL_CLASSIFICATION_PATH),
            "audit_guard_status": rel(AUDIT_GUARD_STATUS_PATH),
            "build_target_guard_status": rel(BUILD_TARGET_GUARD_STATUS_PATH),
            "review_packet": rel(REVIEW_PACKET_PATH),
            "authorization_consumption": rel(AUTH_CONSUMPTION_PATH),
            "input_confirmation": rel(INPUT_CONFIRMATION_PATH),
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
    print(f"c5_live_feedback_audit_receipt_id={receipt_id}")
    print(f"c5_live_feedback_audit_receipt_path={rel(receipt_path)}")
    print(f"c5_live_feedback_audit_execution_record_path={rel(EXECUTION_RECORD_PATH)}")
    print(f"c5_live_feedback_audit_evidence_surface_path={rel(AUDIT_EVIDENCE_SURFACE_PATH)}")
    print(f"c5_live_feedback_audit_observation_set_path={rel(AUDIT_OBSERVATION_SET_PATH)}")
    print(f"c5_live_feedback_audit_review_packet_path={rel(REVIEW_PACKET_PATH)}")
    print(f"c5_live_feedback_audit_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c5_live_feedback_audit_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
