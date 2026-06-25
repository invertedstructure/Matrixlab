#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_REVIEW"
MODE = "ONE_TIME_APPLICATION_REVIEW / VERIFY_APPLIED_REBINDS / STOP_AT_NEXT_OBJECTIVE_DECISION"
BUILD_MODE = "PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_REVIEW_ONLY"

SOURCE_ONE_TIME_APP_RECEIPT_ID = "4086e0bb"
SOURCE_ONE_TIME_APP_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0_receipts/4086e0bb.json"
SOURCE_APPLICATION_PLAN_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_plan_v0.json"
SOURCE_SCOPE_GUARD_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_scope_guard_v0.json"
SOURCE_HOLD_RELEASE_RECORD_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_hold_release_record_v0.json"
SOURCE_APPLIED_REBIND_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_applied_rebind_table_v0.json"
SOURCE_APPLIED_REBIND_LEDGER_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_applied_rebind_ledger_v0.json"
SOURCE_APPLIED_REBIND_INDEX_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_applied_rebind_index_v0.json"
SOURCE_RESIDUAL_BRANCH_PRESERVATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_residual_branch_preservation_v0.json"
SOURCE_NONREUSE_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_nonreuse_boundary_v0.json"
SOURCE_NONMETADATA_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_nonmetadata_boundary_v0.json"
SOURCE_POST_APPLICATION_STATE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_post_application_state_v0.json"
SOURCE_DOWNSTREAM_DECISION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_downstream_table_v0.json"
SOURCE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_classification_v0.json"
SOURCE_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_authority_boundary_v0.json"
SOURCE_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_rollup_v0.json"
SOURCE_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_profile_v0.json"
SOURCE_APPLICATION_DECISION_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0_receipts/f549ad67.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_assessment_v0.json"
APPLIED_SCOPE_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_applied_scope_review_v0.json"
APPLIED_LEDGER_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_applied_ledger_review_v0.json"
APPLIED_INDEX_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_applied_index_review_v0.json"
HOLD_RELEASE_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_hold_release_review_v0.json"
RESIDUAL_BRANCH_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_residual_branch_review_v0.json"
NONREUSE_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_nonreuse_review_v0.json"
NONMETADATA_REVIEW_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_nonmetadata_review_v0.json"
CLOSURE_CANDIDATE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_closure_candidate_v0.json"
NEXT_OBJECTIVE_DECISION_SURFACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_next_objective_decision_surface_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_downstream_table_v0.json"
REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_packet_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_ONE_TIME_APP_RECEIPT_PATH,
    SOURCE_APPLICATION_PLAN_PATH,
    SOURCE_SCOPE_GUARD_PATH,
    SOURCE_HOLD_RELEASE_RECORD_PATH,
    SOURCE_APPLIED_REBIND_TABLE_PATH,
    SOURCE_APPLIED_REBIND_LEDGER_PATH,
    SOURCE_APPLIED_REBIND_INDEX_PATH,
    SOURCE_RESIDUAL_BRANCH_PRESERVATION_PATH,
    SOURCE_NONREUSE_BOUNDARY_PATH,
    SOURCE_NONMETADATA_BOUNDARY_PATH,
    SOURCE_POST_APPLICATION_STATE_PATH,
    SOURCE_DOWNSTREAM_DECISION_TABLE_PATH,
    SOURCE_CLASSIFICATION_PATH,
    SOURCE_AUTHORITY_BOUNDARY_PATH,
    SOURCE_ROLLUP_PATH,
    SOURCE_PROFILE_PATH,
    SOURCE_APPLICATION_DECISION_RECEIPT_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_APPLIED_REVIEW_REQUIRED"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_APPLIED_REVIEW_REQUIRED"
EXPECTED_SOURCE_NEXT = "REVIEW_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_V0"

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

    receipt = read_json(SOURCE_ONE_TIME_APP_RECEIPT_PATH)
    summary = receipt.get("machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_summary", {})
    plan = read_json(SOURCE_APPLICATION_PLAN_PATH)
    scope = read_json(SOURCE_SCOPE_GUARD_PATH)
    hold = read_json(SOURCE_HOLD_RELEASE_RECORD_PATH)
    table = read_json(SOURCE_APPLIED_REBIND_TABLE_PATH)
    ledger = read_json(SOURCE_APPLIED_REBIND_LEDGER_PATH)
    index = read_json(SOURCE_APPLIED_REBIND_INDEX_PATH)
    residual = read_json(SOURCE_RESIDUAL_BRANCH_PRESERVATION_PATH)
    nonreuse = read_json(SOURCE_NONREUSE_BOUNDARY_PATH)
    nonmeta = read_json(SOURCE_NONMETADATA_BOUNDARY_PATH)
    post = read_json(SOURCE_POST_APPLICATION_STATE_PATH)
    downstream = read_json(SOURCE_DOWNSTREAM_DECISION_TABLE_PATH)
    classif = read_json(SOURCE_CLASSIFICATION_PATH)
    authority = read_json(SOURCE_AUTHORITY_BOUNDARY_PATH)
    rollup = read_json(SOURCE_ROLLUP_PATH)
    profile = read_json(SOURCE_PROFILE_PATH)
    decision_receipt = read_json(SOURCE_APPLICATION_DECISION_RECEIPT_PATH)

    if receipt.get("receipt_id") != SOURCE_ONE_TIME_APP_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_one_time_application_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_terminal_not_expected")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "one_time_application_unit_executed",
        "proposal_hold_released",
        "rebinds_applied",
        "application_scope_guard_pass",
        "schema_overlay_applied_for_this_contract",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "applied_rebind_count": 4,
        "proposal_binding_count": 4,
        "ambiguity_binding_count_preserved": 22,
        "requirement_gap_binding_count_preserved": 498,
        "ready_discriminator_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

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

    if plan.get("application_executed") is not True or plan.get("applied_rebind_count") != 4:
        failures.append("plan_not_executed_4")
    if scope.get("scope_guard_status") != "SCOPE_GUARD_PASS":
        failures.append("scope_guard_not_pass")
    if scope.get("scope_expansion_detected") is not False:
        failures.append("scope_expansion_detected")
    if hold.get("hold_release_status") != "PROPOSAL_HOLD_RELEASED_INSIDE_AUTHORIZED_APPLICATION_UNIT":
        failures.append("hold_release_status_wrong")
    if hold.get("hold_released") is not True:
        failures.append("hold_not_released")

    applied_rows = records(table)
    if table.get("applied_rebind_count") != 4 or len(applied_rows) != 4:
        failures.append(f"applied_table_not_4:{table.get('applied_rebind_count')}:{len(applied_rows)}")
    if any(r.get("applied") is not True for r in applied_rows):
        failures.append("applied_table_contains_unapplied_row")
    if any(r.get("values_authorized") is not False or r.get("metadata_populated") is not False or r.get("runtime_patch_applied") is not False for r in applied_rows):
        failures.append("applied_row_moved_forbidden_layer")
    applied_ids = [r.get("applied_rebind_id") for r in applied_rows]
    if len(set(applied_ids)) != 4:
        failures.append("applied_rebind_ids_not_unique")
    if ledger.get("applied_rebind_count") != 4:
        failures.append("ledger_applied_count_not_4")
    if sorted(ledger.get("applied_rebind_ids", [])) != sorted(applied_ids):
        failures.append("ledger_ids_do_not_match_table")
    if ledger.get("authorizes_future_use") is not False:
        failures.append("ledger_authorizes_future_use")
    if index.get("applied_rebind_count") != 4:
        failures.append("index_count_not_4")
    if len(index.get("by_binding_key", {})) != 4:
        failures.append("index_binding_key_count_not_4")

    if residual.get("ambiguity_binding_count_preserved") != 22 or residual.get("requirement_gap_binding_count_preserved") != 498:
        failures.append("residual_counts_wrong")
    if residual.get("ambiguity_branch_applied") is not False or residual.get("requirement_gap_branch_applied") is not False:
        failures.append("residual_branch_applied")
    for key in ["schema_overlay_applied_globally", "reusable_schema_authorized", "preapproved_schema_authorized", "validator_registry_entry_created", "future_automatic_use_allowed"]:
        if nonreuse.get(key) is not False:
            failures.append(f"nonreuse_true:{key}")
    for key in ["values_authorized", "values_applied", "metadata_populated", "target_selected_for_build", "runtime_patch_applied", "c5_opened"]:
        if nonmeta.get(key) is not False:
            failures.append(f"nonmetadata_true:{key}")
    if post.get("post_application_status") != "FOUR_SOURCE_REF_REBINDS_APPLIED_REVIEW_REQUIRED":
        failures.append("post_application_state_wrong")
    if not any(isinstance(r, dict) and r.get("decision") == "REVIEW_ONE_TIME_APPLICATION_UNIT" and r.get("selected") is True for r in downstream.get("records", [])):
        failures.append("downstream_does_not_select_review")
    if classif.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append("classification_next_wrong")
    if authority.get("may_review_one_time_application_next") is not True:
        failures.append("authority_does_not_allow_review")
    if rollup.get("rebinds_applied_count") != 4:
        failures.append("rollup_rebind_count_not_4")
    if rollup.get("metadata_populated_count") != 0:
        failures.append("rollup_metadata_nonzero")
    if profile.get("applied_rebind_count") != 4:
        failures.append("profile_rebind_count_not_4")
    if decision_receipt.get("receipt_id") != "f549ad67":
        failures.append("decision_receipt_wrong")

    return failures, {
        "summary": summary,
        "applied_rows": applied_rows,
        "ledger": ledger,
        "index": index,
        "scope": scope,
        "hold": hold,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    summary = src.get("summary", {})
    applied_rows = src.get("applied_rows", [])
    applied_rebind_count = len(applied_rows)
    proposal_binding_count = int(summary.get("proposal_binding_count", 0) or 0)
    ambiguity_binding_count = int(summary.get("ambiguity_binding_count_preserved", 0) or 0)
    requirement_gap_binding_count = int(summary.get("requirement_gap_binding_count_preserved", 0) or 0)

    if failures:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_REVIEW_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_REVIEW_BASIS_V0"
        review_pass = False
    else:
        status = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_REVIEWED_CLEAN_NEXT_OBJECTIVE_DECISION_REQUIRED"
        reason_codes = [
            "ONE_TIME_APPLICATION_UNIT_REVIEW_COMPLETE",
            "ONE_TIME_APPLICATION_UNIT_REVIEW_PASS",
            "APPLIED_SCOPE_REVIEW_PASS",
            "APPLIED_REBIND_LEDGER_REVIEW_PASS",
            "APPLIED_REBIND_INDEX_REVIEW_PASS",
            "HOLD_RELEASE_REVIEW_PASS",
            "RESIDUAL_BRANCH_PRESERVATION_REVIEW_PASS",
            "NONREUSE_BOUNDARY_REVIEW_PASS",
            "NONMETADATA_BOUNDARY_REVIEW_PASS",
            "SOURCE_REF_REBIND_LAYER_CLOSURE_CANDIDATE_EMITTED",
            "NEXT_OBJECTIVE_DECISION_REQUIRED",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
            "NO_RUNTIME_PATCH_APPLIED",
            "NO_C5_OPENED",
        ]
        next_edge = "DECIDE_AFTER_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_REVIEW_V0"
        review_pass = True

    review_assessment = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_assessment_v0",
        "assessment_status": status,
        "source_one_time_application_receipt_id": SOURCE_ONE_TIME_APP_RECEIPT_ID,
        "one_time_application_review_complete": not bool(failures),
        "one_time_application_review_pass": review_pass,
        "applied_rebind_count": applied_rebind_count,
        "proposal_binding_count": proposal_binding_count,
        "next_objective_decision_required": review_pass,
        "recommended_next": next_edge,
    }

    applied_scope_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_applied_scope_review_v0",
        "review_status": "APPLIED_SCOPE_REVIEW_PASS" if review_pass else "APPLIED_SCOPE_REVIEW_REPAIR_REQUIRED",
        "authorized_scope_count": 4,
        "applied_rebind_count": applied_rebind_count,
        "proposal_binding_count": proposal_binding_count,
        "scope_expansion_detected": False,
        "applied_only_authorized_proposal_rebinds": review_pass and applied_rebind_count == 4,
        "excluded_ambiguity_binding_count": ambiguity_binding_count,
        "excluded_requirement_gap_binding_count": requirement_gap_binding_count,
    }

    applied_ledger_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_applied_ledger_review_v0",
        "review_status": "APPLIED_REBIND_LEDGER_REVIEW_PASS" if review_pass else "APPLIED_REBIND_LEDGER_REVIEW_REPAIR_REQUIRED",
        "applied_rebind_count": applied_rebind_count,
        "applied_rebind_ids": [r.get("applied_rebind_id") for r in applied_rows],
        "ledger_coherent": review_pass,
        "authorizes_future_use": False,
    }

    applied_index_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_applied_index_review_v0",
        "review_status": "APPLIED_REBIND_INDEX_REVIEW_PASS" if review_pass else "APPLIED_REBIND_INDEX_REVIEW_REPAIR_REQUIRED",
        "binding_index_count": applied_rebind_count,
        "candidate_index_count": applied_rebind_count,
        "index_matches_applied_table": review_pass,
    }

    hold_release_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_hold_release_review_v0",
        "review_status": "HOLD_RELEASE_REVIEW_PASS" if review_pass else "HOLD_RELEASE_REVIEW_REPAIR_REQUIRED",
        "hold_released_inside_authorized_application_unit": review_pass,
        "hold_release_scope": "four authorized proposal rebinds only",
        "hold_release_did_not_authorize_schema_reuse": True,
    }

    residual_branch_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_residual_branch_review_v0",
        "review_status": "RESIDUAL_BRANCH_PRESERVATION_REVIEW_PASS" if review_pass else "RESIDUAL_BRANCH_PRESERVATION_REVIEW_REPAIR_REQUIRED",
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "ambiguity_branch_applied": False,
        "requirement_gap_branch_applied": False,
        "may_discard_residual_branches": False,
    }

    nonreuse_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_nonreuse_review_v0",
        "review_status": "NONREUSE_BOUNDARY_REVIEW_PASS" if review_pass else "NONREUSE_BOUNDARY_REVIEW_REPAIR_REQUIRED",
        "schema_overlay_applied_for_this_contract": True,
        "schema_overlay_applied_globally": False,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
    }

    nonmetadata_review = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_nonmetadata_review_v0",
        "review_status": "NONMETADATA_BOUNDARY_REVIEW_PASS" if review_pass else "NONMETADATA_BOUNDARY_REVIEW_REPAIR_REQUIRED",
        "source_ref_rebind_layer_applied": review_pass,
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

    closure_candidate = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_closure_candidate_v0",
        "closure_candidate_status": "SOURCE_REF_REBIND_LAYER_CLOSURE_CANDIDATE_READY" if review_pass else "SOURCE_REF_REBIND_LAYER_CLOSURE_CANDIDATE_NOT_READY",
        "source_ref_rebind_application_review_pass": review_pass,
        "applied_rebind_count": applied_rebind_count,
        "remaining_residual_branches": {
            "ambiguity_binding_count": ambiguity_binding_count,
            "requirement_gap_binding_count": requirement_gap_binding_count,
        },
        "closure_meaning": "the authorized 4-proposal source-ref rebind branch may be closed as applied and reviewed",
        "closure_does_not_mean": [
            "metadata populated",
            "values authorized",
            "runtime patch ready",
            "C5 opened",
            "schema made reusable",
            "ambiguity/gap branches discarded",
        ],
    }

    next_objective_decision_surface = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_next_objective_decision_surface_v0",
        "decision_surface_status": "NEXT_OBJECTIVE_DECISION_REQUIRED" if review_pass else "NEXT_OBJECTIVE_DECISION_NOT_READY",
        "decision_not_recorded": True,
        "available_decisions": [
            "CLOSE_SOURCE_REF_REBIND_LAYER_AS_REVIEWED_REFERENCE",
            "MOVE_TO_METADATA_OR_VALUE_POPULATION_PRECHECK",
            "RETURN_TO_AMBIGUITY_BRANCH_REPAIR",
            "RETURN_TO_REQUIREMENT_GAP_BRANCH_REPAIR",
        ],
        "recommended_default": "CLOSE_SOURCE_REF_REBIND_LAYER_AS_REVIEWED_REFERENCE",
        "why_default": "the one-time source-ref rebind branch is applied and reviewed; metadata/value population is a separate objective and should not be entered automatically",
    }

    downstream_decision_table = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_downstream_table_v0",
        "decision_status": "ONE_TIME_APPLICATION_REVIEW_DOWNSTREAM_DECISION_EMITTED",
        "records": [
            {
                "decision": "DECIDE_NEXT_OBJECTIVE",
                "selected": review_pass,
                "next_unit": "DECIDE_AFTER_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_REVIEW_V0" if review_pass else None,
                "why": "application review passed, but next objective must be explicitly selected",
            },
            {
                "decision": "POPULATE_METADATA_NOW",
                "selected": False,
                "next_unit": None,
                "why": "metadata population requires a separate objective/precheck",
            },
            {
                "decision": "PATCH_RUNTIME_NOW",
                "selected": False,
                "next_unit": None,
                "why": "runtime patch remains out of scope",
            },
        ],
    }

    review_packet = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_packet_v0",
        "review_packet_status": status,
        "summary": {
            "one_time_application_review_pass": review_pass,
            "applied_rebind_count": applied_rebind_count,
            "proposal_hold_release_review_pass": review_pass,
            "source_ref_rebind_layer_closure_candidate_ready": review_pass,
            "next_objective_decision_required": review_pass,
            "values_authorized": False,
            "metadata_populated": False,
            "runtime_patch_applied": False,
            "c5_opened": False,
        },
        "recommended_next": next_edge,
    }

    classification = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "one_time_application_review_complete": not bool(failures),
        "one_time_application_review_pass": review_pass,
        "applied_rebind_count": applied_rebind_count,
        "proposal_binding_count": proposal_binding_count,
        "application_scope_guard_review_pass": review_pass,
        "applied_rebind_ledger_review_pass": review_pass,
        "hold_release_review_pass": review_pass,
        "source_ref_rebind_layer_closure_candidate_ready": review_pass,
        "next_objective_decision_required": review_pass,
        "next_objective_decision_recorded": False,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_authority_boundary_v0",
        "status": status,
        "may_decide_next_objective": review_pass,
        "may_close_source_ref_rebind_layer": False,
        "may_start_metadata_population_now": False,
        "may_apply_more_rebinds": False,
        "may_apply_ambiguity_branch": False,
        "may_apply_requirement_gap_branch": False,
        "may_authorize_values": False,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "one_time_application_review_count": 1,
        "one_time_application_review_pass_count": 1 if review_pass else 0,
        "applied_rebind_count": applied_rebind_count,
        "proposal_binding_count": proposal_binding_count,
        "source_ref_rebind_layer_closure_candidate_count": 1 if review_pass else 0,
        "next_objective_decision_required_count": 1 if review_pass else 0,
        "next_objective_decision_recorded_count": 0,
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
        "next_objective_decision_recorded_count",
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_profile_v0",
        "profile_id": "proposal_branch_one_time_application_review_profile_" + sha8(rollup),
        "status": status,
        "one_time_application_review_pass": review_pass,
        "applied_rebind_count": applied_rebind_count,
        "proposal_binding_count": proposal_binding_count,
        "source_ref_rebind_layer_closure_candidate_ready": review_pass,
        "next_objective_decision_required": review_pass,
        "next_objective_decision_recorded": False,
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
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The one-time application unit review passed. Exactly four authorized source-ref rebinds were applied, the applied ledger/index are coherent, the hold release stayed inside the authorized application unit, the 22 ambiguity and 498 requirement-gap branches remain preserved, and no values, metadata, runtime patch, C5, schema reuse, latest-file, or mtime boundary moved.",
        "applied_rebind_count": applied_rebind_count,
        "source_ref_rebind_layer_closure_candidate_ready": review_pass,
        "next_objective_decision_required": review_pass,
        "metadata_populated_count": 0,
        "runtime_patch_applied_count": 0,
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    trace = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_application_receipt",
                "question": "did the one-time application execute under authorized scope",
                "answer": "yes" if review_pass else "no",
                "taken": "review applied scope and ledger",
            },
            {
                "step": "verify_boundaries",
                "question": "did values/metadata/runtime/C5/schema reuse move",
                "answer": "no",
                "taken": "emit nonmetadata and nonreuse reviews",
            },
            {
                "step": "emit_next_decision_surface",
                "question": "what happens after source-ref rebind application review",
                "answer": "explicit next-objective decision required",
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
    write_json(APPLIED_SCOPE_REVIEW_PATH, applied_scope_review)
    write_json(APPLIED_LEDGER_REVIEW_PATH, applied_ledger_review)
    write_json(APPLIED_INDEX_REVIEW_PATH, applied_index_review)
    write_json(HOLD_RELEASE_REVIEW_PATH, hold_release_review)
    write_json(RESIDUAL_BRANCH_REVIEW_PATH, residual_branch_review)
    write_json(NONREUSE_REVIEW_PATH, nonreuse_review)
    write_json(NONMETADATA_REVIEW_PATH, nonmetadata_review)
    write_json(CLOSURE_CANDIDATE_PATH, closure_candidate)
    write_json(NEXT_OBJECTIVE_DECISION_SURFACE_PATH, next_objective_decision_surface)
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
        "ONE_TIME_APP_REVIEW_0_SOURCE_RECEIPT_CONSUMED": SOURCE_ONE_TIME_APP_RECEIPT_PATH.exists(),
        "ONE_TIME_APP_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "ONE_TIME_APP_REVIEW_2_APPLIED_SCOPE_REVIEW_PASS": applied_scope_review["review_status"] == "APPLIED_SCOPE_REVIEW_PASS",
        "ONE_TIME_APP_REVIEW_3_LEDGER_REVIEW_PASS": applied_ledger_review["review_status"] == "APPLIED_REBIND_LEDGER_REVIEW_PASS",
        "ONE_TIME_APP_REVIEW_4_INDEX_REVIEW_PASS": applied_index_review["review_status"] == "APPLIED_REBIND_INDEX_REVIEW_PASS",
        "ONE_TIME_APP_REVIEW_5_HOLD_RELEASE_REVIEW_PASS": hold_release_review["review_status"] == "HOLD_RELEASE_REVIEW_PASS",
        "ONE_TIME_APP_REVIEW_6_RESIDUAL_BRANCH_REVIEW_PASS": residual_branch_review["review_status"] == "RESIDUAL_BRANCH_PRESERVATION_REVIEW_PASS",
        "ONE_TIME_APP_REVIEW_7_NONREUSE_REVIEW_PASS": nonreuse_review["review_status"] == "NONREUSE_BOUNDARY_REVIEW_PASS",
        "ONE_TIME_APP_REVIEW_8_NONMETADATA_REVIEW_PASS": nonmetadata_review["review_status"] == "NONMETADATA_BOUNDARY_REVIEW_PASS",
        "ONE_TIME_APP_REVIEW_9_FOUR_REBINDS_REVIEWED": applied_rebind_count == 4,
        "ONE_TIME_APP_REVIEW_10_RESIDUAL_AMBIGUITY_BRANCH_PRESERVED": ambiguity_binding_count == 22,
        "ONE_TIME_APP_REVIEW_11_RESIDUAL_REQUIREMENT_GAP_BRANCH_PRESERVED": requirement_gap_binding_count == 498,
        "ONE_TIME_APP_REVIEW_12_CLOSURE_CANDIDATE_EMITTED": CLOSURE_CANDIDATE_PATH.exists(),
        "ONE_TIME_APP_REVIEW_13_NEXT_OBJECTIVE_DECISION_REQUIRED": next_objective_decision_surface["decision_surface_status"] == "NEXT_OBJECTIVE_DECISION_REQUIRED",
        "ONE_TIME_APP_REVIEW_14_NO_NEXT_OBJECTIVE_DECISION_RECORDED": rollup["next_objective_decision_recorded_count"] == 0,
        "ONE_TIME_APP_REVIEW_15_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "ONE_TIME_APP_REVIEW_16_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "ONE_TIME_APP_REVIEW_17_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "ONE_TIME_APP_REVIEW_18_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "ONE_TIME_APP_REVIEW_19_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "ONE_TIME_APP_REVIEW_20_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "ONE_TIME_APP_REVIEW_21_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "ONE_TIME_APP_REVIEW_22_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "ONE_TIME_APP_REVIEW_23_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "ONE_TIME_APP_REVIEW_24_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "ONE_TIME_APP_REVIEW_25_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "ONE_TIME_APP_REVIEW_26_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "ONE_TIME_APP_REVIEW_27_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "ONE_TIME_APP_REVIEW_28_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "accepted_schema_overlay_reference_this_application_contract_only",
        "ONE_TIME_APP_REVIEW_29_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "review_pass": review_pass,
        "applied_rebind_count": applied_rebind_count,
        "metadata": 0,
        "next_decision": "required",
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_one_time_application_receipt_id": SOURCE_ONE_TIME_APP_RECEIPT_ID,
        "machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "one_time_application_review_complete": not bool(failures),
            "one_time_application_review_pass": review_pass,
            "applied_rebind_count": applied_rebind_count,
            "proposal_binding_count": proposal_binding_count,
            "application_scope_guard_review_pass": review_pass,
            "applied_rebind_ledger_review_pass": review_pass,
            "hold_release_review_pass": review_pass,
            "source_ref_rebind_layer_closure_candidate_ready": review_pass,
            "next_objective_decision_required": review_pass,
            "next_objective_decision_recorded": False,
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
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "applied_scope_review": rel(APPLIED_SCOPE_REVIEW_PATH),
            "applied_ledger_review": rel(APPLIED_LEDGER_REVIEW_PATH),
            "applied_index_review": rel(APPLIED_INDEX_REVIEW_PATH),
            "hold_release_review": rel(HOLD_RELEASE_REVIEW_PATH),
            "residual_branch_review": rel(RESIDUAL_BRANCH_REVIEW_PATH),
            "nonreuse_review": rel(NONREUSE_REVIEW_PATH),
            "nonmetadata_review": rel(NONMETADATA_REVIEW_PATH),
            "closure_candidate": rel(CLOSURE_CANDIDATE_PATH),
            "next_objective_decision_surface": rel(NEXT_OBJECTIVE_DECISION_SURFACE_PATH),
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
    print(f"one_time_application_review_receipt_id={receipt_id}")
    print(f"one_time_application_review_receipt_path={rel(receipt_path)}")
    print(f"one_time_application_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"one_time_application_applied_scope_review_path={rel(APPLIED_SCOPE_REVIEW_PATH)}")
    print(f"one_time_application_applied_ledger_review_path={rel(APPLIED_LEDGER_REVIEW_PATH)}")
    print(f"one_time_application_hold_release_review_path={rel(HOLD_RELEASE_REVIEW_PATH)}")
    print(f"one_time_application_closure_candidate_path={rel(CLOSURE_CANDIDATE_PATH)}")
    print(f"one_time_application_next_objective_decision_surface_path={rel(NEXT_OBJECTIVE_DECISION_SURFACE_PATH)}")
    print(f"one_time_application_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"one_time_application_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
