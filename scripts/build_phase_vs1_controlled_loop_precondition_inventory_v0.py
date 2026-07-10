#!/usr/bin/env python3

"""Build VS1.3 controlled loop precondition inventory."""

from __future__ import annotations

import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


SCRIPT = "scripts/build_phase_vs1_controlled_loop_precondition_inventory_v0.py"
EXPECTED_HEAD = "d62db2d74f2ff42bf7f633b4e2169aed409a0703"
OUTPUT_JSON = (
    "docs/matrixlabs/phase_vs1/"
    "phase_vs1_controlled_loop_precondition_inventory_v0.json"
)
OUTPUT_MD = (
    "docs/matrixlabs/phase_vs1/"
    "phase_vs1_controlled_loop_precondition_inventory_v0.md"
)

SOURCE_CONTRACT_JSON = (
    "docs/matrixlabs/phase_vs1/"
    "phase_vs1_controlled_convergence_loop_contract_v0.json"
)
SOURCE_CONTRACT_MD = (
    "docs/matrixlabs/phase_vs1/"
    "phase_vs1_controlled_convergence_loop_contract_v0.md"
)
SOURCE_INTAKE_JSON = (
    "docs/matrixlabs/phase_vs1/phase_vs1_post_vs0_source_intake_v0.json"
)
SOURCE_INTAKE_MD = (
    "docs/matrixlabs/phase_vs1/phase_vs1_post_vs0_source_intake_v0.md"
)
DIRECTION_JSON = "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.json"
DIRECTION_MD = "docs/matrixlabs/phase_vs1/post_vs0_direction_decision_receipt_v0.md"
VS0_ROOT = "docs/matrixlabs/phase_vs0"
VS0_CLOSURE_JSON = "docs/matrixlabs/phase_vs0/phase_vs0_closure_v0.json"
VS0_EVIDENCE_YIELD_JSON = (
    "docs/matrixlabs/phase_vs0/phase_vs0_evidence_yield_report_v0.json"
)
VS0_HAPPY_PATH_VERIFICATION_JSON = (
    "docs/matrixlabs/phase_vs0/phase_vs0_happy_path_verification_v0.json"
)
VS0_NEGATIVE_PROBE_JSON = (
    "docs/matrixlabs/phase_vs0/runs/phase_vs0_first_specimen_runtime_v0/"
    "negative_probes/phase_vs0_negative_probe_battery_v0.json"
)

SCHEMA_VERSION = "matrixlabs_phase_vs1_controlled_loop_precondition_inventory_v0"
ARTIFACT_ID = "phase_vs1_controlled_loop_precondition_inventory_v0"
PHASE_ID = "PHASE_VS1"
UNIT_ID = "VS1.3_CONTROLLED_LOOP_PRECONDITION_INVENTORY"
UNIT_ROLE = "PRECONDITION_INVENTORY_ONLY"
CONTRACT_ARTIFACT_ID = "phase_vs1_controlled_convergence_loop_contract_v0"
CONTRACT_STATUS = "VS1_2_CONTROLLED_LOOP_CONTRACT_DEFINITION_PASS"
CONTRACT_TRANSITION = "ADVANCE(VS1_3_CONTROLLED_LOOP_PRECONDITION_INVENTORY_PENDING)"
PASS_VERDICT = "VS1_3_CONTROLLED_LOOP_PRECONDITION_INVENTORY_PASS"
ARTIFACT_TRANSITION = "ADVANCE(VS1_4_CONTROLLED_LOOP_READINESS_AUDIT_PENDING)"
PRINT_TRANSITION = (
    "ADVANCE(BOOKKEEPING_COMMIT_PHASE_VS1_CONTROLLED_LOOP_PRECONDITION_"
    "INVENTORY_V0_PENDING)"
)

VALID_STATUSES = {
    "PRESENT_VERIFIED",
    "PRESENT_PARTIAL",
    "PRESENT_CANDIDATE_ONLY",
    "PRESENT_BOUNDARY_ONLY",
    "MISSING",
    "INSUFFICIENT",
    "SOURCE_UNVERIFIED",
    "OUT_OF_SCOPE",
}
VALID_BLOCKERS = {
    "AUTHORITY_REQUIRED",
    "PROMOTION_REQUIRED",
    "SCHEMA_REQUIRED",
    "HUMAN_DECISION_REQUIRED",
    "SOURCE_STATUS_REQUIRED",
    "CONTRACT_REVISION_REQUIRED",
    "NONE",
}
STATUS_COUNT_KEY = {
    "PRESENT_VERIFIED": "present_verified",
    "PRESENT_PARTIAL": "present_partial",
    "PRESENT_CANDIDATE_ONLY": "present_candidate_only",
    "PRESENT_BOUNDARY_ONLY": "present_boundary_only",
    "MISSING": "missing",
    "INSUFFICIENT": "insufficient",
    "SOURCE_UNVERIFIED": "source_unverified",
    "OUT_OF_SCOPE": "out_of_scope",
}
BLOCKER_COUNT_KEY = {
    "AUTHORITY_REQUIRED": "authority_required",
    "PROMOTION_REQUIRED": "promotion_required",
    "SCHEMA_REQUIRED": "schema_required",
    "HUMAN_DECISION_REQUIRED": "human_decision_required",
    "SOURCE_STATUS_REQUIRED": "source_status_required",
    "CONTRACT_REVISION_REQUIRED": "contract_revision_required",
    "NONE": "none",
}
PLACEHOLDER_VALUES = {
    "<inventory_status>",
    "<TBD>",
    "TBD",
    "TODO",
    "UNKNOWN",
    "PLACEHOLDER",
    "",
}

EXPECTED_COMPONENTS = [
    "C01_SCOPE_REGIME_DECLARATION_CONTRACT",
    "C02_TYPED_STATE_OBJECT_CONTRACT",
    "C03_EXPLICIT_MOVE_SPACE_CONTRACT",
    "C04_MOVE_SELECTOR_CONTRACT",
    "C05_MOVE_APPLICATOR_CONTRACT",
    "C06_AUTHORITY_POLICY",
    "C07_RADIUS_BUDGET_POLICY",
    "C08_HALT_POLICY",
    "C09_RECEIPT_OBLIGATION_CONTRACT",
    "C10_SOURCE_IDENTITY_FRESHNESS_POLICY",
    "C11_MICRO_SWEEP_BOUNDS_CONTRACT",
    "C12_PRESSURE_READOUT_CONTRACT",
    "C13_PRESSURE_CLASSIFICATION_VOCABULARY",
    "C14_LOCAL_REVISION_SURFACE_CONTRACT",
    "C15_BOUNDED_PORTABILITY_MAP_CONTRACT",
    "C16_REPLAY_AUDIT_CONTRACT",
    "C17_FORBIDDEN_EFFECT_GUARD",
    "C18_EVIDENCE_YIELD_REPORT_HOOK",
    "C19_HUMAN_ESCALATION_DECISION_BOUNDARY",
    "C20_CONVERGENCE_CRITERION_CONTRACT",
]

COMPONENT_METADATA = [
    {
        "component_id": "C01",
        "component_name": "SCOPE_REGIME_DECLARATION_CONTRACT",
        "required_for_loop_stage": "L0_SCOPE_REGIME_DECLARATION",
        "expected_function": (
            "declare the local scope/regime and allowed/forbidden regime movement"
        ),
        "required_fields": [
            "scope_id",
            "regime_id",
            "allowed_source_surfaces",
            "forbidden_source_surfaces",
            "allowed_regime_transitions",
            "forbidden_regime_transitions",
            "object_identity_rules",
            "sameness_difference_criteria",
            "authority_boundary",
            "claim_boundary",
        ],
        "forbidden_inferences": [
            "do_not_infer_loop_regime_from_vs0_phase_naming",
            "do_not_infer_loop_regime_from_a_to_f_chain_structure",
        ],
    },
    {
        "component_id": "C02",
        "component_name": "TYPED_STATE_OBJECT_CONTRACT",
        "required_for_loop_stage": "L1_STATE_INTAKE",
        "expected_function": (
            "define the required starting typed state object for controlled loop "
            "execution"
        ),
        "required_fields": [
            "state_id",
            "source_references",
            "authority_state",
            "loop_position",
            "available_move_references",
            "radius_state",
            "prior_receipts",
            "halt_state",
            "forbidden_effects",
        ],
        "forbidden_inferences": [
            "do_not_treat_vs0_closure_as_controlled_loop_state_without_explicit_state_contract"
        ],
    },
    {
        "component_id": "C03",
        "component_name": "EXPLICIT_MOVE_SPACE_CONTRACT",
        "required_for_loop_stage": "L2_MOVE_SPACE_ADMISSION",
        "expected_function": (
            "declare the explicit set of moves a controlled loop may consider"
        ),
        "required_fields": [
            "move_ids",
            "move_kinds",
            "input_shapes",
            "output_shapes",
            "authority_requirements",
            "radius_costs",
            "receipt_obligations",
            "halt_conditions",
            "forbidden_effects",
            "source_freshness_rules",
        ],
        "forbidden_inferences": [
            "do_not_infer_move_space_from_a_to_f_specimen",
            "do_not_infer_moves_from_file_names",
            "do_not_infer_runner_authority",
        ],
    },
    {
        "component_id": "C04",
        "component_name": "MOVE_SELECTOR_CONTRACT",
        "required_for_loop_stage": "L3_MOVE_SELECTION",
        "expected_function": (
            "define a bounded selector rule for choosing one admitted move"
        ),
        "required_fields": [
            "selection_rule",
            "tie_break_rule",
            "authority_check",
            "radius_check",
            "source_check",
            "halt_check",
            "determinism_or_seed_witness",
        ],
        "forbidden_inferences": [
            "do_not_treat_next_likely_thing_as_selector",
            "do_not_select_by_vibes",
            "do_not_select_by_newest_file",
        ],
    },
    {
        "component_id": "C05",
        "component_name": "MOVE_APPLICATOR_CONTRACT",
        "required_for_loop_stage": "L4_MOVE_APPLICATION_CONTRACT",
        "expected_function": "map state plus admitted move to output or typed stop",
        "required_fields": [
            "input_object_shape",
            "move_object_shape",
            "precondition_checks",
            "state_transition_rule",
            "output_shape",
            "failure_behavior",
            "receipt_obligation",
            "no_mutation_boundary",
        ],
        "forbidden_inferences": [
            "do_not_treat_existing_build_scripts_as_generic_applicator_unless_explicitly_contracted"
        ],
    },
    {
        "component_id": "C06",
        "component_name": "AUTHORITY_POLICY",
        "required_for_loop_stage": "L0_L3_L4_L11",
        "expected_function": (
            "determine whether a move or loop transition is authorized"
        ),
        "required_fields": [
            "authority_source",
            "authority_state_vocabulary",
            "authorized_action_scope",
            "forbidden_action_scope",
            "human_decision_boundary",
            "promotion_boundary",
            "authority_drift_stops",
        ],
        "forbidden_inferences": [
            "do_not_treat_boundary_fragments_as_loop_ready_authority_policy",
            "do_not_consume_human_authority_without_decision_receipt",
        ],
    },
    {
        "component_id": "C07",
        "component_name": "RADIUS_BUDGET_POLICY",
        "required_for_loop_stage": "L3_L4_L11",
        "expected_function": (
            "define reusable radius/budget accounting for controlled loop execution"
        ),
        "required_fields": [
            "radius_before",
            "radius_cost",
            "radius_consumed",
            "radius_after",
            "exhaustion_rule",
            "renewal_rule",
            "budget_overflow_stop",
        ],
        "forbidden_inferences": [
            "do_not_generalize_vs0_radius_behavior_without_explicit_contract"
        ],
    },
    {
        "component_id": "C08",
        "component_name": "HALT_POLICY",
        "required_for_loop_stage": "L4_L11",
        "expected_function": "define explicit halt policy for controlled loop execution",
        "required_fields": [
            "typed_halt_codes",
            "hard_stops",
            "soft_stops",
            "escalation_stops",
            "missing_object_stops",
            "authority_stops",
            "radius_stops",
            "ambiguous_stop_handling",
            "next_lawful_surface_rule",
        ],
        "forbidden_inferences": [
            "do_not_treat_existing_halt_vocabulary_as_loop_ready_without_explicit_contract"
        ],
    },
    {
        "component_id": "C09",
        "component_name": "RECEIPT_OBLIGATION_CONTRACT",
        "required_for_loop_stage": "L5_RECEIPT_EMISSION",
        "expected_function": "define receipt obligations for every attempted loop step",
        "required_fields": [
            "attempted_move",
            "source_state",
            "authority_basis",
            "radius_before",
            "radius_consumed",
            "radius_after",
            "preconditions_checked",
            "output_or_stop",
            "forbidden_effects_checked",
            "next_lawful_surface",
            "self_repair_flag",
        ],
        "forbidden_inferences": [
            "do_not_treat_vs0_receipts_as_reusable_loop_receipt_contract_without_explicit_contract"
        ],
    },
    {
        "component_id": "C10",
        "component_name": "SOURCE_IDENTITY_FRESHNESS_POLICY",
        "required_for_loop_stage": "L0_L1_L2_L3_L4_L5",
        "expected_function": (
            "define trusted source identity, hashes, statuses, source roles, and "
            "freshness rules"
        ),
        "required_fields": [
            "explicit_paths",
            "hashes_or_commit_identity",
            "source_status",
            "source_role",
            "allowed_source_resolver",
            "forbidden_latest_file_resolution",
            "forbidden_mtime_resolution",
            "stale_source_stop",
        ],
        "forbidden_inferences": [
            "do_not_use_latest_file_selection",
            "do_not_use_mtime_selection",
            "do_not_use_baseline_share_as_source_authority",
        ],
    },
    {
        "component_id": "C11",
        "component_name": "MICRO_SWEEP_BOUNDS_CONTRACT",
        "required_for_loop_stage": "L6_MICRO_SWEEP_BOUNDS_CONTRACT",
        "expected_function": (
            "define bounded micro-sweeps over declared variations if later authorized"
        ),
        "required_fields": [
            "sweep_purpose",
            "variation_set",
            "max_cases",
            "max_steps",
            "allowed_moves",
            "radius_budget",
            "aggregation_rule",
            "forbidden_inference_boundary",
        ],
        "forbidden_inferences": [
            "do_not_treat_negative_probes_as_micro_sweeps_without_explicit_contract",
            "do_not_authorize_micro_sweeps_from_inventory",
        ],
    },
    {
        "component_id": "C12",
        "component_name": "PRESSURE_READOUT_CONTRACT",
        "required_for_loop_stage": "L7_PRESSURE_READOUT",
        "expected_function": (
            "define how pressure is read from execution or halted execution"
        ),
        "required_fields": [
            "held_signal",
            "failed_signal",
            "stopped_signal",
            "missing_object",
            "missing_field",
            "boundary_hit",
            "ambiguity",
            "burden",
            "stale_source",
            "next_surface_exposed",
        ],
        "forbidden_inferences": [
            "do_not_treat_evidence_yield_as_complete_loop_pressure_readout_without_explicit_contract"
        ],
    },
    {
        "component_id": "C13",
        "component_name": "PRESSURE_CLASSIFICATION_VOCABULARY",
        "required_for_loop_stage": "L8_PRESSURE_CLASSIFICATION",
        "expected_function": "provide typed vocabulary for classifying pressure",
        "required_fields": [
            "classification_vocabulary",
            "classification_basis",
            "source_reference",
            "next_surface",
        ],
        "forbidden_inferences": [
            "do_not_treat_vocabulary_declaration_as_operational_classifier"
        ],
    },
    {
        "component_id": "C14",
        "component_name": "LOCAL_REVISION_SURFACE_CONTRACT",
        "required_for_loop_stage": "L9_LOCAL_REVISION_SURFACE",
        "expected_function": "define lawful surface where local revisions may be proposed",
        "required_fields": [
            "revision_target_type",
            "pressure_source",
            "proposal_only_boundary",
            "authority_requirement",
            "validation_admissibility_requirement",
            "apply_boundary",
            "receipt_obligation",
        ],
        "forbidden_inferences": [
            "pressure_does_not_self_authorize_revision",
            "do_not_apply_revision_from_inventory",
        ],
    },
    {
        "component_id": "C15",
        "component_name": "BOUNDED_PORTABILITY_MAP_CONTRACT",
        "required_for_loop_stage": "L10_BOUNDED_PORTABILITY_MAPPING",
        "expected_function": (
            "record where a loop shape carries, fails, adapts, or remains untested"
        ),
        "required_fields": [
            "source_case",
            "target_case",
            "declared_transport_or_adaptation",
            "stable_fields",
            "changed_fields",
            "failed_fields",
            "revision_required",
            "untested_boundary",
            "claim_boundary",
            "receipt_references",
        ],
        "forbidden_inferences": [
            "do_not_call_portability_generalization",
            "do_not_infer_portability_from_vs0",
        ],
    },
    {
        "component_id": "C16",
        "component_name": "REPLAY_AUDIT_CONTRACT",
        "required_for_loop_stage": "L5_L11",
        "expected_function": "verify loop steps after the fact through replay or audit",
        "required_fields": [
            "state_snapshot",
            "move_receipt",
            "source_hashes",
            "result_hash",
            "replay_boundary",
            "audit_pass_fail_vocabulary",
            "mutation_detection",
        ],
        "forbidden_inferences": [
            "do_not_infer_replay_contract_from_source_hash_presence_only"
        ],
    },
    {
        "component_id": "C17",
        "component_name": "FORBIDDEN_EFFECT_GUARD",
        "required_for_loop_stage": "ALL_STAGES",
        "expected_function": "guard against forbidden semantic effects",
        "required_fields": [
            "runner_authority_created_guard",
            "runner_readiness_claimed_guard",
            "active_registry_created_guard",
            "trace_generalized_guard",
            "radius_renewed_without_authority_guard",
            "move_space_expanded_without_authority_guard",
            "source_authority_replaced_guard",
            "next_phase_auto_selected_guard",
            "optimization_claimed_guard",
            "global_portability_claimed_guard",
            "local_revision_applied_without_authority_guard",
            "micro_sweep_executed_without_authority_guard",
        ],
        "forbidden_inferences": [
            "do_not_treat_local_vs0_boundary_language_as_reusable_guard_contract_without_explicit_contract"
        ],
    },
    {
        "component_id": "C18",
        "component_name": "EVIDENCE_YIELD_REPORT_HOOK",
        "required_for_loop_stage": "L5_L7_L8_L11",
        "expected_function": "report Confirmation Yield and Diagnostic Yield from loop events",
        "required_fields": [
            "successful_execution_events",
            "halted_stopped_execution_events",
            "decision_relevant_evidence_checks",
            "non_optimization_boundary",
            "next_lawful_surface",
        ],
        "forbidden_inferences": [
            "do_not_treat_vs0_5_as_loop_level_hook_without_explicit_contract"
        ],
    },
    {
        "component_id": "C19",
        "component_name": "HUMAN_ESCALATION_DECISION_BOUNDARY",
        "required_for_loop_stage": "L0_L3_L4_L9_L11",
        "expected_function": (
            "define when the loop must escalate to a human decision surface"
        ),
        "required_fields": [
            "authority_required",
            "promotion_required",
            "unclear_boundary",
            "forbidden_effect_risk",
            "schema_missing",
            "next_phase_decision",
            "revision_apply_decision",
            "radius_renewal_decision",
            "runner_authority_decision",
            "micro_sweep_execution_decision",
        ],
        "forbidden_inferences": [
            "machine_may_expose_decision_surface_candidate_but_not_consume_human_authority_without_decision_receipt"
        ],
    },
    {
        "component_id": "C20",
        "component_name": "CONVERGENCE_CRITERION_CONTRACT",
        "required_for_loop_stage": "L11_REPEAT_OR_HALT_DECISION",
        "expected_function": (
            "define local terminal condition, repeat condition, non-progress "
            "condition, and halt behavior for convergence"
        ),
        "required_fields": [
            "local_terminal_condition",
            "allowed_repeat_condition",
            "non_progress_condition",
            "oscillation_or_repeated_state_guard",
            "max_cycle_or_radius_boundary",
            "evidence_required_to_continue",
            "typed_halt_when_not_met",
        ],
        "forbidden_inferences": [
            "do_not_infer_convergence_from_repeated_movement",
            "do_not_infer_convergence_from_successful_vs0_closure",
            "do_not_treat_optimization_progress_as_convergence_without_explicit_metric_contract",
        ],
    },
]

CANDIDATE_EVIDENCE_PATHS = {
    "C01_SCOPE_REGIME_DECLARATION_CONTRACT": [],
    "C02_TYPED_STATE_OBJECT_CONTRACT": [],
    "C03_EXPLICIT_MOVE_SPACE_CONTRACT": [],
    "C04_MOVE_SELECTOR_CONTRACT": [],
    "C05_MOVE_APPLICATOR_CONTRACT": [],
    "C06_AUTHORITY_POLICY": [
        DIRECTION_JSON,
        SOURCE_INTAKE_JSON,
        SOURCE_CONTRACT_JSON,
    ],
    "C07_RADIUS_BUDGET_POLICY": [SOURCE_CONTRACT_JSON],
    "C08_HALT_POLICY": [SOURCE_CONTRACT_JSON, VS0_NEGATIVE_PROBE_JSON],
    "C09_RECEIPT_OBLIGATION_CONTRACT": [
        SOURCE_CONTRACT_JSON,
        DIRECTION_JSON,
        SOURCE_INTAKE_JSON,
    ],
    "C10_SOURCE_IDENTITY_FRESHNESS_POLICY": [
        SOURCE_CONTRACT_JSON,
        SOURCE_INTAKE_JSON,
        DIRECTION_JSON,
    ],
    "C11_MICRO_SWEEP_BOUNDS_CONTRACT": [SOURCE_CONTRACT_JSON],
    "C12_PRESSURE_READOUT_CONTRACT": [
        SOURCE_CONTRACT_JSON,
        VS0_EVIDENCE_YIELD_JSON,
        VS0_NEGATIVE_PROBE_JSON,
    ],
    "C13_PRESSURE_CLASSIFICATION_VOCABULARY": [SOURCE_CONTRACT_JSON],
    "C14_LOCAL_REVISION_SURFACE_CONTRACT": [SOURCE_CONTRACT_JSON],
    "C15_BOUNDED_PORTABILITY_MAP_CONTRACT": [SOURCE_CONTRACT_JSON],
    "C16_REPLAY_AUDIT_CONTRACT": [],
    "C17_FORBIDDEN_EFFECT_GUARD": [
        SOURCE_CONTRACT_JSON,
        SOURCE_INTAKE_JSON,
        DIRECTION_JSON,
        VS0_CLOSURE_JSON,
    ],
    "C18_EVIDENCE_YIELD_REPORT_HOOK": [
        SOURCE_CONTRACT_JSON,
        VS0_EVIDENCE_YIELD_JSON,
    ],
    "C19_HUMAN_ESCALATION_DECISION_BOUNDARY": [
        DIRECTION_JSON,
        SOURCE_INTAKE_JSON,
        SOURCE_CONTRACT_JSON,
    ],
    "C20_CONVERGENCE_CRITERION_CONTRACT": [SOURCE_CONTRACT_JSON],
}

CLASSIFICATION_PLAN = {
    "C01_SCOPE_REGIME_DECLARATION_CONTRACT": {
        "status": "MISSING",
        "blockers": ["SCHEMA_REQUIRED", "CONTRACT_REVISION_REQUIRED"],
        "notes": ["No declared candidate evidence path exists beyond VS1.2 declaration evidence."],
    },
    "C02_TYPED_STATE_OBJECT_CONTRACT": {
        "status": "MISSING",
        "blockers": ["SCHEMA_REQUIRED", "CONTRACT_REVISION_REQUIRED"],
        "notes": ["No declared MCCL typed-state contract is present in the evidence map."],
    },
    "C03_EXPLICIT_MOVE_SPACE_CONTRACT": {
        "status": "MISSING",
        "blockers": ["AUTHORITY_REQUIRED", "SCHEMA_REQUIRED", "CONTRACT_REVISION_REQUIRED"],
        "notes": ["No declared move-space artifact is present, and move-space may not be inferred from VS0 files."],
    },
    "C04_MOVE_SELECTOR_CONTRACT": {
        "status": "MISSING",
        "blockers": ["SCHEMA_REQUIRED", "CONTRACT_REVISION_REQUIRED"],
        "notes": ["No declared selector contract exists."],
    },
    "C05_MOVE_APPLICATOR_CONTRACT": {
        "status": "MISSING",
        "blockers": ["AUTHORITY_REQUIRED", "SCHEMA_REQUIRED", "CONTRACT_REVISION_REQUIRED"],
        "notes": ["No declared move applicator contract exists."],
    },
    "C06_AUTHORITY_POLICY": {
        "status": "PRESENT_PARTIAL",
        "blockers": ["AUTHORITY_REQUIRED", "HUMAN_DECISION_REQUIRED", "CONTRACT_REVISION_REQUIRED"],
        "notes": ["Declared paths contain authority boundary and non-execution material, but no MCCL-specific authority policy."],
    },
    "C07_RADIUS_BUDGET_POLICY": {
        "status": "PRESENT_CANDIDATE_ONLY",
        "blockers": ["CONTRACT_REVISION_REQUIRED"],
        "notes": ["VS1.2 declares radius budget policy as required, but no independent radius policy artifact exists."],
    },
    "C08_HALT_POLICY": {
        "status": "PRESENT_PARTIAL",
        "blockers": ["CONTRACT_REVISION_REQUIRED"],
        "notes": ["Declared negative-probe evidence contains typed stop precedent, but no MCCL halt policy contract exists."],
    },
    "C09_RECEIPT_OBLIGATION_CONTRACT": {
        "status": "PRESENT_PARTIAL",
        "blockers": ["CONTRACT_REVISION_REQUIRED"],
        "notes": ["Declared source artifacts emit receipts and obligations, but no reusable MCCL loop-step receipt contract exists."],
    },
    "C10_SOURCE_IDENTITY_FRESHNESS_POLICY": {
        "status": "PRESENT_PARTIAL",
        "blockers": ["SOURCE_STATUS_REQUIRED", "CONTRACT_REVISION_REQUIRED"],
        "notes": ["Declared artifacts include paths, commits, and hashes, but no complete freshness policy contract exists."],
    },
    "C11_MICRO_SWEEP_BOUNDS_CONTRACT": {
        "status": "PRESENT_CANDIDATE_ONLY",
        "blockers": ["AUTHORITY_REQUIRED", "CONTRACT_REVISION_REQUIRED"],
        "notes": ["VS1.2 declares the bounds contract but does not authorize or operationalize micro-sweeps."],
    },
    "C12_PRESSURE_READOUT_CONTRACT": {
        "status": "PRESENT_PARTIAL",
        "blockers": ["CONTRACT_REVISION_REQUIRED"],
        "notes": ["VS0 evidence yield and negative probes provide readout precedent, not a complete MCCL pressure contract."],
    },
    "C13_PRESSURE_CLASSIFICATION_VOCABULARY": {
        "status": "PRESENT_CANDIDATE_ONLY",
        "blockers": ["CONTRACT_REVISION_REQUIRED"],
        "notes": ["VS1.2 declares vocabulary only; it is not an operational classifier."],
    },
    "C14_LOCAL_REVISION_SURFACE_CONTRACT": {
        "status": "PRESENT_CANDIDATE_ONLY",
        "blockers": ["AUTHORITY_REQUIRED", "CONTRACT_REVISION_REQUIRED"],
        "notes": ["VS1.2 declares a local revision surface shape but does not authorize revision."],
    },
    "C15_BOUNDED_PORTABILITY_MAP_CONTRACT": {
        "status": "PRESENT_CANDIDATE_ONLY",
        "blockers": ["CONTRACT_REVISION_REQUIRED"],
        "notes": ["VS1.2 declares bounded portability mapping only; portability is not demonstrated."],
    },
    "C16_REPLAY_AUDIT_CONTRACT": {
        "status": "MISSING",
        "blockers": ["SCHEMA_REQUIRED", "CONTRACT_REVISION_REQUIRED"],
        "notes": ["No declared replay audit contract path exists."],
    },
    "C17_FORBIDDEN_EFFECT_GUARD": {
        "status": "PRESENT_BOUNDARY_ONLY",
        "blockers": ["CONTRACT_REVISION_REQUIRED"],
        "notes": ["Declared paths contain boundary and prohibition language, not an operational guard contract."],
    },
    "C18_EVIDENCE_YIELD_REPORT_HOOK": {
        "status": "PRESENT_PARTIAL",
        "blockers": ["CONTRACT_REVISION_REQUIRED"],
        "notes": ["VS0.5 provides evidence-yield precedent, but no MCCL-level hook contract exists."],
    },
    "C19_HUMAN_ESCALATION_DECISION_BOUNDARY": {
        "status": "PRESENT_BOUNDARY_ONLY",
        "blockers": ["AUTHORITY_REQUIRED", "HUMAN_DECISION_REQUIRED", "CONTRACT_REVISION_REQUIRED"],
        "notes": ["Declared paths preserve human decision boundaries, but no operational escalation contract exists."],
    },
    "C20_CONVERGENCE_CRITERION_CONTRACT": {
        "status": "PRESENT_CANDIDATE_ONLY",
        "blockers": ["SCHEMA_REQUIRED", "CONTRACT_REVISION_REQUIRED"],
        "notes": ["VS1.2 declares convergence criterion fields but supplies no domain-specific criterion."],
    },
}

FORBIDDEN_ARTIFACTS = [
    "docs/matrixlabs/runner",
    "docs/matrixlabs/runtime",
    "docs/matrixlabs/move_space",
    "docs/matrixlabs/micro_sweeps",
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_readiness_audit_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_readiness_audit_v0.md",
    "docs/matrixlabs/phase_vs1/phase_vs1_controlled_loop_readiness_certificate_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_component_repair_plan_v0.json",
    "docs/matrixlabs/phase_vs1/phase_vs1_candidate_promotion_v0.json",
]


class InventoryFailure(RuntimeError):
    def __init__(
        self,
        code: str,
        *,
        source: str = "NONE",
        component: str = "NONE",
        field: str = "NONE",
        expected: object = "NONE",
        actual: object = "NONE",
        next_surface: str = "REPAIR_VS1_3_PRECONDITION_INVENTORY_INPUT",
    ) -> None:
        super().__init__(code)
        self.code = code
        self.source = source
        self.component = component
        self.field = field
        self.expected = expected
        self.actual = actual
        self.next_surface = next_surface


def fail(
    code: str,
    *,
    source: str = "NONE",
    component: str = "NONE",
    field: str = "NONE",
    expected: object = "NONE",
    actual: object = "NONE",
    next_surface: str = "REPAIR_VS1_3_PRECONDITION_INVENTORY_INPUT",
) -> None:
    raise InventoryFailure(
        code,
        source=source,
        component=component,
        field=field,
        expected=expected,
        actual=actual,
        next_surface=next_surface,
    )


def run_git(root: Path, args: list[str]) -> str:
    proc = subprocess.run(
        ["git", *args],
        cwd=root,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(
            "STOP_VS1_3_SOURCE_IDENTITY_UNVERIFIED",
            source="git",
            field="git_command",
            expected="success",
            actual=proc.stderr.strip(),
        )
    return proc.stdout.rstrip()


def detect_repo_root(start: Path) -> Path:
    proc = subprocess.run(
        ["git", "rev-parse", "--show-toplevel"],
        cwd=start,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode != 0:
        fail(
            "STOP_VS1_3_SOURCE_IDENTITY_UNVERIFIED",
            source="repo",
            field="repo_root",
            expected="git repository",
            actual=proc.stderr.strip(),
        )
    return Path(proc.stdout.strip()).resolve()


def status_path(line: str) -> str:
    path = line[3:].strip()
    if " -> " in path:
        path = path.split(" -> ", 1)[1].strip()
    return path


def validate_dirty_scope(root: Path) -> None:
    allowed_exact = {
        SCRIPT,
        "scripts/build_baseline_share_v0.py",
        OUTPUT_JSON,
        OUTPUT_MD,
    }
    allowed_prefixes = ("baseline_share/", "discussion_packets/")
    status = run_git(root, ["status", "--short", "--untracked-files=all"])
    for line in status.splitlines():
        path = status_path(line)
        if path in allowed_exact or any(path.startswith(p) for p in allowed_prefixes):
            continue
        if path in {SOURCE_CONTRACT_JSON, SOURCE_CONTRACT_MD}:
            fail(
                "STOP_VS1_3_VS1_2_CONTRACT_MUTATED",
                source=path,
                field="dirty_scope",
                expected="unchanged VS1.2 contract",
                actual=line,
            )
        if path in {SOURCE_INTAKE_JSON, SOURCE_INTAKE_MD}:
            fail(
                "STOP_VS1_3_VS1_1_INTAKE_MUTATED",
                source=path,
                field="dirty_scope",
                expected="unchanged VS1.1 intake",
                actual=line,
            )
        if path in {DIRECTION_JSON, DIRECTION_MD}:
            fail(
                "STOP_VS1_3_DIRECTION_RECEIPT_MUTATED",
                source=path,
                field="dirty_scope",
                expected="unchanged direction receipt",
                actual=line,
            )
        if path.startswith(f"{VS0_ROOT}/"):
            fail(
                "STOP_VS1_3_VS0_SOURCE_MUTATED",
                source=path,
                field="dirty_scope",
                expected="unchanged VS0 source artifacts",
                actual=line,
            )
        fail(
            "STOP_VS1_3_UNCOMMITTED_RESIDUE_USED",
            source=path,
            field="dirty_scope",
            expected="only VS1.3 outputs, baseline_share, or discussion_packets",
            actual=line,
        )


def require_head(root: Path) -> None:
    head = run_git(root, ["rev-parse", "HEAD"])
    if head != EXPECTED_HEAD:
        fail(
            "STOP_VS1_3_SOURCE_IDENTITY_UNVERIFIED",
            source="HEAD",
            field="commit_sha",
            expected=EXPECTED_HEAD,
            actual=head,
        )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(root: Path, rel_path: str) -> dict[str, Any]:
    path = root / rel_path
    if not path.is_file():
        fail(
            "STOP_VS1_3_CONTROLLED_LOOP_CONTRACT_NOT_PASS",
            source=rel_path,
            field="file_presence",
            expected=True,
            actual=False,
        )
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as exc:
        fail(
            "STOP_VS1_3_SOURCE_IDENTITY_UNVERIFIED",
            source=rel_path,
            field="valid_json",
            expected=True,
            actual=str(exc),
        )
    if not isinstance(value, dict):
        fail(
            "STOP_VS1_3_SOURCE_IDENTITY_UNVERIFIED",
            source=rel_path,
            field="json_object",
            expected=True,
            actual=type(value).__name__,
        )
    return value


def require_file(root: Path, rel_path: str) -> None:
    if not (root / rel_path).is_file():
        fail(
            "STOP_VS1_3_SOURCE_IDENTITY_UNVERIFIED",
            source=rel_path,
            field="file_presence",
            expected=True,
            actual=False,
        )


def get_value(obj: dict[str, Any], path: str, default: Any = None) -> Any:
    cur: Any = obj
    for part in path.split("."):
        if not isinstance(cur, dict):
            return default
        cur = cur.get(part, default)
    return cur


def source_paths(root: Path) -> list[str]:
    paths = [
        SOURCE_CONTRACT_JSON,
        SOURCE_CONTRACT_MD,
        SOURCE_INTAKE_JSON,
        SOURCE_INTAKE_MD,
        DIRECTION_JSON,
        DIRECTION_MD,
    ]
    vs0_root = root / VS0_ROOT
    if vs0_root.is_dir():
        for path in sorted(vs0_root.rglob("*")):
            if path.is_file():
                paths.append(path.relative_to(root).as_posix())
    return sorted(set(paths))


def capture_source_hashes(root: Path) -> dict[str, str]:
    hashes: dict[str, str] = {}
    for rel_path in source_paths(root):
        path = root / rel_path
        if not path.is_file():
            fail(
                "STOP_VS1_3_SOURCE_IDENTITY_UNVERIFIED",
                source=rel_path,
                field="source_file",
                expected="present",
                actual="missing",
            )
        hashes[rel_path] = sha256(path)
    return hashes


def validate_source_preservation(
    before: dict[str, str],
    after: dict[str, str],
) -> None:
    if before == after:
        return
    changed = sorted(
        path
        for path in set(before) | set(after)
        if before.get(path) != after.get(path)
    )
    first = changed[0] if changed else "unknown"
    if first in {SOURCE_CONTRACT_JSON, SOURCE_CONTRACT_MD}:
        code = "STOP_VS1_3_VS1_2_CONTRACT_MUTATED"
    elif first in {SOURCE_INTAKE_JSON, SOURCE_INTAKE_MD}:
        code = "STOP_VS1_3_VS1_1_INTAKE_MUTATED"
    elif first in {DIRECTION_JSON, DIRECTION_MD}:
        code = "STOP_VS1_3_DIRECTION_RECEIPT_MUTATED"
    elif first.startswith(f"{VS0_ROOT}/"):
        code = "STOP_VS1_3_VS0_SOURCE_MUTATED"
    else:
        code = "STOP_VS1_3_SOURCE_IDENTITY_UNVERIFIED"
    fail(
        code,
        source=first,
        field="source_hash",
        expected=before.get(first),
        actual=after.get(first),
    )


def validate_source_contract(contract: dict[str, Any]) -> None:
    if contract.get("artifact_id") != CONTRACT_ARTIFACT_ID:
        fail(
            "STOP_VS1_3_CONTROLLED_LOOP_CONTRACT_NOT_PASS",
            source=SOURCE_CONTRACT_JSON,
            field="artifact_id",
            expected=CONTRACT_ARTIFACT_ID,
            actual=contract.get("artifact_id"),
        )
    if contract.get("contract_verdict") != CONTRACT_STATUS:
        fail(
            "STOP_VS1_3_CONTROLLED_LOOP_CONTRACT_NOT_PASS",
            source=SOURCE_CONTRACT_JSON,
            field="contract_verdict",
            expected=CONTRACT_STATUS,
            actual=contract.get("contract_verdict"),
        )
    if get_value(contract, "terminal_transition.transition") != CONTRACT_TRANSITION:
        fail(
            "STOP_VS1_3_CONTROLLED_LOOP_CONTRACT_NOT_PASS",
            source=SOURCE_CONTRACT_JSON,
            field="terminal_transition.transition",
            expected=CONTRACT_TRANSITION,
            actual=get_value(contract, "terminal_transition.transition"),
        )
    components = contract.get("required_components")
    if not isinstance(components, list):
        fail(
            "STOP_VS1_3_REQUIRED_COMPONENT_LIST_MISSING",
            source=SOURCE_CONTRACT_JSON,
            field="required_components",
            expected=EXPECTED_COMPONENTS,
            actual=components,
        )
    if components != EXPECTED_COMPONENTS:
        fail(
            "STOP_VS1_3_REQUIRED_COMPONENT_SET_MISMATCH",
            source=SOURCE_CONTRACT_JSON,
            field="required_components",
            expected=EXPECTED_COMPONENTS,
            actual=components,
        )


def ensure_no_forbidden_artifacts(root: Path) -> None:
    for rel_path in FORBIDDEN_ARTIFACTS:
        if (root / rel_path).exists():
            fail(
                "STOP_VS1_3_READINESS_VERDICT_ISSUED",
                source=rel_path,
                field="forbidden_artifact",
                expected="absent",
                actual="present",
            )


def markdown_contains_vs1_3_overclaim(md: str) -> list[str]:
    hits: list[str] = []
    allowed_patterns = [
        r"\bcontrolled loop ready\s*[:=]\s*false\b",
        r"\bcontrolled loop authorized\s*[:=]\s*false\b",
        r"\bcontrolled loop operational\s*[:=]\s*false\b",
        r"\brunner exists\s*[:=]\s*false\b",
        r"\brunner readiness exists\s*[:=]\s*false\b",
        r"\brunner authority exists\s*[:=]\s*false\b",
        r"\bmicro-sweeps authorized\s*[:=]\s*false\b",
        r"\blocal revision authorized\s*[:=]\s*false\b",
        r"\bportability demonstrated\s*[:=]\s*false\b",
        r"\bmissing components should be built\s*[:=]\s*false\b",
        r"\bcandidate components should be promoted\s*[:=]\s*false\b",
        r"\bpartial components are sufficient\s*[:=]\s*false\b",
        r"\bboundary-only components are operational\s*[:=]\s*false\b",
        r"\bvs1\.4 executed\s*[:=]\s*false\b",
        r"\breadiness audit performed\s*[:=]\s*false\b",
        r"\bloop execution authorized\s*[:=]\s*false\b",
        r"\brepairs allowed\s*[:=]\s*false\b",
        r"\bpromotions allowed\s*[:=]\s*false\b",
        r"\bmissing components ranked\s*[:=]\s*false\b",
        r"\bnext component to build selected\s*[:=]\s*false\b",
        r"\brepair plan created\s*[:=]\s*false\b",
        r"\bimplementation prompt created\s*[:=]\s*false\b",
        r"\bcandidate promoted\s*[:=]\s*false\b",
        r"\bschema promotion requested\s*[:=]\s*false\b",
        r"\bhuman decision consumed\s*[:=]\s*false\b",
        r"\ball components present required for pass\s*[:=]\s*false\b",
        r"\bmissing components allowed in pass\s*[:=]\s*true\b",
        r"\bmissing component is failure\s*[:=]\s*false\b",
        r"\bdoes not judge whether the loop is ready\b",
        r"\bdoes not .*repair gaps\b",
        r"\bdoes not .*rank missing objects\b",
        r"\bdoes not .*promote candidates\b",
        r"\bdoes not .*authorize execution\b",
        r"\bdoes not .*create a runner\b",
        r"\bdoes not .*run micro-sweeps\b",
        r"\bdoes not .*execute vs1\.4\b",
        r"\binventories .* preconditions\b",
    ]
    forbidden_patterns = {
        "controlled loop ready": r"\bcontrolled loop ready\b",
        "readiness certified": r"\breadiness certified\b",
        "readiness audit passed": r"\breadiness audit passed\b",
        "runner ready": r"\brunner ready\b",
        "runner exists": r"\brunner exists\b",
        "runner authority exists": r"\brunner authority exists\b",
        "runtime ready": r"\bruntime ready\b",
        "move-space exists": r"\bmove-space exists\b",
        "micro-sweeps authorized": r"\bmicro-sweeps authorized\b",
        "local revision authorized": r"\blocal revision authorized\b",
        "portability demonstrated": r"\bportability demonstrated\b",
        "VS0 generalized": r"\bvs0 generalized\b",
        "missing components should be built": r"\bmissing components should be built\b",
        "candidate promoted": r"\bcandidate promoted\b",
        "component repaired": r"\bcomponent repaired\b",
        "all components present": r"\ball components present\b",
        "all components verified": r"\ball components verified\b",
        "next component selected": r"\bnext component selected\b",
        "repair plan created": r"\brepair plan created\b",
        "VS1.4 executed": r"\bvs1\.4 executed\b",
        "loop execution authorized": r"\bloop execution authorized\b",
    }
    for lineno, raw_line in enumerate(md.splitlines(), start=1):
        line = raw_line.strip().lower()
        if not line:
            continue
        if any(re.search(pattern, line) for pattern in allowed_patterns):
            continue
        for label, pattern in forbidden_patterns.items():
            if re.search(pattern, line):
                hits.append(f"line {lineno}: {label}: {raw_line}")
    return hits


def source_identity_status(candidate_paths: list[str], observed_paths: list[str]) -> str:
    if not candidate_paths:
        return "NO_CANDIDATE_PATHS_DECLARED"
    if len(candidate_paths) == len(observed_paths):
        return "DECLARED_CANDIDATE_PATHS_PRESENT"
    if observed_paths:
        return "DECLARED_CANDIDATE_PATHS_PARTIAL"
    return "DECLARED_CANDIDATE_PATHS_ABSENT"


def build_component_records(root: Path) -> tuple[dict[str, str], list[dict[str, Any]]]:
    table: dict[str, str] = {}
    records: list[dict[str, Any]] = []
    for meta in COMPONENT_METADATA:
        full_key = f"{meta['component_id']}_{meta['component_name']}"
        if full_key not in EXPECTED_COMPONENTS:
            fail(
                "STOP_VS1_3_COMPONENT_ID_MISMATCH",
                component=full_key,
                field="component_id",
                expected=EXPECTED_COMPONENTS,
                actual=full_key,
            )
        plan = CLASSIFICATION_PLAN[full_key]
        status = plan["status"]
        blockers = plan["blockers"]
        if status not in VALID_STATUSES or status in PLACEHOLDER_VALUES:
            fail(
                "STOP_VS1_3_COMPONENT_STATUS_INVALID",
                component=full_key,
                field="primary_inventory_status",
                expected=sorted(VALID_STATUSES),
                actual=status,
            )
        if not blockers:
            fail(
                "STOP_VS1_3_BLOCKER_FLAGS_MISSING",
                component=full_key,
                field="blocker_flags",
                expected="non-empty list",
                actual=blockers,
            )
        for blocker in blockers:
            if blocker not in VALID_BLOCKERS:
                fail(
                    "STOP_VS1_3_BLOCKER_FLAGS_INVALID",
                    component=full_key,
                    field="blocker_flags",
                    expected=sorted(VALID_BLOCKERS),
                    actual=blocker,
                )
        if "NONE" in blockers and len(blockers) > 1:
            fail(
                "STOP_VS1_3_BLOCKER_FLAGS_INVALID",
                component=full_key,
                field="blocker_flags",
                expected="NONE not mixed with other blockers",
                actual=blockers,
            )

        candidate_paths = CANDIDATE_EVIDENCE_PATHS[full_key]
        observed_paths = [path for path in candidate_paths if (root / path).exists()]
        independent_paths = [
            path for path in observed_paths if path != SOURCE_CONTRACT_JSON
        ]
        declaration_only = not independent_paths
        if status == "PRESENT_VERIFIED" and not independent_paths:
            fail(
                "STOP_VS1_3_COMPONENT_STATUS_INVALID",
                component=full_key,
                field="independent_component_evidence",
                expected="independent artifact for PRESENT_VERIFIED",
                actual=independent_paths,
            )
        table[full_key] = status
        records.append(
            {
                "component_id": meta["component_id"],
                "component_name": meta["component_name"],
                "declared_by": CONTRACT_ARTIFACT_ID,
                "required_for_loop_stage": meta["required_for_loop_stage"],
                "expected_function": meta["expected_function"],
                "candidate_source_paths": candidate_paths,
                "observed_source_paths": observed_paths,
                "source_identity_status": source_identity_status(
                    candidate_paths,
                    observed_paths,
                ),
                "declaration_evidence": {
                    "declared_in_vs1_2_contract": True,
                    "declaration_source_path": SOURCE_CONTRACT_JSON,
                    "declaration_is_component_presence_evidence": False,
                },
                "independent_component_evidence": {
                    "independent_artifact_present": bool(independent_paths),
                    "independent_artifact_paths": independent_paths,
                },
                "primary_inventory_status": status,
                "blocker_flags": blockers,
                "supporting_evidence": [
                    *plan["notes"],
                    (
                        "Observed declared candidate paths: "
                        + (", ".join(observed_paths) if observed_paths else "none")
                    ),
                    (
                        "VS1.2 declaration evidence is recorded but not treated "
                        "as component-presence evidence."
                    ),
                ],
                "missing_fields": (
                    meta["required_fields"]
                    if status in {"MISSING", "PRESENT_CANDIDATE_ONLY", "PRESENT_BOUNDARY_ONLY"}
                    else [
                        field
                        for field in meta["required_fields"]
                        if field not in {
                            "source_reference",
                            "source_references",
                            "source_status",
                        }
                    ]
                ),
                "missing_authority": (
                    "AUTHORITY_REQUIRED" in blockers
                    or "HUMAN_DECISION_REQUIRED" in blockers
                ),
                "missing_schema": "SCHEMA_REQUIRED" in blockers,
                "boundary_notes": [
                    "Declaration evidence does not create authority.",
                    "Inventory status does not authorize readiness, repair, promotion, or execution.",
                    (
                        "No independent component artifact is present."
                        if declaration_only
                        else "Independent declared paths provide precedent or boundary evidence only."
                    ),
                ],
                "forbidden_inferences": meta["forbidden_inferences"],
                "may_feed_vs1_4_readiness_audit_as_evidence": True,
            }
        )
    return table, records


def summarize_statuses(records: list[dict[str, Any]]) -> dict[str, int]:
    counts = {
        "required_components_total": len(records),
        "present_verified": 0,
        "present_partial": 0,
        "present_candidate_only": 0,
        "present_boundary_only": 0,
        "missing": 0,
        "insufficient": 0,
        "source_unverified": 0,
        "out_of_scope": 0,
    }
    for record in records:
        status = record["primary_inventory_status"]
        counts[STATUS_COUNT_KEY[status]] += 1
    return counts


def summarize_blockers(records: list[dict[str, Any]]) -> dict[str, int]:
    counts = {
        "authority_required": 0,
        "promotion_required": 0,
        "schema_required": 0,
        "human_decision_required": 0,
        "source_status_required": 0,
        "contract_revision_required": 0,
        "none": 0,
    }
    for record in records:
        for blocker in record["blocker_flags"]:
            counts[BLOCKER_COUNT_KEY[blocker]] += 1
    return counts


def build_inventory(root: Path) -> dict[str, Any]:
    table, records = build_component_records(root)
    return {
        "schema_version": SCHEMA_VERSION,
        "artifact_id": ARTIFACT_ID,
        "phase_id": PHASE_ID,
        "unit_id": UNIT_ID,
        "unit_role": UNIT_ROLE,
        "source_contract": {
            "artifact_id": CONTRACT_ARTIFACT_ID,
            "path": SOURCE_CONTRACT_JSON,
            "commit_sha": EXPECTED_HEAD,
            "sha256": sha256(root / SOURCE_CONTRACT_JSON),
            "required_status": CONTRACT_STATUS,
            "required_transition": CONTRACT_TRANSITION,
            "source_role": "DECLARED_COMPONENT_LIST",
        },
        "inventory_mode": {
            "declared_components_only": True,
            "additional_requirements_load_bearing": False,
            "directory_scan_authority_allowed": False,
            "declared_path_existence_checks_allowed": True,
            "repo_wide_search_used": False,
            "latest_file_resolution_allowed": False,
            "latest_file_resolution_used": False,
            "mtime_resolution_used": False,
            "baseline_share_as_source_of_truth": False,
            "baseline_share_used_as_source_authority": False,
            "discussion_packets_used_as_source_authority": False,
            "uncommitted_residue_used_as_source_authority": False,
            "chat_memory_used_as_source_authority": False,
            "repairs_allowed": False,
            "promotions_allowed": False,
            "readiness_audit_performed": False,
            "loop_execution_authorized": False,
        },
        "inventory_evidence_map": {
            "evidence_map_declared": True,
            "repo_wide_search_used": False,
            "latest_file_resolution_used": False,
            "mtime_resolution_used": False,
            "baseline_share_used_as_source_authority": False,
            "discussion_packets_used_as_source_authority": False,
            "uncommitted_residue_used_as_source_authority": False,
            "declared_candidate_paths_only": True,
            "declaration_source": {
                "path": SOURCE_CONTRACT_JSON,
                "role": "DECLARATION_EVIDENCE_ONLY",
                "declaration_is_component_presence_evidence": False,
            },
            "candidate_evidence_paths": CANDIDATE_EVIDENCE_PATHS,
        },
        "inventory_pass_semantics": {
            "all_components_classified": True,
            "all_components_present_required_for_pass": False,
            "missing_components_allowed_in_pass": True,
            "partial_components_allowed_in_pass": True,
            "candidate_only_components_allowed_in_pass": True,
            "boundary_only_components_allowed_in_pass": True,
            "unclassified_component_is_failure": True,
            "missing_component_is_failure": False,
        },
        "component_status_table": table,
        "component_records": records,
        "summary_counts": summarize_statuses(records),
        "blocker_flag_summary": summarize_blockers(records),
        "observed_additional_candidate_requirements": [],
        "repair_and_ranking_boundary": {
            "missing_components_ranked": False,
            "next_component_to_build_selected": False,
            "repair_plan_created": False,
            "implementation_prompt_created": False,
            "candidate_promoted": False,
            "schema_promotion_requested": False,
            "human_decision_consumed": False,
        },
        "source_preservation": {
            "vs1_2_contract_mutated_by_vs1_3": False,
            "vs1_1_source_intake_mutated_by_vs1_3": False,
            "post_vs0_direction_decision_receipt_mutated_by_vs1_3": False,
            "vs0_source_artifacts_mutated_by_vs1_3": False,
        },
        "forbidden_inferences_checked": {
            "loop_readiness_inferred": False,
            "component_presence_inferred_from_declaration_only": False,
            "component_sufficiency_inferred_from_partial_presence": False,
            "candidate_authority_inferred": False,
            "boundary_only_component_treated_as_operational": False,
            "missing_component_repaired": False,
            "candidate_promoted": False,
            "loop_execution_authorized": False,
            "micro_sweeps_authorized": False,
            "local_revision_authorized": False,
            "runner_authority_created": False,
            "vs1_4_executed": False,
        },
        "non_claims": {
            "controlled_loop_ready": False,
            "controlled_loop_authorized": False,
            "controlled_loop_operational": False,
            "runner_exists": False,
            "runner_readiness_exists": False,
            "runner_authority_exists": False,
            "micro_sweeps_authorized": False,
            "local_revision_authorized": False,
            "portability_demonstrated": False,
            "missing_components_should_be_built": False,
            "candidate_components_should_be_promoted": False,
            "partial_components_are_sufficient": False,
            "boundary_only_components_are_operational": False,
            "vs1_4_executed": False,
        },
        "evidence_yield": {
            "yield_branch": "CONFIRMATION_YIELD",
            "confirmation_yield_reason": (
                "all VS1.2-declared required components were classified with "
                "source-backed inventory statuses and blocker flags without "
                "readiness, repair, promotion, or execution"
            ),
            "diagnostic_yield_component_records_present": True,
            "diagnostic_yield_available_for_non_present_verified_components": True,
        },
        "inventory_verdict": PASS_VERDICT,
        "terminal_transition": {
            "transition": ARTIFACT_TRANSITION,
            "executes_vs1_4": False,
            "authorizes_loop_execution": False,
            "authorizes_micro_sweeps": False,
            "authorizes_local_revision": False,
        },
        "failures": [],
    }


def build_markdown(inventory: dict[str, Any]) -> str:
    counts = inventory["summary_counts"]
    rows = []
    table = inventory["component_status_table"]
    record_by_key = {
        f"{record['component_id']}_{record['component_name']}": record
        for record in inventory["component_records"]
    }
    for component in EXPECTED_COMPONENTS:
        record = record_by_key[component]
        rows.append(
            "| "
            + " | ".join(
                [
                    component,
                    table[component],
                    ", ".join(record["blocker_flags"]),
                ]
            )
            + " |"
        )
    component_table = "\n".join(
        [
            "| Component | Primary status | Blocker flags |",
            "| --- | --- | --- |",
            *rows,
        ]
    )
    return f"""# Phase VS1.3 controlled loop precondition inventory v0

## Status

{PASS_VERDICT}

## Source contract

- source contract: {CONTRACT_ARTIFACT_ID}
- source contract commit: {EXPECTED_HEAD}
- required source contract status: {CONTRACT_STATUS}
- source role: DECLARED_COMPONENT_LIST

## Inventory mode

- declared components only: true
- additional requirements load-bearing: false
- repo-wide search used: false
- latest-file resolution used: false
- mtime resolution used: false
- baseline_share used as source authority: false
- discussion_packets used as source authority: false
- uncommitted residue used as source authority: false
- repairs allowed: false
- promotions allowed: false
- readiness audit performed: false
- loop execution authorized: false

## Inventory pass semantics

- all components classified: true
- all components present required for pass: false
- missing components allowed in pass: true
- unclassified component is failure: true
- missing component is failure: false

## Summary counts

- required components total: {counts['required_components_total']}
- present verified: {counts['present_verified']}
- present partial: {counts['present_partial']}
- present candidate only: {counts['present_candidate_only']}
- present boundary only: {counts['present_boundary_only']}
- missing: {counts['missing']}
- insufficient: {counts['insufficient']}
- source unverified: {counts['source_unverified']}
- out of scope: {counts['out_of_scope']}

## Component status table

{component_table}

## Repair and ranking boundary

- missing components ranked: false
- next component to build selected: false
- repair plan created: false
- implementation prompt created: false
- candidate promoted: false
- schema promotion requested: false
- human decision consumed: false

## Non-claims

- controlled loop ready: false
- controlled loop authorized: false
- controlled loop operational: false
- runner exists: false
- runner readiness exists: false
- runner authority exists: false
- micro-sweeps authorized: false
- local revision authorized: false
- portability demonstrated: false
- missing components should be built: false
- candidate components should be promoted: false
- partial components are sufficient: false
- boundary-only components are operational: false
- VS1.4 executed: false

## Evidence Yield

- yield branch: CONFIRMATION_YIELD
- Diagnostic Yield component records present: true
- Diagnostic Yield available for non-PRESENT_VERIFIED components: true

## Terminal transition

{ARTIFACT_TRANSITION}

## Boundary statement

VS1.3 inventories the controlled-loop preconditions declared by VS1.2. It classifies every required component and records blockers separately. It does not judge whether the loop is ready, repair gaps, rank missing objects, promote candidates, authorize execution, create a runner, run micro-sweeps, or execute VS1.4.
"""


def validate_inventory(inventory: dict[str, Any], md: str) -> None:
    if inventory.get("schema_version") != SCHEMA_VERSION:
        fail(
            "STOP_VS1_3_SOURCE_IDENTITY_UNVERIFIED",
            field="schema_version",
            expected=SCHEMA_VERSION,
            actual=inventory.get("schema_version"),
        )
    records = inventory.get("component_records")
    if not isinstance(records, list) or len(records) != 20:
        fail(
            "STOP_VS1_3_REQUIRED_COMPONENT_LIST_MISSING",
            field="component_records",
            expected=20,
            actual=len(records) if isinstance(records, list) else type(records).__name__,
        )
    table = inventory.get("component_status_table")
    if not isinstance(table, dict) or list(table.keys()) != EXPECTED_COMPONENTS:
        fail(
            "STOP_VS1_3_REQUIRED_COMPONENT_SET_MISMATCH",
            field="component_status_table",
            expected=EXPECTED_COMPONENTS,
            actual=list(table.keys()) if isinstance(table, dict) else table,
        )
    for record in records:
        full_key = f"{record.get('component_id')}_{record.get('component_name')}"
        if full_key not in EXPECTED_COMPONENTS:
            fail(
                "STOP_VS1_3_COMPONENT_ID_MISMATCH",
                component=full_key,
                field="component_id",
                expected=EXPECTED_COMPONENTS,
                actual=full_key,
            )
        status = record.get("primary_inventory_status")
        if status in PLACEHOLDER_VALUES:
            fail(
                "STOP_VS1_3_PLACEHOLDER_STATUS_EMITTED",
                component=full_key,
                field="primary_inventory_status",
                expected="non-placeholder status",
                actual=status,
            )
        if status not in VALID_STATUSES:
            fail(
                "STOP_VS1_3_COMPONENT_STATUS_INVALID",
                component=full_key,
                field="primary_inventory_status",
                expected=sorted(VALID_STATUSES),
                actual=status,
            )
        if table.get(full_key) != status:
            fail(
                "STOP_VS1_3_COMPONENT_STATUS_MISSING",
                component=full_key,
                field="component_status_table",
                expected=status,
                actual=table.get(full_key),
            )
        blockers = record.get("blocker_flags")
        if not isinstance(blockers, list) or not blockers:
            fail(
                "STOP_VS1_3_BLOCKER_FLAGS_MISSING",
                component=full_key,
                field="blocker_flags",
                expected="non-empty list",
                actual=blockers,
            )
        for blocker in blockers:
            if blocker not in VALID_BLOCKERS:
                fail(
                    "STOP_VS1_3_BLOCKER_FLAGS_INVALID",
                    component=full_key,
                    field="blocker_flags",
                    expected=sorted(VALID_BLOCKERS),
                    actual=blocker,
                )
    if inventory["summary_counts"] != summarize_statuses(records):
        fail(
            "STOP_VS1_3_SUMMARY_COUNT_MISMATCH",
            field="summary_counts",
            expected=summarize_statuses(records),
            actual=inventory["summary_counts"],
        )
    if inventory["blocker_flag_summary"] != summarize_blockers(records):
        fail(
            "STOP_VS1_3_BLOCKER_SUMMARY_MISMATCH",
            field="blocker_flag_summary",
            expected=summarize_blockers(records),
            actual=inventory["blocker_flag_summary"],
        )
    false_paths = [
        "inventory_mode.repo_wide_search_used",
        "inventory_mode.latest_file_resolution_used",
        "inventory_mode.mtime_resolution_used",
        "inventory_mode.baseline_share_used_as_source_authority",
        "inventory_mode.discussion_packets_used_as_source_authority",
        "inventory_mode.uncommitted_residue_used_as_source_authority",
        "inventory_mode.repairs_allowed",
        "inventory_mode.promotions_allowed",
        "inventory_mode.readiness_audit_performed",
        "inventory_mode.loop_execution_authorized",
        "repair_and_ranking_boundary.missing_components_ranked",
        "repair_and_ranking_boundary.next_component_to_build_selected",
        "repair_and_ranking_boundary.repair_plan_created",
        "repair_and_ranking_boundary.implementation_prompt_created",
        "repair_and_ranking_boundary.candidate_promoted",
        "terminal_transition.executes_vs1_4",
        "terminal_transition.authorizes_loop_execution",
        "terminal_transition.authorizes_micro_sweeps",
        "terminal_transition.authorizes_local_revision",
    ]
    for path in false_paths:
        if get_value(inventory, path) is not False:
            fail(
                "STOP_VS1_3_LOOP_EXECUTION_AUTHORIZED",
                field=path,
                expected=False,
                actual=get_value(inventory, path),
            )
    if get_value(inventory, "terminal_transition.transition") != ARTIFACT_TRANSITION:
        fail(
            "STOP_VS1_3_READINESS_VERDICT_ISSUED",
            field="terminal_transition.transition",
            expected=ARTIFACT_TRANSITION,
            actual=get_value(inventory, "terminal_transition.transition"),
        )
    hits = markdown_contains_vs1_3_overclaim(md)
    if hits:
        fail(
            "STOP_VS1_3_READINESS_VERDICT_ISSUED",
            source=OUTPUT_MD,
            field="markdown_overclaim_guard",
            expected=[],
            actual=hits,
        )


def emit_success_readout(inventory: dict[str, Any]) -> None:
    print("BUILD_PHASE_VS1_CONTROLLED_LOOP_PRECONDITION_INVENTORY_V0_COMPLETE")
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"schema_version={SCHEMA_VERSION}")
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"unit_role={UNIT_ROLE}")
    print(f"source_contract_commit_sha={EXPECTED_HEAD}")
    print(f"source_contract_required_status={CONTRACT_STATUS}")
    print(f"source_contract_required_transition={CONTRACT_TRANSITION}")
    print("required_components_total=20")
    print("all_required_components_inventoried=true")
    print("component_set_matches_vs1_2_contract=true")
    print("component_status_table_complete=true")
    print("component_records_complete=true")
    print("summary_counts_match=true")
    print("blocker_summary_matches=true")
    print("declared_components_only=true")
    print("additional_requirements_load_bearing=false")
    print("repo_wide_search_used=false")
    print("latest_file_resolution_used=false")
    print("mtime_resolution_used=false")
    print("baseline_share_used_as_source_authority=false")
    print("discussion_packets_used_as_source_authority=false")
    print("uncommitted_residue_used_as_source_authority=false")
    print("repairs_allowed=false")
    print("promotions_allowed=false")
    print("readiness_audit_performed=false")
    print("loop_execution_authorized=false")
    print("missing_components_ranked=false")
    print("next_component_to_build_selected=false")
    print("repair_plan_created=false")
    print("implementation_prompt_created=false")
    print("candidate_promoted=false")
    print("schema_promotion_requested=false")
    print("human_decision_consumed=false")
    print("controlled_loop_ready=false")
    print("controlled_loop_authorized=false")
    print("controlled_loop_operational=false")
    print("runner_exists=false")
    print("runner_readiness_exists=false")
    print("runner_authority_exists=false")
    print("micro_sweeps_authorized=false")
    print("local_revision_authorized=false")
    print("portability_demonstrated=false")
    print("missing_components_should_be_built=false")
    print("candidate_components_should_be_promoted=false")
    print("partial_components_are_sufficient=false")
    print("boundary_only_components_are_operational=false")
    print("vs1_2_contract_mutated_by_vs1_3=false")
    print("vs1_1_source_intake_mutated_by_vs1_3=false")
    print("post_vs0_direction_decision_receipt_mutated_by_vs1_3=false")
    print("vs0_source_artifacts_mutated_by_vs1_3=false")
    print("evidence_yield_branch=CONFIRMATION_YIELD")
    print("diagnostic_yield_component_records_present=true")
    print("diagnostic_yield_available_for_non_present_verified_components=true")
    print("vs1_4_built=false")
    print("vs1_4_run=false")
    print("readiness_certificate_created=false")
    print("component_repair_artifacts_created=false")
    print("candidate_promotion_artifacts_created=false")
    print("runner_created=false")
    print("runtime_created=false")
    print("move_space_created=false")
    print("micro_sweeps_created=false")
    print(f"inventory_verdict={PASS_VERDICT}")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition={PRINT_TRANSITION}")


def emit_typed_stop(exc: InventoryFailure) -> None:
    print("BUILD_PHASE_VS1_CONTROLLED_LOOP_PRECONDITION_INVENTORY_V0_TYPED_STOP")
    print(f"artifact_id={ARTIFACT_ID}")
    print(f"phase_id={PHASE_ID}")
    print(f"unit_id={UNIT_ID}")
    print(f"inventory_verdict={exc.code}")
    print("yield_branch=DIAGNOSTIC_YIELD")
    print(f"missing_or_invalid_source={exc.source}")
    print(f"violating_component={exc.component}")
    print(f"violating_field={exc.field}")
    print(f"expected_value={exc.expected}")
    print(f"actual_value={exc.actual}")
    print(f"next_lawful_surface={exc.next_surface}")
    print("self_repair_performed=false")
    print("loop_execution_authorized=false")
    print("runner_authority_created=false")
    print("commit_created=false")
    print("push_executed=false")
    print(f"terminal_transition=STOP({exc.code})")


def generate() -> int:
    root = detect_repo_root(Path.cwd())
    require_head(root)
    validate_dirty_scope(root)
    ensure_no_forbidden_artifacts(root)
    for rel_path in [
        SOURCE_CONTRACT_MD,
        SOURCE_INTAKE_MD,
        DIRECTION_MD,
        SOURCE_INTAKE_JSON,
        DIRECTION_JSON,
        VS0_CLOSURE_JSON,
        VS0_EVIDENCE_YIELD_JSON,
        VS0_HAPPY_PATH_VERIFICATION_JSON,
        VS0_NEGATIVE_PROBE_JSON,
    ]:
        require_file(root, rel_path)
    contract = load_json(root, SOURCE_CONTRACT_JSON)
    load_json(root, SOURCE_INTAKE_JSON)
    load_json(root, DIRECTION_JSON)
    load_json(root, VS0_CLOSURE_JSON)
    load_json(root, VS0_EVIDENCE_YIELD_JSON)
    load_json(root, VS0_HAPPY_PATH_VERIFICATION_JSON)
    load_json(root, VS0_NEGATIVE_PROBE_JSON)
    validate_source_contract(contract)
    before_hashes = capture_source_hashes(root)

    inventory = build_inventory(root)
    md = build_markdown(inventory)
    validate_inventory(inventory, md)

    output_json = root / OUTPUT_JSON
    output_md = root / OUTPUT_MD
    output_json.parent.mkdir(parents=True, exist_ok=True)
    output_json.write_text(
        json.dumps(inventory, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    output_md.write_text(md, encoding="utf-8")

    after_hashes = capture_source_hashes(root)
    validate_source_preservation(before_hashes, after_hashes)
    validate_dirty_scope(root)
    ensure_no_forbidden_artifacts(root)
    emit_success_readout(inventory)
    return 0


def main() -> int:
    try:
        return generate()
    except InventoryFailure as exc:
        emit_typed_stop(exc)
        return 1


if __name__ == "__main__":
    sys.exit(main())
