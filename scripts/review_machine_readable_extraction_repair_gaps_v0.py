#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_MACHINE_READABLE_EXTRACTION_REPAIR_GAPS_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_MACHINE_READABLE_EXTRACTION_GAP_REVIEW"
MODE = "EXTRACTION_GAP_REVIEW / NO_VALUE_AUTHORIZATION / NO_METADATA_FILL / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "MACHINE_READABLE_EXTRACTION_GAP_REVIEW_ONLY"

SOURCE_EXTRACTION_REPAIR_RECEIPT_ID = "7cb12bcd"
SOURCE_EXTRACTION_REPAIR_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_repair_v0_receipts/7cb12bcd.json"
SOURCE_EXTRACTION_REPAIR_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_repair_v0/typed_machine_readable_value_extraction_repair_surface_v0.json"
SOURCE_MACHINE_SLOT_DIAGNOSTIC_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_repair_v0/typed_machine_readable_slot_extraction_diagnostic_v0.json"
SOURCE_REF_RESOLUTION_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_repair_v0/typed_machine_readable_source_ref_resolution_table_v0.json"
SOURCE_EXACT_KEY_CANDIDATE_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_repair_v0/typed_machine_readable_exact_key_candidate_table_v0.json"
SOURCE_EXTRACTION_RULE_CANDIDATES_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_repair_v0/typed_machine_readable_extraction_rule_candidates_v0.json"
SOURCE_REPROPOSITION_INPUT_SURFACE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_repair_v0/typed_machine_readable_reproposition_input_surface_v0.json"
SOURCE_NONEXTRACTABLE_REASON_TABLE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_repair_v0/typed_machine_readable_nonextractable_reason_table_v0.json"
SOURCE_EXTRACTION_REPAIR_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_repair_v0/typed_machine_readable_extraction_repair_classification_v0.json"
SOURCE_EXTRACTION_REPAIR_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_repair_v0/typed_machine_readable_extraction_repair_rollup_v0.json"
SOURCE_EXTRACTION_REPAIR_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_repair_v0/typed_machine_readable_extraction_repair_profile_v0.json"

SOURCE_MACHINE_SOURCE_SLOTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_machine_source_slots_v0.json"
SOURCE_SLOT_INVENTORY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_packet_values_input_repair_v0/typed_value_source_metadata_source_packet_values_slot_inventory_v0.json"
SOURCE_FIELD_POLICY_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_source_bridge_v0/typed_value_source_metadata_source_field_policy_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_machine_readable_extraction_gap_review_v0_receipts"

GAP_REVIEW_ASSESSMENT_PATH = OUT_DIR / "typed_machine_readable_extraction_gap_review_assessment_v0.json"
ROW_JSON_PATH_GAP_TABLE_PATH = OUT_DIR / "typed_machine_readable_row_json_path_gap_table_v0.json"
SOURCE_REF_LAYER_REVIEW_PATH = OUT_DIR / "typed_machine_readable_source_ref_layer_review_v0.json"
FIELD_TYPING_GAP_TABLE_PATH = OUT_DIR / "typed_machine_readable_field_typing_gap_table_v0.json"
EXTRACTION_UNIT_NARROWNESS_REVIEW_PATH = OUT_DIR / "typed_machine_readable_extraction_unit_narrowness_review_v0.json"
GAP_CAUSE_CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_extraction_gap_cause_classification_v0.json"
REPAIR_PLAN_OPTIONS_PATH = OUT_DIR / "typed_machine_readable_extraction_gap_repair_plan_options_v0.json"
NEXT_SURFACE_CONTRACT_PATH = OUT_DIR / "typed_machine_readable_source_ref_field_typing_refinement_contract_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_machine_readable_extraction_gap_review_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_machine_readable_extraction_gap_review_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_machine_readable_extraction_gap_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_machine_readable_extraction_gap_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_machine_readable_extraction_gap_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_machine_readable_extraction_gap_review_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_EXTRACTION_REPAIR_RECEIPT_PATH,
    SOURCE_EXTRACTION_REPAIR_SURFACE_PATH,
    SOURCE_MACHINE_SLOT_DIAGNOSTIC_PATH,
    SOURCE_REF_RESOLUTION_TABLE_PATH,
    SOURCE_EXACT_KEY_CANDIDATE_TABLE_PATH,
    SOURCE_EXTRACTION_RULE_CANDIDATES_PATH,
    SOURCE_REPROPOSITION_INPUT_SURFACE_PATH,
    SOURCE_NONEXTRACTABLE_REASON_TABLE_PATH,
    SOURCE_EXTRACTION_REPAIR_CLASSIFICATION_PATH,
    SOURCE_EXTRACTION_REPAIR_ROLLUP_PATH,
    SOURCE_EXTRACTION_REPAIR_PROFILE_PATH,
    SOURCE_MACHINE_SOURCE_SLOTS_PATH,
    SOURCE_SLOT_INVENTORY_PATH,
    SOURCE_FIELD_POLICY_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_MACHINE_READABLE_VALUE_EXTRACTION_SURFACE_REPAIRED_NO_RULE_CANDIDATES"
EXPECTED_SOURCE_STOP = "STOP_TYPED_MACHINE_READABLE_VALUE_EXTRACTION_SURFACE_REPAIRED_NO_RULE_CANDIDATES"
EXPECTED_NEXT = "REVIEW_MACHINE_READABLE_EXTRACTION_REPAIR_GAPS_V0"

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

    receipt = read_json(SOURCE_EXTRACTION_REPAIR_RECEIPT_PATH)
    summary = receipt.get("machine_readable_extraction_repair_summary", {})
    surface = read_json(SOURCE_EXTRACTION_REPAIR_SURFACE_PATH)
    diag = read_json(SOURCE_MACHINE_SLOT_DIAGNOSTIC_PATH)
    resolutions = read_json(SOURCE_REF_RESOLUTION_TABLE_PATH)
    exact = read_json(SOURCE_EXACT_KEY_CANDIDATE_TABLE_PATH)
    rules = read_json(SOURCE_EXTRACTION_RULE_CANDIDATES_PATH)
    nonextractable = read_json(SOURCE_NONEXTRACTABLE_REASON_TABLE_PATH)
    classif = read_json(SOURCE_EXTRACTION_REPAIR_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_EXTRACTION_REPAIR_ROLLUP_PATH)
    profile = read_json(SOURCE_EXTRACTION_REPAIR_PROFILE_PATH)
    machine_slots = read_json(SOURCE_MACHINE_SOURCE_SLOTS_PATH)

    if receipt.get("receipt_id") != SOURCE_EXTRACTION_REPAIR_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("extraction_repair_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"extraction_repair_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("extraction_repair_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"extraction_repair_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("machine_readable_slot_count") != 21:
        failures.append(f"machine_readable_slot_count_not_21:{summary.get('machine_readable_slot_count')}")
    if summary.get("extraction_rule_candidate_count") != 0:
        failures.append("extraction_rule_candidate_count_not_zero")
    if summary.get("candidate_rules_available") is not False:
        failures.append("candidate_rules_available_unexpectedly")
    if summary.get("repair_status_counts", {}).get("ROW_JSON_PATH_REPAIR_REQUIRED") != 21:
        failures.append("row_json_path_repair_required_count_not_21")
    if summary.get("extraction_gap_reason_counts", {}).get("SOURCE_FIELD_NOT_TYPED") != 21:
        failures.append("source_field_not_typed_count_not_21")
    if summary.get("values_authorized") is not False:
        failures.append("values_authorized_unexpectedly")
    if summary.get("values_applied") is not False:
        failures.append("values_applied_unexpectedly")
    if summary.get("source_packet_materialized_for_review") is not False:
        failures.append("source_packet_materialized_unexpectedly")
    if summary.get("metadata_populated") is not False:
        failures.append("metadata_populated_unexpectedly")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")

    if surface.get("surface_status") != "MACHINE_READABLE_VALUE_EXTRACTION_SURFACE_REPAIRED_FOR_REPROPOSITION":
        failures.append("extraction_repair_surface_status_wrong")
    if diag.get("slot_count") != 21:
        failures.append("diagnostic_slot_count_not_21")
    if resolutions.get("record_count") != 21:
        failures.append("resolution_record_count_not_21")
    if exact.get("candidate_count") != 0:
        failures.append("exact_candidate_count_not_zero")
    if rules.get("rule_candidate_count") != 0:
        failures.append("rule_candidate_count_not_zero")
    if nonextractable.get("record_count") != 21:
        failures.append("nonextractable_count_not_21")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("extraction_repair_classification_status_wrong")
    if roll.get("metadata_populated_count") != 0:
        failures.append("extraction_repair_rollup_metadata_populated_nonzero")
    if profile.get("metadata_populated") is not False:
        failures.append("extraction_repair_profile_metadata_populated_true")
    if machine_slots.get("slot_count") != 21:
        failures.append("source_machine_slots_count_not_21")

    return failures

def records() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    diag = read_json(SOURCE_MACHINE_SLOT_DIAGNOSTIC_PATH).get("records", [])
    res = read_json(SOURCE_REF_RESOLUTION_TABLE_PATH).get("records", [])
    candidates = read_json(SOURCE_EXACT_KEY_CANDIDATE_TABLE_PATH).get("records", [])
    nonext = read_json(SOURCE_NONEXTRACTABLE_REASON_TABLE_PATH).get("records", [])
    return (
        [x for x in diag if isinstance(x, dict)],
        [x for x in res if isinstance(x, dict)],
        [x for x in candidates if isinstance(x, dict)],
        [x for x in nonext if isinstance(x, dict)],
    )

def infer_source_layer(ref: Any) -> str:
    if not isinstance(ref, str) or not ref:
        return "SOURCE_REF_MISSING"
    if "source_packet" in ref or "metadata_source" in ref:
        return "SOURCE_PACKET_OR_METADATA_SOURCE_LAYER"
    if "input_repair" in ref or "value_proposition" in ref or "extraction_repair" in ref:
        return "DERIVED_DIAGNOSTIC_LAYER"
    if "receipt" in ref or "_receipts" in ref:
        return "RECEIPT_LAYER"
    if "rollup" in ref or "profile" in ref or "report" in ref:
        return "SUMMARY_LAYER"
    if ref.endswith(".json"):
        return "JSON_ARTIFACT_LAYER"
    return "UNKNOWN_LAYER"

def classify_gap(d: Dict[str, Any]) -> Dict[str, Any]:
    r = d.get("resolution", {})
    row_source_ref = d.get("row_source_ref")
    row_json_path = d.get("row_json_path")
    source_layer = infer_source_layer(row_source_ref)
    source_path_resolved = bool(r.get("source_path_resolved"))
    source_json = bool(r.get("source_file_readable_as_json"))
    row_path_resolves = bool(r.get("row_json_path_resolves"))
    exact_count = int(d.get("exact_key_candidate_count") or 0)
    suffix_count = int(d.get("suffix_key_candidate_count") or 0)
    rule_count = int(d.get("extraction_rule_candidate_count") or 0)

    if not source_path_resolved:
        primary = "SOURCE_REF_UNRESOLVED"
        repair = "REPAIR_SOURCE_REF_TO_LOCAL_TYPED_ARTIFACT"
    elif not source_json:
        primary = "SOURCE_CONTENT_UNREADABLE"
        repair = "REPAIR_SOURCE_CONTENT_OR_FILE_FORMAT"
    elif not row_path_resolves:
        primary = "ROW_JSON_PATH_DOES_NOT_RESOLVE"
        repair = "REPAIR_ROW_JSON_PATH_OR_ROW_SOURCE_REF"
    elif exact_count == 0 and suffix_count == 0:
        primary = "SOURCE_RESOLVES_BUT_FIELD_KEY_NOT_TYPED"
        repair = "ADD_OR_BRIDGE_TYPED_FIELD_KEYS_IN_SOURCE_ARTIFACT"
    elif exact_count == 0 and suffix_count > 0:
        primary = "EXTRACTOR_TOO_STRICT_OR_FIELD_ALIAS_UNTYPED"
        repair = "ADD_TYPED_FIELD_ALIAS_OR_EXTRACTOR_RULE_CANDIDATE"
    elif rule_count == 0:
        primary = "CANDIDATE_FOUND_BUT_RULE_NOT_EMITTED"
        repair = "REPAIR_EXTRACTION_RULE_CANDIDATE_EMISSION"
    else:
        primary = "UNKNOWN_REVIEW_STATE"
        repair = "REVIEW_EXTRACTION_DIAGNOSTIC_MANUALLY"

    return {
        "slot_id": d.get("slot_id"),
        "row_uid": d.get("row_uid"),
        "field": d.get("field"),
        "slot_category": d.get("slot_category"),
        "row_source_ref": row_source_ref,
        "source_layer_class": source_layer,
        "row_json_path": row_json_path,
        "source_path_resolved": source_path_resolved,
        "source_file_readable_as_json": source_json,
        "row_json_path_resolves": row_path_resolves,
        "exact_key_candidate_count": exact_count,
        "suffix_key_candidate_count": suffix_count,
        "extraction_rule_candidate_count": rule_count,
        "previous_repair_status": d.get("repair_status"),
        "previous_extraction_gap_reason": d.get("extraction_gap_reason"),
        "primary_gap_cause": primary,
        "recommended_repair_action": repair,
        "safe_null_behavior": "keep null; do not mark discriminator ready",
    }

def build_tables(gap_records: List[Dict[str, Any]], resolutions: List[Dict[str, Any]], candidates: List[Dict[str, Any]]) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    row_path_records = []
    field_typing_records = []
    source_layer_records = []
    narrowness_records = []

    for g in gap_records:
        if g["primary_gap_cause"] == "ROW_JSON_PATH_DOES_NOT_RESOLVE":
            row_path_records.append({
                "slot_id": g["slot_id"],
                "row_uid": g["row_uid"],
                "field": g["field"],
                "row_source_ref": g["row_source_ref"],
                "row_json_path": g["row_json_path"],
                "source_layer_class": g["source_layer_class"],
                "review": "row_json_path did not resolve inside resolved JSON source",
                "recommended_repair_action": g["recommended_repair_action"],
            })
        if g["primary_gap_cause"] in {
            "SOURCE_RESOLVES_BUT_FIELD_KEY_NOT_TYPED",
            "EXTRACTOR_TOO_STRICT_OR_FIELD_ALIAS_UNTYPED",
            "CANDIDATE_FOUND_BUT_RULE_NOT_EMITTED",
        }:
            field_typing_records.append({
                "slot_id": g["slot_id"],
                "row_uid": g["row_uid"],
                "field": g["field"],
                "source_layer_class": g["source_layer_class"],
                "exact_key_candidate_count": g["exact_key_candidate_count"],
                "suffix_key_candidate_count": g["suffix_key_candidate_count"],
                "review": "source resolved but typed field key/rule candidate is not available",
                "recommended_repair_action": g["recommended_repair_action"],
            })
        source_layer_records.append({
            "slot_id": g["slot_id"],
            "field": g["field"],
            "row_source_ref": g["row_source_ref"],
            "source_layer_class": g["source_layer_class"],
            "source_path_resolved": g["source_path_resolved"],
            "source_file_readable_as_json": g["source_file_readable_as_json"],
            "row_json_path_resolves": g["row_json_path_resolves"],
        })
        narrowness_records.append({
            "slot_id": g["slot_id"],
            "field": g["field"],
            "exact_key_candidate_count": g["exact_key_candidate_count"],
            "suffix_key_candidate_count": g["suffix_key_candidate_count"],
            "extraction_rule_candidate_count": g["extraction_rule_candidate_count"],
            "extractor_too_narrow": g["primary_gap_cause"] in {
                "EXTRACTOR_TOO_STRICT_OR_FIELD_ALIAS_UNTYPED",
                "CANDIDATE_FOUND_BUT_RULE_NOT_EMITTED",
            },
            "review_note": "No exact or bounded suffix candidates existed; extractor narrowness is not primary." if g["exact_key_candidate_count"] == 0 and g["suffix_key_candidate_count"] == 0 else "Candidate existed; extractor/rule emission may be too narrow.",
        })

    return (
        {
            "schema_version": "typed_machine_readable_row_json_path_gap_table_v0",
            "table_status": "ROW_JSON_PATH_GAPS_REVIEWED",
            "record_count": len(row_path_records),
            "records": row_path_records,
        },
        {
            "schema_version": "typed_machine_readable_source_ref_layer_review_v0",
            "review_status": "SOURCE_REF_LAYERS_REVIEWED",
            "source_layer_counts": dict(Counter(r["source_layer_class"] for r in source_layer_records)),
            "record_count": len(source_layer_records),
            "records": source_layer_records,
        },
        {
            "schema_version": "typed_machine_readable_field_typing_gap_table_v0",
            "table_status": "FIELD_TYPING_GAPS_REVIEWED",
            "record_count": len(field_typing_records),
            "records": field_typing_records,
        },
        {
            "schema_version": "typed_machine_readable_extraction_unit_narrowness_review_v0",
            "review_status": "EXTRACTION_UNIT_NARROWNESS_REVIEWED",
            "extractor_too_narrow_count": sum(1 for r in narrowness_records if r["extractor_too_narrow"]),
            "record_count": len(narrowness_records),
            "records": narrowness_records,
        },
    )

def decide(gap_records: List[Dict[str, Any]], row_table: Dict[str, Any], field_table: Dict[str, Any], narrowness: Dict[str, Any]) -> Tuple[str, List[str], str]:
    cause_counts = Counter(g["primary_gap_cause"] for g in gap_records)
    reason_codes = [
        "MACHINE_READABLE_EXTRACTION_GAPS_REVIEWED",
        "ROW_JSON_PATH_GAP_TABLE_EMITTED",
        "SOURCE_REF_LAYER_REVIEW_EMITTED",
        "FIELD_TYPING_GAP_TABLE_EMITTED",
        "NO_VALUES_AUTHORIZED_OR_APPLIED",
        "NO_METADATA_POPULATION",
    ]

    if cause_counts.get("ROW_JSON_PATH_DOES_NOT_RESOLVE", 0) == len(gap_records):
        reason_codes.append("ALL_MACHINE_READABLE_GAPS_ARE_ROW_JSON_PATH_GAPS")
        reason_codes.append("REFINE_SOURCE_REF_OR_ROW_PATH_TYPING_SURFACE_REQUIRED")
        status = "TYPED_MACHINE_READABLE_EXTRACTION_GAPS_REVIEWED_ROW_PATH_REPAIR_REQUIRED"
        next_edge = "REFINE_MACHINE_READABLE_SOURCE_REF_OR_ROW_PATH_TYPING_SURFACE_V0"
    elif field_table["record_count"] > 0:
        reason_codes.append("FIELD_TYPING_GAPS_PRESENT")
        status = "TYPED_MACHINE_READABLE_EXTRACTION_GAPS_REVIEWED_FIELD_TYPING_REPAIR_REQUIRED"
        next_edge = "REFINE_MACHINE_READABLE_FIELD_TYPING_SURFACE_V0"
    elif narrowness["extractor_too_narrow_count"] > 0:
        reason_codes.append("EXTRACTION_UNIT_TOO_NARROW")
        status = "TYPED_MACHINE_READABLE_EXTRACTION_GAPS_REVIEWED_EXTRACTOR_NARROWNESS_REPAIR_REQUIRED"
        next_edge = "REPAIR_MACHINE_READABLE_EXTRACTION_RULE_CANDIDATE_EMISSION_V0"
    else:
        reason_codes.append("MIXED_EXTRACTION_GAPS_REQUIRE_SOURCE_SURFACE_REVIEW")
        status = "TYPED_MACHINE_READABLE_EXTRACTION_GAPS_REVIEWED_MIXED_REPAIR_REQUIRED"
        next_edge = "REFINE_MACHINE_READABLE_SOURCE_REF_OR_FIELD_TYPING_SURFACE_V0"

    return status, reason_codes, next_edge

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_machine_readable_extraction_gap_review_authority_boundary_v0",
        "status": status,
        "may_review_gap_causes": True,
        "may_emit_repair_plan_options": True,
        "may_refine_next_surface_contract": True,
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

def rollup_obj(status: str, gap_records: List[Dict[str, Any]], row_table: Dict[str, Any], source_layer: Dict[str, Any], field_table: Dict[str, Any], narrowness: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    cause_counts = Counter(g["primary_gap_cause"] for g in gap_records)
    repair_counts = Counter(g["recommended_repair_action"] for g in gap_records)
    return {
        "schema_version": "typed_machine_readable_extraction_gap_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "machine_readable_slot_count": len(gap_records),
        "primary_gap_cause_counts": dict(cause_counts),
        "recommended_repair_action_counts": dict(repair_counts),
        "row_json_path_gap_count": row_table["record_count"],
        "field_typing_gap_count": field_table["record_count"],
        "extractor_too_narrow_count": narrowness["extractor_too_narrow_count"],
        "source_layer_counts": source_layer["source_layer_counts"],
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
        "schema_version": "typed_machine_readable_extraction_gap_review_profile_v0",
        "profile_id": "machine_readable_extraction_gap_review_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "gap_review_completed": True,
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
        "schema_version": "typed_machine_readable_extraction_gap_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The extraction repair found no rule candidates; this review classifies whether the blocker is source refs, row JSON paths, field typing, or extractor narrowness.",
        "machine_readable_slot_count": roll["machine_readable_slot_count"],
        "primary_gap_cause_counts": roll["primary_gap_cause_counts"],
        "recommended_repair_action_counts": roll["recommended_repair_action_counts"],
        "row_json_path_gap_count": roll["row_json_path_gap_count"],
        "field_typing_gap_count": roll["field_typing_gap_count"],
        "extractor_too_narrow_count": roll["extractor_too_narrow_count"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
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
        "schema_version": "typed_machine_readable_extraction_gap_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_extraction_repair_halt",
                "question": "why did extraction repair still fail",
                "answer": "no extraction rule candidates; 21 row json path repairs required",
                "taken": "classify source/path/typing/narrowness causes",
            },
            {
                "step": "review_gap_causes",
                "question": "which repair surface should be built next",
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
    failures = validate_basis()

    if failures:
        gap_records = []
        resolutions = []
        candidates = []
        nonext = []
        row_table = {"schema_version": "typed_machine_readable_row_json_path_gap_table_v0", "record_count": 0, "records": []}
        source_layer = {"schema_version": "typed_machine_readable_source_ref_layer_review_v0", "source_layer_counts": {}, "record_count": 0, "records": []}
        field_table = {"schema_version": "typed_machine_readable_field_typing_gap_table_v0", "record_count": 0, "records": []}
        narrowness = {"schema_version": "typed_machine_readable_extraction_unit_narrowness_review_v0", "extractor_too_narrow_count": 0, "record_count": 0, "records": []}
        status = "TYPED_MACHINE_READABLE_EXTRACTION_GAP_REVIEW_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_MACHINE_READABLE_EXTRACTION_GAP_REVIEW_BASIS_V0"
    else:
        diagnostics, resolutions, candidates, nonext = records()
        gap_records = [classify_gap(d) for d in diagnostics]
        row_table, source_layer, field_table, narrowness = build_tables(gap_records, resolutions, candidates)
        status, reason_codes, next_edge = decide(gap_records, row_table, field_table, narrowness)

    roll = rollup_obj(status, gap_records, row_table, source_layer, field_table, narrowness, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    boundary = authority_boundary_obj(status)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    assessment = {
        "schema_version": "typed_machine_readable_extraction_gap_review_assessment_v0",
        "review_status": status,
        "source_extraction_repair_receipt_id": SOURCE_EXTRACTION_REPAIR_RECEIPT_ID,
        "review_mode": "gap_cause_review_no_values",
        "machine_readable_slot_count": roll["machine_readable_slot_count"],
        "primary_gap_cause_counts": roll["primary_gap_cause_counts"],
        "recommended_repair_action_counts": roll["recommended_repair_action_counts"],
        "review_conclusion": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    cause_classification = {
        "schema_version": "typed_machine_readable_extraction_gap_cause_classification_v0",
        "classification_status": "GAP_CAUSES_CLASSIFIED",
        "records": gap_records,
    }

    repair_options = {
        "schema_version": "typed_machine_readable_extraction_gap_repair_plan_options_v0",
        "repair_options_status": "REPAIR_PLAN_OPTIONS_EMITTED",
        "selected_recommended_next": next_edge,
        "safe_options": [
            {
                "option": "REFINE_SOURCE_REF_OR_ROW_PATH_TYPING_SURFACE",
                "recommended": next_edge == "REFINE_MACHINE_READABLE_SOURCE_REF_OR_ROW_PATH_TYPING_SURFACE_V0",
                "next_unit": "REFINE_MACHINE_READABLE_SOURCE_REF_OR_ROW_PATH_TYPING_SURFACE_V0",
                "meaning": "Repair the row source refs / JSON paths so machine-readable slots point at typed field-bearing artifacts.",
            },
            {
                "option": "REFINE_FIELD_TYPING_SURFACE",
                "recommended": next_edge == "REFINE_MACHINE_READABLE_FIELD_TYPING_SURFACE_V0",
                "next_unit": "REFINE_MACHINE_READABLE_FIELD_TYPING_SURFACE_V0",
                "meaning": "Add/bridge typed field keys in already resolving source artifacts.",
            },
            {
                "option": "REPAIR_EXTRACTOR_RULE_CANDIDATE_EMISSION",
                "recommended": next_edge == "REPAIR_MACHINE_READABLE_EXTRACTION_RULE_CANDIDATE_EMISSION_V0",
                "next_unit": "REPAIR_MACHINE_READABLE_EXTRACTION_RULE_CANDIDATE_EMISSION_V0",
                "meaning": "Extractor saw candidates but failed to emit rule candidates.",
            },
            {
                "option": "FREEZE_AS_DIAGNOSTIC_REFERENCE",
                "recommended": False,
                "next_unit": "FREEZE_MACHINE_READABLE_EXTRACTION_GAP_REVIEW_V0",
                "meaning": "Freeze if branch should stop here.",
            },
        ],
        "forbidden_shortcuts": [
            "manual raw value entry",
            "authorize null reasons",
            "apply values",
            "metadata population",
            "discriminator readiness",
            "rule refinement",
            "tie break",
            "target selection",
            "runtime patch",
        ],
    }

    next_contract = {
        "schema_version": "typed_machine_readable_source_ref_field_typing_refinement_contract_v0",
        "contract_status": "NEXT_REFINEMENT_CONTRACT_EMITTED",
        "source_gap_review_receipt_pending": True,
        "required_inputs_for_next_unit": [
            "gap cause classification",
            "row json path gap table",
            "source ref layer review",
            "field typing gap table",
        ],
        "recommended_next_unit": next_edge,
        "must_not": [
            "infer values from row text without typed path",
            "treat source path resolution as value availability",
            "materialize source packet",
            "mark discriminator ready",
            "authorize human/schema fields",
        ],
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    classification = {
        "schema_version": "typed_machine_readable_extraction_gap_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "machine_readable_slot_count": roll["machine_readable_slot_count"],
        "primary_gap_cause_counts": roll["primary_gap_cause_counts"],
        "recommended_repair_action_counts": roll["recommended_repair_action_counts"],
        "row_json_path_gap_count": roll["row_json_path_gap_count"],
        "field_typing_gap_count": roll["field_typing_gap_count"],
        "extractor_too_narrow_count": roll["extractor_too_narrow_count"],
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

    write_json(GAP_REVIEW_ASSESSMENT_PATH, assessment)
    write_json(ROW_JSON_PATH_GAP_TABLE_PATH, row_table)
    write_json(SOURCE_REF_LAYER_REVIEW_PATH, source_layer)
    write_json(FIELD_TYPING_GAP_TABLE_PATH, field_table)
    write_json(EXTRACTION_UNIT_NARROWNESS_REVIEW_PATH, narrowness)
    write_json(GAP_CAUSE_CLASSIFICATION_PATH, cause_classification)
    write_json(REPAIR_PLAN_OPTIONS_PATH, repair_options)
    write_json(NEXT_SURFACE_CONTRACT_PATH, next_contract)
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
        "GAP_REVIEW_0_EXTRACTION_REPAIR_RECEIPT_CONSUMED": SOURCE_EXTRACTION_REPAIR_RECEIPT_PATH.exists(),
        "GAP_REVIEW_1_SLOT_DIAGNOSTIC_CONSUMED": SOURCE_MACHINE_SLOT_DIAGNOSTIC_PATH.exists(),
        "GAP_REVIEW_2_GAP_REVIEW_ASSESSMENT_EMITTED": GAP_REVIEW_ASSESSMENT_PATH.exists(),
        "GAP_REVIEW_3_ROW_JSON_PATH_GAP_TABLE_EMITTED": ROW_JSON_PATH_GAP_TABLE_PATH.exists(),
        "GAP_REVIEW_4_SOURCE_REF_LAYER_REVIEW_EMITTED": SOURCE_REF_LAYER_REVIEW_PATH.exists(),
        "GAP_REVIEW_5_FIELD_TYPING_GAP_TABLE_EMITTED": FIELD_TYPING_GAP_TABLE_PATH.exists(),
        "GAP_REVIEW_6_EXTRACTION_NARROWNESS_REVIEW_EMITTED": EXTRACTION_UNIT_NARROWNESS_REVIEW_PATH.exists(),
        "GAP_REVIEW_7_GAP_CAUSE_CLASSIFICATION_EMITTED": GAP_CAUSE_CLASSIFICATION_PATH.exists(),
        "GAP_REVIEW_8_REPAIR_PLAN_OPTIONS_EMITTED": REPAIR_PLAN_OPTIONS_PATH.exists(),
        "GAP_REVIEW_9_NEXT_SURFACE_CONTRACT_EMITTED": NEXT_SURFACE_CONTRACT_PATH.exists(),
        "GAP_REVIEW_10_NO_VALUES_AUTHORIZED": roll["values_authorized_count"] == 0,
        "GAP_REVIEW_11_NO_VALUES_APPLIED": roll["values_applied_count"] == 0,
        "GAP_REVIEW_12_NO_NULL_REASONS_ACCEPTED": roll["null_reason_accepted_count"] == 0,
        "GAP_REVIEW_13_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "GAP_REVIEW_14_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "GAP_REVIEW_15_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "GAP_REVIEW_16_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "GAP_REVIEW_17_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "GAP_REVIEW_18_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "GAP_REVIEW_19_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "GAP_REVIEW_20_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "GAP_REVIEW_21_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "GAP_REVIEW_22_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "GAP_REVIEW_23_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "GAP_REVIEW_24_NO_C5_OPENED": classification["c5_authorized"] is False,
        "GAP_REVIEW_25_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "GAP_REVIEW_26_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "GAP_REVIEW_27_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "GAP_REVIEW_28_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "GAP_REVIEW_29_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "GAP_REVIEW_30_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_MACHINE_READABLE_EXTRACTION_GAP_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "slot_count": roll["machine_readable_slot_count"],
        "primary_gap_cause_counts": roll["primary_gap_cause_counts"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_machine_readable_extraction_gap_review_receipt_v0",
        "receipt_type": "TYPED_MACHINE_READABLE_EXTRACTION_GAP_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_extraction_repair_receipt_id": SOURCE_EXTRACTION_REPAIR_RECEIPT_ID,
        "machine_readable_extraction_gap_review_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "machine_readable_slot_count": roll["machine_readable_slot_count"],
            "primary_gap_cause_counts": roll["primary_gap_cause_counts"],
            "recommended_repair_action_counts": roll["recommended_repair_action_counts"],
            "row_json_path_gap_count": roll["row_json_path_gap_count"],
            "field_typing_gap_count": roll["field_typing_gap_count"],
            "extractor_too_narrow_count": roll["extractor_too_narrow_count"],
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
            "gap_review_assessment": rel(GAP_REVIEW_ASSESSMENT_PATH),
            "row_json_path_gap_table": rel(ROW_JSON_PATH_GAP_TABLE_PATH),
            "source_ref_layer_review": rel(SOURCE_REF_LAYER_REVIEW_PATH),
            "field_typing_gap_table": rel(FIELD_TYPING_GAP_TABLE_PATH),
            "extraction_unit_narrowness_review": rel(EXTRACTION_UNIT_NARROWNESS_REVIEW_PATH),
            "gap_cause_classification": rel(GAP_CAUSE_CLASSIFICATION_PATH),
            "repair_plan_options": rel(REPAIR_PLAN_OPTIONS_PATH),
            "next_surface_contract": rel(NEXT_SURFACE_CONTRACT_PATH),
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
    print(f"machine_readable_extraction_gap_review_receipt_id={receipt_id}")
    print(f"machine_readable_extraction_gap_review_receipt_path={rel(receipt_path)}")
    print(f"machine_readable_extraction_gap_review_assessment_path={rel(GAP_REVIEW_ASSESSMENT_PATH)}")
    print(f"row_json_path_gap_table_path={rel(ROW_JSON_PATH_GAP_TABLE_PATH)}")
    print(f"source_ref_layer_review_path={rel(SOURCE_REF_LAYER_REVIEW_PATH)}")
    print(f"field_typing_gap_table_path={rel(FIELD_TYPING_GAP_TABLE_PATH)}")
    print(f"extraction_unit_narrowness_review_path={rel(EXTRACTION_UNIT_NARROWNESS_REVIEW_PATH)}")
    print(f"gap_cause_classification_path={rel(GAP_CAUSE_CLASSIFICATION_PATH)}")
    print(f"repair_plan_options_path={rel(REPAIR_PLAN_OPTIONS_PATH)}")
    print(f"next_surface_contract_path={rel(NEXT_SURFACE_CONTRACT_PATH)}")
    print(f"machine_readable_extraction_gap_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"machine_readable_extraction_gap_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
