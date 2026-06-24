#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_B3_CELL0_LOCAL_DECISION_LOOP_SCHEMA_LOCK_V0"
TARGET_UNIT_ID = "b3.cell0.local_decision_loop_schema_lock.v0"
LAYER = "CELL_0 / LOCAL_DECISION_GRAMMAR"
MODE = "CERTIFY / FREEZE / TRANSFER_TEST"
BUILD_MODE = "STATIC_SCHEMA_AND_PROBE_ONLY"
LOOP_ID = "LOCAL_DECISION_LOOP_V0"

SOURCE_B1_RECEIPT_ID = "b9c8f831"
SOURCE_B1_RECEIPT_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0_receipts" / "b9c8f831.json"
SOURCE_B1_PROFILE_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0" / "cell0_local_lawful_actor_profile_v0.json"
SOURCE_B1_PRESSURE_ENUM_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0" / "cell0_pressure_class_enum_v0.json"
SOURCE_B1_TYPED_STOP_SCHEMA_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0" / "cell0_typed_stop_schema_v0.json"
SOURCE_B1_MOVE_REGISTRY_PATH = ROOT / "data" / "b1_cell0_local_lawful_actor_stabilization_v0" / "cell0_local_demo_move_registry_v0.json"

SOURCE_B2_RECEIPT_ID = "7ab64083"
SOURCE_B2_RECEIPT_PATH = ROOT / "data" / "b2_cell0_informative_failure_progress_classifier_v0_receipts" / "7ab64083.json"
SOURCE_B2_PROFILE_PATH = ROOT / "data" / "b2_cell0_informative_failure_progress_classifier_v0" / "b2_informative_failure_profile_v0.json"
SOURCE_B2_PROGRESS_ENUM_PATH = ROOT / "data" / "b2_cell0_informative_failure_progress_classifier_v0" / "failure_progress_class_enum_v0.json"
SOURCE_B2_CLASSIFIER_RULES_PATH = ROOT / "data" / "b2_cell0_informative_failure_progress_classifier_v0" / "informative_failure_classifier_rules_v0.json"
SOURCE_B2_ROLLUP_PATH = ROOT / "data" / "b2_cell0_informative_failure_progress_classifier_v0" / "b2_failure_progress_rollup_v0.json"

OUT_DIR = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0"
RECEIPT_DIR = ROOT / "data" / "b3_cell0_local_decision_loop_schema_lock_v0_receipts"

LOOP_SCHEMA_PATH = OUT_DIR / "local_decision_loop_schema_v0.json"
STEP_ENUM_PATH = OUT_DIR / "local_decision_loop_step_enum_v0.json"
EDGE_ENUM_PATH = OUT_DIR / "local_decision_loop_edge_enum_v0.json"
FORBIDDEN_EDGE_ENUM_PATH = OUT_DIR / "local_decision_loop_forbidden_edge_enum_v0.json"
REQUIRED_DISTINCTION_SCHEMA_PATH = OUT_DIR / "local_required_distinction_record_schema_v0.json"
REQUIRED_DISTINCTION_CATALOG_PATH = OUT_DIR / "local_required_distinction_catalog_v0.json"
TRANSITION_TABLE_PATH = OUT_DIR / "local_decision_loop_transition_table_v0.json"
TRACE_SCHEMA_PATH = OUT_DIR / "local_decision_loop_trace_schema_v0.json"
RECEIPT_SCHEMA_PATH = OUT_DIR / "local_decision_loop_receipt_schema_v0.json"
LICENSE_MAP_PATH = OUT_DIR / "local_decision_loop_edge_artifact_license_map_v0.json"
SURFACE_MATRIX_PATH = OUT_DIR / "local_decision_loop_surface_test_matrix_v0.json"
TRACE_RECORDS_PATH = OUT_DIR / "local_decision_loop_trace_records_v0.jsonl"
LOOP_RECEIPTS_PATH = OUT_DIR / "local_decision_loop_receipts_v0.jsonl"
TRANSFER_ROLLUP_PATH = OUT_DIR / "local_decision_loop_transfer_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "b3_loop_lock_profile_v0.json"
TRANSITION_TRACE_PATH = OUT_DIR / "b3_transition_trace.json"
REPORT_PATH = OUT_DIR / "b3_report.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_B1_RECEIPT_PATH,
    SOURCE_B1_PROFILE_PATH,
    SOURCE_B1_PRESSURE_ENUM_PATH,
    SOURCE_B1_TYPED_STOP_SCHEMA_PATH,
    SOURCE_B1_MOVE_REGISTRY_PATH,
    SOURCE_B2_RECEIPT_PATH,
    SOURCE_B2_PROFILE_PATH,
    SOURCE_B2_PROGRESS_ENUM_PATH,
    SOURCE_B2_CLASSIFIER_RULES_PATH,
    SOURCE_B2_ROLLUP_PATH,
]

STEPS = [
    "LOAD_SURFACE",
    "VALIDATE_SURFACE",
    "SELECT_PRESSURE_GROUP",
    "CHECK_INSPECTION_AUTHORITY",
    "INSPECT_MINIMAL_SURFACE",
    "CLASSIFY_PRESSURE",
    "IDENTIFY_REQUIRED_DISTINCTION",
    "CHECK_DISTINCTION_AVAILABLE",
    "DECIDE_LOCAL_EDGE",
    "EMIT_ARTIFACT",
    "EMIT_RECEIPT",
    "STOP_OR_ADVANCE",
]

EDGE_TYPES = [
    "APPLY_LOCAL_MOVE",
    "EMIT_TYPED_STOP",
    "EMIT_PROPOSAL",
    "EMIT_REPAIR_CANDIDATE",
    "EMIT_EVIDENCE_REQUEST",
    "EMIT_STRATEGIC_PACKET",
    "CLOSE_NO_PRESSURE",
]

FORBIDDEN_EDGES = [
    "PRESSURE_TO_REPAIR_DIRECT",
    "FAILURE_TO_RETRY_DIRECT",
    "RECEIPT_TO_COMMAND_DIRECT",
    "PROPOSAL_TO_PATCH_DIRECT",
    "LABEL_TO_IDENTITY_DIRECT",
    "AUTHORITY_BOUNDARY_TO_EXECUTION_DIRECT",
]

PRESSURE_CLASSES = [
    "NO_PRESSURE",
    "RECEIPT_TRACE_PRESSURE",
    "OBSERVABILITY_PRESSURE",
    "AUTHORITY_PRESSURE",
    "TAXONOMY_PRESSURE",
    "MISSING_MOVE_PRESSURE",
    "LABEL_AMBIGUITY_PRESSURE",
    "BURDEN_PRESSURE",
    "EXTRACTION_PRESSURE",
    "FRONTIER_PRESSURE",
    "AMBIGUOUS_PRESSURE",
]

DISTINCTION_STATUSES = [
    "AVAILABLE",
    "MISSING_EVIDENCE",
    "MISSING_TAXONOMY",
    "MISSING_MOVE",
    "MISSING_AUTHORITY",
    "MISSING_EXTRACTION",
    "AMBIGUOUS",
]

REQUIRED_DISTINCTION_CATALOG = [
    "volatile_metadata_signal != protected_semantic_signal",
    "productive_pressure != radius_improvement",
    "proposal != accepted_patch",
    "workflow_position_label != object_identity",
    "authority_boundary != missing_move",
    "receipt_mismatch != projection_bug",
    "expected_limit != repairable_defect",
    "same_failure != sharper_localization",
    "new_artifact != decision_surface_delta",
    "pressure_classification != execution_authority",
]

ZERO_COUNTER_KEYS = [
    "surface_bespoke_path_count",
    "untyped_distinction_count",
    "missing_receipt_count",
    "hidden_next_command_count",
    "edge_artifact_mismatch_count",
    "static_probe_advance_count",
    "uncatalogued_distinction_count",
    "proposal_applied_count",
    "repair_executed_count",
    "retry_executed_count",
    "builder_command_executed_count",
    "cell1_authorization_count",
    "intercell_protocol_authorization_count",
    "taxonomy_mutation_count",
    "registry_mutation_count",
    "source_mutation_count",
    "prior_receipt_mutation_count",
]

HUMAN_DECISION = {
    "decision": "BUILD_B3_CELL0_LOCAL_DECISION_LOOP_SCHEMA_LOCK",
    "scope": "Build B3 as the Cell 0 local decision loop schema lock in STATIC_SCHEMA_AND_PROBE_ONLY mode. Emit the closed loop schema, step enum, edge enum, forbidden-edge enum, required-distinction schema/catalog, edge/artifact/terminal license map, transition table, trace schema, receipt schema, surface test matrix, loop traces, transfer rollup, profile, and receipt. Verify that every tested surface follows the same loop, names a required distinction, checks availability, selects a closed lawful edge, emits a licensed artifact and receipt, and avoids forbidden direct edges. Do not build Cell 1, create inter-cell protocol, execute repair/retry, mutate taxonomy/registry, or emit hidden next command.",
    "authorized": [
        "define local decision loop schema",
        "define loop step enum",
        "define transition table",
        "define loop trace schema",
        "define loop receipt schema",
        "define closed edge enum",
        "define forbidden direct edge enum",
        "define required distinction schema and local catalog",
        "define edge/artifact/terminal license map",
        "build surface test matrix",
        "run bounded static probe/demo surfaces",
        "emit transfer rollup",
        "emit local decision loop reference object",
        "stop with no next command goal",
    ],
    "not_authorized": [
        "build Cell 1",
        "create inter-cell protocol",
        "expand jurisdiction",
        "execute live repair",
        "execute retry",
        "mutate taxonomy",
        "mutate registry",
        "promote proposal to patch",
        "promote label to identity",
        "treat authority boundary as permission",
        "select live frontier by latest or mtime",
        "emit hidden next command",
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
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def append_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(row, sort_keys=True) + "\n")

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): file_sha256(path) for path in paths if path.exists()}

def validate_source_basis() -> List[str]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")

    if failures:
        return failures

    b1_receipt = read_json(SOURCE_B1_RECEIPT_PATH)
    b1_profile = read_json(SOURCE_B1_PROFILE_PATH)
    b2_receipt = read_json(SOURCE_B2_RECEIPT_PATH)
    b2_profile = read_json(SOURCE_B2_PROFILE_PATH)
    b2_rollup = read_json(SOURCE_B2_ROLLUP_PATH)

    if b1_receipt.get("receipt_id") != SOURCE_B1_RECEIPT_ID:
        failures.append("b1_receipt_id_wrong")
    if b1_receipt.get("gate") != "PASS":
        failures.append("b1_receipt_gate_not_PASS")
    if b1_profile.get("status") != "STABLE_LOCAL_ACTOR_PROFILE":
        failures.append("b1_profile_not_stable")
    if b2_receipt.get("receipt_id") != SOURCE_B2_RECEIPT_ID:
        failures.append("b2_receipt_id_wrong")
    if b2_receipt.get("gate") != "PASS":
        failures.append("b2_receipt_gate_not_PASS")
    if b2_profile.get("status") != "B2_INFORMATIVE_FAILURE_CLASSIFIER_STABLE":
        failures.append("b2_profile_not_stable")
    if b2_rollup.get("failure_events_total") != 12:
        failures.append("b2_rollup_event_count_unexpected")
    return failures

def loop_schema() -> Dict[str, Any]:
    return {
        "schema_version": "local_decision_loop_schema_v0",
        "loop_id": LOOP_ID,
        "build_mode": BUILD_MODE,
        "steps": STEPS,
        "closed_edge_types": EDGE_TYPES,
        "forbidden_edges": FORBIDDEN_EDGES,
        "core_compression": "surface -> authorized inspection -> pressure classification -> required distinction -> availability -> lawful edge -> artifact -> receipt -> stop/advance",
        "rules": [
            "No skipped edges.",
            "No pressure-to-repair direct path.",
            "No failure-to-retry direct path.",
            "No receipt-to-command direct path.",
            "No proposal-to-patch direct path.",
            "No label-to-identity direct path.",
            "No authority-boundary-to-execution direct path.",
        ],
    }

def step_enum() -> Dict[str, Any]:
    return {
        "schema_version": "local_decision_loop_step_enum_v0",
        "closed": True,
        "steps": [{"step": step, "ordinal": i + 1} for i, step in enumerate(STEPS)],
    }

def edge_enum() -> Dict[str, Any]:
    return {
        "schema_version": "local_decision_loop_edge_enum_v0",
        "closed": True,
        "edge_types": EDGE_TYPES,
    }

def forbidden_edge_enum() -> Dict[str, Any]:
    return {
        "schema_version": "local_decision_loop_forbidden_edge_enum_v0",
        "closed": True,
        "forbidden_edges": FORBIDDEN_EDGES,
        "must_remain_zero": True,
    }

def required_distinction_schema() -> Dict[str, Any]:
    return {
        "schema_version": "local_required_distinction_record_schema_v0",
        "record_schema": {
            "schema_version": "local_required_distinction_record_v0",
            "required_distinction_id": "dist_<sig8>",
            "pressure_classification_ref": None,
            "distinction": None,
            "why_required": None,
            "available_evidence": [],
            "missing_evidence": [],
            "status": "AVAILABLE | MISSING | AMBIGUOUS",
        },
        "rule": "No required distinction, no local edge.",
    }

def required_distinction_catalog() -> Dict[str, Any]:
    return {
        "schema_version": "local_required_distinction_catalog_v0",
        "catalog_status": "LOCAL_B3_PROBE_ONLY",
        "global_taxonomy_mutation_authorized": False,
        "distinctions": [
            {
                "distinction": d,
                "catalog_id": "dist_catalog_" + sha8({"distinction": d}),
                "scope": "LOCAL_DECISION_LOOP_V0",
            }
            for d in REQUIRED_DISTINCTION_CATALOG
        ],
    }

def transition_table() -> Dict[str, Any]:
    return {
        "schema_version": "local_decision_loop_transition_table_v0",
        "loop_id": LOOP_ID,
        "rules": [
            {"from": "LOAD_SURFACE", "condition": "fail", "to": "STOP_UNTYPED_SURFACE"},
            {"from": "VALIDATE_SURFACE", "condition": "fail", "to": "STOP_GATE_FAIL"},
            {"from": "SELECT_PRESSURE_GROUP", "condition": "ambiguous", "to": "QUESTION_PACKET_NOT_COMMAND"},
            {"from": "CHECK_INSPECTION_AUTHORITY", "condition": "forbidden", "to": "STOP_AUTHORITY_BOUNDARY"},
            {"from": "INSPECT_MINIMAL_SURFACE", "condition": "overinspection", "to": "STOP_AUTHORITY_VIOLATION"},
            {"from": "CLASSIFY_PRESSURE", "condition": "ambiguous", "to": "QUESTION_PACKET_NOT_COMMAND"},
            {"from": "IDENTIFY_REQUIRED_DISTINCTION", "condition": "missing", "to": "STOP_UNDERTYPED_OBJECT"},
            {"from": "CHECK_DISTINCTION_AVAILABLE", "condition": "MISSING_EVIDENCE", "to": "EMIT_EVIDENCE_REQUEST"},
            {"from": "CHECK_DISTINCTION_AVAILABLE", "condition": "MISSING_MOVE", "to": "EMIT_PROPOSAL"},
            {"from": "CHECK_DISTINCTION_AVAILABLE", "condition": "MISSING_AUTHORITY", "to": "EMIT_TYPED_STOP"},
            {"from": "CHECK_DISTINCTION_AVAILABLE", "condition": "AMBIGUOUS", "to": "QUESTION_PACKET_NOT_COMMAND"},
            {"from": "DECIDE_LOCAL_EDGE", "condition": "none", "to": "EMIT_TYPED_STOP"},
            {"from": "EMIT_ARTIFACT", "condition": "mismatch", "to": "STOP_GATE_FAIL"},
            {"from": "EMIT_RECEIPT", "condition": "missing", "to": "STOP_GATE_FAIL"},
            {"from": "STOP_OR_ADVANCE", "condition": "hidden_next", "to": "STOP_AUTHORITY_VIOLATION"},
        ],
    }

def trace_schema() -> Dict[str, Any]:
    return {
        "schema_version": "local_decision_loop_trace_schema_v0",
        "trace_schema": {
            "schema_version": "local_decision_loop_trace_v0",
            "trace_id": "loop_trace_<sig8>",
            "surface_ref": None,
            "step_results": [
                {
                    "step": None,
                    "status": "PASS | FAIL | STOP",
                    "output_ref": None,
                    "selected_edge": None,
                    "failure_code": None,
                }
            ],
            "terminal": None,
        },
    }

def receipt_schema() -> Dict[str, Any]:
    return {
        "schema_version": "local_decision_loop_receipt_schema_v0",
        "receipt_schema": {
            "schema_version": "local_decision_loop_receipt_v0",
            "receipt_id": "loop_receipt_<sig8>",
            "loop_id": LOOP_ID,
            "surface_ref": None,
            "pressure_group": None,
            "inspection_record_ref": None,
            "pressure_classification_ref": None,
            "required_distinction_ref": None,
            "distinction_status": None,
            "selected_edge": None,
            "artifact_refs": [],
            "forbidden_edge_counts": {},
            "terminal": {
                "type": None,
                "stop_code": None,
                "next_command_goal": None,
            },
        },
    }

def license_map() -> Dict[str, Any]:
    return {
        "schema_version": "local_decision_loop_edge_artifact_license_map_v0",
        "loop_id": LOOP_ID,
        "license_rules": [
            {
                "selected_edge": "APPLY_LOCAL_MOVE",
                "licensed_artifact_kinds": ["local_move_result"],
                "allowed_terminal_types": ["STOP", "ADVANCE"],
                "static_probe_allowed": False,
            },
            {
                "selected_edge": "EMIT_TYPED_STOP",
                "licensed_artifact_kinds": ["halt_record"],
                "allowed_terminal_types": ["STOP"],
                "static_probe_allowed": True,
            },
            {
                "selected_edge": "EMIT_PROPOSAL",
                "licensed_artifact_kinds": ["proposal_packet"],
                "allowed_terminal_types": ["STOP"],
                "static_probe_allowed": True,
                "proposal_applied": False,
                "proposal_accepted": False,
            },
            {
                "selected_edge": "EMIT_REPAIR_CANDIDATE",
                "licensed_artifact_kinds": ["repair_objective_candidate"],
                "allowed_terminal_types": ["STOP"],
                "static_probe_allowed": True,
                "repair_executed": False,
            },
            {
                "selected_edge": "EMIT_EVIDENCE_REQUEST",
                "licensed_artifact_kinds": ["question_packet", "evidence_request"],
                "allowed_terminal_types": ["STOP"],
                "static_probe_allowed": True,
            },
            {
                "selected_edge": "EMIT_STRATEGIC_PACKET",
                "licensed_artifact_kinds": ["a1_strategic_packet", "strategic_packet_stub"],
                "allowed_terminal_types": ["STOP"],
                "static_probe_allowed": True,
                "builder_command_authorized": False,
            },
            {
                "selected_edge": "CLOSE_NO_PRESSURE",
                "licensed_artifact_kinds": ["closure_readout_packet"],
                "allowed_terminal_types": ["STOP"],
                "static_probe_allowed": True,
            },
        ],
        "rule": "If selected edge does not license emitted artifact kind, B3 fails.",
    }

def schemas() -> Dict[Path, Dict[str, Any]]:
    return {
        LOOP_SCHEMA_PATH: loop_schema(),
        STEP_ENUM_PATH: step_enum(),
        EDGE_ENUM_PATH: edge_enum(),
        FORBIDDEN_EDGE_ENUM_PATH: forbidden_edge_enum(),
        REQUIRED_DISTINCTION_SCHEMA_PATH: required_distinction_schema(),
        REQUIRED_DISTINCTION_CATALOG_PATH: required_distinction_catalog(),
        TRANSITION_TABLE_PATH: transition_table(),
        TRACE_SCHEMA_PATH: trace_schema(),
        RECEIPT_SCHEMA_PATH: receipt_schema(),
        LICENSE_MAP_PATH: license_map(),
    }

def surface_matrix_rows() -> List[Dict[str, Any]]:
    rows = [
        {
            "surface_kind": "receipt_burden",
            "pressure_class": "BURDEN_PRESSURE",
            "required_distinction": "productive_pressure != radius_improvement",
            "distinction_status": "AVAILABLE",
            "selected_edge": "EMIT_EVIDENCE_REQUEST",
            "artifact_kind": "evidence_request",
            "terminal": "STOP(STOP_FRONTIER)",
        },
        {
            "surface_kind": "queue_reconciliation",
            "pressure_class": "RECEIPT_TRACE_PRESSURE",
            "required_distinction": "receipt_mismatch != projection_bug",
            "distinction_status": "AVAILABLE",
            "selected_edge": "EMIT_REPAIR_CANDIDATE",
            "artifact_kind": "repair_objective_candidate",
            "terminal": "STOP(STOP_FRONTIER)",
        },
        {
            "surface_kind": "synthetic_remainder",
            "pressure_class": "FRONTIER_PRESSURE",
            "required_distinction": "expected_limit != repairable_defect",
            "distinction_status": "AVAILABLE",
            "selected_edge": "EMIT_STRATEGIC_PACKET",
            "artifact_kind": "strategic_packet_stub",
            "terminal": "STOP(STOP_FRONTIER)",
        },
        {
            "surface_kind": "command_observability",
            "pressure_class": "OBSERVABILITY_PRESSURE",
            "required_distinction": "volatile_metadata_signal != protected_semantic_signal",
            "distinction_status": "AVAILABLE",
            "selected_edge": "EMIT_REPAIR_CANDIDATE",
            "artifact_kind": "repair_objective_candidate",
            "terminal": "STOP(STOP_FRONTIER)",
        },
        {
            "surface_kind": "identity_review",
            "pressure_class": "LABEL_AMBIGUITY_PRESSURE",
            "required_distinction": "workflow_position_label != object_identity",
            "distinction_status": "AVAILABLE",
            "selected_edge": "EMIT_PROPOSAL",
            "artifact_kind": "proposal_packet",
            "terminal": "STOP(STOP_DONE)",
        },
        {
            "surface_kind": "labeling_ambiguity",
            "pressure_class": "LABEL_AMBIGUITY_PRESSURE",
            "required_distinction": "workflow_position_label != object_identity",
            "distinction_status": "AVAILABLE",
            "selected_edge": "EMIT_PROPOSAL",
            "artifact_kind": "proposal_packet",
            "terminal": "STOP(STOP_DONE)",
        },
        {
            "surface_kind": "runtime_scaling",
            "pressure_class": "AUTHORITY_PRESSURE",
            "required_distinction": "authority_boundary != missing_move",
            "distinction_status": "AVAILABLE",
            "selected_edge": "EMIT_TYPED_STOP",
            "artifact_kind": "halt_record",
            "terminal": "STOP(STOP_AUTHORITY_BOUNDARY)",
        },
        {
            "surface_kind": "taxonomy_pressure",
            "pressure_class": "TAXONOMY_PRESSURE",
            "required_distinction": "pressure_classification != execution_authority",
            "distinction_status": "MISSING_TAXONOMY",
            "selected_edge": "EMIT_PROPOSAL",
            "artifact_kind": "proposal_packet",
            "terminal": "STOP(STOP_TAXONOMY_GAP)",
        },
        {
            "surface_kind": "missing_move_pressure",
            "pressure_class": "MISSING_MOVE_PRESSURE",
            "required_distinction": "authority_boundary != missing_move",
            "distinction_status": "MISSING_MOVE",
            "selected_edge": "EMIT_PROPOSAL",
            "artifact_kind": "proposal_packet",
            "terminal": "STOP(STOP_NEEDS_NEW_MOVE)",
        },
        {
            "surface_kind": "authority_boundary",
            "pressure_class": "AUTHORITY_PRESSURE",
            "required_distinction": "authority_boundary != missing_move",
            "distinction_status": "MISSING_AUTHORITY",
            "selected_edge": "EMIT_TYPED_STOP",
            "artifact_kind": "halt_record",
            "terminal": "STOP(STOP_AUTHORITY_BOUNDARY)",
        },
    ]
    for row in rows:
        row["schema_version"] = "local_decision_loop_surface_test_matrix_row_v0"
        row["matrix_row_id"] = "b3_surface_" + sha8(row)
        row["loop_id"] = LOOP_ID
        row["build_mode"] = BUILD_MODE
        row["uses_same_loop"] = True
        row["source_selection_rule"] = "declared_static_probe_surface"
        row["surface_ref"] = row["matrix_row_id"]
        row["required_distinction_ref"] = "dist_" + sha8({"distinction": row["required_distinction"], "surface": row["surface_kind"]})
        row["artifact_ref"] = "artifact_" + sha8({"kind": row["artifact_kind"], "surface": row["surface_kind"]})
        row["receipt_ref"] = "loop_receipt_" + sha8({"surface": row["surface_kind"], "edge": row["selected_edge"]})
    return rows

def license_lookup() -> Dict[str, Dict[str, Any]]:
    return {r["selected_edge"]: r for r in license_map()["license_rules"]}

def artifact_licensed(row: Dict[str, Any]) -> bool:
    rule = license_lookup().get(row["selected_edge"])
    if not rule:
        return False
    if row["artifact_kind"] not in rule["licensed_artifact_kinds"]:
        return False
    terminal_type = row["terminal"].split("(", 1)[0]
    if terminal_type not in rule["allowed_terminal_types"]:
        return False
    if BUILD_MODE == "STATIC_SCHEMA_AND_PROBE_ONLY" and rule.get("static_probe_allowed") is not True:
        return False
    return True

def stop_code_from_terminal(terminal: str) -> str:
    if terminal.startswith("STOP(") and terminal.endswith(")"):
        return terminal[5:-1]
    if terminal.startswith("ADVANCE(") and terminal.endswith(")"):
        return "ADVANCE"
    return "UNKNOWN"

def make_trace_record(row: Dict[str, Any]) -> Dict[str, Any]:
    step_results: List[Dict[str, Any]] = []
    for step in STEPS:
        selected_edge = row["selected_edge"] if step == "DECIDE_LOCAL_EDGE" else None
        output_ref = None
        if step == "LOAD_SURFACE":
            output_ref = row["surface_ref"]
        elif step == "INSPECT_MINIMAL_SURFACE":
            output_ref = "inspection_" + sha8({"surface": row["surface_kind"]})
        elif step == "CLASSIFY_PRESSURE":
            output_ref = "pressure_cls_" + sha8({"surface": row["surface_kind"], "pressure": row["pressure_class"]})
        elif step == "IDENTIFY_REQUIRED_DISTINCTION":
            output_ref = row["required_distinction_ref"]
        elif step == "EMIT_ARTIFACT":
            output_ref = row["artifact_ref"]
        elif step == "EMIT_RECEIPT":
            output_ref = row["receipt_ref"]
        step_results.append({
            "step": step,
            "status": "STOP" if step == "STOP_OR_ADVANCE" else "PASS",
            "output_ref": output_ref,
            "selected_edge": selected_edge,
            "failure_code": None,
        })
    return {
        "schema_version": "local_decision_loop_trace_v0",
        "trace_id": "loop_trace_" + sha8({"surface": row["surface_kind"], "edge": row["selected_edge"]}),
        "loop_id": LOOP_ID,
        "build_mode": BUILD_MODE,
        "surface_ref": row["surface_ref"],
        "step_results": step_results,
        "same_loop_steps": STEPS,
        "surface_bespoke_path_used": False,
        "terminal": {
            "type": "STOP",
            "stop_code": stop_code_from_terminal(row["terminal"]),
            "next_command_goal": None,
        },
    }

def make_loop_receipt(row: Dict[str, Any]) -> Dict[str, Any]:
    forbidden_counts = {edge: 0 for edge in FORBIDDEN_EDGES}
    return {
        "schema_version": "local_decision_loop_receipt_v0",
        "receipt_id": row["receipt_ref"],
        "loop_id": LOOP_ID,
        "surface_ref": row["surface_ref"],
        "surface_kind": row["surface_kind"],
        "pressure_group": row["pressure_class"],
        "inspection_record_ref": "inspection_" + sha8({"surface": row["surface_kind"]}),
        "pressure_classification_ref": "pressure_cls_" + sha8({"surface": row["surface_kind"], "pressure": row["pressure_class"]}),
        "required_distinction_ref": row["required_distinction_ref"],
        "required_distinction": row["required_distinction"],
        "distinction_status": row["distinction_status"],
        "selected_edge": row["selected_edge"],
        "artifact_refs": [row["artifact_ref"]],
        "artifact_kind": row["artifact_kind"],
        "artifact_licensed_by_edge": artifact_licensed(row),
        "forbidden_edge_counts": forbidden_counts,
        "proposal_applied": False,
        "repair_executed": False,
        "retry_executed": False,
        "builder_command_executed": False,
        "cell1_authorized": False,
        "intercell_protocol_authorized": False,
        "terminal": {
            "type": "STOP",
            "stop_code": stop_code_from_terminal(row["terminal"]),
            "next_command_goal": None,
        },
    }

def build_records() -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]], List[Dict[str, Any]]]:
    matrix = surface_matrix_rows()
    traces = [make_trace_record(row) for row in matrix]
    receipts = [make_loop_receipt(row) for row in matrix]
    return matrix, traces, receipts

def transfer_rollup(matrix: List[Dict[str, Any]], traces: List[Dict[str, Any]], receipts: List[Dict[str, Any]]) -> Dict[str, Any]:
    loop_step_failure_counts = {step: 0 for step in STEPS}
    forbidden_edge_counts = {edge: 0 for edge in FORBIDDEN_EDGES}
    edge_artifact_mismatch_count = sum(1 for r in receipts if r["artifact_licensed_by_edge"] is not True)
    static_probe_advance_count = sum(1 for r in receipts if r["terminal"]["type"] != "STOP")
    uncatalogued_distinction_count = sum(1 for row in matrix if row["required_distinction"] not in REQUIRED_DISTINCTION_CATALOG)
    missing_receipt_count = sum(1 for row in matrix if not row.get("receipt_ref"))
    hidden_next_command_count = sum(1 for r in receipts if r["terminal"].get("next_command_goal") is not None)
    untyped_distinction_count = sum(1 for row in matrix if not row.get("required_distinction") or row.get("distinction_status") not in DISTINCTION_STATUSES)
    surface_bespoke_path_count = sum(1 for t in traces if t.get("surface_bespoke_path_used") is True)
    proposal_applied_count = sum(1 for r in receipts if r.get("proposal_applied") is True)
    repair_executed_count = sum(1 for r in receipts if r.get("repair_executed") is True)
    retry_executed_count = sum(1 for r in receipts if r.get("retry_executed") is True)
    builder_command_executed_count = sum(1 for r in receipts if r.get("builder_command_executed") is True)
    cell1_authorization_count = sum(1 for r in receipts if r.get("cell1_authorized") is True)
    intercell_protocol_authorization_count = sum(1 for r in receipts if r.get("intercell_protocol_authorized") is True)
    passed = len(matrix) - sum([
        edge_artifact_mismatch_count,
        static_probe_advance_count,
        uncatalogued_distinction_count,
        missing_receipt_count,
        hidden_next_command_count,
        untyped_distinction_count,
        surface_bespoke_path_count,
        proposal_applied_count,
        repair_executed_count,
        retry_executed_count,
        builder_command_executed_count,
        cell1_authorization_count,
        intercell_protocol_authorization_count,
    ])
    zero_ok = all(v == 0 for v in [
        edge_artifact_mismatch_count,
        static_probe_advance_count,
        uncatalogued_distinction_count,
        missing_receipt_count,
        hidden_next_command_count,
        untyped_distinction_count,
        surface_bespoke_path_count,
        proposal_applied_count,
        repair_executed_count,
        retry_executed_count,
        builder_command_executed_count,
        cell1_authorization_count,
        intercell_protocol_authorization_count,
    ])
    return {
        "schema_version": "local_decision_loop_transfer_rollup_v0",
        "build_mode": BUILD_MODE,
        "surfaces_tested": len(matrix),
        "surfaces_passed": passed if zero_ok else max(0, passed),
        "loop_step_failure_counts": loop_step_failure_counts,
        "forbidden_edge_counts": forbidden_edge_counts,
        "surface_bespoke_path_count": surface_bespoke_path_count,
        "untyped_distinction_count": untyped_distinction_count,
        "missing_receipt_count": missing_receipt_count,
        "hidden_next_command_count": hidden_next_command_count,
        "edge_artifact_mismatch_count": edge_artifact_mismatch_count,
        "static_probe_advance_count": static_probe_advance_count,
        "uncatalogued_distinction_count": uncatalogued_distinction_count,
        "proposal_applied_count": proposal_applied_count,
        "repair_executed_count": repair_executed_count,
        "retry_executed_count": retry_executed_count,
        "builder_command_executed_count": builder_command_executed_count,
        "cell1_authorization_count": cell1_authorization_count,
        "intercell_protocol_authorization_count": intercell_protocol_authorization_count,
        "taxonomy_mutation_count": 0,
        "registry_mutation_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "transfer_result": "TRANSFERABLE_LOCAL_LOOP_V0" if zero_ok else "LOOP_SCHEMA_REPAIR_REQUIRED",
    }

def validate_records(matrix: List[Dict[str, Any]], traces: List[Dict[str, Any]], receipts: List[Dict[str, Any]], rollup: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    row_by_surface = {row["surface_ref"]: row for row in matrix}
    trace_by_surface = {trace["surface_ref"]: trace for trace in traces}
    receipt_by_surface = {receipt["surface_ref"]: receipt for receipt in receipts}

    if len(matrix) != 10:
        failures.append(f"surface_matrix_count_wrong:{len(matrix)}")
    if len(row_by_surface) != len(matrix):
        failures.append("surface_refs_duplicate_or_missing")

    for row in matrix:
        if row.get("uses_same_loop") is not True:
            failures.append(f"surface_not_same_loop:{row['surface_kind']}")
        if row.get("source_selection_rule") != "declared_static_probe_surface":
            failures.append(f"surface_not_declared_static_probe:{row['surface_kind']}")
        if row["pressure_class"] not in PRESSURE_CLASSES:
            failures.append(f"pressure_class_not_closed:{row['surface_kind']}:{row['pressure_class']}")
        if row["selected_edge"] not in EDGE_TYPES:
            failures.append(f"edge_not_closed:{row['surface_kind']}:{row['selected_edge']}")
        if not row.get("required_distinction"):
            failures.append(f"required_distinction_missing:{row['surface_kind']}")
        if row["required_distinction"] not in REQUIRED_DISTINCTION_CATALOG:
            failures.append(f"required_distinction_uncatalogued:{row['surface_kind']}")
        if row["distinction_status"] not in DISTINCTION_STATUSES:
            failures.append(f"distinction_status_invalid:{row['surface_kind']}:{row['distinction_status']}")
        if not artifact_licensed(row):
            failures.append(f"artifact_not_licensed_by_edge:{row['surface_kind']}:{row['selected_edge']}:{row['artifact_kind']}")
        if row["surface_ref"] not in trace_by_surface:
            failures.append(f"trace_missing:{row['surface_kind']}")
        if row["surface_ref"] not in receipt_by_surface:
            failures.append(f"receipt_missing:{row['surface_kind']}")

    for trace in traces:
        trace_steps = [r["step"] for r in trace.get("step_results", [])]
        if trace_steps != STEPS:
            failures.append(f"trace_steps_not_locked:{trace.get('trace_id')}")
        if trace.get("surface_bespoke_path_used") is not False:
            failures.append(f"surface_bespoke_path_used:{trace.get('trace_id')}")
        terminal = trace.get("terminal", {})
        if terminal.get("type") != "STOP":
            failures.append(f"trace_static_probe_advance:{trace.get('trace_id')}")
        if terminal.get("next_command_goal") is not None:
            failures.append(f"trace_hidden_next:{trace.get('trace_id')}")

    for receipt in receipts:
        if receipt["selected_edge"] not in EDGE_TYPES:
            failures.append(f"receipt_edge_not_closed:{receipt['receipt_id']}")
        if receipt["artifact_licensed_by_edge"] is not True:
            failures.append(f"receipt_artifact_not_licensed:{receipt['receipt_id']}")
        for edge, count in receipt["forbidden_edge_counts"].items():
            if edge not in FORBIDDEN_EDGES:
                failures.append(f"receipt_forbidden_edge_unknown:{receipt['receipt_id']}:{edge}")
            if count != 0:
                failures.append(f"receipt_forbidden_edge_nonzero:{receipt['receipt_id']}:{edge}:{count}")
        if receipt.get("proposal_applied") is not False:
            failures.append(f"proposal_to_patch_direct:{receipt['receipt_id']}")
        if receipt.get("repair_executed") is not False:
            failures.append(f"repair_executed:{receipt['receipt_id']}")
        if receipt.get("retry_executed") is not False:
            failures.append(f"retry_executed:{receipt['receipt_id']}")
        if receipt.get("builder_command_executed") is not False:
            failures.append(f"receipt_to_command_direct:{receipt['receipt_id']}")
        if receipt.get("cell1_authorized") is not False:
            failures.append(f"cell1_authorized:{receipt['receipt_id']}")
        if receipt.get("intercell_protocol_authorized") is not False:
            failures.append(f"intercell_protocol_authorized:{receipt['receipt_id']}")
        terminal = receipt["terminal"]
        if terminal["type"] != "STOP":
            failures.append(f"receipt_static_probe_advance:{receipt['receipt_id']}")
        if terminal.get("next_command_goal") is not None:
            failures.append(f"receipt_hidden_next:{receipt['receipt_id']}")

    for edge, count in rollup["forbidden_edge_counts"].items():
        if count != 0:
            failures.append(f"rollup_forbidden_edge_nonzero:{edge}:{count}")

    for key in ZERO_COUNTER_KEYS:
        if rollup.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup.get(key)}")

    if rollup.get("transfer_result") != "TRANSFERABLE_LOCAL_LOOP_V0":
        failures.append(f"transfer_result_not_transferable:{rollup.get('transfer_result')}")

    return failures

def make_profile(rollup: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "b3_local_decision_loop_lock_profile_v0",
        "profile_id": "b3_loop_lock_" + sha8({
            "loop_id": LOOP_ID,
            "result": rollup["transfer_result"],
            "surfaces": rollup["surfaces_tested"],
        }),
        "loop_id": LOOP_ID,
        "build_mode": BUILD_MODE,
        "status": rollup["transfer_result"],
        "locked_steps_ref": rel(STEP_ENUM_PATH),
        "transition_table_ref": rel(TRANSITION_TABLE_PATH),
        "surface_matrix_ref": rel(SURFACE_MATRIX_PATH),
        "transfer_rollup_ref": rel(TRANSFER_ROLLUP_PATH),
        "edge_artifact_license_map_ref": rel(LICENSE_MAP_PATH),
        "required_distinction_catalog_ref": rel(REQUIRED_DISTINCTION_CATALOG_PATH),
        "core_compression": "surface -> authorized inspection -> pressure classification -> required distinction -> availability -> lawful edge -> artifact -> receipt -> stop/advance",
        "forbidden_direct_edges_zero": True,
        "static_probe_advance_count_zero": rollup["static_probe_advance_count"] == 0,
        "must_not_infer": [
            "global closure",
            "Cell 1 readiness",
            "inter-cell protocol readiness",
            "final architecture",
            "automatic repair authority",
            "automatic retry authority",
        ],
        "next_command_goal": None,
    }

def make_transition_trace(profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "b3_transition_trace_v0",
        "trace": [
            {
                "step": "consume_b1_b2_reference_basis",
                "question": "were explicit accepted B1/B2 artifacts consumed as static/probe references",
                "answer": {"b1_receipt_id": SOURCE_B1_RECEIPT_ID, "b2_receipt_id": SOURCE_B2_RECEIPT_ID},
                "taken": "emit_loop_schema",
            },
            {
                "step": "emit_loop_schema",
                "question": "were loop schema, step/edge/forbidden-edge enums, distinction schema/catalog, transition table, license map, trace/receipt schemas emitted",
                "answer": True,
                "taken": "run_transfer_matrix",
            },
            {
                "step": "run_transfer_matrix",
                "question": "did declared surfaces pass through same loop without forbidden direct edges or bespoke paths",
                "answer": profile["status"],
                "taken": "stop",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_B3_LOCAL_DECISION_LOOP_SCHEMA_LOCKED" if profile["status"] == "TRANSFERABLE_LOCAL_LOOP_V0" else "STOP_B3_SURFACE_BESPOKE_PATH_DETECTED",
            "next_command_goal": None,
        },
    }

def make_report(matrix: List[Dict[str, Any]], traces: List[Dict[str, Any]], receipts: List[Dict[str, Any]], rollup: Dict[str, Any], profile: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "b3_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "source_design_consumed_count": 1,
        "b1_reference_basis_consumed_count": 1,
        "b2_reference_basis_consumed_count": 1,
        "loop_schema_emitted_count": 1,
        "step_enum_emitted_count": 1,
        "edge_enum_emitted_count": 1,
        "forbidden_edge_enum_emitted_count": 1,
        "required_distinction_schema_emitted_count": 1,
        "required_distinction_catalog_emitted_count": 1,
        "transition_table_emitted_count": 1,
        "trace_schema_emitted_count": 1,
        "receipt_schema_emitted_count": 1,
        "edge_artifact_license_map_emitted_count": 1,
        "surface_test_matrix_emitted_count": 1,
        "loop_trace_records_emitted_count": len(traces),
        "loop_receipts_emitted_count": len(receipts),
        "transfer_rollup_emitted_count": 1,
        "profile_emitted_count": 1,
        "surfaces_tested": len(matrix),
        "profile_status": profile["status"],
        "forbidden_direct_edges_zero": profile["forbidden_direct_edges_zero"],
        "cell1_authorization_count": 0,
        "intercell_protocol_authorization_count": 0,
        "live_repair_executed_count": 0,
        "retry_executed_count": 0,
        "taxonomy_mutation_count": 0,
        "registry_mutation_count": 0,
        "proposal_application_count": 0,
        "source_mutation_count": 0,
        "prior_receipt_mutation_count": 0,
        "domain_shift_authorization_count": 0,
        "hidden_next_command_count": rollup["hidden_next_command_count"],
        "latest_or_mtime_selection_count": 0,
        "ambient_workspace_inference_count": 0,
        "recommended_next_handling": None,
        "transfer_rollup_ref": rel(TRANSFER_ROLLUP_PATH),
    }

def validate_report(report: Dict[str, Any], rollup: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    for key in [
        "source_design_consumed_count",
        "b1_reference_basis_consumed_count",
        "b2_reference_basis_consumed_count",
        "loop_schema_emitted_count",
        "step_enum_emitted_count",
        "edge_enum_emitted_count",
        "forbidden_edge_enum_emitted_count",
        "required_distinction_schema_emitted_count",
        "required_distinction_catalog_emitted_count",
        "transition_table_emitted_count",
        "trace_schema_emitted_count",
        "receipt_schema_emitted_count",
        "edge_artifact_license_map_emitted_count",
        "surface_test_matrix_emitted_count",
        "transfer_rollup_emitted_count",
        "profile_emitted_count",
    ]:
        if report.get(key) != 1:
            failures.append(f"report_metric_not_one:{key}:{report.get(key)}")

    for key in [
        "cell1_authorization_count",
        "intercell_protocol_authorization_count",
        "live_repair_executed_count",
        "retry_executed_count",
        "taxonomy_mutation_count",
        "registry_mutation_count",
        "proposal_application_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "domain_shift_authorization_count",
        "hidden_next_command_count",
        "latest_or_mtime_selection_count",
        "ambient_workspace_inference_count",
    ]:
        if report.get(key) != 0:
            failures.append(f"report_metric_not_zero:{key}:{report.get(key)}")

    if rollup.get("transfer_result") != "TRANSFERABLE_LOCAL_LOOP_V0":
        failures.append("report_transfer_not_transferable")
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
    for key in [
        "source_design_consumed_count",
        "loop_schema_emitted_count",
        "step_enum_emitted_count",
        "edge_enum_emitted_count",
        "forbidden_edge_enum_emitted_count",
        "required_distinction_schema_emitted_count",
        "required_distinction_catalog_emitted_count",
        "transition_table_emitted_count",
        "trace_schema_emitted_count",
        "receipt_schema_emitted_count",
        "edge_artifact_license_map_emitted_count",
        "surface_test_matrix_emitted_count",
        "transfer_rollup_emitted_count",
        "profile_emitted_count",
    ]:
        if metrics.get(key) != 1:
            failures.append(f"receipt_metric_not_one:{key}:{metrics.get(key)}")
    for key in [
        "cell1_authorization_count",
        "intercell_protocol_authorization_count",
        "live_repair_executed_count",
        "retry_executed_count",
        "taxonomy_mutation_count",
        "registry_mutation_count",
        "proposal_application_count",
        "source_mutation_count",
        "prior_receipt_mutation_count",
        "domain_shift_authorization_count",
        "hidden_next_command_count",
        "latest_or_mtime_selection_count",
        "ambient_workspace_inference_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"receipt_metric_not_zero:{key}:{metrics.get(key)}")
    terminal = receipt.get("terminal", {})
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_B3_LOCAL_DECISION_LOOP_SCHEMA_LOCKED":
        failures.append(f"terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")
    return failures

def run_negative_controls(receipt_path: Path) -> List[Dict[str, Any]]:
    matrix = read_json(SURFACE_MATRIX_PATH)["surfaces"]
    traces = read_jsonl(TRACE_RECORDS_PATH)
    receipts = read_jsonl(LOOP_RECEIPTS_PATH)
    rollup = read_json(TRANSFER_ROLLUP_PATH)
    report = read_json(REPORT_PATH)

    controls: List[Dict[str, Any]] = []

    def add(case: str, failures: List[str], expected_fragment: str) -> None:
        controls.append({
            "case": case,
            "negative_control_pass": any(expected_fragment in f for f in failures),
            "failures": failures,
            "wrote_live_artifact": False,
        })

    for case, forbidden_edge in [
        ("pressure_to_repair_direct_fail", "PRESSURE_TO_REPAIR_DIRECT"),
        ("failure_to_retry_direct_fail", "FAILURE_TO_RETRY_DIRECT"),
        ("receipt_to_command_direct_fail", "RECEIPT_TO_COMMAND_DIRECT"),
        ("proposal_to_patch_direct_fail", "PROPOSAL_TO_PATCH_DIRECT"),
        ("label_to_identity_direct_fail", "LABEL_TO_IDENTITY_DIRECT"),
        ("authority_boundary_to_execution_direct_fail", "AUTHORITY_BOUNDARY_TO_EXECUTION_DIRECT"),
    ]:
        bad_rollup = copy.deepcopy(rollup)
        bad_rollup["forbidden_edge_counts"][forbidden_edge] = 1
        add(case, validate_records(matrix, traces, receipts, bad_rollup), f"rollup_forbidden_edge_nonzero:{forbidden_edge}")

    bad_matrix = copy.deepcopy(matrix)
    bad_matrix[0]["required_distinction"] = None
    add("missing_required_distinction_fail", validate_records(bad_matrix, traces, receipts, rollup), "required_distinction_missing")

    bad_matrix = copy.deepcopy(matrix)
    bad_matrix[0]["distinction_status"] = None
    add("distinction_without_availability_fail", validate_records(bad_matrix, traces, receipts, rollup), "distinction_status_invalid")

    bad_matrix = copy.deepcopy(matrix)
    bad_matrix[0]["artifact_kind"] = "patch"
    add("artifact_not_licensed_by_edge_fail", validate_records(bad_matrix, traces, receipts, rollup), "artifact_not_licensed_by_edge")

    bad_traces = copy.deepcopy(traces)
    bad_traces[0]["surface_bespoke_path_used"] = True
    add("surface_bespoke_path_fail", validate_records(matrix, bad_traces, receipts, rollup), "surface_bespoke_path_used")

    bad_receipts = copy.deepcopy(receipts)
    bad_receipts[0]["surface_ref"] = "missing_surface"
    add("missing_receipt_fail", validate_records(matrix, traces, bad_receipts, rollup), "receipt_missing")

    bad_receipts = copy.deepcopy(receipts)
    bad_receipts[0]["terminal"]["next_command_goal"] = "OPEN_NEXT_OBJECTIVE"
    add("hidden_next_command_fail", validate_records(matrix, traces, bad_receipts, rollup), "receipt_hidden_next")

    bad_report = copy.deepcopy(report)
    bad_report["cell1_authorization_count"] = 1
    add("cell1_authorized_fail", validate_report(bad_report, rollup), "cell1_authorization_count")

    bad_report = copy.deepcopy(report)
    bad_report["intercell_protocol_authorization_count"] = 1
    add("intercell_protocol_authorized_fail", validate_report(bad_report, rollup), "intercell_protocol_authorization_count")

    bad_report = copy.deepcopy(report)
    bad_report["source_mutation_count"] = 1
    add("source_mutation_fail", validate_report(bad_report, rollup), "source_mutation_count")

    bad_report = copy.deepcopy(report)
    bad_report["prior_receipt_mutation_count"] = 1
    add("prior_receipt_mutation_fail", validate_report(bad_report, rollup), "prior_receipt_mutation_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["static_probe_advance_count"] = 1
    add("static_probe_advance_fail", validate_records(matrix, traces, receipts, bad_rollup), "static_probe_advance_count")

    bad_rollup = copy.deepcopy(rollup)
    bad_rollup["edge_artifact_mismatch_count"] = 1
    add("edge_artifact_mismatch_rollup_fail", validate_records(matrix, traces, receipts, bad_rollup), "edge_artifact_mismatch_count")

    return controls

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures = validate_source_basis()

    if failures:
        terminal = {"type": "STOP", "stop_code": "STOP_B3_DEPENDENCY_MISSING", "next_command_goal": None}
        receipt_id = sha8({"unit_id": UNIT_ID, "failures": failures, "terminal": terminal})
        receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
        receipt = {
            "schema_version": "b3_local_decision_loop_schema_lock_receipt_v0",
            "receipt_type": "B3_LOCAL_DECISION_LOOP_SCHEMA_LOCK_RECEIPT",
            "receipt_id": receipt_id,
            "unit_id": UNIT_ID,
            "target_unit_id": TARGET_UNIT_ID,
            "gate": "FAIL",
            "failures": failures,
            "terminal": terminal,
            "created_at": now_iso(),
        }
        write_json(receipt_path, receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        print(f"b3_receipt_id={receipt_id}")
        print(f"b3_receipt_path=data/b3_cell0_local_decision_loop_schema_lock_v0_receipts/{receipt_id}.json")
        return 1

    for path, obj in schemas().items():
        write_json(path, obj)

    matrix, traces, receipts = build_records()
    rollup = transfer_rollup(matrix, traces, receipts)
    profile = make_profile(rollup)
    transition = make_transition_trace(profile)
    report = make_report(matrix, traces, receipts, rollup, profile)

    write_json(SURFACE_MATRIX_PATH, {
        "schema_version": "local_decision_loop_surface_test_matrix_v0",
        "build_mode": BUILD_MODE,
        "loop_id": LOOP_ID,
        "surfaces": matrix,
    })
    append_jsonl(TRACE_RECORDS_PATH, traces)
    append_jsonl(LOOP_RECEIPTS_PATH, receipts)
    write_json(TRANSFER_ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(TRANSITION_TRACE_PATH, transition)
    write_json(REPORT_PATH, report)

    failures.extend(validate_records(matrix, traces, receipts, rollup))
    failures.extend(validate_report(report, rollup))

    source_after = snapshot_files(REQUIRED_SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")
        rollup["source_mutation_count"] = 1
        report["source_mutation_count"] = 1
        write_json(TRANSFER_ROLLUP_PATH, rollup)
        write_json(REPORT_PATH, report)

    acceptance_gate_results = {
        "B3_LOOP_0_SOURCE_DESIGN_CONSUMED": True,
        "B3_LOOP_1_BUILD_MODE_DECLARED": BUILD_MODE == "STATIC_SCHEMA_AND_PROBE_ONLY",
        "B3_LOOP_2_LOOP_SCHEMA_EMITTED": LOOP_SCHEMA_PATH.exists(),
        "B3_LOOP_3_STEP_ENUM_EMITTED": STEP_ENUM_PATH.exists(),
        "B3_LOOP_4_EDGE_ENUM_EMITTED": EDGE_ENUM_PATH.exists(),
        "B3_LOOP_5_FORBIDDEN_EDGE_ENUM_EMITTED": FORBIDDEN_EDGE_ENUM_PATH.exists(),
        "B3_LOOP_6_REQUIRED_DISTINCTION_SCHEMA_EMITTED": REQUIRED_DISTINCTION_SCHEMA_PATH.exists(),
        "B3_LOOP_7_TRANSITION_TABLE_EMITTED": TRANSITION_TABLE_PATH.exists(),
        "B3_LOOP_8_TRACE_SCHEMA_EMITTED": TRACE_SCHEMA_PATH.exists(),
        "B3_LOOP_9_RECEIPT_SCHEMA_EMITTED": RECEIPT_SCHEMA_PATH.exists(),
        "B3_LOOP_10_SURFACE_TEST_MATRIX_EMITTED": SURFACE_MATRIX_PATH.exists() and len(matrix) == 10,
        "B3_LOOP_11_EVERY_SURFACE_USES_SAME_LOOP": all(row["uses_same_loop"] is True for row in matrix),
        "B3_LOOP_12_EVERY_NONTRIVIAL_SURFACE_NAMES_REQUIRED_DISTINCTION": all(row.get("required_distinction") for row in matrix),
        "B3_LOOP_13_EVERY_DISTINCTION_HAS_AVAILABILITY_STATUS": all(row.get("distinction_status") in DISTINCTION_STATUSES for row in matrix),
        "B3_LOOP_14_EVERY_SELECTED_EDGE_CLOSED_ENUM": all(row["selected_edge"] in EDGE_TYPES for row in matrix),
        "B3_LOOP_15_EVERY_ARTIFACT_LICENSED_BY_EDGE": all(artifact_licensed(row) for row in matrix),
        "B3_LOOP_16_EVERY_RUN_EMITS_RECEIPT": len(receipts) == len(matrix),
        "B3_LOOP_17_FORBIDDEN_DIRECT_EDGES_ZERO": all(v == 0 for v in rollup["forbidden_edge_counts"].values()),
        "B3_LOOP_18_NO_SURFACE_BESPOKE_PATH": rollup["surface_bespoke_path_count"] == 0,
        "B3_LOOP_19_NO_PROPOSAL_TO_PATCH": rollup["proposal_applied_count"] == 0,
        "B3_LOOP_20_NO_LABEL_TO_IDENTITY": all(row["required_distinction"] != "workflow_position_label == object_identity" for row in matrix),
        "B3_LOOP_21_NO_AUTHORITY_BOUNDARY_TO_EXECUTION": all(not (r["pressure_group"] == "AUTHORITY_PRESSURE" and r["selected_edge"] == "APPLY_LOCAL_MOVE") for r in receipts),
        "B3_LOOP_22_NO_HIDDEN_NEXT_COMMAND": rollup["hidden_next_command_count"] == 0 and transition["terminal"]["next_command_goal"] is None,
        "B3_LOOP_23_TRANSFER_ROLLUP_EMITTED": TRANSFER_ROLLUP_PATH.exists(),
        "B3_LOOP_24_PROFILE_EMITTED": PROFILE_PATH.exists(),
        "B3_LOOP_25_EDGE_ARTIFACT_LICENSE_MAP_EMITTED": LICENSE_MAP_PATH.exists(),
        "B3_LOOP_26_EVERY_ARTIFACT_LICENSED_BY_EDGE_MAP": rollup["edge_artifact_mismatch_count"] == 0,
        "B3_LOOP_27_STATIC_PROBE_ADVANCE_COUNT_ZERO": rollup["static_probe_advance_count"] == 0,
        "B3_LOOP_28_REQUIRED_DISTINCTION_CATALOG_EMITTED": REQUIRED_DISTINCTION_CATALOG_PATH.exists(),
        "B3_LOOP_29_EVERY_REQUIRED_DISTINCTION_CATALOGUED_OR_TYPED_STOP": rollup["uncatalogued_distinction_count"] == 0,
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = transition["terminal"]
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_b1": SOURCE_B1_RECEIPT_ID,
        "source_b2": SOURCE_B2_RECEIPT_ID,
        "loop_id": LOOP_ID,
        "status": profile["status"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "local_decision_loop_schema": rel(LOOP_SCHEMA_PATH),
        "local_decision_loop_step_enum": rel(STEP_ENUM_PATH),
        "local_decision_loop_edge_enum": rel(EDGE_ENUM_PATH),
        "local_decision_loop_forbidden_edge_enum": rel(FORBIDDEN_EDGE_ENUM_PATH),
        "local_required_distinction_record_schema": rel(REQUIRED_DISTINCTION_SCHEMA_PATH),
        "local_required_distinction_catalog": rel(REQUIRED_DISTINCTION_CATALOG_PATH),
        "local_decision_loop_transition_table": rel(TRANSITION_TABLE_PATH),
        "local_decision_loop_trace_schema": rel(TRACE_SCHEMA_PATH),
        "local_decision_loop_receipt_schema": rel(RECEIPT_SCHEMA_PATH),
        "local_decision_loop_edge_artifact_license_map": rel(LICENSE_MAP_PATH),
        "local_decision_loop_surface_test_matrix": rel(SURFACE_MATRIX_PATH),
        "local_decision_loop_trace_records": rel(TRACE_RECORDS_PATH),
        "local_decision_loop_receipts": rel(LOOP_RECEIPTS_PATH),
        "local_decision_loop_transfer_rollup": rel(TRANSFER_ROLLUP_PATH),
        "b3_loop_lock_profile": rel(PROFILE_PATH),
        "b3_transition_trace": rel(TRANSITION_TRACE_PATH),
        "b3_report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
        "source_b1_receipt": rel(SOURCE_B1_RECEIPT_PATH),
        "source_b2_receipt": rel(SOURCE_B2_RECEIPT_PATH),
    }

    aggregate_metrics = {
        **{k: v for k, v in report.items() if k not in {"schema_version", "unit_id", "target_unit_id"}},
        **{f"rollup_{k}": v for k, v in rollup.items() if k not in {"schema_version", "loop_step_failure_counts", "forbidden_edge_counts"}},
        "loop_step_failure_counts": rollup["loop_step_failure_counts"],
        "forbidden_edge_counts": rollup["forbidden_edge_counts"],
        "source_mutation_count": 1 if source_mutation_detected else report["source_mutation_count"],
    }

    guards = {
        "build_mode_static_schema_and_probe_only": BUILD_MODE == "STATIC_SCHEMA_AND_PROBE_ONLY",
        "b1_reference_basis_consumed": True,
        "b2_reference_basis_consumed": True,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_inference_used": False,
        "closed_steps_only": True,
        "closed_edges_only": True,
        "forbidden_direct_edges_zero": all(v == 0 for v in rollup["forbidden_edge_counts"].values()),
        "same_loop_for_every_surface": all(row["uses_same_loop"] for row in matrix),
        "required_distinction_before_edge": True,
        "edge_artifact_license_map_enforced": True,
        "static_probe_advance_used": False,
        "proposal_to_patch": False,
        "label_to_identity": False,
        "authority_boundary_to_execution": False,
        "cell1_authorized": False,
        "intercell_protocol_authorized": False,
        "repair_executed": False,
        "retry_executed": False,
        "taxonomy_mutated": False,
        "registry_mutated": False,
        "source_mutated": source_mutation_detected,
        "prior_receipts_mutated": False,
        "hidden_next_command": False,
    }

    receipt = {
        "schema_version": "b3_local_decision_loop_schema_lock_receipt_v0",
        "receipt_type": "B3_LOCAL_DECISION_LOOP_SCHEMA_LOCK_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "active_object": "Cell 0 local decision loop across multiple declared pressure surfaces",
        "source_b1_receipt_id": SOURCE_B1_RECEIPT_ID,
        "source_b2_receipt_id": SOURCE_B2_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "b3_summary": {
            "loop_id": LOOP_ID,
            "profile_status": profile["status"],
            "surfaces_tested": rollup["surfaces_tested"],
            "surfaces_passed": rollup["surfaces_passed"],
            "forbidden_direct_edges_zero": all(v == 0 for v in rollup["forbidden_edge_counts"].values()),
            "surface_bespoke_path_count": rollup["surface_bespoke_path_count"],
            "edge_artifact_mismatch_count": rollup["edge_artifact_mismatch_count"],
            "static_probe_advance_count": rollup["static_probe_advance_count"],
            "uncatalogued_distinction_count": rollup["uncatalogued_distinction_count"],
            "hidden_next_command_count": rollup["hidden_next_command_count"],
            "recommended_next_handling": None,
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "b3_guards": guards,
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

    negative_controls = run_negative_controls(receipt_path)
    if len(negative_controls) != 18 or not all(row["negative_control_pass"] and row["wrote_live_artifact"] is False for row in negative_controls):
        receipt = read_json(receipt_path)
        receipt["gate"] = "FAIL"
        receipt["failures"].append("negative_controls_failed")
        receipt["negative_controls"] = negative_controls
        receipt["terminal"] = {"type": "STOP", "stop_code": "STOP_GATE_FAIL", "next_command_goal": None}
        write_json(receipt_path, receipt)
        print(json.dumps(receipt, indent=2, sort_keys=True))
        return 1

    receipt = read_json(receipt_path)
    receipt["negative_controls"] = negative_controls
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"b3_receipt_id={receipt_id}")
    print(f"b3_receipt_path=data/b3_cell0_local_decision_loop_schema_lock_v0_receipts/{receipt_id}.json")
    print(f"b3_profile_path=data/b3_cell0_local_decision_loop_schema_lock_v0/b3_loop_lock_profile_v0.json")
    print(f"b3_rollup_path=data/b3_cell0_local_decision_loop_schema_lock_v0/local_decision_loop_transfer_rollup_v0.json")
    print(f"b3_loop_schema_path=data/b3_cell0_local_decision_loop_schema_lock_v0/local_decision_loop_schema_v0.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
