#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "AUDIT_RUNTIME_T6_CAPABILITY_BOUNDARY_SURFACE_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.t6_capability_boundary_surface_audit_v0"

SOURCE_T6_BOUNDARY_OBJECTIVE_RECEIPT_ID = "6d1fd047"

T6_BOUNDARY_OBJECTIVE_RECEIPT_PATH = ROOT / "data/runtime_t6_capability_boundary_objective_v0_receipts/6d1fd047.json"
T6_OBJECTIVE_PATH = ROOT / "data/runtime_t6_capability_boundary_objective_v0/runtime_t6_capability_boundary_objective_v0.json"
T6_AUDIT_TARGET_PATH = ROOT / "data/runtime_t6_capability_boundary_objective_v0/runtime_t6_capability_boundary_surface_audit_target_v0.json"
LOOP_SCHEMA_PATH = ROOT / "data/runtime_t6_capability_boundary_objective_v0/current_surface_pressure_handling_loop_schema_v0_collection_stage.json"
MISSING_OBJECT_INDEX_PATH = ROOT / "data/runtime_t6_capability_boundary_objective_v0/runtime_t6_missing_object_class_index_v0.json"
CAPABILITY_STOP_PACKET_SCHEMA_PATH = ROOT / "data/runtime_t6_capability_boundary_objective_v0/runtime_t6_capability_stop_packet_schema_v0.json"

T6_FAILED_FEASIBILITY_RECEIPT_PATH = ROOT / "data/runtime_deferred_cases_t6_feasibility_v0_receipts/3d72600a.json"
T6_REGISTRY_PROFILE_PATH = ROOT / "data/runtime_deferred_cases_t6_feasibility_v0/runtime_t6_current_registry_trigger_profile_v0.json"
T6_MOVE_TIE_AUDIT_RECEIPT_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0_receipts/eb20d76b.json"
T6_MOVE_TIE_CLASSIFICATION_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0/runtime_t6_move_tie_surface_classification_v0.json"
T6_STRUCTURED_CANDIDATES_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0/runtime_t6_move_tie_structured_candidate_audit_v0.json"
T6_LOOP_CARRY_FORWARD_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0/runtime_t6_loop_surface_carry_forward_v0.json"

SMOKE_REGISTRY_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_move_registry_snapshot_v0.json"
REACHABILITY_MAP_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_registry_reachability_map_v0.json"

OUT_DIR = ROOT / "data/runtime_t6_capability_boundary_surface_audit_v0"
RECEIPT_DIR = ROOT / "data/runtime_t6_capability_boundary_surface_audit_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_t6_capability_boundary_surface_audit_basis_v0.json"
CURRENT_SURFACE_INVENTORY_PATH = OUT_DIR / "runtime_t6_current_surface_inventory_v0.json"
MISSING_OBJECT_DIAGNOSIS_PATH = OUT_DIR / "runtime_t6_missing_object_diagnosis_v0.json"
CAPABILITY_BOUNDARY_ASSESSMENT_PATH = OUT_DIR / "runtime_t6_capability_boundary_assessment_v0.json"
CAPABILITY_STOP_PACKET_PATH = OUT_DIR / "runtime_t6_capability_stop_packet_v0.json"
PARENT_RETURN_PAYLOAD_PATH = OUT_DIR / "runtime_t6_parent_return_payload_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_t6_capability_boundary_surface_audit_profile_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_t6_capability_boundary_surface_audit_rollup_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_t6_capability_boundary_surface_audit_transition_trace.json"

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
        T6_BOUNDARY_OBJECTIVE_RECEIPT_PATH,
        T6_OBJECTIVE_PATH,
        T6_AUDIT_TARGET_PATH,
        LOOP_SCHEMA_PATH,
        MISSING_OBJECT_INDEX_PATH,
        CAPABILITY_STOP_PACKET_SCHEMA_PATH,
        T6_FAILED_FEASIBILITY_RECEIPT_PATH,
        T6_REGISTRY_PROFILE_PATH,
        T6_MOVE_TIE_AUDIT_RECEIPT_PATH,
        T6_MOVE_TIE_CLASSIFICATION_PATH,
        T6_STRUCTURED_CANDIDATES_PATH,
        T6_LOOP_CARRY_FORWARD_PATH,
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

    objective_receipt = read_json(T6_BOUNDARY_OBJECTIVE_RECEIPT_PATH)
    objective_summary = objective_receipt.get("machine_readable_t6_capability_boundary_objective_summary", {})
    objective = read_json(T6_OBJECTIVE_PATH)
    audit_target = read_json(T6_AUDIT_TARGET_PATH)
    loop_schema = read_json(LOOP_SCHEMA_PATH)
    missing_index = read_json(MISSING_OBJECT_INDEX_PATH)
    stop_packet_schema = read_json(CAPABILITY_STOP_PACKET_SCHEMA_PATH)

    failed_feasibility_receipt = read_json(T6_FAILED_FEASIBILITY_RECEIPT_PATH)
    failed_feasibility_summary = failed_feasibility_receipt.get("machine_readable_t6_feasibility_summary", {})
    registry_profile = read_json(T6_REGISTRY_PROFILE_PATH)

    tie_audit_receipt = read_json(T6_MOVE_TIE_AUDIT_RECEIPT_PATH)
    tie_audit_summary = tie_audit_receipt.get("machine_readable_t6_move_tie_surface_audit_summary", {})
    tie_classification = read_json(T6_MOVE_TIE_CLASSIFICATION_PATH)
    structured_candidates = read_json(T6_STRUCTURED_CANDIDATES_PATH)
    loop_carry_forward = read_json(T6_LOOP_CARRY_FORWARD_PATH)

    smoke_registry = read_json(SMOKE_REGISTRY_PATH)
    reachability_map = read_json(REACHABILITY_MAP_PATH)

    if objective_receipt.get("receipt_id") != SOURCE_T6_BOUNDARY_OBJECTIVE_RECEIPT_ID:
        failures.append(f"objective_receipt_id_wrong:{objective_receipt.get('receipt_id')}")
    if objective_receipt.get("gate") != "PASS":
        failures.append("objective_gate_not_pass")
    if objective_summary.get("ready_for_t6_capability_boundary_surface_audit") is not True:
        failures.append("not_ready_for_t6_capability_boundary_surface_audit")
    if objective_summary.get("next_unit_id") != UNIT_ID:
        failures.append(f"objective_next_unit_wrong:{objective_summary.get('next_unit_id')}")
    if objective_summary.get("t6_repair_authorized") is not False:
        failures.append("t6_repair_should_not_be_authorized")
    if objective_summary.get("t6_case_contract_authorized") is not False:
        failures.append("t6_case_contract_should_not_be_authorized")

    if audit_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"audit_target_next_wrong:{audit_target.get('next_unit_id')}")
    if loop_schema.get("schema_name") != "CURRENT_SURFACE_PRESSURE_HANDLING_LOOP_SCHEMA_V0":
        failures.append("loop_schema_name_wrong")
    if loop_schema.get("schema_status") != "COLLECTION_STAGE_OBJECT":
        failures.append("loop_schema_status_wrong")
    if loop_schema.get("frozen_as_universal_base_schema") is not False:
        failures.append("loop_schema_universal_freeze_wrong")

    minimum_fields = stop_packet_schema.get("minimum_fields", [])
    required_packet_fields = [
        "required_capability",
        "surface_where_stop_occurred",
        "missing_object",
        "evidence_already_collected",
        "why_current_capability_cannot_proceed",
        "safe_next_human_choices",
        "receipt_ref",
        "parent_return_payload",
    ]
    if minimum_fields != required_packet_fields:
        failures.append("capability_stop_packet_minimum_fields_wrong")

    if failed_feasibility_summary.get("loop_trigger_available") is not False:
        failures.append("failed_feasibility_loop_should_be_false")
    if failed_feasibility_summary.get("tie_trigger_available") is not True:
        failures.append("failed_feasibility_tie_should_be_true")
    if "t6_trigger_surface_found_requires_human_contract_decision" not in failed_feasibility_receipt.get("failures", []):
        failures.append("failed_feasibility_reason_missing")

    if tie_audit_summary.get("classification_kind") != "DETECTOR_FALSE_POSITIVE_TEXT_ONLY_TIE_SURFACE":
        failures.append("tie_classification_not_text_only_false_positive")
    if tie_audit_summary.get("structured_tie_hit") is not False:
        failures.append("structured_tie_hit_should_be_false")
    if tie_audit_summary.get("computed_tie_group_count") != 0:
        failures.append("computed_tie_group_count_should_be_zero")
    if structured_candidates.get("real_unresolved_tie_surface_found") is not False:
        failures.append("real_unresolved_tie_surface_should_be_false")
    if loop_carry_forward.get("loop_trigger_available") is not False:
        failures.append("loop_carry_forward_should_be_false")

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
        require_false(objective_summary, key, failures)

    gate = "PASS" if not failures else "FAIL"

    current_surface_inventory = {
        "schema_version": "runtime_t6_current_surface_inventory_v0",
        "inventory_status": "EMITTED" if gate == "PASS" else "PARTIAL",
        "source_objective_ref": rel(T6_OBJECTIVE_PATH),
        "source_missing_object_index_ref": rel(MISSING_OBJECT_INDEX_PATH),
        "source_registry_profile_ref": rel(T6_REGISTRY_PROFILE_PATH),
        "source_reachability_map_ref": rel(REACHABILITY_MAP_PATH),
        "source_smoke_registry_ref": rel(SMOKE_REGISTRY_PATH),
        "available_surfaces": [
            {
                "surface": "runtime_move_registry_snapshot",
                "ref": rel(SMOKE_REGISTRY_PATH),
                "role": "current move registry / available move descriptions",
            },
            {
                "surface": "runtime_registry_reachability_map",
                "ref": rel(REACHABILITY_MAP_PATH),
                "role": "current reachability and trigger-profile surface",
            },
            {
                "surface": "t6_failed_feasibility_receipt",
                "ref": rel(T6_FAILED_FEASIBILITY_RECEIPT_PATH),
                "role": "prior stop showing a tie-surface signal requiring classification",
            },
            {
                "surface": "t6_move_tie_surface_audit",
                "ref": rel(T6_MOVE_TIE_AUDIT_RECEIPT_PATH),
                "role": "follow-up audit that classified the tie signal as text-only false positive",
            },
            {
                "surface": "t6_loop_carry_forward",
                "ref": rel(T6_LOOP_CARRY_FORWARD_PATH),
                "role": "loop surface carry-forward, no current loop trigger",
            },
        ],
        "surface_reading": {
            "loop_trigger_available": False,
            "tie_trigger_available_prior_signal": True,
            "tie_signal_classified_false_positive": True,
            "structured_tie_hit": False,
            "computed_tie_group_count": structured_candidates.get("computed_tie_group_count"),
            "real_unresolved_tie_surface_found": structured_candidates.get("real_unresolved_tie_surface_found"),
            "enough_evidence_to_contract_t6": False,
            "enough_evidence_to_emit_capability_boundary_stop": True,
        },
    }

    missing_object_diagnosis = {
        "schema_version": "runtime_t6_missing_object_diagnosis_v0",
        "diagnosis_status": "MISSING_OBJECTS_IDENTIFIED" if gate == "PASS" else "NOT_READY",
        "diagnoses": [
            {
                "case_key": "T6.step_cap_loop_shape",
                "missing_object": "loop_trigger_surface_missing",
                "surface_where_stop_occurred": "runtime registry reachability profile",
                "evidence_already_collected": [
                    "failed feasibility summary reported loop_trigger_available=false",
                    "loop carry-forward reported loop_trigger_available=false",
                    "no lawful loop/step-cap trigger surface is visible in the current registry profile",
                ],
                "object_is_missing": True,
                "object_is_classified": True,
                "object_is_repairable": False,
                "object_is_authorized": False,
                "object_is_representable": True,
                "object_is_within_current_capability": False,
                "why_not_contractable_now": "A T6 loop case requires a lawful loop or step-cap trigger surface; current evidence only proves absence of that trigger surface.",
            },
            {
                "case_key": "T6.move_tie_unresolved",
                "missing_object": "structured_tie_evidence_missing",
                "surface_where_stop_occurred": "runtime registry reachability profile / move-tie detector",
                "evidence_already_collected": [
                    "prior feasibility audit saw tie_trigger_available=true",
                    "follow-up audit classified this as DETECTOR_FALSE_POSITIVE_TEXT_ONLY_TIE_SURFACE",
                    "structured_tie_hit=false",
                    "move_tie_candidate_count=0",
                    "computed_tie_group_count=0",
                    "real_unresolved_tie_surface_found=false",
                ],
                "object_is_missing": True,
                "object_is_classified": True,
                "object_is_repairable": False,
                "object_is_authorized": False,
                "object_is_representable": True,
                "object_is_within_current_capability": False,
                "why_not_contractable_now": "A T6 move-tie case requires structured competing-move evidence; current capability has only text/noise evidence and zero computed tie groups.",
            },
        ],
        "shared_missing_boundary": {
            "missing_object": "bounded_t6_trigger_surface_capability",
            "meaning": "The current system can inspect existing registry surfaces, but cannot lawfully manufacture or introduce the missing loop/tie trigger surface inside this objective.",
            "anti_overclaim": "This does not prove T6 is invalid or impossible. It only exposes the current capability boundary.",
        },
    }

    required_capability = "bounded_structured_t6_trigger_surface_capability"

    capability_boundary_assessment = {
        "schema_version": "runtime_t6_capability_boundary_assessment_v0",
        "assessment_status": "CAPABILITY_BOUNDARY_FOUND" if gate == "PASS" else "NOT_READY",
        "current_capability_can_inspect_existing_surfaces": True,
        "current_capability_can_identify_missing_objects": True,
        "current_capability_can_classify_false_positive_tie_noise": True,
        "current_capability_can_contract_t6_now": False,
        "current_capability_can_repair_t6_now": False,
        "current_capability_can_add_moves_now": False,
        "current_capability_can_patch_runtime_now": False,
        "current_capability_can_generate_or_authorize_trigger_surface_now": False,
        "required_capability": required_capability,
        "required_capability_description": "A bounded capability that can either harden structured trigger-profile evidence for the current registry or introduce an explicitly authorized synthetic registry variant that contains lawful loop/tie trigger surfaces.",
        "why_current_capability_cannot_proceed": "Current surfaces expose no real loop trigger and no structured move-tie candidate. Proceeding to a T6 contract would require inventing or generating a trigger surface, which is outside current authority.",
        "result": "STOP_CAPABILITY_LAYER_REQUIRED",
    }

    safe_next_human_choices = [
        {
            "choice": "authorize_bounded_structured_trigger_profile_hardening",
            "meaning": "Improve the current registry/reachability profile so loop/tie trigger surfaces are structurally represented, without inventing values.",
        },
        {
            "choice": "authorize_bounded_synthetic_registry_variant_for_t6",
            "meaning": "Create an explicit synthetic registry variant designed to expose a loop or move-tie trigger, then test T6 against that bounded variant.",
        },
        {
            "choice": "defer_t6_again",
            "meaning": "Keep T6 preserved until a later capability layer exists.",
        },
        {
            "choice": "close_t6_for_current_registry_only",
            "meaning": "Record that the current registry has no contractable T6 trigger surface, without making a universal claim about T6.",
        },
    ]

    parent_return_payload = {
        "schema_version": "runtime_t6_parent_return_payload_v0",
        "payload_status": "EMITTED",
        "unit_id": UNIT_ID,
        "result": "STOP_CAPABILITY_LAYER_REQUIRED",
        "missing_objects": [
            "loop_trigger_surface_missing",
            "structured_tie_evidence_missing",
        ],
        "required_capability": required_capability,
        "bounded_next_proposition_available": False,
        "why_no_proposition": "A lawful T6 proposition requires a trigger surface or an authorized capability to construct one; neither exists in the current objective.",
        "safe_next_human_choices": safe_next_human_choices,
    }

    capability_stop_packet = {
        "schema_version": "runtime_t6_capability_stop_packet_v0",
        "stop_code": "STOP_CAPABILITY_LAYER_REQUIRED",
        "required_capability": required_capability,
        "surface_where_stop_occurred": "runtime registry reachability profile / T6 trigger surface boundary",
        "missing_object": [
            "loop_trigger_surface_missing",
            "structured_tie_evidence_missing",
            "bounded_t6_trigger_surface_capability",
        ],
        "evidence_already_collected": {
            "failed_feasibility_receipt_ref": rel(T6_FAILED_FEASIBILITY_RECEIPT_PATH),
            "failed_feasibility_reading": {
                "loop_trigger_available": failed_feasibility_summary.get("loop_trigger_available"),
                "tie_trigger_available": failed_feasibility_summary.get("tie_trigger_available"),
                "failures": failed_feasibility_receipt.get("failures"),
            },
            "move_tie_surface_audit_receipt_ref": rel(T6_MOVE_TIE_AUDIT_RECEIPT_PATH),
            "move_tie_surface_reading": {
                "classification_kind": tie_audit_summary.get("classification_kind"),
                "text_only_tie_hit": tie_audit_summary.get("text_only_tie_hit"),
                "structured_tie_hit": tie_audit_summary.get("structured_tie_hit"),
                "move_tie_candidate_count": tie_audit_summary.get("move_tie_candidate_count"),
                "computed_tie_group_count": tie_audit_summary.get("computed_tie_group_count"),
            },
            "loop_carry_forward_ref": rel(T6_LOOP_CARRY_FORWARD_PATH),
            "loop_carry_forward_reading": {
                "loop_trigger_available": loop_carry_forward.get("loop_trigger_available"),
                "classification": loop_carry_forward.get("classification"),
            },
        },
        "why_current_capability_cannot_proceed": "The current audit can inspect and classify available evidence, but it cannot lawfully create, infer, or authorize the missing T6 trigger surface. A T6 case contract would require structured trigger evidence or a separate authorized trigger-surface capability.",
        "safe_next_human_choices": safe_next_human_choices,
        "receipt_ref": None,
        "parent_return_payload": parent_return_payload,
        "anti_overclaim": {
            "does_not_mean": [
                "T6 is impossible",
                "T6 is invalid",
                "T6 is closed globally",
                "source content is universally absent",
                "human must accept a schema introduction",
            ],
            "does_mean": "The current capability layer cannot proceed lawfully on T6 without a bounded trigger-surface capability or human-declared next objective.",
        },
    }

    basis = {
        "schema_version": "runtime_t6_capability_boundary_surface_audit_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_t6_boundary_objective_receipt_id": SOURCE_T6_BOUNDARY_OBJECTIVE_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "T6 was reopened as a capability-boundary inspection objective; the audit should name the missing objects and stop if current capability cannot lawfully proceed.",
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

    status = (
        "TYPED_RUNTIME_T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT_STOP_CAPABILITY_LAYER_REQUIRED"
        if gate == "PASS"
        else "TYPED_RUNTIME_T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT_GATE_FAIL"
    )

    rollup = {
        "schema_version": "runtime_t6_capability_boundary_surface_audit_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "t6_capability_boundary_surface_audit_done": gate == "PASS",
        "audit_result_kind": "STOP_CAPABILITY_LAYER_REQUIRED" if gate == "PASS" else "GATE_FAIL",
        "bounded_proposition_emitted": False,
        "capability_stop_packet_emitted": gate == "PASS",
        "missing_object_count": 2 if gate == "PASS" else 0,
        "missing_objects": [
            "loop_trigger_surface_missing",
            "structured_tie_evidence_missing",
        ] if gate == "PASS" else [],
        "required_capability": required_capability if gate == "PASS" else None,
        "ready_for_t6_case_contract": False,
        "ready_for_t6_repair": False,
        "next_unit_id": None,
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
        "schema_version": "runtime_t6_capability_boundary_surface_audit_profile_v0",
        "profile_status": status,
        "core_rule": "T6 pressure must terminate as either a bounded proposition or a capability-stop packet. Current evidence supports the capability-stop packet.",
        "current_surface_inventory_ref": rel(CURRENT_SURFACE_INVENTORY_PATH),
        "missing_object_diagnosis_ref": rel(MISSING_OBJECT_DIAGNOSIS_PATH),
        "capability_boundary_assessment_ref": rel(CAPABILITY_BOUNDARY_ASSESSMENT_PATH),
        "capability_stop_packet_ref": rel(CAPABILITY_STOP_PACKET_PATH),
        "parent_return_payload_ref": rel(PARENT_RETURN_PAYLOAD_PATH),
        "recommended_next": None,
        "safe_next_human_choices": safe_next_human_choices,
        "must_not_infer": [
            "T6 is impossible",
            "T6 is globally closed",
            "runtime should be patched",
            "moves should be added",
            "fixtures should be expanded by default",
            "live runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    trace = {
        "schema_version": "runtime_t6_capability_boundary_surface_audit_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT_NEXT",
                "edge": "inspect current T6 pressure surface",
                "to": "T6_MISSING_OBJECTS_IDENTIFIED" if gate == "PASS" else "T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT_GATE_FAIL",
            },
            {
                "from": "T6_MISSING_OBJECTS_IDENTIFIED" if gate == "PASS" else "T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT_GATE_FAIL",
                "edge": "check current capability against missing objects",
                "to": "STOP_CAPABILITY_LAYER_REQUIRED" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "STOP",
            "next_unit_id": None,
            "stop_code": "STOP_CAPABILITY_LAYER_REQUIRED" if gate == "PASS" else "STOP_RUNTIME_T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (CURRENT_SURFACE_INVENTORY_PATH, current_surface_inventory),
        (MISSING_OBJECT_DIAGNOSIS_PATH, missing_object_diagnosis),
        (CAPABILITY_BOUNDARY_ASSESSMENT_PATH, capability_boundary_assessment),
        (PARENT_RETURN_PAYLOAD_PATH, parent_return_payload),
        (CAPABILITY_STOP_PACKET_PATH, capability_stop_packet),
        (PROFILE_PATH, profile),
        (ROLLUP_PATH, rollup),
        (TRACE_OUT_PATH, trace),
    ]:
        write_json(path, obj)

    source_hashes_after = {rel(p): file_sha256(p) for p in required}
    source_mutated = source_hashes_before != source_hashes_after
    if source_mutated:
        gate = "FAIL"
        status = "TYPED_RUNTIME_T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT_SOURCE_MUTATION_FAIL"
        failures.append("source_inputs_mutated")

    reason_codes = [
        "T6_BOUNDARY_OBJECTIVE_RECEIPT_CONSUMED",
        "CURRENT_SURFACE_PRESSURE_LOOP_SCHEMA_CONSUMED",
        "CURRENT_T6_SURFACES_INVENTORIED",
        "MISSING_OBJECTS_IDENTIFIED",
        "LOOP_TRIGGER_SURFACE_MISSING",
        "STRUCTURED_TIE_EVIDENCE_MISSING",
        "CURRENT_CAPABILITY_CANNOT_HANDLE_MISSING_T6_TRIGGER_SURFACE",
        "CAPABILITY_STOP_PACKET_EMITTED",
        "NO_T6_CASE_CONTRACT",
        "NO_T6_REPAIR",
        "NO_RUNTIME_PATCH",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_LIVE_RUNTIME_ADOPTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_t6_capability_boundary_surface_audit_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": "OUTER / RUNTIME_ADOPTION / T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT",
        "mode": "AUDIT_ONLY / MISSING_OBJECT_AND_CAPABILITY_BOUNDARY / NO_CASE_CONTRACT / NO_TEST_RUN",
        "build_mode": "T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT_ONLY",
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "source_t6_boundary_objective_receipt_id": SOURCE_T6_BOUNDARY_OBJECTIVE_RECEIPT_ID,
        "acceptance_gate_results": {
            "T6_SURFACE_0_OBJECTIVE_RECEIPT_CONSUMED": gate == "PASS",
            "T6_SURFACE_1_LOOP_SCHEMA_CONSUMED": gate == "PASS",
            "T6_SURFACE_2_CURRENT_SURFACES_INVENTORIED": gate == "PASS",
            "T6_SURFACE_3_MISSING_OBJECTS_IDENTIFIED": gate == "PASS",
            "T6_SURFACE_4_CAPABILITY_BOUNDARY_FOUND": gate == "PASS",
            "T6_SURFACE_5_STOP_PACKET_EMITTED": gate == "PASS",
            "T6_SURFACE_6_NO_T6_CASE_CONTRACT": gate == "PASS",
            "T6_SURFACE_7_NO_RUNTIME_PATCH": gate == "PASS",
            "T6_SURFACE_8_SOURCE_INPUTS_NOT_MUTATED": not source_mutated,
            "T6_SURFACE_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_t6_capability_boundary_surface_audit_summary": {
            "status": status,
            "t6_capability_boundary_surface_audit_done": gate == "PASS",
            "audit_result_kind": "STOP_CAPABILITY_LAYER_REQUIRED" if gate == "PASS" else "GATE_FAIL",
            "bounded_proposition_emitted": False,
            "capability_stop_packet_emitted": gate == "PASS",
            "stop_code": "STOP_CAPABILITY_LAYER_REQUIRED" if gate == "PASS" else "STOP_RUNTIME_T6_CAPABILITY_BOUNDARY_SURFACE_AUDIT_GATE_FAIL",
            "missing_object_count": 2 if gate == "PASS" else 0,
            "missing_objects": [
                "loop_trigger_surface_missing",
                "structured_tie_evidence_missing",
            ] if gate == "PASS" else [],
            "required_capability": required_capability if gate == "PASS" else None,
            "ready_for_t6_case_contract": False,
            "ready_for_t6_repair": False,
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
            "repair_authorized": False,
            "move_addition_authorized": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "current_surface_inventory": rel(CURRENT_SURFACE_INVENTORY_PATH),
            "missing_object_diagnosis": rel(MISSING_OBJECT_DIAGNOSIS_PATH),
            "capability_boundary_assessment": rel(CAPABILITY_BOUNDARY_ASSESSMENT_PATH),
            "capability_stop_packet": rel(CAPABILITY_STOP_PACKET_PATH),
            "parent_return_payload": rel(PARENT_RETURN_PAYLOAD_PATH),
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

    capability_stop_packet["receipt_ref"] = rel(receipt_path)
    write_json(CAPABILITY_STOP_PACKET_PATH, capability_stop_packet)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_t6_capability_boundary_surface_audit_receipt_id={receipt_id}")
    print(f"runtime_t6_capability_boundary_surface_audit_receipt_path={rel(receipt_path)}")
    print(f"runtime_t6_capability_boundary_surface_audit_next_unit=NONE")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
