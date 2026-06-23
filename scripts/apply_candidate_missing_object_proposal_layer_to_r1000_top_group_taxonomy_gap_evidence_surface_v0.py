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

UNIT_ID = "APPLY_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_TO_R1000_TOP_GROUP_TAXONOMY_GAP_EVIDENCE_SURFACE_V0"
TARGET_UNIT_ID = "candidate_missing_object_proposal_layer_application.r1000_top_group_taxonomy_gap_evidence_surface.v0"

SOURCE_PROPOSAL_LAYER_RECEIPT_ID = "6003c89c"
SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID = "087bf971"
SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID = "11d585b6"
SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID = "5b841942"
SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID = "e3371951"

OUT_DIR = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0"
RECEIPT_DIR = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0_receipts"

CANDIDATE_PROPOSAL_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_candidate_missing_object_proposal.json"
TYPED_DECISION_FIELDS_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_typed_unresolved_decision_fields.jsonl"
PROPOSAL_EVIDENCE_REFS_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_proposal_evidence_refs.json"
HUMAN_SCHEMA_DECISION_PACKET_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_human_schema_decision_packet.json"
PROPOSAL_TRANSITION_TRACE_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_proposal_transition_trace.json"
PROPOSAL_APPLICATION_REPORT_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_proposal_application_report.json"

PROPOSAL_LAYER_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0_receipts" / f"{SOURCE_PROPOSAL_LAYER_RECEIPT_ID}.json"
PROPOSAL_LAYER_CONTRACT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_missing_object_proposal_layer_contract.json"
PROPOSAL_OBJECT_SCHEMA_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_missing_object_proposal_object_schema.json"
TYPED_DECISION_FIELD_SCHEMA_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "typed_unresolved_decision_field_schema.json"
PROPOSAL_REVIEW_DECISION_SCHEMA_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_proposal_review_decision_schema.json"
PROPOSAL_REJECTION_TAXONOMY_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_proposal_rejection_taxonomy.json"
EXPECTED_LIMIT_TARGET_PROFILE_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "expected_limit_proposal_target_profile.json"
PROPOSAL_APPLICATION_CONTRACT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_proposal_application_contract.json"
PROPOSAL_LAYER_ACCEPTANCE_GATES_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_missing_object_proposal_layer_acceptance_gates.json"

QUEUE_RECONCILIATION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
QUEUE_RECONCILIATION_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0" / "r1000_pressure_queue_reconciliation.json"

EXPECTED_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_RECEIPT_ID}.json"
EXPECTED_LIMIT_MARKER_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0" / "expected_source_content_limit_marker.json"
EXPECTED_LIMIT_CLOSURE_RECORD_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0" / "expected_source_content_limit_closure_record.json"

FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_null_evidence_limit_classification_v0_receipts" / f"{SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID}.json"
FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH = ROOT / "data" / "field_introduction_proposal_typing_refinement_v0_receipts" / f"{SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID}.json"

CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID}.json"
CURRENT_SURFACE_PROTOCOL_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "current_surface_pressure_loop_protocol.json"

SOURCE_FILES = [
    PROPOSAL_LAYER_RECEIPT_PATH,
    PROPOSAL_LAYER_CONTRACT_PATH,
    PROPOSAL_OBJECT_SCHEMA_PATH,
    TYPED_DECISION_FIELD_SCHEMA_PATH,
    PROPOSAL_REVIEW_DECISION_SCHEMA_PATH,
    PROPOSAL_REJECTION_TAXONOMY_PATH,
    EXPECTED_LIMIT_TARGET_PROFILE_PATH,
    PROPOSAL_APPLICATION_CONTRACT_PATH,
    PROPOSAL_LAYER_ACCEPTANCE_GATES_PATH,
    QUEUE_RECONCILIATION_RECEIPT_PATH,
    QUEUE_RECONCILIATION_PATH,
    EXPECTED_LIMIT_RECEIPT_PATH,
    EXPECTED_LIMIT_MARKER_PATH,
    EXPECTED_LIMIT_CLOSURE_RECORD_PATH,
    FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH,
    FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH,
    CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH,
    CURRENT_SURFACE_PROTOCOL_PATH,
]

PRESSURE_GROUP = {
    "parent_pressure_class": "TAXONOMY_PRESSURE",
    "pressure_subtype": "missing_label",
    "halt_reason": "STOP_TAXONOMY_GAP",
    "pressure_group_key_hash": "38c604a1",
}

REQUIRED_DESCRIPTOR_FIELDS = [
    "missing_label_identifier",
    "taxonomy_context_ref",
    "current_label_space_ref",
    "expected_label_space_ref",
]

HUMAN_DECISION = {
    "decision": "APPLY_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_TO_R1000_TOP_GROUP_TAXONOMY_GAP_EVIDENCE_SURFACE",
    "scope": "emit one typed candidate missing-object proposal for the R1000 top-group taxonomy-gap evidence surface, without filling target fields or applying the proposal",
    "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
    "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
    "authorized": [
        "consume proposal layer contract",
        "consume expected-limit closure evidence",
        "emit one candidate missing-object proposal instance",
        "emit typed unresolved decision fields for required descriptor fields",
        "emit human/schema decision packet",
        "stop for human/schema decision",
    ],
    "not_authorized": [
        "applying the candidate proposal",
        "authorizing application",
        "filling missing_label_identifier",
        "filling taxonomy_context_ref",
        "filling current_label_space_ref",
        "filling expected_label_space_ref",
        "emitting untyped nulls",
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

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")

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
        "proposal_layer_receipt": read_json(PROPOSAL_LAYER_RECEIPT_PATH),
        "proposal_layer_contract": read_json(PROPOSAL_LAYER_CONTRACT_PATH),
        "proposal_object_schema": read_json(PROPOSAL_OBJECT_SCHEMA_PATH),
        "typed_decision_field_schema": read_json(TYPED_DECISION_FIELD_SCHEMA_PATH),
        "proposal_review_decision_schema": read_json(PROPOSAL_REVIEW_DECISION_SCHEMA_PATH),
        "proposal_rejection_taxonomy": read_json(PROPOSAL_REJECTION_TAXONOMY_PATH),
        "expected_limit_target_profile": read_json(EXPECTED_LIMIT_TARGET_PROFILE_PATH),
        "proposal_application_contract": read_json(PROPOSAL_APPLICATION_CONTRACT_PATH),
        "proposal_layer_acceptance_gates": read_json(PROPOSAL_LAYER_ACCEPTANCE_GATES_PATH),
        "queue_reconciliation_receipt": read_json(QUEUE_RECONCILIATION_RECEIPT_PATH),
        "queue_reconciliation": read_json(QUEUE_RECONCILIATION_PATH),
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

    layer_receipt = sources["proposal_layer_receipt"]
    target_profile = sources["expected_limit_target_profile"]
    expected_limit = sources["expected_limit_receipt"]
    queue = sources["queue_reconciliation_receipt"]

    if layer_receipt.get("receipt_id") != SOURCE_PROPOSAL_LAYER_RECEIPT_ID:
        failures.append("proposal_layer_receipt_id_wrong")
    if layer_receipt.get("gate") != "PASS":
        failures.append("proposal_layer_not_pass")
    if layer_receipt.get("aggregate_metrics", {}).get("proposal_layer_built_count") != 1:
        failures.append("proposal_layer_not_built")
    if layer_receipt.get("aggregate_metrics", {}).get("candidate_proposal_instance_emitted_count") != 0:
        failures.append("proposal_layer_build_already_emitted_candidate_instance")
    if layer_receipt.get("aggregate_metrics", {}).get("proposal_applied_count") != 0:
        failures.append("proposal_layer_build_already_applied_proposal")

    if target_profile.get("first_application_target") != UNIT_ID:
        failures.append("target_profile_first_application_target_wrong")
    if target_profile.get("proposal_only") is not True:
        failures.append("target_profile_not_proposal_only")
    if target_profile.get("application_authorized_by_layer") is not False:
        failures.append("target_profile_authorizes_application")
    if target_profile.get("required_descriptor_fields") != REQUIRED_DESCRIPTOR_FIELDS:
        failures.append("target_profile_required_fields_wrong")

    if expected_limit.get("receipt_id") != SOURCE_EXPECTED_LIMIT_RECEIPT_ID:
        failures.append("expected_limit_receipt_id_wrong")
    if expected_limit.get("gate") != "PASS":
        failures.append("expected_limit_not_pass")
    if expected_limit.get("aggregate_metrics", {}).get("branch_closed") is not True:
        failures.append("expected_limit_branch_not_closed")
    if expected_limit.get("aggregate_metrics", {}).get("expected_limit_marked") is not True:
        failures.append("expected_limit_not_marked")
    if expected_limit.get("aggregate_metrics", {}).get("pressure_group_key_hash") != "38c604a1":
        failures.append("expected_limit_pressure_group_hash_wrong")

    if queue.get("receipt_id") != SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID:
        failures.append("queue_reconciliation_receipt_id_wrong")
    if queue.get("gate") != "PASS":
        failures.append("queue_reconciliation_not_pass")
    if queue.get("aggregate_metrics", {}).get("resolved_group_count") != 2:
        failures.append("queue_resolved_group_count_wrong")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_evidence_refs() -> Dict[str, Any]:
    return {
        "schema_version": "r1000_top_group_taxonomy_gap_proposal_evidence_refs_v0",
        "source_pressure_group": PRESSURE_GROUP,
        "evidence_refs": [
            {
                "receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
                "artifact": rel(EXPECTED_LIMIT_CLOSURE_RECORD_PATH),
                "role": "expected-limit closure source",
            },
            {
                "receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
                "artifact": rel(EXPECTED_LIMIT_MARKER_PATH),
                "role": "expected-limit marker source",
            },
            {
                "receipt_id": SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID,
                "artifact": rel(FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_PATH),
                "role": "field-introduced null evidence limit classifier",
            },
            {
                "receipt_id": SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID,
                "artifact": rel(FIELD_INTRODUCTION_PROPOSAL_RECEIPT_PATH),
                "role": "field-introduction proposal typing source",
            },
            {
                "receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
                "artifact": rel(PROPOSAL_LAYER_CONTRACT_PATH),
                "role": "candidate proposal layer contract",
            },
        ],
    }

def typed_decision_field(field: str) -> Dict[str, Any]:
    return {
        "field": field,
        "value_state": "REQUIRES_SCHEMA_DECISION",
        "missing_object_type": "taxonomy_gap_evidence_surface_descriptor_field",
        "target_field": field,
        "decision_owner": "human_schema_layer",
        "allowed_resolution": [
            "provide_existing_source_reference",
            "define_schema_field_source",
            "mark_field_not_available_at_this_layer",
            "split_candidate_object",
            "weaken_candidate_object",
            "reject_candidate_object",
        ],
        "forbidden_resolution": [
            "set_null_as_value",
            "invent_value_without_source",
            "apply_candidate_without_acceptance",
            "create_taxonomy_label_without_authorization",
            "mutate_source_surface",
            "mutate_existing_receipt",
        ],
    }

def build_candidate_proposal(evidence_refs: Dict[str, Any]) -> Dict[str, Any]:
    unknown_fields = [typed_decision_field(field) for field in REQUIRED_DESCRIPTOR_FIELDS]
    candidate_seed = {
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_pressure_group": PRESSURE_GROUP,
        "missing_object_type": "taxonomy_gap_evidence_surface_descriptor",
        "target_field_or_surface": "field_introduced_taxonomy_gap_evidence_surface",
        "required_object_fields": REQUIRED_DESCRIPTOR_FIELDS,
    }
    candidate_object_id = sha8(candidate_seed)

    return {
        "schema_version": "candidate_missing_object_proposal_instance_v0",
        "candidate_object_id": candidate_object_id,
        "object_status": "CANDIDATE_MISSING_OBJECT_PROPOSAL",
        "missing_object_type": "taxonomy_gap_evidence_surface_descriptor",
        "target_field_or_surface": "field_introduced_taxonomy_gap_evidence_surface",
        "source_pressure_group": PRESSURE_GROUP,
        "source_evidence_refs": evidence_refs["evidence_refs"],
        "why_current_layer_stopped": "current source surface lacks required taxonomy-gap descriptor fields and upstream explicit tracked source chain did not supply non-null values",
        "what_object_is_missing": "a typed descriptor that identifies the missing label, taxonomy context, current label space, and expected label space for the R1000 top-group taxonomy-gap evidence surface",
        "required_object_fields": REQUIRED_DESCRIPTOR_FIELDS,
        "known_fields": {
            "pressure_group_key_hash": "38c604a1",
            "pressure_class": "TAXONOMY_PRESSURE",
            "pressure_subtype": "missing_label",
            "halt_reason": "STOP_TAXONOMY_GAP",
            "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
            "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        },
        "unknown_required_decision_fields": unknown_fields,
        "proposal_basis": "field extraction found taxonomy-gap pressure, but the field-introduced evidence surface lacks the descriptor values needed to distinguish missing label identity and label-space context",
        "candidate_payload": {
            "proposed_object_family": "taxonomy_gap_evidence_surface_descriptor",
            "proposed_scope": "r1000_top_group_38c604a1",
            "required_human_decision": "accept, reject, split, weaken, request more evidence, or mark descriptor unavailable at this layer",
        },
        "application_authorized": False,
        "required_human_schema_decision": [
            "ACCEPT_CANDIDATE_OBJECT",
            "REJECT_CANDIDATE_OBJECT",
            "SPLIT_CANDIDATE_OBJECT",
            "WEAKEN_CANDIDATE_OBJECT",
            "REQUEST_MORE_EVIDENCE",
            "MARK_EXPECTED_UNAVAILABLE_AT_THIS_LAYER",
        ],
        "forbidden_assumptions": [
            "do_not_fill_missing_label_identifier",
            "do_not_fill_taxonomy_context_ref",
            "do_not_fill_current_label_space_ref",
            "do_not_fill_expected_label_space_ref",
            "do_not_create_taxonomy_label",
            "do_not_claim_upstream_universal_nonexistence",
            "do_not_mutate_sources_or_receipts",
            "do_not_apply_without_acceptance",
        ],
        "expected_application_effect": "if accepted in a later unit, materialize a typed unresolved descriptor object while preserving target descriptor fields as decision fields rather than null or invented values",
        "rerun_review_rule": "after accepted application, rerun or review the affected evidence surface and classify whether the taxonomy-gap pressure became more distinguishable",
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_HUMAN_SCHEMA_DECISION_REQUIRED",
            "next_command_goal": None,
        },
    }

def build_human_schema_decision_packet(candidate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "candidate_missing_object_human_schema_decision_packet_v0",
        "decision_packet_id": sha8({
            "candidate_object_id": candidate["candidate_object_id"],
            "decision_scope": "human_schema_review",
        }),
        "candidate_object_id": candidate["candidate_object_id"],
        "candidate_object_ref": rel(CANDIDATE_PROPOSAL_PATH),
        "decision_required": True,
        "application_authorized": False,
        "allowed_decisions": [
            {
                "decision_status": "ACCEPT_CANDIDATE_OBJECT",
                "effect": "authorize a separate application unit to materialize typed unresolved descriptor fields",
            },
            {
                "decision_status": "REJECT_CANDIDATE_OBJECT",
                "effect": "record typed rejection codes and refine proposal schema",
            },
            {
                "decision_status": "SPLIT_CANDIDATE_OBJECT",
                "effect": "split proposal into narrower candidate objects",
            },
            {
                "decision_status": "WEAKEN_CANDIDATE_OBJECT",
                "effect": "reduce required object fields or scope",
            },
            {
                "decision_status": "REQUEST_MORE_EVIDENCE",
                "effect": "stop for additional evidence surface",
            },
            {
                "decision_status": "MARK_EXPECTED_UNAVAILABLE_AT_THIS_LAYER",
                "effect": "close proposal path as expected unavailable at this layer",
            },
        ],
        "typed_rejection_codes_available": [
            "WRONG_TARGET_FIELD",
            "WRONG_MISSING_OBJECT_TYPE",
            "WRONG_EVIDENCE_BASIS",
            "WRONG_SOURCE_LAYER",
            "WRONG_APPLICATION_SCOPE",
            "WRONG_PROPOSED_SCHEMA_FIELD",
            "WRONG_EXPECTED_LIMIT_CLASSIFICATION",
            "INSUFFICIENT_HUMAN_DECISION_OPTIONS",
            "FORBIDDEN_ASSUMPTION_PRESENT",
        ],
        "review_must_not": [
            "apply candidate in this unit",
            "fill unknown fields without source",
            "authorize taxonomy label creation implicitly",
            "mutate existing source/receipt artifacts",
        ],
        "terminal": candidate["terminal"],
    }

def build_transition_trace(candidate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "candidate_missing_object_proposal_application_transition_trace_v0",
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "candidate_object_id": candidate["candidate_object_id"],
        "trace": [
            {
                "step": "consume_proposal_layer",
                "question": "proposal_layer_available",
                "answer": True,
                "taken": "inspect_expected_limit_target",
            },
            {
                "step": "inspect_expected_limit_target",
                "question": "expected_limit_target_matches_r1000_taxonomy_gap",
                "answer": True,
                "taken": "emit_candidate_missing_object_proposal",
            },
            {
                "step": "emit_candidate_missing_object_proposal",
                "question": "unknown_required_fields_are_typed_decision_fields",
                "answer": True,
                "taken": "emit_human_schema_decision_packet",
            },
            {
                "step": "emit_human_schema_decision_packet",
                "question": "application_authorized_now",
                "answer": False,
                "taken": "STOP_HUMAN_SCHEMA_DECISION_REQUIRED",
            },
        ],
        "terminal": candidate["terminal"],
    }

def build_report(candidate: Dict[str, Any], typed_fields: List[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": "candidate_missing_object_proposal_application_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "candidate_object_id": candidate["candidate_object_id"],
        "candidate_proposal_instance_emitted_count": 1,
        "typed_unresolved_decision_field_count": len(typed_fields),
        "required_descriptor_field_count": len(REQUIRED_DESCRIPTOR_FIELDS),
        "proposal_status": "CANDIDATE_MISSING_OBJECT_PROPOSAL",
        "missing_object_type": "taxonomy_gap_evidence_surface_descriptor",
        "target_field_or_surface": "field_introduced_taxonomy_gap_evidence_surface",
        "human_schema_decision_required_count": 1,
        "proposal_applied_count": 0,
        "application_authorized_count": 0,
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
        "recommended_next_handling": "REVIEW_CANDIDATE_MISSING_OBJECT_PROPOSAL_FOR_R1000_TOP_GROUP_TAXONOMY_GAP_V0",
    }

def validate_candidate(candidate: Dict[str, Any], typed_fields: List[Dict[str, Any]], evidence_refs: Dict[str, Any], decision_packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if candidate.get("object_status") != "CANDIDATE_MISSING_OBJECT_PROPOSAL":
        failures.append("candidate_status_wrong")
    if candidate.get("application_authorized") is not False:
        failures.append("candidate_self_authorizes_application")
    if candidate.get("missing_object_type") != "taxonomy_gap_evidence_surface_descriptor":
        failures.append("candidate_missing_object_type_wrong")
    if candidate.get("required_object_fields") != REQUIRED_DESCRIPTOR_FIELDS:
        failures.append("candidate_required_object_fields_wrong")
    if len(candidate.get("unknown_required_decision_fields", [])) != len(REQUIRED_DESCRIPTOR_FIELDS):
        failures.append("candidate_unknown_required_decision_field_count_wrong")
    if len(typed_fields) != len(REQUIRED_DESCRIPTOR_FIELDS):
        failures.append("typed_decision_field_count_wrong")
    if not candidate.get("source_evidence_refs"):
        failures.append("candidate_evidence_refs_missing")
    if len(evidence_refs.get("evidence_refs", [])) < 4:
        failures.append("evidence_refs_insufficient")

    for field_obj in typed_fields:
        if field_obj.get("value_state") != "REQUIRES_SCHEMA_DECISION":
            failures.append(f"typed_field_state_wrong:{field_obj.get('field')}:{field_obj.get('value_state')}")
        if field_obj.get("field") not in REQUIRED_DESCRIPTOR_FIELDS:
            failures.append(f"typed_field_unexpected:{field_obj.get('field')}")
        if "set_null_as_value" not in field_obj.get("forbidden_resolution", []):
            failures.append(f"typed_field_null_not_forbidden:{field_obj.get('field')}")
        if "invent_value_without_source" not in field_obj.get("forbidden_resolution", []):
            failures.append(f"typed_field_invention_not_forbidden:{field_obj.get('field')}")

    if decision_packet.get("decision_required") is not True:
        failures.append("decision_packet_decision_required_wrong")
    if decision_packet.get("application_authorized") is not False:
        failures.append("decision_packet_authorizes_application")
    if candidate["terminal"]["stop_code"] != "STOP_HUMAN_SCHEMA_DECISION_REQUIRED":
        failures.append(f"candidate_terminal_stop_wrong:{candidate['terminal']}")
    if candidate["terminal"]["next_command_goal"] is not None:
        failures.append("candidate_terminal_next_not_null")

    for key in [
        "proposal_applied_count",
        "application_authorized_count",
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

    if report.get("candidate_proposal_instance_emitted_count") != 1:
        failures.append("candidate_proposal_instance_emitted_count_wrong")
    if report.get("human_schema_decision_required_count") != 1:
        failures.append("human_schema_decision_required_count_wrong")

    candidate_text = json.dumps(candidate, sort_keys=True)
    for forbidden_literal in [
        '"missing_label_identifier": null',
        '"taxonomy_context_ref": null',
        '"current_label_space_ref": null',
        '"expected_label_space_ref": null',
    ]:
        if forbidden_literal in candidate_text:
            failures.append(f"forbidden_untyped_null_literal_present:{forbidden_literal}")

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
    if metrics.get("candidate_proposal_instance_emitted_count") != 1:
        failures.append(f"metric_candidate_count_wrong:{metrics.get('candidate_proposal_instance_emitted_count')}")
    if metrics.get("typed_unresolved_decision_field_count") != len(REQUIRED_DESCRIPTOR_FIELDS):
        failures.append(f"metric_typed_field_count_wrong:{metrics.get('typed_unresolved_decision_field_count')}")
    if metrics.get("human_schema_decision_required_count") != 1:
        failures.append(f"metric_human_schema_decision_count_wrong:{metrics.get('human_schema_decision_required_count')}")

    for key in [
        "proposal_applied_count",
        "application_authorized_count",
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
    if terminal.get("stop_code") != "STOP_HUMAN_SCHEMA_DECISION_REQUIRED":
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

    evidence_refs = build_evidence_refs()
    candidate = build_candidate_proposal(evidence_refs)
    typed_fields = candidate["unknown_required_decision_fields"]
    decision_packet = build_human_schema_decision_packet(candidate)
    trace = build_transition_trace(candidate)
    report = build_report(candidate, typed_fields)

    write_json(PROPOSAL_EVIDENCE_REFS_PATH, evidence_refs)
    write_json(CANDIDATE_PROPOSAL_PATH, candidate)
    write_jsonl(TYPED_DECISION_FIELDS_PATH, typed_fields)
    write_json(HUMAN_SCHEMA_DECISION_PACKET_PATH, decision_packet)
    write_json(PROPOSAL_TRANSITION_TRACE_PATH, trace)
    write_json(PROPOSAL_APPLICATION_REPORT_PATH, report)

    failures.extend(validate_candidate(candidate, typed_fields, evidence_refs, decision_packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "PROPOSAL_APP_0_PROPOSAL_LAYER_CONSUMED": sources["proposal_layer_receipt"]["receipt_id"] == SOURCE_PROPOSAL_LAYER_RECEIPT_ID and sources["proposal_layer_receipt"]["gate"] == "PASS",
        "PROPOSAL_APP_1_EXPECTED_LIMIT_TARGET_CONSUMED": sources["expected_limit_receipt"]["receipt_id"] == SOURCE_EXPECTED_LIMIT_RECEIPT_ID and sources["expected_limit_receipt"]["gate"] == "PASS",
        "PROPOSAL_APP_2_CANDIDATE_PROPOSAL_INSTANCE_EMITTED": CANDIDATE_PROPOSAL_PATH.exists() and report["candidate_proposal_instance_emitted_count"] == 1,
        "PROPOSAL_APP_3_TYPED_DECISION_FIELDS_EMITTED": TYPED_DECISION_FIELDS_PATH.exists() and len(typed_fields) == 4,
        "PROPOSAL_APP_4_EVIDENCE_REFS_EMITTED": PROPOSAL_EVIDENCE_REFS_PATH.exists() and len(evidence_refs["evidence_refs"]) >= 4,
        "PROPOSAL_APP_5_HUMAN_SCHEMA_DECISION_PACKET_EMITTED": HUMAN_SCHEMA_DECISION_PACKET_PATH.exists() and decision_packet["decision_required"] is True,
        "PROPOSAL_APP_6_NO_PROPOSAL_APPLIED": report["proposal_applied_count"] == 0,
        "PROPOSAL_APP_7_NO_APPLICATION_AUTHORIZED": report["application_authorized_count"] == 0 and candidate["application_authorized"] is False and decision_packet["application_authorized"] is False,
        "PROPOSAL_APP_8_NO_TARGET_FIELD_FILLED_OR_NULL_EMITTED": report["target_field_filled_count"] == 0 and report["null_field_value_emitted_count"] == 0,
        "PROPOSAL_APP_9_NO_VALUE_OR_TAXONOMY_ACTION": report["field_value_invention_count"] == 0 and report["taxonomy_label_creation_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "PROPOSAL_APP_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "PROPOSAL_APP_11_NO_R1000_RUN_OR_GROUP_OPEN": report["r1000_run_executed_count"] == 0 and report["pressure_group_opened_count"] == 0 and report["next_group_auto_opened_count"] == 0,
        "PROPOSAL_APP_12_STOP_HUMAN_SCHEMA_DECISION_REQUIRED": candidate["terminal"]["stop_code"] == "STOP_HUMAN_SCHEMA_DECISION_REQUIRED",
        "PROPOSAL_APP_13_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and candidate["terminal"]["next_command_goal"] is None,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_HUMAN_SCHEMA_DECISION_REQUIRED",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_field_introduced_null_limit_receipt_id": SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID,
        "source_field_introduction_proposal_receipt_id": SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "candidate_object_id": candidate["candidate_object_id"],
        "candidate_proposal_instance_emitted_count": 1,
        "typed_unresolved_decision_field_count": len(typed_fields),
        "required_descriptor_field_count": len(REQUIRED_DESCRIPTOR_FIELDS),
        "evidence_ref_count": len(evidence_refs["evidence_refs"]),
        "human_schema_decision_required_count": 1,
        "proposal_status": "CANDIDATE_MISSING_OBJECT_PROPOSAL",
        "missing_object_type": "taxonomy_gap_evidence_surface_descriptor",
        "target_field_or_surface": "field_introduced_taxonomy_gap_evidence_surface",
        "proposal_applied_count": 0,
        "application_authorized_count": 0,
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
        "recommended_next_handling": report["recommended_next_handling"],
    }

    guards = {
        "proposal_layer_consumed": True,
        "expected_limit_target_consumed": True,
        "candidate_proposal_instance_emitted": True,
        "typed_decision_fields_emitted": True,
        "human_schema_decision_packet_emitted": True,
        "proposal_applied": False,
        "application_authorized": False,
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
        "source_proposal_layer": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "candidate_object_id": candidate["candidate_object_id"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "candidate_missing_object_proposal": rel(CANDIDATE_PROPOSAL_PATH),
        "typed_unresolved_decision_fields": rel(TYPED_DECISION_FIELDS_PATH),
        "proposal_evidence_refs": rel(PROPOSAL_EVIDENCE_REFS_PATH),
        "human_schema_decision_packet": rel(HUMAN_SCHEMA_DECISION_PACKET_PATH),
        "proposal_transition_trace": rel(PROPOSAL_TRANSITION_TRACE_PATH),
        "proposal_application_report": rel(PROPOSAL_APPLICATION_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "candidate_missing_object_proposal_application_r1000_taxonomy_gap_receipt_v0",
        "receipt_type": "CANDIDATE_MISSING_OBJECT_PROPOSAL_APPLICATION_R1000_TAXONOMY_GAP_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_field_introduced_null_limit_receipt_id": SOURCE_FIELD_INTRODUCED_NULL_LIMIT_RECEIPT_ID,
        "source_field_introduction_proposal_receipt_id": SOURCE_FIELD_INTRODUCTION_PROPOSAL_RECEIPT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "candidate_missing_object_proposal_application_summary": {
            "candidate_object_id": candidate["candidate_object_id"],
            "proposal_status": "CANDIDATE_MISSING_OBJECT_PROPOSAL",
            "missing_object_type": "taxonomy_gap_evidence_surface_descriptor",
            "target_field_or_surface": "field_introduced_taxonomy_gap_evidence_surface",
            "source_pressure_group": PRESSURE_GROUP,
            "typed_unresolved_decision_field_count": len(typed_fields),
            "required_descriptor_fields": REQUIRED_DESCRIPTOR_FIELDS,
            "application_authorized": False,
            "proposal_applied": False,
            "human_schema_decision_required": True,
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "candidate_missing_object_proposal_application_guards": guards,
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
    print(f"candidate_missing_object_proposal_application_receipt_id={receipt_id}")
    print(f"candidate_missing_object_proposal_application_receipt_path=data/candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0_receipts/{receipt_id}.json")
    print(f"candidate_missing_object_proposal_path=data/candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0/r1000_top_group_taxonomy_gap_candidate_missing_object_proposal.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
