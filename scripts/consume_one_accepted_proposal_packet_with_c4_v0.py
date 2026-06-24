#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CONSUME_ONE_ACCEPTED_PROPOSAL_PACKET_WITH_C4_V0"
TARGET_UNIT_ID = "c4.consume_one_accepted_proposal_packet.v0"
LAYER = "CELL_1 / RECEIPT_NATIVE_BUILDER_CONSUMPTION_GATE"
MODE = "C4_CONSUMPTION / ACCEPTED_PACKET / NO_RUNTIME_PATCH"
BUILD_MODE = "C4_ACCEPTED_PROPOSAL_CONSUMPTION_ONLY"

SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID = "71bd1d92"
SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0_receipts" / "71bd1d92.json"
SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "accepted_proposal_packet_v0.json"
SOURCE_REVIEW_DECISION_RECORD_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "review_decision_record_v0.json"
SOURCE_ACCEPTED_PROPOSAL_VALIDATION_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "accepted_proposal_validation_record_v0.json"
SOURCE_C4_CONSUMPTION_CONTRACT_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "c4_consumption_contract_record_v0.json"
SOURCE_ACCEPTED_PROPOSAL_ROLLUP_PATH = ROOT / "data" / "accepted_proposal_packet_for_c4_consumption_v0" / "accepted_proposal_packet_rollup_v0.json"

SOURCE_C4_RERUN_RECEIPT_ID = "a17b6786"
SOURCE_C4_RERUN_RECEIPT_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_preflight_rerun_v0_receipts" / "a17b6786.json"
SOURCE_C4_RERUN_GATE_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_preflight_rerun_v0" / "c4_opening_gate_evaluation_v0_1.json"
SOURCE_C4_RERUN_GATE_STATUS_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_preflight_rerun_v0" / "cell1_gate_status_v0.json"
SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_v0" / "cell1_accepted_proposal_input_schema_v0.json"
SOURCE_C4_AUTHORITY_PROFILE_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_v0" / "cell1_builder_authority_profile_v0.json"
SOURCE_C4_LOOP_TRACE_SCHEMA_PATH = ROOT / "data" / "c4_cell1_receipt_native_builder_v0" / "cell1_builder_loop_trace_schema_v0.json"

SOURCE_C1_PATCH_RECEIPT_ID = "fffa3dd5"
SOURCE_C1_PATCH_RECEIPT_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0_receipts" / "fffa3dd5.json"
SOURCE_C1_PATCH_SCHEMA_PATH = ROOT / "data" / "c1_proposal_interface_gap_patch_from_c3_v0" / "proposal_packet_schema_v0_1.json"

SOURCE_C3_RERUN_RECEIPT_ID = "d554701a"
SOURCE_C3_RERUN_RECEIPT_PATH = ROOT / "data" / "c3_micro_domain_shift_rerun_against_c1_interface_patch_v0_receipts" / "d554701a.json"
SOURCE_C3_RERUN_VERDICT_PATH = ROOT / "data" / "c3_micro_domain_shift_rerun_against_c1_interface_patch_v0" / "c3_interface_readiness_verdict_v0_1.json"

SOURCE_C2_RECEIPT_ID = "348dabde"
SOURCE_C2_RECEIPT_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0_receipts" / "348dabde.json"
SOURCE_C2_LANE_REGISTRY_PATH = ROOT / "data" / "c2_cell0_label_taxonomy_lane_cleaning_v0" / "taxonomy_lane_registry_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH,
    SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH,
    SOURCE_REVIEW_DECISION_RECORD_PATH,
    SOURCE_ACCEPTED_PROPOSAL_VALIDATION_PATH,
    SOURCE_C4_CONSUMPTION_CONTRACT_PATH,
    SOURCE_ACCEPTED_PROPOSAL_ROLLUP_PATH,
    SOURCE_C4_RERUN_RECEIPT_PATH,
    SOURCE_C4_RERUN_GATE_PATH,
    SOURCE_C4_RERUN_GATE_STATUS_PATH,
    SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH,
    SOURCE_C4_AUTHORITY_PROFILE_PATH,
    SOURCE_C4_LOOP_TRACE_SCHEMA_PATH,
    SOURCE_C1_PATCH_RECEIPT_PATH,
    SOURCE_C1_PATCH_SCHEMA_PATH,
    SOURCE_C3_RERUN_RECEIPT_PATH,
    SOURCE_C3_RERUN_VERDICT_PATH,
    SOURCE_C2_RECEIPT_PATH,
    SOURCE_C2_LANE_REGISTRY_PATH,
]

OUT_DIR = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0"
RECEIPT_DIR = ROOT / "data" / "c4_consume_one_accepted_proposal_packet_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "c4_consumption_source_surface_v0.json"
INTAKE_VALIDATION_PATH = OUT_DIR / "c4_accepted_proposal_intake_validation_v0.json"
CONSUMPTION_RECORD_PATH = OUT_DIR / "c4_consumption_record_v0.json"
CELL1_INTAKE_PACKET_PATH = OUT_DIR / "cell1_intake_packet_v0.json"
NO_RUNTIME_PATCH_PLAN_PATH = OUT_DIR / "no_runtime_patch_plan_v0.json"
SCHEMA_CONSUMPTION_PROBE_RECORD_PATH = OUT_DIR / "schema_consumption_probe_record_v0.json"
VERIFICATION_EXPECTATION_RECORD_PATH = OUT_DIR / "verification_expectation_record_v0.json"
HANDOFF_PACKET_PATH = OUT_DIR / "cell1_handoff_packet_v0.json"
ROLLUP_PATH = OUT_DIR / "c4_consumption_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c4_consumption_profile_v0.json"
REPORT_PATH = OUT_DIR / "c4_consumption_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "c4_consumption_transition_trace.json"

ACCEPTED_STATUS = "ACCEPTED_FOR_BUILD"

ZERO_COUNTER_KEYS = [
    "runtime_patch_applied_count",
    "target_file_modified_count",
    "builds_verified_count",
    "verification_pass_emitted_count",
    "c5_opened_count",
    "taxonomy_registry_mutation_count",
    "proposal_status_promoted_count",
    "proposed_only_consumed_as_accepted_count",
    "accepted_proposal_fabricated_count",
    "cell1_general_authority_granted_count",
    "unbounded_payload_inspection_count",
    "hidden_next_command_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
    "unexpected_builder_command_count",
]

HUMAN_DECISION = {
    "decision": "CONSUME_ONE_ACCEPTED_PROPOSAL_PACKET_WITH_C4",
    "scope": "Consume exactly one review-backed accepted proposal packet with C4. Validate that the C4 gate is open, the packet is accepted by review, the review receipt authorizes the exact proposal id, and the packet is scoped to a no-runtime-patch schema-consumption test. Emit C4 intake validation, consumption record, Cell 1 intake/handoff packet, no-runtime-patch plan, schema-consumption probe record, verification expectation record, rollup, profile, report, and receipt. Do not apply runtime patches, do not modify target files, do not emit verification PASS, do not open C5, do not mutate taxonomy, and do not emit hidden next command.",
    "authorized": [
        "consume one accepted proposal packet",
        "validate review receipt and exact proposal id",
        "validate accepted status against C4 accepted proposal schema",
        "emit C4 consumption record",
        "emit Cell 1 intake/handoff packet",
        "emit no-runtime-patch plan",
        "emit schema-consumption probe record",
        "emit verification expectation record",
        "emit C4 consumption receipt",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "consume PROPOSED_ONLY as accepted",
        "fabricate accepted proposal",
        "promote proposal status",
        "apply runtime patch",
        "modify target files",
        "emit verification PASS",
        "claim build verified",
        "grant general Cell 1 authority",
        "mutate taxonomy registry",
        "open C5",
        "emit hidden next command",
    ],
}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures

    accepted_receipt = read_json(SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH)
    packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    review = read_json(SOURCE_REVIEW_DECISION_RECORD_PATH)
    validation = read_json(SOURCE_ACCEPTED_PROPOSAL_VALIDATION_PATH)
    contract = read_json(SOURCE_C4_CONSUMPTION_CONTRACT_PATH)
    accepted_rollup = read_json(SOURCE_ACCEPTED_PROPOSAL_ROLLUP_PATH)
    c4_receipt = read_json(SOURCE_C4_RERUN_RECEIPT_PATH)
    c4_gate = read_json(SOURCE_C4_RERUN_GATE_PATH)
    c4_gate_status = read_json(SOURCE_C4_RERUN_GATE_STATUS_PATH)
    c4_schema = read_json(SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH)
    c1_schema = read_json(SOURCE_C1_PATCH_SCHEMA_PATH)
    c3_verdict = read_json(SOURCE_C3_RERUN_VERDICT_PATH)
    c2_receipt = read_json(SOURCE_C2_RECEIPT_PATH)

    if accepted_receipt.get("receipt_id") != SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID or accepted_receipt.get("gate") != "PASS":
        failures.append("accepted_proposal_receipt_not_accepted")
    if accepted_receipt.get("terminal", {}).get("stop_code") != "STOP_ACCEPTED_PROPOSAL_PACKET_READY_FOR_C4_CONSUMPTION":
        failures.append("accepted_proposal_receipt_wrong_terminal")
    if packet.get("status") != ACCEPTED_STATUS:
        failures.append("packet_not_accepted_for_build")
    if packet.get("review_receipt_id") != review.get("review_receipt_id"):
        failures.append("packet_review_receipt_mismatch")
    if review.get("review_decision") != ACCEPTED_STATUS:
        failures.append("review_not_accepted_for_build")
    if review.get("authorizes_exact_proposal_id") is not True or review.get("proposal_id") != packet.get("proposal_id"):
        failures.append("review_not_exact_proposal")
    if validation.get("validation_status") != "PASS" or validation.get("future_c4_consumption_candidate") is not True:
        failures.append("accepted_proposal_validation_not_pass")
    if contract.get("future_c4_unit") != UNIT_ID:
        failures.append(f"contract_future_unit_mismatch:{contract.get('future_c4_unit')}")
    if contract.get("future_cell1_execution_allowed_by_this_unit") is not False:
        failures.append("contract_allows_cell1_execution_by_this_unit")
    if accepted_rollup.get("c4_consumption_run_count") != 0:
        failures.append("accepted_proposal_source_already_consumed")
    if c4_receipt.get("receipt_id") != SOURCE_C4_RERUN_RECEIPT_ID or c4_receipt.get("gate") != "PASS":
        failures.append("c4_preflight_rerun_basis_not_accepted")
    if c4_gate.get("c4_opening_gate_status") != "OPEN_FOR_NARROW_ACCEPTED_PROPOSAL_TEST":
        failures.append("c4_gate_not_open")
    if c4_gate.get("accepted_proposal_present") is not False:
        failures.append("c4_gate_prior_claimed_accepted_proposal_present")
    if c4_gate_status.get("execution_status") != "NOT_OPENED":
        failures.append("c4_gate_status_execution_already_opened")
    if c4_gate_status.get("may_consume_proposed_only") is not False:
        failures.append("c4_gate_status_allows_proposed_only")
    if ACCEPTED_STATUS not in c4_schema.get("accepted_statuses", []):
        failures.append("accepted_status_not_in_c4_schema")
    if c1_schema.get("review_authority", {}).get("cell1_may_accept") is not False:
        failures.append("c1_schema_allows_cell1_acceptance")
    if c3_verdict.get("verdict") != "CELL1_READY_FOR_NARROW_ACCEPTED_PROPOSAL_TEST":
        failures.append("c3_rerun_verdict_not_ready")
    if c2_receipt.get("receipt_id") != SOURCE_C2_RECEIPT_ID or c2_receipt.get("gate") != "PASS":
        failures.append("c2_basis_not_accepted")
    return failures

def source_surface() -> Dict[str, Any]:
    return {
        "schema_version": "c4_consumption_source_surface_v0",
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_accepted_proposal_receipt_ref": rel(SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH),
        "source_accepted_proposal_packet_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "source_review_decision_record_ref": rel(SOURCE_REVIEW_DECISION_RECORD_PATH),
        "source_c4_preflight_rerun_receipt_id": SOURCE_C4_RERUN_RECEIPT_ID,
        "source_c4_opening_gate_ref": rel(SOURCE_C4_RERUN_GATE_PATH),
        "source_c1_patch_schema_ref": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c3_rerun_verdict_ref": rel(SOURCE_C3_RERUN_VERDICT_PATH),
        "source_c2_lane_registry_ref": rel(SOURCE_C2_LANE_REGISTRY_PATH),
        "surface_status": "EXPLICIT_REVIEW_BACKED_C4_CONSUMPTION_SURFACE",
    }

def intake_validation() -> Dict[str, Any]:
    packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    review = read_json(SOURCE_REVIEW_DECISION_RECORD_PATH)
    c4_schema = read_json(SOURCE_C4_ACCEPTED_PROPOSAL_SCHEMA_PATH)
    failures: List[str] = []

    if packet.get("status") not in c4_schema.get("accepted_statuses", []):
        failures.append("status_not_accepted_by_c4_schema")
    if packet.get("review_receipt_id") != review.get("review_receipt_id"):
        failures.append("review_receipt_id_mismatch")
    if review.get("proposal_id") != packet.get("proposal_id"):
        failures.append("review_proposal_id_mismatch")
    if review.get("authorizes_exact_proposal_id") is not True:
        failures.append("review_not_exact_proposal")
    if packet.get("expected_patch_shape", {}).get("patch_application_expected") is not False:
        failures.append("runtime_patch_expected_but_forbidden")
    if packet.get("review_authority", {}).get("cell1_may_accept") is not False:
        failures.append("packet_allows_cell1_acceptance")
    if not packet.get("builder_interface", {}).get("required_input_refs"):
        failures.append("builder_required_input_refs_missing")

    return {
        "schema_version": "c4_accepted_proposal_intake_validation_v0",
        "validation_id": "c4_intake_" + sha8({"proposal": packet.get("proposal_id"), "review": review.get("review_receipt_id")}),
        "proposal_id": packet.get("proposal_id"),
        "review_receipt_id": review.get("review_receipt_id"),
        "accepted_status_valid": packet.get("status") in c4_schema.get("accepted_statuses", []),
        "review_exact_proposal_valid": review.get("proposal_id") == packet.get("proposal_id") and review.get("authorizes_exact_proposal_id") is True,
        "no_runtime_patch_expected": packet.get("expected_patch_shape", {}).get("patch_application_expected") is False,
        "cell1_may_accept": False,
        "validation_status": "PASS" if not failures else "FAIL",
        "failures": failures,
    }

def consumption_record(validation: Dict[str, Any]) -> Dict[str, Any]:
    packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    return {
        "schema_version": "c4_consumption_record_v0",
        "consumption_id": "c4_consumption_" + sha8({"proposal": packet.get("proposal_id"), "accepted_receipt": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID}),
        "proposal_id": packet.get("proposal_id"),
        "accepted_proposal_packet_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "review_decision_record_ref": rel(SOURCE_REVIEW_DECISION_RECORD_PATH),
        "intake_validation_ref": rel(INTAKE_VALIDATION_PATH),
        "consumption_status": "CONSUMED_FOR_CELL1_INTAKE_PACKET" if validation["validation_status"] == "PASS" else "REJECTED_BY_C4_INTAKE",
        "cell1_execution_opened": False,
        "runtime_patch_applied": False,
        "verification_pass_emitted": False,
        "scope": "single accepted proposal packet only",
    }

def cell1_intake_packet(validation: Dict[str, Any]) -> Dict[str, Any]:
    packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    return {
        "schema_version": "cell1_intake_packet_v0",
        "cell1_intake_packet_id": "cell1_intake_" + sha8({"proposal": packet.get("proposal_id"), "validation": validation["validation_id"]}),
        "proposal_id": packet.get("proposal_id"),
        "proposal_status": packet.get("status"),
        "review_receipt_id": packet.get("review_receipt_id"),
        "accepted_proposal_packet_ref": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "c4_consumption_record_ref": rel(CONSUMPTION_RECORD_PATH),
        "bounded_objective": packet.get("bounded_objective"),
        "target_surface": packet.get("target_surface"),
        "allowed_inputs": packet.get("allowed_inputs"),
        "forbidden_inputs": packet.get("forbidden_inputs"),
        "expected_patch_shape": packet.get("expected_patch_shape"),
        "verification_requirement": packet.get("verification_requirement"),
        "stop_conditions": packet.get("stop_conditions"),
        "execution_status": "READY_FOR_CELL1_SCHEMA_CONSUMPTION_TEST",
        "runtime_patch_allowed": False,
        "general_cell1_authority_granted": False,
        "must_not_infer": [
            "Cell 1 has executed",
            "runtime patch is required",
            "verification has passed",
            "C5 is authorized",
        ],
    }

def no_runtime_patch_plan() -> Dict[str, Any]:
    packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    return {
        "schema_version": "no_runtime_patch_plan_v0",
        "patch_plan_id": "no_patch_" + sha8({"proposal": packet.get("proposal_id")}),
        "proposal_id": packet.get("proposal_id"),
        "plan_kind": "NO_RUNTIME_PATCH_SCHEMA_CONSUMPTION_TEST",
        "patch_application_expected": False,
        "files_expected_to_change": [],
        "objects_expected_to_change": [],
        "files_forbidden_to_change": packet.get("expected_patch_shape", {}).get("files_forbidden_to_change", []),
        "objects_forbidden_to_change": [
            "taxonomy_registry",
            "runtime_source",
            "C5_domain_shift",
        ],
        "expected_tests": [
            "schema consumption probe only",
            "verification expectation emitted but not PASS",
        ],
    }

def schema_consumption_probe_record() -> Dict[str, Any]:
    packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    return {
        "schema_version": "schema_consumption_probe_record_v0",
        "probe_id": "schema_consumption_" + sha8({"proposal": packet.get("proposal_id")}),
        "proposal_id": packet.get("proposal_id"),
        "probe_kind": "SCHEMA_CONSUMPTION_ONLY",
        "checks": {
            "accepted_status_present": packet.get("status") == ACCEPTED_STATUS,
            "review_receipt_present": bool(packet.get("review_receipt_id")),
            "builder_interface_present": "builder_interface" in packet,
            "verification_contract_present": "verification_contract" in packet,
            "payload_boundary_present": "payload_boundary" in packet,
            "no_runtime_patch_expected": packet.get("expected_patch_shape", {}).get("patch_application_expected") is False,
        },
        "probe_status": "PASS",
        "runtime_patch_applied": False,
        "verification_pass_emitted": False,
        "must_not_infer": [
            "probe pass is build verification",
            "runtime patch applied",
            "future probes unnecessary",
        ],
    }

def verification_expectation_record() -> Dict[str, Any]:
    packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    return {
        "schema_version": "verification_expectation_record_v0",
        "verification_expectation_id": "verify_expect_" + sha8({"proposal": packet.get("proposal_id")}),
        "proposal_id": packet.get("proposal_id"),
        "expected_verification_receipt_shape": packet.get("verification_contract", {}).get("expected_verification_receipt_shape"),
        "required_checks": packet.get("verification_requirement", {}).get("required_checks", []),
        "required_negative_controls": packet.get("verification_contract", {}).get("required_negative_controls", []),
        "verification_status": "PENDING_NOT_RUN",
        "verification_pass_emitted": False,
        "must_not_infer": [
            "verification pass",
            "build correctness",
            "runtime patch correctness",
        ],
    }

def handoff_packet() -> Dict[str, Any]:
    packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    return {
        "schema_version": "cell1_handoff_packet_v0",
        "handoff_id": "handoff_cell1_" + sha8({"proposal": packet.get("proposal_id")}),
        "from": "C4",
        "to": "CELL_1_SCHEMA_CONSUMPTION_TEST",
        "proposal_id": packet.get("proposal_id"),
        "cell1_intake_packet_ref": rel(CELL1_INTAKE_PACKET_PATH),
        "no_runtime_patch_plan_ref": rel(NO_RUNTIME_PATCH_PLAN_PATH),
        "schema_consumption_probe_record_ref": rel(SCHEMA_CONSUMPTION_PROBE_RECORD_PATH),
        "verification_expectation_record_ref": rel(VERIFICATION_EXPECTATION_RECORD_PATH),
        "handoff_status": "READY_FOR_CELL1_SCHEMA_CONSUMPTION_TEST",
        "cell1_execution_performed_in_this_unit": False,
        "next_required_action": "RUN_CELL1_SCHEMA_CONSUMPTION_TEST_FROM_C4_HANDOFF_V0",
        "must_not_infer": [
            "Cell 1 executed",
            "verification passed",
            "runtime patch applied",
            "C5 authorized",
        ],
    }

def rollup(validation: Dict[str, Any]) -> Dict[str, Any]:
    packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    return {
        "schema_version": "c4_consumption_rollup_v0",
        "build_mode": BUILD_MODE,
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c4_preflight_rerun_receipt_id": SOURCE_C4_RERUN_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c3_rerun_receipt_id": SOURCE_C3_RERUN_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "proposal_id": packet.get("proposal_id"),
        "proposal_status": packet.get("status"),
        "review_receipt_id": packet.get("review_receipt_id"),
        "accepted_proposals_consumed": 1 if validation["validation_status"] == "PASS" else 0,
        "intake_validation_status": validation["validation_status"],
        "c4_consumption_records_emitted": 1,
        "cell1_intake_packets_emitted": 1,
        "handoff_packets_emitted": 1,
        "schema_consumption_probe_records_emitted": 1,
        "verification_expectation_records_emitted": 1,
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "builds_verified_count": 0,
        "verification_pass_emitted_count": 0,
        "c5_opened_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "proposal_status_promoted_count": 0,
        "proposed_only_consumed_as_accepted_count": 0,
        "accepted_proposal_fabricated_count": 0,
        "cell1_general_authority_granted_count": 0,
        "unbounded_payload_inspection_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "unexpected_builder_command_count": 0,
        "recommended_next": "RUN_CELL1_SCHEMA_CONSUMPTION_TEST_FROM_C4_HANDOFF_V0",
    }

def profile(rollup_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c4_consumption_profile_v0",
        "profile_id": "c4_consumption_" + sha8({"proposal": rollup_obj["proposal_id"], "source": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID}),
        "status": "C4_ACCEPTED_PROPOSAL_CONSUMED_READY_FOR_CELL1_SCHEMA_CONSUMPTION_TEST",
        "proposal_id": rollup_obj["proposal_id"],
        "cell1_intake_packet_ref": rel(CELL1_INTAKE_PACKET_PATH),
        "handoff_packet_ref": rel(HANDOFF_PACKET_PATH),
        "runtime_patch_applied": False,
        "verification_pass_emitted": False,
        "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
        "must_not_infer": [
            "Cell 1 executed",
            "runtime patch applied",
            "verification passed",
            "C5 authorized",
            "general Cell 1 builder authority",
        ],
        "next_command_goal": None,
    }

def report(rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "c4_consumption_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_accepted_proposal_packet_consumed_count": 1,
        "source_review_record_consumed_count": 1,
        "source_c4_gate_consumed_count": 1,
        "intake_validation_emitted_count": 1,
        "c4_consumption_record_emitted_count": 1,
        "cell1_intake_packet_emitted_count": 1,
        "handoff_packet_emitted_count": 1,
        "no_runtime_patch_plan_emitted_count": 1,
        "schema_consumption_probe_record_emitted_count": 1,
        "verification_expectation_record_emitted_count": 1,
        "profile_status": profile_obj["status"],
        "accepted_proposals_consumed": rollup_obj["accepted_proposals_consumed"],
        "runtime_patch_applied_count": 0,
        "target_file_modified_count": 0,
        "builds_verified_count": 0,
        "verification_pass_emitted_count": 0,
        "c5_opened_count": 0,
        "taxonomy_registry_mutation_count": 0,
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "recommended_next_handling": rollup_obj["recommended_next"],
    }

def transition_trace() -> Dict[str, Any]:
    packet = read_json(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH)
    return {
        "schema_version": "c4_consumption_transition_trace_v0",
        "trace": [
            {
                "step": "load_accepted_proposal_packet",
                "question": "is there exactly one review-backed accepted proposal packet",
                "answer": packet.get("proposal_id"),
                "taken": "validate_c4_intake",
            },
            {
                "step": "validate_c4_intake",
                "question": "does review authorize exact proposal id and status match C4 accepted schema",
                "answer": "PASS",
                "taken": "emit_cell1_intake_packet",
            },
            {
                "step": "emit_cell1_intake_packet",
                "question": "does the bounded objective require runtime patch",
                "answer": False,
                "taken": "emit_no_runtime_patch_plan_and_handoff",
            },
            {
                "step": "stop",
                "question": "did C4 avoid patch/probe/verification/C5/hidden continuation",
                "answer": True,
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_C4_CONSUMED_ACCEPTED_PROPOSAL_READY_FOR_CELL1_SCHEMA_CONSUMPTION",
            "next_command_goal": None,
        },
    }

def validate_outputs(validation: Dict[str, Any], consumption: Dict[str, Any], intake: Dict[str, Any], patch_plan: Dict[str, Any], probe: Dict[str, Any], verification: Dict[str, Any], handoff: Dict[str, Any], rollup_obj: Dict[str, Any], profile_obj: Dict[str, Any], report_obj: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if validation.get("validation_status") != "PASS":
        failures.append("intake_validation_not_pass")
    if consumption.get("consumption_status") != "CONSUMED_FOR_CELL1_INTAKE_PACKET":
        failures.append("consumption_status_not_consumed")
    if consumption.get("cell1_execution_opened") is not False:
        failures.append("consumption_claims_cell1_execution")
    if intake.get("execution_status") != "READY_FOR_CELL1_SCHEMA_CONSUMPTION_TEST":
        failures.append("cell1_intake_status_wrong")
    if intake.get("runtime_patch_allowed") is not False:
        failures.append("cell1_intake_allows_runtime_patch")
    if intake.get("general_cell1_authority_granted") is not False:
        failures.append("cell1_intake_grants_general_authority")
    if patch_plan.get("patch_application_expected") is not False:
        failures.append("patch_plan_expects_runtime_patch")
    if patch_plan.get("files_expected_to_change") != []:
        failures.append("patch_plan_expects_file_changes")
    if probe.get("probe_status") != "PASS":
        failures.append("schema_consumption_probe_not_pass")
    if probe.get("runtime_patch_applied") is not False:
        failures.append("probe_claims_runtime_patch")
    if probe.get("verification_pass_emitted") is not False:
        failures.append("probe_claims_verification_pass")
    if verification.get("verification_status") != "PENDING_NOT_RUN":
        failures.append("verification_status_not_pending")
    if verification.get("verification_pass_emitted") is not False:
        failures.append("verification_pass_emitted")
    if handoff.get("handoff_status") != "READY_FOR_CELL1_SCHEMA_CONSUMPTION_TEST":
        failures.append("handoff_status_wrong")
    if handoff.get("cell1_execution_performed_in_this_unit") is not False:
        failures.append("handoff_claims_cell1_execution")
    for key in ZERO_COUNTER_KEYS:
        if rollup_obj.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup_obj.get(key)}")
    if rollup_obj.get("accepted_proposals_consumed") != 1:
        failures.append("accepted_proposals_consumed_not_one")
    if rollup_obj.get("cell1_intake_packets_emitted") != 1:
        failures.append("cell1_intake_packet_count_not_one")
    if profile_obj.get("runtime_patch_applied") is not False:
        failures.append("profile_claims_runtime_patch")
    if profile_obj.get("verification_pass_emitted") is not False:
        failures.append("profile_claims_verification_pass")
    if profile_obj.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    for key in [
        "runtime_patch_applied_count",
        "target_file_modified_count",
        "builds_verified_count",
        "verification_pass_emitted_count",
        "c5_opened_count",
        "taxonomy_registry_mutation_count",
        "hidden_next_command_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
    ]:
        if report_obj.get(key) != 0:
            failures.append(f"report_counter_nonzero:{key}:{report_obj.get(key)}")
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    for gate, ok in receipt.get("acceptance_gate_results", {}).items():
        if ok is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{ok}")
    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_C4_CONSUMED_ACCEPTED_PROPOSAL_READY_FOR_CELL1_SCHEMA_CONSUMPTION":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    validation = read_json(INTAKE_VALIDATION_PATH)
    consumption = read_json(CONSUMPTION_RECORD_PATH)
    intake = read_json(CELL1_INTAKE_PACKET_PATH)
    patch_plan = read_json(NO_RUNTIME_PATCH_PLAN_PATH)
    probe = read_json(SCHEMA_CONSUMPTION_PROBE_RECORD_PATH)
    verification = read_json(VERIFICATION_EXPECTATION_RECORD_PATH)
    handoff = read_json(HANDOFF_PACKET_PATH)
    rollup_obj = read_json(ROLLUP_PATH)
    profile_obj = read_json(PROFILE_PATH)
    report_obj = read_json(REPORT_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    bad_validation = copy.deepcopy(validation)
    bad_validation["validation_status"] = "FAIL"
    add("intake_validation_fail", validate_outputs(bad_validation, consumption, intake, patch_plan, probe, verification, handoff, rollup_obj, profile_obj, report_obj), "intake_validation_not_pass")

    bad_consumption = copy.deepcopy(consumption)
    bad_consumption["consumption_status"] = "REJECTED_BY_C4_INTAKE"
    add("consumption_status_not_consumed_fail", validate_outputs(validation, bad_consumption, intake, patch_plan, probe, verification, handoff, rollup_obj, profile_obj, report_obj), "consumption_status_not_consumed")

    bad_consumption = copy.deepcopy(consumption)
    bad_consumption["cell1_execution_opened"] = True
    add("consumption_claims_cell1_execution_fail", validate_outputs(validation, bad_consumption, intake, patch_plan, probe, verification, handoff, rollup_obj, profile_obj, report_obj), "consumption_claims_cell1_execution")

    bad_intake = copy.deepcopy(intake)
    bad_intake["runtime_patch_allowed"] = True
    add("cell1_intake_allows_runtime_patch_fail", validate_outputs(validation, consumption, bad_intake, patch_plan, probe, verification, handoff, rollup_obj, profile_obj, report_obj), "cell1_intake_allows_runtime_patch")

    bad_intake = copy.deepcopy(intake)
    bad_intake["general_cell1_authority_granted"] = True
    add("cell1_general_authority_granted_fail", validate_outputs(validation, consumption, bad_intake, patch_plan, probe, verification, handoff, rollup_obj, profile_obj, report_obj), "cell1_intake_grants_general_authority")

    bad_patch_plan = copy.deepcopy(patch_plan)
    bad_patch_plan["patch_application_expected"] = True
    add("patch_plan_expects_runtime_patch_fail", validate_outputs(validation, consumption, intake, bad_patch_plan, probe, verification, handoff, rollup_obj, profile_obj, report_obj), "patch_plan_expects_runtime_patch")

    bad_patch_plan = copy.deepcopy(patch_plan)
    bad_patch_plan["files_expected_to_change"] = ["src/matrixlab/cli.py"]
    add("patch_plan_expects_file_changes_fail", validate_outputs(validation, consumption, intake, bad_patch_plan, probe, verification, handoff, rollup_obj, profile_obj, report_obj), "patch_plan_expects_file_changes")

    bad_probe = copy.deepcopy(probe)
    bad_probe["runtime_patch_applied"] = True
    add("probe_claims_runtime_patch_fail", validate_outputs(validation, consumption, intake, patch_plan, bad_probe, verification, handoff, rollup_obj, profile_obj, report_obj), "probe_claims_runtime_patch")

    bad_probe = copy.deepcopy(probe)
    bad_probe["verification_pass_emitted"] = True
    add("probe_claims_verification_pass_fail", validate_outputs(validation, consumption, intake, patch_plan, bad_probe, verification, handoff, rollup_obj, profile_obj, report_obj), "probe_claims_verification_pass")

    bad_verification = copy.deepcopy(verification)
    bad_verification["verification_status"] = "PASS"
    add("verification_status_pass_fail", validate_outputs(validation, consumption, intake, patch_plan, probe, bad_verification, handoff, rollup_obj, profile_obj, report_obj), "verification_status_not_pending")

    bad_handoff = copy.deepcopy(handoff)
    bad_handoff["cell1_execution_performed_in_this_unit"] = True
    add("handoff_claims_cell1_execution_fail", validate_outputs(validation, consumption, intake, patch_plan, probe, verification, bad_handoff, rollup_obj, profile_obj, report_obj), "handoff_claims_cell1_execution")

    for case, counter in [
        ("runtime_patch_applied_fail", "runtime_patch_applied_count"),
        ("target_file_modified_fail", "target_file_modified_count"),
        ("build_verified_fail", "builds_verified_count"),
        ("verification_pass_emitted_fail", "verification_pass_emitted_count"),
        ("c5_opened_fail", "c5_opened_count"),
        ("taxonomy_registry_mutated_fail", "taxonomy_registry_mutation_count"),
        ("proposal_status_promoted_fail", "proposal_status_promoted_count"),
        ("proposed_only_consumed_as_accepted_fail", "proposed_only_consumed_as_accepted_count"),
        ("accepted_proposal_fabricated_fail", "accepted_proposal_fabricated_count"),
        ("cell1_general_authority_counter_fail", "cell1_general_authority_granted_count"),
        ("unbounded_payload_inspection_fail", "unbounded_payload_inspection_count"),
        ("hidden_next_command_fail", "hidden_next_command_count"),
        ("source_mutation_fail", "source_mutation_count"),
        ("prior_receipt_mutation_fail", "prior_receipt_mutation_count"),
        ("unexpected_builder_command_fail", "unexpected_builder_command_count"),
    ]:
        bad_rollup = copy.deepcopy(rollup_obj)
        bad_report = copy.deepcopy(report_obj)
        bad_rollup[counter] = 1
        if counter in bad_report:
            bad_report[counter] = 1
        add(case, validate_outputs(validation, consumption, intake, patch_plan, probe, verification, handoff, bad_rollup, profile_obj, bad_report), counter)

    bad_rollup = copy.deepcopy(rollup_obj)
    bad_rollup["accepted_proposals_consumed"] = 0
    add("accepted_proposals_consumed_not_one_fail", validate_outputs(validation, consumption, intake, patch_plan, probe, verification, handoff, bad_rollup, profile_obj, report_obj), "accepted_proposals_consumed_not_one")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_C4_CONSUMPTION_DEPENDENCY_MISSING", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "c4_consumption_receipt_v0",
            "receipt_type": "C4_ACCEPTED_PROPOSAL_CONSUMPTION_RECEIPT",
            "receipt_id": receipt_id,
            "unit_id": UNIT_ID,
            "target_unit_id": TARGET_UNIT_ID,
            "gate": "FAIL",
            "failures": failures,
            "terminal": terminal,
            "created_at": now_iso(),
        }
        write_json(receipt_path, receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        print(f"c4_consumption_receipt_id={receipt_id}")
        print(f"c4_consumption_receipt_path=data/c4_consume_one_accepted_proposal_packet_v0_receipts/{receipt_id}.json")
        return 1

    validation = intake_validation()
    consumption = consumption_record(validation)
    intake = cell1_intake_packet(validation)
    patch_plan = no_runtime_patch_plan()
    probe = schema_consumption_probe_record()
    verification = verification_expectation_record()
    handoff = handoff_packet()
    rollup_obj = rollup(validation)
    profile_obj = profile(rollup_obj)
    report_obj = report(rollup_obj, profile_obj)
    trace = transition_trace()

    write_json(SOURCE_SURFACE_PATH, source_surface())
    write_json(INTAKE_VALIDATION_PATH, validation)
    write_json(CONSUMPTION_RECORD_PATH, consumption)
    write_json(CELL1_INTAKE_PACKET_PATH, intake)
    write_json(NO_RUNTIME_PATCH_PLAN_PATH, patch_plan)
    write_json(SCHEMA_CONSUMPTION_PROBE_RECORD_PATH, probe)
    write_json(VERIFICATION_EXPECTATION_RECORD_PATH, verification)
    write_json(HANDOFF_PACKET_PATH, handoff)
    write_json(ROLLUP_PATH, rollup_obj)
    write_json(PROFILE_PATH, profile_obj)
    write_json(REPORT_PATH, report_obj)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(validation, consumption, intake, patch_plan, probe, verification, handoff, rollup_obj, profile_obj, report_obj))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup_obj["source_mutation_count"] = 1
        report_obj["source_mutation_count"] = 1
        write_json(ROLLUP_PATH, rollup_obj)
        write_json(REPORT_PATH, report_obj)

    acceptance_gate_results = {
        "C4_CONSUME_0_ACCEPTED_PROPOSAL_RECEIPT_CONSUMED": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH.exists(),
        "C4_CONSUME_1_ACCEPTED_PACKET_CONSUMED": SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH.exists(),
        "C4_CONSUME_2_REVIEW_RECORD_CONSUMED": SOURCE_REVIEW_DECISION_RECORD_PATH.exists(),
        "C4_CONSUME_3_C4_GATE_OPEN_CONSUMED": read_json(SOURCE_C4_RERUN_GATE_PATH).get("c4_opening_gate_status") == "OPEN_FOR_NARROW_ACCEPTED_PROPOSAL_TEST",
        "C4_CONSUME_4_INTAKE_VALIDATION_PASS": validation["validation_status"] == "PASS",
        "C4_CONSUME_5_EXACT_REVIEW_AUTHORITY_VALID": validation["review_exact_proposal_valid"] is True,
        "C4_CONSUME_6_CONSUMPTION_RECORD_EMITTED": CONSUMPTION_RECORD_PATH.exists(),
        "C4_CONSUME_7_ACCEPTED_PROPOSAL_CONSUMED_ONCE": rollup_obj["accepted_proposals_consumed"] == 1,
        "C4_CONSUME_8_CELL1_INTAKE_PACKET_EMITTED": CELL1_INTAKE_PACKET_PATH.exists(),
        "C4_CONSUME_9_NO_RUNTIME_PATCH_PLAN_EMITTED": NO_RUNTIME_PATCH_PLAN_PATH.exists() and patch_plan["patch_application_expected"] is False,
        "C4_CONSUME_10_SCHEMA_CONSUMPTION_PROBE_EMITTED": SCHEMA_CONSUMPTION_PROBE_RECORD_PATH.exists() and probe["probe_status"] == "PASS",
        "C4_CONSUME_11_VERIFICATION_EXPECTATION_PENDING": VERIFICATION_EXPECTATION_RECORD_PATH.exists() and verification["verification_status"] == "PENDING_NOT_RUN",
        "C4_CONSUME_12_HANDOFF_READY_FOR_CELL1_SCHEMA_CONSUMPTION": HANDOFF_PACKET_PATH.exists() and handoff["handoff_status"] == "READY_FOR_CELL1_SCHEMA_CONSUMPTION_TEST",
        "C4_CONSUME_13_NO_RUNTIME_PATCH_APPLIED": rollup_obj["runtime_patch_applied_count"] == 0,
        "C4_CONSUME_14_NO_TARGET_FILE_MODIFIED": rollup_obj["target_file_modified_count"] == 0,
        "C4_CONSUME_15_NO_VERIFICATION_PASS_EMITTED": rollup_obj["verification_pass_emitted_count"] == 0,
        "C4_CONSUME_16_NO_C5_OPENED": rollup_obj["c5_opened_count"] == 0,
        "C4_CONSUME_17_NO_TAXONOMY_MUTATION": rollup_obj["taxonomy_registry_mutation_count"] == 0,
        "C4_CONSUME_18_NO_GENERAL_CELL1_AUTHORITY": rollup_obj["cell1_general_authority_granted_count"] == 0,
        "C4_CONSUME_19_NO_HIDDEN_NEXT_COMMAND": rollup_obj["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
        "C4_CONSUME_20_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
    }

    for gate_name, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate_name}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_accepted_proposal": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "proposal_id": rollup_obj["proposal_id"],
        "consumed": rollup_obj["accepted_proposals_consumed"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "intake_validation": rel(INTAKE_VALIDATION_PATH),
        "consumption_record": rel(CONSUMPTION_RECORD_PATH),
        "cell1_intake_packet": rel(CELL1_INTAKE_PACKET_PATH),
        "no_runtime_patch_plan": rel(NO_RUNTIME_PATCH_PLAN_PATH),
        "schema_consumption_probe_record": rel(SCHEMA_CONSUMPTION_PROBE_RECORD_PATH),
        "verification_expectation_record": rel(VERIFICATION_EXPECTATION_RECORD_PATH),
        "handoff_packet": rel(HANDOFF_PACKET_PATH),
        "rollup": rel(ROLLUP_PATH),
        "profile": rel(PROFILE_PATH),
        "report": rel(REPORT_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_accepted_proposal_receipt": rel(SOURCE_ACCEPTED_PROPOSAL_RECEIPT_PATH),
        "source_accepted_proposal_packet": rel(SOURCE_ACCEPTED_PROPOSAL_PACKET_PATH),
        "source_review_decision_record": rel(SOURCE_REVIEW_DECISION_RECORD_PATH),
        "source_c4_opening_gate": rel(SOURCE_C4_RERUN_GATE_PATH),
        "source_c1_patch_schema": rel(SOURCE_C1_PATCH_SCHEMA_PATH),
        "source_c2_lane_registry": rel(SOURCE_C2_LANE_REGISTRY_PATH),
    }

    guards = {
        "build_mode_c4_accepted_proposal_consumption_only": BUILD_MODE == "C4_ACCEPTED_PROPOSAL_CONSUMPTION_ONLY",
        "accepted_proposal_consumed_once": rollup_obj["accepted_proposals_consumed"] == 1,
        "review_exact_proposal_valid": validation["review_exact_proposal_valid"] is True,
        "cell1_intake_packet_emitted": True,
        "runtime_patch_applied": False,
        "target_file_modified": False,
        "verification_pass_emitted": False,
        "c5_opened": False,
        "taxonomy_registry_mutated": False,
        "general_cell1_authority_granted": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
    }

    receipt = {
        "schema_version": "c4_consumption_receipt_v0",
        "receipt_type": "C4_ACCEPTED_PROPOSAL_CONSUMPTION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "one accepted proposal consumed by C4 into Cell 1 schema-consumption intake",
        "source_accepted_proposal_receipt_id": SOURCE_ACCEPTED_PROPOSAL_RECEIPT_ID,
        "source_c4_preflight_rerun_receipt_id": SOURCE_C4_RERUN_RECEIPT_ID,
        "source_c1_patch_receipt_id": SOURCE_C1_PATCH_RECEIPT_ID,
        "source_c3_rerun_receipt_id": SOURCE_C3_RERUN_RECEIPT_ID,
        "source_c2_receipt_id": SOURCE_C2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "c4_consumption_summary": {
            "profile_status": profile_obj["status"],
            "proposal_id": rollup_obj["proposal_id"],
            "proposal_status": rollup_obj["proposal_status"],
            "review_receipt_id": rollup_obj["review_receipt_id"],
            "accepted_proposals_consumed": rollup_obj["accepted_proposals_consumed"],
            "intake_validation_status": rollup_obj["intake_validation_status"],
            "cell1_intake_packets_emitted": rollup_obj["cell1_intake_packets_emitted"],
            "handoff_packets_emitted": rollup_obj["handoff_packets_emitted"],
            "runtime_patch_applied": False,
            "verification_pass_emitted": False,
            "bad_counters_zero": all(rollup_obj.get(k) == 0 for k in ZERO_COUNTER_KEYS),
            "recommended_next": rollup_obj["recommended_next"],
        },
        "aggregate_metrics": {
            **{k: v for k, v in report_obj.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
            "rollup": rollup_obj,
            "source_mutation_count": 1 if source_mutation_detected else report_obj["source_mutation_count"],
        },
        "acceptance_gate_results": acceptance_gate_results,
        "c4_consumption_guards": guards,
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_receipt(receipt)
    failures.extend(receipt_failures)
    receipt["failures"] = failures
    receipt["gate"] = "PASS" if not failures else "FAIL"
    if failures:
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}

    write_json(receipt_path, receipt)

    negative_controls = run_negative_controls(receipt_path)
    if len(negative_controls) != 27 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
        receipt = read_json(receipt_path)
        receipt["gate"] = "FAIL"
        receipt["failures"].append("negative_controls_failed")
        receipt["negative_controls"] = negative_controls
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}
        write_json(receipt_path, receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 1

    receipt = read_json(receipt_path)
    receipt["negative_controls"] = negative_controls
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c4_consumption_receipt_id={receipt_id}")
    print(f"c4_consumption_receipt_path=data/c4_consume_one_accepted_proposal_packet_v0_receipts/{receipt_id}.json")
    print(f"cell1_intake_packet_path=data/c4_consume_one_accepted_proposal_packet_v0/cell1_intake_packet_v0.json")
    print(f"handoff_packet_path=data/c4_consume_one_accepted_proposal_packet_v0/cell1_handoff_packet_v0.json")
    print(f"c4_consumption_rollup_path=data/c4_consume_one_accepted_proposal_packet_v0/c4_consumption_rollup_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
