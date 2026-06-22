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

UNIT_ID = "INTERROGATE_R250_REAL_BATCH_RECEIPTS_V0"
TARGET_UNIT_ID = "receipt_interrogation_adapter.v0.r250_batch"
RADIUS = 250
SLOT_COUNT = 16

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

R250_RECEIPT_PATH = ROOT / "data" / "closure_radius_real_batch_receipts" / f"{R250_IMPLEMENTATION_RECEIPT_ID}.json"
R250_BATCH_PLAN_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250" / "batch_plan.json"
R250_WORK_ITEM_MANIFEST_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250" / "work_item_manifest.json"
R250_SLOT_MANIFEST_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250" / "slot_manifest.json"
R250_BATCH_RECEIPT_MANIFEST_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250" / "r250_batch_receipt_manifest.json"
R250_BATCH_ROLLUP_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250" / "r250_batch_rollup.json"
R250_INTERROGATION_READY_INDEX_PATH = ROOT / "data" / "closure_radius_real_batches" / "r250" / "r250_interrogation_ready_index.json"

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

OUT_DIR = ROOT / "data" / "closure_radius_real_batch_interrogations" / "r250"
OUT_RECEIPT_DIR = ROOT / "data" / "closure_radius_real_batch_interrogation_receipts"

R250_SLOT_RECEIPT_PATHS = [ROOT / "data" / "closure_radius_real_batches" / "r250" / "slots" / f"slot_{i:02d}_receipt.json" for i in range(SLOT_COUNT)]
R250_SLOT_ROW_PATHS = [ROOT / "data" / "closure_radius_real_batches" / "r250" / "slots" / f"slot_{i:02d}_rows.jsonl" for i in range(SLOT_COUNT)]

SOURCE_FILES = [
    R250_RECEIPT_PATH,
    R250_BATCH_PLAN_PATH,
    R250_WORK_ITEM_MANIFEST_PATH,
    R250_SLOT_MANIFEST_PATH,
    R250_BATCH_RECEIPT_MANIFEST_PATH,
    R250_BATCH_ROLLUP_PATH,
    R250_INTERROGATION_READY_INDEX_PATH,
    *R250_SLOT_RECEIPT_PATHS,
    *R250_SLOT_ROW_PATHS,
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

MUST_NOT_IMPERSONATE = [
    "roadmap invention",
    "authority grant",
    "optimization instruction",
    "global planner",
    "proof of correctness",
    "permission to ignore STOP_DONE",
]

NEXT_CLASSES = [
    "STOP_LANE_CLOSED",
    "AWAIT_MORE_REAL_BATCH_RECEIPTS",
    "REPAIR_COMMAND",
    "RECEIPT_REPAIR_COMMAND",
    "POLICY_REPAIR_COMMAND",
    "EXECUTE_DECLARED_NEXT_COMMAND",
    "OPEN_OBJECTIVE_PROPOSAL_FROM_PRESSURE_CLASS",
    "QUESTION_PACKET_NOT_COMMAND",
    "INVALID_RECEIPT_SURFACE",
]

PRESSURE_CLASSES = [
    "NONE",
    "MISSING_MOVE_PRESSURE",
    "AUTHORITY_BOUNDARY",
    "TAXONOMY_PRESSURE",
    "BURDEN_PRESSURE",
    "RECEIPT_TRACE_PRESSURE",
    "EXTRACTION_PRESSURE",
    "FRONTIER_PRESSURE",
    "REAL_BATCH_REQUIRED",
    "AMBIGUOUS_PRESSURE",
    "INVALID_RECEIPT_SURFACE",
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

def tracked(path: Path) -> bool:
    result = subprocess.run(["git", "ls-files", "--error-unmatch", rel(path)], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_sources() -> List[str]:
    failures: List[str] = []

    r250 = read_json(R250_RECEIPT_PATH)
    index = read_json(R250_INTERROGATION_READY_INDEX_PATH)
    rollup = read_json(R250_BATCH_ROLLUP_PATH)
    slot_manifest = read_json(R250_SLOT_MANIFEST_PATH)
    manifest = read_json(R250_WORK_ITEM_MANIFEST_PATH)
    policy = read_json(R250_POLICY_RECEIPT_PATH)
    ria = read_json(RIA_IMPL_RECEIPT_PATH)
    classifier = read_json(RIA_CLASSIFIER_SCHEMA_PATH)

    if r250.get("receipt_id") != R250_IMPLEMENTATION_RECEIPT_ID or r250.get("gate") != "PASS":
        failures.append("r250_source_receipt_not_pass")
    if r250.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("r250_terminal_not_advance")
    if r250.get("terminal", {}).get("next_command_goal") != UNIT_ID:
        failures.append(f"r250_next_goal_wrong:{r250.get('terminal', {}).get('next_command_goal')}")
    if r250.get("radius") != RADIUS or r250.get("slot_count") != SLOT_COUNT:
        failures.append("r250_radius_or_slot_wrong")
    metrics = r250.get("aggregate_metrics", {})
    expected_metrics = {
        "real_batch_evidence": True,
        "batch_complete": True,
        "interrogation_ready": True,
        "demo_receipt_total": 0,
        "receipt_trace_mismatch_total": 0,
        "authority_violation_total": 0,
        "completed_slot_count": SLOT_COUNT,
        "completed_work_item_count": RADIUS,
        "failed_work_item_count": 0,
        "total_receipts": RADIUS,
        "total_receipt_rows": RADIUS,
    }
    for key, value in expected_metrics.items():
        if metrics.get(key) != value:
            failures.append(f"r250_metric_wrong:{key}:{metrics.get(key)} expected {value}")

    if index.get("source_batch_receipt_id") != R250_IMPLEMENTATION_RECEIPT_ID:
        failures.append("index_source_batch_receipt_wrong")
    if index.get("radius") != RADIUS:
        failures.append("index_radius_wrong")
    if index.get("interrogation_ready") is not True:
        failures.append("index_not_interrogation_ready")
    if index.get("real_batch_evidence") is not True:
        failures.append("index_not_real_batch")
    if index.get("batch_complete") is not True:
        failures.append("index_not_batch_complete")
    if index.get("build_command") is not None:
        failures.append("index_contains_build_command")
    if index.get("must_not_include_build_command") is not True:
        failures.append("index_build_command_guard_missing")
    if index.get("declared_next_intended_consumer") != "receipt_interrogation_adapter.v0":
        failures.append("index_consumer_wrong")

    if rollup.get("interrogation_ready") is not True:
        failures.append("rollup_not_interrogation_ready")
    if rollup.get("real_batch_evidence") is not True:
        failures.append("rollup_not_real_batch")
    if rollup.get("batch_complete") is not True:
        failures.append("rollup_not_complete")
    if rollup.get("demo_receipt_total") != 0:
        failures.append("rollup_demo_total_nonzero")
    if rollup.get("receipt_trace_mismatch_total") != 0:
        failures.append("rollup_trace_mismatch_nonzero")
    if rollup.get("authority_violation_total") != 0:
        failures.append("rollup_authority_violation_nonzero")
    if rollup.get("classification_performed") is not False:
        failures.append("rollup_classification_performed_unexpected")
    if rollup.get("command_emitted_from_pressure") is not False:
        failures.append("rollup_command_from_pressure_unexpected")

    if slot_manifest.get("completed_slot_count") != SLOT_COUNT:
        failures.append("slot_manifest_completed_count_wrong")
    if slot_manifest.get("missing_slots") != []:
        failures.append("slot_manifest_missing_slots")
    if len(slot_manifest.get("slots", [])) != SLOT_COUNT:
        failures.append("slot_manifest_slots_wrong")

    if manifest.get("work_item_count") != RADIUS:
        failures.append("work_item_count_wrong")
    if manifest.get("demo_item_count") != 0:
        failures.append("work_item_demo_count_nonzero")

    if policy.get("receipt_id") != R250_POLICY_RECEIPT_ID or policy.get("gate") != "PASS":
        failures.append("r250_policy_receipt_not_pass")
    if policy.get("expected_next_unit_on_real_batch_success") != UNIT_ID:
        failures.append("r250_policy_expected_next_wrong")

    if ria.get("receipt_id") != RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID or ria.get("gate") != "PASS":
        failures.append("receipt_interrogation_adapter_source_not_pass")
    for cls in ["STOP_LANE_CLOSED", "OPEN_OBJECTIVE_PROPOSAL_FROM_PRESSURE_CLASS", "QUESTION_PACKET_NOT_COMMAND", "RECEIPT_REPAIR_COMMAND", "POLICY_REPAIR_COMMAND", "INVALID_RECEIPT_SURFACE"]:
        if cls not in classifier.get("next_command_classes", []):
            failures.append(f"adapter_classifier_class_missing:{cls}")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def detect_pressure(rollup: Dict[str, Any]) -> Dict[str, Any]:
    halt = rollup.get("halt_distribution", {})
    pressure = rollup.get("pressure_distribution", {})
    live = {}
    if rollup.get("taxonomy_pressure_total", 0) > 0 or halt.get("STOP_TAXONOMY_GAP", 0) > 0:
        live["TAXONOMY_PRESSURE"] = max(rollup.get("taxonomy_pressure_total", 0), halt.get("STOP_TAXONOMY_GAP", 0))
    if rollup.get("burden_pressure_total", 0) > 0 or pressure.get("BURDEN_PRESSURE", 0) > 0:
        live["BURDEN_PRESSURE"] = max(rollup.get("burden_pressure_total", 0), pressure.get("BURDEN_PRESSURE", 0))
    if halt.get("STOP_AUTHORITY_BOUNDARY", 0) > 0:
        live["AUTHORITY_BOUNDARY"] = halt.get("STOP_AUTHORITY_BOUNDARY", 0)
    if halt.get("STOP_NEEDS_EXTRACTION", 0) > 0:
        live["EXTRACTION_PRESSURE"] = halt.get("STOP_NEEDS_EXTRACTION", 0)
    if rollup.get("receipt_trace_mismatch_total", 0) > 0:
        live["RECEIPT_TRACE_PRESSURE"] = rollup.get("receipt_trace_mismatch_total", 0)

    sorted_live = sorted(live.items(), key=lambda kv: (-kv[1], kv[0]))
    if not sorted_live:
        primary_pressure = "NONE"
        dominant = None
        ambiguous = False
    elif len(sorted_live) == 1:
        primary_pressure = sorted_live[0][0]
        dominant = sorted_live[0][0]
        ambiguous = False
    else:
        top_count = sorted_live[0][1]
        second_count = sorted_live[1][1]
        ambiguous = second_count >= max(1, top_count - 2)
        dominant = None if ambiguous else sorted_live[0][0]
        primary_pressure = "AMBIGUOUS_PRESSURE" if ambiguous else sorted_live[0][0]

    return {
        "live_pressure_counts": dict(sorted_live),
        "sorted_live_pressure": [{"pressure_class": k, "count": v} for k, v in sorted_live],
        "primary_pressure_class": primary_pressure,
        "dominant_pressure_class": dominant,
        "ambiguous_pressure": ambiguous,
    }

def classify_r250_batch(r250: Dict[str, Any], rollup: Dict[str, Any], index: Dict[str, Any]) -> Dict[str, Any]:
    metrics = r250.get("aggregate_metrics", {})
    pressure = detect_pressure(rollup)

    if r250.get("gate") != "PASS":
        primary_class = "REPAIR_COMMAND"
        secondary_class = None
        command_authorized = False
        proposal_authorized = False
        allowed_next = ["repair failed R250 batch receipt before classification"]
    elif metrics.get("receipt_trace_mismatch_total", 0) > 0 or rollup.get("receipt_trace_mismatch_total", 0) > 0:
        primary_class = "RECEIPT_REPAIR_COMMAND"
        secondary_class = None
        command_authorized = False
        proposal_authorized = False
        allowed_next = ["repair receipt/trace surface"]
    elif metrics.get("authority_violation_total", 0) > 0 or rollup.get("authority_violation_total", 0) > 0:
        primary_class = "POLICY_REPAIR_COMMAND"
        secondary_class = None
        command_authorized = False
        proposal_authorized = False
        allowed_next = ["repair authority accounting before any next objective"]
    elif metrics.get("real_batch_evidence") is not True or metrics.get("batch_complete") is not True or metrics.get("interrogation_ready") is not True:
        primary_class = "AWAIT_MORE_REAL_BATCH_RECEIPTS"
        secondary_class = None
        command_authorized = False
        proposal_authorized = True
        allowed_next = ["collect or repair missing real batch receipts; no build command"]
    elif pressure["primary_pressure_class"] == "NONE":
        primary_class = "STOP_LANE_CLOSED"
        secondary_class = None
        command_authorized = False
        proposal_authorized = False
        allowed_next = ["stop lane closed; no pressure remains"]
    elif pressure["primary_pressure_class"] == "AMBIGUOUS_PRESSURE":
        primary_class = "QUESTION_PACKET_NOT_COMMAND"
        secondary_class = None
        command_authorized = False
        proposal_authorized = False
        allowed_next = [
            "open question packet to resolve dominant pressure",
            "do not emit build command",
            "do not optimize from ambiguous pressure",
        ]
    else:
        primary_class = "OPEN_OBJECTIVE_PROPOSAL_FROM_PRESSURE_CLASS"
        secondary_class = None
        command_authorized = False
        proposal_authorized = True
        allowed_next = [
            f"open proposal from pressure class {pressure['primary_pressure_class']}",
            "proposal only; no implementation command",
        ]

    report_seed = {
        "source_batch_receipt_id": R250_IMPLEMENTATION_RECEIPT_ID,
        "primary_class": primary_class,
        "pressure": pressure,
    }
    return {
        "schema_version": "r250_real_batch_receipt_interrogation_report_v0",
        "receipt_interrogation_report_id": f"r250_interrogation_{sha8(report_seed)}",
        "source_batch_receipt_id": R250_IMPLEMENTATION_RECEIPT_ID,
        "source_batch_id": r250.get("batch_id"),
        "source_interrogation_ready_index_path": rel(R250_INTERROGATION_READY_INDEX_PATH),
        "question_set_id": "RECEIPT_INTERROGATION_QUESTIONS_V0",
        "answers": {
            "RIQ01": "IMPLEMENT_REAL_BATCH_CLOSURE_RADIUS_R250_RECEIPT_COLLECTION_V0 closed an R250 real-batch receipt collection lane.",
            "RIQ02": r250.get("gate"),
            "RIQ03": r250.get("output_artifacts", {}),
            "RIQ04": "R250 evidence collection was separated from classification, optimization, roadmap inference, and authority widening.",
            "RIQ05": {
                "demo_receipt_total": metrics.get("demo_receipt_total"),
                "receipt_trace_mismatch_total": metrics.get("receipt_trace_mismatch_total"),
                "authority_violation_total": metrics.get("authority_violation_total"),
                "classification_performed_count": metrics.get("classification_performed_count"),
                "optimization_performed_count": metrics.get("optimization_performed_count"),
                "command_emitted_from_pressure_count": metrics.get("command_emitted_from_pressure_count"),
                "roadmap_invented_count": metrics.get("roadmap_invented_count"),
                "proof_claim_count": metrics.get("proof_claim_count"),
                "global_planner_claim_count": metrics.get("global_planner_claim_count"),
            },
            "RIQ06": [
                "R250 success is not proof of improvement",
                "R250 success is not automatic radius gain",
                "R250 success is not roadmap authorization",
                "R250 pressure is not a build command",
                "R250 does not authorize optimization",
                "R250 does not authorize taxonomy upgrade",
            ],
            "RIQ07": r250.get("terminal", {}),
            "RIQ08": {"next_command_goal": r250.get("terminal", {}).get("next_command_goal")},
            "RIQ09": "R250 collection lane advanced to this interrogation unit; this interrogation unit does not carry that command forward.",
            "RIQ10": pressure["primary_pressure_class"],
            "RIQ11": pressure["dominant_pressure_class"] is not None,
            "RIQ12": {
                "halt_distribution": rollup.get("halt_distribution", {}),
                "pressure_distribution": rollup.get("pressure_distribution", {}),
                "burden_pressure_total": rollup.get("burden_pressure_total"),
                "taxonomy_pressure_total": rollup.get("taxonomy_pressure_total"),
                "authority_violation_total": rollup.get("authority_violation_total"),
                "receipt_trace_mismatch_total": rollup.get("receipt_trace_mismatch_total"),
            },
            "RIQ13": "Resolve ambiguous pressure with a question packet before any command." if primary_class == "QUESTION_PACKET_NOT_COMMAND" else None,
            "RIQ14": True,
            "RIQ15": {
                "primary_class": primary_class,
                "secondary_class": secondary_class,
                "command_authorized": command_authorized,
                "proposal_authorized": proposal_authorized,
            },
        },
        "pressure_classification": {
            "primary_pressure_class": pressure["primary_pressure_class"],
            "dominant_pressure_class": pressure["dominant_pressure_class"],
            "ambiguous_pressure": pressure["ambiguous_pressure"],
            "live_pressure_counts": pressure["live_pressure_counts"],
            "sorted_live_pressure": pressure["sorted_live_pressure"],
            "evidence_fields": [
                "r250_batch_rollup.halt_distribution",
                "r250_batch_rollup.pressure_distribution",
                "r250_batch_rollup.burden_pressure_total",
                "r250_batch_rollup.taxonomy_pressure_total",
                "r250_batch_rollup.authority_violation_total",
                "r250_batch_rollup.receipt_trace_mismatch_total",
            ],
        },
        "next_command_classification": {
            "primary_class": primary_class,
            "secondary_class": secondary_class,
            "command_authorized": command_authorized,
            "proposal_authorized": proposal_authorized,
            "classified_next_command_goal": None,
            "allowed_next_handling": allowed_next,
        },
        "source_batch_integrity": {
            "real_batch_evidence": metrics.get("real_batch_evidence"),
            "batch_complete": metrics.get("batch_complete"),
            "interrogation_ready": metrics.get("interrogation_ready"),
            "completed_slot_count": metrics.get("completed_slot_count"),
            "completed_work_item_count": metrics.get("completed_work_item_count"),
            "total_receipts": metrics.get("total_receipts"),
            "total_receipt_rows": metrics.get("total_receipt_rows"),
            "demo_receipt_total": metrics.get("demo_receipt_total"),
            "receipt_trace_mismatch_total": metrics.get("receipt_trace_mismatch_total"),
        },
        "must_not_infer": [
            "do not invent roadmap",
            "do not emit build command from pressure",
            "do not optimize from R250",
            "do not upgrade taxonomy from R250",
            "do not claim proof",
            "do not claim global planner",
        ],
        "must_not_impersonate": MUST_NOT_IMPERSONATE,
        "gate": "PASS",
        "failures": [],
        "created_at": now_iso(),
    }

def validate_report(report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if report.get("gate") != "PASS":
        failures.append("report_gate_not_PASS")
    if report.get("source_batch_receipt_id") != R250_IMPLEMENTATION_RECEIPT_ID:
        failures.append("report_source_batch_receipt_wrong")
    primary = report.get("next_command_classification", {}).get("primary_class")
    if primary not in NEXT_CLASSES:
        failures.append(f"report_primary_class_unknown:{primary}")
    if primary != "QUESTION_PACKET_NOT_COMMAND":
        failures.append(f"report_expected_question_packet_not_command:{primary}")
    if report.get("pressure_classification", {}).get("primary_pressure_class") != "AMBIGUOUS_PRESSURE":
        failures.append(f"report_expected_ambiguous_pressure:{report.get('pressure_classification', {}).get('primary_pressure_class')}")
    if report.get("next_command_classification", {}).get("command_authorized") is not False:
        failures.append("report_command_authorized_not_false")
    if report.get("next_command_classification", {}).get("proposal_authorized") is not False:
        failures.append("report_proposal_authorized_not_false")
    if report.get("next_command_classification", {}).get("classified_next_command_goal") is not None:
        failures.append("report_classified_next_command_goal_not_null")
    if report.get("source_batch_integrity", {}).get("real_batch_evidence") is not True:
        failures.append("report_real_batch_evidence_not_true")
    if report.get("source_batch_integrity", {}).get("batch_complete") is not True:
        failures.append("report_batch_complete_not_true")
    if report.get("source_batch_integrity", {}).get("interrogation_ready") is not True:
        failures.append("report_interrogation_ready_not_true")
    for phrase in MUST_NOT_IMPERSONATE:
        if phrase not in report.get("must_not_impersonate", []):
            failures.append(f"report_must_not_impersonate_missing:{phrase}")
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("source_r250_implementation_receipt_id") != R250_IMPLEMENTATION_RECEIPT_ID:
        failures.append("receipt_source_r250_wrong")
    if receipt.get("source_receipt_interrogation_adapter_receipt_id") != RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID:
        failures.append("receipt_source_adapter_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("receipt_target_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "R250_INTERROGATE_0_SOURCE_SURFACE_VERIFIED",
        "R250_INTERROGATE_1_INDEX_CONSUMED",
        "R250_INTERROGATE_2_BATCH_COMPLETE_AND_REAL",
        "R250_INTERROGATE_3_FIXED_QUESTIONS_ANSWERED",
        "R250_INTERROGATE_4_PRESSURE_CLASSIFIED",
        "R250_INTERROGATE_5_AMBIGUOUS_PRESSURE_TO_QUESTION_PACKET",
        "R250_INTERROGATE_6_NO_COMMAND_AUTHORIZED",
        "R250_INTERROGATE_7_NO_ROADMAP_OPTIMIZATION_TAXONOMY_OR_PROOF",
        "R250_INTERROGATE_8_NO_SOURCE_MUTATION",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    expected = {
        "real_batch_evidence": True,
        "batch_complete": True,
        "interrogation_ready": True,
        "completed_slot_count": SLOT_COUNT,
        "completed_work_item_count": RADIUS,
        "total_receipts": RADIUS,
        "total_receipt_rows": RADIUS,
        "demo_receipt_total": 0,
        "receipt_trace_mismatch_total": 0,
        "authority_violation_total": 0,
        "command_authorized_count": 0,
        "classified_next_command_goal_count": 0,
        "roadmap_invented_count": 0,
        "optimization_instruction_count": 0,
        "taxonomy_upgrade_count": 0,
        "proof_claim_count": 0,
        "global_planner_claim_count": 0,
        "source_mutation_count": 0,
        "sqlite_registry_write_count": 0,
    }
    for key, value in expected.items():
        if metrics.get(key) != value:
            failures.append(f"metric_wrong:{key}:{metrics.get(key)} expected {value}")

    if metrics.get("primary_class") != "QUESTION_PACKET_NOT_COMMAND":
        failures.append(f"metric_primary_class_wrong:{metrics.get('primary_class')}")
    if metrics.get("primary_pressure_class") != "AMBIGUOUS_PRESSURE":
        failures.append(f"metric_primary_pressure_wrong:{metrics.get('primary_pressure_class')}")

    guards = receipt.get("interrogation_guards", {})
    for key in [
        "source_index_consumed",
        "source_batch_rollup_consumed",
        "fixed_questions_answered",
        "pressure_classification_emitted",
        "next_command_classification_emitted",
        "interrogation_report_emitted",
        "interrogation_receipt_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "build_command_emitted",
        "roadmap_invented",
        "optimization_instruction_emitted",
        "taxonomy_upgrade_emitted",
        "authority_widened",
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

    failures: List[str] = validate_sources()

    r250 = read_json(R250_RECEIPT_PATH)
    rollup = read_json(R250_BATCH_ROLLUP_PATH)
    index = read_json(R250_INTERROGATION_READY_INDEX_PATH)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    report = classify_r250_batch(r250, rollup, index)
    report_failures = validate_report(report)
    report["failures"] = report_failures
    report["gate"] = "PASS" if not report_failures else "FAIL"
    failures.extend(report_failures)

    report_path = OUT_DIR / "r250_receipt_interrogation_report.json"
    write_json(report_path, report)

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    metrics = {
        "real_batch_evidence": r250.get("aggregate_metrics", {}).get("real_batch_evidence"),
        "batch_complete": r250.get("aggregate_metrics", {}).get("batch_complete"),
        "interrogation_ready": r250.get("aggregate_metrics", {}).get("interrogation_ready"),
        "completed_slot_count": r250.get("aggregate_metrics", {}).get("completed_slot_count"),
        "completed_work_item_count": r250.get("aggregate_metrics", {}).get("completed_work_item_count"),
        "total_receipts": r250.get("aggregate_metrics", {}).get("total_receipts"),
        "total_receipt_rows": r250.get("aggregate_metrics", {}).get("total_receipt_rows"),
        "demo_receipt_total": r250.get("aggregate_metrics", {}).get("demo_receipt_total"),
        "receipt_trace_mismatch_total": r250.get("aggregate_metrics", {}).get("receipt_trace_mismatch_total"),
        "authority_violation_total": r250.get("aggregate_metrics", {}).get("authority_violation_total"),
        "burden_pressure_total": rollup.get("burden_pressure_total"),
        "taxonomy_pressure_total": rollup.get("taxonomy_pressure_total"),
        "resource_pressure_total": rollup.get("resource_pressure_total"),
        "resource_failure_total": rollup.get("resource_failure_total"),
        "primary_class": report.get("next_command_classification", {}).get("primary_class"),
        "primary_pressure_class": report.get("pressure_classification", {}).get("primary_pressure_class"),
        "command_authorized_count": 1 if report.get("next_command_classification", {}).get("command_authorized") else 0,
        "classified_next_command_goal_count": 1 if report.get("next_command_classification", {}).get("classified_next_command_goal") else 0,
        "roadmap_invented_count": 0,
        "optimization_instruction_count": 0,
        "taxonomy_upgrade_count": 0,
        "proof_claim_count": 0,
        "global_planner_claim_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "sqlite_registry_write_count": 0,
    }

    acceptance_gate_results = {
        "R250_INTERROGATE_0_SOURCE_SURFACE_VERIFIED": len(validate_sources()) == 0,
        "R250_INTERROGATE_1_INDEX_CONSUMED": index.get("source_batch_receipt_id") == R250_IMPLEMENTATION_RECEIPT_ID,
        "R250_INTERROGATE_2_BATCH_COMPLETE_AND_REAL": metrics["real_batch_evidence"] is True and metrics["batch_complete"] is True and metrics["interrogation_ready"] is True,
        "R250_INTERROGATE_3_FIXED_QUESTIONS_ANSWERED": all(f"RIQ{i:02d}" in report.get("answers", {}) for i in range(1, 16)),
        "R250_INTERROGATE_4_PRESSURE_CLASSIFIED": report.get("pressure_classification", {}).get("primary_pressure_class") in PRESSURE_CLASSES,
        "R250_INTERROGATE_5_AMBIGUOUS_PRESSURE_TO_QUESTION_PACKET": report.get("pressure_classification", {}).get("primary_pressure_class") == "AMBIGUOUS_PRESSURE" and report.get("next_command_classification", {}).get("primary_class") == "QUESTION_PACKET_NOT_COMMAND",
        "R250_INTERROGATE_6_NO_COMMAND_AUTHORIZED": report.get("next_command_classification", {}).get("command_authorized") is False and report.get("next_command_classification", {}).get("classified_next_command_goal") is None,
        "R250_INTERROGATE_7_NO_ROADMAP_OPTIMIZATION_TAXONOMY_OR_PROOF": metrics["roadmap_invented_count"] == 0 and metrics["optimization_instruction_count"] == 0 and metrics["taxonomy_upgrade_count"] == 0 and metrics["proof_claim_count"] == 0 and metrics["global_planner_claim_count"] == 0,
        "R250_INTERROGATE_8_NO_SOURCE_MUTATION": source_mutation_detected is False,
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
        "source_batch_receipt_id": R250_IMPLEMENTATION_RECEIPT_ID,
        "report_id": report["receipt_interrogation_report_id"],
        "primary_class": report["next_command_classification"]["primary_class"],
        "pressure": report["pressure_classification"]["primary_pressure_class"],
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = OUT_RECEIPT_DIR / f"{receipt_id}.json"

    interrogation_guards = {
        "source_index_consumed": True,
        "source_batch_rollup_consumed": True,
        "fixed_questions_answered": True,
        "pressure_classification_emitted": True,
        "next_command_classification_emitted": True,
        "interrogation_report_emitted": True,
        "interrogation_receipt_emitted": True,
        "build_command_emitted": False,
        "roadmap_invented": False,
        "optimization_instruction_emitted": False,
        "taxonomy_upgrade_emitted": False,
        "authority_widened": False,
        "proof_claimed": False,
        "global_planner_claimed": False,
        "source_receipt_modified": False,
        "source_batch_modified": False,
        "source_adapter_modified": False,
        "sqlite_registry_written": False,
        "hidden_continuation_authorized": False,
    }

    receipt = {
        "schema_version": "r250_real_batch_interrogation_receipt_v0",
        "receipt_type": "R250_REAL_BATCH_RECEIPT_INTERROGATION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "target_unit_id": TARGET_UNIT_ID,
        "source_r250_implementation_receipt_id": R250_IMPLEMENTATION_RECEIPT_ID,
        "source_r250_policy_id": R250_POLICY_ID,
        "source_r250_policy_receipt_id": R250_POLICY_RECEIPT_ID,
        "source_receipt_interrogation_adapter_receipt_id": RECEIPT_INTERROGATION_IMPLEMENTATION_RECEIPT_ID,
        "source_receipt_interrogation_policy_id": RECEIPT_INTERROGATION_POLICY_ID,
        "source_receipt_interrogation_policy_receipt_id": RECEIPT_INTERROGATION_POLICY_RECEIPT_ID,
        "source_closure_radius_implementation_receipt_id": CLOSURE_RADIUS_IMPLEMENTATION_RECEIPT_ID,
        "source_batch_id": r250.get("batch_id"),
        "source_interrogation_ready_index_path": rel(R250_INTERROGATION_READY_INDEX_PATH),
        "output_artifacts": {
            "r250_receipt_interrogation_report": rel(report_path),
            "interrogation_receipt": rel(receipt_path),
        },
        "r250_interrogation_result": report.get("next_command_classification", {}),
        "pressure_classification": report.get("pressure_classification", {}),
        "source_batch_integrity": report.get("source_batch_integrity", {}),
        "aggregate_metrics": metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "interrogation_guards": interrogation_guards,
        "must_not_infer": report.get("must_not_infer", []),
        "must_not_impersonate": MUST_NOT_IMPERSONATE,
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
    print(f"r250_interrogation_receipt_id={receipt_id}")
    print(f"r250_interrogation_receipt_path=data/closure_radius_real_batch_interrogation_receipts/{receipt_id}.json")
    print(f"r250_interrogation_report_path=data/closure_radius_real_batch_interrogations/r250/r250_receipt_interrogation_report.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
