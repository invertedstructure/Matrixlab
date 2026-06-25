#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_proposal_emission_post_closure_decision.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_POST_CLOSURE_DECISION"
MODE = "DECIDE_ONLY / SELECT_PROPOSED_RECORD_REVIEW / NO_REVIEWED_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_POST_CLOSURE_DECISION_ONLY"

SOURCE_CLOSURE_RECEIPT_ID = "922ef93d"

CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0_receipts/922ef93d.json"
CLOSURE_RECORD_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_reviewed_reference_v0.json"
PROPOSED_RECORD_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposed_record_inventory_freeze_v0.json"
PROPOSED_RESOLUTION_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposed_weak_feedback_resolution_record_freeze_v0.json"
ROUTE_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_route_freeze_v0.json"
BOUNDARY_LOCK_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_review_boundary_lock_v0.json"
UNRESOLVED_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_unresolved_status_freeze_v0.json"
C5_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_c5_block_freeze_v0.json"
RECEIPT_CHAIN_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_receipt_chain_v0.json"
CLOSURE_DECISION_TABLE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_closure_downstream_decision_table_v0.json"
CLOSURE_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_closure_authority_boundary_v0.json"
CLOSURE_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_closure_classification_v0.json"
CLOSURE_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_closure_rollup_v0.json"
CLOSURE_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_closure_profile_v0.json"
CLOSURE_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_closure_report.json"
CLOSURE_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_closure_transition_trace.json"

QA_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_question_answer_records_v0.jsonl"
SOURCE_REF_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_source_ref_satisfaction_records_v0.jsonl"
UNDERTYPED_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_under_typed_acceptance_review_records_v0.jsonl"
PARKING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_parking_execution_continuation_records_v0.jsonl"
PROPOSED_RESOLUTION_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_weak_feedback_resolution_records_v0.jsonl"
EMISSION_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_weak_feedback_resolution_proposal_emission_route_map_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    CLOSURE_RECEIPT_PATH,
    CLOSURE_RECORD_PATH,
    REVIEWED_REFERENCE_PATH,
    PROPOSED_RECORD_FREEZE_PATH,
    PROPOSED_RESOLUTION_FREEZE_PATH,
    ROUTE_FREEZE_PATH,
    BOUNDARY_LOCK_PATH,
    UNRESOLVED_FREEZE_PATH,
    C5_FREEZE_PATH,
    RECEIPT_CHAIN_PATH,
    CLOSURE_DECISION_TABLE_PATH,
    CLOSURE_AUTHORITY_PATH,
    CLOSURE_CLASSIFICATION_PATH,
    CLOSURE_ROLLUP_PATH,
    CLOSURE_PROFILE_PATH,
    CLOSURE_REPORT_PATH,
    CLOSURE_TRACE_PATH,
    QA_RECORDS_PATH,
    SOURCE_REF_RECORDS_PATH,
    UNDERTYPED_RECORDS_PATH,
    PARKING_RECORDS_PATH,
    PROPOSED_RESOLUTION_RECORDS_PATH,
    EMISSION_ROUTE_MAP_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "o2_proposal_emission_post_closure_decision_basis_v0.json"
DECISION_TABLE_PATH = OUT_DIR / "o2_proposal_emission_post_closure_decision_table_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "o2_proposal_emission_selected_next_branch_v0.json"
PROPOSED_RECORD_REVIEW_AUTH_PATH = OUT_DIR / "o2_proposed_record_review_authorization_v0.json"
PROPOSED_RECORD_INPUT_SCOPE_PATH = OUT_DIR / "o2_proposed_record_review_input_scope_v0.json"
UNRESOLVED_CONTINUATION_PATH = OUT_DIR / "o2_proposal_emission_post_closure_unresolved_continuation_v0.json"
C5_BLOCK_CONTINUATION_PATH = OUT_DIR / "o2_proposal_emission_post_closure_c5_block_continuation_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "o2_proposal_emission_post_closure_deferred_branches_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_proposal_emission_post_closure_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_proposal_emission_post_closure_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_proposal_emission_post_closure_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_proposal_emission_post_closure_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_proposal_emission_post_closure_decision_report.json"
TRACE_PATH = OUT_DIR / "o2_proposal_emission_post_closure_decision_transition_trace.json"

EXPECTED_CLOSURE_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED_DECISION_READY"
EXPECTED_CLOSURE_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED_DECISION_READY"
EXPECTED_CLOSURE_NEXT = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REFERENCE_CLOSURE_V0"

SELECTED_BRANCH = "EXECUTE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW"
SELECTED_NEXT_UNIT = "EXECUTE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_V0"

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

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(CLOSURE_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_resolution_proposal_emission_closure_summary", {})
    closure_record = read_json(CLOSURE_RECORD_PATH)
    reviewed_reference = read_json(REVIEWED_REFERENCE_PATH)
    proposed_record_freeze = read_json(PROPOSED_RECORD_FREEZE_PATH)
    proposed_resolution_freeze = read_json(PROPOSED_RESOLUTION_FREEZE_PATH)
    route_freeze = read_json(ROUTE_FREEZE_PATH)
    boundary_lock = read_json(BOUNDARY_LOCK_PATH)
    unresolved_freeze = read_json(UNRESOLVED_FREEZE_PATH)
    c5_freeze = read_json(C5_FREEZE_PATH)
    closure_authority = read_json(CLOSURE_AUTHORITY_PATH)
    closure_classification = read_json(CLOSURE_CLASSIFICATION_PATH)
    closure_rollup = read_json(CLOSURE_ROLLUP_PATH)
    closure_profile = read_json(CLOSURE_PROFILE_PATH)
    closure_report = read_json(CLOSURE_REPORT_PATH)
    closure_trace = read_json(CLOSURE_TRACE_PATH)

    qa_records = read_jsonl(QA_RECORDS_PATH)
    source_records = read_jsonl(SOURCE_REF_RECORDS_PATH)
    undertyped_records = read_jsonl(UNDERTYPED_RECORDS_PATH)
    parking_records = read_jsonl(PARKING_RECORDS_PATH)
    proposed_resolution_records = read_jsonl(PROPOSED_RESOLUTION_RECORDS_PATH)
    route_records = read_jsonl(EMISSION_ROUTE_MAP_PATH)

    if receipt.get("receipt_id") != SOURCE_CLOSURE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("proposal_emission_closure_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_CLOSURE_STOP:
        failures.append("proposal_emission_closure_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("proposal_emission_closure_hidden_next_command")
    if summary.get("status") != EXPECTED_CLOSURE_STATUS:
        failures.append(f"proposal_emission_closure_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_CLOSURE_NEXT:
        failures.append(f"proposal_emission_closure_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "proposal_emission_closed_as_reviewed_reference",
        "reviewed_reference_emitted",
        "post_closure_decision_ready",
        "proposed_records_frozen_as_unreviewed",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "proposed_question_answer_records_frozen_count": 3,
        "proposed_source_ref_satisfaction_records_frozen_count": 2,
        "proposed_under_typed_acceptance_review_records_frozen_count": 2,
        "parking_execution_continuation_records_frozen_count": 3,
        "proposed_resolution_records_frozen_count": 3,
        "proposal_emission_route_records_frozen_count": 3,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    for key in [
        "proposal_review_boundary_crossed",
        "weak_feedback_resolved",
        "question_packets_answered",
        "source_ref_requests_satisfied",
        "under_typed_acceptance_approved",
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

    if summary.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("summary_c5_not_blocked")
    if closure_record.get("closure_status") != "CLOSED_AS_REVIEWED_REFERENCE_PROPOSED_RECORDS_UNREVIEWED":
        failures.append("closure_record_wrong")
    if reviewed_reference.get("proposed_records_remain_unreviewed") is not True:
        failures.append("reviewed_reference_records_not_unreviewed")
    if reviewed_reference.get("reviewed_resolution_records_emitted_count") != 0 or reviewed_reference.get("weak_feedback_resolved") is not False:
        failures.append("reviewed_reference_promoted_or_resolved")
    if proposed_record_freeze.get("all_proposed_records_unreviewed") is not True:
        failures.append("proposed_record_freeze_wrong")
    if proposed_resolution_freeze.get("reviewed_resolution_records_emitted_count") != 0 or proposed_resolution_freeze.get("weak_feedback_resolved") is not False:
        failures.append("proposed_resolution_freeze_wrong")
    if route_freeze.get("all_reviewed_record_emitted_false") is not True or route_freeze.get("all_unresolved") is not True:
        failures.append("route_freeze_wrong")
    if boundary_lock.get("proposal_layer_crossed_into_review_layer") is not False:
        failures.append("boundary_lock_crossed")
    if unresolved_freeze.get("weak_feedback_resolved") is not False or unresolved_freeze.get("resolution_records_emitted_count") != 0:
        failures.append("unresolved_freeze_wrong")
    if c5_freeze.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_freeze.get("c5_opened") is not False:
        failures.append("c5_freeze_wrong")
    if closure_authority.get("may_decide_next_after_proposal_emission_reference_closure") is not True:
        failures.append("closure_authority_no_decide")
    if closure_authority.get("may_emit_reviewed_resolution_records_now") is not False or closure_authority.get("may_open_c5") is not False:
        failures.append("closure_authority_allows_reviewed_or_c5")
    if closure_classification.get("recommended_next") != EXPECTED_CLOSURE_NEXT:
        failures.append("closure_classification_next_wrong")
    if closure_rollup.get("post_closure_decision_ready_count") != 1:
        failures.append("closure_rollup_decision_ready_wrong")
    if closure_profile.get("proposal_emission_closed_as_reviewed_reference") is not True or closure_profile.get("next_command_goal") is not None:
        failures.append("closure_profile_wrong")
    if closure_report.get("recommended_next_handling") != EXPECTED_CLOSURE_NEXT:
        failures.append("closure_report_next_wrong")
    if closure_trace.get("terminal", {}).get("stop_code") != EXPECTED_CLOSURE_STOP:
        failures.append("closure_trace_stop_wrong")

    if len(qa_records) != 3 or len(source_records) != 2 or len(undertyped_records) != 2 or len(parking_records) != 3 or len(proposed_resolution_records) != 3 or len(route_records) != 3:
        failures.append("source_record_counts_wrong")

    for row in proposed_resolution_records:
        if row.get("proposal_status") != "PROPOSED_UNREVIEWED" or row.get("review_status") != "UNREVIEWED":
            failures.append(f"proposed_resolution_status_wrong:{row.get('proposed_resolution_id')}")
        if row.get("counts_as_reviewed_resolution") is not False or row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"proposed_resolution_boundary_wrong:{row.get('proposed_resolution_id')}")

    for row in route_records:
        if row.get("proposed_record_emitted") is not True or row.get("reviewed_record_emitted") is not False:
            failures.append(f"route_flags_wrong:{row.get('emission_route_record_id')}")
        if row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"route_boundary_wrong:{row.get('emission_route_record_id')}")

    return failures, {
        "qa_records": qa_records,
        "source_records": source_records,
        "undertyped_records": undertyped_records,
        "parking_records": parking_records,
        "proposed_resolution_records": proposed_resolution_records,
        "route_records": route_records,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    qa_records = src.get("qa_records", [])
    source_records = src.get("source_records", [])
    undertyped_records = src.get("undertyped_records", [])
    parking_records = src.get("parking_records", [])
    proposed_resolution_records = src.get("proposed_resolution_records", [])
    route_records = src.get("route_records", [])

    decision_pass = not failures
    status = "TYPED_O2_PROPOSAL_EMISSION_POST_CLOSURE_DECISION_SELECTED_PROPOSED_RECORD_REVIEW_READY" if decision_pass else "TYPED_O2_PROPOSAL_EMISSION_POST_CLOSURE_DECISION_BASIS_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_O2_PROPOSAL_EMISSION_POST_CLOSURE_DECISION_BASIS_V0"

    reason_codes = [
        "PROPOSAL_EMISSION_POST_CLOSURE_DECISION_EMITTED",
        "PROPOSAL_EMISSION_CLOSURE_RECEIPT_CONSUMED",
        "PROPOSED_RECORD_REFERENCE_CONFIRMED",
        "PROPOSED_RECORDS_FROZEN_UNREVIEWED_CONFIRMED",
        "ZERO_REVIEWED_RESOLUTION_RECORDS_CONFIRMED",
        "UNRESOLVED_STATUS_CONFIRMED",
        "C5_BLOCK_CONFIRMED",
        "PROPOSED_RECORD_REVIEW_SELECTED_NEXT",
        "NO_RECORD_REVIEW_EXECUTED_IN_DECISION",
        "NO_REVIEWED_RESOLUTION_RECORDS_EMITTED",
        "NO_WEAK_FEEDBACK_RESOLUTION_RECORDED",
        "NO_QUESTION_PACKET_ANSWERED_AS_REVIEWED",
        "NO_SOURCE_REF_REQUEST_SATISFIED_AS_REVIEWED",
        "NO_UNDER_TYPED_ACCEPTANCE_APPROVED_AS_REVIEWED",
        "NO_PARKING_COUNTED_AS_RESOLUTION",
        "NO_C5_RECONSIDERATION_READY",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if decision_pass else failures

    decision_basis = {
        "schema_version": "o2_proposal_emission_post_closure_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_proposal_emission_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "proposal_emission_closed_as_reviewed_reference": decision_pass,
        "proposed_records_frozen_as_unreviewed": decision_pass,
        "proposed_question_answer_records_available_count": len(qa_records),
        "proposed_source_ref_satisfaction_records_available_count": len(source_records),
        "proposed_under_typed_acceptance_review_records_available_count": len(undertyped_records),
        "parking_execution_continuation_records_available_count": len(parking_records),
        "proposed_resolution_records_available_count": len(proposed_resolution_records),
        "proposal_emission_route_records_available_count": len(route_records),
        "record_review_executed_in_decision": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    decision_table = {
        "schema_version": "o2_proposal_emission_post_closure_decision_table_v0",
        "decision_status": "NEXT_BRANCH_SELECTED" if decision_pass else "NO_BRANCH_SELECTED",
        "records": [
            {
                "branch": SELECTED_BRANCH,
                "selected": decision_pass,
                "next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
                "why": "Frozen proposed records exist and passed emission-integrity review. The next lawful edge is to review/accept or reject proposed records under explicit boundaries.",
            },
            {
                "branch": "MARK_WEAK_FEEDBACK_RESOLVED_NOW",
                "selected": False,
                "next_unit": None,
                "why": "No reviewed resolution records exist yet.",
            },
            {
                "branch": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 remains blocked until reviewed resolution exists and a later decision explicitly selects C5 reconsideration.",
            },
            {
                "branch": "RUN_LIVE_FEEDBACK_AUDIT_NOW",
                "selected": False,
                "next_unit": None,
                "why": "This branch is still inside frozen proposed-record review mechanics, not live feedback audit.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "o2_proposal_emission_selected_next_branch_v0",
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "selection_scope": "proposed record review only",
        "selection_reason": "Proposed records are now frozen as unreviewed. The next bounded unit may review proposed records and emit reviewed-resolution artifacts only if it proves the required boundaries.",
        "selected_branch_does_not": [
            "emit reviewed resolution records in this decision unit",
            "mark weak feedback resolved in this decision unit",
            "answer question packets as reviewed",
            "satisfy source-ref requests as reviewed",
            "approve under-typed acceptance as reviewed",
            "count parking as resolution",
            "run live audit",
            "repair",
            "retry",
            "patch runtime",
            "mutate sources",
            "open C5",
        ],
    }

    review_authorization = {
        "schema_version": "o2_proposed_record_review_authorization_v0",
        "authorization_status": "PROPOSED_RECORD_REVIEW_AUTHORIZED_NEXT" if decision_pass else "NOT_AUTHORIZED",
        "authorized_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "authorized_execution_mode": "PROPOSED_RECORD_REVIEW_ONLY / FROM_FROZEN_PROPOSED_RECORDS / NO_C5" if decision_pass else None,
        "authorized_scope": [
            "review proposed question-answer records",
            "review proposed source-ref satisfaction records",
            "review proposed under-typed acceptance review records",
            "review parking continuation records as parked unresolved or reject them",
            "review proposed weak-feedback resolution records",
            "emit explicit reviewed-record artifacts only inside the next execution unit if gates pass",
            "preserve c5_reconsideration_ready=false unless a later C5 decision unit explicitly changes it",
        ],
        "not_authorized_in_this_decision": [
            "emit reviewed resolution records",
            "mark weak feedback resolved",
            "treat proposed records as reviewed records",
            "count parking as resolution",
            "run live audit",
            "repair",
            "retry",
            "patch runtime",
            "mutate sources",
            "open C5",
        ],
    }

    input_scope = {
        "schema_version": "o2_proposed_record_review_input_scope_v0",
        "scope_status": "FROZEN_PROPOSED_RECORDS_ELIGIBLE_FOR_LATER_REVIEW",
        "proposed_question_answer_records_count": len(qa_records),
        "proposed_source_ref_satisfaction_records_count": len(source_records),
        "proposed_under_typed_acceptance_review_records_count": len(undertyped_records),
        "parking_execution_continuation_records_count": len(parking_records),
        "proposed_resolution_records_count": len(proposed_resolution_records),
        "proposal_emission_route_records_count": len(route_records),
        "input_sources": {
            "proposed_question_answer_records": rel(QA_RECORDS_PATH),
            "proposed_source_ref_satisfaction_records": rel(SOURCE_REF_RECORDS_PATH),
            "proposed_under_typed_acceptance_review_records": rel(UNDERTYPED_RECORDS_PATH),
            "parking_execution_continuation_records": rel(PARKING_RECORDS_PATH),
            "proposed_resolution_records": rel(PROPOSED_RESOLUTION_RECORDS_PATH),
            "proposal_emission_route_map": rel(EMISSION_ROUTE_MAP_PATH),
        },
    }

    unresolved_continuation = {
        "schema_version": "o2_proposal_emission_post_closure_unresolved_continuation_v0",
        "unresolved_status_continues": True,
        "record_review_executed_in_decision": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
    }

    c5_continuation = {
        "schema_version": "o2_proposal_emission_post_closure_c5_block_continuation_v0",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "block_continues": True,
        "block_reason": "Decision selected proposed-record review next but did not emit reviewed resolution records.",
    }

    deferred_branches = {
        "schema_version": "o2_proposal_emission_post_closure_deferred_branches_v0",
        "deferred": [
            "MARK_WEAK_FEEDBACK_RESOLVED",
            "OPEN_C5",
            "LIVE_FEEDBACK_AUDIT",
            "REPAIR",
            "RETRY",
            "RUNTIME_PATCH",
            "SOURCE_MUTATION",
        ],
        "why": "This unit only selects the proposed-record review branch.",
    }

    authority_boundary = {
        "schema_version": "o2_proposal_emission_post_closure_decision_authority_boundary_v0",
        "status": status,
        "may_execute_proposed_record_review_next": decision_pass,
        "may_emit_reviewed_resolution_records_now_in_decision_unit": False,
        "may_resolve_weak_feedback_now": False,
        "may_answer_question_packets_as_reviewed_now": False,
        "may_satisfy_source_ref_requests_as_reviewed_now": False,
        "may_approve_under_typed_acceptance_as_reviewed_now": False,
        "may_count_parking_as_resolution": False,
        "may_set_c5_reconsideration_ready": False,
        "may_open_c5": False,
        "may_run_live_feedback_audit_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
    }

    classification = {
        "schema_version": "o2_proposal_emission_post_closure_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_closure_decision_complete": decision_pass,
        "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": recommended_next,
        "proposed_record_review_authorized_next": decision_pass,
        "record_review_executed_in_decision": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
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
        "schema_version": "o2_proposal_emission_post_closure_decision_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "decision_count": 1 if decision_pass else 0,
        "selected_proposed_record_review_count": 1 if decision_pass else 0,
        "proposed_record_review_authorized_next_count": 1 if decision_pass else 0,
        "proposed_question_answer_records_available_count": len(qa_records),
        "proposed_source_ref_satisfaction_records_available_count": len(source_records),
        "proposed_under_typed_acceptance_review_records_available_count": len(undertyped_records),
        "parking_execution_continuation_records_available_count": len(parking_records),
        "proposed_resolution_records_available_count": len(proposed_resolution_records),
        "proposal_emission_route_records_available_count": len(route_records),
        "weak_feedback_resolved_count": 0,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "record_review_executed_in_decision_count": 0,
        "question_packets_answered_count": 0,
        "source_ref_requests_satisfied_count": 0,
        "under_typed_acceptance_approved_count": 0,
        "parked_records_counted_as_resolved_count": 0,
        "live_feedback_audit_executed_count": 0,
        "repair_applied_count": 0,
        "retry_executed_count": 0,
        "target_selected_for_build_count": 0,
        "runtime_patch_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "architecture_change_count": 0,
        "c5_opened_count": 0,
        "c5_reconsideration_ready_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "weak_feedback_resolved_count",
        "resolution_records_emitted_count",
        "reviewed_resolution_records_emitted_count",
        "record_review_executed_in_decision_count",
        "question_packets_answered_count",
        "source_ref_requests_satisfied_count",
        "under_typed_acceptance_approved_count",
        "parked_records_counted_as_resolved_count",
        "live_feedback_audit_executed_count",
        "repair_applied_count",
        "retry_executed_count",
        "target_selected_for_build_count",
        "runtime_patch_count",
        "source_mutated_count",
        "prior_receipt_mutated_count",
        "architecture_change_count",
        "c5_opened_count",
        "c5_reconsideration_ready_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "o2_proposal_emission_post_closure_decision_profile_v0",
        "profile_id": "o2_proposal_emission_post_closure_decision_profile_" + sha8(rollup),
        "status": status,
        "selected_next_unit": recommended_next,
        "decision": "execute proposed-record review next",
        "record_review_executed_in_decision": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Execute proposed-record review next. Do not count the decision itself as review, resolution, or C5 readiness.",
        "must_not_infer": [
            "reviewed resolution records emitted by decision",
            "weak feedback resolved",
            "question packet answered as reviewed",
            "source-ref request satisfied as reviewed",
            "under-typed acceptance approved as reviewed",
            "parking resolved weak feedback",
            "C5 reconsideration ready",
            "C5 opened",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_proposal_emission_post_closure_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The post-closure decision selected proposed-record review as the next branch from the frozen proposal-emission reference. This decision emits no reviewed records, marks no weak feedback resolved, and does not open C5.",
        "selected_next_unit": recommended_next,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_proposal_emission_post_closure_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_proposal_emission_closure",
                "question": "is proposal-emission reference closed",
                "answer": "yes" if decision_pass else "no",
                "taken": "evaluate next branch table",
            },
            {
                "step": "inspect_frozen_proposed_records",
                "question": "what is available after closure",
                "answer": "frozen unreviewed proposed records; zero reviewed resolution records",
                "taken": "preserve unresolved and C5-block state",
            },
            {
                "step": "select_next_branch",
                "question": "what next branch is lawful",
                "answer": SELECTED_NEXT_UNIT if decision_pass else recommended_next,
                "taken": "authorize proposed-record review next",
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
        (PROPOSED_RECORD_REVIEW_AUTH_PATH, review_authorization),
        (PROPOSED_RECORD_INPUT_SCOPE_PATH, input_scope),
        (UNRESOLVED_CONTINUATION_PATH, unresolved_continuation),
        (C5_BLOCK_CONTINUATION_PATH, c5_continuation),
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
        "PROPOSAL_EMISSION_DECIDE_0_CLOSURE_RECEIPT_CONSUMED": CLOSURE_RECEIPT_PATH.exists(),
        "PROPOSAL_EMISSION_DECIDE_1_DECISION_BASIS_EMITTED": DECISION_BASIS_PATH.exists(),
        "PROPOSAL_EMISSION_DECIDE_2_DECISION_TABLE_EMITTED": DECISION_TABLE_PATH.exists(),
        "PROPOSAL_EMISSION_DECIDE_3_PROPOSED_RECORD_REFERENCE_CONFIRMED": decision_basis["proposal_emission_closed_as_reviewed_reference"] is True,
        "PROPOSAL_EMISSION_DECIDE_4_PROPOSED_RECORDS_FROZEN_UNREVIEWED_CONFIRMED": decision_basis["proposed_records_frozen_as_unreviewed"] is True,
        "PROPOSAL_EMISSION_DECIDE_5_ZERO_REVIEWED_RESOLUTION_CONFIRMED": decision_basis["resolution_records_emitted_count"] == 0 and decision_basis["reviewed_resolution_records_emitted_count"] == 0,
        "PROPOSAL_EMISSION_DECIDE_6_INPUT_SCOPE_CONFIRMED": len(proposed_resolution_records) == 3 and len(route_records) == 3,
        "PROPOSAL_EMISSION_DECIDE_7_C5_BLOCK_CONFIRMED": decision_basis["c5_feedback_readiness"] == "BLOCKED_BY_WEAK_FEEDBACK" and decision_basis["c5_reconsideration_ready"] is False,
        "PROPOSAL_EMISSION_DECIDE_8_PROPOSED_RECORD_REVIEW_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "PROPOSAL_EMISSION_DECIDE_9_PROPOSED_RECORD_REVIEW_AUTHORIZATION_EMITTED": review_authorization["authorized_next_unit"] == SELECTED_NEXT_UNIT,
        "PROPOSAL_EMISSION_DECIDE_10_NO_REVIEW_EXECUTED_IN_DECISION": rollup["record_review_executed_in_decision_count"] == 0,
        "PROPOSAL_EMISSION_DECIDE_11_NO_REVIEWED_RESOLUTION_RECORDS_EMITTED": rollup["reviewed_resolution_records_emitted_count"] == 0 and rollup["resolution_records_emitted_count"] == 0,
        "PROPOSAL_EMISSION_DECIDE_12_WEAK_FEEDBACK_NOT_RESOLVED": rollup["weak_feedback_resolved_count"] == 0,
        "PROPOSAL_EMISSION_DECIDE_13_NO_ANSWER_SATISFY_APPROVE": rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "PROPOSAL_EMISSION_DECIDE_14_NO_PARKING_AS_RESOLUTION": rollup["parked_records_counted_as_resolved_count"] == 0,
        "PROPOSAL_EMISSION_DECIDE_15_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "PROPOSAL_EMISSION_DECIDE_16_NO_C5_RECONSIDERATION_READY": rollup["c5_reconsideration_ready_count"] == 0,
        "PROPOSAL_EMISSION_DECIDE_17_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "PROPOSAL_EMISSION_DECIDE_18_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "PROPOSAL_EMISSION_DECIDE_19_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_PROPOSAL_EMISSION_POST_CLOSURE_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "selected": recommended_next,
        "reviewed_resolution_records": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_proposal_emission_post_closure_decision_receipt_v0",
        "receipt_type": "TYPED_O2_PROPOSAL_EMISSION_POST_CLOSURE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_proposal_emission_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "machine_readable_o2_proposal_emission_post_closure_decision_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_closure_decision_complete": decision_pass,
            "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
            "selected_next_unit": recommended_next,
            "proposed_record_review_authorized_next": decision_pass,
            "proposal_emission_closed_as_reviewed_reference": decision_basis["proposal_emission_closed_as_reviewed_reference"],
            "proposed_records_frozen_as_unreviewed": decision_basis["proposed_records_frozen_as_unreviewed"],
            "proposed_question_answer_records_available_count": len(qa_records),
            "proposed_source_ref_satisfaction_records_available_count": len(source_records),
            "proposed_under_typed_acceptance_review_records_available_count": len(undertyped_records),
            "parking_execution_continuation_records_available_count": len(parking_records),
            "proposed_resolution_records_available_count": len(proposed_resolution_records),
            "proposal_emission_route_records_available_count": len(route_records),
            "record_review_executed_in_decision": False,
            "weak_feedback_resolved": False,
            "resolution_records_emitted_count": 0,
            "reviewed_resolution_records_emitted_count": 0,
            "question_packets_answered": False,
            "source_ref_requests_satisfied": False,
            "under_typed_acceptance_approved": False,
            "parking_counted_as_resolution": False,
            "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
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
            "proposed_record_review_authorization": rel(PROPOSED_RECORD_REVIEW_AUTH_PATH),
            "proposed_record_review_input_scope": rel(PROPOSED_RECORD_INPUT_SCOPE_PATH),
            "unresolved_continuation": rel(UNRESOLVED_CONTINUATION_PATH),
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
    print(f"proposal_emission_post_closure_decision_receipt_id={receipt_id}")
    print(f"proposal_emission_post_closure_decision_receipt_path={rel(receipt_path)}")
    print(f"proposal_emission_post_closure_decision_basis_path={rel(DECISION_BASIS_PATH)}")
    print(f"proposal_emission_post_closure_decision_table_path={rel(DECISION_TABLE_PATH)}")
    print(f"proposal_emission_selected_next_branch_path={rel(SELECTED_BRANCH_PATH)}")
    print(f"proposed_record_review_authorization_path={rel(PROPOSED_RECORD_REVIEW_AUTH_PATH)}")
    print(f"proposed_record_review_input_scope_path={rel(PROPOSED_RECORD_INPUT_SCOPE_PATH)}")
    print(f"proposal_emission_post_closure_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"proposal_emission_post_closure_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
