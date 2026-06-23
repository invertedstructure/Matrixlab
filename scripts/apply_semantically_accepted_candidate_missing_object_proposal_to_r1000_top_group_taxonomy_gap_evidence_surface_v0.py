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

UNIT_ID = "APPLY_SEMANTICALLY_ACCEPTED_CANDIDATE_MISSING_OBJECT_PROPOSAL_TO_R1000_TOP_GROUP_TAXONOMY_GAP_EVIDENCE_SURFACE_V0"
TARGET_UNIT_ID = "semantically_accepted_candidate_application.r1000_top_group_taxonomy_gap.v0"

SOURCE_PATCHED_REVIEW_RECEIPT_ID = "0fe3bb6a"
SOURCE_SEMANTIC_PATCH_RECEIPT_ID = "7d078710"
SOURCE_SEMANTIC_BARRIER_RECEIPT_ID = "4e6b09b2"
SOURCE_PROPOSAL_REVIEW_RECEIPT_ID = "a939b4a6"
SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID = "aa01c2a9"
SOURCE_PROPOSAL_LAYER_RECEIPT_ID = "6003c89c"
SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
SOURCE_CANDIDATE_OBJECT_ID = "ce1fe7fc"
PATCHED_CANDIDATE_OBJECT_ID = "a9ec669b"

OUT_DIR = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0"
RECEIPT_DIR = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0_receipts"

ACCEPTED_DESCRIPTOR_OBJECT_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_accepted_typed_unresolved_descriptor_object.json"
APPLIED_EVIDENCE_SURFACE_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_evidence_surface_with_accepted_typed_unresolved_descriptor.json"
APPLICATION_BINDING_PATH = OUT_DIR / "semantically_accepted_candidate_application_binding.json"
APPLICATION_LIMITS_PATH = OUT_DIR / "semantically_accepted_candidate_application_limits.json"
APPLICATION_REVIEW_PACKET_PATH = OUT_DIR / "accepted_descriptor_application_review_packet.json"
APPLICATION_TRANSITION_TRACE_PATH = OUT_DIR / "semantically_accepted_candidate_application_transition_trace.json"
APPLICATION_REPORT_PATH = OUT_DIR / "semantically_accepted_candidate_application_report.json"

PATCHED_REVIEW_RECEIPT_PATH = ROOT / "data" / "semantically_patched_candidate_review_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PATCHED_REVIEW_RECEIPT_ID}.json"
PATCHED_REVIEW_DECISION_PATH = ROOT / "data" / "semantically_patched_candidate_review_r1000_taxonomy_gap_v0" / "semantically_patched_candidate_review_decision.json"
PATCHED_REVIEW_FINDINGS_PATH = ROOT / "data" / "semantically_patched_candidate_review_r1000_taxonomy_gap_v0" / "semantically_patched_candidate_review_findings.json"
PATCHED_REVIEW_AUTHORIZATION_PACKET_PATH = ROOT / "data" / "semantically_patched_candidate_review_r1000_taxonomy_gap_v0" / "semantically_patched_candidate_application_authorization_packet.json"
PATCHED_REVIEW_REPORT_PATH = ROOT / "data" / "semantically_patched_candidate_review_r1000_taxonomy_gap_v0" / "semantically_patched_candidate_review_report.json"

SEMANTIC_PATCH_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_SEMANTIC_PATCH_RECEIPT_ID}.json"
PATCHED_CANDIDATE_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_semantically_patched_candidate_missing_object_proposal.json"
PATCHED_CANDIDATE_REVIEW_PACKET_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0" / "patched_candidate_review_packet.json"
PATCHED_CANDIDATE_BLOCKER_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0" / "patched_candidate_application_blocker_packet.json"
PATCH_DELTA_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0" / "candidate_semantic_patch_delta.json"
IN_CHAT_SEMANTIC_REVIEW_RESULT_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0" / "in_chat_semantic_review_result.json"

SEMANTIC_BARRIER_RECEIPT_PATH = ROOT / "data" / "candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_SEMANTIC_BARRIER_RECEIPT_ID}.json"
PROPOSAL_REVIEW_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PROPOSAL_REVIEW_RECEIPT_ID}.json"
PROPOSAL_APPLICATION_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID}.json"
TYPED_DECISION_FIELDS_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_typed_unresolved_decision_fields.jsonl"
PROPOSAL_EVIDENCE_REFS_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_proposal_evidence_refs.json"

PROPOSAL_LAYER_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0_receipts" / f"{SOURCE_PROPOSAL_LAYER_RECEIPT_ID}.json"
PROPOSAL_APPLICATION_CONTRACT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_proposal_application_contract.json"
EXPECTED_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_RECEIPT_ID}.json"

SOURCE_FILES = [
    PATCHED_REVIEW_RECEIPT_PATH,
    PATCHED_REVIEW_DECISION_PATH,
    PATCHED_REVIEW_FINDINGS_PATH,
    PATCHED_REVIEW_AUTHORIZATION_PACKET_PATH,
    PATCHED_REVIEW_REPORT_PATH,
    SEMANTIC_PATCH_RECEIPT_PATH,
    PATCHED_CANDIDATE_PATH,
    PATCHED_CANDIDATE_REVIEW_PACKET_PATH,
    PATCHED_CANDIDATE_BLOCKER_PATH,
    PATCH_DELTA_PATH,
    IN_CHAT_SEMANTIC_REVIEW_RESULT_PATH,
    SEMANTIC_BARRIER_RECEIPT_PATH,
    PROPOSAL_REVIEW_RECEIPT_PATH,
    PROPOSAL_APPLICATION_RECEIPT_PATH,
    TYPED_DECISION_FIELDS_PATH,
    PROPOSAL_EVIDENCE_REFS_PATH,
    PROPOSAL_LAYER_RECEIPT_PATH,
    PROPOSAL_APPLICATION_CONTRACT_PATH,
    EXPECTED_LIMIT_RECEIPT_PATH,
]

REQUIRED_DESCRIPTOR_FIELDS = [
    "missing_label_identifier",
    "taxonomy_context_ref",
    "current_label_space_ref",
    "expected_label_space_ref",
]

HUMAN_DECISION = {
    "decision": "APPLY_SEMANTICALLY_ACCEPTED_CANDIDATE_MISSING_OBJECT_PROPOSAL_TO_R1000_TOP_GROUP_TAXONOMY_GAP_EVIDENCE_SURFACE",
    "scope": "materialize the semantically accepted patched candidate as an accepted typed unresolved descriptor object on a new derived evidence surface without filling descriptor values or mutating sources",
    "source_patched_review_receipt_id": SOURCE_PATCHED_REVIEW_RECEIPT_ID,
    "source_semantic_patch_receipt_id": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
    "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
    "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
    "authorized": [
        "consume semantically accepted patched candidate review receipt",
        "consume patched candidate object",
        "materialize accepted typed unresolved descriptor object",
        "bind accepted descriptor object to derived R1000 taxonomy-gap evidence surface",
        "preserve typed unresolved descriptor fields",
        "preserve negative claims",
        "preserve evidence basis limitation",
        "emit application review packet",
        "stop without R1000 run or group opening",
    ],
    "not_authorized": [
        "assigning descriptor values",
        "filling missing_label_identifier",
        "filling taxonomy_context_ref",
        "filling current_label_space_ref",
        "filling expected_label_space_ref",
        "inventing values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "emitting taxonomy delta proposal",
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
        "patched_review_receipt": read_json(PATCHED_REVIEW_RECEIPT_PATH),
        "patched_review_decision": read_json(PATCHED_REVIEW_DECISION_PATH),
        "patched_review_findings": read_json(PATCHED_REVIEW_FINDINGS_PATH),
        "patched_review_authorization_packet": read_json(PATCHED_REVIEW_AUTHORIZATION_PACKET_PATH),
        "patched_review_report": read_json(PATCHED_REVIEW_REPORT_PATH),
        "semantic_patch_receipt": read_json(SEMANTIC_PATCH_RECEIPT_PATH),
        "patched_candidate": read_json(PATCHED_CANDIDATE_PATH),
        "patched_candidate_review_packet": read_json(PATCHED_CANDIDATE_REVIEW_PACKET_PATH),
        "patched_candidate_blocker": read_json(PATCHED_CANDIDATE_BLOCKER_PATH),
        "patch_delta": read_json(PATCH_DELTA_PATH),
        "in_chat_semantic_review_result": read_json(IN_CHAT_SEMANTIC_REVIEW_RESULT_PATH),
        "semantic_barrier_receipt": read_json(SEMANTIC_BARRIER_RECEIPT_PATH),
        "proposal_review_receipt": read_json(PROPOSAL_REVIEW_RECEIPT_PATH),
        "proposal_application_receipt": read_json(PROPOSAL_APPLICATION_RECEIPT_PATH),
        "typed_decision_fields": read_jsonl(TYPED_DECISION_FIELDS_PATH),
        "proposal_evidence_refs": read_json(PROPOSAL_EVIDENCE_REFS_PATH),
        "proposal_layer_receipt": read_json(PROPOSAL_LAYER_RECEIPT_PATH),
        "proposal_application_contract": read_json(PROPOSAL_APPLICATION_CONTRACT_PATH),
        "expected_limit_receipt": read_json(EXPECTED_LIMIT_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    review_receipt = sources["patched_review_receipt"]
    review_decision = sources["patched_review_decision"]
    authorization = sources["patched_review_authorization_packet"]
    patched = sources["patched_candidate"]

    if review_receipt.get("receipt_id") != SOURCE_PATCHED_REVIEW_RECEIPT_ID:
        failures.append("patched_review_receipt_id_wrong")
    if review_receipt.get("gate") != "PASS":
        failures.append("patched_review_not_pass")
    if review_receipt.get("patched_candidate_object_id") != PATCHED_CANDIDATE_OBJECT_ID:
        failures.append("patched_candidate_id_wrong_in_review_receipt")
    if review_receipt.get("aggregate_metrics", {}).get("semantic_acceptance_count") != 1:
        failures.append("semantic_acceptance_missing")
    if review_receipt.get("aggregate_metrics", {}).get("application_authorized_for_separate_unit_count") != 1:
        failures.append("separate_application_not_authorized")
    if review_receipt.get("aggregate_metrics", {}).get("application_authorized_in_this_unit_count") != 0:
        failures.append("review_authorized_current_unit")
    if review_receipt.get("aggregate_metrics", {}).get("proposal_applied_count") != 0:
        failures.append("proposal_already_applied_by_review")

    if review_decision.get("decision_status") != "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION":
        failures.append("patched_review_decision_not_accept")
    if review_decision.get("application_authorized_for_separate_unit") is not True:
        failures.append("patched_review_decision_no_separate_auth")
    if review_decision.get("application_authorized_in_this_unit") is not False:
        failures.append("patched_review_decision_current_unit_auth")

    if authorization.get("application_authorized_for_separate_unit") is not True:
        failures.append("authorization_packet_no_separate_auth")
    if authorization.get("application_authorized_in_this_unit") is not False:
        failures.append("authorization_packet_current_unit_auth")

    if patched.get("candidate_object_id") != PATCHED_CANDIDATE_OBJECT_ID:
        failures.append("patched_candidate_object_id_wrong")
    if patched.get("object_status") != "SEMANTICALLY_PATCHED_CANDIDATE_MISSING_OBJECT_PROPOSAL":
        failures.append("patched_candidate_status_wrong")
    if patched.get("semantic_status") != "TYPED_UNRESOLVED_DESCRIPTOR_PROPOSAL":
        failures.append("patched_semantic_status_wrong")
    if patched.get("descriptor_status") != "CANDIDATE_UNRESOLVED_DESCRIPTOR_NOT_VALUE_DESCRIPTOR":
        failures.append("patched_descriptor_status_wrong")
    if patched.get("application_authorized") is not False:
        failures.append("patched_candidate_self_authorizes_application")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_accepted_descriptor_object(patched: Dict[str, Any], typed_fields: List[Dict[str, Any]]) -> Dict[str, Any]:
    accepted_object_id = sha8({
        "patched_candidate_object_id": patched["candidate_object_id"],
        "application": "accepted_typed_unresolved_descriptor_object",
        "source_review_receipt": SOURCE_PATCHED_REVIEW_RECEIPT_ID,
    })

    return {
        "schema_version": "accepted_typed_unresolved_descriptor_object_v0",
        "accepted_descriptor_object_id": accepted_object_id,
        "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": patched["candidate_object_id"],
        "object_status": "ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_OBJECT",
        "semantic_status": patched["semantic_status"],
        "descriptor_status": patched["descriptor_status"],
        "target_surface": "r1000_top_group_taxonomy_gap_evidence_surface",
        "positive_claim": patched["positive_claim"],
        "negative_claims": patched["negative_claims"],
        "evidence_basis_strength": patched["evidence_basis_strength"],
        "required_descriptor_fields": REQUIRED_DESCRIPTOR_FIELDS,
        "typed_unresolved_descriptor_fields": typed_fields,
        "descriptor_values": {
            "missing_label_identifier": {"value_state": "REQUIRES_SCHEMA_DECISION", "value_present": False, "value_is_assigned": False, "forbidden_resolution": ["set_null_as_value", "invent_value_without_source"]},
            "taxonomy_context_ref": {"value_state": "REQUIRES_SCHEMA_DECISION", "value_present": False, "value_is_assigned": False, "forbidden_resolution": ["set_null_as_value", "invent_value_without_source"]},
            "current_label_space_ref": {"value_state": "REQUIRES_SCHEMA_DECISION", "value_present": False, "value_is_assigned": False, "forbidden_resolution": ["set_null_as_value", "invent_value_without_source"]},
            "expected_label_space_ref": {"value_state": "REQUIRES_SCHEMA_DECISION", "value_present": False, "value_is_assigned": False, "forbidden_resolution": ["set_null_as_value", "invent_value_without_source"]},
        },
        "application_effect": "materialized accepted unresolved descriptor object only",
        "application_authorized_by_receipt": SOURCE_PATCHED_REVIEW_RECEIPT_ID,
        "application_authorized_for_this_unit": True,
        "proposal_applied_as_unresolved_descriptor_object": True,
        "descriptor_value_assignment": False,
        "taxonomy_repair_authorized": False,
        "source_mutation_authorized": False,
        "r1000_run_authorized": False,
        "created_from": {
            "semantically_patched_candidate_path": rel(PATCHED_CANDIDATE_PATH),
            "patched_review_receipt_path": rel(PATCHED_REVIEW_RECEIPT_PATH),
        },
    }

def build_applied_surface(accepted: Dict[str, Any], sources: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_top_group_taxonomy_gap_evidence_surface_with_accepted_typed_unresolved_descriptor_v0",
        "surface_id": sha8({
            "accepted_descriptor_object_id": accepted["accepted_descriptor_object_id"],
            "surface": "r1000_top_group_taxonomy_gap_evidence_surface_with_accepted_typed_unresolved_descriptor",
        }),
        "source_surface_refs": {
            "proposal_application_receipt": rel(PROPOSAL_APPLICATION_RECEIPT_PATH),
            "semantic_patch_receipt": rel(SEMANTIC_PATCH_RECEIPT_PATH),
            "patched_review_receipt": rel(PATCHED_REVIEW_RECEIPT_PATH),
            "expected_limit_receipt": rel(EXPECTED_LIMIT_RECEIPT_PATH),
        },
        "surface_status": "DERIVED_SURFACE_WITH_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_OBJECT",
        "accepted_descriptor_object_ref": rel(ACCEPTED_DESCRIPTOR_OBJECT_PATH),
        "accepted_descriptor_object_id": accepted["accepted_descriptor_object_id"],
        "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
        "preserved_evidence_refs": sources["proposal_evidence_refs"].get("evidence_refs", []),
        "typed_unresolved_descriptor_fields": accepted["typed_unresolved_descriptor_fields"],
        "semantic_limitations": {
            "descriptor_values_assigned": False,
            "taxonomy_repair_authorized": False,
            "source_mutation_authorized": False,
            "global_absence_claim_authorized": False,
            "r1000_run_authorized": False,
        },
        "surface_change": {
            "before": "taxonomy-gap evidence surface had required descriptor pressure but no accepted descriptor object",
            "after": "surface has accepted typed unresolved descriptor object with all descriptor values still unresolved",
        },
    }

def build_application_binding(accepted: Dict[str, Any], surface: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "semantically_accepted_candidate_application_binding_v0",
        "binding_id": sha8({
            "accepted_descriptor_object_id": accepted["accepted_descriptor_object_id"],
            "surface_id": surface["surface_id"],
        }),
        "binding_status": "BOUND_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_TO_DERIVED_EVIDENCE_SURFACE",
        "accepted_descriptor_object_id": accepted["accepted_descriptor_object_id"],
        "accepted_descriptor_object_ref": rel(ACCEPTED_DESCRIPTOR_OBJECT_PATH),
        "derived_surface_id": surface["surface_id"],
        "derived_surface_ref": rel(APPLIED_EVIDENCE_SURFACE_PATH),
        "application_scope": "accepted unresolved descriptor object materialization only",
        "not_in_scope": [
            "descriptor value assignment",
            "taxonomy label creation",
            "taxonomy upgrade",
            "source mutation",
            "receipt mutation",
            "R1000 execution",
            "pressure group opening",
        ],
    }

def build_application_limits(accepted: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "semantically_accepted_candidate_application_limits_v0",
        "accepted_descriptor_object_id": accepted["accepted_descriptor_object_id"],
        "limits": {
            "descriptor_value_assignment_allowed": False,
            "target_field_filling_allowed": False,
            "taxonomy_repair_allowed": False,
            "taxonomy_delta_allowed": False,
            "source_mutation_allowed": False,
            "existing_receipt_mutation_allowed": False,
            "r1000_run_allowed": False,
            "pressure_group_open_allowed": False,
            "hidden_next_command_allowed": False,
        },
        "allowed_next_review_questions": [
            "does the derived surface expose the typed unresolved descriptor cleanly",
            "does the object improve reviewability without overstating evidence",
            "does a later layer need more evidence or a split descriptor object",
        ],
    }

def build_review_packet(accepted: Dict[str, Any], surface: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "accepted_descriptor_application_review_packet_v0",
        "accepted_descriptor_object_id": accepted["accepted_descriptor_object_id"],
        "derived_surface_id": surface["surface_id"],
        "review_required": True,
        "review_scope": "review derived surface after accepted unresolved descriptor object materialization",
        "must_check": [
            "accepted descriptor object is present",
            "descriptor values remain unresolved",
            "typed unresolved decision fields remain visible",
            "negative claims are preserved",
            "evidence basis limitation is preserved",
            "no taxonomy repair or value assignment occurred",
        ],
        "allowed_outcomes": [
            "ACCEPT_DERIVED_SURFACE_WITH_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR",
            "REQUEST_MORE_EVIDENCE",
            "SPLIT_DESCRIPTOR_OBJECT",
            "MARK_EXPECTED_UNAVAILABLE_AT_THIS_LAYER",
            "REJECT_APPLICATION_SURFACE_AND_REPATCH",
        ],
    }

def build_transition_trace(accepted: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "semantically_accepted_candidate_application_transition_trace_v0",
        "accepted_descriptor_object_id": accepted["accepted_descriptor_object_id"],
        "trace": [
            {
                "step": "consume_semantic_acceptance",
                "question": "patched candidate accepted for separate application",
                "answer": True,
                "taken": "materialize_unresolved_descriptor_object",
            },
            {
                "step": "materialize_unresolved_descriptor_object",
                "question": "descriptor values assigned",
                "answer": False,
                "taken": "bind_object_to_derived_surface",
            },
            {
                "step": "bind_object_to_derived_surface",
                "question": "taxonomy_or_source_mutation_required",
                "answer": False,
                "taken": "emit_application_review_packet",
            },
            {
                "step": "emit_application_review_packet",
                "question": "run_R1000_or_open_group_now",
                "answer": False,
                "taken": "STOP_SEMANTICALLY_ACCEPTED_CANDIDATE_APPLICATION_COMPLETE_REQUIRES_SURFACE_REVIEW",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_SEMANTICALLY_ACCEPTED_CANDIDATE_APPLICATION_COMPLETE_REQUIRES_SURFACE_REVIEW",
            "next_command_goal": None,
        },
    }

def build_report(accepted: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "semantically_accepted_candidate_application_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_patched_review_receipt_id": SOURCE_PATCHED_REVIEW_RECEIPT_ID,
        "source_semantic_patch_receipt_id": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
        "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
        "accepted_descriptor_object_id": accepted["accepted_descriptor_object_id"],
        "semantic_acceptance_consumed_count": 1,
        "separate_application_authorization_consumed_count": 1,
        "accepted_descriptor_object_materialized_count": 1,
        "derived_surface_emitted_count": 1,
        "application_binding_emitted_count": 1,
        "application_review_packet_emitted_count": 1,
        "proposal_applied_count": 1,
        "proposal_applied_as_unresolved_descriptor_object_count": 1,
        "application_authorized_for_this_unit_count": 1,
        "target_field_filled_count": 0,
        "descriptor_value_assignment_count": 0,
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
        "recommended_next_handling": "REVIEW_DERIVED_R1000_TOP_GROUP_TAXONOMY_GAP_SURFACE_WITH_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_V0",
    }

def validate_application_outputs(
    accepted: Dict[str, Any],
    surface: Dict[str, Any],
    binding: Dict[str, Any],
    limits: Dict[str, Any],
    review_packet: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if accepted.get("object_status") != "ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_OBJECT":
        failures.append("accepted_descriptor_status_wrong")
    if accepted.get("semantic_status") != "TYPED_UNRESOLVED_DESCRIPTOR_PROPOSAL":
        failures.append("accepted_semantic_status_wrong")
    if accepted.get("descriptor_status") != "CANDIDATE_UNRESOLVED_DESCRIPTOR_NOT_VALUE_DESCRIPTOR":
        failures.append("accepted_descriptor_claim_too_strong")
    if accepted.get("proposal_applied_as_unresolved_descriptor_object") is not True:
        failures.append("proposal_not_applied_as_unresolved_descriptor_object")
    if accepted.get("descriptor_value_assignment") is not False:
        failures.append("descriptor_values_assigned")
    if accepted.get("taxonomy_repair_authorized") is not False:
        failures.append("taxonomy_repair_authorized")
    if accepted.get("source_mutation_authorized") is not False:
        failures.append("source_mutation_authorized")
    for field in REQUIRED_DESCRIPTOR_FIELDS:
        field_obj = accepted.get("descriptor_values", {}).get(field, {})
        if field_obj.get("value_is_assigned") is not False:
            failures.append(f"descriptor_value_assigned:{field}")
        if field_obj.get("value_present") is not False:
            failures.append(f"descriptor_value_present:{field}")
        if "value" in field_obj:
            failures.append(f"descriptor_null_or_literal_value_key_present:{field}")
        if field_obj.get("value_state") != "REQUIRES_SCHEMA_DECISION":
            failures.append(f"descriptor_value_state_wrong:{field}")
        if "set_null_as_value" not in field_obj.get("forbidden_resolution", []):
            failures.append(f"descriptor_forbidden_null_resolution_missing:{field}")
    if surface.get("surface_status") != "DERIVED_SURFACE_WITH_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_OBJECT":
        failures.append("derived_surface_status_wrong")
    if surface.get("semantic_limitations", {}).get("descriptor_values_assigned") is not False:
        failures.append("surface_descriptor_values_assigned")
    if binding.get("binding_status") != "BOUND_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_TO_DERIVED_EVIDENCE_SURFACE":
        failures.append("binding_status_wrong")
    for key, value in limits.get("limits", {}).items():
        if value is not False:
            failures.append(f"limit_not_false:{key}:{value}")
    if review_packet.get("review_required") is not True:
        failures.append("application_review_not_required")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "target_field_filled_count",
        "descriptor_value_assignment_count",
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

    if report.get("proposal_applied_count") != 1:
        failures.append("proposal_applied_count_wrong")
    if report.get("proposal_applied_as_unresolved_descriptor_object_count") != 1:
        failures.append("unresolved_descriptor_application_count_wrong")
    if report.get("accepted_descriptor_object_materialized_count") != 1:
        failures.append("accepted_descriptor_object_materialized_count_wrong")

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
    if metrics.get("semantic_acceptance_consumed_count") != 1:
        failures.append("metric_semantic_acceptance_consumed_wrong")
    if metrics.get("accepted_descriptor_object_materialized_count") != 1:
        failures.append("metric_accepted_descriptor_materialized_wrong")
    if metrics.get("proposal_applied_count") != 1:
        failures.append("metric_proposal_applied_wrong")
    if metrics.get("proposal_applied_as_unresolved_descriptor_object_count") != 1:
        failures.append("metric_unresolved_application_wrong")

    for key in [
        "target_field_filled_count",
        "descriptor_value_assignment_count",
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
    if terminal.get("stop_code") != "STOP_SEMANTICALLY_ACCEPTED_CANDIDATE_APPLICATION_COMPLETE_REQUIRES_SURFACE_REVIEW":
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

    patched = sources["patched_candidate"]
    typed_fields = sources["typed_decision_fields"]

    accepted = build_accepted_descriptor_object(patched, typed_fields)
    surface = build_applied_surface(accepted, sources)
    binding = build_application_binding(accepted, surface)
    limits = build_application_limits(accepted)
    review_packet = build_review_packet(accepted, surface)
    trace = build_transition_trace(accepted)
    report = build_report(accepted)

    write_json(ACCEPTED_DESCRIPTOR_OBJECT_PATH, accepted)
    write_json(APPLIED_EVIDENCE_SURFACE_PATH, surface)
    write_json(APPLICATION_BINDING_PATH, binding)
    write_json(APPLICATION_LIMITS_PATH, limits)
    write_json(APPLICATION_REVIEW_PACKET_PATH, review_packet)
    write_json(APPLICATION_TRANSITION_TRACE_PATH, trace)
    write_json(APPLICATION_REPORT_PATH, report)

    failures.extend(validate_application_outputs(
        accepted,
        surface,
        binding,
        limits,
        review_packet,
        trace,
        report,
    ))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "ACCEPTED_APPLICATION_0_PATCHED_REVIEW_CONSUMED": sources["patched_review_receipt"]["receipt_id"] == SOURCE_PATCHED_REVIEW_RECEIPT_ID and sources["patched_review_receipt"]["gate"] == "PASS",
        "ACCEPTED_APPLICATION_1_PATCHED_CANDIDATE_CONSUMED": patched["candidate_object_id"] == PATCHED_CANDIDATE_OBJECT_ID,
        "ACCEPTED_APPLICATION_2_SEMANTIC_ACCEPTANCE_CONSUMED": sources["patched_review_receipt"]["aggregate_metrics"]["semantic_acceptance_count"] == 1,
        "ACCEPTED_APPLICATION_3_SEPARATE_APPLICATION_AUTHORIZATION_CONSUMED": sources["patched_review_receipt"]["aggregate_metrics"]["application_authorized_for_separate_unit_count"] == 1,
        "ACCEPTED_APPLICATION_4_ACCEPTED_DESCRIPTOR_OBJECT_MATERIALIZED": accepted["object_status"] == "ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_OBJECT",
        "ACCEPTED_APPLICATION_5_DERIVED_SURFACE_EMITTED": surface["surface_status"] == "DERIVED_SURFACE_WITH_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_OBJECT",
        "ACCEPTED_APPLICATION_6_APPLICATION_BOUND_TO_DERIVED_SURFACE": binding["binding_status"] == "BOUND_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_TO_DERIVED_EVIDENCE_SURFACE",
        "ACCEPTED_APPLICATION_7_DESCRIPTOR_VALUES_REMAIN_UNRESOLVED": all(accepted["descriptor_values"][field]["value_is_assigned"] is False for field in REQUIRED_DESCRIPTOR_FIELDS),
        "ACCEPTED_APPLICATION_8_NO_TARGET_FIELD_FILLING_OR_VALUE_INVENTION": report["target_field_filled_count"] == 0 and report["descriptor_value_assignment_count"] == 0 and report["field_value_invention_count"] == 0,
        "ACCEPTED_APPLICATION_9_NO_TAXONOMY_ACTION": report["taxonomy_label_creation_count"] == 0 and report["taxonomy_upgrade_authorized_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "ACCEPTED_APPLICATION_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "ACCEPTED_APPLICATION_11_NO_R1000_RUN_OR_GROUP_OPEN": report["r1000_run_executed_count"] == 0 and report["pressure_group_opened_count"] == 0 and report["next_group_auto_opened_count"] == 0,
        "ACCEPTED_APPLICATION_12_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_SEMANTICALLY_ACCEPTED_CANDIDATE_APPLICATION_COMPLETE_REQUIRES_SURFACE_REVIEW",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        }

    aggregate_metrics = {
        "source_patched_review_receipt_id": SOURCE_PATCHED_REVIEW_RECEIPT_ID,
        "source_semantic_patch_receipt_id": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
        "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
        "accepted_descriptor_object_id": accepted["accepted_descriptor_object_id"],
        "derived_surface_id": surface["surface_id"],
        "semantic_acceptance_consumed_count": 1,
        "separate_application_authorization_consumed_count": 1,
        "accepted_descriptor_object_materialized_count": 1,
        "derived_surface_emitted_count": 1,
        "application_binding_emitted_count": 1,
        "application_review_packet_emitted_count": 1,
        "proposal_applied_count": 1,
        "proposal_applied_as_unresolved_descriptor_object_count": 1,
        "application_authorized_for_this_unit_count": 1,
        "target_field_filled_count": 0,
        "descriptor_value_assignment_count": 0,
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
        "semantic_acceptance_consumed": True,
        "separate_application_authorization_consumed": True,
        "accepted_descriptor_object_materialized": True,
        "derived_surface_emitted": True,
        "proposal_applied_as_unresolved_descriptor_object": True,
        "descriptor_values_assigned": False,
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
        "source_patched_review": SOURCE_PATCHED_REVIEW_RECEIPT_ID,
        "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
        "accepted_descriptor_object_id": accepted["accepted_descriptor_object_id"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "accepted_descriptor_object": rel(ACCEPTED_DESCRIPTOR_OBJECT_PATH),
        "derived_evidence_surface": rel(APPLIED_EVIDENCE_SURFACE_PATH),
        "application_binding": rel(APPLICATION_BINDING_PATH),
        "application_limits": rel(APPLICATION_LIMITS_PATH),
        "application_review_packet": rel(APPLICATION_REVIEW_PACKET_PATH),
        "application_transition_trace": rel(APPLICATION_TRANSITION_TRACE_PATH),
        "application_report": rel(APPLICATION_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "semantically_accepted_candidate_application_r1000_taxonomy_gap_receipt_v0",
        "receipt_type": "SEMANTICALLY_ACCEPTED_CANDIDATE_APPLICATION_R1000_TAXONOMY_GAP_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_patched_review_receipt_id": SOURCE_PATCHED_REVIEW_RECEIPT_ID,
        "source_semantic_patch_receipt_id": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
        "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
        "accepted_descriptor_object_id": accepted["accepted_descriptor_object_id"],
        "derived_surface_id": surface["surface_id"],
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "semantically_accepted_candidate_application_summary": {
            "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
            "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
            "accepted_descriptor_object_id": accepted["accepted_descriptor_object_id"],
            "derived_surface_id": surface["surface_id"],
            "application_result": "ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_OBJECT_MATERIALIZED",
            "proposal_applied_as_unresolved_descriptor_object": True,
            "descriptor_value_assignment": False,
            "target_field_filled": False,
            "taxonomy_action": False,
            "source_mutation": False,
            "r1000_run_executed": False,
            "application_review_required": True,
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "semantically_accepted_candidate_application_guards": guards,
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
    print(f"semantically_accepted_candidate_application_receipt_id={receipt_id}")
    print(f"semantically_accepted_candidate_application_receipt_path=data/semantically_accepted_candidate_application_r1000_taxonomy_gap_v0_receipts/{receipt_id}.json")
    print(f"accepted_descriptor_object_path=data/semantically_accepted_candidate_application_r1000_taxonomy_gap_v0/r1000_top_group_taxonomy_gap_accepted_typed_unresolved_descriptor_object.json")
    print(f"derived_evidence_surface_path=data/semantically_accepted_candidate_application_r1000_taxonomy_gap_v0/r1000_top_group_taxonomy_gap_evidence_surface_with_accepted_typed_unresolved_descriptor.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
