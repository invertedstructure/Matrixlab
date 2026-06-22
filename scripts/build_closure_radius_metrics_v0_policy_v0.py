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

UNIT_ID = "BUILD_CLOSURE_RADIUS_METRICS_V0_POLICY_V0"
NEXT_GOAL = "IMPLEMENT_CLOSURE_RADIUS_METRICS_V0_WITH_DEMO_REPORTS_V0"
TARGET_UNIT_ID = "closure_radius_metrics.v0"

TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID = "6d252e63"
TAXONOMY_EVOLUTION_POLICY_ID = "e84eb230"
TAXONOMY_EVOLUTION_POLICY_RECEIPT_ID = "18da290a"
JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID = "6291b0d9"
JURISDICTION_GATE_POLICY_ID = "57838400"
JURISDICTION_GATE_POLICY_RECEIPT_ID = "993751b4"
MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID = "bef08570"
HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID = "75eabbe2"
PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID = "363d2f4a"
TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID = "cc24a11f"
TRACE_SCHEMA_ID = "b4887660"
PROPOSAL_LEDGER_SCHEMA_ID = "eee2a318"
LOCAL_REGIME_V1_HASH = "25802530"

TAX_IMPL_RECEIPT_PATH = ROOT / "data" / "taxonomy_evolution_v0_implementation_receipts" / f"{TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID}.json"
TAX_POLICY_PATH = ROOT / "data" / "taxonomy_evolution_v0_policies" / f"{TAXONOMY_EVOLUTION_POLICY_ID}.json"
TAX_POLICY_RECEIPT_PATH = ROOT / "data" / "taxonomy_evolution_v0_policy_receipts" / f"{TAXONOMY_EVOLUTION_POLICY_ID}.json"
TAX_REGISTRY_PATH = ROOT / "data" / "taxonomy_evolution_v0" / "taxonomy_registry_v0.json"
TAX_REGISTRY_SCHEMA_PATH = ROOT / "data" / "taxonomy_evolution_v0" / "taxonomy_registry_schema_v0.json"
TAX_TRIGGER_POLICY_PATH = ROOT / "data" / "taxonomy_evolution_v0" / "taxonomy_trigger_policy_v0.json"
TAX_PRESSURE_SCHEMA_PATH = ROOT / "data" / "taxonomy_evolution_v0" / "taxonomy_pressure_record_schema_v0.json"
TAX_EXISTING_VOCAB_SCHEMA_PATH = ROOT / "data" / "taxonomy_evolution_v0" / "existing_vocab_test_schema_v0.json"
TAX_DELTA_SCHEMA_PATH = ROOT / "data" / "taxonomy_evolution_v0" / "taxonomy_delta_schema_v0.json"
TAX_UPGRADE_PROPOSAL_SCHEMA_PATH = ROOT / "data" / "taxonomy_evolution_v0" / "taxonomy_upgrade_proposal_schema_v0.json"
TAX_REVIEW_SCHEMA_PATH = ROOT / "data" / "taxonomy_evolution_v0" / "taxonomy_review_record_schema_v0.json"
TAX_REGISTRY_PATCH_SCHEMA_PATH = ROOT / "data" / "taxonomy_evolution_v0" / "taxonomy_registry_patch_schema_v0.json"
TAX_EVOLUTION_RECEIPT_SCHEMA_PATH = ROOT / "data" / "taxonomy_evolution_v0" / "taxonomy_evolution_receipt_schema_v0.json"
TAX_AUTHORITY_PATCH_PATH = ROOT / "data" / "taxonomy_evolution_v0_patches" / "taxonomy_authority_patch_v0.json"
TAX_MOVE_REGISTRY_PATCH_PATH = ROOT / "data" / "taxonomy_evolution_v0_patches" / "taxonomy_move_registry_patch_v0.json"
TAX_DEMO_RECEIPT_PATH = ROOT / "data" / "taxonomy_evolution_v0_demo" / "taxonomy_evolution_demo_receipt.json"

JURIS_IMPL_RECEIPT_PATH = ROOT / "data" / "jurisdiction_gate_v0_implementation_receipts" / f"{JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID}.json"
JURIS_POLICY_PATH = ROOT / "data" / "jurisdiction_gate_v0_policies" / f"{JURISDICTION_GATE_POLICY_ID}.json"
JURIS_POLICY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_gate_v0_policy_receipts" / f"{JURISDICTION_GATE_POLICY_ID}.json"
JURIS_GATE_PATH = ROOT / "data" / "jurisdiction_gate_v0" / "jurisdiction_gate_v0.json"
JURIS_VERDICT_ENUM_PATH = ROOT / "data" / "jurisdiction_gate_v0" / "jurisdiction_verdict_enum_v0.json"
JURIS_AUTHORITY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_gate_v0_demo" / "day5_demo_authority_receipt.json"

MOVE_IMPL_RECEIPT_PATH = ROOT / "data" / "move_registry_v0_implementation_receipts" / f"{MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID}.json"
MOVE_REGISTRY_PATH = ROOT / "data" / "move_registry_v0" / "move_registry_v0.json"
MOVE_ADMISSION_GATE_PATH = ROOT / "data" / "move_registry_v0" / "move_admission_gate_v0.json"

HALT_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "halt_vocabulary_v0_implementation_receipts" / f"{HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID}.json"
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

OUT_DIR = ROOT / "data" / "closure_radius_metrics_v0_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "closure_radius_metrics_v0_policy_receipts"

SOURCE_FILES = [
    TAX_IMPL_RECEIPT_PATH,
    TAX_POLICY_PATH,
    TAX_POLICY_RECEIPT_PATH,
    TAX_REGISTRY_PATH,
    TAX_REGISTRY_SCHEMA_PATH,
    TAX_TRIGGER_POLICY_PATH,
    TAX_PRESSURE_SCHEMA_PATH,
    TAX_EXISTING_VOCAB_SCHEMA_PATH,
    TAX_DELTA_SCHEMA_PATH,
    TAX_UPGRADE_PROPOSAL_SCHEMA_PATH,
    TAX_REVIEW_SCHEMA_PATH,
    TAX_REGISTRY_PATCH_SCHEMA_PATH,
    TAX_EVOLUTION_RECEIPT_SCHEMA_PATH,
    TAX_AUTHORITY_PATCH_PATH,
    TAX_MOVE_REGISTRY_PATCH_PATH,
    TAX_DEMO_RECEIPT_PATH,
    JURIS_IMPL_RECEIPT_PATH,
    JURIS_POLICY_PATH,
    JURIS_POLICY_RECEIPT_PATH,
    JURIS_GATE_PATH,
    JURIS_VERDICT_ENUM_PATH,
    JURIS_AUTHORITY_RECEIPT_PATH,
    MOVE_IMPL_RECEIPT_PATH,
    MOVE_REGISTRY_PATH,
    MOVE_ADMISSION_GATE_PATH,
    HALT_IMPLEMENTATION_RECEIPT_PATH,
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
]

STOP_CLASSES = [
    "CLEAN_BOUNDARY",
    "LOCAL_REPAIR_PRESSURE",
    "MISSING_MOVE_PRESSURE",
    "TAXONOMY_PRESSURE",
    "AUTHORITY_BOUNDARY",
    "EXTRACTION_BOUNDARY",
    "FRONTIER_BOUNDARY",
    "INVALID_RUN",
    "LOOP_PRESSURE",
]

STOP_CLASS_MAPPING = {
    "schema_version": "stop_class_mapping_v0",
    "classes": STOP_CLASSES,
    "mapping": {
        "STOP_DONE": "CLEAN_BOUNDARY",
        "STOP_NEXT_MOVE_BOUNDARY": "CLEAN_BOUNDARY",
        "STOP_VISIBLE_GOTCHA": "LOCAL_REPAIR_PRESSURE",
        "STOP_PROJECTION_BUG": "LOCAL_REPAIR_PRESSURE",
        "STOP_RECEIPT_MISMATCH": "LOCAL_REPAIR_PRESSURE",
        "STOP_NEEDS_NEW_MOVE": "MISSING_MOVE_PRESSURE",
        "STOP_NO_APPLICABLE_MOVE": "MISSING_MOVE_PRESSURE",
        "NO_APPLICABLE_MOVE": "MISSING_MOVE_PRESSURE_LEGACY_ALIAS_ONLY",
        "STOP_TAXONOMY_GAP": "TAXONOMY_PRESSURE",
        "STOP_UNDERTYPED_OBJECT": "TAXONOMY_PRESSURE",
        "STOP_UNTYPED_UNIT": "TAXONOMY_PRESSURE",
        "STOP_LAYER_COLLAPSE": "TAXONOMY_PRESSURE",
        "STOP_AUTHORITY_BOUNDARY": "AUTHORITY_BOUNDARY",
        "STOP_HUMAN_REVIEW_REQUIRED": "AUTHORITY_BOUNDARY",
        "STOP_PROPOSAL_REQUIRED": "AUTHORITY_BOUNDARY",
        "STOP_FORBIDDEN_MOVE": "AUTHORITY_BOUNDARY",
        "STOP_AUTHORITY_VIOLATION": "AUTHORITY_BOUNDARY",
        "STOP_NEEDS_EXTRACTION": "EXTRACTION_BOUNDARY",
        "STOP_FRONTIER": "FRONTIER_BOUNDARY",
        "INVALID_STATE": "INVALID_RUN",
        "INVALID_REGIME": "INVALID_RUN",
        "REGIME_MISMATCH": "INVALID_RUN",
        "STEP_LIMIT_EXCEEDED": "LOOP_PRESSURE",
    },
    "law": [
        "halts are not automatically failures",
        "clean boundaries may be healthy",
        "authority boundaries may be expected",
        "legacy NO_APPLICABLE_MOVE must not impersonate completed proof or successful closure",
    ],
}

CLOSURE_RADIUS_METRIC_SCHEMA = {
    "schema_version": "closure_radius_metric_schema_v0",
    "required_fields": [
        "closure_radius_report_id",
        "schema_version",
        "run_scope",
        "movement",
        "closure_radius",
        "terminal_halt",
        "authority",
        "taxonomy",
        "burden",
        "distinguishability",
        "score",
        "interpretation",
    ],
    "core_law": "Closure radius counts only lawful, registered, admissible, authorized, traced, receipted movement.",
    "lawful_move_required_flags": [
        "registered",
        "admissible",
        "authorized",
        "executed",
        "trace_emitted",
        "receipt_emitted",
    ],
    "excluded_from_executed_radius": [
        "proposal_only_artifacts",
        "blocked_moves",
        "human_review_requests",
        "taxonomy_proposals",
        "unregistered_moves",
        "unauthorized_moves",
        "unreviewed_taxonomy_patches",
    ],
    "radius_vector": [
        "executed_moves_before_halt",
        "completed_units_before_halt",
        "advance_chain_length",
        "terminal_halt_code",
        "terminal_halt_family",
        "human_review_distance",
        "authority_boundary_distance",
        "taxonomy_gap_distance",
        "missing_move_distance",
        "frontier_distance",
        "receipt_burden_per_move",
        "distinguishability_preservation",
    ],
    "must_not_impersonate": [
        "global autonomy",
        "proof closure",
        "final engine correctness",
        "permission to widen jurisdiction",
        "proof that higher radius is always better",
    ],
}

RUN_METRICS_SCHEMA = {
    "schema_version": "run_metrics_schema_v0",
    "metric_families": {
        "movement": [
            "runs_total",
            "units_started",
            "units_completed",
            "moves_inspected",
            "moves_applicable",
            "moves_admissible",
            "moves_authorized",
            "moves_executed",
            "moves_blocked",
            "advance_transitions",
            "stop_transitions",
            "step_limit_hits",
            "authorized_execution_rate",
            "admissibility_to_authority_ratio",
        ],
        "halt": [
            "halt_count_by_code",
            "halt_count_by_family",
            "halt_count_by_class",
            "terminal_halt_rate",
            "repeat_halt_rate",
            "first_halt_code_per_run",
            "halts_per_unit",
            "halts_per_100_moves",
            "expected_halt_count",
            "unexpected_halt_count",
        ],
        "authority": [
            "authority_verdict_count",
            "human_review_requests",
            "proposal_packets_emitted",
            "forbidden_move_attempts",
            "authority_boundary_halts",
            "authorized_moves_per_run",
            "review_required_per_100_moves",
            "authority_block_rate",
        ],
        "taxonomy": [
            "taxonomy_pressure_count",
            "taxonomy_pressure_by_trigger_halt",
            "existing_vocab_tests",
            "taxonomy_deltas_proposed",
            "taxonomy_deltas_accepted",
            "taxonomy_deltas_rejected",
            "taxonomy_deltas_deferred",
            "withhold_count",
            "split_count",
            "refine_count",
            "weaken_count",
            "add_count",
            "repeat_taxonomy_gap_rate",
            "taxonomy_acceptance_rate",
            "add_bias",
        ],
        "burden": [
            "trace_entries_per_run",
            "receipt_bytes_per_run",
            "receipt_bytes_per_move",
            "halt_record_bytes",
            "proposal_bytes",
            "taxonomy_receipt_bytes",
            "metrics_bytes",
            "artifact_refs_per_receipt",
            "receipt_burden_per_lawful_move",
            "trace_density",
        ],
        "distinguishability": [
            "unique_run_ids",
            "unique_state_sig8s",
            "unique_trace_refs",
            "unique_receipt_refs",
            "duplicate_state_sig8_count",
            "ambiguous_halt_records",
            "missing_trace_links",
            "receipt_trace_mismatch_count",
            "unlinked_proposal_count",
            "unlinked_taxonomy_delta_count",
            "distinguishability_preservation",
        ],
        "trend_delta": [
            "delta_moves_executed",
            "delta_units_completed",
            "delta_human_review_rate",
            "delta_taxonomy_gap_rate",
            "delta_receipt_burden_per_move",
            "delta_repeat_halt_rate",
            "delta_authority_block_rate",
            "delta_distinguishability_preservation",
        ],
    },
}

EXPECTED_HALT_POLICY_SCHEMA = {
    "schema_version": "expected_halt_policy_schema_v0",
    "required_fields": [
        "unit_id",
        "expected_terminal_halts",
        "unexpected_terminal_halts",
    ],
    "law": [
        "expected halts are not automatically success",
        "unexpected halts are not automatically fatal without interpretation",
        "STOP_HUMAN_REVIEW_REQUIRED may be healthy under current jurisdiction",
        "STOP_NEXT_MOVE_BOUNDARY may be clean boundary",
        "STOP_NO_APPLICABLE_MOVE counts as clean only if expected_terminal flag says so",
    ],
}

HALT_DISTRIBUTION_REPORT_SCHEMA = {
    "schema_version": "halt_distribution_report_schema_v0",
    "required_fields": [
        "halt_distribution_report_id",
        "schema_version",
        "run_scope",
        "halt_count_by_code",
        "halt_count_by_family",
        "halt_count_by_class",
        "expected_halt_count",
        "unexpected_halt_count",
        "repeat_halt_count",
        "interpretation",
    ],
    "law": [
        "halt counts must not be hidden under average radius",
        "all terminal halts require code, family, and class",
    ],
}

AUTHORITY_BOUNDARY_REPORT_SCHEMA = {
    "schema_version": "authority_boundary_report_schema_v0",
    "required_fields": [
        "authority_boundary_report_id",
        "schema_version",
        "run_scope",
        "authority_verdict_count",
        "human_review_requests",
        "proposal_packets_emitted",
        "forbidden_move_attempts",
        "authority_block_rate",
        "unauthorized_execution_count",
        "interpretation",
    ],
    "law": [
        "unauthorized execution invalidates closure radius score",
        "proposal-only blocks do not count as executed movement",
        "human review requests are boundaries, not executed movement",
    ],
}

TAXONOMY_PRESSURE_REPORT_SCHEMA = {
    "schema_version": "taxonomy_pressure_report_schema_v0",
    "required_fields": [
        "taxonomy_pressure_report_id",
        "schema_version",
        "run_scope",
        "taxonomy_pressure_count",
        "taxonomy_pressure_by_trigger_halt",
        "taxonomy_deltas_proposed",
        "taxonomy_deltas_accepted",
        "taxonomy_deltas_deferred",
        "withhold_count",
        "add_bias",
        "repeat_taxonomy_gap_rate",
        "interpretation",
    ],
    "law": [
        "taxonomy pressure is separate from accepted taxonomy patch",
        "ADD_* bias must be visible",
        "WITHHOLD is valid and not failure",
    ],
}

RECEIPT_BURDEN_REPORT_SCHEMA = {
    "schema_version": "receipt_burden_report_schema_v0",
    "required_fields": [
        "receipt_burden_report_id",
        "schema_version",
        "run_scope",
        "trace_entries",
        "receipt_bytes",
        "receipt_bytes_per_move",
        "receipt_burden_per_lawful_move",
        "trace_density",
        "artifact_refs_per_receipt",
        "receipt_trace_mismatch_count",
        "interpretation",
    ],
    "law": [
        "high burden is not automatically bad",
        "low burden is not automatically good",
        "trace_density below 1 indicates lost observability",
        "burden increase without distinguishability gain is instrumentation pressure",
    ],
}

DISTINGUISHABILITY_METRIC_SCHEMA = {
    "schema_version": "distinguishability_metric_schema_v0",
    "required_fields": [
        "distinguishability_report_id",
        "schema_version",
        "run_scope",
        "total_events",
        "ambiguous_or_unlinked_events",
        "unique_run_ids",
        "unique_trace_refs",
        "unique_receipt_refs",
        "missing_trace_links",
        "receipt_trace_mismatch_count",
        "unlinked_proposal_count",
        "unlinked_taxonomy_delta_count",
        "distinguishability_preservation",
    ],
    "formula": "1 - ambiguous_or_unlinked_events / max(1, total_events)",
    "law": [
        "events that cannot be distinguished later do not support useful closure-radius measurement",
        "receipt compression must preserve distinguishable transition references",
    ],
}

CLOSURE_RADIUS_SCORE_V0 = {
    "schema_version": "closure_radius_score_v0",
    "formula": "executed_moves_before_halt * distinguishability_preservation * authority_integrity_factor * receipt_integrity_factor",
    "authority_integrity_factor": "0 if unauthorized_execution_count > 0 else 1",
    "receipt_integrity_factor": "1 - receipt_trace_mismatch_count / max(1, moves_executed)",
    "law": [
        "score is dashboard convenience, not closure truth",
        "unauthorized execution zeroes score",
        "higher score is not automatically better",
        "lower score caused by correct human review may be healthier than overreach",
    ],
}

CLOSURE_RADIUS_ROLLUP_SCHEMA = {
    "schema_version": "closure_radius_rollup_schema_v0",
    "required_fields": [
        "closure_radius_rollup_id",
        "schema_version",
        "batch_scope",
        "aggregate_radius",
        "halt_distribution",
        "authority_summary",
        "taxonomy_summary",
        "burden_summary",
        "distinguishability_summary",
        "radius_delta",
        "interpretation",
    ],
    "law": [
        "rollup must not hide bad halts under average progress",
        "rollup must compare current batch against previous batch",
        "radius improvement requires authority and receipt integrity",
    ],
}

CLOSURE_RADIUS_DASHBOARD_READOUT = {
    "schema_version": "closure_radius_dashboard_readout_v0",
    "chips": {
        "radius": [
            "mean_moves_before_halt",
            "median_moves_before_halt",
            "completed_units_before_halt",
            "advance_chain_length",
        ],
        "halts": [
            "top_halt_code",
            "unexpected_halt_count",
            "repeat_halt_count",
            "frontier_halt_count",
        ],
        "authority": [
            "authorized_moves",
            "human_review_requests",
            "proposal_only_blocks",
            "forbidden_moves",
            "unauthorized_executions",
        ],
        "taxonomy": [
            "taxonomy_pressures",
            "proposals",
            "accepted",
            "deferred",
            "repeat_gaps",
            "ADD_bias",
        ],
        "burden": [
            "receipt_bytes_per_move",
            "trace_density",
            "unlinked_events",
            "receipt_mismatches",
        ],
    },
    "must_not_impersonate": [
        "global autonomy",
        "proof closure",
        "final engine correctness",
        "permission to self-authorize future registry changes",
        "proof that higher radius is always better",
    ],
}

DAY7_DEMO_RADIUS_REPORT_PLAN = {
    "schema_version": "day7_demo_radius_report_plan_v0",
    "demo_reports": [
        {
            "demo_name": "DAY7_RADIUS_IMPROVES_CLEANLY",
            "purpose": "Accepted missing-move delta reduces missing-move pressure and allows longer lawful runs.",
            "expected_result": "radius increases with authority_integrity_factor=1 and receipt_integrity_factor=1",
        },
        {
            "demo_name": "DAY7_RADIUS_INCREASES_ILLEGALLY",
            "purpose": "Radius-looking movement includes unauthorized execution.",
            "expected_result": "closure_radius_score=0 and improvement is rejected",
        },
        {
            "demo_name": "DAY7_TAXONOMY_PRESSURE_PRODUCTIVE",
            "purpose": "Short-term radius is low while taxonomy pressure exposes missing vocabulary; repeat pressure drops later.",
            "expected_result": "taxonomy pressure is visible and not treated as failure if repeat pressure falls after review",
        },
        {
            "demo_name": "DAY7_RECEIPT_BURDEN_EXPLODES",
            "purpose": "Receipt burden per move rises while distinguishability is unchanged.",
            "expected_result": "instrumentation pressure is reported, not hidden by radius",
        },
    ],
}

DAY7_DEMO_RADIUS_ROLLUP_PLAN = {
    "schema_version": "day7_demo_radius_rollup_plan_v0",
    "batch_comparison": {
        "previous_batch": "day7_demo_batch_previous",
        "current_batch": "day7_demo_batch_current",
    },
    "required_rollup_checks": [
        "mean radius delta",
        "authority integrity",
        "receipt burden per move",
        "distinguishability preservation",
        "unexpected halt count",
        "taxonomy repeat pressure rate",
    ],
}

REQUIRED_IMPLEMENTATION_ARTIFACTS = {
    "closure_radius_metric_schema": "data/closure_radius_metrics_v0/closure_radius_metric_schema_v0.json",
    "run_metrics_schema": "data/closure_radius_metrics_v0/run_metrics_schema_v0.json",
    "stop_class_mapping": "data/closure_radius_metrics_v0/stop_class_mapping_v0.json",
    "expected_halt_policy_schema": "data/closure_radius_metrics_v0/expected_halt_policy_schema_v0.json",
    "halt_distribution_report_schema": "data/closure_radius_metrics_v0/halt_distribution_report_schema_v0.json",
    "authority_boundary_report_schema": "data/closure_radius_metrics_v0/authority_boundary_report_schema_v0.json",
    "taxonomy_pressure_report_schema": "data/closure_radius_metrics_v0/taxonomy_pressure_report_schema_v0.json",
    "receipt_burden_report_schema": "data/closure_radius_metrics_v0/receipt_burden_report_schema_v0.json",
    "distinguishability_metric_schema": "data/closure_radius_metrics_v0/distinguishability_metric_schema_v0.json",
    "closure_radius_score": "data/closure_radius_metrics_v0/closure_radius_score_v0.json",
    "closure_radius_rollup_schema": "data/closure_radius_metrics_v0/closure_radius_rollup_schema_v0.json",
    "closure_radius_dashboard_readout": "data/closure_radius_metrics_v0/closure_radius_dashboard_readout_v0.json",
    "day7_demo_radius_report": "data/closure_radius_metrics_v0_demo/day7_demo_radius_report.json",
    "day7_demo_radius_rollup": "data/closure_radius_metrics_v0_demo/day7_demo_radius_rollup.json",
    "implementation_receipt": "data/closure_radius_metrics_v0_implementation_receipts/<receipt_id>.json",
}

ACCEPTANCE_GATES = {
    "CRP0_source_surface_verified": {"required": True, "description": "Consumes Day 6 taxonomy evolution, Day 5 jurisdiction gate, Day 4 move registry, Day 3 halt vocabulary, proceed adapter, trace ledger, and local regime."},
    "CRP1_closure_radius_metric_schema_declared": {"required": True, "description": "Closure radius metric schema is declared as vector-first."},
    "CRP2_lawful_movement_counter_declared": {"required": True, "description": "Only registered, admissible, authorized, executed, traced, receipted movement counts."},
    "CRP3_proposal_only_movement_excluded_from_executed_radius": {"required": True, "description": "Proposal-only and blocked artifacts do not count as executed movement."},
    "CRP4_unauthorized_execution_zeroes_or_invalidates_radius_score": {"required": True, "description": "Illegal movement cannot increase radius score."},
    "CRP5_halt_distribution_by_code_family_class_declared": {"required": True, "description": "Halts are counted by code, family, and stop class."},
    "CRP6_expected_vs_unexpected_halt_split_declared": {"required": True, "description": "Expected and unexpected terminal halts are separated."},
    "CRP7_authority_boundary_metrics_declared": {"required": True, "description": "Authority verdicts, review requests, proposal-only blocks, forbidden moves, and unauthorized executions are visible."},
    "CRP8_taxonomy_pressure_metrics_declared_separately_from_accepted_patches": {"required": True, "description": "Taxonomy pressure and accepted local patches are distinct metrics."},
    "CRP9_receipt_burden_per_lawful_move_declared": {"required": True, "description": "Receipt/trace burden is measured per lawful executed move."},
    "CRP10_distinguishability_preservation_declared": {"required": True, "description": "Ambiguous/unlinked events reduce distinguishability preservation."},
    "CRP11_rollup_compares_current_batch_to_previous_batch": {"required": True, "description": "Batch rollup includes deltas against prior batch."},
    "CRP12_readout_includes_must_not_impersonate": {"required": True, "description": "Reports carry anti-impersonation block."},
    "CRP13_higher_radius_not_treated_as_automatically_better": {"required": True, "description": "Radius interpretation preserves halt/authority/burden context."},
    "CRP14_no_optimization_tuning_performed_by_policy": {"required": True, "description": "Policy measures only; does not tune or optimize."},
    "CRP15_no_global_closure_final_intelligence_autonomy_claim": {"required": True, "description": "No global closure, final intelligence, or autonomy claims."},
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
    result = subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def validate_inputs() -> List[str]:
    failures: List[str] = []

    tax_impl = read_json(TAX_IMPL_RECEIPT_PATH)
    tax_policy = read_json(TAX_POLICY_PATH)
    tax_policy_receipt = read_json(TAX_POLICY_RECEIPT_PATH)
    tax_demo = read_json(TAX_DEMO_RECEIPT_PATH)

    juris_impl = read_json(JURIS_IMPL_RECEIPT_PATH)
    juris_auth = read_json(JURIS_AUTHORITY_RECEIPT_PATH)
    move_impl = read_json(MOVE_IMPL_RECEIPT_PATH)
    move_registry = read_json(MOVE_REGISTRY_PATH)
    halt_impl = read_json(HALT_IMPLEMENTATION_RECEIPT_PATH)
    halt_vocab = read_json(HALT_VOCABULARY_PATH)
    proceed = read_json(PROCEED_RECEIPT_PATH)
    trace_ledger = read_json(TRACE_LEDGER_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    proposal_ledger = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    local_regime = read_json(LOCAL_REGIME_V1_PATH)

    if tax_impl.get("receipt_id") != TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID or tax_impl.get("gate") != "PASS":
        failures.append("taxonomy_evolution_implementation_source_not_pass")
    if tax_impl.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append("taxonomy_evolution_terminal_not_done")
    tax_metrics = tax_impl.get("aggregate_metrics", {})
    if tax_metrics.get("demo_run_count") != 4:
        failures.append(f"taxonomy_demo_count_wrong:{tax_metrics.get('demo_run_count')}")
    for key in [
        "delta_without_existing_vocab_test_count",
        "add_used_before_existing_vocab_test_count",
        "proposal_accepted_by_runtime_count",
        "review_fabricated_by_runtime_count",
        "patch_without_ACCEPTED_LOCAL_review_count",
        "label_treated_as_truth_count",
        "taxonomy_delta_widened_authority_count",
        "taxonomy_delta_promoted_theorem_status_count",
        "day7_global_taxonomy_count",
        "global_taxonomy_claim_count",
        "final_closure_claim_count",
        "proof_claim_count",
        "hidden_continuation_count",
    ]:
        if tax_metrics.get(key) != 0:
            failures.append(f"taxonomy_metric_not_zero:{key}:{tax_metrics.get(key)}")
    if tax_policy.get("policy_id") != TAXONOMY_EVOLUTION_POLICY_ID:
        failures.append(f"taxonomy_policy_id_wrong:{tax_policy.get('policy_id')}")
    if tax_policy_receipt.get("receipt_id") != TAXONOMY_EVOLUTION_POLICY_RECEIPT_ID:
        failures.append(f"taxonomy_policy_receipt_id_wrong:{tax_policy_receipt.get('receipt_id')}")
    if tax_demo.get("gate") != "PASS":
        failures.append("taxonomy_demo_receipt_not_pass")
    if tax_demo.get("registry_changed_count") != 1:
        failures.append(f"taxonomy_demo_registry_changed_wrong:{tax_demo.get('registry_changed_count')}")

    if juris_impl.get("receipt_id") != JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID or juris_impl.get("gate") != "PASS":
        failures.append("jurisdiction_gate_source_not_pass")
    juris_metrics = juris_impl.get("aggregate_metrics", {})
    for key in [
        "non_authorized_move_execution_count",
        "proposal_accepted_count",
        "proposal_executed_count",
        "registry_mutation_count",
        "taxonomy_mutation_count",
        "jurisdiction_profile_mutation_count",
        "human_silence_authorized_count",
        "day6_taxonomy_evolution_count",
        "global_governance_claim_count",
        "final_authority_claim_count",
        "proof_claim_count",
    ]:
        if juris_metrics.get(key) != 0:
            failures.append(f"jurisdiction_metric_not_zero:{key}:{juris_metrics.get(key)}")
    counts = juris_auth.get("jurisdiction", {}).get("verdict_counts", {})
    for verdict in ["AUTHORIZED_LOCAL", "REQUIRES_PROPOSAL", "REQUIRES_EXTRACTION", "REQUIRES_HUMAN_REVIEW", "FORBIDDEN"]:
        if counts.get(verdict) != 1:
            failures.append(f"jurisdiction_verdict_count_wrong:{verdict}:{counts.get(verdict)}")

    if move_impl.get("receipt_id") != MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID or move_impl.get("gate") != "PASS":
        failures.append("move_registry_source_not_pass")
    if move_registry.get("move_registry_id") != "move_registry_v0" or len(move_registry.get("moves", {})) != 7:
        failures.append("move_registry_source_wrong")

    if halt_impl.get("receipt_id") != HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID or halt_impl.get("gate") != "PASS":
        failures.append("halt_vocabulary_source_not_pass")
    halt_entries = halt_vocab.get("entries", {})
    for code in [
        "STOP_DONE",
        "STOP_NEXT_MOVE_BOUNDARY",
        "STOP_NEEDS_NEW_MOVE",
        "STOP_NEEDS_EXTRACTION",
        "STOP_TAXONOMY_GAP",
        "STOP_UNDERTYPED_OBJECT",
        "STOP_UNTYPED_UNIT",
        "STOP_LAYER_COLLAPSE",
        "STOP_FRONTIER",
        "STOP_RECEIPT_MISMATCH",
        "STOP_GATE_FAIL",
    ]:
        if code not in halt_entries:
            failures.append(f"halt_vocab_missing_for_radius:{code}")
    if "NO_APPLICABLE_MOVE" in halt_entries:
        failures.append("NO_APPLICABLE_MOVE_canonical_leaked")

    if proceed.get("receipt_id") != PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID or proceed.get("gate") != "PASS":
        failures.append("proceed_source_not_pass")
    if trace_ledger.get("receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID or trace_ledger.get("gate") != "PASS":
        failures.append("trace_ledger_source_not_pass")
    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append("trace_schema_wrong")
    if proposal_ledger.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append("proposal_ledger_schema_wrong")
    if local_regime.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append("local_regime_wrong")

    for path in SOURCE_FILES:
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
        failures.append("policy_receipt_id_mismatch")

    metric_schema = policy.get("closure_radius_metric_schema", {})
    if "Closure radius counts only lawful, registered, admissible, authorized, traced, receipted movement." != metric_schema.get("core_law"):
        failures.append("closure_radius_core_law_wrong")
    for flag in ["registered", "admissible", "authorized", "executed", "trace_emitted", "receipt_emitted"]:
        if flag not in metric_schema.get("lawful_move_required_flags", []):
            failures.append(f"lawful_move_flag_missing:{flag}")
    for excluded in ["proposal_only_artifacts", "blocked_moves", "human_review_requests", "taxonomy_proposals", "unregistered_moves", "unauthorized_moves"]:
        if excluded not in metric_schema.get("excluded_from_executed_radius", []):
            failures.append(f"excluded_radius_missing:{excluded}")
    if "proof that higher radius is always better" not in metric_schema.get("must_not_impersonate", []):
        failures.append("higher_radius_not_always_better_missing")

    run_metrics = policy.get("run_metrics_schema", {})
    for family in ["movement", "halt", "authority", "taxonomy", "burden", "distinguishability", "trend_delta"]:
        if family not in run_metrics.get("metric_families", {}):
            failures.append(f"metric_family_missing:{family}")

    stop_classes = policy.get("stop_class_mapping", {})
    if "LOOP_PRESSURE" not in stop_classes.get("classes", []):
        failures.append("LOOP_PRESSURE_class_missing")
    if stop_classes.get("mapping", {}).get("STOP_HUMAN_REVIEW_REQUIRED") != "AUTHORITY_BOUNDARY":
        failures.append("STOP_HUMAN_REVIEW_REQUIRED_mapping_wrong")
    if stop_classes.get("mapping", {}).get("STOP_NEXT_MOVE_BOUNDARY") != "CLEAN_BOUNDARY":
        failures.append("STOP_NEXT_MOVE_BOUNDARY_mapping_wrong")
    if stop_classes.get("mapping", {}).get("STEP_LIMIT_EXCEEDED") != "LOOP_PRESSURE":
        failures.append("STEP_LIMIT_MAPPING_wrong")

    expected = policy.get("expected_halt_policy_schema", {})
    if "STOP_HUMAN_REVIEW_REQUIRED may be healthy under current jurisdiction" not in expected.get("law", []):
        failures.append("expected_human_review_law_missing")
    if "STOP_NO_APPLICABLE_MOVE counts as clean only if expected_terminal flag says so" not in expected.get("law", []):
        failures.append("no_applicable_move_expected_flag_law_missing")

    authority = policy.get("authority_boundary_report_schema", {})
    if "unauthorized execution invalidates closure radius score" not in authority.get("law", []):
        failures.append("unauthorized_zero_law_missing")
    if "proposal-only blocks do not count as executed movement" not in authority.get("law", []):
        failures.append("proposal_only_not_executed_law_missing")

    taxonomy = policy.get("taxonomy_pressure_report_schema", {})
    if "taxonomy pressure is separate from accepted taxonomy patch" not in taxonomy.get("law", []):
        failures.append("taxonomy_pressure_patch_separation_missing")
    if "ADD_* bias must be visible" not in taxonomy.get("law", []):
        failures.append("add_bias_visible_missing")

    burden = policy.get("receipt_burden_report_schema", {})
    if "trace_density below 1 indicates lost observability" not in burden.get("law", []):
        failures.append("trace_density_law_missing")
    if "burden increase without distinguishability gain is instrumentation pressure" not in burden.get("law", []):
        failures.append("burden_instrumentation_pressure_law_missing")

    distinguishability = policy.get("distinguishability_metric_schema", {})
    if distinguishability.get("formula") != "1 - ambiguous_or_unlinked_events / max(1, total_events)":
        failures.append(f"distinguishability_formula_wrong:{distinguishability.get('formula')}")

    score = policy.get("closure_radius_score", {})
    if score.get("authority_integrity_factor") != "0 if unauthorized_execution_count > 0 else 1":
        failures.append("authority_integrity_factor_wrong")
    if "unauthorized execution zeroes score" not in score.get("law", []):
        failures.append("score_zero_law_missing")
    if "higher score is not automatically better" not in score.get("law", []):
        failures.append("score_not_truth_law_missing")

    rollup = policy.get("closure_radius_rollup_schema", {})
    if "rollup must not hide bad halts under average progress" not in rollup.get("law", []):
        failures.append("rollup_halt_hiding_law_missing")
    if "rollup must compare current batch against previous batch" not in rollup.get("law", []):
        failures.append("rollup_delta_law_missing")

    readout = policy.get("closure_radius_dashboard_readout", {})
    for chip in ["radius", "halts", "authority", "taxonomy", "burden"]:
        if chip not in readout.get("chips", {}):
            failures.append(f"dashboard_chip_missing:{chip}")
    for phrase in [
        "global autonomy",
        "proof closure",
        "final engine correctness",
        "permission to self-authorize future registry changes",
        "proof that higher radius is always better",
    ]:
        if phrase not in readout.get("must_not_impersonate", []):
            failures.append(f"readout_non_impersonation_missing:{phrase}")

    demo_plan = policy.get("day7_demo_radius_report_plan", {})
    demos = [d.get("demo_name") for d in demo_plan.get("demo_reports", [])]
    for demo in [
        "DAY7_RADIUS_IMPROVES_CLEANLY",
        "DAY7_RADIUS_INCREASES_ILLEGALLY",
        "DAY7_TAXONOMY_PRESSURE_PRODUCTIVE",
        "DAY7_RECEIPT_BURDEN_EXPLODES",
    ]:
        if demo not in demos:
            failures.append(f"demo_plan_missing:{demo}")

    gates = policy.get("acceptance_gates", {})
    for gate_id in ACCEPTANCE_GATES:
        if gates.get(gate_id, {}).get("required") is not True:
            failures.append(f"acceptance_gate_missing:{gate_id}")

    guards = policy.get("radius_guards", {})
    for key in [
        "closure_radius_policy_built",
        "source_taxonomy_evolution_consumed",
        "source_jurisdiction_gate_consumed",
        "source_move_registry_consumed",
        "source_halt_vocabulary_consumed",
        "source_proceed_adapter_consumed",
        "source_trace_ledger_surface_consumed",
    ]:
        if guards.get(key) is not True:
            failures.append(f"radius_guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "implementation_performed_by_policy",
        "demo_reports_emitted_by_policy",
        "optimization_performed_by_policy",
        "source_taxonomy_evolution_modified",
        "source_jurisdiction_gate_modified",
        "source_move_registry_modified",
        "source_halt_vocabulary_modified",
        "source_proceed_adapter_modified",
        "source_trace_ledger_runner_modified",
        "source_local_regime_v1_modified",
        "unauthorized_moves_counted_as_radius",
        "proposal_only_counted_as_execution",
        "blocked_moves_counted_as_execution",
        "human_review_request_counted_as_execution",
        "taxonomy_proposal_counted_as_patch",
        "halt_counts_hidden_under_average",
        "no_applicable_move_auto_success",
        "higher_radius_treated_as_always_better",
        "global_closure_claimed",
        "final_intelligence_claimed",
        "autonomy_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
        "sqlite_registry_written",
    ]:
        if guards.get(key) is not False:
            failures.append(f"radius_guard_not_false:{key}:{guards.get(key)}")

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
        "source_taxonomy_impl": TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID,
        "next_goal": NEXT_GOAL,
        "vector": CLOSURE_RADIUS_METRIC_SCHEMA["radius_vector"],
    }
    policy_id = sha8(policy_seed)

    radius_guards = {
        "closure_radius_policy_built": True,
        "source_taxonomy_evolution_consumed": True,
        "source_jurisdiction_gate_consumed": True,
        "source_move_registry_consumed": True,
        "source_halt_vocabulary_consumed": True,
        "source_proceed_adapter_consumed": True,
        "source_trace_ledger_surface_consumed": True,
        "implementation_performed_by_policy": False,
        "demo_reports_emitted_by_policy": False,
        "optimization_performed_by_policy": False,
        "source_taxonomy_evolution_modified": False,
        "source_jurisdiction_gate_modified": False,
        "source_move_registry_modified": False,
        "source_halt_vocabulary_modified": False,
        "source_proceed_adapter_modified": False,
        "source_trace_ledger_runner_modified": False,
        "source_local_regime_v1_modified": False,
        "source_trace_modified": False,
        "source_receipt_modified": False,
        "source_ledger_modified": False,
        "unauthorized_moves_counted_as_radius": False,
        "proposal_only_counted_as_execution": False,
        "blocked_moves_counted_as_execution": False,
        "human_review_request_counted_as_execution": False,
        "taxonomy_proposal_counted_as_patch": False,
        "halt_counts_hidden_under_average": False,
        "no_applicable_move_auto_success": False,
        "higher_radius_treated_as_always_better": False,
        "global_closure_claimed": False,
        "final_intelligence_claimed": False,
        "autonomy_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
        "sqlite_registry_read": False,
        "sqlite_registry_written": False,
    }

    policy = {
        "schema_version": "closure_radius_metrics_v0_policy_v0",
        "policy_type": "CLOSURE_RADIUS_METRICS_V0_POLICY",
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "target_unit_id": TARGET_UNIT_ID,
        "source_taxonomy_evolution_implementation_receipt_id": TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID,
        "source_taxonomy_evolution_policy_id": TAXONOMY_EVOLUTION_POLICY_ID,
        "source_taxonomy_evolution_policy_receipt_id": TAXONOMY_EVOLUTION_POLICY_RECEIPT_ID,
        "source_jurisdiction_gate_implementation_receipt_id": JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID,
        "source_jurisdiction_gate_policy_id": JURISDICTION_GATE_POLICY_ID,
        "source_jurisdiction_gate_policy_receipt_id": JURISDICTION_GATE_POLICY_RECEIPT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": {
            "purpose": "Measure how far the runner proceeds inside a bounded jurisdiction before lawful interruption.",
            "core_law": "Closure radius counts only lawful, registered, admissible, authorized, traced, receipted movement.",
            "non_goal": "no optimization, no global closure, no magic score, no hiding halt pressure, no counting unauthorized/proposal-only movement as radius",
            "interpretation": "Measured lawful distance before lawful interruption, not final intelligence or autonomy.",
        },
        "closure_radius_metric_schema": CLOSURE_RADIUS_METRIC_SCHEMA,
        "run_metrics_schema": RUN_METRICS_SCHEMA,
        "stop_class_mapping": STOP_CLASS_MAPPING,
        "expected_halt_policy_schema": EXPECTED_HALT_POLICY_SCHEMA,
        "halt_distribution_report_schema": HALT_DISTRIBUTION_REPORT_SCHEMA,
        "authority_boundary_report_schema": AUTHORITY_BOUNDARY_REPORT_SCHEMA,
        "taxonomy_pressure_report_schema": TAXONOMY_PRESSURE_REPORT_SCHEMA,
        "receipt_burden_report_schema": RECEIPT_BURDEN_REPORT_SCHEMA,
        "distinguishability_metric_schema": DISTINGUISHABILITY_METRIC_SCHEMA,
        "closure_radius_score": CLOSURE_RADIUS_SCORE_V0,
        "closure_radius_rollup_schema": CLOSURE_RADIUS_ROLLUP_SCHEMA,
        "closure_radius_dashboard_readout": CLOSURE_RADIUS_DASHBOARD_READOUT,
        "day7_demo_radius_report_plan": DAY7_DEMO_RADIUS_REPORT_PLAN,
        "day7_demo_radius_rollup_plan": DAY7_DEMO_RADIUS_ROLLUP_PLAN,
        "required_implementation_artifacts": REQUIRED_IMPLEMENTATION_ARTIFACTS,
        "acceptance_gates": ACCEPTANCE_GATES,
        "authorized_operations_next": {
            "read_closure_radius_policy": True,
            "read_closure_radius_policy_receipt": True,
            "write_closure_radius_metric_schema": True,
            "write_run_metrics_schema": True,
            "write_stop_class_mapping": True,
            "write_expected_halt_policy_schema": True,
            "write_halt_distribution_report_schema": True,
            "write_authority_boundary_report_schema": True,
            "write_taxonomy_pressure_report_schema": True,
            "write_receipt_burden_report_schema": True,
            "write_distinguishability_metric_schema": True,
            "write_closure_radius_score": True,
            "write_closure_radius_rollup_schema": True,
            "write_closure_radius_dashboard_readout": True,
            "emit_day7_demo_radius_report": True,
            "emit_day7_demo_radius_rollup": True,
            "emit_implementation_receipt": True,
        },
        "forbidden_operations_next": {
            "optimize_runner": True,
            "tune_policy_from_metrics": True,
            "mutate_existing_taxonomy_registry": True,
            "mutate_existing_jurisdiction_gate": True,
            "mutate_existing_move_registry": True,
            "mutate_existing_halt_vocabulary": True,
            "modify_source_modules": True,
            "modify_local_regime": True,
            "count_unregistered_move_as_radius": True,
            "count_unauthorized_move_as_radius": True,
            "count_proposal_only_as_execution": True,
            "count_blocked_move_as_execution": True,
            "count_human_review_request_as_execution": True,
            "count_taxonomy_proposal_as_accepted_patch": True,
            "hide_halts_under_average_radius": True,
            "treat_no_applicable_move_as_success_without_expected_terminal": True,
            "report_higher_radius_as_always_better": True,
            "claim_global_closure": True,
            "claim_final_intelligence": True,
            "claim_autonomy": True,
            "claim_proof": True,
            "hidden_continuation_after_terminal": True,
            "sqlite_registry_write": True,
            "latest_or_mtime_selection": True,
            "ambient_workspace_authority": True,
        },
        "safety_clauses": {
            "policy_only": True,
            "does_not_emit_demo_reports": True,
            "does_not_optimize_system": True,
            "does_not_mutate_existing_artifacts": True,
            "does_not_modify_source_modules": True,
            "does_not_modify_source_regime": True,
            "does_not_count_unauthorized_or_proposal_only_movement": True,
            "does_not_hide_halt_pressure": True,
            "does_not_treat_radius_as_magic_score": True,
            "does_not_claim_global_closure": True,
            "does_not_claim_final_intelligence_or_autonomy": True,
            "next_unit_required_for_implementation": True,
        },
        "radius_guards": radius_guards,
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
        "source_taxonomy_impl": TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID,
        "terminal": policy["terminal"],
    }
    receipt_id = sha8(receipt_seed)
    policy["policy_receipt_id"] = receipt_id

    receipt = {
        "schema_version": "closure_radius_metrics_v0_policy_receipt_v0",
        "receipt_type": "CLOSURE_RADIUS_METRICS_V0_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "target_unit_id": TARGET_UNIT_ID,
        "source_taxonomy_evolution_implementation_receipt_id": TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID,
        "source_taxonomy_evolution_policy_id": TAXONOMY_EVOLUTION_POLICY_ID,
        "source_taxonomy_evolution_policy_receipt_id": TAXONOMY_EVOLUTION_POLICY_RECEIPT_ID,
        "source_jurisdiction_gate_implementation_receipt_id": JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID,
        "source_jurisdiction_gate_policy_id": JURISDICTION_GATE_POLICY_ID,
        "source_jurisdiction_gate_policy_receipt_id": JURISDICTION_GATE_POLICY_RECEIPT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": policy["policy_summary"],
        "closure_radius_metric_schema": CLOSURE_RADIUS_METRIC_SCHEMA,
        "run_metrics_schema": RUN_METRICS_SCHEMA,
        "stop_class_mapping": STOP_CLASS_MAPPING,
        "expected_halt_policy_schema": EXPECTED_HALT_POLICY_SCHEMA,
        "halt_distribution_report_schema": HALT_DISTRIBUTION_REPORT_SCHEMA,
        "authority_boundary_report_schema": AUTHORITY_BOUNDARY_REPORT_SCHEMA,
        "taxonomy_pressure_report_schema": TAXONOMY_PRESSURE_REPORT_SCHEMA,
        "receipt_burden_report_schema": RECEIPT_BURDEN_REPORT_SCHEMA,
        "distinguishability_metric_schema": DISTINGUISHABILITY_METRIC_SCHEMA,
        "closure_radius_score": CLOSURE_RADIUS_SCORE_V0,
        "closure_radius_rollup_schema": CLOSURE_RADIUS_ROLLUP_SCHEMA,
        "closure_radius_dashboard_readout": CLOSURE_RADIUS_DASHBOARD_READOUT,
        "day7_demo_radius_report_plan": DAY7_DEMO_RADIUS_REPORT_PLAN,
        "day7_demo_radius_rollup_plan": DAY7_DEMO_RADIUS_ROLLUP_PLAN,
        "required_implementation_artifacts": REQUIRED_IMPLEMENTATION_ARTIFACTS,
        "acceptance_gates": ACCEPTANCE_GATES,
        "authorized_operations_next": policy["authorized_operations_next"],
        "forbidden_operations_next": policy["forbidden_operations_next"],
        "safety_clauses": policy["safety_clauses"],
        "radius_guards": radius_guards,
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
    print(f"closure_radius_policy_id={policy['policy_id']}")
    print(f"closure_radius_policy_receipt_id={receipt['receipt_id']}")
    print(f"closure_radius_policy_path=data/closure_radius_metrics_v0_policies/{policy['policy_id']}.json")
    print(f"closure_radius_policy_receipt_path=data/closure_radius_metrics_v0_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
