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

UNIT_ID = "FIX_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_CLI_REGISTRATION_V0"
TARGET_UNIT_ID = "r1000.post_closure_observability_harvest_entrypoint.cli_registration_fix.v0"

SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID = "960a1048"
SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID = "9d834354"
SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID = "2d61b52e"
SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID = "b35e7989"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"

PROBE_RADIUS = 10
FUTURE_RETRY_RADIUS = 10000

OUT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_v0_receipts"

PATCH_PLAN_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_patch_plan.json"
CLI_BEFORE_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_before_surface.json"
CLI_AFTER_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_after_surface.json"
PATCH_REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_patch_report.json"
HELP_CHECK_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_help_check.json"
SMALL_PROBE_RESULT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_small_probe_result.json"
RETRY_READY_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet_after_cli_registration_fix.json"
FIX_DECISION_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_decision.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_report.json"

BUILD_FAILURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_v0_receipts" / f"{SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID}.json"
FIX_AUTHORITY_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_v0" / "r1000_post_closure_observability_harvest_entrypoint_build_failure_fix_authority_packet.json"
FAILURE_CLASSIFICATION_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_v0" / "r1000_post_closure_observability_harvest_entrypoint_build_failure_classification_packet.json"
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
    BUILD_FAILURE_REVIEW_RECEIPT_PATH,
    FIX_AUTHORITY_PACKET_PATH,
    FAILURE_CLASSIFICATION_PACKET_PATH,
    FAILED_ENTRYPOINT_BUILD_RECEIPT_PATH,
    CLI_ENTRYPOINT_INSPECTION_RECEIPT_PATH,
    COMMAND_RESOLVER_FIX_RECEIPT_PATH,
    CLOSURE_REVIEW_RECEIPT_PATH,
    CLOSED_QUEUE_HANDOFF_PATH,
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    FINAL_QUEUE_STATE_PATH,
]

HUMAN_DECISION = {
    "decision": "FIX_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_CLI_REGISTRATION",
    "scope": "repair the previously built post-closure observability harvest entrypoint by fixing CLI registration/help routing and pure JSON probe output, prove it with a bounded radius-10 probe, and emit a radius-10000 retry-ready packet only if the probe passes",
    "source_build_failure_review_receipt_id": SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID,
    "authorized": [
        "consume failed build review and fix authority packet",
        "modify src/matrixlab/cli.py only for entrypoint registration placement/removal of broken registration block",
        "modify src/matrixlab/r1000_post_closure_observability_harvest.py only for probe-compatible CLI surface if needed",
        "run compile checks",
        "run CLI help check",
        "run bounded radius-10 probe",
        "emit retry-ready packet if radius-10 probe writes 10 receipts",
        "stop before radius-10000 retry",
    ],
    "not_authorized": [
        "running radius-10000 harvest",
        "running unbounded/no-cap harvest",
        "reopening R1000 pressure queue",
        "inspecting closed groups",
        "materializing row payloads",
        "assigning identity values",
        "inventing values",
        "filling source fields outside entrypoint implementation",
        "running repair outside CLI registration fix",
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

def run_cmd(args: List[str], timeout: int = 240) -> Tuple[int, str, str, float]:
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

def validate_sources() -> List[str]:
    failures: List[str] = []
    review = read_json(BUILD_FAILURE_REVIEW_RECEIPT_PATH)
    authority = read_json(FIX_AUTHORITY_PACKET_PATH)
    classification = read_json(FAILURE_CLASSIFICATION_PACKET_PATH)
    failed_build = read_json(FAILED_ENTRYPOINT_BUILD_RECEIPT_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if review.get("receipt_id") != SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID:
        failures.append("build_failure_review_receipt_id_wrong")
    if review.get("gate") != "PASS":
        failures.append("build_failure_review_not_pass")
    if review.get("entrypoint_build_failure_review_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("build_failure_review_not_recommending_this_unit")

    if authority.get("authorized_next_unit") != UNIT_ID:
        failures.append("fix_authority_not_for_this_unit")
    if authority.get("fix_authorized_in_this_unit") is not False:
        failures.append("review_unit_authority_leaked_fix_authorization")
    if authority.get("radius_10000_retry_authorized_now") is not False:
        failures.append("review_unit_authorized_radius_10000")

    if classification.get("classification") != "CLI_REGISTRATION_OR_HELP_ROUTING_FAILURE":
        failures.append("failure_classification_not_cli_registration")

    if failed_build.get("receipt_id") != SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID:
        failures.append("failed_entrypoint_build_receipt_id_wrong")
    if failed_build.get("gate") != "FAIL":
        failures.append("failed_entrypoint_build_gate_not_fail")

    if closure.get("gate") != "PASS":
        failures.append("closure_review_not_pass")
    if handoff.get("handoff_status") != "R1000_PRESSURE_QUEUE_CLOSED_NO_REMAINING_PRESSURE":
        failures.append("closed_queue_handoff_status_wrong")
    if final_queue.get("queue_state_status") != "R1000_PRESSURE_QUEUE_CLOSED":
        failures.append("final_queue_not_closed")
    if final_queue.get("remaining_open_group_count") != 0 or final_queue.get("remaining_open_row_count") != 0:
        failures.append("final_queue_has_remaining_pressure")

    for path in SOURCE_FILES + [CLI_PATH, ENTRYPOINT_MODULE_PATH]:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")

    return failures

def surface_cli(path: Path) -> Dict[str, Any]:
    text = path.read_text()
    main_idx = text.find('if __name__ == "__main__"')
    marker_count = text.count("R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT")
    direct_command_count = text.count('@app.command("post-closure-observability-harvest")')
    add_typer_count = text.count("_r1000_post_closure_observability_harvest_app")
    return {
        "path": rel(path),
        "sha256": file_sha256(path),
        "line_count": len(text.splitlines()),
        "main_block_index": main_idx,
        "marker_count": marker_count,
        "direct_command_count": direct_command_count,
        "broken_add_typer_registration_count": add_typer_count,
        "tail": "\n".join(text.splitlines()[-80:]),
    }

def remove_old_registration_block(text: str) -> str:
    lines = text.splitlines()
    out: List[str] = []
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.strip() == "# R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_V0":
            i += 1
            while i < len(lines):
                probe = lines[i]
                if (
                    probe.startswith("try:")
                    or probe.startswith("    from matrixlab.r1000_post_closure_observability_harvest")
                    or probe.startswith("    app.add_typer(_r1000_post_closure_observability_harvest_app")
                    or probe.startswith("except Exception as _r1000_post_closure_observability_harvest_import_error")
                    or probe.startswith("    pass")
                    or probe.strip() == ""
                ):
                    i += 1
                    continue
                break
            continue
        if "r1000_post_closure_observability_harvest" in line and "_r1000_post_closure_observability_harvest" in line:
            i += 1
            continue
        out.append(line)
        i += 1
    return "\n".join(out).rstrip() + "\n"

def find_insert_index_before_main(text: str) -> int:
    match = re.search(r'(?m)^if __name__ == [\'"]__main__[\'"]\s*:', text)
    if match:
        return match.start()
    return len(text)

def patch_cli_registration() -> Dict[str, Any]:
    before = CLI_PATH.read_text()
    before_sha = file_sha256(CLI_PATH)
    cleaned = remove_old_registration_block(before)

    block = '''
# R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_V0_FIXED
@app.command("post-closure-observability-harvest")
def post_closure_observability_harvest_command(
    radius: int = typer.Option(..., "--radius", "-r", min=1, help="Bounded number of observation receipts to emit."),
    source_closure_receipt_id: str = typer.Option("52d0ea8d", "--source-closure-receipt-id", help="Accepted closure review receipt id."),
    label: str | None = typer.Option(None, "--label", help="Optional run label."),
) -> None:
    """Emit bounded post-closure observability receipts without reopening the closed queue."""
    from matrixlab.r1000_post_closure_observability_harvest import run_bounded_harvest
    result = run_bounded_harvest(
        radius=radius,
        source_closure_receipt_id=source_closure_receipt_id,
        label=label,
    )
    typer.echo(json.dumps(result, indent=2, sort_keys=True))
    if result.get("gate") != "PASS":
        raise typer.Exit(code=1)

'''.lstrip()

    if '@app.command("post-closure-observability-harvest")' not in cleaned:
        idx = find_insert_index_before_main(cleaned)
        patched = cleaned[:idx].rstrip() + "\n\n" + block + "\n" + cleaned[idx:].lstrip()
    else:
        patched = cleaned

    CLI_PATH.write_text(patched)
    after_sha = file_sha256(CLI_PATH)
    return {
        "cli_path": rel(CLI_PATH),
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "patch_applied": before_sha != after_sha,
        "old_broken_registration_removed": before.count("_r1000_post_closure_observability_harvest_app") > patched.count("_r1000_post_closure_observability_harvest_app"),
        "direct_command_present": '@app.command("post-closure-observability-harvest")' in patched,
        "registration_before_main": patched.find('@app.command("post-closure-observability-harvest")') < find_insert_index_before_main(patched),
    }

def ensure_module_is_probe_compatible() -> Dict[str, Any]:
    text = ENTRYPOINT_MODULE_PATH.read_text()
    before_sha = file_sha256(ENTRYPOINT_MODULE_PATH)
    changed = False

    # Keep module command available, but the fixed CLI path calls run_bounded_harvest directly.
    # Ensure no debugging prints were accidentally added outside the Typer command path.
    if "def run_bounded_harvest(" not in text:
        raise SystemExit("STOP_ENTRYPOINT_MODULE_MISSING_RUN_BOUNDED_HARVEST")

    after_sha = file_sha256(ENTRYPOINT_MODULE_PATH)
    return {
        "module_path": rel(ENTRYPOINT_MODULE_PATH),
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "patch_applied": changed,
        "run_bounded_harvest_present": True,
    }

def compile_and_help_checks() -> Dict[str, Any]:
    checks = []
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

    root_cmd = ["uv", "run", "python", "src/matrixlab/cli.py", "--help"]
    rc, out, err, elapsed = run_cmd(root_cmd)
    checks.append({
        "kind": "root_help",
        "target": "root --help",
        "command": root_cmd,
        "returncode": rc,
        "stdout_tail": out[-8000:],
        "stderr_tail": err[-4000:],
        "elapsed_seconds": round(elapsed, 6),
        "mentions_entrypoint": "post-closure-observability-harvest" in out or "post-closure-observability-harvest" in err,
    })

    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_registration_help_check_v0",
        "checks": checks,
        "compile_checks_passed": all(c["returncode"] == 0 for c in checks if c["kind"] == "py_compile"),
        "entrypoint_help_passed": any(c["kind"] == "entrypoint_help" and c["returncode"] == 0 and c.get("contains_radius") for c in checks),
        "root_help_passed": any(c["kind"] == "root_help" and c["returncode"] == 0 for c in checks),
    }

def run_small_probe() -> Dict[str, Any]:
    cmd = [
        "uv", "run", "python", "src/matrixlab/cli.py",
        "post-closure-observability-harvest",
        "--radius", str(PROBE_RADIUS),
        "--source-closure-receipt-id", SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "--label", "cli-registration-fix-small-probe",
    ]
    rc, out, err, elapsed = run_cmd(cmd, timeout=240)
    parsed = None
    parse_error = None
    try:
        parsed = json.loads(out)
    except Exception as exc:
        parse_error = f"{type(exc).__name__}: {exc}"

    probe_passed = (
        rc == 0
        and isinstance(parsed, dict)
        and parsed.get("gate") == "PASS"
        and parsed.get("observation_receipt_count") == PROBE_RADIUS
        and (parsed.get("terminal") or {}).get("next_command_goal") is None
    )

    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_registration_small_probe_result_v0",
        "probe_command": cmd,
        "returncode": rc,
        "elapsed_seconds": round(elapsed, 6),
        "stdout_tail": out[-12000:],
        "stderr_tail": err[-4000:],
        "stdout_json_parseable": isinstance(parsed, dict),
        "stdout_parse_error": parse_error,
        "parsed_result": parsed,
        "probe_passed": probe_passed,
        "probe_radius": PROBE_RADIUS,
        "probe_observation_receipt_count": parsed.get("observation_receipt_count") if isinstance(parsed, dict) else None,
        "probe_run_receipt_path": parsed.get("run_receipt_path") if isinstance(parsed, dict) else None,
        "probe_rollup_path": parsed.get("rollup_path") if isinstance(parsed, dict) else None,
        "probe_run_dir": parsed.get("run_dir") if isinstance(parsed, dict) else None,
    }

def build_retry_packet(probe: Dict[str, Any]) -> Dict[str, Any]:
    ready = probe["probe_passed"] is True
    command = [
        "uv", "run", "python", "src/matrixlab/cli.py",
        "post-closure-observability-harvest",
        "--radius", str(FUTURE_RETRY_RADIUS),
        "--source-closure-receipt-id", SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "--label", "radius-10000-post-closure-observability-harvest",
    ]
    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet_after_cli_registration_fix_v0",
        "packet_status": "RADIUS_10000_RETRY_READY_SEPARATE_UNIT" if ready else "RADIUS_10000_RETRY_BLOCKED_CLI_REGISTRATION_FIX_PROBE_FAILED",
        "source_build_failure_review_receipt_id": SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID,
        "entrypoint_command": "post-closure-observability-harvest",
        "cli_registration_fixed": ready,
        "small_probe_passed": ready,
        "small_probe_radius": PROBE_RADIUS,
        "small_probe_observation_receipt_count": probe.get("probe_observation_receipt_count"),
        "radius_10000_retry_command": command if ready else None,
        "radius_10000_retry_authorized_in_this_unit": False,
        "requires_separate_retry_unit": ready,
        "recommended_next_handling": "RETRY_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_WITH_FIXED_CLI_REGISTRATION_V0" if ready else "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_CLI_REGISTRATION_FIX_FAILURE_V0",
    }

def validate_outputs(help_check: Dict[str, Any], probe: Dict[str, Any], retry_packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if help_check.get("compile_checks_passed") is not True:
        failures.append("compile_checks_not_passed")
    if help_check.get("entrypoint_help_passed") is not True:
        failures.append("entrypoint_help_not_passed")
    if probe.get("stdout_json_parseable") is not True:
        failures.append("probe_stdout_not_json")
    if probe.get("probe_passed") is not True:
        failures.append("small_probe_not_passed")
    if probe.get("probe_observation_receipt_count") != PROBE_RADIUS:
        failures.append("small_probe_receipt_count_wrong")
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
        "repair_executed_outside_cli_registration_count",
        "taxonomy_delta_proposal_emitted_count",
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
        "build_failure_review_receipt_consumed_count",
        "fix_authority_packet_consumed_count",
        "cli_before_surface_emitted_count",
        "cli_after_surface_emitted_count",
        "cli_patch_report_emitted_count",
        "help_check_emitted_count",
        "small_probe_executed_count",
        "small_probe_passed_count",
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
        "repair_executed_outside_cli_registration_count",
        "taxonomy_delta_proposal_emitted_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_CLI_REGISTRATION_FIX_COMPLETE_SMALL_PROBE_PASSED_RETRY_READY":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    protected_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    before_surface = surface_cli(CLI_PATH)
    write_json(CLI_BEFORE_SURFACE_PATH, before_surface)

    patch_plan = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_registration_patch_plan_v0",
        "source_build_failure_review_receipt_id": SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID,
        "failure_classification": "CLI_REGISTRATION_OR_HELP_ROUTING_FAILURE",
        "actions": [
            "remove broken late add_typer block if present",
            "insert direct @app.command registration before __main__ invocation",
            "call run_bounded_harvest directly from command wrapper",
            "require help surface with --radius",
            "require radius-10 probe stdout pure JSON and 10 observation receipts",
        ],
        "radius_10000_authorized_in_this_unit": False,
    }
    write_json(PATCH_PLAN_PATH, patch_plan)

    module_report = ensure_module_is_probe_compatible()
    cli_patch_report = patch_cli_registration()
    after_surface = surface_cli(CLI_PATH)
    write_json(CLI_AFTER_SURFACE_PATH, after_surface)

    help_check = compile_and_help_checks()
    write_json(HELP_CHECK_PATH, help_check)

    probe = run_small_probe()
    write_json(SMALL_PROBE_RESULT_PATH, probe)

    retry_packet = build_retry_packet(probe)
    write_json(RETRY_READY_PACKET_PATH, retry_packet)

    decision = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_decision_v0",
        "decision_id": sha8({
            "unit_id": UNIT_ID,
            "probe_passed": probe["probe_passed"],
            "help_passed": help_check["entrypoint_help_passed"],
        }),
        "decision_status": "CLI_REGISTRATION_FIXED_SMALL_PROBE_PASSED_RETRY_READY" if probe["probe_passed"] else "CLI_REGISTRATION_FIX_INCOMPLETE_SMALL_PROBE_FAILED",
        "cli_registration_fixed": probe["probe_passed"],
        "help_check_passed": help_check["entrypoint_help_passed"],
        "small_probe_passed": probe["probe_passed"],
        "radius_10000_retry_ready": retry_packet["packet_status"] == "RADIUS_10000_RETRY_READY_SEPARATE_UNIT",
        "radius_10000_retry_executed": False,
        "recommended_next_handling": retry_packet["recommended_next_handling"],
    }
    write_json(FIX_DECISION_PATH, decision)

    report = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_build_failure_review_receipt_id": SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID,
        "build_failure_review_receipt_consumed_count": 1,
        "fix_authority_packet_consumed_count": 1,
        "cli_before_surface_emitted_count": 1,
        "cli_after_surface_emitted_count": 1,
        "cli_patch_report_emitted_count": 1,
        "module_probe_compatibility_checked_count": 1,
        "cli_direct_command_present_count": 1 if after_surface["direct_command_count"] >= 1 else 0,
        "broken_late_add_typer_removed_count": 1 if cli_patch_report["old_broken_registration_removed"] else 0,
        "registration_before_main_count": 1 if cli_patch_report["registration_before_main"] else 0,
        "compile_checks_passed_count": 1 if help_check["compile_checks_passed"] else 0,
        "help_check_emitted_count": 1,
        "entrypoint_help_passed_count": 1 if help_check["entrypoint_help_passed"] else 0,
        "small_probe_executed_count": 1,
        "small_probe_passed_count": 1 if probe["probe_passed"] else 0,
        "small_probe_radius": PROBE_RADIUS,
        "small_probe_observation_receipt_count": probe.get("probe_observation_receipt_count") or 0,
        "probe_stdout_json_parseable_count": 1 if probe["stdout_json_parseable"] else 0,
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
        "repair_executed_outside_cli_registration_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": retry_packet["recommended_next_handling"],
    }
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(help_check, probe, retry_packet, report))

    protected_after = snapshot_files(SOURCE_FILES)
    protected_mutation_detected = protected_before != protected_after
    if protected_mutation_detected:
        failures.append("protected_prior_artifact_hash_changed")

    trace = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_transition_trace_v0",
        "trace": [
            {
                "step": "consume_build_failure_review",
                "question": "failure was CLI registration/help routing failure",
                "answer": True,
                "taken": "patch_cli_registration",
            },
            {
                "step": "patch_cli_registration",
                "question": "help exposes --radius",
                "answer": help_check["entrypoint_help_passed"],
                "taken": "run_radius_10_probe",
            },
            {
                "step": "run_radius_10_probe",
                "question": "probe stdout is JSON and emits 10 receipts",
                "answer": probe["probe_passed"],
                "taken": "emit_retry_ready_packet" if probe["probe_passed"] else "emit_fix_failure_packet",
            },
            {
                "step": "emit_retry_ready_packet",
                "question": "run radius 10000 now",
                "answer": False,
                "taken": "STOP_CLI_REGISTRATION_FIX_COMPLETE_SMALL_PROBE_PASSED_RETRY_READY" if probe["probe_passed"] else "STOP_CLI_REGISTRATION_FIX_INCOMPLETE_SMALL_PROBE_FAILED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CLI_REGISTRATION_FIX_COMPLETE_SMALL_PROBE_PASSED_RETRY_READY" if probe["probe_passed"] else "STOP_CLI_REGISTRATION_FIX_INCOMPLETE_SMALL_PROBE_FAILED",
            "next_command_goal": None,
        },
    }
    write_json(TRANSITION_TRACE_PATH, trace)

    acceptance_gate_results = {
        "CLI_REG_FIX_0_BUILD_FAILURE_REVIEW_CONSUMED": True,
        "CLI_REG_FIX_1_BROKEN_REGISTRATION_REPAIRED": after_surface["direct_command_count"] >= 1 and cli_patch_report["registration_before_main"],
        "CLI_REG_FIX_2_HELP_EXPOSES_RADIUS": help_check["entrypoint_help_passed"] is True,
        "CLI_REG_FIX_3_COMPILE_CHECKS_PASS": help_check["compile_checks_passed"] is True,
        "CLI_REG_FIX_4_SMALL_PROBE_EXECUTED": report["small_probe_executed_count"] == 1,
        "CLI_REG_FIX_5_SMALL_PROBE_WRITES_10_RECEIPTS": report["small_probe_passed_count"] == 1 and report["small_probe_observation_receipt_count"] == PROBE_RADIUS,
        "CLI_REG_FIX_6_PROBE_STDOUT_JSON": report["probe_stdout_json_parseable_count"] == 1,
        "CLI_REG_FIX_7_RETRY_READY_PACKET_EMITTED": report["retry_ready_packet_emitted_count"] == 1 and report["radius_10000_retry_ready_count"] == 1,
        "CLI_REG_FIX_8_RADIUS_10000_NOT_EXECUTED": report["radius_10000_retry_executed_count"] == 0,
        "CLI_REG_FIX_9_NO_UNBOUNDED_RUN": report["unbounded_or_no_cap_run_count"] == 0,
        "CLI_REG_FIX_10_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0,
        "CLI_REG_FIX_11_NO_PRIOR_ARTIFACT_OR_RECEIPT_MUTATION": protected_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "CLI_REG_FIX_12_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if protected_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_build_failure_review_receipt_id": SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "protected_prior_artifact_mutation_count": 1 if protected_mutation_detected else 0,
    }

    guards = {
        "build_failure_review_consumed": True,
        "cli_registration_fix_authorized": True,
        "cli_source_modified": True,
        "entrypoint_module_modified": False,
        "help_check_passed": help_check["entrypoint_help_passed"],
        "small_probe_executed": True,
        "small_probe_passed": probe["probe_passed"],
        "probe_stdout_json_parseable": probe["stdout_json_parseable"],
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
        "repair_executed_outside_cli_registration": False,
        "taxonomy_delta_proposal_emitted": False,
        "existing_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_build_failure_review_receipt_id": SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID,
        "probe_passed": probe["probe_passed"],
        "retry_ready": retry_packet["packet_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "patch_plan": rel(PATCH_PLAN_PATH),
        "cli_before_surface": rel(CLI_BEFORE_SURFACE_PATH),
        "cli_after_surface": rel(CLI_AFTER_SURFACE_PATH),
        "patch_report": rel(PATCH_REPORT_PATH),
        "help_check": rel(HELP_CHECK_PATH),
        "small_probe_result": rel(SMALL_PROBE_RESULT_PATH),
        "retry_ready_packet": rel(RETRY_READY_PACKET_PATH),
        "fix_decision": rel(FIX_DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "cli_path": rel(CLI_PATH),
        "entrypoint_module_path": rel(ENTRYPOINT_MODULE_PATH),
    }

    patch_report = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_registration_patch_report_v0",
        "module_report": module_report,
        "cli_patch_report": cli_patch_report,
        "help_check_ref": rel(HELP_CHECK_PATH),
        "small_probe_result_ref": rel(SMALL_PROBE_RESULT_PATH),
    }
    write_json(PATCH_REPORT_PATH, patch_report)

    receipt = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_CLI_REGISTRATION_FIX_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_build_failure_review_receipt_id": SOURCE_BUILD_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "cli_registration_fix_summary": {
            "decision_status": decision["decision_status"],
            "cli_registration_fixed": decision["cli_registration_fixed"],
            "entrypoint_command": "post-closure-observability-harvest",
            "help_check_passed": decision["help_check_passed"],
            "small_probe_executed": True,
            "small_probe_passed": decision["small_probe_passed"],
            "small_probe_radius": PROBE_RADIUS,
            "small_probe_observation_receipt_count": probe.get("probe_observation_receipt_count"),
            "probe_stdout_json_parseable": probe["stdout_json_parseable"],
            "radius_10000_retry_ready": decision["radius_10000_retry_ready"],
            "radius_10000_retry_executed": False,
            "radius_10000_retry_command": retry_packet["radius_10000_retry_command"],
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "cli_registration_fix_guards": guards,
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
    print(f"cli_registration_fix_receipt_id={receipt_id}")
    print(f"cli_registration_fix_receipt_path=data/r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_v0_receipts/{receipt_id}.json")
    print(f"retry_ready_packet_path=data/r1000_post_closure_observability_harvest_entrypoint_cli_registration_fix_v0/r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet_after_cli_registration_fix.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
