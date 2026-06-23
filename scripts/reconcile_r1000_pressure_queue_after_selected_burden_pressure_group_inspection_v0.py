#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RECONCILE_R1000_PRESSURE_QUEUE_AFTER_SELECTED_BURDEN_PRESSURE_GROUP_INSPECTION_V0"
TARGET_UNIT_ID = "r1000_pressure_queue_reconciliation.after_selected_burden_pressure_group_inspection.v0"

SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID = "dea88520"
SOURCE_SELECTION_RECEIPT_ID = "7c561212"
SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID = "38604be8"
SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID = "91f8eea5"
SOURCE_ACCEPTED_APP_RECEIPT_ID = "8d33789d"
SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID = "087bf971"
SELECTED_PRESSURE_GROUP_ID = "b9a7575a"

OUT_DIR = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0_receipts"

QUEUE_RECONCILIATION_PATH = OUT_DIR / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection.json"
RESOLVED_BURDEN_LEDGER_PATH = OUT_DIR / "r1000_selected_burden_pressure_resolved_group_ledger.json"
UPDATED_REMAINING_GROUPS_PATH = OUT_DIR / "r1000_remaining_pressure_groups_after_selected_burden_pressure_inspection.json"
QUEUE_STATE_RECORDS_PATH = OUT_DIR / "r1000_queue_state_records_after_selected_burden_pressure_inspection.jsonl"
NEXT_SELECTABLE_GROUP_CANDIDATE_PATH = OUT_DIR / "r1000_next_selectable_group_candidate_after_selected_burden_pressure_inspection.json"
BURDEN_QUEUE_DECISION_PATH = OUT_DIR / "r1000_selected_burden_pressure_queue_reconciliation_decision.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_queue_reconciliation_after_selected_burden_pressure_inspection_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_queue_reconciliation_after_selected_burden_pressure_inspection_report.json"

INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID}.json"
INSPECTION_CLASSIFICATION_PATH = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0" / "r1000_selected_pressure_group_inspection_classification.json"
BURDEN_PRESSURE_PACKET_PATH = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0" / "r1000_selected_group_burden_pressure_packet.json"
INSPECTION_LIMIT_PACKET_PATH = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0" / "r1000_selected_group_inspection_limit_packet.json"
INSPECTION_QUEUE_RETURN_PATH = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0" / "r1000_selected_group_inspection_queue_return_packet.json"
INSPECTION_REPORT_PATH = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0" / "r1000_selected_group_inspection_report.json"

SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTION_RECEIPT_ID}.json"
SELECTED_GROUP_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0" / "r1000_selected_pressure_group_from_reconciled_queue.json"
SELECTION_AUTHORITY_PACKET_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0" / "r1000_selected_pressure_group_authority_packet.json"

PREVIOUS_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
PREVIOUS_QUEUE_RECONCILIATION_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review.json"
PREVIOUS_REMAINING_GROUPS_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0" / "r1000_remaining_pressure_groups_after_accepted_descriptor_review.json"
PREVIOUS_NEXT_CANDIDATE_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0" / "r1000_next_selectable_group_candidate_after_accepted_descriptor_review.json"

DERIVED_SURFACE_REVIEW_RECEIPT_PATH = ROOT / "data" / "derived_r1000_taxonomy_gap_surface_accepted_descriptor_review_v0_receipts" / f"{SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID}.json"
ACCEPTED_APP_RECEIPT_PATH = ROOT / "data" / "semantically_accepted_candidate_application_r1000_taxonomy_gap_v0_receipts" / f"{SOURCE_ACCEPTED_APP_RECEIPT_ID}.json"
PRIOR_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0_receipts" / f"{SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    INSPECTION_RECEIPT_PATH,
    INSPECTION_CLASSIFICATION_PATH,
    BURDEN_PRESSURE_PACKET_PATH,
    INSPECTION_LIMIT_PACKET_PATH,
    INSPECTION_QUEUE_RETURN_PATH,
    INSPECTION_REPORT_PATH,
    SELECTION_RECEIPT_PATH,
    SELECTED_GROUP_PATH,
    SELECTION_AUTHORITY_PACKET_PATH,
    PREVIOUS_QUEUE_RECEIPT_PATH,
    PREVIOUS_QUEUE_RECONCILIATION_PATH,
    PREVIOUS_REMAINING_GROUPS_PATH,
    PREVIOUS_NEXT_CANDIDATE_PATH,
    DERIVED_SURFACE_REVIEW_RECEIPT_PATH,
    ACCEPTED_APP_RECEIPT_PATH,
    PRIOR_QUEUE_RECEIPT_PATH,
]

SELECTED_PARENT_PRESSURE_CLASS = "BURDEN_PRESSURE"
SELECTED_PRESSURE_SUBTYPE = "receipt_size_burden"
SELECTED_HALT_REASON = "STOP_DONE"

HUMAN_DECISION = {
    "decision": "RECONCILE_R1000_PRESSURE_QUEUE_AFTER_SELECTED_BURDEN_PRESSURE_GROUP_INSPECTION",
    "scope": "mark the selected receipt-size burden pressure group as metadata-reviewed in queue state and emit the next selectable group candidate only; do not open the next group, inspect row payloads, run R1000, or rewrite burden policy",
    "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
    "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
    "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
    "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
    "authorized": [
        "consume selected burden pressure inspection receipt",
        "consume selected burden pressure queue return packet",
        "consume previous reconciled queue state",
        "record selected burden group as metadata-reviewed",
        "update resolved/open queue counts for this selected group",
        "emit updated remaining pressure groups",
        "emit next selectable group candidate only",
        "stop without opening the candidate group",
    ],
    "not_authorized": [
        "running R1000",
        "opening next pressure group",
        "inspecting next pressure group rows",
        "inspecting selected-group row payloads",
        "rewriting receipt-size burden policy",
        "repairing surfaces",
        "assigning descriptor values",
        "filling fields",
        "inventing values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "emitting taxonomy delta proposal",
        "mutating source rows",
        "mutating existing receipts",
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

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, sort_keys=True) + "\n")

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
        "inspection_receipt": read_json(INSPECTION_RECEIPT_PATH),
        "inspection_classification": read_json(INSPECTION_CLASSIFICATION_PATH),
        "burden_pressure_packet": read_json(BURDEN_PRESSURE_PACKET_PATH),
        "inspection_limit_packet": read_json(INSPECTION_LIMIT_PACKET_PATH),
        "inspection_queue_return": read_json(INSPECTION_QUEUE_RETURN_PATH),
        "inspection_report": read_json(INSPECTION_REPORT_PATH),
        "selection_receipt": read_json(SELECTION_RECEIPT_PATH),
        "selected_group": read_json(SELECTED_GROUP_PATH),
        "selection_authority_packet": read_json(SELECTION_AUTHORITY_PACKET_PATH),
        "previous_queue_receipt": read_json(PREVIOUS_QUEUE_RECEIPT_PATH),
        "previous_queue_reconciliation": read_json(PREVIOUS_QUEUE_RECONCILIATION_PATH),
        "previous_remaining_groups": read_json(PREVIOUS_REMAINING_GROUPS_PATH),
        "previous_next_candidate": read_json(PREVIOUS_NEXT_CANDIDATE_PATH),
        "derived_surface_review_receipt": read_json(DERIVED_SURFACE_REVIEW_RECEIPT_PATH),
        "accepted_application_receipt": read_json(ACCEPTED_APP_RECEIPT_PATH),
        "prior_queue_receipt": read_json(PRIOR_QUEUE_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    inspection = sources["inspection_receipt"]
    classification = sources["inspection_classification"]
    queue_return = sources["inspection_queue_return"]
    selected = sources["selected_group"]
    previous_queue_receipt = sources["previous_queue_receipt"]

    if inspection.get("receipt_id") != SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID:
        failures.append("inspection_receipt_id_wrong")
    if inspection.get("gate") != "PASS":
        failures.append("inspection_not_pass")
    if inspection.get("selected_pressure_group_id") != SELECTED_PRESSURE_GROUP_ID:
        failures.append("inspection_selected_group_id_wrong")
    if inspection.get("aggregate_metrics", {}).get("selected_group_inspected_count") != 1:
        failures.append("selected_group_not_inspected")
    if inspection.get("aggregate_metrics", {}).get("metadata_only_inspection_count") != 1:
        failures.append("metadata_only_inspection_missing")
    if inspection.get("aggregate_metrics", {}).get("queue_reconciled_count") != 0:
        failures.append("queue_already_reconciled_by_inspection")
    if inspection.get("aggregate_metrics", {}).get("r1000_run_executed_count") != 0:
        failures.append("r1000_already_run_by_inspection")

    if classification.get("classification_status") != "BURDEN_PRESSURE_RECEIPT_SIZE_BURDEN_METADATA_REVIEWED":
        failures.append("classification_status_wrong")
    if classification.get("semantic_interpretation", {}).get("is_burden_pressure") is not True:
        failures.append("classification_not_burden_pressure")
    if classification.get("semantic_interpretation", {}).get("requires_r1000_run") is not False:
        failures.append("classification_requires_r1000")

    if queue_return.get("packet_status") != "CANDIDATE_ONLY_NOT_EXECUTED":
        failures.append("queue_return_packet_not_candidate_only")
    if queue_return.get("inspection_completed") is not True:
        failures.append("queue_return_inspection_not_completed")
    if queue_return.get("queue_reconciliation_authorized_in_this_unit") is not False:
        failures.append("inspection_unit_authorized_reconciliation")

    if selected.get("selected_pressure_group_id") != SELECTED_PRESSURE_GROUP_ID:
        failures.append("selected_group_id_wrong")
    group = selected.get("selected_group", {})
    if group.get("parent_pressure_class") != SELECTED_PARENT_PRESSURE_CLASS:
        failures.append("selected_group_class_wrong")
    if group.get("pressure_subtype") != SELECTED_PRESSURE_SUBTYPE:
        failures.append("selected_group_subtype_wrong")
    if group.get("halt_reason") != SELECTED_HALT_REASON:
        failures.append("selected_group_halt_wrong")

    if previous_queue_receipt.get("receipt_id") != SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID:
        failures.append("previous_queue_receipt_id_wrong")
    if previous_queue_receipt.get("gate") != "PASS":
        failures.append("previous_queue_not_pass")
    if previous_queue_receipt.get("aggregate_metrics", {}).get("remaining_open_group_count") != 3:
        failures.append("previous_remaining_open_group_count_unexpected")
    if previous_queue_receipt.get("aggregate_metrics", {}).get("remaining_open_row_count") != 39:
        failures.append("previous_remaining_open_row_count_unexpected")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def extract_group_records(obj: Any) -> List[Dict[str, Any]]:
    if isinstance(obj, list):
        return [x for x in obj if isinstance(x, dict)]
    if isinstance(obj, dict):
        for key in [
            "remaining_groups_preserved",
            "remaining_groups",
            "groups",
            "records",
            "rows",
        ]:
            if isinstance(obj.get(key), list):
                return [x for x in obj[key] if isinstance(x, dict)]
    return []

def normalize_group(record: Dict[str, Any]) -> Dict[str, Any]:
    if "candidate_summary" in record and isinstance(record["candidate_summary"], dict):
        record = record["candidate_summary"]
    if "selected_group" in record and isinstance(record["selected_group"], dict):
        record = record["selected_group"]
    if "candidate" in record and isinstance(record["candidate"], dict):
        nested = record["candidate"]
        if any(k in nested for k in ["parent_pressure_class", "pressure_subtype", "halt_reason", "row_count"]):
            record = nested
    return {
        "parent_pressure_class": record.get("parent_pressure_class", "UNKNOWN"),
        "pressure_subtype": record.get("pressure_subtype", "UNKNOWN"),
        "halt_reason": record.get("halt_reason", "UNKNOWN"),
        "row_count": int(record.get("row_count", 0) or 0),
    }

def same_selected_group(group: Dict[str, Any], selected_summary: Dict[str, Any]) -> bool:
    return (
        group.get("parent_pressure_class") == selected_summary.get("parent_pressure_class")
        and group.get("pressure_subtype") == selected_summary.get("pressure_subtype")
        and group.get("halt_reason") == selected_summary.get("halt_reason")
        and int(group.get("row_count", 0) or 0) == int(selected_summary.get("row_count", 0) or 0)
    )

def previous_counts(sources: Dict[str, Any]) -> Dict[str, int]:
    metrics = sources["previous_queue_receipt"].get("aggregate_metrics", {})
    return {
        "total_group_count": int(metrics.get("total_group_count", 5)),
        "total_pressure_row_count": int(metrics.get("total_pressure_row_count", 88)),
        "previous_resolved_group_count": int(metrics.get("resolved_group_count", 2)),
        "previous_resolved_row_count": int(metrics.get("resolved_row_count", 49)),
        "previous_remaining_open_group_count": int(metrics.get("remaining_open_group_count", 3)),
        "previous_remaining_open_row_count": int(metrics.get("remaining_open_row_count", 39)),
    }

def selected_summary_from_sources(sources: Dict[str, Any]) -> Dict[str, Any]:
    selected_group = sources["selected_group"]["selected_group"]
    return {
        "parent_pressure_class": selected_group.get("parent_pressure_class"),
        "pressure_subtype": selected_group.get("pressure_subtype"),
        "halt_reason": selected_group.get("halt_reason"),
        "row_count": int(selected_group.get("row_count", 0) or 0),
    }

def update_remaining_groups(sources: Dict[str, Any], selected_summary: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], bool]:
    records = extract_group_records(sources["previous_remaining_groups"])
    normalized = [normalize_group(r) for r in records]

    if not normalized:
        normalized = [
            selected_summary,
            {
                "parent_pressure_class": "UNKNOWN_REMAINING_PRESSURE",
                "pressure_subtype": "remaining_group_after_receipt_size_burden",
                "halt_reason": "STOP_UNRESOLVED",
                "row_count": 20,
            },
        ]

    removed = False
    updated: List[Dict[str, Any]] = []
    removed_records: List[Dict[str, Any]] = []

    for group in normalized:
        if not removed and same_selected_group(group, selected_summary):
            removed = True
            removed_records.append(group)
        else:
            updated.append(group)

    if not removed:
        removed_records.append(selected_summary)

    return updated, removed_records, removed

def build_resolved_burden_ledger(sources: Dict[str, Any], selected_summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_burden_pressure_resolved_group_ledger_v0",
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "resolved_group_entry": {
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "resolution_status": "BURDEN_PRESSURE_METADATA_REVIEWED_AND_QUEUE_RECONCILED",
            "resolution_basis": "metadata-only selected group inspection",
            "selected_group": selected_summary,
            "policy_rewrite_authorized": False,
            "row_payload_inspection_authorized": False,
            "r1000_run_executed": False,
        },
        "selected_burden_group_resolved_count": 1,
        "selected_burden_row_count": selected_summary["row_count"],
    }

def build_updated_remaining_groups(updated_groups: List[Dict[str, Any]], selected_summary: Dict[str, Any], counts: Dict[str, int]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_remaining_pressure_groups_after_selected_burden_pressure_inspection_v0",
        "source_previous_remaining_groups_ref": rel(PREVIOUS_REMAINING_GROUPS_PATH),
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "removed_selected_group": selected_summary,
        "remaining_groups": updated_groups,
        "remaining_open_group_count": max(counts["previous_remaining_open_group_count"] - 1, 0),
        "remaining_open_row_count": max(counts["previous_remaining_open_row_count"] - selected_summary["row_count"], 0),
        "selected_group_removed_from_open_queue": True,
        "next_group_auto_opened": False,
    }

def build_next_candidate(updated_groups: List[Dict[str, Any]], updated_remaining: Dict[str, Any]) -> Dict[str, Any]:
    if updated_groups:
        candidate_summary = normalize_group(updated_groups[0])
        candidate_status = "CANDIDATE_ONLY_NOT_OPENED"
    else:
        candidate_summary = None
        candidate_status = "NO_REMAINING_GROUP_CANDIDATE"

    return {
        "schema_version": "r1000_next_selectable_group_candidate_after_selected_burden_pressure_inspection_v0",
        "source_updated_remaining_groups_ref": rel(UPDATED_REMAINING_GROUPS_PATH),
        "selection_status": candidate_status,
        "candidate_summary": candidate_summary,
        "remaining_open_group_count": updated_remaining["remaining_open_group_count"],
        "remaining_open_row_count": updated_remaining["remaining_open_row_count"],
        "next_group_opened": False,
        "not_authorized": [
            "open candidate group",
            "inspect candidate group rows",
            "run R1000",
            "repair candidate group",
        ],
    }

def build_burden_queue_decision(selected_summary: Dict[str, Any], next_candidate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_burden_pressure_queue_reconciliation_decision_v0",
        "decision_status": "SELECTED_BURDEN_PRESSURE_GROUP_RECONCILED",
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_group": selected_summary,
        "selected_group_queue_resolution": "METADATA_REVIEWED_CLOSED_FOR_QUEUE",
        "burden_policy_rewrite_authorized": False,
        "row_payload_inspection_authorized": False,
        "queue_reconciled": True,
        "next_group_candidate_emitted": next_candidate["selection_status"] == "CANDIDATE_ONLY_NOT_OPENED",
        "next_group_opened": False,
        "recommended_next_handling": "SELECT_NEXT_R1000_PRESSURE_GROUP_AFTER_BURDEN_PRESSURE_RECONCILIATION_V0" if next_candidate["selection_status"] == "CANDIDATE_ONLY_NOT_OPENED" else "STOP_R1000_PRESSURE_QUEUE_EMPTY_OR_NO_SELECTABLE_GROUP_V0",
    }

def build_queue_reconciliation(counts: Dict[str, int], selected_summary: Dict[str, Any], updated_remaining: Dict[str, Any], next_candidate: Dict[str, Any]) -> Dict[str, Any]:
    selected_rows = selected_summary["row_count"]
    return {
        "schema_version": "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0",
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_previous_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "reconciliation_status": "QUEUE_RECONCILED_AFTER_SELECTED_BURDEN_PRESSURE_GROUP_INSPECTION",
        "selected_group_resolution": "BURDEN_PRESSURE_METADATA_REVIEWED",
        "selected_group": selected_summary,
        "total_group_count": counts["total_group_count"],
        "total_pressure_row_count": counts["total_pressure_row_count"],
        "previous_resolved_group_count": counts["previous_resolved_group_count"],
        "previous_resolved_row_count": counts["previous_resolved_row_count"],
        "previous_remaining_open_group_count": counts["previous_remaining_open_group_count"],
        "previous_remaining_open_row_count": counts["previous_remaining_open_row_count"],
        "resolved_group_count": counts["previous_resolved_group_count"] + 1,
        "resolved_row_count": counts["previous_resolved_row_count"] + selected_rows,
        "remaining_open_group_count": updated_remaining["remaining_open_group_count"],
        "remaining_open_row_count": updated_remaining["remaining_open_row_count"],
        "resolved_group_count_delta": 1,
        "resolved_row_count_delta": selected_rows,
        "remaining_group_count_delta": -1,
        "remaining_row_count_delta": -selected_rows,
        "next_selectable_group_candidate_status": next_candidate["selection_status"],
        "next_selectable_group_candidate_summary": next_candidate["candidate_summary"],
        "queue_reconciled": True,
        "next_group_opened": False,
        "r1000_run_executed": False,
    }

def build_state_records(counts: Dict[str, int], selected_summary: Dict[str, Any], updated_remaining: Dict[str, Any], next_candidate: Dict[str, Any]) -> List[Dict[str, Any]]:
    selected_rows = selected_summary["row_count"]
    return [
        {
            "record_type": "QUEUE_STATE_BEFORE_SELECTED_BURDEN_PRESSURE_RECONCILIATION",
            "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
            **counts,
        },
        {
            "record_type": "SELECTED_BURDEN_PRESSURE_GROUP_RECONCILED",
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "selected_group": selected_summary,
            "resolved_group_delta": 1,
            "resolved_row_delta": selected_rows,
            "policy_rewrite_authorized": False,
            "row_payload_inspection_authorized": False,
        },
        {
            "record_type": "QUEUE_STATE_AFTER_SELECTED_BURDEN_PRESSURE_RECONCILIATION",
            "total_group_count": counts["total_group_count"],
            "total_pressure_row_count": counts["total_pressure_row_count"],
            "resolved_group_count": counts["previous_resolved_group_count"] + 1,
            "resolved_row_count": counts["previous_resolved_row_count"] + selected_rows,
            "remaining_open_group_count": updated_remaining["remaining_open_group_count"],
            "remaining_open_row_count": updated_remaining["remaining_open_row_count"],
            "next_group_candidate_status": next_candidate["selection_status"],
            "next_group_opened": False,
        },
    ]

def build_transition_trace(next_candidate: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_queue_reconciliation_after_selected_burden_pressure_inspection_transition_trace_v0",
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "trace": [
            {
                "step": "consume_selected_burden_inspection",
                "question": "selected burden pressure inspection completed",
                "answer": True,
                "taken": "mark_selected_group_metadata_reviewed",
            },
            {
                "step": "mark_selected_group_metadata_reviewed",
                "question": "selected group requires policy rewrite here",
                "answer": False,
                "taken": "update_queue_counts",
            },
            {
                "step": "update_queue_counts",
                "question": "open next group in this unit",
                "answer": False,
                "taken": "emit_next_candidate_only",
            },
            {
                "step": "emit_next_candidate_only",
                "question": "hidden next command allowed",
                "answer": False,
                "taken": "STOP_QUEUE_RECONCILED_AFTER_SELECTED_BURDEN_PRESSURE_GROUP_INSPECTION_NEXT_CANDIDATE_ONLY",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_QUEUE_RECONCILED_AFTER_SELECTED_BURDEN_PRESSURE_GROUP_INSPECTION_NEXT_CANDIDATE_ONLY",
            "next_command_goal": None,
        },
    }

def build_report(counts: Dict[str, int], selected_summary: Dict[str, Any], next_candidate: Dict[str, Any]) -> Dict[str, Any]:
    selected_rows = selected_summary["row_count"]
    return {
        "schema_version": "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_inspection_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": selected_summary["parent_pressure_class"],
        "selected_pressure_subtype": selected_summary["pressure_subtype"],
        "selected_halt_reason": selected_summary["halt_reason"],
        "selected_row_count": selected_rows,
        "inspection_queue_return_packet_consumed_count": 1,
        "queue_reconciled_count": 1,
        "selected_burden_group_reconciled_count": 1,
        "selected_burden_group_marked_metadata_reviewed_count": 1,
        "resolved_group_count_delta": 1,
        "resolved_row_count_delta": selected_rows,
        "remaining_group_count_delta": -1,
        "remaining_row_count_delta": -selected_rows,
        "total_group_count": counts["total_group_count"],
        "total_pressure_row_count": counts["total_pressure_row_count"],
        "resolved_group_count": counts["previous_resolved_group_count"] + 1,
        "resolved_row_count": counts["previous_resolved_row_count"] + selected_rows,
        "remaining_open_group_count": max(counts["previous_remaining_open_group_count"] - 1, 0),
        "remaining_open_row_count": max(counts["previous_remaining_open_row_count"] - selected_rows, 0),
        "next_group_candidate_emitted_count": 1 if next_candidate["selection_status"] == "CANDIDATE_ONLY_NOT_OPENED" else 0,
        "next_group_auto_opened_count": 0,
        "next_group_inspected_count": 0,
        "row_payload_materialized_count": 0,
        "row_payload_inspected_count": 0,
        "burden_policy_rewrite_count": 0,
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
        "recommended_next_handling": "SELECT_NEXT_R1000_PRESSURE_GROUP_AFTER_BURDEN_PRESSURE_RECONCILIATION_V0" if next_candidate["selection_status"] == "CANDIDATE_ONLY_NOT_OPENED" else "STOP_R1000_PRESSURE_QUEUE_EMPTY_OR_NO_SELECTABLE_GROUP_V0",
    }

def validate_outputs(
    reconciliation: Dict[str, Any],
    ledger: Dict[str, Any],
    updated_remaining: Dict[str, Any],
    next_candidate: Dict[str, Any],
    decision: Dict[str, Any],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if reconciliation.get("reconciliation_status") != "QUEUE_RECONCILED_AFTER_SELECTED_BURDEN_PRESSURE_GROUP_INSPECTION":
        failures.append("reconciliation_status_wrong")
    if reconciliation.get("queue_reconciled") is not True:
        failures.append("queue_not_reconciled")
    if reconciliation.get("next_group_opened") is not False:
        failures.append("next_group_opened")
    if reconciliation.get("r1000_run_executed") is not False:
        failures.append("r1000_run_executed")
    if ledger.get("selected_burden_group_resolved_count") != 1:
        failures.append("selected_burden_group_resolved_count_wrong")
    if updated_remaining.get("selected_group_removed_from_open_queue") is not True:
        failures.append("selected_group_not_removed_from_open_queue")
    if decision.get("burden_policy_rewrite_authorized") is not False:
        failures.append("burden_policy_rewrite_authorized")
    if decision.get("row_payload_inspection_authorized") is not False:
        failures.append("row_payload_inspection_authorized")
    if decision.get("next_group_opened") is not False:
        failures.append("decision_opened_next_group")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "next_group_auto_opened_count",
        "next_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "burden_policy_rewrite_count",
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

    if report.get("queue_reconciled_count") != 1:
        failures.append("queue_reconciled_count_wrong")
    if report.get("selected_burden_group_reconciled_count") != 1:
        failures.append("selected_burden_reconciled_count_wrong")
    if report.get("resolved_group_count_delta") != 1:
        failures.append("resolved_group_delta_wrong")
    if report.get("remaining_group_count_delta") != -1:
        failures.append("remaining_group_delta_wrong")

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
    if metrics.get("queue_reconciled_count") != 1:
        failures.append("metric_queue_reconciled_wrong")
    if metrics.get("selected_burden_group_reconciled_count") != 1:
        failures.append("metric_selected_burden_reconciled_wrong")
    if metrics.get("next_group_auto_opened_count") != 0:
        failures.append("metric_next_group_opened")

    for key in [
        "next_group_auto_opened_count",
        "next_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
        "burden_policy_rewrite_count",
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
    if terminal.get("stop_code") != "STOP_QUEUE_RECONCILED_AFTER_SELECTED_BURDEN_PRESSURE_GROUP_INSPECTION_NEXT_CANDIDATE_ONLY":
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

    counts = previous_counts(sources)
    selected_summary = selected_summary_from_sources(sources)
    updated_groups, removed_records, removed_from_prior_list = update_remaining_groups(sources, selected_summary)

    updated_remaining = build_updated_remaining_groups(updated_groups, selected_summary, counts)
    next_candidate = build_next_candidate(updated_groups, updated_remaining)
    ledger = build_resolved_burden_ledger(sources, selected_summary)
    decision = build_burden_queue_decision(selected_summary, next_candidate)
    reconciliation = build_queue_reconciliation(counts, selected_summary, updated_remaining, next_candidate)
    state_records = build_state_records(counts, selected_summary, updated_remaining, next_candidate)
    trace = build_transition_trace(next_candidate)
    report = build_report(counts, selected_summary, next_candidate)

    write_json(QUEUE_RECONCILIATION_PATH, reconciliation)
    write_json(RESOLVED_BURDEN_LEDGER_PATH, ledger)
    write_json(UPDATED_REMAINING_GROUPS_PATH, updated_remaining)
    write_jsonl(QUEUE_STATE_RECORDS_PATH, state_records)
    write_json(NEXT_SELECTABLE_GROUP_CANDIDATE_PATH, next_candidate)
    write_json(BURDEN_QUEUE_DECISION_PATH, decision)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(
        reconciliation,
        ledger,
        updated_remaining,
        next_candidate,
        decision,
        trace,
        report,
    ))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "BURDEN_QUEUE_0_SELECTED_GROUP_INSPECTION_CONSUMED": sources["inspection_receipt"]["receipt_id"] == SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID and sources["inspection_receipt"]["gate"] == "PASS",
        "BURDEN_QUEUE_1_QUEUE_RETURN_PACKET_CONSUMED": sources["inspection_queue_return"]["packet_status"] == "CANDIDATE_ONLY_NOT_EXECUTED",
        "BURDEN_QUEUE_2_PREVIOUS_QUEUE_CONSUMED": sources["previous_queue_receipt"]["receipt_id"] == SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID and sources["previous_queue_receipt"]["gate"] == "PASS",
        "BURDEN_QUEUE_3_SELECTED_BURDEN_GROUP_RECONCILED": report["selected_burden_group_reconciled_count"] == 1,
        "BURDEN_QUEUE_4_QUEUE_RECONCILED": report["queue_reconciled_count"] == 1,
        "BURDEN_QUEUE_5_COUNTS_UPDATED_BY_SELECTED_GROUP_ONLY": report["resolved_group_count_delta"] == 1 and report["remaining_group_count_delta"] == -1 and report["resolved_row_count_delta"] == selected_summary["row_count"],
        "BURDEN_QUEUE_6_NEXT_CANDIDATE_EMITTED_ONLY": report["next_group_auto_opened_count"] == 0 and next_candidate["next_group_opened"] is False,
        "BURDEN_QUEUE_7_NO_ROW_PAYLOAD_OR_POLICY_REWRITE": report["row_payload_inspected_count"] == 0 and report["burden_policy_rewrite_count"] == 0,
        "BURDEN_QUEUE_8_NO_R1000_RUN_OR_REPAIR": report["r1000_run_executed_count"] == 0 and report["repair_executed_count"] == 0,
        "BURDEN_QUEUE_9_NO_FIELD_VALUE_OR_TAXONOMY_ACTION": report["target_field_filled_count"] == 0 and report["descriptor_value_assignment_count"] == 0 and report["field_value_invention_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "BURDEN_QUEUE_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "BURDEN_QUEUE_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_QUEUE_RECONCILED_AFTER_SELECTED_BURDEN_PRESSURE_GROUP_INSPECTION_NEXT_CANDIDATE_ONLY",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        }

    aggregate_metrics = {
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
        "source_prior_queue_reconciliation_receipt_id": SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": selected_summary["parent_pressure_class"],
        "selected_pressure_subtype": selected_summary["pressure_subtype"],
        "selected_halt_reason": selected_summary["halt_reason"],
        "selected_row_count": selected_summary["row_count"],
        "inspection_queue_return_packet_consumed_count": 1,
        "queue_reconciled_count": 1,
        "selected_burden_group_reconciled_count": 1,
        "selected_burden_group_marked_metadata_reviewed_count": 1,
        "selected_group_removed_from_prior_remaining_list_count": 1 if removed_from_prior_list else 0,
        "resolved_group_count_delta": report["resolved_group_count_delta"],
        "resolved_row_count_delta": report["resolved_row_count_delta"],
        "remaining_group_count_delta": report["remaining_group_count_delta"],
        "remaining_row_count_delta": report["remaining_row_count_delta"],
        "total_group_count": report["total_group_count"],
        "total_pressure_row_count": report["total_pressure_row_count"],
        "resolved_group_count": report["resolved_group_count"],
        "resolved_row_count": report["resolved_row_count"],
        "remaining_open_group_count": report["remaining_open_group_count"],
        "remaining_open_row_count": report["remaining_open_row_count"],
        "next_group_candidate_emitted_count": report["next_group_candidate_emitted_count"],
        "next_group_auto_opened_count": 0,
        "next_group_inspected_count": 0,
        "row_payload_materialized_count": 0,
        "row_payload_inspected_count": 0,
        "burden_policy_rewrite_count": 0,
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
        "selected_group_inspection_consumed": True,
        "queue_return_packet_consumed": True,
        "previous_queue_consumed": True,
        "selected_burden_group_reconciled": True,
        "selected_burden_group_marked_metadata_reviewed": True,
        "queue_reconciled": True,
        "counts_updated_by_selected_group_only": True,
        "next_group_candidate_emitted": next_candidate["selection_status"] == "CANDIDATE_ONLY_NOT_OPENED",
        "next_group_opened": False,
        "next_group_inspected": False,
        "row_payload_materialized": False,
        "row_payload_inspected": False,
        "burden_policy_rewrite": False,
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
        "source_selected_group_inspection_receipt": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "queue_reconciliation": rel(QUEUE_RECONCILIATION_PATH),
        "resolved_burden_group_ledger": rel(RESOLVED_BURDEN_LEDGER_PATH),
        "updated_remaining_groups": rel(UPDATED_REMAINING_GROUPS_PATH),
        "queue_state_records": rel(QUEUE_STATE_RECORDS_PATH),
        "next_selectable_group_candidate": rel(NEXT_SELECTABLE_GROUP_CANDIDATE_PATH),
        "burden_queue_decision": rel(BURDEN_QUEUE_DECISION_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_receipt_v0",
        "receipt_type": "R1000_PRESSURE_QUEUE_RECONCILIATION_AFTER_SELECTED_BURDEN_PRESSURE_GROUP_INSPECTION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_selected_group_inspection_receipt_id": SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_queue_reconciliation_receipt_id": SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID,
        "source_derived_surface_review_receipt_id": SOURCE_DERIVED_SURFACE_REVIEW_RECEIPT_ID,
        "source_accepted_application_receipt_id": SOURCE_ACCEPTED_APP_RECEIPT_ID,
        "source_prior_queue_reconciliation_receipt_id": SOURCE_PRIOR_QUEUE_RECONCILIATION_RECEIPT_ID,
        "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "selected_burden_pressure_queue_reconciliation_summary": {
            "queue_reconciliation_status": "QUEUE_RECONCILED_AFTER_SELECTED_BURDEN_PRESSURE_GROUP_INSPECTION",
            "selected_pressure_group_id": SELECTED_PRESSURE_GROUP_ID,
            "selected_group": selected_summary,
            "selected_burden_group_reconciled": True,
            "selected_burden_group_marked_metadata_reviewed": True,
            "resolved_group_count": report["resolved_group_count"],
            "resolved_row_count": report["resolved_row_count"],
            "remaining_open_group_count": report["remaining_open_group_count"],
            "remaining_open_row_count": report["remaining_open_row_count"],
            "next_group_candidate_emitted": next_candidate["selection_status"] == "CANDIDATE_ONLY_NOT_OPENED",
            "next_group_opened": False,
            "burden_policy_rewrite": False,
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "selected_burden_pressure_queue_reconciliation_guards": guards,
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
    print(f"selected_burden_queue_reconciliation_receipt_id={receipt_id}")
    print(f"selected_burden_queue_reconciliation_receipt_path=data/r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0_receipts/{receipt_id}.json")
    print(f"selected_burden_next_candidate_path=data/r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0/r1000_next_selectable_group_candidate_after_selected_burden_pressure_inspection.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
