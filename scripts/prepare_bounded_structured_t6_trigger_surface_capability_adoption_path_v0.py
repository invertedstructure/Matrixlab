#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_PATH_V0"
TARGET_UNIT_ID = "bounded_structured_t6_trigger_surface_capability.adoption_path_prep_v0"
NEXT_UNIT_ID = "REVIEW_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_PATH_V0"

BUILD_REVIEW_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_build_review_receipt_b8dba552"
CAPABILITY_BUILD_ID = "bounded_structured_t6_trigger_surface_capability_build_721f09dc"
ADOPTION_PATH_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_6f9974e5"
BUILD_AUTHORIZATION_ID = "bounded_structured_t6_trigger_surface_capability_build_auth_c0315976"
IMPLEMENTATION_PATH_ID = "accepted_bounded_capability_implementation_path_defd6d9b"
PROPOSAL_ID = "capability_proposal_57dda6e9"
REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"

BUILD_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_review_receipt_b8dba552.json"
ADOPTION_PATH_PREP_TARGET_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_target_v0.json"

CAPABILITY_PROFILE_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0/bounded_structured_t6_trigger_surface_capability_profile_review_v0.json"
SCHEMA_CANDIDATE_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0/bounded_structured_t6_trigger_surface_capability_schema_candidate_review_v0.json"
EVIDENCE_SHAPE_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0/bounded_structured_t6_trigger_surface_evidence_shape_contract_review_v0.json"
EXAMPLE_PAIR_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0/bounded_structured_t6_trigger_surface_example_pair_review_v0.json"
CLASSIFIER_POLICY_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0/bounded_structured_t6_trigger_surface_classifier_policy_review_v0.json"
API_CONTRACT_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0/bounded_structured_t6_trigger_surface_capability_api_contract_review_v0.json"
TEST_EXPECTATIONS_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0/bounded_structured_t6_trigger_surface_capability_test_expectations_review_v0.json"
NEGATIVE_CONTROL_REVIEW_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0/bounded_structured_t6_trigger_surface_capability_negative_control_review_v0.json"

BUILD_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079.json"
CAPABILITY_PROFILE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_profile_v0.json"
SCHEMA_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_schema_candidate_v0.json"
CLASSIFIER_POLICY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_classifier_policy_v0.json"
API_CONTRACT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_api_contract_v0.json"

IMPLEMENTATION_PATH_REVIEW_RECEIPT_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0_receipts/accepted_bounded_capability_implementation_path_review_receipt_e4b4e2d7.json"
BUILD_AUTHORIZATION_TARGET_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0/bounded_structured_t6_trigger_surface_capability_build_authorization_target_v0.json"

PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"

OUT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0"
RECEIPT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_basis_v0.json"
SOURCE_REVIEW_BINDING_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_source_review_binding_v0.json"
ADOPTION_SCOPE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_scope_v0.json"
ADOPTION_SURFACE_INVENTORY_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_surface_inventory_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_authority_boundary_v0.json"
DECISION_SURFACE_MAP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_decision_surface_map_v0.json"
RUNTIME_ADOPTION_CANDIDATE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_runtime_adoption_candidate_v0.json"
SCHEMA_PROMOTION_CANDIDATE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_candidate_v0.json"
MOVE_REGISTRY_CANDIDATE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_move_registry_candidate_v0.json"
FIXTURE_EXPANSION_CANDIDATE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_fixture_expansion_candidate_v0.json"
T6_LIVE_CASE_CANDIDATE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_t6_live_case_candidate_v0.json"
C8_BOUNDARY_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_c8_boundary_v0.json"
ADOPTION_NEGATIVE_CONTROL_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_negative_control_v0.json"
HUMAN_DECISION_PACKET_DRAFT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_draft_v0.json"
ADOPTION_PATH_REVIEW_TARGET_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_review_target_v0.json"
READOUT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_transition_trace.json"

FUTURE_SURFACES = [
    "runtime adoption",
    "schema archive promotion",
    "move registry addition",
    "fixture/test expansion",
    "T6 live-case execution",
]

FORBIDDEN_NOW = [
    "runtime adoption",
    "runtime patch",
    "schema archive mutation",
    "schema mutation",
    "move registry addition",
    "fixture expansion",
    "T6 live case execution",
    "C8 authorization",
    "hidden next command",
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

def lower_list(xs: Any) -> List[str]:
    return [str(x).lower() for x in (xs or [])]

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        BUILD_REVIEW_RECEIPT_PATH,
        ADOPTION_PATH_PREP_TARGET_PATH,
        CAPABILITY_PROFILE_REVIEW_PATH,
        SCHEMA_CANDIDATE_REVIEW_PATH,
        EVIDENCE_SHAPE_REVIEW_PATH,
        EXAMPLE_PAIR_REVIEW_PATH,
        CLASSIFIER_POLICY_REVIEW_PATH,
        API_CONTRACT_REVIEW_PATH,
        TEST_EXPECTATIONS_REVIEW_PATH,
        NEGATIVE_CONTROL_REVIEW_PATH,
        BUILD_RECEIPT_PATH,
        CAPABILITY_PROFILE_PATH,
        SCHEMA_CANDIDATE_PATH,
        CLASSIFIER_POLICY_PATH,
        API_CONTRACT_PATH,
        IMPLEMENTATION_PATH_REVIEW_RECEIPT_PATH,
        BUILD_AUTHORIZATION_TARGET_PATH,
        PROPOSAL_PATH,
        STOP_PACKET_PATH,
    ]

    failures: List[str] = []

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    build_review_receipt = read_json(BUILD_REVIEW_RECEIPT_PATH)
    adoption_target = read_json(ADOPTION_PATH_PREP_TARGET_PATH)
    profile_review = read_json(CAPABILITY_PROFILE_REVIEW_PATH)
    schema_review = read_json(SCHEMA_CANDIDATE_REVIEW_PATH)
    evidence_review = read_json(EVIDENCE_SHAPE_REVIEW_PATH)
    example_review = read_json(EXAMPLE_PAIR_REVIEW_PATH)
    classifier_review = read_json(CLASSIFIER_POLICY_REVIEW_PATH)
    api_review = read_json(API_CONTRACT_REVIEW_PATH)
    test_review = read_json(TEST_EXPECTATIONS_REVIEW_PATH)
    negative_review = read_json(NEGATIVE_CONTROL_REVIEW_PATH)

    build_receipt = read_json(BUILD_RECEIPT_PATH)
    capability_profile = read_json(CAPABILITY_PROFILE_PATH)
    schema_candidate = read_json(SCHEMA_CANDIDATE_PATH)
    classifier_policy = read_json(CLASSIFIER_POLICY_PATH)
    api_contract = read_json(API_CONTRACT_PATH)

    implementation_review_receipt = read_json(IMPLEMENTATION_PATH_REVIEW_RECEIPT_PATH)
    build_authorization_target = read_json(BUILD_AUTHORIZATION_TARGET_PATH)
    proposal = read_json(PROPOSAL_PATH)
    stop_packet = read_json(STOP_PACKET_PATH)

    build_review_summary = build_review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_review_summary", {})
    build_summary = build_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_summary", {})
    implementation_review_summary = implementation_review_receipt.get("machine_readable_accepted_bounded_capability_proposal_implementation_path_review_summary", {})

    if build_review_receipt.get("receipt_id") != BUILD_REVIEW_RECEIPT_ID:
        failures.append(f"build_review_receipt_id_wrong:{build_review_receipt.get('receipt_id')}")
    if build_review_receipt.get("gate") != "PASS":
        failures.append("build_review_receipt_gate_not_pass")
    if build_review_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"build_review_receipt_terminal_next_wrong:{build_review_receipt.get('terminal', {}).get('next_unit_id')}")

    for key in [
        "artifact_review_pass",
        "profile_review_pass",
        "schema_candidate_review_pass",
        "evidence_shape_review_pass",
        "example_pair_review_pass",
        "classifier_policy_review_pass",
        "api_contract_review_pass",
        "test_expectations_review_pass",
        "negative_control_review_pass",
        "adoption_path_prep_target_ready",
    ]:
        if build_review_summary.get(key) is not True:
            failures.append(f"build_review_summary_{key}_not_true:{build_review_summary.get(key)}")

    if build_review_summary.get("adoption_path_id") != ADOPTION_PATH_ID:
        failures.append(f"adoption_path_id_wrong:{build_review_summary.get('adoption_path_id')}")
    if build_review_summary.get("capability_build_id") != CAPABILITY_BUILD_ID:
        failures.append(f"capability_build_id_wrong:{build_review_summary.get('capability_build_id')}")
    if build_review_summary.get("build_authorization_id") != BUILD_AUTHORIZATION_ID:
        failures.append(f"build_authorization_id_wrong:{build_review_summary.get('build_authorization_id')}")
    if build_review_summary.get("implementation_path_id") != IMPLEMENTATION_PATH_ID:
        failures.append(f"implementation_path_id_wrong:{build_review_summary.get('implementation_path_id')}")

    for key in [
        "runtime_adoption_authorized",
        "runtime_patch_authorized",
        "schema_archive_mutation_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "t6_live_case_execution_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(build_review_summary, key, failures, "build_review_summary")

    if adoption_target.get("target_status") != "READY":
        failures.append(f"adoption_target_status_wrong:{adoption_target.get('target_status')}")
    if adoption_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"adoption_target_next_wrong:{adoption_target.get('next_unit_id')}")
    if adoption_target.get("adoption_path_id") != ADOPTION_PATH_ID:
        failures.append("adoption_target_path_id_wrong")
    if adoption_target.get("future_surfaces_require_separate_human_decision") is not True:
        failures.append("adoption_target_future_surfaces_do_not_require_human_decision")

    target_no_auth = lower_list(adoption_target.get("this_target_does_not_authorize"))
    for phrase in [
        "runtime adoption",
        "runtime patch",
        "schema archive mutation",
        "move registry addition",
        "fixture expansion",
        "t6 live case execution",
        "c8 authorization",
    ]:
        if phrase not in target_no_auth:
            failures.append(f"adoption_target_no_authorize_missing:{phrase}")

    for name, obj in [
        ("profile_review", profile_review),
        ("schema_review", schema_review),
        ("evidence_review", evidence_review),
        ("example_review", example_review),
        ("classifier_review", classifier_review),
        ("api_review", api_review),
        ("test_review", test_review),
        ("negative_review", negative_review),
    ]:
        if obj.get("review_status") != "PASS":
            failures.append(f"{name}_not_pass:{obj.get('review_status')}:{obj.get('failures')}")

    if build_summary.get("build_executed") is not True:
        failures.append("source_build_not_executed")
    if build_summary.get("build_review_target_ready") is not True:
        failures.append("source_build_review_target_not_ready")
    if implementation_review_summary.get("bounded_build_unit_authorized") is not True:
        failures.append("implementation_review_did_not_authorize_build")
    if build_authorization_target.get("bounded_build_unit_authorized") is not True:
        failures.append("build_authorization_target_not_authorized")

    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal.get("required_capability") != REQUIRED_CAPABILITY:
        failures.append(f"proposal_required_capability_wrong:{proposal.get('required_capability')}")
    if proposal.get("proposed_surface") != PROPOSED_SURFACE:
        failures.append(f"proposal_surface_wrong:{proposal.get('proposed_surface')}")
    if stop_packet.get("stop_code") != "STOP_CAPABILITY_LAYER_REQUIRED":
        failures.append(f"source_stop_code_wrong:{stop_packet.get('stop_code')}")

    # Source artifact sanity checks.
    if capability_profile.get("capability_name") != REQUIRED_CAPABILITY:
        failures.append("capability_profile_name_wrong")
    if capability_profile.get("surface_name") != PROPOSED_SURFACE:
        failures.append("capability_profile_surface_wrong")
    if schema_candidate.get("schema_candidate_status") != "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION":
        failures.append("schema_candidate_not_candidate_only")
    if schema_candidate.get("archive_mutation_authorized") is not False:
        failures.append("source_schema_candidate_archive_mutation_authorized_unexpected")
    if schema_candidate.get("runtime_adoption_authorized") is not False:
        failures.append("source_schema_candidate_runtime_adoption_authorized_unexpected")
    if api_contract.get("api_kind") != "representation_contract_only":
        failures.append("api_contract_kind_wrong")
    if classifier_policy.get("policy_status") != "BUILT_PENDING_REVIEW":
        failures.append("classifier_policy_status_wrong")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_PATH_PREP_PASS_REVIEW_READY"
        if gate == "PASS"
        else "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_PATH_PREP_GATE_FAIL"
    )

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_basis_v0",
        "unit_id": UNIT_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_build_review_receipt_id": BUILD_REVIEW_RECEIPT_ID,
        "source_capability_build_id": CAPABILITY_BUILD_ID,
        "source_build_authorization_id": BUILD_AUTHORIZATION_ID,
        "source_proposal_id": PROPOSAL_ID,
        "prep_claim": "Prepare adoption/promotion decision path only. Do not adopt into runtime, patch runtime, mutate schema archive, add moves, expand fixtures, execute T6 live case, authorize C8, or create hidden next command.",
        "source_file_hashes": source_hashes,
    }

    source_review_binding = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_source_review_binding_v0",
        "adoption_path_id": ADOPTION_PATH_ID,
        "binding_status": "PASS" if gate == "PASS" else "FAIL",
        "capability_build_id": CAPABILITY_BUILD_ID,
        "build_receipt_id": build_receipt.get("receipt_id"),
        "build_review_receipt_id": build_review_receipt.get("receipt_id"),
        "artifact_review_pass": build_review_summary.get("artifact_review_pass"),
        "reviewed_artifact_refs": {
            "capability_profile": rel(CAPABILITY_PROFILE_PATH),
            "schema_candidate": rel(SCHEMA_CANDIDATE_PATH),
            "classifier_policy": rel(CLASSIFIER_POLICY_PATH),
            "api_contract": rel(API_CONTRACT_PATH),
        },
    }

    adoption_scope = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_scope_v0",
        "adoption_path_id": ADOPTION_PATH_ID,
        "scope_status": "READY_FOR_REVIEW" if gate == "PASS" else "BLOCKED",
        "capability_build_id": CAPABILITY_BUILD_ID,
        "required_capability": REQUIRED_CAPABILITY,
        "proposed_surface": PROPOSED_SURFACE,
        "path_scope": "Prepare decision surfaces for possible future adoption or promotion of reviewed bounded capability artifacts.",
        "in_scope_for_this_unit": [
            "inventory possible future adoption/promotion surfaces",
            "define authority boundaries",
            "prepare candidate decision surfaces",
            "prepare review target",
            "keep every actual adoption/promotion authority false",
        ],
        "not_in_scope_for_this_unit": FORBIDDEN_NOW,
    }

    adoption_surface_inventory = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_surface_inventory_v0",
        "adoption_path_id": ADOPTION_PATH_ID,
        "inventory_status": "READY_FOR_REVIEW" if gate == "PASS" else "BLOCKED",
        "future_surfaces": [
            {
                "surface": "runtime adoption",
                "surface_id": "runtime_adoption_surface_v0",
                "requires_separate_human_decision": True,
                "authorized_now": False,
            },
            {
                "surface": "schema archive promotion",
                "surface_id": "schema_archive_promotion_surface_v0",
                "requires_separate_human_decision": True,
                "authorized_now": False,
            },
            {
                "surface": "move registry addition",
                "surface_id": "move_registry_addition_surface_v0",
                "requires_separate_human_decision": True,
                "authorized_now": False,
            },
            {
                "surface": "fixture/test expansion",
                "surface_id": "fixture_test_expansion_surface_v0",
                "requires_separate_human_decision": True,
                "authorized_now": False,
            },
            {
                "surface": "T6 live-case execution",
                "surface_id": "t6_live_case_execution_surface_v0",
                "requires_separate_human_decision": True,
                "authorized_now": False,
            },
        ],
        "c8_surface_status": "OUT_OF_SCOPE_NOT_AUTHORIZED",
    }

    authority_boundary = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_authority_boundary_v0",
        "adoption_path_id": ADOPTION_PATH_ID,
        "boundary_status": "READY_FOR_REVIEW" if gate == "PASS" else "BLOCKED",
        "future_surfaces_require_separate_human_decision": True,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "boundary_rule": "This path prep unit can prepare decision surfaces only. It cannot choose or apply any adoption/promotion action.",
    }

    decision_surface_map = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_decision_surface_map_v0",
        "adoption_path_id": ADOPTION_PATH_ID,
        "map_status": "READY_FOR_REVIEW" if gate == "PASS" else "BLOCKED",
        "candidate_decisions": [
            "PREPARE_RUNTIME_ADOPTION_DECISION_PACKET",
            "PREPARE_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET",
            "PREPARE_MOVE_REGISTRY_ADDITION_DECISION_PACKET",
            "PREPARE_FIXTURE_TEST_EXPANSION_DECISION_PACKET",
            "PREPARE_T6_LIVE_CASE_EXECUTION_DECISION_PACKET",
            "DEFER_ADOPTION_PATH",
            "FREEZE_CAPABILITY_AS_REFERENCE_ONLY",
            "CLOSE_ADOPTION_PATH_NO_ADOPTION",
        ],
        "decision_rule": "Each non-defer/non-close decision prepares a separate human decision packet. None is selected by this prep unit.",
        "selected_decision": None,
    }

    runtime_adoption_candidate = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_runtime_adoption_candidate_v0",
        "adoption_path_id": ADOPTION_PATH_ID,
        "candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED",
        "candidate_surface": "runtime adoption",
        "source_artifact_refs": [
            rel(CAPABILITY_PROFILE_PATH),
            rel(CLASSIFIER_POLICY_PATH),
            rel(API_CONTRACT_PATH),
        ],
        "required_before_authorization": [
            "review adoption path",
            "prepare explicit runtime adoption decision packet",
            "human accepts runtime adoption",
            "emit runtime adoption build target",
            "run negative controls",
        ],
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
    }

    schema_promotion_candidate = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_candidate_v0",
        "adoption_path_id": ADOPTION_PATH_ID,
        "candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED",
        "candidate_surface": "schema archive promotion",
        "source_schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "required_before_authorization": [
            "review adoption path",
            "prepare explicit schema archive promotion decision packet",
            "human accepts schema promotion",
            "emit schema archive mutation target",
            "verify archive namespace and collision rules",
        ],
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
    }

    move_registry_candidate = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_move_registry_candidate_v0",
        "adoption_path_id": ADOPTION_PATH_ID,
        "candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED",
        "candidate_surface": "move registry addition",
        "candidate_move_kind": "bounded_structured_t6_trigger_surface_classification_move",
        "required_before_authorization": [
            "review adoption path",
            "prepare explicit move registry addition decision packet",
            "human accepts move addition",
            "emit move registry mutation target",
            "verify no hidden runtime adoption",
        ],
        "move_addition_authorized": False,
    }

    fixture_expansion_candidate = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_fixture_expansion_candidate_v0",
        "adoption_path_id": ADOPTION_PATH_ID,
        "candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED",
        "candidate_surface": "fixture/test expansion",
        "source_examples": [
            "positive structured trigger/tie evidence example",
            "text-only tie residue negative control",
        ],
        "required_before_authorization": [
            "review adoption path",
            "prepare explicit fixture/test expansion decision packet",
            "human accepts fixture expansion",
            "emit fixture expansion target",
            "verify example-only artifacts do not silently become fixtures",
        ],
        "fixture_expansion_authorized": False,
    }

    t6_live_case_candidate = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_t6_live_case_candidate_v0",
        "adoption_path_id": ADOPTION_PATH_ID,
        "candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED",
        "candidate_surface": "T6 live-case execution",
        "required_before_authorization": [
            "review adoption path",
            "prepare explicit T6 live-case execution decision packet",
            "human accepts live-case execution",
            "emit bounded live-case execution target",
            "verify runtime/adoption prerequisites are satisfied",
        ],
        "t6_live_case_execution_authorized": False,
    }

    c8_boundary = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_c8_boundary_v0",
        "adoption_path_id": ADOPTION_PATH_ID,
        "boundary_status": "CLOSED",
        "c8_authorized": False,
        "c8_discussion_authorized": False,
        "reason": "C8 remains outside this bounded T6 capability adoption-path prep unit.",
    }

    adoption_negative_control = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_negative_control_v0",
        "adoption_path_id": ADOPTION_PATH_ID,
        "negative_control_status": "PASS" if gate == "PASS" else "BLOCKED",
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
        "negative_control_rule": "Preparing candidate decision surfaces is not the same as adopting/promoting them.",
    }

    human_decision_packet_draft = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_draft_v0",
        "adoption_path_id": ADOPTION_PATH_ID,
        "draft_status": "DRAFT_ONLY_NOT_REVIEWED" if gate == "PASS" else "BLOCKED",
        "decision_required_later": True,
        "selected_decision": None,
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
        "draft_rule": "This draft is not a human decision packet yet. It becomes decision-ready only after adoption path review.",
    }

    adoption_path_review_target = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_review_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "build_review_receipt_id": BUILD_REVIEW_RECEIPT_ID,
        "proposal_id": PROPOSAL_ID,
        "review_scope": "Review adoption-path prep artifacts and decide whether to prepare a human decision packet for one or more future adoption/promotion surfaces.",
        "review_inputs": [
            rel(ADOPTION_SCOPE_PATH),
            rel(ADOPTION_SURFACE_INVENTORY_PATH),
            rel(AUTHORITY_BOUNDARY_PATH),
            rel(DECISION_SURFACE_MAP_PATH),
            rel(RUNTIME_ADOPTION_CANDIDATE_PATH),
            rel(SCHEMA_PROMOTION_CANDIDATE_PATH),
            rel(MOVE_REGISTRY_CANDIDATE_PATH),
            rel(FIXTURE_EXPANSION_CANDIDATE_PATH),
            rel(T6_LIVE_CASE_CANDIDATE_PATH),
            rel(C8_BOUNDARY_PATH),
            rel(ADOPTION_NEGATIVE_CONTROL_PATH),
        ],
        "does_not_authorize_runtime_adoption": True,
        "does_not_authorize_schema_archive_mutation": True,
        "does_not_authorize_move_addition": True,
        "does_not_authorize_fixture_expansion": True,
        "does_not_authorize_t6_live_case_execution": True,
        "does_not_authorize_c8": True,
    }

    rollup = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "source_build_review_pass": True if gate == "PASS" else False,
        "adoption_path_prepared": True if gate == "PASS" else False,
        "adoption_path_review_target_ready": True if gate == "PASS" else False,
        "future_surfaces_require_separate_human_decision": True if gate == "PASS" else False,
        "runtime_adoption_candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED" if gate == "PASS" else "BLOCKED",
        "schema_promotion_candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED" if gate == "PASS" else "BLOCKED",
        "move_registry_candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED" if gate == "PASS" else "BLOCKED",
        "fixture_expansion_candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED" if gate == "PASS" else "BLOCKED",
        "t6_live_case_candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED" if gate == "PASS" else "BLOCKED",
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_readout_v0",
        "status": status,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "interpretation": "Adoption/promotion decision path prepared for review. No runtime adoption, runtime patch, schema archive mutation, move addition, fixture expansion, T6 live execution, hidden next command, or C8 authorization occurred."
        if gate == "PASS" else "Adoption path prep failed typed gates.",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_profile_v0",
        "profile_status": status,
        "adoption_path_id": ADOPTION_PATH_ID,
        "core_rule": "Prepare adoption path only. Every actual adoption/promotion surface remains candidate-only and requires later human decision.",
        "adoption_path_review_target_ref": rel(ADOPTION_PATH_REVIEW_TARGET_PATH),
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "prep_result": "ADOPTION_PATH_PREPARED_FOR_REVIEW" if gate == "PASS" else "ADOPTION_PATH_PREP_GATE_FAIL",
            "adoption_path_id": ADOPTION_PATH_ID,
            "capability_build_id": CAPABILITY_BUILD_ID,
            "proposal_id": PROPOSAL_ID,
            "future_surfaces": FUTURE_SURFACES,
            "future_surfaces_require_separate_human_decision": True if gate == "PASS" else False,
            "adoption_path_review_target_ready": True if gate == "PASS" else False,
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_transition_trace_v0",
        "unit_id": UNIT_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "transitions": [
            {
                "from": "ADOPTION_PATH_PREP_READY",
                "edge": "prepare adoption surfaces, authority boundary, candidates, negative control, and review target",
                "to": "ADOPTION_PATH_PREPARED_FOR_REVIEW" if gate == "PASS" else "ADOPTION_PATH_PREP_GATE_FAIL",
            },
            {
                "from": "ADOPTION_PATH_PREPARED_FOR_REVIEW" if gate == "PASS" else "ADOPTION_PATH_PREP_GATE_FAIL",
                "edge": "emit adoption path review target without adoption or promotion",
                "to": "ADOPTION_PATH_REVIEW_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_PATH_PREP_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (SOURCE_REVIEW_BINDING_PATH, source_review_binding),
        (ADOPTION_SCOPE_PATH, adoption_scope),
        (ADOPTION_SURFACE_INVENTORY_PATH, adoption_surface_inventory),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (DECISION_SURFACE_MAP_PATH, decision_surface_map),
        (RUNTIME_ADOPTION_CANDIDATE_PATH, runtime_adoption_candidate),
        (SCHEMA_PROMOTION_CANDIDATE_PATH, schema_promotion_candidate),
        (MOVE_REGISTRY_CANDIDATE_PATH, move_registry_candidate),
        (FIXTURE_EXPANSION_CANDIDATE_PATH, fixture_expansion_candidate),
        (T6_LIVE_CASE_CANDIDATE_PATH, t6_live_case_candidate),
        (C8_BOUNDARY_PATH, c8_boundary),
        (ADOPTION_NEGATIVE_CONTROL_PATH, adoption_negative_control),
        (HUMAN_DECISION_PACKET_DRAFT_PATH, human_decision_packet_draft),
        (ADOPTION_PATH_REVIEW_TARGET_PATH, adoption_path_review_target),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "BUILD_REVIEW_RECEIPT_CONSUMED",
        "ADOPTION_PATH_PREP_TARGET_CONSUMED",
        "SOURCE_ARTIFACT_REVIEWS_BOUND",
        "ADOPTION_SURFACE_INVENTORY_EMITTED",
        "AUTHORITY_BOUNDARY_EMITTED",
        "DECISION_SURFACE_MAP_EMITTED",
        "RUNTIME_ADOPTION_CANDIDATE_EMITTED_NOT_AUTHORIZED",
        "SCHEMA_PROMOTION_CANDIDATE_EMITTED_NOT_AUTHORIZED",
        "MOVE_REGISTRY_CANDIDATE_EMITTED_NOT_AUTHORIZED",
        "FIXTURE_EXPANSION_CANDIDATE_EMITTED_NOT_AUTHORIZED",
        "T6_LIVE_CASE_CANDIDATE_EMITTED_NOT_AUTHORIZED",
        "C8_BOUNDARY_CLOSED",
        "ADOPTION_NEGATIVE_CONTROL_PASS",
        "HUMAN_DECISION_PACKET_DRAFT_EMITTED_NOT_DECISION_READY",
        "ADOPTION_PATH_REVIEW_TARGET_EMITTED",
        "NO_RUNTIME_REPAIR",
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_PATH_PREP_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "source_build_review_receipt_id": BUILD_REVIEW_RECEIPT_ID,
        "source_build_review_receipt_ref": rel(BUILD_REVIEW_RECEIPT_PATH),
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "ADOPTION_PATH_PREP_0_BUILD_REVIEW_RECEIPT_CONSUMED": gate == "PASS",
            "ADOPTION_PATH_PREP_1_ADOPTION_TARGET_CONSUMED": gate == "PASS",
            "ADOPTION_PATH_PREP_2_SOURCE_ARTIFACT_REVIEWS_PASS": build_review_summary.get("artifact_review_pass") is True,
            "ADOPTION_PATH_PREP_3_SURFACE_INVENTORY_EMITTED": ADOPTION_SURFACE_INVENTORY_PATH.exists() and gate == "PASS",
            "ADOPTION_PATH_PREP_4_AUTHORITY_BOUNDARY_EMITTED": AUTHORITY_BOUNDARY_PATH.exists() and gate == "PASS",
            "ADOPTION_PATH_PREP_5_DECISION_SURFACE_MAP_EMITTED": DECISION_SURFACE_MAP_PATH.exists() and gate == "PASS",
            "ADOPTION_PATH_PREP_6_NEGATIVE_CONTROL_EMITTED": ADOPTION_NEGATIVE_CONTROL_PATH.exists() and gate == "PASS",
            "ADOPTION_PATH_PREP_7_REVIEW_TARGET_EMITTED": ADOPTION_PATH_REVIEW_TARGET_PATH.exists() and gate == "PASS",
            "ADOPTION_PATH_PREP_8_FUTURE_SURFACES_REQUIRE_SEPARATE_HUMAN_DECISION": True,
            "ADOPTION_PATH_PREP_9_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "ADOPTION_PATH_PREP_10_NO_RUNTIME_PATCH": True,
            "ADOPTION_PATH_PREP_11_NO_SCHEMA_ARCHIVE_MUTATION": True,
            "ADOPTION_PATH_PREP_12_NO_MOVE_ADDITION": True,
            "ADOPTION_PATH_PREP_13_NO_FIXTURE_EXPANSION": True,
            "ADOPTION_PATH_PREP_14_NO_T6_LIVE_CASE_EXECUTION": True,
            "ADOPTION_PATH_PREP_15_NO_C8_AUTHORIZATION": True,
            "ADOPTION_PATH_PREP_16_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_structured_t6_trigger_surface_capability_adoption_path_prep_summary": {
            "status": status,
            "adoption_path_id": ADOPTION_PATH_ID,
            "capability_build_id": CAPABILITY_BUILD_ID,
            "build_review_receipt_id": BUILD_REVIEW_RECEIPT_ID,
            "proposal_id": PROPOSAL_ID,
            "required_capability": REQUIRED_CAPABILITY,
            "proposed_surface": PROPOSED_SURFACE,
            "source_build_review_pass": True if gate == "PASS" else False,
            "adoption_path_prepared": True if gate == "PASS" else False,
            "adoption_path_review_target_ready": True if gate == "PASS" else False,
            "future_surfaces": FUTURE_SURFACES,
            "future_surfaces_require_separate_human_decision": True if gate == "PASS" else False,
            "human_adoption_decision_taken": False,
            "selected_adoption_decision": None,
            "runtime_adoption_candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED" if gate == "PASS" else "BLOCKED",
            "schema_promotion_candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED" if gate == "PASS" else "BLOCKED",
            "move_registry_candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED" if gate == "PASS" else "BLOCKED",
            "fixture_expansion_candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED" if gate == "PASS" else "BLOCKED",
            "t6_live_case_candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED" if gate == "PASS" else "BLOCKED",
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
            "source_review_binding": rel(SOURCE_REVIEW_BINDING_PATH),
            "adoption_scope": rel(ADOPTION_SCOPE_PATH),
            "adoption_surface_inventory": rel(ADOPTION_SURFACE_INVENTORY_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "decision_surface_map": rel(DECISION_SURFACE_MAP_PATH),
            "runtime_adoption_candidate": rel(RUNTIME_ADOPTION_CANDIDATE_PATH),
            "schema_promotion_candidate": rel(SCHEMA_PROMOTION_CANDIDATE_PATH),
            "move_registry_candidate": rel(MOVE_REGISTRY_CANDIDATE_PATH),
            "fixture_expansion_candidate": rel(FIXTURE_EXPANSION_CANDIDATE_PATH),
            "t6_live_case_candidate": rel(T6_LIVE_CASE_CANDIDATE_PATH),
            "c8_boundary": rel(C8_BOUNDARY_PATH),
            "adoption_negative_control": rel(ADOPTION_NEGATIVE_CONTROL_PATH),
            "human_decision_packet_draft": rel(HUMAN_DECISION_PACKET_DRAFT_PATH),
            "adoption_path_review_target": rel(ADOPTION_PATH_REVIEW_TARGET_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_structured_t6_trigger_surface_capability_adoption_path_prep_receipt_id={receipt_id}")
    print(f"bounded_structured_t6_trigger_surface_capability_adoption_path_prep_receipt_path={rel(receipt_path)}")
    print(f"bounded_structured_t6_trigger_surface_capability_adoption_path_id={ADOPTION_PATH_ID if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_adoption_path_prep_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
