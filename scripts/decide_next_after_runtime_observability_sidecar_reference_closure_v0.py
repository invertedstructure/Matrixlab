#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "runtime.observability_sidecar.post_reference_closure_decision.v0"
NEXT_UNIT_ID = "PREPARE_C8_TARGET_SHAPE_FROM_PRE_C8_INTERLOCK_PAIR_V0"

LAYER = "RUNTIME / DECISION / POST_REFERENCE_CLOSURE"
MODE = "DECIDE_ONLY / NAME_NEXT_TYPED_UNIT / NO_C8_RUNTIME_AUTHORIZATION"
BUILD_MODE = "POST_SIDECAR_REFERENCE_DECISION_ONLY"

SOURCE_CLOSURE_RECEIPT_ID = "bee348a1"
SOURCE_SCHEMA_VALIDATOR_RECEIPT_ID = "732016f0"

CLOSURE_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0_receipts/bee348a1.json"
REVIEWED_REFERENCE_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/runtime_observability_sidecar_reviewed_reference_v0.json"
PRE_C8_INTERLOCK_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/pre_c8_interlock_completion_reference_v0.json"
POST_DECISION_READY_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/post_runtime_observability_sidecar_reference_decision_ready_v0.json"
CLOSURE_ROLLUP_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/runtime_observability_sidecar_reference_closure_rollup_v0.json"
CLOSURE_PROFILE_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/runtime_observability_sidecar_reference_closure_profile_v0.json"

SCHEMA_VALIDATOR_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0_receipts/732016f0.json"
SCHEMA_VALIDATOR_REFERENCE_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0/runtime_schema_validator_reviewed_reference_v0.json"

OUT_DIR = ROOT / "data/post_runtime_observability_sidecar_reference_decision_v0"
RECEIPT_DIR = ROOT / "data/post_runtime_observability_sidecar_reference_decision_v0_receipts"

BASIS_PATH = OUT_DIR / "post_sidecar_reference_decision_basis_v0.json"
DECISION_PATH = OUT_DIR / "post_sidecar_reference_decision_v0.json"
BOUNDARY_PATH = OUT_DIR / "post_sidecar_reference_decision_boundary_v0.json"
NEXT_UNIT_PATH = OUT_DIR / "post_sidecar_reference_next_unit_v0.json"
ROLLUP_PATH = OUT_DIR / "post_sidecar_reference_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "post_sidecar_reference_decision_profile_v0.json"
TRACE_PATH = OUT_DIR / "post_sidecar_reference_decision_transition_trace.json"

EXPECTED_STATUS = "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_RECOMMENDED_NEXT = UNIT_ID

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

def require_true(summary: Dict[str, Any], key: str, failures: List[str]) -> None:
    if summary.get(key) is not True:
        failures.append(f"required_true_missing:{key}:{summary.get(key)}")

def require_false(summary: Dict[str, Any], key: str, failures: List[str]) -> None:
    if summary.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{summary.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        CLOSURE_RECEIPT_PATH,
        REVIEWED_REFERENCE_PATH,
        PRE_C8_INTERLOCK_PATH,
        POST_DECISION_READY_PATH,
        CLOSURE_ROLLUP_PATH,
        CLOSURE_PROFILE_PATH,
        SCHEMA_VALIDATOR_RECEIPT_PATH,
        SCHEMA_VALIDATOR_REFERENCE_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    closure_receipt = read_json(CLOSURE_RECEIPT_PATH)
    reviewed_reference = read_json(REVIEWED_REFERENCE_PATH)
    interlock = read_json(PRE_C8_INTERLOCK_PATH)
    post_ready = read_json(POST_DECISION_READY_PATH)
    closure_rollup = read_json(CLOSURE_ROLLUP_PATH)
    closure_profile = read_json(CLOSURE_PROFILE_PATH)
    schema_validator_receipt = read_json(SCHEMA_VALIDATOR_RECEIPT_PATH)
    schema_validator_reference = read_json(SCHEMA_VALIDATOR_REFERENCE_PATH)

    summary = closure_receipt.get("machine_readable_runtime_observability_sidecar_reference_closure_summary", {})

    if closure_receipt.get("receipt_id") != SOURCE_CLOSURE_RECEIPT_ID:
        failures.append(f"closure_receipt_id_wrong:{closure_receipt.get('receipt_id')}")
    if closure_receipt.get("gate") != "PASS":
        failures.append(f"closure_receipt_gate_wrong:{closure_receipt.get('gate')}")
    if summary.get("status") != EXPECTED_STATUS:
        failures.append(f"closure_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_RECOMMENDED_NEXT:
        failures.append(f"recommended_next_wrong:{summary.get('recommended_next')}")
    if closure_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("closure_receipt_hidden_next_command")

    for key in [
        "runtime_observability_sidecar_closed_as_reviewed_reference",
        "reviewed_reference_frozen",
        "pre_c8_interlock_pair_complete",
        "post_sidecar_reference_decision_ready",
        "schema_validator_reference_consumed",
        "decision_edge_observability_reference_consumed",
        "hook_registry_reference_frozen",
        "event_record_reference_frozen",
        "append_only_trace_reference_frozen",
        "unknown_hook_gap_reference_frozen",
        "forbidden_control_reference_frozen",
        "load_bearing_field_reference_frozen",
        "negative_control_reference_frozen",
        "bad_counters_zero",
    ]:
        require_true(summary, key, failures)

    for key in [
        "live_runtime_hooks_installed",
        "live_runtime_routing_installed",
        "runtime_effect",
        "runtime_patched",
        "validation_verdict_emitted",
        "authority_checked",
        "admissibility_checked",
        "authorization_verdict_emitted",
        "execution_claimed",
        "execution_command_emitted",
        "schema_archive_mutated",
        "proposal_repaired",
        "schema_created",
        "builder_command_emitted",
        "control_path_blocked",
        "control_path_advanced",
        "c7_authorized",
        "c8_authorized",
        "new_domain_shift_executed",
        "general_cell1_authority_claimed",
        "global_autonomy_claimed",
        "full_transfer_claimed",
        "runtime_wide_enforcement_claimed",
        "source_mutated",
        "prior_receipt_mutated",
        "schema_validator_reference_mutated",
        "observability_reference_mutated",
        "sidecar_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        require_false(summary, key, failures)

    if reviewed_reference.get("reference_status") != "RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"reviewed_reference_status_wrong:{reviewed_reference.get('reference_status')}")
    if reviewed_reference.get("authority_law") != "The sidecar has eyes, not hands.":
        failures.append("sidecar_authority_law_wrong")
    if reviewed_reference.get("core_compression") != "Control path acts. Sidecar records.":
        failures.append("sidecar_core_compression_wrong")

    if interlock.get("completion_status") != "PRE_C8_INTERLOCK_PAIR_COMPLETE":
        failures.append(f"interlock_status_wrong:{interlock.get('completion_status')}")
    if interlock.get("does_not_authorize_c8_by_itself") is not True:
        failures.append("interlock_c8_boundary_missing_or_wrong")

    if post_ready.get("decision_ready") is not True:
        failures.append(f"post_decision_ready_wrong:{post_ready.get('decision_ready')}")
    if post_ready.get("recommended_next") != UNIT_ID:
        failures.append(f"post_decision_ready_next_wrong:{post_ready.get('recommended_next')}")

    if closure_profile.get("next_command_goal") is not None:
        failures.append("closure_profile_hidden_next")
    if closure_profile.get("c8_authorized") is not False:
        failures.append("closure_profile_c8_authorized_true")

    if schema_validator_receipt.get("receipt_id") != SOURCE_SCHEMA_VALIDATOR_RECEIPT_ID:
        failures.append(f"schema_validator_receipt_id_wrong:{schema_validator_receipt.get('receipt_id')}")
    if schema_validator_receipt.get("gate") != "PASS":
        failures.append(f"schema_validator_gate_wrong:{schema_validator_receipt.get('gate')}")
    if schema_validator_reference.get("reference_status") not in {
        "RUNTIME_SCHEMA_VALIDATOR_REVIEWED_REFERENCE_FROZEN",
        "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_FROZEN",
        "SCHEMA_VALIDATOR_REVIEWED_REFERENCE_FROZEN",
        "REVIEWED_REFERENCE_FROZEN",
    }:
        failures.append(f"schema_validator_reference_status_unrecognized:{schema_validator_reference.get('reference_status')}")

    forbidden_rollup_keys = [
        "live_runtime_hooks_installed_count",
        "live_runtime_routing_installed_count",
        "runtime_patch_count",
        "validation_verdict_count",
        "authority_checked_count",
        "admissibility_checked_count",
        "authorization_verdict_count",
        "execution_claim_count",
        "execution_command_count",
        "schema_archive_mutation_count",
        "proposal_repair_count",
        "schema_created_count",
        "builder_command_emitted_count",
        "control_path_blocked_count",
        "control_path_advanced_count",
        "c7_authorized_count",
        "c8_authorized_count",
        "runtime_wide_enforcement_claim_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]
    for key in forbidden_rollup_keys:
        if closure_rollup.get(key, 0) != 0:
            failures.append(f"closure_rollup_forbidden_nonzero:{key}:{closure_rollup.get(key)}")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_POST_SIDECAR_REFERENCE_DECISION_READY_C8_TARGET_SHAPE_NEXT" if gate == "PASS" else "TYPED_POST_SIDECAR_REFERENCE_DECISION_GATE_FAIL"

    source_hash_manifest = {rel(p): file_sha256(p) for p in required}

    acceptance_gate_results = {
        "POST_SIDECAR_DECISION_0_CLOSURE_RECEIPT_CONSUMED": gate == "PASS",
        "POST_SIDECAR_DECISION_1_SCHEMA_VALIDATOR_REFERENCE_PRESENT": gate == "PASS",
        "POST_SIDECAR_DECISION_2_SIDECAR_REFERENCE_FROZEN": gate == "PASS",
        "POST_SIDECAR_DECISION_3_PRE_C8_INTERLOCK_PAIR_COMPLETE": gate == "PASS",
        "POST_SIDECAR_DECISION_4_POST_DECISION_READY_CONSUMED": gate == "PASS",
        "POST_SIDECAR_DECISION_5_NO_LIVE_HOOKS_OR_RUNTIME_PATCH": gate == "PASS",
        "POST_SIDECAR_DECISION_6_NO_VALIDATION_ADMISSIBILITY_AUTHORIZATION_OR_EXECUTION": gate == "PASS",
        "POST_SIDECAR_DECISION_7_NO_C8_RUNTIME_AUTHORIZATION": gate == "PASS",
        "POST_SIDECAR_DECISION_8_NEXT_UNIT_TYPED_AS_C8_TARGET_SHAPE_PREP_ONLY": gate == "PASS",
        "POST_SIDECAR_DECISION_9_NO_SOURCE_REFERENCE_OR_SCHEMA_MUTATION": gate == "PASS",
        "POST_SIDECAR_DECISION_10_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
    }

    reason_codes = [
        "POST_SIDECAR_REFERENCE_DECISION_READY",
        "RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CLOSURE_CONSUMED",
        "SCHEMA_VALIDATOR_REFERENCE_CLOSURE_CONSUMED",
        "PRE_C8_INTERLOCK_PAIR_COMPLETE",
        "C8_TARGET_SHAPE_PREP_IS_NEXT_TYPED_UNIT",
        "C8_RUNTIME_AUTHORIZATION_NOT_GRANTED",
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
        "schema_version": "post_sidecar_reference_decision_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "source_schema_validator_receipt_id": SOURCE_SCHEMA_VALIDATOR_RECEIPT_ID,
        "source_files": source_hash_manifest,
        "consumed_status": summary.get("status"),
        "consumed_recommended_next": summary.get("recommended_next"),
        "pre_c8_interlock_pair_complete": summary.get("pre_c8_interlock_pair_complete"),
        "post_sidecar_reference_decision_ready": summary.get("post_sidecar_reference_decision_ready"),
        "decision_scope": "name the next typed unit after sidecar reference closure",
        "decision_does_not_mean": [
            "C8 runtime is authorized",
            "C8 execution is authorized",
            "runtime hooks may be installed",
            "runtime may be patched",
            "Sidecar gains validation authority",
            "Sidecar gains admissibility authority",
            "Sidecar gains authorization authority",
            "Sidecar gains execution authority",
            "schema archive may be mutated",
            "source references may be mutated",
        ],
    }

    decision = {
        "schema_version": "post_sidecar_reference_decision_v0",
        "decision_status": status,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "selected_next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "selected_next_unit_kind": "C8_TARGET_SHAPE_TYPING_ONLY" if gate == "PASS" else None,
        "selected_next_unit_law": "prepare the C8 target shape from the already frozen pre-C8 interlock pair without authorizing C8 runtime adoption",
        "c8_target_shape_typing_next": gate == "PASS",
        "c8_runtime_authorized": False,
        "c8_execution_authorized": False,
        "runtime_adoption_authorized": False,
        "live_hooks_authorized": False,
        "runtime_patch_authorized": False,
        "schema_mutation_authorized": False,
        "control_path_authority_granted": False,
        "reason_codes": reason_codes,
    }

    boundary = {
        "schema_version": "post_sidecar_reference_decision_boundary_v0",
        "boundary_status": "BOUNDARY_HELD" if gate == "PASS" else "BOUNDARY_FAIL",
        "allowed": [
            "consume frozen Schema Validator reviewed reference",
            "consume frozen Runtime Observability Sidecar reviewed reference",
            "consume pre-C8 interlock completion marker",
            "name next typed unit for C8 target-shape preparation",
            "emit decision receipt",
        ],
        "forbidden": [
            "install live runtime hooks",
            "patch runtime",
            "route runtime traffic",
            "validate proposals",
            "admit proposals",
            "authorize proposals",
            "execute proposals",
            "mutate schema archive",
            "repair proposals",
            "advance control path by sidecar authority",
            "authorize C8 runtime adoption",
            "emit hidden next command",
        ],
    }

    next_unit = {
        "schema_version": "post_sidecar_reference_next_unit_v0",
        "next_unit_id": NEXT_UNIT_ID,
        "layer": "RUNTIME / C8 / TARGET_SHAPE",
        "mode": "TYPE_ONLY / TARGET_PREP / NO_RUNTIME_ADOPTION",
        "active_object": "C8 basic target shape from frozen Schema Validator reference and frozen Runtime Observability Sidecar reference",
        "allowed_inputs": [
            rel(SCHEMA_VALIDATOR_REFERENCE_PATH),
            rel(REVIEWED_REFERENCE_PATH),
            rel(PRE_C8_INTERLOCK_PATH),
            rel(CLOSURE_RECEIPT_PATH),
        ],
        "forbidden_inputs": [
            "live runtime state",
            "latest-file guessing",
            "mtime selection",
            "ambient workspace inference",
            "unregistered source material",
            "schema mutation",
            "runtime patch",
            "C8 execution authority",
        ],
        "action": "type the smallest C8 target shape made lawful by the completed pre-C8 interlock pair",
        "acceptance_gate": "target shape names role, boundary, inputs, forbidden claims, and stop/advance surface without runtime adoption",
        "artifact_target": "c8.target_shape.from_pre_c8_interlock_pair.v0",
        "on_pass": {
            "type": "ADVANCE",
            "next_unit_id": "BUILD_OR_FREEZE_C8_TARGET_SHAPE_V0",
        },
        "must_not_impersonate": [
            "C8 execution",
            "runtime adoption",
            "authorization verdict",
            "schema archive mutation",
            "control path authority",
        ],
    }

    rollup = {
        "schema_version": "post_sidecar_reference_decision_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "source_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "pre_c8_interlock_pair_complete": summary.get("pre_c8_interlock_pair_complete") is True,
        "sidecar_reference_frozen": summary.get("reviewed_reference_frozen") is True,
        "schema_validator_reference_consumed": summary.get("schema_validator_reference_consumed") is True,
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "c8_target_shape_typing_next": gate == "PASS",
        "c8_runtime_authorized": False,
        "runtime_patch_authorized": False,
        "live_hooks_authorized": False,
        "control_path_authority_granted": False,
        "schema_mutation_authorized": False,
        "hidden_next_command": False,
    }

    profile = {
        "schema_version": "post_sidecar_reference_decision_profile_v0",
        "profile_status": status,
        "decision_profile": "PRE_C8_INTERLOCK_COMPLETE_TO_C8_TARGET_SHAPE_TYPING",
        "what_changed": "The post-sidecar decision consumed the frozen sidecar closure and names the next typed unit.",
        "what_did_not_change": [
            "C8 is not runtime-authorized",
            "runtime is not patched",
            "sidecar remains eyes-not-hands",
            "schema validator remains reviewed reference only",
            "no control path authority is granted",
        ],
        "next_command_goal": None,
    }

    trace = {
        "schema_version": "post_sidecar_reference_decision_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_CLOSURE_DECISION_READY",
                "edge": "consume reviewed reference closure receipt",
                "to": "POST_SIDECAR_DECISION_BASIS_ACCEPTED" if gate == "PASS" else "POST_SIDECAR_DECISION_BASIS_FAIL",
            },
            {
                "from": "POST_SIDECAR_DECISION_BASIS_ACCEPTED" if gate == "PASS" else "POST_SIDECAR_DECISION_BASIS_FAIL",
                "edge": "verify pre-C8 interlock pair and no-authority boundary",
                "to": "C8_TARGET_SHAPE_NEXT_TYPED_UNIT_NAMED" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_POST_SIDECAR_REFERENCE_DECISION_GATE_FAIL",
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
        "schema_version": "post_sidecar_reference_decision_receipt_v0",
        "receipt_type": "TYPED_POST_SIDECAR_REFERENCE_DECISION_RECEIPT",
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
        "source_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "source_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_RECEIPT_ID,
        "acceptance_gate_results": acceptance_gate_results,
        "machine_readable_post_sidecar_reference_decision_summary": {
            "status": status,
            "post_sidecar_reference_decision_done": gate == "PASS",
            "source_closure_receipt_consumed": gate == "PASS",
            "schema_validator_reference_consumed": gate == "PASS",
            "runtime_observability_sidecar_reference_consumed": gate == "PASS",
            "pre_c8_interlock_pair_complete": gate == "PASS",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "c8_target_shape_typing_next": gate == "PASS",
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
            "stop_code": None if gate == "PASS" else "STOP_POST_SIDECAR_REFERENCE_DECISION_GATE_FAIL",
        },
    }

    receipt_id = sig8(receipt_body)
    receipt_body["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_body["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_body)

    print(json.dumps(receipt_body, indent=2, sort_keys=True))
    print(f"post_sidecar_reference_decision_receipt_id={receipt_id}")
    print(f"post_sidecar_reference_decision_receipt_path={rel(receipt_path)}")
    print(f"post_sidecar_reference_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
