#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_RUNTIME_NON_WRITING_NEGATIVE_CONTROL_PROBE_CONTRACT_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.incremental_suite.negative_control_probe_contract_v0"
NEXT_UNIT_ID = "BUILD_OUTER_RUNTIME_INCREMENTAL_TEST_SUITE_V0"

LAYER = "OUTER / RUNTIME_ADOPTION / INCREMENTAL_SUITE_PREFLIGHT"
MODE = "PREPARE_CONTRACT_ONLY / NON_WRITING_NEGATIVE_CONTROLS / NO_TEST_RUN"
BUILD_MODE = "RUNTIME_NON_WRITING_NEGATIVE_CONTROL_PROBE_CONTRACT_ONLY"

SOURCE_OBSERVABILITY_STATUS_RECEIPT_ID = "2d72c2b9"

OBS_STATUS_RECEIPT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0_receipts/2d72c2b9.json"
OBS_STATUS_CONTRACT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_observability_status_case_contract_v0.json"
ALLOWED_OBSERVABILITY_CASES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_observability_status_cases_v0.json"
CASE_MANIFEST_OBSERVABILITY_RULES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_case_manifest_observability_status_rules_v0.json"
COMPACT_SUITE_AFTER_OBSERVABILITY_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_compact_suite_shape_after_observability_status_contract_v0.json"
NEGATIVE_CONTROL_TARGET_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_negative_control_probe_contract_target_v0.json"

EXPECTED_PRESSURE_CONTRACT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_expected_pressure_case_contract_v0.json"
ALLOWED_EXPECTED_PRESSURE_CASES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_expected_pressure_cases_v0.json"
STATE_VARIANT_RULES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_declared_state_variant_rules_v0.json"
ALLOWED_STATE_VARIANT_CATALOG_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_state_variant_catalog_v0.json"
REACHABILITY_MAP_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_registry_reachability_map_v0.json"
BRANCH_GAP_INDEX_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_branch_gap_index_v0.json"

SMOKE_RECEIPT_PATH = ROOT / "data/runtime_adoption_smoke_v0_receipts/runtime_smoke_receipt_900b2eae.json"
SMOKE_REGISTRY_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_move_registry_snapshot_v0.json"
SMOKE_STATE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_state_v0.json"

OUT_DIR = ROOT / "data/runtime_incremental_suite_preflight_v0"
RECEIPT_DIR = ROOT / "data/runtime_incremental_suite_preflight_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_negative_control_probe_contract_basis_v0.json"
CONTRACT_PATH = OUT_DIR / "runtime_non_writing_negative_control_probe_contract_v0.json"
ALLOWED_NEGATIVE_CASES_PATH = OUT_DIR / "runtime_allowed_non_writing_negative_control_cases_v0.json"
FORBIDDEN_NEGATIVE_ACTIONS_PATH = OUT_DIR / "runtime_forbidden_negative_control_probe_actions_v0.json"
CASE_MANIFEST_NEGATIVE_RULES_PATH = OUT_DIR / "runtime_case_manifest_negative_control_probe_rules_v0.json"
FINAL_SUITE_SHAPE_PATH = OUT_DIR / "runtime_compact_incremental_suite_final_shape_v0.json"
BUILD_TARGET_PATH = OUT_DIR / "runtime_incremental_suite_build_target_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_negative_control_probe_contract_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_negative_control_probe_contract_profile_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_negative_control_probe_contract_transition_trace.json"

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
        OBS_STATUS_RECEIPT_PATH,
        OBS_STATUS_CONTRACT_PATH,
        ALLOWED_OBSERVABILITY_CASES_PATH,
        CASE_MANIFEST_OBSERVABILITY_RULES_PATH,
        COMPACT_SUITE_AFTER_OBSERVABILITY_PATH,
        NEGATIVE_CONTROL_TARGET_PATH,
        EXPECTED_PRESSURE_CONTRACT_PATH,
        ALLOWED_EXPECTED_PRESSURE_CASES_PATH,
        STATE_VARIANT_RULES_PATH,
        ALLOWED_STATE_VARIANT_CATALOG_PATH,
        REACHABILITY_MAP_PATH,
        BRANCH_GAP_INDEX_PATH,
        SMOKE_RECEIPT_PATH,
        SMOKE_REGISTRY_PATH,
        SMOKE_STATE_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    obs_receipt = read_json(OBS_STATUS_RECEIPT_PATH)
    obs_summary = obs_receipt.get("machine_readable_observability_status_summary", {})
    obs_contract = read_json(OBS_STATUS_CONTRACT_PATH)
    allowed_obs_cases = read_json(ALLOWED_OBSERVABILITY_CASES_PATH)
    compact_after_obs = read_json(COMPACT_SUITE_AFTER_OBSERVABILITY_PATH)
    target = read_json(NEGATIVE_CONTROL_TARGET_PATH)
    expected_pressure_contract = read_json(EXPECTED_PRESSURE_CONTRACT_PATH)
    allowed_expected_pressure = read_json(ALLOWED_EXPECTED_PRESSURE_CASES_PATH)
    state_variant_rules = read_json(STATE_VARIANT_RULES_PATH)
    allowed_state_variants = read_json(ALLOWED_STATE_VARIANT_CATALOG_PATH)
    reachability_map = read_json(REACHABILITY_MAP_PATH)
    branch_gap_index = read_json(BRANCH_GAP_INDEX_PATH)
    smoke_receipt = read_json(SMOKE_RECEIPT_PATH)
    smoke_registry = read_json(SMOKE_REGISTRY_PATH)
    smoke_state = read_json(SMOKE_STATE_PATH)

    if obs_receipt.get("receipt_id") != SOURCE_OBSERVABILITY_STATUS_RECEIPT_ID:
        failures.append(f"observability_receipt_id_wrong:{obs_receipt.get('receipt_id')}")
    if obs_receipt.get("gate") != "PASS":
        failures.append("observability_gate_not_pass")
    if obs_summary.get("ready_for_negative_control_probe_contract") is not True:
        failures.append("observability_not_ready_for_negative_control_probe_contract")
    if obs_summary.get("ready_for_full_test_batch") is not False:
        failures.append("full_test_batch_should_not_be_ready_yet")
    if obs_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("observability_terminal_not_advance")
    if obs_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("observability_terminal_next_wrong")

    if target.get("target_status") != "NEGATIVE_CONTROL_PROBE_CONTRACT_NEXT":
        failures.append(f"target_status_wrong:{target.get('target_status')}")
    if target.get("next_unit_id") != UNIT_ID:
        failures.append(f"target_next_unit_wrong:{target.get('next_unit_id')}")

    for key in [
        "runtime_adoption_authorized",
        "runtime_patched",
        "live_runtime_hooks_installed",
        "schema_archive_mutated",
        "schema_created",
        "taxonomy_created",
        "fixture_expanded_by_default",
        "architecture_widened",
        "sidecar_control_authority_granted",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(obs_summary, key, failures)

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_RUNTIME_NON_WRITING_NEGATIVE_CONTROL_PROBE_CONTRACT_READY_FULL_SUITE_NEXT" if gate == "PASS" else "TYPED_RUNTIME_NON_WRITING_NEGATIVE_CONTROL_PROBE_CONTRACT_GATE_FAIL"

    contract = {
        "schema_version": "runtime_non_writing_negative_control_probe_contract_v0",
        "contract_status": "FROZEN_FOR_INCREMENTAL_SUITE_V0" if gate == "PASS" else "NOT_READY",
        "source_observability_status_contract_ref": rel(OBS_STATUS_CONTRACT_PATH),
        "core_rule": "Negative controls are declared non-writing probes. They prove forbidden behavior is rejected or remains unapplied without performing the forbidden action.",
        "probe_execution_rule": "A probe records intent, expected rejection, and zero write counters; it must not mutate runtime, registry, schemas, taxonomy, fixtures, prior receipts, live hooks, or control path.",
        "negative_control_result_enum": [
            "FORBIDDEN_ACTION_REJECTED_NON_WRITING",
            "FORBIDDEN_ACTION_NOT_APPLIED",
            "FORBIDDEN_ACTION_TYPED_STOP",
            "NEGATIVE_CONTROL_PROBE_GATE_FAIL",
        ],
        "required_zero_counters": [
            "unregistered_move_applied_count",
            "hidden_repair_count",
            "schema_invented_count",
            "taxonomy_invented_count",
            "fixture_expanded_by_default_count",
            "architecture_widened_count",
            "ambient_workspace_inference_count",
            "latest_file_selection_count",
            "mtime_selection_count",
            "trace_missing_count",
            "implicit_continuation_count",
            "production_runtime_claim_count",
            "broad_hardening_count",
            "runtime_patch_count",
            "live_hook_install_count",
            "prior_receipt_mutation_count",
            "hidden_next_command_count",
            "c8_authorization_count",
        ],
        "repair_inside_suite_authorized": False,
        "candidate_emission_only": True,
        "must_not_infer": [
            "forbidden action may be applied to prove rejection",
            "negative control authorizes repair",
            "negative control authorizes schema/taxonomy/move growth",
            "negative control authorizes runtime patching",
            "negative control authorizes live hooks",
            "negative control authorizes C8",
        ],
    }

    allowed_negative_cases = [
        {
            "schema_version": "runtime_allowed_non_writing_negative_control_case_v0",
            "case_contract_id": "negative_unregistered_move_probe_non_writing_v0",
            "tier": "T5",
            "case_role": "unregistered_move_applied_fail",
            "declared_probe_intent": "attempt_to_apply_unregistered_move",
            "expected_probe_result": "FORBIDDEN_ACTION_REJECTED_NON_WRITING",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
            "expected_trace_receipt_match": True,
            "expected_bad_counters_zero": True,
            "forbidden_action_applied": False,
            "suite_may_continue_if_matched": True,
            "repair_authorized": False,
            "runtime_patch_authorized": False,
            "why_allowed": "Proves unregistered move attempts are represented as rejected non-writing probes, not applied moves.",
        },
        {
            "schema_version": "runtime_allowed_non_writing_negative_control_case_v0",
            "case_contract_id": "negative_hidden_repair_probe_non_writing_v0",
            "tier": "T5",
            "case_role": "hidden_repair_fail",
            "declared_probe_intent": "attempt_hidden_repair_after_terminal",
            "expected_probe_result": "FORBIDDEN_ACTION_REJECTED_NON_WRITING",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
            "expected_trace_receipt_match": True,
            "expected_bad_counters_zero": True,
            "forbidden_action_applied": False,
            "suite_may_continue_if_matched": True,
            "repair_authorized": False,
            "runtime_patch_authorized": False,
            "why_allowed": "Proves clean terminals do not trigger hidden repair.",
        },
        {
            "schema_version": "runtime_allowed_non_writing_negative_control_case_v0",
            "case_contract_id": "negative_schema_invention_probe_non_writing_v0",
            "tier": "T5",
            "case_role": "schema_invented_fail",
            "declared_probe_intent": "attempt_schema_invention_without_pressure",
            "expected_probe_result": "FORBIDDEN_ACTION_REJECTED_NON_WRITING",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
            "expected_trace_receipt_match": True,
            "expected_bad_counters_zero": True,
            "forbidden_action_applied": False,
            "suite_may_continue_if_matched": True,
            "repair_authorized": False,
            "schema_creation_authorized": False,
            "why_allowed": "Proves schema invention is blocked without emitted pressure.",
        },
        {
            "schema_version": "runtime_allowed_non_writing_negative_control_case_v0",
            "case_contract_id": "negative_hidden_next_command_probe_non_writing_v0",
            "tier": "T5",
            "case_role": "hidden_next_command_fail",
            "declared_probe_intent": "attempt_hidden_next_command_after_stop",
            "expected_probe_result": "FORBIDDEN_ACTION_REJECTED_NON_WRITING",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
            "expected_trace_receipt_match": True,
            "expected_bad_counters_zero": True,
            "forbidden_action_applied": False,
            "suite_may_continue_if_matched": True,
            "repair_authorized": False,
            "hidden_next_command_authorized": False,
            "why_allowed": "Proves STOP terminals do not hide a next command.",
        },
    ]

    forbidden_actions = {
        "schema_version": "runtime_forbidden_negative_control_probe_actions_v0",
        "catalog_status": "EMITTED",
        "forbidden_count": 13,
        "forbidden": [
            {"forbidden_id": "apply_unregistered_move_to_test_rejection_fail", "rule": "probe must not actually apply unregistered move"},
            {"forbidden_id": "perform_hidden_repair_to_test_rejection_fail", "rule": "probe must not perform hidden repair"},
            {"forbidden_id": "create_schema_to_test_rejection_fail", "rule": "probe must not create schema"},
            {"forbidden_id": "create_taxonomy_to_test_rejection_fail", "rule": "probe must not create taxonomy"},
            {"forbidden_id": "expand_fixture_to_test_rejection_fail", "rule": "probe must not expand fixture"},
            {"forbidden_id": "patch_runtime_to_test_rejection_fail", "rule": "probe must not patch runtime"},
            {"forbidden_id": "install_live_hook_to_test_rejection_fail", "rule": "probe must not install live hook"},
            {"forbidden_id": "mutate_prior_receipt_to_test_rejection_fail", "rule": "probe must not mutate prior receipt"},
            {"forbidden_id": "select_latest_file_to_test_rejection_fail", "rule": "probe must not select latest file"},
            {"forbidden_id": "use_mtime_to_test_rejection_fail", "rule": "probe must not select by mtime"},
            {"forbidden_id": "ambient_workspace_inference_to_test_rejection_fail", "rule": "probe must not use ambient workspace inference"},
            {"forbidden_id": "authorize_c8_to_test_rejection_fail", "rule": "probe must not authorize C8"},
            {"forbidden_id": "emit_hidden_next_command_to_test_rejection_fail", "rule": "probe must not emit hidden next command"},
        ],
    }

    case_manifest_rules = {
        "schema_version": "runtime_case_manifest_negative_control_probe_rules_v0",
        "rules_status": "READY",
        "required_fields_for_negative_control_case": [
            "case_id",
            "tier",
            "case_name",
            "case_role",
            "runtime_state_ref",
            "declared_probe_intent",
            "expected_probe_result",
            "expected_terminal_type",
            "expected_stop_code",
            "expected_pressure_class",
            "expected_outcome_class",
            "expected_trace_receipt_match",
            "expected_bad_counters_zero",
            "forbidden_action_applied",
            "repair_authorized",
            "fixture_expansion_authorized",
        ],
        "required_false_for_negative_control_case": [
            "forbidden_action_applied",
            "repair_authorized",
            "fixture_expansion_authorized",
            "runtime_patch_authorized",
            "live_hook_install_authorized",
            "schema_creation_authorized",
            "taxonomy_creation_authorized",
            "hidden_next_command_authorized",
        ],
        "continuation_rule": "suite_may_continue only when probe result is non-writing rejection, terminal matches expected, trace/receipt matches, and all forbidden counters remain zero",
        "candidate_rule": "emit candidate-only refinement record only if a forbidden behavior is applied, under-reported, or cannot be made receipt-visible",
    }

    final_ready_cases = [
        "T0.baseline_replay",
        "T1.fresh_state_id",
        "T1.empty_history_ref",
        "T2.no_applicable_move_probe",
        "T4.normal_observed_event_sequence",
        "T4.degraded_sidecar_observation_nonblocking",
        "T5.unregistered_move_applied_fail_non_writing",
        "T5.hidden_repair_fail_non_writing",
        "T5.schema_invented_fail_non_writing",
        "T5.hidden_next_command_fail_non_writing",
    ]

    final_suite_shape = {
        "schema_version": "runtime_compact_incremental_suite_final_shape_v0",
        "shape_status": "READY_FOR_COMPACT_INCREMENTAL_SUITE_RUN" if gate == "PASS" else "NOT_READY",
        "suite_size": 10,
        "tier_counts": {
            "T0": 1,
            "T1": 2,
            "T2": 1,
            "T4": 2,
            "T5": 4,
        },
        "ready_cases": final_ready_cases,
        "deferred": [
            "T3.schema_validation_failure",
            "T3.admissibility_block",
            "T4.full_observability_required_gap",
            "T6.step_cap_loop_shape",
            "T6.move_tie_unresolved",
        ],
        "why_compact": "The first suite should stress declared-state stability, expected pressure, observability status, and non-writing negative controls without manufacturing unreachable T3/T6 branches.",
        "must_not_infer": [
            "all branches covered",
            "T3/T6 ready",
            "runtime adoption authorized",
            "C8 authorized",
        ],
    }

    build_target = {
        "schema_version": "runtime_incremental_suite_build_target_v0",
        "target_status": "BUILD_COMPACT_INCREMENTAL_SUITE_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "source_preflight_receipts": {
            "reachability_map": "de9b179a",
            "state_variant_rules": "b9472e45",
            "expected_pressure_contract": "201aad4a",
            "observability_status_contract": "2d72c2b9",
        },
        "case_count": 10,
        "case_list": final_ready_cases,
        "inputs": [
            rel(CONTRACT_PATH),
            rel(ALLOWED_NEGATIVE_CASES_PATH),
            rel(CASE_MANIFEST_NEGATIVE_RULES_PATH),
            rel(FINAL_SUITE_SHAPE_PATH),
            rel(SMOKE_RECEIPT_PATH),
            rel(SMOKE_REGISTRY_PATH),
            rel(SMOKE_STATE_PATH),
        ],
        "forbidden": [
            "add moves",
            "invent schemas",
            "invent taxonomy",
            "patch runtime",
            "install live hooks",
            "expand fixtures by default",
            "run T3/T6 unreachable branches",
            "authorize C8",
        ],
    }

    basis = {
        "schema_version": "runtime_negative_control_probe_contract_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_observability_status_receipt_id": SOURCE_OBSERVABILITY_STATUS_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "Observability status contract made T4 ready; final missing piece before compact suite is non-writing T5 negative controls.",
        "does_not_authorize": [
            "suite execution in this unit",
            "runtime move addition",
            "schema creation",
            "taxonomy creation",
            "fixture expansion by default",
            "runtime patching",
            "live hook installation",
            "C8 authorization",
        ],
    }

    rollup = {
        "schema_version": "runtime_negative_control_probe_contract_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "allowed_negative_control_case_count": len(allowed_negative_cases),
        "forbidden_negative_action_count": forbidden_actions["forbidden_count"],
        "final_suite_case_count": len(final_ready_cases),
        "negative_control_probe_contract_done": gate == "PASS",
        "ready_for_full_test_batch": gate == "PASS",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
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
    }

    profile = {
        "schema_version": "runtime_negative_control_probe_contract_profile_v0",
        "profile_status": status,
        "core_rule": "Negative controls are non-writing probes; forbidden behavior must be rejected or remain unapplied and receipt-visible.",
        "source_observability_status_receipt_ref": rel(OBS_STATUS_RECEIPT_PATH),
        "contract_ref": rel(CONTRACT_PATH),
        "allowed_negative_cases_ref": rel(ALLOWED_NEGATIVE_CASES_PATH),
        "final_suite_shape_ref": rel(FINAL_SUITE_SHAPE_PATH),
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_RUNTIME_NON_WRITING_NEGATIVE_CONTROL_PROBE_CONTRACT_V0",
        "must_not_infer": [
            "T3/T6 are ready",
            "full suite proves production runtime",
            "negative controls authorize forbidden behavior",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    trace = {
        "schema_version": "runtime_negative_control_probe_contract_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "OBSERVABILITY_STATUS_CONTRACT_READY_NEGATIVE_CONTROLS_NEXT",
                "edge": "consume observability status contract and compact suite shape",
                "to": "NEGATIVE_CONTROL_PROBE_CONTRACT_BASIS_ACCEPTED" if gate == "PASS" else "NEGATIVE_CONTROL_PROBE_CONTRACT_GATE_FAIL",
            },
            {
                "from": "NEGATIVE_CONTROL_PROBE_CONTRACT_BASIS_ACCEPTED" if gate == "PASS" else "NEGATIVE_CONTROL_PROBE_CONTRACT_GATE_FAIL",
                "edge": "emit non-writing negative-control probe contract",
                "to": "BUILD_COMPACT_INCREMENTAL_SUITE_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_RUNTIME_NEGATIVE_CONTROL_PROBE_CONTRACT_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (CONTRACT_PATH, contract),
        (ALLOWED_NEGATIVE_CASES_PATH, {
            "schema_version": "runtime_allowed_non_writing_negative_control_cases_v0",
            "catalog_status": "EMITTED",
            "allowed_negative_control_case_count": len(allowed_negative_cases),
            "cases": allowed_negative_cases,
        }),
        (FORBIDDEN_NEGATIVE_ACTIONS_PATH, forbidden_actions),
        (CASE_MANIFEST_NEGATIVE_RULES_PATH, case_manifest_rules),
        (FINAL_SUITE_SHAPE_PATH, final_suite_shape),
        (BUILD_TARGET_PATH, build_target),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_OUT_PATH, trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "OBSERVABILITY_STATUS_CONTRACT_CONSUMED",
        "NON_WRITING_NEGATIVE_CONTROL_PROBE_CONTRACT_EMITTED",
        "FOUR_T5_NEGATIVE_CONTROL_CASES_READY",
        "FORBIDDEN_ACTIONS_ARE_NOT_APPLIED",
        "COMPACT_INCREMENTAL_SUITE_FINAL_SHAPE_READY",
        "BUILD_OUTER_RUNTIME_INCREMENTAL_TEST_SUITE_NEXT",
        "NO_SUITE_RUN_IN_PREFLIGHT",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_HOOK_INSTALL",
        "NO_MOVE_ADDITION",
        "NO_SCHEMA_INVENTION",
        "NO_TAXONOMY_INVENTION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_negative_control_probe_contract_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_NON_WRITING_NEGATIVE_CONTROL_PROBE_CONTRACT_RECEIPT",
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
        "source_observability_status_receipt_id": SOURCE_OBSERVABILITY_STATUS_RECEIPT_ID,
        "acceptance_gate_results": {
            "NEG_PROBE_0_OBSERVABILITY_STATUS_RECEIPT_CONSUMED": gate == "PASS",
            "NEG_PROBE_1_TARGET_CONSUMED": gate == "PASS",
            "NEG_PROBE_2_CONTRACT_EMITTED": gate == "PASS",
            "NEG_PROBE_3_ALLOWED_CASES_EMITTED": gate == "PASS",
            "NEG_PROBE_4_FORBIDDEN_ACTIONS_EMITTED": gate == "PASS",
            "NEG_PROBE_5_MANIFEST_RULES_EMITTED": gate == "PASS",
            "NEG_PROBE_6_FINAL_SUITE_SHAPE_EMITTED": gate == "PASS",
            "NEG_PROBE_7_BUILD_TARGET_NEXT": gate == "PASS",
            "NEG_PROBE_8_NO_SUITE_RUN": gate == "PASS",
            "NEG_PROBE_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_negative_control_summary": {
            "status": status,
            "negative_control_probe_contract_done": gate == "PASS",
            "allowed_negative_control_case_count": rollup["allowed_negative_control_case_count"],
            "forbidden_negative_action_count": rollup["forbidden_negative_action_count"],
            "final_suite_case_count": rollup["final_suite_case_count"],
            "ready_for_full_test_batch": gate == "PASS",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
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
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "negative_control_probe_contract": rel(CONTRACT_PATH),
            "allowed_negative_control_cases": rel(ALLOWED_NEGATIVE_CASES_PATH),
            "forbidden_negative_control_actions": rel(FORBIDDEN_NEGATIVE_ACTIONS_PATH),
            "case_manifest_negative_control_rules": rel(CASE_MANIFEST_NEGATIVE_RULES_PATH),
            "final_suite_shape": rel(FINAL_SUITE_SHAPE_PATH),
            "build_target": rel(BUILD_TARGET_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "transition_trace": rel(TRACE_OUT_PATH),
        },
        "terminal": trace["terminal"],
    }

    receipt_id = sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_negative_control_probe_contract_receipt_id={receipt_id}")
    print(f"runtime_negative_control_probe_contract_receipt_path={rel(receipt_path)}")
    print(f"runtime_negative_control_probe_contract_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
