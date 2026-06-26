#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_RUNTIME_T6_CAPABILITY_BOUNDARY_OBJECTIVE_FROM_LOOP_SCHEMA_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.t6_capability_boundary_objective_v0"
NEXT_UNIT_ID = "AUDIT_RUNTIME_T6_CAPABILITY_BOUNDARY_SURFACE_V0"

SOURCE_CLOSED_DEFERRED_SUITE_DECISION_RECEIPT_ID = "04c2a4f0"

CLOSED_DECISION_RECEIPT_PATH = ROOT / "data/runtime_deferred_pressure_suite_decision_v0_receipts/04c2a4f0.json"
DEFERRED_SUITE_CLOSURE_PATH = ROOT / "data/runtime_deferred_pressure_suite_decision_v0/runtime_deferred_pressure_suite_closure_v0.json"
T6_PRESERVATION_PATH = ROOT / "data/runtime_deferred_pressure_suite_decision_v0/runtime_t6_later_objective_preservation_v0.json"

T6_MOVE_TIE_AUDIT_RECEIPT_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0_receipts/eb20d76b.json"
T6_MOVE_TIE_CLASSIFICATION_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0/runtime_t6_move_tie_surface_classification_v0.json"
T6_STRUCTURED_CANDIDATES_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0/runtime_t6_move_tie_structured_candidate_audit_v0.json"
T6_LOOP_CARRY_FORWARD_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0/runtime_t6_loop_surface_carry_forward_v0.json"

T6_FAILED_FEASIBILITY_RECEIPT_PATH = ROOT / "data/runtime_deferred_cases_t6_feasibility_v0_receipts/3d72600a.json"
T6_REGISTRY_PROFILE_PATH = ROOT / "data/runtime_deferred_cases_t6_feasibility_v0/runtime_t6_current_registry_trigger_profile_v0.json"

SMOKE_REGISTRY_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_move_registry_snapshot_v0.json"
REACHABILITY_MAP_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_registry_reachability_map_v0.json"

OUT_DIR = ROOT / "data/runtime_t6_capability_boundary_objective_v0"
RECEIPT_DIR = ROOT / "data/runtime_t6_capability_boundary_objective_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_t6_capability_boundary_objective_basis_v0.json"
LOOP_SCHEMA_PATH = OUT_DIR / "current_surface_pressure_handling_loop_schema_v0_collection_stage.json"
MISSING_OBJECT_CLASS_INDEX_PATH = OUT_DIR / "runtime_t6_missing_object_class_index_v0.json"
CAPABILITY_STOP_PACKET_SCHEMA_PATH = OUT_DIR / "runtime_t6_capability_stop_packet_schema_v0.json"
T6_OBJECTIVE_PATH = OUT_DIR / "runtime_t6_capability_boundary_objective_v0.json"
T6_AUDIT_TARGET_PATH = OUT_DIR / "runtime_t6_capability_boundary_surface_audit_target_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_t6_capability_boundary_objective_profile_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_t6_capability_boundary_objective_rollup_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_t6_capability_boundary_objective_transition_trace.json"

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
        CLOSED_DECISION_RECEIPT_PATH,
        DEFERRED_SUITE_CLOSURE_PATH,
        T6_PRESERVATION_PATH,
        T6_MOVE_TIE_AUDIT_RECEIPT_PATH,
        T6_MOVE_TIE_CLASSIFICATION_PATH,
        T6_STRUCTURED_CANDIDATES_PATH,
        T6_LOOP_CARRY_FORWARD_PATH,
        T6_FAILED_FEASIBILITY_RECEIPT_PATH,
        T6_REGISTRY_PROFILE_PATH,
        SMOKE_REGISTRY_PATH,
        REACHABILITY_MAP_PATH,
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

    decision_receipt = read_json(CLOSED_DECISION_RECEIPT_PATH)
    decision_summary = decision_receipt.get("machine_readable_deferred_pressure_suite_decision_summary", {})
    closure = read_json(DEFERRED_SUITE_CLOSURE_PATH)
    t6_preservation = read_json(T6_PRESERVATION_PATH)

    t6_tie_receipt = read_json(T6_MOVE_TIE_AUDIT_RECEIPT_PATH)
    t6_tie_summary = t6_tie_receipt.get("machine_readable_t6_move_tie_surface_audit_summary", {})
    t6_tie_classification = read_json(T6_MOVE_TIE_CLASSIFICATION_PATH)
    t6_structured_candidates = read_json(T6_STRUCTURED_CANDIDATES_PATH)
    t6_loop_carry = read_json(T6_LOOP_CARRY_FORWARD_PATH)

    t6_failed_feasibility_receipt = read_json(T6_FAILED_FEASIBILITY_RECEIPT_PATH)
    t6_failed_summary = t6_failed_feasibility_receipt.get("machine_readable_t6_feasibility_summary", {})
    t6_registry_profile = read_json(T6_REGISTRY_PROFILE_PATH)

    smoke_registry = read_json(SMOKE_REGISTRY_PATH)
    reachability_map = read_json(REACHABILITY_MAP_PATH)

    if decision_receipt.get("receipt_id") != SOURCE_CLOSED_DEFERRED_SUITE_DECISION_RECEIPT_ID:
        failures.append(f"decision_receipt_id_wrong:{decision_receipt.get('receipt_id')}")
    if decision_receipt.get("gate") != "PASS":
        failures.append("closed_decision_gate_not_pass")
    if decision_summary.get("branch_closed") is not True:
        failures.append("deferred_pressure_branch_not_closed")
    if decision_summary.get("t6_preserved_for_later") is not True:
        failures.append("t6_not_preserved_for_later")
    if decision_summary.get("next_unit_id") is not None:
        failures.append("closed_decision_should_have_no_next_unit")
    if decision_receipt.get("terminal", {}).get("stop_code") != "STOP_RUNTIME_DEFERRED_PRESSURE_SUITE_BRANCH_COMPLETE":
        failures.append("closed_decision_stop_code_wrong")

    if t6_preservation.get("preservation_status") != "PRESERVED_FOR_LATER_OBJECTIVE":
        failures.append("t6_preservation_status_wrong")
    if t6_preservation.get("t6_cases") != ["T6.step_cap_loop_shape", "T6.move_tie_unresolved"]:
        failures.append("t6_preserved_cases_wrong")

    if t6_tie_summary.get("classification_kind") != "DETECTOR_FALSE_POSITIVE_TEXT_ONLY_TIE_SURFACE":
        failures.append("t6_tie_classification_not_false_positive")
    if t6_tie_summary.get("ready_for_t6_move_tie_contract") is not False:
        failures.append("t6_tie_contract_should_not_be_ready")
    if t6_tie_summary.get("loop_trigger_available") is not False:
        failures.append("loop_trigger_should_be_false")
    if t6_structured_candidates.get("computed_tie_group_count") != 0:
        failures.append("computed_tie_group_count_not_zero")
    if t6_structured_candidates.get("real_unresolved_tie_surface_found") is not False:
        failures.append("real_tie_surface_should_be_false")
    if t6_loop_carry.get("loop_trigger_available") is not False:
        failures.append("loop_carry_not_false")

    if t6_failed_summary.get("tie_trigger_available") is not True:
        failures.append("failed_feasibility_prior_tie_surface_not_visible")
    if t6_failed_summary.get("loop_trigger_available") is not False:
        failures.append("failed_feasibility_loop_should_be_false")
    if "t6_trigger_surface_found_requires_human_contract_decision" not in t6_failed_feasibility_receipt.get("failures", []):
        failures.append("failed_feasibility_reason_missing")

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
        require_false(decision_summary, key, failures)

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_RUNTIME_T6_CAPABILITY_BOUNDARY_OBJECTIVE_READY_SURFACE_AUDIT_NEXT"
        if gate == "PASS"
        else "TYPED_RUNTIME_T6_CAPABILITY_BOUNDARY_OBJECTIVE_GATE_FAIL"
    )

    loop_schema = {
        "schema_version": "current_surface_pressure_handling_loop_schema_v0_collection_stage",
        "schema_name": "CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_SCHEMA_V0",
        "schema_status": "COLLECTION_STAGE_OBJECT",
        "frozen_as_universal_base_schema": False,
        "loop_family": "current_surface_evidence_pressure_loop",
        "core_upgrade_from_introduction_001": "Explicit capability-boundary check before repair, introduction, audit, classification, or closure.",
        "compact_extraction": [
            "INSUFFICIENT_EVIDENCE",
            "IDENTIFY_MISSING_OBJECT",
            "CAN_CURRENT_CAPABILITY_HANDLE_OBJECT?",
            "NO -> STOP_CAPABILITY_LAYER_REQUIRED",
            "YES -> continue lawful branch",
        ],
        "operational_skeleton": {
            "select_pressure_group": True,
            "inspect_current_surface": True,
            "surface_has_enough_evidence": {
                "yes": "classify evidence and act within authority",
                "no": {
                    "identify_missing_surface_object": True,
                    "capability_check": {
                        "no": "STOP_CAPABILITY_LAYER_REQUIRED",
                        "yes": "continue by object type",
                    },
                },
            },
        },
        "missing_object_classes_collection_stage": [
            "evidence_missing",
            "field_missing",
            "value_absent",
            "provenance_missing",
            "reference_broken",
            "source_content_absent",
            "upstream_unresolved",
            "expected_limit_candidate",
            "capability_boundary_unknown",
            "trigger_surface_missing",
            "structured_tie_evidence_missing",
            "loop_trigger_surface_missing",
            "registry_profile_underdeclared",
            "runner_capability_missing",
            "authorization_missing",
        ],
        "distinctions_required_before_action": [
            "object_is_missing",
            "object_is_classified",
            "object_is_repairable",
            "object_is_authorized",
            "object_is_representable",
            "object_is_within_current_capability",
        ],
        "anti_overclaim_rule": {
            "must_not_transform": "current capability cannot handle this",
            "into": [
                "object cannot be handled",
                "object is invalid",
                "branch is closed",
                "source content is absent",
                "human must accept introduction",
            ],
            "capability_stop_meaning": "boundary exposure, not conclusion about the underlying object",
        },
        "one_line_contribution": "Every missing-object branch needs a capability-boundary check before repair, introduction, audit, or closure is allowed.",
    }

    missing_object_index = {
        "schema_version": "runtime_t6_missing_object_class_index_v0",
        "index_status": "COLLECTION_STAGE_T6_OBJECT_INDEX" if gate == "PASS" else "NOT_READY",
        "source_loop_schema_ref": rel(LOOP_SCHEMA_PATH),
        "t6_case_keys": [
            "T6.step_cap_loop_shape",
            "T6.move_tie_unresolved",
        ],
        "current_known_t6_surface_observations": {
            "prior_feasibility_stop": {
                "receipt_ref": rel(T6_FAILED_FEASIBILITY_RECEIPT_PATH),
                "reported_loop_trigger_available": t6_failed_summary.get("loop_trigger_available"),
                "reported_tie_trigger_available": t6_failed_summary.get("tie_trigger_available"),
                "reason": "prior audit stopped because it saw a tie surface but was not authorized to classify it",
            },
            "move_tie_surface_followup": {
                "receipt_ref": rel(T6_MOVE_TIE_AUDIT_RECEIPT_PATH),
                "classification_kind": t6_tie_summary.get("classification_kind"),
                "text_only_tie_hit": t6_tie_summary.get("text_only_tie_hit"),
                "structured_tie_hit": t6_tie_summary.get("structured_tie_hit"),
                "move_tie_candidate_count": t6_tie_summary.get("move_tie_candidate_count"),
                "computed_tie_group_count": t6_tie_summary.get("computed_tie_group_count"),
            },
            "loop_surface": {
                "loop_trigger_available": False,
                "classification": "DEFERRED_CURRENT_REGISTRY_NO_LOOP_TRIGGER",
            },
        },
        "candidate_missing_objects_to_inspect_next": [
            {
                "case_key": "T6.step_cap_loop_shape",
                "candidate_missing_object": "loop_trigger_surface_missing",
                "surface_where_stop_occurred": "runtime registry reachability profile",
                "known_evidence": "loop_trigger_available=false in failed feasibility and loop carry-forward",
                "initial_capability_question": "Can current capability construct or inspect a lawful loop/step-cap trigger without inventing registry moves?",
            },
            {
                "case_key": "T6.move_tie_unresolved",
                "candidate_missing_object": "structured_tie_evidence_missing",
                "surface_where_stop_occurred": "runtime registry reachability profile / move-tie detector",
                "known_evidence": "text-only tie hit, move_tie_candidate_count=0, computed_tie_group_count=0",
                "initial_capability_question": "Can current capability prove competing applicable moves from structured registry evidence rather than tie-related text?",
            },
            {
                "case_key": "T6.shared",
                "candidate_missing_object": "capability_boundary_unknown",
                "surface_where_stop_occurred": "T6 trigger/case-contract boundary",
                "known_evidence": "T6 was preserved as later objective, not continuation pressure from deferred suite",
                "initial_capability_question": "What exact capability is missing before T6 can emit a lawful proposition or typed stop?",
            },
        ],
    }

    capability_stop_packet_schema = {
        "schema_version": "runtime_t6_capability_stop_packet_schema_v0",
        "schema_status": "COLLECTION_STAGE_STOP_PACKET_SHAPE",
        "stop_code": "STOP_CAPABILITY_LAYER_REQUIRED",
        "minimum_fields": [
            "required_capability",
            "surface_where_stop_occurred",
            "missing_object",
            "evidence_already_collected",
            "why_current_capability_cannot_proceed",
            "safe_next_human_choices",
            "receipt_ref",
            "parent_return_payload",
        ],
        "packet_rules": [
            "Do not overclaim object invalidity.",
            "Do not close the underlying object merely because current capability is missing.",
            "Do not authorize repair, schema creation, move addition, runtime patch, fixture expansion, C8, or live runtime adoption.",
            "Return enough evidence for the parent/human to choose a bounded next objective.",
        ],
    }

    t6_objective = {
        "schema_version": "runtime_t6_capability_boundary_objective_v0",
        "objective_status": "READY_FOR_SURFACE_AUDIT" if gate == "PASS" else "NOT_READY",
        "objective_name": "T6_CAPABILITY_BOUNDARY_SURFACE_INSPECTION",
        "source_closed_deferred_suite_decision_receipt_ref": rel(CLOSED_DECISION_RECEIPT_PATH),
        "source_t6_preservation_ref": rel(T6_PRESERVATION_PATH),
        "source_loop_schema_ref": rel(LOOP_SCHEMA_PATH),
        "source_missing_object_index_ref": rel(MISSING_OBJECT_CLASS_INDEX_PATH),
        "objective_rule": "Do not fix T6. Inspect T6 pressure until the exact missing object and capability boundary are explicit.",
        "unit_end_condition": "Every unit must end in either a bounded proposition/next lawful object or STOP_CAPABILITY_LAYER_REQUIRED with a full packet.",
        "inspect_first": [
            "available T6 pressure surface",
            "missing object class",
            "current capability boundary",
            "representability",
            "authorization",
            "whether current capability can continue lawfully",
        ],
        "forbidden": [
            "make T6 pass",
            "invent loop trigger",
            "invent move tie",
            "patch runtime",
            "add moves",
            "expand fixtures by default",
            "create taxonomy as repair",
            "authorize C8",
            "authorize live runtime adoption",
        ],
    }

    t6_audit_target = {
        "schema_version": "runtime_t6_capability_boundary_surface_audit_target_v0",
        "target_status": "T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "source_objective_ref": rel(T6_OBJECTIVE_PATH),
        "source_loop_schema_ref": rel(LOOP_SCHEMA_PATH),
        "source_capability_stop_packet_schema_ref": rel(CAPABILITY_STOP_PACKET_SCHEMA_PATH),
        "target_role": "Inspect T6 pressure step by step and emit either a lawful proposition or STOP_CAPABILITY_LAYER_REQUIRED.",
        "expected_possible_terminal_shapes": [
            {
                "terminal_type": "ADVANCE",
                "meaning": "a bounded next T6 proposition is available within current capability",
            },
            {
                "terminal_type": "STOP",
                "stop_code": "STOP_CAPABILITY_LAYER_REQUIRED",
                "meaning": "current capability cannot proceed and emits the minimum stop packet",
            },
        ],
    }

    basis = {
        "schema_version": "runtime_t6_capability_boundary_objective_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_closed_deferred_suite_decision_receipt_id": SOURCE_CLOSED_DEFERRED_SUITE_DECISION_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "The deferred T3/T4 pressure branch is closed; T6 was preserved for later and should reopen only as a capability-boundary inspection objective.",
        "does_not_authorize": [
            "T6 repair",
            "T6 case contract",
            "runtime repair",
            "move addition",
            "schema archive mutation",
            "taxonomy creation",
            "fixture expansion by default",
            "runtime patching",
            "live runtime adoption",
            "C8 authorization",
        ],
    }

    rollup = {
        "schema_version": "runtime_t6_capability_boundary_objective_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "loop_schema_recorded": gate == "PASS",
        "loop_schema_status": "COLLECTION_STAGE_OBJECT" if gate == "PASS" else "NOT_READY",
        "capability_stop_packet_schema_recorded": gate == "PASS",
        "t6_objective_ready": gate == "PASS",
        "ready_for_t6_capability_boundary_surface_audit": gate == "PASS",
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
        "schema_version": "runtime_t6_capability_boundary_objective_profile_v0",
        "profile_status": status,
        "core_rule": "T6 is reopened as a capability-boundary inspection objective, not as a repair or pass/fail target.",
        "loop_schema_ref": rel(LOOP_SCHEMA_PATH),
        "missing_object_index_ref": rel(MISSING_OBJECT_CLASS_INDEX_PATH),
        "capability_stop_packet_schema_ref": rel(CAPABILITY_STOP_PACKET_SCHEMA_PATH),
        "objective_ref": rel(T6_OBJECTIVE_PATH),
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else None,
        "must_not_infer": [
            "T6 should be fixed",
            "T6 is solved",
            "T6 should pass now",
            "runtime should be patched",
            "moves should be added",
            "live runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    trace = {
        "schema_version": "runtime_t6_capability_boundary_objective_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "DEFERRED_PRESSURE_SUITE_BRANCH_COMPLETE_T6_PRESERVED_FOR_LATER",
                "edge": "human declares bounded T6 capability-boundary objective",
                "to": "CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_SCHEMA_RECORDED" if gate == "PASS" else "T6_CAPABILITY_BOUNDARY_OBJECTIVE_GATE_FAIL",
            },
            {
                "from": "CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_SCHEMA_RECORDED" if gate == "PASS" else "T6_CAPABILITY_BOUNDARY_OBJECTIVE_GATE_FAIL",
                "edge": "prepare T6 missing-object/capability-boundary audit target",
                "to": "T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_RUNTIME_T6_CAPABILITY_BOUNDARY_OBJECTIVE_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (LOOP_SCHEMA_PATH, loop_schema),
        (MISSING_OBJECT_CLASS_INDEX_PATH, missing_object_index),
        (CAPABILITY_STOP_PACKET_SCHEMA_PATH, capability_stop_packet_schema),
        (T6_OBJECTIVE_PATH, t6_objective),
        (T6_AUDIT_TARGET_PATH, t6_audit_target),
        (PROFILE_PATH, profile),
        (ROLLUP_PATH, rollup),
        (TRACE_OUT_PATH, trace),
    ]:
        write_json(path, obj)

    source_hashes_after = {rel(p): file_sha256(p) for p in required}
    source_mutated = source_hashes_before != source_hashes_after
    if source_mutated:
        gate = "FAIL"
        status = "TYPED_RUNTIME_T6_CAPABILITY_BOUNDARY_OBJECTIVE_SOURCE_MUTATION_FAIL"
        failures.append("source_inputs_mutated")

    reason_codes = [
        "CLOSED_DEFERRED_PRESSURE_SUITE_DECISION_RECEIPT_CONSUMED",
        "T6_PRESERVATION_CONSUMED",
        "CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_SCHEMA_RECORDED_COLLECTION_STAGE",
        "MISSING_OBJECT_CLASS_INDEX_RECORDED_COLLECTION_STAGE",
        "CAPABILITY_STOP_PACKET_SCHEMA_RECORDED",
        "T6_REOPENED_AS_BOUNDARY_INSPECTION_OBJECTIVE",
        "NO_T6_REPAIR",
        "NO_T6_CASE_CONTRACT",
        "NO_RUNTIME_PATCH",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_LIVE_RUNTIME_ADOPTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_t6_capability_boundary_objective_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_T6_CAPABILITY_BOUNDARY_OBJECTIVE_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": "OUTER / RUNTIME_ADOPTION / T6_CAPABILITY_BOUNDARY_OBJECTIVE",
        "mode": "PREPARE_OBJECTIVE_ONLY / LOOP_SCHEMA_COLLECTION_STAGE / NO_TEST_RUN",
        "build_mode": "T6_CAPABILITY_BOUNDARY_OBJECTIVE_PREP_ONLY",
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "source_closed_deferred_suite_decision_receipt_id": SOURCE_CLOSED_DEFERRED_SUITE_DECISION_RECEIPT_ID,
        "acceptance_gate_results": {
            "T6_BOUNDARY_0_CLOSED_DECISION_RECEIPT_CONSUMED": gate == "PASS",
            "T6_BOUNDARY_1_T6_PRESERVATION_CONSUMED": gate == "PASS",
            "T6_BOUNDARY_2_LOOP_SCHEMA_RECORDED": gate == "PASS",
            "T6_BOUNDARY_3_MISSING_OBJECT_INDEX_RECORDED": gate == "PASS",
            "T6_BOUNDARY_4_CAPABILITY_STOP_PACKET_SCHEMA_RECORDED": gate == "PASS",
            "T6_BOUNDARY_5_T6_OBJECTIVE_EMITTED": gate == "PASS",
            "T6_BOUNDARY_6_SURFACE_AUDIT_TARGET_NEXT": gate == "PASS",
            "T6_BOUNDARY_7_NO_TEST_RUN": gate == "PASS",
            "T6_BOUNDARY_8_SOURCE_INPUTS_NOT_MUTATED": not source_mutated,
            "T6_BOUNDARY_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_t6_capability_boundary_objective_summary": {
            "status": status,
            "loop_schema_name": "CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_SCHEMA_V0",
            "loop_schema_status": "COLLECTION_STAGE_OBJECT" if gate == "PASS" else "NOT_READY",
            "t6_capability_boundary_objective_ready": gate == "PASS",
            "capability_stop_packet_schema_ready": gate == "PASS",
            "ready_for_t6_capability_boundary_surface_audit": gate == "PASS",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "t6_repair_authorized": False,
            "t6_case_contract_authorized": False,
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
            "loop_schema": rel(LOOP_SCHEMA_PATH),
            "missing_object_class_index": rel(MISSING_OBJECT_CLASS_INDEX_PATH),
            "capability_stop_packet_schema": rel(CAPABILITY_STOP_PACKET_SCHEMA_PATH),
            "t6_objective": rel(T6_OBJECTIVE_PATH),
            "t6_audit_target": rel(T6_AUDIT_TARGET_PATH),
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
    print(f"runtime_t6_capability_boundary_objective_receipt_id={receipt_id}")
    print(f"runtime_t6_capability_boundary_objective_receipt_path={rel(receipt_path)}")
    print(f"runtime_t6_capability_boundary_objective_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
