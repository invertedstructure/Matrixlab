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

UNIT_ID = "REVIEW_SEMANTICALLY_PATCHED_CANDIDATE_MISSING_OBJECT_PROPOSAL_FOR_R1000_TOP_GROUP_TAXONOMY_GAP_V0"
TARGET_UNIT_ID = "semantically_patched_candidate_missing_object_proposal_review.r1000_taxonomy_gap.v0"

SOURCE_SEMANTIC_PATCH_RECEIPT_ID = "7d078710"
SOURCE_SEMANTIC_BARRIER_RECEIPT_ID = "4e6b09b2"
SOURCE_PROPOSAL_REVIEW_RECEIPT_ID = "a939b4a6"
SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID = "aa01c2a9"
SOURCE_PROPOSAL_LAYER_RECEIPT_ID = "6003c89c"
SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
SOURCE_CANDIDATE_OBJECT_ID = "ce1fe7fc"
PATCHED_CANDIDATE_OBJECT_ID = "a9ec669b"

OUT_DIR = ROOT / "data" / "semantically_patched_candidate_review_r1000_taxonomy_gap_v0"
RECEIPT_DIR = ROOT / "data" / "semantically_patched_candidate_review_r1000_taxonomy_gap_v0_receipts"

PATCHED_REVIEW_FINDINGS_PATH = OUT_DIR / "semantically_patched_candidate_review_findings.json"
PATCHED_REVIEW_DECISION_PATH = OUT_DIR / "semantically_patched_candidate_review_decision.json"
PATCHED_APPLICATION_AUTHORIZATION_PACKET_PATH = OUT_DIR / "semantically_patched_candidate_application_authorization_packet.json"
PATCHED_REVIEW_TRANSITION_TRACE_PATH = OUT_DIR / "semantically_patched_candidate_review_transition_trace.json"
PATCHED_REVIEW_REPORT_PATH = OUT_DIR / "semantically_patched_candidate_review_report.json"

SEMANTIC_PATCH_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_SEMANTIC_PATCH_RECEIPT_ID}.json"
IN_CHAT_SEMANTIC_REVIEW_RESULT_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0" / "in_chat_semantic_review_result.json"
PATCH_REQUIREMENTS_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0" / "candidate_semantic_patch_requirements.json"
PATCHED_CANDIDATE_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_semantically_patched_candidate_missing_object_proposal.json"
PATCH_DELTA_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0" / "candidate_semantic_patch_delta.json"
PATCHED_CANDIDATE_REVIEW_PACKET_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0" / "patched_candidate_review_packet.json"
PATCHED_CANDIDATE_BLOCKER_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0" / "patched_candidate_application_blocker_packet.json"
SEMANTIC_PATCH_REPORT_PATH = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0" / "semantic_patch_report.json"

SEMANTIC_BARRIER_RECEIPT_PATH = ROOT / "data" / "candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_SEMANTIC_BARRIER_RECEIPT_ID}.json"
PROPOSAL_REVIEW_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PROPOSAL_REVIEW_RECEIPT_ID}.json"
PROPOSAL_APPLICATION_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID}.json"
PROPOSAL_LAYER_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0_receipts" / f"{SOURCE_PROPOSAL_LAYER_RECEIPT_ID}.json"
EXPECTED_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_RECEIPT_ID}.json"

SOURCE_FILES = [
    SEMANTIC_PATCH_RECEIPT_PATH,
    IN_CHAT_SEMANTIC_REVIEW_RESULT_PATH,
    PATCH_REQUIREMENTS_PATH,
    PATCHED_CANDIDATE_PATH,
    PATCH_DELTA_PATH,
    PATCHED_CANDIDATE_REVIEW_PACKET_PATH,
    PATCHED_CANDIDATE_BLOCKER_PATH,
    SEMANTIC_PATCH_REPORT_PATH,
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

REQUIRED_NEGATIVE_CLAIMS = [
    "does_not_identify_missing_label_identifier",
    "does_not_identify_taxonomy_context_ref",
    "does_not_identify_current_label_space_ref",
    "does_not_identify_expected_label_space_ref",
    "does_not_authorize_taxonomy_repair",
    "does_not_prove_source_content_globally_absent",
    "does_not_authorize_application",
    "does_not_claim_correctness_of_descriptor_values",
]

AUTHORIZED_APPLICATION_UNIT = "APPLY_SEMANTICALLY_ACCEPTED_CANDIDATE_MISSING_OBJECT_PROPOSAL_TO_R1000_TOP_GROUP_TAXONOMY_GAP_EVIDENCE_SURFACE_V0"

HUMAN_DECISION = {
    "decision": "REVIEW_SEMANTICALLY_PATCHED_CANDIDATE_MISSING_OBJECT_PROPOSAL_FOR_R1000_TOP_GROUP_TAXONOMY_GAP",
    "scope": "review the semantically patched candidate and, if the patch fixed the semantic overclaim, authorize only a later separate application unit without applying anything here",
    "source_semantic_patch_receipt_id": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
    "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
    "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
    "authorized": [
        "read semantically patched candidate",
        "validate weakened semantic claims",
        "validate unresolved descriptor fields are preserved",
        "validate evidence basis does not support descriptor values",
        "validate negative claims block value inference",
        "emit patched candidate review decision",
        "authorize only a later separate application unit if accepted",
    ],
    "not_authorized": [
        "applying the patched candidate in this unit",
        "filling missing descriptor fields",
        "assigning descriptor values",
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
        "semantic_patch_receipt": read_json(SEMANTIC_PATCH_RECEIPT_PATH),
        "in_chat_semantic_review_result": read_json(IN_CHAT_SEMANTIC_REVIEW_RESULT_PATH),
        "patch_requirements": read_json(PATCH_REQUIREMENTS_PATH),
        "patched_candidate": read_json(PATCHED_CANDIDATE_PATH),
        "patch_delta": read_json(PATCH_DELTA_PATH),
        "patched_candidate_review_packet": read_json(PATCHED_CANDIDATE_REVIEW_PACKET_PATH),
        "patched_candidate_blocker": read_json(PATCHED_CANDIDATE_BLOCKER_PATH),
        "semantic_patch_report": read_json(SEMANTIC_PATCH_REPORT_PATH),
        "semantic_barrier_receipt": read_json(SEMANTIC_BARRIER_RECEIPT_PATH),
        "proposal_review_receipt": read_json(PROPOSAL_REVIEW_RECEIPT_PATH),
        "proposal_application_receipt": read_json(PROPOSAL_APPLICATION_RECEIPT_PATH),
        "proposal_layer_receipt": read_json(PROPOSAL_LAYER_RECEIPT_PATH),
        "expected_limit_receipt": read_json(EXPECTED_LIMIT_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    patch_receipt = sources["semantic_patch_receipt"]
    patched = sources["patched_candidate"]
    review_result = sources["in_chat_semantic_review_result"]
    blocker = sources["patched_candidate_blocker"]

    if patch_receipt.get("receipt_id") != SOURCE_SEMANTIC_PATCH_RECEIPT_ID:
        failures.append("semantic_patch_receipt_id_wrong")
    if patch_receipt.get("gate") != "PASS":
        failures.append("semantic_patch_not_pass")
    if patch_receipt.get("patched_candidate_object_id") != PATCHED_CANDIDATE_OBJECT_ID:
        failures.append("patched_candidate_id_wrong_in_receipt")
    if patch_receipt.get("aggregate_metrics", {}).get("patched_candidate_review_required_count") != 1:
        failures.append("patched_candidate_review_not_required")
    if patch_receipt.get("aggregate_metrics", {}).get("application_authorized_count") != 0:
        failures.append("application_already_authorized_by_patch")
    if patch_receipt.get("aggregate_metrics", {}).get("proposal_applied_count") != 0:
        failures.append("proposal_already_applied_by_patch")

    if patched.get("candidate_object_id") != PATCHED_CANDIDATE_OBJECT_ID:
        failures.append("patched_candidate_object_id_wrong")
    if patched.get("source_candidate_object_id") != SOURCE_CANDIDATE_OBJECT_ID:
        failures.append("patched_source_candidate_wrong")
    if patched.get("object_status") != "SEMANTICALLY_PATCHED_CANDIDATE_MISSING_OBJECT_PROPOSAL":
        failures.append("patched_candidate_status_wrong")
    if patched.get("application_authorized") is not False:
        failures.append("patched_candidate_self_authorizes_application")

    if review_result.get("semantic_classification") != "ACCEPTABLE_ONLY_AFTER_EDITS":
        failures.append("source_semantic_review_classification_wrong")
    if review_result.get("application_authorized") is not False:
        failures.append("source_semantic_review_authorized_application")

    if blocker.get("application_blocked") is not True:
        failures.append("patched_candidate_blocker_not_blocking")
    if blocker.get("application_authorized") is not False:
        failures.append("patched_candidate_blocker_authorizes_application")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_findings(patched: Dict[str, Any], delta: Dict[str, Any]) -> Dict[str, Any]:
    negative_claims = patched.get("negative_claims", [])
    evidence_strength = patched.get("evidence_basis_strength", {})
    findings = {
        "schema_version": "semantically_patched_candidate_review_findings_v0",
        "patched_candidate_object_id": patched.get("candidate_object_id"),
        "source_candidate_object_id": patched.get("source_candidate_object_id"),
        "object_status_valid": patched.get("object_status") == "SEMANTICALLY_PATCHED_CANDIDATE_MISSING_OBJECT_PROPOSAL",
        "semantic_status_valid": patched.get("semantic_status") == "TYPED_UNRESOLVED_DESCRIPTOR_PROPOSAL",
        "descriptor_status_valid": patched.get("descriptor_status") == "CANDIDATE_UNRESOLVED_DESCRIPTOR_NOT_VALUE_DESCRIPTOR",
        "application_not_authorized": patched.get("application_authorized") is False,
        "required_descriptor_fields_preserved": patched.get("required_object_fields") == REQUIRED_DESCRIPTOR_FIELDS,
        "unknown_decision_fields_preserved": delta.get("unknown_decision_fields_preserved") is True,
        "source_evidence_refs_preserved": delta.get("source_evidence_refs_preserved") is True,
        "negative_claims_complete": all(claim in negative_claims for claim in REQUIRED_NEGATIVE_CLAIMS),
        "evidence_basis_limited_to_unresolved_descriptor": evidence_strength.get("supports") == "typed_unresolved_descriptor_proposal_only",
        "evidence_basis_does_not_support_values": all(item in evidence_strength.get("does_not_support", []) for item in [
            "descriptor_value_assignment",
            "missing_label_identity",
            "taxonomy_context_identity",
            "current_label_space_identity",
            "expected_label_space_identity",
            "taxonomy_label_creation",
            "source_mutation",
        ]),
        "alternatives_present": bool(patched.get("alternative_shapes_considered")),
        "risk_if_wrong_present": bool(patched.get("risk_if_wrong")),
        "correctness_claims_present": False,
        "boundary_crossing_present": False,
    }

    candidate_text = json.dumps(patched, sort_keys=True)
    forbidden_literals = [
        '"application_authorized": true',
        '"descriptor_value_assignment"',
        '"taxonomy_label_created": true',
        '"source_mutated": true',
    ]
    findings["forbidden_literals_detected"] = [
        literal for literal in forbidden_literals
        if literal in candidate_text and literal != '"descriptor_value_assignment"'
    ]

    checks = [
        findings["object_status_valid"],
        findings["semantic_status_valid"],
        findings["descriptor_status_valid"],
        findings["application_not_authorized"],
        findings["required_descriptor_fields_preserved"],
        findings["unknown_decision_fields_preserved"],
        findings["source_evidence_refs_preserved"],
        findings["negative_claims_complete"],
        findings["evidence_basis_limited_to_unresolved_descriptor"],
        findings["evidence_basis_does_not_support_values"],
        findings["alternatives_present"],
        findings["risk_if_wrong_present"],
        not findings["correctness_claims_present"],
        not findings["boundary_crossing_present"],
        len(findings["forbidden_literals_detected"]) == 0,
    ]

    findings["review_result"] = "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION" if all(checks) else "REJECT_OR_REPATCH_PATCHED_CANDIDATE"
    findings["typed_rejection_codes"] = []
    if findings["review_result"] != "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION":
        if not findings["semantic_status_valid"] or not findings["descriptor_status_valid"]:
            findings["typed_rejection_codes"].append("SEMANTIC_CLAIM_TOO_STRONG")
        if not findings["negative_claims_complete"]:
            findings["typed_rejection_codes"].append("NEGATIVE_CLAIMS_INCOMPLETE")
        if not findings["evidence_basis_limited_to_unresolved_descriptor"]:
            findings["typed_rejection_codes"].append("EVIDENCE_BASIS_TOO_STRONG")
        if not findings["unknown_decision_fields_preserved"]:
            findings["typed_rejection_codes"].append("UNRESOLVED_FIELDS_NOT_PRESERVED")
        if not findings["typed_rejection_codes"]:
            findings["typed_rejection_codes"].append("PATCH_REVIEW_FAILED")
    return findings

def build_review_decision(patched: Dict[str, Any], findings: Dict[str, Any]) -> Dict[str, Any]:
    accepted = findings["review_result"] == "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION"
    return {
        "schema_version": "semantically_patched_candidate_review_decision_v0",
        "review_decision_id": sha8({
            "patched_candidate_object_id": patched["candidate_object_id"],
            "review_result": findings["review_result"],
            "source_semantic_patch_receipt": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
        }),
        "source_candidate_object_id": patched["source_candidate_object_id"],
        "patched_candidate_object_id": patched["candidate_object_id"],
        "patched_candidate_ref": rel(PATCHED_CANDIDATE_PATH),
        "decision_status": "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION" if accepted else "REJECT_OR_REPATCH_PATCHED_CANDIDATE",
        "decision_basis": {
            "semantic_status_valid": findings["semantic_status_valid"],
            "descriptor_status_valid": findings["descriptor_status_valid"],
            "negative_claims_complete": findings["negative_claims_complete"],
            "evidence_basis_limited_to_unresolved_descriptor": findings["evidence_basis_limited_to_unresolved_descriptor"],
            "evidence_basis_does_not_support_values": findings["evidence_basis_does_not_support_values"],
            "unknown_decision_fields_preserved": findings["unknown_decision_fields_preserved"],
            "source_evidence_refs_preserved": findings["source_evidence_refs_preserved"],
            "application_not_authorized_in_candidate": findings["application_not_authorized"],
        },
        "typed_rejection_codes": findings["typed_rejection_codes"],
        "semantic_acceptance": accepted,
        "application_authorized_for_separate_unit": accepted,
        "application_authorized_in_this_unit": False,
        "authorized_application_unit": AUTHORIZED_APPLICATION_UNIT if accepted else None,
        "authorized_application_scope": {
            "may_materialize": "typed unresolved descriptor proposal object",
            "must_preserve": [
                "descriptor values unresolved",
                "typed unresolved decision fields",
                "evidence basis limitation",
                "negative claims",
                "no taxonomy repair authorization",
            ],
            "must_not": [
                "fill descriptor values",
                "invent values",
                "create labels",
                "mutate source rows",
                "mutate existing receipts",
            ],
        } if accepted else None,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_PATCHED_CANDIDATE_ACCEPTED_FOR_SEPARATE_APPLICATION_UNIT" if accepted else "STOP_PATCHED_CANDIDATE_REQUIRES_REPATCH_OR_REJECTION",
            "next_command_goal": None,
        },
    }

def build_authorization_packet(review_decision: Dict[str, Any]) -> Dict[str, Any]:
    accepted = review_decision["decision_status"] == "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION"
    return {
        "schema_version": "semantically_patched_candidate_application_authorization_packet_v0",
        "authorization_packet_id": sha8({
            "review_decision_id": review_decision["review_decision_id"],
            "patched_candidate_object_id": review_decision["patched_candidate_object_id"],
        }),
        "source_candidate_object_id": review_decision["source_candidate_object_id"],
        "patched_candidate_object_id": review_decision["patched_candidate_object_id"],
        "review_decision_id": review_decision["review_decision_id"],
        "review_decision_ref": rel(PATCHED_REVIEW_DECISION_PATH),
        "semantic_acceptance": accepted,
        "application_authorized_for_separate_unit": accepted,
        "application_authorized_in_this_unit": False,
        "authorized_application_unit": AUTHORIZED_APPLICATION_UNIT if accepted else None,
        "authorized_effect": [
            "materialize semantically patched typed unresolved descriptor proposal object",
            "preserve descriptor values unresolved",
            "preserve typed unresolved decision fields",
            "preserve no taxonomy repair authorization",
            "emit accepted application receipt",
            "stop for downstream review",
        ] if accepted else [],
        "still_forbidden": [
            "descriptor value assignment",
            "missing_label_identifier invention",
            "taxonomy_context_ref invention",
            "current_label_space_ref invention",
            "expected_label_space_ref invention",
            "taxonomy label creation",
            "taxonomy upgrade",
            "source mutation",
            "existing receipt mutation",
            "R1000 run inside review unit",
            "pressure group opening inside review unit",
        ],
    }

def build_transition_trace(review_decision: Dict[str, Any], findings: Dict[str, Any]) -> Dict[str, Any]:
    accepted = review_decision["decision_status"] == "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION"
    return {
        "schema_version": "semantically_patched_candidate_review_transition_trace_v0",
        "patched_candidate_object_id": review_decision["patched_candidate_object_id"],
        "trace": [
            {
                "step": "consume_semantic_patch",
                "question": "patched_candidate_exists_and_requires_review",
                "answer": True,
                "taken": "inspect_weakened_semantic_claims",
            },
            {
                "step": "inspect_weakened_semantic_claims",
                "question": "semantic_status_and_descriptor_status_are_weakened",
                "answer": findings["semantic_status_valid"] and findings["descriptor_status_valid"],
                "taken": "inspect_negative_claims" if findings["semantic_status_valid"] and findings["descriptor_status_valid"] else "REJECT_OR_REPATCH_PATCHED_CANDIDATE",
            },
            {
                "step": "inspect_negative_claims",
                "question": "negative_claims_block_value_and_authorization_inference",
                "answer": findings["negative_claims_complete"],
                "taken": "inspect_evidence_basis" if findings["negative_claims_complete"] else "REJECT_OR_REPATCH_PATCHED_CANDIDATE",
            },
            {
                "step": "inspect_evidence_basis",
                "question": "evidence_basis_limited_to_unresolved_descriptor_proposal",
                "answer": findings["evidence_basis_limited_to_unresolved_descriptor"],
                "taken": "emit_review_decision" if findings["evidence_basis_limited_to_unresolved_descriptor"] else "REJECT_OR_REPATCH_PATCHED_CANDIDATE",
            },
            {
                "step": "emit_review_decision",
                "question": "application_happens_in_this_unit",
                "answer": False,
                "taken": "STOP_PATCHED_CANDIDATE_ACCEPTED_FOR_SEPARATE_APPLICATION_UNIT" if accepted else "STOP_PATCHED_CANDIDATE_REQUIRES_REPATCH_OR_REJECTION",
            },
        ],
        "terminal": review_decision["terminal"],
    }

def build_report(review_decision: Dict[str, Any], findings: Dict[str, Any]) -> Dict[str, Any]:
    accepted = review_decision["decision_status"] == "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION"
    return {
        "schema_version": "semantically_patched_candidate_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_semantic_patch_receipt_id": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
        "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
        "patched_candidate_reviewed_count": 1,
        "patched_candidate_review_decision_emitted_count": 1,
        "patched_candidate_review_decision_status": review_decision["decision_status"],
        "patched_candidate_accepted_count": 1 if accepted else 0,
        "patched_candidate_rejected_or_repatch_required_count": 0 if accepted else 1,
        "semantic_acceptance_count": 1 if accepted else 0,
        "application_authorized_for_separate_unit_count": 1 if accepted else 0,
        "application_authorized_in_this_unit_count": 0,
        "semantic_status_valid_count": 1 if findings["semantic_status_valid"] else 0,
        "descriptor_status_valid_count": 1 if findings["descriptor_status_valid"] else 0,
        "negative_claims_complete_count": 1 if findings["negative_claims_complete"] else 0,
        "evidence_basis_limited_count": 1 if findings["evidence_basis_limited_to_unresolved_descriptor"] else 0,
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
        "recommended_next_handling": AUTHORIZED_APPLICATION_UNIT if accepted else "REPATCH_OR_REJECT_SEMANTICALLY_PATCHED_CANDIDATE_MISSING_OBJECT_PROPOSAL_FOR_R1000_TOP_GROUP_TAXONOMY_GAP_V0",
    }

def validate_review_outputs(
    findings: Dict[str, Any],
    decision: Dict[str, Any],
    authorization: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if findings.get("review_result") != "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION":
        failures.append(f"findings_review_result_wrong:{findings.get('review_result')}")
    if decision.get("decision_status") != "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION":
        failures.append("decision_status_wrong")
    if decision.get("semantic_acceptance") is not True:
        failures.append("semantic_acceptance_not_true")
    if decision.get("application_authorized_for_separate_unit") is not True:
        failures.append("separate_application_not_authorized")
    if decision.get("application_authorized_in_this_unit") is not False:
        failures.append("review_authorizes_current_unit")
    if authorization.get("application_authorized_for_separate_unit") is not True:
        failures.append("authorization_packet_not_separate_authorized")
    if authorization.get("application_authorized_in_this_unit") is not False:
        failures.append("authorization_packet_authorizes_current_unit")
    if authorization.get("authorized_application_unit") != AUTHORIZED_APPLICATION_UNIT:
        failures.append("authorized_application_unit_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "application_authorized_in_this_unit_count",
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

    if report.get("patched_candidate_reviewed_count") != 1:
        failures.append("patched_candidate_reviewed_count_wrong")
    if report.get("semantic_acceptance_count") != 1:
        failures.append("semantic_acceptance_count_wrong")
    if report.get("application_authorized_for_separate_unit_count") != 1:
        failures.append("separate_application_authorization_count_wrong")

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
    if metrics.get("patched_candidate_reviewed_count") != 1:
        failures.append("metric_patched_reviewed_wrong")
    if metrics.get("patched_candidate_review_decision_status") != "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION":
        failures.append("metric_review_status_wrong")
    if metrics.get("semantic_acceptance_count") != 1:
        failures.append("metric_semantic_acceptance_wrong")
    if metrics.get("application_authorized_for_separate_unit_count") != 1:
        failures.append("metric_separate_application_auth_wrong")

    for key in [
        "application_authorized_in_this_unit_count",
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
    if terminal.get("stop_code") != "STOP_PATCHED_CANDIDATE_ACCEPTED_FOR_SEPARATE_APPLICATION_UNIT":
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
    delta = sources["patch_delta"]

    findings = build_findings(patched, delta)
    decision = build_review_decision(patched, findings)
    authorization = build_authorization_packet(decision)
    trace = build_transition_trace(decision, findings)
    report = build_report(decision, findings)

    write_json(PATCHED_REVIEW_FINDINGS_PATH, findings)
    write_json(PATCHED_REVIEW_DECISION_PATH, decision)
    write_json(PATCHED_APPLICATION_AUTHORIZATION_PACKET_PATH, authorization)
    write_json(PATCHED_REVIEW_TRANSITION_TRACE_PATH, trace)
    write_json(PATCHED_REVIEW_REPORT_PATH, report)

    failures.extend(validate_review_outputs(findings, decision, authorization, trace, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "PATCHED_REVIEW_0_SEMANTIC_PATCH_CONSUMED": sources["semantic_patch_receipt"]["receipt_id"] == SOURCE_SEMANTIC_PATCH_RECEIPT_ID and sources["semantic_patch_receipt"]["gate"] == "PASS",
        "PATCHED_REVIEW_1_PATCHED_CANDIDATE_CONSUMED": patched["candidate_object_id"] == PATCHED_CANDIDATE_OBJECT_ID,
        "PATCHED_REVIEW_2_WEAKENED_SEMANTIC_STATUS_VALIDATED": findings["semantic_status_valid"] and findings["descriptor_status_valid"],
        "PATCHED_REVIEW_3_NEGATIVE_CLAIMS_VALIDATED": findings["negative_claims_complete"],
        "PATCHED_REVIEW_4_EVIDENCE_BASIS_LIMIT_VALIDATED": findings["evidence_basis_limited_to_unresolved_descriptor"] and findings["evidence_basis_does_not_support_values"],
        "PATCHED_REVIEW_5_UNRESOLVED_FIELDS_AND_EVIDENCE_PRESERVED": findings["unknown_decision_fields_preserved"] and findings["source_evidence_refs_preserved"],
        "PATCHED_REVIEW_6_ACCEPTED_FOR_SEPARATE_APPLICATION_ONLY": decision["decision_status"] == "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION" and decision["application_authorized_for_separate_unit"] is True and decision["application_authorized_in_this_unit"] is False,
        "PATCHED_REVIEW_7_NO_PROPOSAL_APPLICATION": report["proposal_applied_count"] == 0,
        "PATCHED_REVIEW_8_NO_FIELD_FILLING_OR_DESCRIPTOR_VALUE_ASSIGNMENT": report["target_field_filled_count"] == 0 and report["descriptor_value_assignment_count"] == 0 and report["null_field_value_emitted_count"] == 0,
        "PATCHED_REVIEW_9_NO_VALUE_OR_TAXONOMY_ACTION": report["field_value_invention_count"] == 0 and report["taxonomy_label_creation_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "PATCHED_REVIEW_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "PATCHED_REVIEW_11_NO_R1000_RUN_OR_GROUP_OPEN": report["r1000_run_executed_count"] == 0 and report["pressure_group_opened_count"] == 0 and report["next_group_auto_opened_count"] == 0,
        "PATCHED_REVIEW_12_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and decision["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_PATCHED_CANDIDATE_ACCEPTED_FOR_SEPARATE_APPLICATION_UNIT",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        }

    aggregate_metrics = {
        "source_semantic_patch_receipt_id": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
        "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
        "patched_candidate_reviewed_count": 1,
        "patched_candidate_review_decision_emitted_count": 1,
        "patched_candidate_review_decision_status": decision["decision_status"],
        "patched_candidate_accepted_count": report["patched_candidate_accepted_count"],
        "patched_candidate_rejected_or_repatch_required_count": report["patched_candidate_rejected_or_repatch_required_count"],
        "semantic_acceptance_count": report["semantic_acceptance_count"],
        "application_authorized_for_separate_unit_count": report["application_authorized_for_separate_unit_count"],
        "application_authorized_in_this_unit_count": 0,
        "semantic_status_valid_count": report["semantic_status_valid_count"],
        "descriptor_status_valid_count": report["descriptor_status_valid_count"],
        "negative_claims_complete_count": report["negative_claims_complete_count"],
        "evidence_basis_limited_count": report["evidence_basis_limited_count"],
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
        "authorized_application_unit": AUTHORIZED_APPLICATION_UNIT,
        "recommended_next_handling": report["recommended_next_handling"],
    }

    guards = {
        "semantic_patch_consumed": True,
        "patched_candidate_consumed": True,
        "weakened_semantic_claims_validated": findings["semantic_status_valid"] and findings["descriptor_status_valid"],
        "negative_claims_validated": findings["negative_claims_complete"],
        "evidence_basis_limited": findings["evidence_basis_limited_to_unresolved_descriptor"],
        "patched_candidate_accepted_for_separate_application": decision["decision_status"] == "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION",
        "application_authorized_for_separate_unit": decision["application_authorized_for_separate_unit"],
        "application_authorized_in_this_unit": False,
        "proposal_applied": False,
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
        "source_semantic_patch": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
        "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
        "decision_status": decision["decision_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "patched_candidate_review_findings": rel(PATCHED_REVIEW_FINDINGS_PATH),
        "patched_candidate_review_decision": rel(PATCHED_REVIEW_DECISION_PATH),
        "patched_candidate_application_authorization_packet": rel(PATCHED_APPLICATION_AUTHORIZATION_PACKET_PATH),
        "patched_candidate_review_transition_trace": rel(PATCHED_REVIEW_TRANSITION_TRACE_PATH),
        "patched_candidate_review_report": rel(PATCHED_REVIEW_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "semantically_patched_candidate_review_r1000_taxonomy_gap_receipt_v0",
        "receipt_type": "SEMANTICALLY_PATCHED_CANDIDATE_REVIEW_R1000_TAXONOMY_GAP_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_semantic_patch_receipt_id": SOURCE_SEMANTIC_PATCH_RECEIPT_ID,
        "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "semantically_patched_candidate_review_summary": {
            "source_candidate_object_id": SOURCE_CANDIDATE_OBJECT_ID,
            "patched_candidate_object_id": PATCHED_CANDIDATE_OBJECT_ID,
            "review_decision_status": decision["decision_status"],
            "semantic_acceptance": decision["semantic_acceptance"],
            "application_authorized_for_separate_unit": decision["application_authorized_for_separate_unit"],
            "application_authorized_in_this_unit": False,
            "authorized_application_unit": AUTHORIZED_APPLICATION_UNIT,
            "proposal_applied": False,
            "descriptor_value_assignment": False,
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "semantically_patched_candidate_review_guards": guards,
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
    print(f"semantically_patched_candidate_review_receipt_id={receipt_id}")
    print(f"semantically_patched_candidate_review_receipt_path=data/semantically_patched_candidate_review_r1000_taxonomy_gap_v0_receipts/{receipt_id}.json")
    print(f"semantically_patched_candidate_review_decision_path=data/semantically_patched_candidate_review_r1000_taxonomy_gap_v0/semantically_patched_candidate_review_decision.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
