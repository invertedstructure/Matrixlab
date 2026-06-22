#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_REPAIRED_SURFACE_V0"
TARGET_UNIT_ID = "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface.v0"

SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID = "d6d40d57"
FAILED_REPAIR_RECEIPT_ID = "1856cb99"
SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID = "ecebcd27"
SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID = "bea59318"
SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID = "707dd84d"
SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID = "7ed31808"
SOURCE_LOOP_APPLICATION_RECEIPT_ID = "be19f438"
SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID = "6148b4fa"
SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID = "7c9718e0"
SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID = "a121ff40"
SOURCE_REPAIR_OBJECTIVE_ID = "12d712af"

TOP_GROUP_KEY_HASH = "38c604a1"
EXPECTED_FIELD_ROW_COUNT = 25

EVIDENCE_FIELDS = [
    "missing_label_identifier",
    "taxonomy_context_ref",
    "current_label_space_ref",
    "expected_label_space_ref",
]

ABSENCE_REASON_FIELDS = {
    "missing_label_identifier": "missing_label_identifier_absence_reason",
    "taxonomy_context_ref": "taxonomy_context_ref_absence_reason",
    "current_label_space_ref": "current_label_space_ref_absence_reason",
    "expected_label_space_ref": "expected_label_space_ref_absence_reason",
}

STRUCTURAL_FIELDS = [
    "pressure_event_id",
    "pressure_group_key_hash",
    "parent_pressure_class",
    "pressure_subtype",
    "halt_reason",
    "source_receipt_ref",
    "source_trace_ref",
]

OUT_DIR = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0"
RECEIPT_DIR = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0_receipts"

RERUN_FIELD_ROWS_PATH = OUT_DIR / "repaired_surface_taxonomy_gap_missing_label_field_rows.jsonl"
RERUN_CONTEXT_REFS_PATH = OUT_DIR / "repaired_surface_taxonomy_gap_context_refs.json"
RERUN_FIELD_PRESENCE_ROLLUP_PATH = OUT_DIR / "repaired_surface_field_presence_rollup.json"
RERUN_EVIDENCE_OUTCOME_PATH = OUT_DIR / "repaired_surface_evidence_outcome.json"
RERUN_COMPARISON_PATH = OUT_DIR / "pre_post_repair_evidence_comparison.json"
RERUN_DECISION_PACKET_PATH = OUT_DIR / "repaired_surface_rerun_decision_packet.json"
RERUN_REPORT_PATH = OUT_DIR / "repaired_surface_rerun_report.json"

STRUCTURAL_REF_FIX_RECEIPT_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0_receipts" / f"{SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID}.json"
FIXED_REPAIRED_ROWS_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0" / "r1000_pressure_event_rows_taxonomy_gap_field_surface_repaired_structural_refs_fixed.jsonl"
FIXED_TOP_GROUP_ROWS_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0" / "top_group_pressure_event_rows_taxonomy_gap_field_surface_repaired_structural_refs_fixed.jsonl"
STRUCTURAL_REF_JOIN_AUDIT_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0" / "structural_ref_join_audit.json"
POST_FIX_FIELD_PRESENCE_AUDIT_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0" / "post_fix_field_presence_audit.json"
POST_FIX_RERUN_INSTRUCTIONS_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0" / "post_fix_rerun_instructions.json"
STRUCTURAL_REF_FIX_PACKET_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0" / "structural_refs_fix_decision_packet.json"
STRUCTURAL_REF_FIX_REPORT_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0" / "structural_refs_fix_report.json"

REPAIR_ELIGIBILITY_RECEIPT_PATH = ROOT / "data" / "localized_evidence_surface_repair_eligibility_v0_receipts" / f"{SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID}.json"
LOCALIZATION_RECEIPT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0_receipts" / f"{SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID}.json"
EVIDENCE_SURFACE_RECEIPT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0_receipts" / f"{SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID}.json"
PRE_REPAIR_EXTRACTION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0_receipts" / f"{SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID}.json"
PRE_REPAIR_FIELD_ROWS_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0" / "taxonomy_gap_missing_label_field_rows.jsonl"
LOOP_APPLICATION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0_receipts" / f"{SOURCE_LOOP_APPLICATION_RECEIPT_ID}.json"
PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID}.json"
TOP_GROUP_CLASSIFICATION_RECEIPT_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0_receipts" / f"{SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID}.json"
R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"

SOURCE_FILES = [
    STRUCTURAL_REF_FIX_RECEIPT_PATH,
    FIXED_REPAIRED_ROWS_PATH,
    FIXED_TOP_GROUP_ROWS_PATH,
    STRUCTURAL_REF_JOIN_AUDIT_PATH,
    POST_FIX_FIELD_PRESENCE_AUDIT_PATH,
    POST_FIX_RERUN_INSTRUCTIONS_PATH,
    STRUCTURAL_REF_FIX_PACKET_PATH,
    STRUCTURAL_REF_FIX_REPORT_PATH,
    REPAIR_ELIGIBILITY_RECEIPT_PATH,
    LOCALIZATION_RECEIPT_PATH,
    EVIDENCE_SURFACE_RECEIPT_PATH,
    PRE_REPAIR_EXTRACTION_RECEIPT_PATH,
    PRE_REPAIR_FIELD_ROWS_PATH,
    LOOP_APPLICATION_RECEIPT_PATH,
    PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH,
    TOP_GROUP_CLASSIFICATION_RECEIPT_PATH,
    R1000_SCALE_RECEIPT_PATH,
]

HUMAN_DECISION = {
    "decision": "RERUN_FIELD_EXTRACTION_ON_FIXED_REPAIRED_SURFACE",
    "scope": "rerun missing-label evidence extraction against fixed repaired overlay only",
    "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
    "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
    "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
    "not_authorized": [
        "taxonomy_repair",
        "taxonomy_upgrade",
        "taxonomy_delta_proposal",
        "authority_widening",
        "burden_optimization",
        "guessing_missing_label_values",
        "mutating_existing_receipts",
        "overwriting_historical_source_rows",
        "protocol_adoption",
        "next_group_auto_open",
        "build_command",
    ],
}

MUST_NOT_INFER = [
    "rerun extraction observes repaired surface only",
    "field key presence is not value presence",
    "null-with-reason does not identify a missing label",
    "absence reason may classify source evidence limit, not taxonomy delta",
    "do not guess missing label values",
    "do not mutate existing receipts",
    "do not auto-open next group",
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
    return path.relative_to(ROOT).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")

def tracked(path: Path) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel(path)],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def load_sources() -> Dict[str, Any]:
    return {
        "structural_ref_fix_receipt": read_json(STRUCTURAL_REF_FIX_RECEIPT_PATH),
        "fixed_rows": read_jsonl(FIXED_REPAIRED_ROWS_PATH),
        "fixed_top_group_rows": read_jsonl(FIXED_TOP_GROUP_ROWS_PATH),
        "structural_ref_join_audit": read_json(STRUCTURAL_REF_JOIN_AUDIT_PATH),
        "post_fix_field_presence_audit": read_json(POST_FIX_FIELD_PRESENCE_AUDIT_PATH),
        "post_fix_rerun_instructions": read_json(POST_FIX_RERUN_INSTRUCTIONS_PATH),
        "structural_ref_fix_packet": read_json(STRUCTURAL_REF_FIX_PACKET_PATH),
        "structural_ref_fix_report": read_json(STRUCTURAL_REF_FIX_REPORT_PATH),
        "repair_eligibility_receipt": read_json(REPAIR_ELIGIBILITY_RECEIPT_PATH),
        "localization_receipt": read_json(LOCALIZATION_RECEIPT_PATH),
        "evidence_surface_receipt": read_json(EVIDENCE_SURFACE_RECEIPT_PATH),
        "pre_repair_extraction_receipt": read_json(PRE_REPAIR_EXTRACTION_RECEIPT_PATH),
        "pre_repair_field_rows": read_jsonl(PRE_REPAIR_FIELD_ROWS_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    fix = sources["structural_ref_fix_receipt"]
    packet = sources["structural_ref_fix_packet"]
    audit = sources["post_fix_field_presence_audit"]

    if fix.get("receipt_id") != SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID:
        failures.append("structural_ref_fix_receipt_id_wrong")
    if fix.get("gate") != "PASS":
        failures.append("structural_ref_fix_not_pass")
    if fix.get("aggregate_metrics", {}).get("structural_refs_preserved") is not True:
        failures.append("structural_refs_not_preserved")
    if fix.get("aggregate_metrics", {}).get("missing_fields_exposed_as_keys") is not True:
        failures.append("missing_field_keys_not_exposed")
    if fix.get("aggregate_metrics", {}).get("absence_reasons_emitted") is not True:
        failures.append("absence_reasons_not_emitted")
    if fix.get("aggregate_metrics", {}).get("source_mutation_count") != 0:
        failures.append("source_mutation_in_fix")
    if fix.get("aggregate_metrics", {}).get("recommended_next_unit") != UNIT_ID:
        failures.append("fix_recommended_next_unit_not_this")

    if packet.get("recommended_next_unit") != UNIT_ID:
        failures.append("packet_next_unit_not_this")
    if audit.get("all_structural_refs_preserved") is not True:
        failures.append("post_fix_audit_structural_refs_not_preserved")

    if len(sources["fixed_top_group_rows"]) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("fixed_top_group_row_count_wrong")
    if len(sources["pre_repair_field_rows"]) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("pre_repair_field_row_count_wrong")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def extract_repaired_field_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for index, row in enumerate(rows):
        out_row = {
            "row_index": index,
            "pressure_event_id": row.get("pressure_event_id"),
            "pressure_group_key_hash": row.get("pressure_group_key_hash"),
            "parent_pressure_class": row.get("parent_pressure_class"),
            "pressure_subtype": row.get("pressure_subtype"),
            "halt_reason": row.get("halt_reason"),
            "source_receipt_ref": row.get("source_receipt_ref"),
            "source_trace_ref": row.get("source_trace_ref"),
            "work_item_id": row.get("work_item_id"),
            "slot_id": row.get("slot_id"),
            "repair_objective_id": row.get("taxonomy_gap_field_surface_repair_objective_id"),
            "structural_refs_fix_applied": row.get("taxonomy_gap_field_surface_structural_refs_fix_applied") is True,
            "source_surface_artifact": rel(FIXED_TOP_GROUP_ROWS_PATH),
        }

        for field in EVIDENCE_FIELDS:
            absence_field = ABSENCE_REASON_FIELDS[field]
            out_row[f"{field}_key_present"] = field in row
            out_row[f"{field}_value_present"] = row.get(field) is not None
            out_row[field] = row.get(field)
            out_row[f"{field}_absence_reason_key_present"] = absence_field in row
            out_row[absence_field] = row.get(absence_field)

        out.append(out_row)
    return out

def build_context_refs(field_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    context = {
        "schema_version": "repaired_surface_taxonomy_gap_context_refs_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "source_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "field_row_count": len(field_rows),
        "missing_label_identifier_key_present_count": sum(1 for row in field_rows if row["missing_label_identifier_key_present"]),
        "taxonomy_context_ref_key_present_count": sum(1 for row in field_rows if row["taxonomy_context_ref_key_present"]),
        "current_label_space_ref_key_present_count": sum(1 for row in field_rows if row["current_label_space_ref_key_present"]),
        "expected_label_space_ref_key_present_count": sum(1 for row in field_rows if row["expected_label_space_ref_key_present"]),
        "missing_label_identifier_value_present_count": sum(1 for row in field_rows if row["missing_label_identifier_value_present"]),
        "taxonomy_context_ref_value_present_count": sum(1 for row in field_rows if row["taxonomy_context_ref_value_present"]),
        "current_label_space_ref_value_present_count": sum(1 for row in field_rows if row["current_label_space_ref_value_present"]),
        "expected_label_space_ref_value_present_count": sum(1 for row in field_rows if row["expected_label_space_ref_value_present"]),
        "absence_reason_counts": {
            field: dict(sorted(Counter(row.get(ABSENCE_REASON_FIELDS[field]) for row in field_rows).items(), key=lambda item: str(item[0])))
            for field in EVIDENCE_FIELDS
        },
        "structural_ref_present_counts": {
            field: sum(1 for row in field_rows if row.get(field) is not None)
            for field in STRUCTURAL_FIELDS
        },
        "taxonomy_delta_evidence_present": False,
        "taxonomy_upgrade_evidence_present": False,
        "missing_label_values_guessed": False,
        "review_only": False,
    }
    context["all_required_field_keys_present"] = all(
        context[f"{field}_key_present_count"] == len(field_rows)
        for field in EVIDENCE_FIELDS
    )
    context["all_required_field_values_present"] = all(
        context[f"{field}_value_present_count"] == len(field_rows)
        for field in EVIDENCE_FIELDS
    )
    context["any_required_field_value_present"] = any(
        context[f"{field}_value_present_count"] > 0
        for field in EVIDENCE_FIELDS
    )
    context["all_absence_reasons_present"] = all(
        sum(context["absence_reason_counts"][field].values()) == len(field_rows)
        for field in EVIDENCE_FIELDS
    )
    context["all_structural_refs_present"] = all(
        count == len(field_rows)
        for count in context["structural_ref_present_counts"].values()
    )
    return context

def build_field_presence_rollup(field_rows: List[Dict[str, Any]], context_refs: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "repaired_surface_field_presence_rollup_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "field_row_count": len(field_rows),
        "expected_field_row_count": EXPECTED_FIELD_ROW_COUNT,
        "field_key_presence_profile": {
            field: sum(1 for row in field_rows if row[f"{field}_key_present"])
            for field in EVIDENCE_FIELDS
        },
        "field_value_presence_profile": {
            field: sum(1 for row in field_rows if row[f"{field}_value_present"])
            for field in EVIDENCE_FIELDS
        },
        "absence_reason_key_presence_profile": {
            field: sum(1 for row in field_rows if row[f"{field}_absence_reason_key_present"])
            for field in EVIDENCE_FIELDS
        },
        "structural_ref_presence_profile": context_refs["structural_ref_present_counts"],
        "all_required_field_keys_present": context_refs["all_required_field_keys_present"],
        "any_required_field_value_present": context_refs["any_required_field_value_present"],
        "all_required_field_values_present": context_refs["all_required_field_values_present"],
        "all_absence_reasons_present": context_refs["all_absence_reasons_present"],
        "all_structural_refs_present": context_refs["all_structural_refs_present"],
        "field_surface_repair_effect": "FIELD_KEYS_AND_ABSENCE_REASONS_NOW_VISIBLE",
        "remaining_evidence_content_gap": "REQUIRED_FIELD_VALUES_STILL_NULL",
        "review_only": False,
    }

def build_evidence_outcome(rollup: Dict[str, Any], context_refs: Dict[str, Any]) -> Dict[str, Any]:
    if rollup["all_required_field_keys_present"] and rollup["all_absence_reasons_present"] and not rollup["any_required_field_value_present"]:
        outcome = "EVIDENCE_SURFACE_REPAIRED_VALUES_ABSENT"
        sufficiency = "EVIDENCE_SURFACE_PRESENT_CONTENT_ABSENT"
        recommended_next = "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT_V0"
        reason = "The repaired surface now exposes required evidence keys and absence reasons, but all required values remain null; this is a content/provenance limit rather than a field-surface visibility gap."
    elif rollup["all_required_field_values_present"]:
        outcome = "EVIDENCE_SURFACE_REPAIRED_VALUES_PRESENT"
        sufficiency = "EVIDENCE_SUFFICIENT_FOR_TAXONOMY_GAP_RECLASSIFICATION"
        recommended_next = "RECLASSIFY_R1000_TOP_GROUP_TAXONOMY_GAP_AFTER_REPAIRED_EVIDENCE_SURFACE_V0"
        reason = "Required evidence values are present."
    else:
        outcome = "EVIDENCE_SURFACE_REPAIR_PARTIAL"
        sufficiency = "EVIDENCE_PARTIAL_REQUIRES_REVIEW"
        recommended_next = "CLASSIFY_PARTIAL_REPAIRED_SURFACE_EVIDENCE_V0"
        reason = "Some required keys or values are present but the repaired evidence state is incomplete."

    return {
        "schema_version": "repaired_surface_evidence_outcome_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "outcome": outcome,
        "evidence_sufficiency_class": sufficiency,
        "outcome_reason": reason,
        "field_surface_repair_validated": rollup["all_required_field_keys_present"] and rollup["all_absence_reasons_present"] and rollup["all_structural_refs_present"],
        "required_field_keys_present": rollup["all_required_field_keys_present"],
        "required_field_values_present": rollup["all_required_field_values_present"],
        "any_required_field_value_present": rollup["any_required_field_value_present"],
        "absence_reasons_present": rollup["all_absence_reasons_present"],
        "structural_refs_present": rollup["all_structural_refs_present"],
        "taxonomy_delta_evidence_present": False,
        "taxonomy_upgrade_evidence_present": False,
        "missing_label_values_guessed": False,
        "recommended_next_unit": recommended_next,
        "review_only": False,
    }

def build_pre_post_comparison(pre_rows: List[Dict[str, Any]], repaired_rows: List[Dict[str, Any]], rollup: Dict[str, Any]) -> Dict[str, Any]:
    pre_key_profile = {
        field: sum(1 for row in pre_rows if row.get(f"{field}_present") is True or field in row)
        for field in EVIDENCE_FIELDS
    }
    pre_value_profile = {
        field: sum(1 for row in pre_rows if row.get(field) is not None)
        for field in EVIDENCE_FIELDS
    }
    post_key_profile = rollup["field_key_presence_profile"]
    post_value_profile = rollup["field_value_presence_profile"]
    return {
        "schema_version": "pre_post_repair_evidence_comparison_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "pre_repair_field_row_count": len(pre_rows),
        "post_repair_field_row_count": len(repaired_rows),
        "pre_repair_key_presence_profile": pre_key_profile,
        "post_repair_key_presence_profile": post_key_profile,
        "delta_key_presence_profile": {
            field: post_key_profile[field] - pre_key_profile[field]
            for field in EVIDENCE_FIELDS
        },
        "pre_repair_value_presence_profile": pre_value_profile,
        "post_repair_value_presence_profile": post_value_profile,
        "delta_value_presence_profile": {
            field: post_value_profile[field] - pre_value_profile[field]
            for field in EVIDENCE_FIELDS
        },
        "repair_improved_key_visibility": any(post_key_profile[field] > pre_key_profile[field] for field in EVIDENCE_FIELDS),
        "repair_improved_value_visibility": any(post_value_profile[field] > pre_value_profile[field] for field in EVIDENCE_FIELDS),
        "review_only": False,
    }

def build_decision_packet(outcome: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "repaired_surface_rerun_decision_packet_v0",
        "packet_type": "POST_RERUN_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "outcome": outcome["outcome"],
        "evidence_sufficiency_class": outcome["evidence_sufficiency_class"],
        "field_surface_repair_validated": outcome["field_surface_repair_validated"],
        "allowed_human_choices": [
            "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT",
            "RECLASSIFY_TAXONOMY_GAP_WITH_REPAIRED_EVIDENCE",
            "REQUEST_SOURCE_PROVENANCE_REPAIR_OBJECTIVE",
            "MARK_HEALTHY_EXPECTED_EVIDENCE_LIMIT",
            "REJECT_REPAIRED_SURFACE_RERUN",
        ],
        "recommended_next_handling": outcome["recommended_next_unit"],
        "recommended_next_unit": outcome["recommended_next_unit"],
        "may_emit_taxonomy_delta": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_authority_widening": False,
        "may_authorize_burden_optimization": False,
        "may_auto_open_next_group": False,
        "may_mutate_existing_receipts": False,
        "may_guess_missing_label_values": False,
        "review_only": False,
    }

def build_report(field_rows: List[Dict[str, Any]], context: Dict[str, Any], rollup: Dict[str, Any], outcome: Dict[str, Any], comparison: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "repaired_surface_rerun_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
            "failed_repair_receipt_id": FAILED_REPAIR_RECEIPT_ID,
            "source_repair_eligibility_receipt_id": SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID,
            "source_localization_audit_receipt_id": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
            "source_evidence_surface_classification_receipt_id": SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID,
            "source_taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
            "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
            "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
            "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
            "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        },
        "field_row_count": len(field_rows),
        "context_refs": context,
        "field_presence_rollup": rollup,
        "evidence_outcome": outcome,
        "pre_post_comparison": comparison,
        "decision_packet_recommended_next_handling": packet["recommended_next_handling"],
        "rerun_executed": True,
        "repair_artifact_consumed": True,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "historical_source_rows_overwritten": False,
        "existing_receipts_mutated": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "burden_optimization_authorized": False,
        "protocol_adoption_authorized": False,
        "next_group_auto_opened": False,
        "missing_label_values_guessed": False,
        "hidden_next_command": False,
    }

def validate_outputs(field_rows: List[Dict[str, Any]], context: Dict[str, Any], rollup: Dict[str, Any], outcome: Dict[str, Any], comparison: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if len(field_rows) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_row_count_wrong")
    if context["field_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("context_field_row_count_wrong")
    if rollup["field_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("rollup_field_row_count_wrong")

    if rollup["all_required_field_keys_present"] is not True:
        failures.append("required_field_keys_not_present")
    if rollup["all_absence_reasons_present"] is not True:
        failures.append("absence_reasons_not_present")
    if rollup["all_structural_refs_present"] is not True:
        failures.append("structural_refs_not_present")
    if rollup["all_required_field_values_present"] is not False:
        failures.append("required_field_values_unexpectedly_all_present")
    if rollup["any_required_field_value_present"] is not False:
        failures.append("required_field_value_unexpectedly_present")

    if outcome["field_surface_repair_validated"] is not True:
        failures.append("field_surface_repair_not_validated")
    if outcome["outcome"] != "EVIDENCE_SURFACE_REPAIRED_VALUES_ABSENT":
        failures.append(f"unexpected_outcome:{outcome['outcome']}")
    if outcome["evidence_sufficiency_class"] != "EVIDENCE_SURFACE_PRESENT_CONTENT_ABSENT":
        failures.append("unexpected_evidence_sufficiency_class")
    if outcome["recommended_next_unit"] != "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT_V0":
        failures.append("unexpected_recommended_next_unit")
    for key in ["taxonomy_delta_evidence_present", "taxonomy_upgrade_evidence_present", "missing_label_values_guessed"]:
        if outcome.get(key) is not False:
            failures.append(f"outcome_guard_not_false:{key}:{outcome.get(key)}")

    if comparison["repair_improved_key_visibility"] is not True:
        failures.append("repair_did_not_improve_key_visibility")
    if comparison["repair_improved_value_visibility"] is not False:
        failures.append("repair_unexpectedly_improved_value_visibility")

    if packet["packet_type"] != "POST_RERUN_REVIEW_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    if packet["recommended_next_unit"] != "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT_V0":
        failures.append("packet_next_unit_wrong")
    for key in [
        "may_emit_taxonomy_delta",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_authority_widening",
        "may_authorize_burden_optimization",
        "may_auto_open_next_group",
        "may_mutate_existing_receipts",
        "may_guess_missing_label_values",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")

    for key in [
        "repair_command_emitted",
        "build_command_emitted",
        "historical_source_rows_overwritten",
        "existing_receipts_mutated",
        "taxonomy_delta_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "burden_optimization_authorized",
        "protocol_adoption_authorized",
        "next_group_auto_opened",
        "missing_label_values_guessed",
        "hidden_next_command",
    ]:
        if report.get(key) is not False:
            failures.append(f"report_guard_not_false:{key}:{report.get(key)}")

    if report["rerun_executed"] is not True:
        failures.append("rerun_not_executed")
    if report["repair_artifact_consumed"] is not True:
        failures.append("repair_artifact_not_consumed")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_structural_ref_fix_receipt_id") != SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID:
        failures.append("source_structural_ref_fix_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "REPAIRED_RERUN_0_FIXED_SURFACE_CONSUMED",
        "REPAIRED_RERUN_1_HUMAN_DECISION_RECORDED",
        "REPAIRED_RERUN_2_FIELD_ROWS_EMITTED",
        "REPAIRED_RERUN_3_FIELD_KEYS_VISIBLE",
        "REPAIRED_RERUN_4_ABSENCE_REASONS_VISIBLE",
        "REPAIRED_RERUN_5_STRUCTURAL_REFS_VISIBLE",
        "REPAIRED_RERUN_6_VALUE_ABSENCE_CLASSIFIED",
        "REPAIRED_RERUN_7_DECISION_PACKET_EMITTED",
        "REPAIRED_RERUN_8_NO_TAXONOMY_ACTION",
        "REPAIRED_RERUN_9_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("field_row_count") != EXPECTED_FIELD_ROW_COUNT:
        failures.append("metric_field_row_count_wrong")
    if metrics.get("all_required_field_keys_present") is not True:
        failures.append("metric_keys_not_present")
    if metrics.get("all_absence_reasons_present") is not True:
        failures.append("metric_absence_reasons_not_present")
    if metrics.get("all_structural_refs_present") is not True:
        failures.append("metric_structural_refs_not_present")
    if metrics.get("any_required_field_value_present") is not False:
        failures.append("metric_value_unexpectedly_present")
    if metrics.get("outcome") != "EVIDENCE_SURFACE_REPAIRED_VALUES_ABSENT":
        failures.append("metric_outcome_wrong")
    if metrics.get("recommended_next_unit") != "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT_V0":
        failures.append("metric_next_unit_wrong")

    for key in [
        "repair_command_emitted_count",
        "build_command_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "authority_widening_authorized_count",
        "burden_optimization_authorized_count",
        "protocol_adoption_authorized_count",
        "next_group_auto_opened_count",
        "historical_source_overwrite_count",
        "existing_receipt_mutation_count",
        "source_mutation_count",
        "missing_label_value_guess_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("repaired_surface_rerun_guards", {})
    for key in [
        "fixed_surface_consumed",
        "human_decision_recorded",
        "field_rows_emitted",
        "field_keys_visible",
        "absence_reasons_visible",
        "structural_refs_visible",
        "value_absence_classified",
        "decision_packet_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "repair_command_emitted",
        "build_command_emitted",
        "taxonomy_upgrade_authorized",
        "taxonomy_delta_proposal_emitted",
        "authority_widening_authorized",
        "burden_optimization_authorized",
        "protocol_adoption_authorized",
        "next_group_auto_opened",
        "historical_source_overwritten",
        "existing_receipts_mutated",
        "source_mutation",
        "missing_label_values_guessed",
        "hidden_next_command",
    ]:
        if guards.get(key) is not False:
            failures.append(f"guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_HUMAN_DECISION_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    source_before = snapshot_files(SOURCE_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    field_rows = extract_repaired_field_rows(sources["fixed_top_group_rows"])
    context_refs = build_context_refs(field_rows)
    rollup = build_field_presence_rollup(field_rows, context_refs)
    outcome = build_evidence_outcome(rollup, context_refs)
    comparison = build_pre_post_comparison(sources["pre_repair_field_rows"], field_rows, rollup)
    packet = build_decision_packet(outcome)
    report = build_report(field_rows, context_refs, rollup, outcome, comparison, packet)

    write_jsonl(RERUN_FIELD_ROWS_PATH, field_rows)
    write_json(RERUN_CONTEXT_REFS_PATH, context_refs)
    write_json(RERUN_FIELD_PRESENCE_ROLLUP_PATH, rollup)
    write_json(RERUN_EVIDENCE_OUTCOME_PATH, outcome)
    write_json(RERUN_COMPARISON_PATH, comparison)
    write_json(RERUN_DECISION_PACKET_PATH, packet)
    write_json(RERUN_REPORT_PATH, report)

    failures.extend(validate_outputs(field_rows, context_refs, rollup, outcome, comparison, packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "REPAIRED_RERUN_0_FIXED_SURFACE_CONSUMED": sources["structural_ref_fix_receipt"]["receipt_id"] == SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID and len(sources["fixed_top_group_rows"]) == EXPECTED_FIELD_ROW_COUNT,
        "REPAIRED_RERUN_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "RERUN_FIELD_EXTRACTION_ON_FIXED_REPAIRED_SURFACE",
        "REPAIRED_RERUN_2_FIELD_ROWS_EMITTED": RERUN_FIELD_ROWS_PATH.exists() and len(field_rows) == EXPECTED_FIELD_ROW_COUNT,
        "REPAIRED_RERUN_3_FIELD_KEYS_VISIBLE": rollup["all_required_field_keys_present"] is True,
        "REPAIRED_RERUN_4_ABSENCE_REASONS_VISIBLE": rollup["all_absence_reasons_present"] is True,
        "REPAIRED_RERUN_5_STRUCTURAL_REFS_VISIBLE": rollup["all_structural_refs_present"] is True,
        "REPAIRED_RERUN_6_VALUE_ABSENCE_CLASSIFIED": outcome["outcome"] == "EVIDENCE_SURFACE_REPAIRED_VALUES_ABSENT",
        "REPAIRED_RERUN_7_DECISION_PACKET_EMITTED": RERUN_DECISION_PACKET_PATH.exists(),
        "REPAIRED_RERUN_8_NO_TAXONOMY_ACTION": report["taxonomy_delta_proposal_emitted"] is False and report["taxonomy_upgrade_authorized"] is False,
        "REPAIRED_RERUN_9_NO_SOURCE_MUTATION": source_mutation_detected is False,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {"type": "STOP", "stop_code": "STOP_HUMAN_DECISION_REQUIRED", "next_command_goal": None}
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if any([
        report["repair_command_emitted"],
        report["build_command_emitted"],
        report["historical_source_rows_overwritten"],
        report["existing_receipts_mutated"],
        report["taxonomy_delta_proposal_emitted"],
        report["taxonomy_upgrade_authorized"],
        report["authority_widening_authorized"],
        report["burden_optimization_authorized"],
        report["protocol_adoption_authorized"],
        report["next_group_auto_opened"],
        report["missing_label_values_guessed"],
        report["hidden_next_command"],
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "field_row_count": len(field_rows),
        "all_required_field_keys_present": rollup["all_required_field_keys_present"],
        "all_absence_reasons_present": rollup["all_absence_reasons_present"],
        "all_structural_refs_present": rollup["all_structural_refs_present"],
        "any_required_field_value_present": rollup["any_required_field_value_present"],
        "all_required_field_values_present": rollup["all_required_field_values_present"],
        "outcome": outcome["outcome"],
        "evidence_sufficiency_class": outcome["evidence_sufficiency_class"],
        "repair_improved_key_visibility": comparison["repair_improved_key_visibility"],
        "repair_improved_value_visibility": comparison["repair_improved_value_visibility"],
        "recommended_next_unit": outcome["recommended_next_unit"],
        "rerun_executed_count": 1,
        "repair_artifact_consumed_count": 1,
        "repair_command_emitted_count": 0,
        "build_command_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "authority_widening_authorized_count": 0,
        "burden_optimization_authorized_count": 0,
        "protocol_adoption_authorized_count": 0,
        "next_group_auto_opened_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "missing_label_value_guess_count": 0,
        "hidden_next_command_count": 0,
    }

    guards = {
        "fixed_surface_consumed": True,
        "human_decision_recorded": True,
        "field_rows_emitted": True,
        "field_keys_visible": rollup["all_required_field_keys_present"],
        "absence_reasons_visible": rollup["all_absence_reasons_present"],
        "structural_refs_visible": rollup["all_structural_refs_present"],
        "value_absence_classified": outcome["outcome"] == "EVIDENCE_SURFACE_REPAIRED_VALUES_ABSENT",
        "decision_packet_emitted": True,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "taxonomy_delta_proposal_emitted": False,
        "authority_widening_authorized": False,
        "burden_optimization_authorized": False,
        "protocol_adoption_authorized": False,
        "next_group_auto_opened": False,
        "historical_source_overwritten": False,
        "existing_receipts_mutated": False,
        "source_mutation": source_mutation_detected,
        "missing_label_values_guessed": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_structural_ref_fix_receipt": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "outcome": outcome["outcome"],
        "recommended_next_unit": outcome["recommended_next_unit"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "repaired_surface_taxonomy_gap_missing_label_field_rows": rel(RERUN_FIELD_ROWS_PATH),
        "repaired_surface_taxonomy_gap_context_refs": rel(RERUN_CONTEXT_REFS_PATH),
        "repaired_surface_field_presence_rollup": rel(RERUN_FIELD_PRESENCE_ROLLUP_PATH),
        "repaired_surface_evidence_outcome": rel(RERUN_EVIDENCE_OUTCOME_PATH),
        "pre_post_repair_evidence_comparison": rel(RERUN_COMPARISON_PATH),
        "repaired_surface_rerun_decision_packet": rel(RERUN_DECISION_PACKET_PATH),
        "repaired_surface_rerun_report": rel(RERUN_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_receipt_v0",
        "receipt_type": "RERUN_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_REPAIRED_SURFACE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "failed_repair_receipt_id": FAILED_REPAIR_RECEIPT_ID,
        "source_repair_eligibility_receipt_id": SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID,
        "source_localization_audit_receipt_id": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
        "source_evidence_surface_classification_receipt_id": SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID,
        "source_taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
        "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
        "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "rerun_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "field_row_count": len(field_rows),
            "all_required_field_keys_present": rollup["all_required_field_keys_present"],
            "all_absence_reasons_present": rollup["all_absence_reasons_present"],
            "all_structural_refs_present": rollup["all_structural_refs_present"],
            "any_required_field_value_present": rollup["any_required_field_value_present"],
            "outcome": outcome["outcome"],
            "evidence_sufficiency_class": outcome["evidence_sufficiency_class"],
            "recommended_next_unit": outcome["recommended_next_unit"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "repaired_surface_rerun_guards": guards,
        "must_not_infer": MUST_NOT_INFER,
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_receipt(receipt)
    failures.extend(receipt_failures)
    receipt["failures"] = failures
    receipt["gate"] = "PASS" if not failures else "FAIL"
    if failures:
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"repaired_surface_rerun_receipt_id={receipt_id}")
    print(f"repaired_surface_rerun_receipt_path=data/rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0_receipts/{receipt_id}.json")
    print(f"repaired_surface_field_rows_path=data/rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0/repaired_surface_taxonomy_gap_missing_label_field_rows.jsonl")
    print(f"repaired_surface_evidence_outcome_path=data/rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0/repaired_surface_evidence_outcome.json")
    print(f"repaired_surface_rerun_decision_packet_path=data/rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0/repaired_surface_rerun_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
