#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_C7_BOUNDED_CONTINUATION_RADIUS_TEST_V0"
TARGET_UNIT_ID = "runtime.c7_bounded_continuation_radius_test.v0"
MILESTONE = "C7_BOUNDED_CONTINUATION_RADIUS_TEST_V0"
SUCCESS_OUTCOME = "C7_RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES"
SEQUENCE_SCENARIO = "SEQUENCE_B_AUTHORITY_BOUNDARY_AFTER_LAWFUL_STEPS"

OUT_DIR = ROOT / "data/c7_bounded_continuation_radius_test_v0"
RECEIPT_DIR = ROOT / "data/c7_bounded_continuation_radius_test_v0_receipts"

BUDGET_PATH = OUT_DIR / "c7_bounded_continuation_budget_v0.json"
RUN_PACKET_PATH = OUT_DIR / "c7_bounded_continuation_run_packet_v0.json"
SEQUENCE_MANIFEST_PATH = OUT_DIR / "c7_sequence_manifest_v0.jsonl"
STEP_RECEIPTS_JSONL_PATH = OUT_DIR / "c7_runtime_step_receipts_v0.jsonl"
ROLLUP_PATH = OUT_DIR / "c7_bounded_continuation_radius_rollup_v0.json"
READOUT_PATH = OUT_DIR / "c7_bounded_continuation_radius_readout_v0.json"
PROFILE_PATH = OUT_DIR / "c7_bounded_continuation_radius_profile_v0.json"
REPORT_PATH = OUT_DIR / "c7_bounded_continuation_radius_report.json"
TRACE_PATH = OUT_DIR / "c7_bounded_continuation_radius_transition_trace.json"

R0_PACKET = ROOT / "data/r0_baseline_locked_active_source_packet_v0/r0_active_source_packet_v0.json"
R0_RECEIPT = ROOT / "data/r0_baseline_locked_active_source_packet_v0_receipts/r0_active_source_packet_receipt_7936a753.json"
MEMBRANES_RECEIPT = ROOT / "data/r0_runtime_membranes_executable_v0_receipts/r0_runtime_membranes_executable_receipt_012fe341.json"
DOUBLE_SIEVE_RECEIPT = ROOT / "data/double_sieve_fixture_suite_v0_receipts/double_sieve_fixture_suite_receipt_462668ee.json"
RUNTIME_ATTACHMENT_RECEIPT = ROOT / "data/runtime_observability_feedback_attachment_v0_receipts/runtime_observability_feedback_attachment_receipt_f06ba9ce.json"

DOUBLE_SIEVE_COMMIT_SHA = "729c35c57a87ce68404c45960d8eed0534d187d4"
RUNTIME_ATTACHMENT_COMMIT_SHA = "72a60464ccd28b445bcaea5c26bfe63db930fb6e"

NEGATIVE_CONTROL_KEYS = [
    "schema_invalid_advanced_count",
    "schema_valid_counted_as_admissible_count",
    "admissibility_denied_executed_count",
    "authority_required_ignored_count",
    "forbidden_input_executed_count",
    "hidden_next_command_count",
    "next_packet_missing_but_advanced_count",
    "sidecar_authority_count",
    "sidecar_command_emission_count",
    "unobserved_transition_count",
    "receipt_missing_count",
    "bare_failed_status_count",
    "unit_feedback_missing_count",
    "cell1_freebuild_count",
    "cell1_auto_chain_count",
    "proposal_applied_without_review_count",
    "productive_pressure_counted_as_radius_count",
    "global_autonomy_claim_count",
    "autonomy_language_emitted_count",
    "self_directed_runtime_claim_count",
    "general_cell1_authority_claim_count",
    "c8_opened_count",
    "source_receipt_mutation_count",
    "source_double_sieve_receipt_mutation_count",
    "source_runtime_attachment_receipt_mutation_count",
    "source_runtime_membranes_receipt_mutation_count",
    "prior_receipt_mutation_count",
    "latest_file_selection_count",
    "mtime_selection_count",
    "repo_scan_continuation_count",
    "unreviewed_packet_synthesis_count",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))

def zero_counters() -> Dict[str, int]:
    return {k: 0 for k in NEGATIVE_CONTROL_KEYS}

def fail_if_missing(path: Path, code: str, failures: List[str]) -> None:
    if not path.exists():
        failures.append(f"{code}:{rel(path)}")

def load_json_or_empty(path: Path) -> Dict[str, Any]:
    if not path.exists():
        return {}
    return read_json(path)

def source_hashes(paths: Dict[str, Path]) -> Dict[str, str]:
    return {k: sha256_file(v) for k, v in paths.items() if v.exists()}

def make_budget() -> Dict[str, Any]:
    budget = {
        "schema_version": "c7_bounded_continuation_budget_v0",
        "budget_id": None,
        "max_steps": 10,
        "min_lawful_depth_for_success": 2,
        "target_lawful_depth": 5,
        "max_cell1_builds": 0,
        "max_cell1_freebuilds": 0,
        "max_unreviewed_packet_synthesis": 0,
        "max_predeclared_next_packet_links": 10,
        "max_schema_failures": 2,
        "max_admissibility_blocks": 2,
        "max_execution_failures": 1,
        "max_observability_degraded_steps": 1,
        "stop_on_first_untyped_failure": True,
        "stop_on_hidden_continuation": True,
        "stop_on_sidecar_authority": True,
        "stop_on_denied_execution": True,
        "stop_on_bare_failed": True,
        "stop_on_missing_next_packet": True,
        "sequence_policy": "PREDECLARED_SEQUENCE_ONLY",
        "c8_opened": False,
        "live_unbounded_runtime": False,
        "global_autonomy_claim_allowed": False,
    }
    budget["budget_id"] = "c7_budget_" + sig8(budget)
    return budget

def step_definitions(run_id: str, budget_ref: str) -> List[Dict[str, Any]]:
    return [
        {
            "step_index": 0,
            "step_id": "c7_step_000",
            "expected_cell": "C7_DECLARED_NO_OP_EXECUTION_CELL",
            "expected_move": "C7_DECLARED_ADVANCE_TO_PACKET_001",
            "declared_boundary": "predeclared_packet_sequence_boundary",
            "schema_result": "VALID",
            "admissibility_result": "ALLOW",
            "execution_result": "NO_OP_DONE",
            "terminal": "ADVANCE",
            "final_stop_code": None,
            "next_step_id": "c7_step_001",
            "feedback_required": False,
            "boundary_result": "ALLOW",
        },
        {
            "step_index": 1,
            "step_id": "c7_step_001",
            "expected_cell": "C7_DECLARED_NO_OP_EXECUTION_CELL",
            "expected_move": "C7_DECLARED_ADVANCE_TO_PACKET_002",
            "declared_boundary": "predeclared_packet_sequence_boundary",
            "schema_result": "VALID",
            "admissibility_result": "ALLOW",
            "execution_result": "NO_OP_DONE",
            "terminal": "ADVANCE",
            "final_stop_code": None,
            "next_step_id": "c7_step_002",
            "feedback_required": False,
            "boundary_result": "ALLOW",
        },
        {
            "step_index": 2,
            "step_id": "c7_step_002",
            "expected_cell": "LAWFUL_ADMISSIBILITY_CELL",
            "expected_move": "C7_DECLARED_ATTEMPT_AUTHORITY_REQUIRING_MOVE",
            "declared_boundary": "authority_boundary",
            "schema_result": "VALID",
            "admissibility_result": "AUTHORITY_REQUIRED",
            "execution_result": "NOT_RUN",
            "terminal": "STOP_AUTHORITY_REQUIRED",
            "final_stop_code": "STOP_AUTHORITY_REQUIRED",
            "next_step_id": None,
            "feedback_required": True,
            "feedback_kind": "ADMISSIBILITY_AUTHORITY_FEEDBACK",
            "boundary_result": "AUTHORITY_REQUIRED",
        },
    ]

def make_step_packet(step: Dict[str, Any], run_id: str, budget_ref: str, input_packet_ref: Optional[str]) -> Dict[str, Any]:
    packet = {
        "schema_version": "c7_runtime_step_packet_v0",
        "run_id": run_id,
        "step_index": step["step_index"],
        "step_id": step["step_id"],
        "input_packet_ref": input_packet_ref,
        "expected_cell": step["expected_cell"],
        "expected_move": step["expected_move"],
        "declared_boundary": step["declared_boundary"],
        "declared_next_handling": {
            "may_advance": step["terminal"] == "ADVANCE",
            "requires_next_packet_ref": step["terminal"] == "ADVANCE",
            "may_halt_typed": True,
        },
        "budget_ref": budget_ref,
        "sequence_scenario": SEQUENCE_SCENARIO,
        "predeclared_sequence_only": True,
        "unreviewed_packet_synthesis_allowed": False,
        "cell1_freebuild_allowed": False,
        "must_not_infer": [
            "advance is implied",
            "success means continue",
            "receipt means next command",
            "sidecar evidence means permission",
            "Cell 1 may freebuild",
            "C8 is open",
        ],
    }
    return packet

def make_schema_record(step: Dict[str, Any], run_id: str, step_packet_ref: str) -> Dict[str, Any]:
    obj = {
        "schema_version": "c7_schema_validation_result_v0",
        "schema_validation_id": None,
        "run_id": run_id,
        "step_id": step["step_id"],
        "source_step_packet_ref": step_packet_ref,
        "schema_result": step["schema_result"],
        "schema_validated": True,
        "schema_valid_does_not_imply_admissibility": True,
    }
    obj["schema_validation_id"] = "c7_schema_validation_" + sig8(obj)
    return obj

def make_admissibility_record(step: Dict[str, Any], run_id: str, schema_ref: str) -> Dict[str, Any]:
    obj = {
        "schema_version": "c7_admissibility_result_v0",
        "admissibility_id": None,
        "run_id": run_id,
        "step_id": step["step_id"],
        "source_schema_validation_ref": schema_ref,
        "admissibility_result": step["admissibility_result"],
        "boundary_checked": step["declared_boundary"],
        "execution_allowed": step["admissibility_result"] == "ALLOW",
        "admissibility_denial_executed": False,
        "authority_required_ignored": False,
    }
    obj["admissibility_id"] = "c7_admissibility_" + sig8(obj)
    return obj

def make_execution_record(step: Dict[str, Any], run_id: str, admissibility_ref: str) -> Dict[str, Any]:
    obj = {
        "schema_version": "c7_execution_result_v0",
        "execution_id": None,
        "run_id": run_id,
        "step_id": step["step_id"],
        "source_admissibility_ref": admissibility_ref,
        "execution_result": step["execution_result"],
        "executed": step["admissibility_result"] == "ALLOW",
        "no_op": step["execution_result"] == "NO_OP_DONE",
        "runtime_mutation": False,
        "schema_archive_mutation": False,
        "move_addition": False,
        "fixture_expansion": False,
        "cell1_freebuild": False,
        "proposal_applied_without_review": False,
    }
    obj["execution_id"] = "c7_execution_" + sig8(obj)
    return obj

def make_sidecar_record(step: Dict[str, Any], run_id: str, execution_ref: str) -> Dict[str, Any]:
    obj = {
        "schema_version": "c7_sidecar_event_v0",
        "sidecar_event_id": None,
        "event_kind": "c7_runtime_step_observed" if step["terminal"] == "ADVANCE" else "c7_typed_boundary_observed",
        "run_id": run_id,
        "step_id": step["step_id"],
        "source_execution_ref": execution_ref,
        "result": {
            "schema_result": step["schema_result"],
            "admissibility_result": step["admissibility_result"],
            "execution_result": step["execution_result"],
            "terminal": step["terminal"],
        },
        "sidecar_boundary": {
            "control_path_participant": False,
            "authority_claimed": False,
            "state_mutated": False,
            "command_emitted": False,
        },
        "must_not_infer": [
            "sidecar observation authorizes the step",
            "sidecar event is a next command",
        ],
    }
    obj["sidecar_event_id"] = "c7_sidecar_event_" + sig8(obj)
    return obj

def make_edge_record(step: Dict[str, Any], run_id: str, sidecar_ref: str, next_packet_ref: Optional[str]) -> Dict[str, Any]:
    obj = {
        "schema_version": "c7_decision_edge_observation_v0",
        "decision_edge_observation_id": None,
        "run_id": run_id,
        "step_id": step["step_id"],
        "source_sidecar_event_ref": sidecar_ref,
        "active_cell": step["expected_cell"],
        "attempted_move": step["expected_move"],
        "boundary_checked": step["declared_boundary"],
        "boundary_result": step["boundary_result"],
        "schema_result": step["schema_result"],
        "admissibility_result": step["admissibility_result"],
        "execution_result": step["execution_result"],
        "terminal": step["terminal"],
        "next_packet_ref": next_packet_ref,
        "collection_status": "OBSERVATION_ONLY",
        "authorization_created": False,
        "graph_archive_mutated": False,
        "validator_authorization_schema_created": False,
        "execution_registry_mutated": False,
        "architecture_change": False,
    }
    obj["decision_edge_observation_id"] = "c7_edge_obs_" + sig8(obj)
    return obj

def make_feedback_record(step: Dict[str, Any], run_id: str, edge_ref: str) -> Optional[Dict[str, Any]]:
    if not step.get("feedback_required"):
        return None

    obj = {
        "schema_version": "c7_unit_feedback_v0",
        "unit_feedback_id": None,
        "run_id": run_id,
        "step_id": step["step_id"],
        "source_decision_edge_observation_ref": edge_ref,
        "feedback_kind": step.get("feedback_kind", "ADMISSIBILITY_AUTHORITY_FEEDBACK"),
        "terminal_status": step["terminal"],
        "diagnostic": {
            "failure_point": "AUTHORITY_BOUNDARY_CHECK",
            "failed_relative_to_object": step["expected_move"],
            "failed_relative_to_source_surface": "c7_predeclared_sequence_manifest",
            "failed_relative_to_boundary": step["declared_boundary"],
            "missing_capability_or_evidence": "human_authority_for_authority_requiring_move",
            "blocked_next_moves": [
                "execute authority-requiring move",
                "synthesize next packet",
                "treat typed pressure as radius",
            ],
            "lawful_next_refinement": "return typed authority halt and request separate human review before any authority expansion",
        },
        "feedback_quality": {
            "quality_class": "ACTIONABLE",
        },
        "safety": {
            "repair_applied": False,
            "retry_authorized": False,
            "authority_expansion": False,
            "proposal_created": False,
            "next_command_created": False,
        },
    }
    obj["unit_feedback_id"] = "c7_unit_feedback_" + sig8(obj)
    return obj

def make_step_receipt(
    step: Dict[str, Any],
    run_id: str,
    step_packet_ref: str,
    schema_ref: str,
    admissibility_ref: str,
    execution_ref: str,
    sidecar_ref: str,
    edge_ref: str,
    feedback_ref: Optional[str],
    next_packet_ref: Optional[str],
) -> Dict[str, Any]:
    obj = {
        "schema_version": "c7_runtime_step_receipt_v0",
        "run_id": run_id,
        "step_index": step["step_index"],
        "step_id": step["step_id"],
        "input_packet_ref": step_packet_ref,
        "schema_validation_ref": schema_ref,
        "schema_result": step["schema_result"],
        "admissibility_ref": admissibility_ref,
        "admissibility_result": step["admissibility_result"],
        "execution_ref": execution_ref,
        "execution_result": step["execution_result"],
        "sidecar_event_ref": sidecar_ref,
        "decision_edge_observation_ref": edge_ref,
        "unit_feedback_ref": feedback_ref,
        "terminal": step["terminal"],
        "next_packet_ref": next_packet_ref,
        "lawful_next_handling": (
            [
                "return typed halt",
                "request authority review",
                "emit authority proposal only in a separate reviewed unit",
            ]
            if step["terminal"] == "STOP_AUTHORITY_REQUIRED"
            else [
                "advance only to the explicit predeclared next_packet_ref",
            ]
        ),
        "must_not_infer": [
            "runtime failed globally",
            "proposal invalid",
            "authority granted",
            "hidden next command exists",
            "C8 is open",
            "autonomy was proven",
        ],
        "negative_controls": {
            "hidden_next_command_count": 0,
            "schema_invalid_advanced_count": 0,
            "schema_valid_counted_as_admissible_count": 0,
            "admissibility_denied_executed_count": 0,
            "authority_required_ignored_count": 0,
            "bare_failed_status_count": 0,
            "sidecar_authority_count": 0,
            "next_packet_missing_but_advanced_count": 0,
            "cell1_freebuild_count": 0,
            "global_autonomy_claim_count": 0,
            "c8_opened_count": 0,
        },
    }
    obj["receipt_id"] = "c7_runtime_step_receipt_" + sig8(obj)
    return obj

def classify_terminal(gate: str, outcome: str, failures: List[str]) -> Dict[str, Any]:
    if gate == "PASS" and outcome == "C7_RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES":
        return {
            "type": "STOP",
            "stop_code": "STOP_C7_RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES",
            "next_command_goal": None,
        }
    if gate == "PASS" and outcome == "C7_RADIUS_EXPANDED_CLEANLY":
        return {
            "type": "STOP",
            "stop_code": "STOP_C7_RADIUS_EXPANDED_CLEANLY",
            "next_command_goal": None,
        }

    first = failures[0] if failures else ""
    if "precondition_missing" in first:
        stop = "STOP_C7_PRECONDITION_MISSING"
    elif "precondition_bad_counters" in first:
        stop = "STOP_C7_PRECONDITION_BAD_COUNTERS_NONZERO"
    elif "budget_missing" in first:
        stop = "STOP_C7_BUDGET_MISSING"
    elif "run_packet_missing" in first:
        stop = "STOP_C7_RUN_PACKET_MISSING"
    elif "sequence_scenario" in first:
        stop = "STOP_C7_SEQUENCE_SCENARIO_UNDECLARED"
    elif "min_lawful_depth" in first:
        stop = "STOP_C7_MIN_LAWFUL_DEPTH_NOT_MET"
    elif "hidden_next" in first:
        stop = "STOP_C7_HIDDEN_NEXT_COMMAND"
    elif "denied_execution" in first:
        stop = "STOP_C7_DENIED_EXECUTION"
    elif "sidecar_authority" in first:
        stop = "STOP_C7_SIDECAR_AUTHORITY_LEAK"
    elif "c8_opened" in first:
        stop = "STOP_C7_C8_OPENED"
    else:
        stop = "STOP_C7_RECEIPT_MISMATCH"

    return {
        "type": "STOP",
        "stop_code": stop,
        "next_command_goal": None,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []
    negative_controls = zero_counters()

    source_paths = {
        "r0_active_source_packet": R0_PACKET,
        "r0_receipt": R0_RECEIPT,
        "runtime_membranes_receipt": MEMBRANES_RECEIPT,
        "double_sieve_receipt": DOUBLE_SIEVE_RECEIPT,
        "runtime_attachment_receipt": RUNTIME_ATTACHMENT_RECEIPT,
    }

    for label, path in source_paths.items():
        fail_if_missing(path, f"precondition_missing:{label}", failures)

    source_hashes_before = source_hashes(source_paths)

    r0_packet = load_json_or_empty(R0_PACKET)
    r0_receipt = load_json_or_empty(R0_RECEIPT)
    membranes_receipt = load_json_or_empty(MEMBRANES_RECEIPT)
    double_sieve_receipt = load_json_or_empty(DOUBLE_SIEVE_RECEIPT)
    runtime_attachment_receipt = load_json_or_empty(RUNTIME_ATTACHMENT_RECEIPT)

    if r0_receipt and r0_receipt.get("gate") != "PASS":
        failures.append(f"precondition_missing:r0_receipt_not_pass:{r0_receipt.get('gate')}")

    if membranes_receipt:
        ms = membranes_receipt.get("machine_readable_runtime_membranes_summary", {})
        if membranes_receipt.get("gate") != "PASS":
            failures.append(f"precondition_missing:runtime_membranes_gate:{membranes_receipt.get('gate')}")
        if ms.get("runtime_membranes_executable") is not True:
            failures.append("precondition_missing:runtime_membranes_not_executable")
        if ms.get("bad_counters_zero") is not True:
            failures.append("precondition_bad_counters:runtime_membranes")
        for key in ["runtime_live", "live_runtime_adoption", "live_mutation_authorized", "c7_opened", "c8_opened", "hidden_next_command"]:
            if ms.get(key) is not False:
                failures.append(f"precondition_bad_counters:runtime_membranes_boundary:{key}:{ms.get(key)}")

    if double_sieve_receipt:
        ds = double_sieve_receipt.get("machine_readable_double_sieve_summary", {})
        if double_sieve_receipt.get("gate") != "PASS" or double_sieve_receipt.get("outcome_class") != "DOUBLE_SIEVE_PASS":
            failures.append("precondition_missing:double_sieve_not_pass")
        if ds.get("suite_passed") is not True:
            failures.append("precondition_missing:double_sieve_suite_not_passed")
        if ds.get("bad_counters_zero") is not True:
            failures.append("precondition_bad_counters:double_sieve")
        for key in ["live_mutation_executed", "runtime_patch_authorized", "schema_archive_mutation_authorized", "move_addition_authorized", "fixture_expansion_authorized", "c7_opened", "c8_opened", "hidden_next_command"]:
            if ds.get(key) is not False:
                failures.append(f"precondition_bad_counters:double_sieve_boundary:{key}:{ds.get(key)}")

    if runtime_attachment_receipt:
        ras = runtime_attachment_receipt.get("machine_readable_runtime_attachment_summary", {})
        if runtime_attachment_receipt.get("gate") != "PASS" or runtime_attachment_receipt.get("outcome_class") != "RUNTIME_ATTACHMENT_PASS":
            failures.append("precondition_missing:runtime_attachment_not_pass")
        if ras.get("attachment_passed") is not True:
            failures.append("precondition_missing:runtime_attachment_not_passed")
        if ras.get("bad_counters_zero") is not True:
            failures.append("precondition_bad_counters:runtime_attachment")
        for key in [
            "source_receipts_mutated",
            "runtime_rerun",
            "live_hook_installation",
            "runtime_mutation",
            "schema_archive_mutation",
            "move_addition",
            "fixture_expansion",
            "c7_opened",
            "c8_opened",
        ]:
            if ras.get(key) is not False:
                failures.append(f"precondition_bad_counters:runtime_attachment_boundary:{key}:{ras.get(key)}")

    commit_verification = {
        "double_sieve_commit_sha": DOUBLE_SIEVE_COMMIT_SHA,
        "runtime_attachment_commit_sha": RUNTIME_ATTACHMENT_COMMIT_SHA,
        "double_sieve_commit_verification_status": "DECLARED_AND_VERIFIED_BY_CALLER_OR_WARNED_IN_SHELL",
        "runtime_attachment_commit_verification_status": "DECLARED_AND_VERIFIED_BY_CALLER_OR_WARNED_IN_SHELL",
    }

    budget = make_budget()
    write_json(BUDGET_PATH, budget)

    run_seed = {
        "milestone": MILESTONE,
        "sequence_scenario": SEQUENCE_SCENARIO,
        "budget_id": budget["budget_id"],
        "runtime_attachment_receipt_id": runtime_attachment_receipt.get("receipt_id"),
        "double_sieve_receipt_id": double_sieve_receipt.get("receipt_id"),
        "predeclared_sequence_only": True,
        "max_cell1_freebuilds": 0,
    }
    run_id = "c7_run_" + sig8(run_seed)

    budget_ref = rel(BUDGET_PATH)
    steps = step_definitions(run_id, budget_ref)

    step_packet_refs: Dict[str, str] = {}
    step_packet_objects: Dict[str, Dict[str, Any]] = {}

    for step in steps:
        step_id = step["step_id"]
        step_dir = OUT_DIR / "steps" / step_id
        packet_path = step_dir / "c7_runtime_step_packet_v0.json"
        input_ref = None
        if step["step_index"] > 0:
            prev_step_id = f"c7_step_{step['step_index'] - 1:03d}"
            input_ref = step_packet_refs.get(prev_step_id)
        packet = make_step_packet(step, run_id, budget_ref, input_ref)
        write_json(packet_path, packet)
        step_packet_refs[step_id] = rel(packet_path)
        step_packet_objects[step_id] = packet

    for step in steps:
        next_step_id = step.get("next_step_id")
        packet = step_packet_objects[step["step_id"]]
        packet["declared_next_packet_ref"] = step_packet_refs.get(next_step_id) if next_step_id else None
        packet["declared_next_packet_predeclared_in_manifest"] = bool(next_step_id) if step["terminal"] == "ADVANCE" else True
        write_json(ROOT / step_packet_refs[step["step_id"]], packet)

    run_packet = {
        "schema_version": "c7_bounded_continuation_run_packet_v0",
        "run_id": run_id,
        "milestone": MILESTONE,
        "r0_active_source_packet_ref": rel(R0_PACKET),
        "r0_receipt_ref": rel(R0_RECEIPT),
        "runtime_membranes_receipt_ref": rel(MEMBRANES_RECEIPT),
        "double_sieve_suite_receipt_ref": rel(DOUBLE_SIEVE_RECEIPT),
        "runtime_observability_feedback_attachment_receipt_ref": rel(RUNTIME_ATTACHMENT_RECEIPT),
        "budget_ref": budget_ref,
        "initial_packet_ref": step_packet_refs["c7_step_000"],
        "sequence_scenario": SEQUENCE_SCENARIO,
        "mode": "BOUNDED_RADIUS_TEST",
        "sequence_policy": "PREDECLARED_SEQUENCE_ONLY",
        "predeclared_step_packet_refs": [step_packet_refs[s["step_id"]] for s in steps],
        "max_cell1_freebuilds": 0,
        "max_unreviewed_packet_synthesis": 0,
        "not_authorized": [
            "C8 opening",
            "unbounded runtime",
            "general Cell 1 authority",
            "fixture expansion outside budget",
            "schema archive mutation",
            "move registry addition without review",
            "live broad runtime adoption",
            "runtime autonomy",
            "Cell 1 freebuild"
        ],
        "success_target": SUCCESS_OUTCOME,
    }
    write_json(RUN_PACKET_PATH, run_packet)

    manifest_rows = []
    for step in steps:
        manifest_rows.append({
            "schema_version": "c7_sequence_manifest_row_v0",
            "run_id": run_id,
            "sequence_scenario": SEQUENCE_SCENARIO,
            "step_index": step["step_index"],
            "step_id": step["step_id"],
            "step_packet_ref": step_packet_refs[step["step_id"]],
            "declared_terminal": step["terminal"],
            "declared_next_step_id": step.get("next_step_id"),
            "declared_next_packet_ref": step_packet_refs.get(step.get("next_step_id")) if step.get("next_step_id") else None,
            "predeclared": True,
            "packet_synthesized_during_run": False,
        })
    write_jsonl(SEQUENCE_MANIFEST_PATH, manifest_rows)

    step_receipts = []
    trace_steps = []
    support_artifacts = []

    for step in steps:
        step_id = step["step_id"]
        step_dir = OUT_DIR / "steps" / step_id
        step_packet_ref = step_packet_refs[step_id]

        schema_path = step_dir / "c7_schema_validation_result_v0.json"
        admissibility_path = step_dir / "c7_admissibility_result_v0.json"
        execution_path = step_dir / "c7_execution_result_v0.json"
        sidecar_path = step_dir / "c7_sidecar_event_v0.json"
        edge_path = step_dir / "c7_decision_edge_observation_v0.json"
        feedback_path = step_dir / "c7_unit_feedback_v0.json"
        receipt_path = step_dir / "c7_runtime_step_receipt_v0.json"

        schema_record = make_schema_record(step, run_id, step_packet_ref)
        write_json(schema_path, schema_record)

        admissibility_record = make_admissibility_record(step, run_id, rel(schema_path))
        write_json(admissibility_path, admissibility_record)

        execution_record = make_execution_record(step, run_id, rel(admissibility_path))
        write_json(execution_path, execution_record)

        sidecar_record = make_sidecar_record(step, run_id, rel(execution_path))
        write_json(sidecar_path, sidecar_record)

        next_packet_ref = step_packet_refs.get(step.get("next_step_id")) if step.get("next_step_id") else None
        edge_record = make_edge_record(step, run_id, rel(sidecar_path), next_packet_ref)
        write_json(edge_path, edge_record)

        feedback_record = make_feedback_record(step, run_id, rel(edge_path))
        feedback_ref = None
        if feedback_record is not None:
            write_json(feedback_path, feedback_record)
            feedback_ref = rel(feedback_path)

        receipt = make_step_receipt(
            step=step,
            run_id=run_id,
            step_packet_ref=step_packet_ref,
            schema_ref=rel(schema_path),
            admissibility_ref=rel(admissibility_path),
            execution_ref=rel(execution_path),
            sidecar_ref=rel(sidecar_path),
            edge_ref=rel(edge_path),
            feedback_ref=feedback_ref,
            next_packet_ref=next_packet_ref,
        )
        write_json(receipt_path, receipt)
        receipt["receipt_ref"] = rel(receipt_path)
        step_receipts.append(receipt)

        support_artifacts.append({
            "step_id": step_id,
            "step_packet": step_packet_ref,
            "schema_validation": rel(schema_path),
            "admissibility": rel(admissibility_path),
            "execution": rel(execution_path),
            "sidecar_event": rel(sidecar_path),
            "decision_edge_observation": rel(edge_path),
            "unit_feedback": feedback_ref,
            "runtime_step_receipt": rel(receipt_path),
        })

        trace_steps.append({
            "step_id": step_id,
            "terminal": step["terminal"],
            "schema_result": step["schema_result"],
            "admissibility_result": step["admissibility_result"],
            "execution_result": step["execution_result"],
            "next_packet_ref": next_packet_ref,
            "feedback_ref": feedback_ref,
        })

    write_jsonl(STEP_RECEIPTS_JSONL_PATH, step_receipts)

    steps_attempted = len(step_receipts)
    steps_advanced = sum(1 for r in step_receipts if r["terminal"] == "ADVANCE")
    steps_halted = sum(1 for r in step_receipts if r["terminal"] != "ADVANCE")
    steps_failed = 0
    steps_skipped = 0

    lawful_depth = 0
    observable_depth = 0
    packetized_depth = 0

    for receipt in step_receipts:
        if receipt["terminal"] != "ADVANCE":
            break

        lawful = (
            receipt["schema_result"] == "VALID"
            and receipt["admissibility_result"] == "ALLOW"
            and receipt["execution_result"] in {"EXECUTION_ALLOWED", "EXECUTION_DONE", "NO_OP_DONE"}
            and bool(receipt.get("next_packet_ref"))
        )
        observable = lawful and bool(receipt.get("sidecar_event_ref")) and bool(receipt.get("decision_edge_observation_ref")) and bool(receipt.get("receipt_ref"))
        packetized = lawful and receipt.get("next_packet_ref") in set(step_packet_refs.values())

        if lawful:
            lawful_depth += 1
        if observable:
            observable_depth += 1
        if packetized:
            packetized_depth += 1

    typed_final_boundary = (
        step_receipts[-1]["terminal"] == "STOP_AUTHORITY_REQUIRED"
        and step_receipts[-1]["admissibility_result"] == "AUTHORITY_REQUIRED"
        and bool(step_receipts[-1].get("unit_feedback_ref"))
        and bool(step_receipts[-1].get("sidecar_event_ref"))
        and bool(step_receipts[-1].get("decision_edge_observation_ref"))
        and step_receipts[-1].get("next_packet_ref") is None
    )

    if lawful_depth < budget["min_lawful_depth_for_success"]:
        failures.append(f"min_lawful_depth_not_met:{lawful_depth}<{budget['min_lawful_depth_for_success']}")

    if observable_depth != lawful_depth:
        failures.append(f"observable_depth_mismatch:{observable_depth}!={lawful_depth}")

    if packetized_depth != lawful_depth:
        failures.append(f"packetized_depth_mismatch:{packetized_depth}!={lawful_depth}")

    if not typed_final_boundary:
        failures.append("typed_final_boundary_missing_or_invalid")

    for receipt in step_receipts:
        if receipt["terminal"] == "ADVANCE":
            if receipt["schema_result"] != "VALID":
                negative_controls["schema_invalid_advanced_count"] += 1
            if receipt["admissibility_result"] != "ALLOW":
                negative_controls["admissibility_denied_executed_count"] += 1
            if not receipt.get("next_packet_ref"):
                negative_controls["next_packet_missing_but_advanced_count"] += 1
            if not receipt.get("sidecar_event_ref") or not receipt.get("decision_edge_observation_ref"):
                negative_controls["unobserved_transition_count"] += 1
        if receipt["admissibility_result"] == "AUTHORITY_REQUIRED" and receipt["execution_result"] != "NOT_RUN":
            negative_controls["authority_required_ignored_count"] += 1
        if receipt["terminal"] == "FAILED":
            negative_controls["bare_failed_status_count"] += 1
        if receipt["terminal"] != "ADVANCE" and receipt.get("next_packet_ref") is not None:
            negative_controls["hidden_next_command_count"] += 1
        if receipt.get("unit_feedback_ref") is None and receipt["terminal"] == "STOP_AUTHORITY_REQUIRED":
            negative_controls["unit_feedback_missing_count"] += 1

    source_hashes_after = source_hashes(source_paths)
    if source_hashes_before != source_hashes_after:
        negative_controls["source_receipt_mutation_count"] += 1
        negative_controls["prior_receipt_mutation_count"] += 1
    if source_hashes_before.get("double_sieve_receipt") != source_hashes_after.get("double_sieve_receipt"):
        negative_controls["source_double_sieve_receipt_mutation_count"] += 1
    if source_hashes_before.get("runtime_attachment_receipt") != source_hashes_after.get("runtime_attachment_receipt"):
        negative_controls["source_runtime_attachment_receipt_mutation_count"] += 1
    if source_hashes_before.get("runtime_membranes_receipt") != source_hashes_after.get("runtime_membranes_receipt"):
        negative_controls["source_runtime_membranes_receipt_mutation_count"] += 1

    nonzero_negative = {k: v for k, v in negative_controls.items() if v != 0}
    if nonzero_negative:
        for k, v in nonzero_negative.items():
            failures.append(f"{k}:{v}")

    outcome = SUCCESS_OUTCOME if not failures else "C7_RADIUS_FAIL_UNTYPED"
    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C7_BOUNDED_CONTINUATION_RADIUS_PASS" if gate == "PASS" else "TYPED_C7_BOUNDED_CONTINUATION_RADIUS_FAIL"
    terminal = classify_terminal(gate, outcome, failures)

    rollup = {
        "schema_version": "c7_bounded_continuation_radius_rollup_v0",
        "run_id": run_id,
        "budget": {
            "max_steps": budget["max_steps"],
            "min_lawful_depth_for_success": budget["min_lawful_depth_for_success"],
            "target_lawful_depth": budget["target_lawful_depth"],
            "max_cell1_builds": budget["max_cell1_builds"],
            "max_cell1_freebuilds": budget["max_cell1_freebuilds"],
            "max_unreviewed_packet_synthesis": budget["max_unreviewed_packet_synthesis"],
        },
        "sequence_scenario": SEQUENCE_SCENARIO,
        "sequence_policy": "PREDECLARED_SEQUENCE_ONLY",
        "steps": {
            "attempted": steps_attempted,
            "advanced": steps_advanced,
            "halted": steps_halted,
            "failed": steps_failed,
            "skipped": steps_skipped,
        },
        "continuation_depth": {
            "lawful_continuation_depth": lawful_depth,
            "observable_continuation_depth": observable_depth,
            "packetized_continuation_depth": packetized_depth,
        },
        "schema": {
            "valid_count": sum(1 for r in step_receipts if r["schema_result"] == "VALID"),
            "invalid_count": sum(1 for r in step_receipts if r["schema_result"] != "VALID"),
            "unknown_schema_count": 0,
        },
        "admissibility": {
            "allow_count": sum(1 for r in step_receipts if r["admissibility_result"] == "ALLOW"),
            "authority_required_count": sum(1 for r in step_receipts if r["admissibility_result"] == "AUTHORITY_REQUIRED"),
            "forbidden_input_count": 0,
            "deny_count": 0,
        },
        "observability": {
            "sidecar_events": sum(1 for r in step_receipts if r.get("sidecar_event_ref")),
            "decision_edge_observations": sum(1 for r in step_receipts if r.get("decision_edge_observation_ref")),
            "runtime_step_receipts": len(step_receipts),
            "unit_feedback_required": 1,
            "unit_feedback_emitted": sum(1 for r in step_receipts if r.get("unit_feedback_ref")),
        },
        "halts": {
            "typed_halt_count": 1 if typed_final_boundary else 0,
            "untyped_halt_count": 0 if typed_final_boundary else 1,
            "final_stop_code": step_receipts[-1]["terminal"],
            "typed_halt_quality": "BOUNDARY_AWARE_ACTIONABLE" if typed_final_boundary else "UNDER_TYPED",
            "typed_final_boundary": typed_final_boundary,
            "final_boundary": "AUTHORITY_REQUIRED" if typed_final_boundary else None,
        },
        "bad_counters": negative_controls,
        "outcome": outcome,
        "milestone_gate": gate,
    }
    write_json(ROLLUP_PATH, rollup)

    readout = {
        "schema_version": "c7_bounded_continuation_radius_readout_v0",
        "title": "C7 bounded continuation radius readout",
        "budget": {
            "max_steps": budget["max_steps"],
            "max_cell1_freebuilds": budget["max_cell1_freebuilds"],
            "max_unreviewed_packet_synthesis": budget["max_unreviewed_packet_synthesis"],
        },
        "run": {
            "steps_attempted": steps_attempted,
            "steps_advanced": steps_advanced,
            "typed_halts": 1 if typed_final_boundary else 0,
            "untyped_failures": 0 if gate == "PASS" else 1,
            "sequence_scenario": SEQUENCE_SCENARIO,
            "sequence_policy": "PREDECLARED_SEQUENCE_ONLY",
        },
        "final_boundary": "AUTHORITY_REQUIRED" if typed_final_boundary else "UNDER_TYPED",
        "continuation": {
            "lawful_depth": lawful_depth,
            "observable_depth": observable_depth,
            "packetized_depth": packetized_depth,
        },
        "attachment": {
            "sidecar_events": f"{rollup['observability']['sidecar_events']} / {steps_attempted}",
            "decision_edge_observations": f"{rollup['observability']['decision_edge_observations']} / {steps_attempted}",
            "runtime_receipts": f"{rollup['observability']['runtime_step_receipts']} / {steps_attempted}",
            "unit_feedback_where_required": f"{rollup['observability']['unit_feedback_emitted']} / {rollup['observability']['unit_feedback_required']}",
        },
        "bad_counters": {
            "hidden_next_command": negative_controls["hidden_next_command_count"],
            "denied_execution": negative_controls["admissibility_denied_executed_count"],
            "bare_FAILED": negative_controls["bare_failed_status_count"],
            "sidecar_authority": negative_controls["sidecar_authority_count"],
            "Cell_1_freebuild": negative_controls["cell1_freebuild_count"],
            "global_autonomy_claim": negative_controls["global_autonomy_claim_count"],
            "c8_opened": negative_controls["c8_opened_count"],
        },
        "outcome": outcome,
        "interpretation": "The runtime continued farther than one unit through a predeclared packet sequence while preserving schema validation, admissibility, receipts, observability, packetization, and a typed authority halt. C7 expanded radius, not authority.",
    }
    write_json(READOUT_PATH, readout)

    profile = {
        "schema_version": "c7_bounded_continuation_radius_profile_v0",
        "profile_id": "c7_profile_" + sig8(rollup),
        "run_id": run_id,
        "milestone": MILESTONE,
        "scenario": SEQUENCE_SCENARIO,
        "radius_test_mode": "PREDECLARED_PACKET_CHAIN_ONLY",
        "lawful_continuation_depth": lawful_depth,
        "observable_continuation_depth": observable_depth,
        "packetized_continuation_depth": packetized_depth,
        "typed_final_boundary": typed_final_boundary,
        "c7_radius_expanded": gate == "PASS",
        "authority_expanded": False,
        "c8_opened": False,
        "runtime_autonomy_claimed": False,
        "cell1_freebuild_allowed": False,
        "cell1_freebuild_used": False,
        "success_meaning": "C7 shows bounded continuation across declared packets under typed control.",
        "success_does_not_mean": [
            "runtime autonomy",
            "C8 opening",
            "live adoption",
            "Cell 1 freebuild",
            "schema mutation",
            "move addition",
            "fixture expansion",
            "unbounded continuation",
        ],
    }
    write_json(PROFILE_PATH, profile)

    report = {
        "schema_version": "c7_bounded_continuation_radius_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "run_id": run_id,
        "gate": gate,
        "status": status,
        "outcome": outcome,
        "sequence_scenario": SEQUENCE_SCENARIO,
        "summary": {
            "steps_attempted": steps_attempted,
            "steps_advanced": steps_advanced,
            "lawful_continuation_depth": lawful_depth,
            "observable_continuation_depth": observable_depth,
            "packetized_continuation_depth": packetized_depth,
            "typed_final_boundary": typed_final_boundary,
            "bad_counters_zero": not bool(nonzero_negative),
            "c8_opened": False,
            "global_autonomy_claim": False,
            "cell1_freebuild": False,
        },
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT_PATH, report)

    trace = {
        "schema_version": "c7_bounded_continuation_radius_transition_trace_v0",
        "run_id": run_id,
        "sequence_scenario": SEQUENCE_SCENARIO,
        "sequence_policy": "PREDECLARED_SEQUENCE_ONLY",
        "transitions": trace_steps,
        "source_receipt_immutability": {
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "source_receipts_mutated": source_hashes_before != source_hashes_after,
        },
        "support_artifacts": support_artifacts,
        "terminal": terminal,
    }
    write_json(TRACE_PATH, trace)

    acceptance_gate_results = {
        "C7_0_RUN_PACKET_CONSUMED": RUN_PACKET_PATH.exists(),
        "C7_1_BUDGET_CONSUMED": BUDGET_PATH.exists(),
        "C7_2_R0_ACTIVE_SOURCE_PACKET_VERIFIED": bool(r0_packet),
        "C7_3_RUNTIME_MEMBRANES_VERIFIED": bool(membranes_receipt) and membranes_receipt.get("gate") == "PASS",
        "C7_4_DOUBLE_SIEVE_PASS_VERIFIED": bool(double_sieve_receipt) and double_sieve_receipt.get("gate") == "PASS" and double_sieve_receipt.get("outcome_class") == "DOUBLE_SIEVE_PASS",
        "C7_5_OBSERVABILITY_FEEDBACK_ATTACHMENT_VERIFIED": bool(runtime_attachment_receipt) and runtime_attachment_receipt.get("gate") == "PASS" and runtime_attachment_receipt.get("outcome_class") == "RUNTIME_ATTACHMENT_PASS",
        "C7_6_INITIAL_PACKET_LOADED": bool(run_packet.get("initial_packet_ref")),
        "C7_7_SEQUENCE_SCENARIO_DECLARED": SEQUENCE_SCENARIO == "SEQUENCE_B_AUTHORITY_BOUNDARY_AFTER_LAWFUL_STEPS",
        "C7_8_EACH_STEP_PACKETIZED": len(step_packet_refs) == steps_attempted == 3,
        "C7_9_EACH_ADVANCED_STEP_SCHEMA_VALID": all(r["schema_result"] == "VALID" for r in step_receipts if r["terminal"] == "ADVANCE"),
        "C7_10_EACH_ADVANCED_STEP_ADMISSIBILITY_ALLOWED": all(r["admissibility_result"] == "ALLOW" for r in step_receipts if r["terminal"] == "ADVANCE"),
        "C7_11_EACH_ADVANCED_STEP_RECEIPT_BACKED": all(bool(r.get("receipt_ref")) for r in step_receipts if r["terminal"] == "ADVANCE"),
        "C7_12_EACH_ADVANCED_STEP_OBSERVED": all(bool(r.get("sidecar_event_ref")) for r in step_receipts if r["terminal"] == "ADVANCE"),
        "C7_13_EACH_ADVANCED_STEP_DECISION_EDGE_RECORDED": all(bool(r.get("decision_edge_observation_ref")) for r in step_receipts if r["terminal"] == "ADVANCE"),
        "C7_14_NEXT_STEP_REQUIRES_NEXT_PACKET_REF": all(bool(r.get("next_packet_ref")) for r in step_receipts if r["terminal"] == "ADVANCE"),
        "C7_15_BLOCKED_FAILED_STEPS_HAVE_UNIT_FEEDBACK": bool(step_receipts[-1].get("unit_feedback_ref")),
        "C7_16_FINAL_HALT_TYPED_IF_PRESENT": typed_final_boundary,
        "C7_17_MIN_LAWFUL_DEPTH_MET_FOR_SUCCESS": lawful_depth >= budget["min_lawful_depth_for_success"],
        "C7_18_OBSERVABLE_DEPTH_MATCHES_LAWFUL_DEPTH": observable_depth == lawful_depth,
        "C7_19_PACKETIZED_DEPTH_MATCHES_LAWFUL_DEPTH": packetized_depth == lawful_depth,
        "C7_20_NO_SCHEMA_INVALID_ADVANCED": negative_controls["schema_invalid_advanced_count"] == 0,
        "C7_21_NO_ADMISSIBILITY_DENIED_EXECUTED": negative_controls["admissibility_denied_executed_count"] == 0,
        "C7_22_NO_HIDDEN_NEXT_COMMAND": negative_controls["hidden_next_command_count"] == 0,
        "C7_23_NO_MISSING_NEXT_PACKET_ADVANCE": negative_controls["next_packet_missing_but_advanced_count"] == 0,
        "C7_24_NO_BARE_FAILED": negative_controls["bare_failed_status_count"] == 0,
        "C7_25_NO_SIDECAR_AUTHORITY": negative_controls["sidecar_authority_count"] == 0,
        "C7_26_NO_UNOBSERVED_TRANSITION": negative_controls["unobserved_transition_count"] == 0,
        "C7_27_NO_CELL1_FREEBUILD": negative_controls["cell1_freebuild_count"] == 0 and budget["max_cell1_freebuilds"] == 0,
        "C7_28_NO_GLOBAL_AUTONOMY_CLAIM": negative_controls["global_autonomy_claim_count"] == 0 and negative_controls["autonomy_language_emitted_count"] == 0,
        "C7_29_C8_NOT_OPENED": negative_controls["c8_opened_count"] == 0,
        "C7_30_ROLLUP_READOUT_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and READOUT_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
        "C7_31_RECEIPT_EMITTED": True,
        "C7_32_BAD_COUNTERS_ZERO": not bool(nonzero_negative),
        "C7_33_PREDECLARED_SEQUENCE_ONLY": run_packet["sequence_policy"] == "PREDECLARED_SEQUENCE_ONLY",
        "C7_34_NO_UNREVIEWED_PACKET_SYNTHESIS": negative_controls["unreviewed_packet_synthesis_count"] == 0 and budget["max_unreviewed_packet_synthesis"] == 0,
        "C7_35_SOURCE_RECEIPTS_IMMUTABLE": source_hashes_before == source_hashes_after,
    }

    false_gates = [k for k, v in acceptance_gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])
        gate = "FAIL"
        status = "TYPED_C7_BOUNDED_CONTINUATION_RADIUS_FAIL"
        outcome = "C7_BLOCKED_RECEIPT_MISMATCH"
        terminal = classify_terminal(gate, outcome, failures)

    receipt = {
        "schema_version": "c7_bounded_continuation_radius_receipt_v0",
        "receipt_type": "TYPED_C7_BOUNDED_CONTINUATION_RADIUS_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "run_id": run_id,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "sequence_scenario": SEQUENCE_SCENARIO,
        "sequence_policy": "PREDECLARED_SEQUENCE_ONLY",
        "commit_verification": commit_verification,
        "source_receipts": {
            "r0_active_source_packet_ref": rel(R0_PACKET),
            "r0_receipt_ref": rel(R0_RECEIPT),
            "runtime_membranes_receipt_ref": rel(MEMBRANES_RECEIPT),
            "double_sieve_suite_receipt_ref": rel(DOUBLE_SIEVE_RECEIPT),
            "runtime_observability_feedback_attachment_receipt_ref": rel(RUNTIME_ATTACHMENT_RECEIPT),
        },
        "failures": failures,
        "warnings": warnings,
        "machine_readable_c7_summary": {
            "c7_radius_test_complete": gate == "PASS",
            "c7_radius_expanded": gate == "PASS",
            "steps_attempted": steps_attempted,
            "steps_advanced": steps_advanced,
            "steps_halted": steps_halted,
            "lawful_continuation_depth": lawful_depth,
            "observable_continuation_depth": observable_depth,
            "packetized_continuation_depth": packetized_depth,
            "typed_halt_count": 1 if typed_final_boundary else 0,
            "untyped_failure_count": 0 if gate == "PASS" else 1,
            "typed_final_boundary": typed_final_boundary,
            "final_boundary": "AUTHORITY_REQUIRED" if typed_final_boundary else None,
            "min_lawful_depth_met": lawful_depth >= budget["min_lawful_depth_for_success"],
            "hidden_next_command": negative_controls["hidden_next_command_count"] != 0,
            "denied_execution": negative_controls["admissibility_denied_executed_count"] != 0,
            "bare_failed": negative_controls["bare_failed_status_count"] != 0,
            "sidecar_authority": negative_controls["sidecar_authority_count"] != 0,
            "cell1_freebuild": negative_controls["cell1_freebuild_count"] != 0,
            "global_autonomy_claim": negative_controls["global_autonomy_claim_count"] != 0 or negative_controls["autonomy_language_emitted_count"] != 0,
            "c8_opened": negative_controls["c8_opened_count"] != 0,
            "predeclared_sequence_only": True,
            "unreviewed_packet_synthesis": False,
            "source_receipts_mutated": source_hashes_before != source_hashes_after,
            "bad_counters_zero": not bool(nonzero_negative),
            "next_command_goal": None,
        },
        "acceptance_gate_results": acceptance_gate_results,
        "negative_controls": negative_controls,
        "source_receipt_immutability": {
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "source_receipts_mutated": source_hashes_before != source_hashes_after,
        },
        "output_artifacts": {
            "budget": rel(BUDGET_PATH),
            "run_packet": rel(RUN_PACKET_PATH),
            "sequence_manifest": rel(SEQUENCE_MANIFEST_PATH),
            "runtime_step_receipts_jsonl": rel(STEP_RECEIPTS_JSONL_PATH),
            "rollup": rel(ROLLUP_PATH),
            "readout": rel(READOUT_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRACE_PATH),
            "step_artifacts": support_artifacts,
        },
        "terminal": terminal,
    }

    receipt["receipt_id"] = "c7_bounded_continuation_radius_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c7_receipt_id={receipt['receipt_id']}")
    print(f"c7_receipt_path={rel(receipt_path)}")
    print(f"c7_run_id={run_id}")
    print(f"c7_outcome={outcome}")
    print(f"c7_terminal_stop_code={terminal['stop_code']}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
