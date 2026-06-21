#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

SOURCE_SURFACE_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_validation_surfaces"
SOURCE_SURFACE_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_validation_surface_receipts"
SOURCE_SURFACE_POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_validation_surface_policies"
SOURCE_SURFACE_POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_validation_surface_policy_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_policy_receipts"

EXPECTED_SOURCE_SURFACE_ID = "40e5f5b4"
EXPECTED_SOURCE_SURFACE_RECEIPT_ID = "065849ef"
EXPECTED_SOURCE_SURFACE_POLICY_ID = "7050f196"
EXPECTED_SOURCE_SURFACE_POLICY_RECEIPT_ID = "2c061175"

POLICY_NAME = "BUILD_PROPOSE_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_POLICY_V0"
PROPOSAL_NAME = "PROPOSE_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_V0"
NEXT_COMMAND_GOAL = "EMIT_PROPOSE_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_V0"

CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
TRIGGER_HALT = "HOLD_NEW_BOUNDED_SURFACE_REQUIRES_RUNNER_DECISION"
SELECTED_ENCODING_ID = "raw_decimal_sig6"
TARGET_RAW_DELTA_FIELD = "compression_ratio"

CANDIDATE_PAYLOAD_FIELDS = [
    "cv",
    "state_hash_before",
    "move_id",
    "state_hash_after",
    "raw_compression_ratio_sig6",
]

FORBIDDEN_EFFECTS = [
    "execution",
    "runner_execution",
    "candidate_rows_creation",
    "registry_insertion",
    "candidate_acceptance",
    "scale_mode_authorization",
    "runtime_semantic_change",
    "runtime_code_change",
    "runtime_receipt_emission_change",
    "registry_sqlite_read",
    "full_registry_scan",
    "latest_file_resolution",
    "mtime_selection",
    "ambient_workspace_inference",
    "case_id_or_cycle_n_identity_patch",
    "rowid_or_receipt_hash_truth_surface",
    "full_occurrence_key_in_signature_payload",
    "audit_or_debug_payload_in_signature_payload",
    "synthetic_fake_validation_rows",
    "transition_compression_probe",
]

FORBIDDEN_AUTHORITY_FLAGS = [
    "authorizes_proposal_execution",
    "authorizes_runner_execution",
    "authorizes_candidate_rows_creation",
    "authorizes_candidate_acceptance",
    "authorizes_scale_mode",
    "authorizes_registry_insertion",
    "authorizes_registry_sqlite_read",
    "authorizes_full_registry_scan",
    "authorizes_runtime_semantic_change",
    "authorizes_runtime_code_change",
    "authorizes_runtime_receipt_emission_change",
    "authorizes_registry_write",
    "authorizes_latest_or_mtime_selection",
    "authorizes_ambient_workspace_inference",
    "authorizes_case_id_or_cycle_n_primary_identity_patch",
    "authorizes_rowid_or_receipt_hash_truth_surface",
    "authorizes_full_occurrence_key_in_payload",
    "authorizes_audit_pointer_in_payload",
    "authorizes_debug_payload_in_payload",
    "authorizes_microhash_as_proof",
    "authorizes_synthetic_fake_validation_rows",
    "authorizes_transition_compression_probe",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def sha8(obj: Any) -> str:
    return hashlib.sha256(blob(obj)).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required file: {path}")
    return json.loads(path.read_text())


def verify_source(
    source_surface: dict[str, Any],
    source_receipt: dict[str, Any],
    source_policy: dict[str, Any],
    source_policy_receipt: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if source_surface.get("surface_id") != EXPECTED_SOURCE_SURFACE_ID:
        failures.append(f"source_surface_id_wrong:{source_surface.get('surface_id')}")
    if source_receipt.get("receipt_id") != EXPECTED_SOURCE_SURFACE_RECEIPT_ID:
        failures.append(f"source_receipt_id_wrong:{source_receipt.get('receipt_id')}")
    if source_surface.get("gate") != "PASS":
        failures.append(f"source_surface_gate_not_PASS:{source_surface.get('gate')}")
    if source_receipt.get("gate") != "PASS":
        failures.append(f"source_receipt_gate_not_PASS:{source_receipt.get('gate')}")
    if source_surface.get("mode") != "OUTER_OBSERVER_ONLY":
        failures.append(f"source_mode_wrong:{source_surface.get('mode')}")
    if source_surface.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"source_candidate_design_wrong:{source_surface.get('candidate_design_id')}")
    if source_surface.get("source_policy_id") != EXPECTED_SOURCE_SURFACE_POLICY_ID:
        failures.append(f"source_policy_ref_wrong:{source_surface.get('source_policy_id')}")
    if source_surface.get("source_policy_receipt_id") != EXPECTED_SOURCE_SURFACE_POLICY_RECEIPT_ID:
        failures.append(f"source_policy_receipt_ref_wrong:{source_surface.get('source_policy_receipt_id')}")

    if source_surface.get("terminal_class") != TRIGGER_HALT:
        failures.append(f"source_terminal_class_wrong:{source_surface.get('terminal_class')}")
    terminal = source_surface.get("terminal") or {}
    if terminal.get("type") != "HOLD":
        failures.append(f"source_terminal_type_wrong:{terminal.get('type')}")
    if terminal.get("stop_code") != TRIGGER_HALT:
        failures.append(f"source_stop_code_wrong:{terminal.get('stop_code')}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"source_next_goal_not_none:{terminal.get('next_command_goal')}")

    decision = source_surface.get("decision") or {}
    expected_true = [
        "new_surface_attempted",
        "runner_discovery_completed",
        "do_not_accept_candidate",
        "do_not_full_registry_scan",
        "do_not_read_registry_sqlite",
        "do_not_change_runtime",
        "do_not_change_runtime_code",
        "do_not_write_registry",
        "do_not_use_case_id_or_cycle_n_as_primary_identity",
        "do_not_use_rowid_or_receipt_hash",
    ]
    for key in expected_true:
        if decision.get(key) is not True:
            failures.append(f"source_decision_flag_not_true:{key}:{decision.get(key)}")

    expected_false = [
        "candidate_accepted",
        "candidate_acceptance_authorized",
        "scale_mode_authorized",
        "new_surface_created",
        "safe_runner_recipe_found",
    ]
    for key in expected_false:
        if decision.get(key) is not False:
            failures.append(f"source_decision_flag_not_false:{key}:{decision.get(key)}")

    if decision.get("terminal_class") != TRIGGER_HALT:
        failures.append(f"source_decision_terminal_wrong:{decision.get('terminal_class')}")

    discovery = source_receipt.get("runner_discovery_summary") or {}
    if discovery.get("safe_recipe_candidates_total") != 0:
        failures.append(f"safe_recipe_candidates_not_zero:{discovery.get('safe_recipe_candidates_total')}")
    if not isinstance(discovery.get("runner_candidates_total"), int):
        failures.append(f"runner_candidates_total_missing:{discovery.get('runner_candidates_total')}")
    if not isinstance(discovery.get("files_discovered_total"), int):
        failures.append(f"files_discovered_total_missing:{discovery.get('files_discovered_total')}")
    if discovery.get("registry_sqlite_read") is not False:
        failures.append(f"discovery_registry_sqlite_read_not_false:{discovery.get('registry_sqlite_read')}")
    if discovery.get("full_registry_scan_used") is not False:
        failures.append(f"discovery_full_scan_not_false:{discovery.get('full_registry_scan_used')}")
    if discovery.get("runtime_code_changed") is not False:
        failures.append(f"discovery_runtime_code_changed_not_false:{discovery.get('runtime_code_changed')}")

    recipe = source_receipt.get("surface_recipe_or_hold") or {}
    if recipe.get("recipe_status") != "HOLD_NO_SAFE_EXISTING_RECIPE":
        failures.append(f"recipe_status_wrong:{recipe.get('recipe_status')}")
    if recipe.get("safe_recipe_candidates_total") != 0:
        failures.append(f"recipe_safe_candidates_not_zero:{recipe.get('safe_recipe_candidates_total')}")
    if recipe.get("safe_recipe_selected") is not None:
        failures.append(f"recipe_safe_selected_not_none:{recipe.get('safe_recipe_selected')}")
    if recipe.get("command_or_recipe") is not None:
        failures.append(f"recipe_command_not_none:{recipe.get('command_or_recipe')}")

    rows_summary = source_receipt.get("surface_rows_summary") or {}
    for key in [
        "rows_created",
        "new_bands_created",
        "candidate_compatible_rows_created",
        "synthetic_fake_rows_created",
    ]:
        if rows_summary.get(key) != 0:
            failures.append(f"rows_summary_{key}_not_zero:{rows_summary.get(key)}")

    guards = source_receipt.get("authority_guards") or {}
    if guards.get("observer_only") is not True:
        failures.append("source_not_observer_only")
    for key in [
        "candidate_accepted",
        "candidate_acceptance_authorized",
        "scale_mode_authorized",
        "full_registry_scan_used",
        "registry_sqlite_read",
        "registry_sqlite_changed",
        "runtime_receipt_emission_changed",
        "runtime_code_changed",
        "registry_write_authorized",
        "receipt_replacement_authorized",
        "receipt_deletion_authorized",
        "receipt_compression_authorized",
        "receipt_suppression_authorized",
        "raw_receipt_hash_used_as_truth_surface",
        "case_id_or_cycle_n_primary_identity_patch_used",
        "rowid_or_receipt_hash_patch_used",
        "full_occurrence_key_in_payload",
        "audit_pointer_in_payload",
        "debug_payload_in_payload",
        "microhash_as_proof_used",
        "synthetic_fake_validation_rows_used",
    ]:
        if guards.get(key) is not False:
            failures.append(f"source_guard_not_false:{key}:{guards.get(key)}")

    pass_gates = source_receipt.get("pass_gates") or {}
    for key in [
        "policy_preconditions",
        "authority_containment",
        "runner_discovery_recorded",
        "surface_recipe_or_hold_recorded",
        "bounded_limits_recorded",
        "candidate_not_accepted",
        "scale_mode_not_authorized",
        "registry_sqlite_not_read",
        "full_registry_not_scanned",
        "runtime_code_not_changed",
        "runtime_receipt_emission_not_changed",
        "synthetic_rows_not_created",
        "truth_surface_preserved",
        "payload_contract_preserved",
        "hold_is_lawful_if_no_safe_recipe",
    ]:
        if pass_gates.get(key) is not True:
            failures.append(f"source_pass_gate_not_true:{key}:{pass_gates.get(key)}")

    if source_policy.get("policy_id") != EXPECTED_SOURCE_SURFACE_POLICY_ID:
        failures.append(f"source_policy_id_wrong:{source_policy.get('policy_id')}")
    if source_policy_receipt.get("receipt_id") != EXPECTED_SOURCE_SURFACE_POLICY_RECEIPT_ID:
        failures.append(f"source_policy_receipt_id_wrong:{source_policy_receipt.get('receipt_id')}")
    if source_policy.get("gate") != "PASS":
        failures.append(f"source_policy_gate_not_PASS:{source_policy.get('gate')}")
    if source_policy.get("terminal", {}).get("next_command_goal") != "IMPLEMENT_RAW_DELTA_SIGNATURE_CANDIDATE_NEW_BOUNDED_VALIDATION_SURFACE_V0":
        failures.append(f"source_policy_next_goal_wrong:{source_policy.get('terminal', {}).get('next_command_goal')}")

    return failures


def build_policy(source_surface_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_surface = load_json(SOURCE_SURFACE_DIR / f"{source_surface_id}.json")
    source_receipt = load_json(SOURCE_SURFACE_RECEIPT_DIR / f"{source_surface_id}.json")
    source_policy = load_json(SOURCE_SURFACE_POLICY_DIR / f"{EXPECTED_SOURCE_SURFACE_POLICY_ID}.json")
    source_policy_receipt = load_json(SOURCE_SURFACE_POLICY_RECEIPT_DIR / f"{EXPECTED_SOURCE_SURFACE_POLICY_ID}.json")

    failures = verify_source(source_surface, source_receipt, source_policy, source_policy_receipt)

    proposal_contract = {
        "proposal_name": PROPOSAL_NAME,
        "proposal_status_if_emitted": "PROPOSED_UNAUTHORIZED",
        "decision_status_if_emitted": "HUMAN_BOUNDARY_PENDING",
        "trigger_halt": TRIGGER_HALT,
        "valid_against": {
            "surface_id": EXPECTED_SOURCE_SURFACE_ID,
            "receipt_id": EXPECTED_SOURCE_SURFACE_RECEIPT_ID,
            "policy_id": EXPECTED_SOURCE_SURFACE_POLICY_ID,
            "policy_receipt_id": EXPECTED_SOURCE_SURFACE_POLICY_RECEIPT_ID,
            "candidate_design_id": CANDIDATE_DESIGN_ID,
            "selected_encoding_id": SELECTED_ENCODING_ID,
            "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
        },
        "current_blocker": (
            "No safe explicit recipe exists for producing RAW_DELTA_SIGNATURE_CANDIDATE_V0-compatible rows "
            "on a fresh bounded validation surface."
        ),
        "proposal_class": "POLICY_BOUNDARY_CANDIDATE",
        "authority_impact": "REQUIRES_HUMAN_BOUNDARY",
        "human_decision_requested": ["APPROVE", "REJECT", "NARROW", "RETYPE", "DEFER"],
        "recommended_default": {
            "option_id": "OPTION_A_NARROWED",
            "status": "RECOMMENDED_NON_AUTHORIZING",
            "claim": (
                "Use existing MatrixLab CLI/run machinery only to create a small fresh bounded run, then use an "
                "observer-only extractor to emit candidate-compatible rows. This is only a proposal and does not "
                "authorize execution."
            ),
        },
        "candidate_recipe_options": [
            {
                "option_id": "OPTION_A_NARROWED",
                "name": "existing_cli_fresh_run_plus_observer_extractor",
                "description": (
                    "Use an existing bounded CLI runner to create fresh receipts, then run an observer-only extractor "
                    "that converts those receipts into RAW_DELTA_SIGNATURE_CANDIDATE_V0-compatible rows."
                ),
                "minimum_required_fields": [
                    "runner_command",
                    "families",
                    "cases_or_depths",
                    "cycles",
                    "max_cells",
                    "receipt_outputs",
                    "extractor_inputs",
                    "candidate_row_schema",
                    "bounds",
                    "gate",
                ],
                "default_bounds": {
                    "max_new_runs": 1,
                    "max_new_cases_total": 10,
                    "max_cycles_per_case": 50,
                    "max_candidate_rows": 10000,
                    "max_new_bands": 512,
                    "max_output_files": 16,
                },
                "allowed_effects_if_later_approved": [
                    "run_existing_bounded_cli_or_script",
                    "write_observer_only_surface_rows",
                    "write_surface_manifest",
                    "write_surface_receipt",
                ],
                "forbidden_effects": FORBIDDEN_EFFECTS,
            },
            {
                "option_id": "OPTION_B_EXISTING_RECEIPT_SURFACE_EXTRACTOR",
                "name": "existing_receipt_surface_plus_stricter_observer_extractor",
                "description": (
                    "Do not run a new simulation. Define a stricter extractor recipe over a named existing receipt family "
                    "that was not previously candidate-compatible."
                ),
                "minimum_required_fields": [
                    "explicit_source_surface_ref",
                    "no_latest_or_mtime_selection",
                    "extractor_inputs",
                    "candidate_row_schema",
                    "bounds",
                    "gate",
                ],
                "allowed_effects_if_later_approved": [
                    "read_explicit_file_backed_surface",
                    "write_observer_only_surface_rows",
                    "write_surface_manifest",
                    "write_surface_receipt",
                ],
                "forbidden_effects": FORBIDDEN_EFFECTS,
            },
            {
                "option_id": "OPTION_C_DEFINE_FIXTURE_RADIUS_DEPTH_RECIPE_FIRST",
                "name": "define_new_bounded_fixture_radius_depth_recipe_first",
                "description": (
                    "Before running anything, define a new bounded fixture/radius/depth surface as an explicit recipe artifact."
                ),
                "minimum_required_fields": [
                    "fixture_family",
                    "radius_or_depth_bounds",
                    "cycles",
                    "case_count",
                    "max_cells",
                    "expected_receipt_surface",
                    "candidate_row_schema",
                    "gate",
                ],
                "allowed_effects_if_later_approved": [
                    "write_recipe_artifact",
                    "write_recipe_receipt",
                ],
                "forbidden_effects": FORBIDDEN_EFFECTS,
            },
            {
                "option_id": "OPTION_D_DEFER_GENERIC_PROCEED_HALT_PROPOSAL_RUNNER",
                "name": "defer_and_build_generic_local_unit_runner_spine",
                "description": (
                    "Pause MatrixLab candidate validation and build the generic local proceed/halt/proposal runner spine."
                ),
                "minimum_required_fields": [
                    "schema_pack",
                    "trace_receipt_writer",
                    "preflight_validator",
                    "minimal_unit_runner",
                    "post_halt_proposal_writer",
                ],
                "allowed_effects_if_later_approved": [
                    "build_generic_local_runner_infra",
                ],
                "forbidden_effects": FORBIDDEN_EFFECTS + [
                    "MatrixLab_candidate_validation_execution",
                ],
            },
        ],
        "proposal_gate": {
            "requires_trigger_halt": True,
            "requires_trigger_receipt": True,
            "requires_valid_against_surface_lock": True,
            "requires_current_blocker": True,
            "requires_candidate_recipe_options": True,
            "requires_recommended_option_non_authorizing": True,
            "requires_authority_impact": True,
            "requires_forbidden_effects": True,
            "requires_required_receipt_if_approved": True,
            "requires_human_decision_request": True,
            "proposal_must_not_execute": True,
            "proposal_must_not_register": True,
            "proposal_must_not_accept": True,
            "proposal_must_not_patch": True,
            "proposal_must_not_authorize_itself": True,
        },
        "required_receipt_if_emitted": {
            "receipt_type": "PROPOSAL_EMISSION_RECEIPT",
            "must_record": [
                "proposal_id",
                "proposal_status",
                "decision_status",
                "trigger_surface_id",
                "trigger_receipt_id",
                "trigger_halt",
                "current_blocker",
                "candidate_recipe_options",
                "recommended_option",
                "authority_impact",
                "forbidden_effects",
                "required_receipt_if_approved",
                "human_decision_requested",
                "gate",
            ],
        },
        "required_receipt_if_approved_later": {
            "receipt_type": "APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_RECEIPT",
            "approval_does_not_execute": True,
            "approval_does_not_insert_registry": True,
            "approval_does_not_accept_candidate": True,
            "next_policy_after_approval": "BUILD_APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_POLICY_V0",
        },
        "post_proposal_next_steps": {
            "if_proposal_emitted": "HUMAN_DECISION_RECORD_V0",
            "if_proposal_fails": "DIAGNOSE_RECIPE_PROPOSAL_POLICY_FAILURE_V0",
        },
    }

    authority = {
        "observer_only": True,
        "authorizes_proposal_emission": True,
        "authorized_next_command_goal": NEXT_COMMAND_GOAL,
        "authorizes_human_boundary_request": True,
        "authorizes_recipe_options_listing": True,
        "authorizes_recommended_option_label": True,
        "authorizes_required_receipt_specification": True,
    }
    for key in FORBIDDEN_AUTHORITY_FLAGS:
        authority[key] = False

    implementation_constraints = {
        "must_touch_only_files": [
            "scripts/emit_propose_new_bounded_validation_surface_recipe_v0.py",
        ],
        "must_not_modify_files": [
            "src/",
            "app/",
            "matrixlab/",
            "scripts/raw_delta_signature_candidate_new_bounded_validation_surface_v0.py",
            "scripts/build_raw_delta_signature_candidate_new_bounded_validation_surface_policy_v0.py",
            "scripts/raw_delta_signature_candidate_bounded_scale_out_v0.py",
            "scripts/build_raw_delta_signature_candidate_bounded_scale_out_policy_v0.py",
            "scripts/raw_delta_signature_candidate_scale_review_v0.py",
            "scripts/build_raw_delta_signature_candidate_scale_review_policy_v0.py",
            "scripts/raw_delta_signature_candidate_probe_v0.py",
            "scripts/build_raw_delta_signature_candidate_policy_v0.py",
            "scripts/raw_delta_compactness_diagnostic_v0.py",
            "scripts/build_raw_delta_compactness_diagnostic_policy_v0.py",
            "scripts/stable_delta_signature_candidate_v0_3_probe.py",
            "scripts/diagnose_v0_3_failure_v0.py",
            "scripts/stable_delta_signature_candidate_v0_2_scale_band_probe.py",
            "scripts/stable_delta_signature_candidate_v0_2_probe.py",
        ],
        "must_start_from_hold_surface": EXPECTED_SOURCE_SURFACE_ID,
        "must_lock_valid_against_surface": True,
        "must_emit_proposed_unauthorized_only": True,
        "must_set_decision_status_human_boundary_pending": True,
        "must_not_execute_runner": True,
        "must_not_create_candidate_rows": True,
        "must_not_accept_candidate": True,
        "must_not_insert_registry": True,
        "must_not_read_registry_sqlite": True,
        "must_not_full_registry_scan": True,
        "must_not_use_latest_or_mtime_selection": True,
        "must_not_change_runtime": True,
        "must_not_change_runtime_code": True,
        "must_not_change_runtime_receipt_emission": True,
        "must_not_write_registry": True,
    }

    required_negative_controls = [
        {
            "case": "proposal_execution_authority_fail",
            "must_fail_if": "proposal emission policy authorizes execution or runner execution",
        },
        {
            "case": "candidate_acceptance_fail",
            "must_fail_if": "candidate acceptance or scale mode is authorized",
        },
        {
            "case": "registry_or_runtime_fail",
            "must_fail_if": "registry write/read, full scan, runtime mutation, or runtime receipt emission change is authorized",
        },
        {
            "case": "latest_mtime_fail",
            "must_fail_if": "latest/mtime/ambient workspace authority is authorized",
        },
        {
            "case": "source_not_hold_fail",
            "must_fail_if": "source surface is not HOLD_NEW_BOUNDED_SURFACE_REQUIRES_RUNNER_DECISION",
        },
        {
            "case": "safe_recipe_already_exists_fail",
            "must_fail_if": "source surface reports safe explicit recipe candidates already exist",
        },
        {
            "case": "proposal_status_wrong_fail",
            "must_fail_if": "proposal status is not PROPOSED_UNAUTHORIZED with HUMAN_BOUNDARY_PENDING",
        },
    ]

    policy = {
        "schema_version": "raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "proposal_name": PROPOSAL_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_surface_id": EXPECTED_SOURCE_SURFACE_ID,
        "source_surface_receipt_id": EXPECTED_SOURCE_SURFACE_RECEIPT_ID,
        "source_surface_policy_id": EXPECTED_SOURCE_SURFACE_POLICY_ID,
        "source_surface_policy_receipt_id": EXPECTED_SOURCE_SURFACE_POLICY_RECEIPT_ID,
        "trigger_halt": TRIGGER_HALT,
        "proposal_contract": proposal_contract,
        "authority": authority,
        "implementation_constraints": implementation_constraints,
        "required_negative_controls": required_negative_controls,
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_PROPOSE_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_POLICY_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    policy_id = sha8({
        "policy_name": POLICY_NAME,
        "proposal_name": PROPOSAL_NAME,
        "source_surface_id": EXPECTED_SOURCE_SURFACE_ID,
        "trigger_halt": TRIGGER_HALT,
        "proposal_contract": proposal_contract,
        "authority": authority,
        "implementation_constraints": implementation_constraints,
    })
    policy["policy_id"] = policy_id
    policy["policy_sig8"] = policy_id

    receipt = {
        "schema_version": "raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_policy_receipt_v0",
        "policy_id": policy_id,
        "policy_sig8": policy_id,
        "policy_name": POLICY_NAME,
        "policy_status": policy["policy_status"],
        "proposal_name": PROPOSAL_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "policy_path": f"data/raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_policies/{policy_id}.json",
        "source_surface_id": EXPECTED_SOURCE_SURFACE_ID,
        "source_surface_receipt_id": EXPECTED_SOURCE_SURFACE_RECEIPT_ID,
        "source_surface_policy_id": EXPECTED_SOURCE_SURFACE_POLICY_ID,
        "source_surface_policy_receipt_id": EXPECTED_SOURCE_SURFACE_POLICY_RECEIPT_ID,
        "trigger_halt": TRIGGER_HALT,
        "proposal_contract_summary": {
            "proposal_status_if_emitted": "PROPOSED_UNAUTHORIZED",
            "decision_status_if_emitted": "HUMAN_BOUNDARY_PENDING",
            "current_blocker": proposal_contract["current_blocker"],
            "proposal_class": "POLICY_BOUNDARY_CANDIDATE",
            "authority_impact": "REQUIRES_HUMAN_BOUNDARY",
            "recommended_option": "OPTION_A_NARROWED",
            "candidate_recipe_options": [
                option["option_id"] for option in proposal_contract["candidate_recipe_options"]
            ],
            "proposal_execution_forbidden": True,
            "runner_execution_forbidden": True,
            "candidate_rows_creation_forbidden": True,
            "candidate_acceptance_forbidden": True,
            "registry_insertion_forbidden": True,
            "registry_sqlite_read_forbidden": True,
            "full_registry_scan_forbidden": True,
            "runtime_change_forbidden": True,
            "latest_mtime_guessing_forbidden": True,
        },
        "authority": authority,
        "implementation_constraints": implementation_constraints,
        "terminal": policy["terminal"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    (OUT_DIR / f"{policy_id}.json").write_text(json.dumps(policy, indent=2, sort_keys=True))
    (OUT_RECEIPT_DIR / f"{policy_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return policy, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-surface-id", default=EXPECTED_SOURCE_SURFACE_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.source_surface_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_json_path=data/raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
