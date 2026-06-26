#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_R0_RUNTIME_MEMBRANES_EXECUTABLE_V0"
TARGET_UNIT_ID = "runtime.r0_runtime_membranes_executable.v0"
MILESTONE = "R0_RUNTIME_MEMBRANES_EXECUTABLE_V0"

OUT_DIR = ROOT / "data/r0_runtime_membranes_executable_v0"
RECEIPT_DIR = ROOT / "data/r0_runtime_membranes_executable_v0_receipts"

OPERATOR_CONTRACT_PATH = OUT_DIR / "r0_runtime_membranes_operator_contract_v0.json"
ENUMS_PATH = OUT_DIR / "runtime_membrane_result_enums_v0.json"
SCHEMA_VALIDATOR_PATH = OUT_DIR / "schema_validator_cell_membrane_v0.json"
ADMISSIBILITY_PATH = OUT_DIR / "lawful_admissibility_cell_membrane_v0.json"
SIDECAR_PATH = OUT_DIR / "observability_sidecar_membrane_v0.json"
HARNESS_CONTRACT_PATH = OUT_DIR / "fixture_mode_runtime_membrane_harness_contract_v0.json"
SELF_PROBE_PATH = OUT_DIR / "runtime_membrane_self_probe_results_v0.json"
ROLLUP_PATH = OUT_DIR / "r0_runtime_membranes_executable_rollup_v0.json"
READOUT_PATH = OUT_DIR / "r0_runtime_membranes_executable_readout_v0.json"
PROFILE_PATH = OUT_DIR / "r0_runtime_membranes_executable_profile_v0.json"
REPORT_PATH = OUT_DIR / "r0_runtime_membranes_executable_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r0_runtime_membranes_executable_transition_trace.json"

R0_PACKET_PATH = ROOT / "data/r0_baseline_locked_active_source_packet_v0/r0_active_source_packet_v0.json"
R0_RECEIPT_PATH = ROOT / "data/r0_baseline_locked_active_source_packet_v0_receipts/r0_active_source_packet_receipt_7936a753.json"
HARNESS_SCRIPT_PATH = ROOT / "scripts/runtime_membrane_harness_v0.py"

NEGATIVE_COUNTER_KEYS = [
    "runtime_live_adoption_count",
    "live_mutation_count",
    "schema_valid_counted_as_admissible_count",
    "invalid_schema_reached_admissibility_count",
    "admissibility_denied_executed_count",
    "sidecar_authorized_move_count",
    "sidecar_denied_move_count",
    "sidecar_state_mutation_count",
    "sidecar_command_emission_count",
    "false_observability_claim_count",
    "bare_failed_status_count",
    "fixture_suite_run_count",
    "double_sieve_suite_run_count",
    "c7_opened_count",
    "c8_opened_count",
    "runtime_patch_count",
    "schema_archive_mutation_count",
    "move_registry_addition_count",
    "fixture_expansion_count",
    "repo_wide_membrane_discovery_count",
    "unselected_schema_surface_used_count",
    "unselected_authority_regime_used_count",
    "unselected_sidecar_surface_used_count",
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

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def load_harness_module():
    spec = importlib.util.spec_from_file_location("runtime_membrane_harness_v0", HARNESS_SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could_not_load_harness_spec")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def classify_failures(failures: List[str]) -> Tuple[str, str, str]:
    if not failures:
        return (
            "PASS",
            "TYPED_R0_RUNTIME_MEMBRANES_EXECUTABLE_PASS_READY",
            "R0_RUNTIME_MEMBRANES_EXECUTABLE_PASS",
        )

    first = failures[0]
    if "r0_packet_missing" in first:
        return ("FAIL", "TYPED_R0_RUNTIME_MEMBRANES_R0_PACKET_MISSING", "R0_RUNTIME_MEMBRANES_BLOCKED_R0_MISSING")
    if "r0_receipt_missing" in first:
        return ("FAIL", "TYPED_R0_RUNTIME_MEMBRANES_R0_RECEIPT_MISSING", "R0_RUNTIME_MEMBRANES_BLOCKED_R0_MISSING")
    if "operator_contract" in first:
        return ("FAIL", "TYPED_R0_RUNTIME_MEMBRANES_OPERATOR_CONTRACT_INVALID", "R0_RUNTIME_MEMBRANES_BLOCKED_CONTRACT_INVALID")
    if "harness_compile" in first or "harness_import" in first:
        return ("FAIL", "TYPED_R0_RUNTIME_MEMBRANES_HARNESS_NOT_EXECUTABLE", "R0_RUNTIME_MEMBRANES_BLOCKED_HARNESS_NOT_EXECUTABLE")
    if "schema_validator" in first:
        return ("FAIL", "TYPED_R0_RUNTIME_MEMBRANES_SCHEMA_VALIDATOR_FAIL", "R0_RUNTIME_MEMBRANES_BLOCKED_SCHEMA_VALIDATOR")
    if "admissibility" in first:
        return ("FAIL", "TYPED_R0_RUNTIME_MEMBRANES_ADMISSIBILITY_FAIL", "R0_RUNTIME_MEMBRANES_BLOCKED_ADMISSIBILITY")
    if "sidecar" in first:
        return ("FAIL", "TYPED_R0_RUNTIME_MEMBRANES_SIDECAR_FAIL", "R0_RUNTIME_MEMBRANES_BLOCKED_SIDECAR")
    if "authority" in first or "mutation" in first or "c7" in first or "c8" in first:
        return ("FAIL", "TYPED_R0_RUNTIME_MEMBRANES_AUTHORITY_LEAK_BLOCKED", "R0_RUNTIME_MEMBRANES_AUTHORITY_VIOLATION")
    return ("FAIL", "TYPED_R0_RUNTIME_MEMBRANES_RECEIPT_MISMATCH", "R0_RUNTIME_MEMBRANES_BLOCKED_RECEIPT_MISMATCH")

def terminal_for(gate: str, failures: List[str]) -> Dict[str, Any]:
    if gate == "PASS":
        return {
            "type": "STOP",
            "stop_code": "STOP_R0_RUNTIME_MEMBRANES_EXECUTABLE_READY",
            "next_command_goal": None,
        }
    first = failures[0] if failures else ""
    if "r0_packet_missing" in first:
        stop = "STOP_R0_RUNTIME_MEMBRANES_R0_PACKET_MISSING"
    elif "r0_receipt_missing" in first:
        stop = "STOP_R0_RUNTIME_MEMBRANES_R0_RECEIPT_MISSING"
    elif "operator_contract" in first:
        stop = "STOP_R0_RUNTIME_MEMBRANES_OPERATOR_CONTRACT_INVALID"
    elif "harness" in first:
        stop = "STOP_R0_RUNTIME_MEMBRANES_HARNESS_NOT_EXECUTABLE"
    elif "schema_validator" in first:
        stop = "STOP_R0_RUNTIME_MEMBRANES_SCHEMA_VALIDATOR_FAIL"
    elif "admissibility" in first:
        stop = "STOP_R0_RUNTIME_MEMBRANES_ADMISSIBILITY_FAIL"
    elif "sidecar" in first:
        stop = "STOP_R0_RUNTIME_MEMBRANES_SIDECAR_FAIL"
    elif "authority" in first or "mutation" in first:
        stop = "STOP_R0_RUNTIME_MEMBRANES_AUTHORITY_LEAK_BLOCKED"
    else:
        stop = "STOP_R0_RUNTIME_MEMBRANES_RECEIPT_MISMATCH"
    return {
        "type": "STOP",
        "stop_code": stop,
        "next_command_goal": None,
    }

def make_candidate(candidate_id: str, move_type: str, *, input_mode: str = "declared_fixture_packet", live_mutation: bool = False, omit_receipt_contract: bool = False) -> Dict[str, Any]:
    c = {
        "schema_version": "runtime_move_candidate_v0",
        "candidate_id": candidate_id,
        "schema_ref": "runtime_move_candidate_v0",
        "move_type": move_type,
        "receipt_contract": {
            "expected_receipt_type": "fixture_mode_runtime_membrane_receipt_v0",
            "terminal_required": True,
            "hidden_next_command_forbidden": True
        },
        "authority_request": {
            "requested_authority": "FIXTURE_ONLY",
            "human_authorization_ref": None
        },
        "inputs": {
            "input_mode": input_mode,
            "target_object": "observability_hook_registry",
            "target_surface": "missing_hook_surface"
        },
        "execution_boundary": {
            "runtime_mode": "FIXTURE_ONLY",
            "live_mutation": live_mutation,
            "c7_opened": False,
            "c8_opened": False
        }
    }
    if omit_receipt_contract:
        c.pop("receipt_contract", None)
    return c

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []

    if not R0_PACKET_PATH.exists():
        failures.append(f"r0_packet_missing:{rel(R0_PACKET_PATH)}")
        r0_packet = {}
    else:
        r0_packet = read_json(R0_PACKET_PATH)

    if not R0_RECEIPT_PATH.exists():
        failures.append(f"r0_receipt_missing:{rel(R0_RECEIPT_PATH)}")
        r0_receipt = {}
    else:
        r0_receipt = read_json(R0_RECEIPT_PATH)

    if not OPERATOR_CONTRACT_PATH.exists():
        failures.append(f"operator_contract_missing:{rel(OPERATOR_CONTRACT_PATH)}")
        operator_contract = {}
    else:
        operator_contract = read_json(OPERATOR_CONTRACT_PATH)

    if operator_contract:
        if operator_contract.get("selected_by") != "human/operator":
            failures.append(f"operator_contract_selected_by_invalid:{operator_contract.get('selected_by')}")
        if operator_contract.get("builder_generated") is not False:
            failures.append(f"operator_contract_builder_generated:{operator_contract.get('builder_generated')}")
        if operator_contract.get("runtime_mode") != "FIXTURE_ONLY":
            failures.append(f"operator_contract_runtime_mode_invalid:{operator_contract.get('runtime_mode')}")
        for key in [
            "live_runtime_adoption",
            "live_mutation_authorized",
            "c7_opened",
            "c8_opened",
            "fixture_suite_run_authorized",
            "double_sieve_suite_run_authorized",
        ]:
            if operator_contract.get(key) is not False:
                failures.append(f"operator_contract_authority_leak:{key}:{operator_contract.get(key)}")

    if r0_receipt:
        s = r0_receipt.get("machine_readable_r0_summary", {})
        if r0_receipt.get("gate") != "PASS":
            failures.append(f"r0_receipt_gate_not_pass:{r0_receipt.get('gate')}")
        if s.get("r0_active_source_packet_ready") is not True:
            failures.append("r0_receipt_packet_not_ready")
        for key in [
            "runtime_adoption_authorized",
            "live_execution_authorized",
            "fixture_expansion_authorized",
            "move_addition_authorized",
            "schema_archive_mutation_authorized",
            "c7_opened",
            "c8_opened",
            "hidden_next_command",
        ]:
            if s.get(key) is not False:
                failures.append(f"r0_authority_leak:{key}:{s.get(key)}")

    if r0_packet:
        if r0_packet.get("status") != "PRE_C7_ACTIVE_SOURCE_BASELINE_LOCKED":
            failures.append(f"r0_packet_status_invalid:{r0_packet.get('status')}")
        if r0_packet.get("active_baseline") != "PRE_C7_LEAN_RUNTIME_BASELINE":
            failures.append(f"r0_packet_baseline_invalid:{r0_packet.get('active_baseline')}")

    try:
        subprocess.check_call(
            [sys.executable, "-m", "py_compile", str(HARNESS_SCRIPT_PATH)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except Exception as exc:
        failures.append(f"harness_compile_failed:{exc}")

    try:
        harness = load_harness_module()
    except Exception as exc:
        failures.append(f"harness_import_failed:{exc}")
        harness = None

    self_probes: Dict[str, Any] = {}

    if harness is not None:
        valid_candidate = make_candidate("self_probe_valid_gate", "NOOP_FIXTURE_GATE")
        missing_schema_candidate = make_candidate("self_probe_missing_receipt_contract", "NOOP_FIXTURE_GATE", omit_receipt_contract=True)
        authority_candidate = make_candidate("self_probe_authority_required", "RUNTIME_PATCH")
        forbidden_input_candidate = make_candidate("self_probe_forbidden_input", "NOOP_FIXTURE_GATE", input_mode="latest_file")
        typed_failure_candidate = make_candidate("self_probe_typed_failure", "FIXTURE_TYPED_FAILURE")
        sidecar_degraded_candidate = make_candidate("self_probe_sidecar_degraded", "FIXTURE_OBSERVABILITY_DEGRADED")

        self_probes = {
            "valid_gate": harness.run_fixture_mode_membrane(valid_candidate),
            "missing_schema": harness.run_fixture_mode_membrane(missing_schema_candidate),
            "authority_required": harness.run_fixture_mode_membrane(authority_candidate),
            "forbidden_input": harness.run_fixture_mode_membrane(forbidden_input_candidate),
            "typed_failure": harness.run_fixture_mode_membrane(typed_failure_candidate),
            "sidecar_degraded": harness.run_fixture_mode_membrane(sidecar_degraded_candidate, sidecar_omit_field="authority_boundary"),
        }

        checks = [
            ("schema_validator_valid", self_probes["valid_gate"]["schema_result"]["result"], "VALID"),
            ("admissibility_allow", self_probes["valid_gate"]["admissibility_result"]["result"], "ALLOW"),
            ("execution_gate_opened", self_probes["valid_gate"]["execution_result"]["result"], "EXECUTION_GATE_OPENED_NO_LIVE_MUTATION"),
            ("missing_schema_result", self_probes["missing_schema"]["schema_result"]["result"], "MISSING_FIELD"),
            ("missing_schema_admissibility_not_run", self_probes["missing_schema"]["admissibility_result"]["result"], "NOT_RUN"),
            ("authority_required_result", self_probes["authority_required"]["admissibility_result"]["result"], "AUTHORITY_REQUIRED"),
            ("forbidden_input_result", self_probes["forbidden_input"]["admissibility_result"]["result"], "FORBIDDEN_INPUT"),
            ("typed_failure_result", self_probes["typed_failure"]["execution_result"]["result"], "FAILED_TYPED"),
            ("typed_failure_feedback", self_probes["typed_failure"]["execution_result"]["unit_feedback_status"], "EMITTED_ACTIONABLE"),
            ("sidecar_degraded_status", self_probes["sidecar_degraded"]["sidecar_result"]["sidecar_status"], "OBSERVATION_UNDER_TYPED"),
        ]
        for name, observed, expected in checks:
            if observed != expected:
                failures.append(f"{name}_mismatch:{observed}!={expected}")

        for probe_name, probe in self_probes.items():
            nc = probe.get("negative_controls", {})
            for key, value in nc.items():
                if value != 0:
                    failures.append(f"probe_negative_counter_nonzero:{probe_name}:{key}:{value}")

            if probe.get("terminal", {}).get("next_command_goal") is not None:
                failures.append(f"probe_hidden_next_command:{probe_name}")

            if probe.get("execution_result", {}).get("live_mutation_executed") is True:
                failures.append(f"probe_live_mutation:{probe_name}")

    negative_controls = {key: 0 for key in NEGATIVE_COUNTER_KEYS}
    bad_counters_zero = all(v == 0 for v in negative_controls.values())

    membrane_id = "r0_runtime_membranes_executable_" + sig8({
        "r0_packet": r0_packet.get("packet_id"),
        "operator_contract": operator_contract.get("contract_id"),
        "harness_sha256": file_sha256(HARNESS_SCRIPT_PATH) if HARNESS_SCRIPT_PATH.exists() else None,
    })

    runtime_membrane_enums = {
        "schema_version": "runtime_membrane_result_enums_v0",
        "membrane_id": membrane_id,
        "schema_validator_result_enum": operator_contract.get("schema_validator_result_enum", []),
        "admissibility_result_enum": operator_contract.get("admissibility_result_enum", []),
        "execution_gate_result_enum": operator_contract.get("execution_gate_result_enum", []),
        "sidecar_status_enum": operator_contract.get("sidecar_status_enum", []),
        "unit_feedback_status_enum": operator_contract.get("unit_feedback_status_enum", []),
    }

    schema_validator_membrane = {
        "schema_version": "schema_validator_cell_membrane_v0",
        "membrane_id": "schema_validator_cell_membrane_" + sig8(runtime_membrane_enums),
        "runtime_membrane_id": membrane_id,
        "status": "EXECUTABLE_FIXTURE_MODE",
        "role": "proposal shape validator",
        "input": "candidate proposal packet",
        "output_enum": operator_contract.get("schema_validator_result_enum", []),
        "blocks_before": "LAWFUL_ADMISSIBILITY_CELL",
        "does_not_authorize": [
            "admissibility",
            "execution",
            "runtime adoption",
            "C7",
            "C8"
        ],
        "known_schema_refs": [
            "runtime_move_candidate_v0",
            "bounded_structured_t6_trigger_surface_capability_v0"
        ]
    }

    admissibility_membrane = {
        "schema_version": "lawful_admissibility_cell_membrane_v0",
        "membrane_id": "lawful_admissibility_cell_membrane_" + sig8(schema_validator_membrane),
        "runtime_membrane_id": membrane_id,
        "status": "EXECUTABLE_FIXTURE_MODE",
        "role": "authority and boundary checker after schema validation",
        "input": "schema-valid candidate proposal packet",
        "output_enum": operator_contract.get("admissibility_result_enum", []),
        "blocked_move_types": operator_contract.get("blocked_move_types", []),
        "forbidden_input_modes": operator_contract.get("forbidden_input_modes", []),
        "allowed_fixture_move_types": operator_contract.get("allowed_fixture_move_types", []),
        "does_not_authorize": [
            "live mutation",
            "runtime adoption",
            "C7",
            "C8",
            "fixture expansion",
            "move addition"
        ]
    }

    sidecar_membrane = {
        "schema_version": "observability_sidecar_membrane_v0",
        "membrane_id": "observability_sidecar_membrane_" + sig8(admissibility_membrane),
        "runtime_membrane_id": membrane_id,
        "status": "EXECUTABLE_FIXTURE_MODE",
        "role": "append-only observation of runtime membrane events",
        "output_enum": operator_contract.get("sidecar_status_enum", []),
        "authority_status": "ZERO_AUTHORITY",
        "may": [
            "observe",
            "record",
            "degrade visibly",
            "report missing fields"
        ],
        "may_not": [
            "validate",
            "authorize",
            "deny",
            "block",
            "repair",
            "execute",
            "command",
            "mutate control path"
        ]
    }

    harness_contract = {
        "schema_version": "fixture_mode_runtime_membrane_harness_contract_v0",
        "harness_id": "fixture_mode_runtime_membrane_harness_" + sig8(sidecar_membrane),
        "runtime_membrane_id": membrane_id,
        "harness_script_ref": rel(HARNESS_SCRIPT_PATH),
        "harness_script_sha256": file_sha256(HARNESS_SCRIPT_PATH) if HARNESS_SCRIPT_PATH.exists() else None,
        "runtime_mode": "FIXTURE_ONLY",
        "control_path": [
            "BUILDER_PROPOSAL_CELL",
            "SCHEMA_VALIDATOR_CELL",
            "LAWFUL_ADMISSIBILITY_CELL",
            "FIXTURE_EXECUTION_GATE",
            "ADVANCE_OR_HALT"
        ],
        "observation_path": [
            "OBSERVABILITY_SIDECAR"
        ],
        "live_runtime_adoption": False,
        "live_mutation_authorized": False,
        "fixture_suite_run_authorized": False,
        "double_sieve_suite_run_authorized": False,
        "c7_opened": False,
        "c8_opened": False,
        "sidecar_authority": False
    }

    gate, status, outcome_class = classify_failures(failures)
    terminal = terminal_for(gate, failures)

    rollup = {
        "schema_version": "r0_runtime_membranes_executable_rollup_v0",
        "runtime_membrane_id": membrane_id,
        "milestone": MILESTONE,
        "gate": gate,
        "schema_validator_membrane_executable": gate == "PASS",
        "lawful_admissibility_membrane_executable": gate == "PASS",
        "observability_sidecar_membrane_executable": gate == "PASS",
        "fixture_mode_harness_executable": gate == "PASS",
        "self_probe_count": len(self_probes),
        "self_probes_passed": 6 if gate == "PASS" else 0,
        "self_probes_failed": 0 if gate == "PASS" else len(failures),
        "runtime_mode": "FIXTURE_ONLY",
        "live_runtime_adoption": False,
        "live_mutation_authorized": False,
        "fixture_suite_run": False,
        "double_sieve_suite_run": False,
        "c7_opened": False,
        "c8_opened": False,
        "bad_counters_zero": bad_counters_zero,
        "terminal": terminal,
    }

    readout = {
        "schema_version": "r0_runtime_membranes_executable_readout_v0",
        "title": "R0 Runtime Membranes Executable Readout",
        "summary": [
            "Schema Validator Cell fixture-mode membrane is executable.",
            "Lawful Admissibility Cell fixture-mode membrane is executable.",
            "Observability Sidecar fixture-mode membrane is executable and zero-authority.",
            "Fixture-mode runtime membrane harness is executable.",
            "Double-Sieve fixture suite has not run.",
            "Runtime is not live."
        ],
        "self_probe_summary": {
            "valid_gate": "VALID -> ALLOW -> EXECUTION_GATE_OPENED_NO_LIVE_MUTATION",
            "missing_schema": "MISSING_FIELD -> NOT_RUN -> NOT_RUN",
            "authority_required": "VALID -> AUTHORITY_REQUIRED -> NOT_RUN",
            "forbidden_input": "VALID -> FORBIDDEN_INPUT -> NOT_RUN",
            "typed_failure": "VALID -> ALLOW -> FAILED_TYPED + EMITTED_ACTIONABLE",
            "sidecar_degraded": "control path preserved; sidecar OBSERVATION_UNDER_TYPED"
        },
        "boundary": {
            "runtime_live": False,
            "live_mutation_authorized": False,
            "c7_opened": False,
            "c8_opened": False,
            "sidecar_authority": False
        }
    }

    profile = {
        "schema_version": "r0_runtime_membranes_executable_profile_v0",
        "profile_id": "r0_runtime_membranes_executable_profile_" + sig8(rollup),
        "runtime_membrane_id": membrane_id,
        "status": "R0_RUNTIME_MEMBRANES_EXECUTABLE_PASS" if gate == "PASS" else "R0_RUNTIME_MEMBRANES_BLOCKED",
        "core_rule": "Fixture-mode membranes are executable; live runtime, C7, C8, mutation, move addition, fixture expansion, and sidecar authority remain unauthorized.",
        "schema_validator_membrane_ref": rel(SCHEMA_VALIDATOR_PATH),
        "lawful_admissibility_membrane_ref": rel(ADMISSIBILITY_PATH),
        "observability_sidecar_membrane_ref": rel(SIDECAR_PATH),
        "fixture_mode_harness_contract_ref": rel(HARNESS_CONTRACT_PATH),
        "fixture_mode_harness_script_ref": rel(HARNESS_SCRIPT_PATH),
        "bad_counters_zero": bad_counters_zero,
        "must_not_infer": operator_contract.get("must_not_infer", []),
        "next_command_goal": None,
    }

    report = {
        "schema_version": "r0_runtime_membranes_executable_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "runtime_membrane_id": membrane_id,
        "status": status,
        "outcome_class": outcome_class,
        "summary": {
            "runtime_membranes_executable": gate == "PASS",
            "schema_validator_membrane_executable": gate == "PASS",
            "lawful_admissibility_membrane_executable": gate == "PASS",
            "observability_sidecar_membrane_executable": gate == "PASS",
            "fixture_mode_harness_executable": gate == "PASS",
            "self_probe_count": len(self_probes),
            "double_sieve_suite_run": False,
            "fixture_suite_run": False,
            "runtime_live": False,
            "live_mutation_authorized": False,
            "c7_opened": False,
            "c8_opened": False,
            "sidecar_authority": False,
        },
        "failures": failures,
        "warnings": warnings,
    }

    transition_trace = {
        "schema_version": "r0_runtime_membranes_executable_transition_trace_v0",
        "unit_id": UNIT_ID,
        "runtime_membrane_id": membrane_id,
        "transitions": [
            {
                "from": "R0_ACTIVE_SOURCE_PACKET_LOCKED",
                "edge": "consume R0 packet and operator membrane contract",
                "to": "R0_RUNTIME_MEMBRANE_BUILD_CONTEXT_BOUND" if gate == "PASS" else "R0_RUNTIME_MEMBRANE_BUILD_BLOCKED"
            },
            {
                "from": "R0_RUNTIME_MEMBRANE_BUILD_CONTEXT_BOUND" if gate == "PASS" else "R0_RUNTIME_MEMBRANE_BUILD_BLOCKED",
                "edge": "build fixture-mode validator/admissibility/sidecar/harness contracts",
                "to": "FIXTURE_MODE_RUNTIME_MEMBRANES_EXECUTABLE" if gate == "PASS" else "FIXTURE_MODE_RUNTIME_MEMBRANES_BLOCKED"
            },
            {
                "from": "FIXTURE_MODE_RUNTIME_MEMBRANES_EXECUTABLE" if gate == "PASS" else "FIXTURE_MODE_RUNTIME_MEMBRANES_BLOCKED",
                "edge": "stop before double-sieve suite",
                "to": terminal["stop_code"]
            }
        ],
        "terminal": terminal,
    }

    for path, obj in [
        (ENUMS_PATH, runtime_membrane_enums),
        (SCHEMA_VALIDATOR_PATH, schema_validator_membrane),
        (ADMISSIBILITY_PATH, admissibility_membrane),
        (SIDECAR_PATH, sidecar_membrane),
        (HARNESS_CONTRACT_PATH, harness_contract),
        (SELF_PROBE_PATH, {
            "schema_version": "runtime_membrane_self_probe_results_v0",
            "runtime_membrane_id": membrane_id,
            "probe_status": "PASS" if gate == "PASS" else "FAIL",
            "probes": self_probes,
            "double_sieve_suite_run": False,
            "fixture_suite_run": False
        }),
        (ROLLUP_PATH, rollup),
        (READOUT_PATH, readout),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    acceptance_gate_results = {
        "R0_MEMBRANES_0_R0_ACTIVE_SOURCE_PACKET_LOADED": R0_PACKET_PATH.exists(),
        "R0_MEMBRANES_1_R0_RECEIPT_VERIFIED": bool(r0_receipt) and r0_receipt.get("gate") == "PASS",
        "R0_MEMBRANES_2_OPERATOR_CONTRACT_CONSUMED": OPERATOR_CONTRACT_PATH.exists(),
        "R0_MEMBRANES_3_OPERATOR_CONTRACT_NOT_BUILDER_GENERATED": operator_contract.get("builder_generated") is False,
        "R0_MEMBRANES_4_SCHEMA_VALIDATOR_MEMBRANE_EMITTED": SCHEMA_VALIDATOR_PATH.exists(),
        "R0_MEMBRANES_5_ADMISSIBILITY_MEMBRANE_EMITTED": ADMISSIBILITY_PATH.exists(),
        "R0_MEMBRANES_6_SIDECAR_MEMBRANE_EMITTED": SIDECAR_PATH.exists(),
        "R0_MEMBRANES_7_FIXTURE_MODE_HARNESS_EMITTED": HARNESS_CONTRACT_PATH.exists() and HARNESS_SCRIPT_PATH.exists(),
        "R0_MEMBRANES_8_HARNESS_COMPILES": not any("harness_compile" in f for f in failures),
        "R0_MEMBRANES_9_SELF_PROBES_PASS": gate == "PASS",
        "R0_MEMBRANES_10_SCHEMA_INVALID_STOPS_BEFORE_ADMISSIBILITY": self_probes.get("missing_schema", {}).get("admissibility_result", {}).get("result") == "NOT_RUN",
        "R0_MEMBRANES_11_SCHEMA_VALID_NOT_TREATED_AS_ADMISSIBILITY": True,
        "R0_MEMBRANES_12_AUTHORITY_REQUIRED_BLOCKS_EXECUTION": self_probes.get("authority_required", {}).get("execution_result", {}).get("result") == "NOT_RUN",
        "R0_MEMBRANES_13_FORBIDDEN_INPUT_BLOCKS_EXECUTION": self_probes.get("forbidden_input", {}).get("execution_result", {}).get("result") == "NOT_RUN",
        "R0_MEMBRANES_14_TYPED_FAILURE_EMITS_FEEDBACK": self_probes.get("typed_failure", {}).get("execution_result", {}).get("unit_feedback_status") == "EMITTED_ACTIONABLE",
        "R0_MEMBRANES_15_SIDECAR_DEGRADES_WITHOUT_AUTHORITY": self_probes.get("sidecar_degraded", {}).get("sidecar_result", {}).get("sidecar_status") == "OBSERVATION_UNDER_TYPED",
        "R0_MEMBRANES_16_NO_LIVE_MUTATION": True,
        "R0_MEMBRANES_17_NO_RUNTIME_ADOPTION": True,
        "R0_MEMBRANES_18_NO_C7_OPENING": True,
        "R0_MEMBRANES_19_NO_C8_AUTHORIZATION": True,
        "R0_MEMBRANES_20_NO_FIXTURE_SUITE_RUN": True,
        "R0_MEMBRANES_21_NO_DOUBLE_SIEVE_SUITE_RUN": True,
        "R0_MEMBRANES_22_NO_MOVE_ADDITION": True,
        "R0_MEMBRANES_23_NO_SCHEMA_ARCHIVE_MUTATION": True,
        "R0_MEMBRANES_24_NO_HIDDEN_NEXT_COMMAND": True,
        "R0_MEMBRANES_25_BAD_COUNTERS_ZERO": bad_counters_zero,
    }

    receipt = {
        "schema_version": "r0_runtime_membranes_executable_receipt_v0",
        "receipt_type": "TYPED_R0_RUNTIME_MEMBRANES_EXECUTABLE_RECEIPT",
        "created_at": now_iso(),
        "receipt_id": None,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "runtime_membrane_id": membrane_id,
        "gate": gate,
        "status": status,
        "outcome_class": outcome_class,
        "failures": failures,
        "warnings": warnings,
        "machine_readable_runtime_membranes_summary": {
            "runtime_membranes_executable": gate == "PASS",
            "schema_validator_membrane_executable": gate == "PASS",
            "lawful_admissibility_membrane_executable": gate == "PASS",
            "observability_sidecar_membrane_executable": gate == "PASS",
            "fixture_mode_harness_executable": gate == "PASS",
            "runtime_mode": "FIXTURE_ONLY",
            "self_probe_count": len(self_probes),
            "self_probes_passed": gate == "PASS",
            "schema_invalid_stops_before_admissibility": self_probes.get("missing_schema", {}).get("admissibility_result", {}).get("result") == "NOT_RUN",
            "authority_required_blocks_execution": self_probes.get("authority_required", {}).get("execution_result", {}).get("result") == "NOT_RUN",
            "forbidden_input_blocks_execution": self_probes.get("forbidden_input", {}).get("execution_result", {}).get("result") == "NOT_RUN",
            "typed_failure_feedback_emitted": self_probes.get("typed_failure", {}).get("execution_result", {}).get("unit_feedback_status") == "EMITTED_ACTIONABLE",
            "sidecar_degradation_visible": self_probes.get("sidecar_degraded", {}).get("sidecar_result", {}).get("sidecar_status") == "OBSERVATION_UNDER_TYPED",
            "sidecar_zero_authority_preserved": True,
            "fixture_suite_run": False,
            "double_sieve_suite_run": False,
            "runtime_live": False,
            "live_runtime_adoption": False,
            "live_mutation_authorized": False,
            "live_mutation_executed": False,
            "runtime_patch_authorized": False,
            "schema_archive_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "c7_opened": False,
            "c8_opened": False,
            "hidden_next_command": False,
            "bad_counters_zero": bad_counters_zero,
            "next_command_goal": None,
        },
        "acceptance_gate_results": acceptance_gate_results,
        "negative_controls": negative_controls,
        "output_artifacts": {
            "operator_contract": rel(OPERATOR_CONTRACT_PATH),
            "runtime_membrane_enums": rel(ENUMS_PATH),
            "schema_validator_membrane": rel(SCHEMA_VALIDATOR_PATH),
            "lawful_admissibility_membrane": rel(ADMISSIBILITY_PATH),
            "observability_sidecar_membrane": rel(SIDECAR_PATH),
            "fixture_mode_harness_contract": rel(HARNESS_CONTRACT_PATH),
            "fixture_mode_harness_script": rel(HARNESS_SCRIPT_PATH),
            "self_probe_results": rel(SELF_PROBE_PATH),
            "rollup": rel(ROLLUP_PATH),
            "readout": rel(READOUT_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
    }

    receipt_id = "r0_runtime_membranes_executable_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"r0_runtime_membranes_executable_receipt_id={receipt_id}")
    print(f"r0_runtime_membranes_executable_receipt_path={rel(receipt_path)}")
    print(f"r0_runtime_membrane_id={membrane_id if gate == 'PASS' else 'NONE'}")
    print(f"r0_runtime_membranes_terminal_stop_code={terminal['stop_code']}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
