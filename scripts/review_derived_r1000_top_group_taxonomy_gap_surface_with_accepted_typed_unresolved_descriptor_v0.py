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

UNIT_ID = "REVIEW_DERIVED_R1000_TOP_GROUP_TAXONOMY_GAP_SURFACE_WITH_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_V0"
TARGET_UNIT_ID = "derived_r1000_taxonomy_gap_surface.accepted_typed_unresolved_descriptor.review.v0"

SOURCE_ACCEPTED_APP_RECEIPT_ID = "8d33789d"
SOURCE_PATCHED_REVIEW_RECEIPT_ID = "0fe3bb6a"
SOURCE_SEMANTIC_PATCH_RECEIPT_ID = "7d078710"
SOURCE_SEMANTIC_BARRIER_RECEIPT_ID = "4e6b09b2"
SOURCE_PROPOSAL_REVIEW_RECEIPT_ID = "a939b4a6"
SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID = "aa01c2a9"
SOURCE_PROPOSAL_LAYER_RECEIPT_ID = "6003c89c"
SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
SOURCE_CANDIDATE_OBJECT_ID = "ce1fe7fc"
PATCHED_CANDIDATE_OBJECT_ID = "a9ec669b"
ACCEPTED_DESCRIPTOR_OBJECT_ID = "86331324"
DERIVED_SURFACE_ID = "b0ee092b"

OUT_DIR = ROOT / "data" / "derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0"
RECEIPT_DIR = ROOT / "data" / "derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0_receipts"

SURFACE_REVIEW_FINDINGS_PATH = OUT_DIR / "derived_surface_accepted_descriptor_review_findings.json"
SURFACE_REVIEW_DECISION_PATH = OUT_DIR / "derived_surface_accepted_descriptor_review_decision.json"
SURFACE_REVIEW_CLOSURE_PACKET_PATH = OUT_DIR / "derived_surface_accepted_descriptor_review_closure_packet.json"
QUEUE_RETURN_PACKET_PATH = OUT_DIR / "derived_surface_accepted_descriptor_queue_return_packet.json"
SURFACE_REVIEW_TRANSITION_TRACE_PATH = OUT_DIR / "derived_surface_accepted_descriptor_review_transition_trace.json"
SURFACE_REVIEW_REPORT_PATH = OUT_DIR / "derived_surface_accepted_descriptor_review_report.json"

ACCEPTED_APP_RECEIPT_PATH = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_ACCEPTED_APP_RECEIPT_ID}.json"
ACCEPTED_DESCRIPTOR_OBJECT_PATH = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_accepted_typed_unresolved_descriptor_object.json"
DERIVED_EVIDENCE_SURFACE_PATH = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_evidence_surface_with_accepted_typed_unresolved_descriptor.json"
APPLICATION_BINDING_PATH = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0" / "semantically_accepted_candidate_application_binding.json"
APPLICATION_LIMITS_PATH = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0" / "semantically_accepted_candidate_application_limits.json"
APPLICATION_REVIEW_PACKET_PATH = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0" / "accepted_descriptor_application_review_packet.json"
APPLICATION_REPORT_PATH = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0" / "semantically_accepted_candidate_application_report.json"

PATCHED_REVIEW_RECEIPT_PATH = ROOT / "data" / "semantically_patched_candidate_review_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PATCHED_REVIEW_RECEIPT_ID}.json"
SEMANTIC_PATCH_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_SEMANTIC_PATCH_RECEIPT_ID}.json"
SEMANTIC_BARRIER_RECEIPT_PATH = ROOT / "data" / "candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_SEMANTIC_BARRIER_RECEIPT_ID}.json"
PROPOSAL_REVIEW_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PROPOSAL_REVIEW_RECEIPT_ID}.json"
PROPOSAL_APPLICATION_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID}.json"
PROPOSAL_LAYER_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0_receipts" / f"{SOURCE_PROPOSAL_LAYER_RECEIPT_ID}.json"
EXPECTED_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_RECEIPT_ID}.json"

SOURCE_FILES = [
    ACCEPTED_APP_RECEIPT_PATH,
    ACCEPTED_DESCRIPTOR_OBJECT_PATH,
    DERIVED_EVIDENCE_SURFACE_PATH,
    APPLICATION_BINDING_PATH,
    APPLICATION_LIMITS_PATH,
    APPLICATION_REVIEW_PACKET_PATH,
    APPLICATION_REPORT_PATH,
    PATCHED_REVIEW_RECEIPT_PATH,
    SEMANTIC_PATCH_RECEIPT_PATH,
    SEMANTIC_BARRIER_RECEIPT_PATH,
    PROPOSAL_REVIEW_RECEIPT_PATH,
    PROPOSAL_APPLICATION_RECEIPT_PATH,
    PROPOSAL_LAYER_RECEIPT_PATH,
    EXPECTED_LIMIT_RECEIPT_PATH,
]

REQUIRED_DESCRIPTOR_FIELDS = [
    "missing_label_identifier",
    "taxonomy_context_ref",
    "current_label_space_ref",
    "expected_label_space_ref",
]

HUMAN_DECISION = {
    "decision": "REVIEW_DERIVED_R1000_TOP_GROUP_TAXONOMY_GAP_SURFACE_WITH_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR",
    "scope": "review the derived evidence surface after accepted unresolved descriptor object materialization and mark it cleanly reviewed without applying values, taxonomy repair, source mutation, R1000 execution, or pressure-group opening",
    "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
    "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
    "derived_surface_id": DERIVED_SURFACE_ID,
    "authorized": [
        "read accepted descriptor object",
        "read derived evidence surface",
        "validate accepted descriptor object is present",
        "validate descriptor fields remain unresolved",
        "validate no literal null descriptor values are present",
        "validate negative claims and evidence limitations remain in force",
        "emit derived surface review decision",
        "emit queue return packet as candidate-only next handling",
        "stop without R1000 run or pressure group opening",
    ],
    "not_authorized": [
        "assigning descriptor values",
        "filling descriptor fields",
        "emitting null field values",
        "inventing values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "emitting taxonomy delta proposal",
        "mutating source rows",
        "mutating existing receipts",
        "running R1000",
        "opening another pressure group",
        "auto-reconciling the queue",
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
        "accepted_application_receipt": read_json(ACCEPTED_APP_RECEIPT_PATH),
        "accepted_descriptor_object": read_json(ACCEPTED_DESCRIPTOR_OBJECT_PATH),
        "derived_evidence_surface": read_json(DERIVED_EVIDENCE_SURFACE_PATH),
        "application_binding": read_json(APPLICATION_BINDING_PATH),
        "application_limits": read_json(APPLICATION_LIMITS_PATH),
        "application_review_packet": read_json(APPLICATION_REVIEW_PACKET_PATH),
        "application_report": read_json(APPLICATION_REPORT_PATH),
        "patched_review_receipt": read_json(PATCHED_REVIEW_RECEIPT_PATH),
        "semantic_patch_receipt": read_json(SEMANTIC_PATCH_RECEIPT_PATH),
        "semantic_barrier_receipt": read_json(SEMANTIC_BARRIER_RECEIPT_PATH),
        "proposal_review_receipt": read_json(PROPOSAL_REVIEW_RECEIPT_PATH),
        "proposal_application_receipt": read_json(PROPOSAL_APPLICATION_RECEIPT_PATH),
        "proposal_layer_receipt": read_json(PROPOSAL_LAYER_RECEIPT_PATH),
        "expected_limit_receipt": read_json(EXPECTED_LIMIT_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    app_receipt = sources["accepted_application_receipt"]
    accepted = sources["accepted_descriptor_object"]
    surface = sources["derived_evidence_surface"]
    binding = sources["application_binding"]
    limits = sources["application_limits"]
    review_packet = sources["application_review_packet"]

    if app_receipt.get("receipt_id") != SOURCE_ACCEPTED_APP_RECEIPT_ID:
        failures.append("accepted_application_receipt_id_wrong")
    if app_receipt.get("gate") != "PASS":
        failures.append("accepted_application_not_pass")
    if app_receipt.get("accepted_descriptor_object_id") != ACCEPTED_DESCRIPTOR_OBJECT_ID:
        failures.append("accepted_descriptor_id_wrong_in_receipt")
    if app_receipt.get("derived_surface_id") != DERIVED_SURFACE_ID:
        failures.append("derived_surface_id_wrong_in_receipt")
    if app_receipt.get("aggregate_metrics", {}).get("proposal_applied_as_unresolved_descriptor_object_count") != 1:
        failures.append("unresolved_descriptor_application_missing")
    if app_receipt.get("aggregate_metrics", {}).get("descriptor_value_assignment_count") != 0:
        failures.append("descriptor_value_assignment_already_occurred")
    if app_receipt.get("aggregate_metrics", {}).get("r1000_run_executed_count") != 0:
        failures.append("r1000_already_executed")

    if accepted.get("accepted_descriptor_object_id") != ACCEPTED_DESCRIPTOR_OBJECT_ID:
        failures.append("accepted_descriptor_object_id_wrong")
    if accepted.get("object_status") != "ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_OBJECT":
        failures.append("accepted_descriptor_object_status_wrong")
    if accepted.get("proposal_applied_as_unresolved_descriptor_object") is not True:
        failures.append("accepted_descriptor_not_marked_applied")
    if accepted.get("descriptor_value_assignment") is not False:
        failures.append("descriptor_value_assignment_true_in_object")
    if accepted.get("taxonomy_repair_authorized") is not False:
        failures.append("taxonomy_repair_authorized_in_object")

    if surface.get("surface_id") != DERIVED_SURFACE_ID:
        failures.append("derived_surface_id_wrong")
    if surface.get("accepted_descriptor_object_id") != ACCEPTED_DESCRIPTOR_OBJECT_ID:
        failures.append("derived_surface_not_bound_to_descriptor")
    if surface.get("surface_status") != "DERIVED_SURFACE_WITH_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_OBJECT":
        failures.append("derived_surface_status_wrong")

    if binding.get("accepted_descriptor_object_id") != ACCEPTED_DESCRIPTOR_OBJECT_ID:
        failures.append("binding_descriptor_id_wrong")
    if binding.get("derived_surface_id") != DERIVED_SURFACE_ID:
        failures.append("binding_surface_id_wrong")

    for key, value in limits.get("limits", {}).items():
        if value is not False:
            failures.append(f"limit_not_false:{key}:{value}")

    if review_packet.get("review_required") is not True:
        failures.append("application_review_packet_not_required")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def descriptor_fields_clean(accepted: Dict[str, Any]) -> Dict[str, Any]:
    results: Dict[str, Any] = {}
    descriptor_values = accepted.get("descriptor_values", {})
    for field in REQUIRED_DESCRIPTOR_FIELDS:
        field_obj = descriptor_values.get(field, {})
        results[field] = {
            "field_present": field in descriptor_values,
            "value_state_requires_schema_decision": field_obj.get("value_state") == "REQUIRES_SCHEMA_DECISION",
            "value_present_false": field_obj.get("value_present") is False,
            "value_is_assigned_false": field_obj.get("value_is_assigned") is False,
            "literal_value_key_absent": "value" not in field_obj,
            "null_resolution_forbidden": "set_null_as_value" in field_obj.get("forbidden_resolution", []),
            "invention_forbidden": "invent_value_without_source" in field_obj.get("forbidden_resolution", []),
        }
    return results

def build_findings(sources: Dict[str, Any]) -> Dict[str, Any]:
    accepted = sources["accepted_descriptor_object"]
    surface = sources["derived_evidence_surface"]
    limits = sources["application_limits"]

    field_results = descriptor_fields_clean(accepted)
    field_checks_pass = all(all(v is True for v in result.values()) for result in field_results.values())

    semantic_limitations = surface.get("semantic_limitations", {})
    limitation_checks = {
        "surface_descriptor_values_unassigned": semantic_limitations.get("descriptor_values_assigned") is False,
        "surface_taxonomy_repair_not_authorized": semantic_limitations.get("taxonomy_repair_authorized") is False,
        "surface_source_mutation_not_authorized": semantic_limitations.get("source_mutation_authorized") is False,
        "surface_global_absence_claim_not_authorized": semantic_limitations.get("global_absence_claim_authorized") is False,
        "surface_r1000_run_not_authorized": semantic_limitations.get("r1000_run_authorized") is False,
    }

    limit_checks = {key: value is False for key, value in limits.get("limits", {}).items()}

    findings = {
        "schema_version": "derived_surface_accepted_descriptor_review_findings_v0",
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "accepted_descriptor_object_present": accepted.get("accepted_descriptor_object_id") == ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_present": surface.get("surface_id") == DERIVED_SURFACE_ID,
        "surface_bound_to_descriptor": surface.get("accepted_descriptor_object_id") == ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "object_status_valid": accepted.get("object_status") == "ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_OBJECT",
        "surface_status_valid": surface.get("surface_status") == "DERIVED_SURFACE_WITH_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_OBJECT",
        "proposal_applied_as_unresolved_descriptor_object": accepted.get("proposal_applied_as_unresolved_descriptor_object") is True,
        "descriptor_value_assignment_absent": accepted.get("descriptor_value_assignment") is False,
        "taxonomy_repair_not_authorized": accepted.get("taxonomy_repair_authorized") is False,
        "source_mutation_not_authorized": accepted.get("source_mutation_authorized") is False,
        "descriptor_field_checks": field_results,
        "descriptor_fields_clean": field_checks_pass,
        "surface_semantic_limitation_checks": limitation_checks,
        "surface_semantic_limitations_clean": all(limitation_checks.values()),
        "application_limit_checks": limit_checks,
        "application_limits_clean": all(limit_checks.values()),
        "negative_claims_preserved": bool(accepted.get("negative_claims")),
        "evidence_basis_limitation_preserved": accepted.get("evidence_basis_strength", {}).get("supports") == "typed_unresolved_descriptor_proposal_only",
        "review_result": None,
        "typed_rejection_codes": [],
    }

    checks = [
        findings["accepted_descriptor_object_present"],
        findings["derived_surface_present"],
        findings["surface_bound_to_descriptor"],
        findings["object_status_valid"],
        findings["surface_status_valid"],
        findings["proposal_applied_as_unresolved_descriptor_object"],
        findings["descriptor_value_assignment_absent"],
        findings["taxonomy_repair_not_authorized"],
        findings["source_mutation_not_authorized"],
        findings["descriptor_fields_clean"],
        findings["surface_semantic_limitations_clean"],
        findings["application_limits_clean"],
        findings["negative_claims_preserved"],
        findings["evidence_basis_limitation_preserved"],
    ]

    if all(checks):
        findings["review_result"] = "ACCEPT_DERIVED_SURFACE_WITH_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR"
    else:
        findings["review_result"] = "REJECT_DERIVED_SURFACE_OR_REQUIRE_REPAIR"
        if not findings["descriptor_fields_clean"]:
            findings["typed_rejection_codes"].append("DESCRIPTOR_FIELDS_NOT_CLEAN")
        if not findings["surface_semantic_limitations_clean"]:
            findings["typed_rejection_codes"].append("SURFACE_LIMITATIONS_NOT_CLEAN")
        if not findings["application_limits_clean"]:
            findings["typed_rejection_codes"].append("APPLICATION_LIMITS_NOT_CLEAN")
        if not findings["surface_bound_to_descriptor"]:
            findings["typed_rejection_codes"].append("SURFACE_DESCRIPTOR_BINDING_BROKEN")
        if not findings["typed_rejection_codes"]:
            findings["typed_rejection_codes"].append("DERIVED_SURFACE_REVIEW_FAILED")

    return findings

def build_decision(findings: Dict[str, Any]) -> Dict[str, Any]:
    accepted = findings["review_result"] == "ACCEPT_DERIVED_SURFACE_WITH_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR"
    return {
        "schema_version": "derived_surface_accepted_descriptor_review_decision_v0",
        "review_decision_id": sha8({
            "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
            "derived_surface_id": DERIVED_SURFACE_ID,
            "review_result": findings["review_result"],
        }),
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "decision_status": findings["review_result"],
        "surface_review_acceptance": accepted,
        "surface_review_rejection": not accepted,
        "typed_rejection_codes": findings["typed_rejection_codes"],
        "application_surface_accepted": accepted,
        "queue_return_candidate_allowed": accepted,
        "queue_reconciliation_authorized_in_this_unit": False,
        "next_group_open_authorized_in_this_unit": False,
        "r1000_run_authorized_in_this_unit": False,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_DERIVED_SURFACE_ACCEPTED_DESCRIPTOR_REVIEW_COMPLETE_QUEUE_RETURN_CANDIDATE",
            "next_command_goal": None,
        } if accepted else {
            "type": "STOP",
            "stop_code": "STOP_DERIVED_SURFACE_REVIEW_FAILED_REPAIR_REQUIRED",
            "next_command_goal": None,
        },
    }

def build_closure_packet(decision: Dict[str, Any]) -> Dict[str, Any]:
    accepted = decision["surface_review_acceptance"] is True
    return {
        "schema_version": "derived_surface_accepted_descriptor_review_closure_packet_v0",
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "closure_status": "DERIVED_SURFACE_REVIEW_ACCEPTED" if accepted else "DERIVED_SURFACE_REVIEW_NOT_ACCEPTED",
        "closed_local_branch": accepted,
        "closed_scope": "accepted typed unresolved descriptor object materialization branch only",
        "not_closed": [
            "descriptor values",
            "taxonomy repair",
            "source content absence beyond explicit tracked source chain",
            "future taxonomy upgrade decisions",
            "unrelated pressure groups",
        ],
        "preserved_open_decisions": [
            "missing_label_identifier remains REQUIRES_SCHEMA_DECISION",
            "taxonomy_context_ref remains REQUIRES_SCHEMA_DECISION",
            "current_label_space_ref remains REQUIRES_SCHEMA_DECISION",
            "expected_label_space_ref remains REQUIRES_SCHEMA_DECISION",
        ],
    }

def build_queue_return_packet(decision: Dict[str, Any]) -> Dict[str, Any]:
    accepted = decision["surface_review_acceptance"] is True
    return {
        "schema_version": "derived_surface_accepted_descriptor_queue_return_packet_v0",
        "packet_status": "CANDIDATE_ONLY_NOT_EXECUTED",
        "return_to_queue_allowed": accepted,
        "queue_reconciliation_authorized_in_this_unit": False,
        "next_group_auto_opened": False,
        "recommended_next_handling": "RECONCILE_R1000_PRESSURE_QUEUE_AFTER_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_SURFACE_REVIEW_V0" if accepted else "REPAIR_DERIVED_SURFACE_ACCEPTED_DESCRIPTOR_REVIEW_FAILURE_V0",
        "reason": "derived surface review accepted; queue may be reconciled by a separate authorized unit" if accepted else "derived surface review failed; repair required before queue return",
    }

def build_transition_trace(decision: Dict[str, Any]) -> Dict[str, Any]:
    accepted = decision["surface_review_acceptance"] is True
    return {
        "schema_version": "derived_surface_accepted_descriptor_review_transition_trace_v0",
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "trace": [
            {
                "step": "consume_accepted_application",
                "question": "accepted descriptor object and derived surface exist",
                "answer": True,
                "taken": "inspect_descriptor_fields",
            },
            {
                "step": "inspect_descriptor_fields",
                "question": "descriptor fields remain unresolved without literal null values",
                "answer": accepted,
                "taken": "inspect_surface_limitations" if accepted else "STOP_DERIVED_SURFACE_REVIEW_FAILED_REPAIR_REQUIRED",
            },
            {
                "step": "inspect_surface_limitations",
                "question": "surface preserves no taxonomy, source, runtime, or global absence authorization",
                "answer": accepted,
                "taken": "emit_review_decision" if accepted else "STOP_DERIVED_SURFACE_REVIEW_FAILED_REPAIR_REQUIRED",
            },
            {
                "step": "emit_review_decision",
                "question": "queue reconciliation happens in this unit",
                "answer": False,
                "taken": decision["terminal"]["stop_code"],
            },
        ],
        "terminal": decision["terminal"],
    }

def build_report(decision: Dict[str, Any], findings: Dict[str, Any]) -> Dict[str, Any]:
    accepted = decision["surface_review_acceptance"] is True
    return {
        "schema_version": "derived_surface_accepted_descriptor_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "derived_surface_reviewed_count": 1,
        "accepted_descriptor_object_reviewed_count": 1,
        "derived_surface_review_decision_emitted_count": 1,
        "derived_surface_review_acceptance_count": 1 if accepted else 0,
        "derived_surface_review_rejection_count": 0 if accepted else 1,
        "descriptor_fields_clean_count": 1 if findings["descriptor_fields_clean"] else 0,
        "surface_semantic_limitations_clean_count": 1 if findings["surface_semantic_limitations_clean"] else 0,
        "application_limits_clean_count": 1 if findings["application_limits_clean"] else 0,
        "closure_packet_emitted_count": 1,
        "queue_return_packet_emitted_count": 1,
        "queue_reconciliation_authorized_in_this_unit_count": 0,
        "queue_reconciled_count": 0,
        "proposal_applied_count": 0,
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
        "recommended_next_handling": "RECONCILE_R1000_PRESSURE_QUEUE_AFTER_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR_SURFACE_REVIEW_V0" if accepted else "REPAIR_DERIVED_SURFACE_ACCEPTED_DESCRIPTOR_REVIEW_FAILURE_V0",
    }

def validate_outputs(
    findings: Dict[str, Any],
    decision: Dict[str, Any],
    closure: Dict[str, Any],
    queue_packet: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if findings.get("review_result") != "ACCEPT_DERIVED_SURFACE_WITH_ACCEPTED_TYPED_UNRESOLVED_DESCRIPTOR":
        failures.append(f"review_result_wrong:{findings.get('review_result')}")
    if findings.get("descriptor_fields_clean") is not True:
        failures.append("descriptor_fields_not_clean")
    if findings.get("surface_semantic_limitations_clean") is not True:
        failures.append("surface_limitations_not_clean")
    if findings.get("application_limits_clean") is not True:
        failures.append("application_limits_not_clean")
    if decision.get("surface_review_acceptance") is not True:
        failures.append("surface_review_not_accepted")
    if decision.get("queue_reconciliation_authorized_in_this_unit") is not False:
        failures.append("queue_reconciliation_authorized_in_review_unit")
    if decision.get("next_group_open_authorized_in_this_unit") is not False:
        failures.append("next_group_open_authorized_in_review_unit")
    if closure.get("closed_local_branch") is not True:
        failures.append("closure_packet_not_closed")
    if queue_packet.get("packet_status") != "CANDIDATE_ONLY_NOT_EXECUTED":
        failures.append("queue_return_packet_not_candidate_only")
    if queue_packet.get("queue_reconciliation_authorized_in_this_unit") is not False:
        failures.append("queue_packet_authorizes_reconciliation")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "queue_reconciliation_authorized_in_this_unit_count",
        "queue_reconciled_count",
        "proposal_applied_count",
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

    if report.get("derived_surface_reviewed_count") != 1:
        failures.append("derived_surface_reviewed_count_wrong")
    if report.get("derived_surface_review_acceptance_count") != 1:
        failures.append("derived_surface_review_acceptance_count_wrong")
    if report.get("queue_return_packet_emitted_count") != 1:
        failures.append("queue_return_packet_count_wrong")

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
    if metrics.get("derived_surface_reviewed_count") != 1:
        failures.append("metric_surface_reviewed_wrong")
    if metrics.get("derived_surface_review_acceptance_count") != 1:
        failures.append("metric_surface_acceptance_wrong")
    if metrics.get("queue_return_packet_emitted_count") != 1:
        failures.append("metric_queue_packet_wrong")

    for key in [
        "queue_reconciliation_authorized_in_this_unit_count",
        "queue_reconciled_count",
        "proposal_applied_count",
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
    if terminal.get("stop_code") != "STOP_DERIVED_SURFACE_ACCEPTED_DESCRIPTOR_REVIEW_COMPLETE_QUEUE_RETURN_CANDIDATE":
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

    findings = build_findings(sources)
    decision = build_decision(findings)
    closure = build_closure_packet(decision)
    queue_packet = build_queue_return_packet(decision)
    trace = build_transition_trace(decision)
    report = build_report(decision, findings)

    write_json(SURFACE_REVIEW_FINDINGS_PATH, findings)
    write_json(SURFACE_REVIEW_DECISION_PATH, decision)
    write_json(SURFACE_REVIEW_CLOSURE_PACKET_PATH, closure)
    write_json(QUEUE_RETURN_PACKET_PATH, queue_packet)
    write_json(SURFACE_REVIEW_TRANSITION_TRACE_PATH, trace)
    write_json(SURFACE_REVIEW_REPORT_PATH, report)

    failures.extend(validate_outputs(findings, decision, closure, queue_packet, trace, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "DERIVED_SURFACE_REVIEW_0_ACCEPTED_APPLICATION_CONSUMED": sources["accepted_application_receipt"]["receipt_id"] == SOURCE_ACCEPTED_APP_RECEIPT_ID and sources["accepted_application_receipt"]["gate"] == "PASS",
        "DERIVED_SURFACE_REVIEW_1_ACCEPTED_DESCRIPTOR_OBJECT_PRESENT": findings["accepted_descriptor_object_present"],
        "DERIVED_SURFACE_REVIEW_2_DERIVED_SURFACE_PRESENT": findings["derived_surface_present"],
        "DERIVED_SURFACE_REVIEW_3_SURFACE_BOUND_TO_DESCRIPTOR": findings["surface_bound_to_descriptor"],
        "DERIVED_SURFACE_REVIEW_4_DESCRIPTOR_FIELDS_CLEAN": findings["descriptor_fields_clean"],
        "DERIVED_SURFACE_REVIEW_5_SURFACE_LIMITATIONS_CLEAN": findings["surface_semantic_limitations_clean"],
        "DERIVED_SURFACE_REVIEW_6_APPLICATION_LIMITS_CLEAN": findings["application_limits_clean"],
        "DERIVED_SURFACE_REVIEW_7_REVIEW_ACCEPTED": decision["surface_review_acceptance"] is True,
        "DERIVED_SURFACE_REVIEW_8_QUEUE_RETURN_PACKET_CANDIDATE_ONLY": queue_packet["packet_status"] == "CANDIDATE_ONLY_NOT_EXECUTED" and queue_packet["queue_reconciliation_authorized_in_this_unit"] is False,
        "DERIVED_SURFACE_REVIEW_9_NO_FIELD_VALUE_OR_TAXONOMY_ACTION": report["target_field_filled_count"] == 0 and report["descriptor_value_assignment_count"] == 0 and report["field_value_invention_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "DERIVED_SURFACE_REVIEW_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "DERIVED_SURFACE_REVIEW_11_NO_R1000_RUN_QUEUE_RECONCILE_OR_GROUP_OPEN": report["r1000_run_executed_count"] == 0 and report["queue_reconciled_count"] == 0 and report["pressure_group_opened_count"] == 0 and report["next_group_auto_opened_count"] == 0,
        "DERIVED_SURFACE_REVIEW_12_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and decision["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_DERIVED_SURFACE_ACCEPTED_DESCRIPTOR_REVIEW_COMPLETE_QUEUE_RETURN_CANDIDATE",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        }

    aggregate_metrics = {
        "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
        "source_patched_review_receipt_id": SOURCE_PATCHED_REVIEW_RECEIPT_ID,
        "source_semantic_patch_receipt_id": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
        "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "derived_surface_reviewed_count": 1,
        "accepted_descriptor_object_reviewed_count": 1,
        "derived_surface_review_decision_emitted_count": 1,
        "derived_surface_review_acceptance_count": report["derived_surface_review_acceptance_count"],
        "derived_surface_review_rejection_count": report["derived_surface_review_rejection_count"],
        "descriptor_fields_clean_count": report["descriptor_fields_clean_count"],
        "surface_semantic_limitations_clean_count": report["surface_semantic_limitations_clean_count"],
        "application_limits_clean_count": report["application_limits_clean_count"],
        "closure_packet_emitted_count": 1,
        "queue_return_packet_emitted_count": 1,
        "queue_reconciliation_authorized_in_this_unit_count": 0,
        "queue_reconciled_count": 0,
        "proposal_applied_count": 0,
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
        "accepted_application_consumed": True,
        "accepted_descriptor_object_present": findings["accepted_descriptor_object_present"],
        "derived_surface_present": findings["derived_surface_present"],
        "surface_bound_to_descriptor": findings["surface_bound_to_descriptor"],
        "descriptor_fields_clean": findings["descriptor_fields_clean"],
        "surface_semantic_limitations_clean": findings["surface_semantic_limitations_clean"],
        "application_limits_clean": findings["application_limits_clean"],
        "derived_surface_review_accepted": decision["surface_review_acceptance"],
        "queue_return_packet_candidate_only": queue_packet["packet_status"] == "CANDIDATE_ONLY_NOT_EXECUTED",
        "queue_reconciliation_authorized_in_this_unit": False,
        "queue_reconciled": False,
        "target_field_filled": False,
        "descriptor_value_assigned": False,
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
        "source_accepted_application": SOURCE_ACCEPTED_APP_RECEIPT_ID,
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "review_result": findings["review_result"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "surface_review_findings": rel(SURFACE_REVIEW_FINDINGS_PATH),
        "surface_review_decision": rel(SURFACE_REVIEW_DECISION_PATH),
        "surface_review_closure_packet": rel(SURFACE_REVIEW_CLOSURE_PACKET_PATH),
        "queue_return_packet": rel(QUEUE_RETURN_PACKET_PATH),
        "surface_review_transition_trace": rel(SURFACE_REVIEW_TRANSITION_TRACE_PATH),
        "surface_review_report": rel(SURFACE_REVIEW_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_receipt_v0",
        "receipt_type": "DERIVED_R1000_TAXONOMY_GAP_SURFACE_ACCEPTED_DESCRIPTOR_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
        "source_patched_review_receipt_id": SOURCE_PATCHED_REVIEW_RECEIPT_ID,
        "source_semantic_patch_receipt_id": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
        "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
        "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
        "derived_surface_id": DERIVED_SURFACE_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "derived_surface_accepted_descriptor_review_summary": {
            "accepted_descriptor_object_id": ACCEPTED_DESCRIPTOR_OBJECT_ID,
            "derived_surface_id": DERIVED_SURFACE_ID,
            "review_result": findings["review_result"],
            "surface_review_acceptance": decision["surface_review_acceptance"],
            "descriptor_fields_clean": findings["descriptor_fields_clean"],
            "surface_semantic_limitations_clean": findings["surface_semantic_limitations_clean"],
            "application_limits_clean": findings["application_limits_clean"],
            "queue_return_packet_status": queue_packet["packet_status"],
            "queue_reconciliation_authorized_in_this_unit": False,
            "queue_reconciled": False,
            "r1000_run_executed": False,
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "derived_surface_accepted_descriptor_review_guards": guards,
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
    print(f"derived_surface_review_receipt_id={receipt_id}")
    print(f"derived_surface_review_receipt_path=data/derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0_receipts/{receipt_id}.json")
    print(f"derived_surface_review_decision_path=data/derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0/derived_surface_accepted_descriptor_review_decision.json")
    print(f"queue_return_packet_path=data/derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0/derived_surface_accepted_descriptor_queue_return_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
