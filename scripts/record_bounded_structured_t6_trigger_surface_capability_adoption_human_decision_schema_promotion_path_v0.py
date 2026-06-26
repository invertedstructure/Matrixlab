#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RECORD_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_HUMAN_DECISION_SCHEMA_ARCHIVE_PROMOTION_PATH_V0"
TARGET_UNIT_ID = "bounded_structured_t6_trigger_surface_capability.adoption_human_decision_schema_promotion_path_v0"
NEXT_UNIT_ID = "PREPARE_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_V0"

SELECTED_DECISION = "PREPARE_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET"

HUMAN_DECISION_PACKET_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_receipt_52138534"
HUMAN_DECISION_PACKET_ID = "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_38ae00c0"
ADOPTION_REVIEW_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_review_9d2fb29e"
ADOPTION_PATH_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_6f9974e5"
CAPABILITY_BUILD_ID = "bounded_structured_t6_trigger_surface_capability_build_721f09dc"
PROPOSAL_ID = "capability_proposal_57dda6e9"
REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"

HUMAN_DECISION_PACKET_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_v0_receipts/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_receipt_52138534.json"
HUMAN_DECISION_REQUEST_PACKET_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_request_packet_v0.json"
DECISION_OPTIONS_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_options_v0.json"
DECISION_EFFECTS_MAP_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_effects_map_v0.json"
AUTHORITY_BOUNDARY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_authority_boundary_v0.json"
SCHEMA_PROMOTION_OPTION_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_adoption_option_schema_archive_promotion_v0.json"
NEGATIVE_CONTROL_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_negative_control_v0.json"

ADOPTION_PATH_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_adoption_path_review_receipt_ec071b02.json"
ADOPTION_PATH_PREP_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0_receipts/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_receipt_34a6f83a.json"
SCHEMA_PROMOTION_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_candidate_v0.json"

BUILD_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_review_receipt_b8dba552.json"
BUILD_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079.json"
SCHEMA_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_schema_candidate_v0.json"
CAPABILITY_PROFILE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_profile_v0.json"
PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"

OUT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_schema_promotion_path_v0"
RECEIPT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_schema_promotion_path_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_basis_v0.json"
DECISION_RECORD_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_record_v0.json"
DECISION_EFFECT_APPLIED_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_promotion_decision_effect_applied_v0.json"
AUTHORITY_BOUNDARY_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_promotion_decision_authority_boundary_review_v0.json"
SCHEMA_PROMOTION_DECISION_PACKET_PREP_TARGET_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_prep_target_v0.json"
NEGATIVE_CONTROL_RESULT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_promotion_decision_negative_control_v0.json"
READOUT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_transition_trace.json"

FORBIDDEN_AUTHORITY_KEYS = [
    "runtime_adoption_authorized",
    "runtime_patch_authorized",
    "schema_archive_mutation_authorized",
    "schema_mutation_authorized",
    "move_addition_authorized",
    "fixture_expansion_authorized",
    "t6_live_case_execution_authorized",
    "hidden_next_command",
    "c8_authorized",
]

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
        HUMAN_DECISION_PACKET_RECEIPT_PATH,
        HUMAN_DECISION_REQUEST_PACKET_PATH,
        DECISION_OPTIONS_PATH,
        DECISION_EFFECTS_MAP_PATH,
        AUTHORITY_BOUNDARY_PATH,
        SCHEMA_PROMOTION_OPTION_PATH,
        NEGATIVE_CONTROL_PATH,
        ADOPTION_PATH_REVIEW_RECEIPT_PATH,
        ADOPTION_PATH_PREP_RECEIPT_PATH,
        SCHEMA_PROMOTION_CANDIDATE_PATH,
        BUILD_REVIEW_RECEIPT_PATH,
        BUILD_RECEIPT_PATH,
        SCHEMA_CANDIDATE_PATH,
        CAPABILITY_PROFILE_PATH,
        PROPOSAL_PATH,
    ]

    failures: List[str] = []

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    packet_receipt = read_json(HUMAN_DECISION_PACKET_RECEIPT_PATH)
    request_packet = read_json(HUMAN_DECISION_REQUEST_PACKET_PATH)
    decision_options = read_json(DECISION_OPTIONS_PATH)
    effects_map = read_json(DECISION_EFFECTS_MAP_PATH)
    source_authority_boundary = read_json(AUTHORITY_BOUNDARY_PATH)
    schema_promotion_option = read_json(SCHEMA_PROMOTION_OPTION_PATH)
    negative_control = read_json(NEGATIVE_CONTROL_PATH)

    adoption_review_receipt = read_json(ADOPTION_PATH_REVIEW_RECEIPT_PATH)
    adoption_prep_receipt = read_json(ADOPTION_PATH_PREP_RECEIPT_PATH)
    schema_promotion_candidate = read_json(SCHEMA_PROMOTION_CANDIDATE_PATH)
    build_review_receipt = read_json(BUILD_REVIEW_RECEIPT_PATH)
    build_receipt = read_json(BUILD_RECEIPT_PATH)
    schema_candidate = read_json(SCHEMA_CANDIDATE_PATH)
    capability_profile = read_json(CAPABILITY_PROFILE_PATH)
    proposal = read_json(PROPOSAL_PATH)

    packet_summary = packet_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_summary", {})
    adoption_review_summary = adoption_review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_adoption_path_review_summary", {})
    adoption_prep_summary = adoption_prep_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_adoption_path_prep_summary", {})
    build_review_summary = build_review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_review_summary", {})
    build_summary = build_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_summary", {})

    if packet_receipt.get("receipt_id") != HUMAN_DECISION_PACKET_RECEIPT_ID:
        failures.append(f"packet_receipt_id_wrong:{packet_receipt.get('receipt_id')}")
    if packet_receipt.get("gate") != "PASS":
        failures.append("packet_receipt_gate_not_pass")
    if packet_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append("packet_terminal_not_stop")
    if packet_receipt.get("terminal", {}).get("stop_code") != "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_HUMAN_DECISION_REQUIRED":
        failures.append(f"packet_stop_code_wrong:{packet_receipt.get('terminal', {}).get('stop_code')}")

    if packet_summary.get("human_decision_packet_ready") is not True:
        failures.append("human_decision_packet_not_ready")
    if packet_summary.get("human_adoption_decision_required") is not True:
        failures.append("human_adoption_decision_not_required")
    if packet_summary.get("human_adoption_decision_taken") is not False:
        failures.append("human_adoption_decision_already_taken")
    if packet_summary.get("selected_adoption_decision") is not None:
        failures.append(f"selected_decision_already_set:{packet_summary.get('selected_adoption_decision')}")
    if SELECTED_DECISION not in (packet_summary.get("available_decisions") or []):
        failures.append(f"selected_decision_not_available:{SELECTED_DECISION}")

    for key in FORBIDDEN_AUTHORITY_KEYS:
        require_false(packet_summary, key, failures, "packet_summary")

    if request_packet.get("packet_status") != "READY_FOR_HUMAN_DECISION":
        failures.append(f"request_packet_status_wrong:{request_packet.get('packet_status')}")
    if request_packet.get("human_decision_taken") is not False:
        failures.append("request_packet_human_decision_taken_not_false")
    if request_packet.get("selected_adoption_decision") is not None:
        failures.append("request_packet_selected_decision_not_none")
    if SELECTED_DECISION not in (request_packet.get("available_decisions") or []):
        failures.append("request_packet_selected_decision_missing")

    if decision_options.get("options_status") != "READY_FOR_HUMAN_DECISION":
        failures.append(f"decision_options_status_wrong:{decision_options.get('options_status')}")
    if decision_options.get("selected_adoption_decision") is not None:
        failures.append("decision_options_selected_not_none")
    option_names = [x.get("decision") for x in (decision_options.get("decision_options") or []) if isinstance(x, dict)]
    if SELECTED_DECISION not in option_names:
        failures.append("decision_options_selected_missing")

    if effects_map.get("effects_status") != "READY_FOR_HUMAN_DECISION":
        failures.append(f"effects_map_status_wrong:{effects_map.get('effects_status')}")
    selected_effect = (effects_map.get("decision_effects") or {}).get(SELECTED_DECISION)
    if not selected_effect:
        failures.append("selected_effect_missing")
    else:
        if selected_effect.get("schema_archive_mutation_authorized") is not False:
            failures.append("selected_effect_schema_archive_mutation_authorized_unexpected")
        if selected_effect.get("schema_mutation_authorized") is not False:
            failures.append("selected_effect_schema_mutation_authorized_unexpected")

    if source_authority_boundary.get("human_decision_required") is not True:
        failures.append("source_boundary_human_decision_required_not_true")
    if source_authority_boundary.get("human_decision_taken") is not False:
        failures.append("source_boundary_human_decision_taken_not_false")
    for key in FORBIDDEN_AUTHORITY_KEYS:
        require_false(source_authority_boundary, key, failures, "source_authority_boundary")

    if schema_promotion_option.get("option") != SELECTED_DECISION:
        failures.append(f"schema_promotion_option_wrong:{schema_promotion_option.get('option')}")
    if schema_promotion_option.get("option_status") != "AVAILABLE_NOT_SELECTED":
        failures.append(f"schema_promotion_option_status_wrong:{schema_promotion_option.get('option_status')}")
    if schema_promotion_option.get("selected") is not False:
        failures.append("schema_promotion_option_already_selected")
    if schema_promotion_option.get("schema_archive_mutation_authorized") is not False:
        failures.append("schema_promotion_option_archive_mutation_authorized_unexpected")
    if schema_promotion_option.get("schema_mutation_authorized") is not False:
        failures.append("schema_promotion_option_schema_mutation_authorized_unexpected")

    if schema_promotion_candidate.get("candidate_status") != "CANDIDATE_ONLY_NOT_AUTHORIZED":
        failures.append(f"schema_promotion_candidate_status_wrong:{schema_promotion_candidate.get('candidate_status')}")
    if schema_promotion_candidate.get("schema_archive_mutation_authorized") is not False:
        failures.append("schema_promotion_candidate_archive_mutation_authorized_unexpected")
    if schema_promotion_candidate.get("schema_mutation_authorized") is not False:
        failures.append("schema_promotion_candidate_schema_mutation_authorized_unexpected")

    if negative_control.get("negative_control_status") != "PASS":
        failures.append(f"negative_control_status_wrong:{negative_control.get('negative_control_status')}")
    zero = negative_control.get("zero_counters_for_this_unit") or {}
    for key in [
        "runtime_adoption_count",
        "runtime_patch_count",
        "schema_archive_mutation_count",
        "schema_mutation_count",
        "move_addition_count",
        "fixture_expansion_count",
        "t6_live_case_execution_count",
        "hidden_next_command_count",
        "c8_authorization_count",
    ]:
        if zero.get(key) != 0:
            failures.append(f"source_negative_control_zero_counter_wrong:{key}:{zero.get(key)}")

    if adoption_review_summary.get("adoption_path_review_pass") is not True:
        failures.append("source_adoption_review_not_pass")
    if adoption_prep_summary.get("adoption_path_prepared") is not True:
        failures.append("source_adoption_path_not_prepared")
    if build_review_summary.get("artifact_review_pass") is not True:
        failures.append("source_build_review_not_pass")
    if build_summary.get("build_executed") is not True:
        failures.append("source_build_not_executed")
    if schema_candidate.get("schema_candidate_status") != "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION":
        failures.append(f"schema_candidate_status_wrong:{schema_candidate.get('schema_candidate_status')}")
    if schema_candidate.get("archive_mutation_authorized") is not False:
        failures.append("schema_candidate_archive_mutation_authorized_unexpected")
    if capability_profile.get("capability_name") != REQUIRED_CAPABILITY:
        failures.append("capability_profile_name_wrong")
    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_PROMOTION_PATH_HUMAN_DECISION_RECORDED_PREP_READY"
        if gate == "PASS"
        else "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_PROMOTION_PATH_HUMAN_DECISION_RECORD_GATE_FAIL"
    )

    human_decision_record_id = "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_" + sig8({
        "human_decision_packet_id": HUMAN_DECISION_PACKET_ID,
        "selected_decision": SELECTED_DECISION,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
    })

    schema_promotion_packet_prep_target_id = "bounded_structured_t6_trigger_surface_capability_schema_promotion_packet_prep_target_" + sig8({
        "human_decision_record_id": human_decision_record_id,
        "selected_decision": SELECTED_DECISION,
        "schema_candidate": PROPOSED_SURFACE,
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_basis_v0",
        "unit_id": UNIT_ID,
        "human_decision_record_id": human_decision_record_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_human_decision_packet_receipt_id": HUMAN_DECISION_PACKET_RECEIPT_ID,
        "source_human_decision_packet_id": HUMAN_DECISION_PACKET_ID,
        "selected_decision": SELECTED_DECISION,
        "source_adoption_path_id": ADOPTION_PATH_ID,
        "source_capability_build_id": CAPABILITY_BUILD_ID,
        "source_proposal_id": PROPOSAL_ID,
        "record_claim": "Record human selection of schema archive promotion decision-packet preparation only. Do not mutate schema archive or promote schema.",
        "source_file_hashes": source_hashes,
    }

    decision_record = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_record_v0",
        "decision_record_status": "HUMAN_DECISION_RECORDED" if gate == "PASS" else "BLOCKED",
        "human_decision_record_id": human_decision_record_id,
        "human_decision_packet_id": HUMAN_DECISION_PACKET_ID,
        "adoption_review_id": ADOPTION_REVIEW_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
        "human_adoption_decision_taken": True if gate == "PASS" else False,
        "decision_effect": "AUTHORIZE_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_PREP_ONLY" if gate == "PASS" else "NONE",
        "decision_does_not_authorize_schema_archive_mutation": True,
        "decision_does_not_authorize_schema_mutation": True,
        "decision_does_not_authorize_runtime_adoption": True,
        "decision_does_not_authorize_move_addition": True,
        "decision_does_not_authorize_fixture_expansion": True,
        "decision_does_not_authorize_t6_live_case_execution": True,
        "decision_does_not_authorize_c8": True,
    }

    decision_effect_applied = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_promotion_decision_effect_applied_v0",
        "human_decision_record_id": human_decision_record_id,
        "effect_status": "APPLIED_TO_NEXT_PREP_TARGET_ONLY" if gate == "PASS" else "BLOCKED",
        "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
        "schema_promotion_decision_packet_prep_authorized": True if gate == "PASS" else False,
        "schema_archive_promotion_decision_packet_prep_target_id": schema_promotion_packet_prep_target_id if gate == "PASS" else None,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    authority_boundary_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_promotion_decision_authority_boundary_review_v0",
        "human_decision_record_id": human_decision_record_id,
        "review_status": "PASS" if gate == "PASS" else "BLOCKED",
        "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
        "allowed_effect": "prepare schema archive promotion decision packet",
        "not_allowed_effects": [
            "schema archive mutation",
            "schema mutation",
            "schema archive promotion execution",
            "runtime adoption",
            "runtime patch",
            "move addition",
            "fixture expansion",
            "T6 live case execution",
            "C8 authorization",
        ],
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "runtime_adoption_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "c8_authorized": False,
    }

    schema_promotion_packet_prep_target = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_prep_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "schema_archive_promotion_decision_packet_prep_target_id": schema_promotion_packet_prep_target_id if gate == "PASS" else None,
        "human_decision_record_id": human_decision_record_id,
        "human_decision_packet_id": HUMAN_DECISION_PACKET_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
        "target_scope": "Prepare a bounded schema archive promotion decision packet for the reviewed schema candidate. Do not mutate or promote the schema archive in this target/prep path.",
        "source_schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "source_schema_candidate_status": schema_candidate.get("schema_candidate_status"),
        "human_decision_required_later_for_actual_schema_archive_mutation": True,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "does_not_authorize_runtime_adoption": True,
        "does_not_authorize_move_addition": True,
        "does_not_authorize_fixture_expansion": True,
        "does_not_authorize_t6_live_case_execution": True,
        "does_not_authorize_c8": True,
    }

    negative_control_result = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_promotion_decision_negative_control_v0",
        "human_decision_record_id": human_decision_record_id,
        "negative_control_status": "PASS" if gate == "PASS" else "BLOCKED",
        "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
        "schema_promotion_decision_packet_prep_authorized": True if gate == "PASS" else False,
        "schema_archive_mutation_count": 0,
        "schema_mutation_count": 0,
        "runtime_adoption_count": 0,
        "runtime_patch_count": 0,
        "move_addition_count": 0,
        "fixture_expansion_count": 0,
        "t6_live_case_execution_count": 0,
        "hidden_next_command_count": 0,
        "c8_authorization_count": 0,
        "negative_control_rule": "Human selection opens only the next schema-promotion decision-packet prep unit; it does not promote or mutate schema archive.",
    }

    rollup = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "human_decision_record_id": human_decision_record_id,
        "human_decision_packet_id": HUMAN_DECISION_PACKET_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "human_adoption_decision_taken": True if gate == "PASS" else False,
        "selected_adoption_decision": SELECTED_DECISION if gate == "PASS" else None,
        "schema_promotion_decision_packet_prep_authorized": True if gate == "PASS" else False,
        "schema_archive_promotion_decision_packet_prep_target_ready": True if gate == "PASS" else False,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_readout_v0",
        "status": status,
        "human_decision_record_id": human_decision_record_id,
        "selected_adoption_decision": SELECTED_DECISION if gate == "PASS" else None,
        "interpretation": "Human selected schema archive promotion decision-packet preparation. Only the next bounded decision-packet prep target is ready; no schema archive mutation or schema promotion occurred."
        if gate == "PASS" else "Schema promotion human decision recording failed typed gates.",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_profile_v0",
        "profile_status": status,
        "human_decision_record_id": human_decision_record_id,
        "core_rule": "Record human decision selecting schema archive promotion path preparation only. Actual schema archive mutation requires a later explicit human decision and receipt.",
        "schema_archive_promotion_decision_packet_prep_target_ref": rel(SCHEMA_PROMOTION_DECISION_PACKET_PREP_TARGET_PATH),
        "must_not_infer": [
            "schema archive mutated",
            "schema promoted",
            "schema mutation authorized",
            "runtime adopted",
            "runtime patched",
            "move registry updated",
            "fixture suite expanded",
            "T6 live case executed",
            "C8 authorized",
        ],
    }

    report = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "decision_result": "SCHEMA_PROMOTION_DECISION_PACKET_PREP_READY" if gate == "PASS" else "SCHEMA_PROMOTION_DECISION_RECORD_GATE_FAIL",
            "human_decision_record_id": human_decision_record_id,
            "human_decision_packet_id": HUMAN_DECISION_PACKET_ID,
            "selected_adoption_decision": SELECTED_DECISION if gate == "PASS" else None,
            "schema_promotion_decision_packet_prep_authorized": True if gate == "PASS" else False,
            "schema_archive_mutation_authorized": False,
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_transition_trace_v0",
        "unit_id": UNIT_ID,
        "human_decision_record_id": human_decision_record_id,
        "transitions": [
            {
                "from": "STOP_HUMAN_DECISION_REQUIRED",
                "edge": "record human selected schema archive promotion decision-packet preparation",
                "to": "SCHEMA_PROMOTION_PATH_HUMAN_DECISION_RECORDED" if gate == "PASS" else "SCHEMA_PROMOTION_HUMAN_DECISION_RECORD_GATE_FAIL",
            },
            {
                "from": "SCHEMA_PROMOTION_PATH_HUMAN_DECISION_RECORDED" if gate == "PASS" else "SCHEMA_PROMOTION_HUMAN_DECISION_RECORD_GATE_FAIL",
                "edge": "emit schema archive promotion decision-packet prep target without schema mutation",
                "to": "SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_PREP_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_PROMOTION_HUMAN_DECISION_RECORD_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (DECISION_RECORD_PATH, decision_record),
        (DECISION_EFFECT_APPLIED_PATH, decision_effect_applied),
        (AUTHORITY_BOUNDARY_REVIEW_PATH, authority_boundary_review),
        (SCHEMA_PROMOTION_DECISION_PACKET_PREP_TARGET_PATH, schema_promotion_packet_prep_target),
        (NEGATIVE_CONTROL_RESULT_PATH, negative_control_result),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "HUMAN_DECISION_PACKET_RECEIPT_CONSUMED",
        "HUMAN_SELECTED_PREPARE_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET",
        "SCHEMA_PROMOTION_OPTION_AVAILABLE",
        "HUMAN_DECISION_RECORDED",
        "SCHEMA_PROMOTION_DECISION_PACKET_PREP_TARGET_EMITTED",
        "NO_SCHEMA_ARCHIVE_MUTATION",
        "NO_SCHEMA_MUTATION",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_RUNTIME_PATCH",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION",
        "NO_T6_LIVE_CASE_EXECUTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "human_decision_record_id": human_decision_record_id,
        "human_decision_packet_id": HUMAN_DECISION_PACKET_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "source_human_decision_packet_receipt_id": HUMAN_DECISION_PACKET_RECEIPT_ID,
        "source_human_decision_packet_receipt_ref": rel(HUMAN_DECISION_PACKET_RECEIPT_PATH),
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "SCHEMA_PROMOTION_DECISION_0_PACKET_RECEIPT_CONSUMED": gate == "PASS",
            "SCHEMA_PROMOTION_DECISION_1_SELECTED_DECISION_AVAILABLE": SELECTED_DECISION in (packet_summary.get("available_decisions") or []),
            "SCHEMA_PROMOTION_DECISION_2_OPTION_AVAILABLE_NOT_SELECTED": schema_promotion_option.get("option_status") == "AVAILABLE_NOT_SELECTED",
            "SCHEMA_PROMOTION_DECISION_3_HUMAN_DECISION_RECORDED": gate == "PASS",
            "SCHEMA_PROMOTION_DECISION_4_PREP_TARGET_EMITTED": SCHEMA_PROMOTION_DECISION_PACKET_PREP_TARGET_PATH.exists() and gate == "PASS",
            "SCHEMA_PROMOTION_DECISION_5_NO_SCHEMA_ARCHIVE_MUTATION": True,
            "SCHEMA_PROMOTION_DECISION_6_NO_SCHEMA_MUTATION": True,
            "SCHEMA_PROMOTION_DECISION_7_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "SCHEMA_PROMOTION_DECISION_8_NO_RUNTIME_PATCH": True,
            "SCHEMA_PROMOTION_DECISION_9_NO_MOVE_ADDITION": True,
            "SCHEMA_PROMOTION_DECISION_10_NO_FIXTURE_EXPANSION": True,
            "SCHEMA_PROMOTION_DECISION_11_NO_T6_LIVE_CASE_EXECUTION": True,
            "SCHEMA_PROMOTION_DECISION_12_NO_C8_AUTHORIZATION": True,
            "SCHEMA_PROMOTION_DECISION_13_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_summary": {
            "status": status,
            "human_decision_record_id": human_decision_record_id,
            "human_decision_packet_id": HUMAN_DECISION_PACKET_ID,
            "adoption_path_id": ADOPTION_PATH_ID,
            "capability_build_id": CAPABILITY_BUILD_ID,
            "proposal_id": PROPOSAL_ID,
            "required_capability": REQUIRED_CAPABILITY,
            "proposed_surface": PROPOSED_SURFACE,
            "human_adoption_decision_taken": True if gate == "PASS" else False,
            "selected_adoption_decision": SELECTED_DECISION if gate == "PASS" else None,
            "schema_promotion_decision_packet_prep_authorized": True if gate == "PASS" else False,
            "schema_archive_promotion_decision_packet_prep_target_ready": True if gate == "PASS" else False,
            "schema_archive_promotion_decision_packet_prep_target_id": schema_promotion_packet_prep_target_id if gate == "PASS" else None,
            "schema_archive_mutation_authorized": False,
            "schema_mutation_authorized": False,
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
            "decision_effect_applied": rel(DECISION_EFFECT_APPLIED_PATH),
            "authority_boundary_review": rel(AUTHORITY_BOUNDARY_REVIEW_PATH),
            "schema_archive_promotion_decision_packet_prep_target": rel(SCHEMA_PROMOTION_DECISION_PACKET_PREP_TARGET_PATH),
            "negative_control_result": rel(NEGATIVE_CONTROL_RESULT_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_receipt_id={receipt_id}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_receipt_path={rel(receipt_path)}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_record_id={human_decision_record_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_promotion_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
