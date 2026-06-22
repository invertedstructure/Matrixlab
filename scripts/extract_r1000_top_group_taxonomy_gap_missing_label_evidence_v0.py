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

UNIT_ID = "EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_V0"
TARGET_UNIT_ID = "taxonomy_gap_missing_label_evidence_extraction.r1000_top_group.v0"

SOURCE_LOOP_APPLICATION_RECEIPT_ID = "be19f438"
SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID = "6148b4fa"
SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID = "7c9718e0"
SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID = "a121ff40"

TOP_GROUP_KEY_HASH = "38c604a1"
EXPECTED_PARENT_PRESSURE_CLASS = "TAXONOMY_PRESSURE"
EXPECTED_PRESSURE_SUBTYPE = "missing_label"
EXPECTED_HALT_REASON = "STOP_TAXONOMY_GAP"
EXPECTED_TOP_GROUP_COUNT = 25
SOURCE_EVIDENCE_REQUEST_ID = "52b0d484"

OUT_DIR = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0"
RECEIPT_DIR = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0_receipts"

FIELD_ROWS_PATH = OUT_DIR / "taxonomy_gap_missing_label_field_rows.jsonl"
CONTEXT_REFS_PATH = OUT_DIR / "taxonomy_gap_context_refs.json"
CAUSE_CANDIDATES_PATH = OUT_DIR / "taxonomy_gap_operational_cause_candidates.json"
REINSPECTION_ROLLUP_PATH = OUT_DIR / "taxonomy_gap_reinspection_rollup.json"
FIELD_EXTRACTION_ASSESSMENT_PATH = OUT_DIR / "taxonomy_gap_field_extraction_assessment.json"
EVIDENCE_EXTRACTION_REPORT_PATH = OUT_DIR / "taxonomy_gap_evidence_extraction_report.json"
EVIDENCE_EXTRACTION_DECISION_PACKET_PATH = OUT_DIR / "taxonomy_gap_evidence_extraction_decision_packet.json"
RECLASSIFICATION_PATH = OUT_DIR / "taxonomy_gap_reclassification_after_field_extraction.json"

LOOP_APP_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0_receipts" / f"{SOURCE_LOOP_APPLICATION_RECEIPT_ID}.json"
EVIDENCE_REQUEST_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0" / "taxonomy_gap_evidence_request.json"
TAXONOMY_GAP_FULL_MEMBERSHIP_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0" / "taxonomy_gap_full_membership.jsonl"
TAXONOMY_GAP_DEEP_FRAGMENT_INSPECTION_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0" / "taxonomy_gap_deep_fragment_inspection.json"
TAXONOMY_GAP_EVIDENCE_ASSESSMENT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0" / "taxonomy_gap_evidence_sufficiency_assessment.json"
TAXONOMY_GAP_RECLASSIFICATION_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0" / "taxonomy_gap_reclassification_after_inspection.json"
TAXONOMY_GAP_APP_REPORT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0" / "pressure_loop_taxonomy_gap_application_report.json"
TAXONOMY_GAP_APP_PACKET_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0" / "pressure_loop_taxonomy_gap_application_decision_packet.json"

PRESSURE_LOOP_RECEIPT_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID}.json"
PRESSURE_LOOP_PROTOCOL_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0" / "pressure_handling_loop_protocol.json"
PRESSURE_LOOP_EVIDENCE_SCHEMA_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0" / "pressure_evidence_sufficiency_schema_v0.json"

TOP_GROUP_RECEIPT_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0_receipts" / f"{SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID}.json"
TOP_GROUP_MEMBERSHIP_SOURCE_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_event_membership.jsonl"
TOP_GROUP_FRAGMENTS_SOURCE_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_representative_fragments.json"
TOP_GROUP_EVIDENCE_SOURCE_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_evidence_rollup.json"

R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"
R1000_PRESSURE_EVENTS_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_event_rows.jsonl"
R1000_GROUP_MEMBERSHIP_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_candidate_c_group_event_membership.jsonl"

SOURCE_FILES = [
    LOOP_APP_RECEIPT_PATH,
    EVIDENCE_REQUEST_PATH,
    TAXONOMY_GAP_FULL_MEMBERSHIP_PATH,
    TAXONOMY_GAP_DEEP_FRAGMENT_INSPECTION_PATH,
    TAXONOMY_GAP_EVIDENCE_ASSESSMENT_PATH,
    TAXONOMY_GAP_RECLASSIFICATION_PATH,
    TAXONOMY_GAP_APP_REPORT_PATH,
    TAXONOMY_GAP_APP_PACKET_PATH,
    PRESSURE_LOOP_RECEIPT_PATH,
    PRESSURE_LOOP_PROTOCOL_PATH,
    PRESSURE_LOOP_EVIDENCE_SCHEMA_PATH,
    TOP_GROUP_RECEIPT_PATH,
    TOP_GROUP_MEMBERSHIP_SOURCE_PATH,
    TOP_GROUP_FRAGMENTS_SOURCE_PATH,
    TOP_GROUP_EVIDENCE_SOURCE_PATH,
    R1000_SCALE_RECEIPT_PATH,
    R1000_PRESSURE_EVENTS_PATH,
    R1000_GROUP_MEMBERSHIP_PATH,
]

VALID_EVIDENCE_CLASSES = [
    "EVIDENCE_SUFFICIENT_FOR_FIXABLE_CLASSIFICATION",
    "EVIDENCE_SUFFICIENT_FOR_HEALTHY_CLASSIFICATION",
    "EVIDENCE_INSUFFICIENT_NEEDS_MORE_FRAGMENTS",
    "EVIDENCE_INSUFFICIENT_NEEDS_DEEPER_MEMBERSHIP",
    "EVIDENCE_INSUFFICIENT_NEEDS_FIELD_EXTRACTION",
    "EVIDENCE_INSUFFICIENT_NEEDS_TOP_TWO_COMPARISON",
    "EVIDENCE_INSUFFICIENT_NEEDS_SCALE_BAND",
    "EVIDENCE_BLOCKED_BY_AUTHORITY",
]

HUMAN_DECISION = {
    "decision": "EXTRACT_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE",
    "scope": "field_extraction_for_current_top_group_only",
    "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
    "source_evidence_request_id": SOURCE_EVIDENCE_REQUEST_ID,
    "not_authorized": [
        "taxonomy_repair",
        "taxonomy_upgrade",
        "taxonomy_delta_proposal",
        "authority_widening",
        "burden_optimization",
        "extraction_repair",
        "repair_execution",
        "next_group_auto_open",
        "protocol_adoption",
        "build_command",
    ],
}

MUST_NOT_INFER = [
    "field extraction is not taxonomy repair",
    "field extraction is not taxonomy upgrade",
    "field absence may classify evidence as still insufficient",
    "do not propose taxonomy delta from missing-label pressure alone",
    "do not repair extraction instrumentation in this unit",
    "do not auto-open next group",
    "do not emit build command",
    "do not mutate source artifacts",
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
        "loop_application_receipt": read_json(LOOP_APP_RECEIPT_PATH),
        "evidence_request": read_json(EVIDENCE_REQUEST_PATH),
        "taxonomy_gap_full_membership": read_jsonl(TAXONOMY_GAP_FULL_MEMBERSHIP_PATH),
        "taxonomy_gap_deep_fragment_inspection": read_json(TAXONOMY_GAP_DEEP_FRAGMENT_INSPECTION_PATH),
        "taxonomy_gap_evidence_assessment": read_json(TAXONOMY_GAP_EVIDENCE_ASSESSMENT_PATH),
        "taxonomy_gap_reclassification": read_json(TAXONOMY_GAP_RECLASSIFICATION_PATH),
        "taxonomy_gap_app_report": read_json(TAXONOMY_GAP_APP_REPORT_PATH),
        "taxonomy_gap_app_packet": read_json(TAXONOMY_GAP_APP_PACKET_PATH),
        "pressure_loop_receipt": read_json(PRESSURE_LOOP_RECEIPT_PATH),
        "pressure_loop_protocol": read_json(PRESSURE_LOOP_PROTOCOL_PATH),
        "pressure_loop_evidence_schema": read_json(PRESSURE_LOOP_EVIDENCE_SCHEMA_PATH),
        "top_group_receipt": read_json(TOP_GROUP_RECEIPT_PATH),
        "top_group_membership": read_jsonl(TOP_GROUP_MEMBERSHIP_SOURCE_PATH),
        "top_group_fragments": read_json(TOP_GROUP_FRAGMENTS_SOURCE_PATH),
        "top_group_evidence": read_json(TOP_GROUP_EVIDENCE_SOURCE_PATH),
        "r1000_scale_receipt": read_json(R1000_SCALE_RECEIPT_PATH),
        "r1000_pressure_events": read_jsonl(R1000_PRESSURE_EVENTS_PATH),
        "r1000_group_membership": read_jsonl(R1000_GROUP_MEMBERSHIP_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    app = sources["loop_application_receipt"]
    request = sources["evidence_request"]
    top = sources["top_group_receipt"]
    protocol = sources["pressure_loop_receipt"]

    if app.get("receipt_id") != SOURCE_LOOP_APPLICATION_RECEIPT_ID:
        failures.append("loop_application_receipt_id_wrong")
    if app.get("gate") != "PASS":
        failures.append("loop_application_receipt_not_pass")
    if app.get("terminal", {}).get("type") != "STOP":
        failures.append("loop_application_terminal_not_stop")
    if app.get("aggregate_metrics", {}).get("evidence_request_id") != SOURCE_EVIDENCE_REQUEST_ID:
        failures.append("source_evidence_request_id_wrong")
    if app.get("aggregate_metrics", {}).get("recommended_next_evidence_unit") != UNIT_ID:
        failures.append("loop_application_recommended_unit_not_this")
    if app.get("aggregate_metrics", {}).get("classification_after_inspection") != "NOT_ENOUGH_EVIDENCE":
        failures.append("loop_application_not_not_enough_evidence")
    if app.get("aggregate_metrics", {}).get("evidence_sufficiency_class") != "EVIDENCE_INSUFFICIENT_NEEDS_FIELD_EXTRACTION":
        failures.append("loop_application_evidence_class_wrong")

    if request.get("evidence_request_id") != SOURCE_EVIDENCE_REQUEST_ID:
        failures.append("evidence_request_id_wrong")
    if request.get("request_type") != "EVIDENCE_REQUEST_NOT_REPAIR":
        failures.append("evidence_request_type_wrong")
    if request.get("allowed_next_evidence_unit_proposal") != UNIT_ID:
        failures.append("request_next_unit_not_this")
    if request.get("repair_objective_proposal_emitted") is not False:
        failures.append("request_repair_proposal_emitted")
    if request.get("taxonomy_upgrade_proposal_emitted") is not False:
        failures.append("request_taxonomy_upgrade_proposal_emitted")
    if request.get("build_command_emitted") is not False:
        failures.append("request_build_command_emitted")

    if top.get("receipt_id") != SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID or top.get("gate") != "PASS":
        failures.append("top_group_receipt_not_pass")
    if top.get("top_group_summary", {}).get("top_group_key_hash") != TOP_GROUP_KEY_HASH:
        failures.append("top_group_key_wrong")
    if top.get("top_group_summary", {}).get("classification") != "NOT_ENOUGH_EVIDENCE":
        failures.append("top_group_classification_wrong")

    if protocol.get("receipt_id") != SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID or protocol.get("gate") != "PASS":
        failures.append("protocol_receipt_not_pass")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def extract_field_rows(sources: Dict[str, Any]) -> List[Dict[str, Any]]:
    pressure_by_id = {row["pressure_event_id"]: row for row in sources["r1000_pressure_events"]}
    app_membership = sources["taxonomy_gap_full_membership"]

    rows: List[Dict[str, Any]] = []
    for row in sorted(app_membership, key=lambda item: item["pressure_event_id"]):
        event = pressure_by_id.get(row["pressure_event_id"], {})
        missing_label_identifier = (
            row.get("missing_label_identifier")
            or event.get("missing_label_identifier")
            or event.get("missing_label")
            or event.get("label")
        )
        taxonomy_context_ref = (
            row.get("taxonomy_context_ref")
            or event.get("taxonomy_context_ref")
            or event.get("taxonomy_ref")
            or event.get("label_space_ref")
        )
        current_label_space_ref = event.get("current_label_space_ref")
        expected_label_space_ref = event.get("expected_label_space_ref")

        field_status = "FIELD_VALUES_ABSENT"
        support_level = "INSUFFICIENT"
        operational_cause_candidate = None

        if missing_label_identifier and taxonomy_context_ref:
            field_status = "FIELD_VALUES_PRESENT"
            support_level = "PARTIAL"
            operational_cause_candidate = "candidate_missing_label_requires_review"
        elif missing_label_identifier or taxonomy_context_ref:
            field_status = "PARTIAL_FIELD_VALUES_PRESENT"
            support_level = "PARTIAL"
            operational_cause_candidate = "partial_taxonomy_gap_field_presence_requires_review"

        rows.append({
            "schema_version": "taxonomy_gap_missing_label_field_row_v0",
            "pressure_event_id": row["pressure_event_id"],
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "parent_pressure_class": row.get("parent_pressure_class"),
            "pressure_subtype": row.get("pressure_subtype"),
            "halt_reason": row.get("halt_reason"),
            "work_item_id": row.get("work_item_id"),
            "slot_id": row.get("slot_id"),
            "source_receipt_ref": row.get("source_receipt_ref"),
            "source_trace_ref": row.get("source_trace_ref"),
            "pressure_pattern_signature_hash": row.get("pressure_pattern_signature_hash"),
            "missing_label_identifier": missing_label_identifier,
            "missing_label_identifier_present": missing_label_identifier is not None,
            "taxonomy_context_ref": taxonomy_context_ref,
            "taxonomy_context_ref_present": taxonomy_context_ref is not None,
            "current_label_space_ref": current_label_space_ref,
            "current_label_space_ref_present": current_label_space_ref is not None,
            "expected_label_space_ref": expected_label_space_ref,
            "expected_label_space_ref_present": expected_label_space_ref is not None,
            "operational_cause_candidate": operational_cause_candidate,
            "evidence_support_level": support_level,
            "field_status": field_status,
            "repair_proposal": None,
            "taxonomy_delta_proposal": None,
            "review_only": True,
        })

    return rows

def build_context_refs(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    context_refs = sorted({row["taxonomy_context_ref"] for row in rows if row["taxonomy_context_ref"]})
    current_refs = sorted({row["current_label_space_ref"] for row in rows if row["current_label_space_ref"]})
    expected_refs = sorted({row["expected_label_space_ref"] for row in rows if row["expected_label_space_ref"]})
    missing_labels = sorted({row["missing_label_identifier"] for row in rows if row["missing_label_identifier"]})

    return {
        "schema_version": "taxonomy_gap_context_refs_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "row_count": len(rows),
        "taxonomy_context_refs": context_refs,
        "current_label_space_refs": current_refs,
        "expected_label_space_refs": expected_refs,
        "missing_label_identifiers": missing_labels,
        "taxonomy_context_ref_present_count": sum(1 for row in rows if row["taxonomy_context_ref_present"]),
        "current_label_space_ref_present_count": sum(1 for row in rows if row["current_label_space_ref_present"]),
        "expected_label_space_ref_present_count": sum(1 for row in rows if row["expected_label_space_ref_present"]),
        "missing_label_identifier_present_count": sum(1 for row in rows if row["missing_label_identifier_present"]),
        "context_refs_sufficient_for_taxonomy_delta": False,
        "review_only": True,
    }

def build_cause_candidates(rows: List[Dict[str, Any]], context_refs: Dict[str, Any]) -> Dict[str, Any]:
    field_status_counts = dict(sorted(Counter(row["field_status"] for row in rows).items()))
    support_counts = dict(sorted(Counter(row["evidence_support_level"] for row in rows).items()))

    candidates = []
    if context_refs["missing_label_identifier_present_count"] == 0 and context_refs["taxonomy_context_ref_present_count"] == 0:
        candidates.append({
            "candidate_id": "FIELD_EXTRACTION_SURFACE_LACKS_TAXONOMY_GAP_DETAIL",
            "candidate_type": "evidence_gap_not_repair",
            "support_level": "STRONG_FOR_EVIDENCE_GAP",
            "description": "All extracted rows preserve taxonomy-gap pressure identity but omit explicit missing_label_identifier and taxonomy_context_ref fields.",
            "may_support_fixable_pressure": False,
            "may_support_healthy_expected_pressure": False,
            "supports_not_enough_evidence": True,
            "forbidden_inference": "do not treat absent fields as taxonomy delta or extraction repair authorization",
        })
    elif context_refs["missing_label_identifier_present_count"] > 0 and context_refs["taxonomy_context_ref_present_count"] > 0:
        candidates.append({
            "candidate_id": "MISSING_LABEL_FIELD_PRESENT_REQUIRES_REVIEW",
            "candidate_type": "possible_taxonomy_delta_candidate_not_authorized",
            "support_level": "PARTIAL",
            "description": "Some explicit missing label fields and taxonomy context refs are present; review is needed before fixable classification.",
            "may_support_fixable_pressure": True,
            "may_support_healthy_expected_pressure": False,
            "supports_not_enough_evidence": True,
            "forbidden_inference": "do not emit taxonomy upgrade or repair command",
        })
    else:
        candidates.append({
            "candidate_id": "PARTIAL_TAXONOMY_GAP_FIELD_PRESENCE",
            "candidate_type": "partial_evidence_gap",
            "support_level": "PARTIAL",
            "description": "Some taxonomy-gap fields are present but not enough to bind a concrete repair scope.",
            "may_support_fixable_pressure": False,
            "may_support_healthy_expected_pressure": False,
            "supports_not_enough_evidence": True,
            "forbidden_inference": "do not emit taxonomy upgrade or repair command",
        })

    return {
        "schema_version": "taxonomy_gap_operational_cause_candidates_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "field_status_counts": field_status_counts,
        "evidence_support_level_counts": support_counts,
        "candidate_count": len(candidates),
        "candidates": candidates,
        "selected_operational_cause_candidate": candidates[0]["candidate_id"],
        "selected_candidate_support_level": candidates[0]["support_level"],
        "fixable_pressure_supported": any(candidate["may_support_fixable_pressure"] for candidate in candidates) and context_refs["context_refs_sufficient_for_taxonomy_delta"] is True,
        "healthy_expected_pressure_supported": any(candidate["may_support_healthy_expected_pressure"] for candidate in candidates),
        "not_enough_evidence_supported": any(candidate["supports_not_enough_evidence"] for candidate in candidates),
        "repair_objective_proposal_emitted": False,
        "taxonomy_delta_proposal_emitted": False,
        "review_only": True,
    }

def build_reinspection_rollup(rows: List[Dict[str, Any]], context_refs: Dict[str, Any], cause_candidates: Dict[str, Any]) -> Dict[str, Any]:
    all_core_refs_present = all(row.get("source_receipt_ref") and row.get("source_trace_ref") for row in rows)
    all_group_identity_preserved = all(
        row.get("pressure_group_key_hash") == TOP_GROUP_KEY_HASH
        and row.get("parent_pressure_class") == EXPECTED_PARENT_PRESSURE_CLASS
        and row.get("pressure_subtype") == EXPECTED_PRESSURE_SUBTYPE
        and row.get("halt_reason") == EXPECTED_HALT_REASON
        for row in rows
    )

    evidence_sufficiency_class = "EVIDENCE_INSUFFICIENT_NEEDS_FIELD_EXTRACTION"
    if not all_core_refs_present:
        evidence_sufficiency_class = "EVIDENCE_INSUFFICIENT_NEEDS_DEEPER_MEMBERSHIP"
    elif context_refs["missing_label_identifier_present_count"] == 0 or context_refs["taxonomy_context_ref_present_count"] == 0:
        evidence_sufficiency_class = "EVIDENCE_INSUFFICIENT_NEEDS_FIELD_EXTRACTION"
    elif cause_candidates["fixable_pressure_supported"] is True:
        evidence_sufficiency_class = "EVIDENCE_SUFFICIENT_FOR_FIXABLE_CLASSIFICATION"

    classification_after_extraction = "NOT_ENOUGH_EVIDENCE"
    if evidence_sufficiency_class == "EVIDENCE_SUFFICIENT_FOR_FIXABLE_CLASSIFICATION":
        classification_after_extraction = "FIXABLE_PRESSURE"

    return {
        "schema_version": "taxonomy_gap_reinspection_rollup_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "row_count": len(rows),
        "expected_row_count": EXPECTED_TOP_GROUP_COUNT,
        "all_group_identity_preserved": all_group_identity_preserved,
        "all_core_refs_present": all_core_refs_present,
        "missing_label_identifier_present_count": context_refs["missing_label_identifier_present_count"],
        "taxonomy_context_ref_present_count": context_refs["taxonomy_context_ref_present_count"],
        "current_label_space_ref_present_count": context_refs["current_label_space_ref_present_count"],
        "expected_label_space_ref_present_count": context_refs["expected_label_space_ref_present_count"],
        "field_status_counts": cause_candidates["field_status_counts"],
        "selected_operational_cause_candidate": cause_candidates["selected_operational_cause_candidate"],
        "evidence_sufficiency_class_after_extraction": evidence_sufficiency_class,
        "classification_after_extraction": classification_after_extraction,
        "classification_reason": (
            "Extracted source rows still lack explicit missing label identifiers and taxonomy context refs; taxonomy-gap pressure remains not enough evidence."
            if classification_after_extraction == "NOT_ENOUGH_EVIDENCE"
            else "Extracted fields may support a bounded fixable classification, but repair remains human-gated."
        ),
        "repair_objective_proposal_emitted": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "review_only": True,
    }

def build_field_extraction_assessment(rollup: Dict[str, Any], context_refs: Dict[str, Any], cause_candidates: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "taxonomy_gap_field_extraction_assessment_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_evidence_request_id": SOURCE_EVIDENCE_REQUEST_ID,
        "extraction_complete": True,
        "extraction_row_count": rollup["row_count"],
        "evidence_sufficiency_class_before": "EVIDENCE_INSUFFICIENT_NEEDS_FIELD_EXTRACTION",
        "evidence_sufficiency_class_after": rollup["evidence_sufficiency_class_after_extraction"],
        "classification_before": "NOT_ENOUGH_EVIDENCE",
        "classification_after": rollup["classification_after_extraction"],
        "missing_evidence_remaining": [
            field for field, count in [
                ("missing_label_identifier", context_refs["missing_label_identifier_present_count"]),
                ("taxonomy_context_ref", context_refs["taxonomy_context_ref_present_count"]),
                ("current_label_space_ref", context_refs["current_label_space_ref_present_count"]),
                ("expected_label_space_ref", context_refs["expected_label_space_ref_present_count"]),
            ]
            if count == 0
        ],
        "operational_cause_candidate": cause_candidates["selected_operational_cause_candidate"],
        "operational_cause_support_level": cause_candidates["selected_candidate_support_level"],
        "fixable_pressure_supported": rollup["classification_after_extraction"] == "FIXABLE_PRESSURE",
        "healthy_expected_pressure_supported": False,
        "not_enough_evidence_supported": rollup["classification_after_extraction"] == "NOT_ENOUGH_EVIDENCE",
        "repair_proposal_allowed": False,
        "taxonomy_upgrade_allowed": False,
        "taxonomy_delta_proposal_allowed": False,
        "extraction_repair_allowed": False,
        "review_only": True,
    }

def build_reclassification(assessment: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "taxonomy_gap_reclassification_after_field_extraction_v0",
        "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
        "source_evidence_request_id": SOURCE_EVIDENCE_REQUEST_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification_before": assessment["classification_before"],
        "classification_after": assessment["classification_after"],
        "classified_exactly_once": True,
        "evidence_sufficiency_class_before": assessment["evidence_sufficiency_class_before"],
        "evidence_sufficiency_class_after": assessment["evidence_sufficiency_class_after"],
        "classification_reason": (
            "Field extraction completed, but required missing-label/context fields remain absent; the group remains NOT_ENOUGH_EVIDENCE."
            if assessment["classification_after"] == "NOT_ENOUGH_EVIDENCE"
            else "Field extraction produced enough explicit fields for a possible fixable classification, but no repair is executed here."
        ),
        "repair_objective_proposal_emitted": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "extraction_repair_authorized": False,
        "repair_executed": False,
        "build_command_emitted": False,
        "review_only": True,
    }

def build_report(rows: List[Dict[str, Any]], context_refs: Dict[str, Any], cause_candidates: Dict[str, Any], rollup: Dict[str, Any], assessment: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "taxonomy_gap_evidence_extraction_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
            "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
            "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
            "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        },
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "extraction_row_count": len(rows),
        "context_refs_summary": context_refs,
        "operational_cause_candidates_summary": cause_candidates,
        "reinspection_rollup": rollup,
        "field_extraction_assessment": assessment,
        "recommended_next_human_choice": (
            "REQUEST_FIELD_INSTRUMENTATION_OR_MANUAL_FRAGMENT_REVIEW"
            if assessment["classification_after"] == "NOT_ENOUGH_EVIDENCE"
            else "REVIEW_FIXABLE_PRESSURE_OBJECTIVE_PROPOSAL_ELIGIBILITY"
        ),
        "action_executed": False,
        "repair_executed": False,
        "repair_command_emitted": False,
        "repair_objective_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "taxonomy_delta_proposal_emitted": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "extraction_repair_authorized": False,
        "source_mutation": False,
        "hidden_next_command": False,
        "review_only": True,
    }

def build_decision_packet(assessment: Dict[str, Any], rollup: Dict[str, Any]) -> Dict[str, Any]:
    choices = [
        "REQUEST_FIELD_INSTRUMENTATION_OR_MANUAL_FRAGMENT_REVIEW",
        "REQUEST_MORE_REPRESENTATIVE_FRAGMENTS",
        "COMPARE_TOP_TWO_GROUPS_BEFORE_DECISION",
        "MARK_EVIDENCE_BLOCKED_BY_AUTHORITY",
        "REJECT_FIELD_EXTRACTION_RESULT",
    ]
    recommended = "REQUEST_FIELD_INSTRUMENTATION_OR_MANUAL_FRAGMENT_REVIEW"
    if assessment["classification_after"] == "FIXABLE_PRESSURE":
        choices = [
            "REVIEW_FIXABLE_PRESSURE_OBJECTIVE_PROPOSAL_ELIGIBILITY",
            "REQUEST_MANUAL_FRAGMENT_REVIEW_BEFORE_REPAIR_OBJECTIVE",
            "REJECT_FIELD_EXTRACTION_RESULT",
        ]
        recommended = "REVIEW_FIXABLE_PRESSURE_OBJECTIVE_PROPOSAL_ELIGIBILITY"

    return {
        "schema_version": "taxonomy_gap_evidence_extraction_decision_packet_v0",
        "packet_type": "HUMAN_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification_after_extraction": assessment["classification_after"],
        "evidence_sufficiency_class_after": assessment["evidence_sufficiency_class_after"],
        "operational_cause_candidate": assessment["operational_cause_candidate"],
        "missing_evidence_remaining": assessment["missing_evidence_remaining"],
        "allowed_human_choices": choices,
        "recommended_next_handling": recommended,
        "repair_objective_proposal_emitted": False,
        "taxonomy_delta_proposal_emitted": False,
        "may_emit_repair_command": False,
        "may_emit_build_command": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_taxonomy_delta": False,
        "may_authorize_authority_widening": False,
        "may_authorize_optimization": False,
        "may_authorize_extraction_repair": False,
        "may_auto_open_next_group": False,
        "may_advance_without_human_decision": False,
        "terminal_rule": "STOP_HUMAN_DECISION_REQUIRED",
        "review_only": True,
    }

def validate_outputs(rows: List[Dict[str, Any]], context_refs: Dict[str, Any], cause_candidates: Dict[str, Any], rollup: Dict[str, Any], assessment: Dict[str, Any], reclassification: Dict[str, Any], report: Dict[str, Any], packet: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if len(rows) != EXPECTED_TOP_GROUP_COUNT:
        failures.append(f"field_row_count_wrong:{len(rows)}")
    for row in rows:
        if row["pressure_group_key_hash"] != TOP_GROUP_KEY_HASH:
            failures.append("row_group_key_wrong")
        if row["parent_pressure_class"] != EXPECTED_PARENT_PRESSURE_CLASS:
            failures.append("row_parent_wrong")
        if row["pressure_subtype"] != EXPECTED_PRESSURE_SUBTYPE:
            failures.append("row_subtype_wrong")
        if row["halt_reason"] != EXPECTED_HALT_REASON:
            failures.append("row_halt_wrong")
        if not row.get("source_receipt_ref"):
            failures.append("row_missing_source_receipt_ref")
        if not row.get("source_trace_ref"):
            failures.append("row_missing_source_trace_ref")
        if row.get("repair_proposal") is not None:
            failures.append("row_repair_proposal_present")
        if row.get("taxonomy_delta_proposal") is not None:
            failures.append("row_taxonomy_delta_proposal_present")

    if context_refs["row_count"] != EXPECTED_TOP_GROUP_COUNT:
        failures.append("context_row_count_wrong")
    if context_refs["context_refs_sufficient_for_taxonomy_delta"] is not False:
        failures.append("context_refs_wrongly_sufficient_for_taxonomy_delta")

    if cause_candidates["candidate_count"] < 1:
        failures.append("cause_candidate_missing")
    if cause_candidates["repair_objective_proposal_emitted"] is not False:
        failures.append("cause_candidate_repair_proposal_emitted")
    if cause_candidates["taxonomy_delta_proposal_emitted"] is not False:
        failures.append("cause_candidate_taxonomy_delta_proposal_emitted")

    if rollup["row_count"] != EXPECTED_TOP_GROUP_COUNT:
        failures.append("rollup_row_count_wrong")
    if rollup["all_group_identity_preserved"] is not True:
        failures.append("group_identity_not_preserved")
    if rollup["all_core_refs_present"] is not True:
        failures.append("core_refs_not_present")
    if rollup["evidence_sufficiency_class_after_extraction"] not in VALID_EVIDENCE_CLASSES:
        failures.append("invalid_evidence_class_after")
    if rollup["classification_after_extraction"] not in {"NOT_ENOUGH_EVIDENCE", "FIXABLE_PRESSURE"}:
        failures.append("invalid_classification_after")
    if rollup["repair_objective_proposal_emitted"] is not False:
        failures.append("rollup_repair_proposal_emitted")
    if rollup["taxonomy_delta_proposal_emitted"] is not False:
        failures.append("rollup_taxonomy_delta_proposal_emitted")
    if rollup["taxonomy_upgrade_authorized"] is not False:
        failures.append("rollup_taxonomy_upgrade_authorized")

    if assessment["extraction_complete"] is not True:
        failures.append("assessment_extraction_not_complete")
    if assessment["extraction_row_count"] != EXPECTED_TOP_GROUP_COUNT:
        failures.append("assessment_row_count_wrong")
    if assessment["repair_proposal_allowed"] is not False:
        failures.append("assessment_repair_allowed")
    if assessment["taxonomy_upgrade_allowed"] is not False:
        failures.append("assessment_taxonomy_upgrade_allowed")
    if assessment["taxonomy_delta_proposal_allowed"] is not False:
        failures.append("assessment_taxonomy_delta_allowed")
    if assessment["extraction_repair_allowed"] is not False:
        failures.append("assessment_extraction_repair_allowed")

    if reclassification["classified_exactly_once"] is not True:
        failures.append("reclassification_not_exactly_once")
    if reclassification["repair_objective_proposal_emitted"] is not False:
        failures.append("reclassification_repair_proposal_emitted")
    if reclassification["taxonomy_delta_proposal_emitted"] is not False:
        failures.append("reclassification_taxonomy_delta_proposal_emitted")
    if reclassification["taxonomy_upgrade_authorized"] is not False:
        failures.append("reclassification_taxonomy_upgrade_authorized")
    if reclassification["build_command_emitted"] is not False:
        failures.append("reclassification_build_command_emitted")

    for key in [
        "action_executed",
        "repair_executed",
        "repair_command_emitted",
        "repair_objective_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "taxonomy_delta_proposal_emitted",
        "authority_widening_authorized",
        "optimization_authorized",
        "extraction_repair_authorized",
        "source_mutation",
        "hidden_next_command",
    ]:
        if report.get(key) is not False:
            failures.append(f"report_guard_not_false:{key}:{report.get(key)}")

    if packet["packet_type"] != "HUMAN_REVIEW_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    for key in [
        "may_emit_repair_command",
        "may_emit_build_command",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_taxonomy_delta",
        "may_authorize_authority_widening",
        "may_authorize_optimization",
        "may_authorize_extraction_repair",
        "may_auto_open_next_group",
        "may_advance_without_human_decision",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_loop_application_receipt_id") != SOURCE_LOOP_APPLICATION_RECEIPT_ID:
        failures.append("source_loop_application_wrong")
    if receipt.get("source_evidence_request_id") != SOURCE_EVIDENCE_REQUEST_ID:
        failures.append("source_evidence_request_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "TAX_GAP_EXTRACT_0_SOURCE_SURFACE_VERIFIED",
        "TAX_GAP_EXTRACT_1_EVIDENCE_REQUEST_VERIFIED",
        "TAX_GAP_EXTRACT_2_FULL_GROUP_MEMBERSHIP_CONSUMED",
        "TAX_GAP_EXTRACT_3_FIELD_ROWS_EMITTED",
        "TAX_GAP_EXTRACT_4_CONTEXT_REFS_EMITTED",
        "TAX_GAP_EXTRACT_5_CAUSE_CANDIDATES_EMITTED",
        "TAX_GAP_EXTRACT_6_REINSPECTION_ROLLUP_EMITTED",
        "TAX_GAP_EXTRACT_7_FIELD_EXTRACTION_ASSESSED",
        "TAX_GAP_EXTRACT_8_RECLASSIFICATION_EMITTED",
        "TAX_GAP_EXTRACT_9_DECISION_PACKET_EMITTED",
        "TAX_GAP_EXTRACT_10_NO_REPAIR_OR_TAXONOMY_ACTION",
        "TAX_GAP_EXTRACT_11_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("field_row_count") != EXPECTED_TOP_GROUP_COUNT:
        failures.append("metric_field_row_count_wrong")
    if metrics.get("evidence_sufficiency_class_after") not in VALID_EVIDENCE_CLASSES:
        failures.append("metric_evidence_class_invalid")
    if metrics.get("classification_after_extraction") not in {"NOT_ENOUGH_EVIDENCE", "FIXABLE_PRESSURE"}:
        failures.append("metric_classification_invalid")
    for key in [
        "repair_command_emitted_count",
        "build_command_emitted_count",
        "repair_executed_count",
        "repair_objective_proposal_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "authority_widening_authorized_count",
        "optimization_authorized_count",
        "extraction_repair_authorized_count",
        "source_mutation_count",
        "hidden_next_command_count",
        "next_group_auto_opened_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("taxonomy_gap_extraction_guards", {})
    for key in [
        "source_surface_verified",
        "evidence_request_verified",
        "full_group_membership_consumed",
        "field_rows_emitted",
        "context_refs_emitted",
        "cause_candidates_emitted",
        "reinspection_rollup_emitted",
        "field_extraction_assessed",
        "reclassification_emitted",
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
        "optimization_authorized",
        "extraction_repair_authorized",
        "source_mutation",
        "hidden_next_command",
        "next_group_auto_opened",
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
    context_refs = build_context_refs(field_rows)
    cause_candidates = build_cause_candidates(field_rows, context_refs)
    reinspection_rollup = build_reinspection_rollup(field_rows, context_refs, cause_candidates)
    assessment = build_field_extraction_assessment(reinspection_rollup, context_refs, cause_candidates)
    reclassification = build_reclassification(assessment)
    report = build_report(field_rows, context_refs, cause_candidates, reinspection_rollup, assessment)
    packet = build_decision_packet(assessment, reinspection_rollup)

    write_jsonl(FIELD_ROWS_PATH, field_rows)
    write_json(CONTEXT_REFS_PATH, context_refs)
    write_json(CAUSE_CANDIDATES_PATH, cause_candidates)
    write_json(REINSPECTION_ROLLUP_PATH, reinspection_rollup)
    write_json(FIELD_EXTRACTION_ASSESSMENT_PATH, assessment)
    write_json(RECLASSIFICATION_PATH, reclassification)
    write_json(EVIDENCE_EXTRACTION_REPORT_PATH, report)
    write_json(EVIDENCE_EXTRACTION_DECISION_PACKET_PATH, packet)

    failures.extend(validate_outputs(field_rows, context_refs, cause_candidates, reinspection_rollup, assessment, reclassification, report, packet))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "TAX_GAP_EXTRACT_0_SOURCE_SURFACE_VERIFIED": len(validate_sources(sources)) == 0,
        "TAX_GAP_EXTRACT_1_EVIDENCE_REQUEST_VERIFIED": sources["evidence_request"]["evidence_request_id"] == SOURCE_EVIDENCE_REQUEST_ID,
        "TAX_GAP_EXTRACT_2_FULL_GROUP_MEMBERSHIP_CONSUMED": len(sources["taxonomy_gap_full_membership"]) == EXPECTED_TOP_GROUP_COUNT,
        "TAX_GAP_EXTRACT_3_FIELD_ROWS_EMITTED": FIELD_ROWS_PATH.exists() and len(field_rows) == EXPECTED_TOP_GROUP_COUNT,
        "TAX_GAP_EXTRACT_4_CONTEXT_REFS_EMITTED": CONTEXT_REFS_PATH.exists(),
        "TAX_GAP_EXTRACT_5_CAUSE_CANDIDATES_EMITTED": CAUSE_CANDIDATES_PATH.exists(),
        "TAX_GAP_EXTRACT_6_REINSPECTION_ROLLUP_EMITTED": REINSPECTION_ROLLUP_PATH.exists(),
        "TAX_GAP_EXTRACT_7_FIELD_EXTRACTION_ASSESSED": FIELD_EXTRACTION_ASSESSMENT_PATH.exists(),
        "TAX_GAP_EXTRACT_8_RECLASSIFICATION_EMITTED": RECLASSIFICATION_PATH.exists(),
        "TAX_GAP_EXTRACT_9_DECISION_PACKET_EMITTED": EVIDENCE_EXTRACTION_DECISION_PACKET_PATH.exists(),
        "TAX_GAP_EXTRACT_10_NO_REPAIR_OR_TAXONOMY_ACTION": report["repair_executed"] is False and report["taxonomy_upgrade_authorized"] is False and report["taxonomy_delta_proposal_emitted"] is False,
        "TAX_GAP_EXTRACT_11_NO_SOURCE_MUTATION": source_mutation_detected is False,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {"type": "STOP", "stop_code": "STOP_HUMAN_DECISION_REQUIRED", "next_command_goal": None}
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if any([
        report["repair_executed"],
        report["repair_command_emitted"],
        report["taxonomy_upgrade_authorized"],
        report["taxonomy_delta_proposal_emitted"],
        report["authority_widening_authorized"],
        report["optimization_authorized"],
        report["extraction_repair_authorized"],
        packet["may_emit_build_command"],
        packet["may_emit_repair_command"],
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
        "source_evidence_request_id": SOURCE_EVIDENCE_REQUEST_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "field_row_count": len(field_rows),
        "expected_field_row_count": EXPECTED_TOP_GROUP_COUNT,
        "missing_label_identifier_present_count": context_refs["missing_label_identifier_present_count"],
        "taxonomy_context_ref_present_count": context_refs["taxonomy_context_ref_present_count"],
        "current_label_space_ref_present_count": context_refs["current_label_space_ref_present_count"],
        "expected_label_space_ref_present_count": context_refs["expected_label_space_ref_present_count"],
        "selected_operational_cause_candidate": cause_candidates["selected_operational_cause_candidate"],
        "selected_candidate_support_level": cause_candidates["selected_candidate_support_level"],
        "evidence_sufficiency_class_before": assessment["evidence_sufficiency_class_before"],
        "evidence_sufficiency_class_after": assessment["evidence_sufficiency_class_after"],
        "classification_before": assessment["classification_before"],
        "classification_after_extraction": assessment["classification_after"],
        "missing_evidence_remaining_count": len(assessment["missing_evidence_remaining"]),
        "repair_command_emitted_count": 0,
        "build_command_emitted_count": 0,
        "repair_executed_count": 0,
        "repair_objective_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "authority_widening_authorized_count": 0,
        "optimization_authorized_count": 0,
        "extraction_repair_authorized_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "hidden_next_command_count": 0,
        "next_group_auto_opened_count": 0,
        "review_only": True,
    }

    guards = {
        "source_surface_verified": len(validate_sources(sources)) == 0,
        "evidence_request_verified": True,
        "full_group_membership_consumed": True,
        "field_rows_emitted": True,
        "context_refs_emitted": True,
        "cause_candidates_emitted": True,
        "reinspection_rollup_emitted": True,
        "field_extraction_assessed": True,
        "reclassification_emitted": True,
        "decision_packet_emitted": True,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "repair_executed": False,
        "repair_objective_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "taxonomy_delta_proposal_emitted": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "extraction_repair_authorized": False,
        "source_mutation": source_mutation_detected,
        "hidden_next_command": False,
        "next_group_auto_opened": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "loop_application_receipt": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
        "evidence_request_id": SOURCE_EVIDENCE_REQUEST_ID,
        "classification_after": assessment["classification_after"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "taxonomy_gap_missing_label_field_rows": rel(FIELD_ROWS_PATH),
        "taxonomy_gap_context_refs": rel(CONTEXT_REFS_PATH),
        "taxonomy_gap_operational_cause_candidates": rel(CAUSE_CANDIDATES_PATH),
        "taxonomy_gap_reinspection_rollup": rel(REINSPECTION_ROLLUP_PATH),
        "taxonomy_gap_field_extraction_assessment": rel(FIELD_EXTRACTION_ASSESSMENT_PATH),
        "taxonomy_gap_reclassification_after_field_extraction": rel(RECLASSIFICATION_PATH),
        "taxonomy_gap_evidence_extraction_report": rel(EVIDENCE_EXTRACTION_REPORT_PATH),
        "taxonomy_gap_evidence_extraction_decision_packet": rel(EVIDENCE_EXTRACTION_DECISION_PACKET_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "taxonomy_gap_missing_label_evidence_extraction_receipt_v0",
        "receipt_type": "TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_EXTRACTION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
        "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "source_evidence_request_id": SOURCE_EVIDENCE_REQUEST_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "extraction_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "field_row_count": len(field_rows),
            "evidence_sufficiency_class_after": assessment["evidence_sufficiency_class_after"],
            "classification_after_extraction": assessment["classification_after"],
            "selected_operational_cause_candidate": cause_candidates["selected_operational_cause_candidate"],
            "missing_evidence_remaining": assessment["missing_evidence_remaining"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "taxonomy_gap_extraction_guards": guards,
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
    print(f"taxonomy_gap_missing_label_evidence_extraction_receipt_id={receipt_id}")
    print(f"taxonomy_gap_missing_label_evidence_extraction_receipt_path=data/pressure_loop_applications/r1000_top_group_taxonomy_gap_evidence_extraction_v0_receipts/{receipt_id}.json")
    print(f"taxonomy_gap_missing_label_field_rows_path=data/pressure_loop_applications/r1000_top_group_taxonomy_gap_evidence_extraction_v0/taxonomy_gap_missing_label_field_rows.jsonl")
    print(f"taxonomy_gap_evidence_extraction_decision_packet_path=data/pressure_loop_applications/r1000_top_group_taxonomy_gap_evidence_extraction_v0/taxonomy_gap_evidence_extraction_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
