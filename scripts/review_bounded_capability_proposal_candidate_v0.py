#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_BOUNDED_CAPABILITY_PROPOSAL_CANDIDATE_V0"
TARGET_UNIT_ID = "bounded_capability_proposal.review_candidate_v0"
NEXT_UNIT_ID_IF_VALID = "PREPARE_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_V0"

ADAPTER_CLOSURE_RECEIPT_ID = "capability_adapter_reference_closure_receipt_b02a18a5"
PROPOSAL_ID = "capability_proposal_57dda6e9"

ADAPTER_CLOSURE_RECEIPT_PATH = ROOT / "data/capability_proposal_adapter_reference_closure_v0_receipts/capability_adapter_reference_closure_receipt_b02a18a5.json"
PENDING_REVIEW_POINTER_PATH = ROOT / "data/capability_proposal_adapter_reference_closure_v0/bounded_capability_proposal_pending_review_pointer_v0.json"
ADAPTER_REFERENCE_INDEX_PATH = ROOT / "data/capability_proposal_adapter_reference_closure_v0/capability_proposal_adapter_reviewed_reference_index_v0.json"
ADAPTER_FREEZE_MANIFEST_PATH = ROOT / "data/capability_proposal_adapter_reference_closure_v0/capability_proposal_adapter_reference_freeze_manifest_v0.json"

PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
HUMAN_DECISION_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/human_capability_decision_packet_v0.json"
STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"
ADAPTER_RECEIPT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0_receipts/capability_adapter_receipt_8c7f0905.json"

OUT_DIR = ROOT / "data/bounded_capability_proposal_review_v0"
RECEIPT_DIR = ROOT / "data/bounded_capability_proposal_review_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_capability_proposal_review_basis_v0.json"
SOURCE_ALIGNMENT_REVIEW_PATH = OUT_DIR / "bounded_capability_proposal_source_alignment_review_v0.json"
SCOPE_REVIEW_PATH = OUT_DIR / "bounded_capability_proposal_scope_review_v0.json"
NON_GOALS_REVIEW_PATH = OUT_DIR / "bounded_capability_proposal_non_goals_review_v0.json"
RECEIPTS_REVIEW_PATH = OUT_DIR / "bounded_capability_proposal_required_receipts_review_v0.json"
ACCEPTANCE_REVIEW_PATH = OUT_DIR / "bounded_capability_proposal_acceptance_conditions_review_v0.json"
HUMAN_DECISION_REVIEW_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_review_v0.json"
VALIDATION_PATH_TARGET_PATH = OUT_DIR / "bounded_capability_proposal_validation_path_target_v0.json"
READOUT_PATH = OUT_DIR / "bounded_capability_proposal_review_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_capability_proposal_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_capability_proposal_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_capability_proposal_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_capability_proposal_review_transition_trace.json"

REQUIRED_PROPOSAL_FIELDS = [
    "schema_version",
    "proposal_id",
    "proposal_kind",
    "proposal_status",
    "source_stop_packet_id",
    "source_unit_id",
    "source_receipt_ref",
    "required_capability",
    "missing_objects_addressed",
    "shared_missing_boundary",
    "proposed_surface",
    "scope",
    "non_goals",
    "required_receipts",
    "acceptance_conditions",
    "boundary_guards",
    "human_decision_options",
    "validator_requirements",
    "must_not_infer",
]

EXPECTED_MISSING_OBJECTS = [
    "loop_trigger_surface_missing",
    "structured_tie_evidence_missing",
]

EXPECTED_REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
EXPECTED_PROPOSAL_KIND = "BOUNDED_TRIGGER_SURFACE_CAPABILITY_PROPOSAL"
EXPECTED_PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"

REQUIRED_NON_GOAL_TERMS = [
    "does not implement the capability",
    "does not repair the source unit",
    "does not add runtime moves",
    "does not mutate schema archive",
    "does not expand fixtures by default",
    "does not patch runtime",
    "does not authorize runtime adoption",
    "does not authorize C8",
    "does not create live control authority",
]

REQUIRED_RECEIPT_TERMS = [
    "capability design receipt",
    "capability build receipt",
    "capability review receipt",
    "negative-control receipt",
    "acceptance-gate receipt",
    "source-stop linkage receipt",
    "validator receipt",
    "human decision receipt",
]

REQUIRED_HUMAN_DECISIONS = [
    "ACCEPT_FOR_BOUNDED_IMPLEMENTATION",
    "REJECT",
    "EDIT_AND_RESUBMIT",
    "DEFER",
    "FREEZE_AS_REFERENCE_ONLY",
    "REQUEST_NARROWER_PROPOSAL",
    "REQUEST_ALTERNATE_PROPOSAL",
    "CLOSE_SOURCE_BRANCH_FOR_CURRENT_REGISTRY_ONLY",
]

FORBIDDEN_SCOPE_TERMS = [
    "runtime repair",
    "runtime adoption",
    "move registry mutation",
    "schema archive mutation",
    "fixture expansion by default",
    "global architecture change",
    "C7/C8 expansion",
    "live hook installation",
    "authority widening",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def require_false(obj: Dict[str, Any], key: str, failures: List[str]) -> None:
    if obj.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{obj.get(key)}")

def text_list_contains(items: List[Any], needle: str) -> bool:
    blob = "\n".join(str(x).lower() for x in items)
    return needle.lower() in blob

def any_forbidden_scope(scope: List[Any]) -> List[str]:
    """Return forbidden terms only when used as positive scope claims.

    A forbidden term appearing inside negative/boundary language is not itself
    a positive scope claim. Examples that must not trip this detector:
    "does not authorize runtime repair", "no fixture expansion by default",
    "negative-control receipt proves no runtime repair".
    """
    negative_markers = [
        "does not",
        "do not",
        "must not",
        "not ",
        " no ",
        "no ",
        "without",
        "forbid",
        "forbidden",
        "negative-control",
        "negative control",
        "boundary guard",
        "boundary",
        "guard",
        "non-goal",
        "non goal",
        "must_not_infer",
        "does_not_authorize",
        "not authorize",
        "does not authorize",
        "proves no",
        "remain zero",
        "zero",
    ]
    positive_hits: List[str] = []
    for item in scope:
        line = str(item).lower()
        for term in FORBIDDEN_SCOPE_TERMS:
            t = term.lower()
            if t not in line:
                continue
            if any(marker in line for marker in negative_markers):
                continue
            positive_hits.append(term)
    return sorted(set(positive_hits))

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        ADAPTER_CLOSURE_RECEIPT_PATH,
        PENDING_REVIEW_POINTER_PATH,
        ADAPTER_REFERENCE_INDEX_PATH,
        ADAPTER_FREEZE_MANIFEST_PATH,
        PROPOSAL_PATH,
        HUMAN_DECISION_PACKET_PATH,
        STOP_PACKET_PATH,
        ADAPTER_RECEIPT_PATH,
    ]

    failures: List[str] = []
    review_findings: List[Dict[str, Any]] = []

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    adapter_closure = read_json(ADAPTER_CLOSURE_RECEIPT_PATH)
    pending_pointer = read_json(PENDING_REVIEW_POINTER_PATH)
    reference_index = read_json(ADAPTER_REFERENCE_INDEX_PATH)
    freeze_manifest = read_json(ADAPTER_FREEZE_MANIFEST_PATH)
    proposal = read_json(PROPOSAL_PATH)
    human_decision = read_json(HUMAN_DECISION_PACKET_PATH)
    stop_packet = read_json(STOP_PACKET_PATH)
    adapter_receipt = read_json(ADAPTER_RECEIPT_PATH)

    closure_summary = adapter_closure.get("machine_readable_capability_proposal_adapter_reference_closure_summary", {})
    adapter_summary = adapter_receipt.get("machine_readable_capability_proposal_adapter_summary", {})

    # Basis checks.
    if adapter_closure.get("receipt_id") != ADAPTER_CLOSURE_RECEIPT_ID:
        failures.append(f"adapter_closure_receipt_id_wrong:{adapter_closure.get('receipt_id')}")
    if adapter_closure.get("gate") != "PASS":
        failures.append("adapter_closure_gate_not_pass")
    if closure_summary.get("adapter_reference_branch_closed") is not True:
        failures.append("adapter_reference_branch_not_closed")
    if closure_summary.get("proposal_review_pending") is not True:
        failures.append("closure_did_not_mark_proposal_review_pending")
    if closure_summary.get("followup_proposal_review_unit_id") != UNIT_ID:
        failures.append(f"closure_followup_wrong:{closure_summary.get('followup_proposal_review_unit_id')}")

    if pending_pointer.get("pending_review") is not True:
        failures.append("pending_pointer_not_pending")
    if pending_pointer.get("pending_review_unit_id") != UNIT_ID:
        failures.append(f"pending_pointer_unit_wrong:{pending_pointer.get('pending_review_unit_id')}")
    if pending_pointer.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"pending_pointer_proposal_id_wrong:{pending_pointer.get('proposal_id')}")

    # Proposal required shape.
    missing_fields = [field for field in REQUIRED_PROPOSAL_FIELDS if field not in proposal]
    if missing_fields:
        failures.append(f"proposal_required_fields_missing:{missing_fields}")

    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal.get("schema_version") != "bounded_capability_proposal_v0":
        failures.append(f"proposal_schema_version_wrong:{proposal.get('schema_version')}")
    if proposal.get("proposal_status") != "PROPOSAL_CANDIDATE_ONLY":
        failures.append(f"proposal_status_wrong:{proposal.get('proposal_status')}")
    if proposal.get("proposal_kind") != EXPECTED_PROPOSAL_KIND:
        failures.append(f"proposal_kind_wrong:{proposal.get('proposal_kind')}")
    if proposal.get("required_capability") != EXPECTED_REQUIRED_CAPABILITY:
        failures.append(f"required_capability_wrong:{proposal.get('required_capability')}")
    if proposal.get("missing_objects_addressed") != EXPECTED_MISSING_OBJECTS:
        failures.append(f"missing_objects_addressed_wrong:{proposal.get('missing_objects_addressed')}")
    if proposal.get("proposed_surface") != EXPECTED_PROPOSED_SURFACE:
        failures.append(f"proposed_surface_wrong:{proposal.get('proposed_surface')}")
    if proposal.get("source_stop_packet_id") != stop_packet.get("stop_packet_id"):
        failures.append("source_stop_packet_id_mismatch")
    if proposal.get("source_receipt_ref") != adapter_receipt.get("source_receipt_ref"):
        review_findings.append({
            "finding_id": "PROPOSAL_REVIEW_FINDING_SOURCE_RECEIPT_REF_DIFFERS_FROM_ADAPTER_SOURCE_RECEIPT_REF",
            "severity": "OBSERVATION_ONLY",
            "finding_kind": "SOURCE_REF_ALIGNMENT_NOTE",
            "proposal_source_receipt_ref": proposal.get("source_receipt_ref"),
            "adapter_source_receipt_ref": adapter_receipt.get("source_receipt_ref"),
            "blocks_validation_path": False,
        })

    # Boundary checks.
    proposal_guards = proposal.get("boundary_guards", {})
    for key in [
        "implementation_authorized",
        "runtime_patch_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "c8_authorized",
    ]:
        require_false(proposal_guards, key, failures)

    for key in [
        "proposal_accepted",
        "proposal_validated",
        "implementation_authorized",
        "runtime_adoption_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "runtime_patch_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        if key in closure_summary:
            require_false(closure_summary, key, failures)
        if key in pending_pointer:
            require_false(pending_pointer, key, failures)

    # Scope/non-goals/reviewability.
    scope = proposal.get("scope") or []
    non_goals = proposal.get("non_goals") or []
    required_receipts = proposal.get("required_receipts") or []
    acceptance_conditions = proposal.get("acceptance_conditions") or []
    human_options_text = proposal.get("human_decision_options") or []
    validator_requirements = proposal.get("validator_requirements") or []
    must_not_infer = proposal.get("must_not_infer") or []

    if not isinstance(scope, list) or len(scope) < 5:
        failures.append("scope_missing_or_too_small")
    forbidden_scope_hits = any_forbidden_scope(scope)
    if forbidden_scope_hits:
        failures.append(f"forbidden_scope_terms_present:{forbidden_scope_hits}")

    missing_non_goals = [term for term in REQUIRED_NON_GOAL_TERMS if not text_list_contains(non_goals, term)]
    if missing_non_goals:
        failures.append(f"required_non_goals_missing:{missing_non_goals}")

    missing_receipts = [term for term in REQUIRED_RECEIPT_TERMS if not text_list_contains(required_receipts, term)]
    if missing_receipts:
        failures.append(f"required_receipts_missing:{missing_receipts}")

    if not isinstance(acceptance_conditions, list) or len(acceptance_conditions) < 5:
        failures.append("acceptance_conditions_missing_or_too_small")
    acceptance_blob = "\n".join(str(x).lower() for x in acceptance_conditions)
    for required_phrase in [
        "distinguish loop trigger present",
        "structured move-tie evidence",
        "missing object",
        "receipt proves no authority widening",
        "negative controls remain zero",
    ]:
        if required_phrase not in acceptance_blob:
            failures.append(f"acceptance_condition_phrase_missing:{required_phrase}")

    if not isinstance(validator_requirements, list) or len(validator_requirements) < 5:
        failures.append("validator_requirements_missing_or_too_small")
    validator_blob = "\n".join(str(x).lower() for x in validator_requirements)
    for required_phrase in [
        "well formed",
        "typed",
        "source stop packet",
        "missing-object distinction",
        "boundary flags",
    ]:
        if required_phrase not in validator_blob:
            failures.append(f"validator_requirement_phrase_missing:{required_phrase}")

    must_not_blob = "\n".join(str(x).lower() for x in must_not_infer)
    for required_phrase in [
        "proposal accepted",
        "implementation authorized",
        "runtime repair authorized",
        "schema mutation authorized",
        "move addition authorized",
        "runtime adoption authorized",
        "c8 authorized",
    ]:
        if required_phrase not in must_not_blob:
            failures.append(f"must_not_infer_phrase_missing:{required_phrase}")

    if human_decision.get("proposal_id") != PROPOSAL_ID:
        failures.append("human_decision_packet_proposal_id_wrong")
    if human_decision.get("decision_required") is not True:
        failures.append("human_decision_required_false")
    if human_decision.get("default_decision") != "DEFER":
        failures.append("human_default_decision_not_defer")
    available_decisions = human_decision.get("available_decisions") or []
    missing_human_decisions = [d for d in REQUIRED_HUMAN_DECISIONS if d not in available_decisions]
    if missing_human_decisions:
        failures.append(f"human_decisions_missing:{missing_human_decisions}")

    for key in [
        "implementation_authorized",
        "runtime_adoption_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "c8_authorized",
    ]:
        require_false(human_decision, key, failures)

    # Determine review classification.
    gate = "PASS" if not failures else "FAIL"
    content_review_verdict = (
        "VALID_PROPOSAL_CANDIDATE_READY_FOR_VALIDATION_PATH"
        if gate == "PASS"
        else "BOUNDED_CAPABILITY_PROPOSAL_REVIEW_GATE_FAIL"
    )
    status = (
        "TYPED_BOUNDED_CAPABILITY_PROPOSAL_REVIEW_PASS_READY_FOR_VALIDATION_PATH"
        if gate == "PASS"
        else "TYPED_BOUNDED_CAPABILITY_PROPOSAL_REVIEW_GATE_FAIL"
    )

    proposal_review_id = "bounded_capability_proposal_review_" + sig8({
        "proposal_id": proposal.get("proposal_id"),
        "proposal_kind": proposal.get("proposal_kind"),
        "proposed_surface": proposal.get("proposed_surface"),
        "source_stop_packet_id": proposal.get("source_stop_packet_id"),
        "adapter_reference_id": closure_summary.get("reference_id"),
    })

    basis = {
        "schema_version": "bounded_capability_proposal_review_basis_v0",
        "unit_id": UNIT_ID,
        "proposal_review_id": proposal_review_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_adapter_closure_receipt_id": ADAPTER_CLOSURE_RECEIPT_ID,
        "source_adapter_reference_id": closure_summary.get("reference_id"),
        "source_proposal_id": PROPOSAL_ID,
        "basis_claim": "Review bounded capability proposal candidate content only. Do not validate, accept, implement, or mutate runtime/schema/move registries.",
        "source_file_hashes": {rel(p): file_sha256(p) for p in required_files},
    }

    source_alignment_review = {
        "schema_version": "bounded_capability_proposal_source_alignment_review_v0",
        "proposal_review_id": proposal_review_id,
        "review_status": "PASS" if gate == "PASS" else "FAIL",
        "source_stop_packet_id_matches": proposal.get("source_stop_packet_id") == stop_packet.get("stop_packet_id"),
        "missing_objects_preserved": proposal.get("missing_objects_addressed") == EXPECTED_MISSING_OBJECTS,
        "required_capability_preserved": proposal.get("required_capability") == EXPECTED_REQUIRED_CAPABILITY,
        "proposal_kind_fits_source": proposal.get("proposal_kind") == EXPECTED_PROPOSAL_KIND,
        "proposed_surface_fits_required_capability": proposal.get("proposed_surface") == EXPECTED_PROPOSED_SURFACE,
        "source_stop_packet_ref": rel(STOP_PACKET_PATH),
        "proposal_ref": rel(PROPOSAL_PATH),
        "findings": review_findings,
    }

    scope_review = {
        "schema_version": "bounded_capability_proposal_scope_review_v0",
        "proposal_review_id": proposal_review_id,
        "review_status": "PASS" if gate == "PASS" else "FAIL",
        "scope_count": len(scope) if isinstance(scope, list) else 0,
        "scope": scope,
        "forbidden_scope_hits": forbidden_scope_hits,
        "scope_narrow_enough": not forbidden_scope_hits and isinstance(scope, list) and len(scope) >= 5,
        "scope_interpretation": "Scope is narrow/source-bound and aims at representability of T6 trigger evidence, not runtime repair."
        if gate == "PASS" else "Scope review found blocking failures.",
    }

    non_goals_review = {
        "schema_version": "bounded_capability_proposal_non_goals_review_v0",
        "proposal_review_id": proposal_review_id,
        "review_status": "PASS" if not missing_non_goals else "FAIL",
        "non_goals_count": len(non_goals) if isinstance(non_goals, list) else 0,
        "required_non_goals": REQUIRED_NON_GOAL_TERMS,
        "missing_required_non_goals": missing_non_goals,
        "non_goals_strong_enough": not missing_non_goals,
    }

    receipts_review = {
        "schema_version": "bounded_capability_proposal_required_receipts_review_v0",
        "proposal_review_id": proposal_review_id,
        "review_status": "PASS" if not missing_receipts else "FAIL",
        "required_receipts_count": len(required_receipts) if isinstance(required_receipts, list) else 0,
        "required_receipts_expected": REQUIRED_RECEIPT_TERMS,
        "missing_required_receipts": missing_receipts,
        "receipt_burden_sufficient": not missing_receipts,
    }

    acceptance_review = {
        "schema_version": "bounded_capability_proposal_acceptance_conditions_review_v0",
        "proposal_review_id": proposal_review_id,
        "review_status": "PASS" if gate == "PASS" else "FAIL",
        "acceptance_conditions_count": len(acceptance_conditions) if isinstance(acceptance_conditions, list) else 0,
        "acceptance_conditions": acceptance_conditions,
        "observable_enough": gate == "PASS",
        "acceptance_interpretation": "Acceptance conditions are observable: they require distinguishability, explicit missing-object representation, no authority widening, and zero negative controls."
        if gate == "PASS" else "Acceptance conditions review found blocking failures.",
    }

    human_decision_review = {
        "schema_version": "bounded_capability_proposal_human_decision_review_v0",
        "proposal_review_id": proposal_review_id,
        "review_status": "PASS" if not missing_human_decisions else "FAIL",
        "decision_required": human_decision.get("decision_required"),
        "default_decision": human_decision.get("default_decision"),
        "available_decisions": available_decisions,
        "missing_decisions": missing_human_decisions,
        "proposal_accepted": False,
        "implementation_authorized": False,
        "human_packet_complete": not missing_human_decisions and human_decision.get("decision_required") is True,
    }

    validation_path_target = {
        "schema_version": "bounded_capability_proposal_validation_path_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID_IF_VALID if gate == "PASS" else None,
        "proposal_review_id": proposal_review_id,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_ref": rel(PROPOSAL_PATH),
        "human_decision_packet_ref": rel(HUMAN_DECISION_PACKET_PATH),
        "adapter_reference_id": closure_summary.get("reference_id"),
        "validation_path_required": True if gate == "PASS" else False,
        "validator_requirements_ref": rel(PROPOSAL_PATH),
        "required_validation_checks": [
            "well formed proposal packet",
            "typed proposal kind",
            "source stop packet cited",
            "missing objects preserved",
            "required capability preserved",
            "scope and non-goals present",
            "required receipts present",
            "acceptance conditions observable",
            "human decision options complete",
            "boundary guards all false",
            "no implementation or acceptance claim",
        ],
        "does_not_authorize": [
            "proposal acceptance",
            "implementation",
            "runtime repair",
            "runtime patch",
            "schema mutation",
            "move addition",
            "fixture expansion",
            "runtime adoption",
            "C8 authorization",
        ],
    }

    rollup = {
        "schema_version": "bounded_capability_proposal_review_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "proposal_review_id": proposal_review_id,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_kind": proposal.get("proposal_kind"),
        "proposed_surface": proposal.get("proposed_surface"),
        "content_review_verdict": content_review_verdict,
        "source_alignment_pass": source_alignment_review["review_status"] == "PASS",
        "scope_review_pass": scope_review["review_status"] == "PASS",
        "non_goals_review_pass": non_goals_review["review_status"] == "PASS",
        "required_receipts_review_pass": receipts_review["review_status"] == "PASS",
        "acceptance_conditions_review_pass": acceptance_review["review_status"] == "PASS",
        "human_decision_review_pass": human_decision_review["review_status"] == "PASS",
        "validation_path_ready": gate == "PASS",
        "proposal_accepted": False,
        "proposal_validated": False,
        "implementation_authorized": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "runtime_patch_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "next_unit_id": NEXT_UNIT_ID_IF_VALID if gate == "PASS" else None,
    }

    readout = {
        "schema_version": "bounded_capability_proposal_review_readout_v0",
        "proposal_review_id": proposal_review_id,
        "status": status,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_kind": proposal.get("proposal_kind"),
        "proposed_surface": proposal.get("proposed_surface"),
        "review_verdict": content_review_verdict,
        "validation_path_ready": gate == "PASS",
        "next_unit_id": NEXT_UNIT_ID_IF_VALID if gate == "PASS" else None,
        "interpretation": "Proposal candidate content is review-clean and ready for a later validation/admissibility path. This review did not validate, accept, or implement the proposal."
        if gate == "PASS" else "Proposal content review found blocking failures.",
    }

    profile = {
        "schema_version": "bounded_capability_proposal_review_profile_v0",
        "profile_status": status,
        "proposal_review_id": proposal_review_id,
        "core_rule": "Review bounded proposal content only; do not accept, validate, implement, repair runtime, or mutate schema/move registries.",
        "proposal_ref": rel(PROPOSAL_PATH),
        "human_decision_packet_ref": rel(HUMAN_DECISION_PACKET_PATH),
        "validation_path_target_ref": rel(VALIDATION_PATH_TARGET_PATH),
        "validation_path_ready": gate == "PASS",
        "next_unit_id": NEXT_UNIT_ID_IF_VALID if gate == "PASS" else None,
        "must_not_infer": [
            "proposal accepted",
            "proposal validated",
            "capability implementation authorized",
            "runtime repaired",
            "runtime adoption authorized",
            "schema mutation authorized",
            "move addition authorized",
            "fixtures may expand by default",
            "C8 authorized",
        ],
    }

    report = {
        "schema_version": "bounded_capability_proposal_review_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "proposal_result": content_review_verdict,
            "proposal_id": proposal.get("proposal_id"),
            "proposal_kind": proposal.get("proposal_kind"),
            "proposed_surface": proposal.get("proposed_surface"),
            "content_review_clean": gate == "PASS",
            "validation_path_ready": gate == "PASS",
            "proposal_accepted": False,
            "proposal_validated": False,
            "implementation_authorized": False,
        },
        "findings": review_findings,
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_capability_proposal_review_transition_trace_v0",
        "unit_id": UNIT_ID,
        "proposal_review_id": proposal_review_id,
        "transitions": [
            {
                "from": "PROPOSAL_CANDIDATE_ONLY_PENDING_REVIEW",
                "edge": "review source alignment, scope, non-goals, receipts, acceptance conditions, human decision packet",
                "to": "VALID_PROPOSAL_CANDIDATE_CONTENT" if gate == "PASS" else "PROPOSAL_REVIEW_GATE_FAIL",
            },
            {
                "from": "VALID_PROPOSAL_CANDIDATE_CONTENT" if gate == "PASS" else "PROPOSAL_REVIEW_GATE_FAIL",
                "edge": "prepare validation path target without acceptance",
                "to": "READY_FOR_VALIDATION_PATH" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID_IF_VALID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_CAPABILITY_PROPOSAL_REVIEW_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (SOURCE_ALIGNMENT_REVIEW_PATH, source_alignment_review),
        (SCOPE_REVIEW_PATH, scope_review),
        (NON_GOALS_REVIEW_PATH, non_goals_review),
        (RECEIPTS_REVIEW_PATH, receipts_review),
        (ACCEPTANCE_REVIEW_PATH, acceptance_review),
        (HUMAN_DECISION_REVIEW_PATH, human_decision_review),
        (VALIDATION_PATH_TARGET_PATH, validation_path_target),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "ADAPTER_REFERENCE_CLOSURE_CONSUMED",
        "PROPOSAL_PENDING_REVIEW_POINTER_CONSUMED",
        "PROPOSAL_CANDIDATE_CONSUMED",
        "SOURCE_STOP_PACKET_ALIGNMENT_REVIEWED",
        "MISSING_OBJECTS_PRESERVED",
        "REQUIRED_CAPABILITY_PRESERVED",
        "PROPOSAL_KIND_FITS_SOURCE",
        "PROPOSED_SURFACE_FITS_REQUIRED_CAPABILITY",
        "SCOPE_REVIEWED_NARROW_SOURCE_BOUND",
        "NON_GOALS_REVIEWED_STRONG",
        "REQUIRED_RECEIPTS_REVIEWED_SUFFICIENT",
        "ACCEPTANCE_CONDITIONS_REVIEWED_OBSERVABLE",
        "HUMAN_DECISION_PACKET_REVIEWED_COMPLETE",
        "VALIDATION_PATH_TARGET_EMITTED",
        "NO_PROPOSAL_VALIDATION",
        "NO_PROPOSAL_ACCEPTANCE",
        "NO_IMPLEMENTATION",
        "NO_RUNTIME_REPAIR",
        "NO_SCHEMA_MUTATION",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_RUNTIME_PATCH",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "bounded_capability_proposal_review_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_CAPABILITY_PROPOSAL_REVIEW_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "proposal_review_id": proposal_review_id,
        "source_adapter_closure_receipt_id": ADAPTER_CLOSURE_RECEIPT_ID,
        "source_adapter_closure_receipt_ref": rel(ADAPTER_CLOSURE_RECEIPT_PATH),
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "review_findings": review_findings,
        "acceptance_gate_results": {
            "PROPOSAL_REVIEW_0_ADAPTER_CLOSURE_CONSUMED": gate == "PASS",
            "PROPOSAL_REVIEW_1_PENDING_POINTER_CONSUMED": gate == "PASS",
            "PROPOSAL_REVIEW_2_PROPOSAL_CANDIDATE_ONLY": proposal.get("proposal_status") == "PROPOSAL_CANDIDATE_ONLY",
            "PROPOSAL_REVIEW_3_SOURCE_ALIGNMENT_PASS": source_alignment_review["review_status"] == "PASS",
            "PROPOSAL_REVIEW_4_SCOPE_PASS": scope_review["review_status"] == "PASS",
            "PROPOSAL_REVIEW_5_NON_GOALS_PASS": non_goals_review["review_status"] == "PASS",
            "PROPOSAL_REVIEW_6_REQUIRED_RECEIPTS_PASS": receipts_review["review_status"] == "PASS",
            "PROPOSAL_REVIEW_7_ACCEPTANCE_CONDITIONS_PASS": acceptance_review["review_status"] == "PASS",
            "PROPOSAL_REVIEW_8_HUMAN_DECISION_PACKET_PASS": human_decision_review["review_status"] == "PASS",
            "PROPOSAL_REVIEW_9_NO_PROPOSAL_VALIDATION": True,
            "PROPOSAL_REVIEW_10_NO_PROPOSAL_ACCEPTANCE": True,
            "PROPOSAL_REVIEW_11_NO_IMPLEMENTATION": True,
            "PROPOSAL_REVIEW_12_NO_RUNTIME_REPAIR": True,
            "PROPOSAL_REVIEW_13_NO_SCHEMA_MUTATION": True,
            "PROPOSAL_REVIEW_14_NO_MOVE_ADDITION": True,
            "PROPOSAL_REVIEW_15_NO_C8_AUTHORIZATION": True,
            "PROPOSAL_REVIEW_16_VALIDATION_PATH_TARGET_EMITTED": VALIDATION_PATH_TARGET_PATH.exists() and gate == "PASS",
            "PROPOSAL_REVIEW_17_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_capability_proposal_review_summary": {
            "status": status,
            "proposal_review_id": proposal_review_id,
            "proposal_id": proposal.get("proposal_id"),
            "proposal_kind": proposal.get("proposal_kind"),
            "proposed_surface": proposal.get("proposed_surface"),
            "proposal_status": proposal.get("proposal_status"),
            "review_verdict": content_review_verdict,
            "content_review_clean": gate == "PASS",
            "validation_path_ready": gate == "PASS",
            "next_unit_id": NEXT_UNIT_ID_IF_VALID if gate == "PASS" else None,
            "proposal_accepted": False,
            "proposal_validated": False,
            "human_decision_taken": False,
            "implementation_authorized": False,
            "runtime_adoption_authorized": False,
            "schema_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "runtime_patch_authorized": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "source_alignment_review": rel(SOURCE_ALIGNMENT_REVIEW_PATH),
            "scope_review": rel(SCOPE_REVIEW_PATH),
            "non_goals_review": rel(NON_GOALS_REVIEW_PATH),
            "required_receipts_review": rel(RECEIPTS_REVIEW_PATH),
            "acceptance_conditions_review": rel(ACCEPTANCE_REVIEW_PATH),
            "human_decision_review": rel(HUMAN_DECISION_REVIEW_PATH),
            "validation_path_target": rel(VALIDATION_PATH_TARGET_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_capability_proposal_review_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_capability_proposal_review_receipt_id={receipt_id}")
    print(f"bounded_capability_proposal_review_receipt_path={rel(receipt_path)}")
    print(f"bounded_capability_proposal_review_next_unit={NEXT_UNIT_ID_IF_VALID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
