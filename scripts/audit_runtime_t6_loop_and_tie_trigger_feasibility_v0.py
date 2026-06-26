#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "AUDIT_RUNTIME_T6_LOOP_AND_TIE_TRIGGER_FEASIBILITY_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.deferred_cases.t6_loop_and_tie_feasibility_v0"
NEXT_UNIT_ID = "BUILD_OUTER_RUNTIME_DEFERRED_PRESSURE_TEST_SUITE_V0"

LAYER = "OUTER / RUNTIME_ADOPTION / DEFERRED_CASES / T6"
MODE = "AUDIT_ONLY / LOOP_AND_TIE_TRIGGER_FEASIBILITY / NO_CASE_CONTRACT / NO_TEST_RUN"
BUILD_MODE = "T6_FEASIBILITY_AUDIT_ONLY"

SOURCE_T4_OBS_RECEIPT_ID = "6ea9018e"

T4_OBS_RECEIPT_PATH = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0_receipts/6ea9018e.json"
T4_CASE_INSTANCE_PATH = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0/runtime_t4_required_observability_gap_case_instance_v0.json"
T4_ALLOWED_CASE_PATH = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0/runtime_allowed_t4_required_observability_gap_case_instance_v0.json"
T4_DEFERRED_SHAPE_PATH = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0/runtime_deferred_suite_shape_after_t4_observability_gap_instance_v0.json"
T6_TARGET_PATH = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0/runtime_t6_loop_and_tie_trigger_feasibility_target_v0.json"

T3_SCHEMA_CONTRACT_PATH = ROOT / "data/runtime_deferred_cases_t3_schema_contract_v0/runtime_t3_schema_validation_failure_case_contract_v0.json"
T3_SCHEMA_ALLOWED_CASE_PATH = ROOT / "data/runtime_deferred_cases_t3_schema_contract_v0/runtime_allowed_t3_schema_validation_failure_case_v0.json"
T3_ADMISSIBILITY_CONTRACT_PATH = ROOT / "data/runtime_deferred_cases_t3_admissibility_contract_v0/runtime_t3_admissibility_block_case_contract_v0.json"
T3_ADMISSIBILITY_ALLOWED_CASE_PATH = ROOT / "data/runtime_deferred_cases_t3_admissibility_contract_v0/runtime_allowed_t3_admissibility_block_case_v0.json"

DEFERRED_READINESS_INDEX_PATH = ROOT / "data/runtime_deferred_cases_readiness_v0/runtime_deferred_cases_readiness_index_v0.json"
DEFERRED_FEASIBILITY_QUEUE_PATH = ROOT / "data/runtime_deferred_cases_readiness_v0/runtime_deferred_cases_feasibility_queue_v0.json"

REACHABILITY_MAP_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_registry_reachability_map_v0.json"
BRANCH_GAP_INDEX_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_branch_gap_index_v0.json"
TIER_FEASIBILITY_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_incremental_suite_tier_feasibility_v0.json"
SMOKE_REGISTRY_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_move_registry_snapshot_v0.json"

OUT_DIR = ROOT / "data/runtime_deferred_cases_t6_feasibility_v0"
RECEIPT_DIR = ROOT / "data/runtime_deferred_cases_t6_feasibility_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_t6_loop_and_tie_feasibility_basis_v0.json"
REGISTRY_PROFILE_PATH = OUT_DIR / "runtime_t6_current_registry_trigger_profile_v0.json"
LOOP_AUDIT_PATH = OUT_DIR / "runtime_t6_step_cap_loop_trigger_audit_v0.json"
TIE_AUDIT_PATH = OUT_DIR / "runtime_t6_move_tie_trigger_audit_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "runtime_t6_loop_and_tie_feasibility_classification_v0.json"
DEFERRED_SHAPE_PATH = OUT_DIR / "runtime_deferred_suite_shape_after_t6_feasibility_audit_v0.json"
SUITE_BUILD_TARGET_PATH = OUT_DIR / "runtime_deferred_pressure_suite_build_target_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_t6_loop_and_tie_feasibility_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_t6_loop_and_tie_feasibility_profile_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_t6_loop_and_tie_feasibility_transition_trace.json"

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

def as_list(value: Any) -> List[Any]:
    return value if isinstance(value, list) else []

def registry_moves(registry: Dict[str, Any]) -> List[Dict[str, Any]]:
    for key in ["moves", "registry_moves", "move_registry"]:
        if isinstance(registry.get(key), list):
            return registry[key]
    return []

def find_case(index: Dict[str, Any], case_key: str) -> Optional[Dict[str, Any]]:
    for row in index.get("deferred_cases", []):
        if row.get("case_key") == case_key:
            return row
    return None

def text_contains_any(obj: Any, needles: List[str]) -> bool:
    text = json.dumps(obj, sort_keys=True).lower()
    return any(n.lower() in text for n in needles)

def int_or_zero(v: Any) -> int:
    try:
        return int(v)
    except Exception:
        return 0

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        T4_OBS_RECEIPT_PATH,
        T4_CASE_INSTANCE_PATH,
        T4_ALLOWED_CASE_PATH,
        T4_DEFERRED_SHAPE_PATH,
        T6_TARGET_PATH,
        T3_SCHEMA_CONTRACT_PATH,
        T3_SCHEMA_ALLOWED_CASE_PATH,
        T3_ADMISSIBILITY_CONTRACT_PATH,
        T3_ADMISSIBILITY_ALLOWED_CASE_PATH,
        DEFERRED_READINESS_INDEX_PATH,
        DEFERRED_FEASIBILITY_QUEUE_PATH,
        REACHABILITY_MAP_PATH,
        BRANCH_GAP_INDEX_PATH,
        TIER_FEASIBILITY_PATH,
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

    t4_receipt = read_json(T4_OBS_RECEIPT_PATH)
    t4_summary = t4_receipt.get("machine_readable_t4_observability_gap_instance_summary", {})
    t4_case_instance = read_json(T4_CASE_INSTANCE_PATH)
    t4_allowed_case = read_json(T4_ALLOWED_CASE_PATH)
    t4_shape = read_json(T4_DEFERRED_SHAPE_PATH)
    t6_target = read_json(T6_TARGET_PATH)

    t3_schema_contract = read_json(T3_SCHEMA_CONTRACT_PATH)
    t3_schema_allowed_case = read_json(T3_SCHEMA_ALLOWED_CASE_PATH)
    t3_admissibility_contract = read_json(T3_ADMISSIBILITY_CONTRACT_PATH)
    t3_admissibility_allowed_case = read_json(T3_ADMISSIBILITY_ALLOWED_CASE_PATH)

    readiness_index = read_json(DEFERRED_READINESS_INDEX_PATH)
    feasibility_queue = read_json(DEFERRED_FEASIBILITY_QUEUE_PATH)
    reachability_map = read_json(REACHABILITY_MAP_PATH)
    branch_gap_index = read_json(BRANCH_GAP_INDEX_PATH)
    tier_feasibility = read_json(TIER_FEASIBILITY_PATH)
    smoke_registry = read_json(SMOKE_REGISTRY_PATH)

    if t4_receipt.get("receipt_id") != SOURCE_T4_OBS_RECEIPT_ID:
        failures.append(f"t4_receipt_id_wrong:{t4_receipt.get('receipt_id')}")
    if t4_receipt.get("gate") != "PASS":
        failures.append("t4_gate_not_pass")
    if t4_summary.get("t4_observability_gap_instance_done") is not True:
        failures.append("t4_observability_gap_instance_not_done")
    if t4_summary.get("ready_for_t6_feasibility_audit") is not True:
        failures.append("not_ready_for_t6_feasibility_audit")
    if t4_summary.get("ready_for_deferred_suite_run") is not False:
        failures.append("deferred_suite_run_should_not_be_ready_before_t6_audit")
    if t4_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("t4_terminal_not_advance")
    if t4_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("t4_terminal_next_wrong")

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
        "sidecar_repair_authorized",
        "sidecar_control_authority",
        "move_addition_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(t4_summary, key, failures)

    t6_loop_case = find_case(readiness_index, "T6.step_cap_loop_shape")
    t6_tie_case = find_case(readiness_index, "T6.move_tie_unresolved")
    if not t6_loop_case:
        failures.append("t6_loop_case_missing_from_readiness_index")
    if not t6_tie_case:
        failures.append("t6_tie_case_missing_from_readiness_index")
    for label, row in [("loop", t6_loop_case), ("tie", t6_tie_case)]:
        if row:
            if row.get("readiness_class") != "NEEDS_FEASIBILITY_AUDIT":
                failures.append(f"t6_{label}_readiness_class_wrong:{row.get('readiness_class')}")
            if row.get("buildability") != "NOT_CASE_CONTRACT_READY":
                failures.append(f"t6_{label}_buildability_wrong:{row.get('buildability')}")

    if t6_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"t6_target_next_unit_wrong:{t6_target.get('next_unit_id')}")

    target_case_keys = set(t6_target.get("case_keys", []))
    if "T6.step_cap_loop_shape" not in target_case_keys:
        failures.append("t6_loop_missing_from_target_case_keys")
    if "T6.move_tie_unresolved" not in target_case_keys:
        failures.append("t6_tie_missing_from_target_case_keys")

    feasibility_items = feasibility_queue.get("queue", [])
    feasibility_keys = {item.get("case_key") for item in feasibility_items}
    if "T6.step_cap_loop_shape" not in feasibility_keys:
        failures.append("t6_loop_missing_from_feasibility_queue")
    if "T6.move_tie_unresolved" not in feasibility_keys:
        failures.append("t6_tie_missing_from_feasibility_queue")

    if t4_shape.get("ready_deferred_cases_after_this_unit") != [
        "T3.schema_validation_failure",
        "T3.admissibility_block",
        "T4.full_observability_required_gap",
    ]:
        failures.append("t4_shape_ready_list_unexpected")

    moves = registry_moves(smoke_registry)
    move_count = len(moves)

    registry_has_cycle = reachability_map.get("registry_has_cycle")
    if registry_has_cycle is None:
        registry_has_cycle = bool(reachability_map.get("cycle_count")) or bool(reachability_map.get("cycles"))

    loop_trigger_candidate_count = int_or_zero(reachability_map.get("loop_trigger_candidate_count"))
    step_cap_trigger_candidate_count = int_or_zero(reachability_map.get("step_cap_trigger_candidate_count"))

    if loop_trigger_candidate_count == 0 and isinstance(reachability_map.get("loop_trigger_candidates"), list):
        loop_trigger_candidate_count = len(reachability_map.get("loop_trigger_candidates", []))
    if step_cap_trigger_candidate_count == 0 and isinstance(reachability_map.get("step_cap_trigger_candidates"), list):
        step_cap_trigger_candidate_count = len(reachability_map.get("step_cap_trigger_candidates", []))

    move_tie_candidate_count = reachability_map.get("move_tie_candidate_count")
    if move_tie_candidate_count is None:
        move_tie_candidate_count = 0
        seen = {}
        for m in moves:
            applies = json.dumps(m.get("applies_when", {}), sort_keys=True)
            priority = m.get("priority", m.get("rank", m.get("order", None)))
            if priority is not None:
                key = (applies, priority)
                seen[key] = seen.get(key, 0) + 1
        move_tie_candidate_count = sum(1 for count in seen.values() if count > 1)

    tie_trigger_candidates = []
    if isinstance(reachability_map.get("move_tie_candidates"), list):
        tie_trigger_candidates = reachability_map["move_tie_candidates"]

    branch_gap_text = json.dumps(branch_gap_index, sort_keys=True)
    tier_feasibility_text = json.dumps(tier_feasibility, sort_keys=True)
    registry_text = json.dumps(smoke_registry, sort_keys=True)

    explicit_loop_surface_visible = text_contains_any(
        smoke_registry,
        [
            "loop_trigger",
            "cycle_trigger",
            "step_cap_loop",
            "loop_shape",
            "repeat_until_step_cap",
        ],
    )

    explicit_tie_surface_visible = text_contains_any(
        smoke_registry,
        [
            "move_tie",
            "tie_unresolved",
            "ambiguous_move",
            "same_priority",
            "tie_break",
        ],
    )

    loop_trigger_available = bool(registry_has_cycle) or loop_trigger_candidate_count > 0 or step_cap_trigger_candidate_count > 0 or explicit_loop_surface_visible
    tie_trigger_available = int_or_zero(move_tie_candidate_count) > 0 or bool(tie_trigger_candidates) or explicit_tie_surface_visible

    # The current expected result is no lawful T6 trigger surface. If a trigger appears, stop for a human
    # case-contract decision instead of silently using it.
    unexpected_trigger_found = loop_trigger_available or tie_trigger_available
    if unexpected_trigger_found:
        failures.append("t6_trigger_surface_found_requires_human_contract_decision")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_RUNTIME_T6_LOOP_AND_TIE_FEASIBILITY_AUDIT_NO_CURRENT_TRIGGER_DEFERRED_SUITE_BUILD_NEXT"
        if gate == "PASS"
        else "TYPED_RUNTIME_T6_LOOP_AND_TIE_FEASIBILITY_AUDIT_GATE_FAIL"
    )

    registry_profile = {
        "schema_version": "runtime_t6_current_registry_trigger_profile_v0",
        "profile_status": "EMITTED" if gate == "PASS" else "PARTIAL",
        "source_reachability_map_ref": rel(REACHABILITY_MAP_PATH),
        "source_registry_ref": rel(SMOKE_REGISTRY_PATH),
        "registry_move_count": move_count,
        "registry_has_cycle": bool(registry_has_cycle),
        "loop_trigger_candidate_count": loop_trigger_candidate_count,
        "step_cap_trigger_candidate_count": step_cap_trigger_candidate_count,
        "explicit_loop_surface_visible": explicit_loop_surface_visible,
        "move_tie_candidate_count": int_or_zero(move_tie_candidate_count),
        "explicit_tie_surface_visible": explicit_tie_surface_visible,
        "loop_trigger_available": loop_trigger_available,
        "tie_trigger_available": tie_trigger_available,
        "reading": "Current registry exposes no lawful loop/tie trigger surface for T6 case construction." if gate == "PASS" else "A possible T6 trigger surface was detected or an audit basis failed; human decision required before contracting T6.",
    }

    loop_audit = {
        "schema_version": "runtime_t6_step_cap_loop_trigger_audit_v0",
        "case_key": "T6.step_cap_loop_shape",
        "audit_status": "NO_CURRENT_REGISTRY_TRIGGER" if gate == "PASS" else "NOT_CLOSED",
        "trigger_available": loop_trigger_available,
        "registry_has_cycle": bool(registry_has_cycle),
        "loop_trigger_candidate_count": loop_trigger_candidate_count,
        "step_cap_trigger_candidate_count": step_cap_trigger_candidate_count,
        "explicit_loop_surface_visible": explicit_loop_surface_visible,
        "case_contract_authorized": False,
        "move_addition_authorized": False,
        "runtime_patch_authorized": False,
        "classification": "DEFERRED_CURRENT_REGISTRY_NO_TRIGGER" if gate == "PASS" else "REQUIRES_HUMAN_DECISION",
        "lawful_handling": "exclude from this deferred suite build; preserve as later registry-variant objective" if gate == "PASS" else "do not contract automatically",
    }

    tie_audit = {
        "schema_version": "runtime_t6_move_tie_trigger_audit_v0",
        "case_key": "T6.move_tie_unresolved",
        "audit_status": "NO_CURRENT_REGISTRY_TRIGGER" if gate == "PASS" else "NOT_CLOSED",
        "trigger_available": tie_trigger_available,
        "move_tie_candidate_count": int_or_zero(move_tie_candidate_count),
        "explicit_tie_surface_visible": explicit_tie_surface_visible,
        "case_contract_authorized": False,
        "move_addition_authorized": False,
        "runtime_patch_authorized": False,
        "classification": "DEFERRED_CURRENT_REGISTRY_NO_TRIGGER" if gate == "PASS" else "REQUIRES_HUMAN_DECISION",
        "lawful_handling": "exclude from this deferred suite build; preserve as later registry-variant objective" if gate == "PASS" else "do not contract automatically",
    }

    classification = {
        "schema_version": "runtime_t6_loop_and_tie_feasibility_classification_v0",
        "classification_status": "T6_CURRENT_REGISTRY_NO_TRIGGER" if gate == "PASS" else "T6_FEASIBILITY_NOT_CLOSED",
        "t6_cases": [
            {
                "case_key": "T6.step_cap_loop_shape",
                "classification": loop_audit["classification"],
                "case_contract_ready": False,
                "case_contract_authorized": False,
                "included_in_deferred_suite_build": False,
                "preserved_for_later": True,
            },
            {
                "case_key": "T6.move_tie_unresolved",
                "classification": tie_audit["classification"],
                "case_contract_ready": False,
                "case_contract_authorized": False,
                "included_in_deferred_suite_build": False,
                "preserved_for_later": True,
            },
        ],
        "ready_cases_for_deferred_suite_build": [
            "T3.schema_validation_failure",
            "T3.admissibility_block",
            "T4.full_observability_required_gap",
        ],
        "excluded_cases_from_this_suite_build": [
            "T6.step_cap_loop_shape",
            "T6.move_tie_unresolved",
        ],
        "decision_law": "Do not manufacture loop/tie triggers. If the current registry has no lawful trigger surface, T6 remains deferred and the suite may build over the ready T3/T4 cases.",
    }

    deferred_shape = {
        "schema_version": "runtime_deferred_suite_shape_after_t6_feasibility_audit_v0",
        "shape_status": "READY_FOR_DEFERRED_PRESSURE_SUITE_BUILD_T3_T4_ONLY" if gate == "PASS" else "NOT_READY",
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
        "excluded_current_registry_no_trigger": [
            "T6.step_cap_loop_shape",
            "T6.move_tie_unresolved",
        ],
        "still_needs_contract": [],
        "still_needs_case_instance": [],
        "still_needs_feasibility_audit": [],
        "ready_for_deferred_suite_build": gate == "PASS",
        "ready_for_deferred_suite_run": False,
    }

    suite_build_target = {
        "schema_version": "runtime_deferred_pressure_suite_build_target_v0",
        "target_status": "DEFERRED_PRESSURE_SUITE_BUILD_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "source_t6_feasibility_classification_ref": rel(CLASSIFICATION_PATH),
        "suite_scope": "T3_T4_READY_CASES_ONLY",
        "include_cases": [
            "T3.schema_validation_failure",
            "T3.admissibility_block",
            "T4.full_observability_required_gap",
        ],
        "exclude_cases": [
            "T6.step_cap_loop_shape",
            "T6.move_tie_unresolved",
        ],
        "exclude_reason": "No lawful loop/tie trigger surface exists in the current registry.",
        "target_role": "Build and run the deferred pressure suite over the three ready expected-pressure cases only.",
        "forbidden": [
            "include T6 without trigger",
            "invent loop trigger",
            "invent move tie",
            "add moves",
            "patch runtime",
            "expand fixtures by default",
            "authorize C8",
            "authorize live runtime adoption",
        ],
    }

    basis = {
        "schema_version": "runtime_t6_loop_and_tie_feasibility_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_t4_observability_receipt_id": SOURCE_T4_OBS_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "T3/T4 deferred cases are ready; T6 requires a feasibility audit before any loop/tie case contract.",
        "does_not_authorize": [
            "T6 case contract",
            "suite execution inside this unit",
            "loop trigger invention",
            "move tie invention",
            "move addition",
            "fixture expansion by default",
            "runtime patching",
            "live runtime adoption",
            "C8 authorization",
        ],
    }

    rollup = {
        "schema_version": "runtime_t6_loop_and_tie_feasibility_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "t6_feasibility_audit_done": gate == "PASS",
        "loop_trigger_available": loop_trigger_available,
        "tie_trigger_available": tie_trigger_available,
        "t6_case_contract_authorized": False,
        "t6_cases_deferred_current_registry": gate == "PASS",
        "ready_for_deferred_suite_build": gate == "PASS",
        "ready_for_deferred_suite_run": False,
        "ready_case_count_for_suite_build": 3 if gate == "PASS" else 0,
        "excluded_t6_case_count": 2 if gate == "PASS" else 0,
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
        "schema_version": "runtime_t6_loop_and_tie_feasibility_profile_v0",
        "profile_status": status,
        "core_rule": "T6 cannot be case-contracted unless a lawful current-registry loop/tie trigger surface exists.",
        "registry_profile_ref": rel(REGISTRY_PROFILE_PATH),
        "loop_audit_ref": rel(LOOP_AUDIT_PATH),
        "tie_audit_ref": rel(TIE_AUDIT_PATH),
        "classification_ref": rel(CLASSIFICATION_PATH),
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_OR_DECIDE_RUNTIME_T6_FEASIBILITY_AUDIT_V0",
        "must_not_infer": [
            "T6 is ready",
            "loop trigger should be invented",
            "move tie should be invented",
            "runtime should be patched",
            "move should be added",
            "deferred suite should include T6",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    trace = {
        "schema_version": "runtime_t6_loop_and_tie_feasibility_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "T4_REQUIRED_OBSERVABILITY_GAP_INSTANCE_READY_T6_FEASIBILITY_NEXT",
                "edge": "consume T6 feasibility target and current registry reachability",
                "to": "T6_CURRENT_REGISTRY_TRIGGER_PROFILED" if gate == "PASS" else "T6_FEASIBILITY_GATE_FAIL",
            },
            {
                "from": "T6_CURRENT_REGISTRY_TRIGGER_PROFILED" if gate == "PASS" else "T6_FEASIBILITY_GATE_FAIL",
                "edge": "classify loop/tie trigger feasibility",
                "to": "DEFERRED_PRESSURE_SUITE_BUILD_T3_T4_ONLY_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_RUNTIME_T6_LOOP_AND_TIE_FEASIBILITY_AUDIT_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (REGISTRY_PROFILE_PATH, registry_profile),
        (LOOP_AUDIT_PATH, loop_audit),
        (TIE_AUDIT_PATH, tie_audit),
        (CLASSIFICATION_PATH, classification),
        (DEFERRED_SHAPE_PATH, deferred_shape),
        (SUITE_BUILD_TARGET_PATH, suite_build_target),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_OUT_PATH, trace),
    ]:
        write_json(path, obj)

    source_hashes_after = {rel(p): file_sha256(p) for p in required}
    source_mutated = source_hashes_before != source_hashes_after
    if source_mutated:
        gate = "FAIL"
        status = "TYPED_RUNTIME_T6_LOOP_AND_TIE_FEASIBILITY_SOURCE_MUTATION_FAIL"
        failures.append("source_inputs_mutated")

    reason_codes = [
        "T4_OBSERVABILITY_GAP_RECEIPT_CONSUMED",
        "T6_FEASIBILITY_TARGET_CONSUMED",
        "CURRENT_REGISTRY_PROFILED",
        "NO_LOOP_TRIGGER_SURFACE_FOUND",
        "NO_MOVE_TIE_TRIGGER_SURFACE_FOUND",
        "T6_CASES_DEFERRED_CURRENT_REGISTRY_NO_TRIGGER",
        "DEFERRED_SUITE_BUILD_T3_T4_ONLY_NEXT",
        "NO_T6_CASE_CONTRACT",
        "NO_LOOP_TRIGGER_INVENTION",
        "NO_MOVE_TIE_INVENTION",
        "NO_SUITE_RUN",
        "NO_RUNTIME_PATCH",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_LIVE_RUNTIME_ADOPTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_t6_loop_and_tie_feasibility_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_T6_LOOP_AND_TIE_FEASIBILITY_AUDIT_RECEIPT",
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
        "source_t4_observability_receipt_id": SOURCE_T4_OBS_RECEIPT_ID,
        "acceptance_gate_results": {
            "T6_FEAS_0_T4_OBSERVABILITY_RECEIPT_CONSUMED": gate == "PASS",
            "T6_FEAS_1_TARGET_CONSUMED": gate == "PASS",
            "T6_FEAS_2_REGISTRY_PROFILED": gate == "PASS",
            "T6_FEAS_3_NO_LOOP_TRIGGER_FOUND": gate == "PASS",
            "T6_FEAS_4_NO_MOVE_TIE_FOUND": gate == "PASS",
            "T6_FEAS_5_T6_EXCLUDED_FROM_THIS_SUITE": gate == "PASS",
            "T6_FEAS_6_DEFERRED_SUITE_BUILD_TARGET_EMITTED": gate == "PASS",
            "T6_FEAS_7_NO_SUITE_RUN": gate == "PASS",
            "T6_FEAS_8_SOURCE_INPUTS_NOT_MUTATED": not source_mutated,
            "T6_FEAS_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_t6_feasibility_summary": {
            "status": status,
            "t6_feasibility_audit_done": gate == "PASS",
            "loop_trigger_available": loop_trigger_available,
            "tie_trigger_available": tie_trigger_available,
            "t6_case_contract_authorized": False,
            "t6_cases_deferred_current_registry": gate == "PASS",
            "ready_cases_for_deferred_suite_build": [
                "T3.schema_validation_failure",
                "T3.admissibility_block",
                "T4.full_observability_required_gap",
            ] if gate == "PASS" else [],
            "excluded_cases_from_this_suite_build": [
                "T6.step_cap_loop_shape",
                "T6.move_tie_unresolved",
            ] if gate == "PASS" else [],
            "ready_for_deferred_suite_build": gate == "PASS",
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
            "registry_profile": rel(REGISTRY_PROFILE_PATH),
            "loop_audit": rel(LOOP_AUDIT_PATH),
            "tie_audit": rel(TIE_AUDIT_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "deferred_shape": rel(DEFERRED_SHAPE_PATH),
            "suite_build_target": rel(SUITE_BUILD_TARGET_PATH),
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
    print(f"runtime_t6_feasibility_receipt_id={receipt_id}")
    print(f"runtime_t6_feasibility_receipt_path={rel(receipt_path)}")
    print(f"runtime_t6_feasibility_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
