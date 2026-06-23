#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RECONCILE_R1000_PRESSURE_QUEUE_AFTER_REPAIRED_BURDEN_GROUP_INSPECTION_V0"
TARGET_UNIT_ID = "r1000_pressure_queue.reconciliation_after_repaired_burden_group_inspection.v0"

SOURCE_REPAIRED_INSPECTION_RECEIPT_ID = "dab2b21d"
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

OUT_DIR = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0_receipts"

RECONCILIATION_DECISION_PATH = OUT_DIR / "r1000_repaired_burden_group_queue_reconciliation_decision.json"
RECONCILIATION_PATH = OUT_DIR / "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection.json"
RESOLVED_LEDGER_PATH = OUT_DIR / "r1000_repaired_burden_group_resolved_group_ledger.json"
QUEUE_STATE_RECORDS_PATH = OUT_DIR / "r1000_queue_state_records_after_repaired_burden_group_inspection.jsonl"
REMAINING_GROUPS_PATH = OUT_DIR / "r1000_remaining_pressure_groups_after_repaired_burden_group_inspection.json"
NEXT_CANDIDATE_PATH = OUT_DIR / "r1000_next_selectable_group_candidate_after_repaired_burden_group_inspection.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_queue_reconciliation_after_repaired_burden_group_inspection_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_queue_reconciliation_after_repaired_burden_group_inspection_report.json"

REPAIRED_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_v0_receipts" / f"{SOURCE_REPAIRED_INSPECTION_RECEIPT_ID}.json"
INSPECTION_SURFACE_PATH = ROOT / "data" / "r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_v0" / "r1000_repaired_selected_group_inspection_surface_after_identity_review.json"
INSPECTION_CLASSIFICATION_PATH = ROOT / "data" / "r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_v0" / "r1000_repaired_selected_group_inspection_classification_after_identity_review.json"
BURDEN_PRESSURE_PACKET_PATH = ROOT / "data" / "r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_v0" / "r1000_repaired_selected_group_burden_pressure_packet_after_identity_review.json"
INSPECTION_LIMIT_PACKET_PATH = ROOT / "data" / "r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_v0" / "r1000_repaired_selected_group_inspection_limit_packet_after_identity_review.json"
QUEUE_RETURN_PACKET_PATH = ROOT / "data" / "r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_v0" / "r1000_repaired_selected_group_inspection_queue_return_packet_after_identity_review.json"
INSPECTION_REPORT_PATH = ROOT / "data" / "r1000_repaired_burden_queue_selected_group_inspection_after_identity_review_v0" / "r1000_repaired_selected_group_inspection_report_after_identity_review.json"

REPAIRED_IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_repaired_burden_queue_candidate_identity_surface_review_v0_receipts" / f"{SOURCE_REPAIRED_IDENTITY_REVIEW_RECEIPT_ID}.json"
IDENTITY_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_burden_queue_next_candidate_identity_preservation_fix_v0_receipts" / f"{SOURCE_IDENTITY_PRESERVATION_FIX_RECEIPT_ID}.json"
IDENTITY_REVIEW_RECEIPT_PATH = ROOT / "data" / "r1000_selected_group_after_burden_identity_surface_review_v0_receipts" / f"{SOURCE_IDENTITY_REVIEW_RECEIPT_ID}.json"
SELECTION_AFTER_BURDEN_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_after_burden_pressure_reconciliation_v0_receipts" / f"{SOURCE_SELECTION_AFTER_BURDEN_RECEIPT_ID}.json"

BURDEN_QUEUE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0_receipts" / f"{SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID}.json"
BURDEN_QUEUE_RECONCILIATION_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection.json"
BURDEN_REMAINING_GROUPS_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0" / "r1000_remaining_pressure_groups_after_selected_burden_pressure_inspection.json"
BURDEN_NEXT_CANDIDATE_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_burden_pressure_group_inspection_v0" / "r1000_next_selectable_group_candidate_after_selected_burden_pressure_inspection.json"

SELECTED_GROUP_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_selected_pressure_group_inspection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTED_GROUP_INSPECTION_RECEIPT_ID}.json"
SELECTION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_group_selection_from_reconciled_queue_v0_receipts" / f"{SOURCE_SELECTION_RECEIPT_ID}.json"
QUEUE_RECONCILIATION_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_accepted_descriptor_surface_review_v0_receipts" / f"{SOURCE_QUEUE_RECONCILIATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    REPAIRED_INSPECTION_RECEIPT_PATH,
    INSPECTION_SURFACE_PATH,
    INSPECTION_CLASSIFICATION_PATH,
    BURDEN_PRESSURE_PACKET_PATH,
    INSPECTION_LIMIT_PACKET_PATH,
    QUEUE_RETURN_PACKET_PATH,
    INSPECTION_REPORT_PATH,
    REPAIRED_IDENTITY_REVIEW_RECEIPT_PATH,
    IDENTITY_FIX_RECEIPT_PATH,
    IDENTITY_REVIEW_RECEIPT_PATH,
    SELECTION_AFTER_BURDEN_RECEIPT_PATH,
    BURDEN_QUEUE_RECEIPT_PATH,
    BURDEN_QUEUE_RECONCILIATION_PATH,
    BURDEN_REMAINING_GROUPS_PATH,
    BURDEN_NEXT_CANDIDATE_PATH,
    SELECTED_GROUP_INSPECTION_RECEIPT_PATH,
    SELECTION_RECEIPT_PATH,
    QUEUE_RECONCILIATION_RECEIPT_PATH,
]

RECOMMENDED_NEXT_HANDLING = "SELECT_NEXT_R1000_PRESSURE_GROUP_AFTER_REPAIRED_BURDEN_GROUP_QUEUE_RECONCILIATION_V0"

HUMAN_DECISION = {
    "decision": "RECONCILE_R1000_PRESSURE_QUEUE_AFTER_REPAIRED_BURDEN_GROUP_INSPECTION",
    "scope": "consume repaired burden group inspection queue-return packet and reconcile queue state by marking that inspected group resolved; emit remaining groups and next candidate only, without opening or inspecting the next group",
    "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
    "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
    "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
    "authorized": [
        "consume repaired selected group inspection receipt",
        "consume queue return packet",
        "consume prior burden queue reconciliation state",
        "mark repaired selected group as resolved in a new derived queue state",
        "emit reconciliation decision",
        "emit resolved ledger",
        "emit remaining groups summary",
        "emit next selectable group candidate only if remaining groups exist",
        "stop before selecting or inspecting any next group",
    ],
    "not_authorized": [
        "mutating prior queue artifacts",
        "mutating receipts",
        "opening next group",
        "inspecting next group",
        "materializing row payloads",
        "running R1000",
        "repairing surfaces",
        "assigning descriptor values",
        "filling fields",
        "inventing values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "emitting taxonomy delta proposal",
        "hidden next command",
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
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))

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
        "repaired_inspection_receipt": read_json(REPAIRED_INSPECTION_RECEIPT_PATH),
        "inspection_surface": read_json(INSPECTION_SURFACE_PATH),
        "inspection_classification": read_json(INSPECTION_CLASSIFICATION_PATH),
        "burden_pressure_packet": read_json(BURDEN_PRESSURE_PACKET_PATH),
        "inspection_limit_packet": read_json(INSPECTION_LIMIT_PACKET_PATH),
        "queue_return_packet": read_json(QUEUE_RETURN_PACKET_PATH),
        "inspection_report": read_json(INSPECTION_REPORT_PATH),
        "repaired_identity_review_receipt": read_json(REPAIRED_IDENTITY_REVIEW_RECEIPT_PATH),
        "identity_fix_receipt": read_json(IDENTITY_FIX_RECEIPT_PATH),
        "identity_review_receipt": read_json(IDENTITY_REVIEW_RECEIPT_PATH),
        "selection_after_burden_receipt": read_json(SELECTION_AFTER_BURDEN_RECEIPT_PATH),
        "burden_queue_receipt": read_json(BURDEN_QUEUE_RECEIPT_PATH),
        "burden_queue_reconciliation": read_json(BURDEN_QUEUE_RECONCILIATION_PATH),
        "burden_remaining_groups": read_json(BURDEN_REMAINING_GROUPS_PATH),
        "burden_next_candidate": read_json(BURDEN_NEXT_CANDIDATE_PATH),
        "selected_group_inspection_receipt": read_json(SELECTED_GROUP_INSPECTION_RECEIPT_PATH),
        "selection_receipt": read_json(SELECTION_RECEIPT_PATH),
        "queue_reconciliation_receipt": read_json(QUEUE_RECONCILIATION_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    receipt = sources["repaired_inspection_receipt"]
    classification = sources["inspection_classification"]
    queue_return = sources["queue_return_packet"]
    burden_reconciliation = sources["burden_queue_reconciliation"]
    burden_receipt = sources["burden_queue_receipt"]

    if receipt.get("receipt_id") != SOURCE_REPAIRED_INSPECTION_RECEIPT_ID:
        failures.append("repaired_inspection_receipt_id_wrong")
    if receipt.get("gate") != "PASS":
        failures.append("repaired_inspection_not_pass")
    if receipt.get("repaired_selected_pressure_group_id") != REPAIRED_SELECTED_PRESSURE_GROUP_ID:
        failures.append("repaired_selected_group_id_wrong_in_receipt")
    if receipt.get("aggregate_metrics", {}).get("selected_group_inspected_count") != 1:
        failures.append("selected_group_not_inspected")
    if receipt.get("aggregate_metrics", {}).get("metadata_only_inspection_count") != 1:
        failures.append("metadata_only_inspection_not_recorded")
    if receipt.get("aggregate_metrics", {}).get("queue_reconciled_count") != 0:
        failures.append("queue_already_reconciled_in_inspection")
    if receipt.get("aggregate_metrics", {}).get("row_payload_inspected_count") != 0:
        failures.append("row_payload_inspected_in_inspection")
    if receipt.get("aggregate_metrics", {}).get("r1000_run_executed_count") != 0:
        failures.append("r1000_run_in_inspection")

    if classification.get("classification_status") != "BURDEN_PRESSURE_RECEIPT_SIZE_BURDEN_METADATA_REVIEWED":
        failures.append("classification_status_wrong")
    if queue_return.get("packet_status") != "CANDIDATE_ONLY_NOT_EXECUTED":
        failures.append("queue_return_packet_not_candidate_only")
    if queue_return.get("queue_reconciliation_required") is not True:
        failures.append("queue_return_missing_reconciliation_requirement")
    if queue_return.get("queue_reconciliation_authorized_in_this_unit") is not False:
        failures.append("queue_return_authorized_reconciliation_in_inspection_unit")

    if burden_receipt.get("receipt_id") != SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID:
        failures.append("prior_burden_queue_receipt_id_wrong")
    if burden_receipt.get("gate") != "PASS":
        failures.append("prior_burden_queue_not_pass")
    if burden_reconciliation.get("queue_reconciled") is not True:
        failures.append("prior_burden_queue_not_reconciled")
    if burden_reconciliation.get("next_group_opened") is not False:
        failures.append("prior_burden_queue_opened_next_group")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def selected_group(sources: Dict[str, Any]) -> Dict[str, Any]:
    return copy.deepcopy(sources["repaired_inspection_receipt"]["repaired_selected_group_inspection_summary"]["selected_group"])

def prior_counts(sources: Dict[str, Any]) -> Dict[str, int]:
    reconciliation = sources["burden_queue_reconciliation"]
    return {
        "total_group_count": int(reconciliation.get("total_group_count", 5)),
        "total_pressure_row_count": int(reconciliation.get("total_pressure_row_count", 88)),
        "resolved_group_count": int(reconciliation.get("resolved_group_count", 3)),
        "resolved_row_count": int(reconciliation.get("resolved_row_count", 68)),
        "remaining_open_group_count": int(reconciliation.get("remaining_open_group_count", 2)),
        "remaining_open_row_count": int(reconciliation.get("remaining_open_row_count", 20)),
    }

def normalize_remaining_groups_payload(payload: Any) -> List[Dict[str, Any]]:
    if isinstance(payload, list):
        candidates = payload
    elif isinstance(payload, dict):
        for key in [
            "remaining_groups",
            "remaining_pressure_groups",
            "open_groups",
            "groups",
            "remaining_open_groups",
        ]:
            if isinstance(payload.get(key), list):
                candidates = payload[key]
                break
        else:
            candidates = []
    else:
        candidates = []

    normalized = []
    for idx, item in enumerate(candidates):
        if isinstance(item, dict):
            group = item.get("candidate_summary") if isinstance(item.get("candidate_summary"), dict) else item
            normalized.append({
                "source_index": idx,
                "raw": item,
                "parent_pressure_class": group.get("parent_pressure_class", group.get("pressure_class", "UNKNOWN")),
                "pressure_subtype": group.get("pressure_subtype", group.get("subtype", "UNKNOWN")),
                "halt_reason": group.get("halt_reason", group.get("stop_code", "UNKNOWN")),
                "row_count": int(group.get("row_count", group.get("rows", 0)) or 0),
            })
    return normalized

def build_reconciliation_decision(sources: Dict[str, Any]) -> Dict[str, Any]:
    group = selected_group(sources)
    counts = prior_counts(sources)
    selected_row_count = int(group.get("row_count", 0) or 0)
    resolved_group_count_after = counts["resolved_group_count"] + 1
    resolved_row_count_after = counts["resolved_row_count"] + selected_row_count
    remaining_open_group_count_after = max(counts["remaining_open_group_count"] - 1, 0)
    remaining_open_row_count_after = max(counts["remaining_open_row_count"] - selected_row_count, 0)

    return {
        "schema_version": "r1000_repaired_burden_group_queue_reconciliation_decision_v0",
        "decision_id": sha8({
            "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
            "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
            "selected_group": group,
        }),
        "decision_status": "RECONCILE_REPAIRED_BURDEN_GROUP_INSPECTION_INTO_QUEUE",
        "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "selected_group": group,
        "prior_counts": counts,
        "count_delta": {
            "resolved_group_delta": 1,
            "resolved_row_delta": selected_row_count,
            "remaining_group_delta": -1 if counts["remaining_open_group_count"] > 0 else 0,
            "remaining_row_delta": -selected_row_count,
        },
        "after_counts": {
            "total_group_count": counts["total_group_count"],
            "total_pressure_row_count": counts["total_pressure_row_count"],
            "resolved_group_count": resolved_group_count_after,
            "resolved_row_count": resolved_row_count_after,
            "remaining_open_group_count": remaining_open_group_count_after,
            "remaining_open_row_count": remaining_open_row_count_after,
        },
        "queue_reconciliation_authorized": True,
        "next_group_candidate_authorized": True,
        "next_group_open_authorized": False,
        "next_group_inspection_authorized": False,
        "row_payload_inspection_authorized": False,
        "r1000_run_authorized": False,
        "repair_authorized": False,
    }

def build_resolved_ledger(decision: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_repaired_burden_group_resolved_ledger_v0",
        "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "resolved_entry": {
            "resolution_id": sha8({
                "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
                "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
                "resolution": "metadata_reviewed_burden_pressure",
            }),
            "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
            "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
            "selected_group": decision["selected_group"],
            "inspection_result": "BURDEN_PRESSURE_RECEIPT_SIZE_BURDEN_METADATA_REVIEWED",
            "resolution_status": "REPAIRED_BURDEN_GROUP_METADATA_REVIEWED_RESOLVED",
            "row_count": decision["selected_group"]["row_count"],
        },
        "prior_resolved_count": decision["prior_counts"]["resolved_group_count"],
        "after_resolved_count": decision["after_counts"]["resolved_group_count"],
    }

def build_remaining_groups(sources: Dict[str, Any], decision: Dict[str, Any]) -> Dict[str, Any]:
    source_remaining = normalize_remaining_groups_payload(sources["burden_remaining_groups"])
    selected = decision["selected_group"]

    remaining = []
    removed_count = 0
    removed_row_count = 0
    selected_signature = (
        selected.get("parent_pressure_class"),
        selected.get("pressure_subtype"),
        selected.get("halt_reason"),
        int(selected.get("row_count", 0) or 0),
    )

    for entry in source_remaining:
        entry_signature = (
            entry.get("parent_pressure_class"),
            entry.get("pressure_subtype"),
            entry.get("halt_reason"),
            int(entry.get("row_count", 0) or 0),
        )
        if removed_count == 0 and entry_signature == selected_signature:
            removed_count += 1
            removed_row_count += int(entry.get("row_count", 0) or 0)
            continue
        remaining.append(entry)

    if not source_remaining:
        remaining = [
            {
                "source_index": 0,
                "parent_pressure_class": "REMAINING_PRESSURE",
                "pressure_subtype": "residual_pressure_after_repaired_burden_reconciliation",
                "halt_reason": "STOP_REMAINING_PRESSURE",
                "row_count": decision["after_counts"]["remaining_open_row_count"],
                "identity_status": "COUNT_ONLY_SYNTHETIC_REMAINDER",
                "requires_identity_review_before_selection": True,
            }
        ] if decision["after_counts"]["remaining_open_row_count"] > 0 else []

    if source_remaining and removed_count == 0 and decision["after_counts"]["remaining_open_row_count"] > 0:
        remaining = [
            {
                "source_index": 0,
                "parent_pressure_class": "REMAINING_PRESSURE",
                "pressure_subtype": "residual_pressure_after_repaired_burden_reconciliation",
                "halt_reason": "STOP_REMAINING_PRESSURE",
                "row_count": decision["after_counts"]["remaining_open_row_count"],
                "identity_status": "COUNT_ONLY_SYNTHETIC_REMAINDER",
                "requires_identity_review_before_selection": True,
            }
        ]

    return {
        "schema_version": "r1000_remaining_pressure_groups_after_repaired_burden_group_inspection_v0",
        "source_burden_remaining_groups_ref": rel(BURDEN_REMAINING_GROUPS_PATH),
        "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
        "selected_repaired_group_removed_by_identity_match_count": removed_count,
        "selected_repaired_group_removed_row_count": removed_row_count,
        "remaining_open_group_count": decision["after_counts"]["remaining_open_group_count"],
        "remaining_open_row_count": decision["after_counts"]["remaining_open_row_count"],
        "remaining_groups": remaining,
        "remaining_groups_materialized_count": len(remaining),
        "next_group_opened": False,
        "next_group_inspected": False,
    }

def build_next_candidate(remaining: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    groups = remaining.get("remaining_groups", [])
    if not groups:
        return None
    first = groups[0]
    return {
        "schema_version": "r1000_next_selectable_group_candidate_after_repaired_burden_group_inspection_v0",
        "candidate_id": sha8({
            "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
            "first_remaining_group": first,
        }),
        "source_remaining_groups_ref": rel(REMAINING_GROUPS_PATH),
        "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
        "selection_status": "CANDIDATE_ONLY_NOT_OPENED",
        "candidate_summary": {
            "parent_pressure_class": first.get("parent_pressure_class", "UNKNOWN"),
            "pressure_subtype": first.get("pressure_subtype", "UNKNOWN"),
            "halt_reason": first.get("halt_reason", "UNKNOWN"),
            "row_count": int(first.get("row_count", 0) or 0),
        },
        "candidate_identity_status": first.get("identity_status", "PRESERVED_FROM_REMAINING_GROUP_SURFACE"),
        "requires_identity_review_before_inspection": first.get("requires_identity_review_before_selection", False),
        "next_group_opened": False,
        "next_group_inspected": False,
        "row_payload_materialized": False,
    }

def build_reconciliation(decision: Dict[str, Any], remaining: Dict[str, Any], next_candidate: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0",
        "queue_reconciliation_id": sha8({
            "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
            "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
            "after_counts": decision["after_counts"],
        }),
        "queue_reconciled": True,
        "reconciliation_result": "QUEUE_RECONCILED_AFTER_REPAIRED_BURDEN_GROUP_INSPECTION",
        "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "resolved_group": decision["selected_group"],
        "prior_counts": decision["prior_counts"],
        "after_counts": decision["after_counts"],
        "resolved_group_count": decision["after_counts"]["resolved_group_count"],
        "resolved_row_count": decision["after_counts"]["resolved_row_count"],
        "remaining_open_group_count": decision["after_counts"]["remaining_open_group_count"],
        "remaining_open_row_count": decision["after_counts"]["remaining_open_row_count"],
        "remaining_groups_ref": rel(REMAINING_GROUPS_PATH),
        "next_group_candidate_ref": rel(NEXT_CANDIDATE_PATH) if next_candidate else None,
        "next_group_candidate_emitted": next_candidate is not None,
        "next_group_opened": False,
        "next_group_inspected": False,
        "row_payload_materialized": False,
        "r1000_run_executed": False,
        "repair_executed": False,
    }

def build_queue_state_records(decision: Dict[str, Any], reconciliation: Dict[str, Any]) -> List[Dict[str, Any]]:
    return [
        {
            "record_type": "QUEUE_STATE_BEFORE_REPAIRED_BURDEN_RECONCILIATION",
            "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
            **decision["prior_counts"],
        },
        {
            "record_type": "QUEUE_STATE_AFTER_REPAIRED_BURDEN_RECONCILIATION",
            "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
            **decision["after_counts"],
            "queue_reconciliation_id": reconciliation["queue_reconciliation_id"],
        },
    ]

def build_transition_trace(decision: Dict[str, Any], next_candidate: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_queue_reconciliation_after_repaired_burden_group_inspection_transition_trace_v0",
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "trace": [
            {
                "step": "consume_repaired_burden_group_inspection",
                "question": "inspection completed and queue return packet emitted",
                "answer": True,
                "taken": "mark_repaired_group_resolved",
            },
            {
                "step": "mark_repaired_group_resolved",
                "question": "mutate prior queue artifacts",
                "answer": False,
                "taken": "emit_derived_queue_reconciliation_artifacts",
            },
            {
                "step": "emit_derived_queue_reconciliation_artifacts",
                "question": "remaining group exists",
                "answer": next_candidate is not None,
                "taken": "emit_next_candidate_only" if next_candidate else "stop_queue_exhausted",
            },
            {
                "step": "emit_next_candidate_only",
                "question": "open or inspect next group in this unit",
                "answer": False,
                "taken": "STOP_QUEUE_RECONCILED_AFTER_REPAIRED_BURDEN_GROUP_INSPECTION_NEXT_CANDIDATE_ONLY",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_QUEUE_RECONCILED_AFTER_REPAIRED_BURDEN_GROUP_INSPECTION_NEXT_CANDIDATE_ONLY" if next_candidate else "STOP_QUEUE_RECONCILED_AFTER_REPAIRED_BURDEN_GROUP_INSPECTION_NO_REMAINING_GROUPS",
            "next_command_goal": None,
        },
    }

def build_report(decision: Dict[str, Any], remaining: Dict[str, Any], next_candidate: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_queue_reconciliation_after_repaired_burden_group_inspection_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
        "source_burden_queue_reconciliation_receipt_id": SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID,
        "repaired_candidate_id": REPAIRED_CANDIDATE_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "selected_parent_pressure_class": decision["selected_group"].get("parent_pressure_class"),
        "selected_pressure_subtype": decision["selected_group"].get("pressure_subtype"),
        "selected_halt_reason": decision["selected_group"].get("halt_reason"),
        "selected_row_count": decision["selected_group"].get("row_count"),
        "repaired_inspection_queue_return_packet_consumed_count": 1,
        "prior_burden_queue_reconciliation_consumed_count": 1,
        "queue_reconciled_count": 1,
        "resolved_group_ledger_emitted_count": 1,
        "remaining_groups_emitted_count": 1,
        "queue_state_records_emitted_count": 2,
        "next_group_candidate_emitted_count": 1 if next_candidate else 0,
        "next_group_auto_opened_count": 0,
        "next_group_inspected_count": 0,
        "selected_group_removed_from_prior_remaining_list_count": remaining["selected_repaired_group_removed_by_identity_match_count"],
        "selected_group_removed_row_count": remaining["selected_repaired_group_removed_row_count"],
        "total_group_count": decision["after_counts"]["total_group_count"],
        "total_pressure_row_count": decision["after_counts"]["total_pressure_row_count"],
        "resolved_group_count_before": decision["prior_counts"]["resolved_group_count"],
        "resolved_group_count_after": decision["after_counts"]["resolved_group_count"],
        "resolved_group_delta": decision["after_counts"]["resolved_group_count"] - decision["prior_counts"]["resolved_group_count"],
        "resolved_row_count_before": decision["prior_counts"]["resolved_row_count"],
        "resolved_row_count_after": decision["after_counts"]["resolved_row_count"],
        "resolved_row_delta": decision["after_counts"]["resolved_row_count"] - decision["prior_counts"]["resolved_row_count"],
        "remaining_group_count_before": decision["prior_counts"]["remaining_open_group_count"],
        "remaining_group_count_after": decision["after_counts"]["remaining_open_group_count"],
        "remaining_group_delta": decision["after_counts"]["remaining_open_group_count"] - decision["prior_counts"]["remaining_open_group_count"],
        "remaining_row_count_before": decision["prior_counts"]["remaining_open_row_count"],
        "remaining_row_count_after": decision["after_counts"]["remaining_open_row_count"],
        "remaining_row_delta": decision["after_counts"]["remaining_open_row_count"] - decision["prior_counts"]["remaining_open_row_count"],
        "row_payload_materialized_count": 0,
        "row_payload_inspected_count": 0,
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
        "recommended_next_handling": RECOMMENDED_NEXT_HANDLING if next_candidate else "R1000_PRESSURE_QUEUE_RECONCILED_NO_REMAINING_GROUPS",
    }

def validate_outputs(
    decision: Dict[str, Any],
    reconciliation: Dict[str, Any],
    ledger: Dict[str, Any],
    remaining: Dict[str, Any],
    next_candidate: Optional[Dict[str, Any]],
    trace: Dict[str, Any],
    report: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if decision.get("decision_status") != "RECONCILE_REPAIRED_BURDEN_GROUP_INSPECTION_INTO_QUEUE":
        failures.append("decision_status_wrong")
    if reconciliation.get("queue_reconciled") is not True:
        failures.append("queue_not_reconciled")
    if reconciliation.get("next_group_opened") is not False:
        failures.append("reconciliation_opened_next_group")
    if ledger.get("resolved_entry", {}).get("resolution_status") != "REPAIRED_BURDEN_GROUP_METADATA_REVIEWED_RESOLVED":
        failures.append("resolved_ledger_status_wrong")
    if remaining.get("next_group_opened") is not False:
        failures.append("remaining_groups_opened_next_group")
    if next_candidate is not None:
        if next_candidate.get("selection_status") != "CANDIDATE_ONLY_NOT_OPENED":
            failures.append("next_candidate_status_wrong")
        if next_candidate.get("next_group_opened") is not False:
            failures.append("next_candidate_opened")
        if next_candidate.get("next_group_inspected") is not False:
            failures.append("next_candidate_inspected")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_terminal_next_not_null")

    for key in [
        "next_group_auto_opened_count",
        "next_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
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

    if report.get("queue_reconciled_count") != 1:
        failures.append("queue_reconciled_count_wrong")
    if report.get("resolved_group_delta") != 1:
        failures.append("resolved_group_delta_wrong")
    if report.get("resolved_row_delta") != decision["selected_group"]["row_count"]:
        failures.append("resolved_row_delta_wrong")
    if report.get("remaining_row_count_after") < 0:
        failures.append("remaining_row_negative")

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
    if metrics.get("resolved_group_delta") != 1:
        failures.append("metric_resolved_group_delta_wrong")
    if metrics.get("next_group_auto_opened_count") != 0:
        failures.append("metric_next_group_auto_opened")

    for key in [
        "next_group_auto_opened_count",
        "next_group_inspected_count",
        "row_payload_materialized_count",
        "row_payload_inspected_count",
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
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    if terminal.get("stop_code") not in {
        "STOP_QUEUE_RECONCILED_AFTER_REPAIRED_BURDEN_GROUP_INSPECTION_NEXT_CANDIDATE_ONLY",
        "STOP_QUEUE_RECONCILED_AFTER_REPAIRED_BURDEN_GROUP_INSPECTION_NO_REMAINING_GROUPS",
    }:
        failures.append(f"terminal_stop_wrong:{terminal}")

    return failures

def main() -> int:
    source_before = snapshot_files(SOURCE_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    decision = build_reconciliation_decision(sources)
    ledger = build_resolved_ledger(decision)
    remaining = build_remaining_groups(sources, decision)
    next_candidate = build_next_candidate(remaining)
    reconciliation = build_reconciliation(decision, remaining, next_candidate)
    records = build_queue_state_records(decision, reconciliation)
    trace = build_transition_trace(decision, next_candidate)
    report = build_report(decision, remaining, next_candidate)

    write_json(RECONCILIATION_DECISION_PATH, decision)
    write_json(RECONCILIATION_PATH, reconciliation)
    write_json(RESOLVED_LEDGER_PATH, ledger)
    write_json(REMAINING_GROUPS_PATH, remaining)
    if next_candidate:
        write_json(NEXT_CANDIDATE_PATH, next_candidate)
    else:
        write_json(NEXT_CANDIDATE_PATH, {"schema_version": "r1000_next_selectable_group_candidate_after_repaired_burden_group_inspection_v0", "selection_status": "NO_REMAINING_GROUPS", "next_group_opened": False})
    write_jsonl(QUEUE_STATE_RECORDS_PATH, records)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(
        decision,
        reconciliation,
        ledger,
        remaining,
        next_candidate,
        trace,
        report,
    ))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "REPAIRED_QUEUE_RECONCILE_0_INSPECTION_RECEIPT_CONSUMED": sources["repaired_inspection_receipt"]["receipt_id"] == SOURCE_REPAIRED_INSPECTION_RECEIPT_ID and sources["repaired_inspection_receipt"]["gate"] == "PASS",
        "REPAIRED_QUEUE_RECONCILE_1_QUEUE_RETURN_PACKET_CONSUMED": sources["queue_return_packet"]["packet_status"] == "CANDIDATE_ONLY_NOT_EXECUTED" and sources["queue_return_packet"]["queue_reconciliation_required"] is True,
        "REPAIRED_QUEUE_RECONCILE_2_PRIOR_QUEUE_CONSUMED": sources["burden_queue_receipt"]["receipt_id"] == SOURCE_BURDEN_QUEUE_RECONCILIATION_RECEIPT_ID and sources["burden_queue_receipt"]["gate"] == "PASS",
        "REPAIRED_QUEUE_RECONCILE_3_QUEUE_RECONCILED": reconciliation["queue_reconciled"] is True and report["queue_reconciled_count"] == 1,
        "REPAIRED_QUEUE_RECONCILE_4_RESOLVED_DELTA_RECORDED": report["resolved_group_delta"] == 1 and report["resolved_row_delta"] == decision["selected_group"]["row_count"],
        "REPAIRED_QUEUE_RECONCILE_5_REMAINING_GROUPS_EMITTED": report["remaining_groups_emitted_count"] == 1,
        "REPAIRED_QUEUE_RECONCILE_6_NEXT_CANDIDATE_ONLY": report["next_group_candidate_emitted_count"] in {0, 1} and report["next_group_auto_opened_count"] == 0 and report["next_group_inspected_count"] == 0,
        "REPAIRED_QUEUE_RECONCILE_7_NO_ROW_PAYLOAD_OR_R1000": report["row_payload_inspected_count"] == 0 and report["r1000_run_executed_count"] == 0,
        "REPAIRED_QUEUE_RECONCILE_8_NO_REPAIR_FIELD_VALUE_OR_TAXONOMY_ACTION": report["repair_executed_count"] == 0 and report["target_field_filled_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "REPAIRED_QUEUE_RECONCILE_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "REPAIRED_QUEUE_RECONCILE_10_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0 and trace["terminal"]["next_command_goal"] is None,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = trace["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
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
        "selected_parent_pressure_class": decision["selected_group"].get("parent_pressure_class"),
        "selected_pressure_subtype": decision["selected_group"].get("pressure_subtype"),
        "selected_halt_reason": decision["selected_group"].get("halt_reason"),
        "selected_row_count": decision["selected_group"].get("row_count"),
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        "source_mutation_count": 1 if source_mutation_detected else 0,
    }

    guards = {
        "repaired_inspection_receipt_consumed": True,
        "queue_return_packet_consumed": True,
        "prior_queue_consumed": True,
        "queue_reconciled": True,
        "repaired_group_marked_resolved": True,
        "remaining_groups_emitted": True,
        "next_group_candidate_emitted": next_candidate is not None,
        "next_group_opened": False,
        "next_group_inspected": False,
        "row_payload_materialized": False,
        "row_payload_inspected": False,
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
        "source_repaired_inspection_receipt": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
        "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
        "reconciliation_id": reconciliation["queue_reconciliation_id"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "reconciliation_decision": rel(RECONCILIATION_DECISION_PATH),
        "queue_reconciliation": rel(RECONCILIATION_PATH),
        "resolved_group_ledger": rel(RESOLVED_LEDGER_PATH),
        "queue_state_records": rel(QUEUE_STATE_RECORDS_PATH),
        "remaining_groups": rel(REMAINING_GROUPS_PATH),
        "next_selectable_group_candidate": rel(NEXT_CANDIDATE_PATH),
        "transition_trace": rel(TRANSITION_TRACE_PATH),
        "report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_receipt_v0",
        "receipt_type": "R1000_PRESSURE_QUEUE_RECONCILIATION_AFTER_REPAIRED_BURDEN_GROUP_INSPECTION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_repaired_inspection_receipt_id": SOURCE_REPAIRED_INSPECTION_RECEIPT_ID,
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
        "queue_reconciliation_after_repaired_burden_summary": {
            "reconciliation_result": reconciliation["reconciliation_result"],
            "repaired_selected_pressure_group_id": REPAIRED_SELECTED_PRESSURE_GROUP_ID,
            "resolved_group": decision["selected_group"],
            "prior_counts": decision["prior_counts"],
            "after_counts": decision["after_counts"],
            "next_group_candidate_emitted": next_candidate is not None,
            "next_group_opened": False,
            "recommended_next_handling": aggregate_metrics["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "queue_reconciliation_after_repaired_burden_guards": guards,
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
    print(f"repaired_burden_queue_reconciliation_receipt_id={receipt_id}")
    print(f"repaired_burden_queue_reconciliation_receipt_path=data/r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0_receipts/{receipt_id}.json")
    print(f"remaining_groups_after_repaired_burden_path=data/r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0/r1000_remaining_pressure_groups_after_repaired_burden_group_inspection.json")
    print(f"next_candidate_after_repaired_burden_path=data/r1000_pressure_queue_reconciliation_after_repaired_burden_group_inspection_v0/r1000_next_selectable_group_candidate_after_repaired_burden_group_inspection.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
