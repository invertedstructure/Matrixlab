#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_O2_WEAK_FEEDBACK_HANDLING_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_handling_closure.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_HANDLING_CLOSURE"
MODE = "CLOSE / FREEZE_REVIEWED_STATIC_HANDLING_REFERENCE / NO_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_HANDLING_CLOSURE_ONLY"

WFH_REVIEW_RECEIPT_ID = "a010297c"
WFH_REVIEW_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0_receipts/a010297c.json"
WFH_REVIEW_ASSESSMENT_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_handling_review_assessment_v0.json"
WFH_HANDLING_REVIEW_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_handling_record_review_v0.json"
WFH_QUESTION_REVIEW_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_question_packet_review_v0.json"
WFH_SOURCE_REF_REVIEW_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_source_ref_request_review_v0.json"
WFH_UNDERTYPED_REVIEW_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_under_typed_acceptance_candidate_review_v0.json"
WFH_PARKING_REVIEW_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_parking_review_v0.json"
WFH_C5_REVIEW_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_c5_block_review_v0.json"
WFH_UNRESOLVED_REVIEW_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_unresolved_status_review_v0.json"
WFH_CLOSURE_CANDIDATE_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_handling_closure_candidate_v0.json"
WFH_REVIEW_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_handling_review_authority_boundary_v0.json"
WFH_REVIEW_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_handling_review_classification_v0.json"
WFH_REVIEW_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_handling_review_rollup_v0.json"
WFH_REVIEW_PROFILE_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_handling_review_profile_v0.json"
WFH_REVIEW_REPORT_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_handling_review_report.json"
WFH_REVIEW_TRACE_PATH = ROOT / "data/o2_weak_feedback_handling_review_v0/o2_weak_feedback_handling_review_transition_trace.json"

WFH_BUILD_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_handling_v0_receipts/50e2e4a1.json"
WFH_HANDLING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_records_v0.jsonl"
WFH_QUESTION_PACKETS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_question_packets_v0.jsonl"
WFH_SOURCE_REF_REQUESTS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_source_ref_requests_v0.jsonl"
WFH_UNDERTYPED_CANDIDATES_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_under_typed_acceptance_candidates_v0.jsonl"
WFH_PARKING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_parking_records_v0.jsonl"
WFH_C5_BLOCK_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_c5_block_records_v0.jsonl"
WFH_BUILD_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_rollup_v0.json"
WFH_BUILD_READOUT_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_readout_v0.json"
WFH_BUILD_PROFILE_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_profile_v0.json"
WFH_BUILD_REPORT_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_report.json"

O2_C5_BLOCK_STATUS_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_c5_block_status_v0.json"
O2_WEAK_FEEDBACK_NOTE_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_weak_feedback_note_v0.json"

REQUIRED_SOURCE_FILES = [
    WFH_REVIEW_RECEIPT_PATH,
    WFH_REVIEW_ASSESSMENT_PATH,
    WFH_HANDLING_REVIEW_PATH,
    WFH_QUESTION_REVIEW_PATH,
    WFH_SOURCE_REF_REVIEW_PATH,
    WFH_UNDERTYPED_REVIEW_PATH,
    WFH_PARKING_REVIEW_PATH,
    WFH_C5_REVIEW_PATH,
    WFH_UNRESOLVED_REVIEW_PATH,
    WFH_CLOSURE_CANDIDATE_PATH,
    WFH_REVIEW_AUTHORITY_PATH,
    WFH_REVIEW_CLASSIFICATION_PATH,
    WFH_REVIEW_ROLLUP_PATH,
    WFH_REVIEW_PROFILE_PATH,
    WFH_REVIEW_REPORT_PATH,
    WFH_REVIEW_TRACE_PATH,
    WFH_BUILD_RECEIPT_PATH,
    WFH_HANDLING_RECORDS_PATH,
    WFH_QUESTION_PACKETS_PATH,
    WFH_SOURCE_REF_REQUESTS_PATH,
    WFH_UNDERTYPED_CANDIDATES_PATH,
    WFH_PARKING_RECORDS_PATH,
    WFH_C5_BLOCK_RECORDS_PATH,
    WFH_BUILD_ROLLUP_PATH,
    WFH_BUILD_READOUT_PATH,
    WFH_BUILD_PROFILE_PATH,
    WFH_BUILD_REPORT_PATH,
    O2_C5_BLOCK_STATUS_PATH,
    O2_WEAK_FEEDBACK_NOTE_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_handling_closure_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_handling_closure_v0_receipts"

CLOSURE_RECORD_PATH = OUT_DIR / "o2_weak_feedback_handling_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "o2_weak_feedback_handling_reviewed_reference_v0.json"
UNRESOLVED_STATUS_FREEZE_PATH = OUT_DIR / "o2_weak_feedback_unresolved_status_freeze_v0.json"
QUESTION_PACKET_FREEZE_PATH = OUT_DIR / "o2_question_packet_candidate_freeze_v0.json"
SOURCE_REF_FREEZE_PATH = OUT_DIR / "o2_source_ref_request_candidate_freeze_v0.json"
UNDERTYPED_ACCEPTANCE_FREEZE_PATH = OUT_DIR / "o2_under_typed_acceptance_candidate_freeze_v0.json"
PARKING_FREEZE_PATH = OUT_DIR / "o2_weak_feedback_parking_not_resolution_freeze_v0.json"
C5_BLOCK_FREEZE_PATH = OUT_DIR / "o2_weak_feedback_c5_block_freeze_v0.json"
RECEIPT_CHAIN_PATH = OUT_DIR / "o2_weak_feedback_handling_receipt_chain_v0.json"
BOUNDARY_LOCK_PATH = OUT_DIR / "o2_weak_feedback_handling_closure_boundary_lock_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o2_weak_feedback_handling_closure_downstream_decision_table_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_weak_feedback_handling_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_weak_feedback_handling_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_weak_feedback_handling_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_weak_feedback_handling_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_weak_feedback_handling_closure_report.json"
TRACE_PATH = OUT_DIR / "o2_weak_feedback_handling_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_O2_WEAK_FEEDBACK_HANDLING_REVIEWED_STATIC_RECORDS_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_HANDLING_REVIEWED_STATIC_RECORDS_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_O2_WEAK_FEEDBACK_HANDLING_AS_REVIEWED_REFERENCE_V0"

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

    review_receipt = read_json(WFH_REVIEW_RECEIPT_PATH)
    summary = review_receipt.get("machine_readable_o2_weak_feedback_handling_review_summary", {})
    review_assessment = read_json(WFH_REVIEW_ASSESSMENT_PATH)
    closure_candidate = read_json(WFH_CLOSURE_CANDIDATE_PATH)
    authority = read_json(WFH_REVIEW_AUTHORITY_PATH)
    rollup = read_json(WFH_REVIEW_ROLLUP_PATH)
    profile = read_json(WFH_REVIEW_PROFILE_PATH)
    report = read_json(WFH_REVIEW_REPORT_PATH)
    trace = read_json(WFH_REVIEW_TRACE_PATH)

    handling = read_jsonl(WFH_HANDLING_RECORDS_PATH)
    questions = read_jsonl(WFH_QUESTION_PACKETS_PATH)
    source_refs = read_jsonl(WFH_SOURCE_REF_REQUESTS_PATH)
    acceptances = read_jsonl(WFH_UNDERTYPED_CANDIDATES_PATH)
    parking = read_jsonl(WFH_PARKING_RECORDS_PATH)
    c5_blocks = read_jsonl(WFH_C5_BLOCK_RECORDS_PATH)

    build_receipt = read_json(WFH_BUILD_RECEIPT_PATH)
    build_rollup = read_json(WFH_BUILD_ROLLUP_PATH)
    build_readout = read_json(WFH_BUILD_READOUT_PATH)
    build_profile = read_json(WFH_BUILD_PROFILE_PATH)

    o2_c5_status = read_json(O2_C5_BLOCK_STATUS_PATH)
    o2_weak_note = read_json(O2_WEAK_FEEDBACK_NOTE_PATH)

    if review_receipt.get("receipt_id") != WFH_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("weak_feedback_handling_review_receipt_not_pass")
    if review_receipt.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("weak_feedback_handling_review_terminal_not_expected")
    if review_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("weak_feedback_handling_review_hidden_next_command")
    if summary.get("status") != EXPECTED_REVIEW_STATUS:
        failures.append(f"weak_feedback_handling_review_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append(f"weak_feedback_handling_review_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "review_complete",
        "review_pass",
        "handling_records_unresolved",
        "question_packets_proposed_only",
        "source_ref_requests_candidate_only",
        "under_typed_acceptance_candidate_only",
        "parking_not_resolution",
        "c5_block_preserved",
        "closure_candidate_ready",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    for key in [
        "weak_feedback_resolved",
        "question_packets_answered",
        "source_ref_requests_satisfied",
        "under_typed_acceptance_approved",
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

    expected_counts = {
        "weak_records_reviewed_count": 3,
        "question_packets_reviewed_count": 3,
        "source_ref_requests_reviewed_count": 2,
        "under_typed_acceptance_candidates_reviewed_count": 2,
        "parking_records_reviewed_count": 3,
        "c5_block_records_reviewed_count": 3,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"review_count_wrong:{key}:{summary.get(key)}")

    if summary.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("summary_c5_not_blocked")
    if review_assessment.get("closure_candidate_ready") is not True:
        failures.append("assessment_closure_not_ready")
    if closure_candidate.get("closure_candidate_status") != "WEAK_FEEDBACK_HANDLING_CLOSE_READY_UNRESOLVED":
        failures.append("closure_candidate_not_ready")
    if authority.get("may_close_weak_feedback_handling_as_reviewed_reference_next") is not True:
        failures.append("authority_does_not_allow_closure")
    if authority.get("may_open_c5") is not False:
        failures.append("authority_allows_c5")
    if rollup.get("closure_candidate_ready_count") != 1:
        failures.append("rollup_closure_candidate_wrong")
    if profile.get("closure_candidate_ready") is not True:
        failures.append("profile_closure_candidate_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    if report.get("recommended_next_handling") != EXPECTED_REVIEW_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("trace_stop_wrong")

    if build_receipt.get("receipt_id") != "50e2e4a1":
        failures.append("build_receipt_wrong")
    if build_rollup.get("weak_records_handled_count") != 3:
        failures.append("build_rollup_handled_wrong")
    if build_readout.get("weak_feedback_resolved") is not False:
        failures.append("build_readout_resolved")
    if build_profile.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("build_profile_c5_wrong")

    if len(handling) != 3 or len(questions) != 3 or len(source_refs) != 2 or len(acceptances) != 2 or len(parking) != 3 or len(c5_blocks) != 3:
        failures.append("source_artifact_counts_wrong")

    for rec in handling:
        if rec.get("resolution_status") != "UNRESOLVED":
            failures.append(f"handling_record_resolved:{rec.get('handling_record_id')}")
        if rec.get("c5_block_preserved") is not True:
            failures.append(f"handling_c5_not_preserved:{rec.get('handling_record_id')}")
    for rec in questions:
        if rec.get("status") != "PROPOSED_ONLY":
            failures.append(f"question_not_proposed_only:{rec.get('question_packet_id')}")
    for rec in source_refs:
        if rec.get("status") != "REQUEST_CANDIDATE_ONLY":
            failures.append(f"source_ref_not_candidate:{rec.get('source_ref_request_id')}")
    for rec in acceptances:
        if rec.get("status") != "CANDIDATE_ONLY":
            failures.append(f"acceptance_not_candidate:{rec.get('acceptance_candidate_id')}")
        if rec.get("c5_unblock_allowed") is not False:
            failures.append(f"acceptance_unblocks_c5:{rec.get('acceptance_candidate_id')}")
    for rec in parking:
        if rec.get("status") != "PARKED_WITH_REASON":
            failures.append(f"parking_status_wrong:{rec.get('parking_id')}")
    for rec in c5_blocks:
        if rec.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or rec.get("c5_opened") is not False:
            failures.append(f"c5_block_wrong:{rec.get('c5_block_record_id')}")

    if o2_c5_status.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("source_c5_status_wrong")
    if o2_weak_note.get("weak_feedback_count") != 3:
        failures.append("source_weak_note_count_wrong")

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

    closure_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_HANDLING_CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED_DECISION_READY" if closure_pass else "TYPED_O2_WEAK_FEEDBACK_HANDLING_CLOSURE_GATE_FAIL"
    recommended_next = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_HANDLING_REFERENCE_CLOSURE_V0" if closure_pass else "REPAIR_O2_WEAK_FEEDBACK_HANDLING_CLOSURE_V0"

    reason_codes = [
        "WEAK_FEEDBACK_HANDLING_CLOSED_AS_REVIEWED_REFERENCE",
        "WEAK_FEEDBACK_HANDLING_REVIEW_RECEIPT_CONSUMED",
        "REVIEWED_STATIC_HANDLING_RECORDS_FROZEN",
        "QUESTION_PACKET_CANDIDATES_FROZEN_PROPOSED_ONLY",
        "SOURCE_REF_REQUESTS_FROZEN_CANDIDATE_ONLY",
        "UNDER_TYPED_ACCEPTANCE_FROZEN_CANDIDATE_ONLY",
        "PARKING_NOT_RESOLUTION_FROZEN",
        "C5_BLOCK_RECORDS_FROZEN",
        "WEAK_FEEDBACK_UNRESOLVED_STATUS_FROZEN",
        "C5_REMAINS_BLOCKED_BY_WEAK_FEEDBACK",
        "POST_CLOSURE_DECISION_READY",
        "NO_QUESTION_PACKET_ANSWERED",
        "NO_SOURCE_REF_REQUEST_SATISFIED",
        "NO_UNDER_TYPED_ACCEPTANCE_APPROVED",
        "NO_WEAK_FEEDBACK_RESOLUTION_ATTEMPTED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_TARGET_SELECTED_FOR_BUILD",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
        "NO_C5_OPENED",
    ] if closure_pass else failures

    closure_record = {
        "schema_version": "o2_weak_feedback_handling_closure_record_v0",
        "closure_status": "CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED" if closure_pass else "CLOSURE_NOT_RECORDED",
        "source_review_receipt_id": WFH_REVIEW_RECEIPT_ID,
        "closed_object": "o2_weak_feedback_handling_static_records_v0",
        "closure_meaning": "Static weak-feedback handling records are frozen as a reviewed reference while weak feedback remains unresolved.",
        "closure_does_not_mean": [
            "weak feedback resolved",
            "question packets answered",
            "source-ref requests satisfied",
            "under-typed acceptance approved",
            "parking counted as resolution",
            "C5 unblocked",
        ],
    }

    reviewed_reference = {
        "schema_version": "o2_weak_feedback_handling_reviewed_reference_v0",
        "reference_status": "FROZEN_REVIEWED_REFERENCE" if closure_pass else "REFERENCE_NOT_FROZEN",
        "reference_object_id": "o2_wfh_reviewed_reference_" + sha8({
            "review_receipt": WFH_REVIEW_RECEIPT_ID,
            "handling": len(handling),
            "questions": len(questions),
            "source_refs": len(source_refs),
            "acceptances": len(acceptances),
            "parking": len(parking),
            "c5": len(c5_blocks),
        }),
        "source_review_receipt_id": WFH_REVIEW_RECEIPT_ID,
        "source_build_receipt_id": "50e2e4a1",
        "source_target_design_receipt_id": "90309841",
        "reviewed_surfaces": {
            "handling_records": len(handling),
            "question_packet_candidates": len(questions),
            "source_ref_request_candidates": len(source_refs),
            "under_typed_acceptance_candidates": len(acceptances),
            "parking_records": len(parking),
            "c5_block_records": len(c5_blocks),
        },
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "reference_use": "future units may cite this reviewed weak-feedback handling reference surface before any resolution, answer, satisfaction, acceptance, or C5-unblock decision.",
    }

    unresolved_status_freeze = {
        "schema_version": "o2_weak_feedback_unresolved_status_freeze_v0",
        "freeze_status": "UNRESOLVED_STATUS_FROZEN",
        "weak_records_frozen": len(handling),
        "weak_feedback_resolved": False,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "meaning": "Handling is reviewed. Resolution has not occurred.",
    }

    question_packet_freeze = {
        "schema_version": "o2_question_packet_candidate_freeze_v0",
        "freeze_status": "QUESTION_PACKETS_FROZEN_PROPOSED_ONLY",
        "question_packet_count": len(questions),
        "all_proposed_only": all(q.get("status") == "PROPOSED_ONLY" for q in questions),
        "answered_count": 0,
        "c5_block_preserved": True,
    }

    source_ref_freeze = {
        "schema_version": "o2_source_ref_request_candidate_freeze_v0",
        "freeze_status": "SOURCE_REF_REQUESTS_FROZEN_CANDIDATE_ONLY",
        "source_ref_request_count": len(source_refs),
        "all_candidate_only": all(r.get("status") == "REQUEST_CANDIDATE_ONLY" for r in source_refs),
        "satisfied_count": 0,
    }

    undertyped_acceptance_freeze = {
        "schema_version": "o2_under_typed_acceptance_candidate_freeze_v0",
        "freeze_status": "UNDER_TYPED_ACCEPTANCE_FROZEN_CANDIDATE_ONLY",
        "under_typed_acceptance_candidate_count": len(acceptances),
        "all_candidate_only": all(a.get("status") == "CANDIDATE_ONLY" for a in acceptances),
        "approved_count": 0,
        "c5_unblock_allowed_count": 0,
    }

    parking_freeze = {
        "schema_version": "o2_weak_feedback_parking_not_resolution_freeze_v0",
        "freeze_status": "PARKING_NOT_RESOLUTION_FROZEN",
        "parking_records_count": len(parking),
        "parking_counted_as_resolution": False,
    }

    c5_block_freeze = {
        "schema_version": "o2_weak_feedback_c5_block_freeze_v0",
        "freeze_status": "C5_BLOCK_FROZEN",
        "c5_block_records_count": len(c5_blocks),
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_opened": False,
        "closure_does_not_unblock_c5": True,
    }

    receipt_chain = {
        "schema_version": "o2_weak_feedback_handling_receipt_chain_v0",
        "chain_status": "RECEIPT_CHAIN_PRESERVED",
        "receipts": [
            {"stage": "o2_closure", "receipt_id": "bf5163d7"},
            {"stage": "post_o2_decision", "receipt_id": "2fef4830"},
            {"stage": "weak_feedback_target_design", "receipt_id": "90309841"},
            {"stage": "weak_feedback_handling_build", "receipt_id": "50e2e4a1"},
            {"stage": "weak_feedback_handling_review", "receipt_id": WFH_REVIEW_RECEIPT_ID},
        ],
        "closure_receipt_pending": True,
    }

    boundary_lock = {
        "schema_version": "o2_weak_feedback_handling_closure_boundary_lock_v0",
        "boundary_lock_status": "BOUNDARIES_LOCKED_AT_CLOSURE",
        "weak_feedback_handling_closed_as_reviewed_reference": closure_pass,
        "weak_feedback_resolved": False,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "live_feedback_audit_executed": False,
        "repair_applied": False,
        "retry_executed": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "architecture_change": False,
        "c5_opened": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
    }

    downstream_decision_table = {
        "schema_version": "o2_weak_feedback_handling_closure_downstream_decision_table_v0",
        "decision_status": "POST_CLOSURE_DECISION_READY" if closure_pass else "CLOSURE_REPAIR_REQUIRED",
        "records": [
            {
                "decision": "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_HANDLING_REFERENCE_CLOSURE",
                "selected": closure_pass,
                "next_unit": recommended_next if closure_pass else None,
                "why": "Reviewed handling reference is closed, but weak feedback remains unresolved and C5 is still blocked.",
            },
            {
                "decision": "RESOLVE_WEAK_FEEDBACK_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Closure freezes reviewed handling. Resolution requires explicit later decision/build/review path.",
            },
            {
                "decision": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 remains blocked by weak feedback.",
            },
        ],
    }

    authority_boundary = {
        "schema_version": "o2_weak_feedback_handling_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_weak_feedback_handling_reference_closure": closure_pass,
        "may_resolve_weak_feedback_now": False,
        "may_answer_question_packets": False,
        "may_satisfy_source_ref_requests": False,
        "may_approve_under_typed_acceptance": False,
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
        "schema_version": "o2_weak_feedback_handling_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "weak_feedback_handling_closed_as_reviewed_reference": closure_pass,
        "reviewed_reference_emitted": closure_pass,
        "weak_feedback_resolved": False,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_opened": False,
        "post_closure_decision_ready": closure_pass,
        "recommended_next": recommended_next,
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
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "o2_weak_feedback_handling_closure_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "closure_count": 1 if closure_pass else 0,
        "reviewed_reference_emitted_count": 1 if closure_pass else 0,
        "handling_records_frozen_count": len(handling),
        "question_packet_candidates_frozen_count": len(questions),
        "source_ref_request_candidates_frozen_count": len(source_refs),
        "under_typed_acceptance_candidates_frozen_count": len(acceptances),
        "parking_records_frozen_count": len(parking),
        "c5_block_records_frozen_count": len(c5_blocks),
        "post_closure_decision_ready_count": 1 if closure_pass else 0,
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
        "schema_version": "o2_weak_feedback_handling_closure_profile_v0",
        "profile_id": "o2_wfh_closure_profile_" + sha8(rollup),
        "status": status,
        "weak_feedback_handling_closed_as_reviewed_reference": closure_pass,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "post_closure_decision_ready": closure_pass,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Decide next after weak-feedback handling closure; do not treat closure as resolution.",
        "must_not_infer": [
            "weak feedback resolved",
            "question packets answered",
            "source-ref requests satisfied",
            "under-typed acceptance approved",
            "parking resolved weak feedback",
            "C5 opened",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_weak_feedback_handling_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The O2 weak-feedback handling layer was closed as a reviewed reference. Reviewed static handling records, proposed-only question packets, candidate-only source-ref requests, candidate-only under-typed acceptance records, parking-not-resolution records, C5 block records, and unresolved weak-feedback status were frozen. Closure did not resolve weak feedback, answer questions, satisfy source-ref requests, approve under-typed acceptance, count parking as resolution, run live audit, repair, retry, select target, patch runtime, mutate sources, or open C5.",
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_weak_feedback_handling_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_handling_review",
                "question": "is weak-feedback handling reviewed clean and close-ready",
                "answer": "yes" if closure_pass else "no",
                "taken": "freeze reviewed handling reference",
            },
            {
                "step": "preserve_unresolved_status",
                "question": "did closure resolve any weak feedback",
                "answer": "no",
                "taken": "freeze unresolved status",
            },
            {
                "step": "preserve_c5_block",
                "question": "is C5 still blocked",
                "answer": "yes",
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
        (UNRESOLVED_STATUS_FREEZE_PATH, unresolved_status_freeze),
        (QUESTION_PACKET_FREEZE_PATH, question_packet_freeze),
        (SOURCE_REF_FREEZE_PATH, source_ref_freeze),
        (UNDERTYPED_ACCEPTANCE_FREEZE_PATH, undertyped_acceptance_freeze),
        (PARKING_FREEZE_PATH, parking_freeze),
        (C5_BLOCK_FREEZE_PATH, c5_block_freeze),
        (RECEIPT_CHAIN_PATH, receipt_chain),
        (BOUNDARY_LOCK_PATH, boundary_lock),
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
        "WFH_CLOSE_0_REVIEW_RECEIPT_CONSUMED": WFH_REVIEW_RECEIPT_PATH.exists(),
        "WFH_CLOSE_1_CLOSURE_RECORD_EMITTED": CLOSURE_RECORD_PATH.exists(),
        "WFH_CLOSE_2_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists(),
        "WFH_CLOSE_3_UNRESOLVED_STATUS_FROZEN": UNRESOLVED_STATUS_FREEZE_PATH.exists() and unresolved_status_freeze["weak_feedback_resolved"] is False,
        "WFH_CLOSE_4_QUESTION_PACKETS_FROZEN_PROPOSED_ONLY": QUESTION_PACKET_FREEZE_PATH.exists() and question_packet_freeze["all_proposed_only"] is True,
        "WFH_CLOSE_5_SOURCE_REF_REQUESTS_FROZEN_CANDIDATE_ONLY": SOURCE_REF_FREEZE_PATH.exists() and source_ref_freeze["all_candidate_only"] is True,
        "WFH_CLOSE_6_UNDER_TYPED_ACCEPTANCE_FROZEN_CANDIDATE_ONLY": UNDERTYPED_ACCEPTANCE_FREEZE_PATH.exists() and undertyped_acceptance_freeze["all_candidate_only"] is True,
        "WFH_CLOSE_7_PARKING_NOT_RESOLUTION_FROZEN": PARKING_FREEZE_PATH.exists() and parking_freeze["parking_counted_as_resolution"] is False,
        "WFH_CLOSE_8_C5_BLOCK_FROZEN": C5_BLOCK_FREEZE_PATH.exists() and c5_block_freeze["c5_opened"] is False,
        "WFH_CLOSE_9_NO_WEAK_FEEDBACK_RESOLUTION": rollup["weak_feedback_resolved_count"] == 0,
        "WFH_CLOSE_10_NO_QUESTION_ANSWERED": rollup["question_packets_answered_count"] == 0,
        "WFH_CLOSE_11_NO_SOURCE_REF_SATISFIED": rollup["source_ref_requests_satisfied_count"] == 0,
        "WFH_CLOSE_12_NO_ACCEPTANCE_APPROVED": rollup["under_typed_acceptance_approved_count"] == 0,
        "WFH_CLOSE_13_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "WFH_CLOSE_14_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "WFH_CLOSE_15_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "WFH_CLOSE_16_POST_CLOSURE_DECISION_READY": rollup["post_closure_decision_ready_count"] == 1,
        "WFH_CLOSE_17_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "WFH_CLOSE_18_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "WFH_CLOSE_19_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_HANDLING_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "closed": closure_pass,
        "unresolved": True,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_handling_closure_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_HANDLING_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_weak_feedback_handling_review_receipt_id": WFH_REVIEW_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_handling_closure_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "weak_feedback_handling_closed_as_reviewed_reference": closure_pass,
            "reviewed_reference_emitted": closure_pass,
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
            "post_closure_decision_ready": closure_pass,
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
            "unresolved_status_freeze": rel(UNRESOLVED_STATUS_FREEZE_PATH),
            "question_packet_freeze": rel(QUESTION_PACKET_FREEZE_PATH),
            "source_ref_request_freeze": rel(SOURCE_REF_FREEZE_PATH),
            "under_typed_acceptance_freeze": rel(UNDERTYPED_ACCEPTANCE_FREEZE_PATH),
            "parking_freeze": rel(PARKING_FREEZE_PATH),
            "c5_block_freeze": rel(C5_BLOCK_FREEZE_PATH),
            "receipt_chain": rel(RECEIPT_CHAIN_PATH),
            "boundary_lock": rel(BOUNDARY_LOCK_PATH),
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
    print(f"weak_feedback_handling_closure_receipt_id={receipt_id}")
    print(f"weak_feedback_handling_closure_receipt_path={rel(receipt_path)}")
    print(f"weak_feedback_handling_closure_record_path={rel(CLOSURE_RECORD_PATH)}")
    print(f"weak_feedback_handling_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"weak_feedback_unresolved_status_freeze_path={rel(UNRESOLVED_STATUS_FREEZE_PATH)}")
    print(f"question_packet_candidate_freeze_path={rel(QUESTION_PACKET_FREEZE_PATH)}")
    print(f"source_ref_request_candidate_freeze_path={rel(SOURCE_REF_FREEZE_PATH)}")
    print(f"under_typed_acceptance_candidate_freeze_path={rel(UNDERTYPED_ACCEPTANCE_FREEZE_PATH)}")
    print(f"weak_feedback_c5_block_freeze_path={rel(C5_BLOCK_FREEZE_PATH)}")
    print(f"weak_feedback_handling_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"weak_feedback_handling_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
