#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_CLOSE_AND_FREEZE_BOUNDED_OBSERVABILITY_PROTOCOL_AFTER_R10000_VOLATILE_ONLY_SIGNAL_V0"
TARGET_UNIT_ID = "r10000.observability_branch.close_and_bounded_protocol_freeze.v0"

SOURCE_GUARD_PATCH_RECEIPT_ID = "45f16008"
SOURCE_FAILURE_REVIEW_RECEIPT_ID = "e3fe49d3"
SOURCE_FAILED_LOCALIZATION_RECEIPT_ID = "bb9e4719"
SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID = "293faf9e"
SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID = "90042e28"
SOURCE_RADIUS_10000_RETRY_RECEIPT_ID = "bb2c8ce3"
SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID = "02711ff1"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"
RUN_ID = "run_6b1b2494"
EXPECTED_RADIUS = 10000

OUT_DIR = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0"
RECEIPT_DIR = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0_receipts"

CLOSE_FREEZE_PLAN_PATH = OUT_DIR / "r10000_close_and_freeze_plan.json"
SOURCE_SURFACE_PATH = OUT_DIR / "r10000_close_and_freeze_source_surface.json"
BRANCH_CLOSURE_DECISION_PATH = OUT_DIR / "r10000_observability_branch_closure_decision.json"
BOUNDED_PROTOCOL_FREEZE_PATH = OUT_DIR / "bounded_observability_protocol_freeze_v0.json"
REUSABLE_PROTOCOL_REFERENCE_PATH = OUT_DIR / "bounded_observability_protocol_reusable_reference_v0.json"
FINAL_STATE_PACKET_PATH = OUT_DIR / "r10000_observability_branch_final_state_packet.json"
NEXT_STATUS_PACKET_PATH = OUT_DIR / "r10000_close_and_freeze_next_status_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r10000_close_and_freeze_transition_trace.json"
REPORT_PATH = OUT_DIR / "r10000_close_and_freeze_report.json"

GUARD_PATCH_RECEIPT_PATH = ROOT / "data" / "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0_receipts" / f"{SOURCE_GUARD_PATCH_RECEIPT_ID}.json"
PATCHED_LOCALIZATION_PACKET_PATH = ROOT / "data" / "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0" / "r10000_signal_localization_patched_acceptance_packet.json"
PATCHED_NEXT_DECISION_PACKET_PATH = ROOT / "data" / "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0" / "r10000_signal_localization_patched_acceptance_next_decision_packet.json"
GUARD_PATCH_REPORT_PATH = ROOT / "data" / "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0" / "r10000_signal_localization_guard_reference_only_acceptance_patch_report.json"
REFERENCE_ONLY_RECHECK_PATH = ROOT / "data" / "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0" / "r10000_signal_localization_reference_only_acceptance_recheck.json"

FAILURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r10000_distinguishable_signal_localization_failure_protected_key_hits_review_v0_receipts" / f"{SOURCE_FAILURE_REVIEW_RECEIPT_ID}.json"
FAILED_LOCALIZATION_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0_receipts" / f"{SOURCE_FAILED_LOCALIZATION_RECEIPT_ID}.json"
SIGNAL_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_rollup_profile_signal_inspection_v0_receipts" / f"{SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID}.json"
RESULT_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_result_review_v0_receipts" / f"{SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID}.json"
RETRY_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_retry_with_cli_wrapper_intercept_parse_fixed_v0_receipts" / f"{SOURCE_RADIUS_10000_RETRY_RECEIPT_ID}.json"

RUN_DIR = ROOT / "data" / "r1000_post_closure_observability_harvest_runs_v0" / RUN_ID
RUN_RECEIPT_PATH = RUN_DIR / "run_receipt.json"
ROLLUP_PATH = RUN_DIR / "rollup.json"
RECEIPT_INDEX_PATH = RUN_DIR / "receipt_index.jsonl"

CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_entrypoint_cli_wrapper_intercept_parse_fix_v0_receipts" / f"{SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID}.json"
CLOSURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID}.json"
CLOSED_QUEUE_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
EXPECTED_LIMIT_MARK_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts" / f"{SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID}.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"

CLI_PATH = ROOT / "src" / "matrixlab" / "cli.py"
ENTRYPOINT_MODULE_PATH = ROOT / "src" / "matrixlab" / "r1000_post_closure_observability_harvest.py"

SOURCE_FILES = [
    GUARD_PATCH_RECEIPT_PATH,
    PATCHED_LOCALIZATION_PACKET_PATH,
    PATCHED_NEXT_DECISION_PACKET_PATH,
    GUARD_PATCH_REPORT_PATH,
    REFERENCE_ONLY_RECHECK_PATH,
    FAILURE_REVIEW_RECEIPT_PATH,
    FAILED_LOCALIZATION_RECEIPT_PATH,
    SIGNAL_INSPECTION_RECEIPT_PATH,
    RESULT_REVIEW_RECEIPT_PATH,
    RETRY_RECEIPT_PATH,
    RUN_RECEIPT_PATH,
    ROLLUP_PATH,
    RECEIPT_INDEX_PATH,
    CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_PATH,
    CLOSURE_REVIEW_RECEIPT_PATH,
    CLOSED_QUEUE_HANDOFF_PATH,
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    FINAL_QUEUE_STATE_PATH,
    CLI_PATH,
    ENTRYPOINT_MODULE_PATH,
]

HUMAN_DECISION = {
    "decision": "CLOSE_AND_FREEZE",
    "scope": "close the R10000 post-closure observability branch and freeze the bounded observability protocol as reusable infrastructure after accepted volatile-only signal localization",
    "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
    "authorized": [
        "consume accepted guard patch receipt",
        "consume patched localization packet",
        "close the R10000 observability branch",
        "freeze bounded observability protocol v0",
        "emit reusable protocol reference",
        "emit final state packet",
        "stop with no next command goal",
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
    guard = read_json(GUARD_PATCH_RECEIPT_PATH)
    patched = read_json(PATCHED_LOCALIZATION_PACKET_PATH)
    next_packet = read_json(PATCHED_NEXT_DECISION_PACKET_PATH)
    report = read_json(GUARD_PATCH_REPORT_PATH)
    recheck = read_json(REFERENCE_ONLY_RECHECK_PATH)
    result_review = read_json(RESULT_REVIEW_RECEIPT_PATH)
    retry = read_json(RETRY_RECEIPT_PATH)
    run_receipt = read_json(RUN_RECEIPT_PATH)
    rollup = read_json(ROLLUP_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if guard.get("receipt_id") != SOURCE_GUARD_PATCH_RECEIPT_ID:
        failures.append("guard_patch_receipt_id_wrong")
    if guard.get("gate") != "PASS":
        failures.append("guard_patch_gate_not_pass")
    if guard.get("r10000_guard_patch_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("guard_patch_not_recommending_close_freeze")
    if patched.get("classification") != "R10000_LOCALIZATION_VOLATILE_RECEIPT_METADATA_ONLY_ACCEPTED_AFTER_REFERENCE_ONLY_GUARD_PATCH":
        failures.append("patched_classification_wrong")
    if patched.get("accepted_driver_class") != "RECEIPT_VOLATILITY_ONLY_NO_STRUCTURAL_SIGNAL_LOCALIZED":
        failures.append("patched_driver_wrong")
    if patched.get("requires_repair") is not False or patched.get("requires_further_localization") is not False:
        failures.append("patched_packet_requires_more_work")
    if next_packet.get("packet_status") != "R10000_SIGNAL_LOCALIZATION_REFERENCE_ONLY_GUARD_PATCH_ACCEPTED_READY_FOR_CLOSE_OR_FREEZE_DECISION":
        failures.append("next_packet_not_close_freeze_ready")
    if recheck.get("reference_only_acceptance_passed") is not True:
        failures.append("reference_only_acceptance_not_passed")
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
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"guard_patch_boundary_count_not_zero:{key}:{report.get(key)}")

    if result_review.get("gate") != "PASS":
        failures.append("result_review_gate_not_pass")
    if retry.get("gate") != "PASS":
        failures.append("retry_gate_not_pass")
    if run_receipt.get("gate") != "PASS":
        failures.append("run_receipt_gate_not_pass")
    if rollup.get("gate") != "PASS":
        failures.append("rollup_gate_not_pass")
    if run_receipt.get("radius_completed") != EXPECTED_RADIUS or rollup.get("radius_completed") != EXPECTED_RADIUS:
        failures.append("radius_completed_not_10000")
    if run_receipt.get("observation_receipt_count") != EXPECTED_RADIUS or rollup.get("observation_receipt_count") != EXPECTED_RADIUS:
        failures.append("observation_receipt_count_not_10000")

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

def build_source_surface() -> Dict[str, Any]:
    guard = read_json(GUARD_PATCH_RECEIPT_PATH)
    patched = read_json(PATCHED_LOCALIZATION_PACKET_PATH)
    result_review = read_json(RESULT_REVIEW_RECEIPT_PATH)
    retry = read_json(RETRY_RECEIPT_PATH)
    rollup = read_json(ROLLUP_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    return {
        "schema_version": "r10000_close_and_freeze_source_surface_v0",
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "source_failure_review_receipt_id": SOURCE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_localization_receipt_id": SOURCE_FAILED_LOCALIZATION_RECEIPT_ID,
        "source_r10000_signal_inspection_receipt_id": SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID,
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "guard_patch_summary": guard.get("r10000_guard_patch_summary"),
        "patched_localization_packet": patched,
        "result_review_summary": result_review.get("radius_10000_result_review_summary"),
        "retry_summary": retry.get("radius_10000_retry_summary"),
        "rollup_core": {
            "gate": rollup.get("gate"),
            "radius_completed": rollup.get("radius_completed"),
            "observation_receipt_count": rollup.get("observation_receipt_count"),
            "runtime_seconds": rollup.get("runtime_seconds"),
        },
        "pressure_queue_closure_core": {
            "receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
            "gate": closure.get("gate"),
            "summary": closure.get("r1000_pressure_queue_closure_review_summary"),
        },
    }

def validate_outputs(branch: Dict[str, Any], freeze: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if branch.get("branch_status") != "CLOSED":
        failures.append("branch_not_closed")
    if freeze.get("freeze_status") != "FROZEN_REUSABLE_REFERENCE":
        failures.append("protocol_not_frozen")
    if freeze.get("bounded_protocol_steps") != [
        "select bounded radius",
        "run bounded sample",
        "produce receipts",
        "inspect rollup/profile",
        "classify signal",
        "choose close, repair observability, localize signal, run larger bounded radius with explicit objective, or freeze protocol",
    ]:
        failures.append("bounded_protocol_steps_changed")
    if report.get("close_decision_count") != 1:
        failures.append("close_decision_count_not_one")
    if report.get("freeze_protocol_count") != 1:
        failures.append("freeze_protocol_count_not_one")

    for key in [
        "radius_10000_rerun_count",
        "new_small_probe_count",
        "unbounded_or_no_cap_run_count",
        "radius_above_10000_run_count",
        "larger_bounded_radius_run_count",
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
        "guard_patch_receipt_consumed_count",
        "patched_localization_packet_consumed_count",
        "source_surface_emitted_count",
        "branch_closure_decision_emitted_count",
        "bounded_protocol_freeze_emitted_count",
        "reusable_protocol_reference_emitted_count",
        "final_state_packet_emitted_count",
        "next_status_packet_emitted_count",
        "close_decision_count",
        "freeze_protocol_count",
        "volatile_only_signal_accepted_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    for key in [
        "radius_10000_rerun_count",
        "new_small_probe_count",
        "unbounded_or_no_cap_run_count",
        "radius_above_10000_run_count",
        "larger_bounded_radius_run_count",
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
    if terminal.get("stop_code") != "STOP_R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    source_surface = build_source_surface()
    patched = read_json(PATCHED_LOCALIZATION_PACKET_PATH)
    guard = read_json(GUARD_PATCH_RECEIPT_PATH)

    plan = {
        "schema_version": "r10000_close_and_freeze_plan_v0",
        "unit_id": UNIT_ID,
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "mode": "close_branch_and_freeze_protocol_no_rerun",
        "decision": "close and freeze",
        "not_authorized": HUMAN_DECISION["not_authorized"],
    }

    branch_closure = {
        "schema_version": "r10000_observability_branch_closure_decision_v0",
        "branch_id": "R10000_POST_CLOSURE_OBSERVABILITY_BRANCH",
        "branch_status": "CLOSED",
        "closure_reason": "Radius-10000 bounded observability harvest completed, reviewed, localized, and patched to accept reference-only protected-key hits; remaining distinguishability is receipt/reference volatility only.",
        "accepted_evidence": {
            "radius_10000_run_gate": read_json(RUN_RECEIPT_PATH).get("gate"),
            "radius_10000_result_review_gate": read_json(RESULT_REVIEW_RECEIPT_PATH).get("gate"),
            "signal_inspection_gate": read_json(SIGNAL_INSPECTION_RECEIPT_PATH).get("gate"),
            "guard_patch_gate": guard.get("gate"),
            "accepted_localization_classification": patched.get("accepted_localization_classification"),
            "accepted_driver_class": patched.get("accepted_driver_class"),
            "patched_classification": patched.get("classification"),
            "requires_repair": patched.get("requires_repair"),
            "requires_further_localization": patched.get("requires_further_localization"),
        },
        "not_closed_as": [
            "semantic signal requiring repair",
            "structural signal requiring further localization",
            "queue reopening",
            "larger radius authorization",
            "unbounded run authorization",
        ],
        "closed_at": now_iso(),
    }

    bounded_protocol = {
        "schema_version": "bounded_observability_protocol_freeze_v0",
        "protocol_id": "BOUNDED_OBSERVABILITY_PROTOCOL_V0",
        "freeze_status": "FROZEN_REUSABLE_REFERENCE",
        "source_branch_id": "R10000_POST_CLOSURE_OBSERVABILITY_BRANCH",
        "bounded_protocol_steps": [
            "select bounded radius",
            "run bounded sample",
            "produce receipts",
            "inspect rollup/profile",
            "classify signal",
            "choose close, repair observability, localize signal, run larger bounded radius with explicit objective, or freeze protocol",
        ],
        "decision_graph": {
            "NO_NEW_SIGNAL_OR_VOLATILE_ONLY_SIGNAL": "close branch or freeze protocol",
            "OBSERVABILITY_HEALTH_CONFIRMED": "freeze protocol or choose explicit next objective",
            "DISTINGUISHABLE_CLEAN_SIGNAL": "localize signal before scaling",
            "OBSERVABILITY_SURFACE_INSUFFICIENT": "repair observability before scaling",
            "BOUNDARY_OR_FAILURE_SIGNAL": "review failure, repair only if supported",
            "LARGER_RADIUS_CANDIDATE": "run only as separate bounded unit with explicit objective",
        },
        "frozen_lessons": [
            "Do not treat larger radius as number-go-up.",
            "Inspect rollup/profile before scaling.",
            "Clean PASS traffic can still contain distinguishable receipt structure.",
            "Receipt/reference volatility must be distinguished from semantic or structural signal.",
            "Protected key-name references are not boundary crossings when materialization/inspection/mutation counters remain zero.",
            "Close/freeze is valid after accepted volatile-only localization.",
        ],
        "hard_guards": [
            "no unbounded run",
            "no hidden next command",
            "no queue reopening during observability review",
            "no closed-group inspection unless explicitly authorized",
            "no row payload materialization unless explicitly authorized",
            "no identity/value invention",
            "no source/prior receipt mutation",
        ],
        "frozen_at": now_iso(),
    }

    reusable_reference = {
        "schema_version": "bounded_observability_protocol_reusable_reference_v0",
        "reference_status": "READY_FOR_REUSE",
        "protocol_id": bounded_protocol["protocol_id"],
        "canonical_source_artifact": rel(BOUNDED_PROTOCOL_FREEZE_PATH),
        "when_to_use": [
            "after a branch closes and needs bounded post-closure observation",
            "before escalating radius",
            "when a clean run may still contain distinguishable receipt/profile signal",
            "when deciding close versus repair versus localization versus explicit bounded scale",
        ],
        "minimum_receipts_to_preserve": [
            "run receipt",
            "rollup/profile",
            "receipt index",
            "signal classification packet",
            "localization packet when signal exists",
            "final close/freeze receipt",
        ],
        "reuse_rule": "Any future branch may reuse this protocol only by selecting a bounded radius and explicit objective; larger radius is not implicit progress.",
    }

    final_state = {
        "schema_version": "r10000_observability_branch_final_state_packet_v0",
        "packet_status": "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN",
        "branch_status": branch_closure["branch_status"],
        "protocol_freeze_status": bounded_protocol["freeze_status"],
        "accepted_final_signal_class": "VOLATILE_RECEIPT_REFERENCE_METADATA_ONLY",
        "accepted_driver_class": patched.get("accepted_driver_class"),
        "requires_repair": False,
        "requires_further_localization": False,
        "larger_radius_authorized_now": False,
        "safe_future_options": [
            "move to next objective",
            "reuse bounded observability protocol on another branch",
            "run a larger bounded radius only as a separate explicit objective",
            "begin domain shift or builder-cell communication work as a separate branch",
        ],
        "auto_next_command": None,
    }

    next_status = {
        "schema_version": "r10000_close_and_freeze_next_status_packet_v0",
        "packet_status": "CLOSED_AND_FROZEN_NO_NEXT_COMMAND",
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "final_state_packet": rel(FINAL_STATE_PACKET_PATH),
        "bounded_protocol_freeze": rel(BOUNDED_PROTOCOL_FREEZE_PATH),
        "reusable_protocol_reference": rel(REUSABLE_PROTOCOL_REFERENCE_PATH),
        "recommended_next_handling": None,
        "auto_next_command": None,
    }

    report = {
        "schema_version": "r10000_close_and_freeze_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "guard_patch_receipt_consumed_count": 1,
        "patched_localization_packet_consumed_count": 1,
        "source_surface_emitted_count": 1,
        "branch_closure_decision_emitted_count": 1,
        "bounded_protocol_freeze_emitted_count": 1,
        "reusable_protocol_reference_emitted_count": 1,
        "final_state_packet_emitted_count": 1,
        "next_status_packet_emitted_count": 1,
        "close_decision_count": 1,
        "freeze_protocol_count": 1,
        "volatile_only_signal_accepted_count": 1,
        "radius_10000_rerun_count": 0,
        "new_small_probe_count": 0,
        "unbounded_or_no_cap_run_count": 0,
        "radius_above_10000_run_count": 0,
        "larger_bounded_radius_run_count": 0,
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
        "recommended_next_handling": None,
    }

    trace = {
        "schema_version": "r10000_close_and_freeze_transition_trace_v0",
        "trace": [
            {
                "step": "consume_guard_patch",
                "question": "is volatile-only localization accepted after reference-only guard patch",
                "answer": True,
                "taken": "close_branch",
            },
            {
                "step": "close_branch",
                "question": "does branch require repair, further localization, or rerun",
                "answer": False,
                "taken": "freeze_bounded_protocol",
            },
            {
                "step": "freeze_bounded_protocol",
                "question": "freeze reusable bounded observability protocol",
                "answer": True,
                "taken": "emit_final_state",
            },
            {
                "step": "emit_final_state",
                "question": "emit hidden next command",
                "answer": False,
                "taken": "STOP_R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN",
            "next_command_goal": None,
        },
    }

    write_json(CLOSE_FREEZE_PLAN_PATH, plan)
    write_json(SOURCE_SURFACE_PATH, source_surface)
    write_json(BRANCH_CLOSURE_DECISION_PATH, branch_closure)
    write_json(BOUNDED_PROTOCOL_FREEZE_PATH, bounded_protocol)
    write_json(REUSABLE_PROTOCOL_REFERENCE_PATH, reusable_reference)
    write_json(FINAL_STATE_PACKET_PATH, final_state)
    write_json(NEXT_STATUS_PACKET_PATH, next_status)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(branch_closure, bounded_protocol, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "CLOSE_FREEZE_0_GUARD_PATCH_CONSUMED": True,
        "CLOSE_FREEZE_1_VOLATILE_ONLY_SIGNAL_ACCEPTED": report["volatile_only_signal_accepted_count"] == 1,
        "CLOSE_FREEZE_2_BRANCH_CLOSED": branch_closure["branch_status"] == "CLOSED",
        "CLOSE_FREEZE_3_PROTOCOL_FROZEN": bounded_protocol["freeze_status"] == "FROZEN_REUSABLE_REFERENCE",
        "CLOSE_FREEZE_4_REUSABLE_REFERENCE_EMITTED": report["reusable_protocol_reference_emitted_count"] == 1,
        "CLOSE_FREEZE_5_FINAL_STATE_EMITTED": report["final_state_packet_emitted_count"] == 1,
        "CLOSE_FREEZE_6_NO_RERUN_OR_PROBE": report["radius_10000_rerun_count"] == 0 and report["new_small_probe_count"] == 0,
        "CLOSE_FREEZE_7_NO_UNBOUNDED_OR_RADIUS_ABOVE_10000": report["unbounded_or_no_cap_run_count"] == 0 and report["radius_above_10000_run_count"] == 0,
        "CLOSE_FREEZE_8_NO_LARGER_BOUNDED_RADIUS_RUN": report["larger_bounded_radius_run_count"] == 0,
        "CLOSE_FREEZE_9_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0 and report["row_payload_inspected_count"] == 0,
        "CLOSE_FREEZE_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "CLOSE_FREEZE_11_NO_REPAIR_OR_TAXONOMY": report["repair_executed_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "CLOSE_FREEZE_12_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None and next_status["auto_next_command"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "source_failure_review_receipt_id": SOURCE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_localization_receipt_id": SOURCE_FAILED_LOCALIZATION_RECEIPT_ID,
        "source_r10000_signal_inspection_receipt_id": SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID,
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards_packet = {
        "close_and_freeze_only_no_rerun": True,
        "existing_artifacts_only": True,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "radius_10000_rerun": False,
        "new_small_probe": False,
        "unbounded_or_no_cap_run": False,
        "radius_above_10000_run": False,
        "larger_bounded_radius_run": False,
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
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "branch_status": branch_closure["branch_status"],
        "freeze_status": bounded_protocol["freeze_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "close_freeze_plan": rel(CLOSE_FREEZE_PLAN_PATH),
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "branch_closure_decision": rel(BRANCH_CLOSURE_DECISION_PATH),
        "bounded_protocol_freeze": rel(BOUNDED_PROTOCOL_FREEZE_PATH),
        "reusable_protocol_reference": rel(REUSABLE_PROTOCOL_REFERENCE_PATH),
        "final_state_packet": rel(FINAL_STATE_PACKET_PATH),
        "next_status_packet": rel(NEXT_STATUS_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_guard_patch_receipt": rel(GUARD_PATCH_RECEIPT_PATH),
        "source_patched_localization_packet": rel(PATCHED_LOCALIZATION_PACKET_PATH),
    }

    receipt = {
        "schema_version": "r10000_observability_branch_close_and_bounded_protocol_freeze_receipt_v0",
        "receipt_type": "R10000_OBSERVABILITY_BRANCH_CLOSE_AND_BOUNDED_PROTOCOL_FREEZE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "source_failure_review_receipt_id": SOURCE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_localization_receipt_id": SOURCE_FAILED_LOCALIZATION_RECEIPT_ID,
        "source_r10000_signal_inspection_receipt_id": SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID,
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "close_and_freeze_summary": {
            "close_freeze_result": "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN",
            "branch_status": branch_closure["branch_status"],
            "protocol_freeze_status": bounded_protocol["freeze_status"],
            "protocol_id": bounded_protocol["protocol_id"],
            "accepted_final_signal_class": final_state["accepted_final_signal_class"],
            "accepted_driver_class": final_state["accepted_driver_class"],
            "requires_repair": final_state["requires_repair"],
            "requires_further_localization": final_state["requires_further_localization"],
            "larger_radius_authorized_now": final_state["larger_radius_authorized_now"],
            "close_and_freeze_only_no_rerun": True,
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "close_and_freeze_guards": guards_packet,
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
    print(f"r10000_close_freeze_receipt_id={receipt_id}")
    print(f"r10000_close_freeze_receipt_path=data/r10000_observability_branch_close_and_bounded_protocol_freeze_v0_receipts/{receipt_id}.json")
    print(f"bounded_protocol_freeze_path=data/r10000_observability_branch_close_and_bounded_protocol_freeze_v0/bounded_observability_protocol_freeze_v0.json")
    print(f"final_state_packet_path=data/r10000_observability_branch_close_and_bounded_protocol_freeze_v0/r10000_observability_branch_final_state_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
