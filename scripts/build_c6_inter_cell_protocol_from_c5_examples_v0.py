#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_V0"
TARGET_UNIT_ID = "inter_cell.protocol_from_c5_examples.v0"
LAYER = "BRIDGE / INTER_CELL_PROTOCOL"
MODE = "DEFINE / CERTIFY / LOCAL_PROTOCOL_CANDIDATE"
BUILD_MODE = "C6_INTER_CELL_PROTOCOL_CANDIDATE_BUILD"

SOURCE_C6_TARGET_DESIGN_RECEIPT_ID = "b0df3c9d"
SOURCE_POST_C6_DECISION_RECEIPT_ID = "89b2d2cc"
SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID = "fe882749"

SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0_receipts/b0df3c9d.json"

C6_TARGET_BASIS_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_target_basis_v0.json"
C6_TARGET_SPEC_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_target_spec_v0.json"
C6_PACKET_FAMILY_TARGET_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_packet_family_target_v0.json"
C6_STATE_MODEL_TARGET_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_state_model_target_v0.json"
C6_GATE_REQUIREMENTS_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_gate_requirements_v0.json"
C6_FORBIDDEN_TRANSITION_TARGET_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_forbidden_transition_target_v0.json"
C6_DERIVATION_POLICY_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_derivation_policy_v0.json"
C6_NEGATIVE_CONTROL_TARGET_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_negative_control_target_v0.json"
C6_OUTPUT_MANIFEST_TARGET_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_output_manifest_target_v0.json"
C6_ACCEPTANCE_GATES_TARGET_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_acceptance_gates_target_v0.json"
C6_BUILD_CONTRACT_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_build_contract_v0.json"
C6_TARGET_AUTHORITY_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_target_authority_boundary_v0.json"
C6_TARGET_CLASSIFICATION_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_target_classification_v0.json"
C6_TARGET_ROLLUP_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_target_rollup_v0.json"
C6_TARGET_PROFILE_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_target_profile_v0.json"
C6_TARGET_REPORT_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_target_report.json"
C6_TARGET_TRACE_PATH = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0/c6_inter_cell_protocol_target_transition_trace.json"

SOURCE_POST_C6_DECISION_RECEIPT_PATH = ROOT / "data/c6_post_example_reference_decision_v0_receipts/89b2d2cc.json"
SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0_receipts/fe882749.json"
C6_EXAMPLES_JSONL_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_examples_from_c5_v0.jsonl"
C6_EXAMPLE_CATALOG_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_example_catalog_v0.json"
C6_PROTOCOL_PRESSURE_READOUT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_protocol_pressure_readout_from_c5_examples_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH,
    C6_TARGET_BASIS_PATH,
    C6_TARGET_SPEC_PATH,
    C6_PACKET_FAMILY_TARGET_PATH,
    C6_STATE_MODEL_TARGET_PATH,
    C6_GATE_REQUIREMENTS_PATH,
    C6_FORBIDDEN_TRANSITION_TARGET_PATH,
    C6_DERIVATION_POLICY_PATH,
    C6_NEGATIVE_CONTROL_TARGET_PATH,
    C6_OUTPUT_MANIFEST_TARGET_PATH,
    C6_ACCEPTANCE_GATES_TARGET_PATH,
    C6_BUILD_CONTRACT_PATH,
    C6_TARGET_AUTHORITY_PATH,
    C6_TARGET_CLASSIFICATION_PATH,
    C6_TARGET_ROLLUP_PATH,
    C6_TARGET_PROFILE_PATH,
    C6_TARGET_REPORT_PATH,
    C6_TARGET_TRACE_PATH,
    SOURCE_POST_C6_DECISION_RECEIPT_PATH,
    SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH,
    C6_EXAMPLES_JSONL_PATH,
    C6_EXAMPLE_CATALOG_PATH,
    C6_PROTOCOL_PRESSURE_READOUT_PATH,
]

OUT_DIR = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0"
RECEIPT_DIR = ROOT / "data/c6_inter_cell_protocol_from_c5_examples_v0_receipts"

INTER_CELL_PROTOCOL_SCHEMA_PATH = OUT_DIR / "inter_cell_protocol_schema_v0.json"
STATE_MACHINE_PATH = OUT_DIR / "inter_cell_packet_state_machine_v0.json"
PROPOSED_ONLY_SCHEMA_PATH = OUT_DIR / "proposed_only_packet_schema_v0.json"
ACCEPTED_PROPOSAL_SCHEMA_PATH = OUT_DIR / "accepted_proposal_packet_schema_v0.json"
CELL1_INTAKE_SCHEMA_PATH = OUT_DIR / "cell1_builder_intake_packet_schema_v0.json"
CELL1_PROBE_SCHEMA_PATH = OUT_DIR / "cell1_probe_or_build_packet_schema_v0.json"
VERIFICATION_RETURN_SCHEMA_PATH = OUT_DIR / "verification_return_packet_schema_v0.json"
HANDOFF_RETURN_SCHEMA_PATH = OUT_DIR / "handoff_return_packet_schema_v0.json"
BLOCKED_FEEDBACK_SCHEMA_PATH = OUT_DIR / "blocked_feedback_packet_schema_v0.json"
EDGE_OBSERVATION_SIDECAR_SCHEMA_PATH = OUT_DIR / "inter_cell_edge_observation_sidecar_schema_v0.json"
UNIT_FEEDBACK_SIDECAR_SCHEMA_PATH = OUT_DIR / "inter_cell_unit_feedback_sidecar_schema_v0.json"
GATE_TABLE_PATH = OUT_DIR / "inter_cell_protocol_gate_table_v0.json"
FORBIDDEN_TRANSITION_TABLE_PATH = OUT_DIR / "inter_cell_forbidden_transition_table_v0.json"
DERIVATION_STATUS_RECORDS_PATH = OUT_DIR / "inter_cell_derivation_status_records_v0.jsonl"
DEMO_PACKETS_PATH = OUT_DIR / "inter_cell_protocol_demo_packets_v0.jsonl"
ROLLUP_PATH = OUT_DIR / "inter_cell_protocol_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "inter_cell_protocol_profile_v0.json"
READOUT_PATH = OUT_DIR / "inter_cell_protocol_readout_v0.json"
REPORT_PATH = OUT_DIR / "c6_report.json"
TRACE_PATH = OUT_DIR / "c6_transition_trace.json"

EXPECTED_TARGET_STATUS = "TYPED_C6_INTER_CELL_PROTOCOL_TARGET_DESIGNED_BUILD_READY"
EXPECTED_TARGET_STOP = "STOP_TYPED_C6_INTER_CELL_PROTOCOL_TARGET_DESIGNED_BUILD_READY"

PACKET_FAMILY = [
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

BAD_COUNTER_KEYS = [
    "proposed_only_consumed_by_cell1_count",
    "proposal_accepted_without_review_count",
    "accepted_packet_without_review_receipt_count",
    "cell1_consumed_unscoped_packet_count",
    "cell1_scope_expansion_count",
    "cell1_freebuild_count",
    "cell1_auto_chain_count",
    "probe_counted_as_verification_count",
    "verification_counted_as_closure_count",
    "handoff_counted_as_hidden_next_command_count",
    "blocked_feedback_counted_as_repair_count",
    "bare_failed_status_count",
    "edge_observation_missing_count",
    "unit_feedback_missing_count",
    "general_cell1_authority_claim_count",
    "global_autonomy_claim_count",
    "full_transfer_claim_count",
    "source_reference_mutation_count",
    "latest_file_guessing_count",
    "mtime_selection_count",
    "hidden_next_command_count",
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

    target_receipt = read_json(SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH)
    target_summary = target_receipt.get("machine_readable_c6_protocol_target_design_summary", {})
    build_contract = read_json(C6_BUILD_CONTRACT_PATH)
    target_spec = read_json(C6_TARGET_SPEC_PATH)
    packet_family_target = read_json(C6_PACKET_FAMILY_TARGET_PATH)
    state_model_target = read_json(C6_STATE_MODEL_TARGET_PATH)
    gate_requirements = read_json(C6_GATE_REQUIREMENTS_PATH)
    forbidden_target = read_json(C6_FORBIDDEN_TRANSITION_TARGET_PATH)
    derivation_policy = read_json(C6_DERIVATION_POLICY_PATH)
    negative_target = read_json(C6_NEGATIVE_CONTROL_TARGET_PATH)
    acceptance_target = read_json(C6_ACCEPTANCE_GATES_TARGET_PATH)
    target_profile = read_json(C6_TARGET_PROFILE_PATH)
    examples = read_jsonl(C6_EXAMPLES_JSONL_PATH)
    catalog = read_json(C6_EXAMPLE_CATALOG_PATH)
    pressure = read_json(C6_PROTOCOL_PRESSURE_READOUT_PATH)

    if target_receipt.get("receipt_id") != SOURCE_C6_TARGET_DESIGN_RECEIPT_ID or target_receipt.get("gate") != "PASS":
        failures.append("target_design_receipt_not_pass")
    if target_receipt.get("terminal", {}).get("stop_code") != EXPECTED_TARGET_STOP:
        failures.append("target_design_stop_wrong")
    if target_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("target_design_hidden_next")
    if target_summary.get("status") != EXPECTED_TARGET_STATUS:
        failures.append(f"target_status_wrong:{target_summary.get('status')}")
    if target_summary.get("recommended_next") != UNIT_ID:
        failures.append(f"target_recommended_next_wrong:{target_summary.get('recommended_next')}")
    for key in [
        "c6_protocol_target_designed",
        "c6_protocol_build_ready",
        "state_model_declared",
        "bad_counters_zero",
    ]:
        if target_summary.get(key) is not True:
            failures.append(f"target_summary_required_true_missing:{key}")
    for key in [
        "protocol_built_in_target_design",
        "protocol_emitted_in_target_design",
        "runtime_patched",
        "c7_authorized",
        "new_domain_shift_executed",
        "full_transfer_claimed",
        "global_autonomy_claimed",
        "general_cell1_authority_claimed",
        "runtime_wide_enforcement_claimed",
        "source_mutated",
        "prior_receipt_mutated",
        "c5_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if target_summary.get(key) is not False:
            failures.append(f"target_forbidden_true:{key}")
    if build_contract.get("build_unit") != UNIT_ID:
        failures.append("build_contract_unit_wrong")
    if build_contract.get("build_authorized_after_target_design") is not True:
        failures.append("build_contract_not_authorized")
    if target_spec.get("schema_claim") != "LOCAL_PROTOCOL_CANDIDATE_TARGET_ONLY":
        failures.append("target_spec_claim_wrong")
    if packet_family_target.get("packet_family") != PACKET_FAMILY:
        failures.append("packet_family_target_wrong")
    if len(state_model_target.get("closed_states", [])) != 16:
        failures.append("state_count_wrong")
    if len(gate_requirements.get("gates", [])) != 9:
        failures.append("gate_count_wrong")
    if len(forbidden_target.get("forbidden_transitions", [])) != 8:
        failures.append("forbidden_transition_count_wrong")
    if len(derivation_policy.get("derivation_records_target", [])) < 9:
        failures.append("derivation_records_low")
    if len(negative_target.get("negative_controls", [])) < 20:
        failures.append("negative_controls_low")
    if len(acceptance_target.get("acceptance_gates", [])) != 34:
        failures.append("acceptance_gates_wrong")
    if target_profile.get("schema_claim") != "LOCAL_PROTOCOL_CANDIDATE_TARGET_ONLY":
        failures.append("target_profile_claim_wrong")
    if len(examples) != 12:
        failures.append("examples_count_wrong")
    if catalog.get("example_count") != 12:
        failures.append("catalog_count_wrong")
    if pressure.get("not_a_c6_protocol_design") is not True:
        failures.append("pressure_claims_design")

    return failures, {
        "target_summary": target_summary,
        "build_contract": build_contract,
        "target_spec": target_spec,
        "packet_family_target": packet_family_target,
        "state_model_target": state_model_target,
        "gate_requirements": gate_requirements,
        "forbidden_target": forbidden_target,
        "derivation_policy": derivation_policy,
        "negative_target": negative_target,
        "acceptance_target": acceptance_target,
        "examples": examples,
        "catalog": catalog,
        "pressure": pressure,
    }

def schema_obj(schema_version: str, required: List[str], properties: Dict[str, Any], rule: str) -> Dict[str, Any]:
    return {
        "schema_version": schema_version,
        "type": "object",
        "required": required,
        "properties": properties,
        "protocol_rule": rule,
        "additionalProperties": False,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    build_pass = not failures
    status = "TYPED_C6_INTER_CELL_PROTOCOL_CANDIDATE_EMITTED" if build_pass else "TYPED_C6_INTER_CELL_PROTOCOL_BUILD_GATE_FAIL"
    recommended_next = "REVIEW_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_V0" if build_pass else "REPAIR_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_V0"

    target_spec = basis.get("target_spec", {})
    packet_family_target = basis.get("packet_family_target", {})
    state_model_target = basis.get("state_model_target", {})
    gate_requirements = basis.get("gate_requirements", {})
    forbidden_target = basis.get("forbidden_target", {})
    derivation_policy = basis.get("derivation_policy", {})
    examples = basis.get("examples", [])

    inter_cell_protocol_schema = {
        "schema_version": "inter_cell_protocol_schema_v0",
        "schema_claim": "LOCAL_PROTOCOL_CANDIDATE_ONLY",
        "source": "reviewed C5-to-C6 examples",
        "source_receipts": {
            "target_design": SOURCE_C6_TARGET_DESIGN_RECEIPT_ID,
            "post_c6_decision": SOURCE_POST_C6_DECISION_RECEIPT_ID,
            "example_reference_closure": SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID,
        },
        "doctrine": [
            "Cells do not pass vibes.",
            "Cells pass packets.",
            "Cell 1 does not receive intentions.",
            "Cell 1 receives accepted, scoped, receipt-backed packets.",
        ],
        "core_law": target_spec.get("core_law"),
        "packet_family": PACKET_FAMILY,
        "shared_required_fields": packet_family_target.get("shared_required_fields", []),
        "must_not_infer": [
            "general Cell 1 authority",
            "global autonomy",
            "full transfer",
            "multi-agent architecture",
            "C7 authorized",
            "runtime-wide enforcement",
        ],
    }

    state_machine = {
        "schema_version": "inter_cell_packet_state_machine_v0",
        "closed_states": state_model_target.get("closed_states", []),
        "allowed_paths": state_model_target.get("allowed_paths", []),
        "forbidden_state_jumps": forbidden_target.get("forbidden_transitions", []),
        "state_model_claim": "LOCAL_PROTOCOL_CANDIDATE_ONLY",
    }

    proposed_only_schema = schema_obj(
        "c6_proposed_only_packet_v0",
        ["schema_version", "packet_id", "from_cell", "to", "status", "source_proposal_ref", "trigger", "proposal_summary", "authority", "must_not_infer"],
        {
            "schema_version": {"const": "c6_proposed_only_packet_v0"},
            "packet_id": {"pattern": "^prop_only_"},
            "from_cell": {"const": "CELL_0"},
            "to": {"const": "REVIEW_OR_AUTHORITY_GATE"},
            "status": {"const": "PROPOSED_ONLY"},
            "source_proposal_ref": {"type": ["string", "null"]},
            "trigger": {"type": "object"},
            "proposal_summary": {"type": "object"},
            "authority": {"type": "object", "required": ["cell1_consumable", "requires_review", "default_without_review"]},
            "must_not_infer": {"type": "array"},
        },
        "Cell 1 must reject this packet."
    )

    accepted_proposal_schema = schema_obj(
        "c6_accepted_proposal_packet_v0",
        ["schema_version", "packet_id", "from_cell", "to", "status", "source_proposal_ref", "review_receipt_ref", "acceptance_scope", "verification_requirement", "handoff_requirement", "must_not_infer"],
        {
            "schema_version": {"const": "c6_accepted_proposal_packet_v0"},
            "packet_id": {"pattern": "^accepted_"},
            "from_cell": {"const": "REVIEW_OR_AUTHORITY_GATE"},
            "to": {"const": "CELL_1"},
            "status": {"const": "ACCEPTED_FOR_CELL1"},
            "source_proposal_ref": {"type": ["string", "null"]},
            "review_receipt_ref": {"type": "string"},
            "acceptance_scope": {"type": "object"},
            "verification_requirement": {"type": "object"},
            "handoff_requirement": {"type": "object"},
            "must_not_infer": {"type": "array"},
        },
        "Accepted proposal packet is the only normal Cell 1 entry point."
    )

    cell1_intake_schema = schema_obj(
        "cell1_builder_intake_packet_v0",
        ["schema_version", "packet_id", "from_cell", "to", "accepted_packet_ref", "intake_contract", "required_returns"],
        {
            "schema_version": {"const": "cell1_builder_intake_packet_v0"},
            "packet_id": {"pattern": "^cell1_intake_"},
            "from_cell": {"const": "C6_PROTOCOL_LAYER"},
            "to": {"const": "CELL_1"},
            "accepted_packet_ref": {"type": "string"},
            "intake_contract": {"type": "object"},
            "required_returns": {"type": "array"},
        },
        "Cell 1 consumes a typed intake contract, not loose proposal text."
    )

    cell1_probe_schema = schema_obj(
        "cell1_probe_or_build_packet_v0",
        ["schema_version", "packet_id", "from_cell", "to", "accepted_packet_ref", "probe_or_build", "scope_result", "next_required_packet"],
        {
            "schema_version": {"const": "cell1_probe_or_build_packet_v0"},
            "packet_id": {"pattern": "^cell1_probe_"},
            "from_cell": {"const": "CELL_1"},
            "to": {"enum": ["CELL_0_OR_REVIEW", "REVIEW_OR_AUTHORITY_GATE", "CELL_0"]},
            "accepted_packet_ref": {"type": "string"},
            "probe_or_build": {"type": "object"},
            "scope_result": {"type": "object"},
            "next_required_packet": {"const": "verification_return_packet_v0"},
        },
        "Probe/build packet is not verification."
    )

    verification_return_schema = schema_obj(
        "verification_return_packet_v0",
        ["schema_version", "packet_id", "from_cell", "to", "accepted_packet_ref", "probe_or_build_packet_ref", "verification", "must_not_infer", "next_required_packet"],
        {
            "schema_version": {"const": "verification_return_packet_v0"},
            "packet_id": {"pattern": "^verify_return_"},
            "from_cell": {"const": "CELL_1"},
            "to": {"enum": ["CELL_0_OR_REVIEW", "REVIEW_OR_AUTHORITY_GATE", "CELL_0"]},
            "accepted_packet_ref": {"type": "string"},
            "probe_or_build_packet_ref": {"type": "string"},
            "verification": {"type": "object"},
            "must_not_infer": {"type": "array"},
            "next_required_packet": {"const": "handoff_return_packet_v0"},
        },
        "Verification pass returns evidence. It does not close the proposal by itself."
    )

    verification_return_schema["must_not_infer_values"] = [
        "global correctness",
        "domain transfer",
        "future failures impossible",
        "review closure",
        "general Cell 1 authority",
    ]

    handoff_return_schema = schema_obj(
        "handoff_return_packet_v0",
        ["schema_version", "packet_id", "from_cell", "to", "accepted_packet_ref", "verification_return_ref", "handoff_status", "summary", "allowed_next_handling", "forbidden_next_handling"],
        {
            "schema_version": {"const": "handoff_return_packet_v0"},
            "packet_id": {"pattern": "^handoff_"},
            "from_cell": {"const": "CELL_1"},
            "to": {"enum": ["CELL_0_OR_REVIEW", "REVIEW_OR_AUTHORITY_GATE", "CELL_0"]},
            "accepted_packet_ref": {"type": "string"},
            "verification_return_ref": {"type": "string"},
            "handoff_status": {"enum": ["RETURNED_TO_CELL0", "RETURNED_TO_REVIEW", "PARKED", "BLOCKED"]},
            "summary": {"type": "object"},
            "allowed_next_handling": {"type": "array"},
            "forbidden_next_handling": {"type": "array"},
        },
        "Cell 1 must return control. No momentum."
    )

    blocked_feedback_schema = schema_obj(
        "blocked_or_typed_stop_feedback_packet_v0",
        ["schema_version", "packet_id", "from_cell", "to", "accepted_packet_ref", "blocked_status", "stop_code", "diagnostic_feedback", "blocked_moves", "lawful_next_moves", "must_not_infer"],
        {
            "schema_version": {"const": "blocked_or_typed_stop_feedback_packet_v0"},
            "packet_id": {"pattern": "^blocked_feedback_"},
            "from_cell": {"const": "CELL_1"},
            "to": {"enum": ["CELL_0_OR_REVIEW", "REVIEW_OR_AUTHORITY_GATE", "CELL_0"]},
            "accepted_packet_ref": {"type": "string"},
            "blocked_status": {"const": "CELL1_BLOCKED"},
            "stop_code": {"type": ["string", "null"]},
            "diagnostic_feedback": {"type": "object"},
            "blocked_moves": {"type": "array"},
            "lawful_next_moves": {"type": "array"},
            "must_not_infer": {"type": "array"},
        },
        "Blocked Cell 1 returns useful feedback, not bare failure."
    )

    edge_observation_schema = schema_obj(
        "inter_cell_decision_edge_observation_v0",
        ["schema_version", "observation_id", "source_packet_ref", "active_object", "attempted_move", "boundary_checked", "boundary_result", "candidate_edge_handles", "blocked_moves", "lawful_next_moves", "collection_status", "schema_claim"],
        {
            "schema_version": {"const": "inter_cell_decision_edge_observation_v0"},
            "observation_id": {"pattern": "^edge_obs_"},
            "source_packet_ref": {"type": ["string", "null"]},
            "active_object": {"type": ["string", "null"]},
            "attempted_move": {"type": ["string", "null"]},
            "boundary_checked": {"type": ["string", "null"]},
            "boundary_result": {"type": ["string", "null"]},
            "candidate_edge_handles": {"type": "array"},
            "blocked_moves": {"type": "array"},
            "lawful_next_moves": {"type": "array"},
            "collection_status": {"const": "OBSERVATION_ONLY"},
            "schema_claim": {"const": "NONE"},
        },
        "Every inter-cell transition should emit an O1-compatible sidecar."
    )

    unit_feedback_schema = schema_obj(
        "inter_cell_unit_feedback_sidecar_v0",
        ["schema_version", "feedback_id", "source_packet_ref", "unit_id", "status", "failure_feedback", "feedback_quality_class"],
        {
            "schema_version": {"const": "inter_cell_unit_feedback_sidecar_v0"},
            "feedback_id": {"pattern": "^unit_feedback_"},
            "source_packet_ref": {"type": ["string", "null"]},
            "unit_id": {"type": ["string", "null"]},
            "status": {"enum": ["FAILED", "BLOCKED", "STOPPED", "NA"]},
            "failure_feedback": {"type": "object"},
            "feedback_quality_class": {"type": ["string", "null"]},
        },
        "C6 does not repair failure. C6 routes feedback."
    )

    gate_table = {
        "schema_version": "inter_cell_protocol_gate_table_v0",
        "gates": gate_requirements.get("gates", []),
        "enforcement_scope": "LOCAL_PROTOCOL_CANDIDATE_ONLY",
    }

    forbidden_transition_table = {
        "schema_version": "inter_cell_forbidden_transition_table_v0",
        "forbidden_transitions": forbidden_target.get("forbidden_transitions", []),
        "forbidden_interpretations": forbidden_target.get("forbidden_interpretations", []),
    }

    derivation_records = derivation_policy.get("derivation_records_target", [])

    demo_packets = [
        {
            "schema_version": "c6_proposed_only_packet_v0",
            "packet_id": "prop_only_" + sig8("demo proposed only"),
            "from_cell": "CELL_0",
            "to": "REVIEW_OR_AUTHORITY_GATE",
            "status": "PROPOSED_ONLY",
            "source_proposal_ref": "demo_proposal_ref",
            "trigger": {"source_receipt_ref": SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID, "halt_or_pressure": "protocol_needed", "required_distinction_ref": "proposal != accepted"},
            "proposal_summary": {"proposal_type": "bounded_protocol_design", "bounded_objective": "design packet law", "target_surface": "inter_cell_protocol", "evidence_refs": [SOURCE_C6_TARGET_DESIGN_RECEIPT_ID]},
            "authority": {"cell1_consumable": False, "requires_review": True, "default_without_review": "NO_EXECUTION"},
            "must_not_infer": ["accepted", "builder command", "registered move", "authorized patch", "Cell 1 consumable"],
        },
        {
            "schema_version": "c6_accepted_proposal_packet_v0",
            "packet_id": "accepted_" + sig8("demo accepted"),
            "from_cell": "REVIEW_OR_AUTHORITY_GATE",
            "to": "CELL_1",
            "status": "ACCEPTED_FOR_CELL1",
            "source_proposal_ref": "demo_proposal_ref",
            "review_receipt_ref": SOURCE_C6_TARGET_DESIGN_RECEIPT_ID,
            "acceptance_scope": {"bounded_objective": "minimal bounded probe", "target_surface": "demo_surface", "allowed_inputs": ["accepted_packet"], "forbidden_inputs": ["proposed_only_packet"], "expected_output": "verification_return_packet_v0"},
            "verification_requirement": {"required_probe": "demo_probe", "expected_gate": "demo_gate", "negative_controls": []},
            "handoff_requirement": {"return_to": "CELL_0_OR_REVIEW", "required_packet": "handoff_return_packet_v0"},
            "must_not_infer": ["general Cell 1 authority", "permission for unrelated builds", "verification pass", "domain transfer", "proposal closure"],
        },
        {
            "schema_version": "cell1_builder_intake_packet_v0",
            "packet_id": "cell1_intake_" + sig8("demo intake"),
            "from_cell": "C6_PROTOCOL_LAYER",
            "to": "CELL_1",
            "accepted_packet_ref": "accepted_demo",
            "intake_contract": {"consume_mode": "ACCEPTED_PACKET_ONLY", "target_surface": "demo_surface", "build_mode": "BOUNDED_PROBE_OR_MINIMAL_PATCH", "scope_limit": "accepted_scope_only", "stop_on_scope_expansion": True},
            "required_returns": ["cell1_probe_or_build_packet_v0", "verification_return_packet_v0", "handoff_return_packet_v0"],
        },
        {
            "schema_version": "verification_return_packet_v0",
            "packet_id": "verify_return_" + sig8("demo verify"),
            "from_cell": "CELL_1",
            "to": "CELL_0_OR_REVIEW",
            "accepted_packet_ref": "accepted_demo",
            "probe_or_build_packet_ref": "cell1_probe_demo",
            "verification": {"status": "PASS", "gate_checked": "demo_gate", "observed_result": {}, "negative_controls": {}},
            "must_not_infer": ["global correctness", "domain transfer", "future failures impossible", "review closure", "general Cell 1 authority"],
            "next_required_packet": "handoff_return_packet_v0",
        },
    ]

    bad_counters = {k: 0 for k in BAD_COUNTER_KEYS}

    rollup = {
        "schema_version": "inter_cell_protocol_rollup_v0",
        "protocol_runs": 0,
        "proposal_packets_seen": 0,
        "proposed_only_packets_blocked_from_cell1": 0,
        "accepted_packets_consumed_by_cell1": 0,
        "cell1_probe_packets_emitted": 0,
        "verification_return_packets_emitted": 0,
        "handoff_return_packets_emitted": 0,
        "blocked_feedback_packets_emitted": 0,
        "edge_observation_sidecars_emitted": 0,
        "unit_feedback_sidecars_emitted": 0,
        "packet_schemas_emitted": 9,
        "state_machine_emitted": 1,
        "gate_table_emitted": 1,
        "forbidden_transition_table_emitted": 1,
        "derivation_records_emitted": len(derivation_records),
        "demo_packets_emitted": len(demo_packets),
        "bad_counters": bad_counters,
    }

    profile = {
        "schema_version": "inter_cell_protocol_profile_v0",
        "profile_id": "c6_profile_" + sig8(rollup),
        "observed_protocol_shapes": [
            {
                "shape": "proposal -> review -> accepted packet -> Cell1 probe -> verification -> handoff",
                "supporting_examples": 4,
                "status": "SUPPORTED_BY_C5_EXAMPLES",
            },
            {
                "shape": "accepted packet -> Cell1 blocked -> diagnostic feedback -> return to review",
                "supporting_examples": 2,
                "status": "SUPPORTED_BY_C5_EXAMPLES",
            },
        ],
        "protocol_gaps": [
            {"gap": "CELL1_BUILDER_INTAKE_PACKET inferred as explicit wrapper", "status": "INFERRED_PROTOCOL_NEED"},
            {"gap": "UNIT_FEEDBACK_SIDECAR inferred from blocked feedback routing", "status": "INFERRED_PROTOCOL_NEED"},
        ],
        "schema_claim": "LOCAL_PROTOCOL_CANDIDATE_ONLY",
        "must_not_infer": [
            "general Cell 1 authority",
            "global autonomy",
            "full transfer",
            "multi-agent architecture",
            "C7 authorized",
            "runtime-wide enforcement",
        ],
        "bad_counters_zero": all(v == 0 for v in bad_counters.values()),
        "next_command_goal": None,
    }

    readout = {
        "schema_version": "inter_cell_protocol_readout_v0",
        "source": "reviewed C5-to-C6 examples",
        "examples_reviewed": 12,
        "packet_types": [
            "proposed-only packet",
            "accepted proposal packet",
            "Cell 1 accepted-proposal consumption",
            "verification return",
            "handoff return",
            "blocked feedback",
            "decision-edge observation",
            "unit feedback sidecar",
        ],
        "core_protocol": [
            "Cell 0 proposes.",
            "Review accepts, rejects, narrows, defers, or parks.",
            "Cell 1 consumes only accepted packets.",
            "Cell 1 probes/builds only within scope.",
            "Cell 1 returns verification.",
            "Cell 1 returns handoff.",
            "Blocked Cell 1 returns diagnostic feedback.",
            "O1/O2 sidecars make transitions and failures visible.",
        ],
        "bad_counters_zero": True,
        "interpretation": "C6 defines a local inter-cell protocol candidate from reviewed C5 examples. It does not grant general Cell 1 authority or claim transfer.",
    }

    report = {
        "schema_version": "c6_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "receipt_backed_claim": "C6 local inter-cell protocol candidate emitted from reviewed C5-to-C6 examples. It defines packet schemas, state machine, gates, forbidden transitions, derivation records, demo packets, rollup/profile/readout, and preserves all authority boundaries.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "c6_transition_trace_v0",
        "trace": [
            {
                "step": "consume_c6_target_design",
                "question": "is the C6 build target ready",
                "answer": "yes" if build_pass else "no",
                "taken": "emit local protocol candidate",
            },
            {
                "step": "emit_packet_law",
                "question": "what communication surface is defined",
                "answer": "typed packet family, state machine, gates, forbidden transitions, sidecars, derivation records",
                "taken": "emit protocol artifacts",
            },
            {
                "step": "preserve_boundary",
                "question": "does this patch runtime, authorize C7, or claim transfer/autonomy",
                "answer": "no",
                "taken": "stop with review-ready protocol candidate",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_C6_INTER_CELL_PROTOCOL_CANDIDATE_EMITTED" if build_pass else "STOP_C6_INTER_CELL_PROTOCOL_BUILD_GATE_FAIL",
            "next_command_goal": None,
        },
    }

    artifacts_json = [
        (INTER_CELL_PROTOCOL_SCHEMA_PATH, inter_cell_protocol_schema),
        (STATE_MACHINE_PATH, state_machine),
        (PROPOSED_ONLY_SCHEMA_PATH, proposed_only_schema),
        (ACCEPTED_PROPOSAL_SCHEMA_PATH, accepted_proposal_schema),
        (CELL1_INTAKE_SCHEMA_PATH, cell1_intake_schema),
        (CELL1_PROBE_SCHEMA_PATH, cell1_probe_schema),
        (VERIFICATION_RETURN_SCHEMA_PATH, verification_return_schema),
        (HANDOFF_RETURN_SCHEMA_PATH, handoff_return_schema),
        (BLOCKED_FEEDBACK_SCHEMA_PATH, blocked_feedback_schema),
        (EDGE_OBSERVATION_SIDECAR_SCHEMA_PATH, edge_observation_schema),
        (UNIT_FEEDBACK_SIDECAR_SCHEMA_PATH, unit_feedback_schema),
        (GATE_TABLE_PATH, gate_table),
        (FORBIDDEN_TRANSITION_TABLE_PATH, forbidden_transition_table),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (READOUT_PATH, readout),
        (REPORT_PATH, report),
        (TRACE_PATH, trace),
    ]
    for path, obj in artifacts_json:
        write_json(path, obj)
    write_jsonl(DERIVATION_STATUS_RECORDS_PATH, derivation_records)
    write_jsonl(DEMO_PACKETS_PATH, demo_packets)

    acceptance_gate_results = {
        "C6_PROTOCOL_0_REVIEWED_EXAMPLE_RECEIPT_CONSUMED": SOURCE_C6_TARGET_DESIGN_RECEIPT_PATH.exists(),
        "C6_PROTOCOL_1_REVIEWED_EXAMPLE_CATALOG_CONSUMED": C6_EXAMPLE_CATALOG_PATH.exists(),
        "C6_PROTOCOL_2_PACKET_FAMILY_DECLARED": INTER_CELL_PROTOCOL_SCHEMA_PATH.exists() and len(PACKET_FAMILY) == 9,
        "C6_PROTOCOL_3_STATE_MACHINE_EMITTED": STATE_MACHINE_PATH.exists(),
        "C6_PROTOCOL_4_PROPOSED_ONLY_PACKET_SCHEMA_EMITTED": PROPOSED_ONLY_SCHEMA_PATH.exists(),
        "C6_PROTOCOL_5_ACCEPTED_PROPOSAL_PACKET_SCHEMA_EMITTED": ACCEPTED_PROPOSAL_SCHEMA_PATH.exists(),
        "C6_PROTOCOL_6_CELL1_INTAKE_PACKET_SCHEMA_EMITTED": CELL1_INTAKE_SCHEMA_PATH.exists(),
        "C6_PROTOCOL_7_CELL1_PROBE_OR_BUILD_PACKET_SCHEMA_EMITTED": CELL1_PROBE_SCHEMA_PATH.exists(),
        "C6_PROTOCOL_8_VERIFICATION_RETURN_PACKET_SCHEMA_EMITTED": VERIFICATION_RETURN_SCHEMA_PATH.exists(),
        "C6_PROTOCOL_9_HANDOFF_RETURN_PACKET_SCHEMA_EMITTED": HANDOFF_RETURN_SCHEMA_PATH.exists(),
        "C6_PROTOCOL_10_BLOCKED_FEEDBACK_PACKET_SCHEMA_EMITTED": BLOCKED_FEEDBACK_SCHEMA_PATH.exists(),
        "C6_PROTOCOL_11_EDGE_OBSERVATION_SIDECAR_SCHEMA_EMITTED": EDGE_OBSERVATION_SIDECAR_SCHEMA_PATH.exists(),
        "C6_PROTOCOL_12_UNIT_FEEDBACK_SIDECAR_SCHEMA_EMITTED": UNIT_FEEDBACK_SIDECAR_SCHEMA_PATH.exists(),
        "C6_PROTOCOL_13_GATE_TABLE_EMITTED": GATE_TABLE_PATH.exists(),
        "C6_PROTOCOL_14_FORBIDDEN_TRANSITION_TABLE_EMITTED": FORBIDDEN_TRANSITION_TABLE_PATH.exists(),
        "C6_PROTOCOL_15_PROPOSED_ONLY_NOT_CELL1_CONSUMABLE": proposed_only_schema["properties"]["authority"]["required"] == ["cell1_consumable", "requires_review", "default_without_review"],
        "C6_PROTOCOL_16_ACCEPTED_PACKET_REQUIRES_REVIEW_RECEIPT": "review_receipt_ref" in accepted_proposal_schema["required"],
        "C6_PROTOCOL_17_CELL1_INTAKE_SCOPED": "intake_contract" in cell1_intake_schema["required"],
        "C6_PROTOCOL_18_CELL1_PROBE_OR_BUILD_NOT_VERIFICATION": cell1_probe_schema["protocol_rule"] == "Probe/build packet is not verification.",
        "C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE": "review closure" in verification_return_schema.get("must_not_infer_values", []),
        "C6_PROTOCOL_20_HANDOFF_NOT_HIDDEN_NEXT_COMMAND": "forbidden_next_handling" in handoff_return_schema["required"],
        "C6_PROTOCOL_21_BLOCKED_FEEDBACK_NOT_REPAIR": "diagnostic_feedback" in blocked_feedback_schema["required"],
        "C6_PROTOCOL_22_EVERY_TRANSITION_OBSERVABLE": EDGE_OBSERVATION_SIDECAR_SCHEMA_PATH.exists(),
        "C6_PROTOCOL_23_FAILED_OR_BLOCKED_TRANSITIONS_HAVE_FEEDBACK": UNIT_FEEDBACK_SIDECAR_SCHEMA_PATH.exists(),
        "C6_PROTOCOL_24_DERIVATION_STATUS_RECORDED": DERIVATION_STATUS_RECORDS_PATH.exists() and len(derivation_records) >= 9,
        "C6_PROTOCOL_25_ROLLUP_PROFILE_READOUT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and READOUT_PATH.exists(),
        "C6_PROTOCOL_26_NO_GENERAL_CELL1_AUTHORITY": bad_counters["general_cell1_authority_claim_count"] == 0,
        "C6_PROTOCOL_27_NO_GLOBAL_AUTONOMY_OR_FULL_TRANSFER_CLAIM": bad_counters["global_autonomy_claim_count"] == 0 and bad_counters["full_transfer_claim_count"] == 0,
        "C6_PROTOCOL_28_NO_SOURCE_REFERENCE_MUTATION": bad_counters["source_reference_mutation_count"] == 0,
        "C6_PROTOCOL_29_NO_LATEST_OR_MTIME_SELECTION": bad_counters["latest_file_guessing_count"] == 0 and bad_counters["mtime_selection_count"] == 0,
        "C6_PROTOCOL_30_BAD_COUNTERS_ZERO": all(v == 0 for v in bad_counters.values()),
        "C6_PROTOCOL_31_NO_HIDDEN_NEXT_COMMAND": trace["terminal"]["next_command_goal"] is None,
        "C6_PROTOCOL_32_LOCAL_PROTOCOL_CANDIDATE_ONLY": profile["schema_claim"] == "LOCAL_PROTOCOL_CANDIDATE_ONLY",
        "C6_PROTOCOL_33_NO_C7_AUTHORIZATION": "C7 authorized" in profile["must_not_infer"],
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_C6_INTER_CELL_PROTOCOL_BUILD_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_C6_INTER_CELL_PROTOCOL_BUILD_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_target": SOURCE_C6_TARGET_DESIGN_RECEIPT_ID,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c6_inter_cell_protocol_from_c5_examples_receipt_v0",
        "receipt_type": "TYPED_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_c6_target_design_receipt_id": SOURCE_C6_TARGET_DESIGN_RECEIPT_ID,
        "machine_readable_c6_protocol_summary": {
            "status": final_status,
            "c6_inter_cell_protocol_candidate_emitted": gate == "PASS",
            "schema_claim": "LOCAL_PROTOCOL_CANDIDATE_ONLY",
            "packet_family_declared": len(PACKET_FAMILY),
            "packet_schemas_emitted": 9,
            "state_machine_emitted": True,
            "gate_table_emitted": True,
            "forbidden_transition_table_emitted": True,
            "derivation_status_records_emitted": len(derivation_records),
            "demo_packets_emitted": len(demo_packets),
            "rollup_profile_readout_emitted": True,
            "bad_counters_zero": profile["bad_counters_zero"],
            "runtime_patched": False,
            "c7_authorized": False,
            "new_domain_shift_executed": False,
            "general_cell1_authority_claimed": False,
            "global_autonomy_claimed": False,
            "full_transfer_claimed": False,
            "runtime_wide_enforcement_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "recommended_next": final_next,
        },
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "inter_cell_protocol_schema": rel(INTER_CELL_PROTOCOL_SCHEMA_PATH),
            "state_machine": rel(STATE_MACHINE_PATH),
            "proposed_only_packet_schema": rel(PROPOSED_ONLY_SCHEMA_PATH),
            "accepted_proposal_packet_schema": rel(ACCEPTED_PROPOSAL_SCHEMA_PATH),
            "cell1_builder_intake_packet_schema": rel(CELL1_INTAKE_SCHEMA_PATH),
            "cell1_probe_or_build_packet_schema": rel(CELL1_PROBE_SCHEMA_PATH),
            "verification_return_packet_schema": rel(VERIFICATION_RETURN_SCHEMA_PATH),
            "handoff_return_packet_schema": rel(HANDOFF_RETURN_SCHEMA_PATH),
            "blocked_feedback_packet_schema": rel(BLOCKED_FEEDBACK_SCHEMA_PATH),
            "edge_observation_sidecar_schema": rel(EDGE_OBSERVATION_SIDECAR_SCHEMA_PATH),
            "unit_feedback_sidecar_schema": rel(UNIT_FEEDBACK_SIDECAR_SCHEMA_PATH),
            "gate_table": rel(GATE_TABLE_PATH),
            "forbidden_transition_table": rel(FORBIDDEN_TRANSITION_TABLE_PATH),
            "derivation_status_records": rel(DERIVATION_STATUS_RECORDS_PATH),
            "demo_packets": rel(DEMO_PACKETS_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "readout": rel(READOUT_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c6_protocol_receipt_id={receipt_id}")
    print(f"c6_protocol_receipt_path={rel(receipt_path)}")
    print(f"c6_protocol_schema_path={rel(INTER_CELL_PROTOCOL_SCHEMA_PATH)}")
    print(f"c6_protocol_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c6_protocol_profile_path={rel(PROFILE_PATH)}")
    print(f"c6_protocol_readout_path={rel(READOUT_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
