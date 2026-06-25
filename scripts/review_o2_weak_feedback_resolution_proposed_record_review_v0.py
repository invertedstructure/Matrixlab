#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_proposed_record_review_review.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REVIEW"
MODE = "REVIEW / REVIEWED_ARTIFACT_INTEGRITY / NO_FINAL_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REVIEW_ONLY"

SOURCE_RECEIPT_ID = "6149c6d9"

SOURCE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0_receipts/6149c6d9.json"
EXECUTION_RECORD_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_execution_record_v0.json"
REVIEWED_QA_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_question_answer_records_v0.jsonl"
REVIEWED_SOURCE_REF_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_source_ref_satisfaction_records_v0.jsonl"
REVIEWED_UNDERTYPED_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_under_typed_acceptance_records_v0.jsonl"
REVIEWED_PARKING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_parking_continuation_records_v0.jsonl"
REVIEWED_RESOLUTION_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_weak_feedback_resolution_records_v0.jsonl"
REVIEWED_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_weak_feedback_resolution_route_map_v0.jsonl"
REVIEW_GATE_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_gate_readout_v0.json"
RESOLUTION_BOUNDARY_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_resolution_boundary_readout_v0.json"
C5_BLOCK_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_c5_block_readout_v0.json"
UNRESOLVED_CONTINUATION_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_unresolved_continuation_v0.json"
AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_classification_v0.json"
ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_rollup_v0.json"
PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_profile_v0.json"
REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_report.json"
TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_transition_trace.json"

POST_DECISION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0_receipts/63793a90.json"
POST_REVIEW_AUTH_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposed_record_review_authorization_v0.json"
PROPOSAL_EMISSION_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0_receipts/922ef93d.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_RECEIPT_PATH,
    EXECUTION_RECORD_PATH,
    REVIEWED_QA_RECORDS_PATH,
    REVIEWED_SOURCE_REF_RECORDS_PATH,
    REVIEWED_UNDERTYPED_RECORDS_PATH,
    REVIEWED_PARKING_RECORDS_PATH,
    REVIEWED_RESOLUTION_RECORDS_PATH,
    REVIEWED_ROUTE_MAP_PATH,
    REVIEW_GATE_READOUT_PATH,
    RESOLUTION_BOUNDARY_READOUT_PATH,
    C5_BLOCK_READOUT_PATH,
    UNRESOLVED_CONTINUATION_PATH,
    AUTHORITY_PATH,
    CLASSIFICATION_PATH,
    ROLLUP_PATH,
    PROFILE_PATH,
    REPORT_PATH,
    TRACE_PATH,
    POST_DECISION_RECEIPT_PATH,
    POST_REVIEW_AUTH_PATH,
    PROPOSAL_EMISSION_CLOSURE_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "o2_proposed_record_review_review_assessment_v0.json"
REVIEWED_ARTIFACT_INVENTORY_REVIEW_PATH = OUT_DIR / "o2_reviewed_artifact_inventory_review_v0.json"
REVIEWED_QA_REVIEW_PATH = OUT_DIR / "o2_reviewed_question_answer_record_review_v0.json"
REVIEWED_SOURCE_REF_REVIEW_PATH = OUT_DIR / "o2_reviewed_source_ref_satisfaction_record_review_v0.json"
REVIEWED_UNDERTYPED_REVIEW_PATH = OUT_DIR / "o2_reviewed_under_typed_acceptance_record_review_v0.json"
REVIEWED_PARKING_REVIEW_PATH = OUT_DIR / "o2_reviewed_parking_continuation_record_review_v0.json"
REVIEWED_RESOLUTION_REVIEW_PATH = OUT_DIR / "o2_reviewed_weak_feedback_resolution_record_review_v0.json"
REVIEWED_ROUTE_REVIEW_PATH = OUT_DIR / "o2_reviewed_route_map_review_v0.json"
FINAL_RESOLUTION_BOUNDARY_REVIEW_PATH = OUT_DIR / "o2_final_resolution_boundary_review_v0.json"
C5_BLOCK_REVIEW_PATH = OUT_DIR / "o2_proposed_record_review_c5_block_review_v0.json"
UNRESOLVED_CONTINUATION_REVIEW_PATH = OUT_DIR / "o2_proposed_record_review_unresolved_continuation_review_v0.json"
CLOSURE_CANDIDATE_PATH = OUT_DIR / "o2_proposed_record_review_closure_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_proposed_record_review_review_authority_boundary_v0.json"
CLASSIFICATION_OUT_PATH = OUT_DIR / "o2_proposed_record_review_review_classification_v0.json"
ROLLUP_OUT_PATH = OUT_DIR / "o2_proposed_record_review_review_rollup_v0.json"
PROFILE_OUT_PATH = OUT_DIR / "o2_proposed_record_review_review_profile_v0.json"
REPORT_OUT_PATH = OUT_DIR / "o2_proposed_record_review_review_report.json"
TRACE_OUT_PATH = OUT_DIR / "o2_proposed_record_review_review_transition_trace.json"

EXPECTED_SOURCE_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_EXECUTED_REVIEWED_ARTIFACTS_CLOSE_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_EXECUTED_REVIEWED_ARTIFACTS_CLOSE_READY"
EXPECTED_SOURCE_NEXT = "REVIEW_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_V0"
RECOMMENDED_NEXT = "CLOSE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_AS_REVIEWED_REFERENCE_V0"

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

    receipt = read_json(SOURCE_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_resolution_proposed_record_review_summary", {})
    execution_record = read_json(EXECUTION_RECORD_PATH)
    qa = read_jsonl(REVIEWED_QA_RECORDS_PATH)
    source = read_jsonl(REVIEWED_SOURCE_REF_RECORDS_PATH)
    undertyped = read_jsonl(REVIEWED_UNDERTYPED_RECORDS_PATH)
    parking = read_jsonl(REVIEWED_PARKING_RECORDS_PATH)
    resolution = read_jsonl(REVIEWED_RESOLUTION_RECORDS_PATH)
    routes = read_jsonl(REVIEWED_ROUTE_MAP_PATH)
    gate_readout = read_json(REVIEW_GATE_READOUT_PATH)
    boundary_readout = read_json(RESOLUTION_BOUNDARY_READOUT_PATH)
    c5_readout = read_json(C5_BLOCK_READOUT_PATH)
    unresolved = read_json(UNRESOLVED_CONTINUATION_PATH)
    authority = read_json(AUTHORITY_PATH)
    classification = read_json(CLASSIFICATION_PATH)
    rollup = read_json(ROLLUP_PATH)
    profile = read_json(PROFILE_PATH)
    report = read_json(REPORT_PATH)
    trace = read_json(TRACE_PATH)

    post_receipt = read_json(POST_DECISION_RECEIPT_PATH)
    post_auth = read_json(POST_REVIEW_AUTH_PATH)
    closure_receipt = read_json(PROPOSAL_EMISSION_CLOSURE_RECEIPT_PATH)

    if receipt.get("receipt_id") != SOURCE_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_proposed_record_review_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_hidden_next_command")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "proposed_record_review_executed",
        "reviewed_artifacts_emitted",
        "review_ready",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "reviewed_question_answer_records_emitted_count": 3,
        "reviewed_source_ref_satisfaction_records_emitted_count": 2,
        "reviewed_under_typed_acceptance_records_emitted_count": 2,
        "reviewed_parking_continuation_records_emitted_count": 3,
        "reviewed_resolution_records_emitted_count": 3,
        "reviewed_route_records_emitted_count": 3,
        "resolution_records_emitted_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    for key in [
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
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
    if execution_record.get("review_execution_status") != "REVIEWED_ARTIFACTS_EMITTED_CLOSE_READY":
        failures.append("execution_record_status_wrong")
    if len(qa) != 3 or len(source) != 2 or len(undertyped) != 2 or len(parking) != 3 or len(resolution) != 3 or len(routes) != 3:
        failures.append("reviewed_artifact_counts_wrong")

    for row in qa:
        if row.get("review_status") != "REVIEWED_ACCEPTED" or row.get("counts_as_answer") is not True or row.get("counts_as_resolution_input") is not True:
            failures.append(f"qa_review_bad:{row.get('reviewed_answer_id')}")
        if row.get("weak_feedback_resolved_by_this_record") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"qa_boundary_bad:{row.get('reviewed_answer_id')}")
    for row in source:
        if row.get("review_status") != "REVIEWED_ACCEPTED" or row.get("counts_as_satisfied") is not True or row.get("counts_as_resolution_input") is not True:
            failures.append(f"source_review_bad:{row.get('reviewed_satisfaction_id')}")
        if row.get("weak_feedback_resolved_by_this_record") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"source_boundary_bad:{row.get('reviewed_satisfaction_id')}")
    for row in undertyped:
        if row.get("review_status") != "REVIEWED_ACCEPTED" or row.get("counts_as_approved") is not True:
            failures.append(f"undertyped_review_bad:{row.get('reviewed_under_typed_acceptance_id')}")
        if row.get("weak_feedback_resolved_by_this_record") is not False or row.get("c5_unblock_allowed") is not False:
            failures.append(f"undertyped_boundary_bad:{row.get('reviewed_under_typed_acceptance_id')}")
    for row in parking:
        if row.get("review_status") != "REVIEWED_PARKING_CONTINUES" or row.get("counts_as_resolution") is not False:
            failures.append(f"parking_review_bad:{row.get('reviewed_parking_continuation_id')}")
        if row.get("weak_feedback_resolved_by_this_record") is not False or row.get("c5_unblock_allowed") is not False:
            failures.append(f"parking_boundary_bad:{row.get('reviewed_parking_continuation_id')}")
    for row in resolution:
        if row.get("review_status") != "REVIEWED_ACCEPTED" or row.get("counts_as_reviewed_resolution") is not True:
            failures.append(f"resolution_review_bad:{row.get('reviewed_resolution_id')}")
        if row.get("counts_as_final_resolution") is not False or row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"resolution_boundary_bad:{row.get('reviewed_resolution_id')}")
        if row.get("requires_resolution_closure_before_resolved") is not True:
            failures.append(f"resolution_closure_gate_missing:{row.get('reviewed_resolution_id')}")
    for row in routes:
        if row.get("reviewed_record_emitted") is not True or row.get("current_resolution_state") != "REVIEWED_NOT_CLOSED":
            failures.append(f"route_review_bad:{row.get('reviewed_route_record_id')}")
        if row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"route_boundary_bad:{row.get('reviewed_route_record_id')}")

    if gate_readout.get("reviewed_resolution_records_emitted_count") != 3 or gate_readout.get("resolution_records_emitted_count") != 0:
        failures.append("gate_readout_counts_wrong")
    if boundary_readout.get("reviewed_resolution_records_exist") is not True or boundary_readout.get("reviewed_artifacts_crossed_into_final_resolution") is not False:
        failures.append("boundary_readout_wrong")
    if c5_readout.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_readout.get("c5_opened") is not False:
        failures.append("c5_readout_wrong")
    if unresolved.get("weak_feedback_resolved") is not False or unresolved.get("reviewed_resolution_records_exist") is not True:
        failures.append("unresolved_wrong")
    if authority.get("may_review_proposed_record_review_next") is not True:
        failures.append("authority_no_review_next")
    if authority.get("may_close_reviewed_resolution_now") is not False or authority.get("may_open_c5") is not False:
        failures.append("authority_allows_close_or_c5")
    if classification.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append("classification_next_wrong")
    if rollup.get("reviewed_resolution_records_emitted_count") != 3 or rollup.get("weak_feedback_resolved_count") != 0:
        failures.append("rollup_wrong")
    if profile.get("reviewed_artifacts_emitted") is not True or profile.get("next_command_goal") is not None:
        failures.append("profile_wrong")
    if report.get("recommended_next_handling") != EXPECTED_SOURCE_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("trace_stop_wrong")
    if post_receipt.get("receipt_id") != "63793a90":
        failures.append("post_decision_receipt_wrong")
    if post_auth.get("authorized_next_unit") != "EXECUTE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_V0":
        failures.append("post_auth_wrong")
    if closure_receipt.get("receipt_id") != "922ef93d":
        failures.append("closure_receipt_wrong")

    return failures, {
        "qa": qa,
        "source": source,
        "undertyped": undertyped,
        "parking": parking,
        "resolution": resolution,
        "routes": routes,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    qa = src.get("qa", [])
    source = src.get("source", [])
    undertyped = src.get("undertyped", [])
    parking = src.get("parking", [])
    resolution = src.get("resolution", [])
    routes = src.get("routes", [])

    review_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REVIEWED_ARTIFACTS_CLEAN_CLOSE_READY" if review_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REVIEW_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REVIEW_COMPLETE",
        "WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REVIEW_PASS",
        "PROPOSED_RECORD_REVIEW_RECEIPT_CONSUMED",
        "REVIEWED_ARTIFACT_INVENTORY_REVIEWED",
        "REVIEWED_QUESTION_ANSWER_RECORDS_CONFIRMED",
        "REVIEWED_SOURCE_REF_SATISFACTION_RECORDS_CONFIRMED",
        "REVIEWED_UNDER_TYPED_ACCEPTANCE_RECORDS_CONFIRMED",
        "REVIEWED_PARKING_CONTINUATION_RECORDS_CONFIRMED_UNRESOLVED",
        "REVIEWED_WEAK_FEEDBACK_RESOLUTION_RECORDS_CONFIRMED_NOT_FINAL",
        "REVIEWED_ROUTE_MAP_CONFIRMED_REVIEWED_NOT_CLOSED",
        "FINAL_RESOLUTION_BOUNDARY_REVIEWED_NOT_CROSSED",
        "C5_BLOCK_REVIEWED_ENFORCED",
        "CLOSURE_CANDIDATE_READY",
        "NO_FINAL_WEAK_FEEDBACK_RESOLUTION_RECORDED",
        "NO_C5_RECONSIDERATION_READY",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if review_pass else failures

    review_assessment = {
        "schema_version": "o2_proposed_record_review_review_assessment_v0",
        "review_status": status,
        "review_complete": review_pass,
        "review_pass": review_pass,
        "source_proposed_record_review_receipt_id": SOURCE_RECEIPT_ID,
        "reviewed_artifacts_integrity_pass": review_pass,
        "closure_candidate_ready": review_pass,
        "recommended_next": recommended_next,
    }

    inventory_review = {
        "schema_version": "o2_reviewed_artifact_inventory_review_v0",
        "review_status": "REVIEWED_ARTIFACT_INVENTORY_REVIEW_PASS" if review_pass else "REVIEWED_ARTIFACT_INVENTORY_REVIEW_FAIL",
        "reviewed_question_answer_records_count": len(qa),
        "reviewed_source_ref_satisfaction_records_count": len(source),
        "reviewed_under_typed_acceptance_records_count": len(undertyped),
        "reviewed_parking_continuation_records_count": len(parking),
        "reviewed_weak_feedback_resolution_records_count": len(resolution),
        "reviewed_route_records_count": len(routes),
        "reviewed_artifacts_exist": True,
    }

    qa_review = {
        "schema_version": "o2_reviewed_question_answer_record_review_v0",
        "review_status": "REVIEWED_QA_RECORD_REVIEW_PASS" if review_pass else "REVIEWED_QA_RECORD_REVIEW_FAIL",
        "reviewed_question_answer_records_reviewed_count": len(qa),
        "all_count_as_answer": all(x.get("counts_as_answer") is True for x in qa),
        "weak_feedback_resolved_by_records": False,
        "c5_reconsideration_ready": False,
    }

    source_review = {
        "schema_version": "o2_reviewed_source_ref_satisfaction_record_review_v0",
        "review_status": "REVIEWED_SOURCE_REF_RECORD_REVIEW_PASS" if review_pass else "REVIEWED_SOURCE_REF_RECORD_REVIEW_FAIL",
        "reviewed_source_ref_satisfaction_records_reviewed_count": len(source),
        "all_count_as_satisfied": all(x.get("counts_as_satisfied") is True for x in source),
        "weak_feedback_resolved_by_records": False,
        "c5_reconsideration_ready": False,
    }

    undertyped_review = {
        "schema_version": "o2_reviewed_under_typed_acceptance_record_review_v0",
        "review_status": "REVIEWED_UNDER_TYPED_ACCEPTANCE_REVIEW_PASS" if review_pass else "REVIEWED_UNDER_TYPED_ACCEPTANCE_REVIEW_FAIL",
        "reviewed_under_typed_acceptance_records_reviewed_count": len(undertyped),
        "all_count_as_approved": all(x.get("counts_as_approved") is True for x in undertyped),
        "weak_feedback_resolved_by_records": False,
        "c5_unblock_allowed": False,
    }

    parking_review = {
        "schema_version": "o2_reviewed_parking_continuation_record_review_v0",
        "review_status": "REVIEWED_PARKING_CONTINUATION_REVIEW_PASS" if review_pass else "REVIEWED_PARKING_CONTINUATION_REVIEW_FAIL",
        "reviewed_parking_continuation_records_reviewed_count": len(parking),
        "all_parking_continues": all(x.get("review_status") == "REVIEWED_PARKING_CONTINUES" for x in parking),
        "parking_counted_as_resolution": False,
        "weak_feedback_resolved_by_records": False,
        "c5_unblock_allowed": False,
    }

    resolution_review = {
        "schema_version": "o2_reviewed_weak_feedback_resolution_record_review_v0",
        "review_status": "REVIEWED_RESOLUTION_RECORD_REVIEW_PASS" if review_pass else "REVIEWED_RESOLUTION_RECORD_REVIEW_FAIL",
        "reviewed_resolution_records_reviewed_count": len(resolution),
        "reviewed_resolution_records_exist": True,
        "all_count_as_reviewed_resolution": all(x.get("counts_as_reviewed_resolution") is True for x in resolution),
        "all_require_resolution_closure_before_resolved": all(x.get("requires_resolution_closure_before_resolved") is True for x in resolution),
        "final_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_reconsideration_ready": False,
    }

    route_review = {
        "schema_version": "o2_reviewed_route_map_review_v0",
        "review_status": "REVIEWED_ROUTE_MAP_REVIEW_PASS" if review_pass else "REVIEWED_ROUTE_MAP_REVIEW_FAIL",
        "reviewed_route_records_reviewed_count": len(routes),
        "all_reviewed_record_emitted": all(x.get("reviewed_record_emitted") is True for x in routes),
        "all_reviewed_not_closed": all(x.get("current_resolution_state") == "REVIEWED_NOT_CLOSED" for x in routes),
        "weak_feedback_resolved": False,
        "c5_reconsideration_ready": False,
    }

    final_boundary_review = {
        "schema_version": "o2_final_resolution_boundary_review_v0",
        "review_status": "FINAL_RESOLUTION_BOUNDARY_REVIEW_PASS" if review_pass else "FINAL_RESOLUTION_BOUNDARY_REVIEW_FAIL",
        "reviewed_artifacts_exist": True,
        "reviewed_resolution_records_exist": True,
        "final_resolution_boundary_crossed": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": len(resolution),
        "requires_closure_before_resolution": True,
    }

    c5_review = {
        "schema_version": "o2_proposed_record_review_c5_block_review_v0",
        "review_status": "C5_BLOCK_REVIEW_PASS" if review_pass else "C5_BLOCK_REVIEW_FAIL",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "block_enforced": True,
        "reason": "Reviewed artifacts exist but final weak-feedback resolution has not been closed.",
    }

    unresolved_review = {
        "schema_version": "o2_proposed_record_review_unresolved_continuation_review_v0",
        "review_status": "UNRESOLVED_CONTINUATION_REVIEW_PASS" if review_pass else "UNRESOLVED_CONTINUATION_REVIEW_FAIL",
        "reviewed_resolution_records_exist": True,
        "weak_feedback_resolved": False,
        "final_resolution_boundary_crossed": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": len(resolution),
        "parking_counted_as_resolution": False,
    }

    closure_candidate = {
        "schema_version": "o2_proposed_record_review_closure_candidate_v0",
        "closure_candidate_status": "PROPOSED_RECORD_REVIEW_CLOSE_READY_REVIEWED_ARTIFACTS_NOT_FINAL" if review_pass else "PROPOSED_RECORD_REVIEW_CLOSE_NOT_READY",
        "review_pass": review_pass,
        "closure_meaning": "Close proposed-record review output as reviewed reference while preserving that final weak-feedback resolution has not been closed.",
        "closure_does_not_mean": [
            "weak feedback finally resolved",
            "C5 reconsideration ready",
            "C5 opened",
            "live feedback audit executed",
            "runtime patched",
            "sources mutated",
        ],
        "recommended_next": recommended_next,
    }

    authority_boundary = {
        "schema_version": "o2_proposed_record_review_review_authority_boundary_v0",
        "status": status,
        "may_close_proposed_record_review_as_reviewed_reference_next": review_pass,
        "may_close_final_weak_feedback_resolution_now": False,
        "may_resolve_weak_feedback_now": False,
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
        "schema_version": "o2_proposed_record_review_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "proposed_record_review_review_complete": review_pass,
        "proposed_record_review_review_pass": review_pass,
        "reviewed_artifacts_integrity_pass": review_pass,
        "closure_candidate_ready": review_pass,
        "reviewed_question_answer_records_reviewed_count": len(qa),
        "reviewed_source_ref_satisfaction_records_reviewed_count": len(source),
        "reviewed_under_typed_acceptance_records_reviewed_count": len(undertyped),
        "reviewed_parking_continuation_records_reviewed_count": len(parking),
        "reviewed_resolution_records_reviewed_count": len(resolution),
        "reviewed_route_records_reviewed_count": len(routes),
        "reviewed_resolution_records_exist": True,
        "final_resolution_boundary_crossed": False,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
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
        "schema_version": "o2_proposed_record_review_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "closure_candidate_ready_count": 1 if review_pass else 0,
        "reviewed_artifacts_integrity_pass_count": 1 if review_pass else 0,
        "reviewed_question_answer_records_reviewed_count": len(qa),
        "reviewed_source_ref_satisfaction_records_reviewed_count": len(source),
        "reviewed_under_typed_acceptance_records_reviewed_count": len(undertyped),
        "reviewed_parking_continuation_records_reviewed_count": len(parking),
        "reviewed_resolution_records_reviewed_count": len(resolution),
        "reviewed_route_records_reviewed_count": len(routes),
        "reviewed_resolution_records_exist_count": 1,
        "weak_feedback_resolved_count": 0,
        "resolution_records_emitted_count": 0,
        "final_resolution_boundary_crossed_count": 0,
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
        "final_resolution_boundary_crossed_count",
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
        "schema_version": "o2_proposed_record_review_review_profile_v0",
        "profile_id": "o2_proposed_record_review_review_profile_" + sha8(rollup),
        "status": status,
        "proposed_record_review_review_pass": review_pass,
        "reviewed_artifacts_integrity_pass": review_pass,
        "reviewed_resolution_records_exist": True,
        "closure_candidate_ready": review_pass,
        "reviewed_resolution_records_reviewed_count": len(resolution),
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "final_resolution_boundary_crossed": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Close proposed-record review as reviewed reference. Do not treat reviewed artifacts as final resolution.",
        "must_not_infer": [
            "weak feedback finally resolved",
            "C5 reconsideration ready",
            "C5 opened",
            "live feedback audit executed",
            "runtime patched",
            "source mutated",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_proposed_record_review_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Proposed-record review output was reviewed clean. Reviewed artifacts and reviewed weak-feedback resolution records exist, but final weak-feedback resolution is not closed and C5 remains blocked.",
        "reviewed_resolution_records_reviewed_count": len(resolution),
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "final_resolution_boundary_crossed": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_proposed_record_review_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_proposed_record_review_output",
                "question": "did proposed-record review emit reviewed artifacts",
                "answer": "yes" if review_pass else "no",
                "taken": "review artifact inventory",
            },
            {
                "step": "verify_reviewed_artifact_integrity",
                "question": "are reviewed artifacts structurally clean",
                "answer": "yes" if review_pass else "no",
                "taken": "confirm reviewed resolution records exist",
            },
            {
                "step": "verify_final_resolution_and_c5_boundaries",
                "question": "did this review finalize weak feedback or open C5",
                "answer": "no",
                "taken": "emit closure-ready reviewed reference candidate",
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
        (REVIEWED_ARTIFACT_INVENTORY_REVIEW_PATH, inventory_review),
        (REVIEWED_QA_REVIEW_PATH, qa_review),
        (REVIEWED_SOURCE_REF_REVIEW_PATH, source_review),
        (REVIEWED_UNDERTYPED_REVIEW_PATH, undertyped_review),
        (REVIEWED_PARKING_REVIEW_PATH, parking_review),
        (REVIEWED_RESOLUTION_REVIEW_PATH, resolution_review),
        (REVIEWED_ROUTE_REVIEW_PATH, route_review),
        (FINAL_RESOLUTION_BOUNDARY_REVIEW_PATH, final_boundary_review),
        (C5_BLOCK_REVIEW_PATH, c5_review),
        (UNRESOLVED_CONTINUATION_REVIEW_PATH, unresolved_review),
        (CLOSURE_CANDIDATE_PATH, closure_candidate),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_OUT_PATH, classification),
        (ROLLUP_OUT_PATH, rollup),
        (PROFILE_OUT_PATH, profile),
        (REPORT_OUT_PATH, report),
        (TRACE_OUT_PATH, trace),
    ]
    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "PROPOSED_RECORD_REVIEW_REVIEW_0_SOURCE_RECEIPT_CONSUMED": SOURCE_RECEIPT_PATH.exists(),
        "PROPOSED_RECORD_REVIEW_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "PROPOSED_RECORD_REVIEW_REVIEW_2_INVENTORY_REVIEW_EMITTED": REVIEWED_ARTIFACT_INVENTORY_REVIEW_PATH.exists(),
        "PROPOSED_RECORD_REVIEW_REVIEW_3_REVIEWED_QA_CONFIRMED": len(qa) == 3 and qa_review["all_count_as_answer"] is True,
        "PROPOSED_RECORD_REVIEW_REVIEW_4_REVIEWED_SOURCE_REF_CONFIRMED": len(source) == 2 and source_review["all_count_as_satisfied"] is True,
        "PROPOSED_RECORD_REVIEW_REVIEW_5_REVIEWED_UNDERTYPED_CONFIRMED": len(undertyped) == 2 and undertyped_review["all_count_as_approved"] is True,
        "PROPOSED_RECORD_REVIEW_REVIEW_6_REVIEWED_PARKING_CONFIRMED_UNRESOLVED": len(parking) == 3 and parking_review["parking_counted_as_resolution"] is False,
        "PROPOSED_RECORD_REVIEW_REVIEW_7_REVIEWED_RESOLUTION_CONFIRMED_NOT_FINAL": len(resolution) == 3 and resolution_review["all_count_as_reviewed_resolution"] is True and resolution_review["weak_feedback_resolved"] is False,
        "PROPOSED_RECORD_REVIEW_REVIEW_8_ROUTE_MAP_CONFIRMED_REVIEWED_NOT_CLOSED": len(routes) == 3 and route_review["all_reviewed_not_closed"] is True,
        "PROPOSED_RECORD_REVIEW_REVIEW_9_FINAL_RESOLUTION_BOUNDARY_NOT_CROSSED": final_boundary_review["final_resolution_boundary_crossed"] is False and final_boundary_review["weak_feedback_resolved"] is False,
        "PROPOSED_RECORD_REVIEW_REVIEW_10_C5_BLOCK_ENFORCED": c5_review["c5_opened"] is False and c5_review["c5_reconsideration_ready"] is False,
        "PROPOSED_RECORD_REVIEW_REVIEW_11_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "PROPOSED_RECORD_REVIEW_REVIEW_12_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "PROPOSED_RECORD_REVIEW_REVIEW_13_CLOSURE_CANDIDATE_READY": closure_candidate["closure_candidate_status"] == "PROPOSED_RECORD_REVIEW_CLOSE_READY_REVIEWED_ARTIFACTS_NOT_FINAL",
        "PROPOSED_RECORD_REVIEW_REVIEW_14_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "PROPOSED_RECORD_REVIEW_REVIEW_15_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "PROPOSED_RECORD_REVIEW_REVIEW_16_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_OUT_PATH.exists() and PROFILE_OUT_PATH.exists() and REPORT_OUT_PATH.exists() and TRACE_OUT_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "review_pass": review_pass,
        "reviewed_resolution_records": len(resolution),
        "final_resolution": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_resolution_proposed_record_review_review_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_proposed_record_review_receipt_id": SOURCE_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_resolution_proposed_record_review_review_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "proposed_record_review_review_complete": review_pass,
            "proposed_record_review_review_pass": review_pass,
            "reviewed_artifacts_integrity_pass": review_pass,
            "closure_candidate_ready": review_pass,
            "reviewed_question_answer_records_reviewed_count": len(qa),
            "reviewed_source_ref_satisfaction_records_reviewed_count": len(source),
            "reviewed_under_typed_acceptance_records_reviewed_count": len(undertyped),
            "reviewed_parking_continuation_records_reviewed_count": len(parking),
            "reviewed_resolution_records_reviewed_count": len(resolution),
            "reviewed_route_records_reviewed_count": len(routes),
            "reviewed_resolution_records_exist": True,
            "resolution_records_emitted_count": 0,
            "weak_feedback_resolved": False,
            "final_resolution_boundary_crossed": False,
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
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "reviewed_artifact_inventory_review": rel(REVIEWED_ARTIFACT_INVENTORY_REVIEW_PATH),
            "reviewed_question_answer_review": rel(REVIEWED_QA_REVIEW_PATH),
            "reviewed_source_ref_satisfaction_review": rel(REVIEWED_SOURCE_REF_REVIEW_PATH),
            "reviewed_under_typed_acceptance_review": rel(REVIEWED_UNDERTYPED_REVIEW_PATH),
            "reviewed_parking_continuation_review": rel(REVIEWED_PARKING_REVIEW_PATH),
            "reviewed_resolution_review": rel(REVIEWED_RESOLUTION_REVIEW_PATH),
            "reviewed_route_review": rel(REVIEWED_ROUTE_REVIEW_PATH),
            "final_resolution_boundary_review": rel(FINAL_RESOLUTION_BOUNDARY_REVIEW_PATH),
            "c5_block_review": rel(C5_BLOCK_REVIEW_PATH),
            "unresolved_continuation_review": rel(UNRESOLVED_CONTINUATION_REVIEW_PATH),
            "closure_candidate": rel(CLOSURE_CANDIDATE_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "classification": rel(CLASSIFICATION_OUT_PATH),
            "rollup": rel(ROLLUP_OUT_PATH),
            "profile": rel(PROFILE_OUT_PATH),
            "report": rel(REPORT_OUT_PATH),
            "transition_trace": rel(TRACE_OUT_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"proposed_record_review_review_receipt_id={receipt_id}")
    print(f"proposed_record_review_review_receipt_path={rel(receipt_path)}")
    print(f"proposed_record_review_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"reviewed_artifact_inventory_review_path={rel(REVIEWED_ARTIFACT_INVENTORY_REVIEW_PATH)}")
    print(f"reviewed_resolution_review_path={rel(REVIEWED_RESOLUTION_REVIEW_PATH)}")
    print(f"final_resolution_boundary_review_path={rel(FINAL_RESOLUTION_BOUNDARY_REVIEW_PATH)}")
    print(f"proposed_record_review_c5_block_review_path={rel(C5_BLOCK_REVIEW_PATH)}")
    print(f"proposed_record_review_review_rollup_path={rel(ROLLUP_OUT_PATH)}")
    print(f"proposed_record_review_review_profile_path={rel(PROFILE_OUT_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
