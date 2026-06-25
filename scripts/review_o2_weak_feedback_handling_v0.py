#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_O2_WEAK_FEEDBACK_HANDLING_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_handling_review.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_HANDLING_REVIEW"
MODE = "REVIEW / STATIC_WEAK_FEEDBACK_HANDLING / NO_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_HANDLING_REVIEW_ONLY"

WFH_BUILD_RECEIPT_ID = "50e2e4a1"
WFH_BUILD_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_handling_v0_receipts/50e2e4a1.json"
WFH_HANDLING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_records_v0.jsonl"
WFH_QUESTION_PACKETS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_question_packets_v0.jsonl"
WFH_SOURCE_REF_REQUESTS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_source_ref_requests_v0.jsonl"
WFH_UNDERTYPED_CANDIDATES_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_under_typed_acceptance_candidates_v0.jsonl"
WFH_PARKING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_parking_records_v0.jsonl"
WFH_C5_BLOCK_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_c5_block_records_v0.jsonl"
WFH_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_rollup_v0.json"
WFH_READOUT_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_readout_v0.json"
WFH_PROFILE_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_profile_v0.json"
WFH_REPORT_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_report.json"
WFH_TRACE_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_transition_trace.json"

WFH_DESIGN_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0_receipts/90309841.json"
WFH_TARGET_DEFINITION_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_handling_target_definition_v0.json"
WFH_INVENTORY_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_record_inventory_v0.json"
WFH_C5_BLOCK_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_handling_target_v0/o2_weak_feedback_c5_block_contract_v0.json"
O2_WEAK_FEEDBACK_NOTE_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_weak_feedback_note_v0.json"
O2_C5_BLOCK_STATUS_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_c5_block_status_v0.json"

REQUIRED_SOURCE_FILES = [
    WFH_BUILD_RECEIPT_PATH,
    WFH_HANDLING_RECORDS_PATH,
    WFH_QUESTION_PACKETS_PATH,
    WFH_SOURCE_REF_REQUESTS_PATH,
    WFH_UNDERTYPED_CANDIDATES_PATH,
    WFH_PARKING_RECORDS_PATH,
    WFH_C5_BLOCK_RECORDS_PATH,
    WFH_ROLLUP_PATH,
    WFH_READOUT_PATH,
    WFH_PROFILE_PATH,
    WFH_REPORT_PATH,
    WFH_TRACE_PATH,
    WFH_DESIGN_RECEIPT_PATH,
    WFH_TARGET_DEFINITION_PATH,
    WFH_INVENTORY_PATH,
    WFH_C5_BLOCK_CONTRACT_PATH,
    O2_WEAK_FEEDBACK_NOTE_PATH,
    O2_C5_BLOCK_STATUS_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_handling_review_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_handling_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "o2_weak_feedback_handling_review_assessment_v0.json"
HANDLING_RECORD_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_handling_record_review_v0.json"
QUESTION_PACKET_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_question_packet_review_v0.json"
SOURCE_REF_REQUEST_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_source_ref_request_review_v0.json"
UNDERTYPED_ACCEPTANCE_REVIEW_PATH = OUT_DIR / "o2_under_typed_acceptance_candidate_review_v0.json"
PARKING_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_parking_review_v0.json"
C5_BLOCK_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_c5_block_review_v0.json"
UNRESOLVED_STATUS_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_unresolved_status_review_v0.json"
CLOSURE_CANDIDATE_PATH = OUT_DIR / "o2_weak_feedback_handling_closure_candidate_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o2_weak_feedback_handling_review_downstream_decision_table_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_weak_feedback_handling_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_weak_feedback_handling_review_classification_v0.json"
ROLLUP_OUT_PATH = OUT_DIR / "o2_weak_feedback_handling_review_rollup_v0.json"
PROFILE_OUT_PATH = OUT_DIR / "o2_weak_feedback_handling_review_profile_v0.json"
REPORT_OUT_PATH = OUT_DIR / "o2_weak_feedback_handling_review_report.json"
TRACE_OUT_PATH = OUT_DIR / "o2_weak_feedback_handling_review_transition_trace.json"

EXPECTED_BUILD_STATUS = "TYPED_O2_WEAK_FEEDBACK_HANDLING_STATIC_RECORDS_EMITTED_REVIEW_READY"
EXPECTED_BUILD_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_HANDLING_STATIC_RECORDS_EMITTED_REVIEW_READY"
EXPECTED_BUILD_NEXT = "REVIEW_O2_WEAK_FEEDBACK_HANDLING_V0"

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

    build_receipt = read_json(WFH_BUILD_RECEIPT_PATH)
    summary = build_receipt.get("machine_readable_o2_weak_feedback_handling_summary", {})
    handling = read_jsonl(WFH_HANDLING_RECORDS_PATH)
    questions = read_jsonl(WFH_QUESTION_PACKETS_PATH)
    source_refs = read_jsonl(WFH_SOURCE_REF_REQUESTS_PATH)
    acceptances = read_jsonl(WFH_UNDERTYPED_CANDIDATES_PATH)
    parking = read_jsonl(WFH_PARKING_RECORDS_PATH)
    c5_blocks = read_jsonl(WFH_C5_BLOCK_RECORDS_PATH)
    rollup = read_json(WFH_ROLLUP_PATH)
    readout = read_json(WFH_READOUT_PATH)
    profile = read_json(WFH_PROFILE_PATH)
    report = read_json(WFH_REPORT_PATH)
    trace = read_json(WFH_TRACE_PATH)
    design_receipt = read_json(WFH_DESIGN_RECEIPT_PATH)
    target_definition = read_json(WFH_TARGET_DEFINITION_PATH)
    inventory = read_json(WFH_INVENTORY_PATH)
    c5_contract = read_json(WFH_C5_BLOCK_CONTRACT_PATH)
    weak_note = read_json(O2_WEAK_FEEDBACK_NOTE_PATH)
    c5_status = read_json(O2_C5_BLOCK_STATUS_PATH)

    if build_receipt.get("receipt_id") != WFH_BUILD_RECEIPT_ID or build_receipt.get("gate") != "PASS":
        failures.append("weak_feedback_handling_build_receipt_not_pass")
    if build_receipt.get("terminal", {}).get("stop_code") != EXPECTED_BUILD_STOP:
        failures.append("weak_feedback_handling_terminal_not_expected")
    if build_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("weak_feedback_handling_hidden_next_command")
    if summary.get("status") != EXPECTED_BUILD_STATUS:
        failures.append(f"weak_feedback_handling_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_BUILD_NEXT:
        failures.append(f"weak_feedback_handling_next_not_expected:{summary.get('recommended_next')}")

    for key in ["weak_feedback_handling_built", "bad_counters_zero"]:
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
        "weak_records_handled_count": 3,
        "weak_feedback_count": 3,
        "under_typed_feedback_count": 2,
        "ambiguous_requires_question_count": 1,
        "question_packet_candidates_emitted": 3,
        "source_ref_request_candidates_emitted": 2,
        "under_typed_acceptance_candidates_emitted": 2,
        "parking_records_emitted": 3,
        "c5_block_records_emitted": 3,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    if summary.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("summary_c5_not_blocked")

    if len(handling) != 3:
        failures.append(f"handling_count_wrong:{len(handling)}")
    if len(questions) != 3:
        failures.append(f"question_count_wrong:{len(questions)}")
    if len(source_refs) != 2:
        failures.append(f"source_ref_count_wrong:{len(source_refs)}")
    if len(acceptances) != 2:
        failures.append(f"acceptance_count_wrong:{len(acceptances)}")
    if len(parking) != 3:
        failures.append(f"parking_count_wrong:{len(parking)}")
    if len(c5_blocks) != 3:
        failures.append(f"c5_block_count_wrong:{len(c5_blocks)}")

    handling_refs = {x.get("source_feedback_ref") for x in handling}
    question_refs = {x.get("source_feedback_ref") for x in questions}
    parking_refs = {x.get("source_feedback_ref") for x in parking}
    c5_refs = {x.get("source_feedback_ref") for x in c5_blocks}
    if len(handling_refs) != 3 or len(question_refs) != 3 or len(parking_refs) != 3 or len(c5_refs) != 3:
        failures.append("weak_ref_coverage_not_three_each_required_surface")
    if handling_refs != parking_refs or handling_refs != c5_refs:
        failures.append("handling_parking_c5_ref_sets_do_not_match")
    if not question_refs.issubset(handling_refs):
        failures.append("question_refs_not_subset_of_handling_refs")

    for rec in handling:
        if rec.get("resolution_status") != "UNRESOLVED":
            failures.append(f"handling_record_resolved:{rec.get('handling_record_id')}")
        if rec.get("handling_status") != "HANDLED_STATICALLY_NOT_RESOLVED":
            failures.append(f"handling_status_wrong:{rec.get('handling_record_id')}")
        if rec.get("c5_block_preserved") is not True:
            failures.append(f"handling_c5_not_preserved:{rec.get('handling_record_id')}")

    for rec in questions:
        if rec.get("status") != "PROPOSED_ONLY":
            failures.append(f"question_not_proposed_only:{rec.get('question_packet_id')}")
        if rec.get("blocked_until_answered") is not True:
            failures.append(f"question_not_blocking:{rec.get('question_packet_id')}")
        if rec.get("c5_block_preserved") is not True:
            failures.append(f"question_c5_not_preserved:{rec.get('question_packet_id')}")

    for rec in source_refs:
        if rec.get("status") != "REQUEST_CANDIDATE_ONLY":
            failures.append(f"source_ref_request_not_candidate:{rec.get('source_ref_request_id')}")
        if not rec.get("requested_evidence_refs"):
            failures.append(f"source_ref_request_missing_evidence_refs:{rec.get('source_ref_request_id')}")

    for rec in acceptances:
        if rec.get("status") != "CANDIDATE_ONLY":
            failures.append(f"under_typed_acceptance_not_candidate:{rec.get('acceptance_candidate_id')}")
        if rec.get("human_or_validator_review_required") is not True:
            failures.append(f"under_typed_acceptance_missing_review:{rec.get('acceptance_candidate_id')}")
        if rec.get("c5_unblock_allowed") is not False:
            failures.append(f"under_typed_acceptance_unblocks_c5:{rec.get('acceptance_candidate_id')}")

    for rec in parking:
        if rec.get("status") != "PARKED_WITH_REASON":
            failures.append(f"parking_status_wrong:{rec.get('parking_id')}")
        if "open C5" not in rec.get("blocked_moves", []):
            failures.append(f"parking_missing_c5_block:{rec.get('parking_id')}")

    for rec in c5_blocks:
        if rec.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
            failures.append(f"c5_block_readiness_wrong:{rec.get('c5_block_record_id')}")
        if rec.get("c5_opened") is not False:
            failures.append(f"c5_block_opened:{rec.get('c5_block_record_id')}")
        if rec.get("unblock_requires_reviewed_resolution_or_acceptance") is not True:
            failures.append(f"c5_block_missing_reviewed_unblock_rule:{rec.get('c5_block_record_id')}")

    required_zero_rollup = [
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
    for key in required_zero_rollup:
        if rollup.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup.get(key)}")

    if readout.get("weak_feedback_resolved") is not False:
        failures.append("readout_weak_feedback_resolved")
    if readout.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("readout_c5_not_blocked")
    if profile.get("bad_counters_zero") is not True:
        failures.append("profile_bad_counters_not_true")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    if report.get("recommended_next_handling") != EXPECTED_BUILD_NEXT:
        failures.append("report_recommended_next_wrong")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_BUILD_STOP:
        failures.append("trace_terminal_wrong")
    if design_receipt.get("receipt_id") != "90309841":
        failures.append("design_receipt_wrong")
    if target_definition.get("target_mode_for_build") != "STATIC_WEAK_FEEDBACK_HANDLING_ONLY":
        failures.append("target_definition_mode_wrong")
    if inventory.get("weak_feedback_count") != 3:
        failures.append("inventory_count_wrong")
    if c5_contract.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("c5_contract_not_blocked")
    if weak_note.get("weak_feedback_count") != 3:
        failures.append("weak_note_count_wrong")
    if c5_status.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("source_c5_status_not_blocked")

    return failures, {
        "summary": summary,
        "handling": handling,
        "questions": questions,
        "source_refs": source_refs,
        "acceptances": acceptances,
        "parking": parking,
        "c5_blocks": c5_blocks,
        "rollup": rollup,
        "readout": readout,
        "profile": profile,
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
    rollup_src = src.get("rollup", {})

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    review_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_HANDLING_REVIEWED_STATIC_RECORDS_CLEAN_CLOSE_READY" if review_pass else "TYPED_O2_WEAK_FEEDBACK_HANDLING_REVIEW_GATE_FAIL"
    recommended_next = "CLOSE_O2_WEAK_FEEDBACK_HANDLING_AS_REVIEWED_REFERENCE_V0" if review_pass else "REPAIR_O2_WEAK_FEEDBACK_HANDLING_V0"

    reason_codes = [
        "WEAK_FEEDBACK_HANDLING_REVIEW_COMPLETE",
        "WEAK_FEEDBACK_HANDLING_REVIEW_PASS",
        "BUILD_RECEIPT_CONSUMED",
        "THREE_WEAK_RECORDS_COVERED_BY_HANDLING_RECORDS",
        "QUESTION_PACKETS_PROPOSED_ONLY_CONFIRMED",
        "SOURCE_REF_REQUESTS_CANDIDATE_ONLY_CONFIRMED",
        "UNDER_TYPED_ACCEPTANCE_CANDIDATE_ONLY_CONFIRMED",
        "PARKING_NOT_RESOLUTION_CONFIRMED",
        "C5_BLOCK_RECORDS_CONFIRMED",
        "WEAK_FEEDBACK_REMAINS_UNRESOLVED",
        "C5_REMAINS_BLOCKED_BY_WEAK_FEEDBACK",
        "NO_LIVE_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_TARGET_SELECTED_FOR_BUILD",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
        "NO_C5_OPENED",
        "CLOSURE_CANDIDATE_READY",
    ] if review_pass else failures

    review_assessment = {
        "schema_version": "o2_weak_feedback_handling_review_assessment_v0",
        "review_status": status,
        "source_weak_feedback_handling_receipt_id": WFH_BUILD_RECEIPT_ID,
        "review_pass": review_pass,
        "weak_records_reviewed": len(handling),
        "question_packets_reviewed": len(questions),
        "source_ref_requests_reviewed": len(source_refs),
        "under_typed_acceptance_candidates_reviewed": len(acceptances),
        "parking_records_reviewed": len(parking),
        "c5_block_records_reviewed": len(c5_blocks),
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "closure_candidate_ready": review_pass,
        "recommended_next": recommended_next,
    }

    handling_record_review = {
        "schema_version": "o2_weak_feedback_handling_record_review_v0",
        "review_status": "HANDLING_RECORD_REVIEW_PASS" if review_pass else "HANDLING_RECORD_REVIEW_FAIL",
        "handling_records_reviewed": len(handling),
        "all_records_unresolved": all(x.get("resolution_status") == "UNRESOLVED" for x in handling),
        "all_records_static_not_resolved": all(x.get("handling_status") == "HANDLED_STATICALLY_NOT_RESOLVED" for x in handling),
        "all_records_preserve_c5_block": all(x.get("c5_block_preserved") is True for x in handling),
    }

    question_packet_review = {
        "schema_version": "o2_weak_feedback_question_packet_review_v0",
        "review_status": "QUESTION_PACKET_REVIEW_PASS" if review_pass else "QUESTION_PACKET_REVIEW_FAIL",
        "question_packets_reviewed": len(questions),
        "all_proposed_only": all(x.get("status") == "PROPOSED_ONLY" for x in questions),
        "all_block_until_answered": all(x.get("blocked_until_answered") is True for x in questions),
        "all_preserve_c5_block": all(x.get("c5_block_preserved") is True for x in questions),
        "question_packets_answered": False,
    }

    source_ref_request_review = {
        "schema_version": "o2_weak_feedback_source_ref_request_review_v0",
        "review_status": "SOURCE_REF_REQUEST_REVIEW_PASS" if review_pass else "SOURCE_REF_REQUEST_REVIEW_FAIL",
        "source_ref_requests_reviewed": len(source_refs),
        "all_request_candidate_only": all(x.get("status") == "REQUEST_CANDIDATE_ONLY" for x in source_refs),
        "source_ref_requests_satisfied": False,
    }

    acceptance_review = {
        "schema_version": "o2_under_typed_acceptance_candidate_review_v0",
        "review_status": "UNDER_TYPED_ACCEPTANCE_CANDIDATE_REVIEW_PASS" if review_pass else "UNDER_TYPED_ACCEPTANCE_CANDIDATE_REVIEW_FAIL",
        "under_typed_acceptance_candidates_reviewed": len(acceptances),
        "all_candidate_only": all(x.get("status") == "CANDIDATE_ONLY" for x in acceptances),
        "all_require_human_or_validator_review": all(x.get("human_or_validator_review_required") is True for x in acceptances),
        "all_c5_unblock_allowed_false": all(x.get("c5_unblock_allowed") is False for x in acceptances),
        "under_typed_acceptance_approved": False,
    }

    parking_review = {
        "schema_version": "o2_weak_feedback_parking_review_v0",
        "review_status": "PARKING_REVIEW_PASS" if review_pass else "PARKING_REVIEW_FAIL",
        "parking_records_reviewed": len(parking),
        "all_parked_with_reason": all(x.get("status") == "PARKED_WITH_REASON" for x in parking),
        "parking_counted_as_resolution": False,
    }

    c5_block_review = {
        "schema_version": "o2_weak_feedback_c5_block_review_v0",
        "review_status": "C5_BLOCK_REVIEW_PASS" if review_pass else "C5_BLOCK_REVIEW_FAIL",
        "c5_block_records_reviewed": len(c5_blocks),
        "all_c5_records_blocked": all(x.get("c5_feedback_readiness") == "BLOCKED_BY_WEAK_FEEDBACK" for x in c5_blocks),
        "all_c5_opened_false": all(x.get("c5_opened") is False for x in c5_blocks),
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
    }

    unresolved_status_review = {
        "schema_version": "o2_weak_feedback_unresolved_status_review_v0",
        "review_status": "UNRESOLVED_STATUS_CONFIRMED",
        "weak_feedback_resolved": False,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parked_records_counted_as_resolved": False,
        "meaning": "Weak feedback now has reviewed handling structures but remains unresolved.",
    }

    closure_candidate = {
        "schema_version": "o2_weak_feedback_handling_closure_candidate_v0",
        "closure_candidate_status": "WEAK_FEEDBACK_HANDLING_CLOSE_READY_UNRESOLVED" if review_pass else "WEAK_FEEDBACK_HANDLING_CLOSE_NOT_READY",
        "review_pass": review_pass,
        "reviewed_reference_candidate": "o2_weak_feedback_handling_static_records_v0",
        "closure_meaning": "Close static handling records as reviewed reference while preserving unresolved weak feedback and C5 block.",
        "closure_does_not_mean": [
            "weak feedback resolved",
            "question packets answered",
            "source-ref requests satisfied",
            "under-typed acceptance approved",
            "C5 unblocked",
        ],
        "recommended_next": recommended_next,
    }

    downstream_decision_table = {
        "schema_version": "o2_weak_feedback_handling_review_downstream_decision_table_v0",
        "decision_status": "CLOSE_READY" if review_pass else "REPAIR_REQUIRED",
        "records": [
            {
                "decision": "CLOSE_WEAK_FEEDBACK_HANDLING_AS_REVIEWED_REFERENCE",
                "selected": review_pass,
                "next_unit": recommended_next if review_pass else None,
                "why": "Static handling records reviewed clean; unresolved status and C5 block preserved.",
            },
            {
                "decision": "RESOLVE_WEAK_FEEDBACK_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Review confirms handling, not resolution.",
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
        "schema_version": "o2_weak_feedback_handling_review_authority_boundary_v0",
        "status": status,
        "may_close_weak_feedback_handling_as_reviewed_reference_next": review_pass,
        "may_resolve_weak_feedback_now": False,
        "may_answer_question_packets": False,
        "may_satisfy_source_ref_requests": False,
        "may_approve_under_typed_acceptance": False,
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
        "schema_version": "o2_weak_feedback_handling_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "review_complete": review_pass,
        "review_pass": review_pass,
        "weak_records_reviewed": len(handling),
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_opened": False,
        "closure_candidate_ready": review_pass,
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
        "schema_version": "o2_weak_feedback_handling_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "weak_records_reviewed_count": len(handling),
        "question_packets_reviewed_count": len(questions),
        "source_ref_requests_reviewed_count": len(source_refs),
        "under_typed_acceptance_candidates_reviewed_count": len(acceptances),
        "parking_records_reviewed_count": len(parking),
        "c5_block_records_reviewed_count": len(c5_blocks),
        "closure_candidate_ready_count": 1 if review_pass else 0,
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
        "schema_version": "o2_weak_feedback_handling_review_profile_v0",
        "profile_id": "o2_weak_feedback_handling_review_profile_" + sha8(rollup),
        "status": status,
        "review_pass": review_pass,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "closure_candidate_ready": review_pass,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Close weak-feedback handling as reviewed reference; do not treat handling as resolution.",
        "must_not_infer": [
            "weak feedback resolved",
            "question packets answered",
            "source-ref requests satisfied",
            "under-typed acceptance approved",
            "live audit complete",
            "C5 opened",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_weak_feedback_handling_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The weak-feedback handling build was reviewed clean. All 3 weak records have static handling records. Question packets remain PROPOSED_ONLY, source-ref requests remain REQUEST_CANDIDATE_ONLY, under-typed acceptance remains CANDIDATE_ONLY, parking is not counted as resolution, and C5 block records preserve BLOCKED_BY_WEAK_FEEDBACK. No weak feedback was resolved, no question packet was answered, no source-ref request was satisfied, no under-typed acceptance was approved, and no live audit, repair, retry, target selection, runtime patch, source mutation, or C5 opening occurred.",
        "weak_records_reviewed": len(handling),
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_weak_feedback_handling_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_handling_build",
                "question": "did static handling records emit for all weak records",
                "answer": "yes" if review_pass else "no",
                "taken": "review handling outputs",
            },
            {
                "step": "verify_nonresolution",
                "question": "did any handling artifact resolve weak feedback or unblock C5",
                "answer": "no",
                "taken": "preserve unresolved status and C5 block",
            },
            {
                "step": "emit_closure_candidate",
                "question": "can static weak-feedback handling close as reviewed reference",
                "answer": "yes" if review_pass else "no",
                "taken": recommended_next,
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
        (HANDLING_RECORD_REVIEW_PATH, handling_record_review),
        (QUESTION_PACKET_REVIEW_PATH, question_packet_review),
        (SOURCE_REF_REQUEST_REVIEW_PATH, source_ref_request_review),
        (UNDERTYPED_ACCEPTANCE_REVIEW_PATH, acceptance_review),
        (PARKING_REVIEW_PATH, parking_review),
        (C5_BLOCK_REVIEW_PATH, c5_block_review),
        (UNRESOLVED_STATUS_REVIEW_PATH, unresolved_status_review),
        (CLOSURE_CANDIDATE_PATH, closure_candidate),
        (DOWNSTREAM_DECISION_TABLE_PATH, downstream_decision_table),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_OUT_PATH, rollup),
        (PROFILE_OUT_PATH, profile),
        (REPORT_OUT_PATH, report),
        (TRACE_OUT_PATH, trace),
    ]
    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "WFH_REVIEW_0_BUILD_RECEIPT_CONSUMED": WFH_BUILD_RECEIPT_PATH.exists(),
        "WFH_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "WFH_REVIEW_2_THREE_HANDLING_RECORDS_REVIEWED": len(handling) == 3,
        "WFH_REVIEW_3_THREE_QUESTION_PACKETS_REVIEWED": len(questions) == 3,
        "WFH_REVIEW_4_TWO_SOURCE_REF_REQUESTS_REVIEWED": len(source_refs) == 2,
        "WFH_REVIEW_5_TWO_UNDER_TYPED_ACCEPTANCE_CANDIDATES_REVIEWED": len(acceptances) == 2,
        "WFH_REVIEW_6_THREE_PARKING_RECORDS_REVIEWED": len(parking) == 3,
        "WFH_REVIEW_7_THREE_C5_BLOCK_RECORDS_REVIEWED": len(c5_blocks) == 3,
        "WFH_REVIEW_8_HANDLING_RECORDS_UNRESOLVED": handling_record_review["all_records_unresolved"] is True,
        "WFH_REVIEW_9_QUESTION_PACKETS_PROPOSED_ONLY": question_packet_review["all_proposed_only"] is True,
        "WFH_REVIEW_10_SOURCE_REF_REQUESTS_CANDIDATE_ONLY": source_ref_request_review["all_request_candidate_only"] is True,
        "WFH_REVIEW_11_UNDER_TYPED_ACCEPTANCE_CANDIDATE_ONLY": acceptance_review["all_candidate_only"] is True,
        "WFH_REVIEW_12_PARKING_NOT_RESOLUTION": parking_review["parking_counted_as_resolution"] is False,
        "WFH_REVIEW_13_C5_BLOCK_PRESERVED": c5_block_review["review_status"] == "C5_BLOCK_REVIEW_PASS",
        "WFH_REVIEW_14_NO_WEAK_FEEDBACK_RESOLUTION": rollup["weak_feedback_resolved_count"] == 0,
        "WFH_REVIEW_15_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "WFH_REVIEW_16_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "WFH_REVIEW_17_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "WFH_REVIEW_18_CLOSURE_CANDIDATE_READY": closure_candidate["closure_candidate_status"] == "WEAK_FEEDBACK_HANDLING_CLOSE_READY_UNRESOLVED",
        "WFH_REVIEW_19_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "WFH_REVIEW_20_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_OUT_PATH.exists() and PROFILE_OUT_PATH.exists() and REPORT_OUT_PATH.exists() and TRACE_OUT_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_HANDLING_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "review_pass": review_pass,
        "weak_records": len(handling),
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_handling_review_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_HANDLING_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_weak_feedback_handling_receipt_id": WFH_BUILD_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_handling_review_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "review_complete": review_pass,
            "review_pass": review_pass,
            "weak_records_reviewed_count": len(handling),
            "question_packets_reviewed_count": len(questions),
            "source_ref_requests_reviewed_count": len(source_refs),
            "under_typed_acceptance_candidates_reviewed_count": len(acceptances),
            "parking_records_reviewed_count": len(parking),
            "c5_block_records_reviewed_count": len(c5_blocks),
            "handling_records_unresolved": handling_record_review["all_records_unresolved"],
            "question_packets_proposed_only": question_packet_review["all_proposed_only"],
            "source_ref_requests_candidate_only": source_ref_request_review["all_request_candidate_only"],
            "under_typed_acceptance_candidate_only": acceptance_review["all_candidate_only"],
            "parking_not_resolution": parking_review["parking_counted_as_resolution"] is False,
            "c5_block_preserved": c5_block_review["review_status"] == "C5_BLOCK_REVIEW_PASS",
            "weak_feedback_resolved": False,
            "question_packets_answered": False,
            "source_ref_requests_satisfied": False,
            "under_typed_acceptance_approved": False,
            "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
            "c5_opened": False,
            "closure_candidate_ready": review_pass,
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
            "handling_record_review": rel(HANDLING_RECORD_REVIEW_PATH),
            "question_packet_review": rel(QUESTION_PACKET_REVIEW_PATH),
            "source_ref_request_review": rel(SOURCE_REF_REQUEST_REVIEW_PATH),
            "under_typed_acceptance_review": rel(UNDERTYPED_ACCEPTANCE_REVIEW_PATH),
            "parking_review": rel(PARKING_REVIEW_PATH),
            "c5_block_review": rel(C5_BLOCK_REVIEW_PATH),
            "unresolved_status_review": rel(UNRESOLVED_STATUS_REVIEW_PATH),
            "closure_candidate": rel(CLOSURE_CANDIDATE_PATH),
            "downstream_decision_table": rel(DOWNSTREAM_DECISION_TABLE_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "classification": rel(CLASSIFICATION_PATH),
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
    print(f"weak_feedback_handling_review_receipt_id={receipt_id}")
    print(f"weak_feedback_handling_review_receipt_path={rel(receipt_path)}")
    print(f"weak_feedback_handling_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"weak_feedback_handling_record_review_path={rel(HANDLING_RECORD_REVIEW_PATH)}")
    print(f"weak_feedback_question_packet_review_path={rel(QUESTION_PACKET_REVIEW_PATH)}")
    print(f"weak_feedback_source_ref_request_review_path={rel(SOURCE_REF_REQUEST_REVIEW_PATH)}")
    print(f"under_typed_acceptance_review_path={rel(UNDERTYPED_ACCEPTANCE_REVIEW_PATH)}")
    print(f"weak_feedback_parking_review_path={rel(PARKING_REVIEW_PATH)}")
    print(f"weak_feedback_c5_block_review_path={rel(C5_BLOCK_REVIEW_PATH)}")
    print(f"weak_feedback_handling_review_rollup_path={rel(ROLLUP_OUT_PATH)}")
    print(f"weak_feedback_handling_review_profile_path={rel(PROFILE_OUT_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
