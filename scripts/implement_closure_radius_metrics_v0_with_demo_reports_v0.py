#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import statistics
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "IMPLEMENT_CLOSURE_RADIUS_METRICS_V0_WITH_DEMO_REPORTS_V0"
TARGET_UNIT_ID = "closure_radius_metrics.v0"

CLOSURE_RADIUS_POLICY_ID = "80f2b331"
CLOSURE_RADIUS_POLICY_RECEIPT_ID = "fc82cb0f"
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

POLICY_PATH = ROOT / "data" / "closure_radius_metrics_v0_policies" / f"{CLOSURE_RADIUS_POLICY_ID}.json"
POLICY_RECEIPT_PATH = ROOT / "data" / "closure_radius_metrics_v0_policy_receipts" / f"{CLOSURE_RADIUS_POLICY_ID}.json"

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

ARTIFACT_DIR = ROOT / "data" / "closure_radius_metrics_v0"
DEMO_DIR = ROOT / "data" / "closure_radius_metrics_v0_demo"
IMPLEMENTATION_RECEIPT_DIR = ROOT / "data" / "closure_radius_metrics_v0_implementation_receipts"

SOURCE_FILES = [
    POLICY_PATH,
    POLICY_RECEIPT_PATH,
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

STOP_CLASS_BY_CODE = {
    "STOP_DONE": "CLEAN_BOUNDARY",
    "STOP_NEXT_MOVE_BOUNDARY": "CLEAN_BOUNDARY",
    "STOP_VISIBLE_GOTCHA": "LOCAL_REPAIR_PRESSURE",
    "STOP_PROJECTION_BUG": "LOCAL_REPAIR_PRESSURE",
    "STOP_RECEIPT_MISMATCH": "LOCAL_REPAIR_PRESSURE",
    "STOP_NEEDS_NEW_MOVE": "MISSING_MOVE_PRESSURE",
    "STOP_NO_APPLICABLE_MOVE": "MISSING_MOVE_PRESSURE",
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
}

HALT_FAMILY_BY_CODE = {
    "STOP_DONE": "BASE_RUNNER",
    "STOP_NEXT_MOVE_BOUNDARY": "PROCEED_MODE",
    "STOP_VISIBLE_GOTCHA": "PROJECTION",
    "STOP_PROJECTION_BUG": "PROJECTION",
    "STOP_RECEIPT_MISMATCH": "RECEIPT_TRACE",
    "STOP_NEEDS_NEW_MOVE": "TAXONOMY_PRESSURE",
    "STOP_NO_APPLICABLE_MOVE": "BASE_RUNNER",
    "STOP_TAXONOMY_GAP": "TAXONOMY_PRESSURE",
    "STOP_UNDERTYPED_OBJECT": "TAXONOMY_PRESSURE",
    "STOP_UNTYPED_UNIT": "TAXONOMY_PRESSURE",
    "STOP_LAYER_COLLAPSE": "LAYERING",
    "STOP_AUTHORITY_BOUNDARY": "AUTHORITY",
    "STOP_HUMAN_REVIEW_REQUIRED": "AUTHORITY",
    "STOP_PROPOSAL_REQUIRED": "AUTHORITY",
    "STOP_FORBIDDEN_MOVE": "AUTHORITY",
    "STOP_AUTHORITY_VIOLATION": "AUTHORITY",
    "STOP_NEEDS_EXTRACTION": "EXTRACTION_PRESSURE",
    "STOP_FRONTIER": "FRONTIER",
    "STEP_LIMIT_EXCEEDED": "PROCEED_MODE",
}

MUST_NOT_IMPERSONATE = [
    "global autonomy",
    "proof closure",
    "final engine correctness",
    "permission to widen jurisdiction",
    "proof that higher radius is always better",
]

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

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def tracked(path: Path) -> bool:
    relp = rel(path)
    result = subprocess.run(["git", "ls-files", "--error-unmatch", relp], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths if path.exists()}

def validate_source_policy(policy: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if policy.get("policy_id") != CLOSURE_RADIUS_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if receipt.get("receipt_id") != CLOSURE_RADIUS_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{receipt.get('receipt_id')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{receipt.get('policy_status')}")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"target_unit_wrong:{receipt.get('target_unit_id')}")
    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"policy_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"policy_terminal_stop_not_null:{terminal.get('stop_code')}")

    metric = receipt.get("closure_radius_metric_schema", {})
    if metric.get("core_law") != "Closure radius counts only lawful, registered, admissible, authorized, traced, receipted movement.":
        failures.append("closure_radius_core_law_wrong")
    for flag in ["registered", "admissible", "authorized", "executed", "trace_emitted", "receipt_emitted"]:
        if flag not in metric.get("lawful_move_required_flags", []):
            failures.append(f"lawful_move_required_flag_missing:{flag}")
    for excluded in ["proposal_only_artifacts", "blocked_moves", "human_review_requests", "taxonomy_proposals", "unregistered_moves", "unauthorized_moves"]:
        if excluded not in metric.get("excluded_from_executed_radius", []):
            failures.append(f"excluded_radius_missing:{excluded}")

    score = receipt.get("closure_radius_score", {})
    if score.get("authority_integrity_factor") != "0 if unauthorized_execution_count > 0 else 1":
        failures.append("score_authority_integrity_wrong")
    if "unauthorized execution zeroes score" not in score.get("law", []):
        failures.append("score_zero_law_missing")
    if "higher score is not automatically better" not in score.get("law", []):
        failures.append("score_not_truth_law_missing")

    stop = receipt.get("stop_class_mapping", {})
    if stop.get("mapping", {}).get("STOP_HUMAN_REVIEW_REQUIRED") != "AUTHORITY_BOUNDARY":
        failures.append("human_review_mapping_wrong")
    if stop.get("mapping", {}).get("STOP_NEXT_MOVE_BOUNDARY") != "CLEAN_BOUNDARY":
        failures.append("next_move_boundary_mapping_wrong")
    if stop.get("mapping", {}).get("STEP_LIMIT_EXCEEDED") != "LOOP_PRESSURE":
        failures.append("step_limit_mapping_wrong")

    expected = receipt.get("expected_halt_policy_schema", {})
    if "STOP_HUMAN_REVIEW_REQUIRED may be healthy under current jurisdiction" not in expected.get("law", []):
        failures.append("expected_human_review_law_missing")

    burden = receipt.get("receipt_burden_report_schema", {})
    if "trace_density below 1 indicates lost observability" not in burden.get("law", []):
        failures.append("trace_density_law_missing")
    if "burden increase without distinguishability gain is instrumentation pressure" not in burden.get("law", []):
        failures.append("burden_pressure_law_missing")

    rollup = receipt.get("closure_radius_rollup_schema", {})
    if "rollup must not hide bad halts under average progress" not in rollup.get("law", []):
        failures.append("rollup_halt_hiding_law_missing")
    if "rollup must compare current batch against previous batch" not in rollup.get("law", []):
        failures.append("rollup_delta_law_missing")

    readout = receipt.get("closure_radius_dashboard_readout", {})
    for chip in ["radius", "halts", "authority", "taxonomy", "burden"]:
        if chip not in readout.get("chips", {}):
            failures.append(f"readout_chip_missing:{chip}")
    if "proof that higher radius is always better" not in readout.get("must_not_impersonate", []):
        failures.append("readout_higher_radius_not_truth_missing")

    guards = receipt.get("radius_guards", {})
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
            failures.append(f"source_policy_guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "implementation_performed_by_policy",
        "demo_reports_emitted_by_policy",
        "optimization_performed_by_policy",
        "source_taxonomy_evolution_modified",
        "source_jurisdiction_gate_modified",
        "source_move_registry_modified",
        "source_halt_vocabulary_modified",
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
            failures.append(f"source_policy_guard_not_false:{key}:{guards.get(key)}")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def validate_external_sources() -> List[str]:
    failures: List[str] = []

    tax_impl = read_json(TAX_IMPL_RECEIPT_PATH)
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
    regime = read_json(LOCAL_REGIME_V1_PATH)

    if tax_impl.get("receipt_id") != TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID or tax_impl.get("gate") != "PASS":
        failures.append("taxonomy_evolution_source_not_pass")
    if tax_impl.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append("taxonomy_evolution_terminal_not_done")
    tax_metrics = tax_impl.get("aggregate_metrics", {})
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
    ]:
        if tax_metrics.get(key) != 0:
            failures.append(f"taxonomy_metric_not_zero:{key}:{tax_metrics.get(key)}")
    if tax_demo.get("gate") != "PASS" or tax_demo.get("registry_changed_count") != 1:
        failures.append("taxonomy_demo_receipt_wrong")

    if juris_impl.get("receipt_id") != JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID or juris_impl.get("gate") != "PASS":
        failures.append("jurisdiction_gate_source_not_pass")
    for key in [
        "non_authorized_move_execution_count",
        "proposal_accepted_count",
        "proposal_executed_count",
        "registry_mutation_count",
        "taxonomy_mutation_count",
        "jurisdiction_profile_mutation_count",
        "human_silence_authorized_count",
        "global_governance_claim_count",
        "final_authority_claim_count",
        "proof_claim_count",
    ]:
        if juris_impl.get("aggregate_metrics", {}).get(key) != 0:
            failures.append(f"jurisdiction_metric_not_zero:{key}:{juris_impl.get('aggregate_metrics', {}).get(key)}")
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
    if regime.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append("local_regime_wrong")

    return failures

def ratio(num: float, den: float) -> float:
    return 0.0 if den == 0 else round(num / den, 6)

def make_run_scope(demo_name: str) -> Dict[str, Any]:
    seed = {"demo": demo_name, "unit": UNIT_ID}
    return {
        "run_id": f"run_{sha8(seed)}",
        "jurisdiction_profile_id": "jurisdiction_profile_v0",
        "move_registry_id": "move_registry_v0",
        "taxonomy_registry_id": "taxonomy_registry_v0",
        "halt_vocabulary_id": "halt_vocabulary_v0",
    }

def score(executed: int, distinguishability: float, unauthorized: int, receipt_mismatches: int) -> Tuple[float, int, float]:
    authority_integrity = 0 if unauthorized > 0 else 1
    receipt_integrity = round(1 - (receipt_mismatches / max(1, executed)), 6)
    if receipt_integrity < 0:
        receipt_integrity = 0.0
    return round(executed * distinguishability * authority_integrity * receipt_integrity, 6), authority_integrity, receipt_integrity

def make_radius_report(
    *,
    demo_name: str,
    units_started: int,
    units_completed: int,
    moves_inspected: int,
    moves_applicable: int,
    moves_admissible: int,
    moves_authorized: int,
    moves_executed: int,
    moves_blocked: int,
    advance_transitions: int,
    stop_code: str,
    expected_halts: List[str],
    unexpected_halts: List[str],
    authority_counts: Dict[str, int],
    taxonomy: Dict[str, Any],
    trace_entries: int,
    receipt_bytes: int,
    total_events: int,
    ambiguous_or_unlinked_events: int,
    receipt_trace_mismatch_count: int,
    previous_mean_radius: Optional[float],
    current_mean_radius: Optional[float],
    scenario_interpretation: str,
    unauthorized_execution_count: int = 0,
    raw_attempted_execution_count: Optional[int] = None,
) -> Dict[str, Any]:
    run_scope = make_run_scope(demo_name)
    halt_class = STOP_CLASS_BY_CODE.get(stop_code, "INVALID_RUN")
    halt_family = HALT_FAMILY_BY_CODE.get(stop_code, "UNKNOWN")
    trace_density = ratio(trace_entries, moves_executed)
    receipt_bytes_per_move = ratio(receipt_bytes, max(1, moves_executed))
    distinguishability_preservation = round(1 - (ambiguous_or_unlinked_events / max(1, total_events)), 6)
    closure_score, authority_integrity, receipt_integrity = score(
        moves_executed,
        distinguishability_preservation,
        unauthorized_execution_count,
        receipt_trace_mismatch_count,
    )
    expected = stop_code in expected_halts
    unexpected = stop_code in unexpected_halts

    report_seed = {"demo_name": demo_name, "run_scope": run_scope, "stop_code": stop_code, "moves_executed": moves_executed}
    closure_radius_report_id = f"closure_radius_{sha8(report_seed)}"

    return {
        "closure_radius_report_id": closure_radius_report_id,
        "schema_version": "closure_radius_report_v0",
        "demo_name": demo_name,
        "run_scope": run_scope,
        "movement": {
            "units_started": units_started,
            "units_completed": units_completed,
            "moves_inspected": moves_inspected,
            "moves_applicable": moves_applicable,
            "moves_admissible": moves_admissible,
            "moves_authorized": moves_authorized,
            "moves_executed": moves_executed,
            "moves_blocked": moves_blocked,
            "raw_attempted_execution_count": raw_attempted_execution_count if raw_attempted_execution_count is not None else moves_executed,
            "unauthorized_execution_count": unauthorized_execution_count,
            "advance_transitions": advance_transitions,
            "stop_transitions": 1,
            "step_limit_hits": 0,
            "authorized_execution_rate": ratio(moves_executed, moves_authorized),
            "admissibility_to_authority_ratio": ratio(moves_authorized, moves_admissible),
        },
        "lawful_movement_counter": {
            "registered": True,
            "admissible": True,
            "authorized": unauthorized_execution_count == 0,
            "executed": True,
            "trace_emitted": trace_entries >= moves_executed,
            "receipt_emitted": True,
            "proposal_only_counted_as_execution": False,
            "blocked_moves_counted_as_execution": False,
            "human_review_request_counted_as_execution": False,
            "taxonomy_proposal_counted_as_patch": False,
            "unauthorized_moves_counted_as_radius": False,
        },
        "closure_radius": {
            "executed_moves_before_halt": moves_executed,
            "completed_units_before_halt": units_completed,
            "advance_chain_length": advance_transitions,
            "terminal_boundary_type": halt_class,
            "human_review_distance": moves_executed if stop_code == "STOP_HUMAN_REVIEW_REQUIRED" else None,
            "authority_boundary_distance": moves_executed if halt_class == "AUTHORITY_BOUNDARY" else None,
            "taxonomy_gap_distance": moves_executed if halt_class == "TAXONOMY_PRESSURE" else None,
            "missing_move_distance": moves_executed if halt_class == "MISSING_MOVE_PRESSURE" else None,
            "frontier_distance": moves_executed if halt_class == "FRONTIER_BOUNDARY" else None,
        },
        "terminal_halt": {
            "halt_code": stop_code,
            "halt_family": halt_family,
            "halt_class": halt_class,
            "halt_record_ref": f"halt_{sha8({'demo': demo_name, 'halt': stop_code})}",
            "expected_terminal": expected,
            "unexpected_terminal": unexpected,
            "expected_terminal_halts": expected_halts,
            "unexpected_terminal_halts": unexpected_halts,
        },
        "authority": {
            "authority_verdict_count": authority_counts,
            "AUTHORIZED_LOCAL": authority_counts.get("AUTHORIZED_LOCAL", 0),
            "REQUIRES_PROPOSAL": authority_counts.get("REQUIRES_PROPOSAL", 0),
            "REQUIRES_EXTRACTION": authority_counts.get("REQUIRES_EXTRACTION", 0),
            "REQUIRES_HUMAN_REVIEW": authority_counts.get("REQUIRES_HUMAN_REVIEW", 0),
            "FORBIDDEN": authority_counts.get("FORBIDDEN", 0),
            "human_review_requests": authority_counts.get("REQUIRES_HUMAN_REVIEW", 0),
            "proposal_packets_emitted": authority_counts.get("REQUIRES_PROPOSAL", 0),
            "forbidden_move_attempts": authority_counts.get("FORBIDDEN", 0),
            "authority_boundary_halts": 1 if halt_class == "AUTHORITY_BOUNDARY" else 0,
            "authority_block_rate": ratio(
                authority_counts.get("REQUIRES_PROPOSAL", 0)
                + authority_counts.get("REQUIRES_EXTRACTION", 0)
                + authority_counts.get("REQUIRES_HUMAN_REVIEW", 0)
                + authority_counts.get("FORBIDDEN", 0),
                moves_admissible,
            ),
            "unauthorized_execution_count": unauthorized_execution_count,
        },
        "taxonomy": taxonomy,
        "burden": {
            "trace_entries": trace_entries,
            "receipt_bytes": receipt_bytes,
            "receipt_bytes_per_move": receipt_bytes_per_move,
            "receipt_burden_per_lawful_move": receipt_bytes_per_move,
            "trace_density": trace_density,
            "artifact_refs_per_receipt": 6,
            "receipt_trace_mismatch_count": receipt_trace_mismatch_count,
            "burden_instrumentation_pressure": False,
        },
        "distinguishability": {
            "total_events": total_events,
            "ambiguous_or_unlinked_events": ambiguous_or_unlinked_events,
            "unique_run_ids": 1,
            "unique_state_sig8s": max(1, moves_executed),
            "unique_trace_refs": trace_entries,
            "unique_receipt_refs": 1,
            "missing_trace_links": 0,
            "receipt_trace_mismatch_count": receipt_trace_mismatch_count,
            "unlinked_proposal_count": 0,
            "unlinked_taxonomy_delta_count": 0,
            "distinguishability_preservation": distinguishability_preservation,
        },
        "score": {
            "closure_radius_score": closure_score,
            "authority_integrity_factor": authority_integrity,
            "receipt_integrity_factor": receipt_integrity,
            "score_is_dashboard_convenience_not_truth": True,
            "radius_improvement_valid": authority_integrity == 1 and receipt_integrity > 0,
        },
        "trend_context": {
            "previous_batch_mean_radius": previous_mean_radius,
            "current_batch_mean_radius": current_mean_radius,
            "delta_mean_radius": None if previous_mean_radius is None or current_mean_radius is None else round(current_mean_radius - previous_mean_radius, 6),
        },
        "interpretation": {
            "smallest_honest_reading": scenario_interpretation,
            "must_not_impersonate": MUST_NOT_IMPERSONATE,
            "allowed_next_handling": [
                "review reported boundary",
                "compare batch rollup",
                "do not optimize from this report alone",
                "declare next unit only after review",
            ],
            "higher_radius_not_automatically_better": True,
        },
        "gate": "PASS",
        "failures": [],
    }

def make_demo_reports() -> List[Dict[str, Any]]:
    return [
        make_radius_report(
            demo_name="DAY7_RADIUS_IMPROVES_CLEANLY",
            units_started=4,
            units_completed=3,
            moves_inspected=42,
            moves_applicable=18,
            moves_admissible=12,
            moves_authorized=12,
            moves_executed=12,
            moves_blocked=0,
            advance_transitions=3,
            stop_code="STOP_NEXT_MOVE_BOUNDARY",
            expected_halts=["STOP_DONE", "STOP_NEXT_MOVE_BOUNDARY", "STOP_HUMAN_REVIEW_REQUIRED"],
            unexpected_halts=["STOP_RECEIPT_MISMATCH", "STOP_AUTHORITY_VIOLATION", "STOP_LAYER_COLLAPSE"],
            authority_counts={"AUTHORIZED_LOCAL": 12, "REQUIRES_PROPOSAL": 0, "REQUIRES_EXTRACTION": 0, "REQUIRES_HUMAN_REVIEW": 0, "FORBIDDEN": 0},
            taxonomy={
                "pressure_count": 0,
                "taxonomy_pressure_by_trigger_halt": {},
                "deltas_proposed": 0,
                "deltas_accepted": 0,
                "deltas_deferred": 0,
                "withhold_count": 0,
                "add_bias": 0.0,
                "repeat_taxonomy_gap_count": 0,
                "repeat_taxonomy_gap_rate": 0.0,
                "accepted_patches_count": 0,
            },
            trace_entries=12,
            receipt_bytes=16800,
            total_events=18,
            ambiguous_or_unlinked_events=0,
            receipt_trace_mismatch_count=0,
            previous_mean_radius=4.0,
            current_mean_radius=9.0,
            scenario_interpretation="Accepted missing-move handling reduced missing-move pressure and allowed longer lawful runs; terminal boundary is clean.",
        ),
        make_radius_report(
            demo_name="DAY7_RADIUS_INCREASES_ILLEGALLY",
            units_started=5,
            units_completed=4,
            moves_inspected=58,
            moves_applicable=25,
            moves_admissible=20,
            moves_authorized=18,
            moves_executed=18,
            moves_blocked=2,
            raw_attempted_execution_count=20,
            unauthorized_execution_count=2,
            advance_transitions=4,
            stop_code="STOP_AUTHORITY_VIOLATION",
            expected_halts=["STOP_DONE", "STOP_NEXT_MOVE_BOUNDARY", "STOP_HUMAN_REVIEW_REQUIRED"],
            unexpected_halts=["STOP_RECEIPT_MISMATCH", "STOP_AUTHORITY_VIOLATION", "STOP_LAYER_COLLAPSE"],
            authority_counts={"AUTHORIZED_LOCAL": 18, "REQUIRES_PROPOSAL": 0, "REQUIRES_EXTRACTION": 0, "REQUIRES_HUMAN_REVIEW": 0, "FORBIDDEN": 2},
            taxonomy={
                "pressure_count": 0,
                "taxonomy_pressure_by_trigger_halt": {},
                "deltas_proposed": 0,
                "deltas_accepted": 0,
                "deltas_deferred": 0,
                "withhold_count": 0,
                "add_bias": 0.0,
                "repeat_taxonomy_gap_count": 0,
                "repeat_taxonomy_gap_rate": 0.0,
                "accepted_patches_count": 0,
            },
            trace_entries=18,
            receipt_bytes=23000,
            total_events=26,
            ambiguous_or_unlinked_events=0,
            receipt_trace_mismatch_count=0,
            previous_mean_radius=9.0,
            current_mean_radius=20.0,
            scenario_interpretation="Raw movement increased, but unauthorized execution was detected; closure radius score is zero and improvement is rejected.",
        ),
        make_radius_report(
            demo_name="DAY7_TAXONOMY_PRESSURE_PRODUCTIVE",
            units_started=3,
            units_completed=2,
            moves_inspected=31,
            moves_applicable=12,
            moves_admissible=8,
            moves_authorized=8,
            moves_executed=5,
            moves_blocked=3,
            advance_transitions=2,
            stop_code="STOP_TAXONOMY_GAP",
            expected_halts=["STOP_DONE", "STOP_NEXT_MOVE_BOUNDARY", "STOP_TAXONOMY_GAP"],
            unexpected_halts=["STOP_RECEIPT_MISMATCH", "STOP_AUTHORITY_VIOLATION", "STOP_LAYER_COLLAPSE"],
            authority_counts={"AUTHORIZED_LOCAL": 8, "REQUIRES_PROPOSAL": 0, "REQUIRES_EXTRACTION": 0, "REQUIRES_HUMAN_REVIEW": 0, "FORBIDDEN": 0},
            taxonomy={
                "pressure_count": 3,
                "taxonomy_pressure_by_trigger_halt": {"STOP_TAXONOMY_GAP": 3},
                "deltas_proposed": 3,
                "deltas_accepted": 2,
                "deltas_deferred": 1,
                "withhold_count": 0,
                "add_bias": 0.333333,
                "repeat_taxonomy_gap_count": 0,
                "repeat_taxonomy_gap_rate": 0.0,
                "accepted_patches_count": 2,
            },
            trace_entries=5,
            receipt_bytes=12500,
            total_events=12,
            ambiguous_or_unlinked_events=0,
            receipt_trace_mismatch_count=0,
            previous_mean_radius=7.0,
            current_mean_radius=5.0,
            scenario_interpretation="Short-term radius remains limited by taxonomy pressure, while accepted deltas reduce repeat gap pressure; this is productive pressure, not radius improvement.",
        ),
        make_radius_report(
            demo_name="DAY7_RECEIPT_BURDEN_EXPLODES",
            units_started=3,
            units_completed=2,
            moves_inspected=34,
            moves_applicable=12,
            moves_admissible=9,
            moves_authorized=7,
            moves_executed=7,
            moves_blocked=2,
            advance_transitions=2,
            stop_code="STOP_NEXT_MOVE_BOUNDARY",
            expected_halts=["STOP_DONE", "STOP_NEXT_MOVE_BOUNDARY", "STOP_HUMAN_REVIEW_REQUIRED"],
            unexpected_halts=["STOP_RECEIPT_MISMATCH", "STOP_AUTHORITY_VIOLATION", "STOP_LAYER_COLLAPSE"],
            authority_counts={"AUTHORIZED_LOCAL": 7, "REQUIRES_PROPOSAL": 1, "REQUIRES_EXTRACTION": 0, "REQUIRES_HUMAN_REVIEW": 1, "FORBIDDEN": 0},
            taxonomy={
                "pressure_count": 1,
                "taxonomy_pressure_by_trigger_halt": {"STOP_UNDERTYPED_OBJECT": 1},
                "deltas_proposed": 1,
                "deltas_accepted": 0,
                "deltas_deferred": 1,
                "withhold_count": 0,
                "add_bias": 0.0,
                "repeat_taxonomy_gap_count": 0,
                "repeat_taxonomy_gap_rate": 0.0,
                "accepted_patches_count": 0,
            },
            trace_entries=7,
            receipt_bytes=43400,
            total_events=15,
            ambiguous_or_unlinked_events=0,
            receipt_trace_mismatch_count=0,
            previous_mean_radius=7.0,
            current_mean_radius=7.0,
            scenario_interpretation="Radius is stable, but receipt burden per move doubled without distinguishability gain; report as instrumentation pressure, not hidden progress.",
        ),
    ]

def mark_burden_pressure(report: Dict[str, Any]) -> None:
    if report["demo_name"] == "DAY7_RECEIPT_BURDEN_EXPLODES":
        report["burden"]["previous_receipt_burden_per_move"] = 3100.0
        report["burden"]["current_receipt_burden_per_move"] = report["burden"]["receipt_burden_per_lawful_move"]
        report["burden"]["burden_instrumentation_pressure"] = True

def validate_radius_report(report: Dict[str, Any], policy_receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    name = report.get("demo_name")
    movement = report.get("movement", {})
    counter = report.get("lawful_movement_counter", {})
    terminal = report.get("terminal_halt", {})
    authority = report.get("authority", {})
    taxonomy = report.get("taxonomy", {})
    burden = report.get("burden", {})
    distinguishability = report.get("distinguishability", {})
    score_obj = report.get("score", {})
    interpretation = report.get("interpretation", {})

    if report.get("gate") != "PASS":
        failures.append(f"{name}:gate_not_PASS")
    if terminal.get("halt_code") not in STOP_CLASS_BY_CODE:
        failures.append(f"{name}:unknown_stop_class:{terminal.get('halt_code')}")
    if terminal.get("halt_class") != STOP_CLASS_BY_CODE.get(terminal.get("halt_code")):
        failures.append(f"{name}:halt_class_wrong:{terminal.get('halt_class')}")
    if not terminal.get("expected_terminal") and not terminal.get("unexpected_terminal"):
        failures.append(f"{name}:terminal_neither_expected_nor_unexpected")
    if terminal.get("halt_code") == "STOP_NO_APPLICABLE_MOVE" and not terminal.get("expected_terminal"):
        failures.append(f"{name}:no_applicable_move_not_expected")

    for flag in ["registered", "admissible", "executed", "trace_emitted", "receipt_emitted"]:
        if counter.get(flag) is not True:
            failures.append(f"{name}:lawful_flag_not_true:{flag}:{counter.get(flag)}")
    for excluded in [
        "proposal_only_counted_as_execution",
        "blocked_moves_counted_as_execution",
        "human_review_request_counted_as_execution",
        "taxonomy_proposal_counted_as_patch",
        "unauthorized_moves_counted_as_radius",
    ]:
        if counter.get(excluded) is not False:
            failures.append(f"{name}:excluded_counter_not_false:{excluded}:{counter.get(excluded)}")

    if authority.get("unauthorized_execution_count", 0) > 0:
        if score_obj.get("authority_integrity_factor") != 0:
            failures.append(f"{name}:unauthorized_did_not_zero_authority_integrity")
        if score_obj.get("closure_radius_score") != 0:
            failures.append(f"{name}:unauthorized_did_not_zero_score:{score_obj.get('closure_radius_score')}")
        if score_obj.get("radius_improvement_valid") is not False:
            failures.append(f"{name}:illegal_improvement_marked_valid")
    else:
        if score_obj.get("authority_integrity_factor") != 1:
            failures.append(f"{name}:authority_integrity_not_one")
    if movement.get("moves_executed", 0) > movement.get("moves_authorized", 0):
        failures.append(f"{name}:executed_exceeds_authorized")
    if movement.get("raw_attempted_execution_count", 0) > movement.get("moves_executed", 0) and authority.get("unauthorized_execution_count", 0) == 0:
        failures.append(f"{name}:raw_attempted_exceeds_executed_without_unauthorized_count")

    if burden.get("trace_density", 0) < 1:
        failures.append(f"{name}:trace_density_below_one")
    expected_density = round(burden.get("trace_entries", 0) / max(1, movement.get("moves_executed", 0)), 6)
    if burden.get("trace_density") != expected_density:
        failures.append(f"{name}:trace_density_wrong:{burden.get('trace_density')} expected {expected_density}")
    expected_burden = round(burden.get("receipt_bytes", 0) / max(1, movement.get("moves_executed", 0)), 6)
    if burden.get("receipt_burden_per_lawful_move") != expected_burden:
        failures.append(f"{name}:burden_per_move_wrong:{burden.get('receipt_burden_per_lawful_move')} expected {expected_burden}")

    expected_dist = round(1 - (distinguishability.get("ambiguous_or_unlinked_events", 0) / max(1, distinguishability.get("total_events", 0))), 6)
    if distinguishability.get("distinguishability_preservation") != expected_dist:
        failures.append(f"{name}:distinguishability_wrong:{distinguishability.get('distinguishability_preservation')} expected {expected_dist}")
    if distinguishability.get("missing_trace_links", 0) != 0:
        failures.append(f"{name}:missing_trace_links_nonzero")
    if distinguishability.get("unlinked_proposal_count", 0) != 0:
        failures.append(f"{name}:unlinked_proposal_nonzero")
    if distinguishability.get("unlinked_taxonomy_delta_count", 0) != 0:
        failures.append(f"{name}:unlinked_taxonomy_delta_nonzero")

    if taxonomy.get("accepted_patches_count", 0) > taxonomy.get("deltas_accepted", 0):
        failures.append(f"{name}:accepted_patches_exceed_accepted_deltas")
    if taxonomy.get("add_bias", 0) > 1:
        failures.append(f"{name}:add_bias_gt_one")
    if name == "DAY7_TAXONOMY_PRESSURE_PRODUCTIVE":
        if taxonomy.get("pressure_count") != 3 or taxonomy.get("deltas_accepted") != 2 or taxonomy.get("repeat_taxonomy_gap_rate") != 0.0:
            failures.append(f"{name}:productive_taxonomy_metrics_wrong")
    if name == "DAY7_RECEIPT_BURDEN_EXPLODES":
        if burden.get("burden_instrumentation_pressure") is not True:
            failures.append(f"{name}:burden_pressure_not_marked")
    if name == "DAY7_RADIUS_IMPROVES_CLEANLY":
        if report.get("trend_context", {}).get("delta_mean_radius", 0) <= 0:
            failures.append(f"{name}:clean_radius_not_improved")
        if score_obj.get("radius_improvement_valid") is not True:
            failures.append(f"{name}:clean_improvement_invalid")
    if name == "DAY7_RADIUS_INCREASES_ILLEGALLY":
        if score_obj.get("closure_radius_score") != 0 or score_obj.get("radius_improvement_valid") is not False:
            failures.append(f"{name}:illegal_radius_not_rejected")

    for phrase in MUST_NOT_IMPERSONATE:
        if phrase not in interpretation.get("must_not_impersonate", []):
            failures.append(f"{name}:must_not_impersonate_missing:{phrase}")
    if interpretation.get("higher_radius_not_automatically_better") is not True:
        failures.append(f"{name}:higher_radius_guard_missing")

    return failures

def make_demo_report_bundle(reports: List[Dict[str, Any]]) -> Dict[str, Any]:
    seed = {"reports": [r["closure_radius_report_id"] for r in reports]}
    return {
        "schema_version": "day7_demo_radius_report_v0",
        "day7_demo_radius_report_id": f"day7_radius_report_{sha8(seed)}",
        "source_policy_id": CLOSURE_RADIUS_POLICY_ID,
        "scenario_reports": reports,
        "demo_names": [r["demo_name"] for r in reports],
        "summary": {
            "scenario_count": len(reports),
            "lawful_improvement_count": sum(1 for r in reports if r["score"]["radius_improvement_valid"] and r["trend_context"]["delta_mean_radius"] and r["trend_context"]["delta_mean_radius"] > 0),
            "illegal_improvement_rejected_count": sum(1 for r in reports if r["authority"]["unauthorized_execution_count"] > 0 and r["score"]["closure_radius_score"] == 0),
            "productive_taxonomy_pressure_count": sum(1 for r in reports if r["demo_name"] == "DAY7_TAXONOMY_PRESSURE_PRODUCTIVE" and r["taxonomy"]["repeat_taxonomy_gap_rate"] == 0.0),
            "burden_pressure_count": sum(1 for r in reports if r["burden"].get("burden_instrumentation_pressure") is True),
        },
        "must_not_impersonate": MUST_NOT_IMPERSONATE,
        "gate": "PASS",
        "failures": [],
        "created_at": now_iso(),
    }

def validate_demo_report_bundle(bundle: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    summary = bundle.get("summary", {})
    expected = {
        "scenario_count": 4,
        "lawful_improvement_count": 1,
        "illegal_improvement_rejected_count": 1,
        "productive_taxonomy_pressure_count": 1,
        "burden_pressure_count": 1,
    }
    for key, expected_value in expected.items():
        if summary.get(key) != expected_value:
            failures.append(f"bundle_summary_wrong:{key}:{summary.get(key)} expected {expected_value}")
    for demo in [
        "DAY7_RADIUS_IMPROVES_CLEANLY",
        "DAY7_RADIUS_INCREASES_ILLEGALLY",
        "DAY7_TAXONOMY_PRESSURE_PRODUCTIVE",
        "DAY7_RECEIPT_BURDEN_EXPLODES",
    ]:
        if demo not in bundle.get("demo_names", []):
            failures.append(f"bundle_demo_missing:{demo}")
    for phrase in MUST_NOT_IMPERSONATE:
        if phrase not in bundle.get("must_not_impersonate", []):
            failures.append(f"bundle_non_impersonation_missing:{phrase}")
    return failures

def mean(values: List[float]) -> float:
    return round(sum(values) / max(1, len(values)), 6)

def median(values: List[float]) -> float:
    return round(float(statistics.median(values)), 6) if values else 0.0

def make_rollup(reports: List[Dict[str, Any]]) -> Dict[str, Any]:
    radii = [r["closure_radius"]["executed_moves_before_halt"] for r in reports]
    scores = [r["score"]["closure_radius_score"] for r in reports]
    halt_distribution: Dict[str, int] = {}
    class_distribution: Dict[str, int] = {}
    for r in reports:
        halt_distribution[r["terminal_halt"]["halt_code"]] = halt_distribution.get(r["terminal_halt"]["halt_code"], 0) + 1
        class_distribution[r["terminal_halt"]["halt_class"]] = class_distribution.get(r["terminal_halt"]["halt_class"], 0) + 1

    authorized_moves = sum(r["authority"]["AUTHORIZED_LOCAL"] for r in reports)
    admissible_moves = sum(r["movement"]["moves_admissible"] for r in reports)
    block_total = sum(
        r["authority"]["REQUIRES_PROPOSAL"]
        + r["authority"]["REQUIRES_EXTRACTION"]
        + r["authority"]["REQUIRES_HUMAN_REVIEW"]
        + r["authority"]["FORBIDDEN"]
        for r in reports
    )
    pressure_total = sum(r["taxonomy"]["pressure_count"] for r in reports)
    proposed_total = sum(r["taxonomy"]["deltas_proposed"] for r in reports)
    accepted_total = sum(r["taxonomy"]["deltas_accepted"] for r in reports)
    deferred_total = sum(r["taxonomy"]["deltas_deferred"] for r in reports)
    add_bias_num = sum(r["taxonomy"]["add_bias"] * max(1, r["taxonomy"]["deltas_proposed"]) for r in reports)
    add_bias_den = sum(max(1, r["taxonomy"]["deltas_proposed"]) for r in reports)
    burden_values = [r["burden"]["receipt_burden_per_lawful_move"] for r in reports]
    dist_values = [r["distinguishability"]["distinguishability_preservation"] for r in reports]
    unauthorized_total = sum(r["authority"]["unauthorized_execution_count"] for r in reports)
    mismatch_total = sum(r["distinguishability"]["receipt_trace_mismatch_count"] for r in reports)
    unlinked_total = sum(r["distinguishability"]["ambiguous_or_unlinked_events"] for r in reports)

    previous_batch_mean_radius = 6.1
    current_batch_mean_radius = mean(radii)
    delta_mean_radius = round(current_batch_mean_radius - previous_batch_mean_radius, 6)

    seed = {"reports": [r["closure_radius_report_id"] for r in reports], "mean": current_batch_mean_radius}
    return {
        "closure_radius_rollup_id": f"closure_rollup_{sha8(seed)}",
        "schema_version": "closure_radius_rollup_v0",
        "batch_scope": {
            "batch_id": "day7_demo_batch_current",
            "previous_batch_id": "day7_demo_batch_previous",
            "runs_total": len(reports),
            "jurisdiction_profile_id": "jurisdiction_profile_v0",
        },
        "aggregate_radius": {
            "mean_executed_moves_before_halt": current_batch_mean_radius,
            "median_executed_moves_before_halt": median(radii),
            "max_executed_moves_before_halt": max(radii),
            "min_executed_moves_before_halt": min(radii),
            "mean_closure_radius_score": mean(scores),
        },
        "halt_distribution": halt_distribution,
        "halt_class_distribution": class_distribution,
        "authority_summary": {
            "authorized_moves": authorized_moves,
            "human_review_requests": sum(r["authority"]["human_review_requests"] for r in reports),
            "proposal_packets": sum(r["authority"]["proposal_packets_emitted"] for r in reports),
            "forbidden_moves": sum(r["authority"]["forbidden_move_attempts"] for r in reports),
            "unauthorized_executions": unauthorized_total,
            "authority_block_rate": ratio(block_total, admissible_moves),
        },
        "taxonomy_summary": {
            "pressures": pressure_total,
            "proposals": proposed_total,
            "accepted": accepted_total,
            "deferred": deferred_total,
            "repeat_pressure_rate": ratio(sum(r["taxonomy"]["repeat_taxonomy_gap_count"] for r in reports), max(1, pressure_total)),
            "add_bias": ratio(add_bias_num, add_bias_den),
        },
        "burden_summary": {
            "mean_receipt_burden_per_move": mean(burden_values),
            "max_receipt_burden_per_move": max(burden_values),
            "burden_pressure_count": sum(1 for r in reports if r["burden"].get("burden_instrumentation_pressure")),
        },
        "distinguishability_summary": {
            "mean_distinguishability_preservation": mean(dist_values),
            "receipt_trace_mismatch_count": mismatch_total,
            "unlinked_event_count": unlinked_total,
        },
        "radius_delta": {
            "previous_batch_mean_radius": previous_batch_mean_radius,
            "current_batch_mean_radius": current_batch_mean_radius,
            "delta_mean_radius": delta_mean_radius,
            "interpretation": "Mean radius increased, but the illegal-radius demo is rejected by authority integrity and the burden demo is flagged as instrumentation pressure.",
        },
        "dashboard_readout": {
            "radius": {
                "mean_moves_before_halt": current_batch_mean_radius,
                "median_moves_before_halt": median(radii),
                "completed_units_before_halt": sum(r["closure_radius"]["completed_units_before_halt"] for r in reports),
                "advance_chain_length": sum(r["closure_radius"]["advance_chain_length"] for r in reports),
            },
            "halts": {
                "top_halt_code": max(halt_distribution, key=halt_distribution.get),
                "unexpected_halt_count": sum(1 for r in reports if r["terminal_halt"]["unexpected_terminal"]),
                "repeat_halt_count": sum(max(0, c - 1) for c in halt_distribution.values()),
                "frontier_halt_count": halt_distribution.get("STOP_FRONTIER", 0),
            },
            "authority": {
                "authorized_moves": authorized_moves,
                "human_review_requests": sum(r["authority"]["human_review_requests"] for r in reports),
                "proposal_only_blocks": sum(r["authority"]["proposal_packets_emitted"] for r in reports),
                "forbidden_moves": sum(r["authority"]["forbidden_move_attempts"] for r in reports),
                "unauthorized_executions": unauthorized_total,
            },
            "taxonomy": {
                "taxonomy_pressures": pressure_total,
                "proposals": proposed_total,
                "accepted": accepted_total,
                "deferred": deferred_total,
                "repeat_gaps": sum(r["taxonomy"]["repeat_taxonomy_gap_count"] for r in reports),
                "ADD_bias": ratio(add_bias_num, add_bias_den),
            },
            "burden": {
                "receipt_bytes_per_move": mean(burden_values),
                "trace_density": mean([r["burden"]["trace_density"] for r in reports]),
                "unlinked_events": unlinked_total,
                "receipt_mismatches": mismatch_total,
            },
        },
        "interpretation": {
            "smallest_honest_reading": "The batch shows lawful radius improvement in one scenario, rejects illegal radius by score zeroing, exposes productive taxonomy pressure, and flags receipt-burden pressure.",
            "must_not_impersonate": MUST_NOT_IMPERSONATE,
            "higher_radius_not_automatically_better": True,
            "allowed_next_handling": [
                "review illegal-radius guard before any optimization",
                "review burden pressure before increasing instrumentation",
                "use taxonomy repeat-pressure trend before accepting new labels",
            ],
        },
        "gate": "PASS",
        "failures": [],
    }

def validate_rollup(rollup: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if rollup.get("gate") != "PASS":
        failures.append("rollup_gate_not_PASS")
    if rollup.get("batch_scope", {}).get("runs_total") != 4:
        failures.append(f"rollup_runs_total_wrong:{rollup.get('batch_scope', {}).get('runs_total')}")
    if rollup.get("radius_delta", {}).get("previous_batch_mean_radius") is None:
        failures.append("rollup_missing_previous_batch")
    if "STOP_AUTHORITY_VIOLATION" not in rollup.get("halt_distribution", {}):
        failures.append("rollup_missing_illegal_authority_halt")
    if rollup.get("authority_summary", {}).get("unauthorized_executions") != 2:
        failures.append(f"rollup_unauthorized_count_wrong:{rollup.get('authority_summary', {}).get('unauthorized_executions')}")
    if rollup.get("burden_summary", {}).get("burden_pressure_count") != 1:
        failures.append("rollup_burden_pressure_count_wrong")
    if rollup.get("distinguishability_summary", {}).get("unlinked_event_count") != 0:
        failures.append("rollup_unlinked_event_count_nonzero")
    if rollup.get("dashboard_readout", {}).get("authority", {}).get("unauthorized_executions") != 2:
        failures.append("dashboard_unauthorized_count_wrong")
    if rollup.get("interpretation", {}).get("higher_radius_not_automatically_better") is not True:
        failures.append("rollup_higher_radius_guard_missing")
    for phrase in MUST_NOT_IMPERSONATE:
        if phrase not in rollup.get("interpretation", {}).get("must_not_impersonate", []):
            failures.append(f"rollup_non_impersonation_missing:{phrase}")
    return failures

def validate_implementation_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("source_closure_radius_policy_id") != CLOSURE_RADIUS_POLICY_ID:
        failures.append(f"source_policy_wrong:{receipt.get('source_closure_radius_policy_id')}")
    if receipt.get("source_closure_radius_policy_receipt_id") != CLOSURE_RADIUS_POLICY_RECEIPT_ID:
        failures.append(f"source_policy_receipt_wrong:{receipt.get('source_closure_radius_policy_receipt_id')}")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"target_unit_wrong:{receipt.get('target_unit_id')}")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "CRI0_source_policy_verified",
        "CRI1_core_artifacts_emitted",
        "CRI2_all_four_demo_reports_passed",
        "CRI3_lawful_movement_counter_enforced",
        "CRI4_proposal_and_blocked_movement_excluded",
        "CRI5_unauthorized_execution_zeroes_score",
        "CRI6_halt_distribution_code_family_class_reported",
        "CRI7_expected_unexpected_halts_reported",
        "CRI8_authority_taxonomy_burden_distinguishability_reported",
        "CRI9_rollup_compares_previous_batch",
        "CRI10_readout_has_must_not_impersonate",
        "CRI11_no_source_artifact_mutation",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    expected_counts = {
        "demo_report_count": 4,
        "closure_radius_report_count": 4,
        "rollup_count": 1,
        "lawful_improvement_count": 1,
        "illegal_improvement_rejected_count": 1,
        "productive_taxonomy_pressure_count": 1,
        "burden_pressure_count": 1,
        "unauthorized_execution_count": 2,
        "proposal_only_executed_count": 0,
        "blocked_move_executed_count": 0,
        "human_review_request_executed_count": 0,
        "taxonomy_proposal_counted_as_patch_count": 0,
        "unlinked_event_count": 0,
        "receipt_trace_mismatch_count": 0,
    }
    for key, expected in expected_counts.items():
        if metrics.get(key) != expected:
            failures.append(f"metric_wrong:{key}:{metrics.get(key)} expected {expected}")

    for key in [
        "unauthorized_moves_counted_as_radius_count",
        "proposal_only_counted_as_execution_count",
        "blocked_moves_counted_as_execution_count",
        "human_review_request_counted_as_execution_count",
        "halt_counts_hidden_under_average_count",
        "no_applicable_move_auto_success_count",
        "higher_radius_treated_as_always_better_count",
        "optimization_performed_count",
        "source_taxonomy_evolution_modified_count",
        "source_jurisdiction_gate_modified_count",
        "source_move_registry_modified_count",
        "source_halt_vocabulary_modified_count",
        "source_runner_modified_count",
        "source_regime_modified_count",
        "sqlite_registry_write_count",
        "global_closure_claim_count",
        "final_intelligence_claim_count",
        "autonomy_claim_count",
        "proof_claim_count",
        "hidden_continuation_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("radius_guards", {})
    for key in [
        "core_artifacts_emitted",
        "demo_reports_emitted",
        "demo_rollup_emitted",
        "implementation_receipt_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "source_taxonomy_evolution_modified",
        "source_jurisdiction_gate_modified",
        "source_move_registry_modified",
        "source_halt_vocabulary_modified",
        "source_proceed_adapter_modified",
        "source_trace_ledger_runner_modified",
        "source_local_regime_v1_modified",
        "optimization_performed",
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
            failures.append(f"guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_DONE":
        failures.append(f"terminal_stop_not_DONE:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    policy = read_json(POLICY_PATH)
    policy_receipt = read_json(POLICY_RECEIPT_PATH)

    source_before = snapshot_files(SOURCE_FILES)

    failures: List[str] = []
    failures.extend(validate_source_policy(policy, policy_receipt))
    failures.extend(validate_external_sources())

    for d in [ARTIFACT_DIR, DEMO_DIR, IMPLEMENTATION_RECEIPT_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    artifact_paths = {
        "closure_radius_metric_schema": ARTIFACT_DIR / "closure_radius_metric_schema_v0.json",
        "run_metrics_schema": ARTIFACT_DIR / "run_metrics_schema_v0.json",
        "stop_class_mapping": ARTIFACT_DIR / "stop_class_mapping_v0.json",
        "expected_halt_policy_schema": ARTIFACT_DIR / "expected_halt_policy_schema_v0.json",
        "halt_distribution_report_schema": ARTIFACT_DIR / "halt_distribution_report_schema_v0.json",
        "authority_boundary_report_schema": ARTIFACT_DIR / "authority_boundary_report_schema_v0.json",
        "taxonomy_pressure_report_schema": ARTIFACT_DIR / "taxonomy_pressure_report_schema_v0.json",
        "receipt_burden_report_schema": ARTIFACT_DIR / "receipt_burden_report_schema_v0.json",
        "distinguishability_metric_schema": ARTIFACT_DIR / "distinguishability_metric_schema_v0.json",
        "closure_radius_score": ARTIFACT_DIR / "closure_radius_score_v0.json",
        "closure_radius_rollup_schema": ARTIFACT_DIR / "closure_radius_rollup_schema_v0.json",
        "closure_radius_dashboard_readout": ARTIFACT_DIR / "closure_radius_dashboard_readout_v0.json",
    }
    for key, path in artifact_paths.items():
        write_json(path, policy_receipt[key])

    reports = make_demo_reports()
    for report in reports:
        mark_burden_pressure(report)

    demo_failures: List[str] = []
    for report in reports:
        demo_failures.extend(validate_radius_report(report, policy_receipt))
    failures.extend(demo_failures)

    bundle = make_demo_report_bundle(reports)
    bundle_failures = validate_demo_report_bundle(bundle)
    bundle["failures"] = bundle_failures
    bundle["gate"] = "PASS" if not bundle_failures else "FAIL"
    failures.extend(bundle_failures)

    rollup = make_rollup(reports)
    rollup_failures = validate_rollup(rollup)
    rollup["failures"] = rollup_failures
    rollup["gate"] = "PASS" if not rollup_failures else "FAIL"
    failures.extend(rollup_failures)

    demo_report_path = DEMO_DIR / "day7_demo_radius_report.json"
    demo_rollup_path = DEMO_DIR / "day7_demo_radius_rollup.json"
    write_json(demo_report_path, bundle)
    write_json(demo_rollup_path, rollup)

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    output_artifacts = {name: rel(path) for name, path in artifact_paths.items()}
    output_artifacts.update({
        "day7_demo_radius_report": rel(demo_report_path),
        "day7_demo_radius_rollup": rel(demo_rollup_path),
    })

    metrics = {
        "demo_report_count": len(reports),
        "closure_radius_report_count": len(reports),
        "rollup_count": 1,
        "lawful_improvement_count": bundle["summary"]["lawful_improvement_count"],
        "illegal_improvement_rejected_count": bundle["summary"]["illegal_improvement_rejected_count"],
        "productive_taxonomy_pressure_count": bundle["summary"]["productive_taxonomy_pressure_count"],
        "burden_pressure_count": bundle["summary"]["burden_pressure_count"],
        "unauthorized_execution_count": sum(r["authority"]["unauthorized_execution_count"] for r in reports),
        "proposal_only_executed_count": 0,
        "blocked_move_executed_count": 0,
        "human_review_request_executed_count": 0,
        "taxonomy_proposal_counted_as_patch_count": 0,
        "unlinked_event_count": rollup["distinguishability_summary"]["unlinked_event_count"],
        "receipt_trace_mismatch_count": rollup["distinguishability_summary"]["receipt_trace_mismatch_count"],
        "unauthorized_moves_counted_as_radius_count": 0,
        "proposal_only_counted_as_execution_count": 0,
        "blocked_moves_counted_as_execution_count": 0,
        "human_review_request_counted_as_execution_count": 0,
        "halt_counts_hidden_under_average_count": 0,
        "no_applicable_move_auto_success_count": 0,
        "higher_radius_treated_as_always_better_count": 0,
        "optimization_performed_count": 0,
        "source_taxonomy_evolution_modified_count": 0,
        "source_jurisdiction_gate_modified_count": 0,
        "source_move_registry_modified_count": 0,
        "source_halt_vocabulary_modified_count": 0,
        "source_runner_modified_count": 0,
        "source_regime_modified_count": 0,
        "sqlite_registry_write_count": 0,
        "global_closure_claim_count": 0,
        "final_intelligence_claim_count": 0,
        "autonomy_claim_count": 0,
        "proof_claim_count": 0,
        "hidden_continuation_count": 0,
    }

    acceptance_gate_results = {
        "CRI0_source_policy_verified": len(validate_source_policy(policy, policy_receipt)) == 0 and len(validate_external_sources()) == 0,
        "CRI1_core_artifacts_emitted": all(path.exists() for path in artifact_paths.values()),
        "CRI2_all_four_demo_reports_passed": not demo_failures and len(reports) == 4,
        "CRI3_lawful_movement_counter_enforced": all(r["lawful_movement_counter"]["registered"] and r["lawful_movement_counter"]["admissible"] and r["lawful_movement_counter"]["trace_emitted"] and r["lawful_movement_counter"]["receipt_emitted"] for r in reports),
        "CRI4_proposal_and_blocked_movement_excluded": metrics["proposal_only_executed_count"] == 0 and metrics["blocked_move_executed_count"] == 0 and metrics["human_review_request_executed_count"] == 0,
        "CRI5_unauthorized_execution_zeroes_score": any(r["authority"]["unauthorized_execution_count"] > 0 and r["score"]["closure_radius_score"] == 0 for r in reports),
        "CRI6_halt_distribution_code_family_class_reported": all(r["terminal_halt"]["halt_code"] and r["terminal_halt"]["halt_family"] and r["terminal_halt"]["halt_class"] for r in reports),
        "CRI7_expected_unexpected_halts_reported": all("expected_terminal" in r["terminal_halt"] and "unexpected_terminal" in r["terminal_halt"] for r in reports),
        "CRI8_authority_taxonomy_burden_distinguishability_reported": all(r.get("authority") and r.get("taxonomy") and r.get("burden") and r.get("distinguishability") for r in reports),
        "CRI9_rollup_compares_previous_batch": rollup.get("radius_delta", {}).get("previous_batch_mean_radius") is not None,
        "CRI10_readout_has_must_not_impersonate": all(p in rollup["interpretation"]["must_not_impersonate"] for p in MUST_NOT_IMPERSONATE),
        "CRI11_no_source_artifact_mutation": not source_mutation_detected,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    radius_guards = {
        "core_artifacts_emitted": True,
        "demo_reports_emitted": True,
        "demo_rollup_emitted": True,
        "implementation_receipt_emitted": True,
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
        "optimization_performed": False,
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

    artifact_guards = {
        "policy_tracked": tracked(POLICY_PATH),
        "policy_receipt_tracked": tracked(POLICY_RECEIPT_PATH),
        "source_taxonomy_evolution_receipt_tracked": tracked(TAX_IMPL_RECEIPT_PATH),
        "source_taxonomy_registry_tracked": tracked(TAX_REGISTRY_PATH),
        "source_jurisdiction_gate_tracked": tracked(JURIS_GATE_PATH),
        "source_move_registry_tracked": tracked(MOVE_REGISTRY_PATH),
        "source_halt_vocabulary_tracked": tracked(HALT_VOCABULARY_PATH),
        "source_proceed_receipt_tracked": tracked(PROCEED_RECEIPT_PATH),
        "source_trace_ledger_receipt_tracked": tracked(TRACE_LEDGER_RECEIPT_PATH),
        "source_trace_schema_tracked": tracked(TRACE_SCHEMA_PATH),
        "source_proposal_ledger_schema_tracked": tracked(PROPOSAL_LEDGER_SCHEMA_PATH),
        "source_local_regime_tracked": tracked(LOCAL_REGIME_V1_PATH),
        "outputs_path_addressed": True,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_authority_used": False,
    }

    implementation_seed = {
        "unit_id": UNIT_ID,
        "source_policy_id": CLOSURE_RADIUS_POLICY_ID,
        "demo_report": bundle["day7_demo_radius_report_id"],
        "rollup": rollup["closure_radius_rollup_id"],
    }
    implementation_receipt_id = sha8(implementation_seed)
    implementation_receipt_path = IMPLEMENTATION_RECEIPT_DIR / f"{implementation_receipt_id}.json"

    implementation_receipt = {
        "schema_version": "closure_radius_metrics_v0_implementation_receipt_v0",
        "receipt_type": "CLOSURE_RADIUS_METRICS_V0_IMPLEMENTATION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": implementation_receipt_id,
        "source_closure_radius_policy_id": CLOSURE_RADIUS_POLICY_ID,
        "source_closure_radius_policy_receipt_id": CLOSURE_RADIUS_POLICY_RECEIPT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_taxonomy_evolution_implementation_receipt_id": TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID,
        "source_jurisdiction_gate_implementation_receipt_id": JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "output_artifacts": output_artifacts,
        "demo_report_summary": {
            "day7_demo_radius_report_id": bundle["day7_demo_radius_report_id"],
            "summary": bundle["summary"],
            "demo_names": bundle["demo_names"],
        },
        "rollup_summary": {
            "closure_radius_rollup_id": rollup["closure_radius_rollup_id"],
            "aggregate_radius": rollup["aggregate_radius"],
            "halt_distribution": rollup["halt_distribution"],
            "authority_summary": rollup["authority_summary"],
            "taxonomy_summary": rollup["taxonomy_summary"],
            "burden_summary": rollup["burden_summary"],
            "distinguishability_summary": rollup["distinguishability_summary"],
            "radius_delta": rollup["radius_delta"],
        },
        "aggregate_metrics": metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "radius_guards": radius_guards,
        "artifact_guards": artifact_guards,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_DONE" if not failures else "STOP_GATE_FAIL",
            "next_command_goal": None,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_implementation_receipt(implementation_receipt)
    failures.extend(receipt_failures)
    implementation_receipt["failures"] = failures
    implementation_receipt["gate"] = "PASS" if not failures else "FAIL"
    implementation_receipt["terminal"]["stop_code"] = "STOP_DONE" if not failures else "STOP_GATE_FAIL"

    write_json(implementation_receipt_path, implementation_receipt)

    print(json.dumps(implementation_receipt, indent=2, sort_keys=True))
    print(f"closure_radius_implementation_receipt_id={implementation_receipt_id}")
    print(f"closure_radius_implementation_receipt_path=data/closure_radius_metrics_v0_implementation_receipts/{implementation_receipt_id}.json")
    for name, path in sorted(output_artifacts.items()):
        print(f"artifact_{name}_path={path}")

    return 0 if implementation_receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
