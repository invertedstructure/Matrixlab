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

UNIT_ID = "FIX_RERUN_REPAIRED_SURFACE_KEY_VISIBILITY_COMPARISON_GATE_V0"
TARGET_UNIT_ID = "repaired_surface_rerun_comparison_gate_fix.v0"

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

OUT_DIR = ROOT / "data" / "repaired_surface_rerun_comparison_gate_fix_v0"
RECEIPT_DIR = ROOT / "data" / "repaired_surface_rerun_comparison_gate_fix_v0_receipts"

CORRECTED_COMPARISON_PATH = OUT_DIR / "corrected_pre_post_repair_evidence_comparison.json"
CORRECTED_RERUN_OUTCOME_PATH = OUT_DIR / "corrected_repaired_surface_evidence_outcome.json"
CORRECTED_DECISION_PACKET_PATH = OUT_DIR / "corrected_repaired_surface_rerun_decision_packet.json"
GATE_FIX_REPORT_PATH = OUT_DIR / "comparison_gate_fix_report.json"

FAILED_RERUN_RECEIPT_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0_receipts" / f"{FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID}.json"
FAILED_RERUN_FIELD_ROWS_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_taxonomy_gap_missing_label_field_rows.jsonl"
FAILED_RERUN_CONTEXT_REFS_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_taxonomy_gap_context_refs.json"
FAILED_RERUN_FIELD_PRESENCE_ROLLUP_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_field_presence_rollup.json"
FAILED_RERUN_EVIDENCE_OUTCOME_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_evidence_outcome.json"
FAILED_RERUN_COMPARISON_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "pre_post_repair_evidence_comparison.json"
FAILED_RERUN_DECISION_PACKET_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_rerun_decision_packet.json"
FAILED_RERUN_REPORT_PATH = ROOT / "data" / "rerun_taxonomy_gap_missing_label_evidence_on_repaired_surface_v0" / "repaired_surface_rerun_report.json"

STRUCTURAL_REF_FIX_RECEIPT_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0_receipts" / f"{SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID}.json"
FIXED_ROWS_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0" / "r1000_pressure_event_rows_taxonomy_gap_field_surface_repaired_structural_refs_fixed.jsonl"
FIXED_TOP_GROUP_ROWS_PATH = ROOT / "data" / "repair_r1000_pressure_event_taxonomy_gap_field_surface_structural_refs_fix_v0" / "top_group_pressure_event_rows_taxonomy_gap_field_surface_repaired_structural_refs_fixed.jsonl"
REPAIR_ELIGIBILITY_RECEIPT_PATH = ROOT / "data" / "localized_evidence_surface_repair_eligibility_v0_receipts" / f"{SOURCE_REPAIR_ELIGIBILITY_RECEIPT_ID}.json"
LOCALIZATION_RECEIPT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_localization_audit_v0_receipts" / f"{SOURCE_LOCALIZATION_AUDIT_RECEIPT_ID}.json"
EVIDENCE_SURFACE_RECEIPT_PATH = ROOT / "data" / "taxonomy_gap_evidence_surface_deficiency_v0_receipts" / f"{SOURCE_EVIDENCE_SURFACE_CLASSIFICATION_RECEIPT_ID}.json"
PRE_REPAIR_EXTRACTION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_evidence_extraction_v0_receipts" / f"{SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID}.json"
LOOP_APPLICATION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0_receipts" / f"{SOURCE_LOOP_APPLICATION_RECEIPT_ID}.json"
PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID}.json"
TOP_GROUP_CLASSIFICATION_RECEIPT_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0_receipts" / f"{SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID}.json"
R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"

FAILED_RERUN_FILES = [
    FAILED_RERUN_RECEIPT_PATH,
    FAILED_RERUN_FIELD_ROWS_PATH,
    FAILED_RERUN_CONTEXT_REFS_PATH,
    FAILED_RERUN_FIELD_PRESENCE_ROLLUP_PATH,
    FAILED_RERUN_EVIDENCE_OUTCOME_PATH,
    FAILED_RERUN_COMPARISON_PATH,
    FAILED_RERUN_DECISION_PACKET_PATH,
    FAILED_RERUN_REPORT_PATH,
]

TRACKED_SOURCE_FILES = [
    STRUCTURAL_REF_FIX_RECEIPT_PATH,
    FIXED_ROWS_PATH,
    FIXED_TOP_GROUP_ROWS_PATH,
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
    "decision": "FIX_RERUN_REPAIRED_SURFACE_COMPARISON_GATE",
    "scope": "correct invalid hard gate requiring key-visibility delta when repaired surface validation already succeeded",
    "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
    "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
    "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
    "not_authorized": [
        "taxonomy_repair",
        "taxonomy_upgrade",
        "taxonomy_delta_proposal",
        "authority_widening",
        "burden_optimization",
        "guessing_missing_label_values",
        "mutating_existing_receipts",
        "overwriting_historical_source_rows",
        "protocol_adoption",
        "next_group_auto_open",
        "build_command",
    ],
}

MUST_NOT_INFER = [
    "comparison gate fix does not rewrite the failed receipt",
    "lack of key-visibility delta is not failure when post-repair keys are present",
    "field key presence is not field value presence",
    "null-with-reason exposes a source content/provenance limit",
    "do not guess missing label values",
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
        "failed_rerun_receipt": read_json(FAILED_RERUN_RECEIPT_PATH),
        "failed_rerun_field_rows": read_jsonl(FAILED_RERUN_FIELD_ROWS_PATH),
        "failed_rerun_context_refs": read_json(FAILED_RERUN_CONTEXT_REFS_PATH),
        "failed_rerun_rollup": read_json(FAILED_RERUN_FIELD_PRESENCE_ROLLUP_PATH),
        "failed_rerun_outcome": read_json(FAILED_RERUN_EVIDENCE_OUTCOME_PATH),
        "failed_rerun_comparison": read_json(FAILED_RERUN_COMPARISON_PATH),
        "failed_rerun_packet": read_json(FAILED_RERUN_DECISION_PACKET_PATH),
        "failed_rerun_report": read_json(FAILED_RERUN_REPORT_PATH),
        "structural_ref_fix_receipt": read_json(STRUCTURAL_REF_FIX_RECEIPT_PATH),
        "repair_eligibility_receipt": read_json(REPAIR_ELIGIBILITY_RECEIPT_PATH),
        "localization_receipt": read_json(LOCALIZATION_RECEIPT_PATH),
        "evidence_surface_receipt": read_json(EVIDENCE_SURFACE_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    failed = sources["failed_rerun_receipt"]
    metrics = failed.get("aggregate_metrics", {})

    if failed.get("receipt_id") != FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID:
        failures.append("failed_rerun_receipt_id_wrong")
    if failed.get("gate") != "FAIL":
        failures.append("failed_rerun_not_fail")
    if failed.get("terminal", {}).get("stop_code") != "STOP_GATE_FAIL":
        failures.append("failed_rerun_stop_not_gate_fail")
    if "repair_did_not_improve_key_visibility" not in failed.get("failures", []):
        failures.append("failed_rerun_not_key_visibility_gate_failure")
    if metrics.get("all_required_field_keys_present") is not True:
        failures.append("failed_rerun_keys_not_present")
    if metrics.get("all_absence_reasons_present") is not True:
        failures.append("failed_rerun_absence_reasons_not_present")
    if metrics.get("all_structural_refs_present") is not True:
        failures.append("failed_rerun_structural_refs_not_present")
    if metrics.get("any_required_field_value_present") is not False:
        failures.append("failed_rerun_unexpected_value_presence")
    if metrics.get("outcome") != "EVIDENCE_SURFACE_REPAIRED_VALUES_ABSENT":
        failures.append("failed_rerun_outcome_wrong")
    if metrics.get("evidence_sufficiency_class") != "EVIDENCE_SURFACE_PRESENT_CONTENT_ABSENT":
        failures.append("failed_rerun_sufficiency_wrong")
    if metrics.get("source_mutation_count") != 0:
        failures.append("failed_rerun_source_mutation")
    if metrics.get("missing_label_value_guess_count") != 0:
        failures.append("failed_rerun_label_guess")

    if len(sources["failed_rerun_field_rows"]) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("failed_rerun_field_row_count_wrong")

    structural = sources["structural_ref_fix_receipt"]
    if structural.get("receipt_id") != SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID or structural.get("gate") != "PASS":
        failures.append("structural_ref_fix_not_pass")
    if structural.get("aggregate_metrics", {}).get("structural_refs_preserved") is not True:
        failures.append("structural_ref_fix_not_valid")

    for path in FAILED_RERUN_FILES:
        if not path.exists():
            failures.append(f"failed_rerun_artifact_missing:{rel(path)}")
    for path in TRACKED_SOURCE_FILES:
        if not tracked(path):
            failures.append(f"tracked_source_missing:{rel(path)}")

    return failures

def build_corrected_comparison(comparison: Dict[str, Any], rollup: Dict[str, Any]) -> Dict[str, Any]:
    corrected = copy.deepcopy(comparison)
    corrected["schema_version"] = "corrected_pre_post_repair_evidence_comparison_v0"
    corrected["source_failed_comparison_artifact"] = rel(FAILED_RERUN_COMPARISON_PATH)
    corrected["invalidated_gate"] = "repair_improved_key_visibility"
    corrected["invalidated_gate_reason"] = "Key-visibility delta is not a valid hard acceptance gate after the repaired overlay has already exposed required keys, absence reasons, and structural refs. Some pre-repair extraction rows may already contain key/presence markers, so delta can be zero while the repaired surface is valid."
    corrected["corrected_acceptance_predicate"] = {
        "all_required_field_keys_present": rollup["all_required_field_keys_present"],
        "all_absence_reasons_present": rollup["all_absence_reasons_present"],
        "all_structural_refs_present": rollup["all_structural_refs_present"],
        "any_required_field_value_present": rollup["any_required_field_value_present"],
    }
    corrected["repair_surface_valid_even_without_key_delta"] = (
        rollup["all_required_field_keys_present"] is True
        and rollup["all_absence_reasons_present"] is True
        and rollup["all_structural_refs_present"] is True
    )
    corrected["key_visibility_delta_required_for_acceptance"] = False
    corrected["value_visibility_delta_required_for_acceptance"] = False
    corrected["review_only"] = False
    return corrected

def build_corrected_outcome(outcome: Dict[str, Any], rollup: Dict[str, Any]) -> Dict[str, Any]:
    corrected = copy.deepcopy(outcome)
    corrected["schema_version"] = "corrected_repaired_surface_evidence_outcome_v0"
    corrected["source_failed_outcome_artifact"] = rel(FAILED_RERUN_EVIDENCE_OUTCOME_PATH)
    corrected["gate_fix_applied"] = True
    corrected["field_surface_repair_validated"] = (
        rollup["all_required_field_keys_present"] is True
        and rollup["all_absence_reasons_present"] is True
        and rollup["all_structural_refs_present"] is True
    )
    corrected["outcome"] = "EVIDENCE_SURFACE_REPAIRED_VALUES_ABSENT"
    corrected["evidence_sufficiency_class"] = "EVIDENCE_SURFACE_PRESENT_CONTENT_ABSENT"
    corrected["recommended_next_unit"] = "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT_V0"
    corrected["taxonomy_delta_evidence_present"] = False
    corrected["taxonomy_upgrade_evidence_present"] = False
    corrected["missing_label_values_guessed"] = False
    corrected["review_only"] = False
    return corrected

def build_corrected_packet(outcome: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "corrected_repaired_surface_rerun_decision_packet_v0",
        "packet_type": "POST_RERUN_GATE_FIX_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
        "corrected_outcome": outcome["outcome"],
        "corrected_evidence_sufficiency_class": outcome["evidence_sufficiency_class"],
        "field_surface_repair_validated": outcome["field_surface_repair_validated"],
        "allowed_human_choices": [
            "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT",
            "REJECT_COMPARISON_GATE_FIX",
            "REQUEST_RERUN_VALIDATOR_ADJUSTMENT",
            "STOP_AND_REVIEW_MANUALLY",
        ],
        "recommended_next_handling": "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT",
        "recommended_next_unit": "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT_V0",
        "may_emit_taxonomy_delta": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_authority_widening": False,
        "may_authorize_burden_optimization": False,
        "may_auto_open_next_group": False,
        "may_mutate_existing_receipts": False,
        "may_guess_missing_label_values": False,
        "review_only": False,
    }

def build_report(corrected_comparison: Dict[str, Any], corrected_outcome: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "comparison_gate_fix_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "source_receipts": {
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
        "invalidated_gate": corrected_comparison["invalidated_gate"],
        "invalidated_gate_reason": corrected_comparison["invalidated_gate_reason"],
        "corrected_acceptance_predicate": corrected_comparison["corrected_acceptance_predicate"],
        "corrected_outcome": corrected_outcome,
        "decision_packet_recommended_next_handling": packet["recommended_next_handling"],
        "gate_fix_executed": True,
        "rerun_reclassified_as_valid_observation": True,
        "repair_command_emitted": False,
        "build_command_emitted": False,
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
    }

def validate_outputs(corrected_comparison: Dict[str, Any], corrected_outcome: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    predicate = corrected_comparison["corrected_acceptance_predicate"]

    if corrected_comparison["invalidated_gate"] != "repair_improved_key_visibility":
        failures.append("wrong_invalidated_gate")
    if corrected_comparison["key_visibility_delta_required_for_acceptance"] is not False:
        failures.append("key_delta_still_required")
    if corrected_comparison["repair_surface_valid_even_without_key_delta"] is not True:
        failures.append("surface_not_valid_without_key_delta")
    if predicate["all_required_field_keys_present"] is not True:
        failures.append("predicate_keys_not_present")
    if predicate["all_absence_reasons_present"] is not True:
        failures.append("predicate_absence_reasons_not_present")
    if predicate["all_structural_refs_present"] is not True:
        failures.append("predicate_structural_refs_not_present")
    if predicate["any_required_field_value_present"] is not False:
        failures.append("predicate_unexpected_value_present")

    if corrected_outcome["field_surface_repair_validated"] is not True:
        failures.append("corrected_surface_not_validated")
    if corrected_outcome["outcome"] != "EVIDENCE_SURFACE_REPAIRED_VALUES_ABSENT":
        failures.append("corrected_outcome_wrong")
    if corrected_outcome["evidence_sufficiency_class"] != "EVIDENCE_SURFACE_PRESENT_CONTENT_ABSENT":
        failures.append("corrected_sufficiency_wrong")
    if corrected_outcome["recommended_next_unit"] != "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT_V0":
        failures.append("corrected_next_unit_wrong")
    for key in ["taxonomy_delta_evidence_present", "taxonomy_upgrade_evidence_present", "missing_label_values_guessed"]:
        if corrected_outcome.get(key) is not False:
            failures.append(f"corrected_outcome_guard_not_false:{key}:{corrected_outcome.get(key)}")

    if packet["packet_type"] != "POST_RERUN_GATE_FIX_REVIEW_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    if packet["recommended_next_unit"] != "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT_V0":
        failures.append("packet_next_unit_wrong")
    for key in [
        "may_emit_taxonomy_delta",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_authority_widening",
        "may_authorize_burden_optimization",
        "may_auto_open_next_group",
        "may_mutate_existing_receipts",
        "may_guess_missing_label_values",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")

    if report["gate_fix_executed"] is not True:
        failures.append("gate_fix_not_executed")
    if report["rerun_reclassified_as_valid_observation"] is not True:
        failures.append("rerun_not_reclassified_as_valid")
    for key in [
        "repair_command_emitted",
        "build_command_emitted",
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

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("failed_repaired_surface_rerun_receipt_id") != FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID:
        failures.append("failed_rerun_receipt_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "COMPARISON_GATE_FIX_0_FAILED_RERUN_CONSUMED",
        "COMPARISON_GATE_FIX_1_HUMAN_DECISION_RECORDED",
        "COMPARISON_GATE_FIX_2_INVALID_GATE_IDENTIFIED",
        "COMPARISON_GATE_FIX_3_POST_REPAIR_SURFACE_VALIDATED",
        "COMPARISON_GATE_FIX_4_CORRECTED_OUTCOME_EMITTED",
        "COMPARISON_GATE_FIX_5_DECISION_PACKET_EMITTED",
        "COMPARISON_GATE_FIX_6_NO_TAXONOMY_ACTION",
        "COMPARISON_GATE_FIX_7_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("failed_rerun_gate") != "repair_improved_key_visibility":
        failures.append("metric_failed_gate_wrong")
    if metrics.get("field_surface_repair_validated") is not True:
        failures.append("metric_surface_not_validated")
    if metrics.get("corrected_outcome") != "EVIDENCE_SURFACE_REPAIRED_VALUES_ABSENT":
        failures.append("metric_corrected_outcome_wrong")
    if metrics.get("recommended_next_unit") != "CLASSIFY_REPAIRED_SURFACE_NULL_EVIDENCE_LIMIT_V0":
        failures.append("metric_next_unit_wrong")
    for key in [
        "repair_command_emitted_count",
        "build_command_emitted_count",
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

    guards = receipt.get("comparison_gate_fix_guards", {})
    for key in [
        "failed_rerun_consumed",
        "human_decision_recorded",
        "invalid_gate_identified",
        "post_repair_surface_validated",
        "corrected_outcome_emitted",
        "decision_packet_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "repair_command_emitted",
        "build_command_emitted",
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
    source_before = snapshot_files(TRACKED_SOURCE_FILES + FAILED_RERUN_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    corrected_comparison = build_corrected_comparison(
        sources["failed_rerun_comparison"],
        sources["failed_rerun_rollup"],
    )
    corrected_outcome = build_corrected_outcome(
        sources["failed_rerun_outcome"],
        sources["failed_rerun_rollup"],
    )
    packet = build_corrected_packet(corrected_outcome)
    report = build_report(corrected_comparison, corrected_outcome, packet)

    write_json(CORRECTED_COMPARISON_PATH, corrected_comparison)
    write_json(CORRECTED_RERUN_OUTCOME_PATH, corrected_outcome)
    write_json(CORRECTED_DECISION_PACKET_PATH, packet)
    write_json(GATE_FIX_REPORT_PATH, report)

    failures.extend(validate_outputs(corrected_comparison, corrected_outcome, packet, report))

    source_after = snapshot_files(TRACKED_SOURCE_FILES + FAILED_RERUN_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "COMPARISON_GATE_FIX_0_FAILED_RERUN_CONSUMED": sources["failed_rerun_receipt"]["receipt_id"] == FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID and sources["failed_rerun_receipt"]["gate"] == "FAIL",
        "COMPARISON_GATE_FIX_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "FIX_RERUN_REPAIRED_SURFACE_COMPARISON_GATE",
        "COMPARISON_GATE_FIX_2_INVALID_GATE_IDENTIFIED": corrected_comparison["invalidated_gate"] == "repair_improved_key_visibility",
        "COMPARISON_GATE_FIX_3_POST_REPAIR_SURFACE_VALIDATED": corrected_outcome["field_surface_repair_validated"] is True,
        "COMPARISON_GATE_FIX_4_CORRECTED_OUTCOME_EMITTED": CORRECTED_RERUN_OUTCOME_PATH.exists() and corrected_outcome["outcome"] == "EVIDENCE_SURFACE_REPAIRED_VALUES_ABSENT",
        "COMPARISON_GATE_FIX_5_DECISION_PACKET_EMITTED": CORRECTED_DECISION_PACKET_PATH.exists(),
        "COMPARISON_GATE_FIX_6_NO_TAXONOMY_ACTION": report["taxonomy_delta_proposal_emitted"] is False and report["taxonomy_upgrade_authorized"] is False,
        "COMPARISON_GATE_FIX_7_NO_SOURCE_MUTATION": source_mutation_detected is False,
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
        "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "accepted_repair_objective_id": SOURCE_REPAIR_OBJECTIVE_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "failed_rerun_gate": "repair_improved_key_visibility",
        "field_surface_repair_validated": corrected_outcome["field_surface_repair_validated"],
        "corrected_outcome": corrected_outcome["outcome"],
        "corrected_evidence_sufficiency_class": corrected_outcome["evidence_sufficiency_class"],
        "recommended_next_unit": corrected_outcome["recommended_next_unit"],
        "gate_fix_executed_count": 1,
        "failed_rerun_consumed_count": 1,
        "repair_command_emitted_count": 0,
        "build_command_emitted_count": 0,
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
        "failed_rerun_consumed": True,
        "human_decision_recorded": True,
        "invalid_gate_identified": corrected_comparison["invalidated_gate"] == "repair_improved_key_visibility",
        "post_repair_surface_validated": corrected_outcome["field_surface_repair_validated"],
        "corrected_outcome_emitted": True,
        "decision_packet_emitted": True,
        "repair_command_emitted": False,
        "build_command_emitted": False,
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
        "failed_rerun_receipt": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
        "corrected_outcome": corrected_outcome["outcome"],
        "recommended_next_unit": corrected_outcome["recommended_next_unit"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "corrected_pre_post_repair_evidence_comparison": rel(CORRECTED_COMPARISON_PATH),
        "corrected_repaired_surface_evidence_outcome": rel(CORRECTED_RERUN_OUTCOME_PATH),
        "corrected_repaired_surface_rerun_decision_packet": rel(CORRECTED_DECISION_PACKET_PATH),
        "comparison_gate_fix_report": rel(GATE_FIX_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "repaired_surface_rerun_comparison_gate_fix_receipt_v0",
        "receipt_type": "REPAIRED_SURFACE_RERUN_COMPARISON_GATE_FIX_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
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
        "gate_fix_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "failed_repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
            "invalidated_gate": corrected_comparison["invalidated_gate"],
            "field_surface_repair_validated": corrected_outcome["field_surface_repair_validated"],
            "corrected_outcome": corrected_outcome["outcome"],
            "corrected_evidence_sufficiency_class": corrected_outcome["evidence_sufficiency_class"],
            "recommended_next_unit": corrected_outcome["recommended_next_unit"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "comparison_gate_fix_guards": guards,
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
    print(f"repaired_surface_comparison_gate_fix_receipt_id={receipt_id}")
    print(f"repaired_surface_comparison_gate_fix_receipt_path=data/repaired_surface_rerun_comparison_gate_fix_v0_receipts/{receipt_id}.json")
    print(f"corrected_repaired_surface_evidence_outcome_path=data/repaired_surface_rerun_comparison_gate_fix_v0/corrected_repaired_surface_evidence_outcome.json")
    print(f"corrected_repaired_surface_rerun_decision_packet_path=data/repaired_surface_rerun_comparison_gate_fix_v0/corrected_repaired_surface_rerun_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
