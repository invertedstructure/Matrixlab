#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_C8_TARGET_SHAPE_FROM_PRE_C8_INTERLOCK_PAIR_V0"
TARGET_UNIT_ID = "c8.target_shape.from_pre_c8_interlock_pair.v0"
NEXT_UNIT_ID = "BUILD_OR_FREEZE_C8_TARGET_SHAPE_V0"

LAYER = "RUNTIME / C8 / TARGET_SHAPE"
MODE = "TYPE_ONLY / TARGET_PREP / NO_RUNTIME_ADOPTION"
BUILD_MODE = "C8_TARGET_SHAPE_PREPARATION_ONLY"

SOURCE_POST_DECISION_RECEIPT_ID = "62ddebf9"
SOURCE_SIDECAR_CLOSURE_RECEIPT_ID = "bee348a1"
SOURCE_SCHEMA_VALIDATOR_RECEIPT_ID = "732016f0"

POST_DECISION_RECEIPT_PATH = ROOT / "data/post_runtime_observability_sidecar_reference_decision_v0_receipts/62ddebf9.json"
POST_DECISION_PATH = ROOT / "data/post_runtime_observability_sidecar_reference_decision_v0/post_sidecar_reference_decision_v0.json"
POST_NEXT_UNIT_PATH = ROOT / "data/post_runtime_observability_sidecar_reference_decision_v0/post_sidecar_reference_next_unit_v0.json"
POST_BOUNDARY_PATH = ROOT / "data/post_runtime_observability_sidecar_reference_decision_v0/post_sidecar_reference_decision_boundary_v0.json"

SIDECAR_CLOSURE_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0_receipts/bee348a1.json"
SIDECAR_REVIEWED_REFERENCE_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/runtime_observability_sidecar_reviewed_reference_v0.json"
PRE_C8_INTERLOCK_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/pre_c8_interlock_completion_reference_v0.json"

SCHEMA_VALIDATOR_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0_receipts/732016f0.json"
SCHEMA_VALIDATOR_REFERENCE_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0/runtime_schema_validator_reviewed_reference_v0.json"
SCHEMA_VALIDATOR_HOOK_REFERENCE_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0/runtime_schema_validator_observability_hook_reference_v0.json"

OUT_DIR = ROOT / "data/c8_target_shape_from_pre_c8_interlock_pair_v0"
RECEIPT_DIR = ROOT / "data/c8_target_shape_from_pre_c8_interlock_pair_v0_receipts"

BASIS_PATH = OUT_DIR / "c8_target_shape_basis_v0.json"
TARGET_SHAPE_PATH = OUT_DIR / "c8_target_shape_v0.json"
INTERLOCK_MAP_PATH = OUT_DIR / "c8_target_shape_interlock_map_v0.json"
BOUNDARY_PATH = OUT_DIR / "c8_target_shape_boundary_v0.json"
ACCEPTANCE_GATE_PATH = OUT_DIR / "c8_target_shape_acceptance_gate_v0.json"
NON_AUTHORIZATION_PATH = OUT_DIR / "c8_target_shape_non_authorization_v0.json"
NEXT_SURFACE_PATH = OUT_DIR / "c8_target_shape_next_surface_v0.json"
ROLLUP_PATH = OUT_DIR / "c8_target_shape_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c8_target_shape_profile_v0.json"
TRACE_PATH = OUT_DIR / "c8_target_shape_transition_trace.json"

EXPECTED_POST_STATUS = "TYPED_POST_SIDECAR_REFERENCE_DECISION_READY_C8_TARGET_SHAPE_NEXT"
EXPECTED_SIDECAR_STATUS = "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"

ACCEPTED_SCHEMA_VALIDATOR_REFERENCE_STATUSES = {
    "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_FROZEN",
    "RUNTIME_SCHEMA_VALIDATOR_REVIEWED_REFERENCE_FROZEN",
    "SCHEMA_VALIDATOR_REVIEWED_REFERENCE_FROZEN",
    "REVIEWED_REFERENCE_FROZEN",
}

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

def require_false(summary: Dict[str, Any], key: str, failures: List[str]) -> None:
    if summary.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{summary.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        POST_DECISION_RECEIPT_PATH,
        POST_DECISION_PATH,
        POST_NEXT_UNIT_PATH,
        POST_BOUNDARY_PATH,
        SIDECAR_CLOSURE_RECEIPT_PATH,
        SIDECAR_REVIEWED_REFERENCE_PATH,
        PRE_C8_INTERLOCK_PATH,
        SCHEMA_VALIDATOR_RECEIPT_PATH,
        SCHEMA_VALIDATOR_REFERENCE_PATH,
        SCHEMA_VALIDATOR_HOOK_REFERENCE_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    post_receipt = read_json(POST_DECISION_RECEIPT_PATH)
    post_decision = read_json(POST_DECISION_PATH)
    post_next_unit = read_json(POST_NEXT_UNIT_PATH)
    post_boundary = read_json(POST_BOUNDARY_PATH)

    sidecar_receipt = read_json(SIDECAR_CLOSURE_RECEIPT_PATH)
    sidecar_reference = read_json(SIDECAR_REVIEWED_REFERENCE_PATH)
    pre_c8_interlock = read_json(PRE_C8_INTERLOCK_PATH)

    schema_validator_receipt = read_json(SCHEMA_VALIDATOR_RECEIPT_PATH)
    schema_validator_reference = read_json(SCHEMA_VALIDATOR_REFERENCE_PATH)
    schema_validator_hook_reference = read_json(SCHEMA_VALIDATOR_HOOK_REFERENCE_PATH)

    post_summary = post_receipt.get("machine_readable_post_sidecar_reference_decision_summary", {})
    sidecar_summary = sidecar_receipt.get("machine_readable_runtime_observability_sidecar_reference_closure_summary", {})

    if post_receipt.get("receipt_id") != SOURCE_POST_DECISION_RECEIPT_ID:
        failures.append(f"post_receipt_id_wrong:{post_receipt.get('receipt_id')}")
    if post_receipt.get("gate") != "PASS":
        failures.append(f"post_receipt_gate_wrong:{post_receipt.get('gate')}")
    if post_summary.get("status") != EXPECTED_POST_STATUS:
        failures.append(f"post_status_wrong:{post_summary.get('status')}")
    if post_summary.get("next_unit_id") != UNIT_ID:
        failures.append(f"post_next_unit_wrong:{post_summary.get('next_unit_id')}")
    if post_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("post_receipt_terminal_not_advance")
    if post_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("post_receipt_terminal_next_wrong")

    if post_next_unit.get("next_unit_id") != UNIT_ID:
        failures.append(f"post_next_unit_artifact_wrong:{post_next_unit.get('next_unit_id')}")
    if post_next_unit.get("mode") != MODE:
        failures.append(f"post_next_unit_mode_wrong:{post_next_unit.get('mode')}")
    if "runtime patch" not in post_next_unit.get("forbidden_inputs", []):
        failures.append("post_next_unit_forbidden_runtime_patch_missing")
    if "C8 execution authority" not in post_next_unit.get("forbidden_inputs", []):
        failures.append("post_next_unit_forbidden_c8_execution_missing")

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

    if sidecar_receipt.get("receipt_id") != SOURCE_SIDECAR_CLOSURE_RECEIPT_ID:
        failures.append(f"sidecar_receipt_id_wrong:{sidecar_receipt.get('receipt_id')}")
    if sidecar_receipt.get("gate") != "PASS":
        failures.append(f"sidecar_receipt_gate_wrong:{sidecar_receipt.get('gate')}")
    if sidecar_summary.get("status") != EXPECTED_SIDECAR_STATUS:
        failures.append(f"sidecar_status_wrong:{sidecar_summary.get('status')}")
    if sidecar_summary.get("pre_c8_interlock_pair_complete") is not True:
        failures.append("sidecar_pre_c8_interlock_not_complete")
    if sidecar_summary.get("reviewed_reference_frozen") is not True:
        failures.append("sidecar_reference_not_frozen")
    if sidecar_summary.get("schema_validator_reference_consumed") is not True:
        failures.append("sidecar_schema_validator_reference_not_consumed")
    if sidecar_summary.get("decision_edge_observability_reference_consumed") is not True:
        failures.append("sidecar_decision_edge_observability_reference_not_consumed")

    for key in [
        "c8_authorized",
        "runtime_effect",
        "runtime_patched",
        "live_runtime_hooks_installed",
        "live_runtime_routing_installed",
        "validation_verdict_emitted",
        "admissibility_checked",
        "authorization_verdict_emitted",
        "execution_claimed",
        "execution_command_emitted",
        "control_path_blocked",
        "control_path_advanced",
        "schema_archive_mutated",
        "schema_created",
        "hidden_next_command",
    ]:
        require_false(sidecar_summary, key, failures)

    if sidecar_reference.get("reference_status") != "RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"sidecar_reference_status_wrong:{sidecar_reference.get('reference_status')}")
    if sidecar_reference.get("authority_law") != "The sidecar has eyes, not hands.":
        failures.append("sidecar_authority_law_wrong")
    if sidecar_reference.get("core_compression") != "Control path acts. Sidecar records.":
        failures.append("sidecar_core_compression_wrong")

    if pre_c8_interlock.get("completion_status") != "PRE_C8_INTERLOCK_PAIR_COMPLETE":
        failures.append(f"pre_c8_interlock_status_wrong:{pre_c8_interlock.get('completion_status')}")
    if pre_c8_interlock.get("does_not_authorize_c8_by_itself") is not True:
        failures.append("pre_c8_interlock_c8_non_authorization_missing")

    if schema_validator_receipt.get("receipt_id") != SOURCE_SCHEMA_VALIDATOR_RECEIPT_ID:
        failures.append(f"schema_validator_receipt_id_wrong:{schema_validator_receipt.get('receipt_id')}")
    if schema_validator_receipt.get("gate") != "PASS":
        failures.append(f"schema_validator_gate_wrong:{schema_validator_receipt.get('gate')}")
    if schema_validator_reference.get("reference_status") not in ACCEPTED_SCHEMA_VALIDATOR_REFERENCE_STATUSES:
        failures.append(f"schema_validator_reference_status_unrecognized:{schema_validator_reference.get('reference_status')}")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_TARGET_SHAPE_PREPARED_NO_RUNTIME_ADOPTION" if gate == "PASS" else "TYPED_C8_TARGET_SHAPE_PREPARATION_GATE_FAIL"

    source_hash_manifest = {rel(p): file_sha256(p) for p in required}

    reason_codes = [
        "C8_TARGET_SHAPE_PREPARED_FROM_PRE_C8_INTERLOCK_PAIR",
        "POST_SIDECAR_DECISION_RECEIPT_CONSUMED",
        "SCHEMA_VALIDATOR_REVIEWED_REFERENCE_CONSUMED",
        "RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_REFERENCE_CONSUMED",
        "PRE_C8_INTERLOCK_PAIR_COMPLETE",
        "TYPE_ONLY_TARGET_SHAPE",
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
        "schema_version": "c8_target_shape_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_post_decision_receipt_id": SOURCE_POST_DECISION_RECEIPT_ID,
        "source_sidecar_closure_receipt_id": SOURCE_SIDECAR_CLOSURE_RECEIPT_ID,
        "source_schema_validator_receipt_id": SOURCE_SCHEMA_VALIDATOR_RECEIPT_ID,
        "source_files": source_hash_manifest,
        "basis_claim": "The pre-C8 interlock pair is complete: Schema Validator reviewed reference plus Runtime Observability Sidecar reviewed reference.",
        "basis_does_not_authorize": [
            "C8 runtime adoption",
            "C8 execution",
            "runtime patching",
            "live hook installation",
            "validation authority",
            "admissibility authority",
            "authorization authority",
            "schema archive mutation",
            "control path authority",
        ],
    }

    target_shape = {
        "schema_version": "c8_target_shape_v0",
        "target_shape_status": status,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "shape_name": "C8 target shape from pre-C8 interlock pair",
        "shape_kind": "TYPE_ONLY_REFERENCE_TARGET",
        "shape_role": "Define the smallest C8 target surface made visible by the completed pre-C8 interlock pair.",
        "core_compression": "Validator checks admissibility shape; sidecar records load-bearing observation; control path remains separate.",
        "components": [
            {
                "component_id": "schema_validator_cell_reference",
                "source_receipt_id": SOURCE_SCHEMA_VALIDATOR_RECEIPT_ID,
                "source_path": rel(SCHEMA_VALIDATOR_REFERENCE_PATH),
                "role_in_shape": "hold predetermined schema/admissibility reference surface",
                "authority_in_this_unit": "REFERENCE_ONLY",
                "may_validate_live_runtime": False,
                "may_authorize": False,
                "may_execute": False,
                "may_mutate_schema_archive": False,
            },
            {
                "component_id": "runtime_observability_sidecar_reference",
                "source_receipt_id": SOURCE_SIDECAR_CLOSURE_RECEIPT_ID,
                "source_path": rel(SIDECAR_REVIEWED_REFERENCE_PATH),
                "role_in_shape": "record load-bearing decision-edge and runtime-observation fields",
                "authority_in_this_unit": "REFERENCE_ONLY",
                "may_install_live_hooks": False,
                "may_patch_runtime": False,
                "may_route_runtime": False,
                "may_block_control_path": False,
                "may_advance_control_path": False,
            },
            {
                "component_id": "control_path_placeholder",
                "source_path": None,
                "role_in_shape": "reserved boundary: any future control-path action must be separately authorized",
                "authority_in_this_unit": "NOT_GRANTED",
                "may_execute": False,
                "may_authorize_runtime_adoption": False,
            },
        ],
        "minimum_c8_shape_fields": [
            "proposal_or_active_object_ref",
            "schema_reference_ref",
            "validator_boundary_result",
            "sidecar_observation_ref",
            "load_bearing_decision_edge_fields",
            "control_path_boundary",
            "terminal_result",
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
            "C8 runtime",
            "C8 execution engine",
            "live validation layer",
            "authorization verdict",
            "admissibility authority",
            "runtime adoption",
            "schema archive mutation",
            "control path authority",
        ],
    }

    interlock_map = {
        "schema_version": "c8_target_shape_interlock_map_v0",
        "interlock_status": "MAPPED" if gate == "PASS" else "NOT_MAPPED",
        "pre_c8_interlock_pair_complete": gate == "PASS",
        "left_reference": {
            "name": "Runtime Schema Validator Cell",
            "receipt_id": SOURCE_SCHEMA_VALIDATOR_RECEIPT_ID,
            "reference_status": schema_validator_reference.get("reference_status"),
            "role": "well-formed / typed / schema-match reference surface",
        },
        "right_reference": {
            "name": "Runtime Observability Sidecar",
            "receipt_id": SOURCE_SIDECAR_CLOSURE_RECEIPT_ID,
            "reference_status": sidecar_reference.get("reference_status"),
            "role": "append-only load-bearing observation reference surface",
        },
        "joint_shape": {
            "validator_side": "may classify target-shape admissibility only when separately built/authorized later",
            "sidecar_side": "may record only when separately adopted later",
            "control_side": "no control action is granted here",
        },
    }

    boundary = {
        "schema_version": "c8_target_shape_boundary_v0",
        "boundary_status": "BOUNDARY_HELD" if gate == "PASS" else "BOUNDARY_FAIL",
        "allowed_in_this_unit": [
            "consume post-sidecar decision receipt",
            "consume Schema Validator reviewed reference",
            "consume Runtime Observability Sidecar reviewed reference",
            "consume pre-C8 interlock completion marker",
            "type C8 target shape",
            "emit target-shape receipt",
            "name next build-or-freeze surface",
        ],
        "forbidden_in_this_unit": [
            "install live runtime hooks",
            "patch runtime",
            "route runtime traffic",
            "execute C8",
            "authorize runtime adoption",
            "emit validation verdict",
            "emit admissibility verdict",
            "emit authorization verdict",
            "mutate schema archive",
            "mutate references",
            "block control path",
            "advance control path",
            "repair proposals",
            "create schemas",
            "emit hidden next command",
        ],
    }

    acceptance_gate = {
        "schema_version": "c8_target_shape_acceptance_gate_v0",
        "gate_status": "PASS" if gate == "PASS" else "FAIL",
        "checks": {
            "post_decision_receipt_consumed": gate == "PASS",
            "schema_validator_reference_consumed": gate == "PASS",
            "sidecar_reference_consumed": gate == "PASS",
            "pre_c8_interlock_pair_complete": gate == "PASS",
            "target_shape_names_role": gate == "PASS",
            "target_shape_names_boundary": gate == "PASS",
            "target_shape_names_inputs": gate == "PASS",
            "target_shape_names_forbidden_claims": gate == "PASS",
            "target_shape_names_stop_advance_surface": gate == "PASS",
            "no_runtime_adoption": gate == "PASS",
            "no_runtime_patch": gate == "PASS",
            "no_live_hooks": gate == "PASS",
            "no_schema_mutation": gate == "PASS",
            "no_control_path_authority": gate == "PASS",
        },
    }

    non_authorization = {
        "schema_version": "c8_target_shape_non_authorization_v0",
        "c8_target_shape_prepared": gate == "PASS",
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

    next_surface = {
        "schema_version": "c8_target_shape_next_surface_v0",
        "current_unit_id": UNIT_ID,
        "terminal_on_pass": {
            "type": "ADVANCE",
            "next_unit_id": NEXT_UNIT_ID,
        },
        "next_unit_id": NEXT_UNIT_ID,
        "next_unit_scope": "decide whether to freeze this target shape as reference or build the smallest executable/reference artifact from it",
        "next_unit_must_not_impersonate": [
            "runtime adoption",
            "C8 execution",
            "schema mutation",
            "control path authority",
        ],
    }

    rollup = {
        "schema_version": "c8_target_shape_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "source_post_decision_receipt_id": SOURCE_POST_DECISION_RECEIPT_ID,
        "source_sidecar_closure_receipt_id": SOURCE_SIDECAR_CLOSURE_RECEIPT_ID,
        "source_schema_validator_receipt_id": SOURCE_SCHEMA_VALIDATOR_RECEIPT_ID,
        "pre_c8_interlock_pair_complete": gate == "PASS",
        "c8_target_shape_prepared": gate == "PASS",
        "component_count": 3 if gate == "PASS" else 0,
        "minimum_shape_field_count": len(target_shape["minimum_c8_shape_fields"]) if gate == "PASS" else 0,
        "load_bearing_edge_field_count": len(target_shape["required_load_bearing_decision_edge_fields"]) if gate == "PASS" else 0,
        "c8_runtime_authorized": False,
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "control_path_authority_granted": False,
        "hidden_next_command": False,
    }

    profile = {
        "schema_version": "c8_target_shape_profile_v0",
        "profile_status": status,
        "profile": "PRE_C8_INTERLOCK_PAIR_TO_C8_TARGET_SHAPE",
        "what_changed": "A typed C8 target shape was prepared from the frozen Schema Validator and Runtime Observability Sidecar references.",
        "what_did_not_change": [
            "C8 is not runtime-authorized",
            "C8 is not executed",
            "runtime is not patched",
            "live hooks are not installed",
            "schema archive is not mutated",
            "control path authority is not granted",
        ],
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_C8_TARGET_SHAPE_PREPARATION_V0",
        "next_command_goal": None,
    }

    trace = {
        "schema_version": "c8_target_shape_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "POST_SIDECAR_REFERENCE_DECISION_READY",
                "edge": "consume ADVANCE next unit",
                "to": "C8_TARGET_SHAPE_BASIS_ACCEPTED" if gate == "PASS" else "C8_TARGET_SHAPE_BASIS_FAIL",
            },
            {
                "from": "C8_TARGET_SHAPE_BASIS_ACCEPTED" if gate == "PASS" else "C8_TARGET_SHAPE_BASIS_FAIL",
                "edge": "type target shape without runtime adoption",
                "to": "C8_TARGET_SHAPE_PREPARED_NO_RUNTIME_ADOPTION" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C8_TARGET_SHAPE_PREPARATION_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (TARGET_SHAPE_PATH, target_shape),
        (INTERLOCK_MAP_PATH, interlock_map),
        (BOUNDARY_PATH, boundary),
        (ACCEPTANCE_GATE_PATH, acceptance_gate),
        (NON_AUTHORIZATION_PATH, non_authorization),
        (NEXT_SURFACE_PATH, next_surface),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_PATH, trace),
    ]:
        write_json(path, obj)

    receipt_body = {
        "schema_version": "c8_target_shape_from_pre_c8_interlock_pair_receipt_v0",
        "receipt_type": "TYPED_C8_TARGET_SHAPE_FROM_PRE_C8_INTERLOCK_PAIR_RECEIPT",
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
        "source_post_decision_receipt_id": SOURCE_POST_DECISION_RECEIPT_ID,
        "source_sidecar_closure_receipt_id": SOURCE_SIDECAR_CLOSURE_RECEIPT_ID,
        "source_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_RECEIPT_ID,
        "acceptance_gate_results": acceptance_gate["checks"],
        "machine_readable_c8_target_shape_summary": {
            "status": status,
            "c8_target_shape_prepared": gate == "PASS",
            "source_post_decision_receipt_consumed": gate == "PASS",
            "schema_validator_reference_consumed": gate == "PASS",
            "runtime_observability_sidecar_reference_consumed": gate == "PASS",
            "pre_c8_interlock_pair_complete": gate == "PASS",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
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
            "component_count": rollup["component_count"],
            "minimum_shape_field_count": rollup["minimum_shape_field_count"],
            "load_bearing_edge_field_count": rollup["load_bearing_edge_field_count"],
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "target_shape": rel(TARGET_SHAPE_PATH),
            "interlock_map": rel(INTERLOCK_MAP_PATH),
            "boundary": rel(BOUNDARY_PATH),
            "acceptance_gate": rel(ACCEPTANCE_GATE_PATH),
            "non_authorization": rel(NON_AUTHORIZATION_PATH),
            "next_surface": rel(NEXT_SURFACE_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C8_TARGET_SHAPE_PREPARATION_GATE_FAIL",
        },
    }

    receipt_id = sig8(receipt_body)
    receipt_body["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_body["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_body)

    print(json.dumps(receipt_body, indent=2, sort_keys=True))
    print(f"c8_target_shape_receipt_id={receipt_id}")
    print(f"c8_target_shape_receipt_path={rel(receipt_path)}")
    print(f"c8_target_shape_path={rel(TARGET_SHAPE_PATH)}")
    print(f"c8_target_shape_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
