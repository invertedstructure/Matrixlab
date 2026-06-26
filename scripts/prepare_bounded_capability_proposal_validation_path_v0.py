#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_V0"
TARGET_UNIT_ID = "bounded_capability_proposal.validation_path_prep_v0"
NEXT_UNIT_ID = "RUN_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_V0"

SCOPE_CLASSIFIER_REPAIR_RECEIPT_ID = "bounded_capability_proposal_scope_classifier_repair_receipt_68694b6f"
REVIEW_RECEIPT_ID = "bounded_capability_proposal_review_receipt_804a23ab"
PROPOSAL_ID = "capability_proposal_57dda6e9"

SCOPE_CLASSIFIER_REPAIR_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_review_scope_classifier_repair_v0_receipts/bounded_capability_proposal_scope_classifier_repair_receipt_68694b6f.json"
REVIEW_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_review_v0_receipts/bounded_capability_proposal_review_receipt_804a23ab.json"
REVIEW_VALIDATION_TARGET_PATH = ROOT / "data/bounded_capability_proposal_review_v0/bounded_capability_proposal_validation_path_target_v0.json"

PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
HUMAN_DECISION_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/human_capability_decision_packet_v0.json"
STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"
ADAPTER_RECEIPT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0_receipts/capability_adapter_receipt_8c7f0905.json"

ADAPTER_CLOSURE_RECEIPT_PATH = ROOT / "data/capability_proposal_adapter_reference_closure_v0_receipts/capability_adapter_reference_closure_receipt_b02a18a5.json"
ADAPTER_REFERENCE_INDEX_PATH = ROOT / "data/capability_proposal_adapter_reference_closure_v0/capability_proposal_adapter_reviewed_reference_index_v0.json"

OUT_DIR = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0"
RECEIPT_DIR = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_capability_proposal_validation_path_prep_basis_v0.json"
VALIDATOR_INPUT_BUNDLE_PATH = OUT_DIR / "bounded_capability_proposal_validator_input_bundle_v0.json"
SCHEMA_VALIDATION_CONTRACT_PATH = OUT_DIR / "bounded_capability_proposal_schema_validation_contract_v0.json"
ADMISSIBILITY_CONTRACT_PATH = OUT_DIR / "bounded_capability_proposal_lawful_admissibility_contract_v0.json"
SOURCE_LINKAGE_CONTRACT_PATH = OUT_DIR / "bounded_capability_proposal_source_linkage_contract_v0.json"
BOUNDARY_GUARD_CONTRACT_PATH = OUT_DIR / "bounded_capability_proposal_boundary_guard_contract_v0.json"
NEGATIVE_CONTROL_CONTRACT_PATH = OUT_DIR / "bounded_capability_proposal_negative_control_contract_v0.json"
HUMAN_DECISION_GATE_CONTRACT_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_gate_contract_v0.json"
VALIDATION_RUN_TARGET_PATH = OUT_DIR / "bounded_capability_proposal_validation_run_target_v0.json"
READOUT_PATH = OUT_DIR / "bounded_capability_proposal_validation_path_prep_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_capability_proposal_validation_path_prep_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_capability_proposal_validation_path_prep_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_capability_proposal_validation_path_prep_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_capability_proposal_validation_path_prep_transition_trace.json"

EXPECTED_PROPOSAL_KIND = "BOUNDED_TRIGGER_SURFACE_CAPABILITY_PROPOSAL"
EXPECTED_PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"
EXPECTED_REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
EXPECTED_MISSING_OBJECTS = [
    "loop_trigger_surface_missing",
    "structured_tie_evidence_missing",
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

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        SCOPE_CLASSIFIER_REPAIR_RECEIPT_PATH,
        REVIEW_RECEIPT_PATH,
        REVIEW_VALIDATION_TARGET_PATH,
        PROPOSAL_PATH,
        HUMAN_DECISION_PACKET_PATH,
        STOP_PACKET_PATH,
        ADAPTER_RECEIPT_PATH,
        ADAPTER_CLOSURE_RECEIPT_PATH,
        ADAPTER_REFERENCE_INDEX_PATH,
    ]

    failures: List[str] = []

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    scope_repair = read_json(SCOPE_CLASSIFIER_REPAIR_RECEIPT_PATH)
    review = read_json(REVIEW_RECEIPT_PATH)
    review_target = read_json(REVIEW_VALIDATION_TARGET_PATH)
    proposal = read_json(PROPOSAL_PATH)
    human_decision = read_json(HUMAN_DECISION_PACKET_PATH)
    stop_packet = read_json(STOP_PACKET_PATH)
    adapter_receipt = read_json(ADAPTER_RECEIPT_PATH)
    adapter_closure = read_json(ADAPTER_CLOSURE_RECEIPT_PATH)
    adapter_reference_index = read_json(ADAPTER_REFERENCE_INDEX_PATH)

    scope_repair_summary = scope_repair.get("machine_readable_bounded_capability_proposal_review_scope_classifier_repair_summary", {})
    review_summary = review.get("machine_readable_bounded_capability_proposal_review_summary", {})
    adapter_summary = adapter_receipt.get("machine_readable_capability_proposal_adapter_summary", {})
    closure_summary = adapter_closure.get("machine_readable_capability_proposal_adapter_reference_closure_summary", {})

    # Upstream state checks.
    if scope_repair.get("receipt_id") != SCOPE_CLASSIFIER_REPAIR_RECEIPT_ID:
        failures.append(f"scope_repair_receipt_id_wrong:{scope_repair.get('receipt_id')}")
    if scope_repair.get("gate") != "PASS":
        failures.append("scope_repair_gate_not_pass")
    if scope_repair_summary.get("classifier_repaired") is not True:
        failures.append("scope_classifier_not_repaired")
    if scope_repair_summary.get("validation_path_ready") is not True:
        failures.append("scope_repair_validation_path_not_ready")
    if scope_repair.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"scope_repair_terminal_next_wrong:{scope_repair.get('terminal', {}).get('next_unit_id')}")

    if review.get("receipt_id") != REVIEW_RECEIPT_ID:
        failures.append(f"review_receipt_id_wrong:{review.get('receipt_id')}")
    if review.get("gate") != "PASS":
        failures.append("review_gate_not_pass")
    if review_summary.get("review_verdict") != "VALID_PROPOSAL_CANDIDATE_READY_FOR_VALIDATION_PATH":
        failures.append(f"review_verdict_wrong:{review_summary.get('review_verdict')}")
    if review_summary.get("validation_path_ready") is not True:
        failures.append("review_validation_path_not_ready")

    if review_target.get("target_status") != "READY":
        failures.append(f"review_target_status_wrong:{review_target.get('target_status')}")
    if review_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"review_target_next_wrong:{review_target.get('next_unit_id')}")
    if review_target.get("proposal_id") != PROPOSAL_ID:
        failures.append("review_target_proposal_id_wrong")

    if adapter_closure.get("gate") != "PASS":
        failures.append("adapter_closure_gate_not_pass")
    if closure_summary.get("adapter_reference_branch_closed") is not True:
        failures.append("adapter_reference_branch_not_closed")

    if adapter_reference_index.get("reference_status") != "REVIEWED_REFERENCE_CLOSED":
        failures.append(f"adapter_reference_status_wrong:{adapter_reference_index.get('reference_status')}")

    # Proposal identity and no-authority checks.
    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal.get("proposal_status") != "PROPOSAL_CANDIDATE_ONLY":
        failures.append(f"proposal_status_wrong:{proposal.get('proposal_status')}")
    if proposal.get("proposal_kind") != EXPECTED_PROPOSAL_KIND:
        failures.append(f"proposal_kind_wrong:{proposal.get('proposal_kind')}")
    if proposal.get("proposed_surface") != EXPECTED_PROPOSED_SURFACE:
        failures.append(f"proposed_surface_wrong:{proposal.get('proposed_surface')}")
    if proposal.get("required_capability") != EXPECTED_REQUIRED_CAPABILITY:
        failures.append(f"required_capability_wrong:{proposal.get('required_capability')}")
    if proposal.get("missing_objects_addressed") != EXPECTED_MISSING_OBJECTS:
        failures.append(f"missing_objects_wrong:{proposal.get('missing_objects_addressed')}")
    if proposal.get("source_stop_packet_id") != stop_packet.get("stop_packet_id"):
        failures.append("proposal_source_stop_packet_id_mismatch")

    guards = proposal.get("boundary_guards", {})
    for key in [
        "implementation_authorized",
        "runtime_patch_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "c8_authorized",
    ]:
        require_false(guards, key, failures)

    for obj_name, obj in [
        ("review_summary", review_summary),
        ("scope_repair_summary", scope_repair_summary),
        ("adapter_summary", adapter_summary),
        ("closure_summary", closure_summary),
    ]:
        for key in [
            "proposal_accepted",
            "proposal_validated",
            "human_decision_taken",
            "implementation_authorized",
            "runtime_adoption_authorized",
            "schema_mutation_authorized",
            "move_addition_authorized",
            "fixture_expansion_authorized",
            "runtime_patch_authorized",
            "hidden_next_command",
            "c8_authorized",
        ]:
            if key in obj and obj.get(key) is not False:
                failures.append(f"{obj_name}_{key}_not_false:{obj.get(key)}")

    if human_decision.get("decision_required") is not True:
        failures.append("human_decision_required_false")
    if human_decision.get("default_decision") != "DEFER":
        failures.append(f"human_default_wrong:{human_decision.get('default_decision')}")
    for key in [
        "implementation_authorized",
        "runtime_adoption_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "c8_authorized",
    ]:
        require_false(human_decision, key, failures)

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_PREP_PASS_RUN_READY"
        if gate == "PASS"
        else "TYPED_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_PREP_GATE_FAIL"
    )

    validation_path_id = "bounded_capability_proposal_validation_path_" + sig8({
        "proposal_id": proposal.get("proposal_id"),
        "proposal_kind": proposal.get("proposal_kind"),
        "proposed_surface": proposal.get("proposed_surface"),
        "review_receipt_id": review.get("receipt_id"),
        "adapter_reference_id": closure_summary.get("reference_id"),
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_capability_proposal_validation_path_prep_basis_v0",
        "unit_id": UNIT_ID,
        "validation_path_id": validation_path_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_scope_classifier_repair_receipt_id": SCOPE_CLASSIFIER_REPAIR_RECEIPT_ID,
        "source_review_receipt_id": REVIEW_RECEIPT_ID,
        "source_proposal_id": PROPOSAL_ID,
        "adapter_reference_id": closure_summary.get("reference_id"),
        "basis_claim": "Prepare the validation/admissibility path for a reviewed bounded capability proposal candidate. Do not validate, accept, implement, or mutate authority-bearing registries.",
        "source_file_hashes": source_hashes,
    }

    validator_input_bundle = {
        "schema_version": "bounded_capability_proposal_validator_input_bundle_v0",
        "validation_path_id": validation_path_id,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_ref": rel(PROPOSAL_PATH),
        "human_decision_packet_ref": rel(HUMAN_DECISION_PACKET_PATH),
        "source_stop_packet_ref": rel(STOP_PACKET_PATH),
        "adapter_receipt_ref": rel(ADAPTER_RECEIPT_PATH),
        "adapter_reference_closure_receipt_ref": rel(ADAPTER_CLOSURE_RECEIPT_PATH),
        "proposal_review_receipt_ref": rel(REVIEW_RECEIPT_PATH),
        "scope_classifier_repair_receipt_ref": rel(SCOPE_CLASSIFIER_REPAIR_RECEIPT_PATH),
        "input_hashes": source_hashes,
        "candidate_status": "PROPOSAL_CANDIDATE_ONLY",
        "validation_run_allowed": gate == "PASS",
    }

    schema_validation_contract = {
        "schema_version": "bounded_capability_proposal_schema_validation_contract_v0",
        "validation_path_id": validation_path_id,
        "contract_status": "READY" if gate == "PASS" else "BLOCKED",
        "validator_name": "Schema Validator Cell / Lawful Admissibility Cell",
        "check_kind": "SCHEMA_VALIDATION",
        "required_checks": [
            "proposal packet is well formed JSON",
            "schema_version is bounded_capability_proposal_v0",
            "proposal_id is stable and matches reviewed candidate",
            "proposal_kind is typed",
            "proposal_status remains PROPOSAL_CANDIDATE_ONLY",
            "source stop packet id is present and matches source packet",
            "required capability is explicit",
            "missing objects are explicit and preserved",
            "scope, non-goals, required receipts, acceptance conditions, boundary guards, validator requirements, and must_not_infer are present",
            "human decision options are complete",
        ],
        "pass_output_status": "SCHEMA_VALIDATION_PASS",
        "fail_output_status": "SCHEMA_VALIDATION_FAIL_TYPED_REASON",
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

    admissibility_contract = {
        "schema_version": "bounded_capability_proposal_lawful_admissibility_contract_v0",
        "validation_path_id": validation_path_id,
        "contract_status": "READY" if gate == "PASS" else "BLOCKED",
        "check_kind": "LAWFUL_ADMISSIBILITY",
        "required_checks": [
            "proposal is source-bound to a capability-boundary typed stop",
            "proposal addresses only missing capability representation, not runtime repair",
            "proposal preserves missing-object distinction",
            "proposal does not create self-authorization",
            "proposal requires validation before human decision",
            "proposal requires human decision before implementation",
            "proposal includes negative-control receipts before any implementation path",
            "proposal does not mutate schema/archive/move registries by itself",
            "proposal admits reject, defer, narrower-proposal, alternate-proposal, and reference-only outcomes",
        ],
        "pass_output_status": "LAWFUL_ADMISSIBILITY_PASS",
        "fail_output_status": "LAWFUL_ADMISSIBILITY_FAIL_TYPED_REASON",
        "human_decision_after_pass_only": True,
    }

    source_linkage_contract = {
        "schema_version": "bounded_capability_proposal_source_linkage_contract_v0",
        "validation_path_id": validation_path_id,
        "contract_status": "READY" if gate == "PASS" else "BLOCKED",
        "source_stop_packet_id": stop_packet.get("stop_packet_id"),
        "source_unit_id": stop_packet.get("source_unit_id"),
        "source_stop_code": stop_packet.get("stop_code"),
        "source_missing_objects": stop_packet.get("missing_objects"),
        "proposal_missing_objects": proposal.get("missing_objects_addressed"),
        "source_required_capability": stop_packet.get("required_capability"),
        "proposal_required_capability": proposal.get("required_capability"),
        "required_linkage_checks": [
            "source stop code is STOP_CAPABILITY_LAYER_REQUIRED",
            "proposal source_stop_packet_id matches source packet",
            "proposal missing_objects_addressed equals source missing_objects",
            "proposal required_capability equals source required_capability",
            "proposal proposed_surface is a bounded v0 surface for that capability",
        ],
    }

    boundary_guard_contract = {
        "schema_version": "bounded_capability_proposal_boundary_guard_contract_v0",
        "validation_path_id": validation_path_id,
        "contract_status": "READY" if gate == "PASS" else "BLOCKED",
        "required_false_flags": [
            "proposal_accepted",
            "proposal_validated_before_run",
            "human_decision_taken",
            "implementation_authorized",
            "runtime_adoption_authorized",
            "schema_mutation_authorized",
            "move_addition_authorized",
            "fixture_expansion_authorized",
            "runtime_patch_authorized",
            "hidden_next_command",
            "c8_authorized",
        ],
        "boundary_rule": "Validation/admissibility may classify the proposal; it may not accept, implement, or grant runtime/schema/move authority.",
    }

    negative_control_contract = {
        "schema_version": "bounded_capability_proposal_negative_control_contract_v0",
        "validation_path_id": validation_path_id,
        "contract_status": "READY" if gate == "PASS" else "BLOCKED",
        "required_zero_counters": [
            "proposal_acceptance_count",
            "implementation_authority_count",
            "human_decision_taken_count",
            "runtime_adoption_authority_count",
            "runtime_patch_count",
            "schema_mutation_count",
            "move_addition_count",
            "fixture_expansion_count",
            "c8_authorization_count",
            "hidden_next_command_count",
        ],
        "zero_counter_meaning": "These counters must remain zero during validation-path preparation and validation run. Later human acceptance must be separately receipted.",
    }

    human_decision_gate_contract = {
        "schema_version": "bounded_capability_proposal_human_decision_gate_contract_v0",
        "validation_path_id": validation_path_id,
        "contract_status": "READY" if gate == "PASS" else "BLOCKED",
        "human_decision_packet_ref": rel(HUMAN_DECISION_PACKET_PATH),
        "decision_required": human_decision.get("decision_required"),
        "default_decision": human_decision.get("default_decision"),
        "available_decisions": human_decision.get("available_decisions"),
        "gate_rule": "Human decision is not available until schema validation and lawful admissibility both pass. Default remains DEFER.",
        "does_not_take_decision": True,
    }

    validation_run_target = {
        "schema_version": "bounded_capability_proposal_validation_run_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "validation_path_id": validation_path_id,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_ref": rel(PROPOSAL_PATH),
        "validator_input_bundle_ref": rel(VALIDATOR_INPUT_BUNDLE_PATH),
        "schema_validation_contract_ref": rel(SCHEMA_VALIDATION_CONTRACT_PATH),
        "lawful_admissibility_contract_ref": rel(ADMISSIBILITY_CONTRACT_PATH),
        "source_linkage_contract_ref": rel(SOURCE_LINKAGE_CONTRACT_PATH),
        "boundary_guard_contract_ref": rel(BOUNDARY_GUARD_CONTRACT_PATH),
        "negative_control_contract_ref": rel(NEGATIVE_CONTROL_CONTRACT_PATH),
        "human_decision_gate_contract_ref": rel(HUMAN_DECISION_GATE_CONTRACT_PATH),
        "run_sequence": [
            "load validator input bundle",
            "verify source linkage",
            "run schema validation checks",
            "run lawful admissibility checks",
            "verify boundary guards and negative controls",
            "emit validation/admissibility receipt",
            "if both pass, advance to human decision packet review/prep",
            "if either fails, stop with typed reason and repair target if local",
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
        "schema_version": "bounded_capability_proposal_validation_path_prep_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "validation_path_id": validation_path_id,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_kind": proposal.get("proposal_kind"),
        "proposed_surface": proposal.get("proposed_surface"),
        "schema_validation_contract_ready": gate == "PASS",
        "lawful_admissibility_contract_ready": gate == "PASS",
        "source_linkage_contract_ready": gate == "PASS",
        "boundary_guard_contract_ready": gate == "PASS",
        "negative_control_contract_ready": gate == "PASS",
        "human_decision_gate_contract_ready": gate == "PASS",
        "validation_run_target_ready": gate == "PASS",
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
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    readout = {
        "schema_version": "bounded_capability_proposal_validation_path_prep_readout_v0",
        "status": status,
        "validation_path_id": validation_path_id,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_status": proposal.get("proposal_status"),
        "prepared_object": "validation/admissibility path",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "interpretation": "Validation path is prepared. The proposal remains candidate-only; no validation, human decision, acceptance, or implementation occurred."
        if gate == "PASS" else "Validation path preparation failed typed gates.",
    }

    profile = {
        "schema_version": "bounded_capability_proposal_validation_path_prep_profile_v0",
        "profile_status": status,
        "validation_path_id": validation_path_id,
        "core_rule": "Prepare validation/admissibility path only. Validation classifies; human decision accepts/rejects/defer; implementation requires later explicit acceptance.",
        "validator_input_bundle_ref": rel(VALIDATOR_INPUT_BUNDLE_PATH),
        "validation_run_target_ref": rel(VALIDATION_RUN_TARGET_PATH),
        "must_not_infer": [
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
        "schema_version": "bounded_capability_proposal_validation_path_prep_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "prep_result": "VALIDATION_PATH_READY" if gate == "PASS" else "VALIDATION_PATH_PREP_GATE_FAIL",
            "validation_path_id": validation_path_id,
            "proposal_id": proposal.get("proposal_id"),
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "proposal_accepted": False,
            "proposal_validated": False,
            "human_decision_taken": False,
            "implementation_authorized": False,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_capability_proposal_validation_path_prep_transition_trace_v0",
        "unit_id": UNIT_ID,
        "validation_path_id": validation_path_id,
        "transitions": [
            {
                "from": "VALID_PROPOSAL_CANDIDATE_READY_FOR_VALIDATION_PATH",
                "edge": "prepare schema validation, lawful admissibility, source linkage, boundary guard, negative control, and human decision gate contracts",
                "to": "VALIDATION_PATH_PREPARED" if gate == "PASS" else "VALIDATION_PATH_PREP_GATE_FAIL",
            },
            {
                "from": "VALIDATION_PATH_PREPARED" if gate == "PASS" else "VALIDATION_PATH_PREP_GATE_FAIL",
                "edge": "emit validation run target without validation or acceptance",
                "to": "RUN_VALIDATION_PATH_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_PREP_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (VALIDATOR_INPUT_BUNDLE_PATH, validator_input_bundle),
        (SCHEMA_VALIDATION_CONTRACT_PATH, schema_validation_contract),
        (ADMISSIBILITY_CONTRACT_PATH, admissibility_contract),
        (SOURCE_LINKAGE_CONTRACT_PATH, source_linkage_contract),
        (BOUNDARY_GUARD_CONTRACT_PATH, boundary_guard_contract),
        (NEGATIVE_CONTROL_CONTRACT_PATH, negative_control_contract),
        (HUMAN_DECISION_GATE_CONTRACT_PATH, human_decision_gate_contract),
        (VALIDATION_RUN_TARGET_PATH, validation_run_target),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "SCOPE_CLASSIFIER_REPAIR_RECEIPT_CONSUMED",
        "CLEAN_PROPOSAL_REVIEW_RECEIPT_CONSUMED",
        "VALIDATION_PATH_TARGET_CONSUMED",
        "PROPOSAL_CANDIDATE_CONSUMED",
        "ADAPTER_REFERENCE_CLOSURE_CONSUMED",
        "SCHEMA_VALIDATION_CONTRACT_EMITTED",
        "LAWFUL_ADMISSIBILITY_CONTRACT_EMITTED",
        "SOURCE_LINKAGE_CONTRACT_EMITTED",
        "BOUNDARY_GUARD_CONTRACT_EMITTED",
        "NEGATIVE_CONTROL_CONTRACT_EMITTED",
        "HUMAN_DECISION_GATE_CONTRACT_EMITTED",
        "VALIDATION_RUN_TARGET_EMITTED",
        "NO_PROPOSAL_VALIDATION",
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
        "schema_version": "bounded_capability_proposal_validation_path_prep_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_PREP_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "validation_path_id": validation_path_id,
        "source_scope_classifier_repair_receipt_id": SCOPE_CLASSIFIER_REPAIR_RECEIPT_ID,
        "source_scope_classifier_repair_receipt_ref": rel(SCOPE_CLASSIFIER_REPAIR_RECEIPT_PATH),
        "source_review_receipt_id": REVIEW_RECEIPT_ID,
        "source_review_receipt_ref": rel(REVIEW_RECEIPT_PATH),
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "VALIDATION_PREP_0_SCOPE_CLASSIFIER_REPAIR_CONSUMED": gate == "PASS",
            "VALIDATION_PREP_1_CLEAN_REVIEW_CONSUMED": gate == "PASS",
            "VALIDATION_PREP_2_PROPOSAL_CANDIDATE_ONLY": proposal.get("proposal_status") == "PROPOSAL_CANDIDATE_ONLY",
            "VALIDATION_PREP_3_SCHEMA_CONTRACT_EMITTED": SCHEMA_VALIDATION_CONTRACT_PATH.exists() and gate == "PASS",
            "VALIDATION_PREP_4_ADMISSIBILITY_CONTRACT_EMITTED": ADMISSIBILITY_CONTRACT_PATH.exists() and gate == "PASS",
            "VALIDATION_PREP_5_SOURCE_LINKAGE_CONTRACT_EMITTED": SOURCE_LINKAGE_CONTRACT_PATH.exists() and gate == "PASS",
            "VALIDATION_PREP_6_BOUNDARY_GUARD_CONTRACT_EMITTED": BOUNDARY_GUARD_CONTRACT_PATH.exists() and gate == "PASS",
            "VALIDATION_PREP_7_NEGATIVE_CONTROL_CONTRACT_EMITTED": NEGATIVE_CONTROL_CONTRACT_PATH.exists() and gate == "PASS",
            "VALIDATION_PREP_8_HUMAN_DECISION_GATE_CONTRACT_EMITTED": HUMAN_DECISION_GATE_CONTRACT_PATH.exists() and gate == "PASS",
            "VALIDATION_PREP_9_RUN_TARGET_EMITTED": VALIDATION_RUN_TARGET_PATH.exists() and gate == "PASS",
            "VALIDATION_PREP_10_NO_PROPOSAL_VALIDATION": True,
            "VALIDATION_PREP_11_NO_PROPOSAL_ACCEPTANCE": True,
            "VALIDATION_PREP_12_NO_HUMAN_DECISION": True,
            "VALIDATION_PREP_13_NO_IMPLEMENTATION": True,
            "VALIDATION_PREP_14_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "VALIDATION_PREP_15_NO_SCHEMA_MUTATION": True,
            "VALIDATION_PREP_16_NO_MOVE_ADDITION": True,
            "VALIDATION_PREP_17_NO_C8_AUTHORIZATION": True,
            "VALIDATION_PREP_18_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_capability_proposal_validation_path_prep_summary": {
            "status": status,
            "validation_path_id": validation_path_id,
            "proposal_id": proposal.get("proposal_id"),
            "proposal_kind": proposal.get("proposal_kind"),
            "proposed_surface": proposal.get("proposed_surface"),
            "proposal_status": proposal.get("proposal_status"),
            "validation_run_target_ready": gate == "PASS",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
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
            "validator_input_bundle": rel(VALIDATOR_INPUT_BUNDLE_PATH),
            "schema_validation_contract": rel(SCHEMA_VALIDATION_CONTRACT_PATH),
            "lawful_admissibility_contract": rel(ADMISSIBILITY_CONTRACT_PATH),
            "source_linkage_contract": rel(SOURCE_LINKAGE_CONTRACT_PATH),
            "boundary_guard_contract": rel(BOUNDARY_GUARD_CONTRACT_PATH),
            "negative_control_contract": rel(NEGATIVE_CONTROL_CONTRACT_PATH),
            "human_decision_gate_contract": rel(HUMAN_DECISION_GATE_CONTRACT_PATH),
            "validation_run_target": rel(VALIDATION_RUN_TARGET_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_capability_proposal_validation_path_prep_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_capability_proposal_validation_path_prep_receipt_id={receipt_id}")
    print(f"bounded_capability_proposal_validation_path_prep_receipt_path={rel(receipt_path)}")
    print(f"bounded_capability_proposal_validation_path_id={validation_path_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_capability_proposal_validation_path_prep_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
