#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RESULT_V0"
TARGET_UNIT_ID = "r1000.post_closure_observability_harvest.radius_10000_result.review.v0"

SOURCE_RADIUS_10000_RETRY_RECEIPT_ID = "bb2c8ce3"
SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID = "02711ff1"
SOURCE_CLI_WRAPPER_FIX_FAILURE_REVIEW_RECEIPT_ID = "a7e5b8e3"
SOURCE_FAILED_CLI_WRAPPER_FIX_RECEIPT_ID = "c7204f69"
SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID = "6f7051cc"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"

EXPECTED_RADIUS = 10000
RUN_ID = "run_6b1b2494"

OUT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_result_review_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_result_review_v0_receipts"

RESULT_REVIEW_SURFACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_result_review_surface.json"
RUN_ARTIFACT_AUDIT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_result_run_artifact_audit.json"
OBSERVATION_RECEIPT_PROFILE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_observation_receipt_profile.json"
BOUNDARY_GUARD_REVIEW_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_boundary_guard_review.json"
RESULT_CLASSIFICATION_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_result_classification_packet.json"
NEXT_STATUS_PACKET_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_result_review_next_status_packet.json"
REVIEW_DECISION_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_result_review_decision.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_result_review_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_post_closure_observability_harvest_radius_10000_result_review_report.json"

RETRY_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0_receipts" / f"{SOURCE_RADIUS_10000_RETRY_RECEIPT_ID}.json"
RETRY_PLAN_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0" / "r1000_post_closure_observability_harvest_radius_10000_retry_plan.json"
SOURCE_PROOF_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0" / "r1000_post_closure_observability_harvest_radius_10000_retry_source_proof_surface.json"
COMMAND_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0" / "r1000_post_closure_observability_harvest_radius_10000_retry_command_surface.json"
RUN_RESULT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0" / "r1000_post_closure_observability_harvest_radius_10000_retry_run_result.json"
RUN_AUDIT_SOURCE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0" / "r1000_post_closure_observability_harvest_radius_10000_retry_run_audit.json"
RETRY_DECISION_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0" / "r1000_post_closure_observability_harvest_radius_10000_retry_decision.json"
RETRY_TRACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0" / "r1000_post_closure_observability_harvest_radius_10000_retry_transition_trace.json"
RETRY_REPORT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0" / "r1000_post_closure_observability_harvest_radius_10000_retry_report.json"
RETRY_NEXT_STATUS_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0" / "r1000_post_closure_observability_harvest_radius_10000_retry_next_status_packet.json"

RUN_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_runs_v0" / RUN_ID
OBS_RECEIPT_DIR = RUN_DIR / "receipts"
RUN_RECEIPT_PATH = RUN_DIR / "run_receipt.json"
ROLLUP_PATH = RUN_DIR / "rollup.json"
RECEIPT_INDEX_PATH = RUN_DIR / "receipt_index.jsonl"

CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_intercept_parse_fix_v0_receipts" / f"{SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID}.json"
CLI_WRAPPER_FIX_FAILURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_failure_review_v0_receipts" / f"{SOURCE_CLI_WRAPPER_FIX_FAILURE_REVIEW_RECEIPT_ID}.json"
FAILED_CLI_WRAPPER_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_runtime_output_fix_v0_receipts" / f"{SOURCE_FAILED_CLI_WRAPPER_FIX_RECEIPT_ID}.json"
CLI_WRAPPER_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_module_runtime_precondition_fix_failure_review_v0_receipts" / f"{SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID}.json"
CLOSURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID}.json"
CLOSED_QUEUE_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
EXPECTED_LIMIT_MARK_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID}.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"

CLI_PATH = ROOT / "src" / "matrixlab" / "cli.py"
ENTRYPOINT_MODULE_PATH = ROOT / "src" / "matrixlab" / "r1000_post_closure_observability_harvest.py"

SOURCE_FILES = [
    RETRY_RECEIPT_PATH,
    RETRY_PLAN_PATH,
    SOURCE_PROOF_SURFACE_PATH,
    COMMAND_SURFACE_PATH,
    RUN_RESULT_PATH,
    RUN_AUDIT_SOURCE_PATH,
    RETRY_DECISION_PATH,
    RETRY_TRACE_PATH,
    RETRY_REPORT_PATH,
    RETRY_NEXT_STATUS_PATH,
    RUN_RECEIPT_PATH,
    ROLLUP_PATH,
    RECEIPT_INDEX_PATH,
    CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_PATH,
    CLI_WRAPPER_FIX_FAILURE_REVIEW_RECEIPT_PATH,
    FAILED_CLI_WRAPPER_FIX_RECEIPT_PATH,
    CLI_WRAPPER_REVIEW_RECEIPT_PATH,
    CLOSURE_REVIEW_RECEIPT_PATH,
    CLOSED_QUEUE_HANDOFF_PATH,
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    FINAL_QUEUE_STATE_PATH,
    CLI_PATH,
    ENTRYPOINT_MODULE_PATH,
]

HUMAN_DECISION = {
    "decision": "REVIEW_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RESULT",
    "scope": "review the completed radius-10000 post-closure observability harvest result without rerunning it or repairing anything; classify the result, audit artifacts, preserve boundary guards, and produce a next-status packet for human/strategy selection",
    "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
    "authorized": [
        "consume radius-10000 retry receipt",
        "consume run receipt, rollup, receipt index, and existing observation receipt files",
        "audit artifact counts and sample parseability without mutation",
        "classify the radius-10000 result",
        "emit review decision and next-status packet",
        "stop before any further run",
    ],
    "not_authorized": [
        "rerunning radius-10000",
        "running radius above 10000",
        "running unbounded/no-cap harvest",
        "running any small probe",
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

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_sources() -> List[str]:
    failures: List[str] = []

    retry = read_json(RETRY_RECEIPT_PATH)
    run_receipt = read_json(RUN_RECEIPT_PATH)
    rollup = read_json(ROLLUP_PATH)
    retry_report = read_json(RETRY_REPORT_PATH)
    retry_decision = read_json(RETRY_DECISION_PATH)
    retry_next = read_json(RETRY_NEXT_STATUS_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if retry.get("receipt_id") != SOURCE_RADIUS_10000_RETRY_RECEIPT_ID:
        failures.append("radius_10000_retry_receipt_id_wrong")
    if retry.get("gate") != "PASS":
        failures.append("radius_10000_retry_gate_not_pass")
    if retry.get("radius_10000_retry_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("radius_10000_retry_not_recommending_this_review")
    if retry.get("radius_10000_retry_summary", {}).get("observation_receipt_count") != EXPECTED_RADIUS:
        failures.append("retry_receipt_observation_count_not_10000")
    if retry.get("radius_10000_retry_summary", {}).get("observation_receipt_files_count") != EXPECTED_RADIUS:
        failures.append("retry_receipt_file_count_not_10000")
    if retry_report.get("radius_10000_retry_passed_count") != 1:
        failures.append("retry_report_pass_count_not_1")
    if retry_decision.get("decision_status") != "RADIUS_10000_POST_CLOSURE_OBSERVABILITY_HARVEST_RETRY_COMPLETE":
        failures.append("retry_decision_not_complete")
    if retry_next.get("packet_status") != "RADIUS_10000_RETRY_COMPLETE_REVIEW_READY":
        failures.append("retry_next_status_not_review_ready")

    if run_receipt.get("gate") != "PASS":
        failures.append("run_receipt_gate_not_pass")
    if run_receipt.get("radius_requested") != EXPECTED_RADIUS or run_receipt.get("radius_completed") != EXPECTED_RADIUS:
        failures.append("run_receipt_radius_not_10000")
    if run_receipt.get("observation_receipt_count") != EXPECTED_RADIUS:
        failures.append("run_receipt_count_not_10000")

    if rollup.get("gate") != "PASS":
        failures.append("rollup_gate_not_pass")
    if rollup.get("radius_completed") != EXPECTED_RADIUS or rollup.get("observation_receipt_count") != EXPECTED_RADIUS:
        failures.append("rollup_radius_or_count_not_10000")

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
    if not OBS_RECEIPT_DIR.exists():
        failures.append(f"source_missing:{rel(OBS_RECEIPT_DIR)}")

    return failures

def audit_run_artifacts() -> Dict[str, Any]:
    receipt_files = sorted(OBS_RECEIPT_DIR.glob("*.json"))
    first_sample = receipt_files[:5]
    last_sample = receipt_files[-5:] if len(receipt_files) >= 5 else receipt_files
    middle_sample = []
    if len(receipt_files) >= EXPECTED_RADIUS:
        middle_sample = [receipt_files[EXPECTED_RADIUS // 2]]

    sample_files = []
    seen = set()
    for p in first_sample + middle_sample + last_sample:
        if p not in seen:
            sample_files.append(p)
            seen.add(p)

    sample_records = []
    parseable = []
    gate_pass = []
    indices = []
    for p in sample_files:
        try:
            obj = read_json(p)
            parseable.append(True)
            gate_pass.append(obj.get("gate") == "PASS")
            indices.append(obj.get("observation_index"))
            sample_records.append({
                "path": rel(p),
                "sha256": file_sha256(p),
                "gate": obj.get("gate"),
                "observation_index": obj.get("observation_index"),
                "radius_requested": obj.get("radius_requested"),
                "run_id": obj.get("run_id"),
                "terminal": obj.get("terminal"),
            })
        except Exception as exc:
            parseable.append(False)
            gate_pass.append(False)
            sample_records.append({
                "path": rel(p),
                "error": f"{type(exc).__name__}:{exc}",
            })

    index_line_count = 0
    if RECEIPT_INDEX_PATH.exists():
        with RECEIPT_INDEX_PATH.open("r", encoding="utf-8") as fh:
            for _ in fh:
                index_line_count += 1

    run_receipt = read_json(RUN_RECEIPT_PATH)
    rollup = read_json(ROLLUP_PATH)

    audit = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_result_run_artifact_audit_v0",
        "run_id": RUN_ID,
        "run_dir": rel(RUN_DIR),
        "run_dir_exists": RUN_DIR.exists(),
        "run_receipt_path": rel(RUN_RECEIPT_PATH),
        "run_receipt_sha256": file_sha256(RUN_RECEIPT_PATH),
        "run_receipt_gate": run_receipt.get("gate"),
        "run_receipt_radius_requested": run_receipt.get("radius_requested"),
        "run_receipt_radius_completed": run_receipt.get("radius_completed"),
        "run_receipt_observation_receipt_count": run_receipt.get("observation_receipt_count"),
        "rollup_path": rel(ROLLUP_PATH),
        "rollup_sha256": file_sha256(ROLLUP_PATH),
        "rollup_gate": rollup.get("gate"),
        "rollup_radius_completed": rollup.get("radius_completed"),
        "rollup_observation_receipt_count": rollup.get("observation_receipt_count"),
        "rollup_runtime_seconds": rollup.get("runtime_seconds"),
        "rollup_observation_write_rate_per_second": rollup.get("observation_write_rate_per_second"),
        "receipt_index_path": rel(RECEIPT_INDEX_PATH),
        "receipt_index_sha256": file_sha256(RECEIPT_INDEX_PATH),
        "receipt_index_line_count": index_line_count,
        "observation_receipt_files_count": len(receipt_files),
        "sample_records": sample_records,
        "sample_parseable": all(parseable) if parseable else False,
        "sample_gate_pass": all(gate_pass) if gate_pass else False,
        "sample_indices": indices,
        "artifact_audit_passed": (
            RUN_DIR.exists()
            and run_receipt.get("gate") == "PASS"
            and run_receipt.get("radius_requested") == EXPECTED_RADIUS
            and run_receipt.get("radius_completed") == EXPECTED_RADIUS
            and run_receipt.get("observation_receipt_count") == EXPECTED_RADIUS
            and rollup.get("gate") == "PASS"
            and rollup.get("radius_completed") == EXPECTED_RADIUS
            and rollup.get("observation_receipt_count") == EXPECTED_RADIUS
            and len(receipt_files) == EXPECTED_RADIUS
            and index_line_count == EXPECTED_RADIUS
            and (all(parseable) if parseable else False)
            and (all(gate_pass) if gate_pass else False)
        ),
    }
    return audit

def observation_profile(audit: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_observation_receipt_profile_v0",
        "run_id": RUN_ID,
        "observation_receipt_count": audit["observation_receipt_files_count"],
        "receipt_index_line_count": audit["receipt_index_line_count"],
        "sample_indices": audit["sample_indices"],
        "sample_records": audit["sample_records"],
        "profile_status": "OBSERVATION_RECEIPT_PROFILE_ACCEPTED_RADIUS_10000" if audit["artifact_audit_passed"] else "OBSERVATION_RECEIPT_PROFILE_REVIEW_FAILED",
    }

def boundary_guard_review() -> Dict[str, Any]:
    retry = read_json(RETRY_RECEIPT_PATH)
    rollup = read_json(ROLLUP_PATH)
    metrics = retry.get("aggregate_metrics", {})
    guard_keys = [
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
    ]
    retry_guard_values = {k: metrics.get(k) for k in guard_keys}
    rollup_guard_values = {k: rollup.get(k) for k in [
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
    ] if k in rollup}
    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_boundary_guard_review_v0",
        "retry_guard_values": retry_guard_values,
        "rollup_guard_values": rollup_guard_values,
        "all_retry_guard_counts_zero": all(v == 0 for v in retry_guard_values.values()),
        "all_rollup_guard_counts_zero": all(v == 0 for v in rollup_guard_values.values()) if rollup_guard_values else True,
        "boundary_guard_review_passed": all(v == 0 for v in retry_guard_values.values()) and (all(v == 0 for v in rollup_guard_values.values()) if rollup_guard_values else True),
    }

def classify_result(audit: Dict[str, Any], guards: Dict[str, Any]) -> Dict[str, Any]:
    accepted = audit["artifact_audit_passed"] and guards["boundary_guard_review_passed"]
    return {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_result_classification_packet_v0",
        "classification": "RADIUS_10000_RESULT_ACCEPTED_BOUNDED_OBSERVABILITY_HARVEST_COMPLETE" if accepted else "RADIUS_10000_RESULT_REVIEW_FAILED",
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "run_id": RUN_ID,
        "evidence": {
            "retry_receipt_gate": read_json(RETRY_RECEIPT_PATH).get("gate"),
            "run_receipt_gate": audit["run_receipt_gate"],
            "rollup_gate": audit["rollup_gate"],
            "radius_completed": audit["rollup_radius_completed"],
            "observation_receipt_count": audit["rollup_observation_receipt_count"],
            "observation_receipt_files_count": audit["observation_receipt_files_count"],
            "receipt_index_line_count": audit["receipt_index_line_count"],
            "artifact_audit_passed": audit["artifact_audit_passed"],
            "boundary_guard_review_passed": guards["boundary_guard_review_passed"],
        },
        "accepted_as_closure_observability_result": accepted,
        "requires_repair": False,
        "requires_rerun": False,
        "requires_human_strategy_selection_for_next_scale_or_close": accepted,
    }

def validate_outputs(audit: Dict[str, Any], guards: Dict[str, Any], classification: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if audit.get("artifact_audit_passed") is not True:
        failures.append("artifact_audit_not_passed")
    if audit.get("observation_receipt_files_count") != EXPECTED_RADIUS:
        failures.append("observation_receipt_files_count_not_10000")
    if audit.get("receipt_index_line_count") != EXPECTED_RADIUS:
        failures.append("receipt_index_line_count_not_10000")
    if guards.get("boundary_guard_review_passed") is not True:
        failures.append("boundary_guard_review_not_passed")
    if classification.get("accepted_as_closure_observability_result") is not True:
        failures.append("classification_not_accepted")

    for key in [
        "radius_10000_rerun_count",
        "new_small_probe_count",
        "unbounded_or_no_cap_run_count",
        "radius_above_10000_run_count",
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
    expected_one = [
        "radius_10000_retry_receipt_consumed_count",
        "run_receipt_consumed_count",
        "rollup_consumed_count",
        "receipt_index_consumed_count",
        "run_artifact_audit_emitted_count",
        "observation_receipt_profile_emitted_count",
        "boundary_guard_review_emitted_count",
        "result_classification_packet_emitted_count",
        "review_decision_emitted_count",
        "next_status_packet_emitted_count",
        "artifact_audit_passed_count",
        "boundary_guard_review_passed_count",
        "result_accepted_count",
    ]
    for key in expected_one:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    if metrics.get("observation_receipt_files_count") != EXPECTED_RADIUS:
        failures.append(f"metric_observation_files_not_10000:{metrics.get('observation_receipt_files_count')}")
    if metrics.get("receipt_index_line_count") != EXPECTED_RADIUS:
        failures.append(f"metric_receipt_index_not_10000:{metrics.get('receipt_index_line_count')}")

    for key in [
        "radius_10000_rerun_count",
        "new_small_probe_count",
        "unbounded_or_no_cap_run_count",
        "radius_above_10000_run_count",
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
    if terminal.get("stop_code") != "STOP_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RESULT_REVIEW_COMPLETE":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    audit = audit_run_artifacts()
    profile = observation_profile(audit)
    guards = boundary_guard_review()
    classification = classify_result(audit, guards)

    decision = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_result_review_decision_v0",
        "decision_id": sha8({
            "unit_id": UNIT_ID,
            "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
            "classification": classification["classification"],
            "run_id": RUN_ID,
        }),
        "decision_status": "RADIUS_10000_RESULT_REVIEW_ACCEPTED",
        "result_classification": classification["classification"],
        "radius_10000_result_accepted": classification["accepted_as_closure_observability_result"],
        "artifact_audit_passed": audit["artifact_audit_passed"],
        "boundary_guard_review_passed": guards["boundary_guard_review_passed"],
        "observation_receipt_count": audit["rollup_observation_receipt_count"],
        "observation_receipt_files_count": audit["observation_receipt_files_count"],
        "receipt_index_line_count": audit["receipt_index_line_count"],
        "runtime_seconds": audit["rollup_runtime_seconds"],
        "run_id": RUN_ID,
        "run_dir": rel(RUN_DIR),
        "review_executed_without_rerun": True,
        "recommended_next_handling": "SELECT_NEXT_POST_CLOSURE_OBSERVABILITY_SCALE_OR_CLOSE_DECISION_AFTER_R10000_REVIEW_V0",
    }

    next_status = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_result_review_next_status_packet_v0",
        "packet_status": "RADIUS_10000_RESULT_REVIEW_ACCEPTED_READY_FOR_HUMAN_STRATEGY_SELECTION",
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "run_id": RUN_ID,
        "run_dir": rel(RUN_DIR),
        "observation_receipt_count": audit["rollup_observation_receipt_count"],
        "observation_receipt_files_count": audit["observation_receipt_files_count"],
        "radius_completed": audit["rollup_radius_completed"],
        "boundary_clean": guards["boundary_guard_review_passed"],
        "available_safe_next_choices": [
            "close this observability branch as accepted",
            "review the radius-10000 rollup/profile for signal content",
            "choose a larger bounded radius only as a separate explicit command",
            "convert accepted observability harvest into a reusable bounded entrypoint protocol",
        ],
        "recommended_next_handling": decision["recommended_next_handling"],
        "auto_next_command": None,
    }

    report = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_result_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "radius_10000_retry_receipt_consumed_count": 1,
        "run_receipt_consumed_count": 1,
        "rollup_consumed_count": 1,
        "receipt_index_consumed_count": 1,
        "run_artifact_audit_emitted_count": 1,
        "observation_receipt_profile_emitted_count": 1,
        "boundary_guard_review_emitted_count": 1,
        "result_classification_packet_emitted_count": 1,
        "review_decision_emitted_count": 1,
        "next_status_packet_emitted_count": 1,
        "artifact_audit_passed_count": 1 if audit["artifact_audit_passed"] else 0,
        "boundary_guard_review_passed_count": 1 if guards["boundary_guard_review_passed"] else 0,
        "result_accepted_count": 1 if classification["accepted_as_closure_observability_result"] else 0,
        "observation_receipt_files_count": audit["observation_receipt_files_count"],
        "receipt_index_line_count": audit["receipt_index_line_count"],
        "radius_completed": audit["rollup_radius_completed"],
        "runtime_seconds": audit["rollup_runtime_seconds"],
        "run_id": RUN_ID,
        "run_dir": rel(RUN_DIR),
        "radius_10000_rerun_count": 0,
        "new_small_probe_count": 0,
        "unbounded_or_no_cap_run_count": 0,
        "radius_above_10000_run_count": 0,
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

    review_surface = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_result_review_surface_v0",
        "review_surface_id": sha8({
            "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
            "classification": classification["classification"],
            "run_id": RUN_ID,
        }),
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "run_id": RUN_ID,
        "run_dir": rel(RUN_DIR),
        "result_classification": classification["classification"],
        "radius_completed": audit["rollup_radius_completed"],
        "observation_receipt_count": audit["rollup_observation_receipt_count"],
        "observation_receipt_files_count": audit["observation_receipt_files_count"],
        "receipt_index_line_count": audit["receipt_index_line_count"],
        "runtime_seconds": audit["rollup_runtime_seconds"],
        "artifact_audit_passed": audit["artifact_audit_passed"],
        "boundary_guard_review_passed": guards["boundary_guard_review_passed"],
        "accepted": classification["accepted_as_closure_observability_result"],
        "recommended_next_handling": decision["recommended_next_handling"],
    }

    trace = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_result_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_radius_10000_retry_receipt",
                "question": "retry completed and requested result review",
                "answer": True,
                "taken": "audit_existing_run_artifacts",
            },
            {
                "step": "audit_existing_run_artifacts",
                "question": "run artifacts show exactly 10000 observation receipts",
                "answer": audit["artifact_audit_passed"],
                "taken": "review_boundary_guards",
            },
            {
                "step": "review_boundary_guards",
                "question": "no boundary violations were recorded",
                "answer": guards["boundary_guard_review_passed"],
                "taken": "classify_result",
            },
            {
                "step": "classify_result",
                "question": "accept radius-10000 result",
                "answer": classification["accepted_as_closure_observability_result"],
                "taken": "emit_next_status_packet",
            },
            {
                "step": "emit_next_status_packet",
                "question": "run another command now",
                "answer": False,
                "taken": "STOP_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RESULT_REVIEW_COMPLETE",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RESULT_REVIEW_COMPLETE",
            "next_command_goal": None,
        },
    }

    write_json(RESULT_REVIEW_SURFACE_PATH, review_surface)
    write_json(RUN_ARTIFACT_AUDIT_PATH, audit)
    write_json(OBSERVATION_RECEIPT_PROFILE_PATH, profile)
    write_json(BOUNDARY_GUARD_REVIEW_PATH, guards)
    write_json(RESULT_CLASSIFICATION_PACKET_PATH, classification)
    write_json(NEXT_STATUS_PACKET_PATH, next_status)
    write_json(REVIEW_DECISION_PATH, decision)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(audit, guards, classification, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "RADIUS_10000_RESULT_REVIEW_0_RETRY_RECEIPT_CONSUMED": True,
        "RADIUS_10000_RESULT_REVIEW_1_RUN_ARTIFACTS_CONSUMED": report["run_receipt_consumed_count"] == 1 and report["rollup_consumed_count"] == 1 and report["receipt_index_consumed_count"] == 1,
        "RADIUS_10000_RESULT_REVIEW_2_ARTIFACT_AUDIT_PASS": report["artifact_audit_passed_count"] == 1,
        "RADIUS_10000_RESULT_REVIEW_3_OBSERVATION_COUNT_10000": report["observation_receipt_files_count"] == EXPECTED_RADIUS and report["receipt_index_line_count"] == EXPECTED_RADIUS,
        "RADIUS_10000_RESULT_REVIEW_4_BOUNDARY_GUARDS_PASS": report["boundary_guard_review_passed_count"] == 1,
        "RADIUS_10000_RESULT_REVIEW_5_RESULT_ACCEPTED": report["result_accepted_count"] == 1,
        "RADIUS_10000_RESULT_REVIEW_6_NO_RERUN_OR_PROBE": report["radius_10000_rerun_count"] == 0 and report["new_small_probe_count"] == 0,
        "RADIUS_10000_RESULT_REVIEW_7_NO_UNBOUNDED_OR_RADIUS_ABOVE_10000": report["unbounded_or_no_cap_run_count"] == 0 and report["radius_above_10000_run_count"] == 0,
        "RADIUS_10000_RESULT_REVIEW_8_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0,
        "RADIUS_10000_RESULT_REVIEW_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "RADIUS_10000_RESULT_REVIEW_10_NO_REPAIR_OR_TAXONOMY": report["repair_executed_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "RADIUS_10000_RESULT_REVIEW_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "source_cli_wrapper_fix_failure_review_receipt_id": SOURCE_CLI_WRAPPER_FIX_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_cli_wrapper_fix_receipt_id": SOURCE_FAILED_CLI_WRAPPER_FIX_RECEIPT_ID,
        "source_cli_wrapper_review_receipt_id": SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards_packet = {
        "radius_10000_retry_receipt_consumed": True,
        "review_only_no_rerun": True,
        "artifact_audit_passed": audit["artifact_audit_passed"],
        "boundary_guard_review_passed": guards["boundary_guard_review_passed"],
        "result_accepted": classification["accepted_as_closure_observability_result"],
        "radius_10000_rerun": False,
        "new_small_probe": False,
        "unbounded_or_no_cap_run": False,
        "radius_above_10000_run": False,
        "source_mutated": source_mutation_detected,
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
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "classification": classification["classification"],
        "run_id": RUN_ID,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "result_review_surface": rel(RESULT_REVIEW_SURFACE_PATH),
        "run_artifact_audit": rel(RUN_ARTIFACT_AUDIT_PATH),
        "observation_receipt_profile": rel(OBSERVATION_RECEIPT_PROFILE_PATH),
        "boundary_guard_review": rel(BOUNDARY_GUARD_REVIEW_PATH),
        "result_classification_packet": rel(RESULT_CLASSIFICATION_PACKET_PATH),
        "next_status_packet": rel(NEXT_STATUS_PACKET_PATH),
        "review_decision": rel(REVIEW_DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "run_dir": rel(RUN_DIR),
        "run_receipt_path": rel(RUN_RECEIPT_PATH),
        "rollup_path": rel(ROLLUP_PATH),
        "receipt_index_path": rel(RECEIPT_INDEX_PATH),
    }

    receipt = {
        "schema_version": "r1000_post_closure_observability_harvest_radius_10000_result_review_receipt_v0",
        "receipt_type": "R1000_POST_CLOSURE_OBSERVABILITY_HARVEST_RADIUS_10000_RESULT_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "source_cli_wrapper_fix_failure_review_receipt_id": SOURCE_CLI_WRAPPER_FIX_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_cli_wrapper_fix_receipt_id": SOURCE_FAILED_CLI_WRAPPER_FIX_RECEIPT_ID,
        "source_cli_wrapper_review_receipt_id": SOURCE_CLI_WRAPPER_REVIEW_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "radius_10000_result_review_summary": {
            "review_result": decision["decision_status"],
            "result_classification": classification["classification"],
            "radius_10000_result_accepted": decision["radius_10000_result_accepted"],
            "run_id": RUN_ID,
            "run_dir": rel(RUN_DIR),
            "radius_completed": audit["rollup_radius_completed"],
            "observation_receipt_count": audit["rollup_observation_receipt_count"],
            "observation_receipt_files_count": audit["observation_receipt_files_count"],
            "receipt_index_line_count": audit["receipt_index_line_count"],
            "runtime_seconds": audit["rollup_runtime_seconds"],
            "artifact_audit_passed": audit["artifact_audit_passed"],
            "boundary_guard_review_passed": guards["boundary_guard_review_passed"],
            "review_only_no_rerun": True,
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "radius_10000_result_review_guards": guards_packet,
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
    print(f"radius_10000_result_review_receipt_id={receipt_id}")
    print(f"radius_10000_result_review_receipt_path=data/r1000_post_closure_observability_harvest_radius_10000_result_review_v0_receipts/{receipt_id}.json")
    print(f"next_status_packet_path=data/r1000_post_closure_observability_harvest_radius_10000_result_review_v0/r1000_post_closure_observability_harvest_radius_10000_result_review_next_status_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
