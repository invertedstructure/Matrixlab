#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_post_final_resolution_reference_decision.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / POST_FINAL_RESOLUTION_REFERENCE_DECISION"
MODE = "DECIDE_ONLY / SELECT_C5_RECONSIDERATION / WEAK_FEEDBACK_RESOLVED / NO_C5_OPEN"
BUILD_MODE = "O2_POST_FINAL_RESOLUTION_REFERENCE_DECISION_ONLY"

SOURCE_REFERENCE_CLOSURE_RECEIPT_ID = "01f38b19"

SOURCE_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0_receipts/01f38b19.json"

REFERENCE_CLOSURE_RECORD_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_resolution_closure_reference_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_resolution_closure_reviewed_reference_v0.json"
REFERENCE_INDEX_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_resolution_closure_reference_index_v0.json"
FINAL_RESOLUTION_RECORDS_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_weak_feedback_resolution_records_reference_v0.json"
RESOLVED_STATUS_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_weak_feedback_resolved_status_reference_v0.json"
FINAL_BOUNDARY_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_resolution_boundary_crossing_reference_v0.json"
C5_BLOCK_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_c5_block_pending_decision_reference_v0.json"
POST_REFERENCE_DECISION_READINESS_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_post_final_resolution_closure_reference_decision_readiness_v0.json"
REFERENCE_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_resolution_closure_reference_closure_authority_boundary_v0.json"
REFERENCE_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_resolution_closure_reference_closure_classification_v0.json"
REFERENCE_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_resolution_closure_reference_closure_rollup_v0.json"
REFERENCE_PROFILE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_resolution_closure_reference_closure_profile_v0.json"
REFERENCE_REPORT_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_resolution_closure_reference_closure_report.json"
REFERENCE_TRACE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0/o2_final_resolution_closure_reference_closure_transition_trace.json"

SOURCE_FINAL_REVIEW_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0_receipts/362cb1b2.json"
SOURCE_FINAL_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0_receipts/283a503b.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_REFERENCE_CLOSURE_RECEIPT_PATH,
    REFERENCE_CLOSURE_RECORD_PATH,
    REVIEWED_REFERENCE_PATH,
    REFERENCE_INDEX_PATH,
    FINAL_RESOLUTION_RECORDS_REFERENCE_PATH,
    RESOLVED_STATUS_REFERENCE_PATH,
    FINAL_BOUNDARY_REFERENCE_PATH,
    C5_BLOCK_REFERENCE_PATH,
    POST_REFERENCE_DECISION_READINESS_PATH,
    REFERENCE_AUTHORITY_PATH,
    REFERENCE_CLASSIFICATION_PATH,
    REFERENCE_ROLLUP_PATH,
    REFERENCE_PROFILE_PATH,
    REFERENCE_REPORT_PATH,
    REFERENCE_TRACE_PATH,
    SOURCE_FINAL_REVIEW_RECEIPT_PATH,
    SOURCE_FINAL_CLOSURE_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_post_final_resolution_reference_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "o2_post_final_resolution_reference_decision_basis_v0.json"
DECISION_TABLE_PATH = OUT_DIR / "o2_post_final_resolution_reference_decision_table_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "o2_c5_reconsideration_selected_branch_v0.json"
C5_RECONSIDERATION_AUTHORIZATION_PATH = OUT_DIR / "o2_c5_reconsideration_authorization_v0.json"
C5_INPUT_SCOPE_PATH = OUT_DIR / "o2_c5_reconsideration_input_scope_v0.json"
RESOLVED_REFERENCE_CONTINUATION_PATH = OUT_DIR / "o2_resolved_weak_feedback_reference_continuation_v0.json"
C5_BLOCK_CONTINUATION_PATH = OUT_DIR / "o2_c5_block_continuation_until_execution_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "o2_post_final_resolution_reference_deferred_branches_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_post_final_resolution_reference_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_post_final_resolution_reference_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_post_final_resolution_reference_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_post_final_resolution_reference_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_post_final_resolution_reference_decision_report.json"
TRACE_PATH = OUT_DIR / "o2_post_final_resolution_reference_decision_transition_trace.json"

EXPECTED_REFERENCE_STATUS = "TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_CLOSED_AS_REVIEWED_REFERENCE_C5_DECISION_READY"
EXPECTED_REFERENCE_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_CLOSED_AS_REVIEWED_REFERENCE_C5_DECISION_READY"
EXPECTED_REFERENCE_NEXT = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REFERENCE_CLOSURE_V0"

SELECTED_BRANCH = "EXECUTE_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION"
SELECTED_NEXT_UNIT = "EXECUTE_O2_C5_RECONSIDERATION_AFTER_WEAK_FEEDBACK_RESOLUTION_V0"

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
    summary = receipt.get("machine_readable_o2_weak_feedback_final_resolution_closure_reference_closure_summary", {})
    closure_record = read_json(REFERENCE_CLOSURE_RECORD_PATH)
    reviewed_reference = read_json(REVIEWED_REFERENCE_PATH)
    reference_index = read_json(REFERENCE_INDEX_PATH)
    final_resolution_reference = read_json(FINAL_RESOLUTION_RECORDS_REFERENCE_PATH)
    resolved_reference = read_json(RESOLVED_STATUS_REFERENCE_PATH)
    boundary_reference = read_json(FINAL_BOUNDARY_REFERENCE_PATH)
    c5_reference = read_json(C5_BLOCK_REFERENCE_PATH)
    decision_readiness = read_json(POST_REFERENCE_DECISION_READINESS_PATH)
    authority = read_json(REFERENCE_AUTHORITY_PATH)
    classification = read_json(REFERENCE_CLASSIFICATION_PATH)
    rollup = read_json(REFERENCE_ROLLUP_PATH)
    profile = read_json(REFERENCE_PROFILE_PATH)
    report = read_json(REFERENCE_REPORT_PATH)
    trace = read_json(REFERENCE_TRACE_PATH)
    final_review_receipt = read_json(SOURCE_FINAL_REVIEW_RECEIPT_PATH)
    final_closure_receipt = read_json(SOURCE_FINAL_CLOSURE_RECEIPT_PATH)

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
        "final_resolution_closure_closed_as_reviewed_reference",
        "reviewed_reference_emitted",
        "post_final_resolution_reference_decision_ready",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    if summary.get("final_resolution_records_frozen_count") != 3:
        failures.append("summary_final_resolution_count_wrong")
    if summary.get("resolution_records_emitted_count") != 3:
        failures.append("summary_resolution_count_wrong")

    for key in [
        "parking_counted_as_resolution",
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
        if summary.get(key) is not False:
            failures.append(f"summary_forbidden_true:{key}")

    if summary.get("c5_feedback_readiness") != "BLOCKED_PENDING_C5_DECISION":
        failures.append("summary_c5_wrong")
    if closure_record.get("closure_status") != "CLOSED_AS_REVIEWED_REFERENCE_C5_DECISION_READY":
        failures.append("closure_record_status_wrong")
    if reviewed_reference.get("weak_feedback_resolved") is not True or reviewed_reference.get("final_resolution_boundary_crossed") is not True:
        failures.append("reviewed_reference_resolution_wrong")
    if reviewed_reference.get("c5_opened") is not False or reviewed_reference.get("c5_reconsideration_ready") is not False:
        failures.append("reviewed_reference_c5_wrong")
    if reviewed_reference.get("post_reference_closure_decision_ready") is not True:
        failures.append("reviewed_reference_decision_not_ready")
    if reference_index.get("index_status") != "REFERENCE_INDEX_EMITTED":
        failures.append("reference_index_wrong")
    if final_resolution_reference.get("final_resolution_records_count") != 3:
        failures.append("final_resolution_reference_count_wrong")
    if final_resolution_reference.get("all_final_resolution_records_closed") is not True:
        failures.append("final_resolution_reference_not_closed")
    if final_resolution_reference.get("all_weak_feedback_resolved") is not True:
        failures.append("final_resolution_reference_not_resolved")
    if final_resolution_reference.get("all_c5_not_ready_not_open") is not True:
        failures.append("final_resolution_reference_c5_wrong")
    if resolved_reference.get("weak_feedback_resolved") is not True or resolved_reference.get("resolution_records_emitted_count") != 3:
        failures.append("resolved_reference_wrong")
    if resolved_reference.get("c5_opened") is not False or resolved_reference.get("c5_reconsideration_ready") is not False:
        failures.append("resolved_reference_c5_wrong")
    if boundary_reference.get("final_resolution_boundary_crossed") is not True or boundary_reference.get("weak_feedback_resolved") is not True:
        failures.append("boundary_reference_wrong")
    if boundary_reference.get("parking_counted_as_resolution") is not False:
        failures.append("boundary_parking_wrong")
    if c5_reference.get("c5_feedback_readiness") != "BLOCKED_PENDING_C5_DECISION":
        failures.append("c5_reference_readiness_wrong")
    if c5_reference.get("c5_opened") is not False or c5_reference.get("c5_reconsideration_ready") is not False:
        failures.append("c5_reference_wrong")
    if c5_reference.get("post_final_resolution_reference_decision_required") is not True:
        failures.append("c5_reference_decision_requirement_missing")
    if decision_readiness.get("decision_ready") is not True:
        failures.append("post_reference_decision_readiness_false")
    if authority.get("may_decide_next_after_final_resolution_closure_reference_closure") is not True:
        failures.append("authority_no_decide")
    if authority.get("may_open_c5_now") is not False or authority.get("may_set_c5_reconsideration_ready_now") is not False:
        failures.append("authority_allows_c5_now")
    if classification.get("recommended_next") != EXPECTED_REFERENCE_NEXT:
        failures.append("classification_next_wrong")
    if rollup.get("post_final_resolution_reference_decision_ready_count") != 1:
        failures.append("rollup_decision_ready_wrong")
    if rollup.get("weak_feedback_resolved_count") != 1 or rollup.get("final_resolution_boundary_crossed_count") != 1:
        failures.append("rollup_resolution_wrong")
    if rollup.get("c5_opened_count") != 0 or rollup.get("c5_reconsideration_ready_count") != 0:
        failures.append("rollup_c5_wrong")
    if profile.get("post_final_resolution_reference_decision_ready") is not True or profile.get("next_command_goal") is not None:
        failures.append("profile_wrong")
    if report.get("recommended_next_handling") != EXPECTED_REFERENCE_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_REFERENCE_STOP:
        failures.append("trace_stop_wrong")
    if final_review_receipt.get("receipt_id") != "362cb1b2" or final_review_receipt.get("gate") != "PASS":
        failures.append("final_review_receipt_wrong")
    if final_closure_receipt.get("receipt_id") != "283a503b" or final_closure_receipt.get("gate") != "PASS":
        failures.append("final_closure_receipt_wrong")

    return failures, {
        "summary": summary,
        "reviewed_reference": reviewed_reference,
        "resolved_reference": resolved_reference,
        "boundary_reference": boundary_reference,
        "c5_reference": c5_reference,
        "decision_readiness": decision_readiness,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    decision_pass = not failures
    status = "TYPED_O2_POST_FINAL_RESOLUTION_REFERENCE_DECISION_SELECTED_C5_RECONSIDERATION_READY" if decision_pass else "TYPED_O2_POST_FINAL_RESOLUTION_REFERENCE_DECISION_GATE_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_O2_POST_FINAL_RESOLUTION_REFERENCE_DECISION_V0"

    reason_codes = [
        "POST_FINAL_RESOLUTION_REFERENCE_DECISION_COMPLETE",
        "FINAL_RESOLUTION_REFERENCE_CLOSURE_RECEIPT_CONSUMED",
        "WEAK_FEEDBACK_RESOLVED_REFERENCE_CONFIRMED",
        "FINAL_RESOLUTION_BOUNDARY_REFERENCE_CONFIRMED",
        "FINAL_RESOLUTION_RECORDS_REFERENCE_CONFIRMED",
        "C5_BLOCK_REFERENCE_CONFIRMED",
        "C5_RECONSIDERATION_SELECTED_NEXT",
        "NO_C5_RECONSIDERATION_READY_IN_DECISION",
        "NO_C5_OPENED_IN_DECISION",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if decision_pass else failures

    decision_basis = {
        "schema_version": "o2_post_final_resolution_reference_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_reference_closure_receipt_id": SOURCE_REFERENCE_CLOSURE_RECEIPT_ID,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "post_final_resolution_reference_decision_ready": decision_pass,
    }

    decision_table = {
        "schema_version": "o2_post_final_resolution_reference_decision_table_v0",
        "decision_status": "NEXT_BRANCH_SELECTED" if decision_pass else "NO_BRANCH_SELECTED",
        "records": [
            {
                "branch": SELECTED_BRANCH,
                "selected": decision_pass,
                "next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
                "why": "Weak feedback has final-resolution closure frozen as reviewed reference; C5 remains blocked pending explicit reconsideration.",
            },
            {
                "branch": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "This decision selects C5 reconsideration execution; it does not itself open C5.",
            },
            {
                "branch": "RUN_LIVE_FEEDBACK_AUDIT_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Live feedback audit is separate from this post-final-resolution reference decision.",
            },
            {
                "branch": "REPAIR_OR_RETRY",
                "selected": False,
                "next_unit": None,
                "why": "No failure is present in the final-resolution reference closure receipt.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "o2_c5_reconsideration_selected_branch_v0",
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "selection_scope": "C5 reconsideration after weak-feedback final-resolution reference closure",
        "selection_reason": "Weak feedback is resolved and frozen as a reviewed reference; C5 may now be reconsidered by an explicit execution unit.",
        "selected_branch_does_not": [
            "open C5",
            "set C5 reconsideration ready",
            "run live feedback audit",
            "repair",
            "retry",
            "patch runtime",
            "mutate source",
            "mutate prior receipts",
            "change architecture",
        ],
    }

    c5_authorization = {
        "schema_version": "o2_c5_reconsideration_authorization_v0",
        "authorization_status": "C5_RECONSIDERATION_AUTHORIZED_NEXT" if decision_pass else "NOT_AUTHORIZED",
        "authorized_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "authorized_execution_mode": "C5_RECONSIDERATION_FROM_FROZEN_FINAL_RESOLUTION_REFERENCE" if decision_pass else None,
        "authorized_scope": [
            "consume final-resolution closure reviewed reference",
            "verify weak feedback resolved",
            "verify C5 remains blocked before reconsideration",
            "decide whether C5 reconsideration readiness can be emitted",
        ],
        "not_authorized_in_this_decision": [
            "set C5 reconsideration ready",
            "open C5",
            "run live feedback audit",
            "repair",
            "retry",
            "patch runtime",
            "mutate source",
            "mutate prior receipts",
        ],
    }

    c5_input_scope = {
        "schema_version": "o2_c5_reconsideration_input_scope_v0",
        "scope_status": "FROZEN_FINAL_RESOLUTION_REFERENCE_ELIGIBLE_FOR_C5_RECONSIDERATION_EXECUTION",
        "source_reference_closure_receipt": rel(SOURCE_REFERENCE_CLOSURE_RECEIPT_PATH),
        "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
        "resolved_status_reference": rel(RESOLVED_STATUS_REFERENCE_PATH),
        "final_boundary_reference": rel(FINAL_BOUNDARY_REFERENCE_PATH),
        "c5_block_reference": rel(C5_BLOCK_REFERENCE_PATH),
        "post_reference_decision_readiness": rel(POST_REFERENCE_DECISION_READINESS_PATH),
        "weak_feedback_resolved": True,
        "final_resolution_records_frozen_count": 3,
    }

    resolved_continuation = {
        "schema_version": "o2_resolved_weak_feedback_reference_continuation_v0",
        "weak_feedback_resolved": True,
        "resolved_status_preserved": True,
        "final_resolution_boundary_crossed": True,
        "resolution_records_emitted_count": 3,
        "decision_emitted_new_resolution_records": False,
    }

    c5_block_continuation = {
        "schema_version": "o2_c5_block_continuation_until_execution_v0",
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "block_continues_until_selected_execution_unit": True,
        "selected_execution_unit": SELECTED_NEXT_UNIT if decision_pass else None,
    }

    deferred_branches = {
        "schema_version": "o2_post_final_resolution_reference_deferred_branches_v0",
        "deferred": [
            "OPEN_C5_NOW",
            "LIVE_FEEDBACK_AUDIT_NOW",
            "REPAIR",
            "RETRY",
            "RUNTIME_PATCH",
            "SOURCE_MUTATION",
            "ARCHITECTURE_CHANGE",
        ],
        "why": "This unit only selects C5 reconsideration execution as the next lawful branch.",
    }

    authority_boundary = {
        "schema_version": "o2_post_final_resolution_reference_decision_authority_boundary_v0",
        "status": status,
        "may_execute_c5_reconsideration_next": decision_pass,
        "may_set_c5_reconsideration_ready_now_in_decision": False,
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
        "schema_version": "o2_post_final_resolution_reference_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_final_resolution_reference_decision_complete": decision_pass,
        "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": recommended_next,
        "c5_reconsideration_authorized_next": decision_pass,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": False,
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
        "schema_version": "o2_post_final_resolution_reference_decision_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "decision_count": 1 if decision_pass else 0,
        "selected_c5_reconsideration_count": 1 if decision_pass else 0,
        "c5_reconsideration_authorized_next_count": 1 if decision_pass else 0,
        "weak_feedback_resolved_count": 1,
        "final_resolution_boundary_crossed_count": 1,
        "final_resolution_records_frozen_count": 3,
        "resolution_records_emitted_count": 3,
        "c5_opened_count": 0,
        "c5_reconsideration_ready_count": 0,
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
        "c5_reconsideration_ready_count",
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
        "schema_version": "o2_post_final_resolution_reference_decision_profile_v0",
        "profile_id": "o2_post_final_resolution_reference_decision_profile_" + sha8(rollup),
        "status": status,
        "selected_next_unit": recommended_next,
        "decision": "execute C5 reconsideration after weak-feedback final-resolution reference closure",
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Execute C5 reconsideration next. Do not treat this decision as C5 readiness or C5 opening.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_post_final_resolution_reference_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The post-final-resolution reference decision selected C5 reconsideration as the next branch. The decision itself does not set C5 readiness and does not open C5.",
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "resolution_records_emitted_count": 3,
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_post_final_resolution_reference_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_final_resolution_reference_closure",
                "question": "is weak feedback resolved and frozen as reviewed reference",
                "answer": "yes" if decision_pass else "no",
                "taken": "evaluate C5 reconsideration branch",
            },
            {
                "step": "select_c5_reconsideration",
                "question": "what is the next lawful edge after weak-feedback resolution",
                "answer": SELECTED_NEXT_UNIT if decision_pass else recommended_next,
                "taken": "authorize C5 reconsideration execution next",
            },
            {
                "step": "preserve_c5_block_in_decision",
                "question": "does this decision open C5",
                "answer": "no",
                "taken": "keep C5 blocked until execution unit",
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
        (C5_RECONSIDERATION_AUTHORIZATION_PATH, c5_authorization),
        (C5_INPUT_SCOPE_PATH, c5_input_scope),
        (RESOLVED_REFERENCE_CONTINUATION_PATH, resolved_continuation),
        (C5_BLOCK_CONTINUATION_PATH, c5_block_continuation),
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
        "POST_FINAL_DECIDE_0_REFERENCE_CLOSURE_RECEIPT_CONSUMED": SOURCE_REFERENCE_CLOSURE_RECEIPT_PATH.exists(),
        "POST_FINAL_DECIDE_1_DECISION_BASIS_EMITTED": DECISION_BASIS_PATH.exists(),
        "POST_FINAL_DECIDE_2_WEAK_FEEDBACK_RESOLVED_REFERENCE_CONFIRMED": decision_basis["weak_feedback_resolved"] is True,
        "POST_FINAL_DECIDE_3_FINAL_BOUNDARY_CONFIRMED": decision_basis["final_resolution_boundary_crossed"] is True,
        "POST_FINAL_DECIDE_4_FINAL_RESOLUTION_RECORDS_CONFIRMED": decision_basis["final_resolution_records_frozen_count"] == 3,
        "POST_FINAL_DECIDE_5_C5_BLOCK_CONFIRMED": decision_basis["c5_opened"] is False and decision_basis["c5_reconsideration_ready"] is False,
        "POST_FINAL_DECIDE_6_C5_RECONSIDERATION_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_FINAL_DECIDE_7_C5_RECONSIDERATION_AUTHORIZATION_EMITTED": c5_authorization["authorized_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_FINAL_DECIDE_8_NO_C5_READY_IN_DECISION": rollup["c5_reconsideration_ready_count"] == 0,
        "POST_FINAL_DECIDE_9_NO_C5_OPENED_IN_DECISION": rollup["c5_opened_count"] == 0,
        "POST_FINAL_DECIDE_10_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "POST_FINAL_DECIDE_11_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "POST_FINAL_DECIDE_12_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "POST_FINAL_DECIDE_13_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "POST_FINAL_DECIDE_14_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_POST_FINAL_RESOLUTION_REFERENCE_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "selected_next_unit": recommended_next,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_post_final_resolution_reference_decision_receipt_v0",
        "receipt_type": "TYPED_O2_POST_FINAL_RESOLUTION_REFERENCE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_final_resolution_closure_reference_closure_receipt_id": SOURCE_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_o2_post_final_resolution_reference_decision_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_final_resolution_reference_decision_complete": decision_pass,
            "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
            "selected_next_unit": recommended_next,
            "c5_reconsideration_authorized_next": decision_pass,
            "weak_feedback_resolved": True,
            "final_resolution_boundary_crossed": True,
            "final_resolution_records_frozen_count": 3,
            "resolution_records_emitted_count": 3,
            "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
            "c5_reconsideration_ready": False,
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
            "c5_reconsideration_authorization": rel(C5_RECONSIDERATION_AUTHORIZATION_PATH),
            "c5_input_scope": rel(C5_INPUT_SCOPE_PATH),
            "resolved_reference_continuation": rel(RESOLVED_REFERENCE_CONTINUATION_PATH),
            "c5_block_continuation": rel(C5_BLOCK_CONTINUATION_PATH),
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
    print(f"post_final_resolution_reference_decision_receipt_id={receipt_id}")
    print(f"post_final_resolution_reference_decision_receipt_path={rel(receipt_path)}")
    print(f"post_final_resolution_reference_decision_basis_path={rel(DECISION_BASIS_PATH)}")
    print(f"c5_reconsideration_selected_branch_path={rel(SELECTED_BRANCH_PATH)}")
    print(f"c5_reconsideration_authorization_path={rel(C5_RECONSIDERATION_AUTHORIZATION_PATH)}")
    print(f"post_final_resolution_reference_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"post_final_resolution_reference_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
