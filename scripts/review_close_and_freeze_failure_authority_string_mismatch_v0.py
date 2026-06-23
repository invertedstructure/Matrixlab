#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_CLOSE_AND_FREEZE_FAILURE_AUTHORITY_STRING_MISMATCH_V0"
TARGET_UNIT_ID = "r10000.close_and_freeze.failure.authority_string_mismatch.review.v0"

SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID = "be986ecf"
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

OUT_DIR = ROOT / "data" / "r10000_close_and_freeze_failure_authority_string_mismatch_review_v0"
RECEIPT_DIR = ROOT / "data" / "r10000_close_and_freeze_failure_authority_string_mismatch_review_v0_receipts"

FAILURE_REVIEW_SURFACE_PATH = OUT_DIR / "r10000_close_and_freeze_failure_review_surface.json"
AUTHORITY_MISMATCH_REVIEW_PATH = OUT_DIR / "r10000_close_and_freeze_authority_string_mismatch_review.json"
SUBSTANTIVE_CLOSE_FREEZE_REVIEW_PATH = OUT_DIR / "r10000_close_and_freeze_substantive_finding_review.json"
AUTHORITY_CLASSIFICATION_PACKET_PATH = OUT_DIR / "r10000_close_and_freeze_authority_classification_packet.json"
FIX_AUTHORITY_PACKET_PATH = OUT_DIR / "r10000_close_and_freeze_authority_string_mismatch_fix_authority_packet.json"
REVIEW_DECISION_PATH = OUT_DIR / "r10000_close_and_freeze_failure_review_decision.json"
NEXT_DECISION_PACKET_PATH = OUT_DIR / "r10000_close_and_freeze_failure_review_next_decision_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r10000_close_and_freeze_failure_review_transition_trace.json"
REPORT_PATH = OUT_DIR / "r10000_close_and_freeze_failure_review_report.json"

FAILED_CLOSE_FREEZE_RECEIPT_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0_receipts" / f"{SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID}.json"
CLOSE_FREEZE_PLAN_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "r10000_close_and_freeze_plan.json"
CLOSE_FREEZE_SOURCE_SURFACE_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "r10000_close_and_freeze_source_surface.json"
BRANCH_CLOSURE_DECISION_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "r10000_observability_branch_closure_decision.json"
BOUNDED_PROTOCOL_FREEZE_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "bounded_observability_protocol_freeze_v0.json"
REUSABLE_PROTOCOL_REFERENCE_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "bounded_observability_protocol_reusable_reference_v0.json"
FINAL_STATE_PACKET_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "r10000_observability_branch_final_state_packet.json"
FAILED_NEXT_STATUS_PACKET_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "r10000_close_and_freeze_next_status_packet.json"
FAILED_TRANSITION_TRACE_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "r10000_close_and_freeze_transition_trace.json"
FAILED_REPORT_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "r10000_close_and_freeze_report.json"

GUARD_PATCH_RECEIPT_PATH = ROOT / "data" / "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0_receipts" / f"{SOURCE_GUARD_PATCH_RECEIPT_ID}.json"
PATCHED_LOCALIZATION_PACKET_PATH = ROOT / "data" / "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0" / "r10000_signal_localization_patched_acceptance_packet.json"
PATCHED_NEXT_DECISION_PACKET_PATH = ROOT / "data" / "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0" / "r10000_signal_localization_patched_acceptance_next_decision_packet.json"
GUARD_PATCH_REPORT_PATH = ROOT / "data" / "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0" / "r10000_signal_localization_guard_reference_only_acceptance_patch_report.json"

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
    FAILED_CLOSE_FREEZE_RECEIPT_PATH,
    CLOSE_FREEZE_PLAN_PATH,
    CLOSE_FREEZE_SOURCE_SURFACE_PATH,
    BRANCH_CLOSURE_DECISION_PATH,
    BOUNDED_PROTOCOL_FREEZE_PATH,
    REUSABLE_PROTOCOL_REFERENCE_PATH,
    FINAL_STATE_PACKET_PATH,
    FAILED_NEXT_STATUS_PACKET_PATH,
    FAILED_TRANSITION_TRACE_PATH,
    FAILED_REPORT_PATH,
    GUARD_PATCH_RECEIPT_PATH,
    PATCHED_LOCALIZATION_PACKET_PATH,
    PATCHED_NEXT_DECISION_PACKET_PATH,
    GUARD_PATCH_REPORT_PATH,
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
    "decision": "REVIEW_CLOSE_AND_FREEZE_FAILURE_AUTHORITY_STRING_MISMATCH",
    "scope": "review the failed close-and-freeze unit; determine whether the failure is only an authority string mismatch where prior close-or-freeze authority validly covers the explicit human-selected close-and-freeze refinement; preserve substantive close/freeze artifacts if supported; emit narrow fix/acceptance authority without rerunning or mutating prior artifacts",
    "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
    "authorized": [
        "consume failed close/freeze receipt and artifacts",
        "consume guard patch receipt and patched localization packet",
        "review close-or-freeze versus close-and-freeze authority wording",
        "review substantive close/freeze artifact validity",
        "emit authority classification packet",
        "emit fix/acceptance authority packet",
        "stop before patch acceptance, rerun, scaling, or row payload work",
    ],
    "not_authorized": [
        "rerunning radius-10000",
        "running radius above 10000",
        "running unbounded/no-cap harvest",
        "running any small probe",
        "modifying src/matrixlab/cli.py",
        "modifying src/matrixlab/r1000_post_closure_observability_harvest.py",
        "modifying failed close/freeze artifacts",
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
    failed = read_json(FAILED_CLOSE_FREEZE_RECEIPT_PATH)
    failed_summary = failed.get("close_and_freeze_summary", {})
    guard = read_json(GUARD_PATCH_RECEIPT_PATH)
    patched = read_json(PATCHED_LOCALIZATION_PACKET_PATH)
    patched_next = read_json(PATCHED_NEXT_DECISION_PACKET_PATH)
    branch = read_json(BRANCH_CLOSURE_DECISION_PATH)
    freeze = read_json(BOUNDED_PROTOCOL_FREEZE_PATH)
    final_state = read_json(FINAL_STATE_PACKET_PATH)
    failed_report = read_json(FAILED_REPORT_PATH)
    run_receipt = read_json(RUN_RECEIPT_PATH)
    rollup = read_json(ROLLUP_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if failed.get("receipt_id") != SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID:
        failures.append("failed_close_freeze_receipt_id_wrong")
    if failed.get("gate") != "FAIL":
        failures.append("failed_close_freeze_gate_not_fail")
    if failed.get("terminal", {}).get("stop_code") != "STOP_GATE_FAIL":
        failures.append("failed_close_freeze_terminal_not_gate_fail")
    if "guard_patch_not_recommending_close_freeze" not in failed.get("failures", []):
        failures.append("expected_guard_patch_recommendation_failure_missing")
    if "receipt_gate_not_PASS:FAIL" not in failed.get("failures", []):
        failures.append("expected_receipt_gate_failure_missing")

    if failed_summary.get("close_freeze_result") != "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN":
        failures.append("failed_summary_not_close_freeze_result")
    if failed_summary.get("branch_status") != "CLOSED":
        failures.append("failed_summary_branch_not_closed")
    if failed_summary.get("protocol_freeze_status") != "FROZEN_REUSABLE_REFERENCE":
        failures.append("failed_summary_protocol_not_frozen")
    if failed_summary.get("requires_repair") is not False or failed_summary.get("requires_further_localization") is not False:
        failures.append("failed_summary_requires_more_work")
    if failed_summary.get("larger_radius_authorized_now") is not False:
        failures.append("failed_summary_authorized_larger_radius")

    if guard.get("gate") != "PASS":
        failures.append("guard_patch_not_pass")
    guard_next = guard.get("r10000_guard_patch_summary", {}).get("recommended_next_handling")
    if guard_next != "DECIDE_CLOSE_OR_FREEZE_BOUNDED_OBSERVABILITY_PROTOCOL_AFTER_R10000_VOLATILE_ONLY_SIGNAL_V0":
        failures.append(f"guard_patch_unexpected_recommendation:{guard_next}")
    if patched.get("classification") != "R10000_LOCALIZATION_VOLATILE_RECEIPT_METADATA_ONLY_ACCEPTED_AFTER_REFERENCE_ONLY_GUARD_PATCH":
        failures.append("patched_classification_wrong")
    if patched.get("accepted_driver_class") != "RECEIPT_VOLATILITY_ONLY_NO_STRUCTURAL_SIGNAL_LOCALIZED":
        failures.append("patched_driver_wrong")
    if patched.get("requires_repair") is not False or patched.get("requires_further_localization") is not False:
        failures.append("patched_packet_requires_more_work")
    if patched_next.get("packet_status") != "R10000_SIGNAL_LOCALIZATION_REFERENCE_ONLY_GUARD_PATCH_ACCEPTED_READY_FOR_CLOSE_OR_FREEZE_DECISION":
        failures.append("patched_next_packet_not_close_or_freeze_ready")

    if branch.get("branch_status") != "CLOSED":
        failures.append("branch_artifact_not_closed")
    if freeze.get("freeze_status") != "FROZEN_REUSABLE_REFERENCE":
        failures.append("freeze_artifact_not_frozen")
    if final_state.get("packet_status") != "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN":
        failures.append("final_state_packet_not_closed_frozen")
    if final_state.get("larger_radius_authorized_now") is not False:
        failures.append("final_state_authorized_larger_radius")
    if final_state.get("auto_next_command") is not None:
        failures.append("final_state_hidden_next_command")

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
        if failed_report.get(key) != 0:
            failures.append(f"failed_report_boundary_count_not_zero:{key}:{failed_report.get(key)}")

    if run_receipt.get("gate") != "PASS" or rollup.get("gate") != "PASS":
        failures.append("r10000_run_or_rollup_not_pass")
    if run_receipt.get("radius_completed") != EXPECTED_RADIUS or rollup.get("radius_completed") != EXPECTED_RADIUS:
        failures.append("radius_not_10000")

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

def authority_string_mismatch_review() -> Dict[str, Any]:
    guard = read_json(GUARD_PATCH_RECEIPT_PATH)
    failed = read_json(FAILED_CLOSE_FREEZE_RECEIPT_PATH)
    plan = read_json(CLOSE_FREEZE_PLAN_PATH)
    patched_next = read_json(PATCHED_NEXT_DECISION_PACKET_PATH)

    prior_recommended = guard.get("r10000_guard_patch_summary", {}).get("recommended_next_handling")
    executed_unit = failed.get("unit_id")
    human_decision = failed.get("human_decision", {}).get("decision")
    packet_safe_choices = patched_next.get("safe_next_choices", [])

    close_or_freeze_authority = prior_recommended == "DECIDE_CLOSE_OR_FREEZE_BOUNDED_OBSERVABILITY_PROTOCOL_AFTER_R10000_VOLATILE_ONLY_SIGNAL_V0"
    executed_close_and_freeze = executed_unit == "DECIDE_CLOSE_AND_FREEZE_BOUNDED_OBSERVABILITY_PROTOCOL_AFTER_R10000_VOLATILE_ONLY_SIGNAL_V0"
    human_selected_close_and_freeze = human_decision == "CLOSE_AND_FREEZE" and plan.get("decision") == "close and freeze"

    if close_or_freeze_authority and executed_close_and_freeze and human_selected_close_and_freeze:
        classification = "CLOSE_OR_FREEZE_AUTHORITY_VALIDLY_COVERS_HUMAN_SELECTED_CLOSE_AND_FREEZE"
        authority_mismatch_only = True
    else:
        classification = "CLOSE_FREEZE_AUTHORITY_MISMATCH_REVIEW_INCONCLUSIVE"
        authority_mismatch_only = False

    return {
        "schema_version": "r10000_close_and_freeze_authority_string_mismatch_review_v0",
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "prior_recommended_next_handling": prior_recommended,
        "executed_unit": executed_unit,
        "human_decision": human_decision,
        "plan_decision": plan.get("decision"),
        "patched_next_packet_safe_choices": packet_safe_choices,
        "close_or_freeze_authority_present": close_or_freeze_authority,
        "executed_close_and_freeze": executed_close_and_freeze,
        "human_selected_close_and_freeze": human_selected_close_and_freeze,
        "authority_mismatch_only": authority_mismatch_only,
        "classification": classification,
        "interpretation": "The prior authority allowed close or freeze; the human selected the compound safe choice close-and-freeze. The failed unit rejected only the exact recommendation string, not the substantive authority or boundary behavior.",
    }

def substantive_close_freeze_review() -> Dict[str, Any]:
    failed = read_json(FAILED_CLOSE_FREEZE_RECEIPT_PATH)
    branch = read_json(BRANCH_CLOSURE_DECISION_PATH)
    freeze = read_json(BOUNDED_PROTOCOL_FREEZE_PATH)
    reference = read_json(REUSABLE_PROTOCOL_REFERENCE_PATH)
    final_state = read_json(FINAL_STATE_PACKET_PATH)
    next_status = read_json(FAILED_NEXT_STATUS_PACKET_PATH)
    report = read_json(FAILED_REPORT_PATH)
    patched = read_json(PATCHED_LOCALIZATION_PACKET_PATH)

    boundary_clean = all(report.get(key) == 0 for key in [
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
    ])

    supported = (
        failed.get("close_and_freeze_summary", {}).get("close_freeze_result") == "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN"
        and branch.get("branch_status") == "CLOSED"
        and freeze.get("freeze_status") == "FROZEN_REUSABLE_REFERENCE"
        and reference.get("reference_status") == "READY_FOR_REUSE"
        and final_state.get("packet_status") == "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN"
        and next_status.get("packet_status") == "CLOSED_AND_FROZEN_NO_NEXT_COMMAND"
        and patched.get("requires_repair") is False
        and patched.get("requires_further_localization") is False
        and boundary_clean
    )

    return {
        "schema_version": "r10000_close_and_freeze_substantive_finding_review_v0",
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "branch_status": branch.get("branch_status"),
        "protocol_freeze_status": freeze.get("freeze_status"),
        "reusable_reference_status": reference.get("reference_status"),
        "final_state_packet_status": final_state.get("packet_status"),
        "next_status_packet_status": next_status.get("packet_status"),
        "accepted_final_signal_class": final_state.get("accepted_final_signal_class"),
        "accepted_driver_class": final_state.get("accepted_driver_class"),
        "requires_repair": final_state.get("requires_repair"),
        "requires_further_localization": final_state.get("requires_further_localization"),
        "larger_radius_authorized_now": final_state.get("larger_radius_authorized_now"),
        "boundary_clean": boundary_clean,
        "substantive_close_freeze_supported_despite_gate_fail": supported,
    }

def build_authority_classification(authority_review: Dict[str, Any], substantive_review: Dict[str, Any]) -> Dict[str, Any]:
    if authority_review["authority_mismatch_only"] and substantive_review["substantive_close_freeze_supported_despite_gate_fail"]:
        classification = "AUTHORITY_STRING_MISMATCH_ONLY_ACCEPT_CLOSE_AND_FREEZE_AFTER_REVIEW"
        recommended = "PATCH_CLOSE_AND_FREEZE_ACCEPTANCE_AFTER_AUTHORITY_STRING_MISMATCH_REVIEW_V0"
        accept_substantive = True
    else:
        classification = "CLOSE_AND_FREEZE_FAILURE_REVIEW_INCONCLUSIVE"
        recommended = "REVIEW_CLOSE_AND_FREEZE_FAILURE_MANUALLY_V0"
        accept_substantive = False

    return {
        "schema_version": "r10000_close_and_freeze_authority_classification_packet_v0",
        "classification": classification,
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "authority_mismatch_classification": authority_review["classification"],
        "substantive_close_freeze_supported": substantive_review["substantive_close_freeze_supported_despite_gate_fail"],
        "accept_substantive_close_freeze_after_review": accept_substantive,
        "true_close_freeze_boundary_violation": False if accept_substantive else None,
        "recommended_next_handling": recommended,
    }

def build_fix_authority(classification_packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r10000_close_and_freeze_authority_string_mismatch_fix_authority_packet_v0",
        "packet_status": "AUTHORITY_STRING_MISMATCH_REVIEWED_NARROW_ACCEPTANCE_PATCH_AUTHORIZED" if classification_packet["classification"] == "AUTHORITY_STRING_MISMATCH_ONLY_ACCEPT_CLOSE_AND_FREEZE_AFTER_REVIEW" else "MANUAL_REVIEW_REQUIRED",
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "authority_classification": classification_packet["classification"],
        "authorized_next_unit": classification_packet["recommended_next_handling"],
        "required_fix_shape": [
            "do not rerun radius-10000",
            "do not inspect or materialize row payloads",
            "do not mutate failed close/freeze artifacts",
            "accept close-and-freeze as valid human-selected refinement of prior close-or-freeze authority",
            "preserve branch_status CLOSED and protocol_freeze_status FROZEN_REUSABLE_REFERENCE",
            "preserve terminal next_command_goal null",
            "emit PASS acceptance receipt and final status packet",
        ],
        "radius_10000_rerun_authorized_now": False,
        "larger_radius_authorized_now": False,
        "repair_authorized_in_this_review_unit": False,
        "recommended_next_handling": classification_packet["recommended_next_handling"],
    }

def validate_outputs(authority_review: Dict[str, Any], substantive_review: Dict[str, Any], classification_packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if authority_review.get("authority_mismatch_only") is not True:
        failures.append("authority_mismatch_only_not_true")
    if substantive_review.get("substantive_close_freeze_supported_despite_gate_fail") is not True:
        failures.append("substantive_close_freeze_not_supported")
    if classification_packet.get("classification") != "AUTHORITY_STRING_MISMATCH_ONLY_ACCEPT_CLOSE_AND_FREEZE_AFTER_REVIEW":
        failures.append(f"authority_classification_wrong:{classification_packet.get('classification')}")
    if classification_packet.get("accept_substantive_close_freeze_after_review") is not True:
        failures.append("substantive_close_freeze_not_accepted")
    if classification_packet.get("true_close_freeze_boundary_violation") is not False:
        failures.append("true_boundary_violation_marked")

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
        "failed_close_freeze_receipt_consumed_count",
        "failed_close_freeze_artifacts_consumed_count",
        "guard_patch_receipt_consumed_count",
        "failure_review_surface_emitted_count",
        "authority_mismatch_review_emitted_count",
        "substantive_close_freeze_review_emitted_count",
        "authority_classification_packet_emitted_count",
        "fix_authority_packet_emitted_count",
        "review_decision_emitted_count",
        "next_decision_packet_emitted_count",
        "authority_mismatch_only_count",
        "substantive_close_freeze_supported_count",
        "accept_close_and_freeze_after_review_count",
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
    if terminal.get("stop_code") != "STOP_CLOSE_AND_FREEZE_FAILURE_REVIEW_COMPLETE_AUTHORITY_STRING_MISMATCH_PATCH_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    authority_review = authority_string_mismatch_review()
    substantive_review = substantive_close_freeze_review()
    classification_packet = build_authority_classification(authority_review, substantive_review)
    fix_authority = build_fix_authority(classification_packet)

    failed = read_json(FAILED_CLOSE_FREEZE_RECEIPT_PATH)
    guard = read_json(GUARD_PATCH_RECEIPT_PATH)

    review_surface = {
        "schema_version": "r10000_close_and_freeze_failure_review_surface_v0",
        "review_surface_id": sha8({
            "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
            "classification": classification_packet["classification"],
        }),
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "failed_receipt_gate": failed.get("gate"),
        "failed_receipt_failures": failed.get("failures"),
        "guard_patch_recommended_next": guard.get("r10000_guard_patch_summary", {}).get("recommended_next_handling"),
        "executed_unit": failed.get("unit_id"),
        "human_decision": failed.get("human_decision", {}).get("decision"),
        "authority_mismatch_classification": authority_review["classification"],
        "substantive_close_freeze_supported": substantive_review["substantive_close_freeze_supported_despite_gate_fail"],
        "recommended_next_handling": classification_packet["recommended_next_handling"],
    }

    decision = {
        "schema_version": "r10000_close_and_freeze_failure_review_decision_v0",
        "decision_id": sha8({
            "unit_id": UNIT_ID,
            "source_failed": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
            "classification": classification_packet["classification"],
        }),
        "decision_status": "CLOSE_AND_FREEZE_FAILURE_REVIEW_ACCEPTS_AUTHORITY_STRING_MISMATCH_ONLY",
        "authority_classification": classification_packet["classification"],
        "authority_mismatch_classification": authority_review["classification"],
        "substantive_close_freeze_supported": substantive_review["substantive_close_freeze_supported_despite_gate_fail"],
        "accepted_branch_status": substantive_review["branch_status"],
        "accepted_protocol_freeze_status": substantive_review["protocol_freeze_status"],
        "accepted_final_signal_class": substantive_review["accepted_final_signal_class"],
        "accepted_driver_class": substantive_review["accepted_driver_class"],
        "true_close_freeze_boundary_violation": classification_packet["true_close_freeze_boundary_violation"],
        "review_only_no_rerun": True,
        "recommended_next_handling": classification_packet["recommended_next_handling"],
    }

    next_decision = {
        "schema_version": "r10000_close_and_freeze_failure_review_next_decision_packet_v0",
        "packet_status": "CLOSE_AND_FREEZE_FAILURE_REVIEW_COMPLETE_AUTHORITY_STRING_MISMATCH_PATCH_READY",
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "authority_classification": classification_packet["classification"],
        "substantive_close_freeze_to_preserve": {
            "branch_status": substantive_review["branch_status"],
            "protocol_freeze_status": substantive_review["protocol_freeze_status"],
            "accepted_final_signal_class": substantive_review["accepted_final_signal_class"],
            "accepted_driver_class": substantive_review["accepted_driver_class"],
        },
        "safe_next_choices": [
            "patch close-and-freeze acceptance as a valid human-selected refinement of close-or-freeze",
            "preserve emitted close/freeze artifacts",
            "do not rerun radius-10000",
            "do not inspect row payloads or closed groups",
            "do not authorize a larger radius in this correction",
        ],
        "recommended_next_handling": classification_packet["recommended_next_handling"],
        "auto_next_command": None,
    }

    report = {
        "schema_version": "r10000_close_and_freeze_failure_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "failed_close_freeze_receipt_consumed_count": 1,
        "failed_close_freeze_artifacts_consumed_count": 1,
        "guard_patch_receipt_consumed_count": 1,
        "failure_review_surface_emitted_count": 1,
        "authority_mismatch_review_emitted_count": 1,
        "substantive_close_freeze_review_emitted_count": 1,
        "authority_classification_packet_emitted_count": 1,
        "fix_authority_packet_emitted_count": 1,
        "review_decision_emitted_count": 1,
        "next_decision_packet_emitted_count": 1,
        "authority_mismatch_only_count": 1 if authority_review["authority_mismatch_only"] else 0,
        "substantive_close_freeze_supported_count": 1 if substantive_review["substantive_close_freeze_supported_despite_gate_fail"] else 0,
        "accept_close_and_freeze_after_review_count": 1 if classification_packet["accept_substantive_close_freeze_after_review"] else 0,
        "true_close_freeze_boundary_violation_count": 1 if classification_packet["true_close_freeze_boundary_violation"] else 0,
        "accepted_branch_status": substantive_review["branch_status"],
        "accepted_protocol_freeze_status": substantive_review["protocol_freeze_status"],
        "accepted_final_signal_class": substantive_review["accepted_final_signal_class"],
        "accepted_driver_class": substantive_review["accepted_driver_class"],
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
        "recommended_next_handling": classification_packet["recommended_next_handling"],
    }

    trace = {
        "schema_version": "r10000_close_and_freeze_failure_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_failed_close_freeze_receipt",
                "question": "failed only on authority recommendation string mismatch",
                "answer": "guard_patch_not_recommending_close_freeze" in failed.get("failures", []),
                "taken": "review_authority_string",
            },
            {
                "step": "review_authority_string",
                "question": "does close-or-freeze authority cover human-selected close-and-freeze",
                "answer": authority_review["authority_mismatch_only"],
                "taken": "review_substantive_close_freeze_artifacts",
            },
            {
                "step": "review_substantive_close_freeze_artifacts",
                "question": "are close/freeze artifacts valid and boundary clean",
                "answer": substantive_review["substantive_close_freeze_supported_despite_gate_fail"],
                "taken": "emit_acceptance_patch_authority",
            },
            {
                "step": "emit_acceptance_patch_authority",
                "question": "patch now",
                "answer": False,
                "taken": "STOP_CLOSE_AND_FREEZE_FAILURE_REVIEW_COMPLETE_AUTHORITY_STRING_MISMATCH_PATCH_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CLOSE_AND_FREEZE_FAILURE_REVIEW_COMPLETE_AUTHORITY_STRING_MISMATCH_PATCH_REQUIRED",
            "next_command_goal": None,
        },
    }

    write_json(FAILURE_REVIEW_SURFACE_PATH, review_surface)
    write_json(AUTHORITY_MISMATCH_REVIEW_PATH, authority_review)
    write_json(SUBSTANTIVE_CLOSE_FREEZE_REVIEW_PATH, substantive_review)
    write_json(AUTHORITY_CLASSIFICATION_PACKET_PATH, classification_packet)
    write_json(FIX_AUTHORITY_PACKET_PATH, fix_authority)
    write_json(REVIEW_DECISION_PATH, decision)
    write_json(NEXT_DECISION_PACKET_PATH, next_decision)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(authority_review, substantive_review, classification_packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "CLOSE_FREEZE_FAILURE_REVIEW_0_FAILED_RECEIPT_CONSUMED": True,
        "CLOSE_FREEZE_FAILURE_REVIEW_1_STRING_MISMATCH_CONFIRMED": authority_review["authority_mismatch_only"] is True,
        "CLOSE_FREEZE_FAILURE_REVIEW_2_SUBSTANTIVE_CLOSE_FREEZE_SUPPORTED": substantive_review["substantive_close_freeze_supported_despite_gate_fail"] is True,
        "CLOSE_FREEZE_FAILURE_REVIEW_3_AUTHORITY_CLASSIFIED": classification_packet["classification"] == "AUTHORITY_STRING_MISMATCH_ONLY_ACCEPT_CLOSE_AND_FREEZE_AFTER_REVIEW",
        "CLOSE_FREEZE_FAILURE_REVIEW_4_FIX_AUTHORITY_PACKET_EMITTED": report["fix_authority_packet_emitted_count"] == 1,
        "CLOSE_FREEZE_FAILURE_REVIEW_5_NO_RERUN_OR_PROBE": report["radius_10000_rerun_count"] == 0 and report["new_small_probe_count"] == 0,
        "CLOSE_FREEZE_FAILURE_REVIEW_6_NO_UNBOUNDED_OR_RADIUS_ABOVE_10000": report["unbounded_or_no_cap_run_count"] == 0 and report["radius_above_10000_run_count"] == 0,
        "CLOSE_FREEZE_FAILURE_REVIEW_7_NO_LARGER_RADIUS": report["larger_bounded_radius_run_count"] == 0,
        "CLOSE_FREEZE_FAILURE_REVIEW_8_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0 and report["row_payload_inspected_count"] == 0,
        "CLOSE_FREEZE_FAILURE_REVIEW_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "CLOSE_FREEZE_FAILURE_REVIEW_10_NO_REPAIR_OR_TAXONOMY": report["repair_executed_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "CLOSE_FREEZE_FAILURE_REVIEW_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
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
        "review_only_no_rerun": True,
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
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "classification": classification_packet["classification"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "failure_review_surface": rel(FAILURE_REVIEW_SURFACE_PATH),
        "authority_mismatch_review": rel(AUTHORITY_MISMATCH_REVIEW_PATH),
        "substantive_close_freeze_review": rel(SUBSTANTIVE_CLOSE_FREEZE_REVIEW_PATH),
        "authority_classification_packet": rel(AUTHORITY_CLASSIFICATION_PACKET_PATH),
        "fix_authority_packet": rel(FIX_AUTHORITY_PACKET_PATH),
        "review_decision": rel(REVIEW_DECISION_PATH),
        "next_decision_packet": rel(NEXT_DECISION_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "failed_close_freeze_receipt": rel(FAILED_CLOSE_FREEZE_RECEIPT_PATH),
        "failed_branch_closure_decision": rel(BRANCH_CLOSURE_DECISION_PATH),
        "failed_bounded_protocol_freeze": rel(BOUNDED_PROTOCOL_FREEZE_PATH),
        "failed_final_state_packet": rel(FINAL_STATE_PACKET_PATH),
    }

    receipt = {
        "schema_version": "r10000_close_and_freeze_failure_authority_string_mismatch_review_receipt_v0",
        "receipt_type": "R10000_CLOSE_AND_FREEZE_FAILURE_AUTHORITY_STRING_MISMATCH_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
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
        "close_and_freeze_failure_review_summary": {
            "review_result": decision["decision_status"],
            "authority_classification": classification_packet["classification"],
            "authority_mismatch_classification": authority_review["classification"],
            "prior_recommended_next_handling": authority_review["prior_recommended_next_handling"],
            "executed_unit": authority_review["executed_unit"],
            "human_decision": authority_review["human_decision"],
            "substantive_close_freeze_supported": substantive_review["substantive_close_freeze_supported_despite_gate_fail"],
            "accepted_branch_status": substantive_review["branch_status"],
            "accepted_protocol_freeze_status": substantive_review["protocol_freeze_status"],
            "accepted_final_signal_class": substantive_review["accepted_final_signal_class"],
            "accepted_driver_class": substantive_review["accepted_driver_class"],
            "true_close_freeze_boundary_violation": classification_packet["true_close_freeze_boundary_violation"],
            "review_only_no_rerun": True,
            "recommended_next_handling": classification_packet["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "close_and_freeze_failure_review_guards": guards_packet,
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
    print(f"close_freeze_failure_review_receipt_id={receipt_id}")
    print(f"close_freeze_failure_review_receipt_path=data/r10000_close_and_freeze_failure_authority_string_mismatch_review_v0_receipts/{receipt_id}.json")
    print(f"fix_authority_packet_path=data/r10000_close_and_freeze_failure_authority_string_mismatch_review_v0/r10000_close_and_freeze_authority_string_mismatch_fix_authority_packet.json")
    print(f"next_decision_packet_path=data/r10000_close_and_freeze_failure_authority_string_mismatch_review_v0/r10000_close_and_freeze_failure_review_next_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
