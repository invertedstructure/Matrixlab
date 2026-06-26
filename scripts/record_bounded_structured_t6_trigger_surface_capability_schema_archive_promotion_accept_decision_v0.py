#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RECORD_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_ACCEPT_DECISION_V0"
TARGET_UNIT_ID = "bounded_structured_t6_trigger_surface_capability.schema_archive_promotion_accept_decision_v0"
NEXT_UNIT_ID = "PREPARE_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_MUTATION_TARGET_V0"

SELECTED_DECISION = "ACCEPT_SCHEMA_ARCHIVE_PROMOTION_FOR_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY"

PROMOTION_PACKET_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_receipt_9d350cee"
PROMOTION_DECISION_PACKET_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_ca415d65"
SOURCE_HUMAN_DECISION_RECORD_ID = "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_362616fe"
SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_receipt_4d152a3e"
ADOPTION_PATH_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_6f9974e5"
CAPABILITY_BUILD_ID = "bounded_structured_t6_trigger_surface_capability_build_721f09dc"
PROPOSAL_ID = "capability_proposal_57dda6e9"
REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"

PROMOTION_PACKET_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_receipt_9d350cee.json"
PROMOTION_REQUEST_PACKET_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_human_decision_request_packet_v0.json"
PROMOTION_DECISION_OPTIONS_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_options_v0.json"
PROMOTION_EFFECTS_MAP_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_effects_map_v0.json"
PROMOTION_AUTHORITY_BOUNDARY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_authority_boundary_v0.json"
PROMOTION_ACCEPT_OPTION_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_option_accept_v0.json"
PROMOTION_NEGATIVE_CONTROL_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_negative_control_v0.json"
PROMOTION_SCHEMA_CANDIDATE_BINDING_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_schema_candidate_binding_v0.json"
PROMOTION_SOURCE_CHAIN_BINDING_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_source_chain_binding_v0.json"

SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_schema_promotion_path_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_receipt_4d152a3e.json"
SCHEMA_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_schema_candidate_v0.json"
CAPABILITY_PROFILE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_profile_v0.json"
BUILD_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079.json"
BUILD_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_review_receipt_b8dba552.json"
PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"

OUT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_v0"
RECEIPT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_basis_v0.json"
DECISION_RECORD_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_human_decision_record_v0.json"
DECISION_EFFECT_APPLIED_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_effect_applied_v0.json"
AUTHORITY_BOUNDARY_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_authority_boundary_review_v0.json"
MUTATION_TARGET_PREP_TARGET_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_prep_target_v0.json"
NEGATIVE_CONTROL_RESULT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_negative_control_v0.json"
READOUT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_transition_trace.json"

FORBIDDEN_FALSE_KEYS = [
    "schema_archive_mutation_authorized",
    "schema_mutation_authorized",
    "runtime_adoption_authorized",
    "runtime_patch_authorized",
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
        PROMOTION_PACKET_RECEIPT_PATH,
        PROMOTION_REQUEST_PACKET_PATH,
        PROMOTION_DECISION_OPTIONS_PATH,
        PROMOTION_EFFECTS_MAP_PATH,
        PROMOTION_AUTHORITY_BOUNDARY_PATH,
        PROMOTION_ACCEPT_OPTION_PATH,
        PROMOTION_NEGATIVE_CONTROL_PATH,
        PROMOTION_SCHEMA_CANDIDATE_BINDING_PATH,
        PROMOTION_SOURCE_CHAIN_BINDING_PATH,
        SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_PATH,
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

    promotion_receipt = read_json(PROMOTION_PACKET_RECEIPT_PATH)
    request_packet = read_json(PROMOTION_REQUEST_PACKET_PATH)
    decision_options = read_json(PROMOTION_DECISION_OPTIONS_PATH)
    effects_map = read_json(PROMOTION_EFFECTS_MAP_PATH)
    authority_boundary = read_json(PROMOTION_AUTHORITY_BOUNDARY_PATH)
    accept_option = read_json(PROMOTION_ACCEPT_OPTION_PATH)
    negative_control = read_json(PROMOTION_NEGATIVE_CONTROL_PATH)
    schema_candidate_binding = read_json(PROMOTION_SCHEMA_CANDIDATE_BINDING_PATH)
    source_chain_binding = read_json(PROMOTION_SOURCE_CHAIN_BINDING_PATH)

    source_schema_promotion_decision_receipt = read_json(SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_PATH)
    schema_candidate = read_json(SCHEMA_CANDIDATE_PATH)
    capability_profile = read_json(CAPABILITY_PROFILE_PATH)
    build_receipt = read_json(BUILD_RECEIPT_PATH)
    build_review_receipt = read_json(BUILD_REVIEW_RECEIPT_PATH)
    proposal = read_json(PROPOSAL_PATH)

    promotion_summary = promotion_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_summary", {})
    source_schema_promotion_summary = source_schema_promotion_decision_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_summary", {})
    build_summary = build_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_summary", {})
    build_review_summary = build_review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_review_summary", {})

    if promotion_receipt.get("receipt_id") != PROMOTION_PACKET_RECEIPT_ID:
        failures.append(f"promotion_receipt_id_wrong:{promotion_receipt.get('receipt_id')}")
    if promotion_receipt.get("gate") != "PASS":
        failures.append("promotion_receipt_gate_not_pass")
    if promotion_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append("promotion_terminal_not_stop")
    if promotion_receipt.get("terminal", {}).get("stop_code") != "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_HUMAN_DECISION_REQUIRED":
        failures.append(f"promotion_stop_code_wrong:{promotion_receipt.get('terminal', {}).get('stop_code')}")

    for key in [
        "schema_archive_promotion_decision_packet_ready",
        "human_schema_promotion_decision_required",
    ]:
        if promotion_summary.get(key) is not True:
            failures.append(f"promotion_summary_{key}_not_true:{promotion_summary.get(key)}")

    if promotion_summary.get("human_schema_promotion_decision_taken") is not False:
        failures.append("promotion_summary_decision_already_taken")
    if promotion_summary.get("selected_schema_promotion_decision") is not None:
        failures.append(f"promotion_summary_selected_decision_not_none:{promotion_summary.get('selected_schema_promotion_decision')}")
    if SELECTED_DECISION not in (promotion_summary.get("available_decisions") or []):
        failures.append(f"selected_decision_not_available:{SELECTED_DECISION}")

    for key in FORBIDDEN_FALSE_KEYS:
        require_false(promotion_summary, key, failures, "promotion_summary")

    if request_packet.get("packet_status") != "READY_FOR_HUMAN_DECISION":
        failures.append(f"request_packet_status_wrong:{request_packet.get('packet_status')}")
    if request_packet.get("human_schema_promotion_decision_taken") is not False:
        failures.append("request_packet_decision_already_taken")
    if request_packet.get("selected_schema_promotion_decision") is not None:
        failures.append("request_packet_selected_decision_not_none")
    if SELECTED_DECISION not in (request_packet.get("available_decisions") or []):
        failures.append("request_packet_selected_decision_missing")

    if decision_options.get("options_status") != "READY_FOR_HUMAN_DECISION":
        failures.append(f"decision_options_status_wrong:{decision_options.get('options_status')}")
    if decision_options.get("selected_schema_promotion_decision") is not None:
        failures.append("decision_options_selected_not_none")
    option_names = [x.get("decision") for x in (decision_options.get("decision_options") or []) if isinstance(x, dict)]
    if SELECTED_DECISION not in option_names:
        failures.append("decision_options_selected_missing")

    selected_effect = (effects_map.get("decision_effects") or {}).get(SELECTED_DECISION)
    if not selected_effect:
        failures.append("selected_effect_missing")
    else:
        if selected_effect.get("schema_archive_mutation_authorized_by_packet") is not False:
            failures.append("selected_effect_mutation_authorized_by_packet_unexpected")
        if selected_effect.get("requires_later_recorded_human_decision") is not True:
            failures.append("selected_effect_later_recorded_human_decision_not_required")

    if accept_option.get("option") != SELECTED_DECISION:
        failures.append(f"accept_option_wrong:{accept_option.get('option')}")
    if accept_option.get("option_status") != "AVAILABLE_NOT_SELECTED":
        failures.append(f"accept_option_status_wrong:{accept_option.get('option_status')}")
    if accept_option.get("selected") is not False:
        failures.append("accept_option_already_selected")
    if accept_option.get("schema_archive_mutation_authorized_now") is not False:
        failures.append("accept_option_mutation_authorized_now_unexpected")

    if authority_boundary.get("human_schema_promotion_decision_required") is not True:
        failures.append("authority_boundary_decision_required_not_true")
    if authority_boundary.get("human_schema_promotion_decision_taken") is not False:
        failures.append("authority_boundary_decision_taken_not_false")
    for key in FORBIDDEN_FALSE_KEYS:
        require_false(authority_boundary, key, failures, "authority_boundary")

    if negative_control.get("negative_control_status") != "PASS":
        failures.append(f"negative_control_status_wrong:{negative_control.get('negative_control_status')}")
    zero = negative_control.get("zero_counters_for_this_unit") or {}
    for key in [
        "schema_archive_mutation_count",
        "schema_mutation_count",
        "runtime_adoption_count",
        "runtime_patch_count",
        "move_addition_count",
        "fixture_expansion_count",
        "t6_live_case_execution_count",
        "hidden_next_command_count",
        "c8_authorization_count",
    ]:
        if zero.get(key) != 0:
            failures.append(f"negative_counter_wrong:{key}:{zero.get(key)}")

    if schema_candidate_binding.get("schema_candidate_status") != "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION":
        failures.append("schema_candidate_binding_status_wrong")
    if schema_candidate_binding.get("schema_archive_mutation_authorized") is not False:
        failures.append("schema_candidate_binding_archive_mutation_unexpected")
    if source_chain_binding.get("binding_status") != "PASS":
        failures.append("source_chain_binding_not_pass")

    if source_schema_promotion_summary.get("schema_promotion_decision_packet_prep_authorized") is not True:
        failures.append("source_schema_promotion_packet_prep_not_authorized")
    if source_schema_promotion_summary.get("selected_adoption_decision") != "PREPARE_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET":
        failures.append("source_adoption_decision_wrong")

    if schema_candidate.get("schema_candidate_status") != "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION":
        failures.append(f"schema_candidate_status_wrong:{schema_candidate.get('schema_candidate_status')}")
    if schema_candidate.get("schema_name") != PROPOSED_SURFACE:
        failures.append(f"schema_candidate_name_wrong:{schema_candidate.get('schema_name')}")
    if schema_candidate.get("archive_mutation_authorized") is not False:
        failures.append("schema_candidate_archive_mutation_authorized_unexpected")
    if schema_candidate.get("runtime_adoption_authorized") is not False:
        failures.append("schema_candidate_runtime_adoption_authorized_unexpected")
    if capability_profile.get("capability_name") != REQUIRED_CAPABILITY:
        failures.append("capability_profile_name_wrong")
    if capability_profile.get("surface_name") != PROPOSED_SURFACE:
        failures.append("capability_profile_surface_wrong")
    if build_summary.get("build_executed") is not True:
        failures.append("build_not_executed")
    if build_review_summary.get("artifact_review_pass") is not True:
        failures.append("build_review_not_pass")
    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_ACCEPT_DECISION_RECORDED_MUTATION_TARGET_PREP_READY"
        if gate == "PASS"
        else "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_ACCEPT_DECISION_GATE_FAIL"
    )

    accept_decision_record_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_" + sig8({
        "promotion_decision_packet_id": PROMOTION_DECISION_PACKET_ID,
        "selected_decision": SELECTED_DECISION,
        "schema_candidate": PROPOSED_SURFACE,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
    })

    mutation_target_prep_target_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_prep_" + sig8({
        "accept_decision_record_id": accept_decision_record_id,
        "schema_candidate": PROPOSED_SURFACE,
        "source_schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_basis_v0",
        "unit_id": UNIT_ID,
        "accept_decision_record_id": accept_decision_record_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_promotion_decision_packet_receipt_id": PROMOTION_PACKET_RECEIPT_ID,
        "source_promotion_decision_packet_id": PROMOTION_DECISION_PACKET_ID,
        "selected_schema_promotion_decision": SELECTED_DECISION if gate == "PASS" else None,
        "source_schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "record_claim": "Record human acceptance of schema archive promotion and authorize only mutation-target preparation. Do not mutate schema archive.",
        "source_file_hashes": source_hashes,
    }

    decision_record = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_human_decision_record_v0",
        "decision_record_status": "HUMAN_SCHEMA_PROMOTION_DECISION_RECORDED" if gate == "PASS" else "BLOCKED",
        "accept_decision_record_id": accept_decision_record_id,
        "promotion_decision_packet_id": PROMOTION_DECISION_PACKET_ID,
        "source_human_decision_record_id": SOURCE_HUMAN_DECISION_RECORD_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "selected_schema_promotion_decision": SELECTED_DECISION if gate == "PASS" else None,
        "human_schema_promotion_decision_taken": True if gate == "PASS" else False,
        "decision_effect": "AUTHORIZE_SCHEMA_ARCHIVE_MUTATION_TARGET_PREP_ONLY" if gate == "PASS" else "NONE",
        "decision_does_not_mutate_schema_archive": True,
        "decision_does_not_authorize_schema_archive_mutation_execution": True,
        "decision_does_not_authorize_runtime_adoption": True,
        "decision_does_not_authorize_move_addition": True,
        "decision_does_not_authorize_fixture_expansion": True,
        "decision_does_not_authorize_t6_live_case_execution": True,
        "decision_does_not_authorize_c8": True,
    }

    decision_effect_applied = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_effect_applied_v0",
        "accept_decision_record_id": accept_decision_record_id,
        "effect_status": "APPLIED_TO_MUTATION_TARGET_PREP_TARGET_ONLY" if gate == "PASS" else "BLOCKED",
        "selected_schema_promotion_decision": SELECTED_DECISION if gate == "PASS" else None,
        "schema_archive_mutation_target_prep_authorized": True if gate == "PASS" else False,
        "schema_archive_mutation_target_prep_target_id": mutation_target_prep_target_id if gate == "PASS" else None,
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_authority_boundary_review_v0",
        "accept_decision_record_id": accept_decision_record_id,
        "review_status": "PASS" if gate == "PASS" else "BLOCKED",
        "allowed_effect": "prepare schema archive mutation target",
        "not_allowed_effects": [
            "schema archive mutation execution",
            "schema archive write",
            "schema mutation",
            "runtime adoption",
            "runtime patch",
            "move addition",
            "fixture expansion",
            "T6 live case execution",
            "C8 authorization",
        ],
        "schema_archive_mutation_target_prep_authorized": True if gate == "PASS" else False,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "c8_authorized": False,
    }

    mutation_target_prep_target = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_prep_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "schema_archive_mutation_target_prep_target_id": mutation_target_prep_target_id if gate == "PASS" else None,
        "accept_decision_record_id": accept_decision_record_id,
        "promotion_decision_packet_id": PROMOTION_DECISION_PACKET_ID,
        "selected_schema_promotion_decision": SELECTED_DECISION if gate == "PASS" else None,
        "schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "schema_candidate_status": schema_candidate.get("schema_candidate_status"),
        "schema_name": schema_candidate.get("schema_name"),
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "target_scope": "Prepare a bounded schema archive mutation target for later review/authorization. Do not mutate schema archive in the prep unit.",
        "schema_archive_mutation_target_prep_authorized": True if gate == "PASS" else False,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "requires_later_review_before_mutation": True,
        "requires_later_human_decision_before_schema_archive_write": True,
        "does_not_authorize_runtime_adoption": True,
        "does_not_authorize_move_addition": True,
        "does_not_authorize_fixture_expansion": True,
        "does_not_authorize_t6_live_case_execution": True,
        "does_not_authorize_c8": True,
    }

    negative_control_result = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_negative_control_v0",
        "accept_decision_record_id": accept_decision_record_id,
        "negative_control_status": "PASS" if gate == "PASS" else "BLOCKED",
        "selected_schema_promotion_decision": SELECTED_DECISION if gate == "PASS" else None,
        "schema_archive_mutation_target_prep_authorized": True if gate == "PASS" else False,
        "schema_archive_mutation_count": 0,
        "schema_mutation_count": 0,
        "runtime_adoption_count": 0,
        "runtime_patch_count": 0,
        "move_addition_count": 0,
        "fixture_expansion_count": 0,
        "t6_live_case_execution_count": 0,
        "hidden_next_command_count": 0,
        "c8_authorization_count": 0,
        "negative_control_rule": "Accepting schema promotion authorizes only mutation-target prep, not schema archive mutation.",
    }

    rollup = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "accept_decision_record_id": accept_decision_record_id,
        "promotion_decision_packet_id": PROMOTION_DECISION_PACKET_ID,
        "selected_schema_promotion_decision": SELECTED_DECISION if gate == "PASS" else None,
        "human_schema_promotion_decision_taken": True if gate == "PASS" else False,
        "schema_archive_mutation_target_prep_authorized": True if gate == "PASS" else False,
        "schema_archive_mutation_target_prep_target_ready": True if gate == "PASS" else False,
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_readout_v0",
        "status": status,
        "accept_decision_record_id": accept_decision_record_id,
        "selected_schema_promotion_decision": SELECTED_DECISION if gate == "PASS" else None,
        "interpretation": "Human accepted schema archive promotion path. Only schema archive mutation target prep is authorized; schema archive has not been mutated."
        if gate == "PASS" else "Schema archive promotion accept decision recording failed typed gates.",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_profile_v0",
        "profile_status": status,
        "accept_decision_record_id": accept_decision_record_id,
        "core_rule": "Human acceptance authorizes mutation-target preparation only. Actual schema archive mutation remains separate, reviewed, and not yet authorized.",
        "mutation_target_prep_target_ref": rel(MUTATION_TARGET_PREP_TARGET_PATH),
        "must_not_infer": [
            "schema archive mutated",
            "schema promoted",
            "schema mutation executed",
            "runtime adopted",
            "runtime patched",
            "move registry updated",
            "fixture suite expanded",
            "T6 live case executed",
            "C8 authorized",
        ],
    }

    report = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "decision_result": "SCHEMA_ARCHIVE_MUTATION_TARGET_PREP_READY" if gate == "PASS" else "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_DECISION_GATE_FAIL",
            "accept_decision_record_id": accept_decision_record_id,
            "promotion_decision_packet_id": PROMOTION_DECISION_PACKET_ID,
            "selected_schema_promotion_decision": SELECTED_DECISION if gate == "PASS" else None,
            "schema_archive_mutation_target_prep_authorized": True if gate == "PASS" else False,
            "schema_archive_mutation_target_prep_target_ready": True if gate == "PASS" else False,
            "schema_archive_mutation_authorized": False,
            "schema_mutation_authorized": False,
            "runtime_adoption_authorized": False,
            "runtime_patch_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "t6_live_case_execution_authorized": False,
            "c8_authorized": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_transition_trace_v0",
        "unit_id": UNIT_ID,
        "accept_decision_record_id": accept_decision_record_id,
        "transitions": [
            {
                "from": "STOP_SCHEMA_ARCHIVE_PROMOTION_HUMAN_DECISION_REQUIRED",
                "edge": "record human acceptance of schema archive promotion",
                "to": "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_DECISION_RECORDED" if gate == "PASS" else "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_DECISION_GATE_FAIL",
            },
            {
                "from": "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_DECISION_RECORDED" if gate == "PASS" else "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_DECISION_GATE_FAIL",
                "edge": "emit schema archive mutation target prep target without mutation",
                "to": "SCHEMA_ARCHIVE_MUTATION_TARGET_PREP_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_ACCEPT_DECISION_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (DECISION_RECORD_PATH, decision_record),
        (DECISION_EFFECT_APPLIED_PATH, decision_effect_applied),
        (AUTHORITY_BOUNDARY_REVIEW_PATH, authority_boundary_review),
        (MUTATION_TARGET_PREP_TARGET_PATH, mutation_target_prep_target),
        (NEGATIVE_CONTROL_RESULT_PATH, negative_control_result),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_RECEIPT_CONSUMED",
        "HUMAN_SELECTED_ACCEPT_SCHEMA_ARCHIVE_PROMOTION",
        "ACCEPT_OPTION_AVAILABLE",
        "HUMAN_SCHEMA_PROMOTION_DECISION_RECORDED",
        "SCHEMA_ARCHIVE_MUTATION_TARGET_PREP_TARGET_EMITTED",
        "NO_SCHEMA_ARCHIVE_MUTATION",
        "NO_SCHEMA_MUTATION_EXECUTION",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_RUNTIME_PATCH",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION",
        "NO_T6_LIVE_CASE_EXECUTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_ACCEPT_DECISION_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "accept_decision_record_id": accept_decision_record_id,
        "promotion_decision_packet_id": PROMOTION_DECISION_PACKET_ID,
        "source_promotion_decision_packet_receipt_id": PROMOTION_PACKET_RECEIPT_ID,
        "source_promotion_decision_packet_receipt_ref": rel(PROMOTION_PACKET_RECEIPT_PATH),
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_0_PACKET_RECEIPT_CONSUMED": gate == "PASS",
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_1_SELECTED_DECISION_AVAILABLE": SELECTED_DECISION in (promotion_summary.get("available_decisions") or []),
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_2_ACCEPT_OPTION_AVAILABLE_NOT_SELECTED": accept_option.get("option_status") == "AVAILABLE_NOT_SELECTED",
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_3_HUMAN_DECISION_RECORDED": gate == "PASS",
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_4_MUTATION_TARGET_PREP_TARGET_EMITTED": MUTATION_TARGET_PREP_TARGET_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_5_NO_SCHEMA_ARCHIVE_MUTATION": True,
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_6_NO_SCHEMA_MUTATION": True,
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_7_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_8_NO_RUNTIME_PATCH": True,
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_9_NO_MOVE_ADDITION": True,
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_10_NO_FIXTURE_EXPANSION": True,
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_11_NO_T6_LIVE_CASE_EXECUTION": True,
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_12_NO_C8_AUTHORIZATION": True,
            "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_13_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_summary": {
            "status": status,
            "accept_decision_record_id": accept_decision_record_id,
            "promotion_decision_packet_id": PROMOTION_DECISION_PACKET_ID,
            "source_promotion_decision_packet_receipt_id": PROMOTION_PACKET_RECEIPT_ID,
            "selected_schema_promotion_decision": SELECTED_DECISION if gate == "PASS" else None,
            "human_schema_promotion_decision_taken": True if gate == "PASS" else False,
            "schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
            "schema_candidate_status": schema_candidate.get("schema_candidate_status"),
            "schema_name": schema_candidate.get("schema_name"),
            "adoption_path_id": ADOPTION_PATH_ID,
            "capability_build_id": CAPABILITY_BUILD_ID,
            "proposal_id": PROPOSAL_ID,
            "schema_archive_mutation_target_prep_authorized": True if gate == "PASS" else False,
            "schema_archive_mutation_target_prep_target_ready": True if gate == "PASS" else False,
            "schema_archive_mutation_target_prep_target_id": mutation_target_prep_target_id if gate == "PASS" else None,
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
            "mutation_target_prep_target": rel(MUTATION_TARGET_PREP_TARGET_PATH),
            "negative_control_result": rel(NEGATIVE_CONTROL_RESULT_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_receipt_id={receipt_id}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_receipt_path={rel(receipt_path)}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_record_id={accept_decision_record_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
