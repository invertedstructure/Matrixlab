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

UNIT_ID = "INSPECT_REPAIRED_R1000_BURDEN_QUEUE_SELECTED_GROUP_AFTER_IDENTITY_REVIEW_V0"
TARGET_UNIT_ID = "r1000_repaired_burden_queue_selected_group.inspection_after_identity_review.v0"

SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID = "39f2fbe0"
SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID = "7cfe198f"
SOURCE_IDENTITY_REVIEW_RECEIPT_ID = "82c10dfc"
SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID = "1cb51143"
SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID = "d3135cdb"
SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID = "dea88520"
SOURCE_SELECTION_RECEIPT_ID = "7c561212"
SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID = "38604be8"
REPAIRED_CANDIDATE_ID = "a0dcb75d"
REPAIRED_SELECTED_PRESSURE_GROUP_ID = "113fd48b"

OUT_DIR = ROOT / "data" / "r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_v0_receipts"

INSPECTION_SURFACE_PATH = OUT_DIR / "r1000_repaired_selected_group_inspection_surface_after_identity_review.json"
INSPECTION_CLASSIFICATION_PATH = OUT_DIR / "r1000_repaired_selected_group_inspection_classification_after_identity_review.json"
BURDEN_PRESSURE_PACKET_PATH = OUT_DIR / "r1000_repaired_selected_group_burden_pressure_packet_after_identity_review.json"
INSPECTION_LIMIT_PACKET_PATH = OUT_DIR / "r1000_repaired_selected_group_inspection_limit_packet_after_identity_review.json"
QUEUE_RETURN_PACKET_PATH = OUT_DIR / "r1000_repaired_selected_group_inspection_queue_return_packet_after_identity_review.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_repaired_selected_group_inspection_transition_trace_after_identity_review.json"
REPORT_PATH = OUT_DIR / "r1000_repaired_selected_group_inspection_report_after_identity_review.json"

REPAIRED_IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_repaired_burden_queue_candidate_identity_surface_review_v0_receipts" / f"{SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID}.json"
REPAIRED_IDENTITY_SURFACE_PATH = ROOT / "data" / "r1000_repaired_burden_queue_candidate_identity_surface_review_v0" / "r1000_repaired_burden_queue_candidate_identity_surface.json"
REPAIRED_IDENTITY_DECISION_PATH = ROOT / "data" / "r1000_repaired_burden_queue_candidate_identity_surface_review_v0" / "r1000_repaired_burden_queue_candidate_identity_review_decision.json"
REPAIRED_IDENTITY_ACCEPTANCE_PACKET_PATH = ROOT / "data" / "r1000_repaired_burden_queue_candidate_identity_surface_review_v0" / "r1000_repaired_burden_queue_candidate_identity_acceptance_packet.json"
REPAIRED_INSPECTION_AUTHORITY_PACKET_PATH = ROOT / "data" / "r1000_repaired_burden_queue_candidate_identity_surface_review_v0" / "r1000_repaired_burden_queue_candidate_inspection_authority_packet.json"

IDENTITY_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0_receipts" / f"{SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID}.json"
REPAIRED_SELECTED_GROUP_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0" / "r1000_selected_pressure_group_after_burden_identity_preserved.json"
REPAIRED_CANDIDATE_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0" / "r1000_next_selectable_group_candidate_after_burden_identity_preserved.json"
INSPECTION_RELEASE_PACKET_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0" / "r1000_burden_queue_identity_preserved_inspection_release_packet.json"

IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_selected_group_after_burden_identity_surface_review_v0_receipts" / f"{SOURCE_IDENTITY_REVIEW_RECEIPT_ID}.json"
SELECTION_AFTER_BURDEN_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_burden_pressure_reconciliation_v0_receipts" / f"{SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID}.json"
BURDEN_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0_receipts" / f"{SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
SELECTED_GROUP_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID}.json"
SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTION_RECEIPT_ID}.json"
QUEUE_RECONCILIATION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    REPAIRED_IDENTITY_REVIEW_RECEIPT_PATH,
    REPAIRED_IDENTITY_SURFACE_PATH,
    REPAIRED_IDENTITY_DECISION_PATH,
    REPAIRED_IDENTITY_ACCEPTANCE_PACKET_PATH,
    REPAIRED_INSPECTION_AUTHORITY_PACKET_PATH,
    IDENTITY_FIX_RECEIPT_PATH,
    REPAIRED_SELECTED_GROUP_PATH,
    REPAIRED_CANDIDATE_PATH,
    INSPECTION_RELEASE_PACKET_PATH,
    IDENTITY_REVIEW_RECEIPT_PATH,
    SELECTION_AFTER_BURDEN_RECEIPT_PATH,
    BURDEN_QUEUE_RECEIPT_PATH,
    SELECTED_GROUP_INSPECTION_RECEIPT_PATH,
    SELECTION_RECEIPT_PATH,
    QUEUE_RECONCILIATION_RECEIPT_PATH,
]

RECOMMENDED_NEXT_HANDLING = "RECONCILE_R1000_PRESSURE_QUEUE_AFTER_REPAIRED_BURDEN_GROUP_INSPECTION_V0"

HUMAN_DECISION = {
    "decision": "INSPECT_REPAIRED_R1000_BURDEN_QUEUE_SELECTED_GROUP_AFTER_IDENTITY_REVIEW",
    "scope": "consume the repaired selected burden group and inspect it at metadata/surface level only; classify receipt-size burden pressure and emit queue-return packet without row payload inspection, R1000 execution, repair, or queue reconciliation",
    "source_repaired_identity_review_receipt_id": SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID,
    "source_identity_preservation_fix_receipt_id": SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID,
    "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
    "authorized": [
        "consume repaired identity review receipt",
        "consume repaired selected group artifact",
        "consume separate inspection authority packet",
        "materialize metadata-level inspection surface",
        "classify repaired selected group pressure behavior",
        "emit burden-pressure packet",
        "emit inspection limit packet",
        "emit queue return packet candidate only",
        "stop before queue reconciliation",
    ],
    "not_authorized": [
        "materializing selected-group row payloads",
        "inspecting selected-group rows",
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
        "queue reconciliation",
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
        "repaired_identity_review_receipt": read_json(REPAIRED_IDENTITY_REVIEW_RECEIPT_PATH),
        "repaired_identity_surface": read_json(REPAIRED_IDENTITY_SURFACE_PATH),
        "repaired_identity_decision": read_json(REPAIRED_IDENTITY_DECISION_PATH),
        "repaired_identity_acceptance_packet": read_json(REPAIRED_IDENTITY_ACCEPTANCE_PACKET_PATH),
        "repaired_inspection_authority_packet": read_json(REPAIRED_INSPECTION_AUTHORITY_PACKET_PATH),
        "identity_fix_receipt": read_json(IDENTITY_FIX_RECEIPT_PATH),
        "repaired_selected_group": read_json(REPAIRED_SELECTED_GROUP_PATH),
        "repaired_candidate": read_json(REPAIRED_CANDIDATE_PATH),
        "inspection_release_packet": read_json(INSPECTION_RELEASE_PACKET_PATH),
        "identity_review_receipt": read_json(IDENTITY_REVIEW_RECEIPT_PATH),
        "selection_after_burden_receipt": read_json(SELECTION_AFTER_BURDEN_RECEIPT_PATH),
        "burden_queue_receipt": read_json(BURDEN_QUEUE_RECEIPT_PATH),
        "selected_group_inspection_receipt": read_json(SELECTED_GROUP_INSPECTION_RECEIPT_PATH),
        "selection_receipt": read_json(SELECTION_RECEIPT_PATH),
        "queue_reconciliation_receipt": read_json(QUEUE_RECONCILIATION_RECEIPT_PATH),
    }

def is_unknown(v: Any) -> bool:
    return v is None or v == "" or v == "UNKNOWN"

def fully_typed(group: Dict[str, Any]) -> bool:
    return (
        not is_unknown(group.get("parent_pressure_class"))
        and not is_unknown(group.get("pressure_subtype"))
        and not is_unknown(group.get("halt_reason"))
        and int(group.get("row_count", 0) or 0) > 0
    )

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    receipt = sources["repaired_identity_review_receipt"]
    decision = sources["repaired_identity_decision"]
    authority = sources["repaired_inspection_authority_packet"]
    selected = sources["repaired_selected_group"]
    candidate = sources["repaired_candidate"]

    if receipt.get("receipt_id") != SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID:
        failures.append("repaired_identity_review_receipt_id_wrong")
    if receipt.get("gate") != "PASS":
        failures.append("repaired_identity_review_not_pass")
    if receipt.get("repaired_selected_pressure_group_id") != REPAIRED_SELECTED_PRESSURE_GROUP_ID:
        failures.append("repaired_selected_id_wrong_in_review_receipt")
    if receipt.get("aggregate_metrics", {}).get("identity_complete_count") != 1:
        failures.append("repaired_identity_not_complete_in_review_receipt")
    if receipt.get("aggregate_metrics", {}).get("inspection_allowed_in_separate_unit_count") != 1:
        failures.append("separate_inspection_not_allowed")
    if receipt.get("aggregate_metrics", {}).get("inspection_authorized_in_this_unit_count") != 0:
        failures.append("review_unit_authorized_inspection")

    if decision.get("decision_status") != "ACCEPT_REPAIRED_IDENTITY_FOR_SEPARATE_INSPECTION":
        failures.append("repaired_identity_decision_status_wrong")
    if decision.get("inspection_allowed_in_separate_unit") is not True:
        failures.append("decision_does_not_allow_separate_inspection")
    if decision.get("inspection_authorized_in_this_unit") is not False:
        failures.append("decision_authorized_inspection_in_review_unit")

    if authority.get("packet_status") != "SEPARATE_INSPECTION_AUTHORITY_PACKET":
        failures.append("inspection_authority_packet_status_wrong")
    if authority.get("repaired_selected_pressure_group_id") != REPAIRED_SELECTED_PRESSURE_GROUP_ID:
        failures.append("inspection_authority_packet_selected_id_wrong")

    if selected.get("selected_pressure_group_id") != REPAIRED_SELECTED_PRESSURE_GROUP_ID:
        failures.append("repaired_selected_group_id_wrong")
    if selected.get("selection_status") != "SELECTED_NOT_INSPECTED":
        failures.append("repaired_selected_group_status_wrong")
    if selected.get("selected_group_rows_inspected") is not False:
        failures.append("repaired_selected_group_already_inspected")
    if selected.get("r1000_run_executed") is not False:
        failures.append("repaired_selected_group_r1000_already_run")
    if not fully_typed(selected.get("selected_group", {})):
        failures.append("repaired_selected_group_not_fully_typed")

    if candidate.get("repaired_candidate_id") != REPAIRED_CANDIDATE_ID:
        failures.append("repaired_candidate_id_wrong")
    if candidate.get("selection_status") != "CANDIDATE_ONLY_NOT_OPENED":
        failures.append("repaired_candidate_status_wrong")
    if candidate.get("next_group_opened") is not False:
        failures.append("repaired_candidate_already_opened")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def selected_group_summary(sources: Dict[str, Any]) -> Dict[str, Any]:
    group = sources["repaired_selected_group"].get("selected_group", {})
    return {
        "parent_pressure_class": group.get("parent_pressure_class"),
        "pressure_subtype": group.get("pressure_subtype"),
        "halt_reason": group.get("halt_reason"),
        "row_count": int(group.get("row_count", 0) or 0),
    }

def build_inspection_surface(sources: Dict[str, Any]) -> Dict[str, Any]:
    group = selected_group_summary(sources)
    return {
        "schema_version": "r1000_repaired_selected_group_inspection_surface_after_identity_review_v0",
        "inspection_surface_id": sha8({
            "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
            "group": group,
            "inspection": "metadata_only_after_repaired_identity_review",
        }),
        "source_repaired_identity_review_receipt_id": SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID,
        "source_identity_preservation_fix_receipt_id": SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID,
        "source_repaired_selected_group_ref": rel(REPAIRED_SELECTED_GROUP_PATH),
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "surface_status": "REPAIRED_SELECTED_GROUP_METADATA_INSPECTION_SURFACE_MATERIALIZED",
        "selected_group": group,
        "metadata_only_inspection": True,
        "identity_complete": fully_typed(group),
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "r1000_run_executed": False,
    }

def build_classification(surface: Dict[str, Any]) -> Dict[str, Any]:
    group = surface["selected_group"]
    is_burden_receipt_size = (
        group.get("parent_pressure_class") == "BURDEN_PRESSURE"
        and group.get("pressure_subtype") == "receipt_size_burden"
        and group.get("halt_reason") == "STOP_DONE"
    )
    status = "BURDEN_PRESSURE_RECEIPT_SIZE_BURDEN_METADATA_REVIEWED" if is_burden_receipt_size else "REPAIRED_SELECTED_GROUP_CLASSIFICATION_REQUIRES_SCHEMA_REVIEW"

    return {
        "schema_version": "r1000_repaired_selected_group_inspection_classification_after_identity_review_v0",
        "classification_id": sha8({
            "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
            "group": group,
            "classification": status,
        }),
        "source_inspection_surface_ref": rel(INSPECTION_SURFACE_PATH),
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "classification_status": status,
        "selected_group": group,
        "semantic_interpretation": {
            "is_burden_pressure": group.get("parent_pressure_class") == "BURDEN_PRESSURE",
            "is_receipt_size_burden": group.get("pressure_subtype") == "receipt_size_burden",
            "selected_halt_reason_stop_done": group.get("halt_reason") == "STOP_DONE",
            "requires_r1000_run": False,
            "requires_row_payload_inspection": False,
            "requires_burden_policy_rewrite": False,
            "requires_queue_reconciliation_after_inspection": True,
        },
        "metadata_only_inspection": True,
        "row_payload_inspected": False,
        "r1000_run_executed": False,
    }

def build_burden_packet(surface: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_repaired_selected_group_burden_pressure_packet_after_identity_review_v0",
        "packet_status": "BURDEN_PRESSURE_METADATA_REVIEWED",
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "selected_group": surface["selected_group"],
        "classification_status": classification["classification_status"],
        "burden_pressure_type": "receipt_size_burden",
        "burden_pressure_handling": "metadata_reviewed_only",
        "row_payload_inspection_authorized": False,
        "r1000_run_authorized": False,
        "burden_policy_rewrite_authorized": False,
        "queue_reconciliation_required": True,
    }

def build_limit_packet(surface: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_repaired_selected_group_inspection_limit_packet_after_identity_review_v0",
        "packet_status": "INSPECTION_LIMIT_RECORDED",
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "limit_type": "METADATA_ONLY_BURDEN_PRESSURE_INSPECTION",
        "selected_group": surface["selected_group"],
        "classification_status": classification["classification_status"],
        "limits": {
            "row_payload_materialized": False,
            "row_payload_inspected": False,
            "r1000_run_executed": False,
            "repair_executed": False,
            "queue_reconciled": False,
            "identity_assignment": False,
            "field_value_invention": False,
        },
        "allowed_next_scope": "queue reconciliation in separate unit only",
    }

def build_queue_return_packet(surface: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_repaired_selected_group_inspection_queue_return_packet_after_identity_review_v0",
        "packet_status": "CANDIDATE_ONLY_NOT_EXECUTED",
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "selected_group": surface["selected_group"],
        "inspection_completed": True,
        "inspection_result": classification["classification_status"],
        "queue_reconciliation_authorized_in_this_unit": False,
        "queue_reconciliation_required": True,
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
    }

def build_transition_trace(surface: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_repaired_selected_group_inspection_transition_trace_after_identity_review_v0",
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "trace": [
            {
                "step": "consume_repaired_identity_review",
                "question": "repaired identity accepted for separate inspection",
                "answer": True,
                "taken": "consume_repaired_selected_group",
            },
            {
                "step": "consume_repaired_selected_group",
                "question": "selected group is identity-complete and not inspected",
                "answer": True,
                "taken": "materialize_metadata_inspection_surface",
            },
            {
                "step": "materialize_metadata_inspection_surface",
                "question": "inspect row payloads in this unit",
                "answer": False,
                "taken": "classify_metadata_surface",
            },
            {
                "step": "classify_metadata_surface",
                "question": "is repaired group receipt-size burden pressure",
                "answer": classification["classification_status"] == "BURDEN_PRESSURE_RECEIPT_SIZE_BURDEN_METADATA_REVIEWED",
                "taken": "emit_queue_return_packet",
            },
            {
                "step": "emit_queue_return_packet",
                "question": "queue reconcile in this unit",
                "answer": False,
                "taken": "STOP_REPAIRED_SELECTED_GROUP_INSPECTED_QUEUE_RECONCILIATION_REQUIRED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_REPAIRED_SELECTED_GROUP_INSPECTED_QUEUE_RECONCILIATION_REQUIRED",
            "next_command_goal": None,
        },
    }

def build_report(surface: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
    group = surface["selected_group"]
    return {
        "schema_version": "r1000_repaired_selected_group_inspection_report_after_identity_review_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_repaired_identity_review_receipt_id": SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID,
        "source_identity_preservation_fix_receipt_id": SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": group.get("parent_pressure_class"),
        "selected_pressure_subtype": group.get("pressure_subtype"),
        "selected_halt_reason": group.get("halt_reason"),
        "selected_row_count": group.get("row_count"),
        "repaired_identity_review_consumed_count": 1,
        "repaired_selected_group_consumed_count": 1,
        "inspection_authority_packet_consumed_count": 1,
        "inspection_surface_materialized_count": 1,
        "metadata_only_inspection_count": 1,
        "classification_emitted_count": 1,
        "burden_pressure_packet_emitted_count": 1,
        "inspection_limit_packet_emitted_count": 1,
        "queue_return_packet_emitted_count": 1,
        "selected_group_inspected_count": 1,
        "classification_status": classification["classification_status"],
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
        "identity_assignment_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
    }

def validate_outputs(
    surface: Dict[str, Any],
    classification: Dict[str, Any],
    burden_packet: Dict[str, Any],
    limit_packet: Dict[str, Any],
    queue_return_packet: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if surface.get("surface_status") != "REPAIRED_SELECTED_GROUP_METADATA_INSPECTION_SURFACE_MATERIALIZED":
        failures.append("inspection_surface_status_wrong")
    if surface.get("metadata_only_inspection") is not True:
        failures.append("metadata_only_flag_missing")
    if surface.get("row_payload_inspected") is not False:
        failures.append("surface_row_payload_inspected")
    if surface.get("r1000_run_executed") is not False:
        failures.append("surface_r1000_run")

    if classification.get("classification_status") != "BURDEN_PRESSURE_RECEIPT_SIZE_BURDEN_METADATA_REVIEWED":
        failures.append("classification_status_wrong")
    if classification.get("semantic_interpretation", {}).get("requires_r1000_run") is not False:
        failures.append("classification_requires_r1000")
    if classification.get("semantic_interpretation", {}).get("requires_row_payload_inspection") is not False:
        failures.append("classification_requires_row_payload")
    if classification.get("semantic_interpretation", {}).get("requires_queue_reconciliation_after_inspection") is not True:
        failures.append("classification_missing_queue_reconciliation_requirement")

    if burden_packet.get("burden_pressure_handling") != "metadata_reviewed_only":
        failures.append("burden_packet_handling_wrong")
    if burden_packet.get("row_payload_inspection_authorized") is not False:
        failures.append("burden_packet_authorizes_row_payload")
    if burden_packet.get("r1000_run_authorized") is not False:
        failures.append("burden_packet_authorizes_r1000")
    if limit_packet.get("limits", {}).get("row_payload_inspected") is not False:
        failures.append("limit_packet_row_payload_inspected")
    if queue_return_packet.get("packet_status") != "CANDIDATE_ONLY_NOT_EXECUTED":
        failures.append("queue_return_packet_not_candidate_only")
    if queue_return_packet.get("queue_reconciliation_authorized_in_this_unit") is not False:
        failures.append("queue_return_authorizes_reconciliation")
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
        "identity_assignment_count",
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
    if report.get("metadata_only_inspection_count") != 1:
        failures.append("metadata_only_count_wrong")
    if report.get("queue_return_packet_emitted_count") != 1:
        failures.append("queue_return_packet_count_wrong")

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
    if metrics.get("metadata_only_inspection_count") != 1:
        failures.append("metric_metadata_only_wrong")
    if metrics.get("classification_emitted_count") != 1:
        failures.append("metric_classification_wrong")

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
        "identity_assignment_count",
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
    if terminal.get("stop_code") != "STOP_REPAIRED_SELECTED_GROUP_INSPECTED_QUEUE_RECONCILIATION_REQUIRED":
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

    surface = build_inspection_surface(sources)
    classification = build_classification(surface)
    burden_packet = build_burden_packet(surface, classification)
    limit_packet = build_limit_packet(surface, classification)
    queue_return_packet = build_queue_return_packet(surface, classification)
    trace = build_transition_trace(surface, classification)
    report = build_report(surface, classification)

    write_json(INSPECTION_SURFACE_PATH, surface)
    write_json(INSPECTION_CLASSIFICATION_PATH, classification)
    write_json(BURDEN_PRESSURE_PACKET_PATH, burden_packet)
    write_json(INSPECTION_LIMIT_PACKET_PATH, limit_packet)
    write_json(QUEUE_RETURN_PACKET_PATH, queue_return_packet)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(
        surface,
        classification,
        burden_packet,
        limit_packet,
        queue_return_packet,
        trace,
        report,
    ))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "REPAIRED_INSPECTION_0_REPAIRED_IDENTITY_REVIEW_CONSUMED": sources["repaired_identity_review_receipt"]["receipt_id"] == SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID and sources["repaired_identity_review_receipt"]["gate"] == "PASS",
        "REPAIRED_INSPECTION_1_REPAIRED_SELECTED_GROUP_CONSUMED": sources["repaired_selected_group"]["selected_pressure_group_id"] == REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "REPAIRED_INSPECTION_2_INSPECTION_AUTHORITY_CONSUMED": sources["repaired_inspection_authority_packet"]["packet_status"] == "SEPARATE_INSPECTION_AUTHORITY_PACKET",
        "REPAIRED_INSPECTION_3_METADATA_SURFACE_MATERIALIZED": surface["surface_status"] == "REPAIRED_SELECTED_GROUP_METADATA_INSPECTION_SURFACE_MATERIALIZED",
        "REPAIRED_INSPECTION_4_BURDEN_PRESSURE_CLASSIFIED": classification["classification_status"] == "BURDEN_PRESSURE_RECEIPT_SIZE_BURDEN_METADATA_REVIEWED",
        "REPAIRED_INSPECTION_5_ROW_PAYLOAD_NOT_MATERIALIZED": report["row_payload_materialized_count"] == 0 and report["row_payload_inspected_count"] == 0,
        "REPAIRED_INSPECTION_6_QUEUE_RETURN_PACKET_CANDIDATE_ONLY": queue_return_packet["packet_status"] == "CANDIDATE_ONLY_NOT_EXECUTED" and queue_return_packet["queue_reconciliation_authorized_in_this_unit"] is False,
        "REPAIRED_INSPECTION_7_NO_R1000_RUN_OR_REPAIR": report["r1000_run_executed_count"] == 0 and report["repair_executed_count"] == 0,
        "REPAIRED_INSPECTION_8_NO_FIELD_VALUE_OR_TAXONOMY_ACTION": report["target_field_filled_count"] == 0 and report["descriptor_value_assignment_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "REPAIRED_INSPECTION_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "REPAIRED_INSPECTION_10_NO_NEXT_GROUP_OR_HIDDEN_COMMAND": report["next_group_auto_opened_count"] == 0 and report["other_group_opened_count"] == 0 and report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_REPAIRED_SELECTED_GROUP_INSPECTED_QUEUE_RECONCILIATION_REQUIRED",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        }

    aggregate_metrics = {
        "source_repaired_identity_review_receipt_id": SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID,
        "source_identity_preservation_fix_receipt_id": SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID,
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_burden_receipt_id": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": surface["selected_group"].get("parent_pressure_class"),
        "selected_pressure_subtype": surface["selected_group"].get("pressure_subtype"),
        "selected_halt_reason": surface["selected_group"].get("halt_reason"),
        "selected_row_count": surface["selected_group"].get("row_count"),
        "repaired_identity_review_consumed_count": 1,
        "repaired_selected_group_consumed_count": 1,
        "inspection_authority_packet_consumed_count": 1,
        "inspection_surface_materialized_count": 1,
        "metadata_only_inspection_count": 1,
        "classification_emitted_count": 1,
        "burden_pressure_packet_emitted_count": 1,
        "inspection_limit_packet_emitted_count": 1,
        "queue_return_packet_emitted_count": 1,
        "selected_group_inspected_count": 1,
        "classification_status": classification["classification_status"],
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
        "identity_assignment_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
    }

    guards = {
        "repaired_identity_review_consumed": True,
        "repaired_selected_group_consumed": True,
        "inspection_authority_packet_consumed": True,
        "metadata_surface_materialized": True,
        "burden_pressure_classified": True,
        "metadata_only_inspection": True,
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "queue_return_packet_emitted": True,
        "queue_reconciled": False,
        "next_group_opened": False,
        "r1000_run_executed": False,
        "repair_executed": False,
        "proposal_applied": False,
        "target_field_filled": False,
        "descriptor_value_assigned": False,
        "null_field_value_emitted": False,
        "field_value_invention": False,
        "identity_assignment": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_repaired_identity_review_receipt": SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
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
        "schema_version": "r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_receipt_v0",
        "receipt_type": "R1000_REPAIRED_BURDEN_QUEUE_SELECTED_GROUP_INSPECTION_AFTER_IDENTITY_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_repaired_identity_review_receipt_id": SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID,
        "source_identity_preservation_fix_receipt_id": SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID,
        "source_identity_review_receipt_id": SOURCE_IDENTITY_REVIEW_RECEIPT_ID,
        "source_selection_after_burden_receipt_id": SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "repaired_selected_group_inspection_summary": {
            "inspection_result": classification["classification_status"],
            "metadata_only_inspection": True,
            "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
            "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
            "selected_group": surface["selected_group"],
            "row_payload_inspected": False,
            "queue_reconciled": False,
            "r1000_run_executed": False,
            "recommended_next_handling": RECOMMENDED_NEXT_HANDLING,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "repaired_selected_group_inspection_guards": guards,
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
    print(f"repaired_selected_group_inspection_receipt_id={receipt_id}")
    print(f"repaired_selected_group_inspection_receipt_path=data/r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_v0_receipts/{receipt_id}.json")
    print(f"repaired_selected_group_inspection_classification_path=data/r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_v0/r1000_repaired_selected_group_inspection_classification_after_identity_review.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
