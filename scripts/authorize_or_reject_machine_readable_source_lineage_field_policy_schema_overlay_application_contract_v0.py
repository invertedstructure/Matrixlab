#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "AUTHORIZE_OR_REJECT_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_AUTHORIZATION"
MODE = "HUMAN_AUTHORIZATION_RECORD / ONE_TIME_SCHEMA_ACCEPTANCE / NO_REUSABLE_SCHEMA / NO_SCHEMA_APPLICATION / NO_REBIND / NO_METADATA_FILL"
BUILD_MODE = "APPLICATION_CONTRACT_AUTHORIZATION_RECORD_ONLY"

SOURCE_APP_CONTRACT_REVIEW_RECEIPT_ID = "661f5061"
SOURCE_APP_CONTRACT_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0_receipts/661f5061.json"
SOURCE_APP_CONTRACT_REVIEW_ASSESSMENT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0/typed_machine_readable_schema_overlay_application_contract_review_assessment_v0.json"
SOURCE_APP_SCOPE_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0/typed_machine_readable_schema_overlay_application_scope_review_v0.json"
SOURCE_APP_FORBIDDEN_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0/typed_machine_readable_schema_overlay_application_forbidden_action_review_v0.json"
SOURCE_APP_PRECONDITION_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0/typed_machine_readable_schema_overlay_application_precondition_review_v0.json"
SOURCE_APP_AUTHORIZATION_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0/typed_machine_readable_schema_overlay_application_authorization_boundary_v0.json"
SOURCE_APP_UNIT_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0/typed_machine_readable_schema_overlay_application_unit_contract_v0.json"
SOURCE_APP_ACCEPTANCE_REQUEST_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0/typed_machine_readable_schema_overlay_application_acceptance_request_v0.json"
SOURCE_APP_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0/typed_machine_readable_schema_overlay_application_contract_review_decision_table_v0.json"
SOURCE_APP_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0/typed_machine_readable_schema_overlay_application_contract_review_packet_v0.json"
SOURCE_APP_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0/typed_machine_readable_schema_overlay_application_contract_review_classification_v0.json"
SOURCE_APP_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0/typed_machine_readable_schema_overlay_application_contract_review_authority_boundary_v0.json"
SOURCE_APP_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0/typed_machine_readable_schema_overlay_application_contract_review_rollup_v0.json"
SOURCE_APP_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_review_v0/typed_machine_readable_schema_overlay_application_contract_review_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_lineage_field_policy_schema_overlay_application_contract_authorization_v0_receipts"

AUTHORIZATION_RECORD_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_human_authorization_record_v0.json"
ONE_TIME_ACCEPTANCE_SCOPE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_one_time_acceptance_scope_v0.json"
NON_REUSE_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_non_reuse_boundary_v0.json"
ACCEPTED_APPLICATION_UNIT_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_accepted_application_unit_contract_v0.json"
AUTHORIZATION_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_authorization_decision_table_v0.json"
AUTHORIZATION_REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_authorization_review_packet_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_authorization_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_authorization_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_authorization_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_authorization_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_authorization_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_schema_overlay_application_contract_authorization_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_APP_CONTRACT_REVIEW_RECEIPT_PATH,
    SOURCE_APP_CONTRACT_REVIEW_ASSESSMENT_PATH,
    SOURCE_APP_SCOPE_REVIEW_PATH,
    SOURCE_APP_FORBIDDEN_REVIEW_PATH,
    SOURCE_APP_PRECONDITION_REVIEW_PATH,
    SOURCE_APP_AUTHORIZATION_BOUNDARY_PATH,
    SOURCE_APP_UNIT_CONTRACT_PATH,
    SOURCE_APP_ACCEPTANCE_REQUEST_PATH,
    SOURCE_APP_DECISION_TABLE_PATH,
    SOURCE_APP_REVIEW_PACKET_PATH,
    SOURCE_APP_CLASSIFICATION_PATH,
    SOURCE_APP_AUTHORITY_BOUNDARY_PATH,
    SOURCE_APP_ROLLUP_PATH,
    SOURCE_APP_PROFILE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEWED_ACCEPTANCE_REQUIRED"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_REVIEWED_ACCEPTANCE_REQUIRED"
EXPECTED_NEXT = "AUTHORIZE_OR_REJECT_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_V0"

HUMAN_DECISION = "ACCEPT_SCHEMA_OVERLAY_APPLICATION_CONTRACT_FOR_APPLICATION_UNIT"
HUMAN_DECISION_TEXT = "schema accepted for this application contract"
HUMAN_SCOPE_NOTE = "one-time acceptance only; not reusable, not preapproved, not validator-registry promoted"

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

    receipt = read_json(SOURCE_APP_CONTRACT_REVIEW_RECEIPT_PATH)
    summary = receipt.get("machine_readable_schema_overlay_application_contract_review_summary", {})
    acceptance_request = read_json(SOURCE_APP_ACCEPTANCE_REQUEST_PATH)
    app_unit_contract = read_json(SOURCE_APP_UNIT_CONTRACT_PATH)
    auth_boundary = read_json(SOURCE_APP_AUTHORIZATION_BOUNDARY_PATH)
    classif = read_json(SOURCE_APP_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_APP_ROLLUP_PATH)
    profile = read_json(SOURCE_APP_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_APP_CONTRACT_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_application_contract_review_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"source_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("application_contract_reviewed") is not True:
        failures.append("application_contract_not_reviewed")
    if summary.get("application_scope_failure_count") != 0:
        failures.append("application_scope_failures_nonzero")
    if summary.get("application_forbidden_action_failure_count") != 0:
        failures.append("application_forbidden_action_failures_nonzero")
    if summary.get("application_precondition_failure_count") != 0:
        failures.append("application_precondition_failures_nonzero")
    if summary.get("application_unit_contract_emitted") is not True:
        failures.append("application_unit_contract_not_emitted")
    if summary.get("application_acceptance_request_emitted") is not True:
        failures.append("acceptance_request_not_emitted")
    if summary.get("application_contract_accepted") is not False:
        failures.append("contract_already_accepted")
    if summary.get("schema_overlay_applied") is not False:
        failures.append("schema_overlay_already_applied")
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
        "ready_discriminator_count",
        "rule_refined",
        "tie_broken",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
    ]:
        val = summary.get(key)
        if key == "ready_discriminator_count":
            if val != 0:
                failures.append("ready_discriminator_nonzero")
        elif val is not False:
            failures.append(f"source_summary_forbidden_true:{key}")

    if acceptance_request.get("request_status") != "APPLICATION_CONTRACT_ACCEPTANCE_REQUIRED":
        failures.append("acceptance_request_status_wrong")
    if HUMAN_DECISION not in acceptance_request.get("allowed_responses", []):
        failures.append("human_acceptance_decision_not_allowed")
    if app_unit_contract.get("contract_status") != "APPLICATION_UNIT_CONTRACT_EMITTED_NOT_ACCEPTED":
        failures.append("application_unit_contract_status_wrong")
    if app_unit_contract.get("accepted_now") is not False:
        failures.append("app_unit_contract_already_accepted")
    if app_unit_contract.get("schema_overlay_applied_now") is not False:
        failures.append("app_unit_contract_claims_overlay_applied")
    if auth_boundary.get("boundary_status") != "APPLICATION_ACCEPTANCE_REQUIRED_NOT_GRANTED":
        failures.append("authorization_boundary_not_waiting_for_acceptance")
    if auth_boundary.get("accepted_now") is not False:
        failures.append("authorization_boundary_already_accepted")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("classification_status_wrong")
    if roll.get("application_contract_accepted_count") != 0:
        failures.append("rollup_contract_already_accepted")
    if roll.get("schema_overlay_applied_count") != 0:
        failures.append("rollup_overlay_applied_nonzero")
    if profile.get("application_contract_accepted") is not False:
        failures.append("profile_contract_already_accepted")
    if profile.get("schema_overlay_applied") is not False:
        failures.append("profile_overlay_already_applied")

    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_basis()

    app_unit_contract = read_json(SOURCE_APP_UNIT_CONTRACT_PATH)
    acceptance_request = read_json(SOURCE_APP_ACCEPTANCE_REQUEST_PATH)

    if failures:
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_AUTHORIZATION_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_AUTHORIZATION_BASIS_V0"
        accepted = False
    else:
        status = "TYPED_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_ACCEPTED_ONE_TIME_APPLICATION_UNIT_AUTHORIZED"
        reason_codes = [
            "HUMAN_APPLICATION_CONTRACT_DECISION_RECORDED",
            "APPLICATION_CONTRACT_ACCEPTED_FOR_THIS_APPLICATION_CONTRACT_ONLY",
            "ONE_TIME_SCHEMA_ACCEPTANCE_RECORDED",
            "APPLICATION_UNIT_CONTRACT_AUTHORIZED_FOR_LATER_BOUNDED_UNIT",
            "REUSABLE_SCHEMA_NOT_AUTHORIZED",
            "PREAPPROVED_SCHEMA_NOT_AUTHORIZED",
            "VALIDATOR_REGISTRY_ENTRY_NOT_CREATED",
            "FUTURE_AUTOMATIC_USE_NOT_ALLOWED",
            "NO_SCHEMA_OVERLAY_APPLIED",
            "NO_TYPING_RULE_APPLIED",
            "NO_FIELD_POLICY_MODIFIED",
            "NO_CANDIDATE_ARTIFACT_MODIFIED",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_V0"
        accepted = True

    authorization_record = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_human_authorization_record_v0",
        "authorization_status": "ACCEPTED_ONE_TIME_FOR_THIS_APPLICATION_CONTRACT" if accepted else "AUTHORIZATION_BASIS_FAIL",
        "source_application_contract_review_receipt_id": SOURCE_APP_CONTRACT_REVIEW_RECEIPT_ID,
        "human_decision": HUMAN_DECISION if accepted else None,
        "human_decision_text": HUMAN_DECISION_TEXT if accepted else None,
        "human_scope_note": HUMAN_SCOPE_NOTE if accepted else None,
        "accepted_for_this_application_contract": accepted,
        "application_contract_accepted": accepted,
        "application_unit_authorized_for_later_bounded_unit": accepted,
        "one_time_acceptance": accepted,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
        "schema_overlay_applied_now": False,
        "created_at": now_iso(),
    }

    one_time_scope = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_one_time_acceptance_scope_v0",
        "scope_status": "ONE_TIME_ACCEPTANCE_SCOPE_RECORDED" if accepted else "ONE_TIME_ACCEPTANCE_SCOPE_NOT_RECORDED",
        "accepted_for_this_application_contract": accepted,
        "bounded_frame": {
            "source_application_contract_review_receipt_id": SOURCE_APP_CONTRACT_REVIEW_RECEIPT_ID,
            "source_application_unit_contract_path": rel(SOURCE_APP_UNIT_CONTRACT_PATH),
            "source_acceptance_request_path": rel(SOURCE_APP_ACCEPTANCE_REQUEST_PATH),
        },
        "authorized_later_unit": "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_V0" if accepted else None,
        "authorized_application_scope": app_unit_contract.get("application_scope", []) if accepted else [],
        "still_forbidden": [
            "source-ref rebind",
            "value extraction",
            "metadata population",
            "discriminator readiness",
            "runtime patch",
            "target selection",
            "C5 opening",
            "future automatic schema reuse",
            "validator registry promotion",
        ],
        "schema_overlay_applied_now": False,
    }

    non_reuse_boundary = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_non_reuse_boundary_v0",
        "boundary_status": "NON_REUSE_BOUNDARY_EXPLICIT",
        "schema_accepted_for_this_application_contract": accepted,
        "schema_reusable": False,
        "schema_preapproved": False,
        "schema_promoted_to_validator_registry": False,
        "future_automatic_use_allowed": False,
        "reuse_requires_future_explicit_authorization": True,
        "future_validator_cell_may_promote_only_if_explicitly_authorized": True,
        "notes": [
            "one-time acceptance does not create reusable schema authority",
            "one-time acceptance does not create preapproved validator-cell rule",
            "one-time acceptance does not allow future branches to import this schema automatically",
        ],
    }

    accepted_app_unit_contract = {
        "schema_version": "typed_machine_readable_schema_overlay_accepted_application_unit_contract_v0",
        "contract_status": "APPLICATION_UNIT_CONTRACT_ACCEPTED_FOR_LATER_BOUNDED_UNIT" if accepted else "APPLICATION_UNIT_CONTRACT_NOT_ACCEPTED",
        "source_application_unit_contract_path": rel(SOURCE_APP_UNIT_CONTRACT_PATH),
        "accepted_for_this_application_contract": accepted,
        "accepted_now_for_later_application_unit": accepted,
        "schema_overlay_applied_now": False,
        "application_scope": app_unit_contract.get("application_scope", []) if accepted else [],
        "application_forbidden_actions": app_unit_contract.get("application_forbidden_actions", []) + [
            "future automatic schema reuse",
            "preapproved schema treatment",
            "validator registry promotion without explicit future authorization",
        ],
        "application_required_preconditions": [
            "this one-time acceptance receipt",
            "separate bounded application unit",
            "zero forbidden-action counters",
        ],
        "next_lawful_unit": next_edge if accepted else None,
    }

    authorization_decision_table = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_authorization_decision_table_v0",
        "decision_status": "APPLICATION_CONTRACT_AUTHORIZATION_DECISION_RECORDED",
        "records": [
            {
                "decision": "ACCEPT_ONE_TIME_FOR_THIS_APPLICATION_CONTRACT",
                "selected": accepted,
                "next_unit": "BUILD_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_UNIT_V0",
                "why": "human accepted the schema for this application contract only",
            },
            {
                "decision": "REJECT_APPLICATION_CONTRACT",
                "selected": False,
                "next_unit": "FREEZE_OR_REPAIR_MACHINE_READABLE_SOURCE_LINEAGE_FIELD_POLICY_SCHEMA_OVERLAY_APPLICATION_CONTRACT_V0",
                "why": "not selected",
            },
            {
                "decision": "PROMOTE_TO_REUSABLE_SCHEMA",
                "selected": False,
                "next_unit": None,
                "why": "explicitly forbidden in this frame; future validator-cell or human-governance layer required",
            },
        ],
    }

    authorization_review_packet = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_authorization_review_packet_v0",
        "review_packet_status": "ONE_TIME_ACCEPTANCE_RECORDED_NEXT_APPLICATION_UNIT_ALLOWED" if accepted else "AUTHORIZATION_NOT_RECORDED",
        "summary": {
            "application_contract_accepted": accepted,
            "accepted_for_this_application_contract": accepted,
            "one_time_acceptance": accepted,
            "application_unit_contract_authorized": accepted,
            "reusable_schema_authorized": False,
            "preapproved_schema_authorized": False,
            "validator_registry_entry_created": False,
            "future_automatic_use_allowed": False,
            "schema_overlay_applied": False,
        },
        "recommended_next": next_edge,
    }

    classification = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_authorization_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "application_contract_authorization_reviewed": True,
        "application_contract_accepted": accepted,
        "accepted_for_this_application_contract": accepted,
        "one_time_acceptance": accepted,
        "application_unit_contract_authorized": accepted,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
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
        "acceptance_boundary": "human_one_time_acceptance_for_this_application_contract",
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_authorization_authority_boundary_v0",
        "status": status,
        "may_record_human_one_time_acceptance": True,
        "may_authorize_later_bounded_application_unit": accepted,
        "may_apply_schema_overlay_now": False,
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
        "may_accept_null_reasons_as_final": False,
        "may_materialize_source_packet_for_review": False,
        "may_populate_metadata": False,
        "may_evaluate_discriminators": False,
        "may_refine_dominance_rule": False,
        "may_break_tie": False,
        "may_select_target_for_build": False,
        "may_apply_runtime_patch": False,
        "may_open_c5": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "acceptance_boundary": "human_one_time_acceptance_for_this_application_contract",
    }

    rollup = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_authorization_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "application_contract_authorization_count": 1,
        "application_contract_accepted_count": 1 if accepted else 0,
        "accepted_for_this_application_contract_count": 1 if accepted else 0,
        "one_time_acceptance_count": 1 if accepted else 0,
        "application_unit_contract_authorized_count": 1 if accepted else 0,
        "reusable_schema_authorized_count": 0,
        "preapproved_schema_authorized_count": 0,
        "validator_registry_entry_created_count": 0,
        "future_automatic_use_allowed_count": 0,
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

    zero_keys = [
        "reusable_schema_authorized_count",
        "preapproved_schema_authorized_count",
        "validator_registry_entry_created_count",
        "future_automatic_use_allowed_count",
        "schema_overlay_applied_count",
        "typing_rule_applied_count",
        "field_policy_modified_count",
        "candidate_artifact_modified_count",
        "source_row_locator_applied_count",
        "rebinds_applied_count",
        "dominance_rule_applied_count",
        "values_authorized_count",
        "values_applied_count",
        "null_reason_accepted_count",
        "source_packet_materialized_for_review_count",
        "metadata_populated_count",
        "ready_discriminator_count",
        "rule_refined_count",
        "tie_broken_count",
        "target_selected_for_build_count",
        "runtime_patch_applied_count",
        "c5_opened_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_authorization_profile_v0",
        "profile_id": "schema_overlay_application_contract_authorization_profile_" + sha8(rollup),
        "status": status,
        "application_contract_accepted": accepted,
        "accepted_for_this_application_contract": accepted,
        "one_time_acceptance": accepted,
        "application_unit_contract_authorized": accepted,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
        "schema_overlay_applied": False,
        "typing_rule_applied": False,
        "field_policy_modified": False,
        "candidate_artifact_modified": False,
        "source_row_locator_applied": False,
        "rebinds_applied": False,
        "values_authorized": False,
        "values_applied": False,
        "source_packet_materialized_for_review": False,
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
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_authorization_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Human accepted this schema-overlay application contract for one bounded application frame only. This does not create reusable, preapproved, validator-registry, or future automatic schema authority.",
        "application_contract_accepted_count": rollup["application_contract_accepted_count"],
        "one_time_acceptance_count": rollup["one_time_acceptance_count"],
        "application_unit_contract_authorized_count": rollup["application_unit_contract_authorized_count"],
        "reusable_schema_authorized_count": 0,
        "preapproved_schema_authorized_count": 0,
        "validator_registry_entry_created_count": 0,
        "future_automatic_use_allowed_count": 0,
        "schema_overlay_applied_count": 0,
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_one_time_acceptance_for_this_application_contract",
    }

    trace = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_authorization_transition_trace_v0",
        "trace": [
            {
                "step": "human_decision_received",
                "question": "accept, reject, repair, or freeze application contract",
                "answer": HUMAN_DECISION_TEXT,
                "taken": "record one-time acceptance",
            },
            {
                "step": "non_reuse_boundary_recorded",
                "question": "does acceptance create reusable or preapproved schema authority",
                "answer": "no",
                "taken": "emit explicit non-reuse boundary",
            },
            {
                "step": "classify_authorization",
                "question": "what is the next lawful object",
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

    write_json(AUTHORIZATION_RECORD_PATH, authorization_record)
    write_json(ONE_TIME_ACCEPTANCE_SCOPE_PATH, one_time_scope)
    write_json(NON_REUSE_BOUNDARY_PATH, non_reuse_boundary)
    write_json(ACCEPTED_APPLICATION_UNIT_CONTRACT_PATH, accepted_app_unit_contract)
    write_json(AUTHORIZATION_DECISION_TABLE_PATH, authorization_decision_table)
    write_json(AUTHORIZATION_REVIEW_PACKET_PATH, authorization_review_packet)
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
        "AUTHORIZATION_0_SOURCE_RECEIPT_CONSUMED": SOURCE_APP_CONTRACT_REVIEW_RECEIPT_PATH.exists(),
        "AUTHORIZATION_1_HUMAN_DECISION_RECORDED": accepted,
        "AUTHORIZATION_2_ONE_TIME_ACCEPTANCE_RECORDED": rollup["one_time_acceptance_count"] == 1,
        "AUTHORIZATION_3_APPLICATION_UNIT_CONTRACT_AUTHORIZED": rollup["application_unit_contract_authorized_count"] == 1,
        "AUTHORIZATION_4_NON_REUSE_BOUNDARY_EMITTED": NON_REUSE_BOUNDARY_PATH.exists(),
        "AUTHORIZATION_5_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "AUTHORIZATION_6_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "AUTHORIZATION_7_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "AUTHORIZATION_8_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "AUTHORIZATION_9_NO_SCHEMA_OVERLAY_APPLIED": rollup["schema_overlay_applied_count"] == 0,
        "AUTHORIZATION_10_NO_TYPING_RULE_APPLIED": rollup["typing_rule_applied_count"] == 0,
        "AUTHORIZATION_11_NO_FIELD_POLICY_MODIFIED": rollup["field_policy_modified_count"] == 0,
        "AUTHORIZATION_12_NO_CANDIDATE_ARTIFACT_MODIFIED": rollup["candidate_artifact_modified_count"] == 0,
        "AUTHORIZATION_13_NO_ROW_LOCATOR_APPLIED": rollup["source_row_locator_applied_count"] == 0,
        "AUTHORIZATION_14_NO_REBINDS_APPLIED": rollup["rebinds_applied_count"] == 0,
        "AUTHORIZATION_15_NO_DOMINANCE_RULE_APPLIED": rollup["dominance_rule_applied_count"] == 0,
        "AUTHORIZATION_16_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "AUTHORIZATION_17_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "AUTHORIZATION_18_NO_NULL_REASONS_ACCEPTED": rollup["null_reason_accepted_count"] == 0,
        "AUTHORIZATION_19_NO_SOURCE_PACKET_MATERIALIZED": rollup["source_packet_materialized_for_review_count"] == 0,
        "AUTHORIZATION_20_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "AUTHORIZATION_21_NO_DISCRIMINATOR_READY": rollup["ready_discriminator_count"] == 0,
        "AUTHORIZATION_22_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "AUTHORIZATION_23_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "AUTHORIZATION_24_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "AUTHORIZATION_25_NO_GENERAL_CELL1_AUTHORITY": rollup["general_cell1_authority_granted_count"] == 0,
        "AUTHORIZATION_26_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "AUTHORIZATION_27_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "AUTHORIZATION_28_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "AUTHORIZATION_29_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_one_time_acceptance_for_this_application_contract",
        "AUTHORIZATION_30_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SCHEMA_OVERLAY_APPLICATION_CONTRACT_AUTHORIZATION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "accepted": accepted,
        "one_time": rollup["one_time_acceptance_count"],
        "reusable": 0,
        "applied": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_schema_overlay_application_contract_authorization_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SCHEMA_OVERLAY_APPLICATION_CONTRACT_AUTHORIZATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_application_contract_review_receipt_id": SOURCE_APP_CONTRACT_REVIEW_RECEIPT_ID,
        "machine_readable_schema_overlay_application_contract_authorization_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "human_decision": HUMAN_DECISION if accepted else None,
            "application_contract_accepted": accepted,
            "accepted_for_this_application_contract": accepted,
            "one_time_acceptance": accepted,
            "application_unit_contract_authorized": accepted,
            "reusable_schema_authorized": False,
            "preapproved_schema_authorized": False,
            "validator_registry_entry_created": False,
            "future_automatic_use_allowed": False,
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
            "authorization_record": rel(AUTHORIZATION_RECORD_PATH),
            "one_time_acceptance_scope": rel(ONE_TIME_ACCEPTANCE_SCOPE_PATH),
            "non_reuse_boundary": rel(NON_REUSE_BOUNDARY_PATH),
            "accepted_application_unit_contract": rel(ACCEPTED_APPLICATION_UNIT_CONTRACT_PATH),
            "authorization_decision_table": rel(AUTHORIZATION_DECISION_TABLE_PATH),
            "authorization_review_packet": rel(AUTHORIZATION_REVIEW_PACKET_PATH),
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
    print(f"schema_overlay_application_contract_authorization_receipt_id={receipt_id}")
    print(f"schema_overlay_application_contract_authorization_receipt_path={rel(receipt_path)}")
    print(f"schema_overlay_application_contract_human_authorization_record_path={rel(AUTHORIZATION_RECORD_PATH)}")
    print(f"schema_overlay_application_contract_one_time_acceptance_scope_path={rel(ONE_TIME_ACCEPTANCE_SCOPE_PATH)}")
    print(f"schema_overlay_application_contract_non_reuse_boundary_path={rel(NON_REUSE_BOUNDARY_PATH)}")
    print(f"schema_overlay_accepted_application_unit_contract_path={rel(ACCEPTED_APPLICATION_UNIT_CONTRACT_PATH)}")
    print(f"schema_overlay_application_contract_authorization_rollup_path={rel(ROLLUP_PATH)}")
    print(f"schema_overlay_application_contract_authorization_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
