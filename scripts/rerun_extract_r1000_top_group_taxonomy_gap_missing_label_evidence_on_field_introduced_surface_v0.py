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

UNIT_ID = "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_FIELD_INTRODUCED_SURFACE_V0"
TARGET_UNIT_ID = "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun.v0"

SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID = "2d9417fc"
SOURCE_PROPOSAL_TYPING_RECEIPT_ID = "5b841942"
SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID = "9ea8fc6e"
SOURCE_NULL_LIMIT_RECEIPT_ID = "9e2c2881"
SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID = "b554aace"
FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID = "b113463f"
SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID = "d6d40d57"

TOP_GROUP_KEY_HASH = "38c604a1"
EXPECTED_ROW_COUNT = 25

INTRODUCED_FIELDS = [
    "missing_label_identifier",
    "taxonomy_context_ref",
    "current_label_space_ref",
    "expected_label_space_ref",
]

FIELD_VALUE_STATUS_FIELDS = {
    "missing_label_identifier": "missing_label_identifier_value_status",
    "taxonomy_context_ref": "taxonomy_context_ref_value_status",
    "current_label_space_ref": "current_label_space_ref_value_status",
    "expected_label_space_ref": "expected_label_space_ref_value_status",
}

ABSENCE_REASON_FIELDS = {
    "missing_label_identifier": "missing_label_identifier_absence_reason",
    "taxonomy_context_ref": "taxonomy_context_ref_absence_reason",
    "current_label_space_ref": "current_label_space_ref_absence_reason",
    "expected_label_space_ref": "expected_label_space_ref_absence_reason",
}

PROVENANCE_FIELDS = {
    "missing_label_identifier": "missing_label_identifier_provenance_ref",
    "taxonomy_context_ref": "taxonomy_context_ref_provenance_ref",
    "current_label_space_ref": "current_label_space_ref_provenance_ref",
    "expected_label_space_ref": "expected_label_space_ref_provenance_ref",
}

OUT_DIR = ROOT / "data" / "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0"
RECEIPT_DIR = ROOT / "data" / "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0_receipts"

FIELD_ROW_OUTPUT_PATH = OUT_DIR / "field_introduced_surface_taxonomy_gap_missing_label_field_rows.jsonl"
OBSERVATION_SUMMARY_PATH = OUT_DIR / "field_introduced_surface_observation_summary.json"
EXTRACTION_AUDIT_PATH = OUT_DIR / "field_introduced_surface_extraction_audit.json"
CLASSIFICATION_PACKET_PATH = OUT_DIR / "field_introduced_surface_classification_packet.json"
RERUN_REPORT_PATH = OUT_DIR / "field_introduced_surface_rerun_report.json"

BUILD_RECEIPT_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0_receipts" / f"{SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID}.json"
BUILD_PLAN_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "source_provenance_field_introduction_build_plan.json"
SCHEMA_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "taxonomy_gap_source_payload_field_introduction_schema_v0.json"
CONTRACT_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "taxonomy_gap_detector_field_emission_contract_v0.json"
R1000_OVERLAY_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "r1000_taxonomy_gap_source_payload_field_introduction_overlay.jsonl"
TOP_GROUP_OVERLAY_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "top_group_taxonomy_gap_source_payload_field_introduction_overlay.jsonl"
BUILD_AUDIT_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "field_introduction_application_audit.json"
RERUN_INSTRUCTIONS_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "post_field_introduction_rerun_instructions.json"
BUILD_DECISION_PACKET_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "field_introduction_build_decision_packet.json"
BUILD_REPORT_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "field_introduction_build_report.json"

PROPOSAL_TYPING_RECEIPT_PATH = ROOT / "data" / "field_introduction_proposal_typing_refinement_v0_receipts" / f"{SOURCE_PROPOSAL_TYPING_RECEIPT_ID}.json"
BOUNDARY_RECEIPT_PATH = ROOT / "data" / "null_evidence_field_introduction_boundary_refinement_v0_receipts" / f"{SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID}.json"
NULL_LIMIT_RECEIPT_PATH = ROOT / "data" / "repaired_surface_null_evidence_limit_classification_v0_receipts" / f"{SOURCE_NULL_LIMIT_RECEIPT_ID}.json"
COMPARISON_GATE_FIX_RECEIPT_PATH = ROOT / "data" / "repaired_surface_rerun_comparison_gate_fix_v0_receipts" / f"{SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID}.json"
FAILED_RERUN_RECEIPT_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0_receipts" / f"{FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID}.json"
FAILED_RERUN_FIELD_ROWS_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_taxonomy_gap_missing_label_field_rows.jsonl"
STRUCTURAL_REF_FIX_RECEIPT_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0_receipts" / f"{SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID}.json"

SOURCE_FILES = [
    BUILD_RECEIPT_PATH,
    BUILD_PLAN_PATH,
    SCHEMA_PATH,
    CONTRACT_PATH,
    R1000_OVERLAY_PATH,
    TOP_GROUP_OVERLAY_PATH,
    BUILD_AUDIT_PATH,
    RERUN_INSTRUCTIONS_PATH,
    BUILD_DECISION_PACKET_PATH,
    BUILD_REPORT_PATH,
    PROPOSAL_TYPING_RECEIPT_PATH,
    BOUNDARY_RECEIPT_PATH,
    NULL_LIMIT_RECEIPT_PATH,
    COMPARISON_GATE_FIX_RECEIPT_PATH,
    FAILED_RERUN_RECEIPT_PATH,
    FAILED_RERUN_FIELD_ROWS_PATH,
    STRUCTURAL_REF_FIX_RECEIPT_PATH,
]

HUMAN_DECISION = {
    "decision": "RERUN_FIELD_EXTRACTION_ON_FIELD_INTRODUCED_SURFACE",
    "scope": "extract taxonomy-gap missing-label evidence from the versioned field-introduced overlay without inventing values or mutating source artifacts",
    "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
    "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
    "authorized": [
        "read field-introduced source overlay",
        "emit rerun field rows",
        "emit observation summary",
        "emit classification packet",
    ],
    "not_authorized": [
        "inventing missing label values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "mutating historical source rows",
        "mutating existing receipts",
        "changing source semantics",
        "source-provenance repair execution",
        "authority widening",
        "burden optimization",
        "protocol adoption",
        "next group auto-open",
        "hidden next command",
    ],
}

MUST_NOT_INFER = [
    "field keys being present does not mean values are present",
    "null introduced values must remain null unless source evidence supplies a value",
    "absence reason plus provenance is evidence surface, not taxonomy repair",
    "rerun may classify the surface as structurally repaired while content remains absent",
    "do not invent missing label values",
    "do not emit taxonomy delta",
    "do not mutate historical source rows",
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
        "build_receipt": read_json(BUILD_RECEIPT_PATH),
        "build_plan": read_json(BUILD_PLAN_PATH),
        "schema": read_json(SCHEMA_PATH),
        "contract": read_json(CONTRACT_PATH),
        "r1000_overlay_rows": read_jsonl(R1000_OVERLAY_PATH),
        "top_group_overlay_rows": read_jsonl(TOP_GROUP_OVERLAY_PATH),
        "build_audit": read_json(BUILD_AUDIT_PATH),
        "rerun_instructions": read_json(RERUN_INSTRUCTIONS_PATH),
        "build_decision_packet": read_json(BUILD_DECISION_PACKET_PATH),
        "build_report": read_json(BUILD_REPORT_PATH),
        "proposal_typing_receipt": read_json(PROPOSAL_TYPING_RECEIPT_PATH),
        "boundary_receipt": read_json(BOUNDARY_RECEIPT_PATH),
        "null_limit_receipt": read_json(NULL_LIMIT_RECEIPT_PATH),
        "comparison_gate_fix_receipt": read_json(COMPARISON_GATE_FIX_RECEIPT_PATH),
        "failed_rerun_receipt": read_json(FAILED_RERUN_RECEIPT_PATH),
        "failed_rerun_field_rows": read_jsonl(FAILED_RERUN_FIELD_ROWS_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    build_receipt = sources["build_receipt"]
    metrics = build_receipt.get("aggregate_metrics", {})
    rerun_instructions = sources["rerun_instructions"]
    packet = sources["build_decision_packet"]

    if build_receipt.get("receipt_id") != SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID:
        failures.append("build_receipt_id_wrong")
    if build_receipt.get("gate") != "PASS":
        failures.append("build_not_pass")
    if metrics.get("introduced_field_count") != len(INTRODUCED_FIELDS):
        failures.append("introduced_field_count_wrong")
    if metrics.get("introduced_overlay_row_count") != EXPECTED_ROW_COUNT:
        failures.append("introduced_overlay_row_count_wrong")
    if metrics.get("no_introduced_values_invented") is not True:
        failures.append("values_invented_in_build")
    if metrics.get("all_absence_reasons_present") is not True:
        failures.append("build_absence_reasons_missing")
    if metrics.get("all_provenance_refs_present") is not True:
        failures.append("build_provenance_refs_missing")
    if metrics.get("source_mutation_count") != 0:
        failures.append("build_source_mutated")
    if metrics.get("taxonomy_delta_proposal_emitted_count") != 0:
        failures.append("build_taxonomy_delta_emitted")
    if metrics.get("taxonomy_upgrade_authorized_count") != 0:
        failures.append("build_taxonomy_upgrade_authorized")
    if rerun_instructions.get("recommended_next_unit") != UNIT_ID:
        failures.append("rerun_instruction_next_unit_wrong")
    if rerun_instructions.get("next_unit_command_emitted") is not False:
        failures.append("rerun_instruction_already_emitted_command")
    if packet.get("recommended_next_unit") != UNIT_ID:
        failures.append("build_packet_next_unit_wrong")
    if packet.get("may_emit_next_command") is not False:
        failures.append("build_packet_may_emit_next_command")
    if len(sources["top_group_overlay_rows"]) != EXPECTED_ROW_COUNT:
        failures.append("top_group_overlay_row_count_wrong")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def extract_field_rows(sources: Dict[str, Any]) -> List[Dict[str, Any]]:
    rows = []
    schema_id = sources["schema"]["schema_id"]
    contract_id = sources["contract"]["contract_id"]

    for index, row in enumerate(sources["top_group_overlay_rows"]):
        extracted = {
            "rerun_row_index": index,
            "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
            "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
            "field_introduction_schema_id": row.get("field_introduction_schema_id"),
            "expected_schema_id": schema_id,
            "contract_id": contract_id,
            "field_introduction_applied": row.get("field_introduction_applied"),
            "field_introduction_versioned_overlay": row.get("field_introduction_versioned_overlay"),
            "field_introduction_historical_source_overwrite": row.get("field_introduction_historical_source_overwrite"),
        }

        for field in INTRODUCED_FIELDS:
            extracted[field] = row.get(field)
            extracted[FIELD_VALUE_STATUS_FIELDS[field]] = row.get(FIELD_VALUE_STATUS_FIELDS[field])
            extracted[ABSENCE_REASON_FIELDS[field]] = row.get(ABSENCE_REASON_FIELDS[field])
            extracted[PROVENANCE_FIELDS[field]] = row.get(PROVENANCE_FIELDS[field])
            extracted[f"{field}_key_visible"] = field in row
            extracted[f"{FIELD_VALUE_STATUS_FIELDS[field]}_key_visible"] = FIELD_VALUE_STATUS_FIELDS[field] in row
            extracted[f"{ABSENCE_REASON_FIELDS[field]}_key_visible"] = ABSENCE_REASON_FIELDS[field] in row
            extracted[f"{PROVENANCE_FIELDS[field]}_key_visible"] = PROVENANCE_FIELDS[field] in row
            extracted[f"{field}_value_present"] = row.get(field) is not None

        rows.append(extracted)
    return rows

def summarize_rows(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    field_key_visible_counts = {}
    status_key_visible_counts = {}
    absence_reason_key_visible_counts = {}
    provenance_key_visible_counts = {}
    value_present_counts = {}
    status_counts = {}
    absence_reason_counts = {}
    provenance_present_counts = {}

    for field in INTRODUCED_FIELDS:
        field_key_visible_counts[field] = sum(1 for row in rows if row.get(f"{field}_key_visible") is True)
        status_key_visible_counts[field] = sum(1 for row in rows if row.get(f"{FIELD_VALUE_STATUS_FIELDS[field]}_key_visible") is True)
        absence_reason_key_visible_counts[field] = sum(1 for row in rows if row.get(f"{ABSENCE_REASON_FIELDS[field]}_key_visible") is True)
        provenance_key_visible_counts[field] = sum(1 for row in rows if row.get(f"{PROVENANCE_FIELDS[field]}_key_visible") is True)
        value_present_counts[field] = sum(1 for row in rows if row.get(f"{field}_value_present") is True)
        status_counts[field] = dict(Counter(row.get(FIELD_VALUE_STATUS_FIELDS[field]) for row in rows))
        absence_reason_counts[field] = dict(Counter(row.get(ABSENCE_REASON_FIELDS[field]) for row in rows))
        provenance_present_counts[field] = sum(1 for row in rows if row.get(PROVENANCE_FIELDS[field]) is not None)

    total_values_present = sum(value_present_counts.values())

    return {
        "schema_version": "field_introduced_surface_observation_summary_v0",
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "row_count": len(rows),
        "introduced_field_count": len(INTRODUCED_FIELDS),
        "introduced_field_names": INTRODUCED_FIELDS,
        "field_key_visible_counts": field_key_visible_counts,
        "status_key_visible_counts": status_key_visible_counts,
        "absence_reason_key_visible_counts": absence_reason_key_visible_counts,
        "provenance_key_visible_counts": provenance_key_visible_counts,
        "value_present_counts": value_present_counts,
        "total_values_present": total_values_present,
        "status_counts": status_counts,
        "absence_reason_counts": absence_reason_counts,
        "provenance_present_counts": provenance_present_counts,
        "all_field_keys_visible": all(count == len(rows) for count in field_key_visible_counts.values()),
        "all_status_keys_visible": all(count == len(rows) for count in status_key_visible_counts.values()),
        "all_absence_reason_keys_visible": all(count == len(rows) for count in absence_reason_key_visible_counts.values()),
        "all_provenance_keys_visible": all(count == len(rows) for count in provenance_key_visible_counts.values()),
        "all_provenance_refs_present": all(count == len(rows) for count in provenance_present_counts.values()),
        "any_values_present": total_values_present > 0,
        "all_values_absent": total_values_present == 0,
        "expected_null_status_only": all(
            set(counts.keys()) == {"VALUE_ABSENT_SOURCE_PAYLOAD_DOES_NOT_EMIT"}
            for counts in status_counts.values()
        ),
        "expected_absence_reason_only": all(
            set(counts.keys()) == {"SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELD"}
            for counts in absence_reason_counts.values()
        ),
        "field_introduced_surface_observation_class": "FIELD_INTRODUCED_SURFACE_PRESENT_VALUES_ABSENT" if total_values_present == 0 else "FIELD_INTRODUCED_SURFACE_PRESENT_VALUES_PRESENT",
    }

def build_audit(rows: List[Dict[str, Any]], summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduced_surface_extraction_audit_v0",
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "input_overlay_path": rel(TOP_GROUP_OVERLAY_PATH),
        "output_field_rows_path": rel(FIELD_ROW_OUTPUT_PATH),
        "row_count": len(rows),
        "expected_row_count": EXPECTED_ROW_COUNT,
        "row_count_matches_expected": len(rows) == EXPECTED_ROW_COUNT,
        "all_field_keys_visible": summary["all_field_keys_visible"],
        "all_status_keys_visible": summary["all_status_keys_visible"],
        "all_absence_reason_keys_visible": summary["all_absence_reason_keys_visible"],
        "all_provenance_keys_visible": summary["all_provenance_keys_visible"],
        "all_provenance_refs_present": summary["all_provenance_refs_present"],
        "any_values_present": summary["any_values_present"],
        "all_values_absent": summary["all_values_absent"],
        "expected_null_status_only": summary["expected_null_status_only"],
        "expected_absence_reason_only": summary["expected_absence_reason_only"],
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_mutation_count": 0,
        "source_semantics_mutation_count": 0,
        "source_provenance_repair_executed_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "next_command_emitted_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
    }

def build_classification_packet(summary: Dict[str, Any], audit: Dict[str, Any]) -> Dict[str, Any]:
    if summary["all_field_keys_visible"] and summary["all_values_absent"]:
        classification = "FIELD_INTRODUCED_SURFACE_PRESENT_CONTENT_ABSENT"
        recommended = "CLASSIFY_FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT_V0"
    elif summary["all_field_keys_visible"] and summary["any_values_present"]:
        classification = "FIELD_INTRODUCED_SURFACE_PRESENT_VALUES_OBSERVED"
        recommended = "CLASSIFY_FIELD_INTRODUCED_SURFACE_VALUES_EVIDENCE_V0"
    else:
        classification = "FIELD_INTRODUCED_SURFACE_DEFICIENT"
        recommended = "REPAIR_FIELD_INTRODUCED_SURFACE_EXTRACTION_V0"

    return {
        "schema_version": "field_introduced_surface_classification_packet_v0",
        "packet_type": "CLASSIFICATION_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": classification,
        "recommended_next_handling": recommended,
        "recommended_next_unit": recommended,
        "evidence_sufficient_for_taxonomy_delta": False,
        "evidence_sufficient_for_value_inference": False,
        "evidence_sufficient_for_source_mutation": False,
        "evidence_sufficient_for_next_classification": True,
        "may_emit_next_command": False,
        "may_invent_missing_label_value": False,
        "may_create_taxonomy_label": False,
        "may_upgrade_taxonomy": False,
        "may_mutate_historical_source": False,
        "may_mutate_existing_receipts": False,
        "may_auto_open_next_group": False,
        "review_only": True,
        "observation_summary": {
            "row_count": summary["row_count"],
            "all_field_keys_visible": summary["all_field_keys_visible"],
            "all_values_absent": summary["all_values_absent"],
            "all_absence_reason_keys_visible": summary["all_absence_reason_keys_visible"],
            "all_provenance_refs_present": summary["all_provenance_refs_present"],
            "field_introduced_surface_observation_class": summary["field_introduced_surface_observation_class"],
        },
    }

def build_report(summary: Dict[str, Any], audit: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduced_surface_rerun_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
            "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
            "source_field_intro_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
            "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
            "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
            "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
            "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        },
        "input_overlay_path": rel(TOP_GROUP_OVERLAY_PATH),
        "output_field_rows_path": rel(FIELD_ROW_OUTPUT_PATH),
        "observation_class": summary["field_introduced_surface_observation_class"],
        "classification": packet["classification"],
        "recommended_next_unit": packet["recommended_next_unit"],
        "row_count": summary["row_count"],
        "introduced_field_count": summary["introduced_field_count"],
        "all_field_keys_visible": summary["all_field_keys_visible"],
        "all_status_keys_visible": summary["all_status_keys_visible"],
        "all_absence_reason_keys_visible": summary["all_absence_reason_keys_visible"],
        "all_provenance_keys_visible": summary["all_provenance_keys_visible"],
        "all_provenance_refs_present": summary["all_provenance_refs_present"],
        "any_values_present": summary["any_values_present"],
        "all_values_absent": summary["all_values_absent"],
        "expected_null_status_only": summary["expected_null_status_only"],
        "expected_absence_reason_only": summary["expected_absence_reason_only"],
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_mutation_count": 0,
        "source_semantics_mutation_count": 0,
        "source_provenance_repair_executed_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "next_command_emitted_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "review_only": True,
    }

def validate_outputs(rows: List[Dict[str, Any]], summary: Dict[str, Any], audit: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if len(rows) != EXPECTED_ROW_COUNT:
        failures.append("output_row_count_wrong")
    if summary["row_count"] != EXPECTED_ROW_COUNT:
        failures.append("summary_row_count_wrong")
    if audit["row_count_matches_expected"] is not True:
        failures.append("audit_row_count_wrong")
    for key in [
        "all_field_keys_visible",
        "all_status_keys_visible",
        "all_absence_reason_keys_visible",
        "all_provenance_keys_visible",
        "all_provenance_refs_present",
        "all_values_absent",
        "expected_null_status_only",
        "expected_absence_reason_only",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_not_true:{key}:{summary.get(key)}")
        if audit.get(key) is not True:
            failures.append(f"audit_not_true:{key}:{audit.get(key)}")
        if report.get(key) is not True:
            failures.append(f"report_not_true:{key}:{report.get(key)}")
    if summary["any_values_present"] is not False:
        failures.append("summary_values_present")
    if audit["any_values_present"] is not False:
        failures.append("audit_values_present")
    if report["any_values_present"] is not False:
        failures.append("report_values_present")
    if summary["field_introduced_surface_observation_class"] != "FIELD_INTRODUCED_SURFACE_PRESENT_VALUES_ABSENT":
        failures.append("observation_class_wrong")
    if packet["classification"] != "FIELD_INTRODUCED_SURFACE_PRESENT_CONTENT_ABSENT":
        failures.append("packet_classification_wrong")
    if packet["recommended_next_unit"] != "CLASSIFY_FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT_V0":
        failures.append("packet_next_unit_wrong")
    for key in [
        "may_emit_next_command",
        "may_invent_missing_label_value",
        "may_create_taxonomy_label",
        "may_upgrade_taxonomy",
        "may_mutate_historical_source",
        "may_mutate_existing_receipts",
        "may_auto_open_next_group",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")
    for key in [
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "historical_source_overwrite_count",
        "existing_receipt_mutation_count",
        "source_mutation_count",
        "source_semantics_mutation_count",
        "source_provenance_repair_executed_count",
        "taxonomy_delta_proposal_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "next_command_emitted_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if audit.get(key) != 0:
            failures.append(f"audit_count_not_zero:{key}:{audit.get(key)}")
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_field_introduction_build_receipt_id") != SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID:
        failures.append("source_build_receipt_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "FIELD_INTRO_RERUN_0_BUILD_RECEIPT_CONSUMED",
        "FIELD_INTRO_RERUN_1_HUMAN_DECISION_RECORDED",
        "FIELD_INTRO_RERUN_2_OVERLAY_READ",
        "FIELD_INTRO_RERUN_3_FIELD_ROWS_EMITTED",
        "FIELD_INTRO_RERUN_4_KEYS_VISIBLE",
        "FIELD_INTRO_RERUN_5_ABSENCE_REASONS_AND_PROVENANCE_VISIBLE",
        "FIELD_INTRO_RERUN_6_VALUES_NOT_INVENTED",
        "FIELD_INTRO_RERUN_7_CLASSIFICATION_PACKET_EMITTED",
        "FIELD_INTRO_RERUN_8_NO_SOURCE_OR_RECEIPT_MUTATION",
        "FIELD_INTRO_RERUN_9_NO_TAXONOMY_ACTION",
        "FIELD_INTRO_RERUN_10_NO_HIDDEN_NEXT_COMMAND",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("row_count") != EXPECTED_ROW_COUNT:
        failures.append("metric_row_count_wrong")
    if metrics.get("introduced_field_count") != len(INTRODUCED_FIELDS):
        failures.append("metric_field_count_wrong")
    if metrics.get("observation_class") != "FIELD_INTRODUCED_SURFACE_PRESENT_VALUES_ABSENT":
        failures.append("metric_observation_class_wrong")
    if metrics.get("classification") != "FIELD_INTRODUCED_SURFACE_PRESENT_CONTENT_ABSENT":
        failures.append("metric_classification_wrong")
    if metrics.get("recommended_next_unit") != "CLASSIFY_FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT_V0":
        failures.append("metric_next_unit_wrong")
    for key in [
        "all_field_keys_visible",
        "all_status_keys_visible",
        "all_absence_reason_keys_visible",
        "all_provenance_keys_visible",
        "all_provenance_refs_present",
        "all_values_absent",
        "expected_null_status_only",
        "expected_absence_reason_only",
    ]:
        if metrics.get(key) is not True:
            failures.append(f"metric_not_true:{key}:{metrics.get(key)}")
    if metrics.get("any_values_present") is not False:
        failures.append("metric_values_present")
    for key in [
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "historical_source_overwrite_count",
        "existing_receipt_mutation_count",
        "source_mutation_count",
        "source_semantics_mutation_count",
        "source_provenance_repair_executed_count",
        "taxonomy_delta_proposal_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "next_command_emitted_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("field_introduced_surface_rerun_guards", {})
    for key in [
        "build_receipt_consumed",
        "human_decision_recorded",
        "overlay_read",
        "field_rows_emitted",
        "keys_visible",
        "absence_reasons_and_provenance_visible",
        "classification_packet_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "values_invented",
        "historical_source_overwritten",
        "existing_receipts_mutated",
        "source_mutated",
        "source_semantics_mutated",
        "source_provenance_repair_executed",
        "taxonomy_delta_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "taxonomy_label_created",
        "next_command_emitted",
        "next_group_auto_opened",
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

    field_rows = extract_field_rows(sources)
    summary = summarize_rows(field_rows)
    audit = build_audit(field_rows, summary)
    packet = build_classification_packet(summary, audit)
    report = build_report(summary, audit, packet)

    write_jsonl(FIELD_ROW_OUTPUT_PATH, field_rows)
    write_json(OBSERVATION_SUMMARY_PATH, summary)
    write_json(EXTRACTION_AUDIT_PATH, audit)
    write_json(CLASSIFICATION_PACKET_PATH, packet)
    write_json(RERUN_REPORT_PATH, report)

    failures.extend(validate_outputs(field_rows, summary, audit, packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "FIELD_INTRO_RERUN_0_BUILD_RECEIPT_CONSUMED": sources["build_receipt"]["receipt_id"] == SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID and sources["build_receipt"]["gate"] == "PASS",
        "FIELD_INTRO_RERUN_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "RERUN_FIELD_EXTRACTION_ON_FIELD_INTRODUCED_SURFACE",
        "FIELD_INTRO_RERUN_2_OVERLAY_READ": len(sources["top_group_overlay_rows"]) == EXPECTED_ROW_COUNT,
        "FIELD_INTRO_RERUN_3_FIELD_ROWS_EMITTED": FIELD_ROW_OUTPUT_PATH.exists() and len(field_rows) == EXPECTED_ROW_COUNT,
        "FIELD_INTRO_RERUN_4_KEYS_VISIBLE": summary["all_field_keys_visible"] and summary["all_status_keys_visible"],
        "FIELD_INTRO_RERUN_5_ABSENCE_REASONS_AND_PROVENANCE_VISIBLE": summary["all_absence_reason_keys_visible"] and summary["all_provenance_refs_present"],
        "FIELD_INTRO_RERUN_6_VALUES_NOT_INVENTED": summary["all_values_absent"] and report["field_value_invention_count"] == 0,
        "FIELD_INTRO_RERUN_7_CLASSIFICATION_PACKET_EMITTED": CLASSIFICATION_PACKET_PATH.exists(),
        "FIELD_INTRO_RERUN_8_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["historical_source_overwrite_count"] == 0 and report["existing_receipt_mutation_count"] == 0 and report["source_mutation_count"] == 0,
        "FIELD_INTRO_RERUN_9_NO_TAXONOMY_ACTION": report["taxonomy_delta_proposal_emitted_count"] == 0 and report["taxonomy_upgrade_authorized_count"] == 0 and report["taxonomy_label_creation_count"] == 0,
        "FIELD_INTRO_RERUN_10_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and report["next_command_emitted_count"] == 0,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {"type": "STOP", "stop_code": "STOP_HUMAN_DECISION_REQUIRED", "next_command_goal": None}
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if any([
        report["field_value_invention_count"],
        report["taxonomy_label_creation_count"],
        report["historical_source_overwrite_count"],
        report["existing_receipt_mutation_count"],
        report["source_mutation_count"],
        report["source_semantics_mutation_count"],
        report["source_provenance_repair_executed_count"],
        report["taxonomy_delta_proposal_emitted_count"],
        report["taxonomy_upgrade_authorized_count"],
        report["next_command_emitted_count"],
        report["next_group_auto_opened_count"],
        report["hidden_next_command_count"],
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
        "source_field_introduction_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
        "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "row_count": summary["row_count"],
        "introduced_field_count": summary["introduced_field_count"],
        "introduced_field_names": INTRODUCED_FIELDS,
        "all_field_keys_visible": summary["all_field_keys_visible"],
        "all_status_keys_visible": summary["all_status_keys_visible"],
        "all_absence_reason_keys_visible": summary["all_absence_reason_keys_visible"],
        "all_provenance_keys_visible": summary["all_provenance_keys_visible"],
        "all_provenance_refs_present": summary["all_provenance_refs_present"],
        "any_values_present": summary["any_values_present"],
        "all_values_absent": summary["all_values_absent"],
        "expected_null_status_only": summary["expected_null_status_only"],
        "expected_absence_reason_only": summary["expected_absence_reason_only"],
        "observation_class": summary["field_introduced_surface_observation_class"],
        "classification": packet["classification"],
        "recommended_next_unit": packet["recommended_next_unit"],
        "field_rows_emitted_count": 1,
        "observation_summary_emitted_count": 1,
        "classification_packet_emitted_count": 1,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "source_semantics_mutation_count": 0,
        "source_provenance_repair_executed_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "next_command_emitted_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
    }

    guards = {
        "build_receipt_consumed": True,
        "human_decision_recorded": True,
        "overlay_read": True,
        "field_rows_emitted": True,
        "keys_visible": summary["all_field_keys_visible"] and summary["all_status_keys_visible"],
        "absence_reasons_and_provenance_visible": summary["all_absence_reason_keys_visible"] and summary["all_provenance_refs_present"],
        "classification_packet_emitted": True,
        "values_invented": False,
        "historical_source_overwritten": False,
        "existing_receipts_mutated": False,
        "source_mutated": source_mutation_detected,
        "source_semantics_mutated": False,
        "source_provenance_repair_executed": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "taxonomy_label_created": False,
        "next_command_emitted": False,
        "next_group_auto_opened": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_build_receipt": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "classification": packet["classification"],
        "recommended_next_unit": packet["recommended_next_unit"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "field_introduced_surface_taxonomy_gap_missing_label_field_rows": rel(FIELD_ROW_OUTPUT_PATH),
        "field_introduced_surface_observation_summary": rel(OBSERVATION_SUMMARY_PATH),
        "field_introduced_surface_extraction_audit": rel(EXTRACTION_AUDIT_PATH),
        "field_introduced_surface_classification_packet": rel(CLASSIFICATION_PACKET_PATH),
        "field_introduced_surface_rerun_report": rel(RERUN_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_receipt_v0",
        "receipt_type": "FIELD_INTRODUCED_SURFACE_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_RERUN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
        "source_field_introduction_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
        "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "field_introduced_surface_rerun_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "row_count": summary["row_count"],
            "introduced_field_names": INTRODUCED_FIELDS,
            "all_field_keys_visible": summary["all_field_keys_visible"],
            "all_absence_reasons_present": summary["all_absence_reason_keys_visible"],
            "all_provenance_refs_present": summary["all_provenance_refs_present"],
            "any_values_present": summary["any_values_present"],
            "all_values_absent": summary["all_values_absent"],
            "observation_class": summary["field_introduced_surface_observation_class"],
            "classification": packet["classification"],
            "recommended_next_unit": packet["recommended_next_unit"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "field_introduced_surface_rerun_guards": guards,
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
    print(f"field_introduced_surface_rerun_receipt_id={receipt_id}")
    print(f"field_introduced_surface_rerun_receipt_path=data/field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0_receipts/{receipt_id}.json")
    print(f"field_introduced_surface_field_rows_path=data/field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0/field_introduced_surface_taxonomy_gap_missing_label_field_rows.jsonl")
    print(f"field_introduced_surface_classification_packet_path=data/field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0/field_introduced_surface_classification_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
