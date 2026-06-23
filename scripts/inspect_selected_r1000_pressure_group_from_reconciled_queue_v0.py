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

UNIT_ID = "INSPECT_SELECTED_R1000_PRESSURE_GROUP_FROM_RECONCILED_QUEUE_V0"
TARGET_UNIT_ID = "r1000_selected_pressure_group.inspection.from_reconciled_queue.v0"

SOURCE_SELECTION_RECEIPT_ID = "7c561212"
SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID = "38604be8"
SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID = "91f8eea5"
SOURCE_ACCEPTED_APP_RECEIPT_ID = "8d33789d"
SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID = "087bf971"
SELECTED_PRESSURE_GROUP_ID = "b9a7575a"

OUT_DIR = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0_receipts"

INSPECTION_SURFACE_PATH = OUT_DIR / "r1000_selected_pressure_group_inspection_surface.json"
INSPECTION_CLASSIFICATION_PATH = OUT_DIR / "r1000_selected_pressure_group_inspection_classification.json"
BURDEN_PRESSURE_PACKET_PATH = OUT_DIR / "r1000_selected_group_burden_pressure_packet.json"
INSPECTION_LIMIT_PACKET_PATH = OUT_DIR / "r1000_selected_group_inspection_limit_packet.json"
QUEUE_RETURN_PACKET_PATH = OUT_DIR / "r1000_selected_group_inspection_queue_return_packet.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_selected_group_inspection_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_selected_group_inspection_report.json"

SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTION_RECEIPT_ID}.json"
SELECTED_GROUP_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0" / "r1000_selected_pressure_group_from_reconciled_queue.json"
SELECTION_DECISION_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0" / "r1000_pressure_group_selection_decision.json"
SELECTION_AUTHORITY_PACKET_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0" / "r1000_selected_pressure_group_authority_packet.json"
SELECTION_REPORT_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0" / "r1000_pressure_group_selection_report.json"

QUEUE_RECONCILIATION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
NEXT_CANDIDATE_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0" / "r1000_next_selectable_group_candidate_after_accepted_descriptor_review.json"
REMAINING_GROUPS_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0" / "r1000_remaining_pressure_groups_after_accepted_descriptor_review.json"
QUEUE_RECONCILIATION_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review.json"

DERIVED_SURFACE_REVIEW_RECEIPT_PATH = ROOT / "data" / "derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0_receipts" / f"{SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID}.json"
ACCEPTED_APP_RECEIPT_PATH = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_ACCEPTED_APP_RECEIPT_ID}.json"
PRIOR_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0_receipts" / f"{SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    SELECTION_RECEIPT_PATH,
    SELECTED_GROUP_PATH,
    SELECTION_DECISION_PATH,
    SELECTION_AUTHORITY_PACKET_PATH,
    SELECTION_REPORT_PATH,
    QUEUE_RECONCILIATION_RECEIPT_PATH,
    NEXT_CANDIDATE_PATH,
    REMAINING_GROUPS_PATH,
    QUEUE_RECONCILIATION_PATH,
    DERIVED_SURFACE_REVIEW_RECEIPT_PATH,
    ACCEPTED_APP_RECEIPT_PATH,
    PRIOR_QUEUE_RECEIPT_PATH,
]

HUMAN_DECISION = {
    "decision": "INSPECT_SELECTED_R1000_PRESSURE_GROUP_FROM_RECONCILED_QUEUE",
    "scope": "inspect the already selected R1000 pressure group at metadata/surface level only and classify the receipt-size burden pressure without running R1000, repairing, mutating sources, or opening another group",
    "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
    "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
    "authorized": [
        "consume selected pressure group object",
        "consume selection authority packet",
        "materialize selected group inspection surface from selected object",
        "classify selected group pressure behavior",
        "emit burden-pressure packet",
        "emit queue return packet candidate only",
        "stop without opening another group",
    ],
    "not_authorized": [
        "running R1000",
        "repairing surfaces",
        "assigning descriptor values",
        "filling fields",
        "inventing values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "emitting taxonomy delta proposal",
        "mutating source rows",
        "mutating existing receipts",
        "opening another pressure group",
        "auto-reconciling queue after inspection",
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
        "selection_receipt": read_json(SELECTION_RECEIPT_PATH),
        "selected_group": read_json(SELECTED_GROUP_PATH),
        "selection_decision": read_json(SELECTION_DECISION_PATH),
        "selection_authority_packet": read_json(SELECTION_AUTHORITY_PACKET_PATH),
        "selection_report": read_json(SELECTION_REPORT_PATH),
        "queue_reconciliation_receipt": read_json(QUEUE_RECONCILIATION_RECEIPT_PATH),
        "next_candidate": read_json(NEXT_CANDIDATE_PATH),
        "remaining_groups": read_json(REMAINING_GROUPS_PATH),
        "queue_reconciliation": read_json(QUEUE_RECONCILIATION_PATH),
        "derived_surface_review_receipt": read_json(DERIVED_SURFACE_REVIEW_RECEIPT_PATH),
        "accepted_application_receipt": read_json(ACCEPTED_APP_RECEIPT_PATH),
        "prior_queue_receipt": read_json(PRIOR_QUEUE_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    receipt = sources["selection_receipt"]
    selected = sources["selected_group"]
    decision = sources["selection_decision"]
    authority = sources["selection_authority_packet"]

    if receipt.get("receipt_id") != SOURCE_SELECTION_RECEIPT_ID:
        failures.append("selection_receipt_id_wrong")
    if receipt.get("gate") != "PASS":
        failures.append("selection_not_pass")
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

    group = selected.get("selected_group", {})
    if group.get("parent_pressure_class") != "BURDEN_PRESSURE":
        failures.append("selected_parent_pressure_class_unexpected")
    if group.get("pressure_subtype") != "receipt_size_burden":
        failures.append("selected_pressure_subtype_unexpected")
    if group.get("halt_reason") != "STOP_DONE":
        failures.append("selected_halt_reason_unexpected")

    if decision.get("inspection_authorized_in_this_unit") is not False:
        failures.append("selection_decision_authorized_inspection_in_selection_unit")
    if authority.get("authority_status") != "SEPARATE_INSPECTION_REQUIRED":
        failures.append("selection_authority_packet_status_wrong")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_inspection_surface(selected: Dict[str, Any]) -> Dict[str, Any]:
    group = selected["selected_group"]
    return {
        "schema_version": "r1000_selected_pressure_group_inspection_surface_v0",
        "inspection_surface_id": sha8({
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "surface": "selected_group_inspection_surface",
        }),
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "surface_status": "SELECTED_GROUP_METADATA_SURFACE_MATERIALIZED",
        "materialized_from": rel(SELECTED_GROUP_PATH),
        "selected_group": group,
        "row_count": group.get("row_count"),
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "available_evidence": [
            "selected pressure group class",
            "selected pressure subtype",
            "selected halt reason",
            "selected row count",
            "selection authority packet",
            "queue reconciliation provenance",
        ],
        "unavailable_evidence": [
            "individual selected-group row payloads",
            "per-row receipt-size measurements",
            "post-selection R1000 behavior",
        ],
    }

def build_classification(surface: Dict[str, Any]) -> Dict[str, Any]:
    group = surface["selected_group"]
    is_receipt_burden = (
        group.get("parent_pressure_class") == "BURDEN_PRESSURE"
        and group.get("pressure_subtype") == "receipt_size_burden"
        and group.get("halt_reason") == "STOP_DONE"
    )
    status = "BURDEN_PRESSURE_RECEIPT_SIZE_BURDEN_METADATA_REVIEWED" if is_receipt_burden else "SELECTED_GROUP_REQUIRES_ADDITIONAL_CLASSIFICATION"

    return {
        "schema_version": "r1000_selected_pressure_group_inspection_classification_v0",
        "classification_id": sha8({
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "classification": status,
        }),
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "classification_status": status,
        "pressure_class": group.get("parent_pressure_class"),
        "pressure_subtype": group.get("pressure_subtype"),
        "halt_reason": group.get("halt_reason"),
        "row_count": group.get("row_count"),
        "inspection_basis": "selected group metadata and queue-selection provenance only",
        "semantic_interpretation": {
            "is_burden_pressure": is_receipt_burden,
            "is_value_gap": False,
            "is_taxonomy_gap": False,
            "is_source_absence_claim": False,
            "is_runtime_failure": False,
            "requires_value_repair": False,
            "requires_taxonomy_repair": False,
            "requires_r1000_run": False,
        },
        "classification_limit": {
            "does_not_measure_individual_receipt_sizes": True,
            "does_not_rewrite_burden_policy": True,
            "does_not_close_all_burden_pressure": True,
            "does_not_open_next_group": True,
        },
    }

def build_burden_pressure_packet(classification: Dict[str, Any], surface: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_group_burden_pressure_packet_v0",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "packet_status": "BURDEN_PRESSURE_METADATA_INSPECTION_PACKET",
        "classification_status": classification["classification_status"],
        "row_count": classification["row_count"],
        "burden_pressure_type": "receipt_size_burden",
        "observed_halt_reason": classification["halt_reason"],
        "inspection_basis": classification["inspection_basis"],
        "local_interpretation": "selected group represents receipt-size burden pressure from completed rows; this inspection records it as metadata-reviewed and returns it for separate queue reconciliation or burden-policy handling",
        "suggested_handling_options": [
            "mark selected burden group as metadata-reviewed and reconcile queue",
            "introduce separate receipt-burden policy/metrics layer if burden pressure needs quantitative treatment",
            "defer deeper burden analysis until individual row payloads are explicitly authorized",
        ],
        "not_authorized_here": [
            "policy rewrite",
            "receipt-size metric redesign",
            "individual row inspection",
            "R1000 rerun",
            "source mutation",
            "queue reconciliation",
            "next group opening",
        ],
    }

def build_limit_packet(classification: Dict[str, Any], surface: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_group_inspection_limit_packet_v0",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "limit_status": "METADATA_LEVEL_INSPECTION_LIMIT",
        "reason": "selected group object exposes group class/subtype/halt/row-count but not individual row payloads or receipt-size measurements",
        "current_unit_can_conclude": [
            "selected group is receipt-size burden pressure",
            "selected group was not inspected before this unit",
            "no value/taxonomy/source/runtime action is required by this metadata inspection",
        ],
        "current_unit_cannot_conclude": [
            "exact per-row receipt-size burden distribution",
            "whether burden policy should be changed",
            "whether receipt-size burden is acceptable globally",
            "whether future rows will remain within burden bounds",
        ],
    }

def build_queue_return_packet(classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_group_inspection_queue_return_packet_v0",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "packet_status": "CANDIDATE_ONLY_NOT_EXECUTED",
        "inspection_completed": True,
        "classification_status": classification["classification_status"],
        "queue_reconciliation_authorized_in_this_unit": False,
        "next_group_auto_opened": False,
        "recommended_next_handling": "RECONCILE_R1000_PRESSURE_QUEUE_AFTER_SELECTED_BURDEN_PRESSURE_GROUP_INSPECTION_V0",
    }

def build_transition_trace(classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_group_inspection_transition_trace_v0",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "trace": [
            {
                "step": "consume_selected_group",
                "question": "selected group exists and was not inspected",
                "answer": True,
                "taken": "materialize_metadata_surface",
            },
            {
                "step": "materialize_metadata_surface",
                "question": "row payload inspection authorized",
                "answer": False,
                "taken": "classify_metadata_surface",
            },
            {
                "step": "classify_metadata_surface",
                "question": "selected group is receipt-size burden pressure",
                "answer": classification["classification_status"] == "BURDEN_PRESSURE_RECEIPT_SIZE_BURDEN_METADATA_REVIEWED",
                "taken": "emit_burden_pressure_packet",
            },
            {
                "step": "emit_burden_pressure_packet",
                "question": "queue reconciliation happens in this unit",
                "answer": False,
                "taken": "STOP_SELECTED_R1000_PRESSURE_GROUP_INSPECTED_QUEUE_RECONCILIATION_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_SELECTED_R1000_PRESSURE_GROUP_INSPECTED_QUEUE_RECONCILIATION_REQUIRED",
            "next_command_goal": None,
        },
    }

def build_report(surface: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_group_inspection_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": classification["pressure_class"],
        "selected_pressure_subtype": classification["pressure_subtype"],
        "selected_halt_reason": classification["halt_reason"],
        "selected_row_count": classification["row_count"],
        "selected_group_consumed_count": 1,
        "inspection_surface_materialized_count": 1,
        "selected_group_inspected_count": 1,
        "classification_emitted_count": 1,
        "burden_pressure_packet_emitted_count": 1,
        "inspection_limit_packet_emitted_count": 1,
        "queue_return_packet_emitted_count": 1,
        "metadata_only_inspection_count": 1,
        "row_payload_materialized_count": 0,
        "row_payload_inspected_count": 0,
        "queue_reconciled_count": 0,
        "next_group_auto_opened_count": 0,
        "other_group_opened_count": 0,
        "r1000_run_executed_count": 0,
        "repair_executed_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "descriptor_value_assignment_count": 0,
        "null_field_value_emitted_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": "RECONCILE_R1000_PRESSURE_QUEUE_AFTER_SELECTED_BURDEN_PRESSURE_GROUP_INSPECTION_V0",
    }

def validate_outputs(
    surface: Dict[str, Any],
    classification: Dict[str, Any],
    burden_packet: Dict[str, Any],
    limit_packet: Dict[str, Any],
    queue_packet: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if surface.get("surface_status") != "SELECTED_GROUP_METADATA_SURFACE_MATERIALIZED":
        failures.append("surface_status_wrong")
    if surface.get("row_payload_materialized") is not False:
        failures.append("row_payload_materialized")
    if surface.get("row_payload_inspected") is not False:
        failures.append("row_payload_inspected")
    if classification.get("classification_status") != "BURDEN_PRESSURE_RECEIPT_SIZE_BURDEN_METADATA_REVIEWED":
        failures.append("classification_status_wrong")
    if classification.get("semantic_interpretation", {}).get("requires_r1000_run") is not False:
        failures.append("classification_requires_r1000")
    if classification.get("semantic_interpretation", {}).get("requires_taxonomy_repair") is not False:
        failures.append("classification_requires_taxonomy_repair")
    if burden_packet.get("packet_status") != "BURDEN_PRESSURE_METADATA_INSPECTION_PACKET":
        failures.append("burden_packet_status_wrong")
    if limit_packet.get("limit_status") != "METADATA_LEVEL_INSPECTION_LIMIT":
        failures.append("limit_packet_status_wrong")
    if queue_packet.get("packet_status") != "CANDIDATE_ONLY_NOT_EXECUTED":
        failures.append("queue_packet_not_candidate_only")
    if queue_packet.get("queue_reconciliation_authorized_in_this_unit") is not False:
        failures.append("queue_packet_authorized_reconciliation")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "queue_reconciled_count",
        "next_group_auto_opened_count",
        "other_group_opened_count",
        "r1000_run_executed_count",
        "repair_executed_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "descriptor_value_assignment_count",
        "null_field_value_emitted_count",
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")

    if report.get("selected_group_inspected_count") != 1:
        failures.append("selected_group_inspected_count_wrong")
    if report.get("classification_emitted_count") != 1:
        failures.append("classification_count_wrong")
    if report.get("metadata_only_inspection_count") != 1:
        failures.append("metadata_only_inspection_count_wrong")

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
    if metrics.get("selected_group_inspected_count") != 1:
        failures.append("metric_selected_group_inspected_wrong")
    if metrics.get("classification_emitted_count") != 1:
        failures.append("metric_classification_wrong")
    if metrics.get("queue_reconciled_count") != 0:
        failures.append("metric_queue_reconciled")

    for key in [
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "queue_reconciled_count",
        "next_group_auto_opened_count",
        "other_group_opened_count",
        "r1000_run_executed_count",
        "repair_executed_count",
        "proposal_applied_count",
        "target_field_filled_count",
        "descriptor_value_assignment_count",
        "null_field_value_emitted_count",
        "field_value_invention_count",
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
    if terminal.get("stop_code") != "STOP_SELECTED_R1000_PRESSURE_GROUP_INSPECTED_QUEUE_RECONCILIATION_REQUIRED":
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

    selected = sources["selected_group"]
    surface = build_inspection_surface(selected)
    classification = build_classification(surface)
    burden_packet = build_burden_pressure_packet(classification, surface)
    limit_packet = build_limit_packet(classification, surface)
    queue_packet = build_queue_return_packet(classification)
    trace = build_transition_trace(classification)
    report = build_report(surface, classification)

    write_json(INSPECTION_SURFACE_PATH, surface)
    write_json(INSPECTION_CLASSIFICATION_PATH, classification)
    write_json(BURDEN_PRESSURE_PACKET_PATH, burden_packet)
    write_json(INSPECTION_LIMIT_PACKET_PATH, limit_packet)
    write_json(QUEUE_RETURN_PACKET_PATH, queue_packet)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(
        surface,
        classification,
        burden_packet,
        limit_packet,
        queue_packet,
        trace,
        report,
    ))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "INSPECT_SELECTED_GROUP_0_SELECTION_CONSUMED": sources["selection_receipt"]["receipt_id"] == SOURCE_SELECTION_RECEIPT_ID and sources["selection_receipt"]["gate"] == "PASS",
        "INSPECT_SELECTED_GROUP_1_SELECTED_GROUP_CONSUMED": selected.get("selected_pressure_group_id") == SELECTED_PRESSURE_GROUP_ID,
        "INSPECT_SELECTED_GROUP_2_METADATA_SURFACE_MATERIALIZED": surface["surface_status"] == "SELECTED_GROUP_METADATA_SURFACE_MATERIALIZED",
        "INSPECT_SELECTED_GROUP_3_BURDEN_PRESSURE_CLASSIFIED": classification["classification_status"] == "BURDEN_PRESSURE_RECEIPT_SIZE_BURDEN_METADATA_REVIEWED",
        "INSPECT_SELECTED_GROUP_4_ROW_PAYLOAD_NOT_MATERIALIZED": report["row_payload_materialized_count"] == 0 and report["row_payload_inspected_count"] == 0,
        "INSPECT_SELECTED_GROUP_5_QUEUE_RETURN_PACKET_CANDIDATE_ONLY": queue_packet["packet_status"] == "CANDIDATE_ONLY_NOT_EXECUTED" and queue_packet["queue_reconciliation_authorized_in_this_unit"] is False,
        "INSPECT_SELECTED_GROUP_6_NO_R1000_RUN_OR_REPAIR": report["r1000_run_executed_count"] == 0 and report["repair_executed_count"] == 0,
        "INSPECT_SELECTED_GROUP_7_NO_FIELD_VALUE_OR_TAXONOMY_ACTION": report["target_field_filled_count"] == 0 and report["descriptor_value_assignment_count"] == 0 and report["field_value_invention_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "INSPECT_SELECTED_GROUP_8_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "INSPECT_SELECTED_GROUP_9_NO_NEXT_GROUP_OR_HIDDEN_COMMAND": report["next_group_auto_opened_count"] == 0 and report["other_group_opened_count"] == 0 and report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_SELECTED_R1000_PRESSURE_GROUP_INSPECTED_QUEUE_RECONCILIATION_REQUIRED",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        }

    aggregate_metrics = {
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
        "source_prior_queue_reconciliation_receipt_id": SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": classification["pressure_class"],
        "selected_pressure_subtype": classification["pressure_subtype"],
        "selected_halt_reason": classification["halt_reason"],
        "selected_row_count": classification["row_count"],
        "selected_group_consumed_count": 1,
        "inspection_surface_materialized_count": 1,
        "selected_group_inspected_count": 1,
        "classification_emitted_count": 1,
        "burden_pressure_packet_emitted_count": 1,
        "inspection_limit_packet_emitted_count": 1,
        "queue_return_packet_emitted_count": 1,
        "metadata_only_inspection_count": 1,
        "row_payload_materialized_count": 0,
        "row_payload_inspected_count": 0,
        "queue_reconciled_count": 0,
        "next_group_auto_opened_count": 0,
        "other_group_opened_count": 0,
        "r1000_run_executed_count": 0,
        "repair_executed_count": 0,
        "proposal_applied_count": 0,
        "target_field_filled_count": 0,
        "descriptor_value_assignment_count": 0,
        "null_field_value_emitted_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": report["recommended_next_handling"],
    }

    guards = {
        "selection_consumed": True,
        "selected_group_consumed": True,
        "metadata_surface_materialized": True,
        "selected_group_inspected": True,
        "burden_pressure_classified": True,
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "queue_reconciled": False,
        "next_group_opened": False,
        "r1000_run_executed": False,
        "repair_executed": False,
        "proposal_applied": False,
        "target_field_filled": False,
        "descriptor_value_assigned": False,
        "null_field_value_emitted": False,
        "values_invented": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_selection_receipt": SOURCE_SELECTION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "classification": classification["classification_status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "inspection_surface": rel(INSPECTION_SURFACE_PATH),
        "inspection_classification": rel(INSPECTION_CLASSIFICATION_PATH),
        "burden_pressure_packet": rel(BURDEN_PRESSURE_PACKET_PATH),
        "inspection_limit_packet": rel(INSPECTION_LIMIT_PACKET_PATH),
        "queue_return_packet": rel(QUEUE_RETURN_PACKET_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_selected_pressure_group_inspection_from_reconciled_queue_receipt_v0",
        "receipt_type": "R1000_SELECTED_PRESSURE_GROUP_INSPECTION_FROM_RECONCILED_QUEUE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
        "source_prior_queue_reconciliation_receipt_id": SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "selected_group_inspection_summary": {
            "inspection_result": "BURDEN_PRESSURE_RECEIPT_SIZE_BURDEN_METADATA_REVIEWED",
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "selected_parent_pressure_class": classification["pressure_class"],
            "selected_pressure_subtype": classification["pressure_subtype"],
            "selected_halt_reason": classification["halt_reason"],
            "selected_row_count": classification["row_count"],
            "metadata_only_inspection": True,
            "row_payload_inspected": False,
            "queue_reconciled": False,
            "r1000_run_executed": False,
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "selected_group_inspection_guards": guards,
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
    print(f"selected_group_inspection_receipt_id={receipt_id}")
    print(f"selected_group_inspection_receipt_path=data/r1000_selected_pressure_group_inspection_from_reconciled_queue_v0_receipts/{receipt_id}.json")
    print(f"selected_group_inspection_classification_path=data/r1000_selected_pressure_group_inspection_from_reconciled_queue_v0/r1000_selected_pressure_group_inspection_classification.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
