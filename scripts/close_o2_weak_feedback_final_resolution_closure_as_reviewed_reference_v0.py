#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_final_resolution_closure_reference_closure.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REFERENCE_CLOSURE"
MODE = "CLOSE / FREEZE_FINAL_RESOLUTION_CLOSURE_AS_REVIEWED_REFERENCE / C5_DECISION_PENDING"
BUILD_MODE = "O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REFERENCE_CLOSURE_ONLY"

SOURCE_REVIEW_RECEIPT_ID = "362cb1b2"

SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0_receipts/362cb1b2.json"
REVIEW_ASSESSMENT_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_final_resolution_closure_review_assessment_v0.json"
FINAL_RECORD_INTEGRITY_REVIEW_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_final_resolution_record_integrity_review_v0.json"
FINAL_BASIS_REVIEW_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_final_basis_record_review_v0.json"
FINAL_ROUTE_REVIEW_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_final_route_closure_review_v0.json"
RESOLVED_STATUS_REVIEW_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_weak_feedback_resolved_status_review_v0.json"
FINAL_BOUNDARY_REVIEW_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_final_resolution_boundary_crossing_review_v0.json"
C5_BLOCK_REVIEW_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_c5_block_after_final_resolution_review_v0.json"
PARKING_REVIEW_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_final_parking_non_resolution_review_v0.json"
CLOSURE_CANDIDATE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_final_resolution_closure_reviewed_reference_candidate_v0.json"
REVIEW_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_final_resolution_closure_review_authority_boundary_v0.json"
REVIEW_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_final_resolution_closure_review_classification_v0.json"
REVIEW_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_final_resolution_closure_review_rollup_v0.json"
REVIEW_PROFILE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_final_resolution_closure_review_profile_v0.json"
REVIEW_REPORT_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_final_resolution_closure_review_report.json"
REVIEW_TRACE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_review_v0/o2_final_resolution_closure_review_transition_trace.json"

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
FINAL_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_closure_rollup_v0.json"
FINAL_PROFILE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_closure_profile_v0.json"
FINAL_REPORT_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_closure_report.json"
FINAL_TRACE_PATH = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0/o2_final_resolution_closure_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_REVIEW_RECEIPT_PATH,
    REVIEW_ASSESSMENT_PATH,
    FINAL_RECORD_INTEGRITY_REVIEW_PATH,
    FINAL_BASIS_REVIEW_PATH,
    FINAL_ROUTE_REVIEW_PATH,
    RESOLVED_STATUS_REVIEW_PATH,
    FINAL_BOUNDARY_REVIEW_PATH,
    C5_BLOCK_REVIEW_PATH,
    PARKING_REVIEW_PATH,
    CLOSURE_CANDIDATE_PATH,
    REVIEW_AUTHORITY_PATH,
    REVIEW_CLASSIFICATION_PATH,
    REVIEW_ROLLUP_PATH,
    REVIEW_PROFILE_PATH,
    REVIEW_REPORT_PATH,
    REVIEW_TRACE_PATH,
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
    FINAL_ROLLUP_PATH,
    FINAL_PROFILE_PATH,
    FINAL_REPORT_PATH,
    FINAL_TRACE_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_final_resolution_closure_reference_closure_v0_receipts"

CLOSURE_RECORD_PATH = OUT_DIR / "o2_final_resolution_closure_reference_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "o2_final_resolution_closure_reviewed_reference_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "o2_final_resolution_closure_reference_index_v0.json"
FINAL_RESOLUTION_RECORDS_REFERENCE_PATH = OUT_DIR / "o2_final_weak_feedback_resolution_records_reference_v0.json"
RESOLVED_STATUS_REFERENCE_PATH = OUT_DIR / "o2_weak_feedback_resolved_status_reference_v0.json"
FINAL_BOUNDARY_REFERENCE_PATH = OUT_DIR / "o2_final_resolution_boundary_crossing_reference_v0.json"
C5_BLOCK_REFERENCE_PATH = OUT_DIR / "o2_c5_block_pending_decision_reference_v0.json"
POST_CLOSURE_DECISION_READINESS_PATH = OUT_DIR / "o2_post_final_resolution_closure_reference_decision_readiness_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_final_resolution_closure_reference_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_final_resolution_closure_reference_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_final_resolution_closure_reference_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_final_resolution_closure_reference_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_final_resolution_closure_reference_closure_report.json"
TRACE_PATH = OUT_DIR / "o2_final_resolution_closure_reference_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REVIEWED_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REVIEWED_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_AS_REVIEWED_REFERENCE_V0"
RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REFERENCE_CLOSURE_V0"

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

    review_receipt = read_json(SOURCE_REVIEW_RECEIPT_PATH)
    review_summary = review_receipt.get("machine_readable_o2_weak_feedback_final_resolution_closure_review_summary", {})
    review_assessment = read_json(REVIEW_ASSESSMENT_PATH)
    record_integrity = read_json(FINAL_RECORD_INTEGRITY_REVIEW_PATH)
    basis_review = read_json(FINAL_BASIS_REVIEW_PATH)
    route_review = read_json(FINAL_ROUTE_REVIEW_PATH)
    resolved_review = read_json(RESOLVED_STATUS_REVIEW_PATH)
    boundary_review = read_json(FINAL_BOUNDARY_REVIEW_PATH)
    c5_review = read_json(C5_BLOCK_REVIEW_PATH)
    parking_review = read_json(PARKING_REVIEW_PATH)
    closure_candidate = read_json(CLOSURE_CANDIDATE_PATH)
    review_authority = read_json(REVIEW_AUTHORITY_PATH)
    review_classification = read_json(REVIEW_CLASSIFICATION_PATH)
    review_rollup = read_json(REVIEW_ROLLUP_PATH)
    review_profile = read_json(REVIEW_PROFILE_PATH)
    review_report = read_json(REVIEW_REPORT_PATH)
    review_trace = read_json(REVIEW_TRACE_PATH)

    final_receipt = read_json(SOURCE_FINAL_RECEIPT_PATH)
    final_summary = final_receipt.get("machine_readable_o2_weak_feedback_final_resolution_closure_summary", {})
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
    final_rollup = read_json(FINAL_ROLLUP_PATH)
    final_profile = read_json(FINAL_PROFILE_PATH)
    final_report = read_json(FINAL_REPORT_PATH)
    final_trace = read_json(FINAL_TRACE_PATH)

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
        "final_resolution_closure_review_complete",
        "final_resolution_closure_review_pass",
        "final_resolution_closure_integrity_validated",
        "close_candidate_ready",
        "final_resolution_closure_executed",
        "review_ready",
        "question_packets_answered",
        "source_ref_requests_satisfied",
        "under_typed_acceptance_approved",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_summary_required_true_missing:{key}")

    expected_counts = {
        "final_question_answer_closure_records_reviewed_count": 3,
        "final_source_ref_closure_records_reviewed_count": 2,
        "final_under_typed_acceptance_records_reviewed_count": 2,
        "final_parking_closure_records_reviewed_count": 3,
        "final_resolution_records_reviewed_count": 3,
        "resolution_records_emitted_count": 3,
        "final_route_closure_records_reviewed_count": 3,
    }
    for key, expected in expected_counts.items():
        if review_summary.get(key) != expected:
            failures.append(f"review_summary_count_wrong:{key}:{review_summary.get(key)}")

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
        if review_summary.get(key) is not False:
            failures.append(f"review_summary_forbidden_true:{key}")

    if review_summary.get("c5_feedback_readiness") != "BLOCKED_PENDING_C5_DECISION":
        failures.append("review_summary_c5_wrong")
    if review_assessment.get("close_candidate_ready") is not True or review_assessment.get("review_pass") is not True:
        failures.append("review_assessment_not_close_ready")
    if record_integrity.get("all_final_resolution_records_closed") is not True or record_integrity.get("all_weak_feedback_resolved") is not True:
        failures.append("record_integrity_wrong")
    if basis_review.get("question_packets_answered") is not True or basis_review.get("source_ref_requests_satisfied") is not True or basis_review.get("under_typed_acceptance_approved") is not True:
        failures.append("basis_review_wrong")
    if route_review.get("all_final_routes_closed") is not True or route_review.get("all_final_resolution_record_emitted") is not True:
        failures.append("route_review_wrong")
    if resolved_review.get("weak_feedback_resolved") is not True or resolved_review.get("resolution_records_emitted_count") != 3:
        failures.append("resolved_review_wrong")
    if boundary_review.get("final_resolution_boundary_crossed") is not True or boundary_review.get("weak_feedback_resolved") is not True:
        failures.append("boundary_review_wrong")
    if c5_review.get("c5_feedback_readiness") != "BLOCKED_PENDING_C5_DECISION" or c5_review.get("c5_opened") is not False:
        failures.append("c5_review_wrong")
    if parking_review.get("parking_counted_as_resolution") is not False or parking_review.get("all_parking_not_resolution") is not True:
        failures.append("parking_review_wrong")
    if closure_candidate.get("close_candidate_ready") is not True:
        failures.append("closure_candidate_not_ready")
    if review_authority.get("may_close_final_resolution_closure_as_reviewed_reference_next") is not True:
        failures.append("review_authority_no_close")
    if review_authority.get("may_open_c5_now") is not False or review_authority.get("may_set_c5_reconsideration_ready_now") is not False:
        failures.append("review_authority_allows_c5")
    if review_classification.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append("review_classification_next_wrong")
    if review_rollup.get("review_pass_count") != 1 or review_rollup.get("close_candidate_ready_count") != 1:
        failures.append("review_rollup_wrong")
    if review_profile.get("next_command_goal") is not None:
        failures.append("review_profile_hidden_next")
    if review_report.get("recommended_next_handling") != EXPECTED_REVIEW_NEXT:
        failures.append("review_report_next_wrong")
    if review_trace.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("review_trace_stop_wrong")

    if final_receipt.get("receipt_id") != "283a503b" or final_receipt.get("gate") != "PASS":
        failures.append("final_receipt_not_pass")
    if final_summary.get("weak_feedback_resolved") is not True or final_summary.get("final_resolution_boundary_crossed") is not True:
        failures.append("final_summary_resolution_wrong")
    if final_summary.get("c5_opened") is not False or final_summary.get("c5_reconsideration_ready") is not False:
        failures.append("final_summary_c5_wrong")
    if execution_record.get("final_resolution_records_emitted_count") != 3 or execution_record.get("weak_feedback_resolved") is not True:
        failures.append("execution_record_wrong")
    if len(final_qa) != 3 or len(final_source) != 2 or len(final_undertyped) != 2 or len(final_parking) != 3 or len(final_resolution) != 3 or len(final_routes) != 3:
        failures.append("final_record_counts_wrong")
    for row in final_resolution:
        if row.get("closure_status") != "FINAL_RESOLUTION_CLOSED" or row.get("counts_as_final_resolution") is not True or row.get("weak_feedback_resolved") is not True:
            failures.append(f"final_resolution_record_wrong:{row.get('final_resolution_id')}")
        if row.get("c5_reconsideration_ready") is not False or row.get("c5_opened") is not False:
            failures.append(f"final_resolution_record_c5_wrong:{row.get('final_resolution_id')}")
    for row in final_parking:
        if row.get("counts_as_final_resolution") is not False:
            failures.append(f"final_parking_counts_as_resolution:{row.get('final_parking_continuation_closure_id')}")
    if resolved_status.get("weak_feedback_resolved") is not True or resolved_status.get("resolution_records_emitted_count") != 3:
        failures.append("resolved_status_wrong")
    if boundary_crossing.get("final_resolution_boundary_crossed") is not True or boundary_crossing.get("weak_feedback_resolved") is not True:
        failures.append("boundary_crossing_wrong")
    if c5_block.get("c5_feedback_readiness") != "BLOCKED_PENDING_C5_DECISION" or c5_block.get("c5_opened") is not False:
        failures.append("c5_block_after_final_wrong")
    if final_rollup.get("weak_feedback_resolved_count") != 1 or final_rollup.get("c5_opened_count") != 0:
        failures.append("final_rollup_wrong")
    if final_profile.get("next_command_goal") is not None or final_profile.get("c5_reconsideration_ready") is not False:
        failures.append("final_profile_wrong")
    if final_report.get("recommended_next_handling") != "REVIEW_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_V0":
        failures.append("final_report_next_wrong")
    if final_trace.get("terminal", {}).get("stop_code") != "STOP_TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_EXECUTED_RESOLUTION_RECORDS_REVIEW_READY":
        failures.append("final_trace_stop_wrong")

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

    close_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_CLOSED_AS_REVIEWED_REFERENCE_C5_DECISION_READY" if close_pass else "TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REFERENCE_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if close_pass else "REPAIR_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REFERENCE_CLOSURE_V0"

    reason_codes = [
        "FINAL_RESOLUTION_CLOSURE_CLOSED_AS_REVIEWED_REFERENCE",
        "FINAL_RESOLUTION_CLOSURE_REVIEW_RECEIPT_CONSUMED",
        "FINAL_RESOLUTION_REVIEW_CONFIRMED_CLEAN",
        "FINAL_RESOLUTION_RECORDS_FROZEN_AS_REFERENCE",
        "WEAK_FEEDBACK_RESOLVED_STATUS_FROZEN_AS_REFERENCE",
        "FINAL_RESOLUTION_BOUNDARY_CROSSING_FROZEN_AS_REFERENCE",
        "PARKING_FROZEN_AS_NON_RESOLUTION",
        "C5_BLOCK_FROZEN_PENDING_C5_DECISION",
        "POST_FINAL_RESOLUTION_REFERENCE_DECISION_READY",
        "NO_C5_RECONSIDERATION_READY",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if close_pass else failures

    closure_record = {
        "schema_version": "o2_final_resolution_closure_reference_closure_record_v0",
        "closure_status": "CLOSED_AS_REVIEWED_REFERENCE_C5_DECISION_READY" if close_pass else "REFERENCE_CLOSURE_NOT_RECORDED",
        "source_final_resolution_closure_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "closed_object": "o2_weak_feedback_final_resolution_closure_v0",
        "closure_meaning": "Final weak-feedback resolution closure output is frozen as a reviewed reference.",
        "closure_does_not_mean": [
            "C5 reconsideration ready",
            "C5 opened",
            "live feedback audit executed",
            "runtime patched",
            "source mutated",
            "architecture changed",
        ],
    }

    reviewed_reference = {
        "schema_version": "o2_final_resolution_closure_reviewed_reference_v0",
        "reference_status": "FROZEN_FINAL_RESOLUTION_CLOSURE_REVIEWED_REFERENCE" if close_pass else "REFERENCE_NOT_FROZEN",
        "reference_object_id": "o2_final_resolution_closure_reviewed_reference_" + sha8({
            "review_receipt": SOURCE_REVIEW_RECEIPT_ID,
            "final_resolution_count": len(final_resolution),
            "weak_feedback_resolved": True,
        }),
        "source_final_resolution_closure_receipt_id": "283a503b",
        "source_final_resolution_closure_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "final_question_answer_closure_records_count": len(final_qa),
        "final_source_ref_closure_records_count": len(final_source),
        "final_under_typed_acceptance_closure_records_count": len(final_undertyped),
        "final_parking_closure_records_count": len(final_parking),
        "final_resolution_records_count": len(final_resolution),
        "final_route_closure_records_count": len(final_routes),
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "parking_counted_as_resolution": False,
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "post_reference_closure_decision_ready": close_pass,
    }

    reference_index = {
        "schema_version": "o2_final_resolution_closure_reference_index_v0",
        "index_status": "REFERENCE_INDEX_EMITTED" if close_pass else "REFERENCE_INDEX_NOT_EMITTED",
        "reference_paths": {
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "closure_record": rel(CLOSURE_RECORD_PATH),
            "final_resolution_records_reference": rel(FINAL_RESOLUTION_RECORDS_REFERENCE_PATH),
            "resolved_status_reference": rel(RESOLVED_STATUS_REFERENCE_PATH),
            "final_boundary_reference": rel(FINAL_BOUNDARY_REFERENCE_PATH),
            "c5_block_reference": rel(C5_BLOCK_REFERENCE_PATH),
        },
    }

    final_resolution_reference = {
        "schema_version": "o2_final_weak_feedback_resolution_records_reference_v0",
        "reference_status": "FINAL_RESOLUTION_RECORDS_FROZEN_AS_REFERENCE",
        "final_resolution_records_count": len(final_resolution),
        "all_final_resolution_records_closed": len(final_resolution) == 3 and all(x.get("closure_status") == "FINAL_RESOLUTION_CLOSED" for x in final_resolution),
        "all_weak_feedback_resolved": all(x.get("weak_feedback_resolved") is True for x in final_resolution),
        "all_c5_not_ready_not_open": all(x.get("c5_reconsideration_ready") is False and x.get("c5_opened") is False for x in final_resolution),
    }

    resolved_status_reference = {
        "schema_version": "o2_weak_feedback_resolved_status_reference_v0",
        "reference_status": "WEAK_FEEDBACK_RESOLVED_STATUS_FROZEN_AS_REFERENCE",
        "weak_feedback_resolved": True,
        "resolution_records_emitted_count": len(final_resolution),
        "final_resolution_boundary_crossed": True,
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    final_boundary_reference = {
        "schema_version": "o2_final_resolution_boundary_crossing_reference_v0",
        "reference_status": "FINAL_RESOLUTION_BOUNDARY_CROSSING_FROZEN_AS_REFERENCE",
        "final_resolution_boundary_crossed": True,
        "weak_feedback_resolved": True,
        "resolution_records_emitted_count": len(final_resolution),
        "parking_counted_as_resolution": False,
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    c5_block_reference = {
        "schema_version": "o2_c5_block_pending_decision_reference_v0",
        "reference_status": "C5_BLOCK_FROZEN_PENDING_EXPLICIT_DECISION",
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "post_final_resolution_reference_decision_required": True,
    }

    post_closure_decision_readiness = {
        "schema_version": "o2_post_final_resolution_closure_reference_decision_readiness_v0",
        "decision_ready": close_pass,
        "recommended_next": recommended_next,
        "eligible_decision_scope": "decide next after final-resolution closure reference closure",
        "allowed_next_question": "whether C5 reconsideration may be selected after reviewed final-resolution closure reference exists",
        "not_authorized_here": [
            "set C5 reconsideration ready",
            "open C5",
            "run live feedback audit",
            "patch runtime",
            "mutate source",
        ],
    }

    authority_boundary = {
        "schema_version": "o2_final_resolution_closure_reference_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_final_resolution_closure_reference_closure": close_pass,
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
        "schema_version": "o2_final_resolution_closure_reference_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "final_resolution_closure_closed_as_reviewed_reference": close_pass,
        "reviewed_reference_emitted": close_pass,
        "post_final_resolution_reference_decision_ready": close_pass,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": len(final_resolution),
        "resolution_records_emitted_count": len(final_resolution),
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
        "schema_version": "o2_final_resolution_closure_reference_closure_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "reference_closure_count": 1 if close_pass else 0,
        "reviewed_reference_emitted_count": 1 if close_pass else 0,
        "post_final_resolution_reference_decision_ready_count": 1 if close_pass else 0,
        "final_resolution_records_frozen_count": len(final_resolution),
        "resolution_records_emitted_count": len(final_resolution),
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
        "schema_version": "o2_final_resolution_closure_reference_closure_profile_v0",
        "profile_id": "o2_final_resolution_closure_reference_closure_profile_" + sha8(rollup),
        "status": status,
        "final_resolution_closure_closed_as_reviewed_reference": close_pass,
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "final_resolution_records_frozen_count": len(final_resolution),
        "resolution_records_emitted_count": len(final_resolution),
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": False,
        "post_final_resolution_reference_decision_ready": close_pass,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Decide next after final-resolution closure reference closure. C5 remains separate until explicitly selected.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_final_resolution_closure_reference_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Final weak-feedback resolution closure is closed as a reviewed reference. Weak feedback remains resolved and C5 remains blocked pending a later explicit decision.",
        "resolution_records_emitted_count": len(final_resolution),
        "weak_feedback_resolved": True,
        "final_resolution_boundary_crossed": True,
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_final_resolution_closure_reference_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_final_resolution_closure_review",
                "question": "is final-resolution closure reviewed clean",
                "answer": "yes" if close_pass else "no",
                "taken": "freeze final-resolution closure reference",
            },
            {
                "step": "preserve_resolved_state",
                "question": "is weak feedback resolved by final records",
                "answer": "yes",
                "taken": "freeze resolved state as reference",
            },
            {
                "step": "preserve_c5_decision_gate",
                "question": "does reference closure open C5",
                "answer": "no",
                "taken": "emit post-reference decision readiness",
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
        (FINAL_RESOLUTION_RECORDS_REFERENCE_PATH, final_resolution_reference),
        (RESOLVED_STATUS_REFERENCE_PATH, resolved_status_reference),
        (FINAL_BOUNDARY_REFERENCE_PATH, final_boundary_reference),
        (C5_BLOCK_REFERENCE_PATH, c5_block_reference),
        (POST_CLOSURE_DECISION_READINESS_PATH, post_closure_decision_readiness),
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
        "FINAL_REFERENCE_CLOSURE_0_REVIEW_RECEIPT_CONSUMED": SOURCE_REVIEW_RECEIPT_PATH.exists(),
        "FINAL_REFERENCE_CLOSURE_1_CLOSURE_RECORD_EMITTED": CLOSURE_RECORD_PATH.exists(),
        "FINAL_REFERENCE_CLOSURE_2_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists(),
        "FINAL_REFERENCE_CLOSURE_3_REFERENCE_INDEX_EMITTED": REFERENCE_INDEX_PATH.exists(),
        "FINAL_REFERENCE_CLOSURE_4_FINAL_RESOLUTION_RECORDS_FROZEN": final_resolution_reference["final_resolution_records_count"] == 3 and final_resolution_reference["all_final_resolution_records_closed"] is True,
        "FINAL_REFERENCE_CLOSURE_5_RESOLVED_STATUS_FROZEN": resolved_status_reference["weak_feedback_resolved"] is True,
        "FINAL_REFERENCE_CLOSURE_6_FINAL_BOUNDARY_FROZEN": final_boundary_reference["final_resolution_boundary_crossed"] is True,
        "FINAL_REFERENCE_CLOSURE_7_PARKING_NOT_RESOLUTION": final_boundary_reference["parking_counted_as_resolution"] is False,
        "FINAL_REFERENCE_CLOSURE_8_C5_BLOCK_FROZEN": c5_block_reference["c5_opened"] is False and c5_block_reference["c5_reconsideration_ready"] is False,
        "FINAL_REFERENCE_CLOSURE_9_POST_REFERENCE_DECISION_READY": post_closure_decision_readiness["decision_ready"] is True,
        "FINAL_REFERENCE_CLOSURE_10_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "FINAL_REFERENCE_CLOSURE_11_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "FINAL_REFERENCE_CLOSURE_12_NO_C5_OPEN": rollup["c5_opened_count"] == 0 and rollup["c5_reconsideration_ready_count"] == 0,
        "FINAL_REFERENCE_CLOSURE_13_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "FINAL_REFERENCE_CLOSURE_14_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "FINAL_REFERENCE_CLOSURE_15_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REFERENCE_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "weak_feedback_resolved": True,
        "resolution_records": len(final_resolution),
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_final_resolution_closure_reference_closure_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_REFERENCE_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_final_resolution_closure_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_final_resolution_closure_reference_closure_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "final_resolution_closure_closed_as_reviewed_reference": close_pass,
            "reviewed_reference_emitted": close_pass,
            "post_final_resolution_reference_decision_ready": close_pass,
            "weak_feedback_resolved": True,
            "final_resolution_boundary_crossed": True,
            "final_resolution_records_frozen_count": len(final_resolution),
            "resolution_records_emitted_count": len(final_resolution),
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
            "closure_record": rel(CLOSURE_RECORD_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "reference_index": rel(REFERENCE_INDEX_PATH),
            "final_resolution_records_reference": rel(FINAL_RESOLUTION_RECORDS_REFERENCE_PATH),
            "resolved_status_reference": rel(RESOLVED_STATUS_REFERENCE_PATH),
            "final_boundary_reference": rel(FINAL_BOUNDARY_REFERENCE_PATH),
            "c5_block_reference": rel(C5_BLOCK_REFERENCE_PATH),
            "post_closure_decision_readiness": rel(POST_CLOSURE_DECISION_READINESS_PATH),
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
    print(f"final_resolution_closure_reference_closure_receipt_id={receipt_id}")
    print(f"final_resolution_closure_reference_closure_receipt_path={rel(receipt_path)}")
    print(f"final_resolution_closure_reference_closure_record_path={rel(CLOSURE_RECORD_PATH)}")
    print(f"final_resolution_closure_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"weak_feedback_resolved_status_reference_path={rel(RESOLVED_STATUS_REFERENCE_PATH)}")
    print(f"c5_block_pending_decision_reference_path={rel(C5_BLOCK_REFERENCE_PATH)}")
    print(f"post_final_resolution_closure_reference_decision_readiness_path={rel(POST_CLOSURE_DECISION_READINESS_PATH)}")
    print(f"final_resolution_closure_reference_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"final_resolution_closure_reference_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
