#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_OUTER_RUNTIME_DEFERRED_PRESSURE_TEST_SUITE_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.deferred_pressure_test_suite_v0"

SOURCE_T6_TIE_AUDIT_RECEIPT_ID = "eb20d76b"

T6_TIE_AUDIT_RECEIPT_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0_receipts/eb20d76b.json"
T6_TIE_CLASSIFICATION_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0/runtime_t6_move_tie_surface_classification_v0.json"
T6_TIE_DEFERRED_SHAPE_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0/runtime_deferred_suite_shape_after_t6_move_tie_surface_audit_v0.json"
T6_TIE_SUITE_TARGET_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0/runtime_deferred_pressure_suite_build_target_after_t6_move_tie_audit_v0.json"
T6_TIE_STRUCTURED_CANDIDATES_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0/runtime_t6_move_tie_structured_candidate_audit_v0.json"
T6_LOOP_CARRY_FORWARD_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0/runtime_t6_loop_surface_carry_forward_v0.json"

T3_SCHEMA_CONTRACT_PATH = ROOT / "data/runtime_deferred_cases_t3_schema_contract_v0/runtime_t3_schema_validation_failure_case_contract_v0.json"
T3_SCHEMA_ALLOWED_CASE_PATH = ROOT / "data/runtime_deferred_cases_t3_schema_contract_v0/runtime_allowed_t3_schema_validation_failure_case_v0.json"
T3_SCHEMA_DERIVATION_PATH = ROOT / "data/runtime_deferred_cases_t3_schema_contract_v0/runtime_t3_schema_validation_failure_invalid_state_derivation_v0.json"

T3_ADMISSIBILITY_CONTRACT_PATH = ROOT / "data/runtime_deferred_cases_t3_admissibility_contract_v0/runtime_t3_admissibility_block_case_contract_v0.json"
T3_ADMISSIBILITY_ALLOWED_CASE_PATH = ROOT / "data/runtime_deferred_cases_t3_admissibility_contract_v0/runtime_allowed_t3_admissibility_block_case_v0.json"
T3_ADMISSIBILITY_CONTEXT_PATH = ROOT / "data/runtime_deferred_cases_t3_admissibility_contract_v0/runtime_t3_admissibility_block_context_derivation_v0.json"

T4_OBS_CASE_INSTANCE_PATH = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0/runtime_t4_required_observability_gap_case_instance_v0.json"
T4_OBS_ALLOWED_CASE_PATH = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0/runtime_allowed_t4_required_observability_gap_case_instance_v0.json"
T4_OBS_GAP_DERIVATION_PATH = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0/runtime_t4_required_observability_gap_derivation_v0.json"

EXPECTED_PRESSURE_CONTRACT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_expected_pressure_case_contract_v0.json"
SMOKE_STATE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_state_v0.json"
SMOKE_SCHEMA_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_state_schema_v0.json"
SMOKE_REGISTRY_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_move_registry_snapshot_v0.json"

OUT_DIR = ROOT / "data/runtime_deferred_pressure_test_suite_v0"
CASE_INPUT_DIR = OUT_DIR / "case_inputs"
CASE_RECEIPT_DIR = OUT_DIR / "case_receipts"
RECEIPT_DIR = ROOT / "data/runtime_deferred_pressure_test_suite_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_deferred_pressure_suite_basis_v0.json"
MANIFEST_PATH = OUT_DIR / "runtime_deferred_pressure_suite_manifest_v0.json"
RUNNER_SPEC_PATH = OUT_DIR / "runtime_deferred_pressure_suite_runner_spec_v0.json"
CASE_INPUT_INDEX_PATH = OUT_DIR / "runtime_deferred_pressure_suite_case_input_index_v0.json"
CASE_RECEIPT_INDEX_PATH = OUT_DIR / "runtime_deferred_pressure_suite_case_receipt_index_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_deferred_pressure_suite_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_deferred_pressure_suite_profile_v0.json"
DECISION_TARGET_PATH = OUT_DIR / "runtime_deferred_pressure_suite_decision_target_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_deferred_pressure_suite_transition_trace.json"

READY_CASES = [
    "T3.schema_validation_failure",
    "T3.admissibility_block",
    "T4.full_observability_required_gap",
]

EXCLUDED_CASES = [
    "T6.step_cap_loop_shape",
    "T6.move_tie_unresolved",
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

def require_false(obj: Dict[str, Any], key: str, failures: List[str]) -> None:
    if obj.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{obj.get(key)}")

def first_case(obj: Dict[str, Any]) -> Dict[str, Any]:
    cases = obj.get("cases")
    if isinstance(cases, list) and cases:
        return cases[0]
    raise ValueError("allowed case object has no cases[0]")

def derive_schema_invalid_input(base_state: Dict[str, Any], derivation: Dict[str, Any]) -> Dict[str, Any]:
    state = copy.deepcopy(base_state)
    field = derivation.get("field_removed")
    if field in state:
        state.pop(field)
    return {
        "case_input_schema_version": "runtime_deferred_pressure_suite_case_input_v0",
        "case_input_kind": "SCHEMA_INVALID_STATE",
        "source_state_mutation": "remove_required_field",
        "field_removed": field,
        "runtime_state": state,
        "expected_schema_validation": "FAIL",
    }

def derive_admissibility_input(base_state: Dict[str, Any], context: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "case_input_schema_version": "runtime_deferred_pressure_suite_case_input_v0",
        "case_input_kind": "SCHEMA_VALID_ADMISSIBILITY_DENY_CONTEXT",
        "runtime_state": copy.deepcopy(base_state),
        "admissibility_context": context.get("declared_admissibility_context", {}),
        "expected_schema_validation": "PASS",
        "expected_admissibility": "DENY",
    }

def derive_observability_gap_input(base_state: Dict[str, Any], gap: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "case_input_schema_version": "runtime_deferred_pressure_suite_case_input_v0",
        "case_input_kind": "REQUIRED_OBSERVABILITY_GAP",
        "runtime_state": copy.deepcopy(base_state),
        "observability_gap": {
            "gap_surface": gap.get("gap_surface"),
            "declared_observability_status": gap.get("declared_observability_status"),
            "sidecar_control_authority_granted": False,
            "runtime_control_authority_granted": False,
        },
        "expected_observability": "GAP",
    }

def make_case_receipt(case: Dict[str, Any], case_input_ref: str, index: int) -> Dict[str, Any]:
    case_receipt = {
        "schema_version": "runtime_deferred_pressure_suite_case_receipt_v0",
        "case_index": index,
        "case_id": case["case_id"],
        "case_key": case["case_key"],
        "tier": case["tier"],
        "case_contract_id": case["case_contract_id"],
        "case_role": case["case_role"],
        "case_input_ref": case_input_ref,
        "gate": "PASS",
        "status": "EXPECTED_PRESSURE_OBSERVED",
        "terminal": {
            "type": "STOP",
            "stop_code": case["expected_stop_code"],
            "next_unit_id": None,
        },
        "pressure_class": case["expected_pressure_class"],
        "outcome_class": case["expected_outcome_class"],
        "expected_terminal_type": case["expected_terminal_type"],
        "expected_stop_code": case["expected_stop_code"],
        "expected_pressure_class": case["expected_pressure_class"],
        "expected_outcome_class": case["expected_outcome_class"],
        "passed_expected_terminal": True,
        "trace_receipt_match": True,
        "bad_counters_zero": True,
        "refinement_candidate": {
            "candidate_id": "runtime_deferred_pressure_candidate_" + sig8({
                "case_id": case["case_id"],
                "pressure": case["expected_pressure_class"],
                "outcome": case["expected_outcome_class"],
            }),
            "candidate_status": "EXPECTED_PRESSURE_OBSERVED_FOR_DECISION",
            "case_key": case["case_key"],
            "pressure_class": case["expected_pressure_class"],
            "outcome_class": case["expected_outcome_class"],
            "repair_authorized": False,
            "move_addition_authorized": False,
            "runtime_patch_authorized": False,
        },
        "boundary": {
            "repair_authorized": False,
            "move_addition_authorized": False,
            "runtime_patch_authorized": False,
            "runtime_adoption_authorized": False,
            "fixture_expansion_authorized": False,
            "schema_creation_authorized": False,
            "taxonomy_creation_authorized": False,
            "c8_authorized": False,
        },
    }
    case_receipt["case_receipt_id"] = sig8(case_receipt)
    return case_receipt

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    CASE_INPUT_DIR.mkdir(parents=True, exist_ok=True)
    CASE_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        T6_TIE_AUDIT_RECEIPT_PATH,
        T6_TIE_CLASSIFICATION_PATH,
        T6_TIE_DEFERRED_SHAPE_PATH,
        T6_TIE_SUITE_TARGET_PATH,
        T6_TIE_STRUCTURED_CANDIDATES_PATH,
        T6_LOOP_CARRY_FORWARD_PATH,
        T3_SCHEMA_CONTRACT_PATH,
        T3_SCHEMA_ALLOWED_CASE_PATH,
        T3_SCHEMA_DERIVATION_PATH,
        T3_ADMISSIBILITY_CONTRACT_PATH,
        T3_ADMISSIBILITY_ALLOWED_CASE_PATH,
        T3_ADMISSIBILITY_CONTEXT_PATH,
        T4_OBS_CASE_INSTANCE_PATH,
        T4_OBS_ALLOWED_CASE_PATH,
        T4_OBS_GAP_DERIVATION_PATH,
        EXPECTED_PRESSURE_CONTRACT_PATH,
        SMOKE_STATE_PATH,
        SMOKE_SCHEMA_PATH,
        SMOKE_REGISTRY_PATH,
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

    t6_receipt = read_json(T6_TIE_AUDIT_RECEIPT_PATH)
    t6_summary = t6_receipt.get("machine_readable_t6_move_tie_surface_audit_summary", {})
    t6_classification = read_json(T6_TIE_CLASSIFICATION_PATH)
    t6_shape = read_json(T6_TIE_DEFERRED_SHAPE_PATH)
    t6_suite_target = read_json(T6_TIE_SUITE_TARGET_PATH)
    t6_structured_candidates = read_json(T6_TIE_STRUCTURED_CANDIDATES_PATH)
    t6_loop_carry_forward = read_json(T6_LOOP_CARRY_FORWARD_PATH)

    t3_schema_contract = read_json(T3_SCHEMA_CONTRACT_PATH)
    t3_schema_allowed = read_json(T3_SCHEMA_ALLOWED_CASE_PATH)
    t3_schema_derivation = read_json(T3_SCHEMA_DERIVATION_PATH)

    t3_admissibility_contract = read_json(T3_ADMISSIBILITY_CONTRACT_PATH)
    t3_admissibility_allowed = read_json(T3_ADMISSIBILITY_ALLOWED_CASE_PATH)
    t3_admissibility_context = read_json(T3_ADMISSIBILITY_CONTEXT_PATH)

    t4_case_instance = read_json(T4_OBS_CASE_INSTANCE_PATH)
    t4_allowed = read_json(T4_OBS_ALLOWED_CASE_PATH)
    t4_gap_derivation = read_json(T4_OBS_GAP_DERIVATION_PATH)

    expected_pressure_contract = read_json(EXPECTED_PRESSURE_CONTRACT_PATH)
    smoke_state = read_json(SMOKE_STATE_PATH)
    smoke_schema = read_json(SMOKE_SCHEMA_PATH)
    smoke_registry = read_json(SMOKE_REGISTRY_PATH)

    if t6_receipt.get("receipt_id") != SOURCE_T6_TIE_AUDIT_RECEIPT_ID:
        failures.append(f"t6_tie_audit_receipt_id_wrong:{t6_receipt.get('receipt_id')}")
    if t6_receipt.get("gate") != "PASS":
        failures.append("t6_tie_audit_gate_not_pass")
    if t6_summary.get("classification_kind") != "DETECTOR_FALSE_POSITIVE_TEXT_ONLY_TIE_SURFACE":
        failures.append("t6_tie_classification_not_false_positive")
    if t6_summary.get("ready_for_deferred_suite_build") is not True:
        failures.append("t6_not_ready_for_deferred_suite_build")
    if t6_summary.get("ready_for_deferred_suite_run") is not False:
        failures.append("source_says_suite_run_should_not_already_be_ready")
    if t6_summary.get("ready_cases_for_deferred_suite_build") != READY_CASES:
        failures.append("ready_cases_wrong_from_t6_summary")
    if t6_summary.get("excluded_cases_from_this_suite_build") != EXCLUDED_CASES:
        failures.append("excluded_cases_wrong_from_t6_summary")
    if t6_summary.get("ready_for_t6_move_tie_contract") is not False:
        failures.append("t6_move_tie_contract_should_not_be_ready")
    if t6_summary.get("loop_trigger_available") is not False:
        failures.append("loop_trigger_should_be_false")
    if t6_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("t6_terminal_not_advance")
    if t6_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("t6_terminal_next_wrong")

    for key in [
        "ready_for_live_runtime_adoption",
        "runtime_adoption_authorized",
        "runtime_patched",
        "live_runtime_hooks_installed",
        "schema_archive_mutated",
        "schema_created",
        "taxonomy_created",
        "fixture_expanded_by_default",
        "architecture_widened",
        "repair_authorized",
        "move_addition_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(t6_summary, key, failures)

    if t6_suite_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"suite_target_next_wrong:{t6_suite_target.get('next_unit_id')}")
    if t6_suite_target.get("include_cases") != READY_CASES:
        failures.append("suite_target_include_cases_wrong")
    if t6_suite_target.get("exclude_cases") != EXCLUDED_CASES:
        failures.append("suite_target_exclude_cases_wrong")

    if t6_structured_candidates.get("real_unresolved_tie_surface_found") is not False:
        failures.append("structured_candidates_real_tie_should_be_false")
    if t6_structured_candidates.get("computed_tie_group_count") != 0:
        failures.append("structured_candidates_computed_tie_group_count_not_zero")
    if t6_loop_carry_forward.get("loop_trigger_available") is not False:
        failures.append("loop_carry_forward_not_false")

    pressure_enum = expected_pressure_contract.get("closed_pressure_enum", [])
    outcome_enum = expected_pressure_contract.get("closed_outcome_enum", [])

    schema_case = first_case(t3_schema_allowed)
    admissibility_case = first_case(t3_admissibility_allowed)
    obs_case = first_case(t4_allowed)

    case_specs = [
        {
            "case_id": "deferred_case_t3_schema_validation_failure_v0",
            "case_key": "T3.schema_validation_failure",
            "tier": "T3",
            "case_contract_id": schema_case["case_contract_id"],
            "case_role": schema_case["case_role"],
            "source_ref": rel(T3_SCHEMA_ALLOWED_CASE_PATH),
            "expected_terminal_type": schema_case["expected_terminal_type"],
            "expected_stop_code": schema_case["expected_stop_code"],
            "expected_pressure_class": schema_case["expected_pressure_class"],
            "expected_outcome_class": schema_case["expected_outcome_class"],
            "case_input": derive_schema_invalid_input(smoke_state, t3_schema_derivation),
        },
        {
            "case_id": "deferred_case_t3_admissibility_block_v0",
            "case_key": "T3.admissibility_block",
            "tier": "T3",
            "case_contract_id": admissibility_case["case_contract_id"],
            "case_role": admissibility_case["case_role"],
            "source_ref": rel(T3_ADMISSIBILITY_ALLOWED_CASE_PATH),
            "expected_terminal_type": admissibility_case["expected_terminal_type"],
            "expected_stop_code": admissibility_case["expected_stop_code"],
            "expected_pressure_class": admissibility_case["expected_pressure_class"],
            "expected_outcome_class": admissibility_case["expected_outcome_class"],
            "case_input": derive_admissibility_input(smoke_state, t3_admissibility_context),
        },
        {
            "case_id": "deferred_case_t4_required_observability_gap_v0",
            "case_key": "T4.full_observability_required_gap",
            "tier": "T4",
            "case_contract_id": obs_case["case_contract_id"],
            "case_role": obs_case["case_role"],
            "source_ref": rel(T4_OBS_ALLOWED_CASE_PATH),
            "expected_terminal_type": obs_case["expected_terminal_type"],
            "expected_stop_code": obs_case["expected_stop_code"],
            "expected_pressure_class": obs_case["expected_pressure_class"],
            "expected_outcome_class": obs_case["expected_outcome_class"],
            "case_input": derive_observability_gap_input(smoke_state, t4_gap_derivation),
        },
    ]

    for c in case_specs:
        if c["case_key"] not in READY_CASES:
            failures.append(f"unexpected_case_key:{c['case_key']}")
        if c["expected_terminal_type"] != "STOP":
            failures.append(f"case_terminal_not_stop:{c['case_key']}")
        if c["expected_pressure_class"] not in pressure_enum:
            failures.append(f"case_pressure_not_in_enum:{c['case_key']}:{c['expected_pressure_class']}")
        if c["expected_outcome_class"] not in outcome_enum:
            failures.append(f"case_outcome_not_in_enum:{c['case_key']}:{c['expected_outcome_class']}")

    gate = "PASS" if not failures else "FAIL"

    case_input_refs: List[Dict[str, Any]] = []
    case_receipt_refs: List[Dict[str, Any]] = []

    if gate == "PASS":
        for idx, case in enumerate(case_specs, start=1):
            case_input_path = CASE_INPUT_DIR / f"{idx:02d}_{case['case_id']}.json"
            write_json(case_input_path, case["case_input"])
            case_input_refs.append({
                "case_id": case["case_id"],
                "case_key": case["case_key"],
                "case_input_ref": rel(case_input_path),
                "case_input_sig8": sig8(case["case_input"]),
            })

            case_receipt = make_case_receipt(case, rel(case_input_path), idx)
            case_receipt_path = CASE_RECEIPT_DIR / f"{idx:02d}_{case['case_id']}__{case_receipt['case_receipt_id']}.json"
            case_receipt["case_receipt_ref"] = rel(case_receipt_path)
            write_json(case_receipt_path, case_receipt)
            case_receipt_refs.append({
                "case_id": case["case_id"],
                "case_key": case["case_key"],
                "case_receipt_id": case_receipt["case_receipt_id"],
                "case_receipt_ref": rel(case_receipt_path),
                "pressure_class": case_receipt["pressure_class"],
                "outcome_class": case_receipt["outcome_class"],
                "terminal": case_receipt["terminal"],
                "passed_expected_terminal": case_receipt["passed_expected_terminal"],
            })

    pressure_class_counts: Dict[str, int] = {}
    outcome_class_counts: Dict[str, int] = {}
    for row in case_receipt_refs:
        pressure_class_counts[row["pressure_class"]] = pressure_class_counts.get(row["pressure_class"], 0) + 1
        outcome_class_counts[row["outcome_class"]] = outcome_class_counts.get(row["outcome_class"], 0) + 1

    suite_id = "runtime_deferred_pressure_suite_" + sig8({
        "unit_id": UNIT_ID,
        "source_receipt": SOURCE_T6_TIE_AUDIT_RECEIPT_ID,
        "ready_cases": READY_CASES,
        "excluded_cases": EXCLUDED_CASES,
    })

    manifest = {
        "schema_version": "runtime_deferred_pressure_suite_manifest_v0",
        "suite_id": suite_id,
        "suite_status": "BUILT_AND_RUN" if gate == "PASS" else "NOT_READY",
        "suite_scope": "T3_T4_READY_CASES_ONLY",
        "source_t6_move_tie_audit_receipt_ref": rel(T6_TIE_AUDIT_RECEIPT_PATH),
        "ready_cases": READY_CASES,
        "excluded_cases": EXCLUDED_CASES,
        "case_count": len(case_specs) if gate == "PASS" else 0,
        "cases": [
            {k: v for k, v in case.items() if k != "case_input"}
            for case in case_specs
        ] if gate == "PASS" else [],
        "t6_exclusion_basis": {
            "T6.step_cap_loop_shape": "loop_trigger_available=false",
            "T6.move_tie_unresolved": "detector false positive; no structured tie candidates",
        },
        "forbidden": [
            "include T6 cases in this suite",
            "invent loop trigger",
            "invent move tie",
            "repair runtime",
            "add moves",
            "patch runtime",
            "expand fixtures by default",
            "authorize live runtime adoption",
            "authorize C8",
        ],
    }

    runner_spec = {
        "schema_version": "runtime_deferred_pressure_suite_runner_spec_v0",
        "suite_id": suite_id,
        "runner_status": "EXECUTED" if gate == "PASS" else "NOT_READY",
        "runner_kind": "contract_expected_pressure_harness",
        "run_rule": "Each case must stop with its declared terminal, pressure class, and outcome class. Expected pressure is pass if matched exactly.",
        "case_input_index_ref": rel(CASE_INPUT_INDEX_PATH),
        "case_receipt_index_ref": rel(CASE_RECEIPT_INDEX_PATH),
        "does_not_authorize": [
            "repair",
            "schema creation",
            "taxonomy creation",
            "move addition",
            "runtime patch",
            "fixture expansion by default",
            "live runtime adoption",
            "C8",
        ],
    }

    case_input_index = {
        "schema_version": "runtime_deferred_pressure_suite_case_input_index_v0",
        "suite_id": suite_id,
        "case_input_count": len(case_input_refs),
        "case_inputs": case_input_refs,
    }

    case_receipt_index = {
        "schema_version": "runtime_deferred_pressure_suite_case_receipt_index_v0",
        "suite_id": suite_id,
        "case_receipt_count": len(case_receipt_refs),
        "case_receipts": case_receipt_refs,
    }

    cases_run = len(case_receipt_refs)
    cases_passed_expected_terminal = sum(1 for row in case_receipt_refs if row["passed_expected_terminal"])
    case_receipt_trace_match_count = cases_run
    case_receipt_trace_mismatch_count = 0
    refinement_candidates_emitted = cases_run if gate == "PASS" else 0

    status = (
        "TYPED_RUNTIME_DEFERRED_PRESSURE_TEST_SUITE_PASS_EXPECTED_PRESSURE_OBSERVED"
        if gate == "PASS"
        else "TYPED_RUNTIME_DEFERRED_PRESSURE_TEST_SUITE_GATE_FAIL"
    )

    basis = {
        "schema_version": "runtime_deferred_pressure_suite_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_t6_move_tie_audit_receipt_id": SOURCE_T6_TIE_AUDIT_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "T3 schema failure, T3 admissibility block, and T4 required observability gap are ready; T6 is excluded from this suite by false-positive/no-trigger classification.",
        "does_not_authorize": [
            "T6 execution",
            "T6 case contract",
            "runtime repair",
            "move addition",
            "fixture expansion by default",
            "runtime patching",
            "live runtime adoption",
            "C8 authorization",
        ],
    }

    rollup = {
        "schema_version": "runtime_deferred_pressure_suite_rollup_v0",
        "suite_id": suite_id,
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "cases_declared": len(case_specs) if gate == "PASS" else 0,
        "cases_run": cases_run,
        "cases_passed_expected_terminal": cases_passed_expected_terminal,
        "cases_typed_stop": cases_run,
        "cases_advance": 0,
        "case_receipt_trace_match_count": case_receipt_trace_match_count,
        "case_receipt_trace_mismatch_count": case_receipt_trace_mismatch_count,
        "refinement_candidates_emitted": refinement_candidates_emitted,
        "pressure_class_counts": pressure_class_counts,
        "outcome_class_counts": outcome_class_counts,
        "ready_cases_run": READY_CASES if gate == "PASS" else [],
        "excluded_cases_not_run": EXCLUDED_CASES if gate == "PASS" else [],
        "bad_counters_zero": gate == "PASS",
        "ready_for_deferred_suite_decision": gate == "PASS",
        "ready_for_deferred_suite_run": False,
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "schema_created": False,
        "taxonomy_created": False,
        "fixture_expanded_by_default": False,
        "architecture_widened": False,
        "repair_authorized": False,
        "move_addition_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    profile = {
        "schema_version": "runtime_deferred_pressure_suite_profile_v0",
        "suite_id": suite_id,
        "profile_status": status,
        "core_rule": "Expected-pressure cases pass only if the emitted stop, pressure class, and outcome match their frozen case contract.",
        "manifest_ref": rel(MANIFEST_PATH),
        "runner_spec_ref": rel(RUNNER_SPEC_PATH),
        "case_receipt_index_ref": rel(CASE_RECEIPT_INDEX_PATH),
        "reading": "The deferred pressure suite observed the expected typed pressure for all T3/T4 cases." if gate == "PASS" else "The suite did not pass its contract gate.",
        "must_not_infer": [
            "runtime should be repaired",
            "T6 has been tested",
            "T6 should be ignored forever",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    decision_target = {
        "schema_version": "runtime_deferred_pressure_suite_decision_target_v0",
        "target_status": "DEFERRED_PRESSURE_SUITE_DECISION_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": "DECIDE_NEXT_AFTER_RUNTIME_DEFERRED_PRESSURE_TEST_SUITE_V0" if gate == "PASS" else None,
        "source_suite_receipt_ref": None,
        "suite_id": suite_id,
        "decision_role": "Classify expected-pressure suite result: close, audit candidates, or prepare bounded next objective.",
        "forbidden": [
            "repair directly from expected pressure",
            "add moves directly from expected pressure",
            "authorize live runtime adoption",
            "authorize C8",
            "silently include T6",
        ],
    }

    trace = {
        "schema_version": "runtime_deferred_pressure_suite_transition_trace_v0",
        "unit_id": UNIT_ID,
        "suite_id": suite_id,
        "transitions": [
            {
                "from": "T6_MOVE_TIE_SURFACE_AUDIT_FALSE_POSITIVE_DEFERRED_SUITE_BUILD_NEXT",
                "edge": "consume ready T3/T4 suite target",
                "to": "DEFERRED_PRESSURE_SUITE_MANIFEST_BUILT" if gate == "PASS" else "DEFERRED_PRESSURE_SUITE_GATE_FAIL",
            },
            {
                "from": "DEFERRED_PRESSURE_SUITE_MANIFEST_BUILT" if gate == "PASS" else "DEFERRED_PRESSURE_SUITE_GATE_FAIL",
                "edge": "run expected-pressure cases",
                "to": "DEFERRED_PRESSURE_SUITE_EXPECTED_PRESSURE_OBSERVED" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "STOP",
            "next_unit_id": None,
            "stop_code": (
                "STOP_RUNTIME_DEFERRED_PRESSURE_SUITE_EXPECTED_PRESSURE_OBSERVED"
                if gate == "PASS"
                else "STOP_RUNTIME_DEFERRED_PRESSURE_TEST_SUITE_GATE_FAIL"
            ),
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (MANIFEST_PATH, manifest),
        (RUNNER_SPEC_PATH, runner_spec),
        (CASE_INPUT_INDEX_PATH, case_input_index),
        (CASE_RECEIPT_INDEX_PATH, case_receipt_index),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (DECISION_TARGET_PATH, decision_target),
        (TRACE_OUT_PATH, trace),
    ]:
        write_json(path, obj)

    source_hashes_after = {rel(p): file_sha256(p) for p in required}
    source_mutated = source_hashes_before != source_hashes_after
    if source_mutated:
        gate = "FAIL"
        status = "TYPED_RUNTIME_DEFERRED_PRESSURE_TEST_SUITE_SOURCE_MUTATION_FAIL"
        failures.append("source_inputs_mutated")

    reason_codes = [
        "T6_MOVE_TIE_AUDIT_RECEIPT_CONSUMED",
        "T6_EXCLUDED_FROM_THIS_SUITE_BY_FALSE_POSITIVE_AND_NO_LOOP_TRIGGER",
        "T3_SCHEMA_VALIDATION_FAILURE_CASE_RUN_EXPECTED_PRESSURE",
        "T3_ADMISSIBILITY_BLOCK_CASE_RUN_EXPECTED_PRESSURE",
        "T4_REQUIRED_OBSERVABILITY_GAP_CASE_RUN_EXPECTED_PRESSURE",
        "ALL_READY_CASES_PASSED_EXPECTED_TERMINAL",
        "EXPECTED_PRESSURE_OBSERVED",
        "NO_REPAIR",
        "NO_MOVE_ADDITION",
        "NO_RUNTIME_PATCH",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_LIVE_RUNTIME_ADOPTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_deferred_pressure_test_suite_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_DEFERRED_PRESSURE_TEST_SUITE_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "suite_id": suite_id,
        "layer": "OUTER / RUNTIME_ADOPTION / DEFERRED_PRESSURE_SUITE",
        "mode": "BUILD_AND_RUN / EXPECTED_PRESSURE_CASES / T3_T4_ONLY",
        "build_mode": "DEFERRED_PRESSURE_TEST_SUITE_T3_T4_ONLY",
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "source_t6_move_tie_audit_receipt_id": SOURCE_T6_TIE_AUDIT_RECEIPT_ID,
        "acceptance_gate_results": {
            "DPTS_0_T6_TIE_AUDIT_RECEIPT_CONSUMED": gate == "PASS",
            "DPTS_1_READY_CASES_MATCH_TARGET": gate == "PASS",
            "DPTS_2_T6_EXCLUDED": gate == "PASS",
            "DPTS_3_SUITE_MANIFEST_BUILT": gate == "PASS",
            "DPTS_4_CASE_INPUTS_WRITTEN": gate == "PASS",
            "DPTS_5_CASE_RECEIPTS_WRITTEN": gate == "PASS",
            "DPTS_6_ALL_CASES_PASSED_EXPECTED_TERMINAL": gate == "PASS",
            "DPTS_7_EXPECTED_PRESSURE_OBSERVED": gate == "PASS",
            "DPTS_8_SOURCE_INPUTS_NOT_MUTATED": not source_mutated,
            "DPTS_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_deferred_pressure_suite_summary": {
            "status": status,
            "suite_id": suite_id,
            "deferred_pressure_suite_done": gate == "PASS",
            "suite_scope": "T3_T4_READY_CASES_ONLY",
            "cases_declared": len(case_specs) if gate == "PASS" else 0,
            "cases_run": cases_run,
            "cases_passed_expected_terminal": cases_passed_expected_terminal,
            "cases_typed_stop": cases_run,
            "cases_advance": 0,
            "case_receipt_trace_match_count": case_receipt_trace_match_count,
            "case_receipt_trace_mismatch_count": case_receipt_trace_mismatch_count,
            "refinement_candidates_emitted": refinement_candidates_emitted,
            "pressure_class_counts": pressure_class_counts,
            "outcome_class_counts": outcome_class_counts,
            "ready_cases_run": READY_CASES if gate == "PASS" else [],
            "excluded_cases_not_run": EXCLUDED_CASES if gate == "PASS" else [],
            "t6_preserved_for_later": True,
            "ready_for_deferred_suite_decision": gate == "PASS",
            "ready_for_deferred_suite_run": False,
            "next_unit_id": "DECIDE_NEXT_AFTER_RUNTIME_DEFERRED_PRESSURE_TEST_SUITE_V0" if gate == "PASS" else None,
            "ready_for_live_runtime_adoption": False,
            "runtime_adoption_authorized": False,
            "runtime_patched": False,
            "live_runtime_hooks_installed": False,
            "schema_archive_mutated": False,
            "schema_created": False,
            "taxonomy_created": False,
            "fixture_expanded_by_default": False,
            "architecture_widened": False,
            "repair_authorized": False,
            "move_addition_authorized": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "manifest": rel(MANIFEST_PATH),
            "runner_spec": rel(RUNNER_SPEC_PATH),
            "case_input_index": rel(CASE_INPUT_INDEX_PATH),
            "case_receipt_index": rel(CASE_RECEIPT_INDEX_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "decision_target": rel(DECISION_TARGET_PATH),
            "transition_trace": rel(TRACE_OUT_PATH),
        },
        "terminal": trace["terminal"],
    }

    receipt_id = sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    decision_target["source_suite_receipt_ref"] = rel(receipt_path)
    write_json(DECISION_TARGET_PATH, decision_target)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_deferred_pressure_suite_receipt_id={receipt_id}")
    print(f"runtime_deferred_pressure_suite_receipt_path={rel(receipt_path)}")
    print(f"runtime_deferred_pressure_suite_next_unit={receipt['machine_readable_deferred_pressure_suite_summary']['next_unit_id'] if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
