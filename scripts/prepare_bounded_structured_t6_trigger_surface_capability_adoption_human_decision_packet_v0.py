#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_HUMAN_DECISION_PACKET_V0"
TARGET_UNIT_ID = "bounded_structured_t6_trigger_surface_capability.adoption_human_decision_packet_v0"

ADOPTION_PATH_REVIEW_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_review_receipt_ec071b02"
ADOPTION_REVIEW_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_review_9d2fb29e"
ADOPTION_PATH_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_6f9974e5"
CAPABILITY_BUILD_ID = "bounded_structured_t6_trigger_surface_capability_build_721f09dc"
PROPOSAL_ID = "capability_proposal_57dda6e9"
REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"
HUMAN_DECISION_PACKET_PREP_TARGET_ID = "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_prep_da562c2c"

ADOPTION_PATH_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_adoption_path_review_receipt_ec071b02.json"
HUMAN_DECISION_PACKET_PREP_TARGET_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_prep_target_v0.json"
SOURCE_BINDING_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0/bounded_structured_t6_trigger_surface_capability_adoption_source_binding_review_v0.json"
ADOPTION_SCOPE_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0/bounded_structured_t6_trigger_surface_capability_adoption_scope_review_v0.json"
SURFACE_INVENTORY_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0/bounded_structured_t6_trigger_surface_capability_adoption_surface_inventory_review_v0.json"
AUTHORITY_BOUNDARY_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0/bounded_structured_t6_trigger_surface_capability_adoption_authority_boundary_review_v0.json"
DECISION_SURFACE_MAP_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0/bounded_structured_t6_trigger_surface_capability_adoption_decision_surface_map_review_v0.json"
CANDIDATE_SURFACES_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0/bounded_structured_t6_trigger_surface_capability_adoption_candidate_surfaces_review_v0.json"
C8_BOUNDARY_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0/bounded_structured_t6_trigger_surface_capability_adoption_c8_boundary_review_v0.json"
ADOPTION_NEGATIVE_CONTROL_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0/bounded_structured_t6_trigger_surface_capability_adoption_negative_control_review_v0.json"

ADOPTION_PATH_PREP_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0_receipts/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_receipt_34a6f83a.json"
RUNTIME_ADOPTION_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_runtime_adoption_candidate_v0.json"
SCHEMA_PROMOTION_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_candidate_v0.json"
MOVE_REGISTRY_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_move_registry_candidate_v0.json"
FIXTURE_EXPANSION_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_fixture_expansion_candidate_v0.json"
T6_LIVE_CASE_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_t6_live_case_candidate_v0.json"
C8_BOUNDARY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_c8_boundary_v0.json"

BUILD_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_review_receipt_b8dba552.json"
BUILD_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079.json"
CAPABILITY_PROFILE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_profile_v0.json"
SCHEMA_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_schema_candidate_v0.json"
PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"

OUT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_v0"
RECEIPT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_basis_v0.json"
SOURCE_REVIEW_BINDING_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_source_review_binding_v0.json"
DECISION_OPTIONS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_options_v0.json"
DECISION_EFFECTS_MAP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_effects_map_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_authority_boundary_v0.json"
RUNTIME_ADOPTION_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_option_runtime_adoption_v0.json"
SCHEMA_PROMOTION_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_option_schema_archive_promotion_v0.json"
MOVE_REGISTRY_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_option_move_registry_addition_v0.json"
FIXTURE_EXPANSION_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_option_fixture_test_expansion_v0.json"
T6_LIVE_CASE_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_option_t6_live_case_execution_v0.json"
DEFER_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_option_defer_v0.json"
FREEZE_REFERENCE_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_option_freeze_reference_only_v0.json"
CLOSE_NO_ADOPTION_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_option_close_no_adoption_v0.json"
HUMAN_DECISION_REQUEST_PACKET_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_request_packet_v0.json"
NEGATIVE_CONTROL_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_negative_control_v0.json"
READOUT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_transition_trace.json"

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

DECISION_OPTIONS = [
    "PREPARE_RUNTIME_ADOPTION_DECISION_PACKET",
    "PREPARE_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET",
    "PREPARE_MOVE_REGISTRY_ADDITION_DECISION_PACKET",
    "PREPARE_FIXTURE_TEST_EXPANSION_DECISION_PACKET",
    "PREPARE_T6_LIVE_CASE_EXECUTION_DECISION_PACKET",
    "DEFER_ADOPTION_PATH",
    "FREEZE_CAPABILITY_AS_REFERENCE_ONLY",
    "CLOSE_ADOPTION_PATH_NO_ADOPTION",
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

def lower_list(xs: Any) -> List[str]:
    return [str(x).lower() for x in (xs or [])]

def require_false(obj: Dict[str, Any], key: str, failures: List[str], prefix: str) -> None:
    if obj.get(key) is not False:
        failures.append(f"{prefix}_{key}_not_false:{obj.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        ADOPTION_PATH_REVIEW_RECEIPT_PATH,
        HUMAN_DECISION_PACKET_PREP_TARGET_PATH,
        SOURCE_BINDING_REVIEW_PATH,
        ADOPTION_SCOPE_REVIEW_PATH,
        SURFACE_INVENTORY_REVIEW_PATH,
        AUTHORITY_BOUNDARY_REVIEW_PATH,
        DECISION_SURFACE_MAP_REVIEW_PATH,
        CANDIDATE_SURFACES_REVIEW_PATH,
        C8_BOUNDARY_REVIEW_PATH,
        ADOPTION_NEGATIVE_CONTROL_REVIEW_PATH,
        ADOPTION_PATH_PREP_RECEIPT_PATH,
        RUNTIME_ADOPTION_CANDIDATE_PATH,
        SCHEMA_PROMOTION_CANDIDATE_PATH,
        MOVE_REGISTRY_CANDIDATE_PATH,
        FIXTURE_EXPANSION_CANDIDATE_PATH,
        T6_LIVE_CASE_CANDIDATE_PATH,
        C8_BOUNDARY_PATH,
        BUILD_REVIEW_RECEIPT_PATH,
        BUILD_RECEIPT_PATH,
        CAPABILITY_PROFILE_PATH,
        SCHEMA_CANDIDATE_PATH,
        PROPOSAL_PATH,
    ]

    failures: List[str] = []

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    review_receipt = read_json(ADOPTION_PATH_REVIEW_RECEIPT_PATH)
    prep_target = read_json(HUMAN_DECISION_PACKET_PREP_TARGET_PATH)
    source_binding_review = read_json(SOURCE_BINDING_REVIEW_PATH)
    scope_review = read_json(ADOPTION_SCOPE_REVIEW_PATH)
    surface_inventory_review = read_json(SURFACE_INVENTORY_REVIEW_PATH)
    authority_boundary_review = read_json(AUTHORITY_BOUNDARY_REVIEW_PATH)
    decision_surface_map_review = read_json(DECISION_SURFACE_MAP_REVIEW_PATH)
    candidate_surfaces_review = read_json(CANDIDATE_SURFACES_REVIEW_PATH)
    c8_boundary_review = read_json(C8_BOUNDARY_REVIEW_PATH)
    negative_control_review = read_json(ADOPTION_NEGATIVE_CONTROL_REVIEW_PATH)

    adoption_path_prep_receipt = read_json(ADOPTION_PATH_PREP_RECEIPT_PATH)
    runtime_adoption_candidate = read_json(RUNTIME_ADOPTION_CANDIDATE_PATH)
    schema_promotion_candidate = read_json(SCHEMA_PROMOTION_CANDIDATE_PATH)
    move_registry_candidate = read_json(MOVE_REGISTRY_CANDIDATE_PATH)
    fixture_expansion_candidate = read_json(FIXTURE_EXPANSION_CANDIDATE_PATH)
    t6_live_case_candidate = read_json(T6_LIVE_CASE_CANDIDATE_PATH)
    c8_boundary = read_json(C8_BOUNDARY_PATH)

    build_review_receipt = read_json(BUILD_REVIEW_RECEIPT_PATH)
    build_receipt = read_json(BUILD_RECEIPT_PATH)
    capability_profile = read_json(CAPABILITY_PROFILE_PATH)
    schema_candidate = read_json(SCHEMA_CANDIDATE_PATH)
    proposal = read_json(PROPOSAL_PATH)

    review_summary = review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_adoption_path_review_summary", {})
    prep_summary = adoption_path_prep_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_adoption_path_prep_summary", {})
    build_review_summary = build_review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_review_summary", {})
    build_summary = build_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_summary", {})

    if review_receipt.get("receipt_id") != ADOPTION_PATH_REVIEW_RECEIPT_ID:
        failures.append(f"review_receipt_id_wrong:{review_receipt.get('receipt_id')}")
    if review_receipt.get("gate") != "PASS":
        failures.append("review_receipt_gate_not_pass")
    if review_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"review_terminal_next_wrong:{review_receipt.get('terminal', {}).get('next_unit_id')}")

    for key in [
        "source_adoption_path_prepared",
        "source_binding_review_pass",
        "scope_review_pass",
        "surface_inventory_review_pass",
        "authority_boundary_review_pass",
        "decision_surface_map_review_pass",
        "candidate_surfaces_review_pass",
        "c8_boundary_review_pass",
        "negative_control_review_pass",
        "human_decision_packet_draft_review_pass",
        "adoption_path_review_pass",
        "human_decision_packet_prep_target_ready",
        "future_surfaces_require_separate_human_decision",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_summary_{key}_not_true:{review_summary.get(key)}")

    if review_summary.get("human_decision_packet_prep_target_id") != HUMAN_DECISION_PACKET_PREP_TARGET_ID:
        failures.append(f"human_decision_packet_prep_target_id_wrong:{review_summary.get('human_decision_packet_prep_target_id')}")
    if review_summary.get("human_adoption_decision_taken") is not False:
        failures.append("human_adoption_decision_already_taken")
    if review_summary.get("selected_adoption_decision") is not None:
        failures.append(f"selected_adoption_decision_not_none:{review_summary.get('selected_adoption_decision')}")

    for key in FORBIDDEN_AUTHORITY_KEYS:
        require_false(review_summary, key, failures, "review_summary")

    if prep_target.get("target_status") != "READY":
        failures.append(f"prep_target_status_wrong:{prep_target.get('target_status')}")
    if prep_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"prep_target_next_wrong:{prep_target.get('next_unit_id')}")
    if prep_target.get("human_decision_packet_prep_target_id") != HUMAN_DECISION_PACKET_PREP_TARGET_ID:
        failures.append("prep_target_id_wrong")
    if prep_target.get("human_decision_required") is not True:
        failures.append("prep_target_human_decision_required_not_true")
    if prep_target.get("human_decision_taken") is not False:
        failures.append("prep_target_human_decision_taken_not_false")
    if prep_target.get("selected_adoption_decision") is not None:
        failures.append("prep_target_selected_decision_not_none")

    must_false = prep_target.get("must_remain_false_until_human_decision") or []
    for key in FORBIDDEN_AUTHORITY_KEYS:
        if key not in must_false:
            failures.append(f"prep_target_must_remain_false_missing:{key}")

    if source_binding_review.get("review_status") != "PASS":
        failures.append("source_binding_review_not_pass")
    if scope_review.get("review_status") != "PASS":
        failures.append("scope_review_not_pass")
    if surface_inventory_review.get("review_status") != "PASS":
        failures.append("surface_inventory_review_not_pass")
    if authority_boundary_review.get("review_status") != "PASS":
        failures.append("authority_boundary_review_not_pass")
    if decision_surface_map_review.get("review_status") != "PASS":
        failures.append("decision_surface_map_review_not_pass")
    if candidate_surfaces_review.get("review_status") != "PASS":
        failures.append("candidate_surfaces_review_not_pass")
    if c8_boundary_review.get("review_status") != "PASS":
        failures.append("c8_boundary_review_not_pass")
    if negative_control_review.get("review_status") != "PASS":
        failures.append("negative_control_review_not_pass")

    for name, candidate, false_keys in [
        ("runtime_adoption", runtime_adoption_candidate, ["runtime_adoption_authorized", "runtime_patch_authorized"]),
        ("schema_promotion", schema_promotion_candidate, ["schema_archive_mutation_authorized", "schema_mutation_authorized"]),
        ("move_registry", move_registry_candidate, ["move_addition_authorized"]),
        ("fixture_expansion", fixture_expansion_candidate, ["fixture_expansion_authorized"]),
        ("t6_live_case", t6_live_case_candidate, ["t6_live_case_execution_authorized"]),
    ]:
        if candidate.get("candidate_status") != "CANDIDATE_ONLY_NOT_AUTHORIZED":
            failures.append(f"{name}_candidate_status_wrong:{candidate.get('candidate_status')}")
        for key in false_keys:
            if candidate.get(key) is not False:
                failures.append(f"{name}_{key}_not_false:{candidate.get(key)}")

    if c8_boundary.get("c8_authorized") is not False:
        failures.append("source_c8_authorized_not_false")
    if c8_boundary.get("c8_discussion_authorized") is not False:
        failures.append("source_c8_discussion_authorized_not_false")

    if prep_summary.get("adoption_path_prepared") is not True:
        failures.append("source_adoption_path_not_prepared")
    if build_review_summary.get("artifact_review_pass") is not True:
        failures.append("source_build_review_not_pass")
    if build_summary.get("build_executed") is not True:
        failures.append("source_build_not_executed")
    if capability_profile.get("capability_name") != REQUIRED_CAPABILITY:
        failures.append("capability_profile_name_wrong")
    if schema_candidate.get("schema_candidate_status") != "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION":
        failures.append("schema_candidate_status_wrong")
    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_HUMAN_DECISION_PACKET_PASS_DECISION_REQUIRED"
        if gate == "PASS"
        else "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_HUMAN_DECISION_PACKET_GATE_FAIL"
    )

    human_decision_packet_id = "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_" + sig8({
        "adoption_review_id": ADOPTION_REVIEW_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "decision_options": DECISION_OPTIONS,
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_basis_v0",
        "unit_id": UNIT_ID,
        "human_decision_packet_id": human_decision_packet_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_adoption_path_review_receipt_id": ADOPTION_PATH_REVIEW_RECEIPT_ID,
        "source_human_decision_packet_prep_target_id": HUMAN_DECISION_PACKET_PREP_TARGET_ID,
        "source_adoption_review_id": ADOPTION_REVIEW_ID,
        "source_adoption_path_id": ADOPTION_PATH_ID,
        "source_capability_build_id": CAPABILITY_BUILD_ID,
        "source_proposal_id": PROPOSAL_ID,
        "prep_claim": "Prepare a human decision packet only. Do not select a decision and do not grant runtime/schema/move/fixture/T6/C8 authority.",
        "source_file_hashes": source_hashes,
    }

    source_review_binding = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_source_review_binding_v0",
        "human_decision_packet_id": human_decision_packet_id,
        "binding_status": "PASS" if gate == "PASS" else "FAIL",
        "adoption_review_id": ADOPTION_REVIEW_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "adoption_path_review_receipt_id": ADOPTION_PATH_REVIEW_RECEIPT_ID,
        "human_decision_packet_prep_target_id": HUMAN_DECISION_PACKET_PREP_TARGET_ID,
        "all_review_gates_passed": True if gate == "PASS" else False,
    }

    decision_options = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_options_v0",
        "human_decision_packet_id": human_decision_packet_id,
        "options_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "selected_adoption_decision": None,
        "decision_options": [
            {
                "decision": "PREPARE_RUNTIME_ADOPTION_DECISION_PACKET",
                "meaning": "Open a later explicit runtime-adoption decision path.",
                "does_not_execute_surface_now": True,
                "authority_granted_by_this_packet": "none until human selects this option in a separate decision record",
            },
            {
                "decision": "PREPARE_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET",
                "meaning": "Open a later explicit schema archive promotion decision path.",
                "does_not_execute_surface_now": True,
                "authority_granted_by_this_packet": "none until human selects this option in a separate decision record",
            },
            {
                "decision": "PREPARE_MOVE_REGISTRY_ADDITION_DECISION_PACKET",
                "meaning": "Open a later explicit move registry addition decision path.",
                "does_not_execute_surface_now": True,
                "authority_granted_by_this_packet": "none until human selects this option in a separate decision record",
            },
            {
                "decision": "PREPARE_FIXTURE_TEST_EXPANSION_DECISION_PACKET",
                "meaning": "Open a later explicit fixture/test expansion decision path.",
                "does_not_execute_surface_now": True,
                "authority_granted_by_this_packet": "none until human selects this option in a separate decision record",
            },
            {
                "decision": "PREPARE_T6_LIVE_CASE_EXECUTION_DECISION_PACKET",
                "meaning": "Open a later explicit T6 live-case execution decision path.",
                "does_not_execute_surface_now": True,
                "authority_granted_by_this_packet": "none until human selects this option in a separate decision record",
            },
            {
                "decision": "DEFER_ADOPTION_PATH",
                "meaning": "Leave the adoption path open but do not proceed.",
                "does_not_execute_surface_now": True,
                "authority_granted_by_this_packet": "none until human selects this option in a separate decision record",
            },
            {
                "decision": "FREEZE_CAPABILITY_AS_REFERENCE_ONLY",
                "meaning": "Keep the built capability as reference-only artifacts.",
                "does_not_execute_surface_now": True,
                "authority_granted_by_this_packet": "none until human selects this option in a separate decision record",
            },
            {
                "decision": "CLOSE_ADOPTION_PATH_NO_ADOPTION",
                "meaning": "Close this adoption path without adoption or promotion.",
                "does_not_execute_surface_now": True,
                "authority_granted_by_this_packet": "none until human selects this option in a separate decision record",
            },
        ],
    }

    decision_effects_map = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_effects_map_v0",
        "human_decision_packet_id": human_decision_packet_id,
        "effects_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "effect_rule": "A selected option may authorize only the next bounded decision-path preparation/recording unit named by that option. It does not execute runtime adoption, schema mutation, move addition, fixture expansion, T6 live case, or C8.",
        "decision_effects": {
            "PREPARE_RUNTIME_ADOPTION_DECISION_PACKET": {
                "next_surface": "runtime adoption decision path",
                "runtime_adoption_authorized": False,
                "runtime_patch_authorized": False,
            },
            "PREPARE_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET": {
                "next_surface": "schema archive promotion decision path",
                "schema_archive_mutation_authorized": False,
                "schema_mutation_authorized": False,
            },
            "PREPARE_MOVE_REGISTRY_ADDITION_DECISION_PACKET": {
                "next_surface": "move registry addition decision path",
                "move_addition_authorized": False,
            },
            "PREPARE_FIXTURE_TEST_EXPANSION_DECISION_PACKET": {
                "next_surface": "fixture/test expansion decision path",
                "fixture_expansion_authorized": False,
            },
            "PREPARE_T6_LIVE_CASE_EXECUTION_DECISION_PACKET": {
                "next_surface": "T6 live-case execution decision path",
                "t6_live_case_execution_authorized": False,
            },
            "DEFER_ADOPTION_PATH": {
                "next_surface": "defer/hold",
                "all_adoption_authorities": False,
            },
            "FREEZE_CAPABILITY_AS_REFERENCE_ONLY": {
                "next_surface": "reference-only freeze",
                "all_adoption_authorities": False,
            },
            "CLOSE_ADOPTION_PATH_NO_ADOPTION": {
                "next_surface": "close no-adoption",
                "all_adoption_authorities": False,
            },
        },
    }

    authority_boundary = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_authority_boundary_v0",
        "human_decision_packet_id": human_decision_packet_id,
        "boundary_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "human_decision_required": True if gate == "PASS" else False,
        "human_decision_taken": False,
        "selected_adoption_decision": None,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "boundary_rule": "The packet may ask for a human decision. It cannot take the decision or execute/promotion/adoption side effects.",
    }

    option_runtime = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_option_runtime_adoption_v0",
        "human_decision_packet_id": human_decision_packet_id,
        "option": "PREPARE_RUNTIME_ADOPTION_DECISION_PACKET",
        "source_candidate_status": runtime_adoption_candidate.get("candidate_status"),
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
    }

    option_schema = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_option_schema_archive_promotion_v0",
        "human_decision_packet_id": human_decision_packet_id,
        "option": "PREPARE_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET",
        "source_candidate_status": schema_promotion_candidate.get("candidate_status"),
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
    }

    option_move = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_option_move_registry_addition_v0",
        "human_decision_packet_id": human_decision_packet_id,
        "option": "PREPARE_MOVE_REGISTRY_ADDITION_DECISION_PACKET",
        "source_candidate_status": move_registry_candidate.get("candidate_status"),
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "move_addition_authorized": False,
    }

    option_fixture = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_option_fixture_test_expansion_v0",
        "human_decision_packet_id": human_decision_packet_id,
        "option": "PREPARE_FIXTURE_TEST_EXPANSION_DECISION_PACKET",
        "source_candidate_status": fixture_expansion_candidate.get("candidate_status"),
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "fixture_expansion_authorized": False,
    }

    option_t6 = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_option_t6_live_case_execution_v0",
        "human_decision_packet_id": human_decision_packet_id,
        "option": "PREPARE_T6_LIVE_CASE_EXECUTION_DECISION_PACKET",
        "source_candidate_status": t6_live_case_candidate.get("candidate_status"),
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "t6_live_case_execution_authorized": False,
    }

    option_defer = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_option_defer_v0",
        "human_decision_packet_id": human_decision_packet_id,
        "option": "DEFER_ADOPTION_PATH",
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "all_adoption_authorities": False,
    }

    option_freeze = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_option_freeze_reference_only_v0",
        "human_decision_packet_id": human_decision_packet_id,
        "option": "FREEZE_CAPABILITY_AS_REFERENCE_ONLY",
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "all_adoption_authorities": False,
    }

    option_close = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_option_close_no_adoption_v0",
        "human_decision_packet_id": human_decision_packet_id,
        "option": "CLOSE_ADOPTION_PATH_NO_ADOPTION",
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "all_adoption_authorities": False,
    }

    human_decision_request_packet = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_request_packet_v0",
        "packet_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "human_decision_packet_id": human_decision_packet_id,
        "adoption_review_id": ADOPTION_REVIEW_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "required_capability": REQUIRED_CAPABILITY,
        "proposed_surface": PROPOSED_SURFACE,
        "decision_question": "Which bounded adoption/promotion path should be prepared next for the reviewed structured T6 trigger-surface capability?",
        "available_decisions": DECISION_OPTIONS,
        "selected_adoption_decision": None,
        "human_decision_taken": False,
        "decision_boundary": "Selecting an option authorizes only the corresponding next bounded decision-path/recording unit. It does not directly adopt, patch, mutate schema, add moves, expand fixtures, execute T6, or authorize C8.",
        "must_remain_false_until_recorded_decision": FORBIDDEN_AUTHORITY_KEYS,
    }

    negative_control = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_negative_control_v0",
        "human_decision_packet_id": human_decision_packet_id,
        "negative_control_status": "PASS" if gate == "PASS" else "BLOCKED",
        "human_decision_taken": False,
        "selected_adoption_decision": None,
        "zero_counters_for_this_unit": {
            "runtime_adoption_count": 0,
            "runtime_patch_count": 0,
            "schema_archive_mutation_count": 0,
            "schema_mutation_count": 0,
            "move_addition_count": 0,
            "fixture_expansion_count": 0,
            "t6_live_case_execution_count": 0,
            "hidden_next_command_count": 0,
            "c8_authorization_count": 0,
        },
        "negative_control_rule": "A human decision packet is not a human decision record and has no side-effect authority.",
    }

    rollup = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "human_decision_packet_id": human_decision_packet_id,
        "adoption_review_id": ADOPTION_REVIEW_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "human_decision_packet_ready": True if gate == "PASS" else False,
        "human_adoption_decision_required": True if gate == "PASS" else False,
        "human_adoption_decision_taken": False,
        "selected_adoption_decision": None,
        "available_decision_count": len(DECISION_OPTIONS) if gate == "PASS" else 0,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "terminal_stop_code": "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_HUMAN_DECISION_REQUIRED" if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_HUMAN_DECISION_PACKET_GATE_FAIL",
    }

    readout = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_readout_v0",
        "status": status,
        "human_decision_packet_id": human_decision_packet_id,
        "adoption_review_id": ADOPTION_REVIEW_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "interpretation": "Human decision packet is ready. No adoption decision has been selected and no runtime/schema/move/fixture/T6/C8 authority was granted."
        if gate == "PASS" else "Human decision packet preparation failed typed gates.",
        "stop_code": "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_HUMAN_DECISION_REQUIRED" if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_HUMAN_DECISION_PACKET_GATE_FAIL",
    }

    profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_profile_v0",
        "profile_status": status,
        "human_decision_packet_id": human_decision_packet_id,
        "core_rule": "Packet asks for a human decision and stops. It does not choose, authorize, or execute any adoption/promotion surface.",
        "human_decision_request_packet_ref": rel(HUMAN_DECISION_REQUEST_PACKET_PATH),
        "must_not_infer": [
            "runtime adopted",
            "runtime patched",
            "schema archive mutated",
            "schema promoted",
            "move registry updated",
            "fixture suite expanded",
            "T6 live case executed",
            "C8 authorized",
            "human adoption decision taken",
            "selected adoption decision",
        ],
    }

    report = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "packet_result": "HUMAN_DECISION_REQUIRED" if gate == "PASS" else "HUMAN_DECISION_PACKET_GATE_FAIL",
            "human_decision_packet_id": human_decision_packet_id,
            "adoption_review_id": ADOPTION_REVIEW_ID,
            "adoption_path_id": ADOPTION_PATH_ID,
            "capability_build_id": CAPABILITY_BUILD_ID,
            "proposal_id": PROPOSAL_ID,
            "human_decision_packet_ready": True if gate == "PASS" else False,
            "human_adoption_decision_taken": False,
            "selected_adoption_decision": None,
            "available_decisions": DECISION_OPTIONS,
            "runtime_adoption_authorized": False,
            "schema_archive_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "t6_live_case_execution_authorized": False,
            "c8_authorized": False,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_transition_trace_v0",
        "unit_id": UNIT_ID,
        "human_decision_packet_id": human_decision_packet_id,
        "transitions": [
            {
                "from": "HUMAN_DECISION_PACKET_PREP_READY",
                "edge": "prepare human decision packet with bounded adoption/promotion options",
                "to": "HUMAN_DECISION_PACKET_READY" if gate == "PASS" else "HUMAN_DECISION_PACKET_GATE_FAIL",
            },
            {
                "from": "HUMAN_DECISION_PACKET_READY" if gate == "PASS" else "HUMAN_DECISION_PACKET_GATE_FAIL",
                "edge": "stop for human decision without selecting option",
                "to": "STOP_HUMAN_DECISION_REQUIRED" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "STOP",
            "next_unit_id": None,
            "stop_code": "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_HUMAN_DECISION_REQUIRED"
            if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_HUMAN_DECISION_PACKET_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (SOURCE_REVIEW_BINDING_PATH, source_review_binding),
        (DECISION_OPTIONS_PATH, decision_options),
        (DECISION_EFFECTS_MAP_PATH, decision_effects_map),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (RUNTIME_ADOPTION_OPTION_PATH, option_runtime),
        (SCHEMA_PROMOTION_OPTION_PATH, option_schema),
        (MOVE_REGISTRY_OPTION_PATH, option_move),
        (FIXTURE_EXPANSION_OPTION_PATH, option_fixture),
        (T6_LIVE_CASE_OPTION_PATH, option_t6),
        (DEFER_OPTION_PATH, option_defer),
        (FREEZE_REFERENCE_OPTION_PATH, option_freeze),
        (CLOSE_NO_ADOPTION_OPTION_PATH, option_close),
        (HUMAN_DECISION_REQUEST_PACKET_PATH, human_decision_request_packet),
        (NEGATIVE_CONTROL_PATH, negative_control),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "ADOPTION_PATH_REVIEW_RECEIPT_CONSUMED",
        "HUMAN_DECISION_PACKET_PREP_TARGET_CONSUMED",
        "SOURCE_REVIEW_BINDING_PASS",
        "DECISION_OPTIONS_EMITTED",
        "DECISION_EFFECTS_MAP_EMITTED",
        "AUTHORITY_BOUNDARY_EMITTED",
        "RUNTIME_ADOPTION_OPTION_AVAILABLE_NOT_SELECTED",
        "SCHEMA_PROMOTION_OPTION_AVAILABLE_NOT_SELECTED",
        "MOVE_REGISTRY_OPTION_AVAILABLE_NOT_SELECTED",
        "FIXTURE_EXPANSION_OPTION_AVAILABLE_NOT_SELECTED",
        "T6_LIVE_CASE_OPTION_AVAILABLE_NOT_SELECTED",
        "DEFER_OPTION_AVAILABLE_NOT_SELECTED",
        "FREEZE_REFERENCE_ONLY_OPTION_AVAILABLE_NOT_SELECTED",
        "CLOSE_NO_ADOPTION_OPTION_AVAILABLE_NOT_SELECTED",
        "HUMAN_DECISION_REQUEST_PACKET_READY",
        "NEGATIVE_CONTROL_PASS",
        "STOP_HUMAN_DECISION_REQUIRED",
        "NO_HUMAN_ADOPTION_DECISION_TAKEN",
        "NO_SELECTED_ADOPTION_DECISION",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_RUNTIME_PATCH",
        "NO_SCHEMA_ARCHIVE_MUTATION",
        "NO_SCHEMA_MUTATION",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_T6_LIVE_CASE_EXECUTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_HUMAN_DECISION_PACKET_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "human_decision_packet_id": human_decision_packet_id,
        "adoption_review_id": ADOPTION_REVIEW_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "source_adoption_path_review_receipt_id": ADOPTION_PATH_REVIEW_RECEIPT_ID,
        "source_adoption_path_review_receipt_ref": rel(ADOPTION_PATH_REVIEW_RECEIPT_PATH),
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "ADOPTION_HUMAN_DECISION_PACKET_0_REVIEW_RECEIPT_CONSUMED": gate == "PASS",
            "ADOPTION_HUMAN_DECISION_PACKET_1_PREP_TARGET_CONSUMED": gate == "PASS",
            "ADOPTION_HUMAN_DECISION_PACKET_2_OPTIONS_EMITTED": DECISION_OPTIONS_PATH.exists() and gate == "PASS",
            "ADOPTION_HUMAN_DECISION_PACKET_3_EFFECTS_MAP_EMITTED": DECISION_EFFECTS_MAP_PATH.exists() and gate == "PASS",
            "ADOPTION_HUMAN_DECISION_PACKET_4_AUTHORITY_BOUNDARY_EMITTED": AUTHORITY_BOUNDARY_PATH.exists() and gate == "PASS",
            "ADOPTION_HUMAN_DECISION_PACKET_5_REQUEST_PACKET_READY": HUMAN_DECISION_REQUEST_PACKET_PATH.exists() and gate == "PASS",
            "ADOPTION_HUMAN_DECISION_PACKET_6_NEGATIVE_CONTROL_PASS": NEGATIVE_CONTROL_PATH.exists() and gate == "PASS",
            "ADOPTION_HUMAN_DECISION_PACKET_7_NO_HUMAN_DECISION_TAKEN": True,
            "ADOPTION_HUMAN_DECISION_PACKET_8_NO_SELECTED_DECISION": True,
            "ADOPTION_HUMAN_DECISION_PACKET_9_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "ADOPTION_HUMAN_DECISION_PACKET_10_NO_RUNTIME_PATCH": True,
            "ADOPTION_HUMAN_DECISION_PACKET_11_NO_SCHEMA_ARCHIVE_MUTATION": True,
            "ADOPTION_HUMAN_DECISION_PACKET_12_NO_MOVE_ADDITION": True,
            "ADOPTION_HUMAN_DECISION_PACKET_13_NO_FIXTURE_EXPANSION": True,
            "ADOPTION_HUMAN_DECISION_PACKET_14_NO_T6_LIVE_CASE_EXECUTION": True,
            "ADOPTION_HUMAN_DECISION_PACKET_15_NO_C8_AUTHORIZATION": True,
            "ADOPTION_HUMAN_DECISION_PACKET_16_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_summary": {
            "status": status,
            "human_decision_packet_id": human_decision_packet_id,
            "adoption_review_id": ADOPTION_REVIEW_ID,
            "adoption_path_id": ADOPTION_PATH_ID,
            "capability_build_id": CAPABILITY_BUILD_ID,
            "proposal_id": PROPOSAL_ID,
            "required_capability": REQUIRED_CAPABILITY,
            "proposed_surface": PROPOSED_SURFACE,
            "human_decision_packet_ready": True if gate == "PASS" else False,
            "human_adoption_decision_required": True if gate == "PASS" else False,
            "human_adoption_decision_taken": False,
            "selected_adoption_decision": None,
            "available_decisions": DECISION_OPTIONS if gate == "PASS" else [],
            "available_decision_count": len(DECISION_OPTIONS) if gate == "PASS" else 0,
            "runtime_adoption_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "schema_promotion_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "move_registry_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "fixture_expansion_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "t6_live_case_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "defer_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "freeze_reference_only_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "close_no_adoption_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "runtime_adoption_authorized": False,
            "runtime_patch_authorized": False,
            "schema_archive_mutation_authorized": False,
            "schema_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "t6_live_case_execution_authorized": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "next_unit_id": None,
            "terminal_stop_code": transition_trace["terminal"]["stop_code"],
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "source_review_binding": rel(SOURCE_REVIEW_BINDING_PATH),
            "decision_options": rel(DECISION_OPTIONS_PATH),
            "decision_effects_map": rel(DECISION_EFFECTS_MAP_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "runtime_adoption_option": rel(RUNTIME_ADOPTION_OPTION_PATH),
            "schema_promotion_option": rel(SCHEMA_PROMOTION_OPTION_PATH),
            "move_registry_option": rel(MOVE_REGISTRY_OPTION_PATH),
            "fixture_expansion_option": rel(FIXTURE_EXPANSION_OPTION_PATH),
            "t6_live_case_option": rel(T6_LIVE_CASE_OPTION_PATH),
            "defer_option": rel(DEFER_OPTION_PATH),
            "freeze_reference_only_option": rel(FREEZE_REFERENCE_OPTION_PATH),
            "close_no_adoption_option": rel(CLOSE_NO_ADOPTION_OPTION_PATH),
            "human_decision_request_packet": rel(HUMAN_DECISION_REQUEST_PACKET_PATH),
            "negative_control": rel(NEGATIVE_CONTROL_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_receipt_id={receipt_id}")
    print(f"bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_receipt_path={rel(receipt_path)}")
    print(f"bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_id={human_decision_packet_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_terminal_stop_code={transition_trace['terminal']['stop_code']}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
