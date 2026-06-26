#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "AUDIT_BOUNDED_CAPABILITY_PROPOSAL_ADMISSIBILITY_SCOPE_BINDING_FAILURE_V0"
TARGET_UNIT_ID = "bounded_capability_proposal.admissibility_scope_binding_failure_audit_v0"

FAILED_VALIDATION_RUN_RECEIPT_ID = "bounded_capability_proposal_validation_path_run_receipt_f39ec164"
PROPOSAL_ID = "capability_proposal_57dda6e9"

FAILED_VALIDATION_RUN_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0_receipts/bounded_capability_proposal_validation_path_run_receipt_f39ec164.json"

VALIDATION_PATH_PREP_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0_receipts/bounded_capability_proposal_validation_path_prep_receipt_ec27c6e9.json"
VALIDATION_RUN_TARGET_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0/bounded_capability_proposal_validation_run_target_v0.json"
ADMISSIBILITY_CONTRACT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0/bounded_capability_proposal_lawful_admissibility_contract_v0.json"
SOURCE_LINKAGE_CONTRACT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0/bounded_capability_proposal_source_linkage_contract_v0.json"

VALIDATION_RUN_ADMISSIBILITY_RESULT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0/bounded_capability_proposal_lawful_admissibility_result_v0.json"
VALIDATION_RUN_SOURCE_LINKAGE_RESULT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0/bounded_capability_proposal_source_linkage_result_v0.json"
VALIDATION_RUN_SCHEMA_RESULT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0/bounded_capability_proposal_schema_validation_result_v0.json"
VALIDATION_RUN_BOUNDARY_RESULT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0/bounded_capability_proposal_boundary_guard_result_v0.json"
VALIDATION_RUN_NEGATIVE_RESULT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0/bounded_capability_proposal_negative_control_result_v0.json"
VALIDATION_RUN_HUMAN_GATE_RESULT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0/bounded_capability_proposal_human_decision_gate_result_v0.json"

PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"
HUMAN_DECISION_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/human_capability_decision_packet_v0.json"
ADAPTER_RECEIPT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0_receipts/capability_adapter_receipt_8c7f0905.json"
ADAPTER_CLOSURE_RECEIPT_PATH = ROOT / "data/capability_proposal_adapter_reference_closure_v0_receipts/capability_adapter_reference_closure_receipt_b02a18a5.json"

OUT_DIR = ROOT / "data/bounded_capability_proposal_admissibility_scope_binding_failure_audit_v0"
RECEIPT_DIR = ROOT / "data/bounded_capability_proposal_admissibility_scope_binding_failure_audit_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_capability_proposal_admissibility_scope_binding_failure_audit_basis_v0.json"
FAILURE_SURFACE_PATH = OUT_DIR / "bounded_capability_proposal_admissibility_scope_binding_failure_surface_v0.json"
STRUCTURAL_BINDING_REVIEW_PATH = OUT_DIR / "bounded_capability_proposal_structural_capability_boundary_binding_review_v0.json"
SCOPE_PHRASE_REVIEW_PATH = OUT_DIR / "bounded_capability_proposal_scope_phrase_binding_review_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "bounded_capability_proposal_admissibility_scope_binding_failure_classification_v0.json"
REPAIR_TARGET_PATH = OUT_DIR / "bounded_capability_proposal_admissibility_scope_binding_repair_target_v0.json"
READOUT_PATH = OUT_DIR / "bounded_capability_proposal_admissibility_scope_binding_failure_audit_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_capability_proposal_admissibility_scope_binding_failure_audit_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_capability_proposal_admissibility_scope_binding_failure_audit_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_capability_proposal_admissibility_scope_binding_failure_audit_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_capability_proposal_admissibility_scope_binding_failure_audit_transition_trace.json"

EXPECTED_FAILURE = "lawful_admissibility_failures:['scope_missing_capability_boundary_binding']"
EXPECTED_PROPOSAL_KIND = "BOUNDED_TRIGGER_SURFACE_CAPABILITY_PROPOSAL"
EXPECTED_REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
EXPECTED_PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"
EXPECTED_MISSING_OBJECTS = [
    "loop_trigger_surface_missing",
    "structured_tie_evidence_missing",
]

NEXT_REPAIR_VALIDATOR = "REPAIR_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_SCOPE_BINDING_CLASSIFIER_V0"
NEXT_EDIT_PROPOSAL = "PREPARE_BOUNDED_CAPABILITY_PROPOSAL_SCOPE_BINDING_LOCAL_EDIT_V0"
NEXT_INVESTIGATE = "INVESTIGATE_BOUNDED_CAPABILITY_PROPOSAL_SCOPE_BINDING_AMBIGUITY_V0"

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

def blob_from(value: Any) -> str:
    if isinstance(value, list):
        return "\n".join(str(x).lower() for x in value)
    if isinstance(value, dict):
        return json.dumps(value, sort_keys=True).lower()
    return str(value).lower()

def has_scope_phrase(scope: Any) -> bool:
    blob = blob_from(scope)
    return "capability-boundary" in blob or "capability boundary" in blob

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        FAILED_VALIDATION_RUN_RECEIPT_PATH,
        VALIDATION_PATH_PREP_RECEIPT_PATH,
        VALIDATION_RUN_TARGET_PATH,
        ADMISSIBILITY_CONTRACT_PATH,
        SOURCE_LINKAGE_CONTRACT_PATH,
        VALIDATION_RUN_ADMISSIBILITY_RESULT_PATH,
        VALIDATION_RUN_SOURCE_LINKAGE_RESULT_PATH,
        VALIDATION_RUN_SCHEMA_RESULT_PATH,
        VALIDATION_RUN_BOUNDARY_RESULT_PATH,
        VALIDATION_RUN_NEGATIVE_RESULT_PATH,
        VALIDATION_RUN_HUMAN_GATE_RESULT_PATH,
        PROPOSAL_PATH,
        STOP_PACKET_PATH,
        HUMAN_DECISION_PACKET_PATH,
        ADAPTER_RECEIPT_PATH,
        ADAPTER_CLOSURE_RECEIPT_PATH,
    ]

    failures: List[str] = []

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    failed_run = read_json(FAILED_VALIDATION_RUN_RECEIPT_PATH)
    prep = read_json(VALIDATION_PATH_PREP_RECEIPT_PATH)
    run_target = read_json(VALIDATION_RUN_TARGET_PATH)
    admissibility_contract = read_json(ADMISSIBILITY_CONTRACT_PATH)
    source_linkage_contract = read_json(SOURCE_LINKAGE_CONTRACT_PATH)

    admissibility_result = read_json(VALIDATION_RUN_ADMISSIBILITY_RESULT_PATH)
    source_linkage_result = read_json(VALIDATION_RUN_SOURCE_LINKAGE_RESULT_PATH)
    schema_result = read_json(VALIDATION_RUN_SCHEMA_RESULT_PATH)
    boundary_result = read_json(VALIDATION_RUN_BOUNDARY_RESULT_PATH)
    negative_result = read_json(VALIDATION_RUN_NEGATIVE_RESULT_PATH)
    human_gate_result = read_json(VALIDATION_RUN_HUMAN_GATE_RESULT_PATH)

    proposal = read_json(PROPOSAL_PATH)
    stop_packet = read_json(STOP_PACKET_PATH)
    human_decision = read_json(HUMAN_DECISION_PACKET_PATH)
    adapter_receipt = read_json(ADAPTER_RECEIPT_PATH)
    adapter_closure = read_json(ADAPTER_CLOSURE_RECEIPT_PATH)

    failed_summary = failed_run.get("machine_readable_bounded_capability_proposal_validation_path_run_summary", {})
    prep_summary = prep.get("machine_readable_bounded_capability_proposal_validation_path_prep_summary", {})
    adapter_summary = adapter_receipt.get("machine_readable_capability_proposal_adapter_summary", {})
    closure_summary = adapter_closure.get("machine_readable_capability_proposal_adapter_reference_closure_summary", {})

    observed_failure_list = failed_run.get("failures") or []
    expected_failure_only = observed_failure_list == [EXPECTED_FAILURE]

    # Basis checks.
    if failed_run.get("receipt_id") != FAILED_VALIDATION_RUN_RECEIPT_ID:
        failures.append(f"failed_run_receipt_id_wrong:{failed_run.get('receipt_id')}")
    if failed_run.get("gate") != "FAIL":
        failures.append("failed_run_gate_not_fail")
    if failed_summary.get("status") != "TYPED_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_RUN_GATE_FAIL":
        failures.append("failed_run_status_unexpected")
    if not expected_failure_only:
        failures.append(f"failure_not_single_scope_binding_failure:{observed_failure_list}")

    if admissibility_result.get("result_status") != "LAWFUL_ADMISSIBILITY_FAIL":
        failures.append(f"admissibility_result_status_wrong:{admissibility_result.get('result_status')}")
    if admissibility_result.get("failures") != ["scope_missing_capability_boundary_binding"]:
        failures.append(f"admissibility_failures_wrong:{admissibility_result.get('failures')}")

    for name, obj in [
        ("schema_result", schema_result),
        ("source_linkage_result", source_linkage_result),
        ("boundary_result", boundary_result),
        ("negative_result", negative_result),
        ("human_gate_result", human_gate_result),
    ]:
        if obj.get("pass") is not True:
            failures.append(f"{name}_not_pass")

    # Structural binding review.
    structural_checks = {
        "proposal_id_matches": proposal.get("proposal_id") == PROPOSAL_ID,
        "proposal_kind_is_capability_proposal": proposal.get("proposal_kind") == EXPECTED_PROPOSAL_KIND,
        "proposal_status_candidate_only": proposal.get("proposal_status") == "PROPOSAL_CANDIDATE_ONLY",
        "source_stop_packet_id_matches": proposal.get("source_stop_packet_id") == stop_packet.get("stop_packet_id"),
        "source_stop_code_is_capability_layer_required": stop_packet.get("stop_code") == "STOP_CAPABILITY_LAYER_REQUIRED",
        "missing_objects_preserved": proposal.get("missing_objects_addressed") == stop_packet.get("missing_objects") == EXPECTED_MISSING_OBJECTS,
        "required_capability_preserved": proposal.get("required_capability") == stop_packet.get("required_capability") == EXPECTED_REQUIRED_CAPABILITY,
        "proposed_surface_matches_required_capability_v0": proposal.get("proposed_surface") == EXPECTED_PROPOSED_SURFACE,
        "adapter_source_missing_objects_preserved": adapter_summary.get("missing_objects") == EXPECTED_MISSING_OBJECTS,
        "adapter_required_capability_preserved": adapter_summary.get("required_capability") == EXPECTED_REQUIRED_CAPABILITY,
        "adapter_reference_closed": closure_summary.get("adapter_reference_branch_closed") is True,
        "source_linkage_result_passed": source_linkage_result.get("pass") is True,
        "schema_validation_result_passed": schema_result.get("pass") is True,
    }

    structural_binding_present = all(structural_checks.values())

    # Direct phrase binding review.
    direct_scope_phrase_present = has_scope_phrase(proposal.get("scope"))
    scope_blob = blob_from(proposal.get("scope"))

    # Contract review: did prep contract require structural binding, phrase binding, or both?
    admissibility_required_checks_blob = blob_from(admissibility_contract.get("required_checks"))
    contract_mentions_source_bound = "source-bound" in admissibility_required_checks_blob or "source bound" in admissibility_required_checks_blob
    contract_mentions_capability_boundary = "capability-boundary" in admissibility_required_checks_blob or "capability boundary" in admissibility_required_checks_blob
    source_linkage_contract_ready = source_linkage_contract.get("contract_status") == "READY"

    # Classification.
    if failures:
        classification = "AUDIT_BASIS_FAIL"
        next_unit_id = None
        repair_target_kind = "NONE"
        audit_verdict = "AUDIT_GATE_FAIL"
    elif structural_binding_present and not direct_scope_phrase_present:
        classification = "VALIDATOR_SCOPE_BINDING_PHRASE_OVERSTRICT_STRUCTURAL_BINDING_PRESENT"
        next_unit_id = NEXT_REPAIR_VALIDATOR
        repair_target_kind = "VALIDATOR_CLASSIFIER_REPAIR"
        audit_verdict = "LOCAL_VALIDATOR_REPAIR_RECOMMENDED"
    elif not structural_binding_present:
        classification = "PROPOSAL_SCOPE_BINDING_STRUCTURALLY_UNDERSPECIFIED"
        next_unit_id = NEXT_EDIT_PROPOSAL
        repair_target_kind = "PROPOSAL_LOCAL_EDIT"
        audit_verdict = "LOCAL_PROPOSAL_EDIT_RECOMMENDED"
    else:
        classification = "SCOPE_BINDING_AMBIGUOUS_REQUIRES_INVESTIGATION"
        next_unit_id = NEXT_INVESTIGATE
        repair_target_kind = "AMBIGUITY_INVESTIGATION"
        audit_verdict = "INVESTIGATION_RECOMMENDED"

    gate = "PASS" if not failures and next_unit_id is not None else "FAIL"
    status = (
        "TYPED_BOUNDED_CAPABILITY_PROPOSAL_ADMISSIBILITY_SCOPE_BINDING_FAILURE_AUDIT_PASS_CLASSIFIED"
        if gate == "PASS"
        else "TYPED_BOUNDED_CAPABILITY_PROPOSAL_ADMISSIBILITY_SCOPE_BINDING_FAILURE_AUDIT_GATE_FAIL"
    )

    audit_id = "bounded_capability_proposal_scope_binding_audit_" + sig8({
        "failed_receipt_id": failed_run.get("receipt_id"),
        "proposal_id": proposal.get("proposal_id"),
        "structural_binding_present": structural_binding_present,
        "direct_scope_phrase_present": direct_scope_phrase_present,
        "classification": classification,
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_capability_proposal_admissibility_scope_binding_failure_audit_basis_v0",
        "unit_id": UNIT_ID,
        "audit_id": audit_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "failed_validation_run_receipt_id": FAILED_VALIDATION_RUN_RECEIPT_ID,
        "failed_validation_run_receipt_ref": rel(FAILED_VALIDATION_RUN_RECEIPT_PATH),
        "observed_failure_list": observed_failure_list,
        "expected_failure_only": expected_failure_only,
        "basis_claim": "Classify the admissibility scope-binding failure without editing the proposal, validating it, accepting it, or implementing it.",
        "source_file_hashes": source_hashes,
    }

    failure_surface = {
        "schema_version": "bounded_capability_proposal_admissibility_scope_binding_failure_surface_v0",
        "audit_id": audit_id,
        "failed_validation_run_receipt_id": failed_run.get("receipt_id"),
        "validation_path_id": failed_summary.get("validation_path_id"),
        "validation_run_id": failed_summary.get("validation_run_id"),
        "failed_gate": failed_run.get("gate"),
        "failed_status": failed_summary.get("status"),
        "failed_reason_codes": failed_summary.get("reason_codes"),
        "failed_failures": observed_failure_list,
        "only_failed_check_family": "LAWFUL_ADMISSIBILITY",
        "passed_families": {
            "source_linkage_pass": source_linkage_result.get("pass"),
            "schema_validation_pass": schema_result.get("pass"),
            "boundary_guard_pass": boundary_result.get("pass"),
            "negative_control_pass": negative_result.get("pass"),
            "human_decision_gate_pass": human_gate_result.get("pass"),
        },
    }

    structural_review = {
        "schema_version": "bounded_capability_proposal_structural_capability_boundary_binding_review_v0",
        "audit_id": audit_id,
        "structural_binding_present": structural_binding_present,
        "structural_checks": structural_checks,
        "source_stop_packet_id": stop_packet.get("stop_packet_id"),
        "source_stop_code": stop_packet.get("stop_code"),
        "source_missing_objects": stop_packet.get("missing_objects"),
        "proposal_missing_objects": proposal.get("missing_objects_addressed"),
        "source_required_capability": stop_packet.get("required_capability"),
        "proposal_required_capability": proposal.get("required_capability"),
        "proposal_kind": proposal.get("proposal_kind"),
        "proposed_surface": proposal.get("proposed_surface"),
        "interpretation": (
            "The proposal is structurally bound to the capability-boundary stop through source stop packet linkage, preserved missing objects, preserved required capability, adapter reference closure, schema pass, and source-linkage pass."
            if structural_binding_present else
            "The proposal is not structurally bound strongly enough; a proposal-local edit or source linkage repair is required."
        ),
    }

    scope_phrase_review = {
        "schema_version": "bounded_capability_proposal_scope_phrase_binding_review_v0",
        "audit_id": audit_id,
        "direct_scope_phrase_present": direct_scope_phrase_present,
        "scope_text": proposal.get("scope"),
        "searched_phrases": ["capability-boundary", "capability boundary"],
        "contract_mentions_source_bound": contract_mentions_source_bound,
        "contract_mentions_capability_boundary": contract_mentions_capability_boundary,
        "source_linkage_contract_ready": source_linkage_contract_ready,
        "interpretation": (
            "The proposal scope does not contain the exact phrase required by the run validator, but structural binding evidence is present."
            if structural_binding_present and not direct_scope_phrase_present else
            "Direct phrase binding or structural binding state requires further handling."
        ),
    }

    classification_artifact = {
        "schema_version": "bounded_capability_proposal_admissibility_scope_binding_failure_classification_v0",
        "audit_id": audit_id,
        "classification": classification,
        "audit_verdict": audit_verdict,
        "repair_target_kind": repair_target_kind,
        "next_unit_id": next_unit_id,
        "classification_reason": (
            "Validator used phrase-level scope binding requirement even though source linkage, missing objects, required capability, and proposed surface already establish structural capability-boundary binding."
            if classification == "VALIDATOR_SCOPE_BINDING_PHRASE_OVERSTRICT_STRUCTURAL_BINDING_PRESENT" else
            "Proposal appears structurally underspecified for capability-boundary binding."
            if classification == "PROPOSAL_SCOPE_BINDING_STRUCTURALLY_UNDERSPECIFIED" else
            "Audit could not classify the scope-binding failure cleanly."
        ),
    }

    repair_target = {
        "schema_version": "bounded_capability_proposal_admissibility_scope_binding_repair_target_v0",
        "audit_id": audit_id,
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "repair_target_kind": repair_target_kind,
        "next_unit_id": next_unit_id,
        "failed_validation_run_receipt_id": failed_run.get("receipt_id"),
        "failed_validation_run_receipt_ref": rel(FAILED_VALIDATION_RUN_RECEIPT_PATH),
        "proposal_id": proposal.get("proposal_id"),
        "proposal_ref": rel(PROPOSAL_PATH),
        "repair_instruction": (
            "Repair the validation-run lawful admissibility classifier so scope binding can pass through structural source-stop/capability linkage, not only the literal phrase in proposal scope."
            if repair_target_kind == "VALIDATOR_CLASSIFIER_REPAIR" else
            "Prepare a minimal proposal-local edit adding explicit capability-boundary binding language to scope without changing authority."
            if repair_target_kind == "PROPOSAL_LOCAL_EDIT" else
            "Investigate ambiguous scope-binding evidence before repair."
        ),
        "proposal_edit_authorized": repair_target_kind == "PROPOSAL_LOCAL_EDIT",
        "validator_repair_authorized": repair_target_kind == "VALIDATOR_CLASSIFIER_REPAIR",
        "proposal_acceptance_authorized": False,
        "proposal_validation_authorized": False,
        "human_decision_taken": False,
        "implementation_authorized": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "runtime_patch_authorized": False,
        "c8_authorized": False,
    }

    rollup = {
        "schema_version": "bounded_capability_proposal_admissibility_scope_binding_failure_audit_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "audit_id": audit_id,
        "failed_validation_run_receipt_id": failed_run.get("receipt_id"),
        "proposal_id": proposal.get("proposal_id"),
        "classification": classification,
        "audit_verdict": audit_verdict,
        "structural_binding_present": structural_binding_present,
        "direct_scope_phrase_present": direct_scope_phrase_present,
        "repair_target_kind": repair_target_kind,
        "next_unit_id": next_unit_id,
        "proposal_edited": False,
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
    }

    readout = {
        "schema_version": "bounded_capability_proposal_admissibility_scope_binding_failure_audit_readout_v0",
        "status": status,
        "audit_id": audit_id,
        "classification": classification,
        "audit_verdict": audit_verdict,
        "repair_target_kind": repair_target_kind,
        "next_unit_id": next_unit_id,
        "interpretation": (
            "The proposal has structural capability-boundary binding; the validation runner was over-strict by requiring an exact phrase in scope."
            if classification == "VALIDATOR_SCOPE_BINDING_PHRASE_OVERSTRICT_STRUCTURAL_BINDING_PRESENT" else
            "The proposal needs a minimal local scope-binding edit before validation can rerun."
            if classification == "PROPOSAL_SCOPE_BINDING_STRUCTURALLY_UNDERSPECIFIED" else
            "The scope-binding failure remains ambiguous."
        ),
    }

    profile = {
        "schema_version": "bounded_capability_proposal_admissibility_scope_binding_failure_audit_profile_v0",
        "profile_status": status,
        "audit_id": audit_id,
        "core_rule": "Audit and classify the admissibility scope-binding failure only; do not edit proposal, rerun validation, accept proposal, take human decision, or implement.",
        "failure_surface_ref": rel(FAILURE_SURFACE_PATH),
        "structural_binding_review_ref": rel(STRUCTURAL_BINDING_REVIEW_PATH),
        "scope_phrase_review_ref": rel(SCOPE_PHRASE_REVIEW_PATH),
        "classification_ref": rel(CLASSIFICATION_PATH),
        "repair_target_ref": rel(REPAIR_TARGET_PATH),
        "must_not_infer": [
            "proposal edited",
            "proposal accepted",
            "proposal validated",
            "human decision taken",
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
        "schema_version": "bounded_capability_proposal_admissibility_scope_binding_failure_audit_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "audit_result": audit_verdict,
            "classification": classification,
            "repair_target_kind": repair_target_kind,
            "next_unit_id": next_unit_id,
            "failed_validation_run_receipt_id": failed_run.get("receipt_id"),
            "proposal_id": proposal.get("proposal_id"),
            "structural_binding_present": structural_binding_present,
            "direct_scope_phrase_present": direct_scope_phrase_present,
            "proposal_edited": False,
            "proposal_accepted": False,
            "proposal_validated": False,
            "implementation_authorized": False,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_capability_proposal_admissibility_scope_binding_failure_audit_transition_trace_v0",
        "unit_id": UNIT_ID,
        "audit_id": audit_id,
        "transitions": [
            {
                "from": "VALIDATION_PATH_RUN_GATE_FAIL_SCOPE_MISSING_CAPABILITY_BOUNDARY_BINDING",
                "edge": "separate structural source/capability binding from literal scope phrase binding",
                "to": classification if gate == "PASS" else "AUDIT_GATE_FAIL",
            },
            {
                "from": classification if gate == "PASS" else "AUDIT_GATE_FAIL",
                "edge": "emit typed repair target without editing proposal or validating",
                "to": repair_target_kind if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": next_unit_id,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_CAPABILITY_PROPOSAL_ADMISSIBILITY_SCOPE_BINDING_AUDIT_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (FAILURE_SURFACE_PATH, failure_surface),
        (STRUCTURAL_BINDING_REVIEW_PATH, structural_review),
        (SCOPE_PHRASE_REVIEW_PATH, scope_phrase_review),
        (CLASSIFICATION_PATH, classification_artifact),
        (REPAIR_TARGET_PATH, repair_target),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "FAILED_VALIDATION_RUN_RECEIPT_CONSUMED",
        "SINGLE_SCOPE_BINDING_FAILURE_CONFIRMED",
        "OTHER_VALIDATION_FAMILIES_PASSED",
        "STRUCTURAL_CAPABILITY_BOUNDARY_BINDING_REVIEWED",
        "SCOPE_PHRASE_BINDING_REVIEWED",
        classification,
        "REPAIR_TARGET_EMITTED",
        "NO_PROPOSAL_EDIT",
        "NO_VALIDATION_RERUN",
        "NO_PROPOSAL_ACCEPTANCE",
        "NO_HUMAN_DECISION_TAKEN",
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
        "schema_version": "bounded_capability_proposal_admissibility_scope_binding_failure_audit_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_CAPABILITY_PROPOSAL_ADMISSIBILITY_SCOPE_BINDING_FAILURE_AUDIT_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "audit_id": audit_id,
        "source_failed_validation_run_receipt_id": FAILED_VALIDATION_RUN_RECEIPT_ID,
        "source_failed_validation_run_receipt_ref": rel(FAILED_VALIDATION_RUN_RECEIPT_PATH),
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "AUDIT_0_FAILED_VALIDATION_RUN_RECEIPT_CONSUMED": gate == "PASS",
            "AUDIT_1_SINGLE_SCOPE_BINDING_FAILURE_CONFIRMED": expected_failure_only,
            "AUDIT_2_SOURCE_LINKAGE_PASS_CONFIRMED": source_linkage_result.get("pass") is True,
            "AUDIT_3_SCHEMA_VALIDATION_PASS_CONFIRMED": schema_result.get("pass") is True,
            "AUDIT_4_BOUNDARY_GUARD_PASS_CONFIRMED": boundary_result.get("pass") is True,
            "AUDIT_5_NEGATIVE_CONTROL_PASS_CONFIRMED": negative_result.get("pass") is True,
            "AUDIT_6_HUMAN_DECISION_GATE_PASS_CONFIRMED": human_gate_result.get("pass") is True,
            "AUDIT_7_STRUCTURAL_BINDING_REVIEW_EMITTED": STRUCTURAL_BINDING_REVIEW_PATH.exists(),
            "AUDIT_8_SCOPE_PHRASE_REVIEW_EMITTED": SCOPE_PHRASE_REVIEW_PATH.exists(),
            "AUDIT_9_CLASSIFICATION_EMITTED": CLASSIFICATION_PATH.exists() and gate == "PASS",
            "AUDIT_10_REPAIR_TARGET_EMITTED": REPAIR_TARGET_PATH.exists() and gate == "PASS",
            "AUDIT_11_NO_PROPOSAL_EDIT": True,
            "AUDIT_12_NO_VALIDATION_RERUN": True,
            "AUDIT_13_NO_PROPOSAL_ACCEPTANCE": True,
            "AUDIT_14_NO_HUMAN_DECISION": True,
            "AUDIT_15_NO_IMPLEMENTATION": True,
            "AUDIT_16_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "AUDIT_17_NO_SCHEMA_MUTATION": True,
            "AUDIT_18_NO_MOVE_ADDITION": True,
            "AUDIT_19_NO_C8_AUTHORIZATION": True,
            "AUDIT_20_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_capability_proposal_admissibility_scope_binding_failure_audit_summary": {
            "status": status,
            "audit_id": audit_id,
            "failed_validation_run_receipt_id": failed_run.get("receipt_id"),
            "validation_path_id": failed_summary.get("validation_path_id"),
            "validation_run_id": failed_summary.get("validation_run_id"),
            "proposal_id": proposal.get("proposal_id"),
            "proposal_kind": proposal.get("proposal_kind"),
            "proposed_surface": proposal.get("proposed_surface"),
            "proposal_status": proposal.get("proposal_status"),
            "observed_failure": observed_failure_list,
            "classification": classification,
            "audit_verdict": audit_verdict,
            "structural_binding_present": structural_binding_present,
            "direct_scope_phrase_present": direct_scope_phrase_present,
            "repair_target_kind": repair_target_kind,
            "next_unit_id": next_unit_id,
            "proposal_edited": False,
            "proposal_validated": False,
            "proposal_accepted": False,
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
            "failure_surface": rel(FAILURE_SURFACE_PATH),
            "structural_binding_review": rel(STRUCTURAL_BINDING_REVIEW_PATH),
            "scope_phrase_review": rel(SCOPE_PHRASE_REVIEW_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "repair_target": rel(REPAIR_TARGET_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_capability_proposal_scope_binding_audit_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_capability_proposal_scope_binding_audit_receipt_id={receipt_id}")
    print(f"bounded_capability_proposal_scope_binding_audit_receipt_path={rel(receipt_path)}")
    print(f"bounded_capability_proposal_scope_binding_audit_next_unit={next_unit_id if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
