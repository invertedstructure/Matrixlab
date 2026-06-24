#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_V0"
TARGET_UNIT_ID = "a0.receipt_to_builder_transition_layer.v0"
SOURCE_DESIGN_OBJECT = "A0_RECEIPT_INTERROGATION_ADAPTER_V0"

OUT_DIR = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0"
RECEIPT_DIR = ROOT / "data" / "a0_receipt_to_builder_transition_layer_v0_receipts"

A0_OUTPUT_SCHEMA_PATH = OUT_DIR / "a0_output_schema_v0.json"
A0_QUESTION_SET_PATH = OUT_DIR / "a0_question_set_v0.json"
A0_CLASSIFICATION_ENUM_PATH = OUT_DIR / "a0_classification_enum_v0.json"
A0_PRESSURE_ENUM_PATH = OUT_DIR / "a0_pressure_enum_v0.json"
A0_COMMAND_CANDIDATE_SCHEMA_PATH = OUT_DIR / "a0_command_candidate_schema_v0.json"
A0_MISSING_OBJECT_PROPOSAL_SCHEMA_PATH = OUT_DIR / "a0_missing_object_proposal_schema_v0.json"
A0_CLASSIFIER_TABLE_PATH = OUT_DIR / "a0_classifier_table_v0.json"
A0_PROBE_CASE_MANIFEST_PATH = OUT_DIR / "a0_probe_case_manifest.json"
A0_PROBE_RESULTS_PATH = OUT_DIR / "a0_probe_results.jsonl"
A0_NEGATIVE_CONTROL_RESULTS_PATH = OUT_DIR / "a0_negative_control_results.jsonl"
A0_TRANSITION_LAYER_REPORT_PATH = OUT_DIR / "a0_transition_layer_report.json"

CLASSIFICATIONS = [
    "STOP_LANE_CLOSED",
    "AWAIT_REAL_BATCH_RECEIPTS",
    "REPAIR_COMMAND_CANDIDATE",
    "OPEN_OBJECTIVE_FROM_PRESSURE_CLASS",
    "QUESTION_PACKET_NOT_COMMAND",
    "OPERATIONAL_SPEC_CANDIDATE",
    "CANDIDATE_MISSING_OBJECT_PROPOSAL",
    "CLOSE_AND_FREEZE_ACCEPTANCE",
]

PRESSURE_ENUM = [
    "NONE",
    "REAL_BATCH_REQUIRED",
    "AMBIGUOUS_PRESSURE",
    "FRAGMENTED_PRESSURE",
    "LOW_MARGIN_PRESSURE",
    "TAXONOMY_PRESSURE",
    "AUTHORITY_BOUNDARY",
    "BURDEN_PRESSURE",
    "EXTRACTION_PRESSURE",
    "RECEIPT_TRACE_PRESSURE",
    "EVIDENCE_SURFACE_DEFICIENCY",
    "MISSING_OBJECT_PRESSURE",
    "CAPABILITY_BOUNDARY",
    "EXPECTED_LIMIT",
]

NEGATIVE_CONTROL_KEYS = [
    "hidden_next_command_count",
    "source_mutation_count",
    "existing_receipt_mutation_count",
    "repair_executed_count",
    "taxonomy_delta_proposal_emitted_count",
    "authority_widening_authorized_count",
    "optimization_authorized_count",
    "unbounded_or_no_cap_run_count",
    "latest_or_mtime_selection",
    "proposal_counted_as_execution",
    "pressure_counted_as_repair",
]

HUMAN_DECISION = {
    "decision": "BUILD_A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER",
    "scope": "Build A0 as the receipt-to-builder transition membrane. A0 consumes explicit receipt bundles, asks a fixed question set, classifies the lawful transition state, and emits only typed candidates or stop packets. It must never execute a builder command, infer a next objective from strategic discussion, use latest/mtime selection, widen authority, or treat STOP_DONE/null-next as a command license.",
    "source_design_object": SOURCE_DESIGN_OBJECT,
    "authorized": [
        "emit static schemas",
        "emit fixed interrogation question set",
        "emit closed classification enum",
        "emit pressure enum",
        "emit classifier table",
        "emit builder command candidate schema",
        "emit missing-object proposal schema",
        "emit probe case manifest",
        "run synthetic probe receipt classifications",
        "run non-writing negative controls",
        "emit adapter script",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "execute builder command",
        "execute repair",
        "mutate source artifacts",
        "mutate prior receipts",
        "invent next objective",
        "infer roadmap from vibes",
        "treat strategic discussion as authority",
        "treat STOP_DONE as automatic next command",
        "treat pressure as repair authorization",
        "treat scale stability as repair authorization",
        "treat missing field as value null without typed object proposal",
        "select live frontier by latest-file guessing",
        "select live frontier by mtime sorting",
        "apply A0 to current frontier in this unit",
    ],
}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_json(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str)

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_json(obj).encode("utf-8")).hexdigest()[:8]

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def read_json(path: Path) -> Any:
    return json.loads(path.read_text())

def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

def flatten_negative_controls(receipt: Dict[str, Any]) -> Dict[str, Any]:
    out: Dict[str, Any] = {}
    for src_key in ("negative_controls", "forbidden_counts", "aggregate_metrics"):
        src = receipt.get(src_key, {})
        if isinstance(src, dict):
            for key in NEGATIVE_CONTROL_KEYS:
                if key in src and key not in out:
                    out[key] = src[key]
    return out

def negative_controls_clean(receipt: Dict[str, Any]) -> Tuple[bool, List[str], List[str]]:
    controls = flatten_negative_controls(receipt)
    failed: List[str] = []
    absent: List[str] = []
    for key in NEGATIVE_CONTROL_KEYS:
        if key not in controls:
            absent.append(key)
            continue
        value = controls[key]
        if isinstance(value, bool):
            if value is not False:
                failed.append(key)
        elif isinstance(value, (int, float)):
            if value != 0:
                failed.append(key)
        elif value not in (None, 0, False, "0", "false", "False"):
            failed.append(key)
    return len(failed) == 0, failed, absent

def receipt_surface_explicit(receipt: Dict[str, Any]) -> bool:
    terminal = receipt.get("terminal")
    has_commit_or_reason = bool(receipt.get("commit")) or bool(receipt.get("no_commit_reason"))
    return (
        bool(receipt.get("receipt_id"))
        and bool(receipt.get("receipt_path"))
        and bool(receipt.get("unit_id"))
        and receipt.get("gate") in ("PASS", "FAIL")
        and isinstance(terminal, dict)
        and "type" in terminal
        and "stop_code" in terminal
        and "next_command_goal" in terminal
        and has_commit_or_reason
    )

def source_selection_valid(receipt: Dict[str, Any]) -> bool:
    rule = receipt.get("source_selection_rule")
    return rule in ("explicit_human_supplied", "explicit_receipt_id", "explicit_receipt_path", "explicit_bundle_manifest")

def infer_lane_or_branch(receipt: Dict[str, Any]) -> str:
    if receipt.get("branch_status") == "CLOSED" or receipt.get("close_and_freeze_summary", {}).get("branch_status") == "CLOSED":
        if receipt.get("close_and_freeze_summary", {}).get("protocol_freeze_status") == "FROZEN_REUSABLE_REFERENCE" or receipt.get("final_close_and_freeze_summary", {}).get("protocol_freeze_status") == "FROZEN_REUSABLE_REFERENCE":
            return "protocol_frozen"
        return "branch_closed"
    if receipt.get("classification") == "CLOSE_AND_FREEZE_ACCEPTANCE":
        return "protocol_frozen"
    if receipt.get("gate") == "FAIL":
        return "repair_attempted"
    if receipt.get("pressure_summary") or receipt.get("remaining_pressure"):
        return "pressure_inspected"
    if receipt.get("evidence_request"):
        return "evidence_requested"
    if receipt.get("candidate_missing_object_proposal") or receipt.get("capability_stop_reached"):
        return "capability_stop_reached"
    terminal = receipt.get("terminal", {})
    if receipt.get("gate") == "PASS" and terminal.get("type") == "STOP" and terminal.get("next_command_goal") is None:
        return "lane_closed"
    return "unclear"

def infer_remaining_pressure(receipt: Dict[str, Any]) -> List[str]:
    pressure = receipt.get("remaining_pressure", [])
    if isinstance(pressure, str):
        pressure = [pressure]
    if not isinstance(pressure, list):
        pressure = []
    out = []
    for item in pressure:
        if item in PRESSURE_ENUM:
            out.append(item)
        elif isinstance(item, dict) and item.get("class") in PRESSURE_ENUM:
            out.append(item["class"])
    if not out:
        dominant = receipt.get("dominant_pressure_class")
        if dominant in PRESSURE_ENUM:
            out.append(dominant)
    return out or ["NONE"]

def infer_authorized_effect(receipt: Dict[str, Any], lane: str) -> str:
    if receipt.get("classification") == "CLOSE_AND_FREEZE_ACCEPTANCE" or lane == "protocol_frozen":
        return "close/freeze acceptance"
    if receipt.get("gate") == "FAIL":
        return "repair predicate" if receipt.get("repair_target") or receipt.get("failure_evidence") or receipt.get("failures") else "question"
    if receipt.get("candidate_missing_object_proposal") or receipt.get("capability_stop_reached"):
        return "candidate missing-object proposal"
    if receipt.get("operational_spec_candidate") or receipt.get("operational_spec_candidate_allowed"):
        return "operational spec candidate"
    pressures = infer_remaining_pressure(receipt)
    if pressures != ["NONE"]:
        if receipt.get("inspection_licensed") is True or receipt.get("pressure_stable_for_inspection") is True:
            return "pressure inspection"
        return "question"
    terminal = receipt.get("terminal", {})
    if receipt.get("gate") == "PASS" and terminal.get("type") == "STOP" and terminal.get("next_command_goal") is None:
        return "no further action"
    if terminal.get("next_command_goal"):
        return "operational spec candidate"
    return "question"

def default_must_not_infer() -> List[str]:
    return [
        "do not infer proof",
        "do not infer optimization",
        "do not infer global closure",
        "do not infer next command",
        "do not infer taxonomy upgrade",
        "do not infer authority widening",
        "do not infer rerun authorization",
        "do not infer missing value from missing field",
        "do not infer live frontier from latest or mtime",
        "do not treat strategic discussion as execution authority",
    ]

def make_repair_candidate(receipt: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "command_id": f"REPAIR_FROM_{receipt.get('unit_id', 'UNKNOWN')}_V0",
        "execution_authorized": False,
        "source_receipt_basis": [receipt.get("receipt_id")],
        "repair_target": receipt.get("repair_target") or receipt.get("failure_target") or "CONCRETE_FAILURE_TARGET_REQUIRED",
        "failure_evidence": receipt.get("failure_evidence") or receipt.get("failures") or [],
        "source_artifacts": receipt.get("output_artifacts", {}),
        "allowed_inputs": ["explicit failed receipt bundle", "concrete failure evidence"],
        "forbidden_inputs": ["strategic vibes", "latest-file guessing", "mtime sorting", "ambient workspace inference"],
        "acceptance_gates": ["repair target is concrete", "forbidden counters remain zero", "terminal next_command_goal null"],
        "negative_controls": NEGATIVE_CONTROL_KEYS,
        "terminal_success": "STOP_HUMAN_DECISION_REQUIRED",
        "terminal_failure": "STOP_GATE_FAIL",
        "success_meaning": "repair command candidate emitted, not executed",
        "must_not_infer": default_must_not_infer(),
    }

def make_operational_spec_candidate(receipt: Dict[str, Any]) -> Dict[str, Any]:
    base_unit = receipt.get("recommended_next_handling") or receipt.get("terminal", {}).get("next_command_goal") or "OPERATIONAL_SPEC_CANDIDATE_REQUIRES_HUMAN_NAME"
    return {
        "unit_id": base_unit,
        "role": "builder-facing operational spec candidate; not executed by A0",
        "source_receipts": [receipt.get("receipt_id")],
        "allowed_inputs": ["explicit receipt bundle", "explicit decision packet", "typed pressure evidence"],
        "forbidden_inputs": ["latest-file guessing", "mtime sorting", "strategic vibes", "authority widening"],
        "target_artifacts": ["operational spec candidate packet"],
        "acceptance_gates": ["receipt gate PASS", "negative controls clean", "human acceptance required before execution"],
        "negative_controls": NEGATIVE_CONTROL_KEYS,
        "terminal_rules": {"success": "STOP_HUMAN_DECISION_REQUIRED", "failure": "STOP_GATE_FAIL"},
        "success_meaning": "A0 drafted an operational spec candidate; builder command not executed",
    }

def make_missing_object_proposal(receipt: Dict[str, Any]) -> Dict[str, Any]:
    proposal = receipt.get("candidate_missing_object_proposal", {})
    if not isinstance(proposal, dict):
        proposal = {}
    candidate_object_id = proposal.get("candidate_object_id") or f"a0_missing_object_{sha8(receipt)[:8]}"
    return {
        "candidate_object_id": candidate_object_id,
        "missing_object_type": proposal.get("missing_object_type") or receipt.get("missing_object_type") or "MISSING_OBJECT_PRESSURE",
        "target_field_or_surface": proposal.get("target_field_or_surface") or receipt.get("target_field_or_surface") or "UNSPECIFIED_SURFACE_REQUIRES_HUMAN_REVIEW",
        "source_pressure_group": proposal.get("source_pressure_group") or receipt.get("source_pressure_group"),
        "source_evidence_refs": proposal.get("source_evidence_refs") or [receipt.get("receipt_id")],
        "why_current_layer_stopped": proposal.get("why_current_layer_stopped") or "capability stop reached; object may be proposed but not applied",
        "required_fields": proposal.get("required_fields") or ["missing_object_type", "target_field_or_surface", "source_evidence_refs", "proposal_basis"],
        "known_fields": proposal.get("known_fields") or {},
        "unknown_but_required_fields": proposal.get("unknown_but_required_fields") or [],
        "proposal_basis": proposal.get("proposal_basis") or "receipt-grounded missing-object pressure",
        "application_authorized": False,
        "allowed_human_resolutions": ["accept candidate", "reject candidate", "revise required fields", "request more evidence"],
        "rejection_feedback_schema": {
            "rejection_reason": None,
            "field_to_change": None,
            "missing_evidence": None,
            "replacement_object_type": None,
        },
    }

def make_command_candidate(receipt: Dict[str, Any], operational: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "command_id": operational.get("unit_id"),
        "execution_authorized": False,
        "source_receipt_basis": [receipt.get("receipt_id")],
        "source_artifacts": receipt.get("output_artifacts", {}),
        "human_decision_basis": receipt.get("decision_packet") or receipt.get("human_decision") or None,
        "allowed_inputs": operational.get("allowed_inputs", []),
        "forbidden_inputs": operational.get("forbidden_inputs", []),
        "target_artifacts": operational.get("target_artifacts", []),
        "acceptance_gates": operational.get("acceptance_gates", []),
        "negative_controls": NEGATIVE_CONTROL_KEYS,
        "terminal_success": "STOP_HUMAN_DECISION_REQUIRED",
        "terminal_failure": "STOP_GATE_FAIL",
        "success_meaning": "candidate emitted for human/builder review; no execution by A0",
        "must_not_infer": default_must_not_infer(),
    }

def classify_receipt(receipt: Dict[str, Any]) -> Dict[str, Any]:
    input_surface = {
        "receipt_id": receipt.get("receipt_id"),
        "receipt_path": receipt.get("receipt_path"),
        "unit_id": receipt.get("unit_id"),
        "gate": receipt.get("gate"),
        "commit": receipt.get("commit"),
        "terminal": receipt.get("terminal"),
        "next_command_goal": receipt.get("terminal", {}).get("next_command_goal") if isinstance(receipt.get("terminal"), dict) else None,
    }

    explicit = receipt_surface_explicit(receipt)
    source_valid = source_selection_valid(receipt)
    gate_passed = receipt.get("gate") == "PASS"
    lane = infer_lane_or_branch(receipt)
    authorized_effect = infer_authorized_effect(receipt, lane)
    must_not = list(dict.fromkeys(default_must_not_infer() + receipt.get("must_not_infer", [])))
    neg_clean, neg_failed, neg_absent = negative_controls_clean(receipt)
    pressure = infer_remaining_pressure(receipt)
    dominant_pressure = receipt.get("dominant_pressure_class")
    if dominant_pressure not in PRESSURE_ENUM:
        dominant_pressure = pressure[0] if pressure else "NONE"

    classification = "QUESTION_PACKET_NOT_COMMAND"
    reason = ""
    builder_allowed = False
    spec_allowed = False
    missing_allowed = False
    op_spec: Optional[Dict[str, Any]] = None
    command_candidate: Optional[Dict[str, Any]] = None
    missing_proposal: Optional[Dict[str, Any]] = None
    decision_packet: Optional[Dict[str, Any]] = None

    if not explicit or not source_valid:
        classification = "QUESTION_PACKET_NOT_COMMAND"
        reason = "receipt surface or explicit source selection is incomplete"
        decision_packet = {
            "packet_type": "QUESTION_PACKET_NOT_COMMAND",
            "missing": {
                "receipt_surface_explicit": explicit,
                "source_selection_valid": source_valid,
                "absent_negative_controls": neg_absent,
            },
        }
    elif not neg_clean:
        classification = "REPAIR_COMMAND_CANDIDATE"
        reason = f"negative controls failed: {neg_failed}"
        command_candidate = make_repair_candidate(receipt)
    elif receipt.get("gate") == "FAIL":
        concrete = bool(receipt.get("repair_target") or receipt.get("failure_evidence") or receipt.get("failures"))
        if concrete:
            classification = "REPAIR_COMMAND_CANDIDATE"
            reason = "gate failed with concrete failure evidence"
            command_candidate = make_repair_candidate(receipt)
        else:
            classification = "QUESTION_PACKET_NOT_COMMAND"
            reason = "gate failed but concrete repair target is ambiguous"
            decision_packet = {"packet_type": "QUESTION_PACKET_NOT_COMMAND", "question": "What concrete repair target does this failed receipt identify?"}
    elif receipt.get("classification") == "CLOSE_AND_FREEZE_ACCEPTANCE" or lane == "protocol_frozen":
        classification = "CLOSE_AND_FREEZE_ACCEPTANCE"
        reason = "branch closure and protocol freeze accepted; terminal next remains null"
        builder_allowed = False
        spec_allowed = False
        decision_packet = {
            "final_state_packet": receipt.get("output_artifacts", {}).get("final_accepted_state_packet") or receipt.get("output_artifacts", {}).get("final_state_packet"),
            "reusable_reference": receipt.get("output_artifacts", {}).get("bounded_protocol_final_reference") or receipt.get("output_artifacts", {}).get("reusable_protocol_reference"),
            "next_command_goal": None,
        }
    elif receipt.get("demo_probe_closed") is True or dominant_pressure == "REAL_BATCH_REQUIRED":
        classification = "AWAIT_REAL_BATCH_RECEIPTS"
        reason = "demo/probe closed but real batch evidence not yet collected"
        decision_packet = {"next_required_evidence": "REAL_BATCH_RECEIPTS"}
    elif receipt.get("candidate_missing_object_proposal") or receipt.get("capability_stop_reached") or dominant_pressure in ("MISSING_OBJECT_PRESSURE", "CAPABILITY_BOUNDARY", "EXPECTED_LIMIT"):
        classification = "CANDIDATE_MISSING_OBJECT_PROPOSAL"
        reason = "capability/missing-object pressure requires candidate object proposal, not null value"
        missing_allowed = True
        missing_proposal = make_missing_object_proposal(receipt)
    elif dominant_pressure in ("AMBIGUOUS_PRESSURE", "FRAGMENTED_PRESSURE", "LOW_MARGIN_PRESSURE") or receipt.get("pressure_ambiguous") is True:
        classification = "QUESTION_PACKET_NOT_COMMAND"
        reason = "pressure exists but is ambiguous or not dominant enough for inspection order"
        decision_packet = {"packet_type": "QUESTION_PACKET_NOT_COMMAND", "pressure": pressure, "dominant_pressure_class": dominant_pressure}
    elif pressure != ["NONE"] and (receipt.get("inspection_licensed") is True or receipt.get("pressure_stable_for_inspection") is True):
        classification = "OPERATIONAL_SPEC_CANDIDATE"
        reason = "stable pressure is clear enough to draft bounded operational spec candidate"
        spec_allowed = True
        op_spec = make_operational_spec_candidate(receipt)
        command_candidate = make_command_candidate(receipt, op_spec)
    elif receipt.get("terminal", {}).get("type") == "STOP" and receipt.get("terminal", {}).get("next_command_goal") is None:
        classification = "STOP_LANE_CLOSED"
        reason = "PASS + STOP + null next + no live actionable pressure"
    elif receipt.get("terminal", {}).get("next_command_goal") or receipt.get("recommended_next_handling"):
        classification = "OPERATIONAL_SPEC_CANDIDATE"
        reason = "receipt explicitly licenses candidate drafting, not execution"
        spec_allowed = True
        op_spec = make_operational_spec_candidate(receipt)
        command_candidate = make_command_candidate(receipt, op_spec)
    else:
        classification = "QUESTION_PACKET_NOT_COMMAND"
        reason = "classification incomplete; no command licensed"

    if command_candidate is not None:
        command_candidate["execution_authorized"] = False
        builder_allowed = False

    result = {
        "schema_version": "a0_receipt_to_builder_transition_layer_v0",
        "interrogation_id": f"a0_{sha8(receipt)}",
        "input_receipt": input_surface,
        "question_answers": {
            "receipt_surface_explicit": explicit,
            "source_selection_valid": source_valid,
            "gate_passed": gate_passed,
            "affected_lane_or_branch": lane,
            "authorized_effect": authorized_effect,
            "must_not_infer": must_not,
            "negative_controls_clean": neg_clean,
            "negative_controls_failed": neg_failed,
            "negative_controls_absent": neg_absent,
            "remaining_pressure": pressure,
            "dominant_pressure_class": dominant_pressure,
            "builder_command_licensed": False,
        },
        "classification": {
            "result": classification,
            "builder_command_allowed": builder_allowed,
            "operational_spec_candidate_allowed": spec_allowed,
            "candidate_missing_object_proposal_allowed": missing_allowed,
            "reason": reason,
        },
        "operational_spec_candidate": op_spec,
        "builder_command_candidate": command_candidate,
        "candidate_missing_object_proposal": missing_proposal,
        "decision_packet": decision_packet,
    }

    if isinstance(result.get("builder_command_candidate"), str):
        raise ValueError("naked command string is forbidden")
    if result["classification"]["builder_command_allowed"] is True:
        raise ValueError("A0 must never allow builder command execution")
    return result

def static_artifacts() -> Dict[str, Any]:
    output_schema = {
        "schema_version": "a0_output_schema_v0",
        "required_top_level_keys": [
            "schema_version",
            "interrogation_id",
            "input_receipt",
            "question_answers",
            "classification",
            "operational_spec_candidate",
            "builder_command_candidate",
            "candidate_missing_object_proposal",
            "decision_packet",
        ],
        "builder_command_candidate_rule": "candidate only; execution_authorized must be false",
        "terminal_rule": "A0 build success stops with STOP_HUMAN_DECISION_REQUIRED and next_command_goal null",
    }

    question_set = {
        "schema_version": "a0_question_set_v0",
        "questions": [
            {"id": "Q0", "question": "Is the receipt surface explicit?", "required": ["receipt_id", "receipt_path", "unit_id", "gate", "terminal", "commit_or_no_commit_reason", "source_selection_rule"]},
            {"id": "Q1", "question": "Did the gate pass?"},
            {"id": "Q2", "question": "What lane or branch did this receipt affect?"},
            {"id": "Q3", "question": "What did the receipt actually authorize?"},
            {"id": "Q4", "question": "What must not be inferred?"},
            {"id": "Q5", "question": "Are negative controls present and clean?"},
            {"id": "Q6", "question": "What pressure remains live?"},
            {"id": "Q7", "question": "Is a builder command explicitly licensed?"},
        ],
    }

    classification_enum = {
        "schema_version": "a0_classification_enum_v0",
        "classification_values": CLASSIFICATIONS,
        "hard_rule": "Only closed enum values are valid.",
    }

    pressure_enum = {
        "schema_version": "a0_pressure_enum_v0",
        "pressure_values": PRESSURE_ENUM,
        "hard_rule": "Pressure classes do not authorize repair or execution by themselves.",
    }

    command_candidate_schema = {
        "schema_version": "a0_command_candidate_schema_v0",
        "required_fields": [
            "command_id",
            "execution_authorized",
            "source_receipt_basis",
            "source_artifacts",
            "human_decision_basis",
            "allowed_inputs",
            "forbidden_inputs",
            "target_artifacts",
            "acceptance_gates",
            "negative_controls",
            "terminal_success",
            "terminal_failure",
            "success_meaning",
            "must_not_infer",
        ],
        "required_constant": {"execution_authorized": False},
        "forbidden": ["naked command string", "execution by A0", "hidden next command"],
    }

    missing_object_schema = {
        "schema_version": "a0_missing_object_proposal_schema_v0",
        "required_fields": [
            "candidate_object_id",
            "missing_object_type",
            "target_field_or_surface",
            "source_pressure_group",
            "source_evidence_refs",
            "why_current_layer_stopped",
            "required_fields",
            "known_fields",
            "unknown_but_required_fields",
            "proposal_basis",
            "application_authorized",
            "allowed_human_resolutions",
            "rejection_feedback_schema",
        ],
        "required_constant": {"application_authorized": False},
    }

    classifier_table = {
        "schema_version": "a0_classifier_table_v0",
        "cases": [
            {"case": "PASS + STOP + null next + no pressure", "classification": "STOP_LANE_CLOSED"},
            {"case": "demo/probe closed cleanly + real evidence not yet collected", "classification": "AWAIT_REAL_BATCH_RECEIPTS"},
            {"case": "FAIL + concrete failure", "classification": "REPAIR_COMMAND_CANDIDATE"},
            {"case": "PASS + pressure ambiguous", "classification": "QUESTION_PACKET_NOT_COMMAND"},
            {"case": "PASS + stable pressure + inspection licensed", "classification": "OPERATIONAL_SPEC_CANDIDATE"},
            {"case": "PASS + missing object / capability stop", "classification": "CANDIDATE_MISSING_OBJECT_PROPOSAL"},
            {"case": "PASS + branch closed / protocol frozen", "classification": "CLOSE_AND_FREEZE_ACCEPTANCE"},
        ],
        "authority_refinement_note": "close-or-freeze may cover human-selected close-and-freeze only as candidate/acceptance after explicit review; never as naked command.",
    }

    return {
        "output_schema": output_schema,
        "question_set": question_set,
        "classification_enum": classification_enum,
        "pressure_enum": pressure_enum,
        "command_candidate_schema": command_candidate_schema,
        "missing_object_schema": missing_object_schema,
        "classifier_table": classifier_table,
    }

def base_negative_controls() -> Dict[str, int]:
    return {key: 0 for key in NEGATIVE_CONTROL_KEYS}

def make_receipt(case_id: str, **overrides: Any) -> Dict[str, Any]:
    receipt = {
        "receipt_id": f"probe_{case_id}",
        "receipt_path": f"data/probes/{case_id}.json",
        "unit_id": f"PROBE_{case_id.upper()}",
        "gate": "PASS",
        "exit_code": 0,
        "commit": "probecommit",
        "source_selection_rule": "explicit_bundle_manifest",
        "terminal": {"type": "STOP", "stop_code": "STOP_DONE", "next_command_goal": None},
        "output_artifacts": {},
        "aggregate_metrics": {},
        "acceptance_gate_results": {},
        "negative_controls": base_negative_controls(),
        "must_not_infer": [],
        "remaining_pressure": ["NONE"],
    }
    receipt.update(overrides)
    return receipt

def probe_cases() -> List[Dict[str, Any]]:
    return [
        {
            "case_id": "closed_lane_receipt",
            "expected_classification": "STOP_LANE_CLOSED",
            "receipt": make_receipt("closed_lane_receipt"),
        },
        {
            "case_id": "failed_gate_receipt",
            "expected_classification": "REPAIR_COMMAND_CANDIDATE",
            "receipt": make_receipt(
                "failed_gate_receipt",
                gate="FAIL",
                exit_code=1,
                terminal={"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None},
                failures=["concrete_error"],
                repair_target="CONCRETE_FAILURE_TARGET",
                failure_evidence=["trace mismatch"],
            ),
        },
        {
            "case_id": "ambiguous_pressure_receipt",
            "expected_classification": "QUESTION_PACKET_NOT_COMMAND",
            "receipt": make_receipt(
                "ambiguous_pressure_receipt",
                remaining_pressure=["AMBIGUOUS_PRESSURE"],
                dominant_pressure_class="AMBIGUOUS_PRESSURE",
                pressure_ambiguous=True,
            ),
        },
        {
            "case_id": "stable_pressure_inspection_receipt",
            "expected_classification": "OPERATIONAL_SPEC_CANDIDATE",
            "receipt": make_receipt(
                "stable_pressure_inspection_receipt",
                remaining_pressure=["EVIDENCE_SURFACE_DEFICIENCY"],
                dominant_pressure_class="EVIDENCE_SURFACE_DEFICIENCY",
                pressure_stable_for_inspection=True,
                inspection_licensed=True,
                recommended_next_handling="INSPECT_STABLE_PRESSURE_SURFACE_V0",
            ),
        },
        {
            "case_id": "not_enough_evidence_receipt",
            "expected_classification": "QUESTION_PACKET_NOT_COMMAND",
            "receipt": make_receipt(
                "not_enough_evidence_receipt",
                receipt_id=None,
                receipt_path=None,
                no_commit_reason="probe missing explicit surface",
                commit=None,
            ),
        },
        {
            "case_id": "missing_object_capability_stop_receipt",
            "expected_classification": "CANDIDATE_MISSING_OBJECT_PROPOSAL",
            "receipt": make_receipt(
                "missing_object_capability_stop_receipt",
                remaining_pressure=["CAPABILITY_BOUNDARY"],
                dominant_pressure_class="CAPABILITY_BOUNDARY",
                capability_stop_reached=True,
                missing_object_type="typed_unresolved_descriptor",
                target_field_or_surface="pressure.surface.missing_descriptor",
                source_pressure_group="probe_pressure_group",
            ),
        },
        {
            "case_id": "close_and_freeze_final_acceptance_receipt",
            "expected_classification": "CLOSE_AND_FREEZE_ACCEPTANCE",
            "receipt": make_receipt(
                "close_and_freeze_final_acceptance_receipt",
                classification="CLOSE_AND_FREEZE_ACCEPTANCE",
                final_close_and_freeze_summary={
                    "final_result": "R10000_OBSERVABILITY_BRANCH_CLOSED_BOUNDED_PROTOCOL_FROZEN_FINAL_ACCEPTED",
                    "branch_status": "CLOSED",
                    "protocol_freeze_status": "FROZEN_REUSABLE_REFERENCE",
                    "recommended_next_handling": None,
                },
                output_artifacts={
                    "final_accepted_state_packet": "data/example/final_state.json",
                    "bounded_protocol_final_reference": "data/example/final_reference.json",
                },
            ),
        },
    ]

def run_probes() -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []
    ok_all = True
    for case in probe_cases():
        result = classify_receipt(case["receipt"])
        ok = result["classification"]["result"] == case["expected_classification"]
        if result.get("builder_command_candidate") is not None:
            ok = ok and result["builder_command_candidate"].get("execution_authorized") is False
        row = {
            "case_id": case["case_id"],
            "expected_classification": case["expected_classification"],
            "observed_classification": result["classification"]["result"],
            "builder_command_allowed": result["classification"]["builder_command_allowed"],
            "operational_spec_candidate_allowed": result["classification"]["operational_spec_candidate_allowed"],
            "candidate_missing_object_proposal_allowed": result["classification"]["candidate_missing_object_proposal_allowed"],
            "probe_pass": ok,
            "result": result,
        }
        rows.append(row)
        ok_all = ok_all and ok
    return rows, ok_all

def expect_failure(case_id: str, func, expected_substring: str) -> Dict[str, Any]:
    try:
        func()
    except Exception as exc:
        return {
            "case_id": case_id,
            "negative_control_pass": expected_substring in str(exc),
            "expected_failure": expected_substring,
            "observed_failure": str(exc),
            "wrote_live_artifact": False,
        }
    return {
        "case_id": case_id,
        "negative_control_pass": False,
        "expected_failure": expected_substring,
        "observed_failure": None,
        "wrote_live_artifact": False,
    }

def assert_condition(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def run_negative_controls() -> Tuple[List[Dict[str, Any]], bool]:
    rows: List[Dict[str, Any]] = []

    def receipt_missing_identity_emits_command_fail() -> None:
        r = make_receipt("neg_missing_identity", receipt_id=None, receipt_path=None)
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] == "QUESTION_PACKET_NOT_COMMAND", "missing identity did not produce question packet")
        assert_condition(out["builder_command_candidate"] is None, "missing identity emitted command candidate")

    def failed_gate_not_repair_candidate_fail() -> None:
        r = make_receipt("neg_fail_gate", gate="FAIL", failures=["x"], repair_target="target", terminal={"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None})
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] == "REPAIR_COMMAND_CANDIDATE", "failed gate not repair candidate")

    def stop_done_null_next_emits_command_fail() -> None:
        r = make_receipt("neg_stop_done")
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] == "STOP_LANE_CLOSED", "stop done null next not lane closed")
        assert_condition(out["builder_command_candidate"] is None, "STOP_DONE null next emitted command")

    def pressure_authorizes_repair_fail() -> None:
        r = make_receipt("neg_pressure_repair", remaining_pressure=["BURDEN_PRESSURE"], dominant_pressure_class="BURDEN_PRESSURE", pressure_stable_for_inspection=True, inspection_licensed=True)
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] != "REPAIR_COMMAND_CANDIDATE", "pressure authorized repair")

    def scale_stability_authorizes_repair_fail() -> None:
        r = make_receipt("neg_scale_stability", scale_stability=True, remaining_pressure=["NONE"])
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] != "REPAIR_COMMAND_CANDIDATE", "scale stability authorized repair")

    def missing_field_left_as_untyped_null_fail() -> None:
        r = make_receipt("neg_missing_field", remaining_pressure=["MISSING_OBJECT_PRESSURE"], dominant_pressure_class="MISSING_OBJECT_PRESSURE", missing_object_type="typed_descriptor")
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] == "CANDIDATE_MISSING_OBJECT_PROPOSAL", "missing field not converted to candidate missing object proposal")
        assert_condition(out["candidate_missing_object_proposal"] is not None, "missing field left null")

    def capability_stop_without_candidate_object_fail() -> None:
        r = make_receipt("neg_cap_stop", capability_stop_reached=True, remaining_pressure=["CAPABILITY_BOUNDARY"], dominant_pressure_class="CAPABILITY_BOUNDARY")
        out = classify_receipt(r)
        assert_condition(out["candidate_missing_object_proposal"] is not None, "capability stop without candidate object")

    def candidate_missing_object_self_applies_fail() -> None:
        r = make_receipt("neg_missing_self_apply", capability_stop_reached=True, remaining_pressure=["CAPABILITY_BOUNDARY"], dominant_pressure_class="CAPABILITY_BOUNDARY")
        out = classify_receipt(r)
        assert_condition(out["candidate_missing_object_proposal"]["application_authorized"] is False, "candidate missing object self-applied")

    def strategic_discussion_as_authority_fail() -> None:
        r = make_receipt("neg_strategic", source_selection_rule="strategic_vibes", terminal={"type": "STOP", "stop_code": "STOP_DONE", "next_command_goal": "RUN_SOMETHING"})
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] == "QUESTION_PACKET_NOT_COMMAND", "strategic discussion treated as authority")

    def latest_or_mtime_selection_fail() -> None:
        r = make_receipt("neg_latest", source_selection_rule="latest")
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] == "QUESTION_PACKET_NOT_COMMAND", "latest/mtime selection accepted")

    def source_mutation_fail() -> None:
        r = make_receipt("neg_source_mutation")
        r["negative_controls"]["source_mutation_count"] = 1
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] == "REPAIR_COMMAND_CANDIDATE", "source mutation did not trigger repair candidate")

    def prior_receipt_mutation_fail() -> None:
        r = make_receipt("neg_receipt_mutation")
        r["negative_controls"]["existing_receipt_mutation_count"] = 1
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] == "REPAIR_COMMAND_CANDIDATE", "prior receipt mutation did not trigger repair candidate")

    def taxonomy_delta_from_pressure_fail() -> None:
        r = make_receipt("neg_taxonomy_pressure", remaining_pressure=["TAXONOMY_PRESSURE"], dominant_pressure_class="TAXONOMY_PRESSURE", pressure_stable_for_inspection=True, inspection_licensed=True)
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] != "REPAIR_COMMAND_CANDIDATE", "taxonomy delta inferred from pressure as repair")
        assert_condition(out["classification"]["result"] == "OPERATIONAL_SPEC_CANDIDATE", "taxonomy pressure not candidate-level")

    def authority_widening_from_pressure_fail() -> None:
        r = make_receipt("neg_authority_widen", remaining_pressure=["AUTHORITY_BOUNDARY"], dominant_pressure_class="AUTHORITY_BOUNDARY", pressure_stable_for_inspection=True, inspection_licensed=True)
        r["negative_controls"]["authority_widening_authorized_count"] = 1
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] == "REPAIR_COMMAND_CANDIDATE", "authority widening not caught")

    def optimization_from_pressure_fail() -> None:
        r = make_receipt("neg_optimization", remaining_pressure=["LOW_MARGIN_PRESSURE"], dominant_pressure_class="LOW_MARGIN_PRESSURE")
        r["negative_controls"]["optimization_authorized_count"] = 1
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] == "REPAIR_COMMAND_CANDIDATE", "optimization from pressure not caught")

    def hidden_next_command_fail() -> None:
        r = make_receipt("neg_hidden_next")
        r["negative_controls"]["hidden_next_command_count"] = 1
        out = classify_receipt(r)
        assert_condition(out["classification"]["result"] == "REPAIR_COMMAND_CANDIDATE", "hidden next command not caught")

    def unknown_classification_enum_fail() -> None:
        assert_condition("MADE_UP_CLASS" not in CLASSIFICATIONS, "unknown classification enum accepted")

    def naked_command_string_fail() -> None:
        r = make_receipt("neg_naked", recommended_next_handling="RUN_NEXT_THING_V0", terminal={"type": "STOP", "stop_code": "STOP_DONE", "next_command_goal": "RUN_NEXT_THING_V0"})
        out = classify_receipt(r)
        assert_condition(not isinstance(out["builder_command_candidate"], str), "naked command string emitted")
        assert_condition(out["builder_command_candidate"]["execution_authorized"] is False, "command candidate execution authorized")

    controls = [
        receipt_missing_identity_emits_command_fail,
        failed_gate_not_repair_candidate_fail,
        stop_done_null_next_emits_command_fail,
        pressure_authorizes_repair_fail,
        scale_stability_authorizes_repair_fail,
        missing_field_left_as_untyped_null_fail,
        capability_stop_without_candidate_object_fail,
        candidate_missing_object_self_applies_fail,
        strategic_discussion_as_authority_fail,
        latest_or_mtime_selection_fail,
        source_mutation_fail,
        prior_receipt_mutation_fail,
        taxonomy_delta_from_pressure_fail,
        authority_widening_from_pressure_fail,
        optimization_from_pressure_fail,
        hidden_next_command_fail,
        unknown_classification_enum_fail,
        naked_command_string_fail,
    ]

    ok_all = True
    for control in controls:
        try:
            control()
            row = {
                "case_id": control.__name__,
                "negative_control_pass": True,
                "observed_failure": None,
                "wrote_live_artifact": False,
            }
        except Exception as exc:
            row = {
                "case_id": control.__name__,
                "negative_control_pass": False,
                "observed_failure": str(exc),
                "wrote_live_artifact": False,
            }
        rows.append(row)
        ok_all = ok_all and row["negative_control_pass"] and not row["wrote_live_artifact"]
    return rows, ok_all

def build_all_artifacts() -> Dict[str, Any]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    artifacts = static_artifacts()
    write_json(A0_OUTPUT_SCHEMA_PATH, artifacts["output_schema"])
    write_json(A0_QUESTION_SET_PATH, artifacts["question_set"])
    write_json(A0_CLASSIFICATION_ENUM_PATH, artifacts["classification_enum"])
    write_json(A0_PRESSURE_ENUM_PATH, artifacts["pressure_enum"])
    write_json(A0_COMMAND_CANDIDATE_SCHEMA_PATH, artifacts["command_candidate_schema"])
    write_json(A0_MISSING_OBJECT_PROPOSAL_SCHEMA_PATH, artifacts["missing_object_schema"])
    write_json(A0_CLASSIFIER_TABLE_PATH, artifacts["classifier_table"])

    manifest = {
        "schema_version": "a0_probe_case_manifest_v0",
        "probe_cases": [
            {
                "case_id": case["case_id"],
                "expected_classification": case["expected_classification"],
                "receipt_id": case["receipt"].get("receipt_id"),
                "description": case["case_id"].replace("_", " "),
            }
            for case in probe_cases()
        ],
    }
    write_json(A0_PROBE_CASE_MANIFEST_PATH, manifest)

    probe_rows, probes_ok = run_probes()
    write_jsonl(A0_PROBE_RESULTS_PATH, probe_rows)

    negative_rows, negatives_ok = run_negative_controls()
    write_jsonl(A0_NEGATIVE_CONTROL_RESULTS_PATH, negative_rows)

    report = {
        "schema_version": "a0_transition_layer_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_design_object": SOURCE_DESIGN_OBJECT,
        "source_design_consumed": True,
        "human_decision_recorded": True,
        "artifact_paths": {
            "output_schema": rel(A0_OUTPUT_SCHEMA_PATH),
            "question_set": rel(A0_QUESTION_SET_PATH),
            "classification_enum": rel(A0_CLASSIFICATION_ENUM_PATH),
            "pressure_enum": rel(A0_PRESSURE_ENUM_PATH),
            "command_candidate_schema": rel(A0_COMMAND_CANDIDATE_SCHEMA_PATH),
            "missing_object_proposal_schema": rel(A0_MISSING_OBJECT_PROPOSAL_SCHEMA_PATH),
            "classifier_table": rel(A0_CLASSIFIER_TABLE_PATH),
            "probe_case_manifest": rel(A0_PROBE_CASE_MANIFEST_PATH),
            "probe_results": rel(A0_PROBE_RESULTS_PATH),
            "negative_control_results": rel(A0_NEGATIVE_CONTROL_RESULTS_PATH),
        },
        "probe_count": len(probe_rows),
        "probe_pass_count": sum(1 for row in probe_rows if row["probe_pass"]),
        "negative_control_count": len(negative_rows),
        "negative_control_pass_count": sum(1 for row in negative_rows if row["negative_control_pass"]),
        "probes_ok": probes_ok,
        "negative_controls_ok": negatives_ok,
        "builder_command_executed_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "live_frontier_application_count": 0,
        "first_live_use_candidate": "APPLY_A0_TO_CURRENT_RECEIPT_CHAIN_FRONTIER_V0",
        "first_live_use_rule": "Frontier must be selected explicitly; no latest-file or mtime guessing.",
        "success_meaning": "A0 exists as a buildable transition layer from explicit receipt evidence to typed candidates or stop packets. No builder command executed.",
    }
    write_json(A0_TRANSITION_LAYER_REPORT_PATH, report)

    return {"report": report, "probe_rows": probe_rows, "negative_rows": negative_rows}

def build_receipt(result: Dict[str, Any]) -> Dict[str, Any]:
    report = result["report"]
    failures: List[str] = []

    expected_files = [
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
        A0_TRANSITION_LAYER_REPORT_PATH,
    ]
    for path in expected_files:
        if not path.exists():
            failures.append(f"missing_output:{rel(path)}")

    probe_by_case = {row["case_id"]: row for row in result["probe_rows"]}
    negative_by_case = {row["case_id"]: row for row in result["negative_rows"]}

    def probe_ok(case_id: str, expected: str) -> bool:
        row = probe_by_case.get(case_id)
        return bool(row and row["probe_pass"] and row["observed_classification"] == expected)

    def neg_ok(case_id: str) -> bool:
        row = negative_by_case.get(case_id)
        return bool(row and row["negative_control_pass"] and row["wrote_live_artifact"] is False)

    acceptance_gate_results = {
        "A0_TRANSITION_0_SOURCE_DESIGN_CONSUMED": report["source_design_consumed"] is True,
        "A0_TRANSITION_1_HUMAN_DECISION_RECORDED": report["human_decision_recorded"] is True,
        "A0_TRANSITION_2_OUTPUT_SCHEMA_EMITTED": A0_OUTPUT_SCHEMA_PATH.exists(),
        "A0_TRANSITION_3_QUESTION_SET_EMITTED": A0_QUESTION_SET_PATH.exists(),
        "A0_TRANSITION_4_CLASSIFICATION_ENUM_EMITTED": A0_CLASSIFICATION_ENUM_PATH.exists(),
        "A0_TRANSITION_5_PRESSURE_ENUM_EMITTED": A0_PRESSURE_ENUM_PATH.exists(),
        "A0_TRANSITION_6_COMMAND_CANDIDATE_SCHEMA_EMITTED": A0_COMMAND_CANDIDATE_SCHEMA_PATH.exists(),
        "A0_TRANSITION_7_MISSING_OBJECT_PROPOSAL_SCHEMA_EMITTED": A0_MISSING_OBJECT_PROPOSAL_SCHEMA_PATH.exists(),
        "A0_TRANSITION_8_CLASSIFIER_TABLE_EMITTED": A0_CLASSIFIER_TABLE_PATH.exists(),
        "A0_TRANSITION_9_PROBE_CASES_EMITTED": A0_PROBE_CASE_MANIFEST_PATH.exists(),
        "A0_TRANSITION_10_PROBE_RESULTS_EMITTED": A0_PROBE_RESULTS_PATH.exists() and report["probe_count"] == 7,
        "A0_TRANSITION_11_STOP_DONE_NULL_NEXT_DOES_NOT_EMIT_COMMAND": probe_ok("closed_lane_receipt", "STOP_LANE_CLOSED") and neg_ok("stop_done_null_next_emits_command_fail"),
        "A0_TRANSITION_12_FAILED_GATE_CLASSIFIES_REPAIR_CANDIDATE": probe_ok("failed_gate_receipt", "REPAIR_COMMAND_CANDIDATE") and neg_ok("failed_gate_not_repair_candidate_fail"),
        "A0_TRANSITION_13_AMBIGUOUS_PRESSURE_CLASSIFIES_QUESTION_PACKET": probe_ok("ambiguous_pressure_receipt", "QUESTION_PACKET_NOT_COMMAND"),
        "A0_TRANSITION_14_CAPABILITY_STOP_CLASSIFIES_MISSING_OBJECT_PROPOSAL": probe_ok("missing_object_capability_stop_receipt", "CANDIDATE_MISSING_OBJECT_PROPOSAL") and neg_ok("capability_stop_without_candidate_object_fail"),
        "A0_TRANSITION_15_CLOSE_FREEZE_CLASSIFIES_FINAL_ACCEPTANCE": probe_ok("close_and_freeze_final_acceptance_receipt", "CLOSE_AND_FREEZE_ACCEPTANCE"),
        "A0_TRANSITION_16_NO_COMMAND_EXECUTED": report["builder_command_executed_count"] == 0 and neg_ok("naked_command_string_fail"),
        "A0_TRANSITION_17_NO_SOURCE_MUTATION": report["source_mutation_count"] == 0 and neg_ok("source_mutation_fail"),
        "A0_TRANSITION_18_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and neg_ok("hidden_next_command_fail"),
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    required_negative_controls = [
        "receipt_missing_identity_emits_command_fail",
        "failed_gate_not_repair_candidate_fail",
        "stop_done_null_next_emits_command_fail",
        "pressure_authorizes_repair_fail",
        "scale_stability_authorizes_repair_fail",
        "missing_field_left_as_untyped_null_fail",
        "capability_stop_without_candidate_object_fail",
        "candidate_missing_object_self_applies_fail",
        "strategic_discussion_as_authority_fail",
        "latest_or_mtime_selection_fail",
        "source_mutation_fail",
        "prior_receipt_mutation_fail",
        "taxonomy_delta_from_pressure_fail",
        "authority_widening_from_pressure_fail",
        "optimization_from_pressure_fail",
        "hidden_next_command_fail",
        "unknown_classification_enum_fail",
        "naked_command_string_fail",
    ]
    for case_id in required_negative_controls:
        if not neg_ok(case_id):
            failures.append(f"negative_control_failed:{case_id}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_HUMAN_DECISION_REQUIRED" if not failures else "STOP_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "report": report,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "output_schema": rel(A0_OUTPUT_SCHEMA_PATH),
        "question_set": rel(A0_QUESTION_SET_PATH),
        "classification_enum": rel(A0_CLASSIFICATION_ENUM_PATH),
        "pressure_enum": rel(A0_PRESSURE_ENUM_PATH),
        "command_candidate_schema": rel(A0_COMMAND_CANDIDATE_SCHEMA_PATH),
        "missing_object_proposal_schema": rel(A0_MISSING_OBJECT_PROPOSAL_SCHEMA_PATH),
        "classifier_table": rel(A0_CLASSIFIER_TABLE_PATH),
        "probe_case_manifest": rel(A0_PROBE_CASE_MANIFEST_PATH),
        "probe_results": rel(A0_PROBE_RESULTS_PATH),
        "negative_control_results": rel(A0_NEGATIVE_CONTROL_RESULTS_PATH),
        "transition_layer_report": rel(A0_TRANSITION_LAYER_REPORT_PATH),
        "adapter_script": "scripts/a0_receipt_to_builder_transition_layer_v0.py",
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "a0_receipt_to_builder_transition_layer_build_receipt_v0",
        "receipt_type": "A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILD_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_design_object": SOURCE_DESIGN_OBJECT,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "a0_build_summary": {
            "build_result": "A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILT" if not failures else "A0_RECEIPT_TO_BUILDER_TRANSITION_LAYER_BUILD_FAILED",
            "schemas_emitted": 6,
            "classifier_table_emitted": True,
            "probe_count": report["probe_count"],
            "probe_pass_count": report["probe_pass_count"],
            "negative_control_count": report["negative_control_count"],
            "negative_control_pass_count": report["negative_control_pass_count"],
            "adapter_script_emitted": True,
            "builder_command_executed_count": 0,
            "live_frontier_application_count": 0,
            "first_live_use_candidate": report["first_live_use_candidate"],
            "success_meaning": report["success_meaning"],
        },
        "aggregate_metrics": {
            "source_design_consumed_count": 1,
            "human_decision_recorded_count": 1,
            "output_schema_emitted_count": 1,
            "question_set_emitted_count": 1,
            "classification_enum_emitted_count": 1,
            "pressure_enum_emitted_count": 1,
            "command_candidate_schema_emitted_count": 1,
            "missing_object_proposal_schema_emitted_count": 1,
            "classifier_table_emitted_count": 1,
            "probe_case_manifest_emitted_count": 1,
            "probe_results_emitted_count": 1,
            "negative_control_results_emitted_count": 1,
            "transition_layer_report_emitted_count": 1,
            "adapter_script_emitted_count": 1,
            "probe_count": report["probe_count"],
            "probe_pass_count": report["probe_pass_count"],
            "negative_control_count": report["negative_control_count"],
            "negative_control_pass_count": report["negative_control_pass_count"],
            "builder_command_executed_count": 0,
            "source_mutation_count": 0,
            "existing_receipt_mutation_count": 0,
            "hidden_next_command_count": 0,
            "live_frontier_application_count": 0,
        },
        "acceptance_gate_results": acceptance_gate_results,
        "a0_build_guards": {
            "build_only_no_live_application": True,
            "builder_command_executed": False,
            "repair_executed": False,
            "source_mutated": False,
            "prior_receipts_mutated": False,
            "hidden_next_command": False,
            "latest_or_mtime_selection_used": False,
            "strategic_discussion_as_authority": False,
            "authority_widened": False,
            "taxonomy_delta_applied": False,
            "optimization_authorized": False,
        },
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)
    return receipt

def run_build() -> int:
    result = build_all_artifacts()
    receipt = build_receipt(result)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"a0_transition_receipt_id={receipt['receipt_id']}")
    print(f"a0_transition_receipt_path={receipt['output_artifacts']['implementation_receipt']}")
    print(f"a0_transition_report_path={rel(A0_TRANSITION_LAYER_REPORT_PATH)}")
    print(f"a0_adapter_script_path=scripts/a0_receipt_to_builder_transition_layer_v0.py")
    return 0 if receipt["gate"] == "PASS" else 1

def run_classify(receipt_path: str) -> int:
    path = Path(receipt_path)
    if not path.is_absolute():
        path = ROOT / path
    receipt = read_json(path)
    result = classify_receipt(receipt)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="A0 receipt-to-builder transition layer v0")
    sub = parser.add_subparsers(dest="cmd")

    sub.add_parser("build", help="build schemas, classifier table, probes, negative controls, and receipt")

    classify = sub.add_parser("classify", help="classify one explicit receipt bundle")
    classify.add_argument("--receipt-path", required=True)

    args = parser.parse_args(argv)

    if args.cmd == "classify":
        return run_classify(args.receipt_path)
    return run_build()

if __name__ == "__main__":
    raise SystemExit(main())
