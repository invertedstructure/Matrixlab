#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_MOVE_REGISTRY_V0_POLICY_V0"
NEXT_GOAL = "IMPLEMENT_MOVE_REGISTRY_V0_WITH_DEMO_RUNS_V0"

TARGET_UNIT_ID = "move_registry.v0"

HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID = "75eabbe2"
HALT_VOCABULARY_POLICY_ID = "0707a2d7"
PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID = "363d2f4a"
TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID = "cc24a11f"
TRACE_SCHEMA_ID = "b4887660"
PROPOSAL_LEDGER_SCHEMA_ID = "eee2a318"
LOCAL_REGIME_V1_HASH = "25802530"

HALT_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "halt_vocabulary_v0_implementation_receipts" / f"{HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID}.json"
HALT_POLICY_PATH = ROOT / "data" / "halt_vocabulary_v0_policies" / f"{HALT_VOCABULARY_POLICY_ID}.json"
HALT_VOCABULARY_PATH = ROOT / "data" / "halt_vocabulary_v0" / "halt_vocabulary_v0.json"
HALT_RECORD_SCHEMA_PATH = ROOT / "data" / "halt_record_schemas" / "halt_record_schema_v0.json"
HALT_NEXT_HANDLING_PATH = ROOT / "data" / "halt_to_next_handling_tables" / "halt_to_next_handling_table_v0.json"
PROCEED_RECEIPT_PATH = ROOT / "data" / "proceed_adapter_v0_implementation_receipts" / f"{PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID}.json"
PROCEED_ADAPTER_MODULE_PATH = ROOT / "src" / "matrixlab" / "proceed_adapter_v0.py"
TRACE_LEDGER_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts" / f"{TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID}.json"
TRACE_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_schemas" / f"{TRACE_SCHEMA_ID}.json"
PROPOSAL_LEDGER_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposal_ledger_schemas" / f"{PROPOSAL_LEDGER_SCHEMA_ID}.json"
TRACE_LEDGER_RUNNER_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_2_trace_ledger.py"
LOCAL_REGIME_V1_PATH = ROOT / "data" / "local_regime_v1_declarations" / f"{LOCAL_REGIME_V1_HASH}.json"

OUT_DIR = ROOT / "data" / "move_registry_v0_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "move_registry_v0_policy_receipts"

REQUIRED_MOVE_FIELDS = [
    "move_id",
    "schema_version",
    "move_kind",
    "layer",
    "priority",
    "applies_when",
    "allowed_inputs",
    "forbidden_inputs",
    "action",
    "state_delta",
    "emits",
    "may_halt",
    "halt_map",
    "non_impersonation",
]

MOVE_KIND_ENUM = {
    "schema_version": "move_kind_enum_v0",
    "allowed_move_kinds": [
        "CONTROL_CHECK",
        "CONTROL_INSPECT",
        "CONTROL_SELECT",
        "CONTROL_EMIT",
        "LOCAL_REPAIR",
        "DOMAIN_TRANSFORM",
        "PROPOSAL_ONLY",
    ],
    "meanings": {
        "CONTROL_CHECK": "validate state, regime, schema, or gate conditions",
        "CONTROL_INSPECT": "compute applicable, admissible, and blocked move sets",
        "CONTROL_SELECT": "select one admissible move deterministically",
        "CONTROL_EMIT": "emit trace, receipt, readout, halt record, or terminal context",
        "LOCAL_REPAIR": "repair local projection or receipt gotcha only",
        "DOMAIN_TRANSFORM": "change the active object or state payload",
        "PROPOSAL_ONLY": "emit proposal pressure only; never self-accept or mutate registry",
    },
}

MOVE_LIFECYCLE = {
    "schema_version": "move_lifecycle_v0",
    "ordered_states": [
        "DRAFTED",
        "REGISTERED",
        "SCHEMA_VALID",
        "APPLICABLE",
        "ADMISSIBLE_PRE_AUTH",
        "SELECTED",
        "APPLIED",
        "TRACED",
        "RECEIPTED",
    ],
    "execution_law": [
        "Only REGISTERED + SCHEMA_VALID + APPLICABLE + ADMISSIBLE_PRE_AUTH + SELECTED moves may execute in Day 4.",
        "Day 4 admissibility is pre-authorization only.",
        "Day 5 resolves jurisdiction/authorization.",
        "PROPOSAL_ONLY moves may emit proposal pressure but may not register, accept, or execute candidate moves.",
    ],
}

APPLIES_WHEN_PREDICATE_SCHEMA = {
    "schema_version": "applies_when_predicate_schema_v0",
    "allowed_operators": ["eq", "neq", "exists", "missing", "in", "not", "all", "any"],
    "no_free_form_code": True,
    "path_reference_style": "dot_path_against_declared_state_or_readout",
    "examples": [
        {"eq": ["state.status", "LOADED"]},
        {"missing": "state.receipt_ref"},
        {"all": [
            {"eq": ["readout.verification_status", "FAIL"]},
            {"eq": ["readout.failure_kind", "PROJECTION_MISMATCH"]},
        ]},
    ],
}

MOVE_SCHEMA = {
    "schema_version": "move_schema_v0",
    "required_fields": REQUIRED_MOVE_FIELDS,
    "field_meanings": {
        "move_id": "stable unique identifier for the registered move",
        "schema_version": "must equal move_schema_v0",
        "move_kind": "one of move_kind_enum_v0",
        "layer": "declared execution/inspection layer",
        "priority": "integer; lower number selected first by selector_priority_v0",
        "applies_when": "bounded predicate grammar, no arbitrary code",
        "allowed_inputs": "declared inputs the move may use",
        "forbidden_inputs": "explicit forbidden inputs/authority patterns",
        "action": "bounded action declaration",
        "state_delta": "declared state change on pass/fail",
        "emits": "declared emitted artifacts",
        "may_halt": "whether the move may produce STOP(stop_code)",
        "halt_map": "declared halt behavior for failure/terminal cases",
        "non_impersonation": "what this move must not pretend to prove/authorize",
    },
    "core_law": "No unregistered move may fire. No schema-invalid move may fire.",
}

COMMON_FORBIDDEN_INPUTS = [
    "chat_memory_authority",
    "latest_file_guessing",
    "mtime_selection",
    "ambient_workspace_inference",
    "unregistered_code_behavior",
    "architecture_widening",
    "unreviewed_taxonomy_promotion",
    "unreviewed_move_registration",
]

STARTER_MOVES = {
    "state.validate_shape.v0": {
        "move_id": "state.validate_shape.v0",
        "schema_version": "move_schema_v0",
        "move_kind": "CONTROL_CHECK",
        "layer": "OUTER",
        "priority": 10,
        "applies_when": {"eq": ["state.status", "LOADED"]},
        "allowed_inputs": ["current_state"],
        "forbidden_inputs": COMMON_FORBIDDEN_INPUTS,
        "action": {"type": "CHECK", "name": "validate_required_state_fields"},
        "state_delta": {"on_pass": {"state.status": "VALID"}, "on_fail": {"state.status": "INVALID"}},
        "emits": ["trace_entry"],
        "may_halt": True,
        "halt_map": {"on_fail": "INVALID_STATE"},
        "non_impersonation": ["does not prove theorem content", "does not prove engine completion"],
    },
    "regime.validate_shape.v0": {
        "move_id": "regime.validate_shape.v0",
        "schema_version": "move_schema_v0",
        "move_kind": "CONTROL_CHECK",
        "layer": "OUTER",
        "priority": 20,
        "applies_when": {"all": [
            {"eq": ["state.status", "VALID"]},
            {"missing": "regime.validation_status"},
        ]},
        "allowed_inputs": ["current_state", "declared_regime", "move_registry_ref"],
        "forbidden_inputs": COMMON_FORBIDDEN_INPUTS,
        "action": {"type": "CHECK", "name": "validate_regime_and_registry_refs"},
        "state_delta": {"on_pass": {"regime.validation_status": "PASS"}, "on_fail": {"regime.validation_status": "FAIL"}},
        "emits": ["trace_entry"],
        "may_halt": True,
        "halt_map": {"on_fail": "INVALID_REGIME"},
        "non_impersonation": ["does not replace regime", "does not authorize registry mutation"],
    },
    "moves.compute_applicable.v0": {
        "move_id": "moves.compute_applicable.v0",
        "schema_version": "move_schema_v0",
        "move_kind": "CONTROL_INSPECT",
        "layer": "MOVE_SPACE",
        "priority": 30,
        "applies_when": {"all": [
            {"eq": ["state.status", "VALID"]},
            {"eq": ["regime.validation_status", "PASS"]},
            {"missing": "state.move_inspection_ref"},
        ]},
        "allowed_inputs": ["current_state", "move_registry_v0", "halt_vocabulary_v0"],
        "forbidden_inputs": COMMON_FORBIDDEN_INPUTS,
        "action": {"type": "INSPECT", "name": "compute_applicable_admissible_blocked_moves"},
        "state_delta": {"on_pass": {"state.move_inspection_ref": "<inspection_id>"}, "on_fail": {"state.halt_code": "STOP_GATE_FAIL"}},
        "emits": ["applicable_move_inspection", "blocked_move_records"],
        "may_halt": True,
        "halt_map": {
            "on_no_applicable_move": "STOP_NO_APPLICABLE_MOVE",
            "on_missing_move_pressure": "STOP_NEEDS_NEW_MOVE",
            "on_fail": "STOP_GATE_FAIL",
        },
        "non_impersonation": ["does not execute moves", "does not authorize moves", "does not register missing moves"],
    },
    "selector.choose_move.v0": {
        "move_id": "selector.choose_move.v0",
        "schema_version": "move_schema_v0",
        "move_kind": "CONTROL_SELECT",
        "layer": "MOVE_SPACE",
        "priority": 40,
        "applies_when": {"all": [
            {"exists": "state.move_inspection_ref"},
            {"missing": "state.selected_move"},
        ]},
        "allowed_inputs": ["applicable_move_inspection", "selector_priority_v0"],
        "forbidden_inputs": COMMON_FORBIDDEN_INPUTS,
        "action": {"type": "SELECT", "name": "select_lowest_priority_admissible_pre_auth_move"},
        "state_delta": {"on_pass": {"state.selected_move": "<move_id>"}, "on_fail": {"state.halt_code": "STOP_GATE_FAIL"}},
        "emits": ["selected_move_record", "trace_entry"],
        "may_halt": True,
        "halt_map": {"on_no_admissible_move": "STOP_NO_APPLICABLE_MOVE", "on_ambiguous_selector": "STOP_GATE_FAIL"},
        "non_impersonation": ["selection is not authorization", "selection is not execution"],
    },
    "unit.mark_complete.v0": {
        "move_id": "unit.mark_complete.v0",
        "schema_version": "move_schema_v0",
        "move_kind": "DOMAIN_TRANSFORM",
        "layer": "OUTER",
        "priority": 50,
        "applies_when": {"all": [
            {"eq": ["state.active_object.object_kind", "BUILD_UNIT"]},
            {"eq": ["state.active_object.completion_status", "PENDING"]},
        ]},
        "allowed_inputs": ["current_state", "selected_move_record"],
        "forbidden_inputs": COMMON_FORBIDDEN_INPUTS,
        "action": {"type": "TRANSFORM", "name": "mark_current_build_unit_complete"},
        "state_delta": {
            "on_pass": {
                "state.active_object.completion_status": "COMPLETE",
                "state.terminal_result": {"type": "STOP", "stop_code": "STOP_NEXT_MOVE_BOUNDARY"},
            },
            "on_fail": {"state.halt_code": "STOP_GATE_FAIL"},
        },
        "emits": ["trace_entry"],
        "may_halt": True,
        "halt_map": {"on_success": "STOP_NEXT_MOVE_BOUNDARY", "on_fail": "STOP_GATE_FAIL"},
        "non_impersonation": ["does not imply global completion", "does not authorize next unit implicitly"],
    },
    "receipt.emit_terminal.v0": {
        "move_id": "receipt.emit_terminal.v0",
        "schema_version": "move_schema_v0",
        "move_kind": "CONTROL_EMIT",
        "layer": "RECEIPT_TRACE",
        "priority": 60,
        "applies_when": {"any": [
            {"exists": "state.terminal_result"},
            {"exists": "state.halt_code"},
        ]},
        "allowed_inputs": ["current_state", "trace_context", "halt_vocabulary_v0"],
        "forbidden_inputs": COMMON_FORBIDDEN_INPUTS,
        "action": {"type": "EMIT", "name": "emit_terminal_receipt_and_move_context"},
        "state_delta": {"on_pass": {"state.receipt_ref": "<receipt_ref>"}, "on_fail": {"state.halt_code": "STOP_RECEIPT_MISMATCH"}},
        "emits": ["trace_entry", "receipt", "readout"],
        "may_halt": True,
        "halt_map": {"on_fail": "STOP_RECEIPT_MISMATCH"},
        "non_impersonation": ["receipt emission is not proof", "terminal receipt is not implicit continuation"],
    },
    "proposal.missing_move.draft.v0": {
        "move_id": "proposal.missing_move.draft.v0",
        "schema_version": "move_schema_v0",
        "move_kind": "PROPOSAL_ONLY",
        "layer": "MOVE_SPACE",
        "priority": 70,
        "applies_when": {"eq": ["state.halt_code", "STOP_NEEDS_NEW_MOVE"]},
        "allowed_inputs": ["current_state", "missing_move_pressure", "halt_vocabulary_v0"],
        "forbidden_inputs": COMMON_FORBIDDEN_INPUTS,
        "action": {"type": "PROPOSE", "name": "draft_smallest_missing_move_candidate"},
        "state_delta": {"on_pass": {"state.missing_move_proposal_ref": "<proposal_id>"}, "on_fail": {"state.halt_code": "STOP_GATE_FAIL"}},
        "emits": ["missing_move_proposal_stub"],
        "may_halt": True,
        "halt_map": {"on_fail": "STOP_GATE_FAIL"},
        "non_impersonation": ["does not register candidate move", "does not accept taxonomy delta", "does not authorize execution"],
    },
}

MOVE_REGISTRY = {
    "schema_version": "move_registry_schema_v0",
    "move_registry_id": "move_registry_v0",
    "selection_policy": "lowest_priority_number",
    "selector_id": "selector_priority_v0",
    "moves": STARTER_MOVES,
    "registry_law": [
        "no unregistered move may fire",
        "no move with failed schema validation may fire",
        "no move with forbidden input pressure may fire",
        "proposal-only moves may not mutate registry",
        "Day 4 admission is pre-authorization; Day 5 handles jurisdiction",
    ],
}

MOVE_ADMISSION_GATE = {
    "schema_version": "move_admission_gate_v0",
    "admission_status_name": "ADMISSIBLE_PRE_AUTH",
    "authorization_status": "DEFERRED_TO_DAY5",
    "admissible_pre_auth_iff": [
        "registered(move)",
        "schema_valid(move)",
        "applies_when_true(move,state)",
        "allowed_inputs_available(move,state)",
        "forbidden_inputs_absent(move,state)",
        "halt_map_complete(move)",
        "action_is_bounded(move)",
    ],
    "day4_may_check": [
        "declared inputs are present",
        "forbidden inputs are absent",
        "move does not require undeclared/ambient input",
        "halt behavior is declared",
        "action is bounded by schema",
    ],
    "day4_must_not_decide": [
        "jurisdiction authority",
        "human authorization",
        "global permission to execute outside declared surface",
    ],
    "halt_on_failure_policy": {
        "no_applicable": "STOP_NO_APPLICABLE_MOVE",
        "missing_move_pressure": "STOP_NEEDS_NEW_MOVE",
        "forbidden_input_required": "STOP_AUTHORITY_VIOLATION",
        "gate_failure": "STOP_GATE_FAIL",
    },
}

BLOCKED_MOVE_RECORD_SCHEMA = {
    "schema_version": "blocked_move_record_schema_v0",
    "required_fields": [
        "blocked_move_id",
        "move_id",
        "state_sig8",
        "block_reason",
        "details",
        "halt_pressure",
        "must_not_impersonate",
    ],
    "block_reasons": [
        "SCHEMA_INVALID",
        "APPLIES_WHEN_FALSE",
        "ALLOWED_INPUT_MISSING",
        "FORBIDDEN_INPUT_REQUIRED",
        "HALT_MAP_INCOMPLETE",
        "ACTION_UNBOUNDED",
        "AUTHORITY_DEFERRED",
        "NEEDS_EXTRACTION",
        "UNKNOWN_BLOCK",
    ],
    "authority_deferred_law": {
        "does_not_mean_STOP_AUTHORITY_VIOLATION": True,
        "meaning": "move may require authority classification beyond Day 4; Day 5 resolves it",
    },
}

APPLICABLE_MOVE_INSPECTION_SCHEMA = {
    "schema_version": "applicable_move_inspection_schema_v0",
    "required_fields": [
        "inspection_id",
        "state_sig8",
        "move_registry_id",
        "registered_count",
        "schema_valid_moves",
        "applicable_moves",
        "admissible_pre_auth_moves",
        "blocked_moves",
        "selected_move",
        "selection_basis",
        "authorization_status",
    ],
    "audit_law": [
        "registered candidates must be visible",
        "blocked moves must have reasons",
        "admissible_pre_auth must be distinct from applicable",
        "selected move must be deterministic",
    ],
}

SELECTED_MOVE_RECORD_SCHEMA = {
    "schema_version": "selected_move_record_schema_v0",
    "required_fields": [
        "selected_move_record_id",
        "inspection_id",
        "selected_move",
        "selection_policy",
        "selection_basis",
        "candidate_count",
        "tie_breaker",
        "authorization_status",
    ],
    "selection_law": {
        "selector_is_deterministic": True,
        "authorization_status": "DEFERRED_TO_DAY5",
        "selected_does_not_mean_authorized": True,
    },
}

MISSING_MOVE_PROPOSAL_STUB = {
    "schema_version": "missing_move_proposal_stub_v0",
    "proposal_type": "MISSING_MOVE",
    "trigger_halt": "STOP_NEEDS_NEW_MOVE",
    "status": "PROPOSED_ONLY",
    "candidate_move_required_fields": [
        "move_id",
        "move_kind",
        "applies_when",
        "action",
        "emits",
        "halt_behavior",
    ],
    "hard_rules": {
        "may_not_write_move_registry": True,
        "may_not_register_candidate_move": True,
        "may_not_execute_candidate_move": True,
        "may_not_mark_candidate_accepted": True,
        "may_not_promote_taxonomy_delta": True,
    },
    "must_not_impersonate": [
        "registered move",
        "accepted taxonomy delta",
        "authorized execution",
    ],
    "allowed_next_handling": [
        "human review",
        "accept into registry in later reviewed unit",
        "reject",
        "defer",
        "weaken proposal",
    ],
}

TRACE_MOVE_CONTEXT_PATCH = {
    "schema_version": "trace_move_context_patch_v0",
    "patch_mode": "future_schema_patch_only_do_not_mutate_existing_traces",
    "add_fields": {
        "move_registry_id": "move_registry_v0",
        "applicable_moves": ["<move_id>"],
        "admissible_pre_auth_moves": ["<move_id>"],
        "blocked_moves": [{"move_id": "<move_id>", "reason": "<block_reason>"}],
        "selected_move": "<move_id|null>",
        "selection_reason": "<selection_basis|null>",
        "move_admission_status": "ADMISSIBLE_PRE_AUTH|BLOCKED|NONE",
        "authorization_status": "DEFERRED_TO_DAY5",
    },
}

RECEIPT_MOVE_REGISTRY_PATCH = {
    "schema_version": "receipt_move_registry_patch_v0",
    "patch_mode": "future_schema_patch_only_do_not_mutate_existing_receipts",
    "add_fields": {
        "move_registry": {
            "move_registry_id": "move_registry_v0",
            "move_registry_sig8": "<sig8>",
            "registered_count": 7,
        },
        "moves": {
            "moves_inspected": 7,
            "moves_applied": ["<move_id>"],
            "blocked_moves_count": "<int>",
            "unregistered_attempts": 0,
        },
    },
    "acceptance_invariant": {
        "unregistered_attempts_must_equal_zero": True,
        "violation_halt": "STOP_AUTHORITY_VIOLATION_OR_STOP_GATE_FAIL",
    },
}

PROCEED_READOUT_MOVE_CONTEXT_PATCH = {
    "schema_version": "proceed_readout_move_context_patch_v0",
    "patch_mode": "future_schema_patch_only_do_not_mutate_existing_readouts",
    "add_fields": {
        "move_inspection_ref": "<inspection_id>",
        "selected_move_record_ref": "<selected_move_record_id|null>",
        "authorization_status": "DEFERRED_TO_DAY5",
        "missing_move_proposal_ref": "<proposal_id|null>",
    },
}

DAY4_DEMO_POSITIVE_RUN_PLAN = {
    "schema_version": "day4_demo_positive_run_plan_v0",
    "demo_name": "DAY4_POSITIVE_BUILD_UNIT_COMPLETION",
    "initial_state": {
        "state_id": "state_demo_day4_positive",
        "schema_version": "runner_state_v0",
        "status": "LOADED",
        "active_object": {
            "object_id": "unit.demo_001",
            "object_kind": "BUILD_UNIT",
            "completion_status": "PENDING",
        },
        "regime": {
            "move_registry_id": "move_registry_v0",
            "selector_id": "selector_priority_v0",
        },
    },
    "expected_move_sequence": [
        "state.validate_shape.v0",
        "regime.validate_shape.v0",
        "moves.compute_applicable.v0",
        "selector.choose_move.v0",
        "unit.mark_complete.v0",
        "receipt.emit_terminal.v0",
    ],
    "expected_terminal_result": {
        "type": "STOP",
        "stop_code": "STOP_NEXT_MOVE_BOUNDARY",
    },
    "expected_meaning": "current unit completed; next action is a separate unit; no implicit continuation",
}

DAY4_DEMO_MISSING_MOVE_RUN_PLAN = {
    "schema_version": "day4_demo_missing_move_run_plan_v0",
    "demo_name": "DAY4_MISSING_MOVE_PRESSURE",
    "initial_state": {
        "state_id": "state_demo_day4_missing_move",
        "schema_version": "runner_state_v0",
        "status": "VALID",
        "active_object": {
            "object_id": "unit.demo_002",
            "object_kind": "BUILD_UNIT",
            "completion_status": "COMPLETE",
            "needs_next_boundary": True,
        },
        "regime": {
            "validation_status": "PASS",
            "move_registry_id": "move_registry_v0",
            "selector_id": "selector_priority_v0",
        },
        "registered_moves_do_not_include": ["boundary.emit_next_unit.v0"],
        "terminal_result": None,
    },
    "expected_terminal_result": {
        "type": "STOP",
        "stop_code": "STOP_NEEDS_NEW_MOVE",
    },
    "expected_missing_move_proposal": {
        "proposal_type": "MISSING_MOVE",
        "candidate_move_id": "boundary.emit_next_unit.v0",
        "status": "PROPOSED_ONLY",
        "must_not_register": True,
        "must_not_execute": True,
    },
}

REQUIRED_IMPLEMENTATION_ARTIFACTS = {
    "move_schema": "data/move_registry_v0/move_schema_v0.json",
    "move_kind_enum": "data/move_registry_v0/move_kind_enum_v0.json",
    "applies_when_predicate_schema": "data/move_registry_v0/applies_when_predicate_schema_v0.json",
    "move_lifecycle": "data/move_registry_v0/move_lifecycle_v0.json",
    "move_registry": "data/move_registry_v0/move_registry_v0.json",
    "move_admission_gate": "data/move_registry_v0/move_admission_gate_v0.json",
    "blocked_move_record_schema": "data/move_registry_v0/blocked_move_record_schema_v0.json",
    "applicable_move_inspection_schema": "data/move_registry_v0/applicable_move_inspection_schema_v0.json",
    "selected_move_record_schema": "data/move_registry_v0/selected_move_record_schema_v0.json",
    "missing_move_proposal_stub": "data/move_registry_v0/missing_move_proposal_stub_v0.json",
    "trace_move_context_patch": "data/move_registry_v0_patches/trace_move_context_patch_v0.json",
    "receipt_move_registry_patch": "data/move_registry_v0_patches/receipt_move_registry_patch_v0.json",
    "proceed_readout_move_context_patch": "data/move_registry_v0_patches/proceed_readout_move_context_patch_v0.json",
    "day4_demo_positive_run": "data/move_registry_v0_demo/day4_demo_positive_run.json",
    "day4_demo_missing_move_run": "data/move_registry_v0_demo/day4_demo_missing_move_run.json",
    "day4_demo_move_run_receipt": "data/move_registry_v0_demo/day4_demo_move_run_receipt.json",
    "implementation_receipt": "data/move_registry_v0_implementation_receipts/<receipt_id>.json",
}

ACCEPTANCE_GATES = {
    "MRP0_source_surface_verified": {
        "required": True,
        "description": "Day 3 halt vocabulary, Day 2 proceed adapter, trace-ledger runner, and local regime sources are tracked and path-addressed.",
    },
    "MRP1_move_schema_required_fields_declared": {
        "required": True,
        "description": "move_schema_v0 declares all required move fields.",
    },
    "MRP2_predicate_grammar_bounded": {
        "required": True,
        "description": "applies_when grammar uses only bounded predicate operators and no arbitrary code.",
    },
    "MRP3_registry_contains_only_starter_moves": {
        "required": True,
        "description": "move_registry_v0 contains the seven starter moves only.",
    },
    "MRP4_no_unregistered_move_may_fire": {
        "required": True,
        "description": "registry law forbids unregistered moves from firing.",
    },
    "MRP5_applicable_admissible_selected_are_separate": {
        "required": True,
        "description": "inspection/admission/selection schemas separate registered, applicable, admissible_pre_auth, selected, and authorized.",
    },
    "MRP6_blocked_moves_require_records": {
        "required": True,
        "description": "blocked_move_record_schema_v0 records every blocked move with reason and anti-impersonation.",
    },
    "MRP7_selector_deterministic": {
        "required": True,
        "description": "selector_priority_v0 chooses deterministic lowest priority number.",
    },
    "MRP8_missing_move_pressure_emits_stop_needs_new_move": {
        "required": True,
        "description": "visible missing move pressure routes to STOP_NEEDS_NEW_MOVE.",
    },
    "MRP9_missing_move_proposal_is_proposed_only": {
        "required": True,
        "description": "missing move proposal stub is PROPOSED_ONLY and cannot mutate registry.",
    },
    "MRP10_no_taxonomy_or_registry_mutation_from_proposal": {
        "required": True,
        "description": "proposal-only move cannot promote taxonomy or register candidate move.",
    },
    "MRP11_day5_authority_not_implemented": {
        "required": True,
        "description": "Day 4 records authorization_status=DEFERRED_TO_DAY5 and does not resolve jurisdiction.",
    },
    "MRP12_patch_artifacts_only_no_old_schema_mutation": {
        "required": True,
        "description": "trace/receipt/readout move-context patches are future-schema patches only.",
    },
}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def tracked(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def validate_predicate(predicate: Any, failures: List[str], context: str) -> None:
    allowed = set(APPLIES_WHEN_PREDICATE_SCHEMA["allowed_operators"])
    if not isinstance(predicate, dict) or len(predicate) != 1:
        failures.append(f"{context}:predicate_malformed:{predicate}")
        return
    op, arg = next(iter(predicate.items()))
    if op not in allowed:
        failures.append(f"{context}:predicate_operator_not_allowed:{op}")
        return
    if op in {"eq", "neq", "in"}:
        if not isinstance(arg, list) or len(arg) != 2:
            failures.append(f"{context}:predicate_{op}_arity_wrong:{arg}")
    elif op in {"exists", "missing"}:
        if not isinstance(arg, str):
            failures.append(f"{context}:predicate_{op}_expects_path:{arg}")
    elif op == "not":
        validate_predicate(arg, failures, context + ".not")
    elif op in {"all", "any"}:
        if not isinstance(arg, list) or not arg:
            failures.append(f"{context}:predicate_{op}_expects_nonempty_list:{arg}")
        else:
            for idx, item in enumerate(arg):
                validate_predicate(item, failures, context + f".{op}[{idx}]")

def validate_move_schema_and_registry() -> List[str]:
    failures: List[str] = []

    for field in REQUIRED_MOVE_FIELDS:
        if field not in MOVE_SCHEMA["required_fields"]:
            failures.append(f"move_schema_required_field_missing:{field}")

    expected_moves = {
        "state.validate_shape.v0",
        "regime.validate_shape.v0",
        "moves.compute_applicable.v0",
        "selector.choose_move.v0",
        "unit.mark_complete.v0",
        "receipt.emit_terminal.v0",
        "proposal.missing_move.draft.v0",
    }

    registry_moves = set(MOVE_REGISTRY["moves"].keys())
    if registry_moves != expected_moves:
        failures.append(f"starter_registry_mismatch:{sorted(registry_moves)}")

    for move_id, move in MOVE_REGISTRY["moves"].items():
        for field in REQUIRED_MOVE_FIELDS:
            if field not in move:
                failures.append(f"{move_id}:required_field_missing:{field}")
        if move.get("move_id") != move_id:
            failures.append(f"{move_id}:move_id_mismatch:{move.get('move_id')}")
        if move.get("schema_version") != "move_schema_v0":
            failures.append(f"{move_id}:schema_version_wrong:{move.get('schema_version')}")
        if move.get("move_kind") not in MOVE_KIND_ENUM["allowed_move_kinds"]:
            failures.append(f"{move_id}:move_kind_unknown:{move.get('move_kind')}")
        if not isinstance(move.get("priority"), int):
            failures.append(f"{move_id}:priority_not_int:{move.get('priority')}")
        validate_predicate(move.get("applies_when"), failures, f"{move_id}.applies_when")
        if not isinstance(move.get("allowed_inputs"), list) or not move.get("allowed_inputs"):
            failures.append(f"{move_id}:allowed_inputs_missing")
        if not isinstance(move.get("forbidden_inputs"), list):
            failures.append(f"{move_id}:forbidden_inputs_not_list")
        for forbidden in ["latest_file_guessing", "mtime_selection", "ambient_workspace_inference", "unregistered_code_behavior"]:
            if forbidden not in move.get("forbidden_inputs", []):
                failures.append(f"{move_id}:common_forbidden_input_missing:{forbidden}")
        if not isinstance(move.get("action"), dict) or "type" not in move.get("action", {}) or "name" not in move.get("action", {}):
            failures.append(f"{move_id}:action_malformed")
        if not isinstance(move.get("state_delta"), dict):
            failures.append(f"{move_id}:state_delta_malformed")
        if not isinstance(move.get("emits"), list) or not move.get("emits"):
            failures.append(f"{move_id}:emits_missing")
        if move.get("may_halt") is not True:
            failures.append(f"{move_id}:may_halt_not_true")
        if not isinstance(move.get("halt_map"), dict) or not move.get("halt_map"):
            failures.append(f"{move_id}:halt_map_missing")
        if not isinstance(move.get("non_impersonation"), list) or not move.get("non_impersonation"):
            failures.append(f"{move_id}:non_impersonation_missing")

    if MOVE_REGISTRY["selection_policy"] != "lowest_priority_number":
        failures.append(f"selection_policy_wrong:{MOVE_REGISTRY['selection_policy']}")
    if "no unregistered move may fire" not in MOVE_REGISTRY["registry_law"]:
        failures.append("registry_law_missing_no_unregistered_move_may_fire")
    if "Day 4 admission is pre-authorization; Day 5 handles jurisdiction" not in MOVE_REGISTRY["registry_law"]:
        failures.append("registry_law_missing_day5_authority_boundary")

    receipt_move = MOVE_REGISTRY["moves"]["receipt.emit_terminal.v0"]
    if receipt_move["applies_when"] != {"any": [{"exists": "state.terminal_result"}, {"exists": "state.halt_code"}]}:
        failures.append("receipt_emit_terminal_applies_when_too_broad_or_wrong")

    unit_move = MOVE_REGISTRY["moves"]["unit.mark_complete.v0"]
    terminal = unit_move.get("state_delta", {}).get("on_pass", {}).get("state.terminal_result")
    if terminal != {"type": "STOP", "stop_code": "STOP_NEXT_MOVE_BOUNDARY"}:
        failures.append(f"unit_mark_complete_terminal_delta_wrong:{terminal}")

    proposal_move = MOVE_REGISTRY["moves"]["proposal.missing_move.draft.v0"]
    if proposal_move["move_kind"] != "PROPOSAL_ONLY":
        failures.append("proposal_missing_move_not_PROPOSAL_ONLY")
    if "does not register candidate move" not in proposal_move.get("non_impersonation", []):
        failures.append("proposal_move_missing_no_register_non_impersonation")

    return failures

def validate_inputs(
    halt_impl: Dict[str, Any],
    halt_policy: Dict[str, Any],
    halt_vocab: Dict[str, Any],
    halt_record_schema: Dict[str, Any],
    halt_next_handling: Dict[str, Any],
    proceed_receipt: Dict[str, Any],
    trace_ledger_receipt: Dict[str, Any],
    trace_schema: Dict[str, Any],
    proposal_ledger_schema: Dict[str, Any],
    local_regime_v1: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if halt_impl.get("receipt_id") != HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"halt_impl_receipt_id_wrong:{halt_impl.get('receipt_id')}")
    if halt_impl.get("gate") != "PASS":
        failures.append(f"halt_impl_gate_not_PASS:{halt_impl.get('gate')}")
    if halt_impl.get("target_unit_id") != "halt_vocabulary.v0":
        failures.append(f"halt_impl_target_wrong:{halt_impl.get('target_unit_id')}")
    if halt_impl.get("terminal", {}).get("type") != "STOP":
        failures.append(f"halt_impl_terminal_not_STOP:{halt_impl.get('terminal')}")
    if halt_impl.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append(f"halt_impl_terminal_stop_not_DONE:{halt_impl.get('terminal')}")
    if halt_impl.get("terminal", {}).get("next_command_goal") is not None:
        failures.append(f"halt_impl_terminal_next_not_null:{halt_impl.get('terminal')}")

    h_metrics = halt_impl.get("aggregate_metrics") or {}
    if h_metrics.get("canonical_halt_entry_count") != 21:
        failures.append(f"halt_entry_count_wrong:{h_metrics.get('canonical_halt_entry_count')}")
    if h_metrics.get("halt_route_count") != 21:
        failures.append(f"halt_route_count_wrong:{h_metrics.get('halt_route_count')}")
    for key in [
        "advance_terminal_as_halt_count",
        "halt_as_proof_claim_count",
        "halt_as_truth_claim_count",
        "hidden_continuation_count",
        "new_move_added_count",
        "taxonomy_delta_applied_count",
        "taxonomy_delta_promoted_count",
        "source_trace_modified_count",
        "source_receipt_modified_count",
        "source_ledger_modified_count",
        "source_runner_modified_count",
        "source_regime_modified_count",
    ]:
        if h_metrics.get(key) != 0:
            failures.append(f"halt_metric_not_zero:{key}:{h_metrics.get(key)}")

    if halt_policy.get("policy_id") != HALT_VOCABULARY_POLICY_ID:
        failures.append(f"halt_policy_id_wrong:{halt_policy.get('policy_id')}")

    entries = halt_vocab.get("entries", {})
    for required_halt in [
        "STOP_NO_APPLICABLE_MOVE",
        "STOP_NEEDS_NEW_MOVE",
        "STOP_AUTHORITY_VIOLATION",
        "STOP_GATE_FAIL",
        "STOP_NEXT_MOVE_BOUNDARY",
        "STOP_RECEIPT_MISMATCH",
    ]:
        if required_halt not in entries:
            failures.append(f"required_halt_missing:{required_halt}")
    if "NO_APPLICABLE_MOVE" in entries:
        failures.append("NO_APPLICABLE_MOVE_must_not_be_canonical")
    if "NO_APPLICABLE_MOVE" not in entries.get("STOP_NO_APPLICABLE_MOVE", {}).get("legacy_aliases", []):
        failures.append("NO_APPLICABLE_MOVE_alias_missing")
    if "proof closure" not in " ".join(entries.get("STOP_NO_APPLICABLE_MOVE", {}).get("must_not_impersonate", [])).lower():
        failures.append("STOP_NO_APPLICABLE_MOVE_missing_proof_closure_guard")

    for field in ["halt_record_id", "halt_code", "canonical_halt_code", "source_readout_ref", "source_trace_ref", "source_receipt_ref", "source_ledger_ref", "terminal_result"]:
        if field not in halt_record_schema.get("required_fields", []):
            failures.append(f"halt_record_schema_required_field_missing:{field}")

    routes = halt_next_handling.get("routes", {})
    for halt_code in ["STOP_NO_APPLICABLE_MOVE", "STOP_NEEDS_NEW_MOVE", "STOP_AUTHORITY_VIOLATION", "STOP_GATE_FAIL"]:
        if halt_code not in routes:
            failures.append(f"halt_next_handling_missing_route:{halt_code}")

    if proceed_receipt.get("receipt_id") != PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"proceed_receipt_id_wrong:{proceed_receipt.get('receipt_id')}")
    if proceed_receipt.get("gate") != "PASS":
        failures.append(f"proceed_gate_not_PASS:{proceed_receipt.get('gate')}")
    if proceed_receipt.get("target_adapter_unit_id") != "proceed_adapter.v0":
        failures.append(f"proceed_target_wrong:{proceed_receipt.get('target_adapter_unit_id')}")

    if trace_ledger_receipt.get("receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"trace_ledger_receipt_id_wrong:{trace_ledger_receipt.get('receipt_id')}")
    if trace_ledger_receipt.get("gate") != "PASS":
        failures.append(f"trace_ledger_gate_not_PASS:{trace_ledger_receipt.get('gate')}")
    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append(f"trace_schema_version_wrong:{trace_schema.get('schema_version')}")
    if proposal_ledger_schema.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append(f"proposal_ledger_schema_version_wrong:{proposal_ledger_schema.get('schema_version')}")
    if local_regime_v1.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append(f"local_regime_v1_hash_wrong:{local_regime_v1.get('local_regime_hash')}")

    for path, label in [
        (HALT_IMPLEMENTATION_RECEIPT_PATH, "halt_implementation_receipt"),
        (HALT_POLICY_PATH, "halt_policy"),
        (HALT_VOCABULARY_PATH, "halt_vocabulary"),
        (HALT_RECORD_SCHEMA_PATH, "halt_record_schema"),
        (HALT_NEXT_HANDLING_PATH, "halt_to_next_handling"),
        (PROCEED_RECEIPT_PATH, "proceed_receipt"),
        (PROCEED_ADAPTER_MODULE_PATH, "proceed_adapter_module"),
        (TRACE_LEDGER_RECEIPT_PATH, "trace_ledger_receipt"),
        (TRACE_SCHEMA_PATH, "trace_schema"),
        (PROPOSAL_LEDGER_SCHEMA_PATH, "proposal_ledger_schema"),
        (TRACE_LEDGER_RUNNER_PATH, "trace_ledger_runner"),
        (LOCAL_REGIME_V1_PATH, "local_regime_v1"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{path.relative_to(ROOT).as_posix()}")

    return failures

def validate_policy(policy: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy.get('policy_status')}")
    if policy.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"target_unit_wrong:{policy.get('target_unit_id')}")
    if policy.get("policy_id") != receipt.get("policy_id"):
        failures.append("policy_receipt_id_mismatch")

    move_schema = policy.get("move_schema") or {}
    for field in REQUIRED_MOVE_FIELDS:
        if field not in move_schema.get("required_fields", []):
            failures.append(f"policy_move_schema_missing:{field}")

    predicate_schema = policy.get("applies_when_predicate_schema") or {}
    if predicate_schema.get("no_free_form_code") is not True:
        failures.append("predicate_schema_allows_free_form_code")
    for op in ["eq", "neq", "exists", "missing", "in", "not", "all", "any"]:
        if op not in predicate_schema.get("allowed_operators", []):
            failures.append(f"predicate_operator_missing:{op}")

    registry = policy.get("move_registry") or {}
    if len(registry.get("moves", {})) != 7:
        failures.append(f"starter_move_count_wrong:{len(registry.get('moves', {}))}")
    if registry.get("selection_policy") != "lowest_priority_number":
        failures.append(f"selection_policy_wrong:{registry.get('selection_policy')}")

    admission = policy.get("move_admission_gate") or {}
    if admission.get("admission_status_name") != "ADMISSIBLE_PRE_AUTH":
        failures.append(f"admission_status_wrong:{admission.get('admission_status_name')}")
    if admission.get("authorization_status") != "DEFERRED_TO_DAY5":
        failures.append(f"authorization_status_wrong:{admission.get('authorization_status')}")
    if "jurisdiction authority" not in admission.get("day4_must_not_decide", []):
        failures.append("day4_must_not_decide_jurisdiction_missing")

    blocked = policy.get("blocked_move_record_schema") or {}
    if "AUTHORITY_DEFERRED" not in blocked.get("block_reasons", []):
        failures.append("AUTHORITY_DEFERRED_block_reason_missing")
    if blocked.get("authority_deferred_law", {}).get("does_not_mean_STOP_AUTHORITY_VIOLATION") is not True:
        failures.append("authority_deferred_law_missing")

    proposal = policy.get("missing_move_proposal_stub") or {}
    if proposal.get("status") != "PROPOSED_ONLY":
        failures.append(f"missing_move_proposal_status_wrong:{proposal.get('status')}")
    for key in ["may_not_write_move_registry", "may_not_register_candidate_move", "may_not_execute_candidate_move", "may_not_mark_candidate_accepted", "may_not_promote_taxonomy_delta"]:
        if proposal.get("hard_rules", {}).get(key) is not True:
            failures.append(f"missing_move_proposal_hard_rule_missing:{key}")

    for patch_key, expected_mode in [
        ("trace_move_context_patch", "future_schema_patch_only_do_not_mutate_existing_traces"),
        ("receipt_move_registry_patch", "future_schema_patch_only_do_not_mutate_existing_receipts"),
        ("proceed_readout_move_context_patch", "future_schema_patch_only_do_not_mutate_existing_readouts"),
    ]:
        if policy.get(patch_key, {}).get("patch_mode") != expected_mode:
            failures.append(f"{patch_key}_mode_wrong:{policy.get(patch_key, {}).get('patch_mode')}")

    demo_pos = policy.get("day4_demo_positive_run_plan") or {}
    if demo_pos.get("expected_terminal_result", {}).get("stop_code") != "STOP_NEXT_MOVE_BOUNDARY":
        failures.append(f"positive_demo_terminal_wrong:{demo_pos.get('expected_terminal_result')}")
    if demo_pos.get("expected_move_sequence") != [
        "state.validate_shape.v0",
        "regime.validate_shape.v0",
        "moves.compute_applicable.v0",
        "selector.choose_move.v0",
        "unit.mark_complete.v0",
        "receipt.emit_terminal.v0",
    ]:
        failures.append("positive_demo_sequence_wrong")

    demo_missing = policy.get("day4_demo_missing_move_run_plan") or {}
    if demo_missing.get("expected_terminal_result", {}).get("stop_code") != "STOP_NEEDS_NEW_MOVE":
        failures.append(f"missing_move_demo_terminal_wrong:{demo_missing.get('expected_terminal_result')}")
    if demo_missing.get("expected_missing_move_proposal", {}).get("status") != "PROPOSED_ONLY":
        failures.append(f"missing_move_demo_proposal_status_wrong:{demo_missing.get('expected_missing_move_proposal')}")

    gates = policy.get("acceptance_gates") or {}
    for gate in ACCEPTANCE_GATES:
        if gates.get(gate, {}).get("required") is not True:
            failures.append(f"acceptance_gate_missing:{gate}")

    guards = policy.get("authority_guards") or {}
    for key in [
        "move_registry_policy_built",
        "source_halt_vocabulary_consumed",
        "source_proceed_adapter_consumed",
        "source_trace_ledger_surface_consumed",
    ]:
        if guards.get(key) is not True:
            failures.append(f"authority_guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "implementation_performed_by_policy",
        "demo_runs_emitted_by_policy",
        "source_halt_vocabulary_modified",
        "source_proceed_adapter_modified",
        "source_trace_ledger_runner_modified",
        "source_local_regime_v1_modified",
        "taxonomy_delta_applied",
        "taxonomy_delta_promoted",
        "new_move_added",
        "unregistered_move_fired",
        "missing_move_proposal_registered",
        "missing_move_proposal_executed",
        "day5_authority_implemented",
        "jurisdiction_resolved",
        "proposal_executed",
        "proposal_promoted",
        "registry_written",
        "registry_sqlite_read",
        "registry_sqlite_written",
        "global_taxonomy_claimed",
        "final_schema_claimed",
        "proof_claimed",
        "halt_as_proof_claimed",
        "hidden_continuation_authorized",
    ]:
        if guards.get(key) is not False:
            failures.append(f"authority_guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != NEXT_GOAL:
        failures.append(f"terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"terminal_stop_not_null:{terminal.get('stop_code')}")

    return failures

def build_policy(write_outputs: bool = True) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    halt_impl = read_json(HALT_IMPLEMENTATION_RECEIPT_PATH)
    halt_policy = read_json(HALT_POLICY_PATH)
    halt_vocab = read_json(HALT_VOCABULARY_PATH)
    halt_record_schema = read_json(HALT_RECORD_SCHEMA_PATH)
    halt_next_handling = read_json(HALT_NEXT_HANDLING_PATH)
    proceed_receipt = read_json(PROCEED_RECEIPT_PATH)
    trace_ledger_receipt = read_json(TRACE_LEDGER_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    proposal_ledger_schema = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    local_regime_v1 = read_json(LOCAL_REGIME_V1_PATH)

    failures: List[str] = []
    failures.extend(validate_inputs(
        halt_impl,
        halt_policy,
        halt_vocab,
        halt_record_schema,
        halt_next_handling,
        proceed_receipt,
        trace_ledger_receipt,
        trace_schema,
        proposal_ledger_schema,
        local_regime_v1,
    ))
    failures.extend(validate_move_schema_and_registry())

    policy_seed = {
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_halt_impl": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "move_registry_sig8": sha8(MOVE_REGISTRY),
        "next_goal": NEXT_GOAL,
    }
    policy_id = sha8(policy_seed)

    authority_guards = {
        "move_registry_policy_built": True,
        "source_halt_vocabulary_consumed": True,
        "source_proceed_adapter_consumed": True,
        "source_trace_ledger_surface_consumed": True,
        "implementation_performed_by_policy": False,
        "demo_runs_emitted_by_policy": False,
        "source_halt_vocabulary_modified": False,
        "source_proceed_adapter_modified": False,
        "source_trace_ledger_runner_modified": False,
        "source_local_regime_v1_modified": False,
        "source_trace_modified": False,
        "source_receipt_modified": False,
        "source_ledger_modified": False,
        "taxonomy_delta_applied": False,
        "taxonomy_delta_promoted": False,
        "new_move_added": False,
        "unregistered_move_fired": False,
        "missing_move_proposal_registered": False,
        "missing_move_proposal_executed": False,
        "day5_authority_implemented": False,
        "jurisdiction_resolved": False,
        "proposal_executed": False,
        "proposal_promoted": False,
        "registry_written": False,
        "registry_sqlite_read": False,
        "registry_sqlite_written": False,
        "global_taxonomy_claimed": False,
        "final_schema_claimed": False,
        "proof_claimed": False,
        "halt_as_proof_claimed": False,
        "hidden_continuation_authorized": False,
    }

    policy = {
        "schema_version": "move_registry_v0_policy_v0",
        "policy_type": "MOVE_REGISTRY_V0_POLICY",
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "target_unit_id": TARGET_UNIT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_policy_id": HALT_VOCABULARY_POLICY_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": {
            "purpose": "Create a finite typed registry of moves the runner may inspect, block, select, or propose against.",
            "core_law": "No unregistered move may fire.",
            "day4_scope": "move exists, schema-valid, applies, admissible_pre_auth, selected",
            "day5_boundary": "authorization_status is DEFERRED_TO_DAY5; Day 4 does not resolve jurisdiction",
            "non_goal": "no final move catalog, no automatic move invention, no full jurisdiction, no taxonomy evolution, no proposal auto-acceptance",
        },
        "move_schema": MOVE_SCHEMA,
        "move_kind_enum": MOVE_KIND_ENUM,
        "applies_when_predicate_schema": APPLIES_WHEN_PREDICATE_SCHEMA,
        "move_lifecycle": MOVE_LIFECYCLE,
        "move_registry": MOVE_REGISTRY,
        "move_registry_sig8": sha8(MOVE_REGISTRY),
        "move_admission_gate": MOVE_ADMISSION_GATE,
        "blocked_move_record_schema": BLOCKED_MOVE_RECORD_SCHEMA,
        "applicable_move_inspection_schema": APPLICABLE_MOVE_INSPECTION_SCHEMA,
        "selected_move_record_schema": SELECTED_MOVE_RECORD_SCHEMA,
        "missing_move_proposal_stub": MISSING_MOVE_PROPOSAL_STUB,
        "trace_move_context_patch": TRACE_MOVE_CONTEXT_PATCH,
        "receipt_move_registry_patch": RECEIPT_MOVE_REGISTRY_PATCH,
        "proceed_readout_move_context_patch": PROCEED_READOUT_MOVE_CONTEXT_PATCH,
        "day4_demo_positive_run_plan": DAY4_DEMO_POSITIVE_RUN_PLAN,
        "day4_demo_missing_move_run_plan": DAY4_DEMO_MISSING_MOVE_RUN_PLAN,
        "required_implementation_artifacts": REQUIRED_IMPLEMENTATION_ARTIFACTS,
        "acceptance_gates": ACCEPTANCE_GATES,
        "authorized_operations_next": {
            "read_move_registry_policy": True,
            "read_move_registry_policy_receipt": True,
            "write_move_schema_artifact": True,
            "write_move_kind_enum_artifact": True,
            "write_applies_when_predicate_schema_artifact": True,
            "write_move_lifecycle_artifact": True,
            "write_move_registry_artifact": True,
            "write_move_admission_gate_artifact": True,
            "write_blocked_move_record_schema_artifact": True,
            "write_applicable_move_inspection_schema_artifact": True,
            "write_selected_move_record_schema_artifact": True,
            "write_missing_move_proposal_stub_artifact": True,
            "write_trace_move_context_patch_artifact": True,
            "write_receipt_move_registry_patch_artifact": True,
            "write_proceed_readout_move_context_patch_artifact": True,
            "emit_day4_demo_positive_run": True,
            "emit_day4_demo_missing_move_run": True,
            "emit_day4_demo_move_run_receipt": True,
            "emit_implementation_receipt": True,
        },
        "forbidden_operations_next": {
            "mutate_existing_halt_vocabulary": True,
            "mutate_existing_proceed_adapter": True,
            "mutate_existing_trace_files": True,
            "mutate_existing_receipt_files": True,
            "mutate_existing_readout_files": True,
            "modify_trace_ledger_runner_module": True,
            "modify_proceed_adapter_module": True,
            "modify_local_regime_v1": True,
            "fire_unregistered_move": True,
            "fire_schema_invalid_move": True,
            "select_move_ambiguously": True,
            "silently_drop_blocked_move": True,
            "register_missing_move_from_proposal": True,
            "execute_missing_move_candidate": True,
            "accept_missing_move_proposal": True,
            "promote_taxonomy_delta": True,
            "accept_taxonomy_delta": True,
            "implement_day5_authority": True,
            "resolve_jurisdiction": True,
            "sqlite_registry_write": True,
            "sqlite_registry_read": True,
            "global_move_catalog_claim": True,
            "final_schema_claim": True,
            "proof_claim": True,
            "hidden_continuation_after_terminal": True,
            "latest_or_mtime_selection": True,
            "ambient_workspace_authority": True,
        },
        "safety_clauses": {
            "policy_only": True,
            "does_not_emit_demo_runs": True,
            "does_not_mutate_existing_artifacts": True,
            "does_not_modify_source_modules": True,
            "does_not_modify_source_regime": True,
            "does_not_register_new_moves": True,
            "does_not_accept_or_execute_missing_move_proposal": True,
            "does_not_accept_or_promote_taxonomy_delta": True,
            "does_not_implement_day5_authority": True,
            "does_not_write_registry": True,
            "does_not_claim_final_move_catalog": True,
            "does_not_claim_proof": True,
            "next_unit_required_for_implementation": True,
        },
        "authority_guards": authority_guards,
        "terminal": {
            "type": "ADVANCE",
            "next_command_goal": NEXT_GOAL,
            "stop_code": None,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "policy_id": policy_id,
        "target_unit_id": TARGET_UNIT_ID,
        "source_halt_impl": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "terminal": policy["terminal"],
    }
    receipt_id = sha8(receipt_seed)
    policy["policy_receipt_id"] = receipt_id

    receipt = {
        "schema_version": "move_registry_v0_policy_receipt_v0",
        "receipt_type": "MOVE_REGISTRY_V0_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "target_unit_id": TARGET_UNIT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_policy_id": HALT_VOCABULARY_POLICY_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": policy["policy_summary"],
        "move_schema": MOVE_SCHEMA,
        "move_kind_enum": MOVE_KIND_ENUM,
        "applies_when_predicate_schema": APPLIES_WHEN_PREDICATE_SCHEMA,
        "move_lifecycle": MOVE_LIFECYCLE,
        "move_registry": MOVE_REGISTRY,
        "move_registry_sig8": sha8(MOVE_REGISTRY),
        "move_admission_gate": MOVE_ADMISSION_GATE,
        "blocked_move_record_schema": BLOCKED_MOVE_RECORD_SCHEMA,
        "applicable_move_inspection_schema": APPLICABLE_MOVE_INSPECTION_SCHEMA,
        "selected_move_record_schema": SELECTED_MOVE_RECORD_SCHEMA,
        "missing_move_proposal_stub": MISSING_MOVE_PROPOSAL_STUB,
        "trace_move_context_patch": TRACE_MOVE_CONTEXT_PATCH,
        "receipt_move_registry_patch": RECEIPT_MOVE_REGISTRY_PATCH,
        "proceed_readout_move_context_patch": PROCEED_READOUT_MOVE_CONTEXT_PATCH,
        "day4_demo_positive_run_plan": DAY4_DEMO_POSITIVE_RUN_PLAN,
        "day4_demo_missing_move_run_plan": DAY4_DEMO_MISSING_MOVE_RUN_PLAN,
        "required_implementation_artifacts": REQUIRED_IMPLEMENTATION_ARTIFACTS,
        "acceptance_gates": ACCEPTANCE_GATES,
        "authorized_operations_next": policy["authorized_operations_next"],
        "forbidden_operations_next": policy["forbidden_operations_next"],
        "safety_clauses": policy["safety_clauses"],
        "authority_guards": authority_guards,
        "terminal": policy["terminal"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    failures.extend(validate_policy(policy, receipt))
    policy["failures"] = failures
    receipt["failures"] = failures
    policy["gate"] = "PASS" if not failures else "FAIL"
    receipt["gate"] = policy["gate"]

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        write_json(OUT_DIR / f"{policy_id}.json", policy)
        write_json(OUT_RECEIPT_DIR / f"{policy_id}.json", receipt)

    return policy, receipt

def main() -> int:
    policy, receipt = build_policy(write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"move_registry_policy_id={policy['policy_id']}")
    print(f"move_registry_policy_receipt_id={receipt['receipt_id']}")
    print(f"move_registry_policy_path=data/move_registry_v0_policies/{policy['policy_id']}.json")
    print(f"move_registry_policy_receipt_path=data/move_registry_v0_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
