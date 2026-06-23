#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_V0"
TARGET_UNIT_ID = "r1000.post_closure_observability_harvest.radius_10000.review.v0"

SOURCE_FAILED_HARVEST_RECEIPT_ID = "722af13e"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"
HARVEST_RADIUS = 10000

FAILED_HARVEST_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_v0_receipts" / f"{SOURCE_FAILED_HARVEST_RECEIPT_ID}.json"
FAILED_HARVEST_ROLLUP_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_v0" / "r1000_post_closure_observability_harvest_radius_10000_rollup.json"
FAILED_HARVEST_FAILURE_GALLERY_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_v0" / "r1000_post_closure_observability_harvest_radius_10000_failure_gallery.json"
FAILED_HARVEST_RUN_LOG_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_v0" / "r1000_post_closure_observability_harvest_radius_10000_run.log"
FAILED_HARVEST_STDERR_LOG_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_v0" / "r1000_post_closure_observability_harvest_radius_10000_stderr.log"
FAILED_HARVEST_RECEIPT_INDEX_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_v0" / "r1000_post_closure_observability_harvest_radius_10000_receipt_index.jsonl"
FAILED_HARVEST_HALT_HISTOGRAM_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_v0" / "r1000_post_closure_observability_harvest_radius_10000_halt_histogram.json"

CLOSURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID}.json"
CLOSED_QUEUE_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
EXPECTED_LIMIT_MARK_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID}.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"
CLI_PATH = ROOT / "src" / "matrixlab" / "cli.py"

OUT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_review_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_review_v0_receipts"

FAILED_HARVEST_REVIEW_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_failed_review_surface.json"
CLI_HELP_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_cli_help_surface.json"
COMMAND_RESOLVER_DEFECT_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_command_resolver_defect_packet.json"
RETRY_AUTHORITY_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_retry_authority_packet.json"
REVIEW_DECISION_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_review_decision.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_review_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_review_report.json"

SOURCE_FILES = [
    FAILED_HARVEST_RECEIPT_PATH,
    FAILED_HARVEST_ROLLUP_PATH,
    FAILED_HARVEST_FAILURE_GALLERY_PATH,
    FAILED_HARVEST_RUN_LOG_PATH,
    FAILED_HARVEST_STDERR_LOG_PATH,
    FAILED_HARVEST_RECEIPT_INDEX_PATH,
    FAILED_HARVEST_HALT_HISTOGRAM_PATH,
    CLOSURE_REVIEW_RECEIPT_PATH,
    CLOSED_QUEUE_HANDOFF_PATH,
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    FINAL_QUEUE_STATE_PATH,
    CLI_PATH,
]

HUMAN_DECISION = {
    "decision": "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000",
    "scope": "review the failed bounded radius-10000 post-closure observability harvest, classify whether the failure was semantic or command-interface/capability, preserve diagnostic artifacts, inspect CLI help surface, and emit a typed retry authority packet without rerunning the 10k harvest",
    "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
    "authorized": [
        "consume failed harvest receipt and diagnostics",
        "consume closed queue handoff",
        "inspect CLI help surface",
        "classify harvest command resolver failure",
        "emit defect packet",
        "emit retry authority packet",
        "preserve failed diagnostic artifacts",
        "stop before rerun",
    ],
    "not_authorized": [
        "rerunning radius-10000 harvest",
        "running unbounded/no-cap harvest",
        "reopening R1000 pressure queue",
        "inspecting closed groups",
        "materializing row payloads",
        "assigning identity values",
        "inventing values",
        "filling fields",
        "running repair",
        "applying taxonomy changes",
        "mutating source artifacts",
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

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_sources() -> List[str]:
    failures: List[str] = []
    failed_receipt = read_json(FAILED_HARVEST_RECEIPT_PATH)
    rollup = read_json(FAILED_HARVEST_ROLLUP_PATH)
    closure_receipt = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if failed_receipt.get("receipt_id") != SOURCE_FAILED_HARVEST_RECEIPT_ID:
        failures.append("failed_harvest_receipt_id_wrong")
    if failed_receipt.get("gate") != "FAIL":
        failures.append("failed_harvest_gate_not_fail")
    if failed_receipt.get("aggregate_metrics", {}).get("harvest_command_resolved_count") != 0:
        failures.append("failed_harvest_command_unexpectedly_resolved")
    if failed_receipt.get("aggregate_metrics", {}).get("new_receipt_count") != 0:
        failures.append("failed_harvest_produced_new_receipts")
    if failed_receipt.get("aggregate_metrics", {}).get("source_mutation_count") != 0:
        failures.append("failed_harvest_mutated_source")
    if failed_receipt.get("aggregate_metrics", {}).get("hidden_next_command_count") != 0:
        failures.append("failed_harvest_hidden_next")

    if rollup.get("harvest_command_resolved") is not False:
        failures.append("rollup_harvest_command_resolved_not_false")
    if rollup.get("new_receipt_count") != 0:
        failures.append("rollup_new_receipt_count_not_zero")
    if rollup.get("source_pressure_queue_closed") is not True:
        failures.append("rollup_source_queue_not_closed")

    if closure_receipt.get("receipt_id") != SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID:
        failures.append("closure_review_receipt_id_wrong")
    if closure_receipt.get("gate") != "PASS":
        failures.append("closure_review_not_pass")
    if closure_receipt.get("pressure_queue_closure_review_summary", {}).get("queue_closed") is not True:
        failures.append("closure_review_queue_not_closed")

    if handoff.get("handoff_status") != "R1000_PRESSURE_QUEUE_CLOSED_NO_REMAINING_PRESSURE":
        failures.append("handoff_status_wrong")
    if handoff.get("recommended_next_handling") is not None:
        failures.append("handoff_recommended_next_not_null")

    if final_queue.get("queue_state_status") != "R1000_PRESSURE_QUEUE_CLOSED":
        failures.append("final_queue_status_wrong")
    if final_queue.get("remaining_open_group_count") != 0:
        failures.append("final_queue_remaining_groups_not_zero")
    if final_queue.get("remaining_open_row_count") != 0:
        failures.append("final_queue_remaining_rows_not_zero")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")

    return failures

def collect_cli_help_surface() -> Dict[str, Any]:
    commands = [
        ["uv", "run", "python", "src/matrixlab/cli.py", "--help"],
        ["uv", "run", "python", "src/matrixlab/cli.py", "run", "--help"],
        ["uv", "run", "python", "src/matrixlab/cli.py", "gate", "--help"],
    ]
    help_results = []
    for args in commands:
        try:
            rc, out, err = run_cmd(args)
            help_results.append({
                "args": args,
                "returncode": rc,
                "stdout_tail": out[-12000:],
                "stderr_tail": err[-4000:],
            })
        except Exception as exc:
            help_results.append({
                "args": args,
                "exception_type": type(exc).__name__,
                "exception_message": str(exc),
            })

    text = "\n".join((item.get("stdout_tail") or "") + "\n" + (item.get("stderr_tail") or "") for item in help_results)
    lower = text.lower()

    likely_radius_terms = {
        "radius": "radius" in lower,
        "cycle": "cycle" in lower,
        "cycles": "cycles" in lower,
        "run": "run" in lower,
        "batch": "batch" in lower,
        "receipt": "receipt" in lower,
        "gate": "gate" in lower,
        "range": "range" in lower,
        "limit": "limit" in lower,
    }

    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_cli_help_surface_v0",
        "cli_path": rel(CLI_PATH),
        "help_results": help_results,
        "likely_radius_terms": likely_radius_terms,
        "cli_help_surface_materialized": True,
    }

def classify_failed_harvest(failed_receipt: Dict[str, Any], rollup: Dict[str, Any], failure_gallery: Dict[str, Any], cli_help: Dict[str, Any]) -> Dict[str, Any]:
    harvest_command_unresolved = rollup.get("harvest_command_resolved") is False
    no_new_receipts = rollup.get("new_receipt_count") == 0
    gate_latest_pass = rollup.get("gate_latest_pass") is True
    source_clean = rollup.get("source_mutation_count") == 0
    hidden_next_clean = rollup.get("hidden_next_command_count") == 0

    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_failed_review_surface_v0",
        "review_surface_id": sha8({
            "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
            "harvest_command_resolved": rollup.get("harvest_command_resolved"),
            "new_receipt_count": rollup.get("new_receipt_count"),
            "failure_count": rollup.get("failure_count"),
        }),
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "failed_harvest_gate": failed_receipt.get("gate"),
        "failed_harvest_terminal": failed_receipt.get("terminal"),
        "radius_requested": rollup.get("radius_requested"),
        "bounded": rollup.get("bounded"),
        "harvest_command_resolved": rollup.get("harvest_command_resolved"),
        "new_receipt_count": rollup.get("new_receipt_count"),
        "receipt_count_before": rollup.get("receipt_count_before"),
        "receipt_count_after": rollup.get("receipt_count_after"),
        "failure_count": rollup.get("failure_count"),
        "unique_halt_count": rollup.get("unique_halt_count"),
        "gate_latest_pass": rollup.get("gate_latest_pass"),
        "source_mutation_count": rollup.get("source_mutation_count"),
        "hidden_next_command_count": rollup.get("hidden_next_command_count"),
        "failure_gallery_failure_count": failure_gallery.get("failure_count"),
        "classification": "COMMAND_INTERFACE_CAPABILITY_FAILURE_NOT_SEMANTIC_QUEUE_FAILURE" if harvest_command_unresolved and no_new_receipts and gate_latest_pass and source_clean and hidden_next_clean else "REQUIRES_DEEPER_REVIEW",
        "queue_closure_still_valid": gate_latest_pass and source_clean,
        "rerun_authorized_in_this_unit": False,
        "retry_requires_resolved_entrypoint": True,
    }

def build_defect_packet(surface: Dict[str, Any], cli_help: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_command_resolver_defect_packet_v0",
        "packet_status": "COMMAND_RESOLVER_DEFECT_CLASSIFIED",
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "defect_type": "HARVEST_COMMAND_INTERFACE_UNRESOLVED",
        "defect_class": surface["classification"],
        "evidence": {
            "harvest_command_resolved": surface["harvest_command_resolved"],
            "new_receipt_count": surface["new_receipt_count"],
            "gate_latest_pass": surface["gate_latest_pass"],
            "source_mutation_count": surface["source_mutation_count"],
            "hidden_next_command_count": surface["hidden_next_command_count"],
            "cli_help_surface_materialized": cli_help["cli_help_surface_materialized"],
            "likely_radius_terms": cli_help["likely_radius_terms"],
        },
        "not_a_queue_closure_failure": surface["queue_closure_still_valid"],
        "not_a_radius_failure": surface["new_receipt_count"] == 0,
        "requires_entrypoint_resolution": True,
    }

def choose_retry_recommendation(cli_help: Dict[str, Any]) -> str:
    terms = cli_help.get("likely_radius_terms", {})
    if terms.get("run") and (terms.get("cycles") or terms.get("radius") or terms.get("limit")):
        return "FIX_R1000_POST_CLOSURE_HARVEST_COMMAND_RESOLVER_FROM_CLI_HELP_V0"
    return "INSPECT_MATRIXLAB_CLI_FOR_OBSERVABILITY_HARVEST_ENTRYPOINT_V0"

def build_retry_authority_packet(surface: Dict[str, Any], cli_help: Dict[str, Any]) -> Dict[str, Any]:
    recommended = choose_retry_recommendation(cli_help)
    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_retry_authority_packet_v0",
        "packet_status": "RETRY_BLOCKED_UNTIL_ENTRYPOINT_RESOLVED",
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "radius_requested": HARVEST_RADIUS,
        "queue_closure_still_valid": surface["queue_closure_still_valid"],
        "rerun_authorized_in_this_unit": False,
        "retry_authorized_now": False,
        "required_before_retry": [
            "resolve actual MatrixLab CLI entrypoint or existing script for high-radius receipt harvest",
            "prove command writes receipts in a small probe",
            "then retry radius 10000 with fixed resolver",
        ],
        "allowed_next_unit": recommended,
        "recommended_next_handling": recommended,
    }

def build_review_decision(surface: Dict[str, Any], defect_packet: Dict[str, Any], retry_packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_review_decision_v0",
        "review_decision_id": sha8({
            "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
            "classification": surface["classification"],
            "recommended_next": retry_packet["recommended_next_handling"],
        }),
        "decision_status": "ACCEPT_FAILURE_AS_COMMAND_INTERFACE_DEFECT_RETRY_BLOCKED",
        "source_failed_review_surface_ref": rel(FAILED_HARVEST_REVIEW_SURFACE_PATH),
        "source_command_resolver_defect_packet_ref": rel(COMMAND_RESOLVER_DEFECT_PACKET_PATH),
        "queue_closure_still_valid": surface["queue_closure_still_valid"],
        "failed_harvest_semantic_rejection": False,
        "failed_harvest_collected_new_receipts": False,
        "failure_artifacts_preserved": True,
        "rerun_authorized_in_this_unit": False,
        "recommended_next_handling": retry_packet["recommended_next_handling"],
    }

def build_transition_trace(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_failed_harvest_receipt",
                "question": "failed harvest receipt exists and records command unresolved",
                "answer": True,
                "taken": "classify_command_interface_defect",
            },
            {
                "step": "classify_command_interface_defect",
                "question": "failure was semantic queue closure failure",
                "answer": False,
                "taken": "inspect_cli_help_surface",
            },
            {
                "step": "inspect_cli_help_surface",
                "question": "rerun radius 10000 in this unit",
                "answer": False,
                "taken": "emit_retry_authority_packet",
            },
            {
                "step": "emit_retry_authority_packet",
                "question": "hidden next command allowed",
                "answer": False,
                "taken": "STOP_POST_CLOSURE_HARVEST_REVIEW_COMPLETE_COMMAND_RESOLVER_FIX_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_POST_CLOSURE_HARVEST_REVIEW_COMPLETE_COMMAND_RESOLVER_FIX_REQUIRED",
            "next_command_goal": None,
        },
    }

def build_report(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "failed_harvest_receipt_consumed_count": 1,
        "failed_harvest_rollup_consumed_count": 1,
        "failed_harvest_failure_gallery_consumed_count": 1,
        "cli_help_surface_materialized_count": 1,
        "failed_harvest_review_surface_emitted_count": 1,
        "command_resolver_defect_packet_emitted_count": 1,
        "retry_authority_packet_emitted_count": 1,
        "review_decision_emitted_count": 1,
        "failure_artifacts_preserved_count": 1,
        "command_interface_failure_classified_count": 1 if surface["classification"] == "COMMAND_INTERFACE_CAPABILITY_FAILURE_NOT_SEMANTIC_QUEUE_FAILURE" else 0,
        "queue_closure_still_valid_count": 1 if surface["queue_closure_still_valid"] else 0,
        "failed_harvest_new_receipt_count": surface["new_receipt_count"],
        "failed_harvest_failure_count": surface["failure_count"],
        "failed_harvest_unique_halt_count": surface["unique_halt_count"],
        "harvest_command_resolved_count": 1 if surface["harvest_command_resolved"] else 0,
        "rerun_executed_count": 0,
        "radius_10000_retry_executed_count": 0,
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

def validate_outputs(surface: Dict[str, Any], defect: Dict[str, Any], retry: Dict[str, Any], decision: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if surface.get("classification") != "COMMAND_INTERFACE_CAPABILITY_FAILURE_NOT_SEMANTIC_QUEUE_FAILURE":
        failures.append("classification_not_command_interface")
    if surface.get("queue_closure_still_valid") is not True:
        failures.append("queue_closure_not_valid")
    if defect.get("packet_status") != "COMMAND_RESOLVER_DEFECT_CLASSIFIED":
        failures.append("defect_packet_status_wrong")
    if defect.get("not_a_radius_failure") is not True:
        failures.append("defect_not_a_radius_failure_false")
    if retry.get("retry_authorized_now") is not False:
        failures.append("retry_authorized_now")
    if decision.get("decision_status") != "ACCEPT_FAILURE_AS_COMMAND_INTERFACE_DEFECT_RETRY_BLOCKED":
        failures.append("decision_status_wrong")
    if decision.get("rerun_authorized_in_this_unit") is not False:
        failures.append("decision_rerun_authorized")
    if report.get("command_interface_failure_classified_count") != 1:
        failures.append("command_interface_failure_classified_count_wrong")
    if report.get("queue_closure_still_valid_count") != 1:
        failures.append("queue_closure_still_valid_count_wrong")
    if report.get("failed_harvest_new_receipt_count") != 0:
        failures.append("failed_harvest_new_receipt_count_not_zero")

    for key in [
        "rerun_executed_count",
        "radius_10000_retry_executed_count",
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

    if report.get("recommended_next_handling") not in {
        "FIX_R1000_POST_CLOSURE_HARVEST_COMMAND_RESOLVER_FROM_CLI_HELP_V0",
        "INSPECT_MATRIXLAB_CLI_FOR_OBSERVABILITY_HARVEST_ENTRYPOINT_V0",
    }:
        failures.append("recommended_next_unexpected")

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
        "failed_harvest_receipt_consumed_count",
        "failed_harvest_rollup_consumed_count",
        "failed_harvest_failure_gallery_consumed_count",
        "cli_help_surface_materialized_count",
        "failed_harvest_review_surface_emitted_count",
        "command_resolver_defect_packet_emitted_count",
        "retry_authority_packet_emitted_count",
        "review_decision_emitted_count",
        "failure_artifacts_preserved_count",
        "command_interface_failure_classified_count",
        "queue_closure_still_valid_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    for key in [
        "rerun_executed_count",
        "radius_10000_retry_executed_count",
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
    if terminal.get("stop_code") != "STOP_POST_CLOSURE_HARVEST_REVIEW_COMPLETE_COMMAND_RESOLVER_FIX_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    failed_receipt = read_json(FAILED_HARVEST_RECEIPT_PATH)
    rollup = read_json(FAILED_HARVEST_ROLLUP_PATH)
    failure_gallery = read_json(FAILED_HARVEST_FAILURE_GALLERY_PATH)

    cli_help = collect_cli_help_surface()
    surface = classify_failed_harvest(failed_receipt, rollup, failure_gallery, cli_help)
    defect = build_defect_packet(surface, cli_help)
    retry = build_retry_authority_packet(surface, cli_help)
    decision = build_review_decision(surface, defect, retry)
    trace = build_transition_trace(decision)
    report = build_report(surface, decision)

    write_json(CLI_HELP_SURFACE_PATH, cli_help)
    write_json(FAILED_HARVEST_REVIEW_SURFACE_PATH, surface)
    write_json(COMMAND_RESOLVER_DEFECT_PACKET_PATH, defect)
    write_json(RETRY_AUTHORITY_PACKET_PATH, retry)
    write_json(REVIEW_DECISION_PATH, decision)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(surface, defect, retry, decision, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "FAILED_HARVEST_REVIEW_0_FAILED_RECEIPT_CONSUMED": failed_receipt.get("receipt_id") == SOURCE_FAILED_HARVEST_RECEIPT_ID and failed_receipt.get("gate") == "FAIL",
        "FAILED_HARVEST_REVIEW_1_COMMAND_INTERFACE_FAILURE_CLASSIFIED": surface["classification"] == "COMMAND_INTERFACE_CAPABILITY_FAILURE_NOT_SEMANTIC_QUEUE_FAILURE",
        "FAILED_HARVEST_REVIEW_2_QUEUE_CLOSURE_STILL_VALID": surface["queue_closure_still_valid"] is True,
        "FAILED_HARVEST_REVIEW_3_CLI_HELP_SURFACE_MATERIALIZED": cli_help["cli_help_surface_materialized"] is True,
        "FAILED_HARVEST_REVIEW_4_RETRY_BLOCKED_UNTIL_ENTRYPOINT_RESOLVED": retry["retry_authorized_now"] is False and report["rerun_executed_count"] == 0,
        "FAILED_HARVEST_REVIEW_5_FAILURE_ARTIFACTS_PRESERVED": report["failure_artifacts_preserved_count"] == 1,
        "FAILED_HARVEST_REVIEW_6_NO_RERUN_OR_QUEUE_REOPEN": report["rerun_executed_count"] == 0 and report["queue_reopened_count"] == 0,
        "FAILED_HARVEST_REVIEW_7_NO_ROW_PAYLOAD_REPAIR_TAXONOMY": report["row_payload_materialized_count"] == 0 and report["repair_executed_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "FAILED_HARVEST_REVIEW_8_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "FAILED_HARVEST_REVIEW_9_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else 0,
    }

    guards = {
        "failed_harvest_receipt_consumed": True,
        "failed_harvest_gate_fail_confirmed": True,
        "command_interface_failure_classified": surface["classification"] == "COMMAND_INTERFACE_CAPABILITY_FAILURE_NOT_SEMANTIC_QUEUE_FAILURE",
        "queue_closure_still_valid": surface["queue_closure_still_valid"],
        "cli_help_surface_materialized": True,
        "retry_authorized_now": False,
        "rerun_executed": False,
        "queue_reopened": False,
        "closed_group_inspected": False,
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "identity_assignment": False,
        "field_value_invention": False,
        "repair_executed": False,
        "taxonomy_delta_proposal_emitted": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "decision": decision["decision_status"],
        "recommended_next": decision["recommended_next_handling"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "failed_harvest_review_surface": rel(FAILED_HARVEST_REVIEW_SURFACE_PATH),
        "cli_help_surface": rel(CLI_HELP_SURFACE_PATH),
        "command_resolver_defect_packet": rel(COMMAND_RESOLVER_DEFECT_PACKET_PATH),
        "retry_authority_packet": rel(RETRY_AUTHORITY_PACKET_PATH),
        "review_decision": rel(REVIEW_DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_review_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_harvest_receipt_id": SOURCE_FAILED_HARVEST_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "failed_harvest_review_summary": {
            "review_result": decision["decision_status"],
            "failure_classification": surface["classification"],
            "failed_harvest_gate": failed_receipt.get("gate"),
            "failed_harvest_terminal": failed_receipt.get("terminal"),
            "radius_requested": HARVEST_RADIUS,
            "harvest_command_resolved": surface["harvest_command_resolved"],
            "new_receipt_count": surface["new_receipt_count"],
            "failed_harvest_failure_count": surface["failure_count"],
            "queue_closure_still_valid": surface["queue_closure_still_valid"],
            "rerun_executed": False,
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "failed_harvest_review_guards": guards,
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
    print(f"failed_harvest_review_receipt_id={receipt_id}")
    print(f"failed_harvest_review_receipt_path=data/r1000_post_closure_observability_harvest_radius_10000_review_v0_receipts/{receipt_id}.json")
    print(f"retry_authority_packet_path=data/r1000_post_closure_observability_harvest_radius_10000_review_v0/r1000_post_closure_observability_harvest_radius_10000_retry_authority_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
