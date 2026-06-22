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

UNIT_ID = "REFINE_FIELD_INTRODUCTION_PROPOSAL_TYPING_V0"
TARGET_UNIT_ID = "field_introduction_proposal_typing_refinement.v0"

SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID = "9ea8fc6e"
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

REQUIRED_PER_FIELD_KEYS = [
    "field_name",
    "field_role",
    "owning_surface",
    "emitting_producer",
    "blocked_loop",
    "blocked_decision",
    "why_required",
    "required_for",
    "where_absence_was_observed",
    "current_source_surface",
    "expected_future_source_surface",
    "null_allowed",
    "null_absence_reason_required",
    "provenance_requirement",
    "allowed_mutation_scope",
    "forbidden_inferred_actions",
    "requested_authorization_decision",
]

AUTHORIZATION_DECISIONS = [
    "ACCEPT_FIELD_INTRODUCTION",
    "DECLINE_FIELD_INTRODUCTION",
    "REQUEST_UPSTREAM_EXISTENCE_AUDIT",
    "MARK_EXPECTED_LIMIT",
    "REJECT_PROPOSAL_AS_UNDECIDABLE",
]

FORBIDDEN_INFERRED_ACTIONS = [
    "do_not_invent_label_value",
    "do_not_create_taxonomy_label",
    "do_not_upgrade_taxonomy",
    "do_not_mutate_source_semantics",
    "do_not_overwrite_historical_source_rows",
    "do_not_mutate_existing_receipts",
    "do_not_auto_open_next_group",
]

FIELD_SPECS = {
    "missing_label_identifier": {
        "field_role": "identifies the specific label that was missing",
        "blocked_decision": "distinguish_one_missing_label_gap_from_another",
        "why_required": "taxonomy-gap missing-label pressure cannot be classified without identifying which label is missing",
        "required_for": "distinguishing one missing-label gap from another",
    },
    "taxonomy_context_ref": {
        "field_role": "identifies the taxonomy context, namespace, or version where the missing-label claim is evaluated",
        "blocked_decision": "determine_taxonomy_context_for_missing_label_claim",
        "why_required": "the same label string can mean different things across taxonomy contexts; classification requires a context reference",
        "required_for": "anchoring missing-label evidence to the correct taxonomy context",
    },
    "current_label_space_ref": {
        "field_role": "identifies the current label space observed by the source payload",
        "blocked_decision": "compare_current_label_space_against_expected_label_space",
        "why_required": "missing-label pressure requires knowing which label space was actually present before claiming something is absent",
        "required_for": "distinguishing current-state absence from taxonomy expectation mismatch",
    },
    "expected_label_space_ref": {
        "field_role": "identifies the expected label space used as the comparison target",
        "blocked_decision": "identify_expected_label_space_for_missing_label_claim",
        "why_required": "a missing label can only be assessed relative to an expected label space",
        "required_for": "checking whether a label is genuinely missing relative to an expected surface",
    },
}

OUT_DIR = ROOT / "data" / "field_introduction_proposal_typing_refinement_v0"
RECEIPT_DIR = ROOT / "data" / "field_introduction_proposal_typing_refinement_v0_receipts"

PROPOSAL_SCHEMA_PATH = OUT_DIR / "field_introduction_proposal_v0_schema.json"
TYPING_AUDIT_PATH = OUT_DIR / "field_introduction_proposal_typing_audit.json"
DECISION_READY_PROPOSAL_PATH = OUT_DIR / "decision_ready_field_introduction_proposal_v0.json"
AUTHORIZATION_PACKET_PATH = OUT_DIR / "field_introduction_authorization_packet.json"
TYPING_REPORT_PATH = OUT_DIR / "field_introduction_proposal_typing_refinement_report.json"

BOUNDARY_RECEIPT_PATH = ROOT / "data" / "null_evidence_field_introduction_boundary_refinement_v0_receipts" / f"{SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID}.json"
FIELD_EXISTENCE_STATUS_PATH = ROOT / "data" / "null_evidence_field_introduction_boundary_refinement_v0" / "field_existence_status_assessment.json"
BOUNDARY_REFINEMENT_PATH = ROOT / "data" / "null_evidence_field_introduction_boundary_refinement_v0" / "field_introduction_boundary_refinement.json"
COARSE_FIELD_INTRO_PROPOSAL_PATH = ROOT / "data" / "null_evidence_field_introduction_boundary_refinement_v0" / "source_provenance_field_introduction_proposal.json"
COARSE_DECISION_PACKET_PATH = ROOT / "data" / "null_evidence_field_introduction_boundary_refinement_v0" / "field_introduction_decision_packet.json"
BOUNDARY_REPORT_PATH = ROOT / "data" / "null_evidence_field_introduction_boundary_refinement_v0" / "field_introduction_boundary_refinement_report.json"

NULL_LIMIT_RECEIPT_PATH = ROOT / "data" / "repaired_surface_null_evidence_limit_classification_v0_receipts" / f"{SOURCE_NULL_LIMIT_RECEIPT_ID}.json"
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
    BOUNDARY_RECEIPT_PATH,
    FIELD_EXISTENCE_STATUS_PATH,
    BOUNDARY_REFINEMENT_PATH,
    COARSE_FIELD_INTRO_PROPOSAL_PATH,
    COARSE_DECISION_PACKET_PATH,
    BOUNDARY_REPORT_PATH,
    NULL_LIMIT_RECEIPT_PATH,
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
    "decision": "REFINE_FIELD_INTRODUCTION_PROPOSAL_TYPING",
    "scope": "make field-introduction proposal decision-ready so authorization can accept, decline, audit, mark expected-limit, or reject as undecidable",
    "source_field_introduction_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
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
    "decision-ready proposal is not field creation",
    "authorization layer decides after proposal typing",
    "proposal must contain enough meaning to decide without interpretive review loop",
    "reject proposal as undecidable is an allowed authorization outcome",
    "do not mutate schema or source payload",
    "do not guess missing label values",
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
        "boundary_receipt": read_json(BOUNDARY_RECEIPT_PATH),
        "existence_status": read_json(FIELD_EXISTENCE_STATUS_PATH),
        "boundary_refinement": read_json(BOUNDARY_REFINEMENT_PATH),
        "coarse_proposal": read_json(COARSE_FIELD_INTRO_PROPOSAL_PATH),
        "coarse_packet": read_json(COARSE_DECISION_PACKET_PATH),
        "boundary_report": read_json(BOUNDARY_REPORT_PATH),
        "null_limit_receipt": read_json(NULL_LIMIT_RECEIPT_PATH),
        "comparison_gate_fix_receipt": read_json(COMPARISON_GATE_FIX_RECEIPT_PATH),
        "failed_rerun_receipt": read_json(FAILED_RERUN_RECEIPT_PATH),
        "field_rows": read_jsonl(RERUN_FIELD_ROWS_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    boundary_receipt = sources["boundary_receipt"]
    metrics = boundary_receipt.get("aggregate_metrics", {})

    if boundary_receipt.get("receipt_id") != SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID:
        failures.append("boundary_receipt_id_wrong")
    if boundary_receipt.get("gate") != "PASS":
        failures.append("boundary_not_pass")
    if metrics.get("proposal_type") != "FIELD_INTRODUCTION_PROPOSAL":
        failures.append("boundary_proposal_type_wrong")
    if metrics.get("refined_action") != "PROPOSE_FIELD_INTRODUCTION":
        failures.append("boundary_refined_action_wrong")
    if metrics.get("current_source_payload_emits_values") is not False:
        failures.append("source_payload_emits_values_unexpected")
    if metrics.get("field_creation_executed_count") != 0:
        failures.append("boundary_created_field")
    if metrics.get("schema_mutation_executed_count") != 0:
        failures.append("boundary_mutated_schema")
    if metrics.get("source_payload_mutation_executed_count") != 0:
        failures.append("boundary_mutated_source_payload")
    if metrics.get("source_mutation_count") != 0:
        failures.append("boundary_mutated_source")
    if metrics.get("missing_label_value_guess_count") != 0:
        failures.append("boundary_guessed_label_value")

    coarse = sources["coarse_proposal"]
    if coarse.get("proposal_type") != "FIELD_INTRODUCTION_PROPOSAL":
        failures.append("coarse_proposal_type_wrong")
    if coarse.get("mutation_executed") is not False:
        failures.append("coarse_proposal_mutated")
    if coarse.get("source_mutation") is not False:
        failures.append("coarse_proposal_source_mutation")

    if len(sources["field_rows"]) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_row_count_wrong")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_schema() -> Dict[str, Any]:
    return {
        "schema_version": "field_introduction_proposal_v0_schema",
        "proposal_type": "FIELD_INTRODUCTION_PROPOSAL_V0",
        "required_top_level_fields": [
            "proposal_id",
            "proposal_type",
            "triggering_failure_class",
            "blocked_loop",
            "blocked_reason",
            "source_pressure_group_key_hash",
            "source_receipt_chain",
            "proposed_introductions",
            "decision_requested",
            "authorization_boundary",
            "forbidden_global_actions",
            "mutation_executed",
        ],
        "required_per_field_keys": REQUIRED_PER_FIELD_KEYS,
        "allowed_decision_requested": AUTHORIZATION_DECISIONS,
        "proposal_validity_rule": "Every proposed field must be specific enough for authorization to accept, decline, request upstream existence audit, mark expected limit, or reject as undecidable without a separate proposal-interpretation loop.",
        "must_not": [
            "create field",
            "mutate schema",
            "mutate source payload",
            "invent field value",
            "create taxonomy label",
            "upgrade taxonomy",
            "mutate source semantics",
            "auto-advance",
        ],
    }

def build_typing_audit(sources: Dict[str, Any]) -> Dict[str, Any]:
    coarse = sources["coarse_proposal"]
    coarse_items = coarse.get("proposed_fields", [])
    present_fields = set()
    missing_by_field = {}

    for item in coarse_items:
        field = item.get("proposed_field_name") or item.get("field_name")
        if not field:
            continue
        present = set(item.keys())
        present_fields.add(field)
        required_alias_safe = []
        for key in REQUIRED_PER_FIELD_KEYS:
            if key == "field_name":
                ok = "field_name" in present or "proposed_field_name" in present
            elif key == "emitting_producer":
                ok = key in present or "emitted_by" in present
            else:
                ok = key in present
            if not ok:
                required_alias_safe.append(key)
        missing_by_field[field] = required_alias_safe

    decision_ready_before = all(not missing_by_field.get(field) for field in PROPOSED_FIELDS)
    return {
        "schema_version": "field_introduction_proposal_typing_audit_v0",
        "source_field_introduction_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
        "source_coarse_proposal": rel(COARSE_FIELD_INTRO_PROPOSAL_PATH),
        "coarse_proposal_type": coarse.get("proposal_type"),
        "coarse_proposed_field_count": len(coarse_items),
        "expected_field_count": len(PROPOSED_FIELDS),
        "coarse_field_names": sorted(present_fields),
        "required_field_names": PROPOSED_FIELDS,
        "missing_decision_ready_keys_by_field": missing_by_field,
        "decision_ready_before_refinement": decision_ready_before,
        "proposal_typing_deficiency_detected": not decision_ready_before,
        "typing_deficiency_class": "PROPOSAL_NOT_DECISION_READY" if not decision_ready_before else "PROPOSAL_ALREADY_DECISION_READY",
        "repair_law": "Do not create another vague review loop; refine proposal into directly decidable authorization object.",
        "field_creation_executed": False,
        "schema_mutation_executed": False,
        "source_payload_mutation_executed": False,
        "source_mutation": False,
        "missing_label_values_guessed": False,
    }

def absence_profile(field_rows: List[Dict[str, Any]]) -> Dict[str, Dict[str, int]]:
    out = {}
    for field in PROPOSED_FIELDS:
        reason_field = f"{field}_absence_reason"
        out[field] = dict(sorted(Counter(row.get(reason_field) for row in field_rows).items(), key=lambda item: str(item[0])))
    return out

def build_decision_ready_proposal(sources: Dict[str, Any], typing_audit: Dict[str, Any]) -> Dict[str, Any]:
    proposal_id = sha8({
        "proposal": "FIELD_INTRODUCTION_PROPOSAL_V0",
        "source_boundary_receipt": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
        "fields": PROPOSED_FIELDS,
        "typing": "decision_ready",
    })
    field_rows = sources["field_rows"]
    absences = absence_profile(field_rows)

    introductions = []
    for field in PROPOSED_FIELDS:
        spec = FIELD_SPECS[field]
        introductions.append({
            "field_name": field,
            "field_role": spec["field_role"],
            "owning_surface": "taxonomy_gap_source_payload",
            "emitting_producer": "taxonomy_gap_detector",
            "blocked_loop": "taxonomy_gap_missing_label_investigation",
            "blocked_decision": spec["blocked_decision"],
            "why_required": spec["why_required"],
            "required_for": spec["required_for"],
            "where_absence_was_observed": [
                rel(RERUN_FIELD_ROWS_PATH),
                rel(FIELD_EXISTENCE_STATUS_PATH),
                rel(BOUNDARY_RECEIPT_PATH),
            ],
            "current_source_surface": "repaired evidence overlay exposes key and absence reason, but source payload does not emit value",
            "expected_future_source_surface": "taxonomy_gap_source_payload emits this field or emits explicit non-applicable/null reason with provenance",
            "null_allowed": True,
            "null_absence_reason_required": True,
            "provenance_requirement": "producer must attach source_trace_ref and source_receipt_ref for emitted value or explicit null reason",
            "allowed_mutation_scope": "add field emission and provenance only; no source semantic reinterpretation",
            "forbidden_inferred_actions": FORBIDDEN_INFERRED_ACTIONS,
            "requested_authorization_decision": AUTHORIZATION_DECISIONS,
            "observed_absence_reason_profile": absences.get(field, {}),
        })

    return {
        "schema_version": "field_introduction_proposal_v0",
        "proposal_id": proposal_id,
        "proposal_type": "FIELD_INTRODUCTION_PROPOSAL_V0",
        "triggering_failure_class": "NONEXISTENT_OR_UNREPRESENTED_FIELD_REQUIRED_FOR_CONTINUATION",
        "blocked_loop": "taxonomy_gap_missing_label_investigation",
        "blocked_reason": "required values are absent from source payload and current evidence surface cannot classify missing-label pressure without them",
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "source_receipt_chain": {
            "field_introduction_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
            "null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
            "comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
            "repaired_surface_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
            "structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
            "taxonomy_gap_evidence_extraction_receipt_id": SOURCE_TAXONOMY_GAP_EVIDENCE_EXTRACTION_RECEIPT_ID,
            "loop_application_receipt_id": SOURCE_LOOP_APPLICATION_RECEIPT_ID,
            "pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
            "top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
            "r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        },
        "proposed_introductions": introductions,
        "decision_requested": AUTHORIZATION_DECISIONS,
        "authorization_boundary": {
            "required": True,
            "reason": "introducing fields changes the source payload/schema contract and must be human-authorized",
            "authorization_layer_options": AUTHORIZATION_DECISIONS,
            "validator_may_reject_as_undecidable": True,
        },
        "forbidden_global_actions": FORBIDDEN_INFERRED_ACTIONS,
        "decision_ready": True,
        "decision_ready_reason": "each proposed field declares role, owner, producer, blocked loop, blocked decision, requirement, null behavior, provenance, allowed mutation scope, forbidden actions, and requested decision",
        "proposal_typing_deficiency_repaired": typing_audit["proposal_typing_deficiency_detected"],
        "mutation_required_if_accepted": True,
        "mutation_executed": False,
        "field_creation_executed": False,
        "schema_mutation_executed": False,
        "source_payload_mutation_executed": False,
        "source_mutation": False,
        "repair_command_emitted": False,
        "build_command_emitted": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "missing_label_values_guessed": False,
        "review_only": True,
    }

def build_authorization_packet(proposal: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduction_authorization_packet_v0",
        "packet_type": "AUTHORIZATION_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "proposal_id": proposal["proposal_id"],
        "proposal_type": proposal["proposal_type"],
        "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "decision_ready": proposal["decision_ready"],
        "requested_authorization_decisions": AUTHORIZATION_DECISIONS,
        "allowed_human_choices": AUTHORIZATION_DECISIONS,
        "recommended_next_handling": "AUTHORIZE_OR_REJECT_FIELD_INTRODUCTION_PROPOSAL",
        "next_if_accepted": "BUILD_SOURCE_PROVENANCE_FIELD_INTRODUCTION_FOR_R1000_TAXONOMY_GAP_VALUES_V0",
        "next_if_audit_requested": "AUDIT_UPSTREAM_EXISTENCE_FOR_R1000_TAXONOMY_GAP_VALUES_V0",
        "next_if_expected_limit": "MARK_R1000_TAXONOMY_GAP_SOURCE_PAYLOAD_EXPECTED_LIMIT_V0",
        "next_if_rejected_as_undecidable": "REPAIR_FIELD_INTRODUCTION_PROPOSAL_TYPING_V0",
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

def build_report(schema: Dict[str, Any], typing_audit: Dict[str, Any], proposal: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduction_proposal_typing_refinement_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_field_introduction_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
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
        "proposal_schema": {
            "schema_version": schema["schema_version"],
            "required_per_field_keys": schema["required_per_field_keys"],
        },
        "typing_audit": {
            "typing_deficiency_class": typing_audit["typing_deficiency_class"],
            "decision_ready_before_refinement": typing_audit["decision_ready_before_refinement"],
            "proposal_typing_deficiency_detected": typing_audit["proposal_typing_deficiency_detected"],
        },
        "decision_ready_proposal": {
            "proposal_id": proposal["proposal_id"],
            "proposal_type": proposal["proposal_type"],
            "decision_ready": proposal["decision_ready"],
            "proposed_field_count": len(proposal["proposed_introductions"]),
        },
        "authorization_packet": {
            "packet_type": packet["packet_type"],
            "recommended_next_handling": packet["recommended_next_handling"],
            "requested_authorization_decisions": packet["requested_authorization_decisions"],
        },
        "typing_refinement_executed": True,
        "decision_ready_proposal_emitted": True,
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

def validate_decision_ready_proposal(proposal: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if proposal.get("proposal_type") != "FIELD_INTRODUCTION_PROPOSAL_V0":
        failures.append("proposal_type_wrong")
    if proposal.get("triggering_failure_class") != "NONEXISTENT_OR_UNREPRESENTED_FIELD_REQUIRED_FOR_CONTINUATION":
        failures.append("triggering_failure_class_wrong")
    if proposal.get("blocked_loop") != "taxonomy_gap_missing_label_investigation":
        failures.append("blocked_loop_wrong")
    if proposal.get("decision_ready") is not True:
        failures.append("proposal_not_decision_ready")
    if proposal.get("decision_requested") != AUTHORIZATION_DECISIONS:
        failures.append("decision_requested_wrong")
    fields = proposal.get("proposed_introductions", [])
    if len(fields) != len(PROPOSED_FIELDS):
        failures.append("proposed_field_count_wrong")
    names = sorted([field.get("field_name") for field in fields])
    if names != sorted(PROPOSED_FIELDS):
        failures.append("proposed_field_names_wrong")
    for item in fields:
        name = item.get("field_name", "<missing>")
        for key in REQUIRED_PER_FIELD_KEYS:
            if key not in item:
                failures.append(f"missing_per_field_key:{name}:{key}")
        if item.get("owning_surface") != "taxonomy_gap_source_payload":
            failures.append(f"owning_surface_wrong:{name}")
        if item.get("emitting_producer") != "taxonomy_gap_detector":
            failures.append(f"emitting_producer_wrong:{name}")
        if item.get("blocked_loop") != "taxonomy_gap_missing_label_investigation":
            failures.append(f"blocked_loop_wrong:{name}")
        if item.get("null_allowed") is not True:
            failures.append(f"null_allowed_wrong:{name}")
        if item.get("null_absence_reason_required") is not True:
            failures.append(f"null_absence_reason_required_wrong:{name}")
        if item.get("requested_authorization_decision") != AUTHORIZATION_DECISIONS:
            failures.append(f"requested_authorization_decision_wrong:{name}")
        forbidden = item.get("forbidden_inferred_actions", [])
        for required in FORBIDDEN_INFERRED_ACTIONS:
            if required not in forbidden:
                failures.append(f"forbidden_action_missing:{name}:{required}")
    for key in [
        "mutation_executed",
        "field_creation_executed",
        "schema_mutation_executed",
        "source_payload_mutation_executed",
        "source_mutation",
        "repair_command_emitted",
        "build_command_emitted",
        "taxonomy_delta_proposal_emitted",
        "taxonomy_upgrade_authorized",
        "missing_label_values_guessed",
    ]:
        if proposal.get(key) is not False:
            failures.append(f"proposal_guard_not_false:{key}:{proposal.get(key)}")
    return failures

def validate_outputs(schema: Dict[str, Any], typing_audit: Dict[str, Any], proposal: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if schema["proposal_type"] != "FIELD_INTRODUCTION_PROPOSAL_V0":
        failures.append("schema_proposal_type_wrong")
    for key in REQUIRED_PER_FIELD_KEYS:
        if key not in schema["required_per_field_keys"]:
            failures.append(f"schema_missing_required_key:{key}")
    if typing_audit["proposal_typing_deficiency_detected"] is not True:
        failures.append("typing_deficiency_not_detected")
    if typing_audit["decision_ready_before_refinement"] is not False:
        failures.append("coarse_proposal_unexpectedly_decision_ready")
    for key in [
        "field_creation_executed",
        "schema_mutation_executed",
        "source_payload_mutation_executed",
        "source_mutation",
        "missing_label_values_guessed",
    ]:
        if typing_audit.get(key) is not False:
            failures.append(f"audit_guard_not_false:{key}:{typing_audit.get(key)}")

    failures.extend(validate_decision_ready_proposal(proposal))

    if packet["packet_type"] != "AUTHORIZATION_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    if packet["decision_ready"] is not True:
        failures.append("packet_not_decision_ready")
    if packet["requested_authorization_decisions"] != AUTHORIZATION_DECISIONS:
        failures.append("packet_requested_decisions_wrong")
    if packet["recommended_next_handling"] != "AUTHORIZE_OR_REJECT_FIELD_INTRODUCTION_PROPOSAL":
        failures.append("packet_recommendation_wrong")
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

    if report["typing_refinement_executed"] is not True:
        failures.append("typing_refinement_not_executed")
    if report["decision_ready_proposal_emitted"] is not True:
        failures.append("decision_ready_proposal_not_emitted")
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
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_field_introduction_boundary_receipt_id") != SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID:
        failures.append("source_boundary_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "PROPOSAL_TYPING_0_BOUNDARY_PROPOSAL_CONSUMED",
        "PROPOSAL_TYPING_1_HUMAN_DECISION_RECORDED",
        "PROPOSAL_TYPING_2_TYPING_DEFICIENCY_DETECTED",
        "PROPOSAL_TYPING_3_SCHEMA_EMITTED",
        "PROPOSAL_TYPING_4_DECISION_READY_PROPOSAL_EMITTED",
        "PROPOSAL_TYPING_5_AUTHORIZATION_PACKET_EMITTED",
        "PROPOSAL_TYPING_6_NO_FIELD_CREATION_OR_SCHEMA_MUTATION",
        "PROPOSAL_TYPING_7_NO_TAXONOMY_ACTION",
        "PROPOSAL_TYPING_8_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("proposal_type") != "FIELD_INTRODUCTION_PROPOSAL_V0":
        failures.append("metric_proposal_type_wrong")
    if metrics.get("decision_ready") is not True:
        failures.append("metric_decision_ready_wrong")
    if metrics.get("typing_deficiency_detected") is not True:
        failures.append("metric_typing_deficiency_not_detected")
    if metrics.get("recommended_next_handling") != "AUTHORIZE_OR_REJECT_FIELD_INTRODUCTION_PROPOSAL":
        failures.append("metric_recommendation_wrong")
    if metrics.get("requested_authorization_decisions") != AUTHORIZATION_DECISIONS:
        failures.append("metric_decisions_wrong")
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

    guards = receipt.get("proposal_typing_guards", {})
    for key in [
        "boundary_proposal_consumed",
        "human_decision_recorded",
        "typing_deficiency_detected",
        "schema_emitted",
        "decision_ready_proposal_emitted",
        "authorization_packet_emitted",
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

    schema = build_schema()
    typing_audit = build_typing_audit(sources)
    decision_ready_proposal = build_decision_ready_proposal(sources, typing_audit)
    authorization_packet = build_authorization_packet(decision_ready_proposal)
    report = build_report(schema, typing_audit, decision_ready_proposal, authorization_packet)

    write_json(PROPOSAL_SCHEMA_PATH, schema)
    write_json(TYPING_AUDIT_PATH, typing_audit)
    write_json(DECISION_READY_PROPOSAL_PATH, decision_ready_proposal)
    write_json(AUTHORIZATION_PACKET_PATH, authorization_packet)
    write_json(TYPING_REPORT_PATH, report)

    failures.extend(validate_outputs(schema, typing_audit, decision_ready_proposal, authorization_packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "PROPOSAL_TYPING_0_BOUNDARY_PROPOSAL_CONSUMED": sources["boundary_receipt"]["receipt_id"] == SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID and sources["boundary_receipt"]["gate"] == "PASS",
        "PROPOSAL_TYPING_1_HUMAN_DECISION_RECORDED": HUMAN_DECISION["decision"] == "REFINE_FIELD_INTRODUCTION_PROPOSAL_TYPING",
        "PROPOSAL_TYPING_2_TYPING_DEFICIENCY_DETECTED": typing_audit["proposal_typing_deficiency_detected"] is True,
        "PROPOSAL_TYPING_3_SCHEMA_EMITTED": PROPOSAL_SCHEMA_PATH.exists(),
        "PROPOSAL_TYPING_4_DECISION_READY_PROPOSAL_EMITTED": decision_ready_proposal["decision_ready"] is True and DECISION_READY_PROPOSAL_PATH.exists(),
        "PROPOSAL_TYPING_5_AUTHORIZATION_PACKET_EMITTED": AUTHORIZATION_PACKET_PATH.exists(),
        "PROPOSAL_TYPING_6_NO_FIELD_CREATION_OR_SCHEMA_MUTATION": report["field_creation_executed"] is False and report["schema_mutation_executed"] is False and report["source_payload_mutation_executed"] is False,
        "PROPOSAL_TYPING_7_NO_TAXONOMY_ACTION": report["taxonomy_delta_proposal_emitted"] is False and report["taxonomy_upgrade_authorized"] is False,
        "PROPOSAL_TYPING_8_NO_SOURCE_MUTATION": source_mutation_detected is False,
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
        "source_field_introduction_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "source_comparison_gate_fix_receipt_id": SOURCE_COMPARISON_GATE_FIX_RECEIPT_ID,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "coarse_proposal_type": typing_audit["coarse_proposal_type"],
        "typing_deficiency_detected": typing_audit["proposal_typing_deficiency_detected"],
        "decision_ready_before_refinement": typing_audit["decision_ready_before_refinement"],
        "proposal_type": decision_ready_proposal["proposal_type"],
        "proposal_id": decision_ready_proposal["proposal_id"],
        "decision_ready": decision_ready_proposal["decision_ready"],
        "proposed_field_count": len(decision_ready_proposal["proposed_introductions"]),
        "proposed_field_names": PROPOSED_FIELDS,
        "required_per_field_key_count": len(REQUIRED_PER_FIELD_KEYS),
        "requested_authorization_decisions": AUTHORIZATION_DECISIONS,
        "recommended_next_handling": authorization_packet["recommended_next_handling"],
        "next_if_accepted": authorization_packet["next_if_accepted"],
        "next_if_audit_requested": authorization_packet["next_if_audit_requested"],
        "next_if_expected_limit": authorization_packet["next_if_expected_limit"],
        "next_if_rejected_as_undecidable": authorization_packet["next_if_rejected_as_undecidable"],
        "typing_refinement_executed_count": 1,
        "decision_ready_proposal_emitted_count": 1,
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
        "boundary_proposal_consumed": True,
        "human_decision_recorded": True,
        "typing_deficiency_detected": typing_audit["proposal_typing_deficiency_detected"],
        "schema_emitted": True,
        "decision_ready_proposal_emitted": decision_ready_proposal["decision_ready"],
        "authorization_packet_emitted": True,
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
        "source_boundary_receipt": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
        "decision_ready_proposal_id": decision_ready_proposal["proposal_id"],
        "proposal_type": decision_ready_proposal["proposal_type"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "field_introduction_proposal_v0_schema": rel(PROPOSAL_SCHEMA_PATH),
        "field_introduction_proposal_typing_audit": rel(TYPING_AUDIT_PATH),
        "decision_ready_field_introduction_proposal_v0": rel(DECISION_READY_PROPOSAL_PATH),
        "field_introduction_authorization_packet": rel(AUTHORIZATION_PACKET_PATH),
        "field_introduction_proposal_typing_refinement_report": rel(TYPING_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "field_introduction_proposal_typing_refinement_receipt_v0",
        "receipt_type": "FIELD_INTRODUCTION_PROPOSAL_TYPING_REFINEMENT_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_field_introduction_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
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
        "proposal_typing_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "typing_deficiency_detected": typing_audit["proposal_typing_deficiency_detected"],
            "decision_ready_before_refinement": typing_audit["decision_ready_before_refinement"],
            "proposal_type": decision_ready_proposal["proposal_type"],
            "proposal_id": decision_ready_proposal["proposal_id"],
            "decision_ready": decision_ready_proposal["decision_ready"],
            "proposed_field_names": PROPOSED_FIELDS,
            "requested_authorization_decisions": AUTHORIZATION_DECISIONS,
            "recommended_next_handling": authorization_packet["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "proposal_typing_guards": guards,
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
    print(f"field_introduction_proposal_typing_receipt_id={receipt_id}")
    print(f"field_introduction_proposal_typing_receipt_path=data/field_introduction_proposal_typing_refinement_v0_receipts/{receipt_id}.json")
    print(f"decision_ready_field_introduction_proposal_path=data/field_introduction_proposal_typing_refinement_v0/decision_ready_field_introduction_proposal_v0.json")
    print(f"field_introduction_authorization_packet_path=data/field_introduction_proposal_typing_refinement_v0/field_introduction_authorization_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
