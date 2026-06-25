#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DESIGN_RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_FROM_REVIEWED_OBSERVABILITY_REFERENCE_V0"
TARGET_UNIT_ID = "runtime.schema_validator_cell.target_design.v0"
LAYER = "RUNTIME / SIEVE_1 / TARGET_DESIGN"
MODE = "DESIGN_ONLY / FORMATION_SIEVE_TARGET / NO_RUNTIME_PATCH"
BUILD_MODE = "RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_DESIGN_ONLY"

SOURCE_POST_EDGE_DECISION_RECEIPT_ID = "1f19ab63"
SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID = "ac09c2e3"

SOURCE_POST_EDGE_DECISION_RECEIPT_PATH = ROOT / "data/post_decision_edge_observability_reference_decision_v0_receipts/1f19ab63.json"

POST_EDGE_DECISION_DIR = ROOT / "data/post_decision_edge_observability_reference_decision_v0"
POST_EDGE_FILES = [
    POST_EDGE_DECISION_DIR / "post_edge_observability_reference_decision_basis_v0.json",
    POST_EDGE_DECISION_DIR / "post_edge_observability_reference_decision_options_v0.json",
    POST_EDGE_DECISION_DIR / "post_edge_observability_reference_selected_branch_v0.json",
    POST_EDGE_DECISION_DIR / "runtime_schema_validator_cell_design_target_v0.json",
    POST_EDGE_DECISION_DIR / "runtime_observability_sidecar_deferred_target_v0.json",
    POST_EDGE_DECISION_DIR / "pre_c8_interlock_plan_v0.json",
    POST_EDGE_DECISION_DIR / "decision_edge_observability_reference_park_record_v0.json",
    POST_EDGE_DECISION_DIR / "post_edge_observability_reference_deferred_branches_v0.json",
    POST_EDGE_DECISION_DIR / "post_edge_observability_reference_decision_authority_boundary_v0.json",
    POST_EDGE_DECISION_DIR / "post_edge_observability_reference_decision_classification_v0.json",
    POST_EDGE_DECISION_DIR / "post_edge_observability_reference_decision_rollup_v0.json",
    POST_EDGE_DECISION_DIR / "post_edge_observability_reference_decision_profile_v0.json",
    POST_EDGE_DECISION_DIR / "post_edge_observability_reference_decision_report.json",
    POST_EDGE_DECISION_DIR / "post_edge_observability_reference_decision_transition_trace.json",
]

SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_PATH = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0_receipts/ac09c2e3.json"
EDGE_OBS_REF_DIR = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0"
EDGE_OBS_REVIEWED_REFERENCE_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_reviewed_reference_v0.json"
EDGE_OBS_FREEZE_MANIFEST_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_reviewed_reference_freeze_manifest_v0.json"
EDGE_OBS_REQUIREMENT_REFERENCE_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_requirement_reference_v0.json"
EDGE_OBS_FIELD_SCHEMA_REFERENCE_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_field_schema_reference_v0.json"
EDGE_OBS_DISTINCTION_GUARD_REFERENCE_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_distinction_guard_reference_v0.json"
EDGE_OBS_NEGATIVE_CONTROL_REFERENCE_PATH = EDGE_OBS_REF_DIR / "decision_edge_observability_negative_control_reference_v0.json"

REQUIRED_SOURCE_FILES = [
    SOURCE_POST_EDGE_DECISION_RECEIPT_PATH,
    SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_PATH,
    EDGE_OBS_REVIEWED_REFERENCE_PATH,
    EDGE_OBS_FREEZE_MANIFEST_PATH,
    EDGE_OBS_REQUIREMENT_REFERENCE_PATH,
    EDGE_OBS_FIELD_SCHEMA_REFERENCE_PATH,
    EDGE_OBS_DISTINCTION_GUARD_REFERENCE_PATH,
    EDGE_OBS_NEGATIVE_CONTROL_REFERENCE_PATH,
] + POST_EDGE_FILES

OUT_DIR = ROOT / "data/runtime_schema_validator_cell_target_from_reviewed_observability_reference_v0"
RECEIPT_DIR = ROOT / "data/runtime_schema_validator_cell_target_from_reviewed_observability_reference_v0_receipts"

DESIGN_BASIS_PATH = OUT_DIR / "runtime_schema_validator_cell_design_basis_v0.json"
SOURCE_DECISION_REVIEW_PATH = OUT_DIR / "runtime_schema_validator_cell_source_decision_review_v0.json"
SOURCE_OBSERVABILITY_REFERENCE_REVIEW_PATH = OUT_DIR / "runtime_schema_validator_cell_source_observability_reference_review_v0.json"
TARGET_SPEC_PATH = OUT_DIR / "runtime_schema_validator_cell_target_spec_v0.json"
FORMATION_CHECK_TABLE_PATH = OUT_DIR / "runtime_schema_validator_cell_formation_check_table_v0.json"
FAILURE_PRECEDENCE_PATH = OUT_DIR / "runtime_schema_validator_cell_failure_precedence_v0.json"
RESULT_ENUM_TARGET_PATH = OUT_DIR / "schema_validation_result_enum_target_v0.json"
RESULT_SCHEMA_TARGET_PATH = OUT_DIR / "schema_validation_result_schema_target_v0.json"
VALIDATED_PACKET_TARGET_PATH = OUT_DIR / "validated_candidate_packet_schema_target_v0.json"
SCHEMA_FEEDBACK_TARGET_PATH = OUT_DIR / "schema_feedback_packet_schema_target_v0.json"
SCHEMA_GAP_FEEDBACK_TARGET_PATH = OUT_DIR / "schema_gap_feedback_packet_schema_target_v0.json"
RECEIPT_SCHEMA_TARGET_PATH = OUT_DIR / "schema_validator_cell_receipt_schema_target_v0.json"
DEMO_CASE_PLAN_PATH = OUT_DIR / "runtime_schema_validator_cell_demo_case_plan_v0.json"
ACCEPTANCE_GATES_PATH = OUT_DIR / "runtime_schema_validator_cell_acceptance_gates_v0.json"
NEGATIVE_CONTROLS_PATH = OUT_DIR / "runtime_schema_validator_cell_negative_controls_v0.json"
SIDECAR_DEPENDENCY_PARK_PATH = OUT_DIR / "runtime_observability_sidecar_dependency_park_v0.json"
BUILD_TARGET_PATH = OUT_DIR / "runtime_schema_validator_cell_build_target_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "runtime_schema_validator_cell_design_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "runtime_schema_validator_cell_design_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_schema_validator_cell_design_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_schema_validator_cell_design_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_schema_validator_cell_design_report.json"
TRACE_PATH = OUT_DIR / "runtime_schema_validator_cell_design_transition_trace.json"

EXPECTED_SOURCE_STATUS = "TYPED_POST_EDGE_OBSERVABILITY_REFERENCE_DECISION_SELECTED_SCHEMA_VALIDATOR_DESIGN_READY"
EXPECTED_SOURCE_STOP = "STOP_TYPED_POST_EDGE_OBSERVABILITY_REFERENCE_DECISION_SELECTED_SCHEMA_VALIDATOR_DESIGN_READY"
EXPECTED_SOURCE_NEXT = UNIT_ID
EXPECTED_SELECTED_BRANCH = "DESIGN_RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_FROM_REVIEWED_OBSERVABILITY_REFERENCE"

RECOMMENDED_NEXT = "BUILD_RUNTIME_SCHEMA_VALIDATOR_CELL_V0"

REQUIRED_EDGE_FIELDS = [
    "active_object",
    "attempted_move",
    "boundary_checked",
    "boundary_result",
    "blocked_moves",
    "lawful_next_moves",
    "source_packet_ref",
]

FAILURE_PRECEDENCE = [
    "SCHEMA_ARCHIVE_UNAVAILABLE",
    "UNKNOWN_SCHEMA",
    "SCHEMA_VERSION_MISMATCH",
    "INVALID_SHAPE",
    "MISSING_FIELD",
    "FORBIDDEN_FIELD",
    "TYPE_MISMATCH",
    "UNKNOWN_MOVE_TYPE",
    "BOUNDARY_MISSING",
    "BOUNDARY_CONFLICT",
    "UNRESOLVED_REFERENCE",
    "RECEIPT_CONTRACT_INSUFFICIENT",
    "DISTINGUISHABILITY_INSUFFICIENT",
    "LAYER_COLLAPSE_IN_PAYLOAD",
    "HIDDEN_EXECUTION_FIELD",
    "SCHEMA_ARCHIVE_GAP",
]

RESULT_ENUM = [
    "VALID",
    "UNKNOWN_SCHEMA",
    "INVALID_SHAPE",
    "TYPE_MISMATCH",
    "MISSING_FIELD",
    "FORBIDDEN_FIELD",
    "BOUNDARY_MISSING",
    "BOUNDARY_CONFLICT",
    "UNRESOLVED_REFERENCE",
    "UNKNOWN_MOVE_TYPE",
    "RECEIPT_CONTRACT_INSUFFICIENT",
    "DISTINGUISHABILITY_INSUFFICIENT",
    "SCHEMA_VERSION_MISMATCH",
    "LAYER_COLLAPSE_IN_PAYLOAD",
    "HIDDEN_EXECUTION_FIELD",
    "SCHEMA_ARCHIVE_UNAVAILABLE",
    "MISSING_REVIEW_BASIS",
    "BUILD_VERIFICATION_MISMATCH",
    "SCHEMA_ARCHIVE_GAP",
]

FORMATION_CHECKS = [
    {"order": 0, "check_name": "schema_archive_available", "failure": "SCHEMA_ARCHIVE_UNAVAILABLE"},
    {"order": 1, "check_name": "schema_known", "failure": "UNKNOWN_SCHEMA"},
    {"order": 2, "check_name": "schema_version_compatible", "failure": "SCHEMA_VERSION_MISMATCH"},
    {"order": 3, "check_name": "shape_valid", "failure": "INVALID_SHAPE"},
    {"order": 4, "check_name": "required_fields_present", "failure": "MISSING_FIELD"},
    {"order": 5, "check_name": "forbidden_fields_absent", "failure": "FORBIDDEN_FIELD"},
    {"order": 6, "check_name": "field_types_correct", "failure": "TYPE_MISMATCH"},
    {"order": 7, "check_name": "declared_move_type_known", "failure": "UNKNOWN_MOVE_TYPE"},
    {"order": 8, "check_name": "declared_boundary_structure_complete", "failure": "BOUNDARY_MISSING"},
    {"order": 9, "check_name": "declared_boundary_structure_consistent", "failure": "BOUNDARY_CONFLICT"},
    {"order": 10, "check_name": "references_structurally_resolvable", "failure": "UNRESOLVED_REFERENCE"},
    {"order": 11, "check_name": "receipt_contract_declared", "failure": "RECEIPT_CONTRACT_INSUFFICIENT"},
    {"order": 12, "check_name": "distinguishability_sufficient", "failure": "DISTINGUISHABILITY_INSUFFICIENT"},
    {"order": 13, "check_name": "layer_collapse_absent", "failure": "LAYER_COLLAPSE_IN_PAYLOAD"},
    {"order": 14, "check_name": "hidden_execution_fields_absent", "failure": "HIDDEN_EXECUTION_FIELD"},
]

DEMO_CASES = [
    ("valid_bounded_repair_proposal", "VALID"),
    ("valid_extraction_proposal", "VALID"),
    ("missing_required_field", "MISSING_FIELD"),
    ("missing_receipt_contract", "RECEIPT_CONTRACT_INSUFFICIENT"),
    ("unknown_schema", "UNKNOWN_SCHEMA"),
    ("schema_version_mismatch", "SCHEMA_VERSION_MISMATCH"),
    ("type_mismatch", "TYPE_MISMATCH"),
    ("boundary_missing", "BOUNDARY_MISSING"),
    ("boundary_conflict", "BOUNDARY_CONFLICT"),
    ("unresolved_reference", "UNRESOLVED_REFERENCE"),
    ("unknown_move_type", "UNKNOWN_MOVE_TYPE"),
    ("distinguishability_insufficient", "DISTINGUISHABILITY_INSUFFICIENT"),
    ("layer_collapse_in_payload", "LAYER_COLLAPSE_IN_PAYLOAD"),
    ("hidden_execution_field", "HIDDEN_EXECUTION_FIELD"),
    ("latest_file_reference", "UNRESOLVED_REFERENCE"),
    ("mtime_reference", "UNRESOLVED_REFERENCE"),
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

    decision_receipt = read_json(SOURCE_POST_EDGE_DECISION_RECEIPT_PATH)
    decision_summary = decision_receipt.get("machine_readable_post_edge_observability_reference_decision_summary", {})
    selected_branch = read_json(POST_EDGE_DECISION_DIR / "post_edge_observability_reference_selected_branch_v0.json")
    source_target = read_json(POST_EDGE_DECISION_DIR / "runtime_schema_validator_cell_design_target_v0.json")
    pre_c8_plan = read_json(POST_EDGE_DECISION_DIR / "pre_c8_interlock_plan_v0.json")
    sidecar_deferred = read_json(POST_EDGE_DECISION_DIR / "runtime_observability_sidecar_deferred_target_v0.json")
    authority = read_json(POST_EDGE_DECISION_DIR / "post_edge_observability_reference_decision_authority_boundary_v0.json")
    classification = read_json(POST_EDGE_DECISION_DIR / "post_edge_observability_reference_decision_classification_v0.json")
    profile = read_json(POST_EDGE_DECISION_DIR / "post_edge_observability_reference_decision_profile_v0.json")
    report = read_json(POST_EDGE_DECISION_DIR / "post_edge_observability_reference_decision_report.json")

    obs_ref_close_receipt = read_json(SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_PATH)
    obs_reviewed_reference = read_json(EDGE_OBS_REVIEWED_REFERENCE_PATH)
    obs_freeze_manifest = read_json(EDGE_OBS_FREEZE_MANIFEST_PATH)
    obs_requirement_reference = read_json(EDGE_OBS_REQUIREMENT_REFERENCE_PATH)
    obs_field_schema_reference = read_json(EDGE_OBS_FIELD_SCHEMA_REFERENCE_PATH)
    obs_distinction_reference = read_json(EDGE_OBS_DISTINCTION_GUARD_REFERENCE_PATH)
    obs_negative_reference = read_json(EDGE_OBS_NEGATIVE_CONTROL_REFERENCE_PATH)

    if decision_receipt.get("receipt_id") != SOURCE_POST_EDGE_DECISION_RECEIPT_ID or decision_receipt.get("gate") != "PASS":
        failures.append("source_post_edge_decision_receipt_not_pass")
    if decision_receipt.get("terminal", {}).get("stop_code") != EXPECTED_SOURCE_STOP:
        failures.append("source_stop_wrong")
    if decision_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_hidden_next")
    if decision_summary.get("status") != EXPECTED_SOURCE_STATUS:
        failures.append(f"source_status_wrong:{decision_summary.get('status')}")
    if decision_summary.get("selected_next_unit") != EXPECTED_SOURCE_NEXT:
        failures.append(f"source_selected_next_wrong:{decision_summary.get('selected_next_unit')}")
    if decision_summary.get("selected_branch") != EXPECTED_SELECTED_BRANCH:
        failures.append(f"source_selected_branch_wrong:{decision_summary.get('selected_branch')}")

    for key in [
        "post_edge_observability_reference_decision_complete",
        "schema_validator_design_selected",
        "schema_validator_design_ready",
        "observability_sidecar_deferred",
        "unit_feedback_hardening_deferred",
        "c7_deferred",
        "c8_deferred",
        "runtime_adoption_deferred",
        "nothing_else_before_c8",
        "bad_counters_zero",
    ]:
        if decision_summary.get(key) is not True:
            failures.append(f"source_required_true_missing:{key}")

    for key in [
        "runtime_effect",
        "runtime_patched",
        "c7_authorized",
        "c8_authorized",
        "new_domain_shift_executed",
        "general_cell1_authority_claimed",
        "global_autonomy_claimed",
        "full_transfer_claimed",
        "runtime_wide_enforcement_claimed",
        "source_mutated",
        "prior_receipt_mutated",
        "c6_reviewed_reference_mutated",
        "bounded_probe_reference_mutated",
        "observability_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if decision_summary.get(key) is not False:
            failures.append(f"source_forbidden_true:{key}")

    if selected_branch.get("selected_next_unit") != EXPECTED_SOURCE_NEXT:
        failures.append("selected_branch_next_wrong")
    if source_target.get("target_unit") != EXPECTED_SOURCE_NEXT:
        failures.append("source_target_unit_wrong")
    if source_target.get("terminology_adjustment", {}).get("use") != "VALIDATE / CLASSIFY / FORMATION_ONLY":
        failures.append("terminology_adjustment_missing")
    if source_target.get("failure_precedence_required") != FAILURE_PRECEDENCE:
        failures.append("failure_precedence_source_wrong")

    if pre_c8_plan.get("nothing_else_before_c8") is not True:
        failures.append("pre_c8_plan_wrong")
    if [x.get("object") for x in pre_c8_plan.get("remaining_pre_c8_mechanics", [])] != ["Schema Validator Cell", "Observability Sidecar"]:
        failures.append("pre_c8_mechanics_wrong")
    if sidecar_deferred.get("deferred_target_status") != "DEFERRED_UNTIL_SCHEMA_VALIDATOR_REFERENCE_EXISTS":
        failures.append("sidecar_not_deferred")

    if authority.get("may_design_schema_validator_cell_next") is not True:
        failures.append("authority_no_schema_validator_design")
    for forbidden in [
        "may_design_observability_sidecar_now",
        "may_build_schema_validator_cell_now",
        "may_build_observability_sidecar_now",
        "may_harden_unit_feedback_now",
        "may_patch_runtime_now",
        "may_open_c7_now",
        "may_open_c8_now",
        "may_execute_new_domain_shift",
        "may_claim_full_transfer",
        "may_claim_global_autonomy",
        "may_claim_general_cell1_authority",
        "may_claim_runtime_wide_enforcement",
        "may_mutate_source",
        "may_mutate_prior_receipts",
        "may_mutate_c6_reviewed_reference",
        "may_mutate_bounded_probe_reference",
        "may_mutate_observability_reference",
    ]:
        if authority.get(forbidden) is not False:
            failures.append(f"authority_forbidden_true:{forbidden}")

    if classification.get("next_command_goal") is not None:
        failures.append("classification_hidden_next")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_SOURCE_NEXT:
        failures.append("report_next_wrong")

    if obs_ref_close_receipt.get("receipt_id") != SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID or obs_ref_close_receipt.get("gate") != "PASS":
        failures.append("obs_ref_close_receipt_not_pass")
    if obs_reviewed_reference.get("reference_status") != "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_FROZEN":
        failures.append("obs_reference_not_frozen")
    if obs_freeze_manifest.get("freeze_status") != "FROZEN":
        failures.append("obs_freeze_manifest_not_frozen")
    if obs_requirement_reference.get("required_fields") != REQUIRED_EDGE_FIELDS:
        failures.append("obs_required_edge_fields_wrong")
    if obs_requirement_reference.get("edge_requirement_count") != 7:
        failures.append("obs_edge_requirement_count_wrong")
    if obs_field_schema_reference.get("required_field_count") != 7:
        failures.append("obs_field_count_wrong")
    if obs_distinction_reference.get("guard_count") != 8:
        failures.append("obs_guard_count_wrong")
    if obs_negative_reference.get("negative_control_count") != 13:
        failures.append("obs_negative_control_count_wrong")

    return failures, {
        "decision_summary": decision_summary,
        "source_target": source_target,
        "pre_c8_plan": pre_c8_plan,
        "sidecar_deferred": sidecar_deferred,
        "obs_reviewed_reference": obs_reviewed_reference,
        "obs_requirement_reference": obs_requirement_reference,
        "obs_field_schema_reference": obs_field_schema_reference,
        "obs_distinction_reference": obs_distinction_reference,
        "obs_negative_reference": obs_negative_reference,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    design_pass = not failures
    status = "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_DESIGNED_BUILD_READY" if design_pass else "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_DESIGN_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if design_pass else "REPAIR_RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_DESIGN_V0"

    decision_summary = basis.get("decision_summary", {})
    source_target = basis.get("source_target", {})
    pre_c8_plan = basis.get("pre_c8_plan", {})
    sidecar_deferred = basis.get("sidecar_deferred", {})
    obs_reviewed_reference = basis.get("obs_reviewed_reference", {})
    obs_requirement_reference = basis.get("obs_requirement_reference", {})
    obs_field_schema_reference = basis.get("obs_field_schema_reference", {})
    obs_distinction_reference = basis.get("obs_distinction_reference", {})
    obs_negative_reference = basis.get("obs_negative_reference", {})

    reason_codes = [
        "RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_DESIGNED",
        "POST_EDGE_OBSERVABILITY_DECISION_RECEIPT_CONSUMED",
        "DECISION_EDGE_OBSERVABILITY_REVIEWED_REFERENCE_CONSUMED",
        "FORMATION_ONLY_BOUNDARY_DEFINED",
        "SCHEMA_ARCHIVE_READ_ONLY_BOUNDARY_DEFINED",
        "VALIDATE_CLASSIFY_TERMINOLOGY_LOCKED",
        "FAILURE_PRECEDENCE_LOCKED",
        "VALIDATION_RESULT_ENUM_TARGET_DEFINED",
        "VALIDATED_CANDIDATE_PACKET_TARGET_DEFINED",
        "SCHEMA_FEEDBACK_PACKET_TARGET_DEFINED",
        "SCHEMA_GAP_FEEDBACK_PACKET_TARGET_DEFINED",
        "RECEIPT_SCHEMA_TARGET_DEFINED",
        "DEMO_CASE_PLAN_DEFINED",
        "OBSERVABILITY_FIELDS_PRESERVED",
        "SIDECAR_DEFERRED_UNTIL_SCHEMA_VALIDATOR_REFERENCE_EXISTS",
        "C8_DEFERRED",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_C7_AUTHORIZATION",
        "NO_C8_AUTHORIZATION",
        "NO_SCHEMA_VALIDATOR_BUILD",
        "NO_OBSERVABILITY_SIDECAR_DESIGN_OR_BUILD",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if design_pass else failures

    design_basis = {
        "schema_version": "runtime_schema_validator_cell_design_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if design_pass else "BASIS_REPAIR_REQUIRED",
        "source_post_edge_observability_decision_receipt_id": SOURCE_POST_EDGE_DECISION_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "source_decision_status": decision_summary.get("status"),
        "source_reference_status": obs_reviewed_reference.get("reference_status"),
        "source_target_unit": source_target.get("target_unit"),
        "pre_c8_plan_status": pre_c8_plan.get("plan_status"),
    }

    source_decision_review = {
        "schema_version": "runtime_schema_validator_cell_source_decision_review_v0",
        "source_decision_receipt_id": SOURCE_POST_EDGE_DECISION_RECEIPT_ID,
        "source_gate": "PASS" if design_pass else "REPAIR_REQUIRED",
        "selected_branch": decision_summary.get("selected_branch"),
        "selected_next_unit": decision_summary.get("selected_next_unit"),
        "sidecar_deferred": decision_summary.get("observability_sidecar_deferred"),
        "c8_deferred": decision_summary.get("c8_deferred"),
        "nothing_else_before_c8": decision_summary.get("nothing_else_before_c8"),
        "next_command_goal": None,
    }

    source_observability_reference_review = {
        "schema_version": "runtime_schema_validator_cell_source_observability_reference_review_v0",
        "source_reference_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "reference_status": obs_reviewed_reference.get("reference_status"),
        "edge_requirement_count": obs_requirement_reference.get("edge_requirement_count"),
        "required_edge_fields": obs_requirement_reference.get("required_fields"),
        "field_schema_count": obs_field_schema_reference.get("required_field_count"),
        "distinction_guard_count": obs_distinction_reference.get("guard_count"),
        "negative_control_count": obs_negative_reference.get("negative_control_count"),
        "load_bearing_rule_consumed": True,
    }

    target_spec = {
        "schema_version": "runtime_schema_validator_cell_target_spec_v0",
        "target_status": "DESIGNED_BUILD_READY" if design_pass else "NOT_READY",
        "future_build_unit": RECOMMENDED_NEXT if design_pass else None,
        "unit_id": "BUILD_RUNTIME_SCHEMA_VALIDATOR_CELL_V0",
        "target_unit_id": "runtime.schema_validator_cell.v0",
        "layer": "RUNTIME / SIEVE_1",
        "mode": "VALIDATE / CLASSIFY / FORMATION_ONLY",
        "active_object": "one Builder / Proposal Cell candidate packet",
        "role": "first proposal-formation sieve",
        "core_question": "Can this proposal be read as a well-formed candidate under a known schema?",
        "core_law": "No proposal may reach the Lawful Admissibility Cell unless it is structurally valid under a known schema.",
        "runtime_position": [
            "Builder / Proposal Cell",
            "Schema Validator Cell",
            "Lawful Admissibility Cell",
            "Builder Execution",
            "Advance / Halt",
        ],
        "load_bearing_distinction": {
            "schema_validator_cell": "Can this proposal be read?",
            "lawful_admissibility_cell": "If readable, is it allowed?",
        },
        "allowed_inputs": [
            "proposal packet",
            "claimed schema ref",
            "claimed schema version",
            "read-only schema archive / registry",
            "schema compatibility table",
            "declared object boundaries",
            "declared move type",
            "declared references",
            "declared receipt contract",
            "declared verification / distinguishability fields",
        ],
        "forbidden_inputs": [
            "current authority regime",
            "human authorization status",
            "strategic roadmap",
            "runtime patch target files",
            "ambient workspace",
            "latest-file selection",
            "mtime selection",
            "hidden memory",
            "execution result",
            "builder output",
        ],
        "allowed_outputs": [
            "schema_validation_result",
            "validated_candidate_packet if VALID",
            "schema_feedback_packet if invalid under known schema",
            "schema_gap_feedback_packet if schema archive gap",
            "schema_validator_receipt",
            "rollup/readout/profile/report/transition_trace",
        ],
        "forbidden_outputs": [
            "authority verdict",
            "admissibility decision",
            "execution approval",
            "builder command",
            "proposal repair output",
            "schema archive mutation",
            "schema creation",
            "runtime patch",
            "C7 authorization",
            "C8 authorization",
        ],
        "valid_means": "structurally validated under known schema",
        "valid_does_not_mean": [
            "authorized",
            "admissible",
            "true",
            "useful",
            "strategically accepted",
            "executed",
            "verified",
        ],
    }

    formation_check_table = {
        "schema_version": "runtime_schema_validator_cell_formation_check_table_v0",
        "checks": FORMATION_CHECKS,
        "deterministic_failure_precedence": FAILURE_PRECEDENCE,
        "advance_only_on": "VALID",
        "invalid_returns_to": "BUILDER_PROPOSAL_CELL",
        "valid_advances_to": "LAWFUL_ADMISSIBILITY_CELL",
    }

    failure_precedence = {
        "schema_version": "runtime_schema_validator_cell_failure_precedence_v0",
        "precedence_status": "LOCKED",
        "failure_precedence": FAILURE_PRECEDENCE,
        "why": "Same malformed proposal should classify deterministically instead of producing unstable failure labels.",
    }

    result_enum_target = {
        "schema_version": "schema_validation_result_enum_target_v0",
        "enum_status": "DESIGNED",
        "closed_results": RESULT_ENUM,
        "only_advancing_result": "VALID",
    }

    result_schema_target = {
        "schema_version": "schema_validation_result_schema_target_v0",
        "target_schema_name": "schema_validation_result_schema_v0.json",
        "required_top_level_fields": [
            "schema_version",
            "validation_id",
            "cell_id",
            "input_proposal_ref",
            "claimed_schema_ref",
            "claimed_schema_version",
            "result",
            "result_class",
            "field_results",
            "boundary_results",
            "return_to",
            "must_not_infer",
            "terminal",
        ],
        "must_not_infer": [
            "proposal is authorized",
            "proposal is true",
            "proposal should execute",
            "proposal is strategically good",
        ],
    }

    validated_packet_target = {
        "schema_version": "validated_candidate_packet_schema_target_v0",
        "target_schema_name": "validated_candidate_packet_schema_v0.json",
        "emitted_only_if": "schema_validation_result.result == VALID",
        "from_cell": "SCHEMA_VALIDATOR_CELL",
        "to_cell": "LAWFUL_ADMISSIBILITY_CELL",
        "required_status_fields": {
            "validation_status": "SCHEMA_VALIDATED",
            "authority_status": "NOT_CHECKED",
            "admissibility_status": "NOT_CHECKED",
            "execution_status": "NOT_EXECUTED",
            "verification_status": "NOT_VERIFIED",
        },
        "must_not_infer": [
            "authorized",
            "admissible",
            "executed",
            "verified",
            "strategically accepted",
        ],
    }

    schema_feedback_target = {
        "schema_version": "schema_feedback_packet_schema_target_v0",
        "target_schema_name": "schema_feedback_packet_schema_v0.json",
        "emitted_if": "known schema exists and proposal fails formation checks",
        "to_cell": "BUILDER_PROPOSAL_CELL",
        "blocked_transition": "LAWFUL_ADMISSIBILITY_CELL",
        "repair_hint_rule": "repair_hint is feedback, not repair",
        "forbidden_next_handling": [
            "send to admissibility anyway",
            "execute",
            "treat as authority denial",
            "mutate schema archive directly",
        ],
    }

    schema_gap_feedback_target = {
        "schema_version": "schema_gap_feedback_packet_schema_target_v0",
        "target_schema_name": "schema_gap_feedback_packet_schema_v0.json",
        "emitted_if": "proposal may be meaningful but no known schema can represent it",
        "gap_class": "SCHEMA_ARCHIVE_GAP",
        "rule": "Schema gap is not schema creation permission.",
        "forbidden_next_handling": [
            "create schema directly",
            "validate by analogy",
            "send to admissibility",
            "execute",
        ],
    }

    receipt_schema_target = {
        "schema_version": "schema_validator_cell_receipt_schema_target_v0",
        "target_schema_name": "schema_validator_cell_receipt_schema_v0.json",
        "required_zero_counters": [
            "authority_claim_count",
            "admissibility_checked_count",
            "execution_claim_count",
            "schema_archive_mutation_count",
            "proposal_repair_count",
            "schema_created_count",
            "unknown_schema_accepted_count",
            "invalid_proposal_advanced_count",
            "missing_receipt_contract_accepted_count",
            "unresolved_reference_accepted_count",
            "forbidden_field_accepted_count",
            "layer_collapse_accepted_count",
            "hidden_execution_field_accepted_count",
            "latest_file_reference_accepted_count",
            "mtime_reference_accepted_count",
            "builder_command_emitted_count",
        ],
    }

    demo_case_plan = {
        "schema_version": "runtime_schema_validator_cell_demo_case_plan_v0",
        "demo_case_count": len(DEMO_CASES),
        "cases": [
            {
                "case_id": f"schema_validator_demo_{i:02d}_{name}",
                "case_name": name,
                "expected_result": expected,
            }
            for i, (name, expected) in enumerate(DEMO_CASES)
        ],
        "expected_valid_count": sum(1 for _, expected in DEMO_CASES if expected == "VALID"),
        "expected_invalid_count": sum(1 for _, expected in DEMO_CASES if expected != "VALID"),
        "latest_or_mtime_cases_must_fail_as": "UNRESOLVED_REFERENCE",
    }

    acceptance_gates = {
        "schema_version": "runtime_schema_validator_cell_acceptance_gates_v0",
        "gate_count": 33,
        "gates": [
            "SCHEMA_VALIDATOR_0_SOURCE_DESIGN_CONSUMED",
            "SCHEMA_VALIDATOR_1_SCHEMA_ARCHIVE_SCHEMA_EMITTED",
            "SCHEMA_VALIDATOR_2_VALIDATION_RESULT_ENUM_EMITTED",
            "SCHEMA_VALIDATOR_3_VALIDATION_RESULT_SCHEMA_EMITTED",
            "SCHEMA_VALIDATOR_4_VALIDATED_CANDIDATE_PACKET_SCHEMA_EMITTED",
            "SCHEMA_VALIDATOR_5_SCHEMA_FEEDBACK_PACKET_SCHEMA_EMITTED",
            "SCHEMA_VALIDATOR_6_SCHEMA_GAP_FEEDBACK_PACKET_SCHEMA_EMITTED",
            "SCHEMA_VALIDATOR_7_RECEIPT_SCHEMA_EMITTED",
            "SCHEMA_VALIDATOR_8_CHECK_TABLE_EMITTED",
            "SCHEMA_VALIDATOR_9_DEMO_INPUTS_EMITTED",
            "SCHEMA_VALIDATOR_10_SCHEMA_KNOWN_CHECK_RUN",
            "SCHEMA_VALIDATOR_11_VERSION_CHECK_RUN",
            "SCHEMA_VALIDATOR_12_REQUIRED_FIELDS_CHECK_RUN",
            "SCHEMA_VALIDATOR_13_FORBIDDEN_FIELDS_CHECK_RUN",
            "SCHEMA_VALIDATOR_14_TYPE_CHECK_RUN",
            "SCHEMA_VALIDATOR_15_MOVE_TYPE_CHECK_RUN",
            "SCHEMA_VALIDATOR_16_BOUNDARY_CHECK_RUN",
            "SCHEMA_VALIDATOR_17_REFERENCE_CHECK_RUN",
            "SCHEMA_VALIDATOR_18_RECEIPT_CONTRACT_CHECK_RUN",
            "SCHEMA_VALIDATOR_19_DISTINGUISHABILITY_CHECK_RUN",
            "SCHEMA_VALIDATOR_20_LAYER_COLLAPSE_CHECK_RUN",
            "SCHEMA_VALIDATOR_21_HIDDEN_EXECUTION_FIELD_CHECK_RUN",
            "SCHEMA_VALIDATOR_22_ONLY_VALID_ADVANCES",
            "SCHEMA_VALIDATOR_23_INVALID_RETURNS_TO_BUILDER",
            "SCHEMA_VALIDATOR_24_NO_AUTHORITY_CLAIM",
            "SCHEMA_VALIDATOR_25_NO_ADMISSIBILITY_CHECK",
            "SCHEMA_VALIDATOR_26_NO_EXECUTION_CLAIM",
            "SCHEMA_VALIDATOR_27_NO_SCHEMA_ARCHIVE_MUTATION",
            "SCHEMA_VALIDATOR_28_NO_PROPOSAL_REPAIR",
            "SCHEMA_VALIDATOR_29_NO_BUILDER_COMMAND",
            "SCHEMA_VALIDATOR_30_ROLLUP_READOUT_PROFILE_EMITTED",
            "SCHEMA_VALIDATOR_31_BAD_COUNTERS_ZERO",
            "SCHEMA_VALIDATOR_32_NO_HIDDEN_NEXT_COMMAND",
        ],
    }

    negative_controls = {
        "schema_version": "runtime_schema_validator_cell_negative_controls_v0",
        "negative_control_count": 19,
        "controls": [
            "unknown_schema_accepted_fail",
            "invalid_proposal_advanced_fail",
            "missing_receipt_contract_accepted_fail",
            "unresolved_reference_accepted_fail",
            "forbidden_field_accepted_fail",
            "layer_collapse_accepted_fail",
            "hidden_execution_field_accepted_fail",
            "latest_file_reference_accepted_fail",
            "mtime_reference_accepted_fail",
            "authority_claim_emitted_fail",
            "admissibility_checked_by_validator_fail",
            "execution_claim_emitted_fail",
            "schema_archive_mutated_fail",
            "proposal_repaired_by_validator_fail",
            "schema_created_by_validator_fail",
            "builder_command_emitted_fail",
            "hidden_next_command_fail",
            "source_mutation_fail",
            "prior_receipt_mutation_fail",
        ],
    }

    sidecar_dependency_park = {
        "schema_version": "runtime_observability_sidecar_dependency_park_v0",
        "park_status": "PARKED_UNTIL_SCHEMA_VALIDATOR_REFERENCE_EXISTS",
        "future_unit": "DESIGN_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_FROM_SCHEMA_VALIDATOR_AND_OBSERVABILITY_REFERENCES_V0",
        "dependency": "future Schema Validator Cell reviewed reference",
        "why": "The Observability Sidecar should observe the Schema Validator event surface, so it must wait for the Schema Validator reference.",
        "not_authorized_now": [
            "design sidecar",
            "build sidecar",
            "patch runtime",
            "claim live instrumentation",
            "authorize C8",
        ],
    }

    build_target = {
        "schema_version": "runtime_schema_validator_cell_build_target_v0",
        "build_target_status": "BUILD_READY" if design_pass else "NOT_READY",
        "recommended_next": recommended_next,
        "build_unit": "BUILD_RUNTIME_SCHEMA_VALIDATOR_CELL_V0",
        "build_meaning": "Build the Schema Validator Cell surface and synthetic/demo validation run. Do not install it as mandatory live runtime routing yet.",
        "must_emit": [
            "schema archive schema",
            "schema validation result enum",
            "schema validation result schema",
            "validated candidate packet schema",
            "schema feedback packet schema",
            "schema gap feedback packet schema",
            "schema validator receipt schema",
            "check table",
            "demo inputs",
            "validation results",
            "validated candidate packets",
            "schema feedback packets",
            "schema gap feedback packets",
            "rollup",
            "readout",
            "profile",
            "report",
            "transition trace",
            "receipt",
        ],
    }

    authority_boundary = {
        "schema_version": "runtime_schema_validator_cell_design_authority_boundary_v0",
        "status": status,
        "may_build_schema_validator_cell_next": design_pass,
        "may_design_observability_sidecar_now": False,
        "may_build_observability_sidecar_now": False,
        "may_harden_unit_feedback_now": False,
        "may_patch_runtime_now": False,
        "may_install_live_runtime_routing": False,
        "may_check_authority": False,
        "may_check_admissibility": False,
        "may_execute": False,
        "may_repair_proposal": False,
        "may_mutate_schema_archive": False,
        "may_create_schema": False,
        "may_emit_builder_command": False,
        "may_open_c7_now": False,
        "may_open_c8_now": False,
        "may_execute_new_domain_shift": False,
        "may_claim_full_transfer": False,
        "may_claim_global_autonomy": False,
        "may_claim_general_cell1_authority": False,
        "may_claim_runtime_wide_enforcement": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_mutate_observability_reference": False,
    }

    classification = {
        "schema_version": "runtime_schema_validator_cell_design_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "runtime_schema_validator_cell_target_designed": design_pass,
        "schema_validator_build_ready": design_pass,
        "source_post_edge_decision_consumed": True,
        "source_observability_reference_consumed": True,
        "formation_only_boundary_defined": True,
        "validate_classify_terminology_locked": True,
        "failure_precedence_locked": True,
        "formation_check_count": len(FORMATION_CHECKS),
        "result_enum_count": len(RESULT_ENUM),
        "demo_case_count": len(DEMO_CASES),
        "acceptance_gate_count": acceptance_gates["gate_count"],
        "negative_control_count": negative_controls["negative_control_count"],
        "observability_required_edge_field_count": len(REQUIRED_EDGE_FIELDS),
        "observability_sidecar_deferred": True,
        "unit_feedback_hardening_deferred": True,
        "c7_deferred": True,
        "c8_deferred": True,
        "runtime_adoption_deferred": True,
        "runtime_effect": False,
        "runtime_patched": False,
        "live_runtime_routing_installed": False,
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
        "observability_reference_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": True,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "runtime_schema_validator_cell_design_rollup_v0",
        "design_count": 1 if design_pass else 0,
        "schema_validator_target_designed_count": 1 if design_pass else 0,
        "schema_validator_build_ready_count": 1 if design_pass else 0,
        "schema_validator_build_count": 0,
        "observability_sidecar_design_count": 0,
        "observability_sidecar_build_count": 0,
        "formation_check_count": len(FORMATION_CHECKS),
        "result_enum_count": len(RESULT_ENUM),
        "demo_case_count": len(DEMO_CASES),
        "acceptance_gate_count": acceptance_gates["gate_count"],
        "negative_control_count": negative_controls["negative_control_count"],
        "authority_checked_count": 0,
        "admissibility_checked_count": 0,
        "execution_claim_count": 0,
        "schema_archive_mutation_count": 0,
        "proposal_repair_count": 0,
        "schema_created_count": 0,
        "builder_command_emitted_count": 0,
        "runtime_patch_count": 0,
        "live_runtime_routing_installed_count": 0,
        "c7_authorized_count": 0,
        "c8_authorized_count": 0,
        "runtime_adoption_count": 0,
        "new_domain_shift_executed_count": 0,
        "general_cell1_authority_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "full_transfer_claim_count": 0,
        "runtime_wide_enforcement_claim_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "observability_reference_mutated_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "runtime_schema_validator_cell_design_profile_v0",
        "profile_id": "runtime_schema_validator_design_" + sig8(rollup),
        "status": status,
        "cell_id": "SCHEMA_VALIDATOR_CELL",
        "core_rule": "Schema Validator Cell validates form. Lawful Admissibility Cell validates permission.",
        "mode": "VALIDATE / CLASSIFY / FORMATION_ONLY",
        "valid_advances_only_to": "LAWFUL_ADMISSIBILITY_CELL",
        "invalid_returns_to": "BUILDER_PROPOSAL_CELL",
        "schema_archive_mutation_allowed": False,
        "authority_checked": False,
        "admissibility_checked": False,
        "execution_allowed": False,
        "build_ready": design_pass,
        "observability_sidecar_deferred": True,
        "bad_counters_zero": True,
        "must_not_infer": [
            "Schema Validator was built",
            "Schema Validator is live runtime routing",
            "VALID means authorized",
            "VALID means admissible",
            "VALID means true",
            "VALID means useful",
            "VALID means execute",
            "feedback hint means repair applied",
            "C8 is authorized",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "runtime_schema_validator_cell_design_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The Runtime Schema Validator Cell target is designed as the first proposal-formation sieve. It consumes the reviewed decision-edge observability reference, preserves load-bearing edge fields, locks formation-only classification, defines deterministic failure precedence, and prepares the build target. It does not build the validator, design the Sidecar, patch runtime, authorize C8, check authority/admissibility, execute, repair proposals, or mutate schema archives.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "runtime_schema_validator_cell_design_transition_trace_v0",
        "trace": [
            {
                "step": "consume_post_edge_observability_decision",
                "question": "was Schema Validator design selected",
                "answer": "yes" if design_pass else "no",
                "taken": "consume selected target and reviewed observability reference",
            },
            {
                "step": "design_schema_validator_target",
                "question": "what does the cell check",
                "answer": "proposal formation/readability under known schema only",
                "taken": "emit target spec, check table, failure precedence, packet targets, gates, controls",
            },
            {
                "step": "preserve_interlock_sequence",
                "question": "does this also design sidecar, patch runtime, or open C8",
                "answer": "no",
                "taken": "park sidecar until Schema Validator reference exists; defer C8",
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
        (SOURCE_OBSERVABILITY_REFERENCE_REVIEW_PATH, source_observability_reference_review),
        (TARGET_SPEC_PATH, target_spec),
        (FORMATION_CHECK_TABLE_PATH, formation_check_table),
        (FAILURE_PRECEDENCE_PATH, failure_precedence),
        (RESULT_ENUM_TARGET_PATH, result_enum_target),
        (RESULT_SCHEMA_TARGET_PATH, result_schema_target),
        (VALIDATED_PACKET_TARGET_PATH, validated_packet_target),
        (SCHEMA_FEEDBACK_TARGET_PATH, schema_feedback_target),
        (SCHEMA_GAP_FEEDBACK_TARGET_PATH, schema_gap_feedback_target),
        (RECEIPT_SCHEMA_TARGET_PATH, receipt_schema_target),
        (DEMO_CASE_PLAN_PATH, demo_case_plan),
        (ACCEPTANCE_GATES_PATH, acceptance_gates),
        (NEGATIVE_CONTROLS_PATH, negative_controls),
        (SIDECAR_DEPENDENCY_PARK_PATH, sidecar_dependency_park),
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
        "SCHEMA_VALIDATOR_DESIGN_0_POST_EDGE_DECISION_RECEIPT_CONSUMED": SOURCE_POST_EDGE_DECISION_RECEIPT_PATH.exists(),
        "SCHEMA_VALIDATOR_DESIGN_1_OBSERVABILITY_REFERENCE_CONSUMED": obs_reviewed_reference.get("reference_status") == "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_FROZEN",
        "SCHEMA_VALIDATOR_DESIGN_2_TARGET_SPEC_EMITTED": TARGET_SPEC_PATH.exists() and target_spec["target_status"] == "DESIGNED_BUILD_READY",
        "SCHEMA_VALIDATOR_DESIGN_3_FORMATION_ONLY_BOUNDARY_DEFINED": target_spec["mode"] == "VALIDATE / CLASSIFY / FORMATION_ONLY",
        "SCHEMA_VALIDATOR_DESIGN_4_CHECK_TABLE_EMITTED": FORMATION_CHECK_TABLE_PATH.exists() and len(FORMATION_CHECKS) == 15,
        "SCHEMA_VALIDATOR_DESIGN_5_FAILURE_PRECEDENCE_EMITTED": FAILURE_PRECEDENCE_PATH.exists() and failure_precedence["failure_precedence"] == FAILURE_PRECEDENCE,
        "SCHEMA_VALIDATOR_DESIGN_6_RESULT_ENUM_TARGET_EMITTED": RESULT_ENUM_TARGET_PATH.exists() and len(RESULT_ENUM) == 19,
        "SCHEMA_VALIDATOR_DESIGN_7_RESULT_SCHEMA_TARGET_EMITTED": RESULT_SCHEMA_TARGET_PATH.exists(),
        "SCHEMA_VALIDATOR_DESIGN_8_VALIDATED_PACKET_TARGET_EMITTED": VALIDATED_PACKET_TARGET_PATH.exists(),
        "SCHEMA_VALIDATOR_DESIGN_9_SCHEMA_FEEDBACK_TARGET_EMITTED": SCHEMA_FEEDBACK_TARGET_PATH.exists(),
        "SCHEMA_VALIDATOR_DESIGN_10_SCHEMA_GAP_FEEDBACK_TARGET_EMITTED": SCHEMA_GAP_FEEDBACK_TARGET_PATH.exists(),
        "SCHEMA_VALIDATOR_DESIGN_11_RECEIPT_SCHEMA_TARGET_EMITTED": RECEIPT_SCHEMA_TARGET_PATH.exists(),
        "SCHEMA_VALIDATOR_DESIGN_12_DEMO_CASE_PLAN_EMITTED": DEMO_CASE_PLAN_PATH.exists() and len(DEMO_CASES) == 16,
        "SCHEMA_VALIDATOR_DESIGN_13_ACCEPTANCE_GATES_EMITTED": ACCEPTANCE_GATES_PATH.exists() and acceptance_gates["gate_count"] == 33,
        "SCHEMA_VALIDATOR_DESIGN_14_NEGATIVE_CONTROLS_EMITTED": NEGATIVE_CONTROLS_PATH.exists() and negative_controls["negative_control_count"] == 19,
        "SCHEMA_VALIDATOR_DESIGN_15_OBSERVABILITY_EDGE_FIELDS_PRESERVED": source_observability_reference_review["required_edge_fields"] == REQUIRED_EDGE_FIELDS,
        "SCHEMA_VALIDATOR_DESIGN_16_SIDECAR_DEFERRED": classification["observability_sidecar_deferred"] is True,
        "SCHEMA_VALIDATOR_DESIGN_17_BUILD_TARGET_EMITTED": BUILD_TARGET_PATH.exists() and build_target["build_target_status"] == "BUILD_READY",
        "SCHEMA_VALIDATOR_DESIGN_18_NO_SCHEMA_VALIDATOR_BUILD": rollup["schema_validator_build_count"] == 0,
        "SCHEMA_VALIDATOR_DESIGN_19_NO_SIDECAR_DESIGN_OR_BUILD": rollup["observability_sidecar_design_count"] == 0 and rollup["observability_sidecar_build_count"] == 0,
        "SCHEMA_VALIDATOR_DESIGN_20_NO_AUTHORITY_OR_ADMISSIBILITY_CHECK": classification["authority_checked"] is False and classification["admissibility_checked"] is False,
        "SCHEMA_VALIDATOR_DESIGN_21_NO_EXECUTION_OR_REPAIR": classification["execution_claimed"] is False and classification["proposal_repaired"] is False,
        "SCHEMA_VALIDATOR_DESIGN_22_NO_SCHEMA_ARCHIVE_MUTATION_OR_CREATION": classification["schema_archive_mutated"] is False and classification["schema_created"] is False,
        "SCHEMA_VALIDATOR_DESIGN_23_NO_BUILDER_COMMAND": classification["builder_command_emitted"] is False,
        "SCHEMA_VALIDATOR_DESIGN_24_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "SCHEMA_VALIDATOR_DESIGN_25_NO_LIVE_RUNTIME_ROUTING": classification["live_runtime_routing_installed"] is False,
        "SCHEMA_VALIDATOR_DESIGN_26_NO_C7_OR_C8": classification["c7_authorized"] is False and classification["c8_authorized"] is False,
        "SCHEMA_VALIDATOR_DESIGN_27_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "SCHEMA_VALIDATOR_DESIGN_28_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["observability_reference_mutated"] is False,
        "SCHEMA_VALIDATOR_DESIGN_29_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "SCHEMA_VALIDATOR_DESIGN_30_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "SCHEMA_VALIDATOR_DESIGN_31_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "SCHEMA_VALIDATOR_DESIGN_32_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_DESIGN_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_DESIGN_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_DESIGN_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_decision": SOURCE_POST_EDGE_DECISION_RECEIPT_ID,
        "recommended_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "runtime_schema_validator_cell_target_design_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_TARGET_DESIGN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_post_edge_observability_reference_decision_receipt_id": SOURCE_POST_EDGE_DECISION_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "machine_readable_runtime_schema_validator_cell_design_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "runtime_schema_validator_cell_target_designed": gate == "PASS",
            "schema_validator_build_ready": gate == "PASS",
            "future_build_unit": final_next,
            "source_post_edge_decision_consumed": True,
            "source_observability_reference_consumed": True,
            "formation_only_boundary_defined": True,
            "validate_classify_terminology_locked": True,
            "failure_precedence_locked": True,
            "formation_check_count": len(FORMATION_CHECKS),
            "result_enum_count": len(RESULT_ENUM),
            "demo_case_count": len(DEMO_CASES),
            "acceptance_gate_count": acceptance_gates["gate_count"],
            "negative_control_count": negative_controls["negative_control_count"],
            "observability_required_edge_field_count": len(REQUIRED_EDGE_FIELDS),
            "observability_sidecar_deferred": True,
            "unit_feedback_hardening_deferred": True,
            "c7_deferred": True,
            "c8_deferred": True,
            "runtime_adoption_deferred": True,
            "runtime_effect": False,
            "runtime_patched": False,
            "live_runtime_routing_installed": False,
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
            "observability_reference_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": True,
            "recommended_next": final_next,
        },
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "design_basis": rel(DESIGN_BASIS_PATH),
            "source_decision_review": rel(SOURCE_DECISION_REVIEW_PATH),
            "source_observability_reference_review": rel(SOURCE_OBSERVABILITY_REFERENCE_REVIEW_PATH),
            "target_spec": rel(TARGET_SPEC_PATH),
            "formation_check_table": rel(FORMATION_CHECK_TABLE_PATH),
            "failure_precedence": rel(FAILURE_PRECEDENCE_PATH),
            "result_enum_target": rel(RESULT_ENUM_TARGET_PATH),
            "result_schema_target": rel(RESULT_SCHEMA_TARGET_PATH),
            "validated_packet_target": rel(VALIDATED_PACKET_TARGET_PATH),
            "schema_feedback_target": rel(SCHEMA_FEEDBACK_TARGET_PATH),
            "schema_gap_feedback_target": rel(SCHEMA_GAP_FEEDBACK_TARGET_PATH),
            "receipt_schema_target": rel(RECEIPT_SCHEMA_TARGET_PATH),
            "demo_case_plan": rel(DEMO_CASE_PLAN_PATH),
            "acceptance_gates": rel(ACCEPTANCE_GATES_PATH),
            "negative_controls": rel(NEGATIVE_CONTROLS_PATH),
            "sidecar_dependency_park": rel(SIDECAR_DEPENDENCY_PARK_PATH),
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
    print(f"runtime_schema_validator_cell_design_receipt_id={receipt_id}")
    print(f"runtime_schema_validator_cell_design_receipt_path={rel(receipt_path)}")
    print(f"runtime_schema_validator_cell_target_spec_path={rel(TARGET_SPEC_PATH)}")
    print(f"runtime_schema_validator_cell_build_target_path={rel(BUILD_TARGET_PATH)}")
    print(f"runtime_schema_validator_cell_design_rollup_path={rel(ROLLUP_PATH)}")
    print(f"runtime_schema_validator_cell_design_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
