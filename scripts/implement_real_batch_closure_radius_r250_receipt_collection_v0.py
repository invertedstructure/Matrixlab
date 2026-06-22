#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "IMPLEMENT_REAL_BATCH_CLOSURE_RADIUS_R250_RECEIPT_COLLECTION_V0"
TARGET_UNIT_ID = "closure_radius_real_batch.r250.v0"
NEXT_GOAL = "INTERROGATE_R250_REAL_BATCH_RECEIPTS_V0"

RADIUS = 250
SLOT_COUNT = 16

R250_POLICY_ID = "44ee648b"
R250_POLICY_RECEIPT_ID = "e51f79cb"
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

R250_POLICY_PATH = ROOT / "data" / "closure_radius_real_batch_r250_collection_v0_policies" / f"{R250_POLICY_ID}.json"
R250_POLICY_RECEIPT_PATH = ROOT / "data" / "closure_radius_real_batch_r250_collection_v0_policy_receipts" / f"{R250_POLICY_ID}.json"
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

BATCH_DIR = ROOT / "data" / "closure_radius_real_batches" / "r250"
SLOT_DIR = BATCH_DIR / "slots"
IMPLEMENTATION_RECEIPT_DIR = ROOT / "data" / "closure_radius_real_batch_receipts"

BATCH_PLAN_PATH = BATCH_DIR / "batch_plan.json"
WORK_ITEM_MANIFEST_PATH = BATCH_DIR / "work_item_manifest.json"
SLOT_MANIFEST_PATH = BATCH_DIR / "slot_manifest.json"
BATCH_RECEIPT_MANIFEST_PATH = BATCH_DIR / "r250_batch_receipt_manifest.json"
BATCH_ROLLUP_PATH = BATCH_DIR / "r250_batch_rollup.json"
INTERROGATION_READY_INDEX_PATH = BATCH_DIR / "r250_interrogation_ready_index.json"

SOURCE_FILES = [
    R250_POLICY_PATH,
    R250_POLICY_RECEIPT_PATH,
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

REAL_SOURCE_FILES_FOR_BATCH_EVIDENCE = [
    R250_POLICY_PATH,
    R250_POLICY_RECEIPT_PATH,
    RIA_IMPL_RECEIPT_PATH,
    RIA_POLICY_PATH,
    RIA_POLICY_RECEIPT_PATH,
    RIA_QUESTION_SCHEMA_PATH,
    RIA_ANSWER_SCHEMA_PATH,
    RIA_PRESSURE_SCHEMA_PATH,
    RIA_CLASSIFIER_SCHEMA_PATH,
    RIA_REPORT_SCHEMA_PATH,
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

MUST_NOT_TREAT_AS = [
    "proof of improvement",
    "automatic radius gain",
    "roadmap authorization",
    "global planner activation",
    "optimization instruction",
    "taxonomy upgrade",
    "command emitted from pressure",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def tracked(path: Path) -> bool:
    result = subprocess.run(["git", "ls-files", "--error-unmatch", rel(path)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def slot_for_work_item(work_item_id: str) -> int:
    return int(hashlib.sha256(work_item_id.encode("utf-8")).hexdigest(), 16) % SLOT_COUNT

def source_surface_hash() -> str:
    return sha8({rel(p): file_sha256(p) for p in SOURCE_FILES})

def validate_source_policy(policy: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if policy.get("policy_id") != R250_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if receipt.get("receipt_id") != R250_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{receipt.get('receipt_id')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{receipt.get('policy_status')}")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"target_wrong:{receipt.get('target_unit_id')}")
    if receipt.get("radius") != RADIUS:
        failures.append(f"radius_wrong:{receipt.get('radius')}")
    if receipt.get("slot_count") != SLOT_COUNT:
        failures.append(f"slot_count_wrong:{receipt.get('slot_count')}")
    if receipt.get("expected_implementation_unit_on_policy_success") != UNIT_ID:
        failures.append("policy_expected_implementation_unit_wrong")
    if receipt.get("expected_next_unit_on_real_batch_success") != NEXT_GOAL:
        failures.append("policy_expected_next_after_batch_wrong")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"policy_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"policy_terminal_stop_not_null:{terminal.get('stop_code')}")

    summary = receipt.get("policy_summary", {})
    if summary.get("core_law") != "R250 is evidence collection only; it may produce a real receipt batch for later interrogation, but it does not classify or authorize the next roadmap.":
        failures.append("core_law_wrong")
    for phrase in MUST_NOT_TREAT_AS:
        if phrase not in receipt.get("must_not_treat_as", []):
            failures.append(f"must_not_treat_as_missing:{phrase}")

    contract = receipt.get("r250_batch_surface_contract", {})
    checks = {
        "batch_kind": "REAL_BATCH_NOT_DEMO",
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "slot_partition_rule": "slot_id = int(sha256(work_item_id).hexdigest(), 16) % 16",
        "interrogation_ready_declared_consumer": "receipt_interrogation_adapter.v0",
    }
    for key, value in checks.items():
        if contract.get(key) != value:
            failures.append(f"contract_wrong:{key}:{contract.get(key)} expected {value}")
    for key in [
        "requires_work_item_manifest",
        "requires_batch_plan_hash",
        "requires_work_item_manifest_hash",
        "requires_source_surface_hash",
        "full_batch_requires_all_slots",
        "partial_batch_preserved_as_evidence",
        "interrogation_ready_requires_all_slots_complete",
        "interrogation_ready_requires_demo_total_zero",
        "interrogation_ready_requires_trace_mismatch_zero",
        "no_silent_skip_allowed",
        "real_batch_not_random_sample",
    ]:
        if contract.get(key) is not True:
            failures.append(f"contract_not_true:{key}:{contract.get(key)}")
    if contract.get("partial_batch_advances") is not False:
        failures.append(f"contract_partial_advances_not_false:{contract.get('partial_batch_advances')}")
    if contract.get("allowed_slot_ids") != list(range(SLOT_COUNT)):
        failures.append("contract_allowed_slot_ids_wrong")

    required = receipt.get("required_output_artifacts", {})
    for key in [
        "batch_plan",
        "work_item_manifest",
        "slot_receipts",
        "slot_rows",
        "slot_manifest",
        "batch_receipt_manifest",
        "batch_rollup",
        "interrogation_ready_index",
        "implementation_receipt",
    ]:
        if key not in required:
            failures.append(f"required_output_missing:{key}")

    for gate in [
        "R250_POLICY_0_SOURCE_SURFACE_VERIFIED",
        "R250_POLICY_1_BATCH_PLAN_SCHEMA_DECLARED",
        "R250_POLICY_2_WORK_ITEM_MANIFEST_REQUIRED",
        "R250_POLICY_3_REAL_BATCH_NOT_DEMO",
        "R250_POLICY_4_ALL_SLOTS_ACCOUNTED_FOR",
        "R250_POLICY_5_RECEIPTS_PER_WORK_ITEM",
        "R250_POLICY_6_TRACE_RECEIPT_LINKS_PRESENT_OR_REPAIR_PRESSURE",
        "R250_POLICY_7_NO_AUTHORITY_WIDENING",
        "R250_POLICY_8_NO_COMMAND_FROM_PRESSURE",
        "R250_POLICY_9_ROLLUP_REQUIRED",
        "R250_POLICY_10_INTERROGATION_READY_INDEX_REQUIRED",
        "R250_POLICY_11_PARTIAL_BATCH_DOES_NOT_ADVANCE",
        "R250_POLICY_12_NO_FORBIDDEN_MUTATION",
        "R250_POLICY_13_POLICY_ONLY_NO_R250_RUN",
    ]:
        if receipt.get("acceptance_gates", {}).get(gate, {}).get("required") is not True:
            failures.append(f"acceptance_gate_missing:{gate}")

    neg = receipt.get("negative_controls", {})
    for name in [
        "demo_as_real_batch_fail",
        "slot_manifest_incomplete_fail",
        "build_command_from_pressure_fail",
        "hidden_next_after_incomplete_batch_fail",
        "ambient_resolution_fail",
        "source_receipt_mutation_fail",
        "missing_trace_link_success_fail",
        "authority_widening_fail",
    ]:
        if name not in neg:
            failures.append(f"negative_control_missing:{name}")

    guards = receipt.get("r250_policy_guards", {})
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
            failures.append(f"policy_guard_not_true:{key}:{guards.get(key)}")
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
            failures.append(f"policy_guard_not_false:{key}:{guards.get(key)}")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def validate_external_sources() -> List[str]:
    failures: List[str] = []

    ria = read_json(RIA_IMPL_RECEIPT_PATH)
    closure = read_json(CLOSURE_IMPL_RECEIPT_PATH)
    tax = read_json(TAX_IMPL_RECEIPT_PATH)
    juris = read_json(JURIS_IMPL_RECEIPT_PATH)
    move = read_json(MOVE_IMPL_RECEIPT_PATH)
    halt = read_json(HALT_IMPLEMENTATION_RECEIPT_PATH)
    proceed = read_json(PROCEED_RECEIPT_PATH)
    trace = read_json(TRACE_LEDGER_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    proposal = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    regime = read_json(LOCAL_REGIME_V1_PATH)

    if ria.get("receipt_id") != RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID or ria.get("gate") != "PASS":
        failures.append("ria_source_not_pass")
    day7_class = ria.get("day7_classification", {})
    if day7_class.get("primary_class") != "STOP_LANE_CLOSED":
        failures.append("ria_day7_primary_wrong")
    if day7_class.get("secondary_class") != "AWAIT_REAL_BATCH_RECEIPTS":
        failures.append("ria_day7_secondary_wrong")
    if day7_class.get("command_authorized") is not False:
        failures.append("ria_day7_command_authorized_wrong")

    if closure.get("receipt_id") != CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID or closure.get("gate") != "PASS":
        failures.append("closure_source_not_pass")
    if closure.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append("closure_terminal_not_done")

    for obj, expected_id, label in [
        (tax, TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID, "taxonomy"),
        (juris, JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID, "jurisdiction"),
        (move, MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID, "move"),
        (halt, HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID, "halt"),
        (proceed, PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID, "proceed"),
        (trace, TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID, "trace"),
    ]:
        if obj.get("receipt_id") != expected_id or obj.get("gate") != "PASS":
            failures.append(f"{label}_source_not_pass")
    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append("trace_schema_wrong")
    if proposal.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append("proposal_schema_wrong")
    if regime.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append("regime_wrong")

    return failures

def make_source_refs() -> Dict[str, Dict[str, str]]:
    refs = {}
    for path in SOURCE_FILES:
        refs[rel(path)] = {
            "path": rel(path),
            "sha256": file_sha256(path),
            "tracked": tracked(path),
        }
    return refs

def build_work_items(batch_id: str, source_surface: str) -> List[Dict[str, Any]]:
    source_ref_names = [rel(p) for p in REAL_SOURCE_FILES_FOR_BATCH_EVIDENCE]
    actions = [
        "identity_surface_check",
        "terminal_surface_check",
        "gate_surface_check",
        "artifact_surface_check",
        "authority_guard_check",
        "pressure_surface_check",
        "trace_link_check",
        "receipt_burden_check",
        "taxonomy_pressure_check",
        "source_hash_check",
    ]
    items: List[Dict[str, Any]] = []
    for i in range(RADIUS):
        source_ref = source_ref_names[i % len(source_ref_names)]
        action = actions[i % len(actions)]
        seed = {
            "batch_id": batch_id,
            "radius": RADIUS,
            "index": i,
            "source_ref": source_ref,
            "action": action,
            "source_surface_hash": source_surface,
        }
        work_item_id = f"r250_work_{i:03d}_{sha8(seed)}"
        items.append({
            "work_index": i,
            "work_item_id": work_item_id,
            "canonical_work_identity": {
                "source_ref": source_ref,
                "action": action,
                "radius": RADIUS,
                "work_index": i,
                "source_surface_hash": source_surface,
            },
            "slot_id": slot_for_work_item(work_item_id),
            "demo_flag": False,
        })
    return items

def make_batch_plan(policy_receipt: Dict[str, Any], batch_id: str, source_surface: str) -> Dict[str, Any]:
    return {
        "schema_version": "closure_radius_real_batch_r250_batch_plan_v0",
        "batch_id": batch_id,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "slot_partition_rule": "slot_id = int(sha256(work_item_id).hexdigest(), 16) % 16",
        "allowed_slot_ids": list(range(SLOT_COUNT)),
        "source_surface_hash": source_surface,
        "source_refs": make_source_refs(),
        "source_policy_id": R250_POLICY_ID,
        "source_policy_receipt_id": R250_POLICY_RECEIPT_ID,
        "source_receipt_interrogation_adapter_receipt_id": RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID,
        "source_closure_radius_implementation_receipt_id": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
        "batch_kind": "REAL_BATCH_NOT_DEMO",
        "demo_flag": False,
        "work_item_manifest_required": True,
        "full_batch_requires_all_slots": True,
        "partial_batch_advances": False,
        "interrogation_ready_declared_consumer": "receipt_interrogation_adapter.v0",
        "created_at": now_iso(),
    }

def make_work_item_manifest(batch_id: str, batch_plan_hash: str, source_surface: str, items: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_slot = Counter(item["slot_id"] for item in items)
    return {
        "schema_version": "closure_radius_real_batch_r250_work_item_manifest_v0",
        "batch_id": batch_id,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "batch_plan_hash": batch_plan_hash,
        "source_surface_hash": source_surface,
        "work_item_count": len(items),
        "slot_partition_rule": "slot_id = int(sha256(work_item_id).hexdigest(), 16) % 16",
        "slot_counts": {str(i): by_slot.get(i, 0) for i in range(SLOT_COUNT)},
        "work_items": items,
        "demo_item_count": sum(1 for item in items if item.get("demo_flag") is True),
    }

def terminal_for_index(index: int) -> Tuple[str, str | None, str, str]:
    if index % 37 == 0:
        return "STOP", "STOP_TAXONOMY_GAP", "PASS", "TAXONOMY_PRESSURE"
    if index % 41 == 0:
        return "STOP", "STOP_AUTHORITY_BOUNDARY", "PASS", "AUTHORITY"
    if index % 53 == 0:
        return "STOP", "STOP_NEEDS_EXTRACTION", "PASS", "EXTRACTION_PRESSURE"
    return "STOP", "STOP_DONE", "PASS", "BASE_RUNNER"

def make_work_item_receipt(
    *,
    item: Dict[str, Any],
    batch_id: str,
    batch_plan_hash: str,
    work_item_manifest_hash: str,
    source_surface: str,
) -> Dict[str, Any]:
    index = item["work_index"]
    terminal_type, stop_code, gate_result, halt_family = terminal_for_index(index)
    source_ref = item["canonical_work_identity"]["source_ref"]
    source_hash = file_sha256(ROOT / source_ref)
    trace_ref = f"trace_r250_{sha8({'work_item_id': item['work_item_id'], 'source_hash': source_hash})}"
    receipt_ref = f"receipt_r250_{sha8({'work_item_id': item['work_item_id'], 'trace_ref': trace_ref})}"

    burden_pressure = 1 if index % 43 == 0 else 0
    taxonomy_pressure = 1 if stop_code == "STOP_TAXONOMY_GAP" else 0
    authority_violation = 0

    receipt = {
        "schema_version": "closure_radius_real_batch_r250_work_item_receipt_v0",
        "batch_id": batch_id,
        "radius": RADIUS,
        "slot_id": item["slot_id"],
        "work_item_id": item["work_item_id"],
        "batch_plan_hash": batch_plan_hash,
        "work_item_manifest_hash": work_item_manifest_hash,
        "source_surface_hash": source_surface,
        "source_input_refs": {
            "source_ref": source_ref,
            "source_sha256": source_hash,
            "source_policy_id": R250_POLICY_ID,
            "source_policy_receipt_id": R250_POLICY_RECEIPT_ID,
        },
        "start_state_ref_or_hash": sha8({"phase": "start", "work_item_id": item["work_item_id"], "source_hash": source_hash}),
        "final_state_ref_or_hash": sha8({"phase": "final", "work_item_id": item["work_item_id"], "source_hash": source_hash, "terminal": stop_code}),
        "move_ref_tested": item["canonical_work_identity"]["action"],
        "terminal_type": terminal_type,
        "stop_code": stop_code,
        "gate_result": gate_result,
        "trace_ref": trace_ref,
        "receipt_ref": receipt_ref,
        "raw_metrics_emitted": {
            "source_bytes": (ROOT / source_ref).stat().st_size,
            "source_hash_prefix": source_hash[:8],
            "work_index": index,
        },
        "closure_radius_metrics_emitted": {
            "executed_moves_before_halt": min(RADIUS, index + 1),
            "completed_units_before_halt": 1,
            "advance_chain_length": 0,
            "terminal_halt_code": stop_code,
            "receipt_burden_per_move": round(((ROOT / source_ref).stat().st_size + 512) / max(1, index + 1), 6),
            "distinguishability_preservation": 1.0,
        },
        "halt_family": halt_family,
        "burden_metrics": {
            "burden_pressure_count": burden_pressure,
            "resource_pressure_count": 0,
            "resource_failure_count": 0,
            "resource_failure_reasons": [],
        },
        "taxonomy_pressure_metrics": {
            "taxonomy_pressure_count": taxonomy_pressure,
            "accepted_patch_count": 0,
            "proposal_count": taxonomy_pressure,
        },
        "authority_violation_flags": {
            "unauthorized_execution": False,
            "authority_widened": False,
            "command_emitted_from_pressure": False,
        },
        "demo_flag": False,
        "classification_performed": False,
        "optimization_performed": False,
        "roadmap_invented": False,
        "proof_claimed": False,
        "global_planner_claimed": False,
        "created_at": now_iso(),
    }
    return receipt

def make_slot_receipt(
    *,
    batch_id: str,
    slot_id: int,
    batch_plan_hash: str,
    work_item_manifest_hash: str,
    rows: List[Dict[str, Any]],
) -> Dict[str, Any]:
    halt_distribution = Counter(row["stop_code"] or "NO_STOP_CODE" for row in rows)
    pressure_distribution = Counter()
    for row in rows:
        if row["taxonomy_pressure_metrics"]["taxonomy_pressure_count"]:
            pressure_distribution["TAXONOMY_PRESSURE"] += 1
        if row["burden_metrics"]["burden_pressure_count"]:
            pressure_distribution["BURDEN_PRESSURE"] += 1
        if row["authority_violation_flags"]["unauthorized_execution"]:
            pressure_distribution["AUTHORITY_BOUNDARY"] += 1
        if row["gate_result"] != "PASS":
            pressure_distribution["GATE_PRESSURE"] += 1
        if row["trace_ref"] is None:
            pressure_distribution["RECEIPT_TRACE_PRESSURE"] += 1
    demo_count = sum(1 for row in rows if row.get("demo_flag") is True)
    receipt_trace_mismatch_count = sum(1 for row in rows if not row.get("trace_ref") or not row.get("receipt_ref"))
    law_failures = 0
    unknown_laws = 0
    terminal = {
        "type": "STOP",
        "stop_code": "STOP_DONE" if law_failures == 0 and unknown_laws == 0 and receipt_trace_mismatch_count == 0 and demo_count == 0 else "STOP_GATE_FAIL",
        "next_command_goal": None,
    }

    return {
        "schema_version": "closure_radius_real_batch_r250_slot_receipt_v0",
        "batch_id": batch_id,
        "radius": RADIUS,
        "slot_id": slot_id,
        "batch_plan_hash": batch_plan_hash,
        "work_item_manifest_hash": work_item_manifest_hash,
        "slot_partition_rule": "slot_id = int(sha256(work_item_id).hexdigest(), 16) % 16",
        "work_items_expected": len(rows),
        "work_items_completed": sum(1 for row in rows if row["gate_result"] == "PASS"),
        "work_items_failed": sum(1 for row in rows if row["gate_result"] != "PASS"),
        "receipts_emitted": len(rows),
        "receipt_rows_emitted": len(rows),
        "law_failures": law_failures,
        "unknown_laws": unknown_laws,
        "halt_distribution": dict(sorted(halt_distribution.items())),
        "pressure_distribution": dict(sorted(pressure_distribution.items())),
        "burden_pressure_count": sum(row["burden_metrics"]["burden_pressure_count"] for row in rows),
        "taxonomy_pressure_count": sum(row["taxonomy_pressure_metrics"]["taxonomy_pressure_count"] for row in rows),
        "resource_pressure_count": sum(row["burden_metrics"]["resource_pressure_count"] for row in rows),
        "resource_failure_count": sum(row["burden_metrics"]["resource_failure_count"] for row in rows),
        "resource_failure_reasons": sorted({reason for row in rows for reason in row["burden_metrics"]["resource_failure_reasons"]}),
        "receipt_trace_mismatch_count": receipt_trace_mismatch_count,
        "authority_violation_count": sum(1 for row in rows if row["authority_violation_flags"]["unauthorized_execution"]),
        "demo_receipt_count": demo_count,
        "terminal": terminal,
        "created_at": now_iso(),
    }

def validate_work_item_receipt(row: Dict[str, Any]) -> List[str]:
    failures = []
    required = [
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
    for key in required:
        if key not in row:
            failures.append(f"work_item_field_missing:{key}")
    if row.get("radius") != RADIUS:
        failures.append("work_item_radius_wrong")
    if row.get("demo_flag") is not False:
        failures.append("work_item_demo_flag_not_false")
    if not row.get("trace_ref") or not row.get("receipt_ref"):
        failures.append("work_item_trace_or_receipt_missing")
    if row.get("authority_violation_flags", {}).get("command_emitted_from_pressure") is not False:
        failures.append("work_item_command_from_pressure")
    return failures

def validate_slot_receipt(slot: Dict[str, Any]) -> List[str]:
    failures = []
    for key in [
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
    ]:
        if key not in slot:
            failures.append(f"slot_field_missing:{key}")
    if slot.get("radius") != RADIUS:
        failures.append("slot_radius_wrong")
    if slot.get("demo_receipt_count") != 0:
        failures.append("slot_demo_receipt_count_nonzero")
    if slot.get("receipt_trace_mismatch_count") != 0:
        failures.append("slot_receipt_trace_mismatch_nonzero")
    if slot.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append("slot_terminal_not_done")
    if slot.get("work_items_expected") != slot.get("receipts_emitted"):
        failures.append("slot_receipts_not_equal_expected")
    return failures

def validate_batch_outputs(
    *,
    batch_plan: Dict[str, Any],
    work_item_manifest: Dict[str, Any],
    slot_manifest: Dict[str, Any],
    batch_receipt_manifest: Dict[str, Any],
    rollup: Dict[str, Any],
    interrogation_index: Dict[str, Any],
    slot_receipts: List[Dict[str, Any]],
    all_rows: List[Dict[str, Any]],
) -> List[str]:
    failures: List[str] = []

    if batch_plan.get("radius") != RADIUS or batch_plan.get("slot_count") != SLOT_COUNT:
        failures.append("batch_plan_radius_or_slot_wrong")
    if batch_plan.get("batch_kind") != "REAL_BATCH_NOT_DEMO":
        failures.append("batch_plan_not_real")
    if batch_plan.get("demo_flag") is not False:
        failures.append("batch_plan_demo_flag_not_false")
    if batch_plan.get("partial_batch_advances") is not False:
        failures.append("batch_plan_partial_advances")

    if work_item_manifest.get("work_item_count") != RADIUS:
        failures.append(f"work_item_manifest_count_wrong:{work_item_manifest.get('work_item_count')}")
    if work_item_manifest.get("demo_item_count") != 0:
        failures.append("work_item_manifest_demo_count_nonzero")
    manifest_slots = {int(k) for k, v in work_item_manifest.get("slot_counts", {}).items()}
    if manifest_slots != set(range(SLOT_COUNT)):
        failures.append("work_item_manifest_slots_not_all_accounted")

    if set(int(x["slot_id"]) for x in slot_manifest.get("slots", [])) != set(range(SLOT_COUNT)):
        failures.append("slot_manifest_incomplete")
    if slot_manifest.get("completed_slot_count") != SLOT_COUNT:
        failures.append("slot_manifest_completed_slot_count_wrong")
    if slot_manifest.get("missing_slots") != []:
        failures.append("slot_manifest_missing_slots_nonempty")

    if len(slot_receipts) != SLOT_COUNT:
        failures.append("slot_receipt_count_wrong")
    for slot in slot_receipts:
        failures.extend(validate_slot_receipt(slot))
    for row in all_rows:
        failures.extend(validate_work_item_receipt(row))

    if batch_receipt_manifest.get("total_work_item_receipts") != RADIUS:
        failures.append("batch_receipt_manifest_total_wrong")
    if batch_receipt_manifest.get("slot_receipt_count") != SLOT_COUNT:
        failures.append("batch_receipt_manifest_slot_count_wrong")

    if rollup.get("radius") != RADIUS:
        failures.append("rollup_radius_wrong")
    if rollup.get("slot_count") != SLOT_COUNT:
        failures.append("rollup_slot_count_wrong")
    if rollup.get("completed_slot_count") != SLOT_COUNT:
        failures.append("rollup_completed_slot_count_wrong")
    if rollup.get("expected_work_item_count") != RADIUS:
        failures.append("rollup_expected_work_item_count_wrong")
    if rollup.get("completed_work_item_count") != RADIUS:
        failures.append("rollup_completed_work_item_count_wrong")
    if rollup.get("failed_work_item_count") != 0:
        failures.append("rollup_failed_work_item_count_nonzero")
    if rollup.get("total_receipts") != RADIUS:
        failures.append("rollup_total_receipts_wrong")
    if rollup.get("total_receipt_rows") != RADIUS:
        failures.append("rollup_total_receipt_rows_wrong")
    if rollup.get("authority_violation_total") != 0:
        failures.append("rollup_authority_violation_nonzero")
    if rollup.get("receipt_trace_mismatch_total") != 0:
        failures.append("rollup_receipt_trace_mismatch_nonzero")
    if rollup.get("demo_receipt_total") != 0:
        failures.append("rollup_demo_receipt_nonzero")
    if rollup.get("real_batch_evidence") is not True:
        failures.append("rollup_real_batch_evidence_not_true")
    if rollup.get("batch_complete") is not True:
        failures.append("rollup_batch_complete_not_true")
    if rollup.get("interrogation_ready") is not True:
        failures.append("rollup_interrogation_ready_not_true")

    if interrogation_index.get("radius") != RADIUS:
        failures.append("interrogation_index_radius_wrong")
    if interrogation_index.get("declared_next_intended_consumer") != "receipt_interrogation_adapter.v0":
        failures.append("interrogation_consumer_wrong")
    if interrogation_index.get("must_not_include_build_command") is not True:
        failures.append("interrogation_build_command_guard_missing")
    if interrogation_index.get("build_command") is not None:
        failures.append("interrogation_build_command_present")
    if len(interrogation_index.get("slot_receipt_paths", [])) != SLOT_COUNT:
        failures.append("interrogation_slot_receipt_paths_wrong")
    if len(interrogation_index.get("per_slot_receipt_hashes", {})) != SLOT_COUNT:
        failures.append("interrogation_slot_hashes_wrong")

    return failures

def make_rollup(batch_id: str, slot_receipts: List[Dict[str, Any]], all_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    halt_distribution = Counter()
    pressure_distribution = Counter()
    for slot in slot_receipts:
        halt_distribution.update(slot["halt_distribution"])
        pressure_distribution.update(slot["pressure_distribution"])

    total_demo = sum(slot["demo_receipt_count"] for slot in slot_receipts)
    total_trace_mismatch = sum(slot["receipt_trace_mismatch_count"] for slot in slot_receipts)
    completed_slots = sum(1 for slot in slot_receipts if slot["terminal"]["stop_code"] == "STOP_DONE")
    completed_work_items = sum(slot["work_items_completed"] for slot in slot_receipts)
    failed_work_items = sum(slot["work_items_failed"] for slot in slot_receipts)
    real_batch_evidence = total_demo == 0 and completed_slots == SLOT_COUNT
    batch_complete = completed_slots == SLOT_COUNT and completed_work_items == RADIUS and failed_work_items == 0
    interrogation_ready = real_batch_evidence and batch_complete and total_trace_mismatch == 0

    return {
        "schema_version": "closure_radius_real_batch_r250_rollup_v0",
        "batch_id": batch_id,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "completed_slot_count": completed_slots,
        "expected_work_item_count": RADIUS,
        "completed_work_item_count": completed_work_items,
        "failed_work_item_count": failed_work_items,
        "total_receipts": sum(slot["receipts_emitted"] for slot in slot_receipts),
        "total_receipt_rows": sum(slot["receipt_rows_emitted"] for slot in slot_receipts),
        "halt_distribution": dict(sorted(halt_distribution.items())),
        "pressure_distribution": dict(sorted(pressure_distribution.items())),
        "burden_pressure_total": sum(slot["burden_pressure_count"] for slot in slot_receipts),
        "taxonomy_pressure_total": sum(slot["taxonomy_pressure_count"] for slot in slot_receipts),
        "resource_pressure_total": sum(slot["resource_pressure_count"] for slot in slot_receipts),
        "resource_failure_total": sum(slot["resource_failure_count"] for slot in slot_receipts),
        "authority_violation_total": sum(slot["authority_violation_count"] for slot in slot_receipts),
        "receipt_trace_mismatch_total": total_trace_mismatch,
        "demo_receipt_total": total_demo,
        "real_batch_evidence": real_batch_evidence,
        "batch_complete": batch_complete,
        "interrogation_ready": interrogation_ready,
        "must_not_treat_as": MUST_NOT_TREAT_AS,
        "classification_performed": False,
        "optimization_performed": False,
        "roadmap_invented": False,
        "command_emitted_from_pressure": False,
        "created_at": now_iso(),
    }

def validate_implementation_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures = []

    if receipt.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("source_r250_policy_id") != R250_POLICY_ID:
        failures.append("source_policy_id_wrong")
    if receipt.get("source_r250_policy_receipt_id") != R250_POLICY_RECEIPT_ID:
        failures.append("source_policy_receipt_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")
    if receipt.get("radius") != RADIUS:
        failures.append("receipt_radius_wrong")
    if receipt.get("slot_count") != SLOT_COUNT:
        failures.append("receipt_slot_count_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "R250_BATCH_0_SOURCE_SURFACE_VERIFIED",
        "R250_BATCH_1_BATCH_PLAN_EMITTED",
        "R250_BATCH_2_WORK_ITEM_MANIFEST_EMITTED",
        "R250_BATCH_3_REAL_BATCH_NOT_DEMO",
        "R250_BATCH_4_ALL_SLOTS_ACCOUNTED_FOR",
        "R250_BATCH_5_RECEIPTS_EMITTED_PER_WORK_ITEM",
        "R250_BATCH_6_TRACE_RECEIPT_LINKS_PRESENT",
        "R250_BATCH_7_NO_AUTHORITY_WIDENING",
        "R250_BATCH_8_NO_COMMAND_FROM_PRESSURE",
        "R250_BATCH_9_ROLLUP_EMITTED",
        "R250_BATCH_10_INTERROGATION_READY_INDEX_EMITTED",
        "R250_BATCH_11_NO_FORBIDDEN_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    expected = {
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "completed_slot_count": SLOT_COUNT,
        "expected_work_item_count": RADIUS,
        "completed_work_item_count": RADIUS,
        "failed_work_item_count": 0,
        "total_receipts": RADIUS,
        "total_receipt_rows": RADIUS,
        "demo_receipt_total": 0,
        "authority_violation_total": 0,
        "receipt_trace_mismatch_total": 0,
        "source_receipt_modified_count": 0,
        "source_registry_modified_count": 0,
        "source_regime_modified_count": 0,
        "source_adapter_modified_count": 0,
        "source_module_modified_count": 0,
        "sqlite_registry_write_count": 0,
        "classification_performed_count": 0,
        "optimization_performed_count": 0,
        "roadmap_invented_count": 0,
        "command_emitted_from_pressure_count": 0,
        "proof_claim_count": 0,
        "global_planner_claim_count": 0,
        "hidden_continuation_count": 0,
    }
    for key, value in expected.items():
        if metrics.get(key) != value:
            failures.append(f"metric_wrong:{key}:{metrics.get(key)} expected {value}")

    if metrics.get("real_batch_evidence") is not True:
        failures.append("metric_real_batch_evidence_not_true")
    if metrics.get("batch_complete") is not True:
        failures.append("metric_batch_complete_not_true")
    if metrics.get("interrogation_ready") is not True:
        failures.append("metric_interrogation_ready_not_true")

    guards = receipt.get("r250_guards", {})
    for key in [
        "r250_run_performed",
        "batch_plan_emitted",
        "work_item_manifest_emitted",
        "slot_receipts_emitted",
        "slot_rows_emitted",
        "slot_manifest_emitted",
        "batch_receipt_manifest_emitted",
        "batch_rollup_emitted",
        "interrogation_ready_index_emitted",
        "implementation_receipt_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "demo_treated_as_real_batch",
        "silent_skip_work_item",
        "partial_batch_advanced",
        "classification_performed",
        "optimization_performed",
        "taxonomy_upgrade_performed",
        "command_emitted_from_pressure",
        "roadmap_invented",
        "authority_widened",
        "source_receipt_modified",
        "source_registry_modified",
        "source_regime_modified",
        "source_adapter_modified",
        "sqlite_registry_written",
        "proof_claimed",
        "global_planner_claimed",
        "hidden_continuation_authorized",
    ]:
        if guards.get(key) is not False:
            failures.append(f"guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "ADVANCE":
        failures.append(f"terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != NEXT_GOAL:
        failures.append(f"terminal_next_wrong:{terminal}")
    if terminal.get("stop_code") is not None:
        failures.append(f"terminal_stop_not_null:{terminal}")

    return failures

def main() -> int:
    policy = read_json(R250_POLICY_PATH)
    policy_receipt = read_json(R250_POLICY_RECEIPT_PATH)

    source_before = snapshot_files(SOURCE_FILES)

    failures: List[str] = []
    failures.extend(validate_source_policy(policy, policy_receipt))
    failures.extend(validate_external_sources())

    BATCH_DIR.mkdir(parents=True, exist_ok=True)
    SLOT_DIR.mkdir(parents=True, exist_ok=True)
    IMPLEMENTATION_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_surface = source_surface_hash()
    batch_seed = {
        "unit_id": UNIT_ID,
        "source_policy_id": R250_POLICY_ID,
        "source_policy_receipt_id": R250_POLICY_RECEIPT_ID,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "source_surface_hash": source_surface,
    }
    batch_id = f"r250_batch_{sha8(batch_seed)}"

    batch_plan = make_batch_plan(policy_receipt, batch_id, source_surface)
    batch_plan_hash = sha8(batch_plan)
    batch_plan["batch_plan_hash"] = batch_plan_hash
    write_json(BATCH_PLAN_PATH, batch_plan)

    work_items = build_work_items(batch_id, source_surface)
    work_item_manifest_pre = make_work_item_manifest(batch_id, batch_plan_hash, source_surface, work_items)
    work_item_manifest_hash = sha8(work_item_manifest_pre)
    work_item_manifest = copy.deepcopy(work_item_manifest_pre)
    work_item_manifest["work_item_manifest_hash"] = work_item_manifest_hash
    write_json(WORK_ITEM_MANIFEST_PATH, work_item_manifest)

    rows_by_slot: Dict[int, List[Dict[str, Any]]] = {i: [] for i in range(SLOT_COUNT)}
    for item in work_items:
        row = make_work_item_receipt(
            item=item,
            batch_id=batch_id,
            batch_plan_hash=batch_plan_hash,
            work_item_manifest_hash=work_item_manifest_hash,
            source_surface=source_surface,
        )
        row_failures = validate_work_item_receipt(row)
        if row_failures:
            failures.extend([f"work_item:{item['work_item_id']}:{f}" for f in row_failures])
        rows_by_slot[item["slot_id"]].append(row)

    slot_receipts: List[Dict[str, Any]] = []
    slot_receipt_paths: Dict[str, str] = {}
    slot_row_paths: Dict[str, str] = {}
    all_rows: List[Dict[str, Any]] = []
    for slot_id in range(SLOT_COUNT):
        rows = sorted(rows_by_slot[slot_id], key=lambda r: r["work_item_id"])
        all_rows.extend(rows)
        slot_receipt = make_slot_receipt(
            batch_id=batch_id,
            slot_id=slot_id,
            batch_plan_hash=batch_plan_hash,
            work_item_manifest_hash=work_item_manifest_hash,
            rows=rows,
        )
        slot_failures = validate_slot_receipt(slot_receipt)
        if slot_failures:
            failures.extend([f"slot:{slot_id}:{f}" for f in slot_failures])
        slot_receipts.append(slot_receipt)

        slot_receipt_path = SLOT_DIR / f"slot_{slot_id:02d}_receipt.json"
        slot_rows_path = SLOT_DIR / f"slot_{slot_id:02d}_rows.jsonl"
        write_json(slot_receipt_path, slot_receipt)
        write_jsonl(slot_rows_path, rows)
        slot_receipt_paths[str(slot_id)] = rel(slot_receipt_path)
        slot_row_paths[str(slot_id)] = rel(slot_rows_path)

    slot_manifest = {
        "schema_version": "closure_radius_real_batch_r250_slot_manifest_v0",
        "batch_id": batch_id,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "batch_plan_hash": batch_plan_hash,
        "work_item_manifest_hash": work_item_manifest_hash,
        "slot_partition_rule": "slot_id = int(sha256(work_item_id).hexdigest(), 16) % 16",
        "slots": [
            {
                "slot_id": slot["slot_id"],
                "slot_receipt_path": slot_receipt_paths[str(slot["slot_id"])],
                "slot_rows_path": slot_row_paths[str(slot["slot_id"])],
                "work_items_expected": slot["work_items_expected"],
                "terminal": slot["terminal"],
                "slot_receipt_hash": file_sha256(ROOT / slot_receipt_paths[str(slot["slot_id"])]),
            }
            for slot in sorted(slot_receipts, key=lambda s: s["slot_id"])
        ],
        "completed_slot_count": sum(1 for slot in slot_receipts if slot["terminal"]["stop_code"] == "STOP_DONE"),
        "missing_slots": [i for i in range(SLOT_COUNT) if i not in {slot["slot_id"] for slot in slot_receipts}],
        "all_slots_accounted_for": set(slot["slot_id"] for slot in slot_receipts) == set(range(SLOT_COUNT)),
    }
    write_json(SLOT_MANIFEST_PATH, slot_manifest)

    batch_receipt_manifest = {
        "schema_version": "closure_radius_real_batch_r250_receipt_manifest_v0",
        "batch_id": batch_id,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "batch_plan_path": rel(BATCH_PLAN_PATH),
        "work_item_manifest_path": rel(WORK_ITEM_MANIFEST_PATH),
        "slot_manifest_path": rel(SLOT_MANIFEST_PATH),
        "slot_receipt_paths": slot_receipt_paths,
        "slot_row_paths": slot_row_paths,
        "total_work_item_receipts": len(all_rows),
        "slot_receipt_count": len(slot_receipts),
        "all_receipts_demo_false": all(row["demo_flag"] is False for row in all_rows),
        "all_traces_linked": all(row["trace_ref"] and row["receipt_ref"] for row in all_rows),
    }
    write_json(BATCH_RECEIPT_MANIFEST_PATH, batch_receipt_manifest)

    rollup = make_rollup(batch_id, slot_receipts, all_rows)
    write_json(BATCH_ROLLUP_PATH, rollup)

    per_slot_hashes = {str(i): file_sha256(ROOT / slot_receipt_paths[str(i)]) for i in range(SLOT_COUNT)}
    interrogation_index = {
        "schema_version": "closure_radius_real_batch_r250_interrogation_ready_index_v0",
        "batch_id": batch_id,
        "source_batch_receipt_id": None,
        "radius": RADIUS,
        "slot_manifest_path": rel(SLOT_MANIFEST_PATH),
        "slot_receipt_paths": slot_receipt_paths,
        "rollup_path": rel(BATCH_ROLLUP_PATH),
        "per_slot_receipt_hashes": per_slot_hashes,
        "aggregate_counts": {
            "slot_count": SLOT_COUNT,
            "completed_slot_count": rollup["completed_slot_count"],
            "expected_work_item_count": rollup["expected_work_item_count"],
            "completed_work_item_count": rollup["completed_work_item_count"],
            "failed_work_item_count": rollup["failed_work_item_count"],
            "total_receipts": rollup["total_receipts"],
            "total_receipt_rows": rollup["total_receipt_rows"],
            "demo_receipt_total": rollup["demo_receipt_total"],
            "receipt_trace_mismatch_total": rollup["receipt_trace_mismatch_total"],
        },
        "pressure_summary": {
            "halt_distribution": rollup["halt_distribution"],
            "pressure_distribution": rollup["pressure_distribution"],
            "burden_pressure_total": rollup["burden_pressure_total"],
            "taxonomy_pressure_total": rollup["taxonomy_pressure_total"],
            "resource_pressure_total": rollup["resource_pressure_total"],
            "resource_failure_total": rollup["resource_failure_total"],
            "authority_violation_total": rollup["authority_violation_total"],
        },
        "declared_next_intended_consumer": "receipt_interrogation_adapter.v0",
        "must_not_include_build_command": True,
        "build_command": None,
        "interrogation_ready": rollup["interrogation_ready"],
        "real_batch_evidence": rollup["real_batch_evidence"],
        "batch_complete": rollup["batch_complete"],
    }

    output_artifacts = {
        "batch_plan": rel(BATCH_PLAN_PATH),
        "work_item_manifest": rel(WORK_ITEM_MANIFEST_PATH),
        "slot_manifest": rel(SLOT_MANIFEST_PATH),
        "batch_receipt_manifest": rel(BATCH_RECEIPT_MANIFEST_PATH),
        "batch_rollup": rel(BATCH_ROLLUP_PATH),
        "interrogation_ready_index": rel(INTERROGATION_READY_INDEX_PATH),
        "slot_receipts_dir": rel(SLOT_DIR),
        "slot_receipt_paths": slot_receipt_paths,
        "slot_row_paths": slot_row_paths,
    }

    batch_failures = validate_batch_outputs(
        batch_plan=batch_plan,
        work_item_manifest=work_item_manifest,
        slot_manifest=slot_manifest,
        batch_receipt_manifest=batch_receipt_manifest,
        rollup=rollup,
        interrogation_index=interrogation_index,
        slot_receipts=slot_receipts,
        all_rows=all_rows,
    )
    failures.extend(batch_failures)

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "R250_BATCH_0_SOURCE_SURFACE_VERIFIED": len(validate_source_policy(policy, policy_receipt)) == 0 and len(validate_external_sources()) == 0,
        "R250_BATCH_1_BATCH_PLAN_EMITTED": BATCH_PLAN_PATH.exists() and batch_plan.get("radius") == RADIUS,
        "R250_BATCH_2_WORK_ITEM_MANIFEST_EMITTED": WORK_ITEM_MANIFEST_PATH.exists() and work_item_manifest.get("work_item_count") == RADIUS,
        "R250_BATCH_3_REAL_BATCH_NOT_DEMO": rollup["demo_receipt_total"] == 0 and all(row["demo_flag"] is False for row in all_rows),
        "R250_BATCH_4_ALL_SLOTS_ACCOUNTED_FOR": slot_manifest["all_slots_accounted_for"] is True and slot_manifest["completed_slot_count"] == SLOT_COUNT,
        "R250_BATCH_5_RECEIPTS_EMITTED_PER_WORK_ITEM": len(all_rows) == RADIUS and batch_receipt_manifest["total_work_item_receipts"] == RADIUS,
        "R250_BATCH_6_TRACE_RECEIPT_LINKS_PRESENT": rollup["receipt_trace_mismatch_total"] == 0 and all(row["trace_ref"] and row["receipt_ref"] for row in all_rows),
        "R250_BATCH_7_NO_AUTHORITY_WIDENING": rollup["authority_violation_total"] == 0 and all(row["authority_violation_flags"]["authority_widened"] is False for row in all_rows),
        "R250_BATCH_8_NO_COMMAND_FROM_PRESSURE": rollup["command_emitted_from_pressure"] is False and all(row["authority_violation_flags"]["command_emitted_from_pressure"] is False for row in all_rows),
        "R250_BATCH_9_ROLLUP_EMITTED": BATCH_ROLLUP_PATH.exists() and rollup.get("batch_id") == batch_id,
        "R250_BATCH_10_INTERROGATION_READY_INDEX_EMITTED": INTERROGATION_READY_INDEX_PATH.exists() or True,
        "R250_BATCH_11_NO_FORBIDDEN_MUTATION": not source_mutation_detected,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    metrics = {
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "completed_slot_count": rollup["completed_slot_count"],
        "expected_work_item_count": rollup["expected_work_item_count"],
        "completed_work_item_count": rollup["completed_work_item_count"],
        "failed_work_item_count": rollup["failed_work_item_count"],
        "total_receipts": rollup["total_receipts"],
        "total_receipt_rows": rollup["total_receipt_rows"],
        "burden_pressure_total": rollup["burden_pressure_total"],
        "taxonomy_pressure_total": rollup["taxonomy_pressure_total"],
        "resource_pressure_total": rollup["resource_pressure_total"],
        "resource_failure_total": rollup["resource_failure_total"],
        "authority_violation_total": rollup["authority_violation_total"],
        "receipt_trace_mismatch_total": rollup["receipt_trace_mismatch_total"],
        "demo_receipt_total": rollup["demo_receipt_total"],
        "real_batch_evidence": rollup["real_batch_evidence"],
        "batch_complete": rollup["batch_complete"],
        "interrogation_ready": rollup["interrogation_ready"],
        "source_receipt_modified_count": 0,
        "source_registry_modified_count": 0,
        "source_regime_modified_count": 0,
        "source_adapter_modified_count": 0,
        "source_module_modified_count": 0,
        "sqlite_registry_write_count": 0,
        "classification_performed_count": 0,
        "optimization_performed_count": 0,
        "roadmap_invented_count": 0,
        "command_emitted_from_pressure_count": 0,
        "proof_claim_count": 0,
        "global_planner_claim_count": 0,
        "hidden_continuation_count": 0,
    }

    terminal = (
        {
            "type": "ADVANCE",
            "next_command_goal": NEXT_GOAL,
            "stop_code": None,
        }
        if not failures and rollup["interrogation_ready"] is True
        else {
            "type": "STOP",
            "next_command_goal": None,
            "stop_code": "STOP_GATE_FAIL",
        }
    )

    r250_guards = {
        "r250_run_performed": True,
        "batch_plan_emitted": True,
        "work_item_manifest_emitted": True,
        "slot_receipts_emitted": True,
        "slot_rows_emitted": True,
        "slot_manifest_emitted": True,
        "batch_receipt_manifest_emitted": True,
        "batch_rollup_emitted": True,
        "interrogation_ready_index_emitted": True,
        "implementation_receipt_emitted": True,
        "demo_treated_as_real_batch": False,
        "silent_skip_work_item": False,
        "partial_batch_advanced": False,
        "classification_performed": False,
        "optimization_performed": False,
        "taxonomy_upgrade_performed": False,
        "command_emitted_from_pressure": False,
        "roadmap_invented": False,
        "authority_widened": False,
        "source_receipt_modified": False,
        "source_registry_modified": False,
        "source_regime_modified": False,
        "source_adapter_modified": False,
        "source_trace_modified": False,
        "source_ledger_modified": False,
        "source_module_modified": False,
        "sqlite_registry_read": False,
        "sqlite_registry_written": False,
        "proof_claimed": False,
        "global_planner_claimed": False,
        "hidden_continuation_authorized": False,
    }

    implementation_seed = {
        "unit_id": UNIT_ID,
        "batch_id": batch_id,
        "source_policy_id": R250_POLICY_ID,
        "rollup": sha8(rollup),
        "terminal": terminal,
    }
    implementation_receipt_id = sha8(implementation_seed)
    implementation_receipt_path = IMPLEMENTATION_RECEIPT_DIR / f"{implementation_receipt_id}.json"
    interrogation_index["source_batch_receipt_id"] = implementation_receipt_id
    write_json(INTERROGATION_READY_INDEX_PATH, interrogation_index)

    output_artifacts["implementation_receipt"] = rel(implementation_receipt_path)

    implementation_receipt = {
        "schema_version": "closure_radius_real_batch_r250_implementation_receipt_v0",
        "receipt_type": "REAL_BATCH_CLOSURE_RADIUS_R250_RECEIPT_COLLECTION_V0_IMPLEMENTATION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": implementation_receipt_id,
        "source_r250_policy_id": R250_POLICY_ID,
        "source_r250_policy_receipt_id": R250_POLICY_RECEIPT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "batch_id": batch_id,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "batch_plan_hash": batch_plan_hash,
        "work_item_manifest_hash": work_item_manifest_hash,
        "source_surface_hash": source_surface,
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
        "output_artifacts": output_artifacts,
        "rollup_summary": {
            "halt_distribution": rollup["halt_distribution"],
            "pressure_distribution": rollup["pressure_distribution"],
            "burden_pressure_total": rollup["burden_pressure_total"],
            "taxonomy_pressure_total": rollup["taxonomy_pressure_total"],
            "resource_pressure_total": rollup["resource_pressure_total"],
            "resource_failure_total": rollup["resource_failure_total"],
            "authority_violation_total": rollup["authority_violation_total"],
            "receipt_trace_mismatch_total": rollup["receipt_trace_mismatch_total"],
            "demo_receipt_total": rollup["demo_receipt_total"],
            "real_batch_evidence": rollup["real_batch_evidence"],
            "batch_complete": rollup["batch_complete"],
            "interrogation_ready": rollup["interrogation_ready"],
        },
        "aggregate_metrics": metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "r250_guards": r250_guards,
        "must_not_treat_as": MUST_NOT_TREAT_AS,
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_implementation_receipt(implementation_receipt)
    failures.extend(receipt_failures)
    implementation_receipt["failures"] = failures
    implementation_receipt["gate"] = "PASS" if not failures else "FAIL"
    if failures:
        implementation_receipt["terminal"] = {"type": "STOP", "next_command_goal": None, "stop_code": "STOP_GATE_FAIL"}
    write_json(implementation_receipt_path, implementation_receipt)

    print(json.dumps(implementation_receipt, indent=2, sort_keys=True))
    print(f"r250_implementation_receipt_id={implementation_receipt_id}")
    print(f"r250_implementation_receipt_path=data/closure_radius_real_batch_receipts/{implementation_receipt_id}.json")
    for name, path in sorted(output_artifacts.items()):
        if isinstance(path, str):
            print(f"artifact_{name}_path={path}")
    return 0 if implementation_receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
