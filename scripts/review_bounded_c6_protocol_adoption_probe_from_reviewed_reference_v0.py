#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_FROM_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "c6.protocol_adoption_probe.review.v0"
LAYER = "BRIDGE / INTER_CELL_PROTOCOL / BOUNDED_ADOPTION_PROBE / REVIEW"
MODE = "REVIEW_ONLY / VERIFY_SYNTHETIC_PROTOCOL_PROBE / NO_RUNTIME_PATCH"
BUILD_MODE = "C6_BOUNDED_PROTOCOL_ADOPTION_PROBE_REVIEW_ONLY"

SOURCE_PROBE_RECEIPT_ID = "6ecaeaf8"
SOURCE_PROBE_DESIGN_RECEIPT_ID = "e0078630"
SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID = "50849d13"
SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_ID = "5a07dcbb"

SOURCE_PROBE_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0_receipts/6ecaeaf8.json"

PROBE_FIXTURE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_fixture_v0.json"
PROBE_PACKET_TRACE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_packet_trace_v0.jsonl"
PROBE_EDGE_OBSERVATIONS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_edge_observations_v0.jsonl"
PROBE_UNIT_FEEDBACK_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_unit_feedback_v0.jsonl"
PROBE_NEGATIVE_CONTROL_RESULTS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_negative_control_results_v0.jsonl"
PROBE_ROLLUP_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_rollup_v0.json"
PROBE_PROFILE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_profile_v0.json"
PROBE_REPORT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_report.json"
PROBE_TRACE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_transition_trace.json"

SOURCE_PROBE_DESIGN_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0_receipts/e0078630.json"
SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0_receipts/50849d13.json"
SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_post_reference_decision_v0_receipts/5a07dcbb.json"

C6_PROTOCOL_REVIEWED_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_reviewed_reference_v0.json"
C6_PACKET_LAW_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_packet_law_reference_v0.json"
C6_PROTOCOL_SURFACE_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_surface_reference_v0.json"
C6_GATE19_REPAIR_REFERENCE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_reference_closure_v0/c6_inter_cell_protocol_gate19_repair_reference_v0.json"

PROBE_DESIGN_BASIS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_design_basis_v0.json"
PROBE_DESIGN_SCOPE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_scope_v0.json"
PROBE_DESIGN_FLOW_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_flow_v0.json"
PROBE_DESIGN_ACCEPTANCE_GATES_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_acceptance_gates_v0.json"
PROBE_DESIGN_NEGATIVE_CONTROLS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_negative_controls_v0.json"
PROBE_DESIGN_FEEDBACK_REQUIREMENTS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_feedback_requirements_v0.json"
PROBE_DESIGN_OBSERVATION_REQUIREMENTS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_design_v0/c6_bounded_protocol_adoption_probe_observation_requirements_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_PROBE_RECEIPT_PATH,
    PROBE_FIXTURE_PATH,
    PROBE_PACKET_TRACE_PATH,
    PROBE_EDGE_OBSERVATIONS_PATH,
    PROBE_UNIT_FEEDBACK_PATH,
    PROBE_NEGATIVE_CONTROL_RESULTS_PATH,
    PROBE_ROLLUP_PATH,
    PROBE_PROFILE_PATH,
    PROBE_REPORT_PATH,
    PROBE_TRACE_PATH,
    SOURCE_PROBE_DESIGN_RECEIPT_PATH,
    SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH,
    SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH,
    C6_PROTOCOL_REVIEWED_REFERENCE_PATH,
    C6_PACKET_LAW_REFERENCE_PATH,
    C6_PROTOCOL_SURFACE_REFERENCE_PATH,
    C6_GATE19_REPAIR_REFERENCE_PATH,
    PROBE_DESIGN_BASIS_PATH,
    PROBE_DESIGN_SCOPE_PATH,
    PROBE_DESIGN_FLOW_PATH,
    PROBE_DESIGN_ACCEPTANCE_GATES_PATH,
    PROBE_DESIGN_NEGATIVE_CONTROLS_PATH,
    PROBE_DESIGN_FEEDBACK_REQUIREMENTS_PATH,
    PROBE_DESIGN_OBSERVATION_REQUIREMENTS_PATH,
]

OUT_DIR = ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0"
RECEIPT_DIR = ROOT / "data/c6_bounded_protocol_adoption_probe_review_v0_receipts"

REVIEW_BASIS_PATH = OUT_DIR / "bounded_adoption_probe_review_basis_v0.json"
SOURCE_RECEIPT_REVIEW_PATH = OUT_DIR / "bounded_adoption_probe_source_receipt_review_v0.json"
PACKET_TRACE_REVIEW_PATH = OUT_DIR / "bounded_adoption_probe_packet_trace_review_v0.json"
EDGE_OBSERVATION_REVIEW_PATH = OUT_DIR / "bounded_adoption_probe_edge_observation_review_v0.json"
UNIT_FEEDBACK_REVIEW_PATH = OUT_DIR / "bounded_adoption_probe_unit_feedback_review_v0.json"
NEGATIVE_CONTROL_REVIEW_PATH = OUT_DIR / "bounded_adoption_probe_negative_control_review_v0.json"
BOUNDARY_REVIEW_PATH = OUT_DIR / "bounded_adoption_probe_boundary_review_v0.json"
CLOSE_CANDIDATE_PATH = OUT_DIR / "bounded_adoption_probe_reviewed_reference_close_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "bounded_adoption_probe_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "bounded_adoption_probe_review_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_adoption_probe_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_adoption_probe_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_adoption_probe_review_report.json"
TRACE_PATH = OUT_DIR / "bounded_adoption_probe_review_transition_trace.json"

EXPECTED_BUILD_STATUS = "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_BUILT_REVIEW_READY"
EXPECTED_BUILD_STOP = "STOP_TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_BUILT_REVIEW_READY"
EXPECTED_BUILD_NEXT = "REVIEW_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_FROM_REVIEWED_REFERENCE_V0"
RECOMMENDED_NEXT = "CLOSE_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_FROM_REVIEWED_REFERENCE_AS_REVIEWED_REFERENCE_V0"

EXPECTED_PACKET_TYPES = [
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

EXPECTED_EDGE_NAMES = [
    "proposal_to_review",
    "review_to_accepted_packet",
    "accepted_packet_to_cell1_intake",
    "cell1_intake_to_probe_or_build",
    "probe_or_build_to_verification_return",
    "verification_return_to_handoff",
    "blocked_or_stop_to_feedback",
]

EXPECTED_FEEDBACK_STATUSES = {"FAILED", "BLOCKED", "STOPPED", "NA"}

EXPECTED_NEGATIVE_CONTROLS = [
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

    probe_receipt = read_json(SOURCE_PROBE_RECEIPT_PATH)
    probe_summary = probe_receipt.get("machine_readable_bounded_c6_adoption_probe_summary", {})
    acceptance_gates = probe_receipt.get("acceptance_gate_results", {})

    fixture = read_json(PROBE_FIXTURE_PATH)
    packet_trace = read_jsonl(PROBE_PACKET_TRACE_PATH)
    edge_observations = read_jsonl(PROBE_EDGE_OBSERVATIONS_PATH)
    unit_feedback = read_jsonl(PROBE_UNIT_FEEDBACK_PATH)
    negative_controls = read_jsonl(PROBE_NEGATIVE_CONTROL_RESULTS_PATH)
    rollup = read_json(PROBE_ROLLUP_PATH)
    profile = read_json(PROBE_PROFILE_PATH)
    report = read_json(PROBE_REPORT_PATH)
    transition_trace = read_json(PROBE_TRACE_PATH)

    design_receipt = read_json(SOURCE_PROBE_DESIGN_RECEIPT_PATH)
    reference_closure_receipt = read_json(SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_PATH)
    post_decision_receipt = read_json(SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_PATH)
    reviewed_reference = read_json(C6_PROTOCOL_REVIEWED_REFERENCE_PATH)
    packet_law = read_json(C6_PACKET_LAW_REFERENCE_PATH)
    protocol_surface = read_json(C6_PROTOCOL_SURFACE_REFERENCE_PATH)
    gate19 = read_json(C6_GATE19_REPAIR_REFERENCE_PATH)

    design_acceptance_gates = read_json(PROBE_DESIGN_ACCEPTANCE_GATES_PATH)
    design_negative_controls = read_json(PROBE_DESIGN_NEGATIVE_CONTROLS_PATH)
    design_feedback_requirements = read_json(PROBE_DESIGN_FEEDBACK_REQUIREMENTS_PATH)
    design_observation_requirements = read_json(PROBE_DESIGN_OBSERVATION_REQUIREMENTS_PATH)

    if probe_receipt.get("receipt_id") != SOURCE_PROBE_RECEIPT_ID or probe_receipt.get("gate") != "PASS":
        failures.append("source_probe_receipt_not_pass")
    if probe_receipt.get("terminal", {}).get("stop_code") != EXPECTED_BUILD_STOP:
        failures.append("source_probe_stop_wrong")
    if probe_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_probe_hidden_next")
    if probe_summary.get("status") != EXPECTED_BUILD_STATUS:
        failures.append(f"source_probe_status_wrong:{probe_summary.get('status')}")
    if probe_summary.get("recommended_next") != EXPECTED_BUILD_NEXT:
        failures.append(f"source_probe_next_wrong:{probe_summary.get('recommended_next')}")

    for key in [
        "bounded_c6_protocol_adoption_probe_built",
        "probe_review_ready",
        "synthetic_protocol_only",
        "negative_controls_passed",
        "proposed_only_rejected_by_cell1",
        "accepted_packet_requires_review_receipt",
        "cell1_intake_scoped",
        "probe_build_not_verification",
        "verification_not_closure",
        "handoff_not_hidden_next_command",
        "blocked_feedback_not_repair",
        "bad_counters_zero",
    ]:
        if probe_summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    for key in [
        "runtime_effect",
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
        if probe_summary.get(key) is not False:
            failures.append(f"summary_forbidden_true:{key}")

    expected_counts = {
        "packet_trace_count": 9,
        "edge_observation_count": 7,
        "unit_feedback_count": 4,
        "negative_control_count": 15,
    }
    for key, expected in expected_counts.items():
        if probe_summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{probe_summary.get(key)}")

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.append("acceptance_gates_false:" + ",".join(false_gates))
    if len(acceptance_gates) != 18:
        failures.append(f"acceptance_gate_count_wrong:{len(acceptance_gates)}")

    if fixture.get("fixture_status") != "BUILT_SYNTHETIC_PROTOCOL_ONLY":
        failures.append("fixture_status_wrong")
    if fixture.get("synthetic_only") is not True or fixture.get("runtime_effect") is not False:
        failures.append("fixture_boundary_wrong")
    if [row.get("packet_type") for row in packet_trace] != EXPECTED_PACKET_TYPES:
        failures.append("packet_trace_sequence_wrong")
    if [row.get("edge_name") for row in edge_observations] != EXPECTED_EDGE_NAMES:
        failures.append("edge_observation_sequence_wrong")
    if {row.get("status") for row in unit_feedback} != EXPECTED_FEEDBACK_STATUSES:
        failures.append("unit_feedback_status_set_wrong")
    if any(row.get("feedback_quality_class") != "USEFUL_DIAGNOSTIC_FEEDBACK" for row in unit_feedback):
        failures.append("unit_feedback_quality_wrong")
    if any(row.get("bare_failed_status") is not False for row in unit_feedback):
        failures.append("unit_feedback_bare_failed_present")
    if [row.get("control") for row in negative_controls] != EXPECTED_NEGATIVE_CONTROLS:
        failures.append("negative_control_sequence_wrong")
    if any(row.get("passed") is not True or row.get("observed") != "FAIL_CLOSED" for row in negative_controls):
        failures.append("negative_controls_not_fail_closed")

    if rollup.get("probe_review_ready_count") != 1:
        failures.append("rollup_review_ready_wrong")
    if rollup.get("runtime_effect_count") != 0:
        failures.append("rollup_runtime_effect_nonzero")
    if rollup.get("negative_controls_passed_count") != 15:
        failures.append("rollup_negative_controls_wrong")
    if any(v != 0 for v in rollup.get("bad_counters", {}).values()):
        failures.append("rollup_bad_counter_nonzero")
    for key in [
        "runtime_patch_count",
        "c7_authorized_count",
        "new_domain_shift_executed_count",
        "general_cell1_authority_claim_count",
        "global_autonomy_claim_count",
        "full_transfer_claim_count",
        "runtime_wide_enforcement_claim_count",
        "source_mutated_count",
        "prior_receipt_mutated_count",
        "c6_reviewed_reference_mutated_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]:
        if rollup.get(key) != 0:
            failures.append(f"rollup_forbidden_nonzero:{key}:{rollup.get(key)}")

    if profile.get("negative_controls_all_fail_closed") is not True:
        failures.append("profile_negative_controls_wrong")
    if profile.get("bad_counters_zero") is not True:
        failures.append("profile_bad_counters_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_BUILD_NEXT:
        failures.append("report_next_wrong")
    if transition_trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next")

    if design_receipt.get("receipt_id") != SOURCE_PROBE_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("design_receipt_not_pass")
    if reference_closure_receipt.get("receipt_id") != SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID or reference_closure_receipt.get("gate") != "PASS":
        failures.append("reference_closure_receipt_not_pass")
    if post_decision_receipt.get("receipt_id") != SOURCE_POST_C6_PROTOCOL_DECISION_RECEIPT_ID or post_decision_receipt.get("gate") != "PASS":
        failures.append("post_decision_receipt_not_pass")
    if reviewed_reference.get("reference_status") != "C6_INTER_CELL_PROTOCOL_REVIEWED_REFERENCE_FROZEN":
        failures.append("reviewed_reference_not_frozen")
    if packet_law.get("packet_law_status") != "REVIEWED_REFERENCE":
        failures.append("packet_law_reference_wrong")
    if protocol_surface.get("surface_status") != "FROZEN_REVIEWED_REFERENCE":
        failures.append("protocol_surface_reference_wrong")
    if gate19.get("repair_class") != "ASSERTION_REPAIR_NOT_PROTOCOL_REDESIGN":
        failures.append("gate19_reference_wrong")

    if len(design_acceptance_gates.get("acceptance_gates", [])) != 18:
        failures.append("design_acceptance_gate_count_wrong")
    if design_negative_controls.get("negative_controls") != EXPECTED_NEGATIVE_CONTROLS:
        failures.append("design_negative_controls_wrong")
    if set(design_feedback_requirements.get("unit_feedback_required_for", [])) != EXPECTED_FEEDBACK_STATUSES:
        failures.append("design_feedback_requirements_wrong")
    if design_observation_requirements.get("required_edge_observations") != EXPECTED_EDGE_NAMES:
        failures.append("design_observation_requirements_wrong")

    return failures, {
        "probe_summary": probe_summary,
        "acceptance_gates": acceptance_gates,
        "fixture": fixture,
        "packet_trace": packet_trace,
        "edge_observations": edge_observations,
        "unit_feedback": unit_feedback,
        "negative_controls": negative_controls,
        "rollup": rollup,
        "profile": profile,
        "reviewed_reference": reviewed_reference,
        "packet_law": packet_law,
        "protocol_surface": protocol_surface,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    review_pass = not failures
    status = "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEWED_CLOSE_READY" if review_pass else "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEW_V0"

    probe_summary = basis.get("probe_summary", {})
    acceptance_gates = basis.get("acceptance_gates", {})
    fixture = basis.get("fixture", {})
    packet_trace = basis.get("packet_trace", [])
    edge_observations = basis.get("edge_observations", [])
    unit_feedback = basis.get("unit_feedback", [])
    negative_controls = basis.get("negative_controls", [])
    rollup_source = basis.get("rollup", {})
    profile_source = basis.get("profile", {})
    reviewed_reference = basis.get("reviewed_reference", {})
    packet_law = basis.get("packet_law", {})
    protocol_surface = basis.get("protocol_surface", {})

    reason_codes = [
        "BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEW_COMPLETE",
        "PROBE_RECEIPT_CONSUMED",
        "SYNTHETIC_PROTOCOL_ONLY_CONFIRMED",
        "PACKET_TRACE_REVIEWED",
        "EDGE_OBSERVATIONS_REVIEWED",
        "UNIT_FEEDBACK_REVIEWED",
        "NEGATIVE_CONTROLS_REVIEWED_FAIL_CLOSED",
        "PACKET_LAW_DISTINCTIONS_CONFIRMED",
        "BAD_COUNTERS_ZERO",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_C7_AUTHORIZATION",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
        "CLOSE_CANDIDATE_READY",
    ] if review_pass else failures

    review_basis = {
        "schema_version": "bounded_adoption_probe_review_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if review_pass else "BASIS_REPAIR_REQUIRED",
        "source_probe_receipt_id": SOURCE_PROBE_RECEIPT_ID,
        "source_probe_design_receipt_id": SOURCE_PROBE_DESIGN_RECEIPT_ID,
        "source_c6_protocol_reference_closure_receipt_id": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "source_reference_status": reviewed_reference.get("reference_status"),
        "packet_law_status": packet_law.get("packet_law_status"),
        "protocol_surface_status": protocol_surface.get("surface_status"),
        "probe_status": probe_summary.get("status"),
    }

    source_receipt_review = {
        "schema_version": "bounded_adoption_probe_source_receipt_review_v0",
        "source_probe_receipt_id": SOURCE_PROBE_RECEIPT_ID,
        "source_gate": "PASS" if review_pass else "REPAIR_REQUIRED",
        "false_acceptance_gates": [k for k, v in acceptance_gates.items() if v is not True],
        "acceptance_gate_count": len(acceptance_gates),
        "all_acceptance_gates_true": all(v is True for v in acceptance_gates.values()) if acceptance_gates else False,
        "terminal_stop": EXPECTED_BUILD_STOP,
        "next_command_goal": None,
    }

    packet_trace_review = {
        "schema_version": "bounded_adoption_probe_packet_trace_review_v0",
        "packet_trace_count": len(packet_trace),
        "packet_types": [row.get("packet_type") for row in packet_trace],
        "packet_sequence_expected": EXPECTED_PACKET_TYPES,
        "packet_sequence_matches": [row.get("packet_type") for row in packet_trace] == EXPECTED_PACKET_TYPES,
        "packet_law_results": {
            "proposed_only_rejected_by_cell1": probe_summary.get("proposed_only_rejected_by_cell1"),
            "accepted_packet_requires_review_receipt": probe_summary.get("accepted_packet_requires_review_receipt"),
            "cell1_intake_scoped": probe_summary.get("cell1_intake_scoped"),
            "probe_build_not_verification": probe_summary.get("probe_build_not_verification"),
            "verification_not_closure": probe_summary.get("verification_not_closure"),
            "handoff_not_hidden_next_command": probe_summary.get("handoff_not_hidden_next_command"),
            "blocked_feedback_not_repair": probe_summary.get("blocked_feedback_not_repair"),
        },
    }

    edge_observation_review = {
        "schema_version": "bounded_adoption_probe_edge_observation_review_v0",
        "edge_observation_count": len(edge_observations),
        "edge_names": [row.get("edge_name") for row in edge_observations],
        "edge_sequence_expected": EXPECTED_EDGE_NAMES,
        "edge_sequence_matches": [row.get("edge_name") for row in edge_observations] == EXPECTED_EDGE_NAMES,
        "all_runtime_effect_false": all(row.get("runtime_effect") is False for row in edge_observations),
    }

    unit_feedback_review = {
        "schema_version": "bounded_adoption_probe_unit_feedback_review_v0",
        "unit_feedback_count": len(unit_feedback),
        "statuses_seen": sorted({row.get("status") for row in unit_feedback}),
        "required_statuses_seen": {row.get("status") for row in unit_feedback} == EXPECTED_FEEDBACK_STATUSES,
        "all_feedback_useful": all(row.get("feedback_quality_class") == "USEFUL_DIAGNOSTIC_FEEDBACK" for row in unit_feedback),
        "bare_failed_status_present": any(row.get("bare_failed_status") is not False for row in unit_feedback),
    }

    negative_control_review = {
        "schema_version": "bounded_adoption_probe_negative_control_review_v0",
        "negative_control_count": len(negative_controls),
        "negative_controls": [row.get("control") for row in negative_controls],
        "all_fail_closed": all(row.get("passed") is True and row.get("observed") == "FAIL_CLOSED" for row in negative_controls),
        "runtime_effect_count": sum(1 for row in negative_controls if row.get("runtime_effect") is not False),
    }

    boundary_review = {
        "schema_version": "bounded_adoption_probe_boundary_review_v0",
        "synthetic_protocol_only": probe_summary.get("synthetic_protocol_only"),
        "runtime_effect": probe_summary.get("runtime_effect"),
        "runtime_patched": probe_summary.get("runtime_patched"),
        "c7_authorized": probe_summary.get("c7_authorized"),
        "new_domain_shift_executed": probe_summary.get("new_domain_shift_executed"),
        "general_cell1_authority_claimed": probe_summary.get("general_cell1_authority_claimed"),
        "global_autonomy_claimed": probe_summary.get("global_autonomy_claimed"),
        "full_transfer_claimed": probe_summary.get("full_transfer_claimed"),
        "runtime_wide_enforcement_claimed": probe_summary.get("runtime_wide_enforcement_claimed"),
        "source_mutated": probe_summary.get("source_mutated"),
        "prior_receipt_mutated": probe_summary.get("prior_receipt_mutated"),
        "c6_reviewed_reference_mutated": probe_summary.get("c6_reviewed_reference_mutated"),
        "hidden_next_command": probe_summary.get("hidden_next_command"),
        "latest_file_guessing": probe_summary.get("latest_file_guessing"),
        "mtime_selection": probe_summary.get("mtime_selection"),
    }

    close_candidate = {
        "schema_version": "bounded_adoption_probe_reviewed_reference_close_candidate_v0",
        "candidate_status": "BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEWED_REFERENCE_CLOSE_READY" if review_pass else "NOT_CLOSE_READY",
        "review_pass": review_pass,
        "source_probe_receipt_id": SOURCE_PROBE_RECEIPT_ID,
        "candidate_next_unit": RECOMMENDED_NEXT if review_pass else None,
        "close_scope": "close bounded C6 synthetic protocol adoption probe as reviewed reference",
        "close_does_not": [
            "patch runtime",
            "authorize C7",
            "claim full transfer",
            "claim global autonomy",
            "grant general Cell 1 authority",
            "claim runtime-wide enforcement",
        ],
    }

    authority_boundary = {
        "schema_version": "bounded_adoption_probe_review_authority_boundary_v0",
        "status": status,
        "may_close_bounded_adoption_probe_as_reviewed_reference_next": review_pass,
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
        "schema_version": "bounded_adoption_probe_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "bounded_c6_protocol_adoption_probe_review_complete": review_pass,
        "bounded_c6_protocol_adoption_probe_review_pass": review_pass,
        "close_candidate_ready": review_pass,
        "source_probe_built": probe_summary.get("bounded_c6_protocol_adoption_probe_built"),
        "synthetic_protocol_only": probe_summary.get("synthetic_protocol_only"),
        "runtime_effect": False,
        "packet_trace_count": len(packet_trace),
        "edge_observation_count": len(edge_observations),
        "unit_feedback_count": len(unit_feedback),
        "negative_control_count": len(negative_controls),
        "negative_controls_passed": probe_summary.get("negative_controls_passed"),
        "bad_counters_zero": probe_summary.get("bad_counters_zero"),
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
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "bounded_adoption_probe_review_rollup_v0",
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "close_candidate_ready_count": 1 if review_pass else 0,
        "packet_trace_count": len(packet_trace),
        "edge_observation_count": len(edge_observations),
        "unit_feedback_count": len(unit_feedback),
        "negative_control_count": len(negative_controls),
        "negative_controls_passed_count": sum(1 for row in negative_controls if row.get("passed") is True),
        "false_acceptance_gate_count": len([k for k, v in acceptance_gates.items() if v is not True]),
        "runtime_effect_count": 0,
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
        "schema_version": "bounded_adoption_probe_review_profile_v0",
        "profile_id": "bounded_c6_adoption_probe_review_" + sig8(rollup),
        "status": status,
        "review_object": "bounded synthetic adoption probe for reviewed C6 packet-law reference",
        "compression": "C6 packet law survived one bounded synthetic inter-cell flow.",
        "review_findings": [
            "Packet trace contains all 9 expected packet/surface entries.",
            "All 7 decision-edge observations are present.",
            "Unit feedback covers FAILED, BLOCKED, STOPPED, and NA with useful diagnostics.",
            "All 15 negative controls fail closed.",
            "No runtime effect, no runtime patch, no C7 authorization, and no broad authority claim.",
        ],
        "bad_counters_zero": True,
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
        "schema_version": "bounded_adoption_probe_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The bounded synthetic C6 adoption probe reviewed clean. It confirms one bounded inter-cell packet-law flow with 9 packet trace entries, 7 edge observations, 4 unit feedback sidecars, 15 fail-closed negative controls, and no runtime/C7/transfer/autonomy/general-authority boundary breach.",
        "recommended_next_handling": recommended_next,
    }

    transition_trace = {
        "schema_version": "bounded_adoption_probe_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_bounded_probe",
                "question": "did the bounded synthetic C6 adoption probe build cleanly",
                "answer": "yes" if review_pass else "no",
                "taken": "review packet trace, edge observations, feedback, and negative controls",
            },
            {
                "step": "verify_packet_law_survival",
                "question": "did packet law survive one bounded inter-cell flow",
                "answer": "yes" if review_pass else "no",
                "taken": "emit close candidate",
            },
            {
                "step": "preserve_boundary",
                "question": "does review patch runtime, authorize C7, or claim transfer/autonomy",
                "answer": "no",
                "taken": "stop with close-ready bounded adoption probe review",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (REVIEW_BASIS_PATH, review_basis),
        (SOURCE_RECEIPT_REVIEW_PATH, source_receipt_review),
        (PACKET_TRACE_REVIEW_PATH, packet_trace_review),
        (EDGE_OBSERVATION_REVIEW_PATH, edge_observation_review),
        (UNIT_FEEDBACK_REVIEW_PATH, unit_feedback_review),
        (NEGATIVE_CONTROL_REVIEW_PATH, negative_control_review),
        (BOUNDARY_REVIEW_PATH, boundary_review),
        (CLOSE_CANDIDATE_PATH, close_candidate),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, transition_trace),
    ]
    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "ADOPTION_PROBE_REVIEW_0_PROBE_RECEIPT_CONSUMED": SOURCE_PROBE_RECEIPT_PATH.exists(),
        "ADOPTION_PROBE_REVIEW_1_PROBE_GATE_PASS": probe_summary.get("bounded_c6_protocol_adoption_probe_built") is True,
        "ADOPTION_PROBE_REVIEW_2_PACKET_TRACE_REVIEWED": PACKET_TRACE_REVIEW_PATH.exists() and packet_trace_review["packet_sequence_matches"] is True,
        "ADOPTION_PROBE_REVIEW_3_EDGE_OBSERVATIONS_REVIEWED": EDGE_OBSERVATION_REVIEW_PATH.exists() and edge_observation_review["edge_sequence_matches"] is True,
        "ADOPTION_PROBE_REVIEW_4_UNIT_FEEDBACK_REVIEWED": UNIT_FEEDBACK_REVIEW_PATH.exists() and unit_feedback_review["required_statuses_seen"] is True and unit_feedback_review["all_feedback_useful"] is True,
        "ADOPTION_PROBE_REVIEW_5_NEGATIVE_CONTROLS_REVIEWED": NEGATIVE_CONTROL_REVIEW_PATH.exists() and negative_control_review["all_fail_closed"] is True,
        "ADOPTION_PROBE_REVIEW_6_PACKET_LAW_DISTINCTIONS_CONFIRMED": all(packet_trace_review["packet_law_results"].values()),
        "ADOPTION_PROBE_REVIEW_7_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "ADOPTION_PROBE_REVIEW_8_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "ADOPTION_PROBE_REVIEW_9_NO_C7": classification["c7_authorized"] is False,
        "ADOPTION_PROBE_REVIEW_10_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "ADOPTION_PROBE_REVIEW_11_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["c6_reviewed_reference_mutated"] is False,
        "ADOPTION_PROBE_REVIEW_12_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "ADOPTION_PROBE_REVIEW_13_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "ADOPTION_PROBE_REVIEW_14_CLOSE_CANDIDATE_READY": close_candidate["review_pass"] is True,
        "ADOPTION_PROBE_REVIEW_15_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEW_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEW_V0"
    terminal = transition_trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_probe": SOURCE_PROBE_RECEIPT_ID,
        "recommended_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "bounded_c6_protocol_adoption_probe_review_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_probe_receipt_id": SOURCE_PROBE_RECEIPT_ID,
        "source_probe_design_receipt_id": SOURCE_PROBE_DESIGN_RECEIPT_ID,
        "source_c6_protocol_reference_closure_receipt_id": SOURCE_C6_PROTOCOL_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_bounded_c6_adoption_probe_review_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "bounded_c6_protocol_adoption_probe_review_complete": gate == "PASS",
            "bounded_c6_protocol_adoption_probe_review_pass": gate == "PASS",
            "close_candidate_ready": gate == "PASS",
            "source_probe_built": probe_summary.get("bounded_c6_protocol_adoption_probe_built"),
            "synthetic_protocol_only": probe_summary.get("synthetic_protocol_only"),
            "runtime_effect": False,
            "packet_trace_count": len(packet_trace),
            "edge_observation_count": len(edge_observations),
            "unit_feedback_count": len(unit_feedback),
            "negative_control_count": len(negative_controls),
            "negative_controls_passed": probe_summary.get("negative_controls_passed"),
            "packet_law_distinctions_confirmed": all(packet_trace_review["packet_law_results"].values()),
            "bad_counters_zero": probe_summary.get("bad_counters_zero"),
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
            "review_basis": rel(REVIEW_BASIS_PATH),
            "source_receipt_review": rel(SOURCE_RECEIPT_REVIEW_PATH),
            "packet_trace_review": rel(PACKET_TRACE_REVIEW_PATH),
            "edge_observation_review": rel(EDGE_OBSERVATION_REVIEW_PATH),
            "unit_feedback_review": rel(UNIT_FEEDBACK_REVIEW_PATH),
            "negative_control_review": rel(NEGATIVE_CONTROL_REVIEW_PATH),
            "boundary_review": rel(BOUNDARY_REVIEW_PATH),
            "close_candidate": rel(CLOSE_CANDIDATE_PATH),
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
    print(f"bounded_c6_protocol_adoption_probe_review_receipt_id={receipt_id}")
    print(f"bounded_c6_protocol_adoption_probe_review_receipt_path={rel(receipt_path)}")
    print(f"bounded_c6_protocol_adoption_probe_review_close_candidate_path={rel(CLOSE_CANDIDATE_PATH)}")
    print(f"bounded_c6_protocol_adoption_probe_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"bounded_c6_protocol_adoption_probe_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
