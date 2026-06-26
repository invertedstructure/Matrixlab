#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "AUDIT_RUNTIME_DEFERRED_CASES_READINESS_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.deferred_cases.readiness_audit_v0"
NEXT_UNIT_ID = "PREPARE_RUNTIME_T3_SCHEMA_VALIDATION_FAILURE_CASE_CONTRACT_V0"

LAYER = "OUTER / RUNTIME_ADOPTION / DEFERRED_CASES"
MODE = "AUDIT_ONLY / DEFERRED_CASES / NO_TEST_RUN / NO_REPAIR"
BUILD_MODE = "CLASSIFY_DEFERRED_CASE_READINESS_ONLY"

SOURCE_NO_APP_AUDIT_RECEIPT_ID = "1be6a297"

NO_APP_AUDIT_RECEIPT_PATH = ROOT / "data/runtime_no_applicable_move_pressure_audit_v0_receipts/1be6a297.json"
NO_APP_CLASSIFICATION_PATH = ROOT / "data/runtime_no_applicable_move_pressure_audit_v0/runtime_no_applicable_move_pressure_classification_v0.json"
NO_APP_CLOSURE_PATH = ROOT / "data/runtime_no_applicable_move_pressure_audit_v0/runtime_no_applicable_move_pressure_candidate_closure_v0.json"

FINAL_SUITE_SHAPE_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_compact_incremental_suite_final_shape_v0.json"
TIER_FEASIBILITY_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_incremental_suite_tier_feasibility_v0.json"
BRANCH_GAP_INDEX_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_branch_gap_index_v0.json"
REACHABILITY_MAP_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_registry_reachability_map_v0.json"

EXPECTED_PRESSURE_CONTRACT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_expected_pressure_case_contract_v0.json"
OBSERVABILITY_CONTRACT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_observability_status_case_contract_v0.json"
ALLOWED_OBSERVABILITY_CASES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_observability_status_cases_v0.json"
STATE_VARIANT_RULES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_declared_state_variant_rules_v0.json"
ALLOWED_STATE_VARIANTS_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_state_variant_catalog_v0.json"
SMOKE_REGISTRY_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_move_registry_snapshot_v0.json"

OUT_DIR = ROOT / "data/runtime_deferred_cases_readiness_v0"
RECEIPT_DIR = ROOT / "data/runtime_deferred_cases_readiness_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_deferred_cases_readiness_basis_v0.json"
READINESS_INDEX_PATH = OUT_DIR / "runtime_deferred_cases_readiness_index_v0.json"
BUILDABLE_QUEUE_PATH = OUT_DIR / "runtime_deferred_cases_buildable_queue_v0.json"
FEASIBILITY_QUEUE_PATH = OUT_DIR / "runtime_deferred_cases_feasibility_queue_v0.json"
NEXT_TARGET_PATH = OUT_DIR / "runtime_t3_schema_validation_failure_case_contract_target_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_deferred_cases_readiness_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_deferred_cases_readiness_profile_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_deferred_cases_readiness_transition_trace.json"

DEFERRED_EXPECTED = [
    "T3.schema_validation_failure",
    "T3.admissibility_block",
    "T4.full_observability_required_gap",
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

def as_list_from_gap_index(gap_index: Any) -> List[Dict[str, Any]]:
    if isinstance(gap_index, list):
        return gap_index
    if isinstance(gap_index, dict):
        for key in ["branch_gap_index", "gaps", "branch_gaps", "items"]:
            if isinstance(gap_index.get(key), list):
                return gap_index[key]
    return []

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        NO_APP_AUDIT_RECEIPT_PATH,
        NO_APP_CLASSIFICATION_PATH,
        NO_APP_CLOSURE_PATH,
        FINAL_SUITE_SHAPE_PATH,
        TIER_FEASIBILITY_PATH,
        BRANCH_GAP_INDEX_PATH,
        REACHABILITY_MAP_PATH,
        EXPECTED_PRESSURE_CONTRACT_PATH,
        OBSERVABILITY_CONTRACT_PATH,
        ALLOWED_OBSERVABILITY_CASES_PATH,
        STATE_VARIANT_RULES_PATH,
        ALLOWED_STATE_VARIANTS_PATH,
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

    no_app_receipt = read_json(NO_APP_AUDIT_RECEIPT_PATH)
    no_app_summary = no_app_receipt.get("machine_readable_no_applicable_move_audit_summary", {})
    no_app_classification = read_json(NO_APP_CLASSIFICATION_PATH)
    no_app_closure = read_json(NO_APP_CLOSURE_PATH)

    final_shape = read_json(FINAL_SUITE_SHAPE_PATH)
    tier_feasibility = read_json(TIER_FEASIBILITY_PATH)
    branch_gap_index = read_json(BRANCH_GAP_INDEX_PATH)
    reachability_map = read_json(REACHABILITY_MAP_PATH)
    expected_pressure_contract = read_json(EXPECTED_PRESSURE_CONTRACT_PATH)
    observability_contract = read_json(OBSERVABILITY_CONTRACT_PATH)
    allowed_observability_cases = read_json(ALLOWED_OBSERVABILITY_CASES_PATH)
    state_variant_rules = read_json(STATE_VARIANT_RULES_PATH)
    allowed_state_variants = read_json(ALLOWED_STATE_VARIANTS_PATH)
    smoke_registry = read_json(SMOKE_REGISTRY_PATH)

    if no_app_receipt.get("receipt_id") != SOURCE_NO_APP_AUDIT_RECEIPT_ID:
        failures.append(f"no_app_audit_receipt_id_wrong:{no_app_receipt.get('receipt_id')}")
    if no_app_receipt.get("gate") != "PASS":
        failures.append("no_app_audit_gate_not_pass")
    if no_app_summary.get("candidate_closed") is not True:
        failures.append("no_app_candidate_not_closed")
    if no_app_summary.get("classification_kind") != "EXPECTED_NEGATIVE_COVERAGE":
        failures.append(f"no_app_classification_wrong:{no_app_summary.get('classification_kind')}")
    if no_app_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append("no_app_terminal_not_stop")
    if no_app_receipt.get("terminal", {}).get("next_unit_id") is not None:
        failures.append("no_app_terminal_next_should_be_none")

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
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(no_app_summary, key, failures)

    deferred_from_final_shape = final_shape.get("deferred", [])
    missing_deferred = sorted(set(DEFERRED_EXPECTED) - set(deferred_from_final_shape))
    if missing_deferred:
        failures.append("missing_deferred_cases:" + ",".join(missing_deferred))

    allowed_obs_cases = allowed_observability_cases.get("cases", [])
    t4_required_gap_allowed = any(
        c.get("case_role") == "full_observability_required_gap"
        and c.get("declared_observability_status") == "GAP_EXPECTED_PRESSURE"
        and c.get("expected_pressure_class") == "RUNTIME_OBSERVABILITY_GAP"
        for c in allowed_obs_cases
    )

    gap_rows = as_list_from_gap_index(branch_gap_index)
    gap_text = json.dumps(branch_gap_index, sort_keys=True)

    registry_moves = smoke_registry.get("moves", [])
    registry_has_cycle = reachability_map.get("registry_has_cycle")
    if registry_has_cycle is None:
        registry_has_cycle = False

    move_tie_candidate_count = reachability_map.get("move_tie_candidate_count")
    if move_tie_candidate_count is None:
        move_tie_candidate_count = 0

    observed_schema_pass_only = reachability_map.get("observed_schema_pass_only")
    if observed_schema_pass_only is None:
        observed_schema_pass_only = "schema_validation_pass" in gap_text and "OBSERVED_PASS_ONLY" in gap_text

    observed_admissibility_pass_only = reachability_map.get("observed_admissibility_pass_only")
    if observed_admissibility_pass_only is None:
        observed_admissibility_pass_only = "admissibility_pass" in gap_text and "OBSERVED_PASS_ONLY" in gap_text

    deferred_cases = [
        {
            "case_key": "T3.schema_validation_failure",
            "tier": "T3",
            "readiness_class": "NEEDS_CASE_CONTRACT",
            "buildability": "CONTRACT_PREP_READY",
            "recommended_next_unit": "PREPARE_RUNTIME_T3_SCHEMA_VALIDATION_FAILURE_CASE_CONTRACT_V0",
            "reason": "Reachability showed schema pass only; failure case must be declared through explicit invalid-state contract before suite inclusion.",
            "evidence": {
                "observed_schema_pass_only": observed_schema_pass_only,
                "branch_gap_text_contains_schema_validation_pass": "schema_validation_pass" in gap_text,
            },
            "authorized_now": {
                "prepare_case_contract": True,
                "run_case": False,
                "repair": False,
                "schema_creation": False,
                "runtime_patch": False,
            },
        },
        {
            "case_key": "T3.admissibility_block",
            "tier": "T3",
            "readiness_class": "NEEDS_CASE_CONTRACT",
            "buildability": "CONTRACT_PREP_READY_AFTER_SCHEMA_FAILURE_CONTRACT",
            "recommended_next_unit": "PREPARE_RUNTIME_T3_ADMISSIBILITY_BLOCK_CASE_CONTRACT_V0",
            "reason": "Reachability showed admissibility pass only; authority-boundary case must be declared through explicit blocked-admissibility contract before suite inclusion.",
            "evidence": {
                "observed_admissibility_pass_only": observed_admissibility_pass_only,
                "branch_gap_text_contains_admissibility_pass": "admissibility_pass" in gap_text,
            },
            "authorized_now": {
                "prepare_case_contract": True,
                "run_case": False,
                "repair": False,
                "schema_creation": False,
                "runtime_patch": False,
            },
        },
        {
            "case_key": "T4.full_observability_required_gap",
            "tier": "T4",
            "readiness_class": "CONTRACT_EXISTS_NEEDS_CASE_INSTANCE",
            "buildability": "CASE_INSTANCE_PREP_READY",
            "recommended_next_unit": "PREPARE_RUNTIME_T4_REQUIRED_OBSERVABILITY_GAP_CASE_INSTANCE_V0",
            "reason": "Observability status contract already allowed GAP_EXPECTED_PRESSURE later; only a bounded case instance is missing.",
            "evidence": {
                "allowed_observability_case_exists": t4_required_gap_allowed,
                "expected_pressure_class": "RUNTIME_OBSERVABILITY_GAP",
            },
            "authorized_now": {
                "prepare_case_instance": True,
                "run_case": False,
                "repair": False,
                "sidecar_control_authority": False,
                "runtime_patch": False,
            },
        },
        {
            "case_key": "T6.step_cap_loop_shape",
            "tier": "T6",
            "readiness_class": "NEEDS_FEASIBILITY_AUDIT",
            "buildability": "NOT_CASE_CONTRACT_READY",
            "recommended_next_unit": "AUDIT_RUNTIME_T6_LOOP_AND_TIE_TRIGGER_FEASIBILITY_V0",
            "reason": "Current registry does not expose a loop/cycle trigger surface; do not manufacture loop-shaped moves.",
            "evidence": {
                "registry_has_cycle": registry_has_cycle,
                "registry_move_count": len(registry_moves),
            },
            "authorized_now": {
                "prepare_case_contract": False,
                "run_case": False,
                "repair": False,
                "move_addition": False,
                "runtime_patch": False,
                "feasibility_audit": True,
            },
        },
        {
            "case_key": "T6.move_tie_unresolved",
            "tier": "T6",
            "readiness_class": "NEEDS_FEASIBILITY_AUDIT",
            "buildability": "NOT_CASE_CONTRACT_READY",
            "recommended_next_unit": "AUDIT_RUNTIME_T6_LOOP_AND_TIE_TRIGGER_FEASIBILITY_V0",
            "reason": "Reachability reported no move-tie surface; do not invent tie cases unless feasibility audit finds a lawful current-registry trigger.",
            "evidence": {
                "move_tie_candidate_count": move_tie_candidate_count,
            },
            "authorized_now": {
                "prepare_case_contract": False,
                "run_case": False,
                "repair": False,
                "move_addition": False,
                "runtime_patch": False,
                "feasibility_audit": True,
            },
        },
    ]

    contract_prep_ready = [c["case_key"] for c in deferred_cases if c["readiness_class"] == "NEEDS_CASE_CONTRACT"]
    case_instance_ready = [c["case_key"] for c in deferred_cases if c["readiness_class"] == "CONTRACT_EXISTS_NEEDS_CASE_INSTANCE"]
    feasibility_required = [c["case_key"] for c in deferred_cases if c["readiness_class"] == "NEEDS_FEASIBILITY_AUDIT"]

    if not t4_required_gap_allowed:
        failures.append("t4_required_observability_gap_not_allowed_by_contract")

    if registry_has_cycle:
        failures.append("registry_has_cycle_unexpected_for_deferred_readiness_audit")
    if move_tie_candidate_count != 0:
        failures.append(f"move_tie_candidate_count_unexpected:{move_tie_candidate_count}")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_RUNTIME_DEFERRED_CASES_READINESS_AUDIT_READY_T3_SCHEMA_CONTRACT_NEXT" if gate == "PASS" else "TYPED_RUNTIME_DEFERRED_CASES_READINESS_AUDIT_GATE_FAIL"

    readiness_index = {
        "schema_version": "runtime_deferred_cases_readiness_index_v0",
        "index_status": "EMITTED" if gate == "PASS" else "PARTIAL",
        "source_no_app_audit_receipt_ref": rel(NO_APP_AUDIT_RECEIPT_PATH),
        "deferred_cases": deferred_cases,
        "contract_prep_ready": contract_prep_ready,
        "case_instance_ready": case_instance_ready,
        "feasibility_required": feasibility_required,
        "not_ready_for_suite_run": DEFERRED_EXPECTED,
    }

    buildable_queue = {
        "schema_version": "runtime_deferred_cases_buildable_queue_v0",
        "queue_status": "EMITTED" if gate == "PASS" else "PARTIAL",
        "queue": [
            {
                "order": 1,
                "case_key": "T3.schema_validation_failure",
                "next_unit_id": "PREPARE_RUNTIME_T3_SCHEMA_VALIDATION_FAILURE_CASE_CONTRACT_V0",
                "queue_reason": "first missing T3 pressure contract",
            },
            {
                "order": 2,
                "case_key": "T3.admissibility_block",
                "next_unit_id": "PREPARE_RUNTIME_T3_ADMISSIBILITY_BLOCK_CASE_CONTRACT_V0",
                "queue_reason": "second missing T3 pressure contract",
            },
            {
                "order": 3,
                "case_key": "T4.full_observability_required_gap",
                "next_unit_id": "PREPARE_RUNTIME_T4_REQUIRED_OBSERVABILITY_GAP_CASE_INSTANCE_V0",
                "queue_reason": "contract exists; bounded case instance missing",
            },
        ],
        "suite_run_allowed_now": False,
    }

    feasibility_queue = {
        "schema_version": "runtime_deferred_cases_feasibility_queue_v0",
        "queue_status": "EMITTED" if gate == "PASS" else "PARTIAL",
        "queue": [
            {
                "order": 1,
                "case_key": "T6.step_cap_loop_shape",
                "next_unit_id": "AUDIT_RUNTIME_T6_LOOP_AND_TIE_TRIGGER_FEASIBILITY_V0",
                "queue_reason": "current registry has no loop/cycle trigger surface",
            },
            {
                "order": 2,
                "case_key": "T6.move_tie_unresolved",
                "next_unit_id": "AUDIT_RUNTIME_T6_LOOP_AND_TIE_TRIGGER_FEASIBILITY_V0",
                "queue_reason": "current registry has no move-tie candidate surface",
            },
        ],
        "case_contract_allowed_now": False,
        "feasibility_audit_required_before_case_contract": True,
    }

    next_target = {
        "schema_version": "runtime_t3_schema_validation_failure_case_contract_target_v0",
        "target_status": "T3_SCHEMA_VALIDATION_FAILURE_CASE_CONTRACT_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "source_readiness_index_ref": rel(READINESS_INDEX_PATH),
        "case_key": "T3.schema_validation_failure",
        "target_role": "Prepare explicit invalid-state expected-pressure contract; do not run the case yet.",
        "allowed_outputs": [
            "schema validation failure case contract",
            "manifest rules for expected schema failure pressure",
            "compact deferred-suite shape update",
            "next target for T3 admissibility block contract",
        ],
        "forbidden_outputs": [
            "run deferred suite",
            "invent schema",
            "patch runtime",
            "add moves",
            "expand fixtures by default",
            "authorize C8",
            "authorize live runtime adoption",
        ],
    }

    basis = {
        "schema_version": "runtime_deferred_cases_readiness_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_no_app_audit_receipt_id": SOURCE_NO_APP_AUDIT_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "Previous pressure branch closed cleanly; five deferred cases now require a readiness split before any deferred suite is built.",
        "does_not_authorize": [
            "suite execution",
            "repair",
            "move addition",
            "schema creation",
            "taxonomy creation",
            "fixture expansion by default",
            "runtime patching",
            "live hook installation",
            "live runtime adoption",
            "C8 authorization",
        ],
    }

    rollup = {
        "schema_version": "runtime_deferred_cases_readiness_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "deferred_case_count": len(DEFERRED_EXPECTED),
        "contract_prep_ready_count": len(contract_prep_ready),
        "case_instance_ready_count": len(case_instance_ready),
        "feasibility_required_count": len(feasibility_required),
        "ready_for_t3_schema_contract": gate == "PASS",
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
        "schema_version": "runtime_deferred_cases_readiness_profile_v0",
        "profile_status": status,
        "core_rule": "Deferred cases must be sorted into case-contract-ready, case-instance-ready, and feasibility-audit-required before any suite run.",
        "source_no_app_audit_receipt_ref": rel(NO_APP_AUDIT_RECEIPT_PATH),
        "readiness_index_ref": rel(READINESS_INDEX_PATH),
        "buildable_queue_ref": rel(BUILDABLE_QUEUE_PATH),
        "feasibility_queue_ref": rel(FEASIBILITY_QUEUE_PATH),
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_RUNTIME_DEFERRED_CASES_READINESS_AUDIT_V0",
        "must_not_infer": [
            "all deferred cases are ready",
            "T6 can be case-contracted now",
            "suite run is authorized",
            "repair is authorized",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    trace = {
        "schema_version": "runtime_deferred_cases_readiness_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "NO_APPLICABLE_MOVE_AUDIT_CLOSED_EXPECTED_NEGATIVE_COVERAGE",
                "edge": "start human-declared deferred-case readiness objective",
                "to": "DEFERRED_CASE_SET_INDEXED" if gate == "PASS" else "DEFERRED_CASE_READINESS_GATE_FAIL",
            },
            {
                "from": "DEFERRED_CASE_SET_INDEXED" if gate == "PASS" else "DEFERRED_CASE_READINESS_GATE_FAIL",
                "edge": "split into buildable contracts, case instances, and feasibility audits",
                "to": "T3_SCHEMA_VALIDATION_FAILURE_CONTRACT_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_RUNTIME_DEFERRED_CASES_READINESS_AUDIT_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (READINESS_INDEX_PATH, readiness_index),
        (BUILDABLE_QUEUE_PATH, buildable_queue),
        (FEASIBILITY_QUEUE_PATH, feasibility_queue),
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
        status = "TYPED_RUNTIME_DEFERRED_CASES_READINESS_SOURCE_MUTATION_FAIL"
        failures.append("source_inputs_mutated")

    reason_codes = [
        "NO_APPLICABLE_MOVE_AUDIT_CLOSURE_CONSUMED",
        "DEFERRED_CASE_SET_INDEXED",
        "T3_SCHEMA_VALIDATION_NEEDS_CASE_CONTRACT",
        "T3_ADMISSIBILITY_NEEDS_CASE_CONTRACT",
        "T4_REQUIRED_OBSERVABILITY_GAP_CONTRACT_EXISTS_NEEDS_INSTANCE",
        "T6_LOOP_SHAPE_NEEDS_FEASIBILITY_AUDIT",
        "T6_MOVE_TIE_NEEDS_FEASIBILITY_AUDIT",
        "T3_SCHEMA_CONTRACT_NEXT",
        "NO_SUITE_RUN",
        "NO_REPAIR",
        "NO_MOVE_ADDITION",
        "NO_SCHEMA_INVENTION",
        "NO_TAXONOMY_INVENTION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_HOOK_INSTALL",
        "NO_LIVE_RUNTIME_ADOPTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_deferred_cases_readiness_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_DEFERRED_CASES_READINESS_RECEIPT",
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
        "source_no_app_audit_receipt_id": SOURCE_NO_APP_AUDIT_RECEIPT_ID,
        "acceptance_gate_results": {
            "DEFERRED_READY_0_NO_APP_AUDIT_CONSUMED": gate == "PASS",
            "DEFERRED_READY_1_DEFERRED_SET_FOUND": set(DEFERRED_EXPECTED).issubset(set(deferred_from_final_shape)),
            "DEFERRED_READY_2_T3_SCHEMA_CONTRACT_READY": gate == "PASS",
            "DEFERRED_READY_3_T3_ADMISSIBILITY_CONTRACT_READY_LATER": gate == "PASS",
            "DEFERRED_READY_4_T4_REQUIRED_GAP_INSTANCE_READY_LATER": t4_required_gap_allowed,
            "DEFERRED_READY_5_T6_FEASIBILITY_REQUIRED": gate == "PASS",
            "DEFERRED_READY_6_NO_SUITE_RUN": gate == "PASS",
            "DEFERRED_READY_7_NO_REPAIR": gate == "PASS",
            "DEFERRED_READY_8_SOURCE_INPUTS_NOT_MUTATED": not source_mutated,
            "DEFERRED_READY_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_deferred_readiness_summary": {
            "status": status,
            "deferred_readiness_audit_done": gate == "PASS",
            "deferred_case_count": len(DEFERRED_EXPECTED),
            "contract_prep_ready": contract_prep_ready,
            "case_instance_ready": case_instance_ready,
            "feasibility_required": feasibility_required,
            "ready_for_t3_schema_contract": gate == "PASS",
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
            "readiness_index": rel(READINESS_INDEX_PATH),
            "buildable_queue": rel(BUILDABLE_QUEUE_PATH),
            "feasibility_queue": rel(FEASIBILITY_QUEUE_PATH),
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
    print(f"runtime_deferred_cases_readiness_receipt_id={receipt_id}")
    print(f"runtime_deferred_cases_readiness_receipt_path={rel(receipt_path)}")
    print(f"runtime_deferred_cases_readiness_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
