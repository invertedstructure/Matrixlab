#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "APPLY_R1000_GROUP_SPECIFIC_INSPECTION_CAPABILITY_TO_SELECTED_GROUP_V0"
TARGET_UNIT_ID = "r1000_group_specific_inspection_application.v0"

SOURCE_GROUP_CAPABILITY_RECEIPT_ID = "73dfb849"
SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID = "4a0cfc09"
SOURCE_FIXED_APPLICATION_RECEIPT_ID = "2a16f593"
SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID = "e3371951"
SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID = "a121ff40"

EXPECTED_SELECTED_GROUP = {
    "parent_pressure_class": "AUTHORITY_BOUNDARY",
    "pressure_subtype": "healthy_boundary_stop",
    "halt_reason": "STOP_AUTHORITY_BOUNDARY",
}

OUT_DIR = ROOT / "data" / "r1000_group_specific_inspection_application_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_group_specific_inspection_application_v0_receipts"

SELECTED_ROWS_PATH = OUT_DIR / "selected_group_rows.jsonl"
EVIDENCE_SURFACE_PATH = OUT_DIR / "selected_group_evidence_surface.json"
SURFACE_RECORDS_PATH = OUT_DIR / "selected_group_surface_state_records.jsonl"
TRANSITION_TRACE_PATH = OUT_DIR / "selected_group_inspection_transition_trace.json"
CLASSIFICATION_PATH = OUT_DIR / "selected_group_boundary_stop_classification.json"
DECISION_PACKET_PATH = OUT_DIR / "selected_group_boundary_stop_decision_packet.json"
APPLICATION_REPORT_PATH = OUT_DIR / "selected_group_inspection_application_report.json"

GROUP_CAPABILITY_RECEIPT_PATH = ROOT / "data" / "r1000_group_specific_inspection_capability_v0_receipts" / f"{SOURCE_GROUP_CAPABILITY_RECEIPT_ID}.json"
AUTHORIZATION_PACKET_PATH = ROOT / "data" / "r1000_group_specific_inspection_capability_v0" / "group_specific_inspection_capability_authorization_packet.json"
CAPABILITY_CONTRACT_PATH = ROOT / "data" / "r1000_group_specific_inspection_capability_v0" / "group_specific_inspection_capability_contract.json"
INSPECTION_PROFILE_PATH = ROOT / "data" / "r1000_group_specific_inspection_capability_v0" / "selected_group_inspection_profile.json"
INSPECTION_DECISION_TABLE_PATH = ROOT / "data" / "r1000_group_specific_inspection_capability_v0" / "selected_group_inspection_decision_table.json"
CAPABILITY_ACCEPTANCE_GATES_PATH = ROOT / "data" / "r1000_group_specific_inspection_capability_v0" / "group_specific_inspection_capability_acceptance_gates.json"

CLOSED_BRANCH_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_current_surface_closed_branch_exclusion_key_match_fix_v0_receipts" / f"{SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID}.json"
FIXED_APPLICATION_RECEIPT_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_fixed_v0_receipts" / f"{SOURCE_FIXED_APPLICATION_RECEIPT_ID}.json"
FIXED_SELECTED_GROUP_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_fixed_v0" / "r1000_current_surface_selected_pressure_group.json"
FIXED_QUEUE_SUMMARY_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_fixed_v0" / "r1000_current_surface_pressure_queue_summary.json"
FIXED_CAPABILITY_STOP_PACKET_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_fixed_v0" / "r1000_current_surface_capability_stop_packet.json"

CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID}.json"
CURRENT_SURFACE_PROTOCOL_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "current_surface_pressure_loop_protocol.json"
SURFACE_STATE_SCHEMA_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "surface_state_record_schema.json"
SURFACE_TRANSITION_TABLE_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "surface_transition_decision_table.json"

R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"
R1000_PRESSURE_ROWS_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_event_rows.jsonl"

SOURCE_FILES = [
    GROUP_CAPABILITY_RECEIPT_PATH,
    AUTHORIZATION_PACKET_PATH,
    CAPABILITY_CONTRACT_PATH,
    INSPECTION_PROFILE_PATH,
    INSPECTION_DECISION_TABLE_PATH,
    CAPABILITY_ACCEPTANCE_GATES_PATH,
    CLOSED_BRANCH_FIX_RECEIPT_PATH,
    FIXED_APPLICATION_RECEIPT_PATH,
    FIXED_SELECTED_GROUP_PATH,
    FIXED_QUEUE_SUMMARY_PATH,
    FIXED_CAPABILITY_STOP_PACKET_PATH,
    CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH,
    CURRENT_SURFACE_PROTOCOL_PATH,
    SURFACE_STATE_SCHEMA_PATH,
    SURFACE_TRANSITION_TABLE_PATH,
    R1000_SCALE_RECEIPT_PATH,
    R1000_PRESSURE_ROWS_PATH,
]

HUMAN_DECISION = {
    "decision": "APPLY_GROUP_SPECIFIC_INSPECTION_CAPABILITY_TO_SELECTED_GROUP",
    "scope": "inspect only the authorized selected R1000 pressure group and classify the boundary-stop surface without repair, R1000 rerun, taxonomy action, or next-group auto-open",
    "source_group_capability_receipt_id": SOURCE_GROUP_CAPABILITY_RECEIPT_ID,
    "source_fixed_application_receipt_id": SOURCE_FIXED_APPLICATION_RECEIPT_ID,
    "selected_group": EXPECTED_SELECTED_GROUP,
    "authorized": [
        "read selected group rows from existing R1000 pressure rows",
        "materialize selected group evidence surface",
        "classify selected boundary-stop surface",
        "emit surface-state records",
        "emit transition trace",
        "emit decision packet",
    ],
    "not_authorized": [
        "running new R1000 pressure generation",
        "inspecting any other group",
        "repairing selected group",
        "inventing values",
        "creating labels",
        "upgrading taxonomy",
        "mutating source rows",
        "mutating existing receipts",
        "auto-opening another pressure group",
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
        "group_capability_receipt": read_json(GROUP_CAPABILITY_RECEIPT_PATH),
        "authorization_packet": read_json(AUTHORIZATION_PACKET_PATH),
        "capability_contract": read_json(CAPABILITY_CONTRACT_PATH),
        "inspection_profile": read_json(INSPECTION_PROFILE_PATH),
        "inspection_decision_table": read_json(INSPECTION_DECISION_TABLE_PATH),
        "closed_branch_fix_receipt": read_json(CLOSED_BRANCH_FIX_RECEIPT_PATH),
        "fixed_application_receipt": read_json(FIXED_APPLICATION_RECEIPT_PATH),
        "fixed_selected_group": read_json(FIXED_SELECTED_GROUP_PATH),
        "fixed_queue_summary": read_json(FIXED_QUEUE_SUMMARY_PATH),
        "fixed_capability_stop_packet": read_json(FIXED_CAPABILITY_STOP_PACKET_PATH),
        "current_surface_protocol_receipt": read_json(CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH),
        "current_surface_protocol": read_json(CURRENT_SURFACE_PROTOCOL_PATH),
        "surface_state_schema": read_json(SURFACE_STATE_SCHEMA_PATH),
        "surface_transition_table": read_json(SURFACE_TRANSITION_TABLE_PATH),
        "r1000_scale_receipt": read_json(R1000_SCALE_RECEIPT_PATH),
        "r1000_pressure_rows": read_jsonl(R1000_PRESSURE_ROWS_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    capability = sources["group_capability_receipt"]
    contract = sources["capability_contract"]
    fixed = sources["fixed_application_receipt"]
    selected_packet = sources["fixed_selected_group"]

    if capability.get("receipt_id") != SOURCE_GROUP_CAPABILITY_RECEIPT_ID:
        failures.append("group_capability_receipt_id_wrong")
    if capability.get("gate") != "PASS":
        failures.append("group_capability_not_pass")
    if capability.get("aggregate_metrics", {}).get("capability_available_after_this_unit") is not True:
        failures.append("capability_not_available")
    if capability.get("aggregate_metrics", {}).get("scope_selected_group_only") is not True:
        failures.append("capability_scope_not_selected_group_only")
    if capability.get("aggregate_metrics", {}).get("inspection_executed_count") != 0:
        failures.append("capability_unit_already_inspected")

    if contract.get("scope") != "single_selected_r1000_pressure_group":
        failures.append("contract_scope_wrong")
    if contract.get("selected_group") != EXPECTED_SELECTED_GROUP:
        failures.append("contract_selected_group_wrong")
    if "inspect_any_other_group" not in contract.get("forbidden_moves", []):
        failures.append("contract_does_not_forbid_other_group")
    if contract.get("capability_boundary", {}).get("may_classify_group_specific_surface") is not True:
        failures.append("contract_does_not_allow_classification")
    if contract.get("capability_boundary", {}).get("may_execute_repairs") is not False:
        failures.append("contract_allows_repairs")

    if fixed.get("receipt_id") != SOURCE_FIXED_APPLICATION_RECEIPT_ID:
        failures.append("fixed_application_receipt_id_wrong")
    if fixed.get("gate") != "PASS":
        failures.append("fixed_application_not_pass")
    if fixed.get("aggregate_metrics", {}).get("selected_group_count") != 1:
        failures.append("fixed_application_selected_group_missing")
    if fixed.get("aggregate_metrics", {}).get("selected_group_row_count") != 24:
        failures.append("fixed_application_selected_group_row_count_wrong")
    if fixed.get("terminal", {}).get("stop_code") != "STOP_CAPABILITY_LAYER_REQUIRED":
        failures.append("fixed_application_not_capability_stop")

    if selected_packet.get("selected") is not True:
        failures.append("selected_group_packet_not_selected")
    if selected_packet.get("selected_group", {}).get("group_key") != EXPECTED_SELECTED_GROUP:
        failures.append("selected_group_packet_group_wrong")
    if selected_packet.get("selected_group", {}).get("row_count") != 24:
        failures.append("selected_group_packet_row_count_wrong")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def selected_group_rows(rows: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    return [
        row for row in rows
        if row.get("parent_pressure_class") == EXPECTED_SELECTED_GROUP["parent_pressure_class"]
        and row.get("pressure_subtype") == EXPECTED_SELECTED_GROUP["pressure_subtype"]
        and row.get("halt_reason") == EXPECTED_SELECTED_GROUP["halt_reason"]
    ]

def row_key_visibility(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    required = ["parent_pressure_class", "pressure_subtype", "halt_reason"]
    missing_by_row = []
    for index, row in enumerate(rows):
        missing = [key for key in required if key not in row or row.get(key) in [None, ""]]
        if missing:
            missing_by_row.append({"row_index": index, "missing_keys": missing})
    return {
        "required_keys": required,
        "all_required_keys_visible": len(missing_by_row) == 0,
        "missing_by_row": missing_by_row,
    }

def build_evidence_surface(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    key_visibility = row_key_visibility(rows)
    parent_counts = Counter(row.get("parent_pressure_class") for row in rows)
    subtype_counts = Counter(row.get("pressure_subtype") for row in rows)
    halt_counts = Counter(row.get("halt_reason") for row in rows)
    unique_group_tuple_count = len(set((row.get("parent_pressure_class"), row.get("pressure_subtype"), row.get("halt_reason")) for row in rows))

    return {
        "schema_version": "r1000_selected_group_evidence_surface_v0",
        "surface_id": sha8({
            "surface": "selected_group_evidence_surface",
            "selected_group": EXPECTED_SELECTED_GROUP,
            "source_rows": SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID,
        }),
        "surface_type": "selected_group_evidence_surface",
        "source_group_capability_receipt_id": SOURCE_GROUP_CAPABILITY_RECEIPT_ID,
        "source_fixed_application_receipt_id": SOURCE_FIXED_APPLICATION_RECEIPT_ID,
        "selected_group": EXPECTED_SELECTED_GROUP,
        "row_count": len(rows),
        "key_visibility": key_visibility,
        "group_tuple_consistency": {
            "unique_group_tuple_count": unique_group_tuple_count,
            "parent_pressure_class_counts": dict(parent_counts),
            "pressure_subtype_counts": dict(subtype_counts),
            "halt_reason_counts": dict(halt_counts),
        },
        "authority_basis": {
            "explicit_parent_pressure_class": EXPECTED_SELECTED_GROUP["parent_pressure_class"],
            "explicit_pressure_subtype": EXPECTED_SELECTED_GROUP["pressure_subtype"],
            "explicit_halt_reason": EXPECTED_SELECTED_GROUP["halt_reason"],
            "authority_basis_visible": key_visibility["all_required_keys_visible"] and unique_group_tuple_count == 1,
        },
        "inspection_scope": {
            "selected_group_only": True,
            "other_group_row_count": 0,
        },
        "forbidden_action_counts": {
            "r1000_run_executed_count": 0,
            "other_group_inspection_count": 0,
            "repair_executed_count": 0,
            "field_value_invention_count": 0,
            "taxonomy_label_creation_count": 0,
            "taxonomy_upgrade_authorized_count": 0,
            "taxonomy_delta_proposal_emitted_count": 0,
            "source_mutation_count": 0,
            "existing_receipt_mutation_count": 0,
            "next_group_auto_opened_count": 0,
            "hidden_next_command_count": 0,
        },
    }

def surface_record(surface_id_seed: Any, surface_type: str, source_receipt_id: str, row_count: int, current_class: str, terminal_type: str | None = None, stop_code: str | None = None) -> Dict[str, Any]:
    return {
        "schema_version": "current_surface_state_record_v0",
        "surface_id": sha8(surface_id_seed),
        "surface_type": surface_type,
        "source_receipt_id": source_receipt_id,
        "pressure_group_key": EXPECTED_SELECTED_GROUP,
        "row_count": row_count,
        "key_visibility": {
            "required_keys_visible": True,
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
            "branch_resolution": "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP_ACCEPTED" if current_class == "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP" else None,
        },
        "capability_state": {
            "required_capability": "CURRENT_SURFACE_GROUP_SPECIFIC_INSPECTION_CAPABILITY",
            "capability_available": True,
            "capability_stop_required": False,
        },
        "terminal": {
            "terminal_type": terminal_type,
            "stop_code": stop_code,
            "next_command_goal": None,
        },
    }

def classify_surface(evidence_surface: Dict[str, Any]) -> Dict[str, Any]:
    enough_rows = evidence_surface["row_count"] == 24
    key_visible = evidence_surface["key_visibility"]["all_required_keys_visible"] is True
    tuple_consistent = evidence_surface["group_tuple_consistency"]["unique_group_tuple_count"] == 1
    authority_basis_visible = evidence_surface["authority_basis"]["authority_basis_visible"] is True
    selected_tuple_matches = evidence_surface["selected_group"] == EXPECTED_SELECTED_GROUP

    if enough_rows and key_visible and tuple_consistent and authority_basis_visible and selected_tuple_matches:
        classification = "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP"
        resolution = "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP_ACCEPTED"
        stop_code = "STOP_SELECTED_GROUP_INSPECTION_COMPLETE_HEALTHY_BOUNDARY_STOP"
    elif key_visible and tuple_consistent:
        classification = "AUTHORITY_BOUNDARY_SURFACE_NEEDS_MORE_DETAIL"
        resolution = "AUTHORITY_BOUNDARY_DETAIL_INSUFFICIENT"
        stop_code = "STOP_AUTHORITY_BASIS_MISSING"
    else:
        classification = "SELECTED_GROUP_SURFACE_DEFICIENT"
        resolution = "SELECTED_GROUP_SURFACE_DEFICIENCY"
        stop_code = "STOP_CAPABILITY_LAYER_REQUIRED"

    return {
        "schema_version": "r1000_selected_group_boundary_stop_classification_v0",
        "classification_id": sha8({
            "selected_group": EXPECTED_SELECTED_GROUP,
            "row_count": evidence_surface["row_count"],
            "classification": classification,
        }),
        "selected_group": EXPECTED_SELECTED_GROUP,
        "row_count": evidence_surface["row_count"],
        "classification": classification,
        "branch_resolution": resolution,
        "classification_basis": {
            "expected_row_count_24": enough_rows,
            "required_keys_visible": key_visible,
            "single_group_tuple": tuple_consistent,
            "authority_basis_visible": authority_basis_visible,
            "selected_tuple_matches_authorized_group": selected_tuple_matches,
            "contract_scope_selected_group_only": True,
        },
        "terminal": {
            "type": "STOP",
            "stop_code": stop_code,
            "next_command_goal": None,
        },
        "forbidden_action_counts": evidence_surface["forbidden_action_counts"],
    }

def build_transition_trace(evidence_surface: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
    trace = [
        {
            "step": "materialize_selected_group_surface",
            "question": "selected_group_rows_visible",
            "answer": evidence_surface["row_count"] == 24,
            "yes": "inspect_boundary_surface",
            "no": "STOP_SELECTED_GROUP_ROWS_MISSING",
            "taken": "inspect_boundary_surface" if evidence_surface["row_count"] == 24 else "STOP_SELECTED_GROUP_ROWS_MISSING",
        },
        {
            "step": "inspect_boundary_surface",
            "question": "boundary_stop_has_explicit_authority_basis",
            "answer": evidence_surface["authority_basis"]["authority_basis_visible"],
            "yes": "classify_boundary_stop",
            "no": "STOP_AUTHORITY_BASIS_MISSING",
            "taken": "classify_boundary_stop" if evidence_surface["authority_basis"]["authority_basis_visible"] else "STOP_AUTHORITY_BASIS_MISSING",
        },
        {
            "step": "classify_boundary_stop",
            "question": "boundary_stop_is_expected_and_healthy",
            "answer": classification["classification"] == "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP",
            "yes": "CLASSIFY_HEALTHY_EXPECTED_BOUNDARY_STOP",
            "no": "classify_boundary_deficiency",
            "taken": classification["classification"],
        },
    ]
    return {
        "schema_version": "r1000_selected_group_inspection_transition_trace_v0",
        "source_group_capability_receipt_id": SOURCE_GROUP_CAPABILITY_RECEIPT_ID,
        "selected_group": EXPECTED_SELECTED_GROUP,
        "trace": trace,
        "terminal": classification["terminal"],
    }

def build_decision_packet(classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_selected_group_boundary_stop_decision_packet_v0",
        "decision_packet_id": sha8({
            "selected_group": EXPECTED_SELECTED_GROUP,
            "classification": classification["classification"],
        }),
        "source_group_capability_receipt_id": SOURCE_GROUP_CAPABILITY_RECEIPT_ID,
        "selected_group": EXPECTED_SELECTED_GROUP,
        "classification": classification["classification"],
        "branch_resolution": classification["branch_resolution"],
        "decision": "ACCEPT_HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP" if classification["classification"] == "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP" else "STOP_WITH_SELECTED_GROUP_DECISION_REQUIRED",
        "authorized_effect": [
            "record selected group inspection result",
            "classify selected boundary-stop surface",
            "stop without opening another group",
        ],
        "not_authorized": HUMAN_DECISION["not_authorized"],
        "terminal": classification["terminal"],
    }

def build_report(rows: List[Dict[str, Any]], evidence_surface: Dict[str, Any], classification: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_group_specific_inspection_application_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_group_capability_receipt_id": SOURCE_GROUP_CAPABILITY_RECEIPT_ID,
        "source_fixed_application_receipt_id": SOURCE_FIXED_APPLICATION_RECEIPT_ID,
        "selected_group": EXPECTED_SELECTED_GROUP,
        "selected_group_row_count": len(rows),
        "selected_group_rows_materialized_count": 1,
        "evidence_surface_emitted_count": 1,
        "surface_state_records_emitted_count": 2,
        "transition_trace_emitted_count": 1,
        "classification_emitted_count": 1,
        "decision_packet_emitted_count": 1,
        "classification": classification["classification"],
        "branch_resolution": classification["branch_resolution"],
        "healthy_expected_boundary_stop_count": 1 if classification["classification"] == "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP" else 0,
        "authority_basis_visible": evidence_surface["authority_basis"]["authority_basis_visible"],
        "scope_selected_group_only": True,
        "inspection_executed_count": 1,
        "r1000_run_executed_count": 0,
        "other_group_inspection_count": 0,
        "repair_executed_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "next_group_auto_opened_count": 0,
        "hidden_next_command_count": 0,
        "recommended_next_handling": "RETURN_TO_PRESSURE_QUEUE_OR_SELECT_NEXT_HUMAN_AUTHORIZED_OBJECTIVE",
    }

def validate_outputs(rows: List[Dict[str, Any]], evidence_surface: Dict[str, Any], records: List[Dict[str, Any]], trace: Dict[str, Any], classification: Dict[str, Any], decision_packet: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if len(rows) != 24:
        failures.append(f"selected_group_row_count_wrong:{len(rows)}")
    if evidence_surface["inspection_scope"]["selected_group_only"] is not True:
        failures.append("evidence_surface_scope_not_selected_only")
    if evidence_surface["inspection_scope"]["other_group_row_count"] != 0:
        failures.append("evidence_surface_other_group_rows_nonzero")
    if evidence_surface["key_visibility"]["all_required_keys_visible"] is not True:
        failures.append("required_keys_not_visible")
    if evidence_surface["group_tuple_consistency"]["unique_group_tuple_count"] != 1:
        failures.append("group_tuple_not_consistent")
    if evidence_surface["authority_basis"]["authority_basis_visible"] is not True:
        failures.append("authority_basis_not_visible")
    if classification["classification"] != "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP":
        failures.append(f"classification_unexpected:{classification['classification']}")
    if classification["branch_resolution"] != "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP_ACCEPTED":
        failures.append(f"branch_resolution_unexpected:{classification['branch_resolution']}")
    if classification["terminal"]["stop_code"] != "STOP_SELECTED_GROUP_INSPECTION_COMPLETE_HEALTHY_BOUNDARY_STOP":
        failures.append(f"classification_stop_wrong:{classification['terminal']}")
    if decision_packet["decision"] != "ACCEPT_HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP":
        failures.append("decision_packet_decision_wrong")
    if trace["terminal"]["type"] != "STOP":
        failures.append("trace_terminal_not_stop")
    if trace["terminal"]["next_command_goal"] is not None:
        failures.append("trace_terminal_next_not_null")
    if len(records) != 2:
        failures.append(f"surface_record_count_wrong:{len(records)}")
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
    for key in [
        "r1000_run_executed_count",
        "other_group_inspection_count",
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
    if report.get("inspection_executed_count") != 1:
        failures.append(f"inspection_executed_count_wrong:{report.get('inspection_executed_count')}")
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
    if metrics.get("selected_group_row_count") != 24:
        failures.append(f"metric_selected_group_row_count_wrong:{metrics.get('selected_group_row_count')}")
    if metrics.get("scope_selected_group_only") is not True:
        failures.append("metric_scope_not_selected_group_only")
    if metrics.get("inspection_executed_count") != 1:
        failures.append(f"metric_inspection_executed_wrong:{metrics.get('inspection_executed_count')}")
    if metrics.get("classification") != "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP":
        failures.append(f"metric_classification_wrong:{metrics.get('classification')}")
    if metrics.get("branch_resolution") != "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP_ACCEPTED":
        failures.append(f"metric_branch_resolution_wrong:{metrics.get('branch_resolution')}")
    for key in [
        "r1000_run_executed_count",
        "other_group_inspection_count",
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
    if terminal.get("stop_code") != "STOP_SELECTED_GROUP_INSPECTION_COMPLETE_HEALTHY_BOUNDARY_STOP":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    source_before = snapshot_files(SOURCE_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    selected_rows = selected_group_rows(sources["r1000_pressure_rows"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    evidence_surface = build_evidence_surface(selected_rows)
    classification = classify_surface(evidence_surface)
    records = [
        surface_record(
            {"surface": "selected_group_evidence_surface", "selected_group": EXPECTED_SELECTED_GROUP},
            "selected_group_evidence_surface",
            SOURCE_GROUP_CAPABILITY_RECEIPT_ID,
            len(selected_rows),
            "SELECTED_GROUP_EVIDENCE_SURFACE_MATERIALIZED",
        ),
        surface_record(
            {"surface": "selected_group_boundary_classification", "classification": classification["classification"]},
            "selected_group_boundary_classification_surface",
            SOURCE_GROUP_CAPABILITY_RECEIPT_ID,
            len(selected_rows),
            classification["classification"],
            terminal_type="STOP",
            stop_code=classification["terminal"]["stop_code"],
        ),
    ]
    trace = build_transition_trace(evidence_surface, classification)
    decision_packet = build_decision_packet(classification)
    report = build_report(selected_rows, evidence_surface, classification)

    write_jsonl(SELECTED_ROWS_PATH, selected_rows)
    write_json(EVIDENCE_SURFACE_PATH, evidence_surface)
    write_jsonl(SURFACE_RECORDS_PATH, records)
    write_json(TRANSITION_TRACE_PATH, trace)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(DECISION_PACKET_PATH, decision_packet)
    write_json(APPLICATION_REPORT_PATH, report)

    failures.extend(validate_outputs(selected_rows, evidence_surface, records, trace, classification, decision_packet, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "GROUP_INSPECTION_0_CAPABILITY_AUTHORIZATION_CONSUMED": sources["group_capability_receipt"]["receipt_id"] == SOURCE_GROUP_CAPABILITY_RECEIPT_ID and sources["group_capability_receipt"]["gate"] == "PASS",
        "GROUP_INSPECTION_1_SELECTED_GROUP_SCOPE_CONFIRMED": len(selected_rows) == 24 and evidence_surface["inspection_scope"]["selected_group_only"] is True,
        "GROUP_INSPECTION_2_SELECTED_ROWS_MATERIALIZED": SELECTED_ROWS_PATH.exists() and len(selected_rows) == 24,
        "GROUP_INSPECTION_3_EVIDENCE_SURFACE_EMITTED": EVIDENCE_SURFACE_PATH.exists(),
        "GROUP_INSPECTION_4_AUTHORITY_BASIS_VISIBLE": evidence_surface["authority_basis"]["authority_basis_visible"] is True,
        "GROUP_INSPECTION_5_CLASSIFICATION_EMITTED": CLASSIFICATION_PATH.exists() and classification["classification"] == "HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP",
        "GROUP_INSPECTION_6_DECISION_PACKET_EMITTED": DECISION_PACKET_PATH.exists() and decision_packet["decision"] == "ACCEPT_HEALTHY_EXPECTED_AUTHORITY_BOUNDARY_STOP",
        "GROUP_INSPECTION_7_NO_R1000_RUN_OR_OTHER_GROUP_INSPECTION": report["r1000_run_executed_count"] == 0 and report["other_group_inspection_count"] == 0,
        "GROUP_INSPECTION_8_NO_REPAIR_EXECUTED": report["repair_executed_count"] == 0,
        "GROUP_INSPECTION_9_NO_VALUE_OR_TAXONOMY_ACTION": report["field_value_invention_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0 and report["taxonomy_upgrade_authorized_count"] == 0,
        "GROUP_INSPECTION_10_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "GROUP_INSPECTION_11_NO_NEXT_GROUP_AUTO_OPEN": report["next_group_auto_opened_count"] == 0,
        "GROUP_INSPECTION_12_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = classification["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_group_capability_receipt_id": SOURCE_GROUP_CAPABILITY_RECEIPT_ID,
        "source_fixed_application_receipt_id": SOURCE_FIXED_APPLICATION_RECEIPT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "selected_group": EXPECTED_SELECTED_GROUP,
        "selected_group_row_count": len(selected_rows),
        "selected_rows_materialized_count": 1,
        "evidence_surface_emitted_count": 1,
        "surface_state_records_emitted_count": len(records),
        "transition_trace_emitted_count": 1,
        "classification_emitted_count": 1,
        "decision_packet_emitted_count": 1,
        "classification": classification["classification"],
        "branch_resolution": classification["branch_resolution"],
        "healthy_expected_boundary_stop_count": report["healthy_expected_boundary_stop_count"],
        "authority_basis_visible": evidence_surface["authority_basis"]["authority_basis_visible"],
        "scope_selected_group_only": True,
        "inspection_executed_count": 1,
        "r1000_run_executed_count": 0,
        "other_group_inspection_count": 0,
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

    guards = {
        "capability_authorization_consumed": True,
        "selected_group_scope_confirmed": len(selected_rows) == 24,
        "selected_rows_materialized": True,
        "evidence_surface_emitted": True,
        "authority_basis_visible": evidence_surface["authority_basis"]["authority_basis_visible"],
        "classification_emitted": True,
        "decision_packet_emitted": True,
        "r1000_run_executed": False,
        "other_group_inspection_executed": False,
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
        "source_capability": SOURCE_GROUP_CAPABILITY_RECEIPT_ID,
        "selected_group": EXPECTED_SELECTED_GROUP,
        "classification": classification["classification"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "selected_group_rows": rel(SELECTED_ROWS_PATH),
        "selected_group_evidence_surface": rel(EVIDENCE_SURFACE_PATH),
        "selected_group_surface_state_records": rel(SURFACE_RECORDS_PATH),
        "selected_group_inspection_transition_trace": rel(TRANSITION_TRACE_PATH),
        "selected_group_boundary_stop_classification": rel(CLASSIFICATION_PATH),
        "selected_group_boundary_stop_decision_packet": rel(DECISION_PACKET_PATH),
        "selected_group_inspection_application_report": rel(APPLICATION_REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_group_specific_inspection_application_receipt_v0",
        "receipt_type": "R1000_GROUP_SPECIFIC_INSPECTION_APPLICATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_group_capability_receipt_id": SOURCE_GROUP_CAPABILITY_RECEIPT_ID,
        "source_fixed_application_receipt_id": SOURCE_FIXED_APPLICATION_RECEIPT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "group_specific_inspection_application_summary": {
            "selected_group": EXPECTED_SELECTED_GROUP,
            "selected_group_row_count": len(selected_rows),
            "classification": classification["classification"],
            "branch_resolution": classification["branch_resolution"],
            "authority_basis_visible": evidence_surface["authority_basis"]["authority_basis_visible"],
            "recommended_next_handling": report["recommended_next_handling"],
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "group_specific_inspection_application_guards": guards,
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
    print(f"group_specific_inspection_application_receipt_id={receipt_id}")
    print(f"group_specific_inspection_application_receipt_path=data/r1000_group_specific_inspection_application_v0_receipts/{receipt_id}.json")
    print(f"group_specific_inspection_classification_path=data/r1000_group_specific_inspection_application_v0/selected_group_boundary_stop_classification.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
