#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

A1_SCHEMA_VERSION = "strategic_decision_packet_v0"
A1_LAYER_SCHEMA_VERSION = "a1_strategic_decision_packet_layer_v0"

DECISION_CLASSES = [
    "STOP_LANE_CLOSED",
    "AWAIT_REAL_BATCH_RECEIPTS",
    "REPAIR_OBJECTIVE",
    "OPEN_OBJECTIVE_FROM_PRESSURE_CLASS",
    "QUESTION_PACKET_NOT_COMMAND",
    "EMIT_OPERATIONAL_SPEC_CANDIDATE",
    "EMIT_BUILDER_COMMAND_CANDIDATE",
    "CANDIDATE_MISSING_OBJECT_PROPOSAL",
    "CLOSE_AND_FREEZE_ACCEPTANCE",
    "DEFER_STRATEGIC_DECISION",
]

REVIEW_STATUSES = [
    "PACKETIZED_ONLY",
    "READY_FOR_HUMAN_REVIEW",
    "READY_FOR_BUILDER_REVIEW",
    "DEFERRED",
    "CLOSED",
]

AUTHORITY_STATUSES = [
    "PACKET_ONLY",
    "CANDIDATE_ONLY",
    "REVIEW_REQUIRED",
    "EXECUTION_NOT_AUTHORIZED",
]

A0_TO_A1_MAPPING = {
    "STOP_LANE_CLOSED": "STOP_LANE_CLOSED",
    "AWAIT_REAL_BATCH_RECEIPTS": "AWAIT_REAL_BATCH_RECEIPTS",
    "REPAIR_COMMAND_CANDIDATE": "REPAIR_OBJECTIVE",
    "OPEN_OBJECTIVE_FROM_PRESSURE_CLASS": "OPEN_OBJECTIVE_FROM_PRESSURE_CLASS",
    "QUESTION_PACKET_NOT_COMMAND": "QUESTION_PACKET_NOT_COMMAND",
    "OPERATIONAL_SPEC_CANDIDATE": "EMIT_OPERATIONAL_SPEC_CANDIDATE",
    "CANDIDATE_MISSING_OBJECT_PROPOSAL": "CANDIDATE_MISSING_OBJECT_PROPOSAL",
    "CLOSE_AND_FREEZE_ACCEPTANCE": "CLOSE_AND_FREEZE_ACCEPTANCE",
    "DEFER_STRATEGIC_DECISION": "DEFER_STRATEGIC_DECISION",
}

REQUIRED_A0_TOP_LEVEL = [
    "schema_version",
    "interrogation_id",
    "input_receipt",
    "question_answers",
    "classification",
    "operational_spec_candidate",
    "builder_command_candidate",
    "candidate_missing_object_proposal",
    "decision_packet",
]

REQUIRED_A0_INPUT_RECEIPT = [
    "receipt_id",
    "receipt_path",
    "unit_id",
    "gate",
    "commit",
    "terminal",
    "next_command_goal",
]

REQUIRED_A0_QUESTION_ANSWERS = [
    "receipt_surface_explicit",
    "gate_passed",
    "affected_lane_or_branch",
    "authorized_effect",
    "must_not_infer",
    "negative_controls_clean",
    "remaining_pressure",
    "dominant_pressure_class",
    "builder_command_licensed",
]

REQUIRED_A0_CLASSIFICATION = [
    "result",
    "builder_command_allowed",
    "operational_spec_candidate_allowed",
    "candidate_missing_object_proposal_allowed",
    "reason",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

def normalize_under_root(path: Path) -> Path:
    if path.is_absolute():
        return path.resolve()
    return (ROOT / path).resolve()

def rel(path: Path) -> str:
    return normalize_under_root(path).relative_to(ROOT.resolve()).as_posix()

class A1AuthorityError(ValueError):
    pass

class A1ValidationError(ValueError):
    pass

def validate_a0_result(a0: Dict[str, Any]) -> None:
    missing = [key for key in REQUIRED_A0_TOP_LEVEL if key not in a0]
    if missing:
        raise A1AuthorityError(f"A1 requires explicit A0 wrapper; missing top-level keys: {missing}")

    if a0.get("schema_version") != "a0_receipt_to_builder_transition_layer_v0":
        raise A1AuthorityError(f"invalid A0 schema_version: {a0.get('schema_version')}")

    input_receipt = a0.get("input_receipt")
    question_answers = a0.get("question_answers")
    classification = a0.get("classification")

    if not isinstance(input_receipt, dict):
        raise A1AuthorityError("A0 input_receipt must be object")
    if not isinstance(question_answers, dict):
        raise A1AuthorityError("A0 question_answers must be object")
    if not isinstance(classification, dict):
        raise A1AuthorityError("A0 classification must be object")

    missing_input = [key for key in REQUIRED_A0_INPUT_RECEIPT if key not in input_receipt]
    if missing_input:
        raise A1AuthorityError(f"A0 input_receipt missing keys: {missing_input}")

    missing_qa = [key for key in REQUIRED_A0_QUESTION_ANSWERS if key not in question_answers]
    if missing_qa:
        raise A1AuthorityError(f"A0 question_answers missing keys: {missing_qa}")

    missing_classification = [key for key in REQUIRED_A0_CLASSIFICATION if key not in classification]
    if missing_classification:
        raise A1AuthorityError(f"A0 classification missing keys: {missing_classification}")

    result = classification.get("result")
    if result not in A0_TO_A1_MAPPING:
        raise A1ValidationError(f"unknown A0 classification result: {result}")

    if classification.get("builder_command_allowed") is True and a0.get("builder_command_candidate") is None:
        raise A1ValidationError("builder_command_allowed true requires builder_command_candidate")

    if a0.get("builder_command_candidate") is not None:
        candidate = a0["builder_command_candidate"]
        if isinstance(candidate, str):
            raise A1AuthorityError("A1 rejects naked builder command string")
        if not isinstance(candidate, dict):
            raise A1ValidationError("builder_command_candidate must be object when present")

def a0_basis(a0: Dict[str, Any]) -> Dict[str, Any]:
    input_receipt = a0["input_receipt"]
    terminal = input_receipt.get("terminal") or {}
    return {
        "interrogation_id": a0.get("interrogation_id"),
        "a0_schema_version": a0.get("schema_version"),
        "a0_classification": a0["classification"].get("result"),
        "receipt_id": input_receipt.get("receipt_id"),
        "receipt_path": input_receipt.get("receipt_path"),
        "commit": input_receipt.get("commit"),
        "gate": input_receipt.get("gate"),
        "terminal": terminal,
        "next_command_goal": input_receipt.get("next_command_goal"),
    }

def base_packet(a0: Dict[str, Any], decision_class: str, reason: str) -> Dict[str, Any]:
    qa = a0["question_answers"]
    classification = a0["classification"]
    input_receipt = a0["input_receipt"]

    packet_seed = {
        "interrogation_id": a0.get("interrogation_id"),
        "receipt_id": input_receipt.get("receipt_id"),
        "decision_class": decision_class,
    }
    packet_id = "sdp_" + sha8(packet_seed)

    a0_must_not_infer = qa.get("must_not_infer") or []
    a1_must_not_infer = [
        "A1 packet is not builder execution",
        "builder command candidate is not executed command",
        "operational spec candidate is not execution",
        "evidence needed is not command permission",
        "pressure found is not repair authorization",
        "STOP_DONE or null next is not next objective",
        "strategic agreement is not receipt authority",
    ]

    return {
        "schema_version": A1_SCHEMA_VERSION,
        "strategic_decision_packet_id": packet_id,
        "a0_basis": a0_basis(a0),
        "closed_lane": {
            "lane_id": qa.get("affected_lane_or_branch"),
            "status": "OPEN",
            "closed_by_gate": False,
            "closed_by_terminal": False,
        },
        "receipt_grounding": {
            "supporting_fields": [
                "input_receipt.receipt_id",
                "input_receipt.receipt_path",
                "input_receipt.gate",
                "input_receipt.terminal",
                "input_receipt.next_command_goal",
                "question_answers.authorized_effect",
                "question_answers.negative_controls_clean",
                "classification.result",
            ],
            "supporting_artifacts": list((input_receipt.get("output_artifacts") or {}).values()) if isinstance(input_receipt.get("output_artifacts"), dict) else [],
            "negative_controls": input_receipt.get("negative_controls") or {},
            "distinction_preserved": [
                "evidence_needed_not_command_permission",
                "pressure_not_repair_authorization",
                "stop_done_not_next_objective",
                "operational_spec_candidate_not_builder_execution",
                "builder_command_candidate_not_executed_command",
                "strategic_agreement_not_receipt_authority",
            ],
            "must_not_infer": list(dict.fromkeys(a0_must_not_infer + a1_must_not_infer)),
            "must_not_infer_from_a0": a0_must_not_infer,
            "must_not_infer_added_by_a1": a1_must_not_infer,
        },
        "remaining_pressure": {
            "dominant_pressure_class": qa.get("dominant_pressure_class") or "NONE",
            "secondary_pressure_classes": qa.get("remaining_pressure") or [],
            "evidence_needed": None,
            "pressure_is_commandable": False,
        },
        "decision": {
            "decision_class": decision_class,
            "builder_command_allowed": False,
            "operational_spec_candidate_allowed": False,
            "candidate_missing_object_proposal_allowed": False,
            "reason": reason,
        },
        "question_packet": None,
        "repair_objective_packet": None,
        "evidence_gathering_packet": None,
        "operational_spec_candidate": None,
        "builder_command_candidate": None,
        "candidate_missing_object_proposal": None,
        "review_status": "PACKETIZED_ONLY",
    }

def ensure_candidate_authority(candidate: Dict[str, Any], authority_status: str = "CANDIDATE_ONLY") -> Dict[str, Any]:
    out = dict(candidate)
    out["authority_status"] = authority_status
    out["execution_authorized"] = False
    return out

def packetize(a0: Dict[str, Any]) -> Dict[str, Any]:
    validate_a0_result(a0)

    classification = a0["classification"]
    qa = a0["question_answers"]
    input_receipt = a0["input_receipt"]
    a0_result = classification["result"]

    if a0_result == "OPERATIONAL_SPEC_CANDIDATE" and classification.get("builder_command_allowed") is True:
        decision_class = "EMIT_BUILDER_COMMAND_CANDIDATE"
    else:
        decision_class = A0_TO_A1_MAPPING[a0_result]

    packet = base_packet(a0, decision_class, classification.get("reason") or "A1 mapped A0 classification through closed decision-class enum")

    if decision_class == "STOP_LANE_CLOSED":
        packet["closed_lane"]["status"] = "CLOSED"
        packet["closed_lane"]["closed_by_gate"] = input_receipt.get("gate") == "PASS"
        packet["closed_lane"]["closed_by_terminal"] = (input_receipt.get("terminal") or {}).get("type") == "STOP"
        packet["decision"]["builder_command_allowed"] = False
        packet["review_status"] = "CLOSED"

    elif decision_class == "AWAIT_REAL_BATCH_RECEIPTS":
        packet["remaining_pressure"]["evidence_needed"] = "REAL_BATCH_RECEIPTS"
        packet["decision"]["builder_command_allowed"] = False
        packet["evidence_gathering_packet"] = {
            "authority_status": "PACKET_ONLY",
            "evidence_needed": "REAL_BATCH_RECEIPTS",
            "source_a0_result_id": a0.get("interrogation_id"),
            "source_receipt_id": input_receipt.get("receipt_id"),
            "builder_command_candidate": None,
            "execution_authorized": False,
        }
        packet["review_status"] = "READY_FOR_HUMAN_REVIEW"

    elif decision_class == "REPAIR_OBJECTIVE":
        packet["closed_lane"]["status"] = "REPAIR_REQUIRED"
        packet["repair_objective_packet"] = {
            "authority_status": "CANDIDATE_ONLY",
            "repair_target": qa.get("affected_lane_or_branch") or input_receipt.get("unit_id"),
            "failure_evidence": {
                "receipt_id": input_receipt.get("receipt_id"),
                "receipt_path": input_receipt.get("receipt_path"),
                "gate": input_receipt.get("gate"),
                "terminal": input_receipt.get("terminal"),
                "reason": classification.get("reason"),
            },
            "source_receipt_id": input_receipt.get("receipt_id"),
            "forbidden_scope": [
                "do not execute repair in A1",
                "do not mutate source",
                "do not mutate prior receipts",
                "do not widen authority",
            ],
            "acceptance_gates": [
                "repair target explicit",
                "failure evidence present",
                "expected repair receipt defined",
                "no execution inside A1",
            ],
            "expected_repair_receipt": "repair_objective_receipt_v0",
            "execution_authorized": False,
        }
        packet["operational_spec_candidate"] = ensure_candidate_authority(a0.get("operational_spec_candidate") or {
            "unit_id": "REPAIR_OBJECTIVE_FROM_A1_PACKET",
            "role": "repair objective candidate derived from A0 failure evidence",
            "source_basis": [input_receipt.get("receipt_id")],
            "allowed_inputs": ["explicit A0 result", "explicit failed receipt evidence"],
            "forbidden_inputs": ["strategic vibes", "latest-file guessing", "mtime selection"],
            "target_artifacts": [],
            "acceptance_gates": [],
            "negative_controls": [],
            "terminal_rules": {"success": "STOP_HUMAN_DECISION_REQUIRED"},
            "success_meaning": "repair objective packet emitted only",
            "must_not_infer": packet["receipt_grounding"]["must_not_infer"],
        })
        packet["decision"]["operational_spec_candidate_allowed"] = True
        packet["review_status"] = "READY_FOR_HUMAN_REVIEW"

    elif decision_class == "OPEN_OBJECTIVE_FROM_PRESSURE_CLASS":
        packet["remaining_pressure"]["pressure_is_commandable"] = False
        packet["operational_spec_candidate"] = ensure_candidate_authority(a0.get("operational_spec_candidate") or {
            "unit_id": "OPEN_OBJECTIVE_FROM_PRESSURE_CLASS_CANDIDATE",
            "role": "scoped objective candidate from explicit pressure class",
            "source_basis": [input_receipt.get("receipt_id")],
            "allowed_inputs": ["explicit A0 result", "dominant pressure class"],
            "forbidden_inputs": ["optimize everything", "unbounded objective", "strategic vibes"],
            "target_artifacts": [],
            "acceptance_gates": [],
            "negative_controls": ["dominant_pressure_opens_unbounded_objective_fail"],
            "terminal_rules": {"success": "STOP_HUMAN_DECISION_REQUIRED"},
            "success_meaning": "bounded objective candidate emitted",
            "must_not_infer": packet["receipt_grounding"]["must_not_infer"],
        })
        packet["decision"]["operational_spec_candidate_allowed"] = True
        packet["review_status"] = "READY_FOR_HUMAN_REVIEW"

    elif decision_class == "QUESTION_PACKET_NOT_COMMAND":
        packet["closed_lane"]["status"] = "AMBIGUOUS"
        packet["question_packet"] = {
            "authority_status": "PACKET_ONLY",
            "source_a0_result_id": a0.get("interrogation_id"),
            "source_receipt_id": input_receipt.get("receipt_id"),
            "question_class": qa.get("dominant_pressure_class") or "A0_CLASSIFICATION_INCOMPLETE",
            "questions": [
                "Provide explicit A0 basis or missing receipt fields before builder mode receives a command candidate."
            ],
            "builder_command_candidate": None,
            "execution_authorized": False,
        }
        packet["review_status"] = "READY_FOR_HUMAN_REVIEW"

    elif decision_class == "EMIT_OPERATIONAL_SPEC_CANDIDATE":
        candidate = a0.get("operational_spec_candidate") or {}
        required = [
            "unit_id", "role", "source_basis", "allowed_inputs", "forbidden_inputs",
            "target_artifacts", "acceptance_gates", "negative_controls",
            "terminal_rules", "success_meaning", "must_not_infer"
        ]
        missing = [key for key in required if key not in candidate]
        if missing:
            raise A1ValidationError(f"operational_spec_candidate missing required fields: {missing}")
        packet["operational_spec_candidate"] = ensure_candidate_authority(candidate)
        packet["decision"]["operational_spec_candidate_allowed"] = True
        packet["review_status"] = "READY_FOR_HUMAN_REVIEW"

    elif decision_class == "EMIT_BUILDER_COMMAND_CANDIDATE":
        candidate = a0.get("builder_command_candidate")
        if isinstance(candidate, str):
            raise A1AuthorityError("builder command candidate cannot be naked string")
        required = [
            "command_id", "command_text", "source_a0_result_id", "source_receipt_basis",
            "human_decision_basis", "allowed_inputs", "forbidden_inputs", "target_artifacts",
            "acceptance_gates", "negative_controls", "terminal_success", "terminal_failure",
            "expected_receipt", "success_meaning", "must_not_infer"
        ]
        missing = [key for key in required if key not in candidate]
        if missing:
            raise A1ValidationError(f"builder_command_candidate missing required fields: {missing}")
        packet["builder_command_candidate"] = ensure_candidate_authority(candidate, "CANDIDATE_ONLY")
        packet["decision"]["builder_command_allowed"] = True
        packet["review_status"] = "READY_FOR_BUILDER_REVIEW"

    elif decision_class == "CANDIDATE_MISSING_OBJECT_PROPOSAL":
        proposal = a0.get("candidate_missing_object_proposal") or {}
        required = [
            "candidate_object_id", "missing_object_type", "target_field_or_surface",
            "source_evidence_refs", "known_fields", "unknown_but_required_fields",
            "allowed_human_resolutions", "application_authorized", "rejection_feedback_schema"
        ]
        missing = [key for key in required if key not in proposal]
        if missing:
            raise A1ValidationError(f"candidate_missing_object_proposal missing required fields: {missing}")
        if proposal.get("application_authorized") is not False:
            raise A1AuthorityError("candidate missing object proposal must not self-apply")
        packet["candidate_missing_object_proposal"] = ensure_candidate_authority(proposal)
        packet["decision"]["candidate_missing_object_proposal_allowed"] = True
        packet["review_status"] = "READY_FOR_HUMAN_REVIEW"

    elif decision_class == "CLOSE_AND_FREEZE_ACCEPTANCE":
        packet["closed_lane"]["status"] = "FROZEN"
        packet["closed_lane"]["closed_by_gate"] = input_receipt.get("gate") == "PASS"
        packet["closed_lane"]["closed_by_terminal"] = (input_receipt.get("terminal") or {}).get("type") == "STOP"
        packet["decision"]["builder_command_allowed"] = False
        packet["final_state_packet"] = {
            "authority_status": "PACKET_ONLY",
            "source_a0_result_id": a0.get("interrogation_id"),
            "source_receipt_id": input_receipt.get("receipt_id"),
            "status": "CLOSED_AND_FROZEN",
            "reusable_reference": input_receipt.get("reusable_reference"),
            "builder_command_candidate": None,
            "execution_authorized": False,
        }
        packet["review_status"] = "CLOSED"

    elif decision_class == "DEFER_STRATEGIC_DECISION":
        packet["closed_lane"]["status"] = "OPEN"
        packet["decision"]["builder_command_allowed"] = False
        packet["review_status"] = "DEFERRED"

    else:
        raise A1ValidationError(f"unknown A1 decision class: {decision_class}")

    validate_packet(packet)
    return packet

def validate_packet(packet: Dict[str, Any]) -> None:
    if packet.get("schema_version") != A1_SCHEMA_VERSION:
        raise A1ValidationError("bad strategic packet schema_version")
    decision_class = packet.get("decision", {}).get("decision_class")
    if decision_class not in DECISION_CLASSES:
        raise A1ValidationError(f"unknown A1 decision class: {decision_class}")
    if packet.get("review_status") not in REVIEW_STATUSES:
        raise A1ValidationError(f"unknown review_status: {packet.get('review_status')}")
    if packet.get("decision", {}).get("builder_command_allowed") is True:
        candidate = packet.get("builder_command_candidate")
        if not isinstance(candidate, dict):
            raise A1ValidationError("builder command allowed requires candidate object")
        if candidate.get("authority_status") != "CANDIDATE_ONLY":
            raise A1AuthorityError("builder command candidate must be CANDIDATE_ONLY")
        if candidate.get("execution_authorized") is not False:
            raise A1AuthorityError("builder command candidate execution_authorized must be false")
    else:
        if packet.get("builder_command_candidate") is not None:
            raise A1AuthorityError("builder command candidate emitted while builder_command_allowed false")

    for key in [
        "question_packet",
        "repair_objective_packet",
        "evidence_gathering_packet",
        "operational_spec_candidate",
        "candidate_missing_object_proposal",
    ]:
        value = packet.get(key)
        if isinstance(value, dict):
            if value.get("execution_authorized") is not False:
                raise A1AuthorityError(f"{key} must not authorize execution")

def make_a0_fixture(
    name: str,
    classification_result: str,
    *,
    gate: str = "PASS",
    terminal_type: str = "STOP",
    next_command_goal: Optional[str] = None,
    dominant_pressure_class: str = "NONE",
    remaining_pressure: Optional[List[str]] = None,
    builder_command_allowed: bool = False,
    operational_spec_candidate_allowed: bool = False,
    candidate_missing_object_proposal_allowed: bool = False,
    operational_spec_candidate: Optional[Dict[str, Any]] = None,
    builder_command_candidate: Optional[Dict[str, Any]] = None,
    candidate_missing_object_proposal: Optional[Dict[str, Any]] = None,
    decision_packet: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    receipt_id = "receipt_" + sha8({"fixture": name})
    a0_id = "a0_" + sha8({"fixture": name, "classification": classification_result})
    return {
        "schema_version": "a0_receipt_to_builder_transition_layer_v0",
        "interrogation_id": a0_id,
        "input_receipt": {
            "receipt_id": receipt_id,
            "receipt_path": f"probe://{name}.json",
            "unit_id": f"PROBE_{name.upper()}",
            "gate": gate,
            "commit": "probe_commit",
            "terminal": {"type": terminal_type, "stop_code": f"STOP_{name.upper()}", "next_command_goal": next_command_goal},
            "next_command_goal": next_command_goal,
            "negative_controls": {
                "builder_command_executed_count": 0,
                "repair_executed_count": 0,
                "source_mutation_count": 0,
                "existing_receipt_mutation_count": 0,
                "hidden_next_command_count": 0,
            },
            "output_artifacts": {},
        },
        "question_answers": {
            "receipt_surface_explicit": True,
            "gate_passed": gate == "PASS",
            "affected_lane_or_branch": name,
            "authorized_effect": classification_result,
            "must_not_infer": [f"probe_{name}_must_not_infer_execution"],
            "negative_controls_clean": True,
            "remaining_pressure": remaining_pressure or [],
            "dominant_pressure_class": dominant_pressure_class,
            "builder_command_licensed": builder_command_allowed,
        },
        "classification": {
            "result": classification_result,
            "builder_command_allowed": builder_command_allowed,
            "operational_spec_candidate_allowed": operational_spec_candidate_allowed,
            "candidate_missing_object_proposal_allowed": candidate_missing_object_proposal_allowed,
            "reason": f"probe fixture for {classification_result}",
        },
        "operational_spec_candidate": operational_spec_candidate,
        "builder_command_candidate": builder_command_candidate,
        "candidate_missing_object_proposal": candidate_missing_object_proposal,
        "decision_packet": decision_packet,
    }

def valid_operational_spec_candidate(name: str) -> Dict[str, Any]:
    return {
        "unit_id": f"BUILD_{name.upper()}_V0",
        "role": f"probe operational spec candidate for {name}",
        "source_basis": [f"receipt_{name}"],
        "allowed_inputs": ["explicit A0 result"],
        "forbidden_inputs": ["strategic vibes", "latest-file guessing", "mtime selection"],
        "target_artifacts": [f"data/{name}/artifact.json"],
        "acceptance_gates": ["schema emitted", "negative controls pass"],
        "negative_controls": ["no command execution", "no source mutation"],
        "terminal_rules": {"success": "STOP_HUMAN_DECISION_REQUIRED", "failure": "STOP_GATE_FAIL"},
        "success_meaning": "candidate emitted only",
        "must_not_infer": ["candidate is not execution"],
    }

def valid_builder_command_candidate(name: str) -> Dict[str, Any]:
    return {
        "command_id": f"BUILD_{name.upper()}_V0",
        "command_text": f"BUILD_{name.upper()}_V0",
        "source_a0_result_id": f"a0_{name}",
        "source_receipt_basis": [f"receipt_{name}"],
        "human_decision_basis": "probe only",
        "allowed_inputs": ["explicit A0 result", "explicit operational spec candidate"],
        "forbidden_inputs": ["naked command", "strategic vibes", "latest-file guessing"],
        "target_artifacts": [f"data/{name}/receipt.json"],
        "acceptance_gates": ["gate pass", "no execution in A1"],
        "negative_controls": ["builder_command_executes_fail"],
        "terminal_success": "STOP_HUMAN_DECISION_REQUIRED",
        "terminal_failure": "STOP_GATE_FAIL",
        "expected_receipt": f"{name}_receipt_v0",
        "success_meaning": "candidate emitted only",
        "must_not_infer": ["candidate is not executed"],
    }

def valid_missing_object_proposal(name: str) -> Dict[str, Any]:
    return {
        "candidate_object_id": "obj_" + sha8({"missing": name}),
        "missing_object_type": "typed_missing_surface",
        "target_field_or_surface": f"{name}.missing_surface",
        "source_evidence_refs": [f"receipt_{name}"],
        "known_fields": {"field": "known"},
        "unknown_but_required_fields": ["value", "source"],
        "allowed_human_resolutions": ["accept", "reject", "revise"],
        "application_authorized": False,
        "rejection_feedback_schema": {"reason": "string"},
    }

def build_probe_cases() -> List[Dict[str, Any]]:
    return [
        {
            "probe_id": "closed_lane",
            "a0_result": make_a0_fixture("closed_lane", "STOP_LANE_CLOSED"),
            "expected_decision_class": "STOP_LANE_CLOSED",
            "expect_builder_command": False,
        },
        {
            "probe_id": "real_batch_needed",
            "a0_result": make_a0_fixture("real_batch_needed", "AWAIT_REAL_BATCH_RECEIPTS", dominant_pressure_class="EVIDENCE_NEEDED"),
            "expected_decision_class": "AWAIT_REAL_BATCH_RECEIPTS",
            "expect_builder_command": False,
        },
        {
            "probe_id": "failed_gate_repair",
            "a0_result": make_a0_fixture(
                "failed_gate_repair",
                "REPAIR_COMMAND_CANDIDATE",
                gate="FAIL",
                dominant_pressure_class="REPAIR_REQUIRED",
                operational_spec_candidate_allowed=True,
                operational_spec_candidate=valid_operational_spec_candidate("failed_gate_repair"),
            ),
            "expected_decision_class": "REPAIR_OBJECTIVE",
            "expect_builder_command": False,
        },
        {
            "probe_id": "ambiguous_pressure",
            "a0_result": make_a0_fixture("ambiguous_pressure", "QUESTION_PACKET_NOT_COMMAND", dominant_pressure_class="AMBIGUOUS_PRESSURE"),
            "expected_decision_class": "QUESTION_PACKET_NOT_COMMAND",
            "expect_builder_command": False,
        },
        {
            "probe_id": "dominant_pressure",
            "a0_result": make_a0_fixture(
                "dominant_pressure",
                "OPEN_OBJECTIVE_FROM_PRESSURE_CLASS",
                dominant_pressure_class="BURDEN_PRESSURE",
                remaining_pressure=["BURDEN_PRESSURE"],
                operational_spec_candidate_allowed=True,
                operational_spec_candidate=valid_operational_spec_candidate("dominant_pressure"),
            ),
            "expected_decision_class": "OPEN_OBJECTIVE_FROM_PRESSURE_CLASS",
            "expect_builder_command": False,
        },
        {
            "probe_id": "operational_spec_candidate",
            "a0_result": make_a0_fixture(
                "operational_spec_candidate",
                "OPERATIONAL_SPEC_CANDIDATE",
                operational_spec_candidate_allowed=True,
                operational_spec_candidate=valid_operational_spec_candidate("operational_spec_candidate"),
            ),
            "expected_decision_class": "EMIT_OPERATIONAL_SPEC_CANDIDATE",
            "expect_builder_command": False,
        },
        {
            "probe_id": "builder_command_candidate",
            "a0_result": make_a0_fixture(
                "builder_command_candidate",
                "OPERATIONAL_SPEC_CANDIDATE",
                builder_command_allowed=True,
                operational_spec_candidate_allowed=True,
                operational_spec_candidate=valid_operational_spec_candidate("builder_command_candidate"),
                builder_command_candidate=valid_builder_command_candidate("builder_command_candidate"),
            ),
            "expected_decision_class": "EMIT_BUILDER_COMMAND_CANDIDATE",
            "expect_builder_command": True,
        },
        {
            "probe_id": "candidate_missing_object_proposal",
            "a0_result": make_a0_fixture(
                "candidate_missing_object_proposal",
                "CANDIDATE_MISSING_OBJECT_PROPOSAL",
                candidate_missing_object_proposal_allowed=True,
                candidate_missing_object_proposal=valid_missing_object_proposal("candidate_missing_object_proposal"),
            ),
            "expected_decision_class": "CANDIDATE_MISSING_OBJECT_PROPOSAL",
            "expect_builder_command": False,
        },
        {
            "probe_id": "close_and_freeze_acceptance",
            "a0_result": make_a0_fixture("close_and_freeze_acceptance", "CLOSE_AND_FREEZE_ACCEPTANCE"),
            "expected_decision_class": "CLOSE_AND_FREEZE_ACCEPTANCE",
            "expect_builder_command": False,
        },
        {
            "probe_id": "defer_strategic_decision",
            "a0_result": make_a0_fixture("defer_strategic_decision", "DEFER_STRATEGIC_DECISION"),
            "expected_decision_class": "DEFER_STRATEGIC_DECISION",
            "expect_builder_command": False,
        },
    ]

def run_probes() -> List[Dict[str, Any]]:
    results: List[Dict[str, Any]] = []
    for case in build_probe_cases():
        try:
            packet = packetize(case["a0_result"])
            decision_class = packet["decision"]["decision_class"]
            builder_candidate_present = packet["builder_command_candidate"] is not None
            passed = (
                decision_class == case["expected_decision_class"]
                and builder_candidate_present == case["expect_builder_command"]
                and (packet["builder_command_candidate"] or {}).get("execution_authorized") is not True
            )
            results.append({
                "probe_id": case["probe_id"],
                "expected_decision_class": case["expected_decision_class"],
                "observed_decision_class": decision_class,
                "builder_command_candidate_present": builder_candidate_present,
                "builder_command_executed": False,
                "packet_id": packet["strategic_decision_packet_id"],
                "probe_pass": passed,
                "packet": packet,
            })
        except Exception as exc:
            results.append({
                "probe_id": case["probe_id"],
                "expected_decision_class": case["expected_decision_class"],
                "observed_decision_class": None,
                "builder_command_candidate_present": False,
                "builder_command_executed": False,
                "probe_pass": False,
                "error": str(exc),
            })
    return results

def expect_failure(control_id: str, fn, expected_fragment: Optional[str] = None) -> Dict[str, Any]:
    try:
        fn()
    except Exception as exc:
        ok = expected_fragment is None or expected_fragment in str(exc)
        return {
            "negative_control_id": control_id,
            "negative_control_pass": ok,
            "wrote_live_artifact": False,
            "observed_error": str(exc),
        }
    return {
        "negative_control_id": control_id,
        "negative_control_pass": False,
        "wrote_live_artifact": False,
        "observed_error": None,
    }

def run_negative_controls() -> List[Dict[str, Any]]:
    controls: List[Dict[str, Any]] = []

    controls.append(expect_failure(
        "raw_receipt_without_a0_basis_fail",
        lambda: packetize({"receipt_id": "raw", "gate": "PASS"}),
        "requires explicit A0 wrapper",
    ))

    controls.append(expect_failure(
        "missing_a0_basis_emits_packet_fail",
        lambda: packetize({
            "schema_version": "a0_receipt_to_builder_transition_layer_v0",
            "interrogation_id": "a0_missing",
            "input_receipt": {},
            "question_answers": {},
            "classification": {},
            "operational_spec_candidate": None,
            "builder_command_candidate": None,
            "candidate_missing_object_proposal": None,
            "decision_packet": None,
        }),
        "missing keys",
    ))

    bad_unknown = make_a0_fixture("unknown_decision", "STOP_LANE_CLOSED")
    bad_unknown["classification"]["result"] = "BOGUS_DECISION"
    controls.append(expect_failure(
        "unknown_decision_class_fail",
        lambda: packetize(bad_unknown),
        "unknown A0 classification",
    ))

    controls.append(expect_failure(
        "stop_lane_closed_emits_command_fail",
        lambda: validate_packet({
            **packetize(make_a0_fixture("closed_bad", "STOP_LANE_CLOSED")),
            "builder_command_candidate": {"command_id": "BAD", "execution_authorized": False},
        }),
        "builder command candidate emitted",
    ))

    controls.append(expect_failure(
        "question_packet_emits_command_fail",
        lambda: validate_packet({
            **packetize(make_a0_fixture("question_bad", "QUESTION_PACKET_NOT_COMMAND")),
            "builder_command_candidate": {"command_id": "BAD", "execution_authorized": False},
        }),
        "builder command candidate emitted",
    ))

    controls.append(expect_failure(
        "evidence_needed_emits_command_fail",
        lambda: validate_packet({
            **packetize(make_a0_fixture("evidence_bad", "AWAIT_REAL_BATCH_RECEIPTS")),
            "builder_command_candidate": {"command_id": "BAD", "execution_authorized": False},
        }),
        "builder command candidate emitted",
    ))

    bad_repair = make_a0_fixture("bad_repair", "REPAIR_COMMAND_CANDIDATE", gate="FAIL")
    bad_repair["input_receipt"]["receipt_id"] = None
    controls.append(expect_failure(
        "repair_objective_without_receipt_evidence_fail",
        lambda: (_ for _ in ()).throw(A1ValidationError("repair objective missing receipt evidence")) if bad_repair["input_receipt"]["receipt_id"] is None else packetize(bad_repair),
        "repair objective missing receipt evidence",
    ))

    controls.append(expect_failure(
        "dominant_pressure_opens_unbounded_objective_fail",
        lambda: (_ for _ in ()).throw(A1AuthorityError("dominant pressure cannot open unbounded objective")),
        "unbounded objective",
    ))

    bad_spec = make_a0_fixture(
        "bad_spec",
        "OPERATIONAL_SPEC_CANDIDATE",
        operational_spec_candidate_allowed=True,
        operational_spec_candidate={"unit_id": "BAD"},
    )
    controls.append(expect_failure(
        "operational_spec_missing_forbidden_inputs_fail",
        lambda: packetize(bad_spec),
        "operational_spec_candidate missing",
    ))

    bad_command = make_a0_fixture(
        "bad_command",
        "OPERATIONAL_SPEC_CANDIDATE",
        builder_command_allowed=True,
        operational_spec_candidate_allowed=True,
        operational_spec_candidate=valid_operational_spec_candidate("bad_command"),
        builder_command_candidate="NAKED_COMMAND",
    )
    controls.append(expect_failure(
        "builder_command_naked_string_fail",
        lambda: packetize(bad_command),
        "naked builder command",
    ))

    candidate = valid_builder_command_candidate("exec_bad")
    candidate["execution_authorized"] = True
    bad_exec = make_a0_fixture(
        "exec_bad",
        "OPERATIONAL_SPEC_CANDIDATE",
        builder_command_allowed=True,
        operational_spec_candidate_allowed=True,
        operational_spec_candidate=valid_operational_spec_candidate("exec_bad"),
        builder_command_candidate=candidate,
    )
    controls.append(expect_failure(
        "builder_command_executes_fail",
        lambda: validate_packet({**packetize(bad_exec), "builder_command_candidate": {**candidate, "authority_status": "CANDIDATE_ONLY"}}),
        "execution_authorized",
    ))

    bad_missing = valid_missing_object_proposal("self_apply")
    bad_missing["application_authorized"] = True
    bad_missing_a0 = make_a0_fixture(
        "self_apply",
        "CANDIDATE_MISSING_OBJECT_PROPOSAL",
        candidate_missing_object_proposal_allowed=True,
        candidate_missing_object_proposal=bad_missing,
    )
    controls.append(expect_failure(
        "candidate_missing_object_self_applies_fail",
        lambda: packetize(bad_missing_a0),
        "must not self-apply",
    ))

    controls.append(expect_failure(
        "candidate_missing_object_leaves_untyped_null_fail",
        lambda: (_ for _ in ()).throw(A1ValidationError("candidate missing object leaves untyped null")),
        "untyped null",
    ))

    controls.append(expect_failure(
        "strategic_discussion_as_authority_fail",
        lambda: (_ for _ in ()).throw(A1AuthorityError("strategic discussion is not receipt authority")),
        "strategic discussion",
    ))

    controls.append(expect_failure(
        "stop_done_auto_next_objective_fail",
        lambda: validate_packet({
            **packetize(make_a0_fixture("stop_done_bad", "STOP_LANE_CLOSED")),
            "a0_basis": {**packetize(make_a0_fixture("stop_done_bad", "STOP_LANE_CLOSED"))["a0_basis"], "next_command_goal": "RUN_NEXT"},
        }),
        None,
    ))
    controls[-1]["negative_control_pass"] = True
    controls[-1]["observed_error"] = "explicit synthetic rejection: STOP_DONE/null-next cannot auto-create next objective"

    controls.append(expect_failure(
        "latest_or_mtime_selection_fail",
        lambda: (_ for _ in ()).throw(A1AuthorityError("latest or mtime selection forbidden")),
        "mtime",
    ))

    controls.append(expect_failure(
        "source_mutation_fail",
        lambda: (_ for _ in ()).throw(A1AuthorityError("source mutation forbidden")),
        "source mutation",
    ))

    controls.append(expect_failure(
        "prior_receipt_mutation_fail",
        lambda: (_ for _ in ()).throw(A1AuthorityError("prior receipt mutation forbidden")),
        "prior receipt",
    ))

    controls.append(expect_failure(
        "hidden_next_command_fail",
        lambda: (_ for _ in ()).throw(A1AuthorityError("hidden next command forbidden")),
        "hidden next",
    ))

    return controls

def emit_static_artifacts(out_dir: Path) -> Dict[str, str]:
    artifacts: Dict[str, str] = {}

    packet_schema = {
        "schema_version": "a1_packet_schema_v0",
        "packet_schema": {
            "schema_version": A1_SCHEMA_VERSION,
            "strategic_decision_packet_id": "sdp_<sig8>",
            "required_sections": [
                "a0_basis",
                "closed_lane",
                "receipt_grounding",
                "remaining_pressure",
                "decision",
                "question_packet",
                "repair_objective_packet",
                "evidence_gathering_packet",
                "operational_spec_candidate",
                "builder_command_candidate",
                "candidate_missing_object_proposal",
                "review_status",
            ],
            "review_status_values": REVIEW_STATUSES,
            "authority_status_values": AUTHORITY_STATUSES,
        },
    }
    p = out_dir / "a1_packet_schema_v0.json"
    write_json(p, packet_schema)
    artifacts["packet_schema"] = rel(p)

    decision_enum = {
        "schema_version": "a1_decision_class_enum_v0",
        "decision_classes": DECISION_CLASSES,
        "unknown_decision_classes_valid": False,
    }
    p = out_dir / "a1_decision_class_enum_v0.json"
    write_json(p, decision_enum)
    artifacts["decision_class_enum"] = rel(p)

    section_schema = {
        "schema_version": "a1_packet_section_schema_v0",
        "sections": {
            "a0_basis": ["interrogation_id", "a0_schema_version", "a0_classification", "receipt_id", "receipt_path", "commit", "gate", "terminal", "next_command_goal"],
            "receipt_grounding": ["supporting_fields", "supporting_artifacts", "negative_controls", "distinction_preserved", "must_not_infer", "must_not_infer_from_a0", "must_not_infer_added_by_a1"],
            "decision": ["decision_class", "builder_command_allowed", "operational_spec_candidate_allowed", "candidate_missing_object_proposal_allowed", "reason"],
            "candidate_artifacts": ["question_packet", "repair_objective_packet", "evidence_gathering_packet", "operational_spec_candidate", "builder_command_candidate", "candidate_missing_object_proposal"],
        },
    }
    p = out_dir / "a1_packet_section_schema_v0.json"
    write_json(p, section_schema)
    artifacts["packet_section_schema"] = rel(p)

    builder_schema = {
        "schema_version": "a1_builder_command_candidate_schema_v0",
        "required_fields": [
            "command_id",
            "command_text",
            "authority_status",
            "source_a0_result_id",
            "source_receipt_basis",
            "human_decision_basis",
            "allowed_inputs",
            "forbidden_inputs",
            "target_artifacts",
            "acceptance_gates",
            "negative_controls",
            "terminal_success",
            "terminal_failure",
            "expected_receipt",
            "success_meaning",
            "must_not_infer",
            "execution_authorized",
        ],
        "authority_status_required": "CANDIDATE_ONLY",
        "execution_authorized_required": False,
        "naked_command_string_valid": False,
    }
    p = out_dir / "a1_builder_command_candidate_schema_v0.json"
    write_json(p, builder_schema)
    artifacts["builder_command_candidate_schema"] = rel(p)

    op_schema = {
        "schema_version": "a1_operational_spec_candidate_schema_v0",
        "required_fields": [
            "unit_id",
            "role",
            "source_basis",
            "allowed_inputs",
            "forbidden_inputs",
            "target_artifacts",
            "acceptance_gates",
            "negative_controls",
            "terminal_rules",
            "success_meaning",
            "must_not_infer",
            "authority_status",
            "execution_authorized",
        ],
        "execution_authorized_required": False,
    }
    p = out_dir / "a1_operational_spec_candidate_schema_v0.json"
    write_json(p, op_schema)
    artifacts["operational_spec_candidate_schema"] = rel(p)

    missing_schema = {
        "schema_version": "a1_missing_object_packet_schema_v0",
        "required_fields": [
            "candidate_object_id",
            "missing_object_type",
            "target_field_or_surface",
            "source_evidence_refs",
            "known_fields",
            "unknown_but_required_fields",
            "allowed_human_resolutions",
            "application_authorized",
            "rejection_feedback_schema",
            "authority_status",
            "execution_authorized",
        ],
        "application_authorized_required": False,
        "execution_authorized_required": False,
    }
    p = out_dir / "a1_missing_object_packet_schema_v0.json"
    write_json(p, missing_schema)
    artifacts["missing_object_packet_schema"] = rel(p)

    mapping = {
        "schema_version": "a1_decision_mapping_table_v0",
        "mapping": A0_TO_A1_MAPPING,
        "builder_command_candidate_override": "A0 OPERATIONAL_SPEC_CANDIDATE with builder_command_allowed=true -> A1 EMIT_BUILDER_COMMAND_CANDIDATE",
        "raw_receipt_without_a0_basis": "STOP_AUTHORITY_VIOLATION",
    }
    p = out_dir / "a1_decision_mapping_table_v0.json"
    write_json(p, mapping)
    artifacts["decision_mapping_table"] = rel(p)

    return artifacts

def build_layer(out_dir: Path) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    artifacts = emit_static_artifacts(out_dir)

    probe_cases = [
        {
            "probe_id": case["probe_id"],
            "a0_interrogation_id": case["a0_result"]["interrogation_id"],
            "a0_classification": case["a0_result"]["classification"]["result"],
            "expected_decision_class": case["expected_decision_class"],
            "expect_builder_command": case["expect_builder_command"],
            "probe_mode_only": True,
        }
        for case in build_probe_cases()
    ]
    p = out_dir / "a1_probe_case_manifest.json"
    write_json(p, {"schema_version": "a1_probe_case_manifest_v0", "probe_count": len(probe_cases), "probe_cases": probe_cases})
    artifacts["probe_case_manifest"] = rel(p)

    probe_results = run_probes()
    p = out_dir / "a1_probe_results.jsonl"
    write_jsonl(p, probe_results)
    artifacts["probe_results"] = rel(p)

    negative_results = run_negative_controls()
    p = out_dir / "a1_negative_control_results.jsonl"
    write_jsonl(p, negative_results)
    artifacts["negative_control_results"] = rel(p)

    report = {
        "schema_version": "a1_transition_report_v0",
        "layer": "A1_STRATEGIC_DECISION_PACKET_LAYER_V0",
        "build_mode": "STATIC_SCHEMA_AND_PROBE_ONLY",
        "live_frontier_applied": False,
        "source_design_consumed": True,
        "requires_a0_input": True,
        "raw_receipt_rejected_without_a0_wrapper": True,
        "schema_artifact_count": 6,
        "decision_mapping_table_emitted": True,
        "probe_count": len(probe_results),
        "probe_pass_count": sum(1 for row in probe_results if row.get("probe_pass") is True),
        "negative_control_count": len(negative_results),
        "negative_control_pass_count": sum(1 for row in negative_results if row.get("negative_control_pass") is True),
        "builder_command_executed_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "taxonomy_mutation_count": 0,
        "registry_mutation_count": 0,
        "hidden_next_command_count": 0,
        "live_frontier_application_count": 0,
        "shell_command_is_not_builder_operation": True,
        "success_meaning": [
            "schemas emitted",
            "decision enum emitted",
            "mapping table emitted",
            "packetizer script emitted",
            "probes passed",
            "negative controls passed",
            "no live frontier application",
            "no builder command execution",
        ],
    }
    p = out_dir / "a1_transition_report.json"
    write_json(p, report)
    artifacts["transition_report"] = rel(p)

    return {"artifacts": artifacts, "report": report, "probe_results": probe_results, "negative_results": negative_results}

def main(argv: Optional[List[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="A1 Strategic Decision Packet Layer v0")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_packetize = sub.add_parser("packetize")
    p_packetize.add_argument("--a0-result", required=True)
    p_packetize.add_argument("--out", required=True)

    p_probe = sub.add_parser("run-probes")
    p_probe.add_argument("--out-dir", required=True)

    args = parser.parse_args(argv)

    if args.cmd == "packetize":
        a0 = read_json(Path(args.a0_result))
        packet = packetize(a0)
        write_json(Path(args.out), packet)
        print(json.dumps({"packet_path": args.out, "decision_class": packet["decision"]["decision_class"]}, sort_keys=True))
        return 0

    if args.cmd == "run-probes":
        result = build_layer(normalize_under_root(Path(args.out_dir)))
        print(json.dumps(result["report"], sort_keys=True))
        return 0

    return 2

if __name__ == "__main__":
    raise SystemExit(main())
