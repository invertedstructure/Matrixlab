#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "AUDIT_RUNTIME_T6_MOVE_TIE_TRIGGER_SURFACE_FOUND_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.deferred_cases.t6_move_tie_surface_found_audit_v0"

FAILED_T6_FEASIBILITY_RECEIPT_ID = "3d72600a"
SOURCE_T4_OBS_RECEIPT_ID = "6ea9018e"

FAILED_T6_FEASIBILITY_RECEIPT_PATH = ROOT / "data/runtime_deferred_cases_t6_feasibility_v0_receipts/3d72600a.json"

T6_REGISTRY_PROFILE_PATH = ROOT / "data/runtime_deferred_cases_t6_feasibility_v0/runtime_t6_current_registry_trigger_profile_v0.json"
T6_TIE_AUDIT_PATH = ROOT / "data/runtime_deferred_cases_t6_feasibility_v0/runtime_t6_move_tie_trigger_audit_v0.json"
T6_LOOP_AUDIT_PATH = ROOT / "data/runtime_deferred_cases_t6_feasibility_v0/runtime_t6_step_cap_loop_trigger_audit_v0.json"
T6_CLASSIFICATION_PATH = ROOT / "data/runtime_deferred_cases_t6_feasibility_v0/runtime_t6_loop_and_tie_feasibility_classification_v0.json"
T6_TARGET_PATH = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0/runtime_t6_loop_and_tie_trigger_feasibility_target_v0.json"

T4_OBS_RECEIPT_PATH = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0_receipts/6ea9018e.json"
T4_CASE_INSTANCE_PATH = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0/runtime_t4_required_observability_gap_case_instance_v0.json"
T4_ALLOWED_CASE_PATH = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0/runtime_allowed_t4_required_observability_gap_case_instance_v0.json"
T4_DEFERRED_SHAPE_PATH = ROOT / "data/runtime_deferred_cases_t4_observability_gap_instance_v0/runtime_deferred_suite_shape_after_t4_observability_gap_instance_v0.json"

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

OUT_DIR = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0"
RECEIPT_DIR = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_t6_move_tie_surface_audit_basis_v0.json"
DETECTOR_PROFILE_PATH = OUT_DIR / "runtime_t6_move_tie_detector_profile_v0.json"
STRUCTURED_CANDIDATES_PATH = OUT_DIR / "runtime_t6_move_tie_structured_candidate_audit_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "runtime_t6_move_tie_surface_classification_v0.json"
LOOP_CARRY_FORWARD_PATH = OUT_DIR / "runtime_t6_loop_surface_carry_forward_v0.json"
DEFERRED_SHAPE_PATH = OUT_DIR / "runtime_deferred_suite_shape_after_t6_move_tie_surface_audit_v0.json"
SUITE_BUILD_TARGET_PATH = OUT_DIR / "runtime_deferred_pressure_suite_build_target_after_t6_move_tie_audit_v0.json"
T6_TIE_CONTRACT_TARGET_PATH = OUT_DIR / "runtime_t6_move_tie_unresolved_case_contract_target_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_t6_move_tie_surface_audit_profile_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_t6_move_tie_surface_audit_rollup_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_t6_move_tie_surface_audit_transition_trace.json"

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

def registry_moves(registry: Dict[str, Any]) -> List[Dict[str, Any]]:
    for key in ["moves", "registry_moves", "move_registry"]:
        if isinstance(registry.get(key), list):
            return registry[key]
    return []

def move_name(move: Dict[str, Any], idx: int) -> str:
    for key in ["move_id", "id", "name", "unit_id", "command_id"]:
        if move.get(key):
            return str(move[key])
    return f"move_index_{idx}"

def norm(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))

def group_key(move: Dict[str, Any], idx: int) -> Tuple[str, str]:
    applies = move.get("applies_when", move.get("when", move.get("predicate", {})))
    priority = move.get("priority", move.get("rank", move.get("order", "__NO_EXPLICIT_PRIORITY__")))
    return (norm(applies), norm(priority))

def has_explicit_ordering(move: Dict[str, Any]) -> bool:
    return any(k in move for k in ["order", "rank", "priority", "sequence", "deterministic_order"])

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
        FAILED_T6_FEASIBILITY_RECEIPT_PATH,
        T6_REGISTRY_PROFILE_PATH,
        T6_TIE_AUDIT_PATH,
        T6_LOOP_AUDIT_PATH,
        T6_CLASSIFICATION_PATH,
        T6_TARGET_PATH,
        T4_OBS_RECEIPT_PATH,
        T4_CASE_INSTANCE_PATH,
        T4_ALLOWED_CASE_PATH,
        T4_DEFERRED_SHAPE_PATH,
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

    failed_receipt = read_json(FAILED_T6_FEASIBILITY_RECEIPT_PATH)
    failed_summary = failed_receipt.get("machine_readable_t6_feasibility_summary", {})
    registry_profile = read_json(T6_REGISTRY_PROFILE_PATH)
    tie_audit = read_json(T6_TIE_AUDIT_PATH)
    loop_audit = read_json(T6_LOOP_AUDIT_PATH)
    failed_classification = read_json(T6_CLASSIFICATION_PATH)
    t6_target = read_json(T6_TARGET_PATH)

    t4_receipt = read_json(T4_OBS_RECEIPT_PATH)
    t4_summary = t4_receipt.get("machine_readable_t4_observability_gap_instance_summary", {})
    t4_shape = read_json(T4_DEFERRED_SHAPE_PATH)

    reachability_map = read_json(REACHABILITY_MAP_PATH)
    branch_gap_index = read_json(BRANCH_GAP_INDEX_PATH)
    tier_feasibility = read_json(TIER_FEASIBILITY_PATH)
    smoke_registry = read_json(SMOKE_REGISTRY_PATH)

    if failed_receipt.get("receipt_id") != FAILED_T6_FEASIBILITY_RECEIPT_ID:
        failures.append(f"failed_t6_receipt_id_wrong:{failed_receipt.get('receipt_id')}")
    if failed_receipt.get("gate") != "FAIL":
        failures.append("failed_t6_gate_not_fail")
    if "t6_trigger_surface_found_requires_human_contract_decision" not in failed_receipt.get("failures", []):
        failures.append("failed_t6_reason_not_trigger_surface_found")
    if failed_summary.get("tie_trigger_available") is not True:
        failures.append("failed_t6_tie_trigger_not_true")
    if failed_summary.get("loop_trigger_available") is not False:
        failures.append("failed_t6_loop_trigger_not_false")
    if failed_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append("failed_t6_terminal_not_stop")
    if failed_receipt.get("terminal", {}).get("next_unit_id") is not None:
        failures.append("failed_t6_next_should_be_none")

    if t4_receipt.get("receipt_id") != "6ea9018e":
        failures.append(f"t4_receipt_id_wrong:{t4_receipt.get('receipt_id')}")
    if t4_receipt.get("gate") != "PASS":
        failures.append("t4_gate_not_pass")
    if t4_summary.get("ready_for_t6_feasibility_audit") is not True:
        failures.append("t4_not_ready_for_t6_feasibility_audit")

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
        if key in failed_summary:
            require_false(failed_summary, key, failures)
        if key in t4_summary:
            require_false(t4_summary, key, failures)

    moves = registry_moves(smoke_registry)

    structured_candidates_from_reachability = []
    if isinstance(reachability_map.get("move_tie_candidates"), list):
        structured_candidates_from_reachability = reachability_map["move_tie_candidates"]

    move_tie_candidate_count = registry_profile.get("move_tie_candidate_count")
    if move_tie_candidate_count is None:
        move_tie_candidate_count = reachability_map.get("move_tie_candidate_count")
    move_tie_candidate_count = int_or_zero(move_tie_candidate_count)

    explicit_tie_surface_visible = bool(registry_profile.get("explicit_tie_surface_visible"))
    tie_trigger_available = bool(registry_profile.get("tie_trigger_available")) or bool(tie_audit.get("trigger_available"))

    computed_groups: Dict[Tuple[str, str], List[Dict[str, Any]]] = {}
    for idx, move in enumerate(moves):
        key = group_key(move, idx)
        computed_groups.setdefault(key, []).append({
            "move_name": move_name(move, idx),
            "move_index": idx,
            "has_explicit_ordering": has_explicit_ordering(move),
            "applies_when": move.get("applies_when", move.get("when", move.get("predicate", {}))),
            "priority_or_rank_or_order": move.get("priority", move.get("rank", move.get("order", None))),
        })

    computed_tie_groups = []
    for key, group in computed_groups.items():
        if len(group) > 1:
            computed_tie_groups.append({
                "group_key": {
                    "applies_when_sig8": hashlib.sha256(key[0].encode("utf-8")).hexdigest()[:8],
                    "priority_sig8": hashlib.sha256(key[1].encode("utf-8")).hexdigest()[:8],
                },
                "moves": group,
                "move_count": len(group),
            })

    text_only_tie_hit = (
        explicit_tie_surface_visible
        and move_tie_candidate_count == 0
        and not structured_candidates_from_reachability
        and not computed_tie_groups
    )

    structured_tie_hit = (
        move_tie_candidate_count > 0
        or bool(structured_candidates_from_reachability)
        or bool(computed_tie_groups)
    )

    # Three-way classification.
    if structured_tie_hit and (structured_candidates_from_reachability or computed_tie_groups):
        classification_kind = "REAL_CURRENT_REGISTRY_MOVE_TIE_TRIGGER_SURFACE"
        next_unit_id = "PREPARE_RUNTIME_T6_MOVE_TIE_UNRESOLVED_CASE_CONTRACT_V0"
        terminal_type = "ADVANCE"
        stop_code = None
        ready_for_t6_move_tie_contract = True
        ready_for_deferred_suite_build = False
        include_t6_move_tie_in_later_suite = True
    elif text_only_tie_hit:
        classification_kind = "DETECTOR_FALSE_POSITIVE_TEXT_ONLY_TIE_SURFACE"
        next_unit_id = "BUILD_OUTER_RUNTIME_DEFERRED_PRESSURE_TEST_SUITE_V0"
        terminal_type = "ADVANCE"
        stop_code = None
        ready_for_t6_move_tie_contract = False
        ready_for_deferred_suite_build = True
        include_t6_move_tie_in_later_suite = False
    else:
        classification_kind = "UNDERDECLARED_REACHABILITY_PROFILE_ARTIFACT"
        next_unit_id = None
        terminal_type = "STOP"
        stop_code = "STOP_RUNTIME_T6_MOVE_TIE_SURFACE_UNDERDECLARED_PROFILE_ARTIFACT"
        ready_for_t6_move_tie_contract = False
        ready_for_deferred_suite_build = False
        include_t6_move_tie_in_later_suite = False

    gate = "PASS" if not failures else "FAIL"
    if gate != "PASS":
        classification_kind = "T6_MOVE_TIE_SURFACE_AUDIT_GATE_FAIL"
        next_unit_id = None
        terminal_type = "STOP"
        stop_code = "STOP_RUNTIME_T6_MOVE_TIE_SURFACE_AUDIT_GATE_FAIL"
        ready_for_t6_move_tie_contract = False
        ready_for_deferred_suite_build = False
        include_t6_move_tie_in_later_suite = False

    if classification_kind == "REAL_CURRENT_REGISTRY_MOVE_TIE_TRIGGER_SURFACE":
        status = "TYPED_RUNTIME_T6_MOVE_TIE_SURFACE_AUDIT_REAL_TRIGGER_CONTRACT_NEXT"
    elif classification_kind == "DETECTOR_FALSE_POSITIVE_TEXT_ONLY_TIE_SURFACE":
        status = "TYPED_RUNTIME_T6_MOVE_TIE_SURFACE_AUDIT_FALSE_POSITIVE_DEFERRED_SUITE_BUILD_NEXT"
    elif classification_kind == "UNDERDECLARED_REACHABILITY_PROFILE_ARTIFACT":
        status = "TYPED_RUNTIME_T6_MOVE_TIE_SURFACE_AUDIT_UNDERDECLARED_PROFILE_ARTIFACT_STOP"
    else:
        status = "TYPED_RUNTIME_T6_MOVE_TIE_SURFACE_AUDIT_GATE_FAIL"

    detector_profile = {
        "schema_version": "runtime_t6_move_tie_detector_profile_v0",
        "profile_status": "EMITTED" if gate == "PASS" else "PARTIAL",
        "source_failed_t6_receipt_ref": rel(FAILED_T6_FEASIBILITY_RECEIPT_PATH),
        "source_registry_profile_ref": rel(T6_REGISTRY_PROFILE_PATH),
        "tie_trigger_available_from_failed_audit": failed_summary.get("tie_trigger_available"),
        "loop_trigger_available_from_failed_audit": failed_summary.get("loop_trigger_available"),
        "tie_trigger_available_from_registry_profile": registry_profile.get("tie_trigger_available"),
        "explicit_tie_surface_visible": explicit_tie_surface_visible,
        "move_tie_candidate_count": move_tie_candidate_count,
        "structured_reachability_candidate_count": len(structured_candidates_from_reachability),
        "computed_tie_group_count": len(computed_tie_groups),
        "text_only_tie_hit": text_only_tie_hit,
        "structured_tie_hit": structured_tie_hit,
        "classification_kind": classification_kind,
    }

    structured_candidates = {
        "schema_version": "runtime_t6_move_tie_structured_candidate_audit_v0",
        "audit_status": "EMITTED" if gate == "PASS" else "PARTIAL",
        "registry_move_count": len(moves),
        "move_tie_candidate_count_reported": move_tie_candidate_count,
        "reachability_move_tie_candidates": structured_candidates_from_reachability,
        "computed_tie_groups": computed_tie_groups,
        "computed_tie_group_count": len(computed_tie_groups),
        "real_unresolved_tie_surface_found": classification_kind == "REAL_CURRENT_REGISTRY_MOVE_TIE_TRIGGER_SURFACE",
        "candidate_reading": (
            "Structured same-condition tie candidate found."
            if classification_kind == "REAL_CURRENT_REGISTRY_MOVE_TIE_TRIGGER_SURFACE"
            else "No structured same-condition tie candidate found."
        ),
    }

    loop_carry_forward = {
        "schema_version": "runtime_t6_loop_surface_carry_forward_v0",
        "case_key": "T6.step_cap_loop_shape",
        "loop_trigger_available": False,
        "classification": "DEFERRED_CURRENT_REGISTRY_NO_LOOP_TRIGGER",
        "included_in_deferred_suite_build": False,
        "preserved_for_later": True,
        "case_contract_authorized": False,
        "move_addition_authorized": False,
        "runtime_patch_authorized": False,
    }

    if classification_kind == "REAL_CURRENT_REGISTRY_MOVE_TIE_TRIGGER_SURFACE":
        ready_cases_for_suite_build = [
            "T3.schema_validation_failure",
            "T3.admissibility_block",
            "T4.full_observability_required_gap",
            "T6.move_tie_unresolved",
        ]
        excluded_cases = ["T6.step_cap_loop_shape"]
    else:
        ready_cases_for_suite_build = [
            "T3.schema_validation_failure",
            "T3.admissibility_block",
            "T4.full_observability_required_gap",
        ] if ready_for_deferred_suite_build else []
        excluded_cases = [
            "T6.step_cap_loop_shape",
            "T6.move_tie_unresolved",
        ] if ready_for_deferred_suite_build else []

    classification = {
        "schema_version": "runtime_t6_move_tie_surface_classification_v0",
        "classification_status": status,
        "classification_kind": classification_kind,
        "case_key": "T6.move_tie_unresolved",
        "is_real_current_registry_move_tie_trigger_surface": classification_kind == "REAL_CURRENT_REGISTRY_MOVE_TIE_TRIGGER_SURFACE",
        "is_detector_false_positive": classification_kind == "DETECTOR_FALSE_POSITIVE_TEXT_ONLY_TIE_SURFACE",
        "is_underdeclared_reachability_profile_artifact": classification_kind == "UNDERDECLARED_REACHABILITY_PROFILE_ARTIFACT",
        "ready_for_t6_move_tie_contract": ready_for_t6_move_tie_contract,
        "ready_for_deferred_suite_build": ready_for_deferred_suite_build,
        "include_t6_move_tie_in_later_suite": include_t6_move_tie_in_later_suite,
        "loop_case_handling": "defer; no current loop trigger",
        "ready_cases_for_deferred_suite_build": ready_cases_for_suite_build,
        "excluded_cases_from_this_suite_build": excluded_cases,
        "decision_law": "A tie surface requires structured evidence of competing applicable moves. Text-only tie metadata is not enough to contract T6.",
        "repair_authorized": False,
        "move_addition_authorized": False,
        "runtime_patch_authorized": False,
        "c8_authorized": False,
    }

    deferred_shape = {
        "schema_version": "runtime_deferred_suite_shape_after_t6_move_tie_surface_audit_v0",
        "shape_status": (
            "READY_FOR_T6_MOVE_TIE_CONTRACT"
            if ready_for_t6_move_tie_contract
            else "READY_FOR_DEFERRED_PRESSURE_SUITE_BUILD_T3_T4_ONLY"
            if ready_for_deferred_suite_build
            else "NOT_READY_UNDERDECLARED_TIE_PROFILE"
        ),
        "ready_deferred_cases_after_this_unit": ready_cases_for_suite_build,
        "contracted_cases": [
            "T3.schema_validation_failure",
            "T3.admissibility_block",
        ],
        "case_instanced_cases": [
            "T4.full_observability_required_gap",
        ],
        "t6_move_tie_contract_ready": ready_for_t6_move_tie_contract,
        "excluded_current_registry_no_trigger_or_false_positive": excluded_cases,
        "still_needs_contract": ["T6.move_tie_unresolved"] if ready_for_t6_move_tie_contract else [],
        "still_needs_case_instance": [],
        "still_needs_feasibility_audit": [] if gate == "PASS" else ["T6.move_tie_unresolved"],
        "ready_for_deferred_suite_build": ready_for_deferred_suite_build,
        "ready_for_deferred_suite_run": False,
    }

    suite_build_target = {
        "schema_version": "runtime_deferred_pressure_suite_build_target_after_t6_move_tie_audit_v0",
        "target_status": "DEFERRED_PRESSURE_SUITE_BUILD_NEXT" if ready_for_deferred_suite_build else "NOT_READY",
        "next_unit_id": "BUILD_OUTER_RUNTIME_DEFERRED_PRESSURE_TEST_SUITE_V0" if ready_for_deferred_suite_build else None,
        "suite_scope": "T3_T4_READY_CASES_ONLY" if ready_for_deferred_suite_build else None,
        "include_cases": ready_cases_for_suite_build,
        "exclude_cases": excluded_cases,
        "exclude_reason": "Move-tie surface was text-only detector false positive; loop has no current trigger." if ready_for_deferred_suite_build else None,
        "forbidden": [
            "include T6 without contract",
            "invent loop trigger",
            "invent move tie",
            "add moves",
            "patch runtime",
            "expand fixtures by default",
            "authorize C8",
            "authorize live runtime adoption",
        ],
    }

    t6_tie_contract_target = {
        "schema_version": "runtime_t6_move_tie_unresolved_case_contract_target_v0",
        "target_status": "T6_MOVE_TIE_UNRESOLVED_CASE_CONTRACT_NEXT" if ready_for_t6_move_tie_contract else "NOT_READY",
        "next_unit_id": "PREPARE_RUNTIME_T6_MOVE_TIE_UNRESOLVED_CASE_CONTRACT_V0" if ready_for_t6_move_tie_contract else None,
        "source_move_tie_surface_classification_ref": rel(CLASSIFICATION_PATH),
        "case_key": "T6.move_tie_unresolved",
        "target_role": "Prepare bounded T6 move-tie unresolved case contract using structured current-registry tie evidence.",
        "structured_candidate_ref": rel(STRUCTURED_CANDIDATES_PATH),
        "forbidden": [
            "invent tie",
            "invent trigger",
            "add moves",
            "patch runtime",
            "run suite now",
            "authorize C8",
            "authorize live runtime adoption",
        ],
    }

    basis = {
        "schema_version": "runtime_t6_move_tie_surface_audit_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "failed_t6_feasibility_receipt_id": FAILED_T6_FEASIBILITY_RECEIPT_ID,
        "source_t4_observability_receipt_id": SOURCE_T4_OBS_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "Previous T6 feasibility audit stopped because a move-tie trigger surface was detected; this unit classifies that detected surface before any T6 contract.",
        "does_not_authorize": [
            "T6 case contract unless structured tie is proven",
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

    profile = {
        "schema_version": "runtime_t6_move_tie_surface_audit_profile_v0",
        "profile_status": status,
        "core_rule": "Tie detection must distinguish structured competing moves from text-only tie metadata.",
        "detector_profile_ref": rel(DETECTOR_PROFILE_PATH),
        "structured_candidates_ref": rel(STRUCTURED_CANDIDATES_PATH),
        "classification_ref": rel(CLASSIFICATION_PATH),
        "recommended_next": next_unit_id,
        "must_not_infer": [
            "tie text means unresolved move tie",
            "T6 is contractable without structured candidate evidence",
            "move should be added",
            "runtime should be patched",
            "deferred suite is runnable inside this unit",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    rollup = {
        "schema_version": "runtime_t6_move_tie_surface_audit_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "classification_kind": classification_kind,
        "text_only_tie_hit": text_only_tie_hit,
        "structured_tie_hit": structured_tie_hit,
        "move_tie_candidate_count": move_tie_candidate_count,
        "computed_tie_group_count": len(computed_tie_groups),
        "ready_for_t6_move_tie_contract": ready_for_t6_move_tie_contract,
        "ready_for_deferred_suite_build": ready_for_deferred_suite_build,
        "ready_for_deferred_suite_run": False,
        "next_unit_id": next_unit_id,
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

    trace = {
        "schema_version": "runtime_t6_move_tie_surface_audit_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "T6_FEASIBILITY_AUDIT_STOPPED_ON_TIE_SURFACE_FOUND",
                "edge": "consume failed T6 feasibility receipt and registry profile",
                "to": "T6_MOVE_TIE_SURFACE_INDEXED" if gate == "PASS" else "T6_MOVE_TIE_SURFACE_AUDIT_GATE_FAIL",
            },
            {
                "from": "T6_MOVE_TIE_SURFACE_INDEXED" if gate == "PASS" else "T6_MOVE_TIE_SURFACE_AUDIT_GATE_FAIL",
                "edge": "classify detected tie surface",
                "to": (
                    "T6_MOVE_TIE_CONTRACT_NEXT"
                    if ready_for_t6_move_tie_contract
                    else "DEFERRED_PRESSURE_SUITE_BUILD_T3_T4_ONLY_NEXT"
                    if ready_for_deferred_suite_build
                    else "STOP_UNDERDECLARED_PROFILE_ARTIFACT"
                ),
            },
        ],
        "terminal": {
            "type": terminal_type,
            "next_unit_id": next_unit_id,
            "stop_code": stop_code,
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (DETECTOR_PROFILE_PATH, detector_profile),
        (STRUCTURED_CANDIDATES_PATH, structured_candidates),
        (CLASSIFICATION_PATH, classification),
        (LOOP_CARRY_FORWARD_PATH, loop_carry_forward),
        (DEFERRED_SHAPE_PATH, deferred_shape),
        (SUITE_BUILD_TARGET_PATH, suite_build_target),
        (T6_TIE_CONTRACT_TARGET_PATH, t6_tie_contract_target),
        (PROFILE_PATH, profile),
        (ROLLUP_PATH, rollup),
        (TRACE_OUT_PATH, trace),
    ]:
        write_json(path, obj)

    source_hashes_after = {rel(p): file_sha256(p) for p in required}
    source_mutated = source_hashes_before != source_hashes_after
    if source_mutated:
        gate = "FAIL"
        status = "TYPED_RUNTIME_T6_MOVE_TIE_SURFACE_AUDIT_SOURCE_MUTATION_FAIL"
        failures.append("source_inputs_mutated")

    reason_codes = [
        "FAILED_T6_FEASIBILITY_RECEIPT_CONSUMED",
        "TIE_SURFACE_DETECTED_BY_PRIOR_AUDIT",
        "STRUCTURED_TIE_CANDIDATES_AUDITED",
        "MOVE_TIE_SURFACE_CLASSIFIED",
        "LOOP_SURFACE_CARRIED_FORWARD_AS_NO_TRIGGER",
        "NO_SUITE_RUN",
        "NO_RUNTIME_PATCH",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_LIVE_RUNTIME_ADOPTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_t6_move_tie_surface_audit_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_T6_MOVE_TIE_SURFACE_AUDIT_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": "OUTER / RUNTIME_ADOPTION / DEFERRED_CASES / T6",
        "mode": "AUDIT_ONLY / MOVE_TIE_SURFACE_FOUND / NO_CASE_CONTRACT / NO_TEST_RUN",
        "build_mode": "T6_MOVE_TIE_SURFACE_CLASSIFICATION_ONLY",
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "failed_t6_feasibility_receipt_id": FAILED_T6_FEASIBILITY_RECEIPT_ID,
        "source_t4_observability_receipt_id": SOURCE_T4_OBS_RECEIPT_ID,
        "acceptance_gate_results": {
            "T6_TIE_0_FAILED_T6_RECEIPT_CONSUMED": gate == "PASS",
            "T6_TIE_1_PRIOR_TIE_SURFACE_CONFIRMED": tie_trigger_available,
            "T6_TIE_2_STRUCTURED_CANDIDATES_AUDITED": gate == "PASS",
            "T6_TIE_3_SURFACE_CLASSIFIED": gate == "PASS",
            "T6_TIE_4_LOOP_CARRIED_FORWARD_NO_TRIGGER": gate == "PASS",
            "T6_TIE_5_NO_SUITE_RUN": gate == "PASS",
            "T6_TIE_6_NO_RUNTIME_PATCH": gate == "PASS",
            "T6_TIE_7_NO_MOVE_ADDITION": gate == "PASS",
            "T6_TIE_8_SOURCE_INPUTS_NOT_MUTATED": not source_mutated,
            "T6_TIE_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_t6_move_tie_surface_audit_summary": {
            "status": status,
            "t6_move_tie_surface_audit_done": gate == "PASS",
            "classification_kind": classification_kind,
            "is_real_current_registry_move_tie_trigger_surface": classification_kind == "REAL_CURRENT_REGISTRY_MOVE_TIE_TRIGGER_SURFACE",
            "is_detector_false_positive": classification_kind == "DETECTOR_FALSE_POSITIVE_TEXT_ONLY_TIE_SURFACE",
            "is_underdeclared_reachability_profile_artifact": classification_kind == "UNDERDECLARED_REACHABILITY_PROFILE_ARTIFACT",
            "text_only_tie_hit": text_only_tie_hit,
            "structured_tie_hit": structured_tie_hit,
            "move_tie_candidate_count": move_tie_candidate_count,
            "computed_tie_group_count": len(computed_tie_groups),
            "loop_trigger_available": False,
            "ready_for_t6_move_tie_contract": ready_for_t6_move_tie_contract,
            "ready_for_deferred_suite_build": ready_for_deferred_suite_build,
            "ready_for_deferred_suite_run": False,
            "ready_cases_for_deferred_suite_build": ready_cases_for_suite_build,
            "excluded_cases_from_this_suite_build": excluded_cases,
            "next_unit_id": next_unit_id,
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
            "detector_profile": rel(DETECTOR_PROFILE_PATH),
            "structured_candidates": rel(STRUCTURED_CANDIDATES_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "loop_carry_forward": rel(LOOP_CARRY_FORWARD_PATH),
            "deferred_shape": rel(DEFERRED_SHAPE_PATH),
            "suite_build_target": rel(SUITE_BUILD_TARGET_PATH),
            "t6_tie_contract_target": rel(T6_TIE_CONTRACT_TARGET_PATH),
            "profile": rel(PROFILE_PATH),
            "rollup": rel(ROLLUP_PATH),
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
    print(f"runtime_t6_move_tie_surface_audit_receipt_id={receipt_id}")
    print(f"runtime_t6_move_tie_surface_audit_receipt_path={rel(receipt_path)}")
    print(f"runtime_t6_move_tie_surface_audit_next_unit={next_unit_id if next_unit_id else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
