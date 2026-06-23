#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "FIX_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_CLI_WRAPPER_RUNTIME_OUTPUT_V0"
TARGET_UNIT_ID = "r1000.post_closure_observability_harvest_entrypoint.cli_wrapper_runtime_output_fix.v0"

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

PROBE_RADIUS = 10
FUTURE_RETRY_RADIUS = 10000

OUT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_v0_receipts"

PATCH_PLAN_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_patch_plan.json"
PRIOR_FAILURE_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_prior_failure_surface.json"
MODULE_PRESERVATION_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_module_preservation_surface.json"
CLI_BEFORE_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_cli_before_surface.json"
CLI_AFTER_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_cli_after_surface.json"
PATCH_REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_patch_report.json"
HELP_CHECK_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_help_check.json"
MODULE_PROBE_RESULT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_module_probe_result.json"
CLI_PROBE_RESULT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_cli_probe_result.json"
RETRY_READY_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet_after_cli_wrapper_runtime_output_fix.json"
FIX_DECISION_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_decision.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_report.json"

CLI_WRAPPER_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_failure_review_v0_receipts" / f"{SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID}.json"
CLI_WRAPPER_FIX_AUTHORITY_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_failure_review_v0" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_failure_fix_authority_packet.json"
CLI_WRAPPER_CLASSIFICATION_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_failure_review_v0" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_failure_classification_packet.json"
CLI_WRAPPER_FAILURE_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_failure_review_v0" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_failure_cli_probe_surface.json"
CLI_WRAPPER_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_failure_review_v0" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_failure_cli_wrapper_surface.json"
MODULE_SUCCESS_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_failure_review_v0" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_failure_module_success_surface.json"

FAILED_MODULE_PRECONDITION_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_v0_receipts" / f"{SOURCE_FAILED_MODULE_PRECONDITION_FIX_RECEIPT_ID}.json"
FAILED_MODULE_PRECONDITION_MODULE_PROBE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_module_probe_result.json"
FAILED_MODULE_PRECONDITION_CLI_PROBE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_v0" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_cli_probe_result.json"

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
    CLI_WRAPPER_REVIEW_RECEIPT_PATH,
    CLI_WRAPPER_FIX_AUTHORITY_PACKET_PATH,
    CLI_WRAPPER_CLASSIFICATION_PACKET_PATH,
    CLI_WRAPPER_FAILURE_SURFACE_PATH,
    CLI_WRAPPER_SURFACE_PATH,
    MODULE_SUCCESS_SURFACE_PATH,
    FAILED_MODULE_PRECONDITION_FIX_RECEIPT_PATH,
    FAILED_MODULE_PRECONDITION_MODULE_PROBE_PATH,
    FAILED_MODULE_PRECONDITION_CLI_PROBE_PATH,
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
    ENTRYPOINT_MODULE_PATH,
]

HUMAN_DECISION = {
    "decision": "FIX_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_CLI_WRAPPER_RUNTIME_OUTPUT",
    "scope": "repair only the CLI wrapper path so it preserves the fixed module path, bypasses noisy Typer/routing output for this command, emits exactly one JSON object on stdout, proves radius-10 CLI probe writes exactly 10 observation receipts, and emits radius-10000 retry-ready packet without running radius 10000",
    "source_cli_wrapper_review_receipt_id": SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID,
    "authorized": [
        "consume CLI-wrapper failure review and fix authority packet",
        "preserve passing module path",
        "modify src/matrixlab/cli.py for this command wrapper/runtime-output path only",
        "run compile and help checks",
        "run bounded radius-10 module preservation probe",
        "run bounded radius-10 CLI probe",
        "emit radius-10000 retry-ready packet only if CLI probe writes 10 receipts and stdout is JSON",
        "stop before radius-10000 retry",
    ],
    "not_authorized": [
        "modifying src/matrixlab/r1000_post_closure_observability_harvest.py",
        "running radius-10000 harvest",
        "running unbounded/no-cap harvest",
        "reopening R1000 pressure queue",
        "inspecting closed groups",
        "materializing row payloads",
        "assigning identity values",
        "inventing values",
        "running unrelated repair",
        "applying taxonomy changes",
        "mutating prior artifacts",
        "mutating existing receipts",
        "hiding next command",
    ],
}

INTERCEPT_BLOCK = r'''
# R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_V0_START
def _r1000_post_closure_observability_harvest_cli_wrapper_runtime_output_fix_v0() -> None:
    import argparse
    import json as _json
    import sys as _sys
    from pathlib import Path as _Path

    argv = list(_sys.argv)
    if len(argv) < 2 or argv[1] != "post-closure-observability-harvest":
        return

    root = _Path(__file__).resolve().parents[2]
    src_root = root / "src"
    if str(src_root) not in _sys.path:
        _sys.path.insert(0, str(src_root))

    parser = argparse.ArgumentParser(prog=f"{argv[0]} post-closure-observability-harvest")
    parser.add_argument("--radius", "-r", type=int, required=True)
    parser.add_argument("--source-closure-receipt-id", default="52d0ea8d")
    parser.add_argument("--label", default=None)

    try:
        ns = parser.parse_args(argv[2:])
        from matrixlab.r1000_post_closure_observability_harvest import run_bounded_harvest
        result = run_bounded_harvest(
            radius=ns.radius,
            source_closure_receipt_id=ns.source_closure_receipt_id,
            label=ns.label,
        )
    except SystemExit:
        raise
    except Exception as exc:
        result = {
            "gate": "FAIL",
            "failures": [f"cli_wrapper_runtime_exception:{type(exc).__name__}:{exc}"],
            "observation_receipt_count": 0,
            "radius_requested": None,
            "terminal": {
                "type": "STOP",
                "stop_code": "STOP_CLI_WRAPPER_RUNTIME_EXCEPTION_CAPTURED",
                "next_command_goal": None,
            },
        }

    print(_json.dumps(result, indent=2, sort_keys=True))
    raise SystemExit(0 if result.get("gate") == "PASS" else 1)


_r1000_post_closure_observability_harvest_cli_wrapper_runtime_output_fix_v0()
# R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_V0_END
'''

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

def run_cmd(args: List[str], timeout: int = 300, env: Dict[str, str] | None = None) -> Tuple[int, str, str, float]:
    start = time.monotonic()
    proc = subprocess.run(
        args,
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        env=env,
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
    review = read_json(CLI_WRAPPER_REVIEW_RECEIPT_PATH)
    authority = read_json(CLI_WRAPPER_FIX_AUTHORITY_PACKET_PATH)
    classification = read_json(CLI_WRAPPER_CLASSIFICATION_PACKET_PATH)
    failed = read_json(FAILED_MODULE_PRECONDITION_FIX_RECEIPT_PATH)
    module_probe = read_json(FAILED_MODULE_PRECONDITION_MODULE_PROBE_PATH)
    cli_probe = read_json(FAILED_MODULE_PRECONDITION_CLI_PROBE_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if review.get("receipt_id") != SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID:
        failures.append("cli_wrapper_review_receipt_id_wrong")
    if review.get("gate") != "PASS":
        failures.append("cli_wrapper_review_not_pass")
    if review.get("module_precondition_fix_failure_review_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("cli_wrapper_review_not_recommending_this_unit")

    if authority.get("recommended_next_handling") != UNIT_ID:
        failures.append("fix_authority_not_for_this_unit")
    if authority.get("fix_authorized_in_this_unit") is not False:
        failures.append("review_unit_authority_leaked_fix_authorization")
    if authority.get("radius_10000_retry_authorized_now") is not False:
        failures.append("review_unit_authorized_radius_10000")

    if classification.get("classification") != "MODULE_FIXED_CLI_WRAPPER_INVOCATION_EXCEPTION_OR_TYPER_ROUTING_FAILURE":
        failures.append("cli_wrapper_classification_wrong")

    if failed.get("receipt_id") != SOURCE_FAILED_MODULE_PRECONDITION_FIX_RECEIPT_ID:
        failures.append("failed_module_precondition_fix_receipt_id_wrong")
    if failed.get("gate") != "FAIL":
        failures.append("failed_module_precondition_fix_gate_not_fail")

    if module_probe.get("probe_passed") is not True:
        failures.append("source_module_probe_not_passed")
    if module_probe.get("probe_observation_receipt_count") != 10:
        failures.append("source_module_probe_receipt_count_not_10")
    if cli_probe.get("probe_passed") is not False:
        failures.append("source_cli_probe_unexpectedly_passed")

    if closure.get("gate") != "PASS":
        failures.append("closure_review_not_pass")
    if handoff.get("handoff_status") != "R1000_PRESSURE_QUEUE_CLOSED_NO_REMAINING_PRESSURE":
        failures.append("closed_queue_handoff_status_wrong")
    if final_queue.get("queue_state_status") != "R1000_PRESSURE_QUEUE_CLOSED":
        failures.append("final_queue_not_closed")
    if final_queue.get("remaining_open_group_count") != 0 or final_queue.get("remaining_open_row_count") != 0:
        failures.append("final_queue_has_remaining_pressure")

    for path in PROTECTED_SOURCE_FILES + [CLI_PATH]:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
    return failures

def source_surface(path: Path) -> Dict[str, Any]:
    text = path.read_text()
    return {
        "path": rel(path),
        "sha256": file_sha256(path),
        "line_count": len(text.splitlines()),
        "has_cli_wrapper_intercept": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_V0_START" in text,
        "intercept_call_before_main": (
            text.find("_r1000_post_closure_observability_harvest_cli_wrapper_runtime_output_fix_v0()")
            < text.find('if __name__ == "__main__"')
            if 'if __name__ == "__main__"' in text else True
        ),
        "contains_direct_command": '@app.command("post-closure-observability-harvest")' in text,
        "contains_typer_echo_json": "typer.echo(json.dumps(result" in text,
        "contains_print_json": "print(json.dumps(result" in text,
        "tail": "\n".join(text.splitlines()[-120:]),
    }

def remove_old_intercept(text: str) -> str:
    pattern = re.compile(
        r"\n?# R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_V0_START\n.*?# R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_V0_END\n?",
        re.DOTALL,
    )
    return pattern.sub("\n", text).rstrip() + "\n"

def insert_intercept_before_main(text: str) -> str:
    cleaned = remove_old_intercept(text)
    match = re.search(r'(?m)^if __name__ == [\'"]__main__[\'"]\s*:', cleaned)
    if match:
        return cleaned[:match.start()].rstrip() + "\n\n" + INTERCEPT_BLOCK.strip() + "\n\n" + cleaned[match.start():].lstrip()
    return cleaned.rstrip() + "\n\n" + INTERCEPT_BLOCK.strip() + "\n"

def patch_cli_wrapper() -> Dict[str, Any]:
    before = CLI_PATH.read_text()
    before_sha = file_sha256(CLI_PATH)
    patched = insert_intercept_before_main(before)

    if "import json" not in patched and "json.dumps(result" in patched:
        lines = patched.splitlines()
        insert_at = 0
        for i, line in enumerate(lines):
            if line.startswith("import ") or line.startswith("from "):
                insert_at = i + 1
        lines.insert(insert_at, "import json")
        patched = "\n".join(lines) + "\n"

    CLI_PATH.write_text(patched)
    after_sha = file_sha256(CLI_PATH)
    return {
        "cli_path": rel(CLI_PATH),
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "patch_applied": before_sha != after_sha,
        "intercept_inserted": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_V0_START" in patched,
        "intercept_before_main": source_surface(CLI_PATH)["intercept_call_before_main"],
        "removed_prior_intercept": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_V0_START" in before,
        "entrypoint_module_unchanged": True,
    }

def run_module_preservation_probe() -> Dict[str, Any]:
    env = dict(__import__("os").environ)
    env["PYTHONPATH"] = str(ROOT / "src") + (":" + env["PYTHONPATH"] if env.get("PYTHONPATH") else "")
    code = "\n".join([
        "import json",
        "from matrixlab.r1000_post_closure_observability_harvest import run_bounded_harvest",
        f"result = run_bounded_harvest(radius={PROBE_RADIUS}, source_closure_receipt_id='{SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID}', label='cli-wrapper-runtime-output-fix-module-preservation-probe')",
        "print(json.dumps(result, indent=2, sort_keys=True))",
    ])
    cmd = ["uv", "run", "python", "-c", code]
    rc, out, err, elapsed = run_cmd(cmd, timeout=300, env=env)
    parsed, parse_error = parse_json_stdout(out)
    passed = rc == 0 and isinstance(parsed, dict) and parsed.get("gate") == "PASS" and parsed.get("observation_receipt_count") == PROBE_RADIUS
    probe = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_module_preservation_probe_v0",
        "probe_command": cmd,
        "returncode": rc,
        "elapsed_seconds": round(elapsed, 6),
        "stdout_tail": out[-12000:],
        "stderr_tail": err[-4000:],
        "stdout_json_parseable": isinstance(parsed, dict),
        "stdout_parse_error": parse_error,
        "parsed_result": parsed,
        "probe_passed": passed,
        "probe_radius": PROBE_RADIUS,
        "probe_observation_receipt_count": parsed.get("observation_receipt_count") if isinstance(parsed, dict) else None,
        "probe_run_receipt_path": parsed.get("run_receipt_path") if isinstance(parsed, dict) else None,
        "probe_rollup_path": parsed.get("rollup_path") if isinstance(parsed, dict) else None,
        "probe_run_dir": parsed.get("run_dir") if isinstance(parsed, dict) else None,
    }
    probe["probe_file_checks"] = probe_file_checks(probe)
    return probe

def run_cli_probe() -> Dict[str, Any]:
    cmd = [
        "uv", "run", "python", "src/matrixlab/cli.py",
        "post-closure-observability-harvest",
        "--radius", str(PROBE_RADIUS),
        "--source-closure-receipt-id", SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "--label", "cli-wrapper-runtime-output-fix-cli-probe",
    ]
    rc, out, err, elapsed = run_cmd(cmd, timeout=300)
    parsed, parse_error = parse_json_stdout(out)
    passed = (
        rc == 0
        and isinstance(parsed, dict)
        and parsed.get("gate") == "PASS"
        and parsed.get("observation_receipt_count") == PROBE_RADIUS
        and (parsed.get("terminal") or {}).get("next_command_goal") is None
    )
    probe = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_cli_probe_result_v0",
        "probe_command": cmd,
        "returncode": rc,
        "elapsed_seconds": round(elapsed, 6),
        "stdout_tail": out[-12000:],
        "stderr_tail": err[-4000:],
        "stdout_json_parseable": isinstance(parsed, dict),
        "stdout_parse_error": parse_error,
        "parsed_result": parsed,
        "probe_passed": passed,
        "probe_radius": PROBE_RADIUS,
        "probe_observation_receipt_count": parsed.get("observation_receipt_count") if isinstance(parsed, dict) else None,
        "probe_run_receipt_path": parsed.get("run_receipt_path") if isinstance(parsed, dict) else None,
        "probe_rollup_path": parsed.get("rollup_path") if isinstance(parsed, dict) else None,
        "probe_run_dir": parsed.get("run_dir") if isinstance(parsed, dict) else None,
    }
    probe["probe_file_checks"] = probe_file_checks(probe)
    return probe

def probe_file_checks(probe: Dict[str, Any]) -> Dict[str, Any]:
    run_dir = probe.get("probe_run_dir")
    run_receipt = probe.get("probe_run_receipt_path")
    rollup = probe.get("probe_rollup_path")
    checks = {
        "run_dir_exists": bool(run_dir) and (ROOT / run_dir).exists(),
        "run_receipt_exists": bool(run_receipt) and (ROOT / run_receipt).exists(),
        "rollup_exists": bool(rollup) and (ROOT / rollup).exists(),
        "observation_receipt_files_count": 0,
    }
    if run_dir and (ROOT / run_dir / "receipts").exists():
        checks["observation_receipt_files_count"] = len(list((ROOT / run_dir / "receipts").glob("*.json")))
    checks["files_valid"] = (
        checks["run_dir_exists"]
        and checks["run_receipt_exists"]
        and checks["rollup_exists"]
        and checks["observation_receipt_files_count"] == PROBE_RADIUS
    )
    return checks

def compile_and_help_checks() -> Dict[str, Any]:
    checks: List[Dict[str, Any]] = []
    for target in [
        "src/matrixlab/cli.py",
        "src/matrixlab/r1000_post_closure_observability_harvest.py",
    ]:
        rc, out, err, elapsed = run_cmd(["uv", "run", "python", "-m", "py_compile", target])
        checks.append({
            "kind": "py_compile",
            "target": target,
            "returncode": rc,
            "stdout_tail": out[-2000:],
            "stderr_tail": err[-4000:],
            "elapsed_seconds": round(elapsed, 6),
        })

    help_cmd = ["uv", "run", "python", "src/matrixlab/cli.py", "post-closure-observability-harvest", "--help"]
    rc, out, err, elapsed = run_cmd(help_cmd)
    checks.append({
        "kind": "entrypoint_help",
        "target": "post-closure-observability-harvest --help",
        "command": help_cmd,
        "returncode": rc,
        "stdout_tail": out[-8000:],
        "stderr_tail": err[-4000:],
        "elapsed_seconds": round(elapsed, 6),
        "contains_radius": "--radius" in out or "--radius" in err,
        "contains_source_closure_receipt_id": "--source-closure-receipt-id" in out or "--source-closure-receipt-id" in err,
    })

    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_help_check_v0",
        "checks": checks,
        "compile_checks_passed": all(c["returncode"] == 0 for c in checks if c["kind"] == "py_compile"),
        "entrypoint_help_passed": any(c["kind"] == "entrypoint_help" and c["returncode"] == 0 and c.get("contains_radius") for c in checks),
    }

def build_retry_packet(cli_probe: Dict[str, Any]) -> Dict[str, Any]:
    ready = cli_probe.get("probe_passed") is True
    command = [
        "uv", "run", "python", "src/matrixlab/cli.py",
        "post-closure-observability-harvest",
        "--radius", str(FUTURE_RETRY_RADIUS),
        "--source-closure-receipt-id", SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "--label", "radius-10000-post-closure-observability-harvest",
    ]
    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet_after_cli_wrapper_runtime_output_fix_v0",
        "packet_status": "RADIUS_10000_RETRY_READY_SEPARATE_UNIT" if ready else "RADIUS_10000_RETRY_BLOCKED_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_PROBE_FAILED",
        "source_cli_wrapper_review_receipt_id": SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID,
        "entrypoint_command": "post-closure-observability-harvest",
        "cli_wrapper_runtime_output_fixed": ready,
        "small_probe_passed": ready,
        "small_probe_radius": PROBE_RADIUS,
        "small_probe_observation_receipt_count": cli_probe.get("probe_observation_receipt_count"),
        "radius_10000_retry_command": command if ready else None,
        "radius_10000_retry_authorized_in_this_unit": False,
        "requires_separate_retry_unit": ready,
        "recommended_next_handling": "RETRY_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_WITH_CLI_WRAPPER_RUNTIME_OUTPUT_FIXED_V0" if ready else "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_FAILURE_V0",
    }

def validate_outputs(help_check: Dict[str, Any], module_probe: Dict[str, Any], cli_probe: Dict[str, Any], retry_packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if help_check.get("compile_checks_passed") is not True:
        failures.append("compile_checks_not_passed")
    if help_check.get("entrypoint_help_passed") is not True:
        failures.append("entrypoint_help_not_passed")
    if module_probe.get("probe_passed") is not True:
        failures.append("module_preservation_probe_not_passed")
    if cli_probe.get("stdout_json_parseable") is not True:
        failures.append("cli_probe_stdout_not_json")
    if cli_probe.get("probe_passed") is not True:
        failures.append("cli_probe_not_passed")
    if cli_probe.get("probe_observation_receipt_count") != PROBE_RADIUS:
        failures.append("cli_probe_receipt_count_wrong")
    if retry_packet.get("packet_status") != "RADIUS_10000_RETRY_READY_SEPARATE_UNIT":
        failures.append("retry_packet_not_ready")
    if retry_packet.get("radius_10000_retry_authorized_in_this_unit") is not False:
        failures.append("radius_10000_authorized_in_this_unit")

    for key in [
        "radius_10000_retry_executed_count",
        "unbounded_or_no_cap_run_count",
        "queue_reopened_count",
        "closed_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "repair_executed_outside_cli_wrapper_count",
        "taxonomy_delta_proposal_emitted_count",
        "existing_receipt_mutation_count",
        "entrypoint_module_mutation_count",
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
        "cli_wrapper_review_receipt_consumed_count",
        "fix_authority_packet_consumed_count",
        "prior_failure_surface_emitted_count",
        "module_preservation_surface_emitted_count",
        "cli_before_surface_emitted_count",
        "cli_after_surface_emitted_count",
        "patch_report_emitted_count",
        "help_check_emitted_count",
        "module_preservation_probe_executed_count",
        "module_preservation_probe_passed_count",
        "cli_probe_executed_count",
        "cli_probe_passed_count",
        "retry_ready_packet_emitted_count",
        "fix_decision_emitted_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    for key in [
        "radius_10000_retry_executed_count",
        "unbounded_or_no_cap_run_count",
        "queue_reopened_count",
        "closed_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "repair_executed_outside_cli_wrapper_count",
        "taxonomy_delta_proposal_emitted_count",
        "existing_receipt_mutation_count",
        "entrypoint_module_mutation_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_COMPLETE_SMALL_PROBE_PASSED_RETRY_READY":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    protected_before = snapshot_files(PROTECTED_SOURCE_FILES)
    cli_before_sha = file_sha256(CLI_PATH)
    module_before_sha = file_sha256(ENTRYPOINT_MODULE_PATH)
    failures = validate_sources()

    prior_failure_surface = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_prior_failure_surface_v0",
        "source_cli_wrapper_review_receipt_id": SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID,
        "cli_wrapper_review_summary": read_json(CLI_WRAPPER_REVIEW_RECEIPT_PATH).get("module_precondition_fix_failure_review_summary"),
        "cli_probe_failure_surface": read_json(CLI_WRAPPER_FAILURE_SURFACE_PATH),
        "cli_wrapper_surface": read_json(CLI_WRAPPER_SURFACE_PATH),
        "module_success_surface": read_json(MODULE_SUCCESS_SURFACE_PATH),
    }
    write_json(PRIOR_FAILURE_SURFACE_PATH, prior_failure_surface)

    write_json(CLI_BEFORE_SURFACE_PATH, source_surface(CLI_PATH))

    patch_plan = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_patch_plan_v0",
        "source_cli_wrapper_review_receipt_id": SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID,
        "classification": "MODULE_FIXED_CLI_WRAPPER_INVOCATION_EXCEPTION_OR_TYPER_ROUTING_FAILURE",
        "actions": [
            "preserve fixed module path unchanged",
            "insert exact argv intercept before Typer app invocation",
            "route post-closure-observability-harvest through fixed run_bounded_harvest",
            "print exactly one JSON object on stdout",
            "run radius-10 module preservation probe",
            "run radius-10 CLI probe and require 10 observation receipts",
            "emit radius-10000 retry-ready packet only after CLI probe pass",
        ],
        "radius_10000_authorized_in_this_unit": False,
    }
    write_json(PATCH_PLAN_PATH, patch_plan)

    patch_report_inner = patch_cli_wrapper()
    write_json(CLI_AFTER_SURFACE_PATH, source_surface(CLI_PATH))

    help_check = compile_and_help_checks()
    write_json(HELP_CHECK_PATH, help_check)

    module_probe = run_module_preservation_probe()
    write_json(MODULE_PROBE_RESULT_PATH, module_probe)

    cli_probe = run_cli_probe()
    write_json(CLI_PROBE_RESULT_PATH, cli_probe)

    retry_packet = build_retry_packet(cli_probe)
    write_json(RETRY_READY_PACKET_PATH, retry_packet)

    module_after_sha = file_sha256(ENTRYPOINT_MODULE_PATH)
    cli_after_sha = file_sha256(CLI_PATH)

    module_preservation = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_module_preservation_surface_v0",
        "entrypoint_module_path": rel(ENTRYPOINT_MODULE_PATH),
        "module_before_sha256": module_before_sha,
        "module_after_sha256": module_after_sha,
        "module_unchanged_in_this_unit": module_before_sha == module_after_sha,
        "module_preservation_probe": module_probe,
    }
    write_json(MODULE_PRESERVATION_SURFACE_PATH, module_preservation)

    decision = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_decision_v0",
        "decision_id": sha8({
            "unit_id": UNIT_ID,
            "module_probe_passed": module_probe.get("probe_passed"),
            "cli_probe_passed": cli_probe.get("probe_passed"),
        }),
        "decision_status": "CLI_WRAPPER_RUNTIME_OUTPUT_FIXED_SMALL_PROBE_PASSED_RETRY_READY" if cli_probe.get("probe_passed") else "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_INCOMPLETE_SMALL_PROBE_FAILED",
        "cli_wrapper_runtime_output_fixed": cli_probe.get("probe_passed") is True,
        "module_preserved": module_before_sha == module_after_sha,
        "help_check_passed": help_check.get("entrypoint_help_passed") is True,
        "module_preservation_probe_passed": module_probe.get("probe_passed") is True,
        "cli_probe_passed": cli_probe.get("probe_passed") is True,
        "cli_probe_stdout_json_parseable": cli_probe.get("stdout_json_parseable") is True,
        "cli_probe_observation_receipt_count": cli_probe.get("probe_observation_receipt_count"),
        "radius_10000_retry_ready": retry_packet["packet_status"] == "RADIUS_10000_RETRY_READY_SEPARATE_UNIT",
        "radius_10000_retry_executed": False,
        "recommended_next_handling": retry_packet["recommended_next_handling"],
    }
    write_json(FIX_DECISION_PATH, decision)

    report = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_cli_wrapper_review_receipt_id": SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID,
        "cli_wrapper_review_receipt_consumed_count": 1,
        "fix_authority_packet_consumed_count": 1,
        "prior_failure_surface_emitted_count": 1,
        "module_preservation_surface_emitted_count": 1,
        "cli_before_surface_emitted_count": 1,
        "cli_after_surface_emitted_count": 1,
        "patch_report_emitted_count": 1,
        "cli_patch_applied_count": 1 if patch_report_inner["patch_applied"] else 0,
        "cli_intercept_inserted_count": 1 if patch_report_inner["intercept_inserted"] else 0,
        "cli_intercept_before_main_count": 1 if patch_report_inner["intercept_before_main"] else 0,
        "entrypoint_module_mutation_count": 0 if module_before_sha == module_after_sha else 1,
        "help_check_emitted_count": 1,
        "compile_checks_passed_count": 1 if help_check.get("compile_checks_passed") else 0,
        "entrypoint_help_passed_count": 1 if help_check.get("entrypoint_help_passed") else 0,
        "module_preservation_probe_executed_count": 1,
        "module_preservation_probe_passed_count": 1 if module_probe.get("probe_passed") else 0,
        "module_preservation_probe_observation_receipt_count": module_probe.get("probe_observation_receipt_count") or 0,
        "module_preservation_probe_observation_receipt_files_count": module_probe.get("probe_file_checks", {}).get("observation_receipt_files_count") or 0,
        "cli_probe_executed_count": 1,
        "cli_probe_passed_count": 1 if cli_probe.get("probe_passed") else 0,
        "cli_probe_stdout_json_parseable_count": 1 if cli_probe.get("stdout_json_parseable") else 0,
        "cli_probe_observation_receipt_count": cli_probe.get("probe_observation_receipt_count") or 0,
        "cli_probe_observation_receipt_files_count": cli_probe.get("probe_file_checks", {}).get("observation_receipt_files_count") or 0,
        "cli_wrapper_runtime_output_fixed_count": 1 if cli_probe.get("probe_passed") else 0,
        "retry_ready_packet_emitted_count": 1,
        "radius_10000_retry_ready_count": 1 if retry_packet["packet_status"] == "RADIUS_10000_RETRY_READY_SEPARATE_UNIT" else 0,
        "fix_decision_emitted_count": 1,
        "radius_10000_retry_executed_count": 0,
        "unbounded_or_no_cap_run_count": 0,
        "queue_reopened_count": 0,
        "closed_group_inspected_count": 0,
        "row_payload_materialized_count": 0,
        "row_payload_inspected_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "repair_executed_outside_cli_wrapper_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": retry_packet["recommended_next_handling"],
    }
    write_json(REPORT_PATH, report)

    patch_report = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_patch_report_v0",
        "cli_patch": patch_report_inner,
        "cli_before_sha256": cli_before_sha,
        "cli_after_sha256": cli_after_sha,
        "module_before_sha256": module_before_sha,
        "module_after_sha256": module_after_sha,
        "module_unchanged": module_before_sha == module_after_sha,
        "help_check_ref": rel(HELP_CHECK_PATH),
        "module_probe_result_ref": rel(MODULE_PROBE_RESULT_PATH),
        "cli_probe_result_ref": rel(CLI_PROBE_RESULT_PATH),
    }
    write_json(PATCH_REPORT_PATH, patch_report)

    failures.extend(validate_outputs(help_check, module_probe, cli_probe, retry_packet, report))

    protected_after = snapshot_files(PROTECTED_SOURCE_FILES)
    protected_mutation_detected = protected_before != protected_after
    if protected_mutation_detected:
        failures.append("protected_prior_or_module_artifact_hash_changed")

    trace = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_transition_trace_v0",
        "trace": [
            {
                "step": "consume_cli_wrapper_failure_review",
                "question": "module path passes and CLI wrapper fails",
                "answer": True,
                "taken": "patch_cli_wrapper_intercept",
            },
            {
                "step": "patch_cli_wrapper_intercept",
                "question": "compile and help checks pass",
                "answer": help_check.get("compile_checks_passed") is True and help_check.get("entrypoint_help_passed") is True,
                "taken": "run_module_preservation_probe",
            },
            {
                "step": "run_module_preservation_probe",
                "question": "module path remains passing",
                "answer": module_probe.get("probe_passed") is True,
                "taken": "run_cli_probe",
            },
            {
                "step": "run_cli_probe",
                "question": "CLI probe emits JSON and writes 10 observation receipts",
                "answer": cli_probe.get("probe_passed") is True,
                "taken": "emit_retry_ready_packet" if cli_probe.get("probe_passed") else "emit_cli_wrapper_fix_failure_packet",
            },
            {
                "step": "emit_retry_ready_packet",
                "question": "run radius 10000 now",
                "answer": False,
                "taken": "STOP_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_COMPLETE_SMALL_PROBE_PASSED_RETRY_READY" if cli_probe.get("probe_passed") else "STOP_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_INCOMPLETE_SMALL_PROBE_FAILED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_COMPLETE_SMALL_PROBE_PASSED_RETRY_READY" if cli_probe.get("probe_passed") else "STOP_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_INCOMPLETE_SMALL_PROBE_FAILED",
            "next_command_goal": None,
        },
    }
    write_json(TRANSITION_TRACE_PATH, trace)

    acceptance_gate_results = {
        "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_0_REVIEW_CONSUMED": True,
        "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_1_MODULE_PRESERVED": module_before_sha == module_after_sha,
        "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_2_CLI_PATCHED": report["cli_patch_applied_count"] == 1 and report["cli_intercept_inserted_count"] == 1,
        "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_3_COMPILE_HELP_PASS": help_check.get("compile_checks_passed") is True and help_check.get("entrypoint_help_passed") is True,
        "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_4_MODULE_PRESERVATION_PROBE_PASSES": report["module_preservation_probe_passed_count"] == 1 and report["module_preservation_probe_observation_receipt_count"] == PROBE_RADIUS,
        "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_5_CLI_PROBE_STDOUT_JSON": report["cli_probe_stdout_json_parseable_count"] == 1,
        "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_6_CLI_PROBE_WRITES_10_RECEIPTS": report["cli_probe_passed_count"] == 1 and report["cli_probe_observation_receipt_count"] == PROBE_RADIUS and report["cli_probe_observation_receipt_files_count"] == PROBE_RADIUS,
        "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_7_RETRY_READY_PACKET_EMITTED": report["retry_ready_packet_emitted_count"] == 1 and report["radius_10000_retry_ready_count"] == 1,
        "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_8_RADIUS_10000_NOT_EXECUTED": report["radius_10000_retry_executed_count"] == 0,
        "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_9_NO_UNBOUNDED_RUN": report["unbounded_or_no_cap_run_count"] == 0,
        "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_10_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0,
        "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_11_NO_PRIOR_ARTIFACT_OR_MODULE_MUTATION": protected_mutation_detected is False and report["existing_receipt_mutation_count"] == 0 and report["entrypoint_module_mutation_count"] == 0,
        "CLI_WRAPPER_RUNTIME_OUTPUT_FIX_12_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if protected_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
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
        "protected_prior_or_module_artifact_mutation_count": 1 if protected_mutation_detected else 0,
    }

    guards = {
        "cli_wrapper_review_consumed": True,
        "cli_wrapper_fix_authorized": True,
        "entrypoint_module_modified": module_before_sha != module_after_sha,
        "cli_source_modified": cli_before_sha != cli_after_sha,
        "module_preservation_probe_passed": module_probe.get("probe_passed"),
        "help_check_passed": help_check.get("entrypoint_help_passed"),
        "cli_probe_executed": True,
        "cli_probe_passed": cli_probe.get("probe_passed"),
        "cli_probe_stdout_json_parseable": cli_probe.get("stdout_json_parseable"),
        "radius_10000_retry_ready": retry_packet["packet_status"] == "RADIUS_10000_RETRY_READY_SEPARATE_UNIT",
        "radius_10000_retry_authorized_in_this_unit": False,
        "radius_10000_retry_executed": False,
        "unbounded_or_no_cap_run": False,
        "queue_reopened": False,
        "closed_group_inspected": False,
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "identity_assignment": False,
        "field_value_invention": False,
        "repair_executed_outside_cli_wrapper": False,
        "taxonomy_delta_proposal_emitted": False,
        "existing_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_cli_wrapper_review_receipt_id": SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID,
        "cli_probe_passed": cli_probe.get("probe_passed"),
        "retry_ready": retry_packet["packet_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "patch_plan": rel(PATCH_PLAN_PATH),
        "prior_failure_surface": rel(PRIOR_FAILURE_SURFACE_PATH),
        "module_preservation_surface": rel(MODULE_PRESERVATION_SURFACE_PATH),
        "cli_before_surface": rel(CLI_BEFORE_SURFACE_PATH),
        "cli_after_surface": rel(CLI_AFTER_SURFACE_PATH),
        "patch_report": rel(PATCH_REPORT_PATH),
        "help_check": rel(HELP_CHECK_PATH),
        "module_probe_result": rel(MODULE_PROBE_RESULT_PATH),
        "cli_probe_result": rel(CLI_PROBE_RESULT_PATH),
        "retry_ready_packet": rel(RETRY_READY_PACKET_PATH),
        "fix_decision": rel(FIX_DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "cli_path": rel(CLI_PATH),
        "entrypoint_module_path": rel(ENTRYPOINT_MODULE_PATH),
    }

    receipt = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_CLI_WRAPPER_RUNTIME_OUTPUT_FIX_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
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
        "cli_wrapper_runtime_output_fix_summary": {
            "decision_status": decision["decision_status"],
            "cli_wrapper_runtime_output_fixed": decision["cli_wrapper_runtime_output_fixed"],
            "entrypoint_command": "post-closure-observability-harvest",
            "module_preserved": decision["module_preserved"],
            "module_preservation_probe_passed": decision["module_preservation_probe_passed"],
            "help_check_passed": decision["help_check_passed"],
            "cli_probe_executed": True,
            "cli_probe_passed": decision["cli_probe_passed"],
            "cli_probe_stdout_json_parseable": decision["cli_probe_stdout_json_parseable"],
            "cli_probe_observation_receipt_count": decision["cli_probe_observation_receipt_count"],
            "radius_10000_retry_ready": decision["radius_10000_retry_ready"],
            "radius_10000_retry_executed": False,
            "radius_10000_retry_command": retry_packet["radius_10000_retry_command"],
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "cli_wrapper_runtime_output_fix_guards": guards,
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
    print(f"cli_wrapper_runtime_output_fix_receipt_id={receipt_id}")
    print(f"cli_wrapper_runtime_output_fix_receipt_path=data/r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_v0_receipts/{receipt_id}.json")
    print(f"retry_ready_packet_path=data/r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_v0/r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet_after_cli_wrapper_runtime_output_fix.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
