#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT"
MODE = "ONE_TIME_APPLICATION / APPLY_AUTHORIZED_SOURCE_REF_REBINDS_ONLY / PRESERVE_RESIDUAL_BRANCHES"
BUILD_MODE = "PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_ONLY"

SOURCE_APP_DECISION_RECEIPT_ID = "f549ad67"
SOURCE_APP_DECISION_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0_receipts/f549ad67.json"
SOURCE_APP_DECISION_RECORD_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_record_v0.json"
SOURCE_AUTH_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_authorization_packet_v0.json"
SOURCE_SCOPE_LOCK_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_scope_lock_v0.json"
SOURCE_HOLD_RELEASE_AUTH_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_release_authorization_v0.json"
SOURCE_PRECONDITION_UPDATE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_precondition_update_v0.json"
SOURCE_RESIDUAL_PRESERVATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_decision_residual_branch_preservation_v0.json"
SOURCE_NONREUSE_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_decision_nonreuse_boundary_v0.json"
SOURCE_NONAPPLICATION_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_decision_nonapplication_boundary_v0.json"
SOURCE_NEXT_APPLICATION_UNIT_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_next_application_unit_contract_v0.json"
SOURCE_DOWNSTREAM_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_downstream_table_v0.json"
SOURCE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_classification_v0.json"
SOURCE_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_authority_boundary_v0.json"
SOURCE_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_rollup_v0.json"
SOURCE_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_profile_v0.json"
SOURCE_PROPOSAL_CANDIDATE_REVIEW_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_candidate_review_table_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0_receipts"

APPLICATION_PLAN_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_plan_v0.json"
SCOPE_GUARD_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_scope_guard_v0.json"
HOLD_RELEASE_RECORD_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_release_record_v0.json"
APPLIED_REBIND_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_applied_rebind_table_v0.json"
APPLIED_REBIND_LEDGER_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_applied_rebind_ledger_v0.json"
APPLIED_REBIND_INDEX_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_applied_rebind_index_v0.json"
RESIDUAL_BRANCH_PRESERVATION_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_residual_branch_preservation_v0.json"
NONREUSE_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_nonreuse_boundary_v0.json"
NONMETADATA_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_nonmetadata_boundary_v0.json"
POST_APPLICATION_STATE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_post_application_state_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_downstream_table_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_APP_DECISION_RECEIPT_PATH,
    SOURCE_APP_DECISION_RECORD_PATH,
    SOURCE_AUTH_PACKET_PATH,
    SOURCE_SCOPE_LOCK_PATH,
    SOURCE_HOLD_RELEASE_AUTH_PATH,
    SOURCE_PRECONDITION_UPDATE_PATH,
    SOURCE_RESIDUAL_PRESERVATION_PATH,
    SOURCE_NONREUSE_BOUNDARY_PATH,
    SOURCE_NONAPPLICATION_BOUNDARY_PATH,
    SOURCE_NEXT_APPLICATION_UNIT_CONTRACT_PATH,
    SOURCE_DOWNSTREAM_TABLE_PATH,
    SOURCE_CLASSIFICATION_PATH,
    SOURCE_AUTHORITY_BOUNDARY_PATH,
    SOURCE_ROLLUP_PATH,
    SOURCE_PROFILE_PATH,
    SOURCE_PROPOSAL_CANDIDATE_REVIEW_TABLE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_APPLICATION_DECISION_RECORDED_ONE_TIME_APPLICATION_AUTHORIZED"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_APPLICATION_DECISION_RECORDED_ONE_TIME_APPLICATION_AUTHORIZED"
EXPECTED_SOURCE_NEXT = "BUILD_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_V0"
EXPECTED_DECISION = "ACCEPT_FOUR_PROPOSAL_REBINDS_FOR_ONE_TIME_APPLICATION_UNIT"

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

    receipt = read_json(SOURCE_APP_DECISION_RECEIPT_PATH)
    summary = receipt.get("machine_readable_partial_schema_aware_rebind_proposal_branch_application_decision_summary", {})
    decision_record = read_json(SOURCE_APP_DECISION_RECORD_PATH)
    auth_packet = read_json(SOURCE_AUTH_PACKET_PATH)
    scope_lock = read_json(SOURCE_SCOPE_LOCK_PATH)
    hold_auth = read_json(SOURCE_HOLD_RELEASE_AUTH_PATH)
    preconditions = read_json(SOURCE_PRECONDITION_UPDATE_PATH)
    residual = read_json(SOURCE_RESIDUAL_PRESERVATION_PATH)
    nonreuse = read_json(SOURCE_NONREUSE_BOUNDARY_PATH)
    nonapp = read_json(SOURCE_NONAPPLICATION_BOUNDARY_PATH)
    next_contract = read_json(SOURCE_NEXT_APPLICATION_UNIT_CONTRACT_PATH)
    downstream = read_json(SOURCE_DOWNSTREAM_TABLE_PATH)
    classif = read_json(SOURCE_CLASSIFICATION_PATH)
    authority = read_json(SOURCE_AUTHORITY_BOUNDARY_PATH)
    rollup = read_json(SOURCE_ROLLUP_PATH)
    profile = read_json(SOURCE_PROFILE_PATH)
    proposal_table = read_json(SOURCE_PROPOSAL_CANDIDATE_REVIEW_TABLE_PATH)

    if receipt.get("receipt_id") != SOURCE_APP_DECISION_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_application_decision_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_terminal_not_expected")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("decision") != EXPECTED_DECISION:
        failures.append(f"decision_not_expected:{summary.get('decision')}")
    if summary.get("authorization_type") != "ONE_TIME_APPLICATION_UNIT_ONLY":
        failures.append("authorization_type_not_one_time")

    for key in [
        "application_decision_recorded",
        "authorization_granted",
        "proposal_hold_release_authorized_for_next_application_unit",
        "rebind_application_authorized_for_next_unit",
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
        "proposal_hold_released",
        "rebinds_applied",
        "schema_overlay_applied_globally",
        "reusable_schema_authorized",
        "preapproved_schema_authorized",
        "validator_registry_entry_created",
        "future_automatic_use_allowed",
        "typing_rule_applied",
        "field_policy_modified",
        "candidate_artifact_modified",
        "source_row_locator_applied",
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

    if decision_record.get("decision") != EXPECTED_DECISION or decision_record.get("authorization_granted") is not True:
        failures.append("decision_record_not_accept_authorized")
    if decision_record.get("rebinds_applied") is not False:
        failures.append("decision_record_already_applied")
    if auth_packet.get("authorization_granted") is not True:
        failures.append("authorization_packet_not_granted")
    if auth_packet.get("requires_separate_application_unit") is not True:
        failures.append("authorization_packet_not_separate_unit")
    if auth_packet.get("rebinds_applied_now") is not False:
        failures.append("authorization_packet_already_applied")
    if scope_lock.get("scope_lock_status") != "SCOPE_LOCKED_TO_FOUR_PROPOSAL_REBINDS":
        failures.append("scope_lock_status_wrong")
    included = scope_lock.get("included_scope", {})
    if included.get("proposal_binding_count") != 4:
        failures.append("scope_lock_not_4")
    if scope_lock.get("may_expand_scope_in_application_unit") is not False:
        failures.append("scope_lock_allows_expansion")
    if hold_auth.get("proposal_hold_release_authorized") is not True:
        failures.append("hold_release_not_authorized")
    if hold_auth.get("proposal_hold_released_now") is not False:
        failures.append("hold_already_released")
    if preconditions.get("application_ready_to_build") is not True or preconditions.get("application_executed_now") is not False:
        failures.append("precondition_update_not_ready_to_build_or_already_executed")
    if residual.get("ambiguity_binding_count_preserved") != 22 or residual.get("requirement_gap_binding_count_preserved") != 498:
        failures.append("residual_counts_wrong")
    for key in ["schema_overlay_applied_globally", "reusable_schema_authorized", "preapproved_schema_authorized", "validator_registry_entry_created", "future_automatic_use_allowed"]:
        if nonreuse.get(key) is not False:
            failures.append(f"nonreuse_boundary_true:{key}")
    if nonapp.get("rebinds_applied") is not False:
        failures.append("nonapplication_boundary_already_applied")
    if next_contract.get("next_application_unit_contract_status") != "NEXT_APPLICATION_UNIT_READY_TO_BUILD":
        failures.append("next_application_unit_contract_not_ready")
    if not any(isinstance(r, dict) and r.get("decision") == "BUILD_ONE_TIME_APPLICATION_UNIT" and r.get("selected") is True for r in downstream.get("records", [])):
        failures.append("downstream_does_not_select_application_unit")
    if classif.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append("classification_next_wrong")
    if authority.get("may_build_one_time_application_unit_next") is not True:
        failures.append("authority_cannot_build_one_time_application")
    if authority.get("may_apply_authorized_four_rebinds_in_next_application_unit") is not True:
        failures.append("authority_does_not_allow_four_rebinds_next_unit")
    if rollup.get("one_time_application_authorization_granted_count") != 1:
        failures.append("rollup_auth_granted_count_wrong")
    if rollup.get("rebinds_applied_count") != 0:
        failures.append("rollup_rebinds_already_applied")
    if profile.get("authorization_granted") is not True:
        failures.append("profile_auth_not_granted")
    if profile.get("rebinds_applied") is not False:
        failures.append("profile_rebinds_already_applied")

    proposal_records = records(proposal_table)
    if len(proposal_records) != 4:
        failures.append(f"proposal_record_count_not_4:{len(proposal_records)}")
    for idx, rec in enumerate(proposal_records):
        if rec.get("proposal_branch_review_status") != "PROPOSAL_BRANCH_CANDIDATE_REVIEW_PASS":
            failures.append(f"proposal_record_not_pass:{idx}")
        if rec.get("rebind_applied") is not False:
            failures.append(f"proposal_record_already_applied:{idx}")
        for key in ["binding_key", "candidate_ref", "source_receipt_id", "source_artifact_path"]:
            if not rec.get(key):
                failures.append(f"proposal_record_missing_{key}:{idx}")

    return failures, {
        "summary": summary,
        "decision_record": decision_record,
        "scope_lock": scope_lock,
        "proposal_records": proposal_records,
    }

def make_applied_rows(proposal_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows_out: List[Dict[str, Any]] = []
    seen = set()
    for idx, rec in enumerate(proposal_records):
        binding_key = rec.get("binding_key")
        if binding_key in seen:
            raise ValueError(f"duplicate binding_key in authorized scope: {binding_key}")
        seen.add(binding_key)
        row = {
            "applied_rebind_id": "applied_rebind_" + sha8({"idx": idx, "binding_key": binding_key, "candidate_ref": rec.get("candidate_ref")}),
            "binding_key": binding_key,
            "candidate_ref": rec.get("candidate_ref"),
            "source_receipt_id": rec.get("source_receipt_id"),
            "source_artifact_path": rec.get("source_artifact_path"),
            "schema_requirement_score": rec.get("schema_requirement_score"),
            "application_scope": "FOUR_AUTHORIZED_PROPOSAL_REBINDS_ONLY",
            "application_type": "ONE_TIME_APPLICATION_UNIT",
            "applied": True,
            "applied_at": now_iso(),
            "application_effect": "source_ref_rebind_recorded_in_applied_rebind_ledger",
            "values_authorized": False,
            "values_applied": False,
            "metadata_populated": False,
            "runtime_patch_applied": False,
            "c5_opened": False,
        }
        rows_out.append(row)
    return rows_out

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

    applied_rows: List[Dict[str, Any]] = []
    try:
        if not failures:
            applied_rows = make_applied_rows(proposal_records)
    except Exception as exc:
        failures.append(f"applied_row_build_failed:{exc}")

    if failures:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_BASIS_V0"
        application_executed = False
        hold_released = False
        rebinds_applied_count = 0
    else:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_APPLIED_REVIEW_REQUIRED"
        reason_codes = [
            "ONE_TIME_APPLICATION_UNIT_EXECUTED",
            "PROPOSAL_HOLD_RELEASED_INSIDE_AUTHORIZED_APPLICATION_UNIT",
            "FOUR_AUTHORIZED_PROPOSAL_REBINDS_APPLIED",
            "APPLICATION_SCOPE_LOCK_ENFORCED",
            "RESIDUAL_AMBIGUITY_BRANCH_PRESERVED",
            "RESIDUAL_REQUIREMENT_GAP_BRANCH_PRESERVED",
            "NO_SCHEMA_REUSE_AUTHORIZED",
            "NO_PREAPPROVED_SCHEMA_AUTHORIZED",
            "NO_VALIDATOR_REGISTRY_ENTRY_CREATED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
            "NO_RUNTIME_PATCH_APPLIED",
            "NO_C5_OPENED",
        ]
        next_edge = "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_V0"
        application_executed = True
        hold_released = True
        rebinds_applied_count = len(applied_rows)

    application_plan = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_plan_v0",
        "plan_status": "ONE_TIME_APPLICATION_PLAN_EXECUTED" if application_executed else "ONE_TIME_APPLICATION_PLAN_NOT_EXECUTED",
        "source_application_decision_receipt_id": SOURCE_APP_DECISION_RECEIPT_ID,
        "authorized_decision": EXPECTED_DECISION,
        "application_scope": "FOUR_AUTHORIZED_PROPOSAL_REBINDS_ONLY",
        "proposal_binding_count": proposal_binding_count,
        "planned_rebind_count": proposal_binding_count,
        "applied_rebind_count": rebinds_applied_count,
        "application_executed": application_executed,
    }

    scope_guard = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_scope_guard_v0",
        "scope_guard_status": "SCOPE_GUARD_PASS" if application_executed else "SCOPE_GUARD_FAIL_OR_NOT_RUN",
        "authorized_scope_count": 4,
        "observed_scope_count": proposal_binding_count,
        "applied_scope_count": rebinds_applied_count,
        "scope_expansion_detected": False,
        "applied_only_authorized_proposal_rebinds": application_executed and rebinds_applied_count == 4,
        "excluded_ambiguity_binding_count": ambiguity_binding_count,
        "excluded_requirement_gap_binding_count": requirement_gap_binding_count,
    }

    hold_release_record = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_release_record_v0",
        "hold_release_status": "PROPOSAL_HOLD_RELEASED_INSIDE_AUTHORIZED_APPLICATION_UNIT" if hold_released else "PROPOSAL_HOLD_NOT_RELEASED",
        "source_application_decision_receipt_id": SOURCE_APP_DECISION_RECEIPT_ID,
        "hold_release_authorized_by_decision": True,
        "hold_released": hold_released,
        "release_scope": "four authorized proposal rebinds only",
        "release_does_not_authorize_schema_reuse": True,
    }

    applied_rebind_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_applied_rebind_table_v0",
        "table_status": "FOUR_AUTHORIZED_PROPOSAL_REBINDS_APPLIED" if application_executed else "NO_REBINDS_APPLIED",
        "source_application_decision_receipt_id": SOURCE_APP_DECISION_RECEIPT_ID,
        "applied_rebind_count": rebinds_applied_count,
        "records": applied_rows,
    }

    applied_rebind_ledger = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_applied_rebind_ledger_v0",
        "ledger_status": "ONE_TIME_APPLICATION_LEDGER_MATERIALIZED" if application_executed else "ONE_TIME_APPLICATION_LEDGER_NOT_MATERIALIZED",
        "ledger_id": "one_time_rebind_application_" + sha8(applied_rows),
        "application_type": "ONE_TIME_APPLICATION_UNIT",
        "applied_rebind_count": rebinds_applied_count,
        "applied_rebind_ids": [r["applied_rebind_id"] for r in applied_rows],
        "source_application_decision_receipt_id": SOURCE_APP_DECISION_RECEIPT_ID,
        "authorizes_future_use": False,
    }

    applied_rebind_index = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_applied_rebind_index_v0",
        "index_status": "APPLIED_REBIND_INDEX_EMITTED" if application_executed else "APPLIED_REBIND_INDEX_NOT_EMITTED",
        "by_binding_key": {r["binding_key"]: r["applied_rebind_id"] for r in applied_rows},
        "by_candidate_ref": {str(r["candidate_ref"]): r["applied_rebind_id"] for r in applied_rows},
        "applied_rebind_count": rebinds_applied_count,
    }

    residual_preservation = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_residual_branch_preservation_v0",
        "preservation_status": "RESIDUAL_BRANCHES_PRESERVED_AFTER_ONE_TIME_APPLICATION",
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "ambiguity_branch_applied": False,
        "requirement_gap_branch_applied": False,
        "may_discard_residual_branches": False,
    }

    nonreuse_boundary = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_nonreuse_boundary_v0",
        "nonreuse_boundary_status": "NONREUSE_BOUNDARY_REAFFIRMED_AFTER_APPLICATION",
        "one_time_application_completed": application_executed,
        "schema_overlay_applied_for_this_contract": True,
        "schema_overlay_applied_globally": False,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
    }

    nonmetadata_boundary = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_nonmetadata_boundary_v0",
        "nonmetadata_boundary_status": "SOURCE_REF_REBIND_APPLIED_VALUES_METADATA_NOT_POPULATED",
        "values_authorized": False,
        "values_applied": False,
        "null_reasons_accepted": False,
        "source_packet_materialized_for_review": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
    }

    post_application_state = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_post_application_state_v0",
        "post_application_status": "FOUR_SOURCE_REF_REBINDS_APPLIED_REVIEW_REQUIRED" if application_executed else "APPLICATION_NOT_EXECUTED",
        "source_application_decision_receipt_id": SOURCE_APP_DECISION_RECEIPT_ID,
        "proposal_hold_released": hold_released,
        "rebinds_applied": application_executed,
        "applied_rebind_count": rebinds_applied_count,
        "applied_rebind_table": rel(APPLIED_REBIND_TABLE_PATH),
        "applied_rebind_ledger": rel(APPLIED_REBIND_LEDGER_PATH),
        "next_review_required": application_executed,
    }

    downstream_decision_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_downstream_table_v0",
        "decision_status": "ONE_TIME_APPLICATION_DOWNSTREAM_DECISION_EMITTED",
        "records": [
            {
                "decision": "REVIEW_ONE_TIME_APPLICATION_UNIT",
                "selected": application_executed,
                "next_unit": "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_V0" if application_executed else None,
                "why": "authorized application has been materialized and must be reviewed before downstream use",
            },
            {
                "decision": "POPULATE_METADATA_NOW",
                "selected": False,
                "next_unit": None,
                "why": "metadata remains out of scope",
            },
            {
                "decision": "PATCH_RUNTIME_NOW",
                "selected": False,
                "next_unit": None,
                "why": "runtime patch remains out of scope",
            },
        ],
    }

    classification = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "one_time_application_unit_executed": application_executed,
        "proposal_hold_released": hold_released,
        "rebinds_applied": application_executed,
        "applied_rebind_count": rebinds_applied_count,
        "proposal_binding_count": proposal_binding_count,
        "application_scope_guard_pass": application_executed and rebinds_applied_count == 4,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_authority_boundary_v0",
        "status": status,
        "may_review_one_time_application_next": application_executed,
        "may_apply_more_rebinds": False,
        "may_apply_ambiguity_branch": False,
        "may_apply_requirement_gap_branch": False,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "one_time_application_unit_executed_count": 1 if application_executed else 0,
        "proposal_hold_released_count": 1 if hold_released else 0,
        "rebinds_applied_count": rebinds_applied_count,
        "proposal_binding_count": proposal_binding_count,
        "application_scope_guard_pass_count": 1 if application_executed and rebinds_applied_count == 4 else 0,
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
        "dominance_rule_applied_count": 0,
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
        "schema_overlay_applied_globally_count",
        "reusable_schema_authorized_count",
        "preapproved_schema_authorized_count",
        "validator_registry_entry_created_count",
        "future_automatic_use_allowed_count",
        "typing_rule_applied_count",
        "field_policy_modified_count",
        "candidate_artifact_modified_count",
        "source_row_locator_applied_count",
        "dominance_rule_applied_count",
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_profile_v0",
        "profile_id": "proposal_branch_one_time_application_profile_" + sha8(rollup),
        "status": status,
        "one_time_application_unit_executed": application_executed,
        "proposal_hold_released": hold_released,
        "rebinds_applied": application_executed,
        "applied_rebind_count": rebinds_applied_count,
        "proposal_binding_count": proposal_binding_count,
        "application_scope_guard_pass": application_executed and rebinds_applied_count == 4,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The authorized one-time application unit released the proposal hold and applied exactly the four authorized source-ref rebinds as an applied rebind ledger. It preserved the 22 ambiguity and 498 requirement-gap branches and did not authorize schema reuse, populate values or metadata, patch runtime, open C5, or use latest/mtime selection.",
        "proposal_binding_count": proposal_binding_count,
        "applied_rebind_count": rebinds_applied_count,
        "proposal_hold_released_count": rollup["proposal_hold_released_count"],
        "metadata_populated_count": 0,
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    trace = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_transition_trace_v0",
        "trace": [
            {
                "step": "consume_application_decision",
                "question": "is one-time application authorized",
                "answer": "yes" if not failures else "no",
                "taken": "build application scope guard",
            },
            {
                "step": "release_hold",
                "question": "may hold be released inside this unit",
                "answer": "yes" if hold_released else "no",
                "taken": "release hold for four authorized proposal rebinds only",
            },
            {
                "step": "apply_rebinds",
                "question": "which rebinds are applied",
                "answer": "exactly four authorized proposal rebinds" if application_executed else "none",
                "taken": "materialize applied rebind table and ledger",
            },
            {
                "step": "preserve_boundaries",
                "question": "were values/metadata/runtime/C5/schema reuse touched",
                "answer": "no",
                "taken": "emit nonmetadata and nonreuse boundary",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(APPLICATION_PLAN_PATH, application_plan)
    write_json(SCOPE_GUARD_PATH, scope_guard)
    write_json(HOLD_RELEASE_RECORD_PATH, hold_release_record)
    write_json(APPLIED_REBIND_TABLE_PATH, applied_rebind_table)
    write_json(APPLIED_REBIND_LEDGER_PATH, applied_rebind_ledger)
    write_json(APPLIED_REBIND_INDEX_PATH, applied_rebind_index)
    write_json(RESIDUAL_BRANCH_PRESERVATION_PATH, residual_preservation)
    write_json(NONREUSE_BOUNDARY_PATH, nonreuse_boundary)
    write_json(NONMETADATA_BOUNDARY_PATH, nonmetadata_boundary)
    write_json(POST_APPLICATION_STATE_PATH, post_application_state)
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
        "ONE_TIME_APP_0_SOURCE_DECISION_RECEIPT_CONSUMED": SOURCE_APP_DECISION_RECEIPT_PATH.exists(),
        "ONE_TIME_APP_1_APPLICATION_PLAN_EMITTED": APPLICATION_PLAN_PATH.exists(),
        "ONE_TIME_APP_2_SCOPE_GUARD_PASS": scope_guard["scope_guard_status"] == "SCOPE_GUARD_PASS",
        "ONE_TIME_APP_3_HOLD_RELEASED_INSIDE_AUTHORIZED_UNIT": hold_release_record["hold_released"] is True,
        "ONE_TIME_APP_4_FOUR_REBINDS_APPLIED": rebinds_applied_count == 4,
        "ONE_TIME_APP_5_APPLIED_REBIND_LEDGER_EMITTED": APPLIED_REBIND_LEDGER_PATH.exists(),
        "ONE_TIME_APP_6_RESIDUAL_AMBIGUITY_BRANCH_PRESERVED": ambiguity_binding_count == 22,
        "ONE_TIME_APP_7_RESIDUAL_REQUIREMENT_GAP_BRANCH_PRESERVED": requirement_gap_binding_count == 498,
        "ONE_TIME_APP_8_NO_SCOPE_EXPANSION": scope_guard["scope_expansion_detected"] is False,
        "ONE_TIME_APP_9_NO_GLOBAL_SCHEMA_APPLICATION": rollup["schema_overlay_applied_globally_count"] == 0,
        "ONE_TIME_APP_10_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "ONE_TIME_APP_11_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "ONE_TIME_APP_12_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "ONE_TIME_APP_13_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "ONE_TIME_APP_14_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "ONE_TIME_APP_15_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "ONE_TIME_APP_16_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "ONE_TIME_APP_17_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "ONE_TIME_APP_18_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "ONE_TIME_APP_19_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "ONE_TIME_APP_20_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "ONE_TIME_APP_21_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "ONE_TIME_APP_22_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "ONE_TIME_APP_23_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "accepted_schema_overlay_reference_this_application_contract_only",
        "ONE_TIME_APP_24_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "application_executed": application_executed,
        "hold_released": hold_released,
        "applied_rebind_count": rebinds_applied_count,
        "metadata": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_application_decision_receipt_id": SOURCE_APP_DECISION_RECEIPT_ID,
        "machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "one_time_application_unit_executed": application_executed,
            "proposal_hold_released": hold_released,
            "rebinds_applied": application_executed,
            "applied_rebind_count": rebinds_applied_count,
            "proposal_binding_count": proposal_binding_count,
            "application_scope_guard_pass": application_executed and rebinds_applied_count == 4,
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
            "application_plan": rel(APPLICATION_PLAN_PATH),
            "scope_guard": rel(SCOPE_GUARD_PATH),
            "hold_release_record": rel(HOLD_RELEASE_RECORD_PATH),
            "applied_rebind_table": rel(APPLIED_REBIND_TABLE_PATH),
            "applied_rebind_ledger": rel(APPLIED_REBIND_LEDGER_PATH),
            "applied_rebind_index": rel(APPLIED_REBIND_INDEX_PATH),
            "residual_branch_preservation": rel(RESIDUAL_BRANCH_PRESERVATION_PATH),
            "nonreuse_boundary": rel(NONREUSE_BOUNDARY_PATH),
            "nonmetadata_boundary": rel(NONMETADATA_BOUNDARY_PATH),
            "post_application_state": rel(POST_APPLICATION_STATE_PATH),
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
    print(f"one_time_application_receipt_id={receipt_id}")
    print(f"one_time_application_receipt_path={rel(receipt_path)}")
    print(f"one_time_application_plan_path={rel(APPLICATION_PLAN_PATH)}")
    print(f"one_time_application_scope_guard_path={rel(SCOPE_GUARD_PATH)}")
    print(f"one_time_application_hold_release_record_path={rel(HOLD_RELEASE_RECORD_PATH)}")
    print(f"one_time_application_applied_rebind_table_path={rel(APPLIED_REBIND_TABLE_PATH)}")
    print(f"one_time_application_applied_rebind_ledger_path={rel(APPLIED_REBIND_LEDGER_PATH)}")
    print(f"one_time_application_post_application_state_path={rel(POST_APPLICATION_STATE_PATH)}")
    print(f"one_time_application_rollup_path={rel(ROLLUP_PATH)}")
    print(f"one_time_application_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
