#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import re
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "AUDIT_TAXONOMY_GAP_EVIDENCE_SURFACE_LOCALIZATION_V0"
TARGET_UNIT_ID = "taxonomy_gap_evidence_surface_localization_audit.v0"

SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID = "707dd84d"
SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID = "7ed31808"
SOURCE_LOOP_APPLICATION_RECEIPT_ID = "be19f438"
SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID = "6148b4fa"
SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID = "7c9718e0"
SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID = "a121ff40"

TOP_GROUP_KEY_HASH = "38c604a1"
EXPECTED_FIELD_ROW_COUNT = 25

MISSING_FIELDS = [
    "missing_label_identifier",
    "taxonomy_context_ref",
    "current_label_space_ref",
    "expected_label_space_ref",
]

STRUCTURAL_FIELDS = [
    "pressure_event_id",
    "pressure_group_key_hash",
    "parent_pressure_class",
    "pressure_subtype",
    "halt_reason",
    "source_receipt_ref",
    "source_trace_ref",
]

LOCALIZATION_CLASSES = [
    "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELDS",
    "SCHEMA_HAS_NO_SLOT_FOR_FIELDS",
    "EXTRACTOR_DID_NOT_READ_EXISTING_FIELDS",
    "PRESSURE_LABEL_TOO_COARSE_FOR_FIELD_RECOVERY",
    "INTENTIONALLY_OPAQUE_HUMAN_BOUNDARY",
    "UNKNOWN_SURFACE_DEFICIENCY",
]

OUT_DIR = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0"
RECEIPT_DIR = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0_receipts"

RAW_SOURCE_FIELD_AUDIT_PATH = OUT_DIR / "raw_source_field_audit.json"
EXTRACTOR_LOGIC_AUDIT_PATH = OUT_DIR / "extractor_logic_audit.json"
SCHEMA_SLOT_AUDIT_PATH = OUT_DIR / "schema_slot_audit.json"
LOCALIZATION_CANDIDATES_PATH = OUT_DIR / "surface_localization_candidates.json"
LOCALIZATION_CLASSIFICATION_PATH = OUT_DIR / "surface_localization_classification.json"
LOCALIZATION_DECISION_PACKET_PATH = OUT_DIR / "surface_localization_decision_packet.json"
LOCALIZATION_REPORT_PATH = OUT_DIR / "surface_localization_audit_report.json"

EVIDENCE_SURFACE_RECEIPT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0_receipts" / f"{SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID}.json"
EVIDENCE_SURFACE_FIELD_ROLLUP_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0" / "evidence_surface_field_presence_rollup.json"
EVIDENCE_SURFACE_CANDIDATES_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0" / "evidence_surface_deficiency_candidates.json"
EVIDENCE_SURFACE_CLASSIFICATION_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0" / "evidence_surface_classification.json"
EVIDENCE_SURFACE_REPAIR_PROPOSAL_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0" / "evidence_surface_repair_objective_proposal.json"
EVIDENCE_SURFACE_PACKET_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0" / "evidence_surface_decision_packet.json"
EVIDENCE_SURFACE_REPORT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0" / "evidence_surface_classification_report.json"

EVIDENCE_EXTRACTION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0_receipts" / f"{SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID}.json"
FIELD_ROWS_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0" / "taxonomy_gap_missing_label_field_rows.jsonl"
CONTEXT_REFS_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0" / "taxonomy_gap_context_refs.json"
CAUSE_CANDIDATES_SOURCE_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0" / "taxonomy_gap_operational_cause_candidates.json"
REINSPECTION_ROLLUP_SOURCE_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0" / "taxonomy_gap_reinspection_rollup.json"
FIELD_EXTRACTION_ASSESSMENT_SOURCE_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0" / "taxonomy_gap_field_extraction_assessment.json"
RECLASSIFICATION_SOURCE_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0" / "taxonomy_gap_reclassification_after_field_extraction.json"
EXTRACTION_REPORT_SOURCE_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0" / "taxonomy_gap_evidence_extraction_report.json"
EXTRACTION_PACKET_SOURCE_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0" / "taxonomy_gap_evidence_extraction_decision_packet.json"

LOOP_APPLICATION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0_receipts" / f"{SOURCE_LOOP_APPLICATION_RECEIPT_ID}.json"
PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID}.json"
TOP_GROUP_CLASSIFICATION_RECEIPT_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0_receipts" / f"{SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID}.json"
R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"
R1000_PRESSURE_EVENTS_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_event_rows.jsonl"
R1000_GROUP_MEMBERSHIP_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_candidate_c_group_event_membership.jsonl"
TOP_GROUP_MEMBERSHIP_SOURCE_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_event_membership.jsonl"
TOP_GROUP_FRAGMENTS_SOURCE_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_representative_fragments.json"

EXTRACTION_BUILDER_PATH = ROOT / "scripts" / "extract_r1000_top_group_taxonomy_gap_missing_label_evidence_v0.py"
CLASSIFICATION_BUILDER_PATH = ROOT / "scripts" / "classify_taxonomy_gap_evidence_surface_deficiency_v0.py"

SOURCE_FILES = [
    EVIDENCE_SURFACE_RECEIPT_PATH,
    EVIDENCE_SURFACE_FIELD_ROLLUP_PATH,
    EVIDENCE_SURFACE_CANDIDATES_PATH,
    EVIDENCE_SURFACE_CLASSIFICATION_PATH,
    EVIDENCE_SURFACE_REPAIR_PROPOSAL_PATH,
    EVIDENCE_SURFACE_PACKET_PATH,
    EVIDENCE_SURFACE_REPORT_PATH,
    EVIDENCE_EXTRACTION_RECEIPT_PATH,
    FIELD_ROWS_PATH,
    CONTEXT_REFS_PATH,
    CAUSE_CANDIDATES_SOURCE_PATH,
    REINSPECTION_ROLLUP_SOURCE_PATH,
    FIELD_EXTRACTION_ASSESSMENT_SOURCE_PATH,
    RECLASSIFICATION_SOURCE_PATH,
    EXTRACTION_REPORT_SOURCE_PATH,
    EXTRACTION_PACKET_SOURCE_PATH,
    LOOP_APPLICATION_RECEIPT_PATH,
    PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH,
    TOP_GROUP_CLASSIFICATION_RECEIPT_PATH,
    R1000_SCALE_RECEIPT_PATH,
    R1000_PRESSURE_EVENTS_PATH,
    R1000_GROUP_MEMBERSHIP_PATH,
    TOP_GROUP_MEMBERSHIP_SOURCE_PATH,
    TOP_GROUP_FRAGMENTS_SOURCE_PATH,
    EXTRACTION_BUILDER_PATH,
    CLASSIFICATION_BUILDER_PATH,
]

HUMAN_DECISION = {
    "decision": "AUDIT_TAXONOMY_GAP_EVIDENCE_SURFACE_LOCALIZATION",
    "scope": "localize evidence-surface deficiency only",
    "source_evidence_surface_classification_receipt_id": SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID,
    "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
    "not_authorized": [
        "taxonomy_repair",
        "taxonomy_upgrade",
        "taxonomy_delta_proposal",
        "authority_widening",
        "burden_optimization",
        "extraction_repair_execution",
        "source_mutation",
        "protocol_adoption",
        "next_group_auto_open",
        "build_command",
    ],
}

MUST_NOT_INFER = [
    "localization audit is not repair",
    "localization audit is not taxonomy delta proposal",
    "source-payload absence does not identify the missing taxonomy label",
    "schema absence does not authorize taxonomy upgrade",
    "extractor logic suspicion does not authorize extraction repair execution",
    "do not mutate source artifacts",
    "do not auto-open next group",
    "do not emit build command",
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

def flatten_keys(obj: Any, prefix: str = "") -> Set[str]:
    keys: Set[str] = set()
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            keys.add(str(k))
            keys.add(key)
            keys.update(flatten_keys(v, key))
    elif isinstance(obj, list):
        for item in obj:
            keys.update(flatten_keys(item, prefix))
    return keys

def load_sources() -> Dict[str, Any]:
    return {
        "evidence_surface_receipt": read_json(EVIDENCE_SURFACE_RECEIPT_PATH),
        "evidence_surface_field_rollup": read_json(EVIDENCE_SURFACE_FIELD_ROLLUP_PATH),
        "evidence_surface_candidates": read_json(EVIDENCE_SURFACE_CANDIDATES_PATH),
        "evidence_surface_classification": read_json(EVIDENCE_SURFACE_CLASSIFICATION_PATH),
        "evidence_surface_repair_proposal": read_json(EVIDENCE_SURFACE_REPAIR_PROPOSAL_PATH),
        "evidence_surface_packet": read_json(EVIDENCE_SURFACE_PACKET_PATH),
        "evidence_surface_report": read_json(EVIDENCE_SURFACE_REPORT_PATH),
        "evidence_extraction_receipt": read_json(EVIDENCE_EXTRACTION_RECEIPT_PATH),
        "field_rows": read_jsonl(FIELD_ROWS_PATH),
        "context_refs": read_json(CONTEXT_REFS_PATH),
        "source_cause_candidates": read_json(CAUSE_CANDIDATES_SOURCE_PATH),
        "source_reinspection_rollup": read_json(REINSPECTION_ROLLUP_SOURCE_PATH),
        "source_field_extraction_assessment": read_json(FIELD_EXTRACTION_ASSESSMENT_SOURCE_PATH),
        "source_reclassification": read_json(RECLASSIFICATION_SOURCE_PATH),
        "source_extraction_report": read_json(EXTRACTION_REPORT_SOURCE_PATH),
        "source_extraction_packet": read_json(EXTRACTION_PACKET_SOURCE_PATH),
        "loop_application_receipt": read_json(LOOP_APPLICATION_RECEIPT_PATH),
        "pressure_loop_protocol_receipt": read_json(PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH),
        "top_group_classification_receipt": read_json(TOP_GROUP_CLASSIFICATION_RECEIPT_PATH),
        "r1000_scale_receipt": read_json(R1000_SCALE_RECEIPT_PATH),
        "r1000_pressure_events": read_jsonl(R1000_PRESSURE_EVENTS_PATH),
        "r1000_group_membership": read_jsonl(R1000_GROUP_MEMBERSHIP_PATH),
        "top_group_membership": read_jsonl(TOP_GROUP_MEMBERSHIP_SOURCE_PATH),
        "top_group_fragments": read_json(TOP_GROUP_FRAGMENTS_SOURCE_PATH),
        "extraction_builder_text": EXTRACTION_BUILDER_PATH.read_text(),
        "classification_builder_text": CLASSIFICATION_BUILDER_PATH.read_text(),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    surface = sources["evidence_surface_receipt"]
    extraction = sources["evidence_extraction_receipt"]

    if surface.get("receipt_id") != SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID:
        failures.append("surface_classification_receipt_id_wrong")
    if surface.get("gate") != "PASS":
        failures.append("surface_classification_receipt_not_pass")
    if surface.get("aggregate_metrics", {}).get("classification") != "NOT_ENOUGH_EVIDENCE":
        failures.append("surface_classification_not_not_enough_evidence")
    if surface.get("aggregate_metrics", {}).get("selected_deficiency_candidate") != "UNKNOWN_SURFACE_DEFICIENCY":
        failures.append("surface_candidate_not_unknown")
    if surface.get("aggregate_metrics", {}).get("recommended_next_evidence_unit") != UNIT_ID:
        failures.append("surface_recommended_unit_not_this")
    if surface.get("aggregate_metrics", {}).get("localized_repair_target_found") is not False:
        failures.append("surface_localized_too_early")

    if extraction.get("receipt_id") != SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID:
        failures.append("extraction_receipt_id_wrong")
    if extraction.get("gate") != "PASS":
        failures.append("extraction_receipt_not_pass")
    if extraction.get("aggregate_metrics", {}).get("field_row_count") != EXPECTED_FIELD_ROW_COUNT:
        failures.append("extraction_field_row_count_wrong")
    for field in [
        "missing_label_identifier_present_count",
        "taxonomy_context_ref_present_count",
        "current_label_space_ref_present_count",
        "expected_label_space_ref_present_count",
    ]:
        if extraction.get("aggregate_metrics", {}).get(field) != 0:
            failures.append(f"extraction_expected_zero_field_wrong:{field}")

    if len(sources["field_rows"]) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_rows_length_wrong")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def group_pressure_events(sources: Dict[str, Any]) -> List[Dict[str, Any]]:
    membership_ids = {
        row["pressure_event_id"]
        for row in sources["r1000_group_membership"]
        if row.get("group_key_hash") == TOP_GROUP_KEY_HASH
    }
    rows = [
        row for row in sources["r1000_pressure_events"]
        if row.get("pressure_event_id") in membership_ids
    ]
    return sorted(rows, key=lambda row: row.get("pressure_event_id", ""))

def audit_raw_source_fields(sources: Dict[str, Any]) -> Dict[str, Any]:
    source_rows = group_pressure_events(sources)
    field_rows = sources["field_rows"]

    raw_key_union = sorted(set().union(*(flatten_keys(row) for row in source_rows))) if source_rows else []
    field_key_union = sorted(set().union(*(flatten_keys(row) for row in field_rows))) if field_rows else []

    raw_missing_profile = {
        field: sum(1 for row in source_rows if field in row and row.get(field) is not None)
        for field in MISSING_FIELDS
    }
    field_row_missing_profile = {
        field: sum(1 for row in field_rows if row.get(f"{field}_present") is True or row.get(field) is not None)
        for field in MISSING_FIELDS
    }
    structural_profile = {
        field: sum(1 for row in source_rows if row.get(field) is not None)
        for field in STRUCTURAL_FIELDS
    }

    nested_hint_hits = {}
    for field in MISSING_FIELDS:
        tokens = field.split("_")
        hit_keys = [
            key for key in raw_key_union
            if all(token in key.lower() for token in tokens[:2])
        ]
        nested_hint_hits[field] = hit_keys

    return {
        "schema_version": "raw_source_field_audit_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_row_count": len(source_rows),
        "expected_source_row_count": EXPECTED_FIELD_ROW_COUNT,
        "field_row_count": len(field_rows),
        "raw_source_field_presence_profile": raw_missing_profile,
        "extracted_field_presence_profile": field_row_missing_profile,
        "structural_field_presence_profile": structural_profile,
        "raw_key_union": raw_key_union,
        "field_row_key_union": field_key_union,
        "nested_hint_hits": nested_hint_hits,
        "raw_source_contains_any_required_missing_field": any(count > 0 for count in raw_missing_profile.values()),
        "raw_source_contains_all_required_missing_fields": all(count == len(source_rows) for count in raw_missing_profile.values()) if source_rows else False,
        "field_rows_preserve_structural_refs": all(
            row.get("source_receipt_ref") and row.get("source_trace_ref") and row.get("pressure_group_key_hash") == TOP_GROUP_KEY_HASH
            for row in field_rows
        ),
        "review_only": True,
    }

def audit_extractor_logic(sources: Dict[str, Any]) -> Dict[str, Any]:
    text = sources["extraction_builder_text"]

    field_read_patterns = {}
    for field in MISSING_FIELDS:
        patterns = [
            f'get("{field}")',
            f"get('{field}')",
            f'"{field}"',
            f"'{field}'",
        ]
        field_read_patterns[field] = {
            "direct_mentions": sum(text.count(pattern) for pattern in patterns),
            "mentioned": any(pattern in text for pattern in patterns),
        }

    fallback_keys = {
        "missing_label_identifier": ["missing_label", "label"],
        "taxonomy_context_ref": ["taxonomy_ref", "label_space_ref"],
        "current_label_space_ref": ["current_label_space_ref"],
        "expected_label_space_ref": ["expected_label_space_ref"],
    }
    fallback_profile = {
        field: {
            "fallback_keys": keys,
            "fallback_mentions": {key: key in text for key in keys},
            "all_fallbacks_mentioned": all(key in text for key in keys),
        }
        for field, keys in fallback_keys.items()
    }

    reads_any_required = any(item["mentioned"] for item in field_read_patterns.values())
    reads_all_required = all(item["mentioned"] for item in field_read_patterns.values())

    return {
        "schema_version": "extractor_logic_audit_v0",
        "extractor_builder_path": rel(EXTRACTION_BUILDER_PATH),
        "required_field_read_profile": field_read_patterns,
        "fallback_key_profile": fallback_profile,
        "extractor_mentions_any_required_missing_field": reads_any_required,
        "extractor_mentions_all_required_missing_fields": reads_all_required,
        "extractor_attempts_fallback_reads": any(
            any(profile["fallback_mentions"].values())
            for profile in fallback_profile.values()
        ),
        "extractor_logic_gap_detected": reads_all_required is False,
        "extractor_logic_gap_fields": [
            field for field, profile in field_read_patterns.items()
            if profile["mentioned"] is False
        ],
        "repair_executed": False,
        "review_only": True,
    }

def audit_schema_slots(sources: Dict[str, Any]) -> Dict[str, Any]:
    json_surfaces = {
        "evidence_surface_field_rollup": sources["evidence_surface_field_rollup"],
        "evidence_surface_classification": sources["evidence_surface_classification"],
        "evidence_extraction_receipt": sources["evidence_extraction_receipt"],
        "context_refs": sources["context_refs"],
        "source_reinspection_rollup": sources["source_reinspection_rollup"],
        "source_field_extraction_assessment": sources["source_field_extraction_assessment"],
        "source_extraction_report": sources["source_extraction_report"],
        "top_group_classification_receipt": sources["top_group_classification_receipt"],
        "r1000_scale_receipt": sources["r1000_scale_receipt"],
    }

    slot_profile = {}
    for name, obj in json_surfaces.items():
        keys = flatten_keys(obj)
        slot_profile[name] = {
            field: field in keys or any(key.endswith(f".{field}") for key in keys)
            for field in MISSING_FIELDS
        }

    source_event_key_union = sorted(set().union(*(flatten_keys(row) for row in group_pressure_events(sources)))) if group_pressure_events(sources) else []
    field_row_key_union = sorted(set().union(*(flatten_keys(row) for row in sources["field_rows"]))) if sources["field_rows"] else []

    source_event_slots = {
        field: field in source_event_key_union or any(key.endswith(f".{field}") for key in source_event_key_union)
        for field in MISSING_FIELDS
    }
    field_row_slots = {
        field: field in field_row_key_union or any(key.endswith(f".{field}") for key in field_row_key_union)
        for field in MISSING_FIELDS
    }

    return {
        "schema_version": "schema_slot_audit_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "artifact_slot_profile": slot_profile,
        "source_event_row_slot_profile": source_event_slots,
        "field_extraction_row_slot_profile": field_row_slots,
        "source_event_schema_has_required_slots": all(source_event_slots.values()),
        "field_extraction_schema_has_required_slots": all(field_row_slots.values()),
        "schema_slot_absence_detected": not all(source_event_slots.values()),
        "schema_slot_absence_fields": [field for field, present in source_event_slots.items() if present is False],
        "review_only": True,
    }

def build_localization_candidates(raw_audit: Dict[str, Any], extractor_audit: Dict[str, Any], schema_audit: Dict[str, Any]) -> Dict[str, Any]:
    candidates = []

    source_payload_support = (
        raw_audit["source_row_count"] == EXPECTED_FIELD_ROW_COUNT
        and raw_audit["raw_source_contains_any_required_missing_field"] is False
        and raw_audit["field_rows_preserve_structural_refs"] is True
    )
    extractor_reads_all = extractor_audit["extractor_mentions_all_required_missing_fields"]
    field_rows_have_slots = schema_audit["field_extraction_schema_has_required_slots"]
    source_event_has_slots = schema_audit["source_event_schema_has_required_slots"]

    candidates.append({
        "candidate_id": "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELDS",
        "localization_class": "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELDS",
        "candidate_surface": "source_payload",
        "support_level": "STRONG" if source_payload_support and extractor_reads_all else "PARTIAL",
        "supporting_evidence_refs": [
            rel(R1000_PRESSURE_EVENTS_PATH),
            rel(R1000_GROUP_MEMBERSHIP_PATH),
            rel(RAW_SOURCE_FIELD_AUDIT_PATH),
            rel(EXTRACTOR_LOGIC_AUDIT_PATH),
        ],
        "missing_fields_explained": MISSING_FIELDS,
        "localized_repair_target_refs": [rel(R1000_PRESSURE_EVENTS_PATH)],
        "may_support_fixable_surface_repair": bool(source_payload_support and extractor_reads_all),
        "may_support_healthy_expected_limit": False,
        "supports_not_enough_evidence": False,
        "forbidden_inference": "Do not infer or fill the missing label values; only localize the surface where fields are absent.",
    })

    candidates.append({
        "candidate_id": "SCHEMA_HAS_NO_SLOT_FOR_FIELDS",
        "localization_class": "SCHEMA_HAS_NO_SLOT_FOR_FIELDS",
        "candidate_surface": "schema_surface",
        "support_level": "STRONG" if not source_event_has_slots and field_rows_have_slots else "PARTIAL",
        "supporting_evidence_refs": [
            rel(SCHEMA_SLOT_AUDIT_PATH),
            rel(R1000_PRESSURE_EVENTS_PATH),
            rel(FIELD_ROWS_PATH),
        ],
        "missing_fields_explained": schema_audit["schema_slot_absence_fields"],
        "localized_repair_target_refs": [rel(R1000_PRESSURE_EVENTS_PATH)] if not source_event_has_slots else [],
        "may_support_fixable_surface_repair": bool(not source_event_has_slots and field_rows_have_slots),
        "may_support_healthy_expected_limit": False,
        "supports_not_enough_evidence": False,
        "forbidden_inference": "Schema-slot absence may justify an evidence-surface objective, not taxonomy upgrade.",
    })

    candidates.append({
        "candidate_id": "EXTRACTOR_DID_NOT_READ_EXISTING_FIELDS",
        "localization_class": "EXTRACTOR_DID_NOT_READ_EXISTING_FIELDS",
        "candidate_surface": "extractor_logic",
        "support_level": "STRONG" if extractor_audit["extractor_logic_gap_detected"] and raw_audit["raw_source_contains_any_required_missing_field"] else "NOT_SUPPORTED",
        "supporting_evidence_refs": [
            rel(EXTRACTION_BUILDER_PATH),
            rel(EXTRACTOR_LOGIC_AUDIT_PATH),
            rel(RAW_SOURCE_FIELD_AUDIT_PATH),
        ],
        "missing_fields_explained": extractor_audit["extractor_logic_gap_fields"],
        "localized_repair_target_refs": [rel(EXTRACTION_BUILDER_PATH)] if extractor_audit["extractor_logic_gap_detected"] else [],
        "may_support_fixable_surface_repair": bool(extractor_audit["extractor_logic_gap_detected"] and raw_audit["raw_source_contains_any_required_missing_field"]),
        "may_support_healthy_expected_limit": False,
        "supports_not_enough_evidence": False,
        "forbidden_inference": "Do not repair extractor logic inside this audit unit.",
    })

    candidates.append({
        "candidate_id": "PRESSURE_LABEL_TOO_COARSE_FOR_FIELD_RECOVERY",
        "localization_class": "PRESSURE_LABEL_TOO_COARSE_FOR_FIELD_RECOVERY",
        "candidate_surface": "pressure_label_coarseness",
        "support_level": "PARTIAL",
        "supporting_evidence_refs": [rel(EVIDENCE_SURFACE_CANDIDATES_PATH)],
        "missing_fields_explained": MISSING_FIELDS,
        "localized_repair_target_refs": [],
        "may_support_fixable_surface_repair": False,
        "may_support_healthy_expected_limit": False,
        "supports_not_enough_evidence": True,
        "forbidden_inference": "Coarse pressure label is not taxonomy delta evidence.",
    })

    candidates.append({
        "candidate_id": "INTENTIONALLY_OPAQUE_HUMAN_BOUNDARY",
        "localization_class": "INTENTIONALLY_OPAQUE_HUMAN_BOUNDARY",
        "candidate_surface": "intentional_opacity",
        "support_level": "NOT_ESTABLISHED",
        "supporting_evidence_refs": [rel(EVIDENCE_SURFACE_PACKET_PATH)],
        "missing_fields_explained": MISSING_FIELDS,
        "localized_repair_target_refs": [],
        "may_support_fixable_surface_repair": False,
        "may_support_healthy_expected_limit": False,
        "supports_not_enough_evidence": True,
        "forbidden_inference": "Do not mark healthy opacity without explicit boundary evidence.",
    })

    candidates.append({
        "candidate_id": "UNKNOWN_SURFACE_DEFICIENCY",
        "localization_class": "UNKNOWN_SURFACE_DEFICIENCY",
        "candidate_surface": "unknown",
        "support_level": "FALLBACK",
        "supporting_evidence_refs": [rel(EVIDENCE_SURFACE_RECEIPT_PATH)],
        "missing_fields_explained": MISSING_FIELDS,
        "localized_repair_target_refs": [],
        "may_support_fixable_surface_repair": False,
        "may_support_healthy_expected_limit": False,
        "supports_not_enough_evidence": True,
        "forbidden_inference": "Use only if no stronger localization candidate is selected.",
    })

    selectable = [
        candidate for candidate in candidates
        if candidate["support_level"] in {"STRONG", "PARTIAL"}
        and candidate["candidate_id"] != "UNKNOWN_SURFACE_DEFICIENCY"
    ]
    strong = [candidate for candidate in candidates if candidate["support_level"] == "STRONG" and candidate["may_support_fixable_surface_repair"]]
    if strong:
        selected = strong[0]
    elif selectable:
        selected = selectable[0]
    else:
        selected = [candidate for candidate in candidates if candidate["candidate_id"] == "UNKNOWN_SURFACE_DEFICIENCY"][0]

    localized = bool(selected["localized_repair_target_refs"]) and selected["candidate_id"] != "UNKNOWN_SURFACE_DEFICIENCY"

    return {
        "schema_version": "surface_localization_candidates_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "selected_localization_candidate": selected["candidate_id"],
        "selected_localization_class": selected["localization_class"],
        "selected_localization_support_level": selected["support_level"],
        "localized_surface_found": localized,
        "localized_surface_refs": selected["localized_repair_target_refs"] if localized else [],
        "may_support_evidence_surface_repair_objective": bool(localized and selected["may_support_fixable_surface_repair"]),
        "may_support_healthy_expected_limit": bool(selected["may_support_healthy_expected_limit"]),
        "supports_not_enough_evidence": bool(selected["supports_not_enough_evidence"]),
        "repair_objective_proposal_emitted": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "review_only": True,
    }

def classify_localization(candidates: Dict[str, Any]) -> Dict[str, Any]:
    if candidates["localized_surface_found"] and candidates["may_support_evidence_surface_repair_objective"]:
        classification = "LOCALIZED_EVIDENCE_SURFACE_DEFICIENCY"
        reason = "Audit localized the missing fields to a concrete evidence surface; a later classification/proposal unit may decide repair-objective eligibility."
        recommended_next = "CLASSIFY_LOCALIZED_EVIDENCE_SURFACE_REPAIR_ELIGIBILITY_V0"
    elif candidates["may_support_healthy_expected_limit"]:
        classification = "LOCALIZED_HEALTHY_EXPECTED_LIMIT"
        reason = "Audit localized the field absence to an intentional opaque boundary."
        recommended_next = "CLASSIFY_HEALTHY_EVIDENCE_LIMIT_SKIP_DECISION_V0"
    else:
        classification = "STILL_UNLOCALIZED_EVIDENCE_SURFACE_DEFICIENCY"
        reason = "Audit did not produce a concrete localized surface sufficient for repair-objective eligibility."
        recommended_next = "REQUEST_MANUAL_EVIDENCE_SURFACE_AUDIT_V0"

    return {
        "schema_version": "surface_localization_classification_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": classification,
        "selected_localization_class": candidates["selected_localization_class"],
        "selected_localization_candidate": candidates["selected_localization_candidate"],
        "selected_localization_support_level": candidates["selected_localization_support_level"],
        "localized_surface_found": candidates["localized_surface_found"],
        "localized_surface_refs": candidates["localized_surface_refs"],
        "classification_reason": reason,
        "recommended_next_review_unit": recommended_next,
        "repair_objective_proposal_emitted": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "repair_executed": False,
        "source_mutation": False,
        "build_command_emitted": False,
        "review_only": True,
    }

def build_decision_packet(classification: Dict[str, Any]) -> Dict[str, Any]:
    if classification["classification"] == "LOCALIZED_EVIDENCE_SURFACE_DEFICIENCY":
        recommended = "REVIEW_LOCALIZED_EVIDENCE_SURFACE_REPAIR_ELIGIBILITY"
    elif classification["classification"] == "LOCALIZED_HEALTHY_EXPECTED_LIMIT":
        recommended = "REVIEW_HEALTHY_LIMIT_SKIP_DECISION"
    else:
        recommended = "REQUEST_MANUAL_EVIDENCE_SURFACE_AUDIT"

    return {
        "schema_version": "surface_localization_decision_packet_v0",
        "packet_type": "HUMAN_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "localization_classification": classification["classification"],
        "selected_localization_class": classification["selected_localization_class"],
        "localized_surface_found": classification["localized_surface_found"],
        "localized_surface_refs": classification["localized_surface_refs"],
        "allowed_human_choices": [
            "REVIEW_LOCALIZED_EVIDENCE_SURFACE_REPAIR_ELIGIBILITY",
            "REQUEST_MANUAL_EVIDENCE_SURFACE_AUDIT",
            "MARK_HEALTHY_EXPECTED_EVIDENCE_LIMIT",
            "COMPARE_TOP_TWO_GROUPS_BEFORE_DECISION",
            "REJECT_LOCALIZATION_AUDIT_RESULT",
        ],
        "recommended_next_handling": recommended,
        "recommended_next_review_unit": classification["recommended_next_review_unit"],
        "may_emit_repair_command": False,
        "may_emit_build_command": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_taxonomy_delta": False,
        "may_authorize_authority_widening": False,
        "may_authorize_burden_optimization": False,
        "may_execute_extraction_repair": False,
        "may_adopt_protocol": False,
        "may_auto_open_next_group": False,
        "may_advance_without_human_decision": False,
        "review_only": True,
    }

def build_report(raw_audit: Dict[str, Any], extractor_audit: Dict[str, Any], schema_audit: Dict[str, Any], candidates: Dict[str, Any], classification: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "surface_localization_audit_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_evidence_surface_classification_receipt_id": SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID,
            "source_taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
            "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
            "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
            "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
            "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        },
        "raw_source_field_audit_summary": {
            "source_row_count": raw_audit["source_row_count"],
            "raw_source_field_presence_profile": raw_audit["raw_source_field_presence_profile"],
            "raw_source_contains_any_required_missing_field": raw_audit["raw_source_contains_any_required_missing_field"],
            "field_rows_preserve_structural_refs": raw_audit["field_rows_preserve_structural_refs"],
        },
        "extractor_logic_audit_summary": {
            "extractor_mentions_all_required_missing_fields": extractor_audit["extractor_mentions_all_required_missing_fields"],
            "extractor_logic_gap_detected": extractor_audit["extractor_logic_gap_detected"],
            "extractor_logic_gap_fields": extractor_audit["extractor_logic_gap_fields"],
        },
        "schema_slot_audit_summary": {
            "source_event_schema_has_required_slots": schema_audit["source_event_schema_has_required_slots"],
            "field_extraction_schema_has_required_slots": schema_audit["field_extraction_schema_has_required_slots"],
            "schema_slot_absence_fields": schema_audit["schema_slot_absence_fields"],
        },
        "localization_summary": classification,
        "decision_packet_recommended_next_handling": packet["recommended_next_handling"],
        "action_executed": False,
        "repair_command_emitted": False,
        "repair_executed": False,
        "repair_objective_proposal_emitted": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "burden_optimization_authorized": False,
        "extraction_repair_executed": False,
        "protocol_adoption_authorized": False,
        "next_group_auto_opened": False,
        "source_mutation": False,
        "hidden_next_command": False,
        "review_only": True,
    }

def validate_outputs(raw_audit: Dict[str, Any], extractor_audit: Dict[str, Any], schema_audit: Dict[str, Any], candidates: Dict[str, Any], classification: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if raw_audit["source_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append(f"raw_source_row_count_wrong:{raw_audit['source_row_count']}")
    for field in MISSING_FIELDS:
        if field not in raw_audit["raw_source_field_presence_profile"]:
            failures.append(f"raw_field_profile_missing:{field}")
        if field not in raw_audit["extracted_field_presence_profile"]:
            failures.append(f"extracted_field_profile_missing:{field}")
        if field not in schema_audit["source_event_row_slot_profile"]:
            failures.append(f"schema_source_slot_profile_missing:{field}")
        if field not in schema_audit["field_extraction_row_slot_profile"]:
            failures.append(f"schema_extraction_slot_profile_missing:{field}")
        if field not in extractor_audit["required_field_read_profile"]:
            failures.append(f"extractor_read_profile_missing:{field}")

    if raw_audit["field_rows_preserve_structural_refs"] is not True:
        failures.append("field_rows_structural_refs_not_preserved")
    if extractor_audit["extractor_mentions_all_required_missing_fields"] is not True:
        failures.append("extractor_does_not_read_all_required_fields")
    if schema_audit["field_extraction_schema_has_required_slots"] is not True:
        failures.append("field_extraction_schema_lacks_required_slots")

    if candidates["candidate_count"] < len(LOCALIZATION_CLASSES):
        failures.append("localization_candidates_missing")
    if candidates["selected_localization_class"] not in LOCALIZATION_CLASSES:
        failures.append("invalid_selected_localization_class")
    if candidates["localized_surface_found"] is True and not candidates["localized_surface_refs"]:
        failures.append("localized_surface_without_refs")
    if candidates["repair_objective_proposal_emitted"] is not False:
        failures.append("localization_emitted_repair_proposal")
    if candidates["taxonomy_delta_proposal_emitted"] is not False:
        failures.append("localization_emitted_taxonomy_delta")
    if candidates["taxonomy_upgrade_authorized"] is not False:
        failures.append("localization_authorized_taxonomy_upgrade")

    if classification["classification"] not in [
        "LOCALIZED_EVIDENCE_SURFACE_DEFICIENCY",
        "LOCALIZED_HEALTHY_EXPECTED_LIMIT",
        "STILL_UNLOCALIZED_EVIDENCE_SURFACE_DEFICIENCY",
    ]:
        failures.append("invalid_localization_classification")
    if classification["repair_objective_proposal_emitted"] is not False:
        failures.append("classification_emitted_repair_proposal")
    if classification["taxonomy_delta_proposal_emitted"] is not False:
        failures.append("classification_emitted_taxonomy_delta")
    if classification["taxonomy_upgrade_authorized"] is not False:
        failures.append("classification_authorized_taxonomy_upgrade")
    if classification["repair_executed"] is not False:
        failures.append("classification_executed_repair")
    if classification["source_mutation"] is not False:
        failures.append("classification_mutated_source")
    if classification["build_command_emitted"] is not False:
        failures.append("classification_emitted_build_command")

    if packet["packet_type"] != "HUMAN_REVIEW_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    for key in [
        "may_emit_repair_command",
        "may_emit_build_command",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_taxonomy_delta",
        "may_authorize_authority_widening",
        "may_authorize_burden_optimization",
        "may_execute_extraction_repair",
        "may_adopt_protocol",
        "may_auto_open_next_group",
        "may_advance_without_human_decision",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")

    for key in [
        "action_executed",
        "repair_command_emitted",
        "repair_executed",
        "repair_objective_proposal_emitted",
        "taxonomy_delta_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "burden_optimization_authorized",
        "extraction_repair_executed",
        "protocol_adoption_authorized",
        "next_group_auto_opened",
        "source_mutation",
        "hidden_next_command",
    ]:
        if report.get(key) is not False:
            failures.append(f"report_guard_not_false:{key}:{report.get(key)}")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_evidence_surface_classification_receipt_id") != SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID:
        failures.append("source_surface_receipt_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "LOCALIZATION_AUDIT_0_SOURCE_SURFACE_VERIFIED",
        "LOCALIZATION_AUDIT_1_HUMAN_DECISION_RECORDED",
        "LOCALIZATION_AUDIT_2_RAW_SOURCE_ROWS_CONSUMED",
        "LOCALIZATION_AUDIT_3_EXTRACTED_FIELD_ROWS_CONSUMED",
        "LOCALIZATION_AUDIT_4_EXTRACTOR_LOGIC_AUDITED",
        "LOCALIZATION_AUDIT_5_SCHEMA_SLOTS_AUDITED",
        "LOCALIZATION_AUDIT_6_LOCALIZATION_CANDIDATES_EMITTED",
        "LOCALIZATION_AUDIT_7_LOCALIZATION_CLASSIFIED",
        "LOCALIZATION_AUDIT_8_DECISION_PACKET_EMITTED",
        "LOCALIZATION_AUDIT_9_NO_REPAIR_OR_TAXONOMY_ACTION",
        "LOCALIZATION_AUDIT_10_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("pressure_group_key_hash") != TOP_GROUP_KEY_HASH:
        failures.append("metric_pressure_group_key_wrong")
    if metrics.get("raw_source_row_count") != EXPECTED_FIELD_ROW_COUNT:
        failures.append("metric_raw_source_row_count_wrong")
    if metrics.get("field_row_count") != EXPECTED_FIELD_ROW_COUNT:
        failures.append("metric_field_row_count_wrong")
    if metrics.get("selected_localization_class") not in LOCALIZATION_CLASSES:
        failures.append("metric_selected_localization_class_invalid")
    for key in [
        "repair_command_emitted_count",
        "build_command_emitted_count",
        "repair_executed_count",
        "repair_objective_proposal_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "authority_widening_authorized_count",
        "burden_optimization_authorized_count",
        "extraction_repair_executed_count",
        "protocol_adoption_authorized_count",
        "next_group_auto_opened_count",
        "source_mutation_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("localization_audit_guards", {})
    for key in [
        "source_surface_verified",
        "human_decision_recorded",
        "raw_source_rows_consumed",
        "extracted_field_rows_consumed",
        "extractor_logic_audited",
        "schema_slots_audited",
        "localization_candidates_emitted",
        "localization_classified",
        "decision_packet_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "repair_command_emitted",
        "build_command_emitted",
        "repair_executed",
        "repair_objective_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "taxonomy_delta_proposal_emitted",
        "authority_widening_authorized",
        "burden_optimization_authorized",
        "extraction_repair_executed",
        "protocol_adoption_authorized",
        "next_group_auto_opened",
        "source_mutation",
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

    raw_audit = audit_raw_source_fields(sources)
    extractor_audit = audit_extractor_logic(sources)
    schema_audit = audit_schema_slots(sources)
    candidates = build_localization_candidates(raw_audit, extractor_audit, schema_audit)
    classification = classify_localization(candidates)
    packet = build_decision_packet(classification)
    report = build_report(raw_audit, extractor_audit, schema_audit, candidates, classification, packet)

    write_json(RAW_SOURCE_FIELD_AUDIT_PATH, raw_audit)
    write_json(EXTRACTOR_LOGIC_AUDIT_PATH, extractor_audit)
    write_json(SCHEMA_SLOT_AUDIT_PATH, schema_audit)
    write_json(LOCALIZATION_CANDIDATES_PATH, candidates)
    write_json(LOCALIZATION_CLASSIFICATION_PATH, classification)
    write_json(LOCALIZATION_DECISION_PACKET_PATH, packet)
    write_json(LOCALIZATION_REPORT_PATH, report)

    failures.extend(validate_outputs(raw_audit, extractor_audit, schema_audit, candidates, classification, packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "LOCALIZATION_AUDIT_0_SOURCE_SURFACE_VERIFIED": len(validate_sources(sources)) == 0,
        "LOCALIZATION_AUDIT_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "AUDIT_TAXONOMY_GAP_EVIDENCE_SURFACE_LOCALIZATION",
        "LOCALIZATION_AUDIT_2_RAW_SOURCE_ROWS_CONSUMED": raw_audit["source_row_count"] == EXPECTED_FIELD_ROW_COUNT,
        "LOCALIZATION_AUDIT_3_EXTRACTED_FIELD_ROWS_CONSUMED": raw_audit["field_row_count"] == EXPECTED_FIELD_ROW_COUNT,
        "LOCALIZATION_AUDIT_4_EXTRACTOR_LOGIC_AUDITED": EXTRACTOR_LOGIC_AUDIT_PATH.exists(),
        "LOCALIZATION_AUDIT_5_SCHEMA_SLOTS_AUDITED": SCHEMA_SLOT_AUDIT_PATH.exists(),
        "LOCALIZATION_AUDIT_6_LOCALIZATION_CANDIDATES_EMITTED": LOCALIZATION_CANDIDATES_PATH.exists() and candidates["candidate_count"] >= len(LOCALIZATION_CLASSES),
        "LOCALIZATION_AUDIT_7_LOCALIZATION_CLASSIFIED": LOCALIZATION_CLASSIFICATION_PATH.exists() and classification["classification"] in [
            "LOCALIZED_EVIDENCE_SURFACE_DEFICIENCY",
            "LOCALIZED_HEALTHY_EXPECTED_LIMIT",
            "STILL_UNLOCALIZED_EVIDENCE_SURFACE_DEFICIENCY",
        ],
        "LOCALIZATION_AUDIT_8_DECISION_PACKET_EMITTED": LOCALIZATION_DECISION_PACKET_PATH.exists(),
        "LOCALIZATION_AUDIT_9_NO_REPAIR_OR_TAXONOMY_ACTION": report["repair_executed"] is False and report["taxonomy_upgrade_authorized"] is False and report["taxonomy_delta_proposal_emitted"] is False,
        "LOCALIZATION_AUDIT_10_NO_SOURCE_MUTATION": source_mutation_detected is False,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {"type": "STOP", "stop_code": "STOP_HUMAN_DECISION_REQUIRED", "next_command_goal": None}
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if any([
        report["repair_command_emitted"],
        report["repair_executed"],
        report["repair_objective_proposal_emitted"],
        report["taxonomy_delta_proposal_emitted"],
        report["taxonomy_upgrade_authorized"],
        report["authority_widening_authorized"],
        report["burden_optimization_authorized"],
        report["extraction_repair_executed"],
        report["source_mutation"],
        report["hidden_next_command"],
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_evidence_surface_classification_receipt_id": SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID,
        "source_taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
        "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
        "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "raw_source_row_count": raw_audit["source_row_count"],
        "field_row_count": raw_audit["field_row_count"],
        "raw_source_contains_any_required_missing_field": raw_audit["raw_source_contains_any_required_missing_field"],
        "extractor_mentions_all_required_missing_fields": extractor_audit["extractor_mentions_all_required_missing_fields"],
        "source_event_schema_has_required_slots": schema_audit["source_event_schema_has_required_slots"],
        "field_extraction_schema_has_required_slots": schema_audit["field_extraction_schema_has_required_slots"],
        "selected_localization_candidate": candidates["selected_localization_candidate"],
        "selected_localization_class": candidates["selected_localization_class"],
        "selected_localization_support_level": candidates["selected_localization_support_level"],
        "localized_surface_found": candidates["localized_surface_found"],
        "localized_surface_refs": candidates["localized_surface_refs"],
        "classification": classification["classification"],
        "recommended_next_review_unit": classification["recommended_next_review_unit"],
        "repair_command_emitted_count": 0,
        "build_command_emitted_count": 0,
        "repair_executed_count": 0,
        "repair_objective_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "authority_widening_authorized_count": 0,
        "burden_optimization_authorized_count": 0,
        "extraction_repair_executed_count": 0,
        "protocol_adoption_authorized_count": 0,
        "next_group_auto_opened_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "hidden_next_command_count": 0,
        "review_only": True,
    }

    guards = {
        "source_surface_verified": len(validate_sources(sources)) == 0,
        "human_decision_recorded": True,
        "raw_source_rows_consumed": True,
        "extracted_field_rows_consumed": True,
        "extractor_logic_audited": True,
        "schema_slots_audited": True,
        "localization_candidates_emitted": True,
        "localization_classified": True,
        "decision_packet_emitted": True,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "repair_executed": False,
        "repair_objective_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "taxonomy_delta_proposal_emitted": False,
        "authority_widening_authorized": False,
        "burden_optimization_authorized": False,
        "extraction_repair_executed": False,
        "protocol_adoption_authorized": False,
        "next_group_auto_opened": False,
        "source_mutation": source_mutation_detected,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_surface_receipt": SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID,
        "selected_localization_class": candidates["selected_localization_class"],
        "classification": classification["classification"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "raw_source_field_audit": rel(RAW_SOURCE_FIELD_AUDIT_PATH),
        "extractor_logic_audit": rel(EXTRACTOR_LOGIC_AUDIT_PATH),
        "schema_slot_audit": rel(SCHEMA_SLOT_AUDIT_PATH),
        "surface_localization_candidates": rel(LOCALIZATION_CANDIDATES_PATH),
        "surface_localization_classification": rel(LOCALIZATION_CLASSIFICATION_PATH),
        "surface_localization_decision_packet": rel(LOCALIZATION_DECISION_PACKET_PATH),
        "surface_localization_audit_report": rel(LOCALIZATION_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "taxonomy_gap_evidence_surface_localization_audit_receipt_v0",
        "receipt_type": "TAXONOMY_GAP_EVIDENCE_SURFACE_LOCALIZATION_AUDIT_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_evidence_surface_classification_receipt_id": SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID,
        "source_taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
        "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
        "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "localization_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "selected_localization_candidate": candidates["selected_localization_candidate"],
            "selected_localization_class": candidates["selected_localization_class"],
            "selected_localization_support_level": candidates["selected_localization_support_level"],
            "localized_surface_found": candidates["localized_surface_found"],
            "localized_surface_refs": candidates["localized_surface_refs"],
            "classification": classification["classification"],
            "classification_reason": classification["classification_reason"],
            "recommended_next_review_unit": classification["recommended_next_review_unit"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "localization_audit_guards": guards,
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
    print(f"taxonomy_gap_evidence_surface_localization_audit_receipt_id={receipt_id}")
    print(f"taxonomy_gap_evidence_surface_localization_audit_receipt_path=data/taxonomy_gap_evidence_surface_localization_audit_v0_receipts/{receipt_id}.json")
    print(f"surface_localization_classification_path=data/taxonomy_gap_evidence_surface_localization_audit_v0/surface_localization_classification.json")
    print(f"surface_localization_decision_packet_path=data/taxonomy_gap_evidence_surface_localization_audit_v0/surface_localization_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
