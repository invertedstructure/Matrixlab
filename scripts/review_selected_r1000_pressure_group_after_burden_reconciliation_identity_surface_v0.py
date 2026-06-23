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

UNIT_ID = "REVIEW_SELECTED_R1000_PRESSURE_GROUP_AFTER_BURDEN_RECONCILIATION_IDENTITY_SURFACE_V0"
TARGET_UNIT_ID = "r1000_selected_pressure_group_after_burden.identity_surface_review.v0"

SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID = "1cb51143"
SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID = "d3135cdb"
SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID = "dea88520"
SOURCE_SELECTION_RECEIPT_ID = "7c561212"
SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID = "38604be8"
SELECTED_PRESSURE_GROUP_ID = "f667fa03"

OUT_DIR = ROOT / "data" / "r1000_selected_group_after_burden_identity_surface_review_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_selected_group_after_burden_identity_surface_review_v0_receipts"

IDENTITY_SURFACE_PATH = OUT_DIR / "r1000_selected_group_after_burden_identity_surface.json"
IDENTITY_REVIEW_DECISION_PATH = OUT_DIR / "r1000_selected_group_after_burden_identity_review_decision.json"
IDENTITY_DEFECT_PACKET_PATH = OUT_DIR / "r1000_selected_group_after_burden_identity_defect_packet.json"
INSPECTION_BLOCK_PACKET_PATH = OUT_DIR / "r1000_selected_group_after_burden_inspection_block_packet.json"
REPAIR_RECOMMENDATION_PACKET_PATH = OUT_DIR / "r1000_selected_group_after_burden_identity_repair_recommendation_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_selected_group_after_burden_identity_review_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_selected_group_after_burden_identity_review_report.json"

SELECTION_AFTER_BURDEN_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_burden_pressure_reconciliation_v0_receipts" / f"{SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID}.json"
SELECTED_AFTER_BURDEN_GROUP_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_burden_pressure_reconciliation_v0" / "r1000_selected_pressure_group_after_burden_pressure_reconciliation.json"
SELECTION_AFTER_BURDEN_DECISION_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_burden_pressure_reconciliation_v0" / "r1000_pressure_group_selection_after_burden_decision.json"
SELECTION_AFTER_BURDEN_AUTHORITY_PACKET_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_burden_pressure_reconciliation_v0" / "r1000_selected_pressure_group_after_burden_authority_packet.json"
SELECTION_AFTER_BURDEN_REPORT_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_burden_pressure_reconciliation_v0" / "r1000_pressure_group_selection_after_burden_report.json"

BURDEN_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0_receipts" / f"{SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
BURDEN_NEXT_CANDIDATE_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0" / "r1000_next_selectable_group_candidate_after_selected_burden_pressure_inspection.json"
BURDEN_REMAINING_GROUPS_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0" / "r1000_remaining_pressure_groups_after_selected_burden_pressure_inspection.json"
BURDEN_QUEUE_RECONCILIATION_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection.json"

SELECTED_GROUP_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID}.json"
SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTION_RECEIPT_ID}.json"
QUEUE_RECONCILIATION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    SELECTION_AFTER_BURDEN_RECEIPT_PATH,
    SELECTED_AFTER_BURDEN_GROUP_PATH,
    SELECTION_AFTER_BURDEN_DECISION_PATH,
    SELECTION_AFTER_BURDEN_AUTHORITY_PACKET_PATH,
    SELECTION_AFTER_BURDEN_REPORT_PATH,
    BURDEN_QUEUE_RECEIPT_PATH,
    BURDEN_NEXT_CANDIDATE_PATH,
    BURDEN_REMAINING_GROUPS_PATH,
    BURDEN_QUEUE_RECONCILIATION_PATH,
    SELECTED_GROUP_INSPECTION_RECEIPT_PATH,
    SELECTION_RECEIPT_PATH,
    QUEUE_RECONCILIATION_RECEIPT_PATH,
]

RECOMMENDED_NEXT_HANDLING = "FIX_R1000_BURDEN_QUEUE_NEXT_CANDIDATE_IDENTITY_PRESERVATION_V0"

HUMAN_DECISION = {
    "decision": "REVIEW_SELECTED_R1000_PRESSURE_GROUP_AFTER_BURDEN_RECONCILIATION_IDENTITY_SURFACE",
    "scope": "review whether the selected pressure group after burden reconciliation has enough typed identity for lawful inspection; do not inspect rows, run R1000, repair the queue, or mutate prior artifacts in this unit",
    "source_selection_after_burden_receipt_id": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
    "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
    "authorized": [
        "consume selected pressure group after burden reconciliation",
        "consume burden queue next-candidate artifact",
        "materialize identity review surface",
        "classify identity completeness",
        "block inspection if identity is weak",
        "emit repair recommendation packet",
        "stop before inspection or repair",
    ],
    "not_authorized": [
        "inspecting selected group rows",
        "running R1000",
        "repairing queue identity",
        "rewriting remaining group artifacts",
        "assigning unknown identity fields",
        "inventing pressure class",
        "inventing pressure subtype",
        "inventing halt reason",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "emitting taxonomy delta proposal",
        "mutating source rows",
        "mutating existing receipts",
        "opening another group",
        "hiding next command",
    ],
}

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

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def tracked(path: Path) -> bool:
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel(path)],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def load_sources() -> Dict[str, Any]:
    return {
        "selection_after_burden_receipt": read_json(SELECTION_AFTER_BURDEN_RECEIPT_PATH),
        "selected_after_burden_group": read_json(SELECTED_AFTER_BURDEN_GROUP_PATH),
        "selection_after_burden_decision": read_json(SELECTION_AFTER_BURDEN_DECISION_PATH),
        "selection_after_burden_authority_packet": read_json(SELECTION_AFTER_BURDEN_AUTHORITY_PACKET_PATH),
        "selection_after_burden_report": read_json(SELECTION_AFTER_BURDEN_REPORT_PATH),
        "burden_queue_receipt": read_json(BURDEN_QUEUE_RECEIPT_PATH),
        "burden_next_candidate": read_json(BURDEN_NEXT_CANDIDATE_PATH),
        "burden_remaining_groups": read_json(BURDEN_REMAINING_GROUPS_PATH),
        "burden_queue_reconciliation": read_json(BURDEN_QUEUE_RECONCILIATION_PATH),
        "selected_group_inspection_receipt": read_json(SELECTED_GROUP_INSPECTION_RECEIPT_PATH),
        "selection_receipt": read_json(SELECTION_RECEIPT_PATH),
        "queue_reconciliation_receipt": read_json(QUEUE_RECONCILIATION_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    receipt = sources["selection_after_burden_receipt"]
    selected = sources["selected_after_burden_group"]
    decision = sources["selection_after_burden_decision"]
    authority = sources["selection_after_burden_authority_packet"]
    burden_candidate = sources["burden_next_candidate"]

    if receipt.get("receipt_id") != SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID:
        failures.append("selection_after_burden_receipt_id_wrong")
    if receipt.get("gate") != "PASS":
        failures.append("selection_after_burden_not_pass")
    if receipt.get("selected_pressure_group_id") != SELECTED_PRESSURE_GROUP_ID:
        failures.append("selected_pressure_group_id_wrong_in_receipt")
    if receipt.get("aggregate_metrics", {}).get("pressure_group_selected_count") != 1:
        failures.append("pressure_group_not_selected")
    if receipt.get("aggregate_metrics", {}).get("selected_group_inspected_count") != 0:
        failures.append("selected_group_already_inspected")
    if receipt.get("aggregate_metrics", {}).get("r1000_run_executed_count") != 0:
        failures.append("r1000_already_run")

    if selected.get("selected_pressure_group_id") != SELECTED_PRESSURE_GROUP_ID:
        failures.append("selected_group_id_wrong")
    if selected.get("selection_status") != "SELECTED_NOT_INSPECTED":
        failures.append("selected_group_status_wrong")
    if selected.get("selected_group_rows_inspected") is not False:
        failures.append("selected_group_rows_already_inspected")
    if selected.get("r1000_run_executed") is not False:
        failures.append("selected_group_r1000_already_run")

    if decision.get("inspection_authorized_in_this_unit") is not False:
        failures.append("selection_decision_authorized_inspection")
    if authority.get("authority_status") != "SEPARATE_INSPECTION_REQUIRED":
        failures.append("selection_authority_status_wrong")
    if burden_candidate.get("selection_status") != "CANDIDATE_ONLY_NOT_OPENED":
        failures.append("burden_candidate_status_wrong")
    if burden_candidate.get("next_group_opened") is not False:
        failures.append("burden_candidate_already_opened")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def selected_group_summary(sources: Dict[str, Any]) -> Dict[str, Any]:
    group = sources["selected_after_burden_group"].get("selected_group", {})
    return {
        "parent_pressure_class": group.get("parent_pressure_class"),
        "pressure_subtype": group.get("pressure_subtype"),
        "halt_reason": group.get("halt_reason"),
        "row_count": int(group.get("row_count", 0) or 0),
    }

def value_is_unknown(value: Any) -> bool:
    return value is None or value == "" or value == "UNKNOWN"

def identity_defects(group: Dict[str, Any]) -> List[Dict[str, Any]]:
    defects: List[Dict[str, Any]] = []
    for field in ["parent_pressure_class", "pressure_subtype", "halt_reason"]:
        if value_is_unknown(group.get(field)):
            defects.append({
                "field": field,
                "observed_value": group.get(field),
                "defect_type": "UNKNOWN_IDENTITY_FIELD",
                "severity": "BLOCKS_INSPECTION",
            })
    return defects

def build_identity_surface(sources: Dict[str, Any]) -> Dict[str, Any]:
    group = selected_group_summary(sources)
    defects = identity_defects(group)
    return {
        "schema_version": "r1000_selected_group_after_burden_identity_surface_v0",
        "identity_surface_id": sha8({
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "group": group,
            "review": "after_burden_identity_surface",
        }),
        "source_selection_after_burden_receipt_id": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "surface_status": "IDENTITY_SURFACE_MATERIALIZED_FOR_REVIEW",
        "selected_group": group,
        "identity_fields_required_for_inspection": [
            "parent_pressure_class",
            "pressure_subtype",
            "halt_reason",
        ],
        "identity_defects": defects,
        "identity_defect_count": len(defects),
        "identity_complete": len(defects) == 0,
        "row_count_present": isinstance(group.get("row_count"), int),
        "row_payload_inspected": False,
        "r1000_run_executed": False,
    }

def build_decision(surface: Dict[str, Any]) -> Dict[str, Any]:
    identity_complete = surface["identity_complete"]
    decision_status = "ACCEPT_IDENTITY_FOR_SEPARATE_INSPECTION" if identity_complete else "BLOCK_INSPECTION_REQUIRES_IDENTITY_PRESERVATION_FIX"
    recommended = "INSPECT_SELECTED_R1000_PRESSURE_GROUP_AFTER_BURDEN_PRESSURE_RECONCILIATION_V0" if identity_complete else RECOMMENDED_NEXT_HANDLING

    return {
        "schema_version": "r1000_selected_group_after_burden_identity_review_decision_v0",
        "identity_review_decision_id": sha8({
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "identity_complete": identity_complete,
            "defect_count": surface["identity_defect_count"],
        }),
        "source_identity_surface_ref": rel(IDENTITY_SURFACE_PATH),
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "decision_status": decision_status,
        "identity_complete": identity_complete,
        "inspection_blocked": not identity_complete,
        "inspection_authorized_after_review": identity_complete,
        "repair_required": not identity_complete,
        "repair_authorized_in_this_unit": False,
        "selected_group": surface["selected_group"],
        "identity_defects": surface["identity_defects"],
        "recommended_next_handling": recommended,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_SELECTED_GROUP_IDENTITY_SURFACE_REVIEW_COMPLETE_REPAIR_REQUIRED" if not identity_complete else "STOP_SELECTED_GROUP_IDENTITY_SURFACE_REVIEW_COMPLETE_INSPECTION_ALLOWED",
            "next_command_goal": None,
        },
    }

def build_identity_defect_packet(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_group_after_burden_identity_defect_packet_v0",
        "packet_status": "IDENTITY_DEFECT_PACKET",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "defect_count": surface["identity_defect_count"],
        "defects": surface["identity_defects"],
        "selected_group": surface["selected_group"],
        "defect_interpretation": "selected group has row count but lacks typed pressure identity fields required for lawful inspection",
        "inspection_blocked": decision["inspection_blocked"],
        "value_repair_authorized": False,
        "identity_assignment_authorized": False,
        "source_mutation_authorized": False,
    }

def build_inspection_block_packet(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_group_after_burden_inspection_block_packet_v0",
        "packet_status": "INSPECTION_BLOCKED_BY_IDENTITY_SURFACE",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "blocked_unit": "INSPECT_SELECTED_R1000_PRESSURE_GROUP_AFTER_BURDEN_PRESSURE_RECONCILIATION_V0",
        "block_reason": "selected group identity fields are UNKNOWN",
        "blocked_fields": [d["field"] for d in surface["identity_defects"]],
        "inspection_authorized": False,
        "repair_authorized_in_this_unit": False,
        "queue_reconciliation_authorized_in_this_unit": False,
        "next_group_opened": False,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def build_repair_recommendation_packet(surface: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_group_after_burden_identity_repair_recommendation_packet_v0",
        "packet_status": "CANDIDATE_ONLY_NOT_EXECUTED",
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
        "repair_target": "next selectable group candidate emitted by selected burden pressure queue reconciliation",
        "source_candidate_ref": rel(BURDEN_NEXT_CANDIDATE_PATH),
        "source_remaining_groups_ref": rel(BURDEN_REMAINING_GROUPS_PATH),
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "required_repair_goal": "preserve or recover typed candidate identity before inspection",
        "required_identity_fields": [
            "parent_pressure_class",
            "pressure_subtype",
            "halt_reason",
            "row_count",
        ],
        "known_current_surface": surface["selected_group"],
        "repair_must_not": [
            "invent pressure class",
            "invent pressure subtype",
            "invent halt reason",
            "mutate source receipts",
            "run R1000",
            "inspect row payloads",
            "open next group",
        ],
    }

def build_transition_trace(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_group_after_burden_identity_review_transition_trace_v0",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "trace": [
            {
                "step": "consume_selected_group_after_burden",
                "question": "selected group exists and is not inspected",
                "answer": True,
                "taken": "materialize_identity_surface",
            },
            {
                "step": "materialize_identity_surface",
                "question": "identity fields complete for inspection",
                "answer": surface["identity_complete"],
                "taken": "block_inspection_and_emit_repair_packet" if not surface["identity_complete"] else "allow_separate_inspection",
            },
            {
                "step": "block_inspection_and_emit_repair_packet",
                "question": "repair identity in this unit",
                "answer": False,
                "taken": decision["terminal"]["stop_code"],
            },
            {
                "step": "terminal",
                "question": "hidden next command allowed",
                "answer": False,
                "taken": "stop_with_null_next_command_goal",
            },
        ],
        "terminal": decision["terminal"],
    }

def build_report(surface: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    group = surface["selected_group"]
    return {
        "schema_version": "r1000_selected_group_after_burden_identity_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_selection_after_burden_receipt_id": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": group.get("parent_pressure_class"),
        "selected_pressure_subtype": group.get("pressure_subtype"),
        "selected_halt_reason": group.get("halt_reason"),
        "selected_row_count": group.get("row_count"),
        "selection_after_burden_consumed_count": 1,
        "identity_surface_materialized_count": 1,
        "identity_review_completed_count": 1,
        "identity_complete_count": 1 if surface["identity_complete"] else 0,
        "identity_defect_count": surface["identity_defect_count"],
        "unknown_identity_field_count": surface["identity_defect_count"],
        "inspection_blocked_count": 1 if decision["inspection_blocked"] else 0,
        "inspection_authorized_after_review_count": 1 if decision["inspection_authorized_after_review"] else 0,
        "identity_defect_packet_emitted_count": 1,
        "inspection_block_packet_emitted_count": 1,
        "repair_recommendation_packet_emitted_count": 1,
        "repair_executed_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "selected_group_inspected_count": 0,
        "selected_group_rows_materialized_count": 0,
        "selected_group_rows_inspected_count": 0,
        "queue_reconciled_count": 0,
        "next_group_auto_opened_count": 0,
        "other_group_opened_count": 0,
        "r1000_run_executed_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "descriptor_value_assignment_count": 0,
        "null_field_value_emitted_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": decision["recommended_next_handling"],
    }

def validate_outputs(
    surface: Dict[str, Any],
    decision: Dict[str, Any],
    defect_packet: Dict[str, Any],
    block_packet: Dict[str, Any],
    repair_packet: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if surface.get("surface_status") != "IDENTITY_SURFACE_MATERIALIZED_FOR_REVIEW":
        failures.append("identity_surface_status_wrong")
    if surface.get("identity_complete") is not False:
        failures.append("identity_unexpectedly_complete")
    if surface.get("identity_defect_count") < 1:
        failures.append("identity_defect_count_missing")
    if decision.get("decision_status") != "BLOCK_INSPECTION_REQUIRES_IDENTITY_PRESERVATION_FIX":
        failures.append("decision_status_wrong")
    if decision.get("inspection_blocked") is not True:
        failures.append("inspection_not_blocked")
    if decision.get("inspection_authorized_after_review") is not False:
        failures.append("inspection_authorized_despite_identity_defect")
    if decision.get("repair_authorized_in_this_unit") is not False:
        failures.append("repair_authorized_in_review_unit")
    if defect_packet.get("identity_assignment_authorized") is not False:
        failures.append("identity_assignment_authorized")
    if block_packet.get("inspection_authorized") is not False:
        failures.append("block_packet_authorized_inspection")
    if repair_packet.get("packet_status") != "CANDIDATE_ONLY_NOT_EXECUTED":
        failures.append("repair_packet_not_candidate_only")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "repair_executed_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "selected_group_inspected_count",
        "selected_group_rows_materialized_count",
        "selected_group_rows_inspected_count",
        "queue_reconciled_count",
        "next_group_auto_opened_count",
        "other_group_opened_count",
        "r1000_run_executed_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "descriptor_value_assignment_count",
        "null_field_value_emitted_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    if report.get("identity_review_completed_count") != 1:
        failures.append("identity_review_completed_count_wrong")
    if report.get("inspection_blocked_count") != 1:
        failures.append("inspection_blocked_count_wrong")
    if report.get("repair_recommendation_packet_emitted_count") != 1:
        failures.append("repair_recommendation_count_wrong")

    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")

    for gate, ok in receipt.get("acceptance_gate_results", {}).items():
        if ok is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{ok}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("identity_review_completed_count") != 1:
        failures.append("metric_identity_review_completed_wrong")
    if metrics.get("identity_defect_count", 0) < 1:
        failures.append("metric_identity_defect_count_missing")
    if metrics.get("inspection_blocked_count") != 1:
        failures.append("metric_inspection_blocked_wrong")

    for key in [
        "repair_executed_count",
        "identity_assignment_count",
        "field_value_invention_count",
        "selected_group_inspected_count",
        "selected_group_rows_materialized_count",
        "selected_group_rows_inspected_count",
        "queue_reconciled_count",
        "next_group_auto_opened_count",
        "other_group_opened_count",
        "r1000_run_executed_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "descriptor_value_assignment_count",
        "null_field_value_emitted_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_SELECTED_GROUP_IDENTITY_SURFACE_REVIEW_COMPLETE_REPAIR_REQUIRED":
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

    surface = build_identity_surface(sources)
    decision = build_decision(surface)
    defect_packet = build_identity_defect_packet(surface, decision)
    block_packet = build_inspection_block_packet(surface, decision)
    repair_packet = build_repair_recommendation_packet(surface)
    trace = build_transition_trace(surface, decision)
    report = build_report(surface, decision)

    write_json(IDENTITY_SURFACE_PATH, surface)
    write_json(IDENTITY_REVIEW_DECISION_PATH, decision)
    write_json(IDENTITY_DEFECT_PACKET_PATH, defect_packet)
    write_json(INSPECTION_BLOCK_PACKET_PATH, block_packet)
    write_json(REPAIR_RECOMMENDATION_PACKET_PATH, repair_packet)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(
        surface,
        decision,
        defect_packet,
        block_packet,
        repair_packet,
        trace,
        report,
    ))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "IDENTITY_REVIEW_0_SELECTION_AFTER_BURDEN_CONSUMED": sources["selection_after_burden_receipt"]["receipt_id"] == SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID and sources["selection_after_burden_receipt"]["gate"] == "PASS",
        "IDENTITY_REVIEW_1_IDENTITY_SURFACE_MATERIALIZED": surface["surface_status"] == "IDENTITY_SURFACE_MATERIALIZED_FOR_REVIEW",
        "IDENTITY_REVIEW_2_UNKNOWN_IDENTITY_DETECTED": surface["identity_defect_count"] >= 1 and surface["identity_complete"] is False,
        "IDENTITY_REVIEW_3_INSPECTION_BLOCKED": decision["inspection_blocked"] is True and decision["inspection_authorized_after_review"] is False,
        "IDENTITY_REVIEW_4_REPAIR_RECOMMENDATION_EMITTED_ONLY": repair_packet["packet_status"] == "CANDIDATE_ONLY_NOT_EXECUTED" and decision["repair_authorized_in_this_unit"] is False,
        "IDENTITY_REVIEW_5_NO_IDENTITY_ASSIGNMENT_OR_INVENTION": report["identity_assignment_count"] == 0 and report["field_value_invention_count"] == 0,
        "IDENTITY_REVIEW_6_NO_GROUP_INSPECTION_OR_QUEUE_RECONCILIATION": report["selected_group_inspected_count"] == 0 and report["queue_reconciled_count"] == 0,
        "IDENTITY_REVIEW_7_NO_R1000_RUN_OR_REPAIR": report["r1000_run_executed_count"] == 0 and report["repair_executed_count"] == 0,
        "IDENTITY_REVIEW_8_NO_FIELD_VALUE_OR_TAXONOMY_ACTION": report["target_field_filled_count"] == 0 and report["descriptor_value_assignment_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "IDENTITY_REVIEW_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "IDENTITY_REVIEW_10_NO_NEXT_GROUP_OR_HIDDEN_COMMAND": report["next_group_auto_opened_count"] == 0 and report["other_group_opened_count"] == 0 and report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_SELECTED_GROUP_IDENTITY_SURFACE_REVIEW_COMPLETE_REPAIR_REQUIRED",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        }

    aggregate_metrics = {
        "source_selection_after_burden_receipt_id": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": surface["selected_group"].get("parent_pressure_class"),
        "selected_pressure_subtype": surface["selected_group"].get("pressure_subtype"),
        "selected_halt_reason": surface["selected_group"].get("halt_reason"),
        "selected_row_count": surface["selected_group"].get("row_count"),
        "selection_after_burden_consumed_count": 1,
        "identity_surface_materialized_count": 1,
        "identity_review_completed_count": 1,
        "identity_complete_count": 1 if surface["identity_complete"] else 0,
        "identity_defect_count": surface["identity_defect_count"],
        "unknown_identity_field_count": surface["identity_defect_count"],
        "inspection_blocked_count": 1,
        "inspection_authorized_after_review_count": 0,
        "identity_defect_packet_emitted_count": 1,
        "inspection_block_packet_emitted_count": 1,
        "repair_recommendation_packet_emitted_count": 1,
        "repair_executed_count": 0,
        "identity_assignment_count": 0,
        "field_value_invention_count": 0,
        "selected_group_inspected_count": 0,
        "selected_group_rows_materialized_count": 0,
        "selected_group_rows_inspected_count": 0,
        "queue_reconciled_count": 0,
        "next_group_auto_opened_count": 0,
        "other_group_opened_count": 0,
        "r1000_run_executed_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "descriptor_value_assignment_count": 0,
        "null_field_value_emitted_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
    }

    guards = {
        "selection_after_burden_consumed": True,
        "identity_surface_materialized": True,
        "unknown_identity_detected": True,
        "inspection_blocked": True,
        "repair_recommendation_emitted": True,
        "repair_executed": False,
        "identity_assignment": False,
        "field_value_invention": False,
        "selected_group_inspected": False,
        "selected_group_rows_materialized": False,
        "selected_group_rows_inspected": False,
        "queue_reconciled": False,
        "next_group_opened": False,
        "r1000_run_executed": False,
        "proposal_applied": False,
        "target_field_filled": False,
        "descriptor_value_assigned": False,
        "null_field_value_emitted": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_selection_after_burden_receipt": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "identity_complete": surface["identity_complete"],
        "identity_defect_count": surface["identity_defect_count"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "identity_surface": rel(IDENTITY_SURFACE_PATH),
        "identity_review_decision": rel(IDENTITY_REVIEW_DECISION_PATH),
        "identity_defect_packet": rel(IDENTITY_DEFECT_PACKET_PATH),
        "inspection_block_packet": rel(INSPECTION_BLOCK_PACKET_PATH),
        "repair_recommendation_packet": rel(REPAIR_RECOMMENDATION_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_selected_group_after_burden_identity_surface_review_receipt_v0",
        "receipt_type": "R1000_SELECTED_GROUP_AFTER_BURDEN_IDENTITY_SURFACE_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_selection_after_burden_receipt_id": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "identity_surface_review_summary": {
            "review_result": "BLOCK_INSPECTION_REQUIRES_IDENTITY_PRESERVATION_FIX",
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "selected_group": surface["selected_group"],
            "identity_complete": surface["identity_complete"],
            "identity_defect_count": surface["identity_defect_count"],
            "inspection_blocked": True,
            "repair_executed": False,
            "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "identity_surface_review_guards": guards,
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
    print(f"identity_surface_review_receipt_id={receipt_id}")
    print(f"identity_surface_review_receipt_path=data/r1000_selected_group_after_burden_identity_surface_review_v0_receipts/{receipt_id}.json")
    print(f"identity_review_decision_path=data/r1000_selected_group_after_burden_identity_surface_review_v0/r1000_selected_group_after_burden_identity_review_decision.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
