#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_proposal_emission_review.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REVIEW"
MODE = "REVIEW / PROPOSED_RECORD_EMISSION_INTEGRITY / NO_REVIEWED_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REVIEW_ONLY"

PROPOSAL_EMISSION_RECEIPT_ID = "1ddc557a"
PROPOSAL_EMISSION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0_receipts/1ddc557a.json"
PROPOSAL_EMISSION_RECORD_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_weak_feedback_resolution_proposal_emission_record_v0.json"
PROPOSED_QA_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_question_answer_records_v0.jsonl"
PROPOSED_SOURCE_REF_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_source_ref_satisfaction_records_v0.jsonl"
PROPOSED_UNDERTYPED_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_under_typed_acceptance_review_records_v0.jsonl"
PARKING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_parking_execution_continuation_records_v0.jsonl"
PROPOSED_RESOLUTION_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_weak_feedback_resolution_records_v0.jsonl"
EMISSION_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_weak_feedback_resolution_proposal_emission_route_map_v0.jsonl"
EMISSION_GATE_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_weak_feedback_resolution_proposal_emission_gate_readout_v0.json"
PROPOSAL_REVIEW_BOUNDARY_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposal_emission_review_boundary_readout_v0.json"
C5_BLOCK_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposal_emission_c5_block_readout_v0.json"
UNRESOLVED_CONTINUATION_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposal_emission_unresolved_continuation_v0.json"
PROPOSAL_EMISSION_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposal_emission_authority_boundary_v0.json"
PROPOSAL_EMISSION_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposal_emission_classification_v0.json"
PROPOSAL_EMISSION_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposal_emission_rollup_v0.json"
PROPOSAL_EMISSION_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposal_emission_profile_v0.json"
PROPOSAL_EMISSION_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposal_emission_report.json"
PROPOSAL_EMISSION_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposal_emission_transition_trace.json"

POST_DECISION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0_receipts/1982e56e.json"
POST_PROPOSAL_AUTH_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_weak_feedback_resolution_proposal_emission_authorization_v0.json"
EXEC_TARGET_REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_target_reviewed_reference_v0.json"

REQUIRED_SOURCE_FILES = [
    PROPOSAL_EMISSION_RECEIPT_PATH,
    PROPOSAL_EMISSION_RECORD_PATH,
    PROPOSED_QA_RECORDS_PATH,
    PROPOSED_SOURCE_REF_RECORDS_PATH,
    PROPOSED_UNDERTYPED_RECORDS_PATH,
    PARKING_RECORDS_PATH,
    PROPOSED_RESOLUTION_RECORDS_PATH,
    EMISSION_ROUTE_MAP_PATH,
    EMISSION_GATE_READOUT_PATH,
    PROPOSAL_REVIEW_BOUNDARY_READOUT_PATH,
    C5_BLOCK_READOUT_PATH,
    UNRESOLVED_CONTINUATION_PATH,
    PROPOSAL_EMISSION_AUTHORITY_PATH,
    PROPOSAL_EMISSION_CLASSIFICATION_PATH,
    PROPOSAL_EMISSION_ROLLUP_PATH,
    PROPOSAL_EMISSION_PROFILE_PATH,
    PROPOSAL_EMISSION_REPORT_PATH,
    PROPOSAL_EMISSION_TRACE_PATH,
    POST_DECISION_RECEIPT_PATH,
    POST_PROPOSAL_AUTH_PATH,
    EXEC_TARGET_REVIEWED_REFERENCE_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "o2_proposal_emission_review_assessment_v0.json"
PROPOSED_RECORD_INVENTORY_REVIEW_PATH = OUT_DIR / "o2_proposed_record_inventory_review_v0.json"
PROPOSED_RESOLUTION_REVIEW_PATH = OUT_DIR / "o2_proposed_weak_feedback_resolution_record_review_v0.json"
EMISSION_ROUTE_REVIEW_PATH = OUT_DIR / "o2_proposal_emission_route_review_v0.json"
EMISSION_GATE_REVIEW_PATH = OUT_DIR / "o2_proposal_emission_gate_review_v0.json"
PROPOSAL_REVIEW_BOUNDARY_REVIEW_PATH = OUT_DIR / "o2_proposal_review_boundary_review_v0.json"
C5_BLOCK_REVIEW_PATH = OUT_DIR / "o2_proposal_emission_c5_block_review_v0.json"
UNRESOLVED_CONTINUATION_REVIEW_PATH = OUT_DIR / "o2_proposal_emission_unresolved_continuation_review_v0.json"
CLOSURE_CANDIDATE_PATH = OUT_DIR / "o2_proposal_emission_closure_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_proposal_emission_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_proposal_emission_review_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_proposal_emission_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_proposal_emission_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_proposal_emission_review_report.json"
TRACE_PATH = OUT_DIR / "o2_proposal_emission_review_transition_trace.json"

EXPECTED_EMISSION_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_EXECUTED_PROPOSED_RECORDS_REVIEW_READY"
EXPECTED_EMISSION_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_EXECUTED_PROPOSED_RECORDS_REVIEW_READY"
EXPECTED_EMISSION_NEXT = "REVIEW_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_V0"
RECOMMENDED_NEXT = "CLOSE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_AS_REVIEWED_REFERENCE_V0"

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

    receipt = read_json(PROPOSAL_EMISSION_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_resolution_proposal_emission_summary", {})
    emission_record = read_json(PROPOSAL_EMISSION_RECORD_PATH)
    qa_records = read_jsonl(PROPOSED_QA_RECORDS_PATH)
    source_records = read_jsonl(PROPOSED_SOURCE_REF_RECORDS_PATH)
    undertyped_records = read_jsonl(PROPOSED_UNDERTYPED_RECORDS_PATH)
    parking_records = read_jsonl(PARKING_RECORDS_PATH)
    resolution_records = read_jsonl(PROPOSED_RESOLUTION_RECORDS_PATH)
    emission_routes = read_jsonl(EMISSION_ROUTE_MAP_PATH)
    gate_readout = read_json(EMISSION_GATE_READOUT_PATH)
    boundary_readout = read_json(PROPOSAL_REVIEW_BOUNDARY_READOUT_PATH)
    c5_readout = read_json(C5_BLOCK_READOUT_PATH)
    unresolved = read_json(UNRESOLVED_CONTINUATION_PATH)
    authority = read_json(PROPOSAL_EMISSION_AUTHORITY_PATH)
    classification = read_json(PROPOSAL_EMISSION_CLASSIFICATION_PATH)
    rollup = read_json(PROPOSAL_EMISSION_ROLLUP_PATH)
    profile = read_json(PROPOSAL_EMISSION_PROFILE_PATH)
    report = read_json(PROPOSAL_EMISSION_REPORT_PATH)
    trace = read_json(PROPOSAL_EMISSION_TRACE_PATH)

    post_receipt = read_json(POST_DECISION_RECEIPT_PATH)
    post_auth = read_json(POST_PROPOSAL_AUTH_PATH)
    reviewed_ref = read_json(EXEC_TARGET_REVIEWED_REFERENCE_PATH)

    if receipt.get("receipt_id") != PROPOSAL_EMISSION_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("proposal_emission_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_EMISSION_STOP:
        failures.append("proposal_emission_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("proposal_emission_hidden_next_command")
    if summary.get("status") != EXPECTED_EMISSION_STATUS:
        failures.append(f"proposal_emission_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_EMISSION_NEXT:
        failures.append(f"proposal_emission_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "proposal_emission_executed",
        "proposal_records_emitted",
        "review_ready",
        "all_proposed_records_unreviewed",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "proposed_question_answer_records_emitted_count": 3,
        "proposed_source_ref_satisfaction_records_emitted_count": 2,
        "proposed_under_typed_acceptance_review_records_emitted_count": 2,
        "parking_execution_continuation_records_emitted_count": 3,
        "proposed_resolution_records_emitted_count": 3,
        "proposal_emission_route_records_count": 3,
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

    if emission_record.get("emission_status") != "PROPOSED_RECORDS_EMITTED_REVIEW_READY":
        failures.append("emission_record_status_wrong")
    if len(qa_records) != 3 or len(source_records) != 2 or len(undertyped_records) != 2 or len(parking_records) != 3 or len(resolution_records) != 3 or len(emission_routes) != 3:
        failures.append("proposal_record_counts_wrong")

    for row in qa_records:
        if row.get("proposal_status") != "PROPOSED_UNREVIEWED" or row.get("review_status") != "UNREVIEWED":
            failures.append(f"qa_record_status_wrong:{row.get('proposed_answer_id')}")
        if row.get("counts_as_answer") is not False or row.get("counts_as_resolution_input") is not False:
            failures.append(f"qa_record_counts_wrong:{row.get('proposed_answer_id')}")
    for row in source_records:
        if row.get("proposal_status") != "PROPOSED_UNREVIEWED" or row.get("review_status") != "UNREVIEWED":
            failures.append(f"source_record_status_wrong:{row.get('proposed_satisfaction_id')}")
        if row.get("counts_as_satisfied") is not False or row.get("counts_as_resolution_input") is not False:
            failures.append(f"source_record_counts_wrong:{row.get('proposed_satisfaction_id')}")
    for row in undertyped_records:
        if row.get("proposal_status") != "PROPOSED_UNREVIEWED" or row.get("review_status") != "UNREVIEWED":
            failures.append(f"undertyped_record_status_wrong:{row.get('proposed_review_id')}")
        if row.get("counts_as_approved") is not False or row.get("c5_unblock_allowed") is not False:
            failures.append(f"undertyped_record_counts_wrong:{row.get('proposed_review_id')}")
    for row in parking_records:
        if row.get("proposal_status") != "PARKED_UNRESOLVED_UNREVIEWED" or row.get("review_status") != "UNREVIEWED":
            failures.append(f"parking_record_status_wrong:{row.get('parking_execution_id')}")
        if row.get("counts_as_resolution") is not False or row.get("c5_unblock_allowed") is not False:
            failures.append(f"parking_record_counts_wrong:{row.get('parking_execution_id')}")
    for row in resolution_records:
        if row.get("proposal_status") != "PROPOSED_UNREVIEWED" or row.get("review_status") != "UNREVIEWED":
            failures.append(f"resolution_record_status_wrong:{row.get('proposed_resolution_id')}")
        if row.get("counts_as_reviewed_resolution") is not False or row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"resolution_record_boundary_wrong:{row.get('proposed_resolution_id')}")
    for row in emission_routes:
        if row.get("proposed_record_emitted") is not True or row.get("reviewed_record_emitted") is not False:
            failures.append(f"route_emission_flags_wrong:{row.get('emission_route_record_id')}")
        if row.get("review_status") != "UNREVIEWED" or row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"route_boundary_wrong:{row.get('emission_route_record_id')}")

    if gate_readout.get("proposed_resolution_records_emitted_count") != 3 or gate_readout.get("reviewed_resolution_records_emitted_count") != 0:
        failures.append("gate_readout_counts_wrong")
    if boundary_readout.get("template_layer_crossed_into_proposal_layer") is not True:
        failures.append("boundary_template_to_proposal_not_crossed")
    if boundary_readout.get("proposal_layer_crossed_into_review_layer") is not False:
        failures.append("boundary_proposal_to_review_crossed")
    if c5_readout.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_readout.get("c5_opened") is not False:
        failures.append("c5_readout_wrong")
    if unresolved.get("weak_feedback_resolved") is not False or unresolved.get("resolution_records_emitted_count") != 0:
        failures.append("unresolved_continuation_wrong")
    if authority.get("may_review_proposal_emission_next") is not True:
        failures.append("authority_no_review_next")
    if authority.get("may_emit_reviewed_resolution_records_now") is not False or authority.get("may_open_c5") is not False:
        failures.append("authority_allows_reviewed_or_c5")
    if classification.get("recommended_next") != EXPECTED_EMISSION_NEXT:
        failures.append("classification_next_wrong")
    if rollup.get("review_ready_count") != 1 or rollup.get("reviewed_resolution_records_emitted_count") != 0:
        failures.append("rollup_wrong")
    if profile.get("proposal_emission_executed") is not True or profile.get("weak_feedback_resolved") is not False:
        failures.append("profile_wrong")
    if report.get("recommended_next_handling") != EXPECTED_EMISSION_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_EMISSION_STOP:
        failures.append("trace_stop_wrong")
    if post_receipt.get("receipt_id") != "1982e56e":
        failures.append("post_decision_receipt_wrong")
    if post_auth.get("authorized_next_unit") != "EXECUTE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_V0":
        failures.append("post_auth_wrong")
    if reviewed_ref.get("templates_are_not_proposed_records") is not True or reviewed_ref.get("c5_opened") is not False:
        failures.append("reviewed_reference_wrong")

    return failures, {
        "qa_records": qa_records,
        "source_records": source_records,
        "undertyped_records": undertyped_records,
        "parking_records": parking_records,
        "resolution_records": resolution_records,
        "emission_routes": emission_routes,
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
    resolution_records = src.get("resolution_records", [])
    emission_routes = src.get("emission_routes", [])

    review_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REVIEWED_PROPOSED_RECORDS_CLEAN_CLOSE_READY" if review_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REVIEW_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REVIEW_COMPLETE",
        "WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REVIEW_PASS",
        "PROPOSAL_EMISSION_RECEIPT_CONSUMED",
        "PROPOSED_RECORD_INVENTORY_REVIEWED",
        "PROPOSED_RECORDS_CONFIRMED_UNREVIEWED",
        "PROPOSED_WEAK_FEEDBACK_RESOLUTION_RECORDS_CONFIRMED_UNREVIEWED",
        "EMISSION_ROUTE_MAP_REVIEWED",
        "TEMPLATE_TO_PROPOSAL_BOUNDARY_CONFIRMED",
        "PROPOSAL_TO_REVIEW_BOUNDARY_NOT_CROSSED",
        "C5_BLOCK_REVIEWED_ENFORCED",
        "CLOSURE_CANDIDATE_READY",
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
    ] if review_pass else failures

    review_assessment = {
        "schema_version": "o2_proposal_emission_review_assessment_v0",
        "review_status": status,
        "review_complete": review_pass,
        "review_pass": review_pass,
        "source_proposal_emission_receipt_id": PROPOSAL_EMISSION_RECEIPT_ID,
        "proposal_emission_reviewed": review_pass,
        "closure_candidate_ready": review_pass,
        "recommended_next": recommended_next,
    }

    inventory_review = {
        "schema_version": "o2_proposed_record_inventory_review_v0",
        "review_status": "PROPOSED_RECORD_INVENTORY_REVIEW_PASS" if review_pass else "PROPOSED_RECORD_INVENTORY_REVIEW_FAIL",
        "proposed_question_answer_records_count": len(qa_records),
        "proposed_source_ref_satisfaction_records_count": len(source_records),
        "proposed_under_typed_acceptance_review_records_count": len(undertyped_records),
        "parking_execution_continuation_records_count": len(parking_records),
        "proposed_weak_feedback_resolution_records_count": len(resolution_records),
        "all_proposed_records_unreviewed": all(x.get("review_status") == "UNREVIEWED" for x in qa_records + source_records + undertyped_records + parking_records + resolution_records),
        "all_proposed_records_not_reviewed_resolution": all(x.get("counts_as_reviewed_resolution") is False for x in resolution_records),
        "all_auxiliary_records_not_counted_as_final": (
            all(x.get("counts_as_answer") is False for x in qa_records)
            and all(x.get("counts_as_satisfied") is False for x in source_records)
            and all(x.get("counts_as_approved") is False for x in undertyped_records)
            and all(x.get("counts_as_resolution") is False for x in parking_records)
        ),
    }

    proposed_resolution_review = {
        "schema_version": "o2_proposed_weak_feedback_resolution_record_review_v0",
        "review_status": "PROPOSED_RESOLUTION_RECORD_REVIEW_PASS" if review_pass else "PROPOSED_RESOLUTION_RECORD_REVIEW_FAIL",
        "proposed_resolution_records_reviewed_count": len(resolution_records),
        "all_proposed_unreviewed": all(x.get("proposal_status") == "PROPOSED_UNREVIEWED" and x.get("review_status") == "UNREVIEWED" for x in resolution_records),
        "reviewed_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_reconsideration_ready": False,
    }

    emission_route_review = {
        "schema_version": "o2_proposal_emission_route_review_v0",
        "review_status": "EMISSION_ROUTE_REVIEW_PASS" if review_pass else "EMISSION_ROUTE_REVIEW_FAIL",
        "emission_route_records_reviewed_count": len(emission_routes),
        "all_proposed_record_emitted": all(x.get("proposed_record_emitted") is True for x in emission_routes),
        "all_reviewed_record_emitted_false": all(x.get("reviewed_record_emitted") is False for x in emission_routes),
        "all_unreviewed": all(x.get("review_status") == "UNREVIEWED" for x in emission_routes),
        "all_unresolved": all(x.get("current_resolution_state") == "UNRESOLVED" for x in emission_routes),
        "all_c5_reconsideration_false": all(x.get("c5_reconsideration_ready") is False for x in emission_routes),
    }

    gate_review = {
        "schema_version": "o2_proposal_emission_gate_review_v0",
        "review_status": "PROPOSAL_EMISSION_GATE_REVIEW_PASS" if review_pass else "PROPOSAL_EMISSION_GATE_REVIEW_FAIL",
        "proposal_emission_executed": True,
        "reviewed_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "review_required_next": False,
        "closure_required_next": review_pass,
    }

    boundary_review = {
        "schema_version": "o2_proposal_review_boundary_review_v0",
        "review_status": "PROPOSAL_REVIEW_BOUNDARY_REVIEW_PASS" if review_pass else "PROPOSAL_REVIEW_BOUNDARY_REVIEW_FAIL",
        "template_layer_crossed_into_proposal_layer": True,
        "proposal_layer_crossed_into_review_layer": False,
        "proposed_records_exist": True,
        "proposed_records_remain_unreviewed": True,
        "proposed_records_are_not_reviewed_records": True,
        "reviewed_resolution_records_emitted_count": 0,
    }

    c5_review = {
        "schema_version": "o2_proposal_emission_c5_block_review_v0",
        "review_status": "C5_BLOCK_REVIEW_PASS" if review_pass else "C5_BLOCK_REVIEW_FAIL",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "block_enforced": True,
        "reason": "Emission review did not promote proposed records into reviewed resolution records.",
    }

    unresolved_review = {
        "schema_version": "o2_proposal_emission_unresolved_continuation_review_v0",
        "review_status": "UNRESOLVED_CONTINUATION_REVIEW_PASS" if review_pass else "UNRESOLVED_CONTINUATION_REVIEW_FAIL",
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
    }

    closure_candidate = {
        "schema_version": "o2_proposal_emission_closure_candidate_v0",
        "closure_candidate_status": "PROPOSAL_EMISSION_CLOSE_READY_PROPOSED_RECORDS_UNREVIEWED" if review_pass else "PROPOSAL_EMISSION_CLOSE_NOT_READY",
        "review_pass": review_pass,
        "closure_meaning": "Close proposal-emission output as reviewed reference while preserving proposed-record/unreviewed status.",
        "closure_does_not_mean": [
            "proposed records become reviewed records",
            "reviewed resolution records exist",
            "weak feedback resolved",
            "question packets answered as reviewed",
            "source-ref requests satisfied as reviewed",
            "under-typed acceptance approved as reviewed",
            "parking counted as resolution",
            "C5 reconsideration ready",
            "C5 opened",
        ],
        "recommended_next": recommended_next,
    }

    authority_boundary = {
        "schema_version": "o2_proposal_emission_review_authority_boundary_v0",
        "status": status,
        "may_close_proposal_emission_as_reviewed_reference_next": review_pass,
        "may_emit_new_proposed_records_now": False,
        "may_emit_reviewed_resolution_records_now": False,
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
        "schema_version": "o2_proposal_emission_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "proposal_emission_review_complete": review_pass,
        "proposal_emission_review_pass": review_pass,
        "proposal_records_reviewed_for_emission_integrity": review_pass,
        "closure_candidate_ready": review_pass,
        "proposed_question_answer_records_reviewed_count": len(qa_records),
        "proposed_source_ref_satisfaction_records_reviewed_count": len(source_records),
        "proposed_under_typed_acceptance_review_records_reviewed_count": len(undertyped_records),
        "parking_execution_continuation_records_reviewed_count": len(parking_records),
        "proposed_resolution_records_reviewed_count": len(resolution_records),
        "proposal_emission_route_records_reviewed_count": len(emission_routes),
        "all_proposed_records_unreviewed": True,
        "proposal_review_boundary_crossed": False,
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
        "schema_version": "o2_proposal_emission_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "closure_candidate_ready_count": 1 if review_pass else 0,
        "proposed_question_answer_records_reviewed_count": len(qa_records),
        "proposed_source_ref_satisfaction_records_reviewed_count": len(source_records),
        "proposed_under_typed_acceptance_review_records_reviewed_count": len(undertyped_records),
        "parking_execution_continuation_records_reviewed_count": len(parking_records),
        "proposed_resolution_records_reviewed_count": len(resolution_records),
        "proposal_emission_route_records_reviewed_count": len(emission_routes),
        "weak_feedback_resolved_count": 0,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
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
        "schema_version": "o2_proposal_emission_review_profile_v0",
        "profile_id": "o2_proposal_emission_review_profile_" + sha8(rollup),
        "status": status,
        "proposal_emission_review_pass": review_pass,
        "proposal_records_reviewed_for_emission_integrity": review_pass,
        "proposed_records_remain_unreviewed": True,
        "closure_candidate_ready": review_pass,
        "proposed_resolution_records_reviewed_count": len(resolution_records),
        "reviewed_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Close proposal emission as reviewed reference. Do not treat emitted proposed records as reviewed resolution.",
        "must_not_infer": [
            "proposed records accepted as reviewed",
            "reviewed resolution records emitted",
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
        "schema_version": "o2_proposal_emission_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Proposal emission reviewed clean for emission integrity. Proposed records exist and remain unreviewed. The proposal-to-review boundary was not crossed; no reviewed resolution records exist; weak feedback remains unresolved; C5 remains blocked.",
        "proposal_emission_review_pass": review_pass,
        "proposed_resolution_records_reviewed_count": len(resolution_records),
        "reviewed_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_proposal_emission_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_proposal_emission",
                "question": "were proposed records emitted and ready for review",
                "answer": "yes" if review_pass else "no",
                "taken": "review proposed-record inventory and route map",
            },
            {
                "step": "verify_proposed_unreviewed_boundary",
                "question": "did review promote proposals into reviewed records",
                "answer": "no",
                "taken": "preserve proposal-to-review boundary",
            },
            {
                "step": "verify_resolution_and_c5_boundary",
                "question": "does emission review resolve weak feedback or unblock C5",
                "answer": "no",
                "taken": "emit close-ready reference candidate",
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
        (PROPOSED_RECORD_INVENTORY_REVIEW_PATH, inventory_review),
        (PROPOSED_RESOLUTION_REVIEW_PATH, proposed_resolution_review),
        (EMISSION_ROUTE_REVIEW_PATH, emission_route_review),
        (EMISSION_GATE_REVIEW_PATH, gate_review),
        (PROPOSAL_REVIEW_BOUNDARY_REVIEW_PATH, boundary_review),
        (C5_BLOCK_REVIEW_PATH, c5_review),
        (UNRESOLVED_CONTINUATION_REVIEW_PATH, unresolved_review),
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
        "PROPOSAL_EMISSION_REVIEW_0_EMISSION_RECEIPT_CONSUMED": PROPOSAL_EMISSION_RECEIPT_PATH.exists(),
        "PROPOSAL_EMISSION_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "PROPOSAL_EMISSION_REVIEW_2_RECORD_INVENTORY_REVIEW_EMITTED": PROPOSED_RECORD_INVENTORY_REVIEW_PATH.exists(),
        "PROPOSAL_EMISSION_REVIEW_3_PROPOSED_RESOLUTION_REVIEW_EMITTED": PROPOSED_RESOLUTION_REVIEW_PATH.exists(),
        "PROPOSAL_EMISSION_REVIEW_4_EMISSION_ROUTE_REVIEW_EMITTED": EMISSION_ROUTE_REVIEW_PATH.exists(),
        "PROPOSAL_EMISSION_REVIEW_5_ALL_PROPOSED_RECORDS_UNREVIEWED": inventory_review["all_proposed_records_unreviewed"] is True,
        "PROPOSAL_EMISSION_REVIEW_6_NO_REVIEWED_RESOLUTION_RECORDS": proposed_resolution_review["reviewed_resolution_records_emitted_count"] == 0 and proposed_resolution_review["resolution_records_emitted_count"] == 0,
        "PROPOSAL_EMISSION_REVIEW_7_EMISSION_ROUTES_REVIEWED_UNREVIEWED": emission_route_review["all_unreviewed"] is True and emission_route_review["all_reviewed_record_emitted_false"] is True,
        "PROPOSAL_EMISSION_REVIEW_8_PROPOSAL_REVIEW_BOUNDARY_NOT_CROSSED": boundary_review["proposal_layer_crossed_into_review_layer"] is False,
        "PROPOSAL_EMISSION_REVIEW_9_C5_BLOCK_ENFORCED": c5_review["c5_opened"] is False and c5_review["c5_reconsideration_ready"] is False,
        "PROPOSAL_EMISSION_REVIEW_10_WEAK_FEEDBACK_NOT_RESOLVED": rollup["weak_feedback_resolved_count"] == 0,
        "PROPOSAL_EMISSION_REVIEW_11_NO_ANSWER_SATISFY_APPROVE": rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "PROPOSAL_EMISSION_REVIEW_12_NO_PARKING_AS_RESOLUTION": rollup["parked_records_counted_as_resolved_count"] == 0,
        "PROPOSAL_EMISSION_REVIEW_13_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "PROPOSAL_EMISSION_REVIEW_14_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "PROPOSAL_EMISSION_REVIEW_15_CLOSURE_CANDIDATE_READY": closure_candidate["closure_candidate_status"] == "PROPOSAL_EMISSION_CLOSE_READY_PROPOSED_RECORDS_UNREVIEWED",
        "PROPOSAL_EMISSION_REVIEW_16_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "PROPOSAL_EMISSION_REVIEW_17_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "PROPOSAL_EMISSION_REVIEW_18_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "review_pass": review_pass,
        "reviewed_resolution_records": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_resolution_proposal_emission_review_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_proposal_emission_receipt_id": PROPOSAL_EMISSION_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_resolution_proposal_emission_review_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "proposal_emission_review_complete": review_pass,
            "proposal_emission_review_pass": review_pass,
            "proposal_records_reviewed_for_emission_integrity": review_pass,
            "closure_candidate_ready": review_pass,
            "proposed_question_answer_records_reviewed_count": len(qa_records),
            "proposed_source_ref_satisfaction_records_reviewed_count": len(source_records),
            "proposed_under_typed_acceptance_review_records_reviewed_count": len(undertyped_records),
            "parking_execution_continuation_records_reviewed_count": len(parking_records),
            "proposed_resolution_records_reviewed_count": len(resolution_records),
            "proposal_emission_route_records_reviewed_count": len(emission_routes),
            "all_proposed_records_unreviewed": True,
            "proposed_records_remain_unreviewed": True,
            "proposal_review_boundary_crossed": False,
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
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "proposed_record_inventory_review": rel(PROPOSED_RECORD_INVENTORY_REVIEW_PATH),
            "proposed_resolution_review": rel(PROPOSED_RESOLUTION_REVIEW_PATH),
            "emission_route_review": rel(EMISSION_ROUTE_REVIEW_PATH),
            "emission_gate_review": rel(EMISSION_GATE_REVIEW_PATH),
            "proposal_review_boundary_review": rel(PROPOSAL_REVIEW_BOUNDARY_REVIEW_PATH),
            "c5_block_review": rel(C5_BLOCK_REVIEW_PATH),
            "unresolved_continuation_review": rel(UNRESOLVED_CONTINUATION_REVIEW_PATH),
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
    print(f"proposal_emission_review_receipt_id={receipt_id}")
    print(f"proposal_emission_review_receipt_path={rel(receipt_path)}")
    print(f"proposal_emission_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"proposed_record_inventory_review_path={rel(PROPOSED_RECORD_INVENTORY_REVIEW_PATH)}")
    print(f"proposed_resolution_review_path={rel(PROPOSED_RESOLUTION_REVIEW_PATH)}")
    print(f"proposal_emission_route_review_path={rel(EMISSION_ROUTE_REVIEW_PATH)}")
    print(f"proposal_emission_gate_review_path={rel(EMISSION_GATE_REVIEW_PATH)}")
    print(f"proposal_review_boundary_review_path={rel(PROPOSAL_REVIEW_BOUNDARY_REVIEW_PATH)}")
    print(f"proposal_emission_c5_block_review_path={rel(C5_BLOCK_REVIEW_PATH)}")
    print(f"proposal_emission_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"proposal_emission_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
