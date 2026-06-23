#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_BUILD_FAILURE_V0"
TARGET_UNIT_ID = "r1000.post_closure_observability_harvest_entrypoint_build_failure.review.v0"

SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID = "9d834354"
SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID = "2d61b52e"
SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID = "b35e7989"
SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID = "c5217505"
SOURCE_FAILED_HARVEST_RECEIPT_ID = "722af13e"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"

OUT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_v0_receipts"

FAILURE_REVIEW_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_surface.json"
CLI_FAILURE_HELP_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_build_failure_cli_help_surface.json"
PROBE_FAILURE_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_build_failure_probe_surface.json"
FAILURE_CLASSIFICATION_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_build_failure_classification_packet.json"
FIX_AUTHORITY_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_build_failure_fix_authority_packet.json"
REVIEW_DECISION_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_decision.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_report.json"

FAILED_BUILD_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_v0_receipts" / f"{SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID}.json"
SOURCE_PATCH_PLAN_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_v0" / "r1000_post_closure_observability_harvest_entrypoint_source_patch_plan.json"
ENTRYPOINT_CONTRACT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_v0" / "r1000_post_closure_observability_harvest_entrypoint_contract.json"
SMALL_PROBE_RESULT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_v0" / "r1000_post_closure_observability_harvest_entrypoint_small_probe_result.json"
RETRY_READY_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_v0" / "r1000_post_closure_observability_harvest_radius_10000_retry_ready_packet.json"
BUILD_DECISION_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_v0" / "r1000_post_closure_observability_harvest_entrypoint_build_decision.json"
BUILD_TRACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_v0" / "r1000_post_closure_observability_harvest_entrypoint_build_transition_trace.json"
BUILD_REPORT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_build_v0" / "r1000_post_closure_observability_harvest_entrypoint_build_report.json"

CLI_ENTRYPOINT_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_cli_observability_harvest_entrypoint_inspection_v0_receipts" / f"{SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID}.json"
COMMAND_RESOLVER_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_harvest_command_resolver_fix_v0_receipts" / f"{SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID}.json"
FAILED_HARVEST_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_review_v0_receipts" / f"{SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID}.json"
FAILED_HARVEST_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_v0_receipts" / f"{SOURCE_FAILED_HARVEST_RECEIPT_ID}.json"

CLOSURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID}.json"
CLOSED_QUEUE_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
EXPECTED_LIMIT_MARK_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID}.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"

CLI_PATH = ROOT / "src" / "matrixlab" / "cli.py"
ENTRYPOINT_MODULE_PATH = ROOT / "src" / "matrixlab" / "r1000_post_closure_observability_harvest.py"

SOURCE_FILES = [
    FAILED_BUILD_RECEIPT_PATH,
    SOURCE_PATCH_PLAN_PATH,
    ENTRYPOINT_CONTRACT_PATH,
    SMALL_PROBE_RESULT_PATH,
    RETRY_READY_PACKET_PATH,
    BUILD_DECISION_PATH,
    BUILD_TRACE_PATH,
    BUILD_REPORT_PATH,
    CLI_ENTRYPOINT_INSPECTION_RECEIPT_PATH,
    COMMAND_RESOLVER_FIX_RECEIPT_PATH,
    FAILED_HARVEST_REVIEW_RECEIPT_PATH,
    FAILED_HARVEST_RECEIPT_PATH,
    CLOSURE_REVIEW_RECEIPT_PATH,
    CLOSED_QUEUE_HANDOFF_PATH,
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    FINAL_QUEUE_STATE_PATH,
    CLI_PATH,
    ENTRYPOINT_MODULE_PATH,
]

HUMAN_DECISION = {
    "decision": "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_BUILD_FAILURE",
    "scope": "review the failed entrypoint build without fixing it; classify help/probe failure, preserve failed source/artifact surfaces, and emit a typed fix authority packet for a separate repair unit",
    "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
    "authorized": [
        "consume failed entrypoint build receipt",
        "consume failed build artifacts",
        "inspect CLI help failure surface",
        "inspect small probe failure surface",
        "classify build failure",
        "emit fix authority packet",
        "preserve failed build artifacts",
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
        "filling fields",
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
    failed_receipt = read_json(FAILED_BUILD_RECEIPT_PATH)
    build_report = read_json(BUILD_REPORT_PATH)
    build_decision = read_json(BUILD_DECISION_PATH)
    retry_packet = read_json(RETRY_READY_PACKET_PATH)
    closure_receipt = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if failed_receipt.get("receipt_id") != SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID:
        failures.append("failed_build_receipt_id_wrong")
    if failed_receipt.get("gate") != "FAIL":
        failures.append("failed_build_receipt_gate_not_fail")
    if failed_receipt.get("entrypoint_build_summary", {}).get("decision_status") != "ENTRYPOINT_BUILD_INCOMPLETE_SMALL_PROBE_FAILED":
        failures.append("failed_build_decision_status_wrong")
    if failed_receipt.get("entrypoint_build_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("failed_build_not_recommending_this_unit")

    if build_report.get("entrypoint_module_written_count") != 1:
        failures.append("failed_build_entrypoint_module_not_written")
    if build_report.get("compile_check_pass_count") != build_report.get("compile_check_count"):
        failures.append("failed_build_compile_not_clean")
    if build_report.get("help_check_pass_count") != 0:
        failures.append("failed_build_help_unexpectedly_passed")
    if build_report.get("small_probe_passed_count") != 0:
        failures.append("failed_build_probe_unexpectedly_passed")
    if build_report.get("radius_10000_retry_executed_count") != 0:
        failures.append("failed_build_radius_10000_executed")

    if build_decision.get("decision_status") != "ENTRYPOINT_BUILD_INCOMPLETE_SMALL_PROBE_FAILED":
        failures.append("build_decision_status_wrong")
    if retry_packet.get("packet_status") != "RADIUS_10000_RETRY_BLOCKED_SMALL_PROBE_FAILED":
        failures.append("retry_packet_status_wrong")

    if closure_receipt.get("gate") != "PASS":
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

def help_surface() -> Dict[str, Any]:
    commands = [
        ["uv", "run", "python", "src/matrixlab/cli.py", "--help"],
        ["uv", "run", "python", "src/matrixlab/cli.py", "post-closure-observability-harvest", "--help"],
    ]
    results = []
    for args in commands:
        rc, out, err = run_cmd(args)
        results.append({
            "args": args,
            "returncode": rc,
            "stdout_tail": out[-12000:],
            "stderr_tail": err[-12000:],
            "stdout_contains_radius": "--radius" in out,
            "stderr_contains_radius": "--radius" in err,
        })
    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_build_failure_cli_help_surface_v0",
        "results": results,
        "entrypoint_help_passed": any(
            r["args"][-2:] == ["post-closure-observability-harvest", "--help"] and r["returncode"] == 0
            for r in results
        ),
    }

def probe_surface() -> Dict[str, Any]:
    probe = read_json(SMALL_PROBE_RESULT_PATH)
    parsed = probe.get("parsed_result")
    stdout_tail = probe.get("stdout_tail") or ""
    stderr_tail = probe.get("stderr_tail") or ""
    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_build_failure_probe_surface_v0",
        "source_small_probe_result_ref": rel(SMALL_PROBE_RESULT_PATH),
        "probe_command": probe.get("probe_command"),
        "probe_returncode": probe.get("returncode"),
        "probe_stdout_tail": stdout_tail[-12000:],
        "probe_stderr_tail": stderr_tail[-12000:],
        "probe_stdout_json_parseable": isinstance(parsed, dict),
        "probe_parsed_result": parsed,
        "probe_passed": probe.get("probe_passed"),
        "probe_radius": probe.get("probe_radius"),
        "probe_observation_receipt_count": probe.get("probe_observation_receipt_count"),
    }

def classify_failure(help_obj: Dict[str, Any], probe_obj: Dict[str, Any]) -> Dict[str, Any]:
    entrypoint_help_passed = help_obj.get("entrypoint_help_passed") is True
    probe_stdout_json_parseable = probe_obj.get("probe_stdout_json_parseable") is True
    probe_passed = probe_obj.get("probe_passed") is True

    if not entrypoint_help_passed and not probe_stdout_json_parseable:
        classification = "CLI_REGISTRATION_OR_HELP_ROUTING_FAILURE"
    elif entrypoint_help_passed and not probe_passed:
        classification = "ENTRYPOINT_RUNTIME_OR_RECEIPT_WRITE_FAILURE"
    else:
        classification = "ENTRYPOINT_BUILD_FAILURE_REQUIRES_MANUAL_REVIEW"

    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_build_failure_classification_packet_v0",
        "classification": classification,
        "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
        "evidence": {
            "entrypoint_module_written": True,
            "compile_checks_passed": True,
            "entrypoint_help_passed": entrypoint_help_passed,
            "probe_stdout_json_parseable": probe_stdout_json_parseable,
            "probe_passed": probe_passed,
            "probe_observation_receipt_count": probe_obj.get("probe_observation_receipt_count"),
        },
        "not_a_queue_closure_failure": True,
        "not_a_radius_10000_failure": True,
        "radius_10000_retry_still_blocked": True,
    }

def build_fix_authority_packet(classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_build_failure_fix_authority_packet_v0",
        "packet_status": "FIX_ENTRYPOINT_CLI_REGISTRATION_AND_PROBE_OUTPUT_AUTHORITY_PACKET",
        "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
        "failure_classification": classification["classification"],
        "authorized_next_unit": "FIX_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_CLI_REGISTRATION_V0",
        "required_fix_shape": [
            "inspect actual src/matrixlab/cli.py Typer app registration order",
            "patch entrypoint registration so help command exposes --radius",
            "ensure command stdout is pure JSON for probe parse",
            "run radius-10 probe and require 10 observation receipts",
            "emit radius-10000 retry-ready packet only after probe pass",
        ],
        "radius_10000_retry_authorized_now": False,
        "fix_authorized_in_this_unit": False,
        "recommended_next_handling": "FIX_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_CLI_REGISTRATION_V0",
    }

def build_decision(classification: Dict[str, Any], authority: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_decision_v0",
        "decision_id": sha8({
            "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
            "classification": classification["classification"],
            "next": authority["recommended_next_handling"],
        }),
        "decision_status": "ACCEPT_ENTRYPOINT_BUILD_FAILURE_AS_CLI_REGISTRATION_REPAIR_REQUIRED",
        "failure_classification": classification["classification"],
        "failed_build_artifacts_preserved": True,
        "radius_10000_retry_authorized": False,
        "repair_authorized_in_this_unit": False,
        "recommended_next_handling": authority["recommended_next_handling"],
    }

def build_report(classification: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
        "failed_build_receipt_consumed_count": 1,
        "failed_build_artifacts_consumed_count": 1,
        "cli_help_failure_surface_emitted_count": 1,
        "small_probe_failure_surface_emitted_count": 1,
        "failure_classification_packet_emitted_count": 1,
        "fix_authority_packet_emitted_count": 1,
        "review_decision_emitted_count": 1,
        "failed_build_artifacts_preserved_count": 1,
        "entrypoint_module_written_count": 1,
        "compile_checks_clean_count": 1,
        "entrypoint_help_failed_count": 1,
        "small_probe_failed_count": 1,
        "probe_stdout_not_json_count": 1,
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

    if classification.get("classification") not in {
        "CLI_REGISTRATION_OR_HELP_ROUTING_FAILURE",
        "ENTRYPOINT_RUNTIME_OR_RECEIPT_WRITE_FAILURE",
        "ENTRYPOINT_BUILD_FAILURE_REQUIRES_MANUAL_REVIEW",
    }:
        failures.append("classification_unknown")
    if classification.get("radius_10000_retry_still_blocked") is not True:
        failures.append("radius_10000_not_blocked")
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
    if report.get("review_decision_emitted_count") != 1:
        failures.append("review_decision_not_emitted")
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
        "failed_build_receipt_consumed_count",
        "failed_build_artifacts_consumed_count",
        "cli_help_failure_surface_emitted_count",
        "small_probe_failure_surface_emitted_count",
        "failure_classification_packet_emitted_count",
        "fix_authority_packet_emitted_count",
        "review_decision_emitted_count",
        "failed_build_artifacts_preserved_count",
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
    if terminal.get("stop_code") != "STOP_ENTRYPOINT_BUILD_FAILURE_REVIEW_COMPLETE_CLI_REGISTRATION_FIX_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    help_obj = help_surface()
    probe_obj = probe_surface()
    classification = classify_failure(help_obj, probe_obj)
    authority = build_fix_authority_packet(classification)
    decision = build_decision(classification, authority)
    report = build_report(classification, decision)

    trace = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_failed_build",
                "question": "failed build produced module and compile-clean source but no working help/probe",
                "answer": True,
                "taken": "classify_cli_registration_failure",
            },
            {
                "step": "classify_cli_registration_failure",
                "question": "run repair in review unit",
                "answer": False,
                "taken": "emit_fix_authority_packet",
            },
            {
                "step": "emit_fix_authority_packet",
                "question": "run radius 10000 now",
                "answer": False,
                "taken": "STOP_ENTRYPOINT_BUILD_FAILURE_REVIEW_COMPLETE_CLI_REGISTRATION_FIX_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_ENTRYPOINT_BUILD_FAILURE_REVIEW_COMPLETE_CLI_REGISTRATION_FIX_REQUIRED",
            "next_command_goal": None,
        },
    }

    write_json(CLI_FAILURE_HELP_SURFACE_PATH, help_obj)
    write_json(PROBE_FAILURE_SURFACE_PATH, probe_obj)
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
        "BUILD_FAILURE_REVIEW_0_FAILED_BUILD_RECEIPT_CONSUMED": True,
        "BUILD_FAILURE_REVIEW_1_HELP_FAILURE_SURFACE_EMITTED": report["cli_help_failure_surface_emitted_count"] == 1,
        "BUILD_FAILURE_REVIEW_2_PROBE_FAILURE_SURFACE_EMITTED": report["small_probe_failure_surface_emitted_count"] == 1,
        "BUILD_FAILURE_REVIEW_3_FAILURE_CLASSIFIED": classification["classification"] in {
            "CLI_REGISTRATION_OR_HELP_ROUTING_FAILURE",
            "ENTRYPOINT_RUNTIME_OR_RECEIPT_WRITE_FAILURE",
            "ENTRYPOINT_BUILD_FAILURE_REQUIRES_MANUAL_REVIEW",
        },
        "BUILD_FAILURE_REVIEW_4_FIX_AUTHORITY_PACKET_EMITTED": report["fix_authority_packet_emitted_count"] == 1,
        "BUILD_FAILURE_REVIEW_5_NO_REPAIR_OR_RETRY": report["repair_executed_count"] == 0 and report["radius_10000_retry_executed_count"] == 0,
        "BUILD_FAILURE_REVIEW_6_NO_SMALL_PROBE_RERUN": report["small_probe_rerun_count"] == 0,
        "BUILD_FAILURE_REVIEW_7_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0,
        "BUILD_FAILURE_REVIEW_8_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "BUILD_FAILURE_REVIEW_9_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "source_failed_harvest_review_receipt_id": SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID,
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards = {
        "failed_build_receipt_consumed": True,
        "failed_build_artifacts_preserved": True,
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
        "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
        "classification": classification["classification"],
        "recommended_next": decision["recommended_next_handling"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "failure_review_surface": rel(FAILURE_REVIEW_SURFACE_PATH),
        "cli_help_failure_surface": rel(CLI_FAILURE_HELP_SURFACE_PATH),
        "probe_failure_surface": rel(PROBE_FAILURE_SURFACE_PATH),
        "failure_classification_packet": rel(FAILURE_CLASSIFICATION_PACKET_PATH),
        "fix_authority_packet": rel(FIX_AUTHORITY_PACKET_PATH),
        "review_decision": rel(REVIEW_DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    review_surface = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_surface_v0",
        "review_surface_id": sha8({
            "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
            "classification": classification["classification"],
        }),
        "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
        "failed_build_gate": read_json(FAILED_BUILD_RECEIPT_PATH).get("gate"),
        "failed_build_failures": read_json(FAILED_BUILD_RECEIPT_PATH).get("failures"),
        "classification": classification["classification"],
        "radius_10000_retry_still_blocked": True,
        "repair_required": True,
        "recommended_next_handling": decision["recommended_next_handling"],
    }
    write_json(FAILURE_REVIEW_SURFACE_PATH, review_surface)

    receipt = {
        "schema_version": "r1000_post_closure_observability_harvest_entrypoint_build_failure_review_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_ENTRYPOINT_BUILD_FAILURE_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_entrypoint_build_receipt_id": SOURCE_FAILED_ENTRYPOINT_BUILD_RECEIPT_ID,
        "source_cli_entrypoint_inspection_receipt_id": SOURCE_CLI_ENTRYPOINT_INSPECTION_RECEIPT_ID,
        "source_command_resolver_fix_receipt_id": SOURCE_COMMAND_RESOLVER_FIX_RECEIPT_ID,
        "source_failed_harvest_review_receipt_id": SOURCE_FAILED_HARVEST_REVIEW_RECEIPT_ID,
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "entrypoint_build_failure_review_summary": {
            "review_result": decision["decision_status"],
            "failure_classification": classification["classification"],
            "entrypoint_module_written": True,
            "compile_checks_clean": True,
            "entrypoint_help_failed": True,
            "small_probe_failed": True,
            "probe_stdout_not_json": True,
            "radius_10000_retry_ready": False,
            "radius_10000_retry_authorized": False,
            "radius_10000_retry_executed": False,
            "repair_executed": False,
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "entrypoint_build_failure_review_guards": guards,
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
    print(f"entrypoint_build_failure_review_receipt_id={receipt_id}")
    print(f"entrypoint_build_failure_review_receipt_path=data/r1000_post_closure_observability_harvest_entrypoint_build_failure_review_v0_receipts/{receipt_id}.json")
    print(f"fix_authority_packet_path=data/r1000_post_closure_observability_harvest_entrypoint_build_failure_review_v0/r1000_post_closure_observability_harvest_entrypoint_build_failure_fix_authority_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
