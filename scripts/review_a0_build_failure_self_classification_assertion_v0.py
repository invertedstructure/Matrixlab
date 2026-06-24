#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_A0_BUILD_FAILURE_SELF_CLASSIFICATION_ASSERTION_V0"
TARGET_UNIT_ID = "a0.build_failure.self_classification_assertion.review.v0"
SOURCE_A0_BUILD_RECEIPT_ID = "067fcaed"
SOURCE_A0_BUILD_UNIT_ID = "BUILD_A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_V0"

OUT_DIR = ROOT / "data" / "a0_build_failure_self_classification_assertion_review_v0"
RECEIPT_DIR = ROOT / "data" / "a0_build_failure_self_classification_assertion_review_v0_receipts"

REVIEW_SURFACE_PATH = OUT_DIR / "a0_self_classification_failure_review_surface.json"
SELF_CLASSIFICATION_OBSERVATION_PATH = OUT_DIR / "a0_self_classification_observation.json"
ASSERTION_MISMATCH_REVIEW_PATH = OUT_DIR / "a0_self_classification_assertion_mismatch_review.json"
SUBSTANTIVE_BUILD_REVIEW_PATH = OUT_DIR / "a0_substantive_build_review.json"
FIX_AUTHORITY_PACKET_PATH = OUT_DIR / "a0_self_classification_assertion_fix_authority_packet.json"
REVIEW_DECISION_PATH = OUT_DIR / "a0_self_classification_failure_review_decision.json"
NEXT_DECISION_PACKET_PATH = OUT_DIR / "a0_self_classification_failure_review_next_decision_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "a0_self_classification_failure_review_transition_trace.json"
REPORT_PATH = OUT_DIR / "a0_self_classification_failure_review_report.json"

A0_RECEIPT_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0_receipts" / f"{SOURCE_A0_BUILD_RECEIPT_ID}.json"
A0_OUTPUT_SCHEMA_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0" / "a0_output_schema_v0.json"
A0_QUESTION_SET_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0" / "a0_question_set_v0.json"
A0_CLASSIFICATION_ENUM_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0" / "a0_classification_enum_v0.json"
A0_PRESSURE_ENUM_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0" / "a0_pressure_enum_v0.json"
A0_COMMAND_CANDIDATE_SCHEMA_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0" / "a0_command_candidate_schema_v0.json"
A0_MISSING_OBJECT_PROPOSAL_SCHEMA_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0" / "a0_missing_object_proposal_schema_v0.json"
A0_CLASSIFIER_TABLE_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0" / "a0_classifier_table_v0.json"
A0_PROBE_CASE_MANIFEST_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0" / "a0_probe_case_manifest.json"
A0_PROBE_RESULTS_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0" / "a0_probe_results.jsonl"
A0_NEGATIVE_CONTROL_RESULTS_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0" / "a0_negative_control_results.jsonl"
A0_REPORT_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0" / "a0_transition_layer_report.json"
A0_ADAPTER_PATH = ROOT / "scripts" / "a0_receipt_to_builder_transition_layer_v0.py"

SOURCE_FILES = [
    A0_RECEIPT_PATH,
    A0_OUTPUT_SCHEMA_PATH,
    A0_QUESTION_SET_PATH,
    A0_CLASSIFICATION_ENUM_PATH,
    A0_PRESSURE_ENUM_PATH,
    A0_COMMAND_CANDIDATE_SCHEMA_PATH,
    A0_MISSING_OBJECT_PROPOSAL_SCHEMA_PATH,
    A0_CLASSIFIER_TABLE_PATH,
    A0_PROBE_CASE_MANIFEST_PATH,
    A0_PROBE_RESULTS_PATH,
    A0_NEGATIVE_CONTROL_RESULTS_PATH,
    A0_REPORT_PATH,
    A0_ADAPTER_PATH,
]

HUMAN_DECISION = {
    "decision": "REVIEW_A0_BUILD_FAILURE_SELF_CLASSIFICATION_ASSERTION",
    "scope": "Review the failed A0 wrapper assertion. Determine whether A0 itself built successfully and whether the block failed only because the wrapper expected STOP_LANE_CLOSED when classifying the raw A0 build receipt, even though A0 correctly returned QUESTION_PACKET_NOT_COMMAND for an incomplete explicit receipt surface/source-selection bundle.",
    "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
    "authorized": [
        "consume A0 build receipt and artifacts",
        "re-run A0 classify against the A0 build receipt as non-writing observation",
        "classify the post-build wrapper assertion failure",
        "preserve substantive A0 build if supported",
        "emit narrow fix authority packet",
        "stop before patching or live frontier application",
    ],
    "not_authorized": [
        "execute builder command",
        "execute repair",
        "mutate A0 source artifacts",
        "mutate prior receipts",
        "apply A0 to current frontier",
        "select live frontier by latest-file guessing",
        "select live frontier by mtime sorting",
        "invent next objective",
        "infer roadmap from strategic discussion",
        "weaken A0 classifier law",
        "treat QUESTION_PACKET_NOT_COMMAND as an A0 classifier failure",
        "hide next command",
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

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def load_a0_module():
    spec = importlib.util.spec_from_file_location("a0_adapter", A0_ADAPTER_PATH)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def validate_sources() -> List[str]:
    failures: List[str] = []
    receipt = read_json(A0_RECEIPT_PATH)
    report = read_json(A0_REPORT_PATH)
    classification_enum = read_json(A0_CLASSIFICATION_ENUM_PATH)
    command_schema = read_json(A0_COMMAND_CANDIDATE_SCHEMA_PATH)
    probe_rows = read_jsonl(A0_PROBE_RESULTS_PATH)
    negative_rows = read_jsonl(A0_NEGATIVE_CONTROL_RESULTS_PATH)

    if receipt.get("receipt_id") != SOURCE_A0_BUILD_RECEIPT_ID:
        failures.append("a0_build_receipt_id_wrong")
    if receipt.get("unit_id") != SOURCE_A0_BUILD_UNIT_ID:
        failures.append("a0_build_unit_wrong")
    if receipt.get("gate") != "PASS":
        failures.append("a0_build_receipt_gate_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != "STOP_HUMAN_DECISION_REQUIRED":
        failures.append("a0_terminal_not_human_decision_required")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("a0_terminal_next_not_null")

    summary = receipt.get("a0_build_summary", {})
    if summary.get("build_result") != "A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILT":
        failures.append("a0_summary_not_built")
    if summary.get("probe_count") != 7 or summary.get("probe_pass_count") != 7:
        failures.append("a0_probe_counts_not_all_pass")
    if summary.get("negative_control_count") != 18 or summary.get("negative_control_pass_count") != 18:
        failures.append("a0_negative_counts_not_all_pass")
    if summary.get("builder_command_executed_count") != 0:
        failures.append("a0_builder_command_executed")
    if summary.get("live_frontier_application_count") != 0:
        failures.append("a0_live_frontier_applied")

    if report.get("probes_ok") is not True:
        failures.append("a0_report_probes_not_ok")
    if report.get("negative_controls_ok") is not True:
        failures.append("a0_report_negative_controls_not_ok")
    if report.get("builder_command_executed_count") != 0:
        failures.append("a0_report_builder_command_executed")
    if report.get("live_frontier_application_count") != 0:
        failures.append("a0_report_live_frontier_applied")
    if report.get("first_live_use_candidate") != "APPLY_A0_TO_CURRENT_RECEIPT_CHAIN_FRONTIER_V0":
        failures.append("a0_first_live_use_candidate_wrong")

    if "QUESTION_PACKET_NOT_COMMAND" not in classification_enum.get("classification_values", []):
        failures.append("a0_classification_enum_missing_question_packet")
    if "STOP_LANE_CLOSED" not in classification_enum.get("classification_values", []):
        failures.append("a0_classification_enum_missing_stop_lane_closed")
    if command_schema.get("required_constant", {}).get("execution_authorized") is not False:
        failures.append("a0_command_candidate_schema_execution_authorized_not_false")

    if len(probe_rows) != 7 or not all(row.get("probe_pass") is True for row in probe_rows):
        failures.append("a0_probe_rows_not_all_pass")
    if len(negative_rows) != 18 or not all(row.get("negative_control_pass") is True and row.get("wrote_live_artifact") is False for row in negative_rows):
        failures.append("a0_negative_rows_not_all_pass_or_nonwriting")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
    return failures

def observe_self_classification() -> Dict[str, Any]:
    a0 = load_a0_module()
    receipt = read_json(A0_RECEIPT_PATH)
    result = a0.classify_receipt(receipt)
    return {
        "schema_version": "a0_self_classification_observation_v0",
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "observed_classification": result.get("classification", {}).get("result"),
        "observed_reason": result.get("classification", {}).get("reason"),
        "expected_by_failed_wrapper": "STOP_LANE_CLOSED",
        "expected_by_a0_law_for_incomplete_surface": "QUESTION_PACKET_NOT_COMMAND",
        "receipt_surface_explicit": result.get("question_answers", {}).get("receipt_surface_explicit"),
        "source_selection_valid": result.get("question_answers", {}).get("source_selection_valid"),
        "negative_controls_clean": result.get("question_answers", {}).get("negative_controls_clean"),
        "negative_controls_absent": result.get("question_answers", {}).get("negative_controls_absent"),
        "builder_command_allowed": result.get("classification", {}).get("builder_command_allowed"),
        "builder_command_candidate": result.get("builder_command_candidate"),
        "decision_packet": result.get("decision_packet"),
        "raw_a0_result": result,
    }

def build_assertion_mismatch_review(observation: Dict[str, Any]) -> Dict[str, Any]:
    mismatch_only = (
        observation["observed_classification"] == "QUESTION_PACKET_NOT_COMMAND"
        and observation["expected_by_failed_wrapper"] == "STOP_LANE_CLOSED"
        and observation["receipt_surface_explicit"] is False
        and observation["source_selection_valid"] is False
        and observation["builder_command_allowed"] is False
        and observation["builder_command_candidate"] is None
    )
    return {
        "schema_version": "a0_self_classification_assertion_mismatch_review_v0",
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "classification": "WRAPPER_ASSERTION_EXPECTED_STOP_LANE_CLOSED_BUT_A0_CORRECTLY_RETURNED_QUESTION_PACKET_NOT_COMMAND" if mismatch_only else "A0_SELF_CLASSIFICATION_REVIEW_INCONCLUSIVE",
        "mismatch_only": mismatch_only,
        "failed_wrapper_expected": observation["expected_by_failed_wrapper"],
        "a0_observed": observation["observed_classification"],
        "a0_expected_for_observed_surface": observation["expected_by_a0_law_for_incomplete_surface"],
        "why_a0_question_packet_is_correct": [
            "raw A0 build receipt has no receipt_path field inside its JSON payload",
            "raw A0 build receipt has no source_selection_rule field",
            "some negative-control keys expected by A0 input schema are absent from this raw receipt shape",
            "A0 law requires explicit receipt bundle selection before classifying a receipt as closed lane",
            "A0 must prefer no command over fake command",
        ],
        "fix_target": "post-build wrapper assertion, not A0 classifier law",
    }

def build_substantive_review() -> Dict[str, Any]:
    receipt = read_json(A0_RECEIPT_PATH)
    report = read_json(A0_REPORT_PATH)
    probe_rows = read_jsonl(A0_PROBE_RESULTS_PATH)
    negative_rows = read_jsonl(A0_NEGATIVE_CONTROL_RESULTS_PATH)

    supported = (
        receipt.get("gate") == "PASS"
        and receipt.get("a0_build_summary", {}).get("build_result") == "A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILT"
        and report.get("probes_ok") is True
        and report.get("negative_controls_ok") is True
        and len(probe_rows) == 7
        and all(row.get("probe_pass") is True for row in probe_rows)
        and len(negative_rows) == 18
        and all(row.get("negative_control_pass") is True and row.get("wrote_live_artifact") is False for row in negative_rows)
        and receipt.get("aggregate_metrics", {}).get("builder_command_executed_count") == 0
        and receipt.get("aggregate_metrics", {}).get("hidden_next_command_count") == 0
        and receipt.get("aggregate_metrics", {}).get("live_frontier_application_count") == 0
    )
    return {
        "schema_version": "a0_substantive_build_review_v0",
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "a0_build_gate": receipt.get("gate"),
        "a0_build_result": receipt.get("a0_build_summary", {}).get("build_result"),
        "probe_count": report.get("probe_count"),
        "probe_pass_count": report.get("probe_pass_count"),
        "negative_control_count": report.get("negative_control_count"),
        "negative_control_pass_count": report.get("negative_control_pass_count"),
        "builder_command_executed_count": receipt.get("aggregate_metrics", {}).get("builder_command_executed_count"),
        "hidden_next_command_count": receipt.get("aggregate_metrics", {}).get("hidden_next_command_count"),
        "live_frontier_application_count": receipt.get("aggregate_metrics", {}).get("live_frontier_application_count"),
        "terminal": receipt.get("terminal"),
        "substantive_a0_build_supported_despite_block_exit_failure": supported,
    }

def validate_outputs(assertion_review: Dict[str, Any], substantive_review: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if assertion_review.get("mismatch_only") is not True:
        failures.append("assertion_mismatch_only_not_true")
    if assertion_review.get("fix_target") != "post-build wrapper assertion, not A0 classifier law":
        failures.append("fix_target_wrong")
    if substantive_review.get("substantive_a0_build_supported_despite_block_exit_failure") is not True:
        failures.append("substantive_a0_build_not_supported")

    for key in [
        "builder_command_executed_count",
        "repair_executed_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
        "live_frontier_application_count",
        "a0_classifier_law_mutation_count",
        "latest_or_mtime_selection_count",
        "strategic_discussion_as_authority_count",
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
        "a0_build_receipt_consumed_count",
        "a0_build_artifacts_consumed_count",
        "self_classification_observation_emitted_count",
        "assertion_mismatch_review_emitted_count",
        "substantive_build_review_emitted_count",
        "fix_authority_packet_emitted_count",
        "review_decision_emitted_count",
        "next_decision_packet_emitted_count",
        "assertion_mismatch_only_count",
        "substantive_a0_build_supported_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    for key in [
        "builder_command_executed_count",
        "repair_executed_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
        "live_frontier_application_count",
        "a0_classifier_law_mutation_count",
        "latest_or_mtime_selection_count",
        "strategic_discussion_as_authority_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_A0_BUILD_FAILURE_REVIEW_COMPLETE_SELF_CLASSIFICATION_ASSERTION_PATCH_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    observation = observe_self_classification()
    assertion_review = build_assertion_mismatch_review(observation)
    substantive_review = build_substantive_review()

    review_surface = {
        "schema_version": "a0_self_classification_failure_review_surface_v0",
        "review_surface_id": sha8({
            "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
            "observed": observation["observed_classification"],
            "classification": assertion_review["classification"],
        }),
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "source_a0_build_unit_id": SOURCE_A0_BUILD_UNIT_ID,
        "block_failure_class": "POST_BUILD_WRAPPER_ASSERTION_FAILURE",
        "a0_build_receipt_gate": read_json(A0_RECEIPT_PATH).get("gate"),
        "a0_build_terminal": read_json(A0_RECEIPT_PATH).get("terminal"),
        "observed_self_classification": observation["observed_classification"],
        "failed_wrapper_expected_classification": observation["expected_by_failed_wrapper"],
        "assertion_review_classification": assertion_review["classification"],
        "substantive_a0_build_supported": substantive_review["substantive_a0_build_supported_despite_block_exit_failure"],
    }

    fix_authority = {
        "schema_version": "a0_self_classification_assertion_fix_authority_packet_v0",
        "packet_status": "A0_SELF_CLASSIFICATION_ASSERTION_REVIEWED_NARROW_WRAPPER_PATCH_AUTHORIZED",
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "authority_classification": assertion_review["classification"],
        "authorized_next_unit": "PATCH_A0_BUILD_SELF_CLASSIFICATION_ASSERTION_TO_EXPLICIT_BUNDLE_OR_QUESTION_PACKET_ACCEPTANCE_V0",
        "required_fix_shape": [
            "do not mutate A0 classifier law",
            "do not execute builder command",
            "do not apply A0 to current frontier",
            "preserve A0 build artifacts",
            "replace self-classification assertion with explicit receipt bundle fixture or accept QUESTION_PACKET_NOT_COMMAND for raw A0 build receipt",
            "package A0 build artifacts and review artifacts",
            "terminal next_command_goal null",
        ],
        "a0_classifier_law_mutation_authorized": False,
        "live_frontier_application_authorized_now": False,
        "builder_command_execution_authorized_now": False,
        "recommended_next_handling": "PATCH_A0_BUILD_SELF_CLASSIFICATION_ASSERTION_TO_EXPLICIT_BUNDLE_OR_QUESTION_PACKET_ACCEPTANCE_V0",
    }

    decision = {
        "schema_version": "a0_self_classification_failure_review_decision_v0",
        "decision_status": "A0_BUILD_FAILURE_REVIEW_ACCEPTS_WRAPPER_ASSERTION_MISMATCH_ONLY",
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "assertion_review_classification": assertion_review["classification"],
        "substantive_a0_build_supported": substantive_review["substantive_a0_build_supported_despite_block_exit_failure"],
        "accepted_a0_build_result": substantive_review["a0_build_result"],
        "accepted_probe_pass_count": substantive_review["probe_pass_count"],
        "accepted_negative_control_pass_count": substantive_review["negative_control_pass_count"],
        "true_a0_classifier_failure": False,
        "true_a0_build_failure": False,
        "review_only_no_patch": True,
        "recommended_next_handling": fix_authority["recommended_next_handling"],
    }

    next_decision = {
        "schema_version": "a0_self_classification_failure_review_next_decision_packet_v0",
        "packet_status": "A0_BUILD_FAILURE_REVIEW_COMPLETE_SELF_CLASSIFICATION_ASSERTION_PATCH_READY",
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "assertion_review_classification": assertion_review["classification"],
        "substantive_a0_build_to_preserve": {
            "a0_build_result": substantive_review["a0_build_result"],
            "probe_pass_count": substantive_review["probe_pass_count"],
            "negative_control_pass_count": substantive_review["negative_control_pass_count"],
            "terminal": substantive_review["terminal"],
        },
        "safe_next_choices": [
            "patch the wrapper assertion only",
            "accept QUESTION_PACKET_NOT_COMMAND for raw A0 build receipt self-classification",
            "or construct an explicit receipt bundle fixture for STOP_LANE_CLOSED assertion",
            "do not mutate A0 classifier law",
            "do not apply A0 to current frontier in this patch",
        ],
        "recommended_next_handling": fix_authority["recommended_next_handling"],
        "auto_next_command": None,
    }

    report = {
        "schema_version": "a0_self_classification_failure_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "a0_build_receipt_consumed_count": 1,
        "a0_build_artifacts_consumed_count": 1,
        "self_classification_observation_emitted_count": 1,
        "assertion_mismatch_review_emitted_count": 1,
        "substantive_build_review_emitted_count": 1,
        "fix_authority_packet_emitted_count": 1,
        "review_decision_emitted_count": 1,
        "next_decision_packet_emitted_count": 1,
        "assertion_mismatch_only_count": 1 if assertion_review["mismatch_only"] else 0,
        "substantive_a0_build_supported_count": 1 if substantive_review["substantive_a0_build_supported_despite_block_exit_failure"] else 0,
        "observed_self_classification": observation["observed_classification"],
        "failed_wrapper_expected_classification": observation["expected_by_failed_wrapper"],
        "accepted_a0_build_result": substantive_review["a0_build_result"],
        "accepted_probe_pass_count": substantive_review["probe_pass_count"],
        "accepted_negative_control_pass_count": substantive_review["negative_control_pass_count"],
        "builder_command_executed_count": 0,
        "repair_executed_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "live_frontier_application_count": 0,
        "a0_classifier_law_mutation_count": 0,
        "latest_or_mtime_selection_count": 0,
        "strategic_discussion_as_authority_count": 0,
        "recommended_next_handling": fix_authority["recommended_next_handling"],
    }

    trace = {
        "schema_version": "a0_self_classification_failure_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_a0_build_receipt",
                "question": "did A0 build receipt pass",
                "answer": read_json(A0_RECEIPT_PATH).get("gate") == "PASS",
                "taken": "observe_self_classification",
            },
            {
                "step": "observe_self_classification",
                "question": "did raw A0 build receipt classify as QUESTION_PACKET_NOT_COMMAND",
                "answer": observation["observed_classification"] == "QUESTION_PACKET_NOT_COMMAND",
                "taken": "review_wrapper_assertion",
            },
            {
                "step": "review_wrapper_assertion",
                "question": "was the failed expectation wrong because the raw receipt was not an explicit A0 bundle",
                "answer": assertion_review["mismatch_only"],
                "taken": "preserve_substantive_build",
            },
            {
                "step": "preserve_substantive_build",
                "question": "are probes/negative controls/build artifacts valid",
                "answer": substantive_review["substantive_a0_build_supported_despite_block_exit_failure"],
                "taken": "emit_patch_authority",
            },
            {
                "step": "emit_patch_authority",
                "question": "patch now",
                "answer": False,
                "taken": "STOP_A0_BUILD_FAILURE_REVIEW_COMPLETE_SELF_CLASSIFICATION_ASSERTION_PATCH_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_A0_BUILD_FAILURE_REVIEW_COMPLETE_SELF_CLASSIFICATION_ASSERTION_PATCH_REQUIRED",
            "next_command_goal": None,
        },
    }

    write_json(REVIEW_SURFACE_PATH, review_surface)
    write_json(SELF_CLASSIFICATION_OBSERVATION_PATH, observation)
    write_json(ASSERTION_MISMATCH_REVIEW_PATH, assertion_review)
    write_json(SUBSTANTIVE_BUILD_REVIEW_PATH, substantive_review)
    write_json(FIX_AUTHORITY_PACKET_PATH, fix_authority)
    write_json(REVIEW_DECISION_PATH, decision)
    write_json(NEXT_DECISION_PACKET_PATH, next_decision)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(assertion_review, substantive_review, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "A0_SELF_CLASS_REVIEW_0_A0_BUILD_RECEIPT_CONSUMED": True,
        "A0_SELF_CLASS_REVIEW_1_A0_BUILD_GATE_PASS_PRESERVED": read_json(A0_RECEIPT_PATH).get("gate") == "PASS",
        "A0_SELF_CLASS_REVIEW_2_SELF_CLASSIFICATION_OBSERVED": observation["observed_classification"] == "QUESTION_PACKET_NOT_COMMAND",
        "A0_SELF_CLASS_REVIEW_3_WRAPPER_ASSERTION_MISMATCH_CONFIRMED": assertion_review["mismatch_only"] is True,
        "A0_SELF_CLASS_REVIEW_4_SUBSTANTIVE_BUILD_SUPPORTED": substantive_review["substantive_a0_build_supported_despite_block_exit_failure"] is True,
        "A0_SELF_CLASS_REVIEW_5_FIX_AUTHORITY_PACKET_EMITTED": report["fix_authority_packet_emitted_count"] == 1,
        "A0_SELF_CLASS_REVIEW_6_NO_BUILDER_COMMAND_EXECUTED": report["builder_command_executed_count"] == 0,
        "A0_SELF_CLASS_REVIEW_7_NO_REPAIR_EXECUTED": report["repair_executed_count"] == 0,
        "A0_SELF_CLASS_REVIEW_8_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "A0_SELF_CLASS_REVIEW_9_NO_LIVE_FRONTIER_APPLICATION": report["live_frontier_application_count"] == 0,
        "A0_SELF_CLASS_REVIEW_10_NO_A0_CLASSIFIER_LAW_MUTATION": report["a0_classifier_law_mutation_count"] == 0,
        "A0_SELF_CLASS_REVIEW_11_NO_LATEST_OR_MTIME_SELECTION": report["latest_or_mtime_selection_count"] == 0,
        "A0_SELF_CLASS_REVIEW_12_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards_packet = {
        "review_only_no_patch": True,
        "builder_command_executed": False,
        "repair_executed": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "live_frontier_applied": False,
        "a0_classifier_law_mutated": False,
        "latest_or_mtime_selection_used": False,
        "strategic_discussion_as_authority": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "classification": assertion_review["classification"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "review_surface": rel(REVIEW_SURFACE_PATH),
        "self_classification_observation": rel(SELF_CLASSIFICATION_OBSERVATION_PATH),
        "assertion_mismatch_review": rel(ASSERTION_MISMATCH_REVIEW_PATH),
        "substantive_build_review": rel(SUBSTANTIVE_BUILD_REVIEW_PATH),
        "fix_authority_packet": rel(FIX_AUTHORITY_PACKET_PATH),
        "review_decision": rel(REVIEW_DECISION_PATH),
        "next_decision_packet": rel(NEXT_DECISION_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_a0_build_receipt": rel(A0_RECEIPT_PATH),
        "source_a0_transition_report": rel(A0_REPORT_PATH),
        "source_a0_adapter_script": rel(A0_ADAPTER_PATH),
    }

    receipt = {
        "schema_version": "a0_build_failure_self_classification_assertion_review_receipt_v0",
        "receipt_type": "A0_BUILD_FAILURE_SELF_CLASSIFICATION_ASSERTION_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "source_a0_build_unit_id": SOURCE_A0_BUILD_UNIT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "a0_self_classification_failure_review_summary": {
            "review_result": decision["decision_status"],
            "assertion_review_classification": assertion_review["classification"],
            "observed_self_classification": observation["observed_classification"],
            "failed_wrapper_expected_classification": observation["expected_by_failed_wrapper"],
            "substantive_a0_build_supported": substantive_review["substantive_a0_build_supported_despite_block_exit_failure"],
            "accepted_a0_build_result": substantive_review["a0_build_result"],
            "accepted_probe_pass_count": substantive_review["probe_pass_count"],
            "accepted_negative_control_pass_count": substantive_review["negative_control_pass_count"],
            "true_a0_classifier_failure": decision["true_a0_classifier_failure"],
            "true_a0_build_failure": decision["true_a0_build_failure"],
            "review_only_no_patch": True,
            "recommended_next_handling": fix_authority["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "a0_self_classification_failure_review_guards": guards_packet,
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
    print(f"a0_self_class_review_receipt_id={receipt_id}")
    print(f"a0_self_class_review_receipt_path=data/a0_build_failure_self_classification_assertion_review_v0_receipts/{receipt_id}.json")
    print(f"fix_authority_packet_path=data/a0_build_failure_self_classification_assertion_review_v0/a0_self_classification_assertion_fix_authority_packet.json")
    print(f"next_decision_packet_path=data/a0_build_failure_self_classification_assertion_review_v0/a0_self_classification_failure_review_next_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
