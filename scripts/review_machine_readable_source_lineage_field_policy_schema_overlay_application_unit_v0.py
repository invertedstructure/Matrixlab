#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEW"
MODE = "SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEW / DOWNSTREAM_USE_GATE / NO_REUSABLE_SCHEMA / NO_REBIND / NO_VALUES / NO_METADATA"
BUILD_MODE = "SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEW_ONLY"

SOURCE_APP_UNIT_RECEIPT_ID = "1d2d38de"
SOURCE_APP_UNIT_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0_receipts/1d2d38de.json"
SOURCE_APP_UNIT_RECORD_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0/typed_machine_readable_schema_overlay_application_unit_record_v0.json"
SOURCE_APPLIED_REFERENCE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0/typed_machine_readable_schema_overlay_applied_reference_v0.json"
SOURCE_FRAME_BINDING_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0/typed_machine_readable_schema_overlay_application_frame_binding_v0.json"
SOURCE_COMPONENT_BINDING_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0/typed_machine_readable_schema_overlay_application_component_binding_v0.json"
SOURCE_NON_REUSE_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0/typed_machine_readable_schema_overlay_application_non_reuse_boundary_v0.json"
SOURCE_EFFECTS_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0/typed_machine_readable_schema_overlay_application_effects_table_v0.json"
SOURCE_DOWNSTREAM_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0/typed_machine_readable_schema_overlay_application_downstream_contract_v0.json"
SOURCE_APP_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0/typed_machine_readable_schema_overlay_application_unit_review_packet_v0.json"
SOURCE_APP_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0/typed_machine_readable_schema_overlay_application_unit_decision_table_v0.json"
SOURCE_APP_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0/typed_machine_readable_schema_overlay_application_unit_classification_v0.json"
SOURCE_APP_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0/typed_machine_readable_schema_overlay_application_unit_authority_boundary_v0.json"
SOURCE_APP_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0/typed_machine_readable_schema_overlay_application_unit_rollup_v0.json"
SOURCE_APP_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_v0/typed_machine_readable_schema_overlay_application_unit_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_review_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_unit_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_review_assessment_v0.json"
APPLIED_REFERENCE_REVIEW_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_applied_reference_review_v0.json"
FRAME_BINDING_REVIEW_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_frame_binding_review_v0.json"
COMPONENT_BINDING_REVIEW_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_component_binding_review_v0.json"
NON_REUSE_BOUNDARY_REVIEW_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_non_reuse_boundary_review_v0.json"
EFFECTS_REVIEW_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_effects_review_v0.json"
DOWNSTREAM_CONTRACT_REVIEW_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_downstream_contract_review_v0.json"
DOWNSTREAM_USE_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_accepted_reference_downstream_use_contract_v0.json"
RETURN_TO_REBIND_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_return_to_rebind_review_contract_v0.json"
REVIEW_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_review_decision_table_v0.json"
REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_review_result_packet_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_review_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_review_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_unit_review_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_APP_UNIT_RECEIPT_PATH,
    SOURCE_APP_UNIT_RECORD_PATH,
    SOURCE_APPLIED_REFERENCE_PATH,
    SOURCE_FRAME_BINDING_PATH,
    SOURCE_COMPONENT_BINDING_PATH,
    SOURCE_NON_REUSE_BOUNDARY_PATH,
    SOURCE_EFFECTS_TABLE_PATH,
    SOURCE_DOWNSTREAM_CONTRACT_PATH,
    SOURCE_APP_REVIEW_PACKET_PATH,
    SOURCE_APP_DECISION_TABLE_PATH,
    SOURCE_APP_CLASSIFICATION_PATH,
    SOURCE_APP_AUTHORITY_BOUNDARY_PATH,
    SOURCE_APP_ROLLUP_PATH,
    SOURCE_APP_PROFILE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLIED_AS_ONE_TIME_ACCEPTED_REFERENCE"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLIED_AS_ONE_TIME_ACCEPTED_REFERENCE"
EXPECTED_SOURCE_NEXT = "REVIEW_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_V0"

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

    receipt = read_json(SOURCE_APP_UNIT_RECEIPT_PATH)
    summary = receipt.get("machine_readable_schema_overlay_application_unit_summary", {})
    unit_record = read_json(SOURCE_APP_UNIT_RECORD_PATH)
    applied_reference = read_json(SOURCE_APPLIED_REFERENCE_PATH)
    frame_binding = read_json(SOURCE_FRAME_BINDING_PATH)
    component_binding = read_json(SOURCE_COMPONENT_BINDING_PATH)
    non_reuse = read_json(SOURCE_NON_REUSE_BOUNDARY_PATH)
    effects = read_json(SOURCE_EFFECTS_TABLE_PATH)
    downstream = read_json(SOURCE_DOWNSTREAM_CONTRACT_PATH)
    classif = read_json(SOURCE_APP_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_APP_ROLLUP_PATH)
    profile = read_json(SOURCE_APP_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_APP_UNIT_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_application_unit_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_application_unit_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_application_unit_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_application_unit_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "schema_overlay_application_unit_built",
        "schema_overlay_applied_for_this_contract",
        "applied_as_reference_for_this_application_contract",
        "one_time_acceptance",
        "accepted_for_this_application_contract",
    ]:
        if summary.get(key) is not True:
            failures.append(f"required_true_missing:{key}")

    if summary.get("component_reference_binding_count") != 5:
        failures.append("component_reference_binding_count_not_5")

    for key in [
        "schema_overlay_applied_globally",
        "reusable_schema_authorized",
        "preapproved_schema_authorized",
        "validator_registry_entry_created",
        "future_automatic_use_allowed",
        "typing_rule_applied",
        "field_policy_modified",
        "candidate_artifact_modified",
        "source_row_locator_applied",
        "rebinds_applied",
        "dominance_rule_applied",
        "values_authorized",
        "values_applied",
        "metadata_populated",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
    ]:
        if summary.get(key) is not False:
            failures.append(f"source_summary_forbidden_true:{key}")

    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")

    if unit_record.get("application_status") != EXPECTED_SOURCE_STATUS:
        failures.append("application_unit_record_status_wrong")
    if unit_record.get("schema_overlay_applied_globally") is not False:
        failures.append("unit_record_claims_global_application")
    if applied_reference.get("reference_status") != "SCHEMA_OVERLAY_REFERENCE_APPLIED_ONE_TIME":
        failures.append("applied_reference_status_wrong")
    if len(applied_reference.get("component_references", [])) != 5:
        failures.append("applied_reference_component_count_not_5")
    if applied_reference.get("scope") != "this_application_contract_only":
        failures.append("applied_reference_scope_wrong")
    if frame_binding.get("binding_status") != "ONE_TIME_APPLICATION_FRAME_BOUND":
        failures.append("frame_binding_status_wrong")
    if "future branches" not in frame_binding.get("not_bound_to", []):
        failures.append("frame_binding_missing_future_branch_exclusion")
    if component_binding.get("binding_status") != "SCHEMA_OVERLAY_COMPONENT_REFERENCES_BOUND":
        failures.append("component_binding_status_wrong")
    if component_binding.get("component_count") != 5:
        failures.append("component_binding_count_not_5")
    if component_binding.get("source_components_modified") is not False:
        failures.append("component_binding_source_components_modified")
    if non_reuse.get("boundary_status") != "NON_REUSE_BOUNDARY_REAFFIRMED_AFTER_APPLICATION":
        failures.append("non_reuse_boundary_status_wrong")
    for key in [
        "schema_overlay_applied_as_reusable_schema",
        "schema_overlay_preapproved",
        "validator_registry_entry_created",
        "future_automatic_use_allowed",
    ]:
        if non_reuse.get(key) is not False:
            failures.append(f"non_reuse_boundary_forbidden_true:{key}")
    if effects.get("positive_effects", {}).get("component_reference_binding_count") != 5:
        failures.append("effects_component_binding_count_not_5")
    for key, val in effects.get("zero_effects", {}).items():
        if val != 0:
            failures.append(f"effects_zero_counter_nonzero:{key}:{val}")
    if downstream.get("contract_status") != "DOWNSTREAM_CONTRACT_EMITTED_AFTER_ONE_TIME_SCHEMA_OVERLAY_APPLICATION":
        failures.append("downstream_contract_status_wrong")
    if "return to source-ref rebind review using explicit accepted overlay reference" not in downstream.get("allowed_next_uses", []):
        failures.append("downstream_contract_missing_rebind_review_return")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("classification_status_wrong")
    if roll.get("schema_overlay_applied_for_this_contract_count") != 1:
        failures.append("rollup_contract_application_count_not_1")
    if roll.get("schema_overlay_applied_globally_count") != 0:
        failures.append("rollup_global_application_nonzero")
    if roll.get("rebinds_applied_count") != 0:
        failures.append("rollup_rebinds_nonzero")
    if roll.get("metadata_populated_count") != 0:
        failures.append("rollup_metadata_nonzero")
    if profile.get("schema_overlay_applied_for_this_contract") is not True:
        failures.append("profile_contract_application_not_true")
    if profile.get("schema_overlay_applied_globally") is not False:
        failures.append("profile_global_application_true")
    return failures

def review_applied_reference() -> Tuple[Dict[str, Any], List[str]]:
    ref = read_json(SOURCE_APPLIED_REFERENCE_PATH)
    checks = {
        "reference_status_one_time": ref.get("reference_status") == "SCHEMA_OVERLAY_REFERENCE_APPLIED_ONE_TIME",
        "component_reference_count_5": len(ref.get("component_references", [])) == 5,
        "scope_this_contract_only": ref.get("scope") == "this_application_contract_only",
        "must_not_reuse_present": "future automatic schema reuse" in ref.get("must_not_be_used_for", []),
        "must_not_registry_present": "validator registry promotion" in ref.get("must_not_be_used_for", []),
        "must_not_rebind_without_review_present": "source-ref rebind without separate review" in ref.get("must_not_be_used_for", []),
        "must_not_metadata_present": "metadata population" in ref.get("must_not_be_used_for", []),
    }
    failures = [k for k, v in checks.items() if not v]
    return {
        "schema_version": "typed_machine_readable_schema_overlay_applied_reference_review_v0",
        "review_status": "APPLIED_REFERENCE_REVIEW_PASS" if not failures else "APPLIED_REFERENCE_REVIEW_FAIL",
        "checks": checks,
        "failures": failures,
    }, failures

def review_frame_binding() -> Tuple[Dict[str, Any], List[str]]:
    frame = read_json(SOURCE_FRAME_BINDING_PATH)
    checks = {
        "frame_bound": frame.get("binding_status") == "ONE_TIME_APPLICATION_FRAME_BOUND",
        "binding_scope_one_time": frame.get("binding_scope") == "one-time / this application contract / this receipt lineage",
        "not_bound_global_registry": "global schema registry" in frame.get("not_bound_to", []),
        "not_bound_validator_registry": "validator reusable-schema registry" in frame.get("not_bound_to", []),
        "not_bound_future_branches": "future branches" in frame.get("not_bound_to", []),
        "not_bound_future_automatic_application": "future automatic application" in frame.get("not_bound_to", []),
    }
    failures = [k for k, v in checks.items() if not v]
    return {
        "schema_version": "typed_machine_readable_schema_overlay_application_frame_binding_review_v0",
        "review_status": "FRAME_BINDING_REVIEW_PASS" if not failures else "FRAME_BINDING_REVIEW_FAIL",
        "checks": checks,
        "failures": failures,
    }, failures

def review_component_binding() -> Tuple[Dict[str, Any], List[str]]:
    comp = read_json(SOURCE_COMPONENT_BINDING_PATH)
    components = comp.get("components", [])
    checks = {
        "component_binding_status_bound": comp.get("binding_status") == "SCHEMA_OVERLAY_COMPONENT_REFERENCES_BOUND",
        "component_count_5": comp.get("component_count") == 5,
        "actual_component_count_5": len(components) == 5,
        "source_hashes_preserved": comp.get("source_hashes_preserved") is True,
        "source_components_not_modified": comp.get("source_components_modified") is False,
        "every_component_has_path": all(bool(c.get("source_path")) for c in components),
        "every_component_has_sha": all(bool(c.get("source_sha256")) for c in components),
        "every_component_applied_for_contract": all(c.get("applied_as_reference_for_this_contract") is True for c in components),
    }
    failures = [k for k, v in checks.items() if not v]
    return {
        "schema_version": "typed_machine_readable_schema_overlay_application_component_binding_review_v0",
        "review_status": "COMPONENT_BINDING_REVIEW_PASS" if not failures else "COMPONENT_BINDING_REVIEW_FAIL",
        "checks": checks,
        "failures": failures,
        "component_count": len(components),
    }, failures

def review_non_reuse_boundary() -> Tuple[Dict[str, Any], List[str]]:
    boundary = read_json(SOURCE_NON_REUSE_BOUNDARY_PATH)
    checks = {
        "boundary_reaffirmed": boundary.get("boundary_status") == "NON_REUSE_BOUNDARY_REAFFIRMED_AFTER_APPLICATION",
        "applied_for_contract": boundary.get("schema_overlay_applied_for_this_contract") is True,
        "not_reusable": boundary.get("schema_overlay_applied_as_reusable_schema") is False,
        "not_preapproved": boundary.get("schema_overlay_preapproved") is False,
        "no_validator_registry": boundary.get("validator_registry_entry_created") is False,
        "no_future_automatic_use": boundary.get("future_automatic_use_allowed") is False,
        "reuse_requires_future_explicit_authorization": boundary.get("reuse_requires_future_explicit_authorization") is True,
        "validator_cell_promotion_requires_future_explicit_authorization": boundary.get("validator_cell_promotion_requires_future_explicit_authorization") is True,
    }
    failures = [k for k, v in checks.items() if not v]
    return {
        "schema_version": "typed_machine_readable_schema_overlay_application_non_reuse_boundary_review_v0",
        "review_status": "NON_REUSE_BOUNDARY_REVIEW_PASS" if not failures else "NON_REUSE_BOUNDARY_REVIEW_FAIL",
        "checks": checks,
        "failures": failures,
    }, failures

def review_effects() -> Tuple[Dict[str, Any], List[str]]:
    effects = read_json(SOURCE_EFFECTS_TABLE_PATH)
    positive = effects.get("positive_effects", {})
    zero = effects.get("zero_effects", {})
    checks = {
        "positive_contract_application_1": positive.get("schema_overlay_applied_for_this_contract_count") == 1,
        "positive_reference_created_1": positive.get("applied_reference_created_count") == 1,
        "positive_component_binding_5": positive.get("component_reference_binding_count") == 5,
        "all_zero_effects_zero": all(v == 0 for v in zero.values()),
    }
    failures = [k for k, v in checks.items() if not v]
    return {
        "schema_version": "typed_machine_readable_schema_overlay_application_effects_review_v0",
        "review_status": "APPLICATION_EFFECTS_REVIEW_PASS" if not failures else "APPLICATION_EFFECTS_REVIEW_FAIL",
        "checks": checks,
        "failures": failures,
        "zero_effects": zero,
    }, failures

def review_downstream_contract() -> Tuple[Dict[str, Any], List[str]]:
    downstream = read_json(SOURCE_DOWNSTREAM_CONTRACT_PATH)
    allowed = set(downstream.get("allowed_next_uses", []))
    forbidden = set(downstream.get("not_authorized", []))
    checks = {
        "downstream_contract_status_ok": downstream.get("contract_status") == "DOWNSTREAM_CONTRACT_EMITTED_AFTER_ONE_TIME_SCHEMA_OVERLAY_APPLICATION",
        "allows_review_application_unit": "review accepted overlay application unit" in allowed,
        "allows_branch_only_schema_basis": "use accepted overlay reference as source-lineage / field-policy typing basis for this branch only" in allowed,
        "allows_return_to_rebind_review": "return to source-ref rebind review using explicit accepted overlay reference" in allowed,
        "forbids_future_automatic_reuse": "future automatic schema reuse" in forbidden,
        "forbids_validator_registry": "validator registry promotion" in forbidden,
        "forbids_source_ref_rebind_in_this_unit": "source-ref rebind in this unit" in forbidden,
        "forbids_metadata_population_in_this_unit": "metadata population in this unit" in forbidden,
        "forbids_value_extraction_in_this_unit": "value extraction in this unit" in forbidden,
    }
    failures = [k for k, v in checks.items() if not v]
    return {
        "schema_version": "typed_machine_readable_schema_overlay_application_downstream_contract_review_v0",
        "review_status": "DOWNSTREAM_CONTRACT_REVIEW_PASS" if not failures else "DOWNSTREAM_CONTRACT_REVIEW_FAIL",
        "checks": checks,
        "failures": failures,
    }, failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_basis()

    applied_review, applied_failures = review_applied_reference()
    frame_review, frame_failures = review_frame_binding()
    component_review, component_failures = review_component_binding()
    non_reuse_review, non_reuse_failures = review_non_reuse_boundary()
    effects_review, effects_failures = review_effects()
    downstream_review, downstream_failures = review_downstream_contract()

    review_failures = (
        applied_failures
        + frame_failures
        + component_failures
        + non_reuse_failures
        + effects_failures
        + downstream_failures
    )

    if failures:
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEW_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEW_BASIS_V0"
        downstream_ready = False
    elif review_failures:
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEWED_REPAIR_REQUIRED"
        reason_codes = [
            "SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEWED",
            "APPLICATION_UNIT_REVIEW_FAILURES_FOUND",
            "NO_DOWNSTREAM_USE_AUTHORIZED",
            "NO_REBINDS_APPLIED",
            "NO_METADATA_POPULATION",
        ] + review_failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_V0"
        downstream_ready = False
    else:
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEWED_DOWNSTREAM_USE_READY"
        reason_codes = [
            "SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEWED",
            "APPLIED_REFERENCE_REVIEW_PASS",
            "FRAME_BINDING_REVIEW_PASS",
            "COMPONENT_BINDING_REVIEW_PASS",
            "NON_REUSE_BOUNDARY_REVIEW_PASS",
            "APPLICATION_EFFECTS_REVIEW_PASS",
            "DOWNSTREAM_CONTRACT_REVIEW_PASS",
            "ACCEPTED_REFERENCE_READY_FOR_BRANCH_ONLY_DOWNSTREAM_USE",
            "REUSABLE_SCHEMA_NOT_AUTHORIZED",
            "PREAPPROVED_SCHEMA_NOT_AUTHORIZED",
            "VALIDATOR_REGISTRY_ENTRY_NOT_CREATED",
            "FUTURE_AUTOMATIC_USE_NOT_ALLOWED",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "REVIEW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_V0"
        downstream_ready = True

    rollup = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "application_unit_review_count": 1,
        "applied_reference_review_failure_count": len(applied_failures),
        "frame_binding_review_failure_count": len(frame_failures),
        "component_binding_review_failure_count": len(component_failures),
        "non_reuse_boundary_review_failure_count": len(non_reuse_failures),
        "effects_review_failure_count": len(effects_failures),
        "downstream_contract_review_failure_count": len(downstream_failures),
        "downstream_use_ready_count": 1 if downstream_ready else 0,
        "return_to_rebind_review_contract_emitted_count": 1 if downstream_ready else 0,
        "schema_overlay_applied_for_this_contract_count": 1,
        "schema_overlay_applied_as_reference_count": 1,
        "schema_overlay_applied_globally_count": 0,
        "component_reference_binding_count": 5,
        "one_time_acceptance_count": 1,
        "accepted_for_this_application_contract_count": 1,
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
        "schema_overlay_applied_globally_count",
        "reusable_schema_authorized_count",
        "preapproved_schema_authorized_count",
        "validator_registry_entry_created_count",
        "future_automatic_use_allowed_count",
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
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_review_profile_v0",
        "profile_id": "schema_overlay_application_unit_review_profile_" + sha8(rollup),
        "status": status,
        "application_unit_reviewed": True,
        "downstream_use_ready": downstream_ready,
        "return_to_rebind_review_contract_emitted": downstream_ready,
        "schema_overlay_applied_for_this_contract": True,
        "applied_as_reference_for_this_application_contract": True,
        "schema_overlay_applied_globally": False,
        "one_time_acceptance": True,
        "accepted_for_this_application_contract": True,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
        "typing_rule_applied": False,
        "field_policy_modified": False,
        "candidate_artifact_modified": False,
        "source_row_locator_applied": False,
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

    downstream_use_contract = {
        "schema_version": "typed_machine_readable_schema_overlay_accepted_reference_downstream_use_contract_v0",
        "contract_status": "ACCEPTED_REFERENCE_DOWNSTREAM_USE_READY" if downstream_ready else "ACCEPTED_REFERENCE_DOWNSTREAM_USE_NOT_READY",
        "accepted_reference_path": rel(SOURCE_APPLIED_REFERENCE_PATH),
        "allowed_downstream_use": [
            "use accepted overlay reference as source-lineage / field-policy typing basis for this branch only",
            "review source-ref rebind candidates against accepted overlay requirements",
            "emit rebind review/proposal surfaces only",
        ] if downstream_ready else [],
        "not_authorized": [
            "automatic source-ref rebind",
            "field-policy mutation",
            "candidate-artifact mutation",
            "value extraction",
            "metadata population",
            "discriminator readiness",
            "runtime patch",
            "C5",
            "schema reuse outside this application contract",
        ],
        "scope": "this receipt lineage only",
    }

    return_to_rebind_contract = {
        "schema_version": "typed_machine_readable_schema_overlay_return_to_rebind_review_contract_v0",
        "contract_status": "RETURN_TO_REBIND_REVIEW_READY" if downstream_ready else "RETURN_TO_REBIND_REVIEW_NOT_READY",
        "next_unit": "REVIEW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_V0" if downstream_ready else None,
        "accepted_schema_overlay_reference_path": rel(SOURCE_APPLIED_REFERENCE_PATH),
        "required_inputs": [
            "accepted schema overlay applied reference",
            "previous residual source-ref rebind candidates",
            "previous residual tie table",
            "source-lineage / field-policy schema overlay component bindings",
        ],
        "allowed_output": [
            "schema-aware rebind candidate review",
            "schema-aware tie classification",
            "proposal surface if unique lawful candidate emerges",
            "typed halt if ambiguity remains",
        ],
        "not_authorized": [
            "apply rebinds",
            "populate values",
            "populate metadata",
            "modify field policy",
            "modify candidate artifacts",
        ],
    }

    review_assessment = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_review_assessment_v0",
        "assessment_status": status,
        "source_application_unit_receipt_id": SOURCE_APP_UNIT_RECEIPT_ID,
        "review_failure_total": len(review_failures),
        "downstream_use_ready": downstream_ready,
        "return_to_rebind_review_contract_emitted": downstream_ready,
        "recommended_next": next_edge,
        "acceptance_boundary": "human_one_time_acceptance_for_this_application_contract",
    }

    decision_table = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_review_decision_table_v0",
        "decision_status": "APPLICATION_UNIT_REVIEW_DECISION_EMITTED",
        "records": [
            {
                "decision": "RETURN_TO_REBIND_REVIEW_WITH_ACCEPTED_SCHEMA_OVERLAY",
                "selected": downstream_ready,
                "next_unit": "REVIEW_MACHINE_READABLE_SOURCE_REF_REBIND_CANDIDATES_WITH_ACCEPTED_SCHEMA_OVERLAY_V0",
                "why": "accepted reference passed review and downstream use is limited to this branch",
            },
            {
                "decision": "REPAIR_APPLICATION_UNIT",
                "selected": not downstream_ready,
                "next_unit": "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_V0",
                "why": "use if reference, frame, component, non-reuse, effects, or downstream review fails",
            },
            {
                "decision": "PROMOTE_TO_REUSABLE_SCHEMA",
                "selected": False,
                "next_unit": None,
                "why": "explicitly not authorized",
            },
        ],
    }

    review_packet = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_review_result_packet_v0",
        "review_packet_status": "APPLICATION_UNIT_REVIEWED_DOWNSTREAM_USE_READY" if downstream_ready else "APPLICATION_UNIT_REVIEWED_REPAIR_REQUIRED",
        "summary": {
            "applied_reference_review_failures": applied_failures,
            "frame_binding_review_failures": frame_failures,
            "component_binding_review_failures": component_failures,
            "non_reuse_boundary_review_failures": non_reuse_failures,
            "effects_review_failures": effects_failures,
            "downstream_contract_review_failures": downstream_failures,
            "downstream_use_ready": downstream_ready,
        },
        "recommended_next": next_edge,
    }

    classification = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "application_unit_reviewed": True,
        "downstream_use_ready": downstream_ready,
        "return_to_rebind_review_contract_emitted": downstream_ready,
        "schema_overlay_applied_for_this_contract": True,
        "applied_as_reference_for_this_application_contract": True,
        "schema_overlay_applied_globally": False,
        "one_time_acceptance": True,
        "accepted_for_this_application_contract": True,
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
        "runtime_patch_authorized": False,
        "c5_authorized": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "acceptance_boundary": "human_one_time_acceptance_for_this_application_contract",
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_review_authority_boundary_v0",
        "status": status,
        "may_use_accepted_reference_downstream_after_review": downstream_ready,
        "may_review_rebind_candidates_against_accepted_overlay": downstream_ready,
        "may_apply_rebinds": False,
        "may_treat_schema_as_reusable": False,
        "may_treat_schema_as_preapproved": False,
        "may_create_validator_registry_entry": False,
        "may_allow_future_automatic_use": False,
        "may_apply_typing_rule": False,
        "may_modify_field_policy": False,
        "may_modify_candidate_artifacts": False,
        "may_authorize_values": False,
        "may_apply_values": False,
        "may_populate_metadata": False,
        "may_select_target_for_build": False,
        "may_apply_runtime_patch": False,
        "may_open_c5": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "acceptance_boundary": "human_one_time_acceptance_for_this_application_contract",
    }

    report = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The one-time schema overlay application unit was reviewed and its accepted reference is ready for branch-only downstream use. This does not authorize reusable schema status, rebind application, values, metadata, runtime patching, or C5.",
        "review_failure_total": len(review_failures),
        "downstream_use_ready_count": rollup["downstream_use_ready_count"],
        "return_to_rebind_review_contract_emitted_count": rollup["return_to_rebind_review_contract_emitted_count"],
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
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_application_unit",
                "question": "was one-time reference application recorded",
                "answer": "yes",
                "taken": "review applied reference and frame binding",
            },
            {
                "step": "review_non_reuse",
                "question": "did reusable/global/preapproved authority leak",
                "answer": "no",
                "taken": "preserve non-reuse boundary",
            },
            {
                "step": "review_downstream_contract",
                "question": "can accepted reference be used downstream in this branch",
                "answer": "yes" if downstream_ready else "no",
                "taken": next_edge,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(REVIEW_ASSESSMENT_PATH, review_assessment)
    write_json(APPLIED_REFERENCE_REVIEW_PATH, applied_review)
    write_json(FRAME_BINDING_REVIEW_PATH, frame_review)
    write_json(COMPONENT_BINDING_REVIEW_PATH, component_review)
    write_json(NON_REUSE_BOUNDARY_REVIEW_PATH, non_reuse_review)
    write_json(EFFECTS_REVIEW_PATH, effects_review)
    write_json(DOWNSTREAM_CONTRACT_REVIEW_PATH, downstream_review)
    write_json(DOWNSTREAM_USE_CONTRACT_PATH, downstream_use_contract)
    write_json(RETURN_TO_REBIND_CONTRACT_PATH, return_to_rebind_contract)
    write_json(REVIEW_DECISION_TABLE_PATH, decision_table)
    write_json(REVIEW_PACKET_PATH, review_packet)
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
        "APP_UNIT_REVIEW_0_SOURCE_RECEIPT_CONSUMED": SOURCE_APP_UNIT_RECEIPT_PATH.exists(),
        "APP_UNIT_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "APP_UNIT_REVIEW_2_APPLIED_REFERENCE_REVIEW_PASS": not applied_failures,
        "APP_UNIT_REVIEW_3_FRAME_BINDING_REVIEW_PASS": not frame_failures,
        "APP_UNIT_REVIEW_4_COMPONENT_BINDING_REVIEW_PASS": not component_failures,
        "APP_UNIT_REVIEW_5_NON_REUSE_BOUNDARY_REVIEW_PASS": not non_reuse_failures,
        "APP_UNIT_REVIEW_6_EFFECTS_REVIEW_PASS": not effects_failures,
        "APP_UNIT_REVIEW_7_DOWNSTREAM_CONTRACT_REVIEW_PASS": not downstream_failures,
        "APP_UNIT_REVIEW_8_DOWNSTREAM_USE_READY": downstream_ready,
        "APP_UNIT_REVIEW_9_RETURN_TO_REBIND_CONTRACT_EMITTED": RETURN_TO_REBIND_CONTRACT_PATH.exists(),
        "APP_UNIT_REVIEW_10_NO_GLOBAL_SCHEMA_APPLICATION": rollup["schema_overlay_applied_globally_count"] == 0,
        "APP_UNIT_REVIEW_11_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "APP_UNIT_REVIEW_12_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "APP_UNIT_REVIEW_13_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "APP_UNIT_REVIEW_14_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "APP_UNIT_REVIEW_15_NO_TYPING_RULE_APPLIED": rollup["typing_rule_applied_count"] == 0,
        "APP_UNIT_REVIEW_16_NO_FIELD_POLICY_MODIFIED": rollup["field_policy_modified_count"] == 0,
        "APP_UNIT_REVIEW_17_NO_CANDIDATE_ARTIFACT_MODIFIED": rollup["candidate_artifact_modified_count"] == 0,
        "APP_UNIT_REVIEW_18_NO_ROW_LOCATOR_APPLIED": rollup["source_row_locator_applied_count"] == 0,
        "APP_UNIT_REVIEW_19_NO_REBINDS_APPLIED": rollup["rebinds_applied_count"] == 0,
        "APP_UNIT_REVIEW_20_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "APP_UNIT_REVIEW_21_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "APP_UNIT_REVIEW_22_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "APP_UNIT_REVIEW_23_NO_DISCRIMINATOR_READY": rollup["ready_discriminator_count"] == 0,
        "APP_UNIT_REVIEW_24_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "APP_UNIT_REVIEW_25_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "APP_UNIT_REVIEW_26_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "APP_UNIT_REVIEW_27_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "APP_UNIT_REVIEW_28_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "APP_UNIT_REVIEW_29_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "APP_UNIT_REVIEW_30_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_one_time_acceptance_for_this_application_contract",
        "APP_UNIT_REVIEW_31_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "downstream_ready": downstream_ready,
        "review_failures": len(review_failures),
        "global": 0,
        "rebind": 0,
        "metadata": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_schema_overlay_application_unit_review_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SCHEMA_OVERLAY_APPLICATION_UNIT_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_application_unit_receipt_id": SOURCE_APP_UNIT_RECEIPT_ID,
        "machine_readable_schema_overlay_application_unit_review_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "application_unit_reviewed": True,
            "review_failure_total": len(review_failures),
            "downstream_use_ready": downstream_ready,
            "return_to_rebind_review_contract_emitted": downstream_ready,
            "schema_overlay_applied_for_this_contract": True,
            "applied_as_reference_for_this_application_contract": True,
            "schema_overlay_applied_globally": False,
            "component_reference_binding_count": 5,
            "one_time_acceptance": True,
            "accepted_for_this_application_contract": True,
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
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "applied_reference_review": rel(APPLIED_REFERENCE_REVIEW_PATH),
            "frame_binding_review": rel(FRAME_BINDING_REVIEW_PATH),
            "component_binding_review": rel(COMPONENT_BINDING_REVIEW_PATH),
            "non_reuse_boundary_review": rel(NON_REUSE_BOUNDARY_REVIEW_PATH),
            "effects_review": rel(EFFECTS_REVIEW_PATH),
            "downstream_contract_review": rel(DOWNSTREAM_CONTRACT_REVIEW_PATH),
            "downstream_use_contract": rel(DOWNSTREAM_USE_CONTRACT_PATH),
            "return_to_rebind_contract": rel(RETURN_TO_REBIND_CONTRACT_PATH),
            "review_decision_table": rel(REVIEW_DECISION_TABLE_PATH),
            "review_packet": rel(REVIEW_PACKET_PATH),
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
    print(f"schema_overlay_application_unit_review_receipt_id={receipt_id}")
    print(f"schema_overlay_application_unit_review_receipt_path={rel(receipt_path)}")
    print(f"schema_overlay_application_unit_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"schema_overlay_applied_reference_review_path={rel(APPLIED_REFERENCE_REVIEW_PATH)}")
    print(f"schema_overlay_application_frame_binding_review_path={rel(FRAME_BINDING_REVIEW_PATH)}")
    print(f"schema_overlay_application_component_binding_review_path={rel(COMPONENT_BINDING_REVIEW_PATH)}")
    print(f"schema_overlay_application_non_reuse_boundary_review_path={rel(NON_REUSE_BOUNDARY_REVIEW_PATH)}")
    print(f"schema_overlay_return_to_rebind_review_contract_path={rel(RETURN_TO_REBIND_CONTRACT_PATH)}")
    print(f"schema_overlay_application_unit_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"schema_overlay_application_unit_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
