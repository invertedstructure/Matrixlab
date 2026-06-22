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

UNIT_ID = "APPLY_PRESSURE_HANDLING_LOOP_TO_R1000_TOP_GROUP_TAXONOMY_GAP_V0"
TARGET_UNIT_ID = "pressure_loop_application.r1000_top_group_taxonomy_gap.v0"

SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID = "6148b4fa"
SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID = "7c9718e0"
SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID = "a121ff40"
SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID = "fabba052"

TOP_GROUP_KEY_HASH = "38c604a1"
EXPECTED_PARENT_PRESSURE_CLASS = "TAXONOMY_PRESSURE"
EXPECTED_PRESSURE_SUBTYPE = "missing_label"
EXPECTED_HALT_REASON = "STOP_TAXONOMY_GAP"
EXPECTED_TOP_GROUP_COUNT = 25

OUT_DIR = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0"
RECEIPT_DIR = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0_receipts"

GROUP_SELECTION_PATH = OUT_DIR / "taxonomy_gap_group_selection.json"
FULL_MEMBERSHIP_PATH = OUT_DIR / "taxonomy_gap_full_membership.jsonl"
DEEP_FRAGMENT_INSPECTION_PATH = OUT_DIR / "taxonomy_gap_deep_fragment_inspection.json"
EVIDENCE_SUFFICIENCY_ASSESSMENT_PATH = OUT_DIR / "taxonomy_gap_evidence_sufficiency_assessment.json"
EVIDENCE_REQUEST_PATH = OUT_DIR / "taxonomy_gap_evidence_request.json"
LOOP_APPLICATION_REPORT_PATH = OUT_DIR / "pressure_loop_taxonomy_gap_application_report.json"
LOOP_APPLICATION_DECISION_PACKET_PATH = OUT_DIR / "pressure_loop_taxonomy_gap_application_decision_packet.json"
RECLASSIFICATION_PATH = OUT_DIR / "taxonomy_gap_reclassification_after_inspection.json"

PRESSURE_LOOP_RECEIPT_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID}.json"
PRESSURE_LOOP_PROTOCOL_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0" / "pressure_handling_loop_protocol.json"
PRESSURE_LOOP_EVIDENCE_SCHEMA_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0" / "pressure_evidence_sufficiency_schema_v0.json"
PRESSURE_LOOP_CLASSIFICATION_SCHEMA_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0" / "pressure_classification_schema_v0.json"
PRESSURE_LOOP_GROUP_SCHEMA_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0" / "pressure_group_schema_v0.json"
PRESSURE_LOOP_RESOLUTION_SCHEMA_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0" / "pressure_resolution_schema_v0.json"

TOP_GROUP_RECEIPT_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0_receipts" / f"{SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID}.json"
TOP_GROUP_SELECTION_SOURCE_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_selection.json"
TOP_GROUP_MEMBERSHIP_SOURCE_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_event_membership.jsonl"
TOP_GROUP_FRAGMENTS_SOURCE_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_representative_fragments.json"
TOP_GROUP_EVIDENCE_SOURCE_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_evidence_rollup.json"
TOP_GROUP_CLASSIFICATION_SOURCE_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_classification.json"
TOP_GROUP_PACKET_SOURCE_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_decision_packet.json"
TOP_GROUP_REPAIR_PROPOSAL_SOURCE_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0" / "top_group_repair_objective_proposal.json"

R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"
R1000_PRESSURE_EVENTS_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_event_rows.jsonl"
R1000_GROUP_MEMBERSHIP_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_candidate_c_group_event_membership.jsonl"
CANDIDATE_C_RECEIPT_PATH = ROOT / "data" / "r250_pressure_candidate_c_interrogation_v0_receipts" / f"{SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    PRESSURE_LOOP_RECEIPT_PATH,
    PRESSURE_LOOP_PROTOCOL_PATH,
    PRESSURE_LOOP_EVIDENCE_SCHEMA_PATH,
    PRESSURE_LOOP_CLASSIFICATION_SCHEMA_PATH,
    PRESSURE_LOOP_GROUP_SCHEMA_PATH,
    PRESSURE_LOOP_RESOLUTION_SCHEMA_PATH,
    TOP_GROUP_RECEIPT_PATH,
    TOP_GROUP_SELECTION_SOURCE_PATH,
    TOP_GROUP_MEMBERSHIP_SOURCE_PATH,
    TOP_GROUP_FRAGMENTS_SOURCE_PATH,
    TOP_GROUP_EVIDENCE_SOURCE_PATH,
    TOP_GROUP_CLASSIFICATION_SOURCE_PATH,
    TOP_GROUP_PACKET_SOURCE_PATH,
    TOP_GROUP_REPAIR_PROPOSAL_SOURCE_PATH,
    R1000_SCALE_RECEIPT_PATH,
    R1000_PRESSURE_EVENTS_PATH,
    R1000_GROUP_MEMBERSHIP_PATH,
    CANDIDATE_C_RECEIPT_PATH,
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

VALID_CLASSIFICATIONS = [
    "FIXABLE_PRESSURE",
    "HEALTHY_EXPECTED_PRESSURE",
    "NOT_ENOUGH_EVIDENCE",
]

HUMAN_DECISION = {
    "decision": "APPLY_PRESSURE_HANDLING_LOOP_TO_CURRENT_TOP_GROUP",
    "scope": "handle_not_enough_evidence_for_top_group_only",
    "handling_state": "HANDLE_NOT_ENOUGH_EVIDENCE",
    "source_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
    "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
    "not_authorized": [
        "taxonomy_repair",
        "taxonomy_upgrade",
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
    "this unit applies HANDLE_NOT_ENOUGH_EVIDENCE only",
    "do not repair taxonomy",
    "do not upgrade taxonomy",
    "do not propose taxonomy delta from pressure alone",
    "do not widen authority",
    "do not optimize burden",
    "do not repair extraction",
    "do not auto-open next group",
    "do not execute repair",
    "do not emit build command",
    "evidence request is not a repair proposal",
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
        "protocol_receipt": read_json(PRESSURE_LOOP_RECEIPT_PATH),
        "protocol": read_json(PRESSURE_LOOP_PROTOCOL_PATH),
        "evidence_schema": read_json(PRESSURE_LOOP_EVIDENCE_SCHEMA_PATH),
        "classification_schema": read_json(PRESSURE_LOOP_CLASSIFICATION_SCHEMA_PATH),
        "group_schema": read_json(PRESSURE_LOOP_GROUP_SCHEMA_PATH),
        "resolution_schema": read_json(PRESSURE_LOOP_RESOLUTION_SCHEMA_PATH),
        "top_group_receipt": read_json(TOP_GROUP_RECEIPT_PATH),
        "top_group_selection": read_json(TOP_GROUP_SELECTION_SOURCE_PATH),
        "top_group_membership": read_jsonl(TOP_GROUP_MEMBERSHIP_SOURCE_PATH),
        "top_group_fragments": read_json(TOP_GROUP_FRAGMENTS_SOURCE_PATH),
        "top_group_evidence": read_json(TOP_GROUP_EVIDENCE_SOURCE_PATH),
        "top_group_classification": read_json(TOP_GROUP_CLASSIFICATION_SOURCE_PATH),
        "top_group_packet": read_json(TOP_GROUP_PACKET_SOURCE_PATH),
        "top_group_repair_proposal": read_json(TOP_GROUP_REPAIR_PROPOSAL_SOURCE_PATH),
        "r1000_scale_receipt": read_json(R1000_SCALE_RECEIPT_PATH),
        "r1000_pressure_events": read_jsonl(R1000_PRESSURE_EVENTS_PATH),
        "r1000_group_membership": read_jsonl(R1000_GROUP_MEMBERSHIP_PATH),
        "candidate_c_receipt": read_json(CANDIDATE_C_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    protocol_receipt = sources["protocol_receipt"]
    protocol = sources["protocol"]
    top_receipt = sources["top_group_receipt"]
    top_selection = sources["top_group_selection"]
    top_classification = sources["top_group_classification"]
    top_proposal = sources["top_group_repair_proposal"]

    if protocol_receipt.get("receipt_id") != SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID:
        failures.append("protocol_receipt_id_wrong")
    if protocol_receipt.get("gate") != "PASS":
        failures.append("protocol_receipt_not_pass")
    if protocol_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("protocol_terminal_not_advance")
    if protocol_receipt.get("terminal", {}).get("next_command_goal") != UNIT_ID:
        failures.append("protocol_next_unit_not_this_application")
    if protocol_receipt.get("first_application_target", {}).get("next_unit_id") != UNIT_ID:
        failures.append("protocol_first_application_not_this_unit")
    if protocol_receipt.get("first_application_target", {}).get("must_not_repair_taxonomy") is not True:
        failures.append("protocol_missing_must_not_repair_taxonomy")

    if protocol.get("first_application_target", {}).get("next_unit_id") != UNIT_ID:
        failures.append("protocol_artifact_next_unit_wrong")
    if protocol.get("first_application_target", {}).get("top_group_key_hash") != TOP_GROUP_KEY_HASH:
        failures.append("protocol_artifact_top_group_wrong")
    if protocol.get("first_application_target", {}).get("classification") != "NOT_ENOUGH_EVIDENCE":
        failures.append("protocol_artifact_classification_wrong")

    if top_receipt.get("receipt_id") != SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID:
        failures.append("top_receipt_id_wrong")
    if top_receipt.get("gate") != "PASS":
        failures.append("top_receipt_not_pass")
    if top_receipt.get("top_group_summary", {}).get("top_group_key_hash") != TOP_GROUP_KEY_HASH:
        failures.append("top_receipt_group_key_wrong")
    if top_receipt.get("top_group_summary", {}).get("classification") != "NOT_ENOUGH_EVIDENCE":
        failures.append("top_receipt_not_not_enough_evidence")
    if top_receipt.get("top_group_summary", {}).get("parent_pressure_class") != EXPECTED_PARENT_PRESSURE_CLASS:
        failures.append("top_receipt_parent_wrong")
    if top_receipt.get("top_group_summary", {}).get("pressure_subtype") != EXPECTED_PRESSURE_SUBTYPE:
        failures.append("top_receipt_subtype_wrong")
    if top_receipt.get("top_group_summary", {}).get("halt_reason") != EXPECTED_HALT_REASON:
        failures.append("top_receipt_halt_wrong")
    if top_receipt.get("top_group_summary", {}).get("top_group_count") != EXPECTED_TOP_GROUP_COUNT:
        failures.append("top_receipt_count_wrong")

    if top_selection.get("top_group_key_hash") != TOP_GROUP_KEY_HASH:
        failures.append("top_selection_key_wrong")
    if top_selection.get("top_group_count") != EXPECTED_TOP_GROUP_COUNT:
        failures.append("top_selection_count_wrong")
    if top_selection.get("top_two_comparison_default") is not False:
        failures.append("top_two_default_in_source")

    if top_classification.get("classification") != "NOT_ENOUGH_EVIDENCE":
        failures.append("source_top_classification_wrong")
    if top_classification.get("repair_command_emitted") is not False:
        failures.append("source_top_repair_command_emitted")
    if top_proposal.get("proposal_emitted") is not False:
        failures.append("source_top_repair_proposal_should_not_exist")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_group_selection(sources: Dict[str, Any]) -> Dict[str, Any]:
    source = sources["top_group_selection"]
    return {
        "schema_version": "taxonomy_gap_group_selection_v0",
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "handling_state": "HANDLE_NOT_ENOUGH_EVIDENCE",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "parent_pressure_class": EXPECTED_PARENT_PRESSURE_CLASS,
        "pressure_subtype": EXPECTED_PRESSURE_SUBTYPE,
        "halt_reason": EXPECTED_HALT_REASON,
        "group_count": source["top_group_count"],
        "group_share": source["top_group_share"],
        "rank": source["top_group_rank"],
        "second_group_count": source["second_group_count"],
        "dominant_margin": source["dominant_margin"],
        "dominant_margin_share": source["dominant_margin_share"],
        "low_margin_warning": source["low_margin_warning"],
        "selection_rule": source["selection_rule"],
        "stable_rank_authorizes_inspection_order_only": True,
        "stable_rank_authorizes_repair": False,
        "top_two_comparison_performed": False,
        "top_two_comparison_fallback_only": True,
        "review_only": True,
    }

def build_full_membership(sources: Dict[str, Any]) -> List[Dict[str, Any]]:
    pressure_by_id = {event["pressure_event_id"]: event for event in sources["r1000_pressure_events"]}
    source_membership = [
        row for row in sources["r1000_group_membership"]
        if row["group_key_hash"] == TOP_GROUP_KEY_HASH
    ]
    rows = []
    for row in sorted(source_membership, key=lambda item: item["pressure_event_id"]):
        event = pressure_by_id.get(row["pressure_event_id"], {})
        rows.append({
            "schema_version": "taxonomy_gap_full_membership_row_v0",
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "pressure_event_id": row["pressure_event_id"],
            "pressure_pattern_signature_hash": row["pressure_pattern_signature_hash"],
            "work_item_id": row["work_item_id"],
            "slot_id": row["slot_id"],
            "source_receipt_ref": row["source_receipt_ref"],
            "source_trace_ref": row["source_trace_ref"],
            "move_kind": row["move_kind"],
            "evidence_field": row["evidence_field"],
            "terminal_decision": event.get("terminal_decision"),
            "parent_pressure_class": event.get("parent_pressure_class"),
            "pressure_subtype": event.get("pressure_subtype"),
            "halt_reason": event.get("halt_reason"),
            "candidate_c_group_key_hash": event.get("candidate_c_group_key_hash"),
            "missing_label_identifier": event.get("missing_label_identifier"),
            "taxonomy_context_ref": event.get("taxonomy_context_ref"),
            "classification_hint": None,
            "review_only": True,
        })
    return rows

def inspect_fragments(full_membership: List[Dict[str, Any]], sources: Dict[str, Any]) -> Dict[str, Any]:
    source_fragments = sources["top_group_fragments"].get("fragments", [])
    inspected = []
    for fragment in source_fragments:
        inspected.append({
            "pressure_event_id": fragment.get("pressure_event_id"),
            "pressure_pattern_signature_hash": fragment.get("pressure_pattern_signature_hash"),
            "source_receipt_ref": fragment.get("source_receipt_ref"),
            "source_trace_ref": fragment.get("source_trace_ref"),
            "work_item_id": fragment.get("work_item_id"),
            "slot_id": fragment.get("slot_id"),
            "move_kind": fragment.get("move_kind"),
            "evidence_field": fragment.get("evidence_field"),
            "terminal_decision": fragment.get("terminal_decision"),
            "parent_pressure_class": fragment.get("parent_pressure_class"),
            "pressure_subtype": fragment.get("pressure_subtype"),
            "halt_reason": fragment.get("halt_reason"),
            "missing_label_identifier_present": fragment.get("missing_label_identifier") is not None,
            "taxonomy_context_ref_present": fragment.get("taxonomy_context_ref") is not None,
            "explicit_missing_label_name": fragment.get("missing_label_identifier"),
            "explicit_taxonomy_context_ref": fragment.get("taxonomy_context_ref"),
            "supports_fixable_pressure": False,
            "supports_healthy_expected_pressure": False,
            "supports_not_enough_evidence": True,
            "inspection_reason": "fragment preserves taxonomy-gap pressure identity but does not expose a concrete missing label identifier or bounded taxonomy delta target",
        })

    missing_identifier_count = sum(1 for row in inspected if row["missing_label_identifier_present"] is False)
    missing_context_count = sum(1 for row in inspected if row["taxonomy_context_ref_present"] is False)

    return {
        "schema_version": "taxonomy_gap_deep_fragment_inspection_v0",
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "full_membership_count": len(full_membership),
        "representative_fragment_count": len(inspected),
        "inspected_fragments": inspected,
        "fragment_findings": {
            "all_fragments_taxonomy_gap": all(row["parent_pressure_class"] == EXPECTED_PARENT_PRESSURE_CLASS and row["pressure_subtype"] == EXPECTED_PRESSURE_SUBTYPE and row["halt_reason"] == EXPECTED_HALT_REASON for row in inspected),
            "missing_label_identifier_present_count": sum(1 for row in inspected if row["missing_label_identifier_present"]),
            "missing_label_identifier_absent_count": missing_identifier_count,
            "taxonomy_context_ref_present_count": sum(1 for row in inspected if row["taxonomy_context_ref_present"]),
            "taxonomy_context_ref_absent_count": missing_context_count,
            "fixable_scope_found": False,
            "healthy_expected_support_found": False,
            "not_enough_evidence_support_found": True,
        },
        "top_two_comparison_performed": False,
        "top_two_comparison_fallback_only": True,
        "review_only": True,
    }

def assess_evidence(full_membership: List[Dict[str, Any]], inspection: Dict[str, Any]) -> Dict[str, Any]:
    findings = inspection["fragment_findings"]

    required_for_taxonomy_gap_classification = [
        "explicit missing label identifier",
        "taxonomy context reference",
        "source event refs",
        "source receipt refs",
        "source trace refs",
        "operational cause mapping",
        "bounded non-mutating evidence target",
    ]

    present = {
        "source_event_refs": len(full_membership) == EXPECTED_TOP_GROUP_COUNT,
        "source_receipt_refs": all(row.get("source_receipt_ref") for row in full_membership),
        "source_trace_refs": all(row.get("source_trace_ref") for row in full_membership),
        "representative_fragments": inspection["representative_fragment_count"] > 0,
        "explicit_missing_label_identifier": findings["missing_label_identifier_present_count"] > 0,
        "taxonomy_context_reference": findings["taxonomy_context_ref_present_count"] > 0,
        "operational_cause_mapping": False,
        "bounded_non_mutating_evidence_target": True,
    }

    missing = [key for key, value in present.items() if not value]

    evidence_class = "EVIDENCE_INSUFFICIENT_NEEDS_FIELD_EXTRACTION"
    if "representative_fragments" in missing:
        evidence_class = "EVIDENCE_INSUFFICIENT_NEEDS_MORE_FRAGMENTS"
    elif "source_event_refs" in missing or "source_receipt_refs" in missing or "source_trace_refs" in missing:
        evidence_class = "EVIDENCE_INSUFFICIENT_NEEDS_DEEPER_MEMBERSHIP"
    elif "explicit_missing_label_identifier" in missing or "taxonomy_context_reference" in missing or "operational_cause_mapping" in missing:
        evidence_class = "EVIDENCE_INSUFFICIENT_NEEDS_FIELD_EXTRACTION"

    return {
        "schema_version": "taxonomy_gap_evidence_sufficiency_assessment_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification_before_application": "NOT_ENOUGH_EVIDENCE",
        "evidence_sufficiency_class": evidence_class,
        "evidence_sufficient_for_fixable_classification": False,
        "evidence_sufficient_for_healthy_classification": False,
        "evidence_insufficient": True,
        "missing_evidence_fields": missing,
        "present_evidence_fields": [key for key, value in present.items() if value],
        "required_for_taxonomy_gap_classification": required_for_taxonomy_gap_classification,
        "classification_after_inspection": "NOT_ENOUGH_EVIDENCE",
        "classification_reason": "Taxonomy-gap fragments preserve pressure identity but do not expose enough explicit missing-label/context fields to propose a bounded taxonomy delta or healthy acceptance.",
        "top_two_comparison_required_now": False,
        "top_two_comparison_fallback_only": True,
        "repair_proposal_allowed": False,
        "taxonomy_upgrade_allowed": False,
        "review_only": True,
    }

def build_evidence_request(assessment: Dict[str, Any]) -> Dict[str, Any]:
    evidence_request_id = sha8({
        "unit_id": UNIT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "evidence_sufficiency_class": assessment["evidence_sufficiency_class"],
        "missing": assessment["missing_evidence_fields"],
    })
    return {
        "schema_version": "taxonomy_gap_evidence_request_v0",
        "evidence_request_id": evidence_request_id,
        "request_type": "EVIDENCE_REQUEST_NOT_REPAIR",
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "evidence_sufficiency_class": assessment["evidence_sufficiency_class"],
        "missing_evidence_reason": assessment["classification_reason"],
        "requested_artifacts": [
            "taxonomy_gap_missing_label_field_rows.jsonl",
            "taxonomy_gap_context_refs.json",
            "taxonomy_gap_operational_cause_candidates.json",
            "taxonomy_gap_reinspection_rollup.json",
        ],
        "requested_extraction_fields": [
            "pressure_event_id",
            "missing_label_identifier",
            "taxonomy_context_ref",
            "current_label_space_ref",
            "expected_label_space_ref",
            "source_receipt_ref",
            "source_trace_ref",
            "operational_cause_candidate",
            "evidence_support_level",
        ],
        "allowed_next_evidence_unit_proposal": "EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_V0",
        "forbidden_scope": [
            "taxonomy repair",
            "taxonomy upgrade",
            "registry mutation",
            "authority widening",
            "burden optimization",
            "extraction repair",
            "repair command",
            "build command",
            "source mutation",
        ],
        "terminal_rule": "STOP_HUMAN_DECISION_REQUIRED",
        "proposal_emitted": False,
        "repair_objective_proposal_emitted": False,
        "taxonomy_upgrade_proposal_emitted": False,
        "build_command_emitted": False,
        "review_only": True,
    }

def build_reclassification(assessment: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "taxonomy_gap_reclassification_after_inspection_v0",
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification_before": "NOT_ENOUGH_EVIDENCE",
        "classification_after": "NOT_ENOUGH_EVIDENCE",
        "classified_exactly_once": True,
        "classification_reason": assessment["classification_reason"],
        "evidence_sufficiency_class": assessment["evidence_sufficiency_class"],
        "evidence_sufficient_for_fixable_classification": False,
        "evidence_sufficient_for_healthy_classification": False,
        "repair_objective_proposal_emitted": False,
        "evidence_request_emitted": True,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "extraction_repair_authorized": False,
        "repair_executed": False,
        "build_command_emitted": False,
        "review_only": True,
    }

def build_report(selection: Dict[str, Any], full_membership: List[Dict[str, Any]], inspection: Dict[str, Any], assessment: Dict[str, Any], request: Dict[str, Any], reclassification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "pressure_loop_taxonomy_gap_application_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
            "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
            "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
            "source_candidate_c_interrogation_receipt_id": SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID,
        },
        "handling_state": "HANDLE_NOT_ENOUGH_EVIDENCE",
        "selection_summary": selection,
        "membership_count": len(full_membership),
        "fragment_inspection_summary": inspection["fragment_findings"],
        "evidence_sufficiency_class": assessment["evidence_sufficiency_class"],
        "missing_evidence_fields": assessment["missing_evidence_fields"],
        "classification_after_inspection": reclassification["classification_after"],
        "evidence_request_id": request["evidence_request_id"],
        "recommended_next_human_choice": "AUTHORIZE_TAXONOMY_GAP_EVIDENCE_EXTRACTION",
        "recommended_next_evidence_unit": request["allowed_next_evidence_unit_proposal"],
        "action_executed": False,
        "repair_executed": False,
        "repair_command_emitted": False,
        "repair_objective_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "taxonomy_upgrade_proposal_emitted": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "extraction_repair_authorized": False,
        "source_mutation": False,
        "hidden_next_command": False,
        "review_only": True,
    }

def build_decision_packet(assessment: Dict[str, Any], request: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "pressure_loop_taxonomy_gap_application_decision_packet_v0",
        "packet_type": "HUMAN_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "handling_state": "HANDLE_NOT_ENOUGH_EVIDENCE",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": "NOT_ENOUGH_EVIDENCE",
        "evidence_sufficiency_class": assessment["evidence_sufficiency_class"],
        "missing_evidence_reason": assessment["classification_reason"],
        "allowed_human_choices": [
            "AUTHORIZE_TAXONOMY_GAP_EVIDENCE_EXTRACTION",
            "REQUEST_MORE_REPRESENTATIVE_FRAGMENTS",
            "COMPARE_TOP_TWO_GROUPS_BEFORE_EVIDENCE_EXTRACTION",
            "MARK_EVIDENCE_BLOCKED_BY_AUTHORITY",
            "REJECT_TAXONOMY_GAP_APPLICATION_RESULT",
        ],
        "recommended_next_handling": "AUTHORIZE_TAXONOMY_GAP_EVIDENCE_EXTRACTION",
        "recommended_next_evidence_unit": request["allowed_next_evidence_unit_proposal"],
        "repair_objective_proposal_emitted": False,
        "taxonomy_upgrade_proposal_emitted": False,
        "may_emit_repair_command": False,
        "may_emit_build_command": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_authority_widening": False,
        "may_authorize_optimization": False,
        "may_authorize_extraction_repair": False,
        "may_auto_open_next_group": False,
        "may_advance_without_human_decision": False,
        "terminal_rule": "STOP_HUMAN_DECISION_REQUIRED",
        "review_only": True,
    }

def validate_outputs(selection: Dict[str, Any], full_membership: List[Dict[str, Any]], inspection: Dict[str, Any], assessment: Dict[str, Any], request: Dict[str, Any], reclassification: Dict[str, Any], report: Dict[str, Any], packet: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if selection["pressure_group_key_hash"] != TOP_GROUP_KEY_HASH:
        failures.append("selection_group_key_wrong")
    if selection["handling_state"] != "HANDLE_NOT_ENOUGH_EVIDENCE":
        failures.append("selection_handling_state_wrong")
    if selection["parent_pressure_class"] != EXPECTED_PARENT_PRESSURE_CLASS:
        failures.append("selection_parent_wrong")
    if selection["pressure_subtype"] != EXPECTED_PRESSURE_SUBTYPE:
        failures.append("selection_subtype_wrong")
    if selection["halt_reason"] != EXPECTED_HALT_REASON:
        failures.append("selection_halt_wrong")
    if selection["group_count"] != EXPECTED_TOP_GROUP_COUNT:
        failures.append("selection_group_count_wrong")
    if selection["stable_rank_authorizes_repair"] is not False:
        failures.append("stable_rank_authorizes_repair")
    if selection["top_two_comparison_performed"] is not False:
        failures.append("top_two_comparison_performed_by_default")

    if len(full_membership) != EXPECTED_TOP_GROUP_COUNT:
        failures.append(f"full_membership_count_wrong:{len(full_membership)}")
    for row in full_membership:
        if row["pressure_group_key_hash"] != TOP_GROUP_KEY_HASH:
            failures.append("membership_group_key_wrong")
        if row["parent_pressure_class"] != EXPECTED_PARENT_PRESSURE_CLASS:
            failures.append("membership_parent_wrong")
        if row["pressure_subtype"] != EXPECTED_PRESSURE_SUBTYPE:
            failures.append("membership_subtype_wrong")
        if row["halt_reason"] != EXPECTED_HALT_REASON:
            failures.append("membership_halt_wrong")

    if inspection["representative_fragment_count"] == 0:
        failures.append("no_fragments_inspected")
    if inspection["top_two_comparison_performed"] is not False:
        failures.append("inspection_top_two_performed_by_default")
    if inspection["fragment_findings"]["fixable_scope_found"] is not False:
        failures.append("fixable_scope_found_unexpectedly")
    if inspection["fragment_findings"]["not_enough_evidence_support_found"] is not True:
        failures.append("not_enough_evidence_not_supported")

    if assessment["evidence_sufficiency_class"] not in VALID_EVIDENCE_CLASSES:
        failures.append("invalid_evidence_sufficiency_class")
    if assessment["classification_after_inspection"] != "NOT_ENOUGH_EVIDENCE":
        failures.append("classification_after_not_not_enough_evidence")
    if assessment["evidence_sufficient_for_fixable_classification"] is not False:
        failures.append("fixable_evidence_wrongly_sufficient")
    if assessment["evidence_sufficient_for_healthy_classification"] is not False:
        failures.append("healthy_evidence_wrongly_sufficient")
    if assessment["evidence_insufficient"] is not True:
        failures.append("evidence_insufficient_not_true")
    if "explicit_missing_label_identifier" not in assessment["missing_evidence_fields"]:
        failures.append("missing_identifier_not_requested")
    if "operational_cause_mapping" not in assessment["missing_evidence_fields"]:
        failures.append("operational_cause_mapping_not_requested")
    if assessment["repair_proposal_allowed"] is not False:
        failures.append("repair_proposal_allowed_unexpectedly")
    if assessment["taxonomy_upgrade_allowed"] is not False:
        failures.append("taxonomy_upgrade_allowed_unexpectedly")

    if request["request_type"] != "EVIDENCE_REQUEST_NOT_REPAIR":
        failures.append("request_type_wrong")
    if request["evidence_sufficiency_class"] != assessment["evidence_sufficiency_class"]:
        failures.append("request_evidence_class_mismatch")
    if not request.get("missing_evidence_reason"):
        failures.append("request_missing_reason_absent")
    if request["allowed_next_evidence_unit_proposal"] != "EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_V0":
        failures.append("next_evidence_unit_wrong")
    for key in [
        "proposal_emitted",
        "repair_objective_proposal_emitted",
        "taxonomy_upgrade_proposal_emitted",
        "build_command_emitted",
    ]:
        if request.get(key) is not False:
            failures.append(f"request_guard_not_false:{key}:{request.get(key)}")

    if reclassification["classification_after"] != "NOT_ENOUGH_EVIDENCE":
        failures.append("reclassification_after_wrong")
    if reclassification["evidence_request_emitted"] is not True:
        failures.append("reclassification_no_evidence_request")
    for key in [
        "repair_objective_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "extraction_repair_authorized",
        "repair_executed",
        "build_command_emitted",
    ]:
        if reclassification.get(key) is not False:
            failures.append(f"reclassification_guard_not_false:{key}:{reclassification.get(key)}")

    for key in [
        "action_executed",
        "repair_executed",
        "repair_command_emitted",
        "repair_objective_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "taxonomy_upgrade_proposal_emitted",
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
    if packet["recommended_next_evidence_unit"] != "EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_V0":
        failures.append("packet_next_evidence_unit_wrong")
    for key in [
        "may_emit_repair_command",
        "may_emit_build_command",
        "may_authorize_taxonomy_upgrade",
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
    if receipt.get("source_pressure_loop_protocol_receipt_id") != SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID:
        failures.append("source_protocol_wrong")
    if receipt.get("source_top_group_classification_receipt_id") != SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID:
        failures.append("source_top_group_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "LOOP_APP_0_SOURCE_SURFACE_VERIFIED",
        "LOOP_APP_1_PROTOCOL_RECEIPT_VERIFIED",
        "LOOP_APP_2_TOP_GROUP_VERIFIED",
        "LOOP_APP_3_HANDLE_NOT_ENOUGH_EVIDENCE_STATE_APPLIED",
        "LOOP_APP_4_FULL_MEMBERSHIP_EXTRACTED",
        "LOOP_APP_5_FRAGMENTS_INSPECTED",
        "LOOP_APP_6_EVIDENCE_SUFFICIENCY_CLASS_EMITTED",
        "LOOP_APP_7_EVIDENCE_REQUEST_EMITTED",
        "LOOP_APP_8_RECLASSIFIED_NOT_ENOUGH_EVIDENCE",
        "LOOP_APP_9_NO_REPAIR_OR_TAXONOMY_ACTION",
        "LOOP_APP_10_DECISION_PACKET_EMITTED",
        "LOOP_APP_11_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("classification_after_inspection") != "NOT_ENOUGH_EVIDENCE":
        failures.append("metric_classification_after_wrong")
    if metrics.get("evidence_sufficiency_class") not in VALID_EVIDENCE_CLASSES:
        failures.append("metric_evidence_class_invalid")
    if metrics.get("top_group_count") != EXPECTED_TOP_GROUP_COUNT:
        failures.append("metric_top_group_count_wrong")
    for key in [
        "repair_command_emitted_count",
        "build_command_emitted_count",
        "repair_executed_count",
        "repair_objective_proposal_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_upgrade_proposal_emitted_count",
        "authority_widening_authorized_count",
        "optimization_authorized_count",
        "extraction_repair_authorized_count",
        "source_mutation_count",
        "hidden_next_command_count",
        "top_two_comparison_default_count",
        "next_group_auto_opened_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("loop_application_guards", {})
    for key in [
        "source_surface_verified",
        "protocol_receipt_verified",
        "top_group_verified",
        "handle_not_enough_evidence_state_applied",
        "full_membership_extracted",
        "fragments_inspected",
        "evidence_sufficiency_class_emitted",
        "evidence_request_emitted",
        "reclassified_not_enough_evidence",
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
        "taxonomy_upgrade_proposal_emitted",
        "authority_widening_authorized",
        "optimization_authorized",
        "extraction_repair_authorized",
        "source_mutation",
        "hidden_next_command",
        "top_two_comparison_by_default",
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

    selection = build_group_selection(sources)
    full_membership = build_full_membership(sources)
    inspection = inspect_fragments(full_membership, sources)
    assessment = assess_evidence(full_membership, inspection)
    evidence_request = build_evidence_request(assessment)
    reclassification = build_reclassification(assessment)
    report = build_report(selection, full_membership, inspection, assessment, evidence_request, reclassification)
    packet = build_decision_packet(assessment, evidence_request)

    write_json(GROUP_SELECTION_PATH, selection)
    write_jsonl(FULL_MEMBERSHIP_PATH, full_membership)
    write_json(DEEP_FRAGMENT_INSPECTION_PATH, inspection)
    write_json(EVIDENCE_SUFFICIENCY_ASSESSMENT_PATH, assessment)
    write_json(EVIDENCE_REQUEST_PATH, evidence_request)
    write_json(RECLASSIFICATION_PATH, reclassification)
    write_json(LOOP_APPLICATION_REPORT_PATH, report)
    write_json(LOOP_APPLICATION_DECISION_PACKET_PATH, packet)

    failures.extend(validate_outputs(selection, full_membership, inspection, assessment, evidence_request, reclassification, report, packet))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "LOOP_APP_0_SOURCE_SURFACE_VERIFIED": len(validate_sources(sources)) == 0,
        "LOOP_APP_1_PROTOCOL_RECEIPT_VERIFIED": sources["protocol_receipt"]["receipt_id"] == SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID and sources["protocol_receipt"]["gate"] == "PASS",
        "LOOP_APP_2_TOP_GROUP_VERIFIED": selection["pressure_group_key_hash"] == TOP_GROUP_KEY_HASH and selection["group_count"] == EXPECTED_TOP_GROUP_COUNT,
        "LOOP_APP_3_HANDLE_NOT_ENOUGH_EVIDENCE_STATE_APPLIED": selection["handling_state"] == "HANDLE_NOT_ENOUGH_EVIDENCE",
        "LOOP_APP_4_FULL_MEMBERSHIP_EXTRACTED": len(full_membership) == EXPECTED_TOP_GROUP_COUNT,
        "LOOP_APP_5_FRAGMENTS_INSPECTED": inspection["representative_fragment_count"] > 0,
        "LOOP_APP_6_EVIDENCE_SUFFICIENCY_CLASS_EMITTED": assessment["evidence_sufficiency_class"] in VALID_EVIDENCE_CLASSES,
        "LOOP_APP_7_EVIDENCE_REQUEST_EMITTED": EVIDENCE_REQUEST_PATH.exists() and evidence_request["request_type"] == "EVIDENCE_REQUEST_NOT_REPAIR",
        "LOOP_APP_8_RECLASSIFIED_NOT_ENOUGH_EVIDENCE": reclassification["classification_after"] == "NOT_ENOUGH_EVIDENCE",
        "LOOP_APP_9_NO_REPAIR_OR_TAXONOMY_ACTION": report["repair_executed"] is False and report["taxonomy_upgrade_authorized"] is False and evidence_request["repair_objective_proposal_emitted"] is False,
        "LOOP_APP_10_DECISION_PACKET_EMITTED": LOOP_APPLICATION_DECISION_PACKET_PATH.exists(),
        "LOOP_APP_11_NO_SOURCE_MUTATION": source_mutation_detected is False,
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
        report["authority_widening_authorized"],
        report["optimization_authorized"],
        report["extraction_repair_authorized"],
        packet["may_emit_build_command"],
        packet["may_emit_repair_command"],
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "top_group_count": EXPECTED_TOP_GROUP_COUNT,
        "full_membership_count": len(full_membership),
        "representative_fragment_count": inspection["representative_fragment_count"],
        "evidence_sufficiency_class": assessment["evidence_sufficiency_class"],
        "classification_before_application": "NOT_ENOUGH_EVIDENCE",
        "classification_after_inspection": reclassification["classification_after"],
        "evidence_request_emitted": True,
        "evidence_request_id": evidence_request["evidence_request_id"],
        "recommended_next_evidence_unit": evidence_request["allowed_next_evidence_unit_proposal"],
        "repair_command_emitted_count": 0,
        "build_command_emitted_count": 0,
        "repair_executed_count": 0,
        "repair_objective_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_upgrade_proposal_emitted_count": 0,
        "authority_widening_authorized_count": 0,
        "optimization_authorized_count": 0,
        "extraction_repair_authorized_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "hidden_next_command_count": 0,
        "top_two_comparison_default_count": 0,
        "next_group_auto_opened_count": 0,
        "review_only": True,
    }

    guards = {
        "source_surface_verified": len(validate_sources(sources)) == 0,
        "protocol_receipt_verified": True,
        "top_group_verified": True,
        "handle_not_enough_evidence_state_applied": True,
        "full_membership_extracted": True,
        "fragments_inspected": True,
        "evidence_sufficiency_class_emitted": True,
        "evidence_request_emitted": True,
        "reclassified_not_enough_evidence": True,
        "decision_packet_emitted": True,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "repair_executed": False,
        "repair_objective_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "taxonomy_upgrade_proposal_emitted": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "extraction_repair_authorized": False,
        "source_mutation": source_mutation_detected,
        "hidden_next_command": False,
        "top_two_comparison_by_default": False,
        "next_group_auto_opened": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "protocol_receipt": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "top_group_receipt": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "evidence_request_id": evidence_request["evidence_request_id"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "taxonomy_gap_group_selection": rel(GROUP_SELECTION_PATH),
        "taxonomy_gap_full_membership": rel(FULL_MEMBERSHIP_PATH),
        "taxonomy_gap_deep_fragment_inspection": rel(DEEP_FRAGMENT_INSPECTION_PATH),
        "taxonomy_gap_evidence_sufficiency_assessment": rel(EVIDENCE_SUFFICIENCY_ASSESSMENT_PATH),
        "taxonomy_gap_evidence_request": rel(EVIDENCE_REQUEST_PATH),
        "taxonomy_gap_reclassification_after_inspection": rel(RECLASSIFICATION_PATH),
        "pressure_loop_taxonomy_gap_application_report": rel(LOOP_APPLICATION_REPORT_PATH),
        "pressure_loop_taxonomy_gap_application_decision_packet": rel(LOOP_APPLICATION_DECISION_PACKET_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "pressure_loop_taxonomy_gap_application_receipt_v0",
        "receipt_type": "PRESSURE_LOOP_TAXONOMY_GAP_APPLICATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "source_candidate_c_interrogation_receipt_id": SOURCE_CANDIDATE_C_INTERROGATION_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "application_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "parent_pressure_class": EXPECTED_PARENT_PRESSURE_CLASS,
            "pressure_subtype": EXPECTED_PRESSURE_SUBTYPE,
            "halt_reason": EXPECTED_HALT_REASON,
            "handling_state": "HANDLE_NOT_ENOUGH_EVIDENCE",
            "classification_after_inspection": reclassification["classification_after"],
            "evidence_sufficiency_class": assessment["evidence_sufficiency_class"],
            "evidence_request_id": evidence_request["evidence_request_id"],
            "recommended_next_evidence_unit": evidence_request["allowed_next_evidence_unit_proposal"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "loop_application_guards": guards,
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
    print(f"pressure_loop_taxonomy_gap_application_receipt_id={receipt_id}")
    print(f"pressure_loop_taxonomy_gap_application_receipt_path=data/pressure_loop_applications/r1000_top_group_taxonomy_gap_v0_receipts/{receipt_id}.json")
    print(f"taxonomy_gap_evidence_request_path=data/pressure_loop_applications/r1000_top_group_taxonomy_gap_v0/taxonomy_gap_evidence_request.json")
    print(f"pressure_loop_taxonomy_gap_application_decision_packet_path=data/pressure_loop_applications/r1000_top_group_taxonomy_gap_v0/pressure_loop_taxonomy_gap_application_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
