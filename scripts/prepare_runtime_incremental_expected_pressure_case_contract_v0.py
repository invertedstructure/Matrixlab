#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_RUNTIME_INCREMENTAL_EXPECTED_PRESSURE_CASE_CONTRACT_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.incremental_suite.expected_pressure_case_contract_v0"
NEXT_UNIT_ID = "PREPARE_RUNTIME_OBSERVABILITY_STATUS_CASE_CONTRACT_V0"

LAYER = "OUTER / RUNTIME_ADOPTION / INCREMENTAL_SUITE_PREFLIGHT"
MODE = "PREPARE_CONTRACT_ONLY / EXPECTED_PRESSURE_CASES / NO_TEST_RUN"
BUILD_MODE = "RUNTIME_EXPECTED_PRESSURE_CASE_CONTRACT_ONLY"

SOURCE_STATE_VARIANT_RULES_RECEIPT_ID = "b9472e45"

STATE_VARIANT_RULES_RECEIPT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0_receipts/b9472e45.json"
STATE_VARIANT_RULES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_declared_state_variant_rules_v0.json"
ALLOWED_VARIANT_CATALOG_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_state_variant_catalog_v0.json"
FORBIDDEN_VARIANT_CATALOG_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_forbidden_state_variant_catalog_v0.json"
COMPACT_SUITE_SHAPE_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_compact_suite_shape_after_state_rules_v0.json"
EXPECTED_PRESSURE_TARGET_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_expected_pressure_case_contract_target_v0.json"
BRANCH_GAP_INDEX_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_branch_gap_index_v0.json"
REACHABILITY_MAP_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_registry_reachability_map_v0.json"
SMOKE_REGISTRY_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_move_registry_snapshot_v0.json"
SMOKE_RECEIPT_PATH = ROOT / "data/runtime_adoption_smoke_v0_receipts/runtime_smoke_receipt_900b2eae.json"

OUT_DIR = ROOT / "data/runtime_incremental_suite_preflight_v0"
RECEIPT_DIR = ROOT / "data/runtime_incremental_suite_preflight_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_expected_pressure_case_contract_basis_v0.json"
CONTRACT_PATH = OUT_DIR / "runtime_expected_pressure_case_contract_v0.json"
ALLOWED_PRESSURE_CASES_PATH = OUT_DIR / "runtime_allowed_expected_pressure_cases_v0.json"
FORBIDDEN_PRESSURE_HANDLING_PATH = OUT_DIR / "runtime_forbidden_expected_pressure_handling_v0.json"
SUITE_CASE_MANIFEST_RULES_PATH = OUT_DIR / "runtime_case_manifest_expected_pressure_rules_v0.json"
COMPACT_SUITE_SHAPE_PATH_AFTER = OUT_DIR / "runtime_compact_suite_shape_after_expected_pressure_contract_v0.json"
NEXT_TARGET_PATH = OUT_DIR / "runtime_observability_status_case_contract_target_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_expected_pressure_case_contract_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_expected_pressure_case_contract_profile_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_expected_pressure_case_contract_transition_trace.json"

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

def require_false(obj: Dict[str, Any], key: str, failures: List[str]) -> None:
    if obj.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{obj.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        STATE_VARIANT_RULES_RECEIPT_PATH,
        STATE_VARIANT_RULES_PATH,
        ALLOWED_VARIANT_CATALOG_PATH,
        FORBIDDEN_VARIANT_CATALOG_PATH,
        COMPACT_SUITE_SHAPE_PATH,
        EXPECTED_PRESSURE_TARGET_PATH,
        BRANCH_GAP_INDEX_PATH,
        REACHABILITY_MAP_PATH,
        SMOKE_REGISTRY_PATH,
        SMOKE_RECEIPT_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    state_variant_receipt = read_json(STATE_VARIANT_RULES_RECEIPT_PATH)
    state_variant_summary = state_variant_receipt.get("machine_readable_state_variant_rules_summary", {})
    state_variant_rules = read_json(STATE_VARIANT_RULES_PATH)
    allowed_variant_catalog = read_json(ALLOWED_VARIANT_CATALOG_PATH)
    forbidden_variant_catalog = read_json(FORBIDDEN_VARIANT_CATALOG_PATH)
    compact_shape = read_json(COMPACT_SUITE_SHAPE_PATH)
    target = read_json(EXPECTED_PRESSURE_TARGET_PATH)
    branch_gap_index = read_json(BRANCH_GAP_INDEX_PATH)
    reachability_map = read_json(REACHABILITY_MAP_PATH)
    smoke_registry = read_json(SMOKE_REGISTRY_PATH)
    smoke_receipt = read_json(SMOKE_RECEIPT_PATH)

    if state_variant_receipt.get("receipt_id") != SOURCE_STATE_VARIANT_RULES_RECEIPT_ID:
        failures.append(f"state_variant_receipt_id_wrong:{state_variant_receipt.get('receipt_id')}")
    if state_variant_receipt.get("gate") != "PASS":
        failures.append("state_variant_gate_not_pass")
    if state_variant_summary.get("ready_for_expected_pressure_case_contract") is not True:
        failures.append("state_variant_not_ready_for_expected_pressure_contract")
    if state_variant_summary.get("ready_for_full_test_batch") is not False:
        failures.append("full_test_batch_should_not_be_ready_yet")
    if state_variant_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("state_variant_terminal_not_advance")
    if state_variant_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("state_variant_terminal_next_wrong")

    if target.get("target_status") != "EXPECTED_PRESSURE_CASE_CONTRACT_NEXT":
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
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(state_variant_summary, key, failures)

    allowed_variants = allowed_variant_catalog.get("variants", [])
    pressure_variants = [
        v for v in allowed_variants
        if v.get("requires_expected_pressure_contract") is True
    ]

    no_applicable_variant = None
    for v in pressure_variants:
        if v.get("case_role") == "declared_no_applicable_move_pressure":
            no_applicable_variant = v

    if no_applicable_variant is None:
        failures.append("no_applicable_move_pressure_variant_missing")

    for v in pressure_variants:
        pc = v.get("expected_pressure_class")
        oc = v.get("expected_outcome_class")
        if pc not in PRESSURE_ENUM:
            failures.append(f"pressure_variant_unregistered_pressure:{v.get('variant_id')}:{pc}")
        if oc not in OUTCOME_ENUM:
            failures.append(f"pressure_variant_unregistered_outcome:{v.get('variant_id')}:{oc}")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_RUNTIME_INCREMENTAL_EXPECTED_PRESSURE_CASE_CONTRACT_READY_OBSERVABILITY_STATUS_NEXT" if gate == "PASS" else "TYPED_RUNTIME_INCREMENTAL_EXPECTED_PRESSURE_CASE_CONTRACT_GATE_FAIL"

    expected_pressure_contract = {
        "schema_version": "runtime_expected_pressure_case_contract_v0",
        "contract_status": "FROZEN_FOR_INCREMENTAL_SUITE_V0" if gate == "PASS" else "NOT_READY",
        "source_state_variant_rules_ref": rel(STATE_VARIANT_RULES_PATH),
        "source_allowed_variant_catalog_ref": rel(ALLOWED_VARIANT_CATALOG_PATH),
        "core_rule": "A typed pressure result may count as a successful test case only when the case manifest declares that pressure as expected or allowed before execution.",
        "pressure_is_not_repair_authority": True,
        "repair_inside_suite_authorized": False,
        "candidate_emission_only": True,
        "allowed_pressure_match_modes": [
            {
                "mode": "EXPECTED_EXACT",
                "rule": "terminal_type, stop_code, pressure_class, and outcome_class must match manifest values exactly",
            },
            {
                "mode": "ALLOWED_PRESSURE",
                "rule": "pressure_class may be accepted only if listed in allowed_pressure for that case",
            },
        ],
        "forbidden_pressure_match_modes": [
            "treat unexpected pressure as pass",
            "repair inside suite",
            "add move from pressure inside suite",
            "add schema from pressure inside suite",
            "add taxonomy from pressure inside suite",
            "retry without changed declared state",
            "hide next command",
        ],
        "closed_pressure_enum": PRESSURE_ENUM,
        "closed_outcome_enum": OUTCOME_ENUM,
        "suite_result_rule": "Expected pressure may allow suite continuation, but must still emit per-case receipt, trace, readout, pressure classification, and candidate-only refinement record if gap/failure is material.",
        "must_not_infer": [
            "expected pressure authorizes repair",
            "expected pressure proves runtime correctness",
            "expected pressure authorizes move addition",
            "expected pressure authorizes schema/taxonomy growth",
            "expected pressure authorizes runtime adoption",
            "C8 is authorized",
        ],
    }

    allowed_pressure_cases = [
        {
            "schema_version": "runtime_allowed_expected_pressure_case_v0",
            "case_contract_id": "expected_pressure_no_applicable_move_probe_v0",
            "source_variant_id": no_applicable_variant.get("variant_id") if no_applicable_variant else None,
            "tier": "T2",
            "case_role": "declared_no_applicable_move_pressure",
            "runtime_phase_value": "NO_APPLICABLE_MOVE_PROBE",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_NO_APPLICABLE_MOVE",
            "expected_pressure_class": "NO_APPLICABLE_MOVE",
            "expected_outcome_class": "RUNTIME_SMOKE_BLOCKED_NO_APPLICABLE_MOVE",
            "expected_trace_receipt_match": True,
            "expected_bad_counters_zero": True,
            "expected_refinement_candidate_count_min": 1,
            "expected_refinement_candidate_status": "CANDIDATE_ONLY",
            "suite_may_continue_if_matched": True,
            "repair_authorized": False,
            "move_addition_authorized": False,
            "schema_creation_authorized": False,
            "taxonomy_creation_authorized": False,
            "runtime_patch_authorized": False,
            "why_allowed": "No applicable move was identified as underdeclared by reachability audit. This contract allows the suite to test that the runtime emits typed pressure instead of inventing a move.",
        }
    ] if no_applicable_variant else []

    forbidden_pressure_handling = {
        "schema_version": "runtime_forbidden_expected_pressure_handling_v0",
        "catalog_status": "EMITTED",
        "forbidden_count": 10,
        "forbidden": [
            {
                "forbidden_id": "unexpected_pressure_pass_fail",
                "rule": "unexpected pressure must fail the case or stop the suite by tier rule",
            },
            {
                "forbidden_id": "expected_pressure_repair_fail",
                "rule": "expected pressure cannot authorize repair inside suite",
            },
            {
                "forbidden_id": "expected_pressure_move_addition_fail",
                "rule": "expected pressure cannot add a move inside suite",
            },
            {
                "forbidden_id": "expected_pressure_schema_creation_fail",
                "rule": "expected pressure cannot create schema inside suite",
            },
            {
                "forbidden_id": "expected_pressure_taxonomy_creation_fail",
                "rule": "expected pressure cannot create taxonomy inside suite",
            },
            {
                "forbidden_id": "expected_pressure_fixture_expansion_fail",
                "rule": "expected pressure cannot expand fixtures by default",
            },
            {
                "forbidden_id": "expected_pressure_runtime_patch_fail",
                "rule": "expected pressure cannot patch runtime",
            },
            {
                "forbidden_id": "expected_pressure_live_hook_fail",
                "rule": "expected pressure cannot install live hooks",
            },
            {
                "forbidden_id": "expected_pressure_c8_authorization_fail",
                "rule": "expected pressure cannot authorize C8",
            },
            {
                "forbidden_id": "expected_pressure_hidden_next_command_fail",
                "rule": "expected pressure cannot hide next unit/command",
            },
        ],
    }

    case_manifest_rules = {
        "schema_version": "runtime_case_manifest_expected_pressure_rules_v0",
        "rules_status": "READY",
        "required_fields_for_expected_pressure_case": [
            "case_id",
            "tier",
            "case_name",
            "case_role",
            "runtime_state_ref",
            "expected_terminal_type",
            "expected_stop_code",
            "expected_pressure_class",
            "expected_outcome_class",
            "expected_trace_receipt_match",
            "allowed_pressure",
            "forbidden_pressure",
            "repair_authorized",
            "fixture_expansion_authorized",
        ],
        "required_false_for_expected_pressure_case": [
            "repair_authorized",
            "fixture_expansion_authorized",
        ],
        "continuation_rule": "suite_may_continue only if the emitted pressure exactly matches expected pressure or allowed_pressure and all forbidden counters remain zero",
        "candidate_rule": "emit candidate-only refinement record if the pressure indicates missing move, observability gap, feedback gap, schema/admissibility failure, mismatch, or projection bug",
        "no_candidate_required_for": [
            "STOP_DONE",
            "NO_PRESSURE_TERMINAL",
        ],
    }

    compact_suite_shape_after = {
        "schema_version": "runtime_compact_suite_shape_after_expected_pressure_contract_v0",
        "shape_status": "PARTIAL_READY_OBSERVABILITY_STATUS_NEXT" if gate == "PASS" else "NOT_READY",
        "ready_cases_after_this_unit": [
            "T0.baseline_replay",
            "T1.fresh_state_id",
            "T1.empty_history_ref",
            "T2.no_applicable_move_probe",
        ],
        "expected_pressure_cases_ready": [
            "T2.no_applicable_move_probe",
        ],
        "not_ready_until_observability_status_contract": [
            "T4.observability_degraded_or_gap",
        ],
        "not_ready_until_negative_control_probe_contract": [
            "T5.non_writing_negative_controls",
        ],
        "deferred": [
            "T3.schema_validation_failure",
            "T3.admissibility_block",
            "T6.step_cap_loop_shape",
            "T6.move_tie_unresolved",
        ],
        "recommended_first_suite_total_cases_after_all_preflight": 10,
    }

    next_target = {
        "schema_version": "runtime_observability_status_case_contract_target_v0",
        "target_status": "OBSERVABILITY_STATUS_CASE_CONTRACT_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "why": "Expected pressure cases are now contracted; next missing piece is non-control observability status handling for T4 before the compact suite can include observability stress.",
        "inputs": [
            rel(CONTRACT_PATH),
            rel(ALLOWED_PRESSURE_CASES_PATH),
            rel(SUITE_CASE_MANIFEST_RULES_PATH),
            rel(COMPACT_SUITE_SHAPE_PATH_AFTER),
        ],
        "forbidden": [
            "run full suite now",
            "give sidecar control path authority",
            "patch runtime",
            "add moves",
            "invent schemas",
            "treat observability status as authorization",
        ],
    }

    basis = {
        "schema_version": "runtime_expected_pressure_case_contract_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_state_variant_rules_receipt_id": SOURCE_STATE_VARIANT_RULES_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "State variant rules identified a no-applicable-move probe that requires an explicit expected-pressure contract before the suite can include it.",
        "does_not_authorize": [
            "suite execution",
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
        "schema_version": "runtime_expected_pressure_case_contract_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "allowed_expected_pressure_case_count": len(allowed_pressure_cases),
        "forbidden_pressure_handling_count": forbidden_pressure_handling["forbidden_count"],
        "expected_pressure_contract_done": gate == "PASS",
        "ready_for_observability_status_case_contract": gate == "PASS",
        "ready_for_full_test_batch": False,
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "schema_created": False,
        "taxonomy_created": False,
        "fixture_expanded_by_default": False,
        "architecture_widened": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    profile = {
        "schema_version": "runtime_expected_pressure_case_contract_profile_v0",
        "profile_status": status,
        "core_rule": "Expected pressure can be a passing test outcome only when declared before execution and never authorizes repair inside the suite.",
        "source_state_variant_rules_receipt_ref": rel(STATE_VARIANT_RULES_RECEIPT_PATH),
        "contract_ref": rel(CONTRACT_PATH),
        "allowed_pressure_cases_ref": rel(ALLOWED_PRESSURE_CASES_PATH),
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_RUNTIME_INCREMENTAL_EXPECTED_PRESSURE_CASE_CONTRACT_V0",
        "must_not_infer": [
            "observability stress is ready",
            "negative controls are ready",
            "full test batch is ready",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    trace = {
        "schema_version": "runtime_expected_pressure_case_contract_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "STATE_VARIANT_RULES_READY_EXPECTED_PRESSURE_NEXT",
                "edge": "consume pressure variant and compact suite shape",
                "to": "EXPECTED_PRESSURE_CASE_CONTRACT_BASIS_ACCEPTED" if gate == "PASS" else "EXPECTED_PRESSURE_CASE_CONTRACT_GATE_FAIL",
            },
            {
                "from": "EXPECTED_PRESSURE_CASE_CONTRACT_BASIS_ACCEPTED" if gate == "PASS" else "EXPECTED_PRESSURE_CASE_CONTRACT_GATE_FAIL",
                "edge": "emit expected-pressure contract",
                "to": "OBSERVABILITY_STATUS_CASE_CONTRACT_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_RUNTIME_EXPECTED_PRESSURE_CASE_CONTRACT_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (CONTRACT_PATH, expected_pressure_contract),
        (ALLOWED_PRESSURE_CASES_PATH, {
            "schema_version": "runtime_allowed_expected_pressure_cases_v0",
            "catalog_status": "EMITTED",
            "allowed_expected_pressure_case_count": len(allowed_pressure_cases),
            "cases": allowed_pressure_cases,
        }),
        (FORBIDDEN_PRESSURE_HANDLING_PATH, forbidden_pressure_handling),
        (SUITE_CASE_MANIFEST_RULES_PATH, case_manifest_rules),
        (COMPACT_SUITE_SHAPE_PATH_AFTER, compact_suite_shape_after),
        (NEXT_TARGET_PATH, next_target),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_OUT_PATH, trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "STATE_VARIANT_RULES_CONSUMED",
        "EXPECTED_PRESSURE_CASE_CONTRACT_EMITTED",
        "NO_APPLICABLE_MOVE_PROBE_CONTRACTED",
        "EXPECTED_PRESSURE_IS_TEST_RESULT_NOT_REPAIR_AUTHORITY",
        "CANDIDATE_ONLY_REFINEMENT_RULE_EMITTED",
        "T2_NO_APPLICABLE_MOVE_PROBE_READY",
        "OBSERVABILITY_STATUS_CONTRACT_NEXT",
        "NO_SUITE_RUN",
        "NO_MOVE_ADDITION",
        "NO_SCHEMA_INVENTION",
        "NO_TAXONOMY_INVENTION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_HOOK_INSTALL",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_expected_pressure_case_contract_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_EXPECTED_PRESSURE_CASE_CONTRACT_RECEIPT",
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
        "source_state_variant_rules_receipt_id": SOURCE_STATE_VARIANT_RULES_RECEIPT_ID,
        "acceptance_gate_results": {
            "EXPECTED_PRESSURE_0_STATE_VARIANT_RULES_CONSUMED": gate == "PASS",
            "EXPECTED_PRESSURE_1_PRESSURE_VARIANT_FOUND": no_applicable_variant is not None,
            "EXPECTED_PRESSURE_2_CONTRACT_EMITTED": gate == "PASS",
            "EXPECTED_PRESSURE_3_ALLOWED_CASES_EMITTED": gate == "PASS",
            "EXPECTED_PRESSURE_4_FORBIDDEN_HANDLING_EMITTED": gate == "PASS",
            "EXPECTED_PRESSURE_5_MANIFEST_RULES_EMITTED": gate == "PASS",
            "EXPECTED_PRESSURE_6_OBSERVABILITY_STATUS_NEXT": gate == "PASS",
            "EXPECTED_PRESSURE_7_NO_SUITE_RUN": gate == "PASS",
            "EXPECTED_PRESSURE_8_NO_RUNTIME_PATCH": gate == "PASS",
            "EXPECTED_PRESSURE_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_expected_pressure_summary": {
            "status": status,
            "expected_pressure_contract_done": gate == "PASS",
            "allowed_expected_pressure_case_count": len(allowed_pressure_cases),
            "forbidden_pressure_handling_count": forbidden_pressure_handling["forbidden_count"],
            "no_applicable_move_probe_ready": no_applicable_variant is not None and gate == "PASS",
            "ready_for_observability_status_case_contract": gate == "PASS",
            "ready_for_full_test_batch": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "runtime_adoption_authorized": False,
            "runtime_patched": False,
            "live_runtime_hooks_installed": False,
            "schema_archive_mutated": False,
            "schema_created": False,
            "taxonomy_created": False,
            "fixture_expanded_by_default": False,
            "architecture_widened": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "expected_pressure_contract": rel(CONTRACT_PATH),
            "allowed_expected_pressure_cases": rel(ALLOWED_PRESSURE_CASES_PATH),
            "forbidden_expected_pressure_handling": rel(FORBIDDEN_PRESSURE_HANDLING_PATH),
            "case_manifest_rules": rel(SUITE_CASE_MANIFEST_RULES_PATH),
            "compact_suite_shape_after_expected_pressure": rel(COMPACT_SUITE_SHAPE_PATH_AFTER),
            "next_target": rel(NEXT_TARGET_PATH),
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
    print(f"runtime_expected_pressure_contract_receipt_id={receipt_id}")
    print(f"runtime_expected_pressure_contract_receipt_path={rel(receipt_path)}")
    print(f"runtime_expected_pressure_contract_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
