#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REFINE_NULL_EVIDENCE_LIMIT_INTO_FIELD_INTRODUCTION_BOUNDARY_V0"
TARGET_UNIT_ID = "null_evidence_field_introduction_boundary_refinement.v0"

SOURCE_NULL_LIMIT_RECEIPT_ID = "9e2c2881"
SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID = "b554aace"
FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID = "b113463f"
SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID = "d6d40d57"
FAILED_REPAIR_RECEIPT_ID = "1856cb99"
SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID = "ecebcd27"
SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID = "bea59318"
SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID = "707dd84d"
SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID = "7ed31808"
SOURCE_LOOP_APPLICATION_RECEIPT_ID = "be19f438"
SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID = "6148b4fa"
SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID = "7c9718e0"
SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID = "a121ff40"

TOP_GROUP_KEY_HASH = "38c604a1"
EXPECTED_FIELD_ROW_COUNT = 25

PROPOSED_FIELDS = [
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

OUT_DIR = ROOT / "data" / "null_evidence_field_introduction_boundary_refinement_v0"
RECEIPT_DIR = ROOT / "data" / "null_evidence_field_introduction_boundary_refinement_v0_receipts"

BOUNDARY_REFINEMENT_PATH = OUT_DIR / "field_introduction_boundary_refinement.json"
EXISTENCE_STATUS_PATH = OUT_DIR / "field_existence_status_assessment.json"
FIELD_INTRODUCTION_PROPOSAL_PATH = OUT_DIR / "source_provenance_field_introduction_proposal.json"
DECISION_PACKET_PATH = OUT_DIR / "field_introduction_decision_packet.json"
REFINEMENT_REPORT_PATH = OUT_DIR / "field_introduction_boundary_refinement_report.json"

NULL_LIMIT_RECEIPT_PATH = ROOT / "data" / "repaired_surface_null_evidence_limit_classification_v0_receipts" / f"{SOURCE_NULL_LIMIT_RECEIPT_ID}.json"
NULL_LIMIT_INPUT_ROLLUP_PATH = ROOT / "data" / "repaired_surface_null_evidence_limit_classification_v0" / "null_evidence_limit_input_rollup.json"
ABSENCE_REASON_CLASSIFICATION_PATH = ROOT / "data" / "repaired_surface_null_evidence_limit_classification_v0" / "absence_reason_classification.json"
NULL_LIMIT_CLASSIFICATION_PATH = ROOT / "data" / "repaired_surface_null_evidence_limit_classification_v0" / "null_evidence_limit_classification.json"
OLD_SOURCE_PROVENANCE_REPAIR_PROPOSAL_PATH = ROOT / "data" / "repaired_surface_null_evidence_limit_classification_v0" / "source_provenance_repair_objective_proposal.json"
OLD_NULL_LIMIT_PACKET_PATH = ROOT / "data" / "repaired_surface_null_evidence_limit_classification_v0" / "null_evidence_limit_decision_packet.json"
NULL_LIMIT_REPORT_PATH = ROOT / "data" / "repaired_surface_null_evidence_limit_classification_v0" / "null_evidence_limit_report.json"

COMPARISON_GATE_FIX_RECEIPT_PATH = ROOT / "data" / "repaired_surface_rerun_comparison_gate_fix_v0_receipts" / f"{SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID}.json"
FAILED_RERUN_RECEIPT_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0_receipts" / f"{FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID}.json"
RERUN_FIELD_ROWS_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_taxonomy_gap_missing_label_field_rows.jsonl"
STRUCTURAL_REF_FIX_RECEIPT_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0_receipts" / f"{SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID}.json"
REPAIR_ELIGIBILITY_RECEIPT_PATH = ROOT / "data" / "localized_evidence_surface_repair_eligibility_v0_receipts" / f"{SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID}.json"
LOCALIZATION_RECEIPT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0_receipts" / f"{SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID}.json"
EVIDENCE_SURFACE_RECEIPT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0_receipts" / f"{SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID}.json"
PRE_REPAIR_EXTRACTION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0_receipts" / f"{SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID}.json"
LOOP_APPLICATION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0_receipts" / f"{SOURCE_LOOP_APPLICATION_RECEIPT_ID}.json"
PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID}.json"
TOP_GROUP_CLASSIFICATION_RECEIPT_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0_receipts" / f"{SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID}.json"
R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"

SOURCE_FILES = [
    NULL_LIMIT_RECEIPT_PATH,
    NULL_LIMIT_INPUT_ROLLUP_PATH,
    ABSENCE_REASON_CLASSIFICATION_PATH,
    NULL_LIMIT_CLASSIFICATION_PATH,
    OLD_SOURCE_PROVENANCE_REPAIR_PROPOSAL_PATH,
    OLD_NULL_LIMIT_PACKET_PATH,
    NULL_LIMIT_REPORT_PATH,
    COMPARISON_GATE_FIX_RECEIPT_PATH,
    FAILED_RERUN_RECEIPT_PATH,
    RERUN_FIELD_ROWS_PATH,
    STRUCTURAL_REF_FIX_RECEIPT_PATH,
    REPAIR_ELIGIBILITY_RECEIPT_PATH,
    LOCALIZATION_RECEIPT_PATH,
    EVIDENCE_SURFACE_RECEIPT_PATH,
    PRE_REPAIR_EXTRACTION_RECEIPT_PATH,
    LOOP_APPLICATION_RECEIPT_PATH,
    PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH,
    TOP_GROUP_CLASSIFICATION_RECEIPT_PATH,
    R1000_SCALE_RECEIPT_PATH,
]

HUMAN_DECISION = {
    "decision": "REFINE_NULL_EVIDENCE_LIMIT_INTO_FIELD_INTRODUCTION_BOUNDARY",
    "scope": "replace repair-biased next object with typed field-introduction proposition boundary",
    "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
    "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
    "not_authorized": [
        "field_creation",
        "schema_mutation",
        "source_payload_mutation",
        "taxonomy_repair",
        "taxonomy_upgrade",
        "taxonomy_delta_proposal",
        "authority_widening",
        "burden_optimization",
        "guessing_missing_label_values",
        "source_provenance_repair_execution",
        "mutating_existing_receipts",
        "overwriting_historical_source_rows",
        "protocol_adoption",
        "next_group_auto_open",
        "build_command",
    ],
}

MUST_NOT_INFER = [
    "field-introduction proposal is not field creation",
    "nonexistent or unrepresented required field must be proposed, not invented",
    "source payload absence does not prove upstream existence",
    "if values exist upstream, use provenance/extraction repair",
    "if values do not exist in the source model, use field-introduction proposal",
    "do not mutate existing receipts",
    "do not emit taxonomy delta",
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
        "null_limit_receipt": read_json(NULL_LIMIT_RECEIPT_PATH),
        "null_limit_input_rollup": read_json(NULL_LIMIT_INPUT_ROLLUP_PATH),
        "absence_reason_classification": read_json(ABSENCE_REASON_CLASSIFICATION_PATH),
        "null_limit_classification": read_json(NULL_LIMIT_CLASSIFICATION_PATH),
        "old_source_provenance_repair_proposal": read_json(OLD_SOURCE_PROVENANCE_REPAIR_PROPOSAL_PATH),
        "old_null_limit_packet": read_json(OLD_NULL_LIMIT_PACKET_PATH),
        "null_limit_report": read_json(NULL_LIMIT_REPORT_PATH),
        "comparison_gate_fix_receipt": read_json(COMPARISON_GATE_FIX_RECEIPT_PATH),
        "failed_rerun_receipt": read_json(FAILED_RERUN_RECEIPT_PATH),
        "rerun_field_rows": read_jsonl(RERUN_FIELD_ROWS_PATH),
        "structural_ref_fix_receipt": read_json(STRUCTURAL_REF_FIX_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    receipt = sources["null_limit_receipt"]
    metrics = receipt.get("aggregate_metrics", {})

    if receipt.get("receipt_id") != SOURCE_NULL_LIMIT_RECEIPT_ID:
        failures.append("null_limit_receipt_id_wrong")
    if receipt.get("gate") != "PASS":
        failures.append("null_limit_not_pass")
    if metrics.get("classification") != "SOURCE_CONTENT_PROVENANCE_ABSENT_REPAIRABLE":
        failures.append("source_classification_not_expected_old_value")
    if metrics.get("absence_reason_class") != "SOURCE_PAYLOAD_DOES_NOT_EMIT_REQUIRED_VALUES":
        failures.append("absence_reason_not_source_payload")
    if metrics.get("any_required_field_value_present") is not False:
        failures.append("unexpected_value_presence")
    if metrics.get("source_provenance_repair_proposal_emitted") is not True:
        failures.append("old_proposal_not_emitted")
    if metrics.get("source_mutation_count") != 0:
        failures.append("source_mutation_in_old_receipt")
    if metrics.get("missing_label_value_guess_count") != 0:
        failures.append("label_guess_in_old_receipt")

    if len(sources["rerun_field_rows"]) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_row_count_wrong")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_existence_status(sources: Dict[str, Any]) -> Dict[str, Any]:
    field_rows = sources["rerun_field_rows"]
    absence_profile = {
        field: dict(sorted(Counter(row.get(ABSENCE_REASON_FIELDS[field]) for row in field_rows).items(), key=lambda item: str(item[0])))
        for field in PROPOSED_FIELDS
    }
    value_profile = {
        field: sum(1 for row in field_rows if row.get(field) is not None)
        for field in PROPOSED_FIELDS
    }
    key_profile = {
        field: sum(1 for row in field_rows if row.get(f"{field}_key_present") is True or field in row)
        for field in PROPOSED_FIELDS
    }

    return {
        "schema_version": "field_existence_status_assessment_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "field_row_count": len(field_rows),
        "proposed_fields": PROPOSED_FIELDS,
        "key_presence_profile": key_profile,
        "value_presence_profile": value_profile,
        "absence_reason_profile": absence_profile,
        "current_source_surface": "repaired evidence overlay with explicit null-with-reason keys",
        "current_source_surface_status": "FIELDS_VISIBLE_VALUES_ABSENT",
        "current_source_payload_emits_values": False,
        "upstream_value_existence_status": "NOT_ESTABLISHED_BY_CURRENT_EVIDENCE",
        "field_introduction_boundary_status": "NONEXISTENT_OR_UNREPRESENTED_FIELD_REQUIRED_FOR_CONTINUATION",
        "repair_vs_introduction_boundary": {
            "if_value_exists_upstream": "PROVENANCE_OR_EXTRACTION_REPAIR",
            "if_value_does_not_exist_upstream": "FIELD_INTRODUCTION_PROPOSAL",
            "current_evidence_supports": "FIELD_INTRODUCTION_PROPOSAL_AS_HUMAN_REVIEW_OBJECT",
        },
        "taxonomy_delta_evidence_present": False,
        "taxonomy_upgrade_evidence_present": False,
        "missing_label_values_guessed": False,
        "field_creation_executed": False,
        "schema_mutation_executed": False,
        "source_payload_mutation_executed": False,
        "review_only": True,
    }

def build_boundary_refinement(existence: Dict[str, Any], sources: Dict[str, Any]) -> Dict[str, Any]:
    old = sources["null_limit_receipt"]["aggregate_metrics"]
    return {
        "schema_version": "field_introduction_boundary_refinement_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "old_classification": old.get("classification"),
        "old_next_if_accepted": old.get("next_if_accepted"),
        "old_problem": "The prior next object was repair-biased; it implied source provenance repair before distinguishing upstream value existence from required field introduction.",
        "refined_classification": "NONEXISTENT_OR_UNREPRESENTED_FIELD_REQUIRED_FOR_CONTINUATION",
        "refined_action": "PROPOSE_FIELD_INTRODUCTION",
        "refined_next_object": "PROPOSE_SOURCE_PROVENANCE_FIELD_INTRODUCTION_V0",
        "boundary_law": "The loop may expose fields required for continuation, but may not create or populate fields that never existed without human-authorized introduction.",
        "case_split": {
            "case_1_value_exists_somewhere": {
                "condition": "Required values exist upstream but current receipt/extraction/provenance surface does not expose them.",
                "allowed_action": "repair evidence surface, extraction, or provenance pointer",
            },
            "case_2_value_never_existed_in_source_payload": {
                "condition": "Required values are not represented by the source payload/model.",
                "allowed_action": "emit typed field-introduction proposal and stop for human decision",
            },
        },
        "current_evidence_position": existence["field_introduction_boundary_status"],
        "current_source_payload_emits_values": existence["current_source_payload_emits_values"],
        "upstream_value_existence_status": existence["upstream_value_existence_status"],
        "proposal_required": True,
        "field_creation_executed": False,
        "schema_mutation_executed": False,
        "source_payload_mutation_executed": False,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "missing_label_values_guessed": False,
        "review_only": True,
    }

def build_field_introduction_proposal(existence: Dict[str, Any], boundary: Dict[str, Any]) -> Dict[str, Any]:
    proposal_id = sha8({
        "proposal": "PROPOSE_SOURCE_PROVENANCE_FIELD_INTRODUCTION_V0",
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "fields": PROPOSED_FIELDS,
        "boundary": boundary["refined_classification"],
    })
    return {
        "schema_version": "source_provenance_field_introduction_proposal_v0",
        "proposal_type": "FIELD_INTRODUCTION_PROPOSAL",
        "proposal_name": "PROPOSE_SOURCE_PROVENANCE_FIELD_INTRODUCTION_V0",
        "proposal_id": proposal_id,
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": "NONEXISTENT_OR_UNREPRESENTED_FIELD_REQUIRED_FOR_CONTINUATION",
        "action": "PROPOSE_FIELD_INTRODUCTION",
        "proposed_fields": [
            {
                "proposed_field_name": field,
                "why_required": "taxonomy-gap investigation cannot classify missing-label pressure without this value",
                "where_absence_was_observed": [
                    rel(RERUN_FIELD_ROWS_PATH),
                    rel(NULL_LIMIT_INPUT_ROLLUP_PATH),
                    rel(NULL_LIMIT_RECEIPT_PATH),
                ],
                "which_loop_could_not_continue": "pressure handling loop for R1000 top group taxonomy gap",
                "current_source_surface": existence["current_source_surface"],
                "expected_future_source_surface": "upstream source payload or schema emits this field with a real value or an explicit non-applicable reason",
                "mutation_required": "schema_or_source_payload_introduction_required_if_accepted",
                "authority_required": "human_review_required",
                "risk_if_not_added": "taxonomy-gap missing-label pressure remains unclassifiable beyond source-content absence",
                "review_decision_required": True,
            }
            for field in PROPOSED_FIELDS
        ],
        "summary_reason": "taxonomy-gap investigation cannot classify missing-label pressure because the upstream source payload does not emit values required to identify the missing label or compare current/expected label spaces",
        "current_source_surface": existence["current_source_surface"],
        "expected_future_source_surface": "source payload/schema has explicit fields for missing label identity and taxonomy context",
        "mutation_required": True,
        "mutation_executed": False,
        "authority_required": "HUMAN_REVIEW_REQUIRED",
        "review_decision_required": True,
        "allowed_human_decisions": [
            "ACCEPT_FIELD_INTRODUCTION_PROPOSAL",
            "DECLINE_FIELD_INTRODUCTION_PROPOSAL",
            "REQUEST_UPSTREAM_EXISTENCE_AUDIT",
            "MARK_HEALTHY_EXPECTED_SOURCE_LIMIT",
            "REJECT_FIELD_INTRODUCTION_BOUNDARY",
        ],
        "if_accepted_next_unit": "BUILD_SOURCE_PROVENANCE_FIELD_INTRODUCTION_FOR_R1000_TAXONOMY_GAP_VALUES_V0",
        "if_existence_audit_requested_next_unit": "AUDIT_UPSTREAM_EXISTENCE_FOR_R1000_TAXONOMY_GAP_VALUES_V0",
        "forbidden_scope": [
            "creating fields inside this unit",
            "populating missing label values by guess",
            "taxonomy repair",
            "taxonomy upgrade",
            "taxonomy delta proposal",
            "mutating existing receipts",
            "overwriting historical source rows",
            "auto-opening next group",
        ],
        "field_creation_executed": False,
        "schema_mutation_executed": False,
        "source_payload_mutation_executed": False,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "burden_optimization_authorized": False,
        "source_mutation": False,
        "missing_label_values_guessed": False,
        "review_only": True,
    }

def build_decision_packet(proposal: Dict[str, Any], boundary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduction_decision_packet_v0",
        "packet_type": "HUMAN_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "refined_classification": boundary["refined_classification"],
        "refined_action": boundary["refined_action"],
        "proposal_type": proposal["proposal_type"],
        "proposal_id": proposal["proposal_id"],
        "proposal_name": proposal["proposal_name"],
        "proposed_field_names": PROPOSED_FIELDS,
        "recommended_next_handling": "REVIEW_FIELD_INTRODUCTION_PROPOSAL",
        "allowed_human_choices": proposal["allowed_human_decisions"],
        "next_if_accepted": proposal["if_accepted_next_unit"],
        "next_if_existence_audit_requested": proposal["if_existence_audit_requested_next_unit"],
        "may_create_field": False,
        "may_mutate_schema": False,
        "may_mutate_source_payload": False,
        "may_emit_repair_command": False,
        "may_emit_build_command": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_taxonomy_delta": False,
        "may_authorize_authority_widening": False,
        "may_authorize_burden_optimization": False,
        "may_execute_source_provenance_repair": False,
        "may_adopt_protocol": False,
        "may_auto_open_next_group": False,
        "may_advance_without_human_decision": False,
        "review_only": True,
    }

def build_report(existence: Dict[str, Any], boundary: Dict[str, Any], proposal: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduction_boundary_refinement_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
            "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
            "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
            "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
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
        "existence_status": existence,
        "boundary_refinement": boundary,
        "field_introduction_proposal": {
            "proposal_id": proposal["proposal_id"],
            "proposal_name": proposal["proposal_name"],
            "proposal_type": proposal["proposal_type"],
            "proposed_field_names": PROPOSED_FIELDS,
        },
        "decision_packet_recommended_next_handling": packet["recommended_next_handling"],
        "refinement_executed": True,
        "field_introduction_proposal_emitted": True,
        "field_creation_executed": False,
        "schema_mutation_executed": False,
        "source_payload_mutation_executed": False,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "source_provenance_repair_executed": False,
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
        "review_only": True,
    }

def validate_outputs(existence: Dict[str, Any], boundary: Dict[str, Any], proposal: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if existence["field_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_row_count_wrong")
    if existence["current_source_payload_emits_values"] is not False:
        failures.append("source_payload_emits_values_unexpected")
    if existence["field_introduction_boundary_status"] != "NONEXISTENT_OR_UNREPRESENTED_FIELD_REQUIRED_FOR_CONTINUATION":
        failures.append("existence_boundary_status_wrong")
    for key in [
        "taxonomy_delta_evidence_present",
        "taxonomy_upgrade_evidence_present",
        "missing_label_values_guessed",
        "field_creation_executed",
        "schema_mutation_executed",
        "source_payload_mutation_executed",
    ]:
        if existence.get(key) is not False:
            failures.append(f"existence_guard_not_false:{key}:{existence.get(key)}")

    if boundary["refined_classification"] != "NONEXISTENT_OR_UNREPRESENTED_FIELD_REQUIRED_FOR_CONTINUATION":
        failures.append("refined_classification_wrong")
    if boundary["refined_action"] != "PROPOSE_FIELD_INTRODUCTION":
        failures.append("refined_action_wrong")
    if boundary["proposal_required"] is not True:
        failures.append("proposal_not_required")
    for key in [
        "field_creation_executed",
        "schema_mutation_executed",
        "source_payload_mutation_executed",
        "repair_command_emitted",
        "build_command_emitted",
        "taxonomy_delta_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "missing_label_values_guessed",
    ]:
        if boundary.get(key) is not False:
            failures.append(f"boundary_guard_not_false:{key}:{boundary.get(key)}")

    if proposal["proposal_type"] != "FIELD_INTRODUCTION_PROPOSAL":
        failures.append("proposal_type_wrong")
    if proposal["proposal_name"] != "PROPOSE_SOURCE_PROVENANCE_FIELD_INTRODUCTION_V0":
        failures.append("proposal_name_wrong")
    if sorted([item["proposed_field_name"] for item in proposal["proposed_fields"]]) != sorted(PROPOSED_FIELDS):
        failures.append("proposal_fields_wrong")
    if proposal["mutation_required"] is not True:
        failures.append("proposal_mutation_not_required")
    if proposal["mutation_executed"] is not False:
        failures.append("proposal_mutation_executed")
    if proposal["authority_required"] != "HUMAN_REVIEW_REQUIRED":
        failures.append("proposal_authority_wrong")
    if proposal["review_decision_required"] is not True:
        failures.append("proposal_review_not_required")
    for key in [
        "field_creation_executed",
        "schema_mutation_executed",
        "source_payload_mutation_executed",
        "repair_command_emitted",
        "build_command_emitted",
        "taxonomy_delta_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "burden_optimization_authorized",
        "source_mutation",
        "missing_label_values_guessed",
    ]:
        if proposal.get(key) is not False:
            failures.append(f"proposal_guard_not_false:{key}:{proposal.get(key)}")

    if packet["packet_type"] != "HUMAN_REVIEW_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    if packet["recommended_next_handling"] != "REVIEW_FIELD_INTRODUCTION_PROPOSAL":
        failures.append("packet_recommendation_wrong")
    if packet["next_if_accepted"] != "BUILD_SOURCE_PROVENANCE_FIELD_INTRODUCTION_FOR_R1000_TAXONOMY_GAP_VALUES_V0":
        failures.append("packet_next_if_accepted_wrong")
    for key in [
        "may_create_field",
        "may_mutate_schema",
        "may_mutate_source_payload",
        "may_emit_repair_command",
        "may_emit_build_command",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_taxonomy_delta",
        "may_authorize_authority_widening",
        "may_authorize_burden_optimization",
        "may_execute_source_provenance_repair",
        "may_adopt_protocol",
        "may_auto_open_next_group",
        "may_advance_without_human_decision",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")

    for key in [
        "field_creation_executed",
        "schema_mutation_executed",
        "source_payload_mutation_executed",
        "repair_command_emitted",
        "build_command_emitted",
        "source_provenance_repair_executed",
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

    if report["refinement_executed"] is not True:
        failures.append("refinement_not_executed")
    if report["field_introduction_proposal_emitted"] is not True:
        failures.append("field_introduction_proposal_not_emitted")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_null_limit_receipt_id") != SOURCE_NULL_LIMIT_RECEIPT_ID:
        failures.append("source_null_limit_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "FIELD_INTRO_BOUNDARY_0_NULL_LIMIT_CONSUMED",
        "FIELD_INTRO_BOUNDARY_1_HUMAN_DECISION_RECORDED",
        "FIELD_INTRO_BOUNDARY_2_REPAIR_BIASED_NEXT_OBJECT_REFINED",
        "FIELD_INTRO_BOUNDARY_3_EXISTENCE_STATUS_ASSESSED",
        "FIELD_INTRO_BOUNDARY_4_FIELD_INTRODUCTION_PROPOSAL_EMITTED",
        "FIELD_INTRO_BOUNDARY_5_DECISION_PACKET_EMITTED",
        "FIELD_INTRO_BOUNDARY_6_NO_FIELD_CREATION_OR_SCHEMA_MUTATION",
        "FIELD_INTRO_BOUNDARY_7_NO_TAXONOMY_ACTION",
        "FIELD_INTRO_BOUNDARY_8_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("refined_classification") != "NONEXISTENT_OR_UNREPRESENTED_FIELD_REQUIRED_FOR_CONTINUATION":
        failures.append("metric_refined_classification_wrong")
    if metrics.get("refined_action") != "PROPOSE_FIELD_INTRODUCTION":
        failures.append("metric_refined_action_wrong")
    if metrics.get("proposal_type") != "FIELD_INTRODUCTION_PROPOSAL":
        failures.append("metric_proposal_type_wrong")
    if metrics.get("recommended_next_handling") != "REVIEW_FIELD_INTRODUCTION_PROPOSAL":
        failures.append("metric_recommendation_wrong")
    if metrics.get("next_if_accepted") != "BUILD_SOURCE_PROVENANCE_FIELD_INTRODUCTION_FOR_R1000_TAXONOMY_GAP_VALUES_V0":
        failures.append("metric_next_if_accepted_wrong")
    for key in [
        "field_creation_executed_count",
        "schema_mutation_executed_count",
        "source_payload_mutation_executed_count",
        "repair_command_emitted_count",
        "build_command_emitted_count",
        "source_provenance_repair_executed_count",
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

    guards = receipt.get("field_introduction_boundary_guards", {})
    for key in [
        "null_limit_consumed",
        "human_decision_recorded",
        "repair_biased_next_object_refined",
        "existence_status_assessed",
        "field_introduction_proposal_emitted",
        "decision_packet_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "field_creation_executed",
        "schema_mutation_executed",
        "source_payload_mutation_executed",
        "repair_command_emitted",
        "build_command_emitted",
        "source_provenance_repair_executed",
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
    source_before = snapshot_files(SOURCE_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    existence = build_existence_status(sources)
    boundary = build_boundary_refinement(existence, sources)
    proposal = build_field_introduction_proposal(existence, boundary)
    packet = build_decision_packet(proposal, boundary)
    report = build_report(existence, boundary, proposal, packet)

    write_json(EXISTENCE_STATUS_PATH, existence)
    write_json(BOUNDARY_REFINEMENT_PATH, boundary)
    write_json(FIELD_INTRODUCTION_PROPOSAL_PATH, proposal)
    write_json(DECISION_PACKET_PATH, packet)
    write_json(REFINEMENT_REPORT_PATH, report)

    failures.extend(validate_outputs(existence, boundary, proposal, packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "FIELD_INTRO_BOUNDARY_0_NULL_LIMIT_CONSUMED": sources["null_limit_receipt"]["receipt_id"] == SOURCE_NULL_LIMIT_RECEIPT_ID and sources["null_limit_receipt"]["gate"] == "PASS",
        "FIELD_INTRO_BOUNDARY_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "REFINE_NULL_EVIDENCE_LIMIT_INTO_FIELD_INTRODUCTION_BOUNDARY",
        "FIELD_INTRO_BOUNDARY_2_REPAIR_BIASED_NEXT_OBJECT_REFINED": boundary["old_next_if_accepted"] == "BUILD_REPAIR_SOURCE_PROVENANCE_FOR_R1000_TAXONOMY_GAP_VALUES_V0",
        "FIELD_INTRO_BOUNDARY_3_EXISTENCE_STATUS_ASSESSED": existence["field_introduction_boundary_status"] == "NONEXISTENT_OR_UNREPRESENTED_FIELD_REQUIRED_FOR_CONTINUATION",
        "FIELD_INTRO_BOUNDARY_4_FIELD_INTRODUCTION_PROPOSAL_EMITTED": proposal["proposal_type"] == "FIELD_INTRODUCTION_PROPOSAL",
        "FIELD_INTRO_BOUNDARY_5_DECISION_PACKET_EMITTED": DECISION_PACKET_PATH.exists(),
        "FIELD_INTRO_BOUNDARY_6_NO_FIELD_CREATION_OR_SCHEMA_MUTATION": report["field_creation_executed"] is False and report["schema_mutation_executed"] is False and report["source_payload_mutation_executed"] is False,
        "FIELD_INTRO_BOUNDARY_7_NO_TAXONOMY_ACTION": report["taxonomy_delta_proposal_emitted"] is False and report["taxonomy_upgrade_authorized"] is False,
        "FIELD_INTRO_BOUNDARY_8_NO_SOURCE_MUTATION": source_mutation_detected is False,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {"type": "STOP", "stop_code": "STOP_HUMAN_DECISION_REQUIRED", "next_command_goal": None}
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if any([
        report["field_creation_executed"],
        report["schema_mutation_executed"],
        report["source_payload_mutation_executed"],
        report["repair_command_emitted"],
        report["build_command_emitted"],
        report["source_provenance_repair_executed"],
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
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "old_classification": boundary["old_classification"],
        "old_next_if_accepted": boundary["old_next_if_accepted"],
        "refined_classification": boundary["refined_classification"],
        "refined_action": boundary["refined_action"],
        "proposal_type": proposal["proposal_type"],
        "proposal_name": proposal["proposal_name"],
        "proposal_id": proposal["proposal_id"],
        "proposed_field_count": len(PROPOSED_FIELDS),
        "proposed_field_names": PROPOSED_FIELDS,
        "current_source_payload_emits_values": existence["current_source_payload_emits_values"],
        "upstream_value_existence_status": existence["upstream_value_existence_status"],
        "recommended_next_handling": packet["recommended_next_handling"],
        "next_if_accepted": packet["next_if_accepted"],
        "refinement_executed_count": 1,
        "field_introduction_proposal_emitted_count": 1,
        "field_creation_executed_count": 0,
        "schema_mutation_executed_count": 0,
        "source_payload_mutation_executed_count": 0,
        "repair_command_emitted_count": 0,
        "build_command_emitted_count": 0,
        "source_provenance_repair_executed_count": 0,
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
        "null_limit_consumed": True,
        "human_decision_recorded": True,
        "repair_biased_next_object_refined": boundary["old_next_if_accepted"] == "BUILD_REPAIR_SOURCE_PROVENANCE_FOR_R1000_TAXONOMY_GAP_VALUES_V0",
        "existence_status_assessed": True,
        "field_introduction_proposal_emitted": True,
        "decision_packet_emitted": True,
        "field_creation_executed": False,
        "schema_mutation_executed": False,
        "source_payload_mutation_executed": False,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "source_provenance_repair_executed": False,
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
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "proposal_id": proposal["proposal_id"],
        "refined_classification": boundary["refined_classification"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "field_existence_status_assessment": rel(EXISTENCE_STATUS_PATH),
        "field_introduction_boundary_refinement": rel(BOUNDARY_REFINEMENT_PATH),
        "source_provenance_field_introduction_proposal": rel(FIELD_INTRODUCTION_PROPOSAL_PATH),
        "field_introduction_decision_packet": rel(DECISION_PACKET_PATH),
        "field_introduction_boundary_refinement_report": rel(REFINEMENT_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "null_evidence_field_introduction_boundary_refinement_receipt_v0",
        "receipt_type": "NULL_EVIDENCE_FIELD_INTRODUCTION_BOUNDARY_REFINEMENT_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
        "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
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
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "field_introduction_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "old_classification": boundary["old_classification"],
            "old_next_if_accepted": boundary["old_next_if_accepted"],
            "refined_classification": boundary["refined_classification"],
            "refined_action": boundary["refined_action"],
            "proposal_type": proposal["proposal_type"],
            "proposal_name": proposal["proposal_name"],
            "proposal_id": proposal["proposal_id"],
            "proposed_field_names": PROPOSED_FIELDS,
            "recommended_next_handling": packet["recommended_next_handling"],
            "next_if_accepted": packet["next_if_accepted"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "field_introduction_boundary_guards": guards,
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
    print(f"field_introduction_boundary_refinement_receipt_id={receipt_id}")
    print(f"field_introduction_boundary_refinement_receipt_path=data/null_evidence_field_introduction_boundary_refinement_v0_receipts/{receipt_id}.json")
    print(f"field_introduction_proposal_path=data/null_evidence_field_introduction_boundary_refinement_v0/source_provenance_field_introduction_proposal.json")
    print(f"field_introduction_decision_packet_path=data/null_evidence_field_introduction_boundary_refinement_v0/field_introduction_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
