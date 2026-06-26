#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_ACCEPTED_BOUNDED_CAPABILITY_PROPOSAL_IMPLEMENTATION_PATH_V0"
TARGET_UNIT_ID = "accepted_bounded_capability_proposal.implementation_path_review_v0"
NEXT_UNIT_ID = "BUILD_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_V0"

IMPLEMENTATION_PATH_PREP_RECEIPT_ID = "accepted_bounded_capability_implementation_path_prep_receipt_b4fc0c59"
PROPOSAL_ID = "capability_proposal_57dda6e9"
EXPECTED_IMPLEMENTATION_CANDIDATE_UNIT = "BUILD_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_V0"
EXPECTED_REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
EXPECTED_PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"
EXPECTED_SELECTED_DECISION = "ACCEPT_FOR_BOUNDED_IMPLEMENTATION"
EXPECTED_MISSING_OBJECTS = [
    "loop_trigger_surface_missing",
    "structured_tie_evidence_missing",
]

IMPLEMENTATION_PATH_PREP_RECEIPT_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_prep_v0_receipts/accepted_bounded_capability_implementation_path_prep_receipt_b4fc0c59.json"

IMPLEMENTATION_REVIEW_TARGET_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_prep_v0/accepted_bounded_capability_proposal_implementation_path_review_target_v0.json"
IMPLEMENTATION_OBJECTIVE_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_prep_v0/accepted_bounded_capability_proposal_implementation_objective_v0.json"
CAPABILITY_BOUNDARY_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_prep_v0/accepted_bounded_capability_proposal_capability_boundary_v0.json"
MINIMAL_IMPLEMENTATION_CONTRACT_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_prep_v0/accepted_bounded_capability_proposal_minimal_implementation_contract_v0.json"
IMPLEMENTATION_GUARD_CONTRACT_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_prep_v0/accepted_bounded_capability_proposal_implementation_guard_contract_v0.json"
TEST_AND_RECEIPT_CONTRACT_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_prep_v0/accepted_bounded_capability_proposal_test_and_receipt_contract_v0.json"
NEGATIVE_CONTROL_CONTRACT_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_prep_v0/accepted_bounded_capability_proposal_implementation_negative_control_contract_v0.json"

ACCEPT_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_human_decision_accept_for_bounded_implementation_v0_receipts/bounded_capability_proposal_human_decision_accept_receipt_6979a229.json"
DECISION_RECORD_PATH = ROOT / "data/bounded_capability_proposal_human_decision_accept_for_bounded_implementation_v0/bounded_capability_proposal_human_decision_record_v0.json"

VALIDATION_RUN_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0_receipts/bounded_capability_proposal_validation_path_run_receipt_375954b6.json"
PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"

OUT_DIR = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0"
RECEIPT_DIR = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0_receipts"

BASIS_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_review_basis_v0.json"
OBJECTIVE_REVIEW_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_objective_review_v0.json"
BOUNDARY_REVIEW_PATH = OUT_DIR / "accepted_bounded_capability_proposal_capability_boundary_review_v0.json"
CONTRACT_REVIEW_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_contract_review_v0.json"
GUARD_REVIEW_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_guard_review_v0.json"
TEST_RECEIPT_REVIEW_PATH = OUT_DIR / "accepted_bounded_capability_proposal_test_and_receipt_review_v0.json"
NEGATIVE_CONTROL_REVIEW_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_negative_control_review_v0.json"
BUILD_AUTHORIZATION_TARGET_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_authorization_target_v0.json"
READOUT_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_review_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_review_transition_trace.json"

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

def false_or_missing(obj: Dict[str, Any], key: str) -> bool:
    return key not in obj or obj.get(key) is False

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        IMPLEMENTATION_PATH_PREP_RECEIPT_PATH,
        IMPLEMENTATION_REVIEW_TARGET_PATH,
        IMPLEMENTATION_OBJECTIVE_PATH,
        CAPABILITY_BOUNDARY_PATH,
        MINIMAL_IMPLEMENTATION_CONTRACT_PATH,
        IMPLEMENTATION_GUARD_CONTRACT_PATH,
        TEST_AND_RECEIPT_CONTRACT_PATH,
        NEGATIVE_CONTROL_CONTRACT_PATH,
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

    prep_receipt = read_json(IMPLEMENTATION_PATH_PREP_RECEIPT_PATH)
    review_target = read_json(IMPLEMENTATION_REVIEW_TARGET_PATH)
    objective = read_json(IMPLEMENTATION_OBJECTIVE_PATH)
    capability_boundary = read_json(CAPABILITY_BOUNDARY_PATH)
    minimal_contract = read_json(MINIMAL_IMPLEMENTATION_CONTRACT_PATH)
    guard_contract = read_json(IMPLEMENTATION_GUARD_CONTRACT_PATH)
    test_receipt_contract = read_json(TEST_AND_RECEIPT_CONTRACT_PATH)
    negative_contract = read_json(NEGATIVE_CONTROL_CONTRACT_PATH)
    accept_receipt = read_json(ACCEPT_RECEIPT_PATH)
    decision_record = read_json(DECISION_RECORD_PATH)
    validation_run = read_json(VALIDATION_RUN_RECEIPT_PATH)
    proposal = read_json(PROPOSAL_PATH)
    stop_packet = read_json(STOP_PACKET_PATH)

    prep_summary = prep_receipt.get("machine_readable_accepted_bounded_capability_proposal_implementation_path_prep_summary", {})
    accept_summary = accept_receipt.get("machine_readable_bounded_capability_proposal_human_decision_accept_summary", {})
    validation_summary = validation_run.get("machine_readable_bounded_capability_proposal_validation_path_run_summary", {})

    if prep_receipt.get("receipt_id") != IMPLEMENTATION_PATH_PREP_RECEIPT_ID:
        failures.append(f"prep_receipt_id_wrong:{prep_receipt.get('receipt_id')}")
    if prep_receipt.get("gate") != "PASS":
        failures.append("prep_receipt_gate_not_pass")
    if prep_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"prep_terminal_next_wrong:{prep_receipt.get('terminal', {}).get('next_unit_id')}")

    for key in [
        "proposal_accepted",
        "bounded_implementation_path_prep_authorized",
        "implementation_path_prepared",
        "implementation_review_target_ready",
    ]:
        if prep_summary.get(key) is not True:
            failures.append(f"prep_{key}_not_true:{prep_summary.get(key)}")

    if prep_summary.get("implementation_candidate_unit") != EXPECTED_IMPLEMENTATION_CANDIDATE_UNIT:
        failures.append(f"implementation_candidate_unit_wrong:{prep_summary.get('implementation_candidate_unit')}")
    if prep_summary.get("implementation_candidate_status") != "CANDIDATE_ONLY_NOT_AUTHORIZED":
        failures.append(f"implementation_candidate_status_wrong:{prep_summary.get('implementation_candidate_status')}")

    for key in [
        "implementation_authorized",
        "implementation_executed",
        "runtime_adoption_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "runtime_patch_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        if prep_summary.get(key) is not False:
            failures.append(f"prep_boundary_{key}_not_false:{prep_summary.get(key)}")

    if review_target.get("target_status") != "READY":
        failures.append(f"review_target_status_wrong:{review_target.get('target_status')}")
    if review_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"review_target_next_wrong:{review_target.get('next_unit_id')}")
    if review_target.get("does_not_authorize_build") is not True:
        failures.append("review_target_does_not_authorize_build_missing")

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
        failures.append("source_stop_packet_mismatch")

    if accept_summary.get("selected_decision") != EXPECTED_SELECTED_DECISION:
        failures.append("accept_summary_selected_decision_wrong")
    if accept_summary.get("proposal_accepted") is not True:
        failures.append("accept_summary_proposal_not_accepted")
    if accept_summary.get("bounded_implementation_path_prep_authorized") is not True:
        failures.append("accept_summary_path_prep_not_authorized")
    if decision_record.get("selected_decision") != EXPECTED_SELECTED_DECISION:
        failures.append("decision_record_selected_decision_wrong")
    if decision_record.get("proposal_accepted") is not True:
        failures.append("decision_record_proposal_not_accepted")
    if validation_summary.get("proposal_validated_by_run") is not True:
        failures.append("validation_proposal_not_validated")
    if validation_summary.get("proposal_admissible_for_human_decision") is not True:
        failures.append("validation_proposal_not_admissible")

    # Objective review.
    objective_failures = []
    if objective.get("objective_status") != "READY_FOR_REVIEW":
        objective_failures.append(f"objective_status_wrong:{objective.get('objective_status')}")
    objective_text = str(objective.get("bounded_objective", "")).lower()
    if "structured t6 trigger-surface capability" not in objective_text:
        objective_failures.append("bounded_objective_missing_structured_t6_trigger_surface")
    not_in_scope = [str(x).lower() for x in objective.get("not_in_scope", [])]
    for phrase in [
        "runtime repair",
        "runtime patch",
        "runtime adoption",
        "schema archive mutation",
        "move registry addition",
        "fixture expansion by default",
        "t6 live case execution",
        "c8",
        "global loop capability",
    ]:
        if phrase not in not_in_scope:
            objective_failures.append(f"not_in_scope_missing:{phrase}")

    # Boundary review.
    boundary_failures = []
    if capability_boundary.get("capability_name") != EXPECTED_REQUIRED_CAPABILITY:
        boundary_failures.append("capability_name_wrong")
    if capability_boundary.get("surface_name") != EXPECTED_PROPOSED_SURFACE:
        boundary_failures.append("surface_name_wrong")
    if capability_boundary.get("source_missing_objects") != EXPECTED_MISSING_OBJECTS:
        boundary_failures.append("source_missing_objects_wrong")
    allowed_shape = capability_boundary.get("allowed_capability_shape") or {}
    for key in EXPECTED_MISSING_OBJECTS + ["text_only_tie_residue"]:
        if key not in allowed_shape:
            boundary_failures.append(f"allowed_shape_missing:{key}")
    authority_boundary = str(capability_boundary.get("authority_boundary", "")).lower()
    if "may not implement" not in authority_boundary and "not implement" not in authority_boundary:
        boundary_failures.append("authority_boundary_missing_no_implementation")

    # Contract review.
    contract_failures = []
    if minimal_contract.get("contract_status") != "READY_FOR_REVIEW":
        contract_failures.append("minimal_contract_not_ready_for_review")
    if minimal_contract.get("implementation_candidate_unit") != EXPECTED_IMPLEMENTATION_CANDIDATE_UNIT:
        contract_failures.append("minimal_contract_candidate_unit_wrong")
    if minimal_contract.get("implementation_candidate_status") != "CANDIDATE_ONLY_NOT_AUTHORIZED":
        contract_failures.append("minimal_contract_candidate_status_wrong")
    if minimal_contract.get("this_unit_does_not_build_these_artifacts") is not True:
        contract_failures.append("minimal_contract_builds_artifacts_unexpected")
    required_before_build = [str(x).lower() for x in minimal_contract.get("required_before_build", [])]
    for phrase in [
        "review this implementation path",
        "confirm implementation target remains bounded to proposed surface",
        "confirm no runtime adoption or move/schema mutation is included",
        "confirm tests/negative controls are sufficient",
        "emit a separate build authorization receipt",
    ]:
        if phrase not in required_before_build:
            contract_failures.append(f"required_before_build_missing:{phrase}")

    # Guard review.
    guard_failures = []
    if guard_contract.get("guard_status") != "READY_FOR_REVIEW":
        guard_failures.append("guard_contract_not_ready_for_review")
    must_false = guard_contract.get("must_remain_false_in_this_unit") or []
    for key in [
        "implementation_authorized",
        "implementation_executed",
        "runtime_adoption_authorized",
        "runtime_patch_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        if key not in must_false:
            guard_failures.append(f"must_remain_false_missing:{key}")

    # Test/receipt review.
    test_failures = []
    if test_receipt_contract.get("contract_status") != "READY_FOR_REVIEW":
        test_failures.append("test_receipt_contract_not_ready")
    required_future_tests = [str(x).lower() for x in test_receipt_contract.get("required_future_tests", [])]
    for phrase in [
        "text-only tie surface remains negative",
        "structured loop trigger surface with required fields is recognized",
        "structured tie evidence with required fields is recognized",
        "missing structured evidence produces typed capability stop, not repair",
    ]:
        if phrase not in required_future_tests:
            test_failures.append(f"future_test_missing:{phrase}")
    receipt_fields = [str(x).lower() for x in test_receipt_contract.get("required_future_receipt_fields", [])]
    for phrase in [
        "source_accept_receipt_id",
        "decision_record_id",
        "proposal_id",
        "required_capability",
        "proposed_surface",
        "implementation_scope",
        "negative_control_counts",
        "runtime_patch_authorized=false",
        "runtime_adoption_authorized=false",
        "c8_authorized=false",
    ]:
        if phrase not in receipt_fields:
            test_failures.append(f"future_receipt_field_missing:{phrase}")

    # Negative-control review.
    negative_failures = []
    zero_counters = negative_contract.get("zero_counters_for_this_unit") or {}
    for key in [
        "implementation_executed_count",
        "runtime_patch_count",
        "runtime_adoption_authority_count",
        "schema_mutation_count",
        "move_addition_count",
        "fixture_expansion_count",
        "hidden_next_command_count",
        "c8_authorization_count",
    ]:
        if zero_counters.get(key) != 0:
            negative_failures.append(f"zero_counter_wrong:{key}:{zero_counters.get(key)}")

    if objective_failures:
        failures.append(f"objective_review_failures:{objective_failures}")
    if boundary_failures:
        failures.append(f"boundary_review_failures:{boundary_failures}")
    if contract_failures:
        failures.append(f"contract_review_failures:{contract_failures}")
    if guard_failures:
        failures.append(f"guard_review_failures:{guard_failures}")
    if test_failures:
        failures.append(f"test_receipt_review_failures:{test_failures}")
    if negative_failures:
        failures.append(f"negative_control_review_failures:{negative_failures}")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_ACCEPTED_BOUNDED_CAPABILITY_PROPOSAL_IMPLEMENTATION_PATH_REVIEW_PASS_BUILD_UNIT_AUTHORIZATION_READY"
        if gate == "PASS"
        else "TYPED_ACCEPTED_BOUNDED_CAPABILITY_PROPOSAL_IMPLEMENTATION_PATH_REVIEW_GATE_FAIL"
    )

    implementation_path_id = prep_summary.get("implementation_path_id")
    build_authorization_id = "bounded_structured_t6_trigger_surface_capability_build_auth_" + sig8({
        "implementation_path_id": implementation_path_id,
        "proposal_id": proposal.get("proposal_id"),
        "candidate_unit": EXPECTED_IMPLEMENTATION_CANDIDATE_UNIT,
        "decision_record_id": decision_record.get("decision_record_id"),
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_review_basis_v0",
        "unit_id": UNIT_ID,
        "implementation_path_id": implementation_path_id,
        "build_authorization_id": build_authorization_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_implementation_path_prep_receipt_id": IMPLEMENTATION_PATH_PREP_RECEIPT_ID,
        "source_proposal_id": PROPOSAL_ID,
        "review_claim": "Review the prepared bounded implementation path and, if clean, authorize the later build unit. Do not build or mutate runtime in this review.",
        "source_file_hashes": source_hashes,
    }

    objective_review = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_objective_review_v0",
        "implementation_path_id": implementation_path_id,
        "review_status": "PASS" if not objective_failures else "FAIL",
        "failures": objective_failures,
        "bounded_objective": objective.get("bounded_objective"),
        "minimal_required_outputs": objective.get("minimal_required_outputs"),
        "not_in_scope": objective.get("not_in_scope"),
    }

    boundary_review = {
        "schema_version": "accepted_bounded_capability_proposal_capability_boundary_review_v0",
        "implementation_path_id": implementation_path_id,
        "review_status": "PASS" if not boundary_failures else "FAIL",
        "failures": boundary_failures,
        "capability_name": capability_boundary.get("capability_name"),
        "surface_name": capability_boundary.get("surface_name"),
        "source_missing_objects": capability_boundary.get("source_missing_objects"),
        "allowed_capability_shape": capability_boundary.get("allowed_capability_shape"),
        "authority_boundary": capability_boundary.get("authority_boundary"),
    }

    contract_review = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_contract_review_v0",
        "implementation_path_id": implementation_path_id,
        "review_status": "PASS" if not contract_failures else "FAIL",
        "failures": contract_failures,
        "implementation_candidate_unit": minimal_contract.get("implementation_candidate_unit"),
        "implementation_candidate_status_before_review": minimal_contract.get("implementation_candidate_status"),
        "required_before_build": minimal_contract.get("required_before_build"),
        "candidate_artifacts_to_build_later": minimal_contract.get("candidate_artifacts_to_build_later"),
    }

    guard_review = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_guard_review_v0",
        "implementation_path_id": implementation_path_id,
        "review_status": "PASS" if not guard_failures else "FAIL",
        "failures": guard_failures,
        "must_remain_false_in_review_unit": guard_contract.get("must_remain_false_in_this_unit"),
        "build_gate_rule": guard_contract.get("build_gate_rule"),
        "implementation_executed": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    test_receipt_review = {
        "schema_version": "accepted_bounded_capability_proposal_test_and_receipt_review_v0",
        "implementation_path_id": implementation_path_id,
        "review_status": "PASS" if not test_failures else "FAIL",
        "failures": test_failures,
        "required_future_tests": test_receipt_contract.get("required_future_tests"),
        "required_future_receipt_fields": test_receipt_contract.get("required_future_receipt_fields"),
    }

    negative_control_review = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_negative_control_review_v0",
        "implementation_path_id": implementation_path_id,
        "review_status": "PASS" if not negative_failures else "FAIL",
        "failures": negative_failures,
        "observed_zero_counters": zero_counters,
    }

    build_authorization_target = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_authorization_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "build_authorization_id": build_authorization_id,
        "implementation_path_id": implementation_path_id,
        "proposal_id": proposal.get("proposal_id"),
        "decision_record_id": decision_record.get("decision_record_id"),
        "source_implementation_path_prep_receipt_id": IMPLEMENTATION_PATH_PREP_RECEIPT_ID,
        "candidate_build_unit": EXPECTED_IMPLEMENTATION_CANDIDATE_UNIT,
        "candidate_status_after_review": "AUTHORIZED_FOR_BOUNDED_BUILD_UNIT" if gate == "PASS" else "BLOCKED",
        "bounded_build_unit_authorized": True if gate == "PASS" else False,
        "build_scope": "Build bounded structured T6 trigger-surface capability representation artifacts only.",
        "build_must_emit": [
            "structured trigger-surface capability profile",
            "capability surface schema candidate artifact",
            "positive structured trigger/tie evidence example",
            "text-only tie residue negative-control case",
            "build receipt with no runtime patch/adoption/schema/move widening unless separately authorized",
        ],
        "build_must_not_do": [
            "runtime adoption",
            "runtime patch",
            "schema archive mutation",
            "move registry addition",
            "fixture expansion by default",
            "T6 live case execution",
            "C8 authorization",
            "hidden next command",
        ],
        "review_unit_does_not_build": True,
    }

    rollup = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_review_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "implementation_path_id": implementation_path_id,
        "build_authorization_id": build_authorization_id,
        "proposal_id": proposal.get("proposal_id"),
        "required_capability": proposal.get("required_capability"),
        "proposed_surface": proposal.get("proposed_surface"),
        "objective_review_pass": not objective_failures,
        "boundary_review_pass": not boundary_failures,
        "contract_review_pass": not contract_failures,
        "guard_review_pass": not guard_failures,
        "test_receipt_review_pass": not test_failures,
        "negative_control_review_pass": not negative_failures,
        "bounded_build_unit_authorized": True if gate == "PASS" else False,
        "candidate_build_unit": EXPECTED_IMPLEMENTATION_CANDIDATE_UNIT,
        "candidate_status_after_review": "AUTHORIZED_FOR_BOUNDED_BUILD_UNIT" if gate == "PASS" else "BLOCKED",
        "implementation_executed": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    readout = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_review_readout_v0",
        "status": status,
        "implementation_path_id": implementation_path_id,
        "build_authorization_id": build_authorization_id,
        "proposal_id": proposal.get("proposal_id"),
        "candidate_build_unit": EXPECTED_IMPLEMENTATION_CANDIDATE_UNIT,
        "bounded_build_unit_authorized": True if gate == "PASS" else False,
        "interpretation": "Implementation path review passed and authorized the bounded build unit. This review did not build, patch runtime, mutate schema, add moves, expand fixtures, or authorize C8."
        if gate == "PASS" else "Implementation path review failed typed gates.",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_review_profile_v0",
        "profile_status": status,
        "implementation_path_id": implementation_path_id,
        "build_authorization_id": build_authorization_id,
        "core_rule": "Review can authorize the next bounded build unit; review itself must not build or mutate runtime/state surfaces.",
        "build_authorization_target_ref": rel(BUILD_AUTHORIZATION_TARGET_PATH),
        "must_not_infer": [
            "build already executed",
            "runtime repaired",
            "runtime adoption authorized",
            "runtime patch authorized",
            "schema archive mutation authorized",
            "move registry addition authorized",
            "fixture expansion authorized",
            "T6 live case executed",
            "C8 authorized",
            "unbounded implementation authority",
        ],
    }

    report = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_review_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "review_result": "BUILD_UNIT_AUTHORIZATION_READY" if gate == "PASS" else "IMPLEMENTATION_PATH_REVIEW_GATE_FAIL",
            "implementation_path_id": implementation_path_id,
            "build_authorization_id": build_authorization_id,
            "proposal_id": proposal.get("proposal_id"),
            "candidate_build_unit": EXPECTED_IMPLEMENTATION_CANDIDATE_UNIT,
            "bounded_build_unit_authorized": True if gate == "PASS" else False,
            "implementation_executed": False,
            "runtime_patch_authorized": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_review_transition_trace_v0",
        "unit_id": UNIT_ID,
        "implementation_path_id": implementation_path_id,
        "transitions": [
            {
                "from": "IMPLEMENTATION_PATH_REVIEW_READY",
                "edge": "review objective, boundary, contracts, guards, tests, receipts, and negative controls",
                "to": "IMPLEMENTATION_PATH_REVIEW_PASS" if gate == "PASS" else "IMPLEMENTATION_PATH_REVIEW_GATE_FAIL",
            },
            {
                "from": "IMPLEMENTATION_PATH_REVIEW_PASS" if gate == "PASS" else "IMPLEMENTATION_PATH_REVIEW_GATE_FAIL",
                "edge": "emit bounded build authorization target without building",
                "to": "BOUNDED_BUILD_UNIT_AUTHORIZED" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_ACCEPTED_BOUNDED_CAPABILITY_PROPOSAL_IMPLEMENTATION_PATH_REVIEW_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (OBJECTIVE_REVIEW_PATH, objective_review),
        (BOUNDARY_REVIEW_PATH, boundary_review),
        (CONTRACT_REVIEW_PATH, contract_review),
        (GUARD_REVIEW_PATH, guard_review),
        (TEST_RECEIPT_REVIEW_PATH, test_receipt_review),
        (NEGATIVE_CONTROL_REVIEW_PATH, negative_control_review),
        (BUILD_AUTHORIZATION_TARGET_PATH, build_authorization_target),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "IMPLEMENTATION_PATH_PREP_RECEIPT_CONSUMED",
        "IMPLEMENTATION_REVIEW_TARGET_CONSUMED",
        "OBJECTIVE_REVIEW_PASS",
        "CAPABILITY_BOUNDARY_REVIEW_PASS",
        "IMPLEMENTATION_CONTRACT_REVIEW_PASS",
        "IMPLEMENTATION_GUARD_REVIEW_PASS",
        "TEST_AND_RECEIPT_REVIEW_PASS",
        "NEGATIVE_CONTROL_REVIEW_PASS",
        "BOUNDED_BUILD_UNIT_AUTHORIZATION_TARGET_EMITTED",
        "BUILD_UNIT_AUTHORIZED_FOR_BOUNDED_CAPABILITY_ARTIFACTS",
        "NO_BUILD_EXECUTED",
        "NO_RUNTIME_REPAIR",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_RUNTIME_PATCH",
        "NO_SCHEMA_MUTATION",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_T6_LIVE_CASE_EXECUTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_review_receipt_v0",
        "receipt_type": "TYPED_ACCEPTED_BOUNDED_CAPABILITY_PROPOSAL_IMPLEMENTATION_PATH_REVIEW_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "implementation_path_id": implementation_path_id,
        "build_authorization_id": build_authorization_id,
        "source_implementation_path_prep_receipt_id": IMPLEMENTATION_PATH_PREP_RECEIPT_ID,
        "source_implementation_path_prep_receipt_ref": rel(IMPLEMENTATION_PATH_PREP_RECEIPT_PATH),
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "IMPLEMENTATION_PATH_REVIEW_0_PREP_RECEIPT_CONSUMED": gate == "PASS",
            "IMPLEMENTATION_PATH_REVIEW_1_REVIEW_TARGET_READY": review_target.get("target_status") == "READY",
            "IMPLEMENTATION_PATH_REVIEW_2_OBJECTIVE_REVIEW_PASS": not objective_failures,
            "IMPLEMENTATION_PATH_REVIEW_3_BOUNDARY_REVIEW_PASS": not boundary_failures,
            "IMPLEMENTATION_PATH_REVIEW_4_CONTRACT_REVIEW_PASS": not contract_failures,
            "IMPLEMENTATION_PATH_REVIEW_5_GUARD_REVIEW_PASS": not guard_failures,
            "IMPLEMENTATION_PATH_REVIEW_6_TEST_RECEIPT_REVIEW_PASS": not test_failures,
            "IMPLEMENTATION_PATH_REVIEW_7_NEGATIVE_CONTROL_REVIEW_PASS": not negative_failures,
            "IMPLEMENTATION_PATH_REVIEW_8_BUILD_AUTHORIZATION_TARGET_EMITTED": BUILD_AUTHORIZATION_TARGET_PATH.exists() and gate == "PASS",
            "IMPLEMENTATION_PATH_REVIEW_9_NO_BUILD_EXECUTED": True,
            "IMPLEMENTATION_PATH_REVIEW_10_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "IMPLEMENTATION_PATH_REVIEW_11_NO_RUNTIME_PATCH": True,
            "IMPLEMENTATION_PATH_REVIEW_12_NO_SCHEMA_MUTATION": True,
            "IMPLEMENTATION_PATH_REVIEW_13_NO_MOVE_ADDITION": True,
            "IMPLEMENTATION_PATH_REVIEW_14_NO_C8_AUTHORIZATION": True,
            "IMPLEMENTATION_PATH_REVIEW_15_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_accepted_bounded_capability_proposal_implementation_path_review_summary": {
            "status": status,
            "implementation_path_id": implementation_path_id,
            "build_authorization_id": build_authorization_id,
            "proposal_id": proposal.get("proposal_id"),
            "proposal_kind": proposal.get("proposal_kind"),
            "proposed_surface": proposal.get("proposed_surface"),
            "required_capability": proposal.get("required_capability"),
            "decision_record_id": decision_record.get("decision_record_id"),
            "selected_decision": EXPECTED_SELECTED_DECISION,
            "proposal_accepted": True if gate == "PASS" else False,
            "implementation_path_prepared": True if gate == "PASS" else False,
            "implementation_path_review_pass": True if gate == "PASS" else False,
            "bounded_build_unit_authorized": True if gate == "PASS" else False,
            "candidate_build_unit": EXPECTED_IMPLEMENTATION_CANDIDATE_UNIT,
            "candidate_status_after_review": "AUTHORIZED_FOR_BOUNDED_BUILD_UNIT" if gate == "PASS" else "BLOCKED",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "build_executed": False,
            "runtime_adoption_authorized": False,
            "runtime_patch_authorized": False,
            "schema_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "t6_live_case_execution_authorized": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "objective_review": rel(OBJECTIVE_REVIEW_PATH),
            "boundary_review": rel(BOUNDARY_REVIEW_PATH),
            "contract_review": rel(CONTRACT_REVIEW_PATH),
            "guard_review": rel(GUARD_REVIEW_PATH),
            "test_receipt_review": rel(TEST_RECEIPT_REVIEW_PATH),
            "negative_control_review": rel(NEGATIVE_CONTROL_REVIEW_PATH),
            "build_authorization_target": rel(BUILD_AUTHORIZATION_TARGET_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "accepted_bounded_capability_implementation_path_review_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"accepted_bounded_capability_implementation_path_review_receipt_id={receipt_id}")
    print(f"accepted_bounded_capability_implementation_path_review_receipt_path={rel(receipt_path)}")
    print(f"accepted_bounded_capability_implementation_path_review_build_authorization_id={build_authorization_id if gate == 'PASS' else 'NONE'}")
    print(f"accepted_bounded_capability_implementation_path_review_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
