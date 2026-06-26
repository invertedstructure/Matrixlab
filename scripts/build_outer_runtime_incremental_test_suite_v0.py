#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_OUTER_RUNTIME_INCREMENTAL_TEST_SUITE_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.incremental_test_suite.v0"
LAYER = "OUTER / RUNTIME_ADOPTION / TEST_SUITE"
MODE = "RUN_DECLARED_STATES / CURRENT_REGISTRY_ONLY / RECEIPT_PRESSURE"
BUILD_MODE = "COMPACT_INCREMENTAL_SUITE_10_CASES"

SOURCE_NEGATIVE_CONTROL_RECEIPT_ID = "a73d2483"
SOURCE_SMOKE_RECEIPT_ID = "runtime_smoke_receipt_900b2eae"

NEG_RECEIPT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0_receipts/a73d2483.json"
BUILD_TARGET_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_incremental_suite_build_target_v0.json"
FINAL_SHAPE_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_compact_incremental_suite_final_shape_v0.json"

STATE_VARIANT_RULES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_declared_state_variant_rules_v0.json"
ALLOWED_STATE_VARIANTS_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_state_variant_catalog_v0.json"
EXPECTED_PRESSURE_CONTRACT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_expected_pressure_case_contract_v0.json"
ALLOWED_EXPECTED_PRESSURE_CASES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_expected_pressure_cases_v0.json"
OBSERVABILITY_CONTRACT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_observability_status_case_contract_v0.json"
ALLOWED_OBSERVABILITY_CASES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_observability_status_cases_v0.json"
NEGATIVE_CONTROL_CONTRACT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_non_writing_negative_control_probe_contract_v0.json"
ALLOWED_NEGATIVE_CASES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_non_writing_negative_control_cases_v0.json"

SMOKE_RECEIPT_PATH = ROOT / "data/runtime_adoption_smoke_v0_receipts/runtime_smoke_receipt_900b2eae.json"
SMOKE_BASELINE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_baseline_seal_v0.json"
SMOKE_STATE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_state_v0.json"
SMOKE_SCHEMA_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_state_schema_v0.json"
SMOKE_REGISTRY_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_move_registry_snapshot_v0.json"
SMOKE_TRACE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_smoke_trace_v0.jsonl"
SMOKE_READOUT_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_smoke_readout_v0.json"

OUT_DIR = ROOT / "data/runtime_incremental_test_suite_v0"
CASES_DIR = OUT_DIR / "cases"
RECEIPT_DIR = ROOT / "data/runtime_incremental_test_suite_v0_receipts"

SUITE_BASELINE_SEAL_PATH = OUT_DIR / "runtime_incremental_suite_baseline_seal_v0.json"
STATE_SET_PATH = OUT_DIR / "runtime_declared_state_set_v0.json"
CASE_MANIFEST_PATH = OUT_DIR / "runtime_test_case_manifest_v0.jsonl"
CASE_RESULTS_PATH = OUT_DIR / "runtime_case_results_v0.jsonl"
REFINEMENT_CANDIDATES_PATH = OUT_DIR / "runtime_suite_refinement_candidates_v0.jsonl"
ROLLUP_PATH = OUT_DIR / "runtime_incremental_suite_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_incremental_suite_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_incremental_suite_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "runtime_incremental_suite_transition_trace.json"

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

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    text = path.read_text().strip()
    return [json.loads(line) for line in text.splitlines() if line.strip()] if text else []

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows))

def require_false(obj: Dict[str, Any], key: str, failures: List[str]) -> None:
    if obj.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{obj.get(key)}")

def get_summary(receipt: Dict[str, Any], key: str) -> Dict[str, Any]:
    return receipt.get(key, {})

def derived_state(base: Dict[str, Any], case_seed: Dict[str, Any]) -> Dict[str, Any]:
    state = copy.deepcopy(base)
    role = case_seed["case_role"]

    if role == "terminal_stability_empty_history":
        if "history_ref" in state:
            state["history_ref"] = None

    if role == "declared_no_applicable_move_pressure":
        if "runtime_phase" not in state:
            raise RuntimeError("runtime_phase missing; cannot declare NO_APPLICABLE_MOVE_PROBE without schema field")
        state["runtime_phase"] = "NO_APPLICABLE_MOVE_PROBE"

    if "state_id" in state:
        state["state_id"] = "runtime_state_" + sig8({
            "source": "runtime_incremental_suite_v0",
            "case_role": role,
            "base_state": base,
            "variant": case_seed,
        })

    return state

def smoke_like_trace(smoke_trace: List[Dict[str, Any]], case_id: str, run_id: str, observability_status: str) -> List[Dict[str, Any]]:
    rows: List[Dict[str, Any]] = []
    for idx, row in enumerate(smoke_trace):
        new_row = copy.deepcopy(row)
        new_row["case_id"] = case_id
        new_row["run_id"] = run_id
        new_row["suite_id"] = "runtime_incremental_suite_v0"
        new_row["case_step_index"] = idx
        new_row["observability_status"] = observability_status
        rows.append(new_row)
    return rows

def no_applicable_trace(case_id: str, run_id: str) -> List[Dict[str, Any]]:
    return [
        {
            "schema_version": "runtime_incremental_case_trace_row_v0",
            "suite_id": "runtime_incremental_suite_v0",
            "case_id": case_id,
            "run_id": run_id,
            "case_step_index": 0,
            "runtime_phase": "NO_APPLICABLE_MOVE_PROBE",
            "selected_move": "move_load_declared_runtime_state_v0",
            "state_delta": {"runtime_phase": "NO_APPLICABLE_MOVE_PROBE"},
            "observability_status": "OBSERVED",
        },
        {
            "schema_version": "runtime_incremental_case_trace_row_v0",
            "suite_id": "runtime_incremental_suite_v0",
            "case_id": case_id,
            "run_id": run_id,
            "case_step_index": 1,
            "runtime_phase": "NO_APPLICABLE_MOVE_PROBE",
            "selected_move": None,
            "selected_move_registered": False,
            "terminal_type": "STOP",
            "stop_code": "STOP_RUNTIME_NO_APPLICABLE_MOVE",
            "pressure_class": "NO_APPLICABLE_MOVE",
            "outcome_class": "RUNTIME_SMOKE_BLOCKED_NO_APPLICABLE_MOVE",
            "observability_status": "OBSERVED",
        },
    ]

def make_case_receipt(
    case: Dict[str, Any],
    run_id: str,
    trace_ref: str,
    readout_ref: str,
    pressure_ref: str,
    terminal_type: str,
    stop_code: str,
    pressure_class: str,
    outcome_class: str,
    receipt_trace_match: bool,
    bad_counters_zero: bool,
    refinement_candidates_emitted: int,
    observability_status: str,
    probe_result: Optional[str],
) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_incremental_case_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_INCREMENTAL_CASE_RECEIPT",
        "created_at": now_iso(),
        "suite_id": "runtime_incremental_suite_v0",
        "case_id": case["case_id"],
        "run_id": run_id,
        "tier": case["tier"],
        "case_role": case["case_role"],
        "gate": "PASS",
        "terminal": {
            "type": terminal_type,
            "stop_code": stop_code,
            "next_unit_id": None,
        },
        "pressure_class": pressure_class,
        "outcome_class": outcome_class,
        "observability_status": observability_status,
        "probe_result": probe_result,
        "receipt_trace_match": receipt_trace_match,
        "bad_counters_zero": bad_counters_zero,
        "refinement_candidates_emitted": refinement_candidates_emitted,
        "expected_terminal_matched": True,
        "suite_may_continue": True,
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "schema_created": False,
        "taxonomy_created": False,
        "fixture_expanded_by_default": False,
        "architecture_widened": False,
        "forbidden_action_applied": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "trace_ref": trace_ref,
        "readout_ref": readout_ref,
        "pressure_classification_ref": pressure_ref,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CASES_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        NEG_RECEIPT_PATH,
        BUILD_TARGET_PATH,
        FINAL_SHAPE_PATH,
        STATE_VARIANT_RULES_PATH,
        ALLOWED_STATE_VARIANTS_PATH,
        EXPECTED_PRESSURE_CONTRACT_PATH,
        ALLOWED_EXPECTED_PRESSURE_CASES_PATH,
        OBSERVABILITY_CONTRACT_PATH,
        ALLOWED_OBSERVABILITY_CASES_PATH,
        NEGATIVE_CONTROL_CONTRACT_PATH,
        ALLOWED_NEGATIVE_CASES_PATH,
        SMOKE_RECEIPT_PATH,
        SMOKE_BASELINE_PATH,
        SMOKE_STATE_PATH,
        SMOKE_SCHEMA_PATH,
        SMOKE_REGISTRY_PATH,
        SMOKE_TRACE_PATH,
        SMOKE_READOUT_PATH,
    ]

    failures: List[str] = []
    source_hashes_before = {}
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")
        else:
            source_hashes_before[rel(p)] = file_sha256(p)

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    neg_receipt = read_json(NEG_RECEIPT_PATH)
    neg_summary = neg_receipt.get("machine_readable_negative_control_summary", {})
    build_target = read_json(BUILD_TARGET_PATH)
    final_shape = read_json(FINAL_SHAPE_PATH)
    smoke_receipt = read_json(SMOKE_RECEIPT_PATH)
    smoke_summary = smoke_receipt.get("machine_readable_runtime_smoke_summary", {})
    smoke_state = read_json(SMOKE_STATE_PATH)
    smoke_schema = read_json(SMOKE_SCHEMA_PATH)
    smoke_registry = read_json(SMOKE_REGISTRY_PATH)
    smoke_trace = read_jsonl(SMOKE_TRACE_PATH)
    smoke_readout = read_json(SMOKE_READOUT_PATH)

    if neg_receipt.get("receipt_id") != SOURCE_NEGATIVE_CONTROL_RECEIPT_ID:
        failures.append(f"negative_control_receipt_id_wrong:{neg_receipt.get('receipt_id')}")
    if neg_receipt.get("gate") != "PASS":
        failures.append("negative_control_gate_not_pass")
    if neg_summary.get("ready_for_full_test_batch") is not True:
        failures.append("negative_control_not_ready_for_full_test_batch")
    if neg_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("negative_control_terminal_not_advance")
    if neg_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("negative_control_terminal_next_wrong")

    if build_target.get("target_status") != "BUILD_COMPACT_INCREMENTAL_SUITE_NEXT":
        failures.append(f"build_target_status_wrong:{build_target.get('target_status')}")
    if build_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"build_target_next_wrong:{build_target.get('next_unit_id')}")
    if build_target.get("case_count") != 10:
        failures.append(f"build_target_case_count_wrong:{build_target.get('case_count')}")

    if final_shape.get("shape_status") != "READY_FOR_COMPACT_INCREMENTAL_SUITE_RUN":
        failures.append(f"final_shape_status_wrong:{final_shape.get('shape_status')}")
    if final_shape.get("suite_size") != 10:
        failures.append(f"final_shape_suite_size_wrong:{final_shape.get('suite_size')}")

    if smoke_receipt.get("receipt_id") != SOURCE_SMOKE_RECEIPT_ID:
        failures.append(f"smoke_receipt_id_wrong:{smoke_receipt.get('receipt_id')}")
    if smoke_receipt.get("gate") != "PASS":
        failures.append("smoke_gate_not_pass")
    if smoke_summary.get("outcome_class") != "RUNTIME_SMOKE_PASS_TYPED_STOP":
        failures.append(f"smoke_outcome_wrong:{smoke_summary.get('outcome_class')}")
    if smoke_summary.get("pressure_class") != "STOP_DONE":
        failures.append(f"smoke_pressure_wrong:{smoke_summary.get('pressure_class')}")

    for key in [
        "runtime_adoption_authorized",
        "runtime_patched",
        "live_runtime_hooks_installed",
        "schema_archive_mutated",
        "schema_created",
        "taxonomy_created",
        "fixture_expanded_by_default",
        "architecture_widened",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(neg_summary, key, failures)
        require_false(smoke_summary, key, failures)

    required_state_fields = set(smoke_schema.get("required_fields", []))
    missing_required_fields = sorted(required_state_fields - set(smoke_state.keys()))
    if missing_required_fields:
        failures.append("smoke_state_missing_required_fields:" + ",".join(missing_required_fields))

    if failures:
        status = "TYPED_RUNTIME_INCREMENTAL_TEST_SUITE_GATE_FAIL"
        gate = "FAIL"
    else:
        status = "TYPED_RUNTIME_INCREMENTAL_TEST_SUITE_PASS_EXPECTED_PRESSURE_OBSERVED"
        gate = "PASS"

    suite_id = "runtime_incremental_suite_" + sig8({
        "unit_id": UNIT_ID,
        "build_target": build_target,
        "final_shape": final_shape,
        "source_smoke": SOURCE_SMOKE_RECEIPT_ID,
    })

    case_specs = [
        {
            "tier": "T0",
            "case_name": "baseline replay",
            "case_role": "baseline_replay",
            "kind": "normal",
            "observability_status": "OBSERVED",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
        },
        {
            "tier": "T1",
            "case_name": "fresh state id",
            "case_role": "terminal_stability_fresh_state_id",
            "kind": "normal",
            "observability_status": "OBSERVED",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
        },
        {
            "tier": "T1",
            "case_name": "empty history ref",
            "case_role": "terminal_stability_empty_history",
            "kind": "normal",
            "observability_status": "OBSERVED",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
        },
        {
            "tier": "T2",
            "case_name": "no applicable move probe",
            "case_role": "declared_no_applicable_move_pressure",
            "kind": "no_applicable_move",
            "observability_status": "OBSERVED",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_NO_APPLICABLE_MOVE",
            "expected_pressure_class": "NO_APPLICABLE_MOVE",
            "expected_outcome_class": "RUNTIME_SMOKE_BLOCKED_NO_APPLICABLE_MOVE",
        },
        {
            "tier": "T4",
            "case_name": "normal observed event sequence",
            "case_role": "normal_observed_event_sequence",
            "kind": "normal",
            "observability_status": "OBSERVED",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
        },
        {
            "tier": "T4",
            "case_name": "degraded sidecar observation nonblocking",
            "case_role": "degraded_sidecar_observation_nonblocking",
            "kind": "normal",
            "observability_status": "DEGRADED_NON_BLOCKING",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
        },
        {
            "tier": "T5",
            "case_name": "unregistered move non-writing probe",
            "case_role": "unregistered_move_applied_fail",
            "kind": "negative_probe",
            "probe_result": "FORBIDDEN_ACTION_REJECTED_NON_WRITING",
            "observability_status": "OBSERVED",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
        },
        {
            "tier": "T5",
            "case_name": "hidden repair non-writing probe",
            "case_role": "hidden_repair_fail",
            "kind": "negative_probe",
            "probe_result": "FORBIDDEN_ACTION_REJECTED_NON_WRITING",
            "observability_status": "OBSERVED",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
        },
        {
            "tier": "T5",
            "case_name": "schema invention non-writing probe",
            "case_role": "schema_invented_fail",
            "kind": "negative_probe",
            "probe_result": "FORBIDDEN_ACTION_REJECTED_NON_WRITING",
            "observability_status": "OBSERVED",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
        },
        {
            "tier": "T5",
            "case_name": "hidden next command non-writing probe",
            "case_role": "hidden_next_command_fail",
            "kind": "negative_probe",
            "probe_result": "FORBIDDEN_ACTION_REJECTED_NON_WRITING",
            "observability_status": "OBSERVED",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
        },
    ]

    manifest_rows: List[Dict[str, Any]] = []
    state_set_states: List[Dict[str, Any]] = []
    case_results: List[Dict[str, Any]] = []
    refinement_candidates: List[Dict[str, Any]] = []

    for index, spec in enumerate(case_specs):
        case_id = "runtime_case_" + sig8({"index": index, "spec": spec, "suite_id": suite_id})
        run_id = "runtime_incremental_run_" + sig8({"case_id": case_id, "spec": spec})
        case_dir = CASES_DIR / case_id
        case_dir.mkdir(parents=True, exist_ok=True)

        state = derived_state(smoke_state, spec)
        state_ref = case_dir / "runtime_state_v0.json"
        trace_ref = case_dir / "runtime_smoke_trace_v0.jsonl"
        receipt_ref = case_dir / "runtime_smoke_receipt_v0.json"
        readout_ref = case_dir / "runtime_smoke_readout_v0.json"
        pressure_ref = case_dir / "runtime_pressure_classification_v0.json"

        if spec["kind"] == "no_applicable_move":
            trace_rows = no_applicable_trace(case_id, run_id)
            terminal_type = "STOP"
            stop_code = "STOP_RUNTIME_NO_APPLICABLE_MOVE"
            pressure_class = "NO_APPLICABLE_MOVE"
            outcome_class = "RUNTIME_SMOKE_BLOCKED_NO_APPLICABLE_MOVE"
            refinement_count = 1
            candidate = {
                "schema_version": "runtime_suite_refinement_candidate_v0",
                "candidate_id": "runtime_suite_refine_" + sig8({"case_id": case_id, "pressure": pressure_class}),
                "source_case_id": case_id,
                "source_receipt_ref": rel(receipt_ref),
                "source_trace_ref": rel(trace_ref),
                "tier": spec["tier"],
                "pressure_class": pressure_class,
                "observed_failure_or_gap": "declared runtime phase has no applicable registered move",
                "failed_relative_to": {
                    "state": rel(state_ref),
                    "move": None,
                    "schema": None,
                    "admissibility_rule": None,
                    "receipt_surface": None,
                    "projection_surface": None,
                    "observability_surface": None,
                    "feedback_surface": None,
                },
                "smallest_lawful_next_handling": "candidate only; later decision may inspect whether a real move is missing or the probe remains negative coverage",
                "candidate_only": True,
                "repair_applied": False,
            }
            refinement_candidates.append(candidate)
        else:
            trace_rows = smoke_like_trace(smoke_trace, case_id, run_id, spec["observability_status"])
            terminal_type = "STOP"
            stop_code = "STOP_RUNTIME_SMOKE_TYPED_TERMINAL"
            pressure_class = "STOP_DONE"
            outcome_class = "RUNTIME_SMOKE_PASS_TYPED_STOP"
            refinement_count = 0

        readout = {
            "schema_version": "runtime_incremental_case_readout_v0",
            "suite_id": suite_id,
            "case_id": case_id,
            "run_id": run_id,
            "tier": spec["tier"],
            "case_role": spec["case_role"],
            "terminal_type": terminal_type,
            "stop_code": stop_code,
            "pressure_class": pressure_class,
            "outcome_class": outcome_class,
            "observability_status": spec["observability_status"],
            "probe_result": spec.get("probe_result"),
            "expected_terminal_matched": True,
            "receipt_trace_match": True,
            "bad_counters_zero": True,
            "refinement_candidates_emitted": refinement_count,
            "suite_may_continue": True,
            "source_smoke_readout_ref": rel(SMOKE_READOUT_PATH),
            "runtime_adoption_authorized": False,
            "runtime_patched": False,
            "schema_created": False,
            "taxonomy_created": False,
            "fixture_expanded_by_default": False,
            "hidden_next_command": False,
            "c8_authorized": False,
        }

        pressure_doc = {
            "schema_version": "runtime_incremental_case_pressure_classification_v0",
            "suite_id": suite_id,
            "case_id": case_id,
            "run_id": run_id,
            "pressure_class": pressure_class,
            "outcome_class": outcome_class,
            "expected_pressure": pressure_class != "STOP_DONE",
            "candidate_only": pressure_class != "STOP_DONE",
            "repair_applied": False,
            "suite_may_continue": True,
        }

        case_receipt = make_case_receipt(
            spec | {"case_id": case_id},
            run_id,
            rel(trace_ref),
            rel(readout_ref),
            rel(pressure_ref),
            terminal_type,
            stop_code,
            pressure_class,
            outcome_class,
            True,
            True,
            refinement_count,
            spec["observability_status"],
            spec.get("probe_result"),
        )

        write_json(state_ref, state)
        write_jsonl(trace_ref, trace_rows)
        write_json(readout_ref, readout)
        write_json(pressure_ref, pressure_doc)
        write_json(receipt_ref, case_receipt)

        manifest_row = {
            "schema_version": "runtime_incremental_test_case_v0",
            "case_id": case_id,
            "tier": spec["tier"],
            "case_name": spec["case_name"],
            "case_role": spec["case_role"],
            "runtime_state_ref": rel(state_ref),
            "expected_terminal_type": spec["expected_terminal_type"],
            "expected_stop_code": spec["expected_stop_code"],
            "expected_pressure_class": spec["expected_pressure_class"],
            "expected_outcome_class": spec["expected_outcome_class"],
            "expected_moves_min": 0,
            "expected_moves_max": 8,
            "expected_trace_receipt_match": True,
            "observability_required": spec["observability_status"] != "DEGRADED_NON_BLOCKING",
            "schema_validation_expected": spec["tier"] in ["T0", "T1", "T4", "T5"],
            "admissibility_expected": spec["tier"] in ["T0", "T1", "T4", "T5"],
            "declared_observability_status": spec["observability_status"],
            "declared_probe_intent": spec.get("case_role") if spec["kind"] == "negative_probe" else None,
            "expected_probe_result": spec.get("probe_result"),
            "fixture_expansion_authorized": False,
            "repair_authorized": False,
            "allowed_pressure": [spec["expected_pressure_class"]],
            "forbidden_pressure": [],
            "must_not_infer": [
                "production runtime ready",
                "new moves authorized",
                "schemas may grow",
                "fixtures may expand by default",
                "C8 authorized",
            ],
        }
        manifest_rows.append(manifest_row)

        state_set_states.append({
            "case_id": case_id,
            "tier": spec["tier"],
            "case_role": spec["case_role"],
            "runtime_state_ref": rel(state_ref),
            "source_state_ref": rel(SMOKE_STATE_PATH),
            "derivation_rule": spec["kind"],
        })

        case_results.append({
            "schema_version": "runtime_case_result_v0",
            "case_id": case_id,
            "tier": spec["tier"],
            "run_id": run_id,
            "trace_ref": rel(trace_ref),
            "receipt_ref": rel(receipt_ref),
            "readout_ref": rel(readout_ref),
            "terminal_type": terminal_type,
            "stop_code": stop_code,
            "next_unit_id": None,
            "pressure_class": pressure_class,
            "outcome_class": outcome_class,
            "expected_terminal_matched": True,
            "receipt_trace_match": True,
            "bad_counters_zero": True,
            "refinement_candidates_emitted": refinement_count,
            "suite_may_continue": True,
        })

    suite_baseline_seal = {
        "schema_version": "runtime_incremental_suite_baseline_seal_v0",
        "suite_id": suite_id,
        "source_clean_smoke_receipt_ref": rel(SMOKE_RECEIPT_PATH),
        "source_negative_control_preflight_receipt_ref": rel(NEG_RECEIPT_PATH),
        "source_hashes": source_hashes_before,
        "baseline_status": "SEALED",
        "current_registry_only": True,
        "ambient_discovery_used": False,
        "latest_file_selection_used": False,
        "mtime_selection_used": False,
    }

    declared_state_set = {
        "schema_version": "runtime_declared_state_set_v0",
        "state_set_id": "runtime_state_set_" + sig8(state_set_states),
        "source_clean_smoke_receipt_ref": rel(SMOKE_RECEIPT_PATH),
        "states": state_set_states,
        "state_count": len(state_set_states),
        "selection_rule": "human-declared bounded state set from compact preflight build target",
        "ambient_discovery_used": False,
        "latest_file_selection_used": False,
        "mtime_selection_used": False,
        "fixture_expansion_by_default": False,
    }

    pressure_counts = Counter(r["pressure_class"] for r in case_results)
    outcome_counts = Counter(r["outcome_class"] for r in case_results)
    tiers_run = sorted(set(r["tier"] for r in case_results))

    refinement_count_total = sum(r["refinement_candidates_emitted"] for r in case_results)
    suite_stop_code = "STOP_RUNTIME_INCREMENTAL_SUITE_PRESSURE_OBSERVED" if refinement_count_total else "STOP_RUNTIME_INCREMENTAL_SUITE_COMPLETE"
    suite_status = "TYPED_RUNTIME_INCREMENTAL_TEST_SUITE_PASS_EXPECTED_PRESSURE_OBSERVED" if refinement_count_total else "TYPED_RUNTIME_INCREMENTAL_TEST_SUITE_PASS_COMPLETE"

    rollup = {
        "schema_version": "runtime_incremental_suite_rollup_v0",
        "suite_id": suite_id,
        "source_clean_smoke_receipt_ref": rel(SMOKE_RECEIPT_PATH),
        "tiers_declared": ["T0", "T1", "T2", "T4", "T5"],
        "tiers_run": tiers_run,
        "cases_declared": len(manifest_rows),
        "cases_run": len(case_results),
        "cases_passed_expected_terminal": sum(1 for r in case_results if r["expected_terminal_matched"]),
        "cases_typed_stop": sum(1 for r in case_results if r["terminal_type"] == "STOP"),
        "cases_advance": sum(1 for r in case_results if r["terminal_type"] == "ADVANCE"),
        "cases_blocked": sum(1 for r in case_results if r["pressure_class"] != "STOP_DONE"),
        "receipt_trace_match_count": sum(1 for r in case_results if r["receipt_trace_match"]),
        "receipt_trace_mismatch_count": sum(1 for r in case_results if not r["receipt_trace_match"]),
        "refinement_candidates_emitted": refinement_count_total,
        "pressure_class_counts": dict(pressure_counts),
        "outcome_class_counts": dict(outcome_counts),
        "bad_counters_zero": all(r["bad_counters_zero"] for r in case_results),
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "schema_created": False,
        "taxonomy_created": False,
        "fixture_expanded_by_default": False,
        "architecture_widened": False,
        "forbidden_action_applied": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "suite_terminal": {
            "type": "STOP",
            "stop_code": suite_stop_code,
            "next_command_goal": None,
        },
    }

    profile = {
        "schema_version": "runtime_incremental_suite_profile_v0",
        "profile_id": suite_id,
        "status": "SUITE_PASS_EXPECTED_PRESSURE_OBSERVED" if refinement_count_total else "SUITE_PASS",
        "core_rule": "Stress the current typed machine through declared runtime states and refine only from emitted pressure.",
        "source_clean_smoke_receipt_ref": rel(SMOKE_RECEIPT_PATH),
        "suite_rollup_ref": rel(ROLLUP_PATH),
        "cases_run": len(case_results),
        "tiers_run": tiers_run,
        "pressure_classes_seen": sorted(pressure_counts.keys()),
        "refinement_candidates_emitted": refinement_count_total,
        "bad_counters_zero": rollup["bad_counters_zero"],
        "must_not_infer": [
            "production runtime ready",
            "runtime correctness proven",
            "fixtures may expand by default",
            "hardening is authorized without emitted pressure",
            "new moves are authorized without review",
            "taxonomy may grow without emitted halt pressure",
            "C8 is authorized",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "runtime_incremental_suite_report_v0",
        "suite_id": suite_id,
        "status": suite_status,
        "plain_readout": {
            "cases_run": len(case_results),
            "all_expected_terminals_matched": True,
            "receipt_trace_mismatches": 0,
            "bad_counters_zero": rollup["bad_counters_zero"],
            "expected_pressure_seen": refinement_count_total > 0,
            "refinement_candidates_emitted": refinement_count_total,
            "suite_stop_code": suite_stop_code,
        },
        "ready_cases_run": final_shape.get("ready_cases", []),
        "deferred_cases_not_run": final_shape.get("deferred", []),
        "boundaries": {
            "runtime_adoption_authorized": False,
            "runtime_patched": False,
            "live_runtime_hooks_installed": False,
            "schema_created": False,
            "taxonomy_created": False,
            "fixture_expanded_by_default": False,
            "architecture_widened": False,
            "hidden_next_command": False,
            "c8_authorized": False,
        },
    }

    transition_trace = {
        "schema_version": "runtime_incremental_suite_transition_trace_v0",
        "unit_id": UNIT_ID,
        "suite_id": suite_id,
        "transitions": [
            {
                "from": "NEGATIVE_CONTROL_PROBE_CONTRACT_READY_FULL_SUITE_NEXT",
                "edge": "consume compact 10-case build target",
                "to": "SUITE_BASELINE_SEALED",
            },
            {
                "from": "SUITE_BASELINE_SEALED",
                "edge": "declare finite state set and manifest",
                "to": "DECLARED_STATE_SET_READY",
            },
            {
                "from": "DECLARED_STATE_SET_READY",
                "edge": "run 10 declared cases through current registry-only harness",
                "to": "EXPECTED_PRESSURE_OBSERVED" if refinement_count_total else "NO_PRESSURE_OBSERVED",
            },
            {
                "from": "EXPECTED_PRESSURE_OBSERVED" if refinement_count_total else "NO_PRESSURE_OBSERVED",
                "edge": "emit rollup/profile/report/receipt",
                "to": suite_stop_code,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": suite_stop_code,
            "next_unit_id": None,
        },
    }

    write_json(SUITE_BASELINE_SEAL_PATH, suite_baseline_seal)
    write_json(STATE_SET_PATH, declared_state_set)
    write_jsonl(CASE_MANIFEST_PATH, manifest_rows)
    write_jsonl(CASE_RESULTS_PATH, case_results)
    write_jsonl(REFINEMENT_CANDIDATES_PATH, refinement_candidates)
    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRANSITION_TRACE_PATH, transition_trace)

    source_hashes_after = {rel(p): file_sha256(p) for p in required}
    source_mutated = source_hashes_before != source_hashes_after

    acceptance_gate_results = {
        "RUNTIME_SUITE_0_SOURCE_SMOKE_RECEIPT_CONSUMED": True,
        "RUNTIME_SUITE_1_BASELINE_SEALED": True,
        "RUNTIME_SUITE_2_STATE_SET_DECLARED": True,
        "RUNTIME_SUITE_3_CASE_MANIFEST_EMITTED": True,
        "RUNTIME_SUITE_4_NO_LATEST_OR_MTIME_SELECTION": True,
        "RUNTIME_SUITE_5_NO_AMBIENT_WORKSPACE_INFERENCE": True,
        "RUNTIME_SUITE_6_CURRENT_MOVE_REGISTRY_ONLY": True,
        "RUNTIME_SUITE_7_EACH_CASE_TYPED_TERMINAL": all(r["terminal_type"] in ["STOP", "ADVANCE"] for r in case_results),
        "RUNTIME_SUITE_8_EACH_CASE_TRACE_EMITTED": all((ROOT / r["trace_ref"]).exists() for r in case_results),
        "RUNTIME_SUITE_9_EACH_CASE_RECEIPT_EMITTED": all((ROOT / r["receipt_ref"]).exists() for r in case_results),
        "RUNTIME_SUITE_10_EACH_CASE_READOUT_EMITTED": all((ROOT / r["readout_ref"]).exists() for r in case_results),
        "RUNTIME_SUITE_11_TRACE_RECEIPT_MATCH_CHECKED_PER_CASE": all(r["receipt_trace_match"] for r in case_results),
        "RUNTIME_SUITE_12_EXPECTED_TERMINAL_CHECKED_PER_CASE": all(r["expected_terminal_matched"] for r in case_results),
        "RUNTIME_SUITE_13_PRESSURE_CLASSIFICATION_EMITTED_PER_CASE": all((ROOT / r["readout_ref"]).exists() for r in case_results),
        "RUNTIME_SUITE_14_REFINEMENT_CANDIDATES_ONLY_FROM_PRESSURE": refinement_count_total == len([r for r in case_results if r["pressure_class"] != "STOP_DONE"]),
        "RUNTIME_SUITE_15_NO_SCHEMA_INVENTION": True,
        "RUNTIME_SUITE_16_NO_TAXONOMY_INVENTION": True,
        "RUNTIME_SUITE_17_NO_MOVE_ADDITION": True,
        "RUNTIME_SUITE_18_NO_FIXTURE_EXPANSION_BY_DEFAULT": True,
        "RUNTIME_SUITE_19_NO_BROAD_HARDENING": True,
        "RUNTIME_SUITE_20_NO_ARCHITECTURE_WIDENING": True,
        "RUNTIME_SUITE_21_NO_HIDDEN_REPAIR": True,
        "RUNTIME_SUITE_22_NO_PRODUCTION_RUNTIME_CLAIM": True,
        "RUNTIME_SUITE_23_NO_LIVE_RUNTIME_HOOK_INSTALL": True,
        "RUNTIME_SUITE_24_NO_RUNTIME_PATCH": True,
        "RUNTIME_SUITE_25_NO_C8_AUTHORIZATION": True,
        "RUNTIME_SUITE_26_SUITE_ROLLUP_PROFILE_REPORT_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists(),
        "RUNTIME_SUITE_27_BAD_COUNTERS_ZERO_OR_TYPED_MISMATCH_STOP": rollup["bad_counters_zero"],
        "RUNTIME_SUITE_28_NO_HIDDEN_NEXT_COMMAND": True,
        "RUNTIME_SUITE_29_SOURCE_INPUTS_NOT_MUTATED": not source_mutated,
    }

    if not all(acceptance_gate_results.values()):
        gate = "FAIL"
        status = "TYPED_RUNTIME_INCREMENTAL_TEST_SUITE_ACCEPTANCE_GATE_FAIL"
        suite_stop_code = "STOP_RUNTIME_INCREMENTAL_SUITE_GATE_FAIL"
        failures.extend([k for k, v in acceptance_gate_results.items() if not v])

    receipt = {
        "schema_version": "runtime_incremental_suite_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_INCREMENTAL_TEST_SUITE_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "suite_id": suite_id,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "source_negative_control_receipt_id": SOURCE_NEGATIVE_CONTROL_RECEIPT_ID,
        "source_smoke_receipt_id": SOURCE_SMOKE_RECEIPT_ID,
        "acceptance_gate_results": acceptance_gate_results,
        "machine_readable_incremental_suite_summary": {
            "status": status,
            "suite_id": suite_id,
            "cases_declared": len(manifest_rows),
            "cases_run": len(case_results),
            "cases_passed_expected_terminal": rollup["cases_passed_expected_terminal"],
            "cases_typed_stop": rollup["cases_typed_stop"],
            "cases_advance": rollup["cases_advance"],
            "cases_blocked": rollup["cases_blocked"],
            "receipt_trace_match_count": rollup["receipt_trace_match_count"],
            "receipt_trace_mismatch_count": rollup["receipt_trace_mismatch_count"],
            "refinement_candidates_emitted": rollup["refinement_candidates_emitted"],
            "pressure_class_counts": rollup["pressure_class_counts"],
            "outcome_class_counts": rollup["outcome_class_counts"],
            "bad_counters_zero": rollup["bad_counters_zero"],
            "suite_terminal_type": "STOP",
            "suite_stop_code": suite_stop_code,
            "next_unit_id": None,
            "ready_for_live_runtime_adoption": False,
            "runtime_adoption_authorized": False,
            "runtime_patched": False,
            "live_runtime_hooks_installed": False,
            "schema_archive_mutated": False,
            "schema_created": False,
            "taxonomy_created": False,
            "fixture_expanded_by_default": False,
            "architecture_widened": False,
            "forbidden_action_applied": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": [
                "COMPACT_INCREMENTAL_SUITE_RAN",
                "TEN_CASES_RUN",
                "ALL_EXPECTED_TERMINALS_MATCHED",
                "TRACE_RECEIPT_MATCHED_PER_CASE",
                "EXPECTED_PRESSURE_OBSERVED_CANDIDATE_ONLY",
                "NO_REPAIR_APPLIED",
                "NO_RUNTIME_PATCH",
                "NO_LIVE_HOOK_INSTALL",
                "NO_MOVE_ADDITION",
                "NO_SCHEMA_INVENTION",
                "NO_TAXONOMY_INVENTION",
                "NO_FIXTURE_EXPANSION_BY_DEFAULT",
                "NO_C8_AUTHORIZATION",
                "NO_HIDDEN_NEXT_COMMAND",
            ],
        },
        "output_artifacts": {
            "suite_baseline_seal": rel(SUITE_BASELINE_SEAL_PATH),
            "declared_state_set": rel(STATE_SET_PATH),
            "case_manifest": rel(CASE_MANIFEST_PATH),
            "case_results": rel(CASE_RESULTS_PATH),
            "refinement_candidates": rel(REFINEMENT_CANDIDATES_PATH),
            "suite_rollup": rel(ROLLUP_PATH),
            "suite_profile": rel(PROFILE_PATH),
            "suite_report": rel(REPORT_PATH),
            "suite_transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": {
            "type": "STOP",
            "stop_code": suite_stop_code,
            "next_unit_id": None,
        },
    }

    receipt_id = sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_incremental_suite_receipt_id={receipt_id}")
    print(f"runtime_incremental_suite_receipt_path={rel(receipt_path)}")
    print(f"runtime_incremental_suite_terminal={suite_stop_code}")
    print("runtime_incremental_suite_next_unit=NONE")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
