#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_VALUE_SOURCE_EQUIVALENCE_CLASS_DIAGNOSTIC_SURFACE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_equivalence_class_diagnostic_surface.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_EQUIVALENCE_CLASS_DIAGNOSTIC"
MODE = "DIAGNOSTIC_SURFACE / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "EQUIVALENCE_CLASS_OBSERVABILITY_ONLY"

SOURCE_DOMINANCE_APPLICATION_RECEIPT_ID = "3ebaf16f"
SOURCE_DOMINANCE_APPLICATION_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_application_v0_receipts/3ebaf16f.json"
SOURCE_DOMINANCE_APPLICATION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_application_v0/explicit_runtime_patch_target_value_source_dominance_rule_application_table_v0.json"
SOURCE_DOMINANCE_EQUIVALENCE_CLASS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_application_v0/explicit_runtime_patch_target_value_source_dominance_rule_equivalence_class_v0.json"
SOURCE_DOMINANCE_APPLICATION_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_application_v0/explicit_runtime_patch_target_value_source_dominance_rule_application_classification_v0.json"
SOURCE_DOMINANCE_APPLICATION_VALUES_PROPOSAL_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_application_v0/explicit_runtime_patch_target_value_source_dominance_rule_application_values_proposal_v0.json"

SOURCE_DOMINANCE_RULE_RECEIPT_ID = "028af962"
SOURCE_DOMINANCE_RULE_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_v0_receipts/028af962.json"
SOURCE_DOMINANCE_RULE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_v0/explicit_runtime_patch_target_value_source_dominance_rule_v0.json"

SOURCE_NARROWING_RECEIPT_ID = "e89512e0"
SOURCE_NARROWING_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0_receipts/e89512e0.json"
SOURCE_NARROWING_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0/runtime_patch_target_value_source_narrowing_table_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_equivalence_class_diagnostic_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_equivalence_class_diagnostic_v0_receipts"

DIAGNOSTIC_SURFACE_PATH = OUT_DIR / "value_source_equivalence_class_diagnostic_surface_v0.json"
FIELD_COMPARISON_PATH = OUT_DIR / "value_source_equivalence_class_field_comparison_v0.json"
OBSERVABILITY_GAP_PATH = OUT_DIR / "value_source_equivalence_class_observability_gap_v0.json"
CASE_CLASSIFICATION_PATH = OUT_DIR / "value_source_equivalence_class_case_classification_v0.json"
NEXT_EDGE_RECOMMENDATION_PATH = OUT_DIR / "value_source_equivalence_class_next_edge_recommendation_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "value_source_equivalence_class_diagnostic_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "value_source_equivalence_class_diagnostic_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "value_source_equivalence_class_diagnostic_profile_v0.json"
REPORT_PATH = OUT_DIR / "value_source_equivalence_class_diagnostic_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "value_source_equivalence_class_diagnostic_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_DOMINANCE_APPLICATION_RECEIPT_PATH,
    SOURCE_DOMINANCE_APPLICATION_TABLE_PATH,
    SOURCE_DOMINANCE_EQUIVALENCE_CLASS_PATH,
    SOURCE_DOMINANCE_APPLICATION_CLASSIFICATION_PATH,
    SOURCE_DOMINANCE_APPLICATION_VALUES_PROPOSAL_PATH,
    SOURCE_DOMINANCE_RULE_RECEIPT_PATH,
    SOURCE_DOMINANCE_RULE_PATH,
    SOURCE_NARROWING_RECEIPT_PATH,
    SOURCE_NARROWING_TABLE_PATH,
]

EXPECTED_SOURCE_STATUS = "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_STILL_MULTIPLE_TOP_ROWS"
EXPECTED_SOURCE_STOP = "STOP_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_STILL_MULTIPLE_TOP_ROWS"
EXPECTED_EQUIVALENCE_STATUS = "TOP_ROW_EQUIVALENCE_CLASS_REMAINS"

RANK_FEATURES = [
    "base_dominance_score",
    "provenance_rank",
    "field_exactness_rank",
    "container_role_rank",
    "explicit_rule_composite_rank",
    "eligible_selected_target_ref",
    "role",
]

NON_RULE_IDENTITY_FIELDS = [
    "source_ref",
    "json_path",
    "value",
    "source_kind",
    "positive_reasons",
    "rejection_reasons",
]

DESIRED_TYPED_METADATA_FIELDS = [
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

    app_receipt = read_json(SOURCE_DOMINANCE_APPLICATION_RECEIPT_PATH)
    app_table = read_json(SOURCE_DOMINANCE_APPLICATION_TABLE_PATH)
    eq = read_json(SOURCE_DOMINANCE_EQUIVALENCE_CLASS_PATH)
    app_class = read_json(SOURCE_DOMINANCE_APPLICATION_CLASSIFICATION_PATH)
    values = read_json(SOURCE_DOMINANCE_APPLICATION_VALUES_PROPOSAL_PATH)
    rule_receipt = read_json(SOURCE_DOMINANCE_RULE_RECEIPT_PATH)
    narrowing_receipt = read_json(SOURCE_NARROWING_RECEIPT_PATH)

    summary = app_receipt.get("dominance_rule_application_summary", {})

    if app_receipt.get("receipt_id") != SOURCE_DOMINANCE_APPLICATION_RECEIPT_ID or app_receipt.get("gate") != "PASS":
        failures.append("dominance_application_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"dominance_application_status_not_expected:{summary.get('status')}")
    if app_receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("dominance_application_terminal_not_expected")
    if summary.get("rule_applied") is not True:
        failures.append("rule_not_applied_in_source")
    if summary.get("top_row_count_after_application") != 3:
        failures.append(f"top_row_count_not_3:{summary.get('top_row_count_after_application')}")
    if summary.get("equivalence_class_status") != EXPECTED_EQUIVALENCE_STATUS:
        failures.append(f"equivalence_status_not_expected:{summary.get('equivalence_class_status')}")
    if summary.get("proposal_ready") is not False:
        failures.append("source_proposal_ready_unexpectedly")
    if summary.get("target_selected_for_build") is not False:
        failures.append("source_selected_target_for_build")
    if summary.get("accepted_for_build") is not False:
        failures.append("source_accepted_for_build")
    if summary.get("runtime_patch_applied") is not False:
        failures.append("source_runtime_patch_applied")

    if app_table.get("application_status") != EXPECTED_SOURCE_STATUS:
        failures.append("application_table_status_not_expected")
    if app_table.get("top_row_count_after_application") != 3:
        failures.append("application_table_top_count_not_3")

    if eq.get("equivalence_status") != EXPECTED_EQUIVALENCE_STATUS:
        failures.append("equivalence_class_artifact_status_not_expected")
    if eq.get("top_row_count") != 3:
        failures.append("equivalence_class_top_count_not_3")

    if app_class.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("application_classification_status_not_expected")
    if app_class.get("target_selected_for_build") is not False:
        failures.append("application_classification_selected_target_for_build")
    if app_class.get("accepted_for_build") is not False:
        failures.append("application_classification_accepted_for_build")
    if app_class.get("runtime_patch_authorized") is not False:
        failures.append("application_classification_authorizes_runtime_patch")

    if values.get("proposal_status") != EXPECTED_SOURCE_STATUS:
        failures.append("values_proposal_status_not_expected")
    if values.get("candidate_values") not in ({}, None):
        failures.append("values_proposal_has_candidate_values_unexpectedly")

    if rule_receipt.get("receipt_id") != SOURCE_DOMINANCE_RULE_RECEIPT_ID or rule_receipt.get("gate") != "PASS":
        failures.append("dominance_rule_receipt_not_pass")

    if narrowing_receipt.get("receipt_id") != SOURCE_NARROWING_RECEIPT_ID or narrowing_receipt.get("gate") != "PASS":
        failures.append("narrowing_receipt_not_pass")

    return failures

def render_value(value: Any) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False)

def top_rows() -> List[Dict[str, Any]]:
    eq = read_json(SOURCE_DOMINANCE_EQUIVALENCE_CLASS_PATH)
    rows = eq.get("top_rows", [])
    if isinstance(rows, list) and rows:
        return [r for r in rows if isinstance(r, dict)]

    app = read_json(SOURCE_DOMINANCE_APPLICATION_TABLE_PATH)
    rows = app.get("top_rows_after_application", [])
    return [r for r in rows if isinstance(r, dict)]

def compare_rows(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    all_keys = sorted({k for row in rows for k in row.keys()})
    shared: Dict[str, Any] = {}
    differing: Dict[str, Any] = {}
    missing_by_field: Dict[str, Any] = {}

    for key in all_keys:
        vals = [row.get(key) for row in rows]
        rendered = {render_value(v) for v in vals}
        absent_count = sum(1 for row in rows if key not in row)
        if len(rendered) == 1:
            shared[key] = vals[0] if vals else None
        else:
            differing[key] = [
                {"row_index": i, "value": row.get(key)}
                for i, row in enumerate(rows)
            ]
        if absent_count:
            missing_by_field[key] = absent_count

    rank_shared = {k: shared.get(k) for k in RANK_FEATURES if k in shared}
    rank_differing = {k: differing.get(k) for k in RANK_FEATURES if k in differing}
    ignored_differing = {
        k: v for k, v in differing.items()
        if k not in RANK_FEATURES
    }

    identity_differing = {
        k: differing[k] for k in NON_RULE_IDENTITY_FIELDS
        if k in differing
    }

    suffixes = []
    for row in rows:
        p = str(row.get("json_path", ""))
        suffixes.append(p.split(".")[-1] if p else "")

    values = [row.get("value") for row in rows]
    sources = [row.get("source_ref") for row in rows]
    roles = [row.get("role") for row in rows]

    return {
        "schema_version": "value_source_equivalence_class_field_comparison_v0",
        "field_comparison_id": "field_compare_" + sha8(rows),
        "top_row_count": len(rows),
        "all_fields": all_keys,
        "shared_fields": shared,
        "differing_fields": differing,
        "missing_by_field": missing_by_field,
        "rank_features_shared": rank_shared,
        "rank_features_differing": rank_differing,
        "ignored_differing_fields": ignored_differing,
        "identity_differing_fields": identity_differing,
        "json_path_suffixes": suffixes,
        "unique_json_path_suffix_count": len(set(suffixes)),
        "unique_value_count": len({render_value(v) for v in values}),
        "unique_source_ref_count": len({render_value(v) for v in sources}),
        "unique_role_count": len({render_value(v) for v in roles}),
        "same_rank_surface": len(rank_differing) == 0,
        "same_role": len({render_value(v) for v in roles}) <= 1,
        "same_value": len({render_value(v) for v in values}) <= 1,
        "source_refs": sources,
        "values": values,
        "top_rows": rows,
    }

def observability_gap(rows: List[Dict[str, Any]], comparison: Dict[str, Any]) -> Dict[str, Any]:
    present_keys = {k for row in rows for k in row.keys()}
    missing_everywhere = [k for k in DESIRED_TYPED_METADATA_FIELDS if k not in present_keys]

    partially_missing = []
    for key in DESIRED_TYPED_METADATA_FIELDS:
        present_count = sum(1 for row in rows if key in row)
        if 0 < present_count < len(rows):
            partially_missing.append({
                "field": key,
                "present_count": present_count,
                "missing_count": len(rows) - present_count,
            })

    ignored_diff_count = len(comparison["ignored_differing_fields"])
    identity_diff_count = len(comparison["identity_differing_fields"])

    return {
        "schema_version": "value_source_equivalence_class_observability_gap_v0",
        "observability_gap_id": "obs_gap_" + sha8({
            "missing": missing_everywhere,
            "partial": partially_missing,
            "ignored_diff_count": ignored_diff_count,
            "identity_diff_count": identity_diff_count,
        }),
        "top_row_count": len(rows),
        "desired_typed_metadata_fields": DESIRED_TYPED_METADATA_FIELDS,
        "missing_everywhere": missing_everywhere,
        "missing_everywhere_count": len(missing_everywhere),
        "partially_missing": partially_missing,
        "partially_missing_count": len(partially_missing),
        "ignored_differing_field_count": ignored_diff_count,
        "identity_differing_field_count": identity_diff_count,
        "diagnostic_observation": (
            "The current top rows tie on rule rank features, but the surface lacks typed metadata needed to distinguish true equivalence "
            "from unresolved distinguishability."
            if len(missing_everywhere) else
            "The current top rows have available typed metadata; remaining non-dominance may need a discriminator or review boundary."
        ),
    }

def classify_case(rows: List[Dict[str, Any]], comparison: Dict[str, Any], gap: Dict[str, Any]) -> Tuple[str, List[str], List[str], str]:
    reason_codes: List[str] = []
    case_signals: List[str] = []

    top_count = len(rows)
    if top_count <= 1:
        return (
            "NO_EQUIVALENCE_CLASS_TO_CHARACTERIZE",
            ["TOP_ROW_COUNT_NOT_MULTIPLE"],
            [],
            "RETURN_TO_DOMINANCE_RULE_APPLICATION_REVIEW_V0",
        )

    if comparison["same_rank_surface"]:
        reason_codes.append("ROWS_IDENTICAL_UNDER_CURRENT_RULE_RANK_FEATURES")
    else:
        reason_codes.append("ROWS_DIFFER_UNDER_RULE_RANK_FEATURES")

    if comparison["ignored_differing_fields"]:
        reason_codes.append("ROWS_HAVE_DIFFERENCES_IGNORED_BY_CURRENT_RULE")
        case_signals.append("MISSING_DISCRIMINATOR_CANDIDATE")

    if comparison["unique_json_path_suffix_count"] > 1 or comparison["unique_role_count"] > 1:
        reason_codes.append("ROWS_MAY_NOT_SHARE_SAME_COMPARISON_GRAIN")
        case_signals.append("WRONG_COMPARISON_GRAIN_CANDIDATE")

    if gap["missing_everywhere_count"] >= 5:
        reason_codes.append("TYPED_METADATA_MISSING_FOR_DISTINGUISHABILITY")
        case_signals.append("MISSING_TYPED_SOURCE_METADATA")

    if comparison["same_rank_surface"] and not comparison["ignored_differing_fields"] and gap["missing_everywhere_count"] == 0:
        reason_codes.append("NO_VISIBLE_DIFFERENTIATOR_AFTER_DIAGNOSTIC")
        case_signals.append("TRUE_EQUIVALENCE_CANDIDATE")

    if comparison["same_rank_surface"] and comparison["ignored_differing_fields"] and gap["missing_everywhere_count"] > 0:
        primary = "UNRESOLVED_DISTINGUISHABILITY_DUE_TO_MISSING_TYPED_METADATA"
        next_edge = "BUILD_NARROWER_TYPED_VALUE_SOURCE_METADATA_SURFACE_V0"
    elif "WRONG_COMPARISON_GRAIN_CANDIDATE" in case_signals:
        primary = "WRONG_COMPARISON_GRAIN_CANDIDATE"
        next_edge = "SPLIT_VALUE_SOURCE_COMPARISON_GRAIN_V0"
    elif "MISSING_DISCRIMINATOR_CANDIDATE" in case_signals:
        primary = "MISSING_DISCRIMINATOR_CANDIDATE"
        next_edge = "ADD_VALUE_SOURCE_EQUIVALENCE_CLASS_REFINEMENT_RULE_V0"
    elif "TRUE_EQUIVALENCE_CANDIDATE" in case_signals:
        primary = "TRUE_EQUIVALENCE_CANDIDATE"
        next_edge = "EMIT_VALUE_SOURCE_EQUIVALENCE_CLASS_REVIEW_PACKET_V0"
    else:
        primary = "INSUFFICIENT_OBSERVABILITY"
        next_edge = "HARDEN_VALUE_SOURCE_EQUIVALENCE_CLASS_DIAGNOSTIC_SURFACE_V0"

    return primary, reason_codes, case_signals, next_edge

def diagnostic_surface_obj(rows: List[Dict[str, Any]], comparison: Dict[str, Any], gap: Dict[str, Any], primary_case: str, reason_codes: List[str], case_signals: List[str], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "value_source_equivalence_class_diagnostic_surface_v0",
        "diagnostic_surface_id": "eq_diag_" + sha8({
            "rows": rows,
            "primary_case": primary_case,
            "reason_codes": reason_codes,
        }),
        "source_application_receipt_id": SOURCE_DOMINANCE_APPLICATION_RECEIPT_ID,
        "source_application_receipt_ref": rel(SOURCE_DOMINANCE_APPLICATION_RECEIPT_PATH),
        "source_equivalence_class_ref": rel(SOURCE_DOMINANCE_EQUIVALENCE_CLASS_PATH),
        "diagnostic_status": "VALUE_SOURCE_EQUIVALENCE_CLASS_CHARACTERIZED",
        "top_row_count": len(rows),
        "receipt_backed_claim": "No row dominates under the current explicit value-source dominance rule.",
        "not_proven": [
            "the rows are semantically equivalent",
            "the rows are equally load-bearing",
            "the rows should remain tied under a better comparison surface",
            "human/schema preference is required",
            "a refined dominance rule would be lawful"
        ],
        "primary_case": primary_case,
        "case_signals": case_signals,
        "reason_codes": reason_codes,
        "field_comparison_ref": rel(FIELD_COMPARISON_PATH),
        "observability_gap_ref": rel(OBSERVABILITY_GAP_PATH),
        "recommended_next": next_edge,
        "top_rows": rows,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
    }

def case_classification_obj(primary_case: str, reason_codes: List[str], case_signals: List[str], next_edge: str, comparison: Dict[str, Any], gap: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "value_source_equivalence_class_case_classification_v0",
        "classification_status": "VALUE_SOURCE_EQUIVALENCE_CLASS_CHARACTERIZED",
        "primary_case": primary_case,
        "case_signals": case_signals,
        "reason_codes": reason_codes,
        "is_true_equivalence_proven": primary_case == "TRUE_EQUIVALENCE_CANDIDATE" and gap["missing_everywhere_count"] == 0,
        "is_current_rule_tie": True,
        "is_real_tie_proven": False,
        "same_rank_surface": comparison["same_rank_surface"],
        "ignored_differing_field_count": len(comparison["ignored_differing_fields"]),
        "missing_typed_metadata_count": gap["missing_everywhere_count"],
        "unique_json_path_suffix_count": comparison["unique_json_path_suffix_count"],
        "unique_value_count": comparison["unique_value_count"],
        "recommended_next": next_edge,
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
        "next_command_goal": None,
    }

def next_edge_obj(primary_case: str, next_edge: str, reason_codes: List[str]) -> Dict[str, Any]:
    edge_map = {
        "TRUE_EQUIVALENCE_CANDIDATE": "preserve equivalence class and emit review packet; do not fabricate target values",
        "MISSING_DISCRIMINATOR_CANDIDATE": "add a refined dominance rule based on visible ignored differentiators",
        "WRONG_COMPARISON_GRAIN_CANDIDATE": "split the value-source comparison surface before ranking",
        "UNRESOLVED_DISTINGUISHABILITY_DUE_TO_MISSING_TYPED_METADATA": "build a narrower typed metadata surface exposing scope, evidence strength, provenance, and inference strength",
        "INSUFFICIENT_OBSERVABILITY": "harden the diagnostic surface before refining any rule",
    }
    return {
        "schema_version": "value_source_equivalence_class_next_edge_recommendation_v0",
        "primary_case": primary_case,
        "recommended_next": next_edge,
        "reason_codes": reason_codes,
        "edge_rationale": edge_map.get(primary_case, "return to diagnostic review"),
        "forbidden_next_moves": [
            "select one of the three rows by preference",
            "use latest-file guessing",
            "use mtime selection",
            "declare candidate for review before diagnostic classification is accepted",
            "apply runtime patch",
            "open C5",
            "grant general Cell1 authority"
        ],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def authority_boundary_obj(primary_case: str) -> Dict[str, Any]:
    return {
        "schema_version": "value_source_equivalence_class_diagnostic_authority_boundary_v0",
        "status": "VALUE_SOURCE_EQUIVALENCE_CLASS_CHARACTERIZED",
        "primary_case": primary_case,
        "may_inspect_equivalence_class": True,
        "may_compare_top_rows": True,
        "may_emit_case_classification": True,
        "may_emit_next_edge_recommendation": True,
        "may_refine_dominance_rule": False,
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

def rollup_obj(primary_case: str, next_edge: str, comparison: Dict[str, Any], gap: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "value_source_equivalence_class_diagnostic_rollup_v0",
        "build_mode": BUILD_MODE,
        "diagnostic_surface_emitted_count": 1,
        "field_comparison_emitted_count": 1,
        "observability_gap_emitted_count": 1,
        "case_classification_emitted_count": 1,
        "next_edge_recommendation_emitted_count": 1,
        "primary_case": primary_case,
        "recommended_next": next_edge,
        "top_row_count": comparison["top_row_count"],
        "same_rank_surface": comparison["same_rank_surface"],
        "ignored_differing_field_count": len(comparison["ignored_differing_fields"]),
        "missing_typed_metadata_count": gap["missing_everywhere_count"],
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
    }

def profile_obj(roll: Dict[str, Any]) -> Dict[str, Any]:
    zero_keys = [
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
        "schema_version": "value_source_equivalence_class_diagnostic_profile_v0",
        "profile_id": "eq_diag_profile_" + sha8(roll),
        "status": "VALUE_SOURCE_EQUIVALENCE_CLASS_CHARACTERIZED",
        "primary_case": roll["primary_case"],
        "diagnostic_surface_emitted": True,
        "tie_broken": False,
        "rule_refined": False,
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

def report_obj(primary_case: str, reason_codes: List[str], next_edge: str, comparison: Dict[str, Any], gap: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "value_source_equivalence_class_diagnostic_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": "VALUE_SOURCE_EQUIVALENCE_CLASS_CHARACTERIZED",
        "primary_case": primary_case,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "No row dominates under current explicit rule.",
        "real_tie_proven": False,
        "top_row_count": comparison["top_row_count"],
        "same_rank_surface": comparison["same_rank_surface"],
        "ignored_differing_field_count": len(comparison["ignored_differing_fields"]),
        "missing_typed_metadata_count": gap["missing_everywhere_count"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
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

def transition_trace_obj(primary_case: str, next_edge: str, reason_codes: List[str]) -> Dict[str, Any]:
    return {
        "schema_version": "value_source_equivalence_class_diagnostic_transition_trace_v0",
        "trace": [
            {
                "step": "consume_applied_current_rule_tie",
                "question": "what does the prior receipt prove",
                "answer": "no row dominates under current explicit rule",
                "taken": "diagnose_equivalence_class_before_refinement",
            },
            {
                "step": "compare_top_rows",
                "question": "is this true equivalence or unresolved distinguishability",
                "answer": primary_case,
                "reason_codes": reason_codes,
                "taken": next_edge,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_VALUE_SOURCE_EQUIVALENCE_CLASS_CHARACTERIZED",
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
        comparison = {
            "schema_version": "value_source_equivalence_class_field_comparison_v0",
            "field_comparison_id": "field_compare_source_fail_" + sha8(failures),
            "top_row_count": 0,
            "all_fields": [],
            "shared_fields": {},
            "differing_fields": {},
            "missing_by_field": {},
            "rank_features_shared": {},
            "rank_features_differing": {},
            "ignored_differing_fields": {},
            "identity_differing_fields": {},
            "json_path_suffixes": [],
            "unique_json_path_suffix_count": 0,
            "unique_value_count": 0,
            "unique_source_ref_count": 0,
            "unique_role_count": 0,
            "same_rank_surface": False,
            "same_role": False,
            "same_value": False,
            "source_refs": [],
            "values": [],
            "top_rows": [],
        }
        gap = {
            "schema_version": "value_source_equivalence_class_observability_gap_v0",
            "observability_gap_id": "obs_gap_source_fail_" + sha8(failures),
            "top_row_count": 0,
            "desired_typed_metadata_fields": DESIRED_TYPED_METADATA_FIELDS,
            "missing_everywhere": DESIRED_TYPED_METADATA_FIELDS,
            "missing_everywhere_count": len(DESIRED_TYPED_METADATA_FIELDS),
            "partially_missing": [],
            "partially_missing_count": 0,
            "ignored_differing_field_count": 0,
            "identity_differing_field_count": 0,
            "diagnostic_observation": "Source basis failed; diagnostic cannot characterize class.",
        }
        primary_case = "DIAGNOSTIC_SOURCE_BASIS_FAIL"
        reason_codes = failures
        case_signals: List[str] = []
        next_edge = "REPAIR_VALUE_SOURCE_EQUIVALENCE_CLASS_DIAGNOSTIC_BASIS_V0"
    else:
        rows = top_rows()
        comparison = compare_rows(rows)
        gap = observability_gap(rows, comparison)
        primary_case, reason_codes, case_signals, next_edge = classify_case(rows, comparison, gap)

    diagnostic = diagnostic_surface_obj(rows, comparison, gap, primary_case, reason_codes, case_signals, next_edge)
    case_classification = case_classification_obj(primary_case, reason_codes, case_signals, next_edge, comparison, gap)
    next_rec = next_edge_obj(primary_case, next_edge, reason_codes)
    boundary = authority_boundary_obj(primary_case)
    roll = rollup_obj(primary_case, next_edge, comparison, gap)
    prof = profile_obj(roll)
    rep = report_obj(primary_case, reason_codes, next_edge, comparison, gap)
    trace = transition_trace_obj(primary_case, next_edge, reason_codes)

    write_json(FIELD_COMPARISON_PATH, comparison)
    write_json(OBSERVABILITY_GAP_PATH, gap)
    write_json(DIAGNOSTIC_SURFACE_PATH, diagnostic)
    write_json(CASE_CLASSIFICATION_PATH, case_classification)
    write_json(NEXT_EDGE_RECOMMENDATION_PATH, next_rec)
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
        "EQ_DIAG_0_APPLICATION_RECEIPT_CONSUMED": SOURCE_DOMINANCE_APPLICATION_RECEIPT_PATH.exists(),
        "EQ_DIAG_1_EQUIVALENCE_CLASS_CONSUMED": SOURCE_DOMINANCE_EQUIVALENCE_CLASS_PATH.exists(),
        "EQ_DIAG_2_DIAGNOSTIC_SURFACE_EMITTED": DIAGNOSTIC_SURFACE_PATH.exists(),
        "EQ_DIAG_3_FIELD_COMPARISON_EMITTED": FIELD_COMPARISON_PATH.exists(),
        "EQ_DIAG_4_OBSERVABILITY_GAP_EMITTED": OBSERVABILITY_GAP_PATH.exists(),
        "EQ_DIAG_5_CASE_CLASSIFICATION_EMITTED": CASE_CLASSIFICATION_PATH.exists(),
        "EQ_DIAG_6_NEXT_EDGE_RECOMMENDATION_EMITTED": NEXT_EDGE_RECOMMENDATION_PATH.exists(),
        "EQ_DIAG_7_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "EQ_DIAG_8_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "EQ_DIAG_9_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "EQ_DIAG_10_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": case_classification["target_candidate_declared_for_review"] is False,
        "EQ_DIAG_11_NO_TARGET_SELECTED_FOR_BUILD": case_classification["target_selected_for_build"] is False,
        "EQ_DIAG_12_NO_ACCEPTED_FOR_BUILD": case_classification["accepted_for_build"] is False,
        "EQ_DIAG_13_NO_RUNTIME_PATCH": case_classification["runtime_patch_authorized"] is False,
        "EQ_DIAG_14_NO_TARGET_FILE_MODIFICATION": case_classification["target_file_modification_authorized"] is False,
        "EQ_DIAG_15_NO_C5_OPENED": case_classification["c5_authorized"] is False,
        "EQ_DIAG_16_NO_GENERAL_CELL1_AUTHORITY": case_classification["general_cell1_authority_granted"] is False,
        "EQ_DIAG_17_NO_LATEST_FILE_GUESSING": case_classification["latest_file_guessing"] is False,
        "EQ_DIAG_18_NO_MTIME_SELECTION": case_classification["mtime_selection"] is False,
        "EQ_DIAG_19_NO_HIDDEN_NEXT_COMMAND": case_classification["next_command_goal"] is None,
        "EQ_DIAG_20_ACCEPTANCE_BOUNDARY_RETAINED": case_classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "EQ_DIAG_21_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_VALUE_SOURCE_EQUIVALENCE_CLASS_DIAGNOSTIC_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "primary_case": primary_case,
        "top_row_count": comparison["top_row_count"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "value_source_equivalence_class_diagnostic_receipt_v0",
        "receipt_type": "VALUE_SOURCE_EQUIVALENCE_CLASS_DIAGNOSTIC_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_dominance_application_receipt_id": SOURCE_DOMINANCE_APPLICATION_RECEIPT_ID,
        "source_dominance_rule_receipt_id": SOURCE_DOMINANCE_RULE_RECEIPT_ID,
        "source_narrowing_receipt_id": SOURCE_NARROWING_RECEIPT_ID,
        "equivalence_class_diagnostic_summary": {
            "status": "VALUE_SOURCE_EQUIVALENCE_CLASS_CHARACTERIZED",
            "primary_case": primary_case,
            "case_signals": case_signals,
            "reason_codes": reason_codes,
            "top_row_count": comparison["top_row_count"],
            "same_rank_surface": comparison["same_rank_surface"],
            "same_role": comparison["same_role"],
            "same_value": comparison["same_value"],
            "unique_json_path_suffix_count": comparison["unique_json_path_suffix_count"],
            "unique_value_count": comparison["unique_value_count"],
            "ignored_differing_field_count": len(comparison["ignored_differing_fields"]),
            "missing_typed_metadata_count": gap["missing_everywhere_count"],
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
            "diagnostic_surface": rel(DIAGNOSTIC_SURFACE_PATH),
            "field_comparison": rel(FIELD_COMPARISON_PATH),
            "observability_gap": rel(OBSERVABILITY_GAP_PATH),
            "case_classification": rel(CASE_CLASSIFICATION_PATH),
            "next_edge_recommendation": rel(NEXT_EDGE_RECOMMENDATION_PATH),
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
    print(f"equivalence_class_diagnostic_receipt_id={receipt_id}")
    print(f"equivalence_class_diagnostic_receipt_path={rel(receipt_path)}")
    print(f"equivalence_class_diagnostic_surface_path={rel(DIAGNOSTIC_SURFACE_PATH)}")
    print(f"equivalence_class_field_comparison_path={rel(FIELD_COMPARISON_PATH)}")
    print(f"equivalence_class_observability_gap_path={rel(OBSERVABILITY_GAP_PATH)}")
    print(f"equivalence_class_case_classification_path={rel(CASE_CLASSIFICATION_PATH)}")
    print(f"equivalence_class_next_edge_recommendation_path={rel(NEXT_EDGE_RECOMMENDATION_PATH)}")
    print(f"equivalence_class_diagnostic_rollup_path={rel(ROLLUP_PATH)}")
    print(f"equivalence_class_diagnostic_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
