#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_TYPED_VALUE_SOURCE_VALUE_PROPOSITIONS_V0"
TARGET_UNIT_ID = "cell1.runtime_patch_target_value_source_metadata_value_proposition_review.v0"
LAYER = "CELL_1 / RUNTIME_PATCH_TARGET_VALUE_SOURCE_METADATA_VALUE_PROPOSITION_REVIEW"
MODE = "REVIEW_ONLY / NO_AUTHORIZATION / NO_METADATA_FILL / NO_TIE_BREAK / NO_ACCEPTANCE"
BUILD_MODE = "VALUE_PROPOSITION_REVIEW_ONLY"

SOURCE_VALUE_PROPOSITION_RECEIPT_ID = "c581a69b"
SOURCE_VALUE_PROPOSITION_RECEIPT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0_receipts/c581a69b.json"
SOURCE_ABSENCE_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_value_absence_classification_v0.json"
SOURCE_MACHINE_PROPOSITION_ATTEMPTS_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_machine_readable_value_proposition_attempts_v0.json"
SOURCE_HUMAN_SCHEMA_BOUNDARY_DIAGNOSTIC_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_human_schema_slot_boundary_diagnostic_v0.json"
SOURCE_VALUE_PROPOSITION_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_value_proposition_packet_v0.json"
SOURCE_PROPOSITION_REVIEW_PACKET_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_value_proposition_review_packet_v0.json"
SOURCE_PROPOSED_SOURCE_PACKET_DRAFT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_proposed_source_packet_draft_v0.json"
SOURCE_NULL_REASON_MATRIX_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_value_null_reason_matrix_v0.json"
SOURCE_AUTHORIZATION_CONTRACT_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_value_proposition_authorization_contract_v0.json"
SOURCE_VALUE_PROPOSITION_CLASSIFICATION_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_value_proposition_classification_v0.json"
SOURCE_VALUE_PROPOSITION_ROLLUP_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_value_proposition_rollup_v0.json"
SOURCE_VALUE_PROPOSITION_PROFILE_PATH = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_v0/typed_value_source_value_proposition_profile_v0.json"

OUT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_review_v0"
RECEIPT_DIR = ROOT / "data/cell1_runtime_patch_target_value_source_metadata_value_proposition_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "typed_value_source_value_proposition_review_assessment_v0.json"
MACHINE_GAP_REVIEW_PATH = OUT_DIR / "typed_value_source_machine_readable_gap_review_v0.json"
HUMAN_SCHEMA_REVIEW_PATH = OUT_DIR / "typed_value_source_human_schema_boundary_review_v0.json"
NULL_REASON_REVIEW_PATH = OUT_DIR / "typed_value_source_null_reason_review_v0.json"
DECISION_OPTIONS_PATH = OUT_DIR / "typed_value_source_value_proposition_review_decision_options_v0.json"
REVIEW_FINDINGS_PATH = OUT_DIR / "typed_value_source_value_proposition_review_findings_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "typed_value_source_value_proposition_review_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "typed_value_source_value_proposition_review_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "typed_value_source_value_proposition_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "typed_value_source_value_proposition_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "typed_value_source_value_proposition_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "typed_value_source_value_proposition_review_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_VALUE_PROPOSITION_RECEIPT_PATH,
    SOURCE_ABSENCE_CLASSIFICATION_PATH,
    SOURCE_MACHINE_PROPOSITION_ATTEMPTS_PATH,
    SOURCE_HUMAN_SCHEMA_BOUNDARY_DIAGNOSTIC_PATH,
    SOURCE_VALUE_PROPOSITION_PACKET_PATH,
    SOURCE_PROPOSITION_REVIEW_PACKET_PATH,
    SOURCE_PROPOSED_SOURCE_PACKET_DRAFT_PATH,
    SOURCE_NULL_REASON_MATRIX_PATH,
    SOURCE_AUTHORIZATION_CONTRACT_PATH,
    SOURCE_VALUE_PROPOSITION_CLASSIFICATION_PATH,
    SOURCE_VALUE_PROPOSITION_ROLLUP_PATH,
    SOURCE_VALUE_PROPOSITION_PROFILE_PATH,
]

EXPECTED_SOURCE_STATUS = "TYPED_VALUE_SOURCE_VALUE_PROPOSITIONS_PARTIAL_WITH_ABSENCE_CLASSIFICATION"
EXPECTED_SOURCE_STOP = "STOP_TYPED_VALUE_SOURCE_VALUE_PROPOSITIONS_PARTIAL_WITH_ABSENCE_CLASSIFICATION"
EXPECTED_NEXT = "AUTHORIZE_OR_REVIEW_TYPED_VALUE_SOURCE_VALUE_PROPOSITIONS_V0"

REPAIRABLE_MACHINE_REASONS = {
    "VALUE_PRESENT_BUT_NOT_EXTRACTED",
    "SOURCE_REF_MISSING",
    "SOURCE_FIELD_NOT_TYPED",
    "SOURCE_CONTENT_ABSENT",
    "MULTIPLE_SOURCE_VALUES_TIED",
}

HUMAN_AUTH_REASONS = {
    "HUMAN_DECISION_REQUIRED",
    "SCHEMA_AUTHORIZATION_REQUIRED",
    "NOT_MACHINE_INFERABLE",
}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> List[str]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    receipt = read_json(SOURCE_VALUE_PROPOSITION_RECEIPT_PATH)
    summary = receipt.get("value_proposition_summary", {})
    packet = read_json(SOURCE_VALUE_PROPOSITION_PACKET_PATH)
    machine = read_json(SOURCE_MACHINE_PROPOSITION_ATTEMPTS_PATH)
    human = read_json(SOURCE_HUMAN_SCHEMA_BOUNDARY_DIAGNOSTIC_PATH)
    nulls = read_json(SOURCE_NULL_REASON_MATRIX_PATH)
    classif = read_json(SOURCE_VALUE_PROPOSITION_CLASSIFICATION_PATH)
    roll = read_json(SOURCE_VALUE_PROPOSITION_ROLLUP_PATH)
    profile = read_json(SOURCE_VALUE_PROPOSITION_PROFILE_PATH)

    if receipt.get("receipt_id") != SOURCE_VALUE_PROPOSITION_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("value_proposition_receipt_not_pass")
    if summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"value_proposition_status_not_expected:{summary.get('status')}")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("value_proposition_terminal_not_expected")
    if summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"value_proposition_next_not_expected:{summary.get('recommended_next')}")
    if summary.get("slot_count") != 30:
        failures.append(f"slot_count_not_30:{summary.get('slot_count')}")
    if summary.get("machine_readable_slot_count") != 21:
        failures.append(f"machine_slot_count_not_21:{summary.get('machine_readable_slot_count')}")
    if summary.get("human_or_schema_slot_count") != 9:
        failures.append(f"human_slot_count_not_9:{summary.get('human_or_schema_slot_count')}")
    if summary.get("source_backed_proposed_value_count") != 0:
        failures.append(f"source_backed_proposed_value_count_not_0:{summary.get('source_backed_proposed_value_count')}")
    if summary.get("null_proposition_count") != 30:
        failures.append(f"null_proposition_count_not_30:{summary.get('null_proposition_count')}")
    if summary.get("authorization_required") is not True:
        failures.append("authorization_required_not_true")
    if summary.get("metadata_populated") is not False:
        failures.append("metadata_populated_unexpectedly")
    if summary.get("ready_discriminator_count") != 0:
        failures.append("ready_discriminator_nonzero")
    if summary.get("rule_refined") is not False:
        failures.append("rule_refined_unexpectedly")
    if summary.get("tie_broken") is not False:
        failures.append("tie_broken_unexpectedly")

    if packet.get("packet_status") != EXPECTED_SOURCE_STATUS:
        failures.append("value_proposition_packet_status_wrong")
    if len(packet.get("propositions", [])) != 30:
        failures.append("value_proposition_packet_count_wrong")
    if len(machine.get("attempts", [])) != 21:
        failures.append("machine_attempt_count_wrong")
    if len(human.get("records", [])) != 9:
        failures.append("human_schema_record_count_wrong")
    if nulls.get("null_count") != 30:
        failures.append("null_reason_count_wrong")
    if classif.get("classification_status") != EXPECTED_SOURCE_STATUS:
        failures.append("value_proposition_classification_status_wrong")
    if roll.get("metadata_populated_count") != 0:
        failures.append("rollup_metadata_populated_nonzero")
    if profile.get("metadata_populated") is not False:
        failures.append("profile_metadata_populated_true")

    return failures

def load_records() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    packet = read_json(SOURCE_VALUE_PROPOSITION_PACKET_PATH)
    machine = read_json(SOURCE_MACHINE_PROPOSITION_ATTEMPTS_PATH)
    human = read_json(SOURCE_HUMAN_SCHEMA_BOUNDARY_DIAGNOSTIC_PATH)
    nulls = read_json(SOURCE_NULL_REASON_MATRIX_PATH)
    propositions = [x for x in packet.get("propositions", []) if isinstance(x, dict)]
    attempts = [x for x in machine.get("attempts", []) if isinstance(x, dict)]
    human_records = [x for x in human.get("records", []) if isinstance(x, dict)]
    null_records = [x for x in nulls.get("records", []) if isinstance(x, dict)]
    return propositions, attempts, human_records, null_records

def review_machine_attempts(attempts: List[Dict[str, Any]]) -> Dict[str, Any]:
    absence_counts = Counter(str(a.get("absence_reason")) for a in attempts)
    probe_counts = Counter(str(a.get("source_probe", {}).get("source_probe_status")) for a in attempts)
    repairable = [
        a for a in attempts
        if a.get("absence_reason") in REPAIRABLE_MACHINE_REASONS
    ]

    records = []
    for a in attempts:
        reason = a.get("absence_reason")
        probe = a.get("source_probe", {})
        records.append({
            "slot_id": a.get("slot_id"),
            "row_uid": a.get("row_uid"),
            "field": a.get("field"),
            "slot_category": a.get("slot_category"),
            "absence_reason": reason,
            "source_probe_status": probe.get("source_probe_status"),
            "source_path": probe.get("source_path"),
            "json_path_value_found": probe.get("json_path_value_found"),
            "proposed_value": a.get("proposed_value"),
            "review_classification": "REPAIR_EXTRACTION_SURFACE" if reason in REPAIRABLE_MACHINE_REASONS else "NOT_REPAIRABLE_BY_EXTRACTION",
            "review_note": "Machine-readable slot remained null; review should improve typed source extraction before authorization."
                if reason in REPAIRABLE_MACHINE_REASONS
                else "Machine-readable slot remained null for non-repairable reason under current taxonomy.",
        })

    return {
        "schema_version": "typed_value_source_machine_readable_gap_review_v0",
        "review_status": "MACHINE_READABLE_VALUE_GAPS_REVIEWED",
        "machine_readable_slot_count": len(attempts),
        "source_backed_proposed_value_count": sum(1 for a in attempts if a.get("proposed_value") is not None),
        "repairable_machine_gap_count": len(repairable),
        "absence_reason_counts": dict(absence_counts),
        "source_probe_status_counts": dict(probe_counts),
        "records": records,
        "review_conclusion": "machine_readable_values_are_not_authorizable_yet",
        "recommended_repair": "REPAIR_TYPED_MACHINE_READABLE_VALUE_EXTRACTION_SURFACE_V0",
    }

def review_human_schema(human_records: List[Dict[str, Any]]) -> Dict[str, Any]:
    category_counts = Counter(str(r.get("slot_category")) for r in human_records)
    reason_counts = Counter(str(r.get("why_machine_cannot_infer")) for r in human_records)

    records = []
    for r in human_records:
        records.append({
            "slot_id": r.get("slot_id"),
            "row_uid": r.get("row_uid"),
            "field": r.get("field"),
            "slot_category": r.get("slot_category"),
            "question_being_asked": r.get("question_being_asked"),
            "why_machine_cannot_infer": r.get("why_machine_cannot_infer"),
            "acceptable_answer_shape": r.get("acceptable_answer_shape"),
            "allowed_resolver": r.get("allowed_resolver"),
            "required_authority": r.get("required_authority"),
            "downstream_consumer": r.get("downstream_consumer"),
            "blocked_until_resolved": r.get("blocked_until_resolved"),
            "safe_null_behavior": r.get("safe_null_behavior"),
            "review_classification": "AUTHORIZATION_BOUNDARY_EXPLAINED_NOT_AUTHORIZED",
            "review_note": "Boundary shape is useful, but no human/schema value is authorized by this review unit.",
        })

    return {
        "schema_version": "typed_value_source_human_schema_boundary_review_v0",
        "review_status": "HUMAN_SCHEMA_BOUNDARIES_REVIEWED_NOT_AUTHORIZED",
        "human_or_schema_slot_count": len(human_records),
        "slot_category_counts": dict(category_counts),
        "why_machine_cannot_infer_counts": dict(reason_counts),
        "records": records,
        "review_conclusion": "human_schema_boundaries_are_explained_but_not_resolved",
        "recommended_repair": "AUTHORIZE_OR_REGISTER_SCHEMA_FOR_HUMAN_SCHEMA_VALUE_BOUNDARIES_V0",
    }

def review_nulls(null_records: List[Dict[str, Any]], propositions: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_slot = {p.get("slot_id"): p for p in propositions}
    reason_counts = Counter(str(r.get("absence_reason")) for r in null_records)
    machine_null_count = 0
    human_null_count = 0
    repair_required_count = 0
    authorization_required_count = 0

    records = []
    for n in null_records:
        p = by_slot.get(n.get("slot_id"), {})
        human_schema = bool(n.get("human_schema_only"))
        reason = n.get("absence_reason")
        if human_schema:
            human_null_count += 1
        else:
            machine_null_count += 1
        if reason in REPAIRABLE_MACHINE_REASONS:
            repair_required_count += 1
            review_class = "NULL_REASON_REQUIRES_EXTRACTION_REPAIR"
        elif reason in HUMAN_AUTH_REASONS:
            authorization_required_count += 1
            review_class = "NULL_REASON_REQUIRES_AUTHORIZATION"
        else:
            review_class = "NULL_REASON_NEEDS_TAXONOMY_REVIEW"

        records.append({
            "slot_id": n.get("slot_id"),
            "row_uid": n.get("row_uid"),
            "field": n.get("field"),
            "human_schema_only": human_schema,
            "absence_reason": reason,
            "safe_null_behavior": n.get("safe_null_behavior"),
            "authorization_required": n.get("authorization_required"),
            "proposition_status": p.get("proposition_status"),
            "review_classification": review_class,
        })

    return {
        "schema_version": "typed_value_source_null_reason_review_v0",
        "review_status": "NULL_REASONS_REVIEWED_NOT_ACCEPTED",
        "null_count": len(null_records),
        "machine_null_count": machine_null_count,
        "human_schema_null_count": human_null_count,
        "repair_required_null_count": repair_required_count,
        "authorization_required_null_count": authorization_required_count,
        "absence_reason_counts": dict(reason_counts),
        "records": records,
        "review_conclusion": "null_reasons_are_diagnostic_not_accepted_as_final_values",
    }

def decide_status(machine_review: Dict[str, Any], human_review: Dict[str, Any], null_review: Dict[str, Any]) -> Tuple[str, List[str], str]:
    reason_codes = [
        "VALUE_PROPOSITION_PACKET_REVIEWED",
        "ZERO_SOURCE_BACKED_PROPOSITIONS_CONFIRMED",
        "ALL_VALUES_REMAIN_NULL_WITH_REASONS",
        "NO_AUTHORIZATION_APPLIED",
        "NO_NULL_REASONS_ACCEPTED_AS_FINAL",
    ]

    if machine_review.get("repairable_machine_gap_count", 0) > 0:
        reason_codes.append("MACHINE_READABLE_VALUE_EXTRACTION_SURFACE_REPAIR_REQUIRED")
    if human_review.get("human_or_schema_slot_count", 0) > 0:
        reason_codes.append("HUMAN_SCHEMA_BOUNDARIES_REVIEWED_BUT_NOT_AUTHORIZED")

    status = "TYPED_VALUE_SOURCE_VALUE_PROPOSITION_REVIEWED_REQUIRES_EXTRACTION_REPAIR_BEFORE_AUTHORIZATION"
    next_edge = "REPAIR_TYPED_MACHINE_READABLE_VALUE_EXTRACTION_SURFACE_V0"
    return status, reason_codes, next_edge

def build_decision_options(next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_value_proposition_review_decision_options_v0",
        "decision_options_status": "REVIEW_OPTIONS_EMITTED",
        "safe_options": [
            {
                "option": "REPAIR_MACHINE_READABLE_EXTRACTION_SURFACE",
                "recommended": True,
                "next_unit": "REPAIR_TYPED_MACHINE_READABLE_VALUE_EXTRACTION_SURFACE_V0",
                "meaning": "Improve extraction/proposition surface for the 21 machine-readable slots before any authorization.",
            },
            {
                "option": "REVIEW_HUMAN_SCHEMA_BOUNDARY_CATEGORIES",
                "recommended": False,
                "next_unit": "REVIEW_TYPED_HUMAN_SCHEMA_VALUE_BOUNDARY_CATEGORIES_V0",
                "meaning": "Refine the 9 human/schema boundary diagnostics if the questions are still too vague.",
            },
            {
                "option": "AUTHORIZE_NULL_REASONS",
                "recommended": False,
                "next_unit": "AUTHORIZE_TYPED_VALUE_SOURCE_VALUE_PROPOSITIONS_V0",
                "meaning": "Not recommended now because all 21 machine-readable slots are still null and repairable.",
            },
            {
                "option": "FREEZE_AS_DIAGNOSTIC_REFERENCE",
                "recommended": False,
                "next_unit": "FREEZE_TYPED_VALUE_SOURCE_VALUE_PROPOSITION_REVIEW_V0",
                "meaning": "Freeze this review as a reference only if we stop this branch.",
            },
        ],
        "selected_recommended_next": next_edge,
        "forbidden_shortcuts": [
            "manual raw value entry as default",
            "authorizing all null reasons without extraction repair",
            "metadata population",
            "discriminator readiness",
            "dominance rule refinement",
            "tie break",
            "target selection",
            "runtime patch",
            "C5",
        ],
    }

def authority_boundary_obj(status: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_value_proposition_review_authority_boundary_v0",
        "status": status,
        "may_review_propositions": True,
        "may_classify_review_result": True,
        "may_recommend_extraction_repair": True,
        "may_authorize_values": False,
        "may_accept_null_reasons_as_final": False,
        "may_materialize_source_packet_for_review": False,
        "may_populate_metadata": False,
        "may_evaluate_discriminators": False,
        "may_refine_rule": False,
        "may_break_tie": False,
        "may_emit_candidate_values_for_target": False,
        "may_declare_target_candidate_for_review": False,
        "may_select_target_for_build": False,
        "may_accept_for_build": False,
        "may_apply_runtime_patch": False,
        "may_modify_target_files": False,
        "may_open_c5": False,
        "may_grant_general_cell1_authority": False,
        "may_use_latest_file_guessing": False,
        "may_use_mtime_selection": False,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

def rollup_obj(status: str, machine_review: Dict[str, Any], human_review: Dict[str, Any], null_review: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_value_proposition_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "review_assessment_emitted_count": 1,
        "machine_gap_review_emitted_count": 1,
        "human_schema_review_emitted_count": 1,
        "null_reason_review_emitted_count": 1,
        "decision_options_emitted_count": 1,
        "slot_count": 30,
        "machine_readable_slot_count": machine_review.get("machine_readable_slot_count", 0),
        "human_or_schema_slot_count": human_review.get("human_or_schema_slot_count", 0),
        "source_backed_proposed_value_count": 0,
        "null_proposition_count": null_review.get("null_count", 0),
        "repairable_machine_gap_count": machine_review.get("repairable_machine_gap_count", 0),
        "human_schema_boundary_review_count": human_review.get("human_or_schema_slot_count", 0),
        "null_reason_accepted_count": 0,
        "authorization_applied_count": 0,
        "values_supplied_count": 0,
        "source_packet_materialized_for_review_count": 0,
        "metadata_populated_count": 0,
        "ready_discriminator_count": 0,
        "rule_refined_count": 0,
        "tie_broken_count": 0,
        "candidate_values_filled_count": 0,
        "target_candidate_declared_for_review_count": 0,
        "target_selected_for_build_count": 0,
        "accepted_for_build_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "proposal_status_promoted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "unbounded_payload_inspection_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": next_edge,
    }

def profile_obj(roll: Dict[str, Any]) -> Dict[str, Any]:
    zero_keys = [
        "null_reason_accepted_count",
        "authorization_applied_count",
        "values_supplied_count",
        "source_packet_materialized_for_review_count",
        "metadata_populated_count",
        "ready_discriminator_count",
        "rule_refined_count",
        "tie_broken_count",
        "candidate_values_filled_count",
        "target_candidate_declared_for_review_count",
        "target_selected_for_build_count",
        "accepted_for_build_count",
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "c5_opened_count",
        "general_cell1_authority_granted_count",
        "taxonomy_registry_mutation_count",
        "proposal_status_promoted_count",
        "accepted_proposal_fabricated_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "hidden_next_command_count",
        "unbounded_payload_inspection_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]
    return {
        "schema_version": "typed_value_source_value_proposition_review_profile_v0",
        "profile_id": "value_proposition_review_profile_" + sha8(roll),
        "status": roll["classification_status"],
        "review_completed": True,
        "authorization_applied": False,
        "null_reasons_accepted": False,
        "source_packet_materialized_for_review": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "rule_refined": False,
        "tie_broken": False,
        "candidate_values_filled": False,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "c5_opened": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": all(roll.get(k) == 0 for k in zero_keys),
        "recommended_next": roll["recommended_next"],
        "next_command_goal": None,
    }

def report_obj(status: str, reason_codes: List[str], roll: Dict[str, Any], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_value_proposition_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The value proposition packet was reviewed but not authorized; with zero source-backed propositions and all machine slots null, extraction repair should precede authorization.",
        "slot_count": roll["slot_count"],
        "machine_readable_slot_count": roll["machine_readable_slot_count"],
        "human_or_schema_slot_count": roll["human_or_schema_slot_count"],
        "source_backed_proposed_value_count": roll["source_backed_proposed_value_count"],
        "null_proposition_count": roll["null_proposition_count"],
        "repairable_machine_gap_count": roll["repairable_machine_gap_count"],
        "recommended_next_handling": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "authorization_applied_count": 0,
        "null_reason_accepted_count": 0,
        "values_supplied_count": 0,
        "source_packet_materialized_for_review_count": 0,
        "metadata_populated_count": 0,
        "ready_discriminator_count": 0,
        "rule_refined_count": 0,
        "tie_broken_count": 0,
        "candidate_values_filled_count": 0,
        "target_candidate_declared_for_review_count": 0,
        "target_selected_for_build_count": 0,
        "accepted_for_build_count": 0,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "c5_opened_count": 0,
        "general_cell1_authority_granted_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
    }

def transition_trace_obj(status: str, reason_codes: List[str], next_edge: str) -> Dict[str, Any]:
    return {
        "schema_version": "typed_value_source_value_proposition_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_value_proposition_packet",
                "question": "should propositions be authorized now",
                "answer": "no; review first, no authorization",
                "taken": "review proposition quality and null reasons",
            },
            {
                "step": "review_machine_readable_gaps",
                "question": "are machine-readable values authorizable",
                "answer": "no source-backed propositions exist",
                "taken": "recommend extraction-surface repair before authorization",
            },
            {
                "step": "review_human_schema_boundaries",
                "question": "are human/schema slots authorized",
                "answer": "not in this unit",
                "taken": "preserve boundary diagnostics",
            },
            {
                "step": "classify_review",
                "question": "what is the next lawful edge",
                "answer": status,
                "reason_codes": reason_codes,
                "taken": next_edge,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_basis()

    propositions, attempts, human_records, null_records = load_records() if not failures else ([], [], [], [])

    machine_review = review_machine_attempts(attempts)
    human_review = review_human_schema(human_records)
    null_review = review_nulls(null_records, propositions)

    if failures:
        status = "TYPED_VALUE_SOURCE_VALUE_PROPOSITION_REVIEW_BASIS_FAIL"
        reason_codes = failures
        next_edge = "REPAIR_TYPED_VALUE_SOURCE_VALUE_PROPOSITION_REVIEW_BASIS_V0"
    else:
        status, reason_codes, next_edge = decide_status(machine_review, human_review, null_review)

    roll = rollup_obj(status, machine_review, human_review, null_review, next_edge)
    prof = profile_obj(roll)
    rep = report_obj(status, reason_codes, roll, next_edge)
    boundary = authority_boundary_obj(status)
    decision_options = build_decision_options(next_edge)
    trace = transition_trace_obj(status, reason_codes, next_edge)

    review_assessment = {
        "schema_version": "typed_value_source_value_proposition_review_assessment_v0",
        "review_status": status,
        "source_value_proposition_receipt_id": SOURCE_VALUE_PROPOSITION_RECEIPT_ID,
        "review_mode": "review_first_no_authorization",
        "slot_count": roll["slot_count"],
        "machine_readable_slot_count": roll["machine_readable_slot_count"],
        "human_or_schema_slot_count": roll["human_or_schema_slot_count"],
        "source_backed_proposed_value_count": roll["source_backed_proposed_value_count"],
        "null_proposition_count": roll["null_proposition_count"],
        "repairable_machine_gap_count": roll["repairable_machine_gap_count"],
        "authorization_applied": False,
        "null_reasons_accepted": False,
        "review_conclusion": "Do not authorize now; repair machine-readable extraction surface first.",
        "recommended_next": next_edge,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
    }

    findings = {
        "schema_version": "typed_value_source_value_proposition_review_findings_v0",
        "findings_status": "VALUE_PROPOSITION_REVIEW_FINDINGS_EMITTED",
        "findings": [
            {
                "finding": "ZERO_SOURCE_BACKED_PROPOSITIONS",
                "detail": "No slot has a source-backed proposed value.",
                "action": "Do not materialize source packet from this proposition packet.",
            },
            {
                "finding": "ALL_VALUES_NULL",
                "detail": "All 30 slots remain null with absence reasons.",
                "action": "Review null reasons as diagnostics, not final accepted values.",
            },
            {
                "finding": "MACHINE_READABLE_GAPS_REPAIRABLE",
                "detail": f"{roll['repairable_machine_gap_count']} machine-readable gaps require extraction-surface repair.",
                "action": "Repair extraction before authorization.",
            },
            {
                "finding": "HUMAN_SCHEMA_BOUNDARIES_NOT_AUTHORIZED",
                "detail": f"{roll['human_or_schema_slot_count']} human/schema boundary slots remain diagnostic only.",
                "action": "Do not authorize in review unit.",
            },
        ],
    }

    classification = {
        "schema_version": "typed_value_source_value_proposition_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "slot_count": roll["slot_count"],
        "machine_readable_slot_count": roll["machine_readable_slot_count"],
        "human_or_schema_slot_count": roll["human_or_schema_slot_count"],
        "source_backed_proposed_value_count": roll["source_backed_proposed_value_count"],
        "null_proposition_count": roll["null_proposition_count"],
        "repairable_machine_gap_count": roll["repairable_machine_gap_count"],
        "authorization_applied": False,
        "null_reasons_accepted": False,
        "source_packet_materialized_for_review": False,
        "metadata_populated": False,
        "ready_discriminator_count": 0,
        "real_tie_proven": False,
        "rule_refined": False,
        "tie_broken": False,
        "candidate_values_filled": False,
        "target_candidate_declared_for_review": False,
        "target_selected_for_build": False,
        "accepted_for_build": False,
        "runtime_patch_authorized": False,
        "target_file_modification_authorized": False,
        "c5_authorized": False,
        "general_cell1_authority_granted": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
        "recommended_next": next_edge,
        "next_command_goal": None,
    }

    write_json(REVIEW_ASSESSMENT_PATH, review_assessment)
    write_json(MACHINE_GAP_REVIEW_PATH, machine_review)
    write_json(HUMAN_SCHEMA_REVIEW_PATH, human_review)
    write_json(NULL_REASON_REVIEW_PATH, null_review)
    write_json(DECISION_OPTIONS_PATH, decision_options)
    write_json(REVIEW_FINDINGS_PATH, findings)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(AUTHORITY_BOUNDARY_PATH, boundary)
    write_json(ROLLUP_PATH, roll)
    write_json(PROFILE_PATH, prof)
    write_json(REPORT_PATH, rep)
    write_json(TRANSITION_TRACE_PATH, trace)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")
        roll["source_mutation_count"] = 1
        rep["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, roll)
        write_json(REPORT_PATH, rep)

    acceptance_gate_results = {
        "PROPOSITION_REVIEW_0_VALUE_PROPOSITION_RECEIPT_CONSUMED": SOURCE_VALUE_PROPOSITION_RECEIPT_PATH.exists(),
        "PROPOSITION_REVIEW_1_PROPOSITION_PACKET_CONSUMED": SOURCE_VALUE_PROPOSITION_PACKET_PATH.exists(),
        "PROPOSITION_REVIEW_2_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "PROPOSITION_REVIEW_3_MACHINE_GAP_REVIEW_EMITTED": MACHINE_GAP_REVIEW_PATH.exists(),
        "PROPOSITION_REVIEW_4_HUMAN_SCHEMA_REVIEW_EMITTED": HUMAN_SCHEMA_REVIEW_PATH.exists(),
        "PROPOSITION_REVIEW_5_NULL_REASON_REVIEW_EMITTED": NULL_REASON_REVIEW_PATH.exists(),
        "PROPOSITION_REVIEW_6_DECISION_OPTIONS_EMITTED": DECISION_OPTIONS_PATH.exists(),
        "PROPOSITION_REVIEW_7_REVIEW_FINDINGS_EMITTED": REVIEW_FINDINGS_PATH.exists(),
        "PROPOSITION_REVIEW_8_NO_AUTHORIZATION_APPLIED": roll["authorization_applied_count"] == 0,
        "PROPOSITION_REVIEW_9_NO_NULL_REASONS_ACCEPTED": roll["null_reason_accepted_count"] == 0,
        "PROPOSITION_REVIEW_10_NO_VALUES_SUPPLIED": roll["values_supplied_count"] == 0,
        "PROPOSITION_REVIEW_11_NO_SOURCE_PACKET_MATERIALIZED": roll["source_packet_materialized_for_review_count"] == 0,
        "PROPOSITION_REVIEW_12_NO_METADATA_POPULATION": roll["metadata_populated_count"] == 0,
        "PROPOSITION_REVIEW_13_NO_DISCRIMINATOR_READY": roll["ready_discriminator_count"] == 0,
        "PROPOSITION_REVIEW_14_NO_RULE_REFINEMENT": roll["rule_refined_count"] == 0,
        "PROPOSITION_REVIEW_15_NO_TIE_BREAK": roll["tie_broken_count"] == 0,
        "PROPOSITION_REVIEW_16_NO_CANDIDATE_VALUES_FILLED": roll["candidate_values_filled_count"] == 0,
        "PROPOSITION_REVIEW_17_NO_TARGET_CANDIDATE_DECLARED_FOR_REVIEW": classification["target_candidate_declared_for_review"] is False,
        "PROPOSITION_REVIEW_18_NO_TARGET_SELECTED_FOR_BUILD": classification["target_selected_for_build"] is False,
        "PROPOSITION_REVIEW_19_NO_ACCEPTED_FOR_BUILD": classification["accepted_for_build"] is False,
        "PROPOSITION_REVIEW_20_NO_RUNTIME_PATCH": classification["runtime_patch_authorized"] is False,
        "PROPOSITION_REVIEW_21_NO_TARGET_FILE_MODIFICATION": classification["target_file_modification_authorized"] is False,
        "PROPOSITION_REVIEW_22_NO_C5_OPENED": classification["c5_authorized"] is False,
        "PROPOSITION_REVIEW_23_NO_GENERAL_CELL1_AUTHORITY": classification["general_cell1_authority_granted"] is False,
        "PROPOSITION_REVIEW_24_NO_LATEST_FILE_GUESSING": classification["latest_file_guessing"] is False,
        "PROPOSITION_REVIEW_25_NO_MTIME_SELECTION": classification["mtime_selection"] is False,
        "PROPOSITION_REVIEW_26_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "PROPOSITION_REVIEW_27_ACCEPTANCE_BOUNDARY_RETAINED": classification["acceptance_boundary"] == "human_or_prevalidated_schema_acceptance_required",
        "PROPOSITION_REVIEW_28_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_VALUE_SOURCE_VALUE_PROPOSITION_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "slot_count": roll["slot_count"],
        "repairable_machine_gap_count": roll["repairable_machine_gap_count"],
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "typed_value_source_value_proposition_review_receipt_v0",
        "receipt_type": "TYPED_VALUE_SOURCE_VALUE_PROPOSITION_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_value_proposition_receipt_id": SOURCE_VALUE_PROPOSITION_RECEIPT_ID,
        "value_proposition_review_summary": {
            "status": status,
            "reason_codes": reason_codes,
            "slot_count": roll["slot_count"],
            "machine_readable_slot_count": roll["machine_readable_slot_count"],
            "human_or_schema_slot_count": roll["human_or_schema_slot_count"],
            "source_backed_proposed_value_count": roll["source_backed_proposed_value_count"],
            "null_proposition_count": roll["null_proposition_count"],
            "repairable_machine_gap_count": roll["repairable_machine_gap_count"],
            "authorization_applied": False,
            "null_reasons_accepted": False,
            "review_completed": True,
            "source_packet_materialized_for_review": False,
            "metadata_populated": False,
            "ready_discriminator_count": 0,
            "real_tie_proven": False,
            "rule_refined": False,
            "tie_broken": False,
            "candidate_values_filled": False,
            "target_candidate_declared_for_review": False,
            "target_selected_for_build": False,
            "accepted_for_build": False,
            "runtime_patch_applied": False,
            "target_file_modified": False,
            "c5_opened": False,
            "general_cell1_authority_granted": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "acceptance_boundary": "human_or_prevalidated_schema_acceptance_required",
            "bad_counters_zero": prof["bad_counters_zero"],
            "recommended_next": next_edge,
        },
        "aggregate_metrics": rep,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "machine_gap_review": rel(MACHINE_GAP_REVIEW_PATH),
            "human_schema_review": rel(HUMAN_SCHEMA_REVIEW_PATH),
            "null_reason_review": rel(NULL_REASON_REVIEW_PATH),
            "decision_options": rel(DECISION_OPTIONS_PATH),
            "review_findings": rel(REVIEW_FINDINGS_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"value_proposition_review_receipt_id={receipt_id}")
    print(f"value_proposition_review_receipt_path={rel(receipt_path)}")
    print(f"value_proposition_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"machine_gap_review_path={rel(MACHINE_GAP_REVIEW_PATH)}")
    print(f"human_schema_review_path={rel(HUMAN_SCHEMA_REVIEW_PATH)}")
    print(f"null_reason_review_path={rel(NULL_REASON_REVIEW_PATH)}")
    print(f"value_proposition_review_decision_options_path={rel(DECISION_OPTIONS_PATH)}")
    print(f"value_proposition_review_findings_path={rel(REVIEW_FINDINGS_PATH)}")
    print(f"value_proposition_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"value_proposition_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
