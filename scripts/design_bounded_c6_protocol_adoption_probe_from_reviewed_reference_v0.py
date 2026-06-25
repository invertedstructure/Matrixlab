#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DESIGN_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_FROM_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "c6.protocol_adoption_probe.design.v0"
LAYER = "BRIDGE / INTER_CELL_PROTOCOL / BOUNDED_ADOPTION_PROBE_DESIGN"
MODE = "DESIGN_ONLY / BOUNDED_PROBE_TARGET / NO_PROBE_EXECUTION / NO_RUNTIME_PATCH"
BUILD_MODE = "C6_BOUNDED_PROTOCOL_ADOPTION_PROBE_DESIGN_ONLY"

SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_ID = "5a07dcbb"
SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID = "50849d13"

SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0_receipts/5a07dcbb.json"

POST_C6_DECISION_BASIS_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0/post_c6_protocol_reference_decision_basis_v0.json"
POST_C6_DECISION_OPTIONS_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0/post_c6_protocol_reference_decision_options_v0.json"
POST_C6_SELECTED_BRANCH_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0/post_c6_protocol_reference_selected_branch_v0.json"
BOUNDED_ADOPTION_PROBE_TARGET_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0/c6_bounded_protocol_adoption_probe_target_v0.json"
C6_REFERENCE_PARK_RECORD_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0/c6_protocol_reference_park_record_v0.json"
POST_C6_DEFERRED_BRANCHES_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0/post_c6_protocol_reference_deferred_branches_v0.json"
POST_C6_AUTHORITY_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0/post_c6_protocol_reference_decision_authority_boundary_v0.json"
POST_C6_CLASSIFICATION_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0/post_c6_protocol_reference_decision_classification_v0.json"
POST_C6_ROLLUP_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0/post_c6_protocol_reference_decision_rollup_v0.json"
POST_C6_PROFILE_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0/post_c6_protocol_reference_decision_profile_v0.json"
POST_C6_REPORT_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0/post_c6_protocol_reference_decision_report.json"
POST_C6_TRACE_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0/post_c6_protocol_reference_decision_transition_trace.json"

SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0_receipts/50849d13.json"
C6_PROTOCOL_REVIEWED_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reviewed_reference_v0.json"
C6_PROTOCOL_FREEZE_MANIFEST_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reviewed_reference_freeze_manifest_v0.json"
C6_PACKET_LAW_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_packet_law_reference_v0.json"
C6_PROTOCOL_SURFACE_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_surface_reference_v0.json"
C6_GATE19_REPAIR_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_gate19_repair_reference_v0.json"

C6_PROTOCOL_SCHEMA_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_schema_v0.json"
C6_STATE_MACHINE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_packet_state_machine_v0.json"
C6_GATE_TABLE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_gate_table_v0.json"
C6_FORBIDDEN_TRANSITION_TABLE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_forbidden_transition_table_v0.json"
C6_DERIVATION_STATUS_RECORDS_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_derivation_status_records_v0.jsonl"
C6_PROTOCOL_READOUT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_readout_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH,
    POST_C6_DECISION_BASIS_PATH,
    POST_C6_DECISION_OPTIONS_PATH,
    POST_C6_SELECTED_BRANCH_PATH,
    BOUNDED_ADOPTION_PROBE_TARGET_PATH,
    C6_REFERENCE_PARK_RECORD_PATH,
    POST_C6_DEFERRED_BRANCHES_PATH,
    POST_C6_AUTHORITY_PATH,
    POST_C6_CLASSIFICATION_PATH,
    POST_C6_ROLLUP_PATH,
    POST_C6_PROFILE_PATH,
    POST_C6_REPORT_PATH,
    POST_C6_TRACE_PATH,
    SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH,
    C6_PROTOCOL_REVIEWED_REFERENCE_PATH,
    C6_PROTOCOL_FREEZE_MANIFEST_PATH,
    C6_PACKET_LAW_REFERENCE_PATH,
    C6_PROTOCOL_SURFACE_REFERENCE_PATH,
    C6_GATE19_REPAIR_REFERENCE_PATH,
    C6_PROTOCOL_SCHEMA_PATH,
    C6_STATE_MACHINE_PATH,
    C6_GATE_TABLE_PATH,
    C6_FORBIDDEN_TRANSITION_TABLE_PATH,
    C6_DERIVATION_STATUS_RECORDS_PATH,
    C6_PROTOCOL_READOUT_PATH,
]

OUT_DIR = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0"
RECEIPT_DIR = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0_receipts"

DESIGN_BASIS_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_design_basis_v0.json"
PROBE_SCOPE_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_scope_v0.json"
PROBE_FLOW_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_flow_v0.json"
PROBE_PACKET_FIXTURE_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_packet_fixture_v0.json"
PROBE_OBSERVATION_REQUIREMENTS_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_observation_requirements_v0.json"
PROBE_FEEDBACK_REQUIREMENTS_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_feedback_requirements_v0.json"
PROBE_ACCEPTANCE_GATES_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_acceptance_gates_v0.json"
PROBE_NEGATIVE_CONTROLS_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_negative_controls_v0.json"
PROBE_OUTPUT_MANIFEST_TARGET_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_output_manifest_target_v0.json"
PROBE_BUILD_CONTRACT_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_build_contract_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_design_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_design_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_design_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_design_profile_v0.json"
REPORT_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_design_report.json"
TRACE_PATH = OUT_DIR / "c6_bounded_protocol_adoption_probe_design_transition_trace.json"

EXPECTED_SOURCE_STATUS = "TYPED_POST_C6_PROTOCOL_REFERENCE_DECISION_SELECTED_BOUNDED_ADOPTION_PROBE_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_POST_C6_PROTOCOL_REFERENCE_DECISION_SELECTED_BOUNDED_ADOPTION_PROBE_READY"
EXPECTED_SOURCE_SELECTED_BRANCH = "DESIGN_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE"
EXPECTED_SOURCE_SELECTED_NEXT = "DESIGN_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_FROM_REVIEWED_REFERENCE_V0"

FUTURE_BUILD_UNIT = "BUILD_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_FROM_REVIEWED_REFERENCE_V0"

EXPECTED_PACKET_FAMILY = [
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

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    decision_receipt = read_json(SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH)
    decision_summary = decision_receipt.get("machine_readable_post_c6_protocol_reference_decision_summary", {})
    selected_branch = read_json(POST_C6_SELECTED_BRANCH_PATH)
    probe_target = read_json(BOUNDED_ADOPTION_PROBE_TARGET_PATH)
    reference_park = read_json(C6_REFERENCE_PARK_RECORD_PATH)
    deferred = read_json(POST_C6_DEFERRED_BRANCHES_PATH)
    authority = read_json(POST_C6_AUTHORITY_PATH)
    classification = read_json(POST_C6_CLASSIFICATION_PATH)
    rollup = read_json(POST_C6_ROLLUP_PATH)
    profile = read_json(POST_C6_PROFILE_PATH)
    report = read_json(POST_C6_REPORT_PATH)
    trace = read_json(POST_C6_TRACE_PATH)

    closure_receipt = read_json(SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH)
    reviewed_reference = read_json(C6_PROTOCOL_REVIEWED_REFERENCE_PATH)
    freeze_manifest = read_json(C6_PROTOCOL_FREEZE_MANIFEST_PATH)
    packet_law = read_json(C6_PACKET_LAW_REFERENCE_PATH)
    protocol_surface = read_json(C6_PROTOCOL_SURFACE_REFERENCE_PATH)
    gate19 = read_json(C6_GATE19_REPAIR_REFERENCE_PATH)

    protocol_schema = read_json(C6_PROTOCOL_SCHEMA_PATH)
    state_machine = read_json(C6_STATE_MACHINE_PATH)
    gate_table = read_json(C6_GATE_TABLE_PATH)
    forbidden_table = read_json(C6_FORBIDDEN_TRANSITION_TABLE_PATH)
    derivation_records = read_jsonl(C6_DERIVATION_STATUS_RECORDS_PATH)
    protocol_readout = read_json(C6_PROTOCOL_READOUT_PATH)

    if decision_receipt.get("receipt_id") != SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_ID or decision_receipt.get("gate") != "PASS":
        failures.append("source_post_c6_protocol_decision_receipt_not_pass")
    if decision_receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_stop_wrong")
    if decision_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_hidden_next")
    if decision_summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_wrong:{decision_summary.get('status')}")
    if decision_summary.get("selected_branch") != EXPECTED_SOURCE_SELECTED_BRANCH:
        failures.append("source_selected_branch_wrong")
    if decision_summary.get("selected_next_unit") != EXPECTED_SOURCE_SELECTED_NEXT:
        failures.append("source_selected_next_wrong")
    if decision_summary.get("recommended_next") != EXPECTED_SOURCE_SELECTED_NEXT:
        failures.append("source_recommended_next_wrong")

    for key in [
        "post_c6_protocol_reference_decision_complete",
        "bounded_adoption_probe_design_ready",
        "c6_reference_parked_available",
        "bad_counters_zero",
    ]:
        if decision_summary.get(key) is not True:
            failures.append(f"source_required_true_missing:{key}")

    for key in [
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
        if decision_summary.get(key) is not False:
            failures.append(f"source_forbidden_true:{key}")

    if selected_branch.get("selected_next_unit") != EXPECTED_SOURCE_SELECTED_NEXT:
        failures.append("selected_branch_next_wrong")
    if probe_target.get("target_unit") != EXPECTED_SOURCE_SELECTED_NEXT:
        failures.append("probe_target_unit_wrong")
    if "patch runtime" not in probe_target.get("probe_must_not_do", []):
        failures.append("probe_target_missing_no_runtime_patch")
    if "authorize C7" not in probe_target.get("probe_must_not_do", []):
        failures.append("probe_target_missing_no_c7")
    if reference_park.get("park_status") != "PARKED_AS_REVIEWED_REFERENCE_AVAILABLE_FOR_CONSUMPTION":
        failures.append("reference_park_status_wrong")
    for branch in ["OPEN_C7", "PATCH_RUNTIME_WITH_C6_PROTOCOL", "CLAIM_RUNTIME_WIDE_ENFORCEMENT"]:
        if branch not in deferred.get("deferred", []):
            failures.append(f"deferred_branch_missing:{branch}")
    if authority.get("may_design_bounded_c6_protocol_adoption_probe_next") is not True:
        failures.append("authority_no_design")
    for forbidden in [
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
    if rollup.get("bounded_adoption_probe_selected_count") != 1:
        failures.append("rollup_probe_selected_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_SOURCE_SELECTED_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next")

    if closure_receipt.get("receipt_id") != SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID or closure_receipt.get("gate") != "PASS":
        failures.append("closure_receipt_not_pass")
    if reviewed_reference.get("reference_status") != "C6_INTER_CELL_PROTOCOL_REVIEWED_REFERENCE_FROZEN":
        failures.append("reviewed_reference_not_frozen")
    if freeze_manifest.get("freeze_status") != "FROZEN":
        failures.append("freeze_manifest_not_frozen")
    if packet_law.get("packet_law_status") != "REVIEWED_REFERENCE":
        failures.append("packet_law_not_reference")
    if protocol_surface.get("surface_status") != "FROZEN_REVIEWED_REFERENCE":
        failures.append("protocol_surface_not_frozen")
    if gate19.get("repair_class") != "ASSERTION_REPAIR_NOT_PROTOCOL_REDESIGN":
        failures.append("gate19_repair_class_wrong")
    if protocol_schema.get("schema_claim") != "LOCAL_PROTOCOL_CANDIDATE_ONLY":
        failures.append("protocol_schema_claim_wrong")
    if protocol_schema.get("packet_family") != EXPECTED_PACKET_FAMILY:
        failures.append("protocol_packet_family_wrong")
    if len(state_machine.get("closed_states", [])) != 16:
        failures.append("state_machine_state_count_wrong")
    if len(gate_table.get("gates", [])) != 9:
        failures.append("gate_table_count_wrong")
    if len(forbidden_table.get("forbidden_transitions", [])) != 8:
        failures.append("forbidden_table_count_wrong")
    if len(derivation_records) != 14:
        failures.append("derivation_count_wrong")
    if "does not grant general Cell 1 authority" not in protocol_readout.get("interpretation", ""):
        failures.append("readout_boundary_missing")

    return failures, {
        "decision_summary": decision_summary,
        "probe_target": probe_target,
        "reviewed_reference": reviewed_reference,
        "packet_law": packet_law,
        "protocol_surface": protocol_surface,
        "protocol_schema": protocol_schema,
        "state_machine": state_machine,
        "gate_table": gate_table,
        "forbidden_table": forbidden_table,
        "derivation_records": derivation_records,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    design_pass = not failures
    status = "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_DESIGNED_BUILD_READY" if design_pass else "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_DESIGN_GATE_FAIL"
    recommended_next = FUTURE_BUILD_UNIT if design_pass else "REPAIR_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_DESIGN_V0"

    decision_summary = basis.get("decision_summary", {})
    probe_target = basis.get("probe_target", {})
    reviewed_reference = basis.get("reviewed_reference", {})
    packet_law = basis.get("packet_law", {})
    protocol_surface = basis.get("protocol_surface", {})
    protocol_schema = basis.get("protocol_schema", {})
    state_machine = basis.get("state_machine", {})
    gate_table = basis.get("gate_table", {})
    forbidden_table = basis.get("forbidden_table", {})
    derivation_records = basis.get("derivation_records", [])

    reason_codes = [
        "BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_DESIGNED",
        "POST_C6_PROTOCOL_REFERENCE_DECISION_RECEIPT_CONSUMED",
        "C6_REVIEWED_REFERENCE_CONSUMED",
        "C6_PACKET_LAW_REFERENCE_CONSUMED",
        "C6_PROTOCOL_SURFACE_REFERENCE_CONSUMED",
        "BOUNDED_FLOW_SELECTED",
        "PACKET_FIXTURE_DESIGNED",
        "OBSERVATION_REQUIREMENTS_DESIGNED",
        "UNIT_FEEDBACK_REQUIREMENTS_DESIGNED",
        "ACCEPTANCE_GATES_DESIGNED",
        "NEGATIVE_CONTROLS_DESIGNED",
        "BUILD_CONTRACT_EMITTED",
        "NO_PROBE_EXECUTION",
        "NO_RUNTIME_PATCH",
        "NO_C7_AUTHORIZATION",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if design_pass else failures

    design_basis = {
        "schema_version": "c6_bounded_protocol_adoption_probe_design_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if design_pass else "BASIS_REPAIR_REQUIRED",
        "source_post_c6_protocol_reference_decision_receipt_id": SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_ID,
        "source_c6_protocol_reference_closure_receipt_id": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "source_reference_status": reviewed_reference.get("reference_status"),
        "packet_law_status": packet_law.get("packet_law_status"),
        "protocol_surface_status": protocol_surface.get("surface_status"),
        "selected_decision_branch": decision_summary.get("selected_branch"),
        "target_unit": UNIT_ID,
        "future_build_unit": FUTURE_BUILD_UNIT,
    }

    probe_scope = {
        "schema_version": "c6_bounded_protocol_adoption_probe_scope_v0",
        "scope_status": "BOUNDED_SCOPE_DESIGNED" if design_pass else "NOT_READY",
        "scope_name": "single_reviewed_reference_to_cell1_intake_packet_flow",
        "allowed_object": "reviewed C6 local packet-law reference",
        "allowed_flow": "one synthetic/protocol-only inter-cell flow from proposed-only packet through accepted packet, Cell 1 intake, probe/build report, verification return, handoff, and sidecars",
        "allowed_actions": [
            "read frozen C6 reference",
            "instantiate demo packet fixture",
            "validate packet distinctions",
            "emit synthetic adoption-probe receipts",
            "emit edge observation sidecars",
            "emit unit feedback sidecars for blocked/failed/stop/NA cases",
        ],
        "forbidden_actions": [
            "patch runtime",
            "register protocol as runtime-wide enforcement",
            "authorize C7",
            "execute new domain shift",
            "mutate C6 reference",
            "grant general Cell 1 authority",
            "claim transfer",
            "claim autonomy",
        ],
    }

    probe_flow = {
        "schema_version": "c6_bounded_protocol_adoption_probe_flow_v0",
        "flow_status": "DESIGNED",
        "flow_steps": [
            {"step": 0, "packet": "PROPOSAL_PACKET_PROPOSED_ONLY", "expected": "not Cell 1 consumable", "next": "UNDER_REVIEW"},
            {"step": 1, "packet": "ACCEPTED_PROPOSAL_PACKET", "expected": "requires review receipt", "next": "CELL1_BUILDER_INTAKE_PACKET"},
            {"step": 2, "packet": "CELL1_BUILDER_INTAKE_PACKET", "expected": "scoped intake only", "next": "CELL1_PROBE_OR_BUILD_PACKET"},
            {"step": 3, "packet": "CELL1_PROBE_OR_BUILD_PACKET", "expected": "probe/build report, not verification", "next": "VERIFICATION_RETURN_PACKET"},
            {"step": 4, "packet": "VERIFICATION_RETURN_PACKET", "expected": "evidence return, not closure", "next": "HANDOFF_RETURN_PACKET"},
            {"step": 5, "packet": "HANDOFF_RETURN_PACKET", "expected": "control returned, no hidden next", "next": "terminal review handling"},
            {"step": 6, "packet": "BLOCKED_OR_TYPED_STOP_FEEDBACK_PACKET", "expected": "diagnostic feedback, not repair", "next": "review or Cell0 handling"},
            {"step": 7, "packet": "DECISION_EDGE_OBSERVATION_SIDECAR", "expected": "transition visible", "next": "sidecar only"},
            {"step": 8, "packet": "UNIT_FEEDBACK_SIDECAR", "expected": "failure/block/stop/NA feedback visible", "next": "sidecar only"},
        ],
        "critical_distinctions": packet_law.get("critical_distinctions", []),
    }

    probe_packet_fixture = {
        "schema_version": "c6_bounded_protocol_adoption_probe_packet_fixture_v0",
        "fixture_status": "DESIGNED_NOT_EXECUTED",
        "fixture_id": "c6_adoption_probe_fixture_" + sig8("single_reviewed_reference_to_cell1_intake_packet_flow"),
        "source_reference": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "packet_family": protocol_schema.get("packet_family", []),
        "synthetic_packets_required": [
            "proposed_only_packet",
            "accepted_proposal_packet",
            "cell1_builder_intake_packet",
            "cell1_probe_or_build_packet",
            "verification_return_packet",
            "handoff_return_packet",
            "blocked_feedback_packet",
            "edge_observation_sidecar",
            "unit_feedback_sidecar",
        ],
        "fixture_must_preserve": [
            "proposed-only is rejected by Cell 1",
            "accepted packet has review receipt",
            "Cell 1 intake remains scoped",
            "probe/build is not verification",
            "verification is not closure",
            "handoff is not hidden next command",
            "blocked feedback is not repair",
        ],
    }

    observation_requirements = {
        "schema_version": "c6_bounded_protocol_adoption_probe_observation_requirements_v0",
        "observation_status": "DESIGNED",
        "required_edge_observations": [
            "proposal_to_review",
            "review_to_accepted_packet",
            "accepted_packet_to_cell1_intake",
            "cell1_intake_to_probe_or_build",
            "probe_or_build_to_verification_return",
            "verification_return_to_handoff",
            "blocked_or_stop_to_feedback",
        ],
        "each_edge_observation_must_include": [
            "active_object",
            "attempted_move",
            "boundary_checked",
            "boundary_result",
            "blocked_moves",
            "lawful_next_moves",
            "source_packet_ref",
        ],
    }

    feedback_requirements = {
        "schema_version": "c6_bounded_protocol_adoption_probe_feedback_requirements_v0",
        "feedback_status": "DESIGNED",
        "unit_feedback_required_for": [
            "FAILED",
            "BLOCKED",
            "STOPPED",
            "NA",
        ],
        "unit_feedback_must_include": [
            "why_it_failed_or_blocked",
            "where_it_failed_or_blocked",
            "relative_object",
            "relative_source_surface",
            "relative_boundary",
            "missing_capability_or_discriminator",
            "exact_refinement_needed",
        ],
        "bare_failed_status_allowed": False,
    }

    acceptance_gates = {
        "schema_version": "c6_bounded_protocol_adoption_probe_acceptance_gates_v0",
        "acceptance_gates": [
            "ADOPTION_PROBE_0_C6_REVIEWED_REFERENCE_CONSUMED",
            "ADOPTION_PROBE_1_PACKET_LAW_REFERENCE_CONSUMED",
            "ADOPTION_PROBE_2_PROTOCOL_SURFACE_CONSUMED",
            "ADOPTION_PROBE_3_PROPOSED_ONLY_REJECTED_BY_CELL1",
            "ADOPTION_PROBE_4_ACCEPTED_PACKET_REQUIRES_REVIEW_RECEIPT",
            "ADOPTION_PROBE_5_CELL1_INTAKE_SCOPED",
            "ADOPTION_PROBE_6_PROBE_BUILD_NOT_VERIFICATION",
            "ADOPTION_PROBE_7_VERIFICATION_NOT_CLOSURE",
            "ADOPTION_PROBE_8_HANDOFF_NOT_HIDDEN_NEXT_COMMAND",
            "ADOPTION_PROBE_9_BLOCKED_FEEDBACK_NOT_REPAIR",
            "ADOPTION_PROBE_10_EDGE_OBSERVATION_SIDECARS_EMITTED",
            "ADOPTION_PROBE_11_UNIT_FEEDBACK_SIDECARS_EMITTED_FOR_FAILED_BLOCKED_STOPPED_NA",
            "ADOPTION_PROBE_12_BAD_COUNTERS_ZERO",
            "ADOPTION_PROBE_13_NO_RUNTIME_PATCH",
            "ADOPTION_PROBE_14_NO_C7_AUTHORIZATION",
            "ADOPTION_PROBE_15_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
            "ADOPTION_PROBE_16_NO_SOURCE_OR_REFERENCE_MUTATION",
            "ADOPTION_PROBE_17_NO_HIDDEN_NEXT_COMMAND",
        ],
    }

    negative_controls = {
        "schema_version": "c6_bounded_protocol_adoption_probe_negative_controls_v0",
        "negative_controls": [
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
        ],
    }

    output_manifest_target = {
        "schema_version": "c6_bounded_protocol_adoption_probe_output_manifest_target_v0",
        "required_outputs_for_future_build": [
            "bounded_adoption_probe_receipt",
            "bounded_adoption_probe_fixture",
            "bounded_adoption_probe_packet_trace",
            "bounded_adoption_probe_edge_observations",
            "bounded_adoption_probe_unit_feedback",
            "bounded_adoption_probe_negative_control_results",
            "bounded_adoption_probe_rollup",
            "bounded_adoption_probe_profile",
            "bounded_adoption_probe_report",
            "bounded_adoption_probe_transition_trace",
        ],
    }

    build_contract = {
        "schema_version": "c6_bounded_protocol_adoption_probe_build_contract_v0",
        "build_unit": FUTURE_BUILD_UNIT,
        "build_authorized_after_design": design_pass,
        "source_reference_receipt": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "source_decision_receipt": SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_ID,
        "must_consume": [
            rel(C6_PROTOCOL_REVIEWED_REFERENCE_PATH),
            rel(C6_PACKET_LAW_REFERENCE_PATH),
            rel(C6_PROTOCOL_SURFACE_REFERENCE_PATH),
            rel(C6_GATE19_REPAIR_REFERENCE_PATH),
            rel(C6_PROTOCOL_SCHEMA_PATH),
            rel(C6_STATE_MACHINE_PATH),
        ],
        "must_not_do": probe_scope["forbidden_actions"],
        "terminal_success": {
            "type": "STOP",
            "stop_code": "STOP_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_BUILT_REVIEW_READY",
            "next_command_goal": None,
        },
    }

    authority_boundary = {
        "schema_version": "c6_bounded_protocol_adoption_probe_design_authority_boundary_v0",
        "status": status,
        "may_build_bounded_adoption_probe_next": design_pass,
        "may_execute_probe_now_in_design": False,
        "may_patch_runtime_now": False,
        "may_open_c7_now": False,
        "may_execute_new_domain_shift": False,
        "may_claim_full_transfer": False,
        "may_claim_global_autonomy": False,
        "may_claim_general_cell1_authority": False,
        "may_claim_runtime_wide_enforcement": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_mutate_c6_reviewed_reference": False,
    }

    classification = {
        "schema_version": "c6_bounded_protocol_adoption_probe_design_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "bounded_c6_protocol_adoption_probe_designed": design_pass,
        "bounded_adoption_probe_build_ready": design_pass,
        "future_build_unit": recommended_next,
        "probe_executed_in_design": False,
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
        "bad_counters_zero": True,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "c6_bounded_protocol_adoption_probe_design_rollup_v0",
        "design_count": 1 if design_pass else 0,
        "build_ready_count": 1 if design_pass else 0,
        "probe_flow_steps": len(probe_flow["flow_steps"]),
        "synthetic_packets_required": len(probe_packet_fixture["synthetic_packets_required"]),
        "acceptance_gate_count": len(acceptance_gates["acceptance_gates"]),
        "negative_control_count": len(negative_controls["negative_controls"]),
        "edge_observation_requirement_count": len(observation_requirements["required_edge_observations"]),
        "unit_feedback_required_status_count": len(feedback_requirements["unit_feedback_required_for"]),
        "probe_executed_count": 0,
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
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "c6_bounded_protocol_adoption_probe_design_profile_v0",
        "profile_id": "c6_bounded_adoption_probe_design_" + sig8(rollup),
        "status": status,
        "design_object": "bounded adoption probe for reviewed C6 packet-law reference",
        "reference_compression": "Cells do not pass vibes. Cells pass packets.",
        "why_this_is_next": "C6 exists as reviewed reference; the smallest useful next edge is a bounded test of consumption, not runtime-wide adoption.",
        "must_not_infer": [
            "runtime patch",
            "C7 authorization",
            "global autonomy",
            "full transfer",
            "general Cell 1 authority",
            "runtime-wide enforcement",
        ],
        "bad_counters_zero": True,
        "next_command_goal": None,
    }

    report = {
        "schema_version": "c6_bounded_protocol_adoption_probe_design_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "A bounded adoption-probe design was emitted from the reviewed C6 packet-law reference. It specifies scope, packet flow, fixture, observation requirements, unit feedback requirements, acceptance gates, negative controls, output manifest, and future build contract. It does not execute the probe, patch runtime, authorize C7, or claim transfer/autonomy/general Cell 1 authority.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "c6_bounded_protocol_adoption_probe_design_transition_trace_v0",
        "trace": [
            {
                "step": "consume_post_c6_protocol_reference_decision",
                "question": "was bounded adoption-probe design selected",
                "answer": "yes" if design_pass else "no",
                "taken": "consume reviewed C6 reference and design bounded probe",
            },
            {
                "step": "design_bounded_probe",
                "question": "what is designed",
                "answer": "one synthetic bounded inter-cell packet-flow probe",
                "taken": "emit build-ready probe design contract",
            },
            {
                "step": "preserve_boundary",
                "question": "does design execute probe, patch runtime, authorize C7, or claim transfer/autonomy",
                "answer": "no",
                "taken": "stop with build-ready bounded probe design",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (DESIGN_BASIS_PATH, design_basis),
        (PROBE_SCOPE_PATH, probe_scope),
        (PROBE_FLOW_PATH, probe_flow),
        (PROBE_PACKET_FIXTURE_PATH, probe_packet_fixture),
        (PROBE_OBSERVATION_REQUIREMENTS_PATH, observation_requirements),
        (PROBE_FEEDBACK_REQUIREMENTS_PATH, feedback_requirements),
        (PROBE_ACCEPTANCE_GATES_PATH, acceptance_gates),
        (PROBE_NEGATIVE_CONTROLS_PATH, negative_controls),
        (PROBE_OUTPUT_MANIFEST_TARGET_PATH, output_manifest_target),
        (PROBE_BUILD_CONTRACT_PATH, build_contract),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, trace),
    ]

    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "C6_ADOPTION_PROBE_DESIGN_0_POST_C6_DECISION_RECEIPT_CONSUMED": SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH.exists(),
        "C6_ADOPTION_PROBE_DESIGN_1_C6_REVIEWED_REFERENCE_CONSUMED": reviewed_reference.get("reference_status") == "C6_INTER_CELL_PROTOCOL_REVIEWED_REFERENCE_FROZEN",
        "C6_ADOPTION_PROBE_DESIGN_2_PACKET_LAW_REFERENCE_CONSUMED": packet_law.get("packet_law_status") == "REVIEWED_REFERENCE",
        "C6_ADOPTION_PROBE_DESIGN_3_PROTOCOL_SURFACE_CONSUMED": protocol_surface.get("surface_status") == "FROZEN_REVIEWED_REFERENCE",
        "C6_ADOPTION_PROBE_DESIGN_4_SCOPE_EMITTED": PROBE_SCOPE_PATH.exists(),
        "C6_ADOPTION_PROBE_DESIGN_5_PACKET_FLOW_EMITTED": PROBE_FLOW_PATH.exists() and len(probe_flow["flow_steps"]) == 9,
        "C6_ADOPTION_PROBE_DESIGN_6_PACKET_FIXTURE_EMITTED": PROBE_PACKET_FIXTURE_PATH.exists() and len(probe_packet_fixture["synthetic_packets_required"]) == 9,
        "C6_ADOPTION_PROBE_DESIGN_7_OBSERVATION_REQUIREMENTS_EMITTED": PROBE_OBSERVATION_REQUIREMENTS_PATH.exists(),
        "C6_ADOPTION_PROBE_DESIGN_8_FEEDBACK_REQUIREMENTS_EMITTED": PROBE_FEEDBACK_REQUIREMENTS_PATH.exists(),
        "C6_ADOPTION_PROBE_DESIGN_9_ACCEPTANCE_GATES_EMITTED": PROBE_ACCEPTANCE_GATES_PATH.exists() and len(acceptance_gates["acceptance_gates"]) == 18,
        "C6_ADOPTION_PROBE_DESIGN_10_NEGATIVE_CONTROLS_EMITTED": PROBE_NEGATIVE_CONTROLS_PATH.exists() and len(negative_controls["negative_controls"]) == 15,
        "C6_ADOPTION_PROBE_DESIGN_11_OUTPUT_MANIFEST_TARGET_EMITTED": PROBE_OUTPUT_MANIFEST_TARGET_PATH.exists(),
        "C6_ADOPTION_PROBE_DESIGN_12_BUILD_CONTRACT_EMITTED": PROBE_BUILD_CONTRACT_PATH.exists() and build_contract["build_unit"] == FUTURE_BUILD_UNIT,
        "C6_ADOPTION_PROBE_DESIGN_13_NO_PROBE_EXECUTION": classification["probe_executed_in_design"] is False,
        "C6_ADOPTION_PROBE_DESIGN_14_NO_RUNTIME_PATCH_OR_C7": classification["runtime_patched"] is False and classification["c7_authorized"] is False,
        "C6_ADOPTION_PROBE_DESIGN_15_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "C6_ADOPTION_PROBE_DESIGN_16_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["c6_reviewed_reference_mutated"] is False,
        "C6_ADOPTION_PROBE_DESIGN_17_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "C6_ADOPTION_PROBE_DESIGN_18_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C6_ADOPTION_PROBE_DESIGN_19_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "C6_ADOPTION_PROBE_DESIGN_20_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_DESIGN_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_DESIGN_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_DESIGN_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_decision": SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_ID,
        "future_build": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c6_bounded_protocol_adoption_probe_design_receipt_v0",
        "receipt_type": "TYPED_C6_BOUNDED_PROTOCOL_ADOPTION_PROBE_DESIGN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_post_c6_protocol_reference_decision_receipt_id": SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_ID,
        "source_c6_protocol_reference_closure_receipt_id": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_c6_bounded_adoption_probe_design_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "bounded_c6_protocol_adoption_probe_designed": gate == "PASS",
            "bounded_adoption_probe_build_ready": gate == "PASS",
            "future_build_unit": final_next,
            "source_reference_status": reviewed_reference.get("reference_status"),
            "probe_flow_steps": len(probe_flow["flow_steps"]),
            "synthetic_packets_required": len(probe_packet_fixture["synthetic_packets_required"]),
            "acceptance_gates_declared": len(acceptance_gates["acceptance_gates"]),
            "negative_controls_declared": len(negative_controls["negative_controls"]),
            "edge_observation_requirements_declared": len(observation_requirements["required_edge_observations"]),
            "unit_feedback_requirements_declared": len(feedback_requirements["unit_feedback_required_for"]),
            "probe_executed_in_design": False,
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
            "bad_counters_zero": True,
            "recommended_next": final_next,
        },
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "design_basis": rel(DESIGN_BASIS_PATH),
            "probe_scope": rel(PROBE_SCOPE_PATH),
            "probe_flow": rel(PROBE_FLOW_PATH),
            "probe_packet_fixture": rel(PROBE_PACKET_FIXTURE_PATH),
            "observation_requirements": rel(PROBE_OBSERVATION_REQUIREMENTS_PATH),
            "feedback_requirements": rel(PROBE_FEEDBACK_REQUIREMENTS_PATH),
            "acceptance_gates": rel(PROBE_ACCEPTANCE_GATES_PATH),
            "negative_controls": rel(PROBE_NEGATIVE_CONTROLS_PATH),
            "output_manifest_target": rel(PROBE_OUTPUT_MANIFEST_TARGET_PATH),
            "build_contract": rel(PROBE_BUILD_CONTRACT_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_c6_protocol_adoption_probe_design_receipt_id={receipt_id}")
    print(f"bounded_c6_protocol_adoption_probe_design_receipt_path={rel(receipt_path)}")
    print(f"bounded_c6_protocol_adoption_probe_scope_path={rel(PROBE_SCOPE_PATH)}")
    print(f"bounded_c6_protocol_adoption_probe_build_contract_path={rel(PROBE_BUILD_CONTRACT_PATH)}")
    print(f"bounded_c6_protocol_adoption_probe_design_rollup_path={rel(ROLLUP_PATH)}")
    print(f"bounded_c6_protocol_adoption_probe_design_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
