#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_MACHINE_READABLE_SOURCE_REF_REBIND_DOMINANCE_RULE_OR_ROW_LOCATOR_SURFACE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_source_ref_decision_surface.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SOURCE_REF_DECISION_SURFACE"
MODE = "DECISION_SURFACE / NO_REBIND_APPLIED / NO_RULE_APPLIED / NO_VALUE_AUTHORIZATION / NO_METADATA_FILL"
BUILD_MODE = "SOURCE_REF_DECISION_SURFACE_ONLY"

SOURCE_NARROWING_RECEIPT_ID = "8edaaab8"
SOURCE_NARROWING_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0_receipts/8edaaab8.json"
SOURCE_NARROWING_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_narrowing_surface_v0.json"
SOURCE_DOMINANCE_FEATURE_MATRIX_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_dominance_feature_matrix_v0.json"
SOURCE_PER_BINDING_NARROWING_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_per_binding_narrowing_v0.json"
SOURCE_NARROWED_REBIND_PROPOSALS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_narrowed_source_ref_rebind_proposals_v0.json"
SOURCE_RESIDUAL_TIE_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_residual_tie_table_v0.json"
SOURCE_DOMINANCE_RULE_CANDIDATES_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_dominance_rule_candidates_v0.json"
SOURCE_NARROWING_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_narrowing_review_packet_v0.json"
SOURCE_REBIND_APPLICATION_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_application_contract_v0.json"
SOURCE_NARROWING_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_narrowing_classification_v0.json"
SOURCE_NARROWING_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_narrowing_rollup_v0.json"
SOURCE_NARROWING_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_narrowing_v0/typed_machine_readable_source_ref_rebind_narrowing_profile_v0.json"

SOURCE_CANDIDATE_SCORE_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_rebind_review_v0/typed_machine_readable_source_ref_rebind_candidate_score_table_v0.json"
SOURCE_BROKEN_BINDING_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_row_path_refinement_v0/typed_machine_readable_broken_row_binding_table_v0.json"
SOURCE_MACHINE_SOURCE_SLOTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_machine_source_slots_v0.json"
SOURCE_FIELD_POLICY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_field_policy_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_ref_decision_surface_v0_receipts"

DECISION_SURFACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_decision_surface_v0.json"
DECISION_LESSON_GRAPH_PATH = OUT_DIR / "typed_machine_readable_source_ref_decision_lesson_graph_v0.json"
EVIDENCE_REQUIREMENT_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_ref_decision_evidence_requirements_v0.json"
DOMINANCE_RULE_SURFACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_rebind_dominance_rule_surface_v0.json"
ROW_LOCATOR_SURFACE_PATH = OUT_DIR / "typed_machine_readable_source_row_locator_surface_v0.json"
PER_BINDING_DECISION_REQUIREMENTS_PATH = OUT_DIR / "typed_machine_readable_per_binding_source_ref_decision_requirements_v0.json"
RESIDUAL_TIE_EXPLANATION_PATH = OUT_DIR / "typed_machine_readable_source_ref_residual_tie_explanation_v0.json"
BRANCH_DECISION_TABLE_PATH = OUT_DIR / "typed_machine_readable_source_ref_next_branch_decision_table_v0.json"
REVIEW_PACKET_PATH = OUT_DIR / "typed_machine_readable_source_ref_decision_surface_review_packet_v0.json"
NEXT_UNIT_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_source_ref_decision_next_unit_contract_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_source_ref_decision_surface_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_source_ref_decision_surface_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_source_ref_decision_surface_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_source_ref_decision_surface_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_source_ref_decision_surface_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_source_ref_decision_surface_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_NARROWING_RECEIPT_PATH,
    SOURCE_NARROWING_SURFACE_PATH,
    SOURCE_DOMINANCE_FEATURE_MATRIX_PATH,
    SOURCE_PER_BINDING_NARROWING_TABLE_PATH,
    SOURCE_NARROWED_REBIND_PROPOSALS_PATH,
    SOURCE_RESIDUAL_TIE_TABLE_PATH,
    SOURCE_DOMINANCE_RULE_CANDIDATES_PATH,
    SOURCE_NARROWING_REVIEW_PACKET_PATH,
    SOURCE_REBIND_APPLICATION_CONTRACT_PATH,
    SOURCE_NARROWING_CLASSIFICATION_PATH,
    SOURCE_NARROWING_ROLLUP_PATH,
    SOURCE_NARROWING_PROFILE_PATH,
    SOURCE_CANDIDATE_SCORE_TABLE_PATH,
    SOURCE_BROKEN_BINDING_TABLE_PATH,
    SOURCE_MACHINE_SOURCE_SLOTS_PATH,
    SOURCE_FIELD_POLICY_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_NARROWING_STILL_AMBIGUOUS"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_SOURCE_REF_REBIND_NARROWING_STILL_AMBIGUOUS"
EXPECTED_NEXT = "BUILD_MACHINE_READABLE_SOURCE_REF_REBIND_DOMINANCE_RULE_OR_ROW_LOCATOR_SURFACE_V0"

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

    receipt = read_json(SOURCE_NARROWING_RECEIPT_PATH)
    summary = receipt.get("machine_readable_source_ref_rebind_narrowing_summary", {})
    features = read_json(SOURCE_DOMINANCE_FEATURE_MATRIX_PATH)
    per = read_json(SOURCE_PER_BINDING_NARROWING_TABLE_PATH)
    narrowed = read_json(SOURCE_NARROWED_REBIND_PROPOSALS_PATH)
    residual = read_json(SOURCE_RESIDUAL_TIE_TABLE_PATH)
    rules = read_json(SOURCE_DOMINANCE_RULE_CANDIDATES_PATH)
    classif = read_json(SOURCE_NARROWING_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_NARROWING_ROLLUP_PATH)
    profile = read_json(SOURCE_NARROWING_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_NARROWING_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("narrowing_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"narrowing_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("narrowing_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"narrowing_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("source_ref_rebind_candidate_count") != 168:
        failures.append("source_ref_candidate_count_not_168")
    if summary.get("binding_count") != 21:
        failures.append("binding_count_not_21")
    if summary.get("narrowed_rebind_proposal_count") != 0:
        failures.append("narrowed_rebind_proposal_count_nonzero")
    if summary.get("residual_tie_binding_count") != 21:
        failures.append("residual_tie_binding_count_not_21")
    if summary.get("dominance_rule_candidate_count") != 1:
        failures.append("dominance_rule_candidate_count_not_1")
    if summary.get("per_binding_narrowing_status_counts", {}).get("RESIDUAL_TOP_CANDIDATES_TIED") != 21:
        failures.append("residual_top_candidates_tied_count_not_21")
    if summary.get("rebinds_applied") is not False:
        failures.append("rebinds_applied_unexpectedly")
    if summary.get("values_authorized") is not False:
        failures.append("values_authorized_unexpectedly")
    if summary.get("metadata_populated") is not False:
        failures.append("metadata_populated_unexpectedly")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")

    if features.get("candidate_count") != 168:
        failures.append("dominance_feature_candidate_count_not_168")
    if per.get("binding_count") != 21:
        failures.append("per_binding_narrowing_count_not_21")
    if narrowed.get("proposal_count") != 0:
        failures.append("narrowed_proposals_nonzero")
    if residual.get("residual_tie_binding_count") != 21:
        failures.append("residual_tie_table_count_not_21")
    if rules.get("rule_candidate_count") != 1:
        failures.append("dominance_rule_table_count_not_1")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("narrowing_classification_status_wrong")
    if roll.get("metadata_populated_count") != 0:
        failures.append("narrowing_rollup_metadata_populated_nonzero")
    if profile.get("metadata_populated") is not False:
        failures.append("narrowing_profile_metadata_populated_true")

    return failures

def load_records() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Dict[str, Any]], Dict[str, Dict[str, Any]]]:
    features = [r for r in read_json(SOURCE_DOMINANCE_FEATURE_MATRIX_PATH).get("records", []) if isinstance(r, dict)]
    residual = [r for r in read_json(SOURCE_RESIDUAL_TIE_TABLE_PATH).get("records", []) if isinstance(r, dict)]
    rules = [r for r in read_json(SOURCE_DOMINANCE_RULE_CANDIDATES_PATH).get("records", []) if isinstance(r, dict)]
    per_rows = [r for r in read_json(SOURCE_PER_BINDING_NARROWING_TABLE_PATH).get("records", []) if isinstance(r, dict)]
    broken = {
        str(r.get("slot_id")): r
        for r in read_json(SOURCE_BROKEN_BINDING_TABLE_PATH).get("records", [])
        if isinstance(r, dict) and r.get("slot_id")
    }
    slots = {
        str(r.get("slot_id")): r
        for r in read_json(SOURCE_MACHINE_SOURCE_SLOTS_PATH).get("slots", [])
        if isinstance(r, dict) and r.get("slot_id")
    }
    return features, residual, rules, per_rows, broken, slots

def evidence_requirements(residual: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for tie in residual:
        rows.append({
            "slot_id": tie.get("slot_id"),
            "row_uid": tie.get("row_uid"),
            "field": tie.get("field"),
            "tied_candidate_count": tie.get("tied_candidate_count"),
            "top_score": tie.get("top_score"),
            "required_evidence_classes": [
                {
                    "evidence_class": "EXPLICIT_SOURCE_ROLE",
                    "question": "Which candidate artifact is the authoritative source row for this slot?",
                    "machine_status": "missing",
                    "allowed_resolver": "prevalidated_schema_or_human_review",
                },
                {
                    "evidence_class": "ARTIFACT_PRODUCER_UNIT",
                    "question": "Which unit produced the artifact as source material rather than diagnostic residue?",
                    "machine_status": "not_distinguishing_under_current_features",
                    "allowed_resolver": "source lineage registry or producer metadata",
                },
                {
                    "evidence_class": "SOURCE_PACKET_LINEAGE",
                    "question": "Does the candidate descend from the source packet layer required by the field policy?",
                    "machine_status": "not_materialized_as typed lineage",
                    "allowed_resolver": "source packet lineage bridge",
                },
                {
                    "evidence_class": "ROW_IDENTITY_MATCH",
                    "question": "Does the candidate contain a row identity matching row_uid/slot_id/field?",
                    "machine_status": "not available as unique evidence",
                    "allowed_resolver": "source row locator surface",
                },
                {
                    "evidence_class": "FIELD_POLICY_SOURCE_OBJECT_MATCH",
                    "question": "Does the candidate match the declared source object for this field?",
                    "machine_status": "not discriminating",
                    "allowed_resolver": "field policy enrichment",
                },
            ],
            "safe_null_behavior": "keep source ref unbound; do not extract value",
        })
    return rows

def build_per_binding_requirements(residual: List[Dict[str, Any]], broken: Dict[str, Dict[str, Any]], slots: Dict[str, Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for tie in residual:
        slot_id = str(tie.get("slot_id"))
        b = broken.get(slot_id, {})
        s = slots.get(slot_id, {})
        rows.append({
            "slot_id": slot_id,
            "row_uid": tie.get("row_uid"),
            "field": tie.get("field"),
            "current_row_source_ref": b.get("current_row_source_ref") or b.get("row_source_ref"),
            "current_row_json_path": b.get("current_row_json_path") or b.get("row_json_path"),
            "required_source_object": s.get("required_source_object"),
            "source_class": s.get("source_class"),
            "tied_candidate_count": tie.get("tied_candidate_count"),
            "decision_requirement": "need evidence that identifies one candidate as source row or proves all candidates are diagnostic residue",
            "dominance_rule_possible": True,
            "row_locator_possible": True,
            "preferred_machine_next": "source_row_locator",
            "why": "Current dominance features score candidate artifacts but do not locate row identity inside candidate artifacts.",
        })
    return rows

def branch_decision(residual: List[Dict[str, Any]], rule_candidates: List[Dict[str, Any]]) -> Tuple[str, List[str], List[Dict[str, Any]], str]:
    # Rule candidate exists, but current evidence has no unique signal. Prefer row locator before authority/policy rule.
    reason_codes = [
        "SOURCE_REF_DECISION_SURFACE_BUILT",
        "RESIDUAL_TIE_EVIDENCE_REQUIREMENTS_EMITTED",
        "DOMINANCE_RULE_SURFACE_EMITTED",
        "SOURCE_ROW_LOCATOR_SURFACE_EMITTED",
        "NO_REBINDS_APPLIED",
        "NO_RULE_APPLIED",
        "NO_VALUES_AUTHORIZED_OR_APPLIED",
        "NO_METADATA_POPULATION",
    ]

    branch_rows = [
        {
            "branch": "DOMINANCE_RULE_AUTHORIZATION",
            "safe_now": False,
            "why": "A dominance-rule candidate exists, but it would need external/schema authority because no current machine evidence selects one candidate.",
            "would_require": [
                "explicit source role policy",
                "accepted source preference",
                "producer/lineage metadata",
            ],
        },
        {
            "branch": "SOURCE_ROW_LOCATOR_SURFACE",
            "safe_now": True,
            "why": "The machine can still inspect candidate artifacts for row identity and source-object structure without choosing a candidate.",
            "would_require": [
                "candidate artifact scan",
                "row_uid/slot_id/field locator features",
                "source packet lineage markers",
                "field policy source-object matching",
            ],
        },
    ]

    status = "TYPED_MACHINE_READABLE_SOURCE_REF_DECISION_SURFACE_BUILT_ROW_LOCATOR_REQUIRED"
    next_edge = "BUILD_MACHINE_READABLE_SOURCE_ROW_LOCATOR_SURFACE_V0"
    reason_codes.append("SOURCE_ROW_LOCATOR_SELECTED_AS_NEXT_MACHINE_DECISION_SURFACE")
    return status, reason_codes, branch_rows, next_edge

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_ref_decision_surface_authority_boundary_v0",
        "status": status,
        "may_describe_decision_requirements": True,
        "may_emit_dominance_rule_surface": True,
        "may_emit_source_row_locator_surface": True,
        "may_select_next_machine_surface": True,
        "may_apply_dominance_rule": False,
        "may_apply_rebinds": False,
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

def rollup_obj(status: str, residual: List[Dict[str, Any]], evidence_rows: List[Dict[str, Any]], branch_rows: List[Dict[str, Any]], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_ref_decision_surface_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "residual_tie_binding_count": len(residual),
        "decision_evidence_requirement_count": sum(len(r.get("required_evidence_classes", [])) for r in evidence_rows),
        "dominance_rule_surface_count": 1,
        "row_locator_surface_count": 1,
        "safe_machine_branch_count": sum(1 for b in branch_rows if b.get("safe_now") is True),
        "selected_next_machine_surface": next_edge,
        "dominance_rule_applied_count": 0,
        "source_row_locator_applied_count": 0,
        "rebinds_applied_count": 0,
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
        "dominance_rule_applied_count",
        "source_row_locator_applied_count",
        "rebinds_applied_count",
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
        "schema_version": "typed_machine_readable_source_ref_decision_surface_profile_v0",
        "profile_id": "source_ref_decision_surface_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "decision_surface_built": True,
        "dominance_rule_applied": False,
        "source_row_locator_applied": False,
        "rebinds_applied": False,
        "refinements_applied": False,
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
        "schema_version": "typed_machine_readable_source_ref_decision_surface_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The narrowing surface still has 21 residual source-ref ties; this unit turns that tie into an explicit decision lesson and selects the next machine-safe surface: source-row locator.",
        "residual_tie_binding_count": roll["residual_tie_binding_count"],
        "decision_evidence_requirement_count": roll["decision_evidence_requirement_count"],
        "dominance_rule_surface_count": roll["dominance_rule_surface_count"],
        "row_locator_surface_count": roll["row_locator_surface_count"],
        "selected_next_machine_surface": next_edge,
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "dominance_rule_applied_count": 0,
        "source_row_locator_applied_count": 0,
        "rebinds_applied_count": 0,
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
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
    }

def transition_trace_obj(status: str, reason_codes: List[str], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_source_ref_decision_surface_transition_trace_v0",
        "trace": [
            {
                "step": "consume_residual_rebind_ties",
                "question": "what kind of evidence would make source-ref choice lawful",
                "answer": "explicit source role, producer lineage, source packet lineage, row identity, and field-policy source object evidence",
                "taken": "emit decision evidence requirements",
            },
            {
                "step": "choose_next_machine_safe_surface",
                "question": "dominance-rule authorization or row locator",
                "answer": "row locator is machine-safe; dominance rule requires authority unless lineage evidence is materialized",
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

    if failures:
        features, residual, rules, per_rows, broken, slots = [], [], [], [], {}, {}
        evidence_rows, per_binding_requirements = [], []
        status = "TYPED_MACHINE_READABLE_SOURCE_REF_DECISION_SURFACE_BASIS_FAIL"
        reason_codes = failures
        branch_rows = []
        next_edge = "REPAIR_MACHINE_READABLE_SOURCE_REF_DECISION_SURFACE_BASIS_V0"
    else:
        features, residual, rules, per_rows, broken, slots = load_records()
        evidence_rows = evidence_requirements(residual)
        per_binding_requirements = build_per_binding_requirements(residual, broken, slots)
        status, reason_codes, branch_rows, next_edge = branch_decision(residual, rules)

    roll = rollup_obj(status, residual, evidence_rows, branch_rows, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    boundary = authority_boundary_obj(status)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    decision_surface = {
        "schema_version": "typed_machine_readable_source_ref_decision_surface_v0",
        "surface_status": status,
        "source_narrowing_receipt_id": SOURCE_NARROWING_RECEIPT_ID,
        "residual_tie_binding_count": roll["residual_tie_binding_count"],
        "decision_evidence_requirement_count": roll["decision_evidence_requirement_count"],
        "dominance_rule_surface_ref": rel(DOMINANCE_RULE_SURFACE_PATH),
        "row_locator_surface_ref": rel(ROW_LOCATOR_SURFACE_PATH),
        "selected_next_machine_surface": next_edge,
        "surface_claim": "This is a decision-teaching surface: it explains what evidence is needed to choose source refs lawfully, without choosing or applying them.",
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    lesson_graph = {
        "schema_version": "typed_machine_readable_source_ref_decision_lesson_graph_v0",
        "graph_status": "DECISION_LESSON_GRAPH_EMITTED",
        "edges": [
            {
                "from": "source_ref_candidates_tied",
                "to": "semantic_narrowing_attempted",
                "lesson": "resolvable JSON candidates are not enough; candidate existence is not candidate authority",
            },
            {
                "from": "semantic_narrowing_attempted",
                "to": "residual_ties",
                "lesson": "without row identity or source lineage, dominance features remain insufficient",
            },
            {
                "from": "residual_ties",
                "to": "decision_evidence_requirements",
                "lesson": "tie must be converted into required evidence, not guessed selection",
            },
            {
                "from": "decision_evidence_requirements",
                "to": "source_row_locator_surface",
                "lesson": "machine-safe next move is to locate row identity and source lineage before policy authorization",
            },
        ],
    }

    dominance_rule_surface = {
        "schema_version": "typed_machine_readable_source_ref_rebind_dominance_rule_surface_v0",
        "surface_status": "DOMINANCE_RULE_SURFACE_BUILT_NOT_APPLIED",
        "input_rule_candidate_count": len(rules),
        "rule_application_authorized": False,
        "why_not_apply": "current machine evidence does not identify a unique source ref; applying a rule now would encode an unauthorised preference",
        "allowed_future_rule_basis": [
            "explicit source role policy",
            "producer unit lineage",
            "source packet lineage",
            "field policy declared source object",
            "human/prevalidated schema accepted source preference",
        ],
        "recommended_machine_branch": "BUILD_MACHINE_READABLE_SOURCE_ROW_LOCATOR_SURFACE_V0",
    }

    row_locator_surface = {
        "schema_version": "typed_machine_readable_source_row_locator_surface_v0",
        "surface_status": "SOURCE_ROW_LOCATOR_SURFACE_BUILT_AS_NEXT_MACHINE_SAFE_BRANCH",
        "purpose": "Inspect candidate source artifacts for row identity and source-object structure without choosing or applying source refs.",
        "locator_inputs": [
            rel(SOURCE_DOMINANCE_FEATURE_MATRIX_PATH),
            rel(SOURCE_RESIDUAL_TIE_TABLE_PATH),
            rel(SOURCE_BROKEN_BINDING_TABLE_PATH),
            rel(SOURCE_MACHINE_SOURCE_SLOTS_PATH),
            rel(SOURCE_FIELD_POLICY_PATH),
        ],
        "locator_should_find": [
            "row_uid/slot_id/field occurrences",
            "source-object collection shape",
            "source packet lineage marker",
            "producer unit identity",
            "field policy source-object match",
        ],
        "recommended_next_unit": "BUILD_MACHINE_READABLE_SOURCE_ROW_LOCATOR_SURFACE_V0",
        "not_authorized_to_rebind": True,
    }

    review_packet = {
        "schema_version": "typed_machine_readable_source_ref_decision_surface_review_packet_v0",
        "review_packet_status": "DECISION_SURFACE_REVIEW_AVAILABLE",
        "question": "Confirm the next machine-safe branch is source row locator rather than source-ref dominance rule authorization.",
        "default_recommended_response": "BUILD_MACHINE_READABLE_SOURCE_ROW_LOCATOR_SURFACE_V0",
        "allowed_responses": [
            "BUILD_MACHINE_READABLE_SOURCE_ROW_LOCATOR_SURFACE_V0",
            "AUTHORIZE_SOURCE_REF_REBIND_DOMINANCE_RULE_SURFACE_V0",
            "FREEZE_SOURCE_REF_DECISION_SURFACE_V0",
        ],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    next_contract = {
        "schema_version": "typed_machine_readable_source_ref_decision_next_unit_contract_v0",
        "contract_status": "NEXT_UNIT_CONTRACT_EMITTED",
        "recommended_next_unit": next_edge,
        "required_inputs_for_next_unit": [
            rel(DECISION_SURFACE_PATH),
            rel(EVIDENCE_REQUIREMENT_TABLE_PATH),
            rel(ROW_LOCATOR_SURFACE_PATH),
            rel(PER_BINDING_DECISION_REQUIREMENTS_PATH),
            rel(SOURCE_DOMINANCE_FEATURE_MATRIX_PATH),
            rel(SOURCE_RESIDUAL_TIE_TABLE_PATH),
        ],
        "must_not": [
            "apply rebinds",
            "authorize values",
            "extract values",
            "populate metadata",
            "mark discriminators ready",
            "use latest/mtime guessing",
        ],
    }

    classification = {
        "schema_version": "typed_machine_readable_source_ref_decision_surface_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "residual_tie_binding_count": roll["residual_tie_binding_count"],
        "decision_evidence_requirement_count": roll["decision_evidence_requirement_count"],
        "selected_next_machine_surface": next_edge,
        "dominance_rule_applied": False,
        "source_row_locator_applied": False,
        "rebinds_applied": False,
        "refinements_applied": False,
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

    write_json(DECISION_SURFACE_PATH, decision_surface)
    write_json(DECISION_LESSON_GRAPH_PATH, lesson_graph)
    write_json(EVIDENCE_REQUIREMENT_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_ref_decision_evidence_requirements_v0",
        "table_status": "DECISION_EVIDENCE_REQUIREMENTS_EMITTED",
        "record_count": len(evidence_rows),
        "records": evidence_rows,
    })
    write_json(DOMINANCE_RULE_SURFACE_PATH, dominance_rule_surface)
    write_json(ROW_LOCATOR_SURFACE_PATH, row_locator_surface)
    write_json(PER_BINDING_DECISION_REQUIREMENTS_PATH, {
        "schema_version": "typed_machine_readable_per_binding_source_ref_decision_requirements_v0",
        "table_status": "PER_BINDING_DECISION_REQUIREMENTS_EMITTED",
        "record_count": len(per_binding_requirements),
        "records": per_binding_requirements,
    })
    write_json(RESIDUAL_TIE_EXPLANATION_PATH, {
        "schema_version": "typed_machine_readable_source_ref_residual_tie_explanation_v0",
        "explanation_status": "RESIDUAL_TIE_EXPLANATION_EMITTED",
        "record_count": len(residual),
        "records": residual,
    })
    write_json(BRANCH_DECISION_TABLE_PATH, {
        "schema_version": "typed_machine_readable_source_ref_next_branch_decision_table_v0",
        "branch_decision_status": "NEXT_BRANCH_DECIDED_WITHOUT_REBIND_APPLICATION",
        "selected_next_machine_surface": next_edge,
        "records": branch_rows,
    })
    write_json(REVIEW_PACKET_PATH, review_packet)
    write_json(NEXT_UNIT_CONTRACT_PATH, next_contract)
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
        "DECISION_SURFACE_0_NARROWING_RECEIPT_CONSUMED": SOURCE_NARROWING_RECEIPT_PATH.exists(),
        "DECISION_SURFACE_1_RESIDUAL_TIE_TABLE_CONSUMED": SOURCE_RESIDUAL_TIE_TABLE_PATH.exists(),
        "DECISION_SURFACE_2_DECISION_SURFACE_EMITTED": DECISION_SURFACE_PATH.exists(),
        "DECISION_SURFACE_3_LESSON_GRAPH_EMITTED": DECISION_LESSON_GRAPH_PATH.exists(),
        "DECISION_SURFACE_4_EVIDENCE_REQUIREMENTS_EMITTED": EVIDENCE_REQUIREMENT_TABLE_PATH.exists(),
        "DECISION_SURFACE_5_DOMINANCE_RULE_SURFACE_EMITTED": DOMINANCE_RULE_SURFACE_PATH.exists(),
        "DECISION_SURFACE_6_ROW_LOCATOR_SURFACE_EMITTED": ROW_LOCATOR_SURFACE_PATH.exists(),
        "DECISION_SURFACE_7_PER_BINDING_REQUIREMENTS_EMITTED": PER_BINDING_DECISION_REQUIREMENTS_PATH.exists(),
        "DECISION_SURFACE_8_RESIDUAL_TIE_EXPLANATION_EMITTED": RESIDUAL_TIE_EXPLANATION_PATH.exists(),
        "DECISION_SURFACE_9_BRANCH_DECISION_TABLE_EMITTED": BRANCH_DECISION_TABLE_PATH.exists(),
        "DECISION_SURFACE_10_REVIEW_PACKET_EMITTED": REVIEW_PACKET_PATH.exists(),
        "DECISION_SURFACE_11_NEXT_UNIT_CONTRACT_EMITTED": NEXT_UNIT_CONTRACT_PATH.exists(),
        "DECISION_SURFACE_12_NO_DOMINANCE_RULE_APPLIED": roll["dominance_rule_applied_count"] == 0,
        "DECISION_SURFACE_13_NO_ROW_LOCATOR_APPLIED": roll["source_row_locator_applied_count"] == 0,
        "DECISION_SURFACE_14_NO_REBINDS_APPLIED": roll["rebinds_applied_count"] == 0,
        "DECISION_SURFACE_15_NO_REFINEMENTS_APPLIED": roll["refinements_applied_count"] == 0,
        "DECISION_SURFACE_16_NO_VALUES_AUTHORIZED": roll["values_authorized_count"] == 0,
        "DECISION_SURFACE_17_NO_VALUES_APPLIED": roll["values_applied_count"] == 0,
        "DECISION_SURFACE_18_NO_NULL_REASONS_ACCEPTED": roll["null_reason_accepted_count"] == 0,
        "DECISION_SURFACE_19_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "DECISION_SURFACE_20_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "DECISION_SURFACE_21_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "DECISION_SURFACE_22_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "DECISION_SURFACE_23_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "DECISION_SURFACE_24_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "DECISION_SURFACE_25_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "DECISION_SURFACE_26_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "DECISION_SURFACE_27_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "DECISION_SURFACE_28_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "DECISION_SURFACE_29_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "DECISION_SURFACE_30_NO_C5_OPENED": classification["c5_authorized"] is False,
        "DECISION_SURFACE_31_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "DECISION_SURFACE_32_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "DECISION_SURFACE_33_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "DECISION_SURFACE_34_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "DECISION_SURFACE_35_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "DECISION_SURFACE_36_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_SOURCE_REF_DECISION_SURFACE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "residual_ties": roll["residual_tie_binding_count"],
        "next": next_edge,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_source_ref_decision_surface_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_SOURCE_REF_DECISION_SURFACE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_narrowing_receipt_id": SOURCE_NARROWING_RECEIPT_ID,
        "machine_readable_source_ref_decision_surface_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "residual_tie_binding_count": roll["residual_tie_binding_count"],
            "decision_evidence_requirement_count": roll["decision_evidence_requirement_count"],
            "dominance_rule_surface_count": roll["dominance_rule_surface_count"],
            "row_locator_surface_count": roll["row_locator_surface_count"],
            "selected_next_machine_surface": next_edge,
            "dominance_rule_applied": False,
            "source_row_locator_applied": False,
            "rebinds_applied": False,
            "refinements_applied": False,
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
            "decision_surface": rel(DECISION_SURFACE_PATH),
            "decision_lesson_graph": rel(DECISION_LESSON_GRAPH_PATH),
            "evidence_requirements": rel(EVIDENCE_REQUIREMENT_TABLE_PATH),
            "dominance_rule_surface": rel(DOMINANCE_RULE_SURFACE_PATH),
            "row_locator_surface": rel(ROW_LOCATOR_SURFACE_PATH),
            "per_binding_decision_requirements": rel(PER_BINDING_DECISION_REQUIREMENTS_PATH),
            "residual_tie_explanation": rel(RESIDUAL_TIE_EXPLANATION_PATH),
            "branch_decision_table": rel(BRANCH_DECISION_TABLE_PATH),
            "review_packet": rel(REVIEW_PACKET_PATH),
            "next_unit_contract": rel(NEXT_UNIT_CONTRACT_PATH),
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
    print(f"source_ref_decision_surface_receipt_id={receipt_id}")
    print(f"source_ref_decision_surface_receipt_path={rel(receipt_path)}")
    print(f"source_ref_decision_surface_path={rel(DECISION_SURFACE_PATH)}")
    print(f"source_ref_decision_lesson_graph_path={rel(DECISION_LESSON_GRAPH_PATH)}")
    print(f"source_ref_decision_evidence_requirements_path={rel(EVIDENCE_REQUIREMENT_TABLE_PATH)}")
    print(f"source_ref_dominance_rule_surface_path={rel(DOMINANCE_RULE_SURFACE_PATH)}")
    print(f"source_row_locator_surface_path={rel(ROW_LOCATOR_SURFACE_PATH)}")
    print(f"per_binding_decision_requirements_path={rel(PER_BINDING_DECISION_REQUIREMENTS_PATH)}")
    print(f"source_ref_decision_branch_table_path={rel(BRANCH_DECISION_TABLE_PATH)}")
    print(f"source_ref_decision_surface_rollup_path={rel(ROLLUP_PATH)}")
    print(f"source_ref_decision_surface_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
