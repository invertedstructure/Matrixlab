#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_OR_FREEZE_C8_BASIC_INTERLOCK_MECHANIC_V0"
TARGET_UNIT_ID = "c8.basic_interlock_mechanic.reviewed_reference.v0"
NEXT_UNIT_ID = "DECIDE_NEXT_AFTER_C8_BASIC_INTERLOCK_MECHANIC_REFERENCE_FREEZE_V0"

LAYER = "RUNTIME / C8 / BASIC_INTERLOCK_MECHANIC_REFERENCE"
MODE = "FREEZE_REFERENCE_ONLY / NO_RUNTIME_ADOPTION / NO_EXECUTION"
BUILD_MODE = "C8_BASIC_INTERLOCK_MECHANIC_REFERENCE_FREEZE_ONLY"

SOURCE_MECHANIC_RECEIPT_ID = "d3d2ab5e"
SOURCE_POST_C8_DECISION_RECEIPT_ID = "04f99452"
SOURCE_C8_TARGET_SHAPE_REFERENCE_RECEIPT_ID = "ea23fd9b"

MECHANIC_RECEIPT_PATH = ROOT / "data/c8_basic_interlock_mechanic_from_target_shape_reference_v0_receipts/d3d2ab5e.json"
MECHANIC_PATH = ROOT / "data/c8_basic_interlock_mechanic_from_target_shape_reference_v0/c8_basic_interlock_mechanic_v0.json"
MECHANIC_BASIS_PATH = ROOT / "data/c8_basic_interlock_mechanic_from_target_shape_reference_v0/c8_basic_interlock_mechanic_basis_v0.json"
MECHANIC_FLOW_PATH = ROOT / "data/c8_basic_interlock_mechanic_from_target_shape_reference_v0/c8_basic_interlock_mechanic_flow_v0.json"
MECHANIC_COMPONENT_MAP_PATH = ROOT / "data/c8_basic_interlock_mechanic_from_target_shape_reference_v0/c8_basic_interlock_component_map_v0.json"
MECHANIC_BOUNDARY_PATH = ROOT / "data/c8_basic_interlock_mechanic_from_target_shape_reference_v0/c8_basic_interlock_mechanic_boundary_v0.json"
MECHANIC_NON_AUTHORIZATION_PATH = ROOT / "data/c8_basic_interlock_mechanic_from_target_shape_reference_v0/c8_basic_interlock_mechanic_non_authorization_v0.json"
MECHANIC_ACCEPTANCE_GATE_PATH = ROOT / "data/c8_basic_interlock_mechanic_from_target_shape_reference_v0/c8_basic_interlock_mechanic_acceptance_gate_v0.json"
MECHANIC_NEXT_SURFACE_PATH = ROOT / "data/c8_basic_interlock_mechanic_from_target_shape_reference_v0/c8_basic_interlock_mechanic_next_surface_v0.json"
MECHANIC_ROLLUP_PATH = ROOT / "data/c8_basic_interlock_mechanic_from_target_shape_reference_v0/c8_basic_interlock_mechanic_rollup_v0.json"
MECHANIC_PROFILE_PATH = ROOT / "data/c8_basic_interlock_mechanic_from_target_shape_reference_v0/c8_basic_interlock_mechanic_profile_v0.json"

POST_C8_DECISION_RECEIPT_PATH = ROOT / "data/post_c8_target_shape_reference_decision_v0_receipts/04f99452.json"
C8_TARGET_SHAPE_REFERENCE_RECEIPT_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0_receipts/ea23fd9b.json"
C8_TARGET_SHAPE_REVIEWED_REFERENCE_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0/c8_target_shape_reviewed_reference_v0.json"
SCHEMA_VALIDATOR_REFERENCE_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0/runtime_schema_validator_reviewed_reference_v0.json"
SIDECAR_REVIEWED_REFERENCE_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/runtime_observability_sidecar_reviewed_reference_v0.json"

OUT_DIR = ROOT / "data/c8_basic_interlock_mechanic_reviewed_reference_v0"
RECEIPT_DIR = ROOT / "data/c8_basic_interlock_mechanic_reviewed_reference_v0_receipts"

BASIS_PATH = OUT_DIR / "c8_basic_interlock_mechanic_reference_freeze_basis_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "c8_basic_interlock_mechanic_reviewed_reference_v0.json"
FREEZE_MANIFEST_PATH = OUT_DIR / "c8_basic_interlock_mechanic_reviewed_reference_freeze_manifest_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "c8_basic_interlock_mechanic_reference_index_v0.json"
BOUNDARY_PATH = OUT_DIR / "c8_basic_interlock_mechanic_reference_boundary_v0.json"
NON_AUTHORIZATION_PATH = OUT_DIR / "c8_basic_interlock_mechanic_reference_non_authorization_v0.json"
ROLLUP_PATH = OUT_DIR / "c8_basic_interlock_mechanic_reference_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c8_basic_interlock_mechanic_reference_profile_v0.json"
TRACE_PATH = OUT_DIR / "c8_basic_interlock_mechanic_reference_transition_trace.json"
POST_FREEZE_DECISION_READY_PATH = OUT_DIR / "post_c8_basic_interlock_mechanic_reference_decision_ready_v0.json"

EXPECTED_MECHANIC_STATUS = "TYPED_C8_BASIC_INTERLOCK_MECHANIC_PREPARED_NO_RUNTIME_ADOPTION"

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
        MECHANIC_RECEIPT_PATH,
        MECHANIC_PATH,
        MECHANIC_BASIS_PATH,
        MECHANIC_FLOW_PATH,
        MECHANIC_COMPONENT_MAP_PATH,
        MECHANIC_BOUNDARY_PATH,
        MECHANIC_NON_AUTHORIZATION_PATH,
        MECHANIC_ACCEPTANCE_GATE_PATH,
        MECHANIC_NEXT_SURFACE_PATH,
        MECHANIC_ROLLUP_PATH,
        MECHANIC_PROFILE_PATH,
        POST_C8_DECISION_RECEIPT_PATH,
        C8_TARGET_SHAPE_REFERENCE_RECEIPT_PATH,
        C8_TARGET_SHAPE_REVIEWED_REFERENCE_PATH,
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

    mechanic_receipt = read_json(MECHANIC_RECEIPT_PATH)
    mechanic = read_json(MECHANIC_PATH)
    basis_src = read_json(MECHANIC_BASIS_PATH)
    flow = read_json(MECHANIC_FLOW_PATH)
    component_map = read_json(MECHANIC_COMPONENT_MAP_PATH)
    boundary_src = read_json(MECHANIC_BOUNDARY_PATH)
    non_auth_src = read_json(MECHANIC_NON_AUTHORIZATION_PATH)
    acceptance_gate_src = read_json(MECHANIC_ACCEPTANCE_GATE_PATH)
    next_surface_src = read_json(MECHANIC_NEXT_SURFACE_PATH)
    rollup_src = read_json(MECHANIC_ROLLUP_PATH)
    profile_src = read_json(MECHANIC_PROFILE_PATH)

    post_c8_decision_receipt = read_json(POST_C8_DECISION_RECEIPT_PATH)
    c8_target_shape_reference_receipt = read_json(C8_TARGET_SHAPE_REFERENCE_RECEIPT_PATH)
    c8_target_shape_reference = read_json(C8_TARGET_SHAPE_REVIEWED_REFERENCE_PATH)
    schema_validator_reference = read_json(SCHEMA_VALIDATOR_REFERENCE_PATH)
    sidecar_reference = read_json(SIDECAR_REVIEWED_REFERENCE_PATH)

    mechanic_summary = mechanic_receipt.get("machine_readable_c8_basic_interlock_mechanic_summary", {})

    if mechanic_receipt.get("receipt_id") != SOURCE_MECHANIC_RECEIPT_ID:
        failures.append(f"mechanic_receipt_id_wrong:{mechanic_receipt.get('receipt_id')}")
    if mechanic_receipt.get("gate") != "PASS":
        failures.append(f"mechanic_receipt_gate_wrong:{mechanic_receipt.get('gate')}")
    if mechanic_summary.get("status") != EXPECTED_MECHANIC_STATUS:
        failures.append(f"mechanic_status_wrong:{mechanic_summary.get('status')}")
    if mechanic_summary.get("c8_basic_interlock_mechanic_prepared") is not True:
        failures.append("mechanic_not_prepared")
    if mechanic_summary.get("next_unit_id") != UNIT_ID:
        failures.append(f"mechanic_next_unit_wrong:{mechanic_summary.get('next_unit_id')}")
    if mechanic_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("mechanic_terminal_not_advance")
    if mechanic_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("mechanic_terminal_next_wrong")

    if mechanic.get("mechanic_status") != EXPECTED_MECHANIC_STATUS:
        failures.append(f"mechanic_artifact_status_wrong:{mechanic.get('mechanic_status')}")
    if mechanic.get("mechanic_kind") != "TYPE_ONLY_REFERENCE_MECHANIC":
        failures.append(f"mechanic_kind_wrong:{mechanic.get('mechanic_kind')}")
    if mechanic.get("reference_only") is not True:
        failures.append("mechanic_not_reference_only")
    if len(component_map.get("components", [])) != 4:
        failures.append(f"component_count_wrong:{len(component_map.get('components', []))}")
    if len(flow.get("flow_edges", [])) != 4:
        failures.append(f"flow_edge_count_wrong:{len(flow.get('flow_edges', []))}")
    if len(mechanic.get("minimum_mechanic_fields", [])) != 7:
        failures.append("minimum_mechanic_field_count_wrong")
    if len(mechanic.get("required_load_bearing_decision_edge_fields", [])) != 7:
        failures.append("load_bearing_edge_field_count_wrong")
    if len(mechanic.get("allowed_terminal_results", [])) != 5:
        failures.append("terminal_result_count_wrong")

    if basis_src.get("basis_status") != "BASIS_ACCEPTED":
        failures.append(f"basis_status_wrong:{basis_src.get('basis_status')}")
    if boundary_src.get("boundary_status") != "BOUNDARY_HELD":
        failures.append(f"boundary_status_wrong:{boundary_src.get('boundary_status')}")
    if acceptance_gate_src.get("gate_status") != "PASS":
        failures.append(f"acceptance_gate_status_wrong:{acceptance_gate_src.get('gate_status')}")
    if next_surface_src.get("next_unit_id") != UNIT_ID:
        failures.append(f"next_surface_next_unit_wrong:{next_surface_src.get('next_unit_id')}")
    if rollup_src.get("c8_basic_interlock_mechanic_prepared") is not True:
        failures.append("rollup_mechanic_not_prepared")
    if profile_src.get("recommended_next") != UNIT_ID:
        failures.append(f"profile_recommended_next_wrong:{profile_src.get('recommended_next')}")
    if profile_src.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")

    if post_c8_decision_receipt.get("receipt_id") != SOURCE_POST_C8_DECISION_RECEIPT_ID:
        failures.append(f"post_c8_decision_receipt_id_wrong:{post_c8_decision_receipt.get('receipt_id')}")
    if post_c8_decision_receipt.get("gate") != "PASS":
        failures.append("post_c8_decision_receipt_gate_not_pass")
    if c8_target_shape_reference_receipt.get("receipt_id") != SOURCE_C8_TARGET_SHAPE_REFERENCE_RECEIPT_ID:
        failures.append(f"c8_target_shape_reference_receipt_id_wrong:{c8_target_shape_reference_receipt.get('receipt_id')}")
    if c8_target_shape_reference.get("reference_status") != "C8_TARGET_SHAPE_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"c8_target_shape_reference_status_wrong:{c8_target_shape_reference.get('reference_status')}")
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
        require_false(mechanic_summary, key, failures)
        require_false(non_auth_src, key, failures)

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_BASIC_INTERLOCK_MECHANIC_FROZEN_AS_REVIEWED_REFERENCE_DECISION_READY" if gate == "PASS" else "TYPED_C8_BASIC_INTERLOCK_MECHANIC_REFERENCE_FREEZE_GATE_FAIL"

    source_hash_manifest = {rel(p): file_sha256(p) for p in required}

    reason_codes = [
        "C8_BASIC_INTERLOCK_MECHANIC_FROZEN_AS_REVIEWED_REFERENCE",
        "C8_BASIC_INTERLOCK_MECHANIC_RECEIPT_CONSUMED",
        "C8_BASIC_INTERLOCK_MECHANIC_ARTIFACTS_CONSUMED",
        "POST_C8_TARGET_SHAPE_DECISION_RECEIPT_CONSUMED",
        "C8_TARGET_SHAPE_REFERENCE_CONSUMED",
        "SCHEMA_VALIDATOR_REFERENCE_CONSUMED",
        "RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CONSUMED",
        "REFERENCE_ONLY_FREEZE",
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
        "POST_C8_BASIC_INTERLOCK_MECHANIC_REFERENCE_DECISION_READY",
    ] if gate == "PASS" else failures

    basis = {
        "schema_version": "c8_basic_interlock_mechanic_reference_freeze_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_mechanic_receipt_id": SOURCE_MECHANIC_RECEIPT_ID,
        "source_post_c8_decision_receipt_id": SOURCE_POST_C8_DECISION_RECEIPT_ID,
        "source_c8_target_shape_reference_receipt_id": SOURCE_C8_TARGET_SHAPE_REFERENCE_RECEIPT_ID,
        "source_files": source_hash_manifest,
        "freeze_scope": "freeze the prepared C8 basic interlock mechanic as reviewed reference only",
        "freeze_does_not_mean": [
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

    reviewed_reference = {
        "schema_version": "c8_basic_interlock_mechanic_reviewed_reference_v0",
        "reference_status": "C8_BASIC_INTERLOCK_MECHANIC_REVIEWED_REFERENCE_FROZEN" if gate == "PASS" else "NOT_FROZEN",
        "source_mechanic_receipt_id": SOURCE_MECHANIC_RECEIPT_ID,
        "source_mechanic_path": rel(MECHANIC_PATH),
        "mechanic_name": mechanic.get("mechanic_name"),
        "mechanic_kind": mechanic.get("mechanic_kind"),
        "mechanic_role": mechanic.get("mechanic_role"),
        "core_compression": mechanic.get("core_compression"),
        "one_step_flow": mechanic.get("one_step_flow"),
        "component_map": component_map.get("components"),
        "flow_edges": flow.get("flow_edges"),
        "minimum_mechanic_fields": mechanic.get("minimum_mechanic_fields"),
        "allowed_terminal_results": mechanic.get("allowed_terminal_results"),
        "required_load_bearing_decision_edge_fields": mechanic.get("required_load_bearing_decision_edge_fields"),
        "must_not_impersonate": mechanic.get("must_not_impersonate"),
        "reference_only": True,
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

    freeze_manifest = {
        "schema_version": "c8_basic_interlock_mechanic_reviewed_reference_freeze_manifest_v0",
        "freeze_status": "FROZEN" if gate == "PASS" else "NOT_FROZEN",
        "reference_id": "c8_basic_interlock_mechanic_reviewed_reference_v0",
        "reference_path": rel(REVIEWED_REFERENCE_PATH),
        "source_hash_manifest": source_hash_manifest,
        "frozen_artifacts": {
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "basis": rel(BASIS_PATH),
            "reference_index": rel(REFERENCE_INDEX_PATH),
            "boundary": rel(BOUNDARY_PATH),
            "non_authorization": rel(NON_AUTHORIZATION_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "post_freeze_decision_ready": rel(POST_FREEZE_DECISION_READY_PATH),
        },
    }

    reference_index = {
        "schema_version": "c8_basic_interlock_mechanic_reference_index_v0",
        "index_status": "REFERENCE_INDEX_EMITTED" if gate == "PASS" else "NOT_EMITTED",
        "entries": [
            {"name": "reviewed_reference", "path": rel(REVIEWED_REFERENCE_PATH)},
            {"name": "freeze_manifest", "path": rel(FREEZE_MANIFEST_PATH)},
            {"name": "basis", "path": rel(BASIS_PATH)},
            {"name": "boundary", "path": rel(BOUNDARY_PATH)},
            {"name": "non_authorization", "path": rel(NON_AUTHORIZATION_PATH)},
            {"name": "rollup", "path": rel(ROLLUP_PATH)},
            {"name": "profile", "path": rel(PROFILE_PATH)},
            {"name": "transition_trace", "path": rel(TRACE_PATH)},
            {"name": "post_freeze_decision_ready", "path": rel(POST_FREEZE_DECISION_READY_PATH)},
        ],
    }

    boundary = {
        "schema_version": "c8_basic_interlock_mechanic_reference_boundary_v0",
        "boundary_status": "BOUNDARY_HELD" if gate == "PASS" else "BOUNDARY_FAIL",
        "allowed": [
            "consume prepared C8 basic interlock mechanic receipt",
            "consume mechanic artifacts",
            "freeze mechanic as reviewed reference",
            "emit freeze manifest",
            "emit reference index",
            "emit post-freeze decision-ready marker",
        ],
        "forbidden": [
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
        "schema_version": "c8_basic_interlock_mechanic_reference_non_authorization_v0",
        "c8_basic_interlock_mechanic_reference_frozen": gate == "PASS",
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

    rollup = {
        "schema_version": "c8_basic_interlock_mechanic_reference_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "source_mechanic_receipt_id": SOURCE_MECHANIC_RECEIPT_ID,
        "c8_basic_interlock_mechanic_reference_frozen": gate == "PASS",
        "component_count": mechanic_summary.get("component_count") if gate == "PASS" else 0,
        "flow_edge_count": mechanic_summary.get("flow_edge_count") if gate == "PASS" else 0,
        "minimum_mechanic_field_count": mechanic_summary.get("minimum_mechanic_field_count") if gate == "PASS" else 0,
        "load_bearing_edge_field_count": mechanic_summary.get("load_bearing_edge_field_count") if gate == "PASS" else 0,
        "terminal_result_count": mechanic_summary.get("terminal_result_count") if gate == "PASS" else 0,
        "c8_runtime_authorized": False,
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "control_path_authority_granted": False,
        "hidden_next_command": False,
    }

    profile = {
        "schema_version": "c8_basic_interlock_mechanic_reference_profile_v0",
        "profile_status": status,
        "profile": "C8_BASIC_INTERLOCK_MECHANIC_REVIEWED_REFERENCE_FREEZE",
        "what_changed": "The prepared C8 basic interlock mechanic was frozen as a reviewed reference.",
        "what_did_not_change": [
            "C8 is not runtime-authorized",
            "C8 is not executed",
            "runtime is not patched",
            "live hooks are not installed",
            "schema archive is not mutated",
            "control path authority is not granted",
            "live admissibility/authorization verdicts are not emitted",
        ],
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_C8_BASIC_INTERLOCK_MECHANIC_REFERENCE_FREEZE_V0",
        "next_command_goal": None,
    }

    post_freeze_decision_ready = {
        "schema_version": "post_c8_basic_interlock_mechanic_reference_decision_ready_v0",
        "decision_ready": gate == "PASS",
        "source_c8_basic_interlock_mechanic_reference_status": reviewed_reference.get("reference_status"),
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else None,
        "next_scope": "decide the next lawful handling after the C8 basic interlock mechanic has been frozen as reviewed reference",
        "does_not_authorize_runtime_adoption": True,
        "does_not_authorize_execution": True,
    }

    trace = {
        "schema_version": "c8_basic_interlock_mechanic_reference_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "C8_BASIC_INTERLOCK_MECHANIC_PREPARED_NO_RUNTIME_ADOPTION",
                "edge": "consume prepared mechanic",
                "to": "C8_BASIC_INTERLOCK_MECHANIC_REFERENCE_BASIS_ACCEPTED" if gate == "PASS" else "C8_BASIC_INTERLOCK_MECHANIC_REFERENCE_BASIS_FAIL",
            },
            {
                "from": "C8_BASIC_INTERLOCK_MECHANIC_REFERENCE_BASIS_ACCEPTED" if gate == "PASS" else "C8_BASIC_INTERLOCK_MECHANIC_REFERENCE_BASIS_FAIL",
                "edge": "freeze as reviewed reference only",
                "to": "C8_BASIC_INTERLOCK_MECHANIC_FROZEN_AS_REVIEWED_REFERENCE_DECISION_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C8_BASIC_INTERLOCK_MECHANIC_REFERENCE_FREEZE_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (REVIEWED_REFERENCE_PATH, reviewed_reference),
        (FREEZE_MANIFEST_PATH, freeze_manifest),
        (REFERENCE_INDEX_PATH, reference_index),
        (BOUNDARY_PATH, boundary),
        (NON_AUTHORIZATION_PATH, non_authorization),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_PATH, trace),
        (POST_FREEZE_DECISION_READY_PATH, post_freeze_decision_ready),
    ]:
        write_json(path, obj)

    receipt_body = {
        "schema_version": "c8_basic_interlock_mechanic_reviewed_reference_receipt_v0",
        "receipt_type": "TYPED_C8_BASIC_INTERLOCK_MECHANIC_REVIEWED_REFERENCE_RECEIPT",
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
        "source_mechanic_receipt_id": SOURCE_MECHANIC_RECEIPT_ID,
        "source_post_c8_decision_receipt_id": SOURCE_POST_C8_DECISION_RECEIPT_ID,
        "source_c8_target_shape_reference_receipt_id": SOURCE_C8_TARGET_SHAPE_REFERENCE_RECEIPT_ID,
        "acceptance_gate_results": {
            "C8_BASIC_INTERLOCK_FREEZE_0_MECHANIC_RECEIPT_CONSUMED": gate == "PASS",
            "C8_BASIC_INTERLOCK_FREEZE_1_MECHANIC_ARTIFACTS_CONSUMED": gate == "PASS",
            "C8_BASIC_INTERLOCK_FREEZE_2_REVIEWED_REFERENCE_EMITTED": gate == "PASS",
            "C8_BASIC_INTERLOCK_FREEZE_3_FREEZE_MANIFEST_EMITTED": gate == "PASS",
            "C8_BASIC_INTERLOCK_FREEZE_4_REFERENCE_INDEX_EMITTED": gate == "PASS",
            "C8_BASIC_INTERLOCK_FREEZE_5_NO_RUNTIME_ADOPTION": gate == "PASS",
            "C8_BASIC_INTERLOCK_FREEZE_6_NO_EXECUTION_OR_AUTHORIZATION": gate == "PASS",
            "C8_BASIC_INTERLOCK_FREEZE_7_NO_SCHEMA_OR_REFERENCE_MUTATION": gate == "PASS",
            "C8_BASIC_INTERLOCK_FREEZE_8_NO_CONTROL_PATH_AUTHORITY": gate == "PASS",
            "C8_BASIC_INTERLOCK_FREEZE_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_c8_basic_interlock_mechanic_reference_summary": {
            "status": status,
            "c8_basic_interlock_mechanic_reference_frozen": gate == "PASS",
            "source_mechanic_receipt_consumed": gate == "PASS",
            "source_post_c8_decision_receipt_consumed": gate == "PASS",
            "source_c8_target_shape_reference_consumed": gate == "PASS",
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
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "freeze_manifest": rel(FREEZE_MANIFEST_PATH),
            "reference_index": rel(REFERENCE_INDEX_PATH),
            "boundary": rel(BOUNDARY_PATH),
            "non_authorization": rel(NON_AUTHORIZATION_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "transition_trace": rel(TRACE_PATH),
            "post_freeze_decision_ready": rel(POST_FREEZE_DECISION_READY_PATH),
        },
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C8_BASIC_INTERLOCK_MECHANIC_REFERENCE_FREEZE_GATE_FAIL",
        },
    }

    receipt_id = sig8(receipt_body)
    receipt_body["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_body["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_body)

    print(json.dumps(receipt_body, indent=2, sort_keys=True))
    print(f"c8_basic_interlock_mechanic_reference_receipt_id={receipt_id}")
    print(f"c8_basic_interlock_mechanic_reference_receipt_path={rel(receipt_path)}")
    print(f"c8_basic_interlock_mechanic_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"c8_basic_interlock_mechanic_reference_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
