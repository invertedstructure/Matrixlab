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

UNIT_ID = "AUTHORIZE_R1000_GROUP_SPECIFIC_INSPECTION_CAPABILITY_V0"
TARGET_UNIT_ID = "r1000_group_specific_inspection_capability.v0"

SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID = "4a0cfc09"
SOURCE_FIXED_APPLICATION_RECEIPT_ID = "2a16f593"
SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID = "e3371951"
SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID = "a121ff40"

OUT_DIR = ROOT / "data" / "r1000_group_specific_inspection_capability_v0"
RECEIPT_DIR = ROOT / "data" / "r1000_group_specific_inspection_capability_v0_receipts"

AUTHORIZATION_PACKET_PATH = OUT_DIR / "group_specific_inspection_capability_authorization_packet.json"
CAPABILITY_CONTRACT_PATH = OUT_DIR / "group_specific_inspection_capability_contract.json"
SELECTED_GROUP_PROFILE_PATH = OUT_DIR / "selected_group_inspection_profile.json"
INSPECTION_DECISION_TABLE_PATH = OUT_DIR / "selected_group_inspection_decision_table.json"
ACCEPTANCE_GATES_PATH = OUT_DIR / "group_specific_inspection_capability_acceptance_gates.json"
REPORT_PATH = OUT_DIR / "group_specific_inspection_capability_report.json"

CLOSED_BRANCH_FIX_RECEIPT_PATH = ROOT / "data" / "r1000_current_surface_closed_branch_exclusion_key_match_fix_v0_receipts" / f"{SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID}.json"
FIXED_APPLICATION_RECEIPT_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_fixed_v0_receipts" / f"{SOURCE_FIXED_APPLICATION_RECEIPT_ID}.json"
FIXED_SELECTED_GROUP_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_fixed_v0" / "r1000_current_surface_selected_pressure_group.json"
FIXED_CAPABILITY_STOP_PACKET_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_fixed_v0" / "r1000_current_surface_capability_stop_packet.json"
FIXED_QUEUE_SUMMARY_PATH = ROOT / "data" / "current_surface_pressure_loop_r1000_application_fixed_v0" / "r1000_current_surface_pressure_queue_summary.json"

CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID}.json"
CURRENT_SURFACE_PROTOCOL_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "current_surface_pressure_loop_protocol.json"
SURFACE_STATE_SCHEMA_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "surface_state_record_schema.json"
SURFACE_TRANSITION_TABLE_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "surface_transition_decision_table.json"
CAPABILITY_STOP_SCHEMA_PATH = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0" / "capability_stop_packet_schema.json"

EXPECTED_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_RECEIPT_ID}.json"

R1000_SCALE_RECEIPT_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0_receipts" / f"{SOURCE_R1000_SCALE_STABILITY_RECEIPT_ID}.json"
R1000_PRESSURE_ROWS_PATH = ROOT / "data" / "r1000_pressure_scale_stability_candidate_c_v0" / "r1000_pressure_event_rows.jsonl"

SOURCE_FILES = [
    CLOSED_BRANCH_FIX_RECEIPT_PATH,
    FIXED_APPLICATION_RECEIPT_PATH,
    FIXED_SELECTED_GROUP_PATH,
    FIXED_CAPABILITY_STOP_PACKET_PATH,
    FIXED_QUEUE_SUMMARY_PATH,
    CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH,
    CURRENT_SURFACE_PROTOCOL_PATH,
    SURFACE_STATE_SCHEMA_PATH,
    SURFACE_TRANSITION_TABLE_PATH,
    CAPABILITY_STOP_SCHEMA_PATH,
    EXPECTED_LIMIT_RECEIPT_PATH,
    R1000_SCALE_RECEIPT_PATH,
    R1000_PRESSURE_ROWS_PATH,
]

EXPECTED_SELECTED_GROUP = {
    "parent_pressure_class": "AUTHORITY_BOUNDARY",
    "pressure_subtype": "healthy_boundary_stop",
    "halt_reason": "STOP_AUTHORITY_BOUNDARY",
}

HUMAN_DECISION = {
    "decision": "AUTHORIZE_GROUP_SPECIFIC_INSPECTION_CAPABILITY",
    "scope": "authorize a narrow inspection capability for the selected R1000 remaining pressure group only, without executing that inspection in this unit",
    "source_closed_branch_fix_receipt_id": SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID,
    "source_fixed_application_receipt_id": SOURCE_FIXED_APPLICATION_RECEIPT_ID,
    "selected_group": EXPECTED_SELECTED_GROUP,
    "authorized": [
        "define selected-group inspection capability contract",
        "define selected-group inspection profile",
        "define yes/no inspection decision table for the selected group",
        "define acceptance gates for applying the selected-group inspection capability",
        "authorize a later application unit to inspect this selected group within the contract",
    ],
    "not_authorized": [
        "executing selected-group inspection in this unit",
        "running new R1000 pressure generation",
        "repairing the selected group",
        "inventing values",
        "creating labels",
        "upgrading taxonomy",
        "mutating source rows",
        "mutating existing receipts",
        "auto-opening another pressure group",
        "claiming general capability for all groups",
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
        "closed_branch_fix_receipt": read_json(CLOSED_BRANCH_FIX_RECEIPT_PATH),
        "fixed_application_receipt": read_json(FIXED_APPLICATION_RECEIPT_PATH),
        "fixed_selected_group": read_json(FIXED_SELECTED_GROUP_PATH),
        "fixed_capability_stop_packet": read_json(FIXED_CAPABILITY_STOP_PACKET_PATH),
        "fixed_queue_summary": read_json(FIXED_QUEUE_SUMMARY_PATH),
        "current_surface_protocol_receipt": read_json(CURRENT_SURFACE_PROTOCOL_RECEIPT_PATH),
        "current_surface_protocol": read_json(CURRENT_SURFACE_PROTOCOL_PATH),
        "surface_state_schema": read_json(SURFACE_STATE_SCHEMA_PATH),
        "surface_transition_table": read_json(SURFACE_TRANSITION_TABLE_PATH),
        "capability_stop_schema": read_json(CAPABILITY_STOP_SCHEMA_PATH),
        "expected_limit_receipt": read_json(EXPECTED_LIMIT_RECEIPT_PATH),
        "r1000_scale_receipt": read_json(R1000_SCALE_RECEIPT_PATH),
        "r1000_pressure_rows": read_jsonl(R1000_PRESSURE_ROWS_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    closed = sources["closed_branch_fix_receipt"]
    fixed = sources["fixed_application_receipt"]
    selected = sources["fixed_selected_group"]
    stop_packet = sources["fixed_capability_stop_packet"]

    if closed.get("receipt_id") != SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID:
        failures.append("closed_branch_fix_receipt_id_wrong")
    if closed.get("gate") != "PASS":
        failures.append("closed_branch_fix_not_pass")
    if closed.get("aggregate_metrics", {}).get("closed_branch_excluded_count_after_fix") != 1:
        failures.append("closed_branch_not_excluded")
    if closed.get("aggregate_metrics", {}).get("selected_group_count_after_fix") != 1:
        failures.append("selected_group_missing_after_fix")
    if closed.get("aggregate_metrics", {}).get("selected_group_key_after_fix") != EXPECTED_SELECTED_GROUP:
        failures.append("selected_group_key_wrong_after_fix")
    if closed.get("terminal", {}).get("stop_code") != "STOP_CAPABILITY_LAYER_REQUIRED":
        failures.append("closed_branch_fix_terminal_not_capability_stop")

    if fixed.get("receipt_id") != SOURCE_FIXED_APPLICATION_RECEIPT_ID:
        failures.append("fixed_application_receipt_id_wrong")
    if fixed.get("gate") != "PASS":
        failures.append("fixed_application_not_pass")
    if fixed.get("aggregate_metrics", {}).get("capability_stop_packet_emitted_count") != 1:
        failures.append("fixed_application_capability_stop_missing")
    if fixed.get("aggregate_metrics", {}).get("selected_group_row_count") != 24:
        failures.append("fixed_application_selected_group_row_count_wrong")

    if selected.get("selected") is not True:
        failures.append("selected_group_packet_not_selected")
    if selected.get("selected_group", {}).get("group_key") != EXPECTED_SELECTED_GROUP:
        failures.append("selected_group_packet_group_wrong")
    if selected.get("selected_group", {}).get("row_count") != 24:
        failures.append("selected_group_packet_row_count_wrong")

    if stop_packet.get("packet_type") != "CAPABILITY_STOP_PACKET":
        failures.append("capability_stop_packet_type_wrong")
    if stop_packet.get("missing_object_type") != "capability_boundary_unknown":
        failures.append("capability_stop_missing_object_wrong")
    if stop_packet.get("required_capability") != "CURRENT_SURFACE_GROUP_SPECIFIC_INSPECTION_CAPABILITY":
        failures.append("capability_stop_required_capability_wrong")
    if stop_packet.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("capability_stop_next_command_not_null")

    if sources["current_surface_protocol_receipt"].get("receipt_id") != SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID:
        failures.append("current_surface_protocol_receipt_id_wrong")
    if sources["current_surface_protocol_receipt"].get("gate") != "PASS":
        failures.append("current_surface_protocol_not_pass")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def count_selected_group_rows(rows: List[Dict[str, Any]]) -> int:
    count = 0
    for row in rows:
        if (
            row.get("parent_pressure_class") == EXPECTED_SELECTED_GROUP["parent_pressure_class"]
            and row.get("pressure_subtype") == EXPECTED_SELECTED_GROUP["pressure_subtype"]
            and row.get("halt_reason") == EXPECTED_SELECTED_GROUP["halt_reason"]
        ):
            count += 1
    return count

def build_authorization_packet(selected_group_row_count: int) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_group_specific_inspection_capability_authorization_packet_v0",
        "authorization_id": sha8({
            "unit": UNIT_ID,
            "source_fix": SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID,
            "selected_group": EXPECTED_SELECTED_GROUP,
        }),
        "authorization_type": "GROUP_SPECIFIC_INSPECTION_CAPABILITY_AUTHORIZATION",
        "source_closed_branch_fix_receipt_id": SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID,
        "source_fixed_application_receipt_id": SOURCE_FIXED_APPLICATION_RECEIPT_ID,
        "selected_group": EXPECTED_SELECTED_GROUP,
        "selected_group_row_count": selected_group_row_count,
        "authorized_capability": "CURRENT_SURFACE_GROUP_SPECIFIC_INSPECTION_CAPABILITY",
        "capability_scope": "selected_group_only",
        "capability_available_after_this_unit": True,
        "authorized_next_application_unit": "APPLY_R1000_GROUP_SPECIFIC_INSPECTION_CAPABILITY_TO_SELECTED_GROUP_V0",
        "not_authorized": HUMAN_DECISION["not_authorized"],
    }

def build_capability_contract(selected_group_row_count: int) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_group_specific_inspection_capability_contract_v0",
        "contract_id": sha8({
            "contract": "selected_group_inspection",
            "selected_group": EXPECTED_SELECTED_GROUP,
            "row_count": selected_group_row_count,
        }),
        "capability_name": "CURRENT_SURFACE_GROUP_SPECIFIC_INSPECTION_CAPABILITY",
        "scope": "single_selected_r1000_pressure_group",
        "selected_group": EXPECTED_SELECTED_GROUP,
        "selected_group_row_count": selected_group_row_count,
        "allowed_moves": [
            "read_selected_group_rows_from_existing_r1000_pressure_rows",
            "materialize_selected_group_evidence_surface",
            "classify_boundary_stop_as_healthy_expected_or_needs_more_detail",
            "emit_surface_state_records",
            "emit_transition_trace",
            "emit_typed_stop_or_decision_packet",
        ],
        "forbidden_moves": [
            "run_new_r1000_generation",
            "inspect_any_other_group",
            "repair_selected_group",
            "invent_values",
            "create_labels",
            "upgrade_taxonomy",
            "mutate_source_rows",
            "mutate_existing_receipts",
            "auto_open_next_group",
            "emit_hidden_next_command",
        ],
        "capability_boundary": {
            "may_classify_group_specific_surface": True,
            "may_execute_repairs": False,
            "may_emit_proposals": True,
            "may_mark_expected_limit": False,
            "must_stop_if_required_move_outside_contract": True,
            "stop_code": "STOP_CAPABILITY_LAYER_REQUIRED",
        },
        "authority_guards": {
            "r1000_run_executed_count": 0,
            "other_group_inspection_count": 0,
            "repair_executed_count": 0,
            "field_value_invention_count": 0,
            "taxonomy_label_creation_count": 0,
            "taxonomy_upgrade_authorized_count": 0,
            "source_mutation_count": 0,
            "existing_receipt_mutation_count": 0,
            "next_group_auto_opened_count": 0,
            "hidden_next_command_count": 0,
        },
    }

def build_selected_group_profile(rows: List[Dict[str, Any]]) -> Dict[str, Any]:
    selected_rows = [
        row for row in rows
        if row.get("parent_pressure_class") == EXPECTED_SELECTED_GROUP["parent_pressure_class"]
        and row.get("pressure_subtype") == EXPECTED_SELECTED_GROUP["pressure_subtype"]
        and row.get("halt_reason") == EXPECTED_SELECTED_GROUP["halt_reason"]
    ]
    sample_refs = [
        {
            "row_index": index,
            "receipt_id": row.get("receipt_id") or row.get("source_receipt_id"),
            "work_item_id": row.get("work_item_id") or row.get("item_id") or row.get("case_id") or row.get("id"),
        }
        for index, row in enumerate(selected_rows[:5])
    ]
    return {
        "schema_version": "selected_group_inspection_profile_v0",
        "selected_group": EXPECTED_SELECTED_GROUP,
        "selected_group_row_count": len(selected_rows),
        "source_rows_path": rel(R1000_PRESSURE_ROWS_PATH),
        "sample_refs": sample_refs,
        "profile_class": "AUTHORITY_BOUNDARY_HEALTHY_BOUNDARY_STOP",
        "initial_interpretation": "candidate healthy authority-boundary stop group requiring group-specific inspection before acceptance",
        "inspection_question": "is this group a healthy expected boundary stop, an authority-surface deficiency, or a capability-layer stop?",
    }

def build_decision_table() -> Dict[str, Any]:
    return {
        "schema_version": "selected_group_inspection_decision_table_v0",
        "selected_group": EXPECTED_SELECTED_GROUP,
        "transitions": [
            {
                "step": "materialize_selected_group_surface",
                "question": "selected_group_rows_visible",
                "yes": "inspect_boundary_surface",
                "no": "STOP_SELECTED_GROUP_ROWS_MISSING",
            },
            {
                "step": "inspect_boundary_surface",
                "question": "boundary_stop_has_explicit_authority_basis",
                "yes": "classify_boundary_stop",
                "no": "STOP_AUTHORITY_BASIS_MISSING",
            },
            {
                "step": "classify_boundary_stop",
                "question": "boundary_stop_is_expected_and_healthy",
                "yes": "CLASSIFY_HEALTHY_EXPECTED_BOUNDARY_STOP",
                "no": "classify_boundary_deficiency",
            },
            {
                "step": "classify_boundary_deficiency",
                "question": "deficiency_repairable_within_current_contract",
                "yes": "STOP_REPAIR_NOT_AUTHORIZED_BY_THIS_CAPABILITY",
                "no": "STOP_CAPABILITY_LAYER_REQUIRED",
            },
            {
                "step": "any_step",
                "question": "required_next_move_exceeds_current_contract",
                "yes": "STOP_CAPABILITY_LAYER_REQUIRED",
                "no": "continue_current_transition",
            },
        ],
        "terminal_codes": [
            "STOP_SELECTED_GROUP_ROWS_MISSING",
            "STOP_AUTHORITY_BASIS_MISSING",
            "CLASSIFY_HEALTHY_EXPECTED_BOUNDARY_STOP",
            "STOP_REPAIR_NOT_AUTHORIZED_BY_THIS_CAPABILITY",
            "STOP_CAPABILITY_LAYER_REQUIRED",
        ],
    }

def build_acceptance_gates() -> Dict[str, Any]:
    gates = [
        "GROUP_CAPABILITY_0_FIXED_APPLICATION_CONSUMED",
        "GROUP_CAPABILITY_1_SELECTED_GROUP_CONFIRMED",
        "GROUP_CAPABILITY_2_CAPABILITY_STOP_PACKET_CONSUMED",
        "GROUP_CAPABILITY_3_AUTHORIZATION_PACKET_EMITTED",
        "GROUP_CAPABILITY_4_CAPABILITY_CONTRACT_EMITTED",
        "GROUP_CAPABILITY_5_SELECTED_GROUP_PROFILE_EMITTED",
        "GROUP_CAPABILITY_6_DECISION_TABLE_EMITTED",
        "GROUP_CAPABILITY_7_SCOPE_SELECTED_GROUP_ONLY",
        "GROUP_CAPABILITY_8_NO_INSPECTION_EXECUTED",
        "GROUP_CAPABILITY_9_NO_R1000_RUN_OR_REPAIR_EXECUTED",
        "GROUP_CAPABILITY_10_NO_VALUE_OR_TAXONOMY_ACTION",
        "GROUP_CAPABILITY_11_NO_SOURCE_OR_RECEIPT_MUTATION",
        "GROUP_CAPABILITY_12_NO_NEXT_GROUP_AUTO_OPEN",
        "GROUP_CAPABILITY_13_NO_HIDDEN_NEXT_COMMAND",
    ]
    return {
        "schema_version": "r1000_group_specific_inspection_capability_acceptance_gates_v0",
        "gates": gates,
        "gate_requirements": {
            "GROUP_CAPABILITY_0_FIXED_APPLICATION_CONSUMED": "fixed R1000 current-surface application receipt must pass",
            "GROUP_CAPABILITY_1_SELECTED_GROUP_CONFIRMED": "selected group must match AUTHORITY_BOUNDARY / healthy_boundary_stop / STOP_AUTHORITY_BOUNDARY",
            "GROUP_CAPABILITY_2_CAPABILITY_STOP_PACKET_CONSUMED": "prior capability stop must identify CURRENT_SURFACE_GROUP_SPECIFIC_INSPECTION_CAPABILITY",
            "GROUP_CAPABILITY_3_AUTHORIZATION_PACKET_EMITTED": "authorization packet must be emitted",
            "GROUP_CAPABILITY_4_CAPABILITY_CONTRACT_EMITTED": "capability contract must be emitted",
            "GROUP_CAPABILITY_5_SELECTED_GROUP_PROFILE_EMITTED": "selected group profile must be emitted",
            "GROUP_CAPABILITY_6_DECISION_TABLE_EMITTED": "selected group inspection decision table must be emitted",
            "GROUP_CAPABILITY_7_SCOPE_SELECTED_GROUP_ONLY": "contract must not generalize to all groups",
            "GROUP_CAPABILITY_8_NO_INSPECTION_EXECUTED": "this unit must authorize capability only, not inspect",
            "GROUP_CAPABILITY_9_NO_R1000_RUN_OR_REPAIR_EXECUTED": "no new R1000 run or repair execution",
            "GROUP_CAPABILITY_10_NO_VALUE_OR_TAXONOMY_ACTION": "no value invention or taxonomy action",
            "GROUP_CAPABILITY_11_NO_SOURCE_OR_RECEIPT_MUTATION": "no source row or existing receipt mutation",
            "GROUP_CAPABILITY_12_NO_NEXT_GROUP_AUTO_OPEN": "no auto-opening any other group",
            "GROUP_CAPABILITY_13_NO_HIDDEN_NEXT_COMMAND": "terminal next_command_goal must remain null",
        },
    }

def build_report(selected_group_row_count: int) -> Dict[str, Any]:
    return {
        "schema_version": "r1000_group_specific_inspection_capability_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_closed_branch_fix_receipt_id": SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID,
        "source_fixed_application_receipt_id": SOURCE_FIXED_APPLICATION_RECEIPT_ID,
        "selected_group": EXPECTED_SELECTED_GROUP,
        "selected_group_row_count": selected_group_row_count,
        "authorization_packet_emitted_count": 1,
        "capability_contract_emitted_count": 1,
        "selected_group_profile_emitted_count": 1,
        "decision_table_emitted_count": 1,
        "capability_available_after_this_unit": True,
        "scope_selected_group_only": True,
        "inspection_executed_count": 0,
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
        "recommended_next_handling": "APPLY_R1000_GROUP_SPECIFIC_INSPECTION_CAPABILITY_TO_SELECTED_GROUP_V0",
    }

def validate_outputs(authorization_packet: Dict[str, Any], contract: Dict[str, Any], profile: Dict[str, Any], decision_table: Dict[str, Any], gates: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if authorization_packet["selected_group"] != EXPECTED_SELECTED_GROUP:
        failures.append("authorization_selected_group_wrong")
    if authorization_packet["capability_scope"] != "selected_group_only":
        failures.append("authorization_scope_not_selected_only")
    if authorization_packet["capability_available_after_this_unit"] is not True:
        failures.append("capability_not_available_after_unit")
    if contract["scope"] != "single_selected_r1000_pressure_group":
        failures.append("contract_scope_wrong")
    if contract["selected_group"] != EXPECTED_SELECTED_GROUP:
        failures.append("contract_selected_group_wrong")
    if "inspect_any_other_group" not in contract["forbidden_moves"]:
        failures.append("contract_does_not_forbid_other_group")
    if profile["selected_group_row_count"] != 24:
        failures.append(f"profile_selected_group_row_count_wrong:{profile['selected_group_row_count']}")
    if len(decision_table["transitions"]) < 5:
        failures.append("decision_table_too_small")
    if "GROUP_CAPABILITY_8_NO_INSPECTION_EXECUTED" not in gates["gates"]:
        failures.append("no_inspection_gate_missing")
    for key in [
        "inspection_executed_count",
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
    if metrics.get("capability_available_after_this_unit") is not True:
        failures.append("metric_capability_not_available")
    if metrics.get("scope_selected_group_only") is not True:
        failures.append("metric_scope_not_selected_group_only")
    if metrics.get("selected_group_row_count") != 24:
        failures.append(f"metric_selected_group_row_count_wrong:{metrics.get('selected_group_row_count')}")
    for key in [
        "inspection_executed_count",
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
    if terminal.get("stop_code") != "STOP_GROUP_SPECIFIC_INSPECTION_CAPABILITY_AUTHORIZED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    source_before = snapshot_files(SOURCE_FILES)
    sources = load_sources()
    failures: List[str] = validate_sources(sources)

    selected_group_row_count = count_selected_group_rows(sources["r1000_pressure_rows"])

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    authorization_packet = build_authorization_packet(selected_group_row_count)
    capability_contract = build_capability_contract(selected_group_row_count)
    selected_group_profile = build_selected_group_profile(sources["r1000_pressure_rows"])
    decision_table = build_decision_table()
    gates = build_acceptance_gates()
    report = build_report(selected_group_row_count)

    write_json(AUTHORIZATION_PACKET_PATH, authorization_packet)
    write_json(CAPABILITY_CONTRACT_PATH, capability_contract)
    write_json(SELECTED_GROUP_PROFILE_PATH, selected_group_profile)
    write_json(INSPECTION_DECISION_TABLE_PATH, decision_table)
    write_json(ACCEPTANCE_GATES_PATH, gates)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(authorization_packet, capability_contract, selected_group_profile, decision_table, gates, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "GROUP_CAPABILITY_0_FIXED_APPLICATION_CONSUMED": sources["fixed_application_receipt"]["receipt_id"] == SOURCE_FIXED_APPLICATION_RECEIPT_ID and sources["fixed_application_receipt"]["gate"] == "PASS",
        "GROUP_CAPABILITY_1_SELECTED_GROUP_CONFIRMED": sources["fixed_selected_group"]["selected_group"]["group_key"] == EXPECTED_SELECTED_GROUP and selected_group_row_count == 24,
        "GROUP_CAPABILITY_2_CAPABILITY_STOP_PACKET_CONSUMED": sources["fixed_capability_stop_packet"]["required_capability"] == "CURRENT_SURFACE_GROUP_SPECIFIC_INSPECTION_CAPABILITY",
        "GROUP_CAPABILITY_3_AUTHORIZATION_PACKET_EMITTED": AUTHORIZATION_PACKET_PATH.exists(),
        "GROUP_CAPABILITY_4_CAPABILITY_CONTRACT_EMITTED": CAPABILITY_CONTRACT_PATH.exists(),
        "GROUP_CAPABILITY_5_SELECTED_GROUP_PROFILE_EMITTED": SELECTED_GROUP_PROFILE_PATH.exists(),
        "GROUP_CAPABILITY_6_DECISION_TABLE_EMITTED": INSPECTION_DECISION_TABLE_PATH.exists(),
        "GROUP_CAPABILITY_7_SCOPE_SELECTED_GROUP_ONLY": capability_contract["scope"] == "single_selected_r1000_pressure_group" and authorization_packet["capability_scope"] == "selected_group_only",
        "GROUP_CAPABILITY_8_NO_INSPECTION_EXECUTED": report["inspection_executed_count"] == 0,
        "GROUP_CAPABILITY_9_NO_R1000_RUN_OR_REPAIR_EXECUTED": report["r1000_run_executed_count"] == 0 and report["repair_executed_count"] == 0,
        "GROUP_CAPABILITY_10_NO_VALUE_OR_TAXONOMY_ACTION": report["field_value_invention_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0 and report["taxonomy_upgrade_authorized_count"] == 0,
        "GROUP_CAPABILITY_11_NO_SOURCE_OR_RECEIPT_MUTATION": source_mutation_detected is False and report["source_mutation_count"] == 0 and report["existing_receipt_mutation_count"] == 0,
        "GROUP_CAPABILITY_12_NO_NEXT_GROUP_AUTO_OPEN": report["next_group_auto_opened_count"] == 0,
        "GROUP_CAPABILITY_13_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_GROUP_SPECIFIC_INSPECTION_CAPABILITY_AUTHORIZED",
        "next_command_goal": None,
    }
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "source_closed_branch_fix_receipt_id": SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID,
        "source_fixed_application_receipt_id": SOURCE_FIXED_APPLICATION_RECEIPT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "selected_group": EXPECTED_SELECTED_GROUP,
        "selected_group_row_count": selected_group_row_count,
        "authorization_packet_emitted_count": 1,
        "capability_contract_emitted_count": 1,
        "selected_group_profile_emitted_count": 1,
        "decision_table_emitted_count": 1,
        "capability_available_after_this_unit": True,
        "scope_selected_group_only": True,
        "inspection_executed_count": 0,
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
        "recommended_next_handling": "APPLY_R1000_GROUP_SPECIFIC_INSPECTION_CAPABILITY_TO_SELECTED_GROUP_V0",
    }

    guards = {
        "fixed_application_consumed": True,
        "selected_group_confirmed": selected_group_row_count == 24,
        "capability_stop_packet_consumed": True,
        "capability_available_after_this_unit": True,
        "scope_selected_group_only": True,
        "inspection_executed": False,
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
        "source_fix": SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID,
        "selected_group": EXPECTED_SELECTED_GROUP,
        "authorization_id": authorization_packet["authorization_id"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "authorization_packet": rel(AUTHORIZATION_PACKET_PATH),
        "capability_contract": rel(CAPABILITY_CONTRACT_PATH),
        "selected_group_inspection_profile": rel(SELECTED_GROUP_PROFILE_PATH),
        "selected_group_inspection_decision_table": rel(INSPECTION_DECISION_TABLE_PATH),
        "acceptance_gates": rel(ACCEPTANCE_GATES_PATH),
        "capability_report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "r1000_group_specific_inspection_capability_authorization_receipt_v0",
        "receipt_type": "R1000_GROUP_SPECIFIC_INSPECTION_CAPABILITY_AUTHORIZATION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_closed_branch_fix_receipt_id": SOURCE_CLOSED_BRANCH_FIX_RECEIPT_ID,
        "source_fixed_application_receipt_id": SOURCE_FIXED_APPLICATION_RECEIPT_ID,
        "source_current_surface_protocol_receipt_id": SOURCE_CURRENT_SURFACE_PROTOCOL_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "group_specific_inspection_capability_summary": {
            "authorization_id": authorization_packet["authorization_id"],
            "contract_id": capability_contract["contract_id"],
            "selected_group": EXPECTED_SELECTED_GROUP,
            "selected_group_row_count": selected_group_row_count,
            "capability_available_after_this_unit": True,
            "scope": "selected_group_only",
            "recommended_next_handling": "APPLY_R1000_GROUP_SPECIFIC_INSPECTION_CAPABILITY_TO_SELECTED_GROUP_V0",
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "group_specific_inspection_capability_guards": guards,
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
    print(f"group_specific_inspection_capability_receipt_id={receipt_id}")
    print(f"group_specific_inspection_capability_receipt_path=data/r1000_group_specific_inspection_capability_v0_receipts/{receipt_id}.json")
    print(f"group_specific_inspection_capability_contract_path=data/r1000_group_specific_inspection_capability_v0/group_specific_inspection_capability_contract.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
