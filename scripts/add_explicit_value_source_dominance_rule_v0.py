#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ADD_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_dominance_rule.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_DOMINANCE_RULE"
MODE = "ADD_RULE / NO_RULE_APPLICATION / NO_ACCEPTANCE"
BUILD_MODE = "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_ONLY"

SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_ID = "e89512e0"
SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0_receipts/e89512e0.json"
SOURCE_VALUE_SOURCE_NARROWING_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0/runtime_patch_target_value_source_narrowing_table_v0.json"
SOURCE_VALUE_SOURCE_DOMINANCE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0/runtime_patch_target_value_source_dominance_classification_v0.json"
SOURCE_VALUE_SOURCE_NARROWED_VALUES_PROPOSAL_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0/runtime_patch_target_value_source_narrowed_values_proposal_v0.json"
SOURCE_VALUE_SOURCE_NARROWING_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0/runtime_patch_target_value_source_narrowing_rollup_v0.json"
SOURCE_VALUE_SOURCE_NARROWING_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_surface_narrowing_v0/runtime_patch_target_value_source_narrowing_profile_v0.json"

SOURCE_SURFACE_REPAIR_RECEIPT_ID = "6ca7147e"
SOURCE_SURFACE_REPAIR_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_input_repair_v0_receipts/6ca7147e.json"
SOURCE_SURFACE_MAP_PATH = ROOT / "data/cell1_runtime_patch_target_evidence_values_proposer_input_repair_v0/runtime_patch_target_value_source_surface_map_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_dominance_rule_v0_receipts"

RULE_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_v0.json"
RULE_IMPACT_PREVIEW_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_impact_preview_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_profile_v0.json"
REPORT_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "explicit_runtime_patch_target_value_source_dominance_rule_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_PATH,
    SOURCE_VALUE_SOURCE_NARROWING_TABLE_PATH,
    SOURCE_VALUE_SOURCE_DOMINANCE_CLASSIFICATION_PATH,
    SOURCE_VALUE_SOURCE_NARROWED_VALUES_PROPOSAL_PATH,
    SOURCE_VALUE_SOURCE_NARROWING_ROLLUP_PATH,
    SOURCE_VALUE_SOURCE_NARROWING_PROFILE_PATH,
    SOURCE_SURFACE_REPAIR_RECEIPT_PATH,
    SOURCE_SURFACE_MAP_PATH,
]

RULE_NAME = "explicit_runtime_patch_target_value_source_dominance_rule_v0"

REQUIRED_PRIOR_STATUS = "VALUE_SOURCE_SURFACE_STILL_MULTIPLE_AMBIGUOUS"
REQUIRED_PRIOR_STOP = "STOP_VALUE_SOURCE_SURFACE_STILL_MULTIPLE_AMBIGUOUS"

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

    narrowing_receipt = read_json(SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_PATH)
    narrowing_table = read_json(SOURCE_VALUE_SOURCE_NARROWING_TABLE_PATH)
    dominance_classification = read_json(SOURCE_VALUE_SOURCE_DOMINANCE_CLASSIFICATION_PATH)
    narrowed_values = read_json(SOURCE_VALUE_SOURCE_NARROWED_VALUES_PROPOSAL_PATH)
    rollup = read_json(SOURCE_VALUE_SOURCE_NARROWING_ROLLUP_PATH)
    profile = read_json(SOURCE_VALUE_SOURCE_NARROWING_PROFILE_PATH)
    surface_repair = read_json(SOURCE_SURFACE_REPAIR_RECEIPT_PATH)
    surface_map = read_json(SOURCE_SURFACE_MAP_PATH)

    summary = narrowing_receipt.get("value_source_narrowing_summary", {})

    if narrowing_receipt.get("receipt_id") != SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_ID or narrowing_receipt.get("gate") != "PASS":
        failures.append("value_source_narrowing_receipt_not_pass")
    if summary.get("status") != REQUIRED_PRIOR_STATUS:
        failures.append(f"narrowing_status_not_required:{summary.get('status')}")
    if narrowing_receipt.get("terminal", {}).get("stop_code") != REQUIRED_PRIOR_STOP:
        failures.append("narrowing_terminal_not_required")
    if summary.get("eligible_selected_target_ref_row_count") != 4:
        failures.append(f"eligible_count_not_4:{summary.get('eligible_selected_target_ref_row_count')}")
    if summary.get("top_dominant_row_count") != 3:
        failures.append(f"top_dominant_count_not_3:{summary.get('top_dominant_row_count')}")
    if summary.get("proposal_ready") is not False:
        failures.append("prior_narrowing_proposal_ready_unexpectedly")
    if summary.get("accepted_for_build") is not False:
        failures.append("prior_narrowing_accepted_for_build")
    if summary.get("runtime_patch_applied") is not False:
        failures.append("prior_narrowing_applied_runtime_patch")

    if dominance_classification.get("classification_status") != REQUIRED_PRIOR_STATUS:
        failures.append("dominance_classification_not_required_status")
    if dominance_classification.get("target_selected_for_build") is not False:
        failures.append("dominance_classification_selects_target_for_build")
    if dominance_classification.get("accepted_for_build") is not False:
        failures.append("dominance_classification_accepts_for_build")
    if dominance_classification.get("runtime_patch_authorized") is not False:
        failures.append("dominance_classification_authorizes_runtime_patch")

    if narrowed_values.get("proposal_status") != REQUIRED_PRIOR_STATUS:
        failures.append("narrowed_values_proposal_not_required_status")
    if narrowed_values.get("candidate_values") not in ({}, None):
        failures.append("narrowed_values_has_candidate_values_unexpectedly")
    if narrowed_values.get("accepted_for_build") is not False:
        failures.append("narrowed_values_accepts_for_build")
    if narrowed_values.get("runtime_patch_authorized") is not False:
        failures.append("narrowed_values_authorizes_runtime_patch")

    if rollup.get("surface_narrowing_status") != REQUIRED_PRIOR_STATUS:
        failures.append("rollup_status_not_required")
    if profile.get("status") != REQUIRED_PRIOR_STATUS:
        failures.append("profile_status_not_required")

    if surface_repair.get("receipt_id") != SOURCE_SURFACE_REPAIR_RECEIPT_ID or surface_repair.get("gate") != "PASS":
        failures.append("surface_repair_receipt_not_pass")
    if surface_repair.get("value_source_surface_summary", {}).get("status") != "VALUE_SOURCE_SURFACE_MULTIPLE_AMBIGUOUS":
        failures.append("surface_repair_status_not_multiple_ambiguous")
    if surface_map.get("typed_value_source_row_count") != 67:
        failures.append(f"surface_map_typed_count_not_67:{surface_map.get('typed_value_source_row_count')}")

    return failures

def rule_obj() -> Dict[str, Any]:
    rule = {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_v0",
        "rule_type": "RUNTIME_PATCH_TARGET_VALUE_SOURCE_DOMINANCE_RULE",
        "rule_name": RULE_NAME,
        "rule_id": "dominance_rule_" + sha8({
            "source": SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_ID,
            "name": RULE_NAME,
        }),
        "source_value_source_narrowing_receipt_id": SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_ID,
        "source_surface_repair_receipt_id": SOURCE_SURFACE_REPAIR_RECEIPT_ID,
        "rule_status": "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_ADDED",
        "problem_being_repaired": {
            "prior_status": REQUIRED_PRIOR_STATUS,
            "prior_reason_codes": [
                "MULTIPLE_ELIGIBLE_SELECTED_TARGET_VALUE_SOURCE_ROWS_WITH_EQUAL_DOMINANCE",
                "NO_SINGLE_DOMINANT_VALUE_SOURCE",
                "SUPPORTING_VERIFICATION_GATE_REF_NOT_UNIQUE",
                "SUPPORTING_ROLLBACK_OR_STOP_BOUNDARY_REF_NOT_UNIQUE"
            ],
            "prior_typed_row_count": 67,
            "prior_eligible_selected_target_ref_row_count": 4,
            "prior_top_dominant_row_count": 3,
        },
        "dominance_rule": {
            "rule_version": "v0",
            "application_mode": "deterministic_filter_then_rank",
            "selected_target_ref_row_filter": [
                {
                    "step": 1,
                    "name": "eligible_selected_target_ref_only",
                    "require": [
                        "row.eligible_selected_target_ref == true",
                        "row.role == selected_target_ref_candidate"
                    ],
                    "reject": [
                        "supporting_field_not_selected_target_ref",
                        "verification_gate_candidate",
                        "rollback_or_stop_boundary_candidate",
                        "metadata_or_receipt_output_path"
                    ]
                },
                {
                    "step": 2,
                    "name": "primary_origin_required",
                    "prefer_or_require": "require",
                    "require": [
                        "row.source_kind == primary_value_surface"
                    ],
                    "allowed_primary_sources": [
                        "data/cell1_runtime_patch_target_evidence_request_v0/target_hint_inventory_v0.json",
                        "data/cell1_runtime_patch_target_evidence_request_v0/narrower_runtime_patch_target_evidence_request_packet_v0.json"
                    ]
                },
                {
                    "step": 3,
                    "name": "field_exactness_priority",
                    "prefer_or_require": "rank",
                    "priority_order": [
                        "json_path_exactly_or_suffixes:selected_target_ref",
                        "json_path_exactly_or_suffixes:runtime_patch_target_ref",
                        "json_path_exactly_or_suffixes:target_ref",
                        "json_path_exactly_or_suffixes:candidate_target_ref",
                        "json_path_exactly_or_suffixes:candidate_ref",
                        "json_path_contains_target_and_ref",
                        "json_path_contains_candidate_and_ref"
                    ]
                },
                {
                    "step": 4,
                    "name": "container_role_priority",
                    "prefer_or_require": "rank",
                    "priority_order": [
                        "parent_or_ancestor_has:explicit_target_candidate",
                        "parent_or_ancestor_has:single_target_candidate",
                        "parent_or_ancestor_has:dominant_target_candidate",
                        "parent_or_ancestor_has:load_bearing_target_candidate",
                        "parent_or_ancestor_has:target_candidate",
                        "parent_or_ancestor_has:hint"
                    ]
                },
                {
                    "step": 5,
                    "name": "provenance_distance_priority",
                    "prefer_or_require": "rank",
                    "priority_order": [
                        "target_hint_inventory_row",
                        "request_packet_direct_field",
                        "derived_surface_map_row"
                    ]
                },
                {
                    "step": 6,
                    "name": "tie_policy",
                    "if_tie_after_all_rank_stages": "STOP_STILL_MULTIPLE_DOMINANT_VALUE_SOURCE_ROWS",
                    "forbidden_tiebreakers": [
                        "latest_file",
                        "mtime",
                        "alphabetical_preference_without_schema_reason",
                        "first_seen_order",
                        "shortest_path_preference_without_schema_reason"
                    ]
                }
            ],
            "supporting_ref_rule": [
                {
                    "field": "VERIFICATION_GATE_REF",
                    "allowed_role": "verification_gate_candidate",
                    "require_unique_after_same_primary_source_or_same_container_filter": True,
                    "if_not_unique": "STOP_SUPPORTING_VERIFICATION_GATE_REF_NOT_UNIQUE"
                },
                {
                    "field": "ROLLBACK_OR_STOP_BOUNDARY_REF",
                    "allowed_role": "rollback_or_stop_boundary_candidate",
                    "require_unique_after_same_primary_source_or_same_container_filter": True,
                    "if_not_unique": "STOP_SUPPORTING_ROLLBACK_OR_STOP_BOUNDARY_REF_NOT_UNIQUE"
                }
            ]
        },
        "application_boundary": {
            "this_rule_does_not_apply_itself": True,
            "next_unit_may_apply_rule": "APPLY_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_V0",
            "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
            "proposal_is_not_acceptance": True,
        },
        "not_authorized": [
            "declare target candidate for review",
            "select target for build",
            "accept for build",
            "apply runtime patch",
            "modify target files",
            "open C5",
            "grant general Cell1 authority",
            "use latest-file guessing",
            "use mtime selection",
            "collapse remaining ambiguity by preference"
        ],
        "recommended_next": "APPLY_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_V0",
    }
    return rule

def suffix_rank(json_path: str) -> int:
    p = json_path.lower().replace("[", ".").replace("]", "")
    segments = [s for s in p.split(".") if s]
    last = segments[-1] if segments else p

    exact_order = [
        "selected_target_ref",
        "runtime_patch_target_ref",
        "target_ref",
        "candidate_target_ref",
        "candidate_ref",
    ]
    for i, key in enumerate(exact_order):
        if last == key or p.endswith("." + key):
            return 100 - (i * 10)

    if "target" in p and "ref" in p:
        return 40
    if "candidate" in p and "ref" in p:
        return 30
    return 0

def container_rank(row: Dict[str, Any]) -> int:
    p = str(row.get("json_path", "")).lower()
    markers = [
        "explicit_target_candidate",
        "single_target_candidate",
        "dominant_target_candidate",
        "load_bearing_target_candidate",
        "target_candidate",
        "hint",
    ]
    for i, marker in enumerate(markers):
        if marker in p:
            return 100 - (i * 10)
    return 0

def provenance_rank(row: Dict[str, Any]) -> int:
    src = str(row.get("source_ref", ""))
    if src.endswith("target_hint_inventory_v0.json"):
        return 100
    if src.endswith("narrower_runtime_patch_target_evidence_request_packet_v0.json"):
        return 80
    return 0

def preview_application(rule: Dict[str, Any]) -> Dict[str, Any]:
    table = read_json(SOURCE_VALUE_SOURCE_NARROWING_TABLE_PATH)
    eligible = table.get("eligible_rows", [])
    classified = table.get("classified_rows", [])

    ranked: List[Dict[str, Any]] = []
    for row in eligible:
        if not isinstance(row, dict):
            continue
        sr = suffix_rank(str(row.get("json_path", "")))
        cr = container_rank(row)
        pr = provenance_rank(row)
        base = int(row.get("dominance_score") or 0)
        composite = (base * 1000000) + (pr * 10000) + (sr * 100) + cr
        ranked.append({
            "source_ref": row.get("source_ref"),
            "json_path": row.get("json_path"),
            "value": row.get("value"),
            "base_dominance_score": base,
            "provenance_rank": pr,
            "field_exactness_rank": sr,
            "container_role_rank": cr,
            "explicit_rule_composite_rank": composite,
            "eligible_selected_target_ref": row.get("eligible_selected_target_ref"),
            "role": row.get("role"),
            "positive_reasons": row.get("positive_reasons"),
            "rejection_reasons": row.get("rejection_reasons"),
        })

    ranked_sorted = sorted(
        ranked,
        key=lambda r: (
            -int(r["explicit_rule_composite_rank"]),
            str(r.get("source_ref")),
            str(r.get("json_path")),
            str(r.get("value")),
        )
    )

    top_rank = ranked_sorted[0]["explicit_rule_composite_rank"] if ranked_sorted else None
    top_rows = [r for r in ranked_sorted if r["explicit_rule_composite_rank"] == top_rank] if top_rank is not None else []

    if not ranked_sorted:
        preview_status = "RULE_PREVIEW_NO_ELIGIBLE_ROWS"
        reason_codes = ["NO_ELIGIBLE_SELECTED_TARGET_REF_ROWS"]
    elif len(top_rows) == 1:
        preview_status = "RULE_PREVIEW_ONE_TOP_VALUE_SOURCE_ROW"
        reason_codes = ["ONE_TOP_ROW_UNDER_RULE_PREVIEW"]
    else:
        preview_status = "RULE_PREVIEW_STILL_MULTIPLE_TOP_ROWS"
        reason_codes = ["MULTIPLE_TOP_ROWS_UNDER_RULE_PREVIEW"]

    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_impact_preview_v0",
        "preview_status": preview_status,
        "reason_codes": reason_codes,
        "source_narrowing_table_ref": rel(SOURCE_VALUE_SOURCE_NARROWING_TABLE_PATH),
        "rule_ref": rel(RULE_PATH),
        "prior_eligible_selected_target_ref_row_count": len(eligible) if isinstance(eligible, list) else None,
        "prior_classified_row_count": len(classified) if isinstance(classified, list) else None,
        "ranked_eligible_row_count": len(ranked_sorted),
        "top_rank": top_rank,
        "top_row_count_under_rule_preview": len(top_rows),
        "top_rows_under_rule_preview": top_rows,
        "ranked_eligible_rows": ranked_sorted,
        "preview_does_not_select_for_build": True,
        "preview_does_not_declare_for_review": True,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "recommended_next": "APPLY_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_V0",
    }

def classification_obj(rule: Dict[str, Any], preview: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_classification_v0",
        "classification_status": "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_ADDED",
        "rule_status": rule["rule_status"],
        "impact_preview_status": preview["preview_status"],
        "impact_preview_top_row_count": preview["top_row_count_under_rule_preview"],
        "prior_status": REQUIRED_PRIOR_STATUS,
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
        "recommended_next": "APPLY_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_V0",
        "next_command_goal": None,
    }

def authority_boundary_obj() -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_authority_boundary_v0",
        "status": "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_ADDED",
        "may_add_rule": True,
        "may_preview_rule_impact_without_selecting": True,
        "may_apply_rule": False,
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
        "must_not_infer": [
            "rule creation applies the rule",
            "rule impact preview selects target for build",
            "single top preview row is accepted for build",
            "rule can break remaining ties by preference"
        ],
    }

def rollup_obj(preview: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_rollup_v0",
        "build_mode": BUILD_MODE,
        "rule_added_count": 1,
        "rule_applied_count": 0,
        "impact_preview_emitted_count": 1,
        "impact_preview_top_row_count": preview["top_row_count_under_rule_preview"],
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
        "recommended_next": "APPLY_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_V0",
    }

def profile_obj(roll: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_profile_v0",
        "profile_id": "dominance_rule_" + sha8(roll),
        "status": "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_ADDED",
        "rule_added": True,
        "rule_applied": False,
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
            "rule_applied_count",
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

def report_obj(preview: Dict[str, Any], roll: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_ADDED",
        "prior_status": REQUIRED_PRIOR_STATUS,
        "impact_preview_status": preview["preview_status"],
        "impact_preview_top_row_count": preview["top_row_count_under_rule_preview"],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "recommended_next_handling": roll["recommended_next"],
        "rule_added_count": 1,
        "rule_applied_count": 0,
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

def transition_trace_obj(preview: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_transition_trace_v0",
        "trace": [
            {
                "step": "consume_still_multiple_ambiguous_narrowing",
                "question": "why did narrowing halt",
                "answer": REQUIRED_PRIOR_STATUS,
                "taken": "add_explicit_value_source_dominance_rule",
            },
            {
                "step": "materialize_rule_not_apply_rule",
                "question": "where is the boundary",
                "answer": "rule is an artifact; application and acceptance remain later boundaries",
                "taken": "emit_rule_and_impact_preview_only",
            },
            {
                "step": "preview_rule_impact",
                "question": "would the rule likely narrow the current eligible rows",
                "answer": preview["preview_status"],
                "top_row_count_under_rule_preview": preview["top_row_count_under_rule_preview"],
                "taken": "recommend_apply_rule_next_without accepting anything",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_ADDED",
            "next_command_goal": None,
        },
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    rule = rule_obj()
    write_json(RULE_PATH, rule)

    preview = preview_application(rule)
    classif = classification_obj(rule, preview)
    boundary = authority_boundary_obj()
    roll = rollup_obj(preview)
    prof = profile_obj(roll)
    rep = report_obj(preview, roll)
    trace = transition_trace_obj(preview)

    write_json(RULE_IMPACT_PREVIEW_PATH, preview)
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
        "DOMINANCE_RULE_0_NARROWING_RECEIPT_CONSUMED": SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_PATH.exists(),
        "DOMINANCE_RULE_1_NARROWING_TABLE_CONSUMED": SOURCE_VALUE_SOURCE_NARROWING_TABLE_PATH.exists(),
        "DOMINANCE_RULE_2_RULE_EMITTED": RULE_PATH.exists(),
        "DOMINANCE_RULE_3_IMPACT_PREVIEW_EMITTED": RULE_IMPACT_PREVIEW_PATH.exists(),
        "DOMINANCE_RULE_4_CLASSIFICATION_EMITTED": CLASSIFICATION_PATH.exists(),
        "DOMINANCE_RULE_5_RULE_NOT_APPLIED": roll["rule_applied_count"] == 0,
        "DOMINANCE_RULE_6_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classif["target_candidate_declared_for_review"] is False,
        "DOMINANCE_RULE_7_NO_TARGET_SELECTED_FOR_BUILD": classif["target_selected_for_build"] is False,
        "DOMINANCE_RULE_8_NO_ACCEPTED_FOR_BUILD": classif["accepted_for_build"] is False,
        "DOMINANCE_RULE_9_NO_RUNTIME_PATCH": classif["runtime_patch_authorized"] is False,
        "DOMINANCE_RULE_10_NO_TARGET_FILE_MODIFICATION": classif["target_file_modification_authorized"] is False,
        "DOMINANCE_RULE_11_NO_C5_OPENED": classif["c5_authorized"] is False,
        "DOMINANCE_RULE_12_NO_GENERAL_CELL1_AUTHORITY": classif["general_cell1_authority_granted"] is False,
        "DOMINANCE_RULE_13_NO_LATEST_FILE_GUESSING": classif["latest_file_guessing"] is False,
        "DOMINANCE_RULE_14_NO_MTIME_SELECTION": classif["mtime_selection"] is False,
        "DOMINANCE_RULE_15_NO_HIDDEN_NEXT_COMMAND": classif["next_command_goal"] is None,
        "DOMINANCE_RULE_16_ACCEPTANCE_BOUNDARY_RETAINED": classif["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "DOMINANCE_RULE_17_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "rule_id": rule["rule_id"],
        "preview_status": preview["preview_status"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "explicit_runtime_patch_target_value_source_dominance_rule_receipt_v0",
        "receipt_type": "EXPLICIT_RUNTIME_PATCH_TARGET_VALUE_SOURCE_DOMINANCE_RULE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_value_source_narrowing_receipt_id": SOURCE_VALUE_SOURCE_NARROWING_RECEIPT_ID,
        "source_surface_repair_receipt_id": SOURCE_SURFACE_REPAIR_RECEIPT_ID,
        "dominance_rule_summary": {
            "status": "EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_ADDED",
            "rule_id": rule["rule_id"],
            "rule_applied": False,
            "impact_preview_status": preview["preview_status"],
            "impact_preview_top_row_count": preview["top_row_count_under_rule_preview"],
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
            "recommended_next": "APPLY_EXPLICIT_VALUE_SOURCE_DOMINANCE_RULE_V0",
        },
        "aggregate_metrics": rep,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "dominance_rule": rel(RULE_PATH),
            "impact_preview": rel(RULE_IMPACT_PREVIEW_PATH),
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
    print(f"dominance_rule_receipt_id={receipt_id}")
    print(f"dominance_rule_receipt_path={rel(receipt_path)}")
    print(f"dominance_rule_path={rel(RULE_PATH)}")
    print(f"dominance_rule_impact_preview_path={rel(RULE_IMPACT_PREVIEW_PATH)}")
    print(f"dominance_rule_classification_path={rel(CLASSIFICATION_PATH)}")
    print(f"dominance_rule_rollup_path={rel(ROLLUP_PATH)}")
    print(f"dominance_rule_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
