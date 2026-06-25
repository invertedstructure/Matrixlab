#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_execution_target_review.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REVIEW"
MODE = "REVIEW / STATIC_RESOLUTION_EXECUTION_TARGET_SURFACE / NO_EXECUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REVIEW_ONLY"

EXEC_BUILD_RECEIPT_ID = "3eb40de8"
EXEC_BUILD_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0_receipts/3eb40de8.json"
EXEC_SURFACE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_target_surface_record_v0.json"
EXEC_MAPPING_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_input_mapping_v0.json"
EXEC_QA_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_question_answer_record_templates_v0.jsonl"
EXEC_SOURCE_REF_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_source_ref_satisfaction_record_templates_v0.jsonl"
EXEC_UNDERTYPED_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_under_typed_acceptance_review_record_templates_v0.jsonl"
EXEC_PARKING_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_parking_execution_continuation_record_templates_v0.jsonl"
EXEC_RESOLUTION_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_weak_feedback_resolution_record_templates_v0.jsonl"
EXEC_PROPOSAL_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_proposal_route_map_v0.jsonl"
EXEC_GATE_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_gate_readout_v0.json"
EXEC_BOUNDARY_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_resolution_proposal_review_boundary_readout_v0.json"
EXEC_C5_BLOCK_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_resolution_execution_c5_block_enforcement_readout_v0.json"
EXEC_ZERO_RECORD_ATTESTATION_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_resolution_execution_zero_record_attestation_v0.json"
EXEC_BUILD_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_target_build_authority_boundary_v0.json"
EXEC_BUILD_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_target_build_classification_v0.json"
EXEC_BUILD_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_target_build_rollup_v0.json"
EXEC_BUILD_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_target_build_profile_v0.json"
EXEC_BUILD_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_target_build_report.json"
EXEC_BUILD_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_target_build_transition_trace.json"

EXEC_DESIGN_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0_receipts/0fea0528.json"
EXEC_TARGET_DEFINITION_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_target_definition_v0.json"
EXEC_GATE_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_gate_contract_v0.json"
EXEC_PROPOSAL_REVIEW_BOUNDARY_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_resolution_proposal_review_boundary_v0.json"
EXEC_C5_BLOCK_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_resolution_execution_c5_block_contract_v0.json"

REQUIRED_SOURCE_FILES = [
    EXEC_BUILD_RECEIPT_PATH,
    EXEC_SURFACE_PATH,
    EXEC_MAPPING_PATH,
    EXEC_QA_TEMPLATES_PATH,
    EXEC_SOURCE_REF_TEMPLATES_PATH,
    EXEC_UNDERTYPED_TEMPLATES_PATH,
    EXEC_PARKING_TEMPLATES_PATH,
    EXEC_RESOLUTION_TEMPLATES_PATH,
    EXEC_PROPOSAL_ROUTE_MAP_PATH,
    EXEC_GATE_READOUT_PATH,
    EXEC_BOUNDARY_READOUT_PATH,
    EXEC_C5_BLOCK_READOUT_PATH,
    EXEC_ZERO_RECORD_ATTESTATION_PATH,
    EXEC_BUILD_AUTHORITY_PATH,
    EXEC_BUILD_CLASSIFICATION_PATH,
    EXEC_BUILD_ROLLUP_PATH,
    EXEC_BUILD_PROFILE_PATH,
    EXEC_BUILD_REPORT_PATH,
    EXEC_BUILD_TRACE_PATH,
    EXEC_DESIGN_RECEIPT_PATH,
    EXEC_TARGET_DEFINITION_PATH,
    EXEC_GATE_CONTRACT_PATH,
    EXEC_PROPOSAL_REVIEW_BOUNDARY_PATH,
    EXEC_C5_BLOCK_CONTRACT_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_execution_target_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_review_assessment_v0.json"
TEMPLATE_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_template_review_v0.json"
PROPOSAL_ROUTE_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_proposal_route_review_v0.json"
GATE_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_gate_review_v0.json"
BOUNDARY_REVIEW_PATH = OUT_DIR / "o2_resolution_proposal_review_boundary_review_v0.json"
C5_BLOCK_REVIEW_PATH = OUT_DIR / "o2_resolution_execution_c5_block_review_v0.json"
ZERO_RECORD_REVIEW_PATH = OUT_DIR / "o2_resolution_execution_zero_record_review_v0.json"
CLOSURE_CANDIDATE_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_closure_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_review_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_review_report.json"
TRACE_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_review_transition_trace.json"

EXPECTED_BUILD_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_STATIC_SURFACE_EMITTED_REVIEW_READY"
EXPECTED_BUILD_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_STATIC_SURFACE_EMITTED_REVIEW_READY"
EXPECTED_BUILD_NEXT = "REVIEW_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_V0"
RECOMMENDED_NEXT = "CLOSE_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_AS_REVIEWED_REFERENCE_V0"

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

def all_false(rows: List[Dict[str, Any]], keys: List[str]) -> bool:
    return all(all(row.get(k) is False for k in keys) for row in rows)

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(EXEC_BUILD_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_resolution_execution_target_build_summary", {})
    surface = read_json(EXEC_SURFACE_PATH)
    mapping = read_json(EXEC_MAPPING_PATH)
    qa_templates = read_jsonl(EXEC_QA_TEMPLATES_PATH)
    source_templates = read_jsonl(EXEC_SOURCE_REF_TEMPLATES_PATH)
    undertyped_templates = read_jsonl(EXEC_UNDERTYPED_TEMPLATES_PATH)
    parking_templates = read_jsonl(EXEC_PARKING_TEMPLATES_PATH)
    resolution_templates = read_jsonl(EXEC_RESOLUTION_TEMPLATES_PATH)
    proposal_routes = read_jsonl(EXEC_PROPOSAL_ROUTE_MAP_PATH)
    gate_readout = read_json(EXEC_GATE_READOUT_PATH)
    boundary_readout = read_json(EXEC_BOUNDARY_READOUT_PATH)
    c5_readout = read_json(EXEC_C5_BLOCK_READOUT_PATH)
    zero_attestation = read_json(EXEC_ZERO_RECORD_ATTESTATION_PATH)
    build_authority = read_json(EXEC_BUILD_AUTHORITY_PATH)
    build_classification = read_json(EXEC_BUILD_CLASSIFICATION_PATH)
    build_rollup = read_json(EXEC_BUILD_ROLLUP_PATH)
    build_profile = read_json(EXEC_BUILD_PROFILE_PATH)
    build_report = read_json(EXEC_BUILD_REPORT_PATH)
    build_trace = read_json(EXEC_BUILD_TRACE_PATH)

    design_receipt = read_json(EXEC_DESIGN_RECEIPT_PATH)
    target_definition = read_json(EXEC_TARGET_DEFINITION_PATH)
    gate_contract = read_json(EXEC_GATE_CONTRACT_PATH)
    proposal_boundary = read_json(EXEC_PROPOSAL_REVIEW_BOUNDARY_PATH)
    c5_contract = read_json(EXEC_C5_BLOCK_CONTRACT_PATH)

    if receipt.get("receipt_id") != EXEC_BUILD_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("execution_target_build_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_BUILD_STOP:
        failures.append("execution_target_build_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("execution_target_build_hidden_next_command")
    if summary.get("status") != EXPECTED_BUILD_STATUS:
        failures.append(f"execution_target_build_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_BUILD_NEXT:
        failures.append(f"execution_target_build_next_wrong:{summary.get('recommended_next')}")

    for key in [
        "execution_target_surface_built",
        "templates_emitted",
        "execution_gate_readout_emitted",
        "proposal_review_boundary_readout_emitted",
        "c5_block_enforcement_readout_emitted",
        "zero_record_attestation_emitted",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "question_answer_templates_count": 3,
        "source_ref_satisfaction_templates_count": 2,
        "under_typed_acceptance_review_templates_count": 2,
        "parking_execution_continuation_templates_count": 3,
        "proposed_resolution_record_templates_count": 3,
        "proposal_route_map_records_count": 3,
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
    if surface.get("surface_status") != "STATIC_EXECUTION_TARGET_SURFACE_EMITTED":
        failures.append("surface_status_wrong")
    if mapping.get("question_answer_templates_count") != 3:
        failures.append("mapping_qa_count_wrong")
    if len(qa_templates) != 3 or len(source_templates) != 2 or len(undertyped_templates) != 2 or len(parking_templates) != 3 or len(resolution_templates) != 3 or len(proposal_routes) != 3:
        failures.append("template_or_route_count_wrong")

    for row in qa_templates:
        if row.get("proposal_status") != "TEMPLATE_ONLY_NOT_PROPOSED":
            failures.append(f"qa_template_status_wrong:{row.get('template_id')}")
        if row.get("review_status") != "UNREVIEWED":
            failures.append(f"qa_template_review_status_wrong:{row.get('template_id')}")
        if row.get("counts_as_answer") is not False or row.get("counts_as_resolution_input") is not False:
            failures.append(f"qa_template_counts_wrong:{row.get('template_id')}")

    for row in source_templates:
        if row.get("proposal_status") != "TEMPLATE_ONLY_NOT_PROPOSED":
            failures.append(f"source_template_status_wrong:{row.get('template_id')}")
        if row.get("review_status") != "UNREVIEWED":
            failures.append(f"source_template_review_status_wrong:{row.get('template_id')}")
        if row.get("counts_as_satisfied") is not False or row.get("counts_as_resolution_input") is not False:
            failures.append(f"source_template_counts_wrong:{row.get('template_id')}")

    for row in undertyped_templates:
        if row.get("proposal_status") != "TEMPLATE_ONLY_NOT_PROPOSED":
            failures.append(f"undertyped_template_status_wrong:{row.get('template_id')}")
        if row.get("review_status") != "UNREVIEWED":
            failures.append(f"undertyped_template_review_status_wrong:{row.get('template_id')}")
        if row.get("counts_as_approved") is not False or row.get("c5_unblock_allowed") is not False:
            failures.append(f"undertyped_template_counts_wrong:{row.get('template_id')}")

    for row in parking_templates:
        if row.get("proposal_status") != "TEMPLATE_ONLY_PARKED_UNRESOLVED":
            failures.append(f"parking_template_status_wrong:{row.get('template_id')}")
        if row.get("review_status") != "UNREVIEWED":
            failures.append(f"parking_template_review_status_wrong:{row.get('template_id')}")
        if row.get("counts_as_resolution") is not False or row.get("c5_unblock_allowed") is not False:
            failures.append(f"parking_template_counts_wrong:{row.get('template_id')}")

    for row in resolution_templates:
        if row.get("proposal_status") != "TEMPLATE_ONLY":
            failures.append(f"resolution_template_status_wrong:{row.get('template_id')}")
        if row.get("review_status") != "UNREVIEWED":
            failures.append(f"resolution_template_review_status_wrong:{row.get('template_id')}")
        if row.get("counts_as_reviewed_resolution") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"resolution_template_counts_wrong:{row.get('template_id')}")

    for row in proposal_routes:
        if row.get("current_resolution_state") != "UNRESOLVED":
            failures.append(f"proposal_route_state_wrong:{row.get('proposal_route_record_id')}")
        if row.get("proposed_record_emitted") is not False or row.get("reviewed_record_emitted") is not False:
            failures.append(f"proposal_route_record_emitted:{row.get('proposal_route_record_id')}")
        if row.get("c5_reconsideration_ready") is not False:
            failures.append(f"proposal_route_c5_ready:{row.get('proposal_route_record_id')}")

    if gate_readout.get("gate_status") != "NOT_EXECUTED_REVIEW_REQUIRED":
        failures.append("gate_readout_status_wrong")
    if gate_readout.get("proposed_resolution_records_emitted_count") != 0 or gate_readout.get("reviewed_resolution_records_emitted_count", 0) != 0:
        failures.append("gate_readout_records_nonzero")
    if boundary_readout.get("template_layer_crossed_into_proposal_layer") is not False or boundary_readout.get("proposal_layer_crossed_into_review_layer") is not False:
        failures.append("boundary_crossed")
    if c5_readout.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_readout.get("c5_reconsideration_ready") is not False or c5_readout.get("c5_opened") is not False:
        failures.append("c5_readout_wrong")
    if zero_attestation.get("resolution_records_emitted_count") != 0 or zero_attestation.get("proposed_resolution_records_emitted_count") != 0:
        failures.append("zero_attestation_records_nonzero")
    if build_authority.get("may_review_o2_weak_feedback_resolution_execution_target_next") is not True:
        failures.append("build_authority_no_review_next")
    if build_authority.get("may_execute_resolution_now") is not False:
        failures.append("build_authority_allows_execution")
    if build_classification.get("recommended_next") != EXPECTED_BUILD_NEXT:
        failures.append("build_classification_next_wrong")
    if build_rollup.get("execution_target_surface_build_count") != 1:
        failures.append("build_rollup_surface_count_wrong")
    if build_profile.get("bad_counters_zero") is not True or build_profile.get("next_command_goal") is not None:
        failures.append("build_profile_wrong")
    if build_report.get("recommended_next_handling") != EXPECTED_BUILD_NEXT:
        failures.append("build_report_next_wrong")
    if build_trace.get("terminal", {}).get("stop_code") != EXPECTED_BUILD_STOP:
        failures.append("build_trace_stop_wrong")

    if design_receipt.get("receipt_id") != "0fea0528":
        failures.append("design_receipt_wrong")
    if target_definition.get("target_mode_for_build") != "STATIC_RESOLUTION_EXECUTION_TARGET_BUILD_ONLY":
        failures.append("target_definition_wrong")
    if gate_contract.get("design_unit_executes_gate") is not False:
        failures.append("gate_contract_executes")
    if proposal_boundary.get("design_unit_crosses_boundary") is not False:
        failures.append("proposal_boundary_design_crosses")
    if c5_contract.get("design_unit_can_unblock_c5") is not False:
        failures.append("c5_contract_design_unblocks")

    return failures, {
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

    review_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REVIEWED_STATIC_SURFACE_CLEAN_CLOSE_READY" if review_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REVIEW_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REVIEW_COMPLETE",
        "WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REVIEW_PASS",
        "EXECUTION_TARGET_BUILD_RECEIPT_CONSUMED",
        "TEMPLATES_REVIEWED_AS_TEMPLATES_ONLY",
        "PROPOSAL_ROUTE_MAP_REVIEWED_UNRESOLVED",
        "EXECUTION_GATE_REVIEWED_NOT_EXECUTED",
        "PROPOSAL_REVIEW_BOUNDARY_REVIEWED_NOT_CROSSED",
        "C5_BLOCK_REVIEWED_ENFORCED",
        "ZERO_RECORD_ATTESTATION_REVIEWED",
        "CLOSURE_CANDIDATE_READY",
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
    ] if review_pass else failures

    review_assessment = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_review_assessment_v0",
        "review_status": status,
        "review_complete": review_pass,
        "review_pass": review_pass,
        "source_execution_target_build_receipt_id": EXEC_BUILD_RECEIPT_ID,
        "closure_candidate_ready": review_pass,
        "recommended_next": recommended_next,
    }

    template_review = {
        "schema_version": "o2_weak_feedback_resolution_execution_template_review_v0",
        "review_status": "TEMPLATE_REVIEW_PASS" if review_pass else "TEMPLATE_REVIEW_FAIL",
        "question_answer_templates": {
            "count": len(qa_templates),
            "all_template_only": all(x.get("proposal_status") == "TEMPLATE_ONLY_NOT_PROPOSED" for x in qa_templates),
            "all_unreviewed": all(x.get("review_status") == "UNREVIEWED" for x in qa_templates),
            "all_not_answers": all_false(qa_templates, ["counts_as_answer", "counts_as_resolution_input"]),
        },
        "source_ref_satisfaction_templates": {
            "count": len(source_templates),
            "all_template_only": all(x.get("proposal_status") == "TEMPLATE_ONLY_NOT_PROPOSED" for x in source_templates),
            "all_unreviewed": all(x.get("review_status") == "UNREVIEWED" for x in source_templates),
            "all_not_satisfied": all_false(source_templates, ["counts_as_satisfied", "counts_as_resolution_input"]),
        },
        "under_typed_acceptance_review_templates": {
            "count": len(undertyped_templates),
            "all_template_only": all(x.get("proposal_status") == "TEMPLATE_ONLY_NOT_PROPOSED" for x in undertyped_templates),
            "all_unreviewed": all(x.get("review_status") == "UNREVIEWED" for x in undertyped_templates),
            "all_not_approved": all_false(undertyped_templates, ["counts_as_approved", "c5_unblock_allowed"]),
        },
        "parking_execution_continuation_templates": {
            "count": len(parking_templates),
            "all_template_only": all(x.get("proposal_status") == "TEMPLATE_ONLY_PARKED_UNRESOLVED" for x in parking_templates),
            "all_unreviewed": all(x.get("review_status") == "UNREVIEWED" for x in parking_templates),
            "all_not_resolution": all_false(parking_templates, ["counts_as_resolution", "c5_unblock_allowed"]),
        },
        "proposed_resolution_record_templates": {
            "count": len(resolution_templates),
            "all_template_only": all(x.get("proposal_status") == "TEMPLATE_ONLY" for x in resolution_templates),
            "all_unreviewed": all(x.get("review_status") == "UNREVIEWED" for x in resolution_templates),
            "all_not_reviewed_resolution": all_false(resolution_templates, ["counts_as_reviewed_resolution", "c5_reconsideration_ready"]),
        },
    }

    route_review = {
        "schema_version": "o2_weak_feedback_resolution_execution_proposal_route_review_v0",
        "review_status": "PROPOSAL_ROUTE_REVIEW_PASS" if review_pass else "PROPOSAL_ROUTE_REVIEW_FAIL",
        "proposal_route_map_records_reviewed": len(proposal_routes),
        "all_unresolved": all(x.get("current_resolution_state") == "UNRESOLVED" for x in proposal_routes),
        "all_proposed_record_emitted_false": all(x.get("proposed_record_emitted") is False for x in proposal_routes),
        "all_reviewed_record_emitted_false": all(x.get("reviewed_record_emitted") is False for x in proposal_routes),
        "all_c5_reconsideration_false": all(x.get("c5_reconsideration_ready") is False for x in proposal_routes),
    }

    gate_review = {
        "schema_version": "o2_weak_feedback_resolution_execution_gate_review_v0",
        "review_status": "EXECUTION_GATE_REVIEW_PASS" if review_pass else "EXECUTION_GATE_REVIEW_FAIL",
        "execution_attempted": False,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
    }

    boundary_review = {
        "schema_version": "o2_resolution_proposal_review_boundary_review_v0",
        "review_status": "PROPOSAL_REVIEW_BOUNDARY_REVIEW_PASS" if review_pass else "PROPOSAL_REVIEW_BOUNDARY_REVIEW_FAIL",
        "template_layer_crossed_into_proposal_layer": False,
        "proposal_layer_crossed_into_review_layer": False,
        "templates_are_not_proposed_records": True,
        "proposed_records_are_not_reviewed_records": True,
    }

    c5_review = {
        "schema_version": "o2_resolution_execution_c5_block_review_v0",
        "review_status": "C5_BLOCK_REVIEW_PASS" if review_pass else "C5_BLOCK_REVIEW_FAIL",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "block_enforced": True,
    }

    zero_record_review = {
        "schema_version": "o2_resolution_execution_zero_record_review_v0",
        "review_status": "ZERO_RECORD_REVIEW_PASS" if review_pass else "ZERO_RECORD_REVIEW_FAIL",
        "proposed_question_answer_records_emitted_count": 0,
        "proposed_source_ref_satisfaction_records_emitted_count": 0,
        "proposed_under_typed_acceptance_review_records_emitted_count": 0,
        "parking_execution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
    }

    closure_candidate = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_closure_candidate_v0",
        "closure_candidate_status": "EXECUTION_TARGET_CLOSE_READY_TEMPLATES_ONLY_UNRESOLVED" if review_pass else "EXECUTION_TARGET_CLOSE_NOT_READY",
        "review_pass": review_pass,
        "closure_meaning": "Close static execution-target surface as reviewed reference while preserving template-only status, zero records, unresolved weak feedback, and C5 block.",
        "closure_does_not_mean": [
            "execution occurred",
            "proposed records emitted",
            "reviewed resolution records emitted",
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

    authority_boundary = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_review_authority_boundary_v0",
        "status": status,
        "may_close_execution_target_as_reviewed_reference_next": review_pass,
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
        "schema_version": "o2_weak_feedback_resolution_execution_target_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "execution_target_review_complete": review_pass,
        "execution_target_review_pass": review_pass,
        "closure_candidate_ready": review_pass,
        "templates_reviewed_as_templates_only": review_pass,
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
        "schema_version": "o2_weak_feedback_resolution_execution_target_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "closure_candidate_ready_count": 1 if review_pass else 0,
        "question_answer_templates_reviewed_count": len(qa_templates),
        "source_ref_satisfaction_templates_reviewed_count": len(source_templates),
        "under_typed_acceptance_review_templates_reviewed_count": len(undertyped_templates),
        "parking_execution_continuation_templates_reviewed_count": len(parking_templates),
        "proposed_resolution_record_templates_reviewed_count": len(resolution_templates),
        "proposal_route_map_records_reviewed_count": len(proposal_routes),
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
        "schema_version": "o2_weak_feedback_resolution_execution_target_review_profile_v0",
        "profile_id": "o2_wf_resolution_execution_target_review_profile_" + sha8(rollup),
        "status": status,
        "execution_target_review_pass": review_pass,
        "closure_candidate_ready": review_pass,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Close the execution-target surface as reviewed reference; do not treat templates as proposed or reviewed records.",
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
        "schema_version": "o2_weak_feedback_resolution_execution_target_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The weak-feedback resolution execution target static surface reviewed clean. All emitted objects are templates or readouts, not proposed records and not reviewed records. Proposal routes remain unresolved, the proposal/review boundary was not crossed, zero records were attested, weak feedback remains unresolved, and C5 remains blocked.",
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_execution_target_build",
                "question": "is static execution-target surface present and review-ready",
                "answer": "yes" if review_pass else "no",
                "taken": "review templates and readouts",
            },
            {
                "step": "verify_templates_only",
                "question": "do templates count as proposed or reviewed records",
                "answer": "no",
                "taken": "preserve zero-record state",
            },
            {
                "step": "verify_c5_block",
                "question": "does reviewed template surface unblock C5",
                "answer": "no",
                "taken": "emit close-ready reviewed reference candidate",
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
        (TEMPLATE_REVIEW_PATH, template_review),
        (PROPOSAL_ROUTE_REVIEW_PATH, route_review),
        (GATE_REVIEW_PATH, gate_review),
        (BOUNDARY_REVIEW_PATH, boundary_review),
        (C5_BLOCK_REVIEW_PATH, c5_review),
        (ZERO_RECORD_REVIEW_PATH, zero_record_review),
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
        "EXEC_TARGET_REVIEW_0_BUILD_RECEIPT_CONSUMED": EXEC_BUILD_RECEIPT_PATH.exists(),
        "EXEC_TARGET_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "EXEC_TARGET_REVIEW_2_TEMPLATE_REVIEW_EMITTED": TEMPLATE_REVIEW_PATH.exists(),
        "EXEC_TARGET_REVIEW_3_PROPOSAL_ROUTE_REVIEW_EMITTED": PROPOSAL_ROUTE_REVIEW_PATH.exists(),
        "EXEC_TARGET_REVIEW_4_TEMPLATES_REVIEWED_AS_TEMPLATES_ONLY": template_review["proposed_resolution_record_templates"]["all_template_only"] is True,
        "EXEC_TARGET_REVIEW_5_ALL_TEMPLATES_UNREVIEWED": template_review["proposed_resolution_record_templates"]["all_unreviewed"] is True,
        "EXEC_TARGET_REVIEW_6_PROPOSAL_ROUTE_UNRESOLVED": route_review["all_unresolved"] is True,
        "EXEC_TARGET_REVIEW_7_NO_PROPOSED_RECORDS_EMITTED": route_review["all_proposed_record_emitted_false"] is True,
        "EXEC_TARGET_REVIEW_8_NO_REVIEWED_RECORDS_EMITTED": route_review["all_reviewed_record_emitted_false"] is True,
        "EXEC_TARGET_REVIEW_9_EXECUTION_GATE_NOT_EXECUTED": gate_review["execution_attempted"] is False,
        "EXEC_TARGET_REVIEW_10_BOUNDARY_NOT_CROSSED": boundary_review["template_layer_crossed_into_proposal_layer"] is False and boundary_review["proposal_layer_crossed_into_review_layer"] is False,
        "EXEC_TARGET_REVIEW_11_C5_BLOCK_ENFORCED": c5_review["c5_opened"] is False and c5_review["c5_reconsideration_ready"] is False,
        "EXEC_TARGET_REVIEW_12_ZERO_RECORDS_REVIEWED": zero_record_review["resolution_records_emitted_count"] == 0 and zero_record_review["proposed_resolution_records_emitted_count"] == 0 and zero_record_review["reviewed_resolution_records_emitted_count"] == 0,
        "EXEC_TARGET_REVIEW_13_NO_RESOLUTION_ANSWER_SATISFY_APPROVE": rollup["weak_feedback_resolved_count"] == 0 and rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "EXEC_TARGET_REVIEW_14_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "EXEC_TARGET_REVIEW_15_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "EXEC_TARGET_REVIEW_16_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "EXEC_TARGET_REVIEW_17_NO_C5_RECONSIDERATION_READY": rollup["c5_reconsideration_ready_count"] == 0,
        "EXEC_TARGET_REVIEW_18_CLOSURE_CANDIDATE_READY": closure_candidate["closure_candidate_status"] == "EXECUTION_TARGET_CLOSE_READY_TEMPLATES_ONLY_UNRESOLVED",
        "EXEC_TARGET_REVIEW_19_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "EXEC_TARGET_REVIEW_20_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "EXEC_TARGET_REVIEW_21_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REVIEW_GATE_FAIL",
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
        "schema_version": "o2_weak_feedback_resolution_execution_target_review_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_execution_target_build_receipt_id": EXEC_BUILD_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_resolution_execution_target_review_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "execution_target_review_complete": review_pass,
            "execution_target_review_pass": review_pass,
            "closure_candidate_ready": review_pass,
            "templates_reviewed_as_templates_only": review_pass,
            "question_answer_templates_reviewed_count": len(qa_templates),
            "source_ref_satisfaction_templates_reviewed_count": len(source_templates),
            "under_typed_acceptance_review_templates_reviewed_count": len(undertyped_templates),
            "parking_execution_continuation_templates_reviewed_count": len(parking_templates),
            "proposed_resolution_record_templates_reviewed_count": len(resolution_templates),
            "proposal_route_map_records_reviewed_count": len(proposal_routes),
            "proposal_routes_unresolved": route_review["all_unresolved"],
            "proposal_routes_proposed_record_emitted_false": route_review["all_proposed_record_emitted_false"],
            "proposal_routes_reviewed_record_emitted_false": route_review["all_reviewed_record_emitted_false"],
            "execution_gate_not_executed": gate_review["execution_attempted"] is False,
            "proposal_review_boundary_not_crossed": boundary_review["template_layer_crossed_into_proposal_layer"] is False and boundary_review["proposal_layer_crossed_into_review_layer"] is False,
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
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "template_review": rel(TEMPLATE_REVIEW_PATH),
            "proposal_route_review": rel(PROPOSAL_ROUTE_REVIEW_PATH),
            "gate_review": rel(GATE_REVIEW_PATH),
            "boundary_review": rel(BOUNDARY_REVIEW_PATH),
            "c5_block_review": rel(C5_BLOCK_REVIEW_PATH),
            "zero_record_review": rel(ZERO_RECORD_REVIEW_PATH),
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
    print(f"weak_feedback_resolution_execution_target_review_receipt_id={receipt_id}")
    print(f"weak_feedback_resolution_execution_target_review_receipt_path={rel(receipt_path)}")
    print(f"weak_feedback_resolution_execution_target_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"weak_feedback_resolution_execution_template_review_path={rel(TEMPLATE_REVIEW_PATH)}")
    print(f"weak_feedback_resolution_execution_proposal_route_review_path={rel(PROPOSAL_ROUTE_REVIEW_PATH)}")
    print(f"weak_feedback_resolution_execution_gate_review_path={rel(GATE_REVIEW_PATH)}")
    print(f"resolution_proposal_review_boundary_review_path={rel(BOUNDARY_REVIEW_PATH)}")
    print(f"resolution_execution_c5_block_review_path={rel(C5_BLOCK_REVIEW_PATH)}")
    print(f"resolution_execution_zero_record_review_path={rel(ZERO_RECORD_REVIEW_PATH)}")
    print(f"execution_target_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"execution_target_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
