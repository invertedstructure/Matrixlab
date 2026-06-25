#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_final_resolution_closure_review.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REVIEW"
MODE = "REVIEW / FINAL_RESOLUTION_CLOSURE_INTEGRITY / WEAK_FEEDBACK_RESOLVED / C5_STILL_BLOCKED"
BUILD_MODE = "O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REVIEW_ONLY"

SOURCE_FINAL_RECEIPT_ID = "283a503b"

SOURCE_FINAL_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0_receipts/283a503b.json"
EXECUTION_RECORD_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_closure_execution_record_v0.json"
FINAL_QA_RECORDS_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_question_answer_closure_records_v0.jsonl"
FINAL_SOURCE_REF_RECORDS_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_source_ref_satisfaction_closure_records_v0.jsonl"
FINAL_UNDERTYPED_RECORDS_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_under_typed_acceptance_closure_records_v0.jsonl"
FINAL_PARKING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_parking_continuation_closure_records_v0.jsonl"
FINAL_RESOLUTION_RECORDS_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_weak_feedback_resolution_records_v0.jsonl"
FINAL_ROUTE_RECORDS_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_route_closure_records_v0.jsonl"
RESOLVED_STATUS_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_weak_feedback_resolved_status_v0.json"
FINAL_BOUNDARY_CROSSING_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_boundary_crossing_v0.json"
C5_BLOCK_AFTER_FINAL_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_c5_block_after_final_resolution_closure_v0.json"
INPUT_CONFIRMATION_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_closure_input_confirmation_v0.json"
FINAL_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_closure_authority_boundary_v0.json"
FINAL_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_closure_classification_v0.json"
FINAL_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_closure_rollup_v0.json"
FINAL_PROFILE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_closure_profile_v0.json"
FINAL_REPORT_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_closure_report.json"
FINAL_TRACE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_closure_transition_trace.json"

SOURCE_DECISION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0_receipts/34bab59d.json"
SOURCE_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0_receipts/2f793867.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_FINAL_RECEIPT_PATH,
    EXECUTION_RECORD_PATH,
    FINAL_QA_RECORDS_PATH,
    FINAL_SOURCE_REF_RECORDS_PATH,
    FINAL_UNDERTYPED_RECORDS_PATH,
    FINAL_PARKING_RECORDS_PATH,
    FINAL_RESOLUTION_RECORDS_PATH,
    FINAL_ROUTE_RECORDS_PATH,
    RESOLVED_STATUS_PATH,
    FINAL_BOUNDARY_CROSSING_PATH,
    C5_BLOCK_AFTER_FINAL_PATH,
    INPUT_CONFIRMATION_PATH,
    FINAL_AUTHORITY_PATH,
    FINAL_CLASSIFICATION_PATH,
    FINAL_ROLLUP_PATH,
    FINAL_PROFILE_PATH,
    FINAL_REPORT_PATH,
    FINAL_TRACE_PATH,
    SOURCE_DECISION_RECEIPT_PATH,
    SOURCE_CLOSURE_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "o2_final_resolution_closure_review_assessment_v0.json"
FINAL_RECORD_INTEGRITY_REVIEW_PATH = OUT_DIR / "o2_final_resolution_record_integrity_review_v0.json"
FINAL_BASIS_REVIEW_PATH = OUT_DIR / "o2_final_basis_record_review_v0.json"
FINAL_ROUTE_REVIEW_PATH = OUT_DIR / "o2_final_route_closure_review_v0.json"
RESOLVED_STATUS_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_resolved_status_review_v0.json"
FINAL_BOUNDARY_REVIEW_PATH = OUT_DIR / "o2_final_resolution_boundary_crossing_review_v0.json"
C5_BLOCK_REVIEW_PATH = OUT_DIR / "o2_c5_block_after_final_resolution_review_v0.json"
PARKING_REVIEW_PATH = OUT_DIR / "o2_final_parking_non_resolution_review_v0.json"
CLOSURE_CANDIDATE_PATH = OUT_DIR / "o2_final_resolution_closure_reviewed_reference_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_final_resolution_closure_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_final_resolution_closure_review_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_final_resolution_closure_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_final_resolution_closure_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_final_resolution_closure_review_report.json"
TRACE_PATH = OUT_DIR / "o2_final_resolution_closure_review_transition_trace.json"

EXPECTED_FINAL_STATUS = "TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_EXECUTED_RESOLUTION_RECORDS_REVIEW_READY"
EXPECTED_FINAL_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_EXECUTED_RESOLUTION_RECORDS_REVIEW_READY"
EXPECTED_FINAL_NEXT = "REVIEW_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_V0"
RECOMMENDED_NEXT = "CLOSE_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_AS_REVIEWED_REFERENCE_V0"

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
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    receipt = read_json(SOURCE_FINAL_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_final_resolution_closure_summary", {})
    execution_record = read_json(EXECUTION_RECORD_PATH)
    final_qa = read_jsonl(FINAL_QA_RECORDS_PATH)
    final_source = read_jsonl(FINAL_SOURCE_REF_RECORDS_PATH)
    final_undertyped = read_jsonl(FINAL_UNDERTYPED_RECORDS_PATH)
    final_parking = read_jsonl(FINAL_PARKING_RECORDS_PATH)
    final_resolution = read_jsonl(FINAL_RESOLUTION_RECORDS_PATH)
    final_routes = read_jsonl(FINAL_ROUTE_RECORDS_PATH)
    resolved_status = read_json(RESOLVED_STATUS_PATH)
    boundary_crossing = read_json(FINAL_BOUNDARY_CROSSING_PATH)
    c5_block = read_json(C5_BLOCK_AFTER_FINAL_PATH)
    input_confirmation = read_json(INPUT_CONFIRMATION_PATH)
    authority = read_json(FINAL_AUTHORITY_PATH)
    classification = read_json(FINAL_CLASSIFICATION_PATH)
    rollup = read_json(FINAL_ROLLUP_PATH)
    profile = read_json(FINAL_PROFILE_PATH)
    report = read_json(FINAL_REPORT_PATH)
    trace = read_json(FINAL_TRACE_PATH)
    decision_receipt = read_json(SOURCE_DECISION_RECEIPT_PATH)
    closure_receipt = read_json(SOURCE_CLOSURE_RECEIPT_PATH)

    if receipt.get("receipt_id") != SOURCE_FINAL_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_final_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_FINAL_STOP:
        failures.append("source_final_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_final_hidden_next")
    if summary.get("status") != EXPECTED_FINAL_STATUS:
        failures.append(f"source_final_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_FINAL_NEXT:
        failures.append(f"source_final_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "final_resolution_closure_executed",
        "review_ready",
        "question_packets_answered",
        "source_ref_requests_satisfied",
        "under_typed_acceptance_approved",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "final_question_answer_closure_records_emitted_count": 3,
        "final_source_ref_closure_records_emitted_count": 2,
        "final_under_typed_acceptance_closure_records_emitted_count": 2,
        "final_parking_closure_records_emitted_count": 3,
        "final_resolution_records_emitted_count": 3,
        "resolution_records_emitted_count": 3,
        "final_route_closure_records_emitted_count": 3,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

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
        failures.append("summary_c5_readiness_wrong")

    if execution_record.get("execution_status") != "FINAL_RESOLUTION_CLOSURE_EXECUTED_REVIEW_READY":
        failures.append("execution_status_wrong")
    if execution_record.get("final_resolution_records_emitted_count") != 3:
        failures.append("execution_final_count_wrong")
    if execution_record.get("weak_feedback_resolved") is not True or execution_record.get("final_resolution_boundary_crossed") is not True:
        failures.append("execution_resolution_not_true")
    if execution_record.get("c5_reconsideration_ready") is not False or execution_record.get("c5_opened") is not False:
        failures.append("execution_c5_wrong")

    if len(final_qa) != 3 or len(final_source) != 2 or len(final_undertyped) != 2 or len(final_parking) != 3 or len(final_resolution) != 3 or len(final_routes) != 3:
        failures.append("final_record_counts_wrong")

    for row in final_qa:
        if row.get("closure_status") != "FINAL_CLOSURE_ACCEPTED" or row.get("counts_as_final_answer_basis") is not True:
            failures.append(f"final_qa_wrong:{row.get('final_question_answer_closure_id')}")
        if row.get("weak_feedback_resolved_by_this_record") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"final_qa_boundary_wrong:{row.get('final_question_answer_closure_id')}")
    for row in final_source:
        if row.get("closure_status") != "FINAL_CLOSURE_ACCEPTED" or row.get("counts_as_final_source_ref_basis") is not True:
            failures.append(f"final_source_wrong:{row.get('final_source_ref_closure_id')}")
    for row in final_undertyped:
        if row.get("closure_status") != "FINAL_CLOSURE_ACCEPTED" or row.get("counts_as_final_under_typed_acceptance_basis") is not True:
            failures.append(f"final_undertyped_wrong:{row.get('final_under_typed_acceptance_closure_id')}")
    for row in final_parking:
        if row.get("closure_status") != "FINAL_PARKING_CONTINUES" or row.get("counts_as_final_resolution") is not False:
            failures.append(f"final_parking_wrong:{row.get('final_parking_continuation_closure_id')}")
        if row.get("weak_feedback_resolved_by_this_record") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"final_parking_boundary_wrong:{row.get('final_parking_continuation_closure_id')}")
    for row in final_resolution:
        if row.get("closure_status") != "FINAL_RESOLUTION_CLOSED":
            failures.append(f"final_resolution_status_wrong:{row.get('final_resolution_id')}")
        if row.get("counts_as_final_resolution") is not True or row.get("weak_feedback_resolved") is not True:
            failures.append(f"final_resolution_not_resolving:{row.get('final_resolution_id')}")
        if row.get("final_resolution_boundary_crossed") is not True:
            failures.append(f"final_resolution_boundary_not_crossed:{row.get('final_resolution_id')}")
        if row.get("c5_reconsideration_ready") is not False or row.get("c5_opened") is not False:
            failures.append(f"final_resolution_c5_wrong:{row.get('final_resolution_id')}")
        if row.get("review_required_next") is not True:
            failures.append(f"final_resolution_review_gate_missing:{row.get('final_resolution_id')}")
    for row in final_routes:
        if row.get("closure_status") != "FINAL_ROUTE_CLOSED" or row.get("final_resolution_record_emitted") is not True:
            failures.append(f"final_route_wrong:{row.get('final_route_closure_id')}")
        if row.get("weak_feedback_resolved") is not True:
            failures.append(f"final_route_not_resolving:{row.get('final_route_closure_id')}")
        if row.get("c5_reconsideration_ready") is not False or row.get("c5_opened") is not False:
            failures.append(f"final_route_c5_wrong:{row.get('final_route_closure_id')}")

    if resolved_status.get("weak_feedback_resolved") is not True or resolved_status.get("resolution_records_emitted_count") != 3:
        failures.append("resolved_status_wrong")
    if resolved_status.get("c5_reconsideration_ready") is not False or resolved_status.get("c5_opened") is not False:
        failures.append("resolved_status_c5_wrong")
    if boundary_crossing.get("final_resolution_boundary_crossed") is not True or boundary_crossing.get("weak_feedback_resolved") is not True:
        failures.append("boundary_crossing_wrong")
    if boundary_crossing.get("parking_counted_as_resolution") is not False:
        failures.append("boundary_parking_wrong")
    if c5_block.get("c5_feedback_readiness") != "BLOCKED_PENDING_C5_DECISION" or c5_block.get("c5_opened") is not False:
        failures.append("c5_block_wrong")
    if input_confirmation.get("reviewed_resolution_records_count") != 3:
        failures.append("input_confirmation_wrong")
    if authority.get("may_review_final_resolution_closure_next") is not True:
        failures.append("authority_no_review_next")
    if authority.get("may_set_c5_reconsideration_ready_now") is not False or authority.get("may_open_c5_now") is not False:
        failures.append("authority_allows_c5")
    if classification.get("recommended_next") != EXPECTED_FINAL_NEXT:
        failures.append("classification_next_wrong")
    if rollup.get("weak_feedback_resolved_count") != 1 or rollup.get("final_resolution_boundary_crossed_count") != 1:
        failures.append("rollup_resolution_wrong")
    if rollup.get("c5_opened_count") != 0 or rollup.get("c5_reconsideration_ready_count") != 0:
        failures.append("rollup_c5_wrong")
    if profile.get("weak_feedback_resolved") is not True or profile.get("final_resolution_boundary_crossed") is not True:
        failures.append("profile_resolution_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_FINAL_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_FINAL_STOP:
        failures.append("trace_stop_wrong")
    if decision_receipt.get("receipt_id") != "34bab59d" or decision_receipt.get("gate") != "PASS":
        failures.append("decision_receipt_wrong")
    if closure_receipt.get("receipt_id") != "2f793867" or closure_receipt.get("gate") != "PASS":
        failures.append("closure_receipt_wrong")

    return failures, {
        "final_qa": final_qa,
        "final_source": final_source,
        "final_undertyped": final_undertyped,
        "final_parking": final_parking,
        "final_resolution": final_resolution,
        "final_routes": final_routes,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    final_qa = src.get("final_qa", [])
    final_source = src.get("final_source", [])
    final_undertyped = src.get("final_undertyped", [])
    final_parking = src.get("final_parking", [])
    final_resolution = src.get("final_resolution", [])
    final_routes = src.get("final_routes", [])

    review_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REVIEWED_CLEAN_CLOSE_READY" if review_pass else "TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REVIEW_V0"

    reason_codes = [
        "FINAL_RESOLUTION_CLOSURE_REVIEW_COMPLETE",
        "FINAL_RESOLUTION_CLOSURE_RECEIPT_CONSUMED",
        "FINAL_RESOLUTION_EXECUTION_RECORD_CONFIRMED",
        "FINAL_BASIS_RECORDS_CONFIRMED",
        "FINAL_WEAK_FEEDBACK_RESOLUTION_RECORDS_CONFIRMED",
        "FINAL_RESOLUTION_BOUNDARY_CROSSING_CONFIRMED",
        "WEAK_FEEDBACK_RESOLVED_STATUS_CONFIRMED",
        "PARKING_CONFIRMED_NOT_COUNTED_AS_RESOLUTION",
        "C5_BLOCK_CONFIRMED_PENDING_C5_DECISION",
        "FINAL_CLOSURE_CLOSE_CANDIDATE_READY",
        "NO_C5_RECONSIDERATION_READY",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if review_pass else failures

    review_assessment = {
        "schema_version": "o2_final_resolution_closure_review_assessment_v0",
        "review_status": status,
        "review_complete": review_pass,
        "review_pass": review_pass,
        "source_final_resolution_closure_receipt_id": SOURCE_FINAL_RECEIPT_ID,
        "final_resolution_closure_integrity_validated": review_pass,
        "close_candidate_ready": review_pass,
        "recommended_next": recommended_next,
    }

    final_record_integrity = {
        "schema_version": "o2_final_resolution_record_integrity_review_v0",
        "review_status": "FINAL_RESOLUTION_RECORD_INTEGRITY_REVIEW_PASS" if review_pass else "FINAL_RESOLUTION_RECORD_INTEGRITY_REVIEW_FAIL",
        "final_resolution_records_reviewed_count": len(final_resolution),
        "all_final_resolution_records_closed": all(x.get("closure_status") == "FINAL_RESOLUTION_CLOSED" for x in final_resolution),
        "all_count_as_final_resolution": all(x.get("counts_as_final_resolution") is True for x in final_resolution),
        "all_weak_feedback_resolved": all(x.get("weak_feedback_resolved") is True for x in final_resolution),
        "all_c5_not_ready_not_open": all(x.get("c5_reconsideration_ready") is False and x.get("c5_opened") is False for x in final_resolution),
    }

    final_basis_review = {
        "schema_version": "o2_final_basis_record_review_v0",
        "review_status": "FINAL_BASIS_RECORD_REVIEW_PASS" if review_pass else "FINAL_BASIS_RECORD_REVIEW_FAIL",
        "final_question_answer_records_reviewed_count": len(final_qa),
        "final_source_ref_records_reviewed_count": len(final_source),
        "final_under_typed_acceptance_records_reviewed_count": len(final_undertyped),
        "question_packets_answered": True,
        "source_ref_requests_satisfied": True,
        "under_typed_acceptance_approved": True,
    }

    final_route_review = {
        "schema_version": "o2_final_route_closure_review_v0",
        "review_status": "FINAL_ROUTE_CLOSURE_REVIEW_PASS" if review_pass else "FINAL_ROUTE_CLOSURE_REVIEW_FAIL",
        "final_route_records_reviewed_count": len(final_routes),
        "all_final_routes_closed": all(x.get("closure_status") == "FINAL_ROUTE_CLOSED" for x in final_routes),
        "all_final_resolution_record_emitted": all(x.get("final_resolution_record_emitted") is True for x in final_routes),
        "all_c5_not_ready_not_open": all(x.get("c5_reconsideration_ready") is False and x.get("c5_opened") is False for x in final_routes),
    }

    resolved_status_review = {
        "schema_version": "o2_weak_feedback_resolved_status_review_v0",
        "review_status": "WEAK_FEEDBACK_RESOLVED_STATUS_REVIEW_PASS" if review_pass else "WEAK_FEEDBACK_RESOLVED_STATUS_REVIEW_FAIL",
        "weak_feedback_resolved": True,
        "resolution_records_emitted_count": len(final_resolution),
        "final_resolution_records_emitted_count": len(final_resolution),
        "review_required_before_c5_decision": True,
    }

    final_boundary_review = {
        "schema_version": "o2_final_resolution_boundary_crossing_review_v0",
        "review_status": "FINAL_RESOLUTION_BOUNDARY_CROSSING_REVIEW_PASS" if review_pass else "FINAL_RESOLUTION_BOUNDARY_CROSSING_REVIEW_FAIL",
        "final_resolution_boundary_crossed": True,
        "weak_feedback_resolved": True,
        "reviewed_to_final_crossing_validated": review_pass,
        "parking_counted_as_resolution": False,
    }

    c5_block_review = {
        "schema_version": "o2_c5_block_after_final_resolution_review_v0",
        "review_status": "C5_BLOCK_AFTER_FINAL_RESOLUTION_REVIEW_PASS" if review_pass else "C5_BLOCK_AFTER_FINAL_RESOLUTION_REVIEW_FAIL",
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "block_enforced": True,
        "c5_decision_required_after_reviewed_final_resolution_closure": True,
    }

    parking_review = {
        "schema_version": "o2_final_parking_non_resolution_review_v0",
        "review_status": "FINAL_PARKING_NON_RESOLUTION_REVIEW_PASS" if review_pass else "FINAL_PARKING_NON_RESOLUTION_REVIEW_FAIL",
        "final_parking_records_reviewed_count": len(final_parking),
        "parking_counted_as_resolution": False,
        "all_parking_not_resolution": all(x.get("counts_as_final_resolution") is False for x in final_parking),
    }

    closure_candidate = {
        "schema_version": "o2_final_resolution_closure_reviewed_reference_candidate_v0",
        "candidate_status": "FINAL_RESOLUTION_CLOSURE_CLOSE_READY_AS_REVIEWED_REFERENCE" if review_pass else "FINAL_RESOLUTION_CLOSURE_NOT_CLOSE_READY",
        "review_pass": review_pass,
        "close_candidate_ready": review_pass,
        "closure_meaning": "Close final-resolution closure output as reviewed reference.",
        "closure_does_not_mean": [
            "C5 reconsideration ready",
            "C5 opened",
            "live feedback audit executed",
            "runtime patched",
            "source mutated",
        ],
        "recommended_next": recommended_next,
    }

    authority_boundary = {
        "schema_version": "o2_final_resolution_closure_review_authority_boundary_v0",
        "status": status,
        "may_close_final_resolution_closure_as_reviewed_reference_next": review_pass,
        "may_set_c5_reconsideration_ready_now": False,
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
        "schema_version": "o2_final_resolution_closure_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "final_resolution_closure_review_complete": review_pass,
        "final_resolution_closure_review_pass": review_pass,
        "final_resolution_closure_integrity_validated": review_pass,
        "close_candidate_ready": review_pass,
        "final_resolution_closure_executed": True,
        "review_ready": True,
        "question_packets_answered": True,
        "source_ref_requests_satisfied": True,
        "under_typed_acceptance_approved": True,
        "final_question_answer_closure_records_reviewed_count": len(final_qa),
        "final_source_ref_closure_records_reviewed_count": len(final_source),
        "final_under_typed_acceptance_records_reviewed_count": len(final_undertyped),
        "final_parking_closure_records_reviewed_count": len(final_parking),
        "final_resolution_records_reviewed_count": len(final_resolution),
        "resolution_records_emitted_count": len(final_resolution),
        "final_route_closure_records_reviewed_count": len(final_routes),
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "parking_counted_as_resolution": False,
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
        "schema_version": "o2_final_resolution_closure_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "close_candidate_ready_count": 1 if review_pass else 0,
        "final_resolution_integrity_validated_count": 1 if review_pass else 0,
        "final_question_answer_closure_records_reviewed_count": len(final_qa),
        "final_source_ref_closure_records_reviewed_count": len(final_source),
        "final_under_typed_acceptance_records_reviewed_count": len(final_undertyped),
        "final_parking_closure_records_reviewed_count": len(final_parking),
        "final_resolution_records_reviewed_count": len(final_resolution),
        "resolution_records_emitted_count": len(final_resolution),
        "final_route_closure_records_reviewed_count": len(final_routes),
        "weak_feedback_resolved_count": 1,
        "final_resolution_boundary_crossed_count": 1,
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
        "schema_version": "o2_final_resolution_closure_review_profile_v0",
        "profile_id": "o2_final_resolution_closure_review_profile_" + sha8(rollup),
        "status": status,
        "final_resolution_closure_review_pass": review_pass,
        "final_resolution_closure_integrity_validated": review_pass,
        "close_candidate_ready": review_pass,
        "resolution_records_emitted_count": len(final_resolution),
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Close final-resolution closure as reviewed reference. C5 remains a separate decision edge.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_final_resolution_closure_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Final weak-feedback resolution closure reviewed clean: final records exist, weak feedback is resolved, and C5 remains blocked pending a later explicit C5 decision.",
        "resolution_records_emitted_count": len(final_resolution),
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_final_resolution_closure_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_final_resolution_closure",
                "question": "did final-resolution closure execute cleanly",
                "answer": "yes" if review_pass else "no",
                "taken": "review final record integrity",
            },
            {
                "step": "verify_resolution_crossing",
                "question": "are final resolution records emitted and weak feedback resolved",
                "answer": "yes" if review_pass else "no",
                "taken": "confirm final boundary crossing",
            },
            {
                "step": "verify_c5_block",
                "question": "did final-resolution closure open C5",
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
        (FINAL_RECORD_INTEGRITY_REVIEW_PATH, final_record_integrity),
        (FINAL_BASIS_REVIEW_PATH, final_basis_review),
        (FINAL_ROUTE_REVIEW_PATH, final_route_review),
        (RESOLVED_STATUS_REVIEW_PATH, resolved_status_review),
        (FINAL_BOUNDARY_REVIEW_PATH, final_boundary_review),
        (C5_BLOCK_REVIEW_PATH, c5_block_review),
        (PARKING_REVIEW_PATH, parking_review),
        (CLOSURE_CANDIDATE_PATH, closure_candidate),
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
        "FINAL_CLOSURE_REVIEW_0_SOURCE_FINAL_RECEIPT_CONSUMED": SOURCE_FINAL_RECEIPT_PATH.exists(),
        "FINAL_CLOSURE_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "FINAL_CLOSURE_REVIEW_2_FINAL_RECORD_INTEGRITY_REVIEWED": final_record_integrity["all_final_resolution_records_closed"] is True and final_record_integrity["all_weak_feedback_resolved"] is True,
        "FINAL_CLOSURE_REVIEW_3_FINAL_BASIS_REVIEWED": final_basis_review["question_packets_answered"] is True and final_basis_review["source_ref_requests_satisfied"] is True and final_basis_review["under_typed_acceptance_approved"] is True,
        "FINAL_CLOSURE_REVIEW_4_FINAL_ROUTES_REVIEWED": final_route_review["all_final_resolution_record_emitted"] is True,
        "FINAL_CLOSURE_REVIEW_5_WEAK_FEEDBACK_RESOLVED_STATUS_CONFIRMED": resolved_status_review["weak_feedback_resolved"] is True and resolved_status_review["resolution_records_emitted_count"] == 3,
        "FINAL_CLOSURE_REVIEW_6_FINAL_BOUNDARY_CROSSING_CONFIRMED": final_boundary_review["final_resolution_boundary_crossed"] is True,
        "FINAL_CLOSURE_REVIEW_7_PARKING_NOT_RESOLUTION": parking_review["parking_counted_as_resolution"] is False,
        "FINAL_CLOSURE_REVIEW_8_C5_BLOCK_CONFIRMED": c5_block_review["c5_opened"] is False and c5_block_review["c5_reconsideration_ready"] is False,
        "FINAL_CLOSURE_REVIEW_9_CLOSE_CANDIDATE_READY": closure_candidate["close_candidate_ready"] is True,
        "FINAL_CLOSURE_REVIEW_10_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "FINAL_CLOSURE_REVIEW_11_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "FINAL_CLOSURE_REVIEW_12_NO_C5_OPEN": rollup["c5_opened_count"] == 0 and rollup["c5_reconsideration_ready_count"] == 0,
        "FINAL_CLOSURE_REVIEW_13_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "FINAL_CLOSURE_REVIEW_14_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "FINAL_CLOSURE_REVIEW_15_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "resolution_records": len(final_resolution),
        "weak_feedback_resolved": True,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_final_resolution_closure_review_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_final_resolution_closure_receipt_id": SOURCE_FINAL_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_final_resolution_closure_review_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "final_resolution_closure_review_complete": review_pass,
            "final_resolution_closure_review_pass": review_pass,
            "final_resolution_closure_integrity_validated": review_pass,
            "close_candidate_ready": review_pass,
            "final_resolution_closure_executed": True,
            "review_ready": True,
            "question_packets_answered": True,
            "source_ref_requests_satisfied": True,
            "under_typed_acceptance_approved": True,
            "final_question_answer_closure_records_reviewed_count": len(final_qa),
            "final_source_ref_closure_records_reviewed_count": len(final_source),
            "final_under_typed_acceptance_records_reviewed_count": len(final_undertyped),
            "final_parking_closure_records_reviewed_count": len(final_parking),
            "final_resolution_records_reviewed_count": len(final_resolution),
            "resolution_records_emitted_count": len(final_resolution),
            "final_route_closure_records_reviewed_count": len(final_routes),
            "weak_feedback_resolved": True,
            "final_resolution_boundary_crossed": True,
            "parking_counted_as_resolution": False,
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
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "final_record_integrity_review": rel(FINAL_RECORD_INTEGRITY_REVIEW_PATH),
            "final_basis_review": rel(FINAL_BASIS_REVIEW_PATH),
            "final_route_review": rel(FINAL_ROUTE_REVIEW_PATH),
            "resolved_status_review": rel(RESOLVED_STATUS_REVIEW_PATH),
            "final_boundary_review": rel(FINAL_BOUNDARY_REVIEW_PATH),
            "c5_block_review": rel(C5_BLOCK_REVIEW_PATH),
            "parking_review": rel(PARKING_REVIEW_PATH),
            "closure_candidate": rel(CLOSURE_CANDIDATE_PATH),
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
    print(f"final_resolution_closure_review_receipt_id={receipt_id}")
    print(f"final_resolution_closure_review_receipt_path={rel(receipt_path)}")
    print(f"final_resolution_closure_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"final_record_integrity_review_path={rel(FINAL_RECORD_INTEGRITY_REVIEW_PATH)}")
    print(f"weak_feedback_resolved_status_review_path={rel(RESOLVED_STATUS_REVIEW_PATH)}")
    print(f"final_boundary_review_path={rel(FINAL_BOUNDARY_REVIEW_PATH)}")
    print(f"c5_block_review_path={rel(C5_BLOCK_REVIEW_PATH)}")
    print(f"final_resolution_closure_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"final_resolution_closure_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
