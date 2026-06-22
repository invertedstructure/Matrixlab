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

UNIT_ID = "CLASSIFY_TAXONOMY_GAP_EVIDENCE_SURFACE_DEFICIENCY_V0"
TARGET_UNIT_ID = "taxonomy_gap_evidence_surface_deficiency_classification.v0"

SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID = "7ed31808"
SOURCE_LOOP_APPLICATION_RECEIPT_ID = "be19f438"
SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID = "6148b4fa"
SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID = "7c9718e0"
SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID = "a121ff40"

TOP_GROUP_KEY_HASH = "38c604a1"
SOURCE_EVIDENCE_REQUEST_ID = "52b0d484"
EXPECTED_FIELD_ROW_COUNT = 25

OUT_DIR = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0"
RECEIPT_DIR = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0_receipts"

FIELD_PRESENCE_ROLLUP_PATH = OUT_DIR / "evidence_surface_field_presence_rollup.json"
DEFICIENCY_CANDIDATES_PATH = OUT_DIR / "evidence_surface_deficiency_candidates.json"
CLASSIFICATION_PATH = OUT_DIR / "evidence_surface_classification.json"
REPAIR_PROPOSAL_PATH = OUT_DIR / "evidence_surface_repair_objective_proposal.json"
DECISION_PACKET_PATH = OUT_DIR / "evidence_surface_decision_packet.json"
REPORT_PATH = OUT_DIR / "evidence_surface_classification_report.json"

EXTRACTION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0_receipts" / f"{SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID}.json"
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

SOURCE_FILES = [
    EXTRACTION_RECEIPT_PATH,
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
]

CLASSIFICATIONS = [
    "FIXABLE_EVIDENCE_SURFACE_DEFICIENCY",
    "HEALTHY_EXPECTED_EVIDENCE_LIMIT",
    "NOT_ENOUGH_EVIDENCE",
]

LOCALIZATION_CLASSES = [
    "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELDS",
    "SCHEMA_HAS_NO_SLOT_FOR_FIELDS",
    "EXTRACTOR_DID_NOT_READ_EXISTING_FIELDS",
    "PRESSURE_LABEL_TOO_COARSE_FOR_FIELD_RECOVERY",
    "INTENTIONALLY_OPAQUE_HUMAN_BOUNDARY",
    "UNKNOWN_SURFACE_DEFICIENCY",
]

MISSING_FIELDS = [
    "missing_label_identifier",
    "taxonomy_context_ref",
    "current_label_space_ref",
    "expected_label_space_ref",
]

REQUIRED_STRUCTURAL_FIELDS = [
    "source_receipt_ref",
    "source_trace_ref",
    "pressure_group_key_hash",
    "parent_pressure_class",
    "pressure_subtype",
    "halt_reason",
]

HUMAN_DECISION = {
    "decision": "CLASSIFY_TAXONOMY_GAP_EVIDENCE_SURFACE_DEFICIENCY",
    "scope": "classification_of_evidence_surface_deficiency_only",
    "source_taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
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
    "taxonomy gap cannot be repaired from missing-label pressure alone",
    "absent fields are not proof of a missing taxonomy label",
    "evidence-surface deficiency may be fixable only if localized",
    "do not emit taxonomy delta",
    "do not upgrade taxonomy",
    "do not execute evidence-surface repair",
    "do not repair extraction in this unit",
    "do not mutate source receipts",
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
        "extraction_receipt": read_json(EXTRACTION_RECEIPT_PATH),
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
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    extraction = sources["extraction_receipt"]
    loop_app = sources["loop_application_receipt"]
    protocol = sources["pressure_loop_protocol_receipt"]
    top = sources["top_group_classification_receipt"]
    packet = sources["source_extraction_packet"]

    if extraction.get("receipt_id") != SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID:
        failures.append("extraction_receipt_id_wrong")
    if extraction.get("gate") != "PASS":
        failures.append("extraction_receipt_not_pass")
    if extraction.get("unit_id") != "EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_V0":
        failures.append("extraction_unit_wrong")
    if extraction.get("source_evidence_request_id") != SOURCE_EVIDENCE_REQUEST_ID:
        failures.append("source_evidence_request_id_wrong")
    if extraction.get("aggregate_metrics", {}).get("field_row_count") != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_row_count_wrong")
    if extraction.get("aggregate_metrics", {}).get("classification_after_extraction") != "NOT_ENOUGH_EVIDENCE":
        failures.append("source_classification_after_wrong")
    if extraction.get("aggregate_metrics", {}).get("evidence_sufficiency_class_after") != "EVIDENCE_INSUFFICIENT_NEEDS_FIELD_EXTRACTION":
        failures.append("source_evidence_class_wrong")
    if extraction.get("aggregate_metrics", {}).get("selected_operational_cause_candidate") != "FIELD_EXTRACTION_SURFACE_LACKS_TAXONOMY_GAP_DETAIL":
        failures.append("source_cause_candidate_wrong")
    for field in [
        "missing_label_identifier_present_count",
        "taxonomy_context_ref_present_count",
        "current_label_space_ref_present_count",
        "expected_label_space_ref_present_count",
    ]:
        if extraction.get("aggregate_metrics", {}).get(field) != 0:
            failures.append(f"expected_zero_field_presence_wrong:{field}")

    if loop_app.get("receipt_id") != SOURCE_LOOP_APPLICATION_RECEIPT_ID or loop_app.get("gate") != "PASS":
        failures.append("loop_application_receipt_not_pass")
    if protocol.get("receipt_id") != SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID or protocol.get("gate") != "PASS":
        failures.append("pressure_loop_protocol_receipt_not_pass")
    if top.get("receipt_id") != SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID or top.get("gate") != "PASS":
        failures.append("top_group_classification_receipt_not_pass")
    if top.get("top_group_summary", {}).get("top_group_key_hash") != TOP_GROUP_KEY_HASH:
        failures.append("top_group_key_wrong")

    if packet.get("packet_type") != "HUMAN_REVIEW_PACKET_NOT_COMMAND":
        failures.append("source_packet_type_wrong")
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
            failures.append(f"source_packet_guard_not_false:{key}:{packet.get(key)}")

    if len(sources["field_rows"]) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_rows_length_wrong")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_field_presence_rollup(sources: Dict[str, Any]) -> Dict[str, Any]:
    rows = sources["field_rows"]
    context_refs = sources["context_refs"]
    extraction = sources["extraction_receipt"]

    missing_field_presence_profile = {
        "missing_label_identifier": sum(1 for row in rows if row.get("missing_label_identifier_present") is True),
        "taxonomy_context_ref": sum(1 for row in rows if row.get("taxonomy_context_ref_present") is True),
        "current_label_space_ref": sum(1 for row in rows if row.get("current_label_space_ref_present") is True),
        "expected_label_space_ref": sum(1 for row in rows if row.get("expected_label_space_ref_present") is True),
    }
    missing_names = [name for name, count in missing_field_presence_profile.items() if count == 0]

    present_structural_field_profile = {
        "source_event_ref": len(rows),
        "source_receipt_ref": sum(1 for row in rows if row.get("source_receipt_ref")),
        "source_trace_ref": sum(1 for row in rows if row.get("source_trace_ref")),
        "pressure_group_key_hash": sum(1 for row in rows if row.get("pressure_group_key_hash") == TOP_GROUP_KEY_HASH),
        "parent_pressure_class": sum(1 for row in rows if row.get("parent_pressure_class") == "TAXONOMY_PRESSURE"),
        "pressure_subtype": sum(1 for row in rows if row.get("pressure_subtype") == "missing_label"),
        "halt_reason": sum(1 for row in rows if row.get("halt_reason") == "STOP_TAXONOMY_GAP"),
    }

    field_absence_distribution = dict(sorted(Counter(row.get("field_status") for row in rows).items()))

    return {
        "schema_version": "evidence_surface_field_presence_rollup_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
        "source_evidence_request_id": SOURCE_EVIDENCE_REQUEST_ID,
        "field_row_count": len(rows),
        "expected_field_row_count": EXPECTED_FIELD_ROW_COUNT,
        "missing_field_names": missing_names,
        "missing_field_count": len(missing_names),
        "missing_field_presence_profile": missing_field_presence_profile,
        "present_structural_field_profile": present_structural_field_profile,
        "field_absence_distribution": field_absence_distribution,
        "source_extraction_summary": extraction.get("extraction_summary", {}),
        "context_refs_summary": {
            "missing_label_identifier_present_count": context_refs.get("missing_label_identifier_present_count"),
            "taxonomy_context_ref_present_count": context_refs.get("taxonomy_context_ref_present_count"),
            "current_label_space_ref_present_count": context_refs.get("current_label_space_ref_present_count"),
            "expected_label_space_ref_present_count": context_refs.get("expected_label_space_ref_present_count"),
            "context_refs_sufficient_for_taxonomy_delta": context_refs.get("context_refs_sufficient_for_taxonomy_delta"),
        },
        "review_only": True,
    }

def build_deficiency_candidates(rollup: Dict[str, Any], sources: Dict[str, Any]) -> Dict[str, Any]:
    source_cause = sources["source_cause_candidates"]
    extraction_report = sources["source_extraction_report"]

    source_surface_candidates = []
    schema_surface_candidates = []
    extraction_logic_candidates = []
    pressure_label_coarseness_candidates = []
    healthy_opacity_candidates = []
    unknown_surface_candidates = []

    source_surface_candidates.append({
        "candidate_id": "SOURCE_PAYLOAD_FIELD_ABSENCE_POSSIBLE",
        "candidate_type": "possible_source_payload_absence",
        "candidate_surface": "source_payload",
        "support_level": "POSSIBLE_NOT_LOCALIZED",
        "supporting_evidence_refs": [rel(FIELD_ROWS_PATH), rel(CONTEXT_REFS_PATH)],
        "missing_fields_explained": rollup["missing_field_names"],
        "localized_repair_target_refs": [],
        "may_support_fixable_surface_repair": False,
        "may_support_healthy_expected_limit": False,
        "supports_not_enough_evidence": True,
        "forbidden_inference": "Do not infer source payload is defective without inspecting raw payload/schema surfaces.",
    })

    schema_surface_candidates.append({
        "candidate_id": "SCHEMA_SLOT_ABSENCE_POSSIBLE",
        "candidate_type": "possible_schema_surface_absence",
        "candidate_surface": "schema_surface",
        "support_level": "POSSIBLE_NOT_LOCALIZED",
        "supporting_evidence_refs": [rel(FIELD_ROWS_PATH), rel(REINSPECTION_ROLLUP_SOURCE_PATH)],
        "missing_fields_explained": rollup["missing_field_names"],
        "localized_repair_target_refs": [],
        "may_support_fixable_surface_repair": False,
        "may_support_healthy_expected_limit": False,
        "supports_not_enough_evidence": True,
        "forbidden_inference": "Do not infer schema repair target without locating the schema slot boundary.",
    })

    extraction_logic_candidates.append({
        "candidate_id": "EXTRACTOR_LOGIC_MISREAD_POSSIBLE",
        "candidate_type": "possible_extractor_logic_gap",
        "candidate_surface": "extractor_logic",
        "support_level": "POSSIBLE_NOT_LOCALIZED",
        "supporting_evidence_refs": [rel(FIELD_EXTRACTION_ASSESSMENT_SOURCE_PATH), rel(EXTRACTION_REPORT_SOURCE_PATH)],
        "missing_fields_explained": rollup["missing_field_names"],
        "localized_repair_target_refs": [],
        "may_support_fixable_surface_repair": False,
        "may_support_healthy_expected_limit": False,
        "supports_not_enough_evidence": True,
        "forbidden_inference": "Do not repair extractor logic until compared against raw source rows.",
    })

    pressure_label_coarseness_candidates.append({
        "candidate_id": "PRESSURE_LABEL_TOO_COARSE_FOR_FIELD_RECOVERY_POSSIBLE",
        "candidate_type": "possible_pressure_label_coarseness",
        "candidate_surface": "pressure_label_coarseness",
        "support_level": "POSSIBLE_NOT_LOCALIZED",
        "supporting_evidence_refs": [rel(CAUSE_CANDIDATES_SOURCE_PATH)],
        "missing_fields_explained": rollup["missing_field_names"],
        "localized_repair_target_refs": [],
        "may_support_fixable_surface_repair": False,
        "may_support_healthy_expected_limit": False,
        "supports_not_enough_evidence": True,
        "forbidden_inference": "Do not treat coarse label as taxonomy delta evidence.",
    })

    healthy_opacity_candidates.append({
        "candidate_id": "INTENTIONAL_OPAQUE_HUMAN_BOUNDARY_NOT_ESTABLISHED",
        "candidate_type": "possible_intentional_opacity",
        "candidate_surface": "intentional_opacity",
        "support_level": "NOT_ESTABLISHED",
        "supporting_evidence_refs": [rel(EXTRACTION_PACKET_SOURCE_PATH)],
        "missing_fields_explained": rollup["missing_field_names"],
        "localized_repair_target_refs": [],
        "may_support_fixable_surface_repair": False,
        "may_support_healthy_expected_limit": False,
        "supports_not_enough_evidence": True,
        "forbidden_inference": "Do not mark healthy opacity without explicit boundary evidence.",
    })

    unknown_surface_candidates.append({
        "candidate_id": "UNKNOWN_SURFACE_DEFICIENCY",
        "candidate_type": "unlocalized_surface_deficiency",
        "candidate_surface": "unknown",
        "support_level": "STRONG",
        "supporting_evidence_refs": [
            rel(EXTRACTION_RECEIPT_PATH),
            rel(FIELD_ROWS_PATH),
            rel(CONTEXT_REFS_PATH),
            rel(CAUSE_CANDIDATES_SOURCE_PATH),
        ],
        "missing_fields_explained": rollup["missing_field_names"],
        "localized_repair_target_refs": [],
        "may_support_fixable_surface_repair": False,
        "may_support_healthy_expected_limit": False,
        "supports_not_enough_evidence": True,
        "forbidden_inference": "Missing fields prove evidence surface insufficiency, not the repair location.",
    })

    all_candidates = (
        source_surface_candidates
        + schema_surface_candidates
        + extraction_logic_candidates
        + pressure_label_coarseness_candidates
        + healthy_opacity_candidates
        + unknown_surface_candidates
    )

    selected = unknown_surface_candidates[0]

    return {
        "schema_version": "evidence_surface_deficiency_candidates_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
        "source_surface_candidates": source_surface_candidates,
        "schema_surface_candidates": schema_surface_candidates,
        "extraction_logic_candidates": extraction_logic_candidates,
        "pressure_label_coarseness_candidates": pressure_label_coarseness_candidates,
        "healthy_opacity_candidates": healthy_opacity_candidates,
        "unknown_surface_candidates": unknown_surface_candidates,
        "all_candidates": all_candidates,
        "candidate_count": len(all_candidates),
        "selected_deficiency_candidate": selected["candidate_id"],
        "selected_deficiency_support_level": selected["support_level"],
        "localized_repair_target_found": False,
        "localized_repair_target_refs": [],
        "classification_bias": "NOT_ENOUGH_EVIDENCE",
        "source_cause_candidate": source_cause.get("selected_operational_cause_candidate"),
        "source_cause_support_level": source_cause.get("selected_candidate_support_level"),
        "repair_objective_proposal_emitted": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "review_only": True,
    }

def classify_surface(rollup: Dict[str, Any], candidates: Dict[str, Any]) -> Dict[str, Any]:
    localized = candidates["localized_repair_target_found"]
    healthy_established = any(c["may_support_healthy_expected_limit"] for c in candidates["all_candidates"])
    fixable_supported = localized and any(c["may_support_fixable_surface_repair"] for c in candidates["all_candidates"])

    if fixable_supported:
        classification = "FIXABLE_EVIDENCE_SURFACE_DEFICIENCY"
        reason = "Evidence surface deficiency is localized to a concrete repair target."
        evidence_request_emitted = False
    elif healthy_established:
        classification = "HEALTHY_EXPECTED_EVIDENCE_LIMIT"
        reason = "Evidence absence is explicitly established as an intentional/healthy opaque boundary."
        evidence_request_emitted = False
    else:
        classification = "NOT_ENOUGH_EVIDENCE"
        reason = "Missing fields are confirmed, but current receipts do not localize whether source payload, schema surface, extractor logic, label coarseness, or intentional opacity caused the absence."
        evidence_request_emitted = True

    return {
        "schema_version": "evidence_surface_classification_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": classification,
        "classification_classes": CLASSIFICATIONS,
        "classified_exactly_once": True,
        "classification_priority": [
            "NOT_ENOUGH_EVIDENCE",
            "HEALTHY_EXPECTED_EVIDENCE_LIMIT",
            "FIXABLE_EVIDENCE_SURFACE_DEFICIENCY",
        ],
        "classification_reason": reason,
        "missing_field_names": rollup["missing_field_names"],
        "missing_field_count": rollup["missing_field_count"],
        "selected_deficiency_candidate": candidates["selected_deficiency_candidate"],
        "selected_deficiency_support_level": candidates["selected_deficiency_support_level"],
        "localized_repair_target_found": localized,
        "localized_repair_target_refs": candidates["localized_repair_target_refs"],
        "fixable_surface_repair_supported": classification == "FIXABLE_EVIDENCE_SURFACE_DEFICIENCY",
        "healthy_expected_limit_supported": classification == "HEALTHY_EXPECTED_EVIDENCE_LIMIT",
        "not_enough_evidence_supported": classification == "NOT_ENOUGH_EVIDENCE",
        "evidence_request_emitted": evidence_request_emitted,
        "recommended_next_evidence_unit": "AUDIT_TAXONOMY_GAP_EVIDENCE_SURFACE_LOCALIZATION_V0" if evidence_request_emitted else None,
        "repair_objective_proposal_emitted": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "extraction_repair_executed": False,
        "source_mutation": False,
        "build_command_emitted": False,
        "review_only": True,
    }

def build_repair_proposal(classification: Dict[str, Any], rollup: Dict[str, Any], candidates: Dict[str, Any]) -> Dict[str, Any]:
    if classification["classification"] != "FIXABLE_EVIDENCE_SURFACE_DEFICIENCY":
        return {
            "schema_version": "evidence_surface_repair_objective_proposal_v0",
            "proposal_emitted": False,
            "reason": "classification_not_fixable",
            "classification": classification["classification"],
            "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "source_evidence_refs": [
                rel(EXTRACTION_RECEIPT_PATH),
                rel(FIELD_ROWS_PATH),
                rel(CONTEXT_REFS_PATH),
                rel(DEFICIENCY_CANDIDATES_PATH),
            ],
            "repair_command_emitted": False,
            "repair_executed": False,
            "taxonomy_upgrade_authorized": False,
            "taxonomy_delta_proposal_emitted": False,
            "authority_widening_authorized": False,
            "optimization_authorized": False,
            "source_mutation": False,
        }

    return {
        "schema_version": "evidence_surface_repair_objective_proposal_v0",
        "proposal_emitted": True,
        "proposal_type": "EVIDENCE_SURFACE_REPAIR_OBJECTIVE_PROPOSAL",
        "repair_objective_id": "REPAIR_TAXONOMY_GAP_EVIDENCE_SURFACE_FIELD_VISIBILITY_V0",
        "repair_scope": "Expose or preserve missing-label evidence fields in the localized evidence surface without deciding taxonomy delta.",
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_evidence_refs": [
            rel(EXTRACTION_RECEIPT_PATH),
            rel(FIELD_ROWS_PATH),
            rel(CONTEXT_REFS_PATH),
        ],
        "missing_fields_to_expose": rollup["missing_field_names"],
        "candidate_files_or_modules_to_inspect": candidates["localized_repair_target_refs"],
        "candidate_schemas_to_update_or_verify": candidates["localized_repair_target_refs"],
        "expected_acceptance_gates": [
            "missing fields emitted or explicitly null with reason",
            "source receipt refs preserved",
            "source trace refs preserved",
            "no taxonomy delta proposed",
            "no taxonomy upgrade authorized",
            "rerun field extraction",
        ],
        "rerun_required_after_repair": True,
        "forbidden_scope": [
            "taxonomy upgrade",
            "taxonomy delta proposal",
            "authority widening",
            "burden optimization",
            "repair execution inside this unit",
            "guessing missing label values",
            "mutating source receipts",
        ],
        "terminal_rule": "STOP_HUMAN_DECISION_REQUIRED",
        "repair_command_emitted": False,
        "repair_executed": False,
        "taxonomy_upgrade_authorized": False,
        "taxonomy_delta_proposal_emitted": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "source_mutation": False,
    }

def build_decision_packet(classification: Dict[str, Any], repair_proposal: Dict[str, Any]) -> Dict[str, Any]:
    allowed = [
        "ACCEPT_EVIDENCE_SURFACE_REPAIR_OBJECTIVE",
        "MARK_EVIDENCE_LIMIT_HEALTHY_AND_SKIP_GROUP",
        "REQUEST_DEEPER_EVIDENCE_SURFACE_AUDIT",
        "COMPARE_EXTRACTION_LOGIC_WITH_RAW_SOURCE_ROWS",
        "REJECT_EVIDENCE_SURFACE_CLASSIFICATION",
    ]
    if classification["classification"] == "FIXABLE_EVIDENCE_SURFACE_DEFICIENCY":
        recommended = "ACCEPT_EVIDENCE_SURFACE_REPAIR_OBJECTIVE"
    elif classification["classification"] == "HEALTHY_EXPECTED_EVIDENCE_LIMIT":
        recommended = "MARK_EVIDENCE_LIMIT_HEALTHY_AND_SKIP_GROUP"
    else:
        recommended = "REQUEST_DEEPER_EVIDENCE_SURFACE_AUDIT"

    evidence_request_id = sha8({
        "unit_id": UNIT_ID,
        "classification": classification["classification"],
        "selected_deficiency_candidate": classification["selected_deficiency_candidate"],
        "missing_fields": classification["missing_field_names"],
    })

    return {
        "schema_version": "evidence_surface_decision_packet_v0",
        "packet_type": "HUMAN_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": classification["classification"],
        "classification_reason": classification["classification_reason"],
        "allowed_human_choices": allowed,
        "recommended_next_handling": recommended,
        "evidence_request_emitted": classification["classification"] == "NOT_ENOUGH_EVIDENCE",
        "evidence_request_id": evidence_request_id if classification["classification"] == "NOT_ENOUGH_EVIDENCE" else None,
        "required_next_evidence": [
            "inspect extraction builder/source to distinguish missing source fields from missing extractor logic",
            "inspect schema for whether taxonomy context fields are representable",
            "inspect receipt rows for raw payload carrying hidden label context",
            "compare top-group raw rows against source pressure events",
            "manual audit of representative fragments",
        ] if classification["classification"] == "NOT_ENOUGH_EVIDENCE" else [],
        "recommended_next_evidence_unit": classification["recommended_next_evidence_unit"],
        "repair_objective_proposal_emitted": repair_proposal["proposal_emitted"],
        "acceptance_recommendation": classification["classification"] == "HEALTHY_EXPECTED_EVIDENCE_LIMIT",
        "skip_current_pressure_group": classification["classification"] == "HEALTHY_EXPECTED_EVIDENCE_LIMIT",
        "next_group_rank_to_inspect": 2 if classification["classification"] == "HEALTHY_EXPECTED_EVIDENCE_LIMIT" else None,
        "may_emit_repair_command": False,
        "may_emit_build_command": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_taxonomy_delta": False,
        "may_authorize_authority_widening": False,
        "may_authorize_burden_optimization": False,
        "may_execute_extraction_repair": False,
        "may_adopt_protocol": False,
        "may_auto_open_next_group": False,
        "review_only": True,
    }

def build_report(rollup: Dict[str, Any], candidates: Dict[str, Any], classification: Dict[str, Any], repair_proposal: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "evidence_surface_classification_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
            "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
            "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
            "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
            "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        },
        "field_presence_rollup": rollup,
        "deficiency_candidate_summary": {
            "selected_deficiency_candidate": candidates["selected_deficiency_candidate"],
            "selected_deficiency_support_level": candidates["selected_deficiency_support_level"],
            "localized_repair_target_found": candidates["localized_repair_target_found"],
            "candidate_count": candidates["candidate_count"],
        },
        "classification_summary": classification,
        "repair_objective_proposal_emitted": repair_proposal["proposal_emitted"],
        "decision_packet_recommended_next_handling": packet["recommended_next_handling"],
        "action_executed": False,
        "repair_command_emitted": False,
        "repair_executed": False,
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

def validate_outputs(rollup: Dict[str, Any], candidates: Dict[str, Any], classification: Dict[str, Any], repair_proposal: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if rollup["field_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_row_count_wrong")
    if rollup["expected_field_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("expected_field_row_count_wrong")
    if sorted(rollup["missing_field_names"]) != sorted(MISSING_FIELDS):
        failures.append("missing_fields_not_reported")
    if rollup["missing_field_count"] != len(MISSING_FIELDS):
        failures.append("missing_field_count_wrong")
    for field in MISSING_FIELDS:
        if field not in rollup["missing_field_presence_profile"]:
            failures.append(f"missing_field_profile_absent:{field}")
        if rollup["missing_field_presence_profile"].get(field) != 0:
            failures.append(f"missing_field_presence_not_zero:{field}:{rollup['missing_field_presence_profile'].get(field)}")
    for field in ["source_event_ref", "source_receipt_ref", "source_trace_ref", "pressure_group_key_hash", "parent_pressure_class", "pressure_subtype", "halt_reason"]:
        if field not in rollup["present_structural_field_profile"]:
            failures.append(f"present_structural_field_missing:{field}")
        if rollup["present_structural_field_profile"].get(field) != EXPECTED_FIELD_ROW_COUNT:
            failures.append(f"present_structural_field_count_wrong:{field}:{rollup['present_structural_field_profile'].get(field)}")

    for group_name in [
        "source_surface_candidates",
        "schema_surface_candidates",
        "extraction_logic_candidates",
        "pressure_label_coarseness_candidates",
        "healthy_opacity_candidates",
        "unknown_surface_candidates",
    ]:
        if not candidates.get(group_name):
            failures.append(f"deficiency_candidate_group_missing:{group_name}")

    if candidates["candidate_count"] < 1:
        failures.append("deficiency_candidates_missing")
    if candidates["selected_deficiency_candidate"] != "UNKNOWN_SURFACE_DEFICIENCY":
        failures.append("selected_deficiency_candidate_wrong")
    if candidates["localized_repair_target_found"] is not False:
        failures.append("localized_repair_target_unexpected")
    if candidates["localized_repair_target_refs"] != []:
        failures.append("localized_repair_target_refs_unexpected")
    for candidate in candidates["all_candidates"]:
        for field in [
            "candidate_id",
            "candidate_type",
            "candidate_surface",
            "support_level",
            "supporting_evidence_refs",
            "missing_fields_explained",
            "localized_repair_target_refs",
            "may_support_fixable_surface_repair",
            "may_support_healthy_expected_limit",
            "supports_not_enough_evidence",
            "forbidden_inference",
        ]:
            if field not in candidate:
                failures.append(f"candidate_field_missing:{candidate.get('candidate_id')}:{field}")

    if classification["classification"] not in CLASSIFICATIONS:
        failures.append("invalid_classification")
    if classification["classified_exactly_once"] is not True:
        failures.append("not_classified_exactly_once")
    class_flags = [
        classification["fixable_surface_repair_supported"],
        classification["healthy_expected_limit_supported"],
        classification["not_enough_evidence_supported"],
    ]
    if sum(1 for flag in class_flags if flag is True) != 1:
        failures.append("classification_multiple_classes")
    if classification["classification"] == "FIXABLE_EVIDENCE_SURFACE_DEFICIENCY" and candidates["localized_repair_target_found"] is not True:
        failures.append("fixable_without_localized_surface")
    if classification["classification"] == "FIXABLE_EVIDENCE_SURFACE_DEFICIENCY" and not rollup["missing_field_names"]:
        failures.append("fixable_without_missing_fields")
    if classification["classification"] == "HEALTHY_EXPECTED_EVIDENCE_LIMIT" and repair_proposal["proposal_emitted"] is True:
        failures.append("healthy_limit_emits_repair")
    if classification["classification"] == "NOT_ENOUGH_EVIDENCE" and repair_proposal["proposal_emitted"] is True:
        failures.append("not_enough_evidence_emits_repair")
    for key in [
        "repair_objective_proposal_emitted",
        "taxonomy_delta_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "extraction_repair_executed",
        "source_mutation",
        "build_command_emitted",
    ]:
        if classification.get(key) is not False:
            failures.append(f"classification_guard_not_false:{key}:{classification.get(key)}")

    if classification["classification"] == "FIXABLE_EVIDENCE_SURFACE_DEFICIENCY":
        if repair_proposal["proposal_emitted"] is not True:
            failures.append("fixable_without_repair_scope")
        for field in [
            "repair_objective_id",
            "repair_scope",
            "source_pressure_group_key_hash",
            "source_evidence_refs",
            "missing_fields_to_expose",
            "candidate_files_or_modules_to_inspect",
            "candidate_schemas_to_update_or_verify",
            "expected_acceptance_gates",
            "rerun_required_after_repair",
            "forbidden_scope",
            "terminal_rule",
        ]:
            if field not in repair_proposal:
                failures.append(f"fixable_proposal_field_missing:{field}")
        if not repair_proposal.get("candidate_files_or_modules_to_inspect"):
            failures.append("fixable_without_candidate_target_refs")
    else:
        if repair_proposal["proposal_emitted"] is not False:
            failures.append("proposal_emitted_for_non_fixable")
        if repair_proposal.get("reason") != "classification_not_fixable":
            failures.append("non_fixable_proposal_reason_wrong")

    for key in [
        "repair_command_emitted",
        "repair_executed",
        "taxonomy_upgrade_authorized",
        "taxonomy_delta_proposal_emitted",
        "authority_widening_authorized",
        "optimization_authorized",
        "source_mutation",
    ]:
        if repair_proposal.get(key) is not False:
            failures.append(f"proposal_guard_not_false:{key}:{repair_proposal.get(key)}")

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
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")

    for key in [
        "action_executed",
        "repair_command_emitted",
        "repair_executed",
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
    if receipt.get("source_taxonomy_gap_evidence_extraction_receipt_id") != SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID:
        failures.append("source_extraction_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "EVIDENCE_SURFACE_0_SOURCE_SURFACE_VERIFIED",
        "EVIDENCE_SURFACE_1_HUMAN_DECISION_RECORDED",
        "EVIDENCE_SURFACE_2_EXTRACTION_RECEIPT_CONSUMED",
        "EVIDENCE_SURFACE_3_FIELD_ROWS_CONSUMED",
        "EVIDENCE_SURFACE_4_MISSING_FIELDS_IDENTIFIED",
        "EVIDENCE_SURFACE_5_DEFICIENCY_CANDIDATES_EMITTED",
        "EVIDENCE_SURFACE_6_DEFICIENCY_LOCALIZATION_EMITTED",
        "EVIDENCE_SURFACE_7_CLASSIFIED_EXACTLY_ONCE",
        "EVIDENCE_SURFACE_8_REPAIR_PROPOSAL_ONLY_IF_FIXABLE",
        "EVIDENCE_SURFACE_9_DECISION_PACKET_EMITTED",
        "EVIDENCE_SURFACE_10_NO_TAXONOMY_DELTA_OR_UPGRADE",
        "EVIDENCE_SURFACE_11_NO_ACTION_EXECUTED",
        "EVIDENCE_SURFACE_12_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("classification") not in CLASSIFICATIONS:
        failures.append("metric_classification_invalid")
    if metrics.get("field_row_count") != EXPECTED_FIELD_ROW_COUNT:
        failures.append("metric_field_row_count_wrong")
    if metrics.get("missing_field_count") != len(MISSING_FIELDS):
        failures.append("metric_missing_field_count_wrong")
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

    guards = receipt.get("evidence_surface_guards", {})
    for key in [
        "source_surface_verified",
        "human_decision_recorded",
        "extraction_receipt_consumed",
        "field_rows_consumed",
        "missing_fields_identified",
        "deficiency_candidates_emitted",
        "deficiency_localization_emitted",
        "classified_exactly_once",
        "decision_packet_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "repair_command_emitted",
        "build_command_emitted",
        "repair_executed",
        "repair_objective_proposal_emitted_unless_fixable",
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

    rollup = build_field_presence_rollup(sources)
    candidates = build_deficiency_candidates(rollup, sources)
    classification = classify_surface(rollup, candidates)
    repair_proposal = build_repair_proposal(classification, rollup, candidates)
    packet = build_decision_packet(classification, repair_proposal)
    report = build_report(rollup, candidates, classification, repair_proposal, packet)

    write_json(FIELD_PRESENCE_ROLLUP_PATH, rollup)
    write_json(DEFICIENCY_CANDIDATES_PATH, candidates)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(REPAIR_PROPOSAL_PATH, repair_proposal)
    write_json(DECISION_PACKET_PATH, packet)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(rollup, candidates, classification, repair_proposal, packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "EVIDENCE_SURFACE_0_SOURCE_SURFACE_VERIFIED": len(validate_sources(sources)) == 0,
        "EVIDENCE_SURFACE_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "CLASSIFY_TAXONOMY_GAP_EVIDENCE_SURFACE_DEFICIENCY",
        "EVIDENCE_SURFACE_2_EXTRACTION_RECEIPT_CONSUMED": sources["extraction_receipt"]["receipt_id"] == SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
        "EVIDENCE_SURFACE_3_FIELD_ROWS_CONSUMED": len(sources["field_rows"]) == EXPECTED_FIELD_ROW_COUNT,
        "EVIDENCE_SURFACE_4_MISSING_FIELDS_IDENTIFIED": sorted(rollup["missing_field_names"]) == sorted(MISSING_FIELDS),
        "EVIDENCE_SURFACE_5_DEFICIENCY_CANDIDATES_EMITTED": DEFICIENCY_CANDIDATES_PATH.exists() and candidates["candidate_count"] >= 1,
        "EVIDENCE_SURFACE_6_DEFICIENCY_LOCALIZATION_EMITTED": "localized_repair_target_found" in candidates and "localized_repair_target_refs" in candidates,
        "EVIDENCE_SURFACE_7_CLASSIFIED_EXACTLY_ONCE": classification["classified_exactly_once"] is True and classification["classification"] in CLASSIFICATIONS,
        "EVIDENCE_SURFACE_8_REPAIR_PROPOSAL_ONLY_IF_FIXABLE": (repair_proposal["proposal_emitted"] is True) == (classification["classification"] == "FIXABLE_EVIDENCE_SURFACE_DEFICIENCY"),
        "EVIDENCE_SURFACE_9_DECISION_PACKET_EMITTED": DECISION_PACKET_PATH.exists(),
        "EVIDENCE_SURFACE_10_NO_TAXONOMY_DELTA_OR_UPGRADE": classification["taxonomy_delta_proposal_emitted"] is False and classification["taxonomy_upgrade_authorized"] is False,
        "EVIDENCE_SURFACE_11_NO_ACTION_EXECUTED": report["action_executed"] is False and report["repair_executed"] is False,
        "EVIDENCE_SURFACE_12_NO_SOURCE_MUTATION": source_mutation_detected is False,
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
        "source_taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
        "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
        "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "field_row_count": rollup["field_row_count"],
        "expected_field_row_count": rollup["expected_field_row_count"],
        "missing_field_names": rollup["missing_field_names"],
        "missing_field_count": rollup["missing_field_count"],
        "selected_deficiency_candidate": candidates["selected_deficiency_candidate"],
        "selected_deficiency_support_level": candidates["selected_deficiency_support_level"],
        "localized_repair_target_found": candidates["localized_repair_target_found"],
        "classification": classification["classification"],
        "classified_exactly_once": classification["classified_exactly_once"],
        "repair_objective_proposal_emitted": repair_proposal["proposal_emitted"],
        "evidence_request_emitted": classification["evidence_request_emitted"],
        "recommended_next_evidence_unit": classification["recommended_next_evidence_unit"],
        "repair_command_emitted_count": 0,
        "build_command_emitted_count": 0,
        "repair_executed_count": 0,
        "repair_objective_proposal_emitted_count": 1 if repair_proposal["proposal_emitted"] else 0,
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
        "extraction_receipt_consumed": True,
        "field_rows_consumed": True,
        "missing_fields_identified": True,
        "deficiency_candidates_emitted": True,
        "deficiency_localization_emitted": True,
        "classified_exactly_once": True,
        "repair_proposal_only_if_fixable": acceptance_gate_results["EVIDENCE_SURFACE_8_REPAIR_PROPOSAL_ONLY_IF_FIXABLE"],
        "decision_packet_emitted": True,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "repair_executed": False,
        "repair_objective_proposal_emitted_unless_fixable": False,
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
        "source_extraction_receipt": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
        "classification": classification["classification"],
        "selected_deficiency_candidate": candidates["selected_deficiency_candidate"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "evidence_surface_field_presence_rollup": rel(FIELD_PRESENCE_ROLLUP_PATH),
        "evidence_surface_deficiency_candidates": rel(DEFICIENCY_CANDIDATES_PATH),
        "evidence_surface_classification": rel(CLASSIFICATION_PATH),
        "evidence_surface_repair_objective_proposal": rel(REPAIR_PROPOSAL_PATH),
        "evidence_surface_decision_packet": rel(DECISION_PACKET_PATH),
        "evidence_surface_classification_report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "taxonomy_gap_evidence_surface_deficiency_classification_receipt_v0",
        "receipt_type": "TAXONOMY_GAP_EVIDENCE_SURFACE_DEFICIENCY_CLASSIFICATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
        "source_loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
        "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "classification_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "classification": classification["classification"],
            "classification_reason": classification["classification_reason"],
            "selected_deficiency_candidate": candidates["selected_deficiency_candidate"],
            "selected_deficiency_support_level": candidates["selected_deficiency_support_level"],
            "localized_repair_target_found": candidates["localized_repair_target_found"],
            "missing_field_names": rollup["missing_field_names"],
            "repair_objective_proposal_emitted": repair_proposal["proposal_emitted"],
            "recommended_next_handling": packet["recommended_next_handling"],
            "recommended_next_evidence_unit": packet["recommended_next_evidence_unit"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "evidence_surface_guards": guards,
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
    print(f"taxonomy_gap_evidence_surface_deficiency_classification_receipt_id={receipt_id}")
    print(f"taxonomy_gap_evidence_surface_deficiency_classification_receipt_path=data/taxonomy_gap_evidence_surface_deficiency_v0_receipts/{receipt_id}.json")
    print(f"evidence_surface_classification_path=data/taxonomy_gap_evidence_surface_deficiency_v0/evidence_surface_classification.json")
    print(f"evidence_surface_decision_packet_path=data/taxonomy_gap_evidence_surface_deficiency_v0/evidence_surface_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
