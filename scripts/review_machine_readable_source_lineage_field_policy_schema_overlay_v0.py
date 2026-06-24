#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_REVIEW"
MODE = "SCHEMA_OVERLAY_REVIEW / NO_SCHEMA_OVERLAY_APPLICATION / NO_TYPING_RULE_APPLICATION / NO_POLICY_MODIFICATION / NO_CANDIDATE_MODIFICATION / NO_REBIND / NO_METADATA_FILL"
BUILD_MODE = "SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_REVIEW_ONLY"

SOURCE_SCHEMA_OVERLAY_RECEIPT_ID = "c8297ef2"
SOURCE_SCHEMA_OVERLAY_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0_receipts/c8297ef2.json"
SOURCE_SCHEMA_OVERLAY_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_surface_v0.json"
SOURCE_ROLE_SCHEMA_OVERLAY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_source_role_schema_overlay_v0.json"
SOURCE_FIELD_POLICY_SCHEMA_OVERLAY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_field_policy_enrichment_schema_overlay_v0.json"
SOURCE_CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_candidate_artifact_typing_schema_overlay_v0.json"
SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_source_lineage_requirement_schema_overlay_v0.json"
SOURCE_ROW_IDENTITY_SCHEMA_OVERLAY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_row_identity_schema_overlay_v0.json"
SOURCE_OVERLAY_VALIDATION_MATRIX_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_schema_overlay_validation_matrix_v0.json"
SOURCE_OVERLAY_NONAPPLICATION_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_schema_overlay_nonapplication_contract_v0.json"
SOURCE_OVERLAY_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_review_packet_v0.json"
SOURCE_OVERLAY_DECISION_OPTIONS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_decision_options_v0.json"
SOURCE_OVERLAY_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_classification_v0.json"
SOURCE_OVERLAY_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_authority_boundary_v0.json"
SOURCE_OVERLAY_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_rollup_v0.json"
SOURCE_OVERLAY_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_assessment_v0.json"
OVERLAY_COMPLETENESS_REVIEW_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_completeness_review_v0.json"
OVERLAY_CONSISTENCY_REVIEW_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_consistency_review_v0.json"
OVERLAY_BOUNDARY_REVIEW_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_nonapplication_boundary_review_v0.json"
OVERLAY_COMPONENT_REVIEW_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_component_review_v0.json"
APPLICATION_PRECONDITION_TABLE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_precondition_table_v0.json"
APPLICATION_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_v0.json"
APPLICATION_REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_review_packet_v0.json"
REVIEW_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_review_decision_table_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_SCHEMA_OVERLAY_RECEIPT_PATH,
    SOURCE_SCHEMA_OVERLAY_SURFACE_PATH,
    SOURCE_ROLE_SCHEMA_OVERLAY_PATH,
    SOURCE_FIELD_POLICY_SCHEMA_OVERLAY_PATH,
    SOURCE_CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH,
    SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH,
    SOURCE_ROW_IDENTITY_SCHEMA_OVERLAY_PATH,
    SOURCE_OVERLAY_VALIDATION_MATRIX_PATH,
    SOURCE_OVERLAY_NONAPPLICATION_CONTRACT_PATH,
    SOURCE_OVERLAY_REVIEW_PACKET_PATH,
    SOURCE_OVERLAY_DECISION_OPTIONS_PATH,
    SOURCE_OVERLAY_CLASSIFICATION_PATH,
    SOURCE_OVERLAY_AUTHORITY_BOUNDARY_PATH,
    SOURCE_OVERLAY_ROLLUP_PATH,
    SOURCE_OVERLAY_PROFILE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_BUILT_REVIEW_REQUIRED"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_BUILT_REVIEW_REQUIRED"
EXPECTED_NEXT = "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0"

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

def records(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    for key in ["records", "slots", "field_policies", "policies", "checks"]:
        val = obj.get(key)
        if isinstance(val, list):
            return [x for x in val if isinstance(x, dict)]
    return []

def validate_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    receipt = read_json(SOURCE_SCHEMA_OVERLAY_RECEIPT_PATH)
    summary = receipt.get("machine_readable_source_lineage_field_policy_schema_overlay_summary", {})
    surface = read_json(SOURCE_SCHEMA_OVERLAY_SURFACE_PATH)
    source_role = read_json(SOURCE_ROLE_SCHEMA_OVERLAY_PATH)
    field_policy = read_json(SOURCE_FIELD_POLICY_SCHEMA_OVERLAY_PATH)
    candidate = read_json(SOURCE_CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH)
    lineage = read_json(SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH)
    row_identity = read_json(SOURCE_ROW_IDENTITY_SCHEMA_OVERLAY_PATH)
    validation_matrix = read_json(SOURCE_OVERLAY_VALIDATION_MATRIX_PATH)
    nonapp = read_json(SOURCE_OVERLAY_NONAPPLICATION_CONTRACT_PATH)
    classif = read_json(SOURCE_OVERLAY_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_OVERLAY_ROLLUP_PATH)
    profile = read_json(SOURCE_OVERLAY_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_SCHEMA_OVERLAY_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_schema_overlay_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_schema_overlay_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_schema_overlay_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"source_schema_overlay_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("schema_overlay_built") is not True:
        failures.append("source_schema_overlay_not_built")
    if summary.get("schema_overlay_applied") is not False:
        failures.append("source_schema_overlay_applied")
    if summary.get("source_role_schema_overlay_count") != 1:
        failures.append("source_role_overlay_count_not_1")
    if summary.get("field_policy_schema_overlay_count") != 1:
        failures.append("field_policy_overlay_count_not_1")
    if summary.get("candidate_artifact_schema_overlay_count") != 1:
        failures.append("candidate_artifact_overlay_count_not_1")
    if summary.get("lineage_requirement_schema_overlay_count") != 1:
        failures.append("lineage_requirement_overlay_count_not_1")
    if summary.get("row_identity_schema_overlay_count") != 1:
        failures.append("row_identity_overlay_count_not_1")
    if summary.get("field_policy_gap_review_count") != 7:
        failures.append("field_policy_gap_review_count_not_7")
    if summary.get("lineage_requirement_review_count") != 105:
        failures.append("lineage_requirement_review_count_not_105")
    if summary.get("candidate_overlay_review_count") != 168:
        failures.append("candidate_overlay_review_count_not_168")
    for key in [
        "typing_rule_applied",
        "field_policy_modified",
        "candidate_artifact_modified",
        "source_row_locator_applied",
        "rebinds_applied",
        "dominance_rule_applied",
        "values_authorized",
        "values_applied",
        "metadata_populated",
        "rule_refined",
        "tie_broken",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
    ]:
        if summary.get(key) is not False:
            failures.append(f"source_summary_forbidden_true:{key}")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")

    if surface.get("surface_status") != EXPECTED_SOURCE_STATUS:
        failures.append("schema_overlay_surface_status_wrong")
    if source_role.get("overlay_status") != "SOURCE_ROLE_SCHEMA_OVERLAY_BUILT_NOT_APPLIED":
        failures.append("source_role_overlay_status_wrong")
    if field_policy.get("overlay_status") != "FIELD_POLICY_ENRICHMENT_SCHEMA_OVERLAY_BUILT_NOT_APPLIED":
        failures.append("field_policy_overlay_status_wrong")
    if candidate.get("overlay_status") != "CANDIDATE_ARTIFACT_TYPING_SCHEMA_OVERLAY_BUILT_NOT_APPLIED":
        failures.append("candidate_overlay_status_wrong")
    if lineage.get("overlay_status") != "SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_BUILT_NOT_APPLIED":
        failures.append("lineage_overlay_status_wrong")
    if row_identity.get("overlay_status") != "ROW_IDENTITY_SCHEMA_OVERLAY_BUILT_NOT_APPLIED":
        failures.append("row_identity_overlay_status_wrong")
    if validation_matrix.get("matrix_status") != "SCHEMA_OVERLAY_VALIDATION_MATRIX_EMITTED":
        failures.append("validation_matrix_status_wrong")
    if nonapp.get("contract_status") != "SCHEMA_OVERLAY_BUILT_NOT_APPLIED":
        failures.append("nonapplication_contract_status_wrong")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("source_classification_status_wrong")
    if roll.get("schema_overlay_applied_count") != 0:
        failures.append("source_rollup_overlay_applied_nonzero")
    if profile.get("schema_overlay_applied") is not False:
        failures.append("source_profile_overlay_applied_true")

    return failures

def review_completeness() -> Tuple[Dict[str, Any], List[str]]:
    source_role = read_json(SOURCE_ROLE_SCHEMA_OVERLAY_PATH)
    field_policy = read_json(SOURCE_FIELD_POLICY_SCHEMA_OVERLAY_PATH)
    candidate = read_json(SOURCE_CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH)
    lineage = read_json(SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH)
    row_identity = read_json(SOURCE_ROW_IDENTITY_SCHEMA_OVERLAY_PATH)

    checks = {
        "source_role_required_fields_present": len(source_role.get("required_candidate_artifact_fields", [])) >= 7,
        "source_role_allowed_roles_present": len(source_role.get("allowed_source_roles", [])) >= 7,
        "field_policy_required_fields_present": len(field_policy.get("required_field_policy_fields", [])) >= 7,
        "field_policy_gap_scope_present": field_policy.get("field_policy_gap_review_count") == 7,
        "candidate_overlay_scope_present": candidate.get("candidate_overlay_review_count") == 168,
        "candidate_required_typing_fields_present": len(candidate.get("required_candidate_typing_fields", [])) >= 6,
        "lineage_requirement_scope_present": lineage.get("lineage_requirement_review_count") == 105,
        "lineage_evidence_classes_present": set(lineage.get("lineage_evidence_class_counts", {}).keys()) >= {
            "ARTIFACT_PRODUCER_UNIT",
            "EXPLICIT_SOURCE_ROLE",
            "FIELD_POLICY_SOURCE_OBJECT_MATCH",
            "ROW_IDENTITY_SCHEMA",
            "SOURCE_PACKET_LINEAGE",
        },
        "row_identity_requirement_present": row_identity.get("row_identity_requirement_count") == 21,
        "row_identity_keys_present": set(row_identity.get("required_row_identity_keys", [])) >= {"slot_id", "row_uid", "field"},
    }
    failures = [k for k, v in checks.items() if not v]
    return {
        "schema_version": "typed_machine_readable_schema_overlay_completeness_review_v0",
        "review_status": "SCHEMA_OVERLAY_COMPLETENESS_PASS" if not failures else "SCHEMA_OVERLAY_COMPLETENESS_FAIL",
        "checks": checks,
        "failures": failures,
        "component_count": 5,
    }, failures

def review_consistency() -> Tuple[Dict[str, Any], List[str]]:
    source_role = read_json(SOURCE_ROLE_SCHEMA_OVERLAY_PATH)
    field_policy = read_json(SOURCE_FIELD_POLICY_SCHEMA_OVERLAY_PATH)
    candidate = read_json(SOURCE_CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH)
    lineage = read_json(SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH)
    row_identity = read_json(SOURCE_ROW_IDENTITY_SCHEMA_OVERLAY_PATH)

    candidate_fields = set(candidate.get("required_candidate_typing_fields", []))
    source_role_fields = set(source_role.get("required_candidate_artifact_fields", []))
    lineage_classes = set(lineage.get("lineage_evidence_class_counts", {}).keys())

    checks = {
        "source_role_declares_source_role": "source_role" in source_role_fields,
        "source_role_declares_lineage_ref": "lineage_ref" in source_role_fields,
        "source_role_declares_source_packet_ref": "source_packet_ref" in source_role_fields,
        "candidate_overlay_declares_candidate_lineage_ref": "candidate_lineage_ref" in candidate_fields,
        "candidate_overlay_declares_candidate_source_role": "candidate_source_role" in candidate_fields,
        "candidate_overlay_declares_candidate_row_identity_schema": "candidate_row_identity_schema" in candidate_fields,
        "field_policy_declares_required_source_object": "required_source_object" in set(field_policy.get("required_field_policy_fields", [])),
        "field_policy_declares_row_identity_keys": "row_identity_keys" in set(field_policy.get("required_field_policy_fields", [])),
        "lineage_has_source_packet_lineage": "SOURCE_PACKET_LINEAGE" in lineage_classes,
        "lineage_has_row_identity_schema": "ROW_IDENTITY_SCHEMA" in lineage_classes,
        "row_identity_keys_are_minimal": row_identity.get("required_row_identity_keys") == ["slot_id", "row_uid", "field"],
    }
    failures = [k for k, v in checks.items() if not v]
    return {
        "schema_version": "typed_machine_readable_schema_overlay_consistency_review_v0",
        "review_status": "SCHEMA_OVERLAY_CONSISTENCY_PASS" if not failures else "SCHEMA_OVERLAY_CONSISTENCY_FAIL",
        "checks": checks,
        "failures": failures,
        "consistency_claim": "overlay components agree on source role, lineage, row identity, and field-policy source-object requirements",
    }, failures

def review_boundary() -> Tuple[Dict[str, Any], List[str]]:
    nonapp = read_json(SOURCE_OVERLAY_NONAPPLICATION_CONTRACT_PATH)
    validation = read_json(SOURCE_OVERLAY_VALIDATION_MATRIX_PATH)
    checks_obj = validation.get("checks", {})
    checks = {
        "nonapplication_contract_present": nonapp.get("contract_status") == "SCHEMA_OVERLAY_BUILT_NOT_APPLIED",
        "schema_overlay_review_allowed": nonapp.get("schema_overlay_may_be_reviewed") is True,
        "schema_overlay_application_forbidden": nonapp.get("schema_overlay_may_be_applied") is False,
        "validation_matrix_forbids_overlay_application": checks_obj.get("schema_overlay_application_authorized") is False,
        "validation_matrix_forbids_typing_rule": checks_obj.get("typing_rule_application_authorized") is False,
        "validation_matrix_forbids_field_policy_modification": checks_obj.get("field_policy_modification_authorized") is False,
        "validation_matrix_forbids_candidate_modification": checks_obj.get("candidate_artifact_modification_authorized") is False,
        "validation_matrix_forbids_source_ref_rebind": checks_obj.get("source_ref_rebind_authorized") is False,
        "validation_matrix_forbids_value_extraction": checks_obj.get("value_extraction_authorized") is False,
        "validation_matrix_forbids_metadata_population": checks_obj.get("metadata_population_authorized") is False,
    }
    failures = [k for k, v in checks.items() if not v]
    return {
        "schema_version": "typed_machine_readable_schema_overlay_nonapplication_boundary_review_v0",
        "review_status": "SCHEMA_OVERLAY_NONAPPLICATION_BOUNDARY_PASS" if not failures else "SCHEMA_OVERLAY_NONAPPLICATION_BOUNDARY_FAIL",
        "checks": checks,
        "failures": failures,
        "boundary_claim": "overlay is reviewable but not applied; application requires a separate explicit application unit",
    }, failures

def component_review() -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_schema_overlay_component_review_v0",
        "review_status": "SCHEMA_OVERLAY_COMPONENTS_REVIEWED",
        "components": [
            {
                "component": "source_role_schema_overlay",
                "path": rel(SOURCE_ROLE_SCHEMA_OVERLAY_PATH),
                "review_status": "COMPONENT_PRESENT_NOT_APPLIED",
            },
            {
                "component": "field_policy_enrichment_schema_overlay",
                "path": rel(SOURCE_FIELD_POLICY_SCHEMA_OVERLAY_PATH),
                "review_status": "COMPONENT_PRESENT_NOT_APPLIED",
            },
            {
                "component": "candidate_artifact_typing_schema_overlay",
                "path": rel(SOURCE_CANDIDATE_ARTIFACT_SCHEMA_OVERLAY_PATH),
                "review_status": "COMPONENT_PRESENT_NOT_APPLIED",
            },
            {
                "component": "source_lineage_requirement_schema_overlay",
                "path": rel(SOURCE_LINEAGE_REQUIREMENT_SCHEMA_OVERLAY_PATH),
                "review_status": "COMPONENT_PRESENT_NOT_APPLIED",
            },
            {
                "component": "row_identity_schema_overlay",
                "path": rel(SOURCE_ROW_IDENTITY_SCHEMA_OVERLAY_PATH),
                "review_status": "COMPONENT_PRESENT_NOT_APPLIED",
            },
        ],
    }

def decide(completeness_failures: List[str], consistency_failures: List[str], boundary_failures: List[str]) -> Tuple[str, List[str], str]:
    reason_codes = [
        "SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_REVIEWED",
        "SCHEMA_OVERLAY_COMPLETENESS_REVIEWED",
        "SCHEMA_OVERLAY_CONSISTENCY_REVIEWED",
        "SCHEMA_OVERLAY_NONAPPLICATION_BOUNDARY_REVIEWED",
        "SCHEMA_OVERLAY_COMPONENTS_REVIEWED",
        "NO_SCHEMA_OVERLAY_APPLIED",
        "NO_TYPING_RULE_APPLIED",
        "NO_FIELD_POLICY_MODIFIED",
        "NO_CANDIDATE_ARTIFACT_MODIFIED",
        "NO_REBINDS_APPLIED",
        "NO_VALUES_AUTHORIZED_OR_APPLIED",
        "NO_METADATA_POPULATION",
    ]

    if not completeness_failures and not consistency_failures and not boundary_failures:
        reason_codes.append("SCHEMA_OVERLAY_APPLICATION_CONTRACT_READY")
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_REVIEWED_APPLICATION_CONTRACT_READY"
        next_edge = "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_V0"
    else:
        reason_codes.append("SCHEMA_OVERLAY_REPAIR_REQUIRED")
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_REVIEWED_REPAIR_REQUIRED"
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0"

    return status, reason_codes, next_edge

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_authority_boundary_v0",
        "status": status,
        "may_review_schema_overlay": True,
        "may_emit_application_contract": True,
        "may_apply_schema_overlay": False,
        "may_apply_typing_rule": False,
        "may_modify_field_policy": False,
        "may_modify_candidate_artifacts": False,
        "may_apply_source_row_locator": False,
        "may_apply_rebinds": False,
        "may_apply_dominance_rule": False,
        "may_authorize_values": False,
        "may_apply_values": False,
        "may_accept_null_reasons_as_final": False,
        "may_materialize_source_packet_for_review": False,
        "may_populate_metadata": False,
        "may_evaluate_discriminators": False,
        "may_refine_dominance_rule": False,
        "may_break_tie": False,
        "may_emit_candidate_values_for_target": False,
        "may_declare_target_candidate_for_review": False,
        "may_select_target_for_build": False,
        "may_accept_for_build": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def rollup_obj(status: str, next_edge: str, completeness_failures: List[str], consistency_failures: List[str], boundary_failures: List[str]) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "schema_overlay_review_count": 1,
        "schema_overlay_component_review_count": 5,
        "schema_overlay_completeness_failure_count": len(completeness_failures),
        "schema_overlay_consistency_failure_count": len(consistency_failures),
        "schema_overlay_boundary_failure_count": len(boundary_failures),
        "application_contract_emitted_count": 1 if not completeness_failures and not consistency_failures and not boundary_failures else 0,
        "schema_overlay_applied_count": 0,
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

def profile_obj(roll: Dict[str, Any]) -> Dict[str, Any]:
    zero_keys = [
        "schema_overlay_applied_count",
        "typing_rule_applied_count",
        "field_policy_modified_count",
        "candidate_artifact_modified_count",
        "source_row_locator_applied_count",
        "rebinds_applied_count",
        "dominance_rule_applied_count",
        "refinements_applied_count",
        "values_authorized_count",
        "values_applied_count",
        "null_reason_accepted_count",
        "source_packet_materialized_for_review_count",
        "metadata_populated_count",
        "ready_discriminator_count",
        "rule_refined_count",
        "tie_broken_count",
        "candidate_values_filled_count",
        "target_candidate_declared_for_review_count",
        "target_selected_for_build_count",
        "accepted_for_build_count",
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "c5_opened_count",
        "general_cell1_authority_granted_count",
        "taxonomy_registry_mutation_count",
        "proposal_status_promoted_count",
        "accepted_proposal_fabricated_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "hidden_next_command_count",
        "unbounded_payload_inspection_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_profile_v0",
        "profile_id": "source_lineage_field_policy_schema_overlay_review_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "schema_overlay_reviewed": True,
        "application_contract_emitted": roll["application_contract_emitted_count"] == 1,
        "schema_overlay_applied": False,
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
        "rule_refined": False,
        "tie_broken": False,
        "candidate_values_filled": False,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(roll.get(k) == 0 for k in zero_keys),
        "recommended_next": roll["recommended_next"],
        "next_command_goal": None,
    }

def report_obj(status: str, reason_codes: List[str], roll: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The non-applicative schema overlay was reviewed for completeness, consistency, and boundary safety. This review may emit an application contract but does not apply the overlay.",
        "schema_overlay_review_count": roll["schema_overlay_review_count"],
        "schema_overlay_component_review_count": roll["schema_overlay_component_review_count"],
        "schema_overlay_completeness_failure_count": roll["schema_overlay_completeness_failure_count"],
        "schema_overlay_consistency_failure_count": roll["schema_overlay_consistency_failure_count"],
        "schema_overlay_boundary_failure_count": roll["schema_overlay_boundary_failure_count"],
        "application_contract_emitted_count": roll["application_contract_emitted_count"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "schema_overlay_applied_count": 0,
        "typing_rule_applied_count": 0,
        "field_policy_modified_count": 0,
        "candidate_artifact_modified_count": 0,
        "rebinds_applied_count": 0,
        "values_authorized_count": 0,
        "values_applied_count": 0,
        "source_packet_materialized_for_review_count": 0,
        "metadata_populated_count": 0,
        "ready_discriminator_count": 0,
        "tie_broken_count": 0,
        "accepted_for_build_count": 0,
        "runtime_patch_applied_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "hidden_next_command_count": 0,
    }

def transition_trace_obj(status: str, reason_codes: List[str], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_schema_overlay",
                "question": "is the non-applicative overlay coherent and complete",
                "answer": "review completeness, consistency, and non-application boundary",
                "taken": "emit overlay review assessment",
            },
            {
                "step": "classify_review_result",
                "question": "can an application contract be emitted for later review",
                "answer": status,
                "reason_codes": reason_codes,
                "taken": next_edge,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_basis()

    completeness_review, completeness_failures = review_completeness()
    consistency_review, consistency_failures = review_consistency()
    boundary_review, boundary_failures = review_boundary()
    component_review_obj = component_review()

    if failures:
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_REVIEW_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_REVIEW_BASIS_V0"
    else:
        status, reason_codes, next_edge = decide(completeness_failures, consistency_failures, boundary_failures)

    roll = rollup_obj(status, next_edge, completeness_failures, consistency_failures, boundary_failures)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    boundary = authority_boundary_obj(status)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    assessment = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_assessment_v0",
        "assessment_status": status,
        "source_schema_overlay_receipt_id": SOURCE_SCHEMA_OVERLAY_RECEIPT_ID,
        "schema_overlay_review_count": roll["schema_overlay_review_count"],
        "schema_overlay_component_review_count": roll["schema_overlay_component_review_count"],
        "schema_overlay_completeness_failure_count": roll["schema_overlay_completeness_failure_count"],
        "schema_overlay_consistency_failure_count": roll["schema_overlay_consistency_failure_count"],
        "schema_overlay_boundary_failure_count": roll["schema_overlay_boundary_failure_count"],
        "application_contract_emitted_count": roll["application_contract_emitted_count"],
        "review_claim": "overlay is reviewed for later application contract only; no application or mutation occurs in this unit",
        "recommended_next": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    preconditions = {
        "schema_version": "typed_machine_readable_schema_overlay_application_precondition_table_v0",
        "table_status": "SCHEMA_OVERLAY_APPLICATION_PRECONDITIONS_EMITTED",
        "records": [
            {
                "precondition": "schema_overlay_review_passed",
                "satisfied": status.endswith("APPLICATION_CONTRACT_READY"),
            },
            {
                "precondition": "human_or_prevalidated_schema_acceptance_available",
                "satisfied": False,
            },
            {
                "precondition": "explicit_application_unit_required",
                "satisfied": False,
            },
            {
                "precondition": "field_policy_mutation_authorized",
                "satisfied": False,
            },
            {
                "precondition": "candidate_artifact_mutation_authorized",
                "satisfied": False,
            },
            {
                "precondition": "source_ref_rebind_authorized",
                "satisfied": False,
            },
        ],
    }

    application_contract = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_v0",
        "contract_status": "SCHEMA_OVERLAY_APPLICATION_CONTRACT_READY_FOR_REVIEW" if status.endswith("APPLICATION_CONTRACT_READY") else "SCHEMA_OVERLAY_APPLICATION_CONTRACT_NOT_READY",
        "recommended_next_unit": next_edge,
        "application_candidate": status.endswith("APPLICATION_CONTRACT_READY"),
        "application_scope_if_later_accepted": [
            "represent source-role typing requirements",
            "represent field-policy enrichment requirements",
            "represent candidate-artifact typing requirements",
            "represent source-lineage requirements",
            "represent row-identity schema requirements",
        ],
        "application_must_not_include": [
            "source-ref rebind",
            "value extraction",
            "metadata population",
            "discriminator readiness",
            "runtime patch",
            "target selection",
            "C5 opening",
        ],
        "requires_before_application": [
            "separate application-contract review",
            "explicit human or prevalidated schema acceptance",
            "separate application unit",
        ],
        "schema_overlay_applied_now": False,
    }

    application_review_packet = {
        "schema_version": "typed_machine_readable_schema_overlay_application_review_packet_v0",
        "review_packet_status": "SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEW_REQUIRED",
        "question": "Review whether the schema overlay application contract may be accepted for a later application unit.",
        "allowed_responses": [
            "ACCEPT_APPLICATION_CONTRACT_FOR_APPLICATION_UNIT",
            "REPAIR_APPLICATION_CONTRACT",
            "FREEZE_SCHEMA_OVERLAY_REVIEW_AS_REFERENCE",
        ],
        "default_recommended_response": next_edge,
        "not_authorized": [
            "apply schema overlay",
            "modify field policy",
            "modify candidate artifacts",
            "rebind source refs",
            "extract values",
            "populate metadata",
        ],
    }

    decision_table = {
        "schema_version": "typed_machine_readable_schema_overlay_review_decision_table_v0",
        "decision_status": "SCHEMA_OVERLAY_REVIEW_DECISION_EMITTED",
        "records": [
            {
                "decision": "REVIEW_APPLICATION_CONTRACT",
                "selected": status.endswith("APPLICATION_CONTRACT_READY"),
                "next_unit": "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_V0",
                "why": "overlay review passed and emitted an application contract; application still requires later review and acceptance",
            },
            {
                "decision": "REPAIR_SCHEMA_OVERLAY",
                "selected": not status.endswith("APPLICATION_CONTRACT_READY"),
                "next_unit": "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_V0",
                "why": "use if completeness, consistency, or boundary review fails",
            },
            {
                "decision": "FREEZE_SCHEMA_OVERLAY_REVIEW",
                "selected": False,
                "next_unit": "FREEZE_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_REVIEW_V0",
                "why": "preserve review object without application path",
            },
        ],
    }

    classification = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "schema_overlay_reviewed": True,
        "application_contract_emitted": roll["application_contract_emitted_count"] == 1,
        "schema_overlay_component_review_count": roll["schema_overlay_component_review_count"],
        "schema_overlay_completeness_failure_count": roll["schema_overlay_completeness_failure_count"],
        "schema_overlay_consistency_failure_count": roll["schema_overlay_consistency_failure_count"],
        "schema_overlay_boundary_failure_count": roll["schema_overlay_boundary_failure_count"],
        "schema_overlay_applied": False,
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
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    write_json(REVIEW_ASSESSMENT_PATH, assessment)
    write_json(OVERLAY_COMPLETENESS_REVIEW_PATH, completeness_review)
    write_json(OVERLAY_CONSISTENCY_REVIEW_PATH, consistency_review)
    write_json(OVERLAY_BOUNDARY_REVIEW_PATH, boundary_review)
    write_json(OVERLAY_COMPONENT_REVIEW_PATH, component_review_obj)
    write_json(APPLICATION_PRECONDITION_TABLE_PATH, preconditions)
    write_json(APPLICATION_CONTRACT_PATH, application_contract)
    write_json(APPLICATION_REVIEW_PACKET_PATH, application_review_packet)
    write_json(REVIEW_DECISION_TABLE_PATH, decision_table)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, roll)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(TRANSITION_TRACE_PATH, trace)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        roll["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, roll)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "OVERLAY_REVIEW_0_SOURCE_RECEIPT_CONSUMED": SOURCE_SCHEMA_OVERLAY_RECEIPT_PATH.exists(),
        "OVERLAY_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "OVERLAY_REVIEW_2_COMPLETENESS_REVIEW_EMITTED": OVERLAY_COMPLETENESS_REVIEW_PATH.exists(),
        "OVERLAY_REVIEW_3_CONSISTENCY_REVIEW_EMITTED": OVERLAY_CONSISTENCY_REVIEW_PATH.exists(),
        "OVERLAY_REVIEW_4_BOUNDARY_REVIEW_EMITTED": OVERLAY_BOUNDARY_REVIEW_PATH.exists(),
        "OVERLAY_REVIEW_5_COMPONENT_REVIEW_EMITTED": OVERLAY_COMPONENT_REVIEW_PATH.exists(),
        "OVERLAY_REVIEW_6_APPLICATION_PRECONDITIONS_EMITTED": APPLICATION_PRECONDITION_TABLE_PATH.exists(),
        "OVERLAY_REVIEW_7_APPLICATION_CONTRACT_EMITTED": APPLICATION_CONTRACT_PATH.exists(),
        "OVERLAY_REVIEW_8_APPLICATION_REVIEW_PACKET_EMITTED": APPLICATION_REVIEW_PACKET_PATH.exists(),
        "OVERLAY_REVIEW_9_DECISION_TABLE_EMITTED": REVIEW_DECISION_TABLE_PATH.exists(),
        "OVERLAY_REVIEW_10_NO_SCHEMA_OVERLAY_APPLIED": roll["schema_overlay_applied_count"] == 0,
        "OVERLAY_REVIEW_11_NO_TYPING_RULE_APPLIED": roll["typing_rule_applied_count"] == 0,
        "OVERLAY_REVIEW_12_NO_FIELD_POLICY_MODIFIED": roll["field_policy_modified_count"] == 0,
        "OVERLAY_REVIEW_13_NO_CANDIDATE_ARTIFACT_MODIFIED": roll["candidate_artifact_modified_count"] == 0,
        "OVERLAY_REVIEW_14_NO_ROW_LOCATOR_APPLIED": roll["source_row_locator_applied_count"] == 0,
        "OVERLAY_REVIEW_15_NO_REBINDS_APPLIED": roll["rebinds_applied_count"] == 0,
        "OVERLAY_REVIEW_16_NO_DOMINANCE_RULE_APPLIED": roll["dominance_rule_applied_count"] == 0,
        "OVERLAY_REVIEW_17_NO_VALUES_AUTHORIZED": roll["values_authorized_count"] == 0,
        "OVERLAY_REVIEW_18_NO_VALUES_APPLIED": roll["values_applied_count"] == 0,
        "OVERLAY_REVIEW_19_NO_NULL_REASONS_ACCEPTED": roll["null_reason_accepted_count"] == 0,
        "OVERLAY_REVIEW_20_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "OVERLAY_REVIEW_21_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "OVERLAY_REVIEW_22_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "OVERLAY_REVIEW_23_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "OVERLAY_REVIEW_24_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "OVERLAY_REVIEW_25_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "OVERLAY_REVIEW_26_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "OVERLAY_REVIEW_27_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "OVERLAY_REVIEW_28_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "OVERLAY_REVIEW_29_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "OVERLAY_REVIEW_30_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "OVERLAY_REVIEW_31_NO_C5_OPENED": classification["c5_authorized"] is False,
        "OVERLAY_REVIEW_32_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "OVERLAY_REVIEW_33_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "OVERLAY_REVIEW_34_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "OVERLAY_REVIEW_35_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "OVERLAY_REVIEW_36_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "OVERLAY_REVIEW_37_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "component_review": roll["schema_overlay_component_review_count"],
        "application_contract": roll["application_contract_emitted_count"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_source_lineage_field_policy_schema_overlay_review_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_schema_overlay_receipt_id": SOURCE_SCHEMA_OVERLAY_RECEIPT_ID,
        "machine_readable_source_lineage_field_policy_schema_overlay_review_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "schema_overlay_reviewed": True,
            "schema_overlay_component_review_count": roll["schema_overlay_component_review_count"],
            "schema_overlay_completeness_failure_count": roll["schema_overlay_completeness_failure_count"],
            "schema_overlay_consistency_failure_count": roll["schema_overlay_consistency_failure_count"],
            "schema_overlay_boundary_failure_count": roll["schema_overlay_boundary_failure_count"],
            "application_contract_emitted": roll["application_contract_emitted_count"] == 1,
            "schema_overlay_applied": False,
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
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
            "bad_counters_zero": prof["bad_counters_zero"],
            "recommended_next": next_edge,
        },
        "aggregate_metrics": rep,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "overlay_completeness_review": rel(OVERLAY_COMPLETENESS_REVIEW_PATH),
            "overlay_consistency_review": rel(OVERLAY_CONSISTENCY_REVIEW_PATH),
            "overlay_boundary_review": rel(OVERLAY_BOUNDARY_REVIEW_PATH),
            "overlay_component_review": rel(OVERLAY_COMPONENT_REVIEW_PATH),
            "application_precondition_table": rel(APPLICATION_PRECONDITION_TABLE_PATH),
            "application_contract": rel(APPLICATION_CONTRACT_PATH),
            "application_review_packet": rel(APPLICATION_REVIEW_PACKET_PATH),
            "review_decision_table": rel(REVIEW_DECISION_TABLE_PATH),
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
    print(f"source_lineage_field_policy_schema_overlay_review_receipt_id={receipt_id}")
    print(f"source_lineage_field_policy_schema_overlay_review_receipt_path={rel(receipt_path)}")
    print(f"schema_overlay_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"schema_overlay_completeness_review_path={rel(OVERLAY_COMPLETENESS_REVIEW_PATH)}")
    print(f"schema_overlay_consistency_review_path={rel(OVERLAY_CONSISTENCY_REVIEW_PATH)}")
    print(f"schema_overlay_boundary_review_path={rel(OVERLAY_BOUNDARY_REVIEW_PATH)}")
    print(f"schema_overlay_application_contract_path={rel(APPLICATION_CONTRACT_PATH)}")
    print(f"schema_overlay_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"schema_overlay_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
