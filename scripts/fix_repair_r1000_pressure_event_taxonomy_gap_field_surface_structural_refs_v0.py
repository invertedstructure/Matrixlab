#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "FIX_REPAIR_R1000_PRESSURE_EVENT_TAXONOMY_GAP_FIELD_SURFACE_STRUCTURAL_REFS_V0"
TARGET_UNIT_ID = "repair_r1000_pressure_event_taxonomy_gap_field_surface.structural_refs_fix.v0"

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

MISSING_FIELDS = [
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

OUT_DIR = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0"
RECEIPT_DIR = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0_receipts"

FIX_PLAN_PATH = OUT_DIR / "structural_refs_fix_plan.json"
FIXED_REPAIRED_ROWS_PATH = OUT_DIR / "r1000_pressure_event_rows_taxonomy_gap_field_surface_repaired_structural_refs_fixed.jsonl"
FIXED_TOP_GROUP_ROWS_PATH = OUT_DIR / "top_group_pressure_event_rows_taxonomy_gap_field_surface_repaired_structural_refs_fixed.jsonl"
STRUCTURAL_REF_JOIN_AUDIT_PATH = OUT_DIR / "structural_ref_join_audit.json"
FIX_DIFF_SUMMARY_PATH = OUT_DIR / "structural_refs_fix_diff_summary.json"
POST_FIX_FIELD_PRESENCE_AUDIT_PATH = OUT_DIR / "post_fix_field_presence_audit.json"
POST_FIX_RERUN_INSTRUCTIONS_PATH = OUT_DIR / "post_fix_rerun_instructions.json"
FIX_DECISION_PACKET_PATH = OUT_DIR / "structural_refs_fix_decision_packet.json"
FIX_REPORT_PATH = OUT_DIR / "structural_refs_fix_report.json"

FAILED_REPAIR_RECEIPT_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_v0_receipts" / f"{FAILED_REPAIR_RECEIPT_ID}.json"
FAILED_REPAIR_PLAN_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_v0" / "repair_plan.json"
FAILED_REPAIR_SCHEMA_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_v0" / "repair_surface_schema.json"
FAILED_REPAIRED_ROWS_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_v0" / "r1000_pressure_event_rows_taxonomy_gap_field_surface_repaired.jsonl"
FAILED_REPAIRED_TOP_GROUP_ROWS_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_v0" / "top_group_pressure_event_rows_taxonomy_gap_field_surface_repaired.jsonl"
FAILED_REPAIR_DIFF_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_v0" / "repair_diff_summary.json"
FAILED_POST_REPAIR_AUDIT_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_v0" / "post_repair_field_presence_audit.json"
FAILED_RERUN_INSTRUCTIONS_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_v0" / "post_repair_rerun_instructions.json"
FAILED_REPAIR_PACKET_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_v0" / "repair_application_decision_packet.json"
FAILED_REPAIR_REPORT_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_v0" / "repair_application_report.json"

REPAIR_ELIGIBILITY_RECEIPT_PATH = ROOT / "data" / "localized_evidence_surface_repair_eligibility_v0_receipts" / f"{SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID}.json"
REPAIR_OBJECTIVE_PROPOSAL_PATH = ROOT / "data" / "localized_evidence_surface_repair_eligibility_v0" / "localized_evidence_surface_repair_objective_proposal.json"
LOCALIZATION_RECEIPT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0_receipts" / f"{SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID}.json"
EVIDENCE_EXTRACTION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0_receipts" / f"{SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID}.json"
FIELD_ROWS_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0" / "taxonomy_gap_missing_label_field_rows.jsonl"
LOOP_APPLICATION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0_receipts" / f"{SOURCE_LOOP_APPLICATION_RECEIPT_ID}.json"
PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID}.json"
TOP_GROUP_CLASSIFICATION_RECEIPT_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0_receipts" / f"{SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID}.json"
R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"
R1000_PRESSURE_EVENTS_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_event_rows.jsonl"
R1000_GROUP_MEMBERSHIP_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_candidate_c_group_event_membership.jsonl"

TRACKED_SOURCE_FILES = [
    REPAIR_ELIGIBILITY_RECEIPT_PATH,
    REPAIR_OBJECTIVE_PROPOSAL_PATH,
    LOCALIZATION_RECEIPT_PATH,
    EVIDENCE_EXTRACTION_RECEIPT_PATH,
    FIELD_ROWS_PATH,
    LOOP_APPLICATION_RECEIPT_PATH,
    PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH,
    TOP_GROUP_CLASSIFICATION_RECEIPT_PATH,
    R1000_SCALE_RECEIPT_PATH,
    R1000_PRESSURE_EVENTS_PATH,
    R1000_GROUP_MEMBERSHIP_PATH,
]

FAILED_REPAIR_FILES = [
    FAILED_REPAIR_RECEIPT_PATH,
    FAILED_REPAIR_PLAN_PATH,
    FAILED_REPAIR_SCHEMA_PATH,
    FAILED_REPAIRED_ROWS_PATH,
    FAILED_REPAIRED_TOP_GROUP_ROWS_PATH,
    FAILED_REPAIR_DIFF_PATH,
    FAILED_POST_REPAIR_AUDIT_PATH,
    FAILED_RERUN_INSTRUCTIONS_PATH,
    FAILED_REPAIR_PACKET_PATH,
    FAILED_REPAIR_REPORT_PATH,
]

HUMAN_DECISION = {
    "decision": "FIX_FAILED_REPAIR_STRUCTURAL_REFS",
    "scope": "repair the failed repaired overlay by joining structural refs from prior field rows",
    "failed_repair_receipt_id": FAILED_REPAIR_RECEIPT_ID,
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
    ],
}

MUST_NOT_INFER = [
    "structural-ref fix repairs the overlay only",
    "do not mutate historical source rows",
    "do not mutate existing receipts",
    "do not guess missing label values",
    "do not emit taxonomy delta",
    "do not upgrade taxonomy",
    "rerun field extraction only after the overlay validates",
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
        "failed_receipt": read_json(FAILED_REPAIR_RECEIPT_PATH),
        "failed_plan": read_json(FAILED_REPAIR_PLAN_PATH),
        "failed_schema": read_json(FAILED_REPAIR_SCHEMA_PATH),
        "failed_repaired_rows": read_jsonl(FAILED_REPAIRED_ROWS_PATH),
        "failed_repaired_top_group_rows": read_jsonl(FAILED_REPAIRED_TOP_GROUP_ROWS_PATH),
        "failed_diff": read_json(FAILED_REPAIR_DIFF_PATH),
        "failed_audit": read_json(FAILED_POST_REPAIR_AUDIT_PATH),
        "failed_rerun": read_json(FAILED_RERUN_INSTRUCTIONS_PATH),
        "failed_packet": read_json(FAILED_REPAIR_PACKET_PATH),
        "failed_report": read_json(FAILED_REPAIR_REPORT_PATH),
        "repair_eligibility_receipt": read_json(REPAIR_ELIGIBILITY_RECEIPT_PATH),
        "repair_objective_proposal": read_json(REPAIR_OBJECTIVE_PROPOSAL_PATH),
        "localization_receipt": read_json(LOCALIZATION_RECEIPT_PATH),
        "evidence_extraction_receipt": read_json(EVIDENCE_EXTRACTION_RECEIPT_PATH),
        "field_rows": read_jsonl(FIELD_ROWS_PATH),
        "pressure_events": read_jsonl(R1000_PRESSURE_EVENTS_PATH),
        "group_membership": read_jsonl(R1000_GROUP_MEMBERSHIP_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    failed = sources["failed_receipt"]
    eligibility = sources["repair_eligibility_receipt"]

    if failed.get("receipt_id") != FAILED_REPAIR_RECEIPT_ID:
        failures.append("failed_receipt_id_wrong")
    if failed.get("gate") != "FAIL":
        failures.append("failed_receipt_not_fail")
    if failed.get("terminal", {}).get("stop_code") != "STOP_GATE_FAIL":
        failures.append("failed_receipt_stop_not_gate_fail")
    if "structural_refs_not_preserved" not in failed.get("failures", []):
        failures.append("failed_receipt_not_structural_ref_failure")
    if failed.get("aggregate_metrics", {}).get("missing_fields_exposed_as_keys") is not True:
        failures.append("failed_repair_did_not_expose_missing_fields")
    if failed.get("aggregate_metrics", {}).get("absence_reasons_emitted") is not True:
        failures.append("failed_repair_did_not_emit_absence_reasons")
    if failed.get("aggregate_metrics", {}).get("structural_refs_preserved") is not False:
        failures.append("failed_repair_structural_refs_not_false")
    if failed.get("aggregate_metrics", {}).get("source_mutation_count") != 0:
        failures.append("failed_repair_mutated_source")

    if eligibility.get("receipt_id") != SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID or eligibility.get("gate") != "PASS":
        failures.append("repair_eligibility_not_pass")
    if eligibility.get("aggregate_metrics", {}).get("repair_objective_id") != SOURCE_REPAIR_OBJECTIVE_ID:
        failures.append("repair_objective_id_wrong")

    if len(sources["failed_repaired_top_group_rows"]) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("failed_top_group_row_count_wrong")
    if len(sources["field_rows"]) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_rows_count_wrong")

    for path in FAILED_REPAIR_FILES:
        if not path.exists():
            failures.append(f"failed_repair_artifact_missing:{rel(path)}")
    for path in TRACKED_SOURCE_FILES:
        if not tracked(path):
            failures.append(f"tracked_source_missing:{rel(path)}")

    return failures

def build_field_row_ref_index(field_rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    index: Dict[str, Dict[str, Any]] = {}
    for row in field_rows:
        pressure_event_id = row.get("pressure_event_id")
        if not pressure_event_id:
            continue
        index[pressure_event_id] = {
            "pressure_event_id": pressure_event_id,
            "pressure_group_key_hash": row.get("pressure_group_key_hash"),
            "parent_pressure_class": row.get("parent_pressure_class"),
            "pressure_subtype": row.get("pressure_subtype"),
            "halt_reason": row.get("halt_reason"),
            "source_receipt_ref": row.get("source_receipt_ref"),
            "source_trace_ref": row.get("source_trace_ref"),
            "work_item_id": row.get("work_item_id"),
            "slot_id": row.get("slot_id"),
            "pressure_pattern_signature_hash": row.get("pressure_pattern_signature_hash"),
        }
    return index

def top_group_ids(sources: Dict[str, Any]) -> set[str]:
    return {
        row["pressure_event_id"]
        for row in sources["group_membership"]
        if row.get("group_key_hash") == TOP_GROUP_KEY_HASH
    }

def fix_rows(sources: Dict[str, Any]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    repaired_rows = sources["failed_repaired_rows"]
    top_ids = top_group_ids(sources)
    ref_index = build_field_row_ref_index(sources["field_rows"])

    fixed_rows: List[Dict[str, Any]] = []
    fixed_top_rows: List[Dict[str, Any]] = []

    join_success = 0
    join_missing = 0
    inserted_counts = {field: 0 for field in STRUCTURAL_FIELDS}
    overwritten_counts = {field: 0 for field in STRUCTURAL_FIELDS}
    field_key_counts = {field: 0 for field in MISSING_FIELDS}
    absence_reason_counts = {field: 0 for field in MISSING_FIELDS}

    for row in repaired_rows:
        new_row = copy.deepcopy(row)
        event_id = new_row.get("pressure_event_id")
        is_top = event_id in top_ids

        if is_top:
            ref = ref_index.get(event_id)
            if ref is None:
                join_missing += 1
            else:
                join_success += 1
                for field in STRUCTURAL_FIELDS:
                    if new_row.get(field) is None and ref.get(field) is not None:
                        new_row[field] = ref[field]
                        inserted_counts[field] += 1
                    elif new_row.get(field) is not None and ref.get(field) is not None and new_row.get(field) != ref.get(field):
                        new_row[f"{field}_pre_structural_ref_fix_value"] = new_row.get(field)
                        new_row[field] = ref[field]
                        overwritten_counts[field] += 1

                for extra in ["work_item_id", "slot_id", "pressure_pattern_signature_hash"]:
                    if new_row.get(extra) is None and ref.get(extra) is not None:
                        new_row[extra] = ref[extra]

            for field in MISSING_FIELDS:
                absence_field = ABSENCE_REASON_FIELDS[field]
                if field not in new_row:
                    new_row[field] = None
                if new_row.get(field) is None and absence_field not in new_row:
                    new_row[absence_field] = "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELD"
                if field in new_row:
                    field_key_counts[field] += 1
                if absence_field in new_row:
                    absence_reason_counts[field] += 1

            new_row["taxonomy_gap_field_surface_structural_refs_fix_applied"] = True
            new_row["taxonomy_gap_field_surface_structural_refs_fix_source_receipt_id"] = FAILED_REPAIR_RECEIPT_ID
            new_row["taxonomy_gap_field_surface_structural_refs_fix_note"] = "Structural refs joined from prior extracted field rows by pressure_event_id."
            fixed_top_rows.append(new_row)
        fixed_rows.append(new_row)

    join_audit = {
        "schema_version": "structural_ref_join_audit_v0",
        "failed_repair_receipt_id": FAILED_REPAIR_RECEIPT_ID,
        "source_field_rows": rel(FIELD_ROWS_PATH),
        "join_key": "pressure_event_id",
        "top_group_row_count": len(fixed_top_rows),
        "expected_top_group_row_count": EXPECTED_FIELD_ROW_COUNT,
        "join_success_count": join_success,
        "join_missing_count": join_missing,
        "inserted_structural_ref_counts": inserted_counts,
        "overwritten_structural_ref_counts": overwritten_counts,
        "field_key_counts_after_fix": field_key_counts,
        "absence_reason_counts_after_fix": absence_reason_counts,
        "review_only": False,
    }

    return fixed_rows, fixed_top_rows, join_audit

def audit_fixed_rows(fixed_top_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    field_presence_profile = {
        field: sum(1 for row in fixed_top_rows if field in row)
        for field in MISSING_FIELDS
    }
    field_non_null_profile = {
        field: sum(1 for row in fixed_top_rows if row.get(field) is not None)
        for field in MISSING_FIELDS
    }
    absence_reason_presence_profile = {
        field: sum(1 for row in fixed_top_rows if ABSENCE_REASON_FIELDS[field] in row)
        for field in MISSING_FIELDS
    }
    structural_profile = {
        field: sum(1 for row in fixed_top_rows if row.get(field) is not None)
        for field in STRUCTURAL_FIELDS
    }
    return {
        "schema_version": "post_structural_refs_fix_field_presence_audit_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "top_group_row_count": len(fixed_top_rows),
        "field_presence_profile": field_presence_profile,
        "field_non_null_profile": field_non_null_profile,
        "absence_reason_presence_profile": absence_reason_presence_profile,
        "structural_field_presence_profile": structural_profile,
        "all_missing_fields_exposed_as_keys": all(count == len(fixed_top_rows) for count in field_presence_profile.values()) if fixed_top_rows else False,
        "all_null_fields_have_absence_reasons": all(count == len(fixed_top_rows) for count in absence_reason_presence_profile.values()) if fixed_top_rows else False,
        "all_structural_refs_preserved": all(count == len(fixed_top_rows) for count in structural_profile.values()) if fixed_top_rows else False,
        "missing_label_values_guessed": any(count > 0 for count in field_non_null_profile.values()),
        "taxonomy_delta_proposed": False,
        "taxonomy_upgrade_authorized": False,
        "review_only": False,
    }

def build_fix_plan() -> Dict[str, Any]:
    return {
        "schema_version": "repair_structural_refs_fix_plan_v0",
        "failed_repair_receipt_id": FAILED_REPAIR_RECEIPT_ID,
        "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "failure_to_fix": "structural_refs_not_preserved",
        "repair_strategy": "join source_receipt_ref and source_trace_ref plus pressure group structural fields from prior extraction field rows by pressure_event_id",
        "input_failed_overlay": rel(FAILED_REPAIRED_ROWS_PATH),
        "input_field_rows": rel(FIELD_ROWS_PATH),
        "output_fixed_overlay": rel(FIXED_REPAIRED_ROWS_PATH),
        "output_fixed_top_group": rel(FIXED_TOP_GROUP_ROWS_PATH),
        "no_taxonomy_repair": True,
        "no_taxonomy_upgrade": True,
        "no_taxonomy_delta": True,
        "no_missing_label_guess": True,
        "no_historical_source_overwrite": True,
        "review_only": False,
    }

def build_diff_summary(fixed_rows: List[Dict[str, Any]], fixed_top_rows: List[Dict[str, Any]], join_audit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "structural_refs_fix_diff_summary_v0",
        "failed_repair_receipt_id": FAILED_REPAIR_RECEIPT_ID,
        "source_failed_overlay": rel(FAILED_REPAIRED_ROWS_PATH),
        "fixed_overlay": rel(FIXED_REPAIRED_ROWS_PATH),
        "failed_overlay_row_count": len(read_jsonl(FAILED_REPAIRED_ROWS_PATH)),
        "fixed_overlay_row_count": len(fixed_rows),
        "fixed_top_group_row_count": len(fixed_top_rows),
        "expected_top_group_row_count": EXPECTED_FIELD_ROW_COUNT,
        "join_success_count": join_audit["join_success_count"],
        "join_missing_count": join_audit["join_missing_count"],
        "inserted_structural_ref_counts": join_audit["inserted_structural_ref_counts"],
        "overwritten_structural_ref_counts": join_audit["overwritten_structural_ref_counts"],
        "historical_source_rows_overwritten": False,
        "existing_receipts_mutated": False,
        "taxonomy_delta_proposed": False,
        "taxonomy_upgrade_authorized": False,
        "missing_label_values_guessed": False,
    }

def build_rerun_instructions(audit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "post_structural_refs_fix_rerun_instructions_v0",
        "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "fixed_repair_surface_artifact": rel(FIXED_REPAIRED_ROWS_PATH),
        "fixed_top_group_repair_surface_artifact": rel(FIXED_TOP_GROUP_ROWS_PATH),
        "rerun_required": True,
        "rerun_sequence": [
            "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_REPAIRED_SURFACE_V0",
            "RERUN_CLASSIFY_TAXONOMY_GAP_EVIDENCE_SURFACE_DEFICIENCY_ON_REPAIRED_SURFACE_V0",
            "RECLASSIFY_R1000_TOP_GROUP_TAXONOMY_GAP_AFTER_REPAIRED_EVIDENCE_SURFACE_V0",
        ],
        "expected_next_observation": {
            "field_keys_present": audit["all_missing_fields_exposed_as_keys"],
            "absence_reasons_present": audit["all_null_fields_have_absence_reasons"],
            "structural_refs_present": audit["all_structural_refs_preserved"],
            "non_null_missing_label_values_expected": False,
            "taxonomy_gap_may_remain_not_enough_evidence": True,
            "reason": "The fixed repair surface exposes keys and structural refs, but intentionally does not invent missing label values.",
        },
        "human_decision_required_before_rerun": False,
        "build_command_emitted": False,
    }

def build_decision_packet(audit: Dict[str, Any]) -> Dict[str, Any]:
    valid = audit["all_missing_fields_exposed_as_keys"] and audit["all_null_fields_have_absence_reasons"] and audit["all_structural_refs_preserved"]
    return {
        "schema_version": "structural_refs_fix_decision_packet_v0",
        "packet_type": "POST_REPAIR_FIX_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "failed_repair_receipt_id": FAILED_REPAIR_RECEIPT_ID,
        "fixed_repair_surface_artifact": rel(FIXED_REPAIRED_ROWS_PATH),
        "fixed_top_group_repair_surface_artifact": rel(FIXED_TOP_GROUP_ROWS_PATH),
        "repair_fix_applied": True,
        "repair_fix_validated": valid,
        "allowed_human_choices": [
            "RERUN_FIELD_EXTRACTION_ON_FIXED_REPAIRED_SURFACE",
            "REJECT_STRUCTURAL_REF_FIX",
            "REQUEST_FIX_ADJUSTMENT",
            "STOP_AND_REVIEW_MANUALLY",
        ],
        "recommended_next_handling": "RERUN_FIELD_EXTRACTION_ON_FIXED_REPAIRED_SURFACE" if valid else "REQUEST_FIX_ADJUSTMENT",
        "recommended_next_unit": "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_REPAIRED_SURFACE_V0" if valid else None,
        "may_emit_taxonomy_delta": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_authority_widening": False,
        "may_authorize_burden_optimization": False,
        "may_auto_open_next_group": False,
        "may_mutate_existing_receipts": False,
        "may_guess_missing_label_values": False,
        "review_only": False,
    }

def build_report(plan: Dict[str, Any], join_audit: Dict[str, Any], diff: Dict[str, Any], audit: Dict[str, Any], rerun: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "repair_structural_refs_fix_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
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
        "fix_plan": plan,
        "structural_ref_join_audit": join_audit,
        "fix_diff_summary": diff,
        "post_fix_audit": audit,
        "rerun_instructions": rerun,
        "decision_packet_recommended_next_handling": packet["recommended_next_handling"],
        "repair_fix_artifact_built": True,
        "repair_fix_executed": True,
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

def validate_outputs(plan: Dict[str, Any], join_audit: Dict[str, Any], diff: Dict[str, Any], audit: Dict[str, Any], rerun: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if plan["failed_repair_receipt_id"] != FAILED_REPAIR_RECEIPT_ID:
        failures.append("plan_failed_receipt_wrong")
    if plan["failure_to_fix"] != "structural_refs_not_preserved":
        failures.append("plan_failure_wrong")
    for key in ["no_taxonomy_repair", "no_taxonomy_upgrade", "no_taxonomy_delta", "no_missing_label_guess", "no_historical_source_overwrite"]:
        if plan.get(key) is not True:
            failures.append(f"plan_guard_not_true:{key}:{plan.get(key)}")

    if join_audit["top_group_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("join_top_group_count_wrong")
    if join_audit["join_success_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("join_success_count_wrong")
    if join_audit["join_missing_count"] != 0:
        failures.append("join_missing_nonzero")

    if diff["fixed_overlay_row_count"] != diff["failed_overlay_row_count"]:
        failures.append("fixed_overlay_row_count_changed")
    if diff["fixed_top_group_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("fixed_top_group_count_wrong")
    for key in ["historical_source_rows_overwritten", "existing_receipts_mutated", "taxonomy_delta_proposed", "taxonomy_upgrade_authorized", "missing_label_values_guessed"]:
        if diff.get(key) is not False:
            failures.append(f"diff_guard_not_false:{key}:{diff.get(key)}")

    if audit["top_group_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("audit_top_group_count_wrong")
    if audit["all_missing_fields_exposed_as_keys"] is not True:
        failures.append("missing_fields_not_exposed")
    if audit["all_null_fields_have_absence_reasons"] is not True:
        failures.append("absence_reasons_missing")
    if audit["all_structural_refs_preserved"] is not True:
        failures.append("structural_refs_not_preserved")
    if audit["missing_label_values_guessed"] is not False:
        failures.append("missing_label_values_guessed")
    if audit["taxonomy_delta_proposed"] is not False:
        failures.append("taxonomy_delta_proposed")
    if audit["taxonomy_upgrade_authorized"] is not False:
        failures.append("taxonomy_upgrade_authorized")

    if rerun["rerun_required"] is not True:
        failures.append("rerun_not_required")
    if rerun["rerun_sequence"][0] != "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_REPAIRED_SURFACE_V0":
        failures.append("rerun_sequence_wrong")
    if rerun["build_command_emitted"] is not False:
        failures.append("rerun_build_command_emitted")

    if packet["packet_type"] != "POST_REPAIR_FIX_REVIEW_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    if packet["repair_fix_applied"] is not True:
        failures.append("packet_fix_not_applied")
    if packet["repair_fix_validated"] is not True:
        failures.append("packet_fix_not_validated")
    if packet["recommended_next_unit"] != "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_REPAIRED_SURFACE_V0":
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
    if report["repair_fix_artifact_built"] is not True:
        failures.append("fix_artifact_not_built")
    if report["repair_fix_executed"] is not True:
        failures.append("fix_not_executed")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("failed_repair_receipt_id") != FAILED_REPAIR_RECEIPT_ID:
        failures.append("failed_receipt_wrong")
    if receipt.get("accepted_repair_objective_id") != SOURCE_REPAIR_OBJECTIVE_ID:
        failures.append("accepted_objective_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "STRUCTURAL_REF_FIX_0_FAILED_REPAIR_CONSUMED",
        "STRUCTURAL_REF_FIX_1_HUMAN_DECISION_RECORDED",
        "STRUCTURAL_REF_FIX_2_FIELD_ROW_REF_INDEX_BUILT",
        "STRUCTURAL_REF_FIX_3_JOIN_SUCCEEDED_FOR_ALL_TOP_ROWS",
        "STRUCTURAL_REF_FIX_4_FIXED_OVERLAY_EMITTED",
        "STRUCTURAL_REF_FIX_5_MISSING_FIELD_KEYS_PRESERVED",
        "STRUCTURAL_REF_FIX_6_ABSENCE_REASONS_PRESERVED",
        "STRUCTURAL_REF_FIX_7_STRUCTURAL_REFS_PRESERVED",
        "STRUCTURAL_REF_FIX_8_NO_TAXONOMY_DELTA_OR_UPGRADE",
        "STRUCTURAL_REF_FIX_9_NO_LABEL_VALUE_GUESSING",
        "STRUCTURAL_REF_FIX_10_NO_HISTORICAL_SOURCE_OVERWRITE",
        "STRUCTURAL_REF_FIX_11_RERUN_PACKET_EMITTED",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("fixed_top_group_row_count") != EXPECTED_FIELD_ROW_COUNT:
        failures.append("metric_fixed_top_count_wrong")
    if metrics.get("join_success_count") != EXPECTED_FIELD_ROW_COUNT:
        failures.append("metric_join_success_wrong")
    if metrics.get("structural_refs_preserved") is not True:
        failures.append("metric_structural_refs_not_preserved")
    for key in ["repair_fix_artifact_built_count", "repair_fix_executed_count"]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")
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

    guards = receipt.get("structural_ref_fix_guards", {})
    for key in [
        "failed_repair_consumed",
        "human_decision_recorded",
        "field_row_ref_index_built",
        "join_succeeded_for_all_top_rows",
        "fixed_overlay_emitted",
        "missing_field_keys_preserved",
        "absence_reasons_preserved",
        "structural_refs_preserved",
        "rerun_packet_emitted",
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
    source_before = snapshot_files(TRACKED_SOURCE_FILES + FAILED_REPAIR_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    plan = build_fix_plan()
    fixed_rows, fixed_top_rows, join_audit = fix_rows(sources)
    audit = audit_fixed_rows(fixed_top_rows)
    diff = build_diff_summary(fixed_rows, fixed_top_rows, join_audit)
    rerun = build_rerun_instructions(audit)
    packet = build_decision_packet(audit)
    report = build_report(plan, join_audit, diff, audit, rerun, packet)

    write_json(FIX_PLAN_PATH, plan)
    write_jsonl(FIXED_REPAIRED_ROWS_PATH, fixed_rows)
    write_jsonl(FIXED_TOP_GROUP_ROWS_PATH, fixed_top_rows)
    write_json(STRUCTURAL_REF_JOIN_AUDIT_PATH, join_audit)
    write_json(FIX_DIFF_SUMMARY_PATH, diff)
    write_json(POST_FIX_FIELD_PRESENCE_AUDIT_PATH, audit)
    write_json(POST_FIX_RERUN_INSTRUCTIONS_PATH, rerun)
    write_json(FIX_DECISION_PACKET_PATH, packet)
    write_json(FIX_REPORT_PATH, report)

    failures.extend(validate_outputs(plan, join_audit, diff, audit, rerun, packet, report))

    source_after = snapshot_files(TRACKED_SOURCE_FILES + FAILED_REPAIR_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "STRUCTURAL_REF_FIX_0_FAILED_REPAIR_CONSUMED": sources["failed_receipt"]["receipt_id"] == FAILED_REPAIR_RECEIPT_ID and sources["failed_receipt"]["gate"] == "FAIL",
        "STRUCTURAL_REF_FIX_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "FIX_FAILED_REPAIR_STRUCTURAL_REFS",
        "STRUCTURAL_REF_FIX_2_FIELD_ROW_REF_INDEX_BUILT": len(build_field_row_ref_index(sources["field_rows"])) == EXPECTED_FIELD_ROW_COUNT,
        "STRUCTURAL_REF_FIX_3_JOIN_SUCCEEDED_FOR_ALL_TOP_ROWS": join_audit["join_success_count"] == EXPECTED_FIELD_ROW_COUNT and join_audit["join_missing_count"] == 0,
        "STRUCTURAL_REF_FIX_4_FIXED_OVERLAY_EMITTED": FIXED_REPAIRED_ROWS_PATH.exists() and FIXED_TOP_GROUP_ROWS_PATH.exists(),
        "STRUCTURAL_REF_FIX_5_MISSING_FIELD_KEYS_PRESERVED": audit["all_missing_fields_exposed_as_keys"] is True,
        "STRUCTURAL_REF_FIX_6_ABSENCE_REASONS_PRESERVED": audit["all_null_fields_have_absence_reasons"] is True,
        "STRUCTURAL_REF_FIX_7_STRUCTURAL_REFS_PRESERVED": audit["all_structural_refs_preserved"] is True,
        "STRUCTURAL_REF_FIX_8_NO_TAXONOMY_DELTA_OR_UPGRADE": report["taxonomy_delta_proposal_emitted"] is False and report["taxonomy_upgrade_authorized"] is False,
        "STRUCTURAL_REF_FIX_9_NO_LABEL_VALUE_GUESSING": report["missing_label_values_guessed"] is False,
        "STRUCTURAL_REF_FIX_10_NO_HISTORICAL_SOURCE_OVERWRITE": report["historical_source_rows_overwritten"] is False and source_mutation_detected is False,
        "STRUCTURAL_REF_FIX_11_RERUN_PACKET_EMITTED": FIX_DECISION_PACKET_PATH.exists(),
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
        "failed_repair_receipt_id": FAILED_REPAIR_RECEIPT_ID,
        "source_repair_eligibility_receipt_id": SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID,
        "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "fixed_repair_surface_artifact": rel(FIXED_REPAIRED_ROWS_PATH),
        "fixed_top_group_repair_surface_artifact": rel(FIXED_TOP_GROUP_ROWS_PATH),
        "fixed_overlay_row_count": diff["fixed_overlay_row_count"],
        "fixed_top_group_row_count": diff["fixed_top_group_row_count"],
        "join_success_count": join_audit["join_success_count"],
        "join_missing_count": join_audit["join_missing_count"],
        "missing_fields_exposed_as_keys": audit["all_missing_fields_exposed_as_keys"],
        "absence_reasons_emitted": audit["all_null_fields_have_absence_reasons"],
        "structural_refs_preserved": audit["all_structural_refs_preserved"],
        "recommended_next_unit": packet["recommended_next_unit"],
        "repair_fix_artifact_built_count": 1,
        "repair_fix_executed_count": 1,
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
        "failed_repair_consumed": True,
        "human_decision_recorded": True,
        "field_row_ref_index_built": len(build_field_row_ref_index(sources["field_rows"])) == EXPECTED_FIELD_ROW_COUNT,
        "join_succeeded_for_all_top_rows": join_audit["join_success_count"] == EXPECTED_FIELD_ROW_COUNT and join_audit["join_missing_count"] == 0,
        "fixed_overlay_emitted": True,
        "missing_field_keys_preserved": audit["all_missing_fields_exposed_as_keys"],
        "absence_reasons_preserved": audit["all_null_fields_have_absence_reasons"],
        "structural_refs_preserved": audit["all_structural_refs_preserved"],
        "rerun_packet_emitted": True,
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
        "failed_repair_receipt": FAILED_REPAIR_RECEIPT_ID,
        "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "fixed_overlay": rel(FIXED_REPAIRED_ROWS_PATH),
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "structural_refs_fix_plan": rel(FIX_PLAN_PATH),
        "fixed_repaired_pressure_event_rows": rel(FIXED_REPAIRED_ROWS_PATH),
        "fixed_repaired_top_group_pressure_event_rows": rel(FIXED_TOP_GROUP_ROWS_PATH),
        "structural_ref_join_audit": rel(STRUCTURAL_REF_JOIN_AUDIT_PATH),
        "structural_refs_fix_diff_summary": rel(FIX_DIFF_SUMMARY_PATH),
        "post_fix_field_presence_audit": rel(POST_FIX_FIELD_PRESENCE_AUDIT_PATH),
        "post_fix_rerun_instructions": rel(POST_FIX_RERUN_INSTRUCTIONS_PATH),
        "structural_refs_fix_decision_packet": rel(FIX_DECISION_PACKET_PATH),
        "structural_refs_fix_report": rel(FIX_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "repair_structural_refs_fix_receipt_v0",
        "receipt_type": "REPAIR_R1000_PRESSURE_EVENT_TAXONOMY_GAP_FIELD_SURFACE_STRUCTURAL_REFS_FIX_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
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
        "fix_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "failed_repair_receipt_id": FAILED_REPAIR_RECEIPT_ID,
            "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
            "fixed_repair_surface_artifact": rel(FIXED_REPAIRED_ROWS_PATH),
            "fixed_top_group_repair_surface_artifact": rel(FIXED_TOP_GROUP_ROWS_PATH),
            "fixed_top_group_row_count": diff["fixed_top_group_row_count"],
            "join_success_count": join_audit["join_success_count"],
            "missing_fields_exposed_as_keys": audit["all_missing_fields_exposed_as_keys"],
            "absence_reasons_emitted": audit["all_null_fields_have_absence_reasons"],
            "structural_refs_preserved": audit["all_structural_refs_preserved"],
            "recommended_next_unit": packet["recommended_next_unit"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "structural_ref_fix_guards": guards,
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
    print(f"repair_structural_refs_fix_receipt_id={receipt_id}")
    print(f"repair_structural_refs_fix_receipt_path=data/repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0_receipts/{receipt_id}.json")
    print(f"fixed_repaired_pressure_event_rows_path=data/repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0/r1000_pressure_event_rows_taxonomy_gap_field_surface_repaired_structural_refs_fixed.jsonl")
    print(f"fixed_repaired_top_group_rows_path=data/repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0/top_group_pressure_event_rows_taxonomy_gap_field_surface_repaired_structural_refs_fixed.jsonl")
    print(f"structural_refs_fix_decision_packet_path=data/repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0/structural_refs_fix_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
