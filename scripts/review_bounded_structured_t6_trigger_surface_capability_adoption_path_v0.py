#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_PATH_V0"
TARGET_UNIT_ID = "bounded_structured_t6_trigger_surface_capability.adoption_path_review_v0"
NEXT_UNIT_ID = "PREPARE_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_HUMAN_DECISION_PACKET_V0"

ADOPTION_PATH_PREP_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_receipt_34a6f83a"
ADOPTION_PATH_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_6f9974e5"
CAPABILITY_BUILD_ID = "bounded_structured_t6_trigger_surface_capability_build_721f09dc"
BUILD_REVIEW_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_build_review_receipt_b8dba552"
BUILD_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079"
PROPOSAL_ID = "capability_proposal_57dda6e9"
REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"

ADOPTION_PATH_PREP_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0_receipts/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_receipt_34a6f83a.json"

ADOPTION_PATH_REVIEW_TARGET_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_adoption_path_review_target_v0.json"
SOURCE_REVIEW_BINDING_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_adoption_source_review_binding_v0.json"
ADOPTION_SCOPE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_adoption_path_scope_v0.json"
ADOPTION_SURFACE_INVENTORY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_adoption_surface_inventory_v0.json"
AUTHORITY_BOUNDARY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_adoption_authority_boundary_v0.json"
DECISION_SURFACE_MAP_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_adoption_decision_surface_map_v0.json"
RUNTIME_ADOPTION_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_runtime_adoption_candidate_v0.json"
SCHEMA_PROMOTION_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_candidate_v0.json"
MOVE_REGISTRY_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_move_registry_candidate_v0.json"
FIXTURE_EXPANSION_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_fixture_expansion_candidate_v0.json"
T6_LIVE_CASE_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_t6_live_case_candidate_v0.json"
C8_BOUNDARY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_c8_boundary_v0.json"
ADOPTION_NEGATIVE_CONTROL_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_adoption_negative_control_v0.json"
HUMAN_DECISION_PACKET_DRAFT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_draft_v0.json"

BUILD_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_review_receipt_b8dba552.json"
BUILD_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079.json"
PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"

OUT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0"
RECEIPT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_review_basis_v0.json"
SOURCE_BINDING_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_source_binding_review_v0.json"
ADOPTION_SCOPE_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_scope_review_v0.json"
SURFACE_INVENTORY_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_surface_inventory_review_v0.json"
AUTHORITY_BOUNDARY_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_authority_boundary_review_v0.json"
DECISION_SURFACE_MAP_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_decision_surface_map_review_v0.json"
CANDIDATE_SURFACES_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_candidate_surfaces_review_v0.json"
C8_BOUNDARY_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_c8_boundary_review_v0.json"
ADOPTION_NEGATIVE_CONTROL_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_negative_control_review_v0.json"
HUMAN_DECISION_PACKET_PREP_TARGET_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_prep_target_v0.json"
READOUT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_review_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_review_transition_trace.json"

EXPECTED_FUTURE_SURFACES = [
    "runtime adoption",
    "schema archive promotion",
    "move registry addition",
    "fixture/test expansion",
    "T6 live-case execution",
]

CANDIDATE_PATHS = {
    "runtime_adoption": RUNTIME_ADOPTION_CANDIDATE_PATH,
    "schema_promotion": SCHEMA_PROMOTION_CANDIDATE_PATH,
    "move_registry": MOVE_REGISTRY_CANDIDATE_PATH,
    "fixture_expansion": FIXTURE_EXPANSION_CANDIDATE_PATH,
    "t6_live_case": T6_LIVE_CASE_CANDIDATE_PATH,
}

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

def lower_list(xs: Any) -> List[str]:
    return [str(x).lower() for x in (xs or [])]

def require_false(obj: Dict[str, Any], key: str, failures: List[str], prefix: str) -> None:
    if obj.get(key) is not False:
        failures.append(f"{prefix}_{key}_not_false:{obj.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        ADOPTION_PATH_PREP_RECEIPT_PATH,
        ADOPTION_PATH_REVIEW_TARGET_PATH,
        SOURCE_REVIEW_BINDING_PATH,
        ADOPTION_SCOPE_PATH,
        ADOPTION_SURFACE_INVENTORY_PATH,
        AUTHORITY_BOUNDARY_PATH,
        DECISION_SURFACE_MAP_PATH,
        RUNTIME_ADOPTION_CANDIDATE_PATH,
        SCHEMA_PROMOTION_CANDIDATE_PATH,
        MOVE_REGISTRY_CANDIDATE_PATH,
        FIXTURE_EXPANSION_CANDIDATE_PATH,
        T6_LIVE_CASE_CANDIDATE_PATH,
        C8_BOUNDARY_PATH,
        ADOPTION_NEGATIVE_CONTROL_PATH,
        HUMAN_DECISION_PACKET_DRAFT_PATH,
        BUILD_REVIEW_RECEIPT_PATH,
        BUILD_RECEIPT_PATH,
        PROPOSAL_PATH,
    ]

    failures: List[str] = []

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    prep_receipt = read_json(ADOPTION_PATH_PREP_RECEIPT_PATH)
    review_target = read_json(ADOPTION_PATH_REVIEW_TARGET_PATH)
    source_binding = read_json(SOURCE_REVIEW_BINDING_PATH)
    adoption_scope = read_json(ADOPTION_SCOPE_PATH)
    surface_inventory = read_json(ADOPTION_SURFACE_INVENTORY_PATH)
    authority_boundary = read_json(AUTHORITY_BOUNDARY_PATH)
    decision_surface_map = read_json(DECISION_SURFACE_MAP_PATH)
    candidates = {name: read_json(path) for name, path in CANDIDATE_PATHS.items()}
    c8_boundary = read_json(C8_BOUNDARY_PATH)
    negative_control = read_json(ADOPTION_NEGATIVE_CONTROL_PATH)
    human_decision_packet_draft = read_json(HUMAN_DECISION_PACKET_DRAFT_PATH)
    build_review_receipt = read_json(BUILD_REVIEW_RECEIPT_PATH)
    build_receipt = read_json(BUILD_RECEIPT_PATH)
    proposal = read_json(PROPOSAL_PATH)

    prep_summary = prep_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_adoption_path_prep_summary", {})
    build_review_summary = build_review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_review_summary", {})
    build_summary = build_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_summary", {})

    if prep_receipt.get("receipt_id") != ADOPTION_PATH_PREP_RECEIPT_ID:
        failures.append(f"prep_receipt_id_wrong:{prep_receipt.get('receipt_id')}")
    if prep_receipt.get("gate") != "PASS":
        failures.append("prep_receipt_gate_not_pass")
    if prep_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"prep_terminal_next_wrong:{prep_receipt.get('terminal', {}).get('next_unit_id')}")

    for key in [
        "source_build_review_pass",
        "adoption_path_prepared",
        "adoption_path_review_target_ready",
        "future_surfaces_require_separate_human_decision",
    ]:
        if prep_summary.get(key) is not True:
            failures.append(f"prep_summary_{key}_not_true:{prep_summary.get(key)}")

    if prep_summary.get("human_adoption_decision_taken") is not False:
        failures.append("prep_summary_human_adoption_decision_already_taken")
    if prep_summary.get("selected_adoption_decision") is not None:
        failures.append(f"prep_summary_selected_adoption_decision_not_none:{prep_summary.get('selected_adoption_decision')}")

    for key in FORBIDDEN_AUTHORITY_KEYS:
        require_false(prep_summary, key, failures, "prep_summary")

    if prep_summary.get("adoption_path_id") != ADOPTION_PATH_ID:
        failures.append(f"prep_summary_adoption_path_id_wrong:{prep_summary.get('adoption_path_id')}")
    if prep_summary.get("capability_build_id") != CAPABILITY_BUILD_ID:
        failures.append(f"prep_summary_capability_build_id_wrong:{prep_summary.get('capability_build_id')}")

    if review_target.get("target_status") != "READY":
        failures.append(f"review_target_status_wrong:{review_target.get('target_status')}")
    if review_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"review_target_next_wrong:{review_target.get('next_unit_id')}")
    for key in [
        "does_not_authorize_runtime_adoption",
        "does_not_authorize_schema_archive_mutation",
        "does_not_authorize_move_addition",
        "does_not_authorize_fixture_expansion",
        "does_not_authorize_t6_live_case_execution",
        "does_not_authorize_c8",
    ]:
        if review_target.get(key) is not True:
            failures.append(f"review_target_{key}_not_true:{review_target.get(key)}")

    # Source binding review.
    binding_failures: List[str] = []
    if source_binding.get("binding_status") != "PASS":
        binding_failures.append(f"binding_status_wrong:{source_binding.get('binding_status')}")
    if source_binding.get("capability_build_id") != CAPABILITY_BUILD_ID:
        binding_failures.append("capability_build_id_wrong")
    if source_binding.get("build_review_receipt_id") != BUILD_REVIEW_RECEIPT_ID:
        binding_failures.append("build_review_receipt_id_wrong")
    if source_binding.get("artifact_review_pass") is not True:
        binding_failures.append("artifact_review_pass_not_true")

    # Scope review.
    scope_failures: List[str] = []
    if adoption_scope.get("scope_status") != "READY_FOR_REVIEW":
        scope_failures.append(f"scope_status_wrong:{adoption_scope.get('scope_status')}")
    if adoption_scope.get("path_scope", "").lower().find("possible future adoption") == -1:
        scope_failures.append("path_scope_missing_future_adoption")
    in_scope = lower_list(adoption_scope.get("in_scope_for_this_unit"))
    for phrase in [
        "inventory possible future adoption/promotion surfaces",
        "define authority boundaries",
        "prepare candidate decision surfaces",
        "prepare review target",
        "keep every actual adoption/promotion authority false",
    ]:
        if phrase not in in_scope:
            scope_failures.append(f"in_scope_missing:{phrase}")

    # Surface inventory review.
    inventory_failures: List[str] = []
    if surface_inventory.get("inventory_status") != "READY_FOR_REVIEW":
        inventory_failures.append(f"inventory_status_wrong:{surface_inventory.get('inventory_status')}")
    inventory_surfaces = surface_inventory.get("future_surfaces") or []
    by_surface = {str(x.get("surface")): x for x in inventory_surfaces if isinstance(x, dict)}
    for surface in EXPECTED_FUTURE_SURFACES:
        item = by_surface.get(surface)
        if not item:
            inventory_failures.append(f"future_surface_missing:{surface}")
            continue
        if item.get("requires_separate_human_decision") is not True:
            inventory_failures.append(f"future_surface_human_decision_not_required:{surface}")
        if item.get("authorized_now") is not False:
            inventory_failures.append(f"future_surface_authorized_now_unexpected:{surface}")
    if surface_inventory.get("c8_surface_status") != "OUT_OF_SCOPE_NOT_AUTHORIZED":
        inventory_failures.append(f"c8_surface_status_wrong:{surface_inventory.get('c8_surface_status')}")

    # Authority boundary review.
    authority_failures: List[str] = []
    if authority_boundary.get("boundary_status") != "READY_FOR_REVIEW":
        authority_failures.append(f"boundary_status_wrong:{authority_boundary.get('boundary_status')}")
    if authority_boundary.get("future_surfaces_require_separate_human_decision") is not True:
        authority_failures.append("future_surfaces_require_separate_human_decision_not_true")
    for key in FORBIDDEN_AUTHORITY_KEYS:
        if authority_boundary.get(key) is not False:
            authority_failures.append(f"{key}_not_false:{authority_boundary.get(key)}")
    if "cannot choose or apply" not in str(authority_boundary.get("boundary_rule", "")).lower():
        authority_failures.append("boundary_rule_missing_cannot_choose_or_apply")

    # Decision surface map review.
    decision_failures: List[str] = []
    if decision_surface_map.get("map_status") != "READY_FOR_REVIEW":
        decision_failures.append(f"map_status_wrong:{decision_surface_map.get('map_status')}")
    if decision_surface_map.get("selected_decision") is not None:
        decision_failures.append("selected_decision_not_none")
    candidate_decisions = decision_surface_map.get("candidate_decisions") or []
    for item in [
        "PREPARE_RUNTIME_ADOPTION_DECISION_PACKET",
        "PREPARE_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET",
        "PREPARE_MOVE_REGISTRY_ADDITION_DECISION_PACKET",
        "PREPARE_FIXTURE_TEST_EXPANSION_DECISION_PACKET",
        "PREPARE_T6_LIVE_CASE_EXECUTION_DECISION_PACKET",
        "DEFER_ADOPTION_PATH",
        "FREEZE_CAPABILITY_AS_REFERENCE_ONLY",
        "CLOSE_ADOPTION_PATH_NO_ADOPTION",
    ]:
        if item not in candidate_decisions:
            decision_failures.append(f"candidate_decision_missing:{item}")
    if "none is selected" not in str(decision_surface_map.get("decision_rule", "")).lower():
        decision_failures.append("decision_rule_missing_none_selected")

    # Candidate surfaces review.
    candidate_failures: List[str] = []
    expected_candidate_false_keys = {
        "runtime_adoption": ["runtime_adoption_authorized", "runtime_patch_authorized"],
        "schema_promotion": ["schema_archive_mutation_authorized", "schema_mutation_authorized"],
        "move_registry": ["move_addition_authorized"],
        "fixture_expansion": ["fixture_expansion_authorized"],
        "t6_live_case": ["t6_live_case_execution_authorized"],
    }
    for name, obj in candidates.items():
        if obj.get("candidate_status") != "CANDIDATE_ONLY_NOT_AUTHORIZED":
            candidate_failures.append(f"{name}_candidate_status_wrong:{obj.get('candidate_status')}")
        if obj.get("adoption_path_id") != ADOPTION_PATH_ID:
            candidate_failures.append(f"{name}_adoption_path_id_wrong:{obj.get('adoption_path_id')}")
        for key in expected_candidate_false_keys[name]:
            if obj.get(key) is not False:
                candidate_failures.append(f"{name}_{key}_not_false:{obj.get(key)}")
        if not obj.get("required_before_authorization"):
            candidate_failures.append(f"{name}_required_before_authorization_missing")

    # C8 and negative-control review.
    c8_failures: List[str] = []
    if c8_boundary.get("boundary_status") != "CLOSED":
        c8_failures.append(f"c8_boundary_status_wrong:{c8_boundary.get('boundary_status')}")
    if c8_boundary.get("c8_authorized") is not False:
        c8_failures.append("c8_authorized_not_false")
    if c8_boundary.get("c8_discussion_authorized") is not False:
        c8_failures.append("c8_discussion_authorized_not_false")

    negative_failures: List[str] = []
    if negative_control.get("negative_control_status") != "PASS":
        negative_failures.append(f"negative_control_status_wrong:{negative_control.get('negative_control_status')}")
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
            negative_failures.append(f"zero_counter_wrong:{key}:{zero.get(key)}")

    # Human decision draft review.
    draft_failures: List[str] = []
    if human_decision_packet_draft.get("draft_status") != "DRAFT_ONLY_NOT_REVIEWED":
        draft_failures.append(f"draft_status_wrong:{human_decision_packet_draft.get('draft_status')}")
    if human_decision_packet_draft.get("decision_required_later") is not True:
        draft_failures.append("decision_required_later_not_true")
    if human_decision_packet_draft.get("selected_decision") is not None:
        draft_failures.append("draft_selected_decision_not_none")
    future_options = lower_list(human_decision_packet_draft.get("available_future_decision_surfaces"))
    for option in [
        "runtime adoption",
        "schema archive promotion",
        "move registry addition",
        "fixture/test expansion",
        "t6 live-case execution",
        "defer",
        "freeze reference-only",
        "close no-adoption",
    ]:
        if option not in future_options:
            draft_failures.append(f"future_decision_surface_missing:{option}")

    if binding_failures:
        failures.append(f"source_binding_review_failures:{binding_failures}")
    if scope_failures:
        failures.append(f"scope_review_failures:{scope_failures}")
    if inventory_failures:
        failures.append(f"inventory_review_failures:{inventory_failures}")
    if authority_failures:
        failures.append(f"authority_boundary_review_failures:{authority_failures}")
    if decision_failures:
        failures.append(f"decision_surface_map_review_failures:{decision_failures}")
    if candidate_failures:
        failures.append(f"candidate_surfaces_review_failures:{candidate_failures}")
    if c8_failures:
        failures.append(f"c8_boundary_review_failures:{c8_failures}")
    if negative_failures:
        failures.append(f"negative_control_review_failures:{negative_failures}")
    if draft_failures:
        failures.append(f"human_decision_packet_draft_review_failures:{draft_failures}")

    if build_review_summary.get("artifact_review_pass") is not True:
        failures.append("source_build_review_artifact_review_not_pass")
    if build_summary.get("build_executed") is not True:
        failures.append("source_build_not_executed")
    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_PATH_REVIEW_PASS_HUMAN_DECISION_PACKET_PREP_READY"
        if gate == "PASS"
        else "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_PATH_REVIEW_GATE_FAIL"
    )

    adoption_review_id = "bounded_structured_t6_trigger_surface_capability_adoption_path_review_" + sig8({
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "prep_receipt_id": ADOPTION_PATH_PREP_RECEIPT_ID,
    })

    human_decision_packet_prep_target_id = "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_prep_" + sig8({
        "adoption_review_id": adoption_review_id,
        "adoption_path_id": ADOPTION_PATH_ID,
        "candidate_surfaces": EXPECTED_FUTURE_SURFACES,
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_review_basis_v0",
        "unit_id": UNIT_ID,
        "adoption_review_id": adoption_review_id,
        "adoption_path_id": ADOPTION_PATH_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_adoption_path_prep_receipt_id": ADOPTION_PATH_PREP_RECEIPT_ID,
        "source_capability_build_id": CAPABILITY_BUILD_ID,
        "source_proposal_id": PROPOSAL_ID,
        "review_claim": "Review adoption path prep and prepare human decision packet target only. Do not select an adoption decision or authorize any adoption/promotion surface.",
        "source_file_hashes": source_hashes,
    }

    source_binding_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_source_binding_review_v0",
        "adoption_review_id": adoption_review_id,
        "review_status": "PASS" if not binding_failures else "FAIL",
        "failures": binding_failures,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "build_receipt_id": BUILD_RECEIPT_ID,
        "build_review_receipt_id": BUILD_REVIEW_RECEIPT_ID,
    }

    adoption_scope_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_scope_review_v0",
        "adoption_review_id": adoption_review_id,
        "review_status": "PASS" if not scope_failures else "FAIL",
        "failures": scope_failures,
        "path_scope": adoption_scope.get("path_scope"),
        "in_scope_for_this_unit": adoption_scope.get("in_scope_for_this_unit"),
        "not_in_scope_for_this_unit": adoption_scope.get("not_in_scope_for_this_unit"),
    }

    surface_inventory_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_surface_inventory_review_v0",
        "adoption_review_id": adoption_review_id,
        "review_status": "PASS" if not inventory_failures else "FAIL",
        "failures": inventory_failures,
        "future_surfaces": surface_inventory.get("future_surfaces"),
        "c8_surface_status": surface_inventory.get("c8_surface_status"),
    }

    authority_boundary_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_authority_boundary_review_v0",
        "adoption_review_id": adoption_review_id,
        "review_status": "PASS" if not authority_failures else "FAIL",
        "failures": authority_failures,
        "future_surfaces_require_separate_human_decision": authority_boundary.get("future_surfaces_require_separate_human_decision"),
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    decision_surface_map_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_decision_surface_map_review_v0",
        "adoption_review_id": adoption_review_id,
        "review_status": "PASS" if not decision_failures else "FAIL",
        "failures": decision_failures,
        "candidate_decisions": decision_surface_map.get("candidate_decisions"),
        "selected_decision": None,
        "decision_rule": decision_surface_map.get("decision_rule"),
    }

    candidate_surfaces_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_candidate_surfaces_review_v0",
        "adoption_review_id": adoption_review_id,
        "review_status": "PASS" if not candidate_failures else "FAIL",
        "failures": candidate_failures,
        "candidate_surface_statuses": {
            name: obj.get("candidate_status") for name, obj in candidates.items()
        },
        "all_candidate_only_not_authorized": not candidate_failures,
    }

    c8_boundary_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_c8_boundary_review_v0",
        "adoption_review_id": adoption_review_id,
        "review_status": "PASS" if not c8_failures else "FAIL",
        "failures": c8_failures,
        "c8_authorized": False,
        "c8_discussion_authorized": False,
    }

    adoption_negative_control_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_negative_control_review_v0",
        "adoption_review_id": adoption_review_id,
        "review_status": "PASS" if not negative_failures else "FAIL",
        "failures": negative_failures,
        "zero_counters_for_this_unit": zero,
    }

    human_decision_packet_prep_target = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_prep_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "human_decision_packet_prep_target_id": human_decision_packet_prep_target_id,
        "adoption_review_id": adoption_review_id,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "review_result": status,
        "packet_scope": "Prepare a human decision packet for adoption/promotion surfaces. The packet-prep unit may surface choices but must not select them.",
        "available_future_decision_surfaces": [
            "runtime adoption",
            "schema archive promotion",
            "move registry addition",
            "fixture/test expansion",
            "T6 live-case execution",
            "defer",
            "freeze reference-only",
            "close no-adoption",
        ],
        "must_remain_false_until_human_decision": FORBIDDEN_AUTHORITY_KEYS,
        "human_decision_required": True,
        "human_decision_taken": False,
        "selected_adoption_decision": None,
    }

    rollup = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_review_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "adoption_review_id": adoption_review_id,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "source_binding_review_pass": not binding_failures,
        "scope_review_pass": not scope_failures,
        "surface_inventory_review_pass": not inventory_failures,
        "authority_boundary_review_pass": not authority_failures,
        "decision_surface_map_review_pass": not decision_failures,
        "candidate_surfaces_review_pass": not candidate_failures,
        "c8_boundary_review_pass": not c8_failures,
        "negative_control_review_pass": not negative_failures,
        "human_decision_packet_draft_review_pass": not draft_failures,
        "adoption_path_review_pass": True if gate == "PASS" else False,
        "human_decision_packet_prep_target_ready": True if gate == "PASS" else False,
        "human_adoption_decision_taken": False,
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
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    readout = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_review_readout_v0",
        "status": status,
        "adoption_review_id": adoption_review_id,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "interpretation": "Adoption path review passed and prepared a human decision packet prep target. No adoption decision was selected and no runtime/schema/move/fixture/T6/C8 authority was granted."
        if gate == "PASS" else "Adoption path review failed typed gates.",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_review_profile_v0",
        "profile_status": status,
        "adoption_review_id": adoption_review_id,
        "adoption_path_id": ADOPTION_PATH_ID,
        "core_rule": "Review adoption path only; prepare human-decision packet target only. Do not choose or apply an adoption surface.",
        "human_decision_packet_prep_target_ref": rel(HUMAN_DECISION_PACKET_PREP_TARGET_PATH),
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
        ],
    }

    report = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_review_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "review_result": "ADOPTION_PATH_REVIEW_PASS_HUMAN_DECISION_PACKET_PREP_READY" if gate == "PASS" else "ADOPTION_PATH_REVIEW_GATE_FAIL",
            "adoption_review_id": adoption_review_id,
            "adoption_path_id": ADOPTION_PATH_ID,
            "capability_build_id": CAPABILITY_BUILD_ID,
            "proposal_id": PROPOSAL_ID,
            "human_decision_packet_prep_target_ready": True if gate == "PASS" else False,
            "human_adoption_decision_taken": False,
            "selected_adoption_decision": None,
            "runtime_adoption_authorized": False,
            "schema_archive_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "t6_live_case_execution_authorized": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_review_transition_trace_v0",
        "unit_id": UNIT_ID,
        "adoption_review_id": adoption_review_id,
        "transitions": [
            {
                "from": "ADOPTION_PATH_REVIEW_READY",
                "edge": "review source binding, scope, inventory, authority boundary, decision map, candidate surfaces, C8 boundary, and negative controls",
                "to": "ADOPTION_PATH_REVIEW_PASS" if gate == "PASS" else "ADOPTION_PATH_REVIEW_GATE_FAIL",
            },
            {
                "from": "ADOPTION_PATH_REVIEW_PASS" if gate == "PASS" else "ADOPTION_PATH_REVIEW_GATE_FAIL",
                "edge": "emit human decision packet prep target without selecting decision",
                "to": "HUMAN_DECISION_PACKET_PREP_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_PATH_REVIEW_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (SOURCE_BINDING_REVIEW_PATH, source_binding_review),
        (ADOPTION_SCOPE_REVIEW_PATH, adoption_scope_review),
        (SURFACE_INVENTORY_REVIEW_PATH, surface_inventory_review),
        (AUTHORITY_BOUNDARY_REVIEW_PATH, authority_boundary_review),
        (DECISION_SURFACE_MAP_REVIEW_PATH, decision_surface_map_review),
        (CANDIDATE_SURFACES_REVIEW_PATH, candidate_surfaces_review),
        (C8_BOUNDARY_REVIEW_PATH, c8_boundary_review),
        (ADOPTION_NEGATIVE_CONTROL_REVIEW_PATH, adoption_negative_control_review),
        (HUMAN_DECISION_PACKET_PREP_TARGET_PATH, human_decision_packet_prep_target),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "ADOPTION_PATH_PREP_RECEIPT_CONSUMED",
        "ADOPTION_PATH_REVIEW_TARGET_CONSUMED",
        "SOURCE_BINDING_REVIEW_PASS",
        "ADOPTION_SCOPE_REVIEW_PASS",
        "ADOPTION_SURFACE_INVENTORY_REVIEW_PASS",
        "AUTHORITY_BOUNDARY_REVIEW_PASS",
        "DECISION_SURFACE_MAP_REVIEW_PASS",
        "CANDIDATE_SURFACES_REVIEW_PASS",
        "C8_BOUNDARY_REVIEW_PASS",
        "ADOPTION_NEGATIVE_CONTROL_REVIEW_PASS",
        "HUMAN_DECISION_PACKET_DRAFT_REVIEW_PASS",
        "HUMAN_DECISION_PACKET_PREP_TARGET_EMITTED",
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_review_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_PATH_REVIEW_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "adoption_review_id": adoption_review_id,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "source_adoption_path_prep_receipt_id": ADOPTION_PATH_PREP_RECEIPT_ID,
        "source_adoption_path_prep_receipt_ref": rel(ADOPTION_PATH_PREP_RECEIPT_PATH),
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "ADOPTION_PATH_REVIEW_0_PREP_RECEIPT_CONSUMED": gate == "PASS",
            "ADOPTION_PATH_REVIEW_1_REVIEW_TARGET_CONSUMED": gate == "PASS",
            "ADOPTION_PATH_REVIEW_2_SOURCE_BINDING_REVIEW_PASS": not binding_failures,
            "ADOPTION_PATH_REVIEW_3_SCOPE_REVIEW_PASS": not scope_failures,
            "ADOPTION_PATH_REVIEW_4_SURFACE_INVENTORY_REVIEW_PASS": not inventory_failures,
            "ADOPTION_PATH_REVIEW_5_AUTHORITY_BOUNDARY_REVIEW_PASS": not authority_failures,
            "ADOPTION_PATH_REVIEW_6_DECISION_SURFACE_MAP_REVIEW_PASS": not decision_failures,
            "ADOPTION_PATH_REVIEW_7_CANDIDATE_SURFACES_REVIEW_PASS": not candidate_failures,
            "ADOPTION_PATH_REVIEW_8_C8_BOUNDARY_REVIEW_PASS": not c8_failures,
            "ADOPTION_PATH_REVIEW_9_NEGATIVE_CONTROL_REVIEW_PASS": not negative_failures,
            "ADOPTION_PATH_REVIEW_10_HUMAN_DECISION_PACKET_PREP_TARGET_EMITTED": HUMAN_DECISION_PACKET_PREP_TARGET_PATH.exists() and gate == "PASS",
            "ADOPTION_PATH_REVIEW_11_NO_HUMAN_ADOPTION_DECISION_TAKEN": True,
            "ADOPTION_PATH_REVIEW_12_NO_SELECTED_ADOPTION_DECISION": True,
            "ADOPTION_PATH_REVIEW_13_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "ADOPTION_PATH_REVIEW_14_NO_RUNTIME_PATCH": True,
            "ADOPTION_PATH_REVIEW_15_NO_SCHEMA_ARCHIVE_MUTATION": True,
            "ADOPTION_PATH_REVIEW_16_NO_MOVE_ADDITION": True,
            "ADOPTION_PATH_REVIEW_17_NO_FIXTURE_EXPANSION": True,
            "ADOPTION_PATH_REVIEW_18_NO_T6_LIVE_CASE_EXECUTION": True,
            "ADOPTION_PATH_REVIEW_19_NO_C8_AUTHORIZATION": True,
            "ADOPTION_PATH_REVIEW_20_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_structured_t6_trigger_surface_capability_adoption_path_review_summary": {
            "status": status,
            "adoption_review_id": adoption_review_id,
            "adoption_path_id": ADOPTION_PATH_ID,
            "capability_build_id": CAPABILITY_BUILD_ID,
            "proposal_id": PROPOSAL_ID,
            "required_capability": REQUIRED_CAPABILITY,
            "proposed_surface": PROPOSED_SURFACE,
            "source_adoption_path_prepared": True if gate == "PASS" else False,
            "source_binding_review_pass": not binding_failures,
            "scope_review_pass": not scope_failures,
            "surface_inventory_review_pass": not inventory_failures,
            "authority_boundary_review_pass": not authority_failures,
            "decision_surface_map_review_pass": not decision_failures,
            "candidate_surfaces_review_pass": not candidate_failures,
            "c8_boundary_review_pass": not c8_failures,
            "negative_control_review_pass": not negative_failures,
            "human_decision_packet_draft_review_pass": not draft_failures,
            "adoption_path_review_pass": True if gate == "PASS" else False,
            "human_decision_packet_prep_target_ready": True if gate == "PASS" else False,
            "human_decision_packet_prep_target_id": human_decision_packet_prep_target_id if gate == "PASS" else None,
            "human_adoption_decision_taken": False,
            "selected_adoption_decision": None,
            "future_surfaces_require_separate_human_decision": True if gate == "PASS" else False,
            "runtime_adoption_authorized": False,
            "runtime_patch_authorized": False,
            "schema_archive_mutation_authorized": False,
            "schema_mutation_authorized": False,
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
            "source_binding_review": rel(SOURCE_BINDING_REVIEW_PATH),
            "adoption_scope_review": rel(ADOPTION_SCOPE_REVIEW_PATH),
            "surface_inventory_review": rel(SURFACE_INVENTORY_REVIEW_PATH),
            "authority_boundary_review": rel(AUTHORITY_BOUNDARY_REVIEW_PATH),
            "decision_surface_map_review": rel(DECISION_SURFACE_MAP_REVIEW_PATH),
            "candidate_surfaces_review": rel(CANDIDATE_SURFACES_REVIEW_PATH),
            "c8_boundary_review": rel(C8_BOUNDARY_REVIEW_PATH),
            "adoption_negative_control_review": rel(ADOPTION_NEGATIVE_CONTROL_REVIEW_PATH),
            "human_decision_packet_prep_target": rel(HUMAN_DECISION_PACKET_PREP_TARGET_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_structured_t6_trigger_surface_capability_adoption_path_review_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_structured_t6_trigger_surface_capability_adoption_path_review_receipt_id={receipt_id}")
    print(f"bounded_structured_t6_trigger_surface_capability_adoption_path_review_receipt_path={rel(receipt_path)}")
    print(f"bounded_structured_t6_trigger_surface_capability_adoption_review_id={adoption_review_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_adoption_path_review_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
