#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_RUNTIME_OUTPUT_FIX_FAILURE_V0"
TARGET_UNIT_ID = "r1000.post_closure_observability_harvest_entrypoint.runtime_output_fix_failure.review.v0"

SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID = "f03f9616"
SOURCE_RUNTIME_OUTPUT_REVIEW_RECEIPT_ID = "15eaca49"
SOURCE_FAILED_CLI_REGISTRATION_FIX_RECEIPT_ID = "4fd77ccb"
SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID = "960a1048"
SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID = "9d834354"
SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID = "2d61b52e"
SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID = "b35e7989"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"

OUT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_v0_receipts"

FAILURE_REVIEW_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_surface.json"
HELP_SUCCESS_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_help_success_surface.json"
MODULE_PROBE_FAILURE_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_module_probe_surface.json"
CLI_PROBE_FAILURE_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_cli_probe_surface.json"
FAILURE_CLASSIFICATION_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_classification_packet.json"
FIX_AUTHORITY_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_fix_authority_packet.json"
REVIEW_DECISION_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_decision.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_report.json"

FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0_receipts" / f"{SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID}.json"
PATCH_PLAN_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_patch_plan.json"
PRIOR_FAILURE_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_prior_failure_surface.json"
MODULE_BEFORE_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_module_before_surface.json"
MODULE_AFTER_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_module_after_surface.json"
CLI_BEFORE_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_cli_before_surface.json"
CLI_AFTER_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_cli_after_surface.json"
PATCH_REPORT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_patch_report.json"
HELP_CHECK_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_help_check.json"
SMALL_PROBE_RESULT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_small_probe_result.json"
RETRY_READY_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0" / "r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet_after_runtime_output_fix.json"
FIX_DECISION_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_decision.json"
FIX_TRACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_transition_trace.json"
FIX_REPORT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_report.json"

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

SOURCE_FILES = [
    FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_PATH,
    PATCH_PLAN_PATH,
    PRIOR_FAILURE_SURFACE_PATH,
    MODULE_BEFORE_SURFACE_PATH,
    MODULE_AFTER_SURFACE_PATH,
    CLI_BEFORE_SURFACE_PATH,
    CLI_AFTER_SURFACE_PATH,
    PATCH_REPORT_PATH,
    HELP_CHECK_PATH,
    SMALL_PROBE_RESULT_PATH,
    RETRY_READY_PACKET_PATH,
    FIX_DECISION_PATH,
    FIX_TRACE_PATH,
    FIX_REPORT_PATH,
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
    "decision": "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_RUNTIME_OUTPUT_FIX_FAILURE",
    "scope": "review failed runtime-output fix without repairing it; classify why module and CLI probes still failed, preserve failed artifacts, and emit a typed fix authority packet for a separate module-precondition/runtime repair unit",
    "source_failed_runtime_output_fix_receipt_id": SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID,
    "authorized": [
        "consume failed runtime-output fix receipt",
        "consume failed runtime-output fix artifacts",
        "inspect help success surface",
        "inspect module probe failure surface",
        "inspect CLI probe failure surface",
        "classify remaining module/runtime failure",
        "emit fix authority packet for separate repair",
        "preserve failed artifacts",
        "stop before repair or retry",
    ],
    "not_authorized": [
        "modifying src/matrixlab/cli.py",
        "modifying src/matrixlab/r1000_post_closure_observability_harvest.py",
        "running radius-10000 harvest",
        "running unbounded/no-cap harvest",
        "running another small probe",
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

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def run_cmd(args: List[str], timeout: int = 120) -> Tuple[int, str, str]:
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
    )
    return proc.returncode, proc.stdout, proc.stderr

def validate_sources() -> List[str]:
    failures: List[str] = []
    failed = read_json(FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_PATH)
    report = read_json(FIX_REPORT_PATH)
    decision = read_json(FIX_DECISION_PATH)
    retry_packet = read_json(RETRY_READY_PACKET_PATH)
    help_check = read_json(HELP_CHECK_PATH)
    probe_bundle = read_json(SMALL_PROBE_RESULT_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if failed.get("receipt_id") != SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID:
        failures.append("failed_runtime_output_fix_receipt_id_wrong")
    if failed.get("gate") != "FAIL":
        failures.append("failed_runtime_output_fix_gate_not_fail")
    if failed.get("runtime_output_fix_summary", {}).get("decision_status") != "RUNTIME_OUTPUT_FIX_INCOMPLETE_SMALL_PROBE_FAILED":
        failures.append("failed_runtime_output_fix_decision_status_wrong")
    if failed.get("runtime_output_fix_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("failed_runtime_output_fix_not_recommending_this_unit")

    if report.get("entrypoint_help_passed_count") != 1:
        failures.append("help_did_not_pass_in_failed_fix")
    if report.get("module_probe_passed_count") != 0:
        failures.append("module_probe_unexpectedly_passed")
    if report.get("cli_probe_passed_count") != 0:
        failures.append("cli_probe_unexpectedly_passed")
    if report.get("cli_probe_stdout_json_parseable_count") != 0:
        failures.append("cli_probe_stdout_unexpectedly_json")
    if report.get("radius_10000_retry_ready_count") != 0:
        failures.append("retry_unexpectedly_ready")
    if report.get("radius_10000_retry_executed_count") != 0:
        failures.append("radius_10000_executed_unexpectedly")

    if decision.get("decision_status") != "RUNTIME_OUTPUT_FIX_INCOMPLETE_SMALL_PROBE_FAILED":
        failures.append("fix_decision_status_wrong")
    if retry_packet.get("packet_status") != "RADIUS_10000_RETRY_BLOCKED_RUNTIME_OUTPUT_FIX_PROBE_FAILED":
        failures.append("retry_packet_status_wrong")
    if help_check.get("entrypoint_help_passed") is not True:
        failures.append("help_check_entrypoint_help_not_passed")

    module_probe = probe_bundle.get("module_probe") or {}
    cli_probe = probe_bundle.get("cli_probe") or {}
    if module_probe.get("probe_passed") is not False:
        failures.append("module_probe_not_failed")
    if cli_probe.get("probe_passed") is not False:
        failures.append("cli_probe_not_failed")

    if closure.get("gate") != "PASS":
        failures.append("closure_review_not_pass")
    if handoff.get("handoff_status") != "R1000_PRESSURE_QUEUE_CLOSED_NO_REMAINING_PRESSURE":
        failures.append("closed_queue_handoff_status_wrong")
    if final_queue.get("queue_state_status") != "R1000_PRESSURE_QUEUE_CLOSED":
        failures.append("final_queue_not_closed")
    if final_queue.get("remaining_open_group_count") != 0 or final_queue.get("remaining_open_row_count") != 0:
        failures.append("final_queue_has_remaining_pressure")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")

    return failures

def current_help_surface() -> Dict[str, Any]:
    cmds = [
        ["uv", "run", "python", "src/matrixlab/cli.py", "post-closure-observability-harvest", "--help"],
        ["uv", "run", "python", "src/matrixlab/cli.py", "--help"],
    ]
    rows = []
    for cmd in cmds:
        rc, out, err = run_cmd(cmd)
        rows.append({
            "command": cmd,
            "returncode": rc,
            "stdout_tail": out[-8000:],
            "stderr_tail": err[-4000:],
            "contains_radius": "--radius" in out or "--radius" in err,
            "mentions_entrypoint": "post-closure-observability-harvest" in out or "post-closure-observability-harvest" in err,
        })
    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_help_success_surface_v0",
        "rows": rows,
        "help_success_confirmed": any(r["returncode"] == 0 and r["contains_radius"] for r in rows),
    }

def _noise_markers(stdout_tail: str, stderr_tail: str) -> List[str]:
    markers = []
    for marker in [
        "Traceback",
        "ModuleNotFoundError",
        "ImportError",
        "NameError",
        "TypeError",
        "KeyError",
        "FileNotFoundError",
        "STOP_CLOSED_QUEUE_PRECONDITION_FAIL",
        "closure_summary_queue_not_closed",
        "closed_handoff_status_wrong",
        "Usage:",
        "Error:",
        "Gate checks",
        "GATE_PASS",
        "╭",
        "┌",
        "Ôö",
        "WARNING",
        "warning",
    ]:
        if marker in stdout_tail or marker in stderr_tail:
            markers.append(marker)
    return markers

def probe_failure_surfaces() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    bundle = read_json(SMALL_PROBE_RESULT_PATH)
    module_probe = bundle.get("module_probe") or {}
    cli_probe = bundle.get("cli_probe") or {}

    module_stdout = module_probe.get("stdout_tail") or ""
    module_stderr = module_probe.get("stderr_tail") or ""
    cli_stdout = cli_probe.get("stdout_tail") or ""
    cli_stderr = cli_probe.get("stderr_tail") or ""

    module_surface = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_module_probe_surface_v0",
        "source_small_probe_result_ref": rel(SMALL_PROBE_RESULT_PATH),
        "probe_command": module_probe.get("probe_command"),
        "returncode": module_probe.get("returncode"),
        "stdout_json_parseable": module_probe.get("stdout_json_parseable"),
        "stdout_parse_error": module_probe.get("stdout_parse_error"),
        "stdout_tail": module_stdout[-12000:],
        "stderr_tail": module_stderr[-12000:],
        "likely_failure_markers": _noise_markers(module_stdout, module_stderr),
        "parsed_result": module_probe.get("parsed_result"),
        "probe_passed": module_probe.get("probe_passed"),
        "probe_observation_receipt_count": module_probe.get("probe_observation_receipt_count"),
        "probe_run_receipt_path": module_probe.get("probe_run_receipt_path"),
        "probe_run_dir": module_probe.get("probe_run_dir"),
    }

    cli_surface = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_cli_probe_surface_v0",
        "source_small_probe_result_ref": rel(SMALL_PROBE_RESULT_PATH),
        "probe_command": cli_probe.get("probe_command"),
        "returncode": cli_probe.get("returncode"),
        "stdout_json_parseable": cli_probe.get("stdout_json_parseable"),
        "stdout_parse_error": cli_probe.get("stdout_parse_error"),
        "stdout_tail": cli_stdout[-12000:],
        "stderr_tail": cli_stderr[-12000:],
        "likely_failure_markers": _noise_markers(cli_stdout, cli_stderr),
        "parsed_result": cli_probe.get("parsed_result"),
        "probe_passed": cli_probe.get("probe_passed"),
        "probe_observation_receipt_count": cli_probe.get("probe_observation_receipt_count"),
        "probe_run_receipt_path": cli_probe.get("probe_run_receipt_path"),
        "probe_rollup_path": cli_probe.get("probe_rollup_path"),
        "probe_run_dir": cli_probe.get("probe_run_dir"),
    }

    return module_surface, cli_surface

def classify_failure(help_obj: Dict[str, Any], module_surface: Dict[str, Any], cli_surface: Dict[str, Any]) -> Dict[str, Any]:
    help_ok = help_obj.get("help_success_confirmed") is True
    module_return = module_surface.get("returncode")
    cli_return = cli_surface.get("returncode")
    module_json = module_surface.get("stdout_json_parseable") is True
    cli_json = cli_surface.get("stdout_json_parseable") is True
    module_count = module_surface.get("probe_observation_receipt_count") or 0
    cli_count = cli_surface.get("probe_observation_receipt_count") or 0

    combined = " ".join(
        [
            str(module_surface.get("stdout_tail") or ""),
            str(module_surface.get("stderr_tail") or ""),
            str(cli_surface.get("stdout_tail") or ""),
            str(cli_surface.get("stderr_tail") or ""),
        ]
    )

    if "STOP_CLOSED_QUEUE_PRECONDITION_FAIL" in combined or "closed_queue" in combined or "closure_summary_queue_not_closed" in combined:
        classification = "MODULE_RUNTIME_CLOSED_QUEUE_PRECONDITION_OR_SCHEMA_VALIDATION_FAILURE"
    elif "Traceback" in combined or module_return not in (0, None) or cli_return not in (0, None):
        classification = "MODULE_RUNTIME_EXCEPTION_BEFORE_JSON_RESULT"
    elif help_ok and not module_json and not cli_json and module_count == 0 and cli_count == 0:
        classification = "MODULE_RUNTIME_OUTPUT_STILL_NOT_JSON_AND_RECEIPT_WRITE_NOT_PROVEN"
    else:
        classification = "RUNTIME_OUTPUT_FIX_FAILURE_REQUIRES_MANUAL_REVIEW"

    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_classification_packet_v0",
        "classification": classification,
        "source_failed_runtime_output_fix_receipt_id": SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID,
        "evidence": {
            "help_success_confirmed": help_ok,
            "module_probe_returncode": module_return,
            "module_probe_stdout_json_parseable": module_json,
            "module_probe_passed": module_surface.get("probe_passed"),
            "module_probe_observation_receipt_count": module_count,
            "module_likely_failure_markers": module_surface.get("likely_failure_markers"),
            "cli_probe_returncode": cli_return,
            "cli_probe_stdout_json_parseable": cli_json,
            "cli_probe_passed": cli_surface.get("probe_passed"),
            "cli_probe_observation_receipt_count": cli_count,
            "cli_likely_failure_markers": cli_surface.get("likely_failure_markers"),
        },
        "not_a_missing_entrypoint_failure": True,
        "not_a_help_routing_failure": help_ok,
        "module_probe_failed": module_surface.get("probe_passed") is False,
        "cli_probe_failed": cli_surface.get("probe_passed") is False,
        "not_a_radius_10000_failure": True,
        "radius_10000_retry_still_blocked": True,
    }

def build_fix_authority_packet(classification: Dict[str, Any]) -> Dict[str, Any]:
    if classification["classification"] == "MODULE_RUNTIME_CLOSED_QUEUE_PRECONDITION_OR_SCHEMA_VALIDATION_FAILURE":
        next_unit = "FIX_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_CLOSED_QUEUE_VALIDATION_V0"
        required_shape = [
            "inspect actual closure receipt schema 52d0ea8d and closed handoff/final queue artifacts",
            "make run_bounded_harvest closed-queue validation schema-tolerant and source-backed",
            "return JSON failure payloads instead of raising before JSON output",
            "require module probe pass before CLI probe",
            "require CLI radius-10 probe writes exactly 10 observation receipts",
            "emit radius-10000 retry-ready packet only after probe pass",
        ]
    else:
        next_unit = "FIX_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_MODULE_RUNTIME_PRECONDITION_V0"
        required_shape = [
            "inspect actual module probe stdout/stderr",
            "remove exception path or precondition failure causing no JSON result",
            "ensure run_bounded_harvest returns exactly one JSON-serializable result",
            "require module probe pass before CLI probe",
            "require CLI radius-10 probe writes exactly 10 observation receipts",
            "emit radius-10000 retry-ready packet only after probe pass",
        ]

    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_fix_authority_packet_v0",
        "packet_status": "FIX_ENTRYPOINT_MODULE_RUNTIME_PRECONDITION_AUTHORITY_PACKET",
        "source_failed_runtime_output_fix_receipt_id": SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID,
        "failure_classification": classification["classification"],
        "authorized_next_unit": next_unit,
        "required_fix_shape": required_shape,
        "radius_10000_retry_authorized_now": False,
        "fix_authorized_in_this_unit": False,
        "recommended_next_handling": next_unit,
    }

def build_decision(classification: Dict[str, Any], authority: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_decision_v0",
        "decision_id": sha8({
            "source_failed_runtime_output_fix_receipt_id": SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID,
            "classification": classification["classification"],
            "next": authority["recommended_next_handling"],
        }),
        "decision_status": "ACCEPT_RUNTIME_OUTPUT_FIX_FAILURE_AS_MODULE_RUNTIME_PRECONDITION_REPAIR_REQUIRED",
        "failure_classification": classification["classification"],
        "help_routing_fixed": classification["evidence"]["help_success_confirmed"],
        "module_probe_failed": classification["module_probe_failed"],
        "cli_probe_failed": classification["cli_probe_failed"],
        "runtime_or_precondition_failure": True,
        "radius_10000_retry_authorized": False,
        "repair_authorized_in_this_unit": False,
        "recommended_next_handling": authority["recommended_next_handling"],
    }

def build_report(classification: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_runtime_output_fix_receipt_id": SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID,
        "failed_runtime_output_fix_receipt_consumed_count": 1,
        "failed_runtime_output_fix_artifacts_consumed_count": 1,
        "help_success_surface_emitted_count": 1,
        "module_probe_failure_surface_emitted_count": 1,
        "cli_probe_failure_surface_emitted_count": 1,
        "failure_classification_packet_emitted_count": 1,
        "fix_authority_packet_emitted_count": 1,
        "review_decision_emitted_count": 1,
        "failed_fix_artifacts_preserved_count": 1,
        "help_routing_fixed_count": 1 if classification["evidence"]["help_success_confirmed"] else 0,
        "module_probe_failed_count": 1 if classification["module_probe_failed"] else 0,
        "cli_probe_failed_count": 1 if classification["cli_probe_failed"] else 0,
        "module_probe_stdout_not_json_count": 1 if not classification["evidence"]["module_probe_stdout_json_parseable"] else 0,
        "cli_probe_stdout_not_json_count": 1 if not classification["evidence"]["cli_probe_stdout_json_parseable"] else 0,
        "receipt_write_not_proven_count": 1 if (classification["evidence"]["module_probe_observation_receipt_count"] or 0) == 0 and (classification["evidence"]["cli_probe_observation_receipt_count"] or 0) == 0 else 0,
        "radius_10000_retry_ready_count": 0,
        "radius_10000_retry_executed_count": 0,
        "small_probe_rerun_count": 0,
        "repair_executed_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "queue_reopened_count": 0,
        "closed_group_inspected_count": 0,
        "row_payload_materialized_count": 0,
        "row_payload_inspected_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def validate_outputs(classification: Dict[str, Any], authority: Dict[str, Any], decision: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if classification.get("radius_10000_retry_still_blocked") is not True:
        failures.append("radius_10000_not_blocked")
    if classification.get("not_a_help_routing_failure") is not True:
        failures.append("help_routing_not_confirmed_fixed")
    if authority.get("radius_10000_retry_authorized_now") is not False:
        failures.append("authority_authorized_radius_10000")
    if authority.get("fix_authorized_in_this_unit") is not False:
        failures.append("authority_authorized_fix_in_review_unit")
    if decision.get("radius_10000_retry_authorized") is not False:
        failures.append("decision_authorized_radius_10000")
    if decision.get("repair_authorized_in_this_unit") is not False:
        failures.append("decision_authorized_repair_in_review_unit")

    for key in [
        "radius_10000_retry_executed_count",
        "small_probe_rerun_count",
        "repair_executed_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "queue_reopened_count",
        "closed_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "taxonomy_delta_proposal_emitted_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    if report.get("fix_authority_packet_emitted_count") != 1:
        failures.append("fix_authority_packet_not_emitted")
    if report.get("module_probe_failed_count") != 1:
        failures.append("module_probe_failed_not_recorded")
    if report.get("cli_probe_failed_count") != 1:
        failures.append("cli_probe_failed_not_recorded")
    if report.get("receipt_write_not_proven_count") != 1:
        failures.append("receipt_write_not_proven_not_recorded")

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
        "failed_runtime_output_fix_receipt_consumed_count",
        "failed_runtime_output_fix_artifacts_consumed_count",
        "help_success_surface_emitted_count",
        "module_probe_failure_surface_emitted_count",
        "cli_probe_failure_surface_emitted_count",
        "failure_classification_packet_emitted_count",
        "fix_authority_packet_emitted_count",
        "review_decision_emitted_count",
        "failed_fix_artifacts_preserved_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    for key in [
        "radius_10000_retry_executed_count",
        "small_probe_rerun_count",
        "repair_executed_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "queue_reopened_count",
        "closed_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "taxonomy_delta_proposal_emitted_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_COMPLETE_MODULE_PRECONDITION_FIX_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    help_obj = current_help_surface()
    module_surface, cli_surface = probe_failure_surfaces()
    classification = classify_failure(help_obj, module_surface, cli_surface)
    authority = build_fix_authority_packet(classification)
    decision = build_decision(classification, authority)
    report = build_report(classification, decision)

    trace = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_failed_runtime_output_fix",
                "question": "help still passes but module and CLI probes fail",
                "answer": True,
                "taken": "classify_module_runtime_failure",
            },
            {
                "step": "classify_module_runtime_failure",
                "question": "run repair in review unit",
                "answer": False,
                "taken": "emit_module_runtime_fix_authority_packet",
            },
            {
                "step": "emit_module_runtime_fix_authority_packet",
                "question": "run radius 10000 now",
                "answer": False,
                "taken": "STOP_RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_COMPLETE_MODULE_PRECONDITION_FIX_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_COMPLETE_MODULE_PRECONDITION_FIX_REQUIRED",
            "next_command_goal": None,
        },
    }

    review_surface = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_surface_v0",
        "review_surface_id": sha8({
            "source_failed_runtime_output_fix_receipt_id": SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID,
            "classification": classification["classification"],
        }),
        "source_failed_runtime_output_fix_receipt_id": SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID,
        "failed_fix_gate": read_json(FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_PATH).get("gate"),
        "failed_fix_failures": read_json(FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_PATH).get("failures"),
        "classification": classification["classification"],
        "help_routing_fixed": classification["evidence"]["help_success_confirmed"],
        "module_probe_failed": classification["module_probe_failed"],
        "cli_probe_failed": classification["cli_probe_failed"],
        "runtime_or_precondition_failure": True,
        "radius_10000_retry_still_blocked": True,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

    write_json(FAILURE_REVIEW_SURFACE_PATH, review_surface)
    write_json(HELP_SUCCESS_SURFACE_PATH, help_obj)
    write_json(MODULE_PROBE_FAILURE_SURFACE_PATH, module_surface)
    write_json(CLI_PROBE_FAILURE_SURFACE_PATH, cli_surface)
    write_json(FAILURE_CLASSIFICATION_PACKET_PATH, classification)
    write_json(FIX_AUTHORITY_PACKET_PATH, authority)
    write_json(REVIEW_DECISION_PATH, decision)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(classification, authority, decision, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_0_FAILED_FIX_RECEIPT_CONSUMED": True,
        "RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_1_HELP_SUCCESS_SURFACE_EMITTED": report["help_success_surface_emitted_count"] == 1,
        "RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_2_MODULE_PROBE_FAILURE_SURFACE_EMITTED": report["module_probe_failure_surface_emitted_count"] == 1,
        "RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_3_CLI_PROBE_FAILURE_SURFACE_EMITTED": report["cli_probe_failure_surface_emitted_count"] == 1,
        "RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_4_FAILURE_CLASSIFIED": classification["classification"] in {
            "MODULE_RUNTIME_CLOSED_QUEUE_PRECONDITION_OR_SCHEMA_VALIDATION_FAILURE",
            "MODULE_RUNTIME_EXCEPTION_BEFORE_JSON_RESULT",
            "MODULE_RUNTIME_OUTPUT_STILL_NOT_JSON_AND_RECEIPT_WRITE_NOT_PROVEN",
            "RUNTIME_OUTPUT_FIX_FAILURE_REQUIRES_MANUAL_REVIEW",
        },
        "RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_5_FIX_AUTHORITY_PACKET_EMITTED": report["fix_authority_packet_emitted_count"] == 1,
        "RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_6_NO_REPAIR_OR_RETRY": report["repair_executed_count"] == 0 and report["radius_10000_retry_executed_count"] == 0,
        "RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_7_NO_SMALL_PROBE_RERUN": report["small_probe_rerun_count"] == 0,
        "RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_8_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0,
        "RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_10_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
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
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards = {
        "failed_runtime_output_fix_receipt_consumed": True,
        "failed_fix_artifacts_preserved": True,
        "help_routing_fixed": classification["evidence"]["help_success_confirmed"],
        "module_probe_failed": classification["module_probe_failed"],
        "cli_probe_failed": classification["cli_probe_failed"],
        "failure_classified": True,
        "fix_authority_packet_emitted": True,
        "radius_10000_retry_authorized_now": False,
        "radius_10000_retry_executed": False,
        "small_probe_rerun_executed": False,
        "repair_executed": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "queue_reopened": False,
        "closed_group_inspected": False,
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "identity_assignment": False,
        "field_value_invention": False,
        "taxonomy_delta_proposal_emitted": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_failed_runtime_output_fix_receipt_id": SOURCE_FAILED_RUNTIME_OUTPUT_FIX_RECEIPT_ID,
        "classification": classification["classification"],
        "recommended_next": decision["recommended_next_handling"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "failure_review_surface": rel(FAILURE_REVIEW_SURFACE_PATH),
        "help_success_surface": rel(HELP_SUCCESS_SURFACE_PATH),
        "module_probe_failure_surface": rel(MODULE_PROBE_FAILURE_SURFACE_PATH),
        "cli_probe_failure_surface": rel(CLI_PROBE_FAILURE_SURFACE_PATH),
        "failure_classification_packet": rel(FAILURE_CLASSIFICATION_PACKET_PATH),
        "fix_authority_packet": rel(FIX_AUTHORITY_PACKET_PATH),
        "review_decision": rel(REVIEW_DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_RUNTIME_OUTPUT_FIX_FAILURE_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
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
        "runtime_output_fix_failure_review_summary": {
            "review_result": decision["decision_status"],
            "failure_classification": classification["classification"],
            "help_routing_fixed": classification["evidence"]["help_success_confirmed"],
            "module_probe_failed": classification["module_probe_failed"],
            "cli_probe_failed": classification["cli_probe_failed"],
            "module_probe_stdout_not_json": not classification["evidence"]["module_probe_stdout_json_parseable"],
            "cli_probe_stdout_not_json": not classification["evidence"]["cli_probe_stdout_json_parseable"],
            "receipt_write_not_proven": (classification["evidence"]["module_probe_observation_receipt_count"] or 0) == 0 and (classification["evidence"]["cli_probe_observation_receipt_count"] or 0) == 0,
            "radius_10000_retry_ready": False,
            "radius_10000_retry_authorized": False,
            "radius_10000_retry_executed": False,
            "repair_executed": False,
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "runtime_output_fix_failure_review_guards": guards,
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
    print(f"runtime_output_fix_failure_review_receipt_id={receipt_id}")
    print(f"runtime_output_fix_failure_review_receipt_path=data/r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_v0_receipts/{receipt_id}.json")
    print(f"fix_authority_packet_path=data/r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_review_v0/r1000_post_closure_observability_harvest_entrypoint_runtime_output_fix_failure_fix_authority_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
