#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_R10000_DISTINGUISHABLE_SIGNAL_LOCALIZATION_FAILURE_PROTECTED_KEY_HITS_V0"
TARGET_UNIT_ID = "r10000.distinguishable_signal_localization.failure_protected_key_hits.review.v0"

SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID = "bb9e4719"
SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID = "293faf9e"
SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID = "90042e28"
SOURCE_RADIUS_10000_RETRY_RECEIPT_ID = "bb2c8ce3"
SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID = "02711ff1"
SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID = "52d0ea8d"
SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"
RUN_ID = "run_6b1b2494"
EXPECTED_RADIUS = 10000

OUT_DIR = ROOT / "data" / "r10000_distinguishable_signal_localization_failure_protected_key_hits_review_v0"
RECEIPT_DIR = ROOT / "data" / "r10000_distinguishable_signal_localization_failure_protected_key_hits_review_v0_receipts"

FAILURE_REVIEW_SURFACE_PATH = OUT_DIR / "r10000_signal_localization_failure_review_surface.json"
PROTECTED_KEY_HIT_REVIEW_PATH = OUT_DIR / "r10000_signal_localization_protected_key_hit_review.json"
LOCALIZATION_FINDING_REVIEW_PATH = OUT_DIR / "r10000_signal_localization_finding_review.json"
GUARD_CLASSIFICATION_PACKET_PATH = OUT_DIR / "r10000_signal_localization_failure_guard_classification_packet.json"
FIX_AUTHORITY_PACKET_PATH = OUT_DIR / "r10000_signal_localization_failure_fix_authority_packet.json"
REVIEW_DECISION_PATH = OUT_DIR / "r10000_signal_localization_failure_review_decision.json"
NEXT_DECISION_PACKET_PATH = OUT_DIR / "r10000_signal_localization_failure_review_next_decision_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r10000_signal_localization_failure_review_transition_trace.json"
REPORT_PATH = OUT_DIR / "r10000_signal_localization_failure_review_report.json"

FAILED_RECEIPT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0_receipts" / f"{SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID}.json"
LOCALIZATION_PLAN_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_localization_plan.json"
SOURCE_SURFACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_source_surface.json"
FIELD_CARDINALITY_PROFILE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_field_cardinality_profile.json"
VOLATILITY_CLASSIFICATION_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_volatility_classification.json"
SHAPE_REDUCTION_EXPERIMENT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_shape_reduction_experiment.json"
SIGNAL_DRIVER_PROFILE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_driver_profile.json"
LOCALIZATION_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_localization_packet.json"
LOCALIZATION_NEXT_DECISION_PACKET_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_localization_next_decision_packet.json"
LOCALIZATION_DECISION_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_localization_decision.json"
LOCALIZATION_TRACE_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_localization_transition_trace.json"
LOCALIZATION_REPORT_PATH = ROOT / "data" / "r1000_post_closure_observability_harvest_radius_10000_distinguishable_signal_localization_v0" / "r10000_distinguishable_signal_localization_report.json"

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
    FAILED_RECEIPT_PATH,
    LOCALIZATION_PLAN_PATH,
    SOURCE_SURFACE_PATH,
    FIELD_CARDINALITY_PROFILE_PATH,
    VOLATILITY_CLASSIFICATION_PATH,
    SHAPE_REDUCTION_EXPERIMENT_PATH,
    SIGNAL_DRIVER_PROFILE_PATH,
    LOCALIZATION_PACKET_PATH,
    LOCALIZATION_NEXT_DECISION_PACKET_PATH,
    LOCALIZATION_DECISION_PATH,
    LOCALIZATION_TRACE_PATH,
    LOCALIZATION_REPORT_PATH,
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
    "decision": "REVIEW_R10000_DISTINGUISHABLE_SIGNAL_LOCALIZATION_FAILURE_PROTECTED_KEY_HITS",
    "scope": "review the failed R10000 distinguishable-signal localization attempt; decide whether the failure is a true boundary violation or an over-strict protected-key-name detector; preserve the useful localization finding if supported; emit narrow fix authority without rerunning or repairing",
    "source_failed_r10000_signal_localization_receipt_id": SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID,
    "authorized": [
        "consume failed localization receipt",
        "consume failed localization artifacts",
        "review protected-key hit evidence",
        "review whether row payloads or closed groups were actually materialized/inspected",
        "review localization finding validity",
        "emit guard classification packet",
        "emit fix authority packet for a separate repair/review-acceptance unit",
        "stop before repair, rerun, scaling, or row payload work",
    ],
    "not_authorized": [
        "rerunning radius-10000",
        "running radius above 10000",
        "running unbounded/no-cap harvest",
        "running any small probe",
        "modifying src/matrixlab/cli.py",
        "modifying src/matrixlab/r1000_post_closure_observability_harvest.py",
        "modifying the failed localization runner",
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
    failed = read_json(FAILED_RECEIPT_PATH)
    report = read_json(LOCALIZATION_REPORT_PATH)
    packet = read_json(LOCALIZATION_PACKET_PATH)
    driver = read_json(SIGNAL_DRIVER_PROFILE_PATH)
    shape = read_json(SHAPE_REDUCTION_EXPERIMENT_PATH)
    cardinality = read_json(FIELD_CARDINALITY_PROFILE_PATH)
    signal = read_json(SIGNAL_INSPECTION_RECEIPT_PATH)
    closure = read_json(CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(CLOSED_QUEUE_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if failed.get("receipt_id") != SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID:
        failures.append("failed_localization_receipt_id_wrong")
    if failed.get("gate") != "FAIL":
        failures.append("failed_localization_gate_not_fail")
    if "protected_payload_key_hit_detected" not in failed.get("failures", []):
        failures.append("expected_protected_key_failure_missing")
    if failed.get("terminal", {}).get("stop_code") != "STOP_GATE_FAIL":
        failures.append("failed_localization_terminal_not_gate_fail")

    if report.get("protected_payload_key_hit_count") != 30000:
        failures.append(f"protected_key_hit_count_unexpected:{report.get('protected_payload_key_hit_count')}")
    if report.get("row_payload_materialized_count") != 0 or report.get("row_payload_inspected_count") != 0:
        failures.append("row_payload_boundary_was_crossed")
    if report.get("closed_group_inspected_count") != 0 or report.get("queue_reopened_count") != 0:
        failures.append("queue_or_closed_group_boundary_was_crossed")
    if report.get("field_value_invention_count") != 0 or report.get("identity_assignment_count") != 0:
        failures.append("identity_or_value_boundary_was_crossed")
    if report.get("source_mutation_count") != 0 or report.get("existing_receipt_mutation_count") != 0:
        failures.append("source_or_receipt_mutation_boundary_was_crossed")

    if packet.get("classification") != "R10000_LOCALIZATION_VOLATILE_RECEIPT_METADATA_ONLY":
        failures.append("localization_packet_classification_not_volatile_only")
    if driver.get("driver_class") != "RECEIPT_VOLATILITY_ONLY_NO_STRUCTURAL_SIGNAL_LOCALIZED":
        failures.append("driver_class_not_volatile_only")
    if shape.get("raw_shape_count") != EXPECTED_RADIUS:
        failures.append("raw_shape_count_not_10000")
    if shape.get("aggressive_scrub_shape_count") != 1:
        failures.append("aggressive_scrub_shape_not_collapsed")
    if shape.get("structure_only_shape_count") != 1:
        failures.append("structure_only_shape_not_collapsed")
    if cardinality.get("protected_payload_key_hit_count") != 30000:
        failures.append("cardinality_protected_hit_count_unexpected")

    if signal.get("gate") != "PASS":
        failures.append("source_signal_inspection_not_pass")
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

def protected_key_hit_review() -> Dict[str, Any]:
    cardinality = read_json(FIELD_CARDINALITY_PROFILE_PATH)
    report = read_json(LOCALIZATION_REPORT_PATH)
    failed = read_json(FAILED_RECEIPT_PATH)
    samples = cardinality.get("protected_payload_key_hit_samples", [])[:50]
    key_counts = {}
    for item in samples:
        key = item.get("key", "UNKNOWN")
        key_counts[key] = key_counts.get(key, 0) + 1

    boundary_counts = {
        "row_payload_materialized_count": report.get("row_payload_materialized_count"),
        "row_payload_inspected_count": report.get("row_payload_inspected_count"),
        "closed_group_inspected_count": report.get("closed_group_inspected_count"),
        "queue_reopened_count": report.get("queue_reopened_count"),
        "identity_assignment_count": report.get("identity_assignment_count"),
        "field_value_invention_count": report.get("field_value_invention_count"),
        "source_mutation_count": report.get("source_mutation_count"),
        "existing_receipt_mutation_count": report.get("existing_receipt_mutation_count"),
    }

    boundary_clean = all(v == 0 for v in boundary_counts.values())
    hit_count = report.get("protected_payload_key_hit_count")

    if hit_count and boundary_clean:
        classification = "PROTECTED_KEY_NAME_REFERENCE_ONLY_NO_PAYLOAD_BOUNDARY_CROSSING"
    elif hit_count and not boundary_clean:
        classification = "PROTECTED_PAYLOAD_BOUNDARY_CROSSING_REVIEW_REQUIRED"
    else:
        classification = "NO_PROTECTED_KEY_HITS_PRESENT"

    return {
        "schema_version": "r10000_signal_localization_protected_key_hit_review_v0",
        "source_failed_r10000_signal_localization_receipt_id": SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID,
        "protected_payload_key_hit_count": hit_count,
        "protected_payload_key_hit_samples": samples,
        "protected_payload_key_sample_key_counts": key_counts,
        "failed_acceptance_gate": "R10000_SIGNAL_LOCALIZATION_7_NO_PROTECTED_PAYLOAD_KEYS",
        "failed_receipt_failures": failed.get("failures"),
        "boundary_counts": boundary_counts,
        "boundary_clean": boundary_clean,
        "classification": classification,
        "interpretation": "The failed unit saw protected key names in existing receipts/profiles, but its own boundary counters show no row payload materialization, row payload inspection, closed group inspection, queue reopening, identity assignment, value invention, source mutation, or receipt mutation.",
    }

def localization_finding_review() -> Dict[str, Any]:
    packet = read_json(LOCALIZATION_PACKET_PATH)
    driver = read_json(SIGNAL_DRIVER_PROFILE_PATH)
    shape = read_json(SHAPE_REDUCTION_EXPERIMENT_PATH)
    volatility = read_json(VOLATILITY_CLASSIFICATION_PATH)

    finding_supported = (
        packet.get("classification") == "R10000_LOCALIZATION_VOLATILE_RECEIPT_METADATA_ONLY"
        and driver.get("driver_class") == "RECEIPT_VOLATILITY_ONLY_NO_STRUCTURAL_SIGNAL_LOCALIZED"
        and shape.get("raw_shape_count") == EXPECTED_RADIUS
        and shape.get("aggressive_scrub_shape_count") == 1
        and shape.get("structure_only_shape_count") == 1
        and driver.get("nonvolatile_driver_count_top_50") == 0
    )

    return {
        "schema_version": "r10000_signal_localization_finding_review_v0",
        "source_failed_r10000_signal_localization_receipt_id": SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID,
        "localization_packet_classification": packet.get("classification"),
        "driver_class": driver.get("driver_class"),
        "shape_reduction": {
            "raw_shape_count": shape.get("raw_shape_count"),
            "volatile_scrub_shape_count": shape.get("volatile_scrub_shape_count"),
            "aggressive_scrub_shape_count": shape.get("aggressive_scrub_shape_count"),
            "structure_only_shape_count": shape.get("structure_only_shape_count"),
            "reduction_class": shape.get("reduction_class"),
        },
        "driver_counts": {
            "volatile_driver_count_top_50": driver.get("volatile_driver_count_top_50"),
            "nonvolatile_driver_count_top_50": driver.get("nonvolatile_driver_count_top_50"),
            "volatile_driver_count_top_100": volatility.get("volatile_driver_count_top_100"),
            "nonvolatile_structural_driver_count_top_100": volatility.get("nonvolatile_structural_driver_count_top_100"),
        },
        "finding_supported_despite_gate_fail": finding_supported,
        "finding_interpretation": "The substantive localization result is usable: distinguishability is explained by receipt/reference volatility, not by a nonvolatile structural or semantic signal.",
    }

def build_guard_classification(hit_review: Dict[str, Any], finding_review: Dict[str, Any]) -> Dict[str, Any]:
    if hit_review["classification"] == "PROTECTED_KEY_NAME_REFERENCE_ONLY_NO_PAYLOAD_BOUNDARY_CROSSING" and finding_review["finding_supported_despite_gate_fail"]:
        classification = "OVERSTRICT_PROTECTED_KEY_GUARD_FALSE_POSITIVE_ACCEPT_FINDING_AFTER_REVIEW"
        recommended = "PATCH_R10000_SIGNAL_LOCALIZATION_PROTECTED_KEY_GUARD_TO_REFERENCE_ONLY_ACCEPTANCE_V0"
        accept_substantive_finding = True
        true_boundary_violation = False
    elif hit_review["classification"] == "PROTECTED_PAYLOAD_BOUNDARY_CROSSING_REVIEW_REQUIRED":
        classification = "TRUE_PROTECTED_PAYLOAD_BOUNDARY_REVIEW_REQUIRED"
        recommended = "REVIEW_R10000_SIGNAL_LOCALIZATION_TRUE_PAYLOAD_BOUNDARY_VIOLATION_V0"
        accept_substantive_finding = False
        true_boundary_violation = True
    else:
        classification = "R10000_SIGNAL_LOCALIZATION_FAILURE_REVIEW_INCONCLUSIVE"
        recommended = "REVIEW_R10000_SIGNAL_LOCALIZATION_FAILURE_MANUALLY_V0"
        accept_substantive_finding = False
        true_boundary_violation = False

    return {
        "schema_version": "r10000_signal_localization_failure_guard_classification_packet_v0",
        "classification": classification,
        "source_failed_r10000_signal_localization_receipt_id": SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID,
        "protected_key_hit_classification": hit_review["classification"],
        "finding_supported_despite_gate_fail": finding_review["finding_supported_despite_gate_fail"],
        "accept_substantive_localization_finding_after_review": accept_substantive_finding,
        "true_payload_boundary_violation": true_boundary_violation,
        "recommended_next_handling": recommended,
    }

def build_fix_authority(guard_packet: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r10000_signal_localization_failure_fix_authority_packet_v0",
        "packet_status": "PROTECTED_KEY_GUARD_FALSE_POSITIVE_REVIEWED_NARROW_PATCH_AUTHORIZED" if guard_packet["classification"] == "OVERSTRICT_PROTECTED_KEY_GUARD_FALSE_POSITIVE_ACCEPT_FINDING_AFTER_REVIEW" else "MANUAL_REVIEW_REQUIRED",
        "source_failed_r10000_signal_localization_receipt_id": SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID,
        "guard_classification": guard_packet["classification"],
        "authorized_next_unit": guard_packet["recommended_next_handling"],
        "required_fix_shape": [
            "do not rerun radius-10000",
            "do not inspect or materialize row payloads",
            "preserve existing failed localization artifacts",
            "patch only the acceptance distinction between protected key-name references and actual protected payload boundary crossing",
            "accept protected key-name hits only when row_payload_materialized_count, row_payload_inspected_count, closed_group_inspected_count, queue_reopened_count, identity_assignment_count, field_value_invention_count, source_mutation_count, and existing_receipt_mutation_count are all zero",
            "carry forward substantive classification R10000_LOCALIZATION_VOLATILE_RECEIPT_METADATA_ONLY if unchanged",
            "emit PASS review/patch receipt and next decision packet",
        ],
        "radius_10000_rerun_authorized_now": False,
        "repair_authorized_in_this_review_unit": False,
        "recommended_next_handling": guard_packet["recommended_next_handling"],
    }

def validate_outputs(hit_review: Dict[str, Any], finding_review: Dict[str, Any], guard_packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if hit_review.get("protected_payload_key_hit_count") != 30000:
        failures.append("protected_key_hit_count_not_30000")
    if hit_review.get("boundary_clean") is not True:
        failures.append("boundary_not_clean")
    if finding_review.get("finding_supported_despite_gate_fail") is not True:
        failures.append("substantive_finding_not_supported")
    if guard_packet.get("classification") != "OVERSTRICT_PROTECTED_KEY_GUARD_FALSE_POSITIVE_ACCEPT_FINDING_AFTER_REVIEW":
        failures.append(f"guard_classification_not_false_positive:{guard_packet.get('classification')}")
    if guard_packet.get("true_payload_boundary_violation") is not False:
        failures.append("true_payload_boundary_violation_marked")

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
        "failed_localization_receipt_consumed_count",
        "failed_localization_artifacts_consumed_count",
        "failure_review_surface_emitted_count",
        "protected_key_hit_review_emitted_count",
        "localization_finding_review_emitted_count",
        "guard_classification_packet_emitted_count",
        "fix_authority_packet_emitted_count",
        "review_decision_emitted_count",
        "next_decision_packet_emitted_count",
        "false_positive_guard_classification_count",
        "substantive_finding_supported_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    if metrics.get("protected_payload_key_hit_count") != 30000:
        failures.append(f"metric_protected_key_hit_count_not_30000:{metrics.get('protected_payload_key_hit_count')}")

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
    if terminal.get("stop_code") != "STOP_R10000_SIGNAL_LOCALIZATION_FAILURE_REVIEW_COMPLETE_GUARD_FALSE_POSITIVE_PATCH_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    hit_review = protected_key_hit_review()
    finding_review = localization_finding_review()
    guard_packet = build_guard_classification(hit_review, finding_review)
    authority = build_fix_authority(guard_packet)

    review_surface = {
        "schema_version": "r10000_signal_localization_failure_review_surface_v0",
        "review_surface_id": sha8({
            "source_failed_r10000_signal_localization_receipt_id": SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID,
            "guard_classification": guard_packet["classification"],
        }),
        "source_failed_r10000_signal_localization_receipt_id": SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID,
        "failed_receipt_gate": read_json(FAILED_RECEIPT_PATH).get("gate"),
        "failed_receipt_failures": read_json(FAILED_RECEIPT_PATH).get("failures"),
        "protected_key_hit_review": hit_review["classification"],
        "localization_finding_supported": finding_review["finding_supported_despite_gate_fail"],
        "guard_classification": guard_packet["classification"],
        "recommended_next_handling": guard_packet["recommended_next_handling"],
    }

    decision = {
        "schema_version": "r10000_signal_localization_failure_review_decision_v0",
        "decision_id": sha8({
            "unit_id": UNIT_ID,
            "source_failed": SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID,
            "classification": guard_packet["classification"],
        }),
        "decision_status": "R10000_SIGNAL_LOCALIZATION_FAILURE_REVIEW_ACCEPTS_GUARD_FALSE_POSITIVE",
        "guard_classification": guard_packet["classification"],
        "protected_key_hit_classification": hit_review["classification"],
        "substantive_localization_finding_supported": finding_review["finding_supported_despite_gate_fail"],
        "accepted_substantive_localization_classification": read_json(LOCALIZATION_PACKET_PATH).get("classification"),
        "accepted_driver_class": read_json(SIGNAL_DRIVER_PROFILE_PATH).get("driver_class"),
        "true_payload_boundary_violation": guard_packet["true_payload_boundary_violation"],
        "review_only_no_rerun": True,
        "repair_executed_in_this_unit": False,
        "recommended_next_handling": guard_packet["recommended_next_handling"],
    }

    next_decision = {
        "schema_version": "r10000_signal_localization_failure_review_next_decision_packet_v0",
        "packet_status": "R10000_SIGNAL_LOCALIZATION_FAILURE_REVIEW_COMPLETE_GUARD_FALSE_POSITIVE_PATCH_READY",
        "source_failed_r10000_signal_localization_receipt_id": SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID,
        "guard_classification": guard_packet["classification"],
        "substantive_finding_to_preserve": {
            "localization_classification": read_json(LOCALIZATION_PACKET_PATH).get("classification"),
            "driver_class": read_json(SIGNAL_DRIVER_PROFILE_PATH).get("driver_class"),
            "recommended_next_after_patch": "DECIDE_CLOSE_OR_FREEZE_BOUNDED_OBSERVABILITY_PROTOCOL_AFTER_R10000_VOLATILE_ONLY_SIGNAL_V0",
        },
        "safe_next_choices": [
            "patch protected-key guard to distinguish references from materialization",
            "after patch, accept volatile-only localization and decide close/freeze",
            "do not rerun radius-10000 for this correction",
            "do not inspect row payloads or closed groups",
        ],
        "recommended_next_handling": guard_packet["recommended_next_handling"],
        "auto_next_command": None,
    }

    report = {
        "schema_version": "r10000_signal_localization_failure_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_r10000_signal_localization_receipt_id": SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID,
        "failed_localization_receipt_consumed_count": 1,
        "failed_localization_artifacts_consumed_count": 1,
        "failure_review_surface_emitted_count": 1,
        "protected_key_hit_review_emitted_count": 1,
        "localization_finding_review_emitted_count": 1,
        "guard_classification_packet_emitted_count": 1,
        "fix_authority_packet_emitted_count": 1,
        "review_decision_emitted_count": 1,
        "next_decision_packet_emitted_count": 1,
        "protected_payload_key_hit_count": hit_review["protected_payload_key_hit_count"],
        "protected_key_reference_only_count": 1 if hit_review["classification"] == "PROTECTED_KEY_NAME_REFERENCE_ONLY_NO_PAYLOAD_BOUNDARY_CROSSING" else 0,
        "false_positive_guard_classification_count": 1 if guard_packet["classification"] == "OVERSTRICT_PROTECTED_KEY_GUARD_FALSE_POSITIVE_ACCEPT_FINDING_AFTER_REVIEW" else 0,
        "true_payload_boundary_violation_count": 1 if guard_packet["true_payload_boundary_violation"] else 0,
        "substantive_finding_supported_count": 1 if finding_review["finding_supported_despite_gate_fail"] else 0,
        "accepted_localization_classification": read_json(LOCALIZATION_PACKET_PATH).get("classification"),
        "accepted_driver_class": read_json(SIGNAL_DRIVER_PROFILE_PATH).get("driver_class"),
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
        "recommended_next_handling": guard_packet["recommended_next_handling"],
    }

    trace = {
        "schema_version": "r10000_signal_localization_failure_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_failed_localization_receipt",
                "question": "failed receipt is gate-fail due protected key hits",
                "answer": True,
                "taken": "review_protected_key_hits",
            },
            {
                "step": "review_protected_key_hits",
                "question": "did protected key hits cross payload/materialization boundary",
                "answer": guard_packet["true_payload_boundary_violation"],
                "taken": "review_substantive_localization_finding",
            },
            {
                "step": "review_substantive_localization_finding",
                "question": "is volatile-only localization supported despite gate fail",
                "answer": finding_review["finding_supported_despite_gate_fail"],
                "taken": "emit_guard_false_positive_fix_authority",
            },
            {
                "step": "emit_guard_false_positive_fix_authority",
                "question": "repair now",
                "answer": False,
                "taken": "STOP_R10000_SIGNAL_LOCALIZATION_FAILURE_REVIEW_COMPLETE_GUARD_FALSE_POSITIVE_PATCH_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_R10000_SIGNAL_LOCALIZATION_FAILURE_REVIEW_COMPLETE_GUARD_FALSE_POSITIVE_PATCH_REQUIRED",
            "next_command_goal": None,
        },
    }

    write_json(FAILURE_REVIEW_SURFACE_PATH, review_surface)
    write_json(PROTECTED_KEY_HIT_REVIEW_PATH, hit_review)
    write_json(LOCALIZATION_FINDING_REVIEW_PATH, finding_review)
    write_json(GUARD_CLASSIFICATION_PACKET_PATH, guard_packet)
    write_json(FIX_AUTHORITY_PACKET_PATH, authority)
    write_json(REVIEW_DECISION_PATH, decision)
    write_json(NEXT_DECISION_PACKET_PATH, next_decision)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(hit_review, finding_review, guard_packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "R10000_LOCALIZATION_FAILURE_REVIEW_0_FAILED_RECEIPT_CONSUMED": True,
        "R10000_LOCALIZATION_FAILURE_REVIEW_1_PROTECTED_KEY_FAILURE_CONFIRMED": hit_review["protected_payload_key_hit_count"] == 30000,
        "R10000_LOCALIZATION_FAILURE_REVIEW_2_BOUNDARY_COUNTERS_CLEAN": hit_review["boundary_clean"] is True,
        "R10000_LOCALIZATION_FAILURE_REVIEW_3_SUBSTANTIVE_FINDING_SUPPORTED": finding_review["finding_supported_despite_gate_fail"] is True,
        "R10000_LOCALIZATION_FAILURE_REVIEW_4_GUARD_FALSE_POSITIVE_CLASSIFIED": guard_packet["classification"] == "OVERSTRICT_PROTECTED_KEY_GUARD_FALSE_POSITIVE_ACCEPT_FINDING_AFTER_REVIEW",
        "R10000_LOCALIZATION_FAILURE_REVIEW_5_FIX_AUTHORITY_PACKET_EMITTED": report["fix_authority_packet_emitted_count"] == 1,
        "R10000_LOCALIZATION_FAILURE_REVIEW_6_NO_RERUN_OR_PROBE": report["radius_10000_rerun_count"] == 0 and report["new_small_probe_count"] == 0,
        "R10000_LOCALIZATION_FAILURE_REVIEW_7_NO_UNBOUNDED_OR_RADIUS_ABOVE_10000": report["unbounded_or_no_cap_run_count"] == 0 and report["radius_above_10000_run_count"] == 0,
        "R10000_LOCALIZATION_FAILURE_REVIEW_8_NO_QUEUE_OR_ROW_ACTION": report["queue_reopened_count"] == 0 and report["row_payload_materialized_count"] == 0 and report["row_payload_inspected_count"] == 0,
        "R10000_LOCALIZATION_FAILURE_REVIEW_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "R10000_LOCALIZATION_FAILURE_REVIEW_10_NO_REPAIR_OR_TAXONOMY": report["repair_executed_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "R10000_LOCALIZATION_FAILURE_REVIEW_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_failed_r10000_signal_localization_receipt_id": SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID,
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
        "source_failed_r10000_signal_localization_receipt_id": SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID,
        "guard_classification": guard_packet["classification"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "failure_review_surface": rel(FAILURE_REVIEW_SURFACE_PATH),
        "protected_key_hit_review": rel(PROTECTED_KEY_HIT_REVIEW_PATH),
        "localization_finding_review": rel(LOCALIZATION_FINDING_REVIEW_PATH),
        "guard_classification_packet": rel(GUARD_CLASSIFICATION_PACKET_PATH),
        "fix_authority_packet": rel(FIX_AUTHORITY_PACKET_PATH),
        "review_decision": rel(REVIEW_DECISION_PATH),
        "next_decision_packet": rel(NEXT_DECISION_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "failed_localization_receipt": rel(FAILED_RECEIPT_PATH),
        "failed_localization_packet": rel(LOCALIZATION_PACKET_PATH),
        "failed_signal_driver_profile": rel(SIGNAL_DRIVER_PROFILE_PATH),
    }

    receipt = {
        "schema_version": "r10000_signal_localization_failure_protected_key_hits_review_receipt_v0",
        "receipt_type": "R10000_SIGNAL_LOCALIZATION_FAILURE_PROTECTED_KEY_HITS_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_r10000_signal_localization_receipt_id": SOURCE_FAILED_R10000_SIGNAL_LOCALIZATION_RECEIPT_ID,
        "source_r10000_signal_inspection_receipt_id": SOURCE_R10000_SIGNAL_INSPECTION_RECEIPT_ID,
        "source_radius_10000_result_review_receipt_id": SOURCE_RADIUS_10000_RESULT_REVIEW_RECEIPT_ID,
        "source_radius_10000_retry_receipt_id": SOURCE_RADIUS_10000_RETRY_RECEIPT_ID,
        "source_cli_wrapper_intercept_parse_fix_receipt_id": SOURCE_CLI_WRAPPER_INTERCEPT_PARSE_FIX_RECEIPT_ID,
        "source_pressure_queue_closure_review_receipt_id": SOURCE_PRESSURE_QUEUE_CLOSURE_REVIEW_RECEIPT_ID,
        "source_synthetic_remainder_expected_limit_mark_receipt_id": SOURCE_SYNTHETIC_REMAINDER_EXPECTED_LIMIT_MARK_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "r10000_signal_localization_failure_review_summary": {
            "review_result": decision["decision_status"],
            "guard_classification": guard_packet["classification"],
            "protected_key_hit_classification": hit_review["classification"],
            "protected_payload_key_hit_count": hit_review["protected_payload_key_hit_count"],
            "boundary_clean": hit_review["boundary_clean"],
            "true_payload_boundary_violation": guard_packet["true_payload_boundary_violation"],
            "substantive_localization_finding_supported": finding_review["finding_supported_despite_gate_fail"],
            "accepted_localization_classification": decision["accepted_substantive_localization_classification"],
            "accepted_driver_class": decision["accepted_driver_class"],
            "review_only_no_rerun": True,
            "recommended_next_handling": decision["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "r10000_signal_localization_failure_review_guards": guards_packet,
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
    print(f"r10000_signal_localization_failure_review_receipt_id={receipt_id}")
    print(f"r10000_signal_localization_failure_review_receipt_path=data/r10000_distinguishable_signal_localization_failure_protected_key_hits_review_v0_receipts/{receipt_id}.json")
    print(f"fix_authority_packet_path=data/r10000_distinguishable_signal_localization_failure_protected_key_hits_review_v0/r10000_signal_localization_failure_fix_authority_packet.json")
    print(f"next_decision_packet_path=data/r10000_distinguishable_signal_localization_failure_protected_key_hits_review_v0/r10000_signal_localization_failure_review_next_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
