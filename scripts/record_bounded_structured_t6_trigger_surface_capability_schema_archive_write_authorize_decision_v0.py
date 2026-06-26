#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RECORD_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_AUTHORIZE_DECISION_V0"
TARGET_UNIT_ID = "bounded_structured_t6_trigger_surface_capability.schema_archive_write_authorize_decision_v0"
NEXT_UNIT_ID = "EXECUTE_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_V0"

SELECTED_DECISION = "AUTHORIZE_SCHEMA_ARCHIVE_WRITE_FOR_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY"

WRITE_PACKET_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_receipt_422cdd89"
WRITE_DECISION_PACKET_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_f86a0126"
MUTATION_TARGET_REVIEW_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_receipt_e8f12c97"
MUTATION_TARGET_REVIEW_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_213c76c7"
MUTATION_TARGET_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_63de098e"
ARCHIVE_ENTRY_CANDIDATE_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_72e26cec"

ADOPTION_PATH_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_6f9974e5"
CAPABILITY_BUILD_ID = "bounded_structured_t6_trigger_surface_capability_build_721f09dc"
PROPOSAL_ID = "capability_proposal_57dda6e9"
SCHEMA_NAME = "bounded_structured_t6_trigger_surface_capability_v0"
REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"

WRITE_PACKET_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_receipt_422cdd89.json"
WRITE_REQUEST_PACKET_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_request_packet_v0.json"
WRITE_DECISION_OPTIONS_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_decision_options_v0.json"
WRITE_DECISION_EFFECTS_MAP_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_decision_effects_map_v0.json"
WRITE_AUTHORITY_BOUNDARY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authority_boundary_v0.json"
WRITE_AUTHORIZE_OPTION_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_option_authorize_v0.json"
WRITE_NEGATIVE_CONTROL_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_negative_control_v0.json"
WRITE_PAYLOAD_BINDING_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_payload_binding_v0.json"
WRITE_SOURCE_CHAIN_BINDING_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_write_source_chain_binding_v0.json"

MUTATION_TARGET_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_receipt_e8f12c97.json"
MUTATION_TARGET_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_receipt_2063a180.json"
ARCHIVE_ENTRY_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_v0.json"
MUTATION_PLAN_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_plan_v0.json"
SCHEMA_CANDIDATE_SNAPSHOT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_schema_candidate_snapshot_v0.json"

SCHEMA_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_schema_candidate_v0.json"
CAPABILITY_PROFILE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_profile_v0.json"
BUILD_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079.json"
BUILD_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_review_receipt_b8dba552.json"
PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"

OUT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_v0"
RECEIPT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_basis_v0.json"
DECISION_RECORD_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_human_decision_record_v0.json"
AUTHORIZATION_EFFECT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorization_effect_applied_v0.json"
AUTHORITY_BOUNDARY_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_authority_boundary_review_v0.json"
WRITE_EXECUTION_TARGET_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_target_v0.json"
NEGATIVE_CONTROL_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_negative_control_v0.json"
READOUT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_transition_trace.json"

PLANNED_SCHEMA_ARCHIVE_REF = "data/schema_archive/bounded_trigger_surface_capability_schema_archive_v0.json"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def require_false(obj: Dict[str, Any], key: str, failures: List[str], prefix: str) -> None:
    if obj.get(key) is not False:
        failures.append(f"{prefix}_{key}_not_false:{obj.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        WRITE_PACKET_RECEIPT_PATH,
        WRITE_REQUEST_PACKET_PATH,
        WRITE_DECISION_OPTIONS_PATH,
        WRITE_DECISION_EFFECTS_MAP_PATH,
        WRITE_AUTHORITY_BOUNDARY_PATH,
        WRITE_AUTHORIZE_OPTION_PATH,
        WRITE_NEGATIVE_CONTROL_PATH,
        WRITE_PAYLOAD_BINDING_PATH,
        WRITE_SOURCE_CHAIN_BINDING_PATH,
        MUTATION_TARGET_REVIEW_RECEIPT_PATH,
        MUTATION_TARGET_RECEIPT_PATH,
        ARCHIVE_ENTRY_CANDIDATE_PATH,
        MUTATION_PLAN_PATH,
        SCHEMA_CANDIDATE_SNAPSHOT_PATH,
        SCHEMA_CANDIDATE_PATH,
        CAPABILITY_PROFILE_PATH,
        BUILD_RECEIPT_PATH,
        BUILD_REVIEW_RECEIPT_PATH,
        PROPOSAL_PATH,
    ]

    failures: List[str] = []
    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    write_packet_receipt = read_json(WRITE_PACKET_RECEIPT_PATH)
    request_packet = read_json(WRITE_REQUEST_PACKET_PATH)
    decision_options = read_json(WRITE_DECISION_OPTIONS_PATH)
    effects_map = read_json(WRITE_DECISION_EFFECTS_MAP_PATH)
    write_boundary = read_json(WRITE_AUTHORITY_BOUNDARY_PATH)
    authorize_option = read_json(WRITE_AUTHORIZE_OPTION_PATH)
    write_negative = read_json(WRITE_NEGATIVE_CONTROL_PATH)
    payload_binding = read_json(WRITE_PAYLOAD_BINDING_PATH)
    source_chain_binding = read_json(WRITE_SOURCE_CHAIN_BINDING_PATH)

    review_receipt = read_json(MUTATION_TARGET_REVIEW_RECEIPT_PATH)
    mutation_receipt = read_json(MUTATION_TARGET_RECEIPT_PATH)
    archive_entry_candidate = read_json(ARCHIVE_ENTRY_CANDIDATE_PATH)
    mutation_plan = read_json(MUTATION_PLAN_PATH)
    schema_candidate_snapshot = read_json(SCHEMA_CANDIDATE_SNAPSHOT_PATH)

    schema_candidate = read_json(SCHEMA_CANDIDATE_PATH)
    capability_profile = read_json(CAPABILITY_PROFILE_PATH)
    build_receipt = read_json(BUILD_RECEIPT_PATH)
    build_review_receipt = read_json(BUILD_REVIEW_RECEIPT_PATH)
    proposal = read_json(PROPOSAL_PATH)

    write_summary = write_packet_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_write_human_decision_packet_summary", {})
    review_summary = review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_summary", {})
    mutation_summary = mutation_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_summary", {})
    build_summary = build_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_summary", {})
    build_review_summary = build_review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_review_summary", {})

    if write_packet_receipt.get("receipt_id") != WRITE_PACKET_RECEIPT_ID:
        failures.append(f"write_packet_receipt_id_wrong:{write_packet_receipt.get('receipt_id')}")
    if write_packet_receipt.get("gate") != "PASS":
        failures.append("write_packet_gate_not_pass")
    if write_packet_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append("write_packet_terminal_not_stop")
    if write_packet_receipt.get("terminal", {}).get("stop_code") != "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_REQUIRED":
        failures.append(f"write_packet_stop_code_wrong:{write_packet_receipt.get('terminal', {}).get('stop_code')}")

    for key in [
        "schema_archive_write_human_decision_packet_ready",
        "human_schema_archive_write_decision_required",
    ]:
        if write_summary.get(key) is not True:
            failures.append(f"write_summary_{key}_not_true:{write_summary.get(key)}")

    if write_summary.get("human_schema_archive_write_decision_taken") is not False:
        failures.append("write_summary_decision_already_taken")
    if write_summary.get("selected_schema_archive_write_decision") is not None:
        failures.append(f"write_summary_selected_decision_not_none:{write_summary.get('selected_schema_archive_write_decision')}")
    if SELECTED_DECISION not in (write_summary.get("available_decisions") or []):
        failures.append(f"selected_decision_not_available:{SELECTED_DECISION}")

    for key in [
        "schema_archive_write_authorized",
        "schema_archive_write_executed",
        "schema_archive_mutation_authorized",
        "schema_mutation_authorized",
        "runtime_adoption_authorized",
        "runtime_patch_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "t6_live_case_execution_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(write_summary, key, failures, "write_summary")

    if request_packet.get("packet_status") != "READY_FOR_HUMAN_DECISION":
        failures.append(f"request_packet_status_wrong:{request_packet.get('packet_status')}")
    if request_packet.get("human_schema_archive_write_decision_taken") is not False:
        failures.append("request_packet_decision_already_taken")
    if request_packet.get("selected_schema_archive_write_decision") is not None:
        failures.append("request_packet_selected_decision_not_none")
    if SELECTED_DECISION not in (request_packet.get("available_decisions") or []):
        failures.append("request_packet_selected_decision_missing")

    if decision_options.get("options_status") != "READY_FOR_HUMAN_DECISION":
        failures.append(f"decision_options_status_wrong:{decision_options.get('options_status')}")
    option_names = [x.get("decision") for x in (decision_options.get("decision_options") or []) if isinstance(x, dict)]
    if SELECTED_DECISION not in option_names:
        failures.append("decision_options_selected_missing")

    selected_effect = (effects_map.get("decision_effects") or {}).get(SELECTED_DECISION)
    if not selected_effect:
        failures.append("selected_effect_missing")
    else:
        if selected_effect.get("schema_archive_write_authorized_by_packet") is not False:
            failures.append("selected_effect_write_authorized_by_packet_unexpected")
        if selected_effect.get("schema_archive_write_executed_by_packet") is not False:
            failures.append("selected_effect_write_executed_by_packet_unexpected")
        if selected_effect.get("requires_later_recorded_human_decision") is not True:
            failures.append("selected_effect_later_decision_not_required")

    if authorize_option.get("option") != SELECTED_DECISION:
        failures.append(f"authorize_option_wrong:{authorize_option.get('option')}")
    if authorize_option.get("option_status") != "AVAILABLE_NOT_SELECTED":
        failures.append(f"authorize_option_status_wrong:{authorize_option.get('option_status')}")
    if authorize_option.get("selected") is not False:
        failures.append("authorize_option_already_selected")
    if authorize_option.get("schema_archive_write_authorized_now") is not False:
        failures.append("authorize_option_write_authorized_now_unexpected")
    if authorize_option.get("schema_archive_write_executed_now") is not False:
        failures.append("authorize_option_write_executed_now_unexpected")

    for obj_name, obj in [
        ("write_boundary", write_boundary),
        ("payload_binding", payload_binding),
    ]:
        for key in [
            "schema_archive_write_authorized",
            "schema_archive_write_executed",
            "schema_archive_mutation_authorized",
            "schema_mutation_authorized",
        ]:
            if key in obj:
                require_false(obj, key, failures, obj_name)

    if write_negative.get("negative_control_status") != "PASS":
        failures.append(f"write_negative_status_wrong:{write_negative.get('negative_control_status')}")
    zero = write_negative.get("zero_counters_for_this_unit") or {}
    for key in [
        "schema_archive_mutation_count",
        "schema_mutation_count",
        "schema_archive_write_authorization_count",
        "schema_archive_write_execution_count",
        "runtime_adoption_count",
        "runtime_patch_count",
        "move_addition_count",
        "fixture_expansion_count",
        "t6_live_case_execution_count",
        "hidden_next_command_count",
        "c8_authorization_count",
    ]:
        if zero.get(key) != 0:
            failures.append(f"write_negative_counter_wrong:{key}:{zero.get(key)}")

    if source_chain_binding.get("binding_status") != "PASS":
        failures.append("source_chain_binding_not_pass")
    if payload_binding.get("write_payload_ready_for_decision") is not True:
        failures.append("payload_binding_not_ready")

    if review_summary.get("schema_archive_mutation_target_review_pass") is not True:
        failures.append("review_summary_not_pass")
    if review_summary.get("schema_archive_write_human_decision_packet_prep_target_ready") is not True:
        failures.append("review_summary_write_packet_prep_not_ready")
    if review_summary.get("mutation_target_id") != MUTATION_TARGET_ID:
        failures.append("review_summary_mutation_target_wrong")
    if review_summary.get("archive_entry_candidate_id") != ARCHIVE_ENTRY_CANDIDATE_ID:
        failures.append("review_summary_archive_entry_wrong")

    if mutation_summary.get("schema_archive_mutation_target_prepared") is not True:
        failures.append("mutation_target_not_prepared")
    if mutation_summary.get("schema_archive_write_executed") is not False:
        failures.append("mutation_summary_write_executed_unexpected")

    if archive_entry_candidate.get("archive_entry_candidate_id") != ARCHIVE_ENTRY_CANDIDATE_ID:
        failures.append("archive_entry_candidate_id_mismatch")
    if archive_entry_candidate.get("entry_status") != "CANDIDATE_ONLY_NOT_WRITTEN":
        failures.append(f"archive_entry_status_wrong:{archive_entry_candidate.get('entry_status')}")
    if archive_entry_candidate.get("archive_write_status") != "NOT_WRITTEN":
        failures.append(f"archive_write_status_wrong:{archive_entry_candidate.get('archive_write_status')}")
    if archive_entry_candidate.get("schema_archive_write_executed") is not False:
        failures.append("archive_entry_write_executed_unexpected")

    if mutation_plan.get("planned_operation") != "ADD_SCHEMA_ENTRY_CANDIDATE_TO_SCHEMA_ARCHIVE":
        failures.append(f"mutation_plan_operation_wrong:{mutation_plan.get('planned_operation')}")
    if mutation_plan.get("write_executed_now") is not False:
        failures.append("mutation_plan_write_executed_now_unexpected")
    if mutation_plan.get("schema_archive_write_authorized") is not False:
        failures.append("mutation_plan_write_authorized_unexpected")

    if schema_candidate_snapshot.get("snapshot_status") != "BOUND_FOR_REVIEW":
        failures.append(f"schema_snapshot_status_wrong:{schema_candidate_snapshot.get('snapshot_status')}")
    if schema_candidate.get("schema_name") != SCHEMA_NAME:
        failures.append(f"schema_candidate_name_wrong:{schema_candidate.get('schema_name')}")
    if schema_candidate.get("schema_candidate_status") != "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION":
        failures.append(f"schema_candidate_status_wrong:{schema_candidate.get('schema_candidate_status')}")
    if capability_profile.get("capability_name") != REQUIRED_CAPABILITY:
        failures.append(f"capability_profile_name_wrong:{capability_profile.get('capability_name')}")
    if capability_profile.get("surface_name") != SCHEMA_NAME:
        failures.append(f"capability_profile_surface_wrong:{capability_profile.get('surface_name')}")
    if build_summary.get("build_executed") is not True:
        failures.append("build_not_executed")
    if build_review_summary.get("artifact_review_pass") is not True:
        failures.append("build_review_not_pass")
    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_AUTHORIZE_DECISION_RECORDED_EXECUTION_TARGET_READY"
        if gate == "PASS"
        else "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_AUTHORIZE_DECISION_GATE_FAIL"
    )

    write_authorize_decision_record_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_" + sig8({
        "write_decision_packet_id": WRITE_DECISION_PACKET_ID,
        "selected_decision": SELECTED_DECISION,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
    })

    write_execution_target_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_target_" + sig8({
        "write_authorize_decision_record_id": write_authorize_decision_record_id,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "planned_schema_archive_ref": PLANNED_SCHEMA_ARCHIVE_REF,
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_basis_v0",
        "unit_id": UNIT_ID,
        "write_authorize_decision_record_id": write_authorize_decision_record_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_write_packet_receipt_id": WRITE_PACKET_RECEIPT_ID,
        "source_write_decision_packet_id": WRITE_DECISION_PACKET_ID,
        "selected_schema_archive_write_decision": SELECTED_DECISION if gate == "PASS" else None,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "record_claim": "Record human schema archive write authorization and prepare the bounded execution target. Do not execute the archive write.",
        "source_file_hashes": source_hashes,
    }

    decision_record = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_human_decision_record_v0",
        "decision_record_status": "HUMAN_SCHEMA_ARCHIVE_WRITE_DECISION_RECORDED" if gate == "PASS" else "BLOCKED",
        "write_authorize_decision_record_id": write_authorize_decision_record_id,
        "write_decision_packet_id": WRITE_DECISION_PACKET_ID,
        "mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
        "selected_schema_archive_write_decision": SELECTED_DECISION if gate == "PASS" else None,
        "human_schema_archive_write_decision_taken": True if gate == "PASS" else False,
        "decision_effect": "AUTHORIZE_BOUNDED_SCHEMA_ARCHIVE_WRITE_EXECUTION_TARGET" if gate == "PASS" else "NONE",
        "decision_does_not_execute_schema_archive_write": True,
        "decision_does_not_authorize_runtime_adoption": True,
        "decision_does_not_authorize_move_addition": True,
        "decision_does_not_authorize_fixture_expansion": True,
        "decision_does_not_authorize_t6_live_case_execution": True,
        "decision_does_not_authorize_c8": True,
    }

    authorization_effect = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorization_effect_applied_v0",
        "write_authorize_decision_record_id": write_authorize_decision_record_id,
        "effect_status": "APPLIED_TO_WRITE_EXECUTION_TARGET_ONLY" if gate == "PASS" else "BLOCKED",
        "selected_schema_archive_write_decision": SELECTED_DECISION if gate == "PASS" else None,
        "schema_archive_write_authorized": True if gate == "PASS" else False,
        "schema_archive_mutation_authorized": True if gate == "PASS" else False,
        "schema_archive_write_execution_target_ready": True if gate == "PASS" else False,
        "schema_archive_write_execution_target_id": write_execution_target_id if gate == "PASS" else None,
        "schema_archive_write_executed": False,
        "schema_archive_mutation_executed": False,
        "schema_mutation_authorized": False,
        "schema_mutation_executed": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    authority_boundary_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_authority_boundary_review_v0",
        "write_authorize_decision_record_id": write_authorize_decision_record_id,
        "review_status": "PASS" if gate == "PASS" else "BLOCKED",
        "allowed_effect": "prepare bounded schema archive write execution target",
        "not_allowed_effects": [
            "execute schema archive write in this unit",
            "modify schema candidate content",
            "runtime adoption",
            "runtime patch",
            "move addition",
            "fixture expansion",
            "T6 live case execution",
            "C8 authorization",
        ],
        "schema_archive_write_authorized": True if gate == "PASS" else False,
        "schema_archive_mutation_authorized": True if gate == "PASS" else False,
        "schema_archive_write_execution_target_ready": True if gate == "PASS" else False,
        "schema_archive_write_executed": False,
        "schema_archive_mutation_executed": False,
        "schema_mutation_authorized": False,
        "schema_mutation_executed": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "c8_authorized": False,
    }

    write_execution_target = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "schema_archive_write_execution_target_id": write_execution_target_id if gate == "PASS" else None,
        "write_authorize_decision_record_id": write_authorize_decision_record_id,
        "write_decision_packet_id": WRITE_DECISION_PACKET_ID,
        "selected_schema_archive_write_decision": SELECTED_DECISION if gate == "PASS" else None,
        "mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "schema_name": SCHEMA_NAME,
        "archive_entry_candidate_ref": rel(ARCHIVE_ENTRY_CANDIDATE_PATH),
        "mutation_plan_ref": rel(MUTATION_PLAN_PATH),
        "schema_candidate_snapshot_ref": rel(SCHEMA_CANDIDATE_SNAPSHOT_PATH),
        "planned_schema_archive_ref": PLANNED_SCHEMA_ARCHIVE_REF,
        "planned_operation": "ADD_SCHEMA_ENTRY_CANDIDATE_TO_SCHEMA_ARCHIVE",
        "target_scope": "Execute one bounded schema archive write for this reviewed archive-entry candidate only.",
        "schema_archive_write_authorized": True if gate == "PASS" else False,
        "schema_archive_mutation_authorized": True if gate == "PASS" else False,
        "schema_archive_write_executed": False,
        "schema_archive_mutation_executed": False,
        "schema_mutation_authorized": False,
        "schema_mutation_executed": False,
        "must_fail_if_archive_entry_already_exists": True,
        "must_emit_write_receipt": True,
        "does_not_authorize_runtime_adoption": True,
        "does_not_authorize_move_addition": True,
        "does_not_authorize_fixture_expansion": True,
        "does_not_authorize_t6_live_case_execution": True,
        "does_not_authorize_c8": True,
    }

    negative_control = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_negative_control_v0",
        "write_authorize_decision_record_id": write_authorize_decision_record_id,
        "negative_control_status": "PASS" if gate == "PASS" else "BLOCKED",
        "selected_schema_archive_write_decision": SELECTED_DECISION if gate == "PASS" else None,
        "schema_archive_write_authorized": True if gate == "PASS" else False,
        "schema_archive_mutation_authorized": True if gate == "PASS" else False,
        "zero_counters_for_this_unit": {
            "schema_archive_write_execution_count": 0,
            "schema_archive_mutation_execution_count": 0,
            "schema_content_mutation_count": 0,
            "runtime_adoption_count": 0,
            "runtime_patch_count": 0,
            "move_addition_count": 0,
            "fixture_expansion_count": 0,
            "t6_live_case_execution_count": 0,
            "hidden_next_command_count": 0,
            "c8_authorization_count": 0,
        },
        "positive_authorization_counters_for_this_unit": {
            "schema_archive_write_authorization_count": 1 if gate == "PASS" else 0,
            "schema_archive_mutation_authorization_count": 1 if gate == "PASS" else 0,
        },
        "negative_control_rule": "This unit records write authorization and emits an execution target, but performs zero archive writes.",
    }

    rollup = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "write_authorize_decision_record_id": write_authorize_decision_record_id,
        "write_decision_packet_id": WRITE_DECISION_PACKET_ID,
        "selected_schema_archive_write_decision": SELECTED_DECISION if gate == "PASS" else None,
        "human_schema_archive_write_decision_taken": True if gate == "PASS" else False,
        "schema_archive_write_authorized": True if gate == "PASS" else False,
        "schema_archive_mutation_authorized": True if gate == "PASS" else False,
        "schema_archive_write_execution_target_ready": True if gate == "PASS" else False,
        "schema_archive_write_execution_target_id": write_execution_target_id if gate == "PASS" else None,
        "schema_archive_write_executed": False,
        "schema_archive_mutation_executed": False,
        "schema_mutation_authorized": False,
        "schema_mutation_executed": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    readout = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_readout_v0",
        "status": status,
        "write_authorize_decision_record_id": write_authorize_decision_record_id,
        "selected_schema_archive_write_decision": SELECTED_DECISION if gate == "PASS" else None,
        "interpretation": "Human authorized the bounded schema archive write. Execution target is ready; no schema archive write has executed yet."
        if gate == "PASS" else "Schema archive write authorize decision recording failed typed gates.",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_profile_v0",
        "profile_status": status,
        "write_authorize_decision_record_id": write_authorize_decision_record_id,
        "core_rule": "Record write authorization and prepare execution target only. The actual schema archive write occurs only in the next bounded execution unit.",
        "write_execution_target_ref": rel(WRITE_EXECUTION_TARGET_PATH),
        "must_not_infer": [
            "schema archive write executed",
            "schema archive entry already promoted",
            "schema candidate content mutated",
            "runtime adopted",
            "runtime patched",
            "move registry updated",
            "fixture suite expanded",
            "T6 live case executed",
            "C8 authorized",
        ],
    }

    report = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "decision_result": "SCHEMA_ARCHIVE_WRITE_EXECUTION_TARGET_READY" if gate == "PASS" else "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_DECISION_GATE_FAIL",
            "write_authorize_decision_record_id": write_authorize_decision_record_id,
            "write_decision_packet_id": WRITE_DECISION_PACKET_ID,
            "selected_schema_archive_write_decision": SELECTED_DECISION if gate == "PASS" else None,
            "schema_archive_write_authorized": True if gate == "PASS" else False,
            "schema_archive_write_execution_target_ready": True if gate == "PASS" else False,
            "schema_archive_write_execution_target_id": write_execution_target_id if gate == "PASS" else None,
            "schema_archive_write_executed": False,
            "schema_archive_mutation_executed": False,
            "schema_mutation_authorized": False,
            "runtime_adoption_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "t6_live_case_execution_authorized": False,
            "c8_authorized": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_transition_trace_v0",
        "unit_id": UNIT_ID,
        "write_authorize_decision_record_id": write_authorize_decision_record_id,
        "transitions": [
            {
                "from": "STOP_SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_REQUIRED",
                "edge": "record human authorization of bounded schema archive write",
                "to": "SCHEMA_ARCHIVE_WRITE_AUTHORIZATION_RECORDED" if gate == "PASS" else "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_DECISION_GATE_FAIL",
            },
            {
                "from": "SCHEMA_ARCHIVE_WRITE_AUTHORIZATION_RECORDED" if gate == "PASS" else "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_DECISION_GATE_FAIL",
                "edge": "emit bounded schema archive write execution target without writing archive",
                "to": "SCHEMA_ARCHIVE_WRITE_EXECUTION_TARGET_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_AUTHORIZE_DECISION_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (DECISION_RECORD_PATH, decision_record),
        (AUTHORIZATION_EFFECT_PATH, authorization_effect),
        (AUTHORITY_BOUNDARY_REVIEW_PATH, authority_boundary_review),
        (WRITE_EXECUTION_TARGET_PATH, write_execution_target),
        (NEGATIVE_CONTROL_PATH, negative_control),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "SCHEMA_ARCHIVE_WRITE_HUMAN_DECISION_PACKET_RECEIPT_CONSUMED",
        "HUMAN_SELECTED_AUTHORIZE_SCHEMA_ARCHIVE_WRITE",
        "AUTHORIZE_OPTION_AVAILABLE",
        "HUMAN_SCHEMA_ARCHIVE_WRITE_DECISION_RECORDED",
        "SCHEMA_ARCHIVE_WRITE_AUTHORIZATION_RECORDED",
        "SCHEMA_ARCHIVE_WRITE_EXECUTION_TARGET_EMITTED",
        "NO_SCHEMA_ARCHIVE_WRITE_EXECUTION",
        "NO_SCHEMA_ARCHIVE_MUTATION_EXECUTION",
        "NO_SCHEMA_CONTENT_MUTATION",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_RUNTIME_PATCH",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION",
        "NO_T6_LIVE_CASE_EXECUTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_WRITE_AUTHORIZE_DECISION_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "write_authorize_decision_record_id": write_authorize_decision_record_id,
        "write_decision_packet_id": WRITE_DECISION_PACKET_ID,
        "source_write_packet_receipt_id": WRITE_PACKET_RECEIPT_ID,
        "source_write_packet_receipt_ref": rel(WRITE_PACKET_RECEIPT_PATH),
        "mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
        "mutation_target_id": MUTATION_TARGET_ID,
        "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_0_PACKET_RECEIPT_CONSUMED": gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_1_SELECTED_DECISION_AVAILABLE": SELECTED_DECISION in (write_summary.get("available_decisions") or []),
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_2_AUTHORIZE_OPTION_AVAILABLE_NOT_SELECTED": authorize_option.get("option_status") == "AVAILABLE_NOT_SELECTED",
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_3_HUMAN_DECISION_RECORDED": gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_4_WRITE_AUTHORIZATION_RECORDED": gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_5_EXECUTION_TARGET_EMITTED": WRITE_EXECUTION_TARGET_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_6_NO_SCHEMA_ARCHIVE_WRITE_EXECUTION": True,
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_7_NO_SCHEMA_ARCHIVE_MUTATION_EXECUTION": True,
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_8_NO_SCHEMA_CONTENT_MUTATION": True,
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_9_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_10_NO_RUNTIME_PATCH": True,
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_11_NO_MOVE_ADDITION": True,
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_12_NO_FIXTURE_EXPANSION": True,
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_13_NO_T6_LIVE_CASE_EXECUTION": True,
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_14_NO_C8_AUTHORIZATION": True,
            "SCHEMA_ARCHIVE_WRITE_AUTHORIZE_15_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_summary": {
            "status": status,
            "write_authorize_decision_record_id": write_authorize_decision_record_id,
            "write_decision_packet_id": WRITE_DECISION_PACKET_ID,
            "source_write_packet_receipt_id": WRITE_PACKET_RECEIPT_ID,
            "selected_schema_archive_write_decision": SELECTED_DECISION if gate == "PASS" else None,
            "human_schema_archive_write_decision_taken": True if gate == "PASS" else False,
            "mutation_target_review_id": MUTATION_TARGET_REVIEW_ID,
            "mutation_target_id": MUTATION_TARGET_ID,
            "archive_entry_candidate_id": ARCHIVE_ENTRY_CANDIDATE_ID,
            "schema_name": SCHEMA_NAME,
            "schema_archive_write_authorized": True if gate == "PASS" else False,
            "schema_archive_mutation_authorized": True if gate == "PASS" else False,
            "schema_archive_write_execution_target_ready": True if gate == "PASS" else False,
            "schema_archive_write_execution_target_id": write_execution_target_id if gate == "PASS" else None,
            "planned_schema_archive_ref": PLANNED_SCHEMA_ARCHIVE_REF,
            "schema_archive_write_executed": False,
            "schema_archive_mutation_executed": False,
            "schema_mutation_authorized": False,
            "schema_mutation_executed": False,
            "runtime_adoption_authorized": False,
            "runtime_patch_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "t6_live_case_execution_authorized": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "decision_record": rel(DECISION_RECORD_PATH),
            "authorization_effect": rel(AUTHORIZATION_EFFECT_PATH),
            "authority_boundary_review": rel(AUTHORITY_BOUNDARY_REVIEW_PATH),
            "write_execution_target": rel(WRITE_EXECUTION_TARGET_PATH),
            "negative_control": rel(NEGATIVE_CONTROL_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_receipt_id={receipt_id}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_receipt_path={rel(receipt_path)}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_decision_record_id={write_authorize_decision_record_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_write_execution_target_id={write_execution_target_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_write_authorize_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
