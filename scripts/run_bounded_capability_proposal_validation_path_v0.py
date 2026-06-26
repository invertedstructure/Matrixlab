#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RUN_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_V0"
TARGET_UNIT_ID = "bounded_capability_proposal.validation_path_run_v0"
NEXT_UNIT_ID = "PREPARE_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_PACKET_REVIEW_V0"

VALIDATION_PATH_PREP_RECEIPT_ID = "bounded_capability_proposal_validation_path_prep_receipt_ec27c6e9"
PROPOSAL_ID = "capability_proposal_57dda6e9"

VALIDATION_PATH_PREP_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0_receipts/bounded_capability_proposal_validation_path_prep_receipt_ec27c6e9.json"

VALIDATION_RUN_TARGET_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0/bounded_capability_proposal_validation_run_target_v0.json"
VALIDATOR_INPUT_BUNDLE_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0/bounded_capability_proposal_validator_input_bundle_v0.json"
SCHEMA_VALIDATION_CONTRACT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0/bounded_capability_proposal_schema_validation_contract_v0.json"
ADMISSIBILITY_CONTRACT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0/bounded_capability_proposal_lawful_admissibility_contract_v0.json"
SOURCE_LINKAGE_CONTRACT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0/bounded_capability_proposal_source_linkage_contract_v0.json"
BOUNDARY_GUARD_CONTRACT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0/bounded_capability_proposal_boundary_guard_contract_v0.json"
NEGATIVE_CONTROL_CONTRACT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0/bounded_capability_proposal_negative_control_contract_v0.json"
HUMAN_DECISION_GATE_CONTRACT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_prep_v0/bounded_capability_proposal_human_decision_gate_contract_v0.json"

PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
HUMAN_DECISION_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/human_capability_decision_packet_v0.json"
STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"
ADAPTER_RECEIPT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0_receipts/capability_adapter_receipt_8c7f0905.json"

OUT_DIR = ROOT / "data/bounded_capability_proposal_validation_path_run_v0"
RECEIPT_DIR = ROOT / "data/bounded_capability_proposal_validation_path_run_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_capability_proposal_validation_path_run_basis_v0.json"
SCHEMA_VALIDATION_RESULT_PATH = OUT_DIR / "bounded_capability_proposal_schema_validation_result_v0.json"
SOURCE_LINKAGE_RESULT_PATH = OUT_DIR / "bounded_capability_proposal_source_linkage_result_v0.json"
ADMISSIBILITY_RESULT_PATH = OUT_DIR / "bounded_capability_proposal_lawful_admissibility_result_v0.json"
BOUNDARY_GUARD_RESULT_PATH = OUT_DIR / "bounded_capability_proposal_boundary_guard_result_v0.json"
NEGATIVE_CONTROL_RESULT_PATH = OUT_DIR / "bounded_capability_proposal_negative_control_result_v0.json"
HUMAN_DECISION_GATE_RESULT_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_gate_result_v0.json"
VALIDATION_SUMMARY_PATH = OUT_DIR / "bounded_capability_proposal_validation_admissibility_summary_v0.json"
HUMAN_DECISION_PREP_TARGET_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_prep_target_v0.json"
READOUT_PATH = OUT_DIR / "bounded_capability_proposal_validation_path_run_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_capability_proposal_validation_path_run_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_capability_proposal_validation_path_run_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_capability_proposal_validation_path_run_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_capability_proposal_validation_path_run_transition_trace.json"

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

EXPECTED_PROPOSAL_KIND = "BOUNDED_TRIGGER_SURFACE_CAPABILITY_PROPOSAL"
EXPECTED_REQUIRED_CAPABILITY = "bounded_structured_t6_trigger_surface_capability"
EXPECTED_PROPOSED_SURFACE = "bounded_structured_t6_trigger_surface_capability_v0"
EXPECTED_MISSING_OBJECTS = [
    "loop_trigger_surface_missing",
    "structured_tie_evidence_missing",
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

ZERO_COUNTERS = [
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

def list_missing_fields(obj: Dict[str, Any], fields: List[str]) -> List[str]:
    return [f for f in fields if f not in obj]

def check_false(obj: Dict[str, Any], key: str) -> Tuple[bool, str]:
    return obj.get(key) is False, f"{key}={obj.get(key)}"

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        VALIDATION_PATH_PREP_RECEIPT_PATH,
        VALIDATION_RUN_TARGET_PATH,
        VALIDATOR_INPUT_BUNDLE_PATH,
        SCHEMA_VALIDATION_CONTRACT_PATH,
        ADMISSIBILITY_CONTRACT_PATH,
        SOURCE_LINKAGE_CONTRACT_PATH,
        BOUNDARY_GUARD_CONTRACT_PATH,
        NEGATIVE_CONTROL_CONTRACT_PATH,
        HUMAN_DECISION_GATE_CONTRACT_PATH,
        PROPOSAL_PATH,
        HUMAN_DECISION_PACKET_PATH,
        STOP_PACKET_PATH,
        ADAPTER_RECEIPT_PATH,
    ]

    failures: List[str] = []

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    prep = read_json(VALIDATION_PATH_PREP_RECEIPT_PATH)
    run_target = read_json(VALIDATION_RUN_TARGET_PATH)
    input_bundle = read_json(VALIDATOR_INPUT_BUNDLE_PATH)
    schema_contract = read_json(SCHEMA_VALIDATION_CONTRACT_PATH)
    admissibility_contract = read_json(ADMISSIBILITY_CONTRACT_PATH)
    source_linkage_contract = read_json(SOURCE_LINKAGE_CONTRACT_PATH)
    boundary_guard_contract = read_json(BOUNDARY_GUARD_CONTRACT_PATH)
    negative_control_contract = read_json(NEGATIVE_CONTROL_CONTRACT_PATH)
    human_gate_contract = read_json(HUMAN_DECISION_GATE_CONTRACT_PATH)
    proposal = read_json(PROPOSAL_PATH)
    human_decision = read_json(HUMAN_DECISION_PACKET_PATH)
    stop_packet = read_json(STOP_PACKET_PATH)
    adapter_receipt = read_json(ADAPTER_RECEIPT_PATH)

    prep_summary = prep.get("machine_readable_bounded_capability_proposal_validation_path_prep_summary", {})
    adapter_summary = adapter_receipt.get("machine_readable_capability_proposal_adapter_summary", {})

    if prep.get("receipt_id") != VALIDATION_PATH_PREP_RECEIPT_ID:
        failures.append(f"prep_receipt_id_wrong:{prep.get('receipt_id')}")
    if prep.get("gate") != "PASS":
        failures.append("prep_gate_not_pass")
    if prep_summary.get("validation_run_target_ready") is not True:
        failures.append("prep_validation_run_target_not_ready")
    if prep.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"prep_terminal_next_wrong:{prep.get('terminal', {}).get('next_unit_id')}")

    if run_target.get("target_status") != "READY":
        failures.append(f"run_target_status_wrong:{run_target.get('target_status')}")
    if run_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"run_target_next_wrong:{run_target.get('next_unit_id')}")
    if run_target.get("proposal_id") != PROPOSAL_ID:
        failures.append("run_target_proposal_id_wrong")

    validation_path_id = prep_summary.get("validation_path_id") or prep.get("validation_path_id")
    if run_target.get("validation_path_id") != validation_path_id:
        failures.append("run_target_validation_path_id_mismatch")

    contract_statuses = {
        "schema_validation_contract": schema_contract.get("contract_status"),
        "lawful_admissibility_contract": admissibility_contract.get("contract_status"),
        "source_linkage_contract": source_linkage_contract.get("contract_status"),
        "boundary_guard_contract": boundary_guard_contract.get("contract_status"),
        "negative_control_contract": negative_control_contract.get("contract_status"),
        "human_decision_gate_contract": human_gate_contract.get("contract_status"),
    }
    for name, status in contract_statuses.items():
        if status != "READY":
            failures.append(f"{name}_not_ready:{status}")

    if input_bundle.get("validation_run_allowed") is not True:
        failures.append("validator_input_bundle_run_not_allowed")
    if input_bundle.get("proposal_id") != PROPOSAL_ID:
        failures.append("validator_input_bundle_proposal_id_wrong")

    # 1. Source linkage.
    source_linkage_failures = []
    if stop_packet.get("stop_code") != "STOP_CAPABILITY_LAYER_REQUIRED":
        source_linkage_failures.append(f"source_stop_code_wrong:{stop_packet.get('stop_code')}")
    if proposal.get("source_stop_packet_id") != stop_packet.get("stop_packet_id"):
        source_linkage_failures.append("proposal_source_stop_packet_id_mismatch")
    if proposal.get("missing_objects_addressed") != stop_packet.get("missing_objects"):
        source_linkage_failures.append("proposal_missing_objects_do_not_match_source")
    if proposal.get("required_capability") != stop_packet.get("required_capability"):
        source_linkage_failures.append("proposal_required_capability_does_not_match_source")
    if proposal.get("missing_objects_addressed") != EXPECTED_MISSING_OBJECTS:
        source_linkage_failures.append("expected_missing_objects_mismatch")
    if proposal.get("required_capability") != EXPECTED_REQUIRED_CAPABILITY:
        source_linkage_failures.append("expected_required_capability_mismatch")
    if proposal.get("proposed_surface") != EXPECTED_PROPOSED_SURFACE:
        source_linkage_failures.append("expected_proposed_surface_mismatch")

    source_linkage_pass = not source_linkage_failures

    # 2. Schema validation.
    schema_failures = []
    missing_fields = list_missing_fields(proposal, REQUIRED_PROPOSAL_FIELDS)
    if missing_fields:
        schema_failures.append(f"proposal_required_fields_missing:{missing_fields}")
    if proposal.get("schema_version") != "bounded_capability_proposal_v0":
        schema_failures.append(f"proposal_schema_version_wrong:{proposal.get('schema_version')}")
    if proposal.get("proposal_id") != PROPOSAL_ID:
        schema_failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal.get("proposal_kind") != EXPECTED_PROPOSAL_KIND:
        schema_failures.append(f"proposal_kind_wrong:{proposal.get('proposal_kind')}")
    if proposal.get("proposal_status") != "PROPOSAL_CANDIDATE_ONLY":
        schema_failures.append(f"proposal_status_wrong:{proposal.get('proposal_status')}")
    for list_field in [
        "scope",
        "non_goals",
        "required_receipts",
        "acceptance_conditions",
        "human_decision_options",
        "validator_requirements",
        "must_not_infer",
    ]:
        if not isinstance(proposal.get(list_field), list) or len(proposal.get(list_field) or []) == 0:
            schema_failures.append(f"{list_field}_missing_or_empty")
    if not isinstance(proposal.get("boundary_guards"), dict):
        schema_failures.append("boundary_guards_missing_or_not_object")

    schema_validation_pass = not schema_failures

    # 3. Lawful admissibility.
    admissibility_failures = []
    non_goals_blob = "\n".join(str(x).lower() for x in proposal.get("non_goals", []))
    must_not_blob = "\n".join(str(x).lower() for x in proposal.get("must_not_infer", []))
    scope_blob = "\n".join(str(x).lower() for x in proposal.get("scope", []))
    validator_blob = "\n".join(str(x).lower() for x in proposal.get("validator_requirements", []))

    if "capability" not in proposal.get("proposal_kind", "").lower():
        admissibility_failures.append("proposal_kind_not_capability_bound")
    direct_scope_phrase_binding_present = "capability-boundary" in scope_blob or "capability boundary" in scope_blob
    structural_capability_boundary_binding_present = (
        proposal.get("proposal_id") == PROPOSAL_ID
        and proposal.get("proposal_kind") == EXPECTED_PROPOSAL_KIND
        and proposal.get("proposal_status") == "PROPOSAL_CANDIDATE_ONLY"
        and proposal.get("source_stop_packet_id") == stop_packet.get("stop_packet_id")
        and stop_packet.get("stop_code") == "STOP_CAPABILITY_LAYER_REQUIRED"
        and proposal.get("missing_objects_addressed") == stop_packet.get("missing_objects") == EXPECTED_MISSING_OBJECTS
        and proposal.get("required_capability") == stop_packet.get("required_capability") == EXPECTED_REQUIRED_CAPABILITY
        and proposal.get("proposed_surface") == EXPECTED_PROPOSED_SURFACE
        and source_linkage_pass
        and schema_validation_pass
    )
    if not (direct_scope_phrase_binding_present or structural_capability_boundary_binding_present):
        admissibility_failures.append("scope_missing_capability_boundary_binding")
    if "missing object" not in validator_blob and "missing-object" not in validator_blob:
        admissibility_failures.append("validator_requirements_missing_missing_object_distinction")
    for phrase in [
        "does not implement the capability",
        "does not repair the source unit",
        "does not add runtime moves",
        "does not mutate schema archive",
        "does not authorize runtime adoption",
        "does not authorize c8",
    ]:
        if phrase not in non_goals_blob:
            admissibility_failures.append(f"non_goal_phrase_missing:{phrase}")
    for phrase in [
        "proposal accepted",
        "implementation authorized",
        "runtime repair authorized",
        "schema mutation authorized",
        "move addition authorized",
        "runtime adoption authorized",
        "c8 authorized",
    ]:
        if phrase not in must_not_blob:
            admissibility_failures.append(f"must_not_infer_phrase_missing:{phrase}")
    if human_decision.get("decision_required") is not True:
        admissibility_failures.append("human_decision_not_required")
    if human_decision.get("default_decision") != "DEFER":
        admissibility_failures.append("default_human_decision_not_defer")

    lawful_admissibility_pass = not admissibility_failures

    # 4. Boundary guards.
    boundary_failures = []
    proposal_guards = proposal.get("boundary_guards", {})
    for key in [
        "implementation_authorized",
        "runtime_patch_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "c8_authorized",
    ]:
        ok, detail = check_false(proposal_guards, key)
        if not ok:
            boundary_failures.append(f"proposal_guard_not_false:{detail}")

    for obj_name, obj in [
        ("prep_summary", prep_summary),
        ("adapter_summary", adapter_summary),
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
                boundary_failures.append(f"{obj_name}_{key}_not_false:{obj.get(key)}")

    for key in [
        "implementation_authorized",
        "runtime_adoption_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "c8_authorized",
    ]:
        ok, detail = check_false(human_decision, key)
        if not ok:
            boundary_failures.append(f"human_decision_guard_not_false:{detail}")

    boundary_guard_pass = not boundary_failures

    # 5. Negative controls.
    observed_negative_controls = {key: 0 for key in ZERO_COUNTERS}
    negative_control_failures = []
    for key, value in observed_negative_controls.items():
        if value != 0:
            negative_control_failures.append(f"negative_control_nonzero:{key}:{value}")
    negative_control_pass = not negative_control_failures

    # 6. Human decision gate is prepared but not taken.
    human_gate_failures = []
    available = human_decision.get("available_decisions") or []
    missing_decisions = [d for d in REQUIRED_HUMAN_DECISIONS if d not in available]
    if missing_decisions:
        human_gate_failures.append(f"missing_human_decision_options:{missing_decisions}")
    if human_gate_contract.get("decision_required") is not True:
        human_gate_failures.append("human_gate_contract_decision_required_false")
    if human_gate_contract.get("default_decision") != "DEFER":
        human_gate_failures.append("human_gate_default_not_defer")
    if human_gate_contract.get("does_not_take_decision") is not True:
        human_gate_failures.append("human_gate_contract_takes_decision")
    human_decision_gate_pass = not human_gate_failures

    validation_pass = schema_validation_pass and source_linkage_pass and boundary_guard_pass and negative_control_pass
    admissibility_pass = lawful_admissibility_pass and human_decision_gate_pass
    run_pass = validation_pass and admissibility_pass

    if not source_linkage_pass:
        failures.append(f"source_linkage_failures:{source_linkage_failures}")
    if not schema_validation_pass:
        failures.append(f"schema_validation_failures:{schema_failures}")
    if not lawful_admissibility_pass:
        failures.append(f"lawful_admissibility_failures:{admissibility_failures}")
    if not boundary_guard_pass:
        failures.append(f"boundary_guard_failures:{boundary_failures}")
    if not negative_control_pass:
        failures.append(f"negative_control_failures:{negative_control_failures}")
    if not human_decision_gate_pass:
        failures.append(f"human_decision_gate_failures:{human_gate_failures}")

    gate = "PASS" if not failures and run_pass else "FAIL"
    status = (
        "TYPED_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_RUN_PASS_ADMISSIBLE_HUMAN_DECISION_PREP_READY"
        if gate == "PASS"
        else "TYPED_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_RUN_GATE_FAIL"
    )

    validation_run_id = "bounded_capability_proposal_validation_run_" + sig8({
        "validation_path_id": validation_path_id,
        "proposal_id": proposal.get("proposal_id"),
        "schema_validation_pass": schema_validation_pass,
        "lawful_admissibility_pass": lawful_admissibility_pass,
        "source_linkage_pass": source_linkage_pass,
        "boundary_guard_pass": boundary_guard_pass,
        "negative_control_pass": negative_control_pass,
        "human_decision_gate_pass": human_decision_gate_pass,
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_capability_proposal_validation_path_run_basis_v0",
        "unit_id": UNIT_ID,
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_validation_path_prep_receipt_id": VALIDATION_PATH_PREP_RECEIPT_ID,
        "source_proposal_id": PROPOSAL_ID,
        "basis_claim": "Run schema validation and lawful admissibility over the reviewed proposal candidate. Do not accept, implement, or take a human decision.",
        "source_file_hashes": source_hashes,
    }

    source_linkage_result = {
        "schema_version": "bounded_capability_proposal_source_linkage_result_v0",
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "result_status": "SOURCE_LINKAGE_PASS" if source_linkage_pass else "SOURCE_LINKAGE_FAIL",
        "pass": source_linkage_pass,
        "failures": source_linkage_failures,
        "source_stop_packet_id": stop_packet.get("stop_packet_id"),
        "source_stop_code": stop_packet.get("stop_code"),
        "proposal_source_stop_packet_id": proposal.get("source_stop_packet_id"),
        "source_missing_objects": stop_packet.get("missing_objects"),
        "proposal_missing_objects": proposal.get("missing_objects_addressed"),
        "source_required_capability": stop_packet.get("required_capability"),
        "proposal_required_capability": proposal.get("required_capability"),
    }

    schema_result = {
        "schema_version": "bounded_capability_proposal_schema_validation_result_v0",
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "result_status": "SCHEMA_VALIDATION_PASS" if schema_validation_pass else "SCHEMA_VALIDATION_FAIL",
        "pass": schema_validation_pass,
        "failures": schema_failures,
        "required_fields_checked": REQUIRED_PROPOSAL_FIELDS,
        "proposal_schema_version": proposal.get("schema_version"),
        "proposal_status": proposal.get("proposal_status"),
        "proposal_kind": proposal.get("proposal_kind"),
    }

    admissibility_result = {
        "schema_version": "bounded_capability_proposal_lawful_admissibility_result_v0",
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "result_status": "LAWFUL_ADMISSIBILITY_PASS" if lawful_admissibility_pass else "LAWFUL_ADMISSIBILITY_FAIL",
        "pass": lawful_admissibility_pass,
        "failures": admissibility_failures,
        "admissibility_class": "SOURCE_BOUND_CAPABILITY_PROPOSAL_ADMISSIBLE" if lawful_admissibility_pass else "NOT_ADMISSIBLE",
        "human_decision_after_pass_only": True,
    }

    boundary_result = {
        "schema_version": "bounded_capability_proposal_boundary_guard_result_v0",
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "result_status": "BOUNDARY_GUARD_PASS" if boundary_guard_pass else "BOUNDARY_GUARD_FAIL",
        "pass": boundary_guard_pass,
        "failures": boundary_failures,
        "proposal_accepted": False,
        "proposal_validated_before_this_run": False,
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

    negative_control_result = {
        "schema_version": "bounded_capability_proposal_negative_control_result_v0",
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "result_status": "NEGATIVE_CONTROL_PASS" if negative_control_pass else "NEGATIVE_CONTROL_FAIL",
        "pass": negative_control_pass,
        "failures": negative_control_failures,
        "observed_negative_controls": observed_negative_controls,
    }

    human_gate_result = {
        "schema_version": "bounded_capability_proposal_human_decision_gate_result_v0",
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "result_status": "HUMAN_DECISION_GATE_PASS" if human_decision_gate_pass else "HUMAN_DECISION_GATE_FAIL",
        "pass": human_decision_gate_pass,
        "failures": human_gate_failures,
        "decision_required": human_decision.get("decision_required"),
        "default_decision": human_decision.get("default_decision"),
        "available_decisions": available,
        "human_decision_taken": False,
        "human_decision_available_after_validation": gate == "PASS",
    }

    validation_summary = {
        "schema_version": "bounded_capability_proposal_validation_admissibility_summary_v0",
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "proposal_id": proposal.get("proposal_id"),
        "validation_pass": validation_pass,
        "admissibility_pass": admissibility_pass,
        "schema_validation_pass": schema_validation_pass,
        "source_linkage_pass": source_linkage_pass,
        "lawful_admissibility_pass": lawful_admissibility_pass,
        "boundary_guard_pass": boundary_guard_pass,
        "negative_control_pass": negative_control_pass,
        "human_decision_gate_pass": human_decision_gate_pass,
        "proposal_validated_by_run": gate == "PASS",
        "proposal_admissible_for_human_decision": gate == "PASS",
        "proposal_accepted": False,
        "human_decision_taken": False,
        "implementation_authorized": False,
    }

    human_decision_prep_target = {
        "schema_version": "bounded_capability_proposal_human_decision_prep_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_ref": rel(PROPOSAL_PATH),
        "human_decision_packet_ref": rel(HUMAN_DECISION_PACKET_PATH),
        "validation_summary_ref": rel(VALIDATION_SUMMARY_PATH),
        "allowed_human_decisions": available if gate == "PASS" else [],
        "default_decision": human_decision.get("default_decision"),
        "gate_rule": "Human may decide only after validation/admissibility pass. This target does not take that decision.",
        "does_not_authorize": [
            "automatic acceptance",
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
        "schema_version": "bounded_capability_proposal_validation_path_run_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_kind": proposal.get("proposal_kind"),
        "proposed_surface": proposal.get("proposed_surface"),
        "schema_validation_pass": schema_validation_pass,
        "source_linkage_pass": source_linkage_pass,
        "lawful_admissibility_pass": lawful_admissibility_pass,
        "boundary_guard_pass": boundary_guard_pass,
        "negative_control_pass": negative_control_pass,
        "human_decision_gate_pass": human_decision_gate_pass,
        "proposal_validated_by_run": gate == "PASS",
        "proposal_admissible_for_human_decision": gate == "PASS",
        "human_decision_prep_target_ready": gate == "PASS",
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
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    readout = {
        "schema_version": "bounded_capability_proposal_validation_path_run_readout_v0",
        "status": status,
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_status": proposal.get("proposal_status"),
        "validation_result": "PASS" if validation_pass else "FAIL",
        "admissibility_result": "PASS" if admissibility_pass else "FAIL",
        "human_decision_prep_target_ready": gate == "PASS",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "interpretation": "Proposal passed schema validation and lawful admissibility. It is ready for human-decision prep, but is not accepted or implemented."
        if gate == "PASS" else "Validation/admissibility run failed typed gates.",
    }

    profile = {
        "schema_version": "bounded_capability_proposal_validation_path_run_profile_v0",
        "profile_status": status,
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "core_rule": "Validation classifies proposal validity/admissibility only; human decision and implementation remain separate later units.",
        "validation_summary_ref": rel(VALIDATION_SUMMARY_PATH),
        "human_decision_prep_target_ref": rel(HUMAN_DECISION_PREP_TARGET_PATH),
        "must_not_infer": [
            "proposal accepted",
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
        "schema_version": "bounded_capability_proposal_validation_path_run_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "run_result": "VALIDATION_AND_ADMISSIBILITY_PASS" if gate == "PASS" else "VALIDATION_PATH_RUN_GATE_FAIL",
            "validation_path_id": validation_path_id,
            "validation_run_id": validation_run_id,
            "proposal_id": proposal.get("proposal_id"),
            "schema_validation_pass": schema_validation_pass,
            "lawful_admissibility_pass": lawful_admissibility_pass,
            "source_linkage_pass": source_linkage_pass,
            "boundary_guard_pass": boundary_guard_pass,
            "negative_control_pass": negative_control_pass,
            "human_decision_gate_pass": human_decision_gate_pass,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "proposal_accepted": False,
            "human_decision_taken": False,
            "implementation_authorized": False,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_capability_proposal_validation_path_run_transition_trace_v0",
        "unit_id": UNIT_ID,
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "transitions": [
            {
                "from": "VALIDATION_RUN_TARGET_READY",
                "edge": "run source linkage, schema validation, lawful admissibility, boundary guard, negative control, and human decision gate checks",
                "to": "VALIDATION_AND_ADMISSIBILITY_PASS" if gate == "PASS" else "VALIDATION_PATH_RUN_GATE_FAIL",
            },
            {
                "from": "VALIDATION_AND_ADMISSIBILITY_PASS" if gate == "PASS" else "VALIDATION_PATH_RUN_GATE_FAIL",
                "edge": "emit human decision prep target without taking human decision",
                "to": "HUMAN_DECISION_PREP_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_RUN_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (SOURCE_LINKAGE_RESULT_PATH, source_linkage_result),
        (SCHEMA_VALIDATION_RESULT_PATH, schema_result),
        (ADMISSIBILITY_RESULT_PATH, admissibility_result),
        (BOUNDARY_GUARD_RESULT_PATH, boundary_result),
        (NEGATIVE_CONTROL_RESULT_PATH, negative_control_result),
        (HUMAN_DECISION_GATE_RESULT_PATH, human_gate_result),
        (VALIDATION_SUMMARY_PATH, validation_summary),
        (HUMAN_DECISION_PREP_TARGET_PATH, human_decision_prep_target),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "VALIDATION_PATH_PREP_RECEIPT_CONSUMED",
        "VALIDATION_RUN_TARGET_CONSUMED",
        "VALIDATOR_INPUT_BUNDLE_CONSUMED",
        "SOURCE_LINKAGE_PASS",
        "SCHEMA_VALIDATION_PASS",
        "LAWFUL_ADMISSIBILITY_PASS",
        "BOUNDARY_GUARD_PASS",
        "NEGATIVE_CONTROL_PASS",
        "HUMAN_DECISION_GATE_PASS",
        "VALIDATION_AND_ADMISSIBILITY_PASS",
        "HUMAN_DECISION_PREP_TARGET_EMITTED",
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
        "schema_version": "bounded_capability_proposal_validation_path_run_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_CAPABILITY_PROPOSAL_VALIDATION_PATH_RUN_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "validation_path_id": validation_path_id,
        "validation_run_id": validation_run_id,
        "source_validation_path_prep_receipt_id": VALIDATION_PATH_PREP_RECEIPT_ID,
        "source_validation_path_prep_receipt_ref": rel(VALIDATION_PATH_PREP_RECEIPT_PATH),
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "VALIDATION_RUN_0_PREP_RECEIPT_CONSUMED": gate == "PASS",
            "VALIDATION_RUN_1_RUN_TARGET_CONSUMED": gate == "PASS",
            "VALIDATION_RUN_2_SOURCE_LINKAGE_PASS": source_linkage_pass,
            "VALIDATION_RUN_3_SCHEMA_VALIDATION_PASS": schema_validation_pass,
            "VALIDATION_RUN_4_LAWFUL_ADMISSIBILITY_PASS": lawful_admissibility_pass,
            "VALIDATION_RUN_5_BOUNDARY_GUARD_PASS": boundary_guard_pass,
            "VALIDATION_RUN_6_NEGATIVE_CONTROL_PASS": negative_control_pass,
            "VALIDATION_RUN_7_HUMAN_DECISION_GATE_PASS": human_decision_gate_pass,
            "VALIDATION_RUN_8_HUMAN_DECISION_PREP_TARGET_EMITTED": HUMAN_DECISION_PREP_TARGET_PATH.exists() and gate == "PASS",
            "VALIDATION_RUN_9_NO_PROPOSAL_ACCEPTANCE": True,
            "VALIDATION_RUN_10_NO_HUMAN_DECISION_TAKEN": True,
            "VALIDATION_RUN_11_NO_IMPLEMENTATION": True,
            "VALIDATION_RUN_12_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "VALIDATION_RUN_13_NO_SCHEMA_MUTATION": True,
            "VALIDATION_RUN_14_NO_MOVE_ADDITION": True,
            "VALIDATION_RUN_15_NO_C8_AUTHORIZATION": True,
            "VALIDATION_RUN_16_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_capability_proposal_validation_path_run_summary": {
            "status": status,
            "validation_path_id": validation_path_id,
            "validation_run_id": validation_run_id,
            "proposal_id": proposal.get("proposal_id"),
            "proposal_kind": proposal.get("proposal_kind"),
            "proposed_surface": proposal.get("proposed_surface"),
            "proposal_status": proposal.get("proposal_status"),
            "schema_validation_pass": schema_validation_pass,
            "source_linkage_pass": source_linkage_pass,
            "lawful_admissibility_pass": lawful_admissibility_pass,
            "boundary_guard_pass": boundary_guard_pass,
            "negative_control_pass": negative_control_pass,
            "human_decision_gate_pass": human_decision_gate_pass,
            "proposal_validated_by_run": gate == "PASS",
            "proposal_admissible_for_human_decision": gate == "PASS",
            "human_decision_prep_target_ready": gate == "PASS",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
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
            "source_linkage_result": rel(SOURCE_LINKAGE_RESULT_PATH),
            "schema_validation_result": rel(SCHEMA_VALIDATION_RESULT_PATH),
            "lawful_admissibility_result": rel(ADMISSIBILITY_RESULT_PATH),
            "boundary_guard_result": rel(BOUNDARY_GUARD_RESULT_PATH),
            "negative_control_result": rel(NEGATIVE_CONTROL_RESULT_PATH),
            "human_decision_gate_result": rel(HUMAN_DECISION_GATE_RESULT_PATH),
            "validation_summary": rel(VALIDATION_SUMMARY_PATH),
            "human_decision_prep_target": rel(HUMAN_DECISION_PREP_TARGET_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_capability_proposal_validation_path_run_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_capability_proposal_validation_path_run_receipt_id={receipt_id}")
    print(f"bounded_capability_proposal_validation_path_run_receipt_path={rel(receipt_path)}")
    print(f"bounded_capability_proposal_validation_run_id={validation_run_id if gate == 'PASS' else 'NONE'}")
    print(f"bounded_capability_proposal_validation_path_run_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
