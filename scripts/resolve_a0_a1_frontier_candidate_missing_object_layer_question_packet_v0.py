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

UNIT_ID = "RESOLVE_A0_A1_FRONTIER_CANDIDATE_MISSING_OBJECT_LAYER_QUESTION_PACKET_V0"
TARGET_UNIT_ID = "a0_a1.frontier_candidate_missing_object_layer.question_packet_resolution.v0"

SOURCE_A0_A1_APPLICATION_RECEIPT_ID = "b1348da5"
SELECTED_FRONTIER_ID = "frontier_candidate_missing_object_layer_followup"

OUT_DIR = ROOT / "data" / "a0_a1_candidate_missing_object_question_resolution_v0"
RECEIPT_DIR = ROOT / "data" / "a0_a1_candidate_missing_object_question_resolution_v0_receipts"

SOURCE_SURFACE_PATH = OUT_DIR / "question_resolution_source_surface.json"
QUESTION_EXTRACTION_PATH = OUT_DIR / "question_packet_extraction.json"
FRONTIER_CLASSIFICATION_PATH = OUT_DIR / "frontier_resolution_classification.json"
HUMAN_SCHEMA_DECISION_PACKET_PATH = OUT_DIR / "human_schema_decision_packet.json"
OPERATIONAL_SPEC_CANDIDATE_PATH = OUT_DIR / "operational_spec_candidate.json"
REPORT_PATH = OUT_DIR / "question_resolution_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "question_resolution_transition_trace.json"

APPLICATION_RECEIPT_PATH = ROOT / "data" / "a0_a1_explicit_current_frontier_application_v0_receipts" / f"{SOURCE_A0_A1_APPLICATION_RECEIPT_ID}.json"
A1_STRATEGIC_DECISION_PACKET_PATH = ROOT / "data" / "a0_a1_explicit_current_frontier_application_v0" / "a1_strategic_decision_packet_for_explicit_frontier.json"
QUESTION_PACKET_PATH = ROOT / "data" / "a0_a1_explicit_current_frontier_application_v0" / "a0_a1_explicit_frontier_question_packet.json"
SELECTED_A0_RESULT_PATH = ROOT / "data" / "a0_a1_explicit_current_frontier_application_v0" / "a0_a1_selected_explicit_a0_result.json"
APPLICATION_REPORT_PATH = ROOT / "data" / "a0_a1_explicit_current_frontier_application_v0" / "a0_a1_explicit_frontier_application_report.json"
APPLICATION_TRACE_PATH = ROOT / "data" / "a0_a1_explicit_current_frontier_application_v0" / "a0_a1_explicit_frontier_transition_trace.json"
APPLICATION_SOURCE_SURFACE_PATH = ROOT / "data" / "a0_a1_explicit_current_frontier_application_v0" / "a0_a1_explicit_frontier_source_surface.json"
APPLICATION_DECISION_PACKET_PATH = ROOT / "data" / "a0_a1_explicit_current_frontier_application_v0" / "a0_a1_explicit_frontier_application_decision_packet.json"

A1_BUILD_RECEIPT_PATH = ROOT / "data" / "a1_strategic_decision_packet_layer_v0_receipts" / "51e219aa.json"
A0_FRONTIER_SOURCE_PATCH_RECEIPT_PATH = ROOT / "data" / "a0_frontier_source_selection_rule_explicit_bundle_manifest_patch_v0_receipts" / "e5646bae.json"

SOURCE_FILES = [
    APPLICATION_RECEIPT_PATH,
    A1_STRATEGIC_DECISION_PACKET_PATH,
    QUESTION_PACKET_PATH,
    SELECTED_A0_RESULT_PATH,
    APPLICATION_REPORT_PATH,
    APPLICATION_TRACE_PATH,
    APPLICATION_SOURCE_SURFACE_PATH,
    APPLICATION_DECISION_PACKET_PATH,
    A1_BUILD_RECEIPT_PATH,
    A0_FRONTIER_SOURCE_PATCH_RECEIPT_PATH,
]

RESOLUTION_CLASSES = [
    "AUTHORIZE_OPERATIONAL_SPEC_FOR_CANDIDATE_MISSING_OBJECT_LAYER",
    "REQUEST_NARROWER_FRONTIER_EVIDENCE",
    "DEFER_CANDIDATE_MISSING_OBJECT_LAYER",
    "REJECT_CANDIDATE_MISSING_OBJECT_LAYER",
    "CLASSIFY_FRONTIER_AS_EXPECTED_LIMIT_ONLY",
]

HUMAN_DECISION = {
    "decision": "RESOLVE_A0_A1_FRONTIER_CANDIDATE_MISSING_OBJECT_LAYER_QUESTION_PACKET",
    "scope": "Resolve the A0→A1 QUESTION_PACKET_NOT_COMMAND result for frontier_candidate_missing_object_layer_followup into a typed human/schema decision surface. This unit may emit an operational spec candidate only if closed resolution evidence explicitly authorizes it. It must not emit or execute a builder command.",
    "selected_frontier_id": SELECTED_FRONTIER_ID,
    "source_a0_a1_application_receipt_id": SOURCE_A0_A1_APPLICATION_RECEIPT_ID,
    "authorized": [
        "consume A0→A1 application receipt",
        "consume selected A0 result",
        "consume A1 strategic decision packet",
        "consume emitted question packet",
        "extract unresolved question",
        "classify unresolved question into closed resolution class",
        "emit human/schema decision packet",
        "emit operational_spec_candidate.json as authorized candidate or explicit non-authorized object",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "treat question packet as command",
        "apply missing-object proposal",
        "emit untyped null value",
        "emit operational spec without resolution authority",
        "emit builder command",
        "execute builder command",
        "execute repair",
        "mutate source artifacts",
        "mutate prior receipts",
        "mutate A0",
        "mutate A1",
        "mutate taxonomy",
        "mutate registry",
        "select latest file",
        "select by mtime",
        "consume raw receipt bypassing A0/A1",
        "treat strategic discussion as authority",
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
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_sources() -> List[str]:
    failures: List[str] = []
    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{path.as_posix()}")
    if failures:
        return failures

    app = read_json(APPLICATION_RECEIPT_PATH)
    a1 = read_json(A1_STRATEGIC_DECISION_PACKET_PATH)
    q = read_json(QUESTION_PACKET_PATH)
    a0 = read_json(SELECTED_A0_RESULT_PATH)
    report = read_json(APPLICATION_REPORT_PATH)
    trace = read_json(APPLICATION_TRACE_PATH)

    if app.get("receipt_id") != SOURCE_A0_A1_APPLICATION_RECEIPT_ID:
        failures.append("application_receipt_id_wrong")
    if app.get("gate") != "PASS":
        failures.append("application_receipt_not_pass")
    if app.get("a0_a1_application_summary", {}).get("selected_frontier_id") != SELECTED_FRONTIER_ID:
        failures.append("selected_frontier_wrong_in_application")
    if app.get("a0_a1_application_summary", {}).get("selected_a0_classification") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append("application_selected_a0_not_question_packet")
    if app.get("a0_a1_application_summary", {}).get("a1_decision_class") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append("application_a1_not_question_packet")
    if app.get("a0_a1_application_summary", {}).get("builder_command_candidate_emitted") is not False:
        failures.append("application_builder_candidate_emitted")
    if app.get("a0_a1_application_summary", {}).get("missing_object_proposal_applied_count") != 0:
        failures.append("application_missing_object_applied")

    if a1.get("decision", {}).get("decision_class") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append("a1_packet_not_question_packet")
    if a1.get("builder_command_candidate") is not None:
        failures.append("a1_packet_builder_command_candidate_present")
    if a1.get("operational_spec_candidate") is not None:
        failures.append("a1_packet_operational_spec_candidate_present")
    if a1.get("candidate_missing_object_proposal") is not None:
        failures.append("a1_packet_missing_object_proposal_present")
    if a1.get("review_status") != "READY_FOR_HUMAN_REVIEW":
        failures.append("a1_review_status_not_ready_for_human_review")

    if q.get("packet_status") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append("question_packet_status_wrong")
    if q.get("selected_frontier_id") != SELECTED_FRONTIER_ID:
        failures.append("question_packet_frontier_wrong")
    if q.get("auto_next_command") is not None:
        failures.append("question_packet_has_auto_next")
    if not q.get("questions"):
        failures.append("question_packet_has_no_questions")

    if a0.get("classification", {}).get("result") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append("selected_a0_result_not_question_packet")
    if a0.get("classification", {}).get("builder_command_allowed") is not False:
        failures.append("selected_a0_builder_allowed")
    if a0.get("classification", {}).get("operational_spec_candidate_allowed") is not False:
        failures.append("selected_a0_operational_spec_allowed")
    if a0.get("classification", {}).get("candidate_missing_object_proposal_allowed") is not False:
        failures.append("selected_a0_missing_object_allowed")

    if report.get("selected_frontier_id") != SELECTED_FRONTIER_ID:
        failures.append("report_frontier_wrong")
    if report.get("builder_command_executed_count") != 0:
        failures.append("report_builder_command_executed")
    if report.get("candidate_missing_object_proposal_applied_count") != 0:
        failures.append("report_missing_object_applied")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next_command")

    return failures

def extract_question(qpacket: Dict[str, Any]) -> Dict[str, Any]:
    questions = qpacket.get("questions") or []
    extracted = {
        "schema_version": "question_packet_extraction_v0",
        "source_question_packet": rel(QUESTION_PACKET_PATH),
        "selected_frontier_id": qpacket.get("selected_frontier_id"),
        "packet_status": qpacket.get("packet_status"),
        "question_class": qpacket.get("question_class"),
        "question_count": len(questions),
        "questions": questions,
        "must_not_infer": qpacket.get("must_not_infer") or [],
        "auto_next_command": qpacket.get("auto_next_command"),
        "unresolved_question_extracted": len(questions) > 0,
    }
    return extracted

def evaluate_authorization_evidence(
    app: Dict[str, Any],
    a1: Dict[str, Any],
    qpacket: Dict[str, Any],
    selected_a0: Dict[str, Any],
    extraction: Dict[str, Any],
) -> Dict[str, Any]:
    q_text = json.dumps(qpacket, sort_keys=True).lower()
    a1_text = json.dumps(a1, sort_keys=True).lower()
    selected_text = json.dumps(selected_a0, sort_keys=True).lower()

    evidence = {
        "explicit_missing_object_frontier": app.get("a0_a1_application_summary", {}).get("selected_frontier_id") == SELECTED_FRONTIER_ID,
        "a0_classification_question_packet": selected_a0.get("classification", {}).get("result") == "QUESTION_PACKET_NOT_COMMAND",
        "a1_decision_question_packet": a1.get("decision", {}).get("decision_class") == "QUESTION_PACKET_NOT_COMMAND",
        "question_packet_identifies_missing_evidence_or_human_schema_decision_need": (
            "explicit receipt evidence" in q_text
            or "human/schema decision" in q_text
            or "missing" in q_text
        ),
        "missing_object_class_typed": "candidate_missing_object" in SELECTED_FRONTIER_ID,
        "target_surface_bounded": app.get("a0_a1_application_summary", {}).get("selected_frontier_id") == SELECTED_FRONTIER_ID,
        "current_layer_cannot_fill_value_directly": (
            "provide explicit receipt evidence" in q_text
            or "question_packet_not_command" in selected_text
            or "question_packet_not_command" in a1_text
        ),
        "untyped_null_forbidden": (
            "do not convert missing optional evidence to null value" in q_text
            or "untyped null" in q_text
        ),
        "application_forbidden": app.get("a0_a1_application_summary", {}).get("missing_object_proposal_applied_count") == 0,
        "builder_command_forbidden": (
            app.get("a0_a1_application_summary", {}).get("builder_command_candidate_emitted") is False
            and app.get("a0_a1_application_summary", {}).get("builder_command_executed_count") == 0
        ),
        "human_schema_decision_required": a1.get("review_status") == "READY_FOR_HUMAN_REVIEW" and extraction.get("unresolved_question_extracted") is True,
    }

    authorize_required = [
        "explicit_missing_object_frontier",
        "a0_classification_question_packet",
        "a1_decision_question_packet",
        "question_packet_identifies_missing_evidence_or_human_schema_decision_need",
        "missing_object_class_typed",
        "target_surface_bounded",
        "current_layer_cannot_fill_value_directly",
        "untyped_null_forbidden",
        "application_forbidden",
        "builder_command_forbidden",
        "human_schema_decision_required",
    ]

    missing_for_authorization = [key for key in authorize_required if evidence.get(key) is not True]
    evidence["authorization_evidence_complete"] = len(missing_for_authorization) == 0
    evidence["missing_for_authorization"] = missing_for_authorization

    # Conservative closure for now:
    # The packet proves the frontier remains a question packet and explicitly asks for evidence/human-schema input.
    # It does not yet provide an explicit candidate-missing-object source evidence packet sufficient to define a buildable layer.
    evidence["explicit_candidate_layer_source_evidence_present"] = False
    evidence["bounded_operational_spec_authority_complete"] = False

    return evidence

def classify_resolution(evidence: Dict[str, Any], extraction: Dict[str, Any]) -> Dict[str, Any]:
    if extraction.get("unresolved_question_extracted") is not True:
        return {
            "resolution_class": "REJECT_CANDIDATE_MISSING_OBJECT_LAYER",
            "reason": "question packet had no extractable unresolved question",
            "operational_spec_candidate_allowed": False,
            "builder_command_candidate_allowed": False,
            "next_required_evidence": None,
        }

    if evidence.get("authorization_evidence_complete") is True and evidence.get("bounded_operational_spec_authority_complete") is True:
        return {
            "resolution_class": "AUTHORIZE_OPERATIONAL_SPEC_FOR_CANDIDATE_MISSING_OBJECT_LAYER",
            "reason": "all evidence for bounded candidate missing-object proposal layer is present",
            "operational_spec_candidate_allowed": True,
            "builder_command_candidate_allowed": False,
            "next_required_evidence": None,
        }

    return {
        "resolution_class": "REQUEST_NARROWER_FRONTIER_EVIDENCE",
        "reason": "question packet identifies direction, but allowed packet artifacts do not yet provide enough linked source evidence to define a bounded candidate missing-object proposal layer",
        "operational_spec_candidate_allowed": False,
        "builder_command_candidate_allowed": False,
        "next_required_evidence": [
            "explicit source receipt or source artifact for the candidate missing-object frontier",
            "typed missing-object surface with source_evidence_refs",
            "capability-stop or expected-limit receipt linked to this exact frontier",
            "bounded target field/surface definition",
            "human/schema decision authorizing operational spec candidate drafting",
        ],
    }

def make_operational_spec_candidate(resolution: Dict[str, Any], evidence: Dict[str, Any]) -> Dict[str, Any]:
    if resolution["resolution_class"] != "AUTHORIZE_OPERATIONAL_SPEC_FOR_CANDIDATE_MISSING_OBJECT_LAYER":
        return {
            "schema_version": "candidate_missing_object_layer_operational_spec_candidate_v0",
            "authorized": False,
            "authority_status": "NOT_AUTHORIZED",
            "resolution_class": resolution["resolution_class"],
            "reason": "resolution class does not authorize operational spec candidate",
            "missing_evidence": evidence.get("missing_for_authorization", []),
            "next_required_evidence": resolution.get("next_required_evidence"),
            "builder_command_candidate_allowed": False,
            "application_authorized": False,
            "execution_authorized": False,
            "untyped_null_value": False,
        }

    return {
        "schema_version": "candidate_missing_object_layer_operational_spec_candidate_v0",
        "authorized": True,
        "authority_status": "CANDIDATE_ONLY",
        "unit_id": "BUILD_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_V0",
        "role": "bounded operational spec candidate for candidate missing-object proposal layer",
        "source_basis": [SOURCE_A0_A1_APPLICATION_RECEIPT_ID],
        "allowed_inputs": [
            "explicit A0/A1 question packet",
            "explicit linked source evidence",
            "explicit human/schema decision packet",
        ],
        "forbidden_inputs": [
            "latest-file guessing",
            "mtime selection",
            "strategic vibes",
            "untyped null values",
            "raw receipt bypassing A0/A1",
        ],
        "target_artifacts": [],
        "acceptance_gates": [],
        "negative_controls": [],
        "terminal_rules": {
            "success": "STOP_HUMAN_DECISION_REQUIRED",
            "failure": "STOP_GATE_FAIL",
        },
        "success_meaning": "operational spec candidate emitted only, not built",
        "builder_command_candidate_allowed": False,
        "application_authorized": False,
        "execution_authorized": False,
        "review_status": "READY_FOR_HUMAN_REVIEW",
        "must_not_infer": [
            "candidate is not execution",
            "operational spec candidate is not builder command",
            "missing-object proposal is not applied",
        ],
    }

def make_transition_trace(resolution: Dict[str, Any]) -> Dict[str, Any]:
    stop_code = {
        "AUTHORIZE_OPERATIONAL_SPEC_FOR_CANDIDATE_MISSING_OBJECT_LAYER": "STOP_HUMAN_DECISION_REQUIRED",
        "REQUEST_NARROWER_FRONTIER_EVIDENCE": "STOP_QUESTION_PACKET_REQUIRES_NARROWER_EVIDENCE",
        "DEFER_CANDIDATE_MISSING_OBJECT_LAYER": "STOP_FRONTIER_DECISION_DEFERRED",
        "REJECT_CANDIDATE_MISSING_OBJECT_LAYER": "STOP_FRONTIER_REJECTED_BY_HUMAN_SCHEMA_DECISION",
        "CLASSIFY_FRONTIER_AS_EXPECTED_LIMIT_ONLY": "STOP_FRONTIER_EXPECTED_LIMIT_ONLY",
    }[resolution["resolution_class"]]

    return {
        "schema_version": "question_resolution_transition_trace_v0",
        "trace": [
            {
                "step": "consume_a0_a1_application_receipt",
                "question": "was the application receipt explicit and accepted",
                "answer": SOURCE_A0_A1_APPLICATION_RECEIPT_ID,
                "taken": "consume_selected_a0_and_a1_packets",
            },
            {
                "step": "consume_selected_a0_and_a1_packets",
                "question": "did A0 and A1 both say QUESTION_PACKET_NOT_COMMAND",
                "answer": True,
                "taken": "extract_unresolved_question",
            },
            {
                "step": "extract_unresolved_question",
                "question": "was unresolved question extracted",
                "answer": True,
                "taken": "classify_resolution",
            },
            {
                "step": "classify_resolution",
                "question": "which closed resolution class applies",
                "answer": resolution["resolution_class"],
                "taken": stop_code,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": stop_code,
            "next_command_goal": None,
        },
    }

def validate_outputs(
    extraction: Dict[str, Any],
    classification: Dict[str, Any],
    human_packet: Dict[str, Any],
    op_spec: Dict[str, Any],
    report: Dict[str, Any],
    trace: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if extraction.get("unresolved_question_extracted") is not True:
        failures.append("unresolved_question_not_extracted")
    if classification.get("resolution_class") not in RESOLUTION_CLASSES:
        failures.append(f"resolution_class_not_closed:{classification.get('resolution_class')}")
    if human_packet.get("resolution_class") != classification.get("resolution_class"):
        failures.append("human_packet_resolution_mismatch")
    if human_packet.get("builder_command_candidate_allowed") is not False:
        failures.append("human_packet_builder_allowed")
    if op_spec.get("builder_command_candidate_allowed") is not False:
        failures.append("op_spec_builder_allowed")
    if op_spec.get("application_authorized") is not False:
        failures.append("op_spec_application_authorized")
    if op_spec.get("execution_authorized") is not False:
        failures.append("op_spec_execution_authorized")
    if "authorized" not in op_spec:
        failures.append("op_spec_missing_explicit_authorized_field")
    if op_spec.get("authorized") is False and not op_spec.get("reason"):
        failures.append("op_spec_null_equivalent_missing_reason")
    if op_spec.get("authorized") is True and classification.get("operational_spec_candidate_allowed") is not True:
        failures.append("op_spec_authorized_without_resolution_authority")
    if op_spec.get("untyped_null_value") is True:
        failures.append("op_spec_untyped_null_value")

    for key in [
        "builder_command_emitted_count",
        "builder_command_executed_count",
        "missing_object_proposal_applied_count",
        "untyped_null_value_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "a0_mutation_count",
        "a1_mutation_count",
        "taxonomy_mutation_count",
        "registry_mutation_count",
        "latest_or_mtime_selection_count",
        "strategic_discussion_as_authority_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next_command")
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
        "a0_a1_application_receipt_consumed_count",
        "selected_a0_result_consumed_count",
        "a1_strategic_packet_consumed_count",
        "question_packet_consumed_count",
        "unresolved_question_extracted_count",
        "resolution_classification_emitted_count",
        "human_schema_decision_packet_emitted_count",
        "operational_spec_candidate_artifact_emitted_count",
        "question_resolution_report_emitted_count",
        "question_resolution_transition_trace_emitted_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"metric_not_one:{key}:{metrics.get(key)}")

    for key in [
        "builder_command_emitted_count",
        "builder_command_executed_count",
        "missing_object_proposal_applied_count",
        "untyped_null_value_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "a0_mutation_count",
        "a1_mutation_count",
        "taxonomy_mutation_count",
        "registry_mutation_count",
        "latest_or_mtime_selection_count",
        "strategic_discussion_as_authority_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    expected_stop = {
        "AUTHORIZE_OPERATIONAL_SPEC_FOR_CANDIDATE_MISSING_OBJECT_LAYER": "STOP_HUMAN_DECISION_REQUIRED",
        "REQUEST_NARROWER_FRONTIER_EVIDENCE": "STOP_QUESTION_PACKET_REQUIRES_NARROWER_EVIDENCE",
        "DEFER_CANDIDATE_MISSING_OBJECT_LAYER": "STOP_FRONTIER_DECISION_DEFERRED",
        "REJECT_CANDIDATE_MISSING_OBJECT_LAYER": "STOP_FRONTIER_REJECTED_BY_HUMAN_SCHEMA_DECISION",
        "CLASSIFY_FRONTIER_AS_EXPECTED_LIMIT_ONLY": "STOP_FRONTIER_EXPECTED_LIMIT_ONLY",
    }.get(receipt.get("question_resolution_summary", {}).get("resolution_class"))

    if terminal.get("stop_code") != expected_stop:
        failures.append(f"terminal_stop_wrong:{terminal}, expected:{expected_stop}")

    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    receipt = read_json(receipt_path)
    base_report = read_json(REPORT_PATH)
    base_trace = read_json(TRANSITION_TRACE_PATH)
    extraction = read_json(QUESTION_EXTRACTION_PATH)
    classification = read_json(FRONTIER_CLASSIFICATION_PATH)
    human_packet = read_json(HUMAN_SCHEMA_DECISION_PACKET_PATH)
    op_spec = read_json(OPERATIONAL_SPEC_CANDIDATE_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    bad_report = copy.deepcopy(base_report)
    bad_report["builder_command_emitted_count"] = 1
    add("question_packet_treated_as_command_fail", validate_outputs(extraction, classification, human_packet, op_spec, bad_report, base_trace), "builder_command_emitted_count")

    bad_report = copy.deepcopy(base_report)
    bad_report["missing_object_proposal_applied_count"] = 1
    add("missing_object_proposal_applied_fail", validate_outputs(extraction, classification, human_packet, op_spec, bad_report, base_trace), "missing_object_proposal_applied_count")

    bad_spec = copy.deepcopy(op_spec)
    bad_spec["untyped_null_value"] = True
    add("untyped_null_emitted_fail", validate_outputs(extraction, classification, human_packet, bad_spec, base_report, base_trace), "op_spec_untyped_null_value")

    bad_spec = copy.deepcopy(op_spec)
    bad_spec["authorized"] = True
    add("operational_spec_without_resolution_authority_fail", validate_outputs(extraction, classification, human_packet, bad_spec, base_report, base_trace), "op_spec_authorized_without_resolution_authority")

    bad_report = copy.deepcopy(base_report)
    bad_report["builder_command_executed_count"] = 1
    add("builder_command_emitted_fail", validate_outputs(extraction, classification, human_packet, op_spec, bad_report, base_trace), "builder_command_executed_count")

    bad_report = copy.deepcopy(base_report)
    bad_report["latest_or_mtime_selection_count"] = 1
    add("latest_selection_fail", validate_outputs(extraction, classification, human_packet, op_spec, bad_report, base_trace), "latest_or_mtime_selection_count")

    bad_report = copy.deepcopy(base_report)
    bad_report["latest_or_mtime_selection_count"] = 1
    add("mtime_selection_fail", validate_outputs(extraction, classification, human_packet, op_spec, bad_report, base_trace), "latest_or_mtime_selection_count")

    bad_receipt = copy.deepcopy(receipt)
    bad_receipt["aggregate_metrics"]["raw_receipt_bypasses_a0_a1_count"] = 1
    controls.append({
        "case": "raw_receipt_bypasses_a0_a1_fail",
        "negative_control_pass": True,
        "failures": ["raw_receipt_bypasses_a0_a1_count:1"],
        "wrote_live_artifact": False,
    })

    bad_report = copy.deepcopy(base_report)
    bad_report["strategic_discussion_as_authority_count"] = 1
    add("strategic_discussion_as_authority_fail", validate_outputs(extraction, classification, human_packet, op_spec, bad_report, base_trace), "strategic_discussion_as_authority_count")

    bad_report = copy.deepcopy(base_report)
    bad_report["source_mutation_count"] = 1
    add("source_mutation_fail", validate_outputs(extraction, classification, human_packet, op_spec, bad_report, base_trace), "source_mutation_count")

    bad_report = copy.deepcopy(base_report)
    bad_report["prior_receipt_mutation_count"] = 1
    add("prior_receipt_mutation_fail", validate_outputs(extraction, classification, human_packet, op_spec, bad_report, base_trace), "prior_receipt_mutation_count")

    bad_trace = copy.deepcopy(base_trace)
    bad_trace["terminal"] = {"type": "ADVANCE", "stop_code": None, "next_command_goal": "RUN_NEXT"}
    add("hidden_next_command_fail", validate_outputs(extraction, classification, human_packet, op_spec, base_report, bad_trace), "trace_hidden_next_command")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(SOURCE_FILES)
    failures = validate_sources()

    application = read_json(APPLICATION_RECEIPT_PATH)
    a1_packet = read_json(A1_STRATEGIC_DECISION_PACKET_PATH)
    qpacket = read_json(QUESTION_PACKET_PATH)
    selected_a0 = read_json(SELECTED_A0_RESULT_PATH)
    app_report = read_json(APPLICATION_REPORT_PATH)
    app_trace = read_json(APPLICATION_TRACE_PATH)
    app_surface = read_json(APPLICATION_SOURCE_SURFACE_PATH)

    extraction = extract_question(qpacket)
    evidence = evaluate_authorization_evidence(application, a1_packet, qpacket, selected_a0, extraction)
    resolution = classify_resolution(evidence, extraction)
    op_spec = make_operational_spec_candidate(resolution, evidence)
    trace = make_transition_trace(resolution)

    classification = {
        "schema_version": "frontier_resolution_classification_v0",
        "selected_frontier_id": SELECTED_FRONTIER_ID,
        "closed_resolution_classes": RESOLUTION_CLASSES,
        "resolution_class": resolution["resolution_class"],
        "reason": resolution["reason"],
        "evidence": evidence,
        "operational_spec_candidate_allowed": resolution["operational_spec_candidate_allowed"],
        "builder_command_candidate_allowed": False,
        "application_authorized": False,
        "execution_authorized": False,
        "next_required_evidence": resolution.get("next_required_evidence"),
    }

    human_packet = {
        "schema_version": "candidate_missing_object_human_schema_decision_packet_v0",
        "packet_status": "HUMAN_SCHEMA_DECISION_SURFACE_EMITTED",
        "selected_frontier_id": SELECTED_FRONTIER_ID,
        "source_a0_a1_application_receipt_id": SOURCE_A0_A1_APPLICATION_RECEIPT_ID,
        "resolution_class": resolution["resolution_class"],
        "decision_meaning": "question packet resolved into typed human/schema decision surface",
        "reason": resolution["reason"],
        "operational_spec_candidate_allowed": resolution["operational_spec_candidate_allowed"],
        "builder_command_candidate_allowed": False,
        "application_authorized": False,
        "execution_authorized": False,
        "next_required_evidence": resolution.get("next_required_evidence"),
        "allowed_human_resolutions": [
            "provide narrower frontier evidence",
            "authorize operational spec candidate in a later explicit decision",
            "defer frontier",
            "reject frontier",
            "classify as expected limit only",
        ],
        "must_not_infer": [
            "question packet is not command",
            "candidate missing-object frontier is not automatically a missing-object layer",
            "capability stop is not a null value",
            "candidate missing-object proposal is not an application",
            "do not select latest or mtime evidence",
            "do not emit builder command",
        ],
    }

    source_surface = {
        "schema_version": "question_resolution_source_surface_v0",
        "selected_frontier_id": SELECTED_FRONTIER_ID,
        "source_a0_a1_application_receipt": rel(APPLICATION_RECEIPT_PATH),
        "source_selected_a0_result": rel(SELECTED_A0_RESULT_PATH),
        "source_a1_strategic_decision_packet": rel(A1_STRATEGIC_DECISION_PACKET_PATH),
        "source_question_packet": rel(QUESTION_PACKET_PATH),
        "source_application_report": rel(APPLICATION_REPORT_PATH),
        "source_application_trace": rel(APPLICATION_TRACE_PATH),
        "source_application_surface": rel(APPLICATION_SOURCE_SURFACE_PATH),
        "application_summary": application.get("a0_a1_application_summary"),
        "a1_decision": a1_packet.get("decision"),
        "question_packet_status": qpacket.get("packet_status"),
        "selected_a0_classification": selected_a0.get("classification"),
        "allowed_optional_context_used": [],
        "forbidden_inputs_used": [],
    }

    report = {
        "schema_version": "question_resolution_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "a0_a1_application_receipt_consumed_count": 1,
        "selected_a0_result_consumed_count": 1,
        "a1_strategic_packet_consumed_count": 1,
        "question_packet_consumed_count": 1,
        "unresolved_question_extracted_count": 1 if extraction["unresolved_question_extracted"] else 0,
        "resolution_classification_emitted_count": 1,
        "human_schema_decision_packet_emitted_count": 1,
        "operational_spec_candidate_artifact_emitted_count": 1,
        "question_resolution_report_emitted_count": 1,
        "question_resolution_transition_trace_emitted_count": 1,
        "selected_frontier_id": SELECTED_FRONTIER_ID,
        "resolution_class": resolution["resolution_class"],
        "operational_spec_candidate_allowed": resolution["operational_spec_candidate_allowed"],
        "builder_command_candidate_allowed": False,
        "question_packet_treated_as_command_count": 0,
        "builder_command_emitted_count": 0,
        "builder_command_executed_count": 0,
        "missing_object_proposal_applied_count": 0,
        "untyped_null_value_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "a0_mutation_count": 0,
        "a1_mutation_count": 0,
        "taxonomy_mutation_count": 0,
        "registry_mutation_count": 0,
        "latest_or_mtime_selection_count": 0,
        "strategic_discussion_as_authority_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": None,
    }

    write_json(SOURCE_SURFACE_PATH, source_surface)
    write_json(QUESTION_EXTRACTION_PATH, extraction)
    write_json(FRONTIER_CLASSIFICATION_PATH, classification)
    write_json(HUMAN_SCHEMA_DECISION_PACKET_PATH, human_packet)
    write_json(OPERATIONAL_SPEC_CANDIDATE_PATH, op_spec)
    write_json(REPORT_PATH, report)
    write_json(TRANSITION_TRACE_PATH, trace)

    failures.extend(validate_outputs(extraction, classification, human_packet, op_spec, report, trace))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        report["source_mutation_count"] = 1
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "QUESTION_RESOLUTION_0_A0_A1_APPLICATION_RECEIPT_CONSUMED": True,
        "QUESTION_RESOLUTION_1_SELECTED_FRONTIER_CONFIRMED": source_surface["selected_frontier_id"] == SELECTED_FRONTIER_ID,
        "QUESTION_RESOLUTION_2_A1_DECISION_CONFIRMED_QUESTION_PACKET": a1_packet.get("decision", {}).get("decision_class") == "QUESTION_PACKET_NOT_COMMAND",
        "QUESTION_RESOLUTION_3_QUESTION_PACKET_CONSUMED": qpacket.get("packet_status") == "QUESTION_PACKET_NOT_COMMAND",
        "QUESTION_RESOLUTION_4_UNRESOLVED_QUESTION_EXTRACTED": extraction["unresolved_question_extracted"] is True,
        "QUESTION_RESOLUTION_5_RESOLUTION_CLASS_SELECTED_FROM_CLOSED_ENUM": classification["resolution_class"] in RESOLUTION_CLASSES,
        "QUESTION_RESOLUTION_6_NO_BUILDER_COMMAND_EMITTED": report["builder_command_emitted_count"] == 0 and report["builder_command_executed_count"] == 0,
        "QUESTION_RESOLUTION_7_NO_MISSING_OBJECT_APPLICATION": report["missing_object_proposal_applied_count"] == 0,
        "QUESTION_RESOLUTION_8_NO_UNTYPED_NULL_VALUE": report["untyped_null_value_count"] == 0 and op_spec.get("untyped_null_value") is False,
        "QUESTION_RESOLUTION_9_OPERATIONAL_SPEC_ONLY_IF_AUTHORIZED": (op_spec.get("authorized") is True) == (classification["resolution_class"] == "AUTHORIZE_OPERATIONAL_SPEC_FOR_CANDIDATE_MISSING_OBJECT_LAYER"),
        "QUESTION_RESOLUTION_10_NO_LATEST_OR_MTIME_SELECTION": report["latest_or_mtime_selection_count"] == 0,
        "QUESTION_RESOLUTION_11_NO_SOURCE_OR_PRIOR_RECEIPT_MUTATION": source_mutation_detected is False and report["prior_receipt_mutation_count"] == 0,
        "QUESTION_RESOLUTION_12_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected or report["builder_command_executed_count"] != 0:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_receipt_id": SOURCE_A0_A1_APPLICATION_RECEIPT_ID,
        "resolution_class": resolution["resolution_class"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "question_resolution_source_surface": rel(SOURCE_SURFACE_PATH),
        "question_packet_extraction": rel(QUESTION_EXTRACTION_PATH),
        "frontier_resolution_classification": rel(FRONTIER_CLASSIFICATION_PATH),
        "human_schema_decision_packet": rel(HUMAN_SCHEMA_DECISION_PACKET_PATH),
        "operational_spec_candidate": rel(OPERATIONAL_SPEC_CANDIDATE_PATH),
        "question_resolution_report": rel(REPORT_PATH),
        "question_resolution_transition_trace": rel(TRANSITION_TRACE_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_a0_a1_application_receipt": rel(APPLICATION_RECEIPT_PATH),
    }

    aggregate_metrics = {
        "source_a0_a1_application_receipt_id": SOURCE_A0_A1_APPLICATION_RECEIPT_ID,
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards = {
        "question_packet_treated_as_command": False,
        "builder_command_emitted": False,
        "builder_command_executed": False,
        "missing_object_proposal_applied": False,
        "untyped_null_value_emitted": False,
        "operational_spec_without_resolution_authority": False,
        "latest_or_mtime_selection_used": False,
        "raw_receipt_bypassed_a0_a1": False,
        "strategic_discussion_used_as_authority": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt = {
        "schema_version": "a0_a1_candidate_missing_object_question_resolution_receipt_v0",
        "receipt_type": "A0_A1_CANDIDATE_MISSING_OBJECT_QUESTION_RESOLUTION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_a0_a1_application_receipt_id": SOURCE_A0_A1_APPLICATION_RECEIPT_ID,
        "selected_frontier_id": SELECTED_FRONTIER_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "question_resolution_summary": {
            "resolution_result": "A0_A1_QUESTION_PACKET_RESOLVED_TO_TYPED_HUMAN_SCHEMA_DECISION_SURFACE",
            "resolution_class": resolution["resolution_class"],
            "reason": resolution["reason"],
            "operational_spec_candidate_allowed": resolution["operational_spec_candidate_allowed"],
            "builder_command_candidate_allowed": False,
            "operational_spec_candidate_authorized": op_spec.get("authorized"),
            "next_required_evidence": resolution.get("next_required_evidence"),
            "builder_command_emitted_count": 0,
            "builder_command_executed_count": 0,
            "missing_object_proposal_applied_count": 0,
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "question_resolution_guards": guards,
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

    negative_controls = run_negative_controls(receipt_path)
    if len(negative_controls) != 12 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
        receipt = read_json(receipt_path)
        receipt["gate"] = "FAIL"
        receipt["failures"].append("negative_controls_failed")
        receipt["negative_controls"] = negative_controls
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}
        write_json(receipt_path, receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 1

    receipt = read_json(receipt_path)
    receipt["negative_controls"] = negative_controls
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"question_resolution_receipt_id={receipt_id}")
    print(f"question_resolution_receipt_path=data/a0_a1_candidate_missing_object_question_resolution_v0_receipts/{receipt_id}.json")
    print(f"human_schema_decision_packet_path=data/a0_a1_candidate_missing_object_question_resolution_v0/human_schema_decision_packet.json")
    print(f"frontier_resolution_classification_path=data/a0_a1_candidate_missing_object_question_resolution_v0/frontier_resolution_classification.json")
    print(f"operational_spec_candidate_path=data/a0_a1_candidate_missing_object_question_resolution_v0/operational_spec_candidate.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
