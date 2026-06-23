#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_FOR_EXPECTED_LIMITS_V0"
TARGET_UNIT_ID = "candidate_missing_object_proposal_layer_for_expected_limits.v0"

SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID = "087bf971"
SOURCE_GROUP_INSPECTION_RECEIPT_ID = "342e34bd"
SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID = "4a0cfc09"
SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID = "11d585b6"
SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID = "5b841942"
SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID = "e3371951"

OUT_DIR = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0"
RECEIPT_DIR = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0_receipts"

LAYER_CONTRACT_PATH = OUT_DIR / "candidate_missing_object_proposal_layer_contract.json"
PROPOSAL_OBJECT_SCHEMA_PATH = OUT_DIR / "candidate_missing_object_proposal_object_schema.json"
TYPED_DECISION_FIELD_SCHEMA_PATH = OUT_DIR / "typed_unresolved_decision_field_schema.json"
PROPOSAL_REVIEW_DECISION_SCHEMA_PATH = OUT_DIR / "candidate_proposal_review_decision_schema.json"
PROPOSAL_REJECTION_TAXONOMY_PATH = OUT_DIR / "candidate_proposal_rejection_taxonomy.json"
EXPECTED_LIMIT_PROPOSAL_TARGET_PROFILE_PATH = OUT_DIR / "expected_limit_proposal_target_profile.json"
PROPOSAL_APPLICATION_CONTRACT_PATH = OUT_DIR / "candidate_proposal_application_contract.json"
PROPOSAL_LAYER_ACCEPTANCE_GATES_PATH = OUT_DIR / "candidate_missing_object_proposal_layer_acceptance_gates.json"
PROPOSAL_LAYER_REPORT_PATH = OUT_DIR / "candidate_missing_object_proposal_layer_report.json"

QUEUE_RECONCILIATION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
QUEUE_RECONCILIATION_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0" / "r1000_pressure_queue_reconciliation.json"
QUEUE_REMAINING_GROUPS_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0" / "r1000_remaining_pressure_groups.json"

GROUP_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_group_specific_inspection_application_v0_receipts" / f"{SOURCE_GROUP_INSPECTION_RECEIPT_ID}.json"
CLOSED_BRANCH_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_current_surface_closed_branch_exclusion_key_match_fix_v0_receipts" / f"{SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID}.json"

EXPECTED_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_RECEIPT_ID}.json"
EXPECTED_LIMIT_MARKER_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0" / "expected_source_content_limit_marker.json"
EXPECTED_LIMIT_CLOSURE_RECORD_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0" / "expected_source_content_limit_closure_record.json"

FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH = ROOT / "data/field_introduced_surface_null_evidence_limit_classification_v0_receipts/11d585b6.json"
FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH = ROOT / "data/field_introduction_proposal_typing_refinement_v0_receipts/5b841942.json"

CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID}.json"
CURRENT_SURFACE_PROTOCOL_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "current_surface_pressure_loop_protocol.json"
CAPABILITY_STOP_SCHEMA_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "capability_stop_packet_schema.json"

SOURCE_FILES = [
    QUEUE_RECONCILIATION_RECEIPT_PATH,
    QUEUE_RECONCILIATION_PATH,
    QUEUE_REMAINING_GROUPS_PATH,
    GROUP_INSPECTION_RECEIPT_PATH,
    CLOSED_BRANCH_FIX_RECEIPT_PATH,
    EXPECTED_LIMIT_RECEIPT_PATH,
    EXPECTED_LIMIT_MARKER_PATH,
    EXPECTED_LIMIT_CLOSURE_RECORD_PATH,
    FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH,
    FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH,
    CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH,
    CURRENT_SURFACE_PROTOCOL_PATH,
    CAPABILITY_STOP_SCHEMA_PATH,
]

REQUIRED_DESCRIPTOR_FIELDS = [
    "missing_label_identifier",
    "taxonomy_context_ref",
    "current_label_space_ref",
    "expected_label_space_ref",
]

HUMAN_DECISION = {
    "decision": "BUILD_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_FOR_EXPECTED_LIMITS",
    "scope": "define a non-self-applying proposal layer that converts expected-limit/capability-stop surfaces into typed candidate missing-object proposals, without filling target fields or applying proposals",
    "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
    "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
    "authorized": [
        "define candidate missing-object proposal object schema",
        "define typed unresolved decision-field schema",
        "define proposal review decision schema",
        "define proposal rejection taxonomy",
        "define expected-limit proposal target profile",
        "define proposal application contract for later accepted proposals",
        "define acceptance gates for proposal-layer application",
    ],
    "not_authorized": [
        "applying any proposal",
        "filling missing target fields",
        "inventing missing values",
        "creating labels",
        "upgrading taxonomy",
        "mutating source rows",
        "mutating existing receipts",
        "running R1000",
        "opening next pressure group",
        "claiming proposals are guaranteed correct",
        "hiding next command",
    ],
}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def tracked(path: Path) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel(path)],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def load_sources() -> Dict[str, Any]:
    return {
        "queue_reconciliation_receipt": read_json(QUEUE_RECONCILIATION_RECEIPT_PATH),
        "queue_reconciliation": read_json(QUEUE_RECONCILIATION_PATH),
        "queue_remaining_groups": read_json(QUEUE_REMAINING_GROUPS_PATH),
        "group_inspection_receipt": read_json(GROUP_INSPECTION_RECEIPT_PATH),
        "closed_branch_fix_receipt": read_json(CLOSED_BRANCH_FIX_RECEIPT_PATH),
        "expected_limit_receipt": read_json(EXPECTED_LIMIT_RECEIPT_PATH),
        "expected_limit_marker": read_json(EXPECTED_LIMIT_MARKER_PATH),
        "expected_limit_closure_record": read_json(EXPECTED_LIMIT_CLOSURE_RECORD_PATH),
        "field_introduced_null_limit_receipt": read_json(FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH),
        "field_introduction_proposal_receipt": read_json(FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH),
        "current_surface_protocol_receipt": read_json(CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH),
        "current_surface_protocol": read_json(CURRENT_SURFACE_PROTOCOL_PATH),
        "capability_stop_schema": read_json(CAPABILITY_STOP_SCHEMA_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    queue_receipt = sources["queue_reconciliation_receipt"]
    expected_limit = sources["expected_limit_receipt"]
    null_limit = sources["field_introduced_null_limit_receipt"]
    proposal_typing = sources["field_introduction_proposal_receipt"]
    protocol = sources["current_surface_protocol_receipt"]

    if queue_receipt.get("receipt_id") != SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID:
        failures.append("queue_reconciliation_receipt_id_wrong")
    if queue_receipt.get("gate") != "PASS":
        failures.append("queue_reconciliation_not_pass")
    if queue_receipt.get("aggregate_metrics", {}).get("resolved_group_count") != 2:
        failures.append("queue_reconciliation_resolved_group_count_wrong")
    if queue_receipt.get("aggregate_metrics", {}).get("remaining_open_group_count") != 3:
        failures.append("queue_reconciliation_remaining_group_count_wrong")
    if queue_receipt.get("aggregate_metrics", {}).get("proposal_layer_built_count") != 0:
        failures.append("queue_reconciliation_already_built_proposal_layer")

    if expected_limit.get("receipt_id") != SOURCE_EXPECTED_LIMIT_RECEIPT_ID:
        failures.append("expected_limit_receipt_id_wrong")
    if expected_limit.get("gate") != "PASS":
        failures.append("expected_limit_not_pass")
    if expected_limit.get("aggregate_metrics", {}).get("branch_closed") is not True:
        failures.append("expected_limit_branch_not_closed")
    if expected_limit.get("aggregate_metrics", {}).get("expected_limit_marked") is not True:
        failures.append("expected_limit_not_marked")
    if expected_limit.get("aggregate_metrics", {}).get("pressure_group_key_hash") != "38c604a1":
        failures.append("expected_limit_hash_wrong")

    if null_limit.get("receipt_id") != SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID:
        failures.append("field_introduced_null_limit_receipt_id_wrong")
    if null_limit.get("gate") != "PASS":
        failures.append("field_introduced_null_limit_not_pass")

    if proposal_typing.get("receipt_id") != SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID:
        failures.append("field_introduction_proposal_receipt_id_wrong")
    if proposal_typing.get("gate") != "PASS":
        failures.append("field_introduction_proposal_not_pass")

    if protocol.get("receipt_id") != SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID:
        failures.append("current_surface_protocol_receipt_id_wrong")
    if protocol.get("gate") != "PASS":
        failures.append("current_surface_protocol_not_pass")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_typed_decision_field_schema() -> Dict[str, Any]:
    return {
        "schema_version": "typed_unresolved_decision_field_schema_v0",
        "field_object_status": "TYPED_UNRESOLVED_DECISION_FIELD",
        "purpose": "represent unknown-but-required fields without emitting untyped nulls or fake values",
        "required_keys": [
            "field",
            "value_state",
            "missing_object_type",
            "target_field",
            "decision_owner",
            "allowed_resolution",
            "forbidden_resolution",
        ],
        "value_state_allowed": [
            "REQUIRES_SCHEMA_DECISION",
            "REQUIRES_EXISTING_SOURCE_REFERENCE",
            "REQUIRES_HUMAN_DECISION",
            "EXPECTED_UNAVAILABLE_AT_THIS_LAYER",
            "REJECTED_CANDIDATE_FIELD",
        ],
        "allowed_resolution": [
            "provide_existing_label_identifier",
            "define_new_label_identifier",
            "provide_taxonomy_context_ref",
            "provide_current_label_space_ref",
            "provide_expected_label_space_ref",
            "mark_label_identifier_not_available_at_this_layer",
            "split_pressure_group",
            "reject_candidate_object",
            "weaken_candidate_object",
            "request_more_evidence",
        ],
        "forbidden_resolution": [
            "set_null_as_value",
            "invent_value_without_source",
            "apply_candidate_without_acceptance",
            "create_taxonomy_label_without_authorization",
            "mutate_source_surface",
            "mutate_existing_receipt",
        ],
        "example": {
            "field": "missing_label_identifier",
            "value_state": "REQUIRES_SCHEMA_DECISION",
            "missing_object_type": "taxonomy_gap_label_identifier",
            "target_field": "missing_label_identifier",
            "decision_owner": "human_schema_layer",
            "allowed_resolution": [
                "provide_existing_label_identifier",
                "define_new_label_identifier",
                "mark_label_identifier_not_available_at_this_layer",
                "split_pressure_group",
                "reject_candidate_object",
            ],
            "forbidden_resolution": [
                "set_null_as_value",
                "invent_value_without_source",
            ],
        },
    }

def build_proposal_object_schema() -> Dict[str, Any]:
    return {
        "schema_version": "candidate_missing_object_proposal_object_schema_v0",
        "object_status": "CANDIDATE_MISSING_OBJECT_PROPOSAL_SCHEMA",
        "required_top_level_keys": [
            "candidate_object_id",
            "object_status",
            "missing_object_type",
            "target_field_or_surface",
            "source_pressure_group",
            "source_evidence_refs",
            "why_current_layer_stopped",
            "what_object_is_missing",
            "required_object_fields",
            "known_fields",
            "unknown_required_decision_fields",
            "proposal_basis",
            "candidate_payload",
            "application_authorized",
            "required_human_schema_decision",
            "forbidden_assumptions",
            "expected_application_effect",
            "rerun_review_rule",
        ],
        "must_not_contain": [
            "untyped_null_field_value",
            "application_authorized_true_at_proposal_time",
            "source_mutation",
            "receipt_mutation",
            "taxonomy_label_creation",
            "hidden_next_command",
        ],
        "candidate_object_id_rule": "sha8 of source expected-limit receipt, source pressure group, missing object type, target surface, and required object fields",
        "unknown_required_decision_field_rule": "each unknown field must use typed_unresolved_decision_field_schema_v0 rather than null",
        "application_rule": "proposal objects are not self-applying; accepted application must happen in a separate application unit",
        "example_candidate_object_shape": {
            "candidate_object_id": "sha8_placeholder",
            "object_status": "CANDIDATE_MISSING_OBJECT_PROPOSAL",
            "missing_object_type": "taxonomy_gap_evidence_surface_descriptor",
            "target_field_or_surface": "field_introduced_taxonomy_gap_evidence_surface",
            "source_pressure_group": {
                "parent_pressure_class": "TAXONOMY_PRESSURE",
                "pressure_subtype": "missing_label",
                "halt_reason": "STOP_TAXONOMY_GAP",
                "pressure_group_key_hash": "38c604a1",
            },
            "source_evidence_refs": [
                {
                    "receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
                    "artifact": "expected_source_content_limit_closure_record",
                    "role": "expected-limit closure source",
                },
                {
                    "receipt_id": SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID,
                    "artifact": rel(FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH),
                    "role": "field-introduced null evidence limit classifier",
                },
                {
                    "receipt_id": SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID,
                    "artifact": rel(FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH),
                    "role": "field introduction proposal typing source",
                },
            ],
            "why_current_layer_stopped": "current source surface lacks required taxonomy-gap descriptor fields and upstream explicit tracked source chain did not supply non-null values",
            "what_object_is_missing": "a typed descriptor that identifies the missing label, taxonomy context, current label space, and expected label space",
            "required_object_fields": REQUIRED_DESCRIPTOR_FIELDS,
            "known_fields": {
                "pressure_group_key_hash": "38c604a1",
                "pressure_class": "TAXONOMY_PRESSURE",
                "pressure_subtype": "missing_label",
                "halt_reason": "STOP_TAXONOMY_GAP",
            },
            "unknown_required_decision_fields": [
                {
                    "field": field,
                    "value_state": "REQUIRES_SCHEMA_DECISION",
                    "missing_object_type": "taxonomy_gap_evidence_surface_descriptor_field",
                    "target_field": field,
                    "decision_owner": "human_schema_layer",
                    "allowed_resolution": [
                        "provide_existing_source_reference",
                        "define_schema_field_source",
                        "mark_field_not_available_at_this_layer",
                        "reject_candidate_object",
                    ],
                    "forbidden_resolution": [
                        "set_null_as_value",
                        "invent_value_without_source",
                    ],
                }
                for field in REQUIRED_DESCRIPTOR_FIELDS
            ],
            "proposal_basis": "field extraction found taxonomy-gap pressure, but the current field-introduced surface lacked required taxonomy-gap descriptor values",
            "candidate_payload": {
                "proposed_object_family": "taxonomy_gap_evidence_surface_descriptor",
                "proposed_scope": "r1000_top_group_38c604a1",
                "required_human_decision": "define descriptor source, split/alter proposal, or mark expected unavailable at this layer",
            },
            "application_authorized": False,
            "required_human_schema_decision": [
                "accept_candidate_object",
                "reject_candidate_object",
                "split_candidate_object",
                "weaken_candidate_object",
                "request_more_evidence",
                "mark_expected_unavailable_at_this_layer",
            ],
            "forbidden_assumptions": [
                "do_not_fill_missing_label_identifier",
                "do_not_create_taxonomy_label",
                "do_not_claim_upstream_universal_nonexistence",
                "do_not_mutate_sources_or_receipts",
            ],
            "expected_application_effect": "if accepted later, emit a typed unresolved descriptor object while preserving target fields as unfilled decision fields",
            "rerun_review_rule": "after accepted application, rerun/review the evidence surface and classify whether the pressure became more distinguishable",
        },
    }

def build_proposal_review_decision_schema() -> Dict[str, Any]:
    return {
        "schema_version": "candidate_proposal_review_decision_schema_v0",
        "review_decision_statuses": [
            "ACCEPT_CANDIDATE_OBJECT",
            "REJECT_CANDIDATE_OBJECT",
            "SPLIT_CANDIDATE_OBJECT",
            "WEAKEN_CANDIDATE_OBJECT",
            "REQUEST_MORE_EVIDENCE",
            "MARK_EXPECTED_UNAVAILABLE_AT_THIS_LAYER",
        ],
        "required_review_keys": [
            "review_decision_id",
            "candidate_object_id",
            "decision_status",
            "decision_basis",
            "typed_rejection_codes",
            "accepted_application_scope",
            "schema_delta_if_any",
            "rerun_review_required",
        ],
        "application_authority_rule": "only ACCEPT_CANDIDATE_OBJECT may authorize a later application unit; this layer never applies the proposal itself",
        "rejection_feedback_rule": "each rejection must select at least one typed rejection code so proposal failures are refinable",
    }

def build_rejection_taxonomy() -> Dict[str, Any]:
    return {
        "schema_version": "candidate_missing_object_proposal_rejection_taxonomy_v0",
        "rejection_codes": [
            {"code": "WRONG_TARGET_FIELD", "meaning": "proposal targeted the wrong field or surface", "refinement_signal": "adjust target_field_or_surface selection rule"},
            {"code": "WRONG_MISSING_OBJECT_TYPE", "meaning": "proposal chose the wrong missing-object type", "refinement_signal": "adjust missing_object_type taxonomy mapping"},
            {"code": "WRONG_EVIDENCE_BASIS", "meaning": "proposal relied on insufficient or wrong evidence refs", "refinement_signal": "tighten required evidence_refs"},
            {"code": "WRONG_SOURCE_LAYER", "meaning": "proposal should have targeted a different source/provenance layer", "refinement_signal": "adjust source layer selection"},
            {"code": "WRONG_APPLICATION_SCOPE", "meaning": "proposal scope was too broad or too narrow", "refinement_signal": "adjust proposed_scope logic"},
            {"code": "WRONG_PROPOSED_SCHEMA_FIELD", "meaning": "one or more required fields do not belong in the proposed object", "refinement_signal": "adjust required_object_fields"},
            {"code": "WRONG_EXPECTED_LIMIT_CLASSIFICATION", "meaning": "proposal should not have been generated from this expected-limit classification", "refinement_signal": "adjust expected-limit eligibility rule"},
            {"code": "INSUFFICIENT_HUMAN_DECISION_OPTIONS", "meaning": "proposal did not expose enough review choices", "refinement_signal": "expand required_human_schema_decision"},
            {"code": "FORBIDDEN_ASSUMPTION_PRESENT", "meaning": "proposal smuggled in value invention, taxonomy creation, source mutation, or self-application", "refinement_signal": "tighten forbidden assumption guards"},
        ],
    }

def build_target_profile() -> Dict[str, Any]:
    return {
        "schema_version": "expected_limit_candidate_missing_object_proposal_target_profile_v0",
        "target_profile_id": sha8({
            "source_expected_limit": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
            "required_descriptor_fields": REQUIRED_DESCRIPTOR_FIELDS,
        }),
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_field_introduced_null_limit_receipt_id": SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID,
        "source_field_introduced_null_limit_receipt_path": rel(FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH),
        "source_field_introduction_proposal_receipt_id": SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID,
        "source_field_introduction_proposal_receipt_path": rel(FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH),
        "eligible_limit_types": [
            "CURRENT_SOURCE_CONTENT_ABSENT_UPSTREAM_EXISTENCE_UNRESOLVED",
            "EXPECTED_SOURCE_CONTENT_LIMIT_MARKED_NO_VALUE_OR_TAXONOMY_REPAIR_AUTHORIZED",
        ],
        "first_application_target": "APPLY_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_TO_R1000_TOP_GROUP_TAXONOMY_GAP_EVIDENCE_SURFACE_V0",
        "first_application_source_branch": {
            "pressure_group_key_hash": "38c604a1",
            "parent_pressure_class": "TAXONOMY_PRESSURE",
            "pressure_subtype": "missing_label",
            "halt_reason": "STOP_TAXONOMY_GAP",
        },
        "candidate_missing_object_type": "taxonomy_gap_evidence_surface_descriptor",
        "target_field_or_surface": "field_introduced_taxonomy_gap_evidence_surface",
        "required_descriptor_fields": REQUIRED_DESCRIPTOR_FIELDS,
        "decision_field_policy": "unknown required fields must be emitted as typed unresolved decision fields, not null",
        "proposal_only": True,
        "application_authorized_by_layer": False,
    }

def build_application_contract() -> Dict[str, Any]:
    return {
        "schema_version": "candidate_missing_object_proposal_application_contract_v0",
        "contract_id": sha8({
            "contract": "candidate_missing_object_proposal_application",
            "scope": "accepted_proposals_only",
        }),
        "application_unit_required": True,
        "application_unit_must_consume": [
            "candidate_missing_object_proposal",
            "human_schema_review_decision",
            "source_evidence_refs",
        ],
        "application_allowed_only_if": [
            "review_decision_status == ACCEPT_CANDIDATE_OBJECT",
            "accepted_application_scope is explicit",
            "application_authorized == true in review decision",
            "proposal forbidden assumptions are all false",
        ],
        "application_forbidden_if": [
            "proposal_status is not CANDIDATE_MISSING_OBJECT_PROPOSAL",
            "review decision missing",
            "review decision rejected/split/weakened/requested_more_evidence",
            "target fields would be filled without source",
            "taxonomy label would be created without separate authorization",
            "source or receipt mutation would occur",
        ],
        "application_effect_limit": "may materialize typed unresolved decision fields and proposal metadata; may not invent field values",
        "post_application_required": [
            "rerun/review affected evidence surface",
            "classify distinguishability change",
            "emit accepted application receipt",
        ],
    }

def build_layer_contract(proposal_schema: Dict[str, Any], decision_field_schema: Dict[str, Any], review_schema: Dict[str, Any], rejection_taxonomy: Dict[str, Any], target_profile: Dict[str, Any], application_contract: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "candidate_missing_object_proposal_layer_contract_v0",
        "layer_id": sha8({
            "layer": TARGET_UNIT_ID,
            "source_queue": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
            "source_expected_limit": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        }),
        "layer_name": "CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_FOR_EXPECTED_LIMITS",
        "purpose": "turn passive expected-limit/capability-stop surfaces into typed, reviewable, non-self-applying missing-object proposals",
        "doctrine": [
            "do_not_fill_missing_values",
            "do_not_leave_missing_objects_as_untyped_nulls",
            "emit_typed_candidate_missing_object_proposal",
            "stop_for_human_schema_decision",
            "apply_only_in_separate_accepted_application_unit",
            "use_typed_rejection_data_to_refine_proposal_schema",
        ],
        "source_receipts": {
            "queue_reconciliation": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
            "expected_limit": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
            "field_introduced_null_limit": SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID,
            "field_introduction_proposal": SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID,
            "current_surface_protocol": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        },
        "source_receipt_paths": {
            "field_introduced_null_limit": rel(FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH),
            "field_introduction_proposal": rel(FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH),
        },
        "proposal_object_schema_ref": rel(PROPOSAL_OBJECT_SCHEMA_PATH),
        "typed_decision_field_schema_ref": rel(TYPED_DECISION_FIELD_SCHEMA_PATH),
        "review_decision_schema_ref": rel(PROPOSAL_REVIEW_DECISION_SCHEMA_PATH),
        "rejection_taxonomy_ref": rel(PROPOSAL_REJECTION_TAXONOMY_PATH),
        "target_profile_ref": rel(EXPECTED_LIMIT_PROPOSAL_TARGET_PROFILE_PATH),
        "application_contract_ref": rel(PROPOSAL_APPLICATION_CONTRACT_PATH),
        "proposal_status_allowed": [
            "CANDIDATE_MISSING_OBJECT_PROPOSAL",
            "REJECTED_CANDIDATE_OBJECT",
            "ACCEPTED_CANDIDATE_OBJECT_PENDING_APPLICATION",
            "APPLIED_CANDIDATE_OBJECT",
        ],
        "minimum_valid_proposal_requirements": proposal_schema["required_top_level_keys"],
        "unknown_field_policy": decision_field_schema["purpose"],
        "review_policy": review_schema["application_authority_rule"],
        "rejection_policy": rejection_taxonomy["rejection_codes"],
        "first_application_target": target_profile["first_application_target"],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_BUILT",
            "next_command_goal": None,
        },
    }

def build_acceptance_gates() -> Dict[str, Any]:
    gates = [
        "PROPOSAL_LAYER_0_QUEUE_RECONCILIATION_CONSUMED",
        "PROPOSAL_LAYER_1_EXPECTED_LIMIT_BRANCH_CONSUMED",
        "PROPOSAL_LAYER_2_PROPOSAL_OBJECT_SCHEMA_EMITTED",
        "PROPOSAL_LAYER_3_TYPED_DECISION_FIELD_SCHEMA_EMITTED",
        "PROPOSAL_LAYER_4_REVIEW_DECISION_SCHEMA_EMITTED",
        "PROPOSAL_LAYER_5_REJECTION_TAXONOMY_EMITTED",
        "PROPOSAL_LAYER_6_TARGET_PROFILE_EMITTED",
        "PROPOSAL_LAYER_7_APPLICATION_CONTRACT_EMITTED",
        "PROPOSAL_LAYER_8_NO_PROPOSAL_APPLIED_OR_EMITTED",
        "PROPOSAL_LAYER_9_NO_NULL_VALUE_OR_VALUE_INVENTION",
        "PROPOSAL_LAYER_10_NO_TAXONOMY_ACTION",
        "PROPOSAL_LAYER_11_NO_SOURCE_OR_RECEIPT_MUTATION",
        "PROPOSAL_LAYER_12_NO_R1000_RUN_OR_GROUP_OPEN",
        "PROPOSAL_LAYER_13_NO_HIDDEN_NEXT_COMMAND",
    ]
    return {
        "schema_version": "candidate_missing_object_proposal_layer_acceptance_gates_v0",
        "gates": gates,
        "gate_requirements": {
            gate: gate.lower()
            for gate in gates
        },
    }

def build_report() -> Dict[str, Any]:
    return {
        "schema_version": "candidate_missing_object_proposal_layer_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "proposal_layer_built_count": 1,
        "proposal_object_schema_emitted_count": 1,
        "typed_decision_field_schema_emitted_count": 1,
        "review_decision_schema_emitted_count": 1,
        "rejection_taxonomy_emitted_count": 1,
        "target_profile_emitted_count": 1,
        "application_contract_emitted_count": 1,
        "candidate_proposal_instance_emitted_count": 0,
        "proposal_applied_count": 0,
        "application_authorized_count": 0,
        "null_field_value_emitted_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "r1000_run_executed_count": 0,
        "pressure_group_opened_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "first_application_target": "APPLY_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_TO_R1000_TOP_GROUP_TAXONOMY_GAP_EVIDENCE_SURFACE_V0",
        "recommended_next_handling": "APPLY_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_TO_R1000_TOP_GROUP_TAXONOMY_GAP_EVIDENCE_SURFACE_V0",
    }

def validate_layer_outputs(contract: Dict[str, Any], proposal_schema: Dict[str, Any], decision_field_schema: Dict[str, Any], review_schema: Dict[str, Any], rejection_taxonomy: Dict[str, Any], target_profile: Dict[str, Any], application_contract: Dict[str, Any], gates: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if contract["layer_name"] != "CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_FOR_EXPECTED_LIMITS":
        failures.append("layer_name_wrong")
    for doctrine in [
        "do_not_fill_missing_values",
        "do_not_leave_missing_objects_as_untyped_nulls",
        "emit_typed_candidate_missing_object_proposal",
        "stop_for_human_schema_decision",
        "apply_only_in_separate_accepted_application_unit",
    ]:
        if doctrine not in contract["doctrine"]:
            failures.append(f"doctrine_missing:{doctrine}")

    for required in [
        "candidate_object_id",
        "missing_object_type",
        "target_field_or_surface",
        "source_evidence_refs",
        "unknown_required_decision_fields",
        "application_authorized",
        "required_human_schema_decision",
        "forbidden_assumptions",
        "rerun_review_rule",
    ]:
        if required not in proposal_schema["required_top_level_keys"]:
            failures.append(f"proposal_schema_required_key_missing:{required}")

    example = proposal_schema["example_candidate_object_shape"]
    if example.get("application_authorized") is not False:
        failures.append("example_proposal_self_authorizes_application")
    if not example.get("source_evidence_refs"):
        failures.append("example_proposal_missing_evidence_refs")
    if len(example.get("unknown_required_decision_fields", [])) != len(REQUIRED_DESCRIPTOR_FIELDS):
        failures.append("example_unknown_decision_field_count_wrong")
    for field_obj in example.get("unknown_required_decision_fields", []):
        if field_obj.get("value_state") != "REQUIRES_SCHEMA_DECISION":
            failures.append("unknown_decision_field_state_wrong")
        if "set_null_as_value" not in field_obj.get("forbidden_resolution", []):
            failures.append("unknown_decision_field_does_not_forbid_null")
        if "invent_value_without_source" not in field_obj.get("forbidden_resolution", []):
            failures.append("unknown_decision_field_does_not_forbid_invention")

    if "set_null_as_value" not in decision_field_schema["forbidden_resolution"]:
        failures.append("decision_field_schema_does_not_forbid_null")
    if "invent_value_without_source" not in decision_field_schema["forbidden_resolution"]:
        failures.append("decision_field_schema_does_not_forbid_invention")
    if "REQUIRES_SCHEMA_DECISION" not in decision_field_schema["value_state_allowed"]:
        failures.append("decision_field_schema_missing_requires_schema_decision")

    if "ACCEPT_CANDIDATE_OBJECT" not in review_schema["review_decision_statuses"]:
        failures.append("review_schema_accept_missing")
    if "REJECT_CANDIDATE_OBJECT" not in review_schema["review_decision_statuses"]:
        failures.append("review_schema_reject_missing")
    if "typed rejection code" not in review_schema["rejection_feedback_rule"]:
        failures.append("review_schema_rejection_feedback_not_typed")

    rejection_codes = {entry["code"] for entry in rejection_taxonomy["rejection_codes"]}
    for code in [
        "WRONG_TARGET_FIELD",
        "WRONG_MISSING_OBJECT_TYPE",
        "WRONG_EVIDENCE_BASIS",
        "WRONG_SOURCE_LAYER",
        "WRONG_APPLICATION_SCOPE",
        "WRONG_PROPOSED_SCHEMA_FIELD",
        "WRONG_EXPECTED_LIMIT_CLASSIFICATION",
        "FORBIDDEN_ASSUMPTION_PRESENT",
    ]:
        if code not in rejection_codes:
            failures.append(f"rejection_code_missing:{code}")

    if target_profile["proposal_only"] is not True:
        failures.append("target_profile_not_proposal_only")
    if target_profile["application_authorized_by_layer"] is not False:
        failures.append("target_profile_authorizes_application")
    if target_profile["required_descriptor_fields"] != REQUIRED_DESCRIPTOR_FIELDS:
        failures.append("target_profile_required_fields_wrong")

    if application_contract["application_unit_required"] is not True:
        failures.append("application_contract_does_not_require_separate_unit")
    if "review decision missing" not in application_contract["application_forbidden_if"]:
        failures.append("application_contract_missing_review_guard")
    if "target fields would be filled without source" not in application_contract["application_forbidden_if"]:
        failures.append("application_contract_missing_value_guard")

    for gate in [
        "PROPOSAL_LAYER_8_NO_PROPOSAL_APPLIED_OR_EMITTED",
        "PROPOSAL_LAYER_9_NO_NULL_VALUE_OR_VALUE_INVENTION",
        "PROPOSAL_LAYER_10_NO_TAXONOMY_ACTION",
        "PROPOSAL_LAYER_11_NO_SOURCE_OR_RECEIPT_MUTATION",
        "PROPOSAL_LAYER_12_NO_R1000_RUN_OR_GROUP_OPEN",
        "PROPOSAL_LAYER_13_NO_HIDDEN_NEXT_COMMAND",
    ]:
        if gate not in gates["gates"]:
            failures.append(f"acceptance_gate_missing:{gate}")

    for key in [
        "candidate_proposal_instance_emitted_count",
        "proposal_applied_count",
        "application_authorized_count",
        "null_field_value_emitted_count",
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "r1000_run_executed_count",
        "pressure_group_opened_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")
    if report.get("proposal_layer_built_count") != 1:
        failures.append("proposal_layer_built_count_wrong")
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")

    for gate, ok in receipt.get("acceptance_gate_results", {}).items():
        if ok is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{ok}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("proposal_layer_built_count") != 1:
        failures.append(f"metric_proposal_layer_built_wrong:{metrics.get('proposal_layer_built_count')}")
    for key in [
        "candidate_proposal_instance_emitted_count",
        "proposal_applied_count",
        "application_authorized_count",
        "null_field_value_emitted_count",
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "r1000_run_executed_count",
        "pressure_group_opened_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_BUILT":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    source_before = snapshot_files(SOURCE_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    decision_field_schema = build_typed_decision_field_schema()
    proposal_schema = build_proposal_object_schema()
    review_schema = build_proposal_review_decision_schema()
    rejection_taxonomy = build_rejection_taxonomy()
    target_profile = build_target_profile()
    application_contract = build_application_contract()
    gates = build_acceptance_gates()
    report = build_report()
    layer_contract = build_layer_contract(
        proposal_schema,
        decision_field_schema,
        review_schema,
        rejection_taxonomy,
        target_profile,
        application_contract,
    )

    write_json(TYPED_DECISION_FIELD_SCHEMA_PATH, decision_field_schema)
    write_json(PROPOSAL_OBJECT_SCHEMA_PATH, proposal_schema)
    write_json(PROPOSAL_REVIEW_DECISION_SCHEMA_PATH, review_schema)
    write_json(PROPOSAL_REJECTION_TAXONOMY_PATH, rejection_taxonomy)
    write_json(EXPECTED_LIMIT_PROPOSAL_TARGET_PROFILE_PATH, target_profile)
    write_json(PROPOSAL_APPLICATION_CONTRACT_PATH, application_contract)
    write_json(PROPOSAL_LAYER_ACCEPTANCE_GATES_PATH, gates)
    write_json(PROPOSAL_LAYER_REPORT_PATH, report)
    write_json(LAYER_CONTRACT_PATH, layer_contract)

    failures.extend(validate_layer_outputs(
        layer_contract,
        proposal_schema,
        decision_field_schema,
        review_schema,
        rejection_taxonomy,
        target_profile,
        application_contract,
        gates,
        report,
    ))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "PROPOSAL_LAYER_0_QUEUE_RECONCILIATION_CONSUMED": sources["queue_reconciliation_receipt"]["receipt_id"] == SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID and sources["queue_reconciliation_receipt"]["gate"] == "PASS",
        "PROPOSAL_LAYER_1_EXPECTED_LIMIT_BRANCH_CONSUMED": sources["expected_limit_receipt"]["receipt_id"] == SOURCE_EXPECTED_LIMIT_RECEIPT_ID and sources["expected_limit_receipt"]["gate"] == "PASS" and sources["expected_limit_receipt"]["aggregate_metrics"]["branch_closed"] is True,
        "PROPOSAL_LAYER_2_PROPOSAL_OBJECT_SCHEMA_EMITTED": PROPOSAL_OBJECT_SCHEMA_PATH.exists(),
        "PROPOSAL_LAYER_3_TYPED_DECISION_FIELD_SCHEMA_EMITTED": TYPED_DECISION_FIELD_SCHEMA_PATH.exists(),
        "PROPOSAL_LAYER_4_REVIEW_DECISION_SCHEMA_EMITTED": PROPOSAL_REVIEW_DECISION_SCHEMA_PATH.exists(),
        "PROPOSAL_LAYER_5_REJECTION_TAXONOMY_EMITTED": PROPOSAL_REJECTION_TAXONOMY_PATH.exists(),
        "PROPOSAL_LAYER_6_TARGET_PROFILE_EMITTED": EXPECTED_LIMIT_PROPOSAL_TARGET_PROFILE_PATH.exists(),
        "PROPOSAL_LAYER_7_APPLICATION_CONTRACT_EMITTED": PROPOSAL_APPLICATION_CONTRACT_PATH.exists(),
        "PROPOSAL_LAYER_8_NO_PROPOSAL_APPLIED_OR_EMITTED": report["candidate_proposal_instance_emitted_count"] == 0 and report["proposal_applied_count"] == 0,
        "PROPOSAL_LAYER_9_NO_NULL_VALUE_OR_VALUE_INVENTION": report["null_field_value_emitted_count"] == 0 and report["field_value_invention_count"] == 0,
        "PROPOSAL_LAYER_10_NO_TAXONOMY_ACTION": report["taxonomy_label_creation_count"] == 0 and report["taxonomy_upgrade_authorized_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "PROPOSAL_LAYER_11_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "PROPOSAL_LAYER_12_NO_R1000_RUN_OR_GROUP_OPEN": report["r1000_run_executed_count"] == 0 and report["pressure_group_opened_count"] == 0 and report["next_group_auto_opened_count"] == 0,
        "PROPOSAL_LAYER_13_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_BUILT",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_field_introduced_null_limit_receipt_id": SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID,
        "source_field_introduced_null_limit_receipt_path": rel(FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH),
        "source_field_introduction_proposal_receipt_id": SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID,
        "source_field_introduction_proposal_receipt_path": rel(FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH),
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "proposal_layer_built_count": 1,
        "proposal_object_schema_emitted_count": 1,
        "typed_decision_field_schema_emitted_count": 1,
        "review_decision_schema_emitted_count": 1,
        "rejection_taxonomy_emitted_count": 1,
        "target_profile_emitted_count": 1,
        "application_contract_emitted_count": 1,
        "candidate_proposal_instance_emitted_count": 0,
        "proposal_applied_count": 0,
        "application_authorized_count": 0,
        "null_field_value_emitted_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "r1000_run_executed_count": 0,
        "pressure_group_opened_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "required_descriptor_field_count": len(REQUIRED_DESCRIPTOR_FIELDS),
        "first_application_target": report["first_application_target"],
        "recommended_next_handling": report["recommended_next_handling"],
    }

    guards = {
        "queue_reconciliation_consumed": True,
        "expected_limit_branch_consumed": True,
        "proposal_layer_built": True,
        "candidate_proposal_instance_emitted": False,
        "proposal_applied": False,
        "application_authorized": False,
        "null_field_value_emitted": False,
        "values_invented": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "r1000_run_executed": False,
        "pressure_group_opened": False,
        "next_group_auto_opened": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_queue": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_expected_limit": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "layer_id": layer_contract["layer_id"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "layer_contract": rel(LAYER_CONTRACT_PATH),
        "proposal_object_schema": rel(PROPOSAL_OBJECT_SCHEMA_PATH),
        "typed_decision_field_schema": rel(TYPED_DECISION_FIELD_SCHEMA_PATH),
        "proposal_review_decision_schema": rel(PROPOSAL_REVIEW_DECISION_SCHEMA_PATH),
        "proposal_rejection_taxonomy": rel(PROPOSAL_REJECTION_TAXONOMY_PATH),
        "expected_limit_proposal_target_profile": rel(EXPECTED_LIMIT_PROPOSAL_TARGET_PROFILE_PATH),
        "proposal_application_contract": rel(PROPOSAL_APPLICATION_CONTRACT_PATH),
        "proposal_layer_acceptance_gates": rel(PROPOSAL_LAYER_ACCEPTANCE_GATES_PATH),
        "proposal_layer_report": rel(PROPOSAL_LAYER_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "candidate_missing_object_proposal_layer_for_expected_limits_receipt_v0",
        "receipt_type": "CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_FOR_EXPECTED_LIMITS_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_field_introduced_null_limit_receipt_id": SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID,
        "source_field_introduced_null_limit_receipt_path": rel(FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH),
        "source_field_introduction_proposal_receipt_id": SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID,
        "source_field_introduction_proposal_receipt_path": rel(FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH),
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "candidate_missing_object_proposal_layer_summary": {
            "layer_id": layer_contract["layer_id"],
            "proposal_layer_built_count": 1,
            "proposal_only": True,
            "candidate_proposal_instance_emitted_count": 0,
            "proposal_applied_count": 0,
            "application_authorized_count": 0,
            "unknown_field_policy": "typed_unresolved_decision_fields_not_null",
            "required_descriptor_fields": REQUIRED_DESCRIPTOR_FIELDS,
            "first_application_target": report["first_application_target"],
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "candidate_missing_object_proposal_layer_guards": guards,
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_receipt(receipt)
    failures.extend(receipt_failures)
    receipt["failures"] = failures
    receipt["gate"] = "PASS" if not failures else "FAIL"
    if failures:
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"candidate_missing_object_proposal_layer_receipt_id={receipt_id}")
    print(f"candidate_missing_object_proposal_layer_receipt_path=data/candidate_missing_object_proposal_layer_for_expected_limits_v0_receipts/{receipt_id}.json")
    print(f"candidate_missing_object_proposal_layer_contract_path=data/candidate_missing_object_proposal_layer_for_expected_limits_v0/candidate_missing_object_proposal_layer_contract.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
