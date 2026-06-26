#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_C8_TARGET_SHAPE_REFERENCE_FREEZE_V0"
TARGET_UNIT_ID = "c8.target_shape.post_reference_freeze_decision.v0"
NEXT_UNIT_ID = "PREPARE_C8_BASIC_INTERLOCK_MECHANIC_FROM_TARGET_SHAPE_REFERENCE_V0"

LAYER = "RUNTIME / C8 / DECISION / POST_TARGET_SHAPE_REFERENCE"
MODE = "DECIDE_ONLY / NAME_NEXT_TYPED_UNIT / NO_RUNTIME_ADOPTION"
BUILD_MODE = "POST_C8_TARGET_SHAPE_REFERENCE_DECISION_ONLY"

SOURCE_C8_REFERENCE_RECEIPT_ID = "ea23fd9b"
SOURCE_C8_TARGET_SHAPE_PREP_RECEIPT_ID = "ec404930"
SOURCE_POST_SIDECAR_DECISION_RECEIPT_ID = "62ddebf9"

C8_REFERENCE_RECEIPT_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0_receipts/ea23fd9b.json"
C8_REVIEWED_REFERENCE_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0/c8_target_shape_reviewed_reference_v0.json"
C8_REFERENCE_BASIS_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0/c8_target_shape_reference_freeze_basis_v0.json"
C8_REFERENCE_BOUNDARY_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0/c8_target_shape_reference_boundary_v0.json"
C8_REFERENCE_NON_AUTHORIZATION_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0/c8_target_shape_reference_non_authorization_v0.json"
C8_REFERENCE_ROLLUP_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0/c8_target_shape_reference_rollup_v0.json"
C8_REFERENCE_PROFILE_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0/c8_target_shape_reference_profile_v0.json"
C8_REFERENCE_DECISION_READY_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0/post_c8_target_shape_reference_decision_ready_v0.json"

C8_TARGET_SHAPE_PREP_RECEIPT_PATH = ROOT / "data/c8_target_shape_from_pre_c8_interlock_pair_v0_receipts/ec404930.json"
POST_SIDECAR_DECISION_RECEIPT_PATH = ROOT / "data/post_runtime_observability_sidecar_reference_decision_v0_receipts/62ddebf9.json"
SCHEMA_VALIDATOR_REFERENCE_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0/runtime_schema_validator_reviewed_reference_v0.json"
SIDECAR_REVIEWED_REFERENCE_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/runtime_observability_sidecar_reviewed_reference_v0.json"

OUT_DIR = ROOT / "data/post_c8_target_shape_reference_decision_v0"
RECEIPT_DIR = ROOT / "data/post_c8_target_shape_reference_decision_v0_receipts"

BASIS_PATH = OUT_DIR / "post_c8_target_shape_reference_decision_basis_v0.json"
DECISION_PATH = OUT_DIR / "post_c8_target_shape_reference_decision_v0.json"
BOUNDARY_PATH = OUT_DIR / "post_c8_target_shape_reference_decision_boundary_v0.json"
NEXT_UNIT_PATH = OUT_DIR / "post_c8_target_shape_reference_next_unit_v0.json"
ROLLUP_PATH = OUT_DIR / "post_c8_target_shape_reference_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "post_c8_target_shape_reference_decision_profile_v0.json"
TRACE_PATH = OUT_DIR / "post_c8_target_shape_reference_decision_transition_trace.json"

EXPECTED_REFERENCE_STATUS = "TYPED_C8_TARGET_SHAPE_FROZEN_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_REFERENCE_NEXT = UNIT_ID

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
        C8_REFERENCE_RECEIPT_PATH,
        C8_REVIEWED_REFERENCE_PATH,
        C8_REFERENCE_BASIS_PATH,
        C8_REFERENCE_BOUNDARY_PATH,
        C8_REFERENCE_NON_AUTHORIZATION_PATH,
        C8_REFERENCE_ROLLUP_PATH,
        C8_REFERENCE_PROFILE_PATH,
        C8_REFERENCE_DECISION_READY_PATH,
        C8_TARGET_SHAPE_PREP_RECEIPT_PATH,
        POST_SIDECAR_DECISION_RECEIPT_PATH,
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

    c8_receipt = read_json(C8_REFERENCE_RECEIPT_PATH)
    c8_reference = read_json(C8_REVIEWED_REFERENCE_PATH)
    c8_basis = read_json(C8_REFERENCE_BASIS_PATH)
    c8_boundary = read_json(C8_REFERENCE_BOUNDARY_PATH)
    c8_non_authorization = read_json(C8_REFERENCE_NON_AUTHORIZATION_PATH)
    c8_rollup = read_json(C8_REFERENCE_ROLLUP_PATH)
    c8_profile = read_json(C8_REFERENCE_PROFILE_PATH)
    c8_decision_ready = read_json(C8_REFERENCE_DECISION_READY_PATH)

    c8_prep_receipt = read_json(C8_TARGET_SHAPE_PREP_RECEIPT_PATH)
    post_sidecar_receipt = read_json(POST_SIDECAR_DECISION_RECEIPT_PATH)
    schema_validator_reference = read_json(SCHEMA_VALIDATOR_REFERENCE_PATH)
    sidecar_reference = read_json(SIDECAR_REVIEWED_REFERENCE_PATH)

    c8_summary = c8_receipt.get("machine_readable_c8_target_shape_reference_summary", {})

    if c8_receipt.get("receipt_id") != SOURCE_C8_REFERENCE_RECEIPT_ID:
        failures.append(f"c8_reference_receipt_id_wrong:{c8_receipt.get('receipt_id')}")
    if c8_receipt.get("gate") != "PASS":
        failures.append(f"c8_reference_receipt_gate_wrong:{c8_receipt.get('gate')}")
    if c8_summary.get("status") != EXPECTED_REFERENCE_STATUS:
        failures.append(f"c8_reference_status_wrong:{c8_summary.get('status')}")
    if c8_summary.get("c8_target_shape_reference_frozen") is not True:
        failures.append("c8_reference_not_frozen")
    if c8_summary.get("next_unit_id") != UNIT_ID:
        failures.append(f"c8_reference_next_unit_wrong:{c8_summary.get('next_unit_id')}")
    if c8_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("c8_reference_terminal_not_advance")
    if c8_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("c8_reference_terminal_next_wrong")

    if c8_reference.get("reference_status") != "C8_TARGET_SHAPE_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"reviewed_reference_status_wrong:{c8_reference.get('reference_status')}")
    if c8_reference.get("reference_only") is not True:
        failures.append("reviewed_reference_not_reference_only")
    if c8_basis.get("basis_status") != "BASIS_ACCEPTED":
        failures.append(f"basis_status_wrong:{c8_basis.get('basis_status')}")
    if c8_boundary.get("boundary_status") != "BOUNDARY_HELD":
        failures.append(f"boundary_status_wrong:{c8_boundary.get('boundary_status')}")
    if c8_rollup.get("c8_target_shape_reference_frozen") is not True:
        failures.append("rollup_reference_not_frozen")
    if c8_profile.get("recommended_next") != UNIT_ID:
        failures.append(f"profile_recommended_next_wrong:{c8_profile.get('recommended_next')}")
    if c8_profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if c8_decision_ready.get("decision_ready") is not True:
        failures.append("post_freeze_decision_not_ready")
    if c8_decision_ready.get("recommended_next") != UNIT_ID:
        failures.append(f"post_freeze_decision_next_wrong:{c8_decision_ready.get('recommended_next')}")

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
        if key in c8_reference:
            require_false(c8_reference, key, failures)

    if c8_prep_receipt.get("receipt_id") != SOURCE_C8_TARGET_SHAPE_PREP_RECEIPT_ID:
        failures.append(f"c8_prep_receipt_id_wrong:{c8_prep_receipt.get('receipt_id')}")
    if c8_prep_receipt.get("gate") != "PASS":
        failures.append("c8_prep_receipt_gate_not_pass")
    if post_sidecar_receipt.get("receipt_id") != SOURCE_POST_SIDECAR_DECISION_RECEIPT_ID:
        failures.append(f"post_sidecar_receipt_id_wrong:{post_sidecar_receipt.get('receipt_id')}")
    if post_sidecar_receipt.get("gate") != "PASS":
        failures.append("post_sidecar_receipt_gate_not_pass")
    if schema_validator_reference.get("reference_status") != "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"schema_validator_reference_status_wrong:{schema_validator_reference.get('reference_status')}")
    if sidecar_reference.get("reference_status") != "RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"sidecar_reference_status_wrong:{sidecar_reference.get('reference_status')}")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_POST_C8_TARGET_SHAPE_REFERENCE_DECISION_READY_BASIC_INTERLOCK_NEXT" if gate == "PASS" else "TYPED_POST_C8_TARGET_SHAPE_REFERENCE_DECISION_GATE_FAIL"

    source_hash_manifest = {rel(p): file_sha256(p) for p in required}

    reason_codes = [
        "POST_C8_TARGET_SHAPE_REFERENCE_DECISION_READY",
        "C8_TARGET_SHAPE_REVIEWED_REFERENCE_CONSUMED",
        "C8_TARGET_SHAPE_PREP_RECEIPT_CONSUMED",
        "POST_SIDECAR_DECISION_RECEIPT_CONSUMED",
        "SCHEMA_VALIDATOR_REFERENCE_CONSUMED",
        "RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CONSUMED",
        "BASIC_INTERLOCK_MECHANIC_IS_NEXT_TYPED_UNIT",
        "TYPE_ONLY_NEXT_UNIT",
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
        "schema_version": "post_c8_target_shape_reference_decision_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_c8_target_shape_reference_receipt_id": SOURCE_C8_REFERENCE_RECEIPT_ID,
        "source_c8_target_shape_prep_receipt_id": SOURCE_C8_TARGET_SHAPE_PREP_RECEIPT_ID,
        "source_post_sidecar_decision_receipt_id": SOURCE_POST_SIDECAR_DECISION_RECEIPT_ID,
        "source_files": source_hash_manifest,
        "decision_scope": "name the next typed unit after the C8 target shape reviewed reference freeze",
        "decision_does_not_authorize": [
            "C8 runtime adoption",
            "C8 execution",
            "live runtime hooks",
            "runtime patching",
            "runtime routing",
            "validation verdicts",
            "admissibility verdicts",
            "authorization verdicts",
            "schema archive mutation",
            "control path authority",
        ],
    }

    decision = {
        "schema_version": "post_c8_target_shape_reference_decision_v0",
        "decision_status": status,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_c8_target_shape_reference_receipt_id": SOURCE_C8_REFERENCE_RECEIPT_ID,
        "selected_next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "selected_next_unit_kind": "C8_BASIC_INTERLOCK_MECHANIC_TYPING_ONLY" if gate == "PASS" else None,
        "selected_next_unit_law": "prepare the smallest C8 basic interlock mechanic from the frozen target-shape reference without runtime adoption",
        "basic_interlock_mechanic_typing_next": gate == "PASS",
        "c8_runtime_authorized": False,
        "c8_execution_authorized": False,
        "runtime_adoption_authorized": False,
        "live_hooks_authorized": False,
        "runtime_patch_authorized": False,
        "runtime_routing_authorized": False,
        "validation_authority_granted": False,
        "admissibility_authority_granted": False,
        "authorization_authority_granted": False,
        "control_path_authority_granted": False,
        "schema_mutation_authorized": False,
        "reason_codes": reason_codes,
    }

    boundary = {
        "schema_version": "post_c8_target_shape_reference_decision_boundary_v0",
        "boundary_status": "BOUNDARY_HELD" if gate == "PASS" else "BOUNDARY_FAIL",
        "allowed": [
            "consume C8 target-shape reviewed reference",
            "consume target-shape freeze receipt",
            "name next typed unit",
            "emit post-freeze decision receipt",
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

    next_unit = {
        "schema_version": "post_c8_target_shape_reference_next_unit_v0",
        "next_unit_id": NEXT_UNIT_ID,
        "layer": "RUNTIME / C8 / BASIC_INTERLOCK_MECHANIC",
        "mode": "TYPE_ONLY / MECHANIC_PREP / NO_RUNTIME_ADOPTION",
        "active_object": "C8 basic interlock mechanic derived from frozen C8 target-shape reference",
        "allowed_inputs": [
            rel(C8_REVIEWED_REFERENCE_PATH),
            rel(C8_REFERENCE_RECEIPT_PATH),
            rel(SCHEMA_VALIDATOR_REFERENCE_PATH),
            rel(SIDECAR_REVIEWED_REFERENCE_PATH),
        ],
        "forbidden_inputs": [
            "live runtime state",
            "runtime patch",
            "runtime routing",
            "C8 execution authority",
            "schema archive mutation",
            "ambient workspace inference",
            "latest-file guessing",
            "mtime selection",
            "unregistered source material",
        ],
        "action": "type the smallest C8 basic interlock mechanic connecting proposal/reference, schema-validator boundary, sidecar observation surface, and control-path boundary",
        "acceptance_gate": "mechanic names components, one-step flow, stop/advance surface, blocked claims, and non-authorization boundary without runtime adoption",
        "artifact_target": "c8.basic_interlock_mechanic.from_target_shape_reference.v0",
        "on_pass": {
            "type": "ADVANCE",
            "next_unit_id": "BUILD_OR_FREEZE_C8_BASIC_INTERLOCK_MECHANIC_V0",
        },
        "must_not_impersonate": [
            "C8 runtime adoption",
            "C8 execution engine",
            "live admissibility service",
            "authorization verdict",
            "schema mutation",
            "control path authority",
        ],
    }

    rollup = {
        "schema_version": "post_c8_target_shape_reference_decision_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "source_c8_target_shape_reference_receipt_id": SOURCE_C8_REFERENCE_RECEIPT_ID,
        "c8_target_shape_reference_consumed": gate == "PASS",
        "basic_interlock_mechanic_typing_next": gate == "PASS",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "c8_runtime_authorized": False,
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "control_path_authority_granted": False,
        "hidden_next_command": False,
    }

    profile = {
        "schema_version": "post_c8_target_shape_reference_decision_profile_v0",
        "profile_status": status,
        "profile": "C8_TARGET_SHAPE_REFERENCE_TO_BASIC_INTERLOCK_MECHANIC",
        "what_changed": "The frozen C8 target shape reference now names the next typed unit: the C8 basic interlock mechanic.",
        "what_did_not_change": [
            "C8 is not runtime-authorized",
            "C8 is not executed",
            "runtime is not patched",
            "live hooks are not installed",
            "schema archive is not mutated",
            "control path authority is not granted",
            "admissibility/authorization verdicts are not emitted",
        ],
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_POST_C8_TARGET_SHAPE_REFERENCE_DECISION_V0",
        "next_command_goal": None,
    }

    trace = {
        "schema_version": "post_c8_target_shape_reference_decision_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "C8_TARGET_SHAPE_FROZEN_AS_REVIEWED_REFERENCE_DECISION_READY",
                "edge": "consume C8 target-shape reviewed reference",
                "to": "POST_C8_TARGET_SHAPE_REFERENCE_DECISION_BASIS_ACCEPTED" if gate == "PASS" else "POST_C8_TARGET_SHAPE_REFERENCE_DECISION_BASIS_FAIL",
            },
            {
                "from": "POST_C8_TARGET_SHAPE_REFERENCE_DECISION_BASIS_ACCEPTED" if gate == "PASS" else "POST_C8_TARGET_SHAPE_REFERENCE_DECISION_BASIS_FAIL",
                "edge": "name next typed basic interlock mechanic unit",
                "to": "C8_BASIC_INTERLOCK_MECHANIC_NEXT_TYPED_UNIT_NAMED" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_POST_C8_TARGET_SHAPE_REFERENCE_DECISION_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (DECISION_PATH, decision),
        (BOUNDARY_PATH, boundary),
        (NEXT_UNIT_PATH, next_unit),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_PATH, trace),
    ]:
        write_json(path, obj)

    receipt_body = {
        "schema_version": "post_c8_target_shape_reference_decision_receipt_v0",
        "receipt_type": "TYPED_POST_C8_TARGET_SHAPE_REFERENCE_DECISION_RECEIPT",
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
        "source_c8_target_shape_reference_receipt_id": SOURCE_C8_REFERENCE_RECEIPT_ID,
        "source_c8_target_shape_prep_receipt_id": SOURCE_C8_TARGET_SHAPE_PREP_RECEIPT_ID,
        "source_post_sidecar_decision_receipt_id": SOURCE_POST_SIDECAR_DECISION_RECEIPT_ID,
        "acceptance_gate_results": {
            "POST_C8_TARGET_SHAPE_DECISION_0_REFERENCE_RECEIPT_CONSUMED": gate == "PASS",
            "POST_C8_TARGET_SHAPE_DECISION_1_REVIEWED_REFERENCE_CONSUMED": gate == "PASS",
            "POST_C8_TARGET_SHAPE_DECISION_2_DECISION_READY_MARKER_CONSUMED": gate == "PASS",
            "POST_C8_TARGET_SHAPE_DECISION_3_NO_RUNTIME_ADOPTION": gate == "PASS",
            "POST_C8_TARGET_SHAPE_DECISION_4_NO_EXECUTION_OR_AUTHORIZATION": gate == "PASS",
            "POST_C8_TARGET_SHAPE_DECISION_5_NEXT_UNIT_TYPED": gate == "PASS",
            "POST_C8_TARGET_SHAPE_DECISION_6_NO_SCHEMA_OR_REFERENCE_MUTATION": gate == "PASS",
            "POST_C8_TARGET_SHAPE_DECISION_7_NO_CONTROL_PATH_AUTHORITY": gate == "PASS",
            "POST_C8_TARGET_SHAPE_DECISION_8_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_post_c8_target_shape_reference_decision_summary": {
            "status": status,
            "post_c8_target_shape_reference_decision_done": gate == "PASS",
            "source_c8_target_shape_reference_consumed": gate == "PASS",
            "basic_interlock_mechanic_typing_next": gate == "PASS",
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
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "decision": rel(DECISION_PATH),
            "boundary": rel(BOUNDARY_PATH),
            "next_unit": rel(NEXT_UNIT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_POST_C8_TARGET_SHAPE_REFERENCE_DECISION_GATE_FAIL",
        },
    }

    receipt_id = sig8(receipt_body)
    receipt_body["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_body["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_body)

    print(json.dumps(receipt_body, indent=2, sort_keys=True))
    print(f"post_c8_target_shape_reference_decision_receipt_id={receipt_id}")
    print(f"post_c8_target_shape_reference_decision_receipt_path={rel(receipt_path)}")
    print(f"post_c8_target_shape_reference_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
