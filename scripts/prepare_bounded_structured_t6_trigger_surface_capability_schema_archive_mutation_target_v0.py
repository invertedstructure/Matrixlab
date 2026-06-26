#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_MUTATION_TARGET_V0"
TARGET_UNIT_ID = "bounded_structured_t6_trigger_surface_capability.schema_archive_mutation_target_v0"
NEXT_UNIT_ID = "REVIEW_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_MUTATION_TARGET_V0"

ACCEPT_DECISION_RECEIPT_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_receipt_5641e392"
ACCEPT_DECISION_RECORD_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_a0d0c10d"
MUTATION_TARGET_PREP_TARGET_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_prep_ad5932d2"
PROMOTION_DECISION_PACKET_ID = "bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_ca415d65"
SELECTED_SCHEMA_PROMOTION_DECISION = "ACCEPT_SCHEMA_ARCHIVE_PROMOTION_FOR_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY"

ADOPTION_PATH_ID = "bounded_structured_t6_trigger_surface_capability_adoption_path_6f9974e5"
CAPABILITY_BUILD_ID = "bounded_structured_t6_trigger_surface_capability_build_721f09dc"
PROPOSAL_ID = "capability_proposal_57dda6e9"
REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
SCHEMA_NAME = "bounded_structured_t6_trigger_surface_capability_v0"

ACCEPT_DECISION_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_receipt_5641e392.json"
MUTATION_TARGET_PREP_TARGET_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_prep_target_v0.json"
ACCEPT_DECISION_RECORD_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_human_decision_record_v0.json"
ACCEPT_DECISION_EFFECT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_effect_applied_v0.json"
ACCEPT_AUTHORITY_BOUNDARY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_authority_boundary_review_v0.json"
ACCEPT_NEGATIVE_CONTROL_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_v0/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_negative_control_v0.json"

PROMOTION_PACKET_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_receipt_9d350cee.json"
SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_adoption_human_decision_schema_promotion_path_v0_receipts/bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_receipt_4d152a3e.json"

SCHEMA_CANDIDATE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_schema_candidate_v0.json"
CAPABILITY_PROFILE_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_profile_v0.json"
EVIDENCE_SHAPE_CONTRACT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_evidence_shape_contract_v0.json"
CLASSIFIER_POLICY_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_classifier_policy_v0.json"
API_CONTRACT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_api_contract_v0.json"
TEST_EXPECTATIONS_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_test_expectations_v0.json"
CAPABILITY_NEGATIVE_CONTROL_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0/bounded_structured_t6_trigger_surface_capability_negative_control_result_v0.json"

BUILD_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_receipt_9f1f0079.json"
BUILD_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_structured_t6_trigger_surface_capability_build_review_v0_receipts/bounded_structured_t6_trigger_surface_capability_build_review_receipt_b8dba552.json"
PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"

OUT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0"
RECEIPT_DIR = ROOT / "data/bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_basis_v0.json"
SOURCE_CHAIN_BINDING_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_source_chain_binding_v0.json"
SCHEMA_CANDIDATE_SNAPSHOT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_schema_candidate_snapshot_v0.json"
ARCHIVE_ENTRY_CANDIDATE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_v0.json"
MUTATION_PLAN_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_plan_v0.json"
MUTATION_PRECONDITIONS_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_preconditions_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_authority_boundary_v0.json"
NEGATIVE_CONTROL_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_negative_control_v0.json"
REVIEW_TARGET_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_target_v0.json"
READOUT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_transition_trace.json"

FORBIDDEN_FALSE_KEYS = [
    "schema_archive_mutation_authorized",
    "schema_mutation_authorized",
    "schema_archive_write_authorized",
    "schema_archive_write_executed",
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

def compact_hash(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        ACCEPT_DECISION_RECEIPT_PATH,
        MUTATION_TARGET_PREP_TARGET_PATH,
        ACCEPT_DECISION_RECORD_PATH,
        ACCEPT_DECISION_EFFECT_PATH,
        ACCEPT_AUTHORITY_BOUNDARY_PATH,
        ACCEPT_NEGATIVE_CONTROL_PATH,
        PROMOTION_PACKET_RECEIPT_PATH,
        SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_PATH,
        SCHEMA_CANDIDATE_PATH,
        CAPABILITY_PROFILE_PATH,
        EVIDENCE_SHAPE_CONTRACT_PATH,
        CLASSIFIER_POLICY_PATH,
        API_CONTRACT_PATH,
        TEST_EXPECTATIONS_PATH,
        CAPABILITY_NEGATIVE_CONTROL_PATH,
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

    accept_receipt = read_json(ACCEPT_DECISION_RECEIPT_PATH)
    prep_target = read_json(MUTATION_TARGET_PREP_TARGET_PATH)
    accept_record = read_json(ACCEPT_DECISION_RECORD_PATH)
    accept_effect = read_json(ACCEPT_DECISION_EFFECT_PATH)
    accept_boundary = read_json(ACCEPT_AUTHORITY_BOUNDARY_PATH)
    accept_negative = read_json(ACCEPT_NEGATIVE_CONTROL_PATH)

    promotion_packet_receipt = read_json(PROMOTION_PACKET_RECEIPT_PATH)
    schema_promotion_decision_receipt = read_json(SCHEMA_PROMOTION_HUMAN_DECISION_RECEIPT_PATH)

    schema_candidate = read_json(SCHEMA_CANDIDATE_PATH)
    capability_profile = read_json(CAPABILITY_PROFILE_PATH)
    evidence_shape = read_json(EVIDENCE_SHAPE_CONTRACT_PATH)
    classifier_policy = read_json(CLASSIFIER_POLICY_PATH)
    api_contract = read_json(API_CONTRACT_PATH)
    test_expectations = read_json(TEST_EXPECTATIONS_PATH)
    capability_negative = read_json(CAPABILITY_NEGATIVE_CONTROL_PATH)

    build_receipt = read_json(BUILD_RECEIPT_PATH)
    build_review_receipt = read_json(BUILD_REVIEW_RECEIPT_PATH)
    proposal = read_json(PROPOSAL_PATH)

    accept_summary = accept_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_accept_decision_summary", {})
    promotion_packet_summary = promotion_packet_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_promotion_decision_packet_summary", {})
    schema_promotion_summary = schema_promotion_decision_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_schema_promotion_human_decision_summary", {})
    build_summary = build_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_summary", {})
    build_review_summary = build_review_receipt.get("machine_readable_bounded_structured_t6_trigger_surface_capability_build_review_summary", {})

    if accept_receipt.get("receipt_id") != ACCEPT_DECISION_RECEIPT_ID:
        failures.append(f"accept_receipt_id_wrong:{accept_receipt.get('receipt_id')}")
    if accept_receipt.get("gate") != "PASS":
        failures.append("accept_receipt_gate_not_pass")
    if accept_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"accept_terminal_next_wrong:{accept_receipt.get('terminal', {}).get('next_unit_id')}")

    for key in [
        "human_schema_promotion_decision_taken",
        "schema_archive_mutation_target_prep_authorized",
        "schema_archive_mutation_target_prep_target_ready",
    ]:
        if accept_summary.get(key) is not True:
            failures.append(f"accept_summary_{key}_not_true:{accept_summary.get(key)}")

    if accept_summary.get("selected_schema_promotion_decision") != SELECTED_SCHEMA_PROMOTION_DECISION:
        failures.append(f"selected_schema_promotion_decision_wrong:{accept_summary.get('selected_schema_promotion_decision')}")
    if accept_summary.get("schema_archive_mutation_target_prep_target_id") != MUTATION_TARGET_PREP_TARGET_ID:
        failures.append("mutation_target_prep_target_id_wrong")
    if accept_summary.get("schema_name") != SCHEMA_NAME:
        failures.append(f"accept_summary_schema_name_wrong:{accept_summary.get('schema_name')}")

    for key in [
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
        require_false(accept_summary, key, failures, "accept_summary")

    if prep_target.get("target_status") != "READY":
        failures.append(f"prep_target_status_wrong:{prep_target.get('target_status')}")
    if prep_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"prep_target_next_wrong:{prep_target.get('next_unit_id')}")
    if prep_target.get("schema_archive_mutation_target_prep_target_id") != MUTATION_TARGET_PREP_TARGET_ID:
        failures.append("prep_target_id_wrong")
    if prep_target.get("schema_archive_mutation_target_prep_authorized") is not True:
        failures.append("prep_target_mutation_target_prep_not_authorized")
    if prep_target.get("schema_archive_mutation_authorized") is not False:
        failures.append("prep_target_schema_archive_mutation_authorized_unexpected")
    if prep_target.get("schema_mutation_authorized") is not False:
        failures.append("prep_target_schema_mutation_authorized_unexpected")
    if prep_target.get("requires_later_review_before_mutation") is not True:
        failures.append("prep_target_later_review_not_required")
    if prep_target.get("requires_later_human_decision_before_schema_archive_write") is not True:
        failures.append("prep_target_later_human_decision_not_required")

    if accept_record.get("decision_record_status") != "HUMAN_SCHEMA_PROMOTION_DECISION_RECORDED":
        failures.append("accept_record_status_wrong")
    if accept_record.get("selected_schema_promotion_decision") != SELECTED_SCHEMA_PROMOTION_DECISION:
        failures.append("accept_record_selected_decision_wrong")
    if accept_effect.get("schema_archive_mutation_target_prep_authorized") is not True:
        failures.append("accept_effect_mutation_target_prep_not_authorized")
    for key in [
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
        require_false(accept_effect, key, failures, "accept_effect")

    if accept_boundary.get("review_status") != "PASS":
        failures.append("accept_boundary_not_pass")
    if accept_boundary.get("schema_archive_mutation_target_prep_authorized") is not True:
        failures.append("accept_boundary_target_prep_not_authorized")
    if accept_negative.get("negative_control_status") != "PASS":
        failures.append("accept_negative_not_pass")
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
        if accept_negative.get(counter_key) != 0:
            failures.append(f"accept_negative_counter_wrong:{counter_key}:{accept_negative.get(counter_key)}")

    if promotion_packet_summary.get("schema_archive_promotion_decision_packet_ready") is not True:
        failures.append("source_promotion_packet_not_ready")
    if schema_promotion_summary.get("schema_promotion_decision_packet_prep_authorized") is not True:
        failures.append("source_schema_promotion_packet_prep_not_authorized")

    if schema_candidate.get("schema_candidate_status") != "BUILT_CANDIDATE_ONLY_NOT_ARCHIVE_MUTATION":
        failures.append(f"schema_candidate_status_wrong:{schema_candidate.get('schema_candidate_status')}")
    if schema_candidate.get("schema_name") != SCHEMA_NAME:
        failures.append(f"schema_candidate_name_wrong:{schema_candidate.get('schema_name')}")
    if schema_candidate.get("archive_mutation_authorized") is not False:
        failures.append("schema_candidate_archive_mutation_authorized_unexpected")
    if schema_candidate.get("runtime_adoption_authorized") is not False:
        failures.append("schema_candidate_runtime_adoption_authorized_unexpected")

    if capability_profile.get("capability_name") != REQUIRED_CAPABILITY:
        failures.append(f"capability_profile_name_wrong:{capability_profile.get('capability_name')}")
    if capability_profile.get("surface_name") != SCHEMA_NAME:
        failures.append(f"capability_profile_surface_wrong:{capability_profile.get('surface_name')}")
    if api_contract.get("api_kind") != "representation_contract_only":
        failures.append(f"api_kind_wrong:{api_contract.get('api_kind')}")
    if test_expectations.get("runtime_execution_required") is not False:
        failures.append("test_expectations_runtime_required_unexpected")
    if capability_negative.get("result_status") != "PASS":
        failures.append("capability_negative_control_not_pass")
    if build_summary.get("build_executed") is not True:
        failures.append("build_not_executed")
    if build_review_summary.get("artifact_review_pass") is not True:
        failures.append("build_review_not_pass")
    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_MUTATION_TARGET_PREP_PASS_REVIEW_READY"
        if gate == "PASS"
        else "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_MUTATION_TARGET_PREP_GATE_FAIL"
    )

    schema_candidate_sha256 = file_sha256(SCHEMA_CANDIDATE_PATH)
    archive_entry_candidate_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_" + sig8({
        "schema_name": SCHEMA_NAME,
        "schema_candidate_sha256": schema_candidate_sha256,
        "accept_decision_record_id": ACCEPT_DECISION_RECORD_ID,
    })

    mutation_target_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_" + sig8({
        "archive_entry_candidate_id": archive_entry_candidate_id,
        "schema_name": SCHEMA_NAME,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "source_target_id": MUTATION_TARGET_PREP_TARGET_ID,
    })

    review_target_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_" + sig8({
        "mutation_target_id": mutation_target_id,
        "archive_entry_candidate_id": archive_entry_candidate_id,
        "source_accept_receipt_id": ACCEPT_DECISION_RECEIPT_ID,
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    archive_entry_candidate = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_entry_candidate_v0",
        "archive_entry_candidate_id": archive_entry_candidate_id,
        "entry_status": "CANDIDATE_ONLY_NOT_WRITTEN" if gate == "PASS" else "BLOCKED",
        "schema_name": SCHEMA_NAME,
        "schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "schema_candidate_sha256": schema_candidate_sha256,
        "schema_candidate_status": schema_candidate.get("schema_candidate_status"),
        "capability_name": REQUIRED_CAPABILITY,
        "capability_profile_ref": rel(CAPABILITY_PROFILE_PATH),
        "source_accept_decision_record_id": ACCEPT_DECISION_RECORD_ID,
        "source_accept_decision_receipt_id": ACCEPT_DECISION_RECEIPT_ID,
        "archive_entry_kind": "bounded_trigger_surface_schema_candidate",
        "archive_write_status": "NOT_WRITTEN",
        "schema_archive_mutation_authorized": False,
        "schema_archive_write_executed": False,
    }

    mutation_target = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_v0",
        "mutation_target_id": mutation_target_id,
        "target_status": "REVIEW_READY" if gate == "PASS" else "BLOCKED",
        "mutation_kind": "ADD_SCHEMA_ENTRY_CANDIDATE_TO_SCHEMA_ARCHIVE",
        "schema_name": SCHEMA_NAME,
        "archive_entry_candidate_id": archive_entry_candidate_id,
        "archive_entry_candidate_ref": rel(ARCHIVE_ENTRY_CANDIDATE_PATH),
        "source_schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "source_schema_candidate_sha256": schema_candidate_sha256,
        "source_accept_decision_record_id": ACCEPT_DECISION_RECORD_ID,
        "source_accept_decision_receipt_id": ACCEPT_DECISION_RECEIPT_ID,
        "claim": "This object is a proposed bounded schema archive mutation target only. It is not an archive write.",
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "schema_archive_write_authorized": False,
        "schema_archive_write_executed": False,
        "requires_review_before_write": True,
        "requires_later_human_decision_before_write": True,
    }

    basis = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_basis_v0",
        "unit_id": UNIT_ID,
        "mutation_target_id": mutation_target_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_accept_decision_receipt_id": ACCEPT_DECISION_RECEIPT_ID,
        "source_accept_decision_record_id": ACCEPT_DECISION_RECORD_ID,
        "source_mutation_target_prep_target_id": MUTATION_TARGET_PREP_TARGET_ID,
        "source_schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "prep_claim": "Prepare a schema archive mutation target for review only. Do not write to or mutate the schema archive.",
        "source_file_hashes": source_hashes,
    }

    source_chain_binding = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_source_chain_binding_v0",
        "mutation_target_id": mutation_target_id,
        "binding_status": "PASS" if gate == "PASS" else "BLOCKED",
        "proposal_id": PROPOSAL_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "promotion_decision_packet_id": PROMOTION_DECISION_PACKET_ID,
        "accept_decision_record_id": ACCEPT_DECISION_RECORD_ID,
        "accept_decision_receipt_id": ACCEPT_DECISION_RECEIPT_ID,
        "selected_schema_promotion_decision": SELECTED_SCHEMA_PROMOTION_DECISION if gate == "PASS" else None,
        "all_source_receipts_passed": True if gate == "PASS" else False,
    }

    schema_candidate_snapshot = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_schema_candidate_snapshot_v0",
        "mutation_target_id": mutation_target_id,
        "snapshot_status": "BOUND_FOR_REVIEW" if gate == "PASS" else "BLOCKED",
        "schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "schema_candidate_sha256": schema_candidate_sha256,
        "schema_candidate": schema_candidate,
        "capability_profile_ref": rel(CAPABILITY_PROFILE_PATH),
        "evidence_shape_contract_ref": rel(EVIDENCE_SHAPE_CONTRACT_PATH),
        "classifier_policy_ref": rel(CLASSIFIER_POLICY_PATH),
        "api_contract_ref": rel(API_CONTRACT_PATH),
        "test_expectations_ref": rel(TEST_EXPECTATIONS_PATH),
    }

    mutation_plan = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_plan_v0",
        "mutation_target_id": mutation_target_id,
        "plan_status": "REVIEW_READY_NOT_EXECUTED" if gate == "PASS" else "BLOCKED",
        "planned_operation": "ADD_SCHEMA_ENTRY_CANDIDATE_TO_SCHEMA_ARCHIVE",
        "planned_entry_candidate_ref": rel(ARCHIVE_ENTRY_CANDIDATE_PATH),
        "planned_write_payload_ref": rel(SCHEMA_CANDIDATE_SNAPSHOT_PATH),
        "planned_archive_key": SCHEMA_NAME,
        "planned_archive_family": "bounded_trigger_surface_capability_schema",
        "pre_write_review_required": True,
        "pre_write_human_decision_required": True,
        "write_executed_now": False,
        "schema_archive_mutation_authorized": False,
        "schema_archive_write_authorized": False,
    }

    mutation_preconditions = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_preconditions_v0",
        "mutation_target_id": mutation_target_id,
        "preconditions_status": "READY_FOR_REVIEW" if gate == "PASS" else "BLOCKED",
        "required_before_write": [
            "review mutation target",
            "verify source chain",
            "verify candidate-only archive entry",
            "verify no current archive mutation occurred",
            "record later human decision for schema archive write",
        ],
        "satisfied_in_this_unit": [
            "accept decision receipt consumed",
            "schema candidate snapshot bound",
            "archive entry candidate emitted",
            "mutation plan emitted",
            "negative control emitted",
            "review target emitted",
        ] if gate == "PASS" else [],
        "not_satisfied_in_this_unit": [
            "mutation target review",
            "schema archive write human decision",
            "schema archive mutation execution",
        ],
    }

    authority_boundary = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_authority_boundary_v0",
        "mutation_target_id": mutation_target_id,
        "boundary_status": "PASS" if gate == "PASS" else "BLOCKED",
        "schema_archive_mutation_target_prepared": True if gate == "PASS" else False,
        "schema_archive_mutation_target_review_ready": True if gate == "PASS" else False,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "schema_archive_write_authorized": False,
        "schema_archive_write_executed": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "t6_live_case_execution_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "boundary_rule": "This unit prepares a mutation target and review target only. It cannot write to the schema archive.",
    }

    negative_control = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_negative_control_v0",
        "mutation_target_id": mutation_target_id,
        "negative_control_status": "PASS" if gate == "PASS" else "BLOCKED",
        "schema_archive_mutation_target_prepared": True if gate == "PASS" else False,
        "zero_counters_for_this_unit": {
            "schema_archive_mutation_count": 0,
            "schema_mutation_count": 0,
            "schema_archive_write_count": 0,
            "runtime_adoption_count": 0,
            "runtime_patch_count": 0,
            "move_addition_count": 0,
            "fixture_expansion_count": 0,
            "t6_live_case_execution_count": 0,
            "hidden_next_command_count": 0,
            "c8_authorization_count": 0,
        },
        "negative_control_rule": "Preparing the mutation target is not schema archive mutation.",
    }

    review_target = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_review_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "schema_archive_mutation_target_review_target_id": review_target_id if gate == "PASS" else None,
        "mutation_target_id": mutation_target_id,
        "archive_entry_candidate_id": archive_entry_candidate_id,
        "source_accept_decision_record_id": ACCEPT_DECISION_RECORD_ID,
        "source_accept_decision_receipt_id": ACCEPT_DECISION_RECEIPT_ID,
        "target_scope": "Review the prepared schema archive mutation target. Do not write to schema archive in review.",
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "schema_archive_write_authorized": False,
        "schema_archive_write_executed": False,
        "requires_later_human_decision_before_schema_archive_write": True,
        "does_not_authorize_runtime_adoption": True,
        "does_not_authorize_move_addition": True,
        "does_not_authorize_fixture_expansion": True,
        "does_not_authorize_t6_live_case_execution": True,
        "does_not_authorize_c8": True,
    }

    rollup = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "mutation_target_id": mutation_target_id,
        "archive_entry_candidate_id": archive_entry_candidate_id,
        "schema_name": SCHEMA_NAME,
        "schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
        "schema_candidate_sha256": schema_candidate_sha256,
        "accept_decision_record_id": ACCEPT_DECISION_RECORD_ID,
        "schema_archive_mutation_target_prepared": True if gate == "PASS" else False,
        "schema_archive_mutation_target_review_ready": True if gate == "PASS" else False,
        "schema_archive_mutation_target_review_target_id": review_target_id if gate == "PASS" else None,
        "schema_archive_mutation_authorized": False,
        "schema_mutation_authorized": False,
        "schema_archive_write_authorized": False,
        "schema_archive_write_executed": False,
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_readout_v0",
        "status": status,
        "mutation_target_id": mutation_target_id,
        "archive_entry_candidate_id": archive_entry_candidate_id,
        "schema_name": SCHEMA_NAME,
        "interpretation": "Schema archive mutation target prepared for review. No schema archive mutation or write occurred."
        if gate == "PASS" else "Schema archive mutation target preparation failed typed gates.",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_profile_v0",
        "profile_status": status,
        "mutation_target_id": mutation_target_id,
        "core_rule": "Prepare mutation target only. Actual schema archive write remains blocked behind review and later human decision.",
        "archive_entry_candidate_ref": rel(ARCHIVE_ENTRY_CANDIDATE_PATH),
        "mutation_plan_ref": rel(MUTATION_PLAN_PATH),
        "review_target_ref": rel(REVIEW_TARGET_PATH),
        "must_not_infer": [
            "schema archive mutated",
            "schema promoted",
            "schema archive write executed",
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
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "target_result": "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_READY" if gate == "PASS" else "SCHEMA_ARCHIVE_MUTATION_TARGET_GATE_FAIL",
            "mutation_target_id": mutation_target_id,
            "archive_entry_candidate_id": archive_entry_candidate_id,
            "schema_name": SCHEMA_NAME,
            "schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
            "schema_candidate_sha256": schema_candidate_sha256,
            "schema_archive_mutation_target_prepared": True if gate == "PASS" else False,
            "schema_archive_mutation_target_review_ready": True if gate == "PASS" else False,
            "schema_archive_mutation_authorized": False,
            "schema_mutation_authorized": False,
            "schema_archive_write_authorized": False,
            "schema_archive_write_executed": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_transition_trace_v0",
        "unit_id": UNIT_ID,
        "mutation_target_id": mutation_target_id,
        "transitions": [
            {
                "from": "SCHEMA_ARCHIVE_MUTATION_TARGET_PREP_READY",
                "edge": "consume accept decision and prepare archive entry candidate plus mutation target",
                "to": "SCHEMA_ARCHIVE_MUTATION_TARGET_PREPARED" if gate == "PASS" else "SCHEMA_ARCHIVE_MUTATION_TARGET_GATE_FAIL",
            },
            {
                "from": "SCHEMA_ARCHIVE_MUTATION_TARGET_PREPARED" if gate == "PASS" else "SCHEMA_ARCHIVE_MUTATION_TARGET_GATE_FAIL",
                "edge": "emit review target without schema archive write",
                "to": "SCHEMA_ARCHIVE_MUTATION_TARGET_REVIEW_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_MUTATION_TARGET_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (SOURCE_CHAIN_BINDING_PATH, source_chain_binding),
        (SCHEMA_CANDIDATE_SNAPSHOT_PATH, schema_candidate_snapshot),
        (ARCHIVE_ENTRY_CANDIDATE_PATH, archive_entry_candidate),
        (MUTATION_PLAN_PATH, mutation_plan),
        (MUTATION_PRECONDITIONS_PATH, mutation_preconditions),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (NEGATIVE_CONTROL_PATH, negative_control),
        (REVIEW_TARGET_PATH, review_target),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "SCHEMA_ARCHIVE_PROMOTION_ACCEPT_DECISION_RECEIPT_CONSUMED",
        "MUTATION_TARGET_PREP_TARGET_CONSUMED",
        "SCHEMA_CANDIDATE_BOUND",
        "ARCHIVE_ENTRY_CANDIDATE_EMITTED",
        "MUTATION_PLAN_EMITTED",
        "MUTATION_PRECONDITIONS_EMITTED",
        "MUTATION_TARGET_REVIEW_TARGET_EMITTED",
        "NEGATIVE_CONTROL_PASS",
        "NO_SCHEMA_ARCHIVE_MUTATION",
        "NO_SCHEMA_MUTATION_EXECUTION",
        "NO_SCHEMA_ARCHIVE_WRITE",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_RUNTIME_PATCH",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION",
        "NO_T6_LIVE_CASE_EXECUTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_SCHEMA_ARCHIVE_MUTATION_TARGET_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "mutation_target_id": mutation_target_id,
        "archive_entry_candidate_id": archive_entry_candidate_id,
        "source_accept_decision_receipt_id": ACCEPT_DECISION_RECEIPT_ID,
        "source_accept_decision_receipt_ref": rel(ACCEPT_DECISION_RECEIPT_PATH),
        "source_accept_decision_record_id": ACCEPT_DECISION_RECORD_ID,
        "source_mutation_target_prep_target_id": MUTATION_TARGET_PREP_TARGET_ID,
        "adoption_path_id": ADOPTION_PATH_ID,
        "capability_build_id": CAPABILITY_BUILD_ID,
        "proposal_id": PROPOSAL_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "SCHEMA_ARCHIVE_MUTATION_TARGET_0_ACCEPT_RECEIPT_CONSUMED": gate == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_1_PREP_TARGET_CONSUMED": gate == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_2_SCHEMA_CANDIDATE_BOUND": gate == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_3_ARCHIVE_ENTRY_CANDIDATE_EMITTED": ARCHIVE_ENTRY_CANDIDATE_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_4_MUTATION_PLAN_EMITTED": MUTATION_PLAN_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_5_MUTATION_PRECONDITIONS_EMITTED": MUTATION_PRECONDITIONS_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_6_REVIEW_TARGET_EMITTED": REVIEW_TARGET_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_7_NEGATIVE_CONTROL_PASS": NEGATIVE_CONTROL_PATH.exists() and gate == "PASS",
            "SCHEMA_ARCHIVE_MUTATION_TARGET_8_NO_SCHEMA_ARCHIVE_MUTATION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_9_NO_SCHEMA_MUTATION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_10_NO_SCHEMA_ARCHIVE_WRITE": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_11_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_12_NO_RUNTIME_PATCH": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_13_NO_MOVE_ADDITION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_14_NO_FIXTURE_EXPANSION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_15_NO_T6_LIVE_CASE_EXECUTION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_16_NO_C8_AUTHORIZATION": True,
            "SCHEMA_ARCHIVE_MUTATION_TARGET_17_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_summary": {
            "status": status,
            "mutation_target_id": mutation_target_id,
            "archive_entry_candidate_id": archive_entry_candidate_id,
            "source_accept_decision_receipt_id": ACCEPT_DECISION_RECEIPT_ID,
            "source_accept_decision_record_id": ACCEPT_DECISION_RECORD_ID,
            "selected_schema_promotion_decision": SELECTED_SCHEMA_PROMOTION_DECISION if gate == "PASS" else None,
            "schema_name": SCHEMA_NAME,
            "schema_candidate_ref": rel(SCHEMA_CANDIDATE_PATH),
            "schema_candidate_sha256": schema_candidate_sha256,
            "schema_candidate_status": schema_candidate.get("schema_candidate_status"),
            "adoption_path_id": ADOPTION_PATH_ID,
            "capability_build_id": CAPABILITY_BUILD_ID,
            "proposal_id": PROPOSAL_ID,
            "schema_archive_mutation_target_prepared": True if gate == "PASS" else False,
            "schema_archive_mutation_target_review_ready": True if gate == "PASS" else False,
            "schema_archive_mutation_target_review_target_id": review_target_id if gate == "PASS" else None,
            "schema_archive_mutation_authorized": False,
            "schema_mutation_authorized": False,
            "schema_archive_write_authorized": False,
            "schema_archive_write_executed": False,
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
            "source_chain_binding": rel(SOURCE_CHAIN_BINDING_PATH),
            "schema_candidate_snapshot": rel(SCHEMA_CANDIDATE_SNAPSHOT_PATH),
            "archive_entry_candidate": rel(ARCHIVE_ENTRY_CANDIDATE_PATH),
            "mutation_plan": rel(MUTATION_PLAN_PATH),
            "mutation_preconditions": rel(MUTATION_PRECONDITIONS_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "negative_control": rel(NEGATIVE_CONTROL_PATH),
            "review_target": rel(REVIEW_TARGET_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_receipt_id={receipt_id}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_receipt_path={rel(receipt_path)}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_id={mutation_target_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_structured_t6_trigger_surface_capability_schema_archive_mutation_target_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
