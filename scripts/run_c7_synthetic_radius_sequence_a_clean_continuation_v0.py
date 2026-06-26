#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RUN_C7_SYNTHETIC_RADIUS_SEQUENCE_A_CLEAN_CONTINUATION_V0"
TARGET_UNIT_ID = "runtime.practical_radius_expansion.synthetic.sequence_A.clean_continuation.v0"
NEXT_UNIT_ID = "RUN_C7_SYNTHETIC_RADIUS_NEGATIVE_HALTS_B_C_V0"

LAYER = "RUNTIME / C7 / SYNTHETIC_TEST / SEQUENCE_A"
MODE = "RUN_SYNTHETIC_FIXTURE / CLEAN_CONTINUATION_ONLY / NO_LIVE_RUNTIME"
BUILD_MODE = "C7_SYNTHETIC_SEQUENCE_A_RUN_ONLY"

SOURCE_C7_RUNNER_RECEIPT_ID = "0b9012bf"

C7_RUNNER_RECEIPT_PATH = ROOT / "data/c7_synthetic_runtime_radius_runner_v0_receipts/0b9012bf.json"
RUNNER_PATH = ROOT / "scripts/run_c7_synthetic_runtime_radius_v0.py"
SEQUENCE_A_TARGET_PATH = ROOT / "data/c7_synthetic_runtime_radius_runner_v0/c7_sequence_a_run_target_v0.json"
RUNNER_MANIFEST_PATH = ROOT / "data/c7_synthetic_runtime_radius_runner_v0/c7_synthetic_runner_manifest_v0.json"
RUNNER_CONTRACT_PATH = ROOT / "data/c7_synthetic_runtime_radius_runner_v0/c7_synthetic_runner_contract_v0.json"

FIXTURE_A_PATH = ROOT / "data/c7_synthetic_runtime_radius_fixtures_v0/fixtures/sequence_A_clean_continuation.json"
FIXTURE_INDEX_PATH = ROOT / "data/c7_synthetic_runtime_radius_fixtures_v0/c7_synthetic_fixture_index_v0.json"
EXPECTED_OUTCOMES_PATH = ROOT / "data/c7_synthetic_runtime_radius_fixtures_v0/c7_synthetic_fixture_expected_outcomes_v0.json"

STEP_PACKET_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_step_packet_contract_v0.json"
STOP_PACKET_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_stop_packet_contract_v0.json"
BUDGET_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_budget_v0.json"
NEGATIVE_COUNTER_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_negative_counter_contract_v0.json"
ROLLUP_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_rollup_contract_v0.json"
READOUT_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_readout_contract_v0.json"

OUT_DIR = ROOT / "data/c7_synthetic_radius_sequence_a_clean_continuation_v0"
RECEIPT_DIR = ROOT / "data/c7_synthetic_radius_sequence_a_clean_continuation_v0_receipts"

BASIS_PATH = OUT_DIR / "c7_sequence_a_run_basis_v0.json"
RUN_RESULT_PATH = OUT_DIR / "c7_sequence_a_run_result_v0.json"
RUN_ARTIFACT_LINKS_PATH = OUT_DIR / "c7_sequence_a_run_artifact_links_v0.json"
ASSERTION_REPORT_PATH = OUT_DIR / "c7_sequence_a_assertion_report_v0.json"
NEXT_TARGET_PATH = OUT_DIR / "c7_negative_halts_b_c_run_target_v0.json"
ROLLUP_PATH = OUT_DIR / "c7_sequence_a_run_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c7_sequence_a_run_profile_v0.json"
TRACE_PATH = OUT_DIR / "c7_sequence_a_run_transition_trace.json"

EXPECTED_RUNNER_STATUS = "TYPED_C7_SYNTHETIC_RUNTIME_RADIUS_RUNNER_BUILT_SEQUENCE_A_NEXT"
EXPECTED_FIXTURE_ID = "sequence_A_clean_continuation"
EXPECTED_OUTCOME = "RADIUS_EXPANDED_CLEANLY"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def extract_marker(stdout: str, key: str) -> str | None:
    prefix = key + "="
    for line in stdout.splitlines():
        if line.startswith(prefix):
            return line.split("=", 1)[1].strip()
    return None

def require_false(obj: Dict[str, Any], key: str, failures: List[str]) -> None:
    if obj.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{obj.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        C7_RUNNER_RECEIPT_PATH,
        RUNNER_PATH,
        SEQUENCE_A_TARGET_PATH,
        RUNNER_MANIFEST_PATH,
        RUNNER_CONTRACT_PATH,
        FIXTURE_A_PATH,
        FIXTURE_INDEX_PATH,
        EXPECTED_OUTCOMES_PATH,
        STEP_PACKET_CONTRACT_PATH,
        STOP_PACKET_CONTRACT_PATH,
        BUDGET_PATH,
        NEGATIVE_COUNTER_CONTRACT_PATH,
        ROLLUP_CONTRACT_PATH,
        READOUT_CONTRACT_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    runner_receipt = read_json(C7_RUNNER_RECEIPT_PATH)
    runner_summary = runner_receipt.get("machine_readable_c7_synthetic_runner_summary", {})
    sequence_a_target = read_json(SEQUENCE_A_TARGET_PATH)
    runner_manifest = read_json(RUNNER_MANIFEST_PATH)
    runner_contract = read_json(RUNNER_CONTRACT_PATH)
    fixture_a = read_json(FIXTURE_A_PATH)
    expected_outcomes = read_json(EXPECTED_OUTCOMES_PATH)

    if runner_receipt.get("receipt_id") != SOURCE_C7_RUNNER_RECEIPT_ID:
        failures.append(f"runner_receipt_id_wrong:{runner_receipt.get('receipt_id')}")
    if runner_receipt.get("gate") != "PASS":
        failures.append(f"runner_receipt_gate_wrong:{runner_receipt.get('gate')}")
    if runner_summary.get("status") != EXPECTED_RUNNER_STATUS:
        failures.append(f"runner_status_wrong:{runner_summary.get('status')}")
    if runner_summary.get("next_unit_id") != UNIT_ID:
        failures.append(f"runner_next_unit_wrong:{runner_summary.get('next_unit_id')}")
    if runner_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("runner_terminal_not_advance")
    if runner_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("runner_terminal_next_wrong")
    if runner_summary.get("ready_for_sequence_a_test_run") is not True:
        failures.append("runner_not_ready_for_sequence_a")
    if runner_summary.get("ready_for_all_c7_test_runs") is not False:
        failures.append("runner_all_tests_should_not_be_ready_yet")

    if sequence_a_target.get("target_status") != "SEQUENCE_A_READY":
        failures.append(f"sequence_a_target_status_wrong:{sequence_a_target.get('target_status')}")
    if sequence_a_target.get("fixture_id") != EXPECTED_FIXTURE_ID:
        failures.append(f"sequence_a_target_fixture_wrong:{sequence_a_target.get('fixture_id')}")
    if sequence_a_target.get("expected_outcome") != EXPECTED_OUTCOME:
        failures.append(f"sequence_a_target_expected_wrong:{sequence_a_target.get('expected_outcome')}")
    if sequence_a_target.get("synthetic_test_only") is not True:
        failures.append("sequence_a_target_not_synthetic_only")
    if sequence_a_target.get("does_not_authorize_live_runtime") is not True:
        failures.append("sequence_a_target_live_runtime_boundary_missing")

    if runner_manifest.get("runner_path") != rel(RUNNER_PATH):
        failures.append(f"runner_manifest_path_wrong:{runner_manifest.get('runner_path')}")
    if runner_contract.get("contract_status") != "FROZEN":
        failures.append("runner_contract_not_frozen")
    if EXPECTED_FIXTURE_ID not in runner_contract.get("fixture_allowlist", []):
        failures.append("sequence_a_not_in_runner_allowlist")
    if runner_contract.get("first_run_fixture") != EXPECTED_FIXTURE_ID:
        failures.append(f"runner_first_fixture_wrong:{runner_contract.get('first_run_fixture')}")

    if fixture_a.get("fixture_id") != EXPECTED_FIXTURE_ID:
        failures.append(f"fixture_id_wrong:{fixture_a.get('fixture_id')}")
    if fixture_a.get("expected_outcome") != EXPECTED_OUTCOME:
        failures.append(f"fixture_expected_outcome_wrong:{fixture_a.get('expected_outcome')}")
    if expected_outcomes.get("expected_outcomes", {}).get(EXPECTED_FIXTURE_ID) != EXPECTED_OUTCOME:
        failures.append("expected_outcomes_index_wrong")

    for key in [
        "c7_live_runtime_run_authorized",
        "runtime_adoption_authorized",
        "live_runtime_hooks_installed",
        "runtime_patched",
        "runtime_routing_installed",
        "validation_verdict_emitted",
        "admissibility_checked",
        "authorization_verdict_emitted",
        "execution_claimed",
        "schema_archive_mutated",
        "schema_created",
        "control_path_blocked",
        "control_path_advanced",
        "hidden_next_command",
    ]:
        require_false(runner_summary, key, failures)

    runner_stdout = ""
    runner_stderr = ""
    runner_returncode = None
    run_receipt_path_str = None
    run_outcome = None

    if not failures:
        proc = subprocess.run(
            [
                "python3",
                rel(RUNNER_PATH),
                "--fixture-id",
                EXPECTED_FIXTURE_ID,
                "--expected-fixture",
                EXPECTED_FIXTURE_ID,
            ],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        runner_stdout = proc.stdout
        runner_stderr = proc.stderr
        runner_returncode = proc.returncode

        if proc.returncode != 0:
            failures.append(f"runner_exit_code:{proc.returncode}")

        run_receipt_path_str = extract_marker(proc.stdout, "c7_synthetic_run_receipt_path")
        run_outcome = extract_marker(proc.stdout, "c7_synthetic_run_outcome")

        if not run_receipt_path_str:
            failures.append("run_receipt_path_not_emitted")
        elif not (ROOT / run_receipt_path_str).exists():
            failures.append(f"run_receipt_missing:{run_receipt_path_str}")

        if run_outcome != EXPECTED_OUTCOME:
            failures.append(f"run_outcome_wrong:{run_outcome}")

    run_receipt = {}
    run_rollup = {}
    run_readout = {}

    if run_receipt_path_str and (ROOT / run_receipt_path_str).exists():
        run_receipt = read_json(ROOT / run_receipt_path_str)
        rollup_path = ROOT / run_receipt.get("output_artifacts", {}).get("rollup", "")
        readout_path = ROOT / run_receipt.get("output_artifacts", {}).get("readout", "")
        if rollup_path.exists():
            run_rollup = read_json(rollup_path)
        else:
            failures.append(f"run_rollup_missing:{rollup_path}")
        if readout_path.exists():
            run_readout = read_json(readout_path)
        else:
            failures.append(f"run_readout_missing:{readout_path}")

    if run_receipt:
        if run_receipt.get("gate") != "PASS":
            failures.append(f"run_receipt_gate_wrong:{run_receipt.get('gate')}")
        if run_receipt.get("fixture_id") != EXPECTED_FIXTURE_ID:
            failures.append(f"run_receipt_fixture_wrong:{run_receipt.get('fixture_id')}")
        if run_receipt.get("outcome") != EXPECTED_OUTCOME:
            failures.append(f"run_receipt_outcome_wrong:{run_receipt.get('outcome')}")
        if run_receipt.get("expected_outcome") != EXPECTED_OUTCOME:
            failures.append(f"run_receipt_expected_wrong:{run_receipt.get('expected_outcome')}")
        if run_receipt.get("synthetic_run_only") is not True:
            failures.append("run_receipt_not_synthetic_only")
        if run_receipt.get("runtime_adoption_authorized") is not False:
            failures.append("run_receipt_runtime_adoption_boundary_wrong")
        if run_receipt.get("c7_live_runtime_run") is not False:
            failures.append("run_receipt_live_runtime_boundary_wrong")

    if run_rollup:
        if run_rollup.get("outcome") != EXPECTED_OUTCOME:
            failures.append(f"rollup_outcome_wrong:{run_rollup.get('outcome')}")
        if run_rollup.get("steps_attempted") != 3:
            failures.append(f"steps_attempted_wrong:{run_rollup.get('steps_attempted')}")
        if run_rollup.get("steps_advanced") != 2:
            failures.append(f"steps_advanced_wrong:{run_rollup.get('steps_advanced')}")
        if run_rollup.get("steps_halted") != 1:
            failures.append(f"steps_halted_wrong:{run_rollup.get('steps_halted')}")
        if run_rollup.get("halts", {}).get("untyped_halt_count") != 0:
            failures.append("untyped_halt_count_nonzero")
        for k, v in run_rollup.get("bad_counters", {}).items():
            if v != 0:
                failures.append(f"bad_counter_nonzero:{k}:{v}")

    if run_readout:
        if run_readout.get("interpretation") != f"Synthetic C7 fixture classified as {EXPECTED_OUTCOME}.":
            failures.append("readout_interpretation_wrong")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C7_SYNTHETIC_SEQUENCE_A_CLEAN_CONTINUATION_PASS_NEGATIVE_HALTS_NEXT" if gate == "PASS" else "TYPED_C7_SYNTHETIC_SEQUENCE_A_CLEAN_CONTINUATION_GATE_FAIL"

    source_hash_manifest = {rel(p): file_sha256(p) for p in required}

    basis = {
        "schema_version": "c7_sequence_a_run_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_c7_runner_receipt_id": SOURCE_C7_RUNNER_RECEIPT_ID,
        "source_files": source_hash_manifest,
        "basis_claim": "C7 synthetic runner passed and named Sequence A clean continuation as the next typed unit.",
        "does_not_authorize": [
            "live runtime run",
            "runtime adoption",
            "runtime patching",
            "live hooks",
            "runtime routing",
            "schema mutation",
            "control path authority",
        ],
    }

    run_result = {
        "schema_version": "c7_sequence_a_run_result_v0",
        "run_status": status,
        "fixture_id": EXPECTED_FIXTURE_ID,
        "expected_outcome": EXPECTED_OUTCOME,
        "observed_outcome": run_outcome,
        "runner_returncode": runner_returncode,
        "runner_stdout": runner_stdout,
        "runner_stderr": runner_stderr,
        "run_receipt_path": run_receipt_path_str,
        "synthetic_run_only": True,
        "live_runtime_run": False,
        "runtime_adoption_authorized": False,
    }

    artifact_links = {
        "schema_version": "c7_sequence_a_run_artifact_links_v0",
        "artifact_status": "EMITTED" if gate == "PASS" else "PARTIAL",
        "runner_receipt": rel(C7_RUNNER_RECEIPT_PATH),
        "synthetic_run_receipt": run_receipt_path_str,
        "synthetic_step_packets": run_receipt.get("output_artifacts", {}).get("step_packets"),
        "synthetic_stop_packet": run_receipt.get("output_artifacts", {}).get("stop_packet"),
        "synthetic_rollup": run_receipt.get("output_artifacts", {}).get("rollup"),
        "synthetic_readout": run_receipt.get("output_artifacts", {}).get("readout"),
    }

    assertion_report = {
        "schema_version": "c7_sequence_a_assertion_report_v0",
        "assertion_status": "PASS" if gate == "PASS" else "FAIL",
        "failures": failures,
        "assertions": {
            "fixture_id_is_sequence_A": fixture_a.get("fixture_id") == EXPECTED_FIXTURE_ID,
            "expected_outcome_matched": run_outcome == EXPECTED_OUTCOME,
            "run_receipt_gate_pass": run_receipt.get("gate") == "PASS",
            "rollup_outcome_matched": run_rollup.get("outcome") == EXPECTED_OUTCOME,
            "steps_attempted_3": run_rollup.get("steps_attempted") == 3,
            "steps_advanced_2": run_rollup.get("steps_advanced") == 2,
            "steps_halted_1": run_rollup.get("steps_halted") == 1,
            "untyped_halt_zero": run_rollup.get("halts", {}).get("untyped_halt_count") == 0,
            "all_bad_counters_zero": all(v == 0 for v in run_rollup.get("bad_counters", {}).values()) if run_rollup else False,
            "synthetic_only": run_receipt.get("synthetic_run_only") is True,
            "live_runtime_not_run": run_receipt.get("c7_live_runtime_run") is False,
            "runtime_adoption_not_authorized": run_receipt.get("runtime_adoption_authorized") is False,
        },
    }

    next_target = {
        "schema_version": "c7_negative_halts_b_c_run_target_v0",
        "target_status": "NEGATIVE_HALTS_B_C_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "fixture_ids": [
            "sequence_B_schema_gap_halt",
            "sequence_C_authority_boundary_halt",
        ],
        "expected_outcomes": {
            "sequence_B_schema_gap_halt": "RADIUS_BLOCKED_BY_SCHEMA_GAP",
            "sequence_C_authority_boundary_halt": "RADIUS_BLOCKED_BY_AUTHORITY_BOUNDARY",
        },
        "synthetic_test_only": True,
        "does_not_authorize_live_runtime": True,
    }

    rollup = {
        "schema_version": "c7_sequence_a_run_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "fixture_id": EXPECTED_FIXTURE_ID,
        "expected_outcome": EXPECTED_OUTCOME,
        "observed_outcome": run_outcome,
        "sequence_a_passed": gate == "PASS",
        "steps_attempted": run_rollup.get("steps_attempted"),
        "steps_advanced": run_rollup.get("steps_advanced"),
        "steps_halted": run_rollup.get("steps_halted"),
        "untyped_halt_count": run_rollup.get("halts", {}).get("untyped_halt_count") if run_rollup else None,
        "bad_counters_zero": all(v == 0 for v in run_rollup.get("bad_counters", {}).values()) if run_rollup else False,
        "ready_for_negative_halts_b_c": gate == "PASS",
        "ready_for_all_c7_test_runs": False,
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "c7_live_runtime_run_authorized": False,
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "control_path_authority_granted": False,
        "hidden_next_command": False,
    }

    profile = {
        "schema_version": "c7_sequence_a_run_profile_v0",
        "profile_status": status,
        "profile": "C7_SYNTHETIC_SEQUENCE_A_CLEAN_CONTINUATION",
        "what_changed": "The first C7 synthetic fixture was run and classified as clean continuation.",
        "what_did_not_change": [
            "negative halt fixtures B/C have not run",
            "handoff/feedback fixtures D/E have not run",
            "live runtime is not authorized",
            "runtime adoption is not authorized",
            "runtime is not patched",
            "live hooks are not installed",
            "schema archive is not mutated",
            "control path authority is not granted",
        ],
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_C7_SYNTHETIC_SEQUENCE_A_RUN_V0",
        "next_command_goal": None,
    }

    trace = {
        "schema_version": "c7_sequence_a_run_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "C7_SYNTHETIC_RUNTIME_RADIUS_RUNNER_BUILT_SEQUENCE_A_NEXT",
                "edge": "consume runner and sequence A target",
                "to": "C7_SEQUENCE_A_RUN_BASIS_ACCEPTED" if gate == "PASS" else "C7_SEQUENCE_A_RUN_BASIS_FAIL",
            },
            {
                "from": "C7_SEQUENCE_A_RUN_BASIS_ACCEPTED" if gate == "PASS" else "C7_SEQUENCE_A_RUN_BASIS_FAIL",
                "edge": "run synthetic clean-continuation fixture",
                "to": "C7_SEQUENCE_A_CLEAN_CONTINUATION_PASS" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C7_SEQUENCE_A_RUN_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (RUN_RESULT_PATH, run_result),
        (RUN_ARTIFACT_LINKS_PATH, artifact_links),
        (ASSERTION_REPORT_PATH, assertion_report),
        (NEXT_TARGET_PATH, next_target),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_PATH, trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "C7_SYNTHETIC_SEQUENCE_A_CLEAN_CONTINUATION_RUN",
        "RUNNER_RECEIPT_CONSUMED",
        "SEQUENCE_A_FIXTURE_CONSUMED",
        "EXPECTED_OUTCOME_MATCHED_RADIUS_EXPANDED_CLEANLY",
        "STEP_PACKETS_EMITTED",
        "STOP_PACKET_EMITTED",
        "ROLLUP_AND_READOUT_EMITTED",
        "BAD_COUNTERS_ZERO",
        "NO_UNTYPED_HALT",
        "NEGATIVE_HALTS_B_C_ARE_NEXT_TYPED_UNIT",
        "NO_LIVE_RUNTIME_RUN",
        "NO_RUNTIME_ADOPTION",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_HOOK_INSTALL",
        "NO_SCHEMA_MUTATION",
        "NO_CONTROL_PATH_AUTHORITY",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt_body = {
        "schema_version": "c7_sequence_a_clean_continuation_receipt_v0",
        "receipt_type": "TYPED_C7_SYNTHETIC_SEQUENCE_A_CLEAN_CONTINUATION_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "source_c7_runner_receipt_id": SOURCE_C7_RUNNER_RECEIPT_ID,
        "source_synthetic_run_receipt_path": run_receipt_path_str,
        "acceptance_gate_results": {
            "C7_SEQUENCE_A_0_RUNNER_RECEIPT_CONSUMED": gate == "PASS",
            "C7_SEQUENCE_A_1_FIXTURE_CONSUMED": gate == "PASS",
            "C7_SEQUENCE_A_2_SYNTHETIC_RUN_EXECUTED": gate == "PASS",
            "C7_SEQUENCE_A_3_EXPECTED_OUTCOME_MATCHED": gate == "PASS",
            "C7_SEQUENCE_A_4_BAD_COUNTERS_ZERO": gate == "PASS",
            "C7_SEQUENCE_A_5_NO_UNTYPED_HALT": gate == "PASS",
            "C7_SEQUENCE_A_6_NEGATIVE_HALTS_NEXT": gate == "PASS",
            "C7_SEQUENCE_A_7_NO_LIVE_RUNTIME_RUN": gate == "PASS",
            "C7_SEQUENCE_A_8_NO_RUNTIME_ADOPTION": gate == "PASS",
            "C7_SEQUENCE_A_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_c7_sequence_a_summary": {
            "status": status,
            "c7_sequence_a_run_done": gate == "PASS",
            "fixture_id": EXPECTED_FIXTURE_ID,
            "expected_outcome": EXPECTED_OUTCOME,
            "observed_outcome": run_outcome,
            "sequence_a_passed": gate == "PASS",
            "steps_attempted": rollup["steps_attempted"],
            "steps_advanced": rollup["steps_advanced"],
            "steps_halted": rollup["steps_halted"],
            "untyped_halt_count": rollup["untyped_halt_count"],
            "bad_counters_zero": rollup["bad_counters_zero"],
            "ready_for_negative_halts_b_c": gate == "PASS",
            "ready_for_all_c7_test_runs": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "c7_live_runtime_run_authorized": False,
            "runtime_adoption_authorized": False,
            "live_runtime_hooks_installed": False,
            "runtime_patched": False,
            "runtime_routing_installed": False,
            "validation_verdict_emitted": False,
            "admissibility_checked": False,
            "authorization_verdict_emitted": False,
            "execution_claimed": False,
            "schema_archive_mutated": False,
            "schema_created": False,
            "control_path_blocked": False,
            "control_path_advanced": False,
            "hidden_next_command": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "run_result": rel(RUN_RESULT_PATH),
            "run_artifact_links": rel(RUN_ARTIFACT_LINKS_PATH),
            "assertion_report": rel(ASSERTION_REPORT_PATH),
            "next_target": rel(NEXT_TARGET_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C7_SEQUENCE_A_RUN_GATE_FAIL",
        },
    }

    receipt_id = sig8(receipt_body)
    receipt_body["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_body["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_body)

    print(json.dumps(receipt_body, indent=2, sort_keys=True))
    print(f"c7_sequence_a_receipt_id={receipt_id}")
    print(f"c7_sequence_a_receipt_path={rel(receipt_path)}")
    print(f"c7_sequence_a_outcome={run_outcome}")
    print(f"c7_sequence_a_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
