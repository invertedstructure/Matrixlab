#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_O2_C5_RECONSIDERATION_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "observation.o2_c5_post_reconsideration_reference_decision.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / POST_C5_RECONSIDERATION_REFERENCE_DECISION"
MODE = "DECIDE_ONLY / SELECT_C5_OPENING_EXECUTION / C5_READY_NOT_OPEN"
BUILD_MODE = "O2_POST_C5_RECONSIDERATION_REFERENCE_DECISION_ONLY"

SOURCE_REFERENCE_CLOSURE_RECEIPT_ID = "3167d93a"

SOURCE_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0_receipts/3167d93a.json"
CLOSURE_RECORD_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_reference_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_reviewed_reference_v0.json"
REFERENCE_INDEX_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_reference_index_v0.json"
READY_STATUS_REFERENCE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_ready_status_reference_v0.json"
OPENING_GUARD_REFERENCE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_opening_guard_reference_v0.json"
OPEN_DECISION_CANDIDATE_REFERENCE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_open_decision_candidate_reference_v0.json"
WEAK_FEEDBACK_BASIS_REFERENCE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_weak_feedback_basis_reference_v0.json"
NO_LIVE_AUDIT_REFERENCE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_no_live_audit_reference_v0.json"
POST_C5_RECONSIDERATION_DECISION_READINESS_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_post_c5_reconsideration_reference_decision_readiness_v0.json"
REFERENCE_AUTHORITY_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_reference_closure_authority_boundary_v0.json"
REFERENCE_CLASSIFICATION_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_reference_closure_classification_v0.json"
REFERENCE_ROLLUP_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_reference_closure_rollup_v0.json"
REFERENCE_PROFILE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_reference_closure_profile_v0.json"
REFERENCE_REPORT_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_reference_closure_report.json"
REFERENCE_TRACE_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_reference_closure_v0/o2_c5_reconsideration_reference_closure_transition_trace.json"

SOURCE_C5_REVIEW_RECEIPT_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_review_v0_receipts/41999f02.json"
SOURCE_C5_EXECUTION_RECEIPT_PATH = ROOT / "data/o2_c5_reconsideration_after_weak_feedback_resolution_v0_receipts/d19ec918.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_REFERENCE_CLOSURE_RECEIPT_PATH,
    CLOSURE_RECORD_PATH,
    REVIEWED_REFERENCE_PATH,
    REFERENCE_INDEX_PATH,
    READY_STATUS_REFERENCE_PATH,
    OPENING_GUARD_REFERENCE_PATH,
    OPEN_DECISION_CANDIDATE_REFERENCE_PATH,
    WEAK_FEEDBACK_BASIS_REFERENCE_PATH,
    NO_LIVE_AUDIT_REFERENCE_PATH,
    POST_C5_RECONSIDERATION_DECISION_READINESS_PATH,
    REFERENCE_AUTHORITY_PATH,
    REFERENCE_CLASSIFICATION_PATH,
    REFERENCE_ROLLUP_PATH,
    REFERENCE_PROFILE_PATH,
    REFERENCE_REPORT_PATH,
    REFERENCE_TRACE_PATH,
    SOURCE_C5_REVIEW_RECEIPT_PATH,
    SOURCE_C5_EXECUTION_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0"
RECEIPT_DIR = ROOT / "data/o2_c5_post_reconsideration_reference_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "o2_c5_post_reconsideration_reference_decision_basis_v0.json"
DECISION_TABLE_PATH = OUT_DIR / "o2_c5_post_reconsideration_reference_decision_table_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "o2_c5_opening_selected_branch_v0.json"
C5_OPENING_AUTHORIZATION_PATH = OUT_DIR / "o2_c5_opening_authorization_v0.json"
C5_OPENING_INPUT_SCOPE_PATH = OUT_DIR / "o2_c5_opening_input_scope_v0.json"
C5_RECONSIDERATION_REFERENCE_CONTINUATION_PATH = OUT_DIR / "o2_c5_reconsideration_reference_continuation_v0.json"
C5_OPENING_GUARD_CONTINUATION_PATH = OUT_DIR / "o2_c5_opening_guard_continuation_until_execution_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "o2_c5_post_reconsideration_reference_deferred_branches_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_c5_post_reconsideration_reference_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_c5_post_reconsideration_reference_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_c5_post_reconsideration_reference_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_c5_post_reconsideration_reference_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_c5_post_reconsideration_reference_decision_report.json"
TRACE_PATH = OUT_DIR / "o2_c5_post_reconsideration_reference_decision_transition_trace.json"

EXPECTED_REFERENCE_STATUS = "TYPED_O2_C5_RECONSIDERATION_CLOSED_AS_REVIEWED_REFERENCE_C5_OPEN_DECISION_READY"
EXPECTED_REFERENCE_STOP = "STOP_TYPED_O2_C5_RECONSIDERATION_CLOSED_AS_REVIEWED_REFERENCE_C5_OPEN_DECISION_READY"
EXPECTED_REFERENCE_NEXT = "DECIDE_NEXT_AFTER_O2_C5_RECONSIDERATION_REFERENCE_CLOSURE_V0"

SELECTED_BRANCH = "EXECUTE_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE"
SELECTED_NEXT_UNIT = "EXECUTE_O2_C5_OPENING_AFTER_RECONSIDERATION_REFERENCE_V0"

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

    receipt = read_json(SOURCE_REFERENCE_CLOSURE_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_c5_reconsideration_reference_closure_summary", {})

    closure_record = read_json(CLOSURE_RECORD_PATH)
    reviewed_reference = read_json(REVIEWED_REFERENCE_PATH)
    reference_index = read_json(REFERENCE_INDEX_PATH)
    ready_reference = read_json(READY_STATUS_REFERENCE_PATH)
    guard_reference = read_json(OPENING_GUARD_REFERENCE_PATH)
    open_candidate_reference = read_json(OPEN_DECISION_CANDIDATE_REFERENCE_PATH)
    weak_feedback_basis = read_json(WEAK_FEEDBACK_BASIS_REFERENCE_PATH)
    no_live_audit = read_json(NO_LIVE_AUDIT_REFERENCE_PATH)
    decision_readiness = read_json(POST_C5_RECONSIDERATION_DECISION_READINESS_PATH)
    authority = read_json(REFERENCE_AUTHORITY_PATH)
    classification = read_json(REFERENCE_CLASSIFICATION_PATH)
    rollup = read_json(REFERENCE_ROLLUP_PATH)
    profile = read_json(REFERENCE_PROFILE_PATH)
    report = read_json(REFERENCE_REPORT_PATH)
    trace = read_json(REFERENCE_TRACE_PATH)

    c5_review_receipt = read_json(SOURCE_C5_REVIEW_RECEIPT_PATH)
    c5_execution_receipt = read_json(SOURCE_C5_EXECUTION_RECEIPT_PATH)

    if receipt.get("receipt_id") != SOURCE_REFERENCE_CLOSURE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_reference_closure_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_REFERENCE_STOP:
        failures.append("source_reference_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_reference_hidden_next")
    if summary.get("status") != EXPECTED_REFERENCE_STATUS:
        failures.append(f"source_reference_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_REFERENCE_NEXT:
        failures.append(f"source_reference_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "c5_reconsideration_closed_as_reviewed_reference",
        "reviewed_reference_emitted",
        "post_c5_reconsideration_reference_decision_ready",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
        "c5_reconsideration_ready",
        "c5_open_decision_candidate_ready",
        "c5_opening_deferred",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    if summary.get("final_resolution_records_frozen_count") != 3:
        failures.append("summary_final_resolution_count_wrong")
    if summary.get("resolution_records_emitted_count") != 3:
        failures.append("summary_resolution_count_wrong")
    if summary.get("c5_feedback_readiness") != "C5_RECONSIDERATION_READY_PENDING_REVIEW":
        failures.append("summary_c5_readiness_wrong")

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

    if closure_record.get("closure_status") != "C5_RECONSIDERATION_CLOSED_AS_REVIEWED_REFERENCE":
        failures.append("closure_record_wrong")
    if reviewed_reference.get("c5_reconsideration_ready") is not True or reviewed_reference.get("c5_opened") is not False:
        failures.append("reviewed_reference_c5_wrong")
    if reviewed_reference.get("post_c5_reconsideration_reference_decision_ready") is not True:
        failures.append("reviewed_reference_decision_not_ready")
    if reference_index.get("index_status") != "REFERENCE_INDEX_EMITTED":
        failures.append("reference_index_wrong")
    if ready_reference.get("c5_reconsideration_ready") is not True or ready_reference.get("c5_opened") is not False:
        failures.append("ready_reference_wrong")
    if guard_reference.get("guard_status") != "C5_OPENING_GUARD_HELD":
        failures.append("guard_reference_status_wrong")
    if guard_reference.get("may_open_c5_now") is not False or guard_reference.get("c5_opened") is not False:
        failures.append("guard_reference_allows_open")
    if open_candidate_reference.get("c5_open_decision_candidate_ready") is not True:
        failures.append("open_candidate_reference_not_ready")
    if open_candidate_reference.get("candidate_does_not_open_c5") is not True or open_candidate_reference.get("c5_opened") is not False:
        failures.append("open_candidate_reference_opens_c5")
    if weak_feedback_basis.get("weak_feedback_resolved") is not True or weak_feedback_basis.get("resolution_records_emitted_count") != 3:
        failures.append("weak_feedback_basis_wrong")
    if no_live_audit.get("live_feedback_audit_executed") is not False:
        failures.append("no_live_audit_wrong")
    if decision_readiness.get("decision_ready") is not True:
        failures.append("decision_readiness_false")
    if authority.get("may_decide_next_after_c5_reconsideration_reference_closure") is not True:
        failures.append("authority_no_decide")
    if authority.get("may_open_c5_now") is not False or authority.get("may_run_live_feedback_audit_now") is not False:
        failures.append("authority_allows_open_or_audit")
    if classification.get("recommended_next") != EXPECTED_REFERENCE_NEXT:
        failures.append("classification_next_wrong")
    if rollup.get("post_c5_reconsideration_reference_decision_ready_count") != 1:
        failures.append("rollup_decision_ready_wrong")
    if rollup.get("c5_reconsideration_ready_count") != 1 or rollup.get("c5_open_decision_candidate_ready_count") != 1:
        failures.append("rollup_ready_or_candidate_wrong")
    if rollup.get("c5_opened_count") != 0 or rollup.get("live_feedback_audit_executed_count") != 0:
        failures.append("rollup_open_or_audit_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_REFERENCE_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_REFERENCE_STOP:
        failures.append("trace_stop_wrong")
    if c5_review_receipt.get("receipt_id") != "41999f02" or c5_review_receipt.get("gate") != "PASS":
        failures.append("c5_review_receipt_wrong")
    if c5_execution_receipt.get("receipt_id") != "d19ec918" or c5_execution_receipt.get("gate") != "PASS":
        failures.append("c5_execution_receipt_wrong")

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

    decision_pass = not failures
    status = "TYPED_O2_POST_C5_RECONSIDERATION_REFERENCE_DECISION_SELECTED_C5_OPENING_EXECUTION_READY" if decision_pass else "TYPED_O2_POST_C5_RECONSIDERATION_REFERENCE_DECISION_GATE_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_O2_POST_C5_RECONSIDERATION_REFERENCE_DECISION_V0"

    reason_codes = [
        "POST_C5_RECONSIDERATION_REFERENCE_DECISION_COMPLETE",
        "C5_RECONSIDERATION_REFERENCE_CLOSURE_RECEIPT_CONSUMED",
        "C5_RECONSIDERATION_READY_REFERENCE_CONFIRMED",
        "C5_OPEN_DECISION_CANDIDATE_CONFIRMED",
        "C5_OPENING_GUARD_REFERENCE_CONFIRMED",
        "WEAK_FEEDBACK_RESOLVED_REFERENCE_CONFIRMED",
        "C5_OPENING_EXECUTION_SELECTED_NEXT",
        "NO_C5_OPENED_IN_DECISION",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED_IN_DECISION",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if decision_pass else failures

    decision_basis = {
        "schema_version": "o2_c5_post_reconsideration_reference_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_c5_reconsideration_reference_closure_receipt_id": SOURCE_REFERENCE_CLOSURE_RECEIPT_ID,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
        "c5_open_decision_candidate_ready": True,
        "c5_opened": False,
        "live_feedback_audit_executed": False,
    }

    decision_table = {
        "schema_version": "o2_c5_post_reconsideration_reference_decision_table_v0",
        "decision_status": "NEXT_BRANCH_SELECTED" if decision_pass else "NO_BRANCH_SELECTED",
        "records": [
            {
                "branch": SELECTED_BRANCH,
                "selected": decision_pass,
                "next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
                "why": "C5 reconsideration is frozen as a reviewed reference and the open-decision candidate is ready.",
            },
            {
                "branch": "OPEN_C5_NOW_IN_DECISION",
                "selected": False,
                "next_unit": None,
                "why": "This unit only selects opening execution; it does not open C5.",
            },
            {
                "branch": "RUN_LIVE_FEEDBACK_AUDIT_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Live audit remains outside this decision-only edge.",
            },
            {
                "branch": "REPAIR_OR_RETRY",
                "selected": False,
                "next_unit": None,
                "why": "No failure is present in the C5 reconsideration reference closure.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "o2_c5_opening_selected_branch_v0",
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "selection_scope": "C5 opening execution after reviewed C5 reconsideration reference closure",
        "selection_reason": "C5 reconsideration readiness is reviewed and frozen; C5 opening may now be tested by a separate execution unit.",
        "selected_branch_does_not": [
            "open C5 in this decision",
            "run live feedback audit in this decision",
            "repair",
            "retry",
            "patch runtime",
            "mutate source",
            "mutate prior receipts",
            "change architecture",
        ],
    }

    c5_opening_authorization = {
        "schema_version": "o2_c5_opening_authorization_v0",
        "authorization_status": "C5_OPENING_EXECUTION_AUTHORIZED_NEXT" if decision_pass else "NOT_AUTHORIZED",
        "authorized_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "authorized_execution_mode": "C5_OPENING_FROM_REVIEWED_RECONSIDERATION_REFERENCE" if decision_pass else None,
        "authorized_scope": [
            "consume C5 reconsideration reviewed reference",
            "verify C5 reconsideration readiness",
            "verify C5 opening guard",
            "decide whether C5 opening record can be emitted",
        ],
        "not_authorized_in_this_decision": [
            "open C5",
            "run live feedback audit",
            "repair",
            "retry",
            "patch runtime",
            "mutate source",
            "mutate prior receipts",
            "change architecture",
        ],
    }

    c5_opening_input_scope = {
        "schema_version": "o2_c5_opening_input_scope_v0",
        "scope_status": "C5_RECONSIDERATION_REVIEWED_REFERENCE_ELIGIBLE_FOR_OPENING_EXECUTION",
        "source_reference_closure_receipt": rel(SOURCE_REFERENCE_CLOSURE_RECEIPT_PATH),
        "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
        "ready_status_reference": rel(READY_STATUS_REFERENCE_PATH),
        "opening_guard_reference": rel(OPENING_GUARD_REFERENCE_PATH),
        "open_decision_candidate_reference": rel(OPEN_DECISION_CANDIDATE_REFERENCE_PATH),
        "post_reference_decision_readiness": rel(POST_C5_RECONSIDERATION_DECISION_READINESS_PATH),
        "c5_reconsideration_ready": True,
        "c5_opened": False,
    }

    readiness_continuation = {
        "schema_version": "o2_c5_reconsideration_reference_continuation_v0",
        "c5_reconsideration_ready": True,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_open_decision_candidate_ready": True,
        "decision_emitted_c5_opening_record": False,
        "c5_opened": False,
    }

    opening_guard_continuation = {
        "schema_version": "o2_c5_opening_guard_continuation_until_execution_v0",
        "guard_status": "C5_OPENING_GUARD_HELD_UNTIL_SELECTED_EXECUTION",
        "c5_reconsideration_ready": True,
        "c5_opened": False,
        "may_open_c5_now_in_decision": False,
        "selected_execution_unit": SELECTED_NEXT_UNIT if decision_pass else None,
    }

    deferred_branches = {
        "schema_version": "o2_c5_post_reconsideration_reference_deferred_branches_v0",
        "deferred": [
            "OPEN_C5_NOW_IN_DECISION",
            "LIVE_FEEDBACK_AUDIT_NOW",
            "REPAIR",
            "RETRY",
            "RUNTIME_PATCH",
            "SOURCE_MUTATION",
            "ARCHITECTURE_CHANGE",
        ],
        "why": "This unit only selects C5 opening execution as the next lawful branch.",
    }

    authority_boundary = {
        "schema_version": "o2_c5_post_reconsideration_reference_decision_authority_boundary_v0",
        "status": status,
        "may_execute_c5_opening_next": decision_pass,
        "may_open_c5_now_in_decision": False,
        "may_run_live_feedback_audit_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_change_architecture": False,
    }

    classification = {
        "schema_version": "o2_c5_post_reconsideration_reference_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_c5_reconsideration_reference_decision_complete": decision_pass,
        "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": recommended_next,
        "c5_opening_authorized_next": decision_pass,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
        "c5_open_decision_candidate_ready": True,
        "c5_opening_executed_in_decision": False,
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
        "schema_version": "o2_c5_post_reconsideration_reference_decision_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "decision_count": 1 if decision_pass else 0,
        "selected_c5_opening_execution_count": 1 if decision_pass else 0,
        "c5_opening_authorized_next_count": 1 if decision_pass else 0,
        "weak_feedback_resolved_count": 1,
        "final_resolution_boundary_crossed_count": 1,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_reconsideration_ready_count": 1,
        "c5_open_decision_candidate_ready_count": 1,
        "c5_opening_executed_in_decision_count": 0,
        "c5_opened_count": 0,
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
        "c5_opening_executed_in_decision_count",
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
        "schema_version": "o2_c5_post_reconsideration_reference_decision_profile_v0",
        "profile_id": "o2_c5_post_reconsideration_reference_decision_profile_" + sha8(rollup),
        "status": status,
        "selected_next_unit": recommended_next,
        "decision": "execute C5 opening after C5 reconsideration reviewed reference closure",
        "weak_feedback_resolved": True,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
        "c5_open_decision_candidate_ready": True,
        "c5_opened": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Execute C5 opening next. This decision itself did not open C5.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_c5_post_reconsideration_reference_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The post-C5-reconsideration reference decision selected C5 opening execution as the next branch. The decision itself did not open C5 and did not run live audit.",
        "weak_feedback_resolved": True,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
        "c5_reconsideration_ready": True,
        "c5_open_decision_candidate_ready": True,
        "c5_opened": False,
        "live_feedback_audit_executed": False,
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_c5_post_reconsideration_reference_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c5_reconsideration_reference_closure",
                "question": "is C5 reconsideration closed as reviewed reference",
                "answer": "yes" if decision_pass else "no",
                "taken": "evaluate C5 opening execution branch",
            },
            {
                "step": "select_c5_opening_execution",
                "question": "what is the next lawful edge after reviewed C5 reconsideration",
                "answer": SELECTED_NEXT_UNIT if decision_pass else recommended_next,
                "taken": "authorize C5 opening execution next",
            },
            {
                "step": "preserve_decision_only_boundary",
                "question": "does this decision open C5",
                "answer": "no",
                "taken": "keep C5 unopened until selected execution unit",
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
        (C5_OPENING_AUTHORIZATION_PATH, c5_opening_authorization),
        (C5_OPENING_INPUT_SCOPE_PATH, c5_opening_input_scope),
        (C5_RECONSIDERATION_REFERENCE_CONTINUATION_PATH, readiness_continuation),
        (C5_OPENING_GUARD_CONTINUATION_PATH, opening_guard_continuation),
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
        "POST_C5_DECIDE_0_REFERENCE_CLOSURE_RECEIPT_CONSUMED": SOURCE_REFERENCE_CLOSURE_RECEIPT_PATH.exists(),
        "POST_C5_DECIDE_1_DECISION_BASIS_EMITTED": DECISION_BASIS_PATH.exists(),
        "POST_C5_DECIDE_2_C5_RECONSIDERATION_READY_REFERENCE_CONFIRMED": decision_basis["c5_reconsideration_ready"] is True,
        "POST_C5_DECIDE_3_C5_OPEN_DECISION_CANDIDATE_CONFIRMED": decision_basis["c5_open_decision_candidate_ready"] is True,
        "POST_C5_DECIDE_4_C5_OPENING_GUARD_CONFIRMED": decision_basis["c5_opened"] is False,
        "POST_C5_DECIDE_5_C5_OPENING_EXECUTION_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_C5_DECIDE_6_C5_OPENING_AUTHORIZATION_EMITTED": c5_opening_authorization["authorized_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_C5_DECIDE_7_NO_C5_OPENED_IN_DECISION": rollup["c5_opened_count"] == 0 and rollup["c5_opening_executed_in_decision_count"] == 0,
        "POST_C5_DECIDE_8_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "POST_C5_DECIDE_9_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "POST_C5_DECIDE_10_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "POST_C5_DECIDE_11_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "POST_C5_DECIDE_12_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_POST_C5_RECONSIDERATION_REFERENCE_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "selected_next_unit": recommended_next,
        "gate": gate,
        "c5_opened": False,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_c5_post_reconsideration_reference_decision_receipt_v0",
        "receipt_type": "TYPED_O2_C5_POST_RECONSIDERATION_REFERENCE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c5_reconsideration_reference_closure_receipt_id": SOURCE_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_o2_c5_post_reconsideration_reference_decision_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_c5_reconsideration_reference_decision_complete": decision_pass,
            "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
            "selected_next_unit": recommended_next,
            "c5_opening_authorized_next": decision_pass,
            "weak_feedback_resolved": True,
            "final_resolution_boundary_crossed": True,
            "final_resolution_records_frozen_count": 3,
            "resolution_records_emitted_count": 3,
            "c5_feedback_readiness": "C5_RECONSIDERATION_READY_PENDING_REVIEW",
            "c5_reconsideration_ready": True,
            "c5_open_decision_candidate_ready": True,
            "c5_opening_executed_in_decision": False,
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
            "c5_opening_authorization": rel(C5_OPENING_AUTHORIZATION_PATH),
            "c5_opening_input_scope": rel(C5_OPENING_INPUT_SCOPE_PATH),
            "c5_reconsideration_reference_continuation": rel(C5_RECONSIDERATION_REFERENCE_CONTINUATION_PATH),
            "c5_opening_guard_continuation": rel(C5_OPENING_GUARD_CONTINUATION_PATH),
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
    print(f"post_c5_reconsideration_reference_decision_receipt_id={receipt_id}")
    print(f"post_c5_reconsideration_reference_decision_receipt_path={rel(receipt_path)}")
    print(f"post_c5_reconsideration_reference_decision_basis_path={rel(DECISION_BASIS_PATH)}")
    print(f"c5_opening_selected_branch_path={rel(SELECTED_BRANCH_PATH)}")
    print(f"c5_opening_authorization_path={rel(C5_OPENING_AUTHORIZATION_PATH)}")
    print(f"post_c5_reconsideration_reference_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"post_c5_reconsideration_reference_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
