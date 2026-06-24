#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT"
MODE = "ONE_TIME_SCHEMA_OVERLAY_APPLICATION_UNIT / APPLY_AS_ACCEPTED_REFERENCE_ONLY / NO_REUSABLE_SCHEMA / NO_REBIND / NO_VALUES / NO_METADATA"
BUILD_MODE = "SCHEMA_OVERLAY_APPLICATION_UNIT_BOUNDED_REFERENCE_APPLICATION_ONLY"

SOURCE_AUTH_RECEIPT_ID = "bba7d971"
SOURCE_AUTH_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization_v0_receipts/bba7d971.json"
SOURCE_AUTH_RECORD_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization_v0/typed_machine_readable_schema_overlay_application_contract_human_authorization_record_v0.json"
SOURCE_ONE_TIME_SCOPE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization_v0/typed_machine_readable_schema_overlay_application_contract_one_time_acceptance_scope_v0.json"
SOURCE_NON_REUSE_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization_v0/typed_machine_readable_schema_overlay_application_contract_non_reuse_boundary_v0.json"
SOURCE_ACCEPTED_APP_UNIT_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization_v0/typed_machine_readable_schema_overlay_accepted_application_unit_contract_v0.json"
SOURCE_AUTH_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization_v0/typed_machine_readable_schema_overlay_application_contract_authorization_decision_table_v0.json"
SOURCE_AUTH_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization_v0/typed_machine_readable_schema_overlay_application_contract_authorization_review_packet_v0.json"
SOURCE_AUTH_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization_v0/typed_machine_readable_schema_overlay_application_contract_authorization_classification_v0.json"
SOURCE_AUTH_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization_v0/typed_machine_readable_schema_overlay_application_contract_authorization_authority_boundary_v0.json"
SOURCE_AUTH_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization_v0/typed_machine_readable_schema_overlay_application_contract_authorization_rollup_v0.json"
SOURCE_AUTH_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization_v0/typed_machine_readable_schema_overlay_application_contract_authorization_profile_v0.json"

SOURCE_SCHEMA_OVERLAY_RECEIPT_ID = "c8297ef2"
SOURCE_SCHEMA_OVERLAY_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0_receipts/c8297ef2.json"
SOURCE_SCHEMA_OVERLAY_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_surface_v0.json"
SOURCE_ROLE_SCHEMA_OVERLAY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_source_role_schema_overlay_v0.json"
SOURCE_FIELD_POLICY_SCHEMA_OVERLAY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_field_policy_enrichment_schema_overlay_v0.json"
SOURCE_CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_candidate_artifact_typing_schema_overlay_v0.json"
SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_source_lineage_requirement_schema_overlay_v0.json"
SOURCE_ROW_IDENTITY_SCHEMA_OVERLAY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_row_identity_schema_overlay_v0.json"
SOURCE_SCHEMA_OVERLAY_NONAPPLICATION_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_schema_overlay_nonapplication_contract_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0_receipts"

APPLICATION_UNIT_RECORD_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_record_v0.json"
APPLIED_REFERENCE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_applied_reference_v0.json"
APPLICATION_FRAME_BINDING_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_frame_binding_v0.json"
APPLICATION_COMPONENT_BINDING_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_component_binding_v0.json"
APPLICATION_NON_REUSE_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_non_reuse_boundary_v0.json"
APPLICATION_EFFECTS_TABLE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_effects_table_v0.json"
APPLICATION_DOWNSTREAM_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_downstream_contract_v0.json"
APPLICATION_REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_review_packet_v0.json"
APPLICATION_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_decision_table_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_AUTH_RECEIPT_PATH,
    SOURCE_AUTH_RECORD_PATH,
    SOURCE_ONE_TIME_SCOPE_PATH,
    SOURCE_NON_REUSE_BOUNDARY_PATH,
    SOURCE_ACCEPTED_APP_UNIT_CONTRACT_PATH,
    SOURCE_AUTH_DECISION_TABLE_PATH,
    SOURCE_AUTH_REVIEW_PACKET_PATH,
    SOURCE_AUTH_CLASSIFICATION_PATH,
    SOURCE_AUTH_AUTHORITY_BOUNDARY_PATH,
    SOURCE_AUTH_ROLLUP_PATH,
    SOURCE_AUTH_PROFILE_PATH,
    SOURCE_SCHEMA_OVERLAY_RECEIPT_PATH,
    SOURCE_SCHEMA_OVERLAY_SURFACE_PATH,
    SOURCE_ROLE_SCHEMA_OVERLAY_PATH,
    SOURCE_FIELD_POLICY_SCHEMA_OVERLAY_PATH,
    SOURCE_CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH,
    SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH,
    SOURCE_ROW_IDENTITY_SCHEMA_OVERLAY_PATH,
    SOURCE_SCHEMA_OVERLAY_NONAPPLICATION_CONTRACT_PATH,
]

EXPECTED_AUTH_STATUS = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_ACCEPTED_ONE_TIME_APPLICATION_UNIT_AUTHORIZED"
EXPECTED_AUTH_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_ACCEPTED_ONE_TIME_APPLICATION_UNIT_AUTHORIZED"
EXPECTED_AUTH_NEXT = "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_V0"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    auth_receipt = read_json(SOURCE_AUTH_RECEIPT_PATH)
    auth_summary = auth_receipt.get("machine_readable_schema_overlay_application_contract_authorization_summary", {})
    auth_record = read_json(SOURCE_AUTH_RECORD_PATH)
    one_time_scope = read_json(SOURCE_ONE_TIME_SCOPE_PATH)
    non_reuse = read_json(SOURCE_NON_REUSE_BOUNDARY_PATH)
    accepted_contract = read_json(SOURCE_ACCEPTED_APP_UNIT_CONTRACT_PATH)
    auth_classif = read_json(SOURCE_AUTH_CLASSIFICATION_PATH)
    auth_roll = read_json(SOURCE_AUTH_ROLLUP_PATH)
    auth_profile = read_json(SOURCE_AUTH_PROFILE_PATH)
    overlay_receipt = read_json(SOURCE_SCHEMA_OVERLAY_RECEIPT_PATH)
    overlay_summary = overlay_receipt.get("machine_readable_source_lineage_field_policy_schema_overlay_summary", {})

    if auth_receipt.get("receipt_id") != SOURCE_AUTH_RECEIPT_ID or auth_receipt.get("gate") != "PASS":
        failures.append("source_authorization_receipt_not_pass")
    if auth_summary.get("status") != EXPECTED_AUTH_STATUS:
        failures.append(f"source_authorization_status_not_expected:{auth_summary.get('status')}")
    if auth_receipt.get("terminal", {}).get("stop_code") != EXPECTED_AUTH_STOP:
        failures.append("source_authorization_terminal_not_expected")
    if auth_summary.get("recommended_next") != EXPECTED_AUTH_NEXT:
        failures.append(f"source_authorization_next_not_expected:{auth_summary.get('recommended_next')}")
    for key in [
        "application_contract_accepted",
        "accepted_for_this_application_contract",
        "one_time_acceptance",
        "application_unit_contract_authorized",
    ]:
        if auth_summary.get(key) is not True:
            failures.append(f"authorization_required_true_missing:{key}")
    for key in [
        "reusable_schema_authorized",
        "preapproved_schema_authorized",
        "validator_registry_entry_created",
        "future_automatic_use_allowed",
        "schema_overlay_applied",
        "typing_rule_applied",
        "field_policy_modified",
        "candidate_artifact_modified",
        "rebinds_applied",
        "values_authorized",
        "values_applied",
        "metadata_populated",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
    ]:
        if auth_summary.get(key) is not False:
            failures.append(f"authorization_forbidden_true:{key}")
    if auth_summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")

    if auth_record.get("authorization_status") != "ACCEPTED_ONE_TIME_FOR_THIS_APPLICATION_CONTRACT":
        failures.append("human_authorization_record_not_accepted_one_time")
    if auth_record.get("schema_overlay_applied_now") is not False:
        failures.append("human_authorization_record_claims_applied")
    if one_time_scope.get("scope_status") != "ONE_TIME_ACCEPTANCE_SCOPE_RECORDED":
        failures.append("one_time_scope_not_recorded")
    if non_reuse.get("schema_reusable") is not False:
        failures.append("non_reuse_schema_reusable_true")
    if non_reuse.get("schema_preapproved") is not False:
        failures.append("non_reuse_schema_preapproved_true")
    if non_reuse.get("schema_promoted_to_validator_registry") is not False:
        failures.append("non_reuse_registry_true")
    if non_reuse.get("future_automatic_use_allowed") is not False:
        failures.append("non_reuse_future_automatic_true")
    if accepted_contract.get("contract_status") != "APPLICATION_UNIT_CONTRACT_ACCEPTED_FOR_LATER_BOUNDED_UNIT":
        failures.append("accepted_application_unit_contract_status_wrong")
    if accepted_contract.get("schema_overlay_applied_now") is not False:
        failures.append("accepted_application_unit_contract_claims_applied_now")
    if auth_classif.get("classification_status") != EXPECTED_AUTH_STATUS:
        failures.append("auth_classification_status_wrong")
    if auth_roll.get("schema_overlay_applied_count") != 0:
        failures.append("auth_rollup_overlay_already_applied")
    if auth_profile.get("schema_overlay_applied") is not False:
        failures.append("auth_profile_overlay_already_applied")

    if overlay_receipt.get("receipt_id") != SOURCE_SCHEMA_OVERLAY_RECEIPT_ID or overlay_receipt.get("gate") != "PASS":
        failures.append("source_schema_overlay_receipt_not_pass")
    if overlay_summary.get("schema_overlay_built") is not True:
        failures.append("source_schema_overlay_not_built")
    if overlay_summary.get("schema_overlay_applied") is not False:
        failures.append("source_schema_overlay_already_applied")
    for p, expected_status in [
        (SOURCE_SCHEMA_OVERLAY_SURFACE_PATH, "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_BUILT_REVIEW_REQUIRED"),
        (SOURCE_ROLE_SCHEMA_OVERLAY_PATH, "SOURCE_ROLE_SCHEMA_OVERLAY_BUILT_NOT_APPLIED"),
        (SOURCE_FIELD_POLICY_SCHEMA_OVERLAY_PATH, "FIELD_POLICY_ENRICHMENT_SCHEMA_OVERLAY_BUILT_NOT_APPLIED"),
        (SOURCE_CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH, "CANDIDATE_ARTIFACT_TYPING_SCHEMA_OVERLAY_BUILT_NOT_APPLIED"),
        (SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH, "SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_BUILT_NOT_APPLIED"),
        (SOURCE_ROW_IDENTITY_SCHEMA_OVERLAY_PATH, "ROW_IDENTITY_SCHEMA_OVERLAY_BUILT_NOT_APPLIED"),
    ]:
        obj = read_json(p)
        observed = obj.get("surface_status") or obj.get("overlay_status")
        if observed != expected_status:
            failures.append(f"overlay_component_status_wrong:{rel(p)}:{observed}")

    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_basis()

    source_hashes = snapshot_files(REQUIRED_SOURCE_FILES)

    if failures:
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_BASIS_V0"
        applied = False
    else:
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLIED_AS_ONE_TIME_ACCEPTED_REFERENCE"
        reason_codes = [
            "SCHEMA_OVERLAY_APPLICATION_UNIT_BUILT",
            "SCHEMA_OVERLAY_APPLIED_AS_ACCEPTED_REFERENCE_FOR_THIS_APPLICATION_CONTRACT",
            "ONE_TIME_APPLICATION_FRAME_BOUND",
            "SOURCE_ROLE_SCHEMA_OVERLAY_REFERENCE_APPLIED",
            "FIELD_POLICY_SCHEMA_OVERLAY_REFERENCE_APPLIED",
            "CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_REFERENCE_APPLIED",
            "LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_REFERENCE_APPLIED",
            "ROW_IDENTITY_SCHEMA_OVERLAY_REFERENCE_APPLIED",
            "NON_REUSE_BOUNDARY_RECORDED",
            "REUSABLE_SCHEMA_NOT_AUTHORIZED",
            "PREAPPROVED_SCHEMA_NOT_AUTHORIZED",
            "VALIDATOR_REGISTRY_ENTRY_NOT_CREATED",
            "FUTURE_AUTOMATIC_USE_NOT_ALLOWED",
            "NO_TYPING_RULE_APPLIED",
            "NO_FIELD_POLICY_MODIFIED",
            "NO_CANDIDATE_ARTIFACT_MODIFIED",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_V0"
        applied = True

    components = [
        {
            "component": "source_role_schema_overlay",
            "source_path": rel(SOURCE_ROLE_SCHEMA_OVERLAY_PATH),
            "source_sha256": source_hashes.get(rel(SOURCE_ROLE_SCHEMA_OVERLAY_PATH)),
            "applied_as_reference_for_this_contract": applied,
        },
        {
            "component": "field_policy_enrichment_schema_overlay",
            "source_path": rel(SOURCE_FIELD_POLICY_SCHEMA_OVERLAY_PATH),
            "source_sha256": source_hashes.get(rel(SOURCE_FIELD_POLICY_SCHEMA_OVERLAY_PATH)),
            "applied_as_reference_for_this_contract": applied,
        },
        {
            "component": "candidate_artifact_typing_schema_overlay",
            "source_path": rel(SOURCE_CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH),
            "source_sha256": source_hashes.get(rel(SOURCE_CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH)),
            "applied_as_reference_for_this_contract": applied,
        },
        {
            "component": "source_lineage_requirement_schema_overlay",
            "source_path": rel(SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH),
            "source_sha256": source_hashes.get(rel(SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH)),
            "applied_as_reference_for_this_contract": applied,
        },
        {
            "component": "row_identity_schema_overlay",
            "source_path": rel(SOURCE_ROW_IDENTITY_SCHEMA_OVERLAY_PATH),
            "source_sha256": source_hashes.get(rel(SOURCE_ROW_IDENTITY_SCHEMA_OVERLAY_PATH)),
            "applied_as_reference_for_this_contract": applied,
        },
    ]

    application_unit_record = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_record_v0",
        "application_status": status,
        "source_authorization_receipt_id": SOURCE_AUTH_RECEIPT_ID,
        "source_schema_overlay_receipt_id": SOURCE_SCHEMA_OVERLAY_RECEIPT_ID,
        "applied_as_reference_for_this_application_contract": applied,
        "schema_overlay_applied_for_this_contract": applied,
        "schema_overlay_applied_globally": False,
        "one_time_acceptance": applied,
        "accepted_for_this_application_contract": applied,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
        "source_files_modified": False,
        "field_policy_modified": False,
        "candidate_artifact_modified": False,
        "created_at": now_iso(),
    }

    applied_reference = {
        "schema_version": "typed_machine_readable_schema_overlay_applied_reference_v0",
        "reference_status": "SCHEMA_OVERLAY_REFERENCE_APPLIED_ONE_TIME" if applied else "SCHEMA_OVERLAY_REFERENCE_NOT_APPLIED",
        "accepted_reference_id": "schema_overlay_reference_" + sha8({"auth": SOURCE_AUTH_RECEIPT_ID, "overlay": SOURCE_SCHEMA_OVERLAY_RECEIPT_ID, "components": components}),
        "application_contract_receipt_id": SOURCE_AUTH_RECEIPT_ID,
        "schema_overlay_receipt_id": SOURCE_SCHEMA_OVERLAY_RECEIPT_ID,
        "component_references": components,
        "scope": "this_application_contract_only",
        "may_be_used_by_next_units_only_for": [
            "reading source-lineage / field-policy schema requirements in this bounded branch",
            "reviewing whether source-ref rebind candidates satisfy accepted schema requirements",
            "constructing future review surfaces within this exact receipt lineage",
        ],
        "must_not_be_used_for": [
            "future automatic schema reuse",
            "preapproved schema treatment",
            "validator registry promotion",
            "source-ref rebind without separate review",
            "value extraction",
            "metadata population",
            "runtime patch",
            "C5 opening",
        ],
    }

    frame_binding = {
        "schema_version": "typed_machine_readable_schema_overlay_application_frame_binding_v0",
        "binding_status": "ONE_TIME_APPLICATION_FRAME_BOUND" if applied else "ONE_TIME_APPLICATION_FRAME_NOT_BOUND",
        "bounded_frame": {
            "authorization_receipt_id": SOURCE_AUTH_RECEIPT_ID,
            "schema_overlay_receipt_id": SOURCE_SCHEMA_OVERLAY_RECEIPT_ID,
            "application_unit": UNIT_ID,
            "target_unit_id": TARGET_UNIT_ID,
        },
        "binding_scope": "one-time / this application contract / this receipt lineage",
        "not_bound_to": [
            "global schema registry",
            "validator reusable-schema registry",
            "future branches",
            "future automatic application",
        ],
    }

    component_binding = {
        "schema_version": "typed_machine_readable_schema_overlay_application_component_binding_v0",
        "binding_status": "SCHEMA_OVERLAY_COMPONENT_REFERENCES_BOUND" if applied else "SCHEMA_OVERLAY_COMPONENT_REFERENCES_NOT_BOUND",
        "component_count": len(components),
        "components": components,
        "source_hashes_preserved": True,
        "source_components_modified": False,
    }

    non_reuse_boundary = {
        "schema_version": "typed_machine_readable_schema_overlay_application_non_reuse_boundary_v0",
        "boundary_status": "NON_REUSE_BOUNDARY_REAFFIRMED_AFTER_APPLICATION",
        "schema_overlay_applied_for_this_contract": applied,
        "schema_overlay_applied_as_reusable_schema": False,
        "schema_overlay_preapproved": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
        "reuse_requires_future_explicit_authorization": True,
        "validator_cell_promotion_requires_future_explicit_authorization": True,
    }

    effects_table = {
        "schema_version": "typed_machine_readable_schema_overlay_application_effects_table_v0",
        "effects_status": "APPLICATION_EFFECTS_RECORDED",
        "positive_effects": {
            "schema_overlay_applied_for_this_contract_count": 1 if applied else 0,
            "applied_reference_created_count": 1 if applied else 0,
            "component_reference_binding_count": len(components) if applied else 0,
        },
        "zero_effects": {
            "reusable_schema_authorized_count": 0,
            "preapproved_schema_authorized_count": 0,
            "validator_registry_entry_created_count": 0,
            "future_automatic_use_allowed_count": 0,
            "typing_rule_applied_count": 0,
            "field_policy_modified_count": 0,
            "candidate_artifact_modified_count": 0,
            "source_row_locator_applied_count": 0,
            "rebinds_applied_count": 0,
            "dominance_rule_applied_count": 0,
            "values_authorized_count": 0,
            "values_applied_count": 0,
            "metadata_populated_count": 0,
            "ready_discriminator_count": 0,
            "target_selected_for_build_count": 0,
            "runtime_patch_applied_count": 0,
            "c5_opened_count": 0,
        },
    }

    downstream_contract = {
        "schema_version": "typed_machine_readable_schema_overlay_application_downstream_contract_v0",
        "contract_status": "DOWNSTREAM_CONTRACT_EMITTED_AFTER_ONE_TIME_SCHEMA_OVERLAY_APPLICATION",
        "accepted_schema_overlay_reference_path": rel(APPLIED_REFERENCE_PATH),
        "allowed_next_uses": [
            "review accepted overlay application unit",
            "use accepted overlay reference as source-lineage / field-policy typing basis for this branch only",
            "return to source-ref rebind review using explicit accepted overlay reference",
        ],
        "next_recommended_review": next_edge,
        "still_requires_later_units_for": [
            "source-ref rebind review",
            "field-policy enrichment if ever authorized",
            "candidate-artifact typing if ever authorized",
            "value extraction if ever authorized",
            "metadata population if ever authorized",
        ],
        "not_authorized": [
            "future automatic schema reuse",
            "validator registry promotion",
            "source-ref rebind in this unit",
            "metadata population in this unit",
            "value extraction in this unit",
        ],
    }

    review_packet = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_review_packet_v0",
        "review_packet_status": "SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEW_REQUIRED",
        "question": "Review whether the one-time schema-overlay reference application was recorded correctly before using it downstream.",
        "recommended_next": next_edge,
        "summary": {
            "applied_as_reference_for_this_application_contract": applied,
            "component_reference_binding_count": len(components) if applied else 0,
            "reusable_schema_authorized": False,
            "preapproved_schema_authorized": False,
            "validator_registry_entry_created": False,
            "future_automatic_use_allowed": False,
            "schema_overlay_applied_globally": False,
        },
    }

    decision_table = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_decision_table_v0",
        "decision_status": "APPLICATION_UNIT_DECISION_EMITTED",
        "records": [
            {
                "decision": "REVIEW_APPLICATION_UNIT",
                "selected": applied,
                "next_unit": "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_V0",
                "why": "application was recorded as one-time accepted reference and must be reviewed before downstream use",
            },
            {
                "decision": "REPAIR_APPLICATION_UNIT",
                "selected": not applied,
                "next_unit": "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_V0",
                "why": "use if authorization basis or application binding fails",
            },
            {
                "decision": "PROMOTE_TO_REUSABLE_SCHEMA",
                "selected": False,
                "next_unit": None,
                "why": "explicitly not authorized in this frame",
            },
        ],
    }

    classification = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "schema_overlay_application_unit_built": True,
        "schema_overlay_applied_for_this_contract": applied,
        "applied_as_reference_for_this_application_contract": applied,
        "schema_overlay_applied_globally": False,
        "one_time_acceptance": applied,
        "accepted_for_this_application_contract": applied,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
        "typing_rule_applied": False,
        "field_policy_modified": False,
        "candidate_artifact_modified": False,
        "source_row_locator_applied": False,
        "rebinds_applied": False,
        "dominance_rule_applied": False,
        "values_authorized": False,
        "values_applied": False,
        "null_reasons_accepted": False,
        "source_packet_materialized_for_review": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "real_tie_proven": False,
        "rule_refined": False,
        "tie_broken": False,
        "candidate_values_filled": False,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "acceptance_boundary": "human_one_time_acceptance_for_this_application_contract",
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_authority_boundary_v0",
        "status": status,
        "may_record_one_time_schema_overlay_reference_application": True,
        "may_use_reference_in_this_branch_after_review": applied,
        "may_treat_schema_as_reusable": False,
        "may_treat_schema_as_preapproved": False,
        "may_create_validator_registry_entry": False,
        "may_allow_future_automatic_use": False,
        "may_apply_typing_rule": False,
        "may_modify_field_policy": False,
        "may_modify_candidate_artifacts": False,
        "may_apply_source_row_locator": False,
        "may_apply_rebinds": False,
        "may_apply_dominance_rule": False,
        "may_authorize_values": False,
        "may_apply_values": False,
        "may_populate_metadata": False,
        "may_evaluate_discriminators": False,
        "may_select_target_for_build": False,
        "may_apply_runtime_patch": False,
        "may_open_c5": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "acceptance_boundary": "human_one_time_acceptance_for_this_application_contract",
    }

    rollup = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "schema_overlay_application_unit_built_count": 1,
        "schema_overlay_applied_for_this_contract_count": 1 if applied else 0,
        "schema_overlay_applied_as_reference_count": 1 if applied else 0,
        "schema_overlay_applied_globally_count": 0,
        "component_reference_binding_count": len(components) if applied else 0,
        "one_time_acceptance_count": 1 if applied else 0,
        "accepted_for_this_application_contract_count": 1 if applied else 0,
        "reusable_schema_authorized_count": 0,
        "preapproved_schema_authorized_count": 0,
        "validator_registry_entry_created_count": 0,
        "future_automatic_use_allowed_count": 0,
        "typing_rule_applied_count": 0,
        "field_policy_modified_count": 0,
        "candidate_artifact_modified_count": 0,
        "source_row_locator_applied_count": 0,
        "rebinds_applied_count": 0,
        "dominance_rule_applied_count": 0,
        "refinements_applied_count": 0,
        "values_authorized_count": 0,
        "values_applied_count": 0,
        "null_reason_accepted_count": 0,
        "source_packet_materialized_for_review_count": 0,
        "metadata_populated_count": 0,
        "ready_discriminator_count": 0,
        "rule_refined_count": 0,
        "tie_broken_count": 0,
        "candidate_values_filled_count": 0,
        "target_candidate_declared_for_review_count": 0,
        "target_selected_for_build_count": 0,
        "accepted_for_build_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "unbounded_payload_inspection_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": next_edge,
    }

    zero_keys = [
        "reusable_schema_authorized_count",
        "preapproved_schema_authorized_count",
        "validator_registry_entry_created_count",
        "future_automatic_use_allowed_count",
        "schema_overlay_applied_globally_count",
        "typing_rule_applied_count",
        "field_policy_modified_count",
        "candidate_artifact_modified_count",
        "source_row_locator_applied_count",
        "rebinds_applied_count",
        "values_authorized_count",
        "values_applied_count",
        "metadata_populated_count",
        "ready_discriminator_count",
        "target_selected_for_build_count",
        "runtime_patch_applied_count",
        "c5_opened_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_profile_v0",
        "profile_id": "schema_overlay_application_unit_profile_" + sha8(rollup),
        "status": status,
        "schema_overlay_application_unit_built": True,
        "schema_overlay_applied_for_this_contract": applied,
        "applied_as_reference_for_this_application_contract": applied,
        "schema_overlay_applied_globally": False,
        "one_time_acceptance": applied,
        "accepted_for_this_application_contract": applied,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
        "typing_rule_applied": False,
        "field_policy_modified": False,
        "candidate_artifact_modified": False,
        "rebinds_applied": False,
        "values_authorized": False,
        "values_applied": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    report = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The schema overlay was applied only as a one-time accepted reference for this application contract. No reusable schema authority, preapproval, validator registry entry, future automatic use, rebind, value extraction, or metadata population was created.",
        "schema_overlay_applied_for_this_contract_count": rollup["schema_overlay_applied_for_this_contract_count"],
        "schema_overlay_applied_as_reference_count": rollup["schema_overlay_applied_as_reference_count"],
        "component_reference_binding_count": rollup["component_reference_binding_count"],
        "reusable_schema_authorized_count": 0,
        "preapproved_schema_authorized_count": 0,
        "validator_registry_entry_created_count": 0,
        "future_automatic_use_allowed_count": 0,
        "rebinds_applied_count": 0,
        "metadata_populated_count": 0,
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_one_time_acceptance_for_this_application_contract",
    }

    trace = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_transition_trace_v0",
        "trace": [
            {
                "step": "consume_one_time_authorization",
                "question": "is a bounded application unit authorized",
                "answer": "yes, for this application contract only",
                "taken": "bind application frame",
            },
            {
                "step": "apply_reference",
                "question": "what does application mean in this unit",
                "answer": "record accepted overlay reference for this contract only",
                "taken": "emit applied reference and component bindings",
            },
            {
                "step": "reaffirm_non_reuse",
                "question": "does this create reusable schema authority",
                "answer": "no",
                "taken": "emit non-reuse boundary",
            },
            {
                "step": "classify_application_unit",
                "question": "what is next lawful object",
                "answer": status,
                "taken": next_edge,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(APPLICATION_UNIT_RECORD_PATH, application_unit_record)
    write_json(APPLIED_REFERENCE_PATH, applied_reference)
    write_json(APPLICATION_FRAME_BINDING_PATH, frame_binding)
    write_json(APPLICATION_COMPONENT_BINDING_PATH, component_binding)
    write_json(APPLICATION_NON_REUSE_BOUNDARY_PATH, non_reuse_boundary)
    write_json(APPLICATION_EFFECTS_TABLE_PATH, effects_table)
    write_json(APPLICATION_DOWNSTREAM_CONTRACT_PATH, downstream_contract)
    write_json(APPLICATION_REVIEW_PACKET_PATH, review_packet)
    write_json(APPLICATION_DECISION_TABLE_PATH, decision_table)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_BOUNDARY_PATH, authority_boundary)
    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRANSITION_TRACE_PATH, trace)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        rollup["source_mutation_count"] = 1
        report["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup)
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "APPLICATION_UNIT_0_AUTHORIZATION_RECEIPT_CONSUMED": SOURCE_AUTH_RECEIPT_PATH.exists(),
        "APPLICATION_UNIT_1_ONE_TIME_ACCEPTANCE_PRESENT": applied,
        "APPLICATION_UNIT_2_APPLICATION_UNIT_RECORD_EMITTED": APPLICATION_UNIT_RECORD_PATH.exists(),
        "APPLICATION_UNIT_3_APPLIED_REFERENCE_EMITTED": APPLIED_REFERENCE_PATH.exists(),
        "APPLICATION_UNIT_4_FRAME_BINDING_EMITTED": APPLICATION_FRAME_BINDING_PATH.exists(),
        "APPLICATION_UNIT_5_COMPONENT_BINDING_EMITTED": APPLICATION_COMPONENT_BINDING_PATH.exists(),
        "APPLICATION_UNIT_6_NON_REUSE_BOUNDARY_EMITTED": APPLICATION_NON_REUSE_BOUNDARY_PATH.exists(),
        "APPLICATION_UNIT_7_EFFECTS_TABLE_EMITTED": APPLICATION_EFFECTS_TABLE_PATH.exists(),
        "APPLICATION_UNIT_8_DOWNSTREAM_CONTRACT_EMITTED": APPLICATION_DOWNSTREAM_CONTRACT_PATH.exists(),
        "APPLICATION_UNIT_9_SCHEMA_OVERLAY_APPLIED_FOR_THIS_CONTRACT": rollup["schema_overlay_applied_for_this_contract_count"] == 1,
        "APPLICATION_UNIT_10_APPLIED_AS_REFERENCE": rollup["schema_overlay_applied_as_reference_count"] == 1,
        "APPLICATION_UNIT_11_NO_GLOBAL_SCHEMA_APPLICATION": rollup["schema_overlay_applied_globally_count"] == 0,
        "APPLICATION_UNIT_12_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "APPLICATION_UNIT_13_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "APPLICATION_UNIT_14_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "APPLICATION_UNIT_15_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "APPLICATION_UNIT_16_NO_TYPING_RULE_APPLIED": rollup["typing_rule_applied_count"] == 0,
        "APPLICATION_UNIT_17_NO_FIELD_POLICY_MODIFIED": rollup["field_policy_modified_count"] == 0,
        "APPLICATION_UNIT_18_NO_CANDIDATE_ARTIFACT_MODIFIED": rollup["candidate_artifact_modified_count"] == 0,
        "APPLICATION_UNIT_19_NO_ROW_LOCATOR_APPLIED": rollup["source_row_locator_applied_count"] == 0,
        "APPLICATION_UNIT_20_NO_REBINDS_APPLIED": rollup["rebinds_applied_count"] == 0,
        "APPLICATION_UNIT_21_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "APPLICATION_UNIT_22_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "APPLICATION_UNIT_23_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "APPLICATION_UNIT_24_NO_DISCRIMINATOR_READY": rollup["ready_discriminator_count"] == 0,
        "APPLICATION_UNIT_25_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "APPLICATION_UNIT_26_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "APPLICATION_UNIT_27_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "APPLICATION_UNIT_28_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "APPLICATION_UNIT_29_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "APPLICATION_UNIT_30_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "APPLICATION_UNIT_31_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_one_time_acceptance_for_this_application_contract",
        "APPLICATION_UNIT_32_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SCHEMA_OVERLAY_APPLICATION_UNIT_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "applied_reference": applied,
        "component_count": len(components),
        "reusable": 0,
        "global": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SCHEMA_OVERLAY_APPLICATION_UNIT_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_authorization_receipt_id": SOURCE_AUTH_RECEIPT_ID,
        "source_schema_overlay_receipt_id": SOURCE_SCHEMA_OVERLAY_RECEIPT_ID,
        "machine_readable_schema_overlay_application_unit_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "schema_overlay_application_unit_built": True,
            "schema_overlay_applied_for_this_contract": applied,
            "applied_as_reference_for_this_application_contract": applied,
            "schema_overlay_applied_globally": False,
            "component_reference_binding_count": len(components) if applied else 0,
            "one_time_acceptance": applied,
            "accepted_for_this_application_contract": applied,
            "reusable_schema_authorized": False,
            "preapproved_schema_authorized": False,
            "validator_registry_entry_created": False,
            "future_automatic_use_allowed": False,
            "typing_rule_applied": False,
            "field_policy_modified": False,
            "candidate_artifact_modified": False,
            "source_row_locator_applied": False,
            "rebinds_applied": False,
            "dominance_rule_applied": False,
            "values_authorized": False,
            "values_applied": False,
            "null_reasons_accepted": False,
            "source_packet_materialized_for_review": False,
            "metadata_populated": False,
            "ready_discriminator_count": 0,
            "target_selected_for_build": False,
            "runtime_patch_applied": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "acceptance_boundary": "human_one_time_acceptance_for_this_application_contract",
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": next_edge,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "application_unit_record": rel(APPLICATION_UNIT_RECORD_PATH),
            "applied_reference": rel(APPLIED_REFERENCE_PATH),
            "application_frame_binding": rel(APPLICATION_FRAME_BINDING_PATH),
            "application_component_binding": rel(APPLICATION_COMPONENT_BINDING_PATH),
            "application_non_reuse_boundary": rel(APPLICATION_NON_REUSE_BOUNDARY_PATH),
            "application_effects_table": rel(APPLICATION_EFFECTS_TABLE_PATH),
            "application_downstream_contract": rel(APPLICATION_DOWNSTREAM_CONTRACT_PATH),
            "application_review_packet": rel(APPLICATION_REVIEW_PACKET_PATH),
            "application_decision_table": rel(APPLICATION_DECISION_TABLE_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"schema_overlay_application_unit_receipt_id={receipt_id}")
    print(f"schema_overlay_application_unit_receipt_path={rel(receipt_path)}")
    print(f"schema_overlay_application_unit_record_path={rel(APPLICATION_UNIT_RECORD_PATH)}")
    print(f"schema_overlay_applied_reference_path={rel(APPLIED_REFERENCE_PATH)}")
    print(f"schema_overlay_application_frame_binding_path={rel(APPLICATION_FRAME_BINDING_PATH)}")
    print(f"schema_overlay_application_component_binding_path={rel(APPLICATION_COMPONENT_BINDING_PATH)}")
    print(f"schema_overlay_application_non_reuse_boundary_path={rel(APPLICATION_NON_REUSE_BOUNDARY_PATH)}")
    print(f"schema_overlay_application_unit_rollup_path={rel(ROLLUP_PATH)}")
    print(f"schema_overlay_application_unit_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
