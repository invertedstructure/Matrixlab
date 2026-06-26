#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_RUNTIME_T3_SCHEMA_VALIDATION_FAILURE_CASE_CONTRACT_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.deferred_cases.t3_schema_validation_failure_contract_v0"
NEXT_UNIT_ID = "PREPARE_RUNTIME_T3_ADMISSIBILITY_BLOCK_CASE_CONTRACT_V0"

LAYER = "OUTER / RUNTIME_ADOPTION / DEFERRED_CASES / T3"
MODE = "PREPARE_CONTRACT_ONLY / SCHEMA_VALIDATION_FAILURE / NO_TEST_RUN"
BUILD_MODE = "T3_SCHEMA_VALIDATION_FAILURE_CASE_CONTRACT_ONLY"

SOURCE_DEFERRED_READINESS_RECEIPT_ID = "60e2ce86"

READINESS_RECEIPT_PATH = ROOT / "data/runtime_deferred_cases_readiness_v0_receipts/60e2ce86.json"
READINESS_INDEX_PATH = ROOT / "data/runtime_deferred_cases_readiness_v0/runtime_deferred_cases_readiness_index_v0.json"
BUILDABLE_QUEUE_PATH = ROOT / "data/runtime_deferred_cases_readiness_v0/runtime_deferred_cases_buildable_queue_v0.json"
T3_SCHEMA_TARGET_PATH = ROOT / "data/runtime_deferred_cases_readiness_v0/runtime_t3_schema_validation_failure_case_contract_target_v0.json"

EXPECTED_PRESSURE_CONTRACT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_expected_pressure_case_contract_v0.json"
CASE_MANIFEST_EXPECTED_PRESSURE_RULES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_case_manifest_expected_pressure_rules_v0.json"
STATE_VARIANT_RULES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_declared_state_variant_rules_v0.json"
STATE_DERIVATION_TEMPLATE_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_state_derivation_template_v0.json"

SMOKE_RECEIPT_PATH = ROOT / "data/runtime_adoption_smoke_v0_receipts/runtime_smoke_receipt_900b2eae.json"
SMOKE_STATE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_state_v0.json"
SMOKE_SCHEMA_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_state_schema_v0.json"
SMOKE_REGISTRY_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_move_registry_snapshot_v0.json"

OUT_DIR = ROOT / "data/runtime_deferred_cases_t3_schema_contract_v0"
RECEIPT_DIR = ROOT / "data/runtime_deferred_cases_t3_schema_contract_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_t3_schema_validation_failure_contract_basis_v0.json"
CONTRACT_PATH = OUT_DIR / "runtime_t3_schema_validation_failure_case_contract_v0.json"
INVALID_STATE_DERIVATION_PATH = OUT_DIR / "runtime_t3_schema_validation_failure_invalid_state_derivation_v0.json"
ALLOWED_CASE_PATH = OUT_DIR / "runtime_allowed_t3_schema_validation_failure_case_v0.json"
MANIFEST_RULES_PATH = OUT_DIR / "runtime_case_manifest_t3_schema_validation_failure_rules_v0.json"
DEFERRED_SHAPE_PATH = OUT_DIR / "runtime_deferred_suite_shape_after_t3_schema_contract_v0.json"
NEXT_TARGET_PATH = OUT_DIR / "runtime_t3_admissibility_block_case_contract_target_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_t3_schema_validation_failure_contract_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_t3_schema_validation_failure_contract_profile_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_t3_schema_validation_failure_contract_transition_trace.json"

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

def find_deferred_case(index: Dict[str, Any], case_key: str) -> Optional[Dict[str, Any]]:
    for row in index.get("deferred_cases", []):
        if row.get("case_key") == case_key:
            return row
    return None

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        READINESS_RECEIPT_PATH,
        READINESS_INDEX_PATH,
        BUILDABLE_QUEUE_PATH,
        T3_SCHEMA_TARGET_PATH,
        EXPECTED_PRESSURE_CONTRACT_PATH,
        CASE_MANIFEST_EXPECTED_PRESSURE_RULES_PATH,
        STATE_VARIANT_RULES_PATH,
        STATE_DERIVATION_TEMPLATE_PATH,
        SMOKE_RECEIPT_PATH,
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

    readiness_receipt = read_json(READINESS_RECEIPT_PATH)
    readiness_summary = readiness_receipt.get("machine_readable_deferred_readiness_summary", {})
    readiness_index = read_json(READINESS_INDEX_PATH)
    buildable_queue = read_json(BUILDABLE_QUEUE_PATH)
    t3_schema_target = read_json(T3_SCHEMA_TARGET_PATH)

    expected_pressure_contract = read_json(EXPECTED_PRESSURE_CONTRACT_PATH)
    expected_pressure_manifest_rules = read_json(CASE_MANIFEST_EXPECTED_PRESSURE_RULES_PATH)
    state_variant_rules = read_json(STATE_VARIANT_RULES_PATH)
    state_derivation_template = read_json(STATE_DERIVATION_TEMPLATE_PATH)

    smoke_receipt = read_json(SMOKE_RECEIPT_PATH)
    smoke_summary = smoke_receipt.get("machine_readable_runtime_smoke_summary", {})
    smoke_state = read_json(SMOKE_STATE_PATH)
    smoke_schema = read_json(SMOKE_SCHEMA_PATH)
    smoke_registry = read_json(SMOKE_REGISTRY_PATH)

    if readiness_receipt.get("receipt_id") != SOURCE_DEFERRED_READINESS_RECEIPT_ID:
        failures.append(f"readiness_receipt_id_wrong:{readiness_receipt.get('receipt_id')}")
    if readiness_receipt.get("gate") != "PASS":
        failures.append("readiness_gate_not_pass")
    if readiness_summary.get("ready_for_t3_schema_contract") is not True:
        failures.append("readiness_not_ready_for_t3_schema_contract")
    if readiness_summary.get("ready_for_deferred_suite_run") is not False:
        failures.append("deferred_suite_run_should_not_be_ready")
    if readiness_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("readiness_terminal_not_advance")
    if readiness_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("readiness_terminal_next_wrong")

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
        require_false(readiness_summary, key, failures)

    t3_case = find_deferred_case(readiness_index, "T3.schema_validation_failure")
    if not t3_case:
        failures.append("t3_schema_case_missing_from_readiness_index")
    else:
        if t3_case.get("readiness_class") != "NEEDS_CASE_CONTRACT":
            failures.append(f"t3_schema_readiness_class_wrong:{t3_case.get('readiness_class')}")
        if t3_case.get("buildability") != "CONTRACT_PREP_READY":
            failures.append(f"t3_schema_buildability_wrong:{t3_case.get('buildability')}")

    if t3_schema_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"target_next_unit_wrong:{t3_schema_target.get('next_unit_id')}")
    if t3_schema_target.get("case_key") != "T3.schema_validation_failure":
        failures.append(f"target_case_key_wrong:{t3_schema_target.get('case_key')}")

    pressure_enum = expected_pressure_contract.get("closed_pressure_enum", [])
    outcome_enum = expected_pressure_contract.get("closed_outcome_enum", [])

    if "SCHEMA_VALIDATION_FAIL" not in pressure_enum:
        failures.append("SCHEMA_VALIDATION_FAIL_not_in_expected_pressure_enum")
    if "RUNTIME_SMOKE_BLOCKED_SCHEMA_VALIDATION" not in outcome_enum:
        failures.append("schema_validation_outcome_not_in_expected_outcome_enum")

    required_fields = smoke_schema.get("required_fields", [])
    if not isinstance(required_fields, list):
        required_fields = []

    preferred_fields = ["runtime_phase", "state_id", "schema_version"]
    invalid_field = None
    for field in preferred_fields:
        if field in required_fields and field in smoke_state:
            invalid_field = field
            break
    if invalid_field is None:
        for field in required_fields:
            if field in smoke_state:
                invalid_field = field
                break

    if invalid_field is None:
        failures.append("no_required_smoke_state_field_available_for_invalid_state_derivation")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_RUNTIME_T3_SCHEMA_VALIDATION_FAILURE_CASE_CONTRACT_READY_ADMISSIBILITY_NEXT" if gate == "PASS" else "TYPED_RUNTIME_T3_SCHEMA_VALIDATION_FAILURE_CASE_CONTRACT_GATE_FAIL"

    invalid_derivation = {
        "schema_version": "runtime_t3_schema_validation_failure_invalid_state_derivation_v0",
        "derivation_status": "READY" if gate == "PASS" else "NOT_READY",
        "source_state_ref": rel(SMOKE_STATE_PATH),
        "source_schema_ref": rel(SMOKE_SCHEMA_PATH),
        "derivation_id": "invalid_state_remove_required_field_" + (invalid_field or "UNRESOLVED"),
        "derivation_kind": "REMOVE_REQUIRED_FIELD",
        "field_removed": invalid_field,
        "invalid_state_is_written_by_suite_later": True,
        "invalid_state_written_now": False,
        "expected_validation_result": "SCHEMA_VALIDATION_FAIL",
        "expected_terminal_type": "STOP",
        "expected_stop_code": "STOP_RUNTIME_SCHEMA_VALIDATION_FAIL",
        "expected_pressure_class": "SCHEMA_VALIDATION_FAIL",
        "expected_outcome_class": "RUNTIME_SMOKE_BLOCKED_SCHEMA_VALIDATION",
        "repair_authorized": False,
        "schema_creation_authorized": False,
        "runtime_patch_authorized": False,
        "why_valid_negative_case": "A derived state missing a required field should fail schema validation before admissibility or move application.",
    }

    contract = {
        "schema_version": "runtime_t3_schema_validation_failure_case_contract_v0",
        "contract_status": "FROZEN_FOR_DEFERRED_SUITE_V0" if gate == "PASS" else "NOT_READY",
        "case_key": "T3.schema_validation_failure",
        "tier": "T3",
        "source_readiness_receipt_ref": rel(READINESS_RECEIPT_PATH),
        "source_expected_pressure_contract_ref": rel(EXPECTED_PRESSURE_CONTRACT_PATH),
        "core_rule": "Schema validation failure is an expected-pressure case only when the manifest declares the invalid-state derivation before execution.",
        "invalid_state_derivation_ref": rel(INVALID_STATE_DERIVATION_PATH),
        "expected_terminal": {
            "type": "STOP",
            "stop_code": "STOP_RUNTIME_SCHEMA_VALIDATION_FAIL",
            "next_unit_id": None,
        },
        "expected_pressure_class": "SCHEMA_VALIDATION_FAIL",
        "expected_outcome_class": "RUNTIME_SMOKE_BLOCKED_SCHEMA_VALIDATION",
        "candidate_emission_only": True,
        "repair_inside_suite_authorized": False,
        "suite_may_continue_if_matched": True,
        "validation_order_requirement": [
            "load declared state",
            "validate declared state schema",
            "stop before admissibility if invalid",
            "emit typed pressure/readout/receipt",
        ],
        "must_not_infer": [
            "schema should be changed",
            "schema validation failure authorizes repair",
            "invalid state authorizes runtime patching",
            "T3 admissibility case is covered by this contract",
            "deferred suite is ready",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    allowed_case = {
        "schema_version": "runtime_allowed_t3_schema_validation_failure_case_v0",
        "catalog_status": "EMITTED" if gate == "PASS" else "NOT_READY",
        "allowed_case_count": 1 if gate == "PASS" else 0,
        "cases": [
            {
                "case_contract_id": "t3_schema_validation_failure_missing_required_field_v0",
                "case_key": "T3.schema_validation_failure",
                "tier": "T3",
                "case_role": "schema_validation_failure_missing_required_field",
                "invalid_state_derivation_ref": rel(INVALID_STATE_DERIVATION_PATH),
                "expected_terminal_type": "STOP",
                "expected_stop_code": "STOP_RUNTIME_SCHEMA_VALIDATION_FAIL",
                "expected_pressure_class": "SCHEMA_VALIDATION_FAIL",
                "expected_outcome_class": "RUNTIME_SMOKE_BLOCKED_SCHEMA_VALIDATION",
                "expected_trace_receipt_match": True,
                "expected_bad_counters_zero": True,
                "expected_refinement_candidate_count_min": 1,
                "suite_may_continue_if_matched": True,
                "repair_authorized": False,
                "schema_creation_authorized": False,
                "runtime_patch_authorized": False,
                "fixture_expansion_authorized": False,
                "why_allowed": "The invalid state is a declared missing-required-field variant for testing typed schema validation pressure.",
            }
        ],
    }

    manifest_rules = {
        "schema_version": "runtime_case_manifest_t3_schema_validation_failure_rules_v0",
        "rules_status": "READY" if gate == "PASS" else "NOT_READY",
        "required_fields_for_t3_schema_failure_case": [
            "case_id",
            "tier",
            "case_name",
            "case_role",
            "runtime_state_ref",
            "invalid_state_derivation_ref",
            "expected_terminal_type",
            "expected_stop_code",
            "expected_pressure_class",
            "expected_outcome_class",
            "expected_trace_receipt_match",
            "expected_bad_counters_zero",
            "repair_authorized",
            "schema_creation_authorized",
            "runtime_patch_authorized",
        ],
        "required_false_for_t3_schema_failure_case": [
            "repair_authorized",
            "schema_creation_authorized",
            "taxonomy_creation_authorized",
            "fixture_expansion_authorized",
            "runtime_patch_authorized",
            "live_hook_install_authorized",
            "runtime_adoption_authorized",
            "c8_authorized",
        ],
        "ordering_rule": "schema validation failure must stop before admissibility check and before registered move inspection",
        "candidate_rule": "emit candidate-only refinement record if schema validation failure is real, underdeclared, mismatched, or not receipt-visible",
        "continuation_rule": "suite_may_continue only if STOP_RUNTIME_SCHEMA_VALIDATION_FAIL and SCHEMA_VALIDATION_FAIL match exactly",
    }

    deferred_shape = {
        "schema_version": "runtime_deferred_suite_shape_after_t3_schema_contract_v0",
        "shape_status": "PARTIAL_READY_T3_ADMISSIBILITY_CONTRACT_NEXT" if gate == "PASS" else "NOT_READY",
        "ready_deferred_cases_after_this_unit": [
            "T3.schema_validation_failure",
        ],
        "contracted_cases": [
            "T3.schema_validation_failure",
        ],
        "still_needs_contract": [
            "T3.admissibility_block",
        ],
        "still_needs_case_instance": [
            "T4.full_observability_required_gap",
        ],
        "still_needs_feasibility_audit": [
            "T6.step_cap_loop_shape",
            "T6.move_tie_unresolved",
        ],
        "ready_for_deferred_suite_run": False,
    }

    next_target = {
        "schema_version": "runtime_t3_admissibility_block_case_contract_target_v0",
        "target_status": "T3_ADMISSIBILITY_BLOCK_CASE_CONTRACT_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "source_t3_schema_contract_ref": rel(CONTRACT_PATH),
        "source_t3_schema_allowed_case_ref": rel(ALLOWED_CASE_PATH),
        "case_key": "T3.admissibility_block",
        "target_role": "Prepare explicit admissibility-block expected-pressure contract; do not run case yet.",
        "forbidden": [
            "run deferred suite now",
            "repair schema",
            "add moves",
            "patch runtime",
            "expand fixtures by default",
            "authorize C8",
            "authorize live runtime adoption",
        ],
    }

    basis = {
        "schema_version": "runtime_t3_schema_validation_failure_contract_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_deferred_readiness_receipt_id": SOURCE_DEFERRED_READINESS_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "Deferred readiness audit marked T3 schema validation failure as contract-prep ready; this unit prepares the expected-pressure contract only.",
        "does_not_authorize": [
            "suite execution",
            "schema repair",
            "schema creation",
            "taxonomy creation",
            "move addition",
            "fixture expansion by default",
            "runtime patching",
            "live runtime adoption",
            "C8 authorization",
        ],
    }

    rollup = {
        "schema_version": "runtime_t3_schema_validation_failure_contract_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "t3_schema_contract_done": gate == "PASS",
        "allowed_t3_schema_failure_case_count": 1 if gate == "PASS" else 0,
        "invalid_state_derivation_ready": gate == "PASS",
        "invalid_field": invalid_field,
        "ready_for_t3_admissibility_contract": gate == "PASS",
        "ready_for_deferred_suite_run": False,
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
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
        "schema_version": "runtime_t3_schema_validation_failure_contract_profile_v0",
        "profile_status": status,
        "core_rule": "Invalid-state schema failure is expected pressure, not permission to mutate the schema.",
        "contract_ref": rel(CONTRACT_PATH),
        "allowed_case_ref": rel(ALLOWED_CASE_PATH),
        "invalid_state_derivation_ref": rel(INVALID_STATE_DERIVATION_PATH),
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_RUNTIME_T3_SCHEMA_VALIDATION_FAILURE_CASE_CONTRACT_V0",
        "must_not_infer": [
            "deferred suite is ready",
            "schema should be repaired",
            "schema archive should mutate",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    trace = {
        "schema_version": "runtime_t3_schema_validation_failure_contract_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "DEFERRED_READINESS_READY_T3_SCHEMA_CONTRACT_NEXT",
                "edge": "consume readiness target and smoke schema",
                "to": "T3_SCHEMA_FAILURE_CONTRACT_BASIS_ACCEPTED" if gate == "PASS" else "T3_SCHEMA_FAILURE_CONTRACT_GATE_FAIL",
            },
            {
                "from": "T3_SCHEMA_FAILURE_CONTRACT_BASIS_ACCEPTED" if gate == "PASS" else "T3_SCHEMA_FAILURE_CONTRACT_GATE_FAIL",
                "edge": "emit expected-pressure schema-failure contract",
                "to": "T3_ADMISSIBILITY_BLOCK_CONTRACT_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_RUNTIME_T3_SCHEMA_VALIDATION_FAILURE_CASE_CONTRACT_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (INVALID_STATE_DERIVATION_PATH, invalid_derivation),
        (CONTRACT_PATH, contract),
        (ALLOWED_CASE_PATH, allowed_case),
        (MANIFEST_RULES_PATH, manifest_rules),
        (DEFERRED_SHAPE_PATH, deferred_shape),
        (NEXT_TARGET_PATH, next_target),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_OUT_PATH, trace),
    ]:
        write_json(path, obj)

    source_hashes_after = {rel(p): file_sha256(p) for p in required}
    source_mutated = source_hashes_before != source_hashes_after
    if source_mutated:
        gate = "FAIL"
        status = "TYPED_RUNTIME_T3_SCHEMA_VALIDATION_FAILURE_CONTRACT_SOURCE_MUTATION_FAIL"
        failures.append("source_inputs_mutated")

    reason_codes = [
        "DEFERRED_READINESS_RECEIPT_CONSUMED",
        "T3_SCHEMA_VALIDATION_FAILURE_TARGET_CONSUMED",
        "INVALID_STATE_DERIVATION_DECLARED",
        "SCHEMA_VALIDATION_FAIL_EXPECTED_PRESSURE_CONTRACTED",
        "T3_SCHEMA_FAILURE_CASE_READY_FOR_DEFERRED_SUITE",
        "T3_ADMISSIBILITY_CONTRACT_NEXT",
        "NO_SUITE_RUN",
        "NO_SCHEMA_REPAIR",
        "NO_SCHEMA_INVENTION",
        "NO_TAXONOMY_INVENTION",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_RUNTIME_ADOPTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_t3_schema_validation_failure_contract_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_T3_SCHEMA_VALIDATION_FAILURE_CASE_CONTRACT_RECEIPT",
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
        "source_deferred_readiness_receipt_id": SOURCE_DEFERRED_READINESS_RECEIPT_ID,
        "acceptance_gate_results": {
            "T3_SCHEMA_0_READINESS_RECEIPT_CONSUMED": gate == "PASS",
            "T3_SCHEMA_1_TARGET_CONSUMED": gate == "PASS",
            "T3_SCHEMA_2_INVALID_STATE_DERIVATION_DECLARED": gate == "PASS",
            "T3_SCHEMA_3_CONTRACT_EMITTED": gate == "PASS",
            "T3_SCHEMA_4_ALLOWED_CASE_EMITTED": gate == "PASS",
            "T3_SCHEMA_5_MANIFEST_RULES_EMITTED": gate == "PASS",
            "T3_SCHEMA_6_ADMISSIBILITY_TARGET_NEXT": gate == "PASS",
            "T3_SCHEMA_7_NO_SUITE_RUN": gate == "PASS",
            "T3_SCHEMA_8_SOURCE_INPUTS_NOT_MUTATED": not source_mutated,
            "T3_SCHEMA_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_t3_schema_contract_summary": {
            "status": status,
            "t3_schema_contract_done": gate == "PASS",
            "case_key": "T3.schema_validation_failure",
            "invalid_state_derivation_ready": gate == "PASS",
            "invalid_field": invalid_field,
            "expected_pressure_class": "SCHEMA_VALIDATION_FAIL",
            "expected_outcome_class": "RUNTIME_SMOKE_BLOCKED_SCHEMA_VALIDATION",
            "allowed_t3_schema_failure_case_count": 1 if gate == "PASS" else 0,
            "ready_for_t3_admissibility_contract": gate == "PASS",
            "ready_for_deferred_suite_run": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
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
            "invalid_state_derivation": rel(INVALID_STATE_DERIVATION_PATH),
            "contract": rel(CONTRACT_PATH),
            "allowed_case": rel(ALLOWED_CASE_PATH),
            "manifest_rules": rel(MANIFEST_RULES_PATH),
            "deferred_shape": rel(DEFERRED_SHAPE_PATH),
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
    print(f"runtime_t3_schema_contract_receipt_id={receipt_id}")
    print(f"runtime_t3_schema_contract_receipt_path={rel(receipt_path)}")
    print(f"runtime_t3_schema_contract_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
