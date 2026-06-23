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

UNIT_ID = "BUILD_CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_PROTOCOL_V0"
TARGET_UNIT_ID = "current_surface_pressure_handling_loop_protocol.v0"

SOURCE_EXPECTED_LIMIT_RECEIPT_ID = "cbde4b69"
SOURCE_UPSTREAM_AUDIT_RECEIPT_ID = "6b1ea913"
SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID = "11d585b6"
SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID = "8617577b"
SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID = "2d9417fc"
SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID = "6148b4fa"
SOURCE_PRESSURE_LOOP_APPLICATION_RECEIPT_ID = "be19f438"

OUT_DIR = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0"
RECEIPT_DIR = ROOT / "data" / "current_surface_pressure_handling_loop_protocol_v0_receipts"

PROTOCOL_PATH = OUT_DIR / "current_surface_pressure_loop_protocol.json"
SURFACE_STATE_SCHEMA_PATH = OUT_DIR / "surface_state_record_schema.json"
TRANSITION_TABLE_PATH = OUT_DIR / "surface_transition_decision_table.json"
CAPABILITY_STOP_SCHEMA_PATH = OUT_DIR / "capability_stop_packet_schema.json"
ACCEPTANCE_GATES_PATH = OUT_DIR / "pressure_loop_acceptance_gates.json"
REPORT_PATH = OUT_DIR / "current_surface_pressure_loop_protocol_report.json"

EXPECTED_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0_receipts" / f"{SOURCE_EXPECTED_LIMIT_RECEIPT_ID}.json"
EXPECTED_LIMIT_MARKER_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0" / "expected_source_content_limit_marker.json"
EXPECTED_LIMIT_CLOSURE_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0" / "expected_source_content_limit_closure_record.json"
EXPECTED_LIMIT_PACKET_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0" / "expected_source_content_limit_decision_packet.json"
EXPECTED_LIMIT_REPORT_PATH = ROOT / "data" / "field_introduced_surface_expected_source_content_limit_v0" / "expected_source_content_limit_report.json"

UPSTREAM_AUDIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_upstream_existence_audit_v0_receipts" / f"{SOURCE_UPSTREAM_AUDIT_RECEIPT_ID}.json"
NULL_LIMIT_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_null_evidence_limit_classification_v0_receipts" / f"{SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID}.json"
FIELD_INTRO_RERUN_RECEIPT_PATH = ROOT / "data" / "field_introduced_surface_taxonomy_gap_missing_label_evidence_rerun_v0_receipts" / f"{SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID}.json"
FIELD_INTRO_BUILD_RECEIPT_PATH = ROOT / "data" / "source_provenance_field_introduction_build_v0_receipts" / f"{SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID}.json"
BASE_PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH = ROOT / "data" / "pressure_handling_loop_protocol_v0_receipts" / f"{SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID}.json"
BASE_PRESSURE_LOOP_APPLICATION_RECEIPT_PATH = ROOT / "data" / "pressure_loop_applications" / "r1000_top_group_taxonomy_gap_v0_receipts" / f"{SOURCE_PRESSURE_LOOP_APPLICATION_RECEIPT_ID}.json"

SOURCE_FILES = [
    EXPECTED_LIMIT_RECEIPT_PATH,
    EXPECTED_LIMIT_MARKER_PATH,
    EXPECTED_LIMIT_CLOSURE_PATH,
    EXPECTED_LIMIT_PACKET_PATH,
    EXPECTED_LIMIT_REPORT_PATH,
    UPSTREAM_AUDIT_RECEIPT_PATH,
    NULL_LIMIT_RECEIPT_PATH,
    FIELD_INTRO_RERUN_RECEIPT_PATH,
    FIELD_INTRO_BUILD_RECEIPT_PATH,
    BASE_PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH,
    BASE_PRESSURE_LOOP_APPLICATION_RECEIPT_PATH,
]

CURRENT_SURFACE_TYPES = [
    "pressure_queue_surface",
    "pressure_group_surface",
    "evidence_surface",
    "repaired_evidence_surface",
    "field_introduced_surface",
    "null_evidence_limit_surface",
    "upstream_audit_surface",
    "expected_limit_closure_surface",
    "capability_stop_surface",
]

MISSING_OBJECT_TYPES = [
    "missing_evidence",
    "missing_surface",
    "missing_field_representation",
    "missing_value",
    "missing_provenance",
    "broken_reference",
    "current_source_content_absent",
    "upstream_existence_unresolved",
    "expected_limit_candidate",
    "capability_boundary_unknown",
    "human_decision_required",
]

STOP_CODES = [
    "STOP_NO_ACTIONABLE_PRESSURE",
    "STOP_NEEDS_PRESSURE_CLASSIFICATION",
    "STOP_SURFACE_DEFICIENCY_UNLOCALIZED",
    "STOP_UNREPRESENTABLE_WITH_CURRENT_AUTHORITY",
    "STOP_AUTHORITY_VIOLATION",
    "STOP_HUMAN_DECISION_REQUIRED",
    "STOP_CAPABILITY_LAYER_REQUIRED",
    "STOP_AUDIT_SCOPE_INSUFFICIENT",
    "STOP_BRANCH_CLOSED_EXPECTED_SOURCE_CONTENT_LIMIT",
]

HUMAN_DECISION = {
    "decision": "BUILD_CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_PROTOCOL",
    "scope": "freeze the current-surface pressure-handling loop before applying it to R1000 pressure surfaces",
    "authorized": [
        "define current surface types",
        "define shared surface-state record schema",
        "define yes/no transition table",
        "define capability-stop packet schema",
        "define authority and closure acceptance gates",
    ],
    "not_authorized": [
        "running R1000 pressure queue",
        "opening next pressure group",
        "inventing values",
        "creating taxonomy labels",
        "upgrading taxonomy",
        "mutating source rows",
        "mutating existing receipts",
        "claiming a final/global taxonomy",
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
        "expected_limit_receipt": read_json(EXPECTED_LIMIT_RECEIPT_PATH),
        "expected_limit_marker": read_json(EXPECTED_LIMIT_MARKER_PATH),
        "expected_limit_closure": read_json(EXPECTED_LIMIT_CLOSURE_PATH),
        "expected_limit_packet": read_json(EXPECTED_LIMIT_PACKET_PATH),
        "expected_limit_report": read_json(EXPECTED_LIMIT_REPORT_PATH),
        "upstream_audit_receipt": read_json(UPSTREAM_AUDIT_RECEIPT_PATH),
        "null_limit_receipt": read_json(NULL_LIMIT_RECEIPT_PATH),
        "field_intro_rerun_receipt": read_json(FIELD_INTRO_RERUN_RECEIPT_PATH),
        "field_intro_build_receipt": read_json(FIELD_INTRO_BUILD_RECEIPT_PATH),
        "base_pressure_loop_protocol_receipt": read_json(BASE_PRESSURE_LOOP_PROTOCOL_RECEIPT_PATH),
        "base_pressure_loop_application_receipt": read_json(BASE_PRESSURE_LOOP_APPLICATION_RECEIPT_PATH),
    }

def validate_sources(sources: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    expected = sources["expected_limit_receipt"]
    expected_metrics = expected.get("aggregate_metrics", {})

    if expected.get("receipt_id") != SOURCE_EXPECTED_LIMIT_RECEIPT_ID:
        failures.append("expected_limit_receipt_id_wrong")
    if expected.get("gate") != "PASS":
        failures.append("expected_limit_not_pass")
    if expected_metrics.get("branch_closed") is not True:
        failures.append("expected_limit_branch_not_closed")
    if expected_metrics.get("expected_limit_marked") is not True:
        failures.append("expected_limit_not_marked")
    if expected_metrics.get("next_group_auto_opened_count") != 0:
        failures.append("source_expected_limit_auto_opened_next_group")
    if expected_metrics.get("hidden_next_command_count") != 0:
        failures.append("source_expected_limit_hidden_next_command")
    if expected_metrics.get("field_value_invention_count") != 0:
        failures.append("source_expected_limit_invented_values")
    if expected_metrics.get("taxonomy_delta_proposal_emitted_count") != 0:
        failures.append("source_expected_limit_taxonomy_delta")
    if expected_metrics.get("universal_upstream_nonexistence_proven") is not False:
        failures.append("source_expected_limit_universal_nonexistence_overclaim")

    if sources["upstream_audit_receipt"].get("receipt_id") != SOURCE_UPSTREAM_AUDIT_RECEIPT_ID:
        failures.append("upstream_audit_receipt_id_wrong")
    if sources["null_limit_receipt"].get("receipt_id") != SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID:
        failures.append("null_limit_receipt_id_wrong")
    if sources["field_intro_rerun_receipt"].get("receipt_id") != SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID:
        failures.append("field_intro_rerun_receipt_id_wrong")
    if sources["field_intro_build_receipt"].get("receipt_id") != SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID:
        failures.append("field_intro_build_receipt_id_wrong")
    if sources["base_pressure_loop_protocol_receipt"].get("receipt_id") != SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID:
        failures.append("base_pressure_loop_protocol_receipt_id_wrong")
    if sources["base_pressure_loop_application_receipt"].get("receipt_id") != SOURCE_PRESSURE_LOOP_APPLICATION_RECEIPT_ID:
        failures.append("base_pressure_loop_application_receipt_id_wrong")

    for path in SOURCE_FILES:
        if not path.exists():
            failures.append(f"source_missing:{rel(path)}")
        elif not tracked(path):
            failures.append(f"source_not_tracked:{rel(path)}")

    return failures

def build_surface_state_record_schema() -> Dict[str, Any]:
    return {
        "schema_version": "current_surface_state_record_schema_v0",
        "record_type": "CURRENT_SURFACE_STATE_RECORD",
        "scope": "current_surfaces_only",
        "surface_types": CURRENT_SURFACE_TYPES,
        "required_fields": [
            "surface_id",
            "surface_type",
            "source_receipt_id",
            "pressure_group_key",
            "row_count",
            "key_visibility",
            "value_state",
            "provenance_state",
            "authority_state",
            "classification",
            "capability_state",
            "terminal",
        ],
        "field_definitions": {
            "surface_id": "stable identifier for the observed surface",
            "surface_type": "one of current surface types",
            "source_receipt_id": "receipt that produced or justified the surface",
            "pressure_group_key": "pressure-group identity, if applicable",
            "row_count": "number of rows represented by the surface, if row-backed",
            "key_visibility": {
                "required_keys_visible": "bool",
                "missing_keys": "list[str]",
            },
            "value_state": {
                "values_present": "bool",
                "values_absent": "bool",
                "value_invention_count": "int",
            },
            "provenance_state": {
                "absence_reasons_present": "bool",
                "provenance_refs_present": "bool",
                "structural_refs_preserved": "bool",
            },
            "authority_state": {
                "source_mutation_count": "int",
                "receipt_mutation_count": "int",
                "taxonomy_action_count": "int",
                "hidden_next_command_count": "int",
                "next_group_auto_opened_count": "int",
            },
            "classification": {
                "current_class": "string|null",
                "limit_type": "string|null",
                "branch_resolution": "string|null",
            },
            "capability_state": {
                "required_capability": "string|null",
                "capability_available": "bool|null",
                "capability_stop_required": "bool",
            },
            "terminal": {
                "terminal_type": "STOP|ADVANCE|PASS|null",
                "stop_code": "string|null",
                "next_command_goal": "string|null",
            },
        },
        "non_goals": [
            "does_not_define_all_future_surfaces",
            "does_not_define_final_taxonomy",
            "does_not_authorize_value_invention",
            "does_not_authorize_automatic_next_group_open",
        ],
    }

def build_transition_table() -> Dict[str, Any]:
    return {
        "schema_version": "current_surface_transition_decision_table_v0",
        "table_type": "YES_NO_SURFACE_TRANSITION_TABLE",
        "scope": "current_surface_pressure_loop",
        "transitions": [
            {
                "step": "select_pressure_group",
                "question": "pressure_group_selected",
                "yes": "inspect_pressure_group_surface",
                "no": "STOP_NO_ACTIONABLE_PRESSURE",
            },
            {
                "step": "inspect_pressure_group_surface",
                "question": "pressure_class_understood_enough_to_choose_inspection",
                "yes": "extract_evidence_surface",
                "no": "STOP_NEEDS_PRESSURE_CLASSIFICATION",
            },
            {
                "step": "extract_evidence_surface",
                "question": "required_evidence_values_visible",
                "yes": "classify_value_evidence",
                "no": "classify_evidence_surface_deficiency",
            },
            {
                "step": "classify_evidence_surface_deficiency",
                "question": "deficiency_localized",
                "yes": "inspect_localized_deficiency",
                "no": "localize_evidence_surface_deficiency",
            },
            {
                "step": "inspect_localized_deficiency",
                "question": "required_keys_or_fields_present",
                "yes": "inspect_value_and_provenance_state",
                "no": "field_or_schema_representation_branch",
            },
            {
                "step": "field_or_schema_representation_branch",
                "question": "missing_representation_can_be_introduced_without_inventing_values",
                "yes": "propose_versioned_field_or_schema_introduction",
                "no": "STOP_UNREPRESENTABLE_WITH_CURRENT_AUTHORITY",
            },
            {
                "step": "propose_versioned_field_or_schema_introduction",
                "question": "human_accepts_introduction",
                "yes": "build_versioned_introduction",
                "no": "STOP_HUMAN_DECISION_REQUIRED",
            },
            {
                "step": "build_versioned_introduction",
                "question": "build_invented_values_or_mutated_source",
                "yes": "STOP_AUTHORITY_VIOLATION",
                "no": "rerun_extraction_on_introduced_surface",
            },
            {
                "step": "rerun_extraction_on_introduced_surface",
                "question": "introduced_field_keys_visible",
                "yes": "inspect_value_and_provenance_state",
                "no": "repair_field_introduced_surface",
            },
            {
                "step": "inspect_value_and_provenance_state",
                "question": "values_present",
                "yes": "classify_value_evidence",
                "no": "classify_null_evidence_limit",
            },
            {
                "step": "classify_null_evidence_limit",
                "question": "current_evidence_resolves_upstream_existence",
                "yes": "classify_resolved_source_state",
                "no": "human_decision_for_upstream_audit_or_limit",
            },
            {
                "step": "human_decision_for_upstream_audit_or_limit",
                "question": "upstream_existence_audit_authorized",
                "yes": "audit_upstream_existence",
                "no": "STOP_HUMAN_DECISION_REQUIRED",
            },
            {
                "step": "audit_upstream_existence",
                "question": "non_null_values_found_in_audited_chain",
                "yes": "classify_upstream_value_evidence",
                "no": "expected_source_content_limit_candidate",
            },
            {
                "step": "expected_source_content_limit_candidate",
                "question": "mark_expected_source_content_limit_authorized",
                "yes": "mark_expected_source_content_limit",
                "no": "STOP_HUMAN_DECISION_REQUIRED",
            },
            {
                "step": "mark_expected_source_content_limit",
                "question": "marker_overclaims_universal_absence_or_authorizes_value_taxonomy_repair",
                "yes": "STOP_AUTHORITY_VIOLATION",
                "no": "close_pressure_branch",
            },
            {
                "step": "any_step",
                "question": "required_next_move_exceeds_current_capability",
                "yes": "STOP_CAPABILITY_LAYER_REQUIRED",
                "no": "continue_current_transition",
            },
        ],
        "terminal_stop_codes": STOP_CODES,
    }

def build_capability_stop_packet_schema() -> Dict[str, Any]:
    return {
        "schema_version": "capability_stop_packet_schema_v0",
        "packet_type": "CAPABILITY_STOP_PACKET",
        "required_fields": [
            "stop_id",
            "source_surface_id",
            "source_receipt_id",
            "pressure_group_key",
            "surface_type",
            "missing_object_type",
            "required_capability",
            "capability_available",
            "why_current_capability_cannot_continue",
            "evidence_already_collected",
            "authority_guards",
            "safe_human_choices",
            "terminal",
        ],
        "field_constraints": {
            "missing_object_type": MISSING_OBJECT_TYPES,
            "capability_available": False,
            "terminal.stop_code": "STOP_CAPABILITY_LAYER_REQUIRED",
            "terminal.next_command_goal": None,
            "authority_guards.value_invention_count": 0,
            "authority_guards.source_mutation_count": 0,
            "authority_guards.receipt_mutation_count": 0,
            "authority_guards.hidden_next_command_count": 0,
        },
        "safe_human_choices": [
            "AUTHORIZE_CAPABILITY_BUILD",
            "REQUEST_NARROWER_INSPECTION",
            "MARK_EXPECTED_LIMIT_IF_EVIDENCE_SUPPORTS_IT",
            "REJECT_CAPABILITY_STOP_AS_INSUFFICIENT",
            "RETURN_TO_PRESSURE_QUEUE",
        ],
        "non_goals": [
            "does_not_build_the_missing_capability",
            "does_not_guess_values",
            "does_not_auto_open_next_group",
        ],
    }

def build_acceptance_gates() -> Dict[str, Any]:
    gates = [
        "CURRENT_SURFACE_LOOP_0_SOURCE_BRANCH_CLOSURE_CONSUMED",
        "CURRENT_SURFACE_LOOP_1_CURRENT_SURFACE_TYPES_DEFINED",
        "CURRENT_SURFACE_LOOP_2_SURFACE_STATE_RECORD_SCHEMA_EMITTED",
        "CURRENT_SURFACE_LOOP_3_YES_NO_TRANSITION_TABLE_EMITTED",
        "CURRENT_SURFACE_LOOP_4_CAPABILITY_STOP_PACKET_SCHEMA_EMITTED",
        "CURRENT_SURFACE_LOOP_5_AUTHORITY_GUARDS_DEFINED",
        "CURRENT_SURFACE_LOOP_6_EXPECTED_LIMIT_CLOSURE_PATH_DEFINED",
        "CURRENT_SURFACE_LOOP_7_NO_VALUE_INVENTION_OR_TAXONOMY_ACTION",
        "CURRENT_SURFACE_LOOP_8_NO_GLOBAL_OR_FINAL_TAXONOMY_CLAIM",
        "CURRENT_SURFACE_LOOP_9_NO_R1000_RUN_OR_NEXT_GROUP_AUTO_OPEN",
        "CURRENT_SURFACE_LOOP_10_NO_HIDDEN_NEXT_COMMAND",
    ]
    return {
        "schema_version": "current_surface_pressure_loop_acceptance_gates_v0",
        "gates": gates,
        "gate_requirements": {
            "CURRENT_SURFACE_LOOP_0_SOURCE_BRANCH_CLOSURE_CONSUMED": "expected-limit branch closure receipt must be PASS and branch_closed=true",
            "CURRENT_SURFACE_LOOP_1_CURRENT_SURFACE_TYPES_DEFINED": "current surface types list must be finite and current-scope only",
            "CURRENT_SURFACE_LOOP_2_SURFACE_STATE_RECORD_SCHEMA_EMITTED": "surface-state record schema must include evidence, provenance, authority, capability, and terminal state",
            "CURRENT_SURFACE_LOOP_3_YES_NO_TRANSITION_TABLE_EMITTED": "transition table must use explicit yes/no decisions",
            "CURRENT_SURFACE_LOOP_4_CAPABILITY_STOP_PACKET_SCHEMA_EMITTED": "capability-stop schema must expose missing object and required capability",
            "CURRENT_SURFACE_LOOP_5_AUTHORITY_GUARDS_DEFINED": "authority guards must prohibit source mutation, receipt mutation, value invention, taxonomy action, hidden command",
            "CURRENT_SURFACE_LOOP_6_EXPECTED_LIMIT_CLOSURE_PATH_DEFINED": "expected-limit path must close branch without universal nonexistence overclaim",
            "CURRENT_SURFACE_LOOP_7_NO_VALUE_INVENTION_OR_TAXONOMY_ACTION": "protocol emits zero authorizations for value invention or taxonomy action",
            "CURRENT_SURFACE_LOOP_8_NO_GLOBAL_OR_FINAL_TAXONOMY_CLAIM": "protocol must be explicitly local/current-surface scoped",
            "CURRENT_SURFACE_LOOP_9_NO_R1000_RUN_OR_NEXT_GROUP_AUTO_OPEN": "protocol build must not run R1000 or open next pressure group",
            "CURRENT_SURFACE_LOOP_10_NO_HIDDEN_NEXT_COMMAND": "terminal must stop for human/application decision with next_command_goal null",
        },
    }

def build_protocol(surface_schema: Dict[str, Any], transition_table: Dict[str, Any], capability_schema: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "current_surface_pressure_handling_loop_protocol_v0",
        "protocol_id": sha8({
            "unit": UNIT_ID,
            "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
            "surface_types": CURRENT_SURFACE_TYPES,
            "transition_count": len(transition_table["transitions"]),
        }),
        "protocol_name": "CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_PROTOCOL_V0",
        "scope": "current_surface_pressure_loop_only",
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_upstream_audit_receipt_id": SOURCE_UPSTREAM_AUDIT_RECEIPT_ID,
        "surface_types": CURRENT_SURFACE_TYPES,
        "missing_object_types": MISSING_OBJECT_TYPES,
        "loop_shape": [
            "select_pressure_group",
            "inspect_current_surface",
            "classify_evidence_sufficiency",
            "identify_missing_object_when_blocked",
            "check_current_capability",
            "repair_or_introduce_surface_when_authorized",
            "rerun_extraction",
            "classify_value_or_null_limit",
            "audit_upstream_when_authorized",
            "mark_scoped_expected_limit_when_authorized",
            "close_branch_or_stop_at_capability_layer",
        ],
        "surface_state_record_schema_ref": rel(SURFACE_STATE_SCHEMA_PATH),
        "surface_transition_decision_table_ref": rel(TRANSITION_TABLE_PATH),
        "capability_stop_packet_schema_ref": rel(CAPABILITY_STOP_SCHEMA_PATH),
        "authority_guards": {
            "value_invention_authorized": False,
            "taxonomy_label_creation_authorized": False,
            "taxonomy_upgrade_authorized": False,
            "source_mutation_authorized": False,
            "existing_receipt_mutation_authorized": False,
            "next_group_auto_open_authorized": False,
            "hidden_next_command_authorized": False,
        },
        "expected_limit_closure_rule": {
            "allowed": True,
            "scope_required": "explicit_tracked_source_chain_or_other_explicit_audited_scope",
            "must_not_claim_universal_nonexistence": True,
            "must_not_authorize_value_or_taxonomy_repair": True,
            "terminal_stop_code": "STOP_BRANCH_CLOSED_EXPECTED_SOURCE_CONTENT_LIMIT",
        },
        "capability_stop_rule": {
            "required_when": "next lawful move requires a capability not present in current runner",
            "terminal_stop_code": "STOP_CAPABILITY_LAYER_REQUIRED",
            "packet_schema_ref": rel(CAPABILITY_STOP_SCHEMA_PATH),
        },
        "non_goals": [
            "not_global",
            "not_final",
            "not_all_future_surfaces",
            "not_a_taxonomy_upgrade",
            "not_an_r1000_run",
            "not_a_next_group_selector",
        ],
    }

def build_report(protocol: Dict[str, Any], surface_schema: Dict[str, Any], transition_table: Dict[str, Any], capability_schema: Dict[str, Any], gates: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "current_surface_pressure_handling_loop_protocol_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "protocol_id": protocol["protocol_id"],
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_upstream_audit_receipt_id": SOURCE_UPSTREAM_AUDIT_RECEIPT_ID,
        "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "surface_type_count": len(protocol["surface_types"]),
        "transition_count": len(transition_table["transitions"]),
        "missing_object_type_count": len(protocol["missing_object_types"]),
        "capability_stop_defined": True,
        "expected_limit_closure_defined": True,
        "current_surface_scope_only": True,
        "global_or_final_taxonomy_claim_count": 0,
        "r1000_run_executed_count": 0,
        "next_group_auto_opened_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
        "output_artifacts": {
            "current_surface_pressure_loop_protocol": rel(PROTOCOL_PATH),
            "surface_state_record_schema": rel(SURFACE_STATE_SCHEMA_PATH),
            "surface_transition_decision_table": rel(TRANSITION_TABLE_PATH),
            "capability_stop_packet_schema": rel(CAPABILITY_STOP_SCHEMA_PATH),
            "pressure_loop_acceptance_gates": rel(ACCEPTANCE_GATES_PATH),
        },
    }

def validate_outputs(protocol: Dict[str, Any], surface_schema: Dict[str, Any], transition_table: Dict[str, Any], capability_schema: Dict[str, Any], gates: Dict[str, Any], report: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if protocol["scope"] != "current_surface_pressure_loop_only":
        failures.append("protocol_scope_wrong")
    if protocol["surface_types"] != CURRENT_SURFACE_TYPES:
        failures.append("surface_types_wrong")
    if "capability_stop_surface" not in protocol["surface_types"]:
        failures.append("capability_stop_surface_missing")
    if "expected_limit_closure_surface" not in protocol["surface_types"]:
        failures.append("expected_limit_closure_surface_missing")
    if len(transition_table["transitions"]) < 10:
        failures.append("transition_table_too_small")
    if not any(t.get("yes") == "STOP_CAPABILITY_LAYER_REQUIRED" or t.get("no") == "STOP_CAPABILITY_LAYER_REQUIRED" for t in transition_table["transitions"]):
        failures.append("capability_stop_transition_missing")
    if capability_schema["field_constraints"]["terminal.stop_code"] != "STOP_CAPABILITY_LAYER_REQUIRED":
        failures.append("capability_stop_code_wrong")
    if capability_schema["field_constraints"]["terminal.next_command_goal"] is not None:
        failures.append("capability_stop_next_not_null")
    if protocol["expected_limit_closure_rule"]["must_not_claim_universal_nonexistence"] is not True:
        failures.append("expected_limit_universal_overclaim_allowed")
    if protocol["expected_limit_closure_rule"]["must_not_authorize_value_or_taxonomy_repair"] is not True:
        failures.append("expected_limit_value_or_taxonomy_allowed")
    if protocol["authority_guards"]["value_invention_authorized"] is not False:
        failures.append("value_invention_authorized")
    if protocol["authority_guards"]["taxonomy_label_creation_authorized"] is not False:
        failures.append("taxonomy_label_creation_authorized")
    if protocol["authority_guards"]["taxonomy_upgrade_authorized"] is not False:
        failures.append("taxonomy_upgrade_authorized")
    if protocol["authority_guards"]["source_mutation_authorized"] is not False:
        failures.append("source_mutation_authorized")
    if protocol["authority_guards"]["next_group_auto_open_authorized"] is not False:
        failures.append("next_group_auto_open_authorized")
    if protocol["authority_guards"]["hidden_next_command_authorized"] is not False:
        failures.append("hidden_next_command_authorized")
    if surface_schema["scope"] != "current_surfaces_only":
        failures.append("surface_schema_scope_wrong")
    for required in [
        "surface_id",
        "surface_type",
        "source_receipt_id",
        "pressure_group_key",
        "key_visibility",
        "value_state",
        "provenance_state",
        "authority_state",
        "classification",
        "capability_state",
        "terminal",
    ]:
        if required not in surface_schema["required_fields"]:
            failures.append(f"surface_schema_missing_required:{required}")
    for gate in [
        "CURRENT_SURFACE_LOOP_0_SOURCE_BRANCH_CLOSURE_CONSUMED",
        "CURRENT_SURFACE_LOOP_1_CURRENT_SURFACE_TYPES_DEFINED",
        "CURRENT_SURFACE_LOOP_2_SURFACE_STATE_RECORD_SCHEMA_EMITTED",
        "CURRENT_SURFACE_LOOP_3_YES_NO_TRANSITION_TABLE_EMITTED",
        "CURRENT_SURFACE_LOOP_4_CAPABILITY_STOP_PACKET_SCHEMA_EMITTED",
        "CURRENT_SURFACE_LOOP_5_AUTHORITY_GUARDS_DEFINED",
        "CURRENT_SURFACE_LOOP_6_EXPECTED_LIMIT_CLOSURE_PATH_DEFINED",
        "CURRENT_SURFACE_LOOP_7_NO_VALUE_INVENTION_OR_TAXONOMY_ACTION",
        "CURRENT_SURFACE_LOOP_8_NO_GLOBAL_OR_FINAL_TAXONOMY_CLAIM",
        "CURRENT_SURFACE_LOOP_9_NO_R1000_RUN_OR_NEXT_GROUP_AUTO_OPEN",
        "CURRENT_SURFACE_LOOP_10_NO_HIDDEN_NEXT_COMMAND",
    ]:
        if gate not in gates["gates"]:
            failures.append(f"acceptance_gate_missing:{gate}")
    for key in [
        "global_or_final_taxonomy_claim_count",
        "r1000_run_executed_count",
        "next_group_auto_opened_count",
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

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "CURRENT_SURFACE_LOOP_0_SOURCE_BRANCH_CLOSURE_CONSUMED",
        "CURRENT_SURFACE_LOOP_1_CURRENT_SURFACE_TYPES_DEFINED",
        "CURRENT_SURFACE_LOOP_2_SURFACE_STATE_RECORD_SCHEMA_EMITTED",
        "CURRENT_SURFACE_LOOP_3_YES_NO_TRANSITION_TABLE_EMITTED",
        "CURRENT_SURFACE_LOOP_4_CAPABILITY_STOP_PACKET_SCHEMA_EMITTED",
        "CURRENT_SURFACE_LOOP_5_AUTHORITY_GUARDS_DEFINED",
        "CURRENT_SURFACE_LOOP_6_EXPECTED_LIMIT_CLOSURE_PATH_DEFINED",
        "CURRENT_SURFACE_LOOP_7_NO_VALUE_INVENTION_OR_TAXONOMY_ACTION",
        "CURRENT_SURFACE_LOOP_8_NO_GLOBAL_OR_FINAL_TAXONOMY_CLAIM",
        "CURRENT_SURFACE_LOOP_9_NO_R1000_RUN_OR_NEXT_GROUP_AUTO_OPEN",
        "CURRENT_SURFACE_LOOP_10_NO_HIDDEN_NEXT_COMMAND",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    if metrics.get("current_surface_scope_only") is not True:
        failures.append("metric_current_surface_scope_wrong")
    if metrics.get("capability_stop_defined") is not True:
        failures.append("metric_capability_stop_missing")
    if metrics.get("expected_limit_closure_defined") is not True:
        failures.append("metric_expected_limit_closure_missing")
    if metrics.get("surface_type_count") != len(CURRENT_SURFACE_TYPES):
        failures.append("metric_surface_type_count_wrong")
    if metrics.get("transition_count", 0) < 10:
        failures.append("metric_transition_count_too_low")
    for key in [
        "global_or_final_taxonomy_claim_count",
        "r1000_run_executed_count",
        "next_group_auto_opened_count",
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
    if terminal.get("stop_code") != "STOP_PROTOCOL_FROZEN_READY_FOR_R1000_APPLICATION":
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

    surface_schema = build_surface_state_record_schema()
    transition_table = build_transition_table()
    capability_schema = build_capability_stop_packet_schema()
    gates = build_acceptance_gates()
    protocol = build_protocol(surface_schema, transition_table, capability_schema)
    report = build_report(protocol, surface_schema, transition_table, capability_schema, gates)

    write_json(SURFACE_STATE_SCHEMA_PATH, surface_schema)
    write_json(TRANSITION_TABLE_PATH, transition_table)
    write_json(CAPABILITY_STOP_SCHEMA_PATH, capability_schema)
    write_json(ACCEPTANCE_GATES_PATH, gates)
    write_json(PROTOCOL_PATH, protocol)
    write_json(REPORT_PATH, report)

    failures.extend(validate_outputs(protocol, surface_schema, transition_table, capability_schema, gates, report))

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    acceptance_gate_results = {
        "CURRENT_SURFACE_LOOP_0_SOURCE_BRANCH_CLOSURE_CONSUMED": sources["expected_limit_receipt"]["receipt_id"] == SOURCE_EXPECTED_LIMIT_RECEIPT_ID and sources["expected_limit_receipt"]["gate"] == "PASS" and sources["expected_limit_receipt"]["aggregate_metrics"]["branch_closed"] is True,
        "CURRENT_SURFACE_LOOP_1_CURRENT_SURFACE_TYPES_DEFINED": protocol["surface_types"] == CURRENT_SURFACE_TYPES,
        "CURRENT_SURFACE_LOOP_2_SURFACE_STATE_RECORD_SCHEMA_EMITTED": SURFACE_STATE_SCHEMA_PATH.exists() and surface_schema["scope"] == "current_surfaces_only",
        "CURRENT_SURFACE_LOOP_3_YES_NO_TRANSITION_TABLE_EMITTED": TRANSITION_TABLE_PATH.exists() and len(transition_table["transitions"]) >= 10,
        "CURRENT_SURFACE_LOOP_4_CAPABILITY_STOP_PACKET_SCHEMA_EMITTED": CAPABILITY_STOP_SCHEMA_PATH.exists() and capability_schema["field_constraints"]["terminal.stop_code"] == "STOP_CAPABILITY_LAYER_REQUIRED",
        "CURRENT_SURFACE_LOOP_5_AUTHORITY_GUARDS_DEFINED": all(v is False for v in protocol["authority_guards"].values()),
        "CURRENT_SURFACE_LOOP_6_EXPECTED_LIMIT_CLOSURE_PATH_DEFINED": protocol["expected_limit_closure_rule"]["allowed"] is True and protocol["expected_limit_closure_rule"]["must_not_claim_universal_nonexistence"] is True,
        "CURRENT_SURFACE_LOOP_7_NO_VALUE_INVENTION_OR_TAXONOMY_ACTION": report["field_value_invention_count"] == 0 and report["taxonomy_delta_proposal_emitted_count"] == 0 and report["taxonomy_upgrade_authorized_count"] == 0,
        "CURRENT_SURFACE_LOOP_8_NO_GLOBAL_OR_FINAL_TAXONOMY_CLAIM": report["global_or_final_taxonomy_claim_count"] == 0 and protocol["scope"] == "current_surface_pressure_loop_only",
        "CURRENT_SURFACE_LOOP_9_NO_R1000_RUN_OR_NEXT_GROUP_AUTO_OPEN": report["r1000_run_executed_count"] == 0 and report["next_group_auto_opened_count"] == 0,
        "CURRENT_SURFACE_LOOP_10_NO_HIDDEN_NEXT_COMMAND": report["hidden_next_command_count"] == 0,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    terminal = {"type": "STOP", "stop_code": "STOP_PROTOCOL_FROZEN_READY_FOR_R1000_APPLICATION", "next_command_goal": None}
    if source_mutation_detected:
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}
    if any([
        report["field_value_invention_count"],
        report["taxonomy_label_creation_count"],
        report["taxonomy_upgrade_authorized_count"],
        report["taxonomy_delta_proposal_emitted_count"],
        report["source_mutation_count"],
        report["existing_receipt_mutation_count"],
        report["r1000_run_executed_count"],
        report["next_group_auto_opened_count"],
        report["hidden_next_command_count"],
    ]):
        terminal = {"type": "STOP", "stop_code": "STOP_AUTHORITY_VIOLATION", "next_command_goal": None}

    aggregate_metrics = {
        "protocol_id": protocol["protocol_id"],
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_upstream_audit_receipt_id": SOURCE_UPSTREAM_AUDIT_RECEIPT_ID,
        "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "source_pressure_loop_application_receipt_id": SOURCE_PRESSURE_LOOP_APPLICATION_RECEIPT_ID,
        "current_surface_scope_only": True,
        "surface_type_count": len(CURRENT_SURFACE_TYPES),
        "transition_count": len(transition_table["transitions"]),
        "missing_object_type_count": len(MISSING_OBJECT_TYPES),
        "capability_stop_defined": True,
        "expected_limit_closure_defined": True,
        "surface_state_schema_emitted_count": 1,
        "transition_table_emitted_count": 1,
        "capability_stop_schema_emitted_count": 1,
        "acceptance_gates_emitted_count": 1,
        "protocol_emitted_count": 1,
        "global_or_final_taxonomy_claim_count": 0,
        "r1000_run_executed_count": 0,
        "next_group_auto_opened_count": 0,
        "field_value_invention_count": 0,
        "taxonomy_label_creation_count": 0,
        "taxonomy_upgrade_authorized_count": 0,
        "taxonomy_delta_proposal_emitted_count": 0,
        "source_mutation_count": 1 if source_mutation_detected else 0,
        "existing_receipt_mutation_count": 0,
        "hidden_next_command_count": 0,
    }

    guards = {
        "current_surface_scope_only": True,
        "capability_stop_defined": True,
        "expected_limit_closure_defined": True,
        "r1000_run_executed": False,
        "next_group_auto_opened": False,
        "values_invented": False,
        "taxonomy_label_created": False,
        "taxonomy_delta_proposal_emitted": False,
        "taxonomy_upgrade_authorized": False,
        "source_mutated": source_mutation_detected,
        "existing_receipts_mutated": False,
        "hidden_next_command": False,
        "global_or_final_taxonomy_claimed": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "source_expected_limit": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "protocol_id": protocol["protocol_id"],
        "terminal": terminal,
    }
    receipt_id = sha8(receipt_seed)
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    output_artifacts = {
        "current_surface_pressure_loop_protocol": rel(PROTOCOL_PATH),
        "surface_state_record_schema": rel(SURFACE_STATE_SCHEMA_PATH),
        "surface_transition_decision_table": rel(TRANSITION_TABLE_PATH),
        "capability_stop_packet_schema": rel(CAPABILITY_STOP_SCHEMA_PATH),
        "pressure_loop_acceptance_gates": rel(ACCEPTANCE_GATES_PATH),
        "current_surface_pressure_loop_protocol_report": rel(REPORT_PATH),
        "implementation_receipt": rel(receipt_path),
    }

    receipt = {
        "schema_version": "current_surface_pressure_handling_loop_protocol_receipt_v0",
        "receipt_type": "CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_PROTOCOL_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_expected_limit_receipt_id": SOURCE_EXPECTED_LIMIT_RECEIPT_ID,
        "source_upstream_audit_receipt_id": SOURCE_UPSTREAM_AUDIT_RECEIPT_ID,
        "source_null_limit_classification_receipt_id": SOURCE_NULL_LIMIT_CLASSIFICATION_RECEIPT_ID,
        "source_field_introduced_surface_rerun_receipt_id": SOURCE_FIELD_INTRO_RERUN_RECEIPT_ID,
        "source_field_introduction_build_receipt_id": SOURCE_FIELD_INTRO_BUILD_RECEIPT_ID,
        "source_pressure_loop_protocol_receipt_id": SOURCE_PRESSURE_LOOP_PROTOCOL_RECEIPT_ID,
        "source_pressure_loop_application_receipt_id": SOURCE_PRESSURE_LOOP_APPLICATION_RECEIPT_ID,
        "human_decision": HUMAN_DECISION,
        "output_artifacts": output_artifacts,
        "current_surface_pressure_loop_protocol_summary": {
            "protocol_id": protocol["protocol_id"],
            "scope": protocol["scope"],
            "surface_types": protocol["surface_types"],
            "missing_object_types": protocol["missing_object_types"],
            "transition_count": len(transition_table["transitions"]),
            "capability_stop_defined": True,
            "expected_limit_closure_defined": True,
            "recommended_next_handling": "APPLY_CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_TO_R1000_PRESSURE_QUEUE_V0",
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "current_surface_pressure_loop_guards": guards,
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
    print(f"current_surface_pressure_loop_protocol_receipt_id={receipt_id}")
    print(f"current_surface_pressure_loop_protocol_receipt_path=data/current_surface_pressure_handling_loop_protocol_v0_receipts/{receipt_id}.json")
    print(f"current_surface_pressure_loop_protocol_path=data/current_surface_pressure_handling_loop_protocol_v0/current_surface_pressure_loop_protocol.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
