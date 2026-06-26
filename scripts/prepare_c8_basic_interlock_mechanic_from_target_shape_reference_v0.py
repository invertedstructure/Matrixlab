#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_C8_BASIC_INTERLOCK_MECHANIC_FROM_TARGET_SHAPE_REFERENCE_V0"
TARGET_UNIT_ID = "c8.basic_interlock_mechanic.from_target_shape_reference.v0"
NEXT_UNIT_ID = "BUILD_OR_FREEZE_C8_BASIC_INTERLOCK_MECHANIC_V0"

LAYER = "RUNTIME / C8 / BASIC_INTERLOCK_MECHANIC"
MODE = "TYPE_ONLY / MECHANIC_PREP / NO_RUNTIME_ADOPTION"
BUILD_MODE = "C8_BASIC_INTERLOCK_MECHANIC_PREPARATION_ONLY"

SOURCE_POST_C8_DECISION_RECEIPT_ID = "04f99452"
SOURCE_C8_REFERENCE_RECEIPT_ID = "ea23fd9b"

POST_C8_DECISION_RECEIPT_PATH = ROOT / "data/post_c8_target_shape_reference_decision_v0_receipts/04f99452.json"
POST_C8_DECISION_PATH = ROOT / "data/post_c8_target_shape_reference_decision_v0/post_c8_target_shape_reference_decision_v0.json"
POST_C8_NEXT_UNIT_PATH = ROOT / "data/post_c8_target_shape_reference_decision_v0/post_c8_target_shape_reference_next_unit_v0.json"
POST_C8_BOUNDARY_PATH = ROOT / "data/post_c8_target_shape_reference_decision_v0/post_c8_target_shape_reference_decision_boundary_v0.json"

C8_REFERENCE_RECEIPT_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0_receipts/ea23fd9b.json"
C8_REVIEWED_REFERENCE_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0/c8_target_shape_reviewed_reference_v0.json"
C8_REFERENCE_NON_AUTHORIZATION_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0/c8_target_shape_reference_non_authorization_v0.json"
C8_REFERENCE_ROLLUP_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0/c8_target_shape_reference_rollup_v0.json"
C8_REFERENCE_PROFILE_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0/c8_target_shape_reference_profile_v0.json"

SCHEMA_VALIDATOR_REFERENCE_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0/runtime_schema_validator_reviewed_reference_v0.json"
SIDECAR_REVIEWED_REFERENCE_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/runtime_observability_sidecar_reviewed_reference_v0.json"

OUT_DIR = ROOT / "data/c8_basic_interlock_mechanic_from_target_shape_reference_v0"
RECEIPT_DIR = ROOT / "data/c8_basic_interlock_mechanic_from_target_shape_reference_v0_receipts"

BASIS_PATH = OUT_DIR / "c8_basic_interlock_mechanic_basis_v0.json"
MECHANIC_PATH = OUT_DIR / "c8_basic_interlock_mechanic_v0.json"
FLOW_PATH = OUT_DIR / "c8_basic_interlock_mechanic_flow_v0.json"
COMPONENT_MAP_PATH = OUT_DIR / "c8_basic_interlock_component_map_v0.json"
BOUNDARY_PATH = OUT_DIR / "c8_basic_interlock_mechanic_boundary_v0.json"
NON_AUTHORIZATION_PATH = OUT_DIR / "c8_basic_interlock_mechanic_non_authorization_v0.json"
ACCEPTANCE_GATE_PATH = OUT_DIR / "c8_basic_interlock_mechanic_acceptance_gate_v0.json"
NEXT_SURFACE_PATH = OUT_DIR / "c8_basic_interlock_mechanic_next_surface_v0.json"
ROLLUP_PATH = OUT_DIR / "c8_basic_interlock_mechanic_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c8_basic_interlock_mechanic_profile_v0.json"
TRACE_PATH = OUT_DIR / "c8_basic_interlock_mechanic_transition_trace.json"

EXPECTED_POST_STATUS = "TYPED_POST_C8_TARGET_SHAPE_REFERENCE_DECISION_READY_BASIC_INTERLOCK_NEXT"
EXPECTED_C8_REFERENCE_STATUS = "TYPED_C8_TARGET_SHAPE_FROZEN_AS_REVIEWED_REFERENCE_DECISION_READY"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def require_false(obj: Dict[str, Any], key: str, failures: List[str]) -> None:
    if obj.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{obj.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        POST_C8_DECISION_RECEIPT_PATH,
        POST_C8_DECISION_PATH,
        POST_C8_NEXT_UNIT_PATH,
        POST_C8_BOUNDARY_PATH,
        C8_REFERENCE_RECEIPT_PATH,
        C8_REVIEWED_REFERENCE_PATH,
        C8_REFERENCE_NON_AUTHORIZATION_PATH,
        C8_REFERENCE_ROLLUP_PATH,
        C8_REFERENCE_PROFILE_PATH,
        SCHEMA_VALIDATOR_REFERENCE_PATH,
        SIDECAR_REVIEWED_REFERENCE_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    post_receipt = read_json(POST_C8_DECISION_RECEIPT_PATH)
    post_decision = read_json(POST_C8_DECISION_PATH)
    post_next_unit = read_json(POST_C8_NEXT_UNIT_PATH)
    post_boundary = read_json(POST_C8_BOUNDARY_PATH)

    c8_receipt = read_json(C8_REFERENCE_RECEIPT_PATH)
    c8_reference = read_json(C8_REVIEWED_REFERENCE_PATH)
    c8_non_authorization = read_json(C8_REFERENCE_NON_AUTHORIZATION_PATH)
    c8_rollup = read_json(C8_REFERENCE_ROLLUP_PATH)
    c8_profile = read_json(C8_REFERENCE_PROFILE_PATH)

    schema_validator_reference = read_json(SCHEMA_VALIDATOR_REFERENCE_PATH)
    sidecar_reference = read_json(SIDECAR_REVIEWED_REFERENCE_PATH)

    post_summary = post_receipt.get("machine_readable_post_c8_target_shape_reference_decision_summary", {})
    c8_summary = c8_receipt.get("machine_readable_c8_target_shape_reference_summary", {})

    if post_receipt.get("receipt_id") != SOURCE_POST_C8_DECISION_RECEIPT_ID:
        failures.append(f"post_decision_receipt_id_wrong:{post_receipt.get('receipt_id')}")
    if post_receipt.get("gate") != "PASS":
        failures.append(f"post_decision_gate_wrong:{post_receipt.get('gate')}")
    if post_summary.get("status") != EXPECTED_POST_STATUS:
        failures.append(f"post_decision_status_wrong:{post_summary.get('status')}")
    if post_summary.get("next_unit_id") != UNIT_ID:
        failures.append(f"post_decision_next_unit_wrong:{post_summary.get('next_unit_id')}")
    if post_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("post_decision_terminal_not_advance")
    if post_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("post_decision_terminal_next_wrong")

    if post_next_unit.get("next_unit_id") != UNIT_ID:
        failures.append(f"next_unit_artifact_wrong:{post_next_unit.get('next_unit_id')}")
    if post_next_unit.get("mode") != MODE:
        failures.append(f"next_unit_mode_wrong:{post_next_unit.get('mode')}")
    if post_next_unit.get("artifact_target") != TARGET_UNIT_ID:
        failures.append(f"next_unit_artifact_target_wrong:{post_next_unit.get('artifact_target')}")

    if c8_receipt.get("receipt_id") != SOURCE_C8_REFERENCE_RECEIPT_ID:
        failures.append(f"c8_reference_receipt_id_wrong:{c8_receipt.get('receipt_id')}")
    if c8_receipt.get("gate") != "PASS":
        failures.append(f"c8_reference_gate_wrong:{c8_receipt.get('gate')}")
    if c8_summary.get("status") != EXPECTED_C8_REFERENCE_STATUS:
        failures.append(f"c8_reference_status_wrong:{c8_summary.get('status')}")
    if c8_summary.get("c8_target_shape_reference_frozen") is not True:
        failures.append("c8_target_shape_reference_not_frozen")
    if c8_reference.get("reference_status") != "C8_TARGET_SHAPE_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"c8_reviewed_reference_status_wrong:{c8_reference.get('reference_status')}")
    if c8_reference.get("reference_only") is not True:
        failures.append("c8_reference_not_reference_only")

    if c8_rollup.get("component_count") != 3:
        failures.append(f"component_count_wrong:{c8_rollup.get('component_count')}")
    if c8_rollup.get("minimum_shape_field_count") != 7:
        failures.append(f"minimum_shape_field_count_wrong:{c8_rollup.get('minimum_shape_field_count')}")
    if c8_rollup.get("load_bearing_edge_field_count") != 7:
        failures.append(f"load_bearing_edge_field_count_wrong:{c8_rollup.get('load_bearing_edge_field_count')}")
    if c8_profile.get("next_command_goal") is not None:
        failures.append("c8_profile_hidden_next")

    if schema_validator_reference.get("reference_status") != "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"schema_validator_reference_status_wrong:{schema_validator_reference.get('reference_status')}")
    if sidecar_reference.get("reference_status") != "RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"sidecar_reference_status_wrong:{sidecar_reference.get('reference_status')}")

    for key in [
        "c8_runtime_authorized",
        "c8_execution_authorized",
        "runtime_adoption_authorized",
        "live_runtime_hooks_installed",
        "runtime_patched",
        "runtime_routing_installed",
        "validation_verdict_emitted",
        "admissibility_checked",
        "authorization_verdict_emitted",
        "execution_claimed",
        "schema_archive_mutated",
        "schema_created",
        "control_path_blocked",
        "control_path_advanced",
        "hidden_next_command",
    ]:
        require_false(post_summary, key, failures)
        require_false(c8_summary, key, failures)
        require_false(c8_non_authorization, key, failures)
        if key in c8_reference:
            require_false(c8_reference, key, failures)

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_BASIC_INTERLOCK_MECHANIC_PREPARED_NO_RUNTIME_ADOPTION" if gate == "PASS" else "TYPED_C8_BASIC_INTERLOCK_MECHANIC_PREPARATION_GATE_FAIL"

    source_hash_manifest = {rel(p): file_sha256(p) for p in required}

    reason_codes = [
        "C8_BASIC_INTERLOCK_MECHANIC_PREPARED_FROM_TARGET_SHAPE_REFERENCE",
        "POST_C8_TARGET_SHAPE_REFERENCE_DECISION_CONSUMED",
        "C8_TARGET_SHAPE_REVIEWED_REFERENCE_CONSUMED",
        "SCHEMA_VALIDATOR_REFERENCE_CONSUMED",
        "RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CONSUMED",
        "TYPE_ONLY_MECHANIC_PREP",
        "NO_C8_RUNTIME_AUTHORIZATION",
        "NO_C8_EXECUTION_AUTHORIZATION",
        "NO_RUNTIME_ADOPTION",
        "NO_LIVE_HOOK_INSTALL",
        "NO_RUNTIME_PATCH",
        "NO_RUNTIME_ROUTING",
        "NO_VALIDATION_AUTHORITY",
        "NO_ADMISSIBILITY_AUTHORITY",
        "NO_AUTHORIZATION_VERDICT",
        "NO_EXECUTION_CLAIM",
        "NO_CONTROL_PATH_BLOCK_OR_ADVANCE",
        "NO_SCHEMA_MUTATION",
        "NO_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    basis = {
        "schema_version": "c8_basic_interlock_mechanic_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_post_c8_decision_receipt_id": SOURCE_POST_C8_DECISION_RECEIPT_ID,
        "source_c8_target_shape_reference_receipt_id": SOURCE_C8_REFERENCE_RECEIPT_ID,
        "source_files": source_hash_manifest,
        "basis_claim": "A frozen C8 target-shape reviewed reference exists and named this basic interlock mechanic as the next typed unit.",
        "basis_does_not_authorize": [
            "C8 runtime adoption",
            "C8 execution",
            "runtime patching",
            "live hook installation",
            "validation authority",
            "admissibility authority",
            "authorization verdict",
            "schema archive mutation",
            "control path authority",
        ],
    }

    component_map = {
        "schema_version": "c8_basic_interlock_component_map_v0",
        "map_status": "MAPPED" if gate == "PASS" else "NOT_MAPPED",
        "components": [
            {
                "component_id": "proposal_or_active_object_ref",
                "role": "input reference being tested by the mechanic",
                "authority": "INPUT_ONLY",
                "may_execute": False,
            },
            {
                "component_id": "schema_validator_reference",
                "role": "checks whether the proposal/active object matches a predetermined schema surface",
                "source_path": rel(SCHEMA_VALIDATOR_REFERENCE_PATH),
                "authority": "REFERENCE_ONLY",
                "may_validate_live_runtime": False,
                "may_authorize": False,
                "may_execute": False,
                "may_mutate_schema_archive": False,
            },
            {
                "component_id": "sidecar_observation_reference",
                "role": "records load-bearing observation fields if later separately adopted",
                "source_path": rel(SIDECAR_REVIEWED_REFERENCE_PATH),
                "authority": "REFERENCE_ONLY",
                "may_install_live_hooks": False,
                "may_patch_runtime": False,
                "may_route_runtime": False,
                "may_block_control_path": False,
                "may_advance_control_path": False,
            },
            {
                "component_id": "control_path_boundary",
                "role": "separates reference/observation/admissibility typing from any future action",
                "authority": "NOT_GRANTED",
                "may_authorize_runtime_adoption": False,
                "may_execute": False,
                "may_block_control_path": False,
                "may_advance_control_path": False,
            },
        ],
    }

    mechanic = {
        "schema_version": "c8_basic_interlock_mechanic_v0",
        "mechanic_status": status,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "mechanic_name": "C8 basic interlock mechanic from target-shape reference",
        "mechanic_kind": "TYPE_ONLY_REFERENCE_MECHANIC",
        "mechanic_role": "Type the smallest interlock between a proposal/reference, schema-validator boundary, sidecar observation surface, and control-path boundary.",
        "core_compression": "Proposal enters; validator boundary classifies shape; sidecar surface records load-bearing fields; control path remains separate.",
        "one_step_flow": [
            "LOAD proposal_or_active_object_ref",
            "CHECK schema_reference_ref against predetermined schema surface",
            "CLASSIFY validator_boundary_result as PASS / FAIL / UNPOSED / NEEDS_HUMAN_REVIEW",
            "RECORD sidecar_observation_ref with load-bearing decision-edge fields",
            "EMIT terminal_result without executing or authorizing runtime adoption",
        ],
        "minimum_mechanic_fields": [
            "proposal_or_active_object_ref",
            "schema_reference_ref",
            "validator_boundary_result",
            "sidecar_observation_ref",
            "load_bearing_decision_edge_fields",
            "control_path_boundary",
            "terminal_result",
        ],
        "allowed_terminal_results": [
            "PASS_SHAPE_ONLY",
            "FAIL_SHAPE_ONLY",
            "UNPOSED_SHAPE",
            "NEEDS_HUMAN_REVIEW",
            "STOP_BOUNDARY_HELD",
        ],
        "required_load_bearing_decision_edge_fields": [
            "active_object",
            "attempted_move",
            "boundary_checked",
            "boundary_result",
            "blocked_moves",
            "lawful_next_moves",
            "source_packet_ref",
        ],
        "must_not_impersonate": [
            "C8 runtime adoption",
            "C8 execution",
            "live admissibility service",
            "authorization verdict",
            "schema archive mutation",
            "control path authority",
        ],
        "reference_only": True,
    }

    flow = {
        "schema_version": "c8_basic_interlock_mechanic_flow_v0",
        "flow_status": "TYPED" if gate == "PASS" else "NOT_TYPED",
        "flow_kind": "ONE_STEP_INTERLOCK",
        "flow_edges": [
            {
                "edge_id": "edge_0_load",
                "from": "input_surface",
                "to": "proposal_or_active_object_ref",
                "allowed_effect": "read reference only",
            },
            {
                "edge_id": "edge_1_validator_boundary",
                "from": "proposal_or_active_object_ref",
                "to": "validator_boundary_result",
                "allowed_effect": "shape classification only",
            },
            {
                "edge_id": "edge_2_sidecar_record",
                "from": "validator_boundary_result",
                "to": "sidecar_observation_ref",
                "allowed_effect": "record load-bearing fields only",
            },
            {
                "edge_id": "edge_3_control_boundary",
                "from": "sidecar_observation_ref",
                "to": "terminal_result",
                "allowed_effect": "emit terminal result without execution",
            },
        ],
    }

    boundary = {
        "schema_version": "c8_basic_interlock_mechanic_boundary_v0",
        "boundary_status": "BOUNDARY_HELD" if gate == "PASS" else "BOUNDARY_FAIL",
        "allowed_in_this_unit": [
            "consume post-C8 target-shape decision receipt",
            "consume frozen C8 target-shape reviewed reference",
            "consume Schema Validator reviewed reference",
            "consume Runtime Observability Sidecar reviewed reference",
            "type the basic interlock mechanic",
            "emit mechanic receipt",
            "name next build-or-freeze surface",
        ],
        "forbidden_in_this_unit": [
            "install live runtime hooks",
            "patch runtime",
            "route runtime traffic",
            "execute C8",
            "authorize runtime adoption",
            "emit live validation verdict",
            "emit live admissibility verdict",
            "emit authorization verdict",
            "mutate schema archive",
            "mutate source references",
            "block control path",
            "advance control path",
            "repair proposals",
            "create schemas",
            "emit hidden next command",
        ],
    }

    non_authorization = {
        "schema_version": "c8_basic_interlock_mechanic_non_authorization_v0",
        "c8_basic_interlock_mechanic_prepared": gate == "PASS",
        "c8_runtime_authorized": False,
        "c8_execution_authorized": False,
        "runtime_adoption_authorized": False,
        "live_runtime_hooks_installed": False,
        "runtime_patched": False,
        "runtime_routing_installed": False,
        "validation_verdict_emitted": False,
        "admissibility_checked": False,
        "authorization_verdict_emitted": False,
        "execution_claimed": False,
        "schema_archive_mutated": False,
        "schema_created": False,
        "control_path_blocked": False,
        "control_path_advanced": False,
        "hidden_next_command": False,
    }

    acceptance_gate = {
        "schema_version": "c8_basic_interlock_mechanic_acceptance_gate_v0",
        "gate_status": "PASS" if gate == "PASS" else "FAIL",
        "checks": {
            "post_c8_decision_receipt_consumed": gate == "PASS",
            "c8_target_shape_reference_consumed": gate == "PASS",
            "schema_validator_reference_consumed": gate == "PASS",
            "sidecar_reference_consumed": gate == "PASS",
            "mechanic_names_components": gate == "PASS",
            "mechanic_names_one_step_flow": gate == "PASS",
            "mechanic_names_stop_advance_surface": gate == "PASS",
            "mechanic_names_blocked_claims": gate == "PASS",
            "mechanic_names_non_authorization_boundary": gate == "PASS",
            "no_runtime_adoption": gate == "PASS",
            "no_runtime_patch": gate == "PASS",
            "no_live_hooks": gate == "PASS",
            "no_schema_mutation": gate == "PASS",
            "no_control_path_authority": gate == "PASS",
        },
    }

    next_surface = {
        "schema_version": "c8_basic_interlock_mechanic_next_surface_v0",
        "current_unit_id": UNIT_ID,
        "terminal_on_pass": {
            "type": "ADVANCE",
            "next_unit_id": NEXT_UNIT_ID,
        },
        "next_unit_id": NEXT_UNIT_ID,
        "next_unit_scope": "freeze/build the typed basic interlock mechanic as reviewed reference only",
        "next_unit_must_not_impersonate": [
            "runtime adoption",
            "C8 execution",
            "schema mutation",
            "control path authority",
        ],
    }

    rollup = {
        "schema_version": "c8_basic_interlock_mechanic_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "source_post_c8_decision_receipt_id": SOURCE_POST_C8_DECISION_RECEIPT_ID,
        "source_c8_target_shape_reference_receipt_id": SOURCE_C8_REFERENCE_RECEIPT_ID,
        "c8_basic_interlock_mechanic_prepared": gate == "PASS",
        "component_count": len(component_map["components"]) if gate == "PASS" else 0,
        "flow_edge_count": len(flow["flow_edges"]) if gate == "PASS" else 0,
        "minimum_mechanic_field_count": len(mechanic["minimum_mechanic_fields"]) if gate == "PASS" else 0,
        "load_bearing_edge_field_count": len(mechanic["required_load_bearing_decision_edge_fields"]) if gate == "PASS" else 0,
        "terminal_result_count": len(mechanic["allowed_terminal_results"]) if gate == "PASS" else 0,
        "c8_runtime_authorized": False,
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "control_path_authority_granted": False,
        "hidden_next_command": False,
    }

    profile = {
        "schema_version": "c8_basic_interlock_mechanic_profile_v0",
        "profile_status": status,
        "profile": "C8_TARGET_SHAPE_REFERENCE_TO_BASIC_INTERLOCK_MECHANIC",
        "what_changed": "A type-only C8 basic interlock mechanic was prepared from the frozen target-shape reference.",
        "what_did_not_change": [
            "C8 is not runtime-authorized",
            "C8 is not executed",
            "runtime is not patched",
            "live hooks are not installed",
            "schema archive is not mutated",
            "control path authority is not granted",
            "live admissibility/authorization verdicts are not emitted",
        ],
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_C8_BASIC_INTERLOCK_MECHANIC_PREPARATION_V0",
        "next_command_goal": None,
    }

    trace = {
        "schema_version": "c8_basic_interlock_mechanic_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "POST_C8_TARGET_SHAPE_REFERENCE_DECISION_READY_BASIC_INTERLOCK_NEXT",
                "edge": "consume ADVANCE next unit",
                "to": "C8_BASIC_INTERLOCK_MECHANIC_BASIS_ACCEPTED" if gate == "PASS" else "C8_BASIC_INTERLOCK_MECHANIC_BASIS_FAIL",
            },
            {
                "from": "C8_BASIC_INTERLOCK_MECHANIC_BASIS_ACCEPTED" if gate == "PASS" else "C8_BASIC_INTERLOCK_MECHANIC_BASIS_FAIL",
                "edge": "type mechanic without runtime adoption",
                "to": "C8_BASIC_INTERLOCK_MECHANIC_PREPARED_NO_RUNTIME_ADOPTION" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C8_BASIC_INTERLOCK_MECHANIC_PREPARATION_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (MECHANIC_PATH, mechanic),
        (FLOW_PATH, flow),
        (COMPONENT_MAP_PATH, component_map),
        (BOUNDARY_PATH, boundary),
        (NON_AUTHORIZATION_PATH, non_authorization),
        (ACCEPTANCE_GATE_PATH, acceptance_gate),
        (NEXT_SURFACE_PATH, next_surface),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_PATH, trace),
    ]:
        write_json(path, obj)

    receipt_body = {
        "schema_version": "c8_basic_interlock_mechanic_from_target_shape_reference_receipt_v0",
        "receipt_type": "TYPED_C8_BASIC_INTERLOCK_MECHANIC_FROM_TARGET_SHAPE_REFERENCE_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "source_post_c8_decision_receipt_id": SOURCE_POST_C8_DECISION_RECEIPT_ID,
        "source_c8_target_shape_reference_receipt_id": SOURCE_C8_REFERENCE_RECEIPT_ID,
        "acceptance_gate_results": acceptance_gate["checks"],
        "machine_readable_c8_basic_interlock_mechanic_summary": {
            "status": status,
            "c8_basic_interlock_mechanic_prepared": gate == "PASS",
            "source_post_c8_decision_receipt_consumed": gate == "PASS",
            "source_c8_target_shape_reference_consumed": gate == "PASS",
            "schema_validator_reference_consumed": gate == "PASS",
            "runtime_observability_sidecar_reference_consumed": gate == "PASS",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "component_count": rollup["component_count"],
            "flow_edge_count": rollup["flow_edge_count"],
            "minimum_mechanic_field_count": rollup["minimum_mechanic_field_count"],
            "load_bearing_edge_field_count": rollup["load_bearing_edge_field_count"],
            "terminal_result_count": rollup["terminal_result_count"],
            "c8_runtime_authorized": False,
            "c8_execution_authorized": False,
            "runtime_adoption_authorized": False,
            "live_runtime_hooks_installed": False,
            "runtime_patched": False,
            "runtime_routing_installed": False,
            "validation_verdict_emitted": False,
            "admissibility_checked": False,
            "authorization_verdict_emitted": False,
            "execution_claimed": False,
            "schema_archive_mutated": False,
            "schema_created": False,
            "control_path_blocked": False,
            "control_path_advanced": False,
            "hidden_next_command": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "mechanic": rel(MECHANIC_PATH),
            "flow": rel(FLOW_PATH),
            "component_map": rel(COMPONENT_MAP_PATH),
            "boundary": rel(BOUNDARY_PATH),
            "non_authorization": rel(NON_AUTHORIZATION_PATH),
            "acceptance_gate": rel(ACCEPTANCE_GATE_PATH),
            "next_surface": rel(NEXT_SURFACE_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C8_BASIC_INTERLOCK_MECHANIC_PREPARATION_GATE_FAIL",
        },
    }

    receipt_id = sig8(receipt_body)
    receipt_body["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_body["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_body)

    print(json.dumps(receipt_body, indent=2, sort_keys=True))
    print(f"c8_basic_interlock_mechanic_receipt_id={receipt_id}")
    print(f"c8_basic_interlock_mechanic_receipt_path={rel(receipt_path)}")
    print(f"c8_basic_interlock_mechanic_path={rel(MECHANIC_PATH)}")
    print(f"c8_basic_interlock_mechanic_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
