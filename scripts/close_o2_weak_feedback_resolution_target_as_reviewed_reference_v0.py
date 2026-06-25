#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_target_closure.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_TARGET_CLOSURE"
MODE = "CLOSE / FREEZE_REVIEWED_RESOLUTION_TARGET_REFERENCE / NO_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_TARGET_CLOSURE_ONLY"

RT_REVIEW_RECEIPT_ID = "288f6dc4"
RT_REVIEW_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0_receipts/288f6dc4.json"
RT_REVIEW_ASSESSMENT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0/o2_weak_feedback_resolution_target_review_assessment_v0.json"
RT_SKELETON_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0/o2_weak_feedback_resolution_skeleton_review_v0.json"
RT_ROUTE_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0/o2_weak_feedback_resolution_route_map_review_v0.json"
RT_GATE_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0/o2_weak_feedback_resolution_gate_readout_review_v0.json"
RT_C5_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0/o2_c5_reconsideration_readout_review_v0.json"
RT_NONRESOLUTION_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0/o2_weak_feedback_resolution_nonresolution_review_v0.json"
RT_CLOSURE_CANDIDATE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0/o2_weak_feedback_resolution_target_closure_candidate_v0.json"
RT_REVIEW_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0/o2_weak_feedback_resolution_target_review_authority_boundary_v0.json"
RT_REVIEW_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0/o2_weak_feedback_resolution_target_review_classification_v0.json"
RT_REVIEW_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0/o2_weak_feedback_resolution_target_review_rollup_v0.json"
RT_REVIEW_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0/o2_weak_feedback_resolution_target_review_profile_v0.json"
RT_REVIEW_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0/o2_weak_feedback_resolution_target_review_report.json"
RT_REVIEW_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_review_v0/o2_weak_feedback_resolution_target_review_transition_trace.json"

RT_BUILD_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0_receipts/16f7210b.json"
RT_SURFACE_RECORD_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_target_surface_record_v0.json"
RT_INPUT_MAPPING_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_input_mapping_v0.json"
RT_QUESTION_SKELETONS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_question_packet_answer_record_skeletons_v0.jsonl"
RT_SOURCE_REF_SKELETONS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_source_ref_satisfaction_record_skeletons_v0.jsonl"
RT_UNDERTYPED_SKELETONS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_under_typed_acceptance_review_record_skeletons_v0.jsonl"
RT_PARKING_SKELETONS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_parking_continuation_record_skeletons_v0.jsonl"
RT_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_route_map_v0.jsonl"
RT_GATE_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_gate_readout_v0.json"
RT_C5_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_c5_reconsideration_readout_v0.json"
RT_NONRESOLUTION_ATTESTATION_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_target_nonresolution_attestation_v0.json"

REQUIRED_SOURCE_FILES = [
    RT_REVIEW_RECEIPT_PATH,
    RT_REVIEW_ASSESSMENT_PATH,
    RT_SKELETON_REVIEW_PATH,
    RT_ROUTE_REVIEW_PATH,
    RT_GATE_REVIEW_PATH,
    RT_C5_REVIEW_PATH,
    RT_NONRESOLUTION_REVIEW_PATH,
    RT_CLOSURE_CANDIDATE_PATH,
    RT_REVIEW_AUTHORITY_PATH,
    RT_REVIEW_CLASSIFICATION_PATH,
    RT_REVIEW_ROLLUP_PATH,
    RT_REVIEW_PROFILE_PATH,
    RT_REVIEW_REPORT_PATH,
    RT_REVIEW_TRACE_PATH,
    RT_BUILD_RECEIPT_PATH,
    RT_SURFACE_RECORD_PATH,
    RT_INPUT_MAPPING_PATH,
    RT_QUESTION_SKELETONS_PATH,
    RT_SOURCE_REF_SKELETONS_PATH,
    RT_UNDERTYPED_SKELETONS_PATH,
    RT_PARKING_SKELETONS_PATH,
    RT_ROUTE_MAP_PATH,
    RT_GATE_READOUT_PATH,
    RT_C5_READOUT_PATH,
    RT_NONRESOLUTION_ATTESTATION_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0_receipts"

CLOSURE_RECORD_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_reviewed_reference_v0.json"
SKELETON_FREEZE_PATH = OUT_DIR / "o2_weak_feedback_resolution_skeleton_freeze_v0.json"
ROUTE_MAP_FREEZE_PATH = OUT_DIR / "o2_weak_feedback_resolution_route_map_freeze_v0.json"
NONRESOLUTION_FREEZE_PATH = OUT_DIR / "o2_weak_feedback_resolution_nonresolution_freeze_v0.json"
C5_BLOCK_FREEZE_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_c5_block_freeze_v0.json"
RECEIPT_CHAIN_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_receipt_chain_v0.json"
BOUNDARY_LOCK_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_closure_boundary_lock_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_closure_downstream_decision_table_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_closure_report.json"
TRACE_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_REVIEWED_STATIC_SURFACE_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_REVIEWED_STATIC_SURFACE_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_AS_REVIEWED_REFERENCE_V0"

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

    receipt = read_json(RT_REVIEW_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_resolution_target_review_summary", {})
    assessment = read_json(RT_REVIEW_ASSESSMENT_PATH)
    skeleton_review = read_json(RT_SKELETON_REVIEW_PATH)
    route_review = read_json(RT_ROUTE_REVIEW_PATH)
    gate_review = read_json(RT_GATE_REVIEW_PATH)
    c5_review = read_json(RT_C5_REVIEW_PATH)
    nonresolution_review = read_json(RT_NONRESOLUTION_REVIEW_PATH)
    closure_candidate = read_json(RT_CLOSURE_CANDIDATE_PATH)
    review_authority = read_json(RT_REVIEW_AUTHORITY_PATH)
    review_classification = read_json(RT_REVIEW_CLASSIFICATION_PATH)
    review_rollup = read_json(RT_REVIEW_ROLLUP_PATH)
    review_profile = read_json(RT_REVIEW_PROFILE_PATH)
    review_report = read_json(RT_REVIEW_REPORT_PATH)
    review_trace = read_json(RT_REVIEW_TRACE_PATH)

    build_receipt = read_json(RT_BUILD_RECEIPT_PATH)
    surface = read_json(RT_SURFACE_RECORD_PATH)
    mapping = read_json(RT_INPUT_MAPPING_PATH)
    questions = read_jsonl(RT_QUESTION_SKELETONS_PATH)
    source_refs = read_jsonl(RT_SOURCE_REF_SKELETONS_PATH)
    undertyped = read_jsonl(RT_UNDERTYPED_SKELETONS_PATH)
    parking = read_jsonl(RT_PARKING_SKELETONS_PATH)
    route_map = read_jsonl(RT_ROUTE_MAP_PATH)
    gate_readout = read_json(RT_GATE_READOUT_PATH)
    c5_readout = read_json(RT_C5_READOUT_PATH)
    nonresolution = read_json(RT_NONRESOLUTION_ATTESTATION_PATH)

    if receipt.get("receipt_id") != RT_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("resolution_target_review_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("resolution_target_review_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("resolution_target_review_hidden_next_command")
    if summary.get("status") != EXPECTED_REVIEW_STATUS:
        failures.append(f"resolution_target_review_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append(f"resolution_target_review_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "review_complete",
        "review_pass",
        "question_skeletons_not_answered",
        "source_ref_skeletons_unsatisfied",
        "under_typed_skeletons_unreviewed",
        "parking_skeletons_not_resolution",
        "route_map_unresolved",
        "resolution_gate_not_resolved",
        "c5_block_preserved",
        "closure_candidate_ready",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "question_answer_skeletons_reviewed": 3,
        "source_ref_satisfaction_skeletons_reviewed": 2,
        "under_typed_acceptance_review_skeletons_reviewed": 2,
        "parking_continuation_skeletons_reviewed": 3,
        "route_map_records_reviewed": 3,
        "resolution_records_emitted_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    for key in [
        "weak_feedback_resolved",
        "question_packets_answered",
        "source_ref_requests_satisfied",
        "under_typed_acceptance_approved",
        "parking_counted_as_resolution",
        "c5_opened",
        "c5_reconsideration_ready",
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
        failures.append("assessment_closure_not_ready")
    if skeleton_review.get("question_answer_skeletons", {}).get("all_not_answered") is not True:
        failures.append("skeleton_review_questions_wrong")
    if skeleton_review.get("source_ref_satisfaction_skeletons", {}).get("all_unsatisfied") is not True:
        failures.append("skeleton_review_source_refs_wrong")
    if skeleton_review.get("under_typed_acceptance_review_skeletons", {}).get("all_unreviewed") is not True:
        failures.append("skeleton_review_undertyped_wrong")
    if skeleton_review.get("parking_continuation_skeletons", {}).get("all_not_resolution") is not True:
        failures.append("skeleton_review_parking_wrong")
    if route_review.get("all_unresolved") is not True:
        failures.append("route_review_not_unresolved")
    if gate_review.get("weak_feedback_resolved") is not False or gate_review.get("resolution_records_emitted_count") != 0:
        failures.append("gate_review_wrong")
    if c5_review.get("c5_opened") is not False or c5_review.get("c5_reconsideration_ready") is not False:
        failures.append("c5_review_wrong")
    if nonresolution_review.get("weak_feedback_resolved") is not False:
        failures.append("nonresolution_review_wrong")
    if closure_candidate.get("closure_candidate_status") != "RESOLUTION_TARGET_CLOSE_READY_UNRESOLVED":
        failures.append("closure_candidate_not_ready")
    if review_authority.get("may_close_resolution_target_as_reviewed_reference_next") is not True:
        failures.append("review_authority_no_close")
    if review_authority.get("may_open_c5") is not False:
        failures.append("review_authority_allows_c5")
    if review_classification.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append("classification_next_wrong")
    if review_rollup.get("closure_candidate_ready_count") != 1:
        failures.append("rollup_closure_candidate_wrong")
    if review_profile.get("closure_candidate_ready") is not True or review_profile.get("bad_counters_zero") is not True:
        failures.append("profile_wrong")
    if review_report.get("recommended_next_handling") != EXPECTED_REVIEW_NEXT:
        failures.append("report_next_wrong")
    if review_trace.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("trace_stop_wrong")

    if build_receipt.get("receipt_id") != "16f7210b":
        failures.append("build_receipt_wrong")
    if surface.get("surface_status") != "STATIC_RESOLUTION_TARGET_SURFACE_EMITTED":
        failures.append("surface_status_wrong")
    if mapping.get("weak_records_mapped_count") != 3:
        failures.append("mapping_count_wrong")
    if len(questions) != 3 or len(source_refs) != 2 or len(undertyped) != 2 or len(parking) != 3 or len(route_map) != 3:
        failures.append("build_surface_counts_wrong")
    if gate_readout.get("weak_feedback_resolved") is not False or gate_readout.get("resolution_records_emitted_count") != 0:
        failures.append("build_gate_readout_wrong")
    if c5_readout.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_readout.get("c5_opened") is not False:
        failures.append("build_c5_readout_wrong")
    if nonresolution.get("weak_feedback_resolved") is not False or nonresolution.get("resolution_records_emitted_count") != 0:
        failures.append("build_nonresolution_wrong")

    return failures, {
        "summary": summary,
        "questions": questions,
        "source_refs": source_refs,
        "undertyped": undertyped,
        "parking": parking,
        "route_map": route_map,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    summary = src.get("summary", {})
    questions = src.get("questions", [])
    source_refs = src.get("source_refs", [])
    undertyped = src.get("undertyped", [])
    parking = src.get("parking", [])
    route_map = src.get("route_map", [])

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    closure_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED_DECISION_READY" if closure_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_CLOSURE_GATE_FAIL"
    recommended_next = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_REFERENCE_CLOSURE_V0" if closure_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_CLOSURE_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_TARGET_CLOSED_AS_REVIEWED_REFERENCE",
        "RESOLUTION_TARGET_REVIEW_RECEIPT_CONSUMED",
        "REVIEWED_SKELETONS_FROZEN",
        "REVIEWED_ROUTE_MAP_FROZEN_UNRESOLVED",
        "REVIEWED_NONRESOLUTION_STATUS_FROZEN",
        "REVIEWED_C5_BLOCK_STATUS_FROZEN",
        "NO_RESOLUTION_RECORDS_FROZEN",
        "POST_CLOSURE_DECISION_READY",
        "NO_WEAK_FEEDBACK_RESOLUTION_ATTEMPTED",
        "NO_QUESTION_PACKET_ANSWERED",
        "NO_SOURCE_REF_REQUEST_SATISFIED",
        "NO_UNDER_TYPED_ACCEPTANCE_APPROVED",
        "NO_PARKING_COUNTED_AS_RESOLUTION",
        "NO_C5_RECONSIDERATION_READY",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_TARGET_SELECTED_FOR_BUILD",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if closure_pass else failures

    closure_record = {
        "schema_version": "o2_weak_feedback_resolution_target_closure_record_v0",
        "closure_status": "CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED" if closure_pass else "CLOSURE_NOT_RECORDED",
        "source_resolution_target_review_receipt_id": RT_REVIEW_RECEIPT_ID,
        "closed_object": "o2_weak_feedback_resolution_target_static_surface_v0",
        "closure_meaning": "Reviewed static resolution-target surface is frozen as a reference.",
        "closure_does_not_mean": [
            "weak feedback resolved",
            "question packets answered",
            "source-ref requests satisfied",
            "under-typed acceptance approved",
            "parking counted as resolution",
            "C5 reconsideration ready",
            "C5 opened",
        ],
    }

    reviewed_reference = {
        "schema_version": "o2_weak_feedback_resolution_target_reviewed_reference_v0",
        "reference_status": "FROZEN_REVIEWED_REFERENCE" if closure_pass else "REFERENCE_NOT_FROZEN",
        "reference_object_id": "o2_wf_resolution_target_reviewed_reference_" + sha8({
            "review_receipt": RT_REVIEW_RECEIPT_ID,
            "questions": len(questions),
            "source_refs": len(source_refs),
            "undertyped": len(undertyped),
            "parking": len(parking),
            "routes": len(route_map),
        }),
        "source_review_receipt_id": RT_REVIEW_RECEIPT_ID,
        "source_build_receipt_id": "16f7210b",
        "source_design_receipt_id": "e9765563",
        "reviewed_surfaces": {
            "question_answer_skeletons": len(questions),
            "source_ref_satisfaction_skeletons": len(source_refs),
            "under_typed_acceptance_review_skeletons": len(undertyped),
            "parking_continuation_skeletons": len(parking),
            "route_map_records": len(route_map),
        },
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "reference_use": "future units may cite this reviewed resolution-target surface before any actual resolution branch executes.",
    }

    skeleton_freeze = {
        "schema_version": "o2_weak_feedback_resolution_skeleton_freeze_v0",
        "freeze_status": "REVIEWED_SKELETONS_FROZEN",
        "question_answer_skeletons_frozen_count": len(questions),
        "source_ref_satisfaction_skeletons_frozen_count": len(source_refs),
        "under_typed_acceptance_review_skeletons_frozen_count": len(undertyped),
        "parking_continuation_skeletons_frozen_count": len(parking),
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
    }

    route_map_freeze = {
        "schema_version": "o2_weak_feedback_resolution_route_map_freeze_v0",
        "freeze_status": "REVIEWED_ROUTE_MAP_FROZEN_UNRESOLVED",
        "route_map_records_frozen_count": len(route_map),
        "all_route_map_records_unresolved": True,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_reconsideration_ready": False,
    }

    nonresolution_freeze = {
        "schema_version": "o2_weak_feedback_resolution_nonresolution_freeze_v0",
        "freeze_status": "NONRESOLUTION_STATUS_FROZEN",
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "c5_opened": False,
    }

    c5_block_freeze = {
        "schema_version": "o2_weak_feedback_resolution_target_c5_block_freeze_v0",
        "freeze_status": "C5_BLOCK_STATUS_FROZEN",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "closure_does_not_unblock_c5": True,
    }

    receipt_chain = {
        "schema_version": "o2_weak_feedback_resolution_target_receipt_chain_v0",
        "chain_status": "RECEIPT_CHAIN_PRESERVED",
        "receipts": [
            {"stage": "wfh_post_closure_decision", "receipt_id": "694e859c"},
            {"stage": "resolution_target_design", "receipt_id": "e9765563"},
            {"stage": "resolution_target_build", "receipt_id": "16f7210b"},
            {"stage": "resolution_target_review", "receipt_id": RT_REVIEW_RECEIPT_ID},
        ],
        "closure_receipt_pending": True,
    }

    boundary_lock = {
        "schema_version": "o2_weak_feedback_resolution_target_closure_boundary_lock_v0",
        "boundary_lock_status": "BOUNDARIES_LOCKED_AT_CLOSURE",
        "resolution_target_closed_as_reviewed_reference": closure_pass,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
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
    }

    downstream_decision_table = {
        "schema_version": "o2_weak_feedback_resolution_target_closure_downstream_decision_table_v0",
        "decision_status": "POST_CLOSURE_DECISION_READY" if closure_pass else "CLOSURE_REPAIR_REQUIRED",
        "records": [
            {
                "decision": "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_REFERENCE_CLOSURE",
                "selected": closure_pass,
                "next_unit": recommended_next if closure_pass else None,
                "why": "Resolution-target reference is closed, but no resolution records exist and C5 remains blocked.",
            },
            {
                "decision": "EXECUTE_RESOLUTION_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Closure freezes the reviewed target surface; execution requires an explicit later branch.",
            },
            {
                "decision": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 reconsideration remains false.",
            },
        ],
    }

    authority_boundary = {
        "schema_version": "o2_weak_feedback_resolution_target_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_resolution_target_reference_closure": closure_pass,
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
        "schema_version": "o2_weak_feedback_resolution_target_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "resolution_target_closed_as_reviewed_reference": closure_pass,
        "reviewed_reference_emitted": closure_pass,
        "post_closure_decision_ready": closure_pass,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
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
        "schema_version": "o2_weak_feedback_resolution_target_closure_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "closure_count": 1 if closure_pass else 0,
        "reviewed_reference_emitted_count": 1 if closure_pass else 0,
        "question_answer_skeletons_frozen_count": len(questions),
        "source_ref_satisfaction_skeletons_frozen_count": len(source_refs),
        "under_typed_acceptance_review_skeletons_frozen_count": len(undertyped),
        "parking_continuation_skeletons_frozen_count": len(parking),
        "route_map_records_frozen_count": len(route_map),
        "post_closure_decision_ready_count": 1 if closure_pass else 0,
        "weak_feedback_resolved_count": 0,
        "resolution_records_emitted_count": 0,
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
        "schema_version": "o2_weak_feedback_resolution_target_closure_profile_v0",
        "profile_id": "o2_wf_resolution_target_closure_profile_" + sha8(rollup),
        "status": status,
        "resolution_target_closed_as_reviewed_reference": closure_pass,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "post_closure_decision_ready": closure_pass,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Decide next after closing the resolution target reference; do not treat closure as resolution.",
        "must_not_infer": [
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
        "schema_version": "o2_weak_feedback_resolution_target_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The weak-feedback resolution target surface was closed as a reviewed reference. Reviewed skeletons, route maps, nonresolution status, and C5-block status were frozen. No resolution records were emitted, weak feedback remains unresolved, C5 reconsideration is false, and C5 remains blocked.",
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_weak_feedback_resolution_target_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_resolution_target_review",
                "question": "is the static resolution target surface reviewed clean and close-ready",
                "answer": "yes" if closure_pass else "no",
                "taken": "freeze reviewed reference",
            },
            {
                "step": "preserve_nonresolution",
                "question": "did closure emit any resolution records",
                "answer": "no",
                "taken": "freeze zero-resolution state",
            },
            {
                "step": "preserve_c5_block",
                "question": "is C5 reconsideration ready",
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
        (SKELETON_FREEZE_PATH, skeleton_freeze),
        (ROUTE_MAP_FREEZE_PATH, route_map_freeze),
        (NONRESOLUTION_FREEZE_PATH, nonresolution_freeze),
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
        "RT_CLOSE_0_REVIEW_RECEIPT_CONSUMED": RT_REVIEW_RECEIPT_PATH.exists(),
        "RT_CLOSE_1_CLOSURE_RECORD_EMITTED": CLOSURE_RECORD_PATH.exists(),
        "RT_CLOSE_2_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists(),
        "RT_CLOSE_3_SKELETON_FREEZE_EMITTED": SKELETON_FREEZE_PATH.exists(),
        "RT_CLOSE_4_ROUTE_MAP_FREEZE_EMITTED": ROUTE_MAP_FREEZE_PATH.exists(),
        "RT_CLOSE_5_NONRESOLUTION_FREEZE_EMITTED": NONRESOLUTION_FREEZE_PATH.exists(),
        "RT_CLOSE_6_C5_BLOCK_FREEZE_EMITTED": C5_BLOCK_FREEZE_PATH.exists(),
        "RT_CLOSE_7_ZERO_RESOLUTION_RECORDS_PRESERVED": rollup["resolution_records_emitted_count"] == 0,
        "RT_CLOSE_8_NO_RESOLUTION_ANSWER_SATISFY_APPROVE": rollup["weak_feedback_resolved_count"] == 0 and rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "RT_CLOSE_9_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "RT_CLOSE_10_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "RT_CLOSE_11_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "RT_CLOSE_12_C5_RECONSIDERATION_FALSE": rollup["c5_reconsideration_ready_count"] == 0,
        "RT_CLOSE_13_POST_CLOSURE_DECISION_READY": rollup["post_closure_decision_ready_count"] == 1,
        "RT_CLOSE_14_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "RT_CLOSE_15_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "RT_CLOSE_16_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "closed": closure_pass,
        "routes": len(route_map),
        "resolution_records": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_resolution_target_closure_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_resolution_target_review_receipt_id": RT_REVIEW_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_resolution_target_closure_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "resolution_target_closed_as_reviewed_reference": closure_pass,
            "reviewed_reference_emitted": closure_pass,
            "question_answer_skeletons_frozen_count": len(questions),
            "source_ref_satisfaction_skeletons_frozen_count": len(source_refs),
            "under_typed_acceptance_review_skeletons_frozen_count": len(undertyped),
            "parking_continuation_skeletons_frozen_count": len(parking),
            "route_map_records_frozen_count": len(route_map),
            "weak_feedback_resolved": False,
            "resolution_records_emitted_count": 0,
            "question_packets_answered": False,
            "source_ref_requests_satisfied": False,
            "under_typed_acceptance_approved": False,
            "parking_counted_as_resolution": False,
            "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
            "c5_reconsideration_ready": False,
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
            "skeleton_freeze": rel(SKELETON_FREEZE_PATH),
            "route_map_freeze": rel(ROUTE_MAP_FREEZE_PATH),
            "nonresolution_freeze": rel(NONRESOLUTION_FREEZE_PATH),
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
    print(f"weak_feedback_resolution_target_closure_receipt_id={receipt_id}")
    print(f"weak_feedback_resolution_target_closure_receipt_path={rel(receipt_path)}")
    print(f"weak_feedback_resolution_target_closure_record_path={rel(CLOSURE_RECORD_PATH)}")
    print(f"weak_feedback_resolution_target_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"weak_feedback_resolution_skeleton_freeze_path={rel(SKELETON_FREEZE_PATH)}")
    print(f"weak_feedback_resolution_route_map_freeze_path={rel(ROUTE_MAP_FREEZE_PATH)}")
    print(f"weak_feedback_resolution_nonresolution_freeze_path={rel(NONRESOLUTION_FREEZE_PATH)}")
    print(f"weak_feedback_resolution_target_c5_block_freeze_path={rel(C5_BLOCK_FREEZE_PATH)}")
    print(f"weak_feedback_resolution_target_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"weak_feedback_resolution_target_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
