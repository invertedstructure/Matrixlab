#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_proposal_emission_closure.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_CLOSURE"
MODE = "CLOSE / FREEZE_REVIEWED_PROPOSAL_EMISSION_REFERENCE / NO_REVIEWED_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_CLOSURE_ONLY"

PROPOSAL_EMISSION_REVIEW_RECEIPT_ID = "89d6b318"
PROPOSAL_EMISSION_REVIEW_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0_receipts/89d6b318.json"
PROPOSAL_EMISSION_REVIEW_ASSESSMENT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposal_emission_review_assessment_v0.json"
PROPOSED_RECORD_INVENTORY_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposed_record_inventory_review_v0.json"
PROPOSED_RESOLUTION_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposed_weak_feedback_resolution_record_review_v0.json"
EMISSION_ROUTE_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposal_emission_route_review_v0.json"
EMISSION_GATE_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposal_emission_gate_review_v0.json"
BOUNDARY_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposal_review_boundary_review_v0.json"
C5_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposal_emission_c5_block_review_v0.json"
UNRESOLVED_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposal_emission_unresolved_continuation_review_v0.json"
CLOSURE_CANDIDATE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposal_emission_closure_candidate_v0.json"
REVIEW_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposal_emission_review_authority_boundary_v0.json"
REVIEW_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposal_emission_review_classification_v0.json"
REVIEW_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposal_emission_review_rollup_v0.json"
REVIEW_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposal_emission_review_profile_v0.json"
REVIEW_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposal_emission_review_report.json"
REVIEW_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_review_v0/o2_proposal_emission_review_transition_trace.json"

PROPOSAL_EMISSION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0_receipts/1ddc557a.json"
PROPOSAL_EMISSION_RECORD_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_weak_feedback_resolution_proposal_emission_record_v0.json"
PROPOSED_QA_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_question_answer_records_v0.jsonl"
PROPOSED_SOURCE_REF_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_source_ref_satisfaction_records_v0.jsonl"
PROPOSED_UNDERTYPED_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_under_typed_acceptance_review_records_v0.jsonl"
PARKING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_parking_execution_continuation_records_v0.jsonl"
PROPOSED_RESOLUTION_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_weak_feedback_resolution_records_v0.jsonl"
EMISSION_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_weak_feedback_resolution_proposal_emission_route_map_v0.jsonl"
EMISSION_GATE_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_weak_feedback_resolution_proposal_emission_gate_readout_v0.json"
PROPOSAL_BOUNDARY_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposal_emission_review_boundary_readout_v0.json"
C5_BLOCK_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposal_emission_c5_block_readout_v0.json"
UNRESOLVED_CONTINUATION_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposal_emission_unresolved_continuation_v0.json"

REQUIRED_SOURCE_FILES = [
    PROPOSAL_EMISSION_REVIEW_RECEIPT_PATH,
    PROPOSAL_EMISSION_REVIEW_ASSESSMENT_PATH,
    PROPOSED_RECORD_INVENTORY_REVIEW_PATH,
    PROPOSED_RESOLUTION_REVIEW_PATH,
    EMISSION_ROUTE_REVIEW_PATH,
    EMISSION_GATE_REVIEW_PATH,
    BOUNDARY_REVIEW_PATH,
    C5_REVIEW_PATH,
    UNRESOLVED_REVIEW_PATH,
    CLOSURE_CANDIDATE_PATH,
    REVIEW_AUTHORITY_PATH,
    REVIEW_CLASSIFICATION_PATH,
    REVIEW_ROLLUP_PATH,
    REVIEW_PROFILE_PATH,
    REVIEW_REPORT_PATH,
    REVIEW_TRACE_PATH,
    PROPOSAL_EMISSION_RECEIPT_PATH,
    PROPOSAL_EMISSION_RECORD_PATH,
    PROPOSED_QA_RECORDS_PATH,
    PROPOSED_SOURCE_REF_RECORDS_PATH,
    PROPOSED_UNDERTYPED_RECORDS_PATH,
    PARKING_RECORDS_PATH,
    PROPOSED_RESOLUTION_RECORDS_PATH,
    EMISSION_ROUTE_MAP_PATH,
    EMISSION_GATE_READOUT_PATH,
    PROPOSAL_BOUNDARY_READOUT_PATH,
    C5_BLOCK_READOUT_PATH,
    UNRESOLVED_CONTINUATION_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0_receipts"

CLOSURE_RECORD_PATH = OUT_DIR / "o2_proposal_emission_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "o2_proposal_emission_reviewed_reference_v0.json"
PROPOSED_RECORD_FREEZE_PATH = OUT_DIR / "o2_proposed_record_inventory_freeze_v0.json"
PROPOSED_RESOLUTION_FREEZE_PATH = OUT_DIR / "o2_proposed_weak_feedback_resolution_record_freeze_v0.json"
EMISSION_ROUTE_FREEZE_PATH = OUT_DIR / "o2_proposal_emission_route_freeze_v0.json"
PROPOSAL_REVIEW_BOUNDARY_LOCK_PATH = OUT_DIR / "o2_proposal_review_boundary_lock_v0.json"
UNRESOLVED_STATUS_FREEZE_PATH = OUT_DIR / "o2_proposal_emission_unresolved_status_freeze_v0.json"
C5_BLOCK_FREEZE_PATH = OUT_DIR / "o2_proposal_emission_c5_block_freeze_v0.json"
RECEIPT_CHAIN_PATH = OUT_DIR / "o2_proposal_emission_receipt_chain_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o2_proposal_emission_closure_downstream_decision_table_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_proposal_emission_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_proposal_emission_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_proposal_emission_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_proposal_emission_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_proposal_emission_closure_report.json"
TRACE_PATH = OUT_DIR / "o2_proposal_emission_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REVIEWED_PROPOSED_RECORDS_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REVIEWED_PROPOSED_RECORDS_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_AS_REVIEWED_REFERENCE_V0"
RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REFERENCE_CLOSURE_V0"

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

    receipt = read_json(PROPOSAL_EMISSION_REVIEW_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_resolution_proposal_emission_review_summary", {})
    assessment = read_json(PROPOSAL_EMISSION_REVIEW_ASSESSMENT_PATH)
    inventory_review = read_json(PROPOSED_RECORD_INVENTORY_REVIEW_PATH)
    proposed_resolution_review = read_json(PROPOSED_RESOLUTION_REVIEW_PATH)
    emission_route_review = read_json(EMISSION_ROUTE_REVIEW_PATH)
    gate_review = read_json(EMISSION_GATE_REVIEW_PATH)
    boundary_review = read_json(BOUNDARY_REVIEW_PATH)
    c5_review = read_json(C5_REVIEW_PATH)
    unresolved_review = read_json(UNRESOLVED_REVIEW_PATH)
    closure_candidate = read_json(CLOSURE_CANDIDATE_PATH)
    review_authority = read_json(REVIEW_AUTHORITY_PATH)
    review_classification = read_json(REVIEW_CLASSIFICATION_PATH)
    review_rollup = read_json(REVIEW_ROLLUP_PATH)
    review_profile = read_json(REVIEW_PROFILE_PATH)
    review_report = read_json(REVIEW_REPORT_PATH)
    review_trace = read_json(REVIEW_TRACE_PATH)

    emission_receipt = read_json(PROPOSAL_EMISSION_RECEIPT_PATH)
    emission_record = read_json(PROPOSAL_EMISSION_RECORD_PATH)
    qa_records = read_jsonl(PROPOSED_QA_RECORDS_PATH)
    source_records = read_jsonl(PROPOSED_SOURCE_REF_RECORDS_PATH)
    undertyped_records = read_jsonl(PROPOSED_UNDERTYPED_RECORDS_PATH)
    parking_records = read_jsonl(PARKING_RECORDS_PATH)
    resolution_records = read_jsonl(PROPOSED_RESOLUTION_RECORDS_PATH)
    emission_routes = read_jsonl(EMISSION_ROUTE_MAP_PATH)
    gate_readout = read_json(EMISSION_GATE_READOUT_PATH)
    boundary_readout = read_json(PROPOSAL_BOUNDARY_READOUT_PATH)
    c5_readout = read_json(C5_BLOCK_READOUT_PATH)
    unresolved = read_json(UNRESOLVED_CONTINUATION_PATH)

    if receipt.get("receipt_id") != PROPOSAL_EMISSION_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("proposal_emission_review_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("proposal_emission_review_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("proposal_emission_review_hidden_next_command")
    if summary.get("status") != EXPECTED_REVIEW_STATUS:
        failures.append(f"proposal_emission_review_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append(f"proposal_emission_review_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "proposal_emission_review_complete",
        "proposal_emission_review_pass",
        "proposal_records_reviewed_for_emission_integrity",
        "closure_candidate_ready",
        "all_proposed_records_unreviewed",
        "proposed_records_remain_unreviewed",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "proposed_question_answer_records_reviewed_count": 3,
        "proposed_source_ref_satisfaction_records_reviewed_count": 2,
        "proposed_under_typed_acceptance_review_records_reviewed_count": 2,
        "parking_execution_continuation_records_reviewed_count": 3,
        "proposed_resolution_records_reviewed_count": 3,
        "proposal_emission_route_records_reviewed_count": 3,
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
    if assessment.get("closure_candidate_ready") is not True:
        failures.append("assessment_not_close_ready")
    if inventory_review.get("all_proposed_records_unreviewed") is not True:
        failures.append("inventory_not_unreviewed")
    if proposed_resolution_review.get("reviewed_resolution_records_emitted_count") != 0 or proposed_resolution_review.get("weak_feedback_resolved") is not False:
        failures.append("proposed_resolution_review_boundary_wrong")
    if emission_route_review.get("all_reviewed_record_emitted_false") is not True or emission_route_review.get("all_unresolved") is not True:
        failures.append("route_review_wrong")
    if gate_review.get("reviewed_resolution_records_emitted_count") != 0 or gate_review.get("closure_required_next") is not True:
        failures.append("gate_review_wrong")
    if boundary_review.get("proposal_layer_crossed_into_review_layer") is not False:
        failures.append("boundary_review_crossed")
    if c5_review.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_review.get("c5_opened") is not False:
        failures.append("c5_review_wrong")
    if unresolved_review.get("weak_feedback_resolved") is not False or unresolved_review.get("resolution_records_emitted_count") != 0:
        failures.append("unresolved_review_wrong")
    if closure_candidate.get("closure_candidate_status") != "PROPOSAL_EMISSION_CLOSE_READY_PROPOSED_RECORDS_UNREVIEWED":
        failures.append("closure_candidate_wrong")
    if review_authority.get("may_close_proposal_emission_as_reviewed_reference_next") is not True:
        failures.append("review_authority_no_close")
    if review_authority.get("may_emit_reviewed_resolution_records_now") is not False or review_authority.get("may_open_c5") is not False:
        failures.append("review_authority_allows_reviewed_or_c5")
    if review_classification.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append("review_classification_next_wrong")
    if review_rollup.get("closure_candidate_ready_count") != 1 or review_rollup.get("reviewed_resolution_records_emitted_count") != 0:
        failures.append("review_rollup_wrong")
    if review_profile.get("proposed_records_remain_unreviewed") is not True or review_profile.get("next_command_goal") is not None:
        failures.append("review_profile_wrong")
    if review_report.get("recommended_next_handling") != EXPECTED_REVIEW_NEXT:
        failures.append("review_report_next_wrong")
    if review_trace.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("review_trace_stop_wrong")

    if emission_receipt.get("receipt_id") != "1ddc557a":
        failures.append("emission_receipt_wrong")
    if emission_record.get("emission_status") != "PROPOSED_RECORDS_EMITTED_REVIEW_READY":
        failures.append("emission_record_wrong")
    if len(qa_records) != 3 or len(source_records) != 2 or len(undertyped_records) != 2 or len(parking_records) != 3 or len(resolution_records) != 3 or len(emission_routes) != 3:
        failures.append("source_record_counts_wrong")
    if gate_readout.get("reviewed_resolution_records_emitted_count") != 0:
        failures.append("gate_readout_reviewed_nonzero")
    if boundary_readout.get("proposal_layer_crossed_into_review_layer") is not False:
        failures.append("boundary_readout_crossed")
    if c5_readout.get("c5_opened") is not False:
        failures.append("c5_readout_wrong")
    if unresolved.get("weak_feedback_resolved") is not False:
        failures.append("unresolved_source_wrong")

    for row in qa_records:
        if row.get("review_status") != "UNREVIEWED" or row.get("counts_as_answer") is not False:
            failures.append(f"qa_record_promoted:{row.get('proposed_answer_id')}")
    for row in source_records:
        if row.get("review_status") != "UNREVIEWED" or row.get("counts_as_satisfied") is not False:
            failures.append(f"source_record_promoted:{row.get('proposed_satisfaction_id')}")
    for row in undertyped_records:
        if row.get("review_status") != "UNREVIEWED" or row.get("counts_as_approved") is not False:
            failures.append(f"undertyped_record_promoted:{row.get('proposed_review_id')}")
    for row in parking_records:
        if row.get("review_status") != "UNREVIEWED" or row.get("counts_as_resolution") is not False:
            failures.append(f"parking_record_promoted:{row.get('parking_execution_id')}")
    for row in resolution_records:
        if row.get("review_status") != "UNREVIEWED":
            failures.append(f"resolution_record_promoted:{row.get('proposed_resolution_id')}")
        if row.get("counts_as_reviewed_resolution") is not False or row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"resolution_record_boundary_wrong:{row.get('proposed_resolution_id')}")

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

    close_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED_DECISION_READY" if close_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if close_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_CLOSURE_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_CLOSED_AS_REVIEWED_REFERENCE",
        "PROPOSAL_EMISSION_REVIEW_RECEIPT_CONSUMED",
        "PROPOSED_RECORD_INVENTORY_FROZEN_UNREVIEWED",
        "PROPOSED_WEAK_FEEDBACK_RESOLUTION_RECORDS_FROZEN_UNREVIEWED",
        "PROPOSAL_EMISSION_ROUTE_MAP_FROZEN",
        "PROPOSAL_REVIEW_BOUNDARY_LOCKED_NOT_CROSSED",
        "UNRESOLVED_STATUS_FROZEN",
        "C5_BLOCK_STATUS_FROZEN",
        "POST_CLOSURE_DECISION_READY",
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
    ] if close_pass else failures

    closure_record = {
        "schema_version": "o2_proposal_emission_closure_record_v0",
        "closure_status": "CLOSED_AS_REVIEWED_REFERENCE_PROPOSED_RECORDS_UNREVIEWED" if close_pass else "CLOSURE_NOT_RECORDED",
        "source_proposal_emission_review_receipt_id": PROPOSAL_EMISSION_REVIEW_RECEIPT_ID,
        "closed_object": "o2_weak_feedback_resolution_proposal_emission_output_v0",
        "closure_meaning": "Proposal-emission output is frozen as a reviewed reference for emission integrity.",
        "closure_does_not_mean": [
            "proposed records are accepted as reviewed records",
            "reviewed resolution records exist",
            "weak feedback resolved",
            "C5 reconsideration ready",
            "C5 opened",
        ],
    }

    reviewed_reference = {
        "schema_version": "o2_proposal_emission_reviewed_reference_v0",
        "reference_status": "FROZEN_REVIEWED_REFERENCE_PROPOSED_RECORDS_UNREVIEWED" if close_pass else "REFERENCE_NOT_FROZEN",
        "reference_object_id": "o2_proposal_emission_reviewed_reference_" + sha8({
            "review_receipt": PROPOSAL_EMISSION_REVIEW_RECEIPT_ID,
            "qa": len(qa_records),
            "source": len(source_records),
            "undertyped": len(undertyped_records),
            "parking": len(parking_records),
            "resolution": len(resolution_records),
            "routes": len(emission_routes),
        }),
        "source_proposal_emission_receipt_id": "1ddc557a",
        "source_proposal_emission_review_receipt_id": PROPOSAL_EMISSION_REVIEW_RECEIPT_ID,
        "frozen_counts": {
            "proposed_question_answer_records": len(qa_records),
            "proposed_source_ref_satisfaction_records": len(source_records),
            "proposed_under_typed_acceptance_review_records": len(undertyped_records),
            "parking_execution_continuation_records": len(parking_records),
            "proposed_weak_feedback_resolution_records": len(resolution_records),
            "proposal_emission_route_records": len(emission_routes),
        },
        "proposed_records_exist": True,
        "proposed_records_remain_unreviewed": True,
        "proposal_review_boundary_crossed": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    proposed_record_freeze = {
        "schema_version": "o2_proposed_record_inventory_freeze_v0",
        "freeze_status": "PROPOSED_RECORDS_FROZEN_UNREVIEWED",
        "proposed_question_answer_records_frozen_count": len(qa_records),
        "proposed_source_ref_satisfaction_records_frozen_count": len(source_records),
        "proposed_under_typed_acceptance_review_records_frozen_count": len(undertyped_records),
        "parking_execution_continuation_records_frozen_count": len(parking_records),
        "proposed_weak_feedback_resolution_records_frozen_count": len(resolution_records),
        "all_proposed_records_unreviewed": True,
        "proposed_records_are_not_reviewed_records": True,
    }

    proposed_resolution_freeze = {
        "schema_version": "o2_proposed_weak_feedback_resolution_record_freeze_v0",
        "freeze_status": "PROPOSED_RESOLUTION_RECORDS_FROZEN_UNREVIEWED",
        "proposed_resolution_records_frozen_count": len(resolution_records),
        "reviewed_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_reconsideration_ready": False,
    }

    emission_route_freeze = {
        "schema_version": "o2_proposal_emission_route_freeze_v0",
        "freeze_status": "PROPOSAL_EMISSION_ROUTES_FROZEN_UNREVIEWED_UNRESOLVED",
        "proposal_emission_route_records_frozen_count": len(emission_routes),
        "all_proposed_record_emitted": True,
        "all_reviewed_record_emitted_false": True,
        "all_unresolved": True,
        "c5_reconsideration_ready": False,
    }

    boundary_lock = {
        "schema_version": "o2_proposal_review_boundary_lock_v0",
        "boundary_lock_status": "PROPOSAL_TO_REVIEW_BOUNDARY_LOCKED_NOT_CROSSED",
        "template_layer_crossed_into_proposal_layer": True,
        "proposal_layer_crossed_into_review_layer": False,
        "proposed_records_exist": True,
        "proposed_records_remain_unreviewed": True,
        "reviewed_resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
    }

    unresolved_freeze = {
        "schema_version": "o2_proposal_emission_unresolved_status_freeze_v0",
        "freeze_status": "UNRESOLVED_STATUS_FROZEN",
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
    }

    c5_freeze = {
        "schema_version": "o2_proposal_emission_c5_block_freeze_v0",
        "freeze_status": "C5_BLOCK_STATUS_FROZEN",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "closure_does_not_unblock_c5": True,
    }

    receipt_chain = {
        "schema_version": "o2_proposal_emission_receipt_chain_v0",
        "chain_status": "RECEIPT_CHAIN_PRESERVED",
        "receipts": [
            {"stage": "execution_target_post_closure_decision", "receipt_id": "1982e56e"},
            {"stage": "proposal_emission", "receipt_id": "1ddc557a"},
            {"stage": "proposal_emission_review", "receipt_id": PROPOSAL_EMISSION_REVIEW_RECEIPT_ID},
        ],
        "closure_receipt_pending": True,
    }

    downstream_decision_table = {
        "schema_version": "o2_proposal_emission_closure_downstream_decision_table_v0",
        "decision_status": "POST_CLOSURE_DECISION_READY" if close_pass else "CLOSURE_REPAIR_REQUIRED",
        "records": [
            {
                "decision": "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_REFERENCE_CLOSURE",
                "selected": close_pass,
                "next_unit": recommended_next if close_pass else None,
                "why": "Proposal-emission reference is closed, but all proposed records remain unreviewed and C5 remains blocked.",
            },
            {
                "decision": "PROMOTE_TO_REVIEWED_RESOLUTION_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Closure only freezes emission integrity. It does not accept proposed records as reviewed resolution.",
            },
            {
                "decision": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 remains blocked because no reviewed resolution exists.",
            },
        ],
    }

    authority_boundary = {
        "schema_version": "o2_proposal_emission_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_proposal_emission_reference_closure": close_pass,
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
        "schema_version": "o2_proposal_emission_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "proposal_emission_closed_as_reviewed_reference": close_pass,
        "reviewed_reference_emitted": close_pass,
        "post_closure_decision_ready": close_pass,
        "proposed_records_frozen_as_unreviewed": close_pass,
        "proposed_question_answer_records_frozen_count": len(qa_records),
        "proposed_source_ref_satisfaction_records_frozen_count": len(source_records),
        "proposed_under_typed_acceptance_review_records_frozen_count": len(undertyped_records),
        "parking_execution_continuation_records_frozen_count": len(parking_records),
        "proposed_resolution_records_frozen_count": len(resolution_records),
        "proposal_emission_route_records_frozen_count": len(emission_routes),
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
        "schema_version": "o2_proposal_emission_closure_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "closure_count": 1 if close_pass else 0,
        "reviewed_reference_emitted_count": 1 if close_pass else 0,
        "post_closure_decision_ready_count": 1 if close_pass else 0,
        "proposed_question_answer_records_frozen_count": len(qa_records),
        "proposed_source_ref_satisfaction_records_frozen_count": len(source_records),
        "proposed_under_typed_acceptance_review_records_frozen_count": len(undertyped_records),
        "parking_execution_continuation_records_frozen_count": len(parking_records),
        "proposed_resolution_records_frozen_count": len(resolution_records),
        "proposal_emission_route_records_frozen_count": len(emission_routes),
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
        "schema_version": "o2_proposal_emission_closure_profile_v0",
        "profile_id": "o2_proposal_emission_closure_profile_" + sha8(rollup),
        "status": status,
        "proposal_emission_closed_as_reviewed_reference": close_pass,
        "proposed_records_frozen_as_unreviewed": close_pass,
        "proposed_resolution_records_frozen_count": len(resolution_records),
        "reviewed_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Decide next after closing proposal-emission reference. Do not treat closure as reviewed resolution.",
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
        "schema_version": "o2_proposal_emission_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Proposal emission was closed as a reviewed reference for emission integrity. Proposed records are frozen as unreviewed; no reviewed resolution records exist; weak feedback remains unresolved; C5 remains blocked.",
        "proposed_resolution_records_frozen_count": len(resolution_records),
        "reviewed_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_proposal_emission_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_proposal_emission_review",
                "question": "is proposal emission reviewed clean and close-ready",
                "answer": "yes" if close_pass else "no",
                "taken": "freeze proposal emission as reviewed reference",
            },
            {
                "step": "freeze_proposed_record_boundary",
                "question": "does closure promote proposals into reviewed resolution records",
                "answer": "no",
                "taken": "freeze proposed records as unreviewed",
            },
            {
                "step": "preserve_unresolved_and_c5_block",
                "question": "does closure resolve weak feedback or open C5",
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
        (PROPOSED_RECORD_FREEZE_PATH, proposed_record_freeze),
        (PROPOSED_RESOLUTION_FREEZE_PATH, proposed_resolution_freeze),
        (EMISSION_ROUTE_FREEZE_PATH, emission_route_freeze),
        (PROPOSAL_REVIEW_BOUNDARY_LOCK_PATH, boundary_lock),
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
        "PROPOSAL_EMISSION_CLOSE_0_REVIEW_RECEIPT_CONSUMED": PROPOSAL_EMISSION_REVIEW_RECEIPT_PATH.exists(),
        "PROPOSAL_EMISSION_CLOSE_1_CLOSURE_RECORD_EMITTED": CLOSURE_RECORD_PATH.exists(),
        "PROPOSAL_EMISSION_CLOSE_2_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists(),
        "PROPOSAL_EMISSION_CLOSE_3_PROPOSED_RECORD_FREEZE_EMITTED": PROPOSED_RECORD_FREEZE_PATH.exists(),
        "PROPOSAL_EMISSION_CLOSE_4_PROPOSED_RESOLUTION_FREEZE_EMITTED": PROPOSED_RESOLUTION_FREEZE_PATH.exists(),
        "PROPOSAL_EMISSION_CLOSE_5_ROUTE_FREEZE_EMITTED": EMISSION_ROUTE_FREEZE_PATH.exists(),
        "PROPOSAL_EMISSION_CLOSE_6_BOUNDARY_LOCK_EMITTED": PROPOSAL_REVIEW_BOUNDARY_LOCK_PATH.exists(),
        "PROPOSAL_EMISSION_CLOSE_7_PROPOSED_RECORDS_STAY_UNREVIEWED": proposed_record_freeze["all_proposed_records_unreviewed"] is True,
        "PROPOSAL_EMISSION_CLOSE_8_NO_REVIEWED_RESOLUTION_RECORDS": proposed_resolution_freeze["reviewed_resolution_records_emitted_count"] == 0 and proposed_resolution_freeze["resolution_records_emitted_count"] == 0,
        "PROPOSAL_EMISSION_CLOSE_9_BOUNDARY_NOT_CROSSED": boundary_lock["proposal_layer_crossed_into_review_layer"] is False,
        "PROPOSAL_EMISSION_CLOSE_10_WEAK_FEEDBACK_NOT_RESOLVED": rollup["weak_feedback_resolved_count"] == 0,
        "PROPOSAL_EMISSION_CLOSE_11_C5_BLOCK_PRESERVED": c5_freeze["c5_opened"] is False and c5_freeze["c5_reconsideration_ready"] is False,
        "PROPOSAL_EMISSION_CLOSE_12_NO_ANSWER_SATISFY_APPROVE": rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "PROPOSAL_EMISSION_CLOSE_13_NO_PARKING_AS_RESOLUTION": rollup["parked_records_counted_as_resolved_count"] == 0,
        "PROPOSAL_EMISSION_CLOSE_14_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "PROPOSAL_EMISSION_CLOSE_15_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "PROPOSAL_EMISSION_CLOSE_16_POST_CLOSURE_DECISION_READY": rollup["post_closure_decision_ready_count"] == 1,
        "PROPOSAL_EMISSION_CLOSE_17_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "PROPOSAL_EMISSION_CLOSE_18_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "PROPOSAL_EMISSION_CLOSE_19_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "closed": close_pass,
        "reviewed_resolution_records": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_resolution_proposal_emission_closure_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_proposal_emission_review_receipt_id": PROPOSAL_EMISSION_REVIEW_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_resolution_proposal_emission_closure_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "proposal_emission_closed_as_reviewed_reference": close_pass,
            "reviewed_reference_emitted": close_pass,
            "post_closure_decision_ready": close_pass,
            "proposed_records_frozen_as_unreviewed": close_pass,
            "proposed_question_answer_records_frozen_count": len(qa_records),
            "proposed_source_ref_satisfaction_records_frozen_count": len(source_records),
            "proposed_under_typed_acceptance_review_records_frozen_count": len(undertyped_records),
            "parking_execution_continuation_records_frozen_count": len(parking_records),
            "proposed_resolution_records_frozen_count": len(resolution_records),
            "proposal_emission_route_records_frozen_count": len(emission_routes),
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
            "closure_record": rel(CLOSURE_RECORD_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "proposed_record_freeze": rel(PROPOSED_RECORD_FREEZE_PATH),
            "proposed_resolution_freeze": rel(PROPOSED_RESOLUTION_FREEZE_PATH),
            "emission_route_freeze": rel(EMISSION_ROUTE_FREEZE_PATH),
            "proposal_review_boundary_lock": rel(PROPOSAL_REVIEW_BOUNDARY_LOCK_PATH),
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
    print(f"proposal_emission_closure_receipt_id={receipt_id}")
    print(f"proposal_emission_closure_receipt_path={rel(receipt_path)}")
    print(f"proposal_emission_closure_record_path={rel(CLOSURE_RECORD_PATH)}")
    print(f"proposal_emission_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"proposed_record_inventory_freeze_path={rel(PROPOSED_RECORD_FREEZE_PATH)}")
    print(f"proposed_resolution_freeze_path={rel(PROPOSED_RESOLUTION_FREEZE_PATH)}")
    print(f"proposal_emission_route_freeze_path={rel(EMISSION_ROUTE_FREEZE_PATH)}")
    print(f"proposal_review_boundary_lock_path={rel(PROPOSAL_REVIEW_BOUNDARY_LOCK_PATH)}")
    print(f"proposal_emission_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"proposal_emission_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
