#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_execution_target_build.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_BUILD"
MODE = "STATIC_RESOLUTION_EXECUTION_TARGET_BUILD_ONLY / NO_EXECUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_STATIC_BUILD_ONLY"

EXEC_DESIGN_RECEIPT_ID = "0fea0528"
EXEC_DESIGN_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0_receipts/0fea0528.json"
EXEC_TARGET_DEFINITION_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_target_definition_v0.json"
EXEC_INPUT_INVENTORY_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_input_surface_inventory_v0.json"
EXEC_QA_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_proposed_question_answer_execution_contract_v0.json"
EXEC_SOURCE_REF_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_proposed_source_ref_satisfaction_execution_contract_v0.json"
EXEC_UNDERTYPED_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_proposed_under_typed_acceptance_review_execution_contract_v0.json"
EXEC_PARKING_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_parking_execution_continuation_contract_v0.json"
EXEC_PROPOSED_RESOLUTION_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_proposed_weak_feedback_resolution_record_contract_v0.json"
EXEC_GATE_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_gate_contract_v0.json"
EXEC_PROPOSAL_REVIEW_BOUNDARY_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_resolution_proposal_review_boundary_v0.json"
EXEC_C5_BLOCK_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_resolution_execution_c5_block_contract_v0.json"
EXEC_NEGATIVE_CONTROLS_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_negative_controls_v0.json"
EXEC_BUILD_AUTHORIZATION_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_target_build_authorization_v0.json"
EXEC_UNRESOLVED_CONTINUATION_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_target_unresolved_continuation_v0.json"
EXEC_AUTHORITY_BOUNDARY_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_target_authority_boundary_v0.json"
EXEC_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_target_classification_v0.json"
EXEC_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_target_rollup_v0.json"
EXEC_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_target_profile_v0.json"
EXEC_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_target_report.json"
EXEC_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_v0/o2_weak_feedback_resolution_execution_target_transition_trace.json"

RT_DECISION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_post_closure_decision_v0_receipts/1100f482.json"
RT_REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_closure_v0/o2_weak_feedback_resolution_target_reviewed_reference_v0.json"
RT_QUESTION_SKELETONS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_question_packet_answer_record_skeletons_v0.jsonl"
RT_SOURCE_REF_SKELETONS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_source_ref_satisfaction_record_skeletons_v0.jsonl"
RT_UNDERTYPED_SKELETONS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_under_typed_acceptance_review_record_skeletons_v0.jsonl"
RT_PARKING_SKELETONS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_parking_continuation_record_skeletons_v0.jsonl"
RT_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_route_map_v0.jsonl"
RT_GATE_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_weak_feedback_resolution_gate_readout_v0.json"
RT_C5_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_build_v0/o2_c5_reconsideration_readout_v0.json"

REQUIRED_SOURCE_FILES = [
    EXEC_DESIGN_RECEIPT_PATH,
    EXEC_TARGET_DEFINITION_PATH,
    EXEC_INPUT_INVENTORY_PATH,
    EXEC_QA_CONTRACT_PATH,
    EXEC_SOURCE_REF_CONTRACT_PATH,
    EXEC_UNDERTYPED_CONTRACT_PATH,
    EXEC_PARKING_CONTRACT_PATH,
    EXEC_PROPOSED_RESOLUTION_CONTRACT_PATH,
    EXEC_GATE_CONTRACT_PATH,
    EXEC_PROPOSAL_REVIEW_BOUNDARY_PATH,
    EXEC_C5_BLOCK_CONTRACT_PATH,
    EXEC_NEGATIVE_CONTROLS_PATH,
    EXEC_BUILD_AUTHORIZATION_PATH,
    EXEC_UNRESOLVED_CONTINUATION_PATH,
    EXEC_AUTHORITY_BOUNDARY_PATH,
    EXEC_CLASSIFICATION_PATH,
    EXEC_ROLLUP_PATH,
    EXEC_PROFILE_PATH,
    EXEC_REPORT_PATH,
    EXEC_TRACE_PATH,
    RT_DECISION_RECEIPT_PATH,
    RT_REVIEWED_REFERENCE_PATH,
    RT_QUESTION_SKELETONS_PATH,
    RT_SOURCE_REF_SKELETONS_PATH,
    RT_UNDERTYPED_SKELETONS_PATH,
    RT_PARKING_SKELETONS_PATH,
    RT_ROUTE_MAP_PATH,
    RT_GATE_READOUT_PATH,
    RT_C5_READOUT_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0_receipts"

SURFACE_RECORD_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_surface_record_v0.json"
INPUT_MAPPING_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_input_mapping_v0.json"
PROPOSED_QA_TEMPLATES_PATH = OUT_DIR / "o2_proposed_question_answer_record_templates_v0.jsonl"
PROPOSED_SOURCE_REF_TEMPLATES_PATH = OUT_DIR / "o2_proposed_source_ref_satisfaction_record_templates_v0.jsonl"
PROPOSED_UNDERTYPED_TEMPLATES_PATH = OUT_DIR / "o2_proposed_under_typed_acceptance_review_record_templates_v0.jsonl"
PARKING_EXECUTION_TEMPLATES_PATH = OUT_DIR / "o2_parking_execution_continuation_record_templates_v0.jsonl"
PROPOSED_RESOLUTION_TEMPLATES_PATH = OUT_DIR / "o2_proposed_weak_feedback_resolution_record_templates_v0.jsonl"
PROPOSAL_ROUTE_MAP_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_proposal_route_map_v0.jsonl"
EXECUTION_GATE_READOUT_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_gate_readout_v0.json"
PROPOSAL_REVIEW_BOUNDARY_READOUT_PATH = OUT_DIR / "o2_resolution_proposal_review_boundary_readout_v0.json"
C5_BLOCK_ENFORCEMENT_READOUT_PATH = OUT_DIR / "o2_resolution_execution_c5_block_enforcement_readout_v0.json"
ZERO_RECORD_ATTESTATION_PATH = OUT_DIR / "o2_resolution_execution_zero_record_attestation_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_build_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_build_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_build_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_build_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_build_report.json"
TRACE_PATH = OUT_DIR / "o2_weak_feedback_resolution_execution_target_build_transition_trace.json"

EXPECTED_DESIGN_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_NEXT = "BUILD_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_V0"
RECOMMENDED_NEXT = "REVIEW_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_V0"

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

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(EXEC_DESIGN_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_resolution_execution_target_summary", {})
    target_definition = read_json(EXEC_TARGET_DEFINITION_PATH)
    inventory = read_json(EXEC_INPUT_INVENTORY_PATH)
    qa_contract = read_json(EXEC_QA_CONTRACT_PATH)
    source_contract = read_json(EXEC_SOURCE_REF_CONTRACT_PATH)
    undertyped_contract = read_json(EXEC_UNDERTYPED_CONTRACT_PATH)
    parking_contract = read_json(EXEC_PARKING_CONTRACT_PATH)
    proposed_resolution_contract = read_json(EXEC_PROPOSED_RESOLUTION_CONTRACT_PATH)
    gate_contract = read_json(EXEC_GATE_CONTRACT_PATH)
    proposal_boundary = read_json(EXEC_PROPOSAL_REVIEW_BOUNDARY_PATH)
    c5_contract = read_json(EXEC_C5_BLOCK_CONTRACT_PATH)
    build_auth = read_json(EXEC_BUILD_AUTHORIZATION_PATH)
    unresolved = read_json(EXEC_UNRESOLVED_CONTINUATION_PATH)
    authority = read_json(EXEC_AUTHORITY_BOUNDARY_PATH)
    design_rollup = read_json(EXEC_ROLLUP_PATH)
    design_profile = read_json(EXEC_PROFILE_PATH)

    rt_decision_receipt = read_json(RT_DECISION_RECEIPT_PATH)
    reviewed_reference = read_json(RT_REVIEWED_REFERENCE_PATH)
    qa_skeletons = read_jsonl(RT_QUESTION_SKELETONS_PATH)
    source_skeletons = read_jsonl(RT_SOURCE_REF_SKELETONS_PATH)
    undertyped_skeletons = read_jsonl(RT_UNDERTYPED_SKELETONS_PATH)
    parking_skeletons = read_jsonl(RT_PARKING_SKELETONS_PATH)
    route_map = read_jsonl(RT_ROUTE_MAP_PATH)
    gate_readout = read_json(RT_GATE_READOUT_PATH)
    c5_readout = read_json(RT_C5_READOUT_PATH)

    if receipt.get("receipt_id") != EXEC_DESIGN_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("execution_target_design_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_DESIGN_STOP:
        failures.append("execution_target_design_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("execution_target_design_hidden_next_command")
    if summary.get("status") != EXPECTED_DESIGN_STATUS:
        failures.append(f"execution_target_design_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_DESIGN_NEXT:
        failures.append(f"execution_target_design_next_wrong:{summary.get('recommended_next')}")
    if summary.get("authorized_next_unit") != EXPECTED_DESIGN_NEXT:
        failures.append("authorized_next_wrong")
    if summary.get("authorized_build_mode") != "STATIC_RESOLUTION_EXECUTION_TARGET_BUILD_ONLY":
        failures.append("authorized_build_mode_wrong")

    for key in [
        "resolution_execution_target_designed",
        "build_authorized_next",
        "proposed_question_answer_contract_frozen",
        "proposed_source_ref_satisfaction_contract_frozen",
        "proposed_under_typed_acceptance_review_contract_frozen",
        "parking_execution_continuation_contract_frozen",
        "proposed_resolution_record_contract_frozen",
        "execution_gate_contract_frozen",
        "proposal_review_boundary_frozen",
        "c5_block_contract_frozen",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "question_answer_skeletons_available_count": 3,
        "source_ref_satisfaction_skeletons_available_count": 2,
        "under_typed_acceptance_review_skeletons_available_count": 2,
        "parking_continuation_skeletons_available_count": 3,
        "route_map_records_available_count": 3,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
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

    if target_definition.get("target_mode_for_build") != "STATIC_RESOLUTION_EXECUTION_TARGET_BUILD_ONLY":
        failures.append("target_definition_mode_wrong")
    if inventory.get("inventory_status") != "INPUT_SURFACES_AVAILABLE_FOR_EXECUTION_TARGET_BUILD":
        failures.append("inventory_status_wrong")
    if qa_contract.get("design_unit_emits_proposed_answers") is not False:
        failures.append("qa_contract_design_emits_records")
    if source_contract.get("design_unit_emits_proposed_source_refs") is not False:
        failures.append("source_contract_design_emits_records")
    if undertyped_contract.get("design_unit_emits_proposed_under_typed_reviews") is not False:
        failures.append("undertyped_contract_design_emits_records")
    if parking_contract.get("design_unit_counts_parking_as_resolution") is not False:
        failures.append("parking_contract_counts_resolution")
    if proposed_resolution_contract.get("design_unit_emits_proposed_resolution_records") is not False:
        failures.append("resolution_contract_design_emits_records")
    if gate_contract.get("design_unit_executes_gate") is not False:
        failures.append("gate_contract_executes")
    if proposal_boundary.get("design_unit_crosses_boundary") is not False:
        failures.append("proposal_boundary_crossed")
    if c5_contract.get("design_unit_can_unblock_c5") is not False:
        failures.append("c5_contract_unblocks_c5")
    if build_auth.get("authorized_next_unit") != EXPECTED_DESIGN_NEXT:
        failures.append("build_auth_next_wrong")
    if unresolved.get("weak_feedback_resolved") is not False or unresolved.get("proposed_resolution_records_emitted_count") != 0:
        failures.append("unresolved_continuation_wrong")
    if authority.get("may_build_o2_weak_feedback_resolution_execution_target_next") is not True:
        failures.append("authority_no_build_next")
    if authority.get("may_execute_resolution_now") is not False:
        failures.append("authority_allows_execution")
    if design_rollup.get("build_authorized_next_count") != 1:
        failures.append("design_rollup_build_next_wrong")
    if design_profile.get("authorized_next_unit") != EXPECTED_DESIGN_NEXT:
        failures.append("design_profile_next_wrong")

    if rt_decision_receipt.get("receipt_id") != "1100f482":
        failures.append("rt_decision_receipt_wrong")
    if reviewed_reference.get("weak_feedback_resolved") is not False or reviewed_reference.get("resolution_records_emitted_count") != 0:
        failures.append("reviewed_reference_wrong")
    if len(qa_skeletons) != 3 or len(source_skeletons) != 2 or len(undertyped_skeletons) != 2 or len(parking_skeletons) != 3 or len(route_map) != 3:
        failures.append("source_surface_counts_wrong")
    if gate_readout.get("weak_feedback_resolved") is not False or gate_readout.get("resolution_records_emitted_count") != 0:
        failures.append("gate_readout_wrong")
    if c5_readout.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_readout.get("c5_opened") is not False:
        failures.append("c5_readout_wrong")
    for row in route_map:
        if row.get("current_resolution_state") != "UNRESOLVED":
            failures.append(f"route_not_unresolved:{row.get('route_map_record_id')}")
        if row.get("c5_reconsideration_ready") is not False:
            failures.append(f"route_c5_ready:{row.get('route_map_record_id')}")

    return failures, {
        "summary": summary,
        "qa_skeletons": qa_skeletons,
        "source_skeletons": source_skeletons,
        "undertyped_skeletons": undertyped_skeletons,
        "parking_skeletons": parking_skeletons,
        "route_map": route_map,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    qa_skeletons = src.get("qa_skeletons", [])
    source_skeletons = src.get("source_skeletons", [])
    undertyped_skeletons = src.get("undertyped_skeletons", [])
    parking_skeletons = src.get("parking_skeletons", [])
    route_map = src.get("route_map", [])

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    qa_templates = [
        {
            "schema_version": "o2_proposed_question_answer_record_template_v0",
            "template_id": "proposed_question_answer_template_" + sha8(row),
            "source_answer_skeleton_ref": row.get("answer_skeleton_id"),
            "source_question_packet_ref": row.get("source_question_packet_ref"),
            "answer_payload_or_ref": None,
            "evidence_refs": [],
            "proposal_status": "TEMPLATE_ONLY_NOT_PROPOSED",
            "review_status": "UNREVIEWED",
            "counts_as_answer": False,
            "counts_as_resolution_input": False,
        }
        for row in qa_skeletons
    ]

    source_templates = [
        {
            "schema_version": "o2_proposed_source_ref_satisfaction_record_template_v0",
            "template_id": "proposed_source_ref_satisfaction_template_" + sha8(row),
            "source_satisfaction_skeleton_ref": row.get("satisfaction_skeleton_id"),
            "source_ref_request_ref": row.get("source_ref_request_ref"),
            "proposed_source_refs": [],
            "proposal_status": "TEMPLATE_ONLY_NOT_PROPOSED",
            "review_status": "UNREVIEWED",
            "counts_as_satisfied": False,
            "counts_as_resolution_input": False,
        }
        for row in source_skeletons
    ]

    undertyped_templates = [
        {
            "schema_version": "o2_proposed_under_typed_acceptance_review_record_template_v0",
            "template_id": "proposed_under_typed_review_template_" + sha8(row),
            "source_review_skeleton_ref": row.get("review_skeleton_id"),
            "proposed_decision": "KEEP_CANDIDATE_ONLY",
            "proposal_status": "TEMPLATE_ONLY_NOT_PROPOSED",
            "review_status": "UNREVIEWED",
            "counts_as_approved": False,
            "c5_unblock_allowed": False,
        }
        for row in undertyped_skeletons
    ]

    parking_templates = [
        {
            "schema_version": "o2_parking_execution_continuation_record_template_v0",
            "template_id": "parking_execution_continuation_template_" + sha8(row),
            "source_parking_skeleton_ref": row.get("parking_continuation_skeleton_id"),
            "continue_parking": True,
            "proposal_status": "TEMPLATE_ONLY_PARKED_UNRESOLVED",
            "review_status": "UNREVIEWED",
            "counts_as_resolution": False,
            "c5_unblock_allowed": False,
        }
        for row in parking_skeletons
    ]

    qa_by_feedback: Dict[str, List[str]] = {}
    for row in qa_templates:
        skel = next((x for x in qa_skeletons if x.get("answer_skeleton_id") == row.get("source_answer_skeleton_ref")), {})
        qa_by_feedback.setdefault(skel.get("source_feedback_ref"), []).append(row["template_id"])

    source_by_feedback: Dict[str, List[str]] = {}
    for row in source_templates:
        skel = next((x for x in source_skeletons if x.get("satisfaction_skeleton_id") == row.get("source_satisfaction_skeleton_ref")), {})
        source_by_feedback.setdefault(skel.get("source_feedback_ref"), []).append(row["template_id"])

    undertyped_by_feedback: Dict[str, List[str]] = {}
    for row in undertyped_templates:
        skel = next((x for x in undertyped_skeletons if x.get("review_skeleton_id") == row.get("source_review_skeleton_ref")), {})
        undertyped_by_feedback.setdefault(skel.get("source_feedback_ref"), []).append(row["template_id"])

    parking_by_feedback: Dict[str, List[str]] = {}
    for row in parking_templates:
        skel = next((x for x in parking_skeletons if x.get("parking_continuation_skeleton_id") == row.get("source_parking_skeleton_ref")), {})
        parking_by_feedback.setdefault(skel.get("source_feedback_ref"), []).append(row["template_id"])

    resolution_templates = []
    proposal_route_map = []
    for route in route_map:
        feedback_ref = route.get("source_feedback_ref")
        resolution_template = {
            "schema_version": "o2_proposed_weak_feedback_resolution_record_template_v0",
            "template_id": "proposed_weak_feedback_resolution_template_" + sha8(route),
            "source_route_map_ref": route.get("route_map_record_id"),
            "proposed_question_answer_template_refs": qa_by_feedback.get(feedback_ref, []),
            "proposed_source_ref_satisfaction_template_refs": source_by_feedback.get(feedback_ref, []),
            "proposed_under_typed_review_template_refs": undertyped_by_feedback.get(feedback_ref, []),
            "parking_continuation_template_refs": parking_by_feedback.get(feedback_ref, []),
            "proposed_resolution_decision": "TEMPLATE_ONLY_NOT_PROPOSED",
            "proposal_status": "TEMPLATE_ONLY",
            "review_status": "UNREVIEWED",
            "counts_as_reviewed_resolution": False,
            "c5_reconsideration_ready": False,
        }
        resolution_templates.append(resolution_template)
        proposal_route_map.append({
            "schema_version": "o2_weak_feedback_resolution_execution_proposal_route_map_record_v0",
            "proposal_route_record_id": "proposal_route_" + sha8(route),
            "source_feedback_ref": feedback_ref,
            "source_route_map_ref": route.get("route_map_record_id"),
            "current_resolution_state": "UNRESOLVED",
            "proposal_template_ref": resolution_template["template_id"],
            "proposed_record_emitted": False,
            "reviewed_record_emitted": False,
            "c5_reconsideration_ready": False,
        })

    build_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_STATIC_SURFACE_EMITTED_REVIEW_READY" if build_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_BUILD_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if build_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_BUILD_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_STATIC_SURFACE_EMITTED",
        "EXECUTION_TARGET_DESIGN_RECEIPT_CONSUMED",
        "EXECUTION_INPUT_MAPPING_EMITTED",
        "PROPOSED_QUESTION_ANSWER_TEMPLATES_EMITTED_NOT_RECORDS",
        "PROPOSED_SOURCE_REF_SATISFACTION_TEMPLATES_EMITTED_NOT_RECORDS",
        "PROPOSED_UNDER_TYPED_ACCEPTANCE_REVIEW_TEMPLATES_EMITTED_NOT_RECORDS",
        "PARKING_EXECUTION_CONTINUATION_TEMPLATES_EMITTED_NOT_RESOLUTION",
        "PROPOSED_RESOLUTION_RECORD_TEMPLATES_EMITTED_NOT_RECORDS",
        "PROPOSAL_ROUTE_MAP_EMITTED_UNRESOLVED",
        "EXECUTION_GATE_READOUT_EMITTED_NOT_EXECUTED",
        "PROPOSAL_REVIEW_BOUNDARY_READOUT_EMITTED",
        "C5_BLOCK_ENFORCEMENT_READOUT_EMITTED",
        "ZERO_RECORD_ATTESTATION_EMITTED",
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
    ] if build_pass else failures

    surface_record = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_surface_record_v0",
        "surface_status": "STATIC_EXECUTION_TARGET_SURFACE_EMITTED" if build_pass else "SURFACE_NOT_EMITTED",
        "source_execution_target_design_receipt_id": EXEC_DESIGN_RECEIPT_ID,
        "surface_meaning": "Execution target templates and gate readouts exist for later review. They are not proposed records and not reviewed resolution records.",
        "surface_does_not_mean": [
            "resolution execution occurred",
            "proposed resolution records emitted",
            "reviewed resolution records emitted",
            "weak feedback resolved",
            "C5 reconsideration ready",
            "C5 opened",
        ],
    }

    input_mapping = {
        "schema_version": "o2_weak_feedback_resolution_execution_input_mapping_v0",
        "mapping_status": "EXECUTION_INPUTS_MAPPED_TO_TEMPLATES",
        "question_answer_templates_count": len(qa_templates),
        "source_ref_satisfaction_templates_count": len(source_templates),
        "under_typed_acceptance_review_templates_count": len(undertyped_templates),
        "parking_execution_continuation_templates_count": len(parking_templates),
        "proposed_resolution_record_templates_count": len(resolution_templates),
        "proposal_route_map_records_count": len(proposal_route_map),
    }

    execution_gate_readout = {
        "schema_version": "o2_weak_feedback_resolution_execution_gate_readout_v0",
        "gate_status": "NOT_EXECUTED_REVIEW_REQUIRED",
        "execution_target_surface_built": build_pass,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "all_templates_only": True,
        "execution_requires_later_authorized_unit": True,
    }

    proposal_review_boundary_readout = {
        "schema_version": "o2_resolution_proposal_review_boundary_readout_v0",
        "boundary_status": "BOUNDARY_PRESERVED",
        "templates_emitted": build_pass,
        "proposed_records_emitted_count": 0,
        "reviewed_records_emitted_count": 0,
        "template_layer_crossed_into_proposal_layer": False,
        "proposal_layer_crossed_into_review_layer": False,
    }

    c5_block_enforcement = {
        "schema_version": "o2_resolution_execution_c5_block_enforcement_readout_v0",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "block_enforced": True,
        "reason": "Execution target build emitted templates only; no reviewed resolution exists.",
    }

    zero_record_attestation = {
        "schema_version": "o2_resolution_execution_zero_record_attestation_v0",
        "attestation_status": "ZERO_RECORDS_ATTESTED",
        "proposed_question_answer_records_emitted_count": 0,
        "proposed_source_ref_satisfaction_records_emitted_count": 0,
        "proposed_under_typed_acceptance_review_records_emitted_count": 0,
        "parking_execution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    write_json(SURFACE_RECORD_PATH, surface_record)
    write_json(INPUT_MAPPING_PATH, input_mapping)
    write_jsonl(PROPOSED_QA_TEMPLATES_PATH, qa_templates)
    write_jsonl(PROPOSED_SOURCE_REF_TEMPLATES_PATH, source_templates)
    write_jsonl(PROPOSED_UNDERTYPED_TEMPLATES_PATH, undertyped_templates)
    write_jsonl(PARKING_EXECUTION_TEMPLATES_PATH, parking_templates)
    write_jsonl(PROPOSED_RESOLUTION_TEMPLATES_PATH, resolution_templates)
    write_jsonl(PROPOSAL_ROUTE_MAP_PATH, proposal_route_map)
    write_json(EXECUTION_GATE_READOUT_PATH, execution_gate_readout)
    write_json(PROPOSAL_REVIEW_BOUNDARY_READOUT_PATH, proposal_review_boundary_readout)
    write_json(C5_BLOCK_ENFORCEMENT_READOUT_PATH, c5_block_enforcement)
    write_json(ZERO_RECORD_ATTESTATION_PATH, zero_record_attestation)

    if len(qa_templates) != 3:
        failures.append(f"qa_template_count_wrong:{len(qa_templates)}")
    if len(source_templates) != 2:
        failures.append(f"source_template_count_wrong:{len(source_templates)}")
    if len(undertyped_templates) != 2:
        failures.append(f"undertyped_template_count_wrong:{len(undertyped_templates)}")
    if len(parking_templates) != 3:
        failures.append(f"parking_template_count_wrong:{len(parking_templates)}")
    if len(resolution_templates) != 3:
        failures.append(f"resolution_template_count_wrong:{len(resolution_templates)}")
    if len(proposal_route_map) != 3:
        failures.append(f"proposal_route_count_wrong:{len(proposal_route_map)}")

    for row in qa_templates + source_templates + undertyped_templates + parking_templates + resolution_templates:
        if row.get("review_status") != "UNREVIEWED":
            failures.append(f"template_review_status_wrong:{row.get('template_id')}")
    for row in resolution_templates:
        if row.get("counts_as_reviewed_resolution") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"resolution_template_counts_or_c5:{row.get('template_id')}")
    for row in proposal_route_map:
        if row.get("current_resolution_state") != "UNRESOLVED" or row.get("proposed_record_emitted") is not False or row.get("reviewed_record_emitted") is not False:
            failures.append(f"proposal_route_wrong:{row.get('proposal_route_record_id')}")

    build_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_STATIC_SURFACE_EMITTED_REVIEW_READY" if build_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_BUILD_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if build_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_BUILD_V0"

    authority_boundary = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_build_authority_boundary_v0",
        "status": status,
        "may_review_o2_weak_feedback_resolution_execution_target_next": build_pass,
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
        "schema_version": "o2_weak_feedback_resolution_execution_target_build_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes if build_pass else failures,
        "execution_target_surface_built": build_pass,
        "templates_emitted": build_pass,
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
        "schema_version": "o2_weak_feedback_resolution_execution_target_build_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "execution_target_surface_build_count": 1 if build_pass else 0,
        "input_mapping_count": 1 if build_pass else 0,
        "question_answer_templates_count": len(qa_templates),
        "source_ref_satisfaction_templates_count": len(source_templates),
        "under_typed_acceptance_review_templates_count": len(undertyped_templates),
        "parking_execution_continuation_templates_count": len(parking_templates),
        "proposed_resolution_record_templates_count": len(resolution_templates),
        "proposal_route_map_records_count": len(proposal_route_map),
        "execution_gate_readout_count": 1 if build_pass else 0,
        "proposal_review_boundary_readout_count": 1 if build_pass else 0,
        "c5_block_enforcement_readout_count": 1 if build_pass else 0,
        "zero_record_attestation_count": 1 if build_pass else 0,
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
        "schema_version": "o2_weak_feedback_resolution_execution_target_build_profile_v0",
        "profile_id": "o2_wf_resolution_execution_target_build_profile_" + sha8(rollup),
        "status": status,
        "execution_target_surface_built": build_pass,
        "templates_emitted": build_pass,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Review the weak-feedback resolution execution target surface next; templates are not proposed or reviewed records.",
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
        "schema_version": "o2_weak_feedback_resolution_execution_target_build_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes if build_pass else failures,
        "receipt_backed_claim": "The weak-feedback resolution execution target static surface was built. It materialized proposed-record templates, proposal route maps, execution gate readout, proposal/review boundary readout, C5-block enforcement readout, and zero-record attestation. It emitted no proposed records and no reviewed resolution records; weak feedback remains unresolved and C5 remains blocked.",
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_build_transition_trace_v0",
        "trace": [
            {
                "step": "consume_execution_target_design",
                "question": "is static execution target build authorized",
                "answer": "yes" if build_pass else "no",
                "taken": "materialize templates and gate readouts",
            },
            {
                "step": "materialize_template_surface",
                "question": "do templates count as proposed or reviewed records",
                "answer": "no",
                "taken": "emit zero-record attestation",
            },
            {
                "step": "preserve_c5_block",
                "question": "does execution target build unblock C5",
                "answer": "no",
                "taken": "review required next",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(AUTHORITY_BOUNDARY_PATH, authority_boundary)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRACE_PATH, trace)

    acceptance_gate_results = {
        "EXEC_TARGET_BUILD_0_DESIGN_RECEIPT_CONSUMED": EXEC_DESIGN_RECEIPT_PATH.exists(),
        "EXEC_TARGET_BUILD_1_SURFACE_RECORD_EMITTED": SURFACE_RECORD_PATH.exists(),
        "EXEC_TARGET_BUILD_2_INPUT_MAPPING_EMITTED": INPUT_MAPPING_PATH.exists(),
        "EXEC_TARGET_BUILD_3_PROPOSED_QA_TEMPLATES_EMITTED": len(qa_templates) == 3,
        "EXEC_TARGET_BUILD_4_PROPOSED_SOURCE_REF_TEMPLATES_EMITTED": len(source_templates) == 2,
        "EXEC_TARGET_BUILD_5_PROPOSED_UNDERTYPED_TEMPLATES_EMITTED": len(undertyped_templates) == 2,
        "EXEC_TARGET_BUILD_6_PARKING_EXECUTION_TEMPLATES_EMITTED": len(parking_templates) == 3,
        "EXEC_TARGET_BUILD_7_PROPOSED_RESOLUTION_TEMPLATES_EMITTED": len(resolution_templates) == 3,
        "EXEC_TARGET_BUILD_8_PROPOSAL_ROUTE_MAP_EMITTED": len(proposal_route_map) == 3,
        "EXEC_TARGET_BUILD_9_EXECUTION_GATE_READOUT_EMITTED_NOT_EXECUTED": EXECUTION_GATE_READOUT_PATH.exists() and execution_gate_readout["proposed_resolution_records_emitted_count"] == 0,
        "EXEC_TARGET_BUILD_10_PROPOSAL_REVIEW_BOUNDARY_READOUT_EMITTED": PROPOSAL_REVIEW_BOUNDARY_READOUT_PATH.exists(),
        "EXEC_TARGET_BUILD_11_C5_BLOCK_ENFORCEMENT_READOUT_EMITTED": C5_BLOCK_ENFORCEMENT_READOUT_PATH.exists() and c5_block_enforcement["c5_opened"] is False,
        "EXEC_TARGET_BUILD_12_ZERO_RECORD_ATTESTATION_EMITTED": ZERO_RECORD_ATTESTATION_PATH.exists() and zero_record_attestation["resolution_records_emitted_count"] == 0,
        "EXEC_TARGET_BUILD_13_NO_RESOLUTION_RECORDS_EMITTED": rollup["resolution_records_emitted_count"] == 0 and rollup["proposed_resolution_records_emitted_count"] == 0 and rollup["reviewed_resolution_records_emitted_count"] == 0,
        "EXEC_TARGET_BUILD_14_NO_RESOLUTION_ANSWER_SATISFY_APPROVE": rollup["weak_feedback_resolved_count"] == 0 and rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "EXEC_TARGET_BUILD_15_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "EXEC_TARGET_BUILD_16_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "EXEC_TARGET_BUILD_17_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "EXEC_TARGET_BUILD_18_NO_C5_RECONSIDERATION_READY": rollup["c5_reconsideration_ready_count"] == 0,
        "EXEC_TARGET_BUILD_19_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "EXEC_TARGET_BUILD_20_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "EXEC_TARGET_BUILD_21_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_BUILD_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "templates": {
            "qa": len(qa_templates),
            "source": len(source_templates),
            "undertyped": len(undertyped_templates),
            "parking": len(parking_templates),
            "resolution": len(resolution_templates),
        },
        "records": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_resolution_execution_target_build_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_EXECUTION_TARGET_BUILD_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_execution_target_design_receipt_id": EXEC_DESIGN_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_resolution_execution_target_build_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "execution_target_surface_built": build_pass,
            "templates_emitted": build_pass,
            "question_answer_templates_count": len(qa_templates),
            "source_ref_satisfaction_templates_count": len(source_templates),
            "under_typed_acceptance_review_templates_count": len(undertyped_templates),
            "parking_execution_continuation_templates_count": len(parking_templates),
            "proposed_resolution_record_templates_count": len(resolution_templates),
            "proposal_route_map_records_count": len(proposal_route_map),
            "execution_gate_readout_emitted": build_pass,
            "proposal_review_boundary_readout_emitted": build_pass,
            "c5_block_enforcement_readout_emitted": build_pass,
            "zero_record_attestation_emitted": build_pass,
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
            "surface_record": rel(SURFACE_RECORD_PATH),
            "input_mapping": rel(INPUT_MAPPING_PATH),
            "proposed_question_answer_templates": rel(PROPOSED_QA_TEMPLATES_PATH),
            "proposed_source_ref_satisfaction_templates": rel(PROPOSED_SOURCE_REF_TEMPLATES_PATH),
            "proposed_under_typed_acceptance_review_templates": rel(PROPOSED_UNDERTYPED_TEMPLATES_PATH),
            "parking_execution_continuation_templates": rel(PARKING_EXECUTION_TEMPLATES_PATH),
            "proposed_resolution_record_templates": rel(PROPOSED_RESOLUTION_TEMPLATES_PATH),
            "proposal_route_map": rel(PROPOSAL_ROUTE_MAP_PATH),
            "execution_gate_readout": rel(EXECUTION_GATE_READOUT_PATH),
            "proposal_review_boundary_readout": rel(PROPOSAL_REVIEW_BOUNDARY_READOUT_PATH),
            "c5_block_enforcement_readout": rel(C5_BLOCK_ENFORCEMENT_READOUT_PATH),
            "zero_record_attestation": rel(ZERO_RECORD_ATTESTATION_PATH),
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
    print(f"weak_feedback_resolution_execution_target_build_receipt_id={receipt_id}")
    print(f"weak_feedback_resolution_execution_target_build_receipt_path={rel(receipt_path)}")
    print(f"weak_feedback_resolution_execution_target_surface_record_path={rel(SURFACE_RECORD_PATH)}")
    print(f"weak_feedback_resolution_execution_input_mapping_path={rel(INPUT_MAPPING_PATH)}")
    print(f"proposed_question_answer_templates_path={rel(PROPOSED_QA_TEMPLATES_PATH)}")
    print(f"proposed_source_ref_satisfaction_templates_path={rel(PROPOSED_SOURCE_REF_TEMPLATES_PATH)}")
    print(f"proposed_under_typed_acceptance_review_templates_path={rel(PROPOSED_UNDERTYPED_TEMPLATES_PATH)}")
    print(f"parking_execution_continuation_templates_path={rel(PARKING_EXECUTION_TEMPLATES_PATH)}")
    print(f"proposed_resolution_record_templates_path={rel(PROPOSED_RESOLUTION_TEMPLATES_PATH)}")
    print(f"proposal_route_map_path={rel(PROPOSAL_ROUTE_MAP_PATH)}")
    print(f"execution_gate_readout_path={rel(EXECUTION_GATE_READOUT_PATH)}")
    print(f"execution_target_build_rollup_path={rel(ROLLUP_PATH)}")
    print(f"execution_target_build_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
