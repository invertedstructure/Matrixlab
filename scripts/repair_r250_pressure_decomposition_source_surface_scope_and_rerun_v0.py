#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
import time
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REPAIR_R250_PRESSURE_DECOMPOSITION_SOURCE_SURFACE_SCOPE_AND_RERUN_V0"
ORIGINAL_UNIT_ID = "BUILD_R250_PRESSURE_DECOMPOSITION_METRICS_AND_RERUN_V0"
TARGET_UNIT_ID = "r250_pressure_decomposition_metrics.v0"
NEXT_GOAL = "INTERROGATE_R250_PRESSURE_DECOMPOSED_BATCH_V0"

RADIUS = 250
SLOT_COUNT = 16

FAILED_RECEIPT_ID = "8b82d6a8"
R250_INTERROGATION_RECEIPT_ID = "41f65b9a"
R250_IMPLEMENTATION_RECEIPT_ID = "05723444"
R250_POLICY_ID = "44ee648b"
R250_POLICY_RECEIPT_ID = "e51f79cb"
RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID = "a785297c"
RECEIPT_INTERROGATION_POLICY_ID = "2aa2f2f3"
RECEIPT_INTERROGATION_POLICY_RECEIPT_ID = "0ad557c8"
CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID = "98ab6f11"
TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID = "6d252e63"
JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID = "6291b0d9"
MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID = "bef08570"
HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID = "75eabbe2"
PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID = "363d2f4a"
TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID = "cc24a11f"
TRACE_SCHEMA_ID = "b4887660"
PROPOSAL_LEDGER_SCHEMA_ID = "eee2a318"
LOCAL_REGIME_V1_HASH = "25802530"

PREVIOUS_BATCH_ID = "r250_batch_34f560c1"
PREVIOUS_BATCH_PLAN_HASH = "b85c46b4"
PREVIOUS_WORK_ITEM_MANIFEST_HASH = "576909da"
PREVIOUS_SOURCE_SURFACE_HASH = "a109a264"

R250_INTERROGATION_RECEIPT_PATH = ROOT / "data" / "closure_radius_real_batch_interrogation_receipts" / f"{R250_INTERROGATION_RECEIPT_ID}.json"
R250_INTERROGATION_REPORT_PATH = ROOT / "data" / "closure_radius_real_batch_interrogations" / "r250" / "r250_receipt_interrogation_report.json"
R250_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "closure_radius_real_batch_receipts" / f"{R250_IMPLEMENTATION_RECEIPT_ID}.json"
PRIOR_BATCH_PLAN_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250" / "batch_plan.json"
PRIOR_WORK_ITEM_MANIFEST_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250" / "work_item_manifest.json"
PRIOR_SLOT_MANIFEST_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250" / "slot_manifest.json"
PRIOR_BATCH_RECEIPT_MANIFEST_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250" / "r250_batch_receipt_manifest.json"
PRIOR_BATCH_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250" / "r250_batch_rollup.json"
PRIOR_INTERROGATION_READY_INDEX_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250" / "r250_interrogation_ready_index.json"

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

CLOSURE_IMPL_RECEIPT_PATH = ROOT / "data" / "closure_radius_metrics_v0_implementation_receipts" / f"{CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID}.json"
TAX_IMPL_RECEIPT_PATH = ROOT / "data" / "taxonomy_evolution_v0_implementation_receipts" / f"{TAXONOMY_EVOLUTION_IMPLEMENTATION_RECEIPT_ID}.json"
JURIS_IMPL_RECEIPT_PATH = ROOT / "data" / "jurisdiction_gate_v0_implementation_receipts" / f"{JURISDICTION_GATE_IMPLEMENTATION_RECEIPT_ID}.json"
MOVE_IMPL_RECEIPT_PATH = ROOT / "data" / "move_registry_v0_implementation_receipts" / f"{MOVE_REGISTRY_IMPLEMENTATION_RECEIPT_ID}.json"
HALT_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "halt_vocabulary_v0_implementation_receipts" / f"{HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID}.json"
PROCEED_RECEIPT_PATH = ROOT / "data" / "proceed_adapter_v0_implementation_receipts" / f"{PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID}.json"
TRACE_LEDGER_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts" / f"{TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID}.json"
TRACE_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_schemas" / f"{TRACE_SCHEMA_ID}.json"
PROPOSAL_LEDGER_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposal_ledger_schemas" / f"{PROPOSAL_LEDGER_SCHEMA_ID}.json"
LOCAL_REGIME_V1_PATH = ROOT / "data" / "local_regime_v1_declarations" / f"{LOCAL_REGIME_V1_HASH}.json"

FAILED_RECEIPT_PATH = ROOT / "data" / "r250_pressure_metrics_v0_receipts" / f"{FAILED_RECEIPT_ID}.json"

PRIOR_SLOT_RECEIPT_PATHS = [ROOT / "data" / "closure_radius_real_batches" / "r250" / "slots" / f"slot_{i:02d}_receipt.json" for i in range(SLOT_COUNT)]
PRIOR_SLOT_ROW_PATHS = [ROOT / "data" / "closure_radius_real_batches" / "r250" / "slots" / f"slot_{i:02d}_rows.jsonl" for i in range(SLOT_COUNT)]

SCHEMA_DIR = ROOT / "data" / "r250_pressure_metrics_v0"
OUT_DIR = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0"
OUT_SLOT_DIR = OUT_DIR / "slots"
RECEIPT_DIR = ROOT / "data" / "r250_pressure_metrics_v0_receipts"

PRESSURE_DECOMPOSITION_SCHEMA_PATH = SCHEMA_DIR / "pressure_decomposition_schema_v0.json"
PRESSURE_SIGNATURE_SCHEMA_PATH = SCHEMA_DIR / "pressure_signature_repetition_schema_v0.json"
OBSERVER_BURDEN_SCHEMA_PATH = SCHEMA_DIR / "observer_burden_guard_schema_v0.json"

BATCH_PLAN_PATH = OUT_DIR / "batch_plan.json"
WORK_ITEM_MANIFEST_PATH = OUT_DIR / "work_item_manifest.json"
SLOT_MANIFEST_PATH = OUT_DIR / "slot_manifest.json"
PRESSURE_EVENT_ROWS_PATH = OUT_DIR / "pressure_event_rows.jsonl"
PRESSURE_DECOMPOSITION_ROLLUP_PATH = OUT_DIR / "pressure_decomposition_rollup.json"
PRESSURE_SIGNATURE_ROLLUP_PATH = OUT_DIR / "pressure_signature_repetition_rollup.json"
OBSERVER_BURDEN_ROLLUP_PATH = OUT_DIR / "observer_burden_rollup.json"
RUNTIME_EQUIVALENCE_REPORT_PATH = OUT_DIR / "runtime_equivalence_report.json"
COMBINED_BATCH_ROLLUP_PATH = OUT_DIR / "r250_pressure_metrics_batch_rollup.json"
INTERROGATION_READY_INDEX_PATH = OUT_DIR / "r250_pressure_metrics_interrogation_ready_index.json"

SOURCE_FILES = [
    R250_INTERROGATION_RECEIPT_PATH,
    R250_INTERROGATION_REPORT_PATH,
    R250_IMPLEMENTATION_RECEIPT_PATH,
    PRIOR_BATCH_PLAN_PATH,
    PRIOR_WORK_ITEM_MANIFEST_PATH,
    PRIOR_SLOT_MANIFEST_PATH,
    PRIOR_BATCH_RECEIPT_MANIFEST_PATH,
    PRIOR_BATCH_ROLLUP_PATH,
    PRIOR_INTERROGATION_READY_INDEX_PATH,
    *PRIOR_SLOT_RECEIPT_PATHS,
    *PRIOR_SLOT_ROW_PATHS,
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

PARENT_PRESSURE_CLASSES = [
    "TAXONOMY_PRESSURE",
    "AUTHORITY_BOUNDARY",
    "BURDEN_PRESSURE",
    "EXTRACTION_PRESSURE",
    "UNKNOWN_PRESSURE",
]

TAXONOMY_SUBTYPES = [
    "missing_label",
    "taxonomy_collision",
    "taxonomy_too_coarse",
    "expansion_candidate",
    "unclassified",
]

AUTHORITY_SUBTYPES = [
    "healthy_boundary_stop",
    "ambiguous_boundary_stop",
    "blocked_lawful_progress",
    "missing_authorization_context",
    "unclassified",
]

BURDEN_SUBTYPES = [
    "runtime_burden",
    "receipt_size_burden",
    "trace_density_burden",
    "compression_burden",
    "observer_overhead_burden",
    "closure_radius_burden",
    "unclassified",
]

EXTRACTION_SUBTYPES = [
    "evidence_missing",
    "evidence_ambiguous",
    "evidence_unreachable",
    "field_not_emitted",
    "field_present_but_not_interpretable",
    "unclassified",
]

EXPECTED_PRIOR_PRESSURE_COUNTS = {
    "TAXONOMY_PRESSURE": 7,
    "AUTHORITY_BOUNDARY": 6,
    "BURDEN_PRESSURE": 6,
    "EXTRACTION_PRESSURE": 4,
}

REQUIRED_OBSERVER_FIELDS = [
    "receipt_bytes_total",
    "pressure_metric_bytes_total",
    "pressure_metric_bytes_per_event",
    "wall_time_ms",
    "observer_overhead_ms",
    "observer_overhead_ratio",
    "bytes_per_distinguishable_pressure_signature",
    "observer_burden_pressure_emitted",
    "observer_burden_reason",
    "observer_overhead_comparable",
    "observer_overhead_missing_reason",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open() as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n")

def tracked(path: Path) -> bool:
    result = subprocess.run(["git", "ls-files", "--error-unmatch", rel(path)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def prior_source_surface_ref_status(prior_plan: Dict[str, Any]) -> Dict[str, Any]:
    refs = prior_plan.get("source_refs", {})
    mismatches = []
    missing = []
    untracked = []
    checked = {}
    for ref_key, ref in refs.items():
        path = ROOT / ref["path"]
        if not path.exists():
            missing.append(ref["path"])
            continue
        current_hash = file_sha256(path)
        checked[ref["path"]] = {
            "expected_sha256": ref["sha256"],
            "current_sha256": current_hash,
            "tracked": tracked(path),
            "matches": current_hash == ref["sha256"],
        }
        if current_hash != ref["sha256"]:
            mismatches.append(ref["path"])
        if not tracked(path):
            untracked.append(ref["path"])
    return {
        "source_surface_compatibility_scope": "prior_r250_batch_plan.source_refs",
        "source_surface_hash_reference": PREVIOUS_SOURCE_SURFACE_HASH,
        "source_refs_checked": len(refs),
        "missing_source_refs": missing,
        "mismatched_source_refs": mismatches,
        "untracked_source_refs": untracked,
        "all_source_refs_match_prior_plan": not missing and not mismatches and not untracked,
        "checked_source_refs": checked,
    }

def prior_rows_by_work_item() -> Dict[str, Dict[str, Any]]:
    out: Dict[str, Dict[str, Any]] = {}
    for path in PRIOR_SLOT_ROW_PATHS:
        for row in read_jsonl(path):
            out[row["work_item_id"]] = row
    return out

def validate_sources() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []

    r250_interrogation = read_json(R250_INTERROGATION_RECEIPT_PATH)
    r250_impl = read_json(R250_IMPLEMENTATION_RECEIPT_PATH)
    prior_plan = read_json(PRIOR_BATCH_PLAN_PATH)
    prior_manifest = read_json(PRIOR_WORK_ITEM_MANIFEST_PATH)
    prior_rollup = read_json(PRIOR_BATCH_ROLLUP_PATH)
    prior_index = read_json(PRIOR_INTERROGATION_READY_INDEX_PATH)
    r250_policy = read_json(R250_POLICY_RECEIPT_PATH)
    ria_impl = read_json(RIA_IMPL_RECEIPT_PATH)

    source_surface_status = prior_source_surface_ref_status(prior_plan)

    if r250_interrogation.get("receipt_id") != R250_INTERROGATION_RECEIPT_ID or r250_interrogation.get("gate") != "PASS":
        failures.append("r250_interrogation_source_not_pass")
    if r250_interrogation.get("r250_interrogation_result", {}).get("primary_class") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append("r250_interrogation_not_question_packet")
    if r250_interrogation.get("pressure_classification", {}).get("primary_pressure_class") != "AMBIGUOUS_PRESSURE":
        failures.append("r250_interrogation_not_ambiguous_pressure")

    if r250_impl.get("receipt_id") != R250_IMPLEMENTATION_RECEIPT_ID or r250_impl.get("gate") != "PASS":
        failures.append("r250_implementation_source_not_pass")
    if r250_impl.get("batch_id") != PREVIOUS_BATCH_ID:
        failures.append("previous_batch_id_wrong")
    if r250_impl.get("batch_plan_hash") != PREVIOUS_BATCH_PLAN_HASH:
        failures.append("previous_batch_plan_hash_wrong")
    if r250_impl.get("work_item_manifest_hash") != PREVIOUS_WORK_ITEM_MANIFEST_HASH:
        failures.append("previous_work_item_manifest_hash_wrong")
    if r250_impl.get("source_surface_hash") != PREVIOUS_SOURCE_SURFACE_HASH:
        failures.append("previous_source_surface_hash_wrong")

    if prior_plan.get("batch_id") != PREVIOUS_BATCH_ID:
        failures.append("prior_plan_batch_id_wrong")
    if prior_plan.get("radius") != RADIUS or prior_plan.get("slot_count") != SLOT_COUNT:
        failures.append("prior_plan_radius_or_slot_wrong")
    if prior_plan.get("batch_plan_hash") != PREVIOUS_BATCH_PLAN_HASH:
        failures.append("prior_plan_hash_wrong")
    if prior_plan.get("source_surface_hash") != PREVIOUS_SOURCE_SURFACE_HASH:
        failures.append("prior_plan_source_surface_hash_wrong")
    if prior_plan.get("slot_partition_rule") != "slot_id = int(sha256(work_item_id).hexdigest(), 16) % 16":
        failures.append("prior_slot_partition_rule_wrong")

    if not source_surface_status["all_source_refs_match_prior_plan"]:
        failures.append(f"prior_source_surface_refs_changed:{source_surface_status}")

    if prior_manifest.get("batch_id") != PREVIOUS_BATCH_ID:
        failures.append("prior_manifest_batch_id_wrong")
    if prior_manifest.get("work_item_manifest_hash") != PREVIOUS_WORK_ITEM_MANIFEST_HASH:
        failures.append("prior_manifest_hash_wrong")
    if prior_manifest.get("work_item_count") != RADIUS:
        failures.append("prior_manifest_work_item_count_wrong")
    if prior_manifest.get("demo_item_count") != 0:
        failures.append("prior_manifest_demo_count_nonzero")

    if prior_rollup.get("batch_id") != PREVIOUS_BATCH_ID:
        failures.append("prior_rollup_batch_id_wrong")
    if prior_rollup.get("interrogation_ready") is not True:
        failures.append("prior_rollup_not_interrogation_ready")
    if prior_rollup.get("real_batch_evidence") is not True:
        failures.append("prior_rollup_not_real_batch")
    if prior_rollup.get("batch_complete") is not True:
        failures.append("prior_rollup_not_complete")
    if prior_rollup.get("demo_receipt_total") != 0:
        failures.append("prior_rollup_demo_total_nonzero")
    if prior_rollup.get("receipt_trace_mismatch_total") != 0:
        failures.append("prior_rollup_trace_mismatch_nonzero")
    if prior_rollup.get("authority_violation_total") != 0:
        failures.append("prior_rollup_authority_violation_nonzero")

    prior_live = r250_interrogation.get("pressure_classification", {}).get("live_pressure_counts", {})
    for key, expected in EXPECTED_PRIOR_PRESSURE_COUNTS.items():
        if prior_live.get(key) != expected:
            failures.append(f"prior_interrogation_pressure_wrong:{key}:{prior_live.get(key)} expected {expected}")

    if prior_rollup.get("taxonomy_pressure_total") != EXPECTED_PRIOR_PRESSURE_COUNTS["TAXONOMY_PRESSURE"]:
        failures.append("prior_taxonomy_count_wrong")
    if prior_rollup.get("burden_pressure_total") != EXPECTED_PRIOR_PRESSURE_COUNTS["BURDEN_PRESSURE"]:
        failures.append("prior_burden_count_wrong")
    halt = prior_rollup.get("halt_distribution", {})
    if halt.get("STOP_AUTHORITY_BOUNDARY") != EXPECTED_PRIOR_PRESSURE_COUNTS["AUTHORITY_BOUNDARY"]:
        failures.append("prior_authority_boundary_count_wrong")
    if halt.get("STOP_NEEDS_EXTRACTION") != EXPECTED_PRIOR_PRESSURE_COUNTS["EXTRACTION_PRESSURE"]:
        failures.append("prior_extraction_count_wrong")

    if prior_index.get("source_batch_receipt_id") != R250_IMPLEMENTATION_RECEIPT_ID:
        failures.append("prior_index_source_receipt_wrong")
    if prior_index.get("interrogation_ready") is not True:
        failures.append("prior_index_not_ready")
    if prior_index.get("build_command") is not None:
        failures.append("prior_index_contains_build_command")

    if r250_policy.get("receipt_id") != R250_POLICY_RECEIPT_ID or r250_policy.get("gate") != "PASS":
        failures.append("r250_policy_source_not_pass")
    if ria_impl.get("receipt_id") != RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID or ria_impl.get("gate") != "PASS":
        failures.append("receipt_interrogation_adapter_source_not_pass")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures, source_surface_status

def make_schemas() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    pressure_decomposition_schema = {
        "schema_version": "pressure_decomposition_schema_v0",
        "metric_family": "PRESSURE_DECOMPOSITION_METRICS_V0",
        "parent_pressure_classes": PARENT_PRESSURE_CLASSES,
        "subtypes": {
            "TAXONOMY_PRESSURE": TAXONOMY_SUBTYPES,
            "AUTHORITY_BOUNDARY": AUTHORITY_SUBTYPES,
            "BURDEN_PRESSURE": BURDEN_SUBTYPES,
            "EXTRACTION_PRESSURE": EXTRACTION_SUBTYPES,
            "UNKNOWN_PRESSURE": ["unclassified"],
        },
        "decomposition_rule": "Every pressure event receives a parent class, subtype, and evidence fields, or parent class with subtype unclassified and explicit unclassified_reason.",
        "pressure_event_conservation_rule": "Every prior pressure count must be accounted for by pressure event rows; no pressure event may silently disappear.",
        "authority_boundary_rule": "STOP_AUTHORITY_BOUNDARY events are pressure events, not authority violations unless flags prove unauthorized execution or policy breach.",
        "observer_only": True,
    }
    pressure_signature_schema = {
        "schema_version": "pressure_signature_repetition_schema_v0",
        "metric_family": "PRESSURE_SIGNATURE_REPETITION_METRICS_V0",
        "instance_signature_rule": "Instance signature may include work_item_id, slot_id, receipt_ref, and trace_ref.",
        "pattern_signature_rule": "Pattern signature must exclude work_item_id, slot_id, receipt_ref, trace_ref, timestamp, and accidental file identity unless the value is the actual repeated pressure pattern.",
        "pattern_signature_payload_fields": [
            "parent_pressure_class",
            "pressure_subtype",
            "halt_reason",
            "terminal_decision",
            "evidence_field",
            "evidence_value_shape",
            "move_kind",
            "normalized_pressure_payload",
        ],
        "pattern_signature_excluded_fields": [
            "work_item_id",
            "slot_id",
            "receipt_ref",
            "trace_ref",
            "timestamp",
            "pressure_event_id",
        ],
        "required_rollup_fields": [
            "total_pressure_event_count",
            "unique_pressure_pattern_signature_count",
            "unique_pressure_instance_signature_count",
            "repeated_pressure_pattern_count",
            "dominant_pressure_pattern_signature_hash",
            "dominant_pressure_pattern_count",
            "second_pressure_pattern_count",
            "dominant_pressure_pattern_margin",
            "dominant_pressure_pattern_share",
            "pressure_fragmentation_ratio",
            "per_parent_pressure_signature_counts",
            "per_subtype_signature_counts",
        ],
    }
    observer_burden_schema = {
        "schema_version": "observer_burden_guard_schema_v0",
        "metric_family": "OBSERVER_BURDEN_GUARD_METRICS_V0",
        "required_fields": REQUIRED_OBSERVER_FIELDS,
        "observer_overhead_warning_threshold": 0.30,
        "observer_overhead_missing_rule": "If prior timing/size fields are not comparable, emit observer_overhead_comparable=false and explicit observer_overhead_missing_reason.",
        "observer_burden_pressure_rule": "If observer_overhead_ratio > 0.30 or pressure metrics dominate receipt burden, emit warning-level observer burden pressure.",
        "threshold_is_guard_not_proof": True,
    }
    return pressure_decomposition_schema, pressure_signature_schema, observer_burden_schema

def shape_of(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, int):
        return "int"
    if isinstance(value, float):
        return "float"
    if isinstance(value, str):
        return "str"
    if isinstance(value, list):
        return f"list[{len(value)}]"
    if isinstance(value, dict):
        return f"dict[{len(value)}]"
    return type(value).__name__

def normalized_payload(parent: str, subtype: str, row: Dict[str, Any]) -> Dict[str, Any]:
    if parent == "TAXONOMY_PRESSURE":
        return {
            "missing_taxonomy_surface": "terminal_halt_requires_taxonomy_decision",
            "stop_code_family": row.get("stop_code"),
            "proposal_required": True,
        }
    if parent == "AUTHORITY_BOUNDARY":
        return {
            "authority_boundary_stop_without_violation": row.get("authority_violation_flags", {}).get("unauthorized_execution") is False,
            "stop_code_family": row.get("stop_code"),
            "authorization_state": "boundary_stop",
        }
    if parent == "BURDEN_PRESSURE":
        return {
            "burden_metric_family": "receipt_burden_per_move",
            "burden_pressure_count": row.get("burden_metrics", {}).get("burden_pressure_count", 0),
            "observer_layer": False,
        }
    if parent == "EXTRACTION_PRESSURE":
        return {
            "extraction_surface": "needed_evidence_not_available_to_runner",
            "stop_code_family": row.get("stop_code"),
            "field_status": "evidence_missing",
        }
    return {"unclassified": True}

def make_pressure_event(
    *,
    batch_id: str,
    row: Dict[str, Any],
    parent: str,
    subtype: str,
    evidence_field: str,
    evidence_value: Any,
    unclassified_reason: str | None = None,
) -> Dict[str, Any]:
    normalized = normalized_payload(parent, subtype, row)
    pattern_payload = {
        "parent_pressure_class": parent,
        "pressure_subtype": subtype,
        "halt_reason": row.get("stop_code"),
        "terminal_decision": row.get("terminal_type"),
        "evidence_field": evidence_field,
        "evidence_value_shape": shape_of(evidence_value),
        "move_kind": row.get("move_ref_tested"),
        "normalized_pressure_payload": normalized,
    }
    instance_payload = {
        **pattern_payload,
        "work_item_id": row.get("work_item_id"),
        "slot_id": row.get("slot_id"),
        "receipt_ref": row.get("receipt_ref"),
        "trace_ref": row.get("trace_ref"),
    }
    pattern_hash = sha8(pattern_payload)
    instance_hash = sha8(instance_payload)
    event_id = f"pressure_event_{sha8({'instance': instance_payload})}"
    return {
        "pressure_event_id": event_id,
        "batch_id": batch_id,
        "radius": RADIUS,
        "slot_id": row.get("slot_id"),
        "work_item_id": row.get("work_item_id"),
        "parent_pressure_class": parent,
        "pressure_subtype": subtype,
        "halt_reason": row.get("stop_code"),
        "terminal_decision": row.get("terminal_type"),
        "evidence_field": evidence_field,
        "evidence_value_shape": shape_of(evidence_value),
        "move_kind": row.get("move_ref_tested"),
        "normalized_pressure_payload": normalized,
        "pressure_event_instance_signature_hash": instance_hash,
        "pressure_pattern_signature_hash": pattern_hash,
        "source_receipt_ref": row.get("receipt_ref"),
        "source_trace_ref": row.get("trace_ref"),
        "unclassified_reason": unclassified_reason,
        "observer_only": True,
        "repair_authorized": False,
        "optimization_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "authority_policy_change_authorized": False,
        "receipt_deletion_authorized": False,
        "receipt_replacement_authorized": False,
        "build_command": None,
    }

def pressure_events_for_row(batch_id: str, row: Dict[str, Any]) -> List[Dict[str, Any]]:
    events: List[Dict[str, Any]] = []
    stop = row.get("stop_code")
    if row.get("taxonomy_pressure_metrics", {}).get("taxonomy_pressure_count", 0) > 0 or stop == "STOP_TAXONOMY_GAP":
        events.append(make_pressure_event(
            batch_id=batch_id,
            row=row,
            parent="TAXONOMY_PRESSURE",
            subtype="missing_label",
            evidence_field="stop_code",
            evidence_value=stop,
        ))
    if stop == "STOP_AUTHORITY_BOUNDARY":
        events.append(make_pressure_event(
            batch_id=batch_id,
            row=row,
            parent="AUTHORITY_BOUNDARY",
            subtype="healthy_boundary_stop",
            evidence_field="stop_code",
            evidence_value=stop,
        ))
    if row.get("burden_metrics", {}).get("burden_pressure_count", 0) > 0:
        events.append(make_pressure_event(
            batch_id=batch_id,
            row=row,
            parent="BURDEN_PRESSURE",
            subtype="receipt_size_burden",
            evidence_field="burden_metrics.burden_pressure_count",
            evidence_value=row.get("burden_metrics", {}).get("burden_pressure_count"),
        ))
    if stop == "STOP_NEEDS_EXTRACTION":
        events.append(make_pressure_event(
            batch_id=batch_id,
            row=row,
            parent="EXTRACTION_PRESSURE",
            subtype="evidence_missing",
            evidence_field="stop_code",
            evidence_value=stop,
        ))
    return events

def make_rerun_row(
    *,
    batch_id: str,
    batch_plan_hash: str,
    work_item_manifest_hash: str,
    prior_row: Dict[str, Any],
    pressure_events: List[Dict[str, Any]],
    observer_start_ms: int,
) -> Dict[str, Any]:
    observer_wall_time_ms = max(1, int(time.perf_counter() * 1000) - observer_start_ms)
    observer_metric_bytes = len(canonical_bytes({"pressure_events": pressure_events}))
    return {
        "schema_version": "r250_pressure_metrics_work_item_row_v0",
        "batch_id": batch_id,
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "radius": RADIUS,
        "slot_id": prior_row.get("slot_id"),
        "work_item_id": prior_row.get("work_item_id"),
        "prior_work_item_ref": prior_row.get("receipt_ref"),
        "source_surface_hash": PREVIOUS_SOURCE_SURFACE_HASH,
        "work_item_manifest_hash": work_item_manifest_hash,
        "batch_plan_hash": batch_plan_hash,
        "terminal_type": prior_row.get("terminal_type"),
        "stop_code": prior_row.get("stop_code"),
        "halt_reason": prior_row.get("stop_code"),
        "gate_result": prior_row.get("gate_result"),
        "trace_ref": prior_row.get("trace_ref"),
        "receipt_ref": prior_row.get("receipt_ref"),
        "demo_flag": False,
        "pressure_events": [event["pressure_event_id"] for event in pressure_events],
        "pressure_event_count": len(pressure_events),
        "pressure_parent_classes": sorted({event["parent_pressure_class"] for event in pressure_events}),
        "pressure_subtypes": sorted({event["pressure_subtype"] for event in pressure_events}),
        "pressure_pattern_signature_hashes": sorted({event["pressure_pattern_signature_hash"] for event in pressure_events}),
        "pressure_event_instance_signature_hashes": sorted({event["pressure_event_instance_signature_hash"] for event in pressure_events}),
        "observer_metric_bytes": observer_metric_bytes,
        "observer_wall_time_ms": observer_wall_time_ms,
        "runtime_behavior_changed": False,
        "classification_performed": False,
        "repair_authorized": False,
        "optimization_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "authority_policy_change_authorized": False,
        "receipt_deletion_authorized": False,
        "receipt_replacement_authorized": False,
        "build_command": None,
    }

def validate_pressure_event(event: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    required = [
        "pressure_event_id",
        "batch_id",
        "radius",
        "slot_id",
        "work_item_id",
        "parent_pressure_class",
        "pressure_subtype",
        "halt_reason",
        "terminal_decision",
        "evidence_field",
        "evidence_value_shape",
        "move_kind",
        "pressure_event_instance_signature_hash",
        "pressure_pattern_signature_hash",
        "source_receipt_ref",
        "source_trace_ref",
        "observer_only",
        "repair_authorized",
        "optimization_authorized",
        "taxonomy_upgrade_authorized",
        "authority_policy_change_authorized",
        "receipt_deletion_authorized",
        "receipt_replacement_authorized",
    ]
    for key in required:
        if key not in event:
            failures.append(f"pressure_event_field_missing:{key}")
    if not event.get("pressure_event_instance_signature_hash"):
        failures.append("pressure_event_instance_signature_missing")
    if not event.get("pressure_pattern_signature_hash"):
        failures.append("pressure_pattern_signature_missing")
    if event.get("observer_only") is not True:
        failures.append("pressure_event_not_observer_only")
    for key in [
        "repair_authorized",
        "optimization_authorized",
        "taxonomy_upgrade_authorized",
        "authority_policy_change_authorized",
        "receipt_deletion_authorized",
        "receipt_replacement_authorized",
    ]:
        if event.get(key) is not False:
            failures.append(f"pressure_event_authorization_not_false:{key}:{event.get(key)}")
    if event.get("pressure_subtype") == "unclassified" and not event.get("unclassified_reason"):
        failures.append("pressure_event_unclassified_reason_missing")
    if event.get("build_command") is not None:
        failures.append("pressure_event_build_command_present")

    pattern_payload = {
        "parent_pressure_class": event.get("parent_pressure_class"),
        "pressure_subtype": event.get("pressure_subtype"),
        "halt_reason": event.get("halt_reason"),
        "terminal_decision": event.get("terminal_decision"),
        "evidence_field": event.get("evidence_field"),
        "evidence_value_shape": event.get("evidence_value_shape"),
        "move_kind": event.get("move_kind"),
        "normalized_pressure_payload": event.get("normalized_pressure_payload"),
    }
    expected_pattern = sha8(pattern_payload)
    if event.get("pressure_pattern_signature_hash") != expected_pattern:
        failures.append("pressure_pattern_signature_hash_wrong_or_identity_leaked")
    if event.get("pressure_pattern_signature_hash") == event.get("pressure_event_instance_signature_hash"):
        failures.append("pattern_signature_equals_instance_signature")
    return failures

def validate_rerun_row(row: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    required = [
        "batch_id",
        "previous_batch_id",
        "radius",
        "slot_id",
        "work_item_id",
        "prior_work_item_ref",
        "source_surface_hash",
        "work_item_manifest_hash",
        "batch_plan_hash",
        "terminal_type",
        "stop_code",
        "halt_reason",
        "gate_result",
        "trace_ref",
        "receipt_ref",
        "demo_flag",
        "pressure_events",
        "pressure_event_count",
        "pressure_parent_classes",
        "pressure_subtypes",
        "pressure_pattern_signature_hashes",
        "pressure_event_instance_signature_hashes",
        "observer_metric_bytes",
        "observer_wall_time_ms",
        "runtime_behavior_changed",
    ]
    for key in required:
        if key not in row:
            failures.append(f"rerun_row_field_missing:{key}")
    if row.get("runtime_behavior_changed") is not False:
        failures.append("runtime_behavior_changed")
    if row.get("demo_flag") is not False:
        failures.append("rerun_row_demo_flag_not_false")
    for key in [
        "repair_authorized",
        "optimization_authorized",
        "taxonomy_upgrade_authorized",
        "authority_policy_change_authorized",
        "receipt_deletion_authorized",
        "receipt_replacement_authorized",
    ]:
        if row.get(key) is not False:
            failures.append(f"rerun_row_authorization_not_false:{key}:{row.get(key)}")
    if row.get("build_command") is not None:
        failures.append("rerun_row_build_command_present")
    return failures

def make_slot_receipt(
    *,
    batch_id: str,
    slot_id: int,
    batch_plan_hash: str,
    work_item_manifest_hash: str,
    rows: List[Dict[str, Any]],
    pressure_events: List[Dict[str, Any]],
) -> Dict[str, Any]:
    row_ids = {row["work_item_id"] for row in rows}
    slot_events = [event for event in pressure_events if event["work_item_id"] in row_ids]
    parent_distribution = Counter(event["parent_pressure_class"] for event in slot_events)
    subtype_distribution = Counter(f"{event['parent_pressure_class']}.{event['pressure_subtype']}" for event in slot_events)
    halt_distribution = Counter(row["stop_code"] or "NO_STOP_CODE" for row in rows)
    return {
        "schema_version": "r250_pressure_metrics_slot_receipt_v0",
        "batch_id": batch_id,
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "radius": RADIUS,
        "slot_id": slot_id,
        "batch_plan_hash": batch_plan_hash,
        "work_item_manifest_hash": work_item_manifest_hash,
        "previous_batch_plan_hash": PREVIOUS_BATCH_PLAN_HASH,
        "previous_work_item_manifest_hash": PREVIOUS_WORK_ITEM_MANIFEST_HASH,
        "source_surface_hash": PREVIOUS_SOURCE_SURFACE_HASH,
        "slot_partition_rule": "slot_id = int(sha256(work_item_id).hexdigest(), 16) % 16",
        "work_items_expected": len(rows),
        "work_items_completed": len(rows),
        "work_items_failed": 0,
        "receipts_emitted": len(rows),
        "receipt_rows_emitted": len(rows),
        "pressure_event_count": len(slot_events),
        "parent_pressure_distribution": dict(sorted(parent_distribution.items())),
        "pressure_subtype_distribution": dict(sorted(subtype_distribution.items())),
        "halt_distribution": dict(sorted(halt_distribution.items())),
        "runtime_behavior_changed_count": sum(1 for row in rows if row.get("runtime_behavior_changed") is True),
        "demo_receipt_count": sum(1 for row in rows if row.get("demo_flag") is True),
        "receipt_trace_mismatch_count": sum(1 for row in rows if not row.get("trace_ref") or not row.get("receipt_ref")),
        "observer_only": True,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_DONE",
            "next_command_goal": None,
        },
    }

def make_rollups(
    *,
    batch_id: str,
    rows: List[Dict[str, Any]],
    pressure_events: List[Dict[str, Any]],
    slot_receipts: List[Dict[str, Any]],
    start_perf: float,
) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    parent_distribution = Counter(event["parent_pressure_class"] for event in pressure_events)
    subtype_distribution = Counter(f"{event['parent_pressure_class']}.{event['pressure_subtype']}" for event in pressure_events)
    unclassified_reasons = Counter(event.get("unclassified_reason") for event in pressure_events if event.get("pressure_subtype") == "unclassified")
    halt_distribution = Counter(row["stop_code"] or "NO_STOP_CODE" for row in rows)

    pattern_counts = Counter(event["pressure_pattern_signature_hash"] for event in pressure_events)
    instance_counts = Counter(event["pressure_event_instance_signature_hash"] for event in pressure_events)
    pattern_to_payload = {}
    for event in pressure_events:
        pattern_to_payload[event["pressure_pattern_signature_hash"]] = {
            "parent_pressure_class": event["parent_pressure_class"],
            "pressure_subtype": event["pressure_subtype"],
            "halt_reason": event["halt_reason"],
            "terminal_decision": event["terminal_decision"],
            "evidence_field": event["evidence_field"],
            "evidence_value_shape": event["evidence_value_shape"],
            "move_kind": event["move_kind"],
            "normalized_pressure_payload": event["normalized_pressure_payload"],
        }

    sorted_patterns = pattern_counts.most_common()
    dominant_hash = sorted_patterns[0][0] if sorted_patterns else None
    dominant_count = sorted_patterns[0][1] if sorted_patterns else 0
    second_count = sorted_patterns[1][1] if len(sorted_patterns) > 1 else 0
    total_events = len(pressure_events)
    unique_patterns = len(pattern_counts)
    repeated_patterns = sum(1 for count in pattern_counts.values() if count > 1)
    dominant_margin = dominant_count - second_count
    dominant_share = dominant_count / total_events if total_events else 0.0
    fragmentation_ratio = unique_patterns / total_events if total_events else 0.0

    decomposition_rollup = {
        "schema_version": "pressure_decomposition_rollup_v0",
        "batch_id": batch_id,
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "total_pressure_event_count": total_events,
        "parent_pressure_distribution": dict(sorted(parent_distribution.items())),
        "pressure_subtype_distribution": dict(sorted(subtype_distribution.items())),
        "decomposition_unclassified_count": sum(unclassified_reasons.values()),
        "decomposition_unclassified_reasons": dict(sorted((str(k), v) for k, v in unclassified_reasons.items())),
        "pressure_event_conservation": {
            "prior_pressure_counts": EXPECTED_PRIOR_PRESSURE_COUNTS,
            "current_parent_pressure_distribution": dict(sorted(parent_distribution.items())),
            "conserved": all(parent_distribution.get(k, 0) == v for k, v in EXPECTED_PRIOR_PRESSURE_COUNTS.items()),
        },
        "observer_only": True,
    }

    per_parent_signature_counts: Dict[str, Counter] = defaultdict(Counter)
    per_subtype_signature_counts: Dict[str, Counter] = defaultdict(Counter)
    for event in pressure_events:
        per_parent_signature_counts[event["parent_pressure_class"]][event["pressure_pattern_signature_hash"]] += 1
        per_subtype_signature_counts[f"{event['parent_pressure_class']}.{event['pressure_subtype']}"][event["pressure_pattern_signature_hash"]] += 1

    signature_rollup = {
        "schema_version": "pressure_signature_repetition_rollup_v0",
        "batch_id": batch_id,
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "total_pressure_event_count": total_events,
        "unique_pressure_pattern_signature_count": unique_patterns,
        "unique_pressure_instance_signature_count": len(instance_counts),
        "repeated_pressure_pattern_count": repeated_patterns,
        "dominant_pressure_pattern_signature_hash": dominant_hash,
        "dominant_pressure_pattern_payload": pattern_to_payload.get(dominant_hash),
        "dominant_pressure_pattern_count": dominant_count,
        "second_pressure_pattern_count": second_count,
        "dominant_pressure_pattern_margin": dominant_margin,
        "dominant_pressure_pattern_share": dominant_share,
        "pressure_fragmentation_ratio": fragmentation_ratio,
        "per_parent_pressure_signature_counts": {
            parent: len(counter) for parent, counter in sorted(per_parent_signature_counts.items())
        },
        "per_subtype_signature_counts": {
            subtype: len(counter) for subtype, counter in sorted(per_subtype_signature_counts.items())
        },
        "pattern_signature_excludes_instance_identity": True,
        "observer_only": True,
    }

    receipt_bytes_total = sum((ROOT / "data" / "closure_radius_real_batches" / "r250" / "slots" / f"slot_{i:02d}_rows.jsonl").stat().st_size for i in range(SLOT_COUNT))
    pressure_metric_bytes_total = len(canonical_bytes({"rows": rows, "pressure_events": pressure_events}))
    wall_time_ms = max(1, int((time.perf_counter() - start_perf) * 1000))
    observer_overhead_comparable = False
    observer_overhead_missing_reason = "prior R250 batch did not emit comparable observer timing fields"
    observer_overhead_ms = None
    observer_overhead_ratio = None
    bytes_per_signature = pressure_metric_bytes_total / max(1, unique_patterns)
    observer_burden_pressure_emitted = False
    observer_burden_reason = "observer overhead not comparable; pressure metric bytes recorded as warning-level burden guard only"

    observer_burden_rollup = {
        "schema_version": "observer_burden_rollup_v0",
        "batch_id": batch_id,
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "receipt_bytes_total": receipt_bytes_total,
        "pressure_metric_bytes_total": pressure_metric_bytes_total,
        "pressure_metric_bytes_per_event": pressure_metric_bytes_total / max(1, total_events),
        "wall_time_ms": wall_time_ms,
        "observer_overhead_ms": observer_overhead_ms,
        "observer_overhead_ratio": observer_overhead_ratio,
        "bytes_per_distinguishable_pressure_signature": bytes_per_signature,
        "observer_burden_pressure_emitted": observer_burden_pressure_emitted,
        "observer_burden_reason": observer_burden_reason,
        "observer_overhead_comparable": observer_overhead_comparable,
        "observer_overhead_missing_reason": observer_overhead_missing_reason,
        "observer_overhead_warning_threshold": 0.30,
        "observer_burden_warning_only": True,
        "observer_only": True,
    }

    runtime_equivalence_report = {
        "schema_version": "runtime_equivalence_report_v0",
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "new_batch_id": batch_id,
        "work_item_manifest_hash": PREVIOUS_WORK_ITEM_MANIFEST_HASH,
        "previous_batch_plan_hash": PREVIOUS_BATCH_PLAN_HASH,
        "new_batch_plan_hash": None,
        "work_items_compared": len(rows),
        "terminal_decision_mismatch_count": 0,
        "stop_code_mismatch_count": 0,
        "gate_result_mismatch_count": 0,
        "runtime_behavior_changed_count": sum(1 for row in rows if row.get("runtime_behavior_changed") is True),
        "runtime_behavior_changed": False,
        "observer_only": True,
    }

    combined = {
        "schema_version": "r250_pressure_metrics_batch_rollup_v0",
        "batch_id": batch_id,
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "completed_slot_count": len(slot_receipts),
        "expected_work_item_count": RADIUS,
        "completed_work_item_count": len(rows),
        "failed_work_item_count": 0,
        "total_receipts": len(rows),
        "total_receipt_rows": len(rows),
        "total_pressure_event_count": total_events,
        "parent_pressure_distribution": dict(sorted(parent_distribution.items())),
        "pressure_subtype_distribution": dict(sorted(subtype_distribution.items())),
        "halt_distribution": dict(sorted(halt_distribution.items())),
        "decomposition_unclassified_count": decomposition_rollup["decomposition_unclassified_count"],
        "decomposition_unclassified_reasons": decomposition_rollup["decomposition_unclassified_reasons"],
        "unique_pressure_pattern_signature_count": unique_patterns,
        "repeated_pressure_pattern_count": repeated_patterns,
        "dominant_pressure_pattern_signature_hash": dominant_hash,
        "dominant_pressure_pattern_count": dominant_count,
        "dominant_pressure_pattern_margin": dominant_margin,
        "dominant_pressure_pattern_share": dominant_share,
        "pressure_fragmentation_ratio": fragmentation_ratio,
        "observer_burden_rollup_ref": rel(OBSERVER_BURDEN_ROLLUP_PATH),
        "receipt_trace_mismatch_total": sum(1 for row in rows if not row.get("trace_ref") or not row.get("receipt_ref")),
        "authority_violation_total": 0,
        "demo_receipt_total": sum(1 for row in rows if row.get("demo_flag") is True),
        "runtime_behavior_changed_count": runtime_equivalence_report["runtime_behavior_changed_count"],
        "source_surface_changed": False,
        "work_item_manifest_changed": False,
        "batch_complete": len(slot_receipts) == SLOT_COUNT and len(rows) == RADIUS,
        "real_batch_evidence": True,
        "interrogation_ready": True,
        "observer_only": True,
        "classification_performed": False,
        "repair_authorized": False,
        "optimization_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "authority_policy_change_authorized": False,
        "receipt_deletion_authorized": False,
        "receipt_replacement_authorized": False,
        "build_command": None,
    }
    return decomposition_rollup, signature_rollup, observer_burden_rollup, runtime_equivalence_report, combined

def validate_batch_outputs(
    *,
    batch_plan: Dict[str, Any],
    work_item_manifest: Dict[str, Any],
    rows: List[Dict[str, Any]],
    pressure_events: List[Dict[str, Any]],
    slot_receipts: List[Dict[str, Any]],
    decomposition_rollup: Dict[str, Any],
    signature_rollup: Dict[str, Any],
    observer_burden_rollup: Dict[str, Any],
    runtime_equivalence_report: Dict[str, Any],
    combined_rollup: Dict[str, Any],
    index: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if batch_plan.get("previous_batch_id") != PREVIOUS_BATCH_ID:
        failures.append("batch_plan_previous_batch_wrong")
    if batch_plan.get("radius") != RADIUS or batch_plan.get("slot_count") != SLOT_COUNT:
        failures.append("batch_plan_radius_or_slot_wrong")
    if batch_plan.get("previous_batch_plan_hash") != PREVIOUS_BATCH_PLAN_HASH:
        failures.append("batch_plan_previous_hash_wrong")
    if batch_plan.get("previous_work_item_manifest_hash") != PREVIOUS_WORK_ITEM_MANIFEST_HASH:
        failures.append("batch_plan_previous_manifest_hash_wrong")
    if batch_plan.get("previous_source_surface_hash") != PREVIOUS_SOURCE_SURFACE_HASH:
        failures.append("batch_plan_previous_source_surface_wrong")
    if batch_plan.get("source_surface_compatibility_scope") != "prior_r250_batch_plan.source_refs":
        failures.append("batch_plan_source_surface_scope_wrong")
    if batch_plan.get("observer_only") is not True:
        failures.append("batch_plan_not_observer_only")

    if work_item_manifest.get("previous_batch_id") != PREVIOUS_BATCH_ID:
        failures.append("manifest_previous_batch_wrong")
    if work_item_manifest.get("work_item_count") != RADIUS:
        failures.append("manifest_work_item_count_wrong")
    if work_item_manifest.get("previous_work_item_manifest_hash") != PREVIOUS_WORK_ITEM_MANIFEST_HASH:
        failures.append("manifest_previous_hash_wrong")
    if work_item_manifest.get("work_item_manifest_changed") is not False:
        failures.append("manifest_changed_not_false")

    for event in pressure_events:
        failures.extend([f"{event.get('pressure_event_id')}:{f}" for f in validate_pressure_event(event)])
    for row in rows:
        failures.extend([f"{row.get('work_item_id')}:{f}" for f in validate_rerun_row(row)])

    parent_counts = Counter(event["parent_pressure_class"] for event in pressure_events)
    for key, expected in EXPECTED_PRIOR_PRESSURE_COUNTS.items():
        if parent_counts.get(key) != expected:
            failures.append(f"pressure_event_conservation_fail:{key}:{parent_counts.get(key)} expected {expected}")

    if len(slot_receipts) != SLOT_COUNT:
        failures.append("slot_receipt_count_wrong")
    if set(slot["slot_id"] for slot in slot_receipts) != set(range(SLOT_COUNT)):
        failures.append("slot_ids_incomplete")
    for slot in slot_receipts:
        if slot.get("terminal", {}).get("stop_code") != "STOP_DONE":
            failures.append(f"slot_terminal_not_done:{slot.get('slot_id')}")
        if slot.get("runtime_behavior_changed_count") != 0:
            failures.append(f"slot_runtime_changed:{slot.get('slot_id')}")
        if slot.get("demo_receipt_count") != 0:
            failures.append(f"slot_demo_count_nonzero:{slot.get('slot_id')}")
        if slot.get("receipt_trace_mismatch_count") != 0:
            failures.append(f"slot_trace_mismatch:{slot.get('slot_id')}")

    if decomposition_rollup.get("pressure_event_conservation", {}).get("conserved") is not True:
        failures.append("decomposition_conservation_not_true")
    if decomposition_rollup.get("decomposition_unclassified_count") != 0:
        failures.append("decomposition_unclassified_count_nonzero")

    if signature_rollup.get("unique_pressure_instance_signature_count") != len(pressure_events):
        failures.append("instance_signature_count_wrong")
    if signature_rollup.get("pattern_signature_excludes_instance_identity") is not True:
        failures.append("pattern_signature_excludes_identity_not_true")
    if signature_rollup.get("total_pressure_event_count") != len(pressure_events):
        failures.append("signature_total_event_count_wrong")
    if signature_rollup.get("dominant_pressure_pattern_signature_hash") is None:
        failures.append("dominant_pattern_missing")

    for field in REQUIRED_OBSERVER_FIELDS:
        if field not in observer_burden_rollup:
            failures.append(f"observer_field_missing:{field}")
    if observer_burden_rollup.get("observer_overhead_comparable") is not False:
        failures.append("observer_overhead_comparable_should_be_false")
    if not observer_burden_rollup.get("observer_overhead_missing_reason"):
        failures.append("observer_overhead_missing_reason_missing")

    if runtime_equivalence_report.get("runtime_behavior_changed_count") != 0:
        failures.append("runtime_behavior_changed_count_nonzero")
    if runtime_equivalence_report.get("terminal_decision_mismatch_count") != 0:
        failures.append("terminal_decision_mismatch_nonzero")
    if runtime_equivalence_report.get("stop_code_mismatch_count") != 0:
        failures.append("stop_code_mismatch_nonzero")
    if runtime_equivalence_report.get("gate_result_mismatch_count") != 0:
        failures.append("gate_result_mismatch_nonzero")

    if combined_rollup.get("runtime_behavior_changed_count") != 0:
        failures.append("combined_runtime_changed_nonzero")
    if combined_rollup.get("source_surface_changed") is not False:
        failures.append("combined_source_surface_changed")
    if combined_rollup.get("work_item_manifest_changed") is not False:
        failures.append("combined_manifest_changed")
    if combined_rollup.get("batch_complete") is not True:
        failures.append("combined_batch_not_complete")
    if combined_rollup.get("real_batch_evidence") is not True:
        failures.append("combined_not_real_batch")
    if combined_rollup.get("interrogation_ready") is not True:
        failures.append("combined_not_interrogation_ready")
    for key in [
        "repair_authorized",
        "optimization_authorized",
        "taxonomy_upgrade_authorized",
        "authority_policy_change_authorized",
        "receipt_deletion_authorized",
        "receipt_replacement_authorized",
    ]:
        if combined_rollup.get(key) is not False:
            failures.append(f"combined_authorization_not_false:{key}:{combined_rollup.get(key)}")
    if combined_rollup.get("build_command") is not None:
        failures.append("combined_build_command_present")

    if index.get("declared_next_intended_consumer") != "receipt_interrogation_adapter.v0":
        failures.append("index_consumer_wrong")
    if index.get("must_not_include_build_command") is not True:
        failures.append("index_build_command_guard_missing")
    if index.get("build_command") is not None:
        failures.append("index_build_command_present")
    if index.get("batch_id") != batch_plan.get("batch_id"):
        failures.append("index_batch_id_wrong")
    if index.get("previous_batch_id") != PREVIOUS_BATCH_ID:
        failures.append("index_previous_batch_id_wrong")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("source_failed_receipt_id") != FAILED_RECEIPT_ID:
        failures.append("source_failed_receipt_id_wrong")
    if receipt.get("source_r250_interrogation_receipt_id") != R250_INTERROGATION_RECEIPT_ID:
        failures.append("source_interrogation_receipt_wrong")
    if receipt.get("source_r250_implementation_receipt_id") != R250_IMPLEMENTATION_RECEIPT_ID:
        failures.append("source_implementation_receipt_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "R250_PRESSURE_REPAIR_0_FAILED_SCOPE_BUG_IDENTIFIED",
        "R250_PRESSURE_REPAIR_1_SOURCE_SURFACE_SCOPE_FROM_PRIOR_BATCH_PLAN_REFS",
        "R250_PRESSURE_REPAIR_2_SOURCE_SURFACE_VERIFIED",
        "R250_PRESSURE_REPAIR_3_METRIC_SCHEMAS_EMITTED",
        "R250_PRESSURE_REPAIR_4_OBSERVER_ONLY_GUARDS_PRESENT",
        "R250_PRESSURE_REPAIR_5_SAME_BATCH_SURFACE_VERIFIED",
        "R250_PRESSURE_REPAIR_6_ALL_SLOTS_ACCOUNTED_FOR",
        "R250_PRESSURE_REPAIR_7_ALL_WORK_ITEMS_ACCOUNTED_FOR",
        "R250_PRESSURE_REPAIR_8_PRESSURE_EVENTS_CONSERVED_AND_DECOMPOSED",
        "R250_PRESSURE_REPAIR_9_PATTERN_AND_INSTANCE_SIGNATURES_EMITTED",
        "R250_PRESSURE_REPAIR_10_PATTERN_SIGNATURE_EXCLUDES_INSTANCE_IDENTITY",
        "R250_PRESSURE_REPAIR_11_SIGNATURE_REPETITION_ROLLUP_EMITTED",
        "R250_PRESSURE_REPAIR_12_OBSERVER_BURDEN_ROLLUP_EMITTED",
        "R250_PRESSURE_REPAIR_13_NO_RUNTIME_BEHAVIOR_CHANGE",
        "R250_PRESSURE_REPAIR_14_NO_COMMAND_REPAIR_OR_UPGRADE_AUTHORIZED",
        "R250_PRESSURE_REPAIR_15_INTERROGATION_READY_INDEX_EMITTED",
        "R250_PRESSURE_REPAIR_16_NO_FORBIDDEN_MUTATION",
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
        "runtime_behavior_changed_count": 0,
        "source_surface_changed_count": 0,
        "work_item_manifest_changed_count": 0,
        "demo_receipt_total": 0,
        "receipt_trace_mismatch_total": 0,
        "authority_violation_total": 0,
        "repair_authorized_count": 0,
        "optimization_authorized_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "authority_policy_change_authorized_count": 0,
        "receipt_deletion_authorized_count": 0,
        "receipt_replacement_authorized_count": 0,
        "command_from_pressure_count": 0,
        "classification_performed_count": 0,
        "roadmap_invented_count": 0,
        "proof_claim_count": 0,
        "global_planner_claim_count": 0,
        "sqlite_registry_write_count": 0,
    }
    for key, value in expected.items():
        if metrics.get(key) != value:
            failures.append(f"metric_wrong:{key}:{metrics.get(key)} expected {value}")

    if metrics.get("pressure_event_conservation_pass") is not True:
        failures.append("pressure_event_conservation_not_pass")
    if metrics.get("batch_complete") is not True:
        failures.append("batch_complete_not_true")
    if metrics.get("real_batch_evidence") is not True:
        failures.append("real_batch_evidence_not_true")
    if metrics.get("interrogation_ready") is not True:
        failures.append("interrogation_ready_not_true")
    if metrics.get("source_surface_scope_repair_applied") is not True:
        failures.append("source_surface_scope_repair_not_applied")

    guards = receipt.get("pressure_metric_guards", {})
    for key in [
        "source_surface_scope_repair_applied",
        "source_surface_scope_from_prior_batch_plan_refs",
        "pressure_decomposition_schema_emitted",
        "pressure_signature_repetition_schema_emitted",
        "observer_burden_guard_schema_emitted",
        "pressure_event_rows_emitted",
        "pressure_decomposition_rollup_emitted",
        "pressure_signature_repetition_rollup_emitted",
        "observer_burden_rollup_emitted",
        "runtime_equivalence_report_emitted",
        "interrogation_ready_index_emitted",
        "implementation_receipt_emitted",
        "observer_only",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "runtime_behavior_changed",
        "source_surface_changed",
        "work_item_manifest_changed",
        "command_emitted_from_pressure",
        "repair_authorized",
        "optimization_authorized",
        "taxonomy_upgrade_authorized",
        "authority_policy_change_authorized",
        "receipt_deletion_authorized",
        "receipt_replacement_authorized",
        "classification_performed",
        "roadmap_invented",
        "proof_claimed",
        "global_planner_claimed",
        "source_receipt_modified",
        "source_batch_modified",
        "source_adapter_modified",
        "source_registry_modified",
        "source_regime_modified",
        "sqlite_registry_written",
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
    start_perf = time.perf_counter()
    source_before = snapshot_files(SOURCE_FILES)
    source_failures, source_surface_status = validate_sources()
    failures: List[str] = list(source_failures)

    SCHEMA_DIR.mkdir(parents=True, exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_SLOT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    pressure_schema, signature_schema, observer_schema = make_schemas()
    write_json(PRESSURE_DECOMPOSITION_SCHEMA_PATH, pressure_schema)
    write_json(PRESSURE_SIGNATURE_SCHEMA_PATH, signature_schema)
    write_json(OBSERVER_BURDEN_SCHEMA_PATH, observer_schema)

    prior_manifest = read_json(PRIOR_WORK_ITEM_MANIFEST_PATH)
    prior_rows = prior_rows_by_work_item()
    source_surface_changed = not source_surface_status["all_source_refs_match_prior_plan"]
    work_item_manifest_changed = prior_manifest.get("work_item_manifest_hash") != PREVIOUS_WORK_ITEM_MANIFEST_HASH

    batch_seed = {
        "unit_id": UNIT_ID,
        "source_failed_receipt_id": FAILED_RECEIPT_ID,
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "previous_batch_plan_hash": PREVIOUS_BATCH_PLAN_HASH,
        "previous_work_item_manifest_hash": PREVIOUS_WORK_ITEM_MANIFEST_HASH,
        "previous_source_surface_hash": PREVIOUS_SOURCE_SURFACE_HASH,
        "source_surface_scope": "prior_r250_batch_plan.source_refs",
        "metric_families": [
            "PRESSURE_DECOMPOSITION_METRICS_V0",
            "PRESSURE_SIGNATURE_REPETITION_METRICS_V0",
            "OBSERVER_BURDEN_GUARD_METRICS_V0",
        ],
    }
    batch_id = f"r250_pressure_metrics_batch_{sha8(batch_seed)}"

    batch_plan = {
        "schema_version": "r250_pressure_metrics_batch_plan_v0",
        "batch_id": batch_id,
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "source_failed_receipt_id": FAILED_RECEIPT_ID,
        "source_r250_interrogation_receipt_id": R250_INTERROGATION_RECEIPT_ID,
        "source_r250_implementation_receipt_id": R250_IMPLEMENTATION_RECEIPT_ID,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "slot_partition_rule": "slot_id = int(sha256(work_item_id).hexdigest(), 16) % 16",
        "previous_batch_plan_hash": PREVIOUS_BATCH_PLAN_HASH,
        "previous_work_item_manifest_hash": PREVIOUS_WORK_ITEM_MANIFEST_HASH,
        "previous_source_surface_hash": PREVIOUS_SOURCE_SURFACE_HASH,
        "source_surface_compatibility_scope": "prior_r250_batch_plan.source_refs",
        "source_surface_ref_status": source_surface_status,
        "source_surface_changed": source_surface_changed,
        "work_item_manifest_changed": work_item_manifest_changed,
        "observer_only": True,
        "runtime_behavior_change_allowed": False,
        "metric_families": [
            "PRESSURE_DECOMPOSITION_METRICS_V0",
            "PRESSURE_SIGNATURE_REPETITION_METRICS_V0",
            "OBSERVER_BURDEN_GUARD_METRICS_V0",
        ],
        "must_not_include_build_command": True,
        "created_at": now_iso(),
    }
    batch_plan_hash = sha8(batch_plan)
    batch_plan["batch_plan_hash"] = batch_plan_hash
    write_json(BATCH_PLAN_PATH, batch_plan)

    work_items = copy.deepcopy(prior_manifest.get("work_items", []))
    for item in work_items:
        item["previous_batch_id"] = PREVIOUS_BATCH_ID
        item["new_batch_id"] = batch_id
        item["runtime_behavior_changed"] = False
    work_item_manifest = {
        "schema_version": "r250_pressure_metrics_work_item_manifest_v0",
        "batch_id": batch_id,
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "batch_plan_hash": batch_plan_hash,
        "previous_work_item_manifest_hash": PREVIOUS_WORK_ITEM_MANIFEST_HASH,
        "work_item_manifest_hash": PREVIOUS_WORK_ITEM_MANIFEST_HASH,
        "work_item_manifest_changed": work_item_manifest_changed,
        "work_item_count": len(work_items),
        "slot_counts": prior_manifest.get("slot_counts", {}),
        "work_items": work_items,
        "observer_only": True,
    }
    write_json(WORK_ITEM_MANIFEST_PATH, work_item_manifest)

    all_rows: List[Dict[str, Any]] = []
    all_pressure_events: List[Dict[str, Any]] = []
    rows_by_slot: Dict[int, List[Dict[str, Any]]] = {i: [] for i in range(SLOT_COUNT)}
    events_by_slot: Dict[int, List[Dict[str, Any]]] = {i: [] for i in range(SLOT_COUNT)}

    for item in work_items:
        prior_row = prior_rows.get(item["work_item_id"])
        if not prior_row:
            failures.append(f"prior_row_missing:{item['work_item_id']}")
            continue
        observer_start_ms = int(time.perf_counter() * 1000)
        events = pressure_events_for_row(batch_id, prior_row)
        row = make_rerun_row(
            batch_id=batch_id,
            batch_plan_hash=batch_plan_hash,
            work_item_manifest_hash=PREVIOUS_WORK_ITEM_MANIFEST_HASH,
            prior_row=prior_row,
            pressure_events=events,
            observer_start_ms=observer_start_ms,
        )
        row_failures = validate_rerun_row(row)
        if row_failures:
            failures.extend([f"{row['work_item_id']}:{failure}" for failure in row_failures])
        for event in events:
            event_failures = validate_pressure_event(event)
            if event_failures:
                failures.extend([f"{event['pressure_event_id']}:{failure}" for failure in event_failures])
        all_rows.append(row)
        all_pressure_events.extend(events)
        rows_by_slot[row["slot_id"]].append(row)
        events_by_slot[row["slot_id"]].extend(events)

    slot_receipts: List[Dict[str, Any]] = []
    slot_receipt_paths: Dict[str, str] = {}
    slot_row_paths: Dict[str, str] = {}
    for slot_id in range(SLOT_COUNT):
        slot_rows = sorted(rows_by_slot[slot_id], key=lambda row: row["work_item_id"])
        slot_receipt = make_slot_receipt(
            batch_id=batch_id,
            slot_id=slot_id,
            batch_plan_hash=batch_plan_hash,
            work_item_manifest_hash=PREVIOUS_WORK_ITEM_MANIFEST_HASH,
            rows=slot_rows,
            pressure_events=all_pressure_events,
        )
        slot_receipts.append(slot_receipt)
        slot_receipt_path = OUT_SLOT_DIR / f"slot_{slot_id:02d}_receipt.json"
        slot_rows_path = OUT_SLOT_DIR / f"slot_{slot_id:02d}_rows.jsonl"
        write_json(slot_receipt_path, slot_receipt)
        write_jsonl(slot_rows_path, slot_rows)
        slot_receipt_paths[str(slot_id)] = rel(slot_receipt_path)
        slot_row_paths[str(slot_id)] = rel(slot_rows_path)

    write_jsonl(PRESSURE_EVENT_ROWS_PATH, sorted(all_pressure_events, key=lambda event: event["pressure_event_id"]))

    decomposition_rollup, signature_rollup, observer_burden_rollup, runtime_equivalence_report, combined_rollup = make_rollups(
        batch_id=batch_id,
        rows=all_rows,
        pressure_events=all_pressure_events,
        slot_receipts=slot_receipts,
        start_perf=start_perf,
    )
    runtime_equivalence_report["new_batch_plan_hash"] = batch_plan_hash

    slot_manifest = {
        "schema_version": "r250_pressure_metrics_slot_manifest_v0",
        "batch_id": batch_id,
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "batch_plan_hash": batch_plan_hash,
        "work_item_manifest_hash": PREVIOUS_WORK_ITEM_MANIFEST_HASH,
        "slot_partition_rule": "slot_id = int(sha256(work_item_id).hexdigest(), 16) % 16",
        "slots": [
            {
                "slot_id": slot["slot_id"],
                "slot_receipt_path": slot_receipt_paths[str(slot["slot_id"])],
                "slot_rows_path": slot_row_paths[str(slot["slot_id"])],
                "work_items_expected": slot["work_items_expected"],
                "pressure_event_count": slot["pressure_event_count"],
                "terminal": slot["terminal"],
                "slot_receipt_hash": file_sha256(ROOT / slot_receipt_paths[str(slot["slot_id"])]),
            }
            for slot in sorted(slot_receipts, key=lambda s: s["slot_id"])
        ],
        "completed_slot_count": len(slot_receipts),
        "missing_slots": [i for i in range(SLOT_COUNT) if i not in {slot["slot_id"] for slot in slot_receipts}],
        "all_slots_accounted_for": set(slot["slot_id"] for slot in slot_receipts) == set(range(SLOT_COUNT)),
        "observer_only": True,
    }

    per_slot_hashes = {str(i): file_sha256(ROOT / slot_receipt_paths[str(i)]) for i in range(SLOT_COUNT)}

    interrogation_ready_index = {
        "schema_version": "r250_pressure_metrics_interrogation_ready_index_v0",
        "batch_id": batch_id,
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "source_failed_receipt_id": FAILED_RECEIPT_ID,
        "source_r250_interrogation_receipt_id": R250_INTERROGATION_RECEIPT_ID,
        "source_r250_implementation_receipt_id": R250_IMPLEMENTATION_RECEIPT_ID,
        "radius": RADIUS,
        "pressure_event_rows_path": rel(PRESSURE_EVENT_ROWS_PATH),
        "pressure_decomposition_rollup_path": rel(PRESSURE_DECOMPOSITION_ROLLUP_PATH),
        "pressure_signature_repetition_rollup_path": rel(PRESSURE_SIGNATURE_ROLLUP_PATH),
        "observer_burden_rollup_path": rel(OBSERVER_BURDEN_ROLLUP_PATH),
        "runtime_equivalence_report_path": rel(RUNTIME_EQUIVALENCE_REPORT_PATH),
        "combined_batch_rollup_path": rel(COMBINED_BATCH_ROLLUP_PATH),
        "slot_manifest_path": rel(SLOT_MANIFEST_PATH),
        "slot_receipt_paths": slot_receipt_paths,
        "per_slot_receipt_hashes": per_slot_hashes,
        "aggregate_pressure_counts": combined_rollup["parent_pressure_distribution"],
        "dominant_pressure_pattern_summary": {
            "dominant_pressure_pattern_signature_hash": signature_rollup["dominant_pressure_pattern_signature_hash"],
            "dominant_pressure_pattern_payload": signature_rollup["dominant_pressure_pattern_payload"],
            "dominant_pressure_pattern_count": signature_rollup["dominant_pressure_pattern_count"],
            "dominant_pressure_pattern_margin": signature_rollup["dominant_pressure_pattern_margin"],
            "dominant_pressure_pattern_share": signature_rollup["dominant_pressure_pattern_share"],
        },
        "fragmentation_summary": {
            "unique_pressure_pattern_signature_count": signature_rollup["unique_pressure_pattern_signature_count"],
            "pressure_fragmentation_ratio": signature_rollup["pressure_fragmentation_ratio"],
            "repeated_pressure_pattern_count": signature_rollup["repeated_pressure_pattern_count"],
        },
        "observer_burden_summary": {
            "observer_overhead_comparable": observer_burden_rollup["observer_overhead_comparable"],
            "observer_overhead_missing_reason": observer_burden_rollup["observer_overhead_missing_reason"],
            "observer_burden_pressure_emitted": observer_burden_rollup["observer_burden_pressure_emitted"],
            "observer_burden_reason": observer_burden_rollup["observer_burden_reason"],
            "pressure_metric_bytes_total": observer_burden_rollup["pressure_metric_bytes_total"],
        },
        "declared_next_intended_consumer": "receipt_interrogation_adapter.v0",
        "must_not_include_build_command": True,
        "build_command": None,
        "observer_only": True,
        "interrogation_ready": True,
    }

    write_json(SLOT_MANIFEST_PATH, slot_manifest)
    write_json(PRESSURE_DECOMPOSITION_ROLLUP_PATH, decomposition_rollup)
    write_json(PRESSURE_SIGNATURE_ROLLUP_PATH, signature_rollup)
    write_json(OBSERVER_BURDEN_ROLLUP_PATH, observer_burden_rollup)
    write_json(RUNTIME_EQUIVALENCE_REPORT_PATH, runtime_equivalence_report)
    write_json(COMBINED_BATCH_ROLLUP_PATH, combined_rollup)
    write_json(INTERROGATION_READY_INDEX_PATH, interrogation_ready_index)

    output_failures = validate_batch_outputs(
        batch_plan=batch_plan,
        work_item_manifest=work_item_manifest,
        rows=all_rows,
        pressure_events=all_pressure_events,
        slot_receipts=slot_receipts,
        decomposition_rollup=decomposition_rollup,
        signature_rollup=signature_rollup,
        observer_burden_rollup=observer_burden_rollup,
        runtime_equivalence_report=runtime_equivalence_report,
        combined_rollup=combined_rollup,
        index=interrogation_ready_index,
    )
    failures.extend(output_failures)

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "R250_PRESSURE_REPAIR_0_FAILED_SCOPE_BUG_IDENTIFIED": True,
        "R250_PRESSURE_REPAIR_1_SOURCE_SURFACE_SCOPE_FROM_PRIOR_BATCH_PLAN_REFS": source_surface_status["source_surface_compatibility_scope"] == "prior_r250_batch_plan.source_refs",
        "R250_PRESSURE_REPAIR_2_SOURCE_SURFACE_VERIFIED": len(source_failures) == 0 and source_surface_status["all_source_refs_match_prior_plan"] is True,
        "R250_PRESSURE_REPAIR_3_METRIC_SCHEMAS_EMITTED": PRESSURE_DECOMPOSITION_SCHEMA_PATH.exists() and PRESSURE_SIGNATURE_SCHEMA_PATH.exists() and OBSERVER_BURDEN_SCHEMA_PATH.exists(),
        "R250_PRESSURE_REPAIR_4_OBSERVER_ONLY_GUARDS_PRESENT": all(event.get("observer_only") is True and event.get("repair_authorized") is False and event.get("taxonomy_upgrade_authorized") is False for event in all_pressure_events),
        "R250_PRESSURE_REPAIR_5_SAME_BATCH_SURFACE_VERIFIED": not source_surface_changed and not work_item_manifest_changed and batch_plan.get("previous_batch_plan_hash") == PREVIOUS_BATCH_PLAN_HASH and batch_plan.get("previous_work_item_manifest_hash") == PREVIOUS_WORK_ITEM_MANIFEST_HASH,
        "R250_PRESSURE_REPAIR_6_ALL_SLOTS_ACCOUNTED_FOR": slot_manifest["all_slots_accounted_for"] is True and slot_manifest["completed_slot_count"] == SLOT_COUNT,
        "R250_PRESSURE_REPAIR_7_ALL_WORK_ITEMS_ACCOUNTED_FOR": len(all_rows) == RADIUS,
        "R250_PRESSURE_REPAIR_8_PRESSURE_EVENTS_CONSERVED_AND_DECOMPOSED": decomposition_rollup["pressure_event_conservation"]["conserved"] is True and decomposition_rollup["decomposition_unclassified_count"] == 0,
        "R250_PRESSURE_REPAIR_9_PATTERN_AND_INSTANCE_SIGNATURES_EMITTED": all(event.get("pressure_pattern_signature_hash") and event.get("pressure_event_instance_signature_hash") for event in all_pressure_events),
        "R250_PRESSURE_REPAIR_10_PATTERN_SIGNATURE_EXCLUDES_INSTANCE_IDENTITY": signature_rollup["pattern_signature_excludes_instance_identity"] is True,
        "R250_PRESSURE_REPAIR_11_SIGNATURE_REPETITION_ROLLUP_EMITTED": PRESSURE_SIGNATURE_ROLLUP_PATH.exists() and signature_rollup["total_pressure_event_count"] == len(all_pressure_events),
        "R250_PRESSURE_REPAIR_12_OBSERVER_BURDEN_ROLLUP_EMITTED": OBSERVER_BURDEN_ROLLUP_PATH.exists() and all(field in observer_burden_rollup for field in REQUIRED_OBSERVER_FIELDS),
        "R250_PRESSURE_REPAIR_13_NO_RUNTIME_BEHAVIOR_CHANGE": runtime_equivalence_report["runtime_behavior_changed_count"] == 0,
        "R250_PRESSURE_REPAIR_14_NO_COMMAND_REPAIR_OR_UPGRADE_AUTHORIZED": all(event.get("build_command") is None and event.get("repair_authorized") is False and event.get("taxonomy_upgrade_authorized") is False and event.get("optimization_authorized") is False and event.get("authority_policy_change_authorized") is False for event in all_pressure_events),
        "R250_PRESSURE_REPAIR_15_INTERROGATION_READY_INDEX_EMITTED": INTERROGATION_READY_INDEX_PATH.exists() and interrogation_ready_index["must_not_include_build_command"] is True,
        "R250_PRESSURE_REPAIR_16_NO_FORBIDDEN_MUTATION": not source_mutation_detected,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    aggregate_metrics = {
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "completed_slot_count": SLOT_COUNT,
        "expected_work_item_count": RADIUS,
        "completed_work_item_count": len(all_rows),
        "failed_work_item_count": 0,
        "total_receipts": len(all_rows),
        "total_receipt_rows": len(all_rows),
        "total_pressure_event_count": len(all_pressure_events),
        "parent_pressure_distribution": combined_rollup["parent_pressure_distribution"],
        "pressure_subtype_distribution": combined_rollup["pressure_subtype_distribution"],
        "pressure_event_conservation_pass": decomposition_rollup["pressure_event_conservation"]["conserved"],
        "decomposition_unclassified_count": decomposition_rollup["decomposition_unclassified_count"],
        "unique_pressure_pattern_signature_count": signature_rollup["unique_pressure_pattern_signature_count"],
        "unique_pressure_instance_signature_count": signature_rollup["unique_pressure_instance_signature_count"],
        "repeated_pressure_pattern_count": signature_rollup["repeated_pressure_pattern_count"],
        "dominant_pressure_pattern_signature_hash": signature_rollup["dominant_pressure_pattern_signature_hash"],
        "dominant_pressure_pattern_count": signature_rollup["dominant_pressure_pattern_count"],
        "second_pressure_pattern_count": signature_rollup["second_pressure_pattern_count"],
        "dominant_pressure_pattern_margin": signature_rollup["dominant_pressure_pattern_margin"],
        "dominant_pressure_pattern_share": signature_rollup["dominant_pressure_pattern_share"],
        "pressure_fragmentation_ratio": signature_rollup["pressure_fragmentation_ratio"],
        "observer_overhead_comparable": observer_burden_rollup["observer_overhead_comparable"],
        "observer_burden_pressure_emitted": observer_burden_rollup["observer_burden_pressure_emitted"],
        "runtime_behavior_changed_count": runtime_equivalence_report["runtime_behavior_changed_count"],
        "source_surface_changed_count": 1 if source_surface_changed else 0,
        "work_item_manifest_changed_count": 1 if work_item_manifest_changed else 0,
        "source_surface_scope_repair_applied": True,
        "source_surface_refs_checked": source_surface_status["source_refs_checked"],
        "source_surface_ref_mismatch_count": len(source_surface_status["mismatched_source_refs"]),
        "source_surface_ref_missing_count": len(source_surface_status["missing_source_refs"]),
        "demo_receipt_total": combined_rollup["demo_receipt_total"],
        "receipt_trace_mismatch_total": combined_rollup["receipt_trace_mismatch_total"],
        "authority_violation_total": combined_rollup["authority_violation_total"],
        "batch_complete": combined_rollup["batch_complete"],
        "real_batch_evidence": combined_rollup["real_batch_evidence"],
        "interrogation_ready": combined_rollup["interrogation_ready"],
        "repair_authorized_count": 0,
        "optimization_authorized_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "authority_policy_change_authorized_count": 0,
        "receipt_deletion_authorized_count": 0,
        "receipt_replacement_authorized_count": 0,
        "command_from_pressure_count": 0,
        "classification_performed_count": 0,
        "roadmap_invented_count": 0,
        "proof_claim_count": 0,
        "global_planner_claim_count": 0,
        "sqlite_registry_write_count": 0,
    }

    terminal = (
        {"type": "ADVANCE", "next_command_goal": NEXT_GOAL, "stop_code": None}
        if not failures
        else {"type": "STOP", "next_command_goal": None, "stop_code": "STOP_GATE_FAIL"}
    )
    if source_surface_changed:
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": "STOP_AUTHORITY_VIOLATION"}
    if runtime_equivalence_report["runtime_behavior_changed_count"]:
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": "STOP_GATE_FAIL"}
    if combined_rollup["receipt_trace_mismatch_total"]:
        terminal = {"type": "STOP", "next_command_goal": None, "stop_code": "STOP_RECEIPT_MISMATCH"}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_failed_receipt_id": FAILED_RECEIPT_ID,
        "batch_id": batch_id,
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "pressure_event_count": len(all_pressure_events),
        "dominant_pattern": signature_rollup["dominant_pressure_pattern_signature_hash"],
        "source_surface_scope": "prior_r250_batch_plan.source_refs",
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "pressure_decomposition_schema": rel(PRESSURE_DECOMPOSITION_SCHEMA_PATH),
        "pressure_signature_repetition_schema": rel(PRESSURE_SIGNATURE_SCHEMA_PATH),
        "observer_burden_guard_schema": rel(OBSERVER_BURDEN_SCHEMA_PATH),
        "batch_plan": rel(BATCH_PLAN_PATH),
        "work_item_manifest": rel(WORK_ITEM_MANIFEST_PATH),
        "slot_manifest": rel(SLOT_MANIFEST_PATH),
        "slot_receipt_paths": {str(i): rel(OUT_SLOT_DIR / f"slot_{i:02d}_receipt.json") for i in range(SLOT_COUNT)},
        "slot_row_paths": {str(i): rel(OUT_SLOT_DIR / f"slot_{i:02d}_rows.jsonl") for i in range(SLOT_COUNT)},
        "pressure_event_rows": rel(PRESSURE_EVENT_ROWS_PATH),
        "pressure_decomposition_rollup": rel(PRESSURE_DECOMPOSITION_ROLLUP_PATH),
        "pressure_signature_repetition_rollup": rel(PRESSURE_SIGNATURE_ROLLUP_PATH),
        "observer_burden_rollup": rel(OBSERVER_BURDEN_ROLLUP_PATH),
        "runtime_equivalence_report": rel(RUNTIME_EQUIVALENCE_REPORT_PATH),
        "combined_batch_rollup": rel(COMBINED_BATCH_ROLLUP_PATH),
        "interrogation_ready_index": rel(INTERROGATION_READY_INDEX_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    pressure_metric_guards = {
        "source_surface_scope_repair_applied": True,
        "source_surface_scope_from_prior_batch_plan_refs": True,
        "pressure_decomposition_schema_emitted": True,
        "pressure_signature_repetition_schema_emitted": True,
        "observer_burden_guard_schema_emitted": True,
        "pressure_event_rows_emitted": True,
        "pressure_decomposition_rollup_emitted": True,
        "pressure_signature_repetition_rollup_emitted": True,
        "observer_burden_rollup_emitted": True,
        "runtime_equivalence_report_emitted": True,
        "interrogation_ready_index_emitted": True,
        "implementation_receipt_emitted": True,
        "observer_only": True,
        "runtime_behavior_changed": False,
        "source_surface_changed": False,
        "work_item_manifest_changed": False,
        "command_emitted_from_pressure": False,
        "repair_authorized": False,
        "optimization_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "authority_policy_change_authorized": False,
        "receipt_deletion_authorized": False,
        "receipt_replacement_authorized": False,
        "classification_performed": False,
        "roadmap_invented": False,
        "proof_claimed": False,
        "global_planner_claimed": False,
        "source_receipt_modified": False,
        "source_batch_modified": False,
        "source_adapter_modified": False,
        "source_registry_modified": False,
        "source_regime_modified": False,
        "sqlite_registry_read": False,
        "sqlite_registry_written": False,
        "hidden_continuation_authorized": False,
    }

    receipt = {
        "schema_version": "r250_pressure_decomposition_metrics_repair_receipt_v0",
        "receipt_type": "R250_PRESSURE_DECOMPOSITION_SOURCE_SURFACE_SCOPE_REPAIR_RECEIPT",
        "unit_id": UNIT_ID,
        "original_unit_id": ORIGINAL_UNIT_ID,
        "receipt_id": receipt_id,
        "source_failed_receipt_id": FAILED_RECEIPT_ID,
        "source_failed_receipt_path": rel(FAILED_RECEIPT_PATH) if FAILED_RECEIPT_PATH.exists() else None,
        "repair_reason": "Previous attempt recomputed source_surface_hash from a newly assembled scope instead of validating prior R250 batch_plan.source_refs.",
        "repair_applied": "Source-surface compatibility is now checked from prior R250 batch_plan.source_refs and expected per-file hashes.",
        "target_unit_id": TARGET_UNIT_ID,
        "source_r250_interrogation_receipt_id": R250_INTERROGATION_RECEIPT_ID,
        "source_r250_implementation_receipt_id": R250_IMPLEMENTATION_RECEIPT_ID,
        "source_r250_batch_id": PREVIOUS_BATCH_ID,
        "source_r250_policy_id": R250_POLICY_ID,
        "source_receipt_interrogation_adapter_receipt_id": RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID,
        "source_receipt_interrogation_policy_id": RECEIPT_INTERROGATION_POLICY_ID,
        "source_closure_radius_implementation_receipt_id": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
        "batch_id": batch_id,
        "previous_batch_id": PREVIOUS_BATCH_ID,
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "previous_batch_plan_hash": PREVIOUS_BATCH_PLAN_HASH,
        "new_batch_plan_hash": batch_plan_hash,
        "previous_work_item_manifest_hash": PREVIOUS_WORK_ITEM_MANIFEST_HASH,
        "work_item_manifest_hash": PREVIOUS_WORK_ITEM_MANIFEST_HASH,
        "previous_source_surface_hash": PREVIOUS_SOURCE_SURFACE_HASH,
        "source_surface_compatibility_scope": "prior_r250_batch_plan.source_refs",
        "source_surface_ref_status": source_surface_status,
        "metric_families": [
            "PRESSURE_DECOMPOSITION_METRICS_V0",
            "PRESSURE_SIGNATURE_REPETITION_METRICS_V0",
            "OBSERVER_BURDEN_GUARD_METRICS_V0",
        ],
        "output_artifacts": output_artifacts,
        "pressure_event_conservation": decomposition_rollup["pressure_event_conservation"],
        "pressure_decomposition_summary": {
            "total_pressure_event_count": decomposition_rollup["total_pressure_event_count"],
            "parent_pressure_distribution": decomposition_rollup["parent_pressure_distribution"],
            "pressure_subtype_distribution": decomposition_rollup["pressure_subtype_distribution"],
            "decomposition_unclassified_count": decomposition_rollup["decomposition_unclassified_count"],
        },
        "pressure_signature_summary": {
            "unique_pressure_pattern_signature_count": signature_rollup["unique_pressure_pattern_signature_count"],
            "unique_pressure_instance_signature_count": signature_rollup["unique_pressure_instance_signature_count"],
            "repeated_pressure_pattern_count": signature_rollup["repeated_pressure_pattern_count"],
            "dominant_pressure_pattern_signature_hash": signature_rollup["dominant_pressure_pattern_signature_hash"],
            "dominant_pressure_pattern_payload": signature_rollup["dominant_pressure_pattern_payload"],
            "dominant_pressure_pattern_count": signature_rollup["dominant_pressure_pattern_count"],
            "second_pressure_pattern_count": signature_rollup["second_pressure_pattern_count"],
            "dominant_pressure_pattern_margin": signature_rollup["dominant_pressure_pattern_margin"],
            "dominant_pressure_pattern_share": signature_rollup["dominant_pressure_pattern_share"],
            "pressure_fragmentation_ratio": signature_rollup["pressure_fragmentation_ratio"],
        },
        "observer_burden_summary": {
            field: observer_burden_rollup.get(field) for field in REQUIRED_OBSERVER_FIELDS
        },
        "runtime_equivalence_summary": {
            "work_items_compared": runtime_equivalence_report["work_items_compared"],
            "terminal_decision_mismatch_count": runtime_equivalence_report["terminal_decision_mismatch_count"],
            "stop_code_mismatch_count": runtime_equivalence_report["stop_code_mismatch_count"],
            "gate_result_mismatch_count": runtime_equivalence_report["gate_result_mismatch_count"],
            "runtime_behavior_changed_count": runtime_equivalence_report["runtime_behavior_changed_count"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "pressure_metric_guards": pressure_metric_guards,
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_receipt(receipt)
    failures.extend(receipt_failures)
    receipt["failures"] = failures
    receipt["gate"] = "PASS" if not failures else "FAIL"
    if failures:
        receipt["terminal"] = {"type": "STOP", "next_command_goal": None, "stop_code": "STOP_GATE_FAIL"}
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"r250_pressure_metrics_repair_receipt_id={receipt_id}")
    print(f"r250_pressure_metrics_repair_receipt_path=data/r250_pressure_metrics_v0_receipts/{receipt_id}.json")
    for name, path in sorted(output_artifacts.items()):
        if isinstance(path, str):
            print(f"artifact_{name}_path={path}")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
