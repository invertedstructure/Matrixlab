#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_proposed_record_review_closure.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE"
MODE = "CLOSE / FREEZE_REVIEWED_ARTIFACT_REFERENCE / NO_FINAL_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_ONLY"

SOURCE_REVIEW_RECEIPT_ID = "98ec96a7"

SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0_receipts/98ec96a7.json"
SOURCE_REVIEW_ASSESSMENT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_proposed_record_review_review_assessment_v0.json"
REVIEWED_ARTIFACT_INVENTORY_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_reviewed_artifact_inventory_review_v0.json"
REVIEWED_QA_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_reviewed_question_answer_record_review_v0.json"
REVIEWED_SOURCE_REF_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_reviewed_source_ref_satisfaction_record_review_v0.json"
REVIEWED_UNDERTYPED_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_reviewed_under_typed_acceptance_record_review_v0.json"
REVIEWED_PARKING_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_reviewed_parking_continuation_record_review_v0.json"
REVIEWED_RESOLUTION_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_reviewed_weak_feedback_resolution_record_review_v0.json"
REVIEWED_ROUTE_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_reviewed_route_map_review_v0.json"
FINAL_RESOLUTION_BOUNDARY_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_final_resolution_boundary_review_v0.json"
C5_BLOCK_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_proposed_record_review_c5_block_review_v0.json"
UNRESOLVED_CONTINUATION_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_proposed_record_review_unresolved_continuation_review_v0.json"
CLOSURE_CANDIDATE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_proposed_record_review_closure_candidate_v0.json"
REVIEW_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_proposed_record_review_review_authority_boundary_v0.json"
REVIEW_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_proposed_record_review_review_classification_v0.json"
REVIEW_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_proposed_record_review_review_rollup_v0.json"
REVIEW_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_proposed_record_review_review_profile_v0.json"
REVIEW_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_proposed_record_review_review_report.json"
REVIEW_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0/o2_proposed_record_review_review_transition_trace.json"

EXEC_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0_receipts/6149c6d9.json"
EXECUTION_RECORD_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_execution_record_v0.json"
REVIEWED_QA_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_question_answer_records_v0.jsonl"
REVIEWED_SOURCE_REF_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_source_ref_satisfaction_records_v0.jsonl"
REVIEWED_UNDERTYPED_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_under_typed_acceptance_records_v0.jsonl"
REVIEWED_PARKING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_parking_continuation_records_v0.jsonl"
REVIEWED_RESOLUTION_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_weak_feedback_resolution_records_v0.jsonl"
REVIEWED_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_weak_feedback_resolution_route_map_v0.jsonl"
EXEC_BOUNDARY_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_resolution_boundary_readout_v0.json"
EXEC_C5_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_c5_block_readout_v0.json"
EXEC_UNRESOLVED_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_unresolved_continuation_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_REVIEW_RECEIPT_PATH,
    SOURCE_REVIEW_ASSESSMENT_PATH,
    REVIEWED_ARTIFACT_INVENTORY_REVIEW_PATH,
    REVIEWED_QA_REVIEW_PATH,
    REVIEWED_SOURCE_REF_REVIEW_PATH,
    REVIEWED_UNDERTYPED_REVIEW_PATH,
    REVIEWED_PARKING_REVIEW_PATH,
    REVIEWED_RESOLUTION_REVIEW_PATH,
    REVIEWED_ROUTE_REVIEW_PATH,
    FINAL_RESOLUTION_BOUNDARY_REVIEW_PATH,
    C5_BLOCK_REVIEW_PATH,
    UNRESOLVED_CONTINUATION_REVIEW_PATH,
    CLOSURE_CANDIDATE_PATH,
    REVIEW_AUTHORITY_PATH,
    REVIEW_CLASSIFICATION_PATH,
    REVIEW_ROLLUP_PATH,
    REVIEW_PROFILE_PATH,
    REVIEW_REPORT_PATH,
    REVIEW_TRACE_PATH,
    EXEC_RECEIPT_PATH,
    EXECUTION_RECORD_PATH,
    REVIEWED_QA_RECORDS_PATH,
    REVIEWED_SOURCE_REF_RECORDS_PATH,
    REVIEWED_UNDERTYPED_RECORDS_PATH,
    REVIEWED_PARKING_RECORDS_PATH,
    REVIEWED_RESOLUTION_RECORDS_PATH,
    REVIEWED_ROUTE_MAP_PATH,
    EXEC_BOUNDARY_READOUT_PATH,
    EXEC_C5_READOUT_PATH,
    EXEC_UNRESOLVED_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0_receipts"

CLOSURE_RECORD_PATH = OUT_DIR / "o2_proposed_record_review_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "o2_proposed_record_review_reviewed_reference_v0.json"
REVIEWED_ARTIFACT_FREEZE_PATH = OUT_DIR / "o2_reviewed_artifact_inventory_freeze_v0.json"
REVIEWED_RESOLUTION_FREEZE_PATH = OUT_DIR / "o2_reviewed_weak_feedback_resolution_record_freeze_v0.json"
REVIEWED_ROUTE_FREEZE_PATH = OUT_DIR / "o2_reviewed_route_map_freeze_v0.json"
FINAL_RESOLUTION_BOUNDARY_LOCK_PATH = OUT_DIR / "o2_final_resolution_boundary_lock_v0.json"
UNRESOLVED_STATUS_FREEZE_PATH = OUT_DIR / "o2_proposed_record_review_unresolved_status_freeze_v0.json"
C5_BLOCK_FREEZE_PATH = OUT_DIR / "o2_proposed_record_review_c5_block_freeze_v0.json"
RECEIPT_CHAIN_PATH = OUT_DIR / "o2_proposed_record_review_receipt_chain_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o2_proposed_record_review_closure_downstream_decision_table_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_proposed_record_review_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_proposed_record_review_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_proposed_record_review_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_proposed_record_review_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_proposed_record_review_closure_report.json"
TRACE_PATH = OUT_DIR / "o2_proposed_record_review_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REVIEWED_ARTIFACTS_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REVIEWED_ARTIFACTS_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_AS_REVIEWED_REFERENCE_V0"
RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REFERENCE_CLOSURE_V0"

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

    review_receipt = read_json(SOURCE_REVIEW_RECEIPT_PATH)
    summary = review_receipt.get("machine_readable_o2_weak_feedback_resolution_proposed_record_review_review_summary", {})
    assessment = read_json(SOURCE_REVIEW_ASSESSMENT_PATH)
    inventory_review = read_json(REVIEWED_ARTIFACT_INVENTORY_REVIEW_PATH)
    resolution_review = read_json(REVIEWED_RESOLUTION_REVIEW_PATH)
    route_review = read_json(REVIEWED_ROUTE_REVIEW_PATH)
    boundary_review = read_json(FINAL_RESOLUTION_BOUNDARY_REVIEW_PATH)
    c5_review = read_json(C5_BLOCK_REVIEW_PATH)
    unresolved_review = read_json(UNRESOLVED_CONTINUATION_REVIEW_PATH)
    closure_candidate = read_json(CLOSURE_CANDIDATE_PATH)
    review_authority = read_json(REVIEW_AUTHORITY_PATH)
    review_classification = read_json(REVIEW_CLASSIFICATION_PATH)
    review_rollup = read_json(REVIEW_ROLLUP_PATH)
    review_profile = read_json(REVIEW_PROFILE_PATH)
    review_report = read_json(REVIEW_REPORT_PATH)
    review_trace = read_json(REVIEW_TRACE_PATH)

    exec_receipt = read_json(EXEC_RECEIPT_PATH)
    exec_summary = exec_receipt.get("machine_readable_o2_weak_feedback_resolution_proposed_record_review_summary", {})
    qa_records = read_jsonl(REVIEWED_QA_RECORDS_PATH)
    source_records = read_jsonl(REVIEWED_SOURCE_REF_RECORDS_PATH)
    undertyped_records = read_jsonl(REVIEWED_UNDERTYPED_RECORDS_PATH)
    parking_records = read_jsonl(REVIEWED_PARKING_RECORDS_PATH)
    resolution_records = read_jsonl(REVIEWED_RESOLUTION_RECORDS_PATH)
    route_records = read_jsonl(REVIEWED_ROUTE_MAP_PATH)
    exec_boundary = read_json(EXEC_BOUNDARY_READOUT_PATH)
    exec_c5 = read_json(EXEC_C5_READOUT_PATH)
    exec_unresolved = read_json(EXEC_UNRESOLVED_PATH)

    if review_receipt.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("review_receipt_not_pass")
    if review_receipt.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("review_stop_wrong")
    if review_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("review_hidden_next_command")
    if summary.get("status") != EXPECTED_REVIEW_STATUS:
        failures.append(f"review_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append(f"review_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "proposed_record_review_review_complete",
        "proposed_record_review_review_pass",
        "reviewed_artifacts_integrity_pass",
        "closure_candidate_ready",
        "reviewed_resolution_records_exist",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "reviewed_question_answer_records_reviewed_count": 3,
        "reviewed_source_ref_satisfaction_records_reviewed_count": 2,
        "reviewed_under_typed_acceptance_records_reviewed_count": 2,
        "reviewed_parking_continuation_records_reviewed_count": 3,
        "reviewed_resolution_records_reviewed_count": 3,
        "reviewed_route_records_reviewed_count": 3,
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
    if assessment.get("closure_candidate_ready") is not True:
        failures.append("assessment_not_close_ready")
    if inventory_review.get("reviewed_weak_feedback_resolution_records_count") != 3:
        failures.append("inventory_wrong")
    if resolution_review.get("reviewed_resolution_records_exist") is not True or resolution_review.get("weak_feedback_resolved") is not False:
        failures.append("resolution_review_wrong")
    if route_review.get("all_reviewed_not_closed") is not True:
        failures.append("route_review_wrong")
    if boundary_review.get("final_resolution_boundary_crossed") is not False or boundary_review.get("weak_feedback_resolved") is not False:
        failures.append("boundary_review_crossed")
    if c5_review.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_review.get("c5_opened") is not False:
        failures.append("c5_review_wrong")
    if unresolved_review.get("weak_feedback_resolved") is not False:
        failures.append("unresolved_review_wrong")
    if closure_candidate.get("closure_candidate_status") != "PROPOSED_RECORD_REVIEW_CLOSE_READY_REVIEWED_ARTIFACTS_NOT_FINAL":
        failures.append("closure_candidate_wrong")
    if review_authority.get("may_close_proposed_record_review_as_reviewed_reference_next") is not True:
        failures.append("authority_no_close")
    if review_authority.get("may_close_final_weak_feedback_resolution_now") is not False or review_authority.get("may_open_c5") is not False:
        failures.append("authority_allows_final_or_c5")
    if review_classification.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append("classification_next_wrong")
    if review_rollup.get("closure_candidate_ready_count") != 1 or review_rollup.get("weak_feedback_resolved_count") != 0:
        failures.append("rollup_wrong")
    if review_profile.get("next_command_goal") is not None or review_profile.get("final_resolution_boundary_crossed") is not False:
        failures.append("profile_wrong")
    if review_report.get("recommended_next_handling") != EXPECTED_REVIEW_NEXT:
        failures.append("report_next_wrong")
    if review_trace.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("trace_stop_wrong")

    if exec_receipt.get("receipt_id") != "6149c6d9" or exec_summary.get("reviewed_artifacts_emitted") is not True:
        failures.append("exec_receipt_wrong")
    if exec_summary.get("reviewed_resolution_records_emitted_count") != 3 or exec_summary.get("weak_feedback_resolved") is not False:
        failures.append("exec_summary_wrong")
    if len(qa_records) != 3 or len(source_records) != 2 or len(undertyped_records) != 2 or len(parking_records) != 3 or len(resolution_records) != 3 or len(route_records) != 3:
        failures.append("reviewed_record_counts_wrong")
    exec_boundary_final_crossed = exec_boundary.get("final_resolution_boundary_crossed")
    if exec_boundary_final_crossed is None:
        exec_boundary_final_crossed = exec_boundary.get("reviewed_artifacts_crossed_into_final_resolution")
    if exec_boundary_final_crossed is not False:
        failures.append("exec_boundary_wrong")
    if exec_c5.get("c5_opened") is not False:
        failures.append("exec_c5_wrong")
    if exec_unresolved.get("weak_feedback_resolved") is not False:
        failures.append("exec_unresolved_wrong")

    for row in resolution_records:
        if row.get("review_status") != "REVIEWED_ACCEPTED" or row.get("counts_as_reviewed_resolution") is not True:
            failures.append(f"reviewed_resolution_status_wrong:{row.get('reviewed_resolution_id')}")
        if row.get("counts_as_final_resolution") is not False or row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"reviewed_resolution_boundary_wrong:{row.get('reviewed_resolution_id')}")
        if row.get("requires_resolution_closure_before_resolved") is not True:
            failures.append(f"reviewed_resolution_missing_closure_gate:{row.get('reviewed_resolution_id')}")
    for row in route_records:
        if row.get("reviewed_record_emitted") is not True or row.get("current_resolution_state") != "REVIEWED_NOT_CLOSED":
            failures.append(f"route_state_wrong:{row.get('reviewed_route_record_id')}")
        if row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"route_boundary_wrong:{row.get('reviewed_route_record_id')}")

    return failures, {
        "qa": qa_records,
        "source": source_records,
        "undertyped": undertyped_records,
        "parking": parking_records,
        "resolution": resolution_records,
        "routes": route_records,
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

    close_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSED_AS_REVIEWED_REFERENCE_FINAL_RESOLUTION_DECISION_READY" if close_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if close_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSED_AS_REVIEWED_REFERENCE",
        "PROPOSED_RECORD_REVIEW_REVIEW_RECEIPT_CONSUMED",
        "REVIEWED_ARTIFACT_REFERENCE_FROZEN",
        "REVIEWED_QUESTION_ANSWER_RECORDS_FROZEN",
        "REVIEWED_SOURCE_REF_SATISFACTION_RECORDS_FROZEN",
        "REVIEWED_UNDER_TYPED_ACCEPTANCE_RECORDS_FROZEN",
        "REVIEWED_PARKING_CONTINUATION_RECORDS_FROZEN_UNRESOLVED",
        "REVIEWED_WEAK_FEEDBACK_RESOLUTION_RECORDS_FROZEN_NOT_FINAL",
        "REVIEWED_ROUTE_MAP_FROZEN_REVIEWED_NOT_CLOSED",
        "FINAL_RESOLUTION_BOUNDARY_LOCKED_NOT_CROSSED",
        "UNRESOLVED_STATUS_FROZEN",
        "C5_BLOCK_STATUS_FROZEN",
        "POST_CLOSURE_DECISION_READY",
        "NO_FINAL_WEAK_FEEDBACK_RESOLUTION_RECORDED",
        "NO_C5_RECONSIDERATION_READY",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if close_pass else failures

    closure_record = {
        "schema_version": "o2_proposed_record_review_closure_record_v0",
        "closure_status": "CLOSED_AS_REVIEWED_REFERENCE_REVIEWED_ARTIFACTS_NOT_FINAL" if close_pass else "CLOSURE_NOT_RECORDED",
        "source_proposed_record_review_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "closed_object": "o2_weak_feedback_resolution_proposed_record_review_output_v0",
        "closure_meaning": "Reviewed-artifact output is frozen as a reviewed reference.",
        "closure_does_not_mean": [
            "final weak-feedback resolution closed",
            "weak feedback resolved",
            "C5 reconsideration ready",
            "C5 opened",
            "live feedback audit executed",
            "runtime patched",
            "source mutated",
        ],
    }

    reviewed_reference = {
        "schema_version": "o2_proposed_record_review_reviewed_reference_v0",
        "reference_status": "FROZEN_REVIEWED_REFERENCE_REVIEWED_ARTIFACTS_NOT_FINAL" if close_pass else "REFERENCE_NOT_FROZEN",
        "reference_object_id": "o2_proposed_record_review_reviewed_reference_" + sha8({
            "review_receipt": SOURCE_REVIEW_RECEIPT_ID,
            "qa": len(qa),
            "source": len(source),
            "undertyped": len(undertyped),
            "parking": len(parking),
            "resolution": len(resolution),
            "routes": len(routes),
        }),
        "source_proposed_record_review_receipt_id": "6149c6d9",
        "source_proposed_record_review_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "frozen_counts": {
            "reviewed_question_answer_records": len(qa),
            "reviewed_source_ref_satisfaction_records": len(source),
            "reviewed_under_typed_acceptance_records": len(undertyped),
            "reviewed_parking_continuation_records": len(parking),
            "reviewed_weak_feedback_resolution_records": len(resolution),
            "reviewed_route_records": len(routes),
        },
        "reviewed_artifacts_exist": True,
        "reviewed_resolution_records_exist": True,
        "final_resolution_boundary_crossed": False,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    artifact_freeze = {
        "schema_version": "o2_reviewed_artifact_inventory_freeze_v0",
        "freeze_status": "REVIEWED_ARTIFACTS_FROZEN",
        "reviewed_question_answer_records_frozen_count": len(qa),
        "reviewed_source_ref_satisfaction_records_frozen_count": len(source),
        "reviewed_under_typed_acceptance_records_frozen_count": len(undertyped),
        "reviewed_parking_continuation_records_frozen_count": len(parking),
        "reviewed_weak_feedback_resolution_records_frozen_count": len(resolution),
        "reviewed_route_records_frozen_count": len(routes),
        "reviewed_artifacts_exist": True,
    }

    resolution_freeze = {
        "schema_version": "o2_reviewed_weak_feedback_resolution_record_freeze_v0",
        "freeze_status": "REVIEWED_RESOLUTION_RECORDS_FROZEN_NOT_FINAL",
        "reviewed_resolution_records_frozen_count": len(resolution),
        "all_count_as_reviewed_resolution": True,
        "all_require_resolution_closure_before_resolved": True,
        "final_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_reconsideration_ready": False,
    }

    route_freeze = {
        "schema_version": "o2_reviewed_route_map_freeze_v0",
        "freeze_status": "REVIEWED_ROUTE_MAP_FROZEN_REVIEWED_NOT_CLOSED",
        "reviewed_route_records_frozen_count": len(routes),
        "all_reviewed_record_emitted": True,
        "all_reviewed_not_closed": True,
        "weak_feedback_resolved": False,
        "c5_reconsideration_ready": False,
    }

    final_boundary_lock = {
        "schema_version": "o2_final_resolution_boundary_lock_v0",
        "boundary_lock_status": "FINAL_RESOLUTION_BOUNDARY_LOCKED_NOT_CROSSED",
        "reviewed_artifacts_exist": True,
        "reviewed_resolution_records_exist": True,
        "final_resolution_boundary_crossed": False,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "requires_decision_before_final_resolution_closure": True,
    }

    unresolved_freeze = {
        "schema_version": "o2_proposed_record_review_unresolved_status_freeze_v0",
        "freeze_status": "UNRESOLVED_STATUS_FROZEN",
        "reviewed_resolution_records_exist": True,
        "weak_feedback_resolved": False,
        "final_resolution_boundary_crossed": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_frozen_count": len(resolution),
        "parking_counted_as_resolution": False,
    }

    c5_freeze = {
        "schema_version": "o2_proposed_record_review_c5_block_freeze_v0",
        "freeze_status": "C5_BLOCK_STATUS_FROZEN",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "closure_does_not_unblock_c5": True,
    }

    receipt_chain = {
        "schema_version": "o2_proposed_record_review_receipt_chain_v0",
        "chain_status": "RECEIPT_CHAIN_PRESERVED",
        "receipts": [
            {"stage": "proposal_emission_post_closure_decision", "receipt_id": "63793a90"},
            {"stage": "proposed_record_review_execution", "receipt_id": "6149c6d9"},
            {"stage": "proposed_record_review_review", "receipt_id": SOURCE_REVIEW_RECEIPT_ID},
        ],
        "closure_receipt_pending": True,
    }

    downstream_decision_table = {
        "schema_version": "o2_proposed_record_review_closure_downstream_decision_table_v0",
        "decision_status": "POST_CLOSURE_DECISION_READY" if close_pass else "CLOSURE_REPAIR_REQUIRED",
        "records": [
            {
                "decision": "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_REFERENCE_CLOSURE",
                "selected": close_pass,
                "next_unit": recommended_next if close_pass else None,
                "why": "Reviewed artifacts are closed as a reference, but final weak-feedback resolution is still not closed.",
            },
            {
                "decision": "FINALIZE_WEAK_FEEDBACK_RESOLUTION_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Closure only freezes reviewed artifacts. A later decision must select final-resolution closure explicitly.",
            },
            {
                "decision": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 remains blocked until final weak-feedback resolution closure and a later C5 decision.",
            },
        ],
    }

    authority_boundary = {
        "schema_version": "o2_proposed_record_review_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_proposed_record_review_reference_closure": close_pass,
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
        "schema_version": "o2_proposed_record_review_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "proposed_record_review_closed_as_reviewed_reference": close_pass,
        "reviewed_reference_emitted": close_pass,
        "post_closure_decision_ready": close_pass,
        "reviewed_artifacts_frozen": close_pass,
        "reviewed_question_answer_records_frozen_count": len(qa),
        "reviewed_source_ref_satisfaction_records_frozen_count": len(source),
        "reviewed_under_typed_acceptance_records_frozen_count": len(undertyped),
        "reviewed_parking_continuation_records_frozen_count": len(parking),
        "reviewed_resolution_records_frozen_count": len(resolution),
        "reviewed_route_records_frozen_count": len(routes),
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
        "schema_version": "o2_proposed_record_review_closure_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "closure_count": 1 if close_pass else 0,
        "reviewed_reference_emitted_count": 1 if close_pass else 0,
        "post_closure_decision_ready_count": 1 if close_pass else 0,
        "reviewed_question_answer_records_frozen_count": len(qa),
        "reviewed_source_ref_satisfaction_records_frozen_count": len(source),
        "reviewed_under_typed_acceptance_records_frozen_count": len(undertyped),
        "reviewed_parking_continuation_records_frozen_count": len(parking),
        "reviewed_resolution_records_frozen_count": len(resolution),
        "reviewed_route_records_frozen_count": len(routes),
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
        "schema_version": "o2_proposed_record_review_closure_profile_v0",
        "profile_id": "o2_proposed_record_review_closure_profile_" + sha8(rollup),
        "status": status,
        "proposed_record_review_closed_as_reviewed_reference": close_pass,
        "reviewed_artifacts_frozen": close_pass,
        "reviewed_resolution_records_exist": True,
        "reviewed_resolution_records_frozen_count": len(resolution),
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "final_resolution_boundary_crossed": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Decide next after closing reviewed-artifact reference. Do not treat closure as final weak-feedback resolution.",
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
        "schema_version": "o2_proposed_record_review_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Proposed-record review was closed as a reviewed reference. Reviewed artifacts and reviewed weak-feedback resolution records are frozen, but final weak-feedback resolution remains unclosed and C5 remains blocked.",
        "reviewed_resolution_records_frozen_count": len(resolution),
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "final_resolution_boundary_crossed": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_proposed_record_review_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_proposed_record_review_review",
                "question": "is reviewed-artifact output clean and close-ready",
                "answer": "yes" if close_pass else "no",
                "taken": "freeze reviewed-artifact reference",
            },
            {
                "step": "lock_final_resolution_boundary",
                "question": "does closure finalize weak-feedback resolution",
                "answer": "no",
                "taken": "preserve final-resolution boundary",
            },
            {
                "step": "preserve_c5_block",
                "question": "does closure open C5",
                "answer": "no",
                "taken": "emit post-closure decision point",
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
        (REVIEWED_ARTIFACT_FREEZE_PATH, artifact_freeze),
        (REVIEWED_RESOLUTION_FREEZE_PATH, resolution_freeze),
        (REVIEWED_ROUTE_FREEZE_PATH, route_freeze),
        (FINAL_RESOLUTION_BOUNDARY_LOCK_PATH, final_boundary_lock),
        (UNRESOLVED_STATUS_FREEZE_PATH, unresolved_freeze),
        (C5_BLOCK_FREEZE_PATH, c5_freeze),
        (RECEIPT_CHAIN_PATH, receipt_chain),
        (DOWNSTREAM_DECISION_TABLE_PATH, downstream_decision_table),
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
        "PROPOSED_RECORD_REVIEW_CLOSE_0_REVIEW_RECEIPT_CONSUMED": SOURCE_REVIEW_RECEIPT_PATH.exists(),
        "PROPOSED_RECORD_REVIEW_CLOSE_1_CLOSURE_RECORD_EMITTED": CLOSURE_RECORD_PATH.exists(),
        "PROPOSED_RECORD_REVIEW_CLOSE_2_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists(),
        "PROPOSED_RECORD_REVIEW_CLOSE_3_REVIEWED_ARTIFACT_FREEZE_EMITTED": REVIEWED_ARTIFACT_FREEZE_PATH.exists(),
        "PROPOSED_RECORD_REVIEW_CLOSE_4_REVIEWED_RESOLUTION_FREEZE_EMITTED": REVIEWED_RESOLUTION_FREEZE_PATH.exists(),
        "PROPOSED_RECORD_REVIEW_CLOSE_5_ROUTE_FREEZE_EMITTED": REVIEWED_ROUTE_FREEZE_PATH.exists(),
        "PROPOSED_RECORD_REVIEW_CLOSE_6_FINAL_BOUNDARY_LOCK_EMITTED": FINAL_RESOLUTION_BOUNDARY_LOCK_PATH.exists(),
        "PROPOSED_RECORD_REVIEW_CLOSE_7_REVIEWED_RESOLUTION_RECORDS_EXIST": len(resolution) == 3,
        "PROPOSED_RECORD_REVIEW_CLOSE_8_FINAL_RESOLUTION_NOT_CROSSED": final_boundary_lock["final_resolution_boundary_crossed"] is False and final_boundary_lock["weak_feedback_resolved"] is False,
        "PROPOSED_RECORD_REVIEW_CLOSE_9_C5_BLOCK_PRESERVED": c5_freeze["c5_opened"] is False and c5_freeze["c5_reconsideration_ready"] is False,
        "PROPOSED_RECORD_REVIEW_CLOSE_10_NO_PARKING_AS_RESOLUTION": rollup["parked_records_counted_as_resolved_count"] == 0,
        "PROPOSED_RECORD_REVIEW_CLOSE_11_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "PROPOSED_RECORD_REVIEW_CLOSE_12_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "PROPOSED_RECORD_REVIEW_CLOSE_13_POST_CLOSURE_DECISION_READY": rollup["post_closure_decision_ready_count"] == 1,
        "PROPOSED_RECORD_REVIEW_CLOSE_14_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "PROPOSED_RECORD_REVIEW_CLOSE_15_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "PROPOSED_RECORD_REVIEW_CLOSE_16_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "closed": close_pass,
        "reviewed_resolution_records": len(resolution),
        "final_resolution": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_resolution_proposed_record_review_closure_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_proposed_record_review_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_resolution_proposed_record_review_closure_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "proposed_record_review_closed_as_reviewed_reference": close_pass,
            "reviewed_reference_emitted": close_pass,
            "post_closure_decision_ready": close_pass,
            "reviewed_artifacts_frozen": close_pass,
            "reviewed_question_answer_records_frozen_count": len(qa),
            "reviewed_source_ref_satisfaction_records_frozen_count": len(source),
            "reviewed_under_typed_acceptance_records_frozen_count": len(undertyped),
            "reviewed_parking_continuation_records_frozen_count": len(parking),
            "reviewed_resolution_records_frozen_count": len(resolution),
            "reviewed_route_records_frozen_count": len(routes),
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
            "closure_record": rel(CLOSURE_RECORD_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "reviewed_artifact_freeze": rel(REVIEWED_ARTIFACT_FREEZE_PATH),
            "reviewed_resolution_freeze": rel(REVIEWED_RESOLUTION_FREEZE_PATH),
            "reviewed_route_freeze": rel(REVIEWED_ROUTE_FREEZE_PATH),
            "final_resolution_boundary_lock": rel(FINAL_RESOLUTION_BOUNDARY_LOCK_PATH),
            "unresolved_status_freeze": rel(UNRESOLVED_STATUS_FREEZE_PATH),
            "c5_block_freeze": rel(C5_BLOCK_FREEZE_PATH),
            "receipt_chain": rel(RECEIPT_CHAIN_PATH),
            "downstream_decision_table": rel(DOWNSTREAM_DECISION_TABLE_PATH),
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
    print(f"proposed_record_review_closure_receipt_id={receipt_id}")
    print(f"proposed_record_review_closure_receipt_path={rel(receipt_path)}")
    print(f"proposed_record_review_closure_record_path={rel(CLOSURE_RECORD_PATH)}")
    print(f"proposed_record_review_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"reviewed_artifact_inventory_freeze_path={rel(REVIEWED_ARTIFACT_FREEZE_PATH)}")
    print(f"reviewed_resolution_freeze_path={rel(REVIEWED_RESOLUTION_FREEZE_PATH)}")
    print(f"reviewed_route_freeze_path={rel(REVIEWED_ROUTE_FREEZE_PATH)}")
    print(f"final_resolution_boundary_lock_path={rel(FINAL_RESOLUTION_BOUNDARY_LOCK_PATH)}")
    print(f"proposed_record_review_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"proposed_record_review_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
