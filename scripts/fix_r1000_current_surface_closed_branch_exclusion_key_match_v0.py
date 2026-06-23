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

UNIT_ID = "FIX_R1000_CURRENT_SURFACE_CLOSED_BRANCH_EXCLUSION_KEY_MATCH_V0"
TARGET_UNIT_ID = "r1000_current_surface_closed_branch_exclusion_key_match_fix.v0"

SOURCE_FAILED_R1000_CURRENT_SURFACE_RECEIPT_ID = "7ae5e47f"
SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID = "e3371951"
SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID = "a121ff40"
SOURCE_TOP_GROUP_CLASSIFICATION_RECEIPT_ID = "7c9718e0"
SOURCE_PRESSURE_LOOP_APPLICATION_RECEIPT_ID = "be19f438"
SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID = "6148b4fa"

CLOSED_BRANCH_SOURCE_HASH = "38c604a1"
EXPECTED_CLOSED_BRANCH_RESOLUTION = "EXPECTED_SOURCE_CONTENT_LIMIT_MARKED_NO_VALUE_OR_TAXONOMY_REPAIR_AUTHORIZED"

FIX_OUT_DIR = ROOT / "data" / "r1000_current_surface_closed_branch_exclusion_key_match_fix_v0"
FIX_RECEIPT_DIR = ROOT / "data" / "r1000_current_surface_closed_branch_exclusion_key_match_fix_v0_receipts"

APP_OUT_DIR = ROOT / "data" / "current_surface_pressure_loop_r1000_application_fixed_v0"
APP_RECEIPT_DIR = ROOT / "data" / "current_surface_pressure_loop_r1000_application_fixed_v0_receipts"

CLOSED_BRANCH_IDENTITY_MAP_PATH = FIX_OUT_DIR / "closed_branch_identity_map.json"
CLOSED_BRANCH_MATCH_AUDIT_PATH = FIX_OUT_DIR / "closed_branch_match_audit.json"
FIX_REPORT_PATH = FIX_OUT_DIR / "closed_branch_exclusion_key_match_fix_report.json"

QUEUE_SUMMARY_PATH = APP_OUT_DIR / "r1000_current_surface_pressure_queue_summary.json"
SURFACE_RECORDS_PATH = APP_OUT_DIR / "r1000_current_surface_state_records.jsonl"
SELECTED_GROUP_PATH = APP_OUT_DIR / "r1000_current_surface_selected_pressure_group.json"
TRANSITION_TRACE_PATH = APP_OUT_DIR / "r1000_current_surface_transition_trace.json"
CAPABILITY_STOP_PACKET_PATH = APP_OUT_DIR / "r1000_current_surface_capability_stop_packet.json"
APPLICATION_REPORT_PATH = APP_OUT_DIR / "r1000_current_surface_pressure_loop_application_report.json"

FAILED_RECEIPT_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_v0_receipts" / f"{SOURCE_FAILED_R1000_CURRENT_SURFACE_RECEIPT_ID}.json"
FAILED_SELECTED_GROUP_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_v0" / "r1000_current_surface_selected_pressure_group.json"
FAILED_CAPABILITY_STOP_PACKET_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_v0" / "r1000_current_surface_capability_stop_packet.json"

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

TRACKED_SOURCE_FILES = [
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

LOCAL_FAILED_FILES = [
    FAILED_RECEIPT_PATH,
    FAILED_SELECTED_GROUP_PATH,
    FAILED_CAPABILITY_STOP_PACKET_PATH,
]

HUMAN_DECISION = {
    "decision": "FIX_R1000_CURRENT_SURFACE_CLOSED_BRANCH_EXCLUSION_KEY_MATCH",
    "scope": "repair closed-branch exclusion by adding explicit semantic-tuple identity matching between the expected-limit closure and R1000 pressure queue groups, then rerun the current-surface application without running R1000 or executing group-specific inspection",
    "source_failed_r1000_current_surface_receipt_id": SOURCE_FAILED_R1000_CURRENT_SURFACE_RECEIPT_ID,
    "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
    "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
    "authorized": [
        "derive closed-branch semantic identity from failed selection and closure receipts",
        "emit closed-branch identity map",
        "exclude matching closed branch by semantic tuple",
        "rerun current-surface queue application on existing tracked R1000 rows",
        "emit capability-stop packet for next remaining group if capability is unknown",
    ],
    "not_authorized": [
        "running new R1000 pressure generation",
        "executing group-specific inspection",
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

def load_sources() -> Dict[str, Any]:
    return {
        "failed_receipt": read_json(FAILED_RECEIPT_PATH),
        "failed_selected_group": read_json(FAILED_SELECTED_GROUP_PATH),
        "failed_capability_stop_packet": read_json(FAILED_CAPABILITY_STOP_PACKET_PATH),
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
    failed = sources["failed_receipt"]
    failed_metrics = failed.get("aggregate_metrics", {})
    expected = sources["expected_limit_receipt"]
    expected_metrics = expected.get("aggregate_metrics", {})
    protocol = sources["protocol_receipt"]

    if failed.get("receipt_id") != SOURCE_FAILED_R1000_CURRENT_SURFACE_RECEIPT_ID:
        failures.append("failed_receipt_id_wrong")
    if failed.get("gate") != "FAIL":
        failures.append("failed_receipt_not_fail")
    if "closed_group_not_detected" not in failed.get("failures", []):
        failures.append("failed_receipt_not_closed_group_failure")
    if failed_metrics.get("closed_group_count") != 0:
        failures.append("failed_receipt_closed_group_count_not_zero")
    if failed_metrics.get("selected_group_count") != 1:
        failures.append("failed_receipt_did_not_select_group")
    if failed_metrics.get("selected_group_row_count") != 25:
        failures.append("failed_receipt_selected_group_count_not_25")

    selected_group = failed_metrics.get("selected_group_key", {})
    if not selected_group:
        failures.append("failed_receipt_missing_selected_group_key")

    if expected.get("receipt_id") != SOURCE_EXPECTED_LIMIT_RECEIPT_ID:
        failures.append("expected_limit_receipt_id_wrong")
    if expected.get("gate") != "PASS":
        failures.append("expected_limit_not_pass")
    if expected_metrics.get("branch_closed") is not True:
        failures.append("expected_limit_branch_not_closed")
    if expected_metrics.get("expected_limit_marked") is not True:
        failures.append("expected_limit_not_marked")
    if expected_metrics.get("pressure_group_key_hash") != CLOSED_BRANCH_SOURCE_HASH:
        failures.append("expected_limit_pressure_group_hash_wrong")
    if expected_metrics.get("branch_resolution") != EXPECTED_CLOSED_BRANCH_RESOLUTION:
        failures.append("expected_limit_branch_resolution_wrong")

    if protocol.get("receipt_id") != SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID:
        failures.append("protocol_receipt_id_wrong")
    if protocol.get("gate") != "PASS":
        failures.append("protocol_not_pass")
    if protocol.get("aggregate_metrics", {}).get("capability_stop_defined") is not True:
        failures.append("protocol_capability_stop_missing")

    for path in TRACKED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")
    for path in LOCAL_FAILED_FILES:
        if not path.exists():
            failures.append(f"local_failed_artifact_missing:{rel(path)}")

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

def normalize_group_key_dict(group_key: Dict[str, Any]) -> Dict[str, str]:
    return {
        "parent_pressure_class": str(group_key.get("parent_pressure_class", "UNKNOWN_PARENT")),
        "pressure_subtype": str(group_key.get("pressure_subtype", "UNKNOWN_SUBTYPE")),
        "halt_reason": str(group_key.get("halt_reason", "UNKNOWN_HALT")),
    }

def key_dict_to_tuple(group_key: Dict[str, Any]) -> Tuple[str, str, str]:
    norm = normalize_group_key_dict(group_key)
    return norm["parent_pressure_class"], norm["pressure_subtype"], norm["halt_reason"]

def group_key_hash(group_key: Tuple[str, str, str]) -> str:
    return sha8({
        "parent_pressure_class": group_key[0],
        "pressure_subtype": group_key[1],
        "halt_reason": group_key[2],
    })

def build_pressure_groups(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    grouped: Dict[Tuple[str, str, str], List[Tuple[int, Dict[str, Any]]]] = defaultdict(list)
    for index, row in enumerate(rows):
        grouped[group_key_tuple(row)].append((index, row))

    groups = []
    for key, indexed_rows in grouped.items():
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
            "semantic_tuple": list(key),
            "group_hash_candidates": hashes,
            "row_count": len(indexed_rows),
            "sample_row_refs": [
                {
                    "row_index": row_index,
                    "work_item_id": first_existing(row, ["work_item_id", "item_id", "case_id", "id"], None),
                    "receipt_id": first_existing(row, ["receipt_id", "source_receipt_id"], None),
                }
                for row_index, row in indexed_rows[:3]
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

def derive_closed_branch_identity_map(sources: Dict[str, Any], groups: List[Dict[str, Any]]) -> Dict[str, Any]:
    failed_selected_key = sources["failed_receipt"]["aggregate_metrics"]["selected_group_key"]
    closed_semantic_tuple = key_dict_to_tuple(failed_selected_key)
    closed_group_matches = [g for g in groups if tuple(g["semantic_tuple"]) == closed_semantic_tuple]

    return {
        "schema_version": "r1000_current_surface_closed_branch_identity_map_v0",
        "source_failed_r1000_current_surface_receipt_id": SOURCE_FAILED_R1000_CURRENT_SURFACE_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "closed_branch_source_hash": CLOSED_BRANCH_SOURCE_HASH,
        "closed_branch_resolution": EXPECTED_CLOSED_BRANCH_RESOLUTION,
        "identity_match_rule": "source_hash_plus_semantic_tuple_from_failed_selection",
        "closed_branch_semantic_key": normalize_group_key_dict(failed_selected_key),
        "closed_branch_semantic_tuple": list(closed_semantic_tuple),
        "matched_group_count": len(closed_group_matches),
        "matched_groups": [
            {
                "group_key": g["group_key"],
                "semantic_tuple": g["semantic_tuple"],
                "group_hash_candidates": g["group_hash_candidates"],
                "row_count": g["row_count"],
            }
            for g in closed_group_matches
        ],
        "non_goal": "does_not_redefine_global_group_hashing",
    }

def is_closed_group(group: Dict[str, Any], identity_map: Dict[str, Any]) -> bool:
    if CLOSED_BRANCH_SOURCE_HASH in group.get("group_hash_candidates", {}).values():
        return True
    return list(group["semantic_tuple"]) == identity_map["closed_branch_semantic_tuple"]

def choose_selected_group(groups: List[Dict[str, Any]], identity_map: Dict[str, Any]) -> Dict[str, Any] | None:
    for group in groups:
        if not is_closed_group(group, identity_map):
            return group
    return None

def build_queue_summary(groups: List[Dict[str, Any]], identity_map: Dict[str, Any], selected: Dict[str, Any] | None) -> Dict[str, Any]:
    closed = [g for g in groups if is_closed_group(g, identity_map)]
    open_groups = [g for g in groups if not is_closed_group(g, identity_map)]
    return {
        "schema_version": "r1000_current_surface_pressure_queue_summary_fixed_v0",
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_failed_r1000_current_surface_receipt_id": SOURCE_FAILED_R1000_CURRENT_SURFACE_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "total_group_count": len(groups),
        "total_pressure_row_count": sum(g["row_count"] for g in groups),
        "closed_group_count": len(closed),
        "open_group_count": len(open_groups),
        "closed_branch_exclusion_rule": identity_map["identity_match_rule"],
        "closed_pressure_group_key_hashes": [CLOSED_BRANCH_SOURCE_HASH],
        "closed_groups": [
            {
                "group_key": g["group_key"],
                "semantic_tuple": g["semantic_tuple"],
                "group_hash_candidates": g["group_hash_candidates"],
                "row_count": g["row_count"],
                "closure_reason": EXPECTED_CLOSED_BRANCH_RESOLUTION,
            }
            for g in closed
        ],
        "open_groups": [
            {
                "group_key": g["group_key"],
                "semantic_tuple": g["semantic_tuple"],
                "group_hash_candidates": g["group_hash_candidates"],
                "row_count": g["row_count"],
            }
            for g in open_groups
        ],
        "selected_next_group": None if selected is None else {
            "group_key": selected["group_key"],
            "semantic_tuple": selected["semantic_tuple"],
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
            {"surface": "queue_fixed", "source": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID},
            "pressure_queue_surface",
            SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
            "R1000_PRESSURE_QUEUE",
            queue_summary["total_pressure_row_count"],
            "R1000_PRESSURE_QUEUE_MATERIALIZED_WITH_CLOSED_BRANCH_EXCLUSION",
        )
    ]

    records.append(
        surface_record(
            {"surface": "closed_branch_exclusion", "source": SOURCE_EXPECTED_LIMIT_RECEIPT_ID},
            "expected_limit_closure_surface",
            SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
            queue_summary["closed_groups"][0]["group_key"] if queue_summary["closed_groups"] else "NO_CLOSED_GROUP",
            queue_summary["closed_groups"][0]["row_count"] if queue_summary["closed_groups"] else 0,
            "CLOSED_BRANCH_EXCLUDED_BY_SEMANTIC_IDENTITY",
            terminal_type=None,
            stop_code=None,
        )
    )

    if selected is not None:
        records.append(
            surface_record(
                {"surface": "selected_group_after_closed_exclusion", "group": selected["group_key"]},
                "pressure_group_surface",
                SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
                selected["group_key"],
                selected["row_count"],
                "NEXT_REMAINING_PRESSURE_GROUP_SELECTED_FOR_INSPECTION",
            )
        )
        records.append(
            surface_record(
                {"surface": "capability_stop_after_closed_exclusion", "group": selected["group_key"]},
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
                {"surface": "empty_queue_after_closed_exclusion", "source": SOURCE_EXPECTED_LIMIT_RECEIPT_ID},
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
            "schema_version": "r1000_current_surface_selected_pressure_group_fixed_v0",
            "selected": False,
            "selection_reason": "no open pressure group remains after closed-branch semantic exclusion",
        }
    return {
        "schema_version": "r1000_current_surface_selected_pressure_group_fixed_v0",
        "selected": True,
        "selection_policy": "highest_count_remaining_group_after_closed_branch_semantic_exclusion",
        "selection_reason": "closed branch excluded; next remaining group selected but not executed",
        "selected_group": selected,
    }

def build_transition_trace(queue_summary: Dict[str, Any], selected: Dict[str, Any] | None) -> Dict[str, Any]:
    trace = [
        {
            "step": "materialize_pressure_queue",
            "question": "tracked_r1000_pressure_queue_available",
            "answer": True,
            "taken": "apply_closed_branch_exclusion",
        },
        {
            "step": "apply_closed_branch_exclusion",
            "question": "closed_branch_detected_by_semantic_identity",
            "answer": queue_summary["closed_group_count"] >= 1,
            "yes": "select_remaining_pressure_group",
            "no": "STOP_GATE_FAIL",
            "taken": "select_remaining_pressure_group" if queue_summary["closed_group_count"] >= 1 else "STOP_GATE_FAIL",
        },
        {
            "step": "select_remaining_pressure_group",
            "question": "open_pressure_group_exists",
            "answer": selected is not None,
            "yes": "capability_boundary_check",
            "no": "STOP_NO_ACTIONABLE_PRESSURE",
            "taken": "capability_boundary_check" if selected is not None else "STOP_NO_ACTIONABLE_PRESSURE",
        },
    ]
    if selected is not None:
        trace.append({
            "step": "capability_boundary_check",
            "question": "required_next_move_exceeds_current_capability",
            "answer": True,
            "yes": "STOP_CAPABILITY_LAYER_REQUIRED",
            "no": "continue_current_transition",
            "taken": "STOP_CAPABILITY_LAYER_REQUIRED",
        })

    return {
        "schema_version": "r1000_current_surface_transition_trace_fixed_v0",
        "source_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "source_closed_branch_identity_map_ref": rel(CLOSED_BRANCH_IDENTITY_MAP_PATH),
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
    return {
        "schema_version": "capability_stop_packet_v0",
        "packet_type": "CAPABILITY_STOP_PACKET",
        "stop_id": sha8({
            "unit": UNIT_ID,
            "selected_group": selected["group_key"],
            "stop": "STOP_CAPABILITY_LAYER_REQUIRED",
        }),
        "source_surface_id": records[-1]["surface_id"],
        "source_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "pressure_group_key": selected["group_key"],
        "surface_type": "capability_stop_surface",
        "missing_object_type": "capability_boundary_unknown",
        "required_capability": "CURRENT_SURFACE_GROUP_SPECIFIC_INSPECTION_CAPABILITY",
        "capability_available": False,
        "why_current_capability_cannot_continue": "closed branch exclusion is now repaired; the next remaining R1000 pressure group is selected, but group-specific inspection capability is not yet authorized or proven by the current runner",
        "evidence_already_collected": {
            "queue_materialized": True,
            "closed_branch_excluded": True,
            "selected_group_row_count": selected["row_count"],
            "selected_group": selected["group_key"],
            "selected_group_hash_candidates": selected["group_hash_candidates"],
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

def build_match_audit(identity_map: Dict[str, Any], failed_sources: Dict[str, Any], queue_summary: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_current_surface_closed_branch_match_audit_v0",
        "failed_receipt_id": SOURCE_FAILED_R1000_CURRENT_SURFACE_RECEIPT_ID,
        "failed_reason": "closed_branch_not_detected",
        "failed_selected_group_key": failed_sources["failed_receipt"]["aggregate_metrics"]["selected_group_key"],
        "failed_selected_group_hash_candidates": failed_sources["failed_receipt"]["aggregate_metrics"]["selected_group_hash_candidates"],
        "closed_branch_source_hash": CLOSED_BRANCH_SOURCE_HASH,
        "fixed_identity_match_rule": identity_map["identity_match_rule"],
        "closed_group_count_after_fix": queue_summary["closed_group_count"],
        "closed_branch_excluded_count_after_fix": queue_summary["closed_group_count"],
        "open_group_count_after_fix": queue_summary["open_group_count"],
        "match_status": "MATCHED_BY_SEMANTIC_TUPLE",
    }

def build_report(queue_summary: Dict[str, Any], selected_packet: Dict[str, Any], capability_packet: Dict[str, Any] | None) -> Dict[str, Any]:
    selected = selected_packet.get("selected") is True
    return {
        "schema_version": "r1000_current_surface_closed_branch_exclusion_key_match_fix_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_r1000_current_surface_receipt_id": SOURCE_FAILED_R1000_CURRENT_SURFACE_RECEIPT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "closed_branch_source_hash": CLOSED_BRANCH_SOURCE_HASH,
        "closed_branch_identity_map_emitted_count": 1,
        "closed_branch_match_audit_emitted_count": 1,
        "failed_closed_group_count_before": 0,
        "closed_group_count_after_fix": queue_summary["closed_group_count"],
        "closed_branch_excluded_count_after_fix": queue_summary["closed_group_count"],
        "open_group_count_after_fix": queue_summary["open_group_count"],
        "selected_group_count_after_fix": 1 if selected else 0,
        "selected_group_row_count_after_fix": selected_packet.get("selected_group", {}).get("row_count", 0) if selected else 0,
        "capability_stop_packet_emitted_count": 1 if capability_packet is not None else 0,
        "capability_stop_required": capability_packet is not None,
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

def validate_fixed_outputs(identity_map: Dict[str, Any], match_audit: Dict[str, Any], queue_summary: Dict[str, Any], records: List[Dict[str, Any]], selected_packet: Dict[str, Any], trace: Dict[str, Any], capability_packet: Dict[str, Any] | None, report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if identity_map["matched_group_count"] < 1:
        failures.append("closed_branch_identity_no_match")
    if identity_map["closed_branch_source_hash"] != CLOSED_BRANCH_SOURCE_HASH:
        failures.append("closed_branch_source_hash_wrong")
    if queue_summary["closed_group_count"] < 1:
        failures.append("closed_group_not_detected_after_fix")
    if queue_summary["closed_group_count"] != 1:
        failures.append(f"closed_group_count_unexpected:{queue_summary['closed_group_count']}")
    if queue_summary["closed_groups"][0]["row_count"] != 25:
        failures.append(f"closed_group_row_count_unexpected:{queue_summary['closed_groups'][0]['row_count']}")
    if queue_summary["open_group_count"] != queue_summary["total_group_count"] - queue_summary["closed_group_count"]:
        failures.append("open_group_count_inconsistent")
    if selected_packet["selected"] is True and selected_packet["selected_group"]["row_count"] >= 25:
        failures.append("selected_group_appears_to_reselect_closed_top_group")
    if selected_packet["selected"] is True and capability_packet is None:
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
    if match_audit["match_status"] != "MATCHED_BY_SEMANTIC_TUPLE":
        failures.append("match_audit_status_wrong")
    for key in [
        "r1000_run_executed_count",
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
        "CLOSED_BRANCH_FIX_0_FAILED_RECEIPT_CONSUMED",
        "CLOSED_BRANCH_FIX_1_CLOSURE_RECEIPT_CONSUMED",
        "CLOSED_BRANCH_FIX_2_IDENTITY_MAP_EMITTED",
        "CLOSED_BRANCH_FIX_3_SEMANTIC_MATCH_DETECTED",
        "CLOSED_BRANCH_FIX_4_CLOSED_BRANCH_EXCLUDED",
        "CLOSED_BRANCH_FIX_5_RERUN_QUEUE_APPLICATION_FIXED",
        "CLOSED_BRANCH_FIX_6_CAPABILITY_STOP_EMITTED_FOR_NEXT_GROUP",
        "CLOSED_BRANCH_FIX_7_NO_R1000_RUN_OR_REPAIR_EXECUTED",
        "CLOSED_BRANCH_FIX_8_NO_VALUE_OR_TAXONOMY_ACTION",
        "CLOSED_BRANCH_FIX_9_NO_SOURCE_OR_RECEIPT_MUTATION",
        "CLOSED_BRANCH_FIX_10_NO_NEXT_GROUP_AUTO_OPEN",
        "CLOSED_BRANCH_FIX_11_NO_HIDDEN_NEXT_COMMAND",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("closed_group_count_after_fix", 0) < 1:
        failures.append("metric_closed_group_not_fixed")
    if metrics.get("closed_branch_excluded_count_after_fix", 0) < 1:
        failures.append("metric_closed_branch_not_excluded")
    if metrics.get("selected_group_count_after_fix") == 1 and metrics.get("capability_stop_packet_emitted_count") != 1:
        failures.append("metric_capability_stop_missing")
    if metrics.get("selected_group_count_after_fix") == 1 and metrics.get("selected_group_row_count_after_fix", 0) >= 25:
        failures.append("metric_selected_group_reselected_closed_top_group")
    for key in [
        "r1000_run_executed_count",
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
    if metrics.get("selected_group_count_after_fix") == 1 and terminal.get("stop_code") != "STOP_CAPABILITY_LAYER_REQUIRED":
        failures.append(f"terminal_stop_wrong_for_selected_group:{terminal}")
    if metrics.get("selected_group_count_after_fix") == 0 and terminal.get("stop_code") != "STOP_NO_ACTIONABLE_PRESSURE":
        failures.append(f"terminal_stop_wrong_for_empty_queue:{terminal}")
    return failures

def main() -> int:
    source_before = snapshot_files(TRACKED_SOURCE_FILES + LOCAL_FAILED_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    FIX_OUT_DIR.mkdir(parents=True, exist_ok=True)
    FIX_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    APP_OUT_DIR.mkdir(parents=True, exist_ok=True)
    APP_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    groups = build_pressure_groups(sources["r1000_pressure_rows"])
    identity_map = derive_closed_branch_identity_map(sources, groups)
    selected = choose_selected_group(groups, identity_map)
    queue_summary = build_queue_summary(groups, identity_map, selected)
    records = build_surface_records(queue_summary, selected)
    selected_packet = build_selected_group(selected)
    trace = build_transition_trace(queue_summary, selected)
    capability_packet = build_capability_stop_packet(selected, records)
    match_audit = build_match_audit(identity_map, sources, queue_summary)
    report = build_report(queue_summary, selected_packet, capability_packet)

    write_json(CLOSED_BRANCH_IDENTITY_MAP_PATH, identity_map)
    write_json(CLOSED_BRANCH_MATCH_AUDIT_PATH, match_audit)
    write_json(QUEUE_SUMMARY_PATH, queue_summary)
    write_jsonl(SURFACE_RECORDS_PATH, records)
    write_json(SELECTED_GROUP_PATH, selected_packet)
    write_json(TRANSITION_TRACE_PATH, trace)
    if capability_packet is not None:
        write_json(CAPABILITY_STOP_PACKET_PATH, capability_packet)
    write_json(APPLICATION_REPORT_PATH, report)
    write_json(FIX_REPORT_PATH, report)

    failures.extend(validate_fixed_outputs(identity_map, match_audit, queue_summary, records, selected_packet, trace, capability_packet, report))

    source_after = snapshot_files(TRACKED_SOURCE_FILES + LOCAL_FAILED_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    selected_count = 1 if selected_packet["selected"] else 0
    capability_stop_count = 1 if capability_packet is not None else 0

    acceptance_gate_results = {
        "CLOSED_BRANCH_FIX_0_FAILED_RECEIPT_CONSUMED": sources["failed_receipt"]["receipt_id"] == SOURCE_FAILED_R1000_CURRENT_SURFACE_RECEIPT_ID and sources["failed_receipt"]["gate"] == "FAIL",
        "CLOSED_BRANCH_FIX_1_CLOSURE_RECEIPT_CONSUMED": sources["expected_limit_receipt"]["receipt_id"] == SOURCE_EXPECTED_LIMIT_RECEIPT_ID and sources["expected_limit_receipt"]["gate"] == "PASS",
        "CLOSED_BRANCH_FIX_2_IDENTITY_MAP_EMITTED": CLOSED_BRANCH_IDENTITY_MAP_PATH.exists(),
        "CLOSED_BRANCH_FIX_3_SEMANTIC_MATCH_DETECTED": identity_map["matched_group_count"] >= 1,
        "CLOSED_BRANCH_FIX_4_CLOSED_BRANCH_EXCLUDED": queue_summary["closed_group_count"] >= 1,
        "CLOSED_BRANCH_FIX_5_RERUN_QUEUE_APPLICATION_FIXED": QUEUE_SUMMARY_PATH.exists() and queue_summary["closed_group_count"] >= 1,
        "CLOSED_BRANCH_FIX_6_CAPABILITY_STOP_EMITTED_FOR_NEXT_GROUP": (selected_count == 0 and capability_stop_count == 0) or (selected_count == 1 and capability_stop_count == 1),
        "CLOSED_BRANCH_FIX_7_NO_R1000_RUN_OR_REPAIR_EXECUTED": report["r1000_run_executed_count"] == 0 and report["repair_executed_count"] == 0,
        "CLOSED_BRANCH_FIX_8_NO_VALUE_OR_TAXONOMY_ACTION": report["field_value_invention_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0 and report["taxonomy_upgrade_authorized_count"] == 0,
        "CLOSED_BRANCH_FIX_9_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "CLOSED_BRANCH_FIX_10_NO_NEXT_GROUP_AUTO_OPEN": report["next_group_auto_opened_count"] == 0,
        "CLOSED_BRANCH_FIX_11_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0,
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
        "source_failed_r1000_current_surface_receipt_id": SOURCE_FAILED_R1000_CURRENT_SURFACE_RECEIPT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "closed_branch_source_hash": CLOSED_BRANCH_SOURCE_HASH,
        "closed_branch_identity_map_emitted_count": 1,
        "closed_branch_match_audit_emitted_count": 1,
        "failed_closed_group_count_before": 0,
        "closed_group_count_after_fix": queue_summary["closed_group_count"],
        "closed_branch_excluded_count_after_fix": queue_summary["closed_group_count"],
        "open_group_count_after_fix": queue_summary["open_group_count"],
        "total_group_count": queue_summary["total_group_count"],
        "total_pressure_row_count": queue_summary["total_pressure_row_count"],
        "selected_group_count_after_fix": selected_count,
        "selected_group_row_count_after_fix": report["selected_group_row_count_after_fix"],
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
        aggregate_metrics["selected_group_key_after_fix"] = selected["group_key"]
        aggregate_metrics["selected_group_hash_candidates_after_fix"] = selected["group_hash_candidates"]

    guards = {
        "failed_receipt_consumed": True,
        "closure_receipt_consumed": True,
        "identity_map_emitted": True,
        "semantic_match_detected": identity_map["matched_group_count"] >= 1,
        "closed_branch_excluded": queue_summary["closed_group_count"] >= 1,
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
        "source_failed": SOURCE_FAILED_R1000_CURRENT_SURFACE_RECEIPT_ID,
        "identity_map": identity_map,
        "selected_after_fix": selected_packet,
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = FIX_RECEIPT_DIR / f"{receipt_id}.json"

    fixed_application_receipt_seed = {
        "unit_id": "APPLY_CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_TO_R1000_PRESSURE_QUEUE_FIXED_V0",
        "source_fix_receipt_preview": receipt_id,
        "selected_after_fix": selected_packet,
        "terminal": terminal,
    }
    fixed_application_receipt_id = sha8(fixed_application_receipt_seed)
    fixed_application_receipt_path = APP_RECEIPT_DIR / f"{fixed_application_receipt_id}.json"

    output_artifacts = {
        "closed_branch_identity_map": rel(CLOSED_BRANCH_IDENTITY_MAP_PATH),
        "closed_branch_match_audit": rel(CLOSED_BRANCH_MATCH_AUDIT_PATH),
        "closed_branch_exclusion_key_match_fix_report": rel(FIX_REPORT_PATH),
        "r1000_current_surface_pressure_queue_summary_fixed": rel(QUEUE_SUMMARY_PATH),
        "r1000_current_surface_state_records_fixed": rel(SURFACE_RECORDS_PATH),
        "r1000_current_surface_selected_pressure_group_fixed": rel(SELECTED_GROUP_PATH),
        "r1000_current_surface_transition_trace_fixed": rel(TRANSITION_TRACE_PATH),
        "r1000_current_surface_pressure_loop_application_report_fixed": rel(APPLICATION_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "fixed_application_receipt": rel(fixed_application_receipt_path),
    }
    if capability_packet is not None:
        output_artifacts["r1000_current_surface_capability_stop_packet_fixed"] = rel(CAPABILITY_STOP_PACKET_PATH)

    fixed_application_receipt = {
        "schema_version": "current_surface_pressure_loop_r1000_application_fixed_receipt_v0",
        "receipt_type": "CURRENT_SURFACE_PRESSURE_LOOP_R1000_APPLICATION_FIXED_RECEIPT",
        "receipt_id": fixed_application_receipt_id,
        "unit_id": "APPLY_CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_TO_R1000_PRESSURE_QUEUE_FIXED_V0",
        "source_fix_receipt_id": receipt_id,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "output_artifacts": {k: v for k, v in output_artifacts.items() if k.startswith("r1000_current_surface_")},
        "aggregate_metrics": {
            "closed_group_count": queue_summary["closed_group_count"],
            "closed_branch_excluded_count": queue_summary["closed_group_count"],
            "open_group_count": queue_summary["open_group_count"],
            "selected_group_count": selected_count,
            "selected_group_row_count": report["selected_group_row_count_after_fix"],
            "capability_stop_packet_emitted_count": capability_stop_count,
            "r1000_run_executed_count": 0,
            "group_specific_inspection_executed_count": 0,
            "repair_executed_count": 0,
            "field_value_invention_count": 0,
            "taxonomy_delta_proposal_emitted_count": 0,
            "source_mutation_count": 0,
            "next_group_auto_opened_count": 0,
            "hidden_next_command_count": 0,
        },
        "terminal": terminal,
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "created_at": now_iso(),
    }
    write_json(fixed_application_receipt_path, fixed_application_receipt)

    receipt = {
        "schema_version": "r1000_current_surface_closed_branch_exclusion_key_match_fix_receipt_v0",
        "receipt_type": "R1000_CURRENT_SURFACE_CLOSED_BRANCH_EXCLUSION_KEY_MATCH_FIX_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_failed_r1000_current_surface_receipt_id": SOURCE_FAILED_R1000_CURRENT_SURFACE_RECEIPT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_r1000_scale_stability_receipt_id": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "closed_branch_exclusion_fix_summary": {
            "closed_branch_source_hash": CLOSED_BRANCH_SOURCE_HASH,
            "identity_match_rule": identity_map["identity_match_rule"],
            "closed_group_count_after_fix": queue_summary["closed_group_count"],
            "closed_branch_excluded_count_after_fix": queue_summary["closed_group_count"],
            "open_group_count_after_fix": queue_summary["open_group_count"],
            "selected_group_count_after_fix": selected_count,
            "selected_group_after_fix": None if selected is None else selected["group_key"],
            "selected_group_row_count_after_fix": report["selected_group_row_count_after_fix"],
            "capability_stop_required": capability_stop_count == 1,
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "closed_branch_exclusion_fix_guards": guards,
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
        fixed_application_receipt["gate"] = "FAIL"
        fixed_application_receipt["terminal"] = receipt["terminal"]
        fixed_application_receipt["failures"] = failures
        write_json(fixed_application_receipt_path, fixed_application_receipt)

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"closed_branch_exclusion_fix_receipt_id={receipt_id}")
    print(f"closed_branch_exclusion_fix_receipt_path=data/r1000_current_surface_closed_branch_exclusion_key_match_fix_v0_receipts/{receipt_id}.json")
    print(f"r1000_current_surface_fixed_application_receipt_id={fixed_application_receipt_id}")
    print(f"r1000_current_surface_fixed_application_receipt_path=data/current_surface_pressure_loop_r1000_application_fixed_v0_receipts/{fixed_application_receipt_id}.json")
    print(f"r1000_current_surface_fixed_selected_group_path=data/current_surface_pressure_loop_r1000_application_fixed_v0/r1000_current_surface_selected_pressure_group.json")
    print(f"r1000_current_surface_fixed_capability_stop_packet_path=data/current_surface_pressure_loop_r1000_application_fixed_v0/r1000_current_surface_capability_stop_packet.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
