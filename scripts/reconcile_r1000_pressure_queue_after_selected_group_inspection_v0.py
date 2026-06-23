#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RECONCILE_R1000_PRESSURE_QUEUE_AFTER_SELECTED_GROUP_INSPECTION_V0"
TARGET_UNIT_ID = "r1000_pressure_queue_reconciliation_after_selected_group_inspection.v0"

SOURCE_GROUP_INSPECTION_RECEIPT_ID = "342e34bd"
SOURCE_GROUP_CAPABILITY_RECEIPT_ID = "73dfb849"
SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID = "4a0cfc09"
SOURCE_FIXED_APPLICATION_RECEIPT_ID = "2a16f593"
SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID = "e3371951"
SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID = "a121ff40"

OUT_DIR = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0_receipts"

QUEUE_RECONCILIATION_PATH = OUT_DIR / "r1000_pressure_queue_reconciliation.json"
RESOLVED_GROUP_LEDGER_PATH = OUT_DIR / "r1000_resolved_pressure_group_ledger.json"
REMAINING_GROUPS_PATH = OUT_DIR / "r1000_remaining_pressure_groups.json"
QUEUE_STATE_RECORDS_PATH = OUT_DIR / "r1000_queue_state_records.jsonl"
NEXT_CANDIDATE_PATH = OUT_DIR / "r1000_next_selectable_group_candidate.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_queue_reconciliation_transition_trace.json"
REPORT_PATH = OUT_DIR / "r1000_pressure_queue_reconciliation_report.json"

GROUP_INSPECTION_RECEIPT_PATH = ROOT / "data" / "r1000_group_specific_inspection_application_v0_receipts" / f"{SOURCE_GROUP_INSPECTION_RECEIPT_ID}.json"
GROUP_INSPECTION_CLASSIFICATION_PATH = ROOT / "data" / "r1000_group_specific_inspection_application_v0" / "selected_group_boundary_stop_classification.json"
GROUP_INSPECTION_DECISION_PACKET_PATH = ROOT / "data" / "r1000_group_specific_inspection_application_v0" / "selected_group_boundary_stop_decision_packet.json"
GROUP_INSPECTION_EVIDENCE_SURFACE_PATH = ROOT / "data" / "r1000_group_specific_inspection_application_v0" / "selected_group_evidence_surface.json"
GROUP_INSPECTION_ROWS_PATH = ROOT / "data" / "r1000_group_specific_inspection_application_v0" / "selected_group_rows.jsonl"

GROUP_CAPABILITY_RECEIPT_PATH = ROOT / "data" / "r1000_group_specific_inspection_capability_v0_receipts" / f"{SOURCE_GROUP_CAPABILITY_RECEIPT_ID}.json"

CLOSED_BRANCH_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_current_surface_closed_branch_exclusion_key_match_fix_v0_receipts" / f"{SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID}.json"
CLOSED_BRANCH_IDENTITY_MAP_PATH = ROOT / "data" / "r1000_current_surface_closed_branch_exclusion_key_match_fix_v0" / "closed_branch_identity_map.json"

FIXED_APPLICATION_RECEIPT_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_fixed_v0_receipts" / f"{SOURCE_FIXED_APPLICATION_RECEIPT_ID}.json"
FIXED_QUEUE_SUMMARY_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_fixed_v0" / "r1000_current_surface_pressure_queue_summary.json"
FIXED_SELECTED_GROUP_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_fixed_v0" / "r1000_current_surface_selected_pressure_group.json"

CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID}.json"
CURRENT_SURFACE_PROTOCOL_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "current_surface_pressure_loop_protocol.json"

EXPECTED_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_RECEIPT_ID}.json"

R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"
R1000_PRESSURE_ROWS_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_event_rows.jsonl"

SOURCE_FILES = [
    GROUP_INSPECTION_RECEIPT_PATH,
    GROUP_INSPECTION_CLASSIFICATION_PATH,
    GROUP_INSPECTION_DECISION_PACKET_PATH,
    GROUP_INSPECTION_EVIDENCE_SURFACE_PATH,
    GROUP_INSPECTION_ROWS_PATH,
    GROUP_CAPABILITY_RECEIPT_PATH,
    CLOSED_BRANCH_FIX_RECEIPT_PATH,
    CLOSED_BRANCH_IDENTITY_MAP_PATH,
    FIXED_APPLICATION_RECEIPT_PATH,
    FIXED_QUEUE_SUMMARY_PATH,
    FIXED_SELECTED_GROUP_PATH,
    CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH,
    CURRENT_SURFACE_PROTOCOL_PATH,
    EXPECTED_LIMIT_RECEIPT_PATH,
    R1000_SCALE_RECEIPT_PATH,
    R1000_PRESSURE_ROWS_PATH,
]

CLOSED_EXPECTED_LIMIT_GROUP = {
    "parent_pressure_class": "TAXONOMY_PRESSURE",
    "pressure_subtype": "missing_label",
    "halt_reason": "STOP_TAXONOMY_GAP",
}

ACCEPTED_HEALTHY_BOUNDARY_GROUP = {
    "parent_pressure_class": "AUTHORITY_BOUNDARY",
    "pressure_subtype": "healthy_boundary_stop",
    "halt_reason": "STOP_AUTHORITY_BOUNDARY",
}

HUMAN_DECISION = {
    "decision": "RECONCILE_R1000_PRESSURE_QUEUE_AFTER_SELECTED_GROUP_INSPECTION",
    "scope": "update the R1000 pressure queue ledger after the selected authority-boundary group was inspected and accepted, without opening another group or building the proposal layer yet",
    "source_group_inspection_receipt_id": SOURCE_GROUP_INSPECTION_RECEIPT_ID,
    "source_closed_branch_fix_receipt_id": SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID,
    "authorized": [
        "read existing tracked R1000 pressure rows",
        "consume closed expected-limit taxonomy branch",
        "consume accepted healthy authority-boundary branch",
        "emit reconciled queue ledger",
        "emit remaining pressure groups",
        "emit next selectable group candidate without opening it",
        "stop with reconciled queue state",
    ],
    "not_authorized": [
        "running new R1000 pressure generation",
        "inspecting another group",
        "repairing any group",
        "inventing values",
        "creating labels",
        "upgrading taxonomy",
        "mutating source rows",
        "mutating existing receipts",
        "auto-opening next group",
        "building proposal layer in this unit",
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

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
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

def key_tuple_from_row(row: Dict[str, Any]) -> Tuple[str, str, str]:
    return (
        str(row.get("parent_pressure_class", "UNKNOWN_PARENT")),
        str(row.get("pressure_subtype", "UNKNOWN_SUBTYPE")),
        str(row.get("halt_reason", "UNKNOWN_HALT")),
    )

def key_dict_to_tuple(key: Dict[str, Any]) -> Tuple[str, str, str]:
    return (
        str(key.get("parent_pressure_class", "UNKNOWN_PARENT")),
        str(key.get("pressure_subtype", "UNKNOWN_SUBTYPE")),
        str(key.get("halt_reason", "UNKNOWN_HALT")),
    )

def key_tuple_to_dict(key: Tuple[str, str, str]) -> Dict[str, str]:
    return {
        "parent_pressure_class": key[0],
        "pressure_subtype": key[1],
        "halt_reason": key[2],
    }

def group_key_hash(key: Tuple[str, str, str]) -> str:
    return sha8({
        "parent_pressure_class": key[0],
        "pressure_subtype": key[1],
        "halt_reason": key[2],
    })

def build_groups(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[str, str, str], List[Tuple[int, Dict[str, Any]]]] = defaultdict(list)
    for index, row in enumerate(rows):
        grouped[key_tuple_from_row(row)].append((index, row))
    groups = []
    for key, indexed_rows in grouped.items():
        groups.append({
            "group_key": key_tuple_to_dict(key),
            "semantic_tuple": list(key),
            "group_hash_candidates": {
                "candidate_key_hash": group_key_hash(key),
                "legacy_join_hash": sha8("|".join(key)),
                "raw_tuple_hash": sha8(key),
            },
            "row_count": len(indexed_rows),
            "sample_row_refs": [
                {
                    "row_index": row_index,
                    "receipt_id": row.get("receipt_id") or row.get("source_receipt_id"),
                    "work_item_id": row.get("work_item_id") or row.get("item_id") or row.get("case_id") or row.get("id"),
                }
                for row_index, row in indexed_rows[:5]
            ],
        })
    groups.sort(
        key=lambda g: (
            -g["row_count"],
            g["group_key"]["parent_pressure_class"],
            g["group_key"]["pressure_subtype"],
            g["group_key"]["halt_reason"],
        )
    )
    return groups

def load_sources() -> Dict[str, Any]:
    return {
        "group_inspection_receipt": read_json(GROUP_INSPECTION_RECEIPT_PATH),
        "group_inspection_classification": read_json(GROUP_INSPECTION_CLASSIFICATION_PATH),
        "group_inspection_decision_packet": read_json(GROUP_INSPECTION_DECISION_PACKET_PATH),
        "group_inspection_evidence_surface": read_json(GROUP_INSPECTION_EVIDENCE_SURFACE_PATH),
        "group_inspection_rows": read_jsonl(GROUP_INSPECTION_ROWS_PATH),
        "group_capability_receipt": read_json(GROUP_CAPABILITY_RECEIPT_PATH),
        "closed_branch_fix_receipt": read_json(CLOSED_BRANCH_FIX_RECEIPT_PATH),
        "closed_branch_identity_map": read_json(CLOSED_BRANCH_IDENTITY_MAP_PATH),
        "fixed_application_receipt": read_json(FIXED_APPLICATION_RECEIPT_PATH),
        "fixed_queue_summary": read_json(FIXED_QUEUE_SUMMARY_PATH),
        "fixed_selected_group": read_json(FIXED_SELECTED_GROUP_PATH),
        "current_surface_protocol_receipt": read_json(CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH),
        "current_surface_protocol": read_json(CURRENT_SURFACE_PROTOCOL_PATH),
        "expected_limit_receipt": read_json(EXPECTED_LIMIT_RECEIPT_PATH),
        "r1000_scale_receipt": read_json(R1000_SCALE_RECEIPT_PATH),
        "r1000_pressure_rows": read_jsonl(R1000_PRESSURE_ROWS_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    inspection = sources["group_inspection_receipt"]
    closed = sources["closed_branch_fix_receipt"]
    fixed = sources["fixed_application_receipt"]
    expected = sources["expected_limit_receipt"]

    if inspection.get("receipt_id") != SOURCE_GROUP_INSPECTION_RECEIPT_ID:
        failures.append("group_inspection_receipt_id_wrong")
    if inspection.get("gate") != "PASS":
        failures.append("group_inspection_not_pass")
    if inspection.get("aggregate_metrics", {}).get("classification") != "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP":
        failures.append("group_inspection_classification_wrong")
    if inspection.get("aggregate_metrics", {}).get("branch_resolution") != "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP_ACCEPTED":
        failures.append("group_inspection_branch_resolution_wrong")
    if inspection.get("aggregate_metrics", {}).get("selected_group_row_count") != 24:
        failures.append("group_inspection_selected_group_row_count_wrong")
    if inspection.get("terminal", {}).get("stop_code") != "STOP_SELECTED_GROUP_INSPECTION_COMPLETE_HEALTHY_BOUNDARY_STOP":
        failures.append("group_inspection_terminal_wrong")

    if sources["group_inspection_classification"].get("classification") != "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP":
        failures.append("classification_artifact_wrong")
    if sources["group_inspection_decision_packet"].get("decision") != "ACCEPT_HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP":
        failures.append("decision_packet_wrong")
    if len(sources["group_inspection_rows"]) != 24:
        failures.append("group_inspection_rows_count_wrong")

    if closed.get("receipt_id") != SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID:
        failures.append("closed_branch_fix_receipt_id_wrong")
    if closed.get("gate") != "PASS":
        failures.append("closed_branch_fix_not_pass")
    if closed.get("aggregate_metrics", {}).get("closed_branch_excluded_count_after_fix") != 1:
        failures.append("closed_expected_limit_group_not_excluded")
    if closed.get("aggregate_metrics", {}).get("closed_group_count_after_fix") != 1:
        failures.append("closed_group_count_after_fix_wrong")

    if fixed.get("receipt_id") != SOURCE_FIXED_APPLICATION_RECEIPT_ID:
        failures.append("fixed_application_receipt_id_wrong")
    if fixed.get("gate") != "PASS":
        failures.append("fixed_application_not_pass")
    if fixed.get("aggregate_metrics", {}).get("open_group_count") != 4:
        failures.append("fixed_application_open_group_count_wrong")

    if expected.get("receipt_id") != SOURCE_EXPECTED_LIMIT_RECEIPT_ID:
        failures.append("expected_limit_receipt_id_wrong")
    if expected.get("gate") != "PASS":
        failures.append("expected_limit_not_pass")
    if expected.get("aggregate_metrics", {}).get("branch_closed") is not True:
        failures.append("expected_limit_branch_not_closed")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def classify_group_state(group: Dict[str, Any]) -> Dict[str, Any]:
    key = group["group_key"]
    if key == CLOSED_EXPECTED_LIMIT_GROUP:
        return {
            "state": "RESOLVED_CLOSED_EXPECTED_LIMIT",
            "resolution": "EXPECTED_SOURCE_CONTENT_LIMIT_MARKED_NO_VALUE_OR_TAXONOMY_REPAIR_AUTHORIZED",
            "source_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        }
    if key == ACCEPTED_HEALTHY_BOUNDARY_GROUP:
        return {
            "state": "RESOLVED_ACCEPTED_HEALTHY_BOUNDARY_STOP",
            "resolution": "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP_ACCEPTED",
            "source_receipt_id": SOURCE_GROUP_INSPECTION_RECEIPT_ID,
        }
    return {
        "state": "OPEN_UNRESOLVED_PRESSURE_GROUP",
        "resolution": None,
        "source_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
    }

def build_reconciliation(groups: List[Dict[str, Any]]) -> Dict[str, Any]:
    reconciled_groups = []
    for group in groups:
        state = classify_group_state(group)
        reconciled_groups.append({
            **{k: v for k, v in group.items() if k != "sample_row_refs"},
            "sample_row_refs": group["sample_row_refs"],
            "queue_state": state["state"],
            "resolution": state["resolution"],
            "resolution_source_receipt_id": state["source_receipt_id"],
        })

    resolved = [g for g in reconciled_groups if g["queue_state"].startswith("RESOLVED")]
    remaining = [g for g in reconciled_groups if g["queue_state"] == "OPEN_UNRESOLVED_PRESSURE_GROUP"]
    next_candidate = remaining[0] if remaining else None

    return {
        "schema_version": "r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0",
        "source_group_inspection_receipt_id": SOURCE_GROUP_INSPECTION_RECEIPT_ID,
        "source_closed_branch_fix_receipt_id": SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID,
        "source_fixed_application_receipt_id": SOURCE_FIXED_APPLICATION_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "total_group_count": len(reconciled_groups),
        "total_pressure_row_count": sum(g["row_count"] for g in reconciled_groups),
        "resolved_group_count": len(resolved),
        "resolved_row_count": sum(g["row_count"] for g in resolved),
        "closed_expected_limit_group_count": len([g for g in reconciled_groups if g["queue_state"] == "RESOLVED_CLOSED_EXPECTED_LIMIT"]),
        "closed_expected_limit_row_count": sum(g["row_count"] for g in reconciled_groups if g["queue_state"] == "RESOLVED_CLOSED_EXPECTED_LIMIT"),
        "accepted_healthy_boundary_stop_group_count": len([g for g in reconciled_groups if g["queue_state"] == "RESOLVED_ACCEPTED_HEALTHY_BOUNDARY_STOP"]),
        "accepted_healthy_boundary_stop_row_count": sum(g["row_count"] for g in reconciled_groups if g["queue_state"] == "RESOLVED_ACCEPTED_HEALTHY_BOUNDARY_STOP"),
        "remaining_open_group_count": len(remaining),
        "remaining_open_row_count": sum(g["row_count"] for g in remaining),
        "reconciled_groups": reconciled_groups,
        "remaining_groups": remaining,
        "next_selectable_group_candidate": None if next_candidate is None else {
            "group_key": next_candidate["group_key"],
            "semantic_tuple": next_candidate["semantic_tuple"],
            "group_hash_candidates": next_candidate["group_hash_candidates"],
            "row_count": next_candidate["row_count"],
            "selection_status": "CANDIDATE_ONLY_NOT_OPENED",
        },
    }

def build_resolved_ledger(reconciliation: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_resolved_pressure_group_ledger_v0",
        "resolved_group_count": reconciliation["resolved_group_count"],
        "resolved_row_count": reconciliation["resolved_row_count"],
        "resolved_groups": [
            {
                "group_key": g["group_key"],
                "row_count": g["row_count"],
                "queue_state": g["queue_state"],
                "resolution": g["resolution"],
                "resolution_source_receipt_id": g["resolution_source_receipt_id"],
            }
            for g in reconciliation["reconciled_groups"]
            if g["queue_state"].startswith("RESOLVED")
        ],
    }

def build_remaining_groups(reconciliation: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_remaining_pressure_groups_after_selected_group_inspection_v0",
        "remaining_open_group_count": reconciliation["remaining_open_group_count"],
        "remaining_open_row_count": reconciliation["remaining_open_row_count"],
        "remaining_groups": reconciliation["remaining_groups"],
    }

def build_queue_state_records(reconciliation: Dict[str, Any]) -> List[Dict[str, Any]]:
    records = []
    for group in reconciliation["reconciled_groups"]:
        records.append({
            "schema_version": "r1000_pressure_queue_state_record_v0",
            "record_id": sha8({
                "group": group["group_key"],
                "state": group["queue_state"],
                "source": group["resolution_source_receipt_id"],
            }),
            "pressure_group_key": group["group_key"],
            "row_count": group["row_count"],
            "queue_state": group["queue_state"],
            "resolution": group["resolution"],
            "resolution_source_receipt_id": group["resolution_source_receipt_id"],
            "authority_state": {
                "source_mutation_count": 0,
                "existing_receipt_mutation_count": 0,
                "other_group_inspection_count": 0,
                "repair_executed_count": 0,
                "field_value_invention_count": 0,
                "taxonomy_action_count": 0,
                "next_group_auto_opened_count": 0,
                "hidden_next_command_count": 0,
            },
        })
    return records

def build_transition_trace(reconciliation: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_queue_reconciliation_transition_trace_v0",
        "source_group_inspection_receipt_id": SOURCE_GROUP_INSPECTION_RECEIPT_ID,
        "trace": [
            {
                "step": "consume_closed_expected_limit_branch",
                "question": "closed_expected_limit_branch_present",
                "answer": reconciliation["closed_expected_limit_group_count"] == 1,
                "yes": "consume_accepted_healthy_boundary_stop_branch",
                "no": "STOP_QUEUE_RECONCILIATION_INPUT_MISSING",
                "taken": "consume_accepted_healthy_boundary_stop_branch" if reconciliation["closed_expected_limit_group_count"] == 1 else "STOP_QUEUE_RECONCILIATION_INPUT_MISSING",
            },
            {
                "step": "consume_accepted_healthy_boundary_stop_branch",
                "question": "accepted_healthy_boundary_stop_present",
                "answer": reconciliation["accepted_healthy_boundary_stop_group_count"] == 1,
                "yes": "materialize_remaining_groups",
                "no": "STOP_QUEUE_RECONCILIATION_INPUT_MISSING",
                "taken": "materialize_remaining_groups" if reconciliation["accepted_healthy_boundary_stop_group_count"] == 1 else "STOP_QUEUE_RECONCILIATION_INPUT_MISSING",
            },
            {
                "step": "materialize_remaining_groups",
                "question": "remaining_groups_exist",
                "answer": reconciliation["remaining_open_group_count"] > 0,
                "yes": "emit_next_candidate_without_opening",
                "no": "STOP_QUEUE_RECONCILED_EMPTY",
                "taken": "emit_next_candidate_without_opening" if reconciliation["remaining_open_group_count"] > 0 else "STOP_QUEUE_RECONCILED_EMPTY",
            },
            {
                "step": "emit_next_candidate_without_opening",
                "question": "next_group_opened",
                "answer": False,
                "yes": "STOP_AUTHORITY_VIOLATION",
                "no": "STOP_QUEUE_RECONCILED",
                "taken": "STOP_QUEUE_RECONCILED",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_QUEUE_RECONCILED",
            "next_command_goal": None,
        },
    }

def build_report(reconciliation: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_pressure_queue_reconciliation_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_group_inspection_receipt_id": SOURCE_GROUP_INSPECTION_RECEIPT_ID,
        "source_closed_branch_fix_receipt_id": SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID,
        "total_group_count": reconciliation["total_group_count"],
        "total_pressure_row_count": reconciliation["total_pressure_row_count"],
        "resolved_group_count": reconciliation["resolved_group_count"],
        "resolved_row_count": reconciliation["resolved_row_count"],
        "closed_expected_limit_group_count": reconciliation["closed_expected_limit_group_count"],
        "closed_expected_limit_row_count": reconciliation["closed_expected_limit_row_count"],
        "accepted_healthy_boundary_stop_group_count": reconciliation["accepted_healthy_boundary_stop_group_count"],
        "accepted_healthy_boundary_stop_row_count": reconciliation["accepted_healthy_boundary_stop_row_count"],
        "remaining_open_group_count": reconciliation["remaining_open_group_count"],
        "remaining_open_row_count": reconciliation["remaining_open_row_count"],
        "next_selectable_group_candidate_count": 1 if reconciliation["next_selectable_group_candidate"] else 0,
        "next_group_auto_opened_count": 0,
        "proposal_layer_built_count": 0,
        "r1000_run_executed_count": 0,
        "other_group_inspection_count": 0,
        "repair_executed_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": "BUILD_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_FOR_EXPECTED_LIMITS_V0",
    }

def validate_outputs(reconciliation: Dict[str, Any], ledger: Dict[str, Any], remaining: Dict[str, Any], records: List[Dict[str, Any]], trace: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if reconciliation["total_group_count"] != 5:
        failures.append(f"total_group_count_wrong:{reconciliation['total_group_count']}")
    if reconciliation["total_pressure_row_count"] != 88:
        failures.append(f"total_pressure_row_count_wrong:{reconciliation['total_pressure_row_count']}")
    if reconciliation["resolved_group_count"] != 2:
        failures.append(f"resolved_group_count_wrong:{reconciliation['resolved_group_count']}")
    if reconciliation["resolved_row_count"] != 49:
        failures.append(f"resolved_row_count_wrong:{reconciliation['resolved_row_count']}")
    if reconciliation["closed_expected_limit_group_count"] != 1:
        failures.append("closed_expected_limit_group_count_wrong")
    if reconciliation["closed_expected_limit_row_count"] != 25:
        failures.append(f"closed_expected_limit_row_count_wrong:{reconciliation['closed_expected_limit_row_count']}")
    if reconciliation["accepted_healthy_boundary_stop_group_count"] != 1:
        failures.append("accepted_healthy_boundary_stop_group_count_wrong")
    if reconciliation["accepted_healthy_boundary_stop_row_count"] != 24:
        failures.append(f"accepted_healthy_boundary_stop_row_count_wrong:{reconciliation['accepted_healthy_boundary_stop_row_count']}")
    if reconciliation["remaining_open_group_count"] != 3:
        failures.append(f"remaining_open_group_count_wrong:{reconciliation['remaining_open_group_count']}")
    if reconciliation["remaining_open_row_count"] != 39:
        failures.append(f"remaining_open_row_count_wrong:{reconciliation['remaining_open_row_count']}")
    if ledger["resolved_group_count"] != 2:
        failures.append("ledger_resolved_group_count_wrong")
    if remaining["remaining_open_group_count"] != 3:
        failures.append("remaining_group_count_wrong")
    if len(records) != 5:
        failures.append(f"queue_state_record_count_wrong:{len(records)}")
    if trace["terminal"]["stop_code"] != "STOP_QUEUE_RECONCILED":
        failures.append(f"trace_stop_wrong:{trace['terminal']}")
    if trace["terminal"]["next_command_goal"] is not None:
        failures.append("trace_next_not_null")
    if reconciliation["next_selectable_group_candidate"] is None:
        failures.append("next_candidate_missing")
    elif reconciliation["next_selectable_group_candidate"]["selection_status"] != "CANDIDATE_ONLY_NOT_OPENED":
        failures.append("next_candidate_status_wrong")
    for record in records:
        authority = record["authority_state"]
        for key, value in authority.items():
            if value != 0:
                failures.append(f"record_authority_not_zero:{key}:{value}")
    for key in [
        "next_group_auto_opened_count",
        "proposal_layer_built_count",
        "r1000_run_executed_count",
        "other_group_inspection_count",
        "repair_executed_count",
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
    expected = {
        "total_group_count": 5,
        "total_pressure_row_count": 88,
        "resolved_group_count": 2,
        "resolved_row_count": 49,
        "closed_expected_limit_group_count": 1,
        "closed_expected_limit_row_count": 25,
        "accepted_healthy_boundary_stop_group_count": 1,
        "accepted_healthy_boundary_stop_row_count": 24,
        "remaining_open_group_count": 3,
        "remaining_open_row_count": 39,
        "next_selectable_group_candidate_count": 1,
    }
    for key, value in expected.items():
        if metrics.get(key) != value:
            failures.append(f"metric_wrong:{key}:{metrics.get(key)}")
    for key in [
        "next_group_auto_opened_count",
        "proposal_layer_built_count",
        "r1000_run_executed_count",
        "other_group_inspection_count",
        "repair_executed_count",
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
    if terminal.get("stop_code") != "STOP_QUEUE_RECONCILED":
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

    groups = build_groups(sources["r1000_pressure_rows"])
    reconciliation = build_reconciliation(groups)
    ledger = build_resolved_ledger(reconciliation)
    remaining = build_remaining_groups(reconciliation)
    records = build_queue_state_records(reconciliation)
    trace = build_transition_trace(reconciliation)
    report = build_report(reconciliation)

    write_json(QUEUE_RECONCILIATION_PATH, reconciliation)
    write_json(RESOLVED_GROUP_LEDGER_PATH, ledger)
    write_json(REMAINING_GROUPS_PATH, remaining)
    write_jsonl(QUEUE_STATE_RECORDS_PATH, records)
    write_json(NEXT_CANDIDATE_PATH, reconciliation["next_selectable_group_candidate"])
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(reconciliation, ledger, remaining, records, trace, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "QUEUE_RECONCILE_0_GROUP_INSPECTION_CONSUMED": sources["group_inspection_receipt"]["receipt_id"] == SOURCE_GROUP_INSPECTION_RECEIPT_ID and sources["group_inspection_receipt"]["gate"] == "PASS",
        "QUEUE_RECONCILE_1_CLOSED_EXPECTED_LIMIT_CONSUMED": reconciliation["closed_expected_limit_group_count"] == 1 and reconciliation["closed_expected_limit_row_count"] == 25,
        "QUEUE_RECONCILE_2_HEALTHY_BOUNDARY_STOP_CONSUMED": reconciliation["accepted_healthy_boundary_stop_group_count"] == 1 and reconciliation["accepted_healthy_boundary_stop_row_count"] == 24,
        "QUEUE_RECONCILE_3_RECONCILED_LEDGER_EMITTED": RESOLVED_GROUP_LEDGER_PATH.exists() and ledger["resolved_group_count"] == 2,
        "QUEUE_RECONCILE_4_REMAINING_GROUPS_EMITTED": REMAINING_GROUPS_PATH.exists() and remaining["remaining_open_group_count"] == 3,
        "QUEUE_RECONCILE_5_NEXT_CANDIDATE_EMITTED_NOT_OPENED": NEXT_CANDIDATE_PATH.exists() and reconciliation["next_selectable_group_candidate"] is not None and reconciliation["next_selectable_group_candidate"]["selection_status"] == "CANDIDATE_ONLY_NOT_OPENED",
        "QUEUE_RECONCILE_6_NO_NEXT_GROUP_AUTO_OPEN": report["next_group_auto_opened_count"] == 0,
        "QUEUE_RECONCILE_7_NO_PROPOSAL_LAYER_BUILT": report["proposal_layer_built_count"] == 0,
        "QUEUE_RECONCILE_8_NO_R1000_RUN_OR_OTHER_GROUP_INSPECTION": report["r1000_run_executed_count"] == 0 and report["other_group_inspection_count"] == 0,
        "QUEUE_RECONCILE_9_NO_REPAIR_OR_VALUE_OR_TAXONOMY_ACTION": report["repair_executed_count"] == 0 and report["field_value_invention_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0,
        "QUEUE_RECONCILE_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "QUEUE_RECONCILE_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_QUEUE_RECONCILED",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_group_inspection_receipt_id": SOURCE_GROUP_INSPECTION_RECEIPT_ID,
        "source_closed_branch_fix_receipt_id": SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID,
        "source_fixed_application_receipt_id": SOURCE_FIXED_APPLICATION_RECEIPT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "total_group_count": reconciliation["total_group_count"],
        "total_pressure_row_count": reconciliation["total_pressure_row_count"],
        "resolved_group_count": reconciliation["resolved_group_count"],
        "resolved_row_count": reconciliation["resolved_row_count"],
        "closed_expected_limit_group_count": reconciliation["closed_expected_limit_group_count"],
        "closed_expected_limit_row_count": reconciliation["closed_expected_limit_row_count"],
        "accepted_healthy_boundary_stop_group_count": reconciliation["accepted_healthy_boundary_stop_group_count"],
        "accepted_healthy_boundary_stop_row_count": reconciliation["accepted_healthy_boundary_stop_row_count"],
        "remaining_open_group_count": reconciliation["remaining_open_group_count"],
        "remaining_open_row_count": reconciliation["remaining_open_row_count"],
        "next_selectable_group_candidate_count": 1 if reconciliation["next_selectable_group_candidate"] else 0,
        "next_selectable_group_candidate": reconciliation["next_selectable_group_candidate"],
        "next_group_auto_opened_count": 0,
        "proposal_layer_built_count": 0,
        "r1000_run_executed_count": 0,
        "other_group_inspection_count": 0,
        "repair_executed_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": "BUILD_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_FOR_EXPECTED_LIMITS_V0",
    }

    guards = {
        "group_inspection_consumed": True,
        "closed_expected_limit_consumed": reconciliation["closed_expected_limit_group_count"] == 1,
        "accepted_healthy_boundary_stop_consumed": reconciliation["accepted_healthy_boundary_stop_group_count"] == 1,
        "queue_reconciled": True,
        "next_candidate_emitted": reconciliation["next_selectable_group_candidate"] is not None,
        "next_group_auto_opened": False,
        "proposal_layer_built": False,
        "r1000_run_executed": False,
        "other_group_inspection_executed": False,
        "repair_executed": False,
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
        "source_group_inspection": SOURCE_GROUP_INSPECTION_RECEIPT_ID,
        "resolved_group_count": reconciliation["resolved_group_count"],
        "remaining_open_group_count": reconciliation["remaining_open_group_count"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "queue_reconciliation": rel(QUEUE_RECONCILIATION_PATH),
        "resolved_group_ledger": rel(RESOLVED_GROUP_LEDGER_PATH),
        "remaining_pressure_groups": rel(REMAINING_GROUPS_PATH),
        "queue_state_records": rel(QUEUE_STATE_RECORDS_PATH),
        "next_selectable_group_candidate": rel(NEXT_CANDIDATE_PATH),
        "queue_reconciliation_transition_trace": rel(TRANSITION_TRACE_PATH),
        "queue_reconciliation_report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_pressure_queue_reconciliation_after_selected_group_inspection_receipt_v0",
        "receipt_type": "R1000_PRESSURE_QUEUE_RECONCILIATION_AFTER_SELECTED_GROUP_INSPECTION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_group_inspection_receipt_id": SOURCE_GROUP_INSPECTION_RECEIPT_ID,
        "source_closed_branch_fix_receipt_id": SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID,
        "source_fixed_application_receipt_id": SOURCE_FIXED_APPLICATION_RECEIPT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "r1000_pressure_queue_reconciliation_summary": {
            "total_group_count": reconciliation["total_group_count"],
            "total_pressure_row_count": reconciliation["total_pressure_row_count"],
            "resolved_group_count": reconciliation["resolved_group_count"],
            "resolved_row_count": reconciliation["resolved_row_count"],
            "closed_expected_limit_group_count": reconciliation["closed_expected_limit_group_count"],
            "closed_expected_limit_row_count": reconciliation["closed_expected_limit_row_count"],
            "accepted_healthy_boundary_stop_group_count": reconciliation["accepted_healthy_boundary_stop_group_count"],
            "accepted_healthy_boundary_stop_row_count": reconciliation["accepted_healthy_boundary_stop_row_count"],
            "remaining_open_group_count": reconciliation["remaining_open_group_count"],
            "remaining_open_row_count": reconciliation["remaining_open_row_count"],
            "next_selectable_group_candidate": reconciliation["next_selectable_group_candidate"],
            "recommended_next_handling": "BUILD_CANDIDATE_MISSING_OBJECT_PROPOSAL_LAYER_FOR_EXPECTED_LIMITS_V0",
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "queue_reconciliation_guards": guards,
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
    print(f"r1000_queue_reconciliation_receipt_id={receipt_id}")
    print(f"r1000_queue_reconciliation_receipt_path=data/r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0_receipts/{receipt_id}.json")
    print(f"r1000_queue_remaining_groups_path=data/r1000_pressure_queue_reconciliation_after_selected_group_inspection_v0/r1000_remaining_pressure_groups.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
