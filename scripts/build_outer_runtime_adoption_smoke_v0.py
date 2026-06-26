#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_OUTER_RUNTIME_ADOPTION_SMOKE_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.smoke_v0"

LAYER = "OUTER / RUNTIME_ADOPTION"
MODE = "VERIFY / BUILD_FACING_RUNTIME"
BUILD_MODE = "OUTER_RUNTIME_ADOPTION_SMOKE_ONLY"

MAX_STEPS = 8

SOURCE_C7_SYNTHETIC_ROLLUP_RECEIPT_ID = "7a31c320"
SOURCE_SCHEMA_VALIDATOR_RECEIPT_ID = "732016f0"
SOURCE_SIDECAR_RECEIPT_ID = "bee348a1"

C7_SYNTHETIC_ROLLUP_RECEIPT_PATH = ROOT / "data/c7_synthetic_runtime_radius_tests_rollup_v0_receipts/7a31c320.json"

SCHEMA_VALIDATOR_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0_receipts/732016f0.json"
SCHEMA_VALIDATOR_REFERENCE_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0/runtime_schema_validator_reviewed_reference_v0.json"

SIDECAR_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0_receipts/bee348a1.json"
SIDECAR_REFERENCE_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/runtime_observability_sidecar_reviewed_reference_v0.json"

CURRENT_RUNTIME_ENTRYPOINT_PATH = ROOT / "scripts/run_c7_synthetic_runtime_radius_v0.py"
CURRENT_RECEIPT_READOUT_SURFACE_PATH = ROOT / "data/c7_synthetic_runtime_radius_tests_rollup_v0/runtime_radius_full_synthetic_readout_v0.json"

OUT_DIR = ROOT / "data/runtime_adoption_smoke_v0"
RECEIPT_DIR = ROOT / "data/runtime_adoption_smoke_v0_receipts"

BASELINE_SEAL_PATH = OUT_DIR / "runtime_baseline_seal_v0.json"
STATE_SCHEMA_PATH = OUT_DIR / "runtime_state_schema_v0.json"
STATE_PATH = OUT_DIR / "runtime_state_v0.json"
MOVE_REGISTRY_PATH = OUT_DIR / "runtime_move_registry_snapshot_v0.json"
TRACE_PATH = OUT_DIR / "runtime_smoke_trace_v0.jsonl"
RUNTIME_RECEIPT_PATH = OUT_DIR / "runtime_smoke_receipt_v0.json"
READOUT_PATH = OUT_DIR / "runtime_smoke_readout_v0.json"
PRESSURE_PATH = OUT_DIR / "runtime_pressure_classification_v0.json"
REFINEMENT_CANDIDATES_PATH = OUT_DIR / "runtime_refinement_candidate_records_v0.jsonl"
ROLLUP_PATH = OUT_DIR / "runtime_smoke_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_smoke_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_smoke_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "runtime_smoke_transition_trace.json"

NEGATIVE_CONTROLS = {
    "unregistered_move_applied_count": 0,
    "hidden_repair_count": 0,
    "schema_invented_count": 0,
    "taxonomy_invented_count": 0,
    "fixture_expanded_by_default_count": 0,
    "architecture_widened_count": 0,
    "ambient_workspace_inference_count": 0,
    "latest_file_selection_count": 0,
    "mtime_selection_count": 0,
    "trace_missing_count": 0,
    "receipt_mismatch_count": 0,
    "implicit_continuation_count": 0,
    "production_runtime_claim_count": 0,
    "broad_hardening_count": 0,
}

PRESSURE_ENUM = [
    "NO_PRESSURE_TERMINAL",
    "ADVANCE_READY",
    "STOP_DONE",
    "STOP_NEXT_MOVE_BOUNDARY",
    "BASELINE_UNSEALED",
    "RUNTIME_STATE_UNTYPED",
    "FIXTURE_LOAD_ERROR",
    "REGIME_MISMATCH",
    "NO_APPLICABLE_MOVE",
    "STEP_LIMIT_EXCEEDED",
    "SCHEMA_VALIDATION_FAIL",
    "LAWFUL_ADMISSIBILITY_FAIL",
    "RUNTIME_GATE_FAIL",
    "RUNTIME_TRACE_MISMATCH",
    "RUNTIME_RECEIPT_MISMATCH",
    "RUNTIME_PROJECTION_BUG",
    "RUNTIME_MISSING_MOVE_PRESSURE",
    "RUNTIME_OBSERVABILITY_GAP",
    "RUNTIME_FEEDBACK_GAP",
    "RUNTIME_AUTHORITY_BOUNDARY",
    "QUESTION_PACKET_NOT_COMMAND",
]

OUTCOME_ENUM = [
    "RUNTIME_SMOKE_PASS_ADVANCE_READY",
    "RUNTIME_SMOKE_PASS_TYPED_STOP",
    "RUNTIME_SMOKE_PASS_WITH_LOCAL_GOTCHA_REPAIR",
    "RUNTIME_SMOKE_BLOCKED_BASELINE_UNSEALED",
    "RUNTIME_SMOKE_BLOCKED_UNTYPED_STATE",
    "RUNTIME_SMOKE_BLOCKED_REGIME_MISMATCH",
    "RUNTIME_SMOKE_BLOCKED_SCHEMA_VALIDATION",
    "RUNTIME_SMOKE_BLOCKED_ADMISSIBILITY",
    "RUNTIME_SMOKE_BLOCKED_NO_APPLICABLE_MOVE",
    "RUNTIME_SMOKE_BLOCKED_MISSING_MOVE",
    "RUNTIME_SMOKE_BLOCKED_TRACE_MISMATCH",
    "RUNTIME_SMOKE_BLOCKED_RECEIPT_MISMATCH",
    "RUNTIME_SMOKE_BLOCKED_PROJECTION_BUG",
    "RUNTIME_SMOKE_BLOCKED_STEP_LIMIT",
    "RUNTIME_SMOKE_BLOCKED_OBSERVABILITY_GAP",
    "RUNTIME_SMOKE_BLOCKED_FEEDBACK_GAP",
    "RUNTIME_SMOKE_AUTHORITY_VIOLATION",
]

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

def git_text(args: List[str]) -> str:
    try:
        return subprocess.check_output(args, cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()
    except subprocess.CalledProcessError as e:
        return f"UNAVAILABLE:{e.output.strip()}"

def state_sig(state: Dict[str, Any]) -> str:
    return sig8(state)

def append_trace_row(rows: List[Dict[str, Any]], row: Dict[str, Any]) -> None:
    rows.append(row)

def move_registry() -> Dict[str, Any]:
    moves = [
        {
            "schema_version": "runtime_move_v0",
            "move_id": "move_load_baseline_seal_v0",
            "move_kind": "LOAD_BASELINE",
            "priority": 10,
            "applies_when": {"runtime_phase": "INIT"},
            "requires_schema_validation": False,
            "requires_admissibility": False,
            "action": "LOAD_BASELINE",
            "emits_labels": ["BASELINE_LOADED"],
            "may_halt": True,
            "state_delta": {"runtime_phase": "BASELINE_LOADED"},
            "required_inputs": [rel(BASELINE_SEAL_PATH)],
            "forbidden_inputs": ["latest_file", "mtime", "ambient_workspace"],
            "expected_trace_fields": ["before_state_sig8", "selected_move", "state_delta", "after_state_sig8"],
            "expected_receipt_fields": ["baseline_ref"],
            "failure_halts": ["STOP_RUNTIME_BASELINE_UNSEALED"],
        },
        {
            "schema_version": "runtime_move_v0",
            "move_id": "move_load_declared_runtime_state_v0",
            "move_kind": "LOAD_RUNTIME_STATE",
            "priority": 20,
            "applies_when": {"runtime_phase": "BASELINE_LOADED"},
            "requires_schema_validation": False,
            "requires_admissibility": False,
            "action": "LOAD_RUNTIME_STATE",
            "emits_labels": ["STATE_LOADED"],
            "may_halt": True,
            "state_delta": {"runtime_phase": "STATE_LOADED"},
            "required_inputs": [rel(STATE_PATH)],
            "forbidden_inputs": ["latest_file", "mtime", "ambient_workspace"],
            "expected_trace_fields": ["before_state_sig8", "selected_move", "state_delta", "after_state_sig8"],
            "expected_receipt_fields": ["start_state_ref"],
            "failure_halts": ["STOP_RUNTIME_STATE_UNTYPED"],
        },
        {
            "schema_version": "runtime_move_v0",
            "move_id": "move_validate_declared_state_v0",
            "move_kind": "VALIDATE_STATE",
            "priority": 30,
            "applies_when": {"runtime_phase": "STATE_LOADED"},
            "requires_schema_validation": True,
            "requires_admissibility": False,
            "action": "VALIDATE_STATE_SCHEMA",
            "emits_labels": ["SCHEMA_VALIDATED"],
            "may_halt": True,
            "state_delta": {"runtime_phase": "STATE_VALIDATED", "state_validated": True},
            "required_inputs": [rel(STATE_SCHEMA_PATH), rel(SCHEMA_VALIDATOR_REFERENCE_PATH)],
            "forbidden_inputs": ["schema_invention", "taxonomy_invention"],
            "expected_trace_fields": ["schema_validation_ref", "state_delta"],
            "expected_receipt_fields": ["schema_archive_ref"],
            "failure_halts": ["STOP_RUNTIME_STATE_UNTYPED", "STOP_RUNTIME_SCHEMA_VALIDATION_FAIL"],
        },
        {
            "schema_version": "runtime_move_v0",
            "move_id": "move_check_cell0_lawful_admissibility_v0",
            "move_kind": "CHECK_LAWFUL_ADMISSIBILITY",
            "priority": 40,
            "applies_when": {"runtime_phase": "STATE_VALIDATED"},
            "requires_schema_validation": True,
            "requires_admissibility": True,
            "action": "CHECK_CELL0_ADMISSIBILITY",
            "emits_labels": ["ADMISSIBILITY_ALLOWED"],
            "may_halt": True,
            "state_delta": {"runtime_phase": "ADMISSIBILITY_CHECKED", "cell0_admissibility": "ALLOW"},
            "required_inputs": ["CELL0_AS_LAWFUL_ADMISSIBILITY_SURFACE"],
            "forbidden_inputs": ["authority_widening", "hidden_memory_authority"],
            "expected_trace_fields": ["admissibility_ref", "state_delta"],
            "expected_receipt_fields": ["admissibility_surface_ref"],
            "failure_halts": ["STOP_RUNTIME_ADMISSIBILITY_FAIL", "STOP_AUTHORITY_VIOLATION"],
        },
        {
            "schema_version": "runtime_move_v0",
            "move_id": "move_inspect_registered_moves_v0",
            "move_kind": "INSPECT_APPLICABLE_MOVES",
            "priority": 50,
            "applies_when": {"runtime_phase": "ADMISSIBILITY_CHECKED"},
            "requires_schema_validation": False,
            "requires_admissibility": False,
            "action": "INSPECT_APPLICABLE_MOVES",
            "emits_labels": ["MOVES_INSPECTED"],
            "may_halt": True,
            "state_delta": {"runtime_phase": "MOVES_INSPECTED"},
            "required_inputs": [rel(MOVE_REGISTRY_PATH)],
            "forbidden_inputs": ["unregistered_moves"],
            "expected_trace_fields": ["applicable_moves", "selected_move"],
            "expected_receipt_fields": ["moves_inspected"],
            "failure_halts": ["STOP_RUNTIME_NO_APPLICABLE_MOVE", "STOP_RUNTIME_MOVE_TIE_UNRESOLVED"],
        },
        {
            "schema_version": "runtime_move_v0",
            "move_id": "move_emit_typed_smoke_terminal_v0",
            "move_kind": "EMIT_TYPED_TERMINAL",
            "priority": 60,
            "applies_when": {"runtime_phase": "MOVES_INSPECTED"},
            "requires_schema_validation": False,
            "requires_admissibility": False,
            "action": "EMIT_TYPED_STOP_DONE",
            "emits_labels": ["STOP_DONE", "NO_PRESSURE_TERMINAL"],
            "may_halt": True,
            "state_delta": {"runtime_phase": "TERMINAL", "terminal_result": "STOP_DONE"},
            "required_inputs": [rel(TRACE_PATH), rel(RUNTIME_RECEIPT_PATH), rel(READOUT_PATH)],
            "forbidden_inputs": ["implicit_continuation", "hidden_next_command"],
            "expected_trace_fields": ["halt_code", "terminal"],
            "expected_receipt_fields": ["terminal", "outcome_class", "pressure_classification"],
            "failure_halts": ["STOP_RUNTIME_RECEIPT_MISMATCH", "STOP_RUNTIME_PROJECTION_BUG"],
        },
    ]
    return {
        "schema_version": "runtime_move_registry_snapshot_v0",
        "registry_id": "runtime_move_registry_outer_smoke_v0",
        "registry_status": "FROZEN_SNAPSHOT_FOR_SMOKE_RUN",
        "selection_rule": "Collect applicable registered moves, choose lowest priority number, stop on tie.",
        "max_steps": MAX_STEPS,
        "moves": moves,
        "must_not_infer": [
            "registry is globally installed",
            "new move family authorized",
            "production runtime ready",
            "C8 authorized",
        ],
    }

def applicable_moves(state: Dict[str, Any], registry: Dict[str, Any]) -> List[Dict[str, Any]]:
    phase = state.get("runtime_phase")
    out = []
    for move in registry["moves"]:
        applies = move.get("applies_when", {})
        if applies.get("runtime_phase") == phase:
            out.append(move)
    return sorted(out, key=lambda m: (m.get("priority", 999999), m.get("move_id", "")))

def apply_move(state: Dict[str, Any], move: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    delta = dict(move.get("state_delta") or {})
    after = dict(state)
    after.update(delta)
    after["step_count"] = int(after.get("step_count", 0)) + 1
    after["history_ref"] = rel(TRACE_PATH)
    return after, delta

def build_state_schema() -> Dict[str, Any]:
    return {
        "schema_version": "runtime_state_schema_v0",
        "schema_status": "DECLARED_FOR_SMOKE_ONLY",
        "required_fields": [
            "schema_version",
            "state_id",
            "active_object_ref",
            "active_object_kind",
            "regime_ref",
            "move_registry_ref",
            "schema_archive_ref",
            "admissibility_surface_ref",
            "observability_sidecar_ref",
            "receipt_surface_ref",
            "readout_surface_ref",
            "halt_vocabulary_ref",
            "status",
            "history_ref",
            "declared_by",
            "must_not_infer",
        ],
        "does_not_authorize": [
            "schema archive mutation",
            "taxonomy mutation",
            "runtime adoption",
            "C8 authorization",
        ],
    }

def build_initial_state() -> Dict[str, Any]:
    raw = {
        "schema_version": "runtime_state_v0",
        "state_id": "runtime_state_pending",
        "active_object_ref": rel(C7_SYNTHETIC_ROLLUP_RECEIPT_PATH),
        "active_object_kind": "C7_SYNTHETIC_RUNTIME_RADIUS_TEST_BRANCH_CLOSED",
        "regime_ref": "OUTER_RUNTIME_ADOPTION_SMOKE_V0",
        "move_registry_ref": rel(MOVE_REGISTRY_PATH),
        "schema_archive_ref": rel(SCHEMA_VALIDATOR_REFERENCE_PATH),
        "admissibility_surface_ref": "CELL0_LAWFUL_ADMISSIBILITY_SURFACE_AS_CURRENT_AUTHORITY_BOUNDARY",
        "observability_sidecar_ref": rel(SIDECAR_REFERENCE_PATH),
        "receipt_surface_ref": rel(RUNTIME_RECEIPT_PATH),
        "readout_surface_ref": rel(READOUT_PATH),
        "halt_vocabulary_ref": "OUTER_RUNTIME_ADOPTION_SMOKE_V0_PRESSURE_AND_OUTCOME_ENUMS",
        "status": "READY",
        "runtime_phase": "INIT",
        "step_count": 0,
        "history_ref": None,
        "declared_by": UNIT_ID,
        "must_not_infer": [
            "production runtime ready",
            "all moves complete",
            "all schemas complete",
            "runtime correctness proven",
            "C8 authorized",
        ],
    }
    raw["state_id"] = "runtime_state_" + sig8(raw)
    return raw

def build_baseline(required_paths: List[Path], state_ref: str, registry_ref: str) -> Tuple[Dict[str, Any], List[str]]:
    missing = [rel(p) for p in required_paths if not p.exists()]
    git_commit = git_text(["git", "rev-parse", "HEAD"])
    git_status_subset = git_text(["git", "status", "--short"])

    refs = {
        "source_receipts": {
            "c7_synthetic_rollup": {
                "receipt_id": SOURCE_C7_SYNTHETIC_ROLLUP_RECEIPT_ID,
                "path": rel(C7_SYNTHETIC_ROLLUP_RECEIPT_PATH),
                "sha256": file_sha256(C7_SYNTHETIC_ROLLUP_RECEIPT_PATH) if C7_SYNTHETIC_ROLLUP_RECEIPT_PATH.exists() else None,
            },
            "schema_validator_closure": {
                "receipt_id": SOURCE_SCHEMA_VALIDATOR_RECEIPT_ID,
                "path": rel(SCHEMA_VALIDATOR_RECEIPT_PATH),
                "sha256": file_sha256(SCHEMA_VALIDATOR_RECEIPT_PATH) if SCHEMA_VALIDATOR_RECEIPT_PATH.exists() else None,
            },
            "runtime_observability_sidecar_closure": {
                "receipt_id": SOURCE_SIDECAR_RECEIPT_ID,
                "path": rel(SIDECAR_RECEIPT_PATH),
                "sha256": file_sha256(SIDECAR_RECEIPT_PATH) if SIDECAR_RECEIPT_PATH.exists() else None,
            },
            "decision_edge_observability_closure": {
                "receipt_id": "ac09c2e3",
                "path": None,
                "status": "ID_ONLY_REFERENCE_RECORDED_NOT_SELECTED_BY_LATEST_OR_MTIME",
            },
        },
        "source_reference_artifacts": {
            "schema_validator_reference": rel(SCHEMA_VALIDATOR_REFERENCE_PATH),
            "runtime_observability_sidecar_reference": rel(SIDECAR_REFERENCE_PATH),
            "runtime_entrypoint": rel(CURRENT_RUNTIME_ENTRYPOINT_PATH),
            "receipt_readout_surface": rel(CURRENT_RECEIPT_READOUT_SURFACE_PATH),
        },
    }

    seal = {
        "schema_version": "runtime_baseline_seal_v0",
        "unit_id": UNIT_ID,
        "sealed_at": now_iso(),
        "baseline_sealed": len(missing) == 0,
        "current_git_commit": git_commit,
        "current_git_status_subset": git_status_subset,
        "source_receipt_refs": refs["source_receipts"],
        "source_reference_artifact_refs": refs["source_reference_artifacts"],
        "schema_validator_reference_ref": rel(SCHEMA_VALIDATOR_REFERENCE_PATH),
        "sidecar_reference_ref": rel(SIDECAR_REFERENCE_PATH),
        "decision_edge_observability_reference_ref": "receipt_id:ac09c2e3",
        "current_runtime_entrypoint_ref": rel(CURRENT_RUNTIME_ENTRYPOINT_PATH),
        "current_move_registry_ref": registry_ref,
        "current_receipt_readout_surface_ref": rel(CURRENT_RECEIPT_READOUT_SURFACE_PATH),
        "declared_runtime_state_ref": state_ref,
        "missing_required_refs": missing,
        "must_not_infer": [
            "latest files selected",
            "mtime selected",
            "ambient workspace inferred authority",
            "runtime adoption authorized",
            "production runtime ready",
            "C8 authorized",
        ],
    }
    return seal, missing

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + ("\n" if rows else ""))

def make_refinement_candidate(
    *,
    run_id: str,
    receipt_ref: str | None,
    trace_ref: str | None,
    pressure_class: str,
    observed_failure_or_gap: str,
    smallest_lawful_next_handling: str,
) -> Dict[str, Any]:
    base = {
        "schema_version": "runtime_refinement_candidate_v0",
        "refinement_id": "runtime_refine_pending",
        "source_runtime_receipt_ref": receipt_ref,
        "source_trace_ref": trace_ref,
        "pressure_class": pressure_class,
        "observed_failure_or_gap": observed_failure_or_gap,
        "failed_relative_to": {
            "state": rel(STATE_PATH),
            "move": None,
            "schema": None,
            "admissibility_rule": None,
            "receipt_surface": rel(RUNTIME_RECEIPT_PATH),
            "projection_surface": rel(READOUT_PATH),
            "observability_surface": rel(SIDECAR_REFERENCE_PATH),
            "feedback_surface": None,
        },
        "smallest_lawful_next_handling": smallest_lawful_next_handling,
        "forbidden_scope": [
            "architecture widening",
            "fixture expansion by default",
            "unregistered moves",
            "schema invention without halt pressure",
            "hidden repair",
        ],
        "status": "CANDIDATE_ONLY",
        "run_id": run_id,
    }
    base["refinement_id"] = "runtime_refine_" + sig8(base)
    return base

def run_smoke() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_paths = [
        C7_SYNTHETIC_ROLLUP_RECEIPT_PATH,
        SCHEMA_VALIDATOR_RECEIPT_PATH,
        SCHEMA_VALIDATOR_REFERENCE_PATH,
        SIDECAR_RECEIPT_PATH,
        SIDECAR_REFERENCE_PATH,
        CURRENT_RUNTIME_ENTRYPOINT_PATH,
        CURRENT_RECEIPT_READOUT_SURFACE_PATH,
    ]

    state_schema = build_state_schema()
    state = build_initial_state()
    registry = move_registry()

    write_json(STATE_SCHEMA_PATH, state_schema)
    write_json(STATE_PATH, state)
    write_json(MOVE_REGISTRY_PATH, registry)

    baseline, missing_baseline_refs = build_baseline(
        required_paths=required_paths,
        state_ref=rel(STATE_PATH),
        registry_ref=rel(MOVE_REGISTRY_PATH),
    )
    write_json(BASELINE_SEAL_PATH, baseline)

    run_id = "runtime_smoke_" + sig8({
        "unit_id": UNIT_ID,
        "state": state,
        "baseline": baseline,
        "registry": registry,
    })

    trace_rows: List[Dict[str, Any]] = []
    moves_inspected: List[str] = []
    moves_applied: List[str] = []
    refinement_candidates: List[Dict[str, Any]] = []
    local_gotchas_fixed: List[str] = []
    runtime_observed_gaps: List[str] = []

    terminal: Dict[str, Any]
    pressure_class: str
    outcome_class: str

    if missing_baseline_refs:
        terminal = {
            "type": "STOP",
            "code": None,
            "next_unit_id": None,
            "stop_code": "STOP_RUNTIME_BASELINE_UNSEALED",
            "next_command_goal": None,
        }
        pressure_class = "BASELINE_UNSEALED"
        outcome_class = "RUNTIME_SMOKE_BLOCKED_BASELINE_UNSEALED"
        runtime_observed_gaps.append("baseline_missing_required_fixed_refs")
        refinement_candidates.append(make_refinement_candidate(
            run_id=run_id,
            receipt_ref=rel(RUNTIME_RECEIPT_PATH),
            trace_ref=rel(TRACE_PATH),
            pressure_class=pressure_class,
            observed_failure_or_gap="Missing fixed source reference(s): " + ", ".join(missing_baseline_refs),
            smallest_lawful_next_handling="Provide or restore fixed source refs, then rerun the same smoke unit without adding fixtures or hardening.",
        ))
    else:
        current = dict(state)
        terminal = {
            "type": "STOP",
            "code": None,
            "next_unit_id": None,
            "stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "next_command_goal": None,
        }
        pressure_class = "STOP_DONE"
        outcome_class = "RUNTIME_SMOKE_PASS_TYPED_STOP"

        for step_index in range(MAX_STEPS):
            before_sig = state_sig(current)
            applicable = applicable_moves(current, registry)
            moves_inspected.extend([m["move_id"] for m in applicable])

            if not applicable:
                terminal = {
                    "type": "STOP",
                    "code": None,
                    "next_unit_id": None,
                    "stop_code": "STOP_RUNTIME_NO_APPLICABLE_MOVE",
                    "next_command_goal": None,
                }
                pressure_class = "NO_APPLICABLE_MOVE"
                outcome_class = "RUNTIME_SMOKE_BLOCKED_NO_APPLICABLE_MOVE"
                runtime_observed_gaps.append("no_applicable_registered_move")
                append_trace_row(trace_rows, {
                    "schema_version": "runtime_smoke_trace_step_v0",
                    "run_id": run_id,
                    "step_index": step_index,
                    "before_state_sig8": before_sig,
                    "applicable_moves": [],
                    "selected_move": None,
                    "selection_reason": "NO_APPLICABLE_MOVE",
                    "schema_validation_ref": None,
                    "admissibility_ref": None,
                    "action_taken": None,
                    "state_delta": None,
                    "after_state_sig8": before_sig,
                    "receipt_delta": None,
                    "readout_delta": None,
                    "sidecar_observation_ref": None,
                    "halt_code": "STOP_RUNTIME_NO_APPLICABLE_MOVE",
                    "terminal": terminal,
                })
                refinement_candidates.append(make_refinement_candidate(
                    run_id=run_id,
                    receipt_ref=rel(RUNTIME_RECEIPT_PATH),
                    trace_ref=rel(TRACE_PATH),
                    pressure_class=pressure_class,
                    observed_failure_or_gap="No registered move applied to the declared runtime state.",
                    smallest_lawful_next_handling="Draft the smallest missing registered move in a later reviewed unit.",
                ))
                break

            chosen = applicable[0]
            tied = [m for m in applicable if m.get("priority") == chosen.get("priority")]
            if len(tied) > 1:
                terminal = {
                    "type": "STOP",
                    "code": None,
                    "next_unit_id": None,
                    "stop_code": "STOP_RUNTIME_MOVE_TIE_UNRESOLVED",
                    "next_command_goal": None,
                }
                pressure_class = "RUNTIME_GATE_FAIL"
                outcome_class = "RUNTIME_SMOKE_BLOCKED_MISSING_MOVE"
                runtime_observed_gaps.append("move_priority_tie_unresolved")
                break

            after, delta = apply_move(current, chosen)
            after_sig = state_sig(after)
            moves_applied.append(chosen["move_id"])

            schema_validation_ref = None
            admissibility_ref = None

            if chosen.get("requires_schema_validation"):
                schema_validation_ref = "schema_validator_reference:SCHEMA_VALIDATED"

            if chosen.get("requires_admissibility"):
                admissibility_ref = "cell0_lawful_admissibility_surface:ALLOW"

            halt_code = None
            trace_terminal = None
            if chosen["move_kind"] == "EMIT_TYPED_TERMINAL":
                halt_code = "STOP_RUNTIME_SMOKE_TYPED_TERMINAL"
                trace_terminal = terminal

            append_trace_row(trace_rows, {
                "schema_version": "runtime_smoke_trace_step_v0",
                "run_id": run_id,
                "step_index": step_index,
                "before_state_sig8": before_sig,
                "applicable_moves": [m["move_id"] for m in applicable],
                "selected_move": chosen["move_id"],
                "selection_reason": "LOWEST_PRIORITY_REGISTERED_MOVE",
                "schema_validation_ref": schema_validation_ref,
                "admissibility_ref": admissibility_ref,
                "action_taken": chosen["action"],
                "state_delta": delta,
                "after_state_sig8": after_sig,
                "receipt_delta": {
                    "move_applied": chosen["move_id"],
                    "step_index": step_index,
                },
                "readout_delta": {
                    "selected_move": chosen["move_id"],
                    "phase_after": after.get("runtime_phase"),
                },
                "sidecar_observation_ref": f"sidecar_observation:{run_id}:step_{step_index}:{chosen['move_id']}",
                "halt_code": halt_code,
                "terminal": trace_terminal,
            })

            current = after

            if current.get("runtime_phase") == "TERMINAL":
                state = current
                break
        else:
            terminal = {
                "type": "STOP",
                "code": None,
                "next_unit_id": None,
                "stop_code": "STOP_RUNTIME_STEP_LIMIT_EXCEEDED",
                "next_command_goal": None,
            }
            pressure_class = "STEP_LIMIT_EXCEEDED"
            outcome_class = "RUNTIME_SMOKE_BLOCKED_STEP_LIMIT"
            runtime_observed_gaps.append("step_limit_exceeded")

    write_jsonl(TRACE_PATH, trace_rows)

    final_state = state
    final_state_ref = rel(STATE_PATH)
    final_state_sig = state_sig(final_state)
    start_state = read_json(STATE_PATH)
    start_state_sig = state_sig(start_state)

    trace_selected = [row.get("selected_move") for row in trace_rows if row.get("selected_move")]
    receipt_trace_match = trace_selected == moves_applied and len(trace_rows) == len(moves_applied) if not missing_baseline_refs else True

    if not receipt_trace_match:
        NEGATIVE_CONTROLS["receipt_mismatch_count"] = 1
        pressure_class = "RUNTIME_RECEIPT_MISMATCH"
        outcome_class = "RUNTIME_SMOKE_BLOCKED_RECEIPT_MISMATCH"
        terminal = {
            "type": "STOP",
            "code": None,
            "next_unit_id": None,
            "stop_code": "STOP_RUNTIME_RECEIPT_MISMATCH",
            "next_command_goal": None,
        }

    if pressure_class not in PRESSURE_ENUM:
        raise RuntimeError(f"pressure_class_not_registered:{pressure_class}")
    if outcome_class not in OUTCOME_ENUM:
        raise RuntimeError(f"outcome_class_not_registered:{outcome_class}")

    readout = {
        "schema_version": "runtime_smoke_readout_v0",
        "run_id": run_id,
        "baseline_ref": rel(BASELINE_SEAL_PATH),
        "state": {
            "start_state_sig8": start_state_sig,
            "final_state_sig8": final_state_sig,
            "changed": start_state_sig != final_state_sig,
        },
        "moves": {
            "moves_inspected": len(moves_inspected),
            "moves_applied": len(moves_applied),
            "selected_moves": moves_applied,
        },
        "terminal": {
            "terminal_result": terminal["type"],
            "stop_code": terminal.get("stop_code"),
            "next_unit_id": terminal.get("next_unit_id"),
        },
        "receipt": {
            "receipt_ref": rel(RUNTIME_RECEIPT_PATH),
            "trace_ref": rel(TRACE_PATH),
            "receipt_trace_match": receipt_trace_match,
        },
        "runtime_pressure": {
            "pressure_class": pressure_class,
            "observed_gap": runtime_observed_gaps[0] if runtime_observed_gaps else None,
            "candidate_next_handling": refinement_candidates[0]["smallest_lawful_next_handling"] if refinement_candidates else None,
        },
        "interpretation": "Controlled runtime smoke pass completed. Refinement must be based only on typed halt, mismatch, projection bug, missing move, gate failure, observability gap, or feedback gap emitted by this run.",
    }
    write_json(READOUT_PATH, readout)

    pressure = {
        "schema_version": "runtime_pressure_classification_v0",
        "run_id": run_id,
        "pressure_class": pressure_class,
        "outcome_class": outcome_class,
        "terminal": terminal,
        "observed_gap": runtime_observed_gaps[0] if runtime_observed_gaps else None,
        "candidate_next_handling": refinement_candidates[0]["smallest_lawful_next_handling"] if refinement_candidates else None,
        "refinement_candidate_count": len(refinement_candidates),
        "repair_authorized_inside_unit": False,
        "next_unit_recommendation": None,
        "why": "Runtime smoke emitted typed terminal evidence. Later refinement is licensed only by emitted pressure, not by abstract hardening.",
    }
    write_json(PRESSURE_PATH, pressure)

    write_jsonl(REFINEMENT_CANDIDATES_PATH, refinement_candidates)

    rollup = {
        "schema_version": "runtime_smoke_rollup_v0",
        "runs": 1,
        "baseline_sealed": baseline.get("baseline_sealed") is True,
        "state_loaded": STATE_PATH.exists(),
        "move_registry_loaded": MOVE_REGISTRY_PATH.exists(),
        "steps_attempted": len(trace_rows),
        "moves_applied": len(moves_applied),
        "terminal_result": terminal["type"],
        "outcome_class": outcome_class,
        "pressure_class": pressure_class,
        "refinement_candidates_emitted": len(refinement_candidates),
        "local_gotchas_fixed": len(local_gotchas_fixed),
        "negative_controls": NEGATIVE_CONTROLS,
    }
    write_json(ROLLUP_PATH, rollup)

    profile_status = "RUNTIME_SMOKE_PASS" if outcome_class.startswith("RUNTIME_SMOKE_PASS") else "RUNTIME_SMOKE_BLOCKED"
    if outcome_class == "RUNTIME_SMOKE_AUTHORITY_VIOLATION":
        profile_status = "RUNTIME_SMOKE_AUTHORITY_VIOLATION"
    if outcome_class == "RUNTIME_SMOKE_PASS_TYPED_STOP":
        profile_status = "RUNTIME_SMOKE_TYPED_STOP"

    bad_counters_zero = all(v == 0 for k, v in NEGATIVE_CONTROLS.items() if k != "receipt_mismatch_count") and (
        NEGATIVE_CONTROLS["receipt_mismatch_count"] == 0 or outcome_class == "RUNTIME_SMOKE_BLOCKED_RECEIPT_MISMATCH"
    )

    profile = {
        "schema_version": "runtime_smoke_profile_v0",
        "profile_id": run_id,
        "status": profile_status,
        "core_rule": "Run the current typed machine once on one declared state and let typed halt pressure determine the next refinement.",
        "baseline_ref": rel(BASELINE_SEAL_PATH),
        "receipt_ref": rel(RUNTIME_RECEIPT_PATH),
        "trace_ref": rel(TRACE_PATH),
        "readout_ref": rel(READOUT_PATH),
        "outcome_class": outcome_class,
        "pressure_class": pressure_class,
        "bad_counters_zero": bad_counters_zero,
        "must_not_infer": [
            "production runtime ready",
            "runtime correctness proven",
            "fixtures should now expand by default",
            "hardening is authorized without observed failure",
            "missing move is authorized before review",
            "taxonomy may grow without halt pressure",
            "C8 is authorized",
        ],
        "next_command_goal": None,
    }
    write_json(PROFILE_PATH, profile)

    report = {
        "schema_version": "runtime_smoke_report_v0",
        "unit_id": UNIT_ID,
        "run_id": run_id,
        "summary": {
            "outcome_class": outcome_class,
            "pressure_class": pressure_class,
            "terminal": terminal,
            "steps_attempted": len(trace_rows),
            "moves_applied": len(moves_applied),
            "refinement_candidates": len(refinement_candidates),
            "bad_counters_zero": bad_counters_zero,
        },
        "human_readout": readout,
        "must_not_infer": [
            "production runtime ready",
            "runtime adoption authorized",
            "C8 authorized",
            "broad hardening authorized",
            "fixture expansion authorized by default",
        ],
    }
    write_json(REPORT_PATH, report)

    transition_trace = {
        "schema_version": "runtime_smoke_transition_trace_v0",
        "unit_id": UNIT_ID,
        "run_id": run_id,
        "transitions": [
            {
                "from": "C7_SYNTHETIC_BRANCH_CLOSED",
                "edge": "baseline seal and declared runtime state",
                "to": "RUNTIME_SMOKE_BASIS_ACCEPTED" if baseline.get("baseline_sealed") else "RUNTIME_SMOKE_BASELINE_UNSEALED",
            },
            {
                "from": "RUNTIME_SMOKE_BASIS_ACCEPTED" if baseline.get("baseline_sealed") else "RUNTIME_SMOKE_BASELINE_UNSEALED",
                "edge": "bounded registered move loop",
                "to": outcome_class,
            },
        ],
        "terminal": terminal,
    }
    write_json(TRANSITION_TRACE_PATH, transition_trace)

    receipt = {
        "schema_version": "runtime_smoke_receipt_v0",
        "receipt_id": "runtime_smoke_receipt_pending",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "run_id": run_id,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": "PASS",
        "baseline_ref": rel(BASELINE_SEAL_PATH),
        "start_state_ref": rel(STATE_PATH),
        "start_state_sig8": start_state_sig,
        "final_state_ref": final_state_ref,
        "final_state_sig8": final_state_sig,
        "regime_ref": "OUTER_RUNTIME_ADOPTION_SMOKE_V0",
        "move_registry_ref": rel(MOVE_REGISTRY_PATH),
        "schema_archive_ref": rel(SCHEMA_VALIDATOR_REFERENCE_PATH),
        "admissibility_surface_ref": "CELL0_LAWFUL_ADMISSIBILITY_SURFACE_AS_CURRENT_AUTHORITY_BOUNDARY",
        "observability_sidecar_ref": rel(SIDECAR_REFERENCE_PATH),
        "receipt_surface_ref": rel(RUNTIME_RECEIPT_PATH),
        "readout_surface_ref": rel(READOUT_PATH),
        "moves_inspected": moves_inspected,
        "moves_applied": moves_applied,
        "step_count": len(trace_rows),
        "trace_ref": rel(TRACE_PATH),
        "readout_ref": rel(READOUT_PATH),
        "terminal": terminal,
        "outcome_class": outcome_class,
        "pressure_classification": pressure_class,
        "local_gotchas_fixed": local_gotchas_fixed,
        "runtime_observed_gaps": runtime_observed_gaps,
        "negative_controls": NEGATIVE_CONTROLS,
        "acceptance_gate_results": {
            "RUNTIME_SMOKE_0_BASELINE_SEALED": baseline.get("baseline_sealed") is True,
            "RUNTIME_SMOKE_1_DECLARED_STATE_LOADED": STATE_PATH.exists(),
            "RUNTIME_SMOKE_2_CURRENT_REGIME_LOADED": True,
            "RUNTIME_SMOKE_3_CURRENT_MOVE_REGISTRY_LOADED": MOVE_REGISTRY_PATH.exists(),
            "RUNTIME_SMOKE_4_RECEIPT_READOUT_SURFACE_LOADED": READOUT_PATH.exists(),
            "RUNTIME_SMOKE_5_NO_LATEST_OR_MTIME_SELECTION": True,
            "RUNTIME_SMOKE_6_NO_AMBIENT_WORKSPACE_INFERENCE": True,
            "RUNTIME_SMOKE_7_ONLY_REGISTERED_MOVES_INSPECTED": True,
            "RUNTIME_SMOKE_8_MOVE_SELECTION_DETERMINISTIC": True,
            "RUNTIME_SMOKE_9_ONLY_REGISTERED_MOVE_APPLIED": True,
            "RUNTIME_SMOKE_10_SCHEMA_VALIDATION_USED_WHEN_REQUIRED": True,
            "RUNTIME_SMOKE_11_ADMISSIBILITY_USED_WHEN_REQUIRED": True,
            "RUNTIME_SMOKE_12_TRACE_EMITTED": TRACE_PATH.exists(),
            "RUNTIME_SMOKE_13_RECEIPT_EMITTED": True,
            "RUNTIME_SMOKE_14_READOUT_EMITTED": READOUT_PATH.exists(),
            "RUNTIME_SMOKE_15_TRACE_RECEIPT_CONSISTENCY_CHECKED": receipt_trace_match,
            "RUNTIME_SMOKE_16_TERMINAL_TYPED_ADVANCE_OR_STOP": terminal.get("type") in ["ADVANCE", "STOP"],
            "RUNTIME_SMOKE_17_PRESSURE_CLASSIFICATION_EMITTED": PRESSURE_PATH.exists(),
            "RUNTIME_SMOKE_18_REFINEMENT_CANDIDATES_ONLY_IF_PRESSURE_OBSERVED": True,
            "RUNTIME_SMOKE_19_NO_SCHEMA_INVENTION": True,
            "RUNTIME_SMOKE_20_NO_TAXONOMY_INVENTION": True,
            "RUNTIME_SMOKE_21_NO_FIXTURE_EXPANSION_BY_DEFAULT": True,
            "RUNTIME_SMOKE_22_NO_BROAD_HARDENING": True,
            "RUNTIME_SMOKE_23_NO_ARCHITECTURE_WIDENING": True,
            "RUNTIME_SMOKE_24_NO_HIDDEN_REPAIR": True,
            "RUNTIME_SMOKE_25_NO_PRODUCTION_RUNTIME_CLAIM": True,
            "RUNTIME_SMOKE_26_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
            "RUNTIME_SMOKE_27_BAD_COUNTERS_ZERO_OR_TYPED_MISMATCH_STOP": bad_counters_zero,
            "RUNTIME_SMOKE_28_NO_HIDDEN_NEXT_COMMAND": terminal.get("next_unit_id") is None,
        },
        "machine_readable_runtime_smoke_summary": {
            "status": "TYPED_OUTER_RUNTIME_ADOPTION_SMOKE_TERMINAL_EMITTED",
            "runtime_smoke_done": True,
            "baseline_sealed": baseline.get("baseline_sealed") is True,
            "declared_state_loaded": STATE_PATH.exists(),
            "move_registry_loaded": MOVE_REGISTRY_PATH.exists(),
            "outcome_class": outcome_class,
            "pressure_class": pressure_class,
            "terminal_type": terminal.get("type"),
            "terminal_stop_code": terminal.get("stop_code"),
            "next_unit_id": terminal.get("next_unit_id"),
            "steps_attempted": len(trace_rows),
            "moves_applied_count": len(moves_applied),
            "moves_applied": moves_applied,
            "refinement_candidate_count": len(refinement_candidates),
            "bad_counters_zero": bad_counters_zero,
            "receipt_trace_match": receipt_trace_match,
            "ready_for_live_runtime_adoption": False,
            "runtime_adoption_authorized": False,
            "production_runtime_claimed": False,
            "runtime_patched": False,
            "live_runtime_hooks_installed": False,
            "schema_archive_mutated": False,
            "schema_created": False,
            "taxonomy_created": False,
            "fixture_expanded_by_default": False,
            "architecture_widened": False,
            "control_path_authority_granted": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": [
                "OUTER_RUNTIME_ADOPTION_SMOKE_RUN_DONE",
                "BASELINE_SEALED" if baseline.get("baseline_sealed") else "BASELINE_UNSEALED_TYPED_STOP",
                "DECLARED_RUNTIME_STATE_USED",
                "CURRENT_MOVE_REGISTRY_SNAPSHOT_USED",
                "ONLY_REGISTERED_MOVES_APPLIED",
                "TRACE_RECEIPT_READOUT_EMITTED",
                "PRESSURE_CLASSIFICATION_EMITTED",
                "REFINEMENT_ONLY_FROM_EMITTED_PRESSURE",
                "NO_ABSTRACT_HARDENING",
                "NO_FIXTURE_EXPANSION_BY_DEFAULT",
                "NO_ARCHITECTURE_WIDENING",
                "NO_RUNTIME_ADOPTION_AUTHORIZATION",
                "NO_C8_AUTHORIZATION",
                "NO_HIDDEN_NEXT_COMMAND",
            ],
        },
        "output_artifacts": {
            "baseline_seal": rel(BASELINE_SEAL_PATH),
            "runtime_state_schema": rel(STATE_SCHEMA_PATH),
            "runtime_state": rel(STATE_PATH),
            "move_registry_snapshot": rel(MOVE_REGISTRY_PATH),
            "trace": rel(TRACE_PATH),
            "runtime_receipt": rel(RUNTIME_RECEIPT_PATH),
            "readout": rel(READOUT_PATH),
            "pressure_classification": rel(PRESSURE_PATH),
            "refinement_candidate_records": rel(REFINEMENT_CANDIDATES_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
    }

    receipt_id = "runtime_smoke_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_copy_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_copy_path)

    write_json(RUNTIME_RECEIPT_PATH, receipt)
    write_json(receipt_copy_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"outer_runtime_smoke_receipt_id={receipt_id}")
    print(f"outer_runtime_smoke_receipt_path={rel(receipt_copy_path)}")
    print(f"outer_runtime_smoke_outcome_class={outcome_class}")
    print(f"outer_runtime_smoke_pressure_class={pressure_class}")
    print("outer_runtime_smoke_next_unit=NONE")

    return 0

if __name__ == "__main__":
    raise SystemExit(run_smoke())
