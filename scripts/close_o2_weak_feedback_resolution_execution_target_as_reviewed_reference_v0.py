#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_execution_target_closure.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_CLOSURE"
MODE = "CLOSE / FREEZE_REVIEWED_EXECUTION_TARGET_REFERENCE / NO_EXECUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_CLOSURE_ONLY"

EXEC_REVIEW_RECEIPT_ID = "81c5d90f"
EXEC_REVIEW_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0_receipts/81c5d90f.json"
EXEC_REVIEW_ASSESSMENT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_weak_feedback_resolution_execution_target_review_assessment_v0.json"
EXEC_TEMPLATE_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_weak_feedback_resolution_execution_template_review_v0.json"
EXEC_PROPOSAL_ROUTE_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_weak_feedback_resolution_execution_proposal_route_review_v0.json"
EXEC_GATE_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_weak_feedback_resolution_execution_gate_review_v0.json"
EXEC_BOUNDARY_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_resolution_proposal_review_boundary_review_v0.json"
EXEC_C5_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_resolution_execution_c5_block_review_v0.json"
EXEC_ZERO_RECORD_REVIEW_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_resolution_execution_zero_record_review_v0.json"
EXEC_CLOSURE_CANDIDATE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_weak_feedback_resolution_execution_target_closure_candidate_v0.json"
EXEC_REVIEW_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_weak_feedback_resolution_execution_target_review_authority_boundary_v0.json"
EXEC_REVIEW_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_weak_feedback_resolution_execution_target_review_classification_v0.json"
EXEC_REVIEW_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_weak_feedback_resolution_execution_target_review_rollup_v0.json"
EXEC_REVIEW_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_weak_feedback_resolution_execution_target_review_profile_v0.json"
EXEC_REVIEW_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_weak_feedback_resolution_execution_target_review_report.json"
EXEC_REVIEW_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0/o2_weak_feedback_resolution_execution_target_review_transition_trace.json"

EXEC_BUILD_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0_receipts/3eb40de8.json"
EXEC_SURFACE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_target_surface_record_v0.json"
EXEC_MAPPING_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_input_mapping_v0.json"
EXEC_QA_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_question_answer_record_templates_v0.jsonl"
EXEC_SOURCE_REF_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_source_ref_satisfaction_record_templates_v0.jsonl"
EXEC_UNDERTYPED_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_under_typed_acceptance_review_record_templates_v0.jsonl"
EXEC_PARKING_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_parking_execution_continuation_record_templates_v0.jsonl"
EXEC_RESOLUTION_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_weak_feedback_resolution_record_templates_v0.jsonl"
EXEC_PROPOSAL_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_proposal_route_map_v0.jsonl"
EXEC_BUILD_GATE_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_gate_readout_v0.json"
EXEC_BUILD_BOUNDARY_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_resolution_proposal_review_boundary_readout_v0.json"
EXEC_BUILD_C5_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_resolution_execution_c5_block_enforcement_readout_v0.json"
EXEC_BUILD_ZERO_RECORD_ATTESTATION_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_resolution_execution_zero_record_attestation_v0.json"

REQUIRED_SOURCE_FILES = [
    EXEC_REVIEW_RECEIPT_PATH,
    EXEC_REVIEW_ASSESSMENT_PATH,
    EXEC_TEMPLATE_REVIEW_PATH,
    EXEC_PROPOSAL_ROUTE_REVIEW_PATH,
    EXEC_GATE_REVIEW_PATH,
    EXEC_BOUNDARY_REVIEW_PATH,
    EXEC_C5_REVIEW_PATH,
    EXEC_ZERO_RECORD_REVIEW_PATH,
    EXEC_CLOSURE_CANDIDATE_PATH,
    EXEC_REVIEW_AUTHORITY_PATH,
    EXEC_REVIEW_CLASSIFICATION_PATH,
    EXEC_REVIEW_ROLLUP_PATH,
    EXEC_REVIEW_PROFILE_PATH,
    EXEC_REVIEW_REPORT_PATH,
    EXEC_REVIEW_TRACE_PATH,
    EXEC_BUILD_RECEIPT_PATH,
    EXEC_SURFACE_PATH,
    EXEC_MAPPING_PATH,
    EXEC_QA_TEMPLATES_PATH,
    EXEC_SOURCE_REF_TEMPLATES_PATH,
    EXEC_UNDERTYPED_TEMPLATES_PATH,
    EXEC_PARKING_TEMPLATES_PATH,
    EXEC_RESOLUTION_TEMPLATES_PATH,
    EXEC_PROPOSAL_ROUTE_MAP_PATH,
    EXEC_BUILD_GATE_READOUT_PATH,
    EXEC_BUILD_BOUNDARY_READOUT_PATH,
    EXEC_BUILD_C5_READOUT_PATH,
    EXEC_BUILD_ZERO_RECORD_ATTESTATION_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0_receipts"

CLOSURE_RECORD_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_reviewed_reference_v0.json"
TEMPLATE_FREEZE_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_template_freeze_v0.json"
PROPOSAL_ROUTE_FREEZE_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_proposal_route_freeze_v0.json"
ZERO_RECORD_FREEZE_PATH = OUT_DIR / "o2_resolution_execution_zero_record_freeze_v0.json"
C5_BLOCK_FREEZE_PATH = OUT_DIR / "o2_resolution_execution_c5_block_freeze_v0.json"
RECEIPT_CHAIN_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_receipt_chain_v0.json"
BOUNDARY_LOCK_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_closure_boundary_lock_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_closure_downstream_decision_table_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_closure_report.json"
TRACE_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REVIEWED_STATIC_SURFACE_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REVIEWED_STATIC_SURFACE_CLEAN_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_AS_REVIEWED_REFERENCE_V0"
RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REFERENCE_CLOSURE_V0"

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

    receipt = read_json(EXEC_REVIEW_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_resolution_execution_target_review_summary", {})
    assessment = read_json(EXEC_REVIEW_ASSESSMENT_PATH)
    template_review = read_json(EXEC_TEMPLATE_REVIEW_PATH)
    route_review = read_json(EXEC_PROPOSAL_ROUTE_REVIEW_PATH)
    gate_review = read_json(EXEC_GATE_REVIEW_PATH)
    boundary_review = read_json(EXEC_BOUNDARY_REVIEW_PATH)
    c5_review = read_json(EXEC_C5_REVIEW_PATH)
    zero_review = read_json(EXEC_ZERO_RECORD_REVIEW_PATH)
    closure_candidate = read_json(EXEC_CLOSURE_CANDIDATE_PATH)
    review_authority = read_json(EXEC_REVIEW_AUTHORITY_PATH)
    review_classification = read_json(EXEC_REVIEW_CLASSIFICATION_PATH)
    review_rollup = read_json(EXEC_REVIEW_ROLLUP_PATH)
    review_profile = read_json(EXEC_REVIEW_PROFILE_PATH)
    review_report = read_json(EXEC_REVIEW_REPORT_PATH)
    review_trace = read_json(EXEC_REVIEW_TRACE_PATH)

    build_receipt = read_json(EXEC_BUILD_RECEIPT_PATH)
    surface = read_json(EXEC_SURFACE_PATH)
    mapping = read_json(EXEC_MAPPING_PATH)
    qa_templates = read_jsonl(EXEC_QA_TEMPLATES_PATH)
    source_templates = read_jsonl(EXEC_SOURCE_REF_TEMPLATES_PATH)
    undertyped_templates = read_jsonl(EXEC_UNDERTYPED_TEMPLATES_PATH)
    parking_templates = read_jsonl(EXEC_PARKING_TEMPLATES_PATH)
    resolution_templates = read_jsonl(EXEC_RESOLUTION_TEMPLATES_PATH)
    proposal_routes = read_jsonl(EXEC_PROPOSAL_ROUTE_MAP_PATH)
    build_gate = read_json(EXEC_BUILD_GATE_READOUT_PATH)
    build_boundary = read_json(EXEC_BUILD_BOUNDARY_READOUT_PATH)
    build_c5 = read_json(EXEC_BUILD_C5_READOUT_PATH)
    build_zero = read_json(EXEC_BUILD_ZERO_RECORD_ATTESTATION_PATH)

    if receipt.get("receipt_id") != EXEC_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("execution_target_review_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("execution_target_review_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("execution_target_review_hidden_next_command")
    if summary.get("status") != EXPECTED_REVIEW_STATUS:
        failures.append(f"execution_target_review_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append(f"execution_target_review_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "execution_target_review_complete",
        "execution_target_review_pass",
        "closure_candidate_ready",
        "templates_reviewed_as_templates_only",
        "proposal_routes_unresolved",
        "proposal_routes_proposed_record_emitted_false",
        "proposal_routes_reviewed_record_emitted_false",
        "execution_gate_not_executed",
        "proposal_review_boundary_not_crossed",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "question_answer_templates_reviewed_count": 3,
        "source_ref_satisfaction_templates_reviewed_count": 2,
        "under_typed_acceptance_review_templates_reviewed_count": 2,
        "parking_execution_continuation_templates_reviewed_count": 3,
        "proposed_resolution_record_templates_reviewed_count": 3,
        "proposal_route_map_records_reviewed_count": 3,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
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
        failures.append("assessment_closure_not_ready")
    if template_review.get("proposed_resolution_record_templates", {}).get("all_template_only") is not True:
        failures.append("template_review_resolution_not_template_only")
    if template_review.get("proposed_resolution_record_templates", {}).get("all_unreviewed") is not True:
        failures.append("template_review_resolution_not_unreviewed")
    if route_review.get("all_unresolved") is not True:
        failures.append("route_review_not_unresolved")
    if route_review.get("all_proposed_record_emitted_false") is not True or route_review.get("all_reviewed_record_emitted_false") is not True:
        failures.append("route_review_records_emitted")
    if gate_review.get("execution_attempted") is not False:
        failures.append("gate_review_executed")
    if boundary_review.get("template_layer_crossed_into_proposal_layer") is not False or boundary_review.get("proposal_layer_crossed_into_review_layer") is not False:
        failures.append("boundary_review_crossed")
    if c5_review.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_review.get("c5_reconsideration_ready") is not False or c5_review.get("c5_opened") is not False:
        failures.append("c5_review_wrong")
    if zero_review.get("resolution_records_emitted_count") != 0 or zero_review.get("proposed_resolution_records_emitted_count") != 0 or zero_review.get("reviewed_resolution_records_emitted_count") != 0:
        failures.append("zero_review_records_nonzero")
    if closure_candidate.get("closure_candidate_status") != "EXECUTION_TARGET_CLOSE_READY_TEMPLATES_ONLY_UNRESOLVED":
        failures.append("closure_candidate_wrong")
    if review_authority.get("may_close_execution_target_as_reviewed_reference_next") is not True:
        failures.append("review_authority_no_close")
    if review_authority.get("may_execute_resolution_now") is not False or review_authority.get("may_open_c5") is not False:
        failures.append("review_authority_allows_execution_or_c5")
    if review_classification.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append("review_classification_next_wrong")
    if review_rollup.get("closure_candidate_ready_count") != 1:
        failures.append("review_rollup_closure_candidate_wrong")
    if review_profile.get("closure_candidate_ready") is not True or review_profile.get("next_command_goal") is not None:
        failures.append("review_profile_wrong")
    if review_report.get("recommended_next_handling") != EXPECTED_REVIEW_NEXT:
        failures.append("review_report_next_wrong")
    if review_trace.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("review_trace_stop_wrong")

    if build_receipt.get("receipt_id") != "3eb40de8":
        failures.append("build_receipt_wrong")
    if surface.get("surface_status") != "STATIC_EXECUTION_TARGET_SURFACE_EMITTED":
        failures.append("surface_status_wrong")
    if mapping.get("proposed_resolution_record_templates_count") != 3:
        failures.append("mapping_resolution_template_count_wrong")
    if len(qa_templates) != 3 or len(source_templates) != 2 or len(undertyped_templates) != 2 or len(parking_templates) != 3 or len(resolution_templates) != 3 or len(proposal_routes) != 3:
        failures.append("source_template_counts_wrong")
    if build_gate.get("proposed_resolution_records_emitted_count") != 0 or build_gate.get("reviewed_resolution_records_emitted_count") != 0:
        failures.append("build_gate_records_nonzero")
    if build_boundary.get("template_layer_crossed_into_proposal_layer") is not False or build_boundary.get("proposal_layer_crossed_into_review_layer") is not False:
        failures.append("build_boundary_crossed")
    if build_c5.get("c5_opened") is not False or build_c5.get("c5_reconsideration_ready") is not False:
        failures.append("build_c5_wrong")
    if build_zero.get("resolution_records_emitted_count") != 0 or build_zero.get("proposed_resolution_records_emitted_count") != 0:
        failures.append("build_zero_wrong")

    for row in proposal_routes:
        if row.get("current_resolution_state") != "UNRESOLVED":
            failures.append(f"proposal_route_not_unresolved:{row.get('proposal_route_record_id')}")
        if row.get("proposed_record_emitted") is not False or row.get("reviewed_record_emitted") is not False:
            failures.append(f"proposal_route_emitted:{row.get('proposal_route_record_id')}")
        if row.get("c5_reconsideration_ready") is not False:
            failures.append(f"proposal_route_c5_ready:{row.get('proposal_route_record_id')}")

    return failures, {
        "summary": summary,
        "qa_templates": qa_templates,
        "source_templates": source_templates,
        "undertyped_templates": undertyped_templates,
        "parking_templates": parking_templates,
        "resolution_templates": resolution_templates,
        "proposal_routes": proposal_routes,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    qa_templates = src.get("qa_templates", [])
    source_templates = src.get("source_templates", [])
    undertyped_templates = src.get("undertyped_templates", [])
    parking_templates = src.get("parking_templates", [])
    resolution_templates = src.get("resolution_templates", [])
    proposal_routes = src.get("proposal_routes", [])

    closure_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED_DECISION_READY" if closure_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if closure_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_CLOSURE_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_CLOSED_AS_REVIEWED_REFERENCE",
        "EXECUTION_TARGET_REVIEW_RECEIPT_CONSUMED",
        "REVIEWED_TEMPLATE_SURFACE_FROZEN",
        "REVIEWED_PROPOSAL_ROUTE_MAP_FROZEN_UNRESOLVED",
        "REVIEWED_EXECUTION_GATE_NOT_EXECUTED_FROZEN",
        "REVIEWED_PROPOSAL_REVIEW_BOUNDARY_NOT_CROSSED_FROZEN",
        "REVIEWED_ZERO_RECORD_STATUS_FROZEN",
        "REVIEWED_C5_BLOCK_STATUS_FROZEN",
        "POST_CLOSURE_DECISION_READY",
        "NO_RESOLUTION_EXECUTION_ATTEMPTED",
        "NO_PROPOSED_RESOLUTION_RECORDS_EMITTED",
        "NO_REVIEWED_RESOLUTION_RECORDS_EMITTED",
        "NO_QUESTION_PACKET_ANSWERED",
        "NO_SOURCE_REF_REQUEST_SATISFIED",
        "NO_UNDER_TYPED_ACCEPTANCE_APPROVED",
        "NO_PARKING_COUNTED_AS_RESOLUTION",
        "NO_C5_RECONSIDERATION_READY",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if closure_pass else failures

    closure_record = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_closure_record_v0",
        "closure_status": "CLOSED_AS_REVIEWED_REFERENCE_UNRESOLVED" if closure_pass else "CLOSURE_NOT_RECORDED",
        "source_execution_target_review_receipt_id": EXEC_REVIEW_RECEIPT_ID,
        "closed_object": "o2_weak_feedback_resolution_execution_target_static_surface_v0",
        "closure_meaning": "Reviewed static execution-target surface is frozen as a reference.",
        "closure_does_not_mean": [
            "execution occurred",
            "proposed records emitted",
            "reviewed resolution records emitted",
            "weak feedback resolved",
            "C5 reconsideration ready",
            "C5 opened",
        ],
    }

    reviewed_reference = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_reviewed_reference_v0",
        "reference_status": "FROZEN_REVIEWED_REFERENCE" if closure_pass else "REFERENCE_NOT_FROZEN",
        "reference_object_id": "o2_wf_execution_target_reviewed_reference_" + sha8({
            "review_receipt": EXEC_REVIEW_RECEIPT_ID,
            "qa": len(qa_templates),
            "source": len(source_templates),
            "undertyped": len(undertyped_templates),
            "parking": len(parking_templates),
            "resolution": len(resolution_templates),
            "routes": len(proposal_routes),
        }),
        "source_execution_target_review_receipt_id": EXEC_REVIEW_RECEIPT_ID,
        "source_execution_target_build_receipt_id": "3eb40de8",
        "source_execution_target_design_receipt_id": "0fea0528",
        "reviewed_surface_counts": {
            "question_answer_templates": len(qa_templates),
            "source_ref_satisfaction_templates": len(source_templates),
            "under_typed_acceptance_review_templates": len(undertyped_templates),
            "parking_execution_continuation_templates": len(parking_templates),
            "proposed_resolution_record_templates": len(resolution_templates),
            "proposal_route_map_records": len(proposal_routes),
        },
        "templates_are_not_proposed_records": True,
        "proposed_records_are_not_reviewed_records": True,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    template_freeze = {
        "schema_version": "o2_weak_feedback_resolution_execution_template_freeze_v0",
        "freeze_status": "REVIEWED_TEMPLATES_FROZEN_AS_TEMPLATES_ONLY",
        "question_answer_templates_frozen_count": len(qa_templates),
        "source_ref_satisfaction_templates_frozen_count": len(source_templates),
        "under_typed_acceptance_review_templates_frozen_count": len(undertyped_templates),
        "parking_execution_continuation_templates_frozen_count": len(parking_templates),
        "proposed_resolution_record_templates_frozen_count": len(resolution_templates),
        "templates_are_not_proposed_records": True,
        "templates_are_not_reviewed_records": True,
    }

    proposal_route_freeze = {
        "schema_version": "o2_weak_feedback_resolution_execution_proposal_route_freeze_v0",
        "freeze_status": "REVIEWED_PROPOSAL_ROUTE_MAP_FROZEN_UNRESOLVED",
        "proposal_route_map_records_frozen_count": len(proposal_routes),
        "all_unresolved": True,
        "proposed_records_emitted_count": 0,
        "reviewed_records_emitted_count": 0,
        "c5_reconsideration_ready": False,
    }

    zero_record_freeze = {
        "schema_version": "o2_resolution_execution_zero_record_freeze_v0",
        "freeze_status": "ZERO_RECORD_STATUS_FROZEN",
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "weak_feedback_resolved": False,
    }

    c5_block_freeze = {
        "schema_version": "o2_resolution_execution_c5_block_freeze_v0",
        "freeze_status": "C5_BLOCK_STATUS_FROZEN",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "closure_does_not_unblock_c5": True,
    }

    receipt_chain = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_receipt_chain_v0",
        "chain_status": "RECEIPT_CHAIN_PRESERVED",
        "receipts": [
            {"stage": "resolution_target_post_closure_decision", "receipt_id": "1100f482"},
            {"stage": "execution_target_design", "receipt_id": "0fea0528"},
            {"stage": "execution_target_build", "receipt_id": "3eb40de8"},
            {"stage": "execution_target_review", "receipt_id": EXEC_REVIEW_RECEIPT_ID},
        ],
        "closure_receipt_pending": True,
    }

    boundary_lock = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_closure_boundary_lock_v0",
        "boundary_lock_status": "BOUNDARIES_LOCKED_AT_CLOSURE",
        "execution_target_closed_as_reviewed_reference": closure_pass,
        "templates_are_not_proposed_records": True,
        "proposed_records_are_not_reviewed_records": True,
        "execution_attempted": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
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
        "schema_version": "o2_weak_feedback_resolution_execution_target_closure_downstream_decision_table_v0",
        "decision_status": "POST_CLOSURE_DECISION_READY" if closure_pass else "CLOSURE_REPAIR_REQUIRED",
        "records": [
            {
                "decision": "DECIDE_NEXT_AFTER_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REFERENCE_CLOSURE",
                "selected": closure_pass,
                "next_unit": recommended_next if closure_pass else None,
                "why": "Execution-target reference is closed, but no proposed or reviewed records exist and C5 remains blocked.",
            },
            {
                "decision": "EXECUTE_RESOLUTION_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Closure only freezes the reviewed template surface. Execution requires a later explicit decision and authorization.",
            },
            {
                "decision": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 remains blocked because weak feedback is unresolved and no reviewed resolution records exist.",
            },
        ],
    }

    authority_boundary = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_execution_target_reference_closure": closure_pass,
        "may_execute_resolution_now": False,
        "may_emit_proposed_resolution_records_now": False,
        "may_emit_reviewed_resolution_records_now": False,
        "may_resolve_weak_feedback_now": False,
        "may_answer_question_packets_now": False,
        "may_satisfy_source_ref_requests_now": False,
        "may_approve_under_typed_acceptance_now": False,
        "may_count_parking_as_resolution": False,
        "may_set_c5_reconsideration_ready": False,
        "may_open_c5": False,
        "may_run_live_feedback_audit_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_select_target_for_build": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
    }

    classification = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "execution_target_closed_as_reviewed_reference": closure_pass,
        "reviewed_reference_emitted": closure_pass,
        "post_closure_decision_ready": closure_pass,
        "templates_frozen_as_templates_only": closure_pass,
        "execution_attempted": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
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
        "schema_version": "o2_weak_feedback_resolution_execution_target_closure_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "closure_count": 1 if closure_pass else 0,
        "reviewed_reference_emitted_count": 1 if closure_pass else 0,
        "post_closure_decision_ready_count": 1 if closure_pass else 0,
        "question_answer_templates_frozen_count": len(qa_templates),
        "source_ref_satisfaction_templates_frozen_count": len(source_templates),
        "under_typed_acceptance_review_templates_frozen_count": len(undertyped_templates),
        "parking_execution_continuation_templates_frozen_count": len(parking_templates),
        "proposed_resolution_record_templates_frozen_count": len(resolution_templates),
        "proposal_route_map_records_frozen_count": len(proposal_routes),
        "weak_feedback_resolved_count": 0,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
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
        "proposed_resolution_records_emitted_count",
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
        "schema_version": "o2_weak_feedback_resolution_execution_target_closure_profile_v0",
        "profile_id": "o2_wf_resolution_execution_target_closure_profile_" + sha8(rollup),
        "status": status,
        "execution_target_closed_as_reviewed_reference": closure_pass,
        "templates_frozen_as_templates_only": closure_pass,
        "execution_attempted": False,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Decide next after closing the execution-target reference. Do not treat closure as execution or resolution.",
        "must_not_infer": [
            "weak feedback resolved",
            "proposed records emitted",
            "reviewed resolution records emitted",
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
        "schema_version": "o2_weak_feedback_resolution_execution_target_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The weak-feedback resolution execution target was closed as a reviewed reference. Templates, proposal routes, zero-record status, proposal/review boundary, and C5-block status were frozen. No execution occurred, no proposed or reviewed resolution records were emitted, weak feedback remains unresolved, and C5 remains blocked.",
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_execution_target_review",
                "question": "is execution-target static surface reviewed clean and close-ready",
                "answer": "yes" if closure_pass else "no",
                "taken": "freeze reviewed execution-target reference",
            },
            {
                "step": "freeze_template_only_boundary",
                "question": "do templates become proposed or reviewed records by closure",
                "answer": "no",
                "taken": "freeze zero-record status",
            },
            {
                "step": "preserve_c5_block",
                "question": "does closure unblock C5",
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
        (TEMPLATE_FREEZE_PATH, template_freeze),
        (PROPOSAL_ROUTE_FREEZE_PATH, proposal_route_freeze),
        (ZERO_RECORD_FREEZE_PATH, zero_record_freeze),
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
        "EXEC_TARGET_CLOSE_0_REVIEW_RECEIPT_CONSUMED": EXEC_REVIEW_RECEIPT_PATH.exists(),
        "EXEC_TARGET_CLOSE_1_CLOSURE_RECORD_EMITTED": CLOSURE_RECORD_PATH.exists(),
        "EXEC_TARGET_CLOSE_2_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists(),
        "EXEC_TARGET_CLOSE_3_TEMPLATE_FREEZE_EMITTED": TEMPLATE_FREEZE_PATH.exists(),
        "EXEC_TARGET_CLOSE_4_PROPOSAL_ROUTE_FREEZE_EMITTED": PROPOSAL_ROUTE_FREEZE_PATH.exists(),
        "EXEC_TARGET_CLOSE_5_ZERO_RECORD_FREEZE_EMITTED": ZERO_RECORD_FREEZE_PATH.exists(),
        "EXEC_TARGET_CLOSE_6_C5_BLOCK_FREEZE_EMITTED": C5_BLOCK_FREEZE_PATH.exists(),
        "EXEC_TARGET_CLOSE_7_TEMPLATES_STAY_TEMPLATES_ONLY": template_freeze["templates_are_not_proposed_records"] is True and template_freeze["templates_are_not_reviewed_records"] is True,
        "EXEC_TARGET_CLOSE_8_PROPOSAL_ROUTE_UNRESOLVED": proposal_route_freeze["all_unresolved"] is True,
        "EXEC_TARGET_CLOSE_9_ZERO_RECORDS_PRESERVED": zero_record_freeze["resolution_records_emitted_count"] == 0 and zero_record_freeze["proposed_resolution_records_emitted_count"] == 0 and zero_record_freeze["reviewed_resolution_records_emitted_count"] == 0,
        "EXEC_TARGET_CLOSE_10_C5_BLOCK_PRESERVED": c5_block_freeze["c5_opened"] is False and c5_block_freeze["c5_reconsideration_ready"] is False,
        "EXEC_TARGET_CLOSE_11_NO_EXECUTION_OR_RECORDS": rollup["resolution_records_emitted_count"] == 0 and rollup["proposed_resolution_records_emitted_count"] == 0 and rollup["reviewed_resolution_records_emitted_count"] == 0,
        "EXEC_TARGET_CLOSE_12_NO_RESOLUTION_ANSWER_SATISFY_APPROVE": rollup["weak_feedback_resolved_count"] == 0 and rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "EXEC_TARGET_CLOSE_13_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "EXEC_TARGET_CLOSE_14_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "EXEC_TARGET_CLOSE_15_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "EXEC_TARGET_CLOSE_16_NO_C5_RECONSIDERATION_READY": rollup["c5_reconsideration_ready_count"] == 0,
        "EXEC_TARGET_CLOSE_17_POST_CLOSURE_DECISION_READY": rollup["post_closure_decision_ready_count"] == 1,
        "EXEC_TARGET_CLOSE_18_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "EXEC_TARGET_CLOSE_19_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "EXEC_TARGET_CLOSE_20_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "closed": closure_pass,
        "records": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_closure_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_execution_target_review_receipt_id": EXEC_REVIEW_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_resolution_execution_target_closure_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "execution_target_closed_as_reviewed_reference": closure_pass,
            "reviewed_reference_emitted": closure_pass,
            "post_closure_decision_ready": closure_pass,
            "templates_frozen_as_templates_only": closure_pass,
            "question_answer_templates_frozen_count": len(qa_templates),
            "source_ref_satisfaction_templates_frozen_count": len(source_templates),
            "under_typed_acceptance_review_templates_frozen_count": len(undertyped_templates),
            "parking_execution_continuation_templates_frozen_count": len(parking_templates),
            "proposed_resolution_record_templates_frozen_count": len(resolution_templates),
            "proposal_route_map_records_frozen_count": len(proposal_routes),
            "execution_attempted": False,
            "weak_feedback_resolved": False,
            "resolution_records_emitted_count": 0,
            "proposed_resolution_records_emitted_count": 0,
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
            "template_freeze": rel(TEMPLATE_FREEZE_PATH),
            "proposal_route_freeze": rel(PROPOSAL_ROUTE_FREEZE_PATH),
            "zero_record_freeze": rel(ZERO_RECORD_FREEZE_PATH),
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
    print(f"weak_feedback_resolution_execution_target_closure_receipt_id={receipt_id}")
    print(f"weak_feedback_resolution_execution_target_closure_receipt_path={rel(receipt_path)}")
    print(f"weak_feedback_resolution_execution_target_closure_record_path={rel(CLOSURE_RECORD_PATH)}")
    print(f"weak_feedback_resolution_execution_target_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"weak_feedback_resolution_execution_template_freeze_path={rel(TEMPLATE_FREEZE_PATH)}")
    print(f"weak_feedback_resolution_execution_proposal_route_freeze_path={rel(PROPOSAL_ROUTE_FREEZE_PATH)}")
    print(f"resolution_execution_zero_record_freeze_path={rel(ZERO_RECORD_FREEZE_PATH)}")
    print(f"resolution_execution_c5_block_freeze_path={rel(C5_BLOCK_FREEZE_PATH)}")
    print(f"execution_target_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"execution_target_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
