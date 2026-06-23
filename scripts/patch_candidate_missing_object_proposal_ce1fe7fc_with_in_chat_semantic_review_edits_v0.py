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

UNIT_ID = "PATCH_CANDIDATE_MISSING_OBJECT_PROPOSAL_CE1FE7FC_WITH_IN_CHAT_SEMANTIC_REVIEW_EDITS_V0"
TARGET_UNIT_ID = "candidate_missing_object_proposal_semantic_patch.ce1fe7fc.r1000_taxonomy_gap.v0"

SOURCE_SEMANTIC_BARRIER_RECEIPT_ID = "4e6b09b2"
SOURCE_PROPOSAL_REVIEW_RECEIPT_ID = "a939b4a6"
SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID = "aa01c2a9"
SOURCE_PROPOSAL_LAYER_RECEIPT_ID = "6003c89c"
SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
CANDIDATE_OBJECT_ID = "ce1fe7fc"

OUT_DIR = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0"
RECEIPT_DIR = ROOT / "data" / "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0_receipts"

IN_CHAT_SEMANTIC_REVIEW_RESULT_PATH = OUT_DIR / "in_chat_semantic_review_result.json"
PATCH_REQUIREMENTS_PATH = OUT_DIR / "candidate_semantic_patch_requirements.json"
PATCHED_CANDIDATE_PATH = OUT_DIR / "r1000_top_group_taxonomy_gap_semantically_patched_candidate_missing_object_proposal.json"
PATCH_DELTA_PATH = OUT_DIR / "candidate_semantic_patch_delta.json"
PATCHED_REVIEW_PACKET_PATH = OUT_DIR / "patched_candidate_review_packet.json"
PATCH_APPLICATION_BLOCKER_PATH = OUT_DIR / "patched_candidate_application_blocker_packet.json"
PATCH_TRANSITION_TRACE_PATH = OUT_DIR / "semantic_patch_transition_trace.json"
PATCH_REPORT_PATH = OUT_DIR / "semantic_patch_report.json"

SEMANTIC_BARRIER_RECEIPT_PATH = ROOT / "data" / "candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_SEMANTIC_BARRIER_RECEIPT_ID}.json"
STRUCTURAL_ONLY_RECLASSIFICATION_PATH = ROOT / "data" / "candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0" / "candidate_review_structural_only_reclassification.json"
IN_CHAT_SEMANTIC_REVIEW_REQUEST_PATH = ROOT / "data" / "candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0" / "in_chat_semantic_review_request.json"
SEMANTIC_REVIEW_CHECKLIST_PATH = ROOT / "data" / "candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0" / "candidate_semantic_review_checklist.json"
SEMANTIC_APPLICATION_BLOCKER_PATH = ROOT / "data" / "candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0" / "candidate_application_blocker_packet.json"
SEMANTIC_BARRIER_REPORT_PATH = ROOT / "data" / "candidate_proposal_semantic_review_barrier_r1000_taxonomy_gap_v0" / "semantic_review_barrier_report.json"

PROPOSAL_REVIEW_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PROPOSAL_REVIEW_RECEIPT_ID}.json"
PROPOSAL_REVIEW_DECISION_PATH = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_candidate_proposal_review_decision.json"
PROPOSAL_REVIEW_AUTHORIZATION_PACKET_PATH = ROOT / "data" / "candidate_missing_object_proposal_review_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_candidate_proposal_application_authorization_packet.json"

PROPOSAL_APPLICATION_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID}.json"
CANDIDATE_PROPOSAL_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_candidate_missing_object_proposal.json"
TYPED_DECISION_FIELDS_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_typed_unresolved_decision_fields.jsonl"
PROPOSAL_EVIDENCE_REFS_PATH = ROOT / "data" / "candidate_missing_object_proposal_application_r1000_taxonomy_gap_v0" / "r1000_top_group_taxonomy_gap_proposal_evidence_refs.json"

PROPOSAL_LAYER_RECEIPT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0_receipts" / f"{SOURCE_PROPOSAL_LAYER_RECEIPT_ID}.json"
PROPOSAL_LAYER_CONTRACT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_missing_object_proposal_layer_contract.json"
PROPOSAL_APPLICATION_CONTRACT_PATH = ROOT / "data" / "candidate_missing_object_proposal_layer_for_expected_limits_v0" / "candidate_proposal_application_contract.json"

EXPECTED_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_RECEIPT_ID}.json"

SOURCE_FILES = [
    SEMANTIC_BARRIER_RECEIPT_PATH,
    STRUCTURAL_ONLY_RECLASSIFICATION_PATH,
    IN_CHAT_SEMANTIC_REVIEW_REQUEST_PATH,
    SEMANTIC_REVIEW_CHECKLIST_PATH,
    SEMANTIC_APPLICATION_BLOCKER_PATH,
    SEMANTIC_BARRIER_REPORT_PATH,
    PROPOSAL_REVIEW_RECEIPT_PATH,
    PROPOSAL_REVIEW_DECISION_PATH,
    PROPOSAL_REVIEW_AUTHORIZATION_PACKET_PATH,
    PROPOSAL_APPLICATION_RECEIPT_PATH,
    CANDIDATE_PROPOSAL_PATH,
    TYPED_DECISION_FIELDS_PATH,
    PROPOSAL_EVIDENCE_REFS_PATH,
    PROPOSAL_LAYER_RECEIPT_PATH,
    PROPOSAL_LAYER_CONTRACT_PATH,
    PROPOSAL_APPLICATION_CONTRACT_PATH,
    EXPECTED_LIMIT_RECEIPT_PATH,
]

REQUIRED_DESCRIPTOR_FIELDS = [
    "missing_label_identifier",
    "taxonomy_context_ref",
    "current_label_space_ref",
    "expected_label_space_ref",
]

SEMANTIC_CLASSIFICATION = "ACCEPTABLE_ONLY_AFTER_EDITS"

HUMAN_DECISION = {
    "decision": "PATCH_CANDIDATE_MISSING_OBJECT_PROPOSAL_CE1FE7FC_WITH_IN_CHAT_SEMANTIC_REVIEW_EDITS",
    "scope": "record in-chat semantic review result, classify candidate as acceptable only after edits, and emit a semantically weakened patched candidate without application authorization",
    "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
    "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
    "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
    "candidate_object_id": CANDIDATE_OBJECT_ID,
    "authorized": [
        "record in-chat semantic review result",
        "classify candidate as acceptable only after edits",
        "emit semantic patch requirements",
        "emit patched candidate proposal with weakened semantic claims",
        "emit patch delta",
        "emit patched candidate review packet",
        "preserve application blocker",
        "stop before application authorization",
    ],
    "not_authorized": [
        "semantic acceptance for application",
        "semantic rejection",
        "applying the proposal",
        "authorizing application",
        "filling missing descriptor fields",
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
        "semantic_barrier_receipt": read_json(SEMANTIC_BARRIER_RECEIPT_PATH),
        "structural_only_reclassification": read_json(STRUCTURAL_ONLY_RECLASSIFICATION_PATH),
        "in_chat_semantic_review_request": read_json(IN_CHAT_SEMANTIC_REVIEW_REQUEST_PATH),
        "semantic_review_checklist": read_json(SEMANTIC_REVIEW_CHECKLIST_PATH),
        "semantic_application_blocker": read_json(SEMANTIC_APPLICATION_BLOCKER_PATH),
        "semantic_barrier_report": read_json(SEMANTIC_BARRIER_REPORT_PATH),
        "proposal_review_receipt": read_json(PROPOSAL_REVIEW_RECEIPT_PATH),
        "proposal_review_decision": read_json(PROPOSAL_REVIEW_DECISION_PATH),
        "proposal_review_authorization_packet": read_json(PROPOSAL_REVIEW_AUTHORIZATION_PACKET_PATH),
        "proposal_application_receipt": read_json(PROPOSAL_APPLICATION_RECEIPT_PATH),
        "candidate_proposal": read_json(CANDIDATE_PROPOSAL_PATH),
        "typed_decision_fields": read_jsonl(TYPED_DECISION_FIELDS_PATH),
        "proposal_evidence_refs": read_json(PROPOSAL_EVIDENCE_REFS_PATH),
        "proposal_layer_receipt": read_json(PROPOSAL_LAYER_RECEIPT_PATH),
        "proposal_layer_contract": read_json(PROPOSAL_LAYER_CONTRACT_PATH),
        "proposal_application_contract": read_json(PROPOSAL_APPLICATION_CONTRACT_PATH),
        "expected_limit_receipt": read_json(EXPECTED_LIMIT_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    barrier = sources["semantic_barrier_receipt"]
    candidate = sources["candidate_proposal"]
    app_receipt = sources["proposal_application_receipt"]
    review_receipt = sources["proposal_review_receipt"]
    blocker = sources["semantic_application_blocker"]

    if barrier.get("receipt_id") != SOURCE_SEMANTIC_BARRIER_RECEIPT_ID:
        failures.append("semantic_barrier_receipt_id_wrong")
    if barrier.get("gate") != "PASS":
        failures.append("semantic_barrier_not_pass")
    if barrier.get("aggregate_metrics", {}).get("in_chat_semantic_review_required_count") != 1:
        failures.append("semantic_review_not_required")
    if barrier.get("aggregate_metrics", {}).get("semantic_acceptance_count") != 0:
        failures.append("semantic_acceptance_already_recorded")
    if barrier.get("aggregate_metrics", {}).get("application_authorized_after_barrier_count") != 0:
        failures.append("application_already_authorized_after_barrier")
    if barrier.get("terminal", {}).get("stop_code") != "STOP_IN_CHAT_SEMANTIC_REVIEW_REQUIRED_BEFORE_APPLICATION_AUTHORIZATION":
        failures.append("semantic_barrier_terminal_wrong")

    if blocker.get("application_blocked") is not True:
        failures.append("semantic_blocker_not_blocking_application")
    if blocker.get("application_authorization_after_barrier") is not False:
        failures.append("semantic_blocker_authorizes_application")

    if candidate.get("candidate_object_id") != CANDIDATE_OBJECT_ID:
        failures.append("candidate_object_id_wrong")
    if candidate.get("object_status") != "CANDIDATE_MISSING_OBJECT_PROPOSAL":
        failures.append("candidate_status_wrong")
    if candidate.get("application_authorized") is not False:
        failures.append("candidate_self_authorizes_application")

    if app_receipt.get("receipt_id") != SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID:
        failures.append("proposal_application_receipt_id_wrong")
    if app_receipt.get("gate") != "PASS":
        failures.append("proposal_application_not_pass")
    if app_receipt.get("aggregate_metrics", {}).get("proposal_applied_count") != 0:
        failures.append("proposal_already_applied")

    if review_receipt.get("receipt_id") != SOURCE_PROPOSAL_REVIEW_RECEIPT_ID:
        failures.append("proposal_review_receipt_id_wrong")
    if review_receipt.get("gate") != "PASS":
        failures.append("proposal_review_not_pass")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_semantic_review_result() -> Dict[str, Any]:
    return {
        "schema_version": "in_chat_semantic_review_result_v0",
        "candidate_object_id": CANDIDATE_OBJECT_ID,
        "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "semantic_review_location": "chat",
        "semantic_review_completed": True,
        "semantic_classification": SEMANTIC_CLASSIFICATION,
        "semantic_acceptance": False,
        "semantic_rejection": False,
        "application_authorized": False,
        "proposal_application_allowed": False,
        "summary": "Candidate is directionally valid because it replaces untyped null absence with typed unresolved decision fields, but it overstates the semantic status of the descriptor object unless patched.",
        "semantically_sound_parts": [
            "represents missing descriptor fields as typed unresolved decision fields",
            "does not fill missing_label_identifier",
            "does not fill taxonomy_context_ref",
            "does not fill current_label_space_ref",
            "does not fill expected_label_space_ref",
            "does not authorize application",
            "does not create taxonomy labels",
            "does not mutate source or receipts",
        ],
        "semantic_issues": [
            "missing_object_type taxonomy_gap_evidence_surface_descriptor sounds stronger than the evidence supports",
            "target surface framing can be read as if a descriptor exists rather than as if a descriptor is required",
            "all meaningful descriptor fields remain unresolved",
            "evidence basis supports a typed unresolved descriptor proposal only, not descriptor value assignment",
        ],
        "required_edits": [
            "add semantic_status TYPED_UNRESOLVED_DESCRIPTOR_PROPOSAL",
            "add descriptor_status CANDIDATE_UNRESOLVED_DESCRIPTOR_NOT_VALUE_DESCRIPTOR",
            "add explicit positive claim that a descriptor object is needed",
            "add explicit negative claims that the proposal does not identify descriptor values",
            "add evidence_basis_strength limited to typed unresolved descriptor proposal only",
            "add alternative_shapes_considered",
            "add risk_if_wrong",
            "keep application_authorized false",
        ],
    }

def build_patch_requirements(review_result: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "candidate_semantic_patch_requirements_v0",
        "candidate_object_id": CANDIDATE_OBJECT_ID,
        "semantic_classification": review_result["semantic_classification"],
        "patch_required": True,
        "patch_requirement_status": "REQUIRED_BEFORE_APPLICATION_AUTHORIZATION",
        "required_patch_fields": [
            "semantic_status",
            "descriptor_status",
            "positive_claim",
            "negative_claims",
            "evidence_basis_strength",
            "alternative_shapes_considered",
            "risk_if_wrong",
            "semantic_review_result",
            "application_authorized",
        ],
        "must_preserve": [
            "unknown_required_decision_fields",
            "source_evidence_refs",
            "application_authorized false",
            "no descriptor value assignment",
            "no taxonomy action",
            "no source mutation",
        ],
        "must_not_add": [
            "descriptor field values",
            "taxonomy labels",
            "taxonomy upgrade authorization",
            "application authorization",
            "correctness claims",
            "global source absence claims",
        ],
    }

def build_patched_candidate(candidate: Dict[str, Any], review_result: Dict[str, Any]) -> Dict[str, Any]:
    patched = copy.deepcopy(candidate)

    patched["schema_version"] = "semantically_patched_candidate_missing_object_proposal_instance_v0"
    patched["source_candidate_object_id"] = candidate["candidate_object_id"]
    patched["candidate_object_id"] = sha8({
        "source_candidate_object_id": candidate["candidate_object_id"],
        "semantic_classification": SEMANTIC_CLASSIFICATION,
        "patch": "weaken_descriptor_claims",
    })
    patched["object_status"] = "SEMANTICALLY_PATCHED_CANDIDATE_MISSING_OBJECT_PROPOSAL"
    patched["semantic_review_result"] = {
        "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "semantic_classification": SEMANTIC_CLASSIFICATION,
        "semantic_acceptance": False,
        "semantic_rejection": False,
        "application_authorized": False,
        "proposal_application_allowed": False,
    }
    patched["semantic_status"] = "TYPED_UNRESOLVED_DESCRIPTOR_PROPOSAL"
    patched["descriptor_status"] = "CANDIDATE_UNRESOLVED_DESCRIPTOR_NOT_VALUE_DESCRIPTOR"
    patched["positive_claim"] = "A descriptor object is needed to make the R1000 top-group taxonomy-gap evidence surface reviewable."
    patched["negative_claims"] = [
        "does_not_identify_missing_label_identifier",
        "does_not_identify_taxonomy_context_ref",
        "does_not_identify_current_label_space_ref",
        "does_not_identify_expected_label_space_ref",
        "does_not_authorize_taxonomy_repair",
        "does_not_prove_source_content_globally_absent",
        "does_not_authorize_application",
        "does_not_claim_correctness_of_descriptor_values",
    ]
    patched["evidence_basis_strength"] = {
        "supports": "typed_unresolved_descriptor_proposal_only",
        "does_not_support": [
            "descriptor_value_assignment",
            "missing_label_identity",
            "taxonomy_context_identity",
            "current_label_space_identity",
            "expected_label_space_identity",
            "taxonomy_label_creation",
            "source_mutation",
        ],
    }
    patched["alternative_shapes_considered"] = [
        "missing_label_identifier_only",
        "label_space_boundary_descriptor",
        "provenance_source_chain_descriptor",
        "expected_unavailable_marker",
        "split_candidate_objects_per_unresolved_descriptor_field",
    ]
    patched["risk_if_wrong"] = [
        "may_collapse_distinct_missing_object_types_into_one_descriptor",
        "may_overstate_semantic_distinguishability",
        "may_bias_later_taxonomy_or_application_units",
        "may_make_downstream_units_treat_required_descriptor_as_existing_descriptor",
    ]
    patched["application_authorized"] = False
    patched["required_human_schema_decision"] = [
        "REVIEW_PATCHED_CANDIDATE_OBJECT",
        "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION",
        "REJECT_PATCHED_CANDIDATE_OBJECT",
        "REQUEST_MORE_EVIDENCE",
        "SPLIT_PATCHED_CANDIDATE_OBJECT",
        "MARK_EXPECTED_UNAVAILABLE_AT_THIS_LAYER",
    ]
    patched["forbidden_assumptions"] = sorted(set(patched.get("forbidden_assumptions", []) + [
        "do_not_treat_unresolved_descriptor_as_value_descriptor",
        "do_not_treat_structural_review_as_semantic_acceptance",
        "do_not_apply_without_explicit_semantic_acceptance",
        "do_not_infer_descriptor_values_from_required_fields",
    ]))
    patched["terminal"] = {
        "type": "STOP",
        "stop_code": "STOP_SEMANTICALLY_PATCHED_CANDIDATE_EMITTED_REQUIRES_REVIEW",
        "next_command_goal": None,
    }
    return patched

def build_patch_delta(candidate: Dict[str, Any], patched: Dict[str, Any]) -> Dict[str, Any]:
    added_keys = sorted([key for key in patched.keys() if key not in candidate])
    changed_keys = sorted([key for key in patched.keys() if key in candidate and patched[key] != candidate[key]])

    return {
        "schema_version": "candidate_semantic_patch_delta_v0",
        "source_candidate_object_id": candidate["candidate_object_id"],
        "patched_candidate_object_id": patched["candidate_object_id"],
        "semantic_classification": SEMANTIC_CLASSIFICATION,
        "patch_delta_type": "WEAKEN_SEMANTIC_CLAIMS_AND_PRESERVE_NO_APPLICATION",
        "added_keys": added_keys,
        "changed_keys": changed_keys,
        "required_descriptor_fields_preserved": patched.get("required_object_fields") == candidate.get("required_object_fields"),
        "unknown_decision_fields_preserved": patched.get("unknown_required_decision_fields") == candidate.get("unknown_required_decision_fields"),
        "source_evidence_refs_preserved": patched.get("source_evidence_refs") == candidate.get("source_evidence_refs"),
        "application_authorized_before": candidate.get("application_authorized"),
        "application_authorized_after": patched.get("application_authorized"),
    }

def build_patched_review_packet(patched: Dict[str, Any], delta: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "patched_candidate_review_packet_v0",
        "patched_candidate_object_id": patched["candidate_object_id"],
        "source_candidate_object_id": patched["source_candidate_object_id"],
        "semantic_classification": SEMANTIC_CLASSIFICATION,
        "review_required": True,
        "application_authorized": False,
        "review_scope": "confirm whether semantic patch is sufficient before any separate application authorization",
        "review_packet_must_check": [
            "semantic_status is TYPED_UNRESOLVED_DESCRIPTOR_PROPOSAL",
            "descriptor_status does not imply descriptor values exist",
            "negative claims block descriptor value inference",
            "evidence basis strength is limited to typed unresolved proposal",
            "alternatives and risks are explicit",
            "application remains unauthorized",
        ],
        "allowed_outcomes": [
            "ACCEPT_PATCHED_CANDIDATE_FOR_SEPARATE_APPLICATION",
            "REJECT_PATCHED_CANDIDATE_OBJECT",
            "REQUEST_MORE_EVIDENCE",
            "SPLIT_PATCHED_CANDIDATE_OBJECT",
            "MARK_EXPECTED_UNAVAILABLE_AT_THIS_LAYER",
        ],
        "patch_delta_ref": rel(PATCH_DELTA_PATH),
        "terminal": patched["terminal"],
    }

def build_application_blocker(patched: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "patched_candidate_application_blocker_packet_v0",
        "patched_candidate_object_id": patched["candidate_object_id"],
        "source_candidate_object_id": patched["source_candidate_object_id"],
        "application_blocked": True,
        "application_authorized": False,
        "blocked_until": "PATCHED_CANDIDATE_REVIEW_ACCEPTS_SEPARATE_APPLICATION_SCOPE",
        "blocked_application_unit": "APPLY_ACCEPTED_CANDIDATE_MISSING_OBJECT_PROPOSAL_TO_R1000_TOP_GROUP_TAXONOMY_GAP_EVIDENCE_SURFACE_V0",
        "reason": "semantic patch emitted after acceptable-only-after-edits review; patched candidate still requires review before application authorization",
        "forbidden_next_handling": [
            "apply patched candidate immediately",
            "fill descriptor values",
            "create taxonomy labels",
            "mutate source rows",
            "mutate existing receipts",
            "treat patch as semantic acceptance",
        ],
    }

def build_transition_trace(patched: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "candidate_semantic_patch_transition_trace_v0",
        "source_candidate_object_id": CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": patched["candidate_object_id"],
        "trace": [
            {
                "step": "consume_semantic_review_barrier",
                "question": "is in-chat semantic review required",
                "answer": True,
                "taken": "record_in_chat_semantic_review_result",
            },
            {
                "step": "record_in_chat_semantic_review_result",
                "question": "is candidate acceptable for application without edits",
                "answer": False,
                "taken": "emit_semantic_patch_requirements",
            },
            {
                "step": "emit_semantic_patch_requirements",
                "question": "can candidate be patched without filling descriptor values",
                "answer": True,
                "taken": "emit_semantically_patched_candidate",
            },
            {
                "step": "emit_semantically_patched_candidate",
                "question": "does patched candidate authorize application now",
                "answer": False,
                "taken": "STOP_SEMANTICALLY_PATCHED_CANDIDATE_EMITTED_REQUIRES_REVIEW",
            },
        ],
        "terminal": patched["terminal"],
    }

def build_report(patched: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "candidate_semantic_patch_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_candidate_object_id": CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": patched["candidate_object_id"],
        "in_chat_semantic_review_consumed_count": 1,
        "semantic_review_completed_count": 1,
        "semantic_classification": SEMANTIC_CLASSIFICATION,
        "semantic_acceptance_count": 0,
        "semantic_rejection_count": 0,
        "acceptable_only_after_edits_count": 1,
        "patch_requirements_emitted_count": 1,
        "candidate_edit_emitted_count": 1,
        "patched_candidate_emitted_count": 1,
        "patched_candidate_review_required_count": 1,
        "application_blocker_packet_emitted_count": 1,
        "application_blocked_count": 1,
        "application_authorized_count": 0,
        "application_authorized_after_patch_count": 0,
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
        "recommended_next_handling": "REVIEW_SEMANTICALLY_PATCHED_CANDIDATE_MISSING_OBJECT_PROPOSAL_FOR_R1000_TOP_GROUP_TAXONOMY_GAP_V0",
    }

def validate_patch_outputs(
    review_result: Dict[str, Any],
    requirements: Dict[str, Any],
    patched: Dict[str, Any],
    delta: Dict[str, Any],
    review_packet: Dict[str, Any],
    blocker: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if review_result.get("semantic_classification") != SEMANTIC_CLASSIFICATION:
        failures.append("semantic_classification_wrong")
    if review_result.get("semantic_acceptance") is not False:
        failures.append("semantic_acceptance_not_false")
    if review_result.get("application_authorized") is not False:
        failures.append("semantic_review_authorizes_application")
    if requirements.get("patch_required") is not True:
        failures.append("patch_not_required")
    if patched.get("object_status") != "SEMANTICALLY_PATCHED_CANDIDATE_MISSING_OBJECT_PROPOSAL":
        failures.append("patched_candidate_status_wrong")
    if patched.get("semantic_status") != "TYPED_UNRESOLVED_DESCRIPTOR_PROPOSAL":
        failures.append("patched_semantic_status_wrong")
    if patched.get("descriptor_status") != "CANDIDATE_UNRESOLVED_DESCRIPTOR_NOT_VALUE_DESCRIPTOR":
        failures.append("patched_descriptor_status_wrong")
    if patched.get("application_authorized") is not False:
        failures.append("patched_candidate_authorizes_application")
    if "does_not_identify_missing_label_identifier" not in patched.get("negative_claims", []):
        failures.append("patched_negative_claim_missing_label_missing")
    if patched.get("evidence_basis_strength", {}).get("supports") != "typed_unresolved_descriptor_proposal_only":
        failures.append("patched_evidence_basis_too_strong")
    if not patched.get("alternative_shapes_considered"):
        failures.append("patched_alternatives_missing")
    if not patched.get("risk_if_wrong"):
        failures.append("patched_risk_missing")
    if delta.get("unknown_decision_fields_preserved") is not True:
        failures.append("typed_decision_fields_not_preserved")
    if delta.get("source_evidence_refs_preserved") is not True:
        failures.append("source_evidence_refs_not_preserved")
    if delta.get("application_authorized_after") is not False:
        failures.append("delta_application_authorized_after_wrong")
    if review_packet.get("review_required") is not True:
        failures.append("patched_review_not_required")
    if review_packet.get("application_authorized") is not False:
        failures.append("patched_review_packet_authorizes_application")
    if blocker.get("application_blocked") is not True:
        failures.append("patch_application_not_blocked")
    if blocker.get("application_authorized") is not False:
        failures.append("patch_blocker_authorizes_application")
    if trace.get("terminal", {}).get("stop_code") != "STOP_SEMANTICALLY_PATCHED_CANDIDATE_EMITTED_REQUIRES_REVIEW":
        failures.append("trace_terminal_stop_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "semantic_acceptance_count",
        "semantic_rejection_count",
        "application_authorized_count",
        "application_authorized_after_patch_count",
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

    if report.get("semantic_review_completed_count") != 1:
        failures.append("semantic_review_completed_count_wrong")
    if report.get("acceptable_only_after_edits_count") != 1:
        failures.append("acceptable_only_after_edits_count_wrong")
    if report.get("candidate_edit_emitted_count") != 1:
        failures.append("candidate_edit_emitted_count_wrong")
    if report.get("patched_candidate_emitted_count") != 1:
        failures.append("patched_candidate_emitted_count_wrong")

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
    if metrics.get("semantic_review_completed_count") != 1:
        failures.append("metric_semantic_review_completed_wrong")
    if metrics.get("semantic_classification") != SEMANTIC_CLASSIFICATION:
        failures.append("metric_semantic_classification_wrong")
    if metrics.get("acceptable_only_after_edits_count") != 1:
        failures.append("metric_acceptable_only_after_edits_wrong")
    if metrics.get("patched_candidate_emitted_count") != 1:
        failures.append("metric_patched_candidate_emitted_wrong")

    for key in [
        "semantic_acceptance_count",
        "semantic_rejection_count",
        "application_authorized_count",
        "application_authorized_after_patch_count",
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
    if terminal.get("stop_code") != "STOP_SEMANTICALLY_PATCHED_CANDIDATE_EMITTED_REQUIRES_REVIEW":
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

    original_candidate = sources["candidate_proposal"]

    review_result = build_semantic_review_result()
    requirements = build_patch_requirements(review_result)
    patched = build_patched_candidate(original_candidate, review_result)
    delta = build_patch_delta(original_candidate, patched)
    review_packet = build_patched_review_packet(patched, delta)
    blocker = build_application_blocker(patched)
    trace = build_transition_trace(patched)
    report = build_report(patched)

    write_json(IN_CHAT_SEMANTIC_REVIEW_RESULT_PATH, review_result)
    write_json(PATCH_REQUIREMENTS_PATH, requirements)
    write_json(PATCHED_CANDIDATE_PATH, patched)
    write_json(PATCH_DELTA_PATH, delta)
    write_json(PATCHED_REVIEW_PACKET_PATH, review_packet)
    write_json(PATCH_APPLICATION_BLOCKER_PATH, blocker)
    write_json(PATCH_TRANSITION_TRACE_PATH, trace)
    write_json(PATCH_REPORT_PATH, report)

    failures.extend(validate_patch_outputs(
        review_result,
        requirements,
        patched,
        delta,
        review_packet,
        blocker,
        trace,
        report,
    ))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "SEMANTIC_PATCH_0_SEMANTIC_BARRIER_CONSUMED": sources["semantic_barrier_receipt"]["receipt_id"] == SOURCE_SEMANTIC_BARRIER_RECEIPT_ID and sources["semantic_barrier_receipt"]["gate"] == "PASS",
        "SEMANTIC_PATCH_1_ORIGINAL_CANDIDATE_CONSUMED": original_candidate["candidate_object_id"] == CANDIDATE_OBJECT_ID,
        "SEMANTIC_PATCH_2_IN_CHAT_SEMANTIC_REVIEW_RESULT_EMITTED": IN_CHAT_SEMANTIC_REVIEW_RESULT_PATH.exists() and review_result["semantic_classification"] == SEMANTIC_CLASSIFICATION,
        "SEMANTIC_PATCH_3_CLASSIFIED_ACCEPTABLE_ONLY_AFTER_EDITS": report["acceptable_only_after_edits_count"] == 1 and report["semantic_acceptance_count"] == 0,
        "SEMANTIC_PATCH_4_PATCH_REQUIREMENTS_EMITTED": PATCH_REQUIREMENTS_PATH.exists() and requirements["patch_required"] is True,
        "SEMANTIC_PATCH_5_PATCHED_CANDIDATE_EMITTED": PATCHED_CANDIDATE_PATH.exists() and patched["object_status"] == "SEMANTICALLY_PATCHED_CANDIDATE_MISSING_OBJECT_PROPOSAL",
        "SEMANTIC_PATCH_6_SEMANTIC_CLAIMS_WEAKENED": patched["semantic_status"] == "TYPED_UNRESOLVED_DESCRIPTOR_PROPOSAL" and patched["descriptor_status"] == "CANDIDATE_UNRESOLVED_DESCRIPTOR_NOT_VALUE_DESCRIPTOR",
        "SEMANTIC_PATCH_7_UNRESOLVED_FIELDS_AND_EVIDENCE_PRESERVED": delta["unknown_decision_fields_preserved"] is True and delta["source_evidence_refs_preserved"] is True,
        "SEMANTIC_PATCH_8_NO_APPLICATION_AUTHORIZATION": report["application_authorized_count"] == 0 and patched["application_authorized"] is False,
        "SEMANTIC_PATCH_9_NO_PROPOSAL_APPLICATION_OR_FIELD_FILLING": report["proposal_applied_count"] == 0 and report["target_field_filled_count"] == 0 and report["descriptor_value_assignment_count"] == 0,
        "SEMANTIC_PATCH_10_NO_VALUE_OR_TAXONOMY_ACTION": report["field_value_invention_count"] == 0 and report["taxonomy_label_creation_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "SEMANTIC_PATCH_11_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "SEMANTIC_PATCH_12_NO_R1000_RUN_OR_GROUP_OPEN": report["r1000_run_executed_count"] == 0 and report["pressure_group_opened_count"] == 0 and report["next_group_auto_opened_count"] == 0,
        "SEMANTIC_PATCH_13_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_SEMANTICALLY_PATCHED_CANDIDATE_EMITTED_REQUIRES_REVIEW",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        }

    aggregate_metrics = {
        "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_candidate_object_id": CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": patched["candidate_object_id"],
        "in_chat_semantic_review_consumed_count": 1,
        "semantic_review_completed_count": 1,
        "semantic_classification": SEMANTIC_CLASSIFICATION,
        "semantic_acceptance_count": 0,
        "semantic_rejection_count": 0,
        "acceptable_only_after_edits_count": 1,
        "patch_requirements_emitted_count": 1,
        "candidate_edit_emitted_count": 1,
        "patched_candidate_emitted_count": 1,
        "patched_candidate_review_required_count": 1,
        "application_blocker_packet_emitted_count": 1,
        "application_blocked_count": 1,
        "application_authorized_count": 0,
        "application_authorized_after_patch_count": 0,
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
        "semantic_barrier_consumed": True,
        "in_chat_semantic_review_result_emitted": True,
        "semantic_review_completed": True,
        "semantic_classification_is_acceptable_only_after_edits": True,
        "semantic_acceptance": False,
        "semantic_rejection": False,
        "patch_requirements_emitted": True,
        "patched_candidate_emitted": True,
        "patched_candidate_review_required": True,
        "application_blocked": True,
        "application_authorized": False,
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
        "source_semantic_barrier": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "source_candidate_object_id": CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": patched["candidate_object_id"],
        "semantic_classification": SEMANTIC_CLASSIFICATION,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "in_chat_semantic_review_result": rel(IN_CHAT_SEMANTIC_REVIEW_RESULT_PATH),
        "patch_requirements": rel(PATCH_REQUIREMENTS_PATH),
        "semantically_patched_candidate": rel(PATCHED_CANDIDATE_PATH),
        "patch_delta": rel(PATCH_DELTA_PATH),
        "patched_candidate_review_packet": rel(PATCHED_REVIEW_PACKET_PATH),
        "patched_candidate_application_blocker": rel(PATCH_APPLICATION_BLOCKER_PATH),
        "semantic_patch_transition_trace": rel(PATCH_TRANSITION_TRACE_PATH),
        "semantic_patch_report": rel(PATCH_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_receipt_v0",
        "receipt_type": "CANDIDATE_MISSING_OBJECT_PROPOSAL_SEMANTIC_PATCH_R1000_TAXONOMY_GAP_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_semantic_barrier_receipt_id": SOURCE_SEMANTIC_BARRIER_RECEIPT_ID,
        "source_proposal_review_receipt_id": SOURCE_PROPOSAL_REVIEW_RECEIPT_ID,
        "source_proposal_application_receipt_id": SOURCE_PROPOSAL_APPLICATION_RECEIPT_ID,
        "source_proposal_layer_receipt_id": SOURCE_PROPOSAL_LAYER_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_candidate_object_id": CANDIDATE_OBJECT_ID,
        "patched_candidate_object_id": patched["candidate_object_id"],
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "candidate_missing_object_proposal_semantic_patch_summary": {
            "source_candidate_object_id": CANDIDATE_OBJECT_ID,
            "patched_candidate_object_id": patched["candidate_object_id"],
            "semantic_classification": SEMANTIC_CLASSIFICATION,
            "semantic_acceptance": False,
            "semantic_rejection": False,
            "application_authorized": False,
            "patched_candidate_review_required": True,
            "semantic_status": patched["semantic_status"],
            "descriptor_status": patched["descriptor_status"],
            "application_blocked": True,
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "candidate_missing_object_proposal_semantic_patch_guards": guards,
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
    print(f"candidate_semantic_patch_receipt_id={receipt_id}")
    print(f"candidate_semantic_patch_receipt_path=data/candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0_receipts/{receipt_id}.json")
    print(f"semantically_patched_candidate_path=data/candidate_missing_object_proposal_semantic_patch_r1000_taxonomy_gap_v0/r1000_top_group_taxonomy_gap_semantically_patched_candidate_missing_object_proposal.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
