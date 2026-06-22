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

UNIT_ID = "CLASSIFY_FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT_V0"
TARGET_UNIT_ID = "field_introduced_surface_null_evidence_limit_classification.v0"

SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID = "8617577b"
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

DECISION_CHOICES = [
    "REQUEST_UPSTREAM_EXISTENCE_AUDIT",
    "MARK_EXPECTED_SOURCE_CONTENT_LIMIT",
    "REJECT_CLASSIFICATION_AS_UNDECIDABLE",
    "REQUEST_FIELD_INTRODUCED_SURFACE_REINSPECTION",
]

OUT_DIR = ROOT / "data" / "field_introduced_surface_null_evidence_limit_classification_v0"
RECEIPT_DIR = ROOT / "data" / "field_introduced_surface_null_evidence_limit_classification_v0_receipts"

LIMIT_CLASSIFICATION_PATH = OUT_DIR / "field_introduced_surface_null_evidence_limit_classification.json"
DECISION_PACKET_PATH = OUT_DIR / "field_introduced_surface_null_evidence_limit_decision_packet.json"
EVIDENCE_LEDGER_PATH = OUT_DIR / "field_introduced_surface_null_evidence_limit_evidence_ledger.json"
CLASSIFICATION_REPORT_PATH = OUT_DIR / "field_introduced_surface_null_evidence_limit_classification_report.json"

RERUN_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0_receipts" / f"{SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID}.json"
FIELD_ROWS_PATH = ROOT / "data" / "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0" / "field_introduced_surface_taxonomy_gap_missing_label_field_rows.jsonl"
OBSERVATION_SUMMARY_PATH = ROOT / "data" / "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0" / "field_introduced_surface_observation_summary.json"
EXTRACTION_AUDIT_PATH = ROOT / "data" / "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0" / "field_introduced_surface_extraction_audit.json"
RERUN_CLASSIFICATION_PACKET_PATH = ROOT / "data" / "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0" / "field_introduced_surface_classification_packet.json"
RERUN_REPORT_PATH = ROOT / "data" / "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0" / "field_introduced_surface_rerun_report.json"

BUILD_RECEIPT_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0_receipts" / f"{SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID}.json"
SCHEMA_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "taxonomy_gap_source_payload_field_introduction_schema_v0.json"
CONTRACT_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "taxonomy_gap_detector_field_emission_contract_v0.json"
OVERLAY_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "top_group_taxonomy_gap_source_payload_field_introduction_overlay.jsonl"
BUILD_AUDIT_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "field_introduction_application_audit.json"

PROPOSAL_TYPING_RECEIPT_PATH = ROOT / "data" / "field_introduction_proposal_typing_refinement_v0_receipts" / f"{SOURCE_PROPOSAL_TYPING_RECEIPT_ID}.json"
BOUNDARY_RECEIPT_PATH = ROOT / "data" / "null_evidence_field_introduction_boundary_refinement_v0_receipts" / f"{SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID}.json"
NULL_LIMIT_RECEIPT_PATH = ROOT / "data" / "repaired_surface_null_evidence_limit_classification_v0_receipts" / f"{SOURCE_NULL_LIMIT_RECEIPT_ID}.json"
COMPARISON_GATE_FIX_RECEIPT_PATH = ROOT / "data" / "repaired_surface_rerun_comparison_gate_fix_v0_receipts" / f"{SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID}.json"
FAILED_RERUN_RECEIPT_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0_receipts" / f"{FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID}.json"
STRUCTURAL_REF_FIX_RECEIPT_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0_receipts" / f"{SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID}.json"

SOURCE_FILES = [
    RERUN_RECEIPT_PATH,
    FIELD_ROWS_PATH,
    OBSERVATION_SUMMARY_PATH,
    EXTRACTION_AUDIT_PATH,
    RERUN_CLASSIFICATION_PACKET_PATH,
    RERUN_REPORT_PATH,
    BUILD_RECEIPT_PATH,
    SCHEMA_PATH,
    CONTRACT_PATH,
    OVERLAY_PATH,
    BUILD_AUDIT_PATH,
    PROPOSAL_TYPING_RECEIPT_PATH,
    BOUNDARY_RECEIPT_PATH,
    NULL_LIMIT_RECEIPT_PATH,
    COMPARISON_GATE_FIX_RECEIPT_PATH,
    FAILED_RERUN_RECEIPT_PATH,
    STRUCTURAL_REF_FIX_RECEIPT_PATH,
]

HUMAN_DECISION = {
    "decision": "CLASSIFY_FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT",
    "scope": "classify the post-field-introduction state where required fields are structurally visible but all values remain null with provenance-backed absence reasons",
    "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
    "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
    "authorized": [
        "classify null evidence limit",
        "emit evidence ledger",
        "emit decision packet",
        "recommend bounded next decision",
    ],
    "not_authorized": [
        "inventing missing label values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "mutating source rows",
        "mutating existing receipts",
        "executing source-provenance repair",
        "executing upstream audit",
        "marking expected limit",
        "authority widening",
        "burden optimization",
        "protocol adoption",
        "next group auto-open",
        "hidden next command",
    ],
}

MUST_NOT_INFER = [
    "structural field presence does not prove value presence",
    "provenance-backed null values are valid evidence of current source-content absence",
    "current source-content absence does not prove upstream nonexistence",
    "this unit classifies the limit but does not mark expected limit",
    "this unit may recommend upstream audit but does not execute it",
    "do not invent missing label values",
    "do not emit taxonomy delta",
    "do not mutate source rows or receipts",
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
        "rerun_receipt": read_json(RERUN_RECEIPT_PATH),
        "field_rows": read_jsonl(FIELD_ROWS_PATH),
        "observation_summary": read_json(OBSERVATION_SUMMARY_PATH),
        "extraction_audit": read_json(EXTRACTION_AUDIT_PATH),
        "rerun_classification_packet": read_json(RERUN_CLASSIFICATION_PACKET_PATH),
        "rerun_report": read_json(RERUN_REPORT_PATH),
        "build_receipt": read_json(BUILD_RECEIPT_PATH),
        "schema": read_json(SCHEMA_PATH),
        "contract": read_json(CONTRACT_PATH),
        "overlay_rows": read_jsonl(OVERLAY_PATH),
        "build_audit": read_json(BUILD_AUDIT_PATH),
        "proposal_typing_receipt": read_json(PROPOSAL_TYPING_RECEIPT_PATH),
        "boundary_receipt": read_json(BOUNDARY_RECEIPT_PATH),
        "null_limit_receipt": read_json(NULL_LIMIT_RECEIPT_PATH),
        "comparison_gate_fix_receipt": read_json(COMPARISON_GATE_FIX_RECEIPT_PATH),
        "failed_rerun_receipt": read_json(FAILED_RERUN_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    rerun_receipt = sources["rerun_receipt"]
    metrics = rerun_receipt.get("aggregate_metrics", {})
    packet = sources["rerun_classification_packet"]

    if rerun_receipt.get("receipt_id") != SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID:
        failures.append("rerun_receipt_id_wrong")
    if rerun_receipt.get("gate") != "PASS":
        failures.append("rerun_not_pass")
    if metrics.get("row_count") != EXPECTED_ROW_COUNT:
        failures.append("rerun_row_count_wrong")
    if metrics.get("all_field_keys_visible") is not True:
        failures.append("field_keys_not_visible")
    if metrics.get("all_absence_reason_keys_visible") is not True:
        failures.append("absence_reason_keys_not_visible")
    if metrics.get("all_provenance_refs_present") is not True:
        failures.append("provenance_refs_not_present")
    if metrics.get("any_values_present") is not False:
        failures.append("values_present_unexpectedly")
    if metrics.get("all_values_absent") is not True:
        failures.append("values_not_all_absent")
    if metrics.get("classification") != "FIELD_INTRODUCED_SURFACE_PRESENT_CONTENT_ABSENT":
        failures.append("rerun_classification_wrong")
    if packet.get("recommended_next_unit") != UNIT_ID:
        failures.append("rerun_packet_next_unit_wrong")
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
            failures.append(f"source_metric_not_zero:{key}:{metrics.get(key)}")

    if len(sources["field_rows"]) != EXPECTED_ROW_COUNT:
        failures.append("field_rows_count_wrong")
    if len(sources["overlay_rows"]) != EXPECTED_ROW_COUNT:
        failures.append("overlay_rows_count_wrong")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_evidence_ledger(sources: Dict[str, Any]) -> Dict[str, Any]:
    rows = sources["field_rows"]
    field_profiles = {}
    for field in INTRODUCED_FIELDS:
        value_status_field = f"{field}_value_status"
        absence_reason_field = f"{field}_absence_reason"
        provenance_field = f"{field}_provenance_ref"
        field_profiles[field] = {
            "key_visible_count": sum(1 for row in rows if row.get(f"{field}_key_visible") is True),
            "value_present_count": sum(1 for row in rows if row.get(f"{field}_value_present") is True),
            "value_status_counts": dict(Counter(row.get(value_status_field) for row in rows)),
            "absence_reason_counts": dict(Counter(row.get(absence_reason_field) for row in rows)),
            "provenance_ref_present_count": sum(1 for row in rows if row.get(provenance_field) is not None),
        }

    return {
        "schema_version": "field_introduced_surface_null_evidence_limit_evidence_ledger_v0",
        "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "row_count": len(rows),
        "introduced_field_names": INTRODUCED_FIELDS,
        "field_profiles": field_profiles,
        "global_observation": {
            "all_field_keys_visible": sources["observation_summary"]["all_field_keys_visible"],
            "all_absence_reason_keys_visible": sources["observation_summary"]["all_absence_reason_keys_visible"],
            "all_provenance_refs_present": sources["observation_summary"]["all_provenance_refs_present"],
            "all_values_absent": sources["observation_summary"]["all_values_absent"],
            "any_values_present": sources["observation_summary"]["any_values_present"],
            "expected_null_status_only": sources["observation_summary"]["expected_null_status_only"],
            "expected_absence_reason_only": sources["observation_summary"]["expected_absence_reason_only"],
        },
        "evidence_conclusion": "FIELD_SURFACE_STRUCTURALLY_PRESENT_BUT_SOURCE_CONTENT_VALUES_ABSENT",
        "non_conclusions": [
            "does_not_prove_upstream_nonexistence",
            "does_not_authorize_value_invention",
            "does_not_authorize_taxonomy_delta",
            "does_not_authorize_expected_limit_marker",
        ],
    }

def build_classification(sources: Dict[str, Any], ledger: Dict[str, Any]) -> Dict[str, Any]:
    summary = sources["observation_summary"]
    classification_id = sha8({
        "unit": UNIT_ID,
        "source": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "class": "FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
    })
    if (
        summary["all_field_keys_visible"] is True
        and summary["all_absence_reason_keys_visible"] is True
        and summary["all_provenance_refs_present"] is True
        and summary["all_values_absent"] is True
        and summary["any_values_present"] is False
    ):
        classification = "FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT"
        limit_type = "CURRENT_SOURCE_CONTENT_ABSENT_UPSTREAM_EXISTENCE_UNRESOLVED"
        recommended = "REQUEST_UPSTREAM_EXISTENCE_AUDIT_OR_MARK_EXPECTED_LIMIT"
        recommended_next_unit_if_audit = "AUDIT_UPSTREAM_EXISTENCE_FOR_FIELD_INTRODUCED_R1000_TAXONOMY_GAP_VALUES_V0"
        recommended_next_unit_if_expected_limit = "MARK_FIELD_INTRODUCED_SURFACE_EXPECTED_SOURCE_CONTENT_LIMIT_V0"
    else:
        classification = "FIELD_INTRODUCED_SURFACE_CLASSIFICATION_UNSTABLE"
        limit_type = "REINSPECTION_REQUIRED"
        recommended = "REQUEST_FIELD_INTRODUCED_SURFACE_REINSPECTION"
        recommended_next_unit_if_audit = None
        recommended_next_unit_if_expected_limit = None

    return {
        "schema_version": "field_introduced_surface_null_evidence_limit_classification_v0",
        "classification_id": classification_id,
        "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": classification,
        "limit_type": limit_type,
        "classification_basis": [
            "all introduced field keys are visible",
            "all absence reason keys are visible",
            "all provenance refs are present",
            "all introduced values are absent",
            "no introduced values were invented",
        ],
        "evidence_ledger_ref": rel(EVIDENCE_LEDGER_PATH),
        "current_source_content_absent": True,
        "upstream_existence_resolved": False,
        "expected_limit_marked": False,
        "taxonomy_gap_resolved": False,
        "taxonomy_delta_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "value_inference_authorized": False,
        "recommended_next_handling": recommended,
        "recommended_next_unit_if_upstream_audit": recommended_next_unit_if_audit,
        "recommended_next_unit_if_expected_limit": recommended_next_unit_if_expected_limit,
        "decision_choices": DECISION_CHOICES,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_mutation_count": 0,
        "source_semantics_mutation_count": 0,
        "source_provenance_repair_executed_count": 0,
        "upstream_audit_executed_count": 0,
        "expected_limit_marked_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "next_command_emitted_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
    }

def build_decision_packet(classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduced_surface_null_evidence_limit_decision_packet_v0",
        "packet_type": "HUMAN_DECISION_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "classification_id": classification["classification_id"],
        "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": classification["classification"],
        "limit_type": classification["limit_type"],
        "recommended_next_handling": classification["recommended_next_handling"],
        "allowed_human_choices": DECISION_CHOICES,
        "next_if_request_upstream_existence_audit": classification["recommended_next_unit_if_upstream_audit"],
        "next_if_mark_expected_source_content_limit": classification["recommended_next_unit_if_expected_limit"],
        "next_if_reject_as_undecidable": "REPAIR_FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT_CLASSIFICATION_V0",
        "next_if_reinspection_requested": "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_FIELD_INTRODUCED_SURFACE_V0",
        "may_execute_upstream_audit": False,
        "may_mark_expected_limit": False,
        "may_emit_next_command": False,
        "may_invent_missing_label_value": False,
        "may_create_taxonomy_label": False,
        "may_upgrade_taxonomy": False,
        "may_emit_taxonomy_delta": False,
        "may_mutate_source": False,
        "may_mutate_existing_receipts": False,
        "may_auto_open_next_group": False,
        "review_only": True,
    }

def build_report(classification: Dict[str, Any], packet: Dict[str, Any], ledger: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduced_surface_null_evidence_limit_classification_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
            "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
            "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
            "source_field_intro_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
            "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
            "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
            "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
            "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        },
        "classification_id": classification["classification_id"],
        "classification": classification["classification"],
        "limit_type": classification["limit_type"],
        "recommended_next_handling": classification["recommended_next_handling"],
        "allowed_human_choices": packet["allowed_human_choices"],
        "row_count": ledger["row_count"],
        "introduced_field_count": len(ledger["introduced_field_names"]),
        "all_field_keys_visible": ledger["global_observation"]["all_field_keys_visible"],
        "all_absence_reason_keys_visible": ledger["global_observation"]["all_absence_reason_keys_visible"],
        "all_provenance_refs_present": ledger["global_observation"]["all_provenance_refs_present"],
        "all_values_absent": ledger["global_observation"]["all_values_absent"],
        "any_values_present": ledger["global_observation"]["any_values_present"],
        "current_source_content_absent": classification["current_source_content_absent"],
        "upstream_existence_resolved": classification["upstream_existence_resolved"],
        "expected_limit_marked": classification["expected_limit_marked"],
        "taxonomy_gap_resolved": classification["taxonomy_gap_resolved"],
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_mutation_count": 0,
        "source_semantics_mutation_count": 0,
        "source_provenance_repair_executed_count": 0,
        "upstream_audit_executed_count": 0,
        "expected_limit_marked_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "next_command_emitted_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "review_only": True,
    }

def validate_outputs(ledger: Dict[str, Any], classification: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if ledger["row_count"] != EXPECTED_ROW_COUNT:
        failures.append("ledger_row_count_wrong")
    if ledger["global_observation"]["all_field_keys_visible"] is not True:
        failures.append("ledger_field_keys_not_visible")
    if ledger["global_observation"]["all_absence_reason_keys_visible"] is not True:
        failures.append("ledger_absence_reasons_not_visible")
    if ledger["global_observation"]["all_provenance_refs_present"] is not True:
        failures.append("ledger_provenance_refs_not_present")
    if ledger["global_observation"]["all_values_absent"] is not True:
        failures.append("ledger_values_not_absent")
    if ledger["global_observation"]["any_values_present"] is not False:
        failures.append("ledger_values_present")
    if classification["classification"] != "FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT":
        failures.append("classification_wrong")
    if classification["limit_type"] != "CURRENT_SOURCE_CONTENT_ABSENT_UPSTREAM_EXISTENCE_UNRESOLVED":
        failures.append("limit_type_wrong")
    if classification["current_source_content_absent"] is not True:
        failures.append("current_source_content_absent_not_true")
    if classification["upstream_existence_resolved"] is not False:
        failures.append("upstream_existence_resolved_unexpected")
    if classification["expected_limit_marked"] is not False:
        failures.append("expected_limit_marked_unexpected")
    if classification["decision_choices"] != DECISION_CHOICES:
        failures.append("decision_choices_wrong")
    if packet["packet_type"] != "HUMAN_DECISION_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    if packet["allowed_human_choices"] != DECISION_CHOICES:
        failures.append("packet_choices_wrong")
    if packet["recommended_next_handling"] != "REQUEST_UPSTREAM_EXISTENCE_AUDIT_OR_MARK_EXPECTED_LIMIT":
        failures.append("packet_recommended_next_wrong")
    for key in [
        "may_execute_upstream_audit",
        "may_mark_expected_limit",
        "may_emit_next_command",
        "may_invent_missing_label_value",
        "may_create_taxonomy_label",
        "may_upgrade_taxonomy",
        "may_emit_taxonomy_delta",
        "may_mutate_source",
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
        "upstream_audit_executed_count",
        "expected_limit_marked_count",
        "taxonomy_delta_proposal_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "next_command_emitted_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if classification.get(key) != 0:
            failures.append(f"classification_count_not_zero:{key}:{classification.get(key)}")
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
    if receipt.get("source_field_introduced_surface_rerun_receipt_id") != SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID:
        failures.append("source_rerun_receipt_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "FIELD_INTRO_NULL_LIMIT_0_RERUN_RECEIPT_CONSUMED",
        "FIELD_INTRO_NULL_LIMIT_1_HUMAN_DECISION_RECORDED",
        "FIELD_INTRO_NULL_LIMIT_2_EVIDENCE_LEDGER_EMITTED",
        "FIELD_INTRO_NULL_LIMIT_3_NULL_LIMIT_CLASSIFIED",
        "FIELD_INTRO_NULL_LIMIT_4_DECISION_PACKET_EMITTED",
        "FIELD_INTRO_NULL_LIMIT_5_NO_UPSTREAM_AUDIT_OR_EXPECTED_LIMIT_MARK",
        "FIELD_INTRO_NULL_LIMIT_6_NO_VALUE_OR_TAXONOMY_ACTION",
        "FIELD_INTRO_NULL_LIMIT_7_NO_SOURCE_OR_RECEIPT_MUTATION",
        "FIELD_INTRO_NULL_LIMIT_8_NO_HIDDEN_NEXT_COMMAND",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("classification") != "FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT":
        failures.append("metric_classification_wrong")
    if metrics.get("limit_type") != "CURRENT_SOURCE_CONTENT_ABSENT_UPSTREAM_EXISTENCE_UNRESOLVED":
        failures.append("metric_limit_type_wrong")
    if metrics.get("recommended_next_handling") != "REQUEST_UPSTREAM_EXISTENCE_AUDIT_OR_MARK_EXPECTED_LIMIT":
        failures.append("metric_next_handling_wrong")
    if metrics.get("row_count") != EXPECTED_ROW_COUNT:
        failures.append("metric_row_count_wrong")
    if metrics.get("current_source_content_absent") is not True:
        failures.append("metric_current_source_content_absent_wrong")
    if metrics.get("upstream_existence_resolved") is not False:
        failures.append("metric_upstream_existence_resolved_wrong")
    if metrics.get("expected_limit_marked") is not False:
        failures.append("metric_expected_limit_marked_wrong")
    if metrics.get("decision_choices") != DECISION_CHOICES:
        failures.append("metric_decision_choices_wrong")
    for key in [
        "all_field_keys_visible",
        "all_absence_reason_keys_visible",
        "all_provenance_refs_present",
        "all_values_absent",
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
        "upstream_audit_executed_count",
        "expected_limit_marked_count",
        "taxonomy_delta_proposal_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "next_command_emitted_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("field_introduced_surface_null_limit_guards", {})
    for key in [
        "rerun_receipt_consumed",
        "human_decision_recorded",
        "evidence_ledger_emitted",
        "null_limit_classified",
        "decision_packet_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "upstream_audit_executed",
        "expected_limit_marked",
        "values_invented",
        "taxonomy_label_created",
        "taxonomy_delta_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "historical_source_overwritten",
        "existing_receipts_mutated",
        "source_mutated",
        "source_semantics_mutated",
        "source_provenance_repair_executed",
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

    ledger = build_evidence_ledger(sources)
    classification = build_classification(sources, ledger)
    packet = build_decision_packet(classification)
    report = build_report(classification, packet, ledger)

    write_json(EVIDENCE_LEDGER_PATH, ledger)
    write_json(LIMIT_CLASSIFICATION_PATH, classification)
    write_json(DECISION_PACKET_PATH, packet)
    write_json(CLASSIFICATION_REPORT_PATH, report)

    failures.extend(validate_outputs(ledger, classification, packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "FIELD_INTRO_NULL_LIMIT_0_RERUN_RECEIPT_CONSUMED": sources["rerun_receipt"]["receipt_id"] == SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID and sources["rerun_receipt"]["gate"] == "PASS",
        "FIELD_INTRO_NULL_LIMIT_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "CLASSIFY_FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT",
        "FIELD_INTRO_NULL_LIMIT_2_EVIDENCE_LEDGER_EMITTED": EVIDENCE_LEDGER_PATH.exists(),
        "FIELD_INTRO_NULL_LIMIT_3_NULL_LIMIT_CLASSIFIED": classification["classification"] == "FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT",
        "FIELD_INTRO_NULL_LIMIT_4_DECISION_PACKET_EMITTED": DECISION_PACKET_PATH.exists(),
        "FIELD_INTRO_NULL_LIMIT_5_NO_UPSTREAM_AUDIT_OR_EXPECTED_LIMIT_MARK": classification["upstream_audit_executed_count"] == 0 and classification["expected_limit_marked_count"] == 0,
        "FIELD_INTRO_NULL_LIMIT_6_NO_VALUE_OR_TAXONOMY_ACTION": classification["field_value_invention_count"] == 0 and classification["taxonomy_delta_proposal_emitted_count"] == 0 and classification["taxonomy_upgrade_authorized_count"] == 0,
        "FIELD_INTRO_NULL_LIMIT_7_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "FIELD_INTRO_NULL_LIMIT_8_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and report["next_command_emitted_count"] == 0,
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
        report["upstream_audit_executed_count"],
        report["expected_limit_marked_count"],
        report["taxonomy_delta_proposal_emitted_count"],
        report["taxonomy_upgrade_authorized_count"],
        report["next_command_emitted_count"],
        report["next_group_auto_opened_count"],
        report["hidden_next_command_count"],
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
        "source_field_introduction_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
        "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "row_count": ledger["row_count"],
        "introduced_field_count": len(INTRODUCED_FIELDS),
        "introduced_field_names": INTRODUCED_FIELDS,
        "all_field_keys_visible": ledger["global_observation"]["all_field_keys_visible"],
        "all_absence_reason_keys_visible": ledger["global_observation"]["all_absence_reason_keys_visible"],
        "all_provenance_refs_present": ledger["global_observation"]["all_provenance_refs_present"],
        "all_values_absent": ledger["global_observation"]["all_values_absent"],
        "any_values_present": ledger["global_observation"]["any_values_present"],
        "classification": classification["classification"],
        "limit_type": classification["limit_type"],
        "current_source_content_absent": classification["current_source_content_absent"],
        "upstream_existence_resolved": classification["upstream_existence_resolved"],
        "expected_limit_marked": classification["expected_limit_marked"],
        "taxonomy_gap_resolved": classification["taxonomy_gap_resolved"],
        "recommended_next_handling": classification["recommended_next_handling"],
        "decision_choices": DECISION_CHOICES,
        "evidence_ledger_emitted_count": 1,
        "classification_emitted_count": 1,
        "decision_packet_emitted_count": 1,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "source_semantics_mutation_count": 0,
        "source_provenance_repair_executed_count": 0,
        "upstream_audit_executed_count": 0,
        "expected_limit_marked_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "next_command_emitted_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
    }

    guards = {
        "rerun_receipt_consumed": True,
        "human_decision_recorded": True,
        "evidence_ledger_emitted": True,
        "null_limit_classified": classification["classification"] == "FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT",
        "decision_packet_emitted": True,
        "upstream_audit_executed": False,
        "expected_limit_marked": False,
        "values_invented": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "historical_source_overwritten": False,
        "existing_receipts_mutated": False,
        "source_mutated": source_mutation_detected,
        "source_semantics_mutated": False,
        "source_provenance_repair_executed": False,
        "next_command_emitted": False,
        "next_group_auto_opened": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_rerun_receipt": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "classification": classification["classification"],
        "limit_type": classification["limit_type"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "field_introduced_surface_null_evidence_limit_evidence_ledger": rel(EVIDENCE_LEDGER_PATH),
        "field_introduced_surface_null_evidence_limit_classification": rel(LIMIT_CLASSIFICATION_PATH),
        "field_introduced_surface_null_evidence_limit_decision_packet": rel(DECISION_PACKET_PATH),
        "field_introduced_surface_null_evidence_limit_classification_report": rel(CLASSIFICATION_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "field_introduced_surface_null_evidence_limit_classification_receipt_v0",
        "receipt_type": "FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT_CLASSIFICATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
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
        "field_introduced_surface_null_limit_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "row_count": ledger["row_count"],
            "introduced_field_names": INTRODUCED_FIELDS,
            "all_field_keys_visible": ledger["global_observation"]["all_field_keys_visible"],
            "all_absence_reasons_present": ledger["global_observation"]["all_absence_reason_keys_visible"],
            "all_provenance_refs_present": ledger["global_observation"]["all_provenance_refs_present"],
            "all_values_absent": ledger["global_observation"]["all_values_absent"],
            "any_values_present": ledger["global_observation"]["any_values_present"],
            "classification": classification["classification"],
            "limit_type": classification["limit_type"],
            "recommended_next_handling": classification["recommended_next_handling"],
            "decision_choices": DECISION_CHOICES,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "field_introduced_surface_null_limit_guards": guards,
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
    print(f"field_introduced_surface_null_limit_classification_receipt_id={receipt_id}")
    print(f"field_introduced_surface_null_limit_classification_receipt_path=data/field_introduced_surface_null_evidence_limit_classification_v0_receipts/{receipt_id}.json")
    print(f"field_introduced_surface_null_limit_decision_packet_path=data/field_introduced_surface_null_evidence_limit_classification_v0/field_introduced_surface_null_evidence_limit_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
