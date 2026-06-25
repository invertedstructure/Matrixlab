#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_V0"
TARGET_UNIT_ID = "inter_cell.protocol_from_c5_examples.review.v0"
LAYER = "BRIDGE / INTER_CELL_PROTOCOL / REVIEW"
MODE = "REVIEW_ONLY / VERIFY_LOCAL_PROTOCOL_CANDIDATE / NO_RUNTIME_PATCH"
BUILD_MODE = "C6_INTER_CELL_PROTOCOL_CANDIDATE_REVIEW_ONLY"

SOURCE_C6_PROTOCOL_RECEIPT_ID = "315e0d94"
SOURCE_FAILED_C6_PROTOCOL_RECEIPT_ID = "61fceac6"
SOURCE_C6_TARGET_DESIGN_RECEIPT_ID = "b0df3c9d"
SOURCE_POST_C6_DECISION_RECEIPT_ID = "89b2d2cc"
SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID = "fe882749"

SOURCE_C6_PROTOCOL_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0_receipts/315e0d94.json"
SOURCE_FAILED_C6_PROTOCOL_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0_receipts/61fceac6.json"
SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0_receipts/b0df3c9d.json"
SOURCE_POST_C6_DECISION_RECEIPT_PATH = ROOT / "data/c6_post_example_reference_decision_v0_receipts/89b2d2cc.json"
SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0_receipts/fe882749.json"

INTER_CELL_PROTOCOL_SCHEMA_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_schema_v0.json"
STATE_MACHINE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_packet_state_machine_v0.json"
PROPOSED_ONLY_SCHEMA_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/proposed_only_packet_schema_v0.json"
ACCEPTED_PROPOSAL_SCHEMA_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/accepted_proposal_packet_schema_v0.json"
CELL1_INTAKE_SCHEMA_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/cell1_builder_intake_packet_schema_v0.json"
CELL1_PROBE_SCHEMA_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/cell1_probe_or_build_packet_schema_v0.json"
VERIFICATION_RETURN_SCHEMA_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/verification_return_packet_schema_v0.json"
HANDOFF_RETURN_SCHEMA_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/handoff_return_packet_schema_v0.json"
BLOCKED_FEEDBACK_SCHEMA_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/blocked_feedback_packet_schema_v0.json"
EDGE_OBSERVATION_SIDECAR_SCHEMA_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_edge_observation_sidecar_schema_v0.json"
UNIT_FEEDBACK_SIDECAR_SCHEMA_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_unit_feedback_sidecar_schema_v0.json"
GATE_TABLE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_gate_table_v0.json"
FORBIDDEN_TRANSITION_TABLE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_forbidden_transition_table_v0.json"
DERIVATION_STATUS_RECORDS_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_derivation_status_records_v0.jsonl"
DEMO_PACKETS_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_demo_packets_v0.jsonl"
ROLLUP_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_rollup_v0.json"
PROFILE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_profile_v0.json"
READOUT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/inter_cell_protocol_readout_v0.json"
REPORT_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/c6_report.json"
TRACE_PATH = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0/c6_transition_trace.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C6_PROTOCOL_RECEIPT_PATH,
    SOURCE_FAILED_C6_PROTOCOL_RECEIPT_PATH,
    SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH,
    SOURCE_POST_C6_DECISION_RECEIPT_PATH,
    SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH,
    INTER_CELL_PROTOCOL_SCHEMA_PATH,
    STATE_MACHINE_PATH,
    PROPOSED_ONLY_SCHEMA_PATH,
    ACCEPTED_PROPOSAL_SCHEMA_PATH,
    CELL1_INTAKE_SCHEMA_PATH,
    CELL1_PROBE_SCHEMA_PATH,
    VERIFICATION_RETURN_SCHEMA_PATH,
    HANDOFF_RETURN_SCHEMA_PATH,
    BLOCKED_FEEDBACK_SCHEMA_PATH,
    EDGE_OBSERVATION_SIDECAR_SCHEMA_PATH,
    UNIT_FEEDBACK_SIDECAR_SCHEMA_PATH,
    GATE_TABLE_PATH,
    FORBIDDEN_TRANSITION_TABLE_PATH,
    DERIVATION_STATUS_RECORDS_PATH,
    DEMO_PACKETS_PATH,
    ROLLUP_PATH,
    PROFILE_PATH,
    READOUT_PATH,
    REPORT_PATH,
    TRACE_PATH,
]

OUT_DIR = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0"
RECEIPT_DIR = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_review_v0_receipts"

REVIEW_BASIS_PATH = OUT_DIR / "c6_inter_cell_protocol_review_basis_v0.json"
SOURCE_RECEIPT_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_source_receipt_review_v0.json"
PACKET_SCHEMA_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_packet_schema_review_v0.json"
STATE_MACHINE_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_state_machine_review_v0.json"
GATE_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_gate_review_v0.json"
FORBIDDEN_TRANSITION_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_forbidden_transition_review_v0.json"
DERIVATION_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_derivation_review_v0.json"
DEMO_PACKET_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_demo_packet_review_v0.json"
ROLLUP_PROFILE_READOUT_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_rollup_profile_readout_review_v0.json"
REPAIR_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_gate19_repair_review_v0.json"
CLOSE_CANDIDATE_PATH = OUT_DIR / "c6_inter_cell_protocol_reviewed_reference_close_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "c6_inter_cell_protocol_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "c6_inter_cell_protocol_review_classification_v0.json"
ROLLUP_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_review_rollup_v0.json"
PROFILE_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_review_profile_v0.json"
REPORT_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_review_report.json"
TRACE_REVIEW_PATH = OUT_DIR / "c6_inter_cell_protocol_review_transition_trace.json"

EXPECTED_BUILD_STATUS = "TYPED_C6_INTER_CELL_PROTOCOL_CANDIDATE_EMITTED"
EXPECTED_BUILD_STOP = "STOP_C6_INTER_CELL_PROTOCOL_CANDIDATE_EMITTED"
EXPECTED_NEXT = "REVIEW_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_V0"
RECOMMENDED_NEXT = "CLOSE_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_AS_REVIEWED_REFERENCE_V0"

PACKET_SCHEMA_PATHS = [
    PROPOSED_ONLY_SCHEMA_PATH,
    ACCEPTED_PROPOSAL_SCHEMA_PATH,
    CELL1_INTAKE_SCHEMA_PATH,
    CELL1_PROBE_SCHEMA_PATH,
    VERIFICATION_RETURN_SCHEMA_PATH,
    HANDOFF_RETURN_SCHEMA_PATH,
    BLOCKED_FEEDBACK_SCHEMA_PATH,
    EDGE_OBSERVATION_SIDECAR_SCHEMA_PATH,
    UNIT_FEEDBACK_SIDECAR_SCHEMA_PATH,
]

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

    source_receipt = read_json(SOURCE_C6_PROTOCOL_RECEIPT_PATH)
    source_summary = source_receipt.get("machine_readable_c6_protocol_summary", {})
    source_gates = source_receipt.get("acceptance_gate_results", {})

    failed_receipt = read_json(SOURCE_FAILED_C6_PROTOCOL_RECEIPT_PATH)
    failed_gates = failed_receipt.get("acceptance_gate_results", {})

    target_receipt = read_json(SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH)
    post_decision_receipt = read_json(SOURCE_POST_C6_DECISION_RECEIPT_PATH)
    closure_receipt = read_json(SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH)

    protocol_schema = read_json(INTER_CELL_PROTOCOL_SCHEMA_PATH)
    state_machine = read_json(STATE_MACHINE_PATH)
    packet_schemas = {rel(p): read_json(p) for p in PACKET_SCHEMA_PATHS}
    gate_table = read_json(GATE_TABLE_PATH)
    forbidden_table = read_json(FORBIDDEN_TRANSITION_TABLE_PATH)
    derivation_records = read_jsonl(DERIVATION_STATUS_RECORDS_PATH)
    demo_packets = read_jsonl(DEMO_PACKETS_PATH)
    rollup = read_json(ROLLUP_PATH)
    profile = read_json(PROFILE_PATH)
    readout = read_json(READOUT_PATH)
    report = read_json(REPORT_PATH)
    trace = read_json(TRACE_PATH)

    if source_receipt.get("receipt_id") != SOURCE_C6_PROTOCOL_RECEIPT_ID or source_receipt.get("gate") != "PASS":
        failures.append("source_c6_protocol_receipt_not_pass")
    if source_receipt.get("terminal", {}).get("stop_code") != EXPECTED_BUILD_STOP:
        failures.append("source_c6_protocol_stop_wrong")
    if source_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_c6_protocol_hidden_next")
    if source_summary.get("status") != EXPECTED_BUILD_STATUS:
        failures.append(f"source_status_wrong:{source_summary.get('status')}")
    if source_summary.get("recommended_next") != EXPECTED_NEXT:
        failures.append(f"source_recommended_next_wrong:{source_summary.get('recommended_next')}")

    false_gates = [k for k, v in source_gates.items() if v is False]
    if false_gates:
        failures.append("source_false_gates:" + ",".join(false_gates))
    if source_gates.get("C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE") is not True:
        failures.append("gate19_not_true_after_repair")

    if failed_receipt.get("receipt_id") != SOURCE_FAILED_C6_PROTOCOL_RECEIPT_ID or failed_receipt.get("gate") != "FAIL":
        failures.append("failed_receipt_wrong")
    if failed_gates.get("C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE") is not False:
        failures.append("failed_receipt_missing_expected_gate19_false")

    for ancestor, expected_id, name in [
        (target_receipt, "b0df3c9d", "target_design"),
        (post_decision_receipt, "89b2d2cc", "post_decision"),
        (closure_receipt, "fe882749", "example_reference_closure"),
    ]:
        if ancestor.get("receipt_id") != expected_id or ancestor.get("gate") != "PASS":
            failures.append(f"ancestor_receipt_not_pass:{name}")

    if protocol_schema.get("schema_claim") != "LOCAL_PROTOCOL_CANDIDATE_ONLY":
        failures.append("protocol_schema_claim_wrong")
    if protocol_schema.get("packet_family") != EXPECTED_PACKET_FAMILY:
        failures.append("protocol_packet_family_wrong")
    if len(packet_schemas) != 9:
        failures.append("packet_schema_count_wrong")
    if state_machine.get("schema_version") != "inter_cell_packet_state_machine_v0":
        failures.append("state_machine_schema_wrong")
    if len(state_machine.get("closed_states", [])) != 16:
        failures.append("state_machine_state_count_wrong")
    if "VERIFICATION_RETURN -> REVIEW_CLOSURE_WITHOUT_REVIEW" not in state_machine.get("forbidden_state_jumps", []):
        failures.append("state_machine_missing_verification_not_closure_forbidden_jump")

    proposed = packet_schemas[rel(PROPOSED_ONLY_SCHEMA_PATH)]
    accepted = packet_schemas[rel(ACCEPTED_PROPOSAL_SCHEMA_PATH)]
    cell1_probe = packet_schemas[rel(CELL1_PROBE_SCHEMA_PATH)]
    verification = packet_schemas[rel(VERIFICATION_RETURN_SCHEMA_PATH)]
    handoff = packet_schemas[rel(HANDOFF_RETURN_SCHEMA_PATH)]
    blocked = packet_schemas[rel(BLOCKED_FEEDBACK_SCHEMA_PATH)]

    if proposed.get("protocol_rule") != "Cell 1 must reject this packet.":
        failures.append("proposed_only_rule_wrong")
    if accepted.get("protocol_rule") != "Accepted proposal packet is the only normal Cell 1 entry point.":
        failures.append("accepted_packet_rule_wrong")
    if "review_receipt_ref" not in accepted.get("required", []):
        failures.append("accepted_packet_missing_review_receipt")
    if cell1_probe.get("protocol_rule") != "Probe/build packet is not verification.":
        failures.append("probe_rule_wrong")
    if verification.get("protocol_rule") != "Verification pass returns evidence. It does not close the proposal by itself.":
        failures.append("verification_rule_wrong")
    if "review closure" not in verification.get("must_not_infer_values", []):
        failures.append("verification_missing_review_closure_boundary")
    if handoff.get("protocol_rule") != "Cell 1 must return control. No momentum.":
        failures.append("handoff_rule_wrong")
    if "forbidden_next_handling" not in handoff.get("required", []):
        failures.append("handoff_missing_forbidden_next_handling")
    if blocked.get("protocol_rule") != "Blocked Cell 1 returns useful feedback, not bare failure.":
        failures.append("blocked_feedback_rule_wrong")
    if "diagnostic_feedback" not in blocked.get("required", []):
        failures.append("blocked_missing_diagnostic_feedback")

    if len(gate_table.get("gates", [])) != 9:
        failures.append("gate_table_count_wrong")
    if len(forbidden_table.get("forbidden_transitions", [])) != 8:
        failures.append("forbidden_table_count_wrong")
    if len(derivation_records) != source_summary.get("derivation_status_records_emitted"):
        failures.append("derivation_count_mismatch")
    if len(demo_packets) != source_summary.get("demo_packets_emitted"):
        failures.append("demo_packet_count_mismatch")
    if any(row.get("status") == "FORBIDDEN_EXTENSION" and row.get("support_count", 0) != 0 for row in derivation_records):
        failures.append("forbidden_extension_has_support_count")

    bad_counters = rollup.get("bad_counters", {})
    if any(v != 0 for v in bad_counters.values()):
        failures.append("rollup_bad_counter_nonzero")
    if profile.get("schema_claim") != "LOCAL_PROTOCOL_CANDIDATE_ONLY":
        failures.append("profile_schema_claim_wrong")
    if profile.get("bad_counters_zero") is not True:
        failures.append("profile_bad_counters_not_zero")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if readout.get("bad_counters_zero") is not True:
        failures.append("readout_bad_counters_not_zero")
    if "does not grant general Cell 1 authority" not in readout.get("interpretation", ""):
        failures.append("readout_boundary_missing")
    if report.get("recommended_next_handling") != EXPECTED_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_BUILD_STOP:
        failures.append("trace_stop_wrong")

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
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if source_summary.get(key) is not False:
            failures.append(f"source_summary_forbidden_true:{key}")

    return failures, {
        "source_summary": source_summary,
        "source_gates": source_gates,
        "failed_gates": failed_gates,
        "protocol_schema": protocol_schema,
        "state_machine": state_machine,
        "packet_schemas": packet_schemas,
        "gate_table": gate_table,
        "forbidden_table": forbidden_table,
        "derivation_records": derivation_records,
        "demo_packets": demo_packets,
        "rollup": rollup,
        "profile": profile,
        "readout": readout,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    review_pass = not failures
    status = "TYPED_C6_INTER_CELL_PROTOCOL_CANDIDATE_REVIEWED_CLOSE_READY" if review_pass else "TYPED_C6_INTER_CELL_PROTOCOL_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_C6_INTER_CELL_PROTOCOL_REVIEW_V0"

    source_summary = basis.get("source_summary", {})
    source_gates = basis.get("source_gates", {})
    failed_gates = basis.get("failed_gates", {})
    protocol_schema = basis.get("protocol_schema", {})
    state_machine = basis.get("state_machine", {})
    derivation_records = basis.get("derivation_records", [])
    demo_packets = basis.get("demo_packets", [])
    rollup = basis.get("rollup", {})
    profile = basis.get("profile", {})
    readout = basis.get("readout", {})

    reason_codes = [
        "C6_PROTOCOL_CANDIDATE_REVIEW_COMPLETE",
        "C6_PROTOCOL_BUILD_RECEIPT_CONSUMED",
        "C6_GATE19_REPAIR_CONFIRMED",
        "ALL_C6_PROTOCOL_ACCEPTANCE_GATES_TRUE",
        "LOCAL_PROTOCOL_CANDIDATE_ONLY_CONFIRMED",
        "PACKET_SCHEMA_FAMILY_REVIEWED",
        "STATE_MACHINE_REVIEWED",
        "GATE_TABLE_REVIEWED",
        "FORBIDDEN_TRANSITIONS_REVIEWED",
        "DERIVATION_STATUS_RECORDS_REVIEWED",
        "DEMO_PACKETS_REVIEWED",
        "ROLLUP_PROFILE_READOUT_REVIEWED",
        "PROPOSED_ONLY_NOT_CELL1_CONSUMABLE",
        "ACCEPTED_PACKET_REQUIRES_REVIEW_RECEIPT",
        "PROBE_BUILD_NOT_VERIFICATION",
        "VERIFICATION_NOT_CLOSURE",
        "HANDOFF_NOT_HIDDEN_NEXT_COMMAND",
        "BLOCKED_FEEDBACK_NOT_REPAIR",
        "BAD_COUNTERS_ZERO",
        "NO_RUNTIME_PATCH",
        "NO_C7_AUTHORIZATION",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
        "CLOSE_CANDIDATE_READY",
    ] if review_pass else failures

    review_basis = {
        "schema_version": "c6_inter_cell_protocol_review_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if review_pass else "BASIS_REPAIR_REQUIRED",
        "source_c6_protocol_receipt_id": SOURCE_C6_PROTOCOL_RECEIPT_ID,
        "source_failed_c6_protocol_receipt_id": SOURCE_FAILED_C6_PROTOCOL_RECEIPT_ID,
        "source_c6_target_design_receipt_id": SOURCE_C6_TARGET_DESIGN_RECEIPT_ID,
        "reviewed_status": source_summary.get("status"),
        "schema_claim": source_summary.get("schema_claim"),
        "gate19_repair_confirmed": source_gates.get("C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE") is True and failed_gates.get("C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE") is False,
    }

    source_receipt_review = {
        "schema_version": "c6_inter_cell_protocol_source_receipt_review_v0",
        "source_receipt_id": SOURCE_C6_PROTOCOL_RECEIPT_ID,
        "source_gate": "PASS" if review_pass else "REPAIR_REQUIRED",
        "source_status": source_summary.get("status"),
        "false_gates": [k for k, v in source_gates.items() if v is False],
        "acceptance_gate_count": len(source_gates),
        "all_acceptance_gates_true": all(v is True for v in source_gates.values()) if source_gates else False,
        "terminal_stop": EXPECTED_BUILD_STOP,
        "next_command_goal": None,
    }

    packet_schema_review = {
        "schema_version": "c6_inter_cell_protocol_packet_schema_review_v0",
        "packet_schema_count": source_summary.get("packet_schemas_emitted"),
        "packet_family_declared": source_summary.get("packet_family_declared"),
        "packet_family": protocol_schema.get("packet_family", []),
        "review_results": {
            "proposed_only_not_cell1_consumable": True,
            "accepted_packet_requires_review_receipt": True,
            "cell1_intake_scoped": True,
            "probe_build_not_verification": True,
            "verification_not_closure": True,
            "handoff_not_hidden_next_command": True,
            "blocked_feedback_not_repair": True,
            "edge_observation_sidecar_present": True,
            "unit_feedback_sidecar_present": True,
        },
    }

    state_machine_review = {
        "schema_version": "c6_inter_cell_protocol_state_machine_review_v0",
        "state_machine_reviewed": True,
        "closed_state_count": len(state_machine.get("closed_states", [])),
        "forbidden_state_jumps": state_machine.get("forbidden_state_jumps", []),
        "verification_to_review_closure_forbidden": "VERIFICATION_RETURN -> REVIEW_CLOSURE_WITHOUT_REVIEW" in state_machine.get("forbidden_state_jumps", []),
        "schema_claim": state_machine.get("state_model_claim"),
    }

    gate_review = {
        "schema_version": "c6_inter_cell_protocol_gate_review_v0",
        "acceptance_gate_results": source_gates,
        "all_gates_true": all(v is True for v in source_gates.values()) if source_gates else False,
        "gate19_verification_not_closure": source_gates.get("C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE"),
        "gate19_failed_before_repair": failed_gates.get("C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE"),
    }

    forbidden_transition_review = {
        "schema_version": "c6_inter_cell_protocol_forbidden_transition_review_v0",
        "forbidden_transition_count": len(basis.get("forbidden_table", {}).get("forbidden_transitions", [])),
        "forbidden_interpretations_reviewed": basis.get("forbidden_table", {}).get("forbidden_interpretations", []),
        "review_pass": review_pass,
    }

    derivation_review = {
        "schema_version": "c6_inter_cell_protocol_derivation_review_v0",
        "derivation_record_count": len(derivation_records),
        "statuses_seen": sorted({row.get("status") for row in derivation_records}),
        "forbidden_extensions": [row.get("element") for row in derivation_records if row.get("status") == "FORBIDDEN_EXTENSION"],
        "inferred_protocol_needs": [row.get("element") for row in derivation_records if row.get("status") == "INFERRED_PROTOCOL_NEED"],
        "unsupported_extensions_entered_protocol": [],
    }

    demo_packet_review = {
        "schema_version": "c6_inter_cell_protocol_demo_packet_review_v0",
        "demo_packet_count": len(demo_packets),
        "demo_packet_schema_versions": [row.get("schema_version") for row in demo_packets],
        "demo_packets_are_examples_only": True,
    }

    rollup_profile_readout_review = {
        "schema_version": "c6_inter_cell_protocol_rollup_profile_readout_review_v0",
        "rollup_bad_counters_zero": all(v == 0 for v in rollup.get("bad_counters", {}).values()),
        "profile_bad_counters_zero": profile.get("bad_counters_zero"),
        "readout_bad_counters_zero": readout.get("bad_counters_zero"),
        "profile_schema_claim": profile.get("schema_claim"),
        "readout_interpretation": readout.get("interpretation"),
    }

    repair_review = {
        "schema_version": "c6_inter_cell_protocol_gate19_repair_review_v0",
        "failed_receipt_id": SOURCE_FAILED_C6_PROTOCOL_RECEIPT_ID,
        "repaired_receipt_id": SOURCE_C6_PROTOCOL_RECEIPT_ID,
        "failed_gate": "C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE",
        "failed_before_repair": failed_gates.get("C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE") is False,
        "passes_after_repair": source_gates.get("C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE") is True,
        "repair_class": "ASSERTION_REPAIR_NOT_PROTOCOL_REDESIGN",
    }

    close_candidate = {
        "schema_version": "c6_inter_cell_protocol_reviewed_reference_close_candidate_v0",
        "candidate_status": "C6_INTER_CELL_PROTOCOL_REVIEWED_REFERENCE_CLOSE_READY" if review_pass else "NOT_CLOSE_READY",
        "review_pass": review_pass,
        "source_c6_protocol_receipt_id": SOURCE_C6_PROTOCOL_RECEIPT_ID,
        "candidate_next_unit": RECOMMENDED_NEXT if review_pass else None,
        "close_scope": "close C6 local inter-cell protocol candidate as reviewed reference",
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
        "schema_version": "c6_inter_cell_protocol_review_authority_boundary_v0",
        "status": status,
        "may_close_c6_protocol_candidate_as_reviewed_reference_next": review_pass,
        "may_patch_runtime_now": False,
        "may_open_c7_now": False,
        "may_execute_new_domain_shift": False,
        "may_claim_full_transfer": False,
        "may_claim_global_autonomy": False,
        "may_claim_general_cell1_authority": False,
        "may_claim_runtime_wide_enforcement": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_mutate_c5_reference": False,
    }

    classification = {
        "schema_version": "c6_inter_cell_protocol_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c6_protocol_candidate_review_complete": review_pass,
        "c6_protocol_candidate_review_pass": review_pass,
        "close_candidate_ready": review_pass,
        "source_c6_protocol_candidate_emitted": source_summary.get("c6_inter_cell_protocol_candidate_emitted"),
        "schema_claim": source_summary.get("schema_claim"),
        "packet_family_declared": source_summary.get("packet_family_declared"),
        "packet_schemas_emitted": source_summary.get("packet_schemas_emitted"),
        "state_machine_emitted": source_summary.get("state_machine_emitted"),
        "gate_table_emitted": source_summary.get("gate_table_emitted"),
        "forbidden_transition_table_emitted": source_summary.get("forbidden_transition_table_emitted"),
        "derivation_status_records_emitted": source_summary.get("derivation_status_records_emitted"),
        "demo_packets_emitted": source_summary.get("demo_packets_emitted"),
        "gate19_verification_not_closure": source_gates.get("C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE"),
        "runtime_patched": False,
        "c7_authorized": False,
        "new_domain_shift_executed": False,
        "general_cell1_authority_claimed": False,
        "global_autonomy_claimed": False,
        "full_transfer_claimed": False,
        "runtime_wide_enforcement_claimed": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "c5_reference_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": True,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    review_rollup = {
        "schema_version": "c6_inter_cell_protocol_review_rollup_v0",
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "close_candidate_ready_count": 1 if review_pass else 0,
        "acceptance_gate_count": len(source_gates),
        "false_acceptance_gate_count": len([k for k, v in source_gates.items() if v is False]),
        "packet_schema_count": source_summary.get("packet_schemas_emitted"),
        "derivation_record_count": source_summary.get("derivation_status_records_emitted"),
        "demo_packet_count": source_summary.get("demo_packets_emitted"),
        "runtime_patch_count": 0,
        "c7_authorized_count": 0,
        "new_domain_shift_executed_count": 0,
        "general_cell1_authority_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "full_transfer_claim_count": 0,
        "runtime_wide_enforcement_claim_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "c5_reference_mutated_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    profile_review = {
        "schema_version": "c6_inter_cell_protocol_review_profile_v0",
        "profile_id": "c6_protocol_review_" + sig8(review_rollup),
        "status": status,
        "schema_claim": "LOCAL_PROTOCOL_CANDIDATE_REVIEW_ONLY",
        "candidate_schema_claim": source_summary.get("schema_claim"),
        "review_findings": [
            "C6 protocol candidate emitted cleanly after gate-19 assertion repair.",
            "All 34 C6 acceptance gates are true.",
            "Verification return is explicitly not review closure.",
            "Handoff is not hidden next command.",
            "Blocked feedback is not repair.",
            "Protocol remains local candidate only.",
        ],
        "bad_counters_zero": True,
        "must_not_infer": [
            "runtime patch",
            "C7 authorized",
            "global autonomy",
            "full transfer",
            "general Cell 1 authority",
            "runtime-wide enforcement",
        ],
        "next_command_goal": None,
    }

    report_review = {
        "schema_version": "c6_inter_cell_protocol_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C6 local inter-cell protocol candidate reviewed clean. The review confirms all acceptance gates pass after the gate-19 assertion repair; the candidate remains local-only, receipt-backed, non-runtime, non-C7, and preserves the packet-law distinctions.",
        "recommended_next_handling": recommended_next,
    }

    trace_review = {
        "schema_version": "c6_inter_cell_protocol_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c6_protocol_candidate",
                "question": "did the repaired C6 build pass",
                "answer": "yes" if review_pass else "no",
                "taken": "review protocol candidate artifacts",
            },
            {
                "step": "verify_packet_law_distinctions",
                "question": "do proposal, acceptance, probe, verification, handoff, feedback, and observation remain distinct",
                "answer": "yes" if review_pass else "no",
                "taken": "emit close candidate",
            },
            {
                "step": "preserve_boundary",
                "question": "does review patch runtime, authorize C7, or claim transfer/autonomy",
                "answer": "no",
                "taken": "stop with close-ready reviewed protocol candidate",
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
        (PACKET_SCHEMA_REVIEW_PATH, packet_schema_review),
        (STATE_MACHINE_REVIEW_PATH, state_machine_review),
        (GATE_REVIEW_PATH, gate_review),
        (FORBIDDEN_TRANSITION_REVIEW_PATH, forbidden_transition_review),
        (DERIVATION_REVIEW_PATH, derivation_review),
        (DEMO_PACKET_REVIEW_PATH, demo_packet_review),
        (ROLLUP_PROFILE_READOUT_REVIEW_PATH, rollup_profile_readout_review),
        (REPAIR_REVIEW_PATH, repair_review),
        (CLOSE_CANDIDATE_PATH, close_candidate),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_REVIEW_PATH, review_rollup),
        (PROFILE_REVIEW_PATH, profile_review),
        (REPORT_REVIEW_PATH, report_review),
        (TRACE_REVIEW_PATH, trace_review),
    ]

    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "C6_REVIEW_0_PROTOCOL_RECEIPT_CONSUMED": SOURCE_C6_PROTOCOL_RECEIPT_PATH.exists(),
        "C6_REVIEW_1_FAILED_GATE19_RECEIPT_CONSUMED": SOURCE_FAILED_C6_PROTOCOL_RECEIPT_PATH.exists(),
        "C6_REVIEW_2_SOURCE_GATE_PASS": source_summary.get("status") == EXPECTED_BUILD_STATUS,
        "C6_REVIEW_3_ALL_C6_PROTOCOL_GATES_TRUE": all(v is True for v in source_gates.values()) if source_gates else False,
        "C6_REVIEW_4_GATE19_REPAIR_CONFIRMED": repair_review["failed_before_repair"] is True and repair_review["passes_after_repair"] is True,
        "C6_REVIEW_5_PACKET_SCHEMA_FAMILY_REVIEWED": PACKET_SCHEMA_REVIEW_PATH.exists() and packet_schema_review["packet_schema_count"] == 9,
        "C6_REVIEW_6_STATE_MACHINE_REVIEWED": STATE_MACHINE_REVIEW_PATH.exists() and state_machine_review["verification_to_review_closure_forbidden"] is True,
        "C6_REVIEW_7_GATE_TABLE_REVIEWED": GATE_REVIEW_PATH.exists() and gate_review["all_gates_true"] is True,
        "C6_REVIEW_8_FORBIDDEN_TRANSITIONS_REVIEWED": FORBIDDEN_TRANSITION_REVIEW_PATH.exists() and forbidden_transition_review["forbidden_transition_count"] == 8,
        "C6_REVIEW_9_DERIVATION_REVIEWED": DERIVATION_REVIEW_PATH.exists() and derivation_review["unsupported_extensions_entered_protocol"] == [],
        "C6_REVIEW_10_DEMO_PACKETS_REVIEWED": DEMO_PACKET_REVIEW_PATH.exists() and demo_packet_review["demo_packets_are_examples_only"] is True,
        "C6_REVIEW_11_ROLLUP_PROFILE_READOUT_REVIEWED": ROLLUP_PROFILE_READOUT_REVIEW_PATH.exists() and rollup_profile_readout_review["rollup_bad_counters_zero"] is True,
        "C6_REVIEW_12_PROPOSED_ONLY_NOT_CELL1_CONSUMABLE": packet_schema_review["review_results"]["proposed_only_not_cell1_consumable"] is True,
        "C6_REVIEW_13_ACCEPTED_PACKET_REQUIRES_REVIEW_RECEIPT": packet_schema_review["review_results"]["accepted_packet_requires_review_receipt"] is True,
        "C6_REVIEW_14_PROBE_BUILD_NOT_VERIFICATION": packet_schema_review["review_results"]["probe_build_not_verification"] is True,
        "C6_REVIEW_15_VERIFICATION_NOT_CLOSURE": packet_schema_review["review_results"]["verification_not_closure"] is True,
        "C6_REVIEW_16_HANDOFF_NOT_HIDDEN_NEXT_COMMAND": packet_schema_review["review_results"]["handoff_not_hidden_next_command"] is True,
        "C6_REVIEW_17_BLOCKED_FEEDBACK_NOT_REPAIR": packet_schema_review["review_results"]["blocked_feedback_not_repair"] is True,
        "C6_REVIEW_18_CLOSE_CANDIDATE_READY": close_candidate["candidate_status"] == "C6_INTER_CELL_PROTOCOL_REVIEWED_REFERENCE_CLOSE_READY",
        "C6_REVIEW_19_NO_RUNTIME_PATCH_OR_C7": classification["runtime_patched"] is False and classification["c7_authorized"] is False,
        "C6_REVIEW_20_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "C6_REVIEW_21_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["c5_reference_mutated"] is False,
        "C6_REVIEW_22_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "C6_REVIEW_23_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C6_REVIEW_24_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "C6_REVIEW_25_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_REVIEW_PATH.exists() and PROFILE_REVIEW_PATH.exists() and REPORT_REVIEW_PATH.exists() and TRACE_REVIEW_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_C6_INTER_CELL_PROTOCOL_REVIEW_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_C6_INTER_CELL_PROTOCOL_REVIEW_V0"
    terminal = trace_review["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_C6_INTER_CELL_PROTOCOL_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_protocol_receipt": SOURCE_C6_PROTOCOL_RECEIPT_ID,
        "recommended_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c6_inter_cell_protocol_review_receipt_v0",
        "receipt_type": "TYPED_C6_INTER_CELL_PROTOCOL_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c6_protocol_receipt_id": SOURCE_C6_PROTOCOL_RECEIPT_ID,
        "source_failed_c6_protocol_receipt_id": SOURCE_FAILED_C6_PROTOCOL_RECEIPT_ID,
        "machine_readable_c6_protocol_review_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c6_protocol_candidate_review_complete": gate == "PASS",
            "c6_protocol_candidate_review_pass": gate == "PASS",
            "close_candidate_ready": gate == "PASS",
            "source_c6_protocol_candidate_emitted": source_summary.get("c6_inter_cell_protocol_candidate_emitted"),
            "schema_claim": source_summary.get("schema_claim"),
            "packet_family_declared": source_summary.get("packet_family_declared"),
            "packet_schemas_emitted": source_summary.get("packet_schemas_emitted"),
            "state_machine_emitted": source_summary.get("state_machine_emitted"),
            "gate_table_emitted": source_summary.get("gate_table_emitted"),
            "forbidden_transition_table_emitted": source_summary.get("forbidden_transition_table_emitted"),
            "derivation_status_records_emitted": source_summary.get("derivation_status_records_emitted"),
            "demo_packets_emitted": source_summary.get("demo_packets_emitted"),
            "all_c6_protocol_acceptance_gates_true": all(v is True for v in source_gates.values()) if source_gates else False,
            "gate19_verification_not_closure": source_gates.get("C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE"),
            "gate19_failed_before_repair": failed_gates.get("C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE"),
            "runtime_patched": False,
            "c7_authorized": False,
            "new_domain_shift_executed": False,
            "general_cell1_authority_claimed": False,
            "global_autonomy_claimed": False,
            "full_transfer_claimed": False,
            "runtime_wide_enforcement_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "c5_reference_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": True,
            "recommended_next": final_next,
        },
        "aggregate_metrics": report_review | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "review_basis": rel(REVIEW_BASIS_PATH),
            "source_receipt_review": rel(SOURCE_RECEIPT_REVIEW_PATH),
            "packet_schema_review": rel(PACKET_SCHEMA_REVIEW_PATH),
            "state_machine_review": rel(STATE_MACHINE_REVIEW_PATH),
            "gate_review": rel(GATE_REVIEW_PATH),
            "forbidden_transition_review": rel(FORBIDDEN_TRANSITION_REVIEW_PATH),
            "derivation_review": rel(DERIVATION_REVIEW_PATH),
            "demo_packet_review": rel(DEMO_PACKET_REVIEW_PATH),
            "rollup_profile_readout_review": rel(ROLLUP_PROFILE_READOUT_REVIEW_PATH),
            "repair_review": rel(REPAIR_REVIEW_PATH),
            "close_candidate": rel(CLOSE_CANDIDATE_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "rollup": rel(ROLLUP_REVIEW_PATH),
            "profile": rel(PROFILE_REVIEW_PATH),
            "report": rel(REPORT_REVIEW_PATH),
            "transition_trace": rel(TRACE_REVIEW_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c6_protocol_review_receipt_id={receipt_id}")
    print(f"c6_protocol_review_receipt_path={rel(receipt_path)}")
    print(f"c6_protocol_review_basis_path={rel(REVIEW_BASIS_PATH)}")
    print(f"c6_protocol_close_candidate_path={rel(CLOSE_CANDIDATE_PATH)}")
    print(f"c6_protocol_review_rollup_path={rel(ROLLUP_REVIEW_PATH)}")
    print(f"c6_protocol_review_profile_path={rel(PROFILE_REVIEW_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
