#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_DOUBLE_SIEVE_FIXTURE_SUITE_V0"
TARGET_UNIT_ID = "runtime.double_sieve_fixture_suite.v0"
MILESTONE = "DOUBLE_SIEVE_FIXTURE_SUITE_PASS"

OUT_DIR = ROOT / "data/double_sieve_fixture_suite_v0"
RECEIPT_DIR = ROOT / "data/double_sieve_fixture_suite_v0_receipts"
FIXTURE_DIR = OUT_DIR / "fixtures"

CONTRACT_PATH = OUT_DIR / "double_sieve_fixture_suite_contract_v0.json"
MANIFEST_PATH = OUT_DIR / "double_sieve_fixture_manifest_v0.jsonl"
ROLLUP_PATH = OUT_DIR / "double_sieve_fixture_suite_rollup_v0.json"
READOUT_PATH = OUT_DIR / "double_sieve_fixture_suite_readout_v0.json"
PROFILE_PATH = OUT_DIR / "double_sieve_fixture_suite_profile_v0.json"
REPORT_PATH = OUT_DIR / "double_sieve_fixture_suite_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "double_sieve_fixture_suite_transition_trace.json"

R0_PACKET_PATH = ROOT / "data/r0_baseline_locked_active_source_packet_v0/r0_active_source_packet_v0.json"
R0_RECEIPT_PATH = ROOT / "data/r0_baseline_locked_active_source_packet_v0_receipts/r0_active_source_packet_receipt_7936a753.json"
MEMBRANE_RECEIPT_PATH = ROOT / "data/r0_runtime_membranes_executable_v0_receipts/r0_runtime_membranes_executable_receipt_012fe341.json"
HARNESS_SCRIPT_PATH = ROOT / "scripts/runtime_membrane_harness_v0.py"

REQUIRED_FIXTURES = [
    "F1_VALID_ADMISSIBLE",
    "F2_INVALID_SCHEMA",
    "F3_AUTHORITY_REQUIRED",
    "F4_FORBIDDEN_INPUT",
    "F5_EXECUTION_FAILURE_TYPED_FEEDBACK",
    "F6_SIDECAR_PARTIAL_OBSERVABILITY",
]

BAD_COUNTER_KEYS = [
    "invalid_schema_reached_admissibility_count",
    "raw_proposal_reached_admissibility_count",
    "schema_valid_counted_as_admissible_count",
    "admissibility_denied_executed_count",
    "authority_required_ignored_count",
    "forbidden_input_executed_count",
    "latest_file_selection_executed_count",
    "mtime_selection_executed_count",
    "sidecar_authorized_move_count",
    "sidecar_denied_move_count",
    "sidecar_state_mutation_count",
    "sidecar_command_emission_count",
    "sidecar_control_action_count",
    "sidecar_authority_claim_count",
    "false_observability_claim_count",
    "bare_failed_status_count",
    "unit_feedback_missing_count",
    "repair_applied_by_feedback_count",
    "live_mutation_count",
    "runtime_patch_count",
    "schema_archive_mutation_count",
    "move_registry_addition_count",
    "fixture_expansion_count",
    "c7_opened_count",
    "c8_opened_count",
    "hidden_next_command_count",
    "repo_wide_membrane_discovery_count",
    "unselected_schema_surface_used_count",
    "unselected_authority_regime_used_count",
    "unselected_sidecar_surface_used_count",
    "membrane_receipt_missing_count",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def load_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def load_harness_module():
    spec = importlib.util.spec_from_file_location("runtime_membrane_harness_v0", HARNESS_SCRIPT_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("could_not_load_runtime_membrane_harness_v0")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def stop_for_failure(failures: List[str]) -> Tuple[str, str, str]:
    if not failures:
        return ("PASS", "TYPED_DOUBLE_SIEVE_FIXTURE_SUITE_PASS", "DOUBLE_SIEVE_PASS")

    first = failures[0]
    if "r0_missing" in first:
        return ("FAIL", "TYPED_DOUBLE_SIEVE_R0_ACTIVE_SOURCE_PACKET_MISSING", "DOUBLE_SIEVE_BLOCKED_R0_MISSING")
    if "membrane_receipt_missing" in first or "harness_missing" in first:
        return ("FAIL", "TYPED_DOUBLE_SIEVE_RUNTIME_MEMBRANE_RUNNER_MISSING", "DOUBLE_SIEVE_BLOCKED_MEMBRANE_RUNNER_MISSING")
    if "fixture_set_underdeclared" in first or "manifest" in first:
        return ("FAIL", "TYPED_DOUBLE_SIEVE_FIXTURE_SET_UNDERDECLARED", "DOUBLE_SIEVE_BLOCKED_FIXTURE_SET_UNDERDECLARED")
    if "invalid_schema_reached_admissibility" in first:
        return ("FAIL", "TYPED_DOUBLE_SIEVE_INVALID_SCHEMA_REACHED_ADMISSIBILITY", "DOUBLE_SIEVE_AUTHORITY_VIOLATION_INVALID_SCHEMA_REACHED_ADMISSIBILITY")
    if "admissibility_denied_executed" in first:
        return ("FAIL", "TYPED_DOUBLE_SIEVE_ADMISSIBILITY_DENIED_EXECUTED", "DOUBLE_SIEVE_AUTHORITY_VIOLATION_ADMISSIBILITY_DENIED_EXECUTED")
    if "sidecar_authority" in first:
        return ("FAIL", "TYPED_DOUBLE_SIEVE_SIDECAR_AUTHORITY_LEAK", "DOUBLE_SIEVE_AUTHORITY_VIOLATION_SIDECAR_AUTHORITY_LEAK")
    if "bare_failed" in first:
        return ("FAIL", "TYPED_DOUBLE_SIEVE_BARE_FAILURE_STATUS", "DOUBLE_SIEVE_FAIL_FIXTURE_MISMATCH")
    if "false_observability" in first:
        return ("FAIL", "TYPED_DOUBLE_SIEVE_FALSE_OBSERVABILITY_CLAIM", "DOUBLE_SIEVE_FAIL_FIXTURE_MISMATCH")
    if "live_mutation" in first:
        return ("FAIL", "TYPED_DOUBLE_SIEVE_LIVE_MUTATION_DETECTED", "DOUBLE_SIEVE_RUNTIME_BOUNDARY_VIOLATION_LIVE_MUTATION")
    if "c7_opened" in first:
        return ("FAIL", "TYPED_DOUBLE_SIEVE_C7_OPENED", "DOUBLE_SIEVE_RUNTIME_BOUNDARY_VIOLATION_C7_OPENED")
    if "c8_opened" in first:
        return ("FAIL", "TYPED_DOUBLE_SIEVE_C8_OPENED", "DOUBLE_SIEVE_RUNTIME_BOUNDARY_VIOLATION_C8_OPENED")
    return ("FAIL", "TYPED_DOUBLE_SIEVE_FIXTURE_SUITE_FAIL", "DOUBLE_SIEVE_FAIL_FIXTURE_MISMATCH")

def terminal_for(gate: str, failures: List[str]) -> Dict[str, Any]:
    if gate == "PASS":
        return {
            "type": "STOP",
            "stop_code": "STOP_DOUBLE_SIEVE_FIXTURE_SUITE_PASS",
            "next_command_goal": None,
        }

    first = failures[0] if failures else ""
    if "r0_missing" in first:
        stop = "STOP_DOUBLE_SIEVE_R0_ACTIVE_SOURCE_PACKET_MISSING"
    elif "membrane_receipt_missing" in first:
        stop = "STOP_DOUBLE_SIEVE_RUNTIME_MEMBRANES_EXECUTABLE_RECEIPT_MISSING"
    elif "harness_missing" in first:
        stop = "STOP_DOUBLE_SIEVE_RUNTIME_MEMBRANE_RUNNER_MISSING"
    elif "fixture_set_underdeclared" in first:
        stop = "STOP_DOUBLE_SIEVE_FIXTURE_SET_UNDERDECLARED"
    elif "manifest" in first:
        stop = "STOP_DOUBLE_SIEVE_FIXTURE_MANIFEST_INVALID"
    elif "invalid_schema_reached_admissibility" in first:
        stop = "STOP_DOUBLE_SIEVE_INVALID_SCHEMA_REACHED_ADMISSIBILITY"
    elif "schema_valid_counted_as_admissible" in first:
        stop = "STOP_DOUBLE_SIEVE_SCHEMA_VALID_COUNTED_AS_ADMISSIBLE"
    elif "admissibility_denied_executed" in first:
        stop = "STOP_DOUBLE_SIEVE_ADMISSIBILITY_DENIED_EXECUTED"
    elif "forbidden_input_executed" in first:
        stop = "STOP_DOUBLE_SIEVE_FORBIDDEN_INPUT_EXECUTED"
    elif "sidecar_authority" in first:
        stop = "STOP_DOUBLE_SIEVE_SIDECAR_AUTHORITY_LEAK"
    elif "bare_failed" in first:
        stop = "STOP_DOUBLE_SIEVE_BARE_FAILURE_STATUS"
    elif "false_observability" in first:
        stop = "STOP_DOUBLE_SIEVE_FALSE_OBSERVABILITY_CLAIM"
    elif "live_mutation" in first:
        stop = "STOP_DOUBLE_SIEVE_LIVE_MUTATION_DETECTED"
    elif "c7_opened" in first:
        stop = "STOP_DOUBLE_SIEVE_C7_OPENED"
    elif "c8_opened" in first:
        stop = "STOP_DOUBLE_SIEVE_C8_OPENED"
    else:
        stop = "STOP_DOUBLE_SIEVE_FIXTURE_SUITE_FAIL"

    return {
        "type": "STOP",
        "stop_code": stop,
        "next_command_goal": None,
    }

def zero_counters() -> Dict[str, int]:
    return {k: 0 for k in BAD_COUNTER_KEYS}

def enrich_negative_controls(fixture_id: str, packet: Dict[str, Any], observed: Dict[str, Any]) -> Dict[str, int]:
    nc = zero_counters()
    harness_nc = observed.get("negative_controls", {})
    for k, v in harness_nc.items():
        if k in nc:
            nc[k] += int(v)

    schema_result = observed["schema_result"]["result"]
    admissibility_result = observed["admissibility_result"]["result"]
    execution_result = observed["execution_result"]["result"]
    sidecar_result = observed["sidecar_result"]
    terminal = observed["terminal"]

    if schema_result != "VALID" and admissibility_result != "NOT_RUN":
        nc["invalid_schema_reached_admissibility_count"] += 1

    if schema_result == "VALID" and admissibility_result == "ALLOW" and execution_result == "NOT_RUN":
        nc["schema_valid_counted_as_admissible_count"] += 1

    if admissibility_result in {"AUTHORITY_REQUIRED", "FORBIDDEN_INPUT", "UNREGISTERED_MOVE", "UNIT_BOUNDARY_EXCEEDED"} and execution_result != "NOT_RUN":
        nc["admissibility_denied_executed_count"] += 1

    if fixture_id == "F3_AUTHORITY_REQUIRED" and execution_result != "NOT_RUN":
        nc["authority_required_ignored_count"] += 1
        nc["runtime_patch_count"] += 1

    if fixture_id == "F4_FORBIDDEN_INPUT" and execution_result != "NOT_RUN":
        nc["forbidden_input_executed_count"] += 1
        nc["latest_file_selection_executed_count"] += 1

    effects = sidecar_result.get("effects", {})
    if effects.get("control_path_modified") is True:
        nc["sidecar_control_action_count"] += 1
    if effects.get("authority_decision_modified") is True:
        nc["sidecar_authority_claim_count"] += 1
    if sidecar_result.get("sidecar_authority_status") != "ZERO_AUTHORITY":
        nc["sidecar_authority_claim_count"] += 1
    if sidecar_result.get("sidecar_status") == "OBSERVATION_UNDER_TYPED" and effects.get("full_observability_claim_allowed") is True:
        nc["false_observability_claim_count"] += 1

    if execution_result == "FAILED":
        nc["bare_failed_status_count"] += 1

    expected_feedback = packet["expected"]["unit_feedback_status"]
    actual_feedback = observed["execution_result"].get("unit_feedback_status")
    if expected_feedback == "EMITTED_ACTIONABLE" and actual_feedback != "EMITTED_ACTIONABLE":
        nc["unit_feedback_missing_count"] += 1

    feedback = observed["execution_result"].get("unit_feedback")
    if isinstance(feedback, dict):
        safety = feedback.get("safety", {})
        if safety.get("repair_applied") is True:
            nc["repair_applied_by_feedback_count"] += 1

    if observed["execution_result"].get("live_mutation_executed") is True:
        nc["live_mutation_count"] += 1

    if terminal.get("next_command_goal") is not None:
        nc["hidden_next_command_count"] += 1

    return nc

def fixture_receipt_path(fixture_id: str) -> Path:
    return FIXTURE_DIR / fixture_id / "double_sieve_fixture_receipt_v0.json"

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []

    if not R0_PACKET_PATH.exists():
        failures.append(f"r0_missing:packet:{rel(R0_PACKET_PATH)}")
        r0_packet = {}
    else:
        r0_packet = read_json(R0_PACKET_PATH)

    if not R0_RECEIPT_PATH.exists():
        failures.append(f"r0_missing:receipt:{rel(R0_RECEIPT_PATH)}")
        r0_receipt = {}
    else:
        r0_receipt = read_json(R0_RECEIPT_PATH)

    if not MEMBRANE_RECEIPT_PATH.exists():
        failures.append(f"membrane_receipt_missing:{rel(MEMBRANE_RECEIPT_PATH)}")
        membrane_receipt = {}
    else:
        membrane_receipt = read_json(MEMBRANE_RECEIPT_PATH)

    if not HARNESS_SCRIPT_PATH.exists():
        failures.append(f"harness_missing:{rel(HARNESS_SCRIPT_PATH)}")

    if not CONTRACT_PATH.exists():
        failures.append(f"manifest_contract_missing:{rel(CONTRACT_PATH)}")
        contract = {}
    else:
        contract = read_json(CONTRACT_PATH)

    if not MANIFEST_PATH.exists():
        failures.append(f"manifest_missing:{rel(MANIFEST_PATH)}")
        manifest = []
    else:
        manifest = load_jsonl(MANIFEST_PATH)

    if contract:
        if contract.get("builder_generated") is not False:
            failures.append("manifest_contract_builder_generated")
        if contract.get("selected_by") != "human/operator":
            failures.append("manifest_contract_not_operator_selected")
        for key in [
            "live_mutation_authorized",
            "live_mutation_executed",
            "c7_opened",
            "c8_opened",
            "live_runtime_adoption",
            "fixture_expansion_authorized",
            "move_addition_authorized",
            "schema_archive_mutation_authorized",
            "sidecar_authority",
        ]:
            if contract.get(key) is not False:
                failures.append(f"contract_authority_leak:{key}:{contract.get(key)}")

    if r0_receipt:
        s = r0_receipt.get("machine_readable_r0_summary", {})
        if r0_receipt.get("gate") != "PASS":
            failures.append(f"r0_receipt_gate_not_pass:{r0_receipt.get('gate')}")
        if s.get("r0_active_source_packet_ready") is not True:
            failures.append("r0_packet_not_ready")
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

    if membrane_receipt:
        ms = membrane_receipt.get("machine_readable_runtime_membranes_summary", {})
        if membrane_receipt.get("gate") != "PASS":
            failures.append(f"membrane_receipt_gate_not_pass:{membrane_receipt.get('gate')}")
        for key in [
            "runtime_membranes_executable",
            "schema_validator_membrane_executable",
            "lawful_admissibility_membrane_executable",
            "observability_sidecar_membrane_executable",
            "fixture_mode_harness_executable",
            "self_probes_passed",
            "bad_counters_zero",
        ]:
            if ms.get(key) is not True:
                failures.append(f"membrane_receipt_{key}_not_true:{ms.get(key)}")
        for key in [
            "fixture_suite_run",
            "double_sieve_suite_run",
            "runtime_live",
            "live_runtime_adoption",
            "live_mutation_authorized",
            "live_mutation_executed",
            "schema_archive_mutation_authorized",
            "move_addition_authorized",
            "fixture_expansion_authorized",
            "c7_opened",
            "c8_opened",
            "hidden_next_command",
        ]:
            if ms.get(key) is not False:
                failures.append(f"membrane_receipt_{key}_not_false:{ms.get(key)}")

    manifest_ids = [row.get("fixture_id") for row in manifest]
    if manifest_ids != REQUIRED_FIXTURES:
        failures.append(f"fixture_set_underdeclared_or_wrong_order:{manifest_ids}")

    harness = None
    if HARNESS_SCRIPT_PATH.exists():
        try:
            spec = importlib.util.spec_from_file_location("runtime_membrane_harness_v0", HARNESS_SCRIPT_PATH)
            if spec is None or spec.loader is None:
                raise RuntimeError("spec_loader_missing")
            harness = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(harness)
        except Exception as exc:
            failures.append(f"harness_import_failed:{exc}")

    suite_id = "double_sieve_fixture_suite_" + sig8({
        "contract": contract.get("suite_id"),
        "membrane_receipt": str(MEMBRANE_RECEIPT_PATH),
        "fixtures": manifest_ids,
    })
    run_id = "double_sieve_suite_run_" + sig8({
        "suite_id": suite_id,
        "fixture_ids": manifest_ids,
    })

    fixture_receipts: List[Dict[str, Any]] = []
    all_fixture_failures: List[str] = []
    aggregate_bad_counters = zero_counters()

    if harness is not None and not any(f.startswith("fixture_set_underdeclared") for f in failures):
        for row in manifest:
            fixture_id = row["fixture_id"]
            packet_path = ROOT / row["input_candidate_ref"]
            if not packet_path.exists():
                all_fixture_failures.append(f"{fixture_id}:fixture_packet_missing:{row['input_candidate_ref']}")
                continue

            packet = read_json(packet_path)
            observed = harness.run_fixture_mode_membrane(
                packet["candidate"],
                sidecar_omit_field=packet.get("sidecar_omit_field"),
            )

            expected = packet["expected"]
            observed_summary = {
                "schema_result": observed["schema_result"]["result"],
                "admissibility_result": observed["admissibility_result"]["result"],
                "execution_result": observed["execution_result"]["result"],
                "sidecar_status": observed["sidecar_result"]["sidecar_status"],
                "unit_feedback_status": observed["execution_result"].get("unit_feedback_status"),
                "terminal_stop_code": observed["terminal"]["stop_code"],
            }

            fixture_failures = []
            comparisons = {
                "schema_result": (observed_summary["schema_result"], expected["schema_result"]),
                "admissibility_result": (observed_summary["admissibility_result"], expected["admissibility_result"]),
                "execution_result": (observed_summary["execution_result"], expected["execution_result"]),
                "sidecar_status": (observed_summary["sidecar_status"], expected["sidecar_status"]),
                "unit_feedback_status": (observed_summary["unit_feedback_status"], expected["unit_feedback_status"]),
                "terminal_stop_code": (observed_summary["terminal_stop_code"], expected["terminal_stop_code"]),
            }
            for key, (actual, exp) in comparisons.items():
                if actual != exp:
                    fixture_failures.append(f"{key}_mismatch:{actual}!={exp}")

            fixture_bad_counters = enrich_negative_controls(fixture_id, packet, observed)
            for key, value in fixture_bad_counters.items():
                aggregate_bad_counters[key] += int(value)

            nonzero = {k: v for k, v in fixture_bad_counters.items() if v != 0}
            for k, v in nonzero.items():
                fixture_failures.append(f"bad_counter_nonzero:{k}:{v}")

            fixture_gate = "PASS" if not fixture_failures else "FAIL"

            receipt = {
                "schema_version": "double_sieve_fixture_receipt_v0",
                "fixture_id": fixture_id,
                "run_id": run_id,
                "fixture_goal": packet.get("fixture_goal"),
                "source_fixture_packet_ref": rel(packet_path),
                "schema_result": observed_summary["schema_result"],
                "admissibility_result": observed_summary["admissibility_result"],
                "execution_result": observed_summary["execution_result"],
                "sidecar_status": observed_summary["sidecar_status"],
                "unit_feedback_status": observed_summary["unit_feedback_status"],
                "expected_terminal": expected["terminal_stop_code"],
                "observed_terminal": observed_summary["terminal_stop_code"],
                "fixture_gate": fixture_gate,
                "failures": fixture_failures,
                "proof_flags": observed.get("proof_flags", {}),
                "negative_controls": fixture_bad_counters,
                "observed": observed,
                "expected": expected,
                "terminal": observed["terminal"],
            }

            write_json(fixture_receipt_path(fixture_id), receipt)
            fixture_receipts.append(receipt)

            if fixture_failures:
                all_fixture_failures.extend([f"{fixture_id}:{f}" for f in fixture_failures])

    for f in all_fixture_failures:
        failures.append(f)

    fixtures_total = len(REQUIRED_FIXTURES)
    fixtures_passed = sum(1 for r in fixture_receipts if r.get("fixture_gate") == "PASS")
    fixtures_failed = fixtures_total - fixtures_passed

    schema_counts = Counter(r.get("schema_result") for r in fixture_receipts)
    admissibility_counts = Counter(r.get("admissibility_result") for r in fixture_receipts)
    execution_counts = Counter(r.get("execution_result") for r in fixture_receipts)
    sidecar_counts = Counter(r.get("sidecar_status") for r in fixture_receipts)
    feedback_counts = Counter(r.get("unit_feedback_status") for r in fixture_receipts)

    bad_counters_zero = all(v == 0 for v in aggregate_bad_counters.values())

    by_id = {r["fixture_id"]: r for r in fixture_receipts}
    f2 = by_id.get("F2_INVALID_SCHEMA", {})
    f3 = by_id.get("F3_AUTHORITY_REQUIRED", {})
    f4 = by_id.get("F4_FORBIDDEN_INPUT", {})
    f5 = by_id.get("F5_EXECUTION_FAILURE_TYPED_FEEDBACK", {})
    f6 = by_id.get("F6_SIDECAR_PARTIAL_OBSERVABILITY", {})

    invalid_schema_stopped_before_admissibility = (
        f2.get("schema_result") == "MISSING_FIELD"
        and f2.get("admissibility_result") == "NOT_RUN"
        and f2.get("execution_result") == "NOT_RUN"
    )
    valid_unauthorized_stopped_at_admissibility = (
        f3.get("schema_result") == "VALID"
        and f3.get("admissibility_result") == "AUTHORITY_REQUIRED"
        and f3.get("execution_result") == "NOT_RUN"
    )
    forbidden_input_stopped_before_execution = (
        f4.get("schema_result") == "VALID"
        and f4.get("admissibility_result") == "FORBIDDEN_INPUT"
        and f4.get("execution_result") == "NOT_RUN"
    )
    execution_failure_typed_feedback_emitted = (
        f5.get("schema_result") == "VALID"
        and f5.get("admissibility_result") == "ALLOW"
        and f5.get("execution_result") == "FAILED_TYPED"
        and f5.get("unit_feedback_status") == "EMITTED_ACTIONABLE"
    )
    sidecar_degradation_no_false_claim = (
        f6.get("sidecar_status") == "OBSERVATION_UNDER_TYPED"
        and f6.get("execution_result") == "CONTROL_RESULT_PRESERVED_WITH_OBSERVABILITY_DEGRADED"
        and f6.get("negative_controls", {}).get("false_observability_claim_count", 1) == 0
    )
    sidecar_zero_authority_preserved = all(
        r.get("negative_controls", {}).get("sidecar_authorized_move_count", 1) == 0
        and r.get("negative_controls", {}).get("sidecar_denied_move_count", 1) == 0
        and r.get("negative_controls", {}).get("sidecar_state_mutation_count", 1) == 0
        and r.get("negative_controls", {}).get("sidecar_authority_claim_count", 1) == 0
        for r in fixture_receipts
    )

    if fixtures_passed != fixtures_total:
        failures.append(f"fixture_mismatch:passed={fixtures_passed}:total={fixtures_total}")
    if not bad_counters_zero:
        failures.append("bad_counters_nonzero")
    if aggregate_bad_counters.get("invalid_schema_reached_admissibility_count", 0):
        failures.append("invalid_schema_reached_admissibility")
    if aggregate_bad_counters.get("admissibility_denied_executed_count", 0):
        failures.append("admissibility_denied_executed")
    if aggregate_bad_counters.get("forbidden_input_executed_count", 0):
        failures.append("forbidden_input_executed")
    if aggregate_bad_counters.get("sidecar_authority_claim_count", 0) or aggregate_bad_counters.get("sidecar_authorized_move_count", 0):
        failures.append("sidecar_authority_leak")
    if aggregate_bad_counters.get("bare_failed_status_count", 0):
        failures.append("bare_failed_status")
    if aggregate_bad_counters.get("false_observability_claim_count", 0):
        failures.append("false_observability_claim")
    if aggregate_bad_counters.get("live_mutation_count", 0):
        failures.append("live_mutation_detected")
    if aggregate_bad_counters.get("c7_opened_count", 0):
        failures.append("c7_opened")
    if aggregate_bad_counters.get("c8_opened_count", 0):
        failures.append("c8_opened")

    gate, status, outcome_class = stop_for_failure(failures)
    terminal = terminal_for(gate, failures)

    rollup = {
        "schema_version": "double_sieve_fixture_suite_rollup_v0",
        "suite_id": suite_id,
        "run_id": run_id,
        "milestone": MILESTONE,
        "fixtures_total": fixtures_total,
        "fixtures_passed": fixtures_passed,
        "fixtures_failed": fixtures_failed,
        "schema_results": dict(schema_counts),
        "admissibility_results": dict(admissibility_counts),
        "execution_results": dict(execution_counts),
        "sidecar_results": dict(sidecar_counts),
        "unit_feedback_results": dict(feedback_counts),
        "unit_feedback": {
            "required": 1,
            "emitted": feedback_counts.get("EMITTED_ACTIONABLE", 0),
            "bare_failed_status_count": aggregate_bad_counters.get("bare_failed_status_count", 0)
        },
        "bad_counters": aggregate_bad_counters,
        "suite_gate": gate,
        "terminal": terminal,
    }

    readout = {
        "schema_version": "double_sieve_fixture_suite_readout_v0",
        "title": "Double-sieve fixture suite readout",
        "fixtures": {
            "total": fixtures_total,
            "passed": fixtures_passed,
            "failed": fixtures_failed,
        },
        "schema_validator": {
            "invalid_schema_reached_admissibility": aggregate_bad_counters.get("invalid_schema_reached_admissibility_count", 0),
            "schema_results": dict(schema_counts),
        },
        "lawful_admissibility": {
            "denied_move_executed": aggregate_bad_counters.get("admissibility_denied_executed_count", 0),
            "forbidden_input_executed": aggregate_bad_counters.get("forbidden_input_executed_count", 0),
            "admissibility_results": dict(admissibility_counts),
        },
        "execution": {
            "execution_gate_opened_no_live_mutation": execution_counts.get("EXECUTION_GATE_OPENED_NO_LIVE_MUTATION", 0),
            "execution_failed_typed": execution_counts.get("FAILED_TYPED", 0),
            "bare_failed": aggregate_bad_counters.get("bare_failed_status_count", 0),
            "execution_results": dict(execution_counts),
        },
        "observability": {
            "complete": sidecar_counts.get("OBSERVATION_COMPLETE", 0),
            "under_typed_degraded": sidecar_counts.get("OBSERVATION_UNDER_TYPED", 0),
            "sidecar_authority_actions": aggregate_bad_counters.get("sidecar_authorized_move_count", 0) + aggregate_bad_counters.get("sidecar_denied_move_count", 0),
            "false_full_observability_claims": aggregate_bad_counters.get("false_observability_claim_count", 0),
        },
        "outcome": "DOUBLE_SIEVE_FIXTURE_SUITE_PASS" if gate == "PASS" else "DOUBLE_SIEVE_FIXTURE_SUITE_FAIL",
        "interpretation": "The runtime membranes are separated and executable across the six essential pre-C7 fixture paths." if gate == "PASS" else "The fixture suite exposed a typed boundary failure.",
    }

    profile = {
        "schema_version": "double_sieve_fixture_suite_profile_v0",
        "profile_id": "double_sieve_fixture_suite_profile_" + sig8(rollup),
        "suite_id": suite_id,
        "run_id": run_id,
        "status": "DOUBLE_SIEVE_PASS" if gate == "PASS" else "DOUBLE_SIEVE_BLOCKED_OR_FAILED",
        "core_rule": "Before testing runtime radius, prove the runtime knows where it must stop.",
        "runtime_mode": "FIXTURE_SUITE_ONLY",
        "source_runtime_membranes_receipt_ref": rel(MEMBRANE_RECEIPT_PATH),
        "fixture_manifest_ref": rel(MANIFEST_PATH),
        "bad_counters_zero": bad_counters_zero,
        "must_not_infer": [
            "C7 is authorized",
            "C8 is authorized",
            "runtime radius is proven",
            "general autonomy is proven",
            "fixture expansion is authorized",
            "sidecar evidence is authority",
            "execution allowed means live mutation occurred"
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "double_sieve_fixture_suite_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "suite_id": suite_id,
        "run_id": run_id,
        "status": status,
        "outcome_class": outcome_class,
        "summary": {
            "suite_passed": gate == "PASS",
            "fixtures_total": fixtures_total,
            "fixtures_passed": fixtures_passed,
            "fixtures_failed": fixtures_failed,
            "invalid_schema_stopped_before_admissibility": invalid_schema_stopped_before_admissibility,
            "valid_unauthorized_stopped_at_admissibility": valid_unauthorized_stopped_at_admissibility,
            "forbidden_input_stopped_before_execution": forbidden_input_stopped_before_execution,
            "execution_failure_typed_feedback_emitted": execution_failure_typed_feedback_emitted,
            "sidecar_degradation_no_false_claim": sidecar_degradation_no_false_claim,
            "sidecar_zero_authority_preserved": sidecar_zero_authority_preserved,
            "bad_counters_zero": bad_counters_zero,
            "runtime_mode": "FIXTURE_SUITE_ONLY",
            "live_mutation_authorized": False,
            "live_mutation_executed": False,
            "c7_opened": False,
            "c8_opened": False,
        },
        "failures": failures,
        "warnings": warnings,
    }

    transition_trace = {
        "schema_version": "double_sieve_fixture_suite_transition_trace_v0",
        "unit_id": UNIT_ID,
        "suite_id": suite_id,
        "run_id": run_id,
        "transitions": [
            {
                "from": "R0_RUNTIME_MEMBRANES_EXECUTABLE_READY",
                "edge": "load committed fixture-mode membranes and suite contract",
                "to": "DOUBLE_SIEVE_FIXTURE_CONTEXT_BOUND" if gate == "PASS" else "DOUBLE_SIEVE_BLOCKED"
            },
            {
                "from": "DOUBLE_SIEVE_FIXTURE_CONTEXT_BOUND" if gate == "PASS" else "DOUBLE_SIEVE_BLOCKED",
                "edge": "run six deterministic boundary fixtures through membranes",
                "to": "DOUBLE_SIEVE_FIXTURE_RESULTS_AGGREGATED" if gate == "PASS" else "DOUBLE_SIEVE_FIXTURE_FAILURE_TYPED"
            },
            {
                "from": "DOUBLE_SIEVE_FIXTURE_RESULTS_AGGREGATED" if gate == "PASS" else "DOUBLE_SIEVE_FIXTURE_FAILURE_TYPED",
                "edge": "emit suite receipt and stop",
                "to": terminal["stop_code"]
            }
        ],
        "fixture_receipt_refs": [rel(fixture_receipt_path(r["fixture_id"])) for r in fixture_receipts],
        "terminal": terminal,
    }

    write_json(ROLLUP_PATH, rollup)
    write_json(READOUT_PATH, readout)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRANSITION_TRACE_PATH, transition_trace)

    acceptance_gate_results = {
        "DOUBLE_SIEVE_0_R0_ACTIVE_SOURCE_PACKET_LOADED": R0_PACKET_PATH.exists() and bool(r0_packet),
        "DOUBLE_SIEVE_1_RUNTIME_MEMBRANE_RUNNER_LOADED": HARNESS_SCRIPT_PATH.exists() and bool(membrane_receipt),
        "DOUBLE_SIEVE_2_FIXTURE_MANIFEST_DECLARED": MANIFEST_PATH.exists(),
        "DOUBLE_SIEVE_3_EXACTLY_SIX_REQUIRED_FIXTURES": manifest_ids == REQUIRED_FIXTURES,
        "DOUBLE_SIEVE_4_NO_FIXTURE_DISCOVERY": True,
        "DOUBLE_SIEVE_5_NO_LATEST_OR_MTIME_SELECTION": aggregate_bad_counters.get("latest_file_selection_executed_count", 0) == 0 and aggregate_bad_counters.get("mtime_selection_executed_count", 0) == 0,
        "DOUBLE_SIEVE_6_F1_VALID_ADMISSIBLE_PASS": by_id.get("F1_VALID_ADMISSIBLE", {}).get("fixture_gate") == "PASS",
        "DOUBLE_SIEVE_7_F2_INVALID_SCHEMA_BLOCKS_BEFORE_ADMISSIBILITY": invalid_schema_stopped_before_admissibility,
        "DOUBLE_SIEVE_8_F3_VALID_AUTHORITY_REQUIRED_BLOCKS_BEFORE_EXECUTION": valid_unauthorized_stopped_at_admissibility,
        "DOUBLE_SIEVE_9_F4_FORBIDDEN_INPUT_BLOCKS_BEFORE_EXECUTION": forbidden_input_stopped_before_execution,
        "DOUBLE_SIEVE_10_F5_EXECUTION_FAILURE_TYPED_FEEDBACK_EMITTED": execution_failure_typed_feedback_emitted,
        "DOUBLE_SIEVE_11_F6_OBSERVABILITY_DEGRADED_NO_FALSE_CLAIM": sidecar_degradation_no_false_claim,
        "DOUBLE_SIEVE_12_INVALID_SCHEMA_NEVER_REACHES_ADMISSIBILITY": aggregate_bad_counters.get("invalid_schema_reached_admissibility_count", 0) == 0,
        "DOUBLE_SIEVE_13_SCHEMA_VALID_NOT_TREATED_AS_ADMISSIBILITY_ALLOW": aggregate_bad_counters.get("schema_valid_counted_as_admissible_count", 0) == 0,
        "DOUBLE_SIEVE_14_ADMISSIBILITY_DENIAL_NEVER_EXECUTES": aggregate_bad_counters.get("admissibility_denied_executed_count", 0) == 0,
        "DOUBLE_SIEVE_15_FORBIDDEN_INPUT_NEVER_EXECUTES": aggregate_bad_counters.get("forbidden_input_executed_count", 0) == 0,
        "DOUBLE_SIEVE_16_EXECUTION_FAILURE_NOT_BARE_FAILED": aggregate_bad_counters.get("bare_failed_status_count", 0) == 0,
        "DOUBLE_SIEVE_17_SIDECAR_ZERO_AUTHORITY_PRESERVED": sidecar_zero_authority_preserved,
        "DOUBLE_SIEVE_18_NO_LIVE_MUTATION": aggregate_bad_counters.get("live_mutation_count", 0) == 0,
        "DOUBLE_SIEVE_19_NO_RUNTIME_PATCH": aggregate_bad_counters.get("runtime_patch_count", 0) == 0,
        "DOUBLE_SIEVE_20_NO_MOVE_ADDITION": aggregate_bad_counters.get("move_registry_addition_count", 0) == 0,
        "DOUBLE_SIEVE_21_NO_SCHEMA_ARCHIVE_MUTATION": aggregate_bad_counters.get("schema_archive_mutation_count", 0) == 0,
        "DOUBLE_SIEVE_22_NO_FIXTURE_EXPANSION": aggregate_bad_counters.get("fixture_expansion_count", 0) == 0,
        "DOUBLE_SIEVE_23_C7_NOT_OPENED": aggregate_bad_counters.get("c7_opened_count", 0) == 0,
        "DOUBLE_SIEVE_24_C8_NOT_OPENED": aggregate_bad_counters.get("c8_opened_count", 0) == 0,
        "DOUBLE_SIEVE_25_FIXTURE_RECEIPTS_EMITTED": len(fixture_receipts) == fixtures_total,
        "DOUBLE_SIEVE_26_SUITE_ROLLUP_READOUT_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and READOUT_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
        "DOUBLE_SIEVE_27_SUITE_RECEIPT_EMITTED": True,
        "DOUBLE_SIEVE_28_BAD_COUNTERS_ZERO": bad_counters_zero,
        "DOUBLE_SIEVE_29_NO_HIDDEN_NEXT_COMMAND": aggregate_bad_counters.get("hidden_next_command_count", 0) == 0,
        "DOUBLE_SIEVE_30_RUNTIME_MEMBRANE_RECEIPT_VERIFIED": bool(membrane_receipt) and membrane_receipt.get("gate") == "PASS",
        "DOUBLE_SIEVE_31_SELECTED_SCHEMA_SURFACE_BOUND": bool(membrane_receipt.get("output_artifacts", {}).get("schema_validator_membrane")),
        "DOUBLE_SIEVE_32_SELECTED_AUTHORITY_REGIME_BOUND": bool(membrane_receipt.get("output_artifacts", {}).get("lawful_admissibility_membrane")),
        "DOUBLE_SIEVE_33_SELECTED_SIDECAR_SURFACE_BOUND": bool(membrane_receipt.get("output_artifacts", {}).get("observability_sidecar_membrane")),
        "DOUBLE_SIEVE_34_NO_REPO_WIDE_MEMBRANE_DISCOVERY": aggregate_bad_counters.get("repo_wide_membrane_discovery_count", 0) == 0,
    }

    receipt = {
        "schema_version": "double_sieve_fixture_suite_receipt_v0",
        "receipt_type": "TYPED_DOUBLE_SIEVE_FIXTURE_SUITE_RECEIPT",
        "created_at": now_iso(),
        "receipt_id": None,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "suite_id": suite_id,
        "run_id": run_id,
        "gate": gate,
        "status": status,
        "outcome_class": outcome_class,
        "failures": failures,
        "warnings": warnings,
        "fixture_receipts": [rel(fixture_receipt_path(r["fixture_id"])) for r in fixture_receipts],
        "machine_readable_double_sieve_summary": {
            "suite_passed": gate == "PASS",
            "fixtures_total": fixtures_total,
            "fixtures_passed": fixtures_passed,
            "fixtures_failed": fixtures_failed,
            "invalid_schema_stopped_before_admissibility": invalid_schema_stopped_before_admissibility,
            "valid_unauthorized_stopped_at_admissibility": valid_unauthorized_stopped_at_admissibility,
            "forbidden_input_stopped_before_execution": forbidden_input_stopped_before_execution,
            "execution_failure_typed_feedback_emitted": execution_failure_typed_feedback_emitted,
            "sidecar_degradation_no_false_claim": sidecar_degradation_no_false_claim,
            "sidecar_zero_authority_preserved": sidecar_zero_authority_preserved,
            "runtime_membrane_receipt_verified": bool(membrane_receipt) and membrane_receipt.get("gate") == "PASS",
            "runtime_mode": "FIXTURE_SUITE_ONLY",
            "schema_results": dict(schema_counts),
            "admissibility_results": dict(admissibility_counts),
            "execution_results": dict(execution_counts),
            "sidecar_results": dict(sidecar_counts),
            "unit_feedback_results": dict(feedback_counts),
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
        "negative_controls": aggregate_bad_counters,
        "output_artifacts": {
            "suite_contract": rel(CONTRACT_PATH),
            "fixture_manifest": rel(MANIFEST_PATH),
            "fixtures_dir": rel(FIXTURE_DIR),
            "rollup": rel(ROLLUP_PATH),
            "readout": rel(READOUT_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
    }

    receipt_id = "double_sieve_fixture_suite_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"double_sieve_fixture_suite_receipt_id={receipt_id}")
    print(f"double_sieve_fixture_suite_receipt_path={rel(receipt_path)}")
    print(f"double_sieve_fixture_suite_id={suite_id}")
    print(f"double_sieve_suite_run_id={run_id}")
    print(f"double_sieve_terminal_stop_code={terminal['stop_code']}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
