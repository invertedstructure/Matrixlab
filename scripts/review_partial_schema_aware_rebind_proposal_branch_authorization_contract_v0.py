#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_REVIEW"
MODE = "AUTHORIZATION_CONTRACT_REVIEW / DECISION_REQUIRED / NO_AUTHORIZATION_GRANTED / NO_REBIND_APPLICATION"
BUILD_MODE = "PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_REVIEW_ONLY"

SOURCE_AUTH_CONTRACT_RECEIPT_ID = "56454d20"
SOURCE_AUTH_CONTRACT_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0_receipts/56454d20.json"
SOURCE_AUTH_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0.json"
SOURCE_AUTH_SCOPE_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_scope_table_v0.json"
SOURCE_AUTH_PRECONDITION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_precondition_table_v0.json"
SOURCE_AUTH_FORBIDDEN_ACTION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_forbidden_action_table_v0.json"
SOURCE_AUTH_HOLD_RELEASE_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_release_contract_v0.json"
SOURCE_AUTH_RESIDUAL_BRANCH_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_residual_branch_contract_v0.json"
SOURCE_AUTH_DECISION_REQUEST_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_decision_request_v0.json"
SOURCE_AUTH_NONAPPLICATION_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_nonapplication_boundary_v0.json"
SOURCE_AUTH_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_packet_v0.json"
SOURCE_AUTH_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_downstream_decision_table_v0.json"
SOURCE_AUTH_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_classification_v0.json"
SOURCE_AUTH_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_authority_boundary_v0.json"
SOURCE_AUTH_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_rollup_v0.json"
SOURCE_AUTH_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_assessment_v0.json"
CONTRACT_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0.json"
SCOPE_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_scope_review_v0.json"
PRECONDITION_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_precondition_review_v0.json"
FORBIDDEN_ACTION_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_forbidden_action_review_v0.json"
HOLD_RELEASE_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_release_review_v0.json"
RESIDUAL_BRANCH_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_residual_branch_review_v0.json"
DECISION_REQUEST_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_decision_request_review_v0.json"
NONAPPLICATION_BOUNDARY_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_nonapplication_boundary_review_v0.json"
DECISION_SURFACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_decision_surface_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_downstream_decision_table_v0.json"
REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_packet_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_AUTH_CONTRACT_RECEIPT_PATH,
    SOURCE_AUTH_CONTRACT_PATH,
    SOURCE_AUTH_SCOPE_TABLE_PATH,
    SOURCE_AUTH_PRECONDITION_TABLE_PATH,
    SOURCE_AUTH_FORBIDDEN_ACTION_TABLE_PATH,
    SOURCE_AUTH_HOLD_RELEASE_CONTRACT_PATH,
    SOURCE_AUTH_RESIDUAL_BRANCH_CONTRACT_PATH,
    SOURCE_AUTH_DECISION_REQUEST_PATH,
    SOURCE_AUTH_NONAPPLICATION_BOUNDARY_PATH,
    SOURCE_AUTH_REVIEW_PACKET_PATH,
    SOURCE_AUTH_DECISION_TABLE_PATH,
    SOURCE_AUTH_CLASSIFICATION_PATH,
    SOURCE_AUTH_AUTHORITY_BOUNDARY_PATH,
    SOURCE_AUTH_ROLLUP_PATH,
    SOURCE_AUTH_PROFILE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_BUILT_REVIEW_REQUIRED"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_BUILT_REVIEW_REQUIRED"
EXPECTED_SOURCE_NEXT = "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_V0"

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

def rows(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    v = obj.get("records")
    return v if isinstance(v, list) else []

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(SOURCE_AUTH_CONTRACT_RECEIPT_PATH)
    summary = receipt.get("machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_summary", {})
    contract = read_json(SOURCE_AUTH_CONTRACT_PATH)
    scope = read_json(SOURCE_AUTH_SCOPE_TABLE_PATH)
    preconditions = read_json(SOURCE_AUTH_PRECONDITION_TABLE_PATH)
    forbidden = read_json(SOURCE_AUTH_FORBIDDEN_ACTION_TABLE_PATH)
    hold = read_json(SOURCE_AUTH_HOLD_RELEASE_CONTRACT_PATH)
    residual = read_json(SOURCE_AUTH_RESIDUAL_BRANCH_CONTRACT_PATH)
    decision_request = read_json(SOURCE_AUTH_DECISION_REQUEST_PATH)
    nonapp = read_json(SOURCE_AUTH_NONAPPLICATION_BOUNDARY_PATH)
    review_packet = read_json(SOURCE_AUTH_REVIEW_PACKET_PATH)
    downstream = read_json(SOURCE_AUTH_DECISION_TABLE_PATH)
    classification = read_json(SOURCE_AUTH_CLASSIFICATION_PATH)
    authority = read_json(SOURCE_AUTH_AUTHORITY_BOUNDARY_PATH)
    rollup = read_json(SOURCE_AUTH_ROLLUP_PATH)
    profile = read_json(SOURCE_AUTH_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_AUTH_CONTRACT_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_authorization_contract_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_terminal_not_expected")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "authorization_contract_built",
        "authorization_contract_review_required",
        "authorization_scope_emitted",
        "authorization_preconditions_emitted",
        "authorization_forbidden_actions_emitted",
        "hold_release_contract_emitted",
        "residual_branch_contract_emitted",
        "decision_request_emitted",
        "schema_overlay_applied_for_this_contract",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "proposal_binding_count": 4,
        "ambiguity_binding_count_preserved": 22,
        "requirement_gap_binding_count_preserved": 498,
        "ready_discriminator_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    for key in [
        "authorization_granted",
        "proposal_hold_released",
        "rebind_application_authorized",
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
        "null_reasons_accepted",
        "source_packet_materialized_for_review",
        "metadata_populated",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if summary.get(key) is not False:
            failures.append(f"summary_forbidden_true:{key}")

    if contract.get("contract_status") != "AUTHORIZATION_CONTRACT_BUILT_REVIEW_REQUIRED":
        failures.append("contract_status_wrong")
    if contract.get("proposal_binding_count") != 4:
        failures.append("contract_proposal_count_wrong")
    for key in ["authorization_granted", "proposal_hold_release_authorized", "rebind_application_authorized", "future_automatic_use_allowed", "reusable_schema_authorized", "preapproved_schema_authorized", "validator_registry_entry_created"]:
        if contract.get(key) is not False:
            failures.append(f"contract_forbidden_true:{key}")

    scope_records = rows(scope)
    if len(scope_records) != 3:
        failures.append("scope_table_record_count_not_3")
    included = [r for r in scope_records if r.get("included") is True]
    if len(included) != 1 or included[0].get("count") != 4:
        failures.append("scope_table_included_scope_wrong")
    excluded_total = sum(int(r.get("count", 0)) for r in scope_records if r.get("included") is False)
    if excluded_total != 520:
        failures.append(f"scope_table_excluded_total_wrong:{excluded_total}")

    precondition_records = rows(preconditions)
    required_unsatisfied = {
        "authorization_contract_review_pass",
        "explicit_human_or_validator_apply_decision_recorded",
        "proposal_hold_release_authorized",
    }
    observed_unsatisfied = {r.get("precondition") for r in precondition_records if r.get("satisfied") is False}
    if not required_unsatisfied.issubset(observed_unsatisfied):
        failures.append("precondition_table_missing_required_unsatisfied_entries")
    if preconditions.get("authorization_ready_now") is not False or preconditions.get("application_ready_now") is not False:
        failures.append("precondition_table_ready_now_true")

    forbidden_actions = forbidden.get("forbidden_actions", [])
    for action in [
        "grant authorization in the contract-build unit",
        "release proposal hold",
        "apply proposal rebinds",
        "authorize values",
        "apply values",
        "populate metadata",
        "apply runtime patch",
        "open C5",
        "promote schema to reusable",
        "treat schema as preapproved",
        "create validator registry entry",
        "allow future automatic use",
        "use latest-file guessing",
        "use mtime selection",
    ]:
        if action not in forbidden_actions:
            failures.append(f"forbidden_action_missing:{action}")

    if hold.get("hold_release_status") != "HOLD_RELEASE_CONDITIONS_EMITTED_NOT_SATISFIED":
        failures.append("hold_release_status_wrong")
    if hold.get("proposal_hold_released") is not False or hold.get("release_authorized_now") is not False:
        failures.append("hold_release_flags_wrong")

    if residual.get("residual_branch_status") != "RESIDUAL_BRANCHES_MUST_REMAIN_PRESERVED":
        failures.append("residual_status_wrong")
    if residual.get("ambiguity_binding_count_preserved") != 22 or residual.get("requirement_gap_binding_count_preserved") != 498:
        failures.append("residual_counts_wrong")
    for key in ["may_discard_residual_branches", "may_collapse_residual_branches_into_null", "may_authorize_residual_branches_here"]:
        if residual.get(key) is not False:
            failures.append(f"residual_forbidden_true:{key}")

    if decision_request.get("decision_request_status") != "HUMAN_OR_VALIDATOR_DECISION_REQUIRED_LATER":
        failures.append("decision_request_status_wrong")
    if decision_request.get("decision_requested_now") is not False or decision_request.get("authorization_granted") is not False:
        failures.append("decision_request_flags_wrong")
    if len(decision_request.get("valid_decisions", [])) != 3:
        failures.append("decision_request_valid_decision_count_wrong")

    for key in [
        "authorization_granted",
        "proposal_hold_released",
        "rebinds_applied",
        "values_authorized",
        "values_applied",
        "metadata_populated",
        "target_selected_for_build",
        "runtime_patch_applied",
        "c5_opened",
    ]:
        if nonapp.get(key) is not False:
            failures.append(f"nonapplication_boundary_true:{key}")

    if review_packet.get("review_packet_status") != EXPECTED_SOURCE_STATUS:
        failures.append("review_packet_status_wrong")
    if classification.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("classification_status_wrong")
    if classification.get("authorization_granted") is not False or classification.get("next_command_goal") is not None:
        failures.append("classification_bad_authorization_or_hidden_next")
    if authority.get("may_review_authorization_contract_next") is not True:
        failures.append("authority_cannot_review_contract")
    for key in [
        "may_grant_authorization_now",
        "may_release_proposal_hold",
        "may_apply_rebinds",
        "may_apply_values",
        "may_populate_metadata",
        "may_select_target_for_build",
        "may_apply_runtime_patch",
        "may_open_c5",
        "may_treat_schema_as_reusable",
        "may_treat_schema_as_preapproved",
        "may_create_validator_registry_entry",
        "may_allow_future_automatic_use",
    ]:
        if authority.get(key) is not False:
            failures.append(f"authority_forbidden_true:{key}")

    if rollup.get("authorization_contract_built_count") != 1:
        failures.append("rollup_contract_built_count_wrong")
    for key in [
        "authorization_granted_count",
        "proposal_hold_released_count",
        "rebind_application_authorized_count",
        "rebinds_applied_count",
        "values_authorized_count",
        "values_applied_count",
        "metadata_populated_count",
        "target_selected_for_build_count",
        "runtime_patch_applied_count",
        "c5_opened_count",
        "reusable_schema_authorized_count",
        "preapproved_schema_authorized_count",
        "validator_registry_entry_created_count",
        "future_automatic_use_allowed_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]:
        if rollup.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup.get(key)}")
    if profile.get("authorization_contract_built") is not True or profile.get("authorization_contract_review_required") is not True:
        failures.append("profile_contract_not_review_required")
    for key in ["authorization_granted", "proposal_hold_released", "rebind_application_authorized", "rebinds_applied", "metadata_populated", "runtime_patch_applied", "c5_opened"]:
        if profile.get(key) is not False:
            failures.append(f"profile_forbidden_true:{key}")

    return failures, {
        "summary": summary,
        "contract": contract,
        "scope": scope,
        "preconditions": preconditions,
        "forbidden": forbidden,
        "hold": hold,
        "residual": residual,
        "decision_request": decision_request,
        "nonapp": nonapp,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    summary = src.get("summary", {})
    proposal_binding_count = int(summary.get("proposal_binding_count", 0) or 0)
    ambiguity_binding_count = int(summary.get("ambiguity_binding_count_preserved", 0) or 0)
    requirement_gap_binding_count = int(summary.get("requirement_gap_binding_count_preserved", 0) or 0)

    if failures:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_REVIEW_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_REVIEW_BASIS_V0"
        review_pass = False
    else:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_REVIEWED_DECISION_REQUIRED"
        reason_codes = [
            "AUTHORIZATION_CONTRACT_REVIEW_COMPLETE",
            "AUTHORIZATION_CONTRACT_REVIEW_PASS",
            "AUTHORIZATION_SCOPE_REVIEW_PASS",
            "AUTHORIZATION_PRECONDITIONS_REVIEW_PASS",
            "AUTHORIZATION_FORBIDDEN_ACTIONS_REVIEW_PASS",
            "HOLD_RELEASE_CONTRACT_REVIEW_PASS",
            "RESIDUAL_BRANCH_PRESERVATION_REVIEW_PASS",
            "DECISION_REQUEST_REVIEW_PASS",
            "NONAPPLICATION_BOUNDARY_REVIEW_PASS",
            "HUMAN_OR_VALIDATOR_DECISION_REQUIRED",
            "NO_AUTHORIZATION_GRANTED",
            "NO_PROPOSAL_HOLD_RELEASED",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "REQUEST_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_APPLICATION_DECISION_V0"
        review_pass = True

    review_assessment = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_assessment_v0",
        "assessment_status": status,
        "source_authorization_contract_receipt_id": SOURCE_AUTH_CONTRACT_RECEIPT_ID,
        "authorization_contract_review_pass": review_pass,
        "human_or_validator_decision_required": review_pass,
        "proposal_binding_count": proposal_binding_count,
        "authorization_granted": False,
        "proposal_hold_released": False,
        "rebinds_applied": False,
        "recommended_next": next_edge,
    }

    contract_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0",
        "review_status": "AUTHORIZATION_CONTRACT_REVIEW_PASS" if review_pass else "AUTHORIZATION_CONTRACT_REVIEW_REPAIR_REQUIRED",
        "proposal_binding_count": proposal_binding_count,
        "contract_scope_is_one_time": True,
        "authorization_granted": False,
        "proposal_hold_release_authorized": False,
        "rebind_application_authorized": False,
        "future_automatic_use_allowed": False,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
    }

    scope_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_scope_review_v0",
        "review_status": "AUTHORIZATION_SCOPE_REVIEW_PASS" if review_pass else "AUTHORIZATION_SCOPE_REVIEW_REPAIR_REQUIRED",
        "included_proposal_binding_count": proposal_binding_count,
        "excluded_ambiguity_binding_count": ambiguity_binding_count,
        "excluded_requirement_gap_binding_count": requirement_gap_binding_count,
        "scope_limited_to_four_proposals": proposal_binding_count == 4,
        "residual_branches_excluded_from_authorization_scope": True,
    }

    precondition_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_precondition_review_v0",
        "review_status": "AUTHORIZATION_PRECONDITION_REVIEW_PASS" if review_pass else "AUTHORIZATION_PRECONDITION_REVIEW_REPAIR_REQUIRED",
        "authorization_ready_now": False,
        "application_ready_now": False,
        "required_unsatisfied_preconditions_preserved": [
            "authorization_contract_review_pass",
            "explicit_human_or_validator_apply_decision_recorded",
            "proposal_hold_release_authorized",
        ],
        "review_result": "preconditions correctly block authorization/application until later decision",
    }

    forbidden_action_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_forbidden_action_review_v0",
        "review_status": "AUTHORIZATION_FORBIDDEN_ACTION_REVIEW_PASS" if review_pass else "AUTHORIZATION_FORBIDDEN_ACTION_REVIEW_REPAIR_REQUIRED",
        "grant_authorization_forbidden_here": True,
        "release_hold_forbidden_here": True,
        "apply_rebinds_forbidden_here": True,
        "values_metadata_patch_c5_forbidden_here": True,
    }

    hold_release_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_release_review_v0",
        "review_status": "HOLD_RELEASE_CONTRACT_REVIEW_PASS" if review_pass else "HOLD_RELEASE_CONTRACT_REVIEW_REPAIR_REQUIRED",
        "proposal_hold_preserved": True,
        "proposal_hold_released": False,
        "release_authorized_now": False,
        "release_requires_later_decision": True,
    }

    residual_branch_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_residual_branch_review_v0",
        "review_status": "RESIDUAL_BRANCH_PRESERVATION_REVIEW_PASS" if review_pass else "RESIDUAL_BRANCH_PRESERVATION_REVIEW_REPAIR_REQUIRED",
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "may_discard_residual_branches": False,
        "may_authorize_residual_branches_here": False,
    }

    decision_request_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_decision_request_review_v0",
        "review_status": "DECISION_REQUEST_REVIEW_PASS" if review_pass else "DECISION_REQUEST_REVIEW_REPAIR_REQUIRED",
        "human_or_validator_decision_required": review_pass,
        "decision_requested_now": False,
        "authorization_granted": False,
        "valid_decisions": [
            "ACCEPT_FOUR_PROPOSAL_REBINDS_FOR_ONE_TIME_APPLICATION_UNIT",
            "REJECT_FOUR_PROPOSAL_REBINDS",
            "DEFER_AND_REPAIR_PROPOSAL_BRANCH",
        ],
    }

    nonapplication_boundary_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_nonapplication_boundary_review_v0",
        "review_status": "NONAPPLICATION_BOUNDARY_REVIEW_PASS" if review_pass else "NONAPPLICATION_BOUNDARY_REVIEW_REPAIR_REQUIRED",
        "authorization_granted": False,
        "proposal_hold_released": False,
        "rebinds_applied": False,
        "values_authorized": False,
        "values_applied": False,
        "metadata_populated": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
    }

    decision_surface = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_decision_surface_v0",
        "decision_surface_status": "DECISION_SURFACE_READY_REQUIRES_HUMAN_OR_VALIDATOR_INPUT" if review_pass else "DECISION_SURFACE_NOT_READY",
        "decision_not_recorded": True,
        "authorization_granted": False,
        "proposal_binding_count": proposal_binding_count,
        "available_decisions": decision_request_review["valid_decisions"],
        "decision_boundary": "later human or validator decision only; this review unit cannot choose",
        "default_without_decision": "NO_AUTHORIZATION_NO_HOLD_RELEASE_NO_REBIND_APPLICATION",
    }

    downstream_decision_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_downstream_decision_table_v0",
        "decision_status": "AUTHORIZATION_CONTRACT_REVIEW_DOWNSTREAM_DECISION_EMITTED",
        "records": [
            {
                "decision": "REQUEST_APPLICATION_DECISION",
                "selected": review_pass,
                "next_unit": "REQUEST_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_APPLICATION_DECISION_V0",
                "why": "authorization contract passed review; a separate human/validator decision is now required",
            },
            {
                "decision": "AUTHORIZE_REBINDS_NOW",
                "selected": False,
                "next_unit": None,
                "why": "review does not grant authorization",
            },
            {
                "decision": "APPLY_REBINDS_NOW",
                "selected": False,
                "next_unit": None,
                "why": "no authorization recorded and proposal hold remains locked",
            },
        ],
    }

    review_packet = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_packet_v0",
        "review_packet_status": status,
        "summary": {
            "authorization_contract_review_pass": review_pass,
            "decision_required": review_pass,
            "proposal_binding_count": proposal_binding_count,
            "authorization_granted": False,
            "proposal_hold_released": False,
            "rebinds_applied": False,
            "metadata_populated": False,
        },
        "recommended_next": next_edge,
    }

    classification = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "authorization_contract_review_complete": not bool(failures),
        "authorization_contract_review_pass": review_pass,
        "human_or_validator_decision_required": review_pass,
        "decision_surface_ready": review_pass,
        "decision_recorded": False,
        "authorization_granted": False,
        "proposal_hold_released": False,
        "rebind_application_authorized": False,
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "schema_overlay_applied_for_this_contract": True,
        "schema_overlay_applied_globally": False,
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
        "runtime_patch_applied": False,
        "c5_opened": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_authority_boundary_v0",
        "status": status,
        "may_request_human_or_validator_decision_next": review_pass,
        "may_grant_authorization_now": False,
        "may_release_proposal_hold": False,
        "may_apply_rebinds": False,
        "may_apply_values": False,
        "may_populate_metadata": False,
        "may_select_target_for_build": False,
        "may_apply_runtime_patch": False,
        "may_open_c5": False,
        "may_treat_schema_as_reusable": False,
        "may_treat_schema_as_preapproved": False,
        "may_create_validator_registry_entry": False,
        "may_allow_future_automatic_use": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    rollup = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "authorization_contract_review_count": 1,
        "authorization_contract_review_pass_count": 1 if review_pass else 0,
        "human_or_validator_decision_required_count": 1 if review_pass else 0,
        "decision_surface_ready_count": 1 if review_pass else 0,
        "decision_recorded_count": 0,
        "authorization_granted_count": 0,
        "proposal_hold_released_count": 0,
        "rebind_application_authorized_count": 0,
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "schema_overlay_applied_for_this_contract_count": 1,
        "schema_overlay_applied_globally_count": 0,
        "reusable_schema_authorized_count": 0,
        "preapproved_schema_authorized_count": 0,
        "validator_registry_entry_created_count": 0,
        "future_automatic_use_allowed_count": 0,
        "typing_rule_applied_count": 0,
        "field_policy_modified_count": 0,
        "candidate_artifact_modified_count": 0,
        "source_row_locator_applied_count": 0,
        "rebinds_applied_count": 0,
        "values_authorized_count": 0,
        "values_applied_count": 0,
        "metadata_populated_count": 0,
        "ready_discriminator_count": 0,
        "target_selected_for_build_count": 0,
        "runtime_patch_applied_count": 0,
        "c5_opened_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": next_edge,
    }

    zero_keys = [
        "decision_recorded_count",
        "authorization_granted_count",
        "proposal_hold_released_count",
        "rebind_application_authorized_count",
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_profile_v0",
        "profile_id": "proposal_branch_authorization_contract_review_profile_" + sha8(rollup),
        "status": status,
        "authorization_contract_review_pass": review_pass,
        "human_or_validator_decision_required": review_pass,
        "decision_surface_ready": review_pass,
        "decision_recorded": False,
        "authorization_granted": False,
        "proposal_hold_released": False,
        "rebind_application_authorized": False,
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "schema_overlay_applied_for_this_contract": True,
        "schema_overlay_applied_globally": False,
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

    report = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The proposal branch authorization contract was reviewed and passed as a decision surface. It is ready to request a separate human/validator decision, but this unit records no decision, grants no authorization, releases no hold, applies no rebinds, and preserves the 22 ambiguity and 498 requirement-gap branches.",
        "proposal_binding_count": proposal_binding_count,
        "authorization_contract_review_pass_count": rollup["authorization_contract_review_pass_count"],
        "decision_recorded_count": 0,
        "authorization_granted_count": 0,
        "proposal_hold_released_count": 0,
        "rebinds_applied_count": 0,
        "metadata_populated_count": 0,
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    trace = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_authorization_contract",
                "question": "does the contract define bounded scope and preconditions",
                "answer": "yes" if review_pass else "no",
                "taken": "review contract surfaces",
            },
            {
                "step": "preserve_nonapplication",
                "question": "does review grant authorization",
                "answer": "no",
                "taken": "emit decision surface only",
            },
            {
                "step": "select_next_boundary",
                "question": "what is the next lawful boundary",
                "answer": "request human or validator decision" if review_pass else "repair contract",
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
    write_json(CONTRACT_REVIEW_PATH, contract_review)
    write_json(SCOPE_REVIEW_PATH, scope_review)
    write_json(PRECONDITION_REVIEW_PATH, precondition_review)
    write_json(FORBIDDEN_ACTION_REVIEW_PATH, forbidden_action_review)
    write_json(HOLD_RELEASE_REVIEW_PATH, hold_release_review)
    write_json(RESIDUAL_BRANCH_REVIEW_PATH, residual_branch_review)
    write_json(DECISION_REQUEST_REVIEW_PATH, decision_request_review)
    write_json(NONAPPLICATION_BOUNDARY_REVIEW_PATH, nonapplication_boundary_review)
    write_json(DECISION_SURFACE_PATH, decision_surface)
    write_json(DOWNSTREAM_DECISION_TABLE_PATH, downstream_decision_table)
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
        "AUTH_CONTRACT_REVIEW_0_SOURCE_RECEIPT_CONSUMED": SOURCE_AUTH_CONTRACT_RECEIPT_PATH.exists(),
        "AUTH_CONTRACT_REVIEW_1_CONTRACT_REVIEW_EMITTED": CONTRACT_REVIEW_PATH.exists(),
        "AUTH_CONTRACT_REVIEW_2_SCOPE_REVIEW_PASS": scope_review["review_status"] == "AUTHORIZATION_SCOPE_REVIEW_PASS",
        "AUTH_CONTRACT_REVIEW_3_PRECONDITION_REVIEW_PASS": precondition_review["review_status"] == "AUTHORIZATION_PRECONDITION_REVIEW_PASS",
        "AUTH_CONTRACT_REVIEW_4_FORBIDDEN_ACTION_REVIEW_PASS": forbidden_action_review["review_status"] == "AUTHORIZATION_FORBIDDEN_ACTION_REVIEW_PASS",
        "AUTH_CONTRACT_REVIEW_5_HOLD_RELEASE_REVIEW_PASS": hold_release_review["review_status"] == "HOLD_RELEASE_CONTRACT_REVIEW_PASS",
        "AUTH_CONTRACT_REVIEW_6_RESIDUAL_BRANCH_REVIEW_PASS": residual_branch_review["review_status"] == "RESIDUAL_BRANCH_PRESERVATION_REVIEW_PASS",
        "AUTH_CONTRACT_REVIEW_7_DECISION_REQUEST_REVIEW_PASS": decision_request_review["review_status"] == "DECISION_REQUEST_REVIEW_PASS",
        "AUTH_CONTRACT_REVIEW_8_NONAPPLICATION_BOUNDARY_REVIEW_PASS": nonapplication_boundary_review["review_status"] == "NONAPPLICATION_BOUNDARY_REVIEW_PASS",
        "AUTH_CONTRACT_REVIEW_9_DECISION_SURFACE_READY": decision_surface["decision_surface_status"] == "DECISION_SURFACE_READY_REQUIRES_HUMAN_OR_VALIDATOR_INPUT",
        "AUTH_CONTRACT_REVIEW_10_FOUR_PROPOSALS_SCOPED": proposal_binding_count == 4,
        "AUTH_CONTRACT_REVIEW_11_RESIDUAL_AMBIGUITY_BRANCH_PRESERVED": ambiguity_binding_count == 22,
        "AUTH_CONTRACT_REVIEW_12_RESIDUAL_REQUIREMENT_GAP_BRANCH_PRESERVED": requirement_gap_binding_count == 498,
        "AUTH_CONTRACT_REVIEW_13_NO_DECISION_RECORDED": rollup["decision_recorded_count"] == 0,
        "AUTH_CONTRACT_REVIEW_14_NO_AUTHORIZATION_GRANTED": rollup["authorization_granted_count"] == 0,
        "AUTH_CONTRACT_REVIEW_15_NO_HOLD_RELEASE": rollup["proposal_hold_released_count"] == 0,
        "AUTH_CONTRACT_REVIEW_16_NO_REBIND_APPLICATION_AUTHORIZED": rollup["rebind_application_authorized_count"] == 0,
        "AUTH_CONTRACT_REVIEW_17_NO_REBINDS_APPLIED": rollup["rebinds_applied_count"] == 0,
        "AUTH_CONTRACT_REVIEW_18_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "AUTH_CONTRACT_REVIEW_19_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "AUTH_CONTRACT_REVIEW_20_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "AUTH_CONTRACT_REVIEW_21_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "AUTH_CONTRACT_REVIEW_22_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "AUTH_CONTRACT_REVIEW_23_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "AUTH_CONTRACT_REVIEW_24_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "AUTH_CONTRACT_REVIEW_25_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "AUTH_CONTRACT_REVIEW_26_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "AUTH_CONTRACT_REVIEW_27_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "AUTH_CONTRACT_REVIEW_28_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "AUTH_CONTRACT_REVIEW_29_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "AUTH_CONTRACT_REVIEW_30_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "AUTH_CONTRACT_REVIEW_31_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "accepted_schema_overlay_reference_this_application_contract_only",
        "AUTH_CONTRACT_REVIEW_32_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "proposal": proposal_binding_count,
        "review_pass": review_pass,
        "decision_recorded": False,
        "authorized": False,
        "hold_released": False,
        "rebinds": 0,
        "metadata": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_authorization_contract_receipt_id": SOURCE_AUTH_CONTRACT_RECEIPT_ID,
        "machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "authorization_contract_review_complete": not bool(failures),
            "authorization_contract_review_pass": review_pass,
            "human_or_validator_decision_required": review_pass,
            "decision_surface_ready": review_pass,
            "decision_recorded": False,
            "authorization_granted": False,
            "proposal_hold_released": False,
            "rebind_application_authorized": False,
            "proposal_binding_count": proposal_binding_count,
            "ambiguity_binding_count_preserved": ambiguity_binding_count,
            "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
            "schema_overlay_applied_for_this_contract": True,
            "schema_overlay_applied_globally": False,
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
            "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": next_edge,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "contract_review": rel(CONTRACT_REVIEW_PATH),
            "scope_review": rel(SCOPE_REVIEW_PATH),
            "precondition_review": rel(PRECONDITION_REVIEW_PATH),
            "forbidden_action_review": rel(FORBIDDEN_ACTION_REVIEW_PATH),
            "hold_release_review": rel(HOLD_RELEASE_REVIEW_PATH),
            "residual_branch_review": rel(RESIDUAL_BRANCH_REVIEW_PATH),
            "decision_request_review": rel(DECISION_REQUEST_REVIEW_PATH),
            "nonapplication_boundary_review": rel(NONAPPLICATION_BOUNDARY_REVIEW_PATH),
            "decision_surface": rel(DECISION_SURFACE_PATH),
            "downstream_decision_table": rel(DOWNSTREAM_DECISION_TABLE_PATH),
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
    print(f"authorization_contract_review_receipt_id={receipt_id}")
    print(f"authorization_contract_review_receipt_path={rel(receipt_path)}")
    print(f"authorization_contract_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"authorization_contract_review_path={rel(CONTRACT_REVIEW_PATH)}")
    print(f"authorization_scope_review_path={rel(SCOPE_REVIEW_PATH)}")
    print(f"authorization_precondition_review_path={rel(PRECONDITION_REVIEW_PATH)}")
    print(f"authorization_forbidden_action_review_path={rel(FORBIDDEN_ACTION_REVIEW_PATH)}")
    print(f"authorization_hold_release_review_path={rel(HOLD_RELEASE_REVIEW_PATH)}")
    print(f"authorization_residual_branch_review_path={rel(RESIDUAL_BRANCH_REVIEW_PATH)}")
    print(f"authorization_decision_surface_path={rel(DECISION_SURFACE_PATH)}")
    print(f"authorization_contract_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"authorization_contract_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
