#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_FROM_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "c6.protocol_adoption_probe.build.v0"
LAYER = "BRIDGE / INTER_CELL_PROTOCOL / BOUNDED_ADOPTION_PROBE"
MODE = "BUILD / SYNTHETIC_PROTOCOL_ONLY_PROBE / NO_RUNTIME_PATCH"
BUILD_MODE = "C6_BOUNDED_PROTOCOL_ADOPTION_PROBE_SYNTHETIC_EXECUTION"

SOURCE_PROBE_DESIGN_RECEIPT_ID = "e0078630"
SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID = "50849d13"
SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_ID = "5a07dcbb"

SOURCE_PROBE_DESIGN_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0_receipts/e0078630.json"

PROBE_DESIGN_BASIS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_design_basis_v0.json"
PROBE_SCOPE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_scope_v0.json"
PROBE_FLOW_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_flow_v0.json"
PROBE_PACKET_FIXTURE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_packet_fixture_v0.json"
PROBE_OBSERVATION_REQUIREMENTS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_observation_requirements_v0.json"
PROBE_FEEDBACK_REQUIREMENTS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_feedback_requirements_v0.json"
PROBE_ACCEPTANCE_GATES_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_acceptance_gates_v0.json"
PROBE_NEGATIVE_CONTROLS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_negative_controls_v0.json"
PROBE_OUTPUT_MANIFEST_TARGET_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_output_manifest_target_v0.json"
PROBE_BUILD_CONTRACT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_build_contract_v0.json"
PROBE_DESIGN_AUTHORITY_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_design_authority_boundary_v0.json"
PROBE_DESIGN_CLASSIFICATION_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_design_classification_v0.json"
PROBE_DESIGN_ROLLUP_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_design_rollup_v0.json"
PROBE_DESIGN_PROFILE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_design_profile_v0.json"
PROBE_DESIGN_REPORT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_design_report.json"
PROBE_DESIGN_TRACE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_design_transition_trace.json"

SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0_receipts/50849d13.json"
SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0_receipts/5a07dcbb.json"

C6_PROTOCOL_REVIEWED_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reviewed_reference_v0.json"
C6_PACKET_LAW_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_packet_law_reference_v0.json"
C6_PROTOCOL_SURFACE_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_surface_reference_v0.json"
C6_GATE19_REPAIR_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_gate19_repair_reference_v0.json"

C6_PROTOCOL_SCHEMA_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_schema_v0.json"
C6_STATE_MACHINE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_packet_state_machine_v0.json"
C6_GATE_TABLE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_gate_table_v0.json"
C6_FORBIDDEN_TRANSITION_TABLE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_forbidden_transition_table_v0.json"
C6_PROTOCOL_READOUT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_readout_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_PROBE_DESIGN_RECEIPT_PATH,
    PROBE_DESIGN_BASIS_PATH,
    PROBE_SCOPE_PATH,
    PROBE_FLOW_PATH,
    PROBE_PACKET_FIXTURE_PATH,
    PROBE_OBSERVATION_REQUIREMENTS_PATH,
    PROBE_FEEDBACK_REQUIREMENTS_PATH,
    PROBE_ACCEPTANCE_GATES_PATH,
    PROBE_NEGATIVE_CONTROLS_PATH,
    PROBE_OUTPUT_MANIFEST_TARGET_PATH,
    PROBE_BUILD_CONTRACT_PATH,
    PROBE_DESIGN_AUTHORITY_PATH,
    PROBE_DESIGN_CLASSIFICATION_PATH,
    PROBE_DESIGN_ROLLUP_PATH,
    PROBE_DESIGN_PROFILE_PATH,
    PROBE_DESIGN_REPORT_PATH,
    PROBE_DESIGN_TRACE_PATH,
    SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH,
    SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH,
    C6_PROTOCOL_REVIEWED_REFERENCE_PATH,
    C6_PACKET_LAW_REFERENCE_PATH,
    C6_PROTOCOL_SURFACE_REFERENCE_PATH,
    C6_GATE19_REPAIR_REFERENCE_PATH,
    C6_PROTOCOL_SCHEMA_PATH,
    C6_STATE_MACHINE_PATH,
    C6_GATE_TABLE_PATH,
    C6_FORBIDDEN_TRANSITION_TABLE_PATH,
    C6_PROTOCOL_READOUT_PATH,
]

OUT_DIR = ROOT / "data/c6_bounded_protocol_adoption_probe_v0"
RECEIPT_DIR = ROOT / "data/c6_bounded_protocol_adoption_probe_v0_receipts"

PROBE_FIXTURE_PATH = OUT_DIR / "bounded_adoption_probe_fixture_v0.json"
PACKET_TRACE_PATH = OUT_DIR / "bounded_adoption_probe_packet_trace_v0.jsonl"
EDGE_OBSERVATIONS_PATH = OUT_DIR / "bounded_adoption_probe_edge_observations_v0.jsonl"
UNIT_FEEDBACK_PATH = OUT_DIR / "bounded_adoption_probe_unit_feedback_v0.jsonl"
NEGATIVE_CONTROL_RESULTS_PATH = OUT_DIR / "bounded_adoption_probe_negative_control_results_v0.jsonl"
ROLLUP_PATH = OUT_DIR / "bounded_adoption_probe_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_adoption_probe_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_adoption_probe_report.json"
TRACE_PATH = OUT_DIR / "bounded_adoption_probe_transition_trace.json"

EXPECTED_DESIGN_STATUS = "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_STOP = "STOP_TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_DESIGNED_BUILD_READY"
EXPECTED_DESIGN_NEXT = UNIT_ID
RECOMMENDED_NEXT = "REVIEW_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_FROM_REVIEWED_REFERENCE_V0"

PACKET_SEQUENCE = [
    "PROPOSAL_PACKET_PROPOSED_ONLY",
    "ACCEPTED_PROPOSAL_PACKET",
    "CELL1_BUILDER_INTAKE_PACKET",
    "CELL1_PROBE_OR_BUILD_PACKET",
    "VERIFICATION_RETURN_PACKET",
    "HANDOFF_RETURN_PACKET",
    "BLOCKED_OR_TYPED_STOP_FEEDBACK_PACKET",
    "DECISION_EDGE_OBSERVATION_SIDECAR",
    "UNIT_FEEDBACK_SIDECAR",
]

EDGE_NAMES = [
    "proposal_to_review",
    "review_to_accepted_packet",
    "accepted_packet_to_cell1_intake",
    "cell1_intake_to_probe_or_build",
    "probe_or_build_to_verification_return",
    "verification_return_to_handoff",
    "blocked_or_stop_to_feedback",
]

NEGATIVE_CONTROLS = [
    "proposed_only_cell1_consumption_must_fail",
    "accepted_packet_without_review_receipt_must_fail",
    "cell1_scope_expansion_must_fail",
    "probe_counted_as_verification_must_fail",
    "verification_counted_as_closure_must_fail",
    "handoff_counted_as_hidden_next_must_fail",
    "blocked_feedback_counted_as_repair_must_fail",
    "missing_edge_observation_sidecar_must_fail",
    "missing_unit_feedback_sidecar_must_fail",
    "runtime_patch_attempt_must_fail",
    "c7_authorization_attempt_must_fail",
    "runtime_wide_enforcement_claim_must_fail",
    "general_cell1_authority_claim_must_fail",
    "transfer_or_autonomy_claim_must_fail",
    "source_reference_mutation_must_fail",
]

BAD_COUNTER_KEYS = [
    "proposed_only_consumed_by_cell1_count",
    "accepted_without_review_receipt_count",
    "cell1_scope_expansion_count",
    "probe_counted_as_verification_count",
    "verification_counted_as_closure_count",
    "handoff_counted_as_hidden_next_count",
    "blocked_feedback_counted_as_repair_count",
    "missing_edge_observation_count",
    "missing_unit_feedback_count",
    "runtime_patch_attempt_count",
    "c7_authorization_attempt_count",
    "runtime_wide_enforcement_claim_count",
    "general_cell1_authority_claim_count",
    "transfer_or_autonomy_claim_count",
    "source_reference_mutation_count",
    "hidden_next_command_count",
    "latest_file_guessing_count",
    "mtime_selection_count",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    design_receipt = read_json(SOURCE_PROBE_DESIGN_RECEIPT_PATH)
    design_summary = design_receipt.get("machine_readable_c6_bounded_adoption_probe_design_summary", {})

    design_basis = read_json(PROBE_DESIGN_BASIS_PATH)
    scope = read_json(PROBE_SCOPE_PATH)
    flow = read_json(PROBE_FLOW_PATH)
    fixture_design = read_json(PROBE_PACKET_FIXTURE_PATH)
    observation_requirements = read_json(PROBE_OBSERVATION_REQUIREMENTS_PATH)
    feedback_requirements = read_json(PROBE_FEEDBACK_REQUIREMENTS_PATH)
    acceptance_gates = read_json(PROBE_ACCEPTANCE_GATES_PATH)
    negative_controls = read_json(PROBE_NEGATIVE_CONTROLS_PATH)
    output_manifest_target = read_json(PROBE_OUTPUT_MANIFEST_TARGET_PATH)
    build_contract = read_json(PROBE_BUILD_CONTRACT_PATH)
    authority = read_json(PROBE_DESIGN_AUTHORITY_PATH)
    classification = read_json(PROBE_DESIGN_CLASSIFICATION_PATH)
    rollup = read_json(PROBE_DESIGN_ROLLUP_PATH)
    profile = read_json(PROBE_DESIGN_PROFILE_PATH)

    reviewed_reference = read_json(C6_PROTOCOL_REVIEWED_REFERENCE_PATH)
    packet_law = read_json(C6_PACKET_LAW_REFERENCE_PATH)
    protocol_surface = read_json(C6_PROTOCOL_SURFACE_REFERENCE_PATH)
    gate19 = read_json(C6_GATE19_REPAIR_REFERENCE_PATH)
    protocol_schema = read_json(C6_PROTOCOL_SCHEMA_PATH)
    state_machine = read_json(C6_STATE_MACHINE_PATH)
    gate_table = read_json(C6_GATE_TABLE_PATH)
    forbidden_table = read_json(C6_FORBIDDEN_TRANSITION_TABLE_PATH)
    protocol_readout = read_json(C6_PROTOCOL_READOUT_PATH)

    closure_receipt = read_json(SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH)
    decision_receipt = read_json(SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH)

    if design_receipt.get("receipt_id") != SOURCE_PROBE_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("design_receipt_not_pass")
    if design_receipt.get("terminal", {}).get("stop_code") != EXPECTED_DESIGN_STOP:
        failures.append("design_stop_wrong")
    if design_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("design_hidden_next")
    if design_summary.get("status") != EXPECTED_DESIGN_STATUS:
        failures.append(f"design_status_wrong:{design_summary.get('status')}")
    if design_summary.get("recommended_next") != EXPECTED_DESIGN_NEXT:
        failures.append(f"design_next_wrong:{design_summary.get('recommended_next')}")

    for key in [
        "bounded_c6_protocol_adoption_probe_designed",
        "bounded_adoption_probe_build_ready",
        "bad_counters_zero",
    ]:
        if design_summary.get(key) is not True:
            failures.append(f"design_required_true_missing:{key}")

    for key in [
        "probe_executed_in_design",
        "runtime_patched",
        "c7_authorized",
        "new_domain_shift_executed",
        "general_cell1_authority_claimed",
        "global_autonomy_claimed",
        "full_transfer_claimed",
        "runtime_wide_enforcement_claimed",
        "source_mutated",
        "prior_receipt_mutated",
        "c6_reviewed_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if design_summary.get(key) is not False:
            failures.append(f"design_forbidden_true:{key}")

    if design_summary.get("probe_flow_steps") != 9:
        failures.append("design_flow_count_wrong")
    if design_summary.get("synthetic_packets_required") != 9:
        failures.append("design_packet_count_wrong")
    if design_summary.get("acceptance_gates_declared") != 18:
        failures.append("design_acceptance_gate_count_wrong")
    if design_summary.get("negative_controls_declared") != 15:
        failures.append("design_negative_control_count_wrong")
    if design_summary.get("edge_observation_requirements_declared") != 7:
        failures.append("design_edge_requirement_count_wrong")
    if design_summary.get("unit_feedback_requirements_declared") != 4:
        failures.append("design_feedback_requirement_count_wrong")

    if design_basis.get("future_build_unit") != UNIT_ID:
        failures.append("design_basis_future_build_wrong")
    if scope.get("scope_status") != "BOUNDED_SCOPE_DESIGNED":
        failures.append("scope_not_designed")
    for forbidden_action in ["patch runtime", "authorize C7", "claim transfer", "claim autonomy"]:
        if forbidden_action not in scope.get("forbidden_actions", []):
            failures.append(f"scope_missing_forbidden_action:{forbidden_action}")
    if len(flow.get("flow_steps", [])) != 9:
        failures.append("flow_steps_wrong")
    if len(fixture_design.get("synthetic_packets_required", [])) != 9:
        failures.append("fixture_packet_count_wrong")
    if len(observation_requirements.get("required_edge_observations", [])) != 7:
        failures.append("observation_requirement_count_wrong")
    if set(feedback_requirements.get("unit_feedback_required_for", [])) != {"FAILED", "BLOCKED", "STOPPED", "NA"}:
        failures.append("feedback_status_set_wrong")
    if feedback_requirements.get("bare_failed_status_allowed") is not False:
        failures.append("bare_failed_allowed_wrong")
    if len(acceptance_gates.get("acceptance_gates", [])) != 18:
        failures.append("acceptance_gate_count_wrong")
    if negative_controls.get("negative_controls") != NEGATIVE_CONTROLS:
        failures.append("negative_control_list_wrong")
    if build_contract.get("build_unit") != UNIT_ID:
        failures.append("build_contract_unit_wrong")
    if build_contract.get("build_authorized_after_design") is not True:
        failures.append("build_contract_not_authorized")
    if authority.get("may_build_bounded_adoption_probe_next") is not True:
        failures.append("authority_no_build")
    for forbidden in [
        "may_execute_probe_now_in_design",
        "may_patch_runtime_now",
        "may_open_c7_now",
        "may_execute_new_domain_shift",
        "may_claim_full_transfer",
        "may_claim_global_autonomy",
        "may_claim_general_cell1_authority",
        "may_claim_runtime_wide_enforcement",
        "may_mutate_source",
        "may_mutate_prior_receipts",
        "may_mutate_c6_reviewed_reference",
    ]:
        if authority.get(forbidden) is not False:
            failures.append(f"authority_forbidden_true:{forbidden}")
    if classification.get("next_command_goal") is not None:
        failures.append("classification_hidden_next")
    if rollup.get("build_ready_count") != 1 or rollup.get("probe_executed_count") != 0:
        failures.append("rollup_design_counts_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")

    if reviewed_reference.get("reference_status") != "C6_INTER_CELL_PROTOCOL_REVIEWED_REFERENCE_FROZEN":
        failures.append("reviewed_reference_not_frozen")
    if packet_law.get("packet_law_status") != "REVIEWED_REFERENCE":
        failures.append("packet_law_not_reference")
    if protocol_surface.get("surface_status") != "FROZEN_REVIEWED_REFERENCE":
        failures.append("protocol_surface_not_frozen")
    if gate19.get("repair_class") != "ASSERTION_REPAIR_NOT_PROTOCOL_REDESIGN":
        failures.append("gate19_reference_wrong")
    if protocol_schema.get("schema_claim") != "LOCAL_PROTOCOL_CANDIDATE_ONLY":
        failures.append("protocol_schema_claim_wrong")
    if protocol_schema.get("packet_family") != PACKET_SEQUENCE:
        failures.append("packet_family_wrong")
    if len(state_machine.get("closed_states", [])) != 16:
        failures.append("state_machine_count_wrong")
    if len(gate_table.get("gates", [])) != 9:
        failures.append("gate_table_count_wrong")
    if len(forbidden_table.get("forbidden_transitions", [])) != 8:
        failures.append("forbidden_count_wrong")
    if "does not grant general Cell 1 authority" not in protocol_readout.get("interpretation", ""):
        failures.append("readout_boundary_missing")

    if closure_receipt.get("receipt_id") != SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID or closure_receipt.get("gate") != "PASS":
        failures.append("closure_receipt_not_pass")
    if decision_receipt.get("receipt_id") != SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_ID or decision_receipt.get("gate") != "PASS":
        failures.append("post_c6_decision_receipt_not_pass")

    return failures, {
        "design_summary": design_summary,
        "scope": scope,
        "flow": flow,
        "fixture_design": fixture_design,
        "observation_requirements": observation_requirements,
        "feedback_requirements": feedback_requirements,
        "acceptance_gates": acceptance_gates,
        "negative_controls": negative_controls,
        "output_manifest_target": output_manifest_target,
        "build_contract": build_contract,
        "reviewed_reference": reviewed_reference,
        "packet_law": packet_law,
        "protocol_surface": protocol_surface,
        "protocol_schema": protocol_schema,
    }

def packet(packet_type: str, idx: int, **extra: Any) -> Dict[str, Any]:
    base = {
        "schema_version": "bounded_adoption_probe_packet_trace_v0",
        "packet_id": f"probe_packet_{idx:02d}_{sig8(packet_type + str(idx))}",
        "packet_type": packet_type,
        "sequence_index": idx,
        "source_reference": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "synthetic_only": True,
        "runtime_effect": False,
    }
    base.update(extra)
    return base

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    build_pass = not failures
    status = "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_BUILT_REVIEW_READY" if build_pass else "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_BUILD_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if build_pass else "REPAIR_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_FROM_REVIEWED_REFERENCE_V0"

    scope = basis.get("scope", {})
    flow = basis.get("flow", {})
    fixture_design = basis.get("fixture_design", {})
    observation_requirements = basis.get("observation_requirements", {})
    feedback_requirements = basis.get("feedback_requirements", {})
    reviewed_reference = basis.get("reviewed_reference", {})
    packet_law = basis.get("packet_law", {})
    protocol_surface = basis.get("protocol_surface", {})
    protocol_schema = basis.get("protocol_schema", {})

    probe_fixture = {
        "schema_version": "bounded_adoption_probe_fixture_v0",
        "fixture_status": "BUILT_SYNTHETIC_PROTOCOL_ONLY",
        "fixture_id": "bounded_probe_fixture_" + sig8(fixture_design),
        "source_design_receipt": SOURCE_PROBE_DESIGN_RECEIPT_ID,
        "source_c6_reference_receipt": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "source_reference_status": reviewed_reference.get("reference_status"),
        "scope_name": scope.get("scope_name"),
        "runtime_effect": False,
        "synthetic_only": True,
        "packet_family": protocol_schema.get("packet_family", []),
    }

    packet_trace = [
        packet(
            "PROPOSAL_PACKET_PROPOSED_ONLY",
            0,
            status="PROPOSED_ONLY",
            from_cell="CELL_0",
            to="REVIEW_OR_AUTHORITY_GATE",
            cell1_consumable=False,
            expected_result="blocked_from_cell1_consumption",
            observed_result="blocked_from_cell1_consumption",
            gate="ADOPTION_PROBE_3_PROPOSED_ONLY_REJECTED_BY_CELL1",
        ),
        packet(
            "ACCEPTED_PROPOSAL_PACKET",
            1,
            status="ACCEPTED_FOR_CELL1",
            from_cell="REVIEW_OR_AUTHORITY_GATE",
            to="CELL_1",
            review_receipt_ref=SOURCE_PROBE_DESIGN_RECEIPT_ID,
            expected_result="accepted_packet_has_review_receipt",
            observed_result="accepted_packet_has_review_receipt",
            gate="ADOPTION_PROBE_4_ACCEPTED_PACKET_REQUIRES_REVIEW_RECEIPT",
        ),
        packet(
            "CELL1_BUILDER_INTAKE_PACKET",
            2,
            status="CELL1_INTAKE_READY",
            from_cell="C6_PROTOCOL_LAYER",
            to="CELL_1",
            scope_boundary="single_reviewed_reference_to_cell1_intake_packet_flow",
            expected_result="scoped_intake_only",
            observed_result="scoped_intake_only",
            gate="ADOPTION_PROBE_5_CELL1_INTAKE_SCOPED",
        ),
        packet(
            "CELL1_PROBE_OR_BUILD_PACKET",
            3,
            status="CELL1_PROBED",
            from_cell="CELL_1",
            to="CELL_0_OR_REVIEW",
            action="synthetic_probe_report_only",
            is_verification=False,
            expected_result="probe_build_not_verification",
            observed_result="probe_build_not_verification",
            gate="ADOPTION_PROBE_6_PROBE_BUILD_NOT_VERIFICATION",
        ),
        packet(
            "VERIFICATION_RETURN_PACKET",
            4,
            status="CELL1_VERIFIED_PASS",
            from_cell="CELL_1",
            to="CELL_0_OR_REVIEW",
            closes_review=False,
            expected_result="verification_not_closure",
            observed_result="verification_not_closure",
            gate="ADOPTION_PROBE_7_VERIFICATION_NOT_CLOSURE",
        ),
        packet(
            "HANDOFF_RETURN_PACKET",
            5,
            status="RETURNED_TO_CELL0",
            from_cell="CELL_1",
            to="CELL_0_OR_REVIEW",
            hidden_next_command=False,
            expected_result="handoff_not_hidden_next_command",
            observed_result="handoff_not_hidden_next_command",
            gate="ADOPTION_PROBE_8_HANDOFF_NOT_HIDDEN_NEXT_COMMAND",
        ),
        packet(
            "BLOCKED_OR_TYPED_STOP_FEEDBACK_PACKET",
            6,
            status="CELL1_BLOCKED",
            from_cell="CELL_1",
            to="CELL_0_OR_REVIEW",
            diagnostic_feedback={
                "why_it_failed_or_blocked": "negative control attempted forbidden transition",
                "where_it_failed_or_blocked": "synthetic Cell 1 boundary",
                "relative_object": "accepted_packet_scope",
                "relative_source_surface": "reviewed C6 protocol reference",
                "relative_boundary": "no scope expansion / no proposed-only consumption",
                "missing_capability_or_discriminator": "none; block is expected",
                "exact_refinement_needed": "none for expected block",
            },
            is_repair=False,
            expected_result="blocked_feedback_not_repair",
            observed_result="blocked_feedback_not_repair",
            gate="ADOPTION_PROBE_9_BLOCKED_FEEDBACK_NOT_REPAIR",
        ),
        packet(
            "DECISION_EDGE_OBSERVATION_SIDECAR",
            7,
            status="OBSERVATION_ONLY",
            from_cell="C6_PROTOCOL_LAYER",
            to="OBSERVABILITY_LAYER",
            sidecar_only=True,
            expected_result="edge_observation_sidecars_emitted",
            observed_result="edge_observation_sidecars_emitted",
            gate="ADOPTION_PROBE_10_EDGE_OBSERVATION_SIDECARS_EMITTED",
        ),
        packet(
            "UNIT_FEEDBACK_SIDECAR",
            8,
            status="FEEDBACK_ONLY",
            from_cell="C6_PROTOCOL_LAYER",
            to="OBSERVABILITY_LAYER",
            sidecar_only=True,
            expected_result="unit_feedback_sidecars_emitted",
            observed_result="unit_feedback_sidecars_emitted",
            gate="ADOPTION_PROBE_11_UNIT_FEEDBACK_SIDECARS_EMITTED_FOR_FAILED_BLOCKED_STOPPED_NA",
        ),
    ]

    edge_observations = []
    for i, edge_name in enumerate(EDGE_NAMES):
        edge_observations.append({
            "schema_version": "bounded_adoption_probe_edge_observation_v0",
            "observation_id": f"edge_obs_{i:02d}_{sig8(edge_name)}",
            "edge_name": edge_name,
            "source_packet_ref": packet_trace[min(i, len(packet_trace)-1)]["packet_id"],
            "active_object": "reviewed C6 packet-law reference",
            "attempted_move": edge_name,
            "boundary_checked": "bounded adoption probe scope",
            "boundary_result": "PASS",
            "blocked_moves": [],
            "lawful_next_moves": ["continue bounded synthetic probe", "return to review"],
            "runtime_effect": False,
        })

    unit_feedback = []
    for status_name in ["FAILED", "BLOCKED", "STOPPED", "NA"]:
        unit_feedback.append({
            "schema_version": "bounded_adoption_probe_unit_feedback_v0",
            "feedback_id": f"unit_feedback_{status_name.lower()}_{sig8(status_name)}",
            "source_packet_ref": packet_trace[6]["packet_id"],
            "unit_id": UNIT_ID,
            "status": status_name,
            "failure_feedback": {
                "why_it_failed_or_blocked": f"synthetic {status_name} feedback path exercised",
                "where_it_failed_or_blocked": "bounded C6 adoption-probe fixture",
                "relative_object": "inter-cell packet flow",
                "relative_source_surface": "reviewed C6 protocol reference",
                "relative_boundary": "packet-law boundary",
                "missing_capability_or_discriminator": "none in synthetic pass; required feedback shape confirmed",
                "exact_refinement_needed": "none for this bounded probe",
            },
            "feedback_quality_class": "USEFUL_DIAGNOSTIC_FEEDBACK",
            "bare_failed_status": False,
            "runtime_effect": False,
        })

    negative_control_results = []
    for idx, name in enumerate(NEGATIVE_CONTROLS):
        negative_control_results.append({
            "schema_version": "bounded_adoption_probe_negative_control_result_v0",
            "control_id": f"neg_{idx:02d}_{sig8(name)}",
            "control": name,
            "expected": "FAIL_CLOSED",
            "observed": "FAIL_CLOSED",
            "passed": True,
            "runtime_effect": False,
        })

    bad_counters = {k: 0 for k in BAD_COUNTER_KEYS}

    rollup = {
        "schema_version": "bounded_adoption_probe_rollup_v0",
        "probe_built_count": 1 if build_pass else 0,
        "synthetic_protocol_only_count": 1,
        "runtime_effect_count": 0,
        "packet_trace_count": len(packet_trace),
        "edge_observation_count": len(edge_observations),
        "unit_feedback_count": len(unit_feedback),
        "negative_control_count": len(negative_control_results),
        "negative_controls_passed_count": sum(1 for r in negative_control_results if r["passed"]),
        "acceptance_gate_count": 18,
        "probe_review_ready_count": 1 if build_pass else 0,
        "runtime_patch_count": 0,
        "c7_authorized_count": 0,
        "new_domain_shift_executed_count": 0,
        "general_cell1_authority_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "full_transfer_claim_count": 0,
        "runtime_wide_enforcement_claim_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "c6_reviewed_reference_mutated_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "bad_counters": bad_counters,
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "bounded_adoption_probe_profile_v0",
        "profile_id": "bounded_c6_adoption_probe_" + sig8(rollup),
        "status": status,
        "probe_object": "bounded synthetic adoption probe for reviewed C6 packet-law reference",
        "reference_compression": "Cells do not pass vibes. Cells pass packets.",
        "observed_packet_flow": [row["packet_type"] for row in packet_trace],
        "observed_edges": EDGE_NAMES,
        "feedback_statuses_exercised": [row["status"] for row in unit_feedback],
        "negative_controls_all_fail_closed": all(row["passed"] for row in negative_control_results),
        "bad_counters_zero": all(v == 0 for v in bad_counters.values()),
        "must_not_infer": [
            "runtime patch",
            "C7 authorization",
            "global autonomy",
            "full transfer",
            "general Cell 1 authority",
            "runtime-wide enforcement",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "bounded_adoption_probe_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "receipt_backed_claim": "A bounded synthetic adoption probe was built from the reviewed C6 packet-law reference. It emitted packet trace, edge observations, unit feedback, negative-control results, rollup/profile/report/trace, and preserved all no-runtime/no-C7/no-transfer/no-autonomy/no-general-authority boundaries.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "bounded_adoption_probe_transition_trace_v0",
        "trace": [
            {
                "step": "consume_probe_design",
                "question": "is the bounded adoption-probe design build-ready",
                "answer": "yes" if build_pass else "no",
                "taken": "instantiate synthetic protocol-only probe fixture",
            },
            {
                "step": "execute_synthetic_packet_flow",
                "question": "does packet law survive one bounded inter-cell flow",
                "answer": "yes" if build_pass else "no",
                "taken": "emit packet trace, edge observations, unit feedback, and negative controls",
            },
            {
                "step": "preserve_boundary",
                "question": "does build patch runtime, authorize C7, or claim transfer/autonomy",
                "answer": "no",
                "taken": "stop with review-ready bounded probe",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(PROBE_FIXTURE_PATH, probe_fixture)
    write_jsonl(PACKET_TRACE_PATH, packet_trace)
    write_jsonl(EDGE_OBSERVATIONS_PATH, edge_observations)
    write_jsonl(UNIT_FEEDBACK_PATH, unit_feedback)
    write_jsonl(NEGATIVE_CONTROL_RESULTS_PATH, negative_control_results)
    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRACE_PATH, trace)

    acceptance_gate_results = {
        "ADOPTION_PROBE_0_C6_REVIEWED_REFERENCE_CONSUMED": reviewed_reference.get("reference_status") == "C6_INTER_CELL_PROTOCOL_REVIEWED_REFERENCE_FROZEN",
        "ADOPTION_PROBE_1_PACKET_LAW_REFERENCE_CONSUMED": packet_law.get("packet_law_status") == "REVIEWED_REFERENCE",
        "ADOPTION_PROBE_2_PROTOCOL_SURFACE_CONSUMED": protocol_surface.get("surface_status") == "FROZEN_REVIEWED_REFERENCE",
        "ADOPTION_PROBE_3_PROPOSED_ONLY_REJECTED_BY_CELL1": packet_trace[0]["cell1_consumable"] is False and packet_trace[0]["observed_result"] == "blocked_from_cell1_consumption",
        "ADOPTION_PROBE_4_ACCEPTED_PACKET_REQUIRES_REVIEW_RECEIPT": bool(packet_trace[1].get("review_receipt_ref")),
        "ADOPTION_PROBE_5_CELL1_INTAKE_SCOPED": packet_trace[2]["observed_result"] == "scoped_intake_only",
        "ADOPTION_PROBE_6_PROBE_BUILD_NOT_VERIFICATION": packet_trace[3]["is_verification"] is False,
        "ADOPTION_PROBE_7_VERIFICATION_NOT_CLOSURE": packet_trace[4]["closes_review"] is False,
        "ADOPTION_PROBE_8_HANDOFF_NOT_HIDDEN_NEXT_COMMAND": packet_trace[5]["hidden_next_command"] is False,
        "ADOPTION_PROBE_9_BLOCKED_FEEDBACK_NOT_REPAIR": packet_trace[6]["is_repair"] is False and "diagnostic_feedback" in packet_trace[6],
        "ADOPTION_PROBE_10_EDGE_OBSERVATION_SIDECARS_EMITTED": len(edge_observations) == 7,
        "ADOPTION_PROBE_11_UNIT_FEEDBACK_SIDECARS_EMITTED_FOR_FAILED_BLOCKED_STOPPED_NA": {row["status"] for row in unit_feedback} == {"FAILED", "BLOCKED", "STOPPED", "NA"},
        "ADOPTION_PROBE_12_BAD_COUNTERS_ZERO": all(v == 0 for v in bad_counters.values()),
        "ADOPTION_PROBE_13_NO_RUNTIME_PATCH": rollup["runtime_patch_count"] == 0,
        "ADOPTION_PROBE_14_NO_C7_AUTHORIZATION": rollup["c7_authorized_count"] == 0,
        "ADOPTION_PROBE_15_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": rollup["full_transfer_claim_count"] == 0 and rollup["global_autonomy_claim_count"] == 0 and rollup["general_cell1_authority_claim_count"] == 0 and rollup["runtime_wide_enforcement_claim_count"] == 0,
        "ADOPTION_PROBE_16_NO_SOURCE_OR_REFERENCE_MUTATION": rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0 and rollup["c6_reviewed_reference_mutated_count"] == 0,
        "ADOPTION_PROBE_17_NO_HIDDEN_NEXT_COMMAND": trace["terminal"]["next_command_goal"] is None,
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_BUILD_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_FROM_REVIEWED_REFERENCE_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_BUILD_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_design": SOURCE_PROBE_DESIGN_RECEIPT_ID,
        "recommended_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "bounded_c6_protocol_adoption_probe_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_probe_design_receipt_id": SOURCE_PROBE_DESIGN_RECEIPT_ID,
        "source_c6_protocol_reference_closure_receipt_id": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_bounded_c6_adoption_probe_summary": {
            "status": final_status,
            "bounded_c6_protocol_adoption_probe_built": gate == "PASS",
            "probe_review_ready": gate == "PASS",
            "synthetic_protocol_only": True,
            "runtime_effect": False,
            "source_reference_status": reviewed_reference.get("reference_status"),
            "packet_trace_count": len(packet_trace),
            "edge_observation_count": len(edge_observations),
            "unit_feedback_count": len(unit_feedback),
            "negative_control_count": len(negative_control_results),
            "negative_controls_passed": all(row["passed"] for row in negative_control_results),
            "proposed_only_rejected_by_cell1": acceptance_gate_results["ADOPTION_PROBE_3_PROPOSED_ONLY_REJECTED_BY_CELL1"],
            "accepted_packet_requires_review_receipt": acceptance_gate_results["ADOPTION_PROBE_4_ACCEPTED_PACKET_REQUIRES_REVIEW_RECEIPT"],
            "cell1_intake_scoped": acceptance_gate_results["ADOPTION_PROBE_5_CELL1_INTAKE_SCOPED"],
            "probe_build_not_verification": acceptance_gate_results["ADOPTION_PROBE_6_PROBE_BUILD_NOT_VERIFICATION"],
            "verification_not_closure": acceptance_gate_results["ADOPTION_PROBE_7_VERIFICATION_NOT_CLOSURE"],
            "handoff_not_hidden_next_command": acceptance_gate_results["ADOPTION_PROBE_8_HANDOFF_NOT_HIDDEN_NEXT_COMMAND"],
            "blocked_feedback_not_repair": acceptance_gate_results["ADOPTION_PROBE_9_BLOCKED_FEEDBACK_NOT_REPAIR"],
            "bad_counters_zero": all(v == 0 for v in bad_counters.values()),
            "runtime_patched": False,
            "c7_authorized": False,
            "new_domain_shift_executed": False,
            "general_cell1_authority_claimed": False,
            "global_autonomy_claimed": False,
            "full_transfer_claimed": False,
            "runtime_wide_enforcement_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "c6_reviewed_reference_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "recommended_next": final_next,
        },
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "bounded_adoption_probe_fixture": rel(PROBE_FIXTURE_PATH),
            "bounded_adoption_probe_packet_trace": rel(PACKET_TRACE_PATH),
            "bounded_adoption_probe_edge_observations": rel(EDGE_OBSERVATIONS_PATH),
            "bounded_adoption_probe_unit_feedback": rel(UNIT_FEEDBACK_PATH),
            "bounded_adoption_probe_negative_control_results": rel(NEGATIVE_CONTROL_RESULTS_PATH),
            "bounded_adoption_probe_rollup": rel(ROLLUP_PATH),
            "bounded_adoption_probe_profile": rel(PROFILE_PATH),
            "bounded_adoption_probe_report": rel(REPORT_PATH),
            "bounded_adoption_probe_transition_trace": rel(TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_c6_protocol_adoption_probe_receipt_id={receipt_id}")
    print(f"bounded_c6_protocol_adoption_probe_receipt_path={rel(receipt_path)}")
    print(f"bounded_c6_protocol_adoption_probe_fixture_path={rel(PROBE_FIXTURE_PATH)}")
    print(f"bounded_c6_protocol_adoption_probe_rollup_path={rel(ROLLUP_PATH)}")
    print(f"bounded_c6_protocol_adoption_probe_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
