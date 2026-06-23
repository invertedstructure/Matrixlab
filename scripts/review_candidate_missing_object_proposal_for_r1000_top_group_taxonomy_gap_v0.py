#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_CANDIDATE_MISSING_OBJECT_PROPOSAL_FOR_R1000_TOP_GROUP_TAXONOMY_GAP_V0"
TARGET_UNIT_ID = "candidate_missing_object_proposal_review.r1000_top_group_taxonomy_gap.v0"

SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID = "aa01c2a9"
SOURCE_PROPOSAL_LAYER_RECEIPT_ID = "6003c89c"
SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID = "087bf971"
SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID = "11d585b6"
SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID = "5b841942"
SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID = "e3371951"

OUT_DIR = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0"
RECEIPT_DIR = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0_receipts"

REVIEW_DECISION_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_candidate_proposal_review_decision.json"
REVIEW_FINDINGS_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_candidate_proposal_review_findings.json"
APPLICATION_AUTHORIZATION_PACKET_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_candidate_proposal_application_authorization_packet.json"
REVIEW_TRANSITION_TRACE_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_candidate_proposal_review_transition_trace.json"
REVIEW_REPORT_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_candidate_proposal_review_report.json"

PROPOSAL_APPLICATION_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID}.json"
CANDIDATE_PROPOSAL_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_candidate_missing_object_proposal.json"
TYPED_DECISION_FIELDS_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_typed_unresolved_decision_fields.jsonl"
PROPOSAL_EVIDENCE_REFS_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_proposal_evidence_refs.json"
HUMAN_SCHEMA_DECISION_PACKET_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_human_schema_decision_packet.json"
PROPOSAL_TRANSITION_TRACE_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_proposal_transition_trace.json"
PROPOSAL_APPLICATION_REPORT_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_proposal_application_report.json"

PROPOSAL_LAYER_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0_receipts" / f"{SOURCE_PROPOSAL_LAYER_RECEIPT_ID}.json"
PROPOSAL_LAYER_CONTRACT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_missing_object_proposal_layer_contract.json"
PROPOSAL_OBJECT_SCHEMA_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_missing_object_proposal_object_schema.json"
TYPED_DECISION_FIELD_SCHEMA_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "typed_unresolved_decision_field_schema.json"
PROPOSAL_REVIEW_DECISION_SCHEMA_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_proposal_review_decision_schema.json"
PROPOSAL_REJECTION_TAXONOMY_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_proposal_rejection_taxonomy.json"
PROPOSAL_APPLICATION_CONTRACT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_proposal_application_contract.json"

QUEUE_RECONCILIATION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"

EXPECTED_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_RECEIPT_ID}.json"
EXPECTED_LIMIT_MARKER_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0" / "expected_source_content_limit_marker.json"
EXPECTED_LIMIT_CLOSURE_RECORD_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0" / "expected_source_content_limit_closure_record.json"

FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_null_evidence_limit_classification_v0_receipts" / f"{SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID}.json"
FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH = ROOT / "data" / "field_introduction_proposal_typing_refinement_v0_receipts" / f"{SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID}.json"

CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID}.json"
CURRENT_SURFACE_PROTOCOL_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "current_surface_pressure_loop_protocol.json"

SOURCE_FILES = [
    PROPOSAL_APPLICATION_RECEIPT_PATH,
    CANDIDATE_PROPOSAL_PATH,
    TYPED_DECISION_FIELDS_PATH,
    PROPOSAL_EVIDENCE_REFS_PATH,
    HUMAN_SCHEMA_DECISION_PACKET_PATH,
    PROPOSAL_TRANSITION_TRACE_PATH,
    PROPOSAL_APPLICATION_REPORT_PATH,
    PROPOSAL_LAYER_RECEIPT_PATH,
    PROPOSAL_LAYER_CONTRACT_PATH,
    PROPOSAL_OBJECT_SCHEMA_PATH,
    TYPED_DECISION_FIELD_SCHEMA_PATH,
    PROPOSAL_REVIEW_DECISION_SCHEMA_PATH,
    PROPOSAL_REJECTION_TAXONOMY_PATH,
    PROPOSAL_APPLICATION_CONTRACT_PATH,
    QUEUE_RECONCILIATION_RECEIPT_PATH,
    EXPECTED_LIMIT_RECEIPT_PATH,
    EXPECTED_LIMIT_MARKER_PATH,
    EXPECTED_LIMIT_CLOSURE_RECORD_PATH,
    FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH,
    FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH,
    CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH,
    CURRENT_SURFACE_PROTOCOL_PATH,
]

REQUIRED_DESCRIPTOR_FIELDS = [
    "missing_label_identifier",
    "taxonomy_context_ref",
    "current_label_space_ref",
    "expected_label_space_ref",
]

EXPECTED_CANDIDATE_ID = "ce1fe7fc"

HUMAN_DECISION = {
    "decision": "REVIEW_CANDIDATE_MISSING_OBJECT_PROPOSAL_FOR_R1000_TOP_GROUP_TAXONOMY_GAP",
    "scope": "review the candidate missing-object proposal as a schema/object-shape decision; if valid, accept it for a later separate application unit without applying it here",
    "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
    "candidate_object_id": EXPECTED_CANDIDATE_ID,
    "authorized": [
        "read candidate missing-object proposal",
        "validate candidate object shape",
        "validate typed unresolved decision fields",
        "validate evidence refs",
        "validate no forbidden assumptions",
        "emit review decision",
        "authorize only a later separate application unit if accepted",
    ],
    "not_authorized": [
        "applying the proposal in this unit",
        "filling missing descriptor fields",
        "inventing values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "mutating source rows",
        "mutating existing receipts",
        "running R1000",
        "opening another pressure group",
        "hiding next command",
    ],
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
    return path.relative_to(ROOT).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    rows: List[Dict[str, Any]] = []
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
        "proposal_application_receipt": read_json(PROPOSAL_APPLICATION_RECEIPT_PATH),
        "candidate_proposal": read_json(CANDIDATE_PROPOSAL_PATH),
        "typed_decision_fields": read_jsonl(TYPED_DECISION_FIELDS_PATH),
        "proposal_evidence_refs": read_json(PROPOSAL_EVIDENCE_REFS_PATH),
        "human_schema_decision_packet": read_json(HUMAN_SCHEMA_DECISION_PACKET_PATH),
        "proposal_transition_trace": read_json(PROPOSAL_TRANSITION_TRACE_PATH),
        "proposal_application_report": read_json(PROPOSAL_APPLICATION_REPORT_PATH),
        "proposal_layer_receipt": read_json(PROPOSAL_LAYER_RECEIPT_PATH),
        "proposal_layer_contract": read_json(PROPOSAL_LAYER_CONTRACT_PATH),
        "proposal_object_schema": read_json(PROPOSAL_OBJECT_SCHEMA_PATH),
        "typed_decision_field_schema": read_json(TYPED_DECISION_FIELD_SCHEMA_PATH),
        "proposal_review_decision_schema": read_json(PROPOSAL_REVIEW_DECISION_SCHEMA_PATH),
        "proposal_rejection_taxonomy": read_json(PROPOSAL_REJECTION_TAXONOMY_PATH),
        "proposal_application_contract": read_json(PROPOSAL_APPLICATION_CONTRACT_PATH),
        "queue_reconciliation_receipt": read_json(QUEUE_RECONCILIATION_RECEIPT_PATH),
        "expected_limit_receipt": read_json(EXPECTED_LIMIT_RECEIPT_PATH),
        "expected_limit_marker": read_json(EXPECTED_LIMIT_MARKER_PATH),
        "expected_limit_closure_record": read_json(EXPECTED_LIMIT_CLOSURE_RECORD_PATH),
        "field_introduced_null_limit_receipt": read_json(FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH),
        "field_introduction_proposal_receipt": read_json(FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH),
        "current_surface_protocol_receipt": read_json(CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH),
        "current_surface_protocol": read_json(CURRENT_SURFACE_PROTOCOL_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    app_receipt = sources["proposal_application_receipt"]
    candidate = sources["candidate_proposal"]
    layer_receipt = sources["proposal_layer_receipt"]

    if app_receipt.get("receipt_id") != SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID:
        failures.append("proposal_application_receipt_id_wrong")
    if app_receipt.get("gate") != "PASS":
        failures.append("proposal_application_not_pass")
    if app_receipt.get("aggregate_metrics", {}).get("candidate_object_id") != EXPECTED_CANDIDATE_ID:
        failures.append("candidate_object_id_wrong_in_application_receipt")
    if app_receipt.get("aggregate_metrics", {}).get("candidate_proposal_instance_emitted_count") != 1:
        failures.append("candidate_proposal_instance_missing")
    if app_receipt.get("aggregate_metrics", {}).get("proposal_applied_count") != 0:
        failures.append("proposal_already_applied_before_review")
    if app_receipt.get("aggregate_metrics", {}).get("application_authorized_count") != 0:
        failures.append("application_already_authorized_before_review")
    if app_receipt.get("terminal", {}).get("stop_code") != "STOP_HUMAN_SCHEMA_DECISION_REQUIRED":
        failures.append("proposal_application_not_waiting_for_human_schema_decision")

    if candidate.get("candidate_object_id") != EXPECTED_CANDIDATE_ID:
        failures.append("candidate_object_id_wrong")
    if candidate.get("object_status") != "CANDIDATE_MISSING_OBJECT_PROPOSAL":
        failures.append("candidate_status_wrong")
    if candidate.get("application_authorized") is not False:
        failures.append("candidate_self_authorizes_application")
    if candidate.get("required_object_fields") != REQUIRED_DESCRIPTOR_FIELDS:
        failures.append("candidate_required_fields_wrong")

    if layer_receipt.get("receipt_id") != SOURCE_PROPOSAL_LAYER_RECEIPT_ID:
        failures.append("proposal_layer_receipt_id_wrong")
    if layer_receipt.get("gate") != "PASS":
        failures.append("proposal_layer_not_pass")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def proposal_shape_findings(candidate: Dict[str, Any], typed_fields: List[Dict[str, Any]], evidence_refs: Dict[str, Any], decision_packet: Dict[str, Any]) -> Dict[str, Any]:
    required_keys = [
        "candidate_object_id",
        "object_status",
        "missing_object_type",
        "target_field_or_surface",
        "source_pressure_group",
        "source_evidence_refs",
        "why_current_layer_stopped",
        "what_object_is_missing",
        "required_object_fields",
        "known_fields",
        "unknown_required_decision_fields",
        "proposal_basis",
        "candidate_payload",
        "application_authorized",
        "required_human_schema_decision",
        "forbidden_assumptions",
        "expected_application_effect",
        "rerun_review_rule",
    ]

    missing_required_keys = [key for key in required_keys if key not in candidate]
    unknown_fields = candidate.get("unknown_required_decision_fields", [])
    field_names = [field.get("field") for field in typed_fields]

    findings = {
        "schema_version": "candidate_missing_object_proposal_review_findings_v0",
        "candidate_object_id": candidate.get("candidate_object_id"),
        "required_keys_present": len(missing_required_keys) == 0,
        "missing_required_keys": missing_required_keys,
        "candidate_status_valid": candidate.get("object_status") == "CANDIDATE_MISSING_OBJECT_PROPOSAL",
        "missing_object_type_valid": candidate.get("missing_object_type") == "taxonomy_gap_evidence_surface_descriptor",
        "target_surface_valid": candidate.get("target_field_or_surface") == "field_introduced_taxonomy_gap_evidence_surface",
        "required_descriptor_fields_valid": candidate.get("required_object_fields") == REQUIRED_DESCRIPTOR_FIELDS,
        "typed_decision_field_count_valid": len(typed_fields) == len(REQUIRED_DESCRIPTOR_FIELDS) and len(unknown_fields) == len(REQUIRED_DESCRIPTOR_FIELDS),
        "typed_decision_fields_match_required_fields": sorted(field_names) == sorted(REQUIRED_DESCRIPTOR_FIELDS),
        "typed_decision_fields_have_required_state": all(field.get("value_state") == "REQUIRES_SCHEMA_DECISION" for field in typed_fields),
        "typed_decision_fields_forbid_null": all("set_null_as_value" in field.get("forbidden_resolution", []) for field in typed_fields),
        "typed_decision_fields_forbid_invention": all("invent_value_without_source" in field.get("forbidden_resolution", []) for field in typed_fields),
        "evidence_refs_present": len(evidence_refs.get("evidence_refs", [])) >= 4,
        "decision_packet_present": decision_packet.get("decision_required") is True,
        "candidate_does_not_self_authorize": candidate.get("application_authorized") is False,
        "forbidden_assumptions_present": False,
        "review_result": None,
        "typed_rejection_codes": [],
    }

    candidate_text = json.dumps(candidate, sort_keys=True)
    forbidden_literals = [
        '"missing_label_identifier": null',
        '"taxonomy_context_ref": null',
        '"current_label_space_ref": null',
        '"expected_label_space_ref": null',
    ]
    findings["untyped_null_literals_present"] = [literal for literal in forbidden_literals if literal in candidate_text]
    findings["untyped_null_literal_count"] = len(findings["untyped_null_literals_present"])

    checks = [
        findings["required_keys_present"],
        findings["candidate_status_valid"],
        findings["missing_object_type_valid"],
        findings["target_surface_valid"],
        findings["required_descriptor_fields_valid"],
        findings["typed_decision_field_count_valid"],
        findings["typed_decision_fields_match_required_fields"],
        findings["typed_decision_fields_have_required_state"],
        findings["typed_decision_fields_forbid_null"],
        findings["typed_decision_fields_forbid_invention"],
        findings["evidence_refs_present"],
        findings["decision_packet_present"],
        findings["candidate_does_not_self_authorize"],
        findings["untyped_null_literal_count"] == 0,
    ]

    if all(checks):
        findings["review_result"] = "ACCEPT_CANDIDATE_OBJECT_FOR_SEPARATE_APPLICATION"
        findings["typed_rejection_codes"] = []
    else:
        findings["review_result"] = "REJECT_CANDIDATE_OBJECT"
        rejection_codes = []
        if not findings["target_surface_valid"]:
            rejection_codes.append("WRONG_TARGET_FIELD")
        if not findings["missing_object_type_valid"]:
            rejection_codes.append("WRONG_MISSING_OBJECT_TYPE")
        if not findings["evidence_refs_present"]:
            rejection_codes.append("WRONG_EVIDENCE_BASIS")
        if not findings["required_descriptor_fields_valid"]:
            rejection_codes.append("WRONG_PROPOSED_SCHEMA_FIELD")
        if not findings["candidate_does_not_self_authorize"] or findings["untyped_null_literal_count"] > 0:
            rejection_codes.append("FORBIDDEN_ASSUMPTION_PRESENT")
        if not rejection_codes:
            rejection_codes.append("WRONG_EVIDENCE_BASIS")
        findings["typed_rejection_codes"] = rejection_codes

    return findings

def build_review_decision(candidate: Dict[str, Any], findings: Dict[str, Any]) -> Dict[str, Any]:
    accepted = findings["review_result"] == "ACCEPT_CANDIDATE_OBJECT_FOR_SEPARATE_APPLICATION"
    return {
        "schema_version": "candidate_proposal_review_decision_v0",
        "review_decision_id": sha8({
            "candidate_object_id": candidate["candidate_object_id"],
            "review_result": findings["review_result"],
            "source_application_receipt": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        }),
        "candidate_object_id": candidate["candidate_object_id"],
        "candidate_object_ref": rel(CANDIDATE_PROPOSAL_PATH),
        "decision_status": "ACCEPT_CANDIDATE_OBJECT" if accepted else "REJECT_CANDIDATE_OBJECT",
        "decision_basis": {
            "review_result": findings["review_result"],
            "required_keys_present": findings["required_keys_present"],
            "typed_decision_fields_valid": findings["typed_decision_field_count_valid"] and findings["typed_decision_fields_have_required_state"],
            "evidence_refs_present": findings["evidence_refs_present"],
            "candidate_does_not_self_authorize": findings["candidate_does_not_self_authorize"],
            "untyped_null_literal_count": findings["untyped_null_literal_count"],
        },
        "typed_rejection_codes": findings["typed_rejection_codes"],
        "accepted_application_scope": {
            "application_scope_status": "AUTHORIZED_FOR_SEPARATE_APPLICATION_UNIT" if accepted else "NOT_AUTHORIZED",
            "authorized_application_unit": "APPLY_ACCEPTED_CANDIDATE_MISSING_OBJECT_PROPOSAL_TO_R1000_TOP_GROUP_TAXONOMY_GAP_EVIDENCE_SURFACE_V0" if accepted else None,
            "candidate_object_id": candidate["candidate_object_id"],
            "allowed_effect": "materialize typed unresolved descriptor object; do not invent descriptor values",
        },
        "schema_delta_if_any": None,
        "rerun_review_required": True if accepted else False,
        "application_authorized_for_separate_unit": accepted,
        "application_authorized_in_this_unit": False,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_REVIEW_DECISION_EMITTED_APPLICATION_REQUIRES_SEPARATE_UNIT" if accepted else "STOP_CANDIDATE_OBJECT_REJECTED",
            "next_command_goal": None,
        },
    }

def build_authorization_packet(review_decision: Dict[str, Any]) -> Dict[str, Any]:
    accepted = review_decision["decision_status"] == "ACCEPT_CANDIDATE_OBJECT"
    return {
        "schema_version": "accepted_candidate_missing_object_proposal_application_authorization_packet_v0",
        "authorization_packet_id": sha8({
            "review_decision_id": review_decision["review_decision_id"],
            "candidate_object_id": review_decision["candidate_object_id"],
        }),
        "candidate_object_id": review_decision["candidate_object_id"],
        "review_decision_id": review_decision["review_decision_id"],
        "review_decision_ref": rel(REVIEW_DECISION_PATH),
        "application_authorized_for_separate_unit": accepted,
        "application_authorized_in_this_unit": False,
        "authorized_application_unit": review_decision["accepted_application_scope"]["authorized_application_unit"],
        "authorized_effect": [
            "materialize typed unresolved descriptor object",
            "preserve missing descriptor fields as typed decision fields",
            "emit accepted application receipt",
            "rerun/review affected evidence surface",
        ] if accepted else [],
        "still_forbidden": [
            "inventing missing_label_identifier",
            "inventing taxonomy_context_ref",
            "inventing current_label_space_ref",
            "inventing expected_label_space_ref",
            "creating taxonomy label without separate taxonomy authorization",
            "mutating source rows",
            "mutating existing receipts",
            "running R1000 in review unit",
            "opening another pressure group in review unit",
        ],
    }

def build_transition_trace(review_decision: Dict[str, Any], findings: Dict[str, Any]) -> Dict[str, Any]:
    accepted = review_decision["decision_status"] == "ACCEPT_CANDIDATE_OBJECT"
    return {
        "schema_version": "candidate_missing_object_proposal_review_transition_trace_v0",
        "candidate_object_id": review_decision["candidate_object_id"],
        "trace": [
            {
                "step": "consume_candidate_proposal",
                "question": "candidate_status_is_reviewable",
                "answer": findings["candidate_status_valid"],
                "taken": "inspect_candidate_shape" if findings["candidate_status_valid"] else "STOP_CANDIDATE_NOT_REVIEWABLE",
            },
            {
                "step": "inspect_candidate_shape",
                "question": "required_shape_and_fields_are_valid",
                "answer": findings["required_keys_present"] and findings["required_descriptor_fields_valid"],
                "taken": "inspect_decision_fields" if findings["required_keys_present"] and findings["required_descriptor_fields_valid"] else "REJECT_CANDIDATE_OBJECT",
            },
            {
                "step": "inspect_decision_fields",
                "question": "unknown_fields_are_typed_not_null",
                "answer": findings["typed_decision_fields_have_required_state"] and findings["untyped_null_literal_count"] == 0,
                "taken": "inspect_evidence_refs" if findings["typed_decision_fields_have_required_state"] and findings["untyped_null_literal_count"] == 0 else "REJECT_CANDIDATE_OBJECT",
            },
            {
                "step": "inspect_evidence_refs",
                "question": "evidence_refs_are_sufficient_for_candidate_shape",
                "answer": findings["evidence_refs_present"],
                "taken": "emit_review_decision" if findings["evidence_refs_present"] else "REJECT_CANDIDATE_OBJECT",
            },
            {
                "step": "emit_review_decision",
                "question": "application_happens_in_this_unit",
                "answer": False,
                "taken": "STOP_REVIEW_DECISION_EMITTED_APPLICATION_REQUIRES_SEPARATE_UNIT" if accepted else "STOP_CANDIDATE_OBJECT_REJECTED",
            },
        ],
        "terminal": review_decision["terminal"],
    }

def build_report(review_decision: Dict[str, Any], findings: Dict[str, Any]) -> Dict[str, Any]:
    accepted = review_decision["decision_status"] == "ACCEPT_CANDIDATE_OBJECT"
    return {
        "schema_version": "candidate_missing_object_proposal_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "candidate_object_id": review_decision["candidate_object_id"],
        "candidate_reviewed_count": 1,
        "review_decision_emitted_count": 1,
        "review_decision_status": review_decision["decision_status"],
        "accepted_candidate_object_count": 1 if accepted else 0,
        "rejected_candidate_object_count": 0 if accepted else 1,
        "typed_rejection_code_count": len(review_decision["typed_rejection_codes"]),
        "application_authorized_for_separate_unit_count": 1 if accepted else 0,
        "application_authorized_in_this_unit_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "null_field_value_emitted_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "r1000_run_executed_count": 0,
        "pressure_group_opened_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": "APPLY_ACCEPTED_CANDIDATE_MISSING_OBJECT_PROPOSAL_TO_R1000_TOP_GROUP_TAXONOMY_GAP_EVIDENCE_SURFACE_V0" if accepted else "REFINE_OR_REJECT_CANDIDATE_MISSING_OBJECT_PROPOSAL_FOR_R1000_TOP_GROUP_TAXONOMY_GAP_V0",
    }

def validate_review_outputs(review_decision: Dict[str, Any], findings: Dict[str, Any], authorization_packet: Dict[str, Any], trace: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if report["candidate_reviewed_count"] != 1:
        failures.append("candidate_reviewed_count_wrong")
    if report["review_decision_emitted_count"] != 1:
        failures.append("review_decision_emitted_count_wrong")
    if review_decision["candidate_object_id"] != EXPECTED_CANDIDATE_ID:
        failures.append("review_candidate_id_wrong")
    if review_decision["decision_status"] != "ACCEPT_CANDIDATE_OBJECT":
        failures.append(f"review_decision_status_not_accept:{review_decision['decision_status']}")
    if report["accepted_candidate_object_count"] != 1:
        failures.append("accepted_candidate_object_count_wrong")
    if report["rejected_candidate_object_count"] != 0:
        failures.append("rejected_candidate_object_count_wrong")
    if review_decision["typed_rejection_codes"] != []:
        failures.append("accepted_review_has_rejection_codes")
    if review_decision["application_authorized_for_separate_unit"] is not True:
        failures.append("separate_application_not_authorized")
    if review_decision["application_authorized_in_this_unit"] is not False:
        failures.append("review_authorizes_application_in_this_unit")
    if authorization_packet["application_authorized_for_separate_unit"] is not True:
        failures.append("authorization_packet_not_separate_authorized")
    if authorization_packet["application_authorized_in_this_unit"] is not False:
        failures.append("authorization_packet_authorizes_current_unit")
    if not authorization_packet["authorized_application_unit"]:
        failures.append("authorized_application_unit_missing")
    if trace["terminal"]["next_command_goal"] is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "application_authorized_in_this_unit_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "null_field_value_emitted_count",
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "r1000_run_executed_count",
        "pressure_group_opened_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")

    for gate, ok in receipt.get("acceptance_gate_results", {}).items():
        if ok is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{ok}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("candidate_reviewed_count") != 1:
        failures.append(f"metric_candidate_reviewed_wrong:{metrics.get('candidate_reviewed_count')}")
    if metrics.get("review_decision_status") != "ACCEPT_CANDIDATE_OBJECT":
        failures.append(f"metric_review_status_wrong:{metrics.get('review_decision_status')}")
    if metrics.get("application_authorized_for_separate_unit_count") != 1:
        failures.append(f"metric_separate_application_auth_wrong:{metrics.get('application_authorized_for_separate_unit_count')}")
    for key in [
        "application_authorized_in_this_unit_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "null_field_value_emitted_count",
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "r1000_run_executed_count",
        "pressure_group_opened_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_REVIEW_DECISION_EMITTED_APPLICATION_REQUIRES_SEPARATE_UNIT":
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

    candidate = sources["candidate_proposal"]
    typed_fields = sources["typed_decision_fields"]
    evidence_refs = sources["proposal_evidence_refs"]
    decision_packet = sources["human_schema_decision_packet"]

    findings = proposal_shape_findings(candidate, typed_fields, evidence_refs, decision_packet)
    review_decision = build_review_decision(candidate, findings)
    authorization_packet = build_authorization_packet(review_decision)
    trace = build_transition_trace(review_decision, findings)
    report = build_report(review_decision, findings)

    write_json(REVIEW_FINDINGS_PATH, findings)
    write_json(REVIEW_DECISION_PATH, review_decision)
    write_json(APPLICATION_AUTHORIZATION_PACKET_PATH, authorization_packet)
    write_json(REVIEW_TRANSITION_TRACE_PATH, trace)
    write_json(REVIEW_REPORT_PATH, report)

    failures.extend(validate_review_outputs(review_decision, findings, authorization_packet, trace, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "PROPOSAL_REVIEW_0_CANDIDATE_CONSUMED": candidate.get("candidate_object_id") == EXPECTED_CANDIDATE_ID,
        "PROPOSAL_REVIEW_1_CANDIDATE_SHAPE_VALIDATED": findings["required_keys_present"] and findings["candidate_status_valid"] and findings["missing_object_type_valid"],
        "PROPOSAL_REVIEW_2_TYPED_DECISION_FIELDS_VALIDATED": findings["typed_decision_field_count_valid"] and findings["typed_decision_fields_have_required_state"],
        "PROPOSAL_REVIEW_3_EVIDENCE_REFS_VALIDATED": findings["evidence_refs_present"],
        "PROPOSAL_REVIEW_4_NO_UNTYPED_NULLS_OR_VALUE_INVENTION": findings["untyped_null_literal_count"] == 0 and report["field_value_invention_count"] == 0,
        "PROPOSAL_REVIEW_5_REVIEW_DECISION_EMITTED": REVIEW_DECISION_PATH.exists() and report["review_decision_emitted_count"] == 1,
        "PROPOSAL_REVIEW_6_ACCEPTED_FOR_SEPARATE_APPLICATION_ONLY": review_decision["decision_status"] == "ACCEPT_CANDIDATE_OBJECT" and review_decision["application_authorized_for_separate_unit"] is True and review_decision["application_authorized_in_this_unit"] is False,
        "PROPOSAL_REVIEW_7_NO_PROPOSAL_APPLIED": report["proposal_applied_count"] == 0,
        "PROPOSAL_REVIEW_8_NO_TARGET_FIELD_FILLED": report["target_field_filled_count"] == 0,
        "PROPOSAL_REVIEW_9_NO_TAXONOMY_ACTION": report["taxonomy_label_creation_count"] == 0 and report["taxonomy_upgrade_authorized_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "PROPOSAL_REVIEW_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "PROPOSAL_REVIEW_11_NO_R1000_RUN_OR_GROUP_OPEN": report["r1000_run_executed_count"] == 0 and report["pressure_group_opened_count"] == 0 and report["next_group_auto_opened_count"] == 0,
        "PROPOSAL_REVIEW_12_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and review_decision["terminal"]["next_command_goal"] is None,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_REVIEW_DECISION_EMITTED_APPLICATION_REQUIRES_SEPARATE_UNIT",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_field_introduced_null_limit_receipt_id": SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID,
        "source_field_introduction_proposal_receipt_id": SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "candidate_object_id": candidate["candidate_object_id"],
        "candidate_reviewed_count": 1,
        "review_decision_emitted_count": 1,
        "review_decision_status": review_decision["decision_status"],
        "accepted_candidate_object_count": report["accepted_candidate_object_count"],
        "rejected_candidate_object_count": report["rejected_candidate_object_count"],
        "typed_rejection_code_count": report["typed_rejection_code_count"],
        "application_authorized_for_separate_unit_count": report["application_authorized_for_separate_unit_count"],
        "application_authorized_in_this_unit_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "null_field_value_emitted_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "r1000_run_executed_count": 0,
        "pressure_group_opened_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "authorized_application_unit": authorization_packet["authorized_application_unit"],
        "recommended_next_handling": report["recommended_next_handling"],
    }

    guards = {
        "candidate_consumed": True,
        "candidate_shape_validated": findings["review_result"] == "ACCEPT_CANDIDATE_OBJECT_FOR_SEPARATE_APPLICATION",
        "review_decision_emitted": True,
        "accepted_for_separate_application_only": review_decision["application_authorized_for_separate_unit"] is True and review_decision["application_authorized_in_this_unit"] is False,
        "proposal_applied": False,
        "target_field_filled": False,
        "null_field_value_emitted": False,
        "values_invented": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "r1000_run_executed": False,
        "pressure_group_opened": False,
        "next_group_auto_opened": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_proposal_application": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "candidate_object_id": candidate["candidate_object_id"],
        "review_decision": review_decision["decision_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "review_findings": rel(REVIEW_FINDINGS_PATH),
        "review_decision": rel(REVIEW_DECISION_PATH),
        "application_authorization_packet": rel(APPLICATION_AUTHORIZATION_PACKET_PATH),
        "review_transition_trace": rel(REVIEW_TRANSITION_TRACE_PATH),
        "review_report": rel(REVIEW_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "candidate_missing_object_proposal_review_r1000_taxonomy_gap_receipt_v0",
        "receipt_type": "CANDIDATE_MISSING_OBJECT_PROPOSAL_REVIEW_R1000_TAXONOMY_GAP_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_field_introduced_null_limit_receipt_id": SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID,
        "source_field_introduction_proposal_receipt_id": SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "candidate_missing_object_proposal_review_summary": {
            "candidate_object_id": candidate["candidate_object_id"],
            "review_decision_status": review_decision["decision_status"],
            "review_result": findings["review_result"],
            "accepted_candidate_object_count": report["accepted_candidate_object_count"],
            "application_authorized_for_separate_unit": review_decision["application_authorized_for_separate_unit"],
            "application_authorized_in_this_unit": False,
            "authorized_application_unit": authorization_packet["authorized_application_unit"],
            "proposal_applied": False,
            "required_descriptor_fields": REQUIRED_DESCRIPTOR_FIELDS,
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "candidate_missing_object_proposal_review_guards": guards,
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
    print(f"candidate_missing_object_proposal_review_receipt_id={receipt_id}")
    print(f"candidate_missing_object_proposal_review_receipt_path=data/candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0_receipts/{receipt_id}.json")
    print(f"candidate_missing_object_proposal_review_decision_path=data/candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0/r1000_top_group_taxonomy_gap_candidate_proposal_review_decision.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
