#!/usr/bin/env python3
from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional

SCHEMA_VALIDATOR_RESULTS = {
    "VALID",
    "UNKNOWN_SCHEMA",
    "MISSING_FIELD",
    "TYPE_MISMATCH",
    "UNRESOLVED_REFERENCE",
    "RECEIPT_CONTRACT_INSUFFICIENT",
}

ADMISSIBILITY_RESULTS = {
    "ALLOW",
    "AUTHORITY_REQUIRED",
    "FORBIDDEN_INPUT",
    "UNREGISTERED_MOVE",
    "UNIT_BOUNDARY_EXCEEDED",
    "NOT_RUN",
}

EXECUTION_GATE_RESULTS = {
    "EXECUTION_GATE_OPENED_NO_LIVE_MUTATION",
    "NOT_RUN",
    "FAILED_TYPED",
    "CONTROL_RESULT_PRESERVED_WITH_OBSERVABILITY_DEGRADED",
}

SIDECAR_STATUSES = {
    "OBSERVATION_COMPLETE",
    "OBSERVATION_UNDER_TYPED",
    "NOT_RUN",
}

UNIT_FEEDBACK_STATUSES = {
    "NOT_REQUIRED",
    "EMITTED_ACTIONABLE",
    "MISSING_REQUIRED",
    "BARE_FAILED_BLOCKED",
}

REQUIRED_CANDIDATE_FIELDS = [
    "schema_version",
    "candidate_id",
    "schema_ref",
    "move_type",
    "receipt_contract",
    "authority_request",
    "inputs",
    "execution_boundary",
]

REQUIRED_RECEIPT_CONTRACT_FIELDS = [
    "expected_receipt_type",
    "terminal_required",
    "hidden_next_command_forbidden",
]

KNOWN_SCHEMA_REFS = {
    "runtime_move_candidate_v0",
    "bounded_structured_t6_trigger_surface_capability_v0"
}

ALLOWED_FIXTURE_MOVE_TYPES = {
    "NOOP_FIXTURE_GATE",
    "FIXTURE_TYPED_FAILURE",
    "FIXTURE_OBSERVABILITY_DEGRADED",
}

AUTHORITY_REQUIRED_MOVE_TYPES = {
    "RUNTIME_PATCH",
    "SCHEMA_ARCHIVE_MUTATION",
    "MOVE_REGISTRY_ADDITION",
    "FIXTURE_EXPANSION",
    "C7_CONTINUATION",
    "C8_RESEARCH_LOOP",
    "LIVE_RUNTIME_MUTATION",
}

FORBIDDEN_INPUT_MODES = {
    "latest_file",
    "mtime_selection",
    "repo_wide_discovery",
    "implicit_active_source_selection",
}

def schema_validator(candidate: Dict[str, Any]) -> Dict[str, Any]:
    missing = [field for field in REQUIRED_CANDIDATE_FIELDS if field not in candidate]
    if missing:
        return {
            "schema_version": "schema_validation_result_v0",
            "result": "MISSING_FIELD",
            "valid": False,
            "failure_class": "MISSING_FIELD",
            "failure_location": {
                "field_path": missing[0]
            },
            "blocked_transition": "LAWFUL_ADMISSIBILITY_CELL",
            "lawful_next_handling": [
                "return to Builder / Proposal Cell",
                "repair candidate shape through explicit proposal",
                "rerun schema validation"
            ],
            "forbidden_next_handling": [
                "send to admissibility",
                "execute",
                "treat as authority denial"
            ]
        }

    if not isinstance(candidate.get("receipt_contract"), dict):
        return {
            "schema_version": "schema_validation_result_v0",
            "result": "TYPE_MISMATCH",
            "valid": False,
            "failure_class": "TYPE_MISMATCH",
            "failure_location": {
                "field_path": "receipt_contract"
            },
            "blocked_transition": "LAWFUL_ADMISSIBILITY_CELL",
            "lawful_next_handling": [
                "return typed schema feedback"
            ],
            "forbidden_next_handling": [
                "send to admissibility",
                "execute"
            ]
        }

    schema_ref = candidate.get("schema_ref")
    if schema_ref not in KNOWN_SCHEMA_REFS:
        return {
            "schema_version": "schema_validation_result_v0",
            "result": "UNKNOWN_SCHEMA",
            "valid": False,
            "failure_class": "UNKNOWN_SCHEMA",
            "failure_location": {
                "field_path": "schema_ref"
            },
            "blocked_transition": "LAWFUL_ADMISSIBILITY_CELL",
            "lawful_next_handling": [
                "bind candidate to R0-selected schema surface",
                "or return unknown schema stop"
            ],
            "forbidden_next_handling": [
                "infer schema from repo",
                "execute"
            ]
        }

    receipt_contract = candidate.get("receipt_contract", {})
    missing_receipt_fields = [
        field for field in REQUIRED_RECEIPT_CONTRACT_FIELDS
        if field not in receipt_contract
    ]
    if missing_receipt_fields:
        return {
            "schema_version": "schema_validation_result_v0",
            "result": "RECEIPT_CONTRACT_INSUFFICIENT",
            "valid": False,
            "failure_class": "RECEIPT_CONTRACT_INSUFFICIENT",
            "failure_location": {
                "field_path": f"receipt_contract.{missing_receipt_fields[0]}"
            },
            "blocked_transition": "LAWFUL_ADMISSIBILITY_CELL",
            "lawful_next_handling": [
                "complete receipt contract",
                "rerun schema validation"
            ],
            "forbidden_next_handling": [
                "send to admissibility",
                "execute without receipt contract"
            ]
        }

    return {
        "schema_version": "schema_validation_result_v0",
        "result": "VALID",
        "valid": True,
        "failure_class": None,
        "failure_location": None,
        "blocked_transition": None,
        "lawful_next_handling": [
            "send to Lawful Admissibility Cell"
        ],
        "forbidden_next_handling": [
            "treat schema VALID as execution permission",
            "skip admissibility"
        ]
    }

def lawful_admissibility(candidate: Dict[str, Any], schema_result: Dict[str, Any]) -> Dict[str, Any]:
    if schema_result.get("result") != "VALID":
        return {
            "schema_version": "admissibility_result_v0",
            "result": "NOT_RUN",
            "execution_allowed": False,
            "blocked_move": None,
            "blocked_by": "schema_validation",
            "lawful_next_handling": [
                "preserve schema stop"
            ],
            "forbidden_next_handling": [
                "execute",
                "treat schema stop as authority decision"
            ]
        }

    move_type = candidate.get("move_type")
    inputs = candidate.get("inputs", {})
    execution_boundary = candidate.get("execution_boundary", {})

    input_mode = inputs.get("input_mode")
    if input_mode in FORBIDDEN_INPUT_MODES:
        return {
            "schema_version": "admissibility_result_v0",
            "result": "FORBIDDEN_INPUT",
            "blocked_move": move_type,
            "blocked_by": "input_boundary",
            "forbidden_input_detected": True,
            "execution_allowed": False,
            "lawful_next_handling": [
                "return typed admissibility stop",
                "replace forbidden input with declared source"
            ],
            "forbidden_next_handling": [
                "execute",
                "select latest file",
                "select by mtime",
                "discover active source from repo"
            ]
        }

    if move_type in AUTHORITY_REQUIRED_MOVE_TYPES:
        return {
            "schema_version": "admissibility_result_v0",
            "result": "AUTHORITY_REQUIRED",
            "blocked_move": move_type,
            "blocked_by": "authority_boundary",
            "execution_allowed": False,
            "lawful_next_handling": [
                "return typed halt",
                "request review",
                "emit authority proposal"
            ],
            "forbidden_next_handling": [
                "execute",
                "treat schema-valid as admissible",
                "treat sidecar evidence as permission"
            ]
        }

    if move_type not in ALLOWED_FIXTURE_MOVE_TYPES:
        return {
            "schema_version": "admissibility_result_v0",
            "result": "UNREGISTERED_MOVE",
            "blocked_move": move_type,
            "blocked_by": "move_registry",
            "execution_allowed": False,
            "lawful_next_handling": [
                "return typed admissibility stop",
                "request move registration through separate review"
            ],
            "forbidden_next_handling": [
                "execute unregistered move",
                "add move automatically"
            ]
        }

    if execution_boundary.get("live_mutation") is True:
        return {
            "schema_version": "admissibility_result_v0",
            "result": "UNIT_BOUNDARY_EXCEEDED",
            "blocked_move": move_type,
            "blocked_by": "fixture_only_boundary",
            "execution_allowed": False,
            "lawful_next_handling": [
                "return boundary stop",
                "remove live mutation request"
            ],
            "forbidden_next_handling": [
                "live mutate",
                "patch runtime",
                "open C7"
            ]
        }

    return {
        "schema_version": "admissibility_result_v0",
        "result": "ALLOW",
        "blocked_move": None,
        "blocked_by": None,
        "execution_allowed": True,
        "allowed_scope": "FIXTURE_ONLY_NO_LIVE_MUTATION",
        "lawful_next_handling": [
            "open fixture execution gate only"
        ],
        "forbidden_next_handling": [
            "perform live mutation",
            "treat fixture allow as runtime adoption",
            "open C7",
            "open C8"
        ]
    }

def fixture_execution_harness(candidate: Dict[str, Any], admissibility_result: Dict[str, Any]) -> Dict[str, Any]:
    if admissibility_result.get("result") != "ALLOW":
        return {
            "schema_version": "execution_gate_result_v0",
            "result": "NOT_RUN",
            "execution_gate_opened": False,
            "fixture_execution_attempted": False,
            "live_execution_attempted": False,
            "live_mutation_executed": False,
            "unit_feedback_status": "NOT_REQUIRED",
            "unit_feedback": None
        }

    move_type = candidate.get("move_type")
    inputs = candidate.get("inputs", {})

    if move_type == "FIXTURE_TYPED_FAILURE":
        feedback = {
            "schema_version": "unit_feedback_record_v0",
            "unit_id": "builder_execution.runtime_fixture_v0",
            "terminal_status": "FAIL",
            "diagnostic": {
                "failure_point": "LOAD_TARGET_SURFACE",
                "failed_relative_to_object": inputs.get("target_object", "unknown_target_object"),
                "failed_relative_to_source_surface": inputs.get("target_surface", "missing_target_surface"),
                "failed_relative_to_boundary": "declared_execution_boundary",
                "missing_capability": "target_surface_resolver",
                "blocked_next_moves": [
                    "apply patch",
                    "emit success receipt"
                ],
                "lawful_next_refinement": "declare or create target surface through reviewed proposal before retry"
            },
            "feedback_quality": {
                "quality_class": "ACTIONABLE"
            },
            "safety": {
                "repair_applied": False,
                "retry_authorized": False,
                "authority_expansion": False
            }
        }
        return {
            "schema_version": "execution_gate_result_v0",
            "result": "FAILED_TYPED",
            "execution_gate_opened": True,
            "fixture_execution_attempted": True,
            "live_execution_attempted": False,
            "live_mutation_executed": False,
            "unit_feedback_status": "EMITTED_ACTIONABLE",
            "unit_feedback": feedback
        }

    if move_type == "FIXTURE_OBSERVABILITY_DEGRADED":
        return {
            "schema_version": "execution_gate_result_v0",
            "result": "CONTROL_RESULT_PRESERVED_WITH_OBSERVABILITY_DEGRADED",
            "execution_gate_opened": True,
            "fixture_execution_attempted": True,
            "live_execution_attempted": False,
            "live_mutation_executed": False,
            "control_path_result_preserved": True,
            "unit_feedback_status": "NOT_REQUIRED",
            "unit_feedback": None
        }

    return {
        "schema_version": "execution_gate_result_v0",
        "result": "EXECUTION_GATE_OPENED_NO_LIVE_MUTATION",
        "execution_gate_opened": True,
        "fixture_execution_attempted": False,
        "live_execution_attempted": False,
        "live_mutation_executed": False,
        "unit_feedback_status": "NOT_REQUIRED",
        "unit_feedback": None
    }

def observability_sidecar(candidate: Dict[str, Any], event: Dict[str, Any]) -> Dict[str, Any]:
    required_fields = [
        "event_kind",
        "schema_result",
        "admissibility_result",
        "authority_boundary",
        "execution_result",
        "terminal"
    ]
    missing = [
        field for field in required_fields
        if field not in event or event.get(field) is None
    ]

    if missing:
        return {
            "schema_version": "observability_sidecar_receipt_v0",
            "sidecar_status": "OBSERVATION_UNDER_TYPED",
            "missing_fields": [
                {
                    "event_kind": event.get("event_kind", "unknown_event"),
                    "field_path": missing[0]
                }
            ],
            "effects": {
                "control_path_modified": False,
                "authority_decision_modified": False,
                "runtime_result_overridden": False,
                "full_observability_claim_allowed": False
            },
            "negative_controls": {
                "sidecar_authorized_move_count": 0,
                "sidecar_denied_move_count": 0,
                "sidecar_state_mutation_count": 0,
                "false_full_observability_claim_count": 0
            },
            "sidecar_authority_status": "ZERO_AUTHORITY"
        }

    return {
        "schema_version": "observability_sidecar_receipt_v0",
        "sidecar_status": "OBSERVATION_COMPLETE",
        "missing_fields": [],
        "effects": {
            "control_path_modified": False,
            "authority_decision_modified": False,
            "runtime_result_overridden": False,
            "full_observability_claim_allowed": True
        },
        "negative_controls": {
            "sidecar_authorized_move_count": 0,
            "sidecar_denied_move_count": 0,
            "sidecar_state_mutation_count": 0,
            "false_full_observability_claim_count": 0
        },
        "sidecar_authority_status": "ZERO_AUTHORITY"
    }

def run_fixture_mode_membrane(candidate: Dict[str, Any], *, sidecar_omit_field: Optional[str] = None) -> Dict[str, Any]:
    candidate_copy = deepcopy(candidate)

    schema_result = schema_validator(candidate_copy)
    admissibility_result = lawful_admissibility(candidate_copy, schema_result)
    execution_result = fixture_execution_harness(candidate_copy, admissibility_result)

    terminal = {
        "type": "STOP",
        "stop_code": _terminal_stop_code(schema_result, admissibility_result, execution_result, sidecar_omit_field),
        "next_command_goal": None
    }

    event = {
        "event_kind": "runtime_membrane_fixture_event",
        "schema_result": schema_result.get("result"),
        "admissibility_result": admissibility_result.get("result"),
        "authority_boundary": {
            "fixture_only": True,
            "live_mutation_authorized": False,
            "sidecar_authority": False
        },
        "execution_result": execution_result.get("result"),
        "terminal": terminal
    }

    if sidecar_omit_field:
        event.pop(sidecar_omit_field, None)

    sidecar_result = observability_sidecar(candidate_copy, event)

    proof_flags = {
        "schema_ran": True,
        "admissibility_ran": schema_result.get("result") == "VALID",
        "execution_ran": admissibility_result.get("result") == "ALLOW",
        "sidecar_ran": True,
        "unit_feedback_ran": execution_result.get("unit_feedback_status") == "EMITTED_ACTIONABLE"
    }

    negative_controls = {
        "invalid_schema_reached_admissibility_count": 0 if schema_result.get("result") == "VALID" or admissibility_result.get("result") == "NOT_RUN" else 1,
        "schema_valid_counted_as_admissible_count": 0,
        "admissibility_denied_executed_count": 0 if admissibility_result.get("result") == "ALLOW" or execution_result.get("result") == "NOT_RUN" else 1,
        "forbidden_input_executed_count": 0,
        "sidecar_authorized_move_count": sidecar_result["negative_controls"]["sidecar_authorized_move_count"],
        "sidecar_denied_move_count": sidecar_result["negative_controls"]["sidecar_denied_move_count"],
        "sidecar_state_mutation_count": sidecar_result["negative_controls"]["sidecar_state_mutation_count"],
        "false_observability_claim_count": sidecar_result["negative_controls"]["false_full_observability_claim_count"],
        "bare_failed_status_count": 0 if execution_result.get("result") != "FAILED" else 1,
        "live_mutation_count": 1 if execution_result.get("live_mutation_executed") else 0,
        "c7_opened_count": 0,
        "c8_opened_count": 0,
        "hidden_next_command_count": 0,
    }

    return {
        "schema_version": "runtime_membrane_fixture_harness_result_v0",
        "candidate_id": candidate_copy.get("candidate_id"),
        "schema_result": schema_result,
        "admissibility_result": admissibility_result,
        "execution_result": execution_result,
        "sidecar_result": sidecar_result,
        "proof_flags": proof_flags,
        "negative_controls": negative_controls,
        "terminal": terminal
    }

def _terminal_stop_code(
    schema_result: Dict[str, Any],
    admissibility_result: Dict[str, Any],
    execution_result: Dict[str, Any],
    sidecar_omit_field: Optional[str],
) -> str:
    if schema_result.get("result") != "VALID":
        return "STOP_SCHEMA_VALIDATION_FAILED"
    if admissibility_result.get("result") == "AUTHORITY_REQUIRED":
        return "STOP_AUTHORITY_REQUIRED"
    if admissibility_result.get("result") == "FORBIDDEN_INPUT":
        return "STOP_FORBIDDEN_INPUT"
    if admissibility_result.get("result") == "UNREGISTERED_MOVE":
        return "STOP_UNREGISTERED_MOVE"
    if admissibility_result.get("result") == "UNIT_BOUNDARY_EXCEEDED":
        return "STOP_UNIT_BOUNDARY_EXCEEDED"
    if execution_result.get("result") == "FAILED_TYPED":
        return "STOP_FIXTURE_EXECUTION_FAILED_TYPED"
    if sidecar_omit_field:
        return "STOP_OBSERVABILITY_DEGRADED_NO_FALSE_CLAIM"
    if execution_result.get("result") == "CONTROL_RESULT_PRESERVED_WITH_OBSERVABILITY_DEGRADED":
        return "STOP_CONTROL_RESULT_PRESERVED_WITH_OBSERVABILITY_DEGRADED"
    return "STOP_EXECUTION_GATE_OPENED_NO_LIVE_MUTATION"
