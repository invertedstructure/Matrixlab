#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PATCH_R10000_SIGNAL_LOCALIZATION_PROTECTED_KEY_GUARD_TO_REFERENCE_ONLY_ACCEPTANCE_V0"
TARGET_UNIT_ID = "r10000.signal_localization.protected_key_guard.reference_only_acceptance.patch.v0"

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

OUT_DIR = ROOT / "data" / "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0"
RECEIPT_DIR = ROOT / "data" / "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0_receipts"

PATCH_PLAN_PATH = OUT_DIR / "r10000_signal_localization_guard_reference_only_acceptance_patch_plan.json"
SOURCE_SURFACE_PATH = OUT_DIR / "r10000_signal_localization_guard_reference_only_acceptance_source_surface.json"
GUARD_PATCH_SPEC_PATH = OUT_DIR / "r10000_signal_localization_guard_reference_only_acceptance_patch_spec.json"
REFERENCE_ONLY_ACCEPTANCE_RECHECK_PATH = OUT_DIR / "r10000_signal_localization_reference_only_acceptance_recheck.json"
PATCHED_LOCALIZATION_PACKET_PATH = OUT_DIR / "r10000_signal_localization_patched_acceptance_packet.json"
PATCHED_DECISION_PATH = OUT_DIR / "r10000_signal_localization_patched_acceptance_decision.json"
NEXT_DECISION_PACKET_PATH = OUT_DIR / "r10000_signal_localization_patched_acceptance_next_decision_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r10000_signal_localization_guard_reference_only_acceptance_patch_transition_trace.json"
REPORT_PATH = OUT_DIR / "r10000_signal_localization_guard_reference_only_acceptance_patch_report.json"

FAILURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r10000_distinguishable_signal_localization_failure_protected_key_hits_review_v0_receipts" / f"{SOURCE_FAILURE_REVIEW_RECEIPT_ID}.json"
FIX_AUTHORITY_PACKET_PATH = ROOT / "data" / "r10000_distinguishable_signal_localization_failure_protected_key_hits_review_v0" / "r10000_signal_localization_failure_fix_authority_packet.json"
FAILURE_NEXT_DECISION_PACKET_PATH = ROOT / "data" / "r10000_distinguishable_signal_localization_failure_protected_key_hits_review_v0" / "r10000_signal_localization_failure_review_next_decision_packet.json"
GUARD_CLASSIFICATION_PACKET_PATH = ROOT / "data" / "r10000_distinguishable_signal_localization_failure_protected_key_hits_review_v0" / "r10000_signal_localization_failure_guard_classification_packet.json"
PROTECTED_KEY_HIT_REVIEW_PATH = ROOT / "data" / "r10000_distinguishable_signal_localization_failure_protected_key_hits_review_v0" / "r10000_signal_localization_protected_key_hit_review.json"
LOCALIZATION_FINDING_REVIEW_PATH = ROOT / "data" / "r10000_distinguishable_signal_localization_failure_protected_key_hits_review_v0" / "r10000_signal_localization_finding_review.json"

FAILED_LOCALIZATION_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0_receipts" / f"{SOURCE_FAILED_LOCALIZATION_RECEIPT_ID}.json"
FAILED_LOCALIZATION_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_localization_packet.json"
FAILED_SIGNAL_DRIVER_PROFILE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_driver_profile.json"
FAILED_SHAPE_REDUCTION_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_shape_reduction_experiment.json"
FAILED_FIELD_CARDINALITY_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_field_cardinality_profile.json"
FAILED_LOCALIZATION_REPORT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_localization_report.json"

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
    FAILURE_NEXT_DECISION_PACKET_PATH,
    GUARD_CLASSIFICATION_PACKET_PATH,
    PROTECTED_KEY_HIT_REVIEW_PATH,
    LOCALIZATION_FINDING_REVIEW_PATH,
    FAILED_LOCALIZATION_RECEIPT_PATH,
    FAILED_LOCALIZATION_PACKET_PATH,
    FAILED_SIGNAL_DRIVER_PROFILE_PATH,
    FAILED_SHAPE_REDUCTION_PATH,
    FAILED_FIELD_CARDINALITY_PATH,
    FAILED_LOCALIZATION_REPORT_PATH,
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
    "decision": "PATCH_R10000_SIGNAL_LOCALIZATION_PROTECTED_KEY_GUARD_TO_REFERENCE_ONLY_ACCEPTANCE",
    "scope": "apply the reviewed narrow acceptance correction: protected key-name hits are not a failure when all materialization/inspection/mutation boundary counters are zero; preserve the volatile-only localization finding and emit a PASS patched acceptance packet without rerunning radius-10000 or inspecting row payloads",
    "source_failure_review_receipt_id": SOURCE_FAILURE_REVIEW_RECEIPT_ID,
    "authorized": [
        "consume failure review receipt and fix authority packet",
        "consume failed localization artifacts",
        "accept protected key-name hits only as reference-only when boundary counters are clean",
        "preserve localization classification R10000_LOCALIZATION_VOLATILE_RECEIPT_METADATA_ONLY",
        "emit patched acceptance packet and next decision packet",
        "stop before close/freeze/scaling decision",
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

BOUNDARY_ZERO_KEYS = [
    "row_payload_materialized_count",
    "row_payload_inspected_count",
    "closed_group_inspected_count",
    "queue_reopened_count",
    "identity_assignment_count",
    "field_value_invention_count",
    "source_mutation_count",
    "existing_receipt_mutation_count",
]

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
    failure_review = read_json(FAILURE_REVIEW_RECEIPT_PATH)
    authority = read_json(FIX_AUTHORITY_PACKET_PATH)
    guard = read_json(GUARD_CLASSIFICATION_PACKET_PATH)
    failed = read_json(FAILED_LOCALIZATION_RECEIPT_PATH)
    failed_packet = read_json(FAILED_LOCALIZATION_PACKET_PATH)
    driver = read_json(FAILED_SIGNAL_DRIVER_PROFILE_PATH)
    failed_report = read_json(FAILED_LOCALIZATION_REPORT_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if failure_review.get("receipt_id") != SOURCE_FAILURE_REVIEW_RECEIPT_ID:
        failures.append("failure_review_receipt_id_wrong")
    if failure_review.get("gate") != "PASS":
        failures.append("failure_review_gate_not_pass")
    if failure_review.get("r10000_signal_localization_failure_review_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("failure_review_not_recommending_this_patch")
    if authority.get("packet_status") != "PROTECTED_KEY_GUARD_FALSE_POSITIVE_REVIEWED_NARROW_PATCH_AUTHORIZED":
        failures.append("fix_authority_packet_not_patch_authorized")
    if authority.get("authorized_next_unit") != UNIT_ID:
        failures.append("fix_authority_authorized_next_wrong")
    if authority.get("radius_10000_rerun_authorized_now") is not False:
        failures.append("fix_authority_allows_rerun_unexpectedly")
    if authority.get("repair_authorized_in_this_review_unit") is not False:
        failures.append("fix_authority_says_review_repair_authorized")

    if guard.get("classification") != "OVERSTRICT_PROTECTED_KEY_GUARD_FALSE_POSITIVE_ACCEPT_FINDING_AFTER_REVIEW":
        failures.append("guard_classification_not_false_positive")
    if guard.get("true_payload_boundary_violation") is not False:
        failures.append("guard_packet_marks_true_boundary_violation")
    if guard.get("accept_substantive_localization_finding_after_review") is not True:
        failures.append("guard_packet_does_not_accept_finding")

    if failed.get("receipt_id") != SOURCE_FAILED_LOCALIZATION_RECEIPT_ID:
        failures.append("failed_localization_receipt_id_wrong")
    if failed.get("gate") != "FAIL":
        failures.append("failed_localization_not_fail")
    if "protected_payload_key_hit_detected" not in failed.get("failures", []):
        failures.append("failed_localization_missing_expected_guard_failure")

    if failed_packet.get("classification") != "R10000_LOCALIZATION_VOLATILE_RECEIPT_METADATA_ONLY":
        failures.append("failed_packet_not_volatile_only")
    if driver.get("driver_class") != "RECEIPT_VOLATILITY_ONLY_NO_STRUCTURAL_SIGNAL_LOCALIZED":
        failures.append("driver_not_volatile_only")
    if failed_report.get("protected_payload_key_hit_count") != 30000:
        failures.append("failed_report_protected_key_hit_count_not_30000")
    for key in BOUNDARY_ZERO_KEYS:
        if failed_report.get(key) != 0:
            failures.append(f"boundary_counter_not_zero:{key}:{failed_report.get(key)}")

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
    failure_review = read_json(FAILURE_REVIEW_RECEIPT_PATH)
    authority = read_json(FIX_AUTHORITY_PACKET_PATH)
    guard = read_json(GUARD_CLASSIFICATION_PACKET_PATH)
    failed = read_json(FAILED_LOCALIZATION_RECEIPT_PATH)
    failed_packet = read_json(FAILED_LOCALIZATION_PACKET_PATH)
    driver = read_json(FAILED_SIGNAL_DRIVER_PROFILE_PATH)
    return {
        "schema_version": "r10000_signal_localization_guard_reference_only_acceptance_source_surface_v0",
        "source_failure_review_receipt_id": SOURCE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_localization_receipt_id": SOURCE_FAILED_LOCALIZATION_RECEIPT_ID,
        "failure_review_summary": failure_review.get("r10000_signal_localization_failure_review_summary"),
        "fix_authority_packet": authority,
        "guard_classification_packet": guard,
        "failed_localization_gate": failed.get("gate"),
        "failed_localization_failures": failed.get("failures"),
        "failed_localization_summary": failed.get("r10000_distinguishable_signal_localization_summary"),
        "failed_localization_packet": failed_packet,
        "failed_driver_profile": {
            "driver_class": driver.get("driver_class"),
            "raw_shape_count": driver.get("raw_shape_count"),
            "volatile_scrub_shape_count": driver.get("volatile_scrub_shape_count"),
            "aggressive_scrub_shape_count": driver.get("aggressive_scrub_shape_count"),
            "structure_only_shape_count": driver.get("structure_only_shape_count"),
            "volatile_driver_count_top_50": driver.get("volatile_driver_count_top_50"),
            "nonvolatile_driver_count_top_50": driver.get("nonvolatile_driver_count_top_50"),
        },
    }

def reference_only_acceptance_recheck() -> Dict[str, Any]:
    failure_review = read_json(FAILURE_REVIEW_RECEIPT_PATH)
    hit_review = read_json(PROTECTED_KEY_HIT_REVIEW_PATH)
    finding = read_json(LOCALIZATION_FINDING_REVIEW_PATH)
    failed_report = read_json(FAILED_LOCALIZATION_REPORT_PATH)
    failed_packet = read_json(FAILED_LOCALIZATION_PACKET_PATH)
    driver = read_json(FAILED_SIGNAL_DRIVER_PROFILE_PATH)
    shape = read_json(FAILED_SHAPE_REDUCTION_PATH)

    boundary_counts = {key: failed_report.get(key) for key in BOUNDARY_ZERO_KEYS}
    boundary_clean = all(value == 0 for value in boundary_counts.values())

    accepted = (
        failure_review.get("gate") == "PASS"
        and hit_review.get("classification") == "PROTECTED_KEY_NAME_REFERENCE_ONLY_NO_PAYLOAD_BOUNDARY_CROSSING"
        and finding.get("finding_supported_despite_gate_fail") is True
        and failed_report.get("protected_payload_key_hit_count") == 30000
        and boundary_clean
        and failed_packet.get("classification") == "R10000_LOCALIZATION_VOLATILE_RECEIPT_METADATA_ONLY"
        and driver.get("driver_class") == "RECEIPT_VOLATILITY_ONLY_NO_STRUCTURAL_SIGNAL_LOCALIZED"
        and shape.get("raw_shape_count") == EXPECTED_RADIUS
        and shape.get("aggressive_scrub_shape_count") == 1
        and shape.get("structure_only_shape_count") == 1
    )

    return {
        "schema_version": "r10000_signal_localization_reference_only_acceptance_recheck_v0",
        "source_failure_review_receipt_id": SOURCE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_localization_receipt_id": SOURCE_FAILED_LOCALIZATION_RECEIPT_ID,
        "protected_payload_key_hit_count": failed_report.get("protected_payload_key_hit_count"),
        "protected_key_hit_classification": hit_review.get("classification"),
        "boundary_counts": boundary_counts,
        "boundary_clean": boundary_clean,
        "substantive_finding_supported": finding.get("finding_supported_despite_gate_fail"),
        "accepted_localization_classification": failed_packet.get("classification"),
        "accepted_driver_class": driver.get("driver_class"),
        "shape_reduction_evidence": {
            "raw_shape_count": shape.get("raw_shape_count"),
            "volatile_scrub_shape_count": shape.get("volatile_scrub_shape_count"),
            "aggressive_scrub_shape_count": shape.get("aggressive_scrub_shape_count"),
            "structure_only_shape_count": shape.get("structure_only_shape_count"),
            "reduction_class": shape.get("reduction_class"),
        },
        "reference_only_acceptance_passed": accepted,
    }

def validate_outputs(recheck: Dict[str, Any], patched_packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if recheck.get("reference_only_acceptance_passed") is not True:
        failures.append("reference_only_acceptance_recheck_not_passed")
    if recheck.get("boundary_clean") is not True:
        failures.append("boundary_not_clean")
    if patched_packet.get("classification") != "R10000_LOCALIZATION_VOLATILE_RECEIPT_METADATA_ONLY_ACCEPTED_AFTER_REFERENCE_ONLY_GUARD_PATCH":
        failures.append(f"patched_classification_wrong:{patched_packet.get('classification')}")
    if patched_packet.get("requires_repair") is not False:
        failures.append("patched_packet_requires_repair_unexpectedly")
    if patched_packet.get("requires_further_localization") is not False:
        failures.append("patched_packet_requires_localization_unexpectedly")

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
    for key in [
        "failure_review_receipt_consumed_count",
        "fix_authority_packet_consumed_count",
        "failed_localization_receipt_consumed_count",
        "failed_localization_artifacts_consumed_count",
        "source_surface_emitted_count",
        "guard_patch_spec_emitted_count",
        "reference_only_acceptance_recheck_emitted_count",
        "patched_localization_packet_emitted_count",
        "patched_decision_emitted_count",
        "next_decision_packet_emitted_count",
        "reference_only_acceptance_passed_count",
        "patched_acceptance_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    if metrics.get("protected_payload_key_hit_count") != 30000:
        failures.append(f"metric_protected_payload_key_hit_count_not_30000:{metrics.get('protected_payload_key_hit_count')}")

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
    if terminal.get("stop_code") != "STOP_R10000_SIGNAL_LOCALIZATION_PROTECTED_KEY_GUARD_PATCH_ACCEPTED_REFERENCE_ONLY":
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
    recheck = reference_only_acceptance_recheck()
    failed_packet = read_json(FAILED_LOCALIZATION_PACKET_PATH)
    driver = read_json(FAILED_SIGNAL_DRIVER_PROFILE_PATH)
    authority = read_json(FIX_AUTHORITY_PACKET_PATH)

    patch_plan = {
        "schema_version": "r10000_signal_localization_guard_reference_only_acceptance_patch_plan_v0",
        "unit_id": UNIT_ID,
        "source_failure_review_receipt_id": SOURCE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_localization_receipt_id": SOURCE_FAILED_LOCALIZATION_RECEIPT_ID,
        "mode": "review_acceptance_patch_only_no_rerun",
        "correction": "protected key-name references are accepted when all materialization/inspection/mutation boundary counters are zero",
        "not_authorized": HUMAN_DECISION["not_authorized"],
    }

    patch_spec = {
        "schema_version": "r10000_signal_localization_guard_reference_only_acceptance_patch_spec_v0",
        "patch_scope": "acceptance semantics only",
        "old_guard": "protected_payload_key_hit_count must be zero",
        "new_guard": "protected_payload_key_hit_count may be nonzero if classified as key-name/reference-only and all boundary counters are zero",
        "required_zero_boundary_counters": BOUNDARY_ZERO_KEYS,
        "required_prior_review_classification": "OVERSTRICT_PROTECTED_KEY_GUARD_FALSE_POSITIVE_ACCEPT_FINDING_AFTER_REVIEW",
        "radius_10000_rerun_required": False,
        "row_payload_materialization_allowed": False,
    }

    patched_packet = {
        "schema_version": "r10000_signal_localization_patched_acceptance_packet_v0",
        "classification": "R10000_LOCALIZATION_VOLATILE_RECEIPT_METADATA_ONLY_ACCEPTED_AFTER_REFERENCE_ONLY_GUARD_PATCH",
        "source_failure_review_receipt_id": SOURCE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_localization_receipt_id": SOURCE_FAILED_LOCALIZATION_RECEIPT_ID,
        "run_id": RUN_ID,
        "accepted_localization_classification": failed_packet.get("classification"),
        "accepted_driver_class": driver.get("driver_class"),
        "reference_only_acceptance_recheck": recheck,
        "patch_authority_packet": {
            "path": rel(FIX_AUTHORITY_PACKET_PATH),
            "packet_status": authority.get("packet_status"),
        },
        "requires_repair": False,
        "requires_further_localization": False,
        "requires_human_strategy_selection": True,
        "recommended_next_handling": "DECIDE_CLOSE_OR_FREEZE_BOUNDED_OBSERVABILITY_PROTOCOL_AFTER_R10000_VOLATILE_ONLY_SIGNAL_V0",
    }

    decision = {
        "schema_version": "r10000_signal_localization_patched_acceptance_decision_v0",
        "decision_id": sha8({
            "unit_id": UNIT_ID,
            "source_failure_review_receipt_id": SOURCE_FAILURE_REVIEW_RECEIPT_ID,
            "classification": patched_packet["classification"],
        }),
        "decision_status": "R10000_SIGNAL_LOCALIZATION_GUARD_PATCH_ACCEPTED_REFERENCE_ONLY",
        "patched_classification": patched_packet["classification"],
        "accepted_localization_classification": patched_packet["accepted_localization_classification"],
        "accepted_driver_class": patched_packet["accepted_driver_class"],
        "protected_payload_key_hit_count": recheck["protected_payload_key_hit_count"],
        "boundary_clean": recheck["boundary_clean"],
        "reference_only_acceptance_passed": recheck["reference_only_acceptance_passed"],
        "review_patch_only_no_rerun": True,
        "recommended_next_handling": patched_packet["recommended_next_handling"],
    }

    next_decision = {
        "schema_version": "r10000_signal_localization_patched_acceptance_next_decision_packet_v0",
        "packet_status": "R10000_SIGNAL_LOCALIZATION_REFERENCE_ONLY_GUARD_PATCH_ACCEPTED_READY_FOR_CLOSE_OR_FREEZE_DECISION",
        "source_failure_review_receipt_id": SOURCE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_localization_receipt_id": SOURCE_FAILED_LOCALIZATION_RECEIPT_ID,
        "run_id": RUN_ID,
        "accepted_driver_class": patched_packet["accepted_driver_class"],
        "accepted_localization_classification": patched_packet["accepted_localization_classification"],
        "safe_next_choices": [
            "close the R10000 observability branch as accepted volatile-only signal",
            "freeze the bounded observability protocol as reusable infrastructure",
            "choose a larger bounded radius only as a separate explicit objective",
            "do not rerun R10000 for this guard correction",
        ],
        "recommended_next_handling": patched_packet["recommended_next_handling"],
        "auto_next_command": None,
    }

    report = {
        "schema_version": "r10000_signal_localization_guard_reference_only_acceptance_patch_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failure_review_receipt_id": SOURCE_FAILURE_REVIEW_RECEIPT_ID,
        "source_failed_localization_receipt_id": SOURCE_FAILED_LOCALIZATION_RECEIPT_ID,
        "failure_review_receipt_consumed_count": 1,
        "fix_authority_packet_consumed_count": 1,
        "failed_localization_receipt_consumed_count": 1,
        "failed_localization_artifacts_consumed_count": 1,
        "source_surface_emitted_count": 1,
        "guard_patch_spec_emitted_count": 1,
        "reference_only_acceptance_recheck_emitted_count": 1,
        "patched_localization_packet_emitted_count": 1,
        "patched_decision_emitted_count": 1,
        "next_decision_packet_emitted_count": 1,
        "protected_payload_key_hit_count": recheck["protected_payload_key_hit_count"],
        "reference_only_acceptance_passed_count": 1 if recheck["reference_only_acceptance_passed"] else 0,
        "patched_acceptance_count": 1 if patched_packet["classification"] == "R10000_LOCALIZATION_VOLATILE_RECEIPT_METADATA_ONLY_ACCEPTED_AFTER_REFERENCE_ONLY_GUARD_PATCH" else 0,
        "accepted_driver_class": patched_packet["accepted_driver_class"],
        "accepted_localization_classification": patched_packet["accepted_localization_classification"],
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
        "recommended_next_handling": patched_packet["recommended_next_handling"],
    }

    trace = {
        "schema_version": "r10000_signal_localization_guard_reference_only_acceptance_patch_transition_trace_v0",
        "trace": [
            {
                "step": "consume_failure_review_and_fix_authority",
                "question": "was guard false positive reviewed and patch authorized",
                "answer": True,
                "taken": "reference_only_acceptance_recheck",
            },
            {
                "step": "reference_only_acceptance_recheck",
                "question": "protected key hits are reference-only with clean boundary counters",
                "answer": recheck["reference_only_acceptance_passed"],
                "taken": "emit_patched_acceptance_packet",
            },
            {
                "step": "emit_patched_acceptance_packet",
                "question": "preserve volatile-only localization finding",
                "answer": patched_packet["accepted_driver_class"],
                "taken": "emit_next_decision_packet",
            },
            {
                "step": "emit_next_decision_packet",
                "question": "close/freeze/scale now",
                "answer": False,
                "taken": "STOP_R10000_SIGNAL_LOCALIZATION_PROTECTED_KEY_GUARD_PATCH_ACCEPTED_REFERENCE_ONLY",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_R10000_SIGNAL_LOCALIZATION_PROTECTED_KEY_GUARD_PATCH_ACCEPTED_REFERENCE_ONLY",
            "next_command_goal": None,
        },
    }

    write_json(PATCH_PLAN_PATH, patch_plan)
    write_json(SOURCE_SURFACE_PATH, source_surface)
    write_json(GUARD_PATCH_SPEC_PATH, patch_spec)
    write_json(REFERENCE_ONLY_ACCEPTANCE_RECHECK_PATH, recheck)
    write_json(PATCHED_LOCALIZATION_PACKET_PATH, patched_packet)
    write_json(PATCHED_DECISION_PATH, decision)
    write_json(NEXT_DECISION_PACKET_PATH, next_decision)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(recheck, patched_packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "R10000_GUARD_PATCH_0_FAILURE_REVIEW_CONSUMED": True,
        "R10000_GUARD_PATCH_1_FIX_AUTHORITY_CONSUMED": True,
        "R10000_GUARD_PATCH_2_REFERENCE_ONLY_RECHECK_PASS": recheck["reference_only_acceptance_passed"] is True,
        "R10000_GUARD_PATCH_3_PATCHED_ACCEPTANCE_EMITTED": report["patched_acceptance_count"] == 1,
        "R10000_GUARD_PATCH_4_VOLATILE_ONLY_FINDING_PRESERVED": report["accepted_localization_classification"] == "R10000_LOCALIZATION_VOLATILE_RECEIPT_METADATA_ONLY" and report["accepted_driver_class"] == "RECEIPT_VOLATILITY_ONLY_NO_STRUCTURAL_SIGNAL_LOCALIZED",
        "R10000_GUARD_PATCH_5_NEXT_DECISION_PACKET_EMITTED": report["next_decision_packet_emitted_count"] == 1,
        "R10000_GUARD_PATCH_6_NO_RERUN_OR_PROBE": report["radius_10000_rerun_count"] == 0 and report["new_small_probe_count"] == 0,
        "R10000_GUARD_PATCH_7_NO_UNBOUNDED_OR_RADIUS_ABOVE_10000": report["unbounded_or_no_cap_run_count"] == 0 and report["radius_above_10000_run_count"] == 0,
        "R10000_GUARD_PATCH_8_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0 and report["row_payload_inspected_count"] == 0,
        "R10000_GUARD_PATCH_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "R10000_GUARD_PATCH_10_NO_TAXONOMY_DELTA": report["taxonomy_delta_proposal_emitted_count"] == 0,
        "R10000_GUARD_PATCH_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
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
        "patch_only_no_rerun": True,
        "existing_artifacts_only": True,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "radius_10000_rerun": False,
        "new_small_probe": False,
        "unbounded_or_no_cap_run": False,
        "radius_above_10000_run": False,
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
        "source_failure_review_receipt_id": SOURCE_FAILURE_REVIEW_RECEIPT_ID,
        "patched_classification": patched_packet["classification"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "patch_plan": rel(PATCH_PLAN_PATH),
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "guard_patch_spec": rel(GUARD_PATCH_SPEC_PATH),
        "reference_only_acceptance_recheck": rel(REFERENCE_ONLY_ACCEPTANCE_RECHECK_PATH),
        "patched_localization_packet": rel(PATCHED_LOCALIZATION_PACKET_PATH),
        "patched_decision": rel(PATCHED_DECISION_PATH),
        "next_decision_packet": rel(NEXT_DECISION_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_failure_review_receipt": rel(FAILURE_REVIEW_RECEIPT_PATH),
        "source_failed_localization_receipt": rel(FAILED_LOCALIZATION_RECEIPT_PATH),
    }

    receipt = {
        "schema_version": "r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_receipt_v0",
        "receipt_type": "R10000_SIGNAL_LOCALIZATION_PROTECTED_KEY_GUARD_REFERENCE_ONLY_ACCEPTANCE_PATCH_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
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
        "r10000_guard_patch_summary": {
            "patch_result": decision["decision_status"],
            "patched_classification": patched_packet["classification"],
            "accepted_localization_classification": patched_packet["accepted_localization_classification"],
            "accepted_driver_class": patched_packet["accepted_driver_class"],
            "protected_payload_key_hit_count": recheck["protected_payload_key_hit_count"],
            "boundary_clean": recheck["boundary_clean"],
            "reference_only_acceptance_passed": recheck["reference_only_acceptance_passed"],
            "requires_repair": patched_packet["requires_repair"],
            "requires_further_localization": patched_packet["requires_further_localization"],
            "patch_only_no_rerun": True,
            "recommended_next_handling": patched_packet["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "r10000_guard_patch_guards": guards_packet,
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
    print(f"r10000_guard_patch_receipt_id={receipt_id}")
    print(f"r10000_guard_patch_receipt_path=data/r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0_receipts/{receipt_id}.json")
    print(f"patched_localization_packet_path=data/r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0/r10000_signal_localization_patched_acceptance_packet.json")
    print(f"next_decision_packet_path=data/r10000_signal_localization_protected_key_guard_reference_only_acceptance_patch_v0/r10000_signal_localization_patched_acceptance_next_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
