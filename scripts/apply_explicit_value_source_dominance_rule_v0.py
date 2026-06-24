#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import shlex
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "APPLY_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_dominance_rule_application.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_DOMINANCE_RULE_APPLICATION"
MODE = "APPLY_RULE / EQUIVALENCE_CLASS_TEST / NO_ACCEPTANCE"
BUILD_MODE = "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLICATION_ONLY"

SOURCE_DOMINANCE_RULE_RECEIPT_ID = "028af962"
SOURCE_DOMINANCE_RULE_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_v0_receipts/028af962.json"
SOURCE_DOMINANCE_RULE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_v0/explicit_runtime_patch_target_value_source_dominance_rule_v0.json"
SOURCE_DOMINANCE_RULE_IMPACT_PREVIEW_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_v0/explicit_runtime_patch_target_value_source_dominance_rule_impact_preview_v0.json"
SOURCE_DOMINANCE_RULE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_v0/explicit_runtime_patch_target_value_source_dominance_rule_classification_v0.json"

SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_ID = "e89512e0"
SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0_receipts/e89512e0.json"
SOURCE_VALUE_SOURCE_NARROWING_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0/runtime_patch_target_value_source_narrowing_table_v0.json"
SOURCE_VALUE_SOURCE_DOMINANCE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0/runtime_patch_target_value_source_dominance_classification_v0.json"
SOURCE_VALUE_SOURCE_NARROWED_VALUES_PROPOSAL_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0/runtime_patch_target_value_source_narrowed_values_proposal_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_application_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_application_v0_receipts"

APPLICATION_TABLE_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_application_table_v0.json"
APPLICATION_EQUIVALENCE_CLASS_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_equivalence_class_v0.json"
APPLICATION_CLASSIFICATION_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_application_classification_v0.json"
APPLICATION_VALUES_PROPOSAL_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_application_values_proposal_v0.json"
APPLICATION_ENV_EXPORTS_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_application_env_exports.sh"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_application_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_application_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_application_profile_v0.json"
REPORT_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_application_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_application_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_DOMINANCE_RULE_RECEIPT_PATH,
    SOURCE_DOMINANCE_RULE_PATH,
    SOURCE_DOMINANCE_RULE_IMPACT_PREVIEW_PATH,
    SOURCE_DOMINANCE_RULE_CLASSIFICATION_PATH,
    SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_PATH,
    SOURCE_VALUE_SOURCE_NARROWING_TABLE_PATH,
    SOURCE_VALUE_SOURCE_DOMINANCE_CLASSIFICATION_PATH,
    SOURCE_VALUE_SOURCE_NARROWED_VALUES_PROPOSAL_PATH,
]

REQUIRED_ENV_FIELDS = [
    "SELECTED_TARGET_REF",
    "SELECTED_TARGET_KIND",
    "WHY_THIS_TARGET_IS_LOAD_BEARING",
    "WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON",
    "SOURCE_EVIDENCE_REFS_JSON",
    "VERIFICATION_GATE_REF",
    "ROLLBACK_OR_STOP_BOUNDARY_REF",
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

    rule_receipt = read_json(SOURCE_DOMINANCE_RULE_RECEIPT_PATH)
    rule = read_json(SOURCE_DOMINANCE_RULE_PATH)
    preview = read_json(SOURCE_DOMINANCE_RULE_IMPACT_PREVIEW_PATH)
    rule_classification = read_json(SOURCE_DOMINANCE_RULE_CLASSIFICATION_PATH)
    narrowing_receipt = read_json(SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_PATH)
    narrowing_table = read_json(SOURCE_VALUE_SOURCE_NARROWING_TABLE_PATH)
    narrowing_classification = read_json(SOURCE_VALUE_SOURCE_DOMINANCE_CLASSIFICATION_PATH)
    narrowed_values = read_json(SOURCE_VALUE_SOURCE_NARROWED_VALUES_PROPOSAL_PATH)

    rule_summary = rule_receipt.get("dominance_rule_summary", {})
    narrowing_summary = narrowing_receipt.get("value_source_narrowing_summary", {})

    if rule_receipt.get("receipt_id") != SOURCE_DOMINANCE_RULE_RECEIPT_ID or rule_receipt.get("gate") != "PASS":
        failures.append("dominance_rule_receipt_not_pass")
    if rule_receipt.get("terminal", {}).get("stop_code") != "STOP_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_ADDED":
        failures.append("dominance_rule_wrong_terminal")
    if rule_summary.get("status") != "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_ADDED":
        failures.append("dominance_rule_summary_wrong_status")
    if rule_summary.get("rule_applied") is not False:
        failures.append("dominance_rule_already_applied_in_source")
    if rule_summary.get("impact_preview_status") != "RULE_PREVIEW_STILL_MULTIPLE_TOP_ROWS":
        failures.append("dominance_rule_preview_status_not_expected")
    if rule_summary.get("impact_preview_top_row_count") != 3:
        failures.append(f"dominance_rule_preview_top_count_not_3:{rule_summary.get('impact_preview_top_row_count')}")

    if rule.get("rule_status") != "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_ADDED":
        failures.append("rule_artifact_wrong_status")
    if rule.get("application_boundary", {}).get("this_rule_does_not_apply_itself") is not True:
        failures.append("rule_boundary_does_not_state_not_self_applying")
    if rule.get("application_boundary", {}).get("acceptance_boundary") != "human_or_prevalidated_schema_acceptance_required":
        failures.append("rule_acceptance_boundary_wrong")

    if preview.get("preview_status") != "RULE_PREVIEW_STILL_MULTIPLE_TOP_ROWS":
        failures.append("preview_status_not_expected")
    if preview.get("top_row_count_under_rule_preview") != 3:
        failures.append(f"preview_top_row_count_not_3:{preview.get('top_row_count_under_rule_preview')}")
    if preview.get("preview_does_not_select_for_build") is not True:
        failures.append("preview_select_for_build_boundary_missing")
    if preview.get("preview_does_not_declare_for_review") is not True:
        failures.append("preview_declare_for_review_boundary_missing")

    if rule_classification.get("classification_status") != "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_ADDED":
        failures.append("rule_classification_wrong_status")
    if rule_classification.get("target_selected_for_build") is not False:
        failures.append("rule_classification_selects_target_for_build")
    if rule_classification.get("accepted_for_build") is not False:
        failures.append("rule_classification_accepts_for_build")
    if rule_classification.get("runtime_patch_authorized") is not False:
        failures.append("rule_classification_authorizes_runtime_patch")

    if narrowing_receipt.get("receipt_id") != SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_ID or narrowing_receipt.get("gate") != "PASS":
        failures.append("narrowing_receipt_not_pass")
    if narrowing_summary.get("status") != "VALUE_SOURCE_SURFACE_STILL_MULTIPLE_AMBIGUOUS":
        failures.append("narrowing_summary_status_not_expected")
    if narrowing_summary.get("top_dominant_row_count") != 3:
        failures.append(f"narrowing_top_count_not_3:{narrowing_summary.get('top_dominant_row_count')}")
    if narrowing_table.get("top_dominant_row_count") != 3:
        failures.append(f"narrowing_table_top_count_not_3:{narrowing_table.get('top_dominant_row_count')}")
    if narrowing_classification.get("classification_status") != "VALUE_SOURCE_SURFACE_STILL_MULTIPLE_AMBIGUOUS":
        failures.append("narrowing_classification_wrong_status")
    if narrowed_values.get("proposal_status") != "VALUE_SOURCE_SURFACE_STILL_MULTIPLE_AMBIGUOUS":
        failures.append("narrowed_values_prior_status_wrong")
    if narrowed_values.get("candidate_values") not in ({}, None):
        failures.append("prior_narrowed_values_unexpected_candidate_values")

    return failures

def build_application() -> Dict[str, Any]:
    rule = read_json(SOURCE_DOMINANCE_RULE_PATH)
    preview = read_json(SOURCE_DOMINANCE_RULE_IMPACT_PREVIEW_PATH)
    narrowing_table = read_json(SOURCE_VALUE_SOURCE_NARROWING_TABLE_PATH)

    ranked_rows = preview.get("ranked_eligible_rows", [])
    top_rows = preview.get("top_rows_under_rule_preview", [])
    top_count = preview.get("top_row_count_under_rule_preview", 0)

    if not isinstance(ranked_rows, list):
        ranked_rows = []
    if not isinstance(top_rows, list):
        top_rows = []

    if top_count == 1 and len(top_rows) == 1:
        application_status = "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_ONE_TOP_ROW"
        reason_codes = ["ONE_TOP_ROW_AFTER_RULE_APPLICATION"]
    elif top_count == 0:
        application_status = "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_NO_ELIGIBLE_ROWS"
        reason_codes = ["NO_ELIGIBLE_ROWS_AFTER_RULE_APPLICATION"]
    else:
        application_status = "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_STILL_MULTIPLE_TOP_ROWS"
        reason_codes = [
            "RULE_APPLIED_BUT_TOP_ROW_TIE_REMAINS",
            f"TOP_ROW_COUNT_{top_count}",
            "EQUIVALENCE_CLASS_REQUIRES_REFINED_DOMINANCE_RULE_OR_TYPED_SOURCE_SURFACE",
        ]

    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_application_table_v0",
        "application_table_id": "dominance_rule_application_" + sha8({
            "rule": rule.get("rule_id"),
            "preview": preview.get("preview_status"),
            "top_count": top_count,
        }),
        "source_rule_ref": rel(SOURCE_DOMINANCE_RULE_PATH),
        "source_rule_receipt_id": SOURCE_DOMINANCE_RULE_RECEIPT_ID,
        "source_impact_preview_ref": rel(SOURCE_DOMINANCE_RULE_IMPACT_PREVIEW_PATH),
        "source_narrowing_table_ref": rel(SOURCE_VALUE_SOURCE_NARROWING_TABLE_PATH),
        "application_status": application_status,
        "reason_codes": reason_codes,
        "rule_applied": True,
        "prior_preview_status": preview.get("preview_status"),
        "ranked_eligible_row_count": len(ranked_rows),
        "top_row_count_after_application": top_count,
        "top_rows_after_application": top_rows,
        "ranked_rows_after_application": ranked_rows,
        "narrowing_table_prior_counts": {
            "typed_row_count": narrowing_table.get("typed_row_count"),
            "eligible_selected_target_ref_row_count": narrowing_table.get("eligible_selected_target_ref_row_count"),
            "top_dominant_row_count": narrowing_table.get("top_dominant_row_count"),
        },
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

def build_equivalence_class(application: Dict[str, Any]) -> Dict[str, Any]:
    top_rows = application.get("top_rows_after_application", [])
    if not isinstance(top_rows, list):
        top_rows = []

    shared_keys = {}
    if top_rows:
        candidate_keys = [
            "base_dominance_score",
            "provenance_rank",
            "field_exactness_rank",
            "container_role_rank",
            "explicit_rule_composite_rank",
            "eligible_selected_target_ref",
            "role",
        ]
        for key in candidate_keys:
            vals = {json.dumps(row.get(key), sort_keys=True) for row in top_rows if isinstance(row, dict)}
            if len(vals) == 1:
                shared_keys[key] = top_rows[0].get(key)

    distinguishing_fields = []
    if top_rows:
        keys = sorted({k for row in top_rows if isinstance(row, dict) for k in row.keys()})
        for key in keys:
            vals = []
            for row in top_rows:
                if isinstance(row, dict):
                    vals.append(row.get(key))
            rendered = {json.dumps(v, sort_keys=True) for v in vals}
            if len(rendered) > 1:
                distinguishing_fields.append(key)

    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_equivalence_class_v0",
        "equivalence_class_id": "dominance_equivalence_" + sha8(top_rows),
        "equivalence_status": "TOP_ROW_EQUIVALENCE_CLASS_REMAINS" if len(top_rows) > 1 else "NO_EQUIVALENCE_CLASS_REMAINS",
        "source_application_table_ref": rel(APPLICATION_TABLE_PATH),
        "top_row_count": len(top_rows),
        "top_rows": top_rows,
        "shared_rank_features": shared_keys,
        "distinguishing_fields": distinguishing_fields,
        "required_refinement": "ADD_VALUE_SOURCE_EQUIVALENCE_CLASS_REFINEMENT_RULE_V0" if len(top_rows) > 1 else None,
        "forbidden_resolution_methods": [
            "latest-file guessing",
            "mtime selection",
            "first-seen order",
            "alphabetical preference without schema reason",
            "manual preference hidden in code",
            "declaring review candidate without explicit rule"
        ],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def values_from_single_top(application: Dict[str, Any]) -> Dict[str, Any]:
    top_rows = application.get("top_rows_after_application", [])
    if not isinstance(top_rows, list) or len(top_rows) != 1:
        return {}

    row = top_rows[0]
    value = row.get("value")
    if not isinstance(value, str) or not value:
        return {}

    values = {
        "SELECTED_TARGET_REF": value,
        "SELECTED_TARGET_KIND": "runtime_patch_target",
        "WHY_THIS_TARGET_IS_LOAD_BEARING": (
            "Proposed after applying the explicit value-source dominance rule. Exactly one top row survived rule application. "
            "This remains a proposal only; human or prevalidated-schema acceptance is required."
        ),
        "WHY_OTHER_HINTS_ARE_NOT_TARGETS_JSON": json.dumps({
            "rejection_basis": "all non-top rows are lower-ranked under explicit dominance rule",
            "source_application_table_ref": rel(APPLICATION_TABLE_PATH),
        }),
        "SOURCE_EVIDENCE_REFS_JSON": json.dumps([
            rel(SOURCE_DOMINANCE_RULE_PATH),
            rel(SOURCE_DOMINANCE_RULE_IMPACT_PREVIEW_PATH),
            rel(SOURCE_VALUE_SOURCE_NARROWING_TABLE_PATH),
        ]),
        "VERIFICATION_GATE_REF": "",
        "ROLLBACK_OR_STOP_BOUNDARY_REF": "",
    }
    return values

def write_env_exports(values: Dict[str, Any]) -> None:
    lines = [
        "# Dominance-rule application values proposal only.",
        "# Human or prevalidated-schema acceptance boundary still applies.",
        "# Do not treat this as selected-for-build or patch authorization.",
    ]
    for field in REQUIRED_ENV_FIELDS:
        lines.append(f"export {field}={shlex.quote(str(values[field]))}")
    lines.append("")
    APPLICATION_ENV_EXPORTS_PATH.write_text("\n".join(lines))

def status_to_next(status: str) -> str:
    if status == "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_ONE_TOP_ROW":
        return "REVIEW_DOMINANCE_RULE_APPLICATION_VALUES_PROPOSAL_V0"
    if status == "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_STILL_MULTIPLE_TOP_ROWS":
        return "ADD_VALUE_SOURCE_EQUIVALENCE_CLASS_REFINEMENT_RULE_V0"
    if status == "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_NO_ELIGIBLE_ROWS":
        return "REPAIR_VALUE_SOURCE_SURFACE_NARROWING_RULE_INPUTS_V0"
    return "REPAIR_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLICATION_V0"

def status_to_stop(status: str) -> str:
    return "STOP_" + status

def classification_obj(application: Dict[str, Any], values: Dict[str, Any]) -> Dict[str, Any]:
    status = application["application_status"]
    ready = status == "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_ONE_TOP_ROW" and bool(values)
    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_application_classification_v0",
        "classification_status": status,
        "reason_codes": application["reason_codes"],
        "rule_applied": True,
        "proposal_ready": ready,
        "candidate_values_filled_count": len(values) if ready else 0,
        "top_row_count_after_application": application["top_row_count_after_application"],
        "target_candidate_proposed_count": 1 if ready else 0,
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
        "recommended_next": status_to_next(status),
        "next_command_goal": None,
    }

def values_proposal_obj(application: Dict[str, Any], values: Dict[str, Any]) -> Dict[str, Any]:
    status = application["application_status"]
    ready = status == "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_ONE_TOP_ROW" and bool(values)
    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_application_values_proposal_v0",
        "proposal_type": "DOMINANCE_RULE_APPLICATION_VALUES_PROPOSAL",
        "proposal_id": "dominance_rule_application_values_" + sha8({
            "status": status,
            "values": values,
        }),
        "proposal_status": status,
        "reason_codes": application["reason_codes"],
        "candidate_values": values if ready else {},
        "application_table_ref": rel(APPLICATION_TABLE_PATH),
        "equivalence_class_ref": rel(APPLICATION_EQUIVALENCE_CLASS_PATH),
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
        "recommended_next": status_to_next(status),
    }

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_application_authority_boundary_v0",
        "status": status,
        "may_apply_rule": True,
        "may_emit_equivalence_class": True,
        "may_emit_values_proposal_if_single_top_row": status == "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_ONE_TOP_ROW",
        "may_emit_env_exports_if_single_top_row": status == "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_ONE_TOP_ROW",
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
        "must_not_infer": [
            "rule application equals acceptance",
            "top row equals selected-for-build",
            "equivalence class may be broken by hidden preference",
            "values proposal authorizes patching"
        ],
    }

def rollup_obj(application: Dict[str, Any], values: Dict[str, Any]) -> Dict[str, Any]:
    status = application["application_status"]
    ready = status == "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLIED_ONE_TOP_ROW" and bool(values)
    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_application_rollup_v0",
        "build_mode": BUILD_MODE,
        "application_status": status,
        "rule_applied_count": 1,
        "equivalence_class_emitted_count": 1,
        "top_row_count_after_application": application["top_row_count_after_application"],
        "values_proposal_ready_count": 1 if ready else 0,
        "values_proposal_not_ready_count": 0 if ready else 1,
        "target_candidate_proposed_count": 1 if ready else 0,
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
        "recommended_next": status_to_next(status),
    }

def profile_obj(roll: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_application_profile_v0",
        "profile_id": "dominance_rule_application_" + sha8(roll),
        "status": roll["application_status"],
        "rule_applied": True,
        "proposal_ready": roll["values_proposal_ready_count"] == 1,
        "target_candidate_proposed": roll["target_candidate_proposed_count"] == 1,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(roll.get(k) == 0 for k in [
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
        ]),
        "recommended_next": roll["recommended_next"],
        "next_command_goal": None,
    }

def report_obj(application: Dict[str, Any], values: Dict[str, Any], roll: Dict[str, Any]) -> Dict[str, Any]:
    status = application["application_status"]
    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_application_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": application["reason_codes"],
        "rule_applied_count": 1,
        "top_row_count_after_application": application["top_row_count_after_application"],
        "candidate_values_filled_count": len(values) if roll["values_proposal_ready_count"] == 1 else 0,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "recommended_next_handling": roll["recommended_next"],
        "target_candidate_proposed_count": roll["target_candidate_proposed_count"],
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

def transition_trace_obj(application: Dict[str, Any]) -> Dict[str, Any]:
    status = application["application_status"]
    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_application_transition_trace_v0",
        "trace": [
            {
                "step": "consume_added_dominance_rule",
                "question": "was the rule previously only added/previewed",
                "answer": "yes",
                "taken": "apply_rule_as_bounded_test",
            },
            {
                "step": "apply_rule_to_ranked_eligible_rows",
                "question": "does rule application produce exactly one top value-source row",
                "answer": status,
                "top_row_count_after_application": application["top_row_count_after_application"],
                "taken": status_to_next(status),
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": status_to_stop(status),
            "next_command_goal": None,
        },
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        application = {
            "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_application_table_v0",
            "application_table_id": "dominance_rule_application_source_fail_" + sha8(failures),
            "source_rule_ref": rel(SOURCE_DOMINANCE_RULE_PATH),
            "source_rule_receipt_id": SOURCE_DOMINANCE_RULE_RECEIPT_ID,
            "source_impact_preview_ref": rel(SOURCE_DOMINANCE_RULE_IMPACT_PREVIEW_PATH),
            "source_narrowing_table_ref": rel(SOURCE_VALUE_SOURCE_NARROWING_TABLE_PATH),
            "application_status": "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLICATION_SOURCE_BASIS_FAIL",
            "reason_codes": failures,
            "rule_applied": False,
            "prior_preview_status": None,
            "ranked_eligible_row_count": 0,
            "top_row_count_after_application": 0,
            "top_rows_after_application": [],
            "ranked_rows_after_application": [],
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
    else:
        application = build_application()

    equivalence = build_equivalence_class(application)
    values = values_from_single_top(application)

    write_json(APPLICATION_TABLE_PATH, application)
    write_json(APPLICATION_EQUIVALENCE_CLASS_PATH, equivalence)

    classif = classification_obj(application, values)
    proposal = values_proposal_obj(application, values)
    boundary = authority_boundary_obj(application["application_status"])
    roll = rollup_obj(application, values)
    prof = profile_obj(roll)
    rep = report_obj(application, values, roll)
    trace = transition_trace_obj(application)

    write_json(APPLICATION_CLASSIFICATION_PATH, classif)
    write_json(APPLICATION_VALUES_PROPOSAL_PATH, proposal)

    if classif["proposal_ready"]:
        write_env_exports(values)
    elif APPLICATION_ENV_EXPORTS_PATH.exists():
        APPLICATION_ENV_EXPORTS_PATH.unlink()

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
        "DOMINANCE_RULE_APPLICATION_0_RULE_RECEIPT_CONSUMED": SOURCE_DOMINANCE_RULE_RECEIPT_PATH.exists(),
        "DOMINANCE_RULE_APPLICATION_1_RULE_ARTIFACT_CONSUMED": SOURCE_DOMINANCE_RULE_PATH.exists(),
        "DOMINANCE_RULE_APPLICATION_2_IMPACT_PREVIEW_CONSUMED": SOURCE_DOMINANCE_RULE_IMPACT_PREVIEW_PATH.exists(),
        "DOMINANCE_RULE_APPLICATION_3_RULE_APPLIED": roll["rule_applied_count"] == 1,
        "DOMINANCE_RULE_APPLICATION_4_APPLICATION_TABLE_EMITTED": APPLICATION_TABLE_PATH.exists(),
        "DOMINANCE_RULE_APPLICATION_5_EQUIVALENCE_CLASS_EMITTED": APPLICATION_EQUIVALENCE_CLASS_PATH.exists(),
        "DOMINANCE_RULE_APPLICATION_6_CLASSIFICATION_EMITTED": APPLICATION_CLASSIFICATION_PATH.exists(),
        "DOMINANCE_RULE_APPLICATION_7_VALUES_PROPOSAL_EMITTED": APPLICATION_VALUES_PROPOSAL_PATH.exists(),
        "DOMINANCE_RULE_APPLICATION_8_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classif["target_candidate_declared_for_review"] is False,
        "DOMINANCE_RULE_APPLICATION_9_NO_TARGET_SELECTED_FOR_BUILD": classif["target_selected_for_build"] is False,
        "DOMINANCE_RULE_APPLICATION_10_NO_ACCEPTED_FOR_BUILD": classif["accepted_for_build"] is False,
        "DOMINANCE_RULE_APPLICATION_11_NO_RUNTIME_PATCH": classif["runtime_patch_authorized"] is False,
        "DOMINANCE_RULE_APPLICATION_12_NO_TARGET_FILE_MODIFICATION": classif["target_file_modification_authorized"] is False,
        "DOMINANCE_RULE_APPLICATION_13_NO_C5_OPENED": classif["c5_authorized"] is False,
        "DOMINANCE_RULE_APPLICATION_14_NO_GENERAL_CELL1_AUTHORITY": classif["general_cell1_authority_granted"] is False,
        "DOMINANCE_RULE_APPLICATION_15_NO_LATEST_FILE_GUESSING": classif["latest_file_guessing"] is False,
        "DOMINANCE_RULE_APPLICATION_16_NO_MTIME_SELECTION": classif["mtime_selection"] is False,
        "DOMINANCE_RULE_APPLICATION_17_NO_HIDDEN_NEXT_COMMAND": classif["next_command_goal"] is None,
        "DOMINANCE_RULE_APPLICATION_18_ACCEPTANCE_BOUNDARY_RETAINED": classif["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "DOMINANCE_RULE_APPLICATION_19_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_APPLICATION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": application["application_status"],
        "top_count": application["top_row_count_after_application"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_application_receipt_v0",
        "receipt_type": "EXPLICIT_RUNTIME_PATCH_TARGET_VALUE_SOURCE_DOMINANCE_RULE_APPLICATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_dominance_rule_receipt_id": SOURCE_DOMINANCE_RULE_RECEIPT_ID,
        "source_value_source_narrowing_receipt_id": SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_ID,
        "dominance_rule_application_summary": {
            "status": application["application_status"],
            "reason_codes": application["reason_codes"],
            "rule_applied": True,
            "top_row_count_after_application": application["top_row_count_after_application"],
            "equivalence_class_status": equivalence["equivalence_status"],
            "proposal_ready": classif["proposal_ready"],
            "candidate_values_filled_count": classif["candidate_values_filled_count"],
            "target_candidate_proposed": roll["target_candidate_proposed_count"] == 1,
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
            "recommended_next": roll["recommended_next"],
        },
        "aggregate_metrics": rep,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "application_table": rel(APPLICATION_TABLE_PATH),
            "equivalence_class": rel(APPLICATION_EQUIVALENCE_CLASS_PATH),
            "classification": rel(APPLICATION_CLASSIFICATION_PATH),
            "values_proposal": rel(APPLICATION_VALUES_PROPOSAL_PATH),
            "env_exports": rel(APPLICATION_ENV_EXPORTS_PATH) if APPLICATION_ENV_EXPORTS_PATH.exists() else None,
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
    print(f"dominance_rule_application_receipt_id={receipt_id}")
    print(f"dominance_rule_application_receipt_path={rel(receipt_path)}")
    print(f"dominance_rule_application_table_path={rel(APPLICATION_TABLE_PATH)}")
    print(f"dominance_rule_equivalence_class_path={rel(APPLICATION_EQUIVALENCE_CLASS_PATH)}")
    print(f"dominance_rule_application_classification_path={rel(APPLICATION_CLASSIFICATION_PATH)}")
    print(f"dominance_rule_application_values_proposal_path={rel(APPLICATION_VALUES_PROPOSAL_PATH)}")
    print(f"dominance_rule_application_env_exports_path={rel(APPLICATION_ENV_EXPORTS_PATH) if APPLICATION_ENV_EXPORTS_PATH.exists() else ''}")
    print(f"dominance_rule_application_rollup_path={rel(ROLLUP_PATH)}")
    print(f"dominance_rule_application_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
