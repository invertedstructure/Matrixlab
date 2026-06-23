#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PATCH_CLOSE_AND_FREEZE_ACCEPTANCE_AFTER_AUTHORITY_STRING_MISMATCH_REVIEW_V0"
TARGET_UNIT_ID = "r10000.close_and_freeze.acceptance_after_authority_string_mismatch.patch.v0"

SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID = "f39ceae9"
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

OUT_DIR = ROOT / "data" / "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0"
RECEIPT_DIR = ROOT / "data" / "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0_receipts"

PATCH_PLAN_PATH = OUT_DIR / "r10000_close_and_freeze_acceptance_patch_plan.json"
SOURCE_SURFACE_PATH = OUT_DIR / "r10000_close_and_freeze_acceptance_source_surface.json"
AUTHORITY_ACCEPTANCE_RECHECK_PATH = OUT_DIR / "r10000_close_and_freeze_authority_acceptance_recheck.json"
PATCHED_ACCEPTANCE_PACKET_PATH = OUT_DIR / "r10000_close_and_freeze_patched_acceptance_packet.json"
FINAL_ACCEPTED_STATE_PACKET_PATH = OUT_DIR / "r10000_close_and_freeze_final_accepted_state_packet.json"
BOUNDED_PROTOCOL_FINAL_REFERENCE_PATH = OUT_DIR / "bounded_observability_protocol_final_reference_v0.json"
PATCHED_DECISION_PATH = OUT_DIR / "r10000_close_and_freeze_patched_acceptance_decision.json"
NEXT_STATUS_PACKET_PATH = OUT_DIR / "r10000_close_and_freeze_acceptance_next_status_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r10000_close_and_freeze_acceptance_patch_transition_trace.json"
REPORT_PATH = OUT_DIR / "r10000_close_and_freeze_acceptance_patch_report.json"

FAILURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r10000_close_and_freeze_failure_authority_string_mismatch_review_v0_receipts" / f"{SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID}.json"
FIX_AUTHORITY_PACKET_PATH = ROOT / "data" / "r10000_close_and_freeze_failure_authority_string_mismatch_review_v0" / "r10000_close_and_freeze_authority_string_mismatch_fix_authority_packet.json"
FAILURE_REVIEW_NEXT_PACKET_PATH = ROOT / "data" / "r10000_close_and_freeze_failure_authority_string_mismatch_review_v0" / "r10000_close_and_freeze_failure_review_next_decision_packet.json"
AUTHORITY_CLASSIFICATION_PACKET_PATH = ROOT / "data" / "r10000_close_and_freeze_failure_authority_string_mismatch_review_v0" / "r10000_close_and_freeze_authority_classification_packet.json"
SUBSTANTIVE_REVIEW_PATH = ROOT / "data" / "r10000_close_and_freeze_failure_authority_string_mismatch_review_v0" / "r10000_close_and_freeze_substantive_finding_review.json"

FAILED_CLOSE_FREEZE_RECEIPT_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0_receipts" / f"{SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID}.json"
BRANCH_CLOSURE_DECISION_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "r10000_observability_branch_closure_decision.json"
BOUNDED_PROTOCOL_FREEZE_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "bounded_observability_protocol_freeze_v0.json"
REUSABLE_PROTOCOL_REFERENCE_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "bounded_observability_protocol_reusable_reference_v0.json"
FAILED_FINAL_STATE_PACKET_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "r10000_observability_branch_final_state_packet.json"
FAILED_NEXT_STATUS_PACKET_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "r10000_close_and_freeze_next_status_packet.json"
FAILED_REPORT_PATH = ROOT / "data" / "r10000_observability_branch_close_and_bounded_protocol_freeze_v0" / "r10000_close_and_freeze_report.json"

GUARD_PATCH_RECEIPT_PATH = ROOT / "data" / "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0_receipts" / f"{SOURCE_GUARD_PATCH_RECEIPT_ID}.json"
PATCHED_LOCALIZATION_PACKET_PATH = ROOT / "data" / "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0" / "r10000_signal_localization_patched_acceptance_packet.json"

LOCALIZATION_FAILURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r10000_distinguishable_signal_localization_failure_protected_key_hits_review_v0_receipts" / f"{SOURCE_FAILURE_REVIEW_RECEIPT_ID}.json"
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
    FAILURE_REVIEW_RECEIPT_PATH,
    FIX_AUTHORITY_PACKET_PATH,
    FAILURE_REVIEW_NEXT_PACKET_PATH,
    AUTHORITY_CLASSIFICATION_PACKET_PATH,
    SUBSTANTIVE_REVIEW_PATH,
    FAILED_CLOSE_FREEZE_RECEIPT_PATH,
    BRANCH_CLOSURE_DECISION_PATH,
    BOUNDED_PROTOCOL_FREEZE_PATH,
    REUSABLE_PROTOCOL_REFERENCE_PATH,
    FAILED_FINAL_STATE_PACKET_PATH,
    FAILED_NEXT_STATUS_PACKET_PATH,
    FAILED_REPORT_PATH,
    GUARD_PATCH_RECEIPT_PATH,
    PATCHED_LOCALIZATION_PACKET_PATH,
    LOCALIZATION_FAILURE_REVIEW_RECEIPT_PATH,
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
    "decision": "PATCH_CLOSE_AND_FREEZE_ACCEPTANCE_AFTER_AUTHORITY_STRING_MISMATCH_REVIEW",
    "scope": "accept the previously emitted close-and-freeze artifacts as final after the authority string mismatch review; close the R10000 branch and freeze the bounded observability protocol with a PASS receipt; do not rerun, mutate prior artifacts, or authorize hidden next work",
    "source_close_freeze_failure_review_receipt_id": SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID,
    "authorized": [
        "consume close/freeze failure review receipt",
        "consume authority string mismatch fix authority packet",
        "consume failed close/freeze artifacts as source evidence",
        "accept close-and-freeze as valid human-selected refinement of close-or-freeze",
        "emit final accepted close/freeze packet",
        "emit final bounded observability protocol reference",
        "stop with no next command goal",
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
    review = read_json(FAILURE_REVIEW_RECEIPT_PATH)
    authority = read_json(FIX_AUTHORITY_PACKET_PATH)
    classification = read_json(AUTHORITY_CLASSIFICATION_PACKET_PATH)
    substantive = read_json(SUBSTANTIVE_REVIEW_PATH)
    failed = read_json(FAILED_CLOSE_FREEZE_RECEIPT_PATH)
    branch = read_json(BRANCH_CLOSURE_DECISION_PATH)
    freeze = read_json(BOUNDED_PROTOCOL_FREEZE_PATH)
    reference = read_json(REUSABLE_PROTOCOL_REFERENCE_PATH)
    final_state = read_json(FAILED_FINAL_STATE_PACKET_PATH)
    failed_next = read_json(FAILED_NEXT_STATUS_PACKET_PATH)
    failed_report = read_json(FAILED_REPORT_PATH)
    guard = read_json(GUARD_PATCH_RECEIPT_PATH)
    patched_localization = read_json(PATCHED_LOCALIZATION_PACKET_PATH)
    run_receipt = read_json(RUN_RECEIPT_PATH)
    rollup = read_json(ROLLUP_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if review.get("receipt_id") != SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID:
        failures.append("close_freeze_failure_review_receipt_id_wrong")
    if review.get("gate") != "PASS":
        failures.append("close_freeze_failure_review_gate_not_pass")
    if review.get("close_and_freeze_failure_review_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("failure_review_not_recommending_this_patch")
    if authority.get("packet_status") != "AUTHORITY_STRING_MISMATCH_REVIEWED_NARROW_ACCEPTANCE_PATCH_AUTHORIZED":
        failures.append("authority_packet_not_patch_authorized")
    if authority.get("authorized_next_unit") != UNIT_ID:
        failures.append("authority_packet_authorized_next_wrong")
    if authority.get("radius_10000_rerun_authorized_now") is not False:
        failures.append("authority_packet_allows_rerun")
    if authority.get("larger_radius_authorized_now") is not False:
        failures.append("authority_packet_allows_larger_radius")
    if authority.get("repair_authorized_in_this_review_unit") is not False:
        failures.append("authority_packet_allows_repair")

    if classification.get("classification") != "AUTHORITY_STRING_MISMATCH_ONLY_ACCEPT_CLOSE_AND_FREEZE_AFTER_REVIEW":
        failures.append("classification_packet_wrong")
    if classification.get("accept_substantive_close_freeze_after_review") is not True:
        failures.append("classification_does_not_accept_substantive_close_freeze")
    if classification.get("true_close_freeze_boundary_violation") is not False:
        failures.append("classification_marks_true_boundary_violation")
    if substantive.get("substantive_close_freeze_supported_despite_gate_fail") is not True:
        failures.append("substantive_review_not_supported")

    if failed.get("receipt_id") != SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID:
        failures.append("failed_close_freeze_receipt_id_wrong")
    if failed.get("gate") != "FAIL":
        failures.append("failed_close_freeze_not_fail")
    if "guard_patch_not_recommending_close_freeze" not in failed.get("failures", []):
        failures.append("expected_authority_string_failure_missing")
    if branch.get("branch_status") != "CLOSED":
        failures.append("branch_not_closed")
    if freeze.get("freeze_status") != "FROZEN_REUSABLE_REFERENCE":
        failures.append("protocol_not_frozen")
    if reference.get("reference_status") != "READY_FOR_REUSE":
        failures.append("reference_not_ready")
    if final_state.get("packet_status") != "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN":
        failures.append("final_state_not_closed_frozen")
    if final_state.get("auto_next_command") is not None:
        failures.append("final_state_has_auto_next_command")
    if failed_next.get("packet_status") != "CLOSED_AND_FROZEN_NO_NEXT_COMMAND":
        failures.append("failed_next_status_not_closed_frozen")
    if failed_next.get("auto_next_command") is not None:
        failures.append("failed_next_has_auto_next_command")

    if guard.get("gate") != "PASS":
        failures.append("guard_patch_not_pass")
    if patched_localization.get("accepted_driver_class") != "RECEIPT_VOLATILITY_ONLY_NO_STRUCTURAL_SIGNAL_LOCALIZED":
        failures.append("patched_localization_driver_wrong")
    if patched_localization.get("requires_repair") is not False or patched_localization.get("requires_further_localization") is not False:
        failures.append("patched_localization_requires_more_work")

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
            failures.append(f"failed_close_freeze_boundary_count_not_zero:{key}:{failed_report.get(key)}")

    if run_receipt.get("gate") != "PASS" or rollup.get("gate") != "PASS":
        failures.append("r10000_run_or_rollup_not_pass")
    if run_receipt.get("radius_completed") != EXPECTED_RADIUS or rollup.get("radius_completed") != EXPECTED_RADIUS:
        failures.append("radius_not_10000")
    if run_receipt.get("observation_receipt_count") != EXPECTED_RADIUS or rollup.get("observation_receipt_count") != EXPECTED_RADIUS:
        failures.append("observation_count_not_10000")

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
    review = read_json(FAILURE_REVIEW_RECEIPT_PATH)
    authority = read_json(FIX_AUTHORITY_PACKET_PATH)
    failed = read_json(FAILED_CLOSE_FREEZE_RECEIPT_PATH)
    branch = read_json(BRANCH_CLOSURE_DECISION_PATH)
    freeze = read_json(BOUNDED_PROTOCOL_FREEZE_PATH)
    final_state = read_json(FAILED_FINAL_STATE_PACKET_PATH)
    patched_localization = read_json(PATCHED_LOCALIZATION_PACKET_PATH)
    return {
        "schema_version": "r10000_close_and_freeze_acceptance_source_surface_v0",
        "source_close_freeze_failure_review_receipt_id": SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "failure_review_summary": review.get("close_and_freeze_failure_review_summary"),
        "fix_authority_packet": authority,
        "failed_close_freeze_summary": failed.get("close_and_freeze_summary"),
        "branch_closure_decision": branch,
        "bounded_protocol_freeze": freeze,
        "final_state_packet": final_state,
        "patched_localization_packet": patched_localization,
    }

def authority_acceptance_recheck() -> Dict[str, Any]:
    review = read_json(FAILURE_REVIEW_RECEIPT_PATH)
    authority = read_json(FIX_AUTHORITY_PACKET_PATH)
    classification = read_json(AUTHORITY_CLASSIFICATION_PACKET_PATH)
    substantive = read_json(SUBSTANTIVE_REVIEW_PATH)
    failed_report = read_json(FAILED_REPORT_PATH)
    branch = read_json(BRANCH_CLOSURE_DECISION_PATH)
    freeze = read_json(BOUNDED_PROTOCOL_FREEZE_PATH)
    final_state = read_json(FAILED_FINAL_STATE_PACKET_PATH)

    boundary_counts = {
        key: failed_report.get(key) for key in [
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
        ]
    }
    boundary_clean = all(v == 0 for v in boundary_counts.values())

    accepted = (
        review.get("gate") == "PASS"
        and authority.get("packet_status") == "AUTHORITY_STRING_MISMATCH_REVIEWED_NARROW_ACCEPTANCE_PATCH_AUTHORIZED"
        and classification.get("classification") == "AUTHORITY_STRING_MISMATCH_ONLY_ACCEPT_CLOSE_AND_FREEZE_AFTER_REVIEW"
        and classification.get("accept_substantive_close_freeze_after_review") is True
        and substantive.get("substantive_close_freeze_supported_despite_gate_fail") is True
        and branch.get("branch_status") == "CLOSED"
        and freeze.get("freeze_status") == "FROZEN_REUSABLE_REFERENCE"
        and final_state.get("packet_status") == "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN"
        and final_state.get("larger_radius_authorized_now") is False
        and final_state.get("auto_next_command") is None
        and boundary_clean
    )

    return {
        "schema_version": "r10000_close_and_freeze_authority_acceptance_recheck_v0",
        "source_close_freeze_failure_review_receipt_id": SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "authority_packet_status": authority.get("packet_status"),
        "authority_classification": classification.get("classification"),
        "substantive_close_freeze_supported": substantive.get("substantive_close_freeze_supported_despite_gate_fail"),
        "branch_status": branch.get("branch_status"),
        "protocol_freeze_status": freeze.get("freeze_status"),
        "final_state_packet_status": final_state.get("packet_status"),
        "boundary_counts": boundary_counts,
        "boundary_clean": boundary_clean,
        "authority_acceptance_passed": accepted,
    }

def validate_outputs(recheck: Dict[str, Any], accepted_state: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if recheck.get("authority_acceptance_passed") is not True:
        failures.append("authority_acceptance_not_passed")
    if accepted_state.get("packet_status") != "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN_FINAL_ACCEPTED":
        failures.append("accepted_state_packet_status_wrong")
    if accepted_state.get("branch_status") != "CLOSED":
        failures.append("accepted_state_branch_not_closed")
    if accepted_state.get("protocol_freeze_status") != "FROZEN_REUSABLE_REFERENCE":
        failures.append("accepted_state_protocol_not_frozen")
    if accepted_state.get("auto_next_command") is not None:
        failures.append("accepted_state_auto_next_not_null")
    if accepted_state.get("recommended_next_handling") is not None:
        failures.append("accepted_state_recommended_next_not_null")

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
        "close_freeze_failure_review_receipt_consumed_count",
        "fix_authority_packet_consumed_count",
        "failed_close_freeze_receipt_consumed_count",
        "failed_close_freeze_artifacts_consumed_count",
        "source_surface_emitted_count",
        "authority_acceptance_recheck_emitted_count",
        "patched_acceptance_packet_emitted_count",
        "final_accepted_state_packet_emitted_count",
        "bounded_protocol_final_reference_emitted_count",
        "patched_decision_emitted_count",
        "next_status_packet_emitted_count",
        "authority_acceptance_passed_count",
        "final_close_freeze_acceptance_count",
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
    if terminal.get("stop_code") != "STOP_R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN_FINAL_ACCEPTED":
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
    recheck = authority_acceptance_recheck()
    branch = read_json(BRANCH_CLOSURE_DECISION_PATH)
    freeze = read_json(BOUNDED_PROTOCOL_FREEZE_PATH)
    reference = read_json(REUSABLE_PROTOCOL_REFERENCE_PATH)
    final_state = read_json(FAILED_FINAL_STATE_PACKET_PATH)
    substantive = read_json(SUBSTANTIVE_REVIEW_PATH)

    patch_plan = {
        "schema_version": "r10000_close_and_freeze_acceptance_patch_plan_v0",
        "unit_id": UNIT_ID,
        "source_close_freeze_failure_review_receipt_id": SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "mode": "acceptance_patch_only_no_rerun_no_prior_artifact_mutation",
        "correction": "accept close-and-freeze as valid human-selected refinement of prior close-or-freeze authority after review",
        "not_authorized": HUMAN_DECISION["not_authorized"],
    }

    patched_acceptance_packet = {
        "schema_version": "r10000_close_and_freeze_patched_acceptance_packet_v0",
        "packet_status": "CLOSE_AND_FREEZE_ACCEPTED_AFTER_AUTHORITY_STRING_MISMATCH_REVIEW",
        "source_close_freeze_failure_review_receipt_id": SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "accepted_authority_classification": "AUTHORITY_STRING_MISMATCH_ONLY_ACCEPT_CLOSE_AND_FREEZE_AFTER_REVIEW",
        "accepted_branch_status": branch.get("branch_status"),
        "accepted_protocol_freeze_status": freeze.get("freeze_status"),
        "accepted_final_signal_class": final_state.get("accepted_final_signal_class"),
        "accepted_driver_class": final_state.get("accepted_driver_class"),
        "requires_repair": False,
        "requires_further_localization": False,
        "larger_radius_authorized_now": False,
        "recommended_next_handling": None,
        "auto_next_command": None,
    }

    final_accepted_state = {
        "schema_version": "r10000_close_and_freeze_final_accepted_state_packet_v0",
        "packet_status": "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN_FINAL_ACCEPTED",
        "branch_status": branch.get("branch_status"),
        "protocol_freeze_status": freeze.get("freeze_status"),
        "protocol_id": freeze.get("protocol_id"),
        "accepted_final_signal_class": final_state.get("accepted_final_signal_class"),
        "accepted_driver_class": final_state.get("accepted_driver_class"),
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "source_close_freeze_failure_review_receipt_id": SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID,
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "requires_repair": False,
        "requires_further_localization": False,
        "larger_radius_authorized_now": False,
        "safe_future_options": final_state.get("safe_future_options", []),
        "recommended_next_handling": None,
        "auto_next_command": None,
    }

    final_reference = {
        "schema_version": "bounded_observability_protocol_final_reference_v0",
        "reference_status": "FINAL_ACCEPTED_REUSABLE_REFERENCE",
        "protocol_id": freeze.get("protocol_id"),
        "source_freeze_artifact": rel(BOUNDED_PROTOCOL_FREEZE_PATH),
        "source_reusable_reference_artifact": rel(REUSABLE_PROTOCOL_REFERENCE_PATH),
        "source_final_accepted_state_packet": rel(FINAL_ACCEPTED_STATE_PACKET_PATH),
        "bounded_protocol_steps": freeze.get("bounded_protocol_steps"),
        "decision_graph": freeze.get("decision_graph"),
        "frozen_lessons": freeze.get("frozen_lessons"),
        "hard_guards": freeze.get("hard_guards"),
        "reuse_rule": reference.get("reuse_rule"),
    }

    decision = {
        "schema_version": "r10000_close_and_freeze_patched_acceptance_decision_v0",
        "decision_id": sha8({
            "unit_id": UNIT_ID,
            "source_review": SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID,
            "branch_status": branch.get("branch_status"),
            "freeze_status": freeze.get("freeze_status"),
        }),
        "decision_status": "R10000_CLOSE_AND_FREEZE_ACCEPTED_AFTER_AUTHORITY_STRING_MISMATCH_REVIEW",
        "accepted_branch_status": branch.get("branch_status"),
        "accepted_protocol_freeze_status": freeze.get("freeze_status"),
        "accepted_final_signal_class": final_state.get("accepted_final_signal_class"),
        "accepted_driver_class": final_state.get("accepted_driver_class"),
        "authority_acceptance_passed": recheck["authority_acceptance_passed"],
        "substantive_close_freeze_supported": substantive.get("substantive_close_freeze_supported_despite_gate_fail"),
        "patch_only_no_rerun": True,
        "recommended_next_handling": None,
    }

    next_status = {
        "schema_version": "r10000_close_and_freeze_acceptance_next_status_packet_v0",
        "packet_status": "R10000_BRANCH_CLOSED_PROTOCOL_FROZEN_FINAL_NO_NEXT_COMMAND",
        "source_close_freeze_acceptance_decision": rel(PATCHED_DECISION_PATH),
        "final_accepted_state_packet": rel(FINAL_ACCEPTED_STATE_PACKET_PATH),
        "bounded_protocol_final_reference": rel(BOUNDED_PROTOCOL_FINAL_REFERENCE_PATH),
        "recommended_next_handling": None,
        "auto_next_command": None,
    }

    report = {
        "schema_version": "r10000_close_and_freeze_acceptance_patch_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_close_freeze_failure_review_receipt_id": SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_close_freeze_receipt_id": SOURCE_FAILED_CLOSE_FREEZE_RECEIPT_ID,
        "source_guard_patch_receipt_id": SOURCE_GUARD_PATCH_RECEIPT_ID,
        "close_freeze_failure_review_receipt_consumed_count": 1,
        "fix_authority_packet_consumed_count": 1,
        "failed_close_freeze_receipt_consumed_count": 1,
        "failed_close_freeze_artifacts_consumed_count": 1,
        "source_surface_emitted_count": 1,
        "authority_acceptance_recheck_emitted_count": 1,
        "patched_acceptance_packet_emitted_count": 1,
        "final_accepted_state_packet_emitted_count": 1,
        "bounded_protocol_final_reference_emitted_count": 1,
        "patched_decision_emitted_count": 1,
        "next_status_packet_emitted_count": 1,
        "authority_acceptance_passed_count": 1 if recheck["authority_acceptance_passed"] else 0,
        "final_close_freeze_acceptance_count": 1 if final_accepted_state["packet_status"] == "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN_FINAL_ACCEPTED" else 0,
        "accepted_branch_status": final_accepted_state["branch_status"],
        "accepted_protocol_freeze_status": final_accepted_state["protocol_freeze_status"],
        "accepted_final_signal_class": final_accepted_state["accepted_final_signal_class"],
        "accepted_driver_class": final_accepted_state["accepted_driver_class"],
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
        "schema_version": "r10000_close_and_freeze_acceptance_patch_transition_trace_v0",
        "trace": [
            {
                "step": "consume_authority_string_mismatch_review",
                "question": "was close-and-freeze accepted as human-selected refinement",
                "answer": True,
                "taken": "authority_acceptance_recheck",
            },
            {
                "step": "authority_acceptance_recheck",
                "question": "are failed close/freeze artifacts substantively valid and boundary clean",
                "answer": recheck["authority_acceptance_passed"],
                "taken": "emit_final_accepted_state",
            },
            {
                "step": "emit_final_accepted_state",
                "question": "close/freeze accepted as final",
                "answer": final_accepted_state["packet_status"],
                "taken": "emit_final_protocol_reference",
            },
            {
                "step": "emit_final_protocol_reference",
                "question": "emit hidden next command",
                "answer": False,
                "taken": "STOP_R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN_FINAL_ACCEPTED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN_FINAL_ACCEPTED",
            "next_command_goal": None,
        },
    }

    write_json(PATCH_PLAN_PATH, patch_plan)
    write_json(SOURCE_SURFACE_PATH, source_surface)
    write_json(AUTHORITY_ACCEPTANCE_RECHECK_PATH, recheck)
    write_json(PATCHED_ACCEPTANCE_PACKET_PATH, patched_acceptance_packet)
    write_json(FINAL_ACCEPTED_STATE_PACKET_PATH, final_accepted_state)
    write_json(BOUNDED_PROTOCOL_FINAL_REFERENCE_PATH, final_reference)
    write_json(PATCHED_DECISION_PATH, decision)
    write_json(NEXT_STATUS_PACKET_PATH, next_status)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(recheck, final_accepted_state, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "FINAL_ACCEPTANCE_0_FAILURE_REVIEW_CONSUMED": True,
        "FINAL_ACCEPTANCE_1_FIX_AUTHORITY_CONSUMED": True,
        "FINAL_ACCEPTANCE_2_AUTHORITY_ACCEPTANCE_RECHECK_PASS": recheck["authority_acceptance_passed"] is True,
        "FINAL_ACCEPTANCE_3_FINAL_STATE_ACCEPTED": final_accepted_state["packet_status"] == "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN_FINAL_ACCEPTED",
        "FINAL_ACCEPTANCE_4_BRANCH_CLOSED": final_accepted_state["branch_status"] == "CLOSED",
        "FINAL_ACCEPTANCE_5_PROTOCOL_FROZEN": final_accepted_state["protocol_freeze_status"] == "FROZEN_REUSABLE_REFERENCE",
        "FINAL_ACCEPTANCE_6_NO_RERUN_OR_PROBE": report["radius_10000_rerun_count"] == 0 and report["new_small_probe_count"] == 0,
        "FINAL_ACCEPTANCE_7_NO_UNBOUNDED_OR_RADIUS_ABOVE_10000": report["unbounded_or_no_cap_run_count"] == 0 and report["radius_above_10000_run_count"] == 0,
        "FINAL_ACCEPTANCE_8_NO_LARGER_RADIUS": report["larger_bounded_radius_run_count"] == 0,
        "FINAL_ACCEPTANCE_9_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0 and report["row_payload_inspected_count"] == 0,
        "FINAL_ACCEPTANCE_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "FINAL_ACCEPTANCE_11_NO_REPAIR_OR_TAXONOMY": report["repair_executed_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "FINAL_ACCEPTANCE_12_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None and next_status["auto_next_command"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_close_freeze_failure_review_receipt_id": SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID,
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
        "acceptance_patch_only_no_rerun": True,
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
        "source_close_freeze_failure_review_receipt_id": SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID,
        "final_state": final_accepted_state["packet_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "patch_plan": rel(PATCH_PLAN_PATH),
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "authority_acceptance_recheck": rel(AUTHORITY_ACCEPTANCE_RECHECK_PATH),
        "patched_acceptance_packet": rel(PATCHED_ACCEPTANCE_PACKET_PATH),
        "final_accepted_state_packet": rel(FINAL_ACCEPTED_STATE_PACKET_PATH),
        "bounded_protocol_final_reference": rel(BOUNDED_PROTOCOL_FINAL_REFERENCE_PATH),
        "patched_decision": rel(PATCHED_DECISION_PATH),
        "next_status_packet": rel(NEXT_STATUS_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_close_freeze_failure_review_receipt": rel(FAILURE_REVIEW_RECEIPT_PATH),
        "source_failed_close_freeze_receipt": rel(FAILED_CLOSE_FREEZE_RECEIPT_PATH),
        "source_failed_bounded_protocol_freeze": rel(BOUNDED_PROTOCOL_FREEZE_PATH),
        "source_failed_final_state_packet": rel(FAILED_FINAL_STATE_PACKET_PATH),
    }

    receipt = {
        "schema_version": "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_receipt_v0",
        "receipt_type": "R10000_CLOSE_AND_FREEZE_ACCEPTANCE_AFTER_AUTHORITY_STRING_MISMATCH_PATCH_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_close_freeze_failure_review_receipt_id": SOURCE_CLOSE_FREEZE_FAILURE_REVIEW_RECEIPT_ID,
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
        "final_close_and_freeze_summary": {
            "final_result": "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN_FINAL_ACCEPTED",
            "branch_status": final_accepted_state["branch_status"],
            "protocol_freeze_status": final_accepted_state["protocol_freeze_status"],
            "protocol_id": final_accepted_state["protocol_id"],
            "accepted_final_signal_class": final_accepted_state["accepted_final_signal_class"],
            "accepted_driver_class": final_accepted_state["accepted_driver_class"],
            "requires_repair": final_accepted_state["requires_repair"],
            "requires_further_localization": final_accepted_state["requires_further_localization"],
            "larger_radius_authorized_now": final_accepted_state["larger_radius_authorized_now"],
            "acceptance_patch_only_no_rerun": True,
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "final_close_and_freeze_guards": guards_packet,
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
    print(f"final_close_freeze_receipt_id={receipt_id}")
    print(f"final_close_freeze_receipt_path=data/r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0_receipts/{receipt_id}.json")
    print(f"final_accepted_state_packet_path=data/r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0/r10000_close_and_freeze_final_accepted_state_packet.json")
    print(f"bounded_protocol_final_reference_path=data/r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0/bounded_observability_protocol_final_reference_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
