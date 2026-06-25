#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT"
MODE = "AUTHORIZATION_CONTRACT_BUILD / NO_AUTHORIZATION_GRANTED / HOLD_PRESERVED / NO_REBIND_APPLICATION"
BUILD_MODE = "PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_ONLY"

SOURCE_PROPOSAL_BRANCH_RECEIPT_ID = "2aee3233"
SOURCE_PROPOSAL_BRANCH_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0_receipts/2aee3233.json"
SOURCE_PROPOSAL_BRANCH_REVIEW_ASSESSMENT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_review_assessment_v0.json"
SOURCE_PROPOSAL_BRANCH_INPUT_INVENTORY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_input_inventory_v0.json"
SOURCE_PROPOSAL_CANDIDATE_REVIEW_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_candidate_review_table_v0.json"
SOURCE_PROPOSAL_CANDIDATE_INTEGRITY_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_candidate_integrity_surface_v0.json"
SOURCE_PROPOSAL_HOLD_PRESERVATION_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_hold_preservation_contract_v0.json"
SOURCE_PROPOSAL_APPLICATION_PRECONDITION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_application_precondition_table_v0.json"
SOURCE_PROPOSAL_AUTHORIZATION_REQUEST_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_authorization_request_packet_v0.json"
SOURCE_RESIDUAL_BRANCH_PRESERVATION_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_residual_branch_preservation_contract_v0.json"
SOURCE_DOWNSTREAM_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_downstream_decision_table_v0.json"
SOURCE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_classification_v0.json"
SOURCE_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authority_boundary_v0.json"
SOURCE_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_rollup_v0.json"
SOURCE_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0_receipts"

AUTH_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0.json"
AUTH_SCOPE_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_scope_table_v0.json"
AUTH_PRECONDITION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_precondition_table_v0.json"
AUTH_FORBIDDEN_ACTION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_forbidden_action_table_v0.json"
AUTH_HOLD_RELEASE_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_release_contract_v0.json"
AUTH_RESIDUAL_BRANCH_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_residual_branch_contract_v0.json"
AUTH_DECISION_REQUEST_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_decision_request_v0.json"
AUTH_NONAPPLICATION_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_nonapplication_boundary_v0.json"
AUTH_REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_packet_v0.json"
AUTH_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_downstream_decision_table_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_PROPOSAL_BRANCH_RECEIPT_PATH,
    SOURCE_PROPOSAL_BRANCH_REVIEW_ASSESSMENT_PATH,
    SOURCE_PROPOSAL_BRANCH_INPUT_INVENTORY_PATH,
    SOURCE_PROPOSAL_CANDIDATE_REVIEW_TABLE_PATH,
    SOURCE_PROPOSAL_CANDIDATE_INTEGRITY_SURFACE_PATH,
    SOURCE_PROPOSAL_HOLD_PRESERVATION_CONTRACT_PATH,
    SOURCE_PROPOSAL_APPLICATION_PRECONDITION_TABLE_PATH,
    SOURCE_PROPOSAL_AUTHORIZATION_REQUEST_PACKET_PATH,
    SOURCE_RESIDUAL_BRANCH_PRESERVATION_CONTRACT_PATH,
    SOURCE_DOWNSTREAM_DECISION_TABLE_PATH,
    SOURCE_CLASSIFICATION_PATH,
    SOURCE_AUTHORITY_BOUNDARY_PATH,
    SOURCE_ROLLUP_PATH,
    SOURCE_PROFILE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_REVIEWED_AUTHORIZATION_CONTRACT_REQUIRED"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_REVIEWED_AUTHORIZATION_CONTRACT_REQUIRED"
EXPECTED_SOURCE_NEXT = "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_V0"

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
    v = obj.get("records")
    return v if isinstance(v, list) else []

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(SOURCE_PROPOSAL_BRANCH_RECEIPT_PATH)
    summary = receipt.get("machine_readable_partial_schema_aware_rebind_proposal_branch_summary", {})
    assessment = read_json(SOURCE_PROPOSAL_BRANCH_REVIEW_ASSESSMENT_PATH)
    candidate_table = read_json(SOURCE_PROPOSAL_CANDIDATE_REVIEW_TABLE_PATH)
    integrity = read_json(SOURCE_PROPOSAL_CANDIDATE_INTEGRITY_SURFACE_PATH)
    hold = read_json(SOURCE_PROPOSAL_HOLD_PRESERVATION_CONTRACT_PATH)
    preconditions = read_json(SOURCE_PROPOSAL_APPLICATION_PRECONDITION_TABLE_PATH)
    auth_request = read_json(SOURCE_PROPOSAL_AUTHORIZATION_REQUEST_PACKET_PATH)
    residual = read_json(SOURCE_RESIDUAL_BRANCH_PRESERVATION_CONTRACT_PATH)
    decision = read_json(SOURCE_DOWNSTREAM_DECISION_TABLE_PATH)
    classif = read_json(SOURCE_CLASSIFICATION_PATH)
    authority = read_json(SOURCE_AUTHORITY_BOUNDARY_PATH)
    rollup = read_json(SOURCE_ROLLUP_PATH)
    profile = read_json(SOURCE_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_PROPOSAL_BRANCH_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_proposal_branch_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_terminal_not_expected")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "proposal_branch_review_complete",
        "proposal_branch_review_pass",
        "authorization_contract_required",
        "proposal_hold_preserved",
        "schema_overlay_applied_for_this_contract",
    ]:
        if summary.get(key) is not True:
            failures.append(f"source_required_true_missing:{key}")

    expected_counts = {
        "proposal_binding_count": 4,
        "proposal_candidate_review_pass_count": 4,
        "proposal_candidate_review_fail_count": 0,
        "ambiguity_binding_count_preserved": 22,
        "requirement_gap_binding_count_preserved": 498,
        "ready_discriminator_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"source_count_wrong:{key}:{summary.get(key)}")

    for key in [
        "proposal_hold_released",
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
            failures.append(f"source_forbidden_true:{key}")

    if assessment.get("authorization_contract_required") is not True:
        failures.append("assessment_auth_contract_not_required")
    if candidate_table.get("proposal_binding_count") != 4 or len(records(candidate_table)) != 4:
        failures.append("candidate_table_not_4")
    if candidate_table.get("proposal_candidate_review_fail_count") != 0:
        failures.append("candidate_table_has_failures")
    if integrity.get("integrity_status") != "PROPOSAL_BRANCH_CANDIDATE_INTEGRITY_PASS":
        failures.append("integrity_surface_not_pass")
    if hold.get("hold_preservation_status") != "PROPOSAL_HOLD_PRESERVED":
        failures.append("hold_not_preserved")
    if hold.get("hold_released") is not False or hold.get("release_allowed_now") is not False:
        failures.append("hold_release_not_false")
    if preconditions.get("application_ready_now") is not False:
        failures.append("application_ready_now_true")
    if auth_request.get("authorization_request_status") != "AUTHORIZATION_CONTRACT_REQUIRED":
        failures.append("authorization_request_status_wrong")
    if residual.get("preservation_status") != "RESIDUAL_BRANCHES_PRESERVED":
        failures.append("residual_branch_not_preserved")
    if residual.get("ambiguity_binding_count_preserved") != 22:
        failures.append("residual_ambiguity_count_wrong")
    if residual.get("requirement_gap_binding_count_preserved") != 498:
        failures.append("residual_gap_count_wrong")
    if any(isinstance(r, dict) and r.get("decision") == "APPLY_PROPOSAL_REBINDS" and r.get("selected") for r in decision.get("records", [])):
        failures.append("downstream_selected_apply_rebinds")
    if classif.get("authorization_contract_required") is not True:
        failures.append("classification_auth_contract_not_required")
    if classif.get("next_command_goal") is not None:
        failures.append("classification_hidden_next_command")
    if authority.get("may_build_authorization_contract_next") is not True:
        failures.append("authority_does_not_allow_auth_contract_build")
    if authority.get("may_apply_rebinds") is not False:
        failures.append("authority_allows_rebinds")
    if authority.get("may_release_proposal_hold") is not False:
        failures.append("authority_allows_hold_release")
    if rollup.get("authorization_contract_required_count") != 1:
        failures.append("rollup_auth_contract_required_not_1")
    if rollup.get("rebinds_applied_count") != 0:
        failures.append("rollup_rebinds_nonzero")
    if profile.get("authorization_contract_required") is not True:
        failures.append("profile_auth_contract_required_not_true")
    if profile.get("proposal_hold_released") is not False:
        failures.append("profile_hold_released")

    return failures, {
        "summary": summary,
        "candidate_rows": records(candidate_table),
        "hold": hold,
        "preconditions": preconditions,
        "residual": residual,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    summary = src.get("summary", {})
    candidate_rows = src.get("candidate_rows", [])
    proposal_binding_count = len(candidate_rows)
    ambiguity_binding_count = int(summary.get("ambiguity_binding_count_preserved", 22) or 22)
    requirement_gap_binding_count = int(summary.get("requirement_gap_binding_count_preserved", 498) or 498)

    if failures:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_BASIS_V0"
        contract_built = False
    else:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_BUILT_REVIEW_REQUIRED"
        reason_codes = [
            "PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_BUILT",
            "AUTHORIZATION_SCOPE_TABLE_EMITTED",
            "AUTHORIZATION_PRECONDITION_TABLE_EMITTED",
            "AUTHORIZATION_FORBIDDEN_ACTION_TABLE_EMITTED",
            "PROPOSAL_HOLD_RELEASE_CONTRACT_EMITTED",
            "RESIDUAL_BRANCH_PRESERVATION_REQUIREMENT_EMITTED",
            "HUMAN_OR_VALIDATOR_DECISION_REQUEST_EMITTED",
            "NONAPPLICATION_BOUNDARY_REAFFIRMED",
            "NO_AUTHORIZATION_GRANTED",
            "NO_PROPOSAL_HOLD_RELEASED",
            "NO_REBINDS_APPLIED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_V0"
        contract_built = True

    proposal_refs = [
        {
            "binding_key": r.get("binding_key"),
            "candidate_ref": r.get("candidate_ref"),
            "source_receipt_id": r.get("source_receipt_id"),
            "source_artifact_path": r.get("source_artifact_path"),
            "schema_requirement_score": r.get("schema_requirement_score"),
            "proposal_authorized_now": False,
            "rebind_applied": False,
        }
        for r in candidate_rows
    ]

    authorization_contract = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_v0",
        "contract_status": "AUTHORIZATION_CONTRACT_BUILT_REVIEW_REQUIRED" if contract_built else "AUTHORIZATION_CONTRACT_NOT_BUILT",
        "source_proposal_branch_receipt_id": SOURCE_PROPOSAL_BRANCH_RECEIPT_ID,
        "proposal_binding_count": proposal_binding_count,
        "proposal_refs": proposal_refs,
        "authorization_scope": "authorize review of whether four held proposal rebinds may be applied later, under this application contract only",
        "authorization_granted": False,
        "proposal_hold_release_authorized": False,
        "rebind_application_authorized": False,
        "one_time_contract_only": True,
        "future_automatic_use_allowed": False,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
    }

    authorization_scope_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_scope_table_v0",
        "scope_status": "AUTHORIZATION_SCOPE_EMITTED",
        "records": [
            {
                "scope_item": "four_held_schema_aware_rebind_proposals",
                "included": True,
                "count": proposal_binding_count,
                "meaning": "only these four proposal candidates may be considered by a later authorization decision",
            },
            {
                "scope_item": "twenty_two_ambiguity_bindings",
                "included": False,
                "count": ambiguity_binding_count,
                "meaning": "preserved as a separate repair branch; not authorized by this contract",
            },
            {
                "scope_item": "four_hundred_ninety_eight_requirement_gap_bindings",
                "included": False,
                "count": requirement_gap_binding_count,
                "meaning": "preserved as a separate repair branch; not authorized by this contract",
            },
        ],
    }

    authorization_precondition_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_precondition_table_v0",
        "precondition_status": "AUTHORIZATION_PRECONDITIONS_EMITTED_NOT_SATISFIED",
        "records": [
            {"precondition": "proposal_branch_review_pass", "satisfied": proposal_binding_count == 4 and not failures},
            {"precondition": "authorization_contract_review_pass", "satisfied": False},
            {"precondition": "explicit_human_or_validator_apply_decision_recorded", "satisfied": False},
            {"precondition": "proposal_hold_release_authorized", "satisfied": False},
            {"precondition": "residual_ambiguity_branch_preserved", "satisfied": ambiguity_binding_count == 22},
            {"precondition": "residual_requirement_gap_branch_preserved", "satisfied": requirement_gap_binding_count == 498},
            {"precondition": "no_global_schema_or_reusable_authority_implied", "satisfied": True},
        ],
        "authorization_ready_now": False,
        "application_ready_now": False,
    }

    forbidden_action_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_forbidden_action_table_v0",
        "forbidden_action_status": "FORBIDDEN_ACTIONS_REAFFIRMED",
        "forbidden_actions": [
            "grant authorization in the contract-build unit",
            "release proposal hold",
            "apply proposal rebinds",
            "apply any rebind outside the four proposal bindings",
            "choose ambiguity winners",
            "invent requirement-gap evidence",
            "authorize values",
            "apply values",
            "populate metadata",
            "mark discriminators ready",
            "select target for build",
            "apply runtime patch",
            "open C5",
            "promote schema to reusable",
            "treat schema as preapproved",
            "create validator registry entry",
            "allow future automatic use",
            "use latest-file guessing",
            "use mtime selection",
        ],
    }

    hold_release_contract = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_release_contract_v0",
        "hold_release_status": "HOLD_RELEASE_CONDITIONS_EMITTED_NOT_SATISFIED",
        "proposal_hold_preserved": True,
        "proposal_hold_released": False,
        "release_authorized_now": False,
        "release_requires": [
            "authorization contract review pass",
            "explicit apply decision",
            "residual branch preservation verified at decision time",
            "non-reuse boundary reaffirmed",
            "apply unit built separately after authorization",
        ],
    }

    residual_branch_contract = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_residual_branch_contract_v0",
        "residual_branch_status": "RESIDUAL_BRANCHES_MUST_REMAIN_PRESERVED",
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "may_discard_residual_branches": False,
        "may_collapse_residual_branches_into_null": False,
        "may_authorize_residual_branches_here": False,
    }

    decision_request = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_decision_request_v0",
        "decision_request_status": "HUMAN_OR_VALIDATOR_DECISION_REQUIRED_LATER",
        "requested_decision": "authorize_or_reject_application_of_four_held_proposal_rebinds",
        "decision_requested_now": False,
        "authorization_granted": False,
        "valid_decisions": [
            "ACCEPT_FOUR_PROPOSAL_REBINDS_FOR_ONE_TIME_APPLICATION_UNIT",
            "REJECT_FOUR_PROPOSAL_REBINDS",
            "DEFER_AND_REPAIR_PROPOSAL_BRANCH",
        ],
        "decision_boundary": "decision may be made only after this authorization contract is reviewed",
    }

    nonapplication_boundary = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_nonapplication_boundary_v0",
        "boundary_status": "NONAPPLICATION_BOUNDARY_REAFFIRMED",
        "authorization_contract_built": contract_built,
        "authorization_granted": False,
        "proposal_hold_released": False,
        "rebinds_applied": False,
        "values_authorized": False,
        "values_applied": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
    }

    review_packet = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_packet_v0",
        "review_packet_status": status,
        "summary": {
            "authorization_contract_built": contract_built,
            "authorization_contract_review_required": True,
            "proposal_binding_count": proposal_binding_count,
            "authorization_granted": False,
            "proposal_hold_released": False,
            "rebinds_applied": False,
            "metadata_populated": False,
        },
        "recommended_next": next_edge,
    }

    downstream_decision_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_downstream_decision_table_v0",
        "decision_status": "AUTHORIZATION_CONTRACT_DOWNSTREAM_DECISION_EMITTED",
        "records": [
            {
                "decision": "REVIEW_AUTHORIZATION_CONTRACT",
                "selected": contract_built,
                "next_unit": "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_V0",
                "why": "contract has been built but not reviewed",
            },
            {
                "decision": "AUTHORIZE_REBINDS",
                "selected": False,
                "next_unit": None,
                "why": "authorization contract review has not passed and no human/validator decision is recorded",
            },
            {
                "decision": "APPLY_REBINDS",
                "selected": False,
                "next_unit": None,
                "why": "not authorized and proposal hold remains locked",
            },
        ],
    }

    classification = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "authorization_contract_built": contract_built,
        "authorization_contract_review_required": True,
        "proposal_binding_count": proposal_binding_count,
        "authorization_scope_emitted": True,
        "authorization_preconditions_emitted": True,
        "authorization_forbidden_actions_emitted": True,
        "hold_release_contract_emitted": True,
        "residual_branch_contract_emitted": True,
        "decision_request_emitted": True,
        "authorization_granted": False,
        "proposal_hold_released": False,
        "rebind_application_authorized": False,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_authority_boundary_v0",
        "status": status,
        "may_review_authorization_contract_next": contract_built,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "authorization_contract_built_count": 1 if contract_built else 0,
        "authorization_contract_review_required_count": 1,
        "proposal_binding_count": proposal_binding_count,
        "authorization_scope_emitted_count": 1,
        "authorization_preconditions_emitted_count": 1,
        "authorization_forbidden_actions_emitted_count": 1,
        "hold_release_contract_emitted_count": 1,
        "residual_branch_contract_emitted_count": 1,
        "decision_request_emitted_count": 1,
        "authorization_granted_count": 0,
        "proposal_hold_released_count": 0,
        "rebind_application_authorized_count": 0,
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
        "general_cell1_authority_granted_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": next_edge,
    }

    zero_keys = [
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_profile_v0",
        "profile_id": "proposal_branch_authorization_contract_profile_" + sha8(rollup),
        "status": status,
        "authorization_contract_built": contract_built,
        "authorization_contract_review_required": True,
        "proposal_binding_count": proposal_binding_count,
        "authorization_granted": False,
        "proposal_hold_released": False,
        "rebind_application_authorized": False,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The proposal branch authorization contract was built for the four held proposal rebinds. It defines scope, preconditions, forbidden actions, hold-release requirements, residual branch preservation, and later decision requirements. It does not grant authorization, release hold, apply rebinds, authorize values, populate metadata, select targets, patch runtime, open C5, or promote reusable schema authority.",
        "proposal_binding_count": proposal_binding_count,
        "authorization_contract_built_count": rollup["authorization_contract_built_count"],
        "authorization_granted_count": 0,
        "proposal_hold_released_count": 0,
        "rebinds_applied_count": 0,
        "metadata_populated_count": 0,
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    trace = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_transition_trace_v0",
        "trace": [
            {
                "step": "consume_proposal_branch_review",
                "question": "what is missing before four proposals can be applied",
                "answer": "bounded authorization contract",
                "taken": "build authorization contract only",
            },
            {
                "step": "define_application_boundary",
                "question": "what may later be authorized",
                "answer": "only four held proposal rebinds under this application contract",
                "taken": "emit scope and precondition tables",
            },
            {
                "step": "preserve_nonapplication",
                "question": "is authorization granted now",
                "answer": "no",
                "taken": "review required before any decision",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(AUTH_CONTRACT_PATH, authorization_contract)
    write_json(AUTH_SCOPE_TABLE_PATH, authorization_scope_table)
    write_json(AUTH_PRECONDITION_TABLE_PATH, authorization_precondition_table)
    write_json(AUTH_FORBIDDEN_ACTION_TABLE_PATH, forbidden_action_table)
    write_json(AUTH_HOLD_RELEASE_CONTRACT_PATH, hold_release_contract)
    write_json(AUTH_RESIDUAL_BRANCH_CONTRACT_PATH, residual_branch_contract)
    write_json(AUTH_DECISION_REQUEST_PATH, decision_request)
    write_json(AUTH_NONAPPLICATION_BOUNDARY_PATH, nonapplication_boundary)
    write_json(AUTH_REVIEW_PACKET_PATH, review_packet)
    write_json(AUTH_DECISION_TABLE_PATH, downstream_decision_table)
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
        "AUTH_CONTRACT_0_SOURCE_RECEIPT_CONSUMED": SOURCE_PROPOSAL_BRANCH_RECEIPT_PATH.exists(),
        "AUTH_CONTRACT_1_AUTHORIZATION_CONTRACT_EMITTED": AUTH_CONTRACT_PATH.exists(),
        "AUTH_CONTRACT_2_SCOPE_TABLE_EMITTED": AUTH_SCOPE_TABLE_PATH.exists(),
        "AUTH_CONTRACT_3_PRECONDITION_TABLE_EMITTED": AUTH_PRECONDITION_TABLE_PATH.exists(),
        "AUTH_CONTRACT_4_FORBIDDEN_ACTION_TABLE_EMITTED": AUTH_FORBIDDEN_ACTION_TABLE_PATH.exists(),
        "AUTH_CONTRACT_5_HOLD_RELEASE_CONTRACT_EMITTED": AUTH_HOLD_RELEASE_CONTRACT_PATH.exists(),
        "AUTH_CONTRACT_6_RESIDUAL_BRANCH_CONTRACT_EMITTED": AUTH_RESIDUAL_BRANCH_CONTRACT_PATH.exists(),
        "AUTH_CONTRACT_7_DECISION_REQUEST_EMITTED": AUTH_DECISION_REQUEST_PATH.exists(),
        "AUTH_CONTRACT_8_NONAPPLICATION_BOUNDARY_EMITTED": AUTH_NONAPPLICATION_BOUNDARY_PATH.exists(),
        "AUTH_CONTRACT_9_FOUR_PROPOSALS_SCOPED": proposal_binding_count == 4,
        "AUTH_CONTRACT_10_RESIDUAL_AMBIGUITY_BRANCH_PRESERVED": ambiguity_binding_count == 22,
        "AUTH_CONTRACT_11_RESIDUAL_REQUIREMENT_GAP_BRANCH_PRESERVED": requirement_gap_binding_count == 498,
        "AUTH_CONTRACT_12_REVIEW_REQUIRED": classification["authorization_contract_review_required"] is True,
        "AUTH_CONTRACT_13_NO_AUTHORIZATION_GRANTED": rollup["authorization_granted_count"] == 0,
        "AUTH_CONTRACT_14_NO_HOLD_RELEASE": rollup["proposal_hold_released_count"] == 0,
        "AUTH_CONTRACT_15_NO_REBIND_APPLICATION_AUTHORIZED": rollup["rebind_application_authorized_count"] == 0,
        "AUTH_CONTRACT_16_NO_REBINDS_APPLIED": rollup["rebinds_applied_count"] == 0,
        "AUTH_CONTRACT_17_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "AUTH_CONTRACT_18_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "AUTH_CONTRACT_19_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "AUTH_CONTRACT_20_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "AUTH_CONTRACT_21_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "AUTH_CONTRACT_22_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "AUTH_CONTRACT_23_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "AUTH_CONTRACT_24_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "AUTH_CONTRACT_25_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "AUTH_CONTRACT_26_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "AUTH_CONTRACT_27_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "AUTH_CONTRACT_28_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "AUTH_CONTRACT_29_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "AUTH_CONTRACT_30_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "accepted_schema_overlay_reference_this_application_contract_only",
        "AUTH_CONTRACT_31_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "proposal": proposal_binding_count,
        "contract": contract_built,
        "authorized": False,
        "hold_released": False,
        "rebinds": 0,
        "metadata": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_proposal_branch_receipt_id": SOURCE_PROPOSAL_BRANCH_RECEIPT_ID,
        "machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "authorization_contract_built": contract_built,
            "authorization_contract_review_required": True,
            "proposal_binding_count": proposal_binding_count,
            "authorization_scope_emitted": True,
            "authorization_preconditions_emitted": True,
            "authorization_forbidden_actions_emitted": True,
            "hold_release_contract_emitted": True,
            "residual_branch_contract_emitted": True,
            "decision_request_emitted": True,
            "authorization_granted": False,
            "proposal_hold_released": False,
            "rebind_application_authorized": False,
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
            "authorization_contract": rel(AUTH_CONTRACT_PATH),
            "authorization_scope_table": rel(AUTH_SCOPE_TABLE_PATH),
            "authorization_precondition_table": rel(AUTH_PRECONDITION_TABLE_PATH),
            "authorization_forbidden_action_table": rel(AUTH_FORBIDDEN_ACTION_TABLE_PATH),
            "hold_release_contract": rel(AUTH_HOLD_RELEASE_CONTRACT_PATH),
            "residual_branch_contract": rel(AUTH_RESIDUAL_BRANCH_CONTRACT_PATH),
            "decision_request": rel(AUTH_DECISION_REQUEST_PATH),
            "nonapplication_boundary": rel(AUTH_NONAPPLICATION_BOUNDARY_PATH),
            "review_packet": rel(AUTH_REVIEW_PACKET_PATH),
            "downstream_decision_table": rel(AUTH_DECISION_TABLE_PATH),
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
    print(f"proposal_branch_authorization_contract_receipt_id={receipt_id}")
    print(f"proposal_branch_authorization_contract_receipt_path={rel(receipt_path)}")
    print(f"proposal_branch_authorization_contract_path={rel(AUTH_CONTRACT_PATH)}")
    print(f"proposal_branch_authorization_scope_table_path={rel(AUTH_SCOPE_TABLE_PATH)}")
    print(f"proposal_branch_authorization_precondition_table_path={rel(AUTH_PRECONDITION_TABLE_PATH)}")
    print(f"proposal_branch_authorization_forbidden_action_table_path={rel(AUTH_FORBIDDEN_ACTION_TABLE_PATH)}")
    print(f"proposal_branch_hold_release_contract_path={rel(AUTH_HOLD_RELEASE_CONTRACT_PATH)}")
    print(f"proposal_branch_residual_branch_contract_path={rel(AUTH_RESIDUAL_BRANCH_CONTRACT_PATH)}")
    print(f"proposal_branch_authorization_decision_request_path={rel(AUTH_DECISION_REQUEST_PATH)}")
    print(f"proposal_branch_authorization_contract_rollup_path={rel(ROLLUP_PATH)}")
    print(f"proposal_branch_authorization_contract_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
