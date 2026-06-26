#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_BUILD_V0"
TARGET_UNIT_ID = "bounded_structured_t6_trigger_surface_capability.build_review_v0"
NEXT_UNIT_ID = "PREPARE_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_ADOPTION_PATH_V0"

BUILD_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079"
CAPABILITY_BUILD_ID = "bounded_structured_t6_trigger_surface_capability_build_721f09dc"
BUILD_AUTHORIZATION_ID = "bounded_structured_t6_trigger_surface_capability_build_auth_c0315976"
IMPLEMENTATION_PATH_ID = "accepted_bounded_capability_implementation_path_defd6d9b"
PROPOSAL_ID = "capability_proposal_57dda6e9"
REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"

BUILD_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079.json"

BUILD_REVIEW_TARGET_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_build_review_target_v0.json"
CAPABILITY_PROFILE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_profile_v0.json"
SCHEMA_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_schema_candidate_v0.json"
EVIDENCE_SHAPE_CONTRACT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_evidence_shape_contract_v0.json"
POSITIVE_EXAMPLE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_positive_example_v0.json"
TEXT_ONLY_NEGATIVE_CONTROL_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_text_only_negative_control_v0.json"
CLASSIFIER_POLICY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_classifier_policy_v0.json"
API_CONTRACT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_api_contract_v0.json"
TEST_EXPECTATIONS_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_test_expectations_v0.json"
NEGATIVE_CONTROL_RESULT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_negative_control_result_v0.json"

IMPLEMENTATION_PATH_REVIEW_RECEIPT_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0_receipts/accepted_bounded_capability_implementation_path_review_receipt_e4b4e2d7.json"
BUILD_AUTHORIZATION_TARGET_PATH = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_review_v0/bounded_structured_t6_trigger_surface_capability_build_authorization_target_v0.json"

PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"

OUT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0"
RECEIPT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_review_basis_v0.json"
CAPABILITY_PROFILE_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_profile_review_v0.json"
SCHEMA_CANDIDATE_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_candidate_review_v0.json"
EVIDENCE_SHAPE_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_evidence_shape_contract_review_v0.json"
EXAMPLE_PAIR_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_example_pair_review_v0.json"
CLASSIFIER_POLICY_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_classifier_policy_review_v0.json"
API_CONTRACT_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_api_contract_review_v0.json"
TEST_EXPECTATIONS_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_test_expectations_review_v0.json"
NEGATIVE_CONTROL_REVIEW_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_negative_control_review_v0.json"
ADOPTION_PATH_PREP_TARGET_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_target_v0.json"
READOUT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_review_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_build_review_transition_trace.json"

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

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        BUILD_RECEIPT_PATH,
        BUILD_REVIEW_TARGET_PATH,
        CAPABILITY_PROFILE_PATH,
        SCHEMA_CANDIDATE_PATH,
        EVIDENCE_SHAPE_CONTRACT_PATH,
        POSITIVE_EXAMPLE_PATH,
        TEXT_ONLY_NEGATIVE_CONTROL_PATH,
        CLASSIFIER_POLICY_PATH,
        API_CONTRACT_PATH,
        TEST_EXPECTATIONS_PATH,
        NEGATIVE_CONTROL_RESULT_PATH,
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

    build_receipt = read_json(BUILD_RECEIPT_PATH)
    build_review_target = read_json(BUILD_REVIEW_TARGET_PATH)
    capability_profile = read_json(CAPABILITY_PROFILE_PATH)
    schema_candidate = read_json(SCHEMA_CANDIDATE_PATH)
    evidence_shape = read_json(EVIDENCE_SHAPE_CONTRACT_PATH)
    positive_example = read_json(POSITIVE_EXAMPLE_PATH)
    text_only_negative = read_json(TEXT_ONLY_NEGATIVE_CONTROL_PATH)
    classifier_policy = read_json(CLASSIFIER_POLICY_PATH)
    api_contract = read_json(API_CONTRACT_PATH)
    test_expectations = read_json(TEST_EXPECTATIONS_PATH)
    negative_control_result = read_json(NEGATIVE_CONTROL_RESULT_PATH)
    implementation_review_receipt = read_json(IMPLEMENTATION_PATH_REVIEW_RECEIPT_PATH)
    build_authorization_target = read_json(BUILD_AUTHORIZATION_TARGET_PATH)
    proposal = read_json(PROPOSAL_PATH)
    stop_packet = read_json(STOP_PACKET_PATH)

    build_summary = build_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_summary", {})
    implementation_review_summary = implementation_review_receipt.get("machine_readable_accepted_bounded_capability_proposal_implementation_path_review_summary", {})

    if build_receipt.get("receipt_id") != BUILD_RECEIPT_ID:
        failures.append(f"build_receipt_id_wrong:{build_receipt.get('receipt_id')}")
    if build_receipt.get("gate") != "PASS":
        failures.append("build_receipt_gate_not_pass")
    if build_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"build_receipt_terminal_next_wrong:{build_receipt.get('terminal', {}).get('next_unit_id')}")

    for key in [
        "bounded_build_unit_authorized",
        "build_executed",
        "build_review_target_ready",
    ]:
        if build_summary.get(key) is not True:
            failures.append(f"build_summary_{key}_not_true:{build_summary.get(key)}")

    if build_summary.get("artifact_count") != 9:
        failures.append(f"artifact_count_wrong:{build_summary.get('artifact_count')}")
    if build_summary.get("capability_build_id") != CAPABILITY_BUILD_ID:
        failures.append(f"capability_build_id_wrong:{build_summary.get('capability_build_id')}")
    if build_summary.get("build_authorization_id") != BUILD_AUTHORIZATION_ID:
        failures.append(f"build_authorization_id_wrong:{build_summary.get('build_authorization_id')}")
    if build_summary.get("implementation_path_id") != IMPLEMENTATION_PATH_ID:
        failures.append(f"implementation_path_id_wrong:{build_summary.get('implementation_path_id')}")

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
        if build_summary.get(key) is not False:
            failures.append(f"build_boundary_{key}_not_false:{build_summary.get(key)}")

    if build_review_target.get("target_status") != "READY":
        failures.append(f"build_review_target_status_wrong:{build_review_target.get('target_status')}")
    if build_review_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"build_review_target_next_wrong:{build_review_target.get('next_unit_id')}")
    for key in [
        "does_not_authorize_runtime_adoption",
        "does_not_authorize_schema_archive_mutation",
        "does_not_authorize_move_addition",
        "does_not_authorize_fixture_expansion",
    ]:
        if build_review_target.get(key) is not True:
            failures.append(f"build_review_target_{key}_not_true:{build_review_target.get(key)}")

    if build_authorization_target.get("build_authorization_id") != BUILD_AUTHORIZATION_ID:
        failures.append("source_build_authorization_target_id_wrong")
    if build_authorization_target.get("bounded_build_unit_authorized") is not True:
        failures.append("source_build_authorization_target_not_authorized")
    if implementation_review_summary.get("bounded_build_unit_authorized") is not True:
        failures.append("implementation_review_did_not_authorize_build_unit")

    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal.get("required_capability") != REQUIRED_CAPABILITY:
        failures.append(f"proposal_required_capability_wrong:{proposal.get('required_capability')}")
    if proposal.get("proposed_surface") != PROPOSED_SURFACE:
        failures.append(f"proposal_surface_wrong:{proposal.get('proposed_surface')}")
    if stop_packet.get("stop_code") != "STOP_CAPABILITY_LAYER_REQUIRED":
        failures.append(f"source_stop_code_wrong:{stop_packet.get('stop_code')}")

    profile_failures: List[str] = []
    if capability_profile.get("profile_status") != "BUILT_PENDING_REVIEW":
        profile_failures.append(f"profile_status_wrong:{capability_profile.get('profile_status')}")
    if capability_profile.get("capability_name") != REQUIRED_CAPABILITY:
        profile_failures.append("capability_name_wrong")
    if capability_profile.get("surface_name") != PROPOSED_SURFACE:
        profile_failures.append("surface_name_wrong")
    recognized = lower_list(capability_profile.get("recognized_evidence_families"))
    for item in [
        "structured_loop_trigger_surface",
        "structured_tie_evidence",
        "typed_absence_reason",
        "text_only_tie_residue_negative_control",
    ]:
        if item not in recognized:
            profile_failures.append(f"recognized_family_missing:{item}")
    states = capability_profile.get("admissible_surface_states") or []
    for item in [
        "STRUCTURED_TRIGGER_SURFACE_PRESENT",
        "STRUCTURED_TRIGGER_SURFACE_ABSENT_TYPED",
        "TEXT_ONLY_TIE_RESIDUE_ONLY",
        "UNDER_TYPED_EVIDENCE",
    ]:
        if item not in states:
            profile_failures.append(f"state_missing:{item}")

    schema_failures: List[str] = []
    if schema_candidate.get("schema_candidate_status") != "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION":
        schema_failures.append(f"schema_status_wrong:{schema_candidate.get('schema_candidate_status')}")
    if schema_candidate.get("schema_name") != PROPOSED_SURFACE:
        schema_failures.append("schema_name_wrong")
    required_fields = schema_candidate.get("required_fields") or {}
    for field in [
        "surface_id",
        "source_proposal_id",
        "source_stop_packet_id",
        "capability_name",
        "loop_trigger_surface",
        "tie_evidence",
        "text_only_residue",
        "classification",
        "evidence_refs",
        "boundary_flags",
    ]:
        if field not in required_fields:
            schema_failures.append(f"required_field_missing:{field}")
    if schema_candidate.get("archive_mutation_authorized") is not False:
        schema_failures.append("archive_mutation_authorized_unexpected")
    if schema_candidate.get("runtime_adoption_authorized") is not False:
        schema_failures.append("runtime_adoption_authorized_unexpected")

    evidence_failures: List[str] = []
    if evidence_shape.get("contract_status") != "BUILT_PENDING_REVIEW":
        evidence_failures.append(f"contract_status_wrong:{evidence_shape.get('contract_status')}")
    for top in [
        "structured_loop_trigger_surface_required_shape",
        "structured_tie_evidence_required_shape",
        "text_only_residue_shape",
    ]:
        if not isinstance(evidence_shape.get(top), dict):
            evidence_failures.append(f"shape_missing:{top}")
    suff = str(evidence_shape.get("sufficiency_rule", "")).lower()
    if "text-only residue is always negative control" not in suff:
        evidence_failures.append("sufficiency_rule_missing_text_only_negative_control")

    example_failures: List[str] = []
    if positive_example.get("classification") != "STRUCTURED_TRIGGER_SURFACE_PRESENT":
        example_failures.append("positive_classification_wrong")
    if positive_example.get("loop_trigger_surface", {}).get("present") is not True:
        example_failures.append("positive_loop_surface_not_present")
    if positive_example.get("tie_evidence", {}).get("present") is not True:
        example_failures.append("positive_tie_evidence_not_present")
    if positive_example.get("fixture_expansion_authorized") is not False:
        example_failures.append("positive_fixture_expansion_authorized_unexpected")
    if text_only_negative.get("classification") != "TEXT_ONLY_TIE_RESIDUE_ONLY":
        example_failures.append("negative_classification_wrong")
    if text_only_negative.get("expected_result") != "NEGATIVE_CONTROL_PASS":
        example_failures.append("negative_expected_result_wrong")
    if text_only_negative.get("loop_trigger_surface", {}).get("present") is not False:
        example_failures.append("negative_loop_surface_present_unexpected")
    if text_only_negative.get("tie_evidence", {}).get("present") is not False:
        example_failures.append("negative_tie_evidence_present_unexpected")
    if text_only_negative.get("text_only_residue", {}).get("present") is not True:
        example_failures.append("negative_text_only_residue_missing")
    if text_only_negative.get("text_only_residue", {}).get("is_sufficient_for_structured_trigger") is not False:
        example_failures.append("negative_text_only_residue_promoted_unexpected")
    if text_only_negative.get("fixture_expansion_authorized") is not False:
        example_failures.append("negative_fixture_expansion_authorized_unexpected")

    policy_failures: List[str] = []
    if classifier_policy.get("policy_status") != "BUILT_PENDING_REVIEW":
        policy_failures.append(f"policy_status_wrong:{classifier_policy.get('policy_status')}")
    rules = classifier_policy.get("classification_rules") or []
    classifications = {r.get("classification"): r for r in rules if isinstance(r, dict)}
    for cls in [
        "STRUCTURED_TRIGGER_SURFACE_PRESENT",
        "STRUCTURED_TRIGGER_SURFACE_ABSENT_TYPED",
        "TEXT_ONLY_TIE_RESIDUE_ONLY",
        "UNDER_TYPED_EVIDENCE",
    ]:
        if cls not in classifications:
            policy_failures.append(f"classification_rule_missing:{cls}")
    if classifications.get("TEXT_ONLY_TIE_RESIDUE_ONLY", {}).get("admissible_as_structured_trigger") is not False:
        policy_failures.append("text_only_rule_admissible_unexpected")
    if classifications.get("STRUCTURED_TRIGGER_SURFACE_PRESENT", {}).get("admissible_as_structured_trigger") is not True:
        policy_failures.append("positive_rule_not_admissible")
    if "no free-text detector residue can promote itself" not in str(classifier_policy.get("determinism_rule", "")).lower():
        policy_failures.append("determinism_rule_missing_no_text_promotion")

    api_failures: List[str] = []
    if api_contract.get("contract_status") != "BUILT_PENDING_REVIEW":
        api_failures.append(f"api_contract_status_wrong:{api_contract.get('contract_status')}")
    if api_contract.get("api_kind") != "representation_contract_only":
        api_failures.append("api_kind_wrong")
    forbidden = lower_list(api_contract.get("forbidden_side_effects"))
    for phrase in [
        "runtime mutation",
        "runtime adoption",
        "schema archive mutation",
        "move registry mutation",
        "fixture creation",
        "t6 live execution",
        "c8 authorization",
    ]:
        if phrase not in forbidden:
            api_failures.append(f"forbidden_side_effect_missing:{phrase}")

    test_failures: List[str] = []
    if test_expectations.get("expectation_status") != "BUILT_PENDING_REVIEW":
        test_failures.append(f"expectation_status_wrong:{test_expectations.get('expectation_status')}")
    tests = test_expectations.get("tests") or []
    test_ids = {t.get("test_id") for t in tests if isinstance(t, dict)}
    for test_id in [
        "positive_structured_trigger_surface_present",
        "negative_text_only_tie_residue_only",
        "missing_structured_evidence_typed_absence",
        "under_typed_evidence_blocks_progress",
    ]:
        if test_id not in test_ids:
            test_failures.append(f"test_missing:{test_id}")
    if test_expectations.get("runtime_execution_required") is not False:
        test_failures.append("runtime_execution_required_unexpected")

    negative_failures: List[str] = []
    if negative_control_result.get("result_status") != "PASS":
        negative_failures.append(f"negative_result_status_wrong:{negative_control_result.get('result_status')}")
    if negative_control_result.get("text_only_residue_promoted") is not False:
        negative_failures.append("text_only_residue_promoted_unexpected")
    if negative_control_result.get("positive_example_is_fixture_expansion") is not False:
        negative_failures.append("positive_example_is_fixture_expansion_unexpected")
    if negative_control_result.get("negative_example_is_fixture_expansion") is not False:
        negative_failures.append("negative_example_is_fixture_expansion_unexpected")
    zero_counters = negative_control_result.get("zero_counters_for_this_build") or {}
    for key in [
        "runtime_patch_count",
        "runtime_adoption_authority_count",
        "schema_archive_mutation_count",
        "move_registry_addition_count",
        "fixture_expansion_count",
        "t6_live_case_execution_count",
        "hidden_next_command_count",
        "c8_authorization_count",
    ]:
        if zero_counters.get(key) != 0:
            negative_failures.append(f"zero_counter_wrong:{key}:{zero_counters.get(key)}")

    if profile_failures:
        failures.append(f"profile_review_failures:{profile_failures}")
    if schema_failures:
        failures.append(f"schema_candidate_review_failures:{schema_failures}")
    if evidence_failures:
        failures.append(f"evidence_shape_review_failures:{evidence_failures}")
    if example_failures:
        failures.append(f"example_pair_review_failures:{example_failures}")
    if policy_failures:
        failures.append(f"classifier_policy_review_failures:{policy_failures}")
    if api_failures:
        failures.append(f"api_contract_review_failures:{api_failures}")
    if test_failures:
        failures.append(f"test_expectations_review_failures:{test_failures}")
    if negative_failures:
        failures.append(f"negative_control_review_failures:{negative_failures}")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_BUILD_REVIEW_PASS_ADOPTION_PATH_PREP_READY"
        if gate == "PASS"
        else "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_BUILD_REVIEW_GATE_FAIL"
    )

    adoption_path_id = "bounded_structured_t6_trigger_surface_capability_adoption_path_" + sig8({
        "capability_build_id": CAPABILITY_BUILD_ID,
        "build_authorization_id": BUILD_AUTHORIZATION_ID,
        "proposal_id": PROPOSAL_ID,
        "surface": PROPOSED_SURFACE,
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_review_basis_v0",
        "unit_id": UNIT_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "adoption_path_id": adoption_path_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_build_receipt_id": BUILD_RECEIPT_ID,
        "source_build_authorization_id": BUILD_AUTHORIZATION_ID,
        "source_proposal_id": PROPOSAL_ID,
        "review_claim": "Review bounded structured T6 trigger-surface capability artifacts. If clean, prepare adoption-path target only; do not adopt into runtime or mutate schema/move/fixture state.",
        "source_file_hashes": source_hashes,
    }

    capability_profile_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_profile_review_v0",
        "capability_build_id": CAPABILITY_BUILD_ID,
        "review_status": "PASS" if not profile_failures else "FAIL",
        "failures": profile_failures,
        "capability_name": capability_profile.get("capability_name"),
        "surface_name": capability_profile.get("surface_name"),
        "recognized_evidence_families": capability_profile.get("recognized_evidence_families"),
        "admissible_surface_states": capability_profile.get("admissible_surface_states"),
    }

    schema_candidate_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_candidate_review_v0",
        "capability_build_id": CAPABILITY_BUILD_ID,
        "review_status": "PASS" if not schema_failures else "FAIL",
        "failures": schema_failures,
        "schema_name": schema_candidate.get("schema_name"),
        "schema_candidate_status": schema_candidate.get("schema_candidate_status"),
        "archive_mutation_authorized": schema_candidate.get("archive_mutation_authorized"),
        "runtime_adoption_authorized": schema_candidate.get("runtime_adoption_authorized"),
    }

    evidence_shape_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_evidence_shape_contract_review_v0",
        "capability_build_id": CAPABILITY_BUILD_ID,
        "review_status": "PASS" if not evidence_failures else "FAIL",
        "failures": evidence_failures,
        "sufficiency_rule": evidence_shape.get("sufficiency_rule"),
    }

    example_pair_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_example_pair_review_v0",
        "capability_build_id": CAPABILITY_BUILD_ID,
        "review_status": "PASS" if not example_failures else "FAIL",
        "failures": example_failures,
        "positive_classification": positive_example.get("classification"),
        "negative_classification": text_only_negative.get("classification"),
        "negative_expected_result": text_only_negative.get("expected_result"),
        "text_only_residue_promoted": text_only_negative.get("text_only_residue", {}).get("is_sufficient_for_structured_trigger"),
        "fixture_expansion_authorized": False,
    }

    classifier_policy_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_classifier_policy_review_v0",
        "capability_build_id": CAPABILITY_BUILD_ID,
        "review_status": "PASS" if not policy_failures else "FAIL",
        "failures": policy_failures,
        "classification_count": len(classifier_policy.get("classification_rules") or []),
        "determinism_rule": classifier_policy.get("determinism_rule"),
    }

    api_contract_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_api_contract_review_v0",
        "capability_build_id": CAPABILITY_BUILD_ID,
        "review_status": "PASS" if not api_failures else "FAIL",
        "failures": api_failures,
        "api_kind": api_contract.get("api_kind"),
        "forbidden_side_effects": api_contract.get("forbidden_side_effects"),
    }

    test_expectations_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_test_expectations_review_v0",
        "capability_build_id": CAPABILITY_BUILD_ID,
        "review_status": "PASS" if not test_failures else "FAIL",
        "failures": test_failures,
        "test_count": len(test_expectations.get("tests") or []),
        "runtime_execution_required": test_expectations.get("runtime_execution_required"),
    }

    negative_control_review = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_negative_control_review_v0",
        "capability_build_id": CAPABILITY_BUILD_ID,
        "review_status": "PASS" if not negative_failures else "FAIL",
        "failures": negative_failures,
        "text_only_residue_promoted": negative_control_result.get("text_only_residue_promoted"),
        "zero_counters_for_this_build": zero_counters,
    }

    adoption_path_prep_target = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_adoption_path_prep_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "adoption_path_id": adoption_path_id,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "build_receipt_id": BUILD_RECEIPT_ID,
        "build_authorization_id": BUILD_AUTHORIZATION_ID,
        "implementation_path_id": IMPLEMENTATION_PATH_ID,
        "proposal_id": PROPOSAL_ID,
        "required_capability": REQUIRED_CAPABILITY,
        "proposed_surface": PROPOSED_SURFACE,
        "path_scope": "Prepare an adoption/promotion decision path for the reviewed bounded capability artifacts. Do not adopt into runtime, mutate schema archive, add moves, expand fixtures, or execute T6 live cases in the prep unit.",
        "possible_future_decision_surfaces": [
            "runtime adoption",
            "schema archive promotion",
            "move registry addition",
            "fixture/test expansion",
            "T6 live-case execution",
        ],
        "future_surfaces_require_separate_human_decision": True,
        "this_target_does_not_authorize": [
            "runtime adoption",
            "runtime patch",
            "schema archive mutation",
            "move registry addition",
            "fixture expansion",
            "T6 live case execution",
            "C8 authorization",
        ],
    }

    rollup = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_review_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "adoption_path_id": adoption_path_id,
        "proposal_id": PROPOSAL_ID,
        "artifact_review_pass": True if gate == "PASS" else False,
        "profile_review_pass": not profile_failures,
        "schema_candidate_review_pass": not schema_failures,
        "evidence_shape_review_pass": not evidence_failures,
        "example_pair_review_pass": not example_failures,
        "classifier_policy_review_pass": not policy_failures,
        "api_contract_review_pass": not api_failures,
        "test_expectations_review_pass": not test_failures,
        "negative_control_review_pass": not negative_failures,
        "adoption_path_prep_target_ready": True if gate == "PASS" else False,
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_review_readout_v0",
        "status": status,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "adoption_path_id": adoption_path_id,
        "proposal_id": PROPOSAL_ID,
        "interpretation": "Built bounded T6 capability artifacts reviewed cleanly. Adoption-path prep target emitted, but no runtime adoption, runtime patch, schema archive mutation, move addition, fixture expansion, T6 live execution, hidden next command, or C8 authorization occurred."
        if gate == "PASS" else "Bounded T6 capability build review failed typed gates.",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_review_profile_v0",
        "profile_status": status,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "core_rule": "Review artifacts only and prepare adoption-path target only. Artifact review is not runtime adoption or schema/move/fixture authority.",
        "adoption_path_prep_target_ref": rel(ADOPTION_PATH_PREP_TARGET_PATH),
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_review_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "review_result": "BUILD_ARTIFACTS_REVIEWED_ADOPTION_PATH_PREP_READY" if gate == "PASS" else "BUILD_REVIEW_GATE_FAIL",
            "capability_build_id": CAPABILITY_BUILD_ID,
            "adoption_path_id": adoption_path_id,
            "proposal_id": PROPOSAL_ID,
            "artifact_review_pass": gate == "PASS",
            "adoption_path_prep_target_ready": gate == "PASS",
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_review_transition_trace_v0",
        "unit_id": UNIT_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "transitions": [
            {
                "from": "BOUNDED_CAPABILITY_BUILD_REVIEW_READY",
                "edge": "review profile, schema candidate, evidence shape, examples, classifier policy, API contract, tests, and negative controls",
                "to": "BOUNDED_CAPABILITY_BUILD_REVIEW_PASS" if gate == "PASS" else "BOUNDED_CAPABILITY_BUILD_REVIEW_GATE_FAIL",
            },
            {
                "from": "BOUNDED_CAPABILITY_BUILD_REVIEW_PASS" if gate == "PASS" else "BOUNDED_CAPABILITY_BUILD_REVIEW_GATE_FAIL",
                "edge": "emit adoption-path prep target without adoption or widening",
                "to": "ADOPTION_PATH_PREP_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_BUILD_REVIEW_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (CAPABILITY_PROFILE_REVIEW_PATH, capability_profile_review),
        (SCHEMA_CANDIDATE_REVIEW_PATH, schema_candidate_review),
        (EVIDENCE_SHAPE_REVIEW_PATH, evidence_shape_review),
        (EXAMPLE_PAIR_REVIEW_PATH, example_pair_review),
        (CLASSIFIER_POLICY_REVIEW_PATH, classifier_policy_review),
        (API_CONTRACT_REVIEW_PATH, api_contract_review),
        (TEST_EXPECTATIONS_REVIEW_PATH, test_expectations_review),
        (NEGATIVE_CONTROL_REVIEW_PATH, negative_control_review),
        (ADOPTION_PATH_PREP_TARGET_PATH, adoption_path_prep_target),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "BUILD_RECEIPT_CONSUMED",
        "BUILD_REVIEW_TARGET_CONSUMED",
        "CAPABILITY_PROFILE_REVIEW_PASS",
        "SCHEMA_CANDIDATE_REVIEW_PASS_NOT_ARCHIVE_MUTATION",
        "EVIDENCE_SHAPE_REVIEW_PASS",
        "POSITIVE_NEGATIVE_EXAMPLE_PAIR_REVIEW_PASS",
        "CLASSIFIER_POLICY_REVIEW_PASS",
        "API_CONTRACT_REVIEW_PASS",
        "TEST_EXPECTATIONS_REVIEW_PASS",
        "NEGATIVE_CONTROL_REVIEW_PASS",
        "ADOPTION_PATH_PREP_TARGET_EMITTED",
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_build_review_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_BUILD_REVIEW_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "adoption_path_id": adoption_path_id,
        "source_build_receipt_id": BUILD_RECEIPT_ID,
        "source_build_receipt_ref": rel(BUILD_RECEIPT_PATH),
        "source_build_authorization_id": BUILD_AUTHORIZATION_ID,
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "BOUNDED_T6_BUILD_REVIEW_0_BUILD_RECEIPT_CONSUMED": gate == "PASS",
            "BOUNDED_T6_BUILD_REVIEW_1_BUILD_REVIEW_TARGET_CONSUMED": gate == "PASS",
            "BOUNDED_T6_BUILD_REVIEW_2_PROFILE_REVIEW_PASS": not profile_failures,
            "BOUNDED_T6_BUILD_REVIEW_3_SCHEMA_REVIEW_PASS": not schema_failures,
            "BOUNDED_T6_BUILD_REVIEW_4_EVIDENCE_SHAPE_REVIEW_PASS": not evidence_failures,
            "BOUNDED_T6_BUILD_REVIEW_5_EXAMPLE_PAIR_REVIEW_PASS": not example_failures,
            "BOUNDED_T6_BUILD_REVIEW_6_CLASSIFIER_POLICY_REVIEW_PASS": not policy_failures,
            "BOUNDED_T6_BUILD_REVIEW_7_API_CONTRACT_REVIEW_PASS": not api_failures,
            "BOUNDED_T6_BUILD_REVIEW_8_TEST_EXPECTATIONS_REVIEW_PASS": not test_failures,
            "BOUNDED_T6_BUILD_REVIEW_9_NEGATIVE_CONTROL_REVIEW_PASS": not negative_failures,
            "BOUNDED_T6_BUILD_REVIEW_10_ADOPTION_PATH_PREP_TARGET_EMITTED": ADOPTION_PATH_PREP_TARGET_PATH.exists() and gate == "PASS",
            "BOUNDED_T6_BUILD_REVIEW_11_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "BOUNDED_T6_BUILD_REVIEW_12_NO_RUNTIME_PATCH": True,
            "BOUNDED_T6_BUILD_REVIEW_13_NO_SCHEMA_ARCHIVE_MUTATION": True,
            "BOUNDED_T6_BUILD_REVIEW_14_NO_MOVE_ADDITION": True,
            "BOUNDED_T6_BUILD_REVIEW_15_NO_FIXTURE_EXPANSION": True,
            "BOUNDED_T6_BUILD_REVIEW_16_NO_T6_LIVE_CASE_EXECUTION": True,
            "BOUNDED_T6_BUILD_REVIEW_17_NO_C8_AUTHORIZATION": True,
            "BOUNDED_T6_BUILD_REVIEW_18_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_structured_t6_trigger_surface_capability_build_review_summary": {
            "status": status,
            "capability_build_id": CAPABILITY_BUILD_ID,
            "adoption_path_id": adoption_path_id,
            "build_authorization_id": BUILD_AUTHORIZATION_ID,
            "implementation_path_id": IMPLEMENTATION_PATH_ID,
            "proposal_id": PROPOSAL_ID,
            "required_capability": REQUIRED_CAPABILITY,
            "proposed_surface": PROPOSED_SURFACE,
            "artifact_review_pass": True if gate == "PASS" else False,
            "profile_review_pass": not profile_failures,
            "schema_candidate_review_pass": not schema_failures,
            "evidence_shape_review_pass": not evidence_failures,
            "example_pair_review_pass": not example_failures,
            "classifier_policy_review_pass": not policy_failures,
            "api_contract_review_pass": not api_failures,
            "test_expectations_review_pass": not test_failures,
            "negative_control_review_pass": not negative_failures,
            "adoption_path_prep_target_ready": True if gate == "PASS" else False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "runtime_adoption_authorized": False,
            "runtime_patch_authorized": False,
            "schema_archive_mutation_authorized": False,
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
            "capability_profile_review": rel(CAPABILITY_PROFILE_REVIEW_PATH),
            "schema_candidate_review": rel(SCHEMA_CANDIDATE_REVIEW_PATH),
            "evidence_shape_review": rel(EVIDENCE_SHAPE_REVIEW_PATH),
            "example_pair_review": rel(EXAMPLE_PAIR_REVIEW_PATH),
            "classifier_policy_review": rel(CLASSIFIER_POLICY_REVIEW_PATH),
            "api_contract_review": rel(API_CONTRACT_REVIEW_PATH),
            "test_expectations_review": rel(TEST_EXPECTATIONS_REVIEW_PATH),
            "negative_control_review": rel(NEGATIVE_CONTROL_REVIEW_PATH),
            "adoption_path_prep_target": rel(ADOPTION_PATH_PREP_TARGET_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_structured_t6_trigger_surface_capability_build_review_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_structured_t6_trigger_surface_capability_build_review_receipt_id={receipt_id}")
    print(f"bounded_structured_t6_trigger_surface_capability_build_review_receipt_path={rel(receipt_path)}")
    print(f"bounded_structured_t6_trigger_surface_capability_adoption_path_id={adoption_path_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_build_review_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
