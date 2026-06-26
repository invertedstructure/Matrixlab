#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_V0"
TARGET_UNIT_ID = "bounded_structured_t6_trigger_surface_capability.schema_archive_promotion_decision_packet_v0"

SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_receipt_4d152a3e"
SCHEMA_PROMOTION_HUMAN_DECISION_RECORD_ID = "bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_362616fe"
SCHEMA_PROMOTION_PACKET_PREP_TARGET_ID = "bounded_structured_t6_trigger_surface_capability_schema_promotion_packet_prep_target_373afac2"
SELECTED_PATH_DECISION = "PREPARE_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET"

HUMAN_DECISION_PACKET_ID = "bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_38ae00c0"
ADOPTION_PATH_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_6f9974e5"
CAPABILITY_BUILD_ID = "bounded_structured_t6_trigger_surface_capability_build_721f09dc"
PROPOSAL_ID = "capability_proposal_57dda6e9"
REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"

SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_schema_promotion_path_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_receipt_4d152a3e.json"
SCHEMA_PROMOTION_PACKET_PREP_TARGET_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_schema_promotion_path_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_prep_target_v0.json"
SCHEMA_PROMOTION_DECISION_RECORD_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_schema_promotion_path_v0/bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_record_v0.json"
SCHEMA_PROMOTION_DECISION_EFFECT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_schema_promotion_path_v0/bounded_structured_t6_trigger_surface_capability_schema_promotion_decision_effect_applied_v0.json"
SCHEMA_PROMOTION_AUTHORITY_BOUNDARY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_schema_promotion_path_v0/bounded_structured_t6_trigger_surface_capability_schema_promotion_decision_authority_boundary_review_v0.json"
SCHEMA_PROMOTION_NEGATIVE_CONTROL_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_schema_promotion_path_v0/bounded_structured_t6_trigger_surface_capability_schema_promotion_decision_negative_control_v0.json"

HUMAN_DECISION_PACKET_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_v0_receipts/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_receipt_52138534.json"
ADOPTION_PATH_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_adoption_path_review_receipt_ec071b02.json"
ADOPTION_PATH_PREP_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0_receipts/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_receipt_34a6f83a.json"
SCHEMA_PROMOTION_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_path_prep_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_candidate_v0.json"

BUILD_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_review_receipt_b8dba552.json"
BUILD_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079.json"

SCHEMA_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_schema_candidate_v0.json"
CAPABILITY_PROFILE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_profile_v0.json"
EVIDENCE_SHAPE_CONTRACT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_evidence_shape_contract_v0.json"
CLASSIFIER_POLICY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_classifier_policy_v0.json"
API_CONTRACT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_api_contract_v0.json"
TEST_EXPECTATIONS_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_test_expectations_v0.json"
NEGATIVE_CONTROL_RESULT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_negative_control_result_v0.json"

PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"

OUT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_v0"
RECEIPT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_basis_v0.json"
SOURCE_CHAIN_BINDING_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_source_chain_binding_v0.json"
SCHEMA_CANDIDATE_BINDING_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_schema_candidate_binding_v0.json"
PROMOTION_SCOPE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_scope_v0.json"
PROMOTION_AUTHORITY_BOUNDARY_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_authority_boundary_v0.json"
PROMOTION_DECISION_OPTIONS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_options_v0.json"
PROMOTION_EFFECTS_MAP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_effects_map_v0.json"
PROMOTION_ACCEPT_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_option_accept_v0.json"
PROMOTION_DEFER_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_option_defer_v0.json"
PROMOTION_FREEZE_REFERENCE_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_option_freeze_reference_only_v0.json"
PROMOTION_REJECT_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_option_reject_v0.json"
PROMOTION_CLOSE_OPTION_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_option_close_no_mutation_v0.json"
PROMOTION_REQUEST_PACKET_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_human_decision_request_packet_v0.json"
PROMOTION_NEGATIVE_CONTROL_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_negative_control_v0.json"
READOUT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_transition_trace.json"

STOP_CODE = "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_HUMAN_DECISION_REQUIRED"

DECISION_OPTIONS = [
    "ACCEPT_SCHEMA_ARCHIVE_PROMOTION_FOR_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY",
    "DEFER_SCHEMA_ARCHIVE_PROMOTION_DECISION",
    "FREEZE_SCHEMA_CANDIDATE_AS_REFERENCE_ONLY",
    "REJECT_SCHEMA_ARCHIVE_PROMOTION",
    "CLOSE_SCHEMA_PROMOTION_PATH_NO_MUTATION",
]

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
        SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_PATH,
        SCHEMA_PROMOTION_PACKET_PREP_TARGET_PATH,
        SCHEMA_PROMOTION_DECISION_RECORD_PATH,
        SCHEMA_PROMOTION_DECISION_EFFECT_PATH,
        SCHEMA_PROMOTION_AUTHORITY_BOUNDARY_PATH,
        SCHEMA_PROMOTION_NEGATIVE_CONTROL_PATH,
        HUMAN_DECISION_PACKET_RECEIPT_PATH,
        ADOPTION_PATH_REVIEW_RECEIPT_PATH,
        ADOPTION_PATH_PREP_RECEIPT_PATH,
        SCHEMA_PROMOTION_CANDIDATE_PATH,
        BUILD_REVIEW_RECEIPT_PATH,
        BUILD_RECEIPT_PATH,
        SCHEMA_CANDIDATE_PATH,
        CAPABILITY_PROFILE_PATH,
        EVIDENCE_SHAPE_CONTRACT_PATH,
        CLASSIFIER_POLICY_PATH,
        API_CONTRACT_PATH,
        TEST_EXPECTATIONS_PATH,
        NEGATIVE_CONTROL_RESULT_PATH,
        PROPOSAL_PATH,
    ]

    failures: List[str] = []
    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    schema_promotion_receipt = read_json(SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_PATH)
    prep_target = read_json(SCHEMA_PROMOTION_PACKET_PREP_TARGET_PATH)
    decision_record_src = read_json(SCHEMA_PROMOTION_DECISION_RECORD_PATH)
    decision_effect_src = read_json(SCHEMA_PROMOTION_DECISION_EFFECT_PATH)
    authority_boundary_src = read_json(SCHEMA_PROMOTION_AUTHORITY_BOUNDARY_PATH)
    negative_control_src = read_json(SCHEMA_PROMOTION_NEGATIVE_CONTROL_PATH)

    human_packet_receipt = read_json(HUMAN_DECISION_PACKET_RECEIPT_PATH)
    adoption_review_receipt = read_json(ADOPTION_PATH_REVIEW_RECEIPT_PATH)
    adoption_prep_receipt = read_json(ADOPTION_PATH_PREP_RECEIPT_PATH)
    schema_promotion_candidate = read_json(SCHEMA_PROMOTION_CANDIDATE_PATH)
    build_review_receipt = read_json(BUILD_REVIEW_RECEIPT_PATH)
    build_receipt = read_json(BUILD_RECEIPT_PATH)

    schema_candidate = read_json(SCHEMA_CANDIDATE_PATH)
    capability_profile = read_json(CAPABILITY_PROFILE_PATH)
    evidence_shape = read_json(EVIDENCE_SHAPE_CONTRACT_PATH)
    classifier_policy = read_json(CLASSIFIER_POLICY_PATH)
    api_contract = read_json(API_CONTRACT_PATH)
    test_expectations = read_json(TEST_EXPECTATIONS_PATH)
    negative_control_result = read_json(NEGATIVE_CONTROL_RESULT_PATH)
    proposal = read_json(PROPOSAL_PATH)

    promotion_summary = schema_promotion_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_summary", {})
    human_packet_summary = human_packet_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_adoption_human_decision_packet_summary", {})
    adoption_review_summary = adoption_review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_adoption_path_review_summary", {})
    adoption_prep_summary = adoption_prep_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_adoption_path_prep_summary", {})
    build_review_summary = build_review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_review_summary", {})
    build_summary = build_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_summary", {})

    if schema_promotion_receipt.get("receipt_id") != SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_ID:
        failures.append(f"schema_promotion_receipt_id_wrong:{schema_promotion_receipt.get('receipt_id')}")
    if schema_promotion_receipt.get("gate") != "PASS":
        failures.append("schema_promotion_receipt_gate_not_pass")
    if schema_promotion_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"schema_promotion_terminal_next_wrong:{schema_promotion_receipt.get('terminal', {}).get('next_unit_id')}")

    for key in [
        "human_adoption_decision_taken",
        "schema_promotion_decision_packet_prep_authorized",
        "schema_archive_promotion_decision_packet_prep_target_ready",
    ]:
        if promotion_summary.get(key) is not True:
            failures.append(f"promotion_summary_{key}_not_true:{promotion_summary.get(key)}")

    if promotion_summary.get("selected_adoption_decision") != SELECTED_PATH_DECISION:
        failures.append(f"selected_path_decision_wrong:{promotion_summary.get('selected_adoption_decision')}")
    if promotion_summary.get("schema_archive_promotion_decision_packet_prep_target_id") != SCHEMA_PROMOTION_PACKET_PREP_TARGET_ID:
        failures.append("promotion_target_id_wrong")

    for key in FORBIDDEN_FALSE_KEYS:
        require_false(promotion_summary, key, failures, "promotion_summary")

    if prep_target.get("target_status") != "READY":
        failures.append(f"prep_target_status_wrong:{prep_target.get('target_status')}")
    if prep_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"prep_target_next_wrong:{prep_target.get('next_unit_id')}")
    if prep_target.get("schema_archive_promotion_decision_packet_prep_target_id") != SCHEMA_PROMOTION_PACKET_PREP_TARGET_ID:
        failures.append("prep_target_id_wrong")
    if prep_target.get("human_decision_required_later_for_actual_schema_archive_mutation") is not True:
        failures.append("prep_target_later_human_decision_not_required")
    if prep_target.get("schema_archive_mutation_authorized") is not False:
        failures.append("prep_target_schema_archive_mutation_authorized_unexpected")
    if prep_target.get("schema_mutation_authorized") is not False:
        failures.append("prep_target_schema_mutation_authorized_unexpected")

    if decision_record_src.get("decision_record_status") != "HUMAN_DECISION_RECORDED":
        failures.append("source_decision_record_not_recorded")
    if decision_record_src.get("selected_decision") != SELECTED_PATH_DECISION:
        failures.append("source_decision_record_selected_wrong")
    if decision_effect_src.get("schema_promotion_decision_packet_prep_authorized") is not True:
        failures.append("source_effect_prep_not_authorized")
    for key in FORBIDDEN_FALSE_KEYS:
        require_false(decision_effect_src, key, failures, "source_effect")

    if authority_boundary_src.get("review_status") != "PASS":
        failures.append("source_authority_boundary_not_pass")
    if negative_control_src.get("negative_control_status") != "PASS":
        failures.append("source_negative_control_not_pass")
    for counter_key in [
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
        if negative_control_src.get(counter_key) != 0:
            failures.append(f"source_negative_counter_wrong:{counter_key}:{negative_control_src.get(counter_key)}")

    if human_packet_summary.get("human_decision_packet_ready") is not True:
        failures.append("source_human_packet_not_ready")
    if adoption_review_summary.get("adoption_path_review_pass") is not True:
        failures.append("source_adoption_review_not_pass")
    if adoption_prep_summary.get("adoption_path_prepared") is not True:
        failures.append("source_adoption_path_not_prepared")
    if build_review_summary.get("artifact_review_pass") is not True:
        failures.append("source_build_review_not_pass")
    if build_summary.get("build_executed") is not True:
        failures.append("source_build_not_executed")

    if schema_promotion_candidate.get("candidate_status") != "CANDIDATE_ONLY_NOT_AUTHORIZED":
        failures.append(f"schema_promotion_candidate_status_wrong:{schema_promotion_candidate.get('candidate_status')}")
    if schema_promotion_candidate.get("schema_archive_mutation_authorized") is not False:
        failures.append("schema_promotion_candidate_archive_mutation_authorized_unexpected")
    if schema_promotion_candidate.get("schema_mutation_authorized") is not False:
        failures.append("schema_promotion_candidate_schema_mutation_authorized_unexpected")

    if schema_candidate.get("schema_candidate_status") != "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION":
        failures.append(f"schema_candidate_status_wrong:{schema_candidate.get('schema_candidate_status')}")
    if schema_candidate.get("archive_mutation_authorized") is not False:
        failures.append("schema_candidate_archive_mutation_authorized_unexpected")
    if schema_candidate.get("runtime_adoption_authorized") is not False:
        failures.append("schema_candidate_runtime_adoption_authorized_unexpected")
    if schema_candidate.get("schema_name") != PROPOSED_SURFACE:
        failures.append(f"schema_candidate_name_wrong:{schema_candidate.get('schema_name')}")

    if capability_profile.get("capability_name") != REQUIRED_CAPABILITY:
        failures.append(f"capability_name_wrong:{capability_profile.get('capability_name')}")
    if capability_profile.get("surface_name") != PROPOSED_SURFACE:
        failures.append(f"surface_name_wrong:{capability_profile.get('surface_name')}")
    if api_contract.get("api_kind") != "representation_contract_only":
        failures.append(f"api_kind_wrong:{api_contract.get('api_kind')}")
    if test_expectations.get("runtime_execution_required") is not False:
        failures.append("test_expectations_runtime_required_unexpected")
    if negative_control_result.get("result_status") != "PASS":
        failures.append("source_capability_negative_control_not_pass")
    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_PASS_DECISION_REQUIRED"
        if gate == "PASS"
        else "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_GATE_FAIL"
    )

    promotion_decision_packet_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_" + sig8({
        "source_human_decision_record_id": SCHEMA_PROMOTION_HUMAN_DECISION_RECORD_ID,
        "schema_candidate": PROPOSED_SURFACE,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "decision_options": DECISION_OPTIONS,
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_basis_v0",
        "unit_id": UNIT_ID,
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_schema_promotion_human_decision_receipt_id": SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_ID,
        "source_human_decision_record_id": SCHEMA_PROMOTION_HUMAN_DECISION_RECORD_ID,
        "source_schema_promotion_packet_prep_target_id": SCHEMA_PROMOTION_PACKET_PREP_TARGET_ID,
        "source_capability_build_id": CAPABILITY_BUILD_ID,
        "source_proposal_id": PROPOSAL_ID,
        "prep_claim": "Prepare schema archive promotion human decision packet only. Do not mutate or promote schema archive.",
        "source_file_hashes": source_hashes,
    }

    source_chain_binding = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_source_chain_binding_v0",
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "binding_status": "PASS" if gate == "PASS" else "BLOCKED",
        "source_human_decision_record_id": SCHEMA_PROMOTION_HUMAN_DECISION_RECORD_ID,
        "selected_path_decision": SELECTED_PATH_DECISION,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "all_source_receipts_passed": True if gate == "PASS" else False,
    }

    schema_candidate_binding = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_schema_candidate_binding_v0",
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "binding_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "schema_name": schema_candidate.get("schema_name"),
        "schema_candidate_status": schema_candidate.get("schema_candidate_status"),
        "object_kind": schema_candidate.get("object_kind"),
        "required_fields": schema_candidate.get("required_fields"),
        "classification_enum": schema_candidate.get("classification_enum"),
        "source_schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
    }

    promotion_scope = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_scope_v0",
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "scope_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "decision_question": "Should the reviewed bounded structured T6 trigger-surface schema candidate be promoted toward schema archive mutation?",
        "in_scope": [
            "present schema candidate",
            "present schema promotion effects",
            "ask for human decision",
            "stop without schema archive mutation",
        ],
        "not_in_scope": [
            "mutate schema archive",
            "promote schema archive entry",
            "runtime adoption",
            "runtime patch",
            "move addition",
            "fixture expansion",
            "T6 live case execution",
            "C8 authorization",
        ],
    }

    promotion_authority_boundary = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_authority_boundary_v0",
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "boundary_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "human_schema_promotion_decision_required": True if gate == "PASS" else False,
        "human_schema_promotion_decision_taken": False,
        "selected_schema_promotion_decision": None,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "boundary_rule": "This packet requests a schema-promotion human decision. It does not itself mutate or promote the schema archive.",
    }

    promotion_decision_options = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_options_v0",
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "options_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "selected_schema_promotion_decision": None,
        "decision_options": [
            {
                "decision": "ACCEPT_SCHEMA_ARCHIVE_PROMOTION_FOR_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY",
                "meaning": "Authorize preparing the bounded schema archive mutation target for this reviewed schema candidate.",
                "does_not_mutate_schema_archive_now": True,
            },
            {
                "decision": "DEFER_SCHEMA_ARCHIVE_PROMOTION_DECISION",
                "meaning": "Keep schema promotion path open without preparing mutation target.",
                "does_not_mutate_schema_archive_now": True,
            },
            {
                "decision": "FREEZE_SCHEMA_CANDIDATE_AS_REFERENCE_ONLY",
                "meaning": "Keep the schema candidate as reference-only and do not promote.",
                "does_not_mutate_schema_archive_now": True,
            },
            {
                "decision": "REJECT_SCHEMA_ARCHIVE_PROMOTION",
                "meaning": "Reject schema archive promotion for this candidate.",
                "does_not_mutate_schema_archive_now": True,
            },
            {
                "decision": "CLOSE_SCHEMA_PROMOTION_PATH_NO_MUTATION",
                "meaning": "Close this schema promotion path without mutation.",
                "does_not_mutate_schema_archive_now": True,
            },
        ],
    }

    promotion_effects_map = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_effects_map_v0",
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "effects_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "effect_rule": "A future selected decision may authorize only its next bounded recording/target unit. This decision packet performs no mutation.",
        "decision_effects": {
            "ACCEPT_SCHEMA_ARCHIVE_PROMOTION_FOR_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY": {
                "next_surface": "schema archive mutation target preparation",
                "schema_archive_mutation_authorized_by_packet": False,
                "requires_later_recorded_human_decision": True,
            },
            "DEFER_SCHEMA_ARCHIVE_PROMOTION_DECISION": {
                "next_surface": "defer/hold",
                "schema_archive_mutation_authorized": False,
            },
            "FREEZE_SCHEMA_CANDIDATE_AS_REFERENCE_ONLY": {
                "next_surface": "reference-only freeze",
                "schema_archive_mutation_authorized": False,
            },
            "REJECT_SCHEMA_ARCHIVE_PROMOTION": {
                "next_surface": "reject promotion",
                "schema_archive_mutation_authorized": False,
            },
            "CLOSE_SCHEMA_PROMOTION_PATH_NO_MUTATION": {
                "next_surface": "close no-mutation",
                "schema_archive_mutation_authorized": False,
            },
        },
    }

    option_accept = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_option_accept_v0",
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "option": "ACCEPT_SCHEMA_ARCHIVE_PROMOTION_FOR_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY",
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "would_authorize_later": "schema archive mutation target preparation",
        "schema_archive_mutation_authorized_now": False,
    }

    option_defer = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_option_defer_v0",
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "option": "DEFER_SCHEMA_ARCHIVE_PROMOTION_DECISION",
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "schema_archive_mutation_authorized": False,
    }

    option_freeze = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_option_freeze_reference_only_v0",
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "option": "FREEZE_SCHEMA_CANDIDATE_AS_REFERENCE_ONLY",
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "schema_archive_mutation_authorized": False,
    }

    option_reject = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_option_reject_v0",
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "option": "REJECT_SCHEMA_ARCHIVE_PROMOTION",
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "schema_archive_mutation_authorized": False,
    }

    option_close = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_option_close_no_mutation_v0",
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "option": "CLOSE_SCHEMA_PROMOTION_PATH_NO_MUTATION",
        "option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
        "selected": False,
        "schema_archive_mutation_authorized": False,
    }

    promotion_request_packet = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_human_decision_request_packet_v0",
        "packet_status": "READY_FOR_HUMAN_DECISION" if gate == "PASS" else "BLOCKED",
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "source_human_decision_record_id": SCHEMA_PROMOTION_HUMAN_DECISION_RECORD_ID,
        "schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "schema_candidate_status": schema_candidate.get("schema_candidate_status"),
        "schema_name": schema_candidate.get("schema_name"),
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "decision_question": "Promote this bounded structured T6 trigger-surface schema candidate toward schema archive mutation?",
        "available_decisions": DECISION_OPTIONS,
        "selected_schema_promotion_decision": None,
        "human_schema_promotion_decision_taken": False,
        "decision_boundary": "This packet requests a decision only. Accepting later authorizes a bounded mutation target path; this packet does not mutate or promote the schema archive.",
        "must_remain_false_until_recorded_decision": FORBIDDEN_FALSE_KEYS,
    }

    promotion_negative_control = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_negative_control_v0",
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "negative_control_status": "PASS" if gate == "PASS" else "BLOCKED",
        "human_schema_promotion_decision_taken": False,
        "selected_schema_promotion_decision": None,
        "zero_counters_for_this_unit": {
            "schema_archive_mutation_count": 0,
            "schema_mutation_count": 0,
            "runtime_adoption_count": 0,
            "runtime_patch_count": 0,
            "move_addition_count": 0,
            "fixture_expansion_count": 0,
            "t6_live_case_execution_count": 0,
            "hidden_next_command_count": 0,
            "c8_authorization_count": 0,
        },
        "negative_control_rule": "Preparing the schema promotion decision packet is not schema archive mutation.",
    }

    rollup = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "source_human_decision_record_id": SCHEMA_PROMOTION_HUMAN_DECISION_RECORD_ID,
        "schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "schema_candidate_status": schema_candidate.get("schema_candidate_status"),
        "human_schema_promotion_decision_required": True if gate == "PASS" else False,
        "human_schema_promotion_decision_taken": False,
        "selected_schema_promotion_decision": None,
        "available_decision_count": len(DECISION_OPTIONS) if gate == "PASS" else 0,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "terminal_stop_code": STOP_CODE if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_GATE_FAIL",
    }

    readout = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_readout_v0",
        "status": status,
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "interpretation": "Schema archive promotion decision packet is ready. No schema archive mutation or schema promotion occurred."
        if gate == "PASS" else "Schema archive promotion decision packet preparation failed typed gates.",
        "stop_code": STOP_CODE if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_GATE_FAIL",
    }

    profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_profile_v0",
        "profile_status": status,
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "core_rule": "Ask for schema promotion decision and stop. Do not mutate or promote schema archive in this unit.",
        "human_decision_request_packet_ref": rel(PROMOTION_REQUEST_PACKET_PATH),
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
            "human schema promotion decision taken",
        ],
    }

    report = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "packet_result": "SCHEMA_ARCHIVE_PROMOTION_HUMAN_DECISION_REQUIRED" if gate == "PASS" else "SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_GATE_FAIL",
            "promotion_decision_packet_id": promotion_decision_packet_id,
            "source_human_decision_record_id": SCHEMA_PROMOTION_HUMAN_DECISION_RECORD_ID,
            "schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
            "available_decisions": DECISION_OPTIONS if gate == "PASS" else [],
            "human_schema_promotion_decision_taken": False,
            "selected_schema_promotion_decision": None,
            "schema_archive_mutation_authorized": False,
            "schema_mutation_authorized": False,
            "runtime_adoption_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "t6_live_case_execution_authorized": False,
            "c8_authorized": False,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_transition_trace_v0",
        "unit_id": UNIT_ID,
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "transitions": [
            {
                "from": "SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_PREP_READY",
                "edge": "prepare schema archive promotion human decision packet",
                "to": "SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_READY" if gate == "PASS" else "SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_GATE_FAIL",
            },
            {
                "from": "SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_READY" if gate == "PASS" else "SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_GATE_FAIL",
                "edge": "stop for human schema promotion decision without mutation",
                "to": "STOP_SCHEMA_ARCHIVE_PROMOTION_HUMAN_DECISION_REQUIRED" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "STOP",
            "next_unit_id": None,
            "stop_code": STOP_CODE if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (SOURCE_CHAIN_BINDING_PATH, source_chain_binding),
        (SCHEMA_CANDIDATE_BINDING_PATH, schema_candidate_binding),
        (PROMOTION_SCOPE_PATH, promotion_scope),
        (PROMOTION_AUTHORITY_BOUNDARY_PATH, promotion_authority_boundary),
        (PROMOTION_DECISION_OPTIONS_PATH, promotion_decision_options),
        (PROMOTION_EFFECTS_MAP_PATH, promotion_effects_map),
        (PROMOTION_ACCEPT_OPTION_PATH, option_accept),
        (PROMOTION_DEFER_OPTION_PATH, option_defer),
        (PROMOTION_FREEZE_REFERENCE_OPTION_PATH, option_freeze),
        (PROMOTION_REJECT_OPTION_PATH, option_reject),
        (PROMOTION_CLOSE_OPTION_PATH, option_close),
        (PROMOTION_REQUEST_PACKET_PATH, promotion_request_packet),
        (PROMOTION_NEGATIVE_CONTROL_PATH, promotion_negative_control),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_CONSUMED",
        "SCHEMA_PROMOTION_PACKET_PREP_TARGET_CONSUMED",
        "SCHEMA_CANDIDATE_BOUND",
        "PROMOTION_DECISION_OPTIONS_EMITTED",
        "PROMOTION_EFFECTS_MAP_EMITTED",
        "PROMOTION_AUTHORITY_BOUNDARY_EMITTED",
        "PROMOTION_HUMAN_DECISION_REQUEST_PACKET_READY",
        "NEGATIVE_CONTROL_PASS",
        "STOP_SCHEMA_ARCHIVE_PROMOTION_HUMAN_DECISION_REQUIRED",
        "NO_HUMAN_SCHEMA_PROMOTION_DECISION_TAKEN",
        "NO_SELECTED_SCHEMA_PROMOTION_DECISION",
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_PROMOTION_DECISION_PACKET_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "promotion_decision_packet_id": promotion_decision_packet_id,
        "source_schema_promotion_human_decision_receipt_id": SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_ID,
        "source_schema_promotion_human_decision_receipt_ref": rel(SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_PATH),
        "source_human_decision_record_id": SCHEMA_PROMOTION_HUMAN_DECISION_RECORD_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_0_SOURCE_DECISION_RECEIPT_CONSUMED": gate == "PASS",
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_1_PREP_TARGET_CONSUMED": gate == "PASS",
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_2_SCHEMA_CANDIDATE_BOUND": gate == "PASS",
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_3_OPTIONS_EMITTED": PROMOTION_DECISION_OPTIONS_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_4_EFFECTS_MAP_EMITTED": PROMOTION_EFFECTS_MAP_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_5_REQUEST_PACKET_READY": PROMOTION_REQUEST_PACKET_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_6_NEGATIVE_CONTROL_PASS": PROMOTION_NEGATIVE_CONTROL_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_7_NO_HUMAN_SCHEMA_PROMOTION_DECISION_TAKEN": True,
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_8_NO_SELECTED_DECISION": True,
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_9_NO_SCHEMA_ARCHIVE_MUTATION": True,
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_10_NO_SCHEMA_MUTATION": True,
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_11_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_12_NO_RUNTIME_PATCH": True,
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_13_NO_MOVE_ADDITION": True,
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_14_NO_FIXTURE_EXPANSION": True,
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_15_NO_T6_LIVE_CASE_EXECUTION": True,
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_16_NO_C8_AUTHORIZATION": True,
            "SCHEMA_ARCHIVE_PROMOTION_PACKET_17_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_summary": {
            "status": status,
            "promotion_decision_packet_id": promotion_decision_packet_id,
            "source_human_decision_record_id": SCHEMA_PROMOTION_HUMAN_DECISION_RECORD_ID,
            "source_schema_promotion_human_decision_receipt_id": SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_ID,
            "adoption_path_id": ADOPTION_PATH_ID,
            "capability_build_id": CAPABILITY_BUILD_ID,
            "proposal_id": PROPOSAL_ID,
            "required_capability": REQUIRED_CAPABILITY,
            "proposed_surface": PROPOSED_SURFACE,
            "schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
            "schema_candidate_status": schema_candidate.get("schema_candidate_status"),
            "schema_archive_promotion_decision_packet_ready": True if gate == "PASS" else False,
            "human_schema_promotion_decision_required": True if gate == "PASS" else False,
            "human_schema_promotion_decision_taken": False,
            "selected_schema_promotion_decision": None,
            "available_decisions": DECISION_OPTIONS if gate == "PASS" else [],
            "available_decision_count": len(DECISION_OPTIONS) if gate == "PASS" else 0,
            "accept_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "defer_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "freeze_reference_only_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "reject_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "close_no_mutation_option_status": "AVAILABLE_NOT_SELECTED" if gate == "PASS" else "BLOCKED",
            "schema_archive_mutation_authorized": False,
            "schema_mutation_authorized": False,
            "runtime_adoption_authorized": False,
            "runtime_patch_authorized": False,
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
            "source_chain_binding": rel(SOURCE_CHAIN_BINDING_PATH),
            "schema_candidate_binding": rel(SCHEMA_CANDIDATE_BINDING_PATH),
            "promotion_scope": rel(PROMOTION_SCOPE_PATH),
            "promotion_authority_boundary": rel(PROMOTION_AUTHORITY_BOUNDARY_PATH),
            "promotion_decision_options": rel(PROMOTION_DECISION_OPTIONS_PATH),
            "promotion_effects_map": rel(PROMOTION_EFFECTS_MAP_PATH),
            "promotion_accept_option": rel(PROMOTION_ACCEPT_OPTION_PATH),
            "promotion_defer_option": rel(PROMOTION_DEFER_OPTION_PATH),
            "promotion_freeze_reference_option": rel(PROMOTION_FREEZE_REFERENCE_OPTION_PATH),
            "promotion_reject_option": rel(PROMOTION_REJECT_OPTION_PATH),
            "promotion_close_option": rel(PROMOTION_CLOSE_OPTION_PATH),
            "promotion_request_packet": rel(PROMOTION_REQUEST_PACKET_PATH),
            "promotion_negative_control": rel(PROMOTION_NEGATIVE_CONTROL_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_receipt_id={receipt_id}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_receipt_path={rel(receipt_path)}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_id={promotion_decision_packet_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_terminal_stop_code={transition_trace['terminal']['stop_code']}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
