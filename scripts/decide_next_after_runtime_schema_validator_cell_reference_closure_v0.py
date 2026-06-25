#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_RUNTIME_SCHEMA_VALIDATOR_CELL_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "runtime.schema_validator_cell.reference.post_closure_decision.v0"
LAYER = "RUNTIME / PRE_C8_INTERLOCK / POST_SCHEMA_VALIDATOR_REFERENCE_DECISION"
MODE = "DECIDE_ONLY / SELECT_OBSERVABILITY_SIDECAR_DESIGN / NO_RUNTIME_PATCH"
BUILD_MODE = "POST_RUNTIME_SCHEMA_VALIDATOR_REFERENCE_DECISION_ONLY"

SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID = "732016f0"
SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID = "ac09c2e3"

SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0_receipts/732016f0.json"
SCHEMA_VALIDATOR_CLOSURE_DIR = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0"

SCHEMA_VALIDATOR_CLOSURE_FILES = [
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_closure_basis_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_review_consumption_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reviewed_reference_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reviewed_reference_freeze_manifest_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_index_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_schema_surface_reference_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_demo_result_reference_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_packet_routing_reference_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_negative_control_reference_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_observability_hook_reference_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_observability_sidecar_design_prerequisite_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_post_closure_decision_ready_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_closure_authority_boundary_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_closure_classification_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_closure_rollup_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_closure_profile_v0.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_closure_report.json",
    SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_closure_transition_trace.json",
]

EDGE_OBS_REF_CLOSE_RECEIPT_PATH = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0_receipts/ac09c2e3.json"
EDGE_OBS_REF_DIR = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0"

EDGE_OBS_FILES = [
    EDGE_OBS_REF_DIR / "decision_edge_observability_reviewed_reference_v0.json",
    EDGE_OBS_REF_DIR / "decision_edge_observability_reviewed_reference_freeze_manifest_v0.json",
    EDGE_OBS_REF_DIR / "decision_edge_observability_requirement_reference_v0.json",
    EDGE_OBS_REF_DIR / "decision_edge_observability_field_schema_reference_v0.json",
    EDGE_OBS_REF_DIR / "decision_edge_observability_distinction_guard_reference_v0.json",
    EDGE_OBS_REF_DIR / "decision_edge_observability_negative_control_reference_v0.json",
]

REQUIRED_SOURCE_FILES = [
    SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH,
    EDGE_OBS_REF_CLOSE_RECEIPT_PATH,
] + SCHEMA_VALIDATOR_CLOSURE_FILES + EDGE_OBS_FILES

OUT_DIR = ROOT / "data/post_runtime_schema_validator_reference_decision_v0"
RECEIPT_DIR = ROOT / "data/post_runtime_schema_validator_reference_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "post_schema_validator_reference_decision_basis_v0.json"
SOURCE_SCHEMA_VALIDATOR_REFERENCE_REVIEW_PATH = OUT_DIR / "post_schema_validator_source_reference_review_v0.json"
SOURCE_EDGE_OBSERVABILITY_REFERENCE_REVIEW_PATH = OUT_DIR / "post_schema_validator_source_edge_observability_reference_review_v0.json"
DECISION_OPTIONS_PATH = OUT_DIR / "post_schema_validator_reference_decision_options_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "post_schema_validator_reference_selected_branch_v0.json"
SIDECAR_DESIGN_TARGET_PATH = OUT_DIR / "runtime_observability_sidecar_design_target_from_schema_validator_and_observability_references_v0.json"
SIDECAR_INPUT_REFERENCE_SET_PATH = OUT_DIR / "runtime_observability_sidecar_input_reference_set_v0.json"
PRE_C8_INTERLOCK_PLAN_PATH = OUT_DIR / "post_schema_validator_pre_c8_interlock_plan_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "post_schema_validator_reference_deferred_branches_v0.json"
REFERENCE_PARK_RECORD_PATH = OUT_DIR / "runtime_schema_validator_reference_park_record_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "post_schema_validator_reference_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "post_schema_validator_reference_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "post_schema_validator_reference_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "post_schema_validator_reference_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "post_schema_validator_reference_decision_report.json"
TRACE_PATH = OUT_DIR / "post_schema_validator_reference_decision_transition_trace.json"

EXPECTED_SOURCE_STATUS = "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY"
EXPECTED_SOURCE_NEXT = UNIT_ID

SELECTED_BRANCH = "DESIGN_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_FROM_SCHEMA_VALIDATOR_AND_OBSERVABILITY_REFERENCES"
SELECTED_NEXT_UNIT = "DESIGN_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_FROM_SCHEMA_VALIDATOR_AND_OBSERVABILITY_REFERENCES_V0"

REQUIRED_EDGE_FIELDS = [
    "active_object",
    "attempted_move",
    "boundary_checked",
    "boundary_result",
    "blocked_moves",
    "lawful_next_moves",
    "source_packet_ref",
]

SCHEMA_VALIDATOR_OBSERVABLE_EVENTS = [
    "schema_validation_started",
    "schema_loaded",
    "schema_validation_check_completed",
    "schema_validation_result",
    "validated_candidate_packet_emitted",
    "schema_feedback_packet_emitted",
    "schema_gap_feedback_packet_emitted",
    "schema_validator_receipt_emitted",
]

SIDECAR_INITIAL_HOOKS = [
    "proposal_created",
    "schema_validation_started",
    "schema_loaded",
    "schema_validation_check_completed",
    "schema_validation_result",
    "validated_candidate_packet_emitted",
    "schema_feedback_packet_emitted",
    "schema_gap_feedback_packet_emitted",
    "schema_validator_receipt_emitted",
    "admissibility_check_started",
    "admissibility_result",
    "admissibility_halt_emitted",
    "admissibility_allow_emitted",
    "execution_started",
    "execution_completed",
    "execution_failed",
    "verification_started",
    "verification_result",
    "handoff_emitted",
    "halt_emitted",
    "advance_emitted",
    "receipt_emitted",
    "decision_edge_observed",
    "unit_feedback_emitted",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    schema_validator_closure_receipt = read_json(SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH)
    schema_validator_summary = schema_validator_closure_receipt.get("machine_readable_runtime_schema_validator_reference_closure_summary", {})
    schema_validator_reference = read_json(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reviewed_reference_v0.json")
    schema_validator_freeze = read_json(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reviewed_reference_freeze_manifest_v0.json")
    schema_validator_observability_hooks = read_json(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_observability_hook_reference_v0.json")
    schema_validator_sidecar_prereq = read_json(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_observability_sidecar_design_prerequisite_v0.json")
    schema_validator_decision_ready = read_json(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_post_closure_decision_ready_v0.json")
    schema_validator_authority = read_json(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_closure_authority_boundary_v0.json")
    schema_validator_classification = read_json(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_closure_classification_v0.json")
    schema_validator_rollup = read_json(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_closure_rollup_v0.json")
    schema_validator_profile = read_json(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_closure_profile_v0.json")
    schema_validator_report = read_json(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_closure_report.json")
    schema_validator_trace = read_json(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reference_closure_transition_trace.json")

    edge_obs_closure_receipt = read_json(EDGE_OBS_REF_CLOSE_RECEIPT_PATH)
    edge_obs_reference = read_json(EDGE_OBS_REF_DIR / "decision_edge_observability_reviewed_reference_v0.json")
    edge_obs_freeze = read_json(EDGE_OBS_REF_DIR / "decision_edge_observability_reviewed_reference_freeze_manifest_v0.json")
    edge_obs_requirement = read_json(EDGE_OBS_REF_DIR / "decision_edge_observability_requirement_reference_v0.json")
    edge_obs_field_schema = read_json(EDGE_OBS_REF_DIR / "decision_edge_observability_field_schema_reference_v0.json")
    edge_obs_distinction = read_json(EDGE_OBS_REF_DIR / "decision_edge_observability_distinction_guard_reference_v0.json")
    edge_obs_negative = read_json(EDGE_OBS_REF_DIR / "decision_edge_observability_negative_control_reference_v0.json")

    if schema_validator_closure_receipt.get("receipt_id") != SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID or schema_validator_closure_receipt.get("gate") != "PASS":
        failures.append("schema_validator_closure_receipt_not_pass")
    if schema_validator_closure_receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("schema_validator_closure_stop_wrong")
    if schema_validator_closure_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("schema_validator_closure_hidden_next")
    if schema_validator_summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"schema_validator_closure_status_wrong:{schema_validator_summary.get('status')}")
    if schema_validator_summary.get("recommended_next") != EXPECTED_SOURCE_NEXT:
        failures.append(f"schema_validator_closure_next_wrong:{schema_validator_summary.get('recommended_next')}")

    for key in [
        "runtime_schema_validator_cell_closed_as_reviewed_reference",
        "reviewed_reference_frozen",
        "post_schema_validator_reference_decision_ready",
        "sidecar_design_prerequisite_satisfied",
        "source_edge_observability_reference_consumed",
        "schema_surface_frozen",
        "demo_result_reference_frozen",
        "packet_routing_reference_frozen",
        "negative_control_reference_frozen",
        "observability_hook_reference_frozen",
        "synthetic_demo_build_only",
        "observability_sidecar_deferred",
        "unit_feedback_hardening_deferred",
        "c7_deferred",
        "c8_deferred",
        "runtime_adoption_deferred",
        "bad_counters_zero",
    ]:
        if schema_validator_summary.get(key) is not True:
            failures.append(f"schema_validator_required_true_missing:{key}")

    for key in [
        "live_runtime_routing_installed",
        "runtime_effect",
        "runtime_patched",
        "authority_checked",
        "admissibility_checked",
        "execution_claimed",
        "schema_archive_mutated",
        "proposal_repaired",
        "schema_created",
        "builder_command_emitted",
        "c7_authorized",
        "c8_authorized",
        "new_domain_shift_executed",
        "general_cell1_authority_claimed",
        "global_autonomy_claimed",
        "full_transfer_claimed",
        "runtime_wide_enforcement_claimed",
        "source_mutated",
        "prior_receipt_mutated",
        "schema_validator_reference_mutated",
        "observability_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if schema_validator_summary.get(key) is not False:
            failures.append(f"schema_validator_forbidden_true:{key}")

    for key, expected in {
        "proposals_evaluated": 16,
        "valid_count": 2,
        "invalid_count": 14,
        "advanced_to_admissibility_count": 2,
        "returned_to_builder_count": 14,
        "hidden_execution_field_count": 1,
        "observable_event_count": 8,
        "load_bearing_edge_field_count": 7,
    }.items():
        if schema_validator_summary.get(key) != expected:
            failures.append(f"schema_validator_count_wrong:{key}:{schema_validator_summary.get(key)}")

    if schema_validator_reference.get("reference_status") != "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_FROZEN":
        failures.append("schema_validator_reference_not_frozen")
    if schema_validator_freeze.get("freeze_status") != "FROZEN":
        failures.append("schema_validator_freeze_not_frozen")
    if schema_validator_observability_hooks.get("schema_validator_surface_observable_events") != SCHEMA_VALIDATOR_OBSERVABLE_EVENTS:
        failures.append("schema_validator_observable_events_wrong")
    if schema_validator_sidecar_prereq.get("prerequisite_status") != "SATISFIED":
        failures.append("schema_validator_sidecar_prereq_not_satisfied")
    if schema_validator_sidecar_prereq.get("next_candidate_branch") != SELECTED_BRANCH:
        failures.append("schema_validator_sidecar_candidate_wrong")
    if schema_validator_decision_ready.get("decision_ready") is not True:
        failures.append("schema_validator_decision_ready_false")
    if schema_validator_decision_ready.get("strong_candidate") != SELECTED_NEXT_UNIT:
        failures.append("schema_validator_strong_candidate_wrong")
    if schema_validator_authority.get("may_decide_next_after_schema_validator_reference_closure") is not True:
        failures.append("schema_validator_authority_no_decide_next")
    if schema_validator_classification.get("next_command_goal") is not None:
        failures.append("schema_validator_classification_hidden_next")
    if schema_validator_rollup.get("sidecar_design_count") != 0 or schema_validator_rollup.get("sidecar_build_count") != 0:
        failures.append("schema_validator_sidecar_already_designed_or_built")
    if schema_validator_profile.get("next_command_goal") is not None:
        failures.append("schema_validator_profile_hidden_next")
    if schema_validator_report.get("recommended_next_handling") != EXPECTED_SOURCE_NEXT:
        failures.append("schema_validator_report_next_wrong")
    if schema_validator_trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("schema_validator_trace_hidden_next")

    if edge_obs_closure_receipt.get("receipt_id") != SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID or edge_obs_closure_receipt.get("gate") != "PASS":
        failures.append("edge_obs_closure_receipt_not_pass")
    if edge_obs_reference.get("reference_status") != "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_FROZEN":
        failures.append("edge_obs_reference_not_frozen")
    if edge_obs_freeze.get("freeze_status") != "FROZEN":
        failures.append("edge_obs_freeze_not_frozen")
    if edge_obs_requirement.get("required_fields") != REQUIRED_EDGE_FIELDS:
        failures.append("edge_obs_required_fields_wrong")
    if edge_obs_requirement.get("edge_requirement_count") != 7:
        failures.append("edge_obs_requirement_count_wrong")
    if edge_obs_field_schema.get("required_field_count") != 7:
        failures.append("edge_obs_field_count_wrong")
    if edge_obs_distinction.get("guard_count") != 8:
        failures.append("edge_obs_guard_count_wrong")
    if edge_obs_negative.get("negative_control_count") != 13:
        failures.append("edge_obs_negative_count_wrong")

    return failures, {
        "schema_validator_summary": schema_validator_summary,
        "schema_validator_reference": schema_validator_reference,
        "schema_validator_observability_hooks": schema_validator_observability_hooks,
        "schema_validator_sidecar_prereq": schema_validator_sidecar_prereq,
        "schema_validator_decision_ready": schema_validator_decision_ready,
        "edge_obs_reference": edge_obs_reference,
        "edge_obs_requirement": edge_obs_requirement,
        "edge_obs_field_schema": edge_obs_field_schema,
        "edge_obs_distinction": edge_obs_distinction,
        "edge_obs_negative": edge_obs_negative,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    decision_pass = not failures
    status = "TYPED_POST_SCHEMA_VALIDATOR_REFERENCE_DECISION_SELECTED_OBSERVABILITY_SIDECAR_DESIGN_READY" if decision_pass else "TYPED_POST_SCHEMA_VALIDATOR_REFERENCE_DECISION_GATE_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_POST_SCHEMA_VALIDATOR_REFERENCE_DECISION_V0"

    schema_validator_summary = basis.get("schema_validator_summary", {})
    schema_validator_reference = basis.get("schema_validator_reference", {})
    schema_validator_observability_hooks = basis.get("schema_validator_observability_hooks", {})
    schema_validator_sidecar_prereq = basis.get("schema_validator_sidecar_prereq", {})
    edge_obs_reference = basis.get("edge_obs_reference", {})
    edge_obs_requirement = basis.get("edge_obs_requirement", {})
    edge_obs_field_schema = basis.get("edge_obs_field_schema", {})
    edge_obs_distinction = basis.get("edge_obs_distinction", {})
    edge_obs_negative = basis.get("edge_obs_negative", {})

    reason_codes = [
        "POST_SCHEMA_VALIDATOR_REFERENCE_DECISION_COMPLETE",
        "RUNTIME_SCHEMA_VALIDATOR_REFERENCE_CLOSURE_RECEIPT_CONSUMED",
        "RUNTIME_SCHEMA_VALIDATOR_REVIEWED_REFERENCE_CONFIRMED",
        "DECISION_EDGE_OBSERVABILITY_REFERENCE_CONFIRMED",
        "SIDECAR_DESIGN_PREREQUISITE_CONFIRMED",
        "OBSERVABILITY_SIDECAR_DESIGN_SELECTED",
        "SIDECAR_TARGET_EMITTED",
        "SIDECAR_INPUT_REFERENCE_SET_EMITTED",
        "PRE_C8_INTERLOCK_PLAN_UPDATED",
        "SCHEMA_VALIDATOR_REFERENCE_PARKED",
        "C8_DEFERRED_UNTIL_SIDECAR_REFERENCE_EXISTS",
        "UNIT_FEEDBACK_HARDENING_DEFERRED",
        "NO_SIDECAR_BUILD",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_RUNTIME_ROUTING",
        "NO_C7_AUTHORIZATION",
        "NO_C8_AUTHORIZATION",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if decision_pass else failures

    decision_basis = {
        "schema_version": "post_schema_validator_reference_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "source_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "source_schema_validator_reference_status": schema_validator_reference.get("reference_status"),
        "source_edge_observability_reference_status": edge_obs_reference.get("reference_status"),
        "decision_scope": "select next pre-C8 interlock branch after Schema Validator reference closure",
    }

    schema_validator_reference_review = {
        "schema_version": "post_schema_validator_source_reference_review_v0",
        "source_reference_receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "reference_status": schema_validator_reference.get("reference_status"),
        "sidecar_design_prerequisite_satisfied": schema_validator_summary.get("sidecar_design_prerequisite_satisfied"),
        "observable_event_count": schema_validator_summary.get("observable_event_count"),
        "observable_events": schema_validator_observability_hooks.get("schema_validator_surface_observable_events"),
        "valid_advances_only_to": schema_validator_reference.get("valid_advances_only_to"),
        "invalid_returns_to": schema_validator_reference.get("invalid_returns_to"),
        "live_runtime_routing_installed": schema_validator_summary.get("live_runtime_routing_installed"),
    }

    edge_observability_reference_review = {
        "schema_version": "post_schema_validator_source_edge_observability_reference_review_v0",
        "source_reference_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "reference_status": edge_obs_reference.get("reference_status"),
        "edge_requirement_count": edge_obs_requirement.get("edge_requirement_count"),
        "required_fields": edge_obs_requirement.get("required_fields"),
        "field_schema_count": edge_obs_field_schema.get("required_field_count"),
        "distinction_guard_count": edge_obs_distinction.get("guard_count"),
        "negative_control_count": edge_obs_negative.get("negative_control_count"),
    }

    decision_options = {
        "schema_version": "post_schema_validator_reference_decision_options_v0",
        "decision_status": "OPTIONS_REVIEWED",
        "options": [
            {
                "option_id": "DESIGN_RUNTIME_OBSERVABILITY_SIDECAR_TARGET",
                "selected": True,
                "why": "Both prerequisites now exist: decision-edge observability reference and Schema Validator reviewed reference.",
                "next_unit": SELECTED_NEXT_UNIT,
            },
            {
                "option_id": "C8",
                "selected": False,
                "why_not": "C8 remains deferred until the Observability Sidecar reference exists.",
            },
            {
                "option_id": "LIVE_RUNTIME_ROUTING",
                "selected": False,
                "why_not": "Schema Validator reference is synthetic/demo and not live routing.",
            },
            {
                "option_id": "UNIT_FEEDBACK_HARDENING",
                "selected": False,
                "why_not": "Deferred until the pre-C8 interlock pair is complete.",
            },
            {
                "option_id": "C7_OR_DOMAIN_SHIFT",
                "selected": False,
                "why_not": "Outside current pre-C8 interlock closure path.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "post_schema_validator_reference_selected_branch_v0",
        "selected_branch": SELECTED_BRANCH,
        "selected_next_unit": SELECTED_NEXT_UNIT,
        "selection_status": "SELECTED_DESIGN_READY" if decision_pass else "NOT_SELECTED",
        "selection_meaning": "Design the Runtime Observability Sidecar target using the frozen Schema Validator reference and frozen decision-edge observability reference.",
    }

    sidecar_input_reference_set = {
        "schema_version": "runtime_observability_sidecar_input_reference_set_v0",
        "reference_set_status": "READY_FOR_SIDECAR_TARGET_DESIGN" if decision_pass else "NOT_READY",
        "schema_validator_reference": {
            "receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
            "reference_path": rel(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reviewed_reference_v0.json"),
            "observability_hook_reference_path": rel(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_observability_hook_reference_v0.json"),
            "sidecar_design_prerequisite_path": rel(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_observability_sidecar_design_prerequisite_v0.json"),
        },
        "decision_edge_observability_reference": {
            "receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
            "reference_path": rel(EDGE_OBS_REF_DIR / "decision_edge_observability_reviewed_reference_v0.json"),
            "requirement_reference_path": rel(EDGE_OBS_REF_DIR / "decision_edge_observability_requirement_reference_v0.json"),
            "field_schema_reference_path": rel(EDGE_OBS_REF_DIR / "decision_edge_observability_field_schema_reference_v0.json"),
        },
        "required_load_bearing_edge_fields": REQUIRED_EDGE_FIELDS,
        "schema_validator_observable_events": SCHEMA_VALIDATOR_OBSERVABLE_EVENTS,
    }

    sidecar_design_target = {
        "schema_version": "runtime_observability_sidecar_design_target_from_schema_validator_and_observability_references_v0",
        "target_status": "DESIGN_READY" if decision_pass else "NOT_READY",
        "future_design_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "target_unit_id": "runtime.observability_sidecar.target_design.v0",
        "layer": "RUNTIME / OBSERVATION / SIDECAR_TARGET_DESIGN",
        "mode": "DESIGN_ONLY / OBSERVE_EMIT_RECEIPT_APPEND_ONLY / NO_CONTROL_AUTHORITY",
        "core_compression": "Control path acts. Sidecar records.",
        "authority_law": "The sidecar has eyes, not hands.",
        "role": "event capture and load-bearing receipt surface for predefined runtime events",
        "must_design": [
            "registered event hook table",
            "event record schema",
            "sidecar receipt schema",
            "append-only trace schema",
            "rollup/readout/profile/report schema",
            "unknown hook behavior",
            "forbidden field behavior",
            "non-blocking failure behavior",
            "blocking-by-policy claim behavior",
            "observability alignment to decision-edge required fields",
        ],
        "initial_hook_set": SIDECAR_INITIAL_HOOKS,
        "load_bearing_edge_fields": REQUIRED_EDGE_FIELDS,
        "must_preserve_boundaries": [
            "no validation authority",
            "no admissibility authority",
            "no execution authority",
            "no proposal authority",
            "no repair authority",
            "no runtime patch",
            "no live instrumentation install",
            "no hidden context",
            "no unbounded payload logging",
            "no schema mutation",
            "no C8 authorization",
        ],
        "must_not_build_yet": True,
        "must_not_install_live_runtime_hooks_yet": True,
    }

    pre_c8_interlock_plan = {
        "schema_version": "post_schema_validator_pre_c8_interlock_plan_v0",
        "plan_status": "SECOND_INTERLOCK_OBJECT_SELECTED_FOR_DESIGN",
        "completed_pre_c8_mechanics": [
            {
                "object": "Schema Validator Cell",
                "status": "REVIEWED_REFERENCE_FROZEN",
                "receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
            }
        ],
        "selected_now": {
            "object": "Observability Sidecar",
            "status": "TARGET_DESIGN_SELECTED",
            "next_unit": SELECTED_NEXT_UNIT,
        },
        "remaining_before_c8": [
            "design Observability Sidecar target",
            "build Observability Sidecar synthetic/reference surface",
            "review Observability Sidecar surface",
            "close Observability Sidecar as reviewed reference",
            "then decide whether C8 can be considered",
        ],
        "nothing_else_before_c8": True,
    }

    deferred_branches = {
        "schema_version": "post_schema_validator_reference_deferred_branches_v0",
        "deferred": [
            "BUILD_RUNTIME_OBSERVABILITY_SIDECAR_V0",
            "LIVE_RUNTIME_ROUTING_INSTALLATION",
            "RUNTIME_PATCH",
            "C8",
            "C7",
            "UNIT_FEEDBACK_HARDENING",
            "NEW_DOMAIN_SHIFT",
            "TRANSFER_AUTONOMY",
            "GENERAL_CELL1_AUTHORITY",
            "RUNTIME_WIDE_ENFORCEMENT",
        ],
        "selected": SELECTED_NEXT_UNIT if decision_pass else None,
    }

    reference_park_record = {
        "schema_version": "runtime_schema_validator_reference_park_record_v0",
        "park_status": "PARKED_AS_INPUT_REFERENCE_FOR_SIDECAR_DESIGN",
        "schema_validator_reference_receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "schema_validator_reference_path": rel(SCHEMA_VALIDATOR_CLOSURE_DIR / "runtime_schema_validator_reviewed_reference_v0.json"),
        "edge_observability_reference_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "edge_observability_reference_path": rel(EDGE_OBS_REF_DIR / "decision_edge_observability_reviewed_reference_v0.json"),
    }

    authority_boundary = {
        "schema_version": "post_schema_validator_reference_decision_authority_boundary_v0",
        "status": status,
        "may_design_observability_sidecar_target_next": decision_pass,
        "may_build_observability_sidecar_now": False,
        "may_install_live_runtime_hooks": False,
        "may_install_live_runtime_routing": False,
        "may_patch_runtime_now": False,
        "may_check_authority": False,
        "may_check_admissibility": False,
        "may_execute": False,
        "may_repair_proposal": False,
        "may_mutate_schema_archive": False,
        "may_create_schema": False,
        "may_emit_builder_command": False,
        "may_open_c7_now": False,
        "may_open_c8_now": False,
        "may_harden_unit_feedback_now": False,
        "may_execute_new_domain_shift": False,
        "may_claim_full_transfer": False,
        "may_claim_global_autonomy": False,
        "may_claim_general_cell1_authority": False,
        "may_claim_runtime_wide_enforcement": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_mutate_schema_validator_reference": False,
        "may_mutate_observability_reference": False,
    }

    classification = {
        "schema_version": "post_schema_validator_reference_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_schema_validator_reference_decision_complete": decision_pass,
        "observability_sidecar_design_selected": decision_pass,
        "observability_sidecar_design_ready": decision_pass,
        "schema_validator_reference_consumed": True,
        "edge_observability_reference_consumed": True,
        "sidecar_input_reference_set_ready": decision_pass,
        "pre_c8_interlock_second_object_selected": decision_pass,
        "schema_validator_reference_parked": decision_pass,
        "observability_sidecar_built": False,
        "observability_sidecar_live": False,
        "live_runtime_hooks_installed": False,
        "live_runtime_routing_installed": False,
        "unit_feedback_hardening_deferred": True,
        "c7_deferred": True,
        "c8_deferred": True,
        "runtime_adoption_deferred": True,
        "runtime_effect": False,
        "runtime_patched": False,
        "authority_checked": False,
        "admissibility_checked": False,
        "execution_claimed": False,
        "schema_archive_mutated": False,
        "proposal_repaired": False,
        "schema_created": False,
        "builder_command_emitted": False,
        "c7_authorized": False,
        "c8_authorized": False,
        "new_domain_shift_executed": False,
        "general_cell1_authority_claimed": False,
        "global_autonomy_claimed": False,
        "full_transfer_claimed": False,
        "runtime_wide_enforcement_claimed": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "schema_validator_reference_mutated": False,
        "observability_reference_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": decision_pass,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "post_schema_validator_reference_decision_rollup_v0",
        "decision_count": 1 if decision_pass else 0,
        "sidecar_design_selected_count": 1 if decision_pass else 0,
        "sidecar_design_ready_count": 1 if decision_pass else 0,
        "schema_validator_reference_consumed_count": 1,
        "edge_observability_reference_consumed_count": 1,
        "schema_validator_observable_event_count": len(SCHEMA_VALIDATOR_OBSERVABLE_EVENTS),
        "sidecar_initial_hook_count": len(SIDECAR_INITIAL_HOOKS),
        "load_bearing_edge_field_count": len(REQUIRED_EDGE_FIELDS),
        "observability_sidecar_build_count": 0,
        "live_runtime_hooks_installed_count": 0,
        "live_runtime_routing_installed_count": 0,
        "runtime_patch_count": 0,
        "authority_checked_count": 0,
        "admissibility_checked_count": 0,
        "execution_claim_count": 0,
        "schema_archive_mutation_count": 0,
        "proposal_repair_count": 0,
        "schema_created_count": 0,
        "builder_command_emitted_count": 0,
        "c7_authorized_count": 0,
        "c8_authorized_count": 0,
        "unit_feedback_hardening_count": 0,
        "runtime_wide_enforcement_claim_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "post_schema_validator_reference_decision_profile_v0",
        "profile_id": "post_schema_validator_reference_decision_" + sig8(rollup),
        "status": status,
        "decision_result": "OBSERVABILITY_SIDECAR_TARGET_DESIGN_SELECTED" if decision_pass else "REPAIR_REQUIRED",
        "completed_first_interlock_object": "Schema Validator Cell reviewed reference",
        "selected_second_interlock_object": "Runtime Observability Sidecar target design",
        "next_unit": recommended_next,
        "sidecar_law": "The sidecar has eyes, not hands.",
        "control_path_rule": "Control path acts. Sidecar records.",
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "c8_authorized": False,
        "must_not_infer": [
            "Sidecar was designed",
            "Sidecar was built",
            "Runtime hooks were installed",
            "Runtime routing was patched",
            "C8 is authorized",
            "Schema Validator is live routing",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "post_schema_validator_reference_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The post-Schema-Validator-reference decision consumed the frozen Schema Validator reviewed reference and the frozen decision-edge observability reference, then selected Runtime Observability Sidecar target design as the next lawful object. The decision emits the Sidecar design target and input reference set, but does not design/build the Sidecar, install live hooks, patch runtime, open C8, harden unit feedback, or claim broader authority.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "post_schema_validator_reference_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_schema_validator_reference_closure",
                "question": "is Schema Validator reference frozen and decision-ready",
                "answer": "yes" if decision_pass else "no",
                "taken": "consume frozen reference as sidecar prerequisite",
            },
            {
                "step": "consume_decision_edge_observability_reference",
                "question": "is load-bearing edge-field reference available",
                "answer": "yes" if decision_pass else "no",
                "taken": "use required fields and observability distinctions as sidecar design basis",
            },
            {
                "step": "select_next_branch",
                "question": "what is the next pre-C8 interlock object",
                "answer": "Runtime Observability Sidecar target design" if decision_pass else "repair",
                "taken": "emit selected branch and stop decision-only",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (DECISION_BASIS_PATH, decision_basis),
        (SOURCE_SCHEMA_VALIDATOR_REFERENCE_REVIEW_PATH, schema_validator_reference_review),
        (SOURCE_EDGE_OBSERVABILITY_REFERENCE_REVIEW_PATH, edge_observability_reference_review),
        (DECISION_OPTIONS_PATH, decision_options),
        (SELECTED_BRANCH_PATH, selected_branch),
        (SIDECAR_DESIGN_TARGET_PATH, sidecar_design_target),
        (SIDECAR_INPUT_REFERENCE_SET_PATH, sidecar_input_reference_set),
        (PRE_C8_INTERLOCK_PLAN_PATH, pre_c8_interlock_plan),
        (DEFERRED_BRANCHES_PATH, deferred_branches),
        (REFERENCE_PARK_RECORD_PATH, reference_park_record),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, trace),
    ]

    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "POST_SCHEMA_VALIDATOR_DECISION_0_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_CONSUMED": SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH.exists(),
        "POST_SCHEMA_VALIDATOR_DECISION_1_SCHEMA_VALIDATOR_REFERENCE_CONFIRMED": schema_validator_reference.get("reference_status") == "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_FROZEN",
        "POST_SCHEMA_VALIDATOR_DECISION_2_EDGE_OBSERVABILITY_REFERENCE_CONFIRMED": edge_obs_reference.get("reference_status") == "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_FROZEN",
        "POST_SCHEMA_VALIDATOR_DECISION_3_SIDECAR_PREREQUISITE_CONFIRMED": schema_validator_sidecar_prereq.get("prerequisite_status") == "SATISFIED",
        "POST_SCHEMA_VALIDATOR_DECISION_4_SIDECAR_DESIGN_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "POST_SCHEMA_VALIDATOR_DECISION_5_SIDECAR_TARGET_EMITTED": SIDECAR_DESIGN_TARGET_PATH.exists() and sidecar_design_target["target_status"] == "DESIGN_READY",
        "POST_SCHEMA_VALIDATOR_DECISION_6_INPUT_REFERENCE_SET_EMITTED": SIDECAR_INPUT_REFERENCE_SET_PATH.exists(),
        "POST_SCHEMA_VALIDATOR_DECISION_7_PRE_C8_PLAN_UPDATED": PRE_C8_INTERLOCK_PLAN_PATH.exists() and pre_c8_interlock_plan["nothing_else_before_c8"] is True,
        "POST_SCHEMA_VALIDATOR_DECISION_8_DEFERRED_BRANCHES_EMITTED": DEFERRED_BRANCHES_PATH.exists(),
        "POST_SCHEMA_VALIDATOR_DECISION_9_SCHEMA_VALIDATOR_REFERENCE_PARKED": REFERENCE_PARK_RECORD_PATH.exists(),
        "POST_SCHEMA_VALIDATOR_DECISION_10_NO_SIDECAR_BUILD": rollup["observability_sidecar_build_count"] == 0,
        "POST_SCHEMA_VALIDATOR_DECISION_11_NO_LIVE_RUNTIME_HOOKS_OR_ROUTING": classification["live_runtime_hooks_installed"] is False and classification["live_runtime_routing_installed"] is False,
        "POST_SCHEMA_VALIDATOR_DECISION_12_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "POST_SCHEMA_VALIDATOR_DECISION_13_NO_AUTHORITY_ADMISSIBILITY_OR_EXECUTION": classification["authority_checked"] is False and classification["admissibility_checked"] is False and classification["execution_claimed"] is False,
        "POST_SCHEMA_VALIDATOR_DECISION_14_NO_SCHEMA_MUTATION_OR_REPAIR": classification["schema_archive_mutated"] is False and classification["proposal_repaired"] is False and classification["schema_created"] is False,
        "POST_SCHEMA_VALIDATOR_DECISION_15_NO_BUILDER_COMMAND": classification["builder_command_emitted"] is False,
        "POST_SCHEMA_VALIDATOR_DECISION_16_NO_C7_OR_C8": classification["c7_authorized"] is False and classification["c8_authorized"] is False,
        "POST_SCHEMA_VALIDATOR_DECISION_17_UNIT_FEEDBACK_DEFERRED": classification["unit_feedback_hardening_deferred"] is True,
        "POST_SCHEMA_VALIDATOR_DECISION_18_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "POST_SCHEMA_VALIDATOR_DECISION_19_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["schema_validator_reference_mutated"] is False and classification["observability_reference_mutated"] is False,
        "POST_SCHEMA_VALIDATOR_DECISION_20_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "POST_SCHEMA_VALIDATOR_DECISION_21_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "POST_SCHEMA_VALIDATOR_DECISION_22_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "POST_SCHEMA_VALIDATOR_DECISION_23_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_POST_SCHEMA_VALIDATOR_REFERENCE_DECISION_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_POST_SCHEMA_VALIDATOR_REFERENCE_DECISION_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_POST_SCHEMA_VALIDATOR_REFERENCE_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_schema_validator_closure": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "selected_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "post_schema_validator_reference_decision_receipt_v0",
        "receipt_type": "TYPED_POST_SCHEMA_VALIDATOR_REFERENCE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_runtime_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "machine_readable_post_schema_validator_reference_decision_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_schema_validator_reference_decision_complete": gate == "PASS",
            "observability_sidecar_design_selected": gate == "PASS",
            "observability_sidecar_design_ready": gate == "PASS",
            "selected_branch": SELECTED_BRANCH if gate == "PASS" else None,
            "selected_next_unit": final_next,
            "schema_validator_reference_consumed": True,
            "edge_observability_reference_consumed": True,
            "sidecar_input_reference_set_ready": gate == "PASS",
            "pre_c8_interlock_second_object_selected": gate == "PASS",
            "schema_validator_observable_event_count": len(SCHEMA_VALIDATOR_OBSERVABLE_EVENTS),
            "sidecar_initial_hook_count": len(SIDECAR_INITIAL_HOOKS),
            "load_bearing_edge_field_count": len(REQUIRED_EDGE_FIELDS),
            "schema_validator_reference_parked": gate == "PASS",
            "observability_sidecar_built": False,
            "observability_sidecar_live": False,
            "live_runtime_hooks_installed": False,
            "live_runtime_routing_installed": False,
            "unit_feedback_hardening_deferred": True,
            "c7_deferred": True,
            "c8_deferred": True,
            "runtime_adoption_deferred": True,
            "runtime_effect": False,
            "runtime_patched": False,
            "authority_checked": False,
            "admissibility_checked": False,
            "execution_claimed": False,
            "schema_archive_mutated": False,
            "proposal_repaired": False,
            "schema_created": False,
            "builder_command_emitted": False,
            "c7_authorized": False,
            "c8_authorized": False,
            "new_domain_shift_executed": False,
            "general_cell1_authority_claimed": False,
            "global_autonomy_claimed": False,
            "full_transfer_claimed": False,
            "runtime_wide_enforcement_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "schema_validator_reference_mutated": False,
            "observability_reference_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": gate == "PASS",
            "recommended_next": final_next,
        },
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "decision_basis": rel(DECISION_BASIS_PATH),
            "source_schema_validator_reference_review": rel(SOURCE_SCHEMA_VALIDATOR_REFERENCE_REVIEW_PATH),
            "source_edge_observability_reference_review": rel(SOURCE_EDGE_OBSERVABILITY_REFERENCE_REVIEW_PATH),
            "decision_options": rel(DECISION_OPTIONS_PATH),
            "selected_branch": rel(SELECTED_BRANCH_PATH),
            "sidecar_design_target": rel(SIDECAR_DESIGN_TARGET_PATH),
            "sidecar_input_reference_set": rel(SIDECAR_INPUT_REFERENCE_SET_PATH),
            "pre_c8_interlock_plan": rel(PRE_C8_INTERLOCK_PLAN_PATH),
            "deferred_branches": rel(DEFERRED_BRANCHES_PATH),
            "reference_park_record": rel(REFERENCE_PARK_RECORD_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"post_schema_validator_reference_decision_receipt_id={receipt_id}")
    print(f"post_schema_validator_reference_decision_receipt_path={rel(receipt_path)}")
    print(f"runtime_observability_sidecar_design_target_path={rel(SIDECAR_DESIGN_TARGET_PATH)}")
    print(f"runtime_observability_sidecar_input_reference_set_path={rel(SIDECAR_INPUT_REFERENCE_SET_PATH)}")
    print(f"post_schema_validator_reference_selected_branch_path={rel(SELECTED_BRANCH_PATH)}")
    print(f"post_schema_validator_reference_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"post_schema_validator_reference_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
