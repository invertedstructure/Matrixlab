#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DESIGN_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_TARGET_V0"
TARGET_UNIT_ID = "inter_cell.protocol_from_c5_examples.target.v0"
LAYER = "BRIDGE / INTER_CELL_PROTOCOL / TARGET_DESIGN"
MODE = "DESIGN_ONLY / TARGET_SPEC / NO_PROTOCOL_BUILD"
BUILD_MODE = "C6_INTER_CELL_PROTOCOL_TARGET_DESIGN_ONLY"

SOURCE_POST_C6_DECISION_RECEIPT_ID = "89b2d2cc"
SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID = "fe882749"

SOURCE_POST_C6_DECISION_RECEIPT_PATH = ROOT / "data/c6_post_example_reference_decision_v0_receipts/89b2d2cc.json"

POST_C6_DECISION_BASIS_PATH = ROOT / "data/c6_post_example_reference_decision_v0/c6_post_example_reference_decision_basis_v0.json"
POST_C6_SELECTED_BRANCH_PATH = ROOT / "data/c6_post_example_reference_decision_v0/c6_post_example_reference_selected_branch_v0.json"
C6_TARGET_DESIGN_AUTH_PATH = ROOT / "data/c6_post_example_reference_decision_v0/c6_protocol_target_design_authorization_from_reviewed_examples_v0.json"
C6_OBJECTIVE_BINDING_PATH = ROOT / "data/c6_post_example_reference_decision_v0/c6_inter_cell_protocol_objective_binding_v0.json"
C6_TARGET_DESIGN_SEED_PATH = ROOT / "data/c6_post_example_reference_decision_v0/c6_inter_cell_protocol_target_design_seed_v0.json"
POST_C6_AUTHORITY_PATH = ROOT / "data/c6_post_example_reference_decision_v0/c6_post_example_reference_decision_authority_boundary_v0.json"
POST_C6_CLASSIFICATION_PATH = ROOT / "data/c6_post_example_reference_decision_v0/c6_post_example_reference_decision_classification_v0.json"
POST_C6_ROLLUP_PATH = ROOT / "data/c6_post_example_reference_decision_v0/c6_post_example_reference_decision_rollup_v0.json"
POST_C6_PROFILE_PATH = ROOT / "data/c6_post_example_reference_decision_v0/c6_post_example_reference_decision_profile_v0.json"
POST_C6_REPORT_PATH = ROOT / "data/c6_post_example_reference_decision_v0/c6_post_example_reference_decision_report.json"
POST_C6_TRACE_PATH = ROOT / "data/c6_post_example_reference_decision_v0/c6_post_example_reference_decision_transition_trace.json"

C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0_receipts/fe882749.json"
C6_EXAMPLE_REVIEWED_REFERENCE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_example_extraction_reviewed_reference_v0.json"
C6_EXAMPLE_SURFACE_REFERENCE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_inter_cell_example_surface_reference_v0.json"
C6_PROTOCOL_PRESSURE_REFERENCE_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_reference_closure_v0/c6_protocol_pressure_reference_non_design_v0.json"

C6_EXAMPLES_JSONL_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_examples_from_c5_v0.jsonl"
C6_EXAMPLE_CATALOG_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_example_catalog_v0.json"
C6_EXAMPLE_SCHEMA_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_inter_cell_protocol_example_schema_v0.json"
C6_PROTOCOL_PRESSURE_READOUT_PATH = ROOT / "data/c6_example_extraction_from_c5_reference_v0/c6_protocol_pressure_readout_from_c5_examples_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_POST_C6_DECISION_RECEIPT_PATH,
    POST_C6_DECISION_BASIS_PATH,
    POST_C6_SELECTED_BRANCH_PATH,
    C6_TARGET_DESIGN_AUTH_PATH,
    C6_OBJECTIVE_BINDING_PATH,
    C6_TARGET_DESIGN_SEED_PATH,
    POST_C6_AUTHORITY_PATH,
    POST_C6_CLASSIFICATION_PATH,
    POST_C6_ROLLUP_PATH,
    POST_C6_PROFILE_PATH,
    POST_C6_REPORT_PATH,
    POST_C6_TRACE_PATH,
    C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH,
    C6_EXAMPLE_REVIEWED_REFERENCE_PATH,
    C6_EXAMPLE_SURFACE_REFERENCE_PATH,
    C6_PROTOCOL_PRESSURE_REFERENCE_PATH,
    C6_EXAMPLES_JSONL_PATH,
    C6_EXAMPLE_CATALOG_PATH,
    C6_EXAMPLE_SCHEMA_PATH,
    C6_PROTOCOL_PRESSURE_READOUT_PATH,
]

OUT_DIR = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0"
RECEIPT_DIR = ROOT / "data/c6_inter_cell_protocol_target_from_c5_examples_v0_receipts"

TARGET_BASIS_PATH = OUT_DIR / "c6_inter_cell_protocol_target_basis_v0.json"
TARGET_SPEC_PATH = OUT_DIR / "c6_inter_cell_protocol_target_spec_v0.json"
PACKET_FAMILY_TARGET_PATH = OUT_DIR / "c6_inter_cell_protocol_packet_family_target_v0.json"
STATE_MODEL_TARGET_PATH = OUT_DIR / "c6_inter_cell_protocol_state_model_target_v0.json"
GATE_REQUIREMENTS_PATH = OUT_DIR / "c6_inter_cell_protocol_gate_requirements_v0.json"
FORBIDDEN_TRANSITION_TARGET_PATH = OUT_DIR / "c6_inter_cell_protocol_forbidden_transition_target_v0.json"
DERIVATION_POLICY_PATH = OUT_DIR / "c6_inter_cell_protocol_derivation_policy_v0.json"
NEGATIVE_CONTROL_TARGET_PATH = OUT_DIR / "c6_inter_cell_protocol_negative_control_target_v0.json"
OUTPUT_MANIFEST_TARGET_PATH = OUT_DIR / "c6_inter_cell_protocol_output_manifest_target_v0.json"
ACCEPTANCE_GATES_TARGET_PATH = OUT_DIR / "c6_inter_cell_protocol_acceptance_gates_target_v0.json"
BUILD_CONTRACT_PATH = OUT_DIR / "c6_inter_cell_protocol_build_contract_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "c6_inter_cell_protocol_target_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "c6_inter_cell_protocol_target_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "c6_inter_cell_protocol_target_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c6_inter_cell_protocol_target_profile_v0.json"
REPORT_PATH = OUT_DIR / "c6_inter_cell_protocol_target_report.json"
TRACE_PATH = OUT_DIR / "c6_inter_cell_protocol_target_transition_trace.json"

EXPECTED_DECISION_STATUS = "TYPED_C6_POST_EXAMPLE_REFERENCE_DECISION_SELECTED_PROTOCOL_TARGET_DESIGN_READY"
EXPECTED_DECISION_STOP = "STOP_TYPED_C6_POST_EXAMPLE_REFERENCE_DECISION_SELECTED_PROTOCOL_TARGET_DESIGN_READY"
EXPECTED_SELECTED_NEXT_UNIT = "DESIGN_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_TARGET_V0"
FUTURE_BUILD_UNIT = "BUILD_C6_INTER_CELL_PROTOCOL_FROM_C5_EXAMPLES_V0"
RECOMMENDED_NEXT = FUTURE_BUILD_UNIT

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

SUPPORTED_EXAMPLE_TYPES = [
    "ACCEPTED_PROPOSAL_PACKET",
    "BLOCKED_OR_TYPED_STOP_FEEDBACK",
    "CELL1_ACCEPTED_PROPOSAL_CONSUMPTION",
    "DECISION_EDGE_OBSERVATION",
    "HANDOFF_RETURN_TO_CELL0",
    "PROPOSAL_PACKET_PROPOSED_ONLY",
    "VERIFICATION_RETURN",
]

ACCEPTANCE_GATES = [
    "C6_PROTOCOL_0_REVIEWED_EXAMPLE_RECEIPT_CONSUMED",
    "C6_PROTOCOL_1_REVIEWED_EXAMPLE_CATALOG_CONSUMED",
    "C6_PROTOCOL_2_PACKET_FAMILY_DECLARED",
    "C6_PROTOCOL_3_STATE_MACHINE_EMITTED",
    "C6_PROTOCOL_4_PROPOSED_ONLY_PACKET_SCHEMA_EMITTED",
    "C6_PROTOCOL_5_ACCEPTED_PROPOSAL_PACKET_SCHEMA_EMITTED",
    "C6_PROTOCOL_6_CELL1_INTAKE_PACKET_SCHEMA_EMITTED",
    "C6_PROTOCOL_7_CELL1_PROBE_OR_BUILD_PACKET_SCHEMA_EMITTED",
    "C6_PROTOCOL_8_VERIFICATION_RETURN_PACKET_SCHEMA_EMITTED",
    "C6_PROTOCOL_9_HANDOFF_RETURN_PACKET_SCHEMA_EMITTED",
    "C6_PROTOCOL_10_BLOCKED_FEEDBACK_PACKET_SCHEMA_EMITTED",
    "C6_PROTOCOL_11_EDGE_OBSERVATION_SIDECAR_SCHEMA_EMITTED",
    "C6_PROTOCOL_12_UNIT_FEEDBACK_SIDECAR_SCHEMA_EMITTED",
    "C6_PROTOCOL_13_GATE_TABLE_EMITTED",
    "C6_PROTOCOL_14_FORBIDDEN_TRANSITION_TABLE_EMITTED",
    "C6_PROTOCOL_15_PROPOSED_ONLY_NOT_CELL1_CONSUMABLE",
    "C6_PROTOCOL_16_ACCEPTED_PACKET_REQUIRES_REVIEW_RECEIPT",
    "C6_PROTOCOL_17_CELL1_INTAKE_SCOPED",
    "C6_PROTOCOL_18_CELL1_PROBE_OR_BUILD_NOT_VERIFICATION",
    "C6_PROTOCOL_19_VERIFICATION_NOT_CLOSURE",
    "C6_PROTOCOL_20_HANDOFF_NOT_HIDDEN_NEXT_COMMAND",
    "C6_PROTOCOL_21_BLOCKED_FEEDBACK_NOT_REPAIR",
    "C6_PROTOCOL_22_EVERY_TRANSITION_OBSERVABLE",
    "C6_PROTOCOL_23_FAILED_OR_BLOCKED_TRANSITIONS_HAVE_FEEDBACK",
    "C6_PROTOCOL_24_DERIVATION_STATUS_RECORDED",
    "C6_PROTOCOL_25_ROLLUP_PROFILE_READOUT_EMITTED",
    "C6_PROTOCOL_26_NO_GENERAL_CELL1_AUTHORITY",
    "C6_PROTOCOL_27_NO_GLOBAL_AUTONOMY_OR_FULL_TRANSFER_CLAIM",
    "C6_PROTOCOL_28_NO_SOURCE_REFERENCE_MUTATION",
    "C6_PROTOCOL_29_NO_LATEST_OR_MTIME_SELECTION",
    "C6_PROTOCOL_30_BAD_COUNTERS_ZERO",
    "C6_PROTOCOL_31_NO_HIDDEN_NEXT_COMMAND",
    "C6_PROTOCOL_32_LOCAL_PROTOCOL_CANDIDATE_ONLY",
    "C6_PROTOCOL_33_NO_C7_AUTHORIZATION",
]

BAD_COUNTERS = [
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
    "c7_authorized_count",
    "runtime_wide_enforcement_claim_count",
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

    decision_receipt = read_json(SOURCE_POST_C6_DECISION_RECEIPT_PATH)
    decision_summary = decision_receipt.get("machine_readable_c6_post_example_reference_decision_summary", {})
    selected_branch = read_json(POST_C6_SELECTED_BRANCH_PATH)
    target_auth = read_json(C6_TARGET_DESIGN_AUTH_PATH)
    objective_binding = read_json(C6_OBJECTIVE_BINDING_PATH)
    target_seed = read_json(C6_TARGET_DESIGN_SEED_PATH)
    post_authority = read_json(POST_C6_AUTHORITY_PATH)
    post_classification = read_json(POST_C6_CLASSIFICATION_PATH)
    post_rollup = read_json(POST_C6_ROLLUP_PATH)
    post_profile = read_json(POST_C6_PROFILE_PATH)

    closure_receipt = read_json(C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_PATH)
    closure_summary = closure_receipt.get("machine_readable_c6_example_reference_closure_summary", {})
    reviewed_reference = read_json(C6_EXAMPLE_REVIEWED_REFERENCE_PATH)
    surface_reference = read_json(C6_EXAMPLE_SURFACE_REFERENCE_PATH)
    pressure_reference = read_json(C6_PROTOCOL_PRESSURE_REFERENCE_PATH)

    examples = read_jsonl(C6_EXAMPLES_JSONL_PATH)
    catalog = read_json(C6_EXAMPLE_CATALOG_PATH)
    example_schema = read_json(C6_EXAMPLE_SCHEMA_PATH)
    pressure_readout = read_json(C6_PROTOCOL_PRESSURE_READOUT_PATH)

    if decision_receipt.get("receipt_id") != SOURCE_POST_C6_DECISION_RECEIPT_ID or decision_receipt.get("gate") != "PASS":
        failures.append("post_c6_decision_receipt_not_pass")
    if decision_receipt.get("terminal", {}).get("stop_code") != EXPECTED_DECISION_STOP:
        failures.append("post_c6_decision_stop_wrong")
    if decision_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("post_c6_decision_hidden_next")
    if decision_summary.get("status") != EXPECTED_DECISION_STATUS:
        failures.append(f"post_c6_decision_status_wrong:{decision_summary.get('status')}")
    if decision_summary.get("selected_next_unit") != EXPECTED_SELECTED_NEXT_UNIT:
        failures.append("post_c6_selected_next_wrong")
    if decision_summary.get("recommended_next") != EXPECTED_SELECTED_NEXT_UNIT:
        failures.append("post_c6_recommended_next_wrong")
    if decision_summary.get("future_build_unit") != FUTURE_BUILD_UNIT:
        failures.append("post_c6_future_build_wrong")
    if decision_summary.get("c6_protocol_target_design_authorized_next") is not True:
        failures.append("target_design_not_authorized")

    for key in [
        "c6_protocol_built_in_decision",
        "c6_protocol_emitted_in_decision",
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
        if decision_summary.get(key) is not False:
            failures.append(f"post_c6_forbidden_true:{key}")

    if selected_branch.get("selected_next_unit") != EXPECTED_SELECTED_NEXT_UNIT:
        failures.append("selected_branch_next_wrong")
    if target_auth.get("authorized_next_unit") != EXPECTED_SELECTED_NEXT_UNIT:
        failures.append("target_auth_next_wrong")
    if objective_binding.get("objective_status") != "BOUND_AS_TARGET_DESIGN_INPUT":
        failures.append("objective_not_bound")
    if target_seed.get("target_design_ready") is not True:
        failures.append("target_seed_not_ready")
    if target_seed.get("future_build_unit") != FUTURE_BUILD_UNIT:
        failures.append("target_seed_future_build_wrong")
    if post_authority.get("may_execute_c6_protocol_target_design_next") is not True:
        failures.append("post_authority_no_target_design")
    for forbidden in [
        "may_build_c6_protocol_now_in_decision",
        "may_emit_c6_protocol_now_in_decision",
        "may_patch_runtime_now_in_decision",
        "may_open_c7_now",
        "may_execute_new_domain_shift",
        "may_claim_full_transfer",
        "may_claim_global_autonomy",
        "may_claim_general_cell1_authority",
        "may_claim_runtime_wide_enforcement",
        "may_mutate_source",
        "may_mutate_prior_receipts",
        "may_mutate_c5_reference",
    ]:
        if post_authority.get(forbidden) is not False:
            failures.append(f"post_authority_forbidden_true:{forbidden}")
    if post_classification.get("next_command_goal") is not None:
        failures.append("post_classification_hidden_next")
    if post_rollup.get("selected_c6_protocol_target_design_count") != 1:
        failures.append("post_rollup_target_design_wrong")
    if post_profile.get("selected_next_unit") != EXPECTED_SELECTED_NEXT_UNIT:
        failures.append("post_profile_next_wrong")
    if post_profile.get("next_command_goal") is not None:
        failures.append("post_profile_hidden_next")

    if closure_receipt.get("receipt_id") != SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID or closure_receipt.get("gate") != "PASS":
        failures.append("closure_receipt_not_pass")
    if closure_summary.get("reviewed_reference_frozen") is not True:
        failures.append("closure_reference_not_frozen")
    if reviewed_reference.get("reference_status") != "C6_EXAMPLE_EXTRACTION_REVIEWED_REFERENCE_FROZEN":
        failures.append("reviewed_reference_not_frozen")
    if surface_reference.get("examples_count") != 12:
        failures.append("surface_reference_count_wrong")
    if pressure_reference.get("not_a_c6_protocol_design") is not True:
        failures.append("pressure_reference_claims_design")

    if len(examples) != 12:
        failures.append(f"examples_count_wrong:{len(examples)}")
    if catalog.get("example_count") != 12:
        failures.append("catalog_count_wrong")
    if sorted(catalog.get("example_types", [])) != SUPPORTED_EXAMPLE_TYPES:
        failures.append("catalog_types_wrong")
    if sorted(example_schema.get("closed_example_types", [])) != SUPPORTED_EXAMPLE_TYPES:
        failures.append("example_schema_types_wrong")
    if pressure_readout.get("not_a_c6_protocol_design") is not True:
        failures.append("pressure_readout_claims_design")

    return failures, {
        "decision_summary": decision_summary,
        "closure_summary": closure_summary,
        "examples": examples,
        "catalog": catalog,
        "pressure_readout": pressure_readout,
        "objective_binding": objective_binding,
        "target_seed": target_seed,
    }

def count_type(examples: List[Dict[str, Any]], typ: str) -> int:
    return sum(1 for ex in examples if ex.get("example_type") == typ)

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    design_pass = not failures
    status = "TYPED_C6_INTER_CELL_PROTOCOL_TARGET_DESIGNED_BUILD_READY" if design_pass else "TYPED_C6_INTER_CELL_PROTOCOL_TARGET_DESIGN_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if design_pass else "REPAIR_C6_INTER_CELL_PROTOCOL_TARGET_DESIGN_V0"

    closure_summary = basis.get("closure_summary", {})
    examples = basis.get("examples", [])
    catalog = basis.get("catalog", {})
    pressure_readout = basis.get("pressure_readout", {})
    objective_binding = basis.get("objective_binding", {})
    target_seed = basis.get("target_seed", {})

    reason_codes = [
        "C6_INTER_CELL_PROTOCOL_TARGET_DESIGNED",
        "POST_C6_DECISION_RECEIPT_CONSUMED",
        "REVIEWED_EXAMPLE_REFERENCE_CLOSURE_CONSUMED",
        "PACKET_LAW_OBJECTIVE_BOUND",
        "PACKET_FAMILY_TARGET_DECLARED",
        "STATE_MODEL_TARGET_DECLARED",
        "GATE_REQUIREMENTS_TARGET_DECLARED",
        "FORBIDDEN_TRANSITIONS_TARGET_DECLARED",
        "DERIVATION_POLICY_TARGET_DECLARED",
        "NEGATIVE_CONTROL_TARGET_DECLARED",
        "BUILD_CONTRACT_EMITTED",
        "FUTURE_BUILD_READY",
        "NO_C6_PROTOCOL_BUILT",
        "NO_C6_PROTOCOL_EMITTED",
        "NO_RUNTIME_PATCH",
        "NO_C7_AUTHORIZATION",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if design_pass else failures

    allowed_states = [
        "PROPOSED_ONLY", "UNDER_REVIEW", "ACCEPTED_FOR_CELL1", "REJECTED", "DEFERRED", "PARKED",
        "CELL1_INTAKE_READY", "CELL1_ACCEPTED_CONSUMPTION", "CELL1_BLOCKED", "CELL1_PROBED",
        "CELL1_VERIFIED_PASS", "CELL1_VERIFIED_FAIL", "RETURNED_TO_CELL0", "RETURNED_TO_REVIEW",
        "CLOSED_BY_REVIEW", "NEW_TYPED_EDGE",
    ]

    allowed_paths = [
        ["PROPOSED_ONLY", "UNDER_REVIEW", "ACCEPTED_FOR_CELL1", "CELL1_INTAKE_READY", "CELL1_ACCEPTED_CONSUMPTION", "CELL1_PROBED", "CELL1_VERIFIED_PASS", "RETURNED_TO_CELL0", "CLOSED_BY_REVIEW"],
        ["PROPOSED_ONLY", "UNDER_REVIEW", "REJECTED"],
        ["PROPOSED_ONLY", "UNDER_REVIEW", "DEFERRED"],
        ["PROPOSED_ONLY", "UNDER_REVIEW", "PARKED"],
        ["ACCEPTED_FOR_CELL1", "CELL1_INTAKE_READY", "CELL1_BLOCKED", "BLOCKED_OR_TYPED_STOP_FEEDBACK_PACKET", "RETURNED_TO_REVIEW"],
    ]

    forbidden_transitions = [
        "PROPOSED_ONLY -> CELL1_ACCEPTED_CONSUMPTION",
        "PROPOSED_ONLY -> CELL1_PROBED",
        "UNDER_REVIEW -> CELL1_ACCEPTED_CONSUMPTION",
        "CELL1_PROBED -> CLOSED_BY_REVIEW",
        "CELL1_VERIFIED_PASS -> GLOBAL_SUCCESS",
        "HANDOFF_RETURN -> NEXT_COMMAND",
        "BLOCKED_FEEDBACK -> REPAIR_APPLIED",
        "VERIFICATION_RETURN -> REVIEW_CLOSURE_WITHOUT_REVIEW",
    ]

    derivation_records = [
        {"element": "PROPOSAL_PACKET_PROPOSED_ONLY", "status": "SUPPORTED_BY_C5_EXAMPLES", "support_count": count_type(examples, "PROPOSAL_PACKET_PROPOSED_ONLY")},
        {"element": "ACCEPTED_PROPOSAL_PACKET", "status": "SUPPORTED_BY_C5_EXAMPLES", "support_count": count_type(examples, "ACCEPTED_PROPOSAL_PACKET")},
        {"element": "CELL1_BUILDER_INTAKE_PACKET", "status": "INFERRED_PROTOCOL_NEED", "support_count": count_type(examples, "CELL1_ACCEPTED_PROPOSAL_CONSUMPTION"), "reason": "Cell 1 needs an explicit intake wrapper for accepted scoped packets."},
        {"element": "CELL1_PROBE_OR_BUILD_PACKET", "status": "INFERRED_PROTOCOL_NEED", "support_count": count_type(examples, "CELL1_ACCEPTED_PROPOSAL_CONSUMPTION"), "reason": "Probe/build action must be distinguished from verification return."},
        {"element": "VERIFICATION_RETURN_PACKET", "status": "SUPPORTED_BY_C5_EXAMPLES", "support_count": count_type(examples, "VERIFICATION_RETURN")},
        {"element": "HANDOFF_RETURN_PACKET", "status": "SUPPORTED_BY_C5_EXAMPLES", "support_count": count_type(examples, "HANDOFF_RETURN_TO_CELL0")},
        {"element": "BLOCKED_OR_TYPED_STOP_FEEDBACK_PACKET", "status": "SUPPORTED_BY_C5_EXAMPLES", "support_count": count_type(examples, "BLOCKED_OR_TYPED_STOP_FEEDBACK")},
        {"element": "DECISION_EDGE_OBSERVATION_SIDECAR", "status": "SUPPORTED_BY_C5_EXAMPLES", "support_count": count_type(examples, "DECISION_EDGE_OBSERVATION")},
        {"element": "UNIT_FEEDBACK_SIDECAR", "status": "INFERRED_PROTOCOL_NEED", "support_count": count_type(examples, "BLOCKED_OR_TYPED_STOP_FEEDBACK"), "reason": "Blocked/failed units need a typed diagnostic sidecar for O2 feedback hardening."},
        {"element": "GENERAL_CELL1_AUTHORITY", "status": "FORBIDDEN_EXTENSION", "support_count": 0},
        {"element": "GLOBAL_AUTONOMY", "status": "FORBIDDEN_EXTENSION", "support_count": 0},
        {"element": "FULL_TRANSFER", "status": "FORBIDDEN_EXTENSION", "support_count": 0},
        {"element": "C7_AUTHORIZATION", "status": "FORBIDDEN_EXTENSION", "support_count": 0},
        {"element": "RUNTIME_WIDE_ENFORCEMENT", "status": "FORBIDDEN_EXTENSION", "support_count": 0},
    ]

    target_basis = {
        "schema_version": "c6_inter_cell_protocol_target_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if design_pass else "BASIS_REPAIR_REQUIRED",
        "source_post_c6_decision_receipt_id": SOURCE_POST_C6_DECISION_RECEIPT_ID,
        "source_c6_example_reference_closure_receipt_id": SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID,
        "examples_reviewed": closure_summary.get("examples_reviewed"),
        "example_types_reviewed": closure_summary.get("example_types_reviewed", []),
        "objective_doctrine": objective_binding.get("clean_doctrine", []),
        "target_design_seed_ref": rel(C6_TARGET_DESIGN_SEED_PATH),
        "target_design_ready": design_pass,
    }

    target_spec = {
        "schema_version": "c6_inter_cell_protocol_target_spec_v0",
        "target_status": status,
        "future_build_unit": FUTURE_BUILD_UNIT,
        "schema_claim": "LOCAL_PROTOCOL_CANDIDATE_TARGET_ONLY",
        "role": "Design the target for a local inter-cell packet-law protocol candidate derived from reviewed C5 examples.",
        "core_doctrine": [
            "Cells do not pass vibes.",
            "Cells pass packets.",
            "Cell 1 does not receive intentions.",
            "Cell 1 receives accepted, scoped, receipt-backed packets.",
        ],
        "core_law": objective_binding.get("core_law"),
        "required_packet_family": PACKET_FAMILY,
        "required_distinctions": objective_binding.get("must_preserve_distinctions", []),
        "success_means": [
            "inter-cell packet family exists",
            "state transitions are typed",
            "Cell 1 consumes only accepted scoped packets",
            "verification return is required",
            "handoff return is required",
            "blocked Cell 1 returns diagnostic feedback",
            "edge observations are required",
            "unit feedback sidecars are required",
            "bad counters are zero",
            "protocol is local candidate only",
        ],
        "success_does_not_mean": [
            "general multi-agent architecture exists",
            "Cell 1 has general authority",
            "transfer is proven",
            "autonomy is proven",
            "runtime-wide enforcement exists",
            "C7 is authorized",
        ],
    }

    packet_family_target = {
        "schema_version": "c6_inter_cell_protocol_packet_family_target_v0",
        "packet_family": PACKET_FAMILY,
        "shared_required_fields": [
            "schema_version",
            "packet_id",
            "from_cell",
            "to",
            "status",
            "source_refs",
            "authority_boundary",
            "scope_boundary",
            "must_not_infer",
            "next_required_packet_or_terminal",
        ],
        "normal_cell1_entrypoint": "ACCEPTED_PROPOSAL_PACKET",
        "non_consumable_by_cell1": ["PROPOSAL_PACKET_PROPOSED_ONLY"],
    }

    state_model_target = {
        "schema_version": "c6_inter_cell_protocol_state_model_target_v0",
        "closed_states": allowed_states,
        "allowed_paths": allowed_paths,
        "state_model_claim": "TARGET_FOR_BUILD_NOT_RUNTIME_EXECUTION",
    }

    gate_requirements = {
        "schema_version": "c6_inter_cell_protocol_gate_requirements_v0",
        "gates": [
            {"gate": "proposal_consumption_gate", "rule": "If packet.status != ACCEPTED_FOR_CELL1, Cell 1 consumption is forbidden."},
            {"gate": "review_basis_gate", "rule": "Accepted packet must cite review receipt."},
            {"gate": "scope_gate", "rule": "Cell 1 may touch only target surfaces named by accepted packet."},
            {"gate": "probe_build_report_gate", "rule": "Cell 1 must report what it actually did."},
            {"gate": "verification_gate", "rule": "Cell 1 must return verification packet after probe/build."},
            {"gate": "handoff_gate", "rule": "Cell 1 must return handoff packet after verification or block."},
            {"gate": "feedback_gate", "rule": "Blocked Cell 1 must emit useful feedback, not bare failure."},
            {"gate": "observation_gate", "rule": "Every inter-cell transition emits decision-edge observation sidecar."},
            {"gate": "unit_feedback_gate", "rule": "Failed, blocked, stopped, or NA units emit unit feedback sidecar."},
        ],
    }

    forbidden_transition_target = {
        "schema_version": "c6_inter_cell_protocol_forbidden_transition_target_v0",
        "forbidden_transitions": forbidden_transitions,
        "forbidden_interpretations": [
            "proposed-only packet as Cell 1 input",
            "probe/build as verification",
            "verification as closure",
            "handoff as hidden next command",
            "blocked feedback as repair",
            "accepted Cell 1 authority as general Cell 1 authority",
        ],
    }

    derivation_policy = {
        "schema_version": "c6_inter_cell_protocol_derivation_policy_v0",
        "allowed_statuses": ["SUPPORTED_BY_C5_EXAMPLES", "INFERRED_PROTOCOL_NEED", "UNSUPPORTED_EXTENSION", "FORBIDDEN_EXTENSION"],
        "rules": {
            "SUPPORTED_BY_C5_EXAMPLES": "May be included normally.",
            "INFERRED_PROTOCOL_NEED": "May be included only with explicit reason.",
            "UNSUPPORTED_EXTENSION": "Must be parked or question-packeted.",
            "FORBIDDEN_EXTENSION": "Must not enter protocol.",
        },
        "derivation_records_target": derivation_records,
    }

    negative_control_target = {
        "schema_version": "c6_inter_cell_protocol_negative_control_target_v0",
        "negative_controls_must_be_non_writing": True,
        "negative_controls": [
            "proposed_only_consumed_by_cell1_fail",
            "proposal_accepted_without_review_fail",
            "accepted_packet_without_review_receipt_fail",
            "cell1_consumed_unscoped_packet_fail",
            "cell1_scope_expansion_fail",
            "cell1_freebuild_fail",
            "cell1_auto_chain_fail",
            "probe_counted_as_verification_fail",
            "verification_counted_as_closure_fail",
            "handoff_counted_as_hidden_next_command_fail",
            "blocked_feedback_counted_as_repair_fail",
            "bare_failed_status_fail",
            "edge_observation_missing_fail",
            "unit_feedback_missing_fail",
            "general_cell1_authority_claim_fail",
            "global_autonomy_claim_fail",
            "full_transfer_claim_fail",
            "source_reference_mutation_fail",
            "latest_file_guessing_fail",
            "mtime_selection_fail",
            "hidden_next_command_fail",
            "c7_authorized_fail",
            "runtime_wide_enforcement_claim_fail",
        ],
    }

    output_manifest_target = {
        "schema_version": "c6_inter_cell_protocol_output_manifest_target_v0",
        "required_output_artifacts_for_future_build": [
            "inter_cell_protocol_schema_v0.json",
            "inter_cell_packet_state_machine_v0.json",
            "proposed_only_packet_schema_v0.json",
            "accepted_proposal_packet_schema_v0.json",
            "cell1_builder_intake_packet_schema_v0.json",
            "cell1_probe_or_build_packet_schema_v0.json",
            "verification_return_packet_schema_v0.json",
            "handoff_return_packet_schema_v0.json",
            "blocked_feedback_packet_schema_v0.json",
            "inter_cell_edge_observation_sidecar_schema_v0.json",
            "inter_cell_unit_feedback_sidecar_schema_v0.json",
            "inter_cell_protocol_gate_table_v0.json",
            "inter_cell_forbidden_transition_table_v0.json",
            "inter_cell_derivation_status_records_v0.jsonl",
            "inter_cell_protocol_demo_packets_v0.jsonl",
            "inter_cell_protocol_rollup_v0.json",
            "inter_cell_protocol_profile_v0.json",
            "inter_cell_protocol_readout_v0.json",
            "c6_report.json",
            "c6_transition_trace.json",
            "receipt",
        ],
    }

    acceptance_gates_target = {
        "schema_version": "c6_inter_cell_protocol_acceptance_gates_target_v0",
        "acceptance_gates": ACCEPTANCE_GATES,
    }

    build_contract = {
        "schema_version": "c6_inter_cell_protocol_build_contract_v0",
        "build_unit": FUTURE_BUILD_UNIT,
        "build_authorized_after_target_design": design_pass,
        "source_basis_required": [
            SOURCE_POST_C6_DECISION_RECEIPT_ID,
            SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID,
        ],
        "must_emit": output_manifest_target["required_output_artifacts_for_future_build"],
        "must_not_emit": [
            "runtime patches",
            "C7 execution artifacts",
            "general Cell 1 authority artifacts",
            "global autonomy claims",
            "full-transfer claims",
            "runtime-wide enforcement claims",
            "source reference mutations",
            "hidden next command",
        ],
        "terminal_success": {
            "type": "STOP",
            "stop_code": "STOP_C6_INTER_CELL_PROTOCOL_CANDIDATE_EMITTED",
            "next_command_goal": None,
        },
    }

    authority_boundary = {
        "schema_version": "c6_inter_cell_protocol_target_authority_boundary_v0",
        "status": status,
        "may_build_c6_protocol_candidate_next": design_pass,
        "may_emit_protocol_now_in_target_design": False,
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
        "schema_version": "c6_inter_cell_protocol_target_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "c6_protocol_target_designed": design_pass,
        "c6_protocol_build_ready": design_pass,
        "selected_build_unit": RECOMMENDED_NEXT if design_pass else None,
        "packet_family_declared": len(PACKET_FAMILY),
        "state_model_declared": True,
        "gate_requirements_declared": len(gate_requirements["gates"]),
        "forbidden_transitions_declared": len(forbidden_transitions),
        "derivation_records_declared": len(derivation_records),
        "acceptance_gates_declared": len(ACCEPTANCE_GATES),
        "negative_controls_declared": len(negative_control_target["negative_controls"]),
        "protocol_built_in_target_design": False,
        "protocol_emitted_in_target_design": False,
        "runtime_patched": False,
        "c7_authorized": False,
        "new_domain_shift_executed": False,
        "full_transfer_claimed": False,
        "global_autonomy_claimed": False,
        "general_cell1_authority_claimed": False,
        "runtime_wide_enforcement_claimed": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "c5_reference_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "c6_inter_cell_protocol_target_rollup_v0",
        "target_design_count": 1 if design_pass else 0,
        "c6_protocol_build_ready_count": 1 if design_pass else 0,
        "packet_family_count": len(PACKET_FAMILY),
        "state_model_target_count": 1,
        "gate_requirements_count": len(gate_requirements["gates"]),
        "forbidden_transition_count": len(forbidden_transitions),
        "derivation_record_count": len(derivation_records),
        "acceptance_gate_count": len(ACCEPTANCE_GATES),
        "negative_control_count": len(negative_control_target["negative_controls"]),
        "protocol_built_in_target_design_count": 0,
        "protocol_emitted_in_target_design_count": 0,
        "runtime_patched_count": 0,
        "c7_authorized_count": 0,
        "new_domain_shift_executed_count": 0,
        "full_transfer_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "general_cell1_authority_claim_count": 0,
        "runtime_wide_enforcement_claim_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "c5_reference_mutated_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "bad_counters": {k: 0 for k in BAD_COUNTERS},
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "protocol_built_in_target_design_count",
        "protocol_emitted_in_target_design_count",
        "runtime_patched_count",
        "c7_authorized_count",
        "new_domain_shift_executed_count",
        "full_transfer_claim_count",
        "global_autonomy_claim_count",
        "general_cell1_authority_claim_count",
        "runtime_wide_enforcement_claim_count",
        "source_mutated_count",
        "prior_receipt_mutated_count",
        "c5_reference_mutated_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "c6_inter_cell_protocol_target_profile_v0",
        "profile_id": "c6_protocol_target_" + sig8(rollup),
        "status": status,
        "schema_claim": "LOCAL_PROTOCOL_CANDIDATE_TARGET_ONLY",
        "observed_protocol_shapes_targeted": [
            {
                "shape": "proposal -> review -> accepted packet -> Cell1 probe -> verification -> handoff",
                "supporting_examples": count_type(examples, "ACCEPTED_PROPOSAL_PACKET") + count_type(examples, "CELL1_ACCEPTED_PROPOSAL_CONSUMPTION") + count_type(examples, "VERIFICATION_RETURN") + count_type(examples, "HANDOFF_RETURN_TO_CELL0"),
                "status": "SUPPORTED_BY_C5_EXAMPLES",
            },
            {
                "shape": "accepted packet -> Cell1 blocked -> diagnostic feedback -> return to review",
                "supporting_examples": count_type(examples, "BLOCKED_OR_TYPED_STOP_FEEDBACK"),
                "status": "SUPPORTED_BY_C5_EXAMPLES",
            },
        ],
        "protocol_gaps": [
            {
                "gap": "CELL1_BUILDER_INTAKE_PACKET is inferred as wrapper around accepted packet consumption.",
                "status": "INFERRED_PROTOCOL_NEED",
            },
            {
                "gap": "UNIT_FEEDBACK_SIDECAR is inferred from blocked/typed-stop feedback surface.",
                "status": "INFERRED_PROTOCOL_NEED",
            },
        ],
        "must_not_infer": [
            "general Cell 1 authority",
            "global autonomy",
            "full transfer",
            "multi-agent architecture",
            "C7 authorized",
            "runtime-wide enforcement",
        ],
        "bad_counters_zero": all(rollup[k] == 0 for k in zero_keys) and all(v == 0 for v in rollup["bad_counters"].values()),
        "next_command_goal": None,
    }

    report = {
        "schema_version": "c6_inter_cell_protocol_target_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "C6 inter-cell protocol target is designed from the reviewed C5-to-C6 example reference. The target specifies packet family, state model, gates, forbidden transitions, derivation policy, negative controls, and future build contract. It does not build or emit the protocol candidate, patch runtime, authorize C7, or claim transfer/autonomy/general Cell 1 authority.",
        "future_build_unit": recommended_next,
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "c6_inter_cell_protocol_target_transition_trace_v0",
        "trace": [
            {
                "step": "consume_post_c6_decision",
                "question": "is C6 protocol target design authorized next",
                "answer": "yes" if design_pass else "no",
                "taken": "consume reviewed example reference and objective binding",
            },
            {
                "step": "design_target_not_protocol",
                "question": "what is emitted",
                "answer": "target spec, packet family target, gates, forbidden transitions, derivation policy, negative controls, and build contract",
                "taken": "defer protocol candidate build to next unit",
            },
            {
                "step": "preserve_boundaries",
                "question": "does target design build protocol, patch runtime, or authorize C7",
                "answer": "no",
                "taken": "emit build-ready target",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (TARGET_BASIS_PATH, target_basis),
        (TARGET_SPEC_PATH, target_spec),
        (PACKET_FAMILY_TARGET_PATH, packet_family_target),
        (STATE_MODEL_TARGET_PATH, state_model_target),
        (GATE_REQUIREMENTS_PATH, gate_requirements),
        (FORBIDDEN_TRANSITION_TARGET_PATH, forbidden_transition_target),
        (DERIVATION_POLICY_PATH, derivation_policy),
        (NEGATIVE_CONTROL_TARGET_PATH, negative_control_target),
        (OUTPUT_MANIFEST_TARGET_PATH, output_manifest_target),
        (ACCEPTANCE_GATES_TARGET_PATH, acceptance_gates_target),
        (BUILD_CONTRACT_PATH, build_contract),
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
        "C6_TARGET_DESIGN_0_POST_C6_DECISION_RECEIPT_CONSUMED": SOURCE_POST_C6_DECISION_RECEIPT_PATH.exists(),
        "C6_TARGET_DESIGN_1_REVIEWED_EXAMPLE_REFERENCE_CONSUMED": C6_EXAMPLE_REVIEWED_REFERENCE_PATH.exists(),
        "C6_TARGET_DESIGN_2_TARGET_BASIS_EMITTED": TARGET_BASIS_PATH.exists(),
        "C6_TARGET_DESIGN_3_TARGET_SPEC_EMITTED": TARGET_SPEC_PATH.exists(),
        "C6_TARGET_DESIGN_4_PACKET_FAMILY_TARGET_EMITTED": PACKET_FAMILY_TARGET_PATH.exists() and len(PACKET_FAMILY) == 9,
        "C6_TARGET_DESIGN_5_STATE_MODEL_TARGET_EMITTED": STATE_MODEL_TARGET_PATH.exists() and len(allowed_states) == 16,
        "C6_TARGET_DESIGN_6_GATE_REQUIREMENTS_EMITTED": GATE_REQUIREMENTS_PATH.exists() and len(gate_requirements["gates"]) == 9,
        "C6_TARGET_DESIGN_7_FORBIDDEN_TRANSITIONS_EMITTED": FORBIDDEN_TRANSITION_TARGET_PATH.exists() and len(forbidden_transitions) == 8,
        "C6_TARGET_DESIGN_8_DERIVATION_POLICY_EMITTED": DERIVATION_POLICY_PATH.exists() and len(derivation_records) >= 9,
        "C6_TARGET_DESIGN_9_NEGATIVE_CONTROLS_EMITTED": NEGATIVE_CONTROL_TARGET_PATH.exists() and len(negative_control_target["negative_controls"]) >= 20,
        "C6_TARGET_DESIGN_10_OUTPUT_MANIFEST_TARGET_EMITTED": OUTPUT_MANIFEST_TARGET_PATH.exists(),
        "C6_TARGET_DESIGN_11_ACCEPTANCE_GATES_TARGET_EMITTED": ACCEPTANCE_GATES_TARGET_PATH.exists() and len(ACCEPTANCE_GATES) == 34,
        "C6_TARGET_DESIGN_12_BUILD_CONTRACT_EMITTED": BUILD_CONTRACT_PATH.exists() and build_contract["build_unit"] == FUTURE_BUILD_UNIT,
        "C6_TARGET_DESIGN_13_NO_PROTOCOL_BUILD_OR_EMISSION": classification["protocol_built_in_target_design"] is False and classification["protocol_emitted_in_target_design"] is False,
        "C6_TARGET_DESIGN_14_NO_RUNTIME_PATCH_OR_C7": classification["runtime_patched"] is False and classification["c7_authorized"] is False,
        "C6_TARGET_DESIGN_15_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "C6_TARGET_DESIGN_16_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["c5_reference_mutated"] is False,
        "C6_TARGET_DESIGN_17_BAD_COUNTERS_ZERO": profile["bad_counters_zero"] is True,
        "C6_TARGET_DESIGN_18_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "C6_TARGET_DESIGN_19_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "C6_TARGET_DESIGN_20_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_C6_INTER_CELL_PROTOCOL_TARGET_DESIGN_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_C6_INTER_CELL_PROTOCOL_TARGET_DESIGN_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_C6_INTER_CELL_PROTOCOL_TARGET_DESIGN_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_decision": SOURCE_POST_C6_DECISION_RECEIPT_ID,
        "future_build": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "c6_inter_cell_protocol_target_design_receipt_v0",
        "receipt_type": "TYPED_C6_INTER_CELL_PROTOCOL_TARGET_DESIGN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_post_c6_decision_receipt_id": SOURCE_POST_C6_DECISION_RECEIPT_ID,
        "source_c6_example_reference_closure_receipt_id": SOURCE_C6_EXAMPLE_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_c6_protocol_target_design_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "c6_protocol_target_designed": gate == "PASS",
            "c6_protocol_build_ready": gate == "PASS",
            "selected_build_unit": final_next,
            "packet_family_declared": len(PACKET_FAMILY),
            "state_model_declared": True,
            "gate_requirements_declared": len(gate_requirements["gates"]),
            "forbidden_transitions_declared": len(forbidden_transitions),
            "derivation_records_declared": len(derivation_records),
            "acceptance_gates_declared": len(ACCEPTANCE_GATES),
            "negative_controls_declared": len(negative_control_target["negative_controls"]),
            "protocol_built_in_target_design": False,
            "protocol_emitted_in_target_design": False,
            "runtime_patched": False,
            "c7_authorized": False,
            "new_domain_shift_executed": False,
            "full_transfer_claimed": False,
            "global_autonomy_claimed": False,
            "general_cell1_authority_claimed": False,
            "runtime_wide_enforcement_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "c5_reference_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": final_next,
        },
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "target_basis": rel(TARGET_BASIS_PATH),
            "target_spec": rel(TARGET_SPEC_PATH),
            "packet_family_target": rel(PACKET_FAMILY_TARGET_PATH),
            "state_model_target": rel(STATE_MODEL_TARGET_PATH),
            "gate_requirements": rel(GATE_REQUIREMENTS_PATH),
            "forbidden_transition_target": rel(FORBIDDEN_TRANSITION_TARGET_PATH),
            "derivation_policy": rel(DERIVATION_POLICY_PATH),
            "negative_control_target": rel(NEGATIVE_CONTROL_TARGET_PATH),
            "output_manifest_target": rel(OUTPUT_MANIFEST_TARGET_PATH),
            "acceptance_gates_target": rel(ACCEPTANCE_GATES_TARGET_PATH),
            "build_contract": rel(BUILD_CONTRACT_PATH),
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
    print(f"c6_protocol_target_design_receipt_id={receipt_id}")
    print(f"c6_protocol_target_design_receipt_path={rel(receipt_path)}")
    print(f"c6_protocol_target_spec_path={rel(TARGET_SPEC_PATH)}")
    print(f"c6_protocol_target_build_contract_path={rel(BUILD_CONTRACT_PATH)}")
    print(f"c6_protocol_target_rollup_path={rel(ROLLUP_PATH)}")
    print(f"c6_protocol_target_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
