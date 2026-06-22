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

UNIT_ID = "BUILD_REAL_BATCH_CLOSURE_RADIUS_R250_RECEIPT_COLLECTION_V0_POLICY_V0"
NEXT_GOAL = "IMPLEMENT_REAL_BATCH_CLOSURE_RADIUS_R250_RECEIPT_COLLECTION_V0"
EXPECTED_NEXT_AFTER_BATCH_SUCCESS = "INTERROGATE_R250_REAL_BATCH_RECEIPTS_V0"
TARGET_UNIT_ID = "closure_radius_real_batch.r250.v0"

RADIUS = 250
SLOT_COUNT = 16

RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID = "a785297c"
RECEIPT_INTERROGATION_POLICY_ID = "2aa2f2f3"
RECEIPT_INTERROGATION_POLICY_RECEIPT_ID = "0ad557c8"
CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID = "98ab6f11"
CLOSURE_RADIUS_POLICY_ID = "80f2b331"
CLOSURE_RADIUS_POLICY_RECEIPT_ID = "fc82cb0f"
TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID = "6d252e63"
JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID = "6291b0d9"
MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID = "bef08570"
HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID = "75eabbe2"
PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID = "363d2f4a"
TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID = "cc24a11f"
TRACE_SCHEMA_ID = "b4887660"
PROPOSAL_LEDGER_SCHEMA_ID = "eee2a318"
LOCAL_REGIME_V1_HASH = "25802530"

RIA_IMPL_RECEIPT_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_implementation_receipts" / f"{RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID}.json"
RIA_POLICY_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_policies" / f"{RECEIPT_INTERROGATION_POLICY_ID}.json"
RIA_POLICY_RECEIPT_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_policy_receipts" / f"{RECEIPT_INTERROGATION_POLICY_ID}.json"
RIA_QUESTION_SCHEMA_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0" / "receipt_interrogation_question_schema_v0.json"
RIA_ANSWER_SCHEMA_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0" / "receipt_interrogation_answer_schema_v0.json"
RIA_PRESSURE_SCHEMA_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0" / "pressure_classification_schema_v0.json"
RIA_CLASSIFIER_SCHEMA_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0" / "next_command_classifier_schema_v0.json"
RIA_REPORT_SCHEMA_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0" / "receipt_interrogation_report_schema_v0.json"
RIA_DAY7_DEMO_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_demo" / "day7_demo_receipt_interrogation.json"

CLOSURE_IMPL_RECEIPT_PATH = ROOT / "data" / "closure_radius_metrics_v0_implementation_receipts" / f"{CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID}.json"
CLOSURE_POLICY_PATH = ROOT / "data" / "closure_radius_metrics_v0_policies" / f"{CLOSURE_RADIUS_POLICY_ID}.json"
CLOSURE_POLICY_RECEIPT_PATH = ROOT / "data" / "closure_radius_metrics_v0_policy_receipts" / f"{CLOSURE_RADIUS_POLICY_ID}.json"
CLOSURE_METRIC_SCHEMA_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "closure_radius_metric_schema_v0.json"
RUN_METRICS_SCHEMA_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "run_metrics_schema_v0.json"
STOP_CLASS_MAPPING_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "stop_class_mapping_v0.json"
EXPECTED_HALT_POLICY_SCHEMA_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "expected_halt_policy_schema_v0.json"
CLOSURE_RADIUS_SCORE_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "closure_radius_score_v0.json"
CLOSURE_RADIUS_ROLLUP_SCHEMA_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "closure_radius_rollup_schema_v0.json"
CLOSURE_RADIUS_DASHBOARD_READOUT_PATH = ROOT / "data" / "closure_radius_metrics_v0" / "closure_radius_dashboard_readout_v0.json"
DAY7_DEMO_RADIUS_REPORT_PATH = ROOT / "data" / "closure_radius_metrics_v0_demo" / "day7_demo_radius_report.json"
DAY7_DEMO_RADIUS_ROLLUP_PATH = ROOT / "data" / "closure_radius_metrics_v0_demo" / "day7_demo_radius_rollup.json"

TAX_IMPL_RECEIPT_PATH = ROOT / "data" / "taxonomy_evolution_v0_implementation_receipts" / f"{TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID}.json"
JURIS_IMPL_RECEIPT_PATH = ROOT / "data" / "jurisdiction_gate_v0_implementation_receipts" / f"{JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID}.json"
MOVE_IMPL_RECEIPT_PATH = ROOT / "data" / "move_registry_v0_implementation_receipts" / f"{MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID}.json"
HALT_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "halt_vocabulary_v0_implementation_receipts" / f"{HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID}.json"
PROCEED_RECEIPT_PATH = ROOT / "data" / "proceed_adapter_v0_implementation_receipts" / f"{PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID}.json"
TRACE_LEDGER_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts" / f"{TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID}.json"
TRACE_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_schemas" / f"{TRACE_SCHEMA_ID}.json"
PROPOSAL_LEDGER_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposal_ledger_schemas" / f"{PROPOSAL_LEDGER_SCHEMA_ID}.json"
LOCAL_REGIME_V1_PATH = ROOT / "data" / "local_regime_v1_declarations" / f"{LOCAL_REGIME_V1_HASH}.json"

OUT_DIR = ROOT / "data" / "closure_radius_real_batch_r250_collection_v0_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "closure_radius_real_batch_r250_collection_v0_policy_receipts"

SOURCE_FILES = [
    RIA_IMPL_RECEIPT_PATH,
    RIA_POLICY_PATH,
    RIA_POLICY_RECEIPT_PATH,
    RIA_QUESTION_SCHEMA_PATH,
    RIA_ANSWER_SCHEMA_PATH,
    RIA_PRESSURE_SCHEMA_PATH,
    RIA_CLASSIFIER_SCHEMA_PATH,
    RIA_REPORT_SCHEMA_PATH,
    RIA_DAY7_DEMO_PATH,
    CLOSURE_IMPL_RECEIPT_PATH,
    CLOSURE_POLICY_PATH,
    CLOSURE_POLICY_RECEIPT_PATH,
    CLOSURE_METRIC_SCHEMA_PATH,
    RUN_METRICS_SCHEMA_PATH,
    STOP_CLASS_MAPPING_PATH,
    EXPECTED_HALT_POLICY_SCHEMA_PATH,
    CLOSURE_RADIUS_SCORE_PATH,
    CLOSURE_RADIUS_ROLLUP_SCHEMA_PATH,
    CLOSURE_RADIUS_DASHBOARD_READOUT_PATH,
    DAY7_DEMO_RADIUS_REPORT_PATH,
    DAY7_DEMO_RADIUS_ROLLUP_PATH,
    TAX_IMPL_RECEIPT_PATH,
    JURIS_IMPL_RECEIPT_PATH,
    MOVE_IMPL_RECEIPT_PATH,
    HALT_IMPLEMENTATION_RECEIPT_PATH,
    PROCEED_RECEIPT_PATH,
    TRACE_LEDGER_RECEIPT_PATH,
    TRACE_SCHEMA_PATH,
    PROPOSAL_LEDGER_SCHEMA_PATH,
    LOCAL_REGIME_V1_PATH,
]

REQUIRED_OUTPUT_ARTIFACTS = {
    "batch_plan": "data/closure_radius_real_batches/r250/batch_plan.json",
    "work_item_manifest": "data/closure_radius_real_batches/r250/work_item_manifest.json",
    "slot_receipts": "data/closure_radius_real_batches/r250/slots/slot_<00-15>_receipt.json",
    "slot_rows": "data/closure_radius_real_batches/r250/slots/slot_<00-15>_rows.jsonl",
    "slot_manifest": "data/closure_radius_real_batches/r250/slot_manifest.json",
    "batch_receipt_manifest": "data/closure_radius_real_batches/r250/r250_batch_receipt_manifest.json",
    "batch_rollup": "data/closure_radius_real_batches/r250/r250_batch_rollup.json",
    "interrogation_ready_index": "data/closure_radius_real_batches/r250/r250_interrogation_ready_index.json",
    "implementation_receipt": "data/closure_radius_real_batch_receipts/<receipt_id>.json",
}

PER_WORK_ITEM_RECEIPT_MINIMUM = [
    "batch_id",
    "radius",
    "slot_id",
    "work_item_id",
    "batch_plan_hash",
    "work_item_manifest_hash",
    "source_input_refs",
    "start_state_ref_or_hash",
    "final_state_ref_or_hash",
    "move_ref_tested",
    "terminal_type",
    "stop_code",
    "gate_result",
    "trace_ref",
    "receipt_ref",
    "raw_metrics_emitted",
    "closure_radius_metrics_emitted",
    "halt_family",
    "burden_metrics",
    "taxonomy_pressure_metrics",
    "authority_violation_flags",
    "demo_flag",
]

PER_SLOT_RECEIPT_MINIMUM = [
    "batch_id",
    "radius",
    "slot_id",
    "batch_plan_hash",
    "work_item_manifest_hash",
    "slot_partition_rule",
    "work_items_expected",
    "work_items_completed",
    "work_items_failed",
    "receipts_emitted",
    "receipt_rows_emitted",
    "law_failures",
    "unknown_laws",
    "halt_distribution",
    "pressure_distribution",
    "burden_pressure_count",
    "taxonomy_pressure_count",
    "resource_pressure_count",
    "resource_failure_count",
    "resource_failure_reasons",
    "receipt_trace_mismatch_count",
    "authority_violation_count",
    "demo_receipt_count",
    "terminal",
]

BATCH_ROLLUP_MINIMUM = [
    "batch_id",
    "radius",
    "slot_count",
    "completed_slot_count",
    "expected_work_item_count",
    "completed_work_item_count",
    "failed_work_item_count",
    "total_receipts",
    "total_receipt_rows",
    "halt_distribution",
    "pressure_distribution",
    "burden_pressure_total",
    "taxonomy_pressure_total",
    "resource_pressure_total",
    "resource_failure_total",
    "authority_violation_total",
    "receipt_trace_mismatch_total",
    "demo_receipt_total",
    "real_batch_evidence",
    "batch_complete",
    "interrogation_ready",
]

INTERROGATION_READY_INDEX_MINIMUM = [
    "batch_id",
    "source_batch_receipt_id",
    "radius",
    "slot_manifest_path",
    "slot_receipt_paths",
    "rollup_path",
    "per_slot_receipt_hashes",
    "aggregate_counts",
    "pressure_summary",
    "declared_next_intended_consumer",
    "must_not_include_build_command",
]

ACCEPTANCE_GATES = {
    "R250_POLICY_0_SOURCE_SURFACE_VERIFIED": {
        "required": True,
        "description": "All source receipts and policies are loaded by explicit id/path. No latest, mtime, or ambient workspace selection.",
    },
    "R250_POLICY_1_BATCH_PLAN_SCHEMA_DECLARED": {
        "required": True,
        "description": "A deterministic batch plan contract exists with radius 250, slot_count 16, partition rule, source refs, plan hash, and work item manifest hash.",
    },
    "R250_POLICY_2_WORK_ITEM_MANIFEST_REQUIRED": {
        "required": True,
        "description": "A work item manifest is required before slot completion can be trusted.",
    },
    "R250_POLICY_3_REAL_BATCH_NOT_DEMO": {
        "required": True,
        "description": "R250 outputs must have demo flag false; demo artifacts are historical reason only, not evidence.",
    },
    "R250_POLICY_4_ALL_SLOTS_ACCOUNTED_FOR": {
        "required": True,
        "description": "All 16 slot ids must appear in the slot manifest with terminal status.",
    },
    "R250_POLICY_5_RECEIPTS_PER_WORK_ITEM": {
        "required": True,
        "description": "Every work item emits either valid receipt or typed failure receipt.",
    },
    "R250_POLICY_6_TRACE_RECEIPT_LINKS_PRESENT_OR_REPAIR_PRESSURE": {
        "required": True,
        "description": "Missing trace links produce receipt repair pressure, not success.",
    },
    "R250_POLICY_7_NO_AUTHORITY_WIDENING": {
        "required": True,
        "description": "No proof, global closure, optimization authority, global planner status, final roadmap, or authority widening.",
    },
    "R250_POLICY_8_NO_COMMAND_FROM_PRESSURE": {
        "required": True,
        "description": "Pressure metrics may be reported but cannot emit a build command.",
    },
    "R250_POLICY_9_ROLLUP_REQUIRED": {
        "required": True,
        "description": "Batch rollup reports halt, pressure, burden, taxonomy, resource, receipt/trace, and authority totals.",
    },
    "R250_POLICY_10_INTERROGATION_READY_INDEX_REQUIRED": {
        "required": True,
        "description": "An explicit index is emitted so the adapter does not scan arbitrary directories.",
    },
    "R250_POLICY_11_PARTIAL_BATCH_DOES_NOT_ADVANCE": {
        "required": True,
        "description": "Partial completion is preserved as evidence but must not be interrogation_ready=true and must not ADVANCE.",
    },
    "R250_POLICY_12_NO_FORBIDDEN_MUTATION": {
        "required": True,
        "description": "No source receipts, registries, regime, adapter artifacts, or sqlite registry are mutated.",
    },
    "R250_POLICY_13_POLICY_ONLY_NO_R250_RUN": {
        "required": True,
        "description": "This policy unit does not run R250 or emit real slot receipts.",
    },
}

NEGATIVE_CONTROLS = {
    "demo_as_real_batch_fail": "demo receipt treated as real batch evidence must fail",
    "slot_manifest_incomplete_fail": "missing slot from slot manifest must fail",
    "build_command_from_pressure_fail": "pressure directly emitting build command must fail",
    "hidden_next_after_incomplete_batch_fail": "incomplete batch with hidden next command must fail",
    "ambient_resolution_fail": "latest/mtime or ambient path resolution must fail",
    "source_receipt_mutation_fail": "source receipt mutation must fail",
    "missing_trace_link_success_fail": "missing trace link counted as success must fail",
    "authority_widening_fail": "authority/global planner/proof claim must fail",
}

TERMINAL_RULES = {
    "complete_batch": {
        "type": "ADVANCE",
        "next_command_goal": EXPECTED_NEXT_AFTER_BATCH_SUCCESS,
        "stop_code": None,
        "condition": "all acceptance gates pass, all slots complete, all receipts non-demo, receipt_trace_mismatch_total == 0, interrogation_ready == true",
    },
    "incomplete_batch": {
        "type": "STOP",
        "next_command_goal": None,
        "stop_code": "STOP_GATE_FAIL",
        "condition": "batch incomplete or any slot missing/incomplete",
    },
    "source_input_authority_failure": {
        "type": "STOP",
        "next_command_goal": None,
        "stop_code": "STOP_AUTHORITY_VIOLATION",
        "condition": "source/input authority fails",
    },
    "trace_receipt_mismatch": {
        "type": "STOP",
        "next_command_goal": None,
        "stop_code": "STOP_RECEIPT_MISMATCH",
        "condition": "trace/receipt mismatch is detected",
    },
}

POLICY_TERMINAL = {
    "type": "ADVANCE",
    "next_command_goal": NEXT_GOAL,
    "stop_code": None,
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

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def tracked(path: Path) -> bool:
    result = subprocess.run(["git", "ls-files", "--error-unmatch", rel(path)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def validate_inputs() -> List[str]:
    failures: List[str] = []

    ria_impl = read_json(RIA_IMPL_RECEIPT_PATH)
    ria_policy = read_json(RIA_POLICY_PATH)
    ria_policy_receipt = read_json(RIA_POLICY_RECEIPT_PATH)
    closure_impl = read_json(CLOSURE_IMPL_RECEIPT_PATH)
    closure_policy = read_json(CLOSURE_POLICY_PATH)
    closure_policy_receipt = read_json(CLOSURE_POLICY_RECEIPT_PATH)
    tax_impl = read_json(TAX_IMPL_RECEIPT_PATH)
    juris_impl = read_json(JURIS_IMPL_RECEIPT_PATH)
    move_impl = read_json(MOVE_IMPL_RECEIPT_PATH)
    halt_impl = read_json(HALT_IMPLEMENTATION_RECEIPT_PATH)
    proceed = read_json(PROCEED_RECEIPT_PATH)
    trace = read_json(TRACE_LEDGER_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    proposal_schema = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    regime = read_json(LOCAL_REGIME_V1_PATH)
    day7_demo = read_json(RIA_DAY7_DEMO_PATH)

    if ria_impl.get("receipt_id") != RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID or ria_impl.get("gate") != "PASS":
        failures.append("receipt_interrogation_implementation_source_not_pass")
    if ria_impl.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append("receipt_interrogation_implementation_terminal_not_done")
    day7_class = ria_impl.get("day7_classification", {})
    if day7_class.get("primary_class") != "STOP_LANE_CLOSED":
        failures.append("ria_day7_primary_class_not_stop_lane_closed")
    if day7_class.get("secondary_class") != "AWAIT_REAL_BATCH_RECEIPTS":
        failures.append("ria_day7_secondary_not_await_real_batch")
    if day7_class.get("command_authorized") is not False:
        failures.append("ria_day7_command_authorized_unexpected")
    if ria_impl.get("aggregate_metrics", {}).get("build_command_from_pressure_count") != 0:
        failures.append("ria_build_command_from_pressure_nonzero")

    if ria_policy.get("policy_id") != RECEIPT_INTERROGATION_POLICY_ID:
        failures.append("ria_policy_id_wrong")
    if ria_policy_receipt.get("receipt_id") != RECEIPT_INTERROGATION_POLICY_RECEIPT_ID:
        failures.append("ria_policy_receipt_id_wrong")
    if "AWAIT_REAL_BATCH_RECEIPTS" not in ria_policy_receipt.get("next_command_classifier_schema", {}).get("next_command_classes", []):
        failures.append("ria_policy_missing_await_real_batch")
    if day7_demo.get("summary", {}).get("await_real_batch_count") != 1:
        failures.append("ria_day7_demo_await_count_wrong")

    if closure_impl.get("receipt_id") != CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID or closure_impl.get("gate") != "PASS":
        failures.append("closure_radius_implementation_source_not_pass")
    if closure_impl.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append("closure_radius_terminal_not_done")
    if closure_policy.get("policy_id") != CLOSURE_RADIUS_POLICY_ID:
        failures.append("closure_policy_id_wrong")
    if closure_policy_receipt.get("receipt_id") != CLOSURE_RADIUS_POLICY_RECEIPT_ID:
        failures.append("closure_policy_receipt_id_wrong")
    closure_metrics = closure_impl.get("aggregate_metrics", {})
    if closure_metrics.get("demo_report_count") != 4:
        failures.append("closure_metrics_demo_count_wrong")
    if closure_metrics.get("lawful_improvement_count") != 1:
        failures.append("closure_metrics_lawful_improvement_count_wrong")
    if closure_metrics.get("productive_taxonomy_pressure_count") != 1:
        failures.append("closure_metrics_productive_taxonomy_pressure_count_wrong")
    if closure_metrics.get("burden_pressure_count") != 1:
        failures.append("closure_metrics_burden_pressure_count_wrong")

    for obj, expected_id, label in [
        (tax_impl, TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID, "taxonomy"),
        (juris_impl, JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID, "jurisdiction"),
        (move_impl, MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID, "move_registry"),
        (halt_impl, HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID, "halt_vocabulary"),
        (proceed, PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID, "proceed"),
        (trace, TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID, "trace_ledger"),
    ]:
        if obj.get("receipt_id") != expected_id or obj.get("gate") != "PASS":
            failures.append(f"{label}_source_not_pass")
    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append("trace_schema_wrong")
    if proposal_schema.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append("proposal_schema_wrong")
    if regime.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append("local_regime_wrong")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def validate_batch_surface_contract(contract: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if contract.get("radius") != RADIUS:
        failures.append(f"radius_wrong:{contract.get('radius')}")
    if contract.get("slot_count") != SLOT_COUNT:
        failures.append(f"slot_count_wrong:{contract.get('slot_count')}")
    if contract.get("allowed_slot_ids") != list(range(SLOT_COUNT)):
        failures.append("allowed_slot_ids_wrong")
    if contract.get("slot_partition_rule") != "slot_id = int(sha256(work_item_id).hexdigest(), 16) % 16":
        failures.append("slot_partition_rule_wrong")
    if contract.get("batch_kind") != "REAL_BATCH_NOT_DEMO":
        failures.append("batch_kind_wrong")
    if contract.get("requires_work_item_manifest") is not True:
        failures.append("work_item_manifest_not_required")
    if contract.get("full_batch_requires_all_slots") is not True:
        failures.append("full_batch_all_slots_not_required")
    if contract.get("partial_batch_advances") is not False:
        failures.append("partial_batch_advances_not_false")
    if contract.get("interrogation_ready_requires_all_slots_complete") is not True:
        failures.append("interrogation_ready_all_slots_not_required")
    if contract.get("interrogation_ready_requires_demo_total_zero") is not True:
        failures.append("interrogation_ready_demo_zero_not_required")
    if contract.get("interrogation_ready_requires_trace_mismatch_zero") is not True:
        failures.append("interrogation_ready_trace_zero_not_required")

    return failures

def validate_policy(policy: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append("policy_status_wrong")
    if policy.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("policy_target_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("receipt_target_wrong")

    summary = policy.get("policy_summary", {})
    if summary.get("core_law") != "R250 is evidence collection only; it may produce a real receipt batch for later interrogation, but it does not classify or authorize the next roadmap.":
        failures.append("core_law_wrong")
    for phrase in [
        "proof of improvement",
        "automatic radius gain",
        "roadmap authorization",
        "global planner activation",
        "optimization instruction",
        "taxonomy upgrade",
        "command emitted from pressure",
    ]:
        if phrase not in policy.get("must_not_treat_as", []):
            failures.append(f"must_not_treat_as_missing:{phrase}")

    failures.extend(validate_batch_surface_contract(policy.get("r250_batch_surface_contract", {})))

    for name, path in REQUIRED_OUTPUT_ARTIFACTS.items():
        if policy.get("required_output_artifacts", {}).get(name) != path:
            failures.append(f"required_output_artifact_wrong:{name}:{policy.get('required_output_artifacts', {}).get(name)}")

    for field in PER_WORK_ITEM_RECEIPT_MINIMUM:
        if field not in policy.get("per_work_item_receipt_minimum", []):
            failures.append(f"per_work_item_field_missing:{field}")
    for field in PER_SLOT_RECEIPT_MINIMUM:
        if field not in policy.get("per_slot_receipt_minimum", []):
            failures.append(f"per_slot_field_missing:{field}")
    for field in BATCH_ROLLUP_MINIMUM:
        if field not in policy.get("batch_rollup_minimum", []):
            failures.append(f"batch_rollup_field_missing:{field}")
    for field in INTERROGATION_READY_INDEX_MINIMUM:
        if field not in policy.get("interrogation_ready_index_minimum", []):
            failures.append(f"interrogation_index_field_missing:{field}")

    terminal_rules = policy.get("terminal_rules", {})
    if terminal_rules.get("complete_batch", {}).get("next_command_goal") != EXPECTED_NEXT_AFTER_BATCH_SUCCESS:
        failures.append("complete_batch_next_goal_wrong")
    if terminal_rules.get("incomplete_batch", {}).get("stop_code") != "STOP_GATE_FAIL":
        failures.append("incomplete_batch_stop_wrong")
    if terminal_rules.get("source_input_authority_failure", {}).get("stop_code") != "STOP_AUTHORITY_VIOLATION":
        failures.append("authority_failure_stop_wrong")
    if terminal_rules.get("trace_receipt_mismatch", {}).get("stop_code") != "STOP_RECEIPT_MISMATCH":
        failures.append("trace_mismatch_stop_wrong")

    gates = policy.get("acceptance_gates", {})
    for gate in ACCEPTANCE_GATES:
        if gates.get(gate, {}).get("required") is not True:
            failures.append(f"acceptance_gate_missing:{gate}")

    neg = policy.get("negative_controls", {})
    for name in NEGATIVE_CONTROLS:
        if name not in neg:
            failures.append(f"negative_control_missing:{name}")

    guards = policy.get("r250_policy_guards", {})
    for key in [
        "policy_built",
        "source_receipt_interrogation_adapter_consumed",
        "source_closure_radius_metrics_consumed",
        "source_taxonomy_evolution_consumed",
        "source_jurisdiction_gate_consumed",
        "source_move_registry_consumed",
        "source_halt_vocabulary_consumed",
        "source_proceed_adapter_consumed",
        "source_trace_ledger_surface_consumed",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "r250_run_performed_by_policy",
        "slot_receipts_emitted_by_policy",
        "real_batch_rollup_emitted_by_policy",
        "interrogation_ready_index_emitted_by_policy",
        "classification_performed_by_policy",
        "optimization_performed_by_policy",
        "taxonomy_upgrade_performed_by_policy",
        "command_emitted_from_pressure_by_policy",
        "roadmap_invented_by_policy",
        "authority_widened_by_policy",
        "source_receipt_modified",
        "source_registry_modified",
        "source_regime_modified",
        "source_adapter_modified",
        "sqlite_registry_written",
        "global_planner_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
    ]:
        if guards.get(key) is not False:
            failures.append(f"guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal", {})
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
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "source_ria_impl": RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID,
        "source_closure_impl": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
        "next_goal": NEXT_GOAL,
    }
    policy_id = sha8(policy_seed)

    r250_policy_guards = {
        "policy_built": True,
        "source_receipt_interrogation_adapter_consumed": True,
        "source_closure_radius_metrics_consumed": True,
        "source_taxonomy_evolution_consumed": True,
        "source_jurisdiction_gate_consumed": True,
        "source_move_registry_consumed": True,
        "source_halt_vocabulary_consumed": True,
        "source_proceed_adapter_consumed": True,
        "source_trace_ledger_surface_consumed": True,
        "r250_run_performed_by_policy": False,
        "slot_receipts_emitted_by_policy": False,
        "real_batch_rollup_emitted_by_policy": False,
        "interrogation_ready_index_emitted_by_policy": False,
        "classification_performed_by_policy": False,
        "optimization_performed_by_policy": False,
        "taxonomy_upgrade_performed_by_policy": False,
        "command_emitted_from_pressure_by_policy": False,
        "roadmap_invented_by_policy": False,
        "authority_widened_by_policy": False,
        "source_receipt_modified": False,
        "source_registry_modified": False,
        "source_regime_modified": False,
        "source_adapter_modified": False,
        "source_trace_modified": False,
        "source_ledger_modified": False,
        "source_module_modified": False,
        "sqlite_registry_read": False,
        "sqlite_registry_written": False,
        "global_planner_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
    }

    policy = {
        "schema_version": "real_batch_closure_radius_r250_receipt_collection_v0_policy_v0",
        "policy_type": "REAL_BATCH_CLOSURE_RADIUS_R250_RECEIPT_COLLECTION_V0_POLICY",
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "target_unit_id": TARGET_UNIT_ID,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "expected_implementation_unit_on_policy_success": NEXT_GOAL,
        "expected_next_unit_on_real_batch_success": EXPECTED_NEXT_AFTER_BATCH_SUCCESS,
        "source_receipt_interrogation_adapter_receipt_id": RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID,
        "source_receipt_interrogation_policy_id": RECEIPT_INTERROGATION_POLICY_ID,
        "source_receipt_interrogation_policy_receipt_id": RECEIPT_INTERROGATION_POLICY_RECEIPT_ID,
        "source_closure_radius_implementation_receipt_id": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
        "source_closure_radius_policy_id": CLOSURE_RADIUS_POLICY_ID,
        "source_closure_radius_policy_receipt_id": CLOSURE_RADIUS_POLICY_RECEIPT_ID,
        "source_taxonomy_evolution_implementation_receipt_id": TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID,
        "source_jurisdiction_gate_implementation_receipt_id": JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": {
            "purpose": "Freeze the lawful contract for collecting real radius-250 closure-radius receipt evidence.",
            "core_law": "R250 is evidence collection only; it may produce a real receipt batch for later interrogation, but it does not classify or authorize the next roadmap.",
            "non_goal": "no R250 run in policy, no classification, no optimization, no roadmap inference, no authority widening, no taxonomy upgrade, no command emitted from pressure",
            "current_reason": "Receipt interrogation adapter classified Day 7 as STOP_LANE_CLOSED plus AWAIT_REAL_BATCH_RECEIPTS.",
        },
        "must_not_treat_as": [
            "proof of improvement",
            "automatic radius gain",
            "roadmap authorization",
            "global planner activation",
            "optimization instruction",
            "taxonomy upgrade",
            "command emitted from pressure",
        ],
        "r250_batch_surface_contract": {
            "schema_version": "r250_batch_surface_contract_v0",
            "batch_kind": "REAL_BATCH_NOT_DEMO",
            "radius": RADIUS,
            "slot_count": SLOT_COUNT,
            "allowed_slot_ids": list(range(SLOT_COUNT)),
            "slot_partition_rule": "slot_id = int(sha256(work_item_id).hexdigest(), 16) % 16",
            "requires_work_item_manifest": True,
            "requires_batch_plan_hash": True,
            "requires_work_item_manifest_hash": True,
            "requires_source_surface_hash": True,
            "full_batch_requires_all_slots": True,
            "partial_batch_preserved_as_evidence": True,
            "partial_batch_advances": False,
            "interrogation_ready_requires_all_slots_complete": True,
            "interrogation_ready_requires_demo_total_zero": True,
            "interrogation_ready_requires_trace_mismatch_zero": True,
            "interrogation_ready_declared_consumer": "receipt_interrogation_adapter.v0",
            "no_silent_skip_allowed": True,
            "real_batch_not_random_sample": True,
        },
        "required_output_artifacts": REQUIRED_OUTPUT_ARTIFACTS,
        "per_work_item_receipt_minimum": PER_WORK_ITEM_RECEIPT_MINIMUM,
        "per_slot_receipt_minimum": PER_SLOT_RECEIPT_MINIMUM,
        "batch_rollup_minimum": BATCH_ROLLUP_MINIMUM,
        "interrogation_ready_index_minimum": INTERROGATION_READY_INDEX_MINIMUM,
        "terminal_rules": TERMINAL_RULES,
        "acceptance_gates": ACCEPTANCE_GATES,
        "negative_controls": NEGATIVE_CONTROLS,
        "authorized_operations_next": {
            "read_r250_policy": True,
            "read_r250_policy_receipt": True,
            "write_batch_plan": True,
            "write_work_item_manifest": True,
            "write_slot_rows": True,
            "write_slot_receipts": True,
            "write_slot_manifest": True,
            "write_batch_receipt_manifest": True,
            "write_batch_rollup": True,
            "write_interrogation_ready_index": True,
            "emit_implementation_receipt": True,
            "run_r250_batch_deterministically": True,
        },
        "forbidden_operations_next": {
            "classify_batch_result": True,
            "optimize_runner": True,
            "widen_authority": True,
            "upgrade_taxonomy": True,
            "emit_build_command_from_pressure": True,
            "invent_roadmap": True,
            "treat_demo_as_real_batch": True,
            "silent_skip_work_item": True,
            "advance_partial_batch": True,
            "mark_interrogation_ready_with_missing_slot": True,
            "mark_interrogation_ready_with_demo_receipts": True,
            "mark_interrogation_ready_with_trace_mismatch": True,
            "latest_or_mtime_selection": True,
            "ambient_workspace_authority": True,
            "mutate_source_receipts": True,
            "mutate_source_registries": True,
            "mutate_source_regime": True,
            "mutate_source_adapter_artifacts": True,
            "sqlite_registry_write": True,
            "claim_proof": True,
            "claim_global_closure": True,
            "claim_global_planner": True,
            "claim_final_roadmap": True,
            "hidden_continuation_after_terminal": True,
        },
        "safety_clauses": {
            "policy_only": True,
            "does_not_run_r250": True,
            "does_not_emit_slot_receipts": True,
            "does_not_emit_real_batch_rollup": True,
            "does_not_emit_interrogation_ready_index": True,
            "does_not_classify_result": True,
            "does_not_optimize": True,
            "does_not_widen_authority": True,
            "does_not_invent_roadmap": True,
            "does_not_upgrade_taxonomy": True,
            "does_not_modify_source_artifacts": True,
            "next_unit_required_for_implementation": True,
        },
        "r250_policy_guards": r250_policy_guards,
        "terminal": POLICY_TERMINAL,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "policy_id": policy_id,
        "target_unit_id": TARGET_UNIT_ID,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "terminal": POLICY_TERMINAL,
    }
    receipt_id = sha8(receipt_seed)
    policy["policy_receipt_id"] = receipt_id

    receipt = {
        "schema_version": "real_batch_closure_radius_r250_receipt_collection_v0_policy_receipt_v0",
        "receipt_type": "REAL_BATCH_CLOSURE_RADIUS_R250_RECEIPT_COLLECTION_V0_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "target_unit_id": TARGET_UNIT_ID,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "expected_implementation_unit_on_policy_success": NEXT_GOAL,
        "expected_next_unit_on_real_batch_success": EXPECTED_NEXT_AFTER_BATCH_SUCCESS,
        "source_receipt_interrogation_adapter_receipt_id": RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID,
        "source_receipt_interrogation_policy_id": RECEIPT_INTERROGATION_POLICY_ID,
        "source_receipt_interrogation_policy_receipt_id": RECEIPT_INTERROGATION_POLICY_RECEIPT_ID,
        "source_closure_radius_implementation_receipt_id": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
        "source_closure_radius_policy_id": CLOSURE_RADIUS_POLICY_ID,
        "source_closure_radius_policy_receipt_id": CLOSURE_RADIUS_POLICY_RECEIPT_ID,
        "source_taxonomy_evolution_implementation_receipt_id": TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID,
        "source_jurisdiction_gate_implementation_receipt_id": JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID,
        "source_move_registry_implementation_receipt_id": MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "policy_summary": policy["policy_summary"],
        "must_not_treat_as": policy["must_not_treat_as"],
        "r250_batch_surface_contract": policy["r250_batch_surface_contract"],
        "required_output_artifacts": REQUIRED_OUTPUT_ARTIFACTS,
        "per_work_item_receipt_minimum": PER_WORK_ITEM_RECEIPT_MINIMUM,
        "per_slot_receipt_minimum": PER_SLOT_RECEIPT_MINIMUM,
        "batch_rollup_minimum": BATCH_ROLLUP_MINIMUM,
        "interrogation_ready_index_minimum": INTERROGATION_READY_INDEX_MINIMUM,
        "terminal_rules": TERMINAL_RULES,
        "acceptance_gates": ACCEPTANCE_GATES,
        "negative_controls": NEGATIVE_CONTROLS,
        "authorized_operations_next": policy["authorized_operations_next"],
        "forbidden_operations_next": policy["forbidden_operations_next"],
        "safety_clauses": policy["safety_clauses"],
        "r250_policy_guards": r250_policy_guards,
        "terminal": POLICY_TERMINAL,
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
    print(f"r250_policy_id={policy['policy_id']}")
    print(f"r250_policy_receipt_id={receipt['receipt_id']}")
    print(f"r250_policy_path=data/closure_radius_real_batch_r250_collection_v0_policies/{policy['policy_id']}.json")
    print(f"r250_policy_receipt_path=data/closure_radius_real_batch_r250_collection_v0_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
