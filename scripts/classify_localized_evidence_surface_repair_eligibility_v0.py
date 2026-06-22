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

UNIT_ID = "CLASSIFY_LOCALIZED_EVIDENCE_SURFACE_REPAIR_ELIGIBILITY_V0"
TARGET_UNIT_ID = "localized_evidence_surface_repair_eligibility.v0"

SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID = "bea59318"
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

OUT_DIR = ROOT / "data" / "localized_evidence_surface_repair_eligibility_v0"
RECEIPT_DIR = ROOT / "data" / "localized_evidence_surface_repair_eligibility_v0_receipts"

ELIGIBILITY_INPUT_ROLLUP_PATH = OUT_DIR / "localized_repair_eligibility_input_rollup.json"
ELIGIBILITY_CLASSIFICATION_PATH = OUT_DIR / "localized_repair_eligibility_classification.json"
REPAIR_OBJECTIVE_PROPOSAL_PATH = OUT_DIR / "localized_evidence_surface_repair_objective_proposal.json"
HUMAN_DECISION_PACKET_PATH = OUT_DIR / "localized_repair_eligibility_decision_packet.json"
ELIGIBILITY_REPORT_PATH = OUT_DIR / "localized_repair_eligibility_report.json"

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
CONTEXT_REFS_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0" / "taxonomy_gap_context_refs.json"

LOOP_APPLICATION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0_receipts" / f"{SOURCE_LOOP_APPLICATION_RECEIPT_ID}.json"
PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID}.json"
TOP_GROUP_CLASSIFICATION_RECEIPT_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0_receipts" / f"{SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID}.json"
R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"
R1000_PRESSURE_EVENTS_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_event_rows.jsonl"
R1000_GROUP_MEMBERSHIP_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_candidate_c_group_event_membership.jsonl"

LOCALIZATION_BUILDER_PATH = ROOT / "scripts" / "audit_taxonomy_gap_evidence_surface_localization_v0.py"
EXTRACTION_BUILDER_PATH = ROOT / "scripts" / "extract_r1000_top_group_taxonomy_gap_missing_label_evidence_v0.py"

SOURCE_FILES = [
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
    CONTEXT_REFS_PATH,
    LOOP_APPLICATION_RECEIPT_PATH,
    PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH,
    TOP_GROUP_CLASSIFICATION_RECEIPT_PATH,
    R1000_SCALE_RECEIPT_PATH,
    R1000_PRESSURE_EVENTS_PATH,
    R1000_GROUP_MEMBERSHIP_PATH,
    LOCALIZATION_BUILDER_PATH,
    EXTRACTION_BUILDER_PATH,
]

ELIGIBILITY_CLASSES = [
    "ELIGIBLE_EVIDENCE_SURFACE_REPAIR_OBJECTIVE",
    "NOT_ELIGIBLE_HEALTHY_EXPECTED_LIMIT",
    "NOT_ENOUGH_EVIDENCE_FOR_REPAIR_ELIGIBILITY",
]

HUMAN_DECISION = {
    "decision": "CLASSIFY_LOCALIZED_EVIDENCE_SURFACE_REPAIR_ELIGIBILITY",
    "scope": "classify and package human-reviewable evidence-surface repair objective only",
    "source_localization_audit_receipt_id": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
    "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
    "not_authorized": [
        "repair_execution",
        "taxonomy_repair",
        "taxonomy_upgrade",
        "taxonomy_delta_proposal",
        "authority_widening",
        "burden_optimization",
        "source_mutation",
        "protocol_adoption",
        "next_group_auto_open",
        "build_command",
    ],
}

MUST_NOT_INFER = [
    "repair eligibility is not repair execution",
    "evidence-surface repair objective is not taxonomy repair",
    "evidence-surface repair objective is not taxonomy delta proposal",
    "do not guess missing label values",
    "do not mutate source rows",
    "do not widen authority",
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

def load_sources() -> Dict[str, Any]:
    return {
        "localization_receipt": read_json(LOCALIZATION_RECEIPT_PATH),
        "raw_source_field_audit": read_json(RAW_SOURCE_FIELD_AUDIT_PATH),
        "extractor_logic_audit": read_json(EXTRACTOR_LOGIC_AUDIT_PATH),
        "schema_slot_audit": read_json(SCHEMA_SLOT_AUDIT_PATH),
        "surface_localization_candidates": read_json(SURFACE_LOCALIZATION_CANDIDATES_PATH),
        "surface_localization_classification": read_json(SURFACE_LOCALIZATION_CLASSIFICATION_PATH),
        "surface_localization_packet": read_json(SURFACE_LOCALIZATION_PACKET_PATH),
        "surface_localization_report": read_json(SURFACE_LOCALIZATION_REPORT_PATH),
        "evidence_surface_receipt": read_json(EVIDENCE_SURFACE_RECEIPT_PATH),
        "evidence_extraction_receipt": read_json(EVIDENCE_EXTRACTION_RECEIPT_PATH),
        "field_rows": read_jsonl(FIELD_ROWS_PATH),
        "context_refs": read_json(CONTEXT_REFS_PATH),
        "loop_application_receipt": read_json(LOOP_APPLICATION_RECEIPT_PATH),
        "pressure_loop_protocol_receipt": read_json(PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH),
        "top_group_classification_receipt": read_json(TOP_GROUP_CLASSIFICATION_RECEIPT_PATH),
        "r1000_scale_receipt": read_json(R1000_SCALE_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    loc = sources["localization_receipt"]
    raw = sources["raw_source_field_audit"]
    extractor = sources["extractor_logic_audit"]
    schema = sources["schema_slot_audit"]
    classification = sources["surface_localization_classification"]

    if loc.get("receipt_id") != SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID:
        failures.append("localization_receipt_id_wrong")
    if loc.get("gate") != "PASS":
        failures.append("localization_receipt_not_pass")
    if loc.get("aggregate_metrics", {}).get("classification") != "LOCALIZED_EVIDENCE_SURFACE_DEFICIENCY":
        failures.append("localization_not_localized_deficiency")
    if loc.get("aggregate_metrics", {}).get("selected_localization_class") != "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELDS":
        failures.append("localization_class_wrong")
    if loc.get("aggregate_metrics", {}).get("selected_localization_support_level") != "STRONG":
        failures.append("localization_support_not_strong")
    if loc.get("aggregate_metrics", {}).get("localized_surface_found") is not True:
        failures.append("localized_surface_not_found")
    if rel(R1000_PRESSURE_EVENTS_PATH) not in loc.get("aggregate_metrics", {}).get("localized_surface_refs", []):
        failures.append("localized_surface_ref_missing")
    if loc.get("aggregate_metrics", {}).get("recommended_next_review_unit") != UNIT_ID:
        failures.append("localization_recommended_unit_not_this")

    if raw.get("source_row_count") != EXPECTED_FIELD_ROW_COUNT:
        failures.append("raw_source_row_count_wrong")
    if raw.get("raw_source_contains_any_required_missing_field") is not False:
        failures.append("raw_source_unexpectedly_contains_fields")
    if raw.get("field_rows_preserve_structural_refs") is not True:
        failures.append("field_rows_do_not_preserve_structural_refs")

    if extractor.get("extractor_mentions_all_required_missing_fields") is not True:
        failures.append("extractor_not_reading_required_fields")
    if schema.get("field_extraction_schema_has_required_slots") is not True:
        failures.append("field_extraction_schema_missing_slots")
    if schema.get("source_event_schema_has_required_slots") is not False:
        failures.append("source_event_schema_unexpectedly_has_slots")

    if classification.get("classification") != "LOCALIZED_EVIDENCE_SURFACE_DEFICIENCY":
        failures.append("surface_localization_classification_wrong")

    if len(sources["field_rows"]) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_rows_length_wrong")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_input_rollup(sources: Dict[str, Any]) -> Dict[str, Any]:
    raw = sources["raw_source_field_audit"]
    extractor = sources["extractor_logic_audit"]
    schema = sources["schema_slot_audit"]
    loc = sources["localization_receipt"]

    return {
        "schema_version": "localized_repair_eligibility_input_rollup_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_localization_audit_receipt_id": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
        "localized_surface_found": True,
        "localized_surface_refs": [rel(R1000_PRESSURE_EVENTS_PATH)],
        "selected_localization_class": "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELDS",
        "selected_localization_support_level": "STRONG",
        "raw_source_row_count": raw["source_row_count"],
        "field_row_count": raw["field_row_count"],
        "missing_fields": MISSING_FIELDS,
        "raw_source_field_presence_profile": raw["raw_source_field_presence_profile"],
        "extracted_field_presence_profile": raw["extracted_field_presence_profile"],
        "extractor_mentions_all_required_missing_fields": extractor["extractor_mentions_all_required_missing_fields"],
        "extractor_attempts_fallback_reads": extractor["extractor_attempts_fallback_reads"],
        "field_extraction_schema_has_required_slots": schema["field_extraction_schema_has_required_slots"],
        "source_event_schema_has_required_slots": schema["source_event_schema_has_required_slots"],
        "source_event_schema_slot_absence_fields": schema["schema_slot_absence_fields"],
        "repair_surface": "source_event_payload_surface",
        "repair_surface_artifact": rel(R1000_PRESSURE_EVENTS_PATH),
        "bounded_repair_surface_found": True,
        "taxonomy_delta_required": False,
        "taxonomy_upgrade_required": False,
        "missing_label_value_guess_required": False,
        "repair_execution_requested": False,
        "review_only": True,
    }

def classify_eligibility(rollup: Dict[str, Any]) -> Dict[str, Any]:
    eligible = (
        rollup["localized_surface_found"] is True
        and rollup["bounded_repair_surface_found"] is True
        and rollup["extractor_mentions_all_required_missing_fields"] is True
        and rollup["field_extraction_schema_has_required_slots"] is True
        and rollup["source_event_schema_has_required_slots"] is False
        and rollup["taxonomy_delta_required"] is False
        and rollup["missing_label_value_guess_required"] is False
    )

    if eligible:
        classification = "ELIGIBLE_EVIDENCE_SURFACE_REPAIR_OBJECTIVE"
        reason = "Localized source-event payload surface lacks required evidence fields, while extractor logic and extracted row schema can carry them; a bounded evidence-surface repair objective can be proposed without taxonomy repair or guessing missing labels."
        proposal_allowed = True
        recommended = "HUMAN_REVIEW_EVIDENCE_SURFACE_REPAIR_OBJECTIVE"
    else:
        classification = "NOT_ENOUGH_EVIDENCE_FOR_REPAIR_ELIGIBILITY"
        reason = "Repair eligibility could not be proven without guessing or unresolved localization."
        proposal_allowed = False
        recommended = "REQUEST_MORE_LOCALIZATION_AUDIT"

    return {
        "schema_version": "localized_repair_eligibility_classification_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": classification,
        "classification_classes": ELIGIBILITY_CLASSES,
        "classified_exactly_once": True,
        "classification_reason": reason,
        "proposal_allowed": proposal_allowed,
        "recommended_next_handling": recommended,
        "repair_surface": rollup["repair_surface"],
        "repair_surface_artifact": rollup["repair_surface_artifact"],
        "missing_fields_to_expose": rollup["missing_fields"],
        "expected_effect": "Expose/preserve missing-label evidence fields in future pressure event rows so extraction can re-run and original taxonomy-gap pressure can be reclassified.",
        "taxonomy_repair_required": False,
        "taxonomy_upgrade_required": False,
        "taxonomy_delta_proposal_required": False,
        "missing_label_value_guess_required": False,
        "repair_executed": False,
        "source_mutation": False,
        "build_command_emitted": False,
        "review_only": True,
    }

def build_repair_objective_proposal(classification: Dict[str, Any], rollup: Dict[str, Any]) -> Dict[str, Any]:
    if classification["classification"] != "ELIGIBLE_EVIDENCE_SURFACE_REPAIR_OBJECTIVE":
        return {
            "schema_version": "localized_evidence_surface_repair_objective_proposal_v0",
            "proposal_emitted": False,
            "reason": "classification_not_eligible",
            "classification": classification["classification"],
            "repair_command_emitted": False,
            "repair_executed": False,
            "taxonomy_upgrade_authorized": False,
            "taxonomy_delta_proposal_emitted": False,
            "authority_widening_authorized": False,
            "burden_optimization_authorized": False,
            "source_mutation": False,
            "build_command_emitted": False,
            "review_only": True,
        }

    repair_objective_id = sha8({
        "objective": "EVIDENCE_SURFACE_REPAIR",
        "surface": rollup["repair_surface_artifact"],
        "missing_fields": rollup["missing_fields"],
        "source": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
    })

    return {
        "schema_version": "localized_evidence_surface_repair_objective_proposal_v0",
        "proposal_emitted": True,
        "proposal_type": "EVIDENCE_SURFACE_REPAIR_OBJECTIVE_PROPOSAL",
        "repair_objective_id": repair_objective_id,
        "repair_objective_name": "REPAIR_R1000_PRESSURE_EVENT_TAXONOMY_GAP_FIELD_SURFACE_V0",
        "repair_scope": "Update the pressure-event source surface so future rows can expose explicit taxonomy-gap evidence fields when available, or explicit null-with-reason when unavailable.",
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_evidence_refs": [
            rel(LOCALIZATION_RECEIPT_PATH),
            rel(RAW_SOURCE_FIELD_AUDIT_PATH),
            rel(SCHEMA_SLOT_AUDIT_PATH),
            rel(EXTRACTOR_LOGIC_AUDIT_PATH),
            rel(FIELD_ROWS_PATH),
        ],
        "localized_repair_surface_refs": rollup["localized_surface_refs"],
        "missing_fields_to_expose": rollup["missing_fields"],
        "field_semantics": {
            "missing_label_identifier": "Opaque identifier/name for the label that the pressure event could not classify, if known by source payload.",
            "taxonomy_context_ref": "Reference to the taxonomy/label-space context in which the missing label was detected.",
            "current_label_space_ref": "Reference to the current emitted label space used by the pressure event.",
            "expected_label_space_ref": "Reference to the expected or required label space, if available.",
        },
        "required_output_behavior": [
            "preserve existing pressure_event_id",
            "preserve pressure_group_key_hash",
            "preserve parent_pressure_class",
            "preserve pressure_subtype",
            "preserve halt_reason",
            "preserve source_receipt_ref",
            "preserve source_trace_ref",
            "emit missing evidence fields when available",
            "emit explicit null values with absence_reason when fields are unavailable",
            "do not infer missing label values",
        ],
        "candidate_artifacts_to_update_or_verify": [
            rel(R1000_PRESSURE_EVENTS_PATH),
            "producer_of_r1000_pressure_event_rows_jsonl",
            "pressure_event_row_schema_or_emitter",
        ],
        "candidate_scripts_to_inspect": [
            "producer_of_r1000_pressure_event_rows_jsonl",
            rel(LOCALIZATION_BUILDER_PATH),
            rel(EXTRACTION_BUILDER_PATH),
        ],
        "expected_acceptance_gates": [
            "source surface emits required field keys or explicit null-with-reason",
            "existing structural refs preserved",
            "25-row top group remains addressable",
            "field extraction rerun consumes new surface",
            "taxonomy gap reclassification reruns after evidence surface repair",
            "no taxonomy delta proposed",
            "no taxonomy upgrade authorized",
            "no missing label value guessed",
            "no source receipt mutation",
        ],
        "rerun_required_after_repair": [
            "EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_V0",
            "CLASSIFY_TAXONOMY_GAP_EVIDENCE_SURFACE_DEFICIENCY_V0",
            "reclassify original taxonomy-gap pressure group after evidence improves",
        ],
        "forbidden_scope": [
            "taxonomy repair",
            "taxonomy upgrade",
            "taxonomy delta proposal",
            "authority widening",
            "burden optimization",
            "guessing missing label values",
            "mutating existing receipts",
            "auto-opening next group",
            "executing repair inside this unit",
        ],
        "terminal_rule": "STOP_HUMAN_DECISION_REQUIRED",
        "repair_command_emitted": False,
        "repair_executed": False,
        "taxonomy_upgrade_authorized": False,
        "taxonomy_delta_proposal_emitted": False,
        "authority_widening_authorized": False,
        "burden_optimization_authorized": False,
        "source_mutation": False,
        "build_command_emitted": False,
        "review_only": True,
    }

def build_decision_packet(classification: Dict[str, Any], proposal: Dict[str, Any]) -> Dict[str, Any]:
    if proposal["proposal_emitted"]:
        recommended = "ACCEPT_EVIDENCE_SURFACE_REPAIR_OBJECTIVE"
    else:
        recommended = "REQUEST_MORE_LOCALIZATION_AUDIT"

    return {
        "schema_version": "localized_repair_eligibility_decision_packet_v0",
        "packet_type": "HUMAN_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": classification["classification"],
        "classification_reason": classification["classification_reason"],
        "proposal_emitted": proposal["proposal_emitted"],
        "repair_objective_id": proposal.get("repair_objective_id"),
        "allowed_human_choices": [
            "ACCEPT_EVIDENCE_SURFACE_REPAIR_OBJECTIVE",
            "DECLINE_EVIDENCE_SURFACE_REPAIR_OBJECTIVE",
            "REQUEST_MORE_LOCALIZATION_AUDIT",
            "MARK_HEALTHY_EXPECTED_EVIDENCE_LIMIT",
            "REJECT_REPAIR_ELIGIBILITY_CLASSIFICATION",
        ],
        "recommended_next_handling": recommended,
        "next_if_accepted": "BUILD_REPAIR_R1000_PRESSURE_EVENT_TAXONOMY_GAP_FIELD_SURFACE_V0",
        "next_if_declined": "STOP_OR_INSPECT_NEXT_PRESSURE_GROUP_BY_HUMAN_DECISION",
        "may_emit_repair_command": False,
        "may_emit_build_command": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_taxonomy_delta": False,
        "may_authorize_authority_widening": False,
        "may_authorize_burden_optimization": False,
        "may_execute_repair": False,
        "may_adopt_protocol": False,
        "may_auto_open_next_group": False,
        "may_advance_without_human_decision": False,
        "review_only": True,
    }

def build_report(rollup: Dict[str, Any], classification: Dict[str, Any], proposal: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "localized_repair_eligibility_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_localization_audit_receipt_id": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
            "source_evidence_surface_classification_receipt_id": SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID,
            "source_taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
            "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
            "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
            "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
            "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        },
        "input_rollup": rollup,
        "classification_summary": classification,
        "repair_objective_proposal": {
            "proposal_emitted": proposal["proposal_emitted"],
            "repair_objective_id": proposal.get("repair_objective_id"),
            "repair_objective_name": proposal.get("repair_objective_name"),
            "repair_scope": proposal.get("repair_scope"),
        },
        "decision_packet_recommended_next_handling": packet["recommended_next_handling"],
        "action_executed": False,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "repair_executed": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "burden_optimization_authorized": False,
        "protocol_adoption_authorized": False,
        "next_group_auto_opened": False,
        "source_mutation": False,
        "hidden_next_command": False,
        "review_only": True,
    }

def validate_outputs(rollup: Dict[str, Any], classification: Dict[str, Any], proposal: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if rollup["localized_surface_found"] is not True:
        failures.append("localized_surface_not_found")
    if rollup["localized_surface_refs"] != [rel(R1000_PRESSURE_EVENTS_PATH)]:
        failures.append("localized_surface_refs_wrong")
    if rollup["selected_localization_class"] != "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELDS":
        failures.append("selected_localization_class_wrong")
    if rollup["selected_localization_support_level"] != "STRONG":
        failures.append("selected_localization_support_not_strong")
    if rollup["raw_source_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("raw_source_row_count_wrong")
    if rollup["field_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_row_count_wrong")
    if rollup["extractor_mentions_all_required_missing_fields"] is not True:
        failures.append("extractor_not_ready_for_fields")
    if rollup["field_extraction_schema_has_required_slots"] is not True:
        failures.append("field_extraction_schema_not_ready")
    if rollup["source_event_schema_has_required_slots"] is not False:
        failures.append("source_event_schema_should_lack_slots")
    if sorted(rollup["missing_fields"]) != sorted(MISSING_FIELDS):
        failures.append("missing_fields_wrong")
    if rollup["taxonomy_delta_required"] is not False:
        failures.append("taxonomy_delta_required")
    if rollup["taxonomy_upgrade_required"] is not False:
        failures.append("taxonomy_upgrade_required")
    if rollup["missing_label_value_guess_required"] is not False:
        failures.append("missing_label_guess_required")

    if classification["classification"] not in ELIGIBILITY_CLASSES:
        failures.append("invalid_eligibility_classification")
    if classification["classified_exactly_once"] is not True:
        failures.append("not_classified_exactly_once")
    if classification["classification"] == "ELIGIBLE_EVIDENCE_SURFACE_REPAIR_OBJECTIVE" and classification["proposal_allowed"] is not True:
        failures.append("eligible_without_proposal_allowed")
    if classification["classification"] != "ELIGIBLE_EVIDENCE_SURFACE_REPAIR_OBJECTIVE" and proposal["proposal_emitted"] is True:
        failures.append("proposal_emitted_for_non_eligible")
    for key in [
        "taxonomy_repair_required",
        "taxonomy_upgrade_required",
        "taxonomy_delta_proposal_required",
        "missing_label_value_guess_required",
        "repair_executed",
        "source_mutation",
        "build_command_emitted",
    ]:
        if classification.get(key) is not False:
            failures.append(f"classification_guard_not_false:{key}:{classification.get(key)}")

    if proposal["proposal_emitted"] is not True:
        failures.append("expected_repair_objective_proposal_not_emitted")
    for field in [
        "proposal_type",
        "repair_objective_id",
        "repair_objective_name",
        "repair_scope",
        "source_pressure_group_key_hash",
        "source_evidence_refs",
        "localized_repair_surface_refs",
        "missing_fields_to_expose",
        "field_semantics",
        "required_output_behavior",
        "candidate_artifacts_to_update_or_verify",
        "candidate_scripts_to_inspect",
        "expected_acceptance_gates",
        "rerun_required_after_repair",
        "forbidden_scope",
        "terminal_rule",
    ]:
        if field not in proposal:
            failures.append(f"proposal_field_missing:{field}")
    if proposal.get("proposal_type") != "EVIDENCE_SURFACE_REPAIR_OBJECTIVE_PROPOSAL":
        failures.append("proposal_type_wrong")
    if sorted(proposal.get("missing_fields_to_expose", [])) != sorted(MISSING_FIELDS):
        failures.append("proposal_missing_fields_wrong")
    if rel(R1000_PRESSURE_EVENTS_PATH) not in proposal.get("localized_repair_surface_refs", []):
        failures.append("proposal_localized_surface_ref_missing")
    for forbidden in [
        "taxonomy repair",
        "taxonomy upgrade",
        "taxonomy delta proposal",
        "authority widening",
        "burden optimization",
        "guessing missing label values",
        "mutating existing receipts",
    ]:
        if forbidden not in proposal.get("forbidden_scope", []):
            failures.append(f"proposal_forbidden_scope_missing:{forbidden}")
    for key in [
        "repair_command_emitted",
        "repair_executed",
        "taxonomy_upgrade_authorized",
        "taxonomy_delta_proposal_emitted",
        "authority_widening_authorized",
        "burden_optimization_authorized",
        "source_mutation",
        "build_command_emitted",
    ]:
        if proposal.get(key) is not False:
            failures.append(f"proposal_guard_not_false:{key}:{proposal.get(key)}")

    if packet["packet_type"] != "HUMAN_REVIEW_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    if packet["recommended_next_handling"] != "ACCEPT_EVIDENCE_SURFACE_REPAIR_OBJECTIVE":
        failures.append("packet_recommendation_wrong")
    if packet["next_if_accepted"] != "BUILD_REPAIR_R1000_PRESSURE_EVENT_TAXONOMY_GAP_FIELD_SURFACE_V0":
        failures.append("packet_next_if_accepted_wrong")
    for key in [
        "may_emit_repair_command",
        "may_emit_build_command",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_taxonomy_delta",
        "may_authorize_authority_widening",
        "may_authorize_burden_optimization",
        "may_execute_repair",
        "may_adopt_protocol",
        "may_auto_open_next_group",
        "may_advance_without_human_decision",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")

    for key in [
        "action_executed",
        "repair_command_emitted",
        "build_command_emitted",
        "repair_executed",
        "taxonomy_delta_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "burden_optimization_authorized",
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
    if receipt.get("source_localization_audit_receipt_id") != SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID:
        failures.append("source_localization_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "REPAIR_ELIGIBILITY_0_SOURCE_SURFACE_VERIFIED",
        "REPAIR_ELIGIBILITY_1_HUMAN_DECISION_RECORDED",
        "REPAIR_ELIGIBILITY_2_LOCALIZATION_CONSUMED",
        "REPAIR_ELIGIBILITY_3_ELIGIBILITY_CLASSIFIED",
        "REPAIR_ELIGIBILITY_4_REPAIR_OBJECTIVE_PROPOSAL_EMITTED",
        "REPAIR_ELIGIBILITY_5_DECISION_PACKET_EMITTED",
        "REPAIR_ELIGIBILITY_6_NO_REPAIR_OR_TAXONOMY_ACTION",
        "REPAIR_ELIGIBILITY_7_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("classification") != "ELIGIBLE_EVIDENCE_SURFACE_REPAIR_OBJECTIVE":
        failures.append("metric_classification_wrong")
    if metrics.get("proposal_emitted") is not True:
        failures.append("metric_proposal_not_emitted")
    if metrics.get("localized_surface_refs") != [rel(R1000_PRESSURE_EVENTS_PATH)]:
        failures.append("metric_localized_surface_refs_wrong")
    for key in [
        "repair_command_emitted_count",
        "build_command_emitted_count",
        "repair_executed_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "authority_widening_authorized_count",
        "burden_optimization_authorized_count",
        "protocol_adoption_authorized_count",
        "next_group_auto_opened_count",
        "source_mutation_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("repair_eligibility_guards", {})
    for key in [
        "source_surface_verified",
        "human_decision_recorded",
        "localization_consumed",
        "eligibility_classified",
        "repair_objective_proposal_emitted",
        "decision_packet_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "repair_command_emitted",
        "build_command_emitted",
        "repair_executed",
        "taxonomy_upgrade_authorized",
        "taxonomy_delta_proposal_emitted",
        "authority_widening_authorized",
        "burden_optimization_authorized",
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

    rollup = build_input_rollup(sources)
    classification = classify_eligibility(rollup)
    proposal = build_repair_objective_proposal(classification, rollup)
    packet = build_decision_packet(classification, proposal)
    report = build_report(rollup, classification, proposal, packet)

    write_json(ELIGIBILITY_INPUT_ROLLUP_PATH, rollup)
    write_json(ELIGIBILITY_CLASSIFICATION_PATH, classification)
    write_json(REPAIR_OBJECTIVE_PROPOSAL_PATH, proposal)
    write_json(HUMAN_DECISION_PACKET_PATH, packet)
    write_json(ELIGIBILITY_REPORT_PATH, report)

    failures.extend(validate_outputs(rollup, classification, proposal, packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "REPAIR_ELIGIBILITY_0_SOURCE_SURFACE_VERIFIED": len(validate_sources(sources)) == 0,
        "REPAIR_ELIGIBILITY_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "CLASSIFY_LOCALIZED_EVIDENCE_SURFACE_REPAIR_ELIGIBILITY",
        "REPAIR_ELIGIBILITY_2_LOCALIZATION_CONSUMED": sources["localization_receipt"]["receipt_id"] == SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID and rollup["localized_surface_found"] is True,
        "REPAIR_ELIGIBILITY_3_ELIGIBILITY_CLASSIFIED": classification["classification"] == "ELIGIBLE_EVIDENCE_SURFACE_REPAIR_OBJECTIVE",
        "REPAIR_ELIGIBILITY_4_REPAIR_OBJECTIVE_PROPOSAL_EMITTED": proposal["proposal_emitted"] is True and proposal["proposal_type"] == "EVIDENCE_SURFACE_REPAIR_OBJECTIVE_PROPOSAL",
        "REPAIR_ELIGIBILITY_5_DECISION_PACKET_EMITTED": HUMAN_DECISION_PACKET_PATH.exists(),
        "REPAIR_ELIGIBILITY_6_NO_REPAIR_OR_TAXONOMY_ACTION": report["repair_executed"] is False and report["taxonomy_upgrade_authorized"] is False and report["taxonomy_delta_proposal_emitted"] is False,
        "REPAIR_ELIGIBILITY_7_NO_SOURCE_MUTATION": source_mutation_detected is False,
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
        report["repair_executed"],
        report["taxonomy_delta_proposal_emitted"],
        report["taxonomy_upgrade_authorized"],
        report["authority_widening_authorized"],
        report["burden_optimization_authorized"],
        report["source_mutation"],
        report["hidden_next_command"],
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_localization_audit_receipt_id": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
        "source_evidence_surface_classification_receipt_id": SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID,
        "source_taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": classification["classification"],
        "proposal_allowed": classification["proposal_allowed"],
        "proposal_emitted": proposal["proposal_emitted"],
        "repair_objective_id": proposal.get("repair_objective_id"),
        "repair_objective_name": proposal.get("repair_objective_name"),
        "localized_surface_refs": rollup["localized_surface_refs"],
        "missing_fields_to_expose": rollup["missing_fields"],
        "recommended_next_handling": packet["recommended_next_handling"],
        "next_if_accepted": packet["next_if_accepted"],
        "repair_command_emitted_count": 0,
        "build_command_emitted_count": 0,
        "repair_executed_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "authority_widening_authorized_count": 0,
        "burden_optimization_authorized_count": 0,
        "protocol_adoption_authorized_count": 0,
        "next_group_auto_opened_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "hidden_next_command_count": 0,
        "review_only": True,
    }

    guards = {
        "source_surface_verified": len(validate_sources(sources)) == 0,
        "human_decision_recorded": True,
        "localization_consumed": True,
        "eligibility_classified": True,
        "repair_objective_proposal_emitted": proposal["proposal_emitted"] is True,
        "decision_packet_emitted": True,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "repair_executed": False,
        "taxonomy_upgrade_authorized": False,
        "taxonomy_delta_proposal_emitted": False,
        "authority_widening_authorized": False,
        "burden_optimization_authorized": False,
        "protocol_adoption_authorized": False,
        "next_group_auto_opened": False,
        "source_mutation": source_mutation_detected,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_localization_receipt": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
        "classification": classification["classification"],
        "repair_objective_id": proposal.get("repair_objective_id"),
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "localized_repair_eligibility_input_rollup": rel(ELIGIBILITY_INPUT_ROLLUP_PATH),
        "localized_repair_eligibility_classification": rel(ELIGIBILITY_CLASSIFICATION_PATH),
        "localized_evidence_surface_repair_objective_proposal": rel(REPAIR_OBJECTIVE_PROPOSAL_PATH),
        "localized_repair_eligibility_decision_packet": rel(HUMAN_DECISION_PACKET_PATH),
        "localized_repair_eligibility_report": rel(ELIGIBILITY_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "localized_evidence_surface_repair_eligibility_receipt_v0",
        "receipt_type": "LOCALIZED_EVIDENCE_SURFACE_REPAIR_ELIGIBILITY_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_localization_audit_receipt_id": SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID,
        "source_evidence_surface_classification_receipt_id": SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID,
        "source_taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
        "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
        "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "eligibility_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "classification": classification["classification"],
            "classification_reason": classification["classification_reason"],
            "proposal_emitted": proposal["proposal_emitted"],
            "repair_objective_id": proposal.get("repair_objective_id"),
            "repair_objective_name": proposal.get("repair_objective_name"),
            "localized_repair_surface_refs": proposal.get("localized_repair_surface_refs"),
            "missing_fields_to_expose": proposal.get("missing_fields_to_expose"),
            "recommended_next_handling": packet["recommended_next_handling"],
            "next_if_accepted": packet["next_if_accepted"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "repair_eligibility_guards": guards,
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
    print(f"localized_evidence_surface_repair_eligibility_receipt_id={receipt_id}")
    print(f"localized_evidence_surface_repair_eligibility_receipt_path=data/localized_evidence_surface_repair_eligibility_v0_receipts/{receipt_id}.json")
    print(f"localized_repair_eligibility_classification_path=data/localized_evidence_surface_repair_eligibility_v0/localized_repair_eligibility_classification.json")
    print(f"localized_evidence_surface_repair_objective_proposal_path=data/localized_evidence_surface_repair_eligibility_v0/localized_evidence_surface_repair_objective_proposal.json")
    print(f"localized_repair_eligibility_decision_packet_path=data/localized_evidence_surface_repair_eligibility_v0/localized_repair_eligibility_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
