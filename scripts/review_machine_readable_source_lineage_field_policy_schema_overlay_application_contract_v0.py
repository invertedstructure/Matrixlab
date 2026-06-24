#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEW"
MODE = "APPLICATION_CONTRACT_REVIEW / NO_SCHEMA_OVERLAY_APPLICATION / NO_TYPING_RULE_APPLICATION / NO_POLICY_MODIFICATION / NO_CANDIDATE_MODIFICATION / NO_REBIND / NO_METADATA_FILL"
BUILD_MODE = "SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEW_ONLY"

SOURCE_OVERLAY_REVIEW_RECEIPT_ID = "fe0ffb41"
SOURCE_OVERLAY_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0_receipts/fe0ffb41.json"
SOURCE_REVIEW_ASSESSMENT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_review_assessment_v0.json"
SOURCE_COMPLETENESS_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0/typed_machine_readable_schema_overlay_completeness_review_v0.json"
SOURCE_CONSISTENCY_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0/typed_machine_readable_schema_overlay_consistency_review_v0.json"
SOURCE_BOUNDARY_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0/typed_machine_readable_schema_overlay_nonapplication_boundary_review_v0.json"
SOURCE_COMPONENT_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0/typed_machine_readable_schema_overlay_component_review_v0.json"
SOURCE_APPLICATION_PRECONDITION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0/typed_machine_readable_schema_overlay_application_precondition_table_v0.json"
SOURCE_APPLICATION_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0/typed_machine_readable_schema_overlay_application_contract_v0.json"
SOURCE_APPLICATION_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0/typed_machine_readable_schema_overlay_application_review_packet_v0.json"
SOURCE_REVIEW_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0/typed_machine_readable_schema_overlay_review_decision_table_v0.json"
SOURCE_REVIEW_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_review_classification_v0.json"
SOURCE_REVIEW_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_review_authority_boundary_v0.json"
SOURCE_REVIEW_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_review_rollup_v0.json"
SOURCE_REVIEW_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_review_v0/typed_machine_readable_source_lineage_field_policy_schema_overlay_review_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0_receipts"

APPLICATION_CONTRACT_REVIEW_ASSESSMENT_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_review_assessment_v0.json"
APPLICATION_SCOPE_REVIEW_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_scope_review_v0.json"
APPLICATION_FORBIDDEN_ACTION_REVIEW_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_forbidden_action_review_v0.json"
APPLICATION_PRECONDITION_REVIEW_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_precondition_review_v0.json"
APPLICATION_AUTHORIZATION_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_authorization_boundary_v0.json"
APPLICATION_UNIT_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_contract_v0.json"
APPLICATION_ACCEPTANCE_REQUEST_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_acceptance_request_v0.json"
APPLICATION_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_review_decision_table_v0.json"
APPLICATION_REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_review_packet_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_review_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_review_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_review_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_OVERLAY_REVIEW_RECEIPT_PATH,
    SOURCE_REVIEW_ASSESSMENT_PATH,
    SOURCE_COMPLETENESS_REVIEW_PATH,
    SOURCE_CONSISTENCY_REVIEW_PATH,
    SOURCE_BOUNDARY_REVIEW_PATH,
    SOURCE_COMPONENT_REVIEW_PATH,
    SOURCE_APPLICATION_PRECONDITION_TABLE_PATH,
    SOURCE_APPLICATION_CONTRACT_PATH,
    SOURCE_APPLICATION_REVIEW_PACKET_PATH,
    SOURCE_REVIEW_DECISION_TABLE_PATH,
    SOURCE_REVIEW_CLASSIFICATION_PATH,
    SOURCE_REVIEW_AUTHORITY_BOUNDARY_PATH,
    SOURCE_REVIEW_ROLLUP_PATH,
    SOURCE_REVIEW_PROFILE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_REVIEWED_APPLICATION_CONTRACT_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_REVIEWED_APPLICATION_CONTRACT_READY"
EXPECTED_NEXT = "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_V0"

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
    for key in ["records", "checks", "preconditions"]:
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

    receipt = read_json(SOURCE_OVERLAY_REVIEW_RECEIPT_PATH)
    summary = receipt.get("machine_readable_source_lineage_field_policy_schema_overlay_review_summary", {})
    app_contract = read_json(SOURCE_APPLICATION_CONTRACT_PATH)
    preconditions = read_json(SOURCE_APPLICATION_PRECONDITION_TABLE_PATH)
    classif = read_json(SOURCE_REVIEW_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_REVIEW_ROLLUP_PATH)
    profile = read_json(SOURCE_REVIEW_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_OVERLAY_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_overlay_review_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_overlay_review_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_overlay_review_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"source_overlay_review_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("schema_overlay_reviewed") is not True:
        failures.append("source_overlay_not_reviewed")
    if summary.get("schema_overlay_component_review_count") != 5:
        failures.append("component_review_count_not_5")
    if summary.get("schema_overlay_completeness_failure_count") != 0:
        failures.append("completeness_failures_nonzero")
    if summary.get("schema_overlay_consistency_failure_count") != 0:
        failures.append("consistency_failures_nonzero")
    if summary.get("schema_overlay_boundary_failure_count") != 0:
        failures.append("boundary_failures_nonzero")
    if summary.get("application_contract_emitted") is not True:
        failures.append("application_contract_not_emitted")
    for key in [
        "schema_overlay_applied",
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

    if app_contract.get("contract_status") != "SCHEMA_OVERLAY_APPLICATION_CONTRACT_READY_FOR_REVIEW":
        failures.append("application_contract_not_ready_for_review")
    if app_contract.get("application_candidate") is not True:
        failures.append("application_contract_candidate_not_true")
    if app_contract.get("schema_overlay_applied_now") is not False:
        failures.append("application_contract_claims_applied_now")
    if len(app_contract.get("application_scope_if_later_accepted", [])) != 5:
        failures.append("application_scope_count_not_5")
    forbidden = set(app_contract.get("application_must_not_include", []))
    for item in ["source-ref rebind", "value extraction", "metadata population", "discriminator readiness", "runtime patch", "target selection", "C5 opening"]:
        if item not in forbidden:
            failures.append(f"application_must_not_missing:{item}")
    required = set(app_contract.get("requires_before_application", []))
    for item in ["separate application-contract review", "explicit human or prevalidated schema acceptance", "separate application unit"]:
        if item not in required:
            failures.append(f"requires_before_application_missing:{item}")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("source_classification_status_wrong")
    if roll.get("schema_overlay_applied_count") != 0:
        failures.append("source_rollup_overlay_applied_nonzero")
    if profile.get("schema_overlay_applied") is not False:
        failures.append("source_profile_overlay_applied_true")

    return failures

def review_scope(app_contract: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    expected = {
        "represent source-role typing requirements",
        "represent field-policy enrichment requirements",
        "represent candidate-artifact typing requirements",
        "represent source-lineage requirements",
        "represent row-identity schema requirements",
    }
    observed = set(app_contract.get("application_scope_if_later_accepted", []))
    missing = sorted(expected - observed)
    return {
        "schema_version": "typed_machine_readable_schema_overlay_application_scope_review_v0",
        "review_status": "APPLICATION_SCOPE_REVIEW_PASS" if not missing else "APPLICATION_SCOPE_REVIEW_FAIL",
        "expected_scope": sorted(expected),
        "observed_scope": sorted(observed),
        "missing_scope": missing,
        "scope_claim": "application scope is limited to representing schema overlay typing requirements if later accepted",
    }, missing

def review_forbidden_actions(app_contract: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    expected = {
        "source-ref rebind",
        "value extraction",
        "metadata population",
        "discriminator readiness",
        "runtime patch",
        "target selection",
        "C5 opening",
    }
    observed = set(app_contract.get("application_must_not_include", []))
    missing = sorted(expected - observed)
    return {
        "schema_version": "typed_machine_readable_schema_overlay_application_forbidden_action_review_v0",
        "review_status": "APPLICATION_FORBIDDEN_ACTION_REVIEW_PASS" if not missing else "APPLICATION_FORBIDDEN_ACTION_REVIEW_FAIL",
        "expected_forbidden_actions": sorted(expected),
        "observed_forbidden_actions": sorted(observed),
        "missing_forbidden_actions": missing,
        "forbidden_action_claim": "application contract explicitly excludes rebinds, values, metadata, target selection, runtime patch, and C5",
    }, missing

def review_preconditions(app_contract: Dict[str, Any], precondition_table: Dict[str, Any]) -> Tuple[Dict[str, Any], List[str]]:
    required = {
        "separate application-contract review",
        "explicit human or prevalidated schema acceptance",
        "separate application unit",
    }
    observed_required = set(app_contract.get("requires_before_application", []))
    missing_required = sorted(required - observed_required)

    rows = records(precondition_table)
    precondition_states = {str(r.get("precondition")): r.get("satisfied") for r in rows}
    expected_unsatisfied = {
        "human_or_prevalidated_schema_acceptance_available",
        "explicit_application_unit_required",
        "field_policy_mutation_authorized",
        "candidate_artifact_mutation_authorized",
        "source_ref_rebind_authorized",
    }
    wrong_satisfied = sorted(k for k in expected_unsatisfied if precondition_states.get(k) is True)

    failures = missing_required + [f"precondition_should_not_be_satisfied:{x}" for x in wrong_satisfied]
    return {
        "schema_version": "typed_machine_readable_schema_overlay_application_precondition_review_v0",
        "review_status": "APPLICATION_PRECONDITION_REVIEW_PASS" if not failures else "APPLICATION_PRECONDITION_REVIEW_FAIL",
        "required_before_application": sorted(required),
        "observed_required_before_application": sorted(observed_required),
        "missing_required_before_application": missing_required,
        "precondition_states": precondition_states,
        "wrongly_satisfied_preconditions": wrong_satisfied,
        "precondition_claim": "application remains blocked until explicit acceptance and a separate application unit exist",
    }, failures

def decide(scope_failures: List[str], forbidden_failures: List[str], precondition_failures: List[str]) -> Tuple[str, List[str], str]:
    reason_codes = [
        "SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEWED",
        "APPLICATION_SCOPE_REVIEWED",
        "APPLICATION_FORBIDDEN_ACTIONS_REVIEWED",
        "APPLICATION_PRECONDITIONS_REVIEWED",
        "APPLICATION_AUTHORIZATION_BOUNDARY_EMITTED",
        "NO_SCHEMA_OVERLAY_APPLIED",
        "NO_TYPING_RULE_APPLIED",
        "NO_FIELD_POLICY_MODIFIED",
        "NO_CANDIDATE_ARTIFACT_MODIFIED",
        "NO_REBINDS_APPLIED",
        "NO_VALUES_AUTHORIZED_OR_APPLIED",
        "NO_METADATA_POPULATION",
    ]

    if not scope_failures and not forbidden_failures and not precondition_failures:
        reason_codes.append("APPLICATION_CONTRACT_REVIEWED_ACCEPTANCE_REQUIRED")
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEWED_ACCEPTANCE_REQUIRED"
        next_edge = "AUTHORIZE_OR_REJECT_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_V0"
    else:
        reason_codes.append("APPLICATION_CONTRACT_REPAIR_REQUIRED")
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEWED_REPAIR_REQUIRED"
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_V0"

    return status, reason_codes, next_edge

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_review_authority_boundary_v0",
        "status": status,
        "may_review_application_contract": True,
        "may_emit_acceptance_request": True,
        "may_emit_application_unit_contract": True,
        "may_accept_application_contract": False,
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

def rollup_obj(status: str, next_edge: str, scope_failures: List[str], forbidden_failures: List[str], precondition_failures: List[str]) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "application_contract_review_count": 1,
        "application_scope_failure_count": len(scope_failures),
        "application_forbidden_action_failure_count": len(forbidden_failures),
        "application_precondition_failure_count": len(precondition_failures),
        "application_unit_contract_emitted_count": 1 if not scope_failures and not forbidden_failures and not precondition_failures else 0,
        "application_acceptance_request_emitted_count": 1 if not scope_failures and not forbidden_failures and not precondition_failures else 0,
        "application_contract_accepted_count": 0,
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
        "application_contract_accepted_count",
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
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_review_profile_v0",
        "profile_id": "schema_overlay_application_contract_review_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "application_contract_reviewed": True,
        "application_unit_contract_emitted": roll["application_unit_contract_emitted_count"] == 1,
        "application_acceptance_request_emitted": roll["application_acceptance_request_emitted_count"] == 1,
        "application_contract_accepted": False,
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
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The schema-overlay application contract was reviewed. This unit emits an acceptance request and application-unit contract if safe, but does not accept or apply the contract.",
        "application_contract_review_count": roll["application_contract_review_count"],
        "application_scope_failure_count": roll["application_scope_failure_count"],
        "application_forbidden_action_failure_count": roll["application_forbidden_action_failure_count"],
        "application_precondition_failure_count": roll["application_precondition_failure_count"],
        "application_unit_contract_emitted_count": roll["application_unit_contract_emitted_count"],
        "application_acceptance_request_emitted_count": roll["application_acceptance_request_emitted_count"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "application_contract_accepted_count": 0,
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
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_application_contract",
                "question": "is the application contract safe enough to request acceptance",
                "answer": "review scope, forbidden actions, and preconditions",
                "taken": "emit application contract review assessment",
            },
            {
                "step": "classify_application_contract_review",
                "question": "can acceptance be requested without applying anything",
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

    app_contract = read_json(SOURCE_APPLICATION_CONTRACT_PATH)
    precondition_table = read_json(SOURCE_APPLICATION_PRECONDITION_TABLE_PATH)

    scope_review, scope_failures = review_scope(app_contract)
    forbidden_review, forbidden_failures = review_forbidden_actions(app_contract)
    precondition_review, precondition_failures = review_preconditions(app_contract, precondition_table)

    if failures:
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEW_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEW_BASIS_V0"
    else:
        status, reason_codes, next_edge = decide(scope_failures, forbidden_failures, precondition_failures)

    roll = rollup_obj(status, next_edge, scope_failures, forbidden_failures, precondition_failures)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    authority = authority_boundary_obj(status)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    review_assessment = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_review_assessment_v0",
        "assessment_status": status,
        "source_overlay_review_receipt_id": SOURCE_OVERLAY_REVIEW_RECEIPT_ID,
        "application_contract_review_count": roll["application_contract_review_count"],
        "application_scope_failure_count": roll["application_scope_failure_count"],
        "application_forbidden_action_failure_count": roll["application_forbidden_action_failure_count"],
        "application_precondition_failure_count": roll["application_precondition_failure_count"],
        "application_unit_contract_emitted_count": roll["application_unit_contract_emitted_count"],
        "application_acceptance_request_emitted_count": roll["application_acceptance_request_emitted_count"],
        "review_claim": "application contract can request acceptance only; it cannot accept or apply itself",
        "recommended_next": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    app_auth_boundary = {
        "schema_version": "typed_machine_readable_schema_overlay_application_authorization_boundary_v0",
        "boundary_status": "APPLICATION_ACCEPTANCE_REQUIRED_NOT_GRANTED",
        "application_contract_reviewed": True,
        "acceptance_required": True,
        "accepted_now": False,
        "application_unit_may_be_built_after_acceptance": True,
        "application_unit_may_run_now": False,
        "authority_required": "human_or_prevalidated_schema_acceptance",
        "forbidden_without_acceptance": [
            "schema overlay application",
            "typing rule application",
            "field policy modification",
            "candidate artifact modification",
            "source-ref rebind",
            "value extraction",
            "metadata population",
            "discriminator readiness",
        ],
    }

    app_unit_contract = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_contract_v0",
        "contract_status": "APPLICATION_UNIT_CONTRACT_EMITTED_NOT_ACCEPTED",
        "may_be_used_only_after": [
            "application contract accepted",
            "explicit application unit invoked",
        ],
        "application_scope": app_contract.get("application_scope_if_later_accepted", []),
        "application_forbidden_actions": app_contract.get("application_must_not_include", []),
        "application_required_preconditions": app_contract.get("requires_before_application", []),
        "accepted_now": False,
        "schema_overlay_applied_now": False,
    }

    acceptance_request = {
        "schema_version": "typed_machine_readable_schema_overlay_application_acceptance_request_v0",
        "request_status": "APPLICATION_CONTRACT_ACCEPTANCE_REQUIRED",
        "question": "Accept, reject, or repair the schema overlay application contract before any application unit may be run.",
        "allowed_responses": [
            "ACCEPT_SCHEMA_OVERLAY_APPLICATION_CONTRACT_FOR_APPLICATION_UNIT",
            "REJECT_SCHEMA_OVERLAY_APPLICATION_CONTRACT",
            "REPAIR_SCHEMA_OVERLAY_APPLICATION_CONTRACT",
            "FREEZE_SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEW",
        ],
        "default_recommended_response": "AUTHORIZE_OR_REJECT_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_V0",
        "accepted_now": False,
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
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_review_decision_table_v0",
        "decision_status": "APPLICATION_CONTRACT_REVIEW_DECISION_EMITTED",
        "records": [
            {
                "decision": "REQUEST_ACCEPTANCE",
                "selected": status.endswith("ACCEPTANCE_REQUIRED"),
                "next_unit": "AUTHORIZE_OR_REJECT_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_V0",
                "why": "application contract is safe enough to request acceptance, but acceptance is not granted in this unit",
            },
            {
                "decision": "REPAIR_APPLICATION_CONTRACT",
                "selected": status.endswith("REPAIR_REQUIRED"),
                "next_unit": "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_V0",
                "why": "use if scope, forbidden action, or precondition review fails",
            },
            {
                "decision": "FREEZE_APPLICATION_CONTRACT_REVIEW",
                "selected": False,
                "next_unit": "FREEZE_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEW_V0",
                "why": "preserve this review object without continuing toward application",
            },
        ],
    }

    review_packet = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_review_packet_v0",
        "review_packet_status": "APPLICATION_CONTRACT_REVIEW_COMPLETE_ACCEPTANCE_REQUIRED",
        "summary": {
            "scope_failures": scope_failures,
            "forbidden_action_failures": forbidden_failures,
            "precondition_failures": precondition_failures,
            "application_unit_contract_emitted": roll["application_unit_contract_emitted_count"] == 1,
            "application_acceptance_request_emitted": roll["application_acceptance_request_emitted_count"] == 1,
        },
        "recommended_next": next_edge,
        "not_authorized": [
            "schema overlay application",
            "typing rule application",
            "field policy modification",
            "candidate artifact modification",
            "source-ref rebind",
            "value extraction",
            "metadata population",
        ],
    }

    classification = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "application_contract_reviewed": True,
        "application_scope_failure_count": roll["application_scope_failure_count"],
        "application_forbidden_action_failure_count": roll["application_forbidden_action_failure_count"],
        "application_precondition_failure_count": roll["application_precondition_failure_count"],
        "application_unit_contract_emitted": roll["application_unit_contract_emitted_count"] == 1,
        "application_acceptance_request_emitted": roll["application_acceptance_request_emitted_count"] == 1,
        "application_contract_accepted": False,
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

    write_json(APPLICATION_CONTRACT_REVIEW_ASSESSMENT_PATH, review_assessment)
    write_json(APPLICATION_SCOPE_REVIEW_PATH, scope_review)
    write_json(APPLICATION_FORBIDDEN_ACTION_REVIEW_PATH, forbidden_review)
    write_json(APPLICATION_PRECONDITION_REVIEW_PATH, precondition_review)
    write_json(APPLICATION_AUTHORIZATION_BOUNDARY_PATH, app_auth_boundary)
    write_json(APPLICATION_UNIT_CONTRACT_PATH, app_unit_contract)
    write_json(APPLICATION_ACCEPTANCE_REQUEST_PATH, acceptance_request)
    write_json(APPLICATION_DECISION_TABLE_PATH, decision_table)
    write_json(APPLICATION_REVIEW_PACKET_PATH, review_packet)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_BOUNDARY_PATH, authority)
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
        "APP_CONTRACT_REVIEW_0_SOURCE_RECEIPT_CONSUMED": SOURCE_OVERLAY_REVIEW_RECEIPT_PATH.exists(),
        "APP_CONTRACT_REVIEW_1_CONTRACT_REVIEW_ASSESSMENT_EMITTED": APPLICATION_CONTRACT_REVIEW_ASSESSMENT_PATH.exists(),
        "APP_CONTRACT_REVIEW_2_APPLICATION_SCOPE_REVIEW_EMITTED": APPLICATION_SCOPE_REVIEW_PATH.exists(),
        "APP_CONTRACT_REVIEW_3_FORBIDDEN_ACTION_REVIEW_EMITTED": APPLICATION_FORBIDDEN_ACTION_REVIEW_PATH.exists(),
        "APP_CONTRACT_REVIEW_4_PRECONDITION_REVIEW_EMITTED": APPLICATION_PRECONDITION_REVIEW_PATH.exists(),
        "APP_CONTRACT_REVIEW_5_AUTHORIZATION_BOUNDARY_EMITTED": APPLICATION_AUTHORIZATION_BOUNDARY_PATH.exists(),
        "APP_CONTRACT_REVIEW_6_APPLICATION_UNIT_CONTRACT_EMITTED": APPLICATION_UNIT_CONTRACT_PATH.exists(),
        "APP_CONTRACT_REVIEW_7_ACCEPTANCE_REQUEST_EMITTED": APPLICATION_ACCEPTANCE_REQUEST_PATH.exists(),
        "APP_CONTRACT_REVIEW_8_DECISION_TABLE_EMITTED": APPLICATION_DECISION_TABLE_PATH.exists(),
        "APP_CONTRACT_REVIEW_9_REVIEW_PACKET_EMITTED": APPLICATION_REVIEW_PACKET_PATH.exists(),
        "APP_CONTRACT_REVIEW_10_NO_APPLICATION_CONTRACT_ACCEPTED": roll["application_contract_accepted_count"] == 0,
        "APP_CONTRACT_REVIEW_11_NO_SCHEMA_OVERLAY_APPLIED": roll["schema_overlay_applied_count"] == 0,
        "APP_CONTRACT_REVIEW_12_NO_TYPING_RULE_APPLIED": roll["typing_rule_applied_count"] == 0,
        "APP_CONTRACT_REVIEW_13_NO_FIELD_POLICY_MODIFIED": roll["field_policy_modified_count"] == 0,
        "APP_CONTRACT_REVIEW_14_NO_CANDIDATE_ARTIFACT_MODIFIED": roll["candidate_artifact_modified_count"] == 0,
        "APP_CONTRACT_REVIEW_15_NO_ROW_LOCATOR_APPLIED": roll["source_row_locator_applied_count"] == 0,
        "APP_CONTRACT_REVIEW_16_NO_REBINDS_APPLIED": roll["rebinds_applied_count"] == 0,
        "APP_CONTRACT_REVIEW_17_NO_DOMINANCE_RULE_APPLIED": roll["dominance_rule_applied_count"] == 0,
        "APP_CONTRACT_REVIEW_18_NO_VALUES_AUTHORIZED": roll["values_authorized_count"] == 0,
        "APP_CONTRACT_REVIEW_19_NO_VALUES_APPLIED": roll["values_applied_count"] == 0,
        "APP_CONTRACT_REVIEW_20_NO_NULL_REASONS_ACCEPTED": roll["null_reason_accepted_count"] == 0,
        "APP_CONTRACT_REVIEW_21_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "APP_CONTRACT_REVIEW_22_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "APP_CONTRACT_REVIEW_23_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "APP_CONTRACT_REVIEW_24_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "APP_CONTRACT_REVIEW_25_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "APP_CONTRACT_REVIEW_26_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "APP_CONTRACT_REVIEW_27_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "APP_CONTRACT_REVIEW_28_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "APP_CONTRACT_REVIEW_29_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "APP_CONTRACT_REVIEW_30_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "APP_CONTRACT_REVIEW_31_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "APP_CONTRACT_REVIEW_32_NO_C5_OPENED": classification["c5_authorized"] is False,
        "APP_CONTRACT_REVIEW_33_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "APP_CONTRACT_REVIEW_34_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "APP_CONTRACT_REVIEW_35_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "APP_CONTRACT_REVIEW_36_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "APP_CONTRACT_REVIEW_37_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "APP_CONTRACT_REVIEW_38_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "scope_failures": scope_failures,
        "forbidden_failures": forbidden_failures,
        "precondition_failures": precondition_failures,
        "accepted": False,
        "applied": False,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_review_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_overlay_review_receipt_id": SOURCE_OVERLAY_REVIEW_RECEIPT_ID,
        "machine_readable_schema_overlay_application_contract_review_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "application_contract_reviewed": True,
            "application_scope_failure_count": roll["application_scope_failure_count"],
            "application_forbidden_action_failure_count": roll["application_forbidden_action_failure_count"],
            "application_precondition_failure_count": roll["application_precondition_failure_count"],
            "application_unit_contract_emitted": roll["application_unit_contract_emitted_count"] == 1,
            "application_acceptance_request_emitted": roll["application_acceptance_request_emitted_count"] == 1,
            "application_contract_accepted": False,
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
            "application_contract_review_assessment": rel(APPLICATION_CONTRACT_REVIEW_ASSESSMENT_PATH),
            "application_scope_review": rel(APPLICATION_SCOPE_REVIEW_PATH),
            "application_forbidden_action_review": rel(APPLICATION_FORBIDDEN_ACTION_REVIEW_PATH),
            "application_precondition_review": rel(APPLICATION_PRECONDITION_REVIEW_PATH),
            "application_authorization_boundary": rel(APPLICATION_AUTHORIZATION_BOUNDARY_PATH),
            "application_unit_contract": rel(APPLICATION_UNIT_CONTRACT_PATH),
            "application_acceptance_request": rel(APPLICATION_ACCEPTANCE_REQUEST_PATH),
            "application_decision_table": rel(APPLICATION_DECISION_TABLE_PATH),
            "application_review_packet": rel(APPLICATION_REVIEW_PACKET_PATH),
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
    print(f"schema_overlay_application_contract_review_receipt_id={receipt_id}")
    print(f"schema_overlay_application_contract_review_receipt_path={rel(receipt_path)}")
    print(f"schema_overlay_application_contract_review_assessment_path={rel(APPLICATION_CONTRACT_REVIEW_ASSESSMENT_PATH)}")
    print(f"schema_overlay_application_scope_review_path={rel(APPLICATION_SCOPE_REVIEW_PATH)}")
    print(f"schema_overlay_application_forbidden_action_review_path={rel(APPLICATION_FORBIDDEN_ACTION_REVIEW_PATH)}")
    print(f"schema_overlay_application_precondition_review_path={rel(APPLICATION_PRECONDITION_REVIEW_PATH)}")
    print(f"schema_overlay_application_authorization_boundary_path={rel(APPLICATION_AUTHORIZATION_BOUNDARY_PATH)}")
    print(f"schema_overlay_application_unit_contract_path={rel(APPLICATION_UNIT_CONTRACT_PATH)}")
    print(f"schema_overlay_application_acceptance_request_path={rel(APPLICATION_ACCEPTANCE_REQUEST_PATH)}")
    print(f"schema_overlay_application_contract_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"schema_overlay_application_contract_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
