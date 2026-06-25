#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_target_review.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_TARGET_REVIEW"
MODE = "REVIEW / STATIC_RESOLUTION_TARGET_SURFACE / NO_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_TARGET_REVIEW_ONLY"

RT_BUILD_RECEIPT_ID = "16f7210b"
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
RT_BUILD_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_target_build_authority_boundary_v0.json"
RT_BUILD_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_target_build_classification_v0.json"
RT_BUILD_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_target_build_rollup_v0.json"
RT_BUILD_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_target_build_profile_v0.json"
RT_BUILD_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_target_build_report.json"
RT_BUILD_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_target_build_transition_trace.json"

RT_DESIGN_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0_receipts/e9765563.json"
RT_TARGET_DEFINITION_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_target_definition_v0.json"
RT_RESOLUTION_GATE_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_gate_contract_v0.json"
RT_C5_RECONSIDERATION_RULE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_c5_reconsideration_rule_v0.json"

REQUIRED_SOURCE_FILES = [
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
    RT_BUILD_AUTHORITY_PATH,
    RT_BUILD_CLASSIFICATION_PATH,
    RT_BUILD_ROLLUP_PATH,
    RT_BUILD_PROFILE_PATH,
    RT_BUILD_REPORT_PATH,
    RT_BUILD_TRACE_PATH,
    RT_DESIGN_RECEIPT_PATH,
    RT_TARGET_DEFINITION_PATH,
    RT_RESOLUTION_GATE_CONTRACT_PATH,
    RT_C5_RECONSIDERATION_RULE_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_target_review_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_target_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_review_assessment_v0.json"
SKELETON_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_resolution_skeleton_review_v0.json"
ROUTE_MAP_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_resolution_route_map_review_v0.json"
GATE_READOUT_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_resolution_gate_readout_review_v0.json"
C5_READOUT_REVIEW_PATH = OUT_DIR / "o2_c5_reconsideration_readout_review_v0.json"
NONRESOLUTION_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_resolution_nonresolution_review_v0.json"
CLOSURE_CANDIDATE_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_closure_candidate_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_review_downstream_decision_table_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_review_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_review_report.json"
TRACE_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_review_transition_trace.json"

EXPECTED_BUILD_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_STATIC_SURFACE_EMITTED_REVIEW_READY"
EXPECTED_BUILD_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_STATIC_SURFACE_EMITTED_REVIEW_READY"
EXPECTED_BUILD_NEXT = "REVIEW_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_V0"

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

    receipt = read_json(RT_BUILD_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_resolution_target_build_summary", {})
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
    authority = read_json(RT_BUILD_AUTHORITY_PATH)
    build_classification = read_json(RT_BUILD_CLASSIFICATION_PATH)
    build_rollup = read_json(RT_BUILD_ROLLUP_PATH)
    build_profile = read_json(RT_BUILD_PROFILE_PATH)
    build_report = read_json(RT_BUILD_REPORT_PATH)
    build_trace = read_json(RT_BUILD_TRACE_PATH)

    design_receipt = read_json(RT_DESIGN_RECEIPT_PATH)
    target_definition = read_json(RT_TARGET_DEFINITION_PATH)
    gate_contract = read_json(RT_RESOLUTION_GATE_CONTRACT_PATH)
    c5_rule = read_json(RT_C5_RECONSIDERATION_RULE_PATH)

    if receipt.get("receipt_id") != RT_BUILD_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("resolution_target_build_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_BUILD_STOP:
        failures.append("resolution_target_build_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("resolution_target_build_hidden_next_command")
    if summary.get("status") != EXPECTED_BUILD_STATUS:
        failures.append(f"resolution_target_build_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_BUILD_NEXT:
        failures.append(f"resolution_target_build_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "resolution_target_surface_built",
        "input_mapping_emitted",
        "resolution_gate_readout_emitted",
        "c5_reconsideration_readout_emitted",
        "nonresolution_attested",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "question_answer_skeletons_emitted": 3,
        "source_ref_satisfaction_skeletons_emitted": 2,
        "under_typed_acceptance_review_skeletons_emitted": 2,
        "parking_continuation_skeletons_emitted": 3,
        "weak_feedback_route_map_records_emitted": 3,
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

    if surface.get("surface_status") != "STATIC_RESOLUTION_TARGET_SURFACE_EMITTED":
        failures.append("surface_status_wrong")
    if mapping.get("weak_records_mapped_count") != 3:
        failures.append("mapping_weak_record_count_wrong")
    if len(questions) != 3 or len(source_refs) != 2 or len(undertyped) != 2 or len(parking) != 3 or len(route_map) != 3:
        failures.append("skeleton_or_route_count_wrong")

    for row in questions:
        if row.get("review_status") != "NOT_ANSWERED":
            failures.append(f"question_skeleton_status_wrong:{row.get('answer_skeleton_id')}")
        if row.get("counts_as_resolution_input") is not False:
            failures.append(f"question_skeleton_counts_resolution:{row.get('answer_skeleton_id')}")
        if row.get("c5_unblock_allowed") is not False:
            failures.append(f"question_skeleton_unblocks_c5:{row.get('answer_skeleton_id')}")

    for row in source_refs:
        if row.get("review_status") != "UNSATISFIED":
            failures.append(f"source_ref_skeleton_status_wrong:{row.get('satisfaction_skeleton_id')}")
        if row.get("counts_as_resolution_input") is not False:
            failures.append(f"source_ref_skeleton_counts_resolution:{row.get('satisfaction_skeleton_id')}")
        if row.get("provided_source_refs") != []:
            failures.append(f"source_ref_skeleton_has_sources:{row.get('satisfaction_skeleton_id')}")

    for row in undertyped:
        if row.get("review_status") != "UNREVIEWED":
            failures.append(f"undertyped_skeleton_status_wrong:{row.get('review_skeleton_id')}")
        if row.get("review_decision") != "UNREVIEWED":
            failures.append(f"undertyped_skeleton_decision_wrong:{row.get('review_skeleton_id')}")
        if row.get("c5_unblock_allowed") is not False:
            failures.append(f"undertyped_skeleton_unblocks_c5:{row.get('review_skeleton_id')}")

    for row in parking:
        if row.get("counts_as_resolution") is not False:
            failures.append(f"parking_skeleton_counts_resolution:{row.get('parking_continuation_skeleton_id')}")
        if row.get("review_status") != "PARKED_UNRESOLVED":
            failures.append(f"parking_skeleton_status_wrong:{row.get('parking_continuation_skeleton_id')}")
        if row.get("c5_unblock_allowed") is not False:
            failures.append(f"parking_skeleton_unblocks_c5:{row.get('parking_continuation_skeleton_id')}")

    for row in route_map:
        if row.get("current_resolution_state") != "UNRESOLVED":
            failures.append(f"route_state_wrong:{row.get('route_map_record_id')}")
        if row.get("resolution_decision") != "NOT_EVALUATED":
            failures.append(f"route_decision_wrong:{row.get('route_map_record_id')}")
        if row.get("review_status") != "TARGET_SURFACE_ONLY":
            failures.append(f"route_status_wrong:{row.get('route_map_record_id')}")
        if row.get("c5_reconsideration_ready") is not False:
            failures.append(f"route_c5_ready:{row.get('route_map_record_id')}")

    if gate_readout.get("weak_feedback_resolved") is not False:
        failures.append("gate_readout_resolved")
    if gate_readout.get("resolution_records_emitted_count") != 0:
        failures.append("gate_readout_resolution_records_nonzero")
    if c5_readout.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_readout.get("c5_opened") is not False or c5_readout.get("c5_reconsideration_ready") is not False:
        failures.append("c5_readout_wrong")
    if nonresolution.get("weak_feedback_resolved") is not False or nonresolution.get("c5_opened") is not False:
        failures.append("nonresolution_attestation_wrong")
    if authority.get("may_review_o2_weak_feedback_resolution_target_next") is not True:
        failures.append("authority_no_review_next")
    if authority.get("may_open_c5") is not False:
        failures.append("authority_allows_c5")
    if build_classification.get("recommended_next") != EXPECTED_BUILD_NEXT:
        failures.append("classification_next_wrong")

    for key in [
        "weak_feedback_resolved_count",
        "resolution_records_emitted_count",
        "question_packets_answered_count",
        "source_ref_requests_satisfied_count",
        "under_typed_acceptance_approved_count",
        "parked_records_counted_as_resolved_count",
        "c5_opened_count",
        "c5_reconsideration_ready_count",
    ]:
        if build_rollup.get(key) != 0:
            failures.append(f"build_rollup_counter_nonzero:{key}:{build_rollup.get(key)}")

    if build_profile.get("bad_counters_zero") is not True:
        failures.append("build_profile_bad_counters_not_true")
    if build_profile.get("next_command_goal") is not None:
        failures.append("build_profile_hidden_next")
    if build_report.get("recommended_next_handling") != EXPECTED_BUILD_NEXT:
        failures.append("build_report_next_wrong")
    if build_trace.get("terminal", {}).get("stop_code") != EXPECTED_BUILD_STOP:
        failures.append("build_trace_stop_wrong")

    if design_receipt.get("receipt_id") != "e9765563":
        failures.append("design_receipt_wrong")
    if target_definition.get("target_mode_for_build") != "STATIC_RESOLUTION_TARGET_BUILD_ONLY":
        failures.append("target_definition_mode_wrong")
    if gate_contract.get("design_unit_emits_resolution_records") is not False:
        failures.append("gate_contract_design_emits_resolution")
    if c5_rule.get("design_unit_can_unblock_c5") is not False:
        failures.append("c5_rule_design_unblocks_c5")

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

    review_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_REVIEWED_STATIC_SURFACE_CLEAN_CLOSE_READY" if review_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_REVIEW_GATE_FAIL"
    recommended_next = "CLOSE_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_AS_REVIEWED_REFERENCE_V0" if review_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_REVIEW_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_TARGET_REVIEW_COMPLETE",
        "WEAK_FEEDBACK_RESOLUTION_TARGET_REVIEW_PASS",
        "BUILD_RECEIPT_CONSUMED",
        "QUESTION_ANSWER_SKELETONS_REVIEWED_NOT_ANSWERED",
        "SOURCE_REF_SATISFACTION_SKELETONS_REVIEWED_UNSATISFIED",
        "UNDER_TYPED_ACCEPTANCE_REVIEW_SKELETONS_REVIEWED_UNREVIEWED",
        "PARKING_CONTINUATION_SKELETONS_REVIEWED_NOT_RESOLUTION",
        "ROUTE_MAP_REVIEWED_UNRESOLVED",
        "RESOLUTION_GATE_REVIEWED_NOT_RESOLVED",
        "C5_RECONSIDERATION_REVIEWED_BLOCKED",
        "NONRESOLUTION_CONFIRMED",
        "CLOSURE_CANDIDATE_READY",
        "NO_WEAK_FEEDBACK_RESOLUTION_ATTEMPTED",
        "NO_QUESTION_PACKET_ANSWERED",
        "NO_SOURCE_REF_REQUEST_SATISFIED",
        "NO_UNDER_TYPED_ACCEPTANCE_APPROVED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_TARGET_SELECTED_FOR_BUILD",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
        "NO_C5_OPENED",
    ] if review_pass else failures

    review_assessment = {
        "schema_version": "o2_weak_feedback_resolution_target_review_assessment_v0",
        "review_status": status,
        "source_resolution_target_build_receipt_id": RT_BUILD_RECEIPT_ID,
        "review_complete": review_pass,
        "review_pass": review_pass,
        "question_answer_skeletons_reviewed": len(questions),
        "source_ref_satisfaction_skeletons_reviewed": len(source_refs),
        "under_typed_acceptance_review_skeletons_reviewed": len(undertyped),
        "parking_continuation_skeletons_reviewed": len(parking),
        "route_map_records_reviewed": len(route_map),
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "closure_candidate_ready": review_pass,
        "recommended_next": recommended_next,
    }

    skeleton_review = {
        "schema_version": "o2_weak_feedback_resolution_skeleton_review_v0",
        "review_status": "SKELETON_REVIEW_PASS" if review_pass else "SKELETON_REVIEW_FAIL",
        "question_answer_skeletons": {
            "count": len(questions),
            "all_not_answered": all(x.get("review_status") == "NOT_ANSWERED" for x in questions),
            "all_not_resolution_input": all(x.get("counts_as_resolution_input") is False for x in questions),
        },
        "source_ref_satisfaction_skeletons": {
            "count": len(source_refs),
            "all_unsatisfied": all(x.get("review_status") == "UNSATISFIED" for x in source_refs),
            "all_not_resolution_input": all(x.get("counts_as_resolution_input") is False for x in source_refs),
        },
        "under_typed_acceptance_review_skeletons": {
            "count": len(undertyped),
            "all_unreviewed": all(x.get("review_status") == "UNREVIEWED" for x in undertyped),
            "all_c5_unblock_false": all(x.get("c5_unblock_allowed") is False for x in undertyped),
        },
        "parking_continuation_skeletons": {
            "count": len(parking),
            "all_not_resolution": all(x.get("counts_as_resolution") is False for x in parking),
            "all_parked_unresolved": all(x.get("review_status") == "PARKED_UNRESOLVED" for x in parking),
        },
    }

    route_review = {
        "schema_version": "o2_weak_feedback_resolution_route_map_review_v0",
        "review_status": "ROUTE_MAP_REVIEW_PASS" if review_pass else "ROUTE_MAP_REVIEW_FAIL",
        "route_map_records_reviewed": len(route_map),
        "all_unresolved": all(x.get("current_resolution_state") == "UNRESOLVED" for x in route_map),
        "all_not_evaluated": all(x.get("resolution_decision") == "NOT_EVALUATED" for x in route_map),
        "all_target_surface_only": all(x.get("review_status") == "TARGET_SURFACE_ONLY" for x in route_map),
        "all_c5_reconsideration_false": all(x.get("c5_reconsideration_ready") is False for x in route_map),
    }

    gate_review = {
        "schema_version": "o2_weak_feedback_resolution_gate_readout_review_v0",
        "review_status": "RESOLUTION_GATE_REVIEW_PASS" if review_pass else "RESOLUTION_GATE_REVIEW_FAIL",
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "question_packets_answered_count": 0,
        "source_ref_requests_satisfied_count": 0,
        "under_typed_acceptance_approved_count": 0,
        "parking_counted_as_resolution_count": 0,
        "resolution_requires_later_review": True,
    }

    c5_review = {
        "schema_version": "o2_c5_reconsideration_readout_review_v0",
        "review_status": "C5_RECONSIDERATION_REVIEW_PASS" if review_pass else "C5_RECONSIDERATION_REVIEW_FAIL",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_opened": False,
        "c5_reconsideration_ready": False,
        "reason": "Static resolution target surface has no reviewed resolution records.",
    }

    nonresolution_review = {
        "schema_version": "o2_weak_feedback_resolution_nonresolution_review_v0",
        "review_status": "NONRESOLUTION_CONFIRMED",
        "weak_feedback_resolved": False,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "resolution_records_emitted_count": 0,
        "c5_opened": False,
    }

    closure_candidate = {
        "schema_version": "o2_weak_feedback_resolution_target_closure_candidate_v0",
        "closure_candidate_status": "RESOLUTION_TARGET_CLOSE_READY_UNRESOLVED" if review_pass else "RESOLUTION_TARGET_CLOSE_NOT_READY",
        "review_pass": review_pass,
        "reviewed_reference_candidate": "o2_weak_feedback_resolution_target_static_surface_v0",
        "closure_meaning": "Close static resolution target surface as reviewed reference while preserving unresolved weak feedback and C5 block.",
        "closure_does_not_mean": [
            "weak feedback resolved",
            "question packets answered",
            "source-ref requests satisfied",
            "under-typed acceptance approved",
            "parking counted as resolution",
            "C5 reconsideration ready",
            "C5 opened",
        ],
        "recommended_next": recommended_next,
    }

    downstream_decision_table = {
        "schema_version": "o2_weak_feedback_resolution_target_review_downstream_decision_table_v0",
        "decision_status": "CLOSE_READY" if review_pass else "REPAIR_REQUIRED",
        "records": [
            {
                "decision": "CLOSE_RESOLUTION_TARGET_AS_REVIEWED_REFERENCE",
                "selected": review_pass,
                "next_unit": recommended_next if review_pass else None,
                "why": "Static resolution target surface reviewed clean; no resolution or C5 unblock occurred.",
            },
            {
                "decision": "RESOLVE_WEAK_FEEDBACK_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Review proves the target surface only; resolution requires later authorized branch.",
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
        "schema_version": "o2_weak_feedback_resolution_target_review_authority_boundary_v0",
        "status": status,
        "may_close_resolution_target_as_reviewed_reference_next": review_pass,
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
        "schema_version": "o2_weak_feedback_resolution_target_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "review_complete": review_pass,
        "review_pass": review_pass,
        "closure_candidate_ready": review_pass,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_opened": False,
        "c5_reconsideration_ready": False,
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
        "schema_version": "o2_weak_feedback_resolution_target_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "question_answer_skeletons_reviewed_count": len(questions),
        "source_ref_satisfaction_skeletons_reviewed_count": len(source_refs),
        "under_typed_acceptance_review_skeletons_reviewed_count": len(undertyped),
        "parking_continuation_skeletons_reviewed_count": len(parking),
        "route_map_records_reviewed_count": len(route_map),
        "closure_candidate_ready_count": 1 if review_pass else 0,
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
        "schema_version": "o2_weak_feedback_resolution_target_review_profile_v0",
        "profile_id": "o2_wf_resolution_target_review_profile_" + sha8(rollup),
        "status": status,
        "review_pass": review_pass,
        "closure_candidate_ready": review_pass,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Close the resolution target surface as reviewed reference; do not treat review as resolution.",
        "must_not_infer": [
            "weak feedback resolved",
            "question packet answered",
            "source-ref request satisfied",
            "under-typed acceptance approved",
            "parking resolved weak feedback",
            "C5 opened",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_weak_feedback_resolution_target_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The weak-feedback resolution target surface reviewed clean. Skeletons are present at expected counts and do not count as answers, satisfaction, approval, or resolution. Route maps remain UNRESOLVED, no resolution records exist, C5 reconsideration is false, and C5 remains blocked.",
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_weak_feedback_resolution_target_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_resolution_target_build",
                "question": "did static resolution target surface build cleanly",
                "answer": "yes" if review_pass else "no",
                "taken": "review skeletons and route map",
            },
            {
                "step": "verify_nonresolution",
                "question": "do skeletons or route map resolve weak feedback",
                "answer": "no",
                "taken": "preserve unresolved state",
            },
            {
                "step": "verify_c5_block",
                "question": "is C5 reconsideration ready",
                "answer": "no",
                "taken": "emit closure candidate",
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
        (SKELETON_REVIEW_PATH, skeleton_review),
        (ROUTE_MAP_REVIEW_PATH, route_review),
        (GATE_READOUT_REVIEW_PATH, gate_review),
        (C5_READOUT_REVIEW_PATH, c5_review),
        (NONRESOLUTION_REVIEW_PATH, nonresolution_review),
        (CLOSURE_CANDIDATE_PATH, closure_candidate),
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
        "RT_REVIEW_0_BUILD_RECEIPT_CONSUMED": RT_BUILD_RECEIPT_PATH.exists(),
        "RT_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "RT_REVIEW_2_SKELETON_REVIEW_EMITTED": SKELETON_REVIEW_PATH.exists(),
        "RT_REVIEW_3_ROUTE_MAP_REVIEW_EMITTED": ROUTE_MAP_REVIEW_PATH.exists(),
        "RT_REVIEW_4_QUESTION_SKELETONS_NOT_ANSWERED": skeleton_review["question_answer_skeletons"]["all_not_answered"] is True,
        "RT_REVIEW_5_SOURCE_REF_SKELETONS_UNSATISFIED": skeleton_review["source_ref_satisfaction_skeletons"]["all_unsatisfied"] is True,
        "RT_REVIEW_6_UNDER_TYPED_SKELETONS_UNREVIEWED": skeleton_review["under_typed_acceptance_review_skeletons"]["all_unreviewed"] is True,
        "RT_REVIEW_7_PARKING_SKELETONS_NOT_RESOLUTION": skeleton_review["parking_continuation_skeletons"]["all_not_resolution"] is True,
        "RT_REVIEW_8_ROUTE_MAP_UNRESOLVED": route_review["all_unresolved"] is True,
        "RT_REVIEW_9_RESOLUTION_GATE_NOT_RESOLVED": gate_review["weak_feedback_resolved"] is False and gate_review["resolution_records_emitted_count"] == 0,
        "RT_REVIEW_10_C5_RECONSIDERATION_BLOCKED": c5_review["c5_opened"] is False and c5_review["c5_reconsideration_ready"] is False,
        "RT_REVIEW_11_NONRESOLUTION_CONFIRMED": nonresolution_review["weak_feedback_resolved"] is False,
        "RT_REVIEW_12_NO_RESOLUTION_ANSWER_SATISFY_APPROVE": rollup["weak_feedback_resolved_count"] == 0 and rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "RT_REVIEW_13_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "RT_REVIEW_14_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "RT_REVIEW_15_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "RT_REVIEW_16_CLOSURE_CANDIDATE_READY": closure_candidate["closure_candidate_status"] == "RESOLUTION_TARGET_CLOSE_READY_UNRESOLVED",
        "RT_REVIEW_17_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "RT_REVIEW_18_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "RT_REVIEW_19_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "review_pass": review_pass,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_resolution_target_review_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_resolution_target_build_receipt_id": RT_BUILD_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_resolution_target_review_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "review_complete": review_pass,
            "review_pass": review_pass,
            "question_answer_skeletons_reviewed": len(questions),
            "source_ref_satisfaction_skeletons_reviewed": len(source_refs),
            "under_typed_acceptance_review_skeletons_reviewed": len(undertyped),
            "parking_continuation_skeletons_reviewed": len(parking),
            "route_map_records_reviewed": len(route_map),
            "question_skeletons_not_answered": skeleton_review["question_answer_skeletons"]["all_not_answered"],
            "source_ref_skeletons_unsatisfied": skeleton_review["source_ref_satisfaction_skeletons"]["all_unsatisfied"],
            "under_typed_skeletons_unreviewed": skeleton_review["under_typed_acceptance_review_skeletons"]["all_unreviewed"],
            "parking_skeletons_not_resolution": skeleton_review["parking_continuation_skeletons"]["all_not_resolution"],
            "route_map_unresolved": route_review["all_unresolved"],
            "resolution_gate_not_resolved": gate_review["weak_feedback_resolved"] is False,
            "resolution_records_emitted_count": 0,
            "c5_reconsideration_ready": False,
            "c5_block_preserved": True,
            "closure_candidate_ready": review_pass,
            "weak_feedback_resolved": False,
            "question_packets_answered": False,
            "source_ref_requests_satisfied": False,
            "under_typed_acceptance_approved": False,
            "parking_counted_as_resolution": False,
            "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
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
            "skeleton_review": rel(SKELETON_REVIEW_PATH),
            "route_map_review": rel(ROUTE_MAP_REVIEW_PATH),
            "gate_readout_review": rel(GATE_READOUT_REVIEW_PATH),
            "c5_readout_review": rel(C5_READOUT_REVIEW_PATH),
            "nonresolution_review": rel(NONRESOLUTION_REVIEW_PATH),
            "closure_candidate": rel(CLOSURE_CANDIDATE_PATH),
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
    print(f"weak_feedback_resolution_target_review_receipt_id={receipt_id}")
    print(f"weak_feedback_resolution_target_review_receipt_path={rel(receipt_path)}")
    print(f"weak_feedback_resolution_target_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"weak_feedback_resolution_skeleton_review_path={rel(SKELETON_REVIEW_PATH)}")
    print(f"weak_feedback_resolution_route_map_review_path={rel(ROUTE_MAP_REVIEW_PATH)}")
    print(f"weak_feedback_resolution_gate_readout_review_path={rel(GATE_READOUT_REVIEW_PATH)}")
    print(f"c5_reconsideration_readout_review_path={rel(C5_READOUT_REVIEW_PATH)}")
    print(f"weak_feedback_resolution_target_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"weak_feedback_resolution_target_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
