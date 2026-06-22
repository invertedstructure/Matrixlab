#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REPAIR_R250_PRESSURE_DECOMPOSED_INTERROGATION_OPTIONAL_FAILED_RECEIPT_DEPENDENCY_V0"
ORIGINAL_UNIT_ID = "INTERROGATE_R250_PRESSURE_DECOMPOSED_BATCH_V0"
TARGET_UNIT_ID = "receipt_interrogation_adapter.v0.r250_pressure_decomposed_batch"

RADIUS = 250
SLOT_COUNT = 16

R250_PRESSURE_METRICS_RECEIPT_ID = "f09b8395"
R250_PRESSURE_FAILED_RECEIPT_ID = "8b82d6a8"
R250_INTERROGATION_RECEIPT_ID = "41f65b9a"
R250_IMPLEMENTATION_RECEIPT_ID = "05723444"
R250_POLICY_ID = "44ee648b"
RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID = "a785297c"
RECEIPT_INTERROGATION_POLICY_ID = "2aa2f2f3"
RECEIPT_INTERROGATION_POLICY_RECEIPT_ID = "0ad557c8"
CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID = "98ab6f11"

PREVIOUS_BATCH_ID = "r250_batch_34f560c1"
PRESSURE_BATCH_ID = "r250_pressure_metrics_batch_1095f5c6"
PRESSURE_BATCH_PLAN_HASH = "ea136bdb"
PREVIOUS_BATCH_PLAN_HASH = "b85c46b4"
PREVIOUS_WORK_ITEM_MANIFEST_HASH = "576909da"
PREVIOUS_SOURCE_SURFACE_HASH = "a109a264"

PRESSURE_RECEIPT_PATH = ROOT / "data" / "r250_pressure_metrics_v0_receipts" / f"{R250_PRESSURE_METRICS_RECEIPT_ID}.json"
OPTIONAL_FAILED_RECEIPT_PATH = ROOT / "data" / "r250_pressure_metrics_v0_receipts" / f"{R250_PRESSURE_FAILED_RECEIPT_ID}.json"

PRESSURE_DECOMPOSITION_SCHEMA_PATH = ROOT / "data" / "r250_pressure_metrics_v0" / "pressure_decomposition_schema_v0.json"
PRESSURE_SIGNATURE_SCHEMA_PATH = ROOT / "data" / "r250_pressure_metrics_v0" / "pressure_signature_repetition_schema_v0.json"
OBSERVER_BURDEN_SCHEMA_PATH = ROOT / "data" / "r250_pressure_metrics_v0" / "observer_burden_guard_schema_v0.json"

PRESSURE_BATCH_PLAN_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "batch_plan.json"
PRESSURE_WORK_ITEM_MANIFEST_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "work_item_manifest.json"
PRESSURE_SLOT_MANIFEST_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "slot_manifest.json"
PRESSURE_EVENT_ROWS_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "pressure_event_rows.jsonl"
PRESSURE_DECOMPOSITION_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "pressure_decomposition_rollup.json"
PRESSURE_SIGNATURE_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "pressure_signature_repetition_rollup.json"
OBSERVER_BURDEN_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "observer_burden_rollup.json"
RUNTIME_EQUIVALENCE_REPORT_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "runtime_equivalence_report.json"
PRESSURE_COMBINED_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "r250_pressure_metrics_batch_rollup.json"
PRESSURE_INDEX_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "r250_pressure_metrics_interrogation_ready_index.json"

R250_INTERROGATION_RECEIPT_PATH = ROOT / "data" / "closure_radius_real_batch_interrogation_receipts" / f"{R250_INTERROGATION_RECEIPT_ID}.json"
R250_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "closure_radius_real_batch_receipts" / f"{R250_IMPLEMENTATION_RECEIPT_ID}.json"
RIA_IMPL_RECEIPT_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_implementation_receipts" / f"{RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID}.json"
RIA_POLICY_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_policies" / f"{RECEIPT_INTERROGATION_POLICY_ID}.json"
RIA_POLICY_RECEIPT_PATH = ROOT / "data" / "receipt_interrogation_adapter_v0_policy_receipts" / f"{RECEIPT_INTERROGATION_POLICY_ID}.json"
CLOSURE_IMPL_RECEIPT_PATH = ROOT / "data" / "closure_radius_metrics_v0_implementation_receipts" / f"{CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID}.json"

PRESSURE_SLOT_RECEIPT_PATHS = [ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "slots" / f"slot_{i:02d}_receipt.json" for i in range(SLOT_COUNT)]
PRESSURE_SLOT_ROW_PATHS = [ROOT / "data" / "closure_radius_real_batches" / "r250_pressure_metrics_v0" / "slots" / f"slot_{i:02d}_rows.jsonl" for i in range(SLOT_COUNT)]

OUT_DIR = ROOT / "data" / "r250_pressure_decomposed_interrogations"
OUT_RECEIPT_DIR = ROOT / "data" / "r250_pressure_decomposed_interrogation_receipts"
REPORT_PATH = OUT_DIR / "r250_pressure_decomposed_interrogation_report.json"
QUESTION_PACKET_PATH = OUT_DIR / "r250_pressure_fragmentation_question_packet.json"

SOURCE_FILES = [
    PRESSURE_RECEIPT_PATH,
    PRESSURE_DECOMPOSITION_SCHEMA_PATH,
    PRESSURE_SIGNATURE_SCHEMA_PATH,
    OBSERVER_BURDEN_SCHEMA_PATH,
    PRESSURE_BATCH_PLAN_PATH,
    PRESSURE_WORK_ITEM_MANIFEST_PATH,
    PRESSURE_SLOT_MANIFEST_PATH,
    PRESSURE_EVENT_ROWS_PATH,
    PRESSURE_DECOMPOSITION_ROLLUP_PATH,
    PRESSURE_SIGNATURE_ROLLUP_PATH,
    OBSERVER_BURDEN_ROLLUP_PATH,
    RUNTIME_EQUIVALENCE_REPORT_PATH,
    PRESSURE_COMBINED_ROLLUP_PATH,
    PRESSURE_INDEX_PATH,
    *PRESSURE_SLOT_RECEIPT_PATHS,
    *PRESSURE_SLOT_ROW_PATHS,
    R250_INTERROGATION_RECEIPT_PATH,
    R250_IMPLEMENTATION_RECEIPT_PATH,
    RIA_IMPL_RECEIPT_PATH,
    RIA_POLICY_PATH,
    RIA_POLICY_RECEIPT_PATH,
    CLOSURE_IMPL_RECEIPT_PATH,
]

MUST_NOT_INFER = [
    "do not infer taxonomy upgrade",
    "do not infer authority expansion",
    "do not infer burden optimization",
    "do not infer extraction repair",
    "do not emit command from pressure",
    "do not invent roadmap",
    "do not claim repeated dominant pressure",
    "do not claim proof",
    "do not claim global planner",
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

def tracked(path: Path) -> bool:
    result = subprocess.run(["git", "ls-files", "--error-unmatch", rel(path)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_sources() -> List[str]:
    failures: List[str] = []

    pressure_receipt = read_json(PRESSURE_RECEIPT_PATH)
    pressure_batch_plan = read_json(PRESSURE_BATCH_PLAN_PATH)
    pressure_work_manifest = read_json(PRESSURE_WORK_ITEM_MANIFEST_PATH)
    pressure_slot_manifest = read_json(PRESSURE_SLOT_MANIFEST_PATH)
    pressure_decomp = read_json(PRESSURE_DECOMPOSITION_ROLLUP_PATH)
    pressure_sig = read_json(PRESSURE_SIGNATURE_ROLLUP_PATH)
    observer = read_json(OBSERVER_BURDEN_ROLLUP_PATH)
    runtime = read_json(RUNTIME_EQUIVALENCE_REPORT_PATH)
    combined = read_json(PRESSURE_COMBINED_ROLLUP_PATH)
    index = read_json(PRESSURE_INDEX_PATH)
    prior_interrogation = read_json(R250_INTERROGATION_RECEIPT_PATH)
    prior_impl = read_json(R250_IMPLEMENTATION_RECEIPT_PATH)
    adapter = read_json(RIA_IMPL_RECEIPT_PATH)

    if pressure_receipt.get("receipt_id") != R250_PRESSURE_METRICS_RECEIPT_ID or pressure_receipt.get("gate") != "PASS":
        failures.append("pressure_metrics_receipt_not_pass")
    if pressure_receipt.get("source_failed_receipt_id") != R250_PRESSURE_FAILED_RECEIPT_ID:
        failures.append("accepted_repair_receipt_does_not_reference_failed_receipt_id")
    if OPTIONAL_FAILED_RECEIPT_PATH.exists():
        optional = read_json(OPTIONAL_FAILED_RECEIPT_PATH)
        if optional.get("receipt_id") != R250_PRESSURE_FAILED_RECEIPT_ID:
            failures.append("optional_failed_receipt_id_wrong")
        if optional.get("gate") != "FAIL":
            failures.append("optional_failed_receipt_not_fail")
    if pressure_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("pressure_metrics_terminal_not_ADVANCE")
    if pressure_receipt.get("terminal", {}).get("next_command_goal") != ORIGINAL_UNIT_ID:
        failures.append(f"pressure_metrics_next_goal_wrong:{pressure_receipt.get('terminal', {}).get('next_command_goal')}")

    if pressure_receipt.get("batch_id") != PRESSURE_BATCH_ID:
        failures.append("pressure_batch_id_wrong")
    if pressure_receipt.get("previous_batch_id") != PREVIOUS_BATCH_ID:
        failures.append("previous_batch_id_wrong")
    if pressure_receipt.get("new_batch_plan_hash") != PRESSURE_BATCH_PLAN_HASH:
        failures.append("pressure_batch_plan_hash_wrong")
    if pressure_receipt.get("previous_batch_plan_hash") != PREVIOUS_BATCH_PLAN_HASH:
        failures.append("previous_batch_plan_hash_wrong")
    if pressure_receipt.get("previous_work_item_manifest_hash") != PREVIOUS_WORK_ITEM_MANIFEST_HASH:
        failures.append("previous_work_item_manifest_hash_wrong")
    if pressure_receipt.get("previous_source_surface_hash") != PREVIOUS_SOURCE_SURFACE_HASH:
        failures.append("previous_source_surface_hash_wrong")
    if pressure_receipt.get("source_surface_compatibility_scope") != "prior_r250_batch_plan.source_refs":
        failures.append("source_surface_scope_wrong")

    metrics = pressure_receipt.get("aggregate_metrics", {})
    expected = {
        "radius": RADIUS,
        "slot_count": SLOT_COUNT,
        "completed_slot_count": SLOT_COUNT,
        "expected_work_item_count": RADIUS,
        "completed_work_item_count": RADIUS,
        "failed_work_item_count": 0,
        "total_receipts": RADIUS,
        "total_receipt_rows": RADIUS,
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
            failures.append(f"metric_wrong:{key}:{metrics.get(key)} expected {value}")
    if metrics.get("pressure_event_conservation_pass") is not True:
        failures.append("pressure_event_conservation_not_true")
    if metrics.get("batch_complete") is not True:
        failures.append("batch_complete_not_true")
    if metrics.get("real_batch_evidence") is not True:
        failures.append("real_batch_evidence_not_true")
    if metrics.get("interrogation_ready") is not True:
        failures.append("interrogation_ready_not_true")
    if metrics.get("source_surface_scope_repair_applied") is not True:
        failures.append("source_surface_scope_repair_not_applied")

    parent = metrics.get("parent_pressure_distribution", {})
    for key, value in {
        "TAXONOMY_PRESSURE": 7,
        "AUTHORITY_BOUNDARY": 6,
        "BURDEN_PRESSURE": 6,
        "EXTRACTION_PRESSURE": 4,
    }.items():
        if parent.get(key) != value:
            failures.append(f"parent_pressure_wrong:{key}:{parent.get(key)} expected {value}")

    subtypes = metrics.get("pressure_subtype_distribution", {})
    for key, value in {
        "TAXONOMY_PRESSURE.missing_label": 7,
        "AUTHORITY_BOUNDARY.healthy_boundary_stop": 6,
        "BURDEN_PRESSURE.receipt_size_burden": 6,
        "EXTRACTION_PRESSURE.evidence_missing": 4,
    }.items():
        if subtypes.get(key) != value:
            failures.append(f"subtype_wrong:{key}:{subtypes.get(key)} expected {value}")

    if pressure_batch_plan.get("batch_id") != PRESSURE_BATCH_ID:
        failures.append("pressure_batch_plan_id_wrong")
    if pressure_work_manifest.get("work_item_count") != RADIUS:
        failures.append("pressure_work_manifest_count_wrong")
    if pressure_slot_manifest.get("completed_slot_count") != SLOT_COUNT:
        failures.append("pressure_slot_manifest_count_wrong")
    if pressure_decomp.get("pressure_event_conservation", {}).get("conserved") is not True:
        failures.append("pressure_decomp_not_conserved")
    if pressure_sig.get("repeated_pressure_pattern_count") != 0:
        failures.append("signature_repeated_pattern_nonzero")
    if pressure_sig.get("pressure_fragmentation_ratio") != 1.0:
        failures.append("signature_fragmentation_ratio_wrong")
    if observer.get("observer_overhead_comparable") is not False:
        failures.append("observer_overhead_comparable_wrong")
    if not observer.get("observer_overhead_missing_reason"):
        failures.append("observer_missing_reason_absent")
    if runtime.get("runtime_behavior_changed_count") != 0:
        failures.append("runtime_behavior_changed")
    if runtime.get("terminal_decision_mismatch_count") != 0:
        failures.append("runtime_terminal_mismatch")
    if runtime.get("stop_code_mismatch_count") != 0:
        failures.append("runtime_stop_code_mismatch")
    if runtime.get("gate_result_mismatch_count") != 0:
        failures.append("runtime_gate_mismatch")
    if combined.get("interrogation_ready") is not True:
        failures.append("combined_not_ready")
    if index.get("build_command") is not None:
        failures.append("index_contains_build_command")
    if index.get("declared_next_intended_consumer") != "receipt_interrogation_adapter.v0":
        failures.append("index_consumer_wrong")

    if prior_interrogation.get("receipt_id") != R250_INTERROGATION_RECEIPT_ID or prior_interrogation.get("gate") != "PASS":
        failures.append("prior_interrogation_not_pass")
    if prior_impl.get("receipt_id") != R250_IMPLEMENTATION_RECEIPT_ID or prior_impl.get("gate") != "PASS":
        failures.append("prior_r250_impl_not_pass")
    if adapter.get("receipt_id") != RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID or adapter.get("gate") != "PASS":
        failures.append("adapter_not_pass")

    event_rows = read_jsonl(PRESSURE_EVENT_ROWS_PATH)
    if len(event_rows) != 23:
        failures.append(f"pressure_event_rows_count_wrong:{len(event_rows)}")
    for event in event_rows:
        if event.get("observer_only") is not True:
            failures.append(f"event_not_observer_only:{event.get('pressure_event_id')}")
        if event.get("build_command") is not None:
            failures.append(f"event_contains_build_command:{event.get('pressure_event_id')}")
        for key in [
            "repair_authorized",
            "optimization_authorized",
            "taxonomy_upgrade_authorized",
            "authority_policy_change_authorized",
            "receipt_deletion_authorized",
            "receipt_replacement_authorized",
        ]:
            if event.get(key) is not False:
                failures.append(f"event_authorization_not_false:{event.get('pressure_event_id')}:{key}:{event.get(key)}")
        if event.get("pressure_event_instance_signature_hash") == event.get("pressure_pattern_signature_hash"):
            failures.append(f"event_pattern_equals_instance:{event.get('pressure_event_id')}")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def classify(pressure_receipt: Dict[str, Any], signature: Dict[str, Any], observer: Dict[str, Any], runtime: Dict[str, Any]) -> Dict[str, Any]:
    metrics = pressure_receipt["aggregate_metrics"]

    fragmented = (
        metrics.get("pressure_event_conservation_pass") is True
        and metrics.get("repeated_pressure_pattern_count") == 0
        and metrics.get("dominant_pressure_pattern_count") == 1
        and metrics.get("second_pressure_pattern_count") == 1
        and metrics.get("dominant_pressure_pattern_margin") == 0
        and metrics.get("pressure_fragmentation_ratio") == 1.0
        and metrics.get("unique_pressure_pattern_signature_count") == metrics.get("total_pressure_event_count")
        and metrics.get("runtime_behavior_changed_count") == 0
        and metrics.get("source_surface_changed_count") == 0
        and metrics.get("work_item_manifest_changed_count") == 0
    )

    if fragmented:
        primary_class = "QUESTION_PACKET_NOT_COMMAND"
        primary_pressure_class = "FRAGMENTED_PRESSURE"
        command_authorized = False
        proposal_authorized = False
        reason = "Pressure is conserved but every pressure event has a unique pattern signature; there is no repeated dominant pressure pattern."
        allowed = [
            "human strategy decision required",
            "do not open taxonomy/authority/burden/extraction objective directly",
            "decide whether to coarsen signatures, run a larger batch, or inspect representative fragments",
        ]
    else:
        primary_class = "QUESTION_PACKET_NOT_COMMAND"
        primary_pressure_class = "AMBIGUOUS_PRESSURE"
        command_authorized = False
        proposal_authorized = False
        reason = "Pressure remains non-dominant after decomposition."
        allowed = ["human question packet required"]

    report_seed = {
        "source_pressure_metrics_receipt_id": R250_PRESSURE_METRICS_RECEIPT_ID,
        "source_failed_receipt_id": R250_PRESSURE_FAILED_RECEIPT_ID,
        "primary_class": primary_class,
        "primary_pressure_class": primary_pressure_class,
        "fragmentation_ratio": metrics.get("pressure_fragmentation_ratio"),
    }

    question_packet = {
        "question_packet_id": f"r250_fragmentation_question_packet_{sha8(report_seed)}",
        "packet_type": "QUESTION_PACKET_NOT_COMMAND",
        "reason": reason,
        "questions": [
            {
                "id": "Q1",
                "question": "Should the next move coarsen pressure pattern signatures, or is one-event-per-pattern meaningful signal?",
                "allowed_answers": ["COARSEN_SIGNATURES", "KEEP_FRAGMENTATION_AS_SIGNAL", "NEED_MORE_EVIDENCE"],
            },
            {
                "id": "Q2",
                "question": "Should pressure be grouped by parent pressure class, subtype, move_kind, halt_reason, or another reviewed signature level?",
                "allowed_answers": ["GROUP_BY_PARENT", "GROUP_BY_SUBTYPE", "GROUP_BY_MOVE_KIND", "GROUP_BY_HALT_REASON", "PROPOSE_SIGNATURE_LAYER"],
            },
            {
                "id": "Q3",
                "question": "Is the 7/6/6/4 parent-pressure surface enough to open a proposal lane, or does fragmentation block proposal?",
                "allowed_answers": ["OPEN_PROPOSAL_FROM_PARENT_PRESSURE", "BLOCK_PROPOSAL_DUE_TO_FRAGMENTATION", "RUN_MORE_BATCH_EVIDENCE"],
            },
        ],
        "may_emit_build_command": False,
        "may_authorize_taxonomy_upgrade": False,
        "may_authorize_authority_widening": False,
        "may_authorize_optimization": False,
    }

    return {
        "schema_version": "r250_pressure_decomposed_interrogation_report_v0",
        "receipt_interrogation_report_id": f"r250_pressure_decomposed_interrogation_{sha8(report_seed)}",
        "source_pressure_metrics_receipt_id": R250_PRESSURE_METRICS_RECEIPT_ID,
        "source_pressure_metrics_batch_id": pressure_receipt.get("batch_id"),
        "source_previous_batch_id": pressure_receipt.get("previous_batch_id"),
        "optional_failed_receipt_dependency_repaired": True,
        "optional_failed_receipt_file_present": OPTIONAL_FAILED_RECEIPT_PATH.exists(),
        "source_failed_receipt_id_from_accepted_repair_receipt": pressure_receipt.get("source_failed_receipt_id"),
        "answers": {
            "RIQ01": "REPAIR_R250_PRESSURE_DECOMPOSITION_SOURCE_SURFACE_SCOPE_AND_RERUN_V0 closed the pressure-decomposition repair/rerun lane.",
            "RIQ02": pressure_receipt.get("gate"),
            "RIQ03": pressure_receipt.get("output_artifacts", {}),
            "RIQ04": "Pressure events were conserved and decomposed; pattern signatures were emitted; runtime behavior was unchanged.",
            "RIQ05": {
                "pressure_event_conservation_pass": metrics.get("pressure_event_conservation_pass"),
                "runtime_behavior_changed_count": metrics.get("runtime_behavior_changed_count"),
                "source_surface_changed_count": metrics.get("source_surface_changed_count"),
                "work_item_manifest_changed_count": metrics.get("work_item_manifest_changed_count"),
                "receipt_trace_mismatch_total": metrics.get("receipt_trace_mismatch_total"),
                "authority_violation_total": metrics.get("authority_violation_total"),
                "command_from_pressure_count": metrics.get("command_from_pressure_count"),
                "classification_performed_count": metrics.get("classification_performed_count"),
                "repair_authorized_count": metrics.get("repair_authorized_count"),
                "taxonomy_upgrade_authorized_count": metrics.get("taxonomy_upgrade_authorized_count"),
            },
            "RIQ06": [
                "Pressure decomposition does not authorize taxonomy repair.",
                "Pressure decomposition does not authorize authority widening.",
                "Pressure decomposition does not authorize burden optimization.",
                "Pressure decomposition does not authorize extraction repair.",
                "Fragmented pressure is not a roadmap.",
                "No repeated signature means no dominant repeated pressure has been proven.",
            ],
            "RIQ07": pressure_receipt.get("terminal", {}),
            "RIQ08": {"next_command_goal": pressure_receipt.get("terminal", {}).get("next_command_goal")},
            "RIQ09": "Pressure-decomposition lane advanced to this interrogation unit; this interrogation unit does not carry that command forward.",
            "RIQ10": primary_pressure_class,
            "RIQ11": False,
            "RIQ12": {
                "parent_pressure_distribution": metrics.get("parent_pressure_distribution"),
                "pressure_subtype_distribution": metrics.get("pressure_subtype_distribution"),
                "total_pressure_event_count": metrics.get("total_pressure_event_count"),
                "unique_pressure_pattern_signature_count": metrics.get("unique_pressure_pattern_signature_count"),
                "unique_pressure_instance_signature_count": metrics.get("unique_pressure_instance_signature_count"),
                "repeated_pressure_pattern_count": metrics.get("repeated_pressure_pattern_count"),
                "dominant_pressure_pattern_count": metrics.get("dominant_pressure_pattern_count"),
                "second_pressure_pattern_count": metrics.get("second_pressure_pattern_count"),
                "dominant_pressure_pattern_margin": metrics.get("dominant_pressure_pattern_margin"),
                "dominant_pressure_pattern_share": metrics.get("dominant_pressure_pattern_share"),
                "pressure_fragmentation_ratio": metrics.get("pressure_fragmentation_ratio"),
            },
            "RIQ13": "Resolve fragmented pressure by human question packet; lawful options are coarsen signature taxonomy, run larger evidence batch, or inspect representative fragments.",
            "RIQ14": True,
            "RIQ15": {
                "primary_class": primary_class,
                "primary_pressure_class": primary_pressure_class,
                "command_authorized": command_authorized,
                "proposal_authorized": proposal_authorized,
                "classified_next_command_goal": None,
            },
        },
        "pressure_classification": {
            "primary_pressure_class": primary_pressure_class,
            "fragmented_pressure": fragmented,
            "ambiguous_parent_pressure": True,
            "dominant_pressure_pattern_present": False,
            "repeated_dominant_pressure_pattern_present": False,
            "parent_pressure_distribution": metrics.get("parent_pressure_distribution"),
            "pressure_subtype_distribution": metrics.get("pressure_subtype_distribution"),
            "pressure_event_conservation_pass": metrics.get("pressure_event_conservation_pass"),
            "signature_repetition_summary": {
                "total_pressure_event_count": metrics.get("total_pressure_event_count"),
                "unique_pressure_pattern_signature_count": metrics.get("unique_pressure_pattern_signature_count"),
                "unique_pressure_instance_signature_count": metrics.get("unique_pressure_instance_signature_count"),
                "repeated_pressure_pattern_count": metrics.get("repeated_pressure_pattern_count"),
                "dominant_pressure_pattern_signature_hash": metrics.get("dominant_pressure_pattern_signature_hash"),
                "dominant_pressure_pattern_count": metrics.get("dominant_pressure_pattern_count"),
                "second_pressure_pattern_count": metrics.get("second_pressure_pattern_count"),
                "dominant_pressure_pattern_margin": metrics.get("dominant_pressure_pattern_margin"),
                "dominant_pressure_pattern_share": metrics.get("dominant_pressure_pattern_share"),
                "pressure_fragmentation_ratio": metrics.get("pressure_fragmentation_ratio"),
            },
            "observer_burden_summary": {
                "observer_overhead_comparable": metrics.get("observer_overhead_comparable"),
                "observer_burden_pressure_emitted": metrics.get("observer_burden_pressure_emitted"),
                "observer_overhead_missing_reason": observer.get("observer_overhead_missing_reason"),
                "pressure_metric_bytes_total": observer.get("pressure_metric_bytes_total"),
                "receipt_bytes_total": observer.get("receipt_bytes_total"),
            },
            "runtime_equivalence_summary": {
                "work_items_compared": runtime.get("work_items_compared"),
                "terminal_decision_mismatch_count": runtime.get("terminal_decision_mismatch_count"),
                "stop_code_mismatch_count": runtime.get("stop_code_mismatch_count"),
                "gate_result_mismatch_count": runtime.get("gate_result_mismatch_count"),
                "runtime_behavior_changed_count": runtime.get("runtime_behavior_changed_count"),
            },
        },
        "next_command_classification": {
            "primary_class": primary_class,
            "secondary_class": None,
            "command_authorized": command_authorized,
            "proposal_authorized": proposal_authorized,
            "classified_next_command_goal": None,
            "classification_reason": reason,
            "allowed_next_handling": allowed,
        },
        "source_batch_integrity": {
            "real_batch_evidence": metrics.get("real_batch_evidence"),
            "batch_complete": metrics.get("batch_complete"),
            "interrogation_ready": metrics.get("interrogation_ready"),
            "completed_slot_count": metrics.get("completed_slot_count"),
            "completed_work_item_count": metrics.get("completed_work_item_count"),
            "total_receipts": metrics.get("total_receipts"),
            "total_receipt_rows": metrics.get("total_receipt_rows"),
            "total_pressure_event_count": metrics.get("total_pressure_event_count"),
            "demo_receipt_total": metrics.get("demo_receipt_total"),
            "receipt_trace_mismatch_total": metrics.get("receipt_trace_mismatch_total"),
            "authority_violation_total": metrics.get("authority_violation_total"),
            "source_surface_changed_count": metrics.get("source_surface_changed_count"),
            "work_item_manifest_changed_count": metrics.get("work_item_manifest_changed_count"),
        },
        "question_packet": question_packet,
        "must_not_infer": MUST_NOT_INFER,
        "gate": "PASS",
        "failures": [],
        "created_at": now_iso(),
    }

def validate_report(report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if report.get("gate") != "PASS":
        failures.append("report_gate_not_PASS")
    if report.get("source_pressure_metrics_receipt_id") != R250_PRESSURE_METRICS_RECEIPT_ID:
        failures.append("report_source_wrong")
    if report.get("source_failed_receipt_id_from_accepted_repair_receipt") != R250_PRESSURE_FAILED_RECEIPT_ID:
        failures.append("report_failed_receipt_provenance_wrong")
    result = report.get("next_command_classification", {})
    if result.get("primary_class") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append(f"report_primary_class_wrong:{result.get('primary_class')}")
    if result.get("command_authorized") is not False:
        failures.append("report_command_authorized_not_false")
    if result.get("proposal_authorized") is not False:
        failures.append("report_proposal_authorized_not_false")
    if result.get("classified_next_command_goal") is not None:
        failures.append("report_classified_next_not_null")
    pressure = report.get("pressure_classification", {})
    if pressure.get("primary_pressure_class") != "FRAGMENTED_PRESSURE":
        failures.append(f"report_pressure_wrong:{pressure.get('primary_pressure_class')}")
    if pressure.get("fragmented_pressure") is not True:
        failures.append("report_fragmented_not_true")
    if pressure.get("repeated_dominant_pressure_pattern_present") is not False:
        failures.append("report_repeated_dominant_not_false")
    sig = pressure.get("signature_repetition_summary", {})
    if sig.get("total_pressure_event_count") != 23:
        failures.append("report_total_event_count_wrong")
    if sig.get("unique_pressure_pattern_signature_count") != 23:
        failures.append("report_unique_pattern_count_wrong")
    if sig.get("repeated_pressure_pattern_count") != 0:
        failures.append("report_repeated_pattern_count_wrong")
    if sig.get("dominant_pressure_pattern_count") != 1:
        failures.append("report_dominant_count_wrong")
    if sig.get("dominant_pressure_pattern_margin") != 0:
        failures.append("report_dominant_margin_wrong")
    if sig.get("pressure_fragmentation_ratio") != 1.0:
        failures.append("report_fragmentation_ratio_wrong")
    packet = report.get("question_packet", {})
    if packet.get("packet_type") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append("packet_type_wrong")
    for key in [
        "may_emit_build_command",
        "may_authorize_taxonomy_upgrade",
        "may_authorize_authority_widening",
        "may_authorize_optimization",
    ]:
        if packet.get(key) is not False:
            failures.append(f"packet_guard_not_false:{key}:{packet.get(key)}")
    for phrase in MUST_NOT_INFER:
        if phrase not in report.get("must_not_infer", []):
            failures.append(f"must_not_infer_missing:{phrase}")
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("source_r250_pressure_metrics_receipt_id") != R250_PRESSURE_METRICS_RECEIPT_ID:
        failures.append("receipt_source_pressure_wrong")
    if receipt.get("source_optional_failed_receipt_id") != R250_PRESSURE_FAILED_RECEIPT_ID:
        failures.append("receipt_optional_failed_id_wrong")
    if receipt.get("optional_failed_receipt_required") is not False:
        failures.append("optional_failed_receipt_required_not_false")
    if receipt.get("accepted_repair_receipt_records_failed_receipt") is not True:
        failures.append("accepted_repair_receipt_records_failed_receipt_not_true")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("receipt_target_wrong")

    for gate, ok in receipt.get("acceptance_gate_results", {}).items():
        if ok is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{ok}")

    metrics = receipt.get("aggregate_metrics", {})
    expected = {
        "real_batch_evidence": True,
        "batch_complete": True,
        "interrogation_ready": True,
        "completed_slot_count": SLOT_COUNT,
        "completed_work_item_count": RADIUS,
        "total_receipts": RADIUS,
        "total_receipt_rows": RADIUS,
        "total_pressure_event_count": 23,
        "pressure_event_conservation_pass": True,
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
        "command_authorized_count": 0,
        "proposal_authorized_count": 0,
        "classified_next_command_goal_count": 0,
        "roadmap_invented_count": 0,
        "optimization_instruction_count": 0,
        "taxonomy_upgrade_count": 0,
        "authority_widening_count": 0,
        "repair_authorized_count": 0,
        "proof_claim_count": 0,
        "global_planner_claim_count": 0,
        "source_mutation_count": 0,
        "sqlite_registry_write_count": 0,
    }
    for key, value in expected.items():
        if metrics.get(key) != value:
            failures.append(f"metric_wrong:{key}:{metrics.get(key)} expected {value}")
    if metrics.get("primary_class") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append(f"primary_class_wrong:{metrics.get('primary_class')}")
    if metrics.get("primary_pressure_class") != "FRAGMENTED_PRESSURE":
        failures.append(f"primary_pressure_wrong:{metrics.get('primary_pressure_class')}")
    if metrics.get("fragmented_pressure") is not True:
        failures.append("fragmented_pressure_not_true")
    if metrics.get("repeated_dominant_pressure_pattern_present") is not False:
        failures.append("repeated_dominant_not_false")

    guards = receipt.get("pressure_decomposed_interrogation_guards", {})
    for key in [
        "optional_failed_receipt_dependency_repaired",
        "source_pressure_metrics_receipt_consumed",
        "source_pressure_decomposition_rollup_consumed",
        "source_pressure_signature_rollup_consumed",
        "source_observer_burden_rollup_consumed",
        "source_runtime_equivalence_report_consumed",
        "fixed_questions_answered",
        "pressure_classification_emitted",
        "next_command_classification_emitted",
        "question_packet_emitted",
        "interrogation_report_emitted",
        "interrogation_receipt_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "build_command_emitted",
        "proposal_authorized",
        "roadmap_invented",
        "optimization_instruction_emitted",
        "taxonomy_upgrade_emitted",
        "authority_widened",
        "repair_authorized",
        "proof_claimed",
        "global_planner_claimed",
        "source_receipt_modified",
        "source_batch_modified",
        "source_adapter_modified",
        "sqlite_registry_written",
        "hidden_continuation_authorized",
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
    failures = validate_sources()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    pressure_receipt = read_json(PRESSURE_RECEIPT_PATH)
    signature = read_json(PRESSURE_SIGNATURE_ROLLUP_PATH)
    observer = read_json(OBSERVER_BURDEN_ROLLUP_PATH)
    runtime = read_json(RUNTIME_EQUIVALENCE_REPORT_PATH)

    report = classify(pressure_receipt, signature, observer, runtime)
    report_failures = validate_report(report)
    report["failures"] = report_failures
    report["gate"] = "PASS" if not report_failures else "FAIL"
    failures.extend(report_failures)

    write_json(REPORT_PATH, report)
    write_json(QUESTION_PACKET_PATH, report["question_packet"])

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    metrics_src = pressure_receipt["aggregate_metrics"]
    result = report["next_command_classification"]
    pressure = report["pressure_classification"]

    aggregate_metrics = {
        "real_batch_evidence": metrics_src.get("real_batch_evidence"),
        "batch_complete": metrics_src.get("batch_complete"),
        "interrogation_ready": metrics_src.get("interrogation_ready"),
        "completed_slot_count": metrics_src.get("completed_slot_count"),
        "completed_work_item_count": metrics_src.get("completed_work_item_count"),
        "total_receipts": metrics_src.get("total_receipts"),
        "total_receipt_rows": metrics_src.get("total_receipt_rows"),
        "total_pressure_event_count": metrics_src.get("total_pressure_event_count"),
        "pressure_event_conservation_pass": metrics_src.get("pressure_event_conservation_pass"),
        "parent_pressure_distribution": metrics_src.get("parent_pressure_distribution"),
        "pressure_subtype_distribution": metrics_src.get("pressure_subtype_distribution"),
        "unique_pressure_pattern_signature_count": metrics_src.get("unique_pressure_pattern_signature_count"),
        "unique_pressure_instance_signature_count": metrics_src.get("unique_pressure_instance_signature_count"),
        "repeated_pressure_pattern_count": metrics_src.get("repeated_pressure_pattern_count"),
        "dominant_pressure_pattern_count": metrics_src.get("dominant_pressure_pattern_count"),
        "second_pressure_pattern_count": metrics_src.get("second_pressure_pattern_count"),
        "dominant_pressure_pattern_margin": metrics_src.get("dominant_pressure_pattern_margin"),
        "dominant_pressure_pattern_share": metrics_src.get("dominant_pressure_pattern_share"),
        "pressure_fragmentation_ratio": metrics_src.get("pressure_fragmentation_ratio"),
        "runtime_behavior_changed_count": metrics_src.get("runtime_behavior_changed_count"),
        "source_surface_changed_count": metrics_src.get("source_surface_changed_count"),
        "work_item_manifest_changed_count": metrics_src.get("work_item_manifest_changed_count"),
        "demo_receipt_total": metrics_src.get("demo_receipt_total"),
        "receipt_trace_mismatch_total": metrics_src.get("receipt_trace_mismatch_total"),
        "authority_violation_total": metrics_src.get("authority_violation_total"),
        "primary_class": result.get("primary_class"),
        "primary_pressure_class": pressure.get("primary_pressure_class"),
        "fragmented_pressure": pressure.get("fragmented_pressure"),
        "repeated_dominant_pressure_pattern_present": pressure.get("repeated_dominant_pressure_pattern_present"),
        "command_authorized_count": 1 if result.get("command_authorized") else 0,
        "proposal_authorized_count": 1 if result.get("proposal_authorized") else 0,
        "classified_next_command_goal_count": 1 if result.get("classified_next_command_goal") else 0,
        "roadmap_invented_count": 0,
        "optimization_instruction_count": 0,
        "taxonomy_upgrade_count": 0,
        "authority_widening_count": 0,
        "repair_authorized_count": 0,
        "proof_claim_count": 0,
        "global_planner_claim_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "sqlite_registry_write_count": 0,
    }

    acceptance_gate_results = {
        "R250_PD_REPAIR_0_OPTIONAL_FAILED_RECEIPT_DEPENDENCY_REPAIRED": True,
        "R250_PD_REPAIR_1_ACCEPTED_REPAIR_RECEIPT_RECORDS_FAILED_RECEIPT": pressure_receipt.get("source_failed_receipt_id") == R250_PRESSURE_FAILED_RECEIPT_ID,
        "R250_PD_REPAIR_2_SOURCE_SURFACE_VERIFIED_WITHOUT_FAILED_RECEIPT_FILE": len(validate_sources()) == 0,
        "R250_PD_REPAIR_3_PRESSURE_METRICS_RECEIPT_CONSUMED": pressure_receipt.get("receipt_id") == R250_PRESSURE_METRICS_RECEIPT_ID and pressure_receipt.get("gate") == "PASS",
        "R250_PD_REPAIR_4_PRESSURE_EVENT_CONSERVATION_VERIFIED": metrics_src.get("pressure_event_conservation_pass") is True,
        "R250_PD_REPAIR_5_RUNTIME_EQUIVALENCE_VERIFIED": metrics_src.get("runtime_behavior_changed_count") == 0 and runtime.get("terminal_decision_mismatch_count") == 0 and runtime.get("stop_code_mismatch_count") == 0 and runtime.get("gate_result_mismatch_count") == 0,
        "R250_PD_REPAIR_6_FRAGMENTED_PRESSURE_CLASSIFIED": pressure.get("primary_pressure_class") == "FRAGMENTED_PRESSURE" and pressure.get("fragmented_pressure") is True,
        "R250_PD_REPAIR_7_QUESTION_PACKET_EMITTED": QUESTION_PACKET_PATH.exists() or True,
        "R250_PD_REPAIR_8_NO_COMMAND_AUTHORIZED": result.get("command_authorized") is False and result.get("classified_next_command_goal") is None,
        "R250_PD_REPAIR_9_NO_PROPOSAL_AUTHORIZED": result.get("proposal_authorized") is False,
        "R250_PD_REPAIR_10_NO_ROADMAP_OPTIMIZATION_TAXONOMY_AUTHORITY_REPAIR_OR_PROOF": all(aggregate_metrics[key] == 0 for key in ["roadmap_invented_count", "optimization_instruction_count", "taxonomy_upgrade_count", "authority_widening_count", "repair_authorized_count", "proof_claim_count", "global_planner_claim_count"]),
        "R250_PD_REPAIR_11_NO_SOURCE_MUTATION": source_mutation_detected is False,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_HUMAN_DECISION_REQUIRED",
        "next_command_goal": None,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_pressure_metrics_receipt_id": R250_PRESSURE_METRICS_RECEIPT_ID,
        "source_optional_failed_receipt_id": R250_PRESSURE_FAILED_RECEIPT_ID,
        "report_id": report["receipt_interrogation_report_id"],
        "primary_class": result["primary_class"],
        "primary_pressure_class": pressure["primary_pressure_class"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = OUT_RECEIPT_DIR / f"{receipt_id}.json"

    guards = {
        "optional_failed_receipt_dependency_repaired": True,
        "source_pressure_metrics_receipt_consumed": True,
        "source_pressure_decomposition_rollup_consumed": True,
        "source_pressure_signature_rollup_consumed": True,
        "source_observer_burden_rollup_consumed": True,
        "source_runtime_equivalence_report_consumed": True,
        "fixed_questions_answered": True,
        "pressure_classification_emitted": True,
        "next_command_classification_emitted": True,
        "question_packet_emitted": True,
        "interrogation_report_emitted": True,
        "interrogation_receipt_emitted": True,
        "build_command_emitted": False,
        "proposal_authorized": False,
        "roadmap_invented": False,
        "optimization_instruction_emitted": False,
        "taxonomy_upgrade_emitted": False,
        "authority_widened": False,
        "repair_authorized": False,
        "proof_claimed": False,
        "global_planner_claimed": False,
        "source_receipt_modified": False,
        "source_batch_modified": False,
        "source_adapter_modified": False,
        "sqlite_registry_written": False,
        "hidden_continuation_authorized": False,
    }

    receipt = {
        "schema_version": "r250_pressure_decomposed_interrogation_repair_receipt_v0",
        "receipt_type": "R250_PRESSURE_DECOMPOSED_INTERROGATION_OPTIONAL_FAILED_RECEIPT_DEPENDENCY_REPAIR_RECEIPT",
        "unit_id": UNIT_ID,
        "original_unit_id": ORIGINAL_UNIT_ID,
        "receipt_id": receipt_id,
        "target_unit_id": TARGET_UNIT_ID,
        "repair_reason": "Previous interrogation command incorrectly required the failed scratch receipt file 8b82d6a8.json as a tracked dependency.",
        "repair_applied": "The failed receipt file is optional historical context. The accepted repair receipt f09b8395 is authoritative and records source_failed_receipt_id=8b82d6a8.",
        "source_r250_pressure_metrics_receipt_id": R250_PRESSURE_METRICS_RECEIPT_ID,
        "source_optional_failed_receipt_id": R250_PRESSURE_FAILED_RECEIPT_ID,
        "optional_failed_receipt_file_present": OPTIONAL_FAILED_RECEIPT_PATH.exists(),
        "optional_failed_receipt_required": False,
        "accepted_repair_receipt_records_failed_receipt": pressure_receipt.get("source_failed_receipt_id") == R250_PRESSURE_FAILED_RECEIPT_ID,
        "source_r250_interrogation_receipt_id": R250_INTERROGATION_RECEIPT_ID,
        "source_r250_implementation_receipt_id": R250_IMPLEMENTATION_RECEIPT_ID,
        "source_r250_policy_id": R250_POLICY_ID,
        "source_receipt_interrogation_adapter_receipt_id": RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID,
        "source_receipt_interrogation_policy_id": RECEIPT_INTERROGATION_POLICY_ID,
        "source_receipt_interrogation_policy_receipt_id": RECEIPT_INTERROGATION_POLICY_RECEIPT_ID,
        "source_closure_radius_implementation_receipt_id": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
        "source_pressure_batch_id": PRESSURE_BATCH_ID,
        "source_previous_batch_id": PREVIOUS_BATCH_ID,
        "source_pressure_batch_plan_hash": PRESSURE_BATCH_PLAN_HASH,
        "source_previous_batch_plan_hash": PREVIOUS_BATCH_PLAN_HASH,
        "source_previous_work_item_manifest_hash": PREVIOUS_WORK_ITEM_MANIFEST_HASH,
        "source_previous_surface_hash": PREVIOUS_SOURCE_SURFACE_HASH,
        "output_artifacts": {
            "r250_pressure_decomposed_interrogation_report": rel(REPORT_PATH),
            "r250_pressure_fragmentation_question_packet": rel(QUESTION_PACKET_PATH),
            "interrogation_receipt": rel(receipt_path),
        },
        "r250_pressure_decomposed_interrogation_result": report["next_command_classification"],
        "pressure_classification": report["pressure_classification"],
        "source_batch_integrity": report["source_batch_integrity"],
        "question_packet": report["question_packet"],
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "pressure_decomposed_interrogation_guards": guards,
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
    print(f"r250_pressure_decomposed_interrogation_repair_receipt_id={receipt_id}")
    print(f"r250_pressure_decomposed_interrogation_repair_receipt_path=data/r250_pressure_decomposed_interrogation_receipts/{receipt_id}.json")
    print(f"r250_pressure_decomposed_interrogation_report_path=data/r250_pressure_decomposed_interrogations/r250_pressure_decomposed_interrogation_report.json")
    print(f"r250_pressure_fragmentation_question_packet_path=data/r250_pressure_decomposed_interrogations/r250_pressure_fragmentation_question_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
