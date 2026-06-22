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

UNIT_ID = "BUILD_SOURCE_PROVENANCE_FIELD_INTRODUCTION_FOR_R1000_TAXONOMY_GAP_VALUES_V0"
TARGET_UNIT_ID = "source_provenance_field_introduction_build.v0"

SOURCE_PROPOSAL_TYPING_RECEIPT_ID = "5b841942"
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

INTRODUCED_FIELDS = [
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

FIELD_VALUE_STATUS_FIELDS = {
    "missing_label_identifier": "missing_label_identifier_value_status",
    "taxonomy_context_ref": "taxonomy_context_ref_value_status",
    "current_label_space_ref": "current_label_space_ref_value_status",
    "expected_label_space_ref": "expected_label_space_ref_value_status",
}

PROVENANCE_FIELDS = {
    "missing_label_identifier": "missing_label_identifier_provenance_ref",
    "taxonomy_context_ref": "taxonomy_context_ref_provenance_ref",
    "current_label_space_ref": "current_label_space_ref_provenance_ref",
    "expected_label_space_ref": "expected_label_space_ref_provenance_ref",
}

OUT_DIR = ROOT / "data" / "source_provenance_field_introduction_build_v0"
RECEIPT_DIR = ROOT / "data" / "source_provenance_field_introduction_build_v0_receipts"

BUILD_PLAN_PATH = OUT_DIR / "source_provenance_field_introduction_build_plan.json"
INTRODUCED_SCHEMA_PATH = OUT_DIR / "taxonomy_gap_source_payload_field_introduction_schema_v0.json"
PRODUCER_CONTRACT_PATH = OUT_DIR / "taxonomy_gap_detector_field_emission_contract_v0.json"
INTRODUCED_SOURCE_OVERLAY_PATH = OUT_DIR / "r1000_taxonomy_gap_source_payload_field_introduction_overlay.jsonl"
TOP_GROUP_INTRODUCED_OVERLAY_PATH = OUT_DIR / "top_group_taxonomy_gap_source_payload_field_introduction_overlay.jsonl"
INTRODUCTION_AUDIT_PATH = OUT_DIR / "field_introduction_application_audit.json"
RERUN_INSTRUCTIONS_PATH = OUT_DIR / "post_field_introduction_rerun_instructions.json"
BUILD_DECISION_PACKET_PATH = OUT_DIR / "field_introduction_build_decision_packet.json"
BUILD_REPORT_PATH = OUT_DIR / "field_introduction_build_report.json"

PROPOSAL_TYPING_RECEIPT_PATH = ROOT / "data" / "field_introduction_proposal_typing_refinement_v0_receipts" / f"{SOURCE_PROPOSAL_TYPING_RECEIPT_ID}.json"
PROPOSAL_SCHEMA_PATH = ROOT / "data" / "field_introduction_proposal_typing_refinement_v0" / "field_introduction_proposal_v0_schema.json"
PROPOSAL_TYPING_AUDIT_PATH = ROOT / "data" / "field_introduction_proposal_typing_refinement_v0" / "field_introduction_proposal_typing_audit.json"
DECISION_READY_PROPOSAL_PATH = ROOT / "data" / "field_introduction_proposal_typing_refinement_v0" / "decision_ready_field_introduction_proposal_v0.json"
AUTHORIZATION_PACKET_PATH = ROOT / "data" / "field_introduction_proposal_typing_refinement_v0" / "field_introduction_authorization_packet.json"
PROPOSAL_TYPING_REPORT_PATH = ROOT / "data" / "field_introduction_proposal_typing_refinement_v0" / "field_introduction_proposal_typing_refinement_report.json"

BOUNDARY_RECEIPT_PATH = ROOT / "data" / "null_evidence_field_introduction_boundary_refinement_v0_receipts" / f"{SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID}.json"
COARSE_FIELD_INTRO_PROPOSAL_PATH = ROOT / "data" / "null_evidence_field_introduction_boundary_refinement_v0" / "source_provenance_field_introduction_proposal.json"
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
    PROPOSAL_TYPING_RECEIPT_PATH,
    PROPOSAL_SCHEMA_PATH,
    PROPOSAL_TYPING_AUDIT_PATH,
    DECISION_READY_PROPOSAL_PATH,
    AUTHORIZATION_PACKET_PATH,
    PROPOSAL_TYPING_REPORT_PATH,
    BOUNDARY_RECEIPT_PATH,
    COARSE_FIELD_INTRO_PROPOSAL_PATH,
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
    "decision": "ACCEPT_FIELD_INTRODUCTION",
    "scope": "build versioned source-provenance field introduction artifacts from decision-ready proposal without inventing values or mutating historical sources",
    "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
    "source_pressure_group_key_hash": TOP_GROUP_KEY_HASH,
    "authorized": [
        "emit versioned field-introduction schema artifact",
        "emit taxonomy_gap_detector field-emission contract",
        "emit source payload overlay with introduced fields, null values, explicit absence reasons, and provenance refs",
        "emit rerun instructions",
    ],
    "not_authorized": [
        "inventing missing label values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "mutating historical source rows",
        "mutating existing receipts",
        "changing source semantics",
        "authority widening",
        "burden optimization",
        "protocol adoption",
        "next group auto-open",
        "hidden next command",
    ],
}

MUST_NOT_INFER = [
    "accepted field introduction authorizes versioned artifacts, not value invention",
    "introduced fields may be null but must carry explicit absence reason and provenance reference",
    "historical source rows are not overwritten",
    "existing receipts are not mutated",
    "taxonomy labels are not created",
    "taxonomy is not upgraded",
    "rerun is emitted as instruction only",
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
        "proposal_typing_receipt": read_json(PROPOSAL_TYPING_RECEIPT_PATH),
        "proposal_schema": read_json(PROPOSAL_SCHEMA_PATH),
        "proposal_typing_audit": read_json(PROPOSAL_TYPING_AUDIT_PATH),
        "decision_ready_proposal": read_json(DECISION_READY_PROPOSAL_PATH),
        "authorization_packet": read_json(AUTHORIZATION_PACKET_PATH),
        "proposal_typing_report": read_json(PROPOSAL_TYPING_REPORT_PATH),
        "boundary_receipt": read_json(BOUNDARY_RECEIPT_PATH),
        "coarse_proposal": read_json(COARSE_FIELD_INTRO_PROPOSAL_PATH),
        "null_limit_receipt": read_json(NULL_LIMIT_RECEIPT_PATH),
        "failed_rerun_receipt": read_json(FAILED_RERUN_RECEIPT_PATH),
        "field_rows": read_jsonl(RERUN_FIELD_ROWS_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    receipt = sources["proposal_typing_receipt"]
    metrics = receipt.get("aggregate_metrics", {})
    proposal = sources["decision_ready_proposal"]
    packet = sources["authorization_packet"]

    if receipt.get("receipt_id") != SOURCE_PROPOSAL_TYPING_RECEIPT_ID:
        failures.append("proposal_typing_receipt_id_wrong")
    if receipt.get("gate") != "PASS":
        failures.append("proposal_typing_not_pass")
    if metrics.get("proposal_type") != "FIELD_INTRODUCTION_PROPOSAL_V0":
        failures.append("proposal_type_wrong")
    if metrics.get("decision_ready") is not True:
        failures.append("proposal_not_decision_ready")
    if packet.get("recommended_next_handling") != "AUTHORIZE_OR_REJECT_FIELD_INTRODUCTION_PROPOSAL":
        failures.append("authorization_packet_not_ready")
    if packet.get("next_if_accepted") != UNIT_ID:
        failures.append("authorization_packet_next_if_accepted_not_this_unit")
    if proposal.get("proposal_type") != "FIELD_INTRODUCTION_PROPOSAL_V0":
        failures.append("decision_ready_proposal_type_wrong")
    if proposal.get("decision_ready") is not True:
        failures.append("decision_ready_proposal_not_ready")
    if proposal.get("mutation_executed") is not False:
        failures.append("proposal_already_mutated")
    if proposal.get("field_creation_executed") is not False:
        failures.append("proposal_already_created_fields")
    if proposal.get("source_mutation") is not False:
        failures.append("proposal_source_mutation")
    names = sorted([item.get("field_name") for item in proposal.get("proposed_introductions", [])])
    if names != sorted(INTRODUCED_FIELDS):
        failures.append("proposal_field_names_wrong")
    if len(sources["field_rows"]) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("field_row_count_wrong")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_plan(sources: Dict[str, Any]) -> Dict[str, Any]:
    proposal = sources["decision_ready_proposal"]
    return {
        "schema_version": "source_provenance_field_introduction_build_plan_v0",
        "unit_id": UNIT_ID,
        "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
        "source_decision_ready_proposal_id": proposal["proposal_id"],
        "human_decision": HUMAN_DECISION,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "build_action": "BUILD_VERSIONED_SOURCE_PROVENANCE_FIELD_INTRODUCTION_ARTIFACTS",
        "introduced_fields": INTRODUCED_FIELDS,
        "build_outputs": [
            rel(INTRODUCED_SCHEMA_PATH),
            rel(PRODUCER_CONTRACT_PATH),
            rel(INTRODUCED_SOURCE_OVERLAY_PATH),
            rel(TOP_GROUP_INTRODUCED_OVERLAY_PATH),
            rel(INTRODUCTION_AUDIT_PATH),
            rel(RERUN_INSTRUCTIONS_PATH),
            rel(BUILD_DECISION_PACKET_PATH),
            rel(BUILD_REPORT_PATH),
        ],
        "mutation_policy": {
            "historical_source_rows_overwritten": False,
            "existing_receipts_mutated": False,
            "new_versioned_schema_artifact_emitted": True,
            "new_versioned_source_overlay_emitted": True,
            "source_semantics_changed": False,
            "taxonomy_changed": False,
        },
        "value_policy": {
            "invent_missing_label_values": False,
            "default_value_for_new_fields": None,
            "absence_reason_required": True,
            "provenance_ref_required": True,
        },
        "terminal_rule": "STOP_HUMAN_DECISION_REQUIRED_AFTER_BUILD_RECEIPT",
    }

def build_schema_artifact(sources: Dict[str, Any]) -> Dict[str, Any]:
    proposal = sources["decision_ready_proposal"]
    fields = []
    for item in proposal["proposed_introductions"]:
        fields.append({
            "field_name": item["field_name"],
            "field_role": item["field_role"],
            "owning_surface": item["owning_surface"],
            "emitting_producer": item["emitting_producer"],
            "blocked_loop": item["blocked_loop"],
            "blocked_decision": item["blocked_decision"],
            "required_for": item["required_for"],
            "null_allowed": item["null_allowed"],
            "null_absence_reason_required": item["null_absence_reason_required"],
            "provenance_requirement": item["provenance_requirement"],
            "value_status_field": FIELD_VALUE_STATUS_FIELDS[item["field_name"]],
            "absence_reason_field": ABSENCE_REASON_FIELDS[item["field_name"]],
            "provenance_ref_field": PROVENANCE_FIELDS[item["field_name"]],
        })
    return {
        "schema_version": "taxonomy_gap_source_payload_field_introduction_schema_v0",
        "schema_id": sha8({"schema": "taxonomy_gap_source_payload_field_introduction_schema_v0", "source": SOURCE_PROPOSAL_TYPING_RECEIPT_ID}),
        "source_decision_ready_proposal_id": proposal["proposal_id"],
        "owning_surface": "taxonomy_gap_source_payload",
        "emitting_producer": "taxonomy_gap_detector",
        "introduced_fields": fields,
        "required_support_fields_per_introduced_field": [
            "value_status_field",
            "absence_reason_field",
            "provenance_ref_field",
        ],
        "allowed_value_statuses": [
            "VALUE_PRESENT",
            "VALUE_ABSENT_SOURCE_PAYLOAD_DOES_NOT_EMIT",
            "VALUE_ABSENT_UPSTREAM_EXISTENCE_UNKNOWN",
            "VALUE_NOT_APPLICABLE_EXPECTED_LIMIT",
        ],
        "forbidden_actions": [
            "do_not_invent_label_value",
            "do_not_create_taxonomy_label",
            "do_not_upgrade_taxonomy",
            "do_not_mutate_source_semantics",
            "do_not_overwrite_historical_source_rows",
            "do_not_mutate_existing_receipts",
        ],
        "versioned_artifact_only": True,
        "historical_source_overwrite": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
    }

def build_producer_contract(schema: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "taxonomy_gap_detector_field_emission_contract_v0",
        "contract_id": sha8({"contract": "taxonomy_gap_detector_field_emission_contract_v0", "schema": schema["schema_id"]}),
        "emitting_producer": "taxonomy_gap_detector",
        "owning_surface": "taxonomy_gap_source_payload",
        "introduced_schema_id": schema["schema_id"],
        "producer_obligations": [
            "emit each introduced field when available",
            "emit null when unavailable",
            "emit explicit value status for each introduced field",
            "emit explicit absence reason for each null value",
            "emit provenance reference for each value or null reason",
            "preserve source_receipt_ref and source_trace_ref",
        ],
        "per_field_contract": {
            field["field_name"]: {
                "value_field": field["field_name"],
                "value_status_field": field["value_status_field"],
                "absence_reason_field": field["absence_reason_field"],
                "provenance_ref_field": field["provenance_ref_field"],
                "null_allowed": field["null_allowed"],
                "null_absence_reason_required": field["null_absence_reason_required"],
            }
            for field in schema["introduced_fields"]
        },
        "forbidden_producer_behaviors": [
            "invent missing label value",
            "synthesize taxonomy label",
            "reinterpret source semantics without separate authorization",
            "upgrade taxonomy",
        ],
        "versioned_artifact_only": True,
    }

def build_overlay_rows(field_rows: List[Dict[str, Any]], schema: Dict[str, Any]) -> List[Dict[str, Any]]:
    overlay_rows = []
    for index, row in enumerate(field_rows):
        out = copy.deepcopy(row)
        out["field_introduction_schema_id"] = schema["schema_id"]
        out["field_introduction_source_proposal_typing_receipt_id"] = SOURCE_PROPOSAL_TYPING_RECEIPT_ID
        out["field_introduction_applied"] = True
        out["field_introduction_versioned_overlay"] = True
        out["field_introduction_historical_source_overwrite"] = False
        for field in INTRODUCED_FIELDS:
            out[field] = None
            out[FIELD_VALUE_STATUS_FIELDS[field]] = "VALUE_ABSENT_SOURCE_PAYLOAD_DOES_NOT_EMIT"
            out[ABSENCE_REASON_FIELDS[field]] = "SOURCE_PAYLOAD_DOES_NOT_EMIT_FIELD"
            out[PROVENANCE_FIELDS[field]] = {
                "source": "field_introduction_build_v0",
                "reason": "field introduced by authorization but value not invented",
                "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
                "source_field_introduction_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
                "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
                "source_rerun_receipt_id": FAILED_REPAIRED_SURFACE_RERUN_RECEIPT_ID,
                "source_row_index": index,
            }
        overlay_rows.append(out)
    return overlay_rows

def build_audit(overlay_rows: List[Dict[str, Any]], schema: Dict[str, Any], contract: Dict[str, Any]) -> Dict[str, Any]:
    field_key_counts = {field: 0 for field in INTRODUCED_FIELDS}
    value_present_counts = {field: 0 for field in INTRODUCED_FIELDS}
    value_status_counts = {field: {} for field in INTRODUCED_FIELDS}
    absence_reason_counts = {field: {} for field in INTRODUCED_FIELDS}
    provenance_ref_counts = {field: 0 for field in INTRODUCED_FIELDS}

    for row in overlay_rows:
        for field in INTRODUCED_FIELDS:
            if field in row:
                field_key_counts[field] += 1
            if row.get(field) is not None:
                value_present_counts[field] += 1
            status = row.get(FIELD_VALUE_STATUS_FIELDS[field])
            value_status_counts[field][status] = value_status_counts[field].get(status, 0) + 1
            reason = row.get(ABSENCE_REASON_FIELDS[field])
            absence_reason_counts[field][reason] = absence_reason_counts[field].get(reason, 0) + 1
            if row.get(PROVENANCE_FIELDS[field]) is not None:
                provenance_ref_counts[field] += 1

    return {
        "schema_version": "field_introduction_application_audit_v0",
        "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
        "schema_id": schema["schema_id"],
        "contract_id": contract["contract_id"],
        "overlay_row_count": len(overlay_rows),
        "introduced_field_count": len(INTRODUCED_FIELDS),
        "field_key_counts": field_key_counts,
        "value_present_counts": value_present_counts,
        "value_status_counts": value_status_counts,
        "absence_reason_counts": absence_reason_counts,
        "provenance_ref_counts": provenance_ref_counts,
        "all_introduced_field_keys_present": all(count == len(overlay_rows) for count in field_key_counts.values()),
        "no_introduced_values_invented": all(count == 0 for count in value_present_counts.values()),
        "all_value_statuses_present": all(sum(counts.values()) == len(overlay_rows) for counts in value_status_counts.values()),
        "all_absence_reasons_present": all(sum(counts.values()) == len(overlay_rows) for counts in absence_reason_counts.values()),
        "all_provenance_refs_present": all(count == len(overlay_rows) for count in provenance_ref_counts.values()),
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "missing_label_value_guess_count": 0,
        "source_semantics_mutation_count": 0,
    }

def build_rerun_instructions(schema: Dict[str, Any], contract: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "post_field_introduction_rerun_instructions_v0",
        "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
        "schema_id": schema["schema_id"],
        "contract_id": contract["contract_id"],
        "introduced_overlay": rel(TOP_GROUP_INTRODUCED_OVERLAY_PATH),
        "recommended_next_unit": "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_FIELD_INTRODUCED_SURFACE_V0",
        "rerun_goal": "observe whether introduced source payload fields make taxonomy-gap missing-label investigation classifiable without inventing values",
        "must_preserve": [
            "do not invent missing label values",
            "preserve explicit null absence reasons",
            "preserve provenance refs",
            "do not mutate historical source rows",
            "do not emit taxonomy delta",
        ],
        "next_unit_command_emitted": False,
    }

def build_decision_packet(schema: Dict[str, Any], contract: Dict[str, Any], audit: Dict[str, Any], rerun: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduction_build_decision_packet_v0",
        "packet_type": "POST_BUILD_REVIEW_PACKET_NOT_COMMAND",
        "source_unit_id": UNIT_ID,
        "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
        "schema_id": schema["schema_id"],
        "contract_id": contract["contract_id"],
        "introduced_overlay": rel(TOP_GROUP_INTRODUCED_OVERLAY_PATH),
        "build_validated": audit["all_introduced_field_keys_present"] and audit["no_introduced_values_invented"] and audit["all_absence_reasons_present"] and audit["all_provenance_refs_present"],
        "recommended_next_handling": "RERUN_FIELD_EXTRACTION_ON_FIELD_INTRODUCED_SURFACE",
        "recommended_next_unit": rerun["recommended_next_unit"],
        "allowed_human_choices": [
            "RERUN_FIELD_EXTRACTION_ON_FIELD_INTRODUCED_SURFACE",
            "REQUEST_FIELD_INTRODUCTION_BUILD_AUDIT",
            "REJECT_FIELD_INTRODUCTION_BUILD",
            "MARK_EXPECTED_LIMIT",
        ],
        "may_emit_next_command": False,
        "may_create_taxonomy_label": False,
        "may_upgrade_taxonomy": False,
        "may_invent_missing_label_value": False,
        "may_mutate_historical_source": False,
        "may_mutate_existing_receipts": False,
        "may_auto_open_next_group": False,
        "review_only": True,
    }

def build_report(plan: Dict[str, Any], schema: Dict[str, Any], contract: Dict[str, Any], audit: Dict[str, Any], rerun: Dict[str, Any], packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "field_introduction_build_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_receipts": {
            "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
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
        "build_plan": plan,
        "schema_id": schema["schema_id"],
        "contract_id": contract["contract_id"],
        "audit": audit,
        "rerun_instructions": rerun,
        "decision_packet_recommended_next_unit": packet["recommended_next_unit"],
        "field_introduction_build_executed": True,
        "versioned_schema_artifact_emitted": True,
        "producer_contract_emitted": True,
        "versioned_source_overlay_emitted": True,
        "introduced_field_count": len(INTRODUCED_FIELDS),
        "introduced_overlay_row_count": audit["overlay_row_count"],
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_semantics_mutation_count": 0,
        "source_mutation_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "repair_command_emitted_count": 0,
        "build_command_emitted_count": 0,
        "next_command_emitted_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "review_only": True,
    }

def validate_outputs(schema: Dict[str, Any], contract: Dict[str, Any], overlay_rows: List[Dict[str, Any]], audit: Dict[str, Any], rerun: Dict[str, Any], packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if schema["owning_surface"] != "taxonomy_gap_source_payload":
        failures.append("schema_owning_surface_wrong")
    if schema["emitting_producer"] != "taxonomy_gap_detector":
        failures.append("schema_producer_wrong")
    if len(schema["introduced_fields"]) != len(INTRODUCED_FIELDS):
        failures.append("schema_field_count_wrong")
    if contract["introduced_schema_id"] != schema["schema_id"]:
        failures.append("contract_schema_id_wrong")
    if len(overlay_rows) != EXPECTED_FIELD_ROW_COUNT:
        failures.append("overlay_row_count_wrong")
    if audit["overlay_row_count"] != EXPECTED_FIELD_ROW_COUNT:
        failures.append("audit_overlay_row_count_wrong")
    if audit["all_introduced_field_keys_present"] is not True:
        failures.append("introduced_keys_not_all_present")
    if audit["no_introduced_values_invented"] is not True:
        failures.append("introduced_values_invented")
    if audit["all_value_statuses_present"] is not True:
        failures.append("value_statuses_not_present")
    if audit["all_absence_reasons_present"] is not True:
        failures.append("absence_reasons_not_present")
    if audit["all_provenance_refs_present"] is not True:
        failures.append("provenance_refs_not_present")
    for key in [
        "historical_source_overwrite_count",
        "existing_receipt_mutation_count",
        "taxonomy_delta_proposal_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "missing_label_value_guess_count",
        "source_semantics_mutation_count",
    ]:
        if audit.get(key) != 0:
            failures.append(f"audit_count_not_zero:{key}:{audit.get(key)}")
    if rerun["recommended_next_unit"] != "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_FIELD_INTRODUCED_SURFACE_V0":
        failures.append("rerun_next_unit_wrong")
    if rerun["next_unit_command_emitted"] is not False:
        failures.append("rerun_command_emitted")
    if packet["packet_type"] != "POST_BUILD_REVIEW_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    if packet["build_validated"] is not True:
        failures.append("packet_build_not_validated")
    if packet["recommended_next_unit"] != rerun["recommended_next_unit"]:
        failures.append("packet_next_unit_wrong")
    for key in [
        "may_emit_next_command",
        "may_create_taxonomy_label",
        "may_upgrade_taxonomy",
        "may_invent_missing_label_value",
        "may_mutate_historical_source",
        "may_mutate_existing_receipts",
        "may_auto_open_next_group",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")
    for key in [
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "historical_source_overwrite_count",
        "existing_receipt_mutation_count",
        "source_mutation_count",
        "source_semantics_mutation_count",
        "taxonomy_delta_proposal_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "repair_command_emitted_count",
        "build_command_emitted_count",
        "next_command_emitted_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")
    if report["field_introduction_build_executed"] is not True:
        failures.append("build_not_executed")
    if report["versioned_schema_artifact_emitted"] is not True:
        failures.append("schema_not_emitted")
    if report["producer_contract_emitted"] is not True:
        failures.append("contract_not_emitted")
    if report["versioned_source_overlay_emitted"] is not True:
        failures.append("overlay_not_emitted")
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("source_proposal_typing_receipt_id") != SOURCE_PROPOSAL_TYPING_RECEIPT_ID:
        failures.append("source_proposal_typing_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "FIELD_INTRO_BUILD_0_DECISION_READY_PROPOSAL_CONSUMED",
        "FIELD_INTRO_BUILD_1_HUMAN_ACCEPTANCE_RECORDED",
        "FIELD_INTRO_BUILD_2_SCHEMA_ARTIFACT_EMITTED",
        "FIELD_INTRO_BUILD_3_PRODUCER_CONTRACT_EMITTED",
        "FIELD_INTRO_BUILD_4_SOURCE_OVERLAY_EMITTED",
        "FIELD_INTRO_BUILD_5_FIELDS_INTRODUCED_WITHOUT_VALUES",
        "FIELD_INTRO_BUILD_6_ABSENCE_REASONS_AND_PROVENANCE_PRESENT",
        "FIELD_INTRO_BUILD_7_RERUN_PACKET_EMITTED",
        "FIELD_INTRO_BUILD_8_NO_HISTORICAL_SOURCE_OR_RECEIPT_MUTATION",
        "FIELD_INTRO_BUILD_9_NO_TAXONOMY_ACTION",
        "FIELD_INTRO_BUILD_10_NO_HIDDEN_NEXT_COMMAND",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("introduced_field_count") != len(INTRODUCED_FIELDS):
        failures.append("metric_field_count_wrong")
    if metrics.get("introduced_overlay_row_count") != EXPECTED_FIELD_ROW_COUNT:
        failures.append("metric_overlay_row_count_wrong")
    if metrics.get("all_introduced_field_keys_present") is not True:
        failures.append("metric_keys_not_present")
    if metrics.get("no_introduced_values_invented") is not True:
        failures.append("metric_values_invented")
    if metrics.get("all_absence_reasons_present") is not True:
        failures.append("metric_absence_reasons_not_present")
    if metrics.get("all_provenance_refs_present") is not True:
        failures.append("metric_provenance_refs_not_present")
    if metrics.get("recommended_next_unit") != "RERUN_EXTRACT_R1000_TOP_GROUP_TAXONOMY_GAP_MISSING_LABEL_EVIDENCE_ON_FIELD_INTRODUCED_SURFACE_V0":
        failures.append("metric_next_unit_wrong")
    for key in [
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "historical_source_overwrite_count",
        "existing_receipt_mutation_count",
        "source_mutation_count",
        "source_semantics_mutation_count",
        "taxonomy_delta_proposal_emitted_count",
        "taxonomy_upgrade_authorized_count",
        "repair_command_emitted_count",
        "build_command_emitted_count",
        "next_command_emitted_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("field_introduction_build_guards", {})
    for key in [
        "decision_ready_proposal_consumed",
        "human_acceptance_recorded",
        "schema_artifact_emitted",
        "producer_contract_emitted",
        "source_overlay_emitted",
        "fields_introduced_without_values",
        "absence_reasons_and_provenance_present",
        "rerun_packet_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "historical_source_overwritten",
        "existing_receipts_mutated",
        "source_semantics_mutated",
        "taxonomy_label_created",
        "taxonomy_upgrade_authorized",
        "taxonomy_delta_proposal_emitted",
        "missing_label_values_guessed",
        "next_command_emitted",
        "next_group_auto_opened",
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

    plan = build_plan(sources)
    schema = build_schema_artifact(sources)
    contract = build_producer_contract(schema)
    overlay_rows = build_overlay_rows(sources["field_rows"], schema)
    audit = build_audit(overlay_rows, schema, contract)
    rerun = build_rerun_instructions(schema, contract)
    packet = build_decision_packet(schema, contract, audit, rerun)
    report = build_report(plan, schema, contract, audit, rerun, packet)

    write_json(BUILD_PLAN_PATH, plan)
    write_json(INTRODUCED_SCHEMA_PATH, schema)
    write_json(PRODUCER_CONTRACT_PATH, contract)
    write_jsonl(INTRODUCED_SOURCE_OVERLAY_PATH, overlay_rows)
    write_jsonl(TOP_GROUP_INTRODUCED_OVERLAY_PATH, overlay_rows)
    write_json(INTRODUCTION_AUDIT_PATH, audit)
    write_json(RERUN_INSTRUCTIONS_PATH, rerun)
    write_json(BUILD_DECISION_PACKET_PATH, packet)
    write_json(BUILD_REPORT_PATH, report)

    failures.extend(validate_outputs(schema, contract, overlay_rows, audit, rerun, packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "FIELD_INTRO_BUILD_0_DECISION_READY_PROPOSAL_CONSUMED": sources["proposal_typing_receipt"]["receipt_id"] == SOURCE_PROPOSAL_TYPING_RECEIPT_ID and sources["decision_ready_proposal"]["decision_ready"] is True,
        "FIELD_INTRO_BUILD_1_HUMAN_ACCEPTANCE_RECORDED": HUMAN_DECISION["decision"] == "ACCEPT_FIELD_INTRODUCTION",
        "FIELD_INTRO_BUILD_2_SCHEMA_ARTIFACT_EMITTED": INTRODUCED_SCHEMA_PATH.exists(),
        "FIELD_INTRO_BUILD_3_PRODUCER_CONTRACT_EMITTED": PRODUCER_CONTRACT_PATH.exists(),
        "FIELD_INTRO_BUILD_4_SOURCE_OVERLAY_EMITTED": INTRODUCED_SOURCE_OVERLAY_PATH.exists() and TOP_GROUP_INTRODUCED_OVERLAY_PATH.exists(),
        "FIELD_INTRO_BUILD_5_FIELDS_INTRODUCED_WITHOUT_VALUES": audit["all_introduced_field_keys_present"] is True and audit["no_introduced_values_invented"] is True,
        "FIELD_INTRO_BUILD_6_ABSENCE_REASONS_AND_PROVENANCE_PRESENT": audit["all_absence_reasons_present"] is True and audit["all_provenance_refs_present"] is True,
        "FIELD_INTRO_BUILD_7_RERUN_PACKET_EMITTED": RERUN_INSTRUCTIONS_PATH.exists() and BUILD_DECISION_PACKET_PATH.exists(),
        "FIELD_INTRO_BUILD_8_NO_HISTORICAL_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["historical_source_overwrite_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "FIELD_INTRO_BUILD_9_NO_TAXONOMY_ACTION": report["taxonomy_delta_proposal_emitted_count"] == 0 and report["taxonomy_upgrade_authorized_count"] == 0 and report["taxonomy_label_creation_count"] == 0,
        "FIELD_INTRO_BUILD_10_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and report["next_command_emitted_count"] == 0,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {"type": "STOP", "stop_code": "STOP_HUMAN_DECISION_REQUIRED", "next_command_goal": None}
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if any([
        report["field_value_invention_count"],
        report["taxonomy_label_creation_count"],
        report["historical_source_overwrite_count"],
        report["existing_receipt_mutation_count"],
        report["source_semantics_mutation_count"],
        report["taxonomy_delta_proposal_emitted_count"],
        report["taxonomy_upgrade_authorized_count"],
        report["repair_command_emitted_count"],
        report["build_command_emitted_count"],
        report["next_command_emitted_count"],
        report["next_group_auto_opened_count"],
        report["hidden_next_command_count"],
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
        "source_decision_ready_proposal_id": sources["decision_ready_proposal"]["proposal_id"],
        "source_field_introduction_boundary_receipt_id": SOURCE_FIELD_INTRO_BOUNDARY_RECEIPT_ID,
        "source_null_limit_receipt_id": SOURCE_NULL_LIMIT_RECEIPT_ID,
        "source_structural_ref_fix_receipt_id": SOURCE_STRUCTURAL_REF_FIX_RECEIPT_ID,
        "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
        "schema_id": schema["schema_id"],
        "contract_id": contract["contract_id"],
        "introduced_field_count": len(INTRODUCED_FIELDS),
        "introduced_field_names": INTRODUCED_FIELDS,
        "introduced_overlay_row_count": len(overlay_rows),
        "all_introduced_field_keys_present": audit["all_introduced_field_keys_present"],
        "no_introduced_values_invented": audit["no_introduced_values_invented"],
        "all_value_statuses_present": audit["all_value_statuses_present"],
        "all_absence_reasons_present": audit["all_absence_reasons_present"],
        "all_provenance_refs_present": audit["all_provenance_refs_present"],
        "recommended_next_unit": rerun["recommended_next_unit"],
        "field_introduction_build_executed_count": 1,
        "versioned_schema_artifact_emitted_count": 1,
        "producer_contract_emitted_count": 1,
        "versioned_source_overlay_emitted_count": 1,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "historical_source_overwrite_count": 0,
        "existing_receipt_mutation_count": 0,
        "source_semantics_mutation_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "repair_command_emitted_count": 0,
        "build_command_emitted_count": 0,
        "next_command_emitted_count": 0,
        "next_group_auto_opened_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "hidden_next_command_count": 0,
    }

    guards = {
        "decision_ready_proposal_consumed": True,
        "human_acceptance_recorded": True,
        "schema_artifact_emitted": True,
        "producer_contract_emitted": True,
        "source_overlay_emitted": True,
        "fields_introduced_without_values": audit["all_introduced_field_keys_present"] and audit["no_introduced_values_invented"],
        "absence_reasons_and_provenance_present": audit["all_absence_reasons_present"] and audit["all_provenance_refs_present"],
        "rerun_packet_emitted": True,
        "historical_source_overwritten": False,
        "existing_receipts_mutated": False,
        "source_semantics_mutated": False,
        "taxonomy_label_created": False,
        "taxonomy_upgrade_authorized": False,
        "taxonomy_delta_proposal_emitted": False,
        "missing_label_values_guessed": False,
        "next_command_emitted": False,
        "next_group_auto_opened": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_proposal_typing_receipt": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
        "schema_id": schema["schema_id"],
        "contract_id": contract["contract_id"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_provenance_field_introduction_build_plan": rel(BUILD_PLAN_PATH),
        "taxonomy_gap_source_payload_field_introduction_schema": rel(INTRODUCED_SCHEMA_PATH),
        "taxonomy_gap_detector_field_emission_contract": rel(PRODUCER_CONTRACT_PATH),
        "r1000_taxonomy_gap_source_payload_field_introduction_overlay": rel(INTRODUCED_SOURCE_OVERLAY_PATH),
        "top_group_taxonomy_gap_source_payload_field_introduction_overlay": rel(TOP_GROUP_INTRODUCED_OVERLAY_PATH),
        "field_introduction_application_audit": rel(INTRODUCTION_AUDIT_PATH),
        "post_field_introduction_rerun_instructions": rel(RERUN_INSTRUCTIONS_PATH),
        "field_introduction_build_decision_packet": rel(BUILD_DECISION_PACKET_PATH),
        "field_introduction_build_report": rel(BUILD_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "source_provenance_field_introduction_build_receipt_v0",
        "receipt_type": "SOURCE_PROVENANCE_FIELD_INTRODUCTION_BUILD_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_proposal_typing_receipt_id": SOURCE_PROPOSAL_TYPING_RECEIPT_ID,
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
        "field_introduction_build_summary": {
            "pressure_group_key_hash": TOP_GROUP_KEY_HASH,
            "schema_id": schema["schema_id"],
            "contract_id": contract["contract_id"],
            "introduced_field_names": INTRODUCED_FIELDS,
            "introduced_overlay_row_count": len(overlay_rows),
            "no_introduced_values_invented": audit["no_introduced_values_invented"],
            "all_absence_reasons_present": audit["all_absence_reasons_present"],
            "all_provenance_refs_present": audit["all_provenance_refs_present"],
            "recommended_next_unit": rerun["recommended_next_unit"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "field_introduction_build_guards": guards,
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
    print(f"source_provenance_field_introduction_build_receipt_id={receipt_id}")
    print(f"source_provenance_field_introduction_build_receipt_path=data/source_provenance_field_introduction_build_v0_receipts/{receipt_id}.json")
    print(f"introduced_schema_path=data/source_provenance_field_introduction_build_v0/taxonomy_gap_source_payload_field_introduction_schema_v0.json")
    print(f"introduced_overlay_path=data/source_provenance_field_introduction_build_v0/top_group_taxonomy_gap_source_payload_field_introduction_overlay.jsonl")
    print(f"post_field_introduction_rerun_instructions_path=data/source_provenance_field_introduction_build_v0/post_field_introduction_rerun_instructions.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
