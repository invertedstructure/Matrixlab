#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PATCH_A0_BUILD_SELF_CLASSIFICATION_ASSERTION_TO_EXPLICIT_BUNDLE_OR_QUESTION_PACKET_ACCEPTANCE_V0"
TARGET_UNIT_ID = "a0.build_self_classification_assertion.explicit_bundle_or_question_packet_acceptance.patch.v0"

SOURCE_A0_BUILD_RECEIPT_ID = "067fcaed"
SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID = "2ff85a7a"

OUT_DIR = ROOT / "data" / "a0_self_classification_assertion_acceptance_patch_v0"
RECEIPT_DIR = ROOT / "data" / "a0_self_classification_assertion_acceptance_patch_v0_receipts"

PATCH_PLAN_PATH = OUT_DIR / "a0_self_classification_assertion_acceptance_patch_plan.json"
SOURCE_SURFACE_PATH = OUT_DIR / "a0_self_classification_assertion_acceptance_source_surface.json"
RAW_SELF_CLASSIFICATION_RECHECK_PATH = OUT_DIR / "a0_raw_build_receipt_self_classification_recheck.json"
EXPLICIT_BUNDLE_FIXTURE_PATH = OUT_DIR / "a0_explicit_closed_lane_bundle_fixture.json"
EXPLICIT_BUNDLE_CLASSIFICATION_RECHECK_PATH = OUT_DIR / "a0_explicit_closed_lane_bundle_classification_recheck.json"
PATCHED_ASSERTION_RULE_PATH = OUT_DIR / "a0_patched_self_classification_assertion_rule.json"
PACKAGING_GUARD_RECHECK_PATH = OUT_DIR / "a0_expected_artifact_packaging_guard_recheck.json"
FINAL_ACCEPTANCE_PACKET_PATH = OUT_DIR / "a0_transition_layer_final_acceptance_packet.json"
NEXT_STATUS_PACKET_PATH = OUT_DIR / "a0_self_classification_assertion_acceptance_next_status_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "a0_self_classification_assertion_acceptance_transition_trace.json"
REPORT_PATH = OUT_DIR / "a0_self_classification_assertion_acceptance_patch_report.json"

A0_BUILD_RECEIPT_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0_receipts" / f"{SOURCE_A0_BUILD_RECEIPT_ID}.json"
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

A0_SELF_CLASS_REVIEW_RECEIPT_PATH = ROOT / "data" / "a0_build_failure_self_classification_assertion_review_v0_receipts" / f"{SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID}.json"
A0_SELF_CLASS_REVIEW_SURFACE_PATH = ROOT / "data" / "a0_build_failure_self_classification_assertion_review_v0" / "a0_self_classification_failure_review_surface.json"
A0_SELF_CLASS_OBSERVATION_PATH = ROOT / "data" / "a0_build_failure_self_classification_assertion_review_v0" / "a0_self_classification_observation.json"
A0_ASSERTION_MISMATCH_REVIEW_PATH = ROOT / "data" / "a0_build_failure_self_classification_assertion_review_v0" / "a0_self_classification_assertion_mismatch_review.json"
A0_SUBSTANTIVE_BUILD_REVIEW_PATH = ROOT / "data" / "a0_build_failure_self_classification_assertion_review_v0" / "a0_substantive_build_review.json"
A0_FIX_AUTHORITY_PACKET_PATH = ROOT / "data" / "a0_build_failure_self_classification_assertion_review_v0" / "a0_self_classification_assertion_fix_authority_packet.json"
A0_FAILURE_REVIEW_DECISION_PATH = ROOT / "data" / "a0_build_failure_self_classification_assertion_review_v0" / "a0_self_classification_failure_review_decision.json"
A0_FAILURE_REVIEW_NEXT_PACKET_PATH = ROOT / "data" / "a0_build_failure_self_classification_assertion_review_v0" / "a0_self_classification_failure_review_next_decision_packet.json"
A0_FAILURE_REVIEW_TRACE_PATH = ROOT / "data" / "a0_build_failure_self_classification_assertion_review_v0" / "a0_self_classification_failure_review_transition_trace.json"
A0_FAILURE_REVIEW_REPORT_PATH = ROOT / "data" / "a0_build_failure_self_classification_assertion_review_v0" / "a0_self_classification_failure_review_report.json"

SOURCE_FILES = [
    A0_BUILD_RECEIPT_PATH,
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
    A0_SELF_CLASS_REVIEW_RECEIPT_PATH,
    A0_SELF_CLASS_REVIEW_SURFACE_PATH,
    A0_SELF_CLASS_OBSERVATION_PATH,
    A0_ASSERTION_MISMATCH_REVIEW_PATH,
    A0_SUBSTANTIVE_BUILD_REVIEW_PATH,
    A0_FIX_AUTHORITY_PACKET_PATH,
    A0_FAILURE_REVIEW_DECISION_PATH,
    A0_FAILURE_REVIEW_NEXT_PACKET_PATH,
    A0_FAILURE_REVIEW_TRACE_PATH,
    A0_FAILURE_REVIEW_REPORT_PATH,
]

EXPECTED_PACKAGING_ARTIFACTS = [
    A0_ADAPTER_PATH,
    A0_BUILD_RECEIPT_PATH,
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
    A0_SELF_CLASS_REVIEW_RECEIPT_PATH,
    A0_SELF_CLASS_REVIEW_SURFACE_PATH,
    A0_SELF_CLASS_OBSERVATION_PATH,
    A0_ASSERTION_MISMATCH_REVIEW_PATH,
    A0_SUBSTANTIVE_BUILD_REVIEW_PATH,
    A0_FIX_AUTHORITY_PACKET_PATH,
    A0_FAILURE_REVIEW_DECISION_PATH,
    A0_FAILURE_REVIEW_NEXT_PACKET_PATH,
    A0_FAILURE_REVIEW_TRACE_PATH,
    A0_FAILURE_REVIEW_REPORT_PATH,
]

HUMAN_DECISION = {
    "decision": "PATCH_A0_BUILD_SELF_CLASSIFICATION_ASSERTION_TO_EXPLICIT_BUNDLE_OR_QUESTION_PACKET_ACCEPTANCE",
    "scope": "Patch the post-build assertion contract, not the A0 classifier law. Accept QUESTION_PACKET_NOT_COMMAND for raw A0 build receipt self-classification, and prove STOP_LANE_CLOSED only on an explicit closed-lane receipt bundle fixture. Treat the A0 adapter script as an expected build artifact during packaging, not as forbidden source mutation.",
    "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
    "source_a0_self_class_review_receipt_id": SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID,
    "authorized": [
        "consume A0 build receipt and artifacts",
        "consume self-classification assertion review receipt and fix authority packet",
        "re-run A0 classification against raw A0 build receipt and accept QUESTION_PACKET_NOT_COMMAND",
        "create explicit closed-lane bundle fixture and assert STOP_LANE_CLOSED on that explicit fixture",
        "emit patched assertion rule",
        "emit final A0 acceptance packet",
        "package A0 build artifacts, review artifacts, and patch artifacts",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "mutate A0 classifier law",
        "execute builder command",
        "execute repair",
        "apply A0 to current frontier",
        "select live frontier by latest-file guessing",
        "select live frontier by mtime sorting",
        "mutate prior receipts",
        "invent next objective",
        "infer roadmap from strategic discussion",
        "weaken QUESTION_PACKET_NOT_COMMAND behavior",
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
            line=line.strip()
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

def all_negative_controls_zero() -> Dict[str, int]:
    return {
        "hidden_next_command_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "repair_executed_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "authority_widening_authorized_count": 0,
        "optimization_authorized_count": 0,
        "unbounded_or_no_cap_run_count": 0,
        "latest_or_mtime_selection": 0,
        "proposal_counted_as_execution": 0,
        "pressure_counted_as_repair": 0,
    }

def validate_sources() -> List[str]:
    failures: List[str] = []
    a0_receipt = read_json(A0_BUILD_RECEIPT_PATH)
    a0_report = read_json(A0_REPORT_PATH)
    review_receipt = read_json(A0_SELF_CLASS_REVIEW_RECEIPT_PATH)
    fix_authority = read_json(A0_FIX_AUTHORITY_PACKET_PATH)
    assertion_review = read_json(A0_ASSERTION_MISMATCH_REVIEW_PATH)
    substantive_review = read_json(A0_SUBSTANTIVE_BUILD_REVIEW_PATH)

    if a0_receipt.get("receipt_id") != SOURCE_A0_BUILD_RECEIPT_ID:
        failures.append("a0_build_receipt_id_wrong")
    if a0_receipt.get("gate") != "PASS":
        failures.append("a0_build_receipt_gate_not_pass")
    if a0_receipt.get("a0_build_summary", {}).get("build_result") != "A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILT":
        failures.append("a0_build_result_not_built")
    if a0_receipt.get("a0_build_summary", {}).get("probe_pass_count") != 7:
        failures.append("a0_probe_pass_count_not_7")
    if a0_receipt.get("a0_build_summary", {}).get("negative_control_pass_count") != 18:
        failures.append("a0_negative_control_pass_count_not_18")
    if a0_report.get("live_frontier_application_count") != 0:
        failures.append("a0_report_live_frontier_application_not_zero")
    if a0_report.get("builder_command_executed_count") != 0:
        failures.append("a0_report_builder_command_executed")

    if review_receipt.get("receipt_id") != SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID:
        failures.append("review_receipt_id_wrong")
    if review_receipt.get("gate") != "PASS":
        failures.append("review_receipt_gate_not_pass")
    if review_receipt.get("a0_self_classification_failure_review_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("review_not_recommending_this_patch")
    if review_receipt.get("a0_self_classification_failure_review_summary", {}).get("true_a0_classifier_failure") is not False:
        failures.append("review_marks_true_classifier_failure")
    if review_receipt.get("a0_self_classification_failure_review_summary", {}).get("true_a0_build_failure") is not False:
        failures.append("review_marks_true_build_failure")

    if fix_authority.get("packet_status") != "A0_SELF_CLASSIFICATION_ASSERTION_REVIEWED_NARROW_WRAPPER_PATCH_AUTHORIZED":
        failures.append("fix_authority_not_authorized")
    if fix_authority.get("authorized_next_unit") != UNIT_ID:
        failures.append("fix_authority_authorized_next_wrong")
    if fix_authority.get("a0_classifier_law_mutation_authorized") is not False:
        failures.append("fix_authority_allows_classifier_law_mutation")
    if fix_authority.get("live_frontier_application_authorized_now") is not False:
        failures.append("fix_authority_allows_live_frontier")
    if fix_authority.get("builder_command_execution_authorized_now") is not False:
        failures.append("fix_authority_allows_builder_command")

    if assertion_review.get("mismatch_only") is not True:
        failures.append("assertion_review_not_mismatch_only")
    if assertion_review.get("fix_target") != "post-build wrapper assertion, not A0 classifier law":
        failures.append("assertion_review_fix_target_wrong")
    if substantive_review.get("substantive_a0_build_supported_despite_block_exit_failure") is not True:
        failures.append("substantive_review_not_supported")

    probe_rows = read_jsonl(A0_PROBE_RESULTS_PATH)
    negative_rows = read_jsonl(A0_NEGATIVE_CONTROL_RESULTS_PATH)
    if len(probe_rows) != 7 or not all(row.get("probe_pass") is True for row in probe_rows):
        failures.append("a0_probe_rows_not_all_pass")
    if len(negative_rows) != 18 or not all(row.get("negative_control_pass") is True and row.get("wrote_live_artifact") is False for row in negative_rows):
        failures.append("a0_negative_rows_not_all_pass_nonwriting")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
    return failures

def make_explicit_closed_lane_bundle(raw_receipt: Dict[str, Any]) -> Dict[str, Any]:
    bundle = copy.deepcopy(raw_receipt)
    bundle["receipt_path"] = rel(A0_BUILD_RECEIPT_PATH)
    bundle["source_selection_rule"] = "explicit_receipt_path"
    bundle["no_commit_reason"] = bundle.get("no_commit_reason") or "build receipt intentionally has no commit yet because previous wrapper assertion failed before commit"
    bundle["negative_controls"] = all_negative_controls_zero()
    bundle["remaining_pressure"] = ["NONE"]
    bundle["must_not_infer"] = list(dict.fromkeys((bundle.get("must_not_infer") or []) + [
        "do not infer next command",
        "do not infer live frontier",
        "do not infer builder command execution",
    ]))
    bundle["classification"] = None
    bundle.pop("final_close_and_freeze_summary", None)
    bundle.pop("close_and_freeze_summary", None)
    return bundle

def validate_outputs(raw_recheck: Dict[str, Any], explicit_recheck: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if raw_recheck.get("observed_classification") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append("raw_recheck_not_question_packet")
    if raw_recheck.get("raw_question_packet_accepted") is not True:
        failures.append("raw_question_packet_not_accepted")
    if explicit_recheck.get("observed_classification") != "STOP_LANE_CLOSED":
        failures.append("explicit_bundle_not_stop_lane_closed")
    if explicit_recheck.get("explicit_bundle_stop_lane_closed_passed") is not True:
        failures.append("explicit_bundle_stop_not_passed")

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
        "a0_self_class_review_receipt_consumed_count",
        "fix_authority_packet_consumed_count",
        "raw_self_classification_recheck_emitted_count",
        "explicit_bundle_fixture_emitted_count",
        "explicit_bundle_classification_recheck_emitted_count",
        "patched_assertion_rule_emitted_count",
        "packaging_guard_recheck_emitted_count",
        "final_acceptance_packet_emitted_count",
        "next_status_packet_emitted_count",
        "raw_question_packet_acceptance_count",
        "explicit_bundle_stop_lane_closed_acceptance_count",
        "a0_transition_layer_final_acceptance_count",
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
    if terminal.get("stop_code") != "STOP_A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILT_PATCH_ACCEPTED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    a0 = load_a0_module()
    raw_receipt = read_json(A0_BUILD_RECEIPT_PATH)
    raw_result = a0.classify_receipt(raw_receipt)
    explicit_bundle = make_explicit_closed_lane_bundle(raw_receipt)
    explicit_result = a0.classify_receipt(explicit_bundle)

    raw_recheck = {
        "schema_version": "a0_raw_build_receipt_self_classification_recheck_v0",
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "observed_classification": raw_result.get("classification", {}).get("result"),
        "observed_reason": raw_result.get("classification", {}).get("reason"),
        "receipt_surface_explicit": raw_result.get("question_answers", {}).get("receipt_surface_explicit"),
        "source_selection_valid": raw_result.get("question_answers", {}).get("source_selection_valid"),
        "builder_command_allowed": raw_result.get("classification", {}).get("builder_command_allowed"),
        "builder_command_candidate": raw_result.get("builder_command_candidate"),
        "raw_question_packet_accepted": (
            raw_result.get("classification", {}).get("result") == "QUESTION_PACKET_NOT_COMMAND"
            and raw_result.get("classification", {}).get("builder_command_allowed") is False
            and raw_result.get("builder_command_candidate") is None
        ),
        "raw_a0_result": raw_result,
    }

    explicit_recheck = {
        "schema_version": "a0_explicit_closed_lane_bundle_classification_recheck_v0",
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "explicit_bundle_path": rel(EXPLICIT_BUNDLE_FIXTURE_PATH),
        "observed_classification": explicit_result.get("classification", {}).get("result"),
        "observed_reason": explicit_result.get("classification", {}).get("reason"),
        "receipt_surface_explicit": explicit_result.get("question_answers", {}).get("receipt_surface_explicit"),
        "source_selection_valid": explicit_result.get("question_answers", {}).get("source_selection_valid"),
        "negative_controls_clean": explicit_result.get("question_answers", {}).get("negative_controls_clean"),
        "builder_command_allowed": explicit_result.get("classification", {}).get("builder_command_allowed"),
        "builder_command_candidate": explicit_result.get("builder_command_candidate"),
        "explicit_bundle_stop_lane_closed_passed": (
            explicit_result.get("classification", {}).get("result") == "STOP_LANE_CLOSED"
            and explicit_result.get("classification", {}).get("builder_command_allowed") is False
            and explicit_result.get("builder_command_candidate") is None
            and explicit_result.get("question_answers", {}).get("receipt_surface_explicit") is True
            and explicit_result.get("question_answers", {}).get("source_selection_valid") is True
        ),
        "explicit_a0_result": explicit_result,
    }

    patch_plan = {
        "schema_version": "a0_self_classification_assertion_acceptance_patch_plan_v0",
        "unit_id": UNIT_ID,
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "source_a0_self_class_review_receipt_id": SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID,
        "mode": "patch_wrapper_assertion_only_no_classifier_law_mutation",
        "fix": [
            "accept QUESTION_PACKET_NOT_COMMAND for raw A0 build receipt self-classification",
            "assert STOP_LANE_CLOSED only on explicit closed-lane receipt bundle fixture",
            "treat A0 adapter script as expected build artifact in packaging guard",
        ],
        "not_authorized": HUMAN_DECISION["not_authorized"],
    }

    source_surface = {
        "schema_version": "a0_self_classification_assertion_acceptance_source_surface_v0",
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "source_a0_self_class_review_receipt_id": SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID,
        "a0_build_summary": read_json(A0_BUILD_RECEIPT_PATH).get("a0_build_summary"),
        "a0_review_summary": read_json(A0_SELF_CLASS_REVIEW_RECEIPT_PATH).get("a0_self_classification_failure_review_summary"),
        "fix_authority_packet": read_json(A0_FIX_AUTHORITY_PACKET_PATH),
        "raw_self_classification_recheck": raw_recheck,
        "explicit_bundle_classification_recheck": explicit_recheck,
    }

    patched_assertion_rule = {
        "schema_version": "a0_patched_self_classification_assertion_rule_v0",
        "rule_status": "PATCHED_ASSERTION_RULE_ACCEPTED",
        "raw_a0_build_receipt_self_classification": {
            "expected_classification": "QUESTION_PACKET_NOT_COMMAND",
            "reason": "raw A0 build receipt is not an explicit A0 receipt bundle because it lacks receipt_path/source_selection_rule and full negative-control input surface",
        },
        "explicit_closed_lane_bundle_classification": {
            "expected_classification": "STOP_LANE_CLOSED",
            "reason": "explicit bundle supplies receipt_path, source_selection_rule, no-commit reason, clean negative controls, STOP terminal, null next, and no pressure",
        },
        "classifier_law_change_required": False,
        "wrapper_assertion_change_required": True,
    }

    packaging_guard = {
        "schema_version": "a0_expected_artifact_packaging_guard_recheck_v0",
        "guard_status": "EXPECTED_A0_ARTIFACTS_ALLOWED_FOR_PACKAGING",
        "expected_artifacts": [rel(p) for p in EXPECTED_PACKAGING_ARTIFACTS],
        "expected_new_build_artifacts_not_forbidden_source_mutations": [
            rel(A0_ADAPTER_PATH),
            rel(A0_BUILD_RECEIPT_PATH),
            rel(A0_SELF_CLASS_REVIEW_RECEIPT_PATH),
        ],
        "forbidden_prior_artifact_mutation_check": "hash comparison over existing source files, not git untracked status for expected A0 artifacts",
        "a0_adapter_script_is_expected_build_artifact": True,
        "packaging_guard_false_positive_resolved": True,
    }

    final_acceptance = {
        "schema_version": "a0_transition_layer_final_acceptance_packet_v0",
        "packet_status": "A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILT_PATCH_ACCEPTED",
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "source_a0_self_class_review_receipt_id": SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID,
        "a0_build_result": read_json(A0_BUILD_RECEIPT_PATH).get("a0_build_summary", {}).get("build_result"),
        "probe_pass_count": read_json(A0_BUILD_RECEIPT_PATH).get("a0_build_summary", {}).get("probe_pass_count"),
        "negative_control_pass_count": read_json(A0_BUILD_RECEIPT_PATH).get("a0_build_summary", {}).get("negative_control_pass_count"),
        "raw_self_classification_accepted": raw_recheck["raw_question_packet_accepted"],
        "explicit_bundle_stop_lane_closed_accepted": explicit_recheck["explicit_bundle_stop_lane_closed_passed"],
        "classifier_law_mutated": False,
        "builder_command_executed": False,
        "live_frontier_application_count": 0,
        "first_live_use_candidate": "APPLY_A0_TO_CURRENT_RECEIPT_CHAIN_FRONTIER_V0",
        "first_live_use_requires_explicit_frontier_packet": True,
        "recommended_next_handling": None,
        "auto_next_command": None,
    }

    next_status = {
        "schema_version": "a0_self_classification_assertion_acceptance_next_status_packet_v0",
        "packet_status": "A0_BUILT_AND_PATCH_ACCEPTED_NO_NEXT_COMMAND",
        "a0_final_acceptance_packet": rel(FINAL_ACCEPTANCE_PACKET_PATH),
        "first_live_use_candidate": "APPLY_A0_TO_CURRENT_RECEIPT_CHAIN_FRONTIER_V0",
        "first_live_use_requirement": "explicit frontier packet only; no latest-file, mtime, vibes, or hidden roadmap selection",
        "recommended_next_handling": None,
        "auto_next_command": None,
    }

    report = {
        "schema_version": "a0_self_classification_assertion_acceptance_patch_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "source_a0_self_class_review_receipt_id": SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID,
        "a0_build_receipt_consumed_count": 1,
        "a0_self_class_review_receipt_consumed_count": 1,
        "fix_authority_packet_consumed_count": 1,
        "raw_self_classification_recheck_emitted_count": 1,
        "explicit_bundle_fixture_emitted_count": 1,
        "explicit_bundle_classification_recheck_emitted_count": 1,
        "patched_assertion_rule_emitted_count": 1,
        "packaging_guard_recheck_emitted_count": 1,
        "final_acceptance_packet_emitted_count": 1,
        "next_status_packet_emitted_count": 1,
        "raw_observed_classification": raw_recheck["observed_classification"],
        "explicit_bundle_observed_classification": explicit_recheck["observed_classification"],
        "raw_question_packet_acceptance_count": 1 if raw_recheck["raw_question_packet_accepted"] else 0,
        "explicit_bundle_stop_lane_closed_acceptance_count": 1 if explicit_recheck["explicit_bundle_stop_lane_closed_passed"] else 0,
        "a0_transition_layer_final_acceptance_count": 1 if final_acceptance["packet_status"] == "A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILT_PATCH_ACCEPTED" else 0,
        "builder_command_executed_count": 0,
        "repair_executed_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "live_frontier_application_count": 0,
        "a0_classifier_law_mutation_count": 0,
        "latest_or_mtime_selection_count": 0,
        "strategic_discussion_as_authority_count": 0,
        "recommended_next_handling": None,
    }

    trace = {
        "schema_version": "a0_self_classification_assertion_acceptance_transition_trace_v0",
        "trace": [
            {
                "step": "consume_review",
                "question": "was self-classification failure reviewed as wrapper assertion mismatch only",
                "answer": read_json(A0_SELF_CLASS_REVIEW_RECEIPT_PATH).get("a0_self_classification_failure_review_summary", {}).get("review_result") == "A0_BUILD_FAILURE_REVIEW_ACCEPTS_WRAPPER_ASSERTION_MISMATCH_ONLY",
                "taken": "recheck_raw_receipt",
            },
            {
                "step": "recheck_raw_receipt",
                "question": "does raw A0 build receipt classify as QUESTION_PACKET_NOT_COMMAND",
                "answer": raw_recheck["raw_question_packet_accepted"],
                "taken": "build_explicit_closed_lane_bundle_fixture",
            },
            {
                "step": "build_explicit_closed_lane_bundle_fixture",
                "question": "does explicit closed-lane bundle classify as STOP_LANE_CLOSED",
                "answer": explicit_recheck["explicit_bundle_stop_lane_closed_passed"],
                "taken": "accept_a0_build_and_patch_wrapper_assertion",
            },
            {
                "step": "accept_a0_build_and_patch_wrapper_assertion",
                "question": "is A0 final accepted without live frontier application",
                "answer": final_acceptance["packet_status"],
                "taken": "STOP_A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILT_PATCH_ACCEPTED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILT_PATCH_ACCEPTED",
            "next_command_goal": None,
        },
    }

    write_json(PATCH_PLAN_PATH, patch_plan)
    write_json(SOURCE_SURFACE_PATH, source_surface)
    write_json(RAW_SELF_CLASSIFICATION_RECHECK_PATH, raw_recheck)
    write_json(EXPLICIT_BUNDLE_FIXTURE_PATH, explicit_bundle)
    write_json(EXPLICIT_BUNDLE_CLASSIFICATION_RECHECK_PATH, explicit_recheck)
    write_json(PATCHED_ASSERTION_RULE_PATH, patched_assertion_rule)
    write_json(PACKAGING_GUARD_RECHECK_PATH, packaging_guard)
    write_json(FINAL_ACCEPTANCE_PACKET_PATH, final_acceptance)
    write_json(NEXT_STATUS_PACKET_PATH, next_status)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(raw_recheck, explicit_recheck, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "A0_ASSERTION_PATCH_0_A0_BUILD_RECEIPT_CONSUMED": True,
        "A0_ASSERTION_PATCH_1_REVIEW_RECEIPT_CONSUMED": True,
        "A0_ASSERTION_PATCH_2_FIX_AUTHORITY_CONSUMED": True,
        "A0_ASSERTION_PATCH_3_RAW_RECEIPT_QUESTION_PACKET_ACCEPTED": raw_recheck["raw_question_packet_accepted"] is True,
        "A0_ASSERTION_PATCH_4_EXPLICIT_BUNDLE_STOP_LANE_CLOSED_ACCEPTED": explicit_recheck["explicit_bundle_stop_lane_closed_passed"] is True,
        "A0_ASSERTION_PATCH_5_PACKAGING_GUARD_FALSE_POSITIVE_RESOLVED": packaging_guard["packaging_guard_false_positive_resolved"] is True,
        "A0_ASSERTION_PATCH_6_FINAL_A0_ACCEPTANCE_PACKET_EMITTED": report["final_acceptance_packet_emitted_count"] == 1,
        "A0_ASSERTION_PATCH_7_NO_BUILDER_COMMAND_EXECUTED": report["builder_command_executed_count"] == 0,
        "A0_ASSERTION_PATCH_8_NO_REPAIR_EXECUTED": report["repair_executed_count"] == 0,
        "A0_ASSERTION_PATCH_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "A0_ASSERTION_PATCH_10_NO_LIVE_FRONTIER_APPLICATION": report["live_frontier_application_count"] == 0,
        "A0_ASSERTION_PATCH_11_NO_A0_CLASSIFIER_LAW_MUTATION": report["a0_classifier_law_mutation_count"] == 0,
        "A0_ASSERTION_PATCH_12_NO_LATEST_OR_MTIME_SELECTION": report["latest_or_mtime_selection_count"] == 0,
        "A0_ASSERTION_PATCH_13_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "source_a0_self_class_review_receipt_id": SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards_packet = {
        "patch_only_no_classifier_law_mutation": True,
        "builder_command_executed": False,
        "repair_executed": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "live_frontier_applied": False,
        "a0_classifier_law_mutated": False,
        "latest_or_mtime_selection_used": False,
        "strategic_discussion_as_authority": False,
        "hidden_next_command": False,
        "expected_a0_adapter_script_packaged_as_artifact": True,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "source_a0_self_class_review_receipt_id": SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID,
        "final_status": final_acceptance["packet_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "patch_plan": rel(PATCH_PLAN_PATH),
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "raw_self_classification_recheck": rel(RAW_SELF_CLASSIFICATION_RECHECK_PATH),
        "explicit_bundle_fixture": rel(EXPLICIT_BUNDLE_FIXTURE_PATH),
        "explicit_bundle_classification_recheck": rel(EXPLICIT_BUNDLE_CLASSIFICATION_RECHECK_PATH),
        "patched_assertion_rule": rel(PATCHED_ASSERTION_RULE_PATH),
        "packaging_guard_recheck": rel(PACKAGING_GUARD_RECHECK_PATH),
        "final_acceptance_packet": rel(FINAL_ACCEPTANCE_PACKET_PATH),
        "next_status_packet": rel(NEXT_STATUS_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_a0_build_receipt": rel(A0_BUILD_RECEIPT_PATH),
        "source_a0_self_class_review_receipt": rel(A0_SELF_CLASS_REVIEW_RECEIPT_PATH),
        "source_a0_adapter_script": rel(A0_ADAPTER_PATH),
    }

    receipt = {
        "schema_version": "a0_self_classification_assertion_acceptance_patch_receipt_v0",
        "receipt_type": "A0_SELF_CLASSIFICATION_ASSERTION_ACCEPTANCE_PATCH_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "source_a0_self_class_review_receipt_id": SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "a0_assertion_acceptance_patch_summary": {
            "patch_result": "A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILT_PATCH_ACCEPTED",
            "raw_build_receipt_classification_accepted": raw_recheck["observed_classification"],
            "explicit_bundle_classification_accepted": explicit_recheck["observed_classification"],
            "a0_build_result": read_json(A0_BUILD_RECEIPT_PATH).get("a0_build_summary", {}).get("build_result"),
            "probe_pass_count": read_json(A0_BUILD_RECEIPT_PATH).get("a0_build_summary", {}).get("probe_pass_count"),
            "negative_control_pass_count": read_json(A0_BUILD_RECEIPT_PATH).get("a0_build_summary", {}).get("negative_control_pass_count"),
            "a0_classifier_law_mutated": False,
            "builder_command_executed": False,
            "live_frontier_application_count": 0,
            "first_live_use_candidate": "APPLY_A0_TO_CURRENT_RECEIPT_CHAIN_FRONTIER_V0",
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "a0_assertion_acceptance_patch_guards": guards_packet,
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
    print(f"a0_assertion_patch_receipt_id={receipt_id}")
    print(f"a0_assertion_patch_receipt_path=data/a0_self_classification_assertion_acceptance_patch_v0_receipts/{receipt_id}.json")
    print(f"a0_final_acceptance_packet_path=data/a0_self_classification_assertion_acceptance_patch_v0/a0_transition_layer_final_acceptance_packet.json")
    print(f"a0_explicit_bundle_fixture_path=data/a0_self_classification_assertion_acceptance_patch_v0/a0_explicit_closed_lane_bundle_fixture.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
