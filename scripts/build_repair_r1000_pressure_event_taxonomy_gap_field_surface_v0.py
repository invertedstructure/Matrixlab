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

UNIT_ID = "BUILD_REPAIR_R1000_PRESSURE_EVENT_TAXONOMY_GAP_FIELD_SURFACE_V0"
TARGET_UNIT_ID = "repair_r1000_pressure_event_taxonomy_gap_field_surface.v0"

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

OUT_DIR = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_v0"
RECEIPT_DIR = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_v0_receipts"

REPAIR_PLAN_PATH = OUT_DIR / "repair_plan.json"
REPAIR_SURFACE_SCHEMA_PATH = OUT_DIR / "repair_surface_schema.json"
REPAIRED_PRESSURE_EVENT_ROWS_PATH = OUT_DIR / "r1000_pressure_event_rows_taxonomy_gap_field_surface_repaired.jsonl"
REPAIRED_TOP_GROUP_ROWS_PATH = OUT_DIR / "top_group_pressure_event_rows_taxonomy_gap_field_surface_repaired.jsonl"
REPAIR_DIFF_SUMMARY_PATH = OUT_DIR / "repair_diff_summary.json"
POST_REPAIR_FIELD_PRESENCE_AUDIT_PATH = OUT_DIR / "post_repair_field_presence_audit.json"
RERUN_INSTRUCTIONS_PATH = OUT_DIR / "post_repair_rerun_instructions.json"
REPAIR_DECISION_PACKET_PATH = OUT_DIR / "repair_application_decision_packet.json"
REPAIR_REPORT_PATH = OUT_DIR / "repair_application_report.json"

REPAIR_ELIGIBILITY_RECEIPT_PATH = ROOT / "data" / "localized_evidence_surface_repair_eligibility_v0_receipts" / f"{SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID}.json"
REPAIR_ELIGIBILITY_INPUT_ROLLUP_PATH = ROOT / "data" / "localized_evidence_surface_repair_eligibility_v0" / "localized_repair_eligibility_input_rollup.json"
REPAIR_ELIGIBILITY_CLASSIFICATION_PATH = ROOT / "data" / "localized_evidence_surface_repair_eligibility_v0" / "localized_repair_eligibility_classification.json"
REPAIR_OBJECTIVE_PROPOSAL_PATH = ROOT / "data" / "localized_evidence_surface_repair_eligibility_v0" / "localized_evidence_surface_repair_objective_proposal.json"
REPAIR_ELIGIBILITY_PACKET_PATH = ROOT / "data" / "localized_evidence_surface_repair_eligibility_v0" / "localized_repair_eligibility_decision_packet.json"
REPAIR_ELIGIBILITY_REPORT_PATH = ROOT / "data" / "localized_evidence_surface_repair_eligibility_v0" / "localized_repair_eligibility_report.json"

LOCALIZATION_RECEIPT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0_receipts" / f"{SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID}.json"
RAW_SOURCE_FIELD_AUDIT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0" / "raw_source_field_audit.json"
EXTRACTOR_LOGIC_AUDIT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0" / "extractor_logic_audit.json"
SCHEMA_SLOT_AUDIT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0" / "schema_slot_audit.json"
SURFACE_LOCALIZATION_CANDIDATES_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0" / "surface_localization_candidates.json"
SURFACE_LOCALIZATION_CLASSIFICATION_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0" / "surface_localization_classification.json"
SURFACE_LOCALIZATION_PACKET_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0" / "surface_localization_decision_packet.json"
SURFACE_LOCALIZATION_REPORT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0" / "surface_localization_audit_report.json"

EVIDENCE_SURFACE_RECEIPT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0_receipts" / f"{SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID}.json"
EVIDENCE_EXTRACTION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0_receipts" / f"{SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID}.json"
FIELD_ROWS_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0" / "taxonomy_gap_missing_label_field_rows.jsonl"
LOOP_APPLICATION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0_receipts" / f"{SOURCE_LOOP_APPLICATION_RECEIPT_ID}.json"
PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID}.json"
TOP_GROUP_CLASSIFICATION_RECEIPT_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0_receipts" / f"{SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID}.json"
R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"
R1000_PRESSURE_EVENTS_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_event_rows.jsonl"
R1000_GROUP_MEMBERSHIP_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_candidate_c_group_event_membership.jsonl"

SOURCE_FILES = [
    REPAIR_ELIGIBILITY_RECEIPT_PATH,
    REPAIR_ELIGIBILITY_INPUT_ROLLUP_PATH,
    REPAIR_ELIGIBILITY_CLASSIFICATION_PATH,
    REPAIR_OBJECTIVE_PROPOSAL_PATH,
    REPAIR_ELIGIBILITY_PACKET_PATH,
    REPAIR_ELIGIBILITY_REPORT_PATH,
    LOCALIZATION_RECEIPT_PATH,
    RAW_SOURCE_FIELD_AUDIT_PATH,
    EXTRACTOR_LOGIC_AUDIT_PATH,
    SCHEMA_SLOT_AUDIT_PATH,
    SURFACE_LOCALIZATION_CANDIDATES_PATH,
    SURFACE_LOCALIZATION_CLASSIFICATION_PATH,
    SURFACE_LOCALIZATION_PACKET_PATH,
    SURFACE_LOCALIZATION_REPORT_PATH,
    EVIDENCE_SURFACE_RECEIPT_PATH,
    EVIDENCE_EXTRACTION_RECEIPT_PATH,
    FIELD_ROWS_PATH,
    LOOP_APPLICATION_RECEIPT_PATH,
    PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH,
    TOP_GROUP_CLASSIFICATION_RECEIPT_PATH,
    R1000_SCALE_RECEIPT_PATH,
    R1000_PRESSURE_EVENTS_PATH,
    R1000_GROUP_MEMBERSHIP_PATH,
]

HUMAN_DECISION = {
    "decision": "ACCEPT_EVIDENCE_SURFACE_REPAIR_OBJECTIVE",
    "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
    "accepted_repair_objective_name": "REPAIR_R1000_PRESSURE_EVENT_TAXONOMY_GAP_FIELD_SURFACE_V0",
    "scope": "build repaired evidence surface artifact and rerun instructions only",
    "source_repair_eligibility_receipt_id": SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID,
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
    "repair builds a repaired evidence surface; it does not decide taxonomy",
    "null-with-reason is allowed when source does not know the field value",
    "do not guess missing label values",
    "do not mutate existing receipts",
    "do not overwrite historical source rows",
    "do not auto-open next group",
    "rerun field extraction after repair before reclassifying taxonomy gap",
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
        "repair_eligibility_receipt": read_json(REPAIR_ELIGIBILITY_RECEIPT_PATH),
        "repair_eligibility_input_rollup": read_json(REPAIR_ELIGIBILITY_INPUT_ROLLUP_PATH),
        "repair_eligibility_classification": read_json(REPAIR_ELIGIBILITY_CLASSIFICATION_PATH),
        "repair_objective_proposal": read_json(REPAIR_OBJECTIVE_PROPOSAL_PATH),
        "repair_eligibility_packet": read_json(REPAIR_ELIGIBILITY_PACKET_PATH),
        "repair_eligibility_report": read_json(REPAIR_ELIGIBILITY_REPORT_PATH),
        "localization_receipt": read_json(LOCALIZATION_RECEIPT_PATH),
        "raw_source_field_audit": read_json(RAW_SOURCE_FIELD_AUDIT_PATH),
        "extractor_logic_audit": read_json(EXTRACTOR_LOGIC_AUDIT_PATH),
        "schema_slot_audit": read_json(SCHEMA_SLOT_AUDIT_PATH),
        "surface_localization_classification": read_json(SURFACE_LOCALIZATION_CLASSIFICATION_PATH),
        "field_rows": read_jsonl(FIELD_ROWS_PATH),
        "pressure_events": read_jsonl(R1000_PRESSURE_EVENTS_PATH),
        "group_membership": read_jsonl(R1000_GROUP_MEMBERSHIP_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    eligibility = sources["repair_eligibility_receipt"]
    proposal = sources["repair_objective_proposal"]
    packet = sources["repair_eligibility_packet"]
    loc = sources["localization_receipt"]

    if eligibility.get("receipt_id") != SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID:
        failures.append("repair_eligibility_receipt_id_wrong")
    if eligibility.get("gate") != "PASS":
        failures.append("repair_eligibility_not_pass")
    if eligibility.get("aggregate_metrics", {}).get("classification") != "ELIGIBLE_EVIDENCE_SURFACE_REPAIR_OBJECTIVE":
        failures.append("repair_not_eligible")
    if eligibility.get("aggregate_metrics", {}).get("proposal_emitted") is not True:
        failures.append("repair_proposal_not_emitted")
    if eligibility.get("aggregate_metrics", {}).get("repair_objective_id") != SOURCE_REPAIR_OBJECTIVE_ID:
        failures.append("repair_objective_id_wrong")

    if proposal.get("proposal_emitted") is not True:
        failures.append("proposal_not_emitted")
    if proposal.get("repair_objective_id") != SOURCE_REPAIR_OBJECTIVE_ID:
        failures.append("proposal_objective_id_wrong")
    if proposal.get("repair_objective_name") != "REPAIR_R1000_PRESSURE_EVENT_TAXONOMY_GAP_FIELD_SURFACE_V0":
        failures.append("proposal_objective_name_wrong")
    if sorted(proposal.get("missing_fields_to_expose", [])) != sorted(MISSING_FIELDS):
        failures.append("proposal_missing_fields_wrong")
    if rel(R1000_PRESSURE_EVENTS_PATH) not in proposal.get("localized_repair_surface_refs", []):
        failures.append("proposal_localized_surface_ref_wrong")

    if packet.get("recommended_next_handling") != "ACCEPT_EVIDENCE_SURFACE_REPAIR_OBJECTIVE":
        failures.append("packet_not_accept_recommendation")
    if packet.get("next_if_accepted") != UNIT_ID:
        failures.append("packet_next_if_accepted_not_this")
    if loc.get("aggregate_metrics", {}).get("selected_localization_class") != "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELDS":
        failures.append("localization_class_wrong")

    if len(sources["field_rows"]) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_rows_length_wrong")
    top_group_ids = {
        row["pressure_event_id"]
        for row in sources["group_membership"]
        if row.get("group_key_hash") == TOP_GROUP_KEY_HASH
    }
    top_events = [row for row in sources["pressure_events"] if row.get("pressure_event_id") in top_group_ids]
    if len(top_events) != EXPECTED_FIELD_ROW_COUNT:
        failures.append(f"top_group_pressure_event_count_wrong:{len(top_events)}")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def top_group_pressure_event_ids(sources: Dict[str, Any]) -> set[str]:
    return {
        row["pressure_event_id"]
        for row in sources["group_membership"]
        if row.get("group_key_hash") == TOP_GROUP_KEY_HASH
    }

def build_repair_plan(sources: Dict[str, Any]) -> Dict[str, Any]:
    proposal = sources["repair_objective_proposal"]
    return {
        "schema_version": "repair_r1000_pressure_event_taxonomy_gap_field_surface_plan_v0",
        "repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "repair_objective_name": "REPAIR_R1000_PRESSURE_EVENT_TAXONOMY_GAP_FIELD_SURFACE_V0",
        "accepted_by_human": True,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "repair_surface": "source_event_payload_surface_overlay",
        "source_surface_artifact": rel(R1000_PRESSURE_EVENTS_PATH),
        "repaired_surface_artifact": rel(REPAIRED_PRESSURE_EVENT_ROWS_PATH),
        "top_group_repaired_surface_artifact": rel(REPAIRED_TOP_GROUP_ROWS_PATH),
        "missing_fields_to_expose": MISSING_FIELDS,
        "absence_reason_fields": ABSENCE_REASON_FIELDS,
        "repair_strategy": "copy pressure event rows into a repaired overlay surface; preserve structural fields; add required evidence keys with explicit null values and absence reasons when source payload has no value",
        "why_overlay_not_overwrite": "historical source rows and receipts are preserved; downstream rerun can consume repaired surface explicitly",
        "no_taxonomy_repair": True,
        "no_taxonomy_upgrade": True,
        "no_taxonomy_delta": True,
        "no_missing_label_guess": True,
        "proposal_source_refs": proposal.get("source_evidence_refs", []),
        "review_only": False,
    }

def build_repair_schema(plan: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_event_taxonomy_gap_field_surface_schema_v0",
        "surface": "pressure_event_row",
        "required_structural_fields": STRUCTURAL_FIELDS,
        "required_taxonomy_gap_evidence_fields": MISSING_FIELDS,
        "required_absence_reason_fields": list(ABSENCE_REASON_FIELDS.values()),
        "field_rules": {
            field: {
                "value_rule": "emit actual value if known by source payload; otherwise emit null",
                "absence_reason_field": ABSENCE_REASON_FIELDS[field],
                "absence_reason_rule": "required when value is null",
            }
            for field in MISSING_FIELDS
        },
        "absence_reason_vocab": [
            "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELD",
            "SOURCE_PAYLOAD_FIELD_UNKNOWN",
            "FIELD_NOT_APPLICABLE_TO_PRESSURE_EVENT",
        ],
        "forbidden": [
            "guess missing label values",
            "derive taxonomy delta",
            "upgrade taxonomy",
            "mutate existing receipts",
        ],
        "review_only": False,
    }

def repair_rows(sources: Dict[str, Any]) -> tuple[List[Dict[str, Any]], List[Dict[str, Any]], Dict[str, Any]]:
    source_rows = sources["pressure_events"]
    top_ids = top_group_pressure_event_ids(sources)

    repaired_rows: List[Dict[str, Any]] = []
    repaired_top_rows: List[Dict[str, Any]] = []
    modified_count = 0
    field_insert_counts = {field: 0 for field in MISSING_FIELDS}
    absence_reason_insert_counts = {field: 0 for field in MISSING_FIELDS}

    for row in source_rows:
        new_row = copy.deepcopy(row)
        row_is_top_group = row.get("pressure_event_id") in top_ids

        if row_is_top_group:
            for field in MISSING_FIELDS:
                absence_field = ABSENCE_REASON_FIELDS[field]
                if field not in new_row:
                    new_row[field] = None
                    field_insert_counts[field] += 1
                    modified_count += 1
                if new_row.get(field) is None:
                    if absence_field not in new_row:
                        new_row[absence_field] = "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELD"
                        absence_reason_insert_counts[field] += 1
                        modified_count += 1
                elif absence_field not in new_row:
                    new_row[absence_field] = None
                    absence_reason_insert_counts[field] += 1
                    modified_count += 1

            new_row["taxonomy_gap_field_surface_repair_applied"] = True
            new_row["taxonomy_gap_field_surface_repair_objective_id"] = SOURCE_REPAIR_OBJECTIVE_ID
            new_row["taxonomy_gap_field_surface_repair_source_receipt_id"] = SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID
            new_row["taxonomy_gap_field_surface_repair_note"] = "Explicit evidence field surface added; values remain null where source payload does not emit them."
            modified_count += 4
            repaired_top_rows.append(new_row)
        else:
            new_row["taxonomy_gap_field_surface_repair_applied"] = False

        repaired_rows.append(new_row)

    diff_summary = {
        "schema_version": "repair_r1000_pressure_event_taxonomy_gap_field_surface_diff_summary_v0",
        "source_surface_artifact": rel(R1000_PRESSURE_EVENTS_PATH),
        "repaired_surface_artifact": rel(REPAIRED_PRESSURE_EVENT_ROWS_PATH),
        "source_row_count": len(source_rows),
        "repaired_row_count": len(repaired_rows),
        "top_group_repaired_row_count": len(repaired_top_rows),
        "expected_top_group_row_count": EXPECTED_FIELD_ROW_COUNT,
        "modified_top_group_row_count": len(repaired_top_rows),
        "field_insert_counts": field_insert_counts,
        "absence_reason_insert_counts": absence_reason_insert_counts,
        "total_insert_operations": modified_count,
        "source_surface_overwritten": False,
        "existing_receipts_mutated": False,
        "taxonomy_delta_proposed": False,
        "taxonomy_upgrade_authorized": False,
        "missing_label_values_guessed": False,
    }
    return repaired_rows, repaired_top_rows, diff_summary

def audit_repair(repaired_top_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    field_presence_profile = {
        field: sum(1 for row in repaired_top_rows if field in row)
        for field in MISSING_FIELDS
    }
    field_non_null_profile = {
        field: sum(1 for row in repaired_top_rows if row.get(field) is not None)
        for field in MISSING_FIELDS
    }
    absence_reason_presence_profile = {
        field: sum(1 for row in repaired_top_rows if ABSENCE_REASON_FIELDS[field] in row)
        for field in MISSING_FIELDS
    }
    structural_profile = {
        field: sum(1 for row in repaired_top_rows if row.get(field) is not None)
        for field in STRUCTURAL_FIELDS
    }
    return {
        "schema_version": "post_repair_field_presence_audit_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "top_group_row_count": len(repaired_top_rows),
        "field_presence_profile": field_presence_profile,
        "field_non_null_profile": field_non_null_profile,
        "absence_reason_presence_profile": absence_reason_presence_profile,
        "structural_field_presence_profile": structural_profile,
        "all_missing_fields_exposed_as_keys": all(count == len(repaired_top_rows) for count in field_presence_profile.values()) if repaired_top_rows else False,
        "all_null_fields_have_absence_reasons": all(count == len(repaired_top_rows) for count in absence_reason_presence_profile.values()) if repaired_top_rows else False,
        "all_structural_refs_preserved": all(count == len(repaired_top_rows) for count in structural_profile.values()) if repaired_top_rows else False,
        "missing_label_values_guessed": any(count > 0 for count in field_non_null_profile.values()),
        "taxonomy_delta_proposed": False,
        "taxonomy_upgrade_authorized": False,
        "review_only": False,
    }

def build_rerun_instructions(plan: Dict[str, Any], audit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "post_repair_rerun_instructions_v0",
        "repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "repair_surface_artifact": rel(REPAIRED_PRESSURE_EVENT_ROWS_PATH),
        "top_group_repair_surface_artifact": rel(REPAIRED_TOP_GROUP_ROWS_PATH),
        "rerun_required": True,
        "rerun_sequence": [
            "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_REPAIRED_SURFACE_V0",
            "RERUN_CLASSIFY_TAXONOMY_GAP_EVIDENCE_SURFACE_DEFICIENCY_ON_REPAIRED_SURFACE_V0",
            "RECLASSIFY_R1000_TOP_GROUP_TAXONOMY_GAP_AFTER_REPAIRED_EVIDENCE_SURFACE_V0",
        ],
        "expected_next_observation": {
            "field_keys_present": audit["all_missing_fields_exposed_as_keys"],
            "absence_reasons_present": audit["all_null_fields_have_absence_reasons"],
            "non_null_missing_label_values_expected": False,
            "taxonomy_gap_may_remain_not_enough_evidence": True,
            "reason": "Repair exposes the evidence surface. It does not invent missing label values, so later classification may become healthy expected limit or still require source-level label provenance.",
        },
        "human_decision_required_before_rerun": False,
        "build_command_emitted": False,
    }

def build_decision_packet(audit: Dict[str, Any], rerun: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "repair_application_decision_packet_v0",
        "packet_type": "POST_REPAIR_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "repair_surface_artifact": rel(REPAIRED_PRESSURE_EVENT_ROWS_PATH),
        "top_group_repair_surface_artifact": rel(REPAIRED_TOP_GROUP_ROWS_PATH),
        "repair_applied": True,
        "repair_validated": audit["all_missing_fields_exposed_as_keys"] and audit["all_null_fields_have_absence_reasons"] and audit["all_structural_refs_preserved"],
        "allowed_human_choices": [
            "RERUN_FIELD_EXTRACTION_ON_REPAIRED_SURFACE",
            "REJECT_REPAIR_ARTIFACT",
            "REQUEST_REPAIR_ADJUSTMENT",
            "MARK_SOURCE_LIMIT_HEALTHY_AFTER_REPAIR",
            "STOP_AND_REVIEW_MANUALLY",
        ],
        "recommended_next_handling": "RERUN_FIELD_EXTRACTION_ON_REPAIRED_SURFACE",
        "recommended_next_unit": "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_REPAIRED_SURFACE_V0",
        "may_emit_taxonomy_delta": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_authority_widening": False,
        "may_authorize_burden_optimization": False,
        "may_auto_open_next_group": False,
        "may_mutate_existing_receipts": False,
        "may_guess_missing_label_values": False,
        "review_only": False,
    }

def build_report(plan: Dict[str, Any], schema: Dict[str, Any], diff: Dict[str, Any], audit: Dict[str, Any], rerun: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "repair_r1000_pressure_event_taxonomy_gap_field_surface_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_repair_eligibility_receipt_id": SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID,
            "source_localization_audit_receipt_id": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
            "source_evidence_surface_classification_receipt_id": SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID,
            "source_taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
            "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
            "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
            "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
            "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        },
        "repair_plan_summary": plan,
        "repair_schema_summary": schema,
        "repair_diff_summary": diff,
        "post_repair_audit": audit,
        "rerun_instructions": rerun,
        "decision_packet_recommended_next_handling": packet["recommended_next_handling"],
        "repair_artifact_built": True,
        "repair_executed": True,
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

def validate_outputs(plan: Dict[str, Any], schema: Dict[str, Any], diff: Dict[str, Any], audit: Dict[str, Any], rerun: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if plan["accepted_by_human"] is not True:
        failures.append("repair_not_human_accepted")
    if plan["repair_objective_id"] != SOURCE_REPAIR_OBJECTIVE_ID:
        failures.append("repair_objective_id_wrong")
    if sorted(plan["missing_fields_to_expose"]) != sorted(MISSING_FIELDS):
        failures.append("plan_missing_fields_wrong")
    for key in ["no_taxonomy_repair", "no_taxonomy_upgrade", "no_taxonomy_delta", "no_missing_label_guess"]:
        if plan.get(key) is not True:
            failures.append(f"plan_guard_not_true:{key}:{plan.get(key)}")

    if sorted(schema["required_taxonomy_gap_evidence_fields"]) != sorted(MISSING_FIELDS):
        failures.append("schema_missing_fields_wrong")
    for field in MISSING_FIELDS:
        if field not in schema["field_rules"]:
            failures.append(f"schema_field_rule_missing:{field}")
        if ABSENCE_REASON_FIELDS[field] not in schema["required_absence_reason_fields"]:
            failures.append(f"schema_absence_reason_missing:{field}")

    if diff["source_row_count"] != diff["repaired_row_count"]:
        failures.append("repaired_row_count_changed")
    if diff["top_group_repaired_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("top_group_repaired_row_count_wrong")
    if diff["source_surface_overwritten"] is not False:
        failures.append("source_surface_overwritten")
    if diff["existing_receipts_mutated"] is not False:
        failures.append("existing_receipts_mutated")
    if diff["taxonomy_delta_proposed"] is not False:
        failures.append("taxonomy_delta_proposed")
    if diff["taxonomy_upgrade_authorized"] is not False:
        failures.append("taxonomy_upgrade_authorized")
    if diff["missing_label_values_guessed"] is not False:
        failures.append("missing_label_values_guessed")

    if audit["top_group_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("audit_top_group_row_count_wrong")
    if audit["all_missing_fields_exposed_as_keys"] is not True:
        failures.append("missing_fields_not_exposed")
    if audit["all_null_fields_have_absence_reasons"] is not True:
        failures.append("absence_reasons_missing")
    if audit["all_structural_refs_preserved"] is not True:
        failures.append("structural_refs_not_preserved")
    if audit["missing_label_values_guessed"] is not False:
        failures.append("audit_missing_label_values_guessed")
    if audit["taxonomy_delta_proposed"] is not False:
        failures.append("audit_taxonomy_delta_proposed")
    if audit["taxonomy_upgrade_authorized"] is not False:
        failures.append("audit_taxonomy_upgrade_authorized")

    if rerun["rerun_required"] is not True:
        failures.append("rerun_not_required")
    if rerun["rerun_sequence"][0] != "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_REPAIRED_SURFACE_V0":
        failures.append("rerun_sequence_wrong")
    if rerun["build_command_emitted"] is not False:
        failures.append("rerun_build_command_emitted")

    if packet["packet_type"] != "POST_REPAIR_REVIEW_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    if packet["repair_applied"] is not True:
        failures.append("packet_repair_not_applied")
    if packet["repair_validated"] is not True:
        failures.append("packet_repair_not_validated")
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
    if report["repair_artifact_built"] is not True:
        failures.append("repair_artifact_not_built")
    if report["repair_executed"] is not True:
        failures.append("repair_not_executed")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_repair_eligibility_receipt_id") != SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID:
        failures.append("source_repair_eligibility_wrong")
    if receipt.get("accepted_repair_objective_id") != SOURCE_REPAIR_OBJECTIVE_ID:
        failures.append("accepted_objective_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "REPAIR_FIELD_SURFACE_0_SOURCE_SURFACE_VERIFIED",
        "REPAIR_FIELD_SURFACE_1_HUMAN_ACCEPTANCE_RECORDED",
        "REPAIR_FIELD_SURFACE_2_REPAIR_PLAN_EMITTED",
        "REPAIR_FIELD_SURFACE_3_REPAIRED_SURFACE_EMITTED",
        "REPAIR_FIELD_SURFACE_4_MISSING_FIELD_KEYS_EXPOSED",
        "REPAIR_FIELD_SURFACE_5_ABSENCE_REASONS_EMITTED",
        "REPAIR_FIELD_SURFACE_6_STRUCTURAL_REFS_PRESERVED",
        "REPAIR_FIELD_SURFACE_7_NO_TAXONOMY_DELTA_OR_UPGRADE",
        "REPAIR_FIELD_SURFACE_8_NO_LABEL_VALUE_GUESSING",
        "REPAIR_FIELD_SURFACE_9_NO_HISTORICAL_SOURCE_OVERWRITE",
        "REPAIR_FIELD_SURFACE_10_RERUN_PACKET_EMITTED",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("repair_objective_id") != SOURCE_REPAIR_OBJECTIVE_ID:
        failures.append("metric_objective_wrong")
    if metrics.get("top_group_repaired_row_count") != EXPECTED_FIELD_ROW_COUNT:
        failures.append("metric_top_group_count_wrong")
    for key in [
        "repair_artifact_built_count",
        "repair_executed_count",
    ]:
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
        "missing_label_value_guess_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("repair_field_surface_guards", {})
    for key in [
        "source_surface_verified",
        "human_acceptance_recorded",
        "repair_plan_emitted",
        "repaired_surface_emitted",
        "missing_field_keys_exposed",
        "absence_reasons_emitted",
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

    plan = build_repair_plan(sources)
    schema = build_repair_schema(plan)
    repaired_rows, repaired_top_rows, diff = repair_rows(sources)
    audit = audit_repair(repaired_top_rows)
    rerun = build_rerun_instructions(plan, audit)
    packet = build_decision_packet(audit, rerun)
    report = build_report(plan, schema, diff, audit, rerun, packet)

    write_json(REPAIR_PLAN_PATH, plan)
    write_json(REPAIR_SURFACE_SCHEMA_PATH, schema)
    write_jsonl(REPAIRED_PRESSURE_EVENT_ROWS_PATH, repaired_rows)
    write_jsonl(REPAIRED_TOP_GROUP_ROWS_PATH, repaired_top_rows)
    write_json(REPAIR_DIFF_SUMMARY_PATH, diff)
    write_json(POST_REPAIR_FIELD_PRESENCE_AUDIT_PATH, audit)
    write_json(RERUN_INSTRUCTIONS_PATH, rerun)
    write_json(REPAIR_DECISION_PACKET_PATH, packet)
    write_json(REPAIR_REPORT_PATH, report)

    failures.extend(validate_outputs(plan, schema, diff, audit, rerun, packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "REPAIR_FIELD_SURFACE_0_SOURCE_SURFACE_VERIFIED": len(validate_sources(sources)) == 0,
        "REPAIR_FIELD_SURFACE_1_HUMAN_ACCEPTANCE_RECORDED": HUMAN_DECISION["decision"] == "ACCEPT_EVIDENCE_SURFACE_REPAIR_OBJECTIVE",
        "REPAIR_FIELD_SURFACE_2_REPAIR_PLAN_EMITTED": REPAIR_PLAN_PATH.exists(),
        "REPAIR_FIELD_SURFACE_3_REPAIRED_SURFACE_EMITTED": REPAIRED_PRESSURE_EVENT_ROWS_PATH.exists() and REPAIRED_TOP_GROUP_ROWS_PATH.exists(),
        "REPAIR_FIELD_SURFACE_4_MISSING_FIELD_KEYS_EXPOSED": audit["all_missing_fields_exposed_as_keys"] is True,
        "REPAIR_FIELD_SURFACE_5_ABSENCE_REASONS_EMITTED": audit["all_null_fields_have_absence_reasons"] is True,
        "REPAIR_FIELD_SURFACE_6_STRUCTURAL_REFS_PRESERVED": audit["all_structural_refs_preserved"] is True,
        "REPAIR_FIELD_SURFACE_7_NO_TAXONOMY_DELTA_OR_UPGRADE": report["taxonomy_delta_proposal_emitted"] is False and report["taxonomy_upgrade_authorized"] is False,
        "REPAIR_FIELD_SURFACE_8_NO_LABEL_VALUE_GUESSING": report["missing_label_values_guessed"] is False,
        "REPAIR_FIELD_SURFACE_9_NO_HISTORICAL_SOURCE_OVERWRITE": report["historical_source_rows_overwritten"] is False and source_mutation_detected is False,
        "REPAIR_FIELD_SURFACE_10_RERUN_PACKET_EMITTED": REPAIR_DECISION_PACKET_PATH.exists(),
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
        "source_repair_eligibility_receipt_id": SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID,
        "source_localization_audit_receipt_id": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
        "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "repair_surface_artifact": rel(REPAIRED_PRESSURE_EVENT_ROWS_PATH),
        "top_group_repair_surface_artifact": rel(REPAIRED_TOP_GROUP_ROWS_PATH),
        "source_row_count": diff["source_row_count"],
        "repaired_row_count": diff["repaired_row_count"],
        "top_group_repaired_row_count": diff["top_group_repaired_row_count"],
        "missing_fields_exposed_as_keys": audit["all_missing_fields_exposed_as_keys"],
        "absence_reasons_emitted": audit["all_null_fields_have_absence_reasons"],
        "structural_refs_preserved": audit["all_structural_refs_preserved"],
        "recommended_next_unit": packet["recommended_next_unit"],
        "repair_artifact_built_count": 1,
        "repair_executed_count": 1,
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
        "source_surface_verified": len(validate_sources(sources)) == 0,
        "human_acceptance_recorded": True,
        "repair_plan_emitted": True,
        "repaired_surface_emitted": True,
        "missing_field_keys_exposed": audit["all_missing_fields_exposed_as_keys"],
        "absence_reasons_emitted": audit["all_null_fields_have_absence_reasons"],
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
        "source_repair_eligibility_receipt": SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID,
        "repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "repair_surface": rel(REPAIRED_PRESSURE_EVENT_ROWS_PATH),
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "repair_plan": rel(REPAIR_PLAN_PATH),
        "repair_surface_schema": rel(REPAIR_SURFACE_SCHEMA_PATH),
        "repaired_pressure_event_rows": rel(REPAIRED_PRESSURE_EVENT_ROWS_PATH),
        "repaired_top_group_pressure_event_rows": rel(REPAIRED_TOP_GROUP_ROWS_PATH),
        "repair_diff_summary": rel(REPAIR_DIFF_SUMMARY_PATH),
        "post_repair_field_presence_audit": rel(POST_REPAIR_FIELD_PRESENCE_AUDIT_PATH),
        "post_repair_rerun_instructions": rel(RERUN_INSTRUCTIONS_PATH),
        "repair_application_decision_packet": rel(REPAIR_DECISION_PACKET_PATH),
        "repair_application_report": rel(REPAIR_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "repair_r1000_pressure_event_taxonomy_gap_field_surface_receipt_v0",
        "receipt_type": "REPAIR_R1000_PRESSURE_EVENT_TAXONOMY_GAP_FIELD_SURFACE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
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
        "repair_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
            "repair_surface_artifact": rel(REPAIRED_PRESSURE_EVENT_ROWS_PATH),
            "top_group_repair_surface_artifact": rel(REPAIRED_TOP_GROUP_ROWS_PATH),
            "top_group_repaired_row_count": diff["top_group_repaired_row_count"],
            "missing_fields_exposed_as_keys": audit["all_missing_fields_exposed_as_keys"],
            "absence_reasons_emitted": audit["all_null_fields_have_absence_reasons"],
            "structural_refs_preserved": audit["all_structural_refs_preserved"],
            "recommended_next_unit": packet["recommended_next_unit"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "repair_field_surface_guards": guards,
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
    print(f"repair_r1000_pressure_event_taxonomy_gap_field_surface_receipt_id={receipt_id}")
    print(f"repair_r1000_pressure_event_taxonomy_gap_field_surface_receipt_path=data/repair_r1000_pressure_event_taxonomy_gap_field_surface_v0_receipts/{receipt_id}.json")
    print(f"repaired_pressure_event_rows_path=data/repair_r1000_pressure_event_taxonomy_gap_field_surface_v0/r1000_pressure_event_rows_taxonomy_gap_field_surface_repaired.jsonl")
    print(f"repaired_top_group_rows_path=data/repair_r1000_pressure_event_taxonomy_gap_field_surface_v0/top_group_pressure_event_rows_taxonomy_gap_field_surface_repaired.jsonl")
    print(f"repair_application_decision_packet_path=data/repair_r1000_pressure_event_taxonomy_gap_field_surface_v0/repair_application_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
