#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "AUDIT_UPSTREAM_EXISTENCE_FOR_FIELD_INTRODUCED_R1000_TAXONOMY_GAP_VALUES_V0"
TARGET_UNIT_ID = "field_introduced_surface_upstream_existence_audit.v0"

SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID = "11d585b6"
SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID = "8617577b"
SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID = "2d9417fc"
SOURCE_PROPOSAL_TYPING_RECEIPT_ID = "5b841942"
SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID = "9ea8fc6e"
SOURCE_NULL_LIMIT_RECEIPT_ID = "9e2c2881"
SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID = "b554aace"
FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID = "b113463f"
SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID = "d6d40d57"
SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID = "bea59318"
SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID = "707dd84d"
SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID = "7ed31808"
SOURCE_LOOP_APPLICATION_RECEIPT_ID = "be19f438"
SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID = "7c9718e0"
SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID = "a121ff40"

TOP_GROUP_KEY_HASH = "38c604a1"
EXPECTED_ROW_COUNT = 25

AUDITED_FIELDS = [
    "missing_label_identifier",
    "taxonomy_context_ref",
    "current_label_space_ref",
    "expected_label_space_ref",
]

OUT_DIR = ROOT / "data" / "field_introduced_surface_upstream_existence_audit_v0"
RECEIPT_DIR = ROOT / "data" / "field_introduced_surface_upstream_existence_audit_v0_receipts"

AUDIT_SCOPE_PATH = OUT_DIR / "upstream_existence_audit_scope.json"
AUDIT_LEDGER_PATH = OUT_DIR / "upstream_existence_audit_ledger.json"
FIELD_EXISTENCE_MATRIX_PATH = OUT_DIR / "upstream_field_existence_matrix.json"
AUDIT_CLASSIFICATION_PATH = OUT_DIR / "upstream_existence_audit_classification.json"
DECISION_PACKET_PATH = OUT_DIR / "upstream_existence_audit_decision_packet.json"
AUDIT_REPORT_PATH = OUT_DIR / "upstream_existence_audit_report.json"

NULL_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_null_evidence_limit_classification_v0_receipts" / f"{SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID}.json"
NULL_LIMIT_LEDGER_PATH = ROOT / "data" / "field_introduced_surface_null_evidence_limit_classification_v0" / "field_introduced_surface_null_evidence_limit_evidence_ledger.json"
NULL_LIMIT_CLASSIFICATION_PATH = ROOT / "data" / "field_introduced_surface_null_evidence_limit_classification_v0" / "field_introduced_surface_null_evidence_limit_classification.json"
NULL_LIMIT_DECISION_PACKET_PATH = ROOT / "data" / "field_introduced_surface_null_evidence_limit_classification_v0" / "field_introduced_surface_null_evidence_limit_decision_packet.json"
NULL_LIMIT_REPORT_PATH = ROOT / "data" / "field_introduced_surface_null_evidence_limit_classification_v0" / "field_introduced_surface_null_evidence_limit_classification_report.json"

RERUN_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0_receipts" / f"{SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID}.json"
FIELD_INTRODUCED_ROWS_PATH = ROOT / "data" / "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0" / "field_introduced_surface_taxonomy_gap_missing_label_field_rows.jsonl"
BUILD_RECEIPT_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0_receipts" / f"{SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID}.json"
FIELD_INTRODUCED_OVERLAY_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "top_group_taxonomy_gap_source_payload_field_introduction_overlay.jsonl"
FIELD_INTRO_SCHEMA_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "taxonomy_gap_source_payload_field_introduction_schema_v0.json"
FIELD_INTRO_CONTRACT_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0" / "taxonomy_gap_detector_field_emission_contract_v0.json"

PROPOSAL_TYPING_RECEIPT_PATH = ROOT / "data" / "field_introduction_proposal_typing_refinement_v0_receipts" / f"{SOURCE_PROPOSAL_TYPING_RECEIPT_ID}.json"
BOUNDARY_RECEIPT_PATH = ROOT / "data" / "null_evidence_field_introduction_boundary_refinement_v0_receipts" / f"{SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID}.json"
REPAIRED_NULL_LIMIT_RECEIPT_PATH = ROOT / "data" / "repaired_surface_null_evidence_limit_classification_v0_receipts" / f"{SOURCE_NULL_LIMIT_RECEIPT_ID}.json"
COMPARISON_GATE_FIX_RECEIPT_PATH = ROOT / "data" / "repaired_surface_rerun_comparison_gate_fix_v0_receipts" / f"{SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID}.json"
FAILED_REPAIRED_RERUN_RECEIPT_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0_receipts" / f"{FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID}.json"
REPAIRED_SURFACE_FIELD_ROWS_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_taxonomy_gap_missing_label_field_rows.jsonl"
STRUCTURAL_REF_FIX_RECEIPT_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0_receipts" / f"{SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID}.json"

LOCALIZATION_AUDIT_RECEIPT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0_receipts" / f"{SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID}.json"
EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0_receipts" / f"{SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID}.json"
PRE_FIELD_INTRO_EVIDENCE_EXTRACTION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0_receipts" / f"{SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID}.json"
PRE_FIELD_INTRO_EVIDENCE_ROWS_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0" / "taxonomy_gap_missing_label_field_rows.jsonl"
LOOP_APPLICATION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0_receipts" / f"{SOURCE_LOOP_APPLICATION_RECEIPT_ID}.json"
TOP_GROUP_CLASSIFICATION_RECEIPT_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0_receipts" / f"{SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID}.json"
R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"
RAW_R1000_PRESSURE_EVENT_ROWS_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_event_rows.jsonl"

AUDIT_SOURCE_PATHS = [
    ("field_introduced_rows", FIELD_INTRODUCED_ROWS_PATH),
    ("field_introduced_overlay", FIELD_INTRODUCED_OVERLAY_PATH),
    ("repaired_surface_field_rows", REPAIRED_SURFACE_FIELD_ROWS_PATH),
    ("pre_field_introduction_evidence_rows", PRE_FIELD_INTRO_EVIDENCE_ROWS_PATH),
    ("raw_r1000_pressure_event_rows", RAW_R1000_PRESSURE_EVENT_ROWS_PATH),
]

SOURCE_FILES = [
    NULL_LIMIT_RECEIPT_PATH,
    NULL_LIMIT_LEDGER_PATH,
    NULL_LIMIT_CLASSIFICATION_PATH,
    NULL_LIMIT_DECISION_PACKET_PATH,
    NULL_LIMIT_REPORT_PATH,
    RERUN_RECEIPT_PATH,
    FIELD_INTRODUCED_ROWS_PATH,
    BUILD_RECEIPT_PATH,
    FIELD_INTRODUCED_OVERLAY_PATH,
    FIELD_INTRO_SCHEMA_PATH,
    FIELD_INTRO_CONTRACT_PATH,
    PROPOSAL_TYPING_RECEIPT_PATH,
    BOUNDARY_RECEIPT_PATH,
    REPAIRED_NULL_LIMIT_RECEIPT_PATH,
    COMPARISON_GATE_FIX_RECEIPT_PATH,
    FAILED_REPAIRED_RERUN_RECEIPT_PATH,
    REPAIRED_SURFACE_FIELD_ROWS_PATH,
    STRUCTURAL_REF_FIX_RECEIPT_PATH,
    LOCALIZATION_AUDIT_RECEIPT_PATH,
    EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_PATH,
    PRE_FIELD_INTRO_EVIDENCE_EXTRACTION_RECEIPT_PATH,
    LOOP_APPLICATION_RECEIPT_PATH,
    TOP_GROUP_CLASSIFICATION_RECEIPT_PATH,
    R1000_SCALE_RECEIPT_PATH,
]

OPTIONAL_SOURCE_FILES = [
    PRE_FIELD_INTRO_EVIDENCE_ROWS_PATH,
    RAW_R1000_PRESSURE_EVENT_ROWS_PATH,
]

HUMAN_DECISION = {
    "decision": "REQUEST_UPSTREAM_EXISTENCE_AUDIT",
    "scope": "audit explicit upstream/source-chain artifacts for preexisting values of the four field-introduction fields before marking the null evidence as expected source-content limit",
    "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
    "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
    "authorized": [
        "read explicit audited source-chain artifacts",
        "count key presence and non-null values for audited fields",
        "emit upstream existence audit ledger",
        "emit bounded decision packet",
    ],
    "not_authorized": [
        "inventing missing label values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "mutating source rows",
        "mutating existing receipts",
        "executing source-provenance repair",
        "marking expected limit",
        "authority widening",
        "burden optimization",
        "protocol adoption",
        "next group auto-open",
        "hidden next command",
    ],
}

MUST_NOT_INFER = [
    "absence in the audited explicit chain does not prove universal nonexistence outside the audited chain",
    "if no values are found, the next human decision may mark expected limit or request broader audit",
    "audit may inspect explicit source artifacts only",
    "do not invent missing label values",
    "do not emit taxonomy delta",
    "do not mutate source rows or receipts",
    "do not mark expected limit inside this unit",
    "do not auto-open next group",
]

DECISION_CHOICES = [
    "MARK_EXPECTED_SOURCE_CONTENT_LIMIT",
    "REQUEST_BROADER_UPSTREAM_EXISTENCE_AUDIT",
    "REJECT_AUDIT_AS_INSUFFICIENT",
    "REQUEST_FIELD_INTRODUCED_SURFACE_REINSPECTION",
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
    if not path.exists():
        return rows
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
        "null_limit_receipt": read_json(NULL_LIMIT_RECEIPT_PATH),
        "null_limit_classification": read_json(NULL_LIMIT_CLASSIFICATION_PATH),
        "null_limit_decision_packet": read_json(NULL_LIMIT_DECISION_PACKET_PATH),
        "null_limit_report": read_json(NULL_LIMIT_REPORT_PATH),
        "rerun_receipt": read_json(RERUN_RECEIPT_PATH),
        "build_receipt": read_json(BUILD_RECEIPT_PATH),
        "localization_audit_receipt": read_json(LOCALIZATION_AUDIT_RECEIPT_PATH),
        "audit_sources": {
            name: read_jsonl(path)
            for name, path in AUDIT_SOURCE_PATHS
        },
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    null_receipt = sources["null_limit_receipt"]
    metrics = null_receipt.get("aggregate_metrics", {})
    packet = sources["null_limit_decision_packet"]

    if null_receipt.get("receipt_id") != SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID:
        failures.append("null_limit_receipt_id_wrong")
    if null_receipt.get("gate") != "PASS":
        failures.append("null_limit_not_pass")
    if metrics.get("classification") != "FIELD_INTRODUCED_SURFACE_NULL_EVIDENCE_LIMIT":
        failures.append("null_limit_classification_wrong")
    if metrics.get("limit_type") != "CURRENT_SOURCE_CONTENT_ABSENT_UPSTREAM_EXISTENCE_UNRESOLVED":
        failures.append("null_limit_type_wrong")
    if metrics.get("upstream_existence_resolved") is not False:
        failures.append("upstream_already_resolved")
    if metrics.get("expected_limit_marked") is not False:
        failures.append("expected_limit_already_marked")
    if packet.get("next_if_request_upstream_existence_audit") != UNIT_ID:
        failures.append("decision_packet_audit_next_unit_wrong")
    if packet.get("may_execute_upstream_audit") is not False:
        failures.append("decision_packet_wrongly_authorizes_audit_execution")
    if sources["rerun_receipt"].get("receipt_id") != SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID:
        failures.append("rerun_receipt_id_wrong")
    if sources["build_receipt"].get("receipt_id") != SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID:
        failures.append("build_receipt_id_wrong")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    for path in OPTIONAL_SOURCE_FILES:
        if path.exists() and not tracked(path):
            failures.append(f"optional_source_not_tracked:{rel(path)}")

    return failures

def inspect_source_rows(name: str, path: Path, rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    field_profiles: Dict[str, Any] = {}
    for field in AUDITED_FIELDS:
        key_present_count = 0
        non_null_value_count = 0
        null_value_count = 0
        sample_non_null_values = []
        for index, row in enumerate(rows):
            if field in row:
                key_present_count += 1
                value = row.get(field)
                if value is None:
                    null_value_count += 1
                else:
                    non_null_value_count += 1
                    if len(sample_non_null_values) < 3:
                        sample_non_null_values.append({"row_index": index, "value": value})
        field_profiles[field] = {
            "key_present_count": key_present_count,
            "non_null_value_count": non_null_value_count,
            "null_value_count": null_value_count,
            "sample_non_null_values": sample_non_null_values,
        }
    return {
        "source_name": name,
        "path": rel(path),
        "exists": path.exists(),
        "tracked": tracked(path) if path.exists() else False,
        "row_count": len(rows),
        "field_profiles": field_profiles,
        "total_key_present_count": sum(profile["key_present_count"] for profile in field_profiles.values()),
        "total_non_null_value_count": sum(profile["non_null_value_count"] for profile in field_profiles.values()),
    }

def build_audit_scope(sources: Dict[str, Any]) -> Dict[str, Any]:
    audited = []
    for name, path in AUDIT_SOURCE_PATHS:
        rows = sources["audit_sources"][name]
        audited.append({
            "source_name": name,
            "path": rel(path),
            "exists": path.exists(),
            "row_count": len(rows),
            "reason_for_inclusion": {
                "field_introduced_rows": "post-field-introduction extracted field surface",
                "field_introduced_overlay": "versioned source overlay introduced by accepted field-introduction proposal",
                "repaired_surface_field_rows": "pre-field-introduction repaired field surface",
                "pre_field_introduction_evidence_rows": "original taxonomy-gap evidence extraction rows if present",
                "raw_r1000_pressure_event_rows": "localized source payload identified by evidence-surface localization audit if present",
            }[name],
        })
    return {
        "schema_version": "field_introduced_surface_upstream_existence_audit_scope_v0",
        "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "audited_fields": AUDITED_FIELDS,
        "audited_sources": audited,
        "audit_boundary": "explicit_tracked_source_chain_only",
        "non_claim": "does_not_prove_universal_nonexistence_outside_audited_chain",
    }

def build_audit_ledger(sources: Dict[str, Any]) -> Dict[str, Any]:
    source_results = []
    for name, path in AUDIT_SOURCE_PATHS:
        source_results.append(inspect_source_rows(name, path, sources["audit_sources"][name]))

    field_totals: Dict[str, Any] = {}
    for field in AUDITED_FIELDS:
        field_totals[field] = {
            "audited_key_present_count": sum(src["field_profiles"][field]["key_present_count"] for src in source_results),
            "audited_non_null_value_count": sum(src["field_profiles"][field]["non_null_value_count"] for src in source_results),
            "audited_null_value_count": sum(src["field_profiles"][field]["null_value_count"] for src in source_results),
            "sources_with_non_null_values": [
                src["source_name"]
                for src in source_results
                if src["field_profiles"][field]["non_null_value_count"] > 0
            ],
        }

    return {
        "schema_version": "field_introduced_surface_upstream_existence_audit_ledger_v0",
        "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "audited_fields": AUDITED_FIELDS,
        "source_results": source_results,
        "field_totals": field_totals,
        "audited_source_count": len(source_results),
        "audited_existing_source_count": sum(1 for src in source_results if src["exists"]),
        "audited_row_count_total": sum(src["row_count"] for src in source_results),
        "audited_key_present_count_total": sum(total["audited_key_present_count"] for total in field_totals.values()),
        "audited_non_null_value_count_total": sum(total["audited_non_null_value_count"] for total in field_totals.values()),
        "audited_values_found": any(total["audited_non_null_value_count"] > 0 for total in field_totals.values()),
    }

def build_existence_matrix(ledger: Dict[str, Any]) -> Dict[str, Any]:
    matrix = {}
    for field, totals in ledger["field_totals"].items():
        matrix[field] = {
            "exists_as_key_in_audited_chain": totals["audited_key_present_count"] > 0,
            "exists_as_non_null_value_in_audited_chain": totals["audited_non_null_value_count"] > 0,
            "audited_key_present_count": totals["audited_key_present_count"],
            "audited_non_null_value_count": totals["audited_non_null_value_count"],
            "sources_with_non_null_values": totals["sources_with_non_null_values"],
        }
    return {
        "schema_version": "field_introduced_surface_upstream_field_existence_matrix_v0",
        "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "matrix": matrix,
        "any_field_value_found": any(v["exists_as_non_null_value_in_audited_chain"] for v in matrix.values()),
        "all_field_values_absent_in_audited_chain": all(not v["exists_as_non_null_value_in_audited_chain"] for v in matrix.values()),
    }

def build_classification(ledger: Dict[str, Any], matrix: Dict[str, Any]) -> Dict[str, Any]:
    values_found = matrix["any_field_value_found"]
    if values_found:
        classification = "UPSTREAM_VALUES_FOUND_IN_AUDITED_CHAIN"
        recommended = "CLASSIFY_UPSTREAM_VALUES_FOR_TAXONOMY_GAP_RESOLUTION_V0"
        next_if_mark = None
    else:
        classification = "UPSTREAM_VALUES_NOT_FOUND_IN_AUDITED_CHAIN"
        recommended = "MARK_EXPECTED_SOURCE_CONTENT_LIMIT_OR_REQUEST_BROADER_AUDIT"
        next_if_mark = "MARK_FIELD_INTRODUCED_SURFACE_EXPECTED_SOURCE_CONTENT_LIMIT_V0"

    return {
        "schema_version": "field_introduced_surface_upstream_existence_audit_classification_v0",
        "classification_id": sha8({
            "unit": UNIT_ID,
            "source": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
            "values_found": values_found,
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        }),
        "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": classification,
        "audit_scope": "explicit_tracked_source_chain_only",
        "audited_values_found": values_found,
        "audited_non_null_value_count_total": ledger["audited_non_null_value_count_total"],
        "all_field_values_absent_in_audited_chain": matrix["all_field_values_absent_in_audited_chain"],
        "universal_upstream_nonexistence_proven": False,
        "expected_limit_marked": False,
        "taxonomy_gap_resolved": False,
        "recommended_next_handling": recommended,
        "next_if_mark_expected_source_content_limit": next_if_mark,
        "next_if_request_broader_audit": "REQUEST_BROADER_UPSTREAM_EXISTENCE_AUDIT_FOR_R1000_TAXONOMY_GAP_VALUES_V0",
        "decision_choices": DECISION_CHOICES,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_mutation_count": 0,
        "source_semantics_mutation_count": 0,
        "source_provenance_repair_executed_count": 0,
        "upstream_audit_executed_count": 1,
        "expected_limit_marked_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "next_command_emitted_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
    }

def build_decision_packet(classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduced_surface_upstream_existence_audit_decision_packet_v0",
        "packet_type": "HUMAN_DECISION_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "classification_id": classification["classification_id"],
        "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "audit_classification": classification["classification"],
        "audit_scope": classification["audit_scope"],
        "audited_values_found": classification["audited_values_found"],
        "universal_upstream_nonexistence_proven": False,
        "recommended_next_handling": classification["recommended_next_handling"],
        "allowed_human_choices": DECISION_CHOICES,
        "next_if_mark_expected_source_content_limit": classification["next_if_mark_expected_source_content_limit"],
        "next_if_request_broader_audit": classification["next_if_request_broader_audit"],
        "next_if_reject_as_insufficient": "REPAIR_UPSTREAM_EXISTENCE_AUDIT_SCOPE_V0",
        "next_if_reinspection_requested": "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_FIELD_INTRODUCED_SURFACE_V0",
        "may_mark_expected_limit": False,
        "may_execute_broader_audit": False,
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

def build_report(scope: Dict[str, Any], ledger: Dict[str, Any], matrix: Dict[str, Any], classification: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduced_surface_upstream_existence_audit_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
            "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
            "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
            "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
            "source_field_intro_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
            "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
            "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
            "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
            "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
            "source_localization_audit_receipt_id": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
        },
        "audit_scope": scope["audit_boundary"],
        "audited_fields": AUDITED_FIELDS,
        "audited_source_count": ledger["audited_source_count"],
        "audited_existing_source_count": ledger["audited_existing_source_count"],
        "audited_row_count_total": ledger["audited_row_count_total"],
        "audited_key_present_count_total": ledger["audited_key_present_count_total"],
        "audited_non_null_value_count_total": ledger["audited_non_null_value_count_total"],
        "audited_values_found": ledger["audited_values_found"],
        "all_field_values_absent_in_audited_chain": matrix["all_field_values_absent_in_audited_chain"],
        "classification": classification["classification"],
        "recommended_next_handling": classification["recommended_next_handling"],
        "decision_choices": packet["allowed_human_choices"],
        "universal_upstream_nonexistence_proven": False,
        "expected_limit_marked": False,
        "taxonomy_gap_resolved": False,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_mutation_count": 0,
        "source_semantics_mutation_count": 0,
        "source_provenance_repair_executed_count": 0,
        "upstream_audit_executed_count": 1,
        "expected_limit_marked_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "next_command_emitted_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "review_only": True,
    }

def validate_outputs(scope: Dict[str, Any], ledger: Dict[str, Any], matrix: Dict[str, Any], classification: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if scope["audit_boundary"] != "explicit_tracked_source_chain_only":
        failures.append("audit_scope_wrong")
    if ledger["audited_source_count"] != len(AUDIT_SOURCE_PATHS):
        failures.append("audited_source_count_wrong")
    if ledger["audited_existing_source_count"] < 3:
        failures.append("too_few_existing_audit_sources")
    if ledger["audited_non_null_value_count_total"] != 0:
        failures.append("audited_values_found_unexpectedly")
    if ledger["audited_values_found"] is not False:
        failures.append("ledger_values_found")
    if matrix["any_field_value_found"] is not False:
        failures.append("matrix_values_found")
    if matrix["all_field_values_absent_in_audited_chain"] is not True:
        failures.append("matrix_values_not_absent")
    if classification["classification"] != "UPSTREAM_VALUES_NOT_FOUND_IN_AUDITED_CHAIN":
        failures.append("classification_wrong")
    if classification["audited_values_found"] is not False:
        failures.append("classification_values_found")
    if classification["universal_upstream_nonexistence_proven"] is not False:
        failures.append("universal_nonexistence_overclaimed")
    if classification["expected_limit_marked"] is not False:
        failures.append("expected_limit_marked")
    if packet["packet_type"] != "HUMAN_DECISION_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    if packet["allowed_human_choices"] != DECISION_CHOICES:
        failures.append("packet_choices_wrong")
    if packet["next_if_mark_expected_source_content_limit"] != "MARK_FIELD_INTRODUCED_SURFACE_EXPECTED_SOURCE_CONTENT_LIMIT_V0":
        failures.append("packet_mark_next_wrong")
    for key in [
        "may_mark_expected_limit",
        "may_execute_broader_audit",
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
    if classification.get("upstream_audit_executed_count") != 1:
        failures.append("classification_audit_count_wrong")
    if report.get("upstream_audit_executed_count") != 1:
        failures.append("report_audit_count_wrong")
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_null_limit_classification_receipt_id") != SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID:
        failures.append("source_null_limit_receipt_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "UPSTREAM_EXISTENCE_AUDIT_0_NULL_LIMIT_RECEIPT_CONSUMED",
        "UPSTREAM_EXISTENCE_AUDIT_1_HUMAN_DECISION_RECORDED",
        "UPSTREAM_EXISTENCE_AUDIT_2_SCOPE_EMITTED",
        "UPSTREAM_EXISTENCE_AUDIT_3_LEDGER_EMITTED",
        "UPSTREAM_EXISTENCE_AUDIT_4_EXISTENCE_MATRIX_EMITTED",
        "UPSTREAM_EXISTENCE_AUDIT_5_VALUES_NOT_FOUND_IN_AUDITED_CHAIN",
        "UPSTREAM_EXISTENCE_AUDIT_6_NO_UNIVERSAL_NONEXISTENCE_OVERCLAIM",
        "UPSTREAM_EXISTENCE_AUDIT_7_DECISION_PACKET_EMITTED",
        "UPSTREAM_EXISTENCE_AUDIT_8_NO_EXPECTED_LIMIT_MARK_OR_TAXONOMY_ACTION",
        "UPSTREAM_EXISTENCE_AUDIT_9_NO_SOURCE_OR_RECEIPT_MUTATION",
        "UPSTREAM_EXISTENCE_AUDIT_10_NO_HIDDEN_NEXT_COMMAND",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("classification") != "UPSTREAM_VALUES_NOT_FOUND_IN_AUDITED_CHAIN":
        failures.append("metric_classification_wrong")
    if metrics.get("audit_scope") != "explicit_tracked_source_chain_only":
        failures.append("metric_scope_wrong")
    if metrics.get("audited_values_found") is not False:
        failures.append("metric_values_found")
    if metrics.get("audited_non_null_value_count_total") != 0:
        failures.append("metric_non_null_count_wrong")
    if metrics.get("all_field_values_absent_in_audited_chain") is not True:
        failures.append("metric_values_not_absent")
    if metrics.get("universal_upstream_nonexistence_proven") is not False:
        failures.append("metric_universal_nonexistence_overclaim")
    if metrics.get("expected_limit_marked") is not False:
        failures.append("metric_expected_limit_marked")
    if metrics.get("recommended_next_handling") != "MARK_EXPECTED_SOURCE_CONTENT_LIMIT_OR_REQUEST_BROADER_AUDIT":
        failures.append("metric_next_handling_wrong")
    if metrics.get("decision_choices") != DECISION_CHOICES:
        failures.append("metric_decision_choices_wrong")
    if metrics.get("upstream_audit_executed_count") != 1:
        failures.append("metric_audit_count_wrong")
    for key in [
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "historical_source_overwrite_count",
        "existing_receipt_mutation_count",
        "source_mutation_count",
        "source_semantics_mutation_count",
        "source_provenance_repair_executed_count",
        "expected_limit_marked_count",
        "taxonomy_delta_proposal_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "next_command_emitted_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("upstream_existence_audit_guards", {})
    for key in [
        "null_limit_receipt_consumed",
        "human_decision_recorded",
        "scope_emitted",
        "ledger_emitted",
        "existence_matrix_emitted",
        "audit_executed",
        "decision_packet_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "values_found_in_audited_chain",
        "universal_nonexistence_overclaimed",
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
    source_before = snapshot_files(SOURCE_FILES + [p for p in OPTIONAL_SOURCE_FILES if p.exists()])
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    scope = build_audit_scope(sources)
    ledger = build_audit_ledger(sources)
    matrix = build_existence_matrix(ledger)
    classification = build_classification(ledger, matrix)
    packet = build_decision_packet(classification)
    report = build_report(scope, ledger, matrix, classification, packet)

    write_json(AUDIT_SCOPE_PATH, scope)
    write_json(AUDIT_LEDGER_PATH, ledger)
    write_json(FIELD_EXISTENCE_MATRIX_PATH, matrix)
    write_json(AUDIT_CLASSIFICATION_PATH, classification)
    write_json(DECISION_PACKET_PATH, packet)
    write_json(AUDIT_REPORT_PATH, report)

    failures.extend(validate_outputs(scope, ledger, matrix, classification, packet, report))

    source_after = snapshot_files(SOURCE_FILES + [p for p in OPTIONAL_SOURCE_FILES if p.exists()])
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "UPSTREAM_EXISTENCE_AUDIT_0_NULL_LIMIT_RECEIPT_CONSUMED": sources["null_limit_receipt"]["receipt_id"] == SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID and sources["null_limit_receipt"]["gate"] == "PASS",
        "UPSTREAM_EXISTENCE_AUDIT_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "REQUEST_UPSTREAM_EXISTENCE_AUDIT",
        "UPSTREAM_EXISTENCE_AUDIT_2_SCOPE_EMITTED": AUDIT_SCOPE_PATH.exists(),
        "UPSTREAM_EXISTENCE_AUDIT_3_LEDGER_EMITTED": AUDIT_LEDGER_PATH.exists(),
        "UPSTREAM_EXISTENCE_AUDIT_4_EXISTENCE_MATRIX_EMITTED": FIELD_EXISTENCE_MATRIX_PATH.exists(),
        "UPSTREAM_EXISTENCE_AUDIT_5_VALUES_NOT_FOUND_IN_AUDITED_CHAIN": ledger["audited_values_found"] is False and ledger["audited_non_null_value_count_total"] == 0,
        "UPSTREAM_EXISTENCE_AUDIT_6_NO_UNIVERSAL_NONEXISTENCE_OVERCLAIM": classification["universal_upstream_nonexistence_proven"] is False,
        "UPSTREAM_EXISTENCE_AUDIT_7_DECISION_PACKET_EMITTED": DECISION_PACKET_PATH.exists(),
        "UPSTREAM_EXISTENCE_AUDIT_8_NO_EXPECTED_LIMIT_MARK_OR_TAXONOMY_ACTION": classification["expected_limit_marked_count"] == 0 and classification["taxonomy_delta_proposal_emitted_count"] == 0 and classification["taxonomy_upgrade_authorized_count"] == 0,
        "UPSTREAM_EXISTENCE_AUDIT_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "UPSTREAM_EXISTENCE_AUDIT_10_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and report["next_command_emitted_count"] == 0,
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
        report["expected_limit_marked_count"],
        report["taxonomy_delta_proposal_emitted_count"],
        report["taxonomy_upgrade_authorized_count"],
        report["next_command_emitted_count"],
        report["next_group_auto_opened_count"],
        report["hidden_next_command_count"],
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
        "source_field_introduction_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
        "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "source_localization_audit_receipt_id": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "audit_scope": classification["audit_scope"],
        "classification": classification["classification"],
        "audited_fields": AUDITED_FIELDS,
        "audited_source_count": ledger["audited_source_count"],
        "audited_existing_source_count": ledger["audited_existing_source_count"],
        "audited_row_count_total": ledger["audited_row_count_total"],
        "audited_key_present_count_total": ledger["audited_key_present_count_total"],
        "audited_non_null_value_count_total": ledger["audited_non_null_value_count_total"],
        "audited_values_found": ledger["audited_values_found"],
        "all_field_values_absent_in_audited_chain": matrix["all_field_values_absent_in_audited_chain"],
        "universal_upstream_nonexistence_proven": classification["universal_upstream_nonexistence_proven"],
        "expected_limit_marked": classification["expected_limit_marked"],
        "taxonomy_gap_resolved": classification["taxonomy_gap_resolved"],
        "recommended_next_handling": classification["recommended_next_handling"],
        "decision_choices": DECISION_CHOICES,
        "scope_emitted_count": 1,
        "audit_ledger_emitted_count": 1,
        "existence_matrix_emitted_count": 1,
        "audit_classification_emitted_count": 1,
        "decision_packet_emitted_count": 1,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "source_semantics_mutation_count": 0,
        "source_provenance_repair_executed_count": 0,
        "upstream_audit_executed_count": 1,
        "expected_limit_marked_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "next_command_emitted_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
    }

    guards = {
        "null_limit_receipt_consumed": True,
        "human_decision_recorded": True,
        "scope_emitted": True,
        "ledger_emitted": True,
        "existence_matrix_emitted": True,
        "audit_executed": True,
        "decision_packet_emitted": True,
        "values_found_in_audited_chain": ledger["audited_values_found"],
        "universal_nonexistence_overclaimed": classification["universal_upstream_nonexistence_proven"],
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
        "source_null_limit": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "classification": classification["classification"],
        "audited_non_null_value_count_total": ledger["audited_non_null_value_count_total"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "upstream_existence_audit_scope": rel(AUDIT_SCOPE_PATH),
        "upstream_existence_audit_ledger": rel(AUDIT_LEDGER_PATH),
        "upstream_field_existence_matrix": rel(FIELD_EXISTENCE_MATRIX_PATH),
        "upstream_existence_audit_classification": rel(AUDIT_CLASSIFICATION_PATH),
        "upstream_existence_audit_decision_packet": rel(DECISION_PACKET_PATH),
        "upstream_existence_audit_report": rel(AUDIT_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "field_introduced_surface_upstream_existence_audit_receipt_v0",
        "receipt_type": "FIELD_INTRODUCED_SURFACE_UPSTREAM_EXISTENCE_AUDIT_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
        "source_field_introduction_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
        "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "source_localization_audit_receipt_id": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "upstream_existence_audit_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "audit_scope": classification["audit_scope"],
            "audited_fields": AUDITED_FIELDS,
            "audited_source_count": ledger["audited_source_count"],
            "audited_existing_source_count": ledger["audited_existing_source_count"],
            "audited_row_count_total": ledger["audited_row_count_total"],
            "audited_non_null_value_count_total": ledger["audited_non_null_value_count_total"],
            "audited_values_found": ledger["audited_values_found"],
            "classification": classification["classification"],
            "universal_upstream_nonexistence_proven": classification["universal_upstream_nonexistence_proven"],
            "expected_limit_marked": classification["expected_limit_marked"],
            "recommended_next_handling": classification["recommended_next_handling"],
            "decision_choices": DECISION_CHOICES,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "upstream_existence_audit_guards": guards,
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
    print(f"upstream_existence_audit_receipt_id={receipt_id}")
    print(f"upstream_existence_audit_receipt_path=data/field_introduced_surface_upstream_existence_audit_v0_receipts/{receipt_id}.json")
    print(f"upstream_existence_audit_decision_packet_path=data/field_introduced_surface_upstream_existence_audit_v0/upstream_existence_audit_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
