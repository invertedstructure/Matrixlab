#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_NARROWER_TYPED_VALUE_SOURCE_METADATA_SURFACE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_surface.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_SURFACE"
MODE = "BUILD_TYPED_METADATA_SURFACE / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "TYPED_METADATA_OBSERVABILITY_ONLY"

SOURCE_EQ_DIAG_RECEIPT_ID = "100c866f"
SOURCE_EQ_DIAG_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_equivalence_class_diagnostic_v0_receipts/100c866f.json"
SOURCE_EQ_DIAG_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_equivalence_class_diagnostic_v0/value_source_equivalence_class_diagnostic_surface_v0.json"
SOURCE_EQ_FIELD_COMPARISON_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_equivalence_class_diagnostic_v0/value_source_equivalence_class_field_comparison_v0.json"
SOURCE_EQ_OBSERVABILITY_GAP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_equivalence_class_diagnostic_v0/value_source_equivalence_class_observability_gap_v0.json"
SOURCE_EQ_CASE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_equivalence_class_diagnostic_v0/value_source_equivalence_class_case_classification_v0.json"
SOURCE_EQ_NEXT_EDGE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_equivalence_class_diagnostic_v0/value_source_equivalence_class_next_edge_recommendation_v0.json"

SOURCE_DOMINANCE_APPLICATION_RECEIPT_ID = "3ebaf16f"
SOURCE_DOMINANCE_APPLICATION_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_application_v0_receipts/3ebaf16f.json"
SOURCE_DOMINANCE_EQUIVALENCE_CLASS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_application_v0/explicit_runtime_patch_target_value_source_dominance_rule_equivalence_class_v0.json"
SOURCE_DOMINANCE_APPLICATION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_application_v0/explicit_runtime_patch_target_value_source_dominance_rule_application_table_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_surface_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_surface_v0_receipts"

METADATA_SURFACE_PATH = OUT_DIR / "typed_value_source_metadata_surface_v0.json"
ROW_METADATA_TEMPLATE_PATH = OUT_DIR / "typed_value_source_row_metadata_template_v0.json"
DISCRIMINATOR_CANDIDATE_SURFACE_PATH = OUT_DIR / "typed_value_source_discriminator_candidate_surface_v0.json"
METADATA_EXTRACTION_REQUEST_PATH = OUT_DIR / "typed_value_source_metadata_extraction_request_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_value_source_metadata_surface_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_value_source_metadata_surface_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_value_source_metadata_surface_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_value_source_metadata_surface_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_value_source_metadata_surface_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_value_source_metadata_surface_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_EQ_DIAG_RECEIPT_PATH,
    SOURCE_EQ_DIAG_SURFACE_PATH,
    SOURCE_EQ_FIELD_COMPARISON_PATH,
    SOURCE_EQ_OBSERVABILITY_GAP_PATH,
    SOURCE_EQ_CASE_CLASSIFICATION_PATH,
    SOURCE_EQ_NEXT_EDGE_PATH,
    SOURCE_DOMINANCE_APPLICATION_RECEIPT_PATH,
    SOURCE_DOMINANCE_EQUIVALENCE_CLASS_PATH,
    SOURCE_DOMINANCE_APPLICATION_TABLE_PATH,
]

EXPECTED_DIAG_STATUS = "VALUE_SOURCE_EQUIVALENCE_CLASS_CHARACTERIZED"
EXPECTED_PRIMARY_CASE = "UNRESOLVED_DISTINGUISHABILITY_DUE_TO_MISSING_TYPED_METADATA"
EXPECTED_NEXT = "BUILD_NARROWER_TYPED_VALUE_SOURCE_METADATA_SURFACE_V0"

CORE_METADATA_FIELDS = [
    "direct_evidence_ref",
    "direct_evidence_strength",
    "load_bearing_reason",
    "target_scope",
    "target_aspect",
    "comparison_grain",
    "source_authority",
    "source_role",
    "inference_strength",
    "inference_chain_ref",
    "provenance_depth",
    "verification_gate_ref",
    "rollback_or_stop_boundary_ref",
    "schema_preference_key",
    "human_preference_boundary_ref",
]

FIELD_ROLE_MAP = {
    "direct_evidence_ref": "evidence_anchor",
    "direct_evidence_strength": "evidence_strength",
    "load_bearing_reason": "load_bearingness",
    "target_scope": "scope",
    "target_aspect": "comparison_grain",
    "comparison_grain": "comparison_grain",
    "source_authority": "provenance",
    "source_role": "provenance",
    "inference_strength": "inference_strength",
    "inference_chain_ref": "inference_strength",
    "provenance_depth": "provenance",
    "verification_gate_ref": "supporting_ref",
    "rollback_or_stop_boundary_ref": "supporting_ref",
    "schema_preference_key": "schema_preference",
    "human_preference_boundary_ref": "review_boundary",
}

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

def validate_source_basis() -> List[str]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    diag_receipt = read_json(SOURCE_EQ_DIAG_RECEIPT_PATH)
    diag_surface = read_json(SOURCE_EQ_DIAG_SURFACE_PATH)
    field_cmp = read_json(SOURCE_EQ_FIELD_COMPARISON_PATH)
    obs_gap = read_json(SOURCE_EQ_OBSERVABILITY_GAP_PATH)
    case_class = read_json(SOURCE_EQ_CASE_CLASSIFICATION_PATH)
    next_edge = read_json(SOURCE_EQ_NEXT_EDGE_PATH)
    app_receipt = read_json(SOURCE_DOMINANCE_APPLICATION_RECEIPT_PATH)
    eq_class = read_json(SOURCE_DOMINANCE_EQUIVALENCE_CLASS_PATH)

    diag_summary = diag_receipt.get("equivalence_class_diagnostic_summary", {})
    app_summary = app_receipt.get("dominance_rule_application_summary", {})

    if diag_receipt.get("receipt_id") != SOURCE_EQ_DIAG_RECEIPT_ID or diag_receipt.get("gate") != "PASS":
        failures.append("diagnostic_receipt_not_pass")
    if diag_summary.get("status") != EXPECTED_DIAG_STATUS:
        failures.append(f"diagnostic_status_not_expected:{diag_summary.get('status')}")
    if diag_summary.get("primary_case") != EXPECTED_PRIMARY_CASE:
        failures.append(f"diagnostic_primary_case_not_expected:{diag_summary.get('primary_case')}")
    if diag_summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"diagnostic_next_not_expected:{diag_summary.get('recommended_next')}")
    if diag_summary.get("real_tie_proven") is not False:
        failures.append("diagnostic_claimed_real_tie")
    if diag_summary.get("rule_refined") is not False:
        failures.append("diagnostic_refined_rule")
    if diag_summary.get("tie_broken") is not False:
        failures.append("diagnostic_broke_tie")
    if diag_summary.get("candidate_values_filled") is not False:
        failures.append("diagnostic_filled_candidate_values")

    if diag_surface.get("diagnostic_status") != EXPECTED_DIAG_STATUS:
        failures.append("diagnostic_surface_status_not_expected")
    if diag_surface.get("primary_case") != EXPECTED_PRIMARY_CASE:
        failures.append("diagnostic_surface_primary_case_not_expected")

    if case_class.get("primary_case") != EXPECTED_PRIMARY_CASE:
        failures.append("case_classification_primary_case_not_expected")
    if case_class.get("recommended_next") != EXPECTED_NEXT:
        failures.append("case_classification_next_not_expected")
    if case_class.get("is_real_tie_proven") is not False:
        failures.append("case_classification_claimed_real_tie")

    if next_edge.get("recommended_next") != EXPECTED_NEXT:
        failures.append("next_edge_recommendation_not_expected")

    if field_cmp.get("top_row_count") != 3:
        failures.append(f"field_comparison_top_count_not_3:{field_cmp.get('top_row_count')}")
    if field_cmp.get("same_rank_surface") is not True:
        failures.append("field_comparison_not_same_rank_surface")
    if field_cmp.get("unique_value_count") != 2:
        failures.append(f"field_comparison_unique_value_count_not_2:{field_cmp.get('unique_value_count')}")

    if obs_gap.get("missing_everywhere_count") != 15:
        failures.append(f"observability_gap_missing_count_not_15:{obs_gap.get('missing_everywhere_count')}")

    if app_receipt.get("receipt_id") != SOURCE_DOMINANCE_APPLICATION_RECEIPT_ID or app_receipt.get("gate") != "PASS":
        failures.append("dominance_application_receipt_not_pass")
    if app_summary.get("status") != "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_STILL_MULTIPLE_TOP_ROWS":
        failures.append("dominance_application_status_not_expected")
    if app_summary.get("top_row_count_after_application") != 3:
        failures.append("dominance_application_top_count_not_3")

    if eq_class.get("equivalence_status") != "TOP_ROW_EQUIVALENCE_CLASS_REMAINS":
        failures.append("source_equivalence_status_not_expected")
    if eq_class.get("top_row_count") != 3:
        failures.append("source_equivalence_top_count_not_3")

    return failures

def source_top_rows() -> List[Dict[str, Any]]:
    field_cmp = read_json(SOURCE_EQ_FIELD_COMPARISON_PATH)
    rows = field_cmp.get("top_rows")
    if isinstance(rows, list) and rows:
        return [r for r in rows if isinstance(r, dict)]

    diag_surface = read_json(SOURCE_EQ_DIAG_SURFACE_PATH)
    rows = diag_surface.get("top_rows")
    if isinstance(rows, list) and rows:
        return [r for r in rows if isinstance(r, dict)]

    eq_class = read_json(SOURCE_DOMINANCE_EQUIVALENCE_CLASS_PATH)
    rows = eq_class.get("top_rows", [])
    return [r for r in rows if isinstance(r, dict)]

def row_uid(row: Dict[str, Any], idx: int) -> str:
    return "top_row_" + str(idx) + "_" + sha8({
        "source_ref": row.get("source_ref"),
        "json_path": row.get("json_path"),
        "value": row.get("value"),
    })

def row_existing_metadata(row: Dict[str, Any]) -> Dict[str, Any]:
    existing = {}
    for key in CORE_METADATA_FIELDS:
        if key in row:
            existing[key] = row[key]
    return existing

def build_row_templates(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    field_cmp = read_json(SOURCE_EQ_FIELD_COMPARISON_PATH)
    obs_gap = read_json(SOURCE_EQ_OBSERVABILITY_GAP_PATH)
    missing_everywhere = set(obs_gap.get("missing_everywhere", []))

    templates: List[Dict[str, Any]] = []
    for idx, row in enumerate(rows):
        existing = row_existing_metadata(row)
        required_fields = []
        for field in CORE_METADATA_FIELDS:
            required_fields.append({
                "field": field,
                "role": FIELD_ROLE_MAP.get(field, "unknown"),
                "present_in_current_row": field in row,
                "missing_everywhere_in_current_surface": field in missing_everywhere,
                "value": existing.get(field),
                "required_for_distinguishability": True,
                "allowed_fill_sources": [
                    "explicit typed value-source metadata artifact",
                    "source row field if already present",
                    "prevalidated schema field",
                    "human/schema review packet"
                ],
                "forbidden_fill_methods": [
                    "latest-file guessing",
                    "mtime selection",
                    "alphabetical preference",
                    "first-seen order",
                    "unstated human preference",
                    "semantic vibe inference"
                ],
            })

        templates.append({
            "row_uid": row_uid(row, idx),
            "row_index": idx,
            "source_ref": row.get("source_ref"),
            "json_path": row.get("json_path"),
            "value": row.get("value"),
            "role": row.get("role"),
            "current_rank_features": {
                "base_dominance_score": row.get("base_dominance_score"),
                "provenance_rank": row.get("provenance_rank"),
                "field_exactness_rank": row.get("field_exactness_rank"),
                "container_role_rank": row.get("container_role_rank"),
                "explicit_rule_composite_rank": row.get("explicit_rule_composite_rank"),
                "eligible_selected_target_ref": row.get("eligible_selected_target_ref"),
            },
            "existing_metadata": existing,
            "required_metadata_fields": required_fields,
            "metadata_completion_status": "MISSING_TYPED_METADATA",
        })

    return templates

def ignored_differentiators() -> List[Dict[str, Any]]:
    field_cmp = read_json(SOURCE_EQ_FIELD_COMPARISON_PATH)
    ignored = field_cmp.get("ignored_differing_fields", {})
    rows = source_top_rows()

    out: List[Dict[str, Any]] = []
    if isinstance(ignored, dict):
        for field, values in ignored.items():
            out.append({
                "field": field,
                "current_status": "VISIBLE_BUT_IGNORED_BY_CURRENT_RULE",
                "values_by_row": values,
                "candidate_discriminator": True,
                "needs_typing_before_rule_use": field not in CORE_METADATA_FIELDS,
                "notes": "Visible difference exists, but current dominance rule did not use it as a typed discriminator.",
            })

    # Always include value/json_path as explicit differentiability probes, because diagnostic showed same_value=false.
    for field in ["value", "json_path", "source_ref"]:
        values = [{"row_index": idx, "value": row.get(field)} for idx, row in enumerate(rows)]
        unique_values = {json.dumps(v["value"], sort_keys=True) for v in values}
        out.append({
            "field": field,
            "current_status": "VISIBLE_IDENTITY_FIELD",
            "values_by_row": values,
            "unique_value_count": len(unique_values),
            "candidate_discriminator": len(unique_values) > 1,
            "needs_typing_before_rule_use": True,
            "notes": "Identity-level difference must be typed into scope/evidence/provenance before it can lawfully break a tie.",
        })

    return out

def build_metadata_surface(rows: List[Dict[str, Any]], templates: List[Dict[str, Any]], differentiators: List[Dict[str, Any]]) -> Dict[str, Any]:
    obs_gap = read_json(SOURCE_EQ_OBSERVABILITY_GAP_PATH)
    field_cmp = read_json(SOURCE_EQ_FIELD_COMPARISON_PATH)

    return {
        "schema_version": "typed_value_source_metadata_surface_v0",
        "metadata_surface_id": "metadata_surface_" + sha8({
            "source_diag": SOURCE_EQ_DIAG_RECEIPT_ID,
            "rows": rows,
            "missing": obs_gap.get("missing_everywhere", []),
        }),
        "source_equivalence_class_diagnostic_receipt_id": SOURCE_EQ_DIAG_RECEIPT_ID,
        "source_dominance_application_receipt_id": SOURCE_DOMINANCE_APPLICATION_RECEIPT_ID,
        "surface_status": "NARROWER_TYPED_VALUE_SOURCE_METADATA_SURFACE_BUILT",
        "purpose": "Expose typed metadata required to distinguish whether the three top rows are a real tie, missing discriminator, wrong comparison grain, or review boundary.",
        "receipt_backed_claim": "No row dominates under the current explicit dominance rule; real tie remains unproven.",
        "top_row_count": len(rows),
        "same_rank_surface": field_cmp.get("same_rank_surface"),
        "same_value": field_cmp.get("same_value"),
        "unique_value_count": field_cmp.get("unique_value_count"),
        "missing_typed_metadata_fields": obs_gap.get("missing_everywhere", []),
        "missing_typed_metadata_count": obs_gap.get("missing_everywhere_count"),
        "row_metadata_templates": templates,
        "candidate_discriminators": differentiators,
        "completion_rule": {
            "may_mark_field_complete_only_if": [
                "field value appears in an explicit typed metadata artifact",
                "field value is already present in source row",
                "field value is supplied by prevalidated schema",
                "field value is supplied by human/schema review packet"
            ],
            "must_not_complete_from": [
                "latest-file guessing",
                "mtime selection",
                "first-seen order",
                "alphabetical tie-break",
                "untyped semantic inference",
                "hidden preference"
            ],
        },
        "not_authorized": [
            "tie break",
            "rule refinement",
            "candidate values fill",
            "target candidate declared for review",
            "selected for build",
            "accepted for build",
            "runtime patch",
            "target file modification",
            "C5",
            "general Cell1 authority"
        ],
        "recommended_next": "EXTRACT_OR_POPULATE_TYPED_VALUE_SOURCE_METADATA_SURFACE_V0",
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def build_discriminator_surface(differentiators: List[Dict[str, Any]], templates: List[Dict[str, Any]]) -> Dict[str, Any]:
    visible_candidates = [d for d in differentiators if d.get("candidate_discriminator")]
    missing_roles = {}
    for field in CORE_METADATA_FIELDS:
        role = FIELD_ROLE_MAP.get(field, "unknown")
        missing_roles.setdefault(role, []).append(field)

    return {
        "schema_version": "typed_value_source_discriminator_candidate_surface_v0",
        "discriminator_surface_id": "discriminator_surface_" + sha8({
            "visible": visible_candidates,
            "roles": missing_roles,
        }),
        "visible_candidate_discriminator_count": len(visible_candidates),
        "visible_candidate_discriminators": visible_candidates,
        "typed_metadata_roles_required": missing_roles,
        "discriminator_status": "VISIBLE_DIFFERENCES_REQUIRE_TYPED_METADATA_BEFORE_RULE_USE",
        "possible_future_cases": [
            {
                "case": "MISSING_DISCRIMINATOR",
                "condition": "a visible ignored field receives a typed role that lawfully separates row load-bearingness or scope",
                "next": "ADD_VALUE_SOURCE_EQUIVALENCE_CLASS_REFINEMENT_RULE_V0",
            },
            {
                "case": "WRONG_COMPARISON_GRAIN",
                "condition": "target_scope/target_aspect/comparison_grain differs across rows",
                "next": "SPLIT_VALUE_SOURCE_COMPARISON_GRAIN_V0",
            },
            {
                "case": "TRUE_EQUIVALENCE",
                "condition": "all typed metadata is complete and no lawful discriminator emerges",
                "next": "EMIT_VALUE_SOURCE_EQUIVALENCE_CLASS_REVIEW_PACKET_V0",
            },
            {
                "case": "HUMAN_OR_SCHEMA_PREFERENCE_BOUNDARY",
                "condition": "machine-visible metadata is complete but selection depends on schema preference/human boundary",
                "next": "EMIT_VALUE_SOURCE_EQUIVALENCE_CLASS_REVIEW_PACKET_V0",
            },
        ],
    }

def build_extraction_request(templates: List[Dict[str, Any]], differentiators: List[Dict[str, Any]]) -> Dict[str, Any]:
    rows = []
    for template in templates:
        rows.append({
            "row_uid": template["row_uid"],
            "row_index": template["row_index"],
            "source_ref": template["source_ref"],
            "json_path": template["json_path"],
            "value": template["value"],
            "required_fields": [
                {
                    "field": item["field"],
                    "role": item["role"],
                    "required_for_distinguishability": item["required_for_distinguishability"],
                    "current_value": item["value"],
                    "status": "PRESENT" if item["present_in_current_row"] else "MISSING",
                }
                for item in template["required_metadata_fields"]
            ],
        })

    return {
        "schema_version": "typed_value_source_metadata_extraction_request_v0",
        "request_id": "metadata_extraction_request_" + sha8(rows),
        "request_status": "TYPED_VALUE_SOURCE_METADATA_EXTRACTION_REQUESTED",
        "source_metadata_surface_ref": rel(METADATA_SURFACE_PATH),
        "row_count": len(rows),
        "rows": rows,
        "visible_candidate_discriminators_ref": rel(DISCRIMINATOR_CANDIDATE_SURFACE_PATH),
        "required_output_contract": {
            "object_type": "TYPED_VALUE_SOURCE_METADATA_POPULATION_PACKET",
            "schema_version": "typed_value_source_metadata_population_packet_v0",
            "required_per_row_fields": CORE_METADATA_FIELDS,
            "must_preserve_row_uid": True,
            "must_not_select_target": True,
            "must_not_break_tie": True,
            "must_not_accept_for_build": True,
            "must_not_apply_patch": True,
        },
        "recommended_next": "EXTRACT_OR_POPULATE_TYPED_VALUE_SOURCE_METADATA_SURFACE_V0",
    }

def classify_surface(surface: Dict[str, Any], templates: List[Dict[str, Any]]) -> Tuple[str, List[str], str]:
    missing_count = int(surface.get("missing_typed_metadata_count") or 0)
    visible_discriminators = [
        d for d in surface.get("candidate_discriminators", [])
        if d.get("candidate_discriminator")
    ]
    complete_rows = [
        t for t in templates
        if all(item["present_in_current_row"] for item in t["required_metadata_fields"])
    ]

    reason_codes: List[str] = []

    if missing_count > 0:
        reason_codes.append("MISSING_TYPED_METADATA_FIELDS_EXPOSED")
    if visible_discriminators:
        reason_codes.append("VISIBLE_IGNORED_DIFFERENTIATORS_REQUIRE_TYPING")
    if len(complete_rows) < len(templates):
        reason_codes.append("ROW_METADATA_TEMPLATES_INCOMPLETE")
    if surface.get("unique_value_count") and surface.get("unique_value_count") > 1:
        reason_codes.append("ROWS_HAVE_DISTINCT_VALUES_BUT_NO_TYPED_DISCRIMINATOR")

    status = "NARROWER_TYPED_VALUE_SOURCE_METADATA_SURFACE_BUILT_NEEDS_POPULATION"
    next_edge = "EXTRACT_OR_POPULATE_TYPED_VALUE_SOURCE_METADATA_SURFACE_V0"

    return status, reason_codes, next_edge

def classification_obj(status: str, reason_codes: List[str], next_edge: str, surface: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_surface_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "top_row_count": surface["top_row_count"],
        "missing_typed_metadata_count": surface["missing_typed_metadata_count"],
        "candidate_discriminator_count": len([d for d in surface["candidate_discriminators"] if d.get("candidate_discriminator")]),
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

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_surface_authority_boundary_v0",
        "status": status,
        "may_build_metadata_surface": True,
        "may_emit_row_templates": True,
        "may_emit_discriminator_candidates": True,
        "may_request_metadata_population": True,
        "may_populate_metadata": False,
        "may_refine_rule": False,
        "may_break_tie": False,
        "may_emit_candidate_values": False,
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

def rollup_obj(status: str, surface: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_surface_rollup_v0",
        "build_mode": BUILD_MODE,
        "metadata_surface_emitted_count": 1,
        "row_metadata_template_emitted_count": 1,
        "discriminator_candidate_surface_emitted_count": 1,
        "metadata_extraction_request_emitted_count": 1,
        "classification_status": status,
        "top_row_count": surface["top_row_count"],
        "missing_typed_metadata_count": surface["missing_typed_metadata_count"],
        "candidate_discriminator_count": len([d for d in surface["candidate_discriminators"] if d.get("candidate_discriminator")]),
        "metadata_populated_count": 0,
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
        "metadata_populated_count",
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
        "schema_version": "typed_value_source_metadata_surface_profile_v0",
        "profile_id": "metadata_surface_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "metadata_surface_built": True,
        "metadata_populated": False,
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

def report_obj(status: str, reason_codes: List[str], surface: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_metadata_surface_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "No row dominates under current explicit rule; real tie remains unproven.",
        "top_row_count": surface["top_row_count"],
        "same_rank_surface": surface["same_rank_surface"],
        "same_value": surface["same_value"],
        "unique_value_count": surface["unique_value_count"],
        "missing_typed_metadata_count": surface["missing_typed_metadata_count"],
        "candidate_discriminator_count": len([d for d in surface["candidate_discriminators"] if d.get("candidate_discriminator")]),
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "metadata_populated_count": 0,
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
        "schema_version": "typed_value_source_metadata_surface_transition_trace_v0",
        "trace": [
            {
                "step": "consume_equivalence_class_diagnostic",
                "question": "is this a real tie or unresolved distinguishability",
                "answer": EXPECTED_PRIMARY_CASE,
                "taken": "build_typed_metadata_surface",
            },
            {
                "step": "materialize_metadata_requirements",
                "question": "what metadata must exist before lawful tie refinement",
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
    failures = validate_source_basis()

    if failures:
        rows: List[Dict[str, Any]] = []
        templates: List[Dict[str, Any]] = []
        differentiators: List[Dict[str, Any]] = []
        surface = {
            "schema_version": "typed_value_source_metadata_surface_v0",
            "metadata_surface_id": "metadata_surface_source_fail_" + sha8(failures),
            "surface_status": "TYPED_METADATA_SURFACE_SOURCE_BASIS_FAIL",
            "purpose": "Source basis failed; metadata surface cannot be built.",
            "top_row_count": 0,
            "same_rank_surface": None,
            "same_value": None,
            "unique_value_count": None,
            "missing_typed_metadata_fields": CORE_METADATA_FIELDS,
            "missing_typed_metadata_count": len(CORE_METADATA_FIELDS),
            "row_metadata_templates": [],
            "candidate_discriminators": [],
            "recommended_next": "REPAIR_TYPED_VALUE_SOURCE_METADATA_SURFACE_BASIS_V0",
            "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        }
        status = "TYPED_METADATA_SURFACE_SOURCE_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_TYPED_VALUE_SOURCE_METADATA_SURFACE_BASIS_V0"
    else:
        rows = source_top_rows()
        templates = build_row_templates(rows)
        differentiators = ignored_differentiators()
        surface = build_metadata_surface(rows, templates, differentiators)
        status, reason_codes, next_edge = classify_surface(surface, templates)

    discriminator_surface = build_discriminator_surface(differentiators, templates)
    extraction_request = build_extraction_request(templates, differentiators)

    classif = classification_obj(status, reason_codes, next_edge, surface)
    boundary = authority_boundary_obj(status)
    roll = rollup_obj(status, surface, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, surface, next_edge)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    write_json(METADATA_SURFACE_PATH, surface)
    write_json(ROW_METADATA_TEMPLATE_PATH, {
        "schema_version": "typed_value_source_row_metadata_template_v0",
        "template_status": "ROW_METADATA_TEMPLATES_EMITTED",
        "row_count": len(templates),
        "required_fields": CORE_METADATA_FIELDS,
        "row_metadata_templates": templates,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    })
    write_json(DISCRIMINATOR_CANDIDATE_SURFACE_PATH, discriminator_surface)
    write_json(METADATA_EXTRACTION_REQUEST_PATH, extraction_request)
    write_json(CLASSIFICATION_PATH, classif)
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
        "METADATA_SURFACE_0_DIAGNOSTIC_RECEIPT_CONSUMED": SOURCE_EQ_DIAG_RECEIPT_PATH.exists(),
        "METADATA_SURFACE_1_FIELD_COMPARISON_CONSUMED": SOURCE_EQ_FIELD_COMPARISON_PATH.exists(),
        "METADATA_SURFACE_2_OBSERVABILITY_GAP_CONSUMED": SOURCE_EQ_OBSERVABILITY_GAP_PATH.exists(),
        "METADATA_SURFACE_3_METADATA_SURFACE_EMITTED": METADATA_SURFACE_PATH.exists(),
        "METADATA_SURFACE_4_ROW_TEMPLATE_EMITTED": ROW_METADATA_TEMPLATE_PATH.exists(),
        "METADATA_SURFACE_5_DISCRIMINATOR_SURFACE_EMITTED": DISCRIMINATOR_CANDIDATE_SURFACE_PATH.exists(),
        "METADATA_SURFACE_6_EXTRACTION_REQUEST_EMITTED": METADATA_EXTRACTION_REQUEST_PATH.exists(),
        "METADATA_SURFACE_7_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "METADATA_SURFACE_8_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "METADATA_SURFACE_9_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "METADATA_SURFACE_10_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "METADATA_SURFACE_11_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classif["target_candidate_declared_for_review"] is False,
        "METADATA_SURFACE_12_NO_TARGET_SELECTED_FOR_BUILD": classif["target_selected_for_build"] is False,
        "METADATA_SURFACE_13_NO_ACCEPTED_FOR_BUILD": classif["accepted_for_build"] is False,
        "METADATA_SURFACE_14_NO_RUNTIME_PATCH": classif["runtime_patch_authorized"] is False,
        "METADATA_SURFACE_15_NO_TARGET_FILE_MODIFICATION": classif["target_file_modification_authorized"] is False,
        "METADATA_SURFACE_16_NO_C5_OPENED": classif["c5_authorized"] is False,
        "METADATA_SURFACE_17_NO_GENERAL_CELL1_AUTHORITY": classif["general_cell1_authority_granted"] is False,
        "METADATA_SURFACE_18_NO_LATEST_FILE_GUESSING": classif["latest_file_guessing"] is False,
        "METADATA_SURFACE_19_NO_MTIME_SELECTION": classif["mtime_selection"] is False,
        "METADATA_SURFACE_20_NO_HIDDEN_NEXT_COMMAND": classif["next_command_goal"] is None,
        "METADATA_SURFACE_21_ACCEPTANCE_BOUNDARY_RETAINED": classif["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "METADATA_SURFACE_22_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_VALUE_SOURCE_METADATA_SURFACE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "surface": surface.get("metadata_surface_id"),
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_value_source_metadata_surface_receipt_v0",
        "receipt_type": "TYPED_VALUE_SOURCE_METADATA_SURFACE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_equivalence_class_diagnostic_receipt_id": SOURCE_EQ_DIAG_RECEIPT_ID,
        "source_dominance_application_receipt_id": SOURCE_DOMINANCE_APPLICATION_RECEIPT_ID,
        "typed_metadata_surface_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "top_row_count": surface.get("top_row_count"),
            "same_rank_surface": surface.get("same_rank_surface"),
            "same_value": surface.get("same_value"),
            "unique_value_count": surface.get("unique_value_count"),
            "missing_typed_metadata_count": surface.get("missing_typed_metadata_count"),
            "candidate_discriminator_count": len([d for d in surface.get("candidate_discriminators", []) if d.get("candidate_discriminator")]),
            "metadata_surface_built": True,
            "metadata_populated": False,
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
            "metadata_surface": rel(METADATA_SURFACE_PATH),
            "row_metadata_template": rel(ROW_METADATA_TEMPLATE_PATH),
            "discriminator_candidate_surface": rel(DISCRIMINATOR_CANDIDATE_SURFACE_PATH),
            "metadata_extraction_request": rel(METADATA_EXTRACTION_REQUEST_PATH),
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
    print(f"metadata_surface_receipt_id={receipt_id}")
    print(f"metadata_surface_receipt_path={rel(receipt_path)}")
    print(f"metadata_surface_path={rel(METADATA_SURFACE_PATH)}")
    print(f"row_metadata_template_path={rel(ROW_METADATA_TEMPLATE_PATH)}")
    print(f"discriminator_candidate_surface_path={rel(DISCRIMINATOR_CANDIDATE_SURFACE_PATH)}")
    print(f"metadata_extraction_request_path={rel(METADATA_EXTRACTION_REQUEST_PATH)}")
    print(f"metadata_surface_classification_path={rel(CLASSIFICATION_PATH)}")
    print(f"metadata_surface_rollup_path={rel(ROLLUP_PATH)}")
    print(f"metadata_surface_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
