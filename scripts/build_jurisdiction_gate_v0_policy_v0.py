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

UNIT_ID = "BUILD_JURISDICTION_GATE_V0_POLICY_V0"
NEXT_GOAL = "IMPLEMENT_JURISDICTION_GATE_V0_WITH_DEMO_VERDICTS_V0"
TARGET_UNIT_ID = "jurisdiction_gate.v0"

MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID = "bef08570"
MOVE_REGISTRY_POLICY_ID = "34863965"
MOVE_REGISTRY_POLICY_RECEIPT_ID = "1264c091"
HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID = "75eabbe2"
HALT_VOCABULARY_POLICY_ID = "0707a2d7"
PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID = "363d2f4a"
TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID = "cc24a11f"
TRACE_SCHEMA_ID = "b4887660"
PROPOSAL_LEDGER_SCHEMA_ID = "eee2a318"
LOCAL_REGIME_V1_HASH = "25802530"

MOVE_IMPL_RECEIPT_PATH = ROOT / "data" / "move_registry_v0_implementation_receipts" / f"{MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID}.json"
MOVE_POLICY_PATH = ROOT / "data" / "move_registry_v0_policies" / f"{MOVE_REGISTRY_POLICY_ID}.json"
MOVE_POLICY_RECEIPT_PATH = ROOT / "data" / "move_registry_v0_policy_receipts" / f"{MOVE_REGISTRY_POLICY_ID}.json"
MOVE_REGISTRY_PATH = ROOT / "data" / "move_registry_v0" / "move_registry_v0.json"
MOVE_ADMISSION_GATE_PATH = ROOT / "data" / "move_registry_v0" / "move_admission_gate_v0.json"
MOVE_INSPECTION_SCHEMA_PATH = ROOT / "data" / "move_registry_v0" / "applicable_move_inspection_schema_v0.json"
BLOCKED_MOVE_SCHEMA_PATH = ROOT / "data" / "move_registry_v0" / "blocked_move_record_schema_v0.json"
SELECTED_MOVE_SCHEMA_PATH = ROOT / "data" / "move_registry_v0" / "selected_move_record_schema_v0.json"
MISSING_MOVE_STUB_PATH = ROOT / "data" / "move_registry_v0" / "missing_move_proposal_stub_v0.json"
DAY4_POSITIVE_RUN_PATH = ROOT / "data" / "move_registry_v0_demo" / "day4_demo_positive_run.json"
DAY4_MISSING_MOVE_RUN_PATH = ROOT / "data" / "move_registry_v0_demo" / "day4_demo_missing_move_run.json"

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

OUT_DIR = ROOT / "data" / "jurisdiction_gate_v0_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "jurisdiction_gate_v0_policy_receipts"

VERDICTS = [
    "AUTHORIZED_LOCAL",
    "REQUIRES_PROPOSAL",
    "REQUIRES_EXTRACTION",
    "REQUIRES_HUMAN_REVIEW",
    "FORBIDDEN",
]

AUTHORITY_HALT_PATCH_ENTRIES = {
    "STOP_AUTHORITY_BOUNDARY": {
        "halt_code": "STOP_AUTHORITY_BOUNDARY",
        "canonical_halt_code": "STOP_AUTHORITY_BOUNDARY",
        "halt_family": "AUTHORITY",
        "smallest_honest_meaning": "A move is admissible, but the current jurisdiction profile does not authorize execution inside this unit.",
        "must_not_impersonate": [
            "move invalidity",
            "proof failure",
            "runner error",
            "human rejection",
        ],
        "allowed_next_handling": [
            "emit authority verdict",
            "emit proposal if allowed",
            "request human review if required",
            "narrow the move or jurisdiction profile explicitly",
        ],
    },
    "STOP_PROPOSAL_REQUIRED": {
        "halt_code": "STOP_PROPOSAL_REQUIRED",
        "canonical_halt_code": "STOP_PROPOSAL_REQUIRED",
        "halt_family": "AUTHORITY",
        "smallest_honest_meaning": "The next move may be proposed but may not execute under the current jurisdiction.",
        "must_not_impersonate": [
            "accepted move",
            "authorized execution",
            "taxonomy upgrade",
            "registry mutation",
        ],
        "allowed_next_handling": [
            "emit proposal packet",
            "await review",
            "defer",
            "narrow proposal",
        ],
    },
    "STOP_HUMAN_REVIEW_REQUIRED": {
        "halt_code": "STOP_HUMAN_REVIEW_REQUIRED",
        "canonical_halt_code": "STOP_HUMAN_REVIEW_REQUIRED",
        "halt_family": "AUTHORITY",
        "smallest_honest_meaning": "The move is understandable but requires human approval before execution.",
        "must_not_impersonate": [
            "failure",
            "forbidden move",
            "completed decision",
            "self-authorization",
        ],
        "allowed_next_handling": [
            "emit human review request",
            "list approve/reject/defer/narrow/request-extraction options",
            "do not execute until approved",
        ],
    },
    "STOP_FORBIDDEN_MOVE": {
        "halt_code": "STOP_FORBIDDEN_MOVE",
        "canonical_halt_code": "STOP_FORBIDDEN_MOVE",
        "halt_family": "AUTHORITY",
        "smallest_honest_meaning": "The move is outside the current regime or violates a forbidden action/input rule.",
        "must_not_impersonate": [
            "temporary lack of confidence",
            "ordinary missing move",
            "human review request",
        ],
        "allowed_next_handling": [
            "record forbidden verdict",
            "do not execute",
            "do not propose as currently shaped",
            "reformulate only through a separate lawful unit",
        ],
    },
}

JURISDICTION_PROFILE_SCHEMA = {
    "schema_version": "jurisdiction_profile_schema_v0",
    "required_fields": [
        "jurisdiction_profile_id",
        "schema_version",
        "scope",
        "authorized_local",
        "proposal_allowed",
        "requires_extraction",
        "requires_human_review",
        "forbidden",
    ],
    "profile_is_local": True,
    "relative_to": [
        "current_state",
        "current_unit",
        "current_layer",
        "current_mode",
        "current_active_object",
        "current_source_surface",
    ],
    "must_not_impersonate": [
        "global governance",
        "final autonomy profile",
        "human approval",
        "future authorization",
    ],
    "example_profile": {
        "jurisdiction_profile_id": "jurisdiction_profile_v0",
        "schema_version": "jurisdiction_profile_schema_v0",
        "scope": {
            "layer": "OUTER",
            "mode": "BUILD",
            "active_object": "runner_surface_v0",
            "unit_id": "proceed.unit.execute_declared_runner_unit.v0",
        },
        "authorized_local": {
            "move_kinds": [
                "CONTROL_CHECK",
                "CONTROL_INSPECT",
                "CONTROL_SELECT",
                "CONTROL_EMIT",
                "LOCAL_REPAIR",
            ],
            "layers": ["OUTER", "MOVE_SPACE", "RECEIPT_TRACE"],
            "max_effect": [
                "state_status_update",
                "trace_append",
                "receipt_emit",
                "readout_emit",
                "local_projection_repair",
            ],
            "explicitly_authorized_demo_moves": [
                "state.validate_shape.v0",
                "regime.validate_shape.v0",
                "moves.compute_applicable.v0",
                "selector.choose_move.v0",
                "receipt.emit_terminal.v0",
            ],
            "pre_authorized_domain_transforms": [
                "unit.mark_complete.v0",
            ],
        },
        "proposal_allowed": {
            "move_kinds": ["PROPOSAL_ONLY", "DOMAIN_TRANSFORM"],
            "conditions": [
                "triggered_by_typed_halt",
                "candidate_move_not_registered",
                "proposal_does_not_mutate_registry",
            ],
        },
        "requires_extraction": {
            "conditions": [
                "depends_on_unclassified_code_behavior",
                "depends_on_proto_history",
                "depends_on_non_imported_implementation_detail",
            ],
        },
        "requires_human_review": {
            "conditions": [
                "changes_registry",
                "accepts_taxonomy_delta",
                "widens_jurisdiction",
                "executes_domain_transform_not_pre_authorized",
                "promotes_frontier_to_active_build",
            ],
        },
        "forbidden": {
            "inputs": [
                "chat_memory_authority",
                "latest_file_guessing",
                "mtime_selection",
                "ambient_workspace_inference",
                "ui_state_authority",
                "unregistered_move_execution",
            ],
            "actions": [
                "self_authorize_taxonomy_delta",
                "self_modify_jurisdiction_profile",
                "execute_unregistered_move",
                "promote_frontier_claim",
                "collapse_theorem_and_witness_layers",
            ],
        },
    },
}

JURISDICTION_VERDICT_ENUM = {
    "schema_version": "jurisdiction_verdict_enum_v0",
    "verdicts": VERDICTS,
    "meanings": {
        "AUTHORIZED_LOCAL": "runner may execute the move inside the current local jurisdiction profile",
        "REQUIRES_PROPOSAL": "runner may describe the move and emit a proposal packet, but may not execute it",
        "REQUIRES_EXTRACTION": "move depends on material that must be lawfully extracted first",
        "REQUIRES_HUMAN_REVIEW": "move is understandable but requires human approval before execution",
        "FORBIDDEN": "move is outside current regime or violates forbidden input/action rule",
    },
    "verdict_to_halt": {
        "AUTHORIZED_LOCAL": None,
        "REQUIRES_PROPOSAL": "STOP_PROPOSAL_REQUIRED",
        "REQUIRES_EXTRACTION": "STOP_NEEDS_EXTRACTION",
        "REQUIRES_HUMAN_REVIEW": "STOP_HUMAN_REVIEW_REQUIRED",
        "FORBIDDEN": "STOP_FORBIDDEN_MOVE",
    },
}

MOVE_AUTHORITY_PATCH = {
    "schema_version": "move_authority_patch_v0",
    "patch_mode": "future_move_schema_patch_only_do_not_mutate_existing_move_registry",
    "add_field": {
        "authority": {
            "required_verdict": "AUTHORIZED_LOCAL|REQUIRES_PROPOSAL|REQUIRES_HUMAN_REVIEW",
            "authority_tags": ["<tag>"],
            "may_emit_proposal_if_denied": False,
            "requires_human_review_if": [],
            "forbidden_if": [
                "requires_unregistered_input",
                "would_modify_registry_without_review",
            ],
        }
    },
    "examples": {
        "authorized_local": {
            "required_verdict": "AUTHORIZED_LOCAL",
            "authority_tags": ["state_update", "trace_append"],
            "may_emit_proposal_if_denied": False,
            "requires_human_review_if": [],
            "forbidden_if": [
                "requires_unregistered_input",
                "would_modify_registry",
            ],
        },
        "proposal_only": {
            "required_verdict": "REQUIRES_PROPOSAL",
            "authority_tags": ["proposal_emit_only"],
            "may_emit_proposal_if_denied": True,
            "execution_forbidden": True,
            "must_not_mutate": [
                "move_registry",
                "taxonomy_registry",
                "jurisdiction_profile",
            ],
        },
        "registry_changing": {
            "required_verdict": "REQUIRES_HUMAN_REVIEW",
            "authority_tags": ["registry_mutation"],
            "may_emit_proposal_if_denied": True,
            "execution_forbidden_without_review": True,
        },
    },
}

JURISDICTION_GATE = {
    "schema_version": "jurisdiction_gate_v0",
    "purpose": "Separate admissible_pre_auth moves from authorized executable moves.",
    "core_law": "A move may be locally admissible and still not authorized.",
    "execution_rule": "Only AUTHORIZED_LOCAL moves may execute.",
    "selector_rule": "Selector may only choose from authorized_executable_moves.",
    "verdict_order": [
        "FORBIDDEN",
        "REQUIRES_EXTRACTION",
        "REQUIRES_HUMAN_REVIEW",
        "REQUIRES_PROPOSAL",
        "AUTHORIZED_LOCAL",
        "STOP_AUTHORITY_BOUNDARY_FALLBACK",
    ],
    "pseudocode": [
        "If move uses forbidden input: FORBIDDEN",
        "If move action is forbidden: FORBIDDEN",
        "If move depends on unextracted code/proto/history behavior: REQUIRES_EXTRACTION",
        "If move mutates registry, taxonomy, jurisdiction, or authority profile: REQUIRES_HUMAN_REVIEW",
        "If move is proposal-only: REQUIRES_PROPOSAL",
        "If move kind/layer/effects are inside authorized_local: AUTHORIZED_LOCAL",
        "Else: STOP_AUTHORITY_BOUNDARY fallback",
    ],
    "anti_laundering_law": [
        "FORBIDDEN is checked before proposal.",
        "REQUIRES_HUMAN_REVIEW is checked before proposal when registry/taxonomy/jurisdiction mutation is involved.",
        "A registry mutation cannot be laundered through proposal-only wording.",
        "A forbidden move cannot be softened into human review unless reformulated through a separate lawful unit.",
    ],
}

AUTHORITY_VERDICT_RECORD_SCHEMA = {
    "schema_version": "authority_verdict_record_schema_v0",
    "required_fields": [
        "authority_verdict_id",
        "schema_version",
        "run_id",
        "unit_id",
        "state_sig8",
        "move_id",
        "move_admissibility_status",
        "jurisdiction_profile_id",
        "authority_verdict",
        "reason",
        "allowed_effects",
        "forbidden_effects_checked",
        "terminal_if_not_authorized",
        "proposal_ref",
        "review_request_ref",
        "extraction_request_ref",
        "must_not_impersonate",
    ],
    "audit_law": [
        "Every admissible_pre_auth move receives an authority verdict.",
        "A blocked authority verdict is not move inadmissibility.",
        "A human-review verdict is not rejection.",
        "A forbidden verdict is not proposal permission.",
    ],
}

AUTHORITY_BLOCKED_MOVE_RECORD_SCHEMA = {
    "schema_version": "authority_blocked_move_record_schema_v0",
    "required_fields": [
        "blocked_move_id",
        "move_id",
        "block_reason",
        "admissibility_status",
        "authority_verdict",
        "halt_pressure",
        "authority_verdict_ref",
        "proposal_ref",
        "review_request_ref",
        "must_not_impersonate",
    ],
    "authority_block_reasons": [
        "AUTHORITY_BOUNDARY",
        "PROPOSAL_ONLY",
        "HUMAN_REVIEW_REQUIRED",
        "EXTRACTION_REQUIRED",
        "FORBIDDEN_BY_PROFILE",
    ],
}

PROPOSAL_PACKET_SCHEMA = {
    "schema_version": "proposal_packet_schema_v0",
    "required_fields": [
        "proposal_id",
        "schema_version",
        "proposal_type",
        "trigger",
        "proposed_action",
        "why_move_is_admissible",
        "why_not_authorized",
        "requested_decision",
        "if_approved",
        "if_rejected",
        "must_not_impersonate",
        "status",
    ],
    "status": "PROPOSED_ONLY",
    "core_law": [
        "A proposal is not execution.",
        "A proposal is not acceptance.",
        "A proposal is not authority.",
        "A proposal may not mutate registry, taxonomy, or jurisdiction profile.",
    ],
}

HUMAN_REVIEW_REQUEST_SCHEMA = {
    "schema_version": "human_review_request_schema_v0",
    "required_fields": [
        "review_request_id",
        "schema_version",
        "trigger_halt",
        "move_id",
        "authority_verdict",
        "question",
        "decision_options",
        "default_without_response",
        "must_not_impersonate",
    ],
    "decision_options": [
        {
            "option": "APPROVE",
            "meaning": "Authorize this exact move once under the declared unit.",
        },
        {
            "option": "REJECT",
            "meaning": "Do not authorize this move.",
        },
        {
            "option": "DEFER",
            "meaning": "Keep proposal open but do not execute.",
        },
        {
            "option": "NARROW",
            "meaning": "Request a smaller proposal.",
        },
        {
            "option": "REQUEST_EXTRACTION",
            "meaning": "Require extraction before review.",
        },
    ],
    "default_without_response": "NO_EXECUTION",
    "core_law": "No response means no execution.",
}

HALT_VOCABULARY_AUTHORITY_PATCH = {
    "schema_version": "halt_vocabulary_authority_patch_v0",
    "patch_mode": "future_halt_vocabulary_patch_only_do_not_mutate_existing_halt_vocabulary",
    "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
    "patch_reason": "Day 5 jurisdiction pressure requires distinguishing ordinary authority boundaries from authority violations.",
    "adds_canonical_entries": AUTHORITY_HALT_PATCH_ENTRIES,
    "reuses_existing_entries": {
        "STOP_NEEDS_EXTRACTION": "used for REQUIRES_EXTRACTION verdict",
        "STOP_AUTHORITY_VIOLATION": "reserved for actual authority violation, not ordinary jurisdiction boundary",
    },
    "non_goal": "This is a patch declaration, not taxonomy evolution runtime and not in-place mutation.",
}

MOVE_INSPECTION_AUTHORITY_PATCH = {
    "schema_version": "move_inspection_authority_patch_v0",
    "patch_mode": "future_schema_patch_only_do_not_mutate_existing_day4_inspections",
    "add_fields": {
        "authority_checked_moves": [
            {
                "move_id": "<move_id>",
                "authority_verdict": "<verdict>",
                "authority_verdict_ref": "<authority_verdict_id>",
            }
        ],
        "authorized_executable_moves": ["<move_id>"],
        "proposal_only_moves": ["<move_id>"],
        "extraction_required_moves": ["<move_id>"],
        "human_review_required_moves": ["<move_id>"],
        "forbidden_moves": ["<move_id>"],
        "selector_input": "authorized_executable_moves_only",
    },
}

TRACE_AUTHORITY_PATCH = {
    "schema_version": "trace_authority_patch_v0",
    "patch_mode": "future_schema_patch_only_do_not_mutate_existing_traces",
    "add_fields": {
        "jurisdiction_profile_id": "jurisdiction_profile_v0",
        "authority_verdict": "<verdict>",
        "authority_verdict_ref": "<authority_verdict_id>",
        "authorized_executable_moves": ["<move_id>"],
        "proposal_packet_ref": "<proposal_id|null>",
        "human_review_request_ref": "<review_request_id|null>",
        "selector_input": "authorized_executable_moves_only",
    },
}

RECEIPT_AUTHORITY_PATCH = {
    "schema_version": "receipt_authority_patch_v0",
    "patch_mode": "future_schema_patch_only_do_not_mutate_existing_receipts",
    "add_fields": {
        "jurisdiction": {
            "jurisdiction_profile_id": "jurisdiction_profile_v0",
            "verdict_counts": {
                "AUTHORIZED_LOCAL": "<int>",
                "REQUIRES_PROPOSAL": "<int>",
                "REQUIRES_EXTRACTION": "<int>",
                "REQUIRES_HUMAN_REVIEW": "<int>",
                "FORBIDDEN": "<int>",
            },
        },
        "authority": {
            "authorized_executable_moves": ["<move_id>"],
            "proposal_packets_emitted": "<int>",
            "human_review_requests_emitted": "<int>",
            "forbidden_moves_count": "<int>",
        },
    },
}

PROCEED_READOUT_AUTHORITY_PATCH = {
    "schema_version": "proceed_readout_authority_patch_v0",
    "patch_mode": "future_schema_patch_only_do_not_mutate_existing_readouts",
    "add_fields": {
        "jurisdiction_profile_ref": "<jurisdiction_profile_id>",
        "authority_verdict_refs": ["<authority_verdict_id>"],
        "authorized_executable_moves": ["<move_id>"],
        "authority_terminal": "ADVANCE|STOP",
        "proposal_packet_ref": "<proposal_id|null>",
        "human_review_request_ref": "<review_request_id|null>",
    },
}

DEMO_AUTHORIZED_MOVE_PLAN = {
    "schema_version": "day5_demo_authorized_move_plan_v0",
    "demo_name": "DAY5_AUTHORIZED_LOCAL_MOVE",
    "state": {
        "status": "VALID",
        "active_object": {
            "object_kind": "BUILD_UNIT",
            "completion_status": "PENDING",
        },
    },
    "admissible_move": "unit.mark_complete.v0",
    "expected_authority_verdict": "AUTHORIZED_LOCAL",
    "expected_terminal": {
        "type": "ADVANCE",
        "next_unit_id": "receipt.emit_terminal.v0",
    },
}

DEMO_PROPOSAL_REQUIRED_PLAN = {
    "schema_version": "day5_demo_proposal_required_plan_v0",
    "demo_name": "DAY5_PROPOSAL_REQUIRED",
    "admissible_move": "boundary.emit_next_unit.v0",
    "expected_authority_verdict": "REQUIRES_PROPOSAL",
    "expected_halt": "STOP_PROPOSAL_REQUIRED",
    "expected_proposal_status": "PROPOSED_ONLY",
    "must_not_execute_candidate": True,
    "must_not_register_candidate": True,
}

DEMO_EXTRACTION_REQUIRED_PLAN = {
    "schema_version": "day5_demo_extraction_required_plan_v0",
    "demo_name": "DAY5_EXTRACTION_REQUIRED",
    "admissible_move": "proto.import_behavior.v0",
    "expected_authority_verdict": "REQUIRES_EXTRACTION",
    "expected_halt": "STOP_NEEDS_EXTRACTION",
    "must_not_execute": True,
}

DEMO_HUMAN_REVIEW_REQUIRED_PLAN = {
    "schema_version": "day5_demo_human_review_required_plan_v0",
    "demo_name": "DAY5_HUMAN_REVIEW_REQUIRED",
    "admissible_move": "move_registry.add_candidate.v0",
    "expected_authority_verdict": "REQUIRES_HUMAN_REVIEW",
    "expected_halt": "STOP_HUMAN_REVIEW_REQUIRED",
    "expected_review_default": "NO_EXECUTION",
    "must_not_execute_without_review": True,
    "must_not_mutate_registry": True,
}

DEMO_FORBIDDEN_MOVE_PLAN = {
    "schema_version": "day5_demo_forbidden_move_plan_v0",
    "demo_name": "DAY5_FORBIDDEN_MOVE",
    "admissible_move": "execute_unregistered_move.v0",
    "expected_authority_verdict": "FORBIDDEN",
    "expected_halt": "STOP_FORBIDDEN_MOVE",
    "must_not_execute": True,
    "must_not_propose_as_currently_shaped": True,
}

REQUIRED_IMPLEMENTATION_ARTIFACTS = {
    "jurisdiction_profile_schema": "data/jurisdiction_gate_v0/jurisdiction_profile_schema_v0.json",
    "jurisdiction_verdict_enum": "data/jurisdiction_gate_v0/jurisdiction_verdict_enum_v0.json",
    "move_authority_patch": "data/jurisdiction_gate_v0/move_authority_patch_v0.json",
    "jurisdiction_gate": "data/jurisdiction_gate_v0/jurisdiction_gate_v0.json",
    "authority_verdict_record_schema": "data/jurisdiction_gate_v0/authority_verdict_record_schema_v0.json",
    "authority_blocked_move_record_schema": "data/jurisdiction_gate_v0/authority_blocked_move_record_schema_v0.json",
    "proposal_packet_schema": "data/jurisdiction_gate_v0/proposal_packet_schema_v0.json",
    "human_review_request_schema": "data/jurisdiction_gate_v0/human_review_request_schema_v0.json",
    "halt_vocabulary_authority_patch": "data/jurisdiction_gate_v0/halt_vocabulary_authority_patch_v0.json",
    "move_inspection_authority_patch": "data/jurisdiction_gate_v0_patches/move_inspection_authority_patch_v0.json",
    "trace_authority_patch": "data/jurisdiction_gate_v0_patches/trace_authority_patch_v0.json",
    "receipt_authority_patch": "data/jurisdiction_gate_v0_patches/receipt_authority_patch_v0.json",
    "proceed_readout_authority_patch": "data/jurisdiction_gate_v0_patches/proceed_readout_authority_patch_v0.json",
    "day5_demo_authorized_move": "data/jurisdiction_gate_v0_demo/day5_demo_authorized_move.json",
    "day5_demo_proposal_required": "data/jurisdiction_gate_v0_demo/day5_demo_proposal_required.json",
    "day5_demo_extraction_required": "data/jurisdiction_gate_v0_demo/day5_demo_extraction_required.json",
    "day5_demo_human_review_required": "data/jurisdiction_gate_v0_demo/day5_demo_human_review_required.json",
    "day5_demo_forbidden_move": "data/jurisdiction_gate_v0_demo/day5_demo_forbidden_move.json",
    "day5_demo_authority_receipt": "data/jurisdiction_gate_v0_demo/day5_demo_authority_receipt.json",
    "implementation_receipt": "data/jurisdiction_gate_v0_implementation_receipts/<receipt_id>.json",
}

ACCEPTANCE_GATES = {
    "JGP0_source_surface_verified": {
        "required": True,
        "description": "Consumes Day 4 move registry implementation, Day 3 halt vocabulary, proceed adapter, trace ledger, and local regime sources.",
    },
    "JGP1_jurisdiction_profile_schema_declared": {
        "required": True,
        "description": "Local jurisdiction profile schema is declared and explicitly non-global.",
    },
    "JGP2_verdict_enum_declared": {
        "required": True,
        "description": "Five jurisdiction verdicts are declared.",
    },
    "JGP3_halt_vocabulary_authority_patch_declared": {
        "required": True,
        "description": "Authority boundary halt patch is declared without mutating the base vocabulary.",
    },
    "JGP4_move_authority_patch_declared": {
        "required": True,
        "description": "Move authority field patch is declared without mutating the Day 4 registry.",
    },
    "JGP5_every_admissible_move_receives_authority_verdict": {
        "required": True,
        "description": "Implementation must verdict every admissible_pre_auth move.",
    },
    "JGP6_selector_restricted_to_authorized_local": {
        "required": True,
        "description": "Selector input is authorized_executable_moves only.",
    },
    "JGP7_proposal_required_emits_proposed_only_packet": {
        "required": True,
        "description": "REQUIRES_PROPOSAL emits PROPOSED_ONLY packet and does not execute.",
    },
    "JGP8_extraction_required_halts_without_execution": {
        "required": True,
        "description": "REQUIRES_EXTRACTION maps to STOP_NEEDS_EXTRACTION and does not execute.",
    },
    "JGP9_human_review_required_emits_review_request": {
        "required": True,
        "description": "REQUIRES_HUMAN_REVIEW emits review request and does not execute without approval.",
    },
    "JGP10_forbidden_move_cannot_execute_or_self_reframe": {
        "required": True,
        "description": "FORBIDDEN maps to STOP_FORBIDDEN_MOVE and cannot be proposed as currently shaped.",
    },
    "JGP11_authority_verdicts_link_to_trace_receipt_readout": {
        "required": True,
        "description": "Authority verdicts are linkable into trace, receipt, and proceed-readout patches.",
    },
    "JGP12_no_registry_taxonomy_jurisdiction_mutation": {
        "required": True,
        "description": "Policy cannot mutate registry, taxonomy, or jurisdiction profile.",
    },
    "JGP13_day6_taxonomy_evolution_not_implemented": {
        "required": True,
        "description": "Day 5 does not implement taxonomy evolution.",
    },
    "JGP14_patch_artifacts_only_no_old_schema_mutation": {
        "required": True,
        "description": "All patches are future-schema patches only.",
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

def validate_inputs() -> List[str]:
    failures: List[str] = []

    move_impl = read_json(MOVE_IMPL_RECEIPT_PATH)
    move_policy = read_json(MOVE_POLICY_PATH)
    move_policy_receipt = read_json(MOVE_POLICY_RECEIPT_PATH)
    move_registry = read_json(MOVE_REGISTRY_PATH)
    move_admission_gate = read_json(MOVE_ADMISSION_GATE_PATH)
    move_inspection_schema = read_json(MOVE_INSPECTION_SCHEMA_PATH)
    blocked_move_schema = read_json(BLOCKED_MOVE_SCHEMA_PATH)
    missing_move_stub = read_json(MISSING_MOVE_STUB_PATH)
    day4_positive = read_json(DAY4_POSITIVE_RUN_PATH)
    day4_missing = read_json(DAY4_MISSING_MOVE_RUN_PATH)

    halt_impl = read_json(HALT_IMPLEMENTATION_RECEIPT_PATH)
    halt_vocab = read_json(HALT_VOCABULARY_PATH)
    proceed_receipt = read_json(PROCEED_RECEIPT_PATH)
    trace_ledger_receipt = read_json(TRACE_LEDGER_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    proposal_ledger_schema = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    local_regime = read_json(LOCAL_REGIME_V1_PATH)

    if move_impl.get("receipt_id") != MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"move_impl_receipt_id_wrong:{move_impl.get('receipt_id')}")
    if move_impl.get("gate") != "PASS":
        failures.append(f"move_impl_gate_not_PASS:{move_impl.get('gate')}")
    if move_impl.get("target_unit_id") != "move_registry.v0":
        failures.append(f"move_impl_target_wrong:{move_impl.get('target_unit_id')}")
    if move_impl.get("terminal", {}).get("type") != "STOP":
        failures.append(f"move_impl_terminal_not_STOP:{move_impl.get('terminal')}")
    if move_impl.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append(f"move_impl_terminal_not_DONE:{move_impl.get('terminal')}")
    if move_impl.get("terminal", {}).get("next_command_goal") is not None:
        failures.append(f"move_impl_terminal_next_not_null:{move_impl.get('terminal')}")

    move_metrics = move_impl.get("aggregate_metrics", {})
    if move_metrics.get("starter_move_count") != 7:
        failures.append(f"starter_move_count_wrong:{move_metrics.get('starter_move_count')}")
    if move_metrics.get("authorization_deferred_count") != 2:
        failures.append(f"authorization_deferred_count_wrong:{move_metrics.get('authorization_deferred_count')}")
    for key in [
        "unregistered_move_fire_count",
        "schema_invalid_move_fire_count",
        "missing_move_candidate_registered_count",
        "missing_move_candidate_executed_count",
        "missing_move_proposal_accepted_count",
        "taxonomy_delta_applied_count",
        "taxonomy_delta_promoted_count",
        "day5_authority_resolution_count",
        "jurisdiction_resolved_count",
        "registry_sqlite_write_count",
        "proof_claim_count",
        "hidden_continuation_count",
    ]:
        if move_metrics.get(key) != 0:
            failures.append(f"move_impl_metric_not_zero:{key}:{move_metrics.get(key)}")

    if move_policy.get("policy_id") != MOVE_REGISTRY_POLICY_ID:
        failures.append(f"move_policy_id_wrong:{move_policy.get('policy_id')}")
    if move_policy_receipt.get("receipt_id") != MOVE_REGISTRY_POLICY_RECEIPT_ID:
        failures.append(f"move_policy_receipt_id_wrong:{move_policy_receipt.get('receipt_id')}")
    if move_policy_receipt.get("gate") != "PASS":
        failures.append(f"move_policy_receipt_gate_not_PASS:{move_policy_receipt.get('gate')}")

    if move_registry.get("move_registry_id") != "move_registry_v0":
        failures.append(f"move_registry_id_wrong:{move_registry.get('move_registry_id')}")
    if len(move_registry.get("moves", {})) != 7:
        failures.append(f"move_registry_count_wrong:{len(move_registry.get('moves', {}))}")
    if "no unregistered move may fire" not in move_registry.get("registry_law", []):
        failures.append("move_registry_core_law_missing")
    if move_admission_gate.get("admission_status_name") != "ADMISSIBLE_PRE_AUTH":
        failures.append(f"move_admission_status_wrong:{move_admission_gate.get('admission_status_name')}")
    if move_admission_gate.get("authorization_status") != "DEFERRED_TO_DAY5":
        failures.append(f"move_authorization_status_wrong:{move_admission_gate.get('authorization_status')}")
    if "authorization_status" not in move_inspection_schema.get("required_fields", []):
        failures.append("move_inspection_schema_missing_authorization_status")
    if "AUTHORITY_DEFERRED" not in blocked_move_schema.get("block_reasons", []):
        failures.append("day4_blocked_schema_missing_AUTHORITY_DEFERRED")
    if missing_move_stub.get("status") != "PROPOSED_ONLY":
        failures.append(f"missing_move_stub_not_proposed_only:{missing_move_stub.get('status')}")

    if day4_positive.get("gate") != "PASS" or day4_positive.get("terminal_result", {}).get("stop_code") != "STOP_NEXT_MOVE_BOUNDARY":
        failures.append("day4_positive_source_not_pass")
    if day4_missing.get("gate") != "PASS" or day4_missing.get("terminal_result", {}).get("stop_code") != "STOP_NEEDS_NEW_MOVE":
        failures.append("day4_missing_source_not_pass")
    if day4_missing.get("proposal_status") != "PROPOSED_ONLY":
        failures.append("day4_missing_proposal_not_proposed_only")

    if halt_impl.get("receipt_id") != HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID or halt_impl.get("gate") != "PASS":
        failures.append("halt_impl_source_not_pass")
    halt_entries = halt_vocab.get("entries", {})
    for required in [
        "STOP_AUTHORITY_VIOLATION",
        "STOP_NEEDS_EXTRACTION",
        "STOP_NEEDS_NEW_MOVE",
        "STOP_GATE_FAIL",
    ]:
        if required not in halt_entries:
            failures.append(f"halt_vocab_missing_required:{required}")
    if "NO_APPLICABLE_MOVE" in halt_entries:
        failures.append("NO_APPLICABLE_MOVE_canonical_leaked")

    if proceed_receipt.get("receipt_id") != PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID or proceed_receipt.get("gate") != "PASS":
        failures.append("proceed_receipt_source_not_pass")
    if trace_ledger_receipt.get("receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID or trace_ledger_receipt.get("gate") != "PASS":
        failures.append("trace_ledger_source_not_pass")
    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append("trace_schema_version_wrong")
    if proposal_ledger_schema.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append("proposal_ledger_schema_version_wrong")
    if local_regime.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append("local_regime_hash_wrong")

    for path in [
        MOVE_IMPL_RECEIPT_PATH,
        MOVE_POLICY_PATH,
        MOVE_POLICY_RECEIPT_PATH,
        MOVE_REGISTRY_PATH,
        MOVE_ADMISSION_GATE_PATH,
        MOVE_INSPECTION_SCHEMA_PATH,
        BLOCKED_MOVE_SCHEMA_PATH,
        SELECTED_MOVE_SCHEMA_PATH,
        MISSING_MOVE_STUB_PATH,
        DAY4_POSITIVE_RUN_PATH,
        DAY4_MISSING_MOVE_RUN_PATH,
        HALT_IMPLEMENTATION_RECEIPT_PATH,
        HALT_POLICY_PATH,
        HALT_VOCABULARY_PATH,
        HALT_RECORD_SCHEMA_PATH,
        HALT_NEXT_HANDLING_PATH,
        PROCEED_RECEIPT_PATH,
        PROCEED_ADAPTER_MODULE_PATH,
        TRACE_LEDGER_RECEIPT_PATH,
        TRACE_SCHEMA_PATH,
        PROPOSAL_LEDGER_SCHEMA_PATH,
        TRACE_LEDGER_RUNNER_PATH,
        LOCAL_REGIME_V1_PATH,
    ]:
        if not tracked(path):
            failures.append(f"source_artifact_not_tracked:{path.relative_to(ROOT).as_posix()}")

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
        failures.append("policy_id_receipt_mismatch")

    profile = policy.get("jurisdiction_profile_schema", {})
    for field in [
        "jurisdiction_profile_id",
        "schema_version",
        "scope",
        "authorized_local",
        "proposal_allowed",
        "requires_extraction",
        "requires_human_review",
        "forbidden",
    ]:
        if field not in profile.get("required_fields", []):
            failures.append(f"jurisdiction_profile_schema_required_missing:{field}")
    if profile.get("profile_is_local") is not True:
        failures.append("jurisdiction_profile_not_local")
    if "global governance" not in profile.get("must_not_impersonate", []):
        failures.append("jurisdiction_profile_missing_global_non_impersonation")

    verdict_enum = policy.get("jurisdiction_verdict_enum", {})
    if verdict_enum.get("verdicts") != VERDICTS:
        failures.append(f"verdict_enum_wrong:{verdict_enum.get('verdicts')}")
    if verdict_enum.get("verdict_to_halt", {}).get("REQUIRES_EXTRACTION") != "STOP_NEEDS_EXTRACTION":
        failures.append("requires_extraction_not_mapped_to_STOP_NEEDS_EXTRACTION")

    halt_patch = policy.get("halt_vocabulary_authority_patch", {})
    if halt_patch.get("patch_mode") != "future_halt_vocabulary_patch_only_do_not_mutate_existing_halt_vocabulary":
        failures.append(f"halt_patch_mode_wrong:{halt_patch.get('patch_mode')}")
    for code in [
        "STOP_AUTHORITY_BOUNDARY",
        "STOP_PROPOSAL_REQUIRED",
        "STOP_HUMAN_REVIEW_REQUIRED",
        "STOP_FORBIDDEN_MOVE",
    ]:
        if code not in halt_patch.get("adds_canonical_entries", {}):
            failures.append(f"halt_authority_patch_missing:{code}")
    if halt_patch.get("reuses_existing_entries", {}).get("STOP_NEEDS_EXTRACTION") != "used for REQUIRES_EXTRACTION verdict":
        failures.append("halt_patch_not_reusing_STOP_NEEDS_EXTRACTION")

    move_patch = policy.get("move_authority_patch", {})
    if move_patch.get("patch_mode") != "future_move_schema_patch_only_do_not_mutate_existing_move_registry":
        failures.append(f"move_authority_patch_mode_wrong:{move_patch.get('patch_mode')}")
    if "authority" not in move_patch.get("add_field", {}):
        failures.append("move_authority_patch_missing_authority_field")

    gate = policy.get("jurisdiction_gate", {})
    if gate.get("execution_rule") != "Only AUTHORIZED_LOCAL moves may execute.":
        failures.append(f"jurisdiction_execution_rule_wrong:{gate.get('execution_rule')}")
    if gate.get("selector_rule") != "Selector may only choose from authorized_executable_moves.":
        failures.append(f"jurisdiction_selector_rule_wrong:{gate.get('selector_rule')}")
    if gate.get("verdict_order")[:5] != [
        "FORBIDDEN",
        "REQUIRES_EXTRACTION",
        "REQUIRES_HUMAN_REVIEW",
        "REQUIRES_PROPOSAL",
        "AUTHORIZED_LOCAL",
    ]:
        failures.append(f"jurisdiction_verdict_order_wrong:{gate.get('verdict_order')}")

    verdict_schema = policy.get("authority_verdict_record_schema", {})
    for field in [
        "authority_verdict_id",
        "run_id",
        "state_sig8",
        "move_id",
        "move_admissibility_status",
        "jurisdiction_profile_id",
        "authority_verdict",
        "terminal_if_not_authorized",
        "proposal_ref",
        "review_request_ref",
        "must_not_impersonate",
    ]:
        if field not in verdict_schema.get("required_fields", []):
            failures.append(f"authority_verdict_schema_missing:{field}")

    authority_blocked = policy.get("authority_blocked_move_record_schema", {})
    for reason in [
        "AUTHORITY_BOUNDARY",
        "PROPOSAL_ONLY",
        "HUMAN_REVIEW_REQUIRED",
        "EXTRACTION_REQUIRED",
        "FORBIDDEN_BY_PROFILE",
    ]:
        if reason not in authority_blocked.get("authority_block_reasons", []):
            failures.append(f"authority_block_reason_missing:{reason}")

    proposal_schema = policy.get("proposal_packet_schema", {})
    if proposal_schema.get("status") != "PROPOSED_ONLY":
        failures.append(f"proposal_schema_status_wrong:{proposal_schema.get('status')}")
    for phrase in [
        "A proposal is not execution.",
        "A proposal is not acceptance.",
        "A proposal is not authority.",
    ]:
        if phrase not in proposal_schema.get("core_law", []):
            failures.append(f"proposal_core_law_missing:{phrase}")

    review_schema = policy.get("human_review_request_schema", {})
    if review_schema.get("default_without_response") != "NO_EXECUTION":
        failures.append(f"review_default_wrong:{review_schema.get('default_without_response')}")
    if review_schema.get("core_law") != "No response means no execution.":
        failures.append(f"review_core_law_wrong:{review_schema.get('core_law')}")

    for patch_key, mode in [
        ("move_inspection_authority_patch", "future_schema_patch_only_do_not_mutate_existing_day4_inspections"),
        ("trace_authority_patch", "future_schema_patch_only_do_not_mutate_existing_traces"),
        ("receipt_authority_patch", "future_schema_patch_only_do_not_mutate_existing_receipts"),
        ("proceed_readout_authority_patch", "future_schema_patch_only_do_not_mutate_existing_readouts"),
    ]:
        if policy.get(patch_key, {}).get("patch_mode") != mode:
            failures.append(f"{patch_key}_mode_wrong:{policy.get(patch_key, {}).get('patch_mode')}")

    demo_expectations = {
        "day5_demo_authorized_move_plan": ("expected_authority_verdict", "AUTHORIZED_LOCAL"),
        "day5_demo_proposal_required_plan": ("expected_authority_verdict", "REQUIRES_PROPOSAL"),
        "day5_demo_extraction_required_plan": ("expected_authority_verdict", "REQUIRES_EXTRACTION"),
        "day5_demo_human_review_required_plan": ("expected_authority_verdict", "REQUIRES_HUMAN_REVIEW"),
        "day5_demo_forbidden_move_plan": ("expected_authority_verdict", "FORBIDDEN"),
    }
    for demo_key, (field, expected) in demo_expectations.items():
        if policy.get(demo_key, {}).get(field) != expected:
            failures.append(f"{demo_key}_{field}_wrong:{policy.get(demo_key, {}).get(field)}")

    gates = policy.get("acceptance_gates", {})
    for gate_id in ACCEPTANCE_GATES:
        if gates.get(gate_id, {}).get("required") is not True:
            failures.append(f"acceptance_gate_missing:{gate_id}")

    guards = policy.get("authority_guards", {})
    for key in [
        "jurisdiction_gate_policy_built",
        "source_move_registry_consumed",
        "source_halt_vocabulary_consumed",
        "source_proceed_adapter_consumed",
        "source_trace_ledger_surface_consumed",
    ]:
        if guards.get(key) is not True:
            failures.append(f"authority_guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "implementation_performed_by_policy",
        "demo_verdicts_emitted_by_policy",
        "source_move_registry_modified",
        "source_halt_vocabulary_modified",
        "source_proceed_adapter_modified",
        "source_trace_ledger_runner_modified",
        "source_local_regime_v1_modified",
        "registry_mutated",
        "taxonomy_delta_applied",
        "taxonomy_delta_promoted",
        "jurisdiction_profile_modified",
        "jurisdiction_resolved_globally",
        "proposal_accepted",
        "proposal_executed",
        "human_silence_authorized",
        "forbidden_move_softened_to_proposal",
        "day6_taxonomy_evolution_implemented",
        "sqlite_registry_written",
        "global_governance_claimed",
        "final_authority_claimed",
        "proof_claimed",
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
    failures = validate_inputs()

    policy_seed = {
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_move_impl": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "verdicts": VERDICTS,
        "next_goal": NEXT_GOAL,
    }
    policy_id = sha8(policy_seed)

    authority_guards = {
        "jurisdiction_gate_policy_built": True,
        "source_move_registry_consumed": True,
        "source_halt_vocabulary_consumed": True,
        "source_proceed_adapter_consumed": True,
        "source_trace_ledger_surface_consumed": True,
        "implementation_performed_by_policy": False,
        "demo_verdicts_emitted_by_policy": False,
        "source_move_registry_modified": False,
        "source_halt_vocabulary_modified": False,
        "source_proceed_adapter_modified": False,
        "source_trace_ledger_runner_modified": False,
        "source_local_regime_v1_modified": False,
        "source_trace_modified": False,
        "source_receipt_modified": False,
        "source_ledger_modified": False,
        "registry_mutated": False,
        "taxonomy_delta_applied": False,
        "taxonomy_delta_promoted": False,
        "jurisdiction_profile_modified": False,
        "jurisdiction_resolved_globally": False,
        "proposal_accepted": False,
        "proposal_executed": False,
        "human_silence_authorized": False,
        "forbidden_move_softened_to_proposal": False,
        "day6_taxonomy_evolution_implemented": False,
        "sqlite_registry_read": False,
        "sqlite_registry_written": False,
        "global_governance_claimed": False,
        "final_authority_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
    }

    policy = {
        "schema_version": "jurisdiction_gate_v0_policy_v0",
        "policy_type": "JURISDICTION_GATE_V0_POLICY",
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "target_unit_id": TARGET_UNIT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "source_move_registry_policy_id": MOVE_REGISTRY_POLICY_ID,
        "source_move_registry_policy_receipt_id": MOVE_REGISTRY_POLICY_RECEIPT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_policy_id": HALT_VOCABULARY_POLICY_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": {
            "purpose": "Separate admissible_pre_auth moves from authorized executable moves.",
            "core_law": "A move may be locally admissible and still not authorized.",
            "execution_rule": "Only AUTHORIZED_LOCAL moves may execute.",
            "selector_rule": "Selector may only choose from authorized_executable_moves.",
            "non_goal": "no final governance, no global autonomy, no proposal self-approval, no registry mutation, no Day 6 taxonomy evolution",
        },
        "jurisdiction_profile_schema": JURISDICTION_PROFILE_SCHEMA,
        "jurisdiction_verdict_enum": JURISDICTION_VERDICT_ENUM,
        "move_authority_patch": MOVE_AUTHORITY_PATCH,
        "jurisdiction_gate": JURISDICTION_GATE,
        "authority_verdict_record_schema": AUTHORITY_VERDICT_RECORD_SCHEMA,
        "authority_blocked_move_record_schema": AUTHORITY_BLOCKED_MOVE_RECORD_SCHEMA,
        "proposal_packet_schema": PROPOSAL_PACKET_SCHEMA,
        "human_review_request_schema": HUMAN_REVIEW_REQUEST_SCHEMA,
        "halt_vocabulary_authority_patch": HALT_VOCABULARY_AUTHORITY_PATCH,
        "move_inspection_authority_patch": MOVE_INSPECTION_AUTHORITY_PATCH,
        "trace_authority_patch": TRACE_AUTHORITY_PATCH,
        "receipt_authority_patch": RECEIPT_AUTHORITY_PATCH,
        "proceed_readout_authority_patch": PROCEED_READOUT_AUTHORITY_PATCH,
        "day5_demo_authorized_move_plan": DEMO_AUTHORIZED_MOVE_PLAN,
        "day5_demo_proposal_required_plan": DEMO_PROPOSAL_REQUIRED_PLAN,
        "day5_demo_extraction_required_plan": DEMO_EXTRACTION_REQUIRED_PLAN,
        "day5_demo_human_review_required_plan": DEMO_HUMAN_REVIEW_REQUIRED_PLAN,
        "day5_demo_forbidden_move_plan": DEMO_FORBIDDEN_MOVE_PLAN,
        "required_implementation_artifacts": REQUIRED_IMPLEMENTATION_ARTIFACTS,
        "acceptance_gates": ACCEPTANCE_GATES,
        "authorized_operations_next": {
            "read_jurisdiction_gate_policy": True,
            "read_jurisdiction_gate_policy_receipt": True,
            "write_jurisdiction_profile_schema_artifact": True,
            "write_jurisdiction_verdict_enum_artifact": True,
            "write_move_authority_patch_artifact": True,
            "write_jurisdiction_gate_artifact": True,
            "write_authority_verdict_record_schema_artifact": True,
            "write_authority_blocked_move_record_schema_artifact": True,
            "write_proposal_packet_schema_artifact": True,
            "write_human_review_request_schema_artifact": True,
            "write_halt_vocabulary_authority_patch_artifact": True,
            "write_move_inspection_authority_patch_artifact": True,
            "write_trace_authority_patch_artifact": True,
            "write_receipt_authority_patch_artifact": True,
            "write_proceed_readout_authority_patch_artifact": True,
            "emit_day5_demo_authorized_move": True,
            "emit_day5_demo_proposal_required": True,
            "emit_day5_demo_extraction_required": True,
            "emit_day5_demo_human_review_required": True,
            "emit_day5_demo_forbidden_move": True,
            "emit_day5_demo_authority_receipt": True,
            "emit_implementation_receipt": True,
        },
        "forbidden_operations_next": {
            "mutate_existing_move_registry": True,
            "mutate_existing_halt_vocabulary": True,
            "mutate_existing_trace_files": True,
            "mutate_existing_receipt_files": True,
            "mutate_existing_readout_files": True,
            "modify_trace_ledger_runner_module": True,
            "modify_proceed_adapter_module": True,
            "modify_local_regime_v1": True,
            "select_from_admissible_without_authority": True,
            "execute_non_authorized_move": True,
            "execute_requires_proposal_move": True,
            "execute_requires_extraction_move": True,
            "execute_requires_human_review_move_without_approval": True,
            "execute_forbidden_move": True,
            "treat_proposal_as_approval": True,
            "treat_human_silence_as_authorization": True,
            "soften_forbidden_move_into_proposal_without_reformulation": True,
            "mutate_registry_from_proposal": True,
            "mutate_taxonomy_from_proposal": True,
            "mutate_jurisdiction_profile": True,
            "implement_day6_taxonomy_evolution": True,
            "sqlite_registry_write": True,
            "sqlite_registry_read": True,
            "global_governance_claim": True,
            "final_authority_claim": True,
            "proof_claim": True,
            "hidden_continuation_after_terminal": True,
            "latest_or_mtime_selection": True,
            "ambient_workspace_authority": True,
        },
        "safety_clauses": {
            "policy_only": True,
            "does_not_emit_demo_verdicts": True,
            "does_not_mutate_existing_artifacts": True,
            "does_not_modify_source_modules": True,
            "does_not_modify_source_regime": True,
            "does_not_modify_move_registry": True,
            "does_not_modify_halt_vocabulary": True,
            "halt_vocabulary_authority_patch_only": True,
            "does_not_accept_or_execute_proposals": True,
            "does_not_treat_human_silence_as_authorization": True,
            "does_not_implement_day6_taxonomy_evolution": True,
            "does_not_claim_global_authority": True,
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
        "source_move_impl": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "terminal": policy["terminal"],
    }
    receipt_id = sha8(receipt_seed)
    policy["policy_receipt_id"] = receipt_id

    receipt = {
        "schema_version": "jurisdiction_gate_v0_policy_receipt_v0",
        "receipt_type": "JURISDICTION_GATE_V0_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "target_unit_id": TARGET_UNIT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "source_move_registry_policy_id": MOVE_REGISTRY_POLICY_ID,
        "source_move_registry_policy_receipt_id": MOVE_REGISTRY_POLICY_RECEIPT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_policy_id": HALT_VOCABULARY_POLICY_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": policy["policy_summary"],
        "jurisdiction_profile_schema": JURISDICTION_PROFILE_SCHEMA,
        "jurisdiction_verdict_enum": JURISDICTION_VERDICT_ENUM,
        "move_authority_patch": MOVE_AUTHORITY_PATCH,
        "jurisdiction_gate": JURISDICTION_GATE,
        "authority_verdict_record_schema": AUTHORITY_VERDICT_RECORD_SCHEMA,
        "authority_blocked_move_record_schema": AUTHORITY_BLOCKED_MOVE_RECORD_SCHEMA,
        "proposal_packet_schema": PROPOSAL_PACKET_SCHEMA,
        "human_review_request_schema": HUMAN_REVIEW_REQUEST_SCHEMA,
        "halt_vocabulary_authority_patch": HALT_VOCABULARY_AUTHORITY_PATCH,
        "move_inspection_authority_patch": MOVE_INSPECTION_AUTHORITY_PATCH,
        "trace_authority_patch": TRACE_AUTHORITY_PATCH,
        "receipt_authority_patch": RECEIPT_AUTHORITY_PATCH,
        "proceed_readout_authority_patch": PROCEED_READOUT_AUTHORITY_PATCH,
        "day5_demo_authorized_move_plan": DEMO_AUTHORIZED_MOVE_PLAN,
        "day5_demo_proposal_required_plan": DEMO_PROPOSAL_REQUIRED_PLAN,
        "day5_demo_extraction_required_plan": DEMO_EXTRACTION_REQUIRED_PLAN,
        "day5_demo_human_review_required_plan": DEMO_HUMAN_REVIEW_REQUIRED_PLAN,
        "day5_demo_forbidden_move_plan": DEMO_FORBIDDEN_MOVE_PLAN,
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
    print(f"jurisdiction_gate_policy_id={policy['policy_id']}")
    print(f"jurisdiction_gate_policy_receipt_id={receipt['receipt_id']}")
    print(f"jurisdiction_gate_policy_path=data/jurisdiction_gate_v0_policies/{policy['policy_id']}.json")
    print(f"jurisdiction_gate_policy_receipt_path=data/jurisdiction_gate_v0_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
