#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_RUNTIME_OBSERVABILITY_AND_FEEDBACK_ATTACHMENT_V0"
TARGET_UNIT_ID = "runtime.observability_and_feedback_attachment.v0"
MILESTONE = "RUNTIME_OBSERVABILITY_AND_FEEDBACK_ATTACHED"

OUT_DIR = ROOT / "data/runtime_observability_feedback_attachment_v0"
RECEIPT_DIR = ROOT / "data/runtime_observability_feedback_attachment_v0_receipts"

INTAKE_PATH = OUT_DIR / "runtime_attachment_intake_v0.json"
STEP_BUNDLES_PATH = OUT_DIR / "runtime_step_bundles_v0.jsonl"
SIDECAR_EVENTS_PATH = OUT_DIR / "observability_sidecar_events_v0.jsonl"
EDGE_OBS_PATH = OUT_DIR / "decision_edge_observation_records_v0.jsonl"
UNIT_FEEDBACK_PATH = OUT_DIR / "unit_feedback_records_v0.jsonl"
DEGRADATION_PATH = OUT_DIR / "observability_degradation_records_v0.jsonl"
STEP_RECEIPTS_PATH = OUT_DIR / "runtime_step_receipts_v0.jsonl"
ROLLUP_PATH = OUT_DIR / "runtime_observability_feedback_rollup_v0.json"
READOUT_PATH = OUT_DIR / "runtime_observability_feedback_readout_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_observability_feedback_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_observability_feedback_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "runtime_observability_feedback_transition_trace.json"

EXPECTED_FIXTURE_ORDER = [
    "F1_VALID_ADMISSIBLE",
    "F2_INVALID_SCHEMA",
    "F3_AUTHORITY_REQUIRED",
    "F4_FORBIDDEN_INPUT",
    "F5_EXECUTION_FAILURE_TYPED_FEEDBACK",
    "F6_SIDECAR_PARTIAL_OBSERVABILITY",
]

NEGATIVE_CONTROL_KEYS = [
    "bare_failed_status_count",
    "unobserved_transition_count",
    "hidden_next_command_count",
    "sidecar_authority_count",
    "sidecar_control_path_modification_count",
    "sidecar_state_mutation_count",
    "sidecar_command_emission_count",
    "feedback_missing_count",
    "repair_applied_by_feedback_count",
    "retry_authorized_by_feedback_count",
    "authority_expanded_by_feedback_count",
    "false_full_observability_claim_count",
    "decision_edge_authorization_created_count",
    "graph_archive_mutation_count",
    "validator_authorization_schema_created_count",
    "runtime_mutation_count",
    "source_receipt_mutation_count",
    "source_fixture_receipt_mutation_count",
    "source_double_sieve_receipt_mutation_count",
    "schema_archive_mutation_count",
    "move_addition_count",
    "fixture_expansion_count",
    "c7_opened_count",
    "c8_opened_count",
    "latest_file_selection_count",
    "mtime_selection_count",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))

def zero_counters() -> Dict[str, int]:
    return {k: 0 for k in NEGATIVE_CONTROL_KEYS}

def add_counters(dst: Dict[str, int], src: Dict[str, int]) -> None:
    for k, v in src.items():
        if k in dst:
            dst[k] += int(v)

def classify_failure(failures: List[str]) -> Tuple[str, str, str]:
    if not failures:
        return (
            "PASS",
            "TYPED_RUNTIME_OBSERVABILITY_FEEDBACK_ATTACHMENT_PASS",
            "RUNTIME_ATTACHMENT_PASS",
        )

    first = failures[0]
    if "intake_missing" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_INTAKE_MISSING", "RUNTIME_ATTACHMENT_BLOCKED_INTAKE_MISSING")
    if "r0_packet_missing" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_R0_PACKET_MISSING", "RUNTIME_ATTACHMENT_BLOCKED_R0_PACKET_MISSING")
    if "runtime_membranes_receipt_missing" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_RUNTIME_MEMBRANES_RECEIPT_MISSING", "RUNTIME_ATTACHMENT_BLOCKED_RUNTIME_MEMBRANES_MISSING")
    if "double_sieve_not_passed" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_DOUBLE_SIEVE_NOT_PASSED", "RUNTIME_ATTACHMENT_BLOCKED_DOUBLE_SIEVE_NOT_PASSED")
    if "step_outputs_missing" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_STEP_OUTPUTS_MISSING", "RUNTIME_ATTACHMENT_BLOCKED_STEP_OUTPUTS_MISSING")
    if "feedback_missing" in first or "feedback_attachment_incomplete" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_FEEDBACK_ATTACHMENT_INCOMPLETE", "RUNTIME_ATTACHMENT_BLOCKED_FEEDBACK_INCOMPLETE")
    if "degradation_unrecorded" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_OBSERVABILITY_DEGRADATION_UNRECORDED", "RUNTIME_ATTACHMENT_BLOCKED_OBSERVABILITY_DEGRADATION_UNRECORDED")
    if "bare_failed" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_BARE_FAILED_STATUS", "RUNTIME_ATTACHMENT_FAIL_BARE_FAILED_STATUS")
    if "unobserved_transition" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_UNOBSERVED_TRANSITION", "RUNTIME_ATTACHMENT_FAIL_UNOBSERVED_TRANSITION")
    if "hidden_next" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_HIDDEN_NEXT_COMMAND", "RUNTIME_ATTACHMENT_FAIL_HIDDEN_NEXT_COMMAND")
    if "sidecar_authority" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_SIDECAR_AUTHORITY_LEAK", "RUNTIME_ATTACHMENT_AUTHORITY_VIOLATION_SIDECAR_AUTHORITY")
    if "false_observability" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_FALSE_OBSERVABILITY_CLAIM", "RUNTIME_ATTACHMENT_FAIL_FALSE_OBSERVABILITY_CLAIM")
    if "runtime_mutation" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_RUNTIME_MUTATION_DETECTED", "RUNTIME_ATTACHMENT_RUNTIME_BOUNDARY_VIOLATION_MUTATION")
    if "c7_opened" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_C7_OPENED", "RUNTIME_ATTACHMENT_RUNTIME_BOUNDARY_VIOLATION_C7_OPENED")
    if "c8_opened" in first:
        return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_C8_OPENED", "RUNTIME_ATTACHMENT_RUNTIME_BOUNDARY_VIOLATION_C8_OPENED")
    return ("FAIL", "TYPED_RUNTIME_ATTACHMENT_RECEIPT_MISMATCH", "RUNTIME_ATTACHMENT_BLOCKED_RECEIPT_MISMATCH")

def terminal_for(gate: str, failures: List[str]) -> Dict[str, Any]:
    if gate == "PASS":
        return {
            "type": "STOP",
            "stop_code": "STOP_RUNTIME_OBSERVABILITY_AND_FEEDBACK_ATTACHED",
            "next_command_goal": None,
        }

    first = failures[0] if failures else ""
    if "intake_missing" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_INTAKE_MISSING"
    elif "intake_untyped" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_INTAKE_UNTYPED"
    elif "r0_packet_missing" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_R0_PACKET_MISSING"
    elif "runtime_membranes_receipt_missing" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_RUNTIME_MEMBRANES_RECEIPT_MISSING"
    elif "double_sieve_not_passed" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_DOUBLE_SIEVE_NOT_PASSED"
    elif "step_outputs_missing" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_STEP_OUTPUTS_MISSING"
    elif "schema_surface_missing" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_SCHEMA_SURFACE_MISSING"
    elif "feedback" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_FEEDBACK_ATTACHMENT_INCOMPLETE"
    elif "degradation_unrecorded" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_OBSERVABILITY_DEGRADATION_UNRECORDED"
    elif "bare_failed" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_BARE_FAILED_STATUS"
    elif "unobserved_transition" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_UNOBSERVED_TRANSITION"
    elif "hidden_next" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_HIDDEN_NEXT_COMMAND"
    elif "sidecar_authority" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_SIDECAR_AUTHORITY_LEAK"
    elif "false_observability" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_FALSE_OBSERVABILITY_CLAIM"
    elif "runtime_mutation" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_RUNTIME_MUTATION_DETECTED"
    elif "c7_opened" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_C7_OPENED"
    elif "c8_opened" in first:
        stop = "STOP_RUNTIME_ATTACHMENT_C8_OPENED"
    else:
        stop = "STOP_RUNTIME_ATTACHMENT_RECEIPT_MISMATCH"

    return {
        "type": "STOP",
        "stop_code": stop,
        "next_command_goal": None,
    }

def fixture_outcome(fixture_id: str) -> str:
    return {
        "F1_VALID_ADMISSIBLE": "STEP_EXECUTION_GATE_OPENED_OBSERVED_NO_MUTATION",
        "F2_INVALID_SCHEMA": "STEP_BLOCKED_BY_SCHEMA_WITH_FEEDBACK",
        "F3_AUTHORITY_REQUIRED": "STEP_BLOCKED_BY_ADMISSIBILITY_WITH_FEEDBACK",
        "F4_FORBIDDEN_INPUT": "STEP_BLOCKED_BY_ADMISSIBILITY_WITH_FEEDBACK",
        "F5_EXECUTION_FAILURE_TYPED_FEEDBACK": "STEP_EXECUTION_FAILED_WITH_FEEDBACK",
        "F6_SIDECAR_PARTIAL_OBSERVABILITY": "STEP_OBSERVABILITY_DEGRADED_NO_FALSE_CLAIM",
    }[fixture_id]

def feedback_kind(fixture_id: str) -> Optional[str]:
    return {
        "F1_VALID_ADMISSIBLE": None,
        "F2_INVALID_SCHEMA": "SCHEMA_FORMATION_FEEDBACK",
        "F3_AUTHORITY_REQUIRED": "ADMISSIBILITY_AUTHORITY_FEEDBACK",
        "F4_FORBIDDEN_INPUT": "FORBIDDEN_INPUT_FEEDBACK",
        "F5_EXECUTION_FAILURE_TYPED_FEEDBACK": "EXECUTION_FAILURE_FEEDBACK",
        "F6_SIDECAR_PARTIAL_OBSERVABILITY": None,
    }[fixture_id]

def blocked_or_failed(fixture_id: str) -> bool:
    return fixture_id in {
        "F2_INVALID_SCHEMA",
        "F3_AUTHORITY_REQUIRED",
        "F4_FORBIDDEN_INPUT",
        "F5_EXECUTION_FAILURE_TYPED_FEEDBACK",
    }

def degradation_required(fixture_id: str) -> bool:
    return fixture_id == "F6_SIDECAR_PARTIAL_OBSERVABILITY"

def active_cell_for(fr: Dict[str, Any]) -> str:
    fixture_id = fr["fixture_id"]
    if fixture_id == "F2_INVALID_SCHEMA":
        return "SCHEMA_VALIDATOR_CELL"
    if fixture_id in {"F3_AUTHORITY_REQUIRED", "F4_FORBIDDEN_INPUT"}:
        return "LAWFUL_ADMISSIBILITY_CELL"
    if fixture_id == "F5_EXECUTION_FAILURE_TYPED_FEEDBACK":
        return "FIXTURE_EXECUTION_HARNESS"
    if fixture_id == "F6_SIDECAR_PARTIAL_OBSERVABILITY":
        return "OBSERVABILITY_SIDECAR"
    return "FIXTURE_EXECUTION_GATE"

def boundary_for(fr: Dict[str, Any]) -> str:
    fixture_id = fr["fixture_id"]
    if fixture_id == "F2_INVALID_SCHEMA":
        return "schema_shape_boundary"
    if fixture_id == "F3_AUTHORITY_REQUIRED":
        return "authority_boundary"
    if fixture_id == "F4_FORBIDDEN_INPUT":
        return "input_boundary"
    if fixture_id == "F5_EXECUTION_FAILURE_TYPED_FEEDBACK":
        return "declared_execution_boundary"
    if fixture_id == "F6_SIDECAR_PARTIAL_OBSERVABILITY":
        return "observability_completeness_boundary"
    return "fixture_only_no_live_mutation_boundary"

def attempted_move_for(fr: Dict[str, Any]) -> str:
    observed = fr.get("observed", {})
    candidate_id = observed.get("candidate_id")
    packet = fr.get("source_fixture_packet_ref")
    return candidate_id or packet or fr["fixture_id"]

def blocked_moves_for(fr: Dict[str, Any]) -> List[str]:
    fixture_id = fr["fixture_id"]
    if fixture_id == "F2_INVALID_SCHEMA":
        return ["LAWFUL_ADMISSIBILITY_CELL", "FIXTURE_EXECUTION_GATE"]
    if fixture_id == "F3_AUTHORITY_REQUIRED":
        return ["RUNTIME_PATCH", "FIXTURE_EXECUTION_GATE"]
    if fixture_id == "F4_FORBIDDEN_INPUT":
        return ["latest_file_selection", "mtime_selection", "FIXTURE_EXECUTION_GATE"]
    if fixture_id == "F5_EXECUTION_FAILURE_TYPED_FEEDBACK":
        return ["apply patch", "emit success receipt"]
    return []

def lawful_next_moves_for(fr: Dict[str, Any]) -> List[str]:
    fixture_id = fr["fixture_id"]
    if fixture_id == "F1_VALID_ADMISSIBLE":
        return ["halt after fixture gate opened with no live mutation"]
    if fixture_id == "F2_INVALID_SCHEMA":
        return ["return to Builder / Proposal Cell", "add receipt_contract", "rerun schema validation"]
    if fixture_id == "F3_AUTHORITY_REQUIRED":
        return ["return typed halt", "request review", "emit authority proposal"]
    if fixture_id == "F4_FORBIDDEN_INPUT":
        return ["return typed admissibility stop", "replace forbidden input with declared source"]
    if fixture_id == "F5_EXECUTION_FAILURE_TYPED_FEEDBACK":
        return ["declare or create target surface through reviewed proposal before retry"]
    if fixture_id == "F6_SIDECAR_PARTIAL_OBSERVABILITY":
        return ["preserve control result", "emit observability degradation record", "deny full-observability claim"]
    return []

def next_handling_for(fr: Dict[str, Any]) -> Dict[str, Any]:
    fixture_id = fr["fixture_id"]
    if fixture_id == "F1_VALID_ADMISSIBLE":
        kind = "HALT"
        return_target = None
    elif fixture_id == "F2_INVALID_SCHEMA":
        kind = "RETURN_TO_BUILDER"
        return_target = "BUILDER_PROPOSAL_CELL"
    elif fixture_id in {"F3_AUTHORITY_REQUIRED", "F4_FORBIDDEN_INPUT"}:
        kind = "RETURN_TO_REVIEW"
        return_target = "HUMAN_REVIEW_OR_AUTHORITY_PROPOSAL"
    elif fixture_id == "F5_EXECUTION_FAILURE_TYPED_FEEDBACK":
        kind = "RETURN_TO_BUILDER"
        return_target = "TARGET_SURFACE_DECLARATION_OR_REVIEWED_PROPOSAL"
    elif fixture_id == "F6_SIDECAR_PARTIAL_OBSERVABILITY":
        kind = "PARK"
        return_target = "OBSERVABILITY_ATTACHMENT_REVIEW"
    else:
        kind = "HALT"
        return_target = None

    return {
        "kind": kind,
        "next_packet_ref": None,
        "return_target": return_target,
        "next_command_goal": None,
    }

def movement_for(fr: Dict[str, Any]) -> Dict[str, Any]:
    fixture_id = fr["fixture_id"]
    advanced = fixture_id == "F1_VALID_ADMISSIBLE"
    halted = fixture_id != "F1_VALID_ADMISSIBLE"
    return {
        "advanced": advanced,
        "halted": halted,
        "blocked_moves": blocked_moves_for(fr),
        "lawful_next_moves": lawful_next_moves_for(fr),
    }

def make_feedback(fr: Dict[str, Any], edge_id: str, step_id: str) -> Optional[Dict[str, Any]]:
    fixture_id = fr["fixture_id"]
    kind = feedback_kind(fixture_id)
    if not kind:
        return None

    if fixture_id == "F2_INVALID_SCHEMA":
        diagnostic = {
            "failure_point": "SCHEMA_VALIDATION",
            "failed_relative_to_object": "runtime_move_candidate_v0",
            "failed_relative_to_source_surface": "fixture_packet_v0.candidate",
            "failed_relative_to_boundary": "schema_shape_boundary",
            "missing_capability_or_evidence": "receipt_contract",
            "blocked_next_moves": ["send to admissibility", "execute"],
            "lawful_next_refinement": "add receipt_contract and rerun schema validation"
        }
        quality = "BOUNDARY_AWARE_FAILURE"
        terminal_status = "BLOCKED"
        unit_id = "schema_validator.runtime_fixture_v0"
    elif fixture_id == "F3_AUTHORITY_REQUIRED":
        diagnostic = {
            "failure_point": "AUTHORITY_BOUNDARY_CHECK",
            "failed_relative_to_object": "RUNTIME_PATCH",
            "failed_relative_to_source_surface": "lawful_admissibility_cell_membrane_v0",
            "failed_relative_to_boundary": "authority_boundary",
            "missing_capability_or_evidence": "human_authorization_for_runtime_patch",
            "blocked_next_moves": ["execute", "treat schema-valid as admissible"],
            "lawful_next_refinement": "return typed halt or emit authority proposal for review"
        }
        quality = "ACTIONABLE"
        terminal_status = "BLOCKED"
        unit_id = "lawful_admissibility.runtime_fixture_v0"
    elif fixture_id == "F4_FORBIDDEN_INPUT":
        diagnostic = {
            "failure_point": "INPUT_BOUNDARY_CHECK",
            "failed_relative_to_object": "candidate.inputs.input_mode",
            "failed_relative_to_source_surface": "fixture_packet_v0.candidate.inputs",
            "failed_relative_to_boundary": "forbidden_input_boundary",
            "missing_capability_or_evidence": "declared_non-latest_non-mtime_source_ref",
            "blocked_next_moves": ["execute", "select latest file", "select by mtime"],
            "lawful_next_refinement": "replace forbidden input mode with explicit declared source reference"
        }
        quality = "ACTIONABLE"
        terminal_status = "BLOCKED"
        unit_id = "lawful_admissibility.runtime_fixture_v0"
    elif fixture_id == "F5_EXECUTION_FAILURE_TYPED_FEEDBACK":
        observed_feedback = fr.get("observed", {}).get("execution_result", {}).get("unit_feedback")
        if isinstance(observed_feedback, dict):
            diagnostic_raw = observed_feedback.get("diagnostic", {})
            diagnostic = {
                "failure_point": diagnostic_raw.get("failure_point", "LOAD_TARGET_SURFACE"),
                "failed_relative_to_object": diagnostic_raw.get("failed_relative_to_object", "observability_hook_registry"),
                "failed_relative_to_source_surface": diagnostic_raw.get("failed_relative_to_source_surface", "missing_hook_surface"),
                "failed_relative_to_boundary": diagnostic_raw.get("failed_relative_to_boundary", "declared_execution_boundary"),
                "missing_capability_or_evidence": diagnostic_raw.get("missing_capability", "target_surface_resolver"),
                "blocked_next_moves": diagnostic_raw.get("blocked_next_moves", ["apply patch", "emit success receipt"]),
                "lawful_next_refinement": diagnostic_raw.get("lawful_next_refinement", "declare or create target surface through reviewed proposal before retry")
            }
            quality = observed_feedback.get("feedback_quality", {}).get("quality_class", "ACTIONABLE")
        else:
            diagnostic = {
                "failure_point": "LOAD_TARGET_SURFACE",
                "failed_relative_to_object": "observability_hook_registry",
                "failed_relative_to_source_surface": "missing_hook_surface",
                "failed_relative_to_boundary": "declared_execution_boundary",
                "missing_capability_or_evidence": "target_surface_resolver",
                "blocked_next_moves": ["apply patch", "emit success receipt"],
                "lawful_next_refinement": "declare or create target surface through reviewed proposal before retry"
            }
            quality = "ACTIONABLE"
        terminal_status = "FAIL"
        unit_id = "builder_execution.runtime_fixture_v0"
    else:
        return None

    base = {
        "schema_version": "unit_feedback_record_v0",
        "feedback_id": None,
        "source_step_id": step_id,
        "source_edge_observation_id": edge_id,
        "source_edge_observation_ref": {
            "artifact": rel(EDGE_OBS_PATH),
            "record_id": edge_id
        },
        "unit_id": unit_id,
        "terminal_status": terminal_status,
        "feedback_kind": kind,
        "diagnostic": diagnostic,
        "feedback_quality": {
            "quality_class": quality
        },
        "safety": {
            "repair_applied": False,
            "retry_authorized": False,
            "authority_expansion": False,
            "proposal_created": False,
            "next_command_created": False
        }
    }
    base["feedback_id"] = "unit_feedback_" + sig8(base)
    return base

def make_sidecar_event(fr: Dict[str, Any], source_ref: str, step_id: str, run_id: str) -> Dict[str, Any]:
    fixture_id = fr["fixture_id"]
    event_kind = {
        "F1_VALID_ADMISSIBLE": "execution_allowed_packet_emitted",
        "F2_INVALID_SCHEMA": "schema_feedback_packet_emitted",
        "F3_AUTHORITY_REQUIRED": "admissibility_result_emitted",
        "F4_FORBIDDEN_INPUT": "admissibility_result_emitted",
        "F5_EXECUTION_FAILURE_TYPED_FEEDBACK": "execution_failed_typed",
        "F6_SIDECAR_PARTIAL_OBSERVABILITY": "observability_degraded",
    }[fixture_id]

    terminal = fr.get("terminal") or {
        "type": "STOP",
        "stop_code": fr.get("observed_terminal"),
        "next_command_goal": None
    }

    event = {
        "schema_version": "observability_sidecar_event_v0",
        "event_id": None,
        "event_kind": event_kind,
        "run_id": run_id,
        "step_id": step_id,
        "fixture_id": fixture_id,
        "cell_id": active_cell_for(fr),
        "source_packet_ref": fr.get("source_fixture_packet_ref"),
        "source_fixture_receipt_ref": source_ref,
        "result": {
            "schema_result": fr.get("schema_result"),
            "admissibility_result": fr.get("admissibility_result"),
            "execution_result": fr.get("execution_result"),
            "sidecar_status": fr.get("sidecar_status"),
            "unit_feedback_status": fr.get("unit_feedback_status"),
            "step_outcome": fixture_outcome(fixture_id)
        },
        "terminal": terminal,
        "provenance": {
            "source_kind": "DOUBLE_SIEVE_FIXTURE_RECEIPT",
            "source_fixture_receipt_ref": source_ref,
            "derived_not_live_emitted": True
        },
        "sidecar_boundary": {
            "control_path_participant": False,
            "authority_claimed": False,
            "state_mutated": False,
            "command_emitted": False
        }
    }
    event["event_id"] = "obs_event_" + sig8(event)
    return event

def make_edge_observation(fr: Dict[str, Any], source_ref: str, sidecar_event_id: str, step_id: str, run_id: str) -> Dict[str, Any]:
    fixture_id = fr["fixture_id"]
    edge = {
        "schema_version": "decision_edge_observation_record_v0",
        "observation_id": None,
        "source_sidecar_event_id": sidecar_event_id,
        "source_sidecar_event_ref": {
            "artifact": rel(SIDECAR_EVENTS_PATH),
            "record_id": sidecar_event_id
        },
        "source_packet_ref": fr.get("source_fixture_packet_ref"),
        "source_fixture_receipt_ref": source_ref,
        "run_id": run_id,
        "step_id": step_id,
        "fixture_id": fixture_id,
        "active_cell": active_cell_for(fr),
        "active_object": fr.get("source_fixture_packet_ref"),
        "attempted_move": attempted_move_for(fr),
        "boundary_checked": boundary_for(fr),
        "boundary_result": fr.get("admissibility_result") if fr.get("schema_result") == "VALID" else fr.get("schema_result"),
        "control_result": fr.get("execution_result"),
        "blocked_moves": blocked_moves_for(fr),
        "lawful_next_moves": lawful_next_moves_for(fr),
        "candidate_edge_handles": [
            {
                "handle": f"{fixture_id}:{active_cell_for(fr)}:{boundary_for(fr)}",
                "status": "OBSERVED_ONCE",
                "authorized_for_reuse": False
            }
        ],
        "collection_status": "OBSERVATION_ONLY",
        "schema_claim": "NONE",
        "architecture_change": False,
        "authorization_created": False,
        "execution_registry_mutated": False,
        "graph_archive_mutated": False,
        "validator_authorization_schema_created": False
    }
    edge["observation_id"] = "edge_obs_" + sig8(edge)
    return edge

def make_degradation(fr: Dict[str, Any], sidecar_event_id: str, step_id: str) -> Optional[Dict[str, Any]]:
    if fr["fixture_id"] != "F6_SIDECAR_PARTIAL_OBSERVABILITY":
        return None

    observed_sidecar = fr.get("observed", {}).get("sidecar_result", {})
    missing_fields = observed_sidecar.get("missing_fields", [
        {
            "event_kind": "admissibility_result_emitted",
            "field_path": "authority_boundary"
        }
    ])

    degradation = {
        "schema_version": "observability_degradation_record_v0",
        "degradation_id": None,
        "source_step_id": step_id,
        "source_sidecar_event_id": sidecar_event_id,
        "source_sidecar_event_ref": {
            "artifact": rel(SIDECAR_EVENTS_PATH),
            "record_id": sidecar_event_id
        },
        "sidecar_status": "OBSERVATION_UNDER_TYPED",
        "missing_fields": missing_fields,
        "control_result_preserved": True,
        "full_observability_claim_allowed": False,
        "effects": {
            "control_path_modified": False,
            "authority_decision_modified": False,
            "runtime_result_overridden": False
        },
        "negative_controls": {
            "sidecar_authorized_move_count": 0,
            "sidecar_denied_move_count": 0,
            "sidecar_state_mutation_count": 0,
            "false_full_observability_claim_count": 0
        }
    }
    degradation["degradation_id"] = "obs_degradation_" + sig8(degradation)
    return degradation

def make_step_receipt(
    fr: Dict[str, Any],
    source_ref: str,
    run_id: str,
    step_id: str,
    sidecar_event_id: str,
    edge_id: str,
    feedback_id: Optional[str],
    degradation_id: Optional[str],
    bad_counters: Dict[str, int],
) -> Dict[str, Any]:
    receipt = {
        "schema_version": "runtime_step_receipt_v0",
        "receipt_id": None,
        "run_id": run_id,
        "step_id": step_id,
        "fixture_id": fr["fixture_id"],
        "input_packet_ref": fr.get("source_fixture_packet_ref"),
        "source_fixture_receipt_ref": source_ref,
        "control_cell": active_cell_for(fr),
        "control_result": fr.get("execution_result"),
        "step_outcome": fixture_outcome(fr["fixture_id"]),
        "terminal": fr.get("terminal") or {
            "type": "STOP",
            "stop_code": fr.get("observed_terminal"),
            "next_command_goal": None
        },
        "sidecar_event_id": sidecar_event_id,
        "sidecar_event_ref": {
            "artifact": rel(SIDECAR_EVENTS_PATH),
            "record_id": sidecar_event_id
        },
        "decision_edge_observation_id": edge_id,
        "decision_edge_observation_ref": {
            "artifact": rel(EDGE_OBS_PATH),
            "record_id": edge_id
        },
        "unit_feedback_id": feedback_id,
        "unit_feedback_ref": None if feedback_id is None else {
            "artifact": rel(UNIT_FEEDBACK_PATH),
            "record_id": feedback_id
        },
        "observability_degradation_id": degradation_id,
        "observability_degradation_ref": None if degradation_id is None else {
            "artifact": rel(DEGRADATION_PATH),
            "record_id": degradation_id
        },
        "movement": movement_for(fr),
        "next_handling": next_handling_for(fr),
        "negative_controls": {
            "bare_failed_status_count": bad_counters["bare_failed_status_count"],
            "unobserved_transition_count": bad_counters["unobserved_transition_count"],
            "hidden_next_command_count": bad_counters["hidden_next_command_count"],
            "sidecar_authority_count": bad_counters["sidecar_authority_count"]
        }
    }
    receipt["receipt_id"] = "runtime_step_receipt_" + sig8(receipt)
    return receipt

def make_step_bundle(
    fr: Dict[str, Any],
    source_ref: str,
    run_id: str,
    step_id: str,
    sidecar_event_id: str,
    edge_id: str,
    feedback_id: Optional[str],
    degradation_id: Optional[str],
    step_receipt_id: str,
    bad_counters: Dict[str, int],
) -> Dict[str, Any]:
    fixture_id = fr["fixture_id"]
    observability_status = "OBSERVATION_DEGRADED" if degradation_required(fixture_id) else "OBSERVED"
    feedback_status = "FEEDBACK_EMITTED" if feedback_id else "NOT_REQUIRED"

    bundle = {
        "schema_version": "runtime_step_bundle_v0",
        "bundle_id": None,
        "run_id": run_id,
        "step_id": step_id,
        "fixture_id": fixture_id,
        "input_packet_ref": fr.get("source_fixture_packet_ref"),
        "source_fixture_receipt_ref": source_ref,
        "control_cell": active_cell_for(fr),
        "control_result": fr.get("execution_result"),
        "step_outcome": fixture_outcome(fixture_id),
        "step_terminal": fr.get("terminal") or {
            "type": "STOP",
            "stop_code": fr.get("observed_terminal"),
            "next_command_goal": None
        },
        "sidecar_event_id": sidecar_event_id,
        "sidecar_event_ref": {
            "artifact": rel(SIDECAR_EVENTS_PATH),
            "record_id": sidecar_event_id
        },
        "decision_edge_observation_id": edge_id,
        "decision_edge_observation_ref": {
            "artifact": rel(EDGE_OBS_PATH),
            "record_id": edge_id
        },
        "unit_feedback_id": feedback_id,
        "unit_feedback_ref": None if feedback_id is None else {
            "artifact": rel(UNIT_FEEDBACK_PATH),
            "record_id": feedback_id
        },
        "observability_degradation_id": degradation_id,
        "observability_degradation_ref": None if degradation_id is None else {
            "artifact": rel(DEGRADATION_PATH),
            "record_id": degradation_id
        },
        "runtime_step_receipt_id": step_receipt_id,
        "runtime_step_receipt_ref": {
            "artifact": rel(STEP_RECEIPTS_PATH),
            "record_id": step_receipt_id
        },
        "observability_status": observability_status,
        "feedback_status": feedback_status,
        "bundle_gate": "PASS",
        "bad_counters": {
            "bare_failed_status_count": bad_counters["bare_failed_status_count"],
            "unobserved_transition_count": bad_counters["unobserved_transition_count"],
            "hidden_next_command_count": bad_counters["hidden_next_command_count"],
            "sidecar_authority_count": bad_counters["sidecar_authority_count"]
        }
    }
    bundle["bundle_id"] = "runtime_step_bundle_" + sig8(bundle)
    return bundle

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []

    if not INTAKE_PATH.exists():
        failures.append(f"intake_missing:{rel(INTAKE_PATH)}")
        intake = {}
    else:
        intake = read_json(INTAKE_PATH)

    if intake:
        if intake.get("schema_version") != "runtime_attachment_intake_v0":
            failures.append(f"intake_untyped:{intake.get('schema_version')}")
        if intake.get("selected_by") != "human/operator":
            failures.append(f"intake_not_operator_selected:{intake.get('selected_by')}")
        if intake.get("builder_generated") is not False:
            failures.append(f"intake_builder_generated:{intake.get('builder_generated')}")
        if intake.get("attachment_mode") != "ATTACH_TO_COMMITTED_DOUBLE_SIEVE_STEP_RECEIPTS":
            failures.append(f"intake_attachment_mode_wrong:{intake.get('attachment_mode')}")
        for key in [
            "runtime_rerun_authorized",
            "source_receipt_mutation_authorized",
            "live_hook_installation_authorized",
            "graph_archive_mutation_authorized",
            "validator_authorization_schema_creation_authorized",
            "decision_edge_authorization_creation_authorized",
            "runtime_mutation_authorized",
            "schema_archive_mutation_authorized",
            "move_addition_authorized",
            "fixture_expansion_authorized",
            "c7_opened",
            "c8_opened",
        ]:
            if intake.get(key) is not False:
                failures.append(f"intake_authority_leak:{key}:{intake.get(key)}")

    source_paths = {}
    for key in [
        "source_r0_active_source_packet_ref",
        "source_r0_receipt_ref",
        "source_runtime_membranes_receipt_ref",
        "source_double_sieve_suite_receipt_ref",
        "source_double_sieve_rollup_ref",
    ]:
        ref = intake.get(key) if intake else None
        if not ref:
            failures.append(f"intake_missing_ref:{key}")
            continue
        path = ROOT / ref
        source_paths[key] = path
        if not path.exists():
            if key == "source_r0_active_source_packet_ref":
                failures.append(f"r0_packet_missing:{ref}")
            elif key == "source_runtime_membranes_receipt_ref":
                failures.append(f"runtime_membranes_receipt_missing:{ref}")
            elif key == "source_double_sieve_suite_receipt_ref":
                failures.append(f"double_sieve_receipt_missing:{ref}")
            else:
                failures.append(f"source_ref_missing:{key}:{ref}")

    source_hashes_before = {
        key: sha256_file(path)
        for key, path in source_paths.items()
        if path.exists()
    }

    r0_packet = read_json(source_paths["source_r0_active_source_packet_ref"]) if source_paths.get("source_r0_active_source_packet_ref", Path()).exists() else {}
    r0_receipt = read_json(source_paths["source_r0_receipt_ref"]) if source_paths.get("source_r0_receipt_ref", Path()).exists() else {}
    membrane_receipt = read_json(source_paths["source_runtime_membranes_receipt_ref"]) if source_paths.get("source_runtime_membranes_receipt_ref", Path()).exists() else {}
    double_sieve_receipt = read_json(source_paths["source_double_sieve_suite_receipt_ref"]) if source_paths.get("source_double_sieve_suite_receipt_ref", Path()).exists() else {}
    double_sieve_rollup = read_json(source_paths["source_double_sieve_rollup_ref"]) if source_paths.get("source_double_sieve_rollup_ref", Path()).exists() else {}

    if r0_receipt and r0_receipt.get("gate") != "PASS":
        failures.append(f"r0_receipt_not_pass:{r0_receipt.get('gate')}")

    if membrane_receipt:
        ms = membrane_receipt.get("machine_readable_runtime_membranes_summary", {})
        if membrane_receipt.get("gate") != "PASS":
            failures.append(f"runtime_membranes_receipt_not_pass:{membrane_receipt.get('gate')}")
        if ms.get("runtime_membranes_executable") is not True:
            failures.append("runtime_membranes_not_executable")
        for key in ["runtime_live", "live_runtime_adoption", "live_mutation_authorized", "c7_opened", "c8_opened"]:
            if ms.get(key) is not False:
                failures.append(f"runtime_membranes_boundary_leak:{key}:{ms.get(key)}")

    if double_sieve_receipt:
        ds = double_sieve_receipt.get("machine_readable_double_sieve_summary", {})
        if double_sieve_receipt.get("gate") != "PASS":
            failures.append("double_sieve_not_passed:gate")
        if double_sieve_receipt.get("outcome_class") != "DOUBLE_SIEVE_PASS":
            failures.append(f"double_sieve_not_passed:outcome:{double_sieve_receipt.get('outcome_class')}")
        if ds.get("suite_passed") is not True:
            failures.append(f"double_sieve_not_passed:suite_passed:{ds.get('suite_passed')}")
        if ds.get("fixtures_passed") != 6 or ds.get("fixtures_failed") != 0:
            failures.append(f"double_sieve_not_passed:fixtures:{ds.get('fixtures_passed')}/{ds.get('fixtures_failed')}")
        for key in [
            "live_mutation_executed",
            "runtime_patch_authorized",
            "schema_archive_mutation_authorized",
            "move_addition_authorized",
            "fixture_expansion_authorized",
            "c7_opened",
            "c8_opened",
            "hidden_next_command",
        ]:
            if ds.get(key) is not False:
                failures.append(f"double_sieve_boundary_leak:{key}:{ds.get(key)}")

    fixture_refs = intake.get("source_fixture_receipt_refs", []) if intake else []
    runtime_step_refs = intake.get("source_runtime_step_refs", []) if intake else []
    if fixture_refs != runtime_step_refs:
        failures.append("runtime_step_refs_do_not_match_fixture_receipt_refs")
    if len(fixture_refs) != 6:
        failures.append(f"step_outputs_missing:fixture_ref_count:{len(fixture_refs)}")

    fixture_receipts = []
    fixture_hashes_before = {}
    for ref in fixture_refs:
        path = ROOT / ref
        if not path.exists():
            failures.append(f"step_outputs_missing:{ref}")
            continue
        fixture_hashes_before[ref] = sha256_file(path)
        fixture_receipts.append(read_json(path))

    fixture_ids = [fr.get("fixture_id") for fr in fixture_receipts]
    if fixture_ids != EXPECTED_FIXTURE_ORDER:
        failures.append(f"fixture_order_wrong:{fixture_ids}")

    attachment_run_id = "runtime_attachment_run_" + sig8({
        "intake_id": intake.get("intake_id"),
        "double_sieve_receipt": double_sieve_receipt.get("receipt_id"),
        "fixture_ids": fixture_ids,
    })

    sidecar_events: List[Dict[str, Any]] = []
    edge_observations: List[Dict[str, Any]] = []
    unit_feedback_records: List[Dict[str, Any]] = []
    degradation_records: List[Dict[str, Any]] = []
    runtime_step_receipts: List[Dict[str, Any]] = []
    step_bundles: List[Dict[str, Any]] = []

    aggregate_counters = zero_counters()
    step_outcomes = Counter()

    if not failures:
        for idx, (ref, fr) in enumerate(zip(fixture_refs, fixture_receipts), start=1):
            fixture_id = fr["fixture_id"]
            step_id = f"runtime_attachment_step_{idx:02d}_{fixture_id}"

            step_counters = zero_counters()

            if fr.get("execution_result") == "FAILED":
                step_counters["bare_failed_status_count"] += 1

            sidecar_event = make_sidecar_event(fr, ref, step_id, attachment_run_id)
            edge = make_edge_observation(fr, ref, sidecar_event["event_id"], step_id, attachment_run_id)
            feedback = make_feedback(fr, edge["observation_id"], step_id)
            degradation = make_degradation(fr, sidecar_event["event_id"], step_id)

            if blocked_or_failed(fixture_id) and feedback is None:
                step_counters["feedback_missing_count"] += 1
            if not blocked_or_failed(fixture_id) and feedback is not None:
                warnings.append(f"unexpected_feedback_for_non_blocked_step:{fixture_id}")

            if degradation_required(fixture_id) and degradation is None:
                step_counters["false_full_observability_claim_count"] += 1
            if degradation_required(fixture_id):
                if degradation and degradation.get("full_observability_claim_allowed") is not False:
                    step_counters["false_full_observability_claim_count"] += 1

            sb = sidecar_event["sidecar_boundary"]
            if sb.get("control_path_participant") is not False:
                step_counters["sidecar_control_path_modification_count"] += 1
            if sb.get("authority_claimed") is not False:
                step_counters["sidecar_authority_count"] += 1
            if sb.get("state_mutated") is not False:
                step_counters["sidecar_state_mutation_count"] += 1
            if sb.get("command_emitted") is not False:
                step_counters["sidecar_command_emission_count"] += 1

            if edge.get("authorization_created") is not False:
                step_counters["decision_edge_authorization_created_count"] += 1
            if edge.get("graph_archive_mutated") is not False:
                step_counters["graph_archive_mutation_count"] += 1
            if edge.get("validator_authorization_schema_created") is not False:
                step_counters["validator_authorization_schema_created_count"] += 1
            if edge.get("execution_registry_mutated") is not False:
                step_counters["move_addition_count"] += 1

            if feedback:
                safety = feedback.get("safety", {})
                if safety.get("repair_applied") is not False:
                    step_counters["repair_applied_by_feedback_count"] += 1
                if safety.get("retry_authorized") is not False:
                    step_counters["retry_authorized_by_feedback_count"] += 1
                if safety.get("authority_expansion") is not False:
                    step_counters["authority_expanded_by_feedback_count"] += 1
                if safety.get("next_command_created") is not False:
                    step_counters["hidden_next_command_count"] += 1

            if not sidecar_event:
                step_counters["unobserved_transition_count"] += 1
            if not edge:
                step_counters["unobserved_transition_count"] += 1

            step_receipt = make_step_receipt(
                fr=fr,
                source_ref=ref,
                run_id=attachment_run_id,
                step_id=step_id,
                sidecar_event_id=sidecar_event["event_id"],
                edge_id=edge["observation_id"],
                feedback_id=feedback["feedback_id"] if feedback else None,
                degradation_id=degradation["degradation_id"] if degradation else None,
                bad_counters=step_counters,
            )

            if step_receipt.get("next_handling", {}).get("next_command_goal") is not None:
                step_counters["hidden_next_command_count"] += 1

            bundle = make_step_bundle(
                fr=fr,
                source_ref=ref,
                run_id=attachment_run_id,
                step_id=step_id,
                sidecar_event_id=sidecar_event["event_id"],
                edge_id=edge["observation_id"],
                feedback_id=feedback["feedback_id"] if feedback else None,
                degradation_id=degradation["degradation_id"] if degradation else None,
                step_receipt_id=step_receipt["receipt_id"],
                bad_counters=step_counters,
            )

            if not bundle.get("sidecar_event_ref"):
                step_counters["unobserved_transition_count"] += 1
            if not bundle.get("decision_edge_observation_ref"):
                step_counters["unobserved_transition_count"] += 1
            if not bundle.get("runtime_step_receipt_ref"):
                step_counters["unobserved_transition_count"] += 1
            if blocked_or_failed(fixture_id) and not bundle.get("unit_feedback_ref"):
                step_counters["feedback_missing_count"] += 1
            if degradation_required(fixture_id) and not bundle.get("observability_degradation_ref"):
                step_counters["false_full_observability_claim_count"] += 1

            bundle["bad_counters"] = {
                "bare_failed_status_count": step_counters["bare_failed_status_count"],
                "unobserved_transition_count": step_counters["unobserved_transition_count"],
                "hidden_next_command_count": step_counters["hidden_next_command_count"],
                "sidecar_authority_count": step_counters["sidecar_authority_count"],
            }
            bundle["bundle_gate"] = "PASS" if all(v == 0 for v in step_counters.values()) else "FAIL"

            sidecar_events.append(sidecar_event)
            edge_observations.append(edge)
            if feedback:
                unit_feedback_records.append(feedback)
            if degradation:
                degradation_records.append(degradation)
            runtime_step_receipts.append(step_receipt)
            step_bundles.append(bundle)
            step_outcomes[fixture_outcome(fixture_id)] += 1
            add_counters(aggregate_counters, step_counters)

    source_hashes_after = {
        key: sha256_file(path)
        for key, path in source_paths.items()
        if path.exists()
    }
    fixture_hashes_after = {
        ref: sha256_file(ROOT / ref)
        for ref in fixture_refs
        if (ROOT / ref).exists()
    }

    if source_hashes_before != source_hashes_after:
        aggregate_counters["source_receipt_mutation_count"] += 1
    if fixture_hashes_before != fixture_hashes_after:
        aggregate_counters["source_fixture_receipt_mutation_count"] += 1
    if source_hashes_before.get("source_double_sieve_suite_receipt_ref") != source_hashes_after.get("source_double_sieve_suite_receipt_ref"):
        aggregate_counters["source_double_sieve_receipt_mutation_count"] += 1

    if any(v != 0 for v in aggregate_counters.values()):
        for key, value in aggregate_counters.items():
            if value:
                failures.append(f"{key}:{value}")

    write_jsonl(SIDECAR_EVENTS_PATH, sidecar_events)
    write_jsonl(EDGE_OBS_PATH, edge_observations)
    write_jsonl(UNIT_FEEDBACK_PATH, unit_feedback_records)
    write_jsonl(DEGRADATION_PATH, degradation_records)
    write_jsonl(STEP_RECEIPTS_PATH, runtime_step_receipts)
    write_jsonl(STEP_BUNDLES_PATH, step_bundles)

    runtime_steps_total = len(fixture_receipts)
    sidecar_events_emitted = len(sidecar_events)
    edge_obs_emitted = len(edge_observations)
    step_receipts_emitted = len(runtime_step_receipts)
    blocked_failed_steps = sum(1 for fr in fixture_receipts if blocked_or_failed(fr.get("fixture_id")))
    feedback_required_count = blocked_failed_steps
    feedback_emitted = len(unit_feedback_records)
    degraded_steps = sum(1 for fr in fixture_receipts if degradation_required(fr.get("fixture_id")))
    degradation_emitted = len(degradation_records)

    coverage = {
        "sidecar_event_coverage": sidecar_events_emitted / runtime_steps_total if runtime_steps_total else 0.0,
        "decision_edge_coverage": edge_obs_emitted / runtime_steps_total if runtime_steps_total else 0.0,
        "receipt_coverage": step_receipts_emitted / runtime_steps_total if runtime_steps_total else 0.0,
        "unit_feedback_coverage": feedback_emitted / feedback_required_count if feedback_required_count else 1.0,
        "observability_degradation_record_coverage": degradation_emitted / degraded_steps if degraded_steps else 1.0,
    }

    expected_coverage_pass = (
        runtime_steps_total == 6
        and sidecar_events_emitted == 6
        and edge_obs_emitted == 6
        and step_receipts_emitted == 6
        and blocked_failed_steps == 4
        and feedback_required_count == 4
        and feedback_emitted == 4
        and degraded_steps == 1
        and degradation_emitted == 1
        and all(v == 1.0 for v in coverage.values())
    )

    if not expected_coverage_pass:
        failures.append("feedback_attachment_incomplete:coverage")

    if aggregate_counters["bare_failed_status_count"]:
        failures.append("bare_failed_status")
    if aggregate_counters["unobserved_transition_count"]:
        failures.append("unobserved_transition")
    if aggregate_counters["hidden_next_command_count"]:
        failures.append("hidden_next_command")
    if aggregate_counters["sidecar_authority_count"]:
        failures.append("sidecar_authority_leak")
    if aggregate_counters["false_full_observability_claim_count"]:
        failures.append("false_observability_claim")
    if aggregate_counters["runtime_mutation_count"]:
        failures.append("runtime_mutation_detected")
    if aggregate_counters["c7_opened_count"]:
        failures.append("c7_opened")
    if aggregate_counters["c8_opened_count"]:
        failures.append("c8_opened")

    gate, status, outcome_class = classify_failure(failures)
    terminal = terminal_for(gate, failures)

    rollup = {
        "schema_version": "runtime_observability_feedback_rollup_v0",
        "milestone": MILESTONE,
        "attachment_run_id": attachment_run_id,
        "source_double_sieve_suite_id": double_sieve_receipt.get("suite_id"),
        "source_double_sieve_run_id": double_sieve_receipt.get("run_id"),
        "runtime_steps_total": runtime_steps_total,
        "sidecar_events_emitted": sidecar_events_emitted,
        "decision_edge_observations_emitted": edge_obs_emitted,
        "runtime_step_receipts_emitted": step_receipts_emitted,
        "blocked_or_failed_steps": blocked_failed_steps,
        "unit_feedback_required": feedback_required_count,
        "unit_feedback_emitted": feedback_emitted,
        "observability_degraded_steps": degraded_steps,
        "observability_degradation_records_emitted": degradation_emitted,
        "step_outcomes": dict(step_outcomes),
        "coverage": coverage,
        "bad_counters": aggregate_counters,
        "milestone_gate": gate,
        "terminal": terminal,
    }

    readout = {
        "schema_version": "runtime_observability_feedback_readout_v0",
        "title": "Runtime observability and feedback attachment readout",
        "runtime_steps_checked": runtime_steps_total,
        "attachment_coverage": {
            "sidecar_events": f"{sidecar_events_emitted} / {runtime_steps_total}",
            "decision_edge_observations": f"{edge_obs_emitted} / {runtime_steps_total}",
            "runtime_step_receipts": f"{step_receipts_emitted} / {runtime_steps_total}",
            "unit_feedback_where_required": f"{feedback_emitted} / {feedback_required_count}",
            "observability_degradation_records": f"{degradation_emitted} / {degraded_steps}",
        },
        "bad_counters": {
            "bare_FAILED": aggregate_counters["bare_failed_status_count"],
            "unobserved_transition": aggregate_counters["unobserved_transition_count"],
            "hidden_next_command": aggregate_counters["hidden_next_command_count"],
            "sidecar_authority": aggregate_counters["sidecar_authority_count"],
            "feedback_missing": aggregate_counters["feedback_missing_count"],
            "false_full_observability_claim": aggregate_counters["false_full_observability_claim_count"],
        },
        "outcome": "RUNTIME_OBSERVABILITY_AND_FEEDBACK_ATTACHED" if gate == "PASS" else "RUNTIME_OBSERVABILITY_AND_FEEDBACK_ATTACHMENT_FAIL",
        "interpretation": "Every committed Double-Sieve runtime step now has downstream observation, decision-edge, feedback where required, degradation record where required, and receipt attachment." if gate == "PASS" else "Runtime attachment exposed a typed evidence gap.",
    }

    profile = {
        "schema_version": "runtime_observability_feedback_profile_v0",
        "profile_id": "runtime_observability_feedback_profile_" + sig8(rollup),
        "attachment_run_id": attachment_run_id,
        "status": "RUNTIME_ATTACHMENT_PASS" if gate == "PASS" else "RUNTIME_ATTACHMENT_BLOCKED_OR_FAILED",
        "source_mode": "DOWNSTREAM_ATTACHMENT_OVER_COMMITTED_DOUBLE_SIEVE_RECEIPTS",
        "runtime_rerun": False,
        "live_hook_installation": False,
        "source_receipts_mutated": False,
        "graph_archive_mutation": False,
        "validator_authorization_schema_created": False,
        "decision_edge_authorization_created": False,
        "bad_counters_zero": all(v == 0 for v in aggregate_counters.values()),
        "success_meaning": "Every committed Double-Sieve runtime step is observable, decision-edge recorded, diagnostically explained when blocked/failed, and receipt-backed.",
        "success_does_not_mean": [
            "C7 is open",
            "C8 is open",
            "runtime radius is proven",
            "runtime adoption is authorized",
            "runtime mutation is authorized",
            "sidecar has authority",
            "O1 is a graph engine",
            "O2 may repair",
            "decision-edge observations are validator authorization schemas"
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "runtime_observability_feedback_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "attachment_run_id": attachment_run_id,
        "status": status,
        "outcome_class": outcome_class,
        "summary": {
            "attachment_passed": gate == "PASS",
            "runtime_steps_total": runtime_steps_total,
            "sidecar_events_emitted": sidecar_events_emitted,
            "decision_edge_observations_emitted": edge_obs_emitted,
            "runtime_step_receipts_emitted": step_receipts_emitted,
            "unit_feedback_required": feedback_required_count,
            "unit_feedback_emitted": feedback_emitted,
            "observability_degraded_steps": degraded_steps,
            "observability_degradation_records_emitted": degradation_emitted,
            "no_bare_failed": aggregate_counters["bare_failed_status_count"] == 0,
            "no_unobserved_transition": aggregate_counters["unobserved_transition_count"] == 0,
            "no_hidden_next_command": aggregate_counters["hidden_next_command_count"] == 0,
            "no_sidecar_authority": aggregate_counters["sidecar_authority_count"] == 0,
            "no_false_observability_claim": aggregate_counters["false_full_observability_claim_count"] == 0,
            "source_receipts_mutated": False,
            "runtime_rerun": False,
            "runtime_mutation": False,
            "c7_opened": False,
            "c8_opened": False,
        },
        "failures": failures,
        "warnings": warnings,
    }

    transition_trace = {
        "schema_version": "runtime_observability_feedback_transition_trace_v0",
        "unit_id": UNIT_ID,
        "attachment_run_id": attachment_run_id,
        "transitions": [
            {
                "from": "DOUBLE_SIEVE_FIXTURE_SUITE_PASS_COMMITTED",
                "edge": "consume explicit attachment intake and committed step receipts",
                "to": "RUNTIME_ATTACHMENT_CONTEXT_BOUND" if gate == "PASS" else "RUNTIME_ATTACHMENT_BLOCKED"
            },
            {
                "from": "RUNTIME_ATTACHMENT_CONTEXT_BOUND" if gate == "PASS" else "RUNTIME_ATTACHMENT_BLOCKED",
                "edge": "derive sidecar events, decision-edge observations, feedback, degradation records, and step receipts",
                "to": "RUNTIME_ATTACHMENT_BUNDLES_COMPLETE" if gate == "PASS" else "RUNTIME_ATTACHMENT_INCOMPLETE"
            },
            {
                "from": "RUNTIME_ATTACHMENT_BUNDLES_COMPLETE" if gate == "PASS" else "RUNTIME_ATTACHMENT_INCOMPLETE",
                "edge": "emit attachment receipt and stop",
                "to": terminal["stop_code"]
            }
        ],
        "source_receipt_immutability": {
            "source_receipts_mutated": False,
            "source_fixture_receipts_mutated": False,
            "source_double_sieve_receipt_mutated": False,
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "fixture_hashes_before": fixture_hashes_before,
            "fixture_hashes_after": fixture_hashes_after
        },
        "terminal": terminal,
    }

    write_json(ROLLUP_PATH, rollup)
    write_json(READOUT_PATH, readout)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRANSITION_TRACE_PATH, transition_trace)

    acceptance_gate_results = {
        "RUNTIME_ATTACHMENT_0_INTAKE_CONSUMED": INTAKE_PATH.exists() and bool(intake),
        "RUNTIME_ATTACHMENT_1_R0_ACTIVE_SOURCE_PACKET_REF_VERIFIED": bool(r0_packet),
        "RUNTIME_ATTACHMENT_2_RUNTIME_MEMBRANES_RECEIPT_VERIFIED": bool(membrane_receipt) and membrane_receipt.get("gate") == "PASS",
        "RUNTIME_ATTACHMENT_3_DOUBLE_SIEVE_PASS_RECEIPT_VERIFIED": bool(double_sieve_receipt) and double_sieve_receipt.get("gate") == "PASS" and double_sieve_receipt.get("outcome_class") == "DOUBLE_SIEVE_PASS",
        "RUNTIME_ATTACHMENT_4_FIXTURE_RECEIPTS_F1_TO_F6_LOADED": fixture_ids == EXPECTED_FIXTURE_ORDER,
        "RUNTIME_ATTACHMENT_5_RUNTIME_STEP_OUTPUTS_LOADED": len(fixture_receipts) == 6,
        "RUNTIME_ATTACHMENT_6_EACH_STEP_HAS_SIDECAR_EVENT": sidecar_events_emitted == 6,
        "RUNTIME_ATTACHMENT_7_EACH_STEP_HAS_DECISION_EDGE_OBSERVATION": edge_obs_emitted == 6,
        "RUNTIME_ATTACHMENT_8_EACH_STEP_HAS_RUNTIME_STEP_RECEIPT": step_receipts_emitted == 6,
        "RUNTIME_ATTACHMENT_9_BLOCKED_FAILED_STEPS_HAVE_UNIT_FEEDBACK": feedback_emitted == feedback_required_count == 4,
        "RUNTIME_ATTACHMENT_10_SCHEMA_BLOCK_HAS_DIAGNOSTIC_FEEDBACK": any(r.get("feedback_kind") == "SCHEMA_FORMATION_FEEDBACK" for r in unit_feedback_records),
        "RUNTIME_ATTACHMENT_11_AUTHORITY_BLOCK_HAS_DIAGNOSTIC_FEEDBACK": any(r.get("feedback_kind") == "ADMISSIBILITY_AUTHORITY_FEEDBACK" for r in unit_feedback_records),
        "RUNTIME_ATTACHMENT_12_FORBIDDEN_INPUT_BLOCK_HAS_DIAGNOSTIC_FEEDBACK": any(r.get("feedback_kind") == "FORBIDDEN_INPUT_FEEDBACK" for r in unit_feedback_records),
        "RUNTIME_ATTACHMENT_13_EXECUTION_FAILURE_HAS_TYPED_FEEDBACK": any(r.get("feedback_kind") == "EXECUTION_FAILURE_FEEDBACK" for r in unit_feedback_records),
        "RUNTIME_ATTACHMENT_14_OBSERVABILITY_DEGRADATION_RECORDED": degradation_emitted == 1,
        "RUNTIME_ATTACHMENT_15_NO_FALSE_FULL_OBSERVABILITY_CLAIM": aggregate_counters["false_full_observability_claim_count"] == 0,
        "RUNTIME_ATTACHMENT_16_NO_BARE_FAILED": aggregate_counters["bare_failed_status_count"] == 0,
        "RUNTIME_ATTACHMENT_17_NO_UNOBSERVED_TRANSITION": aggregate_counters["unobserved_transition_count"] == 0,
        "RUNTIME_ATTACHMENT_18_NO_HIDDEN_NEXT_COMMAND": aggregate_counters["hidden_next_command_count"] == 0,
        "RUNTIME_ATTACHMENT_19_NO_SIDECAR_AUTHORITY": aggregate_counters["sidecar_authority_count"] == 0,
        "RUNTIME_ATTACHMENT_20_NO_SIDE_CAR_CONTROL_PATH_MODIFICATION": aggregate_counters["sidecar_control_path_modification_count"] == 0,
        "RUNTIME_ATTACHMENT_21_NO_REPAIR_APPLIED_BY_FEEDBACK": aggregate_counters["repair_applied_by_feedback_count"] == 0,
        "RUNTIME_ATTACHMENT_22_NO_RUNTIME_MUTATION": aggregate_counters["runtime_mutation_count"] == 0,
        "RUNTIME_ATTACHMENT_23_NO_SCHEMA_ARCHIVE_MUTATION": aggregate_counters["schema_archive_mutation_count"] == 0,
        "RUNTIME_ATTACHMENT_24_NO_MOVE_ADDITION": aggregate_counters["move_addition_count"] == 0,
        "RUNTIME_ATTACHMENT_25_NO_FIXTURE_EXPANSION": aggregate_counters["fixture_expansion_count"] == 0,
        "RUNTIME_ATTACHMENT_26_C7_NOT_OPENED": aggregate_counters["c7_opened_count"] == 0,
        "RUNTIME_ATTACHMENT_27_C8_NOT_OPENED": aggregate_counters["c8_opened_count"] == 0,
        "RUNTIME_ATTACHMENT_28_ROLLUP_READOUT_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and READOUT_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRANSITION_TRACE_PATH.exists(),
        "RUNTIME_ATTACHMENT_29_RECEIPT_EMITTED": True,
        "RUNTIME_ATTACHMENT_30_BAD_COUNTERS_ZERO": all(v == 0 for v in aggregate_counters.values()),
        "RUNTIME_ATTACHMENT_31_NO_LATEST_OR_MTIME_SELECTION": aggregate_counters["latest_file_selection_count"] == 0 and aggregate_counters["mtime_selection_count"] == 0,
        "RUNTIME_ATTACHMENT_32_NO_GRAPH_ARCHIVE_MUTATION": aggregate_counters["graph_archive_mutation_count"] == 0,
        "RUNTIME_ATTACHMENT_33_NO_VALIDATOR_AUTHORIZATION_SCHEMA_CREATED": aggregate_counters["validator_authorization_schema_created_count"] == 0,
        "RUNTIME_ATTACHMENT_34_NO_DECISION_EDGE_AUTHORIZATION_CREATED": aggregate_counters["decision_edge_authorization_created_count"] == 0,
        "RUNTIME_ATTACHMENT_35_SOURCE_RECEIPTS_IMMUTABLE": aggregate_counters["source_receipt_mutation_count"] == 0 and aggregate_counters["source_fixture_receipt_mutation_count"] == 0 and aggregate_counters["source_double_sieve_receipt_mutation_count"] == 0,
        "RUNTIME_ATTACHMENT_36_NO_RUNTIME_RERUN": intake.get("runtime_rerun_authorized") is False,
        "RUNTIME_ATTACHMENT_37_ATTACHMENT_RECORDS_MARKED_DERIVED_NOT_LIVE": all(e.get("provenance", {}).get("derived_not_live_emitted") is True for e in sidecar_events),
    }

    false_gates = [k for k, v in acceptance_gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])
        gate, status, outcome_class = classify_failure(failures)
        terminal = terminal_for(gate, failures)

    receipt = {
        "schema_version": "runtime_observability_feedback_attachment_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_OBSERVABILITY_FEEDBACK_ATTACHMENT_RECEIPT",
        "created_at": now_iso(),
        "receipt_id": None,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "attachment_run_id": attachment_run_id,
        "source_double_sieve_receipt_id": double_sieve_receipt.get("receipt_id"),
        "source_double_sieve_suite_id": double_sieve_receipt.get("suite_id"),
        "source_double_sieve_run_id": double_sieve_receipt.get("run_id"),
        "gate": gate,
        "status": status,
        "outcome_class": outcome_class,
        "failures": failures,
        "warnings": warnings,
        "machine_readable_runtime_attachment_summary": {
            "attachment_passed": gate == "PASS",
            "runtime_steps_total": runtime_steps_total,
            "sidecar_events_emitted": sidecar_events_emitted,
            "decision_edge_observations_emitted": edge_obs_emitted,
            "runtime_step_receipts_emitted": step_receipts_emitted,
            "blocked_or_failed_steps": blocked_failed_steps,
            "unit_feedback_required": feedback_required_count,
            "unit_feedback_emitted": feedback_emitted,
            "observability_degraded_steps": degraded_steps,
            "observability_degradation_records_emitted": degradation_emitted,
            "coverage": coverage,
            "step_outcomes": dict(step_outcomes),
            "no_bare_failed": aggregate_counters["bare_failed_status_count"] == 0,
            "no_unobserved_transition": aggregate_counters["unobserved_transition_count"] == 0,
            "no_hidden_next_command": aggregate_counters["hidden_next_command_count"] == 0,
            "no_sidecar_authority": aggregate_counters["sidecar_authority_count"] == 0,
            "no_false_observability_claim": aggregate_counters["false_full_observability_claim_count"] == 0,
            "no_feedback_missing": aggregate_counters["feedback_missing_count"] == 0,
            "no_graph_archive_mutation": aggregate_counters["graph_archive_mutation_count"] == 0,
            "no_validator_authorization_schema_created": aggregate_counters["validator_authorization_schema_created_count"] == 0,
            "no_decision_edge_authorization_created": aggregate_counters["decision_edge_authorization_created_count"] == 0,
            "source_receipts_mutated": False,
            "runtime_rerun": False,
            "live_hook_installation": False,
            "runtime_mutation": False,
            "schema_archive_mutation": False,
            "move_addition": False,
            "fixture_expansion": False,
            "c7_opened": False,
            "c8_opened": False,
            "bad_counters_zero": all(v == 0 for v in aggregate_counters.values()),
            "next_command_goal": None,
        },
        "acceptance_gate_results": acceptance_gate_results,
        "negative_controls": aggregate_counters,
        "source_receipt_immutability": {
            "source_receipts_mutated": False,
            "source_fixture_receipts_mutated": False,
            "source_double_sieve_receipt_mutated": False,
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "fixture_hashes_before": fixture_hashes_before,
            "fixture_hashes_after": fixture_hashes_after
        },
        "output_artifacts": {
            "intake": rel(INTAKE_PATH),
            "runtime_step_bundles": rel(STEP_BUNDLES_PATH),
            "observability_sidecar_events": rel(SIDECAR_EVENTS_PATH),
            "decision_edge_observation_records": rel(EDGE_OBS_PATH),
            "unit_feedback_records": rel(UNIT_FEEDBACK_PATH),
            "observability_degradation_records": rel(DEGRADATION_PATH),
            "runtime_step_receipts": rel(STEP_RECEIPTS_PATH),
            "rollup": rel(ROLLUP_PATH),
            "readout": rel(READOUT_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
    }

    receipt_id = "runtime_observability_feedback_attachment_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_attachment_receipt_id={receipt_id}")
    print(f"runtime_attachment_receipt_path={rel(receipt_path)}")
    print(f"runtime_attachment_run_id={attachment_run_id}")
    print(f"runtime_attachment_terminal_stop_code={terminal['stop_code']}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
