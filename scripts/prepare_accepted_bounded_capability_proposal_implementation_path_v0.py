#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_ACCEPTED_BOUNDED_CAPABILITY_PROPOSAL_IMPLEMENTATION_PATH_V0"
TARGET_UNIT_ID = "accepted_bounded_capability_proposal.implementation_path_prep_v0"
NEXT_UNIT_ID = "REVIEW_ACCEPTED_BOUNDED_CAPABILITY_PROPOSAL_IMPLEMENTATION_PATH_V0"

ACCEPT_RECEIPT_ID = "bounded_capability_proposal_human_decision_accept_receipt_6979a229"
PROPOSAL_ID = "capability_proposal_57dda6e9"
SELECTED_DECISION = "ACCEPT_FOR_BOUNDED_IMPLEMENTATION"

ACCEPT_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_human_decision_accept_for_bounded_implementation_v0_receipts/bounded_capability_proposal_human_decision_accept_receipt_6979a229.json"
IMPLEMENTATION_PATH_PREP_TARGET_PATH = ROOT / "data/bounded_capability_proposal_human_decision_accept_for_bounded_implementation_v0/accepted_bounded_capability_proposal_implementation_path_prep_target_v0.json"
DECISION_RECORD_PATH = ROOT / "data/bounded_capability_proposal_human_decision_accept_for_bounded_implementation_v0/bounded_capability_proposal_human_decision_record_v0.json"
ACCEPT_BOUNDARY_PATH = ROOT / "data/bounded_capability_proposal_human_decision_accept_for_bounded_implementation_v0/bounded_capability_proposal_human_decision_accept_boundary_review_v0.json"

VALIDATION_RUN_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0_receipts/bounded_capability_proposal_validation_path_run_receipt_375954b6.json"
VALIDATION_SUMMARY_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0/bounded_capability_proposal_validation_admissibility_summary_v0.json"

PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"
HUMAN_DECISION_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/human_capability_decision_packet_v0.json"

OUT_DIR = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_prep_v0"
RECEIPT_DIR = ROOT / "data/accepted_bounded_capability_proposal_implementation_path_prep_v0_receipts"

BASIS_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_prep_basis_v0.json"
IMPLEMENTATION_OBJECTIVE_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_objective_v0.json"
CAPABILITY_BOUNDARY_PATH = OUT_DIR / "accepted_bounded_capability_proposal_capability_boundary_v0.json"
MINIMAL_IMPLEMENTATION_CONTRACT_PATH = OUT_DIR / "accepted_bounded_capability_proposal_minimal_implementation_contract_v0.json"
IMPLEMENTATION_GUARD_CONTRACT_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_guard_contract_v0.json"
TEST_AND_RECEIPT_CONTRACT_PATH = OUT_DIR / "accepted_bounded_capability_proposal_test_and_receipt_contract_v0.json"
NEGATIVE_CONTROL_CONTRACT_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_negative_control_contract_v0.json"
IMPLEMENTATION_REVIEW_TARGET_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_review_target_v0.json"
READOUT_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_prep_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_prep_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_prep_profile_v0.json"
REPORT_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_prep_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_prep_transition_trace.json"

EXPECTED_REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
EXPECTED_PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"
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

def require_false(obj: Dict[str, Any], key: str, failures: List[str], prefix: str) -> None:
    if obj.get(key) is not False:
        failures.append(f"{prefix}_{key}_not_false:{obj.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        ACCEPT_RECEIPT_PATH,
        IMPLEMENTATION_PATH_PREP_TARGET_PATH,
        DECISION_RECORD_PATH,
        ACCEPT_BOUNDARY_PATH,
        VALIDATION_RUN_RECEIPT_PATH,
        VALIDATION_SUMMARY_PATH,
        PROPOSAL_PATH,
        STOP_PACKET_PATH,
        HUMAN_DECISION_PACKET_PATH,
    ]

    failures: List[str] = []

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    accept_receipt = read_json(ACCEPT_RECEIPT_PATH)
    implementation_path_prep_target = read_json(IMPLEMENTATION_PATH_PREP_TARGET_PATH)
    decision_record = read_json(DECISION_RECORD_PATH)
    accept_boundary = read_json(ACCEPT_BOUNDARY_PATH)
    validation_run = read_json(VALIDATION_RUN_RECEIPT_PATH)
    validation_summary = read_json(VALIDATION_SUMMARY_PATH)
    proposal = read_json(PROPOSAL_PATH)
    stop_packet = read_json(STOP_PACKET_PATH)
    human_decision_packet = read_json(HUMAN_DECISION_PACKET_PATH)

    accept_summary = accept_receipt.get("machine_readable_bounded_capability_proposal_human_decision_accept_summary", {})
    validation_run_summary = validation_run.get("machine_readable_bounded_capability_proposal_validation_path_run_summary", {})

    # Source acceptance checks.
    if accept_receipt.get("receipt_id") != ACCEPT_RECEIPT_ID:
        failures.append(f"accept_receipt_id_wrong:{accept_receipt.get('receipt_id')}")
    if accept_receipt.get("gate") != "PASS":
        failures.append("accept_receipt_gate_not_pass")
    if accept_receipt.get("selected_decision") != SELECTED_DECISION:
        failures.append(f"accept_receipt_selected_decision_wrong:{accept_receipt.get('selected_decision')}")
    if accept_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"accept_receipt_terminal_next_wrong:{accept_receipt.get('terminal', {}).get('next_unit_id')}")

    for key in [
        "proposal_validated_by_run",
        "proposal_admissible_for_human_decision",
        "proposal_accepted",
        "human_decision_taken",
        "bounded_implementation_path_prep_authorized",
    ]:
        if accept_summary.get(key) is not True:
            failures.append(f"accept_summary_{key}_not_true:{accept_summary.get(key)}")

    for key in [
        "implementation_authorized",
        "runtime_adoption_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "runtime_patch_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(accept_summary, key, failures, "accept_summary")

    # Prep target checks.
    if implementation_path_prep_target.get("target_status") != "READY":
        failures.append(f"implementation_path_prep_target_status_wrong:{implementation_path_prep_target.get('target_status')}")
    if implementation_path_prep_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"implementation_path_prep_target_next_wrong:{implementation_path_prep_target.get('next_unit_id')}")
    if implementation_path_prep_target.get("proposal_id") != PROPOSAL_ID:
        failures.append("implementation_path_prep_target_proposal_id_wrong")
    if implementation_path_prep_target.get("selected_decision") != SELECTED_DECISION:
        failures.append("implementation_path_prep_target_selected_decision_wrong")

    # Decision record checks.
    if decision_record.get("decision_record_status") != "HUMAN_DECISION_RECORDED":
        failures.append(f"decision_record_status_wrong:{decision_record.get('decision_record_status')}")
    if decision_record.get("selected_decision") != SELECTED_DECISION:
        failures.append("decision_record_selected_decision_wrong")
    if decision_record.get("proposal_accepted") is not True:
        failures.append("decision_record_proposal_not_accepted")
    if decision_record.get("does_not_implement") is not True:
        failures.append("decision_record_does_not_implement_missing")

    # Proposal and stop checks.
    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal.get("proposal_status") != "PROPOSAL_CANDIDATE_ONLY":
        failures.append(f"proposal_status_wrong:{proposal.get('proposal_status')}")
    if proposal.get("required_capability") != EXPECTED_REQUIRED_CAPABILITY:
        failures.append(f"proposal_required_capability_wrong:{proposal.get('required_capability')}")
    if proposal.get("proposed_surface") != EXPECTED_PROPOSED_SURFACE:
        failures.append(f"proposal_proposed_surface_wrong:{proposal.get('proposed_surface')}")
    if proposal.get("missing_objects_addressed") != EXPECTED_MISSING_OBJECTS:
        failures.append(f"proposal_missing_objects_wrong:{proposal.get('missing_objects_addressed')}")

    if stop_packet.get("stop_code") != "STOP_CAPABILITY_LAYER_REQUIRED":
        failures.append(f"source_stop_code_wrong:{stop_packet.get('stop_code')}")
    if proposal.get("source_stop_packet_id") != stop_packet.get("stop_packet_id"):
        failures.append("proposal_source_stop_packet_mismatch")
    if stop_packet.get("required_capability") != EXPECTED_REQUIRED_CAPABILITY:
        failures.append(f"stop_packet_required_capability_wrong:{stop_packet.get('required_capability')}")
    if stop_packet.get("missing_objects") != EXPECTED_MISSING_OBJECTS:
        failures.append(f"stop_packet_missing_objects_wrong:{stop_packet.get('missing_objects')}")

    # Validation still clean.
    if validation_run.get("gate") != "PASS":
        failures.append("validation_run_gate_not_pass")
    for key in [
        "schema_validation_pass",
        "source_linkage_pass",
        "lawful_admissibility_pass",
        "boundary_guard_pass",
        "negative_control_pass",
        "human_decision_gate_pass",
        "proposal_validated_by_run",
        "proposal_admissible_for_human_decision",
    ]:
        if validation_run_summary.get(key) is not True:
            failures.append(f"validation_run_{key}_not_true:{validation_run_summary.get(key)}")

    if validation_summary.get("proposal_validated_by_run") is not True:
        failures.append("validation_summary_proposal_not_validated")
    if validation_summary.get("proposal_admissible_for_human_decision") is not True:
        failures.append("validation_summary_proposal_not_admissible")

    # No actual implementation yet.
    for obj_name, obj in [
        ("accept_boundary", accept_boundary),
        ("human_decision_packet", human_decision_packet),
    ]:
        for key in [
            "implementation_authorized",
            "runtime_adoption_authorized",
            "schema_mutation_authorized",
            "move_addition_authorized",
            "c8_authorized",
        ]:
            if key in obj:
                require_false(obj, key, failures, obj_name)

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_ACCEPTED_BOUNDED_CAPABILITY_PROPOSAL_IMPLEMENTATION_PATH_PREP_PASS_REVIEW_READY"
        if gate == "PASS"
        else "TYPED_ACCEPTED_BOUNDED_CAPABILITY_PROPOSAL_IMPLEMENTATION_PATH_PREP_GATE_FAIL"
    )

    implementation_path_id = "accepted_bounded_capability_implementation_path_" + sig8({
        "decision_record_id": decision_record.get("decision_record_id"),
        "proposal_id": proposal.get("proposal_id"),
        "required_capability": proposal.get("required_capability"),
        "proposed_surface": proposal.get("proposed_surface"),
        "missing_objects": proposal.get("missing_objects_addressed"),
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_prep_basis_v0",
        "unit_id": UNIT_ID,
        "implementation_path_id": implementation_path_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_accept_receipt_id": ACCEPT_RECEIPT_ID,
        "source_decision_record_id": decision_record.get("decision_record_id"),
        "source_proposal_id": PROPOSAL_ID,
        "selected_decision": SELECTED_DECISION,
        "basis_claim": "Prepare the bounded implementation path for the accepted proposal. Do not implement, patch runtime, mutate schemas, add moves, or expand fixtures.",
        "source_file_hashes": source_hashes,
    }

    implementation_objective = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_objective_v0",
        "implementation_path_id": implementation_path_id,
        "objective_status": "READY_FOR_REVIEW" if gate == "PASS" else "BLOCKED",
        "proposal_id": proposal.get("proposal_id"),
        "proposal_kind": proposal.get("proposal_kind"),
        "required_capability": proposal.get("required_capability"),
        "proposed_surface": proposal.get("proposed_surface"),
        "source_stop_code": stop_packet.get("stop_code"),
        "source_missing_objects": stop_packet.get("missing_objects"),
        "bounded_objective": "Introduce a bounded structured T6 trigger-surface capability representation path sufficient to distinguish real structured trigger evidence from text-only detector residue.",
        "minimal_required_outputs": [
            "a structured trigger-surface profile shape",
            "typed evidence fields for loop trigger surface and tie evidence",
            "negative controls for text-only tie residue",
            "receipt fields proving no runtime patch or move/schema mutation occurred during path preparation",
            "review target before any implementation",
        ],
        "not_in_scope": [
            "runtime repair",
            "runtime patch",
            "runtime adoption",
            "schema archive mutation",
            "move registry addition",
            "fixture expansion by default",
            "T6 live case execution",
            "C8",
            "global loop capability",
        ],
    }

    capability_boundary = {
        "schema_version": "accepted_bounded_capability_proposal_capability_boundary_v0",
        "implementation_path_id": implementation_path_id,
        "boundary_status": "READY_FOR_REVIEW" if gate == "PASS" else "BLOCKED",
        "capability_name": EXPECTED_REQUIRED_CAPABILITY,
        "surface_name": EXPECTED_PROPOSED_SURFACE,
        "source_missing_objects": EXPECTED_MISSING_OBJECTS,
        "allowed_capability_shape": {
            "loop_trigger_surface_missing": "Represent whether a structured loop trigger surface exists, with evidence pointer or typed absence reason.",
            "structured_tie_evidence_missing": "Represent whether structured tie evidence exists, with evidence pointer or typed absence reason.",
            "text_only_tie_residue": "Represent detector text residue as insufficient unless promoted by structured evidence.",
        },
        "authority_boundary": "This path may prepare a capability representation and review gates. It may not implement or activate runtime behavior until a later explicit implementation unit is authorized.",
    }

    minimal_implementation_contract = {
        "schema_version": "accepted_bounded_capability_proposal_minimal_implementation_contract_v0",
        "implementation_path_id": implementation_path_id,
        "contract_status": "READY_FOR_REVIEW" if gate == "PASS" else "BLOCKED",
        "contract_kind": "BOUNDED_IMPLEMENTATION_PATH_PREP_CONTRACT",
        "implementation_candidate_unit": "BUILD_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_V0",
        "implementation_candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED",
        "required_before_build": [
            "review this implementation path",
            "confirm implementation target remains bounded to proposed surface",
            "confirm no runtime adoption or move/schema mutation is included",
            "confirm tests/negative controls are sufficient",
            "emit a separate build authorization receipt",
        ],
        "candidate_artifacts_to_build_later": [
            "bounded structured T6 trigger-surface capability profile",
            "capability surface schema candidate",
            "text-only tie residue negative-control case",
            "structured trigger/tie evidence positive shape example",
            "receipt contract for future implementation",
        ],
        "this_unit_does_not_build_these_artifacts": True,
    }

    implementation_guard_contract = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_guard_contract_v0",
        "implementation_path_id": implementation_path_id,
        "guard_status": "READY_FOR_REVIEW" if gate == "PASS" else "BLOCKED",
        "must_remain_false_in_this_unit": [
            "implementation_authorized",
            "implementation_executed",
            "runtime_adoption_authorized",
            "runtime_patch_authorized",
            "schema_mutation_authorized",
            "move_addition_authorized",
            "fixture_expansion_authorized",
            "hidden_next_command",
            "c8_authorized",
        ],
        "build_gate_rule": "A later build unit must be separately authorized after this implementation path is reviewed. Path prep alone is not build authorization.",
    }

    test_and_receipt_contract = {
        "schema_version": "accepted_bounded_capability_proposal_test_and_receipt_contract_v0",
        "implementation_path_id": implementation_path_id,
        "contract_status": "READY_FOR_REVIEW" if gate == "PASS" else "BLOCKED",
        "required_future_tests": [
            "text-only tie surface remains negative",
            "structured loop trigger surface with required fields is recognized",
            "structured tie evidence with required fields is recognized",
            "missing structured evidence produces typed capability stop, not repair",
            "receipt records source stop packet, decision record, capability boundary, and all negative controls",
        ],
        "required_future_receipt_fields": [
            "source_accept_receipt_id",
            "decision_record_id",
            "proposal_id",
            "required_capability",
            "proposed_surface",
            "implementation_scope",
            "negative_control_counts",
            "runtime_patch_authorized=false",
            "runtime_adoption_authorized=false",
            "schema_mutation_authorized=false unless separately authorized",
            "move_addition_authorized=false unless separately authorized",
            "c8_authorized=false",
        ],
    }

    negative_control_contract = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_negative_control_contract_v0",
        "implementation_path_id": implementation_path_id,
        "contract_status": "READY_FOR_REVIEW" if gate == "PASS" else "BLOCKED",
        "zero_counters_for_this_unit": {
            "implementation_executed_count": 0,
            "runtime_patch_count": 0,
            "runtime_adoption_authority_count": 0,
            "schema_mutation_count": 0,
            "move_addition_count": 0,
            "fixture_expansion_count": 0,
            "hidden_next_command_count": 0,
            "c8_authorization_count": 0,
        },
        "negative_control_rule": "Implementation path preparation may create contracts and review targets only. Any executable implementation requires a later receipt."
    }

    implementation_review_target = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_review_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "implementation_path_id": implementation_path_id,
        "proposal_id": proposal.get("proposal_id"),
        "decision_record_id": decision_record.get("decision_record_id"),
        "source_accept_receipt_id": ACCEPT_RECEIPT_ID,
        "review_scope": "Review bounded implementation path prep artifacts and decide whether the implementation candidate can be authorized for a later build unit.",
        "review_inputs": [
            rel(IMPLEMENTATION_OBJECTIVE_PATH),
            rel(CAPABILITY_BOUNDARY_PATH),
            rel(MINIMAL_IMPLEMENTATION_CONTRACT_PATH),
            rel(IMPLEMENTATION_GUARD_CONTRACT_PATH),
            rel(TEST_AND_RECEIPT_CONTRACT_PATH),
            rel(NEGATIVE_CONTROL_CONTRACT_PATH),
        ],
        "does_not_authorize_build": True,
    }

    rollup = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_prep_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "implementation_path_id": implementation_path_id,
        "proposal_id": proposal.get("proposal_id"),
        "decision_record_id": decision_record.get("decision_record_id"),
        "selected_decision": SELECTED_DECISION,
        "proposal_accepted": True if gate == "PASS" else False,
        "bounded_implementation_path_prep_authorized": True if gate == "PASS" else False,
        "implementation_path_prepared": True if gate == "PASS" else False,
        "implementation_review_target_ready": True if gate == "PASS" else False,
        "implementation_authorized": False,
        "implementation_executed": False,
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
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_prep_readout_v0",
        "status": status,
        "implementation_path_id": implementation_path_id,
        "proposal_id": proposal.get("proposal_id"),
        "decision_record_id": decision_record.get("decision_record_id"),
        "interpretation": "Bounded implementation path is prepared for review. No implementation/build/runtime patch occurred."
        if gate == "PASS" else "Implementation path prep failed typed gates.",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_prep_profile_v0",
        "profile_status": status,
        "implementation_path_id": implementation_path_id,
        "core_rule": "Prepare implementation path only. Build remains candidate-only until a later explicit review/authorization unit.",
        "implementation_objective_ref": rel(IMPLEMENTATION_OBJECTIVE_PATH),
        "capability_boundary_ref": rel(CAPABILITY_BOUNDARY_PATH),
        "minimal_implementation_contract_ref": rel(MINIMAL_IMPLEMENTATION_CONTRACT_PATH),
        "implementation_review_target_ref": rel(IMPLEMENTATION_REVIEW_TARGET_PATH),
        "must_not_infer": [
            "implementation authorized",
            "implementation executed",
            "runtime repaired",
            "runtime adoption authorized",
            "schema mutation authorized",
            "move addition authorized",
            "fixtures may expand by default",
            "C8 authorized",
            "unbounded capability authority",
        ],
    }

    report = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_prep_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "prep_result": "IMPLEMENTATION_PATH_PREPARED_FOR_REVIEW" if gate == "PASS" else "IMPLEMENTATION_PATH_PREP_GATE_FAIL",
            "implementation_path_id": implementation_path_id,
            "proposal_id": proposal.get("proposal_id"),
            "selected_decision": SELECTED_DECISION,
            "implementation_review_target_ready": gate == "PASS",
            "implementation_authorized": False,
            "implementation_executed": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_prep_transition_trace_v0",
        "unit_id": UNIT_ID,
        "implementation_path_id": implementation_path_id,
        "transitions": [
            {
                "from": "ACCEPTED_FOR_BOUNDED_IMPLEMENTATION_PATH_PREP",
                "edge": "derive bounded implementation objective, capability boundary, guards, tests, and negative controls",
                "to": "IMPLEMENTATION_PATH_PREPARED_FOR_REVIEW" if gate == "PASS" else "IMPLEMENTATION_PATH_PREP_GATE_FAIL",
            },
            {
                "from": "IMPLEMENTATION_PATH_PREPARED_FOR_REVIEW" if gate == "PASS" else "IMPLEMENTATION_PATH_PREP_GATE_FAIL",
                "edge": "emit review target without implementation",
                "to": "IMPLEMENTATION_PATH_REVIEW_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_ACCEPTED_BOUNDED_CAPABILITY_PROPOSAL_IMPLEMENTATION_PATH_PREP_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (IMPLEMENTATION_OBJECTIVE_PATH, implementation_objective),
        (CAPABILITY_BOUNDARY_PATH, capability_boundary),
        (MINIMAL_IMPLEMENTATION_CONTRACT_PATH, minimal_implementation_contract),
        (IMPLEMENTATION_GUARD_CONTRACT_PATH, implementation_guard_contract),
        (TEST_AND_RECEIPT_CONTRACT_PATH, test_and_receipt_contract),
        (NEGATIVE_CONTROL_CONTRACT_PATH, negative_control_contract),
        (IMPLEMENTATION_REVIEW_TARGET_PATH, implementation_review_target),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "ACCEPT_RECEIPT_CONSUMED",
        "IMPLEMENTATION_PATH_PREP_TARGET_CONSUMED",
        "DECISION_RECORD_CONSUMED",
        "PROPOSAL_ACCEPTED_FOR_BOUNDED_IMPLEMENTATION_PATH_PREP_CONFIRMED",
        "SOURCE_CAPABILITY_BOUNDARY_PRESERVED",
        "IMPLEMENTATION_OBJECTIVE_EMITTED",
        "CAPABILITY_BOUNDARY_EMITTED",
        "MINIMAL_IMPLEMENTATION_CONTRACT_EMITTED",
        "IMPLEMENTATION_GUARD_CONTRACT_EMITTED",
        "TEST_AND_RECEIPT_CONTRACT_EMITTED",
        "NEGATIVE_CONTROL_CONTRACT_EMITTED",
        "IMPLEMENTATION_PATH_REVIEW_TARGET_EMITTED",
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
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_prep_receipt_v0",
        "receipt_type": "TYPED_ACCEPTED_BOUNDED_CAPABILITY_PROPOSAL_IMPLEMENTATION_PATH_PREP_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "implementation_path_id": implementation_path_id,
        "source_accept_receipt_id": ACCEPT_RECEIPT_ID,
        "source_accept_receipt_ref": rel(ACCEPT_RECEIPT_PATH),
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "IMPLEMENTATION_PATH_PREP_0_ACCEPT_RECEIPT_CONSUMED": gate == "PASS",
            "IMPLEMENTATION_PATH_PREP_1_DECISION_RECORD_CONSUMED": gate == "PASS",
            "IMPLEMENTATION_PATH_PREP_2_PROPOSAL_ACCEPTED_CONFIRMED": accept_summary.get("proposal_accepted") is True,
            "IMPLEMENTATION_PATH_PREP_3_PATH_PREP_AUTHORIZED": accept_summary.get("bounded_implementation_path_prep_authorized") is True,
            "IMPLEMENTATION_PATH_PREP_4_SOURCE_BOUNDARY_PRESERVED": proposal.get("source_stop_packet_id") == stop_packet.get("stop_packet_id"),
            "IMPLEMENTATION_PATH_PREP_5_IMPLEMENTATION_OBJECTIVE_EMITTED": IMPLEMENTATION_OBJECTIVE_PATH.exists() and gate == "PASS",
            "IMPLEMENTATION_PATH_PREP_6_CAPABILITY_BOUNDARY_EMITTED": CAPABILITY_BOUNDARY_PATH.exists() and gate == "PASS",
            "IMPLEMENTATION_PATH_PREP_7_MINIMAL_IMPLEMENTATION_CONTRACT_EMITTED": MINIMAL_IMPLEMENTATION_CONTRACT_PATH.exists() and gate == "PASS",
            "IMPLEMENTATION_PATH_PREP_8_TEST_AND_RECEIPT_CONTRACT_EMITTED": TEST_AND_RECEIPT_CONTRACT_PATH.exists() and gate == "PASS",
            "IMPLEMENTATION_PATH_PREP_9_REVIEW_TARGET_EMITTED": IMPLEMENTATION_REVIEW_TARGET_PATH.exists() and gate == "PASS",
            "IMPLEMENTATION_PATH_PREP_10_NO_IMPLEMENTATION": True,
            "IMPLEMENTATION_PATH_PREP_11_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "IMPLEMENTATION_PATH_PREP_12_NO_SCHEMA_MUTATION": True,
            "IMPLEMENTATION_PATH_PREP_13_NO_MOVE_ADDITION": True,
            "IMPLEMENTATION_PATH_PREP_14_NO_C8_AUTHORIZATION": True,
            "IMPLEMENTATION_PATH_PREP_15_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_accepted_bounded_capability_proposal_implementation_path_prep_summary": {
            "status": status,
            "implementation_path_id": implementation_path_id,
            "proposal_id": proposal.get("proposal_id"),
            "proposal_kind": proposal.get("proposal_kind"),
            "proposed_surface": proposal.get("proposed_surface"),
            "required_capability": proposal.get("required_capability"),
            "decision_record_id": decision_record.get("decision_record_id"),
            "selected_decision": SELECTED_DECISION,
            "proposal_accepted": True if gate == "PASS" else False,
            "bounded_implementation_path_prep_authorized": True if gate == "PASS" else False,
            "implementation_path_prepared": True if gate == "PASS" else False,
            "implementation_review_target_ready": True if gate == "PASS" else False,
            "implementation_candidate_unit": "BUILD_BOUNDED_STRUCTURED_T6_TRIGGER_SURFACE_CAPABILITY_V0",
            "implementation_candidate_status": "CANDIDATE_ONLY_NOT_AUTHORIZED",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "implementation_authorized": False,
            "implementation_executed": False,
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
            "implementation_objective": rel(IMPLEMENTATION_OBJECTIVE_PATH),
            "capability_boundary": rel(CAPABILITY_BOUNDARY_PATH),
            "minimal_implementation_contract": rel(MINIMAL_IMPLEMENTATION_CONTRACT_PATH),
            "implementation_guard_contract": rel(IMPLEMENTATION_GUARD_CONTRACT_PATH),
            "test_and_receipt_contract": rel(TEST_AND_RECEIPT_CONTRACT_PATH),
            "negative_control_contract": rel(NEGATIVE_CONTROL_CONTRACT_PATH),
            "implementation_review_target": rel(IMPLEMENTATION_REVIEW_TARGET_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "accepted_bounded_capability_implementation_path_prep_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"accepted_bounded_capability_implementation_path_prep_receipt_id={receipt_id}")
    print(f"accepted_bounded_capability_implementation_path_prep_receipt_path={rel(receipt_path)}")
    print(f"accepted_bounded_capability_implementation_path_id={implementation_path_id if gate == 'PASS' else 'NONE'}")
    print(f"accepted_bounded_capability_implementation_path_prep_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
