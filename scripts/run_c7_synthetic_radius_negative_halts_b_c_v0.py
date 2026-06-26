#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RUN_C7_SYNTHETIC_RADIUS_NEGATIVE_HALTS_B_C_V0"
TARGET_UNIT_ID = "runtime.practical_radius_expansion.synthetic.negative_halts_B_C.v0"
NEXT_UNIT_ID = "RUN_C7_SYNTHETIC_RADIUS_HANDOFF_AND_FEEDBACK_D_E_V0"

LAYER = "RUNTIME / C7 / SYNTHETIC_TEST / NEGATIVE_HALTS_B_C"
MODE = "RUN_SYNTHETIC_FIXTURES / NEGATIVE_HALTS_ONLY / NO_LIVE_RUNTIME"
BUILD_MODE = "C7_SYNTHETIC_NEGATIVE_HALTS_B_C_RUN_ONLY"

SOURCE_C7_SEQUENCE_A_RECEIPT_ID = "2d503369"
SOURCE_C7_RUNNER_RECEIPT_ID = "0b9012bf"

SEQUENCE_A_RECEIPT_PATH = ROOT / "data/c7_synthetic_radius_sequence_a_clean_continuation_v0_receipts/2d503369.json"
NEGATIVE_HALTS_TARGET_PATH = ROOT / "data/c7_synthetic_radius_sequence_a_clean_continuation_v0/c7_negative_halts_b_c_run_target_v0.json"

C7_RUNNER_RECEIPT_PATH = ROOT / "data/c7_synthetic_runtime_radius_runner_v0_receipts/0b9012bf.json"
RUNNER_PATH = ROOT / "scripts/run_c7_synthetic_runtime_radius_v0.py"

FIXTURE_B_PATH = ROOT / "data/c7_synthetic_runtime_radius_fixtures_v0/fixtures/sequence_B_schema_gap_halt.json"
FIXTURE_C_PATH = ROOT / "data/c7_synthetic_runtime_radius_fixtures_v0/fixtures/sequence_C_authority_boundary_halt.json"
FIXTURE_INDEX_PATH = ROOT / "data/c7_synthetic_runtime_radius_fixtures_v0/c7_synthetic_fixture_index_v0.json"
EXPECTED_OUTCOMES_PATH = ROOT / "data/c7_synthetic_runtime_radius_fixtures_v0/c7_synthetic_fixture_expected_outcomes_v0.json"

STEP_PACKET_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_step_packet_contract_v0.json"
STOP_PACKET_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_stop_packet_contract_v0.json"
BUDGET_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_budget_v0.json"
NEGATIVE_COUNTER_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_negative_counter_contract_v0.json"
ROLLUP_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_rollup_contract_v0.json"
READOUT_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_readout_contract_v0.json"

OUT_DIR = ROOT / "data/c7_synthetic_radius_negative_halts_b_c_v0"
RECEIPT_DIR = ROOT / "data/c7_synthetic_radius_negative_halts_b_c_v0_receipts"

BASIS_PATH = OUT_DIR / "c7_negative_halts_b_c_run_basis_v0.json"
RUN_RESULTS_PATH = OUT_DIR / "c7_negative_halts_b_c_run_results_v0.json"
RUN_ARTIFACT_LINKS_PATH = OUT_DIR / "c7_negative_halts_b_c_run_artifact_links_v0.json"
ASSERTION_REPORT_PATH = OUT_DIR / "c7_negative_halts_b_c_assertion_report_v0.json"
NEXT_TARGET_PATH = OUT_DIR / "c7_handoff_and_feedback_d_e_run_target_v0.json"
ROLLUP_PATH = OUT_DIR / "c7_negative_halts_b_c_run_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c7_negative_halts_b_c_run_profile_v0.json"
TRACE_PATH = OUT_DIR / "c7_negative_halts_b_c_run_transition_trace.json"

EXPECTED_SEQUENCE_A_STATUS = "TYPED_C7_SYNTHETIC_SEQUENCE_A_CLEAN_CONTINUATION_PASS_NEGATIVE_HALTS_NEXT"
EXPECTED_RUNNER_STATUS = "TYPED_C7_SYNTHETIC_RUNTIME_RADIUS_RUNNER_BUILT_SEQUENCE_A_NEXT"

FIXTURES = [
    {
        "fixture_id": "sequence_B_schema_gap_halt",
        "expected_outcome": "RADIUS_BLOCKED_BY_SCHEMA_GAP",
        "expected_stop_code": "STOP_SCHEMA_GAP",
        "expected_steps_attempted": 2,
        "expected_steps_advanced": 1,
        "expected_steps_halted": 1,
        "expected_unit_feedback_records": 1,
        "expected_schema_unknown": 1,
        "expected_authority_required": 0,
    },
    {
        "fixture_id": "sequence_C_authority_boundary_halt",
        "expected_outcome": "RADIUS_BLOCKED_BY_AUTHORITY_BOUNDARY",
        "expected_stop_code": "STOP_AUTHORITY_REQUIRED",
        "expected_steps_attempted": 2,
        "expected_steps_advanced": 1,
        "expected_steps_halted": 1,
        "expected_unit_feedback_records": 1,
        "expected_schema_unknown": 0,
        "expected_authority_required": 1,
    },
]

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

def run_fixture(fixture_id: str, expected_outcome: str) -> Dict[str, Any]:
    proc = subprocess.run(
        [
            "python3",
            rel(RUNNER_PATH),
            "--fixture-id",
            fixture_id,
            "--expected-fixture",
            fixture_id,
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )

    run_receipt_path_str = extract_marker(proc.stdout, "c7_synthetic_run_receipt_path")
    observed_outcome = extract_marker(proc.stdout, "c7_synthetic_run_outcome")

    run_receipt: Dict[str, Any] = {}
    run_rollup: Dict[str, Any] = {}
    run_readout: Dict[str, Any] = {}
    stop_packet: Dict[str, Any] = {}
    feedback_records: List[Dict[str, Any]] = []

    if run_receipt_path_str and (ROOT / run_receipt_path_str).exists():
        run_receipt = read_json(ROOT / run_receipt_path_str)
        rollup_path = ROOT / run_receipt.get("output_artifacts", {}).get("rollup", "")
        readout_path = ROOT / run_receipt.get("output_artifacts", {}).get("readout", "")
        stop_path = ROOT / run_receipt.get("output_artifacts", {}).get("stop_packet", "")
        feedback_path = ROOT / run_receipt.get("output_artifacts", {}).get("unit_feedback_records", "")

        if rollup_path.exists():
            run_rollup = read_json(rollup_path)
        if readout_path.exists():
            run_readout = read_json(readout_path)
        if stop_path.exists():
            stop_packet = read_json(stop_path)
        if feedback_path.exists():
            text = feedback_path.read_text().strip()
            feedback_records = [json.loads(line) for line in text.splitlines()] if text else []

    return {
        "fixture_id": fixture_id,
        "expected_outcome": expected_outcome,
        "observed_outcome": observed_outcome,
        "returncode": proc.returncode,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
        "run_receipt_path": run_receipt_path_str,
        "run_receipt": run_receipt,
        "rollup": run_rollup,
        "readout": run_readout,
        "stop_packet": stop_packet,
        "feedback_records": feedback_records,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        SEQUENCE_A_RECEIPT_PATH,
        NEGATIVE_HALTS_TARGET_PATH,
        C7_RUNNER_RECEIPT_PATH,
        RUNNER_PATH,
        FIXTURE_B_PATH,
        FIXTURE_C_PATH,
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

    sequence_a_receipt = read_json(SEQUENCE_A_RECEIPT_PATH)
    sequence_a_summary = sequence_a_receipt.get("machine_readable_c7_sequence_a_summary", {})
    negative_target = read_json(NEGATIVE_HALTS_TARGET_PATH)
    runner_receipt = read_json(C7_RUNNER_RECEIPT_PATH)
    runner_summary = runner_receipt.get("machine_readable_c7_synthetic_runner_summary", {})
    expected_index = read_json(EXPECTED_OUTCOMES_PATH)

    if sequence_a_receipt.get("receipt_id") != SOURCE_C7_SEQUENCE_A_RECEIPT_ID:
        failures.append(f"sequence_a_receipt_id_wrong:{sequence_a_receipt.get('receipt_id')}")
    if sequence_a_receipt.get("gate") != "PASS":
        failures.append(f"sequence_a_gate_wrong:{sequence_a_receipt.get('gate')}")
    if sequence_a_summary.get("status") != EXPECTED_SEQUENCE_A_STATUS:
        failures.append(f"sequence_a_status_wrong:{sequence_a_summary.get('status')}")
    if sequence_a_summary.get("next_unit_id") != UNIT_ID:
        failures.append(f"sequence_a_next_unit_wrong:{sequence_a_summary.get('next_unit_id')}")
    if sequence_a_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("sequence_a_terminal_not_advance")
    if sequence_a_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("sequence_a_terminal_next_wrong")
    if sequence_a_summary.get("ready_for_negative_halts_b_c") is not True:
        failures.append("sequence_a_not_ready_for_negative_halts")

    if negative_target.get("target_status") != "NEGATIVE_HALTS_B_C_NEXT":
        failures.append(f"negative_target_status_wrong:{negative_target.get('target_status')}")
    if negative_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"negative_target_next_wrong:{negative_target.get('next_unit_id')}")
    if negative_target.get("synthetic_test_only") is not True:
        failures.append("negative_target_not_synthetic_only")
    if negative_target.get("does_not_authorize_live_runtime") is not True:
        failures.append("negative_target_live_runtime_boundary_missing")

    if runner_receipt.get("receipt_id") != SOURCE_C7_RUNNER_RECEIPT_ID:
        failures.append(f"runner_receipt_id_wrong:{runner_receipt.get('receipt_id')}")
    if runner_receipt.get("gate") != "PASS":
        failures.append("runner_gate_not_pass")
    if runner_summary.get("status") != EXPECTED_RUNNER_STATUS:
        failures.append(f"runner_status_wrong:{runner_summary.get('status')}")

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
        require_false(sequence_a_summary, key, failures)
        require_false(runner_summary, key, failures)

    for fx in FIXTURES:
        if fx["fixture_id"] not in negative_target.get("fixture_ids", []):
            failures.append(f"fixture_missing_from_negative_target:{fx['fixture_id']}")
        if negative_target.get("expected_outcomes", {}).get(fx["fixture_id"]) != fx["expected_outcome"]:
            failures.append(f"negative_target_expected_wrong:{fx['fixture_id']}")
        if expected_index.get("expected_outcomes", {}).get(fx["fixture_id"]) != fx["expected_outcome"]:
            failures.append(f"expected_index_wrong:{fx['fixture_id']}")

    run_results: List[Dict[str, Any]] = []
    if not failures:
        for fx in FIXTURES:
            run_results.append(run_fixture(fx["fixture_id"], fx["expected_outcome"]))

    for fx, result in zip(FIXTURES, run_results):
        prefix = fx["fixture_id"]

        if result["returncode"] != 0:
            failures.append(f"{prefix}:runner_exit_code:{result['returncode']}")
        if not result["run_receipt_path"]:
            failures.append(f"{prefix}:run_receipt_path_not_emitted")
        elif not (ROOT / result["run_receipt_path"]).exists():
            failures.append(f"{prefix}:run_receipt_missing:{result['run_receipt_path']}")
        if result["observed_outcome"] != fx["expected_outcome"]:
            failures.append(f"{prefix}:outcome_wrong:{result['observed_outcome']}")

        receipt = result["run_receipt"]
        rollup = result["rollup"]
        stop = result["stop_packet"]
        feedback_records = result["feedback_records"]

        if receipt:
            if receipt.get("gate") != "PASS":
                failures.append(f"{prefix}:receipt_gate_wrong:{receipt.get('gate')}")
            if receipt.get("outcome") != fx["expected_outcome"]:
                failures.append(f"{prefix}:receipt_outcome_wrong:{receipt.get('outcome')}")
            if receipt.get("synthetic_run_only") is not True:
                failures.append(f"{prefix}:not_synthetic_only")
            if receipt.get("runtime_adoption_authorized") is not False:
                failures.append(f"{prefix}:runtime_adoption_boundary_wrong")
            if receipt.get("c7_live_runtime_run") is not False:
                failures.append(f"{prefix}:live_runtime_boundary_wrong")

        if rollup:
            if rollup.get("outcome") != fx["expected_outcome"]:
                failures.append(f"{prefix}:rollup_outcome_wrong:{rollup.get('outcome')}")
            if rollup.get("steps_attempted") != fx["expected_steps_attempted"]:
                failures.append(f"{prefix}:steps_attempted_wrong:{rollup.get('steps_attempted')}")
            if rollup.get("steps_advanced") != fx["expected_steps_advanced"]:
                failures.append(f"{prefix}:steps_advanced_wrong:{rollup.get('steps_advanced')}")
            if rollup.get("steps_halted") != fx["expected_steps_halted"]:
                failures.append(f"{prefix}:steps_halted_wrong:{rollup.get('steps_halted')}")
            if rollup.get("halts", {}).get("untyped_halt_count") != 0:
                failures.append(f"{prefix}:untyped_halt_count_nonzero")
            if rollup.get("schema_validation", {}).get("unknown_schema_count") != fx["expected_schema_unknown"]:
                failures.append(f"{prefix}:unknown_schema_count_wrong")
            if rollup.get("cell0_admissibility", {}).get("authority_required_count") != fx["expected_authority_required"]:
                failures.append(f"{prefix}:authority_required_count_wrong")
            for k, v in rollup.get("bad_counters", {}).items():
                if v != 0:
                    failures.append(f"{prefix}:bad_counter_nonzero:{k}:{v}")

        if stop:
            if stop.get("stop_code") != fx["expected_stop_code"]:
                failures.append(f"{prefix}:stop_code_wrong:{stop.get('stop_code')}")

        if len(feedback_records) != fx["expected_unit_feedback_records"]:
            failures.append(f"{prefix}:feedback_count_wrong:{len(feedback_records)}")
        for feedback in feedback_records:
            if feedback.get("diagnostic_quality") != "USEFUL":
                failures.append(f"{prefix}:feedback_not_useful:{feedback.get('diagnostic_quality')}")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C7_SYNTHETIC_NEGATIVE_HALTS_B_C_PASS_HANDOFF_FEEDBACK_NEXT" if gate == "PASS" else "TYPED_C7_SYNTHETIC_NEGATIVE_HALTS_B_C_GATE_FAIL"

    source_hash_manifest = {rel(p): file_sha256(p) for p in required}

    basis = {
        "schema_version": "c7_negative_halts_b_c_run_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_c7_sequence_a_receipt_id": SOURCE_C7_SEQUENCE_A_RECEIPT_ID,
        "source_c7_runner_receipt_id": SOURCE_C7_RUNNER_RECEIPT_ID,
        "source_files": source_hash_manifest,
        "basis_claim": "Sequence A passed and named negative halts B/C as the next typed unit.",
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

    compact_results = []
    for result in run_results:
        rollup = result.get("rollup", {})
        stop = result.get("stop_packet", {})
        compact_results.append({
            "fixture_id": result["fixture_id"],
            "expected_outcome": result["expected_outcome"],
            "observed_outcome": result["observed_outcome"],
            "run_receipt_path": result["run_receipt_path"],
            "steps_attempted": rollup.get("steps_attempted"),
            "steps_advanced": rollup.get("steps_advanced"),
            "steps_halted": rollup.get("steps_halted"),
            "stop_code": stop.get("stop_code"),
            "untyped_halt_count": rollup.get("halts", {}).get("untyped_halt_count"),
            "bad_counters_zero": all(v == 0 for v in rollup.get("bad_counters", {}).values()) if rollup else False,
            "unit_feedback_record_count": len(result.get("feedback_records", [])),
            "diagnostic_quality_values": [f.get("diagnostic_quality") for f in result.get("feedback_records", [])],
        })

    run_results_doc = {
        "schema_version": "c7_negative_halts_b_c_run_results_v0",
        "run_status": status,
        "results": compact_results,
        "synthetic_run_only": True,
        "live_runtime_run": False,
        "runtime_adoption_authorized": False,
    }

    artifact_links = {
        "schema_version": "c7_negative_halts_b_c_run_artifact_links_v0",
        "artifact_status": "EMITTED" if gate == "PASS" else "PARTIAL",
        "sequence_a_receipt": rel(SEQUENCE_A_RECEIPT_PATH),
        "runner_receipt": rel(C7_RUNNER_RECEIPT_PATH),
        "runs": [
            {
                "fixture_id": result["fixture_id"],
                "synthetic_run_receipt": result["run_receipt_path"],
                "synthetic_step_packets": result.get("run_receipt", {}).get("output_artifacts", {}).get("step_packets"),
                "synthetic_stop_packet": result.get("run_receipt", {}).get("output_artifacts", {}).get("stop_packet"),
                "synthetic_unit_feedback_records": result.get("run_receipt", {}).get("output_artifacts", {}).get("unit_feedback_records"),
                "synthetic_rollup": result.get("run_receipt", {}).get("output_artifacts", {}).get("rollup"),
                "synthetic_readout": result.get("run_receipt", {}).get("output_artifacts", {}).get("readout"),
            }
            for result in run_results
        ],
    }

    assertion_report = {
        "schema_version": "c7_negative_halts_b_c_assertion_report_v0",
        "assertion_status": "PASS" if gate == "PASS" else "FAIL",
        "failures": failures,
        "assertions": {
            "sequence_B_outcome_schema_gap": any(r["fixture_id"] == "sequence_B_schema_gap_halt" and r["observed_outcome"] == "RADIUS_BLOCKED_BY_SCHEMA_GAP" for r in compact_results),
            "sequence_C_outcome_authority_boundary": any(r["fixture_id"] == "sequence_C_authority_boundary_halt" and r["observed_outcome"] == "RADIUS_BLOCKED_BY_AUTHORITY_BOUNDARY" for r in compact_results),
            "both_runs_gate_pass": all(r.get("bad_counters_zero") for r in compact_results) and len(compact_results) == 2,
            "no_untyped_halts": all(r.get("untyped_halt_count") == 0 for r in compact_results),
            "all_bad_counters_zero": all(r.get("bad_counters_zero") is True for r in compact_results),
            "feedback_records_useful": all("USEFUL" in r.get("diagnostic_quality_values", []) for r in compact_results),
            "synthetic_only": True,
            "live_runtime_not_run": True,
            "runtime_adoption_not_authorized": True,
        },
    }

    next_target = {
        "schema_version": "c7_handoff_and_feedback_d_e_run_target_v0",
        "target_status": "HANDOFF_AND_FEEDBACK_D_E_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "fixture_ids": [
            "sequence_D_cell1_accepted_build_handoff",
            "sequence_E_missing_capability_feedback",
        ],
        "expected_outcomes": {
            "sequence_D_cell1_accepted_build_handoff": "RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES",
            "sequence_E_missing_capability_feedback": "RADIUS_BLOCKED_BY_MISSING_CAPABILITY",
        },
        "synthetic_test_only": True,
        "does_not_authorize_live_runtime": True,
    }

    total_steps_attempted = sum((r.get("steps_attempted") or 0) for r in compact_results)
    total_steps_advanced = sum((r.get("steps_advanced") or 0) for r in compact_results)
    total_steps_halted = sum((r.get("steps_halted") or 0) for r in compact_results)
    total_feedback = sum((r.get("unit_feedback_record_count") or 0) for r in compact_results)

    rollup = {
        "schema_version": "c7_negative_halts_b_c_run_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "fixtures_run": [r["fixture_id"] for r in compact_results],
        "expected_outcomes_matched": gate == "PASS",
        "steps_attempted": total_steps_attempted,
        "steps_advanced": total_steps_advanced,
        "steps_halted": total_steps_halted,
        "unit_feedback_record_count": total_feedback,
        "untyped_halt_count": sum((r.get("untyped_halt_count") or 0) for r in compact_results),
        "bad_counters_zero": all(r.get("bad_counters_zero") is True for r in compact_results) if compact_results else False,
        "ready_for_handoff_and_feedback_d_e": gate == "PASS",
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
        "schema_version": "c7_negative_halts_b_c_run_profile_v0",
        "profile_status": status,
        "profile": "C7_SYNTHETIC_NEGATIVE_HALTS_B_C",
        "what_changed": "Synthetic schema-gap and authority-boundary halt fixtures were run and classified.",
        "what_did_not_change": [
            "handoff/feedback fixtures D/E have not run",
            "full C7 rollup has not been emitted",
            "live runtime is not authorized",
            "runtime adoption is not authorized",
            "runtime is not patched",
            "live hooks are not installed",
            "schema archive is not mutated",
            "control path authority is not granted",
        ],
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_C7_SYNTHETIC_NEGATIVE_HALTS_B_C_RUN_V0",
        "next_command_goal": None,
    }

    trace = {
        "schema_version": "c7_negative_halts_b_c_run_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "C7_SEQUENCE_A_CLEAN_CONTINUATION_PASS",
                "edge": "consume negative halt target",
                "to": "C7_NEGATIVE_HALTS_B_C_BASIS_ACCEPTED" if gate == "PASS" else "C7_NEGATIVE_HALTS_B_C_BASIS_FAIL",
            },
            {
                "from": "C7_NEGATIVE_HALTS_B_C_BASIS_ACCEPTED" if gate == "PASS" else "C7_NEGATIVE_HALTS_B_C_BASIS_FAIL",
                "edge": "run schema-gap and authority-boundary synthetic fixtures",
                "to": "C7_NEGATIVE_HALTS_B_C_PASS" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C7_NEGATIVE_HALTS_B_C_RUN_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (RUN_RESULTS_PATH, run_results_doc),
        (RUN_ARTIFACT_LINKS_PATH, artifact_links),
        (ASSERTION_REPORT_PATH, assertion_report),
        (NEXT_TARGET_PATH, next_target),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_PATH, trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "C7_SYNTHETIC_NEGATIVE_HALTS_B_C_RUN",
        "SEQUENCE_A_RECEIPT_CONSUMED",
        "RUNNER_RECEIPT_CONSUMED",
        "SEQUENCE_B_SCHEMA_GAP_HALT_MATCHED",
        "SEQUENCE_C_AUTHORITY_BOUNDARY_HALT_MATCHED",
        "UNIT_FEEDBACK_RECORDS_USEFUL",
        "BAD_COUNTERS_ZERO",
        "NO_UNTYPED_HALT",
        "HANDOFF_AND_FEEDBACK_D_E_ARE_NEXT_TYPED_UNIT",
        "NO_LIVE_RUNTIME_RUN",
        "NO_RUNTIME_ADOPTION",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_HOOK_INSTALL",
        "NO_SCHEMA_MUTATION",
        "NO_CONTROL_PATH_AUTHORITY",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt_body = {
        "schema_version": "c7_negative_halts_b_c_receipt_v0",
        "receipt_type": "TYPED_C7_SYNTHETIC_NEGATIVE_HALTS_B_C_RECEIPT",
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
        "source_c7_sequence_a_receipt_id": SOURCE_C7_SEQUENCE_A_RECEIPT_ID,
        "source_c7_runner_receipt_id": SOURCE_C7_RUNNER_RECEIPT_ID,
        "acceptance_gate_results": {
            "C7_NEG_HALTS_0_SEQUENCE_A_RECEIPT_CONSUMED": gate == "PASS",
            "C7_NEG_HALTS_1_RUNNER_RECEIPT_CONSUMED": gate == "PASS",
            "C7_NEG_HALTS_2_SEQUENCE_B_SCHEMA_GAP_MATCHED": gate == "PASS",
            "C7_NEG_HALTS_3_SEQUENCE_C_AUTHORITY_BOUNDARY_MATCHED": gate == "PASS",
            "C7_NEG_HALTS_4_FEEDBACK_RECORDS_USEFUL": gate == "PASS",
            "C7_NEG_HALTS_5_BAD_COUNTERS_ZERO": gate == "PASS",
            "C7_NEG_HALTS_6_NO_UNTYPED_HALT": gate == "PASS",
            "C7_NEG_HALTS_7_HANDOFF_FEEDBACK_NEXT": gate == "PASS",
            "C7_NEG_HALTS_8_NO_LIVE_RUNTIME_RUN": gate == "PASS",
            "C7_NEG_HALTS_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_c7_negative_halts_b_c_summary": {
            "status": status,
            "c7_negative_halts_b_c_run_done": gate == "PASS",
            "fixtures_run": rollup["fixtures_run"],
            "expected_outcomes_matched": rollup["expected_outcomes_matched"],
            "steps_attempted": rollup["steps_attempted"],
            "steps_advanced": rollup["steps_advanced"],
            "steps_halted": rollup["steps_halted"],
            "unit_feedback_record_count": rollup["unit_feedback_record_count"],
            "untyped_halt_count": rollup["untyped_halt_count"],
            "bad_counters_zero": rollup["bad_counters_zero"],
            "ready_for_handoff_and_feedback_d_e": gate == "PASS",
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
            "run_results": rel(RUN_RESULTS_PATH),
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
            "stop_code": None if gate == "PASS" else "STOP_C7_NEGATIVE_HALTS_B_C_RUN_GATE_FAIL",
        },
    }

    receipt_id = sig8(receipt_body)
    receipt_body["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_body["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_body)

    print(json.dumps(receipt_body, indent=2, sort_keys=True))
    print(f"c7_negative_halts_b_c_receipt_id={receipt_id}")
    print(f"c7_negative_halts_b_c_receipt_path={rel(receipt_path)}")
    print(f"c7_negative_halts_b_c_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
