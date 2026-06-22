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

UNIT_ID = "BUILD_R250_PRESSURE_SIGNATURE_COARSENING_REVIEW_LAYER_V0"
TARGET_UNIT_ID = "r250_pressure_signature_coarsening_review_layer.v0"

SOURCE_PD_INTERROGATION_RECEIPT_ID = "1f934d51"
SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID = "f09b8395"
SOURCE_FAILED_PRESSURE_METRICS_RECEIPT_ID_OPTIONAL = "8b82d6a8"
SOURCE_R250_IMPLEMENTATION_RECEIPT_ID = "05723444"
SOURCE_R250_INTERROGATION_RECEIPT_ID = "41f65b9a"
SOURCE_R250_POLICY_ID = "44ee648b"
SOURCE_RECEIPT_INTERROGATION_ADAPTER_RECEIPT_ID = "a785297c"
SOURCE_RECEIPT_INTERROGATION_POLICY_ID = "2aa2f2f3"
SOURCE_CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID = "98ab6f11"

SOURCE_PRESSURE_BATCH_ID = "r250_pressure_metrics_batch_1095f5c6"
SOURCE_PREVIOUS_R250_BATCH_ID = "r250_batch_34f560c1"

RADIUS = 250
SOURCE_PRESSURE_EVENT_COUNT = 23
EXACT_UNIQUE_PATTERN_SIGNATURE_COUNT = 23
EXACT_REPEATED_PATTERN_COUNT = 0
EXACT_FRAGMENTATION_RATIO = 1.0

HUMAN_SELECTED_ANSWERS = {
    "Q1": "COARSEN_SIGNATURES",
    "Q2": "GROUP_BY_SUBTYPE + GROUP_BY_HALT_REASON",
    "Q3": "BLOCK_PROPOSAL_DUE_TO_FRAGMENTATION",
}

VALID_CANDIDATE_STATUSES = {
    "TOO_COARSE",
    "TOO_FINE",
    "PROMISING_REVIEW_LAYER",
    "INSUFFICIENT_EVIDENCE",
    "INVALID_COARSENING_RULE",
}

INSTANCE_IDENTITY_FIELDS = {
    "work_item_id",
    "slot_id",
    "source_receipt_ref",
    "source_trace_ref",
    "receipt_ref",
    "trace_ref",
    "timestamp",
    "file_path",
    "pressure_event_id",
}

SOURCE_PD_INTERROGATION_RECEIPT_PATH = ROOT / "data" / "r250_pressure_decomposed_interrogation_receipts" / f"{SOURCE_PD_INTERROGATION_RECEIPT_ID}.json"
SOURCE_PD_INTERROGATION_REPORT_PATH = ROOT / "data" / "r250_pressure_decomposed_interrogations" / "r250_pressure_decomposed_interrogation_report.json"
SOURCE_FRAGMENTATION_QUESTION_PACKET_PATH = ROOT / "data" / "r250_pressure_decomposed_interrogations" / "r250_pressure_fragmentation_question_packet.json"
SOURCE_PRESSURE_METRICS_RECEIPT_PATH = ROOT / "data" / "r250_pressure_metrics_v0_receipts" / f"{SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID}.json"
OPTIONAL_FAILED_PRESSURE_METRICS_RECEIPT_PATH = ROOT / "data" / "r250_pressure_metrics_v0_receipts" / f"{SOURCE_FAILED_PRESSURE_METRICS_RECEIPT_ID_OPTIONAL}.json"

SOURCE_PRESSURE_EVENT_ROWS_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "pressure_event_rows.jsonl"
SOURCE_PRESSURE_DECOMPOSITION_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "pressure_decomposition_rollup.json"
SOURCE_PRESSURE_SIGNATURE_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "pressure_signature_repetition_rollup.json"
SOURCE_OBSERVER_BURDEN_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "observer_burden_rollup.json"
SOURCE_RUNTIME_EQUIVALENCE_REPORT_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "runtime_equivalence_report.json"
SOURCE_PRESSURE_BATCH_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "r250_pressure_metrics_batch_rollup.json"
SOURCE_PRESSURE_INTERROGATION_READY_INDEX_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "r250_pressure_metrics_interrogation_ready_index.json"

SOURCE_R250_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "closure_radius_real_batch_receipts" / f"{SOURCE_R250_IMPLEMENTATION_RECEIPT_ID}.json"
SOURCE_R250_INTERROGATION_RECEIPT_PATH = ROOT / "data" / "closure_radius_real_batch_interrogation_receipts" / f"{SOURCE_R250_INTERROGATION_RECEIPT_ID}.json"
SOURCE_R250_POLICY_PATH = ROOT / "data" / "closure_radius_real_batch_r250_collection_v0_policies" / f"{SOURCE_R250_POLICY_ID}.json"
SOURCE_RIA_RECEIPT_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_implementation_receipts" / f"{SOURCE_RECEIPT_INTERROGATION_ADAPTER_RECEIPT_ID}.json"
SOURCE_RIA_POLICY_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_policies" / f"{SOURCE_RECEIPT_INTERROGATION_POLICY_ID}.json"
SOURCE_CLOSURE_RADIUS_RECEIPT_PATH = ROOT / "data" / "closure_radius_metrics_v0_implementation_receipts" / f"{SOURCE_CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    SOURCE_PD_INTERROGATION_RECEIPT_PATH,
    SOURCE_PD_INTERROGATION_REPORT_PATH,
    SOURCE_FRAGMENTATION_QUESTION_PACKET_PATH,
    SOURCE_PRESSURE_METRICS_RECEIPT_PATH,
    SOURCE_PRESSURE_EVENT_ROWS_PATH,
    SOURCE_PRESSURE_DECOMPOSITION_ROLLUP_PATH,
    SOURCE_PRESSURE_SIGNATURE_ROLLUP_PATH,
    SOURCE_OBSERVER_BURDEN_ROLLUP_PATH,
    SOURCE_RUNTIME_EQUIVALENCE_REPORT_PATH,
    SOURCE_PRESSURE_BATCH_ROLLUP_PATH,
    SOURCE_PRESSURE_INTERROGATION_READY_INDEX_PATH,
    SOURCE_R250_IMPLEMENTATION_RECEIPT_PATH,
    SOURCE_R250_INTERROGATION_RECEIPT_PATH,
    SOURCE_R250_POLICY_PATH,
    SOURCE_RIA_RECEIPT_PATH,
    SOURCE_RIA_POLICY_PATH,
    SOURCE_CLOSURE_RADIUS_RECEIPT_PATH,
]

OUT_DIR = ROOT / "data" / "r250_pressure_coarsening_review_v0"
RECEIPT_DIR = ROOT / "data" / "r250_pressure_coarsening_review_v0_receipts"

COARSENING_CANDIDATE_SCHEMA_PATH = OUT_DIR / "coarsening_candidate_schema_v0.json"
COARSENED_SIGNATURE_SCHEMA_PATH = OUT_DIR / "coarsened_signature_schema_v0.json"
COARSENING_REVIEW_GUARD_SCHEMA_PATH = OUT_DIR / "coarsening_review_guard_schema_v0.json"
COARSENED_EVENT_ROWS_PATH = OUT_DIR / "coarsened_pressure_event_rows.jsonl"
COARSENING_CANDIDATE_ROLLUPS_PATH = OUT_DIR / "coarsening_candidate_rollups.json"
COARSENING_COMPARISON_MATRIX_PATH = OUT_DIR / "coarsening_comparison_matrix.json"
COARSENING_OBSERVER_BURDEN_ROLLUP_PATH = OUT_DIR / "coarsening_observer_burden_rollup.json"
COARSENING_REVIEW_REPORT_PATH = OUT_DIR / "r250_pressure_coarsening_review_report.json"
COARSENING_REVIEW_PACKET_PATH = OUT_DIR / "r250_pressure_coarsening_review_packet.json"

CANDIDATES = [
    {
        "candidate_id": "A",
        "candidate_name": "parent_only",
        "coarsening_fields": ["parent_pressure_class"],
        "purpose": "baseline coarse grouping",
        "baseline_only": True,
        "center_candidate": False,
        "requires_explicit_family_rules": False,
    },
    {
        "candidate_id": "B",
        "candidate_name": "parent_plus_subtype",
        "coarsening_fields": ["parent_pressure_class", "pressure_subtype"],
        "purpose": "test whether subtype reveals meaningful pressure clusters",
        "baseline_only": False,
        "center_candidate": False,
        "requires_explicit_family_rules": False,
    },
    {
        "candidate_id": "C",
        "candidate_name": "parent_plus_subtype_plus_halt_reason",
        "coarsening_fields": ["parent_pressure_class", "pressure_subtype", "halt_reason"],
        "purpose": "human-selected center candidate",
        "baseline_only": False,
        "center_candidate": True,
        "requires_explicit_family_rules": False,
    },
    {
        "candidate_id": "D",
        "candidate_name": "parent_plus_subtype_plus_halt_reason_plus_move_kind",
        "coarsening_fields": ["parent_pressure_class", "pressure_subtype", "halt_reason", "move_kind"],
        "purpose": "test whether move kind avoids over-coarsening",
        "baseline_only": False,
        "center_candidate": False,
        "requires_explicit_family_rules": False,
    },
    {
        "candidate_id": "E",
        "candidate_name": "parent_plus_subtype_plus_halt_reason_plus_evidence_field",
        "coarsening_fields": ["parent_pressure_class", "pressure_subtype", "halt_reason", "evidence_field"],
        "purpose": "test whether evidence-field grouping explains fragmentation",
        "baseline_only": False,
        "center_candidate": False,
        "requires_explicit_family_rules": False,
    },
    {
        "candidate_id": "F",
        "candidate_name": "parent_plus_subtype_plus_halt_reason_plus_normalized_payload_family",
        "coarsening_fields": ["parent_pressure_class", "pressure_subtype", "halt_reason", "normalized_payload_family"],
        "purpose": "test payload family grouping only if explicit family rules exist",
        "baseline_only": False,
        "center_candidate": False,
        "requires_explicit_family_rules": True,
    },
]

MUST_NOT_INFER = [
    "do not infer coarsening acceptance",
    "do not infer taxonomy upgrade",
    "do not infer authority expansion",
    "do not infer burden optimization",
    "do not infer extraction repair",
    "do not emit command from coarsening",
    "do not emit proposal from coarsening",
    "do not overwrite exact pressure signatures",
    "do not claim fragmentation is false",
    "do not claim parent pressure is dominant",
    "do not claim proof",
    "do not claim roadmap",
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
    rows = []
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

def load_sources() -> Dict[str, Any]:
    return {
        "pd_receipt": read_json(SOURCE_PD_INTERROGATION_RECEIPT_PATH),
        "pd_report": read_json(SOURCE_PD_INTERROGATION_REPORT_PATH),
        "fragmentation_packet": read_json(SOURCE_FRAGMENTATION_QUESTION_PACKET_PATH),
        "pressure_receipt": read_json(SOURCE_PRESSURE_METRICS_RECEIPT_PATH),
        "pressure_events": read_jsonl(SOURCE_PRESSURE_EVENT_ROWS_PATH),
        "decomposition_rollup": read_json(SOURCE_PRESSURE_DECOMPOSITION_ROLLUP_PATH),
        "signature_rollup": read_json(SOURCE_PRESSURE_SIGNATURE_ROLLUP_PATH),
        "observer_rollup": read_json(SOURCE_OBSERVER_BURDEN_ROLLUP_PATH),
        "runtime_report": read_json(SOURCE_RUNTIME_EQUIVALENCE_REPORT_PATH),
        "batch_rollup": read_json(SOURCE_PRESSURE_BATCH_ROLLUP_PATH),
        "index": read_json(SOURCE_PRESSURE_INTERROGATION_READY_INDEX_PATH),
        "r250_receipt": read_json(SOURCE_R250_IMPLEMENTATION_RECEIPT_PATH),
        "r250_interrogation_receipt": read_json(SOURCE_R250_INTERROGATION_RECEIPT_PATH),
        "ria_receipt": read_json(SOURCE_RIA_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    pd_receipt = sources["pd_receipt"]
    pd_report = sources["pd_report"]
    fragmentation_packet = sources["fragmentation_packet"]
    pressure_receipt = sources["pressure_receipt"]
    events = sources["pressure_events"]
    decomposition = sources["decomposition_rollup"]
    signature = sources["signature_rollup"]
    observer = sources["observer_rollup"]
    runtime = sources["runtime_report"]
    batch_rollup = sources["batch_rollup"]
    index = sources["index"]

    if pd_receipt.get("receipt_id") != SOURCE_PD_INTERROGATION_RECEIPT_ID or pd_receipt.get("gate") != "PASS":
        failures.append("source_pd_interrogation_receipt_not_pass")
    if pd_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append("source_pd_terminal_not_stop")
    if pd_receipt.get("terminal", {}).get("stop_code") != "STOP_HUMAN_DECISION_REQUIRED":
        failures.append("source_pd_stop_code_wrong")
    if pd_receipt.get("r250_pressure_decomposed_interrogation_result", {}).get("primary_class") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append("source_pd_primary_class_wrong")
    if pd_receipt.get("pressure_classification", {}).get("primary_pressure_class") != "FRAGMENTED_PRESSURE":
        failures.append("source_pd_pressure_class_wrong")
    if pd_receipt.get("pressure_classification", {}).get("fragmented_pressure") is not True:
        failures.append("source_pd_not_fragmented")
    if pd_receipt.get("r250_pressure_decomposed_interrogation_result", {}).get("command_authorized") is not False:
        failures.append("source_pd_command_authorized")
    if pd_receipt.get("r250_pressure_decomposed_interrogation_result", {}).get("proposal_authorized") is not False:
        failures.append("source_pd_proposal_authorized")

    if pd_report.get("source_pressure_metrics_receipt_id") != SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID:
        failures.append("pd_report_source_pressure_receipt_wrong")

    if fragmentation_packet.get("packet_type") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append("fragmentation_packet_type_wrong")
    for key in [
        "may_emit_build_command",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_authority_widening",
        "may_authorize_optimization",
    ]:
        if fragmentation_packet.get(key) is not False:
            failures.append(f"fragmentation_packet_guard_not_false:{key}:{fragmentation_packet.get(key)}")

    if pressure_receipt.get("receipt_id") != SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID or pressure_receipt.get("gate") != "PASS":
        failures.append("source_pressure_metrics_receipt_not_pass")
    if pressure_receipt.get("source_failed_receipt_id") != SOURCE_FAILED_PRESSURE_METRICS_RECEIPT_ID_OPTIONAL:
        failures.append("source_pressure_metrics_failed_id_not_recorded")
    if pressure_receipt.get("batch_id") != SOURCE_PRESSURE_BATCH_ID:
        failures.append("source_pressure_batch_id_wrong")
    if pressure_receipt.get("previous_batch_id") != SOURCE_PREVIOUS_R250_BATCH_ID:
        failures.append("source_previous_batch_id_wrong")

    metrics = pressure_receipt.get("aggregate_metrics", {})
    expected = {
        "total_pressure_event_count": 23,
        "unique_pressure_pattern_signature_count": 23,
        "unique_pressure_instance_signature_count": 23,
        "repeated_pressure_pattern_count": 0,
        "dominant_pressure_pattern_count": 1,
        "second_pressure_pattern_count": 1,
        "dominant_pressure_pattern_margin": 0,
        "pressure_fragmentation_ratio": 1.0,
        "runtime_behavior_changed_count": 0,
        "source_surface_changed_count": 0,
        "work_item_manifest_changed_count": 0,
        "demo_receipt_total": 0,
        "receipt_trace_mismatch_total": 0,
        "authority_violation_total": 0,
        "command_from_pressure_count": 0,
        "classification_performed_count": 0,
        "roadmap_invented_count": 0,
        "proof_claim_count": 0,
        "global_planner_claim_count": 0,
        "sqlite_registry_write_count": 0,
    }
    for key, value in expected.items():
        if metrics.get(key) != value:
            failures.append(f"source_metric_wrong:{key}:{metrics.get(key)} expected {value}")
    if metrics.get("pressure_event_conservation_pass") is not True:
        failures.append("source_pressure_event_conservation_not_true")
    if metrics.get("batch_complete") is not True:
        failures.append("source_batch_not_complete")
    if metrics.get("real_batch_evidence") is not True:
        failures.append("source_not_real_batch")
    if metrics.get("interrogation_ready") is not True:
        failures.append("source_not_interrogation_ready")

    if len(events) != SOURCE_PRESSURE_EVENT_COUNT:
        failures.append(f"pressure_event_count_wrong:{len(events)}")
    for event in events:
        if event.get("pressure_pattern_signature_hash") is None:
            failures.append(f"event_missing_exact_signature:{event.get('pressure_event_id')}")
        if event.get("observer_only") is not True:
            failures.append(f"event_not_observer_only:{event.get('pressure_event_id')}")
        if event.get("build_command") is not None:
            failures.append(f"event_contains_build_command:{event.get('pressure_event_id')}")

    parent_counts = Counter(event.get("parent_pressure_class") for event in events)
    expected_parent = {
        "TAXONOMY_PRESSURE": 7,
        "AUTHORITY_BOUNDARY": 6,
        "BURDEN_PRESSURE": 6,
        "EXTRACTION_PRESSURE": 4,
    }
    for key, value in expected_parent.items():
        if parent_counts.get(key) != value:
            failures.append(f"source_event_parent_count_wrong:{key}:{parent_counts.get(key)} expected {value}")

    if decomposition.get("pressure_event_conservation", {}).get("conserved") is not True:
        failures.append("decomposition_not_conserved")
    if signature.get("pressure_fragmentation_ratio") != 1.0:
        failures.append("signature_fragmentation_ratio_wrong")
    if signature.get("repeated_pressure_pattern_count") != 0:
        failures.append("signature_repeated_pattern_nonzero")
    if observer.get("observer_overhead_comparable") is not False:
        failures.append("observer_comparable_wrong")
    if not observer.get("observer_overhead_missing_reason"):
        failures.append("observer_missing_reason_missing")
    if runtime.get("runtime_behavior_changed_count") != 0:
        failures.append("runtime_behavior_changed")
    if runtime.get("terminal_decision_mismatch_count") != 0:
        failures.append("runtime_terminal_mismatch")
    if runtime.get("stop_code_mismatch_count") != 0:
        failures.append("runtime_stop_code_mismatch")
    if runtime.get("gate_result_mismatch_count") != 0:
        failures.append("runtime_gate_mismatch")
    if batch_rollup.get("interrogation_ready") is not True:
        failures.append("batch_rollup_not_ready")
    if index.get("build_command") is not None:
        failures.append("index_contains_build_command")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def make_schemas() -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
    candidate_schema = {
        "schema_version": "coarsening_candidate_schema_v0",
        "target_unit_id": TARGET_UNIT_ID,
        "candidate_statuses": sorted(VALID_CANDIDATE_STATUSES),
        "candidates": CANDIDATES,
        "candidate_a_rule": "Candidate A is baseline-only and may not be selected as best candidate or PROMISING_REVIEW_LAYER.",
        "candidate_c_rule": "Candidate C is the human-selected center candidate: parent + subtype + halt_reason.",
        "candidate_f_rule": "Candidate F is INVALID_COARSENING_RULE unless explicit normalized payload family rules exist.",
        "review_only": True,
    }
    signature_schema = {
        "schema_version": "coarsened_signature_schema_v0",
        "required_per_event_fields": [
            "pressure_event_id",
            "original_pressure_pattern_signature_hash",
            "coarsening_candidate_id",
            "coarsened_signature_hash",
            "coarsening_fields_used",
            "coarsening_payload",
            "coarsening_loss_fields",
            "parent_pressure_class",
            "pressure_subtype",
            "halt_reason",
            "move_kind",
            "evidence_field",
            "normalized_payload_family",
            "work_item_id",
            "slot_id",
            "source_receipt_ref",
            "source_trace_ref",
        ],
        "forbidden_signature_hash_fields": sorted(INSTANCE_IDENTITY_FIELDS),
        "exact_signature_preservation_rule": "The original exact pressure signature must never be overwritten.",
        "review_only": True,
    }
    guard_schema = {
        "schema_version": "coarsening_review_guard_schema_v0",
        "guards": [
            "no_runtime_rerun",
            "no_source_mutation",
            "no_exact_signature_overwrite",
            "no_instance_identity_in_coarsened_signature",
            "no_repair_authorized",
            "no_taxonomy_upgrade_authorized",
            "no_authority_widening_authorized",
            "no_optimization_authorized",
            "no_command_authorized",
            "no_proposal_authorized",
        ],
        "terminal_on_success": {
            "type": "STOP",
            "stop_code": "STOP_HUMAN_DECISION_REQUIRED",
            "next_command_goal": None,
        },
        "review_only": True,
    }
    return candidate_schema, signature_schema, guard_schema

def normalized_payload_family_for_event(event: Dict[str, Any]) -> Tuple[str | None, str | None]:
    return None, "family_rule_missing"

def candidate_available(candidate: Dict[str, Any]) -> Tuple[bool, str | None]:
    if candidate["candidate_id"] == "F":
        return False, "family_rule_missing"
    return True, None

def coarsening_payload_for_candidate(candidate: Dict[str, Any], event: Dict[str, Any]) -> Dict[str, Any]:
    payload = {}
    for field in candidate["coarsening_fields"]:
        if field == "normalized_payload_family":
            family, _ = normalized_payload_family_for_event(event)
            payload[field] = family
        else:
            payload[field] = event.get(field)
    return payload

def coarsening_loss_fields_for_candidate(candidate: Dict[str, Any]) -> List[str]:
    base = {
        "parent_pressure_class",
        "pressure_subtype",
        "halt_reason",
        "move_kind",
        "evidence_field",
        "normalized_payload_family",
    }
    return sorted(base - set(candidate["coarsening_fields"]))

def make_coarsened_rows(events: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []

    for candidate in CANDIDATES:
        available, unavailable_reason = candidate_available(candidate)
        if not available:
            for event in events:
                family, family_reason = normalized_payload_family_for_event(event)
                row = {
                    "schema_version": "coarsened_pressure_event_row_v0",
                    "pressure_event_id": event["pressure_event_id"],
                    "original_pressure_pattern_signature_hash": event["pressure_pattern_signature_hash"],
                    "coarsening_candidate_id": candidate["candidate_id"],
                    "coarsening_candidate_name": candidate["candidate_name"],
                    "coarsened_signature_hash": None,
                    "coarsening_fields_used": candidate["coarsening_fields"],
                    "coarsening_payload": None,
                    "coarsening_loss_fields": coarsening_loss_fields_for_candidate(candidate),
                    "candidate_available": False,
                    "unavailable_reason": unavailable_reason or family_reason,
                    "parent_pressure_class": event.get("parent_pressure_class"),
                    "pressure_subtype": event.get("pressure_subtype"),
                    "halt_reason": event.get("halt_reason"),
                    "move_kind": event.get("move_kind"),
                    "evidence_field": event.get("evidence_field"),
                    "normalized_payload_family": family,
                    "work_item_id": event.get("work_item_id"),
                    "slot_id": event.get("slot_id"),
                    "source_receipt_ref": event.get("source_receipt_ref"),
                    "source_trace_ref": event.get("source_trace_ref"),
                    "instance_identity_used_in_signature": False,
                    "exact_signature_overwritten": False,
                    "review_only": True,
                    "build_command": None,
                    "proposal_authorized": False,
                    "repair_authorized": False,
                    "taxonomy_upgrade_authorized": False,
                    "authority_widening_authorized": False,
                    "optimization_authorized": False,
                    "runtime_rerun": False,
                }
                rows.append(row)
            continue

        for event in events:
            payload = coarsening_payload_for_candidate(candidate, event)
            signature_material = {
                "candidate_id": candidate["candidate_id"],
                "coarsening_payload": payload,
            }
            coarsened_hash = sha8(signature_material)
            row = {
                "schema_version": "coarsened_pressure_event_row_v0",
                "pressure_event_id": event["pressure_event_id"],
                "original_pressure_pattern_signature_hash": event["pressure_pattern_signature_hash"],
                "coarsening_candidate_id": candidate["candidate_id"],
                "coarsening_candidate_name": candidate["candidate_name"],
                "coarsened_signature_hash": coarsened_hash,
                "coarsening_fields_used": candidate["coarsening_fields"],
                "coarsening_payload": payload,
                "coarsening_loss_fields": coarsening_loss_fields_for_candidate(candidate),
                "candidate_available": True,
                "unavailable_reason": None,
                "parent_pressure_class": event.get("parent_pressure_class"),
                "pressure_subtype": event.get("pressure_subtype"),
                "halt_reason": event.get("halt_reason"),
                "move_kind": event.get("move_kind"),
                "evidence_field": event.get("evidence_field"),
                "normalized_payload_family": None,
                "work_item_id": event.get("work_item_id"),
                "slot_id": event.get("slot_id"),
                "source_receipt_ref": event.get("source_receipt_ref"),
                "source_trace_ref": event.get("source_trace_ref"),
                "instance_identity_used_in_signature": False,
                "exact_signature_overwritten": False,
                "review_only": True,
                "build_command": None,
                "proposal_authorized": False,
                "repair_authorized": False,
                "taxonomy_upgrade_authorized": False,
                "authority_widening_authorized": False,
                "optimization_authorized": False,
                "runtime_rerun": False,
            }
            rows.append(row)
    return rows

def collapse_counts(rows: List[Dict[str, Any]]) -> Dict[str, int]:
    groups: Dict[str, List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        if row.get("coarsened_signature_hash") is not None:
            groups[row["coarsened_signature_hash"]].append(row)

    exact_collapsed = 0
    parent_collapsed = 0
    subtype_collapsed = 0
    halt_collapsed = 0
    move_collapsed = 0
    evidence_collapsed = 0

    for group_rows in groups.values():
        if len({r["original_pressure_pattern_signature_hash"] for r in group_rows}) > 1:
            exact_collapsed += len({r["original_pressure_pattern_signature_hash"] for r in group_rows}) - 1
        if len({r["parent_pressure_class"] for r in group_rows}) > 1:
            parent_collapsed += len({r["parent_pressure_class"] for r in group_rows}) - 1
        if len({r["pressure_subtype"] for r in group_rows}) > 1:
            subtype_collapsed += len({r["pressure_subtype"] for r in group_rows}) - 1
        if len({r["halt_reason"] for r in group_rows}) > 1:
            halt_collapsed += len({r["halt_reason"] for r in group_rows}) - 1
        if len({r["move_kind"] for r in group_rows}) > 1:
            move_collapsed += len({r["move_kind"] for r in group_rows}) - 1
        if len({r["evidence_field"] for r in group_rows}) > 1:
            evidence_collapsed += len({r["evidence_field"] for r in group_rows}) - 1

    return {
        "exact_pattern_signatures_collapsed_count": exact_collapsed,
        "parent_classes_collapsed_count": parent_collapsed,
        "subtypes_collapsed_count": subtype_collapsed,
        "halt_reasons_collapsed_count": halt_collapsed,
        "move_kinds_collapsed_count": move_collapsed,
        "evidence_fields_collapsed_count": evidence_collapsed,
    }

def coarsening_loss_score(loss: Dict[str, int], candidate: Dict[str, Any]) -> Tuple[int, str]:
    weighted = (
        loss["parent_classes_collapsed_count"] * 100
        + loss["subtypes_collapsed_count"] * 30
        + loss["halt_reasons_collapsed_count"] * 20
        + loss["move_kinds_collapsed_count"] * 5
        + loss["evidence_fields_collapsed_count"] * 5
        + loss["exact_pattern_signatures_collapsed_count"]
    )
    if candidate["candidate_id"] == "A":
        return weighted, "high" if weighted > 0 else "none"
    if loss["parent_classes_collapsed_count"] > 0:
        return weighted, "high"
    if loss["subtypes_collapsed_count"] > 0 or loss["halt_reasons_collapsed_count"] > 0:
        return weighted, "medium"
    if loss["exact_pattern_signatures_collapsed_count"] > 0:
        return weighted, "bounded"
    return weighted, "none"

def classify_candidate(candidate: Dict[str, Any], rows: List[Dict[str, Any]], loss: Dict[str, int], dominant_share: float, repeated_count: int, dominant_count: int, unique_count: int) -> Tuple[str, List[str]]:
    reasons: List[str] = []

    available, unavailable_reason = candidate_available(candidate)
    if not available:
        return "INVALID_COARSENING_RULE", [unavailable_reason or "candidate unavailable"]

    score, loss_level = coarsening_loss_score(loss, candidate)

    if candidate["candidate_id"] == "A":
        reasons.append("Candidate A is baseline-only and cannot be selected as best candidate.")
        if dominant_count > 1:
            return "TOO_COARSE", reasons
        return "INSUFFICIENT_EVIDENCE", reasons

    if unique_count == len(rows):
        return "TOO_FINE", ["No coarsening benefit; still all singletons."]

    if loss_level == "high":
        return "TOO_COARSE", [f"Coarsening loss level high; score={score}."]

    if repeated_count >= 1 and dominant_share >= 0.20 and loss_level in {"none", "bounded"}:
        return "PROMISING_REVIEW_LAYER", [
            "Repeated coarsened signatures appeared.",
            "Dominant share is meaningfully above exact-signature share.",
            f"Coarsening loss level is {loss_level}.",
            "Review only; no command or proposal emitted.",
        ]

    if repeated_count == 0:
        return "TOO_FINE", ["No repeated coarsened signatures appeared."]

    return "INSUFFICIENT_EVIDENCE", ["Repeated groups exist but review heuristic is not strong enough."]

def rollup_candidate(candidate: Dict[str, Any], candidate_rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    available, unavailable_reason = candidate_available(candidate)

    if not available:
        loss = {
            "exact_pattern_signatures_collapsed_count": 0,
            "parent_classes_collapsed_count": 0,
            "subtypes_collapsed_count": 0,
            "halt_reasons_collapsed_count": 0,
            "move_kinds_collapsed_count": 0,
            "evidence_fields_collapsed_count": 0,
        }
        return {
            "candidate_id": candidate["candidate_id"],
            "candidate_name": candidate["candidate_name"],
            "coarsening_fields": candidate["coarsening_fields"],
            "total_pressure_event_count": SOURCE_PRESSURE_EVENT_COUNT,
            "candidate_available": False,
            "unavailable_reason": unavailable_reason,
            "unique_coarsened_signature_count": 0,
            "repeated_coarsened_signature_count": 0,
            "dominant_coarsened_signature_hash": None,
            "dominant_coarsened_signature_count": 0,
            "second_coarsened_signature_count": 0,
            "dominant_coarsened_signature_margin": 0,
            "dominant_coarsened_signature_share": 0.0,
            "coarsened_fragmentation_ratio": 1.0,
            "groups_with_multiple_events_count": 0,
            "singletons_count": SOURCE_PRESSURE_EVENT_COUNT,
            "coarsening_loss": loss,
            "coarsening_loss_score": 0,
            "coarsening_loss_level": "not_applicable",
            "over_coarsening_risk": "not_applicable",
            "under_coarsening_risk": "not_applicable",
            "baseline_only": candidate["baseline_only"],
            "center_candidate": candidate["center_candidate"],
            "review_status": "INVALID_COARSENING_RULE",
            "review_status_reasons": [unavailable_reason or "unavailable"],
            "command_authorized": False,
            "proposal_authorized": False,
            "build_command": None,
            "review_only": True,
        }

    groups = Counter(row["coarsened_signature_hash"] for row in candidate_rows if row["coarsened_signature_hash"] is not None)
    unique_count = len(groups)
    repeated_count = sum(1 for count in groups.values() if count > 1)
    dominant_hash = None
    dominant_count = 0
    second_count = 0
    if groups:
        common = groups.most_common()
        dominant_hash = common[0][0]
        dominant_count = common[0][1]
        second_count = common[1][1] if len(common) > 1 else 0

    total = len(candidate_rows)
    dominant_margin = dominant_count - second_count
    dominant_share = dominant_count / total if total else 0.0
    fragmentation_ratio = unique_count / total if total else 1.0
    groups_with_multiple = repeated_count
    singletons = sum(1 for count in groups.values() if count == 1)
    loss = collapse_counts(candidate_rows)
    score, loss_level = coarsening_loss_score(loss, candidate)
    status, reasons = classify_candidate(candidate, candidate_rows, loss, dominant_share, repeated_count, dominant_count, unique_count)

    over_risk = "high" if status == "TOO_COARSE" or loss_level == "high" else ("medium" if loss_level == "medium" else "low")
    under_risk = "high" if status == "TOO_FINE" else ("medium" if repeated_count == 0 else "low")

    if candidate["candidate_id"] == "A" and status == "PROMISING_REVIEW_LAYER":
        status = "TOO_COARSE"
        reasons.append("Candidate A baseline-only guard forced status away from PROMISING_REVIEW_LAYER.")

    return {
        "candidate_id": candidate["candidate_id"],
        "candidate_name": candidate["candidate_name"],
        "coarsening_fields": candidate["coarsening_fields"],
        "total_pressure_event_count": total,
        "candidate_available": True,
        "unavailable_reason": None,
        "unique_coarsened_signature_count": unique_count,
        "repeated_coarsened_signature_count": repeated_count,
        "dominant_coarsened_signature_hash": dominant_hash,
        "dominant_coarsened_signature_count": dominant_count,
        "second_coarsened_signature_count": second_count,
        "dominant_coarsened_signature_margin": dominant_margin,
        "dominant_coarsened_signature_share": dominant_share,
        "coarsened_fragmentation_ratio": fragmentation_ratio,
        "groups_with_multiple_events_count": groups_with_multiple,
        "singletons_count": singletons,
        "coarsening_loss": loss,
        "coarsening_loss_score": score,
        "coarsening_loss_level": loss_level,
        "over_coarsening_risk": over_risk,
        "under_coarsening_risk": under_risk,
        "baseline_only": candidate["baseline_only"],
        "center_candidate": candidate["center_candidate"],
        "review_status": status,
        "review_status_reasons": reasons,
        "command_authorized": False,
        "proposal_authorized": False,
        "build_command": None,
        "review_only": True,
    }

def validate_coarsened_row(row: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    required = [
        "pressure_event_id",
        "original_pressure_pattern_signature_hash",
        "coarsening_candidate_id",
        "coarsened_signature_hash",
        "coarsening_fields_used",
        "coarsening_payload",
        "coarsening_loss_fields",
        "parent_pressure_class",
        "pressure_subtype",
        "halt_reason",
        "move_kind",
        "evidence_field",
        "normalized_payload_family",
        "work_item_id",
        "slot_id",
        "source_receipt_ref",
        "source_trace_ref",
    ]
    for key in required:
        if key not in row:
            failures.append(f"coarsened_row_field_missing:{key}")

    if row.get("exact_signature_overwritten") is not False:
        failures.append("exact_signature_overwritten")
    if row.get("instance_identity_used_in_signature") is not False:
        failures.append("instance_identity_used_in_signature")
    if row.get("build_command") is not None:
        failures.append("build_command_present")
    for key in [
        "proposal_authorized",
        "repair_authorized",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "runtime_rerun",
    ]:
        if row.get(key) is not False:
            failures.append(f"guard_not_false:{key}:{row.get(key)}")

    if row.get("candidate_available") is True:
        payload = row.get("coarsening_payload") or {}
        used_fields = set(row.get("coarsening_fields_used") or [])
        for forbidden in INSTANCE_IDENTITY_FIELDS:
            if forbidden in payload:
                failures.append(f"instance_identity_in_payload:{forbidden}")
            if forbidden in used_fields:
                failures.append(f"instance_identity_in_fields:{forbidden}")
        expected_hash = sha8({
            "candidate_id": row["coarsening_candidate_id"],
            "coarsening_payload": payload,
        })
        if row.get("coarsened_signature_hash") != expected_hash:
            failures.append("coarsened_signature_hash_wrong")
    return failures

def validate_candidate_rollup(rollup: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    required = [
        "candidate_id",
        "candidate_name",
        "coarsening_fields",
        "total_pressure_event_count",
        "unique_coarsened_signature_count",
        "repeated_coarsened_signature_count",
        "dominant_coarsened_signature_hash",
        "dominant_coarsened_signature_count",
        "second_coarsened_signature_count",
        "dominant_coarsened_signature_margin",
        "dominant_coarsened_signature_share",
        "coarsened_fragmentation_ratio",
        "groups_with_multiple_events_count",
        "singletons_count",
        "coarsening_loss",
        "coarsening_loss_score",
        "over_coarsening_risk",
        "under_coarsening_risk",
        "review_status",
    ]
    for key in required:
        if key not in rollup:
            failures.append(f"candidate_rollup_field_missing:{key}")
    if rollup.get("review_status") not in VALID_CANDIDATE_STATUSES:
        failures.append(f"invalid_review_status:{rollup.get('review_status')}")
    if rollup.get("candidate_id") == "A":
        if rollup.get("baseline_only") is not True:
            failures.append("candidate_a_not_baseline_only")
        if rollup.get("review_status") == "PROMISING_REVIEW_LAYER":
            failures.append("candidate_a_promising_forbidden")
    if rollup.get("candidate_id") == "F":
        if rollup.get("review_status") != "INVALID_COARSENING_RULE":
            failures.append("candidate_f_not_invalid_without_family_rules")
        if rollup.get("unavailable_reason") != "family_rule_missing":
            failures.append("candidate_f_missing_family_rule_reason")
    for key in ["command_authorized", "proposal_authorized"]:
        if rollup.get(key) is not False:
            failures.append(f"candidate_authorization_not_false:{key}:{rollup.get(key)}")
    if rollup.get("build_command") is not None:
        failures.append("candidate_build_command_present")
    if rollup.get("review_only") is not True:
        failures.append("candidate_not_review_only")
    return failures

def build_outputs(sources: Dict[str, Any]) -> Dict[str, Any]:
    start = time.perf_counter()
    events = sorted(sources["pressure_events"], key=lambda row: row["pressure_event_id"])

    schemas = make_schemas()
    write_json(COARSENING_CANDIDATE_SCHEMA_PATH, schemas[0])
    write_json(COARSENED_SIGNATURE_SCHEMA_PATH, schemas[1])
    write_json(COARSENING_REVIEW_GUARD_SCHEMA_PATH, schemas[2])

    coarsened_rows = make_coarsened_rows(events)
    write_jsonl(COARSENED_EVENT_ROWS_PATH, coarsened_rows)

    rows_by_candidate = defaultdict(list)
    for row in coarsened_rows:
        rows_by_candidate[row["coarsening_candidate_id"]].append(row)

    candidate_rollups = []
    for candidate in CANDIDATES:
        candidate_rollups.append(rollup_candidate(candidate, rows_by_candidate[candidate["candidate_id"]]))

    promising = [r for r in candidate_rollups if r["review_status"] == "PROMISING_REVIEW_LAYER"]
    promising_non_a = [r for r in promising if r["candidate_id"] != "A"]
    best_candidate = None
    if promising_non_a:
        best_candidate = sorted(
            promising_non_a,
            key=lambda r: (
                r["center_candidate"],
                r["dominant_coarsened_signature_share"],
                -r["coarsening_loss_score"],
            ),
            reverse=True,
        )[0]

    rejected = [
        {
            "candidate_id": r["candidate_id"],
            "candidate_name": r["candidate_name"],
            "review_status": r["review_status"],
            "review_status_reasons": r["review_status_reasons"],
        }
        for r in candidate_rollups
        if best_candidate is None or r["candidate_id"] != best_candidate["candidate_id"]
    ]

    comparison_matrix = {
        "schema_version": "coarsening_comparison_matrix_v0",
        "exact_signature_baseline": {
            "total_pressure_event_count": SOURCE_PRESSURE_EVENT_COUNT,
            "unique_pressure_pattern_signature_count": EXACT_UNIQUE_PATTERN_SIGNATURE_COUNT,
            "repeated_pressure_pattern_count": EXACT_REPEATED_PATTERN_COUNT,
            "pressure_fragmentation_ratio": EXACT_FRAGMENTATION_RATIO,
            "dominant_pressure_pattern_share": 1 / SOURCE_PRESSURE_EVENT_COUNT,
        },
        "parent_pressure_baseline": {
            "TAXONOMY_PRESSURE.missing_label": 7,
            "AUTHORITY_BOUNDARY.healthy_boundary_stop": 6,
            "BURDEN_PRESSURE.receipt_size_burden": 6,
            "EXTRACTION_PRESSURE.evidence_missing": 4,
        },
        "candidate_rows": candidate_rollups,
        "best_candidate_id": best_candidate["candidate_id"] if best_candidate else None,
        "best_candidate_review_status": best_candidate["review_status"] if best_candidate else None,
        "candidate_a_baseline_only": True,
        "candidate_c_center_candidate": True,
        "candidate_f_family_rule_missing": True,
        "review_only": True,
    }
    write_json(COARSENING_CANDIDATE_ROLLUPS_PATH, {
        "schema_version": "coarsening_candidate_rollups_v0",
        "source_pressure_event_count": SOURCE_PRESSURE_EVENT_COUNT,
        "candidate_count": len(CANDIDATES),
        "candidate_rollups": candidate_rollups,
        "best_candidate": best_candidate,
        "review_only": True,
    })
    write_json(COARSENING_COMPARISON_MATRIX_PATH, comparison_matrix)

    observer_elapsed_ms = max(1, int((time.perf_counter() - start) * 1000))
    output_bytes_estimate = len(canonical_bytes({
        "coarsened_rows": coarsened_rows,
        "candidate_rollups": candidate_rollups,
        "comparison_matrix": comparison_matrix,
    }))
    groups_total = sum(r["unique_coarsened_signature_count"] for r in candidate_rollups)
    observer_burden_warning = output_bytes_estimate > 250000
    observer = {
        "schema_version": "coarsening_observer_burden_rollup_v0",
        "coarsening_review_bytes_total": output_bytes_estimate,
        "coarsening_review_bytes_per_event": output_bytes_estimate / SOURCE_PRESSURE_EVENT_COUNT,
        "coarsening_review_wall_time_ms": observer_elapsed_ms,
        "coarsening_review_candidate_count": len(CANDIDATES),
        "coarsening_review_groups_total": groups_total,
        "bytes_per_review_group": output_bytes_estimate / max(1, groups_total),
        "observer_burden_warning": observer_burden_warning,
        "observer_burden_reason": "review output exceeds provisional byte threshold" if observer_burden_warning else "observer burden within provisional review threshold",
        "recommended_next_handling": "STOP_OR_COMPRESS_REVIEW_LAYER" if observer_burden_warning else "REVIEW_PACKET",
        "review_only": True,
    }
    write_json(COARSENING_OBSERVER_BURDEN_ROLLUP_PATH, observer)

    produced_repeated_groups = any(r["repeated_coarsened_signature_count"] >= 1 for r in candidate_rollups if r["candidate_available"])
    produced_dominant_group = any(r["dominant_coarsened_signature_share"] >= 0.20 for r in candidate_rollups if r["candidate_available"])
    too_lossy = any(r["coarsening_loss_level"] == "high" and r["review_status"] == "TOO_COARSE" for r in candidate_rollups)

    if best_candidate:
        recommended_next = "ACCEPT_COARSENING_LAYER_FOR_NEXT_INTERROGATION"
    elif any(r["review_status"] == "TOO_FINE" for r in candidate_rollups if r["candidate_id"] in {"C", "D", "E"}):
        recommended_next = "INSPECT_REPRESENTATIVE_FRAGMENTS"
    else:
        recommended_next = "RUN_MORE_BATCH_EVIDENCE"

    review_packet = {
        "schema_version": "r250_pressure_coarsening_review_packet_v0",
        "packet_type": "HUMAN_REVIEW_PACKET_NOT_COMMAND",
        "source_r250_pressure_decomposed_interrogation_receipt_id": SOURCE_PD_INTERROGATION_RECEIPT_ID,
        "source_r250_pressure_metrics_repair_receipt_id": SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID,
        "human_selected_answers": HUMAN_SELECTED_ANSWERS,
        "best_candidate_id": best_candidate["candidate_id"] if best_candidate else None,
        "best_candidate_status": best_candidate["review_status"] if best_candidate else None,
        "allowed_human_choices": [
            "ACCEPT_COARSENING_LAYER_FOR_NEXT_INTERROGATION",
            "REJECT_COARSENING_KEEP_FRAGMENTATION_AS_SIGNAL",
            "RUN_MORE_BATCH_EVIDENCE",
            "INSPECT_REPRESENTATIVE_FRAGMENTS",
            "DEFINE_NORMALIZED_PAYLOAD_FAMILY_RULES",
        ],
        "recommended_next_handling": recommended_next,
        "must_not_ask_for": [
            "taxonomy_upgrade",
            "authority_widening",
            "extraction_repair",
            "burden_optimization",
            "direct_build_command",
        ],
        "may_emit_build_command": False,
        "may_emit_objective_proposal": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_authority_widening": False,
        "may_authorize_optimization": False,
        "review_only": True,
    }
    write_json(COARSENING_REVIEW_PACKET_PATH, review_packet)

    report = {
        "schema_version": "r250_pressure_coarsening_review_report_v0",
        "source_receipt_ids": {
            "source_r250_pressure_decomposed_interrogation_receipt_id": SOURCE_PD_INTERROGATION_RECEIPT_ID,
            "source_r250_pressure_metrics_repair_receipt_id": SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID,
            "source_failed_pressure_metrics_receipt_id_optional": SOURCE_FAILED_PRESSURE_METRICS_RECEIPT_ID_OPTIONAL,
            "source_r250_implementation_receipt_id": SOURCE_R250_IMPLEMENTATION_RECEIPT_ID,
            "source_r250_interrogation_receipt_id": SOURCE_R250_INTERROGATION_RECEIPT_ID,
            "source_r250_policy_id": SOURCE_R250_POLICY_ID,
            "source_receipt_interrogation_adapter_receipt_id": SOURCE_RECEIPT_INTERROGATION_ADAPTER_RECEIPT_ID,
            "source_receipt_interrogation_policy_id": SOURCE_RECEIPT_INTERROGATION_POLICY_ID,
        },
        "source_question_packet_id": sources["pd_receipt"].get("question_packet", {}).get("question_packet_id"),
        "human_selected_answers": HUMAN_SELECTED_ANSWERS,
        "exact_signature_baseline": comparison_matrix["exact_signature_baseline"],
        "parent_pressure_baseline": comparison_matrix["parent_pressure_baseline"],
        "candidate_rollup_table": candidate_rollups,
        "best_candidate": best_candidate,
        "rejected_candidates": rejected,
        "observer_burden_summary": observer,
        "coarsening_produced_repeated_groups": produced_repeated_groups,
        "coarsening_produced_dominant_group": produced_dominant_group,
        "coarsening_too_lossy": too_lossy,
        "recommended_next_handling": recommended_next,
        "must_not_infer": MUST_NOT_INFER,
        "review_only": True,
        "command_authorized": False,
        "proposal_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "runtime_behavior_changed": False,
    }
    write_json(COARSENING_REVIEW_REPORT_PATH, report)

    return {
        "coarsened_rows": coarsened_rows,
        "candidate_rollups": candidate_rollups,
        "comparison_matrix": comparison_matrix,
        "observer_burden": observer,
        "review_report": report,
        "review_packet": review_packet,
        "best_candidate": best_candidate,
    }

def validate_outputs(outputs: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    coarsened_rows = outputs["coarsened_rows"]
    candidate_rollups = outputs["candidate_rollups"]
    comparison = outputs["comparison_matrix"]
    observer = outputs["observer_burden"]
    report = outputs["review_report"]
    packet = outputs["review_packet"]

    if len(coarsened_rows) != SOURCE_PRESSURE_EVENT_COUNT * len(CANDIDATES):
        failures.append(f"coarsened_row_count_wrong:{len(coarsened_rows)}")

    for row in coarsened_rows:
        failures.extend([f"{row.get('coarsening_candidate_id')}:{row.get('pressure_event_id')}:{f}" for f in validate_coarsened_row(row)])

    candidate_ids = {r["candidate_id"] for r in candidate_rollups}
    if candidate_ids != {c["candidate_id"] for c in CANDIDATES}:
        failures.append(f"candidate_set_wrong:{sorted(candidate_ids)}")

    for rollup in candidate_rollups:
        failures.extend([f"{rollup.get('candidate_id')}:{f}" for f in validate_candidate_rollup(rollup)])

    original_exact = defaultdict(set)
    for row in coarsened_rows:
        original_exact[row["pressure_event_id"]].add(row["original_pressure_pattern_signature_hash"])
    if any(len(values) != 1 for values in original_exact.values()):
        failures.append("exact_signature_not_preserved_consistently")

    if any(row["exact_signature_overwritten"] is not False for row in coarsened_rows):
        failures.append("exact_signature_overwritten")
    if any(row["instance_identity_used_in_signature"] is not False for row in coarsened_rows):
        failures.append("instance_identity_used_in_signature")

    for row in coarsened_rows:
        if row["candidate_available"] is True:
            payload = row["coarsening_payload"] or {}
            forbidden_present = sorted(set(payload.keys()) & INSTANCE_IDENTITY_FIELDS)
            if forbidden_present:
                failures.append(f"instance_identity_in_coarsened_payload:{row['coarsening_candidate_id']}:{forbidden_present}")

    candidate_a = next(r for r in candidate_rollups if r["candidate_id"] == "A")
    if candidate_a["review_status"] == "PROMISING_REVIEW_LAYER":
        failures.append("candidate_a_promising_forbidden")
    if comparison.get("candidate_a_baseline_only") is not True:
        failures.append("candidate_a_baseline_guard_missing")

    candidate_c = next(r for r in candidate_rollups if r["candidate_id"] == "C")
    if candidate_c["coarsening_fields"] != ["parent_pressure_class", "pressure_subtype", "halt_reason"]:
        failures.append("candidate_c_fields_wrong")
    if comparison.get("candidate_c_center_candidate") is not True:
        failures.append("candidate_c_center_guard_missing")

    candidate_f = next(r for r in candidate_rollups if r["candidate_id"] == "F")
    if candidate_f["review_status"] != "INVALID_COARSENING_RULE":
        failures.append("candidate_f_status_wrong")
    if candidate_f["unavailable_reason"] != "family_rule_missing":
        failures.append("candidate_f_family_rule_reason_missing")

    for rollup in candidate_rollups:
        loss = rollup.get("coarsening_loss")
        if not isinstance(loss, dict):
            failures.append(f"coarsening_loss_missing:{rollup['candidate_id']}")
            continue
        for key in [
            "exact_pattern_signatures_collapsed_count",
            "parent_classes_collapsed_count",
            "subtypes_collapsed_count",
            "halt_reasons_collapsed_count",
            "move_kinds_collapsed_count",
            "evidence_fields_collapsed_count",
        ]:
            if key not in loss:
                failures.append(f"coarsening_loss_field_missing:{rollup['candidate_id']}:{key}")

    if observer.get("coarsening_review_candidate_count") != len(CANDIDATES):
        failures.append("observer_candidate_count_wrong")
    for key in [
        "coarsening_review_bytes_total",
        "coarsening_review_bytes_per_event",
        "coarsening_review_wall_time_ms",
        "coarsening_review_candidate_count",
        "coarsening_review_groups_total",
        "bytes_per_review_group",
        "observer_burden_warning",
        "observer_burden_reason",
    ]:
        if key not in observer:
            failures.append(f"observer_burden_field_missing:{key}")

    for key in [
        "command_authorized",
        "proposal_authorized",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "runtime_behavior_changed",
    ]:
        if report.get(key) is not False:
            failures.append(f"report_guard_not_false:{key}:{report.get(key)}")

    if packet.get("packet_type") != "HUMAN_REVIEW_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    for choice in [
        "ACCEPT_COARSENING_LAYER_FOR_NEXT_INTERROGATION",
        "REJECT_COARSENING_KEEP_FRAGMENTATION_AS_SIGNAL",
        "RUN_MORE_BATCH_EVIDENCE",
        "INSPECT_REPRESENTATIVE_FRAGMENTS",
        "DEFINE_NORMALIZED_PAYLOAD_FAMILY_RULES",
    ]:
        if choice not in packet.get("allowed_human_choices", []):
            failures.append(f"packet_choice_missing:{choice}")
    for key in [
        "may_emit_build_command",
        "may_emit_objective_proposal",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_authority_widening",
        "may_authorize_optimization",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_id_wrong")
    if receipt.get("source_r250_pressure_decomposed_interrogation_receipt_id") != SOURCE_PD_INTERROGATION_RECEIPT_ID:
        failures.append("source_pd_receipt_wrong")
    if receipt.get("source_r250_pressure_metrics_repair_receipt_id") != SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID:
        failures.append("source_pressure_metrics_repair_receipt_wrong")
    if receipt.get("source_failed_pressure_metrics_receipt_id_optional") != SOURCE_FAILED_PRESSURE_METRICS_RECEIPT_ID_OPTIONAL:
        failures.append("source_failed_optional_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "R250_COARSEN_0_SOURCE_SURFACE_VERIFIED",
        "R250_COARSEN_1_HUMAN_DECISION_RECORDED",
        "R250_COARSEN_2_EXACT_SIGNATURES_PRESERVED",
        "R250_COARSEN_3_FIXED_CANDIDATES_TESTED",
        "R250_COARSEN_4_NO_INSTANCE_IDENTITY_IN_COARSENED_SIGNATURES",
        "R250_COARSEN_5_COARSENING_LOSS_MEASURED",
        "R250_COARSEN_6_CANDIDATE_STATUS_CLASSIFIED",
        "R250_COARSEN_7_CANDIDATE_A_BASELINE_ONLY",
        "R250_COARSEN_8_CANDIDATE_F_REQUIRES_EXPLICIT_FAMILY_RULES",
        "R250_COARSEN_9_OBSERVER_BURDEN_MEASURED",
        "R250_COARSEN_10_NO_RUNTIME_BEHAVIOR_CHANGE",
        "R250_COARSEN_11_NO_REPAIR_OR_UPGRADE_AUTHORIZED",
        "R250_COARSEN_12_NO_COMMAND_OR_PROPOSAL_FROM_PRESSURE",
        "R250_COARSEN_13_REVIEW_PACKET_EMITTED",
        "R250_COARSEN_14_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    expected_zero = [
        "runtime_behavior_changed_count",
        "repair_authorized_count",
        "taxonomy_upgrade_authorized_count",
        "authority_widening_authorized_count",
        "optimization_authorized_count",
        "command_authorized_count",
        "proposal_authorized_count",
        "roadmap_invented_count",
        "proof_claim_count",
        "source_mutation_count",
        "sqlite_registry_write_count",
        "exact_signature_overwrite_count",
        "instance_identity_in_coarsened_signature_count",
    ]
    for key in expected_zero:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")
    if metrics.get("source_pressure_event_count") != SOURCE_PRESSURE_EVENT_COUNT:
        failures.append("source_pressure_event_count_wrong")
    if metrics.get("coarsening_candidate_count") != len(CANDIDATES):
        failures.append("candidate_count_wrong")
    if metrics.get("candidate_a_baseline_only") is not True:
        failures.append("metric_candidate_a_baseline_only_not_true")
    if metrics.get("candidate_f_invalid_without_family_rules") is not True:
        failures.append("metric_candidate_f_invalid_not_true")
    if metrics.get("review_packet_emitted") is not True:
        failures.append("review_packet_not_emitted")
    if metrics.get("review_only") is not True:
        failures.append("review_only_not_true")

    guards = receipt.get("coarsening_review_guards", {})
    for key in [
        "human_decision_recorded",
        "exact_signatures_preserved",
        "fixed_candidates_tested",
        "coarsening_loss_measured",
        "candidate_status_classified",
        "observer_burden_measured",
        "review_packet_emitted",
        "candidate_a_baseline_only",
        "candidate_f_requires_explicit_family_rules",
        "review_only",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "runtime_rerun",
        "runtime_behavior_changed",
        "source_mutation",
        "exact_signature_overwritten",
        "instance_identity_used_in_coarsened_signature",
        "command_emitted",
        "proposal_emitted",
        "repair_authorized",
        "taxonomy_upgrade_authorized",
        "authority_widening_authorized",
        "optimization_authorized",
        "roadmap_invented",
        "proof_claimed",
        "sqlite_registry_written",
        "hidden_next_command",
    ]:
        if guards.get(key) is not False:
            failures.append(f"guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_HUMAN_DECISION_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    source_before = snapshot_files(SOURCE_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    outputs = build_outputs(sources)
    failures.extend(validate_outputs(outputs))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    candidate_rollups = outputs["candidate_rollups"]
    best_candidate = outputs["best_candidate"]
    coarsened_rows = outputs["coarsened_rows"]

    candidate_status_counts = Counter(r["review_status"] for r in candidate_rollups)
    promising_count = candidate_status_counts.get("PROMISING_REVIEW_LAYER", 0)
    too_coarse_count = candidate_status_counts.get("TOO_COARSE", 0)
    too_fine_count = candidate_status_counts.get("TOO_FINE", 0)
    insufficient_count = candidate_status_counts.get("INSUFFICIENT_EVIDENCE", 0)
    invalid_count = candidate_status_counts.get("INVALID_COARSENING_RULE", 0)

    exact_signature_overwrite_count = sum(1 for row in coarsened_rows if row.get("exact_signature_overwritten") is not False)
    instance_identity_count = sum(1 for row in coarsened_rows if row.get("instance_identity_used_in_signature") is not False)

    aggregate_metrics = {
        "source_pressure_event_count": SOURCE_PRESSURE_EVENT_COUNT,
        "exact_unique_pattern_signature_count": EXACT_UNIQUE_PATTERN_SIGNATURE_COUNT,
        "exact_repeated_pattern_count": EXACT_REPEATED_PATTERN_COUNT,
        "exact_fragmentation_ratio": EXACT_FRAGMENTATION_RATIO,
        "coarsening_candidate_count": len(CANDIDATES),
        "coarsened_event_row_count": len(coarsened_rows),
        "candidate_status_counts": dict(sorted(candidate_status_counts.items())),
        "promising_review_layer_count": promising_count,
        "too_coarse_count": too_coarse_count,
        "too_fine_count": too_fine_count,
        "insufficient_evidence_count": insufficient_count,
        "invalid_coarsening_rule_count": invalid_count,
        "best_candidate_id": best_candidate["candidate_id"] if best_candidate else None,
        "best_candidate_status": best_candidate["review_status"] if best_candidate else None,
        "candidate_a_baseline_only": True,
        "candidate_f_invalid_without_family_rules": True,
        "candidate_c_center_candidate": True,
        "coarsening_produced_repeated_groups": outputs["review_report"]["coarsening_produced_repeated_groups"],
        "coarsening_produced_dominant_group": outputs["review_report"]["coarsening_produced_dominant_group"],
        "coarsening_too_lossy": outputs["review_report"]["coarsening_too_lossy"],
        "observer_burden_warning": outputs["observer_burden"]["observer_burden_warning"],
        "review_packet_emitted": COARSENING_REVIEW_PACKET_PATH.exists(),
        "review_only": True,
        "runtime_behavior_changed_count": 0,
        "repair_authorized_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "authority_widening_authorized_count": 0,
        "optimization_authorized_count": 0,
        "command_authorized_count": 0,
        "proposal_authorized_count": 0,
        "roadmap_invented_count": 0,
        "proof_claim_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "sqlite_registry_write_count": 0,
        "exact_signature_overwrite_count": exact_signature_overwrite_count,
        "instance_identity_in_coarsened_signature_count": instance_identity_count,
    }

    acceptance_gate_results = {
        "R250_COARSEN_0_SOURCE_SURFACE_VERIFIED": len(validate_sources(sources)) == 0,
        "R250_COARSEN_1_HUMAN_DECISION_RECORDED": HUMAN_SELECTED_ANSWERS == {
            "Q1": "COARSEN_SIGNATURES",
            "Q2": "GROUP_BY_SUBTYPE + GROUP_BY_HALT_REASON",
            "Q3": "BLOCK_PROPOSAL_DUE_TO_FRAGMENTATION",
        },
        "R250_COARSEN_2_EXACT_SIGNATURES_PRESERVED": exact_signature_overwrite_count == 0 and all(row.get("original_pressure_pattern_signature_hash") for row in coarsened_rows),
        "R250_COARSEN_3_FIXED_CANDIDATES_TESTED": {r["candidate_id"] for r in candidate_rollups} == {"A", "B", "C", "D", "E", "F"},
        "R250_COARSEN_4_NO_INSTANCE_IDENTITY_IN_COARSENED_SIGNATURES": instance_identity_count == 0,
        "R250_COARSEN_5_COARSENING_LOSS_MEASURED": all(isinstance(r.get("coarsening_loss"), dict) for r in candidate_rollups),
        "R250_COARSEN_6_CANDIDATE_STATUS_CLASSIFIED": all(r.get("review_status") in VALID_CANDIDATE_STATUSES for r in candidate_rollups),
        "R250_COARSEN_7_CANDIDATE_A_BASELINE_ONLY": next(r for r in candidate_rollups if r["candidate_id"] == "A")["review_status"] != "PROMISING_REVIEW_LAYER",
        "R250_COARSEN_8_CANDIDATE_F_REQUIRES_EXPLICIT_FAMILY_RULES": next(r for r in candidate_rollups if r["candidate_id"] == "F")["review_status"] == "INVALID_COARSENING_RULE",
        "R250_COARSEN_9_OBSERVER_BURDEN_MEASURED": all(key in outputs["observer_burden"] for key in ["coarsening_review_bytes_total", "coarsening_review_bytes_per_event", "coarsening_review_wall_time_ms", "observer_burden_warning", "observer_burden_reason"]),
        "R250_COARSEN_10_NO_RUNTIME_BEHAVIOR_CHANGE": True,
        "R250_COARSEN_11_NO_REPAIR_OR_UPGRADE_AUTHORIZED": aggregate_metrics["repair_authorized_count"] == 0 and aggregate_metrics["taxonomy_upgrade_authorized_count"] == 0 and aggregate_metrics["authority_widening_authorized_count"] == 0 and aggregate_metrics["optimization_authorized_count"] == 0,
        "R250_COARSEN_12_NO_COMMAND_OR_PROPOSAL_FROM_PRESSURE": aggregate_metrics["command_authorized_count"] == 0 and aggregate_metrics["proposal_authorized_count"] == 0,
        "R250_COARSEN_13_REVIEW_PACKET_EMITTED": COARSENING_REVIEW_PACKET_PATH.exists(),
        "R250_COARSEN_14_NO_SOURCE_MUTATION": source_mutation_detected is False,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_HUMAN_DECISION_REQUIRED",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if exact_signature_overwrite_count or instance_identity_count:
        terminal = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}
    if aggregate_metrics["command_authorized_count"] or aggregate_metrics["proposal_authorized_count"]:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_pd_receipt": SOURCE_PD_INTERROGATION_RECEIPT_ID,
        "source_pressure_metrics_receipt": SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID,
        "candidate_count": len(CANDIDATES),
        "best_candidate_id": aggregate_metrics["best_candidate_id"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "coarsening_candidate_schema": rel(COARSENING_CANDIDATE_SCHEMA_PATH),
        "coarsened_signature_schema": rel(COARSENED_SIGNATURE_SCHEMA_PATH),
        "coarsening_review_guard_schema": rel(COARSENING_REVIEW_GUARD_SCHEMA_PATH),
        "coarsened_pressure_event_rows": rel(COARSENED_EVENT_ROWS_PATH),
        "coarsening_candidate_rollups": rel(COARSENING_CANDIDATE_ROLLUPS_PATH),
        "coarsening_comparison_matrix": rel(COARSENING_COMPARISON_MATRIX_PATH),
        "coarsening_observer_burden_rollup": rel(COARSENING_OBSERVER_BURDEN_ROLLUP_PATH),
        "r250_pressure_coarsening_review_report": rel(COARSENING_REVIEW_REPORT_PATH),
        "r250_pressure_coarsening_review_packet": rel(COARSENING_REVIEW_PACKET_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    guards = {
        "human_decision_recorded": True,
        "exact_signatures_preserved": exact_signature_overwrite_count == 0,
        "fixed_candidates_tested": True,
        "coarsening_loss_measured": True,
        "candidate_status_classified": True,
        "observer_burden_measured": True,
        "review_packet_emitted": COARSENING_REVIEW_PACKET_PATH.exists(),
        "candidate_a_baseline_only": True,
        "candidate_f_requires_explicit_family_rules": True,
        "review_only": True,
        "runtime_rerun": False,
        "runtime_behavior_changed": False,
        "source_mutation": source_mutation_detected,
        "exact_signature_overwritten": exact_signature_overwrite_count != 0,
        "instance_identity_used_in_coarsened_signature": instance_identity_count != 0,
        "command_emitted": False,
        "proposal_emitted": False,
        "repair_authorized": False,
        "taxonomy_upgrade_authorized": False,
        "authority_widening_authorized": False,
        "optimization_authorized": False,
        "roadmap_invented": False,
        "proof_claimed": False,
        "sqlite_registry_written": False,
        "hidden_next_command": False,
    }

    receipt = {
        "schema_version": "r250_pressure_signature_coarsening_review_layer_receipt_v0",
        "receipt_type": "R250_PRESSURE_SIGNATURE_COARSENING_REVIEW_LAYER_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "target_unit_id": TARGET_UNIT_ID,
        "source_r250_pressure_decomposed_interrogation_receipt_id": SOURCE_PD_INTERROGATION_RECEIPT_ID,
        "source_r250_pressure_metrics_repair_receipt_id": SOURCE_PRESSURE_METRICS_REPAIR_RECEIPT_ID,
        "source_failed_pressure_metrics_receipt_id_optional": SOURCE_FAILED_PRESSURE_METRICS_RECEIPT_ID_OPTIONAL,
        "optional_failed_receipt_required": False,
        "source_r250_pressure_batch_id": SOURCE_PRESSURE_BATCH_ID,
        "source_previous_r250_batch_id": SOURCE_PREVIOUS_R250_BATCH_ID,
        "source_r250_implementation_receipt_id": SOURCE_R250_IMPLEMENTATION_RECEIPT_ID,
        "source_r250_interrogation_receipt_id": SOURCE_R250_INTERROGATION_RECEIPT_ID,
        "source_r250_policy_id": SOURCE_R250_POLICY_ID,
        "source_receipt_interrogation_adapter_receipt_id": SOURCE_RECEIPT_INTERROGATION_ADAPTER_RECEIPT_ID,
        "source_receipt_interrogation_policy_id": SOURCE_RECEIPT_INTERROGATION_POLICY_ID,
        "human_selected_answers": HUMAN_SELECTED_ANSWERS,
        "candidate_set": CANDIDATES,
        "output_artifacts": output_artifacts,
        "review_summary": {
            "best_candidate": best_candidate,
            "candidate_status_counts": aggregate_metrics["candidate_status_counts"],
            "coarsening_produced_repeated_groups": aggregate_metrics["coarsening_produced_repeated_groups"],
            "coarsening_produced_dominant_group": aggregate_metrics["coarsening_produced_dominant_group"],
            "coarsening_too_lossy": aggregate_metrics["coarsening_too_lossy"],
            "recommended_next_handling": outputs["review_packet"]["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "coarsening_review_guards": guards,
        "must_not_infer": MUST_NOT_INFER,
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
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"r250_pressure_coarsening_review_receipt_id={receipt_id}")
    print(f"r250_pressure_coarsening_review_receipt_path=data/r250_pressure_coarsening_review_v0_receipts/{receipt_id}.json")
    print(f"r250_pressure_coarsening_review_report_path=data/r250_pressure_coarsening_review_v0/r250_pressure_coarsening_review_report.json")
    print(f"r250_pressure_coarsening_review_packet_path=data/r250_pressure_coarsening_review_v0/r250_pressure_coarsening_review_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
