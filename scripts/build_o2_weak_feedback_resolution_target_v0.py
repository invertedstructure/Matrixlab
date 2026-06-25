#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_target_build.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_TARGET_BUILD"
MODE = "STATIC_RESOLUTION_TARGET_BUILD_ONLY / NO_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_TARGET_STATIC_BUILD_ONLY"

RT_DESIGN_RECEIPT_ID = "e9765563"
RT_DESIGN_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0_receipts/e9765563.json"
RT_TARGET_DEFINITION_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_target_definition_v0.json"
RT_INPUT_SURFACE_INVENTORY_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_input_surface_inventory_v0.json"
RT_RESOLUTION_STATE_ENUM_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_state_enum_v0.json"
RT_QUESTION_ANSWER_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_question_packet_answer_contract_v0.json"
RT_SOURCE_REF_SATISFACTION_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_source_ref_satisfaction_contract_v0.json"
RT_UNDERTYPED_REVIEW_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_under_typed_acceptance_review_contract_v0.json"
RT_PARKING_CONTINUATION_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_parking_continuation_contract_v0.json"
RT_RESOLUTION_GATE_CONTRACT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_gate_contract_v0.json"
RT_C5_RECONSIDERATION_RULE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_c5_reconsideration_rule_v0.json"
RT_NEGATIVE_CONTROLS_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_negative_controls_v0.json"
RT_ACCEPTANCE_GATES_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_target_acceptance_gates_v0.json"
RT_TERMINAL_RULES_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_target_terminal_rules_v0.json"
RT_BUILD_AUTHORIZATION_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_target_build_authorization_v0.json"
RT_C5_BLOCK_CONTINUATION_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_target_c5_block_continuation_v0.json"
RT_AUTHORITY_BOUNDARY_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_target_authority_boundary_v0.json"
RT_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_target_classification_v0.json"
RT_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_target_rollup_v0.json"
RT_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_target_profile_v0.json"
RT_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_target_v0/o2_weak_feedback_resolution_target_report.json"

WFH_POST_DECISION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0_receipts/694e859c.json"
WFH_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0_receipts/07cfbdec.json"
WFH_REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_handling_reviewed_reference_v0.json"
WFH_UNRESOLVED_FREEZE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_unresolved_status_freeze_v0.json"
WFH_C5_BLOCK_FREEZE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_c5_block_freeze_v0.json"

WFH_HANDLING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_records_v0.jsonl"
WFH_QUESTION_PACKETS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_question_packets_v0.jsonl"
WFH_SOURCE_REF_REQUESTS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_source_ref_requests_v0.jsonl"
WFH_UNDERTYPED_CANDIDATES_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_under_typed_acceptance_candidates_v0.jsonl"
WFH_PARKING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_parking_records_v0.jsonl"
WFH_C5_BLOCK_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_c5_block_records_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    RT_DESIGN_RECEIPT_PATH,
    RT_TARGET_DEFINITION_PATH,
    RT_INPUT_SURFACE_INVENTORY_PATH,
    RT_RESOLUTION_STATE_ENUM_PATH,
    RT_QUESTION_ANSWER_CONTRACT_PATH,
    RT_SOURCE_REF_SATISFACTION_CONTRACT_PATH,
    RT_UNDERTYPED_REVIEW_CONTRACT_PATH,
    RT_PARKING_CONTINUATION_CONTRACT_PATH,
    RT_RESOLUTION_GATE_CONTRACT_PATH,
    RT_C5_RECONSIDERATION_RULE_PATH,
    RT_NEGATIVE_CONTROLS_PATH,
    RT_ACCEPTANCE_GATES_PATH,
    RT_TERMINAL_RULES_PATH,
    RT_BUILD_AUTHORIZATION_PATH,
    RT_C5_BLOCK_CONTINUATION_PATH,
    RT_AUTHORITY_BOUNDARY_PATH,
    RT_CLASSIFICATION_PATH,
    RT_ROLLUP_PATH,
    RT_PROFILE_PATH,
    RT_REPORT_PATH,
    WFH_POST_DECISION_RECEIPT_PATH,
    WFH_CLOSURE_RECEIPT_PATH,
    WFH_REVIEWED_REFERENCE_PATH,
    WFH_UNRESOLVED_FREEZE_PATH,
    WFH_C5_BLOCK_FREEZE_PATH,
    WFH_HANDLING_RECORDS_PATH,
    WFH_QUESTION_PACKETS_PATH,
    WFH_SOURCE_REF_REQUESTS_PATH,
    WFH_UNDERTYPED_CANDIDATES_PATH,
    WFH_PARKING_RECORDS_PATH,
    WFH_C5_BLOCK_RECORDS_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_target_build_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_target_build_v0_receipts"

SURFACE_RECORD_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_surface_record_v0.json"
INPUT_MAPPING_PATH = OUT_DIR / "o2_weak_feedback_resolution_input_mapping_v0.json"
QUESTION_ANSWER_SKELETONS_PATH = OUT_DIR / "o2_question_packet_answer_record_skeletons_v0.jsonl"
SOURCE_REF_SATISFACTION_SKELETONS_PATH = OUT_DIR / "o2_source_ref_satisfaction_record_skeletons_v0.jsonl"
UNDERTYPED_REVIEW_SKELETONS_PATH = OUT_DIR / "o2_under_typed_acceptance_review_record_skeletons_v0.jsonl"
PARKING_CONTINUATION_SKELETONS_PATH = OUT_DIR / "o2_parking_continuation_record_skeletons_v0.jsonl"
WEAK_FEEDBACK_ROUTE_MAP_PATH = OUT_DIR / "o2_weak_feedback_resolution_route_map_v0.jsonl"
RESOLUTION_GATE_READOUT_PATH = OUT_DIR / "o2_weak_feedback_resolution_gate_readout_v0.json"
C5_RECONSIDERATION_READOUT_PATH = OUT_DIR / "o2_c5_reconsideration_readout_v0.json"
NONRESOLUTION_ATTESTATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_nonresolution_attestation_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_build_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_build_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_build_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_build_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_build_report.json"
TRACE_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_build_transition_trace.json"

EXPECTED_DESIGN_STATUS = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_STOP = "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_NEXT = "BUILD_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_V0"

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

    receipt = read_json(RT_DESIGN_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_weak_feedback_resolution_target_summary", {})
    target_definition = read_json(RT_TARGET_DEFINITION_PATH)
    input_inventory = read_json(RT_INPUT_SURFACE_INVENTORY_PATH)
    state_enum = read_json(RT_RESOLUTION_STATE_ENUM_PATH)
    question_contract = read_json(RT_QUESTION_ANSWER_CONTRACT_PATH)
    source_ref_contract = read_json(RT_SOURCE_REF_SATISFACTION_CONTRACT_PATH)
    undertyped_contract = read_json(RT_UNDERTYPED_REVIEW_CONTRACT_PATH)
    parking_contract = read_json(RT_PARKING_CONTINUATION_CONTRACT_PATH)
    resolution_gate_contract = read_json(RT_RESOLUTION_GATE_CONTRACT_PATH)
    c5_rule = read_json(RT_C5_RECONSIDERATION_RULE_PATH)
    build_auth = read_json(RT_BUILD_AUTHORIZATION_PATH)
    authority = read_json(RT_AUTHORITY_BOUNDARY_PATH)
    rollup = read_json(RT_ROLLUP_PATH)
    profile = read_json(RT_PROFILE_PATH)

    post_decision = read_json(WFH_POST_DECISION_RECEIPT_PATH)
    closure_receipt = read_json(WFH_CLOSURE_RECEIPT_PATH)
    reviewed_reference = read_json(WFH_REVIEWED_REFERENCE_PATH)
    unresolved_freeze = read_json(WFH_UNRESOLVED_FREEZE_PATH)
    c5_freeze = read_json(WFH_C5_BLOCK_FREEZE_PATH)

    handling = read_jsonl(WFH_HANDLING_RECORDS_PATH)
    questions = read_jsonl(WFH_QUESTION_PACKETS_PATH)
    source_refs = read_jsonl(WFH_SOURCE_REF_REQUESTS_PATH)
    acceptances = read_jsonl(WFH_UNDERTYPED_CANDIDATES_PATH)
    parking = read_jsonl(WFH_PARKING_RECORDS_PATH)
    c5_blocks = read_jsonl(WFH_C5_BLOCK_RECORDS_PATH)

    if receipt.get("receipt_id") != RT_DESIGN_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("resolution_target_design_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_DESIGN_STOP:
        failures.append("resolution_target_design_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("resolution_target_design_hidden_next_command")
    if summary.get("status") != EXPECTED_DESIGN_STATUS:
        failures.append(f"resolution_target_design_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_DESIGN_NEXT:
        failures.append(f"resolution_target_design_next_wrong:{summary.get('recommended_next')}")
    if summary.get("authorized_next_unit") != EXPECTED_DESIGN_NEXT:
        failures.append("authorized_next_wrong")
    if summary.get("authorized_build_mode") != "STATIC_RESOLUTION_TARGET_BUILD_ONLY":
        failures.append("authorized_build_mode_wrong")

    for key in [
        "resolution_target_designed",
        "input_surface_inventory_emitted",
        "resolution_state_enum_frozen",
        "question_answer_contract_frozen",
        "source_ref_satisfaction_contract_frozen",
        "under_typed_acceptance_review_contract_frozen",
        "parking_continuation_contract_frozen",
        "resolution_gate_contract_frozen",
        "c5_reconsideration_rule_frozen",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    for key in [
        "weak_feedback_resolved",
        "question_packets_answered",
        "source_ref_requests_satisfied",
        "under_typed_acceptance_approved",
        "parking_counted_as_resolution",
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
        "handling_records_available_count": 3,
        "question_packet_candidates_available_count": 3,
        "source_ref_request_candidates_available_count": 2,
        "under_typed_acceptance_candidates_available_count": 2,
        "parking_records_available_count": 3,
        "c5_block_records_available_count": 3,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    if summary.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("summary_c5_not_blocked")
    if target_definition.get("target_mode_for_build") != "STATIC_RESOLUTION_TARGET_BUILD_ONLY":
        failures.append("target_definition_mode_wrong")
    if input_inventory.get("inventory_status") != "INPUT_SURFACES_AVAILABLE_FOR_TARGET_BUILD":
        failures.append("input_inventory_status_wrong")
    if state_enum.get("design_unit_sets_resolution_state") is not False:
        failures.append("state_enum_claims_design_sets_resolution")
    if question_contract.get("design_unit_answers_questions") is not False:
        failures.append("question_contract_answers")
    if source_ref_contract.get("design_unit_satisfies_source_refs") is not False:
        failures.append("source_ref_contract_satisfies")
    if undertyped_contract.get("design_unit_approves_under_typed_acceptance") is not False:
        failures.append("undertyped_contract_approves")
    if parking_contract.get("design_unit_counts_parking_as_resolution") is not False:
        failures.append("parking_contract_counts_resolution")
    if resolution_gate_contract.get("design_unit_emits_resolution_records") is not False:
        failures.append("resolution_gate_emits_resolution_records")
    if c5_rule.get("design_unit_can_unblock_c5") is not False:
        failures.append("c5_rule_unblocks_c5")
    if build_auth.get("authorized_next_unit") != EXPECTED_DESIGN_NEXT:
        failures.append("build_auth_next_wrong")
    if authority.get("may_build_o2_weak_feedback_resolution_target_next") is not True:
        failures.append("authority_no_build")
    if authority.get("may_open_c5") is not False:
        failures.append("authority_allows_c5")
    if rollup.get("build_authorized_next_count") != 1:
        failures.append("rollup_build_next_wrong")
    if profile.get("authorized_next_unit") != EXPECTED_DESIGN_NEXT:
        failures.append("profile_next_wrong")

    if post_decision.get("receipt_id") != "694e859c":
        failures.append("post_decision_receipt_wrong")
    if closure_receipt.get("receipt_id") != "07cfbdec":
        failures.append("closure_receipt_wrong")
    if reviewed_reference.get("weak_feedback_resolved") is not False:
        failures.append("reviewed_reference_resolved")
    if unresolved_freeze.get("weak_feedback_resolved") is not False:
        failures.append("unresolved_freeze_resolved")
    if c5_freeze.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_freeze.get("c5_opened") is not False:
        failures.append("c5_freeze_wrong")

    if len(handling) != 3 or len(questions) != 3 or len(source_refs) != 2 or len(acceptances) != 2 or len(parking) != 3 or len(c5_blocks) != 3:
        failures.append("source_artifact_counts_wrong")

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

    question_skeletons: List[Dict[str, Any]] = []
    for q in questions:
        question_skeletons.append({
            "schema_version": "o2_question_packet_answer_record_skeleton_v0",
            "answer_skeleton_id": "answer_skeleton_" + sha8(q),
            "source_question_packet_ref": q.get("question_packet_id"),
            "source_feedback_ref": q.get("source_feedback_ref"),
            "answer_text_or_ref": None,
            "answer_evidence_refs": [],
            "review_status": "NOT_ANSWERED",
            "counts_as_resolution_input": False,
            "c5_unblock_allowed": False,
        })

    source_ref_skeletons: List[Dict[str, Any]] = []
    for req in source_refs:
        source_ref_skeletons.append({
            "schema_version": "o2_source_ref_satisfaction_record_skeleton_v0",
            "satisfaction_skeleton_id": "source_ref_satisfaction_skeleton_" + sha8(req),
            "source_ref_request_ref": req.get("source_ref_request_id"),
            "source_feedback_ref": req.get("source_feedback_ref"),
            "provided_source_refs": [],
            "evidence_scope": None,
            "review_status": "UNSATISFIED",
            "counts_as_resolution_input": False,
            "c5_unblock_allowed": False,
        })

    undertyped_skeletons: List[Dict[str, Any]] = []
    for cand in acceptances:
        undertyped_skeletons.append({
            "schema_version": "o2_under_typed_acceptance_review_record_skeleton_v0",
            "review_skeleton_id": "under_typed_review_skeleton_" + sha8(cand),
            "source_acceptance_candidate_ref": cand.get("acceptance_candidate_id"),
            "source_feedback_ref": cand.get("source_feedback_ref"),
            "review_decision": "UNREVIEWED",
            "review_reason": None,
            "review_status": "UNREVIEWED",
            "c5_unblock_allowed": False,
            "counts_as_resolution_input": False,
        })

    parking_skeletons: List[Dict[str, Any]] = []
    for parked in parking:
        parking_skeletons.append({
            "schema_version": "o2_parking_continuation_record_skeleton_v0",
            "parking_continuation_skeleton_id": "parking_continuation_skeleton_" + sha8(parked),
            "source_parking_ref": parked.get("parking_id"),
            "source_feedback_ref": parked.get("source_feedback_ref"),
            "continue_parking": True,
            "counts_as_resolution": False,
            "review_status": "PARKED_UNRESOLVED",
            "c5_unblock_allowed": False,
        })

    q_by_feedback = {}
    for row in question_skeletons:
        q_by_feedback.setdefault(row.get("source_feedback_ref"), []).append(row.get("answer_skeleton_id"))
    src_by_feedback = {}
    for row in source_ref_skeletons:
        src_by_feedback.setdefault(row.get("source_feedback_ref"), []).append(row.get("satisfaction_skeleton_id"))
    acc_by_feedback = {}
    for row in undertyped_skeletons:
        acc_by_feedback.setdefault(row.get("source_feedback_ref"), []).append(row.get("review_skeleton_id"))
    park_by_feedback = {}
    for row in parking_skeletons:
        park_by_feedback.setdefault(row.get("source_feedback_ref"), []).append(row.get("parking_continuation_skeleton_id"))

    route_map: List[Dict[str, Any]] = []
    for record in handling:
        feedback_ref = record.get("source_feedback_ref")
        route_map.append({
            "schema_version": "o2_weak_feedback_resolution_route_map_record_v0",
            "route_map_record_id": "weak_feedback_route_" + sha8(record),
            "source_feedback_ref": feedback_ref,
            "source_handling_record_ref": record.get("handling_record_id"),
            "question_answer_skeleton_refs": q_by_feedback.get(feedback_ref, []),
            "source_ref_satisfaction_skeleton_refs": src_by_feedback.get(feedback_ref, []),
            "under_typed_acceptance_review_skeleton_refs": acc_by_feedback.get(feedback_ref, []),
            "parking_continuation_skeleton_refs": park_by_feedback.get(feedback_ref, []),
            "current_resolution_state": "UNRESOLVED",
            "resolution_decision": "NOT_EVALUATED",
            "review_status": "TARGET_SURFACE_ONLY",
            "c5_reconsideration_ready": False,
        })

    surface_record = {
        "schema_version": "o2_weak_feedback_resolution_target_surface_record_v0",
        "surface_status": "STATIC_RESOLUTION_TARGET_SURFACE_EMITTED",
        "source_resolution_target_design_receipt_id": RT_DESIGN_RECEIPT_ID,
        "target_surface_meaning": "Record skeletons and route maps exist for later review/resolution units.",
        "target_surface_does_not_mean": [
            "question packets answered",
            "source-ref requests satisfied",
            "under-typed acceptance approved",
            "parking counted as resolution",
            "weak feedback resolved",
            "C5 unblocked",
        ],
    }

    input_mapping = {
        "schema_version": "o2_weak_feedback_resolution_input_mapping_v0",
        "mapping_status": "INPUTS_MAPPED_TO_SKELETONS",
        "weak_records_mapped_count": len(route_map),
        "question_answer_skeletons_count": len(question_skeletons),
        "source_ref_satisfaction_skeletons_count": len(source_ref_skeletons),
        "under_typed_acceptance_review_skeletons_count": len(undertyped_skeletons),
        "parking_continuation_skeletons_count": len(parking_skeletons),
        "route_map_path": rel(WEAK_FEEDBACK_ROUTE_MAP_PATH),
    }

    resolution_gate_readout = {
        "schema_version": "o2_weak_feedback_resolution_gate_readout_v0",
        "gate_status": "NOT_RESOLVED_REVIEW_REQUIRED",
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "question_packets_answered_count": 0,
        "source_ref_requests_satisfied_count": 0,
        "under_typed_acceptance_approved_count": 0,
        "parking_counted_as_resolution_count": 0,
        "weak_records_ready_for_review_count": len(route_map),
        "resolution_requires_later_review": True,
    }

    c5_reconsideration_readout = {
        "schema_version": "o2_c5_reconsideration_readout_v0",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_opened": False,
        "c5_reconsideration_ready": False,
        "reason": "Resolution target surface exists, but no reviewed resolution exists.",
    }

    nonresolution_attestation = {
        "schema_version": "o2_weak_feedback_resolution_target_nonresolution_attestation_v0",
        "attestation_status": "NONRESOLUTION_ATTESTED",
        "weak_feedback_resolved": False,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "resolution_records_emitted_count": 0,
        "live_feedback_audit_executed": False,
        "repair_applied": False,
        "retry_executed": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "architecture_change": False,
        "c5_opened": False,
    }

    write_json(SURFACE_RECORD_PATH, surface_record)
    write_json(INPUT_MAPPING_PATH, input_mapping)
    write_jsonl(QUESTION_ANSWER_SKELETONS_PATH, question_skeletons)
    write_jsonl(SOURCE_REF_SATISFACTION_SKELETONS_PATH, source_ref_skeletons)
    write_jsonl(UNDERTYPED_REVIEW_SKELETONS_PATH, undertyped_skeletons)
    write_jsonl(PARKING_CONTINUATION_SKELETONS_PATH, parking_skeletons)
    write_jsonl(WEAK_FEEDBACK_ROUTE_MAP_PATH, route_map)
    write_json(RESOLUTION_GATE_READOUT_PATH, resolution_gate_readout)
    write_json(C5_RECONSIDERATION_READOUT_PATH, c5_reconsideration_readout)
    write_json(NONRESOLUTION_ATTESTATION_PATH, nonresolution_attestation)

    if len(question_skeletons) != 3:
        failures.append(f"question_skeleton_count_wrong:{len(question_skeletons)}")
    if len(source_ref_skeletons) != 2:
        failures.append(f"source_ref_skeleton_count_wrong:{len(source_ref_skeletons)}")
    if len(undertyped_skeletons) != 2:
        failures.append(f"undertyped_skeleton_count_wrong:{len(undertyped_skeletons)}")
    if len(parking_skeletons) != 3:
        failures.append(f"parking_skeleton_count_wrong:{len(parking_skeletons)}")
    if len(route_map) != 3:
        failures.append(f"route_map_count_wrong:{len(route_map)}")
    for row in question_skeletons:
        if row.get("review_status") != "NOT_ANSWERED" or row.get("counts_as_resolution_input") is not False:
            failures.append(f"question_skeleton_not_unanswered:{row.get('answer_skeleton_id')}")
    for row in source_ref_skeletons:
        if row.get("review_status") != "UNSATISFIED" or row.get("counts_as_resolution_input") is not False:
            failures.append(f"source_ref_skeleton_not_unsatisfied:{row.get('satisfaction_skeleton_id')}")
    for row in undertyped_skeletons:
        if row.get("review_status") != "UNREVIEWED" or row.get("c5_unblock_allowed") is not False:
            failures.append(f"undertyped_skeleton_wrong:{row.get('review_skeleton_id')}")
    for row in parking_skeletons:
        if row.get("counts_as_resolution") is not False or row.get("c5_unblock_allowed") is not False:
            failures.append(f"parking_skeleton_counts_resolution:{row.get('parking_continuation_skeleton_id')}")
    for row in route_map:
        if row.get("current_resolution_state") != "UNRESOLVED" or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"route_map_wrong:{row.get('route_map_record_id')}")

    build_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_STATIC_SURFACE_EMITTED_REVIEW_READY" if build_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_BUILD_GATE_FAIL"
    recommended_next = "REVIEW_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_V0" if build_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_BUILD_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_TARGET_STATIC_SURFACE_EMITTED",
        "RESOLUTION_TARGET_DESIGN_RECEIPT_CONSUMED",
        "INPUT_MAPPING_EMITTED",
        "QUESTION_ANSWER_SKELETONS_EMITTED_NOT_ANSWERED",
        "SOURCE_REF_SATISFACTION_SKELETONS_EMITTED_UNSATISFIED",
        "UNDER_TYPED_ACCEPTANCE_REVIEW_SKELETONS_EMITTED_UNREVIEWED",
        "PARKING_CONTINUATION_SKELETONS_EMITTED_NOT_RESOLUTION",
        "WEAK_FEEDBACK_RESOLUTION_ROUTE_MAP_EMITTED",
        "RESOLUTION_GATE_READOUT_EMITTED_NOT_RESOLVED",
        "C5_RECONSIDERATION_READOUT_EMITTED_BLOCKED",
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
    ] if build_pass else failures

    authority_boundary = {
        "schema_version": "o2_weak_feedback_resolution_target_build_authority_boundary_v0",
        "status": status,
        "may_review_o2_weak_feedback_resolution_target_next": build_pass,
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
        "schema_version": "o2_weak_feedback_resolution_target_build_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "resolution_target_surface_built": build_pass,
        "recommended_next": recommended_next,
        "weak_feedback_resolved": False,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "resolution_records_emitted_count": 0,
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
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "o2_weak_feedback_resolution_target_build_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "resolution_target_surface_build_count": 1 if build_pass else 0,
        "input_mapping_count": 1 if build_pass else 0,
        "question_answer_skeletons_count": len(question_skeletons),
        "source_ref_satisfaction_skeletons_count": len(source_ref_skeletons),
        "under_typed_acceptance_review_skeletons_count": len(undertyped_skeletons),
        "parking_continuation_skeletons_count": len(parking_skeletons),
        "weak_feedback_route_map_records_count": len(route_map),
        "resolution_gate_readout_count": 1 if build_pass else 0,
        "c5_reconsideration_readout_count": 1 if build_pass else 0,
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
        "schema_version": "o2_weak_feedback_resolution_target_build_profile_v0",
        "profile_id": "o2_wf_resolution_target_build_profile_" + sha8(rollup),
        "status": status,
        "resolution_target_surface_built": build_pass,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Review the weak-feedback resolution target surface next; do not treat skeletons as answers or resolution.",
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
        "schema_version": "o2_weak_feedback_resolution_target_build_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The weak-feedback resolution target surface was built. It materialized input mappings, question-answer skeletons, source-ref satisfaction skeletons, under-typed acceptance review skeletons, parking continuation skeletons, weak-feedback route maps, resolution gate readout, and C5 reconsideration readout. It did not answer, satisfy, approve, resolve, run live audit, repair, retry, select target, patch runtime, mutate sources, or open C5.",
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_weak_feedback_resolution_target_build_transition_trace_v0",
        "trace": [
            {
                "step": "consume_resolution_target_design",
                "question": "is static resolution-target build authorized",
                "answer": "yes" if build_pass else "no",
                "taken": "materialize skeletons and route map",
            },
            {
                "step": "materialize_nonresolution_surface",
                "question": "do skeletons answer, satisfy, approve, or resolve",
                "answer": "no",
                "taken": "emit nonresolution attestation",
            },
            {
                "step": "preserve_c5_block",
                "question": "does built target surface unblock C5",
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
        "RT_BUILD_0_DESIGN_RECEIPT_CONSUMED": RT_DESIGN_RECEIPT_PATH.exists(),
        "RT_BUILD_1_SURFACE_RECORD_EMITTED": SURFACE_RECORD_PATH.exists(),
        "RT_BUILD_2_INPUT_MAPPING_EMITTED": INPUT_MAPPING_PATH.exists(),
        "RT_BUILD_3_QUESTION_ANSWER_SKELETONS_EMITTED": len(question_skeletons) == 3,
        "RT_BUILD_4_SOURCE_REF_SATISFACTION_SKELETONS_EMITTED": len(source_ref_skeletons) == 2,
        "RT_BUILD_5_UNDER_TYPED_ACCEPTANCE_REVIEW_SKELETONS_EMITTED": len(undertyped_skeletons) == 2,
        "RT_BUILD_6_PARKING_CONTINUATION_SKELETONS_EMITTED": len(parking_skeletons) == 3,
        "RT_BUILD_7_ROUTE_MAP_EMITTED": len(route_map) == 3,
        "RT_BUILD_8_RESOLUTION_GATE_READOUT_EMITTED_NOT_RESOLVED": RESOLUTION_GATE_READOUT_PATH.exists() and resolution_gate_readout["weak_feedback_resolved"] is False,
        "RT_BUILD_9_C5_RECONSIDERATION_READOUT_EMITTED_BLOCKED": C5_RECONSIDERATION_READOUT_PATH.exists() and c5_reconsideration_readout["c5_opened"] is False,
        "RT_BUILD_10_NONRESOLUTION_ATTESTED": NONRESOLUTION_ATTESTATION_PATH.exists() and nonresolution_attestation["weak_feedback_resolved"] is False,
        "RT_BUILD_11_NO_RESOLUTION_ANSWER_SATISFY_APPROVE": rollup["weak_feedback_resolved_count"] == 0 and rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "RT_BUILD_12_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "RT_BUILD_13_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "RT_BUILD_14_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "RT_BUILD_15_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "RT_BUILD_16_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "RT_BUILD_17_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_BUILD_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "question_skeletons": len(question_skeletons),
        "source_ref_skeletons": len(source_ref_skeletons),
        "route_map": len(route_map),
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_resolution_target_build_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_BUILD_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_resolution_target_design_receipt_id": RT_DESIGN_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_resolution_target_build_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "resolution_target_surface_built": build_pass,
            "input_mapping_emitted": build_pass,
            "question_answer_skeletons_emitted": len(question_skeletons),
            "source_ref_satisfaction_skeletons_emitted": len(source_ref_skeletons),
            "under_typed_acceptance_review_skeletons_emitted": len(undertyped_skeletons),
            "parking_continuation_skeletons_emitted": len(parking_skeletons),
            "weak_feedback_route_map_records_emitted": len(route_map),
            "resolution_gate_readout_emitted": build_pass,
            "c5_reconsideration_readout_emitted": build_pass,
            "nonresolution_attested": build_pass,
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
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": recommended_next,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "surface_record": rel(SURFACE_RECORD_PATH),
            "input_mapping": rel(INPUT_MAPPING_PATH),
            "question_answer_skeletons": rel(QUESTION_ANSWER_SKELETONS_PATH),
            "source_ref_satisfaction_skeletons": rel(SOURCE_REF_SATISFACTION_SKELETONS_PATH),
            "under_typed_acceptance_review_skeletons": rel(UNDERTYPED_REVIEW_SKELETONS_PATH),
            "parking_continuation_skeletons": rel(PARKING_CONTINUATION_SKELETONS_PATH),
            "weak_feedback_route_map": rel(WEAK_FEEDBACK_ROUTE_MAP_PATH),
            "resolution_gate_readout": rel(RESOLUTION_GATE_READOUT_PATH),
            "c5_reconsideration_readout": rel(C5_RECONSIDERATION_READOUT_PATH),
            "nonresolution_attestation": rel(NONRESOLUTION_ATTESTATION_PATH),
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
    print(f"weak_feedback_resolution_target_build_receipt_id={receipt_id}")
    print(f"weak_feedback_resolution_target_build_receipt_path={rel(receipt_path)}")
    print(f"weak_feedback_resolution_target_surface_record_path={rel(SURFACE_RECORD_PATH)}")
    print(f"weak_feedback_resolution_input_mapping_path={rel(INPUT_MAPPING_PATH)}")
    print(f"question_answer_skeletons_path={rel(QUESTION_ANSWER_SKELETONS_PATH)}")
    print(f"source_ref_satisfaction_skeletons_path={rel(SOURCE_REF_SATISFACTION_SKELETONS_PATH)}")
    print(f"under_typed_acceptance_review_skeletons_path={rel(UNDERTYPED_REVIEW_SKELETONS_PATH)}")
    print(f"parking_continuation_skeletons_path={rel(PARKING_CONTINUATION_SKELETONS_PATH)}")
    print(f"weak_feedback_route_map_path={rel(WEAK_FEEDBACK_ROUTE_MAP_PATH)}")
    print(f"resolution_gate_readout_path={rel(RESOLUTION_GATE_READOUT_PATH)}")
    print(f"resolution_target_build_rollup_path={rel(ROLLUP_PATH)}")
    print(f"resolution_target_build_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
