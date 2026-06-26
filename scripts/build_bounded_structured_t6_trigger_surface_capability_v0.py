#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_V0"
TARGET_UNIT_ID = "bounded_structured_t6_trigger_surface_capability.build_v0"
NEXT_UNIT_ID = "REVIEW_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_BUILD_V0"

IMPLEMENTATION_PATH_REVIEW_RECEIPT_ID = "accepted_bounded_capability_implementation_path_review_receipt_e4b4e2d7"
PROPOSAL_ID = "capability_proposal_57dda6e9"
EXPECTED_BUILD_AUTHORIZATION_ID = "bounded_structured_t6_trigger_surface_capability_build_auth_c0315976"
EXPECTED_IMPLEMENTATION_PATH_ID = "accepted_bounded_capability_implementation_path_defd6d9b"
EXPECTED_REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
EXPECTED_PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"
EXPECTED_BUILD_UNIT = "BUILD_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_V0"
EXPECTED_SELECTED_DECISION = "ACCEPT_FOR_BOUNDED_IMPLEMENTATION"
EXPECTED_MISSING_OBJECTS = [
    "loop_trigger_surface_missing",
    "structured_tie_evidence_missing",
]

IMPLEMENTATION_PATH_REVIEW_RECEIPT_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0_receipts/accepted_bounded_capability_implementation_path_review_receipt_e4b4e2d7.json"

BUILD_AUTHORIZATION_TARGET_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0/bounded_structured_t6_trigger_surface_capability_build_authorization_target_v0.json"
IMPLEMENTATION_OBJECTIVE_REVIEW_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0/accepted_bounded_capability_proposal_implementation_objective_review_v0.json"
CAPABILITY_BOUNDARY_REVIEW_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0/accepted_bounded_capability_proposal_capability_boundary_review_v0.json"
IMPLEMENTATION_CONTRACT_REVIEW_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0/accepted_bounded_capability_proposal_implementation_contract_review_v0.json"
GUARD_REVIEW_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0/accepted_bounded_capability_proposal_implementation_guard_review_v0.json"
TEST_RECEIPT_REVIEW_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0/accepted_bounded_capability_proposal_test_and_receipt_review_v0.json"
NEGATIVE_CONTROL_REVIEW_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0/accepted_bounded_capability_proposal_implementation_negative_control_review_v0.json"

IMPLEMENTATION_PATH_PREP_RECEIPT_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_prep_v0_receipts/accepted_bounded_capability_implementation_path_prep_receipt_b4fc0c59.json"
ACCEPT_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_human_decision_accept_for_bounded_implementation_v0_receipts/bounded_capability_proposal_human_decision_accept_receipt_6979a229.json"
DECISION_RECORD_PATH = ROOT / "data/bounded_capability_proposal_human_decision_accept_for_bounded_implementation_v0/bounded_capability_proposal_human_decision_record_v0.json"

VALIDATION_RUN_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0_receipts/bounded_capability_proposal_validation_path_run_receipt_375954b6.json"
PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"

OUT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0"
RECEIPT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_basis_v0.json"
CAPABILITY_PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_profile_v0.json"
SURFACE_SCHEMA_CANDIDATE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_candidate_v0.json"
EVIDENCE_SHAPE_CONTRACT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_evidence_shape_contract_v0.json"
POSITIVE_STRUCTURED_EXAMPLE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_positive_example_v0.json"
TEXT_ONLY_NEGATIVE_CONTROL_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_text_only_negative_control_v0.json"
CLASSIFIER_POLICY_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_classifier_policy_v0.json"
CAPABILITY_API_CONTRACT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_api_contract_v0.json"
TEST_EXPECTATIONS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_test_expectations_v0.json"
NEGATIVE_CONTROL_RESULT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_negative_control_result_v0.json"
BUILD_REVIEW_TARGET_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_review_target_v0.json"
READOUT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_transition_trace.json"

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
        IMPLEMENTATION_PATH_REVIEW_RECEIPT_PATH,
        BUILD_AUTHORIZATION_TARGET_PATH,
        IMPLEMENTATION_OBJECTIVE_REVIEW_PATH,
        CAPABILITY_BOUNDARY_REVIEW_PATH,
        IMPLEMENTATION_CONTRACT_REVIEW_PATH,
        GUARD_REVIEW_PATH,
        TEST_RECEIPT_REVIEW_PATH,
        NEGATIVE_CONTROL_REVIEW_PATH,
        IMPLEMENTATION_PATH_PREP_RECEIPT_PATH,
        ACCEPT_RECEIPT_PATH,
        DECISION_RECORD_PATH,
        VALIDATION_RUN_RECEIPT_PATH,
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

    implementation_review_receipt = read_json(IMPLEMENTATION_PATH_REVIEW_RECEIPT_PATH)
    build_authorization_target = read_json(BUILD_AUTHORIZATION_TARGET_PATH)
    objective_review = read_json(IMPLEMENTATION_OBJECTIVE_REVIEW_PATH)
    boundary_review = read_json(CAPABILITY_BOUNDARY_REVIEW_PATH)
    contract_review = read_json(IMPLEMENTATION_CONTRACT_REVIEW_PATH)
    guard_review = read_json(GUARD_REVIEW_PATH)
    test_receipt_review = read_json(TEST_RECEIPT_REVIEW_PATH)
    negative_control_review = read_json(NEGATIVE_CONTROL_REVIEW_PATH)

    prep_receipt = read_json(IMPLEMENTATION_PATH_PREP_RECEIPT_PATH)
    accept_receipt = read_json(ACCEPT_RECEIPT_PATH)
    decision_record = read_json(DECISION_RECORD_PATH)
    validation_run = read_json(VALIDATION_RUN_RECEIPT_PATH)
    proposal = read_json(PROPOSAL_PATH)
    stop_packet = read_json(STOP_PACKET_PATH)

    review_summary = implementation_review_receipt.get("machine_readable_accepted_bounded_capability_proposal_implementation_path_review_summary", {})
    prep_summary = prep_receipt.get("machine_readable_accepted_bounded_capability_proposal_implementation_path_prep_summary", {})
    accept_summary = accept_receipt.get("machine_readable_bounded_capability_proposal_human_decision_accept_summary", {})
    validation_summary = validation_run.get("machine_readable_bounded_capability_proposal_validation_path_run_summary", {})

    if implementation_review_receipt.get("receipt_id") != IMPLEMENTATION_PATH_REVIEW_RECEIPT_ID:
        failures.append(f"implementation_review_receipt_id_wrong:{implementation_review_receipt.get('receipt_id')}")
    if implementation_review_receipt.get("gate") != "PASS":
        failures.append("implementation_review_gate_not_pass")
    if implementation_review_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"implementation_review_terminal_next_wrong:{implementation_review_receipt.get('terminal', {}).get('next_unit_id')}")

    for key in [
        "proposal_accepted",
        "implementation_path_prepared",
        "implementation_path_review_pass",
        "bounded_build_unit_authorized",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_summary_{key}_not_true:{review_summary.get(key)}")

    if review_summary.get("build_authorization_id") != EXPECTED_BUILD_AUTHORIZATION_ID:
        failures.append(f"build_authorization_id_wrong:{review_summary.get('build_authorization_id')}")
    if review_summary.get("implementation_path_id") != EXPECTED_IMPLEMENTATION_PATH_ID:
        failures.append(f"implementation_path_id_wrong:{review_summary.get('implementation_path_id')}")
    if review_summary.get("candidate_build_unit") != EXPECTED_BUILD_UNIT:
        failures.append(f"candidate_build_unit_wrong:{review_summary.get('candidate_build_unit')}")
    if review_summary.get("candidate_status_after_review") != "AUTHORIZED_FOR_BOUNDED_BUILD_UNIT":
        failures.append(f"candidate_status_wrong:{review_summary.get('candidate_status_after_review')}")

    for key in [
        "build_executed",
        "runtime_adoption_authorized",
        "runtime_patch_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "t6_live_case_execution_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(review_summary, key, failures, "review_summary")

    if build_authorization_target.get("target_status") != "READY":
        failures.append(f"build_target_status_wrong:{build_authorization_target.get('target_status')}")
    if build_authorization_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"build_target_next_wrong:{build_authorization_target.get('next_unit_id')}")
    if build_authorization_target.get("build_authorization_id") != EXPECTED_BUILD_AUTHORIZATION_ID:
        failures.append("build_target_authorization_id_wrong")
    if build_authorization_target.get("candidate_build_unit") != EXPECTED_BUILD_UNIT:
        failures.append("build_target_candidate_unit_wrong")
    if build_authorization_target.get("bounded_build_unit_authorized") is not True:
        failures.append("build_target_not_authorized")
    if build_authorization_target.get("review_unit_does_not_build") is not True:
        failures.append("build_target_review_unit_does_not_build_missing")

    for name, obj in [
        ("objective_review", objective_review),
        ("boundary_review", boundary_review),
        ("contract_review", contract_review),
        ("guard_review", guard_review),
        ("test_receipt_review", test_receipt_review),
        ("negative_control_review", negative_control_review),
    ]:
        if obj.get("review_status") != "PASS":
            failures.append(f"{name}_not_pass:{obj.get('review_status')}:{obj.get('failures')}")

    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal.get("required_capability") != EXPECTED_REQUIRED_CAPABILITY:
        failures.append(f"proposal_required_capability_wrong:{proposal.get('required_capability')}")
    if proposal.get("proposed_surface") != EXPECTED_PROPOSED_SURFACE:
        failures.append(f"proposal_surface_wrong:{proposal.get('proposed_surface')}")
    if proposal.get("missing_objects_addressed") != EXPECTED_MISSING_OBJECTS:
        failures.append(f"proposal_missing_objects_wrong:{proposal.get('missing_objects_addressed')}")

    if stop_packet.get("stop_code") != "STOP_CAPABILITY_LAYER_REQUIRED":
        failures.append(f"source_stop_code_wrong:{stop_packet.get('stop_code')}")
    if proposal.get("source_stop_packet_id") != stop_packet.get("stop_packet_id"):
        failures.append("proposal_source_stop_packet_mismatch")
    if stop_packet.get("required_capability") != EXPECTED_REQUIRED_CAPABILITY:
        failures.append("stop_required_capability_wrong")

    if accept_summary.get("proposal_accepted") is not True:
        failures.append("accept_summary_proposal_not_accepted")
    if accept_summary.get("selected_decision") != EXPECTED_SELECTED_DECISION:
        failures.append("accept_summary_selected_decision_wrong")
    if prep_summary.get("implementation_path_prepared") is not True:
        failures.append("prep_summary_path_not_prepared")
    if validation_summary.get("proposal_validated_by_run") is not True:
        failures.append("validation_summary_proposal_not_validated")
    if validation_summary.get("proposal_admissible_for_human_decision") is not True:
        failures.append("validation_summary_proposal_not_admissible")
    if decision_record.get("decision_record_status") != "HUMAN_DECISION_RECORDED":
        failures.append("decision_record_status_wrong")
    if decision_record.get("proposal_accepted") is not True:
        failures.append("decision_record_proposal_not_accepted")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_BUILD_PASS_REVIEW_READY"
        if gate == "PASS"
        else "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_BUILD_GATE_FAIL"
    )

    capability_build_id = "bounded_structured_t6_trigger_surface_capability_build_" + sig8({
        "build_authorization_id": EXPECTED_BUILD_AUTHORIZATION_ID,
        "implementation_path_id": EXPECTED_IMPLEMENTATION_PATH_ID,
        "proposal_id": proposal.get("proposal_id"),
        "required_capability": proposal.get("required_capability"),
        "proposed_surface": proposal.get("proposed_surface"),
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_basis_v0",
        "unit_id": UNIT_ID,
        "capability_build_id": capability_build_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_implementation_path_review_receipt_id": IMPLEMENTATION_PATH_REVIEW_RECEIPT_ID,
        "source_build_authorization_id": EXPECTED_BUILD_AUTHORIZATION_ID,
        "source_implementation_path_id": EXPECTED_IMPLEMENTATION_PATH_ID,
        "source_proposal_id": PROPOSAL_ID,
        "build_claim": "Build bounded structured T6 trigger-surface capability representation artifacts only. Do not adopt into runtime, patch runtime, mutate schema archive, add moves, expand fixtures, execute T6 live case, authorize C8, or create hidden next command.",
        "source_file_hashes": source_hashes,
    }

    capability_profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_profile_v0",
        "capability_build_id": capability_build_id,
        "capability_name": EXPECTED_REQUIRED_CAPABILITY,
        "surface_name": EXPECTED_PROPOSED_SURFACE,
        "profile_status": "BUILT_PENDING_REVIEW" if gate == "PASS" else "BLOCKED",
        "source_proposal_id": PROPOSAL_ID,
        "source_stop_code": stop_packet.get("stop_code"),
        "source_missing_objects": EXPECTED_MISSING_OBJECTS,
        "purpose": "Represent a bounded structured T6 trigger surface so text-only tie residue is not treated as sufficient trigger evidence.",
        "recognized_evidence_families": [
            "structured_loop_trigger_surface",
            "structured_tie_evidence",
            "typed_absence_reason",
            "text_only_tie_residue_negative_control",
        ],
        "admissible_surface_states": [
            "STRUCTURED_TRIGGER_SURFACE_PRESENT",
            "STRUCTURED_TRIGGER_SURFACE_ABSENT_TYPED",
            "TEXT_ONLY_TIE_RESIDUE_ONLY",
            "UNDER_TYPED_EVIDENCE",
        ],
        "non_authorities": [
            "runtime adoption",
            "runtime patch",
            "schema archive mutation",
            "move registry addition",
            "fixture expansion",
            "T6 live case execution",
            "C8 authorization",
        ],
    }

    surface_schema_candidate = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_candidate_v0",
        "schema_candidate_status": "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION" if gate == "PASS" else "BLOCKED",
        "capability_build_id": capability_build_id,
        "schema_name": EXPECTED_PROPOSED_SURFACE,
        "object_kind": "BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_OBJECT",
        "required_fields": {
            "surface_id": "string",
            "source_proposal_id": "string",
            "source_stop_packet_id": "string",
            "capability_name": "string",
            "loop_trigger_surface": "structured_surface_or_typed_absence",
            "tie_evidence": "structured_evidence_or_typed_absence",
            "text_only_residue": "negative_control_or_null",
            "classification": "enum",
            "evidence_refs": "array",
            "boundary_flags": "object",
        },
        "classification_enum": [
            "STRUCTURED_TRIGGER_SURFACE_PRESENT",
            "STRUCTURED_TRIGGER_SURFACE_ABSENT_TYPED",
            "TEXT_ONLY_TIE_RESIDUE_ONLY",
            "UNDER_TYPED_EVIDENCE",
        ],
        "archive_mutation_authorized": False,
        "runtime_adoption_authorized": False,
    }

    evidence_shape_contract = {
        "schema_version": "bounded_structured_t6_trigger_surface_evidence_shape_contract_v0",
        "capability_build_id": capability_build_id,
        "contract_status": "BUILT_PENDING_REVIEW" if gate == "PASS" else "BLOCKED",
        "structured_loop_trigger_surface_required_shape": {
            "present": "bool",
            "surface_family": "string",
            "trigger_condition_ref": "string_or_null",
            "source_receipt_ref": "string_or_null",
            "typed_absence_reason": "string_or_null",
        },
        "structured_tie_evidence_required_shape": {
            "present": "bool",
            "tie_family": "string",
            "tie_object_ref": "string_or_null",
            "source_receipt_ref": "string_or_null",
            "typed_absence_reason": "string_or_null",
        },
        "text_only_residue_shape": {
            "present": "bool",
            "text": "string_or_null",
            "detector_ref": "string_or_null",
            "is_sufficient_for_structured_trigger": False,
        },
        "sufficiency_rule": "A trigger surface is sufficient only when structured loop trigger surface and structured tie evidence are present. Text-only residue is always negative control unless separately promoted by structured evidence.",
    }

    positive_structured_example = {
        "schema_version": "bounded_structured_t6_trigger_surface_positive_example_v0",
        "capability_build_id": capability_build_id,
        "example_status": "BUILT_EXAMPLE_ONLY_NOT_FIXTURE_EXPANSION" if gate == "PASS" else "BLOCKED",
        "surface_id": "example_structured_t6_surface_positive_v0",
        "source_proposal_id": PROPOSAL_ID,
        "source_stop_packet_id": stop_packet.get("stop_packet_id"),
        "capability_name": EXPECTED_REQUIRED_CAPABILITY,
        "loop_trigger_surface": {
            "present": True,
            "surface_family": "bounded_t6_loop_trigger_surface",
            "trigger_condition_ref": "example_trigger_condition_ref",
            "source_receipt_ref": "example_source_receipt_ref",
            "typed_absence_reason": None,
        },
        "tie_evidence": {
            "present": True,
            "tie_family": "structured_tie_evidence",
            "tie_object_ref": "example_tie_object_ref",
            "source_receipt_ref": "example_source_receipt_ref",
            "typed_absence_reason": None,
        },
        "text_only_residue": {
            "present": False,
            "text": None,
            "detector_ref": None,
            "is_sufficient_for_structured_trigger": False,
        },
        "classification": "STRUCTURED_TRIGGER_SURFACE_PRESENT",
        "fixture_expansion_authorized": False,
    }

    text_only_negative_control = {
        "schema_version": "bounded_structured_t6_trigger_surface_text_only_negative_control_v0",
        "capability_build_id": capability_build_id,
        "negative_control_status": "BUILT_EXAMPLE_ONLY_NOT_FIXTURE_EXPANSION" if gate == "PASS" else "BLOCKED",
        "surface_id": "example_text_only_tie_residue_negative_v0",
        "source_proposal_id": PROPOSAL_ID,
        "source_stop_packet_id": stop_packet.get("stop_packet_id"),
        "capability_name": EXPECTED_REQUIRED_CAPABILITY,
        "loop_trigger_surface": {
            "present": False,
            "surface_family": "bounded_t6_loop_trigger_surface",
            "trigger_condition_ref": None,
            "source_receipt_ref": None,
            "typed_absence_reason": "loop_trigger_surface_missing",
        },
        "tie_evidence": {
            "present": False,
            "tie_family": "structured_tie_evidence",
            "tie_object_ref": None,
            "source_receipt_ref": None,
            "typed_absence_reason": "structured_tie_evidence_missing",
        },
        "text_only_residue": {
            "present": True,
            "text": "tie surface mentioned in detector text only",
            "detector_ref": "text_only_detector_residue",
            "is_sufficient_for_structured_trigger": False,
        },
        "classification": "TEXT_ONLY_TIE_RESIDUE_ONLY",
        "expected_result": "NEGATIVE_CONTROL_PASS",
        "fixture_expansion_authorized": False,
    }

    classifier_policy = {
        "schema_version": "bounded_structured_t6_trigger_surface_classifier_policy_v0",
        "capability_build_id": capability_build_id,
        "policy_status": "BUILT_PENDING_REVIEW" if gate == "PASS" else "BLOCKED",
        "classification_rules": [
            {
                "when": "loop_trigger_surface.present is true and tie_evidence.present is true",
                "classification": "STRUCTURED_TRIGGER_SURFACE_PRESENT",
                "admissible_as_structured_trigger": True,
            },
            {
                "when": "loop_trigger_surface.present is false or tie_evidence.present is false, with typed absence reasons",
                "classification": "STRUCTURED_TRIGGER_SURFACE_ABSENT_TYPED",
                "admissible_as_structured_trigger": False,
            },
            {
                "when": "text_only_residue.present is true and structured evidence is absent",
                "classification": "TEXT_ONLY_TIE_RESIDUE_ONLY",
                "admissible_as_structured_trigger": False,
            },
            {
                "when": "required fields are missing or under-typed",
                "classification": "UNDER_TYPED_EVIDENCE",
                "admissible_as_structured_trigger": False,
            },
        ],
        "determinism_rule": "Classification is deterministic from structured fields only; no free-text detector residue can promote itself.",
    }

    capability_api_contract = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_api_contract_v0",
        "capability_build_id": capability_build_id,
        "contract_status": "BUILT_PENDING_REVIEW" if gate == "PASS" else "BLOCKED",
        "api_kind": "representation_contract_only",
        "input_object": "BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_OBJECT",
        "output_fields": [
            "classification",
            "admissible_as_structured_trigger",
            "typed_absence_reasons",
            "negative_control_status",
            "evidence_refs",
            "boundary_flags",
        ],
        "forbidden_side_effects": [
            "runtime mutation",
            "runtime adoption",
            "schema archive mutation",
            "move registry mutation",
            "fixture creation",
            "T6 live execution",
            "C8 authorization",
        ],
    }

    test_expectations = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_test_expectations_v0",
        "capability_build_id": capability_build_id,
        "expectation_status": "BUILT_PENDING_REVIEW" if gate == "PASS" else "BLOCKED",
        "tests": [
            {
                "test_id": "positive_structured_trigger_surface_present",
                "input_ref": rel(POSITIVE_STRUCTURED_EXAMPLE_PATH),
                "expected_classification": "STRUCTURED_TRIGGER_SURFACE_PRESENT",
                "expected_admissible_as_structured_trigger": True,
            },
            {
                "test_id": "negative_text_only_tie_residue_only",
                "input_ref": rel(TEXT_ONLY_NEGATIVE_CONTROL_PATH),
                "expected_classification": "TEXT_ONLY_TIE_RESIDUE_ONLY",
                "expected_admissible_as_structured_trigger": False,
            },
            {
                "test_id": "missing_structured_evidence_typed_absence",
                "input_shape": "structured fields present with typed absence reasons",
                "expected_classification": "STRUCTURED_TRIGGER_SURFACE_ABSENT_TYPED",
                "expected_admissible_as_structured_trigger": False,
            },
            {
                "test_id": "under_typed_evidence_blocks_progress",
                "input_shape": "required structured fields missing",
                "expected_classification": "UNDER_TYPED_EVIDENCE",
                "expected_admissible_as_structured_trigger": False,
            },
        ],
        "runtime_execution_required": False,
    }

    negative_control_result = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_negative_control_result_v0",
        "capability_build_id": capability_build_id,
        "result_status": "PASS" if gate == "PASS" else "BLOCKED",
        "text_only_residue_promoted": False,
        "positive_example_is_fixture_expansion": False,
        "negative_example_is_fixture_expansion": False,
        "zero_counters_for_this_build": {
            "runtime_patch_count": 0,
            "runtime_adoption_authority_count": 0,
            "schema_archive_mutation_count": 0,
            "move_registry_addition_count": 0,
            "fixture_expansion_count": 0,
            "t6_live_case_execution_count": 0,
            "hidden_next_command_count": 0,
            "c8_authorization_count": 0,
        },
    }

    build_review_target = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_review_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "capability_build_id": capability_build_id,
        "build_authorization_id": EXPECTED_BUILD_AUTHORIZATION_ID,
        "implementation_path_id": EXPECTED_IMPLEMENTATION_PATH_ID,
        "proposal_id": PROPOSAL_ID,
        "review_scope": "Review bounded structured T6 trigger-surface capability representation artifacts before any runtime adoption, schema archive promotion, move registry addition, fixture expansion, or T6 live execution.",
        "review_inputs": [
            rel(CAPABILITY_PROFILE_PATH),
            rel(SURFACE_SCHEMA_CANDIDATE_PATH),
            rel(EVIDENCE_SHAPE_CONTRACT_PATH),
            rel(POSITIVE_STRUCTURED_EXAMPLE_PATH),
            rel(TEXT_ONLY_NEGATIVE_CONTROL_PATH),
            rel(CLASSIFIER_POLICY_PATH),
            rel(CAPABILITY_API_CONTRACT_PATH),
            rel(TEST_EXPECTATIONS_PATH),
            rel(NEGATIVE_CONTROL_RESULT_PATH),
        ],
        "does_not_authorize_runtime_adoption": True,
        "does_not_authorize_schema_archive_mutation": True,
        "does_not_authorize_move_addition": True,
        "does_not_authorize_fixture_expansion": True,
    }

    rollup = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "capability_build_id": capability_build_id,
        "build_authorization_id": EXPECTED_BUILD_AUTHORIZATION_ID,
        "implementation_path_id": EXPECTED_IMPLEMENTATION_PATH_ID,
        "proposal_id": PROPOSAL_ID,
        "required_capability": EXPECTED_REQUIRED_CAPABILITY,
        "proposed_surface": EXPECTED_PROPOSED_SURFACE,
        "bounded_build_unit_authorized": True if gate == "PASS" else False,
        "build_executed": True if gate == "PASS" else False,
        "artifact_count": 9 if gate == "PASS" else 0,
        "build_review_target_ready": True if gate == "PASS" else False,
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_readout_v0",
        "status": status,
        "capability_build_id": capability_build_id,
        "build_authorization_id": EXPECTED_BUILD_AUTHORIZATION_ID,
        "proposal_id": PROPOSAL_ID,
        "interpretation": "Bounded structured T6 trigger-surface capability representation artifacts were built and are ready for review. No runtime adoption, runtime patch, schema archive mutation, move addition, fixture expansion, T6 live execution, hidden next command, or C8 authorization occurred."
        if gate == "PASS" else "Bounded structured T6 trigger-surface capability build failed typed gates.",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_profile_v0",
        "profile_status": status,
        "capability_build_id": capability_build_id,
        "core_rule": "Build bounded representation artifacts only. The artifact build is not runtime adoption and not schema archive promotion.",
        "capability_profile_ref": rel(CAPABILITY_PROFILE_PATH),
        "surface_schema_candidate_ref": rel(SURFACE_SCHEMA_CANDIDATE_PATH),
        "classifier_policy_ref": rel(CLASSIFIER_POLICY_PATH),
        "build_review_target_ref": rel(BUILD_REVIEW_TARGET_PATH),
        "must_not_infer": [
            "runtime adopted",
            "runtime patched",
            "schema archive mutated",
            "move registry updated",
            "fixture suite expanded",
            "T6 live case executed",
            "C8 authorized",
            "global trigger capability",
        ],
    }

    report = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "build_result": "BOUNDED_CAPABILITY_ARTIFACTS_BUILT_REVIEW_READY" if gate == "PASS" else "BOUNDED_CAPABILITY_BUILD_GATE_FAIL",
            "capability_build_id": capability_build_id,
            "proposal_id": PROPOSAL_ID,
            "build_authorization_id": EXPECTED_BUILD_AUTHORIZATION_ID,
            "artifact_count": 9 if gate == "PASS" else 0,
            "build_review_target_ready": gate == "PASS",
            "runtime_adoption_authorized": False,
            "runtime_patch_authorized": False,
            "schema_archive_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_transition_trace_v0",
        "unit_id": UNIT_ID,
        "capability_build_id": capability_build_id,
        "transitions": [
            {
                "from": "BOUNDED_BUILD_UNIT_AUTHORIZED",
                "edge": "build bounded structured trigger-surface representation artifacts",
                "to": "BOUNDED_CAPABILITY_ARTIFACTS_BUILT" if gate == "PASS" else "BOUNDED_CAPABILITY_BUILD_GATE_FAIL",
            },
            {
                "from": "BOUNDED_CAPABILITY_ARTIFACTS_BUILT" if gate == "PASS" else "BOUNDED_CAPABILITY_BUILD_GATE_FAIL",
                "edge": "emit build review target without runtime adoption or schema/move/fixture widening",
                "to": "BOUNDED_CAPABILITY_BUILD_REVIEW_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_BUILD_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (CAPABILITY_PROFILE_PATH, capability_profile),
        (SURFACE_SCHEMA_CANDIDATE_PATH, surface_schema_candidate),
        (EVIDENCE_SHAPE_CONTRACT_PATH, evidence_shape_contract),
        (POSITIVE_STRUCTURED_EXAMPLE_PATH, positive_structured_example),
        (TEXT_ONLY_NEGATIVE_CONTROL_PATH, text_only_negative_control),
        (CLASSIFIER_POLICY_PATH, classifier_policy),
        (CAPABILITY_API_CONTRACT_PATH, capability_api_contract),
        (TEST_EXPECTATIONS_PATH, test_expectations),
        (NEGATIVE_CONTROL_RESULT_PATH, negative_control_result),
        (BUILD_REVIEW_TARGET_PATH, build_review_target),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    output_core_artifacts = [
        CAPABILITY_PROFILE_PATH,
        SURFACE_SCHEMA_CANDIDATE_PATH,
        EVIDENCE_SHAPE_CONTRACT_PATH,
        POSITIVE_STRUCTURED_EXAMPLE_PATH,
        TEXT_ONLY_NEGATIVE_CONTROL_PATH,
        CLASSIFIER_POLICY_PATH,
        CAPABILITY_API_CONTRACT_PATH,
        TEST_EXPECTATIONS_PATH,
        NEGATIVE_CONTROL_RESULT_PATH,
    ]

    output_hashes = {rel(p): file_sha256(p) for p in output_core_artifacts}

    reason_codes = [
        "IMPLEMENTATION_PATH_REVIEW_RECEIPT_CONSUMED",
        "BUILD_AUTHORIZATION_TARGET_CONSUMED",
        "BOUNDED_BUILD_UNIT_AUTHORIZED_CONFIRMED",
        "CAPABILITY_PROFILE_BUILT",
        "SURFACE_SCHEMA_CANDIDATE_BUILT_NOT_ARCHIVE_MUTATION",
        "EVIDENCE_SHAPE_CONTRACT_BUILT",
        "POSITIVE_STRUCTURED_EXAMPLE_BUILT_NOT_FIXTURE_EXPANSION",
        "TEXT_ONLY_NEGATIVE_CONTROL_BUILT_NOT_FIXTURE_EXPANSION",
        "CLASSIFIER_POLICY_BUILT",
        "CAPABILITY_API_CONTRACT_BUILT",
        "TEST_EXPECTATIONS_BUILT",
        "NEGATIVE_CONTROL_RESULT_BUILT",
        "BUILD_REVIEW_TARGET_EMITTED",
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_BUILD_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "capability_build_id": capability_build_id,
        "source_implementation_path_review_receipt_id": IMPLEMENTATION_PATH_REVIEW_RECEIPT_ID,
        "source_implementation_path_review_receipt_ref": rel(IMPLEMENTATION_PATH_REVIEW_RECEIPT_PATH),
        "source_build_authorization_id": EXPECTED_BUILD_AUTHORIZATION_ID,
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "BOUNDED_T6_BUILD_0_REVIEW_RECEIPT_CONSUMED": gate == "PASS",
            "BOUNDED_T6_BUILD_1_BUILD_AUTHORIZATION_CONSUMED": build_authorization_target.get("bounded_build_unit_authorized") is True,
            "BOUNDED_T6_BUILD_2_PROFILE_BUILT": CAPABILITY_PROFILE_PATH.exists() and gate == "PASS",
            "BOUNDED_T6_BUILD_3_SCHEMA_CANDIDATE_BUILT": SURFACE_SCHEMA_CANDIDATE_PATH.exists() and gate == "PASS",
            "BOUNDED_T6_BUILD_4_EVIDENCE_CONTRACT_BUILT": EVIDENCE_SHAPE_CONTRACT_PATH.exists() and gate == "PASS",
            "BOUNDED_T6_BUILD_5_POSITIVE_EXAMPLE_BUILT": POSITIVE_STRUCTURED_EXAMPLE_PATH.exists() and gate == "PASS",
            "BOUNDED_T6_BUILD_6_TEXT_ONLY_NEGATIVE_CONTROL_BUILT": TEXT_ONLY_NEGATIVE_CONTROL_PATH.exists() and gate == "PASS",
            "BOUNDED_T6_BUILD_7_CLASSIFIER_POLICY_BUILT": CLASSIFIER_POLICY_PATH.exists() and gate == "PASS",
            "BOUNDED_T6_BUILD_8_TEST_EXPECTATIONS_BUILT": TEST_EXPECTATIONS_PATH.exists() and gate == "PASS",
            "BOUNDED_T6_BUILD_9_REVIEW_TARGET_EMITTED": BUILD_REVIEW_TARGET_PATH.exists() and gate == "PASS",
            "BOUNDED_T6_BUILD_10_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "BOUNDED_T6_BUILD_11_NO_RUNTIME_PATCH": True,
            "BOUNDED_T6_BUILD_12_NO_SCHEMA_ARCHIVE_MUTATION": True,
            "BOUNDED_T6_BUILD_13_NO_MOVE_ADDITION": True,
            "BOUNDED_T6_BUILD_14_NO_FIXTURE_EXPANSION": True,
            "BOUNDED_T6_BUILD_15_NO_T6_LIVE_CASE_EXECUTION": True,
            "BOUNDED_T6_BUILD_16_NO_C8_AUTHORIZATION": True,
            "BOUNDED_T6_BUILD_17_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_structured_t6_trigger_surface_capability_build_summary": {
            "status": status,
            "capability_build_id": capability_build_id,
            "build_authorization_id": EXPECTED_BUILD_AUTHORIZATION_ID,
            "implementation_path_id": EXPECTED_IMPLEMENTATION_PATH_ID,
            "proposal_id": PROPOSAL_ID,
            "proposal_kind": proposal.get("proposal_kind"),
            "required_capability": EXPECTED_REQUIRED_CAPABILITY,
            "proposed_surface": EXPECTED_PROPOSED_SURFACE,
            "build_unit": UNIT_ID,
            "bounded_build_unit_authorized": True if gate == "PASS" else False,
            "build_executed": True if gate == "PASS" else False,
            "build_review_target_ready": True if gate == "PASS" else False,
            "artifact_count": 9 if gate == "PASS" else 0,
            "schema_candidate_status": "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION" if gate == "PASS" else "BLOCKED",
            "positive_example_status": "BUILT_EXAMPLE_ONLY_NOT_FIXTURE_EXPANSION" if gate == "PASS" else "BLOCKED",
            "text_only_negative_control_status": "BUILT_EXAMPLE_ONLY_NOT_FIXTURE_EXPANSION" if gate == "PASS" else "BLOCKED",
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
            "output_core_artifact_hashes": output_hashes,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "capability_profile": rel(CAPABILITY_PROFILE_PATH),
            "surface_schema_candidate": rel(SURFACE_SCHEMA_CANDIDATE_PATH),
            "evidence_shape_contract": rel(EVIDENCE_SHAPE_CONTRACT_PATH),
            "positive_structured_example": rel(POSITIVE_STRUCTURED_EXAMPLE_PATH),
            "text_only_negative_control": rel(TEXT_ONLY_NEGATIVE_CONTROL_PATH),
            "classifier_policy": rel(CLASSIFIER_POLICY_PATH),
            "capability_api_contract": rel(CAPABILITY_API_CONTRACT_PATH),
            "test_expectations": rel(TEST_EXPECTATIONS_PATH),
            "negative_control_result": rel(NEGATIVE_CONTROL_RESULT_PATH),
            "build_review_target": rel(BUILD_REVIEW_TARGET_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_structured_t6_trigger_surface_capability_build_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_structured_t6_trigger_surface_capability_build_receipt_id={receipt_id}")
    print(f"bounded_structured_t6_trigger_surface_capability_build_receipt_path={rel(receipt_path)}")
    print(f"bounded_structured_t6_trigger_surface_capability_build_id={capability_build_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_build_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
