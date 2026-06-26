#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "APPLY_CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_TO_R1000_PRESSURE_QUEUE_V0"
TARGET_UNIT_ID = "current_surface_pressure_loop_r1000_application.v0"

SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID = "e3371951"
SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID = "a121ff40"
SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID = "7c9718e0"
SOURCE_PRESSURE_LOOP_APPLICATION_RECEIPT_ID = "be19f438"
SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID = "6148b4fa"

CLOSED_PRESSURE_GROUP_KEY_HASHES = ["38c604a1"]
EXPECTED_CLOSED_BRANCH_RESOLUTION = "EXPECTED_SOURCE_CONTENT_LIMIT_MARKED_NO_VALUE_OR_TAXONOMY_REPAIR_AUTHORIZED"

OUT_DIR = ROOT / "data" / "current_surface_pressure_loop_r1000_application_v0"
RECEIPT_DIR = ROOT / "data" / "current_surface_pressure_loop_r1000_application_v0_receipts"

QUEUE_SUMMARY_PATH = OUT_DIR / "r1000_current_surface_pressure_queue_summary.json"
SURFACE_RECORDS_PATH = OUT_DIR / "r1000_current_surface_state_records.jsonl"
SELECTED_GROUP_PATH = OUT_DIR / "r1000_current_surface_selected_pressure_group.json"
TRANSITION_TRACE_PATH = OUT_DIR / "r1000_current_surface_transition_trace.json"
CAPABILITY_STOP_PACKET_PATH = OUT_DIR / "r1000_current_surface_capability_stop_packet.json"
APPLICATION_REPORT_PATH = OUT_DIR / "r1000_current_surface_pressure_loop_application_report.json"

PROTOCOL_RECEIPT_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID}.json"
PROTOCOL_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "current_surface_pressure_loop_protocol.json"
SURFACE_SCHEMA_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "surface_state_record_schema.json"
TRANSITION_TABLE_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "surface_transition_decision_table.json"
CAPABILITY_SCHEMA_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "capability_stop_packet_schema.json"
ACCEPTANCE_GATES_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "pressure_loop_acceptance_gates.json"

EXPECTED_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_RECEIPT_ID}.json"
EXPECTED_LIMIT_MARKER_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0" / "expected_source_content_limit_marker.json"
EXPECTED_LIMIT_CLOSURE_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0" / "expected_source_content_limit_closure_record.json"

R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"
R1000_PRESSURE_ROWS_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_event_rows.jsonl"
TOP_GROUP_CLASSIFICATION_RECEIPT_PATH = ROOT / "data" / "r1000_candidate_c_top_group_classification_v0_receipts" / f"{SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID}.json"
PRIOR_LOOP_APPLICATION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0_receipts" / f"{SOURCE_PRESSURE_LOOP_APPLICATION_RECEIPT_ID}.json"
BASE_PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID}.json"

SOURCE_FILES = [
    PROTOCOL_RECEIPT_PATH,
    PROTOCOL_PATH,
    SURFACE_SCHEMA_PATH,
    TRANSITION_TABLE_PATH,
    CAPABILITY_SCHEMA_PATH,
    ACCEPTANCE_GATES_PATH,
    EXPECTED_LIMIT_RECEIPT_PATH,
    EXPECTED_LIMIT_MARKER_PATH,
    EXPECTED_LIMIT_CLOSURE_PATH,
    R1000_SCALE_RECEIPT_PATH,
    R1000_PRESSURE_ROWS_PATH,
    TOP_GROUP_CLASSIFICATION_RECEIPT_PATH,
    PRIOR_LOOP_APPLICATION_RECEIPT_PATH,
    BASE_PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH,
]

HUMAN_DECISION = {
    "decision": "APPLY_CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_TO_R1000_PRESSURE_QUEUE",
    "scope": "apply the frozen current-surface pressure loop to the existing tracked R1000 pressure queue, excluding the already closed expected-limit branch, without running a new R1000 computation or auto-opening a next group",
    "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
    "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
    "authorized": [
        "read existing tracked R1000 pressure event rows",
        "materialize current-surface pressure queue summary",
        "exclude already closed pressure branch",
        "select next remaining pressure group for inspection",
        "emit surface-state records",
        "emit transition trace",
        "stop at capability layer if the next move requires a capability not yet present",
    ],
    "not_authorized": [
        "running new R1000 pressure generation",
        "opening next group for execution",
        "repairing selected group",
        "inventing values",
        "creating labels",
        "upgrading taxonomy",
        "mutating source rows",
        "mutating existing receipts",
        "claiming unlimited capability",
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
    rows = []
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
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

def load_sources() -> Dict[str, Any]:
    return {
        "protocol_receipt": read_json(PROTOCOL_RECEIPT_PATH),
        "protocol": read_json(PROTOCOL_PATH),
        "surface_schema": read_json(SURFACE_SCHEMA_PATH),
        "transition_table": read_json(TRANSITION_TABLE_PATH),
        "capability_schema": read_json(CAPABILITY_SCHEMA_PATH),
        "expected_limit_receipt": read_json(EXPECTED_LIMIT_RECEIPT_PATH),
        "expected_limit_marker": read_json(EXPECTED_LIMIT_MARKER_PATH),
        "expected_limit_closure": read_json(EXPECTED_LIMIT_CLOSURE_PATH),
        "r1000_scale_receipt": read_json(R1000_SCALE_RECEIPT_PATH),
        "r1000_pressure_rows": read_jsonl(R1000_PRESSURE_ROWS_PATH),
        "top_group_classification_receipt": read_json(TOP_GROUP_CLASSIFICATION_RECEIPT_PATH),
        "prior_loop_application_receipt": read_json(PRIOR_LOOP_APPLICATION_RECEIPT_PATH),
        "base_pressure_loop_protocol_receipt": read_json(BASE_PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    protocol_receipt = sources["protocol_receipt"]
    protocol_metrics = protocol_receipt.get("aggregate_metrics", {})
    expected_receipt = sources["expected_limit_receipt"]
    expected_metrics = expected_receipt.get("aggregate_metrics", {})

    if protocol_receipt.get("receipt_id") != SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID:
        failures.append("protocol_receipt_id_wrong")
    if protocol_receipt.get("gate") != "PASS":
        failures.append("protocol_not_pass")
    if protocol_metrics.get("current_surface_scope_only") is not True:
        failures.append("protocol_not_current_surface_scoped")
    if protocol_metrics.get("capability_stop_defined") is not True:
        failures.append("protocol_capability_stop_missing")
    if protocol_metrics.get("expected_limit_closure_defined") is not True:
        failures.append("protocol_expected_limit_closure_missing")
    if protocol_metrics.get("r1000_run_executed_count") != 0:
        failures.append("protocol_already_ran_r1000")
    if protocol_metrics.get("next_group_auto_opened_count") != 0:
        failures.append("protocol_auto_opened_next_group")

    if expected_receipt.get("receipt_id") != SOURCE_EXPECTED_LIMIT_RECEIPT_ID:
        failures.append("expected_limit_receipt_id_wrong")
    if expected_receipt.get("gate") != "PASS":
        failures.append("expected_limit_not_pass")
    if expected_metrics.get("branch_closed") is not True:
        failures.append("expected_limit_branch_not_closed")
    if expected_metrics.get("expected_limit_marked") is not True:
        failures.append("expected_limit_not_marked")
    if expected_metrics.get("next_group_auto_opened_count") != 0:
        failures.append("expected_limit_auto_opened_next_group")

    if sources["r1000_scale_receipt"].get("receipt_id") != SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID:
        failures.append("r1000_scale_receipt_id_wrong")
    if sources["top_group_classification_receipt"].get("receipt_id") != SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID:
        failures.append("top_group_classification_receipt_id_wrong")
    if sources["prior_loop_application_receipt"].get("receipt_id") != SOURCE_PRESSURE_LOOP_APPLICATION_RECEIPT_ID:
        failures.append("prior_loop_application_receipt_id_wrong")
    if not sources["r1000_pressure_rows"]:
        failures.append("r1000_pressure_rows_empty")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def first_existing(row: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    for key in keys:
        if key in row and row.get(key) is not None:
            return row.get(key)
    return default

def group_key_tuple(row: Dict[str, Any]) -> Tuple[str, str, str]:
    parent = str(first_existing(row, ["parent_pressure_class", "pressure_class", "class"], "UNKNOWN_PARENT"))
    subtype = str(first_existing(row, ["pressure_subtype", "subtype", "pressure_kind"], "UNKNOWN_SUBTYPE"))
    halt = str(first_existing(row, ["halt_reason", "stop_code", "halt"], "UNKNOWN_HALT"))
    return parent, subtype, halt

def group_key_hash(group_key: Tuple[str, str, str]) -> str:
    return sha8({
        "parent_pressure_class": group_key[0],
        "pressure_subtype": group_key[1],
        "halt_reason": group_key[2],
    })

def build_pressure_groups(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[str, str, str], List[Dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[group_key_tuple(row)].append(row)

    groups = []
    for key, group_rows in grouped.items():
        hashes = {
            "candidate_key_hash": group_key_hash(key),
            "legacy_join_hash": sha8("|".join(key)),
            "raw_tuple_hash": sha8(key),
        }
        groups.append({
            "group_key": {
                "parent_pressure_class": key[0],
                "pressure_subtype": key[1],
                "halt_reason": key[2],
            },
            "group_hash_candidates": hashes,
            "row_count": len(group_rows),
            "sample_row_refs": [
                {
                    "row_index": group_rows.index(row),
                    "work_item_id": first_existing(row, ["work_item_id", "item_id", "case_id", "id"], None),
                    "receipt_id": first_existing(row, ["receipt_id", "source_receipt_id"], None),
                }
                for row in group_rows[:3]
            ],
            "rows": group_rows,
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

def is_closed_group(group: Dict[str, Any]) -> bool:
    return any(h in CLOSED_PRESSURE_GROUP_KEY_HASHES for h in group["group_hash_candidates"].values())

def choose_selected_group(groups: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    for group in groups:
        if not is_closed_group(group):
            return group
    return None

def build_queue_summary(groups: List[Dict[str, Any]], selected: Dict[str, Any] | None) -> Dict[str, Any]:
    closed = [g for g in groups if is_closed_group(g)]
    open_groups = [g for g in groups if not is_closed_group(g)]
    profile = [g["row_count"] for g in groups[:10]]
    return {
        "schema_version": "r1000_current_surface_pressure_queue_summary_v0",
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "total_group_count": len(groups),
        "total_pressure_row_count": sum(g["row_count"] for g in groups),
        "closed_group_count": len(closed),
        "open_group_count": len(open_groups),
        "closed_pressure_group_key_hashes": CLOSED_PRESSURE_GROUP_KEY_HASHES,
        "top_group_profile": profile,
        "closed_groups": [
            {
                "group_key": g["group_key"],
                "group_hash_candidates": g["group_hash_candidates"],
                "row_count": g["row_count"],
                "closure_reason": EXPECTED_CLOSED_BRANCH_RESOLUTION,
            }
            for g in closed
        ],
        "selected_next_group": None if selected is None else {
            "group_key": selected["group_key"],
            "group_hash_candidates": selected["group_hash_candidates"],
            "row_count": selected["row_count"],
        },
    }

def surface_record(surface_id_seed: Any, surface_type: str, source_receipt_id: str, pressure_group_key: Any, row_count: int, current_class: str | None, terminal_type: str | None = None, stop_code: str | None = None, capability_stop_required: bool = False, required_capability: str | None = None) -> Dict[str, Any]:
    return {
        "schema_version": "current_surface_state_record_v0",
        "surface_id": sha8(surface_id_seed),
        "surface_type": surface_type,
        "source_receipt_id": source_receipt_id,
        "pressure_group_key": pressure_group_key,
        "row_count": row_count,
        "key_visibility": {
            "required_keys_visible": None,
            "missing_keys": [],
        },
        "value_state": {
            "values_present": None,
            "values_absent": None,
            "value_invention_count": 0,
        },
        "provenance_state": {
            "absence_reasons_present": None,
            "provenance_refs_present": None,
            "structural_refs_preserved": None,
        },
        "authority_state": {
            "source_mutation_count": 0,
            "receipt_mutation_count": 0,
            "taxonomy_action_count": 0,
            "hidden_next_command_count": 0,
            "next_group_auto_opened_count": 0,
        },
        "classification": {
            "current_class": current_class,
            "limit_type": None,
            "branch_resolution": None,
        },
        "capability_state": {
            "required_capability": required_capability,
            "capability_available": False if capability_stop_required else None,
            "capability_stop_required": capability_stop_required,
        },
        "terminal": {
            "terminal_type": terminal_type,
            "stop_code": stop_code,
            "next_command_goal": None,
        },
    }

def build_surface_records(queue_summary: Dict[str, Any], selected: Dict[str, Any] | None) -> List[Dict[str, Any]]:
    records = [
        surface_record(
            {"surface": "queue", "source": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID},
            "pressure_queue_surface",
            SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
            "R1000_PRESSURE_QUEUE",
            queue_summary["total_pressure_row_count"],
            "R1000_PRESSURE_QUEUE_MATERIALIZED",
        )
    ]

    if selected is not None:
        records.append(
            surface_record(
                {"surface": "selected_group", "group": selected["group_key"]},
                "pressure_group_surface",
                SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
                selected["group_key"],
                selected["row_count"],
                "NEXT_REMAINING_PRESSURE_GROUP_SELECTED_FOR_INSPECTION",
            )
        )
        records.append(
            surface_record(
                {"surface": "capability_stop", "group": selected["group_key"]},
                "capability_stop_surface",
                SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
                selected["group_key"],
                selected["row_count"],
                "CAPABILITY_BOUNDARY_UNKNOWN_FOR_SELECTED_GROUP_INSPECTION",
                terminal_type="STOP",
                stop_code="STOP_CAPABILITY_LAYER_REQUIRED",
                capability_stop_required=True,
                required_capability="CURRENT_SURFACE_GROUP_SPECIFIC_INSPECTION_CAPABILITY",
            )
        )
    else:
        records.append(
            surface_record(
                {"surface": "queue_closed", "source": SOURCE_EXPECTED_LIMIT_RECEIPT_ID},
                "expected_limit_closure_surface",
                SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
                "R1000_PRESSURE_QUEUE",
                0,
                "NO_OPEN_PRESSURE_GROUP_AFTER_CLOSED_BRANCH_FILTER",
                terminal_type="STOP",
                stop_code="STOP_NO_ACTIONABLE_PRESSURE",
            )
        )

    return records

def build_selected_group(selected: Dict[str, Any] | None) -> Dict[str, Any]:
    if selected is None:
        return {
            "schema_version": "r1000_current_surface_selected_pressure_group_v0",
            "selected": False,
            "selection_reason": "no open pressure group remains after closed-branch filter",
        }
    group_copy = {k: v for k, v in selected.items() if k != "rows"}
    return {
        "schema_version": "r1000_current_surface_selected_pressure_group_v0",
        "selected": True,
        "selection_policy": "highest_count_remaining_group_after_closed_branch_filter",
        "selection_reason": "current protocol can select for inspection but must stop before group-specific execution if capability is unknown",
        "selected_group": group_copy,
    }

def build_transition_trace(queue_summary: Dict[str, Any], selected: Dict[str, Any] | None) -> Dict[str, Any]:
    trace = [
        {
            "step": "select_pressure_group",
            "question": "pressure_group_selected",
            "answer": selected is not None,
            "yes": "inspect_pressure_group_surface",
            "no": "STOP_NO_ACTIONABLE_PRESSURE",
            "taken": "inspect_pressure_group_surface" if selected is not None else "STOP_NO_ACTIONABLE_PRESSURE",
        }
    ]
    if selected is not None:
        trace.extend([
            {
                "step": "inspect_pressure_group_surface",
                "question": "pressure_class_understood_enough_to_choose_inspection",
                "answer": False,
                "yes": "extract_evidence_surface",
                "no": "STOP_NEEDS_PRESSURE_CLASSIFICATION",
                "taken": "STOP_CAPABILITY_LAYER_REQUIRED",
                "override_reason": "selected remaining group requires group-specific inspection capability not yet proven for current runner",
            },
            {
                "step": "any_step",
                "question": "required_next_move_exceeds_current_capability",
                "answer": True,
                "yes": "STOP_CAPABILITY_LAYER_REQUIRED",
                "no": "continue_current_transition",
                "taken": "STOP_CAPABILITY_LAYER_REQUIRED",
            },
        ])

    return {
        "schema_version": "r1000_current_surface_transition_trace_v0",
        "source_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "queue_summary_ref": rel(QUEUE_SUMMARY_PATH),
        "selected_group_ref": rel(SELECTED_GROUP_PATH),
        "trace": trace,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CAPABILITY_LAYER_REQUIRED" if selected is not None else "STOP_NO_ACTIONABLE_PRESSURE",
            "next_command_goal": None,
        },
    }

def build_capability_stop_packet(selected: Dict[str, Any] | None, records: List[Dict[str, Any]]) -> Dict[str, Any] | None:
    if selected is None:
        return None
    stop_id = sha8({
        "unit": UNIT_ID,
        "selected_group": selected["group_key"],
        "stop": "STOP_CAPABILITY_LAYER_REQUIRED",
    })
    return {
        "schema_version": "capability_stop_packet_v0",
        "packet_type": "CAPABILITY_STOP_PACKET",
        "stop_id": stop_id,
        "source_surface_id": records[-1]["surface_id"],
        "source_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "pressure_group_key": selected["group_key"],
        "surface_type": "capability_stop_surface",
        "missing_object_type": "capability_boundary_unknown",
        "required_capability": "CURRENT_SURFACE_GROUP_SPECIFIC_INSPECTION_CAPABILITY",
        "capability_available": False,
        "why_current_capability_cannot_continue": "the frozen current-surface protocol can select the next remaining R1000 pressure group, but this unit is not authorized to execute a group-specific inspection/repair path or to infer capability coverage for the selected group",
        "evidence_already_collected": {
            "queue_materialized": True,
            "closed_branch_excluded": True,
            "selected_group_row_count": selected["row_count"],
            "selected_group": selected["group_key"],
        },
        "authority_guards": {
            "value_invention_count": 0,
            "source_mutation_count": 0,
            "receipt_mutation_count": 0,
            "taxonomy_action_count": 0,
            "next_group_auto_opened_count": 0,
            "hidden_next_command_count": 0,
        },
        "safe_human_choices": [
            "AUTHORIZE_GROUP_SPECIFIC_INSPECTION_CAPABILITY",
            "REQUEST_NARROWER_SELECTED_GROUP_INSPECTION_PLAN",
            "RETURN_TO_PRESSURE_QUEUE",
            "REJECT_CAPABILITY_STOP_AS_INSUFFICIENT",
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CAPABILITY_LAYER_REQUIRED",
            "next_command_goal": None,
        },
    }

def build_report(queue_summary: Dict[str, Any], selected_packet: Dict[str, Any], trace: Dict[str, Any], capability_packet: Dict[str, Any] | None) -> Dict[str, Any]:
    selected = selected_packet.get("selected") is True
    return {
        "schema_version": "r1000_current_surface_pressure_loop_application_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "total_pressure_row_count": queue_summary["total_pressure_row_count"],
        "total_group_count": queue_summary["total_group_count"],
        "closed_group_count": queue_summary["closed_group_count"],
        "open_group_count": queue_summary["open_group_count"],
        "selected_group_count": 1 if selected else 0,
        "selected_group_row_count": selected_packet.get("selected_group", {}).get("row_count", 0) if selected else 0,
        "closed_branch_excluded_count": queue_summary["closed_group_count"],
        "surface_state_records_emitted_count": 3 if selected else 2,
        "transition_trace_emitted_count": 1,
        "capability_stop_packet_emitted_count": 1 if capability_packet is not None else 0,
        "capability_stop_required": capability_packet is not None,
        "capability_stop_code": None if capability_packet is None else capability_packet["terminal"]["stop_code"],
        "r1000_run_executed_count": 0,
        "group_specific_inspection_executed_count": 0,
        "repair_executed_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": "AUTHORIZE_GROUP_SPECIFIC_INSPECTION_CAPABILITY_OR_REQUEST_NARROWER_SELECTED_GROUP_INSPECTION_PLAN" if selected else "RETURN_TO_PRESSURE_QUEUE",
    }

def validate_outputs(queue_summary: Dict[str, Any], records: List[Dict[str, Any]], selected_packet: Dict[str, Any], trace: Dict[str, Any], capability_packet: Dict[str, Any] | None, report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if queue_summary["total_pressure_row_count"] <= 0:
        failures.append("queue_row_count_not_positive")
    if queue_summary["closed_group_count"] < 1:
        failures.append("closed_group_not_detected")
    if "38c604a1" not in queue_summary["closed_pressure_group_key_hashes"]:
        failures.append("closed_group_hash_missing")
    if selected_packet["selected"] is True and selected_packet["selected_group"]["row_count"] <= 0:
        failures.append("selected_group_row_count_not_positive")
    if capability_packet is None and selected_packet["selected"] is True:
        failures.append("capability_stop_missing_for_selected_group")
    if capability_packet is not None:
        if capability_packet["terminal"]["stop_code"] != "STOP_CAPABILITY_LAYER_REQUIRED":
            failures.append("capability_stop_code_wrong")
        if capability_packet["terminal"]["next_command_goal"] is not None:
            failures.append("capability_stop_next_not_null")
        if capability_packet["capability_available"] is not False:
            failures.append("capability_available_not_false")
        for key in [
            "value_invention_count",
            "source_mutation_count",
            "receipt_mutation_count",
            "taxonomy_action_count",
            "next_group_auto_opened_count",
            "hidden_next_command_count",
        ]:
            if capability_packet["authority_guards"].get(key) != 0:
                failures.append(f"capability_packet_guard_not_zero:{key}:{capability_packet['authority_guards'].get(key)}")
    if trace["terminal"]["type"] != "STOP":
        failures.append("trace_terminal_not_stop")
    if selected_packet["selected"] is True and trace["terminal"]["stop_code"] != "STOP_CAPABILITY_LAYER_REQUIRED":
        failures.append("trace_stop_wrong_for_selected_group")
    if report["r1000_run_executed_count"] != 0:
        failures.append("report_r1000_run_executed")
    for key in [
        "group_specific_inspection_executed_count",
        "repair_executed_count",
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_count_not_zero:{key}:{report.get(key)}")
    for record in records:
        authority = record["authority_state"]
        for key in [
            "source_mutation_count",
            "receipt_mutation_count",
            "taxonomy_action_count",
            "hidden_next_command_count",
            "next_group_auto_opened_count",
        ]:
            if authority.get(key) != 0:
                failures.append(f"surface_authority_not_zero:{key}:{authority.get(key)}")
    return failures

def validate_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != UNIT_ID:
        failures.append("unit_id_wrong")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append("target_unit_wrong")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "R1000_CURRENT_SURFACE_0_PROTOCOL_CONSUMED",
        "R1000_CURRENT_SURFACE_1_QUEUE_MATERIALIZED",
        "R1000_CURRENT_SURFACE_2_CLOSED_BRANCH_EXCLUDED",
        "R1000_CURRENT_SURFACE_3_SURFACE_RECORDS_EMITTED",
        "R1000_CURRENT_SURFACE_4_SELECTED_GROUP_IDENTIFIED_OR_EMPTY_QUEUE_STOP",
        "R1000_CURRENT_SURFACE_5_TRANSITION_TRACE_EMITTED",
        "R1000_CURRENT_SURFACE_6_CAPABILITY_STOP_EMITTED_FOR_UNKNOWN_CAPABILITY",
        "R1000_CURRENT_SURFACE_7_NO_R1000_RUN_OR_REPAIR_EXECUTED",
        "R1000_CURRENT_SURFACE_8_NO_VALUE_OR_TAXONOMY_ACTION",
        "R1000_CURRENT_SURFACE_9_NO_SOURCE_OR_RECEIPT_MUTATION",
        "R1000_CURRENT_SURFACE_10_NO_NEXT_GROUP_AUTO_OPEN",
        "R1000_CURRENT_SURFACE_11_NO_HIDDEN_NEXT_COMMAND",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("total_pressure_row_count", 0) <= 0:
        failures.append("metric_total_pressure_rows_not_positive")
    if metrics.get("closed_branch_excluded_count", 0) < 1:
        failures.append("metric_closed_branch_not_excluded")
    if metrics.get("selected_group_count") not in [0, 1]:
        failures.append("metric_selected_group_count_invalid")
    if metrics.get("selected_group_count") == 1 and metrics.get("capability_stop_packet_emitted_count") != 1:
        failures.append("metric_capability_stop_missing")
    if metrics.get("r1000_run_executed_count") != 0:
        failures.append("metric_r1000_run_executed")
    for key in [
        "group_specific_inspection_executed_count",
        "repair_executed_count",
        "field_value_invention_count",
        "taxonomy_label_creation_count",
        "taxonomy_upgrade_authorized_count",
        "taxonomy_delta_proposal_emitted_count",
        "source_mutation_count",
        "existing_receipt_mutation_count",
        "next_group_auto_opened_count",
        "hidden_next_command_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    if metrics.get("selected_group_count") == 1 and terminal.get("stop_code") != "STOP_CAPABILITY_LAYER_REQUIRED":
        failures.append(f"terminal_stop_wrong_for_selected_group:{terminal}")
    if metrics.get("selected_group_count") == 0 and terminal.get("stop_code") != "STOP_NO_ACTIONABLE_PRESSURE":
        failures.append(f"terminal_stop_wrong_for_empty_queue:{terminal}")

    return failures

def main() -> int:
    source_before = snapshot_files(SOURCE_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    groups = build_pressure_groups(sources["r1000_pressure_rows"])
    selected = choose_selected_group(groups)
    queue_summary = build_queue_summary(groups, selected)
    records = build_surface_records(queue_summary, selected)
    selected_packet = build_selected_group(selected)
    trace = build_transition_trace(queue_summary, selected)
    capability_packet = build_capability_stop_packet(selected, records)
    report = build_report(queue_summary, selected_packet, trace, capability_packet)

    write_json(QUEUE_SUMMARY_PATH, {k: v for k, v in queue_summary.items() if k != "rows"})
    write_jsonl(SURFACE_RECORDS_PATH, records)
    write_json(SELECTED_GROUP_PATH, selected_packet)
    write_json(TRANSITION_TRACE_PATH, trace)
    if capability_packet is not None:
        write_json(CAPABILITY_STOP_PACKET_PATH, capability_packet)
    write_json(APPLICATION_REPORT_PATH, report)

    failures.extend(validate_outputs(queue_summary, records, selected_packet, trace, capability_packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    selected_count = 1 if selected_packet["selected"] else 0
    capability_stop_count = 1 if capability_packet is not None else 0

    acceptance_gate_results = {
        "R1000_CURRENT_SURFACE_0_PROTOCOL_CONSUMED": sources["protocol_receipt"]["receipt_id"] == SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID and sources["protocol_receipt"]["gate"] == "PASS",
        "R1000_CURRENT_SURFACE_1_QUEUE_MATERIALIZED": QUEUE_SUMMARY_PATH.exists() and queue_summary["total_pressure_row_count"] > 0,
        "R1000_CURRENT_SURFACE_2_CLOSED_BRANCH_EXCLUDED": queue_summary["closed_group_count"] >= 1 and "38c604a1" in queue_summary["closed_pressure_group_key_hashes"],
        "R1000_CURRENT_SURFACE_3_SURFACE_RECORDS_EMITTED": SURFACE_RECORDS_PATH.exists() and len(records) >= 2,
        "R1000_CURRENT_SURFACE_4_SELECTED_GROUP_IDENTIFIED_OR_EMPTY_QUEUE_STOP": selected_count in [0, 1],
        "R1000_CURRENT_SURFACE_5_TRANSITION_TRACE_EMITTED": TRANSITION_TRACE_PATH.exists() and trace["terminal"]["type"] == "STOP",
        "R1000_CURRENT_SURFACE_6_CAPABILITY_STOP_EMITTED_FOR_UNKNOWN_CAPABILITY": (selected_count == 0 and capability_stop_count == 0) or (selected_count == 1 and capability_stop_count == 1 and capability_packet["terminal"]["stop_code"] == "STOP_CAPABILITY_LAYER_REQUIRED"),
        "R1000_CURRENT_SURFACE_7_NO_R1000_RUN_OR_REPAIR_EXECUTED": report["r1000_run_executed_count"] == 0 and report["repair_executed_count"] == 0,
        "R1000_CURRENT_SURFACE_8_NO_VALUE_OR_TAXONOMY_ACTION": report["field_value_invention_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0 and report["taxonomy_upgrade_authorized_count"] == 0,
        "R1000_CURRENT_SURFACE_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "R1000_CURRENT_SURFACE_10_NO_NEXT_GROUP_AUTO_OPEN": report["next_group_auto_opened_count"] == 0,
        "R1000_CURRENT_SURFACE_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_CAPABILITY_LAYER_REQUIRED" if selected_count == 1 else "STOP_NO_ACTIONABLE_PRESSURE",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if any([
        report["r1000_run_executed_count"],
        report["group_specific_inspection_executed_count"],
        report["repair_executed_count"],
        report["field_value_invention_count"],
        report["taxonomy_label_creation_count"],
        report["taxonomy_upgrade_authorized_count"],
        report["taxonomy_delta_proposal_emitted_count"],
        report["source_mutation_count"],
        report["existing_receipt_mutation_count"],
        report["next_group_auto_opened_count"],
        report["hidden_next_command_count"],
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "source_pressure_loop_application_receipt_id": SOURCE_PRESSURE_LOOP_APPLICATION_RECEIPT_ID,
        "total_pressure_row_count": queue_summary["total_pressure_row_count"],
        "total_group_count": queue_summary["total_group_count"],
        "closed_group_count": queue_summary["closed_group_count"],
        "open_group_count": queue_summary["open_group_count"],
        "closed_branch_excluded_count": queue_summary["closed_group_count"],
        "selected_group_count": selected_count,
        "selected_group_row_count": report["selected_group_row_count"],
        "surface_state_records_emitted_count": len(records),
        "transition_trace_emitted_count": 1,
        "capability_stop_packet_emitted_count": capability_stop_count,
        "capability_stop_required": capability_stop_count == 1,
        "capability_stop_code": None if capability_packet is None else capability_packet["terminal"]["stop_code"],
        "r1000_run_executed_count": 0,
        "group_specific_inspection_executed_count": 0,
        "repair_executed_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": report["recommended_next_handling"],
    }

    if selected is not None:
        aggregate_metrics["selected_group_key"] = selected["group_key"]
        aggregate_metrics["selected_group_hash_candidates"] = selected["group_hash_candidates"]

    guards = {
        "protocol_consumed": True,
        "queue_materialized": True,
        "closed_branch_excluded": queue_summary["closed_group_count"] >= 1,
        "selected_group_identified": selected_count == 1,
        "capability_stop_emitted": capability_stop_count == 1,
        "r1000_run_executed": False,
        "group_specific_inspection_executed": False,
        "repair_executed": False,
        "values_invented": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "next_group_auto_opened": False,
        "hidden_next_command": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_protocol": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "selected_group": selected_packet,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "r1000_current_surface_pressure_queue_summary": rel(QUEUE_SUMMARY_PATH),
        "r1000_current_surface_state_records": rel(SURFACE_RECORDS_PATH),
        "r1000_current_surface_selected_pressure_group": rel(SELECTED_GROUP_PATH),
        "r1000_current_surface_transition_trace": rel(TRANSITION_TRACE_PATH),
        "r1000_current_surface_pressure_loop_application_report": rel(APPLICATION_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }
    if capability_packet is not None:
        output_artifacts["r1000_current_surface_capability_stop_packet"] = rel(CAPABILITY_STOP_PACKET_PATH)

    receipt = {
        "schema_version": "current_surface_pressure_loop_r1000_application_receipt_v0",
        "receipt_type": "CURRENT_SURFACE_PRESSURE_LOOP_R1000_APPLICATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "source_top_group_classification_receipt_id": SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID,
        "source_pressure_loop_application_receipt_id": SOURCE_PRESSURE_LOOP_APPLICATION_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "r1000_current_surface_application_summary": {
            "total_pressure_row_count": queue_summary["total_pressure_row_count"],
            "total_group_count": queue_summary["total_group_count"],
            "closed_group_count": queue_summary["closed_group_count"],
            "open_group_count": queue_summary["open_group_count"],
            "selected_group_count": selected_count,
            "selected_group": None if selected is None else selected["group_key"],
            "selected_group_row_count": report["selected_group_row_count"],
            "capability_stop_required": capability_stop_count == 1,
            "capability_stop_code": None if capability_packet is None else capability_packet["terminal"]["stop_code"],
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "r1000_current_surface_application_guards": guards,
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
    print(f"r1000_current_surface_application_receipt_id={receipt_id}")
    print(f"r1000_current_surface_application_receipt_path=data/current_surface_pressure_loop_r1000_application_v0_receipts/{receipt_id}.json")
    print(f"r1000_current_surface_selected_group_path=data/current_surface_pressure_loop_r1000_application_v0/r1000_current_surface_selected_pressure_group.json")
    print(f"r1000_current_surface_capability_stop_packet_path=data/current_surface_pressure_loop_r1000_application_v0/r1000_current_surface_capability_stop_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
