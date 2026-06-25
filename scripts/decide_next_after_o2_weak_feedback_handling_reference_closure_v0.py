#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_HANDLING_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_handling_post_closure_decision.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_HANDLING_POST_CLOSURE_DECISION"
MODE = "DECIDE_ONLY / SELECT_NEXT_BRANCH / NO_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_HANDLING_POST_CLOSURE_DECISION_ONLY"

WFH_CLOSURE_RECEIPT_ID = "07cfbdec"
WFH_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0_receipts/07cfbdec.json"
WFH_CLOSURE_RECORD_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_handling_closure_record_v0.json"
WFH_REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_handling_reviewed_reference_v0.json"
WFH_UNRESOLVED_FREEZE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_unresolved_status_freeze_v0.json"
WFH_QUESTION_FREEZE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_question_packet_candidate_freeze_v0.json"
WFH_SOURCE_REF_FREEZE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_source_ref_request_candidate_freeze_v0.json"
WFH_UNDERTYPED_FREEZE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_under_typed_acceptance_candidate_freeze_v0.json"
WFH_PARKING_FREEZE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_parking_not_resolution_freeze_v0.json"
WFH_C5_BLOCK_FREEZE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_c5_block_freeze_v0.json"
WFH_RECEIPT_CHAIN_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_handling_receipt_chain_v0.json"
WFH_BOUNDARY_LOCK_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_handling_closure_boundary_lock_v0.json"
WFH_CLOSURE_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_handling_closure_classification_v0.json"
WFH_CLOSURE_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_handling_closure_authority_boundary_v0.json"
WFH_CLOSURE_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_handling_closure_rollup_v0.json"
WFH_CLOSURE_PROFILE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_handling_closure_profile_v0.json"
WFH_CLOSURE_REPORT_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_handling_closure_report.json"

WFH_HANDLING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_records_v0.jsonl"
WFH_QUESTION_PACKETS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_question_packets_v0.jsonl"
WFH_SOURCE_REF_REQUESTS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_source_ref_requests_v0.jsonl"
WFH_UNDERTYPED_CANDIDATES_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_under_typed_acceptance_candidates_v0.jsonl"
WFH_PARKING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_parking_records_v0.jsonl"
WFH_C5_BLOCK_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_c5_block_records_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    WFH_CLOSURE_RECEIPT_PATH,
    WFH_CLOSURE_RECORD_PATH,
    WFH_REVIEWED_REFERENCE_PATH,
    WFH_UNRESOLVED_FREEZE_PATH,
    WFH_QUESTION_FREEZE_PATH,
    WFH_SOURCE_REF_FREEZE_PATH,
    WFH_UNDERTYPED_FREEZE_PATH,
    WFH_PARKING_FREEZE_PATH,
    WFH_C5_BLOCK_FREEZE_PATH,
    WFH_RECEIPT_CHAIN_PATH,
    WFH_BOUNDARY_LOCK_PATH,
    WFH_CLOSURE_CLASSIFICATION_PATH,
    WFH_CLOSURE_AUTHORITY_PATH,
    WFH_CLOSURE_ROLLUP_PATH,
    WFH_CLOSURE_PROFILE_PATH,
    WFH_CLOSURE_REPORT_PATH,
    WFH_HANDLING_RECORDS_PATH,
    WFH_QUESTION_PACKETS_PATH,
    WFH_SOURCE_REF_REQUESTS_PATH,
    WFH_UNDERTYPED_CANDIDATES_PATH,
    WFH_PARKING_RECORDS_PATH,
    WFH_C5_BLOCK_RECORDS_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "o2_wfh_post_closure_decision_basis_v0.json"
DECISION_TABLE_PATH = OUT_DIR / "o2_wfh_post_closure_decision_table_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "o2_wfh_selected_next_branch_v0.json"
RESOLUTION_TARGET_AUTH_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_authorization_v0.json"
UNRESOLVED_BLOCK_CONTINUATION_PATH = OUT_DIR / "o2_weak_feedback_unresolved_block_continuation_v0.json"
C5_BLOCK_CONTINUATION_PATH = OUT_DIR / "o2_wfh_c5_block_continuation_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "o2_wfh_deferred_branches_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_wfh_post_closure_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_wfh_post_closure_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_wfh_post_closure_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_wfh_post_closure_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_wfh_post_closure_decision_report.json"
TRACE_PATH = OUT_DIR / "o2_wfh_post_closure_decision_transition_trace.json"

EXPECTED_CLOSURE_STATUS = "TYPED_O2_WEAK_FEEDBACK_HANDLING_CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED_DECISION_READY"
EXPECTED_CLOSURE_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_HANDLING_CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED_DECISION_READY"
EXPECTED_CLOSURE_NEXT = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_HANDLING_REFERENCE_CLOSURE_V0"

SELECTED_NEXT_UNIT = "DESIGN_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_V0"

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

    closure_receipt = read_json(WFH_CLOSURE_RECEIPT_PATH)
    summary = closure_receipt.get("machine_readable_o2_weak_feedback_handling_closure_summary", {})
    reviewed_reference = read_json(WFH_REVIEWED_REFERENCE_PATH)
    unresolved_freeze = read_json(WFH_UNRESOLVED_FREEZE_PATH)
    question_freeze = read_json(WFH_QUESTION_FREEZE_PATH)
    source_ref_freeze = read_json(WFH_SOURCE_REF_FREEZE_PATH)
    undertyped_freeze = read_json(WFH_UNDERTYPED_FREEZE_PATH)
    parking_freeze = read_json(WFH_PARKING_FREEZE_PATH)
    c5_freeze = read_json(WFH_C5_BLOCK_FREEZE_PATH)
    boundary_lock = read_json(WFH_BOUNDARY_LOCK_PATH)
    closure_authority = read_json(WFH_CLOSURE_AUTHORITY_PATH)
    closure_rollup = read_json(WFH_CLOSURE_ROLLUP_PATH)
    closure_profile = read_json(WFH_CLOSURE_PROFILE_PATH)
    closure_report = read_json(WFH_CLOSURE_REPORT_PATH)

    handling = read_jsonl(WFH_HANDLING_RECORDS_PATH)
    questions = read_jsonl(WFH_QUESTION_PACKETS_PATH)
    source_refs = read_jsonl(WFH_SOURCE_REF_REQUESTS_PATH)
    acceptances = read_jsonl(WFH_UNDERTYPED_CANDIDATES_PATH)
    parking = read_jsonl(WFH_PARKING_RECORDS_PATH)
    c5_blocks = read_jsonl(WFH_C5_BLOCK_RECORDS_PATH)

    if closure_receipt.get("receipt_id") != WFH_CLOSURE_RECEIPT_ID or closure_receipt.get("gate") != "PASS":
        failures.append("wfh_closure_receipt_not_pass")
    if closure_receipt.get("terminal", {}).get("stop_code") != EXPECTED_CLOSURE_STOP:
        failures.append("wfh_closure_terminal_not_expected")
    if closure_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("wfh_closure_hidden_next_command")
    if summary.get("status") != EXPECTED_CLOSURE_STATUS:
        failures.append(f"wfh_closure_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_CLOSURE_NEXT:
        failures.append(f"wfh_closure_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "weak_feedback_handling_closed_as_reviewed_reference",
        "reviewed_reference_emitted",
        "post_closure_decision_ready",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"closure_required_true_missing:{key}")

    for key in [
        "weak_feedback_resolved",
        "question_packets_answered",
        "source_ref_requests_satisfied",
        "under_typed_acceptance_approved",
        "parking_counted_as_resolution",
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
            failures.append(f"closure_forbidden_true:{key}")

    expected_counts = {
        "handling_records_frozen_count": 3,
        "question_packet_candidates_frozen_count": 3,
        "source_ref_request_candidates_frozen_count": 2,
        "under_typed_acceptance_candidates_frozen_count": 2,
        "parking_records_frozen_count": 3,
        "c5_block_records_frozen_count": 3,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"closure_count_wrong:{key}:{summary.get(key)}")

    if summary.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("closure_c5_readiness_not_blocked")
    if reviewed_reference.get("weak_feedback_resolved") is not False:
        failures.append("reviewed_reference_resolved")
    if unresolved_freeze.get("weak_feedback_resolved") is not False:
        failures.append("unresolved_freeze_resolved")
    if question_freeze.get("answered_count") != 0:
        failures.append("question_freeze_answered")
    if source_ref_freeze.get("satisfied_count") != 0:
        failures.append("source_ref_freeze_satisfied")
    if undertyped_freeze.get("approved_count") != 0 or undertyped_freeze.get("c5_unblock_allowed_count") != 0:
        failures.append("undertyped_freeze_approved_or_unblocked")
    if parking_freeze.get("parking_counted_as_resolution") is not False:
        failures.append("parking_freeze_counted_as_resolution")
    if c5_freeze.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_freeze.get("c5_opened") is not False:
        failures.append("c5_freeze_not_blocked")
    if boundary_lock.get("weak_feedback_resolved") is not False or boundary_lock.get("c5_opened") is not False:
        failures.append("boundary_lock_wrong")
    if closure_authority.get("may_decide_next_after_weak_feedback_handling_reference_closure") is not True:
        failures.append("closure_authority_no_post_decision")
    if closure_authority.get("may_open_c5") is not False:
        failures.append("closure_authority_allows_c5")
    if closure_rollup.get("post_closure_decision_ready_count") != 1:
        failures.append("closure_rollup_decision_ready_wrong")
    if closure_profile.get("post_closure_decision_ready") is not True:
        failures.append("closure_profile_decision_ready_wrong")
    if closure_report.get("recommended_next_handling") != EXPECTED_CLOSURE_NEXT:
        failures.append("closure_report_next_wrong")

    if len(handling) != 3 or len(questions) != 3 or len(source_refs) != 2 or len(acceptances) != 2 or len(parking) != 3 or len(c5_blocks) != 3:
        failures.append("source_artifact_counts_wrong")

    return failures, {
        "summary": summary,
        "handling": handling,
        "questions": questions,
        "source_refs": source_refs,
        "acceptances": acceptances,
        "parking": parking,
        "c5_blocks": c5_blocks,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    summary = src.get("summary", {})
    handling = src.get("handling", [])
    questions = src.get("questions", [])
    source_refs = src.get("source_refs", [])
    acceptances = src.get("acceptances", [])
    parking = src.get("parking", [])
    c5_blocks = src.get("c5_blocks", [])

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    decision_pass = not failures
    status = "TYPED_O2_WFH_POST_CLOSURE_DECISION_SELECTED_WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGN_READY" if decision_pass else "TYPED_O2_WFH_POST_CLOSURE_DECISION_BASIS_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_O2_WFH_POST_CLOSURE_DECISION_BASIS_V0"

    reason_codes = [
        "WFH_POST_CLOSURE_DECISION_EMITTED",
        "WFH_CLOSURE_RECEIPT_CONSUMED",
        "REVIEWED_STATIC_HANDLING_REFERENCE_CONFIRMED",
        "UNRESOLVED_WEAK_FEEDBACK_CONFIRMED",
        "QUESTION_PACKETS_UNANSWERED_CONFIRMED",
        "SOURCE_REF_REQUESTS_UNSATISFIED_CONFIRMED",
        "UNDER_TYPED_ACCEPTANCE_UNAPPROVED_CONFIRMED",
        "PARKING_NOT_RESOLUTION_CONFIRMED",
        "C5_BLOCKED_BY_WEAK_FEEDBACK_CONFIRMED",
        "WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGN_SELECTED_NEXT",
        "NO_WEAK_FEEDBACK_RESOLUTION_ATTEMPTED",
        "NO_QUESTION_PACKET_ANSWERED",
        "NO_SOURCE_REF_REQUEST_SATISFIED",
        "NO_UNDER_TYPED_ACCEPTANCE_APPROVED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_TARGET_SELECTED_FOR_BUILD",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
        "NO_C5_OPENED",
    ] if decision_pass else failures

    decision_basis = {
        "schema_version": "o2_wfh_post_closure_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_wfh_closure_receipt_id": WFH_CLOSURE_RECEIPT_ID,
        "weak_feedback_handling_closed_as_reviewed_reference": summary.get("weak_feedback_handling_closed_as_reviewed_reference"),
        "reviewed_reference_emitted": summary.get("reviewed_reference_emitted"),
        "handling_records_frozen_count": len(handling),
        "question_packet_candidates_frozen_count": len(questions),
        "source_ref_request_candidates_frozen_count": len(source_refs),
        "under_typed_acceptance_candidates_frozen_count": len(acceptances),
        "parking_records_frozen_count": len(parking),
        "c5_block_records_frozen_count": len(c5_blocks),
        "weak_feedback_resolved": False,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_opened": False,
    }

    decision_table = {
        "schema_version": "o2_wfh_post_closure_decision_table_v0",
        "decision_status": "NEXT_BRANCH_SELECTED" if decision_pass else "NO_BRANCH_SELECTED",
        "records": [
            {
                "branch": "DESIGN_O2_WEAK_FEEDBACK_RESOLUTION_TARGET",
                "selected": decision_pass,
                "next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
                "why": "The handling reference is closed, but weak feedback remains unresolved and now has reviewed candidate structures requiring explicit target design before any answer/satisfaction/approval can occur.",
            },
            {
                "branch": "ANSWER_OR_RESOLVE_NOW",
                "selected": False,
                "next_unit": None,
                "why": "This unit decides the next branch only. It may not answer question packets, satisfy source-ref requests, approve under-typed acceptance, or resolve weak feedback.",
            },
            {
                "branch": "RUN_LIVE_FEEDBACK_AUDIT_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Live audit remains a later possible target if the resolution design determines explicit source traces are required.",
            },
            {
                "branch": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 remains blocked by weak feedback.",
            },
            {
                "branch": "PARK_AND_MOVE_TO_OTHER_PRE_C5_HARDENING",
                "selected": False,
                "next_unit": None,
                "why": "Parking is available but not selected because the current closed reference exposes an explicit resolution-target design edge.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "o2_wfh_selected_next_branch_v0",
        "selected_branch": "DESIGN_O2_WEAK_FEEDBACK_RESOLUTION_TARGET" if decision_pass else None,
        "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "selection_scope": "target design only",
        "selection_reason": "Reviewed handling reference exists; unresolved candidate/question/source-ref/acceptance structures need an explicit design target before any resolution step.",
        "selected_branch_does_not": [
            "answer question packets now",
            "satisfy source-ref requests now",
            "approve under-typed acceptance now",
            "count parking as resolution",
            "run live audit now",
            "repair",
            "retry",
            "select build target",
            "patch runtime",
            "open C5",
        ],
    }

    resolution_target_auth = {
        "schema_version": "o2_weak_feedback_resolution_target_authorization_v0",
        "authorization_status": "TARGET_DESIGN_AUTHORIZED" if decision_pass else "NOT_AUTHORIZED",
        "authorized_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "authorized_design_mode": "DESIGN_ONLY / WEAK_FEEDBACK_RESOLUTION_TARGET / NO_RESOLUTION_NO_C5" if decision_pass else None,
        "target_goal": "Design a bounded resolution target for the reviewed weak-feedback handling reference.",
        "target_should_define": [
            "how question packets may be answered or remain blocked",
            "how source-ref requests may be satisfied or escalated",
            "how under-typed acceptance candidates may be approved, rejected, or kept candidate-only",
            "how parking may remain explicit without counting as resolution",
            "what exact reviewed state would count as weak-feedback resolved",
            "what exact reviewed state, if any, could unblock C5",
        ],
        "target_may_not": [
            "resolve weak feedback during design",
            "answer question packets during design",
            "satisfy source-ref requests during design",
            "approve under-typed acceptance during design",
            "run live audit",
            "repair",
            "retry",
            "select target for build",
            "patch runtime",
            "mutate sources",
            "open C5",
        ],
    }

    unresolved_block_continuation = {
        "schema_version": "o2_weak_feedback_unresolved_block_continuation_v0",
        "unresolved_status_continues": True,
        "weak_feedback_resolved": False,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "why": "Decision selected a target design branch only; it did not execute any resolution action.",
    }

    c5_block_continuation = {
        "schema_version": "o2_wfh_c5_block_continuation_v0",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_opened": False,
        "block_continues": True,
        "block_reason": "Weak feedback remains unresolved after reviewed handling reference closure.",
        "c5_may_be_reconsidered_only_after": [
            "resolution target is designed, built, reviewed, and closed",
            "or a later human-governed bounded decision explicitly accepts unresolved weak feedback as a C5 preflight state",
        ],
    }

    deferred_branches = {
        "schema_version": "o2_wfh_deferred_branches_v0",
        "deferred": [
            "ANSWER_QUESTION_PACKETS",
            "SATISFY_SOURCE_REF_REQUESTS",
            "APPROVE_UNDER_TYPED_ACCEPTANCE",
            "COUNT_PARKING_AS_RESOLUTION",
            "LIVE_FEEDBACK_AUDIT",
            "REPAIR",
            "RETRY",
            "TARGET_SELECTION",
            "RUNTIME_PATCH",
            "C5",
        ],
        "why": "This unit only selects the next design target.",
    }

    authority_boundary = {
        "schema_version": "o2_wfh_post_closure_decision_authority_boundary_v0",
        "status": status,
        "may_design_o2_weak_feedback_resolution_target_next": decision_pass,
        "may_resolve_weak_feedback_now": False,
        "may_answer_question_packets_now": False,
        "may_satisfy_source_ref_requests_now": False,
        "may_approve_under_typed_acceptance_now": False,
        "may_count_parking_as_resolution": False,
        "may_run_live_feedback_audit_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_select_target_for_build": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_open_c5": False,
    }

    classification = {
        "schema_version": "o2_wfh_post_closure_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_closure_decision_complete": decision_pass,
        "selected_next_branch": "DESIGN_O2_WEAK_FEEDBACK_RESOLUTION_TARGET" if decision_pass else None,
        "selected_next_unit": recommended_next,
        "weak_feedback_resolved": False,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
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
        "schema_version": "o2_wfh_post_closure_decision_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "decision_count": 1 if decision_pass else 0,
        "selected_resolution_target_design_count": 1 if decision_pass else 0,
        "handling_records_available_count": len(handling),
        "question_packet_candidates_available_count": len(questions),
        "source_ref_request_candidates_available_count": len(source_refs),
        "under_typed_acceptance_candidates_available_count": len(acceptances),
        "parking_records_available_count": len(parking),
        "c5_block_records_available_count": len(c5_blocks),
        "c5_block_continuation_count": 1 if decision_pass else 0,
        "weak_feedback_resolved_count": 0,
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
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "weak_feedback_resolved_count",
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
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "o2_wfh_post_closure_decision_profile_v0",
        "profile_id": "o2_wfh_post_closure_decision_profile_" + sha8(rollup),
        "status": status,
        "selected_next_unit": recommended_next,
        "decision": "design weak-feedback resolution target next",
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Design the weak-feedback resolution target next. Continue to preserve C5 block until reviewed resolution or explicit governed acceptance occurs.",
        "must_not_infer": [
            "weak feedback resolved",
            "question packet answered",
            "source-ref request satisfied",
            "under-typed acceptance approved",
            "parking resolved weak feedback",
            "live audit complete",
            "C5 opened",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_wfh_post_closure_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The post-closure decision selected weak-feedback resolution target design as the next branch. This is a design authorization only. It does not answer question packets, satisfy source-ref requests, approve under-typed acceptance, count parking as resolution, run live audit, repair, retry, select target, patch runtime, mutate sources, or open C5.",
        "selected_next_unit": recommended_next,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_wfh_post_closure_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_wfh_closure",
                "question": "is weak-feedback handling closed as reviewed reference",
                "answer": "yes" if decision_pass else "no",
                "taken": "evaluate next branch table",
            },
            {
                "step": "inspect_unresolved_surface",
                "question": "what remains after closure",
                "answer": "unanswered questions, unsatisfied source-ref requests, unapproved under-typed acceptance candidates, parking-not-resolution, and C5 block",
                "taken": "preserve unresolved status",
            },
            {
                "step": "select_next_branch",
                "question": "what next branch is lawful",
                "answer": SELECTED_NEXT_UNIT if decision_pass else recommended_next,
                "taken": "authorize weak-feedback resolution target design next",
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
        (RESOLUTION_TARGET_AUTH_PATH, resolution_target_auth),
        (UNRESOLVED_BLOCK_CONTINUATION_PATH, unresolved_block_continuation),
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
        "WFH_DECIDE_0_CLOSURE_RECEIPT_CONSUMED": WFH_CLOSURE_RECEIPT_PATH.exists(),
        "WFH_DECIDE_1_DECISION_BASIS_EMITTED": DECISION_BASIS_PATH.exists(),
        "WFH_DECIDE_2_DECISION_TABLE_EMITTED": DECISION_TABLE_PATH.exists(),
        "WFH_DECIDE_3_REVIEWED_REFERENCE_CONFIRMED": summary.get("weak_feedback_handling_closed_as_reviewed_reference") is True,
        "WFH_DECIDE_4_UNRESOLVED_STATUS_CONFIRMED": summary.get("weak_feedback_resolved") is False,
        "WFH_DECIDE_5_QUESTION_UNANSWERED_CONFIRMED": summary.get("question_packets_answered") is False,
        "WFH_DECIDE_6_SOURCE_REF_UNSATISFIED_CONFIRMED": summary.get("source_ref_requests_satisfied") is False,
        "WFH_DECIDE_7_ACCEPTANCE_UNAPPROVED_CONFIRMED": summary.get("under_typed_acceptance_approved") is False,
        "WFH_DECIDE_8_C5_BLOCK_CONFIRMED": summary.get("c5_feedback_readiness") == "BLOCKED_BY_WEAK_FEEDBACK",
        "WFH_DECIDE_9_RESOLUTION_TARGET_DESIGN_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "WFH_DECIDE_10_RESOLUTION_TARGET_AUTHORIZATION_EMITTED": resolution_target_auth["authorized_next_unit"] == SELECTED_NEXT_UNIT,
        "WFH_DECIDE_11_NO_RESOLUTION_OR_ANSWER_OR_SATISFY_OR_APPROVE": rollup["weak_feedback_resolved_count"] == 0 and rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "WFH_DECIDE_12_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "WFH_DECIDE_13_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "WFH_DECIDE_14_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "WFH_DECIDE_15_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "WFH_DECIDE_16_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "WFH_DECIDE_17_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WFH_POST_CLOSURE_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "selected": recommended_next,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_wfh_post_closure_decision_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_HANDLING_POST_CLOSURE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_wfh_closure_receipt_id": WFH_CLOSURE_RECEIPT_ID,
        "machine_readable_o2_wfh_post_closure_decision_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_closure_decision_complete": decision_pass,
            "selected_next_branch": "DESIGN_O2_WEAK_FEEDBACK_RESOLUTION_TARGET" if decision_pass else None,
            "selected_next_unit": recommended_next,
            "weak_feedback_handling_reference_closed": summary.get("weak_feedback_handling_closed_as_reviewed_reference"),
            "handling_records_available_count": len(handling),
            "question_packet_candidates_available_count": len(questions),
            "source_ref_request_candidates_available_count": len(source_refs),
            "under_typed_acceptance_candidates_available_count": len(acceptances),
            "parking_records_available_count": len(parking),
            "c5_block_records_available_count": len(c5_blocks),
            "weak_feedback_resolved": False,
            "question_packets_answered": False,
            "source_ref_requests_satisfied": False,
            "under_typed_acceptance_approved": False,
            "parking_counted_as_resolution": False,
            "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
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
            "resolution_target_authorization": rel(RESOLUTION_TARGET_AUTH_PATH),
            "unresolved_block_continuation": rel(UNRESOLVED_BLOCK_CONTINUATION_PATH),
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
    print(f"wfh_post_closure_decision_receipt_id={receipt_id}")
    print(f"wfh_post_closure_decision_receipt_path={rel(receipt_path)}")
    print(f"wfh_post_closure_decision_basis_path={rel(DECISION_BASIS_PATH)}")
    print(f"wfh_post_closure_decision_table_path={rel(DECISION_TABLE_PATH)}")
    print(f"wfh_selected_next_branch_path={rel(SELECTED_BRANCH_PATH)}")
    print(f"weak_feedback_resolution_target_authorization_path={rel(RESOLUTION_TARGET_AUTH_PATH)}")
    print(f"wfh_unresolved_block_continuation_path={rel(UNRESOLVED_BLOCK_CONTINUATION_PATH)}")
    print(f"wfh_c5_block_continuation_path={rel(C5_BLOCK_CONTINUATION_PATH)}")
    print(f"wfh_post_closure_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"wfh_post_closure_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
