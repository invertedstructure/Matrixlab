#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_RUNTIME_T4_REQUIRED_OBSERVABILITY_GAP_CASE_INSTANCE_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.deferred_cases.t4_required_observability_gap_instance_v0"
NEXT_UNIT_ID = "AUDIT_RUNTIME_T6_LOOP_AND_TIE_TRIGGER_FEASIBILITY_V0"

LAYER = "OUTER / RUNTIME_ADOPTION / DEFERRED_CASES / T4"
MODE = "PREPARE_CASE_INSTANCE_ONLY / REQUIRED_OBSERVABILITY_GAP / NO_TEST_RUN"
BUILD_MODE = "T4_REQUIRED_OBSERVABILITY_GAP_CASE_INSTANCE_ONLY"

SOURCE_T3_ADMISSIBILITY_RECEIPT_ID = "e8a7665a"

T3_ADMISSIBILITY_RECEIPT_PATH = ROOT / "data/runtime_deferred_cases_t3_admissibility_contract_v0_receipts/e8a7665a.json"
T3_ADMISSIBILITY_CONTRACT_PATH = ROOT / "data/runtime_deferred_cases_t3_admissibility_contract_v0/runtime_t3_admissibility_block_case_contract_v0.json"
T3_ADMISSIBILITY_ALLOWED_CASE_PATH = ROOT / "data/runtime_deferred_cases_t3_admissibility_contract_v0/runtime_allowed_t3_admissibility_block_case_v0.json"
T3_ADMISSIBILITY_DEFERRED_SHAPE_PATH = ROOT / "data/runtime_deferred_cases_t3_admissibility_contract_v0/runtime_deferred_suite_shape_after_t3_admissibility_contract_v0.json"
T4_TARGET_PATH = ROOT / "data/runtime_deferred_cases_t3_admissibility_contract_v0/runtime_t4_required_observability_gap_case_instance_target_v0.json"

T3_SCHEMA_CONTRACT_PATH = ROOT / "data/runtime_deferred_cases_t3_schema_contract_v0/runtime_t3_schema_validation_failure_case_contract_v0.json"
T3_SCHEMA_ALLOWED_CASE_PATH = ROOT / "data/runtime_deferred_cases_t3_schema_contract_v0/runtime_allowed_t3_schema_validation_failure_case_v0.json"

DEFERRED_READINESS_INDEX_PATH = ROOT / "data/runtime_deferred_cases_readiness_v0/runtime_deferred_cases_readiness_index_v0.json"
DEFERRED_FEASIBILITY_QUEUE_PATH = ROOT / "data/runtime_deferred_cases_readiness_v0/runtime_deferred_cases_feasibility_queue_v0.json"

OBSERVABILITY_CONTRACT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_observability_status_case_contract_v0.json"
ALLOWED_OBSERVABILITY_CASES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_observability_status_cases_v0.json"
CASE_MANIFEST_OBSERVABILITY_RULES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_case_manifest_observability_status_rules_v0.json"
FORBIDDEN_OBSERVABILITY_CONTROL_CLAIMS_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_forbidden_observability_control_claims_v0.json"

SMOKE_RECEIPT_PATH = ROOT / "data/runtime_adoption_smoke_v0_receipts/runtime_smoke_receipt_900b2eae.json"
SMOKE_STATE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_state_v0.json"
SMOKE_SCHEMA_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_state_schema_v0.json"
SMOKE_REGISTRY_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_move_registry_snapshot_v0.json"

OUT_DIR = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0"
RECEIPT_DIR = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_t4_required_observability_gap_instance_basis_v0.json"
GAP_DERIVATION_PATH = OUT_DIR / "runtime_t4_required_observability_gap_derivation_v0.json"
CASE_INSTANCE_PATH = OUT_DIR / "runtime_t4_required_observability_gap_case_instance_v0.json"
ALLOWED_CASE_PATH = OUT_DIR / "runtime_allowed_t4_required_observability_gap_case_instance_v0.json"
MANIFEST_RULES_PATH = OUT_DIR / "runtime_case_manifest_t4_required_observability_gap_rules_v0.json"
DEFERRED_SHAPE_PATH = OUT_DIR / "runtime_deferred_suite_shape_after_t4_observability_gap_instance_v0.json"
NEXT_TARGET_PATH = OUT_DIR / "runtime_t6_loop_and_tie_trigger_feasibility_target_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_t4_required_observability_gap_instance_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_t4_required_observability_gap_instance_profile_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_t4_required_observability_gap_instance_transition_trace.json"

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

def allowed_cases(obj: Dict[str, Any]) -> List[Dict[str, Any]]:
    if isinstance(obj.get("cases"), list):
        return obj["cases"]
    if isinstance(obj.get("allowed_cases"), list):
        return obj["allowed_cases"]
    if isinstance(obj.get("observability_cases"), list):
        return obj["observability_cases"]
    return []

def find_observability_required_gap_case(rows: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    preferred = []
    fallback = []
    for row in rows:
        text = json.dumps(row, sort_keys=True)
        if row.get("case_key") == "T4.full_observability_required_gap":
            preferred.append(row)
        elif row.get("case_role") == "full_observability_required_gap":
            preferred.append(row)
        elif "full_observability_required_gap" in text:
            fallback.append(row)
        elif "GAP_EXPECTED_PRESSURE" in text and "RUNTIME_OBSERVABILITY_GAP" in text:
            fallback.append(row)
    if preferred:
        return preferred[0]
    if fallback:
        return fallback[0]
    return None

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        T3_ADMISSIBILITY_RECEIPT_PATH,
        T3_ADMISSIBILITY_CONTRACT_PATH,
        T3_ADMISSIBILITY_ALLOWED_CASE_PATH,
        T3_ADMISSIBILITY_DEFERRED_SHAPE_PATH,
        T4_TARGET_PATH,
        T3_SCHEMA_CONTRACT_PATH,
        T3_SCHEMA_ALLOWED_CASE_PATH,
        DEFERRED_READINESS_INDEX_PATH,
        DEFERRED_FEASIBILITY_QUEUE_PATH,
        OBSERVABILITY_CONTRACT_PATH,
        ALLOWED_OBSERVABILITY_CASES_PATH,
        CASE_MANIFEST_OBSERVABILITY_RULES_PATH,
        FORBIDDEN_OBSERVABILITY_CONTROL_CLAIMS_PATH,
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

    t3_receipt = read_json(T3_ADMISSIBILITY_RECEIPT_PATH)
    t3_summary = t3_receipt.get("machine_readable_t3_admissibility_contract_summary", {})
    t3_contract = read_json(T3_ADMISSIBILITY_CONTRACT_PATH)
    t3_allowed_case = read_json(T3_ADMISSIBILITY_ALLOWED_CASE_PATH)
    t3_shape = read_json(T3_ADMISSIBILITY_DEFERRED_SHAPE_PATH)
    t4_target = read_json(T4_TARGET_PATH)

    t3_schema_contract = read_json(T3_SCHEMA_CONTRACT_PATH)
    t3_schema_allowed_case = read_json(T3_SCHEMA_ALLOWED_CASE_PATH)

    readiness_index = read_json(DEFERRED_READINESS_INDEX_PATH)
    feasibility_queue = read_json(DEFERRED_FEASIBILITY_QUEUE_PATH)

    observability_contract = read_json(OBSERVABILITY_CONTRACT_PATH)
    allowed_observability_cases = read_json(ALLOWED_OBSERVABILITY_CASES_PATH)
    manifest_observability_rules = read_json(CASE_MANIFEST_OBSERVABILITY_RULES_PATH)
    forbidden_observability_claims = read_json(FORBIDDEN_OBSERVABILITY_CONTROL_CLAIMS_PATH)

    smoke_receipt = read_json(SMOKE_RECEIPT_PATH)
    smoke_summary = smoke_receipt.get("machine_readable_runtime_smoke_summary", {})
    smoke_state = read_json(SMOKE_STATE_PATH)
    smoke_schema = read_json(SMOKE_SCHEMA_PATH)
    smoke_registry = read_json(SMOKE_REGISTRY_PATH)

    if t3_receipt.get("receipt_id") != SOURCE_T3_ADMISSIBILITY_RECEIPT_ID:
        failures.append(f"t3_admissibility_receipt_id_wrong:{t3_receipt.get('receipt_id')}")
    if t3_receipt.get("gate") != "PASS":
        failures.append("t3_admissibility_gate_not_pass")
    if t3_summary.get("t3_admissibility_contract_done") is not True:
        failures.append("t3_admissibility_contract_not_done")
    if t3_summary.get("ready_for_t4_observability_gap_instance") is not True:
        failures.append("not_ready_for_t4_observability_gap_instance")
    if t3_summary.get("ready_for_deferred_suite_run") is not False:
        failures.append("deferred_suite_run_should_not_be_ready_yet")
    if t3_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("t3_admissibility_terminal_not_advance")
    if t3_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("t3_admissibility_terminal_next_wrong")

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
        "admissibility_widening_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(t3_summary, key, failures)

    t4_case = find_deferred_case(readiness_index, "T4.full_observability_required_gap")
    if not t4_case:
        failures.append("t4_required_observability_gap_missing_from_readiness_index")
    else:
        if t4_case.get("readiness_class") != "CONTRACT_EXISTS_NEEDS_CASE_INSTANCE":
            failures.append(f"t4_readiness_class_wrong:{t4_case.get('readiness_class')}")
        if t4_case.get("buildability") != "CASE_INSTANCE_PREP_READY":
            failures.append(f"t4_buildability_wrong:{t4_case.get('buildability')}")

    if t4_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"target_next_unit_wrong:{t4_target.get('next_unit_id')}")
    if t4_target.get("case_key") != "T4.full_observability_required_gap":
        failures.append(f"target_case_key_wrong:{t4_target.get('case_key')}")

    if t3_shape.get("ready_deferred_cases_after_this_unit") != ["T3.schema_validation_failure", "T3.admissibility_block"]:
        failures.append("t3_admissibility_shape_ready_list_unexpected")
    if "T4.full_observability_required_gap" not in t3_shape.get("still_needs_case_instance", []):
        failures.append("t4_gap_not_marked_still_needs_case_instance")

    obs_rows = allowed_cases(allowed_observability_cases)
    selected_obs_case = find_observability_required_gap_case(obs_rows)
    if not selected_obs_case:
        failures.append("allowed_t4_required_observability_gap_case_not_found")

    expected_pressure_class = None
    expected_outcome_class = None
    declared_observability_status = None
    if selected_obs_case:
        expected_pressure_class = selected_obs_case.get("expected_pressure_class") or selected_obs_case.get("pressure_class")
        expected_outcome_class = selected_obs_case.get("expected_outcome_class") or selected_obs_case.get("outcome_class")
        declared_observability_status = selected_obs_case.get("declared_observability_status") or selected_obs_case.get("observability_status")
        if not expected_pressure_class:
            failures.append("selected_t4_case_missing_expected_pressure_class")
        if declared_observability_status not in ["GAP_EXPECTED_PRESSURE", "REQUIRED_GAP_EXPECTED_PRESSURE", None]:
            failures.append(f"selected_t4_case_observability_status_unexpected:{declared_observability_status}")

    if expected_pressure_class is None:
        expected_pressure_class = "RUNTIME_OBSERVABILITY_GAP"
    if expected_outcome_class is None:
        expected_outcome_class = "RUNTIME_SMOKE_BLOCKED_REQUIRED_OBSERVABILITY_GAP"
    if declared_observability_status is None:
        declared_observability_status = "GAP_EXPECTED_PRESSURE"

    forbidden_text = json.dumps(forbidden_observability_claims, sort_keys=True)
    if "sidecar" not in forbidden_text.lower() and "control" not in forbidden_text.lower():
        failures.append("forbidden_observability_control_claims_not_visible")

    feasibility_items = feasibility_queue.get("queue", [])
    t6_keys = {item.get("case_key") for item in feasibility_items}
    if "T6.step_cap_loop_shape" not in t6_keys or "T6.move_tie_unresolved" not in t6_keys:
        failures.append("t6_feasibility_queue_incomplete")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_RUNTIME_T4_REQUIRED_OBSERVABILITY_GAP_CASE_INSTANCE_READY_T6_FEASIBILITY_NEXT" if gate == "PASS" else "TYPED_RUNTIME_T4_REQUIRED_OBSERVABILITY_GAP_CASE_INSTANCE_GATE_FAIL"

    gap_derivation = {
        "schema_version": "runtime_t4_required_observability_gap_derivation_v0",
        "derivation_status": "READY" if gate == "PASS" else "NOT_READY",
        "source_observability_contract_ref": rel(OBSERVABILITY_CONTRACT_PATH),
        "source_allowed_observability_case_ref": rel(ALLOWED_OBSERVABILITY_CASES_PATH),
        "source_state_ref": rel(SMOKE_STATE_PATH),
        "source_smoke_receipt_ref": rel(SMOKE_RECEIPT_PATH),
        "derivation_id": "required_observability_gap_missing_required_receipt_surface_v0",
        "derivation_kind": "DECLARE_REQUIRED_OBSERVABILITY_GAP",
        "declared_observability_status": declared_observability_status,
        "gap_surface": "required runtime observation/receipt surface intentionally unavailable for this declared case",
        "gap_written_by_suite_later": True,
        "gap_written_now": False,
        "sidecar_control_authority_granted": False,
        "runtime_control_authority_granted": False,
        "expected_terminal_type": "STOP",
        "expected_stop_code": "STOP_RUNTIME_REQUIRED_OBSERVABILITY_GAP",
        "expected_pressure_class": expected_pressure_class,
        "expected_outcome_class": expected_outcome_class,
        "repair_authorized": False,
        "sidecar_repair_authorized": False,
        "runtime_patch_authorized": False,
        "why_valid_negative_case": "The case requires an observation surface and declares that surface absent; the lawful outcome is typed observability-gap pressure, not sidecar control.",
    }

    case_instance = {
        "schema_version": "runtime_t4_required_observability_gap_case_instance_v0",
        "case_instance_status": "FROZEN_FOR_DEFERRED_SUITE_V0" if gate == "PASS" else "NOT_READY",
        "case_key": "T4.full_observability_required_gap",
        "tier": "T4",
        "source_t3_admissibility_receipt_ref": rel(T3_ADMISSIBILITY_RECEIPT_PATH),
        "source_observability_contract_ref": rel(OBSERVABILITY_CONTRACT_PATH),
        "selected_observability_contract_case": selected_obs_case,
        "gap_derivation_ref": rel(GAP_DERIVATION_PATH),
        "case_contract_id": "t4_required_observability_gap_missing_required_surface_v0",
        "case_role": "full_observability_required_gap",
        "expected_terminal": {
            "type": "STOP",
            "stop_code": "STOP_RUNTIME_REQUIRED_OBSERVABILITY_GAP",
            "next_unit_id": None,
        },
        "expected_pressure_class": expected_pressure_class,
        "expected_outcome_class": expected_outcome_class,
        "candidate_emission_only": True,
        "repair_inside_suite_authorized": False,
        "suite_may_continue_if_matched": True,
        "validation_order_requirement": [
            "load declared state",
            "validate declared state schema",
            "evaluate admissibility if present",
            "evaluate required observability surface",
            "stop before treating missing observation as runtime success",
            "emit typed pressure/readout/receipt",
        ],
        "must_not_infer": [
            "sidecar controls runtime",
            "sidecar may repair runtime",
            "observability gap authorizes runtime patching",
            "fixture expansion is authorized",
            "deferred suite is ready",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    allowed_case = {
        "schema_version": "runtime_allowed_t4_required_observability_gap_case_instance_v0",
        "catalog_status": "EMITTED" if gate == "PASS" else "NOT_READY",
        "allowed_case_count": 1 if gate == "PASS" else 0,
        "cases": [
            {
                "case_contract_id": "t4_required_observability_gap_missing_required_surface_v0",
                "case_key": "T4.full_observability_required_gap",
                "tier": "T4",
                "case_role": "full_observability_required_gap",
                "gap_derivation_ref": rel(GAP_DERIVATION_PATH),
                "expected_terminal_type": "STOP",
                "expected_stop_code": "STOP_RUNTIME_REQUIRED_OBSERVABILITY_GAP",
                "expected_pressure_class": expected_pressure_class,
                "expected_outcome_class": expected_outcome_class,
                "expected_trace_receipt_match": True,
                "expected_bad_counters_zero": True,
                "expected_refinement_candidate_count_min": 1,
                "suite_may_continue_if_matched": True,
                "repair_authorized": False,
                "sidecar_repair_authorized": False,
                "sidecar_control_authority": False,
                "runtime_patch_authorized": False,
                "fixture_expansion_authorized": False,
                "why_allowed": "Existing observability contract allowed a later required-gap expected-pressure case; this unit only binds the specific case instance.",
            }
        ],
    }

    manifest_rules = {
        "schema_version": "runtime_case_manifest_t4_required_observability_gap_rules_v0",
        "rules_status": "READY" if gate == "PASS" else "NOT_READY",
        "required_fields_for_t4_required_observability_gap_case": [
            "case_id",
            "tier",
            "case_name",
            "case_role",
            "runtime_state_ref",
            "gap_derivation_ref",
            "expected_terminal_type",
            "expected_stop_code",
            "expected_pressure_class",
            "expected_outcome_class",
            "expected_trace_receipt_match",
            "expected_bad_counters_zero",
            "repair_authorized",
            "sidecar_repair_authorized",
            "sidecar_control_authority",
            "runtime_patch_authorized",
        ],
        "required_false_for_t4_required_observability_gap_case": [
            "repair_authorized",
            "sidecar_repair_authorized",
            "sidecar_control_authority",
            "schema_creation_authorized",
            "taxonomy_creation_authorized",
            "fixture_expansion_authorized",
            "runtime_patch_authorized",
            "live_hook_install_authorized",
            "runtime_adoption_authorized",
            "c8_authorized",
        ],
        "ordering_rule": "required observability gap must be classified as observability pressure before the suite treats the case as clean",
        "candidate_rule": "emit candidate-only refinement record if required observability gap is real, underdeclared, mismatched, or not receipt-visible",
        "continuation_rule": "suite_may_continue only if expected stop, pressure, and outcome match exactly",
    }

    deferred_shape = {
        "schema_version": "runtime_deferred_suite_shape_after_t4_observability_gap_instance_v0",
        "shape_status": "PARTIAL_READY_T6_FEASIBILITY_AUDIT_NEXT" if gate == "PASS" else "NOT_READY",
        "ready_deferred_cases_after_this_unit": [
            "T3.schema_validation_failure",
            "T3.admissibility_block",
            "T4.full_observability_required_gap",
        ],
        "contracted_cases": [
            "T3.schema_validation_failure",
            "T3.admissibility_block",
        ],
        "case_instanced_cases": [
            "T4.full_observability_required_gap",
        ],
        "still_needs_contract": [],
        "still_needs_case_instance": [],
        "still_needs_feasibility_audit": [
            "T6.step_cap_loop_shape",
            "T6.move_tie_unresolved",
        ],
        "ready_for_t6_feasibility_audit": gate == "PASS",
        "ready_for_deferred_suite_run": False,
    }

    next_target = {
        "schema_version": "runtime_t6_loop_and_tie_trigger_feasibility_target_v0",
        "target_status": "T6_LOOP_AND_TIE_TRIGGER_FEASIBILITY_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "source_t4_observability_gap_case_instance_ref": rel(CASE_INSTANCE_PATH),
        "source_t4_allowed_case_ref": rel(ALLOWED_CASE_PATH),
        "case_keys": [
            "T6.step_cap_loop_shape",
            "T6.move_tie_unresolved",
        ],
        "target_role": "Audit whether the current runtime registry exposes lawful loop or tie trigger surfaces before any T6 case contract is prepared.",
        "forbidden": [
            "invent loop trigger",
            "invent move tie",
            "add moves",
            "patch runtime",
            "run deferred suite now",
            "expand fixtures by default",
            "authorize C8",
            "authorize live runtime adoption",
        ],
    }

    basis = {
        "schema_version": "runtime_t4_required_observability_gap_instance_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_t3_admissibility_receipt_id": SOURCE_T3_ADMISSIBILITY_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "T3 cases are contracted; T4 required observability gap already has an observability contract and now needs a bounded case instance.",
        "does_not_authorize": [
            "suite execution",
            "sidecar control authority",
            "sidecar repair",
            "runtime repair",
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
        "schema_version": "runtime_t4_required_observability_gap_instance_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "t4_observability_gap_instance_done": gate == "PASS",
        "allowed_t4_observability_gap_case_count": 1 if gate == "PASS" else 0,
        "gap_derivation_ready": gate == "PASS",
        "expected_pressure_class": expected_pressure_class,
        "expected_outcome_class": expected_outcome_class,
        "ready_for_t6_feasibility_audit": gate == "PASS",
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
        "sidecar_repair_authorized": False,
        "sidecar_control_authority": False,
        "move_addition_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    profile = {
        "schema_version": "runtime_t4_required_observability_gap_instance_profile_v0",
        "profile_status": status,
        "core_rule": "Required observability gap is expected pressure at the evidence boundary, not permission for the sidecar to control or repair runtime.",
        "case_instance_ref": rel(CASE_INSTANCE_PATH),
        "allowed_case_ref": rel(ALLOWED_CASE_PATH),
        "gap_derivation_ref": rel(GAP_DERIVATION_PATH),
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_RUNTIME_T4_REQUIRED_OBSERVABILITY_GAP_CASE_INSTANCE_V0",
        "must_not_infer": [
            "deferred suite is ready",
            "sidecar should control runtime",
            "sidecar should repair runtime",
            "runtime should be patched",
            "move should be added",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    trace = {
        "schema_version": "runtime_t4_required_observability_gap_instance_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "T3_ADMISSIBILITY_BLOCK_CONTRACT_READY_T4_OBSERVABILITY_NEXT",
                "edge": "consume T4 observability target and observability contract",
                "to": "T4_REQUIRED_OBSERVABILITY_GAP_INSTANCE_BASIS_ACCEPTED" if gate == "PASS" else "T4_REQUIRED_OBSERVABILITY_GAP_INSTANCE_GATE_FAIL",
            },
            {
                "from": "T4_REQUIRED_OBSERVABILITY_GAP_INSTANCE_BASIS_ACCEPTED" if gate == "PASS" else "T4_REQUIRED_OBSERVABILITY_GAP_INSTANCE_GATE_FAIL",
                "edge": "emit bounded T4 required-gap case instance",
                "to": "T6_LOOP_AND_TIE_FEASIBILITY_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_RUNTIME_T4_REQUIRED_OBSERVABILITY_GAP_CASE_INSTANCE_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (GAP_DERIVATION_PATH, gap_derivation),
        (CASE_INSTANCE_PATH, case_instance),
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
        status = "TYPED_RUNTIME_T4_REQUIRED_OBSERVABILITY_GAP_INSTANCE_SOURCE_MUTATION_FAIL"
        failures.append("source_inputs_mutated")

    reason_codes = [
        "T3_ADMISSIBILITY_CONTRACT_RECEIPT_CONSUMED",
        "T4_REQUIRED_OBSERVABILITY_GAP_TARGET_CONSUMED",
        "OBSERVABILITY_CONTRACT_CONSUMED",
        "REQUIRED_OBSERVABILITY_GAP_CASE_INSTANCE_DECLARED",
        "T4_REQUIRED_OBSERVABILITY_GAP_CASE_READY_FOR_DEFERRED_SUITE",
        "T6_LOOP_AND_TIE_FEASIBILITY_NEXT",
        "NO_SUITE_RUN",
        "NO_SIDECAR_CONTROL_AUTHORITY",
        "NO_SIDECAR_REPAIR",
        "NO_RUNTIME_PATCH",
        "NO_SCHEMA_INVENTION",
        "NO_TAXONOMY_INVENTION",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_LIVE_RUNTIME_ADOPTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_t4_required_observability_gap_case_instance_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_T4_REQUIRED_OBSERVABILITY_GAP_CASE_INSTANCE_RECEIPT",
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
        "source_t3_admissibility_receipt_id": SOURCE_T3_ADMISSIBILITY_RECEIPT_ID,
        "acceptance_gate_results": {
            "T4_OBS_GAP_0_T3_ADMISSIBILITY_RECEIPT_CONSUMED": gate == "PASS",
            "T4_OBS_GAP_1_TARGET_CONSUMED": gate == "PASS",
            "T4_OBS_GAP_2_OBSERVABILITY_CONTRACT_CONSUMED": gate == "PASS",
            "T4_OBS_GAP_3_GAP_DERIVATION_DECLARED": gate == "PASS",
            "T4_OBS_GAP_4_CASE_INSTANCE_EMITTED": gate == "PASS",
            "T4_OBS_GAP_5_ALLOWED_CASE_EMITTED": gate == "PASS",
            "T4_OBS_GAP_6_T6_FEASIBILITY_TARGET_NEXT": gate == "PASS",
            "T4_OBS_GAP_7_NO_SUITE_RUN": gate == "PASS",
            "T4_OBS_GAP_8_SOURCE_INPUTS_NOT_MUTATED": not source_mutated,
            "T4_OBS_GAP_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_t4_observability_gap_instance_summary": {
            "status": status,
            "t4_observability_gap_instance_done": gate == "PASS",
            "case_key": "T4.full_observability_required_gap",
            "gap_derivation_ready": gate == "PASS",
            "expected_pressure_class": expected_pressure_class,
            "expected_outcome_class": expected_outcome_class,
            "allowed_t4_observability_gap_case_count": 1 if gate == "PASS" else 0,
            "ready_for_t6_feasibility_audit": gate == "PASS",
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
            "sidecar_repair_authorized": False,
            "sidecar_control_authority": False,
            "move_addition_authorized": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "gap_derivation": rel(GAP_DERIVATION_PATH),
            "case_instance": rel(CASE_INSTANCE_PATH),
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
    print(f"runtime_t4_observability_gap_instance_receipt_id={receipt_id}")
    print(f"runtime_t4_observability_gap_instance_receipt_path={rel(receipt_path)}")
    print(f"runtime_t4_observability_gap_instance_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
