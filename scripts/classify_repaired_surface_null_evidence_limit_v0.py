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

UNIT_ID = "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT_V0"
TARGET_UNIT_ID = "repaired_surface_null_evidence_limit_classification.v0"

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
SOURCE_REPAIR_OBJECTIVE_ID = "12d712af"

TOP_GROUP_KEY_HASH = "38c604a1"
EXPECTED_FIELD_ROW_COUNT = 25

EVIDENCE_FIELDS = [
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

OUT_DIR = ROOT / "data" / "repaired_surface_null_evidence_limit_classification_v0"
RECEIPT_DIR = ROOT / "data" / "repaired_surface_null_evidence_limit_classification_v0_receipts"

NULL_LIMIT_INPUT_ROLLUP_PATH = OUT_DIR / "null_evidence_limit_input_rollup.json"
ABSENCE_REASON_CLASSIFICATION_PATH = OUT_DIR / "absence_reason_classification.json"
NULL_LIMIT_CLASSIFICATION_PATH = OUT_DIR / "null_evidence_limit_classification.json"
SOURCE_PROVENANCE_REPAIR_PROPOSAL_PATH = OUT_DIR / "source_provenance_repair_objective_proposal.json"
NULL_LIMIT_DECISION_PACKET_PATH = OUT_DIR / "null_evidence_limit_decision_packet.json"
NULL_LIMIT_REPORT_PATH = OUT_DIR / "null_evidence_limit_report.json"

COMPARISON_GATE_FIX_RECEIPT_PATH = ROOT / "data" / "repaired_surface_rerun_comparison_gate_fix_v0_receipts" / f"{SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID}.json"
CORRECTED_COMPARISON_PATH = ROOT / "data" / "repaired_surface_rerun_comparison_gate_fix_v0" / "corrected_pre_post_repair_evidence_comparison.json"
CORRECTED_OUTCOME_PATH = ROOT / "data" / "repaired_surface_rerun_comparison_gate_fix_v0" / "corrected_repaired_surface_evidence_outcome.json"
CORRECTED_PACKET_PATH = ROOT / "data" / "repaired_surface_rerun_comparison_gate_fix_v0" / "corrected_repaired_surface_rerun_decision_packet.json"
GATE_FIX_REPORT_PATH = ROOT / "data" / "repaired_surface_rerun_comparison_gate_fix_v0" / "comparison_gate_fix_report.json"

FAILED_RERUN_RECEIPT_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0_receipts" / f"{FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID}.json"
RERUN_FIELD_ROWS_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_taxonomy_gap_missing_label_field_rows.jsonl"
RERUN_CONTEXT_REFS_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_taxonomy_gap_context_refs.json"
RERUN_FIELD_PRESENCE_ROLLUP_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_field_presence_rollup.json"
RERUN_EVIDENCE_OUTCOME_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_evidence_outcome.json"
RERUN_DECISION_PACKET_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_rerun_decision_packet.json"
RERUN_REPORT_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_rerun_report.json"

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
    COMPARISON_GATE_FIX_RECEIPT_PATH,
    CORRECTED_COMPARISON_PATH,
    CORRECTED_OUTCOME_PATH,
    CORRECTED_PACKET_PATH,
    GATE_FIX_REPORT_PATH,
    FAILED_RERUN_RECEIPT_PATH,
    RERUN_FIELD_ROWS_PATH,
    RERUN_CONTEXT_REFS_PATH,
    RERUN_FIELD_PRESENCE_ROLLUP_PATH,
    RERUN_EVIDENCE_OUTCOME_PATH,
    RERUN_DECISION_PACKET_PATH,
    RERUN_REPORT_PATH,
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

CLASSIFICATION_CLASSES = [
    "SOURCE_CONTENT_PROVENANCE_ABSENT_REPAIRABLE",
    "SOURCE_CONTENT_PROVENANCE_ABSENT_HEALTHY_LIMIT",
    "PARTIAL_CONTENT_PROVENANCE_AVAILABLE",
    "NOT_ENOUGH_EVIDENCE_TO_CLASSIFY_NULL_LIMIT",
]

HUMAN_DECISION = {
    "decision": "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT",
    "scope": "classify null evidence limit and expose human-reviewable source provenance objective if applicable",
    "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
    "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
    "not_authorized": [
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
    "null evidence classification is not taxonomy repair",
    "absence reason SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELD does not identify a missing label",
    "source provenance objective may request instrumentation but must not guess values",
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
        "comparison_gate_fix_receipt": read_json(COMPARISON_GATE_FIX_RECEIPT_PATH),
        "corrected_comparison": read_json(CORRECTED_COMPARISON_PATH),
        "corrected_outcome": read_json(CORRECTED_OUTCOME_PATH),
        "corrected_packet": read_json(CORRECTED_PACKET_PATH),
        "gate_fix_report": read_json(GATE_FIX_REPORT_PATH),
        "failed_rerun_receipt": read_json(FAILED_RERUN_RECEIPT_PATH),
        "field_rows": read_jsonl(RERUN_FIELD_ROWS_PATH),
        "context_refs": read_json(RERUN_CONTEXT_REFS_PATH),
        "field_presence_rollup": read_json(RERUN_FIELD_PRESENCE_ROLLUP_PATH),
        "rerun_outcome": read_json(RERUN_EVIDENCE_OUTCOME_PATH),
        "rerun_packet": read_json(RERUN_DECISION_PACKET_PATH),
        "rerun_report": read_json(RERUN_REPORT_PATH),
        "structural_ref_fix_receipt": read_json(STRUCTURAL_REF_FIX_RECEIPT_PATH),
        "repair_eligibility_receipt": read_json(REPAIR_ELIGIBILITY_RECEIPT_PATH),
        "localization_receipt": read_json(LOCALIZATION_RECEIPT_PATH),
        "evidence_surface_receipt": read_json(EVIDENCE_SURFACE_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    gate_fix = sources["comparison_gate_fix_receipt"]
    corrected_outcome = sources["corrected_outcome"]

    if gate_fix.get("receipt_id") != SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID:
        failures.append("comparison_gate_fix_receipt_id_wrong")
    if gate_fix.get("gate") != "PASS":
        failures.append("comparison_gate_fix_not_pass")
    if gate_fix.get("aggregate_metrics", {}).get("field_surface_repair_validated") is not True:
        failures.append("field_surface_repair_not_validated")
    if gate_fix.get("aggregate_metrics", {}).get("corrected_outcome") != "EVIDENCE_SURFACE_REPAIRED_VALUES_ABSENT":
        failures.append("corrected_outcome_wrong")
    if gate_fix.get("aggregate_metrics", {}).get("corrected_evidence_sufficiency_class") != "EVIDENCE_SURFACE_PRESENT_CONTENT_ABSENT":
        failures.append("corrected_sufficiency_wrong")
    if gate_fix.get("aggregate_metrics", {}).get("recommended_next_unit") != UNIT_ID:
        failures.append("gate_fix_recommended_next_unit_not_this")
    if gate_fix.get("aggregate_metrics", {}).get("source_mutation_count") != 0:
        failures.append("comparison_gate_fix_mutated_source")

    if corrected_outcome.get("recommended_next_unit") != UNIT_ID:
        failures.append("corrected_packet_next_unit_not_this")
    if len(sources["field_rows"]) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_row_count_wrong")
    if sources["field_presence_rollup"].get("all_required_field_keys_present") is not True:
        failures.append("field_keys_not_present")
    if sources["field_presence_rollup"].get("all_absence_reasons_present") is not True:
        failures.append("absence_reasons_not_present")
    if sources["field_presence_rollup"].get("all_structural_refs_present") is not True:
        failures.append("structural_refs_not_present")
    if sources["field_presence_rollup"].get("any_required_field_value_present") is not False:
        failures.append("unexpected_value_presence")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_input_rollup(sources: Dict[str, Any]) -> Dict[str, Any]:
    field_rows = sources["field_rows"]
    reason_profile = {
        field: dict(sorted(Counter(row.get(ABSENCE_REASON_FIELDS[field]) for row in field_rows).items(), key=lambda item: str(item[0])))
        for field in EVIDENCE_FIELDS
    }
    value_presence_profile = {
        field: sum(1 for row in field_rows if row.get(field) is not None)
        for field in EVIDENCE_FIELDS
    }
    key_presence_profile = {
        field: sum(1 for row in field_rows if row.get(f"{field}_key_present") is True or field in row)
        for field in EVIDENCE_FIELDS
    }
    absence_reason_key_profile = {
        field: sum(1 for row in field_rows if ABSENCE_REASON_FIELDS[field] in row)
        for field in EVIDENCE_FIELDS
    }
    all_reasons_source_payload_missing = all(
        reason_profile[field] == {"SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELD": EXPECTED_FIELD_ROW_COUNT}
        for field in EVIDENCE_FIELDS
    )

    return {
        "schema_version": "null_evidence_limit_input_rollup_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
        "source_failed_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
        "field_row_count": len(field_rows),
        "expected_field_row_count": EXPECTED_FIELD_ROW_COUNT,
        "key_presence_profile": key_presence_profile,
        "value_presence_profile": value_presence_profile,
        "absence_reason_key_profile": absence_reason_key_profile,
        "absence_reason_value_profile": reason_profile,
        "all_required_field_keys_present": sources["field_presence_rollup"]["all_required_field_keys_present"],
        "all_absence_reasons_present": sources["field_presence_rollup"]["all_absence_reasons_present"],
        "all_structural_refs_present": sources["field_presence_rollup"]["all_structural_refs_present"],
        "any_required_field_value_present": sources["field_presence_rollup"]["any_required_field_value_present"],
        "all_required_field_values_present": sources["field_presence_rollup"]["all_required_field_values_present"],
        "all_nulls_have_source_payload_absence_reason": all_reasons_source_payload_missing,
        "field_surface_repair_validated": sources["corrected_outcome"]["field_surface_repair_validated"],
        "corrected_evidence_sufficiency_class": sources["corrected_outcome"]["evidence_sufficiency_class"],
        "taxonomy_delta_evidence_present": False,
        "taxonomy_upgrade_evidence_present": False,
        "missing_label_values_guessed": False,
        "review_only": True,
    }

def classify_absence_reason(rollup: Dict[str, Any]) -> Dict[str, Any]:
    if rollup["all_nulls_have_source_payload_absence_reason"]:
        absence_class = "SOURCE_PAYLOAD_DOES_NOT_EMIT_REQUIRED_VALUES"
        support = "STRONG"
        reason = "Every required field is exposed as a key, every value is null, and every null is explained by SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELD."
    elif rollup["all_absence_reasons_present"]:
        absence_class = "EXPLICIT_NULL_REASON_MIXED"
        support = "PARTIAL"
        reason = "Nulls have explicit reasons, but reasons are not uniform."
    else:
        absence_class = "NULL_REASON_INSUFFICIENT"
        support = "WEAK"
        reason = "Null values are present without complete absence reasons."
    return {
        "schema_version": "absence_reason_classification_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "absence_reason_class": absence_class,
        "support_level": support,
        "classification_reason": reason,
        "absence_reason_value_profile": rollup["absence_reason_value_profile"],
        "taxonomy_delta_evidence_present": False,
        "taxonomy_upgrade_evidence_present": False,
        "missing_label_values_guessed": False,
        "review_only": True,
    }

def classify_null_limit(rollup: Dict[str, Any], absence: Dict[str, Any]) -> Dict[str, Any]:
    if (
        rollup["field_surface_repair_validated"] is True
        and rollup["all_required_field_keys_present"] is True
        and rollup["all_absence_reasons_present"] is True
        and rollup["any_required_field_value_present"] is False
        and absence["absence_reason_class"] == "SOURCE_PAYLOAD_DOES_NOT_EMIT_REQUIRED_VALUES"
    ):
        classification = "SOURCE_CONTENT_PROVENANCE_ABSENT_REPAIRABLE"
        reason = "The evidence surface is valid, but required values remain absent because the source payload does not emit them. This is a source content/provenance deficiency, not a taxonomy delta."
        proposal_allowed = True
        recommended = "REVIEW_SOURCE_PROVENANCE_REPAIR_OBJECTIVE"
    elif rollup["any_required_field_value_present"]:
        classification = "PARTIAL_CONTENT_PROVENANCE_AVAILABLE"
        reason = "Some required values are now present; taxonomy-gap reclassification may be possible after partial evidence review."
        proposal_allowed = False
        recommended = "RECLASSIFY_TAXONOMY_GAP_WITH_PARTIAL_REPAIRED_EVIDENCE"
    else:
        classification = "NOT_ENOUGH_EVIDENCE_TO_CLASSIFY_NULL_LIMIT"
        reason = "The null-value state cannot be cleanly attributed to a source payload provenance deficiency."
        proposal_allowed = False
        recommended = "REQUEST_MORE_NULL_EVIDENCE_AUDIT"

    return {
        "schema_version": "null_evidence_limit_classification_v0",
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": classification,
        "classification_classes": CLASSIFICATION_CLASSES,
        "classification_reason": reason,
        "absence_reason_class": absence["absence_reason_class"],
        "support_level": absence["support_level"],
        "proposal_allowed": proposal_allowed,
        "recommended_next_handling": recommended,
        "taxonomy_repair_required": False,
        "taxonomy_upgrade_required": False,
        "taxonomy_delta_proposal_required": False,
        "missing_label_value_guess_required": False,
        "source_provenance_repair_execution_authorized": False,
        "source_mutation": False,
        "build_command_emitted": False,
        "review_only": True,
    }

def build_source_provenance_repair_proposal(classification: Dict[str, Any], rollup: Dict[str, Any]) -> Dict[str, Any]:
    if not classification["proposal_allowed"]:
        return {
            "schema_version": "source_provenance_repair_objective_proposal_v0",
            "proposal_emitted": False,
            "reason": "classification_not_eligible",
            "classification": classification["classification"],
            "repair_command_emitted": False,
            "repair_executed": False,
            "taxonomy_upgrade_authorized": False,
            "taxonomy_delta_proposal_emitted": False,
            "source_mutation": False,
            "build_command_emitted": False,
            "review_only": True,
        }

    proposal_id = sha8({
        "proposal": "SOURCE_PROVENANCE_REPAIR_OBJECTIVE",
        "source": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
        "fields": EVIDENCE_FIELDS,
        "reason": "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELD",
    })

    return {
        "schema_version": "source_provenance_repair_objective_proposal_v0",
        "proposal_emitted": True,
        "proposal_type": "SOURCE_PROVENANCE_REPAIR_OBJECTIVE_PROPOSAL",
        "repair_objective_id": proposal_id,
        "repair_objective_name": "REPAIR_SOURCE_PROVENANCE_FOR_R1000_TAXONOMY_GAP_VALUES_V0",
        "repair_scope": "Identify and instrument the upstream producer or provenance layer that could emit real values for the taxonomy-gap evidence fields, or classify the absence as a healthy expected source limit if no such producer exists.",
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_evidence_refs": [
            rel(COMPARISON_GATE_FIX_RECEIPT_PATH),
            rel(CORRECTED_OUTCOME_PATH),
            rel(RERUN_FIELD_ROWS_PATH),
            rel(RERUN_CONTEXT_REFS_PATH),
            rel(RERUN_FIELD_PRESENCE_ROLLUP_PATH),
        ],
        "missing_values_to_source": EVIDENCE_FIELDS,
        "current_absence_reason": "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELD",
        "required_review_questions": [
            "Which upstream producer creates the pressure event payload rows?",
            "Does that producer have access to missing_label_identifier?",
            "Does that producer have access to taxonomy_context_ref?",
            "Does that producer have access to current_label_space_ref?",
            "Does that producer have access to expected_label_space_ref?",
            "If not available, is this a healthy expected source boundary?",
        ],
        "candidate_artifacts_to_inspect": [
            "producer_of_r1000_pressure_event_rows_jsonl",
            "pressure_event_payload_schema",
            "taxonomy pressure emitter",
            "halt reason emitter for STOP_TAXONOMY_GAP",
        ],
        "expected_acceptance_gates_if_accepted": [
            "producer localized",
            "available provenance fields identified",
            "unavailable provenance fields explicitly classified with reason",
            "no missing label values guessed",
            "no taxonomy delta emitted",
            "no taxonomy upgrade authorized",
            "historical receipts not mutated",
        ],
        "rerun_required_after_source_provenance_repair": [
            "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_REPAIRED_SURFACE_V0",
            "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT_V0",
            "RECLASSIFY_R1000_TOP_GROUP_TAXONOMY_GAP_AFTER_REPAIRED_EVIDENCE_SURFACE_V0 if values become available",
        ],
        "forbidden_scope": [
            "taxonomy repair",
            "taxonomy upgrade",
            "taxonomy delta proposal",
            "guessing missing label values",
            "mutating existing receipts",
            "overwriting historical source rows",
            "auto-opening next group",
            "executing source provenance repair inside this unit",
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
    recommended = "ACCEPT_SOURCE_PROVENANCE_REPAIR_OBJECTIVE" if proposal["proposal_emitted"] else classification["recommended_next_handling"]
    return {
        "schema_version": "null_evidence_limit_decision_packet_v0",
        "packet_type": "HUMAN_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "classification": classification["classification"],
        "classification_reason": classification["classification_reason"],
        "proposal_emitted": proposal["proposal_emitted"],
        "source_provenance_repair_objective_id": proposal.get("repair_objective_id"),
        "allowed_human_choices": [
            "ACCEPT_SOURCE_PROVENANCE_REPAIR_OBJECTIVE",
            "DECLINE_SOURCE_PROVENANCE_REPAIR_OBJECTIVE",
            "MARK_HEALTHY_EXPECTED_SOURCE_LIMIT",
            "REQUEST_MORE_NULL_EVIDENCE_AUDIT",
            "REJECT_NULL_LIMIT_CLASSIFICATION",
        ],
        "recommended_next_handling": recommended,
        "next_if_accepted": "BUILD_REPAIR_SOURCE_PROVENANCE_FOR_R1000_TAXONOMY_GAP_VALUES_V0" if proposal["proposal_emitted"] else None,
        "next_if_declined": "MARK_HEALTHY_EXPECTED_SOURCE_LIMIT_OR_STOP",
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

def build_report(rollup: Dict[str, Any], absence: Dict[str, Any], classification: Dict[str, Any], proposal: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "null_evidence_limit_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
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
        "input_rollup": rollup,
        "absence_reason_classification": absence,
        "null_limit_classification": classification,
        "source_provenance_repair_objective_proposal": {
            "proposal_emitted": proposal["proposal_emitted"],
            "repair_objective_id": proposal.get("repair_objective_id"),
            "repair_objective_name": proposal.get("repair_objective_name"),
        },
        "decision_packet_recommended_next_handling": packet["recommended_next_handling"],
        "classification_executed": True,
        "proposal_emitted": proposal["proposal_emitted"],
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

def validate_outputs(rollup: Dict[str, Any], absence: Dict[str, Any], classification: Dict[str, Any], proposal: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if rollup["field_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("rollup_field_row_count_wrong")
    if rollup["all_required_field_keys_present"] is not True:
        failures.append("keys_not_present")
    if rollup["all_absence_reasons_present"] is not True:
        failures.append("absence_reasons_not_present")
    if rollup["all_structural_refs_present"] is not True:
        failures.append("structural_refs_not_present")
    if rollup["any_required_field_value_present"] is not False:
        failures.append("unexpected_value_presence")
    if rollup["all_nulls_have_source_payload_absence_reason"] is not True:
        failures.append("source_payload_absence_reason_not_uniform")
    if rollup["field_surface_repair_validated"] is not True:
        failures.append("field_surface_repair_not_validated")
    for key in ["taxonomy_delta_evidence_present", "taxonomy_upgrade_evidence_present", "missing_label_values_guessed"]:
        if rollup.get(key) is not False:
            failures.append(f"rollup_guard_not_false:{key}:{rollup.get(key)}")

    if absence["absence_reason_class"] != "SOURCE_PAYLOAD_DOES_NOT_EMIT_REQUIRED_VALUES":
        failures.append("absence_reason_class_wrong")
    if absence["support_level"] != "STRONG":
        failures.append("absence_support_not_strong")
    for key in ["taxonomy_delta_evidence_present", "taxonomy_upgrade_evidence_present", "missing_label_values_guessed"]:
        if absence.get(key) is not False:
            failures.append(f"absence_guard_not_false:{key}:{absence.get(key)}")

    if classification["classification"] != "SOURCE_CONTENT_PROVENANCE_ABSENT_REPAIRABLE":
        failures.append("classification_wrong")
    if classification["proposal_allowed"] is not True:
        failures.append("proposal_not_allowed")
    for key in [
        "taxonomy_repair_required",
        "taxonomy_upgrade_required",
        "taxonomy_delta_proposal_required",
        "missing_label_value_guess_required",
        "source_provenance_repair_execution_authorized",
        "source_mutation",
        "build_command_emitted",
    ]:
        if classification.get(key) is not False:
            failures.append(f"classification_guard_not_false:{key}:{classification.get(key)}")

    if proposal["proposal_emitted"] is not True:
        failures.append("source_provenance_proposal_not_emitted")
    if proposal.get("proposal_type") != "SOURCE_PROVENANCE_REPAIR_OBJECTIVE_PROPOSAL":
        failures.append("proposal_type_wrong")
    if proposal.get("repair_objective_name") != "REPAIR_SOURCE_PROVENANCE_FOR_R1000_TAXONOMY_GAP_VALUES_V0":
        failures.append("proposal_objective_name_wrong")
    if sorted(proposal.get("missing_values_to_source", [])) != sorted(EVIDENCE_FIELDS):
        failures.append("proposal_missing_values_wrong")
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
    if packet["recommended_next_handling"] != "ACCEPT_SOURCE_PROVENANCE_REPAIR_OBJECTIVE":
        failures.append("packet_recommendation_wrong")
    if packet["next_if_accepted"] != "BUILD_REPAIR_SOURCE_PROVENANCE_FOR_R1000_TAXONOMY_GAP_VALUES_V0":
        failures.append("packet_next_if_accepted_wrong")
    for key in [
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

    if report["classification_executed"] is not True:
        failures.append("classification_not_executed")
    if report["proposal_emitted"] is not True:
        failures.append("report_proposal_not_emitted")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_comparison_gate_fix_receipt_id") != SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID:
        failures.append("source_gate_fix_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "NULL_LIMIT_0_GATE_FIX_CONSUMED",
        "NULL_LIMIT_1_HUMAN_DECISION_RECORDED",
        "NULL_LIMIT_2_NULL_REASON_CLASSIFIED",
        "NULL_LIMIT_3_SOURCE_PROVENANCE_LIMIT_CLASSIFIED",
        "NULL_LIMIT_4_REPAIR_OBJECTIVE_PROPOSAL_EMITTED",
        "NULL_LIMIT_5_DECISION_PACKET_EMITTED",
        "NULL_LIMIT_6_NO_TAXONOMY_ACTION",
        "NULL_LIMIT_7_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("classification") != "SOURCE_CONTENT_PROVENANCE_ABSENT_REPAIRABLE":
        failures.append("metric_classification_wrong")
    if metrics.get("absence_reason_class") != "SOURCE_PAYLOAD_DOES_NOT_EMIT_REQUIRED_VALUES":
        failures.append("metric_absence_class_wrong")
    if metrics.get("source_provenance_repair_proposal_emitted") is not True:
        failures.append("metric_proposal_not_emitted")
    if metrics.get("recommended_next_handling") != "ACCEPT_SOURCE_PROVENANCE_REPAIR_OBJECTIVE":
        failures.append("metric_recommendation_wrong")
    if metrics.get("next_if_accepted") != "BUILD_REPAIR_SOURCE_PROVENANCE_FOR_R1000_TAXONOMY_GAP_VALUES_V0":
        failures.append("metric_next_if_accepted_wrong")
    for key in [
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

    guards = receipt.get("null_limit_guards", {})
    for key in [
        "gate_fix_consumed",
        "human_decision_recorded",
        "null_reason_classified",
        "source_provenance_limit_classified",
        "repair_objective_proposal_emitted",
        "decision_packet_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
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

    rollup = build_input_rollup(sources)
    absence = classify_absence_reason(rollup)
    classification = classify_null_limit(rollup, absence)
    proposal = build_source_provenance_repair_proposal(classification, rollup)
    packet = build_decision_packet(classification, proposal)
    report = build_report(rollup, absence, classification, proposal, packet)

    write_json(NULL_LIMIT_INPUT_ROLLUP_PATH, rollup)
    write_json(ABSENCE_REASON_CLASSIFICATION_PATH, absence)
    write_json(NULL_LIMIT_CLASSIFICATION_PATH, classification)
    write_json(SOURCE_PROVENANCE_REPAIR_PROPOSAL_PATH, proposal)
    write_json(NULL_LIMIT_DECISION_PACKET_PATH, packet)
    write_json(NULL_LIMIT_REPORT_PATH, report)

    failures.extend(validate_outputs(rollup, absence, classification, proposal, packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "NULL_LIMIT_0_GATE_FIX_CONSUMED": sources["comparison_gate_fix_receipt"]["receipt_id"] == SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID and sources["comparison_gate_fix_receipt"]["gate"] == "PASS",
        "NULL_LIMIT_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT",
        "NULL_LIMIT_2_NULL_REASON_CLASSIFIED": absence["absence_reason_class"] == "SOURCE_PAYLOAD_DOES_NOT_EMIT_REQUIRED_VALUES",
        "NULL_LIMIT_3_SOURCE_PROVENANCE_LIMIT_CLASSIFIED": classification["classification"] == "SOURCE_CONTENT_PROVENANCE_ABSENT_REPAIRABLE",
        "NULL_LIMIT_4_REPAIR_OBJECTIVE_PROPOSAL_EMITTED": proposal["proposal_emitted"] is True,
        "NULL_LIMIT_5_DECISION_PACKET_EMITTED": NULL_LIMIT_DECISION_PACKET_PATH.exists(),
        "NULL_LIMIT_6_NO_TAXONOMY_ACTION": report["taxonomy_delta_proposal_emitted"] is False and report["taxonomy_upgrade_authorized"] is False,
        "NULL_LIMIT_7_NO_SOURCE_MUTATION": source_mutation_detected is False,
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
        "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
        "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "field_row_count": rollup["field_row_count"],
        "all_required_field_keys_present": rollup["all_required_field_keys_present"],
        "all_absence_reasons_present": rollup["all_absence_reasons_present"],
        "all_structural_refs_present": rollup["all_structural_refs_present"],
        "any_required_field_value_present": rollup["any_required_field_value_present"],
        "absence_reason_class": absence["absence_reason_class"],
        "classification": classification["classification"],
        "source_provenance_repair_proposal_emitted": proposal["proposal_emitted"],
        "source_provenance_repair_objective_id": proposal.get("repair_objective_id"),
        "recommended_next_handling": packet["recommended_next_handling"],
        "next_if_accepted": packet["next_if_accepted"],
        "classification_executed_count": 1,
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
        "gate_fix_consumed": True,
        "human_decision_recorded": True,
        "null_reason_classified": absence["absence_reason_class"] == "SOURCE_PAYLOAD_DOES_NOT_EMIT_REQUIRED_VALUES",
        "source_provenance_limit_classified": classification["classification"] == "SOURCE_CONTENT_PROVENANCE_ABSENT_REPAIRABLE",
        "repair_objective_proposal_emitted": proposal["proposal_emitted"] is True,
        "decision_packet_emitted": True,
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
        "source_gate_fix_receipt": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
        "classification": classification["classification"],
        "proposal_id": proposal.get("repair_objective_id"),
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "null_evidence_limit_input_rollup": rel(NULL_LIMIT_INPUT_ROLLUP_PATH),
        "absence_reason_classification": rel(ABSENCE_REASON_CLASSIFICATION_PATH),
        "null_evidence_limit_classification": rel(NULL_LIMIT_CLASSIFICATION_PATH),
        "source_provenance_repair_objective_proposal": rel(SOURCE_PROVENANCE_REPAIR_PROPOSAL_PATH),
        "null_evidence_limit_decision_packet": rel(NULL_LIMIT_DECISION_PACKET_PATH),
        "null_evidence_limit_report": rel(NULL_LIMIT_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "repaired_surface_null_evidence_limit_classification_receipt_v0",
        "receipt_type": "REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT_CLASSIFICATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
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
        "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "null_limit_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "absence_reason_class": absence["absence_reason_class"],
            "classification": classification["classification"],
            "classification_reason": classification["classification_reason"],
            "source_provenance_repair_proposal_emitted": proposal["proposal_emitted"],
            "source_provenance_repair_objective_id": proposal.get("repair_objective_id"),
            "source_provenance_repair_objective_name": proposal.get("repair_objective_name"),
            "recommended_next_handling": packet["recommended_next_handling"],
            "next_if_accepted": packet["next_if_accepted"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "null_limit_guards": guards,
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
    print(f"repaired_surface_null_evidence_limit_receipt_id={receipt_id}")
    print(f"repaired_surface_null_evidence_limit_receipt_path=data/repaired_surface_null_evidence_limit_classification_v0_receipts/{receipt_id}.json")
    print(f"null_evidence_limit_classification_path=data/repaired_surface_null_evidence_limit_classification_v0/null_evidence_limit_classification.json")
    print(f"source_provenance_repair_objective_proposal_path=data/repaired_surface_null_evidence_limit_classification_v0/source_provenance_repair_objective_proposal.json")
    print(f"null_evidence_limit_decision_packet_path=data/repaired_surface_null_evidence_limit_classification_v0/null_evidence_limit_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
