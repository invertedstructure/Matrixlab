#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_SOURCE_REF_REBIND_LAYER_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind.source_ref_layer_closure.v0"
LAYER = "CELL_1 / SOURCE_REF_REBIND_LAYER_CLOSURE"
MODE = "CLOSURE / REVIEWED_REFERENCE_FREEZE / POST_UPDATE_DECISION_READY"
BUILD_MODE = "SOURCE_REF_REBIND_LAYER_CLOSURE_ONLY"

SOURCE_REVIEW_RECEIPT_ID = "b3bcc049"
SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0_receipts/b3bcc049.json"
SOURCE_REVIEW_ASSESSMENT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_assessment_v0.json"
SOURCE_APPLIED_SCOPE_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_applied_scope_review_v0.json"
SOURCE_APPLIED_LEDGER_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_applied_ledger_review_v0.json"
SOURCE_APPLIED_INDEX_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_applied_index_review_v0.json"
SOURCE_HOLD_RELEASE_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_hold_release_review_v0.json"
SOURCE_RESIDUAL_BRANCH_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_residual_branch_review_v0.json"
SOURCE_NONREUSE_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_nonreuse_review_v0.json"
SOURCE_NONMETADATA_REVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_nonmetadata_review_v0.json"
SOURCE_CLOSURE_CANDIDATE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_closure_candidate_v0.json"
SOURCE_NEXT_OBJECTIVE_DECISION_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_next_objective_decision_surface_v0.json"
SOURCE_DOWNSTREAM_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_downstream_table_v0.json"
SOURCE_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_packet_v0.json"
SOURCE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_classification_v0.json"
SOURCE_AUTHORITY_BOUNDARY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_authority_boundary_v0.json"
SOURCE_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_rollup_v0.json"
SOURCE_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_review_v0/typed_machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_profile_v0.json"
SOURCE_ONE_TIME_APP_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_one_time_application_unit_v0_receipts/4086e0bb.json"
SOURCE_APP_DECISION_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_proposal_branch_application_decision_v0_receipts/f549ad67.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_partial_schema_aware_rebind_source_ref_layer_closure_v0_receipts"

CLOSURE_RECORD_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_layer_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_layer_reviewed_reference_v0.json"
REFERENCE_FREEZE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_layer_reference_freeze_v0.json"
RECEIPT_CHAIN_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_layer_closure_receipt_chain_v0.json"
BOUNDARY_LOCK_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_layer_closure_boundary_lock_v0.json"
RESIDUAL_BRANCH_CARRY_FORWARD_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_layer_residual_branch_carry_forward_v0.json"
POST_CLOSURE_DECISION_SURFACE_PATH = OUT_DIR / "typed_machine_readable_post_source_ref_rebind_closure_decision_surface_v0.json"
POST_UPDATE_SEQUENCE_HINT_PATH = OUT_DIR / "typed_machine_readable_post_closure_observability_feedback_hardening_sequence_hint_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_layer_closure_downstream_decision_table_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_layer_closure_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_layer_closure_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_layer_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_layer_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_layer_closure_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_layer_closure_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_REVIEW_RECEIPT_PATH,
    SOURCE_REVIEW_ASSESSMENT_PATH,
    SOURCE_APPLIED_SCOPE_REVIEW_PATH,
    SOURCE_APPLIED_LEDGER_REVIEW_PATH,
    SOURCE_APPLIED_INDEX_REVIEW_PATH,
    SOURCE_HOLD_RELEASE_REVIEW_PATH,
    SOURCE_RESIDUAL_BRANCH_REVIEW_PATH,
    SOURCE_NONREUSE_REVIEW_PATH,
    SOURCE_NONMETADATA_REVIEW_PATH,
    SOURCE_CLOSURE_CANDIDATE_PATH,
    SOURCE_NEXT_OBJECTIVE_DECISION_SURFACE_PATH,
    SOURCE_DOWNSTREAM_TABLE_PATH,
    SOURCE_REVIEW_PACKET_PATH,
    SOURCE_CLASSIFICATION_PATH,
    SOURCE_AUTHORITY_BOUNDARY_PATH,
    SOURCE_ROLLUP_PATH,
    SOURCE_PROFILE_PATH,
    SOURCE_ONE_TIME_APP_RECEIPT_PATH,
    SOURCE_APP_DECISION_RECEIPT_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_REVIEWED_CLEAN_NEXT_OBJECTIVE_DECISION_REQUIRED"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_UNIT_REVIEWED_CLEAN_NEXT_OBJECTIVE_DECISION_REQUIRED"
EXPECTED_SOURCE_NEXT = "DECIDE_AFTER_PARTIAL_SCHEMA_AWARE_REBIND_PROPOSAL_BRANCH_ONE_TIME_APPLICATION_REVIEW_V0"

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

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(SOURCE_REVIEW_RECEIPT_PATH)
    summary = receipt.get("machine_readable_partial_schema_aware_rebind_proposal_branch_one_time_application_review_summary", {})
    assessment = read_json(SOURCE_REVIEW_ASSESSMENT_PATH)
    applied_scope = read_json(SOURCE_APPLIED_SCOPE_REVIEW_PATH)
    applied_ledger = read_json(SOURCE_APPLIED_LEDGER_REVIEW_PATH)
    applied_index = read_json(SOURCE_APPLIED_INDEX_REVIEW_PATH)
    hold_review = read_json(SOURCE_HOLD_RELEASE_REVIEW_PATH)
    residual_review = read_json(SOURCE_RESIDUAL_BRANCH_REVIEW_PATH)
    nonreuse_review = read_json(SOURCE_NONREUSE_REVIEW_PATH)
    nonmetadata_review = read_json(SOURCE_NONMETADATA_REVIEW_PATH)
    closure_candidate = read_json(SOURCE_CLOSURE_CANDIDATE_PATH)
    next_surface = read_json(SOURCE_NEXT_OBJECTIVE_DECISION_SURFACE_PATH)
    classification = read_json(SOURCE_CLASSIFICATION_PATH)
    rollup = read_json(SOURCE_ROLLUP_PATH)
    profile = read_json(SOURCE_PROFILE_PATH)
    one_time_app_receipt = read_json(SOURCE_ONE_TIME_APP_RECEIPT_PATH)
    app_decision_receipt = read_json(SOURCE_APP_DECISION_RECEIPT_PATH)

    if receipt.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("source_review_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_terminal_not_expected")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "one_time_application_review_complete",
        "one_time_application_review_pass",
        "application_scope_guard_review_pass",
        "applied_rebind_ledger_review_pass",
        "hold_release_review_pass",
        "source_ref_rebind_layer_closure_candidate_ready",
        "next_objective_decision_required",
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
        "next_objective_decision_recorded",
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

    if assessment.get("one_time_application_review_pass") is not True:
        failures.append("assessment_review_not_pass")
    if applied_scope.get("review_status") != "APPLIED_SCOPE_REVIEW_PASS":
        failures.append("applied_scope_not_pass")
    if applied_scope.get("applied_rebind_count") != 4:
        failures.append("applied_scope_count_not_4")
    if applied_ledger.get("review_status") != "APPLIED_REBIND_LEDGER_REVIEW_PASS":
        failures.append("applied_ledger_not_pass")
    if applied_index.get("review_status") != "APPLIED_REBIND_INDEX_REVIEW_PASS":
        failures.append("applied_index_not_pass")
    if hold_review.get("review_status") != "HOLD_RELEASE_REVIEW_PASS":
        failures.append("hold_review_not_pass")
    if residual_review.get("ambiguity_binding_count_preserved") != 22 or residual_review.get("requirement_gap_binding_count_preserved") != 498:
        failures.append("residual_counts_wrong")
    if residual_review.get("ambiguity_branch_applied") is not False or residual_review.get("requirement_gap_branch_applied") is not False:
        failures.append("residual_branch_applied")
    for key in ["schema_overlay_applied_globally", "reusable_schema_authorized", "preapproved_schema_authorized", "validator_registry_entry_created", "future_automatic_use_allowed"]:
        if nonreuse_review.get(key) is not False:
            failures.append(f"nonreuse_true:{key}")
    for key in ["values_authorized", "values_applied", "metadata_populated", "target_selected_for_build", "runtime_patch_applied", "c5_opened"]:
        if nonmetadata_review.get(key) is not False:
            failures.append(f"nonmetadata_true:{key}")
    if closure_candidate.get("closure_candidate_status") != "SOURCE_REF_REBIND_LAYER_CLOSURE_CANDIDATE_READY":
        failures.append("closure_candidate_not_ready")
    if next_surface.get("decision_surface_status") != "NEXT_OBJECTIVE_DECISION_REQUIRED":
        failures.append("next_surface_not_required")
    if next_surface.get("recommended_default") != "CLOSE_SOURCE_REF_REBIND_LAYER_AS_REVIEWED_REFERENCE":
        failures.append("next_surface_recommended_default_wrong")
    if classification.get("next_objective_decision_recorded") is not False:
        failures.append("classification_next_decision_already_recorded")
    if rollup.get("source_ref_rebind_layer_closure_candidate_count") != 1:
        failures.append("rollup_closure_candidate_count_wrong")
    if profile.get("source_ref_rebind_layer_closure_candidate_ready") is not True:
        failures.append("profile_closure_candidate_not_ready")
    if one_time_app_receipt.get("receipt_id") != "4086e0bb":
        failures.append("one_time_app_receipt_wrong")
    if app_decision_receipt.get("receipt_id") != "f549ad67":
        failures.append("app_decision_receipt_wrong")

    return failures, {
        "summary": summary,
        "applied_ledger": applied_ledger,
        "applied_index": applied_index,
        "closure_candidate": closure_candidate,
        "next_surface": next_surface,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    summary = src.get("summary", {})
    applied_rebind_count = int(summary.get("applied_rebind_count", 0) or 0)
    proposal_binding_count = int(summary.get("proposal_binding_count", 0) or 0)
    ambiguity_binding_count = int(summary.get("ambiguity_binding_count_preserved", 0) or 0)
    requirement_gap_binding_count = int(summary.get("requirement_gap_binding_count_preserved", 0) or 0)

    if failures:
        status = "TYPED_SOURCE_REF_REBIND_LAYER_CLOSURE_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_SOURCE_REF_REBIND_LAYER_CLOSURE_BASIS_V0"
        closed = False
    else:
        status = "TYPED_SOURCE_REF_REBIND_LAYER_CLOSED_AS_REVIEWED_REFERENCE_POST_UPDATE_DECISION_READY"
        reason_codes = [
            "SOURCE_REF_REBIND_LAYER_CLOSED_AS_REVIEWED_REFERENCE",
            "ONE_TIME_APPLICATION_REVIEW_CONSUMED",
            "FOUR_APPLIED_REBINDS_FROZEN_AS_REVIEWED_REFERENCE",
            "APPLIED_LEDGER_AND_INDEX_REFERENCE_PRESERVED",
            "RESIDUAL_AMBIGUITY_BRANCH_CARRIED_FORWARD",
            "RESIDUAL_REQUIREMENT_GAP_BRANCH_CARRIED_FORWARD",
            "NONREUSE_BOUNDARY_FROZEN",
            "NONMETADATA_BOUNDARY_FROZEN",
            "NO_NEXT_OBJECTIVE_EXECUTED",
            "POST_UPDATE_DECISION_READY",
            "DECISION_EDGE_OBSERVABILITY_RECOMMENDED_FIRST",
            "UNIT_FEEDBACK_HARDENING_RECOMMENDED_SECOND",
            "NO_VALUES_AUTHORIZED_OR_APPLIED",
            "NO_METADATA_POPULATION",
            "NO_RUNTIME_PATCH_APPLIED",
            "NO_C5_OPENED",
        ]
        next_edge = "DESIGN_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET_V0"
        closed = True

    closure_record = {
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_closure_record_v0",
        "closure_status": "CLOSED_AS_REVIEWED_REFERENCE" if closed else "CLOSURE_NOT_RECORDED",
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "closed_object": "partial_schema_aware_source_ref_rebind_layer",
        "closure_basis": {
            "one_time_application_review_pass": closed,
            "applied_rebind_count": applied_rebind_count,
            "proposal_binding_count": proposal_binding_count,
            "source_ref_rebind_layer_closure_candidate_ready": closed,
        },
        "closure_meaning": "the authorized four source-ref rebinds are applied, reviewed, and frozen as a reference object",
        "closure_does_not_mean": [
            "metadata populated",
            "values authorized",
            "runtime patch ready",
            "C5 opened",
            "schema made reusable",
            "ambiguity branch resolved",
            "requirement-gap branch resolved",
        ],
    }

    reviewed_reference = {
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_reviewed_reference_v0",
        "reference_status": "FROZEN_REVIEWED_REFERENCE" if closed else "REFERENCE_NOT_FROZEN",
        "reference_object_id": "source_ref_rebind_layer_reviewed_reference_" + sha8({
            "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
            "applied_rebind_count": applied_rebind_count,
            "proposal_binding_count": proposal_binding_count,
        }),
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_one_time_application_receipt_id": "4086e0bb",
        "source_application_decision_receipt_id": "f549ad67",
        "applied_rebind_count": applied_rebind_count,
        "proposal_binding_count": proposal_binding_count,
        "reference_use": "future units may cite this as reviewed source-ref rebind context",
        "reference_not_authority_for": [
            "schema reuse",
            "automatic future application",
            "metadata population",
            "value authorization",
            "runtime patching",
            "C5 opening",
        ],
    }

    reference_freeze = {
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_reference_freeze_v0",
        "freeze_status": "FREEZE_COMPLETE" if closed else "FREEZE_NOT_COMPLETE",
        "frozen_reference_path": rel(REVIEWED_REFERENCE_PATH),
        "frozen_receipt_chain_path": rel(RECEIPT_CHAIN_PATH),
        "may_mutate_prior_artifacts": False,
        "may_reopen_without_explicit_new_objective": False,
        "may_treat_as_reusable_schema": False,
    }

    receipt_chain = {
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_closure_receipt_chain_v0",
        "chain_status": "RECEIPT_CHAIN_PRESERVED",
        "receipts": [
            {"stage": "proposal_branch_review", "receipt_id": "2aee3233"},
            {"stage": "authorization_contract_build", "receipt_id": "56454d20"},
            {"stage": "authorization_contract_review", "receipt_id": "a4f000a6"},
            {"stage": "application_decision_record", "receipt_id": "f549ad67"},
            {"stage": "one_time_application_unit", "receipt_id": "4086e0bb"},
            {"stage": "one_time_application_review", "receipt_id": SOURCE_REVIEW_RECEIPT_ID},
        ],
        "closure_receipt_pending": True,
    }

    boundary_lock = {
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_closure_boundary_lock_v0",
        "boundary_lock_status": "BOUNDARIES_LOCKED_AT_CLOSURE",
        "source_ref_rebind_layer_closed": closed,
        "schema_overlay_applied_for_this_contract": True,
        "schema_overlay_applied_globally": False,
        "reusable_schema_authorized": False,
        "preapproved_schema_authorized": False,
        "validator_registry_entry_created": False,
        "future_automatic_use_allowed": False,
        "values_authorized": False,
        "values_applied": False,
        "metadata_populated": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "c5_opened": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
    }

    residual_carry = {
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_residual_branch_carry_forward_v0",
        "carry_forward_status": "RESIDUAL_BRANCHES_CARRIED_FORWARD_UNRESOLVED",
        "ambiguity_binding_count": ambiguity_binding_count,
        "requirement_gap_binding_count": requirement_gap_binding_count,
        "ambiguity_branch_resolved": False,
        "requirement_gap_branch_resolved": False,
        "may_discard_residual_branches": False,
        "may_treat_residual_as_null": False,
        "allowed_future_handling": [
            "explicit ambiguity branch repair objective",
            "explicit requirement-gap branch repair objective",
            "preserve as residual reference while moving to another bounded objective",
        ],
    }

    post_closure_decision_surface = {
        "schema_version": "typed_machine_readable_post_source_ref_rebind_closure_decision_surface_v0",
        "decision_surface_status": "POST_CLOSURE_NEXT_OBJECTIVE_READY",
        "decision_recorded": False,
        "available_decisions": [
            "DESIGN_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET_V0",
            "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0",
            "MOVE_TO_METADATA_OR_VALUE_POPULATION_PRECHECK",
            "RETURN_TO_AMBIGUITY_BRANCH_REPAIR",
            "RETURN_TO_REQUIREMENT_GAP_BRANCH_REPAIR",
        ],
        "recommended_default": "DESIGN_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET_V0",
        "recommended_second": "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0",
        "why_default": "decision-edge observability is a cheap high-value instrumentation upgrade before post-rebind metadata/value work",
    }

    hardening_hint = {
        "schema_version": "typed_machine_readable_post_closure_observability_feedback_hardening_sequence_hint_v0",
        "hint_status": "POST_UPDATE_HARDENING_SEQUENCE_PRESERVED_AS_HINT_NOT_EXECUTED",
        "sequence": [
            {
                "order": 1,
                "target": "decision_edge_observability",
                "purpose": "expose graph-relevant edge fields from receipts",
                "fields": [
                    "active_object",
                    "attempted_move",
                    "boundary_checked",
                    "blocked_move",
                    "lawful_next_move",
                    "capability_boundary",
                    "authority_boundary",
                    "terminal_result",
                ],
                "executed_now": False,
            },
            {
                "order": 2,
                "target": "unit_feedback_hardening",
                "purpose": "make failed or blocked units report useful repair feedback",
                "fields": [
                    "failure_reason",
                    "failure_location",
                    "relative_object",
                    "relative_source_surface",
                    "relative_boundary",
                    "missing_capability",
                    "exact_refinement_needed",
                ],
                "executed_now": False,
            },
        ],
    }

    downstream_decision_table = {
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_closure_downstream_decision_table_v0",
        "decision_status": "SOURCE_REF_REBIND_LAYER_CLOSURE_DOWNSTREAM_TABLE_EMITTED",
        "records": [
            {
                "decision": "DESIGN_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET",
                "selected": closed,
                "next_unit": "DESIGN_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET_V0" if closed else None,
                "why": "source-ref rebind layer is closed; first cheap post-update hardening target is decision-edge observability",
            },
            {
                "decision": "START_METADATA_POPULATION_NOW",
                "selected": False,
                "next_unit": None,
                "why": "metadata/value population is not entered automatically after closure",
            },
            {
                "decision": "REOPEN_SOURCE_REF_REBIND_LAYER",
                "selected": False,
                "next_unit": None,
                "why": "closed reference can be cited, not silently reopened",
            },
        ],
    }

    classification = {
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "source_ref_rebind_layer_closed": closed,
        "closed_as_reviewed_reference": closed,
        "reviewed_reference_emitted": closed,
        "applied_rebind_count": applied_rebind_count,
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "post_closure_next_objective_decision_ready": closed,
        "post_closure_next_objective_executed": False,
        "recommended_next": next_edge,
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
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_closure_authority_boundary_v0",
        "status": status,
        "may_cite_reviewed_reference_in_future_units": closed,
        "may_design_decision_edge_observability_next": closed,
        "may_design_unit_feedback_hardening_next": False,
        "may_start_metadata_population_now": False,
        "may_apply_more_rebinds": False,
        "may_reopen_source_ref_rebind_layer_without_new_objective": False,
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
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_closure_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "source_ref_rebind_layer_closed_count": 1 if closed else 0,
        "reviewed_reference_emitted_count": 1 if closed else 0,
        "applied_rebind_count": applied_rebind_count,
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "post_closure_next_objective_decision_ready_count": 1 if closed else 0,
        "post_closure_next_objective_executed_count": 0,
        "decision_edge_observability_recommended_count": 1 if closed else 0,
        "unit_feedback_hardening_recommended_count": 1 if closed else 0,
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
        "post_closure_next_objective_executed_count",
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
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_closure_profile_v0",
        "profile_id": "source_ref_rebind_layer_closure_profile_" + sha8(rollup),
        "status": status,
        "source_ref_rebind_layer_closed": closed,
        "closed_as_reviewed_reference": closed,
        "reviewed_reference_emitted": closed,
        "applied_rebind_count": applied_rebind_count,
        "proposal_binding_count": proposal_binding_count,
        "ambiguity_binding_count_preserved": ambiguity_binding_count,
        "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
        "post_closure_next_objective_decision_ready": closed,
        "post_closure_next_objective_executed": False,
        "recommended_next": next_edge,
        "recommended_post_update_sequence": [
            "decision_edge_observability",
            "unit_feedback_hardening",
        ],
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
        "next_command_goal": None,
    }

    report = {
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The source-ref rebind layer was closed as a reviewed reference object after the one-time application review passed. Exactly four source-ref rebinds are frozen as reviewed context, the 22 ambiguity and 498 requirement-gap branches are carried forward unresolved, and no values, metadata, runtime patch, C5, reusable schema authority, preapproval, validator registry, latest-file, or mtime boundary moved.",
        "applied_rebind_count": applied_rebind_count,
        "source_ref_rebind_layer_closed_count": rollup["source_ref_rebind_layer_closed_count"],
        "reviewed_reference_emitted_count": rollup["reviewed_reference_emitted_count"],
        "metadata_populated_count": 0,
        "runtime_patch_applied_count": 0,
        "recommended_next_handling": next_edge,
        "recommended_post_update_sequence": [
            "DESIGN_DECISION_EDGE_OBSERVABILITY_HARDENING_TARGET_V0",
            "DESIGN_UNIT_FEEDBACK_HARDENING_TARGET_V0",
        ],
        "acceptance_boundary": "accepted_schema_overlay_reference_this_application_contract_only",
    }

    trace = {
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_reviewed_application",
                "question": "is the source-ref rebind application cleanly reviewed",
                "answer": "yes" if closed else "no",
                "taken": "close as reviewed reference",
            },
            {
                "step": "freeze_reference",
                "question": "what object is frozen",
                "answer": "four applied/reviewed source-ref rebinds plus receipt chain",
                "taken": "emit reviewed reference and boundary lock",
            },
            {
                "step": "preserve_residuals",
                "question": "were ambiguity and requirement-gap branches resolved",
                "answer": "no",
                "taken": "carry 22 ambiguity and 498 requirement-gap bindings forward",
            },
            {
                "step": "select_post_closure_direction",
                "question": "what is recommended next",
                "answer": "decision-edge observability hardening first",
                "taken": next_edge,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(CLOSURE_RECORD_PATH, closure_record)
    write_json(REVIEWED_REFERENCE_PATH, reviewed_reference)
    write_json(REFERENCE_FREEZE_PATH, reference_freeze)
    write_json(RECEIPT_CHAIN_PATH, receipt_chain)
    write_json(BOUNDARY_LOCK_PATH, boundary_lock)
    write_json(RESIDUAL_BRANCH_CARRY_FORWARD_PATH, residual_carry)
    write_json(POST_CLOSURE_DECISION_SURFACE_PATH, post_closure_decision_surface)
    write_json(POST_UPDATE_SEQUENCE_HINT_PATH, hardening_hint)
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
        "CLOSURE_0_SOURCE_REVIEW_RECEIPT_CONSUMED": SOURCE_REVIEW_RECEIPT_PATH.exists(),
        "CLOSURE_1_CLOSURE_RECORD_EMITTED": CLOSURE_RECORD_PATH.exists(),
        "CLOSURE_2_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists(),
        "CLOSURE_3_REFERENCE_FREEZE_EMITTED": REFERENCE_FREEZE_PATH.exists(),
        "CLOSURE_4_RECEIPT_CHAIN_EMITTED": RECEIPT_CHAIN_PATH.exists(),
        "CLOSURE_5_BOUNDARY_LOCK_EMITTED": BOUNDARY_LOCK_PATH.exists(),
        "CLOSURE_6_FOUR_REBINDS_FROZEN_AS_REVIEWED": applied_rebind_count == 4 and closed,
        "CLOSURE_7_RESIDUAL_AMBIGUITY_BRANCH_CARRIED_FORWARD": ambiguity_binding_count == 22,
        "CLOSURE_8_RESIDUAL_REQUIREMENT_GAP_BRANCH_CARRIED_FORWARD": requirement_gap_binding_count == 498,
        "CLOSURE_9_POST_CLOSURE_DECISION_SURFACE_EMITTED": POST_CLOSURE_DECISION_SURFACE_PATH.exists(),
        "CLOSURE_10_POST_UPDATE_SEQUENCE_HINT_EMITTED": POST_UPDATE_SEQUENCE_HINT_PATH.exists(),
        "CLOSURE_11_NO_POST_CLOSURE_OBJECTIVE_EXECUTED": rollup["post_closure_next_objective_executed_count"] == 0,
        "CLOSURE_12_NO_VALUES_AUTHORIZED": rollup["values_authorized_count"] == 0,
        "CLOSURE_13_NO_VALUES_APPLIED": rollup["values_applied_count"] == 0,
        "CLOSURE_14_NO_METADATA_POPULATION": rollup["metadata_populated_count"] == 0,
        "CLOSURE_15_NO_TARGET_SELECTED": rollup["target_selected_for_build_count"] == 0,
        "CLOSURE_16_NO_RUNTIME_PATCH": rollup["runtime_patch_applied_count"] == 0,
        "CLOSURE_17_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "CLOSURE_18_NO_REUSABLE_SCHEMA_AUTHORIZED": rollup["reusable_schema_authorized_count"] == 0,
        "CLOSURE_19_NO_PREAPPROVED_SCHEMA_AUTHORIZED": rollup["preapproved_schema_authorized_count"] == 0,
        "CLOSURE_20_NO_VALIDATOR_REGISTRY_ENTRY": rollup["validator_registry_entry_created_count"] == 0,
        "CLOSURE_21_NO_FUTURE_AUTOMATIC_USE": rollup["future_automatic_use_allowed_count"] == 0,
        "CLOSURE_22_NO_LATEST_FILE_GUESSING": rollup["latest_file_guessing_count"] == 0,
        "CLOSURE_23_NO_MTIME_SELECTION": rollup["mtime_selection_count"] == 0,
        "CLOSURE_24_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "CLOSURE_25_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "accepted_schema_overlay_reference_this_application_contract_only",
        "CLOSURE_26_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_SOURCE_REF_REBIND_LAYER_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "closed": closed,
        "applied_rebind_count": applied_rebind_count,
        "ambiguity": ambiguity_binding_count,
        "requirement_gap": requirement_gap_binding_count,
        "metadata": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_source_ref_rebind_layer_closure_receipt_v0",
        "receipt_type": "TYPED_SOURCE_REF_REBIND_LAYER_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "machine_readable_source_ref_rebind_layer_closure_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "source_ref_rebind_layer_closed": closed,
            "closed_as_reviewed_reference": closed,
            "reviewed_reference_emitted": closed,
            "applied_rebind_count": applied_rebind_count,
            "proposal_binding_count": proposal_binding_count,
            "ambiguity_binding_count_preserved": ambiguity_binding_count,
            "requirement_gap_binding_count_preserved": requirement_gap_binding_count,
            "post_closure_next_objective_decision_ready": closed,
            "post_closure_next_objective_executed": False,
            "recommended_next": next_edge,
            "recommended_post_update_sequence": [
                "decision_edge_observability",
                "unit_feedback_hardening",
            ],
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
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "closure_record": rel(CLOSURE_RECORD_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "reference_freeze": rel(REFERENCE_FREEZE_PATH),
            "receipt_chain": rel(RECEIPT_CHAIN_PATH),
            "boundary_lock": rel(BOUNDARY_LOCK_PATH),
            "residual_branch_carry_forward": rel(RESIDUAL_BRANCH_CARRY_FORWARD_PATH),
            "post_closure_decision_surface": rel(POST_CLOSURE_DECISION_SURFACE_PATH),
            "post_update_sequence_hint": rel(POST_UPDATE_SEQUENCE_HINT_PATH),
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
    print(f"source_ref_rebind_layer_closure_receipt_id={receipt_id}")
    print(f"source_ref_rebind_layer_closure_receipt_path={rel(receipt_path)}")
    print(f"source_ref_rebind_layer_closure_record_path={rel(CLOSURE_RECORD_PATH)}")
    print(f"source_ref_rebind_layer_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"source_ref_rebind_layer_reference_freeze_path={rel(REFERENCE_FREEZE_PATH)}")
    print(f"source_ref_rebind_layer_receipt_chain_path={rel(RECEIPT_CHAIN_PATH)}")
    print(f"source_ref_rebind_layer_boundary_lock_path={rel(BOUNDARY_LOCK_PATH)}")
    print(f"post_closure_decision_surface_path={rel(POST_CLOSURE_DECISION_SURFACE_PATH)}")
    print(f"post_update_sequence_hint_path={rel(POST_UPDATE_SEQUENCE_HINT_PATH)}")
    print(f"source_ref_rebind_layer_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"source_ref_rebind_layer_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
