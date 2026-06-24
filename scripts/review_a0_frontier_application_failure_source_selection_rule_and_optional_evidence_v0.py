#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_A0_FRONTIER_APPLICATION_FAILURE_SOURCE_SELECTION_RULE_AND_OPTIONAL_EVIDENCE_V0"
TARGET_UNIT_ID = "a0.frontier_application.failure.source_selection_rule_and_optional_evidence.review.v0"

SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID = "c1d0f615"
SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID = "6d14e637"
SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID = "454aa103"
SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID = "52d0ea8d"

OUT_DIR = ROOT / "data" / "a0_current_receipt_chain_frontier_application_failure_review_v0"
RECEIPT_DIR = ROOT / "data" / "a0_current_receipt_chain_frontier_application_failure_review_v0_receipts"

REVIEW_SURFACE_PATH = OUT_DIR / "a0_frontier_application_failure_review_surface.json"
SOURCE_SELECTION_REVIEW_PATH = OUT_DIR / "a0_frontier_source_selection_rule_mismatch_review.json"
OPTIONAL_EVIDENCE_REVIEW_PATH = OUT_DIR / "a0_frontier_optional_evidence_gap_review.json"
SUBSTANTIVE_BEHAVIOR_REVIEW_PATH = OUT_DIR / "a0_frontier_application_substantive_behavior_review.json"
FIX_AUTHORITY_PACKET_PATH = OUT_DIR / "a0_frontier_application_source_selection_fix_authority_packet.json"
REVIEW_DECISION_PATH = OUT_DIR / "a0_frontier_application_failure_review_decision.json"
NEXT_DECISION_PACKET_PATH = OUT_DIR / "a0_frontier_application_failure_review_next_decision_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "a0_frontier_application_failure_review_transition_trace.json"
REPORT_PATH = OUT_DIR / "a0_frontier_application_failure_review_report.json"

A0_FRONTIER_FAILURE_RECEIPT_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0_receipts" / f"{SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID}.json"
A0_FRONTIER_SELECTION_PACKET_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0" / "a0_explicit_frontier_selection_packet.json"
A0_FRONTIER_BUNDLE_MANIFEST_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0" / "a0_frontier_receipt_bundle_manifest.json"
A0_FRONTIER_BUNDLES_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0" / "a0_frontier_explicit_receipt_bundles.json"
A0_FRONTIER_CLASSIFICATIONS_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0" / "a0_frontier_classifications.jsonl"
A0_FRONTIER_ROLLUP_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0" / "a0_frontier_classification_rollup.json"
A0_FRONTIER_DECISION_PACKET_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0" / "a0_frontier_decision_packet.json"
A0_FRONTIER_QUESTION_PACKET_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0" / "a0_frontier_question_packet.json"
A0_FRONTIER_OPERATIONAL_SPEC_CANDIDATE_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0" / "a0_frontier_operational_spec_candidate.json"
A0_FRONTIER_NEXT_STATUS_PACKET_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0" / "a0_frontier_application_next_status_packet.json"
A0_FRONTIER_TRACE_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0" / "a0_frontier_application_transition_trace.json"
A0_FRONTIER_REPORT_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0" / "a0_frontier_application_report.json"

A0_FINAL_ACCEPTANCE_RECEIPT_PATH = ROOT / "data" / "a0_self_classification_assertion_acceptance_patch_v0_receipts" / f"{SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID}.json"
A0_FINAL_ACCEPTANCE_PACKET_PATH = ROOT / "data" / "a0_self_classification_assertion_acceptance_patch_v0" / "a0_transition_layer_final_acceptance_packet.json"
A0_ADAPTER_PATH = ROOT / "scripts" / "a0_receipt_to_builder_transition_layer_v0.py"

R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH = ROOT / "data" / "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0_receipts" / f"{SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID}.json"
R10000_FINAL_STATE_PACKET_PATH = ROOT / "data" / "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0" / "r10000_close_and_freeze_final_accepted_state_packet.json"
R1000_CLOSURE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID}.json"
R1000_CLOSED_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"

SOURCE_FILES = [
    A0_FRONTIER_FAILURE_RECEIPT_PATH,
    A0_FRONTIER_SELECTION_PACKET_PATH,
    A0_FRONTIER_BUNDLE_MANIFEST_PATH,
    A0_FRONTIER_BUNDLES_PATH,
    A0_FRONTIER_CLASSIFICATIONS_PATH,
    A0_FRONTIER_ROLLUP_PATH,
    A0_FRONTIER_DECISION_PACKET_PATH,
    A0_FRONTIER_QUESTION_PACKET_PATH,
    A0_FRONTIER_OPERATIONAL_SPEC_CANDIDATE_PATH,
    A0_FRONTIER_NEXT_STATUS_PACKET_PATH,
    A0_FRONTIER_TRACE_PATH,
    A0_FRONTIER_REPORT_PATH,
    A0_FINAL_ACCEPTANCE_RECEIPT_PATH,
    A0_FINAL_ACCEPTANCE_PACKET_PATH,
    A0_ADAPTER_PATH,
    R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH,
    R10000_FINAL_STATE_PACKET_PATH,
    R1000_CLOSURE_RECEIPT_PATH,
    R1000_CLOSED_HANDOFF_PATH,
]

HUMAN_DECISION = {
    "decision": "REVIEW_A0_FRONTIER_APPLICATION_FAILURE_SOURCE_SELECTION_RULE_AND_OPTIONAL_EVIDENCE",
    "scope": "Review the failed A0 frontier application. Determine whether the failure is caused by the frontier wrapper using a source_selection_rule outside A0's accepted explicit input contract, and whether optional missing frontier evidence was handled safely as question/evidence gap rather than latest/mtime guessing.",
    "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
    "authorized": [
        "consume failed A0 frontier application receipt and artifacts",
        "review source_selection_rule mismatch",
        "review optional evidence warnings and question-packet behavior",
        "preserve A0 classifier law",
        "emit narrow fix authority packet",
        "stop before patching or executing any builder command",
    ],
    "not_authorized": [
        "execute builder command",
        "execute repair",
        "mutate A0 classifier law",
        "mutate source artifacts",
        "mutate prior receipts",
        "apply taxonomy changes",
        "select missing frontier evidence by latest-file guessing",
        "select missing frontier evidence by mtime sorting",
        "run radius-10000 again",
        "run radius above 10000",
        "run unbounded/no-cap harvest",
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

def validate_sources() -> List[str]:
    failures: List[str] = []
    failed = read_json(A0_FRONTIER_FAILURE_RECEIPT_PATH)
    selection = read_json(A0_FRONTIER_SELECTION_PACKET_PATH)
    bundles = read_json(A0_FRONTIER_BUNDLES_PATH)
    rows = read_jsonl(A0_FRONTIER_CLASSIFICATIONS_PATH)
    decision = read_json(A0_FRONTIER_DECISION_PACKET_PATH)
    question = read_json(A0_FRONTIER_QUESTION_PACKET_PATH)
    report = read_json(A0_FRONTIER_REPORT_PATH)
    a0_final = read_json(A0_FINAL_ACCEPTANCE_RECEIPT_PATH)

    if failed.get("receipt_id") != SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID:
        failures.append("frontier_failure_receipt_id_wrong")
    if failed.get("gate") != "FAIL":
        failures.append("frontier_failure_receipt_gate_not_fail")
    if failed.get("unit_id") != "APPLY_A0_TO_CURRENT_RECEIPT_CHAIN_FRONTIER_V0":
        failures.append("frontier_failure_unit_wrong")
    if "r10000_frontier_wrong_classification:QUESTION_PACKET_NOT_COMMAND" not in failed.get("failures", []):
        failures.append("expected_r10000_classification_failure_missing")
    if failed.get("a0_frontier_application_summary", {}).get("builder_command_allowed_count") != 0:
        failures.append("frontier_failure_builder_command_allowed")
    if failed.get("a0_frontier_application_summary", {}).get("question_packet_required") is not True:
        failures.append("frontier_failure_no_question_packet_required")
    if failed.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("frontier_failure_hidden_next")

    if selection.get("selection_rule") != "explicit_human_supplied_frontier_packet":
        failures.append("frontier_selection_rule_not_explicit_human_supplied")
    if selection.get("auto_selected_frontier") is not None:
        failures.append("frontier_auto_selected")

    bundle_list = bundles.get("bundles", [])
    if len(bundle_list) != 3:
        failures.append("frontier_bundle_count_not_3")
    bad_rules = []
    for bundle in bundle_list:
        receipt = bundle.get("receipt_bundle", {})
        rule = receipt.get("source_selection_rule")
        if rule == "explicit_frontier_packet":
            bad_rules.append(bundle.get("frontier_id"))
    if not bad_rules:
        failures.append("source_selection_rule_mismatch_not_observed")

    r10000_row = next((r for r in rows if r.get("frontier_id") == "frontier_r10000_closed_frozen"), None)
    if not r10000_row:
        failures.append("r10000_frontier_row_missing")
    else:
        qa = r10000_row.get("a0_result", {}).get("question_answers", {})
        if r10000_row.get("a0_classification") != "QUESTION_PACKET_NOT_COMMAND":
            failures.append("r10000_row_not_question_packet")
        if qa.get("source_selection_valid") is not False:
            failures.append("r10000_source_selection_not_invalid")
        if r10000_row.get("builder_command_allowed") is not False:
            failures.append("r10000_builder_allowed")

    if decision.get("decision_status") != "QUESTION_PACKET_NOT_COMMAND_FOR_FRONTIER_EVIDENCE_OR_SELECTION_GAP":
        failures.append("decision_status_wrong")
    if decision.get("builder_command_allowed") is not False:
        failures.append("decision_builder_allowed")
    if decision.get("auto_next_command") is not None:
        failures.append("decision_auto_next")

    if question.get("packet_status") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append("question_packet_status_wrong")
    if question.get("auto_next_command") is not None:
        failures.append("question_auto_next")

    for key in [
        "builder_command_executed_count",
        "repair_executed_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
        "latest_or_mtime_selection_count",
        "strategic_discussion_as_authority_count",
        "radius_10000_rerun_count",
        "radius_above_10000_run_count",
        "unbounded_or_no_cap_run_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    if a0_final.get("gate") != "PASS":
        failures.append("a0_final_not_pass")
    if a0_final.get("a0_assertion_acceptance_patch_summary", {}).get("patch_result") != "A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILT_PATCH_ACCEPTED":
        failures.append("a0_final_not_accepted")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")

    return failures

def build_reviews() -> Dict[str, Dict[str, Any]]:
    failed = read_json(A0_FRONTIER_FAILURE_RECEIPT_PATH)
    selection = read_json(A0_FRONTIER_SELECTION_PACKET_PATH)
    bundles = read_json(A0_FRONTIER_BUNDLES_PATH)
    rows = read_jsonl(A0_FRONTIER_CLASSIFICATIONS_PATH)
    question = read_json(A0_FRONTIER_QUESTION_PACKET_PATH)
    report = read_json(A0_FRONTIER_REPORT_PATH)

    bad_rule_frontiers = []
    for bundle in bundles.get("bundles", []):
        rule = bundle.get("receipt_bundle", {}).get("source_selection_rule")
        if rule == "explicit_frontier_packet":
            bad_rule_frontiers.append(bundle.get("frontier_id"))

    r10000_row = next((r for r in rows if r.get("frontier_id") == "frontier_r10000_closed_frozen"), {})
    r1000_row = next((r for r in rows if r.get("frontier_id") == "frontier_r1000_pressure_queue_closed"), {})
    candidate_row = next((r for r in rows if r.get("frontier_id") == "frontier_candidate_missing_object_layer_followup"), {})

    source_selection_review = {
        "schema_version": "a0_frontier_source_selection_rule_mismatch_review_v0",
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "review_classification": "A0_FRONTIER_WRAPPER_USED_UNACCEPTED_SOURCE_SELECTION_RULE",
        "mismatch_only": True,
        "bad_rule": "explicit_frontier_packet",
        "bad_rule_frontiers": bad_rule_frontiers,
        "a0_allowed_rules_observed_from_design": [
            "explicit_human_supplied",
            "explicit_receipt_id",
            "explicit_receipt_path",
            "explicit_bundle_manifest",
        ],
        "recommended_fix": "use explicit_bundle_manifest for frontier receipt bundles; do not widen A0 source-selection enum in this patch",
        "r10000_observed_classification": r10000_row.get("a0_classification"),
        "r10000_source_selection_valid": r10000_row.get("a0_result", {}).get("question_answers", {}).get("source_selection_valid"),
        "r10000_expected_after_fix": "CLOSE_AND_FREEZE_ACCEPTANCE",
    }

    optional_missing_questions = question.get("questions", [])
    optional_evidence_review = {
        "schema_version": "a0_frontier_optional_evidence_gap_review_v0",
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "review_classification": "OPTIONAL_FRONTIER_EVIDENCE_MISSING_HANDLED_AS_QUESTION_PACKET_NOT_COMMAND",
        "optional_evidence_missing_handled_safely": True,
        "question_count": len(optional_missing_questions),
        "question_frontiers": [q.get("frontier_id") for q in optional_missing_questions],
        "latest_or_mtime_selection_count": report.get("latest_or_mtime_selection_count"),
        "missing_optional_evidence_treated_as_null_value": False,
        "recommended_fix_scope": [
            "do not search by latest/mtime",
            "preserve question packet behavior for absent optional receipt evidence",
            "allow source-selection-rule patch to expose closed frontiers correctly",
        ],
    }

    substantive_behavior_review = {
        "schema_version": "a0_frontier_application_substantive_behavior_review_v0",
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "substantive_behavior_safe": (
            failed.get("a0_frontier_application_summary", {}).get("builder_command_allowed_count") == 0
            and report.get("builder_command_executed_count") == 0
            and report.get("repair_executed_count") == 0
            and report.get("hidden_next_command_count") == 0
            and report.get("source_mutation_count") == 0
            and report.get("latest_or_mtime_selection_count") == 0
        ),
        "frontier_decision_status": failed.get("a0_frontier_application_summary", {}).get("decision_status"),
        "r10000_classification": r10000_row.get("a0_classification"),
        "r1000_classification": r1000_row.get("a0_classification"),
        "candidate_missing_object_classification": candidate_row.get("a0_classification"),
        "builder_command_allowed_count": failed.get("a0_frontier_application_summary", {}).get("builder_command_allowed_count"),
        "operational_spec_candidate_allowed_count": failed.get("a0_frontier_application_summary", {}).get("operational_spec_candidate_allowed_count"),
        "candidate_missing_object_proposal_allowed_count": failed.get("a0_frontier_application_summary", {}).get("candidate_missing_object_proposal_allowed_count"),
        "question_packet_required": failed.get("a0_frontier_application_summary", {}).get("question_packet_required"),
        "true_a0_classifier_failure": False,
        "true_a0_frontier_application_semantic_failure": False,
    }

    return {
        "source_selection_review": source_selection_review,
        "optional_evidence_review": optional_evidence_review,
        "substantive_behavior_review": substantive_behavior_review,
    }

def validate_outputs(source_selection_review: Dict[str, Any], optional_evidence_review: Dict[str, Any], substantive_behavior_review: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if source_selection_review.get("mismatch_only") is not True:
        failures.append("source_selection_mismatch_only_not_true")
    if source_selection_review.get("recommended_fix") != "use explicit_bundle_manifest for frontier receipt bundles; do not widen A0 source-selection enum in this patch":
        failures.append("source_selection_recommended_fix_wrong")
    if optional_evidence_review.get("optional_evidence_missing_handled_safely") is not True:
        failures.append("optional_evidence_not_handled_safely")
    if optional_evidence_review.get("latest_or_mtime_selection_count") != 0:
        failures.append("optional_evidence_latest_or_mtime_used")
    if substantive_behavior_review.get("substantive_behavior_safe") is not True:
        failures.append("substantive_behavior_not_safe")
    if substantive_behavior_review.get("true_a0_classifier_failure") is not False:
        failures.append("marked_true_a0_classifier_failure")
    if substantive_behavior_review.get("true_a0_frontier_application_semantic_failure") is not False:
        failures.append("marked_true_frontier_semantic_failure")

    for key in [
        "builder_command_executed_count",
        "repair_executed_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
        "latest_or_mtime_selection_count",
        "strategic_discussion_as_authority_count",
        "radius_10000_rerun_count",
        "radius_above_10000_run_count",
        "unbounded_or_no_cap_run_count",
        "a0_classifier_law_mutation_count",
        "a0_source_selection_enum_widening_count",
        "live_frontier_patch_executed_count",
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
        "a0_frontier_failure_receipt_consumed_count",
        "frontier_failure_artifacts_consumed_count",
        "source_selection_review_emitted_count",
        "optional_evidence_review_emitted_count",
        "substantive_behavior_review_emitted_count",
        "fix_authority_packet_emitted_count",
        "review_decision_emitted_count",
        "next_decision_packet_emitted_count",
        "source_selection_mismatch_only_count",
        "optional_evidence_handled_safely_count",
        "substantive_behavior_safe_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    for key in [
        "builder_command_executed_count",
        "repair_executed_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
        "latest_or_mtime_selection_count",
        "strategic_discussion_as_authority_count",
        "radius_10000_rerun_count",
        "radius_above_10000_run_count",
        "unbounded_or_no_cap_run_count",
        "a0_classifier_law_mutation_count",
        "a0_source_selection_enum_widening_count",
        "live_frontier_patch_executed_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_A0_FRONTIER_FAILURE_REVIEW_COMPLETE_SOURCE_SELECTION_PATCH_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    reviews = build_reviews()
    source_selection_review = reviews["source_selection_review"]
    optional_evidence_review = reviews["optional_evidence_review"]
    substantive_behavior_review = reviews["substantive_behavior_review"]

    review_surface = {
        "schema_version": "a0_frontier_application_failure_review_surface_v0",
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "failed_unit": "APPLY_A0_TO_CURRENT_RECEIPT_CHAIN_FRONTIER_V0",
        "failed_gate": read_json(A0_FRONTIER_FAILURE_RECEIPT_PATH).get("gate"),
        "failure_class": "SOURCE_SELECTION_RULE_CONTRACT_MISMATCH_PLUS_OPTIONAL_EVIDENCE_GAP",
        "direct_failures": read_json(A0_FRONTIER_FAILURE_RECEIPT_PATH).get("failures"),
        "frontier_summary": read_json(A0_FRONTIER_FAILURE_RECEIPT_PATH).get("a0_frontier_application_summary"),
    }

    fix_authority = {
        "schema_version": "a0_frontier_application_source_selection_fix_authority_packet_v0",
        "packet_status": "A0_FRONTIER_SOURCE_SELECTION_RULE_REVIEWED_NARROW_PATCH_AUTHORIZED",
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "authorized_next_unit": "PATCH_A0_FRONTIER_APPLICATION_SOURCE_SELECTION_RULE_TO_EXPLICIT_BUNDLE_MANIFEST_V0",
        "required_fix_shape": [
            "change frontier receipt bundle source_selection_rule from explicit_frontier_packet to explicit_bundle_manifest",
            "do not widen A0 source-selection enum",
            "do not mutate A0 classifier law",
            "preserve optional evidence gap as QUESTION_PACKET_NOT_COMMAND unless explicit receipt path is supplied",
            "prove R10000 frontier classifies as CLOSE_AND_FREEZE_ACCEPTANCE after source-selection fix",
            "stop with next_command_goal null",
        ],
        "a0_classifier_law_mutation_authorized": False,
        "a0_source_selection_enum_widening_authorized": False,
        "builder_command_execution_authorized_now": False,
        "live_frontier_execution_authorized_now": False,
        "recommended_next_handling": "PATCH_A0_FRONTIER_APPLICATION_SOURCE_SELECTION_RULE_TO_EXPLICIT_BUNDLE_MANIFEST_V0",
    }

    decision = {
        "schema_version": "a0_frontier_application_failure_review_decision_v0",
        "decision_status": "A0_FRONTIER_FAILURE_REVIEW_ACCEPTS_SOURCE_SELECTION_RULE_MISMATCH_ONLY_FOR_CLOSED_FRONTIERS",
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "source_selection_mismatch_only": source_selection_review["mismatch_only"],
        "optional_evidence_gap_handled_safely": optional_evidence_review["optional_evidence_missing_handled_safely"],
        "substantive_behavior_safe": substantive_behavior_review["substantive_behavior_safe"],
        "true_a0_classifier_failure": False,
        "true_semantic_frontier_failure": False,
        "review_only_no_patch": True,
        "recommended_next_handling": fix_authority["recommended_next_handling"],
    }

    next_decision = {
        "schema_version": "a0_frontier_application_failure_review_next_decision_packet_v0",
        "packet_status": "A0_FRONTIER_FAILURE_REVIEW_COMPLETE_SOURCE_SELECTION_PATCH_READY",
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "safe_next_choices": [
            "patch source_selection_rule to explicit_bundle_manifest",
            "do not widen A0 allowed source-selection enum",
            "do not use latest/mtime to resolve optional evidence",
            "do not execute builder command",
        ],
        "recommended_next_handling": fix_authority["recommended_next_handling"],
        "auto_next_command": None,
    }

    report = {
        "schema_version": "a0_frontier_application_failure_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "a0_frontier_failure_receipt_consumed_count": 1,
        "frontier_failure_artifacts_consumed_count": 1,
        "source_selection_review_emitted_count": 1,
        "optional_evidence_review_emitted_count": 1,
        "substantive_behavior_review_emitted_count": 1,
        "fix_authority_packet_emitted_count": 1,
        "review_decision_emitted_count": 1,
        "next_decision_packet_emitted_count": 1,
        "source_selection_mismatch_only_count": 1 if source_selection_review["mismatch_only"] else 0,
        "optional_evidence_handled_safely_count": 1 if optional_evidence_review["optional_evidence_missing_handled_safely"] else 0,
        "substantive_behavior_safe_count": 1 if substantive_behavior_review["substantive_behavior_safe"] else 0,
        "observed_bad_source_selection_rule": source_selection_review["bad_rule"],
        "bad_rule_frontier_count": len(source_selection_review["bad_rule_frontiers"]),
        "r10000_observed_classification": source_selection_review["r10000_observed_classification"],
        "r10000_expected_after_fix": source_selection_review["r10000_expected_after_fix"],
        "builder_command_executed_count": 0,
        "repair_executed_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "latest_or_mtime_selection_count": 0,
        "strategic_discussion_as_authority_count": 0,
        "radius_10000_rerun_count": 0,
        "radius_above_10000_run_count": 0,
        "unbounded_or_no_cap_run_count": 0,
        "a0_classifier_law_mutation_count": 0,
        "a0_source_selection_enum_widening_count": 0,
        "live_frontier_patch_executed_count": 0,
        "recommended_next_handling": fix_authority["recommended_next_handling"],
    }

    trace = {
        "schema_version": "a0_frontier_application_failure_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_failed_frontier_application",
                "question": "did application fail on R10000 close/freeze expectation",
                "answer": "r10000_frontier_wrong_classification:QUESTION_PACKET_NOT_COMMAND" in read_json(A0_FRONTIER_FAILURE_RECEIPT_PATH).get("failures", []),
                "taken": "review_source_selection_rule",
            },
            {
                "step": "review_source_selection_rule",
                "question": "was unaccepted source_selection_rule observed",
                "answer": source_selection_review["bad_rule_frontiers"],
                "taken": "review_optional_evidence",
            },
            {
                "step": "review_optional_evidence",
                "question": "was missing optional evidence handled safely",
                "answer": optional_evidence_review["optional_evidence_missing_handled_safely"],
                "taken": "review_substantive_behavior",
            },
            {
                "step": "review_substantive_behavior",
                "question": "did any builder command execute",
                "answer": substantive_behavior_review["builder_command_allowed_count"] if "builder_command_allowed_count" in substantive_behavior_review else 0,
                "taken": "emit_fix_authority",
            },
            {
                "step": "emit_fix_authority",
                "question": "patch now",
                "answer": False,
                "taken": "STOP_A0_FRONTIER_FAILURE_REVIEW_COMPLETE_SOURCE_SELECTION_PATCH_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_A0_FRONTIER_FAILURE_REVIEW_COMPLETE_SOURCE_SELECTION_PATCH_REQUIRED",
            "next_command_goal": None,
        },
    }

    write_json(REVIEW_SURFACE_PATH, review_surface)
    write_json(SOURCE_SELECTION_REVIEW_PATH, source_selection_review)
    write_json(OPTIONAL_EVIDENCE_REVIEW_PATH, optional_evidence_review)
    write_json(SUBSTANTIVE_BEHAVIOR_REVIEW_PATH, substantive_behavior_review)
    write_json(FIX_AUTHORITY_PACKET_PATH, fix_authority)
    write_json(REVIEW_DECISION_PATH, decision)
    write_json(NEXT_DECISION_PACKET_PATH, next_decision)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(source_selection_review, optional_evidence_review, substantive_behavior_review, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "A0_FRONTIER_FAIL_REVIEW_0_FAILURE_RECEIPT_CONSUMED": True,
        "A0_FRONTIER_FAIL_REVIEW_1_SOURCE_SELECTION_MISMATCH_CONFIRMED": source_selection_review["mismatch_only"] is True,
        "A0_FRONTIER_FAIL_REVIEW_2_RECOMMENDS_BUNDLE_MANIFEST_NOT_ENUM_WIDENING": source_selection_review["recommended_fix"] == "use explicit_bundle_manifest for frontier receipt bundles; do not widen A0 source-selection enum in this patch",
        "A0_FRONTIER_FAIL_REVIEW_3_OPTIONAL_EVIDENCE_HANDLED_SAFELY": optional_evidence_review["optional_evidence_missing_handled_safely"] is True,
        "A0_FRONTIER_FAIL_REVIEW_4_SUBSTANTIVE_BEHAVIOR_SAFE": substantive_behavior_review["substantive_behavior_safe"] is True,
        "A0_FRONTIER_FAIL_REVIEW_5_FIX_AUTHORITY_PACKET_EMITTED": report["fix_authority_packet_emitted_count"] == 1,
        "A0_FRONTIER_FAIL_REVIEW_6_NO_BUILDER_COMMAND_EXECUTED": report["builder_command_executed_count"] == 0,
        "A0_FRONTIER_FAIL_REVIEW_7_NO_REPAIR_EXECUTED": report["repair_executed_count"] == 0,
        "A0_FRONTIER_FAIL_REVIEW_8_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "A0_FRONTIER_FAIL_REVIEW_9_NO_A0_CLASSIFIER_LAW_MUTATION": report["a0_classifier_law_mutation_count"] == 0,
        "A0_FRONTIER_FAIL_REVIEW_10_NO_ENUM_WIDENING": report["a0_source_selection_enum_widening_count"] == 0,
        "A0_FRONTIER_FAIL_REVIEW_11_NO_LATEST_OR_MTIME_SELECTION": report["latest_or_mtime_selection_count"] == 0,
        "A0_FRONTIER_FAIL_REVIEW_12_NO_RADIUS_RERUN_OR_UNBOUNDED": report["radius_10000_rerun_count"] == 0 and report["radius_above_10000_run_count"] == 0 and report["unbounded_or_no_cap_run_count"] == 0,
        "A0_FRONTIER_FAIL_REVIEW_13_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "source_r10000_final_close_freeze_receipt_id": SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID,
        "source_r1000_pressure_queue_closure_receipt_id": SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards_packet = {
        "review_only_no_patch": True,
        "builder_command_executed": False,
        "repair_executed": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "a0_classifier_law_mutated": False,
        "a0_source_selection_enum_widened": False,
        "latest_or_mtime_selection_used": False,
        "radius_10000_rerun": False,
        "radius_above_10000_run": False,
        "unbounded_or_no_cap_run": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "classification": decision["decision_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "review_surface": rel(REVIEW_SURFACE_PATH),
        "source_selection_review": rel(SOURCE_SELECTION_REVIEW_PATH),
        "optional_evidence_review": rel(OPTIONAL_EVIDENCE_REVIEW_PATH),
        "substantive_behavior_review": rel(SUBSTANTIVE_BEHAVIOR_REVIEW_PATH),
        "fix_authority_packet": rel(FIX_AUTHORITY_PACKET_PATH),
        "review_decision": rel(REVIEW_DECISION_PATH),
        "next_decision_packet": rel(NEXT_DECISION_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_a0_frontier_failure_receipt": rel(A0_FRONTIER_FAILURE_RECEIPT_PATH),
        "source_a0_frontier_classifications": rel(A0_FRONTIER_CLASSIFICATIONS_PATH),
        "source_a0_frontier_question_packet": rel(A0_FRONTIER_QUESTION_PACKET_PATH),
    }

    receipt = {
        "schema_version": "a0_frontier_application_failure_review_receipt_v0",
        "receipt_type": "A0_FRONTIER_APPLICATION_FAILURE_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "source_r10000_final_close_freeze_receipt_id": SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID,
        "source_r1000_pressure_queue_closure_receipt_id": SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "a0_frontier_failure_review_summary": {
            "review_result": decision["decision_status"],
            "failure_class": review_surface["failure_class"],
            "source_selection_review_classification": source_selection_review["review_classification"],
            "observed_bad_source_selection_rule": source_selection_review["bad_rule"],
            "recommended_fix": source_selection_review["recommended_fix"],
            "optional_evidence_review_classification": optional_evidence_review["review_classification"],
            "optional_evidence_handled_safely": optional_evidence_review["optional_evidence_missing_handled_safely"],
            "substantive_behavior_safe": substantive_behavior_review["substantive_behavior_safe"],
            "true_a0_classifier_failure": decision["true_a0_classifier_failure"],
            "true_semantic_frontier_failure": decision["true_semantic_frontier_failure"],
            "review_only_no_patch": True,
            "recommended_next_handling": fix_authority["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "a0_frontier_failure_review_guards": guards_packet,
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
    print(f"a0_frontier_failure_review_receipt_id={receipt_id}")
    print(f"a0_frontier_failure_review_receipt_path=data/a0_current_receipt_chain_frontier_application_failure_review_v0_receipts/{receipt_id}.json")
    print(f"fix_authority_packet_path=data/a0_current_receipt_chain_frontier_application_failure_review_v0/a0_frontier_application_source_selection_fix_authority_packet.json")
    print(f"next_decision_packet_path=data/a0_current_receipt_chain_frontier_application_failure_review_v0/a0_frontier_application_failure_review_next_decision_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
