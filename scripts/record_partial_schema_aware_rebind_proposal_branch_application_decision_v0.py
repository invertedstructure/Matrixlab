#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RECORD_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_APPLICATION_DECISION_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_APPLICATION_DECISION"
MODE = "CHAT_HUMAN_DECISION_RECORD / ONE_TIME_APPLICATION_AUTHORIZATION / NO_APPLICATION_IN_THIS_UNIT"
BUILD_MODE = "PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_APPLICATION_DECISION_RECORD_ONLY"

SOURCE_AUTH_REVIEW_RECEIPT_ID = "a4f000a6"
SOURCE_AUTH_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0_receipts/a4f000a6.json"
SOURCE_AUTH_REVIEW_ASSESSMENT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_assessment_v0.json"
SOURCE_AUTH_CONTRACT_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0.json"
SOURCE_AUTH_SCOPE_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_scope_review_v0.json"
SOURCE_AUTH_PRECONDITION_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_precondition_review_v0.json"
SOURCE_AUTH_FORBIDDEN_ACTION_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_forbidden_action_review_v0.json"
SOURCE_AUTH_HOLD_RELEASE_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_release_review_v0.json"
SOURCE_AUTH_RESIDUAL_BRANCH_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_residual_branch_review_v0.json"
SOURCE_AUTH_DECISION_REQUEST_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_decision_request_review_v0.json"
SOURCE_AUTH_NONAPPLICATION_BOUNDARY_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_nonapplication_boundary_review_v0.json"
SOURCE_AUTH_DECISION_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_decision_surface_v0.json"
SOURCE_AUTH_DOWNSTREAM_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_downstream_decision_table_v0.json"
SOURCE_AUTH_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_classification_v0.json"
SOURCE_AUTH_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_authority_boundary_v0.json"
SOURCE_AUTH_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_rollup_v0.json"
SOURCE_AUTH_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_profile_v0.json"
SOURCE_PROPOSAL_CANDIDATE_REVIEW_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_candidate_review_table_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0_receipts"

DECISION_RECORD_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_record_v0.json"
DECISION_AUTHORIZATION_PACKET_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_authorization_packet_v0.json"
DECISION_SCOPE_LOCK_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_scope_lock_v0.json"
DECISION_HOLD_RELEASE_AUTHORIZATION_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_release_authorization_v0.json"
DECISION_APPLICATION_PRECONDITION_UPDATE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_precondition_update_v0.json"
DECISION_RESIDUAL_BRANCH_PRESERVATION_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_decision_residual_branch_preservation_v0.json"
DECISION_NONREUSE_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_decision_nonreuse_boundary_v0.json"
DECISION_NONAPPLICATION_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_decision_nonapplication_boundary_v0.json"
NEXT_APPLICATION_UNIT_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_next_application_unit_contract_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_downstream_table_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_AUTH_REVIEW_RECEIPT_PATH,
    SOURCE_AUTH_REVIEW_ASSESSMENT_PATH,
    SOURCE_AUTH_CONTRACT_REVIEW_PATH,
    SOURCE_AUTH_SCOPE_REVIEW_PATH,
    SOURCE_AUTH_PRECONDITION_REVIEW_PATH,
    SOURCE_AUTH_FORBIDDEN_ACTION_REVIEW_PATH,
    SOURCE_AUTH_HOLD_RELEASE_REVIEW_PATH,
    SOURCE_AUTH_RESIDUAL_BRANCH_REVIEW_PATH,
    SOURCE_AUTH_DECISION_REQUEST_REVIEW_PATH,
    SOURCE_AUTH_NONAPPLICATION_BOUNDARY_REVIEW_PATH,
    SOURCE_AUTH_DECISION_SURFACE_PATH,
    SOURCE_AUTH_DOWNSTREAM_DECISION_TABLE_PATH,
    SOURCE_AUTH_CLASSIFICATION_PATH,
    SOURCE_AUTH_AUTHORITY_BOUNDARY_PATH,
    SOURCE_AUTH_ROLLUP_PATH,
    SOURCE_AUTH_PROFILE_PATH,
    SOURCE_PROPOSAL_CANDIDATE_REVIEW_TABLE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_REVIEWED_DECISION_REQUIRED"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_AUTHORIZATION_CONTRACT_REVIEWED_DECISION_REQUIRED"
EXPECTED_SOURCE_NEXT = "REQUEST_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_APPLICATION_DECISION_V0"

CHAT_REVIEW_DECISION = "ACCEPT_FOUR_PROPOSAL_REBINDS_FOR_ONE_TIME_APPLICATION_UNIT"
CHAT_REVIEW_BASIS = "User confirmed in chat: good that is the correct choice, accept the one time application."

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

    receipt = read_json(SOURCE_AUTH_REVIEW_RECEIPT_PATH)
    summary = receipt.get("machine_readable_partial_schema_aware_rebind_proposal_branch_authorization_contract_review_summary", {})
    assessment = read_json(SOURCE_AUTH_REVIEW_ASSESSMENT_PATH)
    contract_review = read_json(SOURCE_AUTH_CONTRACT_REVIEW_PATH)
    scope_review = read_json(SOURCE_AUTH_SCOPE_REVIEW_PATH)
    precondition_review = read_json(SOURCE_AUTH_PRECONDITION_REVIEW_PATH)
    forbidden_review = read_json(SOURCE_AUTH_FORBIDDEN_ACTION_REVIEW_PATH)
    hold_review = read_json(SOURCE_AUTH_HOLD_RELEASE_REVIEW_PATH)
    residual_review = read_json(SOURCE_AUTH_RESIDUAL_BRANCH_REVIEW_PATH)
    decision_request_review = read_json(SOURCE_AUTH_DECISION_REQUEST_REVIEW_PATH)
    nonapp_review = read_json(SOURCE_AUTH_NONAPPLICATION_BOUNDARY_REVIEW_PATH)
    decision_surface = read_json(SOURCE_AUTH_DECISION_SURFACE_PATH)
    downstream = read_json(SOURCE_AUTH_DOWNSTREAM_DECISION_TABLE_PATH)
    classification = read_json(SOURCE_AUTH_CLASSIFICATION_PATH)
    authority = read_json(SOURCE_AUTH_AUTHORITY_BOUNDARY_PATH)
    rollup = read_json(SOURCE_AUTH_ROLLUP_PATH)
    profile = read_json(SOURCE_AUTH_PROFILE_PATH)
    proposal_table = read_json(SOURCE_PROPOSAL_CANDIDATE_REVIEW_TABLE_PATH)

    if receipt.get("receipt_id") != SOURCE_AUTH_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_auth_review_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_terminal_not_expected")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "authorization_contract_review_complete",
        "authorization_contract_review_pass",
        "human_or_validator_decision_required",
        "decision_surface_ready",
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
        "decision_recorded",
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
            failures.append(f"source_forbidden_true:{key}")

    if assessment.get("human_or_validator_decision_required") is not True:
        failures.append("assessment_decision_not_required")
    if contract_review.get("review_status") != "AUTHORIZATION_CONTRACT_REVIEW_PASS":
        failures.append("contract_review_not_pass")
    if scope_review.get("scope_limited_to_four_proposals") is not True:
        failures.append("scope_not_limited_to_four")
    if precondition_review.get("authorization_ready_now") is not False:
        failures.append("precondition_authorization_ready_true")
    if forbidden_review.get("grant_authorization_forbidden_here") is not True:
        failures.append("forbidden_review_missing_grant_forbidden")
    if hold_review.get("proposal_hold_released") is not False:
        failures.append("hold_already_released")
    if residual_review.get("ambiguity_binding_count_preserved") != 22 or residual_review.get("requirement_gap_binding_count_preserved") != 498:
        failures.append("residual_counts_wrong")
    valid = decision_request_review.get("valid_decisions", [])
    if CHAT_REVIEW_DECISION not in valid:
        failures.append("accepted_decision_not_in_valid_decisions")
    if decision_surface.get("decision_surface_status") != "DECISION_SURFACE_READY_REQUIRES_HUMAN_OR_VALIDATOR_INPUT":
        failures.append("decision_surface_not_ready")
    if decision_surface.get("decision_not_recorded") is not True:
        failures.append("decision_surface_already_recorded")
    if classification.get("human_or_validator_decision_required") is not True:
        failures.append("classification_decision_not_required")
    if authority.get("may_request_human_or_validator_decision_next") is not True:
        failures.append("authority_cannot_request_decision")
    if rollup.get("decision_recorded_count") != 0 or rollup.get("authorization_granted_count") != 0:
        failures.append("rollup_prior_decision_or_authorization_nonzero")
    if profile.get("decision_recorded") is not False or profile.get("authorization_granted") is not False:
        failures.append("profile_prior_decision_or_authorization_true")
    proposal_records = records(proposal_table)
    if len(proposal_records) != 4:
        failures.append(f"proposal_record_count_not_4:{len(proposal_records)}")
    if any(r.get("rebind_applied") is not False for r in proposal_records):
        failures.append("proposal_record_already_applied")

    return failures, {
        "summary": summary,
        "proposal_records": proposal_records,
        "valid_decisions": valid,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    summary = src.get("summary", {})
    proposal_records = src.get("proposal_records", [])
    proposal_binding_count = len(proposal_records)
    ambiguity_binding_count = int(summary.get("ambiguity_binding_count_preserved", 22) or 22)
    requirement_gap_binding_count = int(summary.get("requirement_gap_binding_count_preserved", 498) or 498)

    if failures:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_APPLICATION_DECISION_RECORD_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_APPLICATION_DECISION_RECORD_BASIS_V0"
        decision_recorded = False
        authorization_granted = False
    else:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_APPLICATION_DECISION_RECORDED_ONE_TIME_APPLICATION_AUTHORIZED"
        reason_codes = [
            "CHAT_HUMAN_DECISION_RECORDED",
            "ACCEPT_FOUR_PROPOSAL_REBINDS_FOR_ONE_TIME_APPLICATION_UNIT",
            "ONE_TIME_APPLICATION_AUTHORIZATION_GRANTED",
            "APPLICATION_SCOPE_LOCKED_TO_FOUR_PROPOSAL_REBINDS",
            "PROPOSAL_HOLD_RELEASE_AUTHORIZED_FOR_NEXT_APPLICATION_UNIT_ONLY",
            "RESIDUAL_AMBIGUITY_BRANCH_PRESERVED",
            "RESIDUAL_REQUIREMENT_GAP_BRANCH_PRESERVED",
            "NO_SCHEMA_REUSE_AUTHORIZED",
            "NO_PREAPPROVED_SCHEMA_AUTHORIZED",
            "NO_VALIDATOR_REGISTRY_ENTRY_CREATED",
            "NO_REBINDS_APPLIED_IN_DECISION_UNIT",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
        ]
        next_edge = "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_V0"
        decision_recorded = True
        authorization_granted = True

    proposal_refs = [
        {
            "binding_key": r.get("binding_key"),
            "candidate_ref": r.get("candidate_ref"),
            "source_receipt_id": r.get("source_receipt_id"),
            "source_artifact_path": r.get("source_artifact_path"),
            "schema_requirement_score": r.get("schema_requirement_score"),
            "authorized_for_one_time_application_unit": authorization_granted,
            "rebind_applied": False,
        }
        for r in proposal_records
    ]

    decision_record = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_record_v0",
        "decision_record_status": "APPLICATION_DECISION_RECORDED" if decision_recorded else "APPLICATION_DECISION_NOT_RECORDED",
        "source_authorization_contract_review_receipt_id": SOURCE_AUTH_REVIEW_RECEIPT_ID,
        "decision": CHAT_REVIEW_DECISION if decision_recorded else None,
        "decision_basis": CHAT_REVIEW_BASIS if decision_recorded else None,
        "decision_recorded": decision_recorded,
        "authorization_granted": authorization_granted,
        "authorization_type": "ONE_TIME_APPLICATION_UNIT_ONLY" if authorization_granted else None,
        "proposal_binding_count": proposal_binding_count,
        "proposal_refs": proposal_refs,
        "proposal_hold_released": False,
        "rebinds_applied": False,
    }

    authorization_packet = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_authorization_packet_v0",
        "authorization_packet_status": "ONE_TIME_APPLICATION_AUTHORIZATION_PACKET_EMITTED" if authorization_granted else "ONE_TIME_APPLICATION_AUTHORIZATION_PACKET_NOT_EMITTED",
        "authorized_action": "apply four held proposal rebinds in a separate one-time application unit only",
        "authorized_scope_count": proposal_binding_count,
        "authorization_granted": authorization_granted,
        "authorization_grants_direct_application_now": False,
        "requires_separate_application_unit": True,
        "proposal_hold_release_authorized_for_next_application_unit": authorization_granted,
        "proposal_hold_released_now": False,
        "rebinds_applied_now": False,
    }

    scope_lock = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_scope_lock_v0",
        "scope_lock_status": "SCOPE_LOCKED_TO_FOUR_PROPOSAL_REBINDS" if authorization_granted else "SCOPE_NOT_LOCKED",
        "included_scope": {
            "proposal_binding_count": proposal_binding_count,
            "proposal_refs": proposal_refs,
        },
        "excluded_scope": {
            "ambiguity_binding_count": ambiguity_binding_count,
            "requirement_gap_binding_count": requirement_gap_binding_count,
            "all_future_schema_reuse": False,
            "validator_registry_entry": False,
        },
        "may_expand_scope_in_application_unit": False,
    }

    hold_release_authorization = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_release_authorization_v0",
        "hold_release_authorization_status": "HOLD_RELEASE_AUTHORIZED_FOR_NEXT_APPLICATION_UNIT_ONLY" if authorization_granted else "HOLD_RELEASE_NOT_AUTHORIZED",
        "proposal_hold_release_authorized": authorization_granted,
        "proposal_hold_released_now": False,
        "release_may_occur_only_inside": "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_V0",
        "release_preconditions": [
            "decision record is consumed",
            "scope lock still matches four proposal refs",
            "residual branches still preserved",
            "no reusable schema authority inferred",
            "application unit applies only the authorized four rebinds",
        ],
    }

    application_precondition_update = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_precondition_update_v0",
        "precondition_update_status": "APPLICATION_PRECONDITIONS_PARTIALLY_SATISFIED_BY_DECISION",
        "preconditions": [
            {"precondition": "authorization_contract_review_pass", "satisfied": True},
            {"precondition": "explicit_human_or_validator_apply_decision_recorded", "satisfied": decision_recorded},
            {"precondition": "proposal_hold_release_authorized_for_next_application_unit", "satisfied": authorization_granted},
            {"precondition": "scope_lock_to_four_proposals", "satisfied": proposal_binding_count == 4},
            {"precondition": "separate_application_unit_built", "satisfied": False},
            {"precondition": "rebinds_applied", "satisfied": False},
        ],
        "application_ready_to_build": authorization_granted,
        "application_executed_now": False,
    }

    residual_preservation = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_decision_residual_branch_preservation_v0",
        "preservation_status": "RESIDUAL_BRANCHES_PRESERVED_ACROSS_DECISION",
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "decision_authorizes_ambiguity_branch": False,
        "decision_authorizes_requirement_gap_branch": False,
        "may_discard_residual_branches": False,
    }

    nonreuse_boundary = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_decision_nonreuse_boundary_v0",
        "nonreuse_boundary_status": "NONREUSE_BOUNDARY_REAFFIRMED",
        "one_time_application_only": authorization_granted,
        "schema_overlay_applied_for_this_contract": True,
        "schema_overlay_applied_globally": False,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
    }

    nonapplication_boundary = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_decision_nonapplication_boundary_v0",
        "nonapplication_boundary_status": "DECISION_RECORDED_NO_APPLICATION_IN_THIS_UNIT",
        "decision_recorded": decision_recorded,
        "authorization_granted": authorization_granted,
        "proposal_hold_released": False,
        "rebind_application_authorized_for_next_unit": authorization_granted,
        "rebinds_applied": False,
        "values_authorized": False,
        "values_applied": False,
        "metadata_populated": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
    }

    next_application_unit_contract = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_next_application_unit_contract_v0",
        "next_application_unit_contract_status": "NEXT_APPLICATION_UNIT_READY_TO_BUILD" if authorization_granted else "NEXT_APPLICATION_UNIT_NOT_READY",
        "next_unit": "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_V0" if authorization_granted else None,
        "must_consume": [
            rel(DECISION_RECORD_PATH),
            rel(DECISION_AUTHORIZATION_PACKET_PATH),
            rel(DECISION_SCOPE_LOCK_PATH),
            rel(DECISION_HOLD_RELEASE_AUTHORIZATION_PATH),
            rel(DECISION_RESIDUAL_BRANCH_PRESERVATION_PATH),
            rel(DECISION_NONREUSE_BOUNDARY_PATH),
        ],
        "must_apply_only": "the four proposal refs listed in the scope lock",
        "must_not_apply": [
            "ambiguity branch bindings",
            "requirement-gap branch bindings",
            "values",
            "metadata",
            "runtime patch",
            "C5 opening",
            "schema reuse or validator registry promotion",
        ],
    }

    downstream_decision_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_downstream_table_v0",
        "decision_status": "APPLICATION_DECISION_DOWNSTREAM_TABLE_EMITTED",
        "records": [
            {
                "decision": "BUILD_ONE_TIME_APPLICATION_UNIT",
                "selected": authorization_granted,
                "next_unit": "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_V0" if authorization_granted else None,
                "why": "one-time application decision was accepted and recorded",
            },
            {
                "decision": "APPLY_REBINDS_IN_DECISION_UNIT",
                "selected": False,
                "next_unit": None,
                "why": "decision unit records authority only; application must be a separate unit",
            },
            {
                "decision": "PROMOTE_SCHEMA_REUSE",
                "selected": False,
                "next_unit": None,
                "why": "decision is one-time application only",
            },
        ],
    }

    classification = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "application_decision_recorded": decision_recorded,
        "decision": CHAT_REVIEW_DECISION if decision_recorded else None,
        "authorization_granted": authorization_granted,
        "authorization_type": "ONE_TIME_APPLICATION_UNIT_ONLY" if authorization_granted else None,
        "proposal_binding_count": proposal_binding_count,
        "proposal_hold_release_authorized_for_next_application_unit": authorization_granted,
        "proposal_hold_released": False,
        "rebind_application_authorized_for_next_unit": authorization_granted,
        "rebinds_applied": False,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_authority_boundary_v0",
        "status": status,
        "may_build_one_time_application_unit_next": authorization_granted,
        "may_release_proposal_hold_in_next_application_unit": authorization_granted,
        "may_apply_authorized_four_rebinds_in_next_application_unit": authorization_granted,
        "may_apply_rebinds_now": False,
        "may_release_proposal_hold_now": False,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "application_decision_recorded_count": 1 if decision_recorded else 0,
        "application_decision_accept_count": 1 if authorization_granted else 0,
        "one_time_application_authorization_granted_count": 1 if authorization_granted else 0,
        "proposal_binding_count": proposal_binding_count,
        "proposal_hold_release_authorized_for_next_application_unit_count": 1 if authorization_granted else 0,
        "rebind_application_authorized_for_next_unit_count": 1 if authorization_granted else 0,
        "proposal_hold_released_count": 0,
        "rebinds_applied_count": 0,
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
        "proposal_hold_released_count",
        "rebinds_applied_count",
        "schema_overlay_applied_globally_count",
        "reusable_schema_authorized_count",
        "preapproved_schema_authorized_count",
        "validator_registry_entry_created_count",
        "future_automatic_use_allowed_count",
        "typing_rule_applied_count",
        "field_policy_modified_count",
        "candidate_artifact_modified_count",
        "source_row_locator_applied_count",
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_profile_v0",
        "profile_id": "proposal_branch_application_decision_profile_" + sha8(rollup),
        "status": status,
        "application_decision_recorded": decision_recorded,
        "decision": CHAT_REVIEW_DECISION if decision_recorded else None,
        "authorization_granted": authorization_granted,
        "authorization_type": "ONE_TIME_APPLICATION_UNIT_ONLY" if authorization_granted else None,
        "proposal_binding_count": proposal_binding_count,
        "proposal_hold_release_authorized_for_next_application_unit": authorization_granted,
        "proposal_hold_released": False,
        "rebind_application_authorized_for_next_unit": authorization_granted,
        "rebinds_applied": False,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The chat human decision accepted the four held proposal rebinds for a one-time application unit. This records bounded authorization for the next application unit only. It does not apply rebinds, release the hold in this unit, authorize schema reuse, populate values or metadata, patch runtime, or open C5.",
        "proposal_binding_count": proposal_binding_count,
        "application_decision_recorded_count": rollup["application_decision_recorded_count"],
        "one_time_application_authorization_granted_count": rollup["one_time_application_authorization_granted_count"],
        "proposal_hold_released_count": 0,
        "rebinds_applied_count": 0,
        "metadata_populated_count": 0,
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    trace = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_decision_surface",
                "question": "is the authorization contract reviewed and decision surface ready",
                "answer": "yes" if not failures else "no",
                "taken": "record chat human decision",
            },
            {
                "step": "record_bounded_decision",
                "question": "what decision was made",
                "answer": CHAT_REVIEW_DECISION if decision_recorded else None,
                "taken": "grant one-time application-unit authorization only",
            },
            {
                "step": "preserve_nonapplication_boundary",
                "question": "does this unit apply rebinds",
                "answer": "no",
                "taken": "emit next application unit contract",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(DECISION_RECORD_PATH, decision_record)
    write_json(DECISION_AUTHORIZATION_PACKET_PATH, authorization_packet)
    write_json(DECISION_SCOPE_LOCK_PATH, scope_lock)
    write_json(DECISION_HOLD_RELEASE_AUTHORIZATION_PATH, hold_release_authorization)
    write_json(DECISION_APPLICATION_PRECONDITION_UPDATE_PATH, application_precondition_update)
    write_json(DECISION_RESIDUAL_BRANCH_PRESERVATION_PATH, residual_preservation)
    write_json(DECISION_NONREUSE_BOUNDARY_PATH, nonreuse_boundary)
    write_json(DECISION_NONAPPLICATION_BOUNDARY_PATH, nonapplication_boundary)
    write_json(NEXT_APPLICATION_UNIT_CONTRACT_PATH, next_application_unit_contract)
    write_json(DOWNSTREAM_DECISION_TABLE_PATH, downstream_decision_table)
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
        "APP_DECISION_0_SOURCE_AUTH_REVIEW_RECEIPT_CONSUMED": SOURCE_AUTH_REVIEW_RECEIPT_PATH.exists(),
        "APP_DECISION_1_DECISION_RECORD_EMITTED": DECISION_RECORD_PATH.exists(),
        "APP_DECISION_2_ACCEPT_DECISION_RECORDED": decision_recorded and decision_record["decision"] == CHAT_REVIEW_DECISION,
        "APP_DECISION_3_ONE_TIME_APPLICATION_AUTHORIZATION_GRANTED": authorization_granted,
        "APP_DECISION_4_SCOPE_LOCKED_TO_FOUR_PROPOSALS": proposal_binding_count == 4,
        "APP_DECISION_5_HOLD_RELEASE_AUTHORIZED_FOR_NEXT_UNIT_ONLY": hold_release_authorization["proposal_hold_release_authorized"] is True and hold_release_authorization["proposal_hold_released_now"] is False,
        "APP_DECISION_6_NEXT_APPLICATION_UNIT_CONTRACT_EMITTED": NEXT_APPLICATION_UNIT_CONTRACT_PATH.exists(),
        "APP_DECISION_7_RESIDUAL_AMBIGUITY_BRANCH_PRESERVED": ambiguity_binding_count == 22,
        "APP_DECISION_8_RESIDUAL_REQUIREMENT_GAP_BRANCH_PRESERVED": requirement_gap_binding_count == 498,
        "APP_DECISION_9_NO_HOLD_RELEASE_IN_DECISION_UNIT": rollup["proposal_hold_released_count"] == 0,
        "APP_DECISION_10_NO_REBINDS_APPLIED_IN_DECISION_UNIT": rollup["rebinds_applied_count"] == 0,
        "APP_DECISION_11_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "APP_DECISION_12_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "APP_DECISION_13_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "APP_DECISION_14_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "APP_DECISION_15_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "APP_DECISION_16_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "APP_DECISION_17_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "APP_DECISION_18_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "APP_DECISION_19_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "APP_DECISION_20_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "APP_DECISION_21_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "APP_DECISION_22_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "APP_DECISION_23_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "APP_DECISION_24_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "accepted_schema_overlay_reference_this_application_contract_only",
        "APP_DECISION_25_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_APPLICATION_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "decision": CHAT_REVIEW_DECISION,
        "decision_recorded": decision_recorded,
        "authorization_granted": authorization_granted,
        "proposal": proposal_binding_count,
        "hold_released": False,
        "rebinds_applied": False,
        "metadata": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_APPLICATION_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_authorization_contract_review_receipt_id": SOURCE_AUTH_REVIEW_RECEIPT_ID,
        "chat_human_decision": CHAT_REVIEW_DECISION,
        "machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "application_decision_recorded": decision_recorded,
            "decision": CHAT_REVIEW_DECISION if decision_recorded else None,
            "authorization_granted": authorization_granted,
            "authorization_type": "ONE_TIME_APPLICATION_UNIT_ONLY" if authorization_granted else None,
            "proposal_binding_count": proposal_binding_count,
            "proposal_hold_release_authorized_for_next_application_unit": authorization_granted,
            "proposal_hold_released": False,
            "rebind_application_authorized_for_next_unit": authorization_granted,
            "rebinds_applied": False,
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
            "decision_record": rel(DECISION_RECORD_PATH),
            "authorization_packet": rel(DECISION_AUTHORIZATION_PACKET_PATH),
            "scope_lock": rel(DECISION_SCOPE_LOCK_PATH),
            "hold_release_authorization": rel(DECISION_HOLD_RELEASE_AUTHORIZATION_PATH),
            "application_precondition_update": rel(DECISION_APPLICATION_PRECONDITION_UPDATE_PATH),
            "residual_branch_preservation": rel(DECISION_RESIDUAL_BRANCH_PRESERVATION_PATH),
            "nonreuse_boundary": rel(DECISION_NONREUSE_BOUNDARY_PATH),
            "nonapplication_boundary": rel(DECISION_NONAPPLICATION_BOUNDARY_PATH),
            "next_application_unit_contract": rel(NEXT_APPLICATION_UNIT_CONTRACT_PATH),
            "downstream_decision_table": rel(DOWNSTREAM_DECISION_TABLE_PATH),
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
    print(f"application_decision_receipt_id={receipt_id}")
    print(f"application_decision_receipt_path={rel(receipt_path)}")
    print(f"application_decision_record_path={rel(DECISION_RECORD_PATH)}")
    print(f"application_decision_authorization_packet_path={rel(DECISION_AUTHORIZATION_PACKET_PATH)}")
    print(f"application_decision_scope_lock_path={rel(DECISION_SCOPE_LOCK_PATH)}")
    print(f"application_decision_hold_release_authorization_path={rel(DECISION_HOLD_RELEASE_AUTHORIZATION_PATH)}")
    print(f"application_decision_next_application_unit_contract_path={rel(NEXT_APPLICATION_UNIT_CONTRACT_PATH)}")
    print(f"application_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"application_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
