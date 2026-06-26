#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_OR_FREEZE_C8_TARGET_SHAPE_V0"
TARGET_UNIT_ID = "c8.target_shape.reviewed_reference.v0"
NEXT_UNIT_ID = "DECIDE_NEXT_AFTER_C8_TARGET_SHAPE_REFERENCE_FREEZE_V0"

LAYER = "RUNTIME / C8 / TARGET_SHAPE_REFERENCE"
MODE = "FREEZE_REFERENCE_ONLY / NO_RUNTIME_ADOPTION / NO_EXECUTION"
BUILD_MODE = "C8_TARGET_SHAPE_REFERENCE_FREEZE_ONLY"

SOURCE_C8_TARGET_SHAPE_RECEIPT_ID = "ec404930"
SOURCE_POST_DECISION_RECEIPT_ID = "62ddebf9"
SOURCE_SCHEMA_VALIDATOR_REFERENCE_CLOSURE_RECEIPT_ID = "732016f0"
SOURCE_SIDECAR_CLOSURE_RECEIPT_ID = "bee348a1"

C8_TARGET_SHAPE_RECEIPT_PATH = ROOT / "data/c8_target_shape_from_pre_c8_interlock_pair_v0_receipts/ec404930.json"
C8_TARGET_SHAPE_PATH = ROOT / "data/c8_target_shape_from_pre_c8_interlock_pair_v0/c8_target_shape_v0.json"
C8_TARGET_SHAPE_BASIS_PATH = ROOT / "data/c8_target_shape_from_pre_c8_interlock_pair_v0/c8_target_shape_basis_v0.json"
C8_TARGET_SHAPE_BOUNDARY_PATH = ROOT / "data/c8_target_shape_from_pre_c8_interlock_pair_v0/c8_target_shape_boundary_v0.json"
C8_TARGET_SHAPE_INTERLOCK_MAP_PATH = ROOT / "data/c8_target_shape_from_pre_c8_interlock_pair_v0/c8_target_shape_interlock_map_v0.json"
C8_TARGET_SHAPE_NON_AUTHORIZATION_PATH = ROOT / "data/c8_target_shape_from_pre_c8_interlock_pair_v0/c8_target_shape_non_authorization_v0.json"
C8_TARGET_SHAPE_NEXT_SURFACE_PATH = ROOT / "data/c8_target_shape_from_pre_c8_interlock_pair_v0/c8_target_shape_next_surface_v0.json"
C8_TARGET_SHAPE_ROLLUP_PATH = ROOT / "data/c8_target_shape_from_pre_c8_interlock_pair_v0/c8_target_shape_rollup_v0.json"
C8_TARGET_SHAPE_PROFILE_PATH = ROOT / "data/c8_target_shape_from_pre_c8_interlock_pair_v0/c8_target_shape_profile_v0.json"

POST_DECISION_RECEIPT_PATH = ROOT / "data/post_runtime_observability_sidecar_reference_decision_v0_receipts/62ddebf9.json"
SCHEMA_VALIDATOR_REFERENCE_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0/runtime_schema_validator_reviewed_reference_v0.json"
SIDECAR_REVIEWED_REFERENCE_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/runtime_observability_sidecar_reviewed_reference_v0.json"
PRE_C8_INTERLOCK_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/pre_c8_interlock_completion_reference_v0.json"

OUT_DIR = ROOT / "data/c8_target_shape_reviewed_reference_v0"
RECEIPT_DIR = ROOT / "data/c8_target_shape_reviewed_reference_v0_receipts"

BASIS_PATH = OUT_DIR / "c8_target_shape_reference_freeze_basis_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "c8_target_shape_reviewed_reference_v0.json"
FREEZE_MANIFEST_PATH = OUT_DIR / "c8_target_shape_reviewed_reference_freeze_manifest_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "c8_target_shape_reference_index_v0.json"
BOUNDARY_PATH = OUT_DIR / "c8_target_shape_reference_boundary_v0.json"
NON_AUTHORIZATION_PATH = OUT_DIR / "c8_target_shape_reference_non_authorization_v0.json"
ROLLUP_PATH = OUT_DIR / "c8_target_shape_reference_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c8_target_shape_reference_profile_v0.json"
TRACE_PATH = OUT_DIR / "c8_target_shape_reference_transition_trace.json"
POST_FREEZE_DECISION_READY_PATH = OUT_DIR / "post_c8_target_shape_reference_decision_ready_v0.json"

EXPECTED_C8_TARGET_SHAPE_STATUS = "TYPED_C8_TARGET_SHAPE_PREPARED_NO_RUNTIME_ADOPTION"
EXPECTED_NEXT_FROM_TARGET_SHAPE = UNIT_ID

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
        C8_TARGET_SHAPE_RECEIPT_PATH,
        C8_TARGET_SHAPE_PATH,
        C8_TARGET_SHAPE_BASIS_PATH,
        C8_TARGET_SHAPE_BOUNDARY_PATH,
        C8_TARGET_SHAPE_INTERLOCK_MAP_PATH,
        C8_TARGET_SHAPE_NON_AUTHORIZATION_PATH,
        C8_TARGET_SHAPE_NEXT_SURFACE_PATH,
        C8_TARGET_SHAPE_ROLLUP_PATH,
        C8_TARGET_SHAPE_PROFILE_PATH,
        POST_DECISION_RECEIPT_PATH,
        SCHEMA_VALIDATOR_REFERENCE_PATH,
        SIDECAR_REVIEWED_REFERENCE_PATH,
        PRE_C8_INTERLOCK_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    c8_receipt = read_json(C8_TARGET_SHAPE_RECEIPT_PATH)
    c8_shape = read_json(C8_TARGET_SHAPE_PATH)
    c8_basis = read_json(C8_TARGET_SHAPE_BASIS_PATH)
    c8_boundary = read_json(C8_TARGET_SHAPE_BOUNDARY_PATH)
    c8_interlock_map = read_json(C8_TARGET_SHAPE_INTERLOCK_MAP_PATH)
    c8_non_authorization = read_json(C8_TARGET_SHAPE_NON_AUTHORIZATION_PATH)
    c8_next_surface = read_json(C8_TARGET_SHAPE_NEXT_SURFACE_PATH)
    c8_rollup = read_json(C8_TARGET_SHAPE_ROLLUP_PATH)
    c8_profile = read_json(C8_TARGET_SHAPE_PROFILE_PATH)

    post_decision_receipt = read_json(POST_DECISION_RECEIPT_PATH)
    schema_validator_reference = read_json(SCHEMA_VALIDATOR_REFERENCE_PATH)
    sidecar_reference = read_json(SIDECAR_REVIEWED_REFERENCE_PATH)
    pre_c8_interlock = read_json(PRE_C8_INTERLOCK_PATH)

    c8_summary = c8_receipt.get("machine_readable_c8_target_shape_summary", {})

    if c8_receipt.get("receipt_id") != SOURCE_C8_TARGET_SHAPE_RECEIPT_ID:
        failures.append(f"c8_receipt_id_wrong:{c8_receipt.get('receipt_id')}")
    if c8_receipt.get("gate") != "PASS":
        failures.append(f"c8_receipt_gate_wrong:{c8_receipt.get('gate')}")
    if c8_summary.get("status") != EXPECTED_C8_TARGET_SHAPE_STATUS:
        failures.append(f"c8_target_shape_status_wrong:{c8_summary.get('status')}")
    if c8_summary.get("c8_target_shape_prepared") is not True:
        failures.append("c8_target_shape_not_prepared")
    if c8_summary.get("next_unit_id") != UNIT_ID:
        failures.append(f"c8_target_shape_next_unit_wrong:{c8_summary.get('next_unit_id')}")
    if c8_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("c8_receipt_terminal_not_advance")
    if c8_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("c8_receipt_terminal_next_wrong")

    if c8_shape.get("target_shape_status") != EXPECTED_C8_TARGET_SHAPE_STATUS:
        failures.append(f"target_shape_artifact_status_wrong:{c8_shape.get('target_shape_status')}")
    if c8_shape.get("shape_kind") != "TYPE_ONLY_REFERENCE_TARGET":
        failures.append(f"target_shape_kind_wrong:{c8_shape.get('shape_kind')}")
    if c8_shape.get("shape_role") != "Define the smallest C8 target surface made visible by the completed pre-C8 interlock pair.":
        failures.append("target_shape_role_wrong")
    if len(c8_shape.get("components", [])) != 3:
        failures.append(f"target_shape_component_count_wrong:{len(c8_shape.get('components', []))}")
    if len(c8_shape.get("minimum_c8_shape_fields", [])) != 7:
        failures.append("target_shape_minimum_field_count_wrong")
    if len(c8_shape.get("required_load_bearing_decision_edge_fields", [])) != 7:
        failures.append("target_shape_load_bearing_field_count_wrong")

    for comp in c8_shape.get("components", []):
        for key, value in comp.items():
            if key.startswith("may_") and value is not False:
                failures.append(f"component_may_flag_not_false:{comp.get('component_id')}:{key}:{value}")

    if c8_basis.get("basis_status") != "BASIS_ACCEPTED":
        failures.append(f"basis_status_wrong:{c8_basis.get('basis_status')}")
    if c8_boundary.get("boundary_status") != "BOUNDARY_HELD":
        failures.append(f"boundary_status_wrong:{c8_boundary.get('boundary_status')}")
    if c8_interlock_map.get("pre_c8_interlock_pair_complete") is not True:
        failures.append("interlock_map_pair_not_complete")
    if c8_rollup.get("c8_target_shape_prepared") is not True:
        failures.append("rollup_target_shape_not_prepared")
    if c8_profile.get("recommended_next") != UNIT_ID:
        failures.append(f"profile_recommended_next_wrong:{c8_profile.get('recommended_next')}")
    if c8_profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")

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
        require_false(c8_summary, key, failures)
        require_false(c8_non_authorization, key, failures)

    if post_decision_receipt.get("receipt_id") != SOURCE_POST_DECISION_RECEIPT_ID:
        failures.append(f"post_decision_receipt_id_wrong:{post_decision_receipt.get('receipt_id')}")
    if schema_validator_reference.get("reference_status") != "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"schema_validator_reference_status_wrong:{schema_validator_reference.get('reference_status')}")
    if sidecar_reference.get("reference_status") != "RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"sidecar_reference_status_wrong:{sidecar_reference.get('reference_status')}")
    if pre_c8_interlock.get("completion_status") != "PRE_C8_INTERLOCK_PAIR_COMPLETE":
        failures.append(f"pre_c8_interlock_status_wrong:{pre_c8_interlock.get('completion_status')}")
    if pre_c8_interlock.get("does_not_authorize_c8_by_itself") is not True:
        failures.append("pre_c8_interlock_non_authorization_wrong")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_TARGET_SHAPE_FROZEN_AS_REVIEWED_REFERENCE_DECISION_READY" if gate == "PASS" else "TYPED_C8_TARGET_SHAPE_REFERENCE_FREEZE_GATE_FAIL"

    source_hash_manifest = {rel(p): file_sha256(p) for p in required}

    reason_codes = [
        "C8_TARGET_SHAPE_FROZEN_AS_REVIEWED_REFERENCE",
        "C8_TARGET_SHAPE_RECEIPT_CONSUMED",
        "POST_SIDECAR_DECISION_RECEIPT_CONSUMED",
        "SCHEMA_VALIDATOR_REFERENCE_CONSUMED",
        "RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CONSUMED",
        "PRE_C8_INTERLOCK_PAIR_COMPLETE",
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
        "POST_C8_TARGET_SHAPE_REFERENCE_DECISION_READY",
    ] if gate == "PASS" else failures

    basis = {
        "schema_version": "c8_target_shape_reference_freeze_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_c8_target_shape_receipt_id": SOURCE_C8_TARGET_SHAPE_RECEIPT_ID,
        "source_post_decision_receipt_id": SOURCE_POST_DECISION_RECEIPT_ID,
        "source_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_REFERENCE_CLOSURE_RECEIPT_ID,
        "source_sidecar_closure_receipt_id": SOURCE_SIDECAR_CLOSURE_RECEIPT_ID,
        "source_files": source_hash_manifest,
        "freeze_scope": "freeze the prepared C8 target shape as reviewed reference only",
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
        "schema_version": "c8_target_shape_reviewed_reference_v0",
        "reference_status": "C8_TARGET_SHAPE_REVIEWED_REFERENCE_FROZEN" if gate == "PASS" else "NOT_FROZEN",
        "source_c8_target_shape_receipt_id": SOURCE_C8_TARGET_SHAPE_RECEIPT_ID,
        "source_target_shape_path": rel(C8_TARGET_SHAPE_PATH),
        "shape_name": c8_shape.get("shape_name"),
        "shape_kind": c8_shape.get("shape_kind"),
        "shape_role": c8_shape.get("shape_role"),
        "core_compression": c8_shape.get("core_compression"),
        "components": c8_shape.get("components"),
        "minimum_c8_shape_fields": c8_shape.get("minimum_c8_shape_fields"),
        "required_load_bearing_decision_edge_fields": c8_shape.get("required_load_bearing_decision_edge_fields"),
        "must_not_impersonate": c8_shape.get("must_not_impersonate"),
        "reference_only": True,
        "runtime_adoption_authorized": False,
        "c8_runtime_authorized": False,
        "c8_execution_authorized": False,
        "live_runtime_hooks_installed": False,
        "runtime_patched": False,
        "runtime_routing_installed": False,
        "validation_verdict_emitted": False,
        "admissibility_checked": False,
        "authorization_verdict_emitted": False,
        "execution_claimed": False,
        "schema_archive_mutated": False,
        "control_path_authority_granted": False,
    }

    freeze_manifest = {
        "schema_version": "c8_target_shape_reviewed_reference_freeze_manifest_v0",
        "freeze_status": "FROZEN" if gate == "PASS" else "NOT_FROZEN",
        "reference_id": "c8_target_shape_reviewed_reference_v0",
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
        "schema_version": "c8_target_shape_reference_index_v0",
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
        "schema_version": "c8_target_shape_reference_boundary_v0",
        "boundary_status": "BOUNDARY_HELD" if gate == "PASS" else "BOUNDARY_FAIL",
        "allowed": [
            "consume prepared C8 target-shape receipt",
            "consume target-shape artifacts",
            "freeze target shape as reviewed reference",
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
            "emit validation verdict",
            "emit admissibility verdict",
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
        "schema_version": "c8_target_shape_reference_non_authorization_v0",
        "c8_target_shape_reference_frozen": gate == "PASS",
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
        "schema_version": "c8_target_shape_reference_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "source_c8_target_shape_receipt_id": SOURCE_C8_TARGET_SHAPE_RECEIPT_ID,
        "c8_target_shape_reference_frozen": gate == "PASS",
        "component_count": c8_summary.get("component_count") if gate == "PASS" else 0,
        "minimum_shape_field_count": c8_summary.get("minimum_shape_field_count") if gate == "PASS" else 0,
        "load_bearing_edge_field_count": c8_summary.get("load_bearing_edge_field_count") if gate == "PASS" else 0,
        "runtime_adoption_authorized": False,
        "c8_runtime_authorized": False,
        "c8_execution_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "control_path_authority_granted": False,
        "hidden_next_command": False,
    }

    profile = {
        "schema_version": "c8_target_shape_reference_profile_v0",
        "profile_status": status,
        "profile": "C8_TARGET_SHAPE_REVIEWED_REFERENCE_FREEZE",
        "what_changed": "The prepared C8 target shape was frozen as a reviewed reference.",
        "what_did_not_change": [
            "C8 is not runtime-authorized",
            "C8 is not executed",
            "runtime is not patched",
            "live hooks are not installed",
            "schema archive is not mutated",
            "control path authority is not granted",
            "admissibility/authorization verdicts are not emitted",
        ],
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_C8_TARGET_SHAPE_REFERENCE_FREEZE_V0",
        "next_command_goal": None,
    }

    post_freeze_decision_ready = {
        "schema_version": "post_c8_target_shape_reference_decision_ready_v0",
        "decision_ready": gate == "PASS",
        "source_c8_target_shape_reference_status": reviewed_reference.get("reference_status"),
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else None,
        "next_scope": "decide the next lawful handling after the C8 target shape has been frozen as reviewed reference",
        "does_not_authorize_runtime_adoption": True,
        "does_not_authorize_execution": True,
    }

    trace = {
        "schema_version": "c8_target_shape_reference_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "C8_TARGET_SHAPE_PREPARED_NO_RUNTIME_ADOPTION",
                "edge": "consume prepared target shape",
                "to": "C8_TARGET_SHAPE_REFERENCE_BASIS_ACCEPTED" if gate == "PASS" else "C8_TARGET_SHAPE_REFERENCE_BASIS_FAIL",
            },
            {
                "from": "C8_TARGET_SHAPE_REFERENCE_BASIS_ACCEPTED" if gate == "PASS" else "C8_TARGET_SHAPE_REFERENCE_BASIS_FAIL",
                "edge": "freeze as reviewed reference only",
                "to": "C8_TARGET_SHAPE_FROZEN_AS_REVIEWED_REFERENCE_DECISION_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C8_TARGET_SHAPE_REFERENCE_FREEZE_GATE_FAIL",
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
        "schema_version": "c8_target_shape_reviewed_reference_receipt_v0",
        "receipt_type": "TYPED_C8_TARGET_SHAPE_REVIEWED_REFERENCE_RECEIPT",
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
        "source_c8_target_shape_receipt_id": SOURCE_C8_TARGET_SHAPE_RECEIPT_ID,
        "source_post_decision_receipt_id": SOURCE_POST_DECISION_RECEIPT_ID,
        "source_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_REFERENCE_CLOSURE_RECEIPT_ID,
        "source_sidecar_closure_receipt_id": SOURCE_SIDECAR_CLOSURE_RECEIPT_ID,
        "acceptance_gate_results": {
            "C8_TARGET_SHAPE_FREEZE_0_TARGET_SHAPE_RECEIPT_CONSUMED": gate == "PASS",
            "C8_TARGET_SHAPE_FREEZE_1_TARGET_SHAPE_ARTIFACTS_CONSUMED": gate == "PASS",
            "C8_TARGET_SHAPE_FREEZE_2_SCHEMA_VALIDATOR_REFERENCE_CONSUMED": gate == "PASS",
            "C8_TARGET_SHAPE_FREEZE_3_SIDECAR_REFERENCE_CONSUMED": gate == "PASS",
            "C8_TARGET_SHAPE_FREEZE_4_PRE_C8_INTERLOCK_PAIR_CONFIRMED": gate == "PASS",
            "C8_TARGET_SHAPE_FREEZE_5_REVIEWED_REFERENCE_EMITTED": gate == "PASS",
            "C8_TARGET_SHAPE_FREEZE_6_FREEZE_MANIFEST_EMITTED": gate == "PASS",
            "C8_TARGET_SHAPE_FREEZE_7_NO_RUNTIME_ADOPTION": gate == "PASS",
            "C8_TARGET_SHAPE_FREEZE_8_NO_EXECUTION_OR_AUTHORIZATION": gate == "PASS",
            "C8_TARGET_SHAPE_FREEZE_9_NO_SCHEMA_OR_REFERENCE_MUTATION": gate == "PASS",
            "C8_TARGET_SHAPE_FREEZE_10_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_c8_target_shape_reference_summary": {
            "status": status,
            "c8_target_shape_reference_frozen": gate == "PASS",
            "source_c8_target_shape_receipt_consumed": gate == "PASS",
            "schema_validator_reference_consumed": gate == "PASS",
            "runtime_observability_sidecar_reference_consumed": gate == "PASS",
            "pre_c8_interlock_pair_complete": gate == "PASS",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "component_count": rollup["component_count"],
            "minimum_shape_field_count": rollup["minimum_shape_field_count"],
            "load_bearing_edge_field_count": rollup["load_bearing_edge_field_count"],
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
            "stop_code": None if gate == "PASS" else "STOP_C8_TARGET_SHAPE_REFERENCE_FREEZE_GATE_FAIL",
        },
    }

    receipt_id = sig8(receipt_body)
    receipt_body["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_body["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_body)

    print(json.dumps(receipt_body, indent=2, sort_keys=True))
    print(f"c8_target_shape_reference_receipt_id={receipt_id}")
    print(f"c8_target_shape_reference_receipt_path={rel(receipt_path)}")
    print(f"c8_target_shape_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"c8_target_shape_reference_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
