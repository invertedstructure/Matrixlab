#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DESIGN_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_FROM_SCHEMA_VALIDATOR_AND_OBSERVABILITY_REFERENCES_V0"
TARGET_UNIT_ID = "runtime.observability_sidecar.target_design.v0"
LAYER = "RUNTIME / OBSERVATION / SIDECAR_TARGET_DESIGN"
MODE = "DESIGN_ONLY / OBSERVE_EMIT_RECEIPT_APPEND_ONLY / NO_CONTROL_AUTHORITY"
BUILD_MODE = "RUNTIME_OBSERVABILITY_SIDECAR_TARGET_DESIGN_ONLY"

SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID = "1ca1e03b"
SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID = "732016f0"
SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID = "ac09c2e3"

POST_DECISION_RECEIPT_PATH = ROOT / "data/post_runtime_schema_validator_reference_decision_v0_receipts/1ca1e03b.json"
POST_DECISION_DIR = ROOT / "data/post_runtime_schema_validator_reference_decision_v0"

POST_DECISION_FILES = [
    POST_DECISION_DIR / "post_schema_validator_reference_decision_basis_v0.json",
    POST_DECISION_DIR / "post_schema_validator_source_reference_review_v0.json",
    POST_DECISION_DIR / "post_schema_validator_source_edge_observability_reference_review_v0.json",
    POST_DECISION_DIR / "post_schema_validator_reference_decision_options_v0.json",
    POST_DECISION_DIR / "post_schema_validator_reference_selected_branch_v0.json",
    POST_DECISION_DIR / "runtime_observability_sidecar_design_target_from_schema_validator_and_observability_references_v0.json",
    POST_DECISION_DIR / "runtime_observability_sidecar_input_reference_set_v0.json",
    POST_DECISION_DIR / "post_schema_validator_pre_c8_interlock_plan_v0.json",
    POST_DECISION_DIR / "post_schema_validator_reference_deferred_branches_v0.json",
    POST_DECISION_DIR / "runtime_schema_validator_reference_park_record_v0.json",
    POST_DECISION_DIR / "post_schema_validator_reference_decision_authority_boundary_v0.json",
    POST_DECISION_DIR / "post_schema_validator_reference_decision_classification_v0.json",
    POST_DECISION_DIR / "post_schema_validator_reference_decision_rollup_v0.json",
    POST_DECISION_DIR / "post_schema_validator_reference_decision_profile_v0.json",
    POST_DECISION_DIR / "post_schema_validator_reference_decision_report.json",
    POST_DECISION_DIR / "post_schema_validator_reference_decision_transition_trace.json",
]

SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0_receipts/732016f0.json"
SCHEMA_VALIDATOR_REF_DIR = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0"
SCHEMA_VALIDATOR_REF_FILES = [
    SCHEMA_VALIDATOR_REF_DIR / "runtime_schema_validator_reviewed_reference_v0.json",
    SCHEMA_VALIDATOR_REF_DIR / "runtime_schema_validator_reviewed_reference_freeze_manifest_v0.json",
    SCHEMA_VALIDATOR_REF_DIR / "runtime_schema_validator_observability_hook_reference_v0.json",
    SCHEMA_VALIDATOR_REF_DIR / "runtime_observability_sidecar_design_prerequisite_v0.json",
    SCHEMA_VALIDATOR_REF_DIR / "runtime_schema_validator_reference_post_closure_decision_ready_v0.json",
]

EDGE_OBS_CLOSURE_RECEIPT_PATH = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0_receipts/ac09c2e3.json"
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
    POST_DECISION_RECEIPT_PATH,
    SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH,
    EDGE_OBS_CLOSURE_RECEIPT_PATH,
] + POST_DECISION_FILES + SCHEMA_VALIDATOR_REF_FILES + EDGE_OBS_FILES

OUT_DIR = ROOT / "data/runtime_observability_sidecar_target_from_schema_validator_and_observability_references_v0"
RECEIPT_DIR = ROOT / "data/runtime_observability_sidecar_target_from_schema_validator_and_observability_references_v0_receipts"

DESIGN_BASIS_PATH = OUT_DIR / "runtime_observability_sidecar_design_basis_v0.json"
SOURCE_DECISION_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_source_decision_review_v0.json"
SOURCE_SCHEMA_VALIDATOR_REFERENCE_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_source_schema_validator_reference_review_v0.json"
SOURCE_EDGE_OBSERVABILITY_REFERENCE_REVIEW_PATH = OUT_DIR / "runtime_observability_sidecar_source_edge_observability_reference_review_v0.json"
TARGET_SPEC_PATH = OUT_DIR / "runtime_observability_sidecar_target_spec_v0.json"
HOOK_REGISTRY_TARGET_PATH = OUT_DIR / "runtime_observability_sidecar_hook_registry_target_v0.json"
EVENT_RECORD_SCHEMA_TARGET_PATH = OUT_DIR / "runtime_observability_sidecar_event_record_schema_target_v0.json"
RECEIPT_SCHEMA_TARGET_PATH = OUT_DIR / "runtime_observability_sidecar_receipt_schema_target_v0.json"
APPEND_ONLY_TRACE_SCHEMA_TARGET_PATH = OUT_DIR / "runtime_observability_sidecar_append_only_trace_schema_target_v0.json"
ROLLUP_READOUT_PROFILE_SCHEMA_TARGET_PATH = OUT_DIR / "runtime_observability_sidecar_rollup_readout_profile_schema_target_v0.json"
UNKNOWN_HOOK_BEHAVIOR_TARGET_PATH = OUT_DIR / "runtime_observability_sidecar_unknown_hook_behavior_target_v0.json"
FORBIDDEN_CONTROL_BEHAVIOR_TARGET_PATH = OUT_DIR / "runtime_observability_sidecar_forbidden_control_behavior_target_v0.json"
NONBLOCKING_FAILURE_BEHAVIOR_TARGET_PATH = OUT_DIR / "runtime_observability_sidecar_nonblocking_failure_behavior_target_v0.json"
LOAD_BEARING_FIELD_MAP_PATH = OUT_DIR / "runtime_observability_sidecar_load_bearing_field_map_v0.json"
OBSERVABILITY_ALIGNMENT_TARGET_PATH = OUT_DIR / "runtime_observability_sidecar_observability_alignment_target_v0.json"
DEMO_CASE_PLAN_PATH = OUT_DIR / "runtime_observability_sidecar_demo_case_plan_v0.json"
ACCEPTANCE_GATES_PATH = OUT_DIR / "runtime_observability_sidecar_acceptance_gates_v0.json"
NEGATIVE_CONTROLS_PATH = OUT_DIR / "runtime_observability_sidecar_negative_controls_v0.json"
BUILD_TARGET_PATH = OUT_DIR / "runtime_observability_sidecar_build_target_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "runtime_observability_sidecar_design_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "runtime_observability_sidecar_design_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_observability_sidecar_design_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_observability_sidecar_design_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_observability_sidecar_design_report.json"
TRACE_PATH = OUT_DIR / "runtime_observability_sidecar_design_transition_trace.json"

EXPECTED_SOURCE_STATUS = "TYPED_POST_SCHEMA_VALIDATOR_REFERENCE_DECISION_SELECTED_OBSERVABILITY_SIDECAR_DESIGN_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_POST_SCHEMA_VALIDATOR_REFERENCE_DECISION_SELECTED_OBSERVABILITY_SIDECAR_DESIGN_READY"
EXPECTED_SELECTED_NEXT = UNIT_ID
EXPECTED_SELECTED_BRANCH = "DESIGN_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_FROM_SCHEMA_VALIDATOR_AND_OBSERVABILITY_REFERENCES"

RECOMMENDED_NEXT = "BUILD_RUNTIME_OBSERVABILITY_SIDECAR_V0"

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

DEMO_CASES = [
    ("known_hook_records_event", "RECORDED"),
    ("schema_validator_result_event_records_edge_fields", "RECORDED"),
    ("validated_candidate_packet_event_records_source_packet", "RECORDED"),
    ("schema_feedback_event_records_blocked_move", "RECORDED"),
    ("unknown_hook_returns_observation_hook_unknown", "OBSERVATION_HOOK_UNKNOWN"),
    ("new_hook_need_returns_observability_hook_gap", "OBSERVABILITY_HOOK_GAP"),
    ("control_attempt_rejected_no_block", "CONTROL_AUTHORITY_FORBIDDEN"),
    ("authorization_claim_rejected_no_block", "AUTHORITY_CLAIM_FORBIDDEN"),
    ("admissibility_claim_rejected_no_block", "ADMISSIBILITY_CLAIM_FORBIDDEN"),
    ("execution_claim_rejected_no_block", "EXECUTION_CLAIM_FORBIDDEN"),
    ("repair_claim_rejected_no_block", "REPAIR_CLAIM_FORBIDDEN"),
    ("unbounded_payload_rejected", "UNBOUNDED_PAYLOAD_FORBIDDEN"),
    ("source_mutation_attempt_rejected", "SOURCE_MUTATION_FORBIDDEN"),
    ("runtime_patch_attempt_rejected", "RUNTIME_PATCH_FORBIDDEN"),
    ("live_hook_install_attempt_rejected", "LIVE_HOOK_INSTALL_FORBIDDEN"),
    ("c8_authorization_attempt_rejected", "C8_AUTHORIZATION_FORBIDDEN"),
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

    post_decision_receipt = read_json(POST_DECISION_RECEIPT_PATH)
    post_decision_summary = post_decision_receipt.get("machine_readable_post_schema_validator_reference_decision_summary", {})
    selected_branch = read_json(POST_DECISION_DIR / "post_schema_validator_reference_selected_branch_v0.json")
    source_sidecar_target = read_json(POST_DECISION_DIR / "runtime_observability_sidecar_design_target_from_schema_validator_and_observability_references_v0.json")
    input_reference_set = read_json(POST_DECISION_DIR / "runtime_observability_sidecar_input_reference_set_v0.json")
    pre_c8_plan = read_json(POST_DECISION_DIR / "post_schema_validator_pre_c8_interlock_plan_v0.json")
    authority = read_json(POST_DECISION_DIR / "post_schema_validator_reference_decision_authority_boundary_v0.json")
    classification = read_json(POST_DECISION_DIR / "post_schema_validator_reference_decision_classification_v0.json")
    rollup = read_json(POST_DECISION_DIR / "post_schema_validator_reference_decision_rollup_v0.json")
    profile = read_json(POST_DECISION_DIR / "post_schema_validator_reference_decision_profile_v0.json")

    schema_validator_closure_receipt = read_json(SCHEMA_VALIDATOR_CLOSURE_RECEIPT_PATH)
    schema_validator_reference = read_json(SCHEMA_VALIDATOR_REF_DIR / "runtime_schema_validator_reviewed_reference_v0.json")
    schema_validator_freeze = read_json(SCHEMA_VALIDATOR_REF_DIR / "runtime_schema_validator_reviewed_reference_freeze_manifest_v0.json")
    schema_validator_hooks = read_json(SCHEMA_VALIDATOR_REF_DIR / "runtime_schema_validator_observability_hook_reference_v0.json")
    schema_validator_prereq = read_json(SCHEMA_VALIDATOR_REF_DIR / "runtime_observability_sidecar_design_prerequisite_v0.json")

    edge_obs_closure_receipt = read_json(EDGE_OBS_CLOSURE_RECEIPT_PATH)
    edge_obs_reference = read_json(EDGE_OBS_REF_DIR / "decision_edge_observability_reviewed_reference_v0.json")
    edge_obs_freeze = read_json(EDGE_OBS_REF_DIR / "decision_edge_observability_reviewed_reference_freeze_manifest_v0.json")
    edge_obs_requirement = read_json(EDGE_OBS_REF_DIR / "decision_edge_observability_requirement_reference_v0.json")
    edge_obs_field_schema = read_json(EDGE_OBS_REF_DIR / "decision_edge_observability_field_schema_reference_v0.json")
    edge_obs_distinction = read_json(EDGE_OBS_REF_DIR / "decision_edge_observability_distinction_guard_reference_v0.json")
    edge_obs_negative = read_json(EDGE_OBS_REF_DIR / "decision_edge_observability_negative_control_reference_v0.json")

    if post_decision_receipt.get("receipt_id") != SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID or post_decision_receipt.get("gate") != "PASS":
        failures.append("post_schema_validator_decision_receipt_not_pass")
    if post_decision_receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("post_schema_validator_decision_stop_wrong")
    if post_decision_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("post_schema_validator_decision_hidden_next")
    if post_decision_summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"post_schema_validator_decision_status_wrong:{post_decision_summary.get('status')}")
    if post_decision_summary.get("selected_next_unit") != EXPECTED_SELECTED_NEXT:
        failures.append(f"post_schema_validator_selected_next_wrong:{post_decision_summary.get('selected_next_unit')}")
    if post_decision_summary.get("selected_branch") != EXPECTED_SELECTED_BRANCH:
        failures.append(f"post_schema_validator_selected_branch_wrong:{post_decision_summary.get('selected_branch')}")

    for key in [
        "post_schema_validator_reference_decision_complete",
        "observability_sidecar_design_selected",
        "observability_sidecar_design_ready",
        "schema_validator_reference_consumed",
        "edge_observability_reference_consumed",
        "sidecar_input_reference_set_ready",
        "pre_c8_interlock_second_object_selected",
        "schema_validator_reference_parked",
        "unit_feedback_hardening_deferred",
        "c7_deferred",
        "c8_deferred",
        "runtime_adoption_deferred",
        "bad_counters_zero",
    ]:
        if post_decision_summary.get(key) is not True:
            failures.append(f"decision_required_true_missing:{key}")

    for key in [
        "observability_sidecar_built",
        "observability_sidecar_live",
        "live_runtime_hooks_installed",
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
        if post_decision_summary.get(key) is not False:
            failures.append(f"decision_forbidden_true:{key}")

    for key, expected in {
        "schema_validator_observable_event_count": 8,
        "sidecar_initial_hook_count": 24,
        "load_bearing_edge_field_count": 7,
    }.items():
        if post_decision_summary.get(key) != expected:
            failures.append(f"decision_count_wrong:{key}:{post_decision_summary.get(key)}")

    if selected_branch.get("selected_next_unit") != EXPECTED_SELECTED_NEXT:
        failures.append("selected_branch_next_wrong")
    if source_sidecar_target.get("target_status") != "DESIGN_READY":
        failures.append("source_sidecar_target_not_design_ready")
    if source_sidecar_target.get("must_not_build_yet") is not True:
        failures.append("source_sidecar_target_missing_must_not_build")
    if source_sidecar_target.get("must_not_install_live_runtime_hooks_yet") is not True:
        failures.append("source_sidecar_target_missing_no_live_hooks")
    if input_reference_set.get("reference_set_status") != "READY_FOR_SIDECAR_TARGET_DESIGN":
        failures.append("input_reference_set_not_ready")
    if pre_c8_plan.get("nothing_else_before_c8") is not True:
        failures.append("pre_c8_plan_wrong")
    if authority.get("may_design_observability_sidecar_target_next") is not True:
        failures.append("authority_does_not_allow_design_next")
    if classification.get("next_command_goal") is not None:
        failures.append("classification_hidden_next")
    if rollup.get("sidecar_initial_hook_count") != 24:
        failures.append("rollup_hook_count_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")

    if schema_validator_closure_receipt.get("receipt_id") != SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID or schema_validator_closure_receipt.get("gate") != "PASS":
        failures.append("schema_validator_closure_not_pass")
    if schema_validator_reference.get("reference_status") != "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_FROZEN":
        failures.append("schema_validator_reference_not_frozen")
    if schema_validator_freeze.get("freeze_status") != "FROZEN":
        failures.append("schema_validator_freeze_not_frozen")
    if schema_validator_hooks.get("schema_validator_surface_observable_events") != SCHEMA_VALIDATOR_OBSERVABLE_EVENTS:
        failures.append("schema_validator_hooks_wrong")
    if schema_validator_prereq.get("prerequisite_status") != "SATISFIED":
        failures.append("schema_validator_sidecar_prereq_not_satisfied")

    if edge_obs_closure_receipt.get("receipt_id") != SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID or edge_obs_closure_receipt.get("gate") != "PASS":
        failures.append("edge_observability_closure_not_pass")
    if edge_obs_reference.get("reference_status") != "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_FROZEN":
        failures.append("edge_observability_reference_not_frozen")
    if edge_obs_freeze.get("freeze_status") != "FROZEN":
        failures.append("edge_observability_freeze_not_frozen")
    if edge_obs_requirement.get("required_fields") != REQUIRED_EDGE_FIELDS:
        failures.append("edge_observability_required_fields_wrong")
    if edge_obs_requirement.get("edge_requirement_count") != 7:
        failures.append("edge_observability_requirement_count_wrong")
    if edge_obs_field_schema.get("required_field_count") != 7:
        failures.append("edge_observability_field_count_wrong")
    if edge_obs_distinction.get("guard_count") != 8:
        failures.append("edge_observability_guard_count_wrong")
    if edge_obs_negative.get("negative_control_count") != 13:
        failures.append("edge_observability_negative_count_wrong")

    return failures, {
        "post_decision_summary": post_decision_summary,
        "source_sidecar_target": source_sidecar_target,
        "input_reference_set": input_reference_set,
        "schema_validator_reference": schema_validator_reference,
        "schema_validator_hooks": schema_validator_hooks,
        "schema_validator_prereq": schema_validator_prereq,
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

    design_pass = not failures
    status = "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_DESIGNED_BUILD_READY" if design_pass else "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_DESIGN_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if design_pass else "REPAIR_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_DESIGN_V0"

    post_decision_summary = basis.get("post_decision_summary", {})
    source_sidecar_target = basis.get("source_sidecar_target", {})
    input_reference_set = basis.get("input_reference_set", {})
    schema_validator_reference = basis.get("schema_validator_reference", {})
    schema_validator_hooks = basis.get("schema_validator_hooks", {})
    edge_obs_requirement = basis.get("edge_obs_requirement", {})
    edge_obs_field_schema = basis.get("edge_obs_field_schema", {})
    edge_obs_distinction = basis.get("edge_obs_distinction", {})
    edge_obs_negative = basis.get("edge_obs_negative", {})

    reason_codes = [
        "RUNTIME_OBSERVABILITY_SIDECAR_TARGET_DESIGNED",
        "POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_CONSUMED",
        "SCHEMA_VALIDATOR_REVIEWED_REFERENCE_CONSUMED",
        "DECISION_EDGE_OBSERVABILITY_REFERENCE_CONSUMED",
        "SIDECAR_DESIGN_TARGET_CONSUMED",
        "SIDECAR_INPUT_REFERENCE_SET_CONSUMED",
        "HOOK_REGISTRY_TARGET_DEFINED",
        "EVENT_RECORD_SCHEMA_TARGET_DEFINED",
        "SIDECAR_RECEIPT_SCHEMA_TARGET_DEFINED",
        "APPEND_ONLY_TRACE_SCHEMA_TARGET_DEFINED",
        "ROLLUP_READOUT_PROFILE_SCHEMA_TARGET_DEFINED",
        "UNKNOWN_HOOK_BEHAVIOR_DEFINED",
        "FORBIDDEN_CONTROL_BEHAVIOR_DEFINED",
        "NONBLOCKING_FAILURE_BEHAVIOR_DEFINED",
        "LOAD_BEARING_FIELD_MAP_DEFINED",
        "OBSERVABILITY_ALIGNMENT_DEFINED",
        "DEMO_CASE_PLAN_DEFINED",
        "ACCEPTANCE_GATES_DEFINED",
        "NEGATIVE_CONTROLS_DEFINED",
        "BUILD_TARGET_DEFINED",
        "CONTROL_PATH_ACTS_SIDECAR_RECORDS",
        "SIDECAR_HAS_EYES_NOT_HANDS",
        "NO_SIDECAR_BUILD",
        "NO_LIVE_HOOK_INSTALL",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_RUNTIME_ROUTING",
        "NO_AUTHORITY_CHECK",
        "NO_ADMISSIBILITY_CHECK",
        "NO_EXECUTION_CLAIM",
        "NO_SCHEMA_ARCHIVE_MUTATION",
        "NO_PROPOSAL_REPAIR",
        "NO_SCHEMA_CREATION",
        "NO_BUILDER_COMMAND",
        "NO_C7_AUTHORIZATION",
        "NO_C8_AUTHORIZATION",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if design_pass else failures

    design_basis = {
        "schema_version": "runtime_observability_sidecar_design_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if design_pass else "BASIS_REPAIR_REQUIRED",
        "source_post_schema_validator_decision_receipt_id": SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID,
        "source_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID,
        "decision_status": post_decision_summary.get("status"),
        "design_scope": "design target for Runtime Observability Sidecar from frozen Schema Validator and decision-edge observability references",
    }

    source_decision_review = {
        "schema_version": "runtime_observability_sidecar_source_decision_review_v0",
        "source_decision_receipt_id": SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID,
        "source_decision_status": post_decision_summary.get("status"),
        "selected_next_unit": post_decision_summary.get("selected_next_unit"),
        "sidecar_design_selected": post_decision_summary.get("observability_sidecar_design_selected"),
        "sidecar_design_ready": post_decision_summary.get("observability_sidecar_design_ready"),
        "source_declared_hook_count": post_decision_summary.get("sidecar_initial_hook_count"),
        "next_command_goal": None,
    }

    schema_validator_reference_review = {
        "schema_version": "runtime_observability_sidecar_source_schema_validator_reference_review_v0",
        "source_reference_receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "reference_status": schema_validator_reference.get("reference_status"),
        "observable_event_count": len(schema_validator_hooks.get("schema_validator_surface_observable_events", [])),
        "observable_events": schema_validator_hooks.get("schema_validator_surface_observable_events"),
        "valid_advances_only_to": schema_validator_reference.get("valid_advances_only_to"),
        "invalid_returns_to": schema_validator_reference.get("invalid_returns_to"),
        "sidecar_design_prerequisite_consumed": True,
    }

    edge_observability_reference_review = {
        "schema_version": "runtime_observability_sidecar_source_edge_observability_reference_review_v0",
        "source_reference_receipt_id": SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID,
        "reference_status": "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_FROZEN",
        "edge_requirement_count": edge_obs_requirement.get("edge_requirement_count"),
        "required_fields": edge_obs_requirement.get("required_fields"),
        "field_schema_count": edge_obs_field_schema.get("required_field_count"),
        "distinction_guard_count": edge_obs_distinction.get("guard_count"),
        "negative_control_count": edge_obs_negative.get("negative_control_count"),
    }

    target_spec = {
        "schema_version": "runtime_observability_sidecar_target_spec_v0",
        "target_status": "DESIGNED_BUILD_READY" if design_pass else "NOT_READY",
        "future_build_unit": RECOMMENDED_NEXT if design_pass else None,
        "unit_id": "BUILD_RUNTIME_OBSERVABILITY_SIDECAR_V0",
        "target_unit_id": "runtime.observability_sidecar.v0",
        "layer": "RUNTIME / OBSERVATION",
        "mode": "OBSERVE / EMIT_RECEIPT / APPEND_ONLY",
        "core_compression": "Control path acts. Sidecar records.",
        "authority_law": "The sidecar has eyes, not hands.",
        "role": "observe predefined runtime event hooks and emit load-bearing append-only evidence records",
        "input_reference_set": input_reference_set,
        "allowed_inputs": [
            "predefined event hook id",
            "event payload matching hook schema",
            "source packet reference",
            "runtime cell id",
            "attempted move descriptor",
            "boundary check descriptor",
            "timestamp",
        ],
        "allowed_outputs": [
            "sidecar event record",
            "append-only trace entry",
            "sidecar receipt",
            "sidecar rollup",
            "sidecar readout",
            "sidecar profile",
            "sidecar report",
        ],
        "forbidden_outputs": [
            "validation verdict",
            "admissibility verdict",
            "authorization verdict",
            "execution command",
            "proposal repair",
            "schema mutation",
            "runtime patch",
            "live hook installation",
            "builder command",
            "C8 authorization",
        ],
        "must_not_build_yet": True,
        "must_not_install_live_runtime_hooks_yet": True,
    }

    hook_registry_target = {
        "schema_version": "runtime_observability_sidecar_hook_registry_target_v0",
        "registry_status": "DESIGNED",
        "hook_count": len(SIDECAR_INITIAL_HOOKS),
        "hooks": [
            {
                "hook_id": hook,
                "status": "REGISTERED_TARGET",
                "load_bearing": True,
                "control_authority": False,
            }
            for hook in SIDECAR_INITIAL_HOOKS
        ],
        "unknown_hook_result": "OBSERVATION_HOOK_UNKNOWN",
        "new_hook_need_result": "OBSERVABILITY_HOOK_GAP",
        "registration_rule": "No dynamic hook registration during observation.",
    }

    event_record_schema_target = {
        "schema_version": "runtime_observability_sidecar_event_record_schema_target_v0",
        "target_schema_name": "runtime_observability_sidecar_event_record_schema_v0.json",
        "required_fields": [
            "schema_version",
            "event_id",
            "sidecar_id",
            "hook_id",
            "hook_known",
            "event_status",
            "active_object",
            "attempted_move",
            "boundary_checked",
            "boundary_result",
            "blocked_moves",
            "lawful_next_moves",
            "source_packet_ref",
            "source_cell",
            "target_cell",
            "observed_at",
            "payload_digest",
            "payload_excerpt",
            "forbidden_claims_detected",
            "terminal",
        ],
        "required_load_bearing_edge_fields": REQUIRED_EDGE_FIELDS,
        "payload_rule": "Store bounded payload excerpt plus digest, not unbounded payload.",
    }

    receipt_schema_target = {
        "schema_version": "runtime_observability_sidecar_receipt_schema_target_v0",
        "target_schema_name": "runtime_observability_sidecar_receipt_schema_v0.json",
        "required_fields": [
            "schema_version",
            "receipt_id",
            "unit_id",
            "sidecar_id",
            "gate",
            "events_observed",
            "events_recorded",
            "unknown_hooks",
            "hook_gaps",
            "forbidden_control_claims",
            "negative_controls",
            "output_artifacts",
            "terminal",
        ],
        "required_zero_counters": [
            "validation_verdict_count",
            "admissibility_verdict_count",
            "authorization_verdict_count",
            "execution_command_count",
            "proposal_repair_count",
            "schema_mutation_count",
            "runtime_patch_count",
            "live_hook_install_count",
            "blocking_action_count",
            "builder_command_count",
            "c8_authorization_count",
        ],
    }

    append_only_trace_schema_target = {
        "schema_version": "runtime_observability_sidecar_append_only_trace_schema_target_v0",
        "target_schema_name": "runtime_observability_sidecar_append_only_trace_schema_v0.json",
        "append_only": True,
        "required_entry_fields": [
            "trace_index",
            "event_id",
            "hook_id",
            "source_packet_ref",
            "active_object",
            "attempted_move",
            "boundary_checked",
            "boundary_result",
            "event_status",
            "previous_entry_digest",
            "entry_digest",
        ],
        "mutation_rule": "Existing trace entries are not edited by the sidecar.",
    }

    rollup_schema_target = {
        "schema_version": "runtime_observability_sidecar_rollup_readout_profile_schema_target_v0",
        "must_emit": [
            "hook_counts",
            "event_status_counts",
            "unknown_hook_count",
            "hook_gap_count",
            "forbidden_control_claim_count",
            "load_bearing_field_presence_count",
            "negative_controls",
            "profile_status",
        ],
    }

    unknown_hook_behavior = {
        "schema_version": "runtime_observability_sidecar_unknown_hook_behavior_target_v0",
        "unknown_hook_result": "OBSERVATION_HOOK_UNKNOWN",
        "new_hook_need_result": "OBSERVABILITY_HOOK_GAP",
        "unknown_hook_behavior": "record typed observation failure and continue; do not register hook dynamically",
        "hook_gap_behavior": "emit gap feedback for later design review; do not patch runtime",
    }

    forbidden_control_behavior = {
        "schema_version": "runtime_observability_sidecar_forbidden_control_behavior_target_v0",
        "forbidden_claims": [
            "VALIDATION_VERDICT",
            "ADMISSIBILITY_VERDICT",
            "AUTHORIZATION_VERDICT",
            "EXECUTION_COMMAND",
            "PROPOSAL_REPAIR",
            "SCHEMA_MUTATION",
            "RUNTIME_PATCH",
            "LIVE_HOOK_INSTALL",
            "BLOCKING_ACTION",
            "BUILDER_COMMAND",
            "C8_AUTHORIZATION",
        ],
        "behavior": "record forbidden claim as evidence; do not perform it",
        "sidecar_control_authority": False,
    }

    nonblocking_failure_behavior = {
        "schema_version": "runtime_observability_sidecar_nonblocking_failure_behavior_target_v0",
        "rule": "Observation failure must not block, advance, authorize, execute, or repair the control path.",
        "failure_results": [
            "OBSERVATION_HOOK_UNKNOWN",
            "OBSERVABILITY_HOOK_GAP",
            "EVENT_PAYLOAD_INVALID",
            "UNBOUNDED_PAYLOAD_FORBIDDEN",
            "FORBIDDEN_CONTROL_CLAIM",
            "TRACE_APPEND_FAILED",
        ],
        "allowed_next": [
            "emit sidecar failure receipt",
            "emit rollup/readout",
            "return to caller without control-path effect",
        ],
    }

    load_bearing_field_map = {
        "schema_version": "runtime_observability_sidecar_load_bearing_field_map_v0",
        "required_edge_fields": REQUIRED_EDGE_FIELDS,
        "field_map": {
            "active_object": "object or packet being acted on",
            "attempted_move": "move the control path attempted",
            "boundary_checked": "boundary or guard observed",
            "boundary_result": "observed outcome of boundary check",
            "blocked_moves": "moves made unavailable by observed boundary",
            "lawful_next_moves": "next moves exposed by the control path or typed stop",
            "source_packet_ref": "explicit packet or receipt reference",
        },
        "why": "These fields allow decision-edge reconstruction without logging everything.",
    }

    observability_alignment = {
        "schema_version": "runtime_observability_sidecar_observability_alignment_target_v0",
        "alignment_status": "DESIGNED",
        "decision_edge_reference_required_fields": REQUIRED_EDGE_FIELDS,
        "schema_validator_observable_events": SCHEMA_VALIDATOR_OBSERVABLE_EVENTS,
        "sidecar_initial_hook_set": SIDECAR_INITIAL_HOOKS,
        "distinction": {
            "control_path": "acts",
            "sidecar": "records",
            "schema_validator": "validates proposal formation only",
            "lawful_admissibility": "checks permission only",
        },
    }

    demo_case_plan = {
        "schema_version": "runtime_observability_sidecar_demo_case_plan_v0",
        "demo_case_count": len(DEMO_CASES),
        "cases": [
            {
                "case_id": f"sidecar_demo_{i:02d}_{name}",
                "case_name": name,
                "expected_result": expected,
            }
            for i, (name, expected) in enumerate(DEMO_CASES)
        ],
    }

    acceptance_gates = {
        "schema_version": "runtime_observability_sidecar_acceptance_gates_v0",
        "gate_count": 30,
        "gates": [
            "SIDECAR_0_SOURCE_DECISION_CONSUMED",
            "SIDECAR_1_SCHEMA_VALIDATOR_REFERENCE_CONSUMED",
            "SIDECAR_2_EDGE_OBSERVABILITY_REFERENCE_CONSUMED",
            "SIDECAR_3_TARGET_SPEC_EMITTED",
            "SIDECAR_4_HOOK_REGISTRY_TARGET_EMITTED",
            "SIDECAR_5_EVENT_RECORD_SCHEMA_TARGET_EMITTED",
            "SIDECAR_6_RECEIPT_SCHEMA_TARGET_EMITTED",
            "SIDECAR_7_APPEND_ONLY_TRACE_SCHEMA_TARGET_EMITTED",
            "SIDECAR_8_ROLLUP_READOUT_PROFILE_SCHEMA_TARGET_EMITTED",
            "SIDECAR_9_UNKNOWN_HOOK_BEHAVIOR_EMITTED",
            "SIDECAR_10_FORBIDDEN_CONTROL_BEHAVIOR_EMITTED",
            "SIDECAR_11_NONBLOCKING_FAILURE_BEHAVIOR_EMITTED",
            "SIDECAR_12_LOAD_BEARING_FIELD_MAP_EMITTED",
            "SIDECAR_13_OBSERVABILITY_ALIGNMENT_EMITTED",
            "SIDECAR_14_DEMO_CASE_PLAN_EMITTED",
            "SIDECAR_15_ACCEPTANCE_GATES_EMITTED",
            "SIDECAR_16_NEGATIVE_CONTROLS_EMITTED",
            "SIDECAR_17_BUILD_TARGET_EMITTED",
            "SIDECAR_18_NO_SIDECAR_BUILD",
            "SIDECAR_19_NO_LIVE_HOOK_INSTALL",
            "SIDECAR_20_NO_RUNTIME_EFFECT_OR_PATCH",
            "SIDECAR_21_NO_LIVE_RUNTIME_ROUTING",
            "SIDECAR_22_NO_VALIDATION_ADMISSIBILITY_AUTHORITY_OR_EXECUTION",
            "SIDECAR_23_NO_SCHEMA_MUTATION_OR_REPAIR",
            "SIDECAR_24_NO_BUILDER_COMMAND",
            "SIDECAR_25_NO_C7_OR_C8",
            "SIDECAR_26_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT",
            "SIDECAR_27_NO_SOURCE_OR_REFERENCE_MUTATION",
            "SIDECAR_28_BAD_COUNTERS_ZERO",
            "SIDECAR_29_NO_HIDDEN_NEXT_COMMAND",
        ],
    }

    negative_controls = {
        "schema_version": "runtime_observability_sidecar_negative_controls_v0",
        "negative_control_count": 20,
        "controls": [
            "validation_verdict_emitted_fail",
            "admissibility_verdict_emitted_fail",
            "authorization_verdict_emitted_fail",
            "execution_command_emitted_fail",
            "proposal_repair_emitted_fail",
            "schema_mutation_emitted_fail",
            "runtime_patch_emitted_fail",
            "live_hook_install_emitted_fail",
            "control_path_blocked_by_sidecar_fail",
            "control_path_advanced_by_sidecar_fail",
            "builder_command_emitted_fail",
            "c8_authorization_emitted_fail",
            "unknown_hook_registered_dynamically_fail",
            "unbounded_payload_logged_fail",
            "source_mutated_fail",
            "prior_receipt_mutated_fail",
            "schema_validator_reference_mutated_fail",
            "observability_reference_mutated_fail",
            "latest_or_mtime_selection_fail",
            "hidden_next_command_fail",
        ],
    }

    build_target = {
        "schema_version": "runtime_observability_sidecar_build_target_v0",
        "build_target_status": "BUILD_READY" if design_pass else "NOT_READY",
        "recommended_next": recommended_next,
        "build_unit": "BUILD_RUNTIME_OBSERVABILITY_SIDECAR_V0",
        "build_meaning": "Build a synthetic/reference Runtime Observability Sidecar surface. Do not install live hooks or patch runtime.",
        "must_emit": [
            "hook registry",
            "event record schema",
            "sidecar receipt schema",
            "append-only trace schema",
            "demo event inputs",
            "event records",
            "append-only trace",
            "unknown hook demo",
            "hook gap demo",
            "forbidden control claim demos",
            "rollup",
            "readout",
            "profile",
            "report",
            "transition trace",
            "receipt",
        ],
    }

    authority_boundary = {
        "schema_version": "runtime_observability_sidecar_design_authority_boundary_v0",
        "status": status,
        "may_build_observability_sidecar_next": design_pass,
        "may_install_live_runtime_hooks": False,
        "may_install_live_runtime_routing": False,
        "may_patch_runtime_now": False,
        "may_validate": False,
        "may_check_authority": False,
        "may_check_admissibility": False,
        "may_execute": False,
        "may_repair_proposal": False,
        "may_mutate_schema_archive": False,
        "may_create_schema": False,
        "may_emit_builder_command": False,
        "may_block_control_path": False,
        "may_advance_control_path": False,
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
        "schema_version": "runtime_observability_sidecar_design_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "runtime_observability_sidecar_target_designed": design_pass,
        "observability_sidecar_build_ready": design_pass,
        "source_decision_consumed": True,
        "schema_validator_reference_consumed": True,
        "edge_observability_reference_consumed": True,
        "hook_registry_target_defined": design_pass,
        "event_record_schema_target_defined": design_pass,
        "receipt_schema_target_defined": design_pass,
        "append_only_trace_schema_target_defined": design_pass,
        "rollup_readout_profile_schema_target_defined": design_pass,
        "unknown_hook_behavior_defined": design_pass,
        "forbidden_control_behavior_defined": design_pass,
        "nonblocking_failure_behavior_defined": design_pass,
        "load_bearing_field_map_defined": design_pass,
        "observability_alignment_defined": design_pass,
        "demo_case_plan_defined": design_pass,
        "acceptance_gates_defined": design_pass,
        "negative_controls_defined": design_pass,
        "hook_count": len(SIDECAR_INITIAL_HOOKS),
        "schema_validator_observable_event_count": len(SCHEMA_VALIDATOR_OBSERVABLE_EVENTS),
        "load_bearing_edge_field_count": len(REQUIRED_EDGE_FIELDS),
        "demo_case_count": len(DEMO_CASES),
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
        "validation_verdict_emitted": False,
        "authority_checked": False,
        "admissibility_checked": False,
        "execution_claimed": False,
        "schema_archive_mutated": False,
        "proposal_repaired": False,
        "schema_created": False,
        "builder_command_emitted": False,
        "control_path_blocked": False,
        "control_path_advanced": False,
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
        "bad_counters_zero": design_pass,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "runtime_observability_sidecar_design_rollup_v0",
        "design_count": 1 if design_pass else 0,
        "target_designed_count": 1 if design_pass else 0,
        "build_ready_count": 1 if design_pass else 0,
        "hook_count": len(SIDECAR_INITIAL_HOOKS),
        "schema_validator_observable_event_count": len(SCHEMA_VALIDATOR_OBSERVABLE_EVENTS),
        "load_bearing_edge_field_count": len(REQUIRED_EDGE_FIELDS),
        "demo_case_count": len(DEMO_CASES),
        "acceptance_gate_count": acceptance_gates["gate_count"],
        "negative_control_count": negative_controls["negative_control_count"],
        "observability_sidecar_build_count": 0,
        "live_runtime_hooks_installed_count": 0,
        "live_runtime_routing_installed_count": 0,
        "runtime_patch_count": 0,
        "validation_verdict_count": 0,
        "authority_checked_count": 0,
        "admissibility_checked_count": 0,
        "execution_claim_count": 0,
        "schema_archive_mutation_count": 0,
        "proposal_repair_count": 0,
        "schema_created_count": 0,
        "builder_command_emitted_count": 0,
        "control_path_blocked_count": 0,
        "control_path_advanced_count": 0,
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
        "schema_version": "runtime_observability_sidecar_design_profile_v0",
        "profile_id": "runtime_observability_sidecar_design_" + sig8(rollup),
        "status": status,
        "target": "Runtime Observability Sidecar",
        "design_result": "BUILD_READY" if design_pass else "REPAIR_REQUIRED",
        "core_compression": "Control path acts. Sidecar records.",
        "authority_law": "The sidecar has eyes, not hands.",
        "hook_count": len(SIDECAR_INITIAL_HOOKS),
        "build_unit": recommended_next,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "c8_authorized": False,
        "must_not_infer": [
            "Sidecar was built",
            "Live hooks were installed",
            "Runtime routing was patched",
            "Sidecar can validate",
            "Sidecar can authorize",
            "Sidecar can block",
            "Sidecar can execute",
            "C8 is authorized",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "runtime_observability_sidecar_design_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The Runtime Observability Sidecar target has been designed from the frozen Schema Validator reference and frozen decision-edge observability reference. The design defines hook registry, event record schema, sidecar receipt schema, append-only trace schema, rollup/readout/profile surface, unknown-hook behavior, forbidden-control behavior, nonblocking failure behavior, load-bearing field map, observability alignment, demo plan, gates, controls, and build target. It does not build the Sidecar, install live hooks, patch runtime, route traffic, validate, authorize, admit, execute, repair, mutate schemas, emit builder commands, open C8, or claim broader authority.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "runtime_observability_sidecar_design_transition_trace_v0",
        "trace": [
            {
                "step": "consume_post_schema_validator_decision",
                "question": "was Sidecar target design selected",
                "answer": "yes" if design_pass else "no",
                "taken": "consume selected target and input reference set",
            },
            {
                "step": "consume_references",
                "question": "are Schema Validator and decision-edge observability references frozen",
                "answer": "yes" if design_pass else "no",
                "taken": "define Sidecar target from both references",
            },
            {
                "step": "design_sidecar_target",
                "question": "what is the sidecar allowed to do",
                "answer": "observe and emit append-only receipts only",
                "taken": "emit design target and stop build-ready",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (DESIGN_BASIS_PATH, design_basis),
        (SOURCE_DECISION_REVIEW_PATH, source_decision_review),
        (SOURCE_SCHEMA_VALIDATOR_REFERENCE_REVIEW_PATH, schema_validator_reference_review),
        (SOURCE_EDGE_OBSERVABILITY_REFERENCE_REVIEW_PATH, edge_observability_reference_review),
        (TARGET_SPEC_PATH, target_spec),
        (HOOK_REGISTRY_TARGET_PATH, hook_registry_target),
        (EVENT_RECORD_SCHEMA_TARGET_PATH, event_record_schema_target),
        (RECEIPT_SCHEMA_TARGET_PATH, receipt_schema_target),
        (APPEND_ONLY_TRACE_SCHEMA_TARGET_PATH, append_only_trace_schema_target),
        (ROLLUP_READOUT_PROFILE_SCHEMA_TARGET_PATH, rollup_schema_target),
        (UNKNOWN_HOOK_BEHAVIOR_TARGET_PATH, unknown_hook_behavior),
        (FORBIDDEN_CONTROL_BEHAVIOR_TARGET_PATH, forbidden_control_behavior),
        (NONBLOCKING_FAILURE_BEHAVIOR_TARGET_PATH, nonblocking_failure_behavior),
        (LOAD_BEARING_FIELD_MAP_PATH, load_bearing_field_map),
        (OBSERVABILITY_ALIGNMENT_TARGET_PATH, observability_alignment),
        (DEMO_CASE_PLAN_PATH, demo_case_plan),
        (ACCEPTANCE_GATES_PATH, acceptance_gates),
        (NEGATIVE_CONTROLS_PATH, negative_controls),
        (BUILD_TARGET_PATH, build_target),
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
        "SIDECAR_DESIGN_0_SOURCE_DECISION_CONSUMED": POST_DECISION_RECEIPT_PATH.exists(),
        "SIDECAR_DESIGN_1_SCHEMA_VALIDATOR_REFERENCE_CONSUMED": schema_validator_reference_review["reference_status"] == "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_FROZEN",
        "SIDECAR_DESIGN_2_EDGE_OBSERVABILITY_REFERENCE_CONSUMED": edge_observability_reference_review["reference_status"] == "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_FROZEN",
        "SIDECAR_DESIGN_3_TARGET_SPEC_EMITTED": TARGET_SPEC_PATH.exists() and target_spec["target_status"] == "DESIGNED_BUILD_READY",
        "SIDECAR_DESIGN_4_HOOK_REGISTRY_TARGET_EMITTED": HOOK_REGISTRY_TARGET_PATH.exists() and hook_registry_target["hook_count"] == 24,
        "SIDECAR_DESIGN_5_EVENT_RECORD_SCHEMA_TARGET_EMITTED": EVENT_RECORD_SCHEMA_TARGET_PATH.exists(),
        "SIDECAR_DESIGN_6_RECEIPT_SCHEMA_TARGET_EMITTED": RECEIPT_SCHEMA_TARGET_PATH.exists(),
        "SIDECAR_DESIGN_7_APPEND_ONLY_TRACE_SCHEMA_TARGET_EMITTED": APPEND_ONLY_TRACE_SCHEMA_TARGET_PATH.exists() and append_only_trace_schema_target["append_only"] is True,
        "SIDECAR_DESIGN_8_ROLLUP_READOUT_PROFILE_SCHEMA_TARGET_EMITTED": ROLLUP_READOUT_PROFILE_SCHEMA_TARGET_PATH.exists(),
        "SIDECAR_DESIGN_9_UNKNOWN_HOOK_BEHAVIOR_EMITTED": UNKNOWN_HOOK_BEHAVIOR_TARGET_PATH.exists(),
        "SIDECAR_DESIGN_10_FORBIDDEN_CONTROL_BEHAVIOR_EMITTED": FORBIDDEN_CONTROL_BEHAVIOR_TARGET_PATH.exists() and forbidden_control_behavior["sidecar_control_authority"] is False,
        "SIDECAR_DESIGN_11_NONBLOCKING_FAILURE_BEHAVIOR_EMITTED": NONBLOCKING_FAILURE_BEHAVIOR_TARGET_PATH.exists(),
        "SIDECAR_DESIGN_12_LOAD_BEARING_FIELD_MAP_EMITTED": LOAD_BEARING_FIELD_MAP_PATH.exists() and load_bearing_field_map["required_edge_fields"] == REQUIRED_EDGE_FIELDS,
        "SIDECAR_DESIGN_13_OBSERVABILITY_ALIGNMENT_EMITTED": OBSERVABILITY_ALIGNMENT_TARGET_PATH.exists(),
        "SIDECAR_DESIGN_14_DEMO_CASE_PLAN_EMITTED": DEMO_CASE_PLAN_PATH.exists() and demo_case_plan["demo_case_count"] == 16,
        "SIDECAR_DESIGN_15_ACCEPTANCE_GATES_EMITTED": ACCEPTANCE_GATES_PATH.exists() and acceptance_gates["gate_count"] == 30,
        "SIDECAR_DESIGN_16_NEGATIVE_CONTROLS_EMITTED": NEGATIVE_CONTROLS_PATH.exists() and negative_controls["negative_control_count"] == 20,
        "SIDECAR_DESIGN_17_BUILD_TARGET_EMITTED": BUILD_TARGET_PATH.exists() and build_target["build_target_status"] == "BUILD_READY",
        "SIDECAR_DESIGN_18_NO_SIDECAR_BUILD": classification["observability_sidecar_built"] is False,
        "SIDECAR_DESIGN_19_NO_LIVE_HOOK_INSTALL": classification["live_runtime_hooks_installed"] is False,
        "SIDECAR_DESIGN_20_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "SIDECAR_DESIGN_21_NO_LIVE_RUNTIME_ROUTING": classification["live_runtime_routing_installed"] is False,
        "SIDECAR_DESIGN_22_NO_VALIDATION_ADMISSIBILITY_AUTHORITY_OR_EXECUTION": classification["validation_verdict_emitted"] is False and classification["authority_checked"] is False and classification["admissibility_checked"] is False and classification["execution_claimed"] is False,
        "SIDECAR_DESIGN_23_NO_SCHEMA_MUTATION_OR_REPAIR": classification["schema_archive_mutated"] is False and classification["proposal_repaired"] is False and classification["schema_created"] is False,
        "SIDECAR_DESIGN_24_NO_BUILDER_COMMAND": classification["builder_command_emitted"] is False,
        "SIDECAR_DESIGN_25_NO_C7_OR_C8": classification["c7_authorized"] is False and classification["c8_authorized"] is False,
        "SIDECAR_DESIGN_26_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "SIDECAR_DESIGN_27_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["schema_validator_reference_mutated"] is False and classification["observability_reference_mutated"] is False,
        "SIDECAR_DESIGN_28_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "SIDECAR_DESIGN_29_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_DESIGN_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_DESIGN_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_DESIGN_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_decision": SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID,
        "recommended_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "runtime_observability_sidecar_target_design_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_DESIGN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_post_schema_validator_reference_decision_receipt_id": SOURCE_POST_SCHEMA_VALIDATOR_DECISION_RECEIPT_ID,
        "source_runtime_schema_validator_reference_closure_receipt_id": SOURCE_SCHEMA_VALIDATOR_CLOSURE_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBSERVABILITY_CLOSURE_RECEIPT_ID,
        "machine_readable_runtime_observability_sidecar_design_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "runtime_observability_sidecar_target_designed": gate == "PASS",
            "observability_sidecar_build_ready": gate == "PASS",
            "source_decision_consumed": True,
            "schema_validator_reference_consumed": True,
            "edge_observability_reference_consumed": True,
            "hook_registry_target_defined": gate == "PASS",
            "event_record_schema_target_defined": gate == "PASS",
            "receipt_schema_target_defined": gate == "PASS",
            "append_only_trace_schema_target_defined": gate == "PASS",
            "rollup_readout_profile_schema_target_defined": gate == "PASS",
            "unknown_hook_behavior_defined": gate == "PASS",
            "forbidden_control_behavior_defined": gate == "PASS",
            "nonblocking_failure_behavior_defined": gate == "PASS",
            "load_bearing_field_map_defined": gate == "PASS",
            "observability_alignment_defined": gate == "PASS",
            "demo_case_plan_defined": gate == "PASS",
            "acceptance_gates_defined": gate == "PASS",
            "negative_controls_defined": gate == "PASS",
            "hook_count": len(SIDECAR_INITIAL_HOOKS),
            "schema_validator_observable_event_count": len(SCHEMA_VALIDATOR_OBSERVABLE_EVENTS),
            "load_bearing_edge_field_count": len(REQUIRED_EDGE_FIELDS),
            "demo_case_count": len(DEMO_CASES),
            "acceptance_gate_count": acceptance_gates["gate_count"],
            "negative_control_count": negative_controls["negative_control_count"],
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
            "validation_verdict_emitted": False,
            "authority_checked": False,
            "admissibility_checked": False,
            "execution_claimed": False,
            "schema_archive_mutated": False,
            "proposal_repaired": False,
            "schema_created": False,
            "builder_command_emitted": False,
            "control_path_blocked": False,
            "control_path_advanced": False,
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
            "design_basis": rel(DESIGN_BASIS_PATH),
            "source_decision_review": rel(SOURCE_DECISION_REVIEW_PATH),
            "source_schema_validator_reference_review": rel(SOURCE_SCHEMA_VALIDATOR_REFERENCE_REVIEW_PATH),
            "source_edge_observability_reference_review": rel(SOURCE_EDGE_OBSERVABILITY_REFERENCE_REVIEW_PATH),
            "target_spec": rel(TARGET_SPEC_PATH),
            "hook_registry_target": rel(HOOK_REGISTRY_TARGET_PATH),
            "event_record_schema_target": rel(EVENT_RECORD_SCHEMA_TARGET_PATH),
            "receipt_schema_target": rel(RECEIPT_SCHEMA_TARGET_PATH),
            "append_only_trace_schema_target": rel(APPEND_ONLY_TRACE_SCHEMA_TARGET_PATH),
            "rollup_readout_profile_schema_target": rel(ROLLUP_READOUT_PROFILE_SCHEMA_TARGET_PATH),
            "unknown_hook_behavior_target": rel(UNKNOWN_HOOK_BEHAVIOR_TARGET_PATH),
            "forbidden_control_behavior_target": rel(FORBIDDEN_CONTROL_BEHAVIOR_TARGET_PATH),
            "nonblocking_failure_behavior_target": rel(NONBLOCKING_FAILURE_BEHAVIOR_TARGET_PATH),
            "load_bearing_field_map": rel(LOAD_BEARING_FIELD_MAP_PATH),
            "observability_alignment_target": rel(OBSERVABILITY_ALIGNMENT_TARGET_PATH),
            "demo_case_plan": rel(DEMO_CASE_PLAN_PATH),
            "acceptance_gates": rel(ACCEPTANCE_GATES_PATH),
            "negative_controls": rel(NEGATIVE_CONTROLS_PATH),
            "build_target": rel(BUILD_TARGET_PATH),
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
    print(f"runtime_observability_sidecar_design_receipt_id={receipt_id}")
    print(f"runtime_observability_sidecar_design_receipt_path={rel(receipt_path)}")
    print(f"runtime_observability_sidecar_target_spec_path={rel(TARGET_SPEC_PATH)}")
    print(f"runtime_observability_sidecar_build_target_path={rel(BUILD_TARGET_PATH)}")
    print(f"runtime_observability_sidecar_design_rollup_path={rel(ROLLUP_PATH)}")
    print(f"runtime_observability_sidecar_design_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
