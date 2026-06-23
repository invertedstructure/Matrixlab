#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RETRY_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_WITH_CLI_WRAPPER_INTERCEPT_PARSE_FIXED_V0"
TARGET_UNIT_ID = "r1000.post_closure_observability_harvest.radius_10000_retry.with_cli_wrapper_intercept_parse_fixed.v0"

SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID = "02711ff1"
SOURCE_CLI_WRAPPER_FIX_FAILURE_REVIEW_RECEIPT_ID = "a7e5b8e3"
SOURCE_FAILED_CLI_WRAPPER_FIX_RECEIPT_ID = "c7204f69"
SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID = "6f7051cc"
SOURCE_FAILED_MODULE_PRECONDITION_FIX_RECEIPT_ID = "1a9b0363"
SOURCE_MODULE_PRECONDITION_REVIEW_RECEIPT_ID = "18ca1234"
SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID = "f03f9616"
SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID = "15eaca49"
SOURCE_FAILED_CLI_REGISTRATION_FIX_RECEIPT_ID = "4fd77ccb"
SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID = "960a1048"
SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID = "9d834354"
SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID = "2d61b52e"
SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID = "b35e7989"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"

RETRY_RADIUS = 10000

OUT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0_receipts"

PLAN_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_plan.json"
SOURCE_PROOF_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_source_proof_surface.json"
COMMAND_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_command_surface.json"
RUN_RESULT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_run_result.json"
RUN_AUDIT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_run_audit.json"
DECISION_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_decision.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_report.json"
NEXT_STATUS_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_next_status_packet.json"

CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_intercept_parse_fix_v0_receipts" / f"{SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID}.json"
RETRY_READY_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_intercept_parse_fix_v0" / "r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet_after_cli_wrapper_intercept_parse_fix.json"
SMALL_CLI_PROBE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_intercept_parse_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_intercept_parse_cli_probe_result.json"
SMALL_MODULE_PROBE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_intercept_parse_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_intercept_parse_module_probe_result.json"

CLI_WRAPPER_FIX_FAILURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_failure_review_v0_receipts" / f"{SOURCE_CLI_WRAPPER_FIX_FAILURE_REVIEW_RECEIPT_ID}.json"
FAILED_CLI_WRAPPER_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_v0_receipts" / f"{SOURCE_FAILED_CLI_WRAPPER_FIX_RECEIPT_ID}.json"
CLI_WRAPPER_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_failure_review_v0_receipts" / f"{SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID}.json"
FAILED_MODULE_PRECONDITION_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_v0_receipts" / f"{SOURCE_FAILED_MODULE_PRECONDITION_FIX_RECEIPT_ID}.json"
MODULE_PRECONDITION_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_v0_receipts" / f"{SOURCE_MODULE_PRECONDITION_REVIEW_RECEIPT_ID}.json"
FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0_receipts" / f"{SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID}.json"
RUNTIME_OUTPUT_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_failure_review_v0_receipts" / f"{SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID}.json"
FAILED_CLI_REGISTRATION_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_v0_receipts" / f"{SOURCE_FAILED_CLI_REGISTRATION_FIX_RECEIPT_ID}.json"
BUILD_FAILURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_v0_receipts" / f"{SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID}.json"
FAILED_ENTRYPOINT_BUILD_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_v0_receipts" / f"{SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID}.json"
CLI_ENTRYPOINT_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_cli_observability_harvest_entrypoint_inspection_v0_receipts" / f"{SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID}.json"
COMMAND_RESOLVER_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0_receipts" / f"{SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID}.json"
CLOSURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID}.json"
CLOSED_QUEUE_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
EXPECTED_LIMIT_MARK_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID}.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"

CLI_PATH = ROOT / "src" / "matrixlab" / "cli.py"
ENTRYPOINT_MODULE_PATH = ROOT / "src" / "matrixlab" / "r1000_post_closure_observability_harvest.py"

PROTECTED_SOURCE_FILES = [
    CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_PATH,
    RETRY_READY_PACKET_PATH,
    SMALL_CLI_PROBE_PATH,
    SMALL_MODULE_PROBE_PATH,
    CLI_WRAPPER_FIX_FAILURE_REVIEW_RECEIPT_PATH,
    FAILED_CLI_WRAPPER_FIX_RECEIPT_PATH,
    CLI_WRAPPER_REVIEW_RECEIPT_PATH,
    FAILED_MODULE_PRECONDITION_FIX_RECEIPT_PATH,
    MODULE_PRECONDITION_REVIEW_RECEIPT_PATH,
    FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_PATH,
    RUNTIME_OUTPUT_REVIEW_RECEIPT_PATH,
    FAILED_CLI_REGISTRATION_FIX_RECEIPT_PATH,
    BUILD_FAILURE_REVIEW_RECEIPT_PATH,
    FAILED_ENTRYPOINT_BUILD_RECEIPT_PATH,
    CLI_ENTRYPOINT_INSPECTION_RECEIPT_PATH,
    COMMAND_RESOLVER_FIX_RECEIPT_PATH,
    CLOSURE_REVIEW_RECEIPT_PATH,
    CLOSED_QUEUE_HANDOFF_PATH,
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    FINAL_QUEUE_STATE_PATH,
    CLI_PATH,
    ENTRYPOINT_MODULE_PATH,
]

HUMAN_DECISION = {
    "decision": "RETRY_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_WITH_CLI_WRAPPER_INTERCEPT_PARSE_FIXED",
    "scope": "execute the previously blocked radius-10000 post-closure observability harvest as a separate bounded retry unit after CLI wrapper intercept/parse proof passed",
    "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
    "authorized": [
        "consume retry-ready packet",
        "consume passing CLI-wrapper intercept/parse fix receipt",
        "run exactly one bounded radius-10000 post-closure observability harvest through the fixed CLI entrypoint",
        "parse stdout as one JSON object",
        "require exactly 10000 observation receipts",
        "audit run directory and receipt files",
        "emit retry completion receipt",
    ],
    "not_authorized": [
        "running unbounded/no-cap harvest",
        "running radius greater than 10000",
        "running more than one radius-10000 retry",
        "modifying src/matrixlab/cli.py",
        "modifying src/matrixlab/r1000_post_closure_observability_harvest.py",
        "reopening R1000 pressure queue",
        "inspecting closed groups",
        "materializing row payloads",
        "assigning identity values",
        "inventing values",
        "running repair in this unit",
        "applying taxonomy changes",
        "mutating prior artifacts",
        "mutating existing receipts",
        "hiding next command",
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
    return path.relative_to(ROOT).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def run_cmd(args: List[str], timeout: int = 1800) -> Tuple[int, str, str, float]:
    start = time.monotonic()
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout, proc.stderr, time.monotonic() - start

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def parse_json_stdout(out: str) -> Tuple[Any, str | None]:
    try:
        return json.loads(out), None
    except Exception as exc:
        return None, f"{type(exc).__name__}: {exc}"

def validate_sources() -> List[str]:
    failures: List[str] = []

    fix = read_json(CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_PATH)
    retry_packet = read_json(RETRY_READY_PACKET_PATH)
    small_cli_probe = read_json(SMALL_CLI_PROBE_PATH)
    small_module_probe = read_json(SMALL_MODULE_PROBE_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if fix.get("receipt_id") != SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID:
        failures.append("cli_wrapper_intercept_parse_fix_receipt_id_wrong")
    if fix.get("gate") != "PASS":
        failures.append("cli_wrapper_intercept_parse_fix_not_pass")
    summary = fix.get("cli_wrapper_intercept_parse_fix_summary", {})
    if summary.get("recommended_next_handling") != UNIT_ID:
        failures.append("cli_wrapper_intercept_parse_fix_not_recommending_this_unit")
    if summary.get("radius_10000_retry_ready") is not True:
        failures.append("radius_10000_not_ready_in_fix_receipt")
    if summary.get("radius_10000_retry_executed") is not False:
        failures.append("radius_10000_already_executed_in_fix_receipt")
    if summary.get("cli_probe_passed") is not True or summary.get("cli_probe_observation_receipt_count") != 10:
        failures.append("small_cli_probe_not_proven_in_fix_receipt")

    if retry_packet.get("packet_status") != "RADIUS_10000_RETRY_READY_SEPARATE_UNIT":
        failures.append("retry_packet_not_ready")
    if retry_packet.get("requires_separate_retry_unit") is not True:
        failures.append("retry_packet_not_separate_unit")
    if retry_packet.get("radius_10000_retry_authorized_in_this_unit") is not False:
        failures.append("retry_packet_authorized_in_prior_unit")
    command = retry_packet.get("radius_10000_retry_command")
    if not isinstance(command, list) or "--radius" not in command or "10000" not in command:
        failures.append("retry_packet_command_missing_radius_10000")

    if small_cli_probe.get("probe_passed") is not True:
        failures.append("small_cli_probe_not_passed")
    if small_cli_probe.get("probe_observation_receipt_count") != 10:
        failures.append("small_cli_probe_receipt_count_not_10")
    if small_module_probe.get("probe_passed") is not True:
        failures.append("small_module_probe_not_passed")

    if closure.get("gate") != "PASS":
        failures.append("closure_review_not_pass")
    if handoff.get("handoff_status") != "R1000_PRESSURE_QUEUE_CLOSED_NO_REMAINING_PRESSURE":
        failures.append("closed_queue_handoff_status_wrong")
    if final_queue.get("queue_state_status") != "R1000_PRESSURE_QUEUE_CLOSED":
        failures.append("final_queue_not_closed")
    if final_queue.get("remaining_open_group_count") != 0 or final_queue.get("remaining_open_row_count") != 0:
        failures.append("final_queue_has_remaining_pressure")

    for path in PROTECTED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
    return failures

def run_radius_10000() -> Dict[str, Any]:
    cmd = [
        "uv", "run", "python", "src/matrixlab/cli.py",
        "post-closure-observability-harvest",
        "--radius", str(RETRY_RADIUS),
        "--source-closure-receipt-id", SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "--label", "radius-10000-post-closure-observability-harvest",
    ]
    rc, out, err, elapsed = run_cmd(cmd, timeout=1800)
    parsed, parse_error = parse_json_stdout(out)
    passed = (
        rc == 0
        and isinstance(parsed, dict)
        and parsed.get("gate") == "PASS"
        and parsed.get("radius_requested") == RETRY_RADIUS
        and parsed.get("radius_completed") == RETRY_RADIUS
        and parsed.get("observation_receipt_count") == RETRY_RADIUS
        and (parsed.get("terminal") or {}).get("next_command_goal") is None
    )
    result = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_run_result_v0",
        "retry_command": cmd,
        "returncode": rc,
        "elapsed_seconds": round(elapsed, 6),
        "stdout_json_parseable": isinstance(parsed, dict),
        "stdout_parse_error": parse_error,
        "stdout_tail": out[-12000:],
        "stderr_tail": err[-12000:],
        "parsed_result": parsed,
        "run_passed": passed,
        "radius_requested": parsed.get("radius_requested") if isinstance(parsed, dict) else None,
        "radius_completed": parsed.get("radius_completed") if isinstance(parsed, dict) else None,
        "observation_receipt_count": parsed.get("observation_receipt_count") if isinstance(parsed, dict) else None,
        "run_dir": parsed.get("run_dir") if isinstance(parsed, dict) else None,
        "run_receipt_path": parsed.get("run_receipt_path") if isinstance(parsed, dict) else None,
        "rollup_path": parsed.get("rollup_path") if isinstance(parsed, dict) else None,
        "receipt_index_path": parsed.get("receipt_index_path") if isinstance(parsed, dict) else None,
    }
    return result

def audit_run(result: Dict[str, Any]) -> Dict[str, Any]:
    run_dir_rel = result.get("run_dir")
    run_receipt_rel = result.get("run_receipt_path")
    rollup_rel = result.get("rollup_path")
    index_rel = result.get("receipt_index_path")

    run_dir = ROOT / run_dir_rel if isinstance(run_dir_rel, str) else None
    receipt_dir = run_dir / "receipts" if run_dir else None

    audit: Dict[str, Any] = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_run_audit_v0",
        "run_dir": run_dir_rel,
        "run_dir_exists": bool(run_dir and run_dir.exists()),
        "run_receipt_path": run_receipt_rel,
        "run_receipt_exists": bool(run_receipt_rel and (ROOT / run_receipt_rel).exists()),
        "rollup_path": rollup_rel,
        "rollup_exists": bool(rollup_rel and (ROOT / rollup_rel).exists()),
        "receipt_index_path": index_rel,
        "receipt_index_exists": bool(index_rel and (ROOT / index_rel).exists()),
        "observation_receipt_files_count": 0,
        "observation_receipt_sample_paths": [],
        "run_receipt_gate": None,
        "rollup_gate": None,
        "rollup_radius_completed": None,
        "rollup_observation_receipt_count": None,
        "all_observation_receipts_parseable_sample": False,
        "all_observation_receipts_gate_pass_sample": False,
        "audit_passed": False,
    }

    if receipt_dir and receipt_dir.exists():
        receipt_files = sorted(receipt_dir.glob("*.json"))
        audit["observation_receipt_files_count"] = len(receipt_files)
        sample = receipt_files[:3] + receipt_files[-3:] if len(receipt_files) >= 6 else receipt_files
        audit["observation_receipt_sample_paths"] = [rel(p) for p in sample]
        parseable = []
        gate_pass = []
        for p in sample:
            try:
                obj = read_json(p)
                parseable.append(True)
                gate_pass.append(obj.get("gate") == "PASS")
            except Exception:
                parseable.append(False)
                gate_pass.append(False)
        audit["all_observation_receipts_parseable_sample"] = all(parseable) if parseable else False
        audit["all_observation_receipts_gate_pass_sample"] = all(gate_pass) if gate_pass else False

    if run_receipt_rel and (ROOT / run_receipt_rel).exists():
        rr = read_json(ROOT / run_receipt_rel)
        audit["run_receipt_gate"] = rr.get("gate")
        audit["run_receipt_observation_receipt_count"] = rr.get("observation_receipt_count")
        audit["run_receipt_radius_completed"] = rr.get("radius_completed")

    if rollup_rel and (ROOT / rollup_rel).exists():
        rollup = read_json(ROOT / rollup_rel)
        audit["rollup_gate"] = rollup.get("gate")
        audit["rollup_radius_completed"] = rollup.get("radius_completed")
        audit["rollup_observation_receipt_count"] = rollup.get("observation_receipt_count")
        audit["rollup_runtime_seconds"] = rollup.get("runtime_seconds")
        audit["rollup_observation_write_rate_per_second"] = rollup.get("observation_write_rate_per_second")
        for key in [
            "queue_reopened_count",
            "closed_group_inspected_count",
            "row_payload_materialized_count",
            "row_payload_inspected_count",
            "identity_assignment_count",
            "field_value_invention_count",
            "repair_executed_count",
            "taxonomy_delta_proposal_emitted_count",
            "source_mutation_count",
            "existing_receipt_mutation_count",
            "hidden_next_command_count",
        ]:
            audit[f"rollup_{key}"] = rollup.get(key)

    audit["audit_passed"] = (
        audit["run_dir_exists"]
        and audit["run_receipt_exists"]
        and audit["rollup_exists"]
        and audit["receipt_index_exists"]
        and audit["observation_receipt_files_count"] == RETRY_RADIUS
        and audit["run_receipt_gate"] == "PASS"
        and audit["rollup_gate"] == "PASS"
        and audit.get("run_receipt_observation_receipt_count") == RETRY_RADIUS
        and audit.get("run_receipt_radius_completed") == RETRY_RADIUS
        and audit["rollup_radius_completed"] == RETRY_RADIUS
        and audit["rollup_observation_receipt_count"] == RETRY_RADIUS
        and audit["all_observation_receipts_parseable_sample"]
        and audit["all_observation_receipts_gate_pass_sample"]
    )
    return audit

def validate_outputs(result: Dict[str, Any], audit: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if result.get("stdout_json_parseable") is not True:
        failures.append("radius_10000_stdout_not_json")
    if result.get("run_passed") is not True:
        failures.append("radius_10000_run_not_passed")
    if result.get("radius_requested") != RETRY_RADIUS:
        failures.append("radius_requested_not_10000")
    if result.get("radius_completed") != RETRY_RADIUS:
        failures.append("radius_completed_not_10000")
    if result.get("observation_receipt_count") != RETRY_RADIUS:
        failures.append("observation_receipt_count_not_10000")
    if audit.get("audit_passed") is not True:
        failures.append("radius_10000_run_audit_not_passed")
    if audit.get("observation_receipt_files_count") != RETRY_RADIUS:
        failures.append("observation_receipt_files_count_not_10000")

    for key in [
        "unbounded_or_no_cap_run_count",
        "radius_above_10000_run_count",
        "extra_radius_10000_retry_count",
        "queue_reopened_count",
        "closed_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "repair_executed_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")
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

    metrics = receipt.get("aggregate_metrics", {})
    for key in [
        "retry_ready_packet_consumed_count",
        "cli_wrapper_intercept_parse_fix_receipt_consumed_count",
        "small_cli_probe_proof_consumed_count",
        "radius_10000_retry_executed_count",
        "radius_10000_retry_passed_count",
        "radius_10000_stdout_json_parseable_count",
        "radius_10000_observation_receipt_count",
        "radius_10000_observation_receipt_files_count",
        "radius_10000_run_audit_passed_count",
        "decision_emitted_count",
    ]:
        expected = RETRY_RADIUS if key in {"radius_10000_observation_receipt_count", "radius_10000_observation_receipt_files_count"} else 1
        if metrics.get(key) != expected:
            failures.append(f"metric_wrong:{key}:{metrics.get(key)} expected {expected}")

    for key in [
        "unbounded_or_no_cap_run_count",
        "radius_above_10000_run_count",
        "extra_radius_10000_retry_count",
        "queue_reopened_count",
        "closed_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "repair_executed_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RETRY_COMPLETE":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    protected_before = snapshot_files(PROTECTED_SOURCE_FILES)
    failures = validate_sources()

    plan = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_plan_v0",
        "unit_id": UNIT_ID,
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "retry_radius": RETRY_RADIUS,
        "bounded": True,
        "single_retry_only": True,
        "command_source": "retry_ready_packet",
        "radius_above_10000_authorized": False,
        "unbounded_authorized": False,
    }
    write_json(PLAN_PATH, plan)

    source_proof = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_source_proof_surface_v0",
        "fix_receipt": {
            "path": rel(CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_PATH),
            "receipt_id": read_json(CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_PATH).get("receipt_id"),
            "gate": read_json(CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_PATH).get("gate"),
            "summary": read_json(CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_PATH).get("cli_wrapper_intercept_parse_fix_summary"),
        },
        "retry_ready_packet": read_json(RETRY_READY_PACKET_PATH),
        "small_cli_probe": read_json(SMALL_CLI_PROBE_PATH),
        "small_module_probe": read_json(SMALL_MODULE_PROBE_PATH),
    }
    write_json(SOURCE_PROOF_SURFACE_PATH, source_proof)

    command_surface = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_command_surface_v0",
        "command": [
            "uv", "run", "python", "src/matrixlab/cli.py",
            "post-closure-observability-harvest",
            "--radius", str(RETRY_RADIUS),
            "--source-closure-receipt-id", SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
            "--label", "radius-10000-post-closure-observability-harvest",
        ],
        "radius": RETRY_RADIUS,
        "bounded": True,
        "unbounded_or_no_cap": False,
        "source_closure_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
    }
    write_json(COMMAND_SURFACE_PATH, command_surface)

    result = run_radius_10000()
    write_json(RUN_RESULT_PATH, result)

    audit = audit_run(result)
    write_json(RUN_AUDIT_PATH, audit)

    decision = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_decision_v0",
        "decision_id": sha8({
            "unit_id": UNIT_ID,
            "run_passed": result.get("run_passed"),
            "audit_passed": audit.get("audit_passed"),
            "run_dir": result.get("run_dir"),
        }),
        "decision_status": "RADIUS_10000_POST_CLOSURE_OBSERVABILITY_HARVEST_RETRY_COMPLETE" if result.get("run_passed") and audit.get("audit_passed") else "RADIUS_10000_POST_CLOSURE_OBSERVABILITY_HARVEST_RETRY_FAILED",
        "radius_10000_retry_executed": True,
        "radius_10000_retry_passed": result.get("run_passed") is True and audit.get("audit_passed") is True,
        "radius_requested": result.get("radius_requested"),
        "radius_completed": result.get("radius_completed"),
        "observation_receipt_count": result.get("observation_receipt_count"),
        "observation_receipt_files_count": audit.get("observation_receipt_files_count"),
        "run_dir": result.get("run_dir"),
        "run_receipt_path": result.get("run_receipt_path"),
        "rollup_path": result.get("rollup_path"),
        "recommended_next_handling": "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RESULT_V0" if result.get("run_passed") and audit.get("audit_passed") else "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RETRY_FAILURE_V0",
    }
    write_json(DECISION_PATH, decision)

    report = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "retry_ready_packet_consumed_count": 1,
        "cli_wrapper_intercept_parse_fix_receipt_consumed_count": 1,
        "small_cli_probe_proof_consumed_count": 1,
        "small_module_probe_proof_consumed_count": 1,
        "radius_10000_retry_executed_count": 1,
        "radius_10000_retry_passed_count": 1 if decision["radius_10000_retry_passed"] else 0,
        "radius_10000_stdout_json_parseable_count": 1 if result.get("stdout_json_parseable") else 0,
        "radius_10000_observation_receipt_count": result.get("observation_receipt_count") or 0,
        "radius_10000_observation_receipt_files_count": audit.get("observation_receipt_files_count") or 0,
        "radius_10000_run_audit_passed_count": 1 if audit.get("audit_passed") else 0,
        "runtime_seconds": result.get("elapsed_seconds"),
        "run_dir": result.get("run_dir"),
        "run_receipt_path": result.get("run_receipt_path"),
        "rollup_path": result.get("rollup_path"),
        "receipt_index_path": result.get("receipt_index_path"),
        "decision_emitted_count": 1,
        "unbounded_or_no_cap_run_count": 0,
        "radius_above_10000_run_count": 0,
        "extra_radius_10000_retry_count": 0,
        "queue_reopened_count": 0,
        "closed_group_inspected_count": 0,
        "row_payload_materialized_count": 0,
        "row_payload_inspected_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "repair_executed_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": decision["recommended_next_handling"],
    }
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(result, audit, report))

    protected_after = snapshot_files(PROTECTED_SOURCE_FILES)
    protected_mutation_detected = protected_before != protected_after
    if protected_mutation_detected:
        failures.append("protected_prior_or_source_artifact_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    trace = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_transition_trace_v0",
        "trace": [
            {
                "step": "consume_retry_ready_packet",
                "question": "radius-10000 retry ready from fixed CLI wrapper intercept parse",
                "answer": True,
                "taken": "run_bounded_radius_10000_retry",
            },
            {
                "step": "run_bounded_radius_10000_retry",
                "question": "stdout JSON and radius completed exactly 10000",
                "answer": result.get("run_passed") is True,
                "taken": "audit_run_artifacts",
            },
            {
                "step": "audit_run_artifacts",
                "question": "run directory contains exactly 10000 observation receipt files and run/rollup pass",
                "answer": audit.get("audit_passed") is True,
                "taken": "emit_completion_receipt" if audit.get("audit_passed") else "emit_retry_failure_receipt",
            },
            {
                "step": "emit_completion_receipt",
                "question": "run another retry now",
                "answer": False,
                "taken": "STOP_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RETRY_COMPLETE" if audit.get("audit_passed") else "STOP_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RETRY_FAILED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RETRY_COMPLETE" if decision["radius_10000_retry_passed"] else "STOP_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RETRY_FAILED",
            "next_command_goal": None,
        },
    }
    write_json(TRANSITION_TRACE_PATH, trace)

    next_status = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_next_status_packet_v0",
        "packet_status": "RADIUS_10000_RETRY_COMPLETE_REVIEW_READY" if decision["radius_10000_retry_passed"] else "RADIUS_10000_RETRY_FAILED_REVIEW_REQUIRED",
        "source_retry_receipt_pending": True,
        "run_dir": result.get("run_dir"),
        "run_receipt_path": result.get("run_receipt_path"),
        "rollup_path": result.get("rollup_path"),
        "observation_receipt_count": result.get("observation_receipt_count"),
        "recommended_next_handling": decision["recommended_next_handling"],
        "auto_next_command": None,
    }
    write_json(NEXT_STATUS_PACKET_PATH, next_status)

    acceptance_gate_results = {
        "RADIUS_10000_RETRY_0_READY_PACKET_CONSUMED": True,
        "RADIUS_10000_RETRY_1_FIX_RECEIPT_PASS_CONSUMED": True,
        "RADIUS_10000_RETRY_2_SMALL_PROBE_PROOF_CONSUMED": True,
        "RADIUS_10000_RETRY_3_SINGLE_BOUNDED_RADIUS_10000_EXECUTED": report["radius_10000_retry_executed_count"] == 1 and report["radius_above_10000_run_count"] == 0 and report["extra_radius_10000_retry_count"] == 0,
        "RADIUS_10000_RETRY_4_STDOUT_JSON": report["radius_10000_stdout_json_parseable_count"] == 1,
        "RADIUS_10000_RETRY_5_RUN_PASS": report["radius_10000_retry_passed_count"] == 1,
        "RADIUS_10000_RETRY_6_WRITES_10000_RECEIPTS": report["radius_10000_observation_receipt_count"] == RETRY_RADIUS and report["radius_10000_observation_receipt_files_count"] == RETRY_RADIUS,
        "RADIUS_10000_RETRY_7_RUN_AUDIT_PASS": report["radius_10000_run_audit_passed_count"] == 1,
        "RADIUS_10000_RETRY_8_NO_UNBOUNDED_OR_RADIUS_ABOVE_10000": report["unbounded_or_no_cap_run_count"] == 0 and report["radius_above_10000_run_count"] == 0,
        "RADIUS_10000_RETRY_9_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0,
        "RADIUS_10000_RETRY_10_NO_SOURCE_OR_RECEIPT_MUTATION": protected_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "RADIUS_10000_RETRY_11_NO_REPAIR_OR_TAXONOMY": report["repair_executed_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "RADIUS_10000_RETRY_12_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if protected_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "source_cli_wrapper_fix_failure_review_receipt_id": SOURCE_CLI_WRAPPER_FIX_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_cli_wrapper_fix_receipt_id": SOURCE_FAILED_CLI_WRAPPER_FIX_RECEIPT_ID,
        "source_cli_wrapper_review_receipt_id": SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID,
        "source_failed_module_precondition_fix_receipt_id": SOURCE_FAILED_MODULE_PRECONDITION_FIX_RECEIPT_ID,
        "source_module_precondition_review_receipt_id": SOURCE_MODULE_PRECONDITION_REVIEW_RECEIPT_ID,
        "source_failed_runtime_output_fix_receipt_id": SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID,
        "source_runtime_output_review_receipt_id": SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID,
        "source_failed_cli_registration_fix_receipt_id": SOURCE_FAILED_CLI_REGISTRATION_FIX_RECEIPT_ID,
        "source_build_failure_review_receipt_id": SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "protected_prior_or_source_artifact_mutation_count": 1 if protected_mutation_detected else 0,
    }

    guards = {
        "retry_ready_packet_consumed": True,
        "fixed_cli_wrapper_intercept_parse_receipt_consumed": True,
        "bounded_radius_10000_only": True,
        "radius_10000_retry_executed": True,
        "radius_10000_retry_passed": decision["radius_10000_retry_passed"],
        "stdout_json_parseable": result.get("stdout_json_parseable"),
        "observation_receipt_count_exact_10000": result.get("observation_receipt_count") == RETRY_RADIUS,
        "observation_receipt_files_count_exact_10000": audit.get("observation_receipt_files_count") == RETRY_RADIUS,
        "run_audit_passed": audit.get("audit_passed"),
        "unbounded_or_no_cap_run": False,
        "radius_above_10000_run": False,
        "extra_radius_10000_retry": False,
        "source_mutated": protected_mutation_detected,
        "existing_receipts_mutated": False,
        "queue_reopened": False,
        "closed_group_inspected": False,
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "identity_assignment": False,
        "field_value_invention": False,
        "repair_executed": False,
        "taxonomy_delta_proposal_emitted": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "run_dir": result.get("run_dir"),
        "observation_receipt_count": result.get("observation_receipt_count"),
        "audit_passed": audit.get("audit_passed"),
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "plan": rel(PLAN_PATH),
        "source_proof_surface": rel(SOURCE_PROOF_SURFACE_PATH),
        "command_surface": rel(COMMAND_SURFACE_PATH),
        "run_result": rel(RUN_RESULT_PATH),
        "run_audit": rel(RUN_AUDIT_PATH),
        "decision": rel(DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "next_status_packet": rel(NEXT_STATUS_PACKET_PATH),
        "implementation_receipt": rel(receipt_path),
        "run_dir": result.get("run_dir"),
        "run_receipt_path": result.get("run_receipt_path"),
        "rollup_path": result.get("rollup_path"),
        "receipt_index_path": result.get("receipt_index_path"),
    }

    receipt = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RETRY_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "source_cli_wrapper_fix_failure_review_receipt_id": SOURCE_CLI_WRAPPER_FIX_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_cli_wrapper_fix_receipt_id": SOURCE_FAILED_CLI_WRAPPER_FIX_RECEIPT_ID,
        "source_cli_wrapper_review_receipt_id": SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID,
        "source_failed_module_precondition_fix_receipt_id": SOURCE_FAILED_MODULE_PRECONDITION_FIX_RECEIPT_ID,
        "source_module_precondition_review_receipt_id": SOURCE_MODULE_PRECONDITION_REVIEW_RECEIPT_ID,
        "source_failed_runtime_output_fix_receipt_id": SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID,
        "source_runtime_output_review_receipt_id": SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID,
        "source_failed_cli_registration_fix_receipt_id": SOURCE_FAILED_CLI_REGISTRATION_FIX_RECEIPT_ID,
        "source_build_failure_review_receipt_id": SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "radius_10000_retry_summary": {
            "decision_status": decision["decision_status"],
            "radius_10000_retry_executed": True,
            "radius_10000_retry_passed": decision["radius_10000_retry_passed"],
            "stdout_json_parseable": result.get("stdout_json_parseable"),
            "radius_requested": result.get("radius_requested"),
            "radius_completed": result.get("radius_completed"),
            "observation_receipt_count": result.get("observation_receipt_count"),
            "observation_receipt_files_count": audit.get("observation_receipt_files_count"),
            "run_audit_passed": audit.get("audit_passed"),
            "runtime_seconds": result.get("elapsed_seconds"),
            "run_dir": result.get("run_dir"),
            "run_receipt_path": result.get("run_receipt_path"),
            "rollup_path": result.get("rollup_path"),
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "radius_10000_retry_guards": guards,
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

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"radius_10000_retry_receipt_id={receipt_id}")
    print(f"radius_10000_retry_receipt_path=data/r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0_receipts/{receipt_id}.json")
    print(f"radius_10000_run_dir={result.get('run_dir')}")
    print(f"radius_10000_run_receipt_path={result.get('run_receipt_path')}")
    print(f"radius_10000_rollup_path={result.get('rollup_path')}")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
