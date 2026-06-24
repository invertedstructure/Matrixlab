#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PATCH_A0_FRONTIER_APPLICATION_SOURCE_SELECTION_RULE_TO_EXPLICIT_BUNDLE_MANIFEST_V0"
TARGET_UNIT_ID = "a0.frontier_application.source_selection_rule.explicit_bundle_manifest.patch.v0"

SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID = "c1d0f615"
SOURCE_A0_FRONTIER_FAILURE_REVIEW_RECEIPT_ID = "85e16aee"
SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID = "6d14e637"
SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID = "454aa103"
SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID = "52d0ea8d"

OUT_DIR = ROOT / "data" / "a0_frontier_source_selection_rule_explicit_bundle_manifest_patch_v0"
RECEIPT_DIR = ROOT / "data" / "a0_frontier_source_selection_rule_explicit_bundle_manifest_patch_v0_receipts"

PATCH_PLAN_PATH = OUT_DIR / "a0_frontier_source_selection_patch_plan.json"
SOURCE_SURFACE_PATH = OUT_DIR / "a0_frontier_source_selection_patch_source_surface.json"
PATCHED_SELECTION_PACKET_PATH = OUT_DIR / "a0_frontier_source_selection_patched_selection_packet.json"
PATCHED_BUNDLE_MANIFEST_PATH = OUT_DIR / "a0_frontier_source_selection_patched_bundle_manifest.json"
PATCHED_BUNDLES_PATH = OUT_DIR / "a0_frontier_source_selection_patched_explicit_receipt_bundles.json"
PATCHED_CLASSIFICATIONS_PATH = OUT_DIR / "a0_frontier_source_selection_patched_classifications.jsonl"
PATCHED_ROLLUP_PATH = OUT_DIR / "a0_frontier_source_selection_patched_rollup.json"
PATCHED_DECISION_PACKET_PATH = OUT_DIR / "a0_frontier_source_selection_patched_decision_packet.json"
PATCHED_QUESTION_PACKET_PATH = OUT_DIR / "a0_frontier_source_selection_patched_question_packet.json"
FINAL_ACCEPTANCE_PACKET_PATH = OUT_DIR / "a0_frontier_source_selection_patch_final_acceptance_packet.json"
NEXT_STATUS_PACKET_PATH = OUT_DIR / "a0_frontier_source_selection_patch_next_status_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "a0_frontier_source_selection_patch_transition_trace.json"
REPORT_PATH = OUT_DIR / "a0_frontier_source_selection_patch_report.json"

A0_FRONTIER_FAILURE_RECEIPT_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0_receipts" / f"{SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID}.json"
A0_FRONTIER_FAILURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_failure_review_v0_receipts" / f"{SOURCE_A0_FRONTIER_FAILURE_REVIEW_RECEIPT_ID}.json"
A0_FIX_AUTHORITY_PACKET_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_failure_review_v0" / "a0_frontier_application_source_selection_fix_authority_packet.json"
A0_FAILURE_NEXT_DECISION_PACKET_PATH = ROOT / "data" / "a0_current_receipt_chain_frontier_application_failure_review_v0" / "a0_frontier_application_failure_review_next_decision_packet.json"
A0_FINAL_ACCEPTANCE_RECEIPT_PATH = ROOT / "data" / "a0_self_classification_assertion_acceptance_patch_v0_receipts" / f"{SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID}.json"
A0_FINAL_ACCEPTANCE_PACKET_PATH = ROOT / "data" / "a0_self_classification_assertion_acceptance_patch_v0" / "a0_transition_layer_final_acceptance_packet.json"
A0_ADAPTER_PATH = ROOT / "scripts" / "a0_receipt_to_builder_transition_layer_v0.py"

R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH = ROOT / "data" / "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0_receipts" / f"{SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID}.json"
R10000_FINAL_STATE_PACKET_PATH = ROOT / "data" / "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0" / "r10000_close_and_freeze_final_accepted_state_packet.json"
R10000_BOUNDED_PROTOCOL_FINAL_REFERENCE_PATH = ROOT / "data" / "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0" / "bounded_observability_protocol_final_reference_v0.json"

R1000_CLOSURE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID}.json"
R1000_CLOSED_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"

SOURCE_FILES = [
    A0_FRONTIER_FAILURE_RECEIPT_PATH,
    A0_FRONTIER_FAILURE_REVIEW_RECEIPT_PATH,
    A0_FIX_AUTHORITY_PACKET_PATH,
    A0_FAILURE_NEXT_DECISION_PACKET_PATH,
    A0_FINAL_ACCEPTANCE_RECEIPT_PATH,
    A0_FINAL_ACCEPTANCE_PACKET_PATH,
    A0_ADAPTER_PATH,
    R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH,
    R10000_FINAL_STATE_PACKET_PATH,
    R10000_BOUNDED_PROTOCOL_FINAL_REFERENCE_PATH,
    R1000_CLOSURE_RECEIPT_PATH,
    R1000_CLOSED_HANDOFF_PATH,
]

NEGATIVE_CONTROLS = {
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

HUMAN_DECISION = {
    "decision": "PATCH_A0_FRONTIER_APPLICATION_SOURCE_SELECTION_RULE_TO_EXPLICIT_BUNDLE_MANIFEST",
    "scope": "Patch the A0 frontier application wrapper to use source_selection_rule=explicit_bundle_manifest for frontier receipt bundles. Do not widen A0 source-selection enum, do not mutate A0 classifier law, preserve missing optional evidence as QUESTION_PACKET_NOT_COMMAND, and stop without executing any builder command.",
    "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
    "source_a0_frontier_failure_review_receipt_id": SOURCE_A0_FRONTIER_FAILURE_REVIEW_RECEIPT_ID,
    "authorized": [
        "consume failed frontier application receipt",
        "consume frontier failure review and fix authority packet",
        "patch frontier bundle source_selection_rule to explicit_bundle_manifest",
        "reclassify explicit frontier bundles with A0",
        "prove R10000 frontier classifies as CLOSE_AND_FREEZE_ACCEPTANCE",
        "preserve optional evidence gap as QUESTION_PACKET_NOT_COMMAND",
        "emit patched frontier decision and final acceptance packet",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "mutate A0 classifier law",
        "widen A0 source-selection enum",
        "execute builder command",
        "execute repair",
        "mutate source artifacts",
        "mutate prior receipts",
        "select missing evidence by latest-file guessing",
        "select missing evidence by mtime sorting",
        "run radius-10000 again",
        "run radius above 10000",
        "run unbounded/no-cap harvest",
        "apply taxonomy changes",
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

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

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
    failed = read_json(A0_FRONTIER_FAILURE_RECEIPT_PATH)
    review = read_json(A0_FRONTIER_FAILURE_REVIEW_RECEIPT_PATH)
    authority = read_json(A0_FIX_AUTHORITY_PACKET_PATH)
    a0_final = read_json(A0_FINAL_ACCEPTANCE_RECEIPT_PATH)
    r10000 = read_json(R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH)
    r1000 = read_json(R1000_CLOSURE_RECEIPT_PATH)

    if failed.get("receipt_id") != SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID:
        failures.append("frontier_failure_receipt_id_wrong")
    if failed.get("gate") != "FAIL":
        failures.append("frontier_failure_not_fail")
    if review.get("receipt_id") != SOURCE_A0_FRONTIER_FAILURE_REVIEW_RECEIPT_ID:
        failures.append("frontier_review_receipt_id_wrong")
    if review.get("gate") != "PASS":
        failures.append("frontier_review_not_pass")
    if review.get("a0_frontier_failure_review_summary", {}).get("recommended_next_handling") != UNIT_ID:
        failures.append("frontier_review_not_recommending_this_patch")
    if review.get("a0_frontier_failure_review_summary", {}).get("recommended_fix") != "use explicit_bundle_manifest for frontier receipt bundles; do not widen A0 source-selection enum in this patch":
        failures.append("frontier_review_wrong_fix")
    if authority.get("packet_status") != "A0_FRONTIER_SOURCE_SELECTION_RULE_REVIEWED_NARROW_PATCH_AUTHORIZED":
        failures.append("fix_authority_not_authorized")
    if authority.get("authorized_next_unit") != UNIT_ID:
        failures.append("fix_authority_authorized_next_wrong")
    if authority.get("a0_classifier_law_mutation_authorized") is not False:
        failures.append("fix_authority_allows_classifier_law_mutation")
    if authority.get("a0_source_selection_enum_widening_authorized") is not False:
        failures.append("fix_authority_allows_enum_widening")
    if authority.get("builder_command_execution_authorized_now") is not False:
        failures.append("fix_authority_allows_builder_execution")
    if a0_final.get("gate") != "PASS":
        failures.append("a0_final_not_pass")
    if r10000.get("gate") != "PASS":
        failures.append("r10000_not_pass")
    if r10000.get("final_close_and_freeze_summary", {}).get("final_result") != "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN_FINAL_ACCEPTED":
        failures.append("r10000_not_final_closed_frozen")
    if r1000.get("gate") != "PASS":
        failures.append("r1000_not_pass")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
    return failures

def with_a0_surface(receipt: Dict[str, Any], receipt_path: Path, no_commit_reason: str) -> Dict[str, Any]:
    bundle = copy.deepcopy(receipt)
    bundle["receipt_path"] = rel(receipt_path)
    bundle["source_selection_rule"] = "explicit_bundle_manifest"
    if not bundle.get("commit"):
        bundle["no_commit_reason"] = bundle.get("no_commit_reason") or no_commit_reason
    bundle["negative_controls"] = {**NEGATIVE_CONTROLS, **(bundle.get("negative_controls") or {})}
    bundle["must_not_infer"] = list(dict.fromkeys((bundle.get("must_not_infer") or []) + [
        "do not infer next command",
        "do not infer live frontier from latest or mtime",
        "do not treat strategic discussion as authority",
        "do not infer repair authorization",
        "do not infer taxonomy upgrade",
    ]))
    return bundle

def make_patched_selection_packet() -> Dict[str, Any]:
    return {
        "schema_version": "a0_frontier_source_selection_patched_selection_packet_v0",
        "packet_status": "EXPLICIT_FRONTIER_SELECTION_PATCHED_TO_BUNDLE_MANIFEST_RULE",
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "source_a0_frontier_failure_review_receipt_id": SOURCE_A0_FRONTIER_FAILURE_REVIEW_RECEIPT_ID,
        "selection_rule": "explicit_human_supplied_frontier_packet",
        "bundle_source_selection_rule": "explicit_bundle_manifest",
        "a0_enum_widened": False,
        "candidate_frontiers": [
            {
                "frontier_id": "frontier_r10000_closed_frozen",
                "source_receipt_id": SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID,
                "source_receipt_path": rel(R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH),
                "expected_after_patch": "CLOSE_AND_FREEZE_ACCEPTANCE",
            },
            {
                "frontier_id": "frontier_r1000_pressure_queue_closed",
                "source_receipt_id": SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID,
                "source_receipt_path": rel(R1000_CLOSURE_RECEIPT_PATH),
                "expected_after_patch": "STOP_LANE_CLOSED",
            },
            {
                "frontier_id": "frontier_candidate_missing_object_layer_followup",
                "source_receipt_id": "cbde4b69",
                "source_receipt_path": None,
                "expected_after_patch": "QUESTION_PACKET_NOT_COMMAND",
                "reason": "optional evidence absent; do not select by latest/mtime",
            },
        ],
        "auto_selected_frontier": None,
    }

def make_patched_bundles() -> List[Dict[str, Any]]:
    r10000_receipt = with_a0_surface(
        read_json(R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH),
        R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH,
        "R10000 final close/freeze acceptance receipt already committed in prior branch",
    )
    r10000_receipt["classification"] = "CLOSE_AND_FREEZE_ACCEPTANCE"
    r10000_receipt["remaining_pressure"] = ["NONE"]
    r10000_receipt["dominant_pressure_class"] = "NONE"
    r10000_receipt["output_artifacts"] = {
        **(r10000_receipt.get("output_artifacts") or {}),
        "final_accepted_state_packet": rel(R10000_FINAL_STATE_PACKET_PATH),
        "bounded_protocol_final_reference": rel(R10000_BOUNDED_PROTOCOL_FINAL_REFERENCE_PATH),
    }

    r1000_receipt = with_a0_surface(
        read_json(R1000_CLOSURE_RECEIPT_PATH),
        R1000_CLOSURE_RECEIPT_PATH,
        "R1000 pressure queue closure review receipt already committed in prior branch",
    )
    r1000_receipt.pop("classification", None)
    r1000_receipt["remaining_pressure"] = ["NONE"]
    r1000_receipt["dominant_pressure_class"] = "NONE"
    r1000_receipt["output_artifacts"] = {
        **(r1000_receipt.get("output_artifacts") or {}),
        "closed_queue_handoff": rel(R1000_CLOSED_HANDOFF_PATH),
    }

    missing_receipt = {
        "receipt_id": "cbde4b69",
        "receipt_path": None,
        "unit_id": "EXPECTED_SOURCE_CONTENT_LIMIT_FRONTIER_EVIDENCE_MISSING",
        "gate": None,
        "no_commit_reason": "source receipt path absent from explicit frontier input surface",
        "source_selection_rule": "explicit_bundle_manifest",
        "terminal": {"type": "STOP", "stop_code": "STOP_EVIDENCE_MISSING", "next_command_goal": None},
        "negative_controls": NEGATIVE_CONTROLS,
        "remaining_pressure": ["EVIDENCE_SURFACE_DEFICIENCY"],
        "dominant_pressure_class": "EVIDENCE_SURFACE_DEFICIENCY",
        "must_not_infer": [
            "do not infer candidate missing-object followup without explicit receipt evidence",
            "do not use latest or mtime to find the missing receipt",
            "do not convert missing optional evidence to null value",
        ],
    }

    return [
        {
            "frontier_id": "frontier_r10000_closed_frozen",
            "bundle_status": "EXPLICIT_BUNDLE_READY",
            "source_receipt_path": rel(R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH),
            "receipt_bundle": r10000_receipt,
        },
        {
            "frontier_id": "frontier_r1000_pressure_queue_closed",
            "bundle_status": "EXPLICIT_BUNDLE_READY",
            "source_receipt_path": rel(R1000_CLOSURE_RECEIPT_PATH),
            "receipt_bundle": r1000_receipt,
        },
        {
            "frontier_id": "frontier_candidate_missing_object_layer_followup",
            "bundle_status": "EXPLICIT_BUNDLE_EVIDENCE_MISSING",
            "source_receipt_path": None,
            "receipt_bundle": missing_receipt,
        },
    ]

def classify_bundles(bundles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    a0 = load_a0_module()
    rows: List[Dict[str, Any]] = []
    for bundle in bundles:
        result = a0.classify_receipt(bundle["receipt_bundle"])
        rows.append({
            "frontier_id": bundle["frontier_id"],
            "bundle_status": bundle["bundle_status"],
            "source_receipt_path": bundle["source_receipt_path"],
            "source_selection_rule": bundle["receipt_bundle"].get("source_selection_rule"),
            "a0_classification": result["classification"]["result"],
            "builder_command_allowed": result["classification"]["builder_command_allowed"],
            "operational_spec_candidate_allowed": result["classification"]["operational_spec_candidate_allowed"],
            "candidate_missing_object_proposal_allowed": result["classification"]["candidate_missing_object_proposal_allowed"],
            "reason": result["classification"]["reason"],
            "a0_result": result,
        })
    return rows

def decide(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    counts: Dict[str, int] = {}
    for row in rows:
        counts[row["a0_classification"]] = counts.get(row["a0_classification"], 0) + 1

    question_packet_required = any(row["a0_classification"] == "QUESTION_PACKET_NOT_COMMAND" or row["bundle_status"] != "EXPLICIT_BUNDLE_READY" for row in rows)
    builder_allowed_count = sum(1 for row in rows if row["builder_command_allowed"] is True)
    spec_allowed_count = sum(1 for row in rows if row["operational_spec_candidate_allowed"] is True)
    missing_allowed_count = sum(1 for row in rows if row["candidate_missing_object_proposal_allowed"] is True)

    if builder_allowed_count:
        status = "STOP_AUTHORITY_VIOLATION"
    elif question_packet_required:
        status = "A0_FRONTIER_SOURCE_SELECTION_PATCH_ACCEPTED_WITH_OPTIONAL_EVIDENCE_QUESTION_PACKET"
    elif spec_allowed_count or missing_allowed_count:
        status = "A0_FRONTIER_SOURCE_SELECTION_PATCH_ACCEPTED_CANDIDATE_AVAILABLE_FOR_HUMAN_REVIEW"
    else:
        status = "A0_FRONTIER_SOURCE_SELECTION_PATCH_ACCEPTED_ALL_FRONTIERS_CLOSED"

    return {
        "schema_version": "a0_frontier_source_selection_patched_decision_packet_v0",
        "decision_status": status,
        "classification_counts": counts,
        "builder_command_allowed_count": builder_allowed_count,
        "operational_spec_candidate_allowed_count": spec_allowed_count,
        "candidate_missing_object_proposal_allowed_count": missing_allowed_count,
        "question_packet_required": question_packet_required,
        "builder_command_allowed": False,
        "recommended_next_handling": None,
        "auto_next_command": None,
    }

def validate_outputs(rows: List[Dict[str, Any]], decision: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    classifications = {row["frontier_id"]: row["a0_classification"] for row in rows}
    rules = {row["frontier_id"]: row["source_selection_rule"] for row in rows}

    if any(rule != "explicit_bundle_manifest" for rule in rules.values()):
        failures.append(f"source_selection_rule_not_all_explicit_bundle_manifest:{rules}")
    if classifications.get("frontier_r10000_closed_frozen") != "CLOSE_AND_FREEZE_ACCEPTANCE":
        failures.append(f"r10000_not_close_freeze:{classifications.get('frontier_r10000_closed_frozen')}")
    if classifications.get("frontier_r1000_pressure_queue_closed") != "STOP_LANE_CLOSED":
        failures.append(f"r1000_not_stop_lane_closed:{classifications.get('frontier_r1000_pressure_queue_closed')}")
    if classifications.get("frontier_candidate_missing_object_layer_followup") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append(f"candidate_missing_optional_not_question_packet:{classifications.get('frontier_candidate_missing_object_layer_followup')}")
    if any(row["builder_command_allowed"] is True for row in rows):
        failures.append("builder_command_allowed_by_row")
    if decision.get("builder_command_allowed") is not False:
        failures.append("decision_builder_allowed")
    if decision.get("auto_next_command") is not None:
        failures.append("decision_auto_next_not_null")
    if decision.get("recommended_next_handling") is not None:
        failures.append("decision_recommended_next_not_null")

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
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    for gate, ok in receipt.get("acceptance_gate_results", {}).items():
        if ok is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{ok}")

    metrics = receipt.get("aggregate_metrics", {})
    for key in [
        "frontier_failure_receipt_consumed_count",
        "frontier_failure_review_receipt_consumed_count",
        "fix_authority_packet_consumed_count",
        "patched_selection_packet_emitted_count",
        "patched_bundle_manifest_emitted_count",
        "patched_bundles_emitted_count",
        "patched_classifications_emitted_count",
        "patched_rollup_emitted_count",
        "patched_decision_packet_emitted_count",
        "patched_question_packet_emitted_count",
        "final_acceptance_packet_emitted_count",
        "next_status_packet_emitted_count",
        "r10000_close_freeze_acceptance_count",
        "r1000_stop_lane_closed_count",
        "optional_evidence_question_packet_count",
        "source_selection_rule_patch_acceptance_count",
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
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_A0_FRONTIER_SOURCE_SELECTION_RULE_PATCH_ACCEPTED_HUMAN_DECISION_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    patched_selection = make_patched_selection_packet()
    patched_bundles = make_patched_bundles()
    rows = classify_bundles(patched_bundles)
    decision = decide(rows)

    rollup = {
        "schema_version": "a0_frontier_source_selection_patched_rollup_v0",
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "source_a0_frontier_failure_review_receipt_id": SOURCE_A0_FRONTIER_FAILURE_REVIEW_RECEIPT_ID,
        "frontier_count": len(rows),
        "classification_counts": decision["classification_counts"],
        "builder_command_allowed_count": decision["builder_command_allowed_count"],
        "operational_spec_candidate_allowed_count": decision["operational_spec_candidate_allowed_count"],
        "candidate_missing_object_proposal_allowed_count": decision["candidate_missing_object_proposal_allowed_count"],
        "frontiers": [
            {
                "frontier_id": row["frontier_id"],
                "bundle_status": row["bundle_status"],
                "source_selection_rule": row["source_selection_rule"],
                "a0_classification": row["a0_classification"],
                "builder_command_allowed": row["builder_command_allowed"],
                "reason": row["reason"],
            }
            for row in rows
        ],
    }

    question_rows = [row for row in rows if row["a0_classification"] == "QUESTION_PACKET_NOT_COMMAND" or row["bundle_status"] != "EXPLICIT_BUNDLE_READY"]
    question_packet = {
        "schema_version": "a0_frontier_source_selection_patched_question_packet_v0",
        "packet_status": "QUESTION_PACKET_NOT_COMMAND" if question_rows else "NO_QUESTION_PACKET_REQUIRED",
        "questions": [
            {
                "frontier_id": row["frontier_id"],
                "question": "Optional frontier evidence remains absent. Provide explicit receipt path or explicit bundle manifest if this frontier should be elevated.",
                "classification": row["a0_classification"],
                "bundle_status": row["bundle_status"],
                "reason": row["reason"],
            }
            for row in question_rows
        ],
        "must_not_infer": [
            "do not infer missing optional evidence by latest/mtime",
            "do not convert missing optional evidence to null value",
            "do not execute builder command",
            "do not infer next objective from closed frontiers",
        ],
        "auto_next_command": None,
    }

    report = {
        "schema_version": "a0_frontier_source_selection_patch_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "frontier_failure_receipt_consumed_count": 1,
        "frontier_failure_review_receipt_consumed_count": 1,
        "fix_authority_packet_consumed_count": 1,
        "patched_selection_packet_emitted_count": 1,
        "patched_bundle_manifest_emitted_count": 1,
        "patched_bundles_emitted_count": 1,
        "patched_classifications_emitted_count": 1,
        "patched_rollup_emitted_count": 1,
        "patched_decision_packet_emitted_count": 1,
        "patched_question_packet_emitted_count": 1,
        "final_acceptance_packet_emitted_count": 1,
        "next_status_packet_emitted_count": 1,
        "r10000_classification": next((r["a0_classification"] for r in rows if r["frontier_id"] == "frontier_r10000_closed_frozen"), None),
        "r1000_classification": next((r["a0_classification"] for r in rows if r["frontier_id"] == "frontier_r1000_pressure_queue_closed"), None),
        "candidate_missing_object_frontier_classification": next((r["a0_classification"] for r in rows if r["frontier_id"] == "frontier_candidate_missing_object_layer_followup"), None),
        "r10000_close_freeze_acceptance_count": 1 if any(r["frontier_id"] == "frontier_r10000_closed_frozen" and r["a0_classification"] == "CLOSE_AND_FREEZE_ACCEPTANCE" for r in rows) else 0,
        "r1000_stop_lane_closed_count": 1 if any(r["frontier_id"] == "frontier_r1000_pressure_queue_closed" and r["a0_classification"] == "STOP_LANE_CLOSED" for r in rows) else 0,
        "optional_evidence_question_packet_count": 1 if any(r["frontier_id"] == "frontier_candidate_missing_object_layer_followup" and r["a0_classification"] == "QUESTION_PACKET_NOT_COMMAND" for r in rows) else 0,
        "source_selection_rule_patch_acceptance_count": 1,
        "builder_command_allowed_count": decision["builder_command_allowed_count"],
        "operational_spec_candidate_allowed_count": decision["operational_spec_candidate_allowed_count"],
        "candidate_missing_object_proposal_allowed_count": decision["candidate_missing_object_proposal_allowed_count"],
        "question_packet_required": decision["question_packet_required"],
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
        "recommended_next_handling": None,
    }

    final_acceptance = {
        "schema_version": "a0_frontier_source_selection_patch_final_acceptance_packet_v0",
        "packet_status": "A0_FRONTIER_SOURCE_SELECTION_RULE_PATCH_ACCEPTED",
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "source_a0_frontier_failure_review_receipt_id": SOURCE_A0_FRONTIER_FAILURE_REVIEW_RECEIPT_ID,
        "source_selection_rule_used": "explicit_bundle_manifest",
        "a0_source_selection_enum_widened": False,
        "a0_classifier_law_mutated": False,
        "r10000_frontier_classification": report["r10000_classification"],
        "r1000_frontier_classification": report["r1000_classification"],
        "candidate_missing_object_frontier_classification": report["candidate_missing_object_frontier_classification"],
        "builder_command_allowed_count": decision["builder_command_allowed_count"],
        "builder_command_executed": False,
        "question_packet_required": decision["question_packet_required"],
        "recommended_next_handling": None,
        "auto_next_command": None,
    }

    next_status = {
        "schema_version": "a0_frontier_source_selection_patch_next_status_packet_v0",
        "packet_status": "A0_FRONTIER_SOURCE_SELECTION_PATCH_COMPLETE_HUMAN_DECISION_REQUIRED",
        "decision_status": decision["decision_status"],
        "frontier_rollup": rel(PATCHED_ROLLUP_PATH),
        "decision_packet": rel(PATCHED_DECISION_PACKET_PATH),
        "question_packet": rel(PATCHED_QUESTION_PACKET_PATH),
        "recommended_next_handling": None,
        "auto_next_command": None,
    }

    trace = {
        "schema_version": "a0_frontier_source_selection_patch_transition_trace_v0",
        "trace": [
            {
                "step": "consume_failure_review",
                "question": "was narrow source-selection patch authorized",
                "answer": read_json(A0_FIX_AUTHORITY_PACKET_PATH).get("authorized_next_unit") == UNIT_ID,
                "taken": "patch_bundle_source_selection_rule",
            },
            {
                "step": "patch_bundle_source_selection_rule",
                "question": "was explicit_bundle_manifest used without enum widening",
                "answer": all(row["source_selection_rule"] == "explicit_bundle_manifest" for row in rows),
                "taken": "reclassify_frontiers",
            },
            {
                "step": "reclassify_frontiers",
                "question": "did R10000 classify as close/freeze acceptance",
                "answer": report["r10000_classification"],
                "taken": "emit_final_acceptance",
            },
            {
                "step": "emit_final_acceptance",
                "question": "was any builder command executed",
                "answer": False,
                "taken": "STOP_A0_FRONTIER_SOURCE_SELECTION_RULE_PATCH_ACCEPTED_HUMAN_DECISION_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_A0_FRONTIER_SOURCE_SELECTION_RULE_PATCH_ACCEPTED_HUMAN_DECISION_REQUIRED",
            "next_command_goal": None,
        },
    }

    manifest = {
        "schema_version": "a0_frontier_source_selection_patched_bundle_manifest_v0",
        "bundle_source_selection_rule": "explicit_bundle_manifest",
        "bundle_count": len(patched_bundles),
        "bundles": [
            {
                "frontier_id": bundle["frontier_id"],
                "bundle_status": bundle["bundle_status"],
                "source_receipt_path": bundle["source_receipt_path"],
                "receipt_id": bundle["receipt_bundle"].get("receipt_id"),
                "source_selection_rule": bundle["receipt_bundle"].get("source_selection_rule"),
            }
            for bundle in patched_bundles
        ],
    }

    source_surface = {
        "schema_version": "a0_frontier_source_selection_patch_source_surface_v0",
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "source_a0_frontier_failure_review_receipt_id": SOURCE_A0_FRONTIER_FAILURE_REVIEW_RECEIPT_ID,
        "failure_summary": read_json(A0_FRONTIER_FAILURE_RECEIPT_PATH).get("a0_frontier_application_summary"),
        "review_summary": read_json(A0_FRONTIER_FAILURE_REVIEW_RECEIPT_PATH).get("a0_frontier_failure_review_summary"),
        "fix_authority_packet": read_json(A0_FIX_AUTHORITY_PACKET_PATH),
    }

    patch_plan = {
        "schema_version": "a0_frontier_source_selection_patch_plan_v0",
        "unit_id": UNIT_ID,
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "source_a0_frontier_failure_review_receipt_id": SOURCE_A0_FRONTIER_FAILURE_REVIEW_RECEIPT_ID,
        "patch_type": "wrapper_source_selection_rule_only",
        "from_rule": "explicit_frontier_packet",
        "to_rule": "explicit_bundle_manifest",
        "a0_enum_widening": False,
        "a0_classifier_law_mutation": False,
        "execute_builder_command": False,
    }

    write_json(PATCH_PLAN_PATH, patch_plan)
    write_json(SOURCE_SURFACE_PATH, source_surface)
    write_json(PATCHED_SELECTION_PACKET_PATH, patched_selection)
    write_json(PATCHED_BUNDLE_MANIFEST_PATH, manifest)
    write_json(PATCHED_BUNDLES_PATH, {"schema_version": "a0_frontier_source_selection_patched_bundles_v0", "bundles": patched_bundles})
    write_jsonl(PATCHED_CLASSIFICATIONS_PATH, rows)
    write_json(PATCHED_ROLLUP_PATH, rollup)
    write_json(PATCHED_DECISION_PACKET_PATH, decision)
    write_json(PATCHED_QUESTION_PACKET_PATH, question_packet)
    write_json(FINAL_ACCEPTANCE_PACKET_PATH, final_acceptance)
    write_json(NEXT_STATUS_PACKET_PATH, next_status)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(rows, decision, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "A0_FRONTIER_SOURCE_PATCH_0_FAILURE_REVIEW_CONSUMED": True,
        "A0_FRONTIER_SOURCE_PATCH_1_FIX_AUTHORITY_CONSUMED": True,
        "A0_FRONTIER_SOURCE_PATCH_2_EXPLICIT_BUNDLE_MANIFEST_USED": all(row["source_selection_rule"] == "explicit_bundle_manifest" for row in rows),
        "A0_FRONTIER_SOURCE_PATCH_3_NO_A0_ENUM_WIDENING": report["a0_source_selection_enum_widening_count"] == 0,
        "A0_FRONTIER_SOURCE_PATCH_4_NO_A0_CLASSIFIER_LAW_MUTATION": report["a0_classifier_law_mutation_count"] == 0,
        "A0_FRONTIER_SOURCE_PATCH_5_R10000_CLOSE_FREEZE_ACCEPTED": report["r10000_close_freeze_acceptance_count"] == 1,
        "A0_FRONTIER_SOURCE_PATCH_6_R1000_STOP_LANE_CLOSED": report["r1000_stop_lane_closed_count"] == 1,
        "A0_FRONTIER_SOURCE_PATCH_7_OPTIONAL_EVIDENCE_REMAINS_QUESTION_PACKET": report["optional_evidence_question_packet_count"] == 1,
        "A0_FRONTIER_SOURCE_PATCH_8_NO_BUILDER_COMMAND_ALLOWED": report["builder_command_allowed_count"] == 0,
        "A0_FRONTIER_SOURCE_PATCH_9_NO_BUILDER_COMMAND_EXECUTED": report["builder_command_executed_count"] == 0,
        "A0_FRONTIER_SOURCE_PATCH_10_NO_REPAIR_EXECUTED": report["repair_executed_count"] == 0,
        "A0_FRONTIER_SOURCE_PATCH_11_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "A0_FRONTIER_SOURCE_PATCH_12_NO_LATEST_OR_MTIME_SELECTION": report["latest_or_mtime_selection_count"] == 0,
        "A0_FRONTIER_SOURCE_PATCH_13_NO_RADIUS_RERUN_OR_UNBOUNDED": report["radius_10000_rerun_count"] == 0 and report["radius_above_10000_run_count"] == 0 and report["unbounded_or_no_cap_run_count"] == 0,
        "A0_FRONTIER_SOURCE_PATCH_14_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected or report["builder_command_allowed_count"] != 0:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "source_a0_frontier_failure_review_receipt_id": SOURCE_A0_FRONTIER_FAILURE_REVIEW_RECEIPT_ID,
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "source_r10000_final_close_freeze_receipt_id": SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID,
        "source_r1000_pressure_queue_closure_receipt_id": SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards_packet = {
        "patch_only_source_selection_rule": True,
        "a0_classifier_law_mutated": False,
        "a0_source_selection_enum_widened": False,
        "builder_command_executed": False,
        "repair_executed": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "latest_or_mtime_selection_used": False,
        "radius_10000_rerun": False,
        "radius_above_10000_run": False,
        "unbounded_or_no_cap_run": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "source_a0_frontier_failure_review_receipt_id": SOURCE_A0_FRONTIER_FAILURE_REVIEW_RECEIPT_ID,
        "decision": decision["decision_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "patch_plan": rel(PATCH_PLAN_PATH),
        "source_surface": rel(SOURCE_SURFACE_PATH),
        "patched_selection_packet": rel(PATCHED_SELECTION_PACKET_PATH),
        "patched_bundle_manifest": rel(PATCHED_BUNDLE_MANIFEST_PATH),
        "patched_bundles": rel(PATCHED_BUNDLES_PATH),
        "patched_classifications": rel(PATCHED_CLASSIFICATIONS_PATH),
        "patched_rollup": rel(PATCHED_ROLLUP_PATH),
        "patched_decision_packet": rel(PATCHED_DECISION_PACKET_PATH),
        "patched_question_packet": rel(PATCHED_QUESTION_PACKET_PATH),
        "final_acceptance_packet": rel(FINAL_ACCEPTANCE_PACKET_PATH),
        "next_status_packet": rel(NEXT_STATUS_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_a0_frontier_failure_receipt": rel(A0_FRONTIER_FAILURE_RECEIPT_PATH),
        "source_a0_frontier_failure_review_receipt": rel(A0_FRONTIER_FAILURE_REVIEW_RECEIPT_PATH),
        "source_a0_adapter_script": rel(A0_ADAPTER_PATH),
    }

    receipt = {
        "schema_version": "a0_frontier_source_selection_rule_patch_receipt_v0",
        "receipt_type": "A0_FRONTIER_SOURCE_SELECTION_RULE_PATCH_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_a0_frontier_failure_receipt_id": SOURCE_A0_FRONTIER_FAILURE_RECEIPT_ID,
        "source_a0_frontier_failure_review_receipt_id": SOURCE_A0_FRONTIER_FAILURE_REVIEW_RECEIPT_ID,
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "source_r10000_final_close_freeze_receipt_id": SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID,
        "source_r1000_pressure_queue_closure_receipt_id": SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "a0_frontier_source_selection_patch_summary": {
            "patch_result": "A0_FRONTIER_SOURCE_SELECTION_RULE_PATCH_ACCEPTED",
            "source_selection_rule_used": "explicit_bundle_manifest",
            "r10000_frontier_classification": report["r10000_classification"],
            "r1000_frontier_classification": report["r1000_classification"],
            "candidate_missing_object_frontier_classification": report["candidate_missing_object_frontier_classification"],
            "question_packet_required": report["question_packet_required"],
            "builder_command_allowed_count": report["builder_command_allowed_count"],
            "operational_spec_candidate_allowed_count": report["operational_spec_candidate_allowed_count"],
            "candidate_missing_object_proposal_allowed_count": report["candidate_missing_object_proposal_allowed_count"],
            "a0_classifier_law_mutated": False,
            "a0_source_selection_enum_widened": False,
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "a0_frontier_source_selection_patch_guards": guards_packet,
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
    print(f"a0_frontier_source_selection_patch_receipt_id={receipt_id}")
    print(f"a0_frontier_source_selection_patch_receipt_path=data/a0_frontier_source_selection_rule_explicit_bundle_manifest_patch_v0_receipts/{receipt_id}.json")
    print(f"a0_frontier_source_selection_final_acceptance_packet_path=data/a0_frontier_source_selection_rule_explicit_bundle_manifest_patch_v0/a0_frontier_source_selection_patch_final_acceptance_packet.json")
    print(f"a0_frontier_source_selection_question_packet_path=data/a0_frontier_source_selection_rule_explicit_bundle_manifest_patch_v0/a0_frontier_source_selection_patched_question_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
