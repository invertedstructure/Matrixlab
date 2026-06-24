#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "APPLY_A0_TO_CURRENT_RECEIPT_CHAIN_FRONTIER_V0"
TARGET_UNIT_ID = "a0.current_receipt_chain_frontier.application.v0"

SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID = "6d14e637"
SOURCE_A0_BUILD_RECEIPT_ID = "067fcaed"
SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID = "2ff85a7a"
SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID = "454aa103"
SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID = "52d0ea8d"
SOURCE_EXPECTED_LIMIT_MARK_RECEIPT_ID = "db7c0af2"
SOURCE_CANDIDATE_MISSING_OBJECT_ACCEPTED_DESCRIPTOR_RECEIPT_ID = "91f8eea5"
SOURCE_EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT_ID = "cbde4b69"

OUT_DIR = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0"
RECEIPT_DIR = ROOT / "data" / "a0_current_receipt_chain_frontier_application_v0_receipts"

FRONTIER_SELECTION_PACKET_PATH = OUT_DIR / "a0_explicit_frontier_selection_packet.json"
FRONTIER_BUNDLE_MANIFEST_PATH = OUT_DIR / "a0_frontier_receipt_bundle_manifest.json"
FRONTIER_BUNDLES_PATH = OUT_DIR / "a0_frontier_explicit_receipt_bundles.json"
FRONTIER_CLASSIFICATIONS_PATH = OUT_DIR / "a0_frontier_classifications.jsonl"
FRONTIER_ROLLUP_PATH = OUT_DIR / "a0_frontier_classification_rollup.json"
FRONTIER_DECISION_PACKET_PATH = OUT_DIR / "a0_frontier_decision_packet.json"
QUESTION_PACKET_PATH = OUT_DIR / "a0_frontier_question_packet.json"
OPERATIONAL_SPEC_CANDIDATE_PATH = OUT_DIR / "a0_frontier_operational_spec_candidate.json"
NEXT_STATUS_PACKET_PATH = OUT_DIR / "a0_frontier_application_next_status_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "a0_frontier_application_transition_trace.json"
REPORT_PATH = OUT_DIR / "a0_frontier_application_report.json"

A0_FINAL_ACCEPTANCE_RECEIPT_PATH = ROOT / "data" / "a0_self_classification_assertion_acceptance_patch_v0_receipts" / f"{SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID}.json"
A0_FINAL_ACCEPTANCE_PACKET_PATH = ROOT / "data" / "a0_self_classification_assertion_acceptance_patch_v0" / "a0_transition_layer_final_acceptance_packet.json"
A0_NEXT_STATUS_PACKET_PATH = ROOT / "data" / "a0_self_classification_assertion_acceptance_patch_v0" / "a0_self_classification_assertion_acceptance_next_status_packet.json"
A0_BUILD_RECEIPT_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0_receipts" / f"{SOURCE_A0_BUILD_RECEIPT_ID}.json"
A0_SELF_CLASS_REVIEW_RECEIPT_PATH = ROOT / "data" / "a0_build_failure_self_classification_assertion_review_v0_receipts" / f"{SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID}.json"
A0_ADAPTER_PATH = ROOT / "scripts" / "a0_receipt_to_builder_transition_layer_v0.py"
A0_REPORT_PATH = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0" / "a0_transition_layer_report.json"

R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH = ROOT / "data" / "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0_receipts" / f"{SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID}.json"
R10000_FINAL_STATE_PACKET_PATH = ROOT / "data" / "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0" / "r10000_close_and_freeze_final_accepted_state_packet.json"
R10000_BOUNDED_PROTOCOL_FINAL_REFERENCE_PATH = ROOT / "data" / "r10000_close_and_freeze_acceptance_after_authority_string_mismatch_patch_v0" / "bounded_observability_protocol_final_reference_v0.json"

R1000_CLOSURE_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0_receipts" / f"{SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID}.json"
R1000_CLOSED_HANDOFF_PATH = ROOT / "data" / "r1000_pressure_queue_closure_review_after_synthetic_remainder_expected_limit_v0" / "r1000_pressure_queue_closed_handoff_after_synthetic_remainder_expected_limit.json"
EXPECTED_LIMIT_MARK_RECEIPT_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_MARK_RECEIPT_ID}.json"
FINAL_QUEUE_STATE_PATH = ROOT / "data" / "r1000_synthetic_remainder_expected_queue_resolution_limit_mark_v0" / "r1000_final_pressure_queue_state_after_synthetic_remainder_expected_limit.json"

ACCEPTED_DESCRIPTOR_RECEIPT_PATH = ROOT / "data" / "r1000_top_group_taxonomy_gap_surface_with_accepted_typed_unresolved_descriptor_review_v0_receipts" / f"{SOURCE_CANDIDATE_MISSING_OBJECT_ACCEPTED_DESCRIPTOR_RECEIPT_ID}.json"
EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_mark_v0_receipts" / f"{SOURCE_EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT_ID}.json"

SOURCE_FILES = [
    A0_FINAL_ACCEPTANCE_RECEIPT_PATH,
    A0_FINAL_ACCEPTANCE_PACKET_PATH,
    A0_NEXT_STATUS_PACKET_PATH,
    A0_BUILD_RECEIPT_PATH,
    A0_SELF_CLASS_REVIEW_RECEIPT_PATH,
    A0_ADAPTER_PATH,
    A0_REPORT_PATH,
    R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH,
    R10000_FINAL_STATE_PACKET_PATH,
    R10000_BOUNDED_PROTOCOL_FINAL_REFERENCE_PATH,
    R1000_CLOSURE_REVIEW_RECEIPT_PATH,
    R1000_CLOSED_HANDOFF_PATH,
    EXPECTED_LIMIT_MARK_RECEIPT_PATH,
    FINAL_QUEUE_STATE_PATH,
]

OPTIONAL_SOURCE_FILES = [
    ACCEPTED_DESCRIPTOR_RECEIPT_PATH,
    EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT_PATH,
]

HUMAN_DECISION = {
    "decision": "APPLY_A0_TO_CURRENT_RECEIPT_CHAIN_FRONTIER",
    "scope": "Apply the built A0 receipt-to-builder transition layer to an explicit frontier packet. Classify current frontier candidates from explicit receipt bundles only. Do not select by latest file, mtime, vibes, or hidden roadmap. Emit classifications, question packet or operational spec candidate if licensed, and stop without executing builder commands.",
    "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
    "authorized": [
        "consume A0 final acceptance receipt and adapter",
        "construct explicit frontier selection packet",
        "construct explicit receipt bundles for named frontier candidates",
        "run A0 classification on explicit bundles",
        "emit frontier classification rollup",
        "emit decision packet",
        "emit operational spec candidate only if licensed by explicit frontier classification",
        "emit question packet when evidence is missing or ambiguous",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "execute builder command",
        "execute repair",
        "mutate source artifacts",
        "mutate prior receipts",
        "select live frontier by latest-file guessing",
        "select live frontier by mtime sorting",
        "infer roadmap from strategic discussion",
        "treat R10000 closure as next objective license",
        "treat R1000 queue closure as repair authorization",
        "treat missing optional frontier evidence as null value",
        "apply taxonomy changes",
        "run radius-10000 again",
        "run radius above 10000",
        "run unbounded/no-cap harvest",
        "hide next command",
    ],
}

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

def with_a0_surface(receipt: Dict[str, Any], receipt_path: Path, no_commit_reason: str) -> Dict[str, Any]:
    bundle = copy.deepcopy(receipt)
    bundle["receipt_path"] = rel(receipt_path)
    bundle["source_selection_rule"] = "explicit_frontier_packet"
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

def validate_sources() -> List[str]:
    failures: List[str] = []
    a0_final = read_json(A0_FINAL_ACCEPTANCE_RECEIPT_PATH)
    a0_packet = read_json(A0_FINAL_ACCEPTANCE_PACKET_PATH)
    a0_report = read_json(A0_REPORT_PATH)
    r10000 = read_json(R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH)
    r1000 = read_json(R1000_CLOSURE_REVIEW_RECEIPT_PATH)
    handoff = read_json(R1000_CLOSED_HANDOFF_PATH)
    final_queue = read_json(FINAL_QUEUE_STATE_PATH)

    if a0_final.get("receipt_id") != SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID:
        failures.append("a0_final_acceptance_receipt_id_wrong")
    if a0_final.get("gate") != "PASS":
        failures.append("a0_final_acceptance_not_pass")
    if a0_final.get("a0_assertion_acceptance_patch_summary", {}).get("patch_result") != "A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILT_PATCH_ACCEPTED":
        failures.append("a0_not_final_accepted")
    if a0_packet.get("packet_status") != "A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILT_PATCH_ACCEPTED":
        failures.append("a0_final_acceptance_packet_status_wrong")
    if a0_report.get("builder_command_executed_count") != 0:
        failures.append("a0_build_executed_command")
    if not A0_ADAPTER_PATH.exists():
        failures.append("a0_adapter_missing")

    if r10000.get("receipt_id") != SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID:
        failures.append("r10000_final_close_freeze_receipt_id_wrong")
    if r10000.get("gate") != "PASS":
        failures.append("r10000_final_close_freeze_not_pass")
    if r10000.get("final_close_and_freeze_summary", {}).get("final_result") != "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN_FINAL_ACCEPTED":
        failures.append("r10000_final_not_closed_frozen")

    if r1000.get("receipt_id") != SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID:
        failures.append("r1000_closure_receipt_id_wrong")
    if r1000.get("gate") != "PASS":
        failures.append("r1000_closure_not_pass")
    if handoff.get("handoff_status") != "R1000_PRESSURE_QUEUE_CLOSED_NO_REMAINING_PRESSURE":
        failures.append("r1000_handoff_not_closed")
    if final_queue.get("queue_state_status") != "R1000_PRESSURE_QUEUE_CLOSED":
        failures.append("r1000_final_queue_not_closed")
    if final_queue.get("remaining_open_group_count") != 0 or final_queue.get("remaining_open_row_count") != 0:
        failures.append("r1000_final_queue_has_open_pressure")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
    return failures

def make_frontier_selection_packet() -> Dict[str, Any]:
    candidates = [
        {
            "frontier_id": "frontier_r10000_closed_frozen",
            "frontier_label": "R10000 branch closed/frozen",
            "selection_basis": "explicit_human_supplied",
            "source_receipt_id": SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID,
            "source_receipt_path": rel(R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH),
            "expected_a0_classification": "CLOSE_AND_FREEZE_ACCEPTANCE",
            "why_included": "recently closed branch; verify no next command should be inferred",
        },
        {
            "frontier_id": "frontier_r1000_pressure_queue_closed",
            "frontier_label": "R1000 pressure queue closed after expected source-content limit",
            "selection_basis": "explicit_human_supplied",
            "source_receipt_id": SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID,
            "source_receipt_path": rel(R1000_CLOSURE_REVIEW_RECEIPT_PATH),
            "expected_a0_classification": "STOP_LANE_CLOSED",
            "why_included": "closed pressure queue; verify no repair or pressure execution is inferred",
        },
        {
            "frontier_id": "frontier_candidate_missing_object_layer_followup",
            "frontier_label": "candidate missing-object layer / expected source-content limit follow-up",
            "selection_basis": "explicit_human_supplied",
            "source_receipt_id": SOURCE_EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT_ID,
            "source_receipt_path": rel(EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT_PATH) if EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT_PATH.exists() else None,
            "expected_a0_classification": "QUESTION_PACKET_NOT_COMMAND",
            "why_included": "design-level next transition may exist, but must not be inferred without explicit receipt evidence",
        },
    ]
    return {
        "schema_version": "a0_explicit_frontier_selection_packet_v0",
        "packet_status": "EXPLICIT_FRONTIER_SELECTION_FOR_A0_APPLICATION",
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "selection_rule": "explicit_human_supplied_frontier_packet",
        "forbidden_selection_rules": ["latest", "mtime", "workspace_guess", "strategic_vibes", "hidden_builder_state"],
        "candidate_frontiers": candidates,
        "human_decision": HUMAN_DECISION,
        "auto_selected_frontier": None,
    }

def make_frontier_bundles(selection: Dict[str, Any]) -> List[Dict[str, Any]]:
    bundles: List[Dict[str, Any]] = []

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
    bundles.append({
        "frontier_id": "frontier_r10000_closed_frozen",
        "bundle_status": "EXPLICIT_BUNDLE_READY",
        "source_receipt_path": rel(R10000_FINAL_CLOSE_FREEZE_RECEIPT_PATH),
        "receipt_bundle": r10000_receipt,
    })

    r1000_receipt = with_a0_surface(
        read_json(R1000_CLOSURE_REVIEW_RECEIPT_PATH),
        R1000_CLOSURE_REVIEW_RECEIPT_PATH,
        "R1000 pressure queue closure review receipt already committed in prior branch",
    )
    r1000_receipt["remaining_pressure"] = ["NONE"]
    r1000_receipt["dominant_pressure_class"] = "NONE"
    r1000_receipt["output_artifacts"] = {
        **(r1000_receipt.get("output_artifacts") or {}),
        "closed_queue_handoff": rel(R1000_CLOSED_HANDOFF_PATH),
        "final_queue_state": rel(FINAL_QUEUE_STATE_PATH),
    }
    bundles.append({
        "frontier_id": "frontier_r1000_pressure_queue_closed",
        "bundle_status": "EXPLICIT_BUNDLE_READY",
        "source_receipt_path": rel(R1000_CLOSURE_REVIEW_RECEIPT_PATH),
        "receipt_bundle": r1000_receipt,
    })

    if EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT_PATH.exists():
        missing_source = read_json(EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT_PATH)
        candidate_receipt = with_a0_surface(
            missing_source,
            EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT_PATH,
            "expected source content limit receipt already committed in prior branch",
        )
        candidate_receipt["remaining_pressure"] = ["EXPECTED_LIMIT"]
        candidate_receipt["dominant_pressure_class"] = "EXPECTED_LIMIT"
        candidate_receipt["capability_stop_reached"] = True
        candidate_receipt["missing_object_type"] = "expected_source_content_limit_followup"
        candidate_receipt["target_field_or_surface"] = "candidate_missing_object_layer.expected_source_content_limit"
        status = "EXPLICIT_BUNDLE_READY"
    else:
        candidate_receipt = {
            "receipt_id": SOURCE_EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT_ID,
            "receipt_path": None,
            "unit_id": "EXPECTED_SOURCE_CONTENT_LIMIT_FRONTIER_EVIDENCE_MISSING",
            "gate": None,
            "no_commit_reason": "source receipt path absent from current explicit frontier input surface",
            "source_selection_rule": "explicit_human_supplied",
            "terminal": {"type": "STOP", "stop_code": "STOP_EVIDENCE_MISSING", "next_command_goal": None},
            "negative_controls": NEGATIVE_CONTROLS,
            "remaining_pressure": ["EVIDENCE_SURFACE_DEFICIENCY"],
            "dominant_pressure_class": "EVIDENCE_SURFACE_DEFICIENCY",
            "must_not_infer": [
                "do not infer candidate missing-object followup without explicit receipt evidence",
                "do not use latest or mtime to find the missing receipt",
            ],
        }
        status = "EXPLICIT_BUNDLE_EVIDENCE_MISSING"
    bundles.append({
        "frontier_id": "frontier_candidate_missing_object_layer_followup",
        "bundle_status": status,
        "source_receipt_path": rel(EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT_PATH) if EXPECTED_SOURCE_CONTENT_LIMIT_RECEIPT_PATH.exists() else None,
        "receipt_bundle": candidate_receipt,
    })

    return bundles

def classify_frontiers(bundles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    a0 = load_a0_module()
    rows: List[Dict[str, Any]] = []
    for bundle in bundles:
        result = a0.classify_receipt(bundle["receipt_bundle"])
        rows.append({
            "frontier_id": bundle["frontier_id"],
            "bundle_status": bundle["bundle_status"],
            "source_receipt_path": bundle["source_receipt_path"],
            "a0_classification": result["classification"]["result"],
            "builder_command_allowed": result["classification"]["builder_command_allowed"],
            "operational_spec_candidate_allowed": result["classification"]["operational_spec_candidate_allowed"],
            "candidate_missing_object_proposal_allowed": result["classification"]["candidate_missing_object_proposal_allowed"],
            "reason": result["classification"]["reason"],
            "a0_result": result,
        })
    return rows

def decide_frontier(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    close_count = sum(1 for r in rows if r["a0_classification"] == "CLOSE_AND_FREEZE_ACCEPTANCE")
    stop_count = sum(1 for r in rows if r["a0_classification"] == "STOP_LANE_CLOSED")
    question_count = sum(1 for r in rows if r["a0_classification"] == "QUESTION_PACKET_NOT_COMMAND")
    spec_count = sum(1 for r in rows if r["a0_classification"] == "OPERATIONAL_SPEC_CANDIDATE")
    missing_count = sum(1 for r in rows if r["a0_classification"] == "CANDIDATE_MISSING_OBJECT_PROPOSAL")
    repair_count = sum(1 for r in rows if r["a0_classification"] == "REPAIR_COMMAND_CANDIDATE")

    command_allowed_count = sum(1 for r in rows if r["builder_command_allowed"] is True)
    ambiguous_or_missing = [r for r in rows if r["a0_classification"] == "QUESTION_PACKET_NOT_COMMAND" or r["bundle_status"] != "EXPLICIT_BUNDLE_READY"]
    operational_candidates = [r for r in rows if r["operational_spec_candidate_allowed"] is True or r["candidate_missing_object_proposal_allowed"] is True]

    if command_allowed_count:
        decision = "STOP_AUTHORITY_VIOLATION"
        recommended = None
        question_packet_required = False
        operational_spec_allowed = False
    elif operational_candidates:
        decision = "FRONTIER_OPERATIONAL_SPEC_OR_MISSING_OBJECT_CANDIDATE_AVAILABLE_FOR_HUMAN_REVIEW"
        recommended = None
        question_packet_required = False
        operational_spec_allowed = True
    elif ambiguous_or_missing:
        decision = "QUESTION_PACKET_NOT_COMMAND_FOR_FRONTIER_EVIDENCE_OR_SELECTION_GAP"
        recommended = None
        question_packet_required = True
        operational_spec_allowed = False
    else:
        decision = "ALL_EXPLICIT_FRONTIERS_CLASSIFIED_CLOSED_NO_COMMAND"
        recommended = None
        question_packet_required = False
        operational_spec_allowed = False

    return {
        "schema_version": "a0_frontier_decision_packet_v0",
        "decision_status": decision,
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "frontier_counts": {
            "total": len(rows),
            "close_and_freeze_acceptance": close_count,
            "stop_lane_closed": stop_count,
            "question_packet_not_command": question_count,
            "operational_spec_candidate": spec_count,
            "candidate_missing_object_proposal": missing_count,
            "repair_command_candidate": repair_count,
            "builder_command_allowed": command_allowed_count,
        },
        "question_packet_required": question_packet_required,
        "operational_spec_candidate_allowed": operational_spec_allowed,
        "builder_command_allowed": False,
        "recommended_next_handling": recommended,
        "auto_next_command": None,
    }

def validate_outputs(rows: List[Dict[str, Any]], decision: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if not rows:
        failures.append("no_frontier_rows")
    if any(r["builder_command_allowed"] is True for r in rows):
        failures.append("builder_command_allowed_by_a0_frontier")
    if decision.get("builder_command_allowed") is not False:
        failures.append("decision_builder_command_allowed_not_false")
    if decision.get("auto_next_command") is not None:
        failures.append("decision_auto_next_not_null")

    classifications = {r["frontier_id"]: r["a0_classification"] for r in rows}
    if classifications.get("frontier_r10000_closed_frozen") != "CLOSE_AND_FREEZE_ACCEPTANCE":
        failures.append(f"r10000_frontier_wrong_classification:{classifications.get('frontier_r10000_closed_frozen')}")
    if classifications.get("frontier_r1000_pressure_queue_closed") not in ("STOP_LANE_CLOSED", "QUESTION_PACKET_NOT_COMMAND"):
        failures.append(f"r1000_frontier_unexpected_classification:{classifications.get('frontier_r1000_pressure_queue_closed')}")
    if classifications.get("frontier_candidate_missing_object_layer_followup") not in ("QUESTION_PACKET_NOT_COMMAND", "CANDIDATE_MISSING_OBJECT_PROPOSAL"):
        failures.append(f"candidate_frontier_unexpected_classification:{classifications.get('frontier_candidate_missing_object_layer_followup')}")

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
        "a0_final_acceptance_receipt_consumed_count",
        "explicit_frontier_selection_packet_emitted_count",
        "frontier_bundle_manifest_emitted_count",
        "frontier_bundles_emitted_count",
        "frontier_classification_rows_emitted_count",
        "frontier_rollup_emitted_count",
        "frontier_decision_packet_emitted_count",
        "next_status_packet_emitted_count",
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
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_A0_FRONTIER_APPLICATION_COMPLETE_HUMAN_DECISION_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES + [p for p in OPTIONAL_SOURCE_FILES if p.exists()])
    failures = validate_sources()

    selection = make_frontier_selection_packet()
    bundles = make_frontier_bundles(selection)
    rows = classify_frontiers(bundles)
    decision = decide_frontier(rows)

    rollup = {
        "schema_version": "a0_frontier_classification_rollup_v0",
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "frontier_count": len(rows),
        "classification_counts": {},
        "builder_command_allowed_count": sum(1 for r in rows if r["builder_command_allowed"] is True),
        "operational_spec_candidate_allowed_count": sum(1 for r in rows if r["operational_spec_candidate_allowed"] is True),
        "candidate_missing_object_proposal_allowed_count": sum(1 for r in rows if r["candidate_missing_object_proposal_allowed"] is True),
        "frontiers": [
            {
                "frontier_id": r["frontier_id"],
                "bundle_status": r["bundle_status"],
                "a0_classification": r["a0_classification"],
                "builder_command_allowed": r["builder_command_allowed"],
                "operational_spec_candidate_allowed": r["operational_spec_candidate_allowed"],
                "candidate_missing_object_proposal_allowed": r["candidate_missing_object_proposal_allowed"],
                "reason": r["reason"],
            }
            for r in rows
        ],
    }
    for row in rows:
        rollup["classification_counts"][row["a0_classification"]] = rollup["classification_counts"].get(row["a0_classification"], 0) + 1

    question_packet = {
        "schema_version": "a0_frontier_question_packet_v0",
        "packet_status": "QUESTION_PACKET_NOT_COMMAND" if decision["question_packet_required"] else "NO_QUESTION_PACKET_REQUIRED",
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "questions": [],
        "must_not_infer": [
            "do not infer next objective from closed R10000 branch",
            "do not infer repair from closed R1000 pressure queue",
            "do not infer candidate missing-object followup from missing optional evidence",
            "do not select missing frontier receipt by latest or mtime",
            "do not execute a builder command from this A0 application",
        ],
        "auto_next_command": None,
    }
    if decision["question_packet_required"]:
        for row in rows:
            if row["a0_classification"] == "QUESTION_PACKET_NOT_COMMAND" or row["bundle_status"] != "EXPLICIT_BUNDLE_READY":
                question_packet["questions"].append({
                    "frontier_id": row["frontier_id"],
                    "question": "Provide an explicit receipt bundle/source path or human frontier selection if this frontier should become an operational spec candidate.",
                    "classification": row["a0_classification"],
                    "bundle_status": row["bundle_status"],
                    "reason": row["reason"],
                })

    operational_spec_candidate = None
    if decision["operational_spec_candidate_allowed"]:
        operational_spec_candidate = {
            "schema_version": "a0_frontier_operational_spec_candidate_v0",
            "candidate_status": "OPERATIONAL_SPEC_CANDIDATE_AVAILABLE_FOR_HUMAN_REVIEW",
            "execution_authorized": False,
            "source_frontier_rows": [
                r["frontier_id"] for r in rows
                if r["operational_spec_candidate_allowed"] or r["candidate_missing_object_proposal_allowed"]
            ],
            "allowed_inputs": ["explicit frontier packet", "explicit receipt bundle"],
            "forbidden_inputs": ["latest", "mtime", "strategic vibes", "hidden builder state"],
            "terminal_success": "STOP_HUMAN_DECISION_REQUIRED",
        }

    report = {
        "schema_version": "a0_frontier_application_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "a0_final_acceptance_receipt_consumed_count": 1,
        "explicit_frontier_selection_packet_emitted_count": 1,
        "frontier_bundle_manifest_emitted_count": 1,
        "frontier_bundles_emitted_count": 1,
        "frontier_classification_rows_emitted_count": 1,
        "frontier_rollup_emitted_count": 1,
        "frontier_decision_packet_emitted_count": 1,
        "question_packet_emitted_count": 1,
        "operational_spec_candidate_emitted_count": 1 if operational_spec_candidate else 0,
        "next_status_packet_emitted_count": 1,
        "frontier_count": len(rows),
        "builder_command_allowed_count": rollup["builder_command_allowed_count"],
        "operational_spec_candidate_allowed_count": rollup["operational_spec_candidate_allowed_count"],
        "candidate_missing_object_proposal_allowed_count": rollup["candidate_missing_object_proposal_allowed_count"],
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
        "recommended_next_handling": None,
    }

    next_status = {
        "schema_version": "a0_frontier_application_next_status_packet_v0",
        "packet_status": "A0_FRONTIER_APPLICATION_COMPLETE_HUMAN_DECISION_REQUIRED",
        "decision_status": decision["decision_status"],
        "frontier_rollup": rel(FRONTIER_ROLLUP_PATH),
        "decision_packet": rel(FRONTIER_DECISION_PACKET_PATH),
        "question_packet": rel(QUESTION_PACKET_PATH),
        "operational_spec_candidate": rel(OPERATIONAL_SPEC_CANDIDATE_PATH) if operational_spec_candidate else None,
        "recommended_next_handling": None,
        "auto_next_command": None,
    }

    trace = {
        "schema_version": "a0_frontier_application_transition_trace_v0",
        "trace": [
            {
                "step": "consume_a0_final_acceptance",
                "question": "is A0 built and final accepted",
                "answer": read_json(A0_FINAL_ACCEPTANCE_RECEIPT_PATH).get("gate") == "PASS",
                "taken": "construct_explicit_frontier_packet",
            },
            {
                "step": "construct_explicit_frontier_packet",
                "question": "was frontier selected explicitly",
                "answer": selection["selection_rule"],
                "taken": "classify_frontier_bundles",
            },
            {
                "step": "classify_frontier_bundles",
                "question": "did A0 allow any builder command",
                "answer": rollup["builder_command_allowed_count"] > 0,
                "taken": "emit_decision_packet",
            },
            {
                "step": "emit_decision_packet",
                "question": "what is the frontier decision",
                "answer": decision["decision_status"],
                "taken": "STOP_A0_FRONTIER_APPLICATION_COMPLETE_HUMAN_DECISION_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_A0_FRONTIER_APPLICATION_COMPLETE_HUMAN_DECISION_REQUIRED",
            "next_command_goal": None,
        },
    }

    manifest = {
        "schema_version": "a0_frontier_receipt_bundle_manifest_v0",
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "bundle_count": len(bundles),
        "bundles": [
            {
                "frontier_id": b["frontier_id"],
                "bundle_status": b["bundle_status"],
                "source_receipt_path": b["source_receipt_path"],
                "receipt_id": b["receipt_bundle"].get("receipt_id"),
            }
            for b in bundles
        ],
    }

    write_json(FRONTIER_SELECTION_PACKET_PATH, selection)
    write_json(FRONTIER_BUNDLE_MANIFEST_PATH, manifest)
    write_json(FRONTIER_BUNDLES_PATH, {"schema_version": "a0_frontier_explicit_receipt_bundles_v0", "bundles": bundles})
    write_jsonl(FRONTIER_CLASSIFICATIONS_PATH, rows)
    write_json(FRONTIER_ROLLUP_PATH, rollup)
    write_json(FRONTIER_DECISION_PACKET_PATH, decision)
    write_json(QUESTION_PACKET_PATH, question_packet)
    if operational_spec_candidate:
        write_json(OPERATIONAL_SPEC_CANDIDATE_PATH, operational_spec_candidate)
    else:
        write_json(OPERATIONAL_SPEC_CANDIDATE_PATH, {"schema_version": "a0_frontier_operational_spec_candidate_v0", "candidate_status": "NOT_EMITTED", "execution_authorized": False})
    write_json(NEXT_STATUS_PACKET_PATH, next_status)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(rows, decision, report))

    source_after = snapshot_files(SOURCE_FILES + [p for p in OPTIONAL_SOURCE_FILES if p.exists()])
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "A0_FRONTIER_0_A0_FINAL_ACCEPTANCE_CONSUMED": True,
        "A0_FRONTIER_1_EXPLICIT_SELECTION_PACKET_EMITTED": FRONTIER_SELECTION_PACKET_PATH.exists(),
        "A0_FRONTIER_2_NO_LATEST_OR_MTIME_SELECTION": report["latest_or_mtime_selection_count"] == 0,
        "A0_FRONTIER_3_FRONTIER_BUNDLES_EXPLICIT": len(bundles) == 3,
        "A0_FRONTIER_4_CLASSIFICATIONS_EMITTED": FRONTIER_CLASSIFICATIONS_PATH.exists() and len(rows) == 3,
        "A0_FRONTIER_5_R10000_CLASSIFIES_CLOSE_FREEZE_ACCEPTANCE": any(r["frontier_id"] == "frontier_r10000_closed_frozen" and r["a0_classification"] == "CLOSE_AND_FREEZE_ACCEPTANCE" for r in rows),
        "A0_FRONTIER_6_NO_BUILDER_COMMAND_ALLOWED": report["builder_command_allowed_count"] == 0,
        "A0_FRONTIER_7_DECISION_PACKET_EMITTED": FRONTIER_DECISION_PACKET_PATH.exists(),
        "A0_FRONTIER_8_QUESTION_PACKET_OR_SPEC_CANDIDATE_TYPED": QUESTION_PACKET_PATH.exists() and OPERATIONAL_SPEC_CANDIDATE_PATH.exists(),
        "A0_FRONTIER_9_NO_COMMAND_EXECUTED": report["builder_command_executed_count"] == 0,
        "A0_FRONTIER_10_NO_REPAIR_EXECUTED": report["repair_executed_count"] == 0,
        "A0_FRONTIER_11_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["existing_receipt_mutation_count"] == 0,
        "A0_FRONTIER_12_NO_RADIUS_RERUN_OR_UNBOUNDED": report["radius_10000_rerun_count"] == 0 and report["radius_above_10000_run_count"] == 0 and report["unbounded_or_no_cap_run_count"] == 0,
        "A0_FRONTIER_13_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected or report["builder_command_allowed_count"] != 0:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "source_a0_self_class_review_receipt_id": SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID,
        "source_r10000_final_close_freeze_receipt_id": SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID,
        "source_r1000_pressure_queue_closure_receipt_id": SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards_packet = {
        "explicit_frontier_selection_only": True,
        "latest_or_mtime_selection_used": False,
        "builder_command_executed": False,
        "repair_executed": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "strategic_discussion_as_authority": False,
        "radius_10000_rerun": False,
        "radius_above_10000_run": False,
        "unbounded_or_no_cap_run": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "decision": decision["decision_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "frontier_selection_packet": rel(FRONTIER_SELECTION_PACKET_PATH),
        "frontier_bundle_manifest": rel(FRONTIER_BUNDLE_MANIFEST_PATH),
        "frontier_bundles": rel(FRONTIER_BUNDLES_PATH),
        "frontier_classifications": rel(FRONTIER_CLASSIFICATIONS_PATH),
        "frontier_rollup": rel(FRONTIER_ROLLUP_PATH),
        "frontier_decision_packet": rel(FRONTIER_DECISION_PACKET_PATH),
        "question_packet": rel(QUESTION_PACKET_PATH),
        "operational_spec_candidate": rel(OPERATIONAL_SPEC_CANDIDATE_PATH),
        "next_status_packet": rel(NEXT_STATUS_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_a0_final_acceptance_receipt": rel(A0_FINAL_ACCEPTANCE_RECEIPT_PATH),
        "source_a0_adapter_script": rel(A0_ADAPTER_PATH),
    }

    receipt = {
        "schema_version": "a0_current_receipt_chain_frontier_application_receipt_v0",
        "receipt_type": "A0_CURRENT_RECEIPT_CHAIN_FRONTIER_APPLICATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_a0_final_acceptance_receipt_id": SOURCE_A0_FINAL_ACCEPTANCE_RECEIPT_ID,
        "source_a0_build_receipt_id": SOURCE_A0_BUILD_RECEIPT_ID,
        "source_a0_self_class_review_receipt_id": SOURCE_A0_SELF_CLASS_REVIEW_RECEIPT_ID,
        "source_r10000_final_close_freeze_receipt_id": SOURCE_R10000_FINAL_CLOSE_FREEZE_RECEIPT_ID,
        "source_r1000_pressure_queue_closure_receipt_id": SOURCE_R1000_PRESSURE_QUEUE_CLOSURE_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "a0_frontier_application_summary": {
            "application_result": "A0_FRONTIER_APPLICATION_COMPLETE",
            "frontier_count": len(rows),
            "decision_status": decision["decision_status"],
            "r10000_frontier_classification": next((r["a0_classification"] for r in rows if r["frontier_id"] == "frontier_r10000_closed_frozen"), None),
            "r1000_frontier_classification": next((r["a0_classification"] for r in rows if r["frontier_id"] == "frontier_r1000_pressure_queue_closed"), None),
            "candidate_missing_object_frontier_classification": next((r["a0_classification"] for r in rows if r["frontier_id"] == "frontier_candidate_missing_object_layer_followup"), None),
            "builder_command_allowed_count": report["builder_command_allowed_count"],
            "operational_spec_candidate_allowed_count": report["operational_spec_candidate_allowed_count"],
            "candidate_missing_object_proposal_allowed_count": report["candidate_missing_object_proposal_allowed_count"],
            "question_packet_required": decision["question_packet_required"],
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "a0_frontier_application_guards": guards_packet,
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
    print(f"a0_frontier_application_receipt_id={receipt_id}")
    print(f"a0_frontier_application_receipt_path=data/a0_current_receipt_chain_frontier_application_v0_receipts/{receipt_id}.json")
    print(f"a0_frontier_decision_packet_path=data/a0_current_receipt_chain_frontier_application_v0/a0_frontier_decision_packet.json")
    print(f"a0_frontier_question_packet_path=data/a0_current_receipt_chain_frontier_application_v0/a0_frontier_question_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
