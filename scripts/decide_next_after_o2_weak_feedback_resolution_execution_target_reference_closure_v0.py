#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_execution_target_post_closure_decision.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_POST_CLOSURE_DECISION"
MODE = "DECIDE_ONLY / SELECT_PROPOSAL_EMISSION_EXECUTION / NO_EMISSION_NO_REVIEW_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_POST_CLOSURE_DECISION_ONLY"

EXEC_CLOSURE_RECEIPT_ID = "ab47a30d"
EXEC_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0_receipts/ab47a30d.json"
EXEC_CLOSURE_RECORD_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_target_closure_record_v0.json"
EXEC_REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_target_reviewed_reference_v0.json"
EXEC_TEMPLATE_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_template_freeze_v0.json"
EXEC_PROPOSAL_ROUTE_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_proposal_route_freeze_v0.json"
EXEC_ZERO_RECORD_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_resolution_execution_zero_record_freeze_v0.json"
EXEC_C5_BLOCK_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_resolution_execution_c5_block_freeze_v0.json"
EXEC_RECEIPT_CHAIN_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_target_receipt_chain_v0.json"
EXEC_BOUNDARY_LOCK_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_target_closure_boundary_lock_v0.json"
EXEC_CLOSURE_DECISION_TABLE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_target_closure_downstream_decision_table_v0.json"
EXEC_CLOSURE_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_target_closure_authority_boundary_v0.json"
EXEC_CLOSURE_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_target_closure_classification_v0.json"
EXEC_CLOSURE_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_target_closure_rollup_v0.json"
EXEC_CLOSURE_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_target_closure_profile_v0.json"
EXEC_CLOSURE_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_target_closure_report.json"
EXEC_CLOSURE_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_target_closure_transition_trace.json"

EXEC_BUILD_QA_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_question_answer_record_templates_v0.jsonl"
EXEC_BUILD_SOURCE_REF_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_source_ref_satisfaction_record_templates_v0.jsonl"
EXEC_BUILD_UNDERTYPED_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_under_typed_acceptance_review_record_templates_v0.jsonl"
EXEC_BUILD_PARKING_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_parking_execution_continuation_record_templates_v0.jsonl"
EXEC_BUILD_RESOLUTION_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_weak_feedback_resolution_record_templates_v0.jsonl"
EXEC_BUILD_PROPOSAL_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_proposal_route_map_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    EXEC_CLOSURE_RECEIPT_PATH,
    EXEC_CLOSURE_RECORD_PATH,
    EXEC_REVIEWED_REFERENCE_PATH,
    EXEC_TEMPLATE_FREEZE_PATH,
    EXEC_PROPOSAL_ROUTE_FREEZE_PATH,
    EXEC_ZERO_RECORD_FREEZE_PATH,
    EXEC_C5_BLOCK_FREEZE_PATH,
    EXEC_RECEIPT_CHAIN_PATH,
    EXEC_BOUNDARY_LOCK_PATH,
    EXEC_CLOSURE_DECISION_TABLE_PATH,
    EXEC_CLOSURE_AUTHORITY_PATH,
    EXEC_CLOSURE_CLASSIFICATION_PATH,
    EXEC_CLOSURE_ROLLUP_PATH,
    EXEC_CLOSURE_PROFILE_PATH,
    EXEC_CLOSURE_REPORT_PATH,
    EXEC_CLOSURE_TRACE_PATH,
    EXEC_BUILD_QA_TEMPLATES_PATH,
    EXEC_BUILD_SOURCE_REF_TEMPLATES_PATH,
    EXEC_BUILD_UNDERTYPED_TEMPLATES_PATH,
    EXEC_BUILD_PARKING_TEMPLATES_PATH,
    EXEC_BUILD_RESOLUTION_TEMPLATES_PATH,
    EXEC_BUILD_PROPOSAL_ROUTE_MAP_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "o2_exec_target_post_closure_decision_basis_v0.json"
DECISION_TABLE_PATH = OUT_DIR / "o2_exec_target_post_closure_decision_table_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "o2_exec_target_selected_next_branch_v0.json"
PROPOSAL_EMISSION_AUTH_PATH = OUT_DIR / "o2_weak_feedback_resolution_proposal_emission_authorization_v0.json"
TEMPLATE_INPUT_SCOPE_PATH = OUT_DIR / "o2_proposal_emission_input_scope_v0.json"
UNRESOLVED_CONTINUATION_PATH = OUT_DIR / "o2_exec_target_post_closure_unresolved_continuation_v0.json"
C5_BLOCK_CONTINUATION_PATH = OUT_DIR / "o2_exec_target_post_closure_c5_block_continuation_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "o2_exec_target_post_closure_deferred_branches_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_exec_target_post_closure_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_exec_target_post_closure_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_exec_target_post_closure_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_exec_target_post_closure_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_exec_target_post_closure_decision_report.json"
TRACE_PATH = OUT_DIR / "o2_exec_target_post_closure_decision_transition_trace.json"

EXPECTED_CLOSURE_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED_DECISION_READY"
EXPECTED_CLOSURE_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED_DECISION_READY"
EXPECTED_CLOSURE_NEXT = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REFERENCE_CLOSURE_V0"

SELECTED_BRANCH = "EXECUTE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION"
SELECTED_NEXT_UNIT = "EXECUTE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_V0"

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

    receipt = read_json(EXEC_CLOSURE_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_resolution_execution_target_closure_summary", {})
    closure_record = read_json(EXEC_CLOSURE_RECORD_PATH)
    reviewed_reference = read_json(EXEC_REVIEWED_REFERENCE_PATH)
    template_freeze = read_json(EXEC_TEMPLATE_FREEZE_PATH)
    route_freeze = read_json(EXEC_PROPOSAL_ROUTE_FREEZE_PATH)
    zero_freeze = read_json(EXEC_ZERO_RECORD_FREEZE_PATH)
    c5_freeze = read_json(EXEC_C5_BLOCK_FREEZE_PATH)
    boundary_lock = read_json(EXEC_BOUNDARY_LOCK_PATH)
    closure_authority = read_json(EXEC_CLOSURE_AUTHORITY_PATH)
    closure_classification = read_json(EXEC_CLOSURE_CLASSIFICATION_PATH)
    closure_rollup = read_json(EXEC_CLOSURE_ROLLUP_PATH)
    closure_profile = read_json(EXEC_CLOSURE_PROFILE_PATH)
    closure_report = read_json(EXEC_CLOSURE_REPORT_PATH)
    closure_trace = read_json(EXEC_CLOSURE_TRACE_PATH)

    qa_templates = read_jsonl(EXEC_BUILD_QA_TEMPLATES_PATH)
    source_templates = read_jsonl(EXEC_BUILD_SOURCE_REF_TEMPLATES_PATH)
    undertyped_templates = read_jsonl(EXEC_BUILD_UNDERTYPED_TEMPLATES_PATH)
    parking_templates = read_jsonl(EXEC_BUILD_PARKING_TEMPLATES_PATH)
    resolution_templates = read_jsonl(EXEC_BUILD_RESOLUTION_TEMPLATES_PATH)
    proposal_routes = read_jsonl(EXEC_BUILD_PROPOSAL_ROUTE_MAP_PATH)

    if receipt.get("receipt_id") != EXEC_CLOSURE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("execution_target_closure_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_CLOSURE_STOP:
        failures.append("execution_target_closure_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("execution_target_closure_hidden_next_command")
    if summary.get("status") != EXPECTED_CLOSURE_STATUS:
        failures.append(f"execution_target_closure_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_CLOSURE_NEXT:
        failures.append(f"execution_target_closure_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "execution_target_closed_as_reviewed_reference",
        "reviewed_reference_emitted",
        "post_closure_decision_ready",
        "templates_frozen_as_templates_only",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "question_answer_templates_frozen_count": 3,
        "source_ref_satisfaction_templates_frozen_count": 2,
        "under_typed_acceptance_review_templates_frozen_count": 2,
        "parking_execution_continuation_templates_frozen_count": 3,
        "proposed_resolution_record_templates_frozen_count": 3,
        "proposal_route_map_records_frozen_count": 3,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    for key in [
        "execution_attempted",
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
    if closure_record.get("closure_status") != "CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED":
        failures.append("closure_record_wrong")
    if reviewed_reference.get("templates_are_not_proposed_records") is not True or reviewed_reference.get("proposed_records_are_not_reviewed_records") is not True:
        failures.append("reviewed_reference_boundary_wrong")
    if reviewed_reference.get("resolution_records_emitted_count") != 0 or reviewed_reference.get("proposed_resolution_records_emitted_count") != 0 or reviewed_reference.get("reviewed_resolution_records_emitted_count") != 0:
        failures.append("reviewed_reference_records_nonzero")
    if template_freeze.get("templates_are_not_proposed_records") is not True or template_freeze.get("templates_are_not_reviewed_records") is not True:
        failures.append("template_freeze_wrong")
    if route_freeze.get("all_unresolved") is not True or route_freeze.get("proposed_records_emitted_count") != 0 or route_freeze.get("reviewed_records_emitted_count") != 0:
        failures.append("route_freeze_wrong")
    if zero_freeze.get("resolution_records_emitted_count") != 0 or zero_freeze.get("proposed_resolution_records_emitted_count") != 0 or zero_freeze.get("reviewed_resolution_records_emitted_count") != 0:
        failures.append("zero_freeze_records_nonzero")
    if c5_freeze.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_freeze.get("c5_reconsideration_ready") is not False or c5_freeze.get("c5_opened") is not False:
        failures.append("c5_freeze_wrong")
    if boundary_lock.get("execution_attempted") is not False or boundary_lock.get("weak_feedback_resolved") is not False:
        failures.append("boundary_lock_wrong")
    if closure_authority.get("may_decide_next_after_execution_target_reference_closure") is not True:
        failures.append("closure_authority_no_decide")
    if closure_authority.get("may_execute_resolution_now") is not False or closure_authority.get("may_open_c5") is not False:
        failures.append("closure_authority_allows_execution_or_c5")
    if closure_classification.get("recommended_next") != EXPECTED_CLOSURE_NEXT:
        failures.append("closure_classification_next_wrong")
    if closure_rollup.get("post_closure_decision_ready_count") != 1:
        failures.append("closure_rollup_decision_ready_wrong")
    if closure_profile.get("execution_target_closed_as_reviewed_reference") is not True or closure_profile.get("next_command_goal") is not None:
        failures.append("closure_profile_wrong")
    if closure_report.get("recommended_next_handling") != EXPECTED_CLOSURE_NEXT:
        failures.append("closure_report_next_wrong")
    if closure_trace.get("terminal", {}).get("stop_code") != EXPECTED_CLOSURE_STOP:
        failures.append("closure_trace_stop_wrong")

    if len(qa_templates) != 3 or len(source_templates) != 2 or len(undertyped_templates) != 2 or len(parking_templates) != 3 or len(resolution_templates) != 3 or len(proposal_routes) != 3:
        failures.append("template_or_route_counts_wrong")
    for row in resolution_templates:
        if row.get("proposal_status") != "TEMPLATE_ONLY":
            failures.append(f"resolution_template_not_template_only:{row.get('template_id')}")
        if row.get("counts_as_reviewed_resolution") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"resolution_template_counts_or_c5:{row.get('template_id')}")
    for row in proposal_routes:
        if row.get("current_resolution_state") != "UNRESOLVED":
            failures.append(f"proposal_route_not_unresolved:{row.get('proposal_route_record_id')}")
        if row.get("proposed_record_emitted") is not False or row.get("reviewed_record_emitted") is not False:
            failures.append(f"proposal_route_emitted:{row.get('proposal_route_record_id')}")
        if row.get("c5_reconsideration_ready") is not False:
            failures.append(f"proposal_route_c5_ready:{row.get('proposal_route_record_id')}")

    return failures, {
        "summary": summary,
        "qa_templates": qa_templates,
        "source_templates": source_templates,
        "undertyped_templates": undertyped_templates,
        "parking_templates": parking_templates,
        "resolution_templates": resolution_templates,
        "proposal_routes": proposal_routes,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    qa_templates = src.get("qa_templates", [])
    source_templates = src.get("source_templates", [])
    undertyped_templates = src.get("undertyped_templates", [])
    parking_templates = src.get("parking_templates", [])
    resolution_templates = src.get("resolution_templates", [])
    proposal_routes = src.get("proposal_routes", [])

    decision_pass = not failures
    status = "TYPED_O2_EXEC_TARGET_POST_CLOSURE_DECISION_SELECTED_PROPOSAL_EMISSION_EXECUTION_READY" if decision_pass else "TYPED_O2_EXEC_TARGET_POST_CLOSURE_DECISION_BASIS_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_O2_EXEC_TARGET_POST_CLOSURE_DECISION_BASIS_V0"

    reason_codes = [
        "EXECUTION_TARGET_POST_CLOSURE_DECISION_EMITTED",
        "EXECUTION_TARGET_CLOSURE_RECEIPT_CONSUMED",
        "REVIEWED_EXECUTION_TARGET_REFERENCE_CONFIRMED",
        "TEMPLATE_ONLY_SURFACE_CONFIRMED",
        "ZERO_PROPOSED_AND_REVIEWED_RECORDS_CONFIRMED",
        "UNRESOLVED_PROPOSAL_ROUTE_MAP_CONFIRMED",
        "C5_BLOCK_CONFIRMED",
        "PROPOSAL_EMISSION_EXECUTION_SELECTED_NEXT",
        "NO_PROPOSAL_EMISSION_EXECUTED_IN_DECISION",
        "NO_RESOLUTION_EXECUTION_ATTEMPTED",
        "NO_PROPOSED_RESOLUTION_RECORDS_EMITTED",
        "NO_REVIEWED_RESOLUTION_RECORDS_EMITTED",
        "NO_QUESTION_PACKET_ANSWERED",
        "NO_SOURCE_REF_REQUEST_SATISFIED",
        "NO_UNDER_TYPED_ACCEPTANCE_APPROVED",
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
        "schema_version": "o2_exec_target_post_closure_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_execution_target_closure_receipt_id": EXEC_CLOSURE_RECEIPT_ID,
        "execution_target_closed_as_reviewed_reference": True if decision_pass else False,
        "templates_frozen_as_templates_only": True if decision_pass else False,
        "question_answer_templates_available_count": len(qa_templates),
        "source_ref_satisfaction_templates_available_count": len(source_templates),
        "under_typed_acceptance_review_templates_available_count": len(undertyped_templates),
        "parking_execution_continuation_templates_available_count": len(parking_templates),
        "proposed_resolution_record_templates_available_count": len(resolution_templates),
        "proposal_route_map_records_available_count": len(proposal_routes),
        "execution_attempted": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    decision_table = {
        "schema_version": "o2_exec_target_post_closure_decision_table_v0",
        "decision_status": "NEXT_BRANCH_SELECTED" if decision_pass else "NO_BRANCH_SELECTED",
        "records": [
            {
                "branch": SELECTED_BRANCH,
                "selected": decision_pass,
                "next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
                "why": "The reviewed execution-target reference is closed. The next lawful edge is to execute proposal emission from frozen templates into proposed records under template-only/proposal/review boundaries.",
            },
            {
                "branch": "REVIEW_PROPOSALS_NOW",
                "selected": False,
                "next_unit": None,
                "why": "No proposed records exist yet.",
            },
            {
                "branch": "MARK_WEAK_FEEDBACK_RESOLVED_NOW",
                "selected": False,
                "next_unit": None,
                "why": "No proposed or reviewed resolution records exist.",
            },
            {
                "branch": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 remains blocked until reviewed resolution exists and a later decision explicitly selects C5 reconsideration.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "o2_exec_target_selected_next_branch_v0",
        "selected_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "selection_scope": "proposal emission execution only",
        "selection_reason": "The reviewed execution-target reference has frozen templates and unresolved proposal routes. A later execution unit may emit proposed records, but this decision unit emits none.",
        "selected_branch_does_not": [
            "emit proposed records in this decision unit",
            "emit reviewed resolution records",
            "mark weak feedback resolved",
            "answer question packets as reviewed answers",
            "satisfy source-ref requests as reviewed satisfaction",
            "approve under-typed acceptance as reviewed approval",
            "count parking as resolution",
            "run live audit",
            "repair",
            "retry",
            "patch runtime",
            "mutate sources",
            "open C5",
        ],
    }

    proposal_emission_auth = {
        "schema_version": "o2_weak_feedback_resolution_proposal_emission_authorization_v0",
        "authorization_status": "PROPOSAL_EMISSION_EXECUTION_AUTHORIZED_NEXT" if decision_pass else "NOT_AUTHORIZED",
        "authorized_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "authorized_execution_mode": "PROPOSAL_EMISSION_ONLY / FROM_REVIEWED_TEMPLATES / NO_REVIEWED_RESOLUTION_NO_C5" if decision_pass else None,
        "authorized_scope": [
            "emit proposed question-answer records from reviewed templates",
            "emit proposed source-ref satisfaction records from reviewed templates",
            "emit proposed under-typed acceptance review records from reviewed templates",
            "emit parking continuation records as parked unresolved",
            "emit proposed weak-feedback resolution records from proposal route templates",
            "preserve review_status=UNREVIEWED for emitted proposed records",
            "preserve c5_reconsideration_ready=false",
        ],
        "not_authorized": [
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

    template_input_scope = {
        "schema_version": "o2_proposal_emission_input_scope_v0",
        "scope_status": "FROZEN_TEMPLATES_ELIGIBLE_FOR_LATER_PROPOSAL_EMISSION",
        "question_answer_template_count": len(qa_templates),
        "source_ref_satisfaction_template_count": len(source_templates),
        "under_typed_acceptance_review_template_count": len(undertyped_templates),
        "parking_execution_continuation_template_count": len(parking_templates),
        "proposed_resolution_record_template_count": len(resolution_templates),
        "proposal_route_map_record_count": len(proposal_routes),
        "template_sources": {
            "question_answer_templates": rel(EXEC_BUILD_QA_TEMPLATES_PATH),
            "source_ref_satisfaction_templates": rel(EXEC_BUILD_SOURCE_REF_TEMPLATES_PATH),
            "under_typed_acceptance_review_templates": rel(EXEC_BUILD_UNDERTYPED_TEMPLATES_PATH),
            "parking_execution_continuation_templates": rel(EXEC_BUILD_PARKING_TEMPLATES_PATH),
            "proposed_resolution_record_templates": rel(EXEC_BUILD_RESOLUTION_TEMPLATES_PATH),
            "proposal_route_map": rel(EXEC_BUILD_PROPOSAL_ROUTE_MAP_PATH),
        },
    }

    unresolved_continuation = {
        "schema_version": "o2_exec_target_post_closure_unresolved_continuation_v0",
        "unresolved_status_continues": True,
        "decision_unit_emitted_records": False,
        "execution_attempted": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
    }

    c5_block_continuation = {
        "schema_version": "o2_exec_target_post_closure_c5_block_continuation_v0",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "block_continues": True,
        "block_reason": "Decision selected proposal-emission execution next but did not emit or review resolution records.",
    }

    deferred_branches = {
        "schema_version": "o2_exec_target_post_closure_deferred_branches_v0",
        "deferred": [
            "REVIEW_PROPOSAL_RECORDS",
            "CLOSE_REVIEWED_RESOLUTION",
            "MARK_WEAK_FEEDBACK_RESOLVED",
            "OPEN_C5",
            "LIVE_FEEDBACK_AUDIT",
            "REPAIR",
            "RETRY",
            "RUNTIME_PATCH",
            "SOURCE_MUTATION",
        ],
        "why": "This unit only selects the next proposal-emission execution branch.",
    }

    authority_boundary = {
        "schema_version": "o2_exec_target_post_closure_decision_authority_boundary_v0",
        "status": status,
        "may_execute_proposal_emission_next": decision_pass,
        "may_emit_records_now_in_decision_unit": False,
        "may_emit_reviewed_resolution_records_now": False,
        "may_resolve_weak_feedback_now": False,
        "may_answer_question_packets_now": False,
        "may_satisfy_source_ref_requests_now": False,
        "may_approve_under_typed_acceptance_now": False,
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
        "schema_version": "o2_exec_target_post_closure_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_closure_decision_complete": decision_pass,
        "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
        "selected_next_unit": recommended_next,
        "proposal_emission_authorized_next": decision_pass,
        "decision_unit_emitted_records": False,
        "execution_attempted": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
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
        "schema_version": "o2_exec_target_post_closure_decision_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "decision_count": 1 if decision_pass else 0,
        "selected_proposal_emission_execution_count": 1 if decision_pass else 0,
        "proposal_emission_authorized_next_count": 1 if decision_pass else 0,
        "question_answer_templates_available_count": len(qa_templates),
        "source_ref_satisfaction_templates_available_count": len(source_templates),
        "under_typed_acceptance_review_templates_available_count": len(undertyped_templates),
        "parking_execution_continuation_templates_available_count": len(parking_templates),
        "proposed_resolution_record_templates_available_count": len(resolution_templates),
        "proposal_route_map_records_available_count": len(proposal_routes),
        "weak_feedback_resolved_count": 0,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "decision_unit_emitted_records_count": 0,
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
        "proposed_resolution_records_emitted_count",
        "reviewed_resolution_records_emitted_count",
        "decision_unit_emitted_records_count",
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
        "schema_version": "o2_exec_target_post_closure_decision_profile_v0",
        "profile_id": "o2_exec_target_post_closure_decision_profile_" + sha8(rollup),
        "status": status,
        "selected_next_unit": recommended_next,
        "decision": "execute weak-feedback resolution proposal emission next",
        "decision_unit_emitted_records": False,
        "execution_attempted": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Execute proposal emission next. Emitted records, if any, must remain proposed/unreviewed and must not resolve weak feedback or unblock C5.",
        "must_not_infer": [
            "proposal records emitted by decision",
            "reviewed resolution records emitted",
            "weak feedback resolved",
            "question packet answered",
            "source-ref request satisfied",
            "under-typed acceptance approved",
            "parking resolved weak feedback",
            "C5 reconsideration ready",
            "C5 opened",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_exec_target_post_closure_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The post-closure decision selected proposal-emission execution as the next branch from the reviewed execution-target reference. This decision emits no records, performs no execution, marks no weak feedback resolved, and does not open C5.",
        "selected_next_unit": recommended_next,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_exec_target_post_closure_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_execution_target_closure",
                "question": "is reviewed execution-target reference closed",
                "answer": "yes" if decision_pass else "no",
                "taken": "evaluate next branch table",
            },
            {
                "step": "inspect_template_only_surface",
                "question": "what is available after closure",
                "answer": "frozen templates and unresolved proposal routes; zero proposed/reviewed records",
                "taken": "preserve unresolved and C5-block state",
            },
            {
                "step": "select_next_branch",
                "question": "what next branch is lawful",
                "answer": SELECTED_NEXT_UNIT if decision_pass else recommended_next,
                "taken": "authorize proposal emission execution next",
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
        (PROPOSAL_EMISSION_AUTH_PATH, proposal_emission_auth),
        (TEMPLATE_INPUT_SCOPE_PATH, template_input_scope),
        (UNRESOLVED_CONTINUATION_PATH, unresolved_continuation),
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
        "EXEC_TARGET_DECIDE_0_CLOSURE_RECEIPT_CONSUMED": EXEC_CLOSURE_RECEIPT_PATH.exists(),
        "EXEC_TARGET_DECIDE_1_DECISION_BASIS_EMITTED": DECISION_BASIS_PATH.exists(),
        "EXEC_TARGET_DECIDE_2_DECISION_TABLE_EMITTED": DECISION_TABLE_PATH.exists(),
        "EXEC_TARGET_DECIDE_3_REVIEWED_REFERENCE_CONFIRMED": decision_basis["execution_target_closed_as_reviewed_reference"] is True,
        "EXEC_TARGET_DECIDE_4_TEMPLATE_ONLY_SURFACE_CONFIRMED": decision_basis["templates_frozen_as_templates_only"] is True,
        "EXEC_TARGET_DECIDE_5_ZERO_RECORDS_CONFIRMED": decision_basis["resolution_records_emitted_count"] == 0 and decision_basis["proposed_resolution_records_emitted_count"] == 0 and decision_basis["reviewed_resolution_records_emitted_count"] == 0,
        "EXEC_TARGET_DECIDE_6_INPUT_SCOPE_CONFIRMED": len(resolution_templates) == 3 and len(proposal_routes) == 3,
        "EXEC_TARGET_DECIDE_7_C5_BLOCK_CONFIRMED": decision_basis["c5_feedback_readiness"] == "BLOCKED_BY_WEAK_FEEDBACK" and decision_basis["c5_reconsideration_ready"] is False,
        "EXEC_TARGET_DECIDE_8_PROPOSAL_EMISSION_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "EXEC_TARGET_DECIDE_9_PROPOSAL_EMISSION_AUTHORIZATION_EMITTED": proposal_emission_auth["authorized_next_unit"] == SELECTED_NEXT_UNIT,
        "EXEC_TARGET_DECIDE_10_NO_RECORDS_EMITTED_IN_DECISION": rollup["decision_unit_emitted_records_count"] == 0 and rollup["proposed_resolution_records_emitted_count"] == 0 and rollup["reviewed_resolution_records_emitted_count"] == 0,
        "EXEC_TARGET_DECIDE_11_NO_RESOLUTION_ANSWER_SATISFY_APPROVE": rollup["weak_feedback_resolved_count"] == 0 and rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "EXEC_TARGET_DECIDE_12_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "EXEC_TARGET_DECIDE_13_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "EXEC_TARGET_DECIDE_14_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "EXEC_TARGET_DECIDE_15_NO_C5_RECONSIDERATION_READY": rollup["c5_reconsideration_ready_count"] == 0,
        "EXEC_TARGET_DECIDE_16_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "EXEC_TARGET_DECIDE_17_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "EXEC_TARGET_DECIDE_18_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_EXEC_TARGET_POST_CLOSURE_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "selected": recommended_next,
        "records": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_exec_target_post_closure_decision_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_POST_CLOSURE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_execution_target_closure_receipt_id": EXEC_CLOSURE_RECEIPT_ID,
        "machine_readable_o2_exec_target_post_closure_decision_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_closure_decision_complete": decision_pass,
            "selected_next_branch": SELECTED_BRANCH if decision_pass else None,
            "selected_next_unit": recommended_next,
            "proposal_emission_authorized_next": decision_pass,
            "execution_target_reference_closed": decision_basis["execution_target_closed_as_reviewed_reference"],
            "templates_frozen_as_templates_only": decision_basis["templates_frozen_as_templates_only"],
            "question_answer_templates_available_count": len(qa_templates),
            "source_ref_satisfaction_templates_available_count": len(source_templates),
            "under_typed_acceptance_review_templates_available_count": len(undertyped_templates),
            "parking_execution_continuation_templates_available_count": len(parking_templates),
            "proposed_resolution_record_templates_available_count": len(resolution_templates),
            "proposal_route_map_records_available_count": len(proposal_routes),
            "decision_unit_emitted_records": False,
            "execution_attempted": False,
            "weak_feedback_resolved": False,
            "resolution_records_emitted_count": 0,
            "proposed_resolution_records_emitted_count": 0,
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
            "proposal_emission_authorization": rel(PROPOSAL_EMISSION_AUTH_PATH),
            "template_input_scope": rel(TEMPLATE_INPUT_SCOPE_PATH),
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
    print(f"exec_target_post_closure_decision_receipt_id={receipt_id}")
    print(f"exec_target_post_closure_decision_receipt_path={rel(receipt_path)}")
    print(f"exec_target_post_closure_decision_basis_path={rel(DECISION_BASIS_PATH)}")
    print(f"exec_target_post_closure_decision_table_path={rel(DECISION_TABLE_PATH)}")
    print(f"exec_target_selected_next_branch_path={rel(SELECTED_BRANCH_PATH)}")
    print(f"proposal_emission_authorization_path={rel(PROPOSAL_EMISSION_AUTH_PATH)}")
    print(f"proposal_emission_input_scope_path={rel(TEMPLATE_INPUT_SCOPE_PATH)}")
    print(f"exec_target_post_closure_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"exec_target_post_closure_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
