#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

DECISION_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_human_decisions"
DECISION_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_human_decision_receipts"

PROPOSAL_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_proposals"
PROPOSAL_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_recipe_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_approved_new_bounded_surface_recipe_policy_receipts"

EXPECTED_DECISION_ID = "55b293ef"
EXPECTED_DECISION_RECEIPT_ID = "6dc33fbd"
EXPECTED_PROPOSAL_ID = "71f1a3f0"
EXPECTED_PROPOSAL_RECEIPT_ID = "d8a7686c"

POLICY_NAME = "APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_POLICY_V0"
BUILDER_GOAL = "BUILD_APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_POLICY_V0"
NEXT_COMMAND_GOAL = "IMPLEMENT_APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_V0"

CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
SELECTED_OPTION_ID = "OPTION_A_NARROWED"
TRIGGER_HALT = "HOLD_NEW_BOUNDED_SURFACE_REQUIRES_RUNNER_DECISION"

APPROVED_BOUNDS = {
    "max_new_runs": 1,
    "max_new_cases_total": 10,
    "max_cycles_per_case": 50,
    "max_candidate_rows": 10000,
    "max_new_bands": 512,
    "max_output_files": 16,
}

VALID_AGAINST = {
    "surface_id": "40e5f5b4",
    "receipt_id": "065849ef",
    "policy_id": "7050f196",
    "policy_receipt_id": "2c061175",
    "candidate_design_id": CANDIDATE_DESIGN_ID,
    "selected_encoding_id": "raw_decimal_sig6",
    "selected_target_raw_delta_field": "compression_ratio",
}

PAYLOAD_FIELDS = [
    "cv",
    "state_hash_before",
    "move_id",
    "state_hash_after",
    "raw_compression_ratio_sig6",
]

FORBIDDEN_NOW = [
    "runner_execution_now",
    "candidate_rows_creation_now",
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

FORBIDDEN_NEXT_IMPLEMENTATION = [
    "candidate_acceptance",
    "scale_mode_authorization",
    "registry_insertion",
    "registry_write",
    "registry_sqlite_read",
    "full_registry_scan",
    "runtime_semantic_change",
    "runtime_code_change",
    "runtime_receipt_emission_change",
    "latest_file_resolution",
    "mtime_selection",
    "ambient_workspace_inference",
    "case_id_or_cycle_n_identity_patch",
    "rowid_or_receipt_hash_truth_surface",
    "full_occurrence_key_in_signature_payload",
    "audit_or_debug_payload_in_signature_payload",
    "synthetic_fake_validation_rows",
    "transition_compression_probe",
    "receipt_replacement",
    "receipt_deletion",
    "receipt_suppression",
    "candidate_acceptance_via_recipe_success",
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


def verify_decision_and_proposal(
    decision: dict[str, Any],
    decision_receipt: dict[str, Any],
    proposal: dict[str, Any],
    proposal_receipt: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if decision.get("decision_id") != EXPECTED_DECISION_ID:
        failures.append(f"decision_id_wrong:{decision.get('decision_id')}")
    if decision_receipt.get("receipt_id") != EXPECTED_DECISION_RECEIPT_ID:
        failures.append(f"decision_receipt_id_wrong:{decision_receipt.get('receipt_id')}")
    if decision_receipt.get("decision_id") != EXPECTED_DECISION_ID:
        failures.append(f"decision_receipt_decision_id_wrong:{decision_receipt.get('decision_id')}")

    if proposal.get("proposal_id") != EXPECTED_PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal_receipt.get("receipt_id") != EXPECTED_PROPOSAL_RECEIPT_ID:
        failures.append(f"proposal_receipt_id_wrong:{proposal_receipt.get('receipt_id')}")
    if proposal_receipt.get("proposal_id") != EXPECTED_PROPOSAL_ID:
        failures.append(f"proposal_receipt_proposal_id_wrong:{proposal_receipt.get('proposal_id')}")

    if decision.get("gate") != "PASS":
        failures.append(f"decision_gate_not_PASS:{decision.get('gate')}")
    if decision_receipt.get("gate") != "PASS":
        failures.append(f"decision_receipt_gate_not_PASS:{decision_receipt.get('gate')}")
    if proposal.get("gate") != "PASS":
        failures.append(f"proposal_gate_not_PASS:{proposal.get('gate')}")
    if proposal_receipt.get("gate") != "PASS":
        failures.append(f"proposal_receipt_gate_not_PASS:{proposal_receipt.get('gate')}")

    if decision.get("decision") != "APPROVE":
        failures.append(f"decision_not_APPROVE:{decision.get('decision')}")
    if decision.get("decision_status") != "APPROVED_SCOPED":
        failures.append(f"decision_status_wrong:{decision.get('decision_status')}")
    if decision.get("proposal_id") != EXPECTED_PROPOSAL_ID:
        failures.append(f"decision_proposal_id_wrong:{decision.get('proposal_id')}")
    if decision.get("proposal_receipt_id") != EXPECTED_PROPOSAL_RECEIPT_ID:
        failures.append(f"decision_proposal_receipt_id_wrong:{decision.get('proposal_receipt_id')}")
    if decision.get("valid_against") != VALID_AGAINST:
        failures.append(f"decision_valid_against_wrong:{decision.get('valid_against')}")

    decision_scope = decision.get("decision_scope") or {}
    if decision_scope.get("trigger_surface_id") != VALID_AGAINST["surface_id"]:
        failures.append(f"decision_scope_surface_wrong:{decision_scope.get('trigger_surface_id')}")
    if decision_scope.get("trigger_receipt_id") != VALID_AGAINST["receipt_id"]:
        failures.append(f"decision_scope_receipt_wrong:{decision_scope.get('trigger_receipt_id')}")
    if decision_scope.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"decision_scope_candidate_wrong:{decision_scope.get('candidate_design_id')}")

    approved_scope = decision.get("approved_recipe_scope") or {}
    if approved_scope.get("selected_option_id") != SELECTED_OPTION_ID:
        failures.append(f"selected_option_wrong:{approved_scope.get('selected_option_id')}")
    if approved_scope.get("approval_scope") != "RECIPE_SHAPE_ONLY_NOT_EXECUTION":
        failures.append(f"approval_scope_wrong:{approved_scope.get('approval_scope')}")
    if approved_scope.get("approved_bounds") != APPROVED_BOUNDS:
        failures.append(f"approved_bounds_wrong:{approved_scope.get('approved_bounds')}")
    for required in [
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
    ]:
        if required not in set(approved_scope.get("approved_required_fields") or []):
            failures.append(f"approved_required_field_missing:{required}")

    effects = decision.get("decision_effects") or {}
    if effects.get("authorizes_recipe_policy_build") is not True:
        failures.append(f"authorizes_recipe_policy_build_not_true:{effects.get('authorizes_recipe_policy_build')}")
    if effects.get("authorized_next_command_goal") != BUILDER_GOAL:
        failures.append(f"decision_next_goal_wrong:{effects.get('authorized_next_command_goal')}")
    if effects.get("approves_option_a_narrowed") is not True:
        failures.append(f"approves_option_a_not_true:{effects.get('approves_option_a_narrowed')}")
    if effects.get("approval_is_scoped_to_valid_against_surface") is not True:
        failures.append("approval_not_scoped")

    for key in [
        "approval_does_not_execute",
        "approval_does_not_run_runner",
        "approval_does_not_create_candidate_rows",
        "approval_does_not_accept_candidate",
        "approval_does_not_authorize_scale_mode",
        "approval_does_not_insert_registry",
        "approval_does_not_read_registry_sqlite",
        "approval_does_not_full_registry_scan",
        "approval_does_not_mutate_runtime",
        "approval_does_not_change_runtime_code",
        "approval_does_not_change_runtime_receipt_emission",
        "approval_does_not_use_latest_or_mtime_selection",
        "approval_does_not_use_case_id_or_cycle_n_identity_patch",
        "approval_does_not_use_rowid_or_receipt_hash_truth_surface",
        "approval_does_not_put_full_occurrence_key_in_payload",
        "approval_does_not_put_audit_or_debug_in_payload",
        "approval_does_not_create_synthetic_fake_rows",
        "approval_does_not_run_transition_compression_probe",
    ]:
        if effects.get(key) is not True:
            failures.append(f"decision_guard_not_true:{key}:{effects.get(key)}")

    required_next = decision.get("required_next_artifact") or {}
    if required_next.get("artifact_name") != "APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_POLICY_V0":
        failures.append(f"required_next_artifact_wrong:{required_next.get('artifact_name')}")
    if required_next.get("builder_goal") != BUILDER_GOAL:
        failures.append(f"required_next_builder_goal_wrong:{required_next.get('builder_goal')}")
    if required_next.get("must_include_bounds") != APPROVED_BOUNDS:
        failures.append(f"required_next_bounds_wrong:{required_next.get('must_include_bounds')}")
    for key in [
        "must_include_runner_command",
        "must_include_observer_extractor_contract",
        "must_include_candidate_row_schema",
        "must_include_no_latest_mtime_guard",
        "must_include_no_runtime_mutation_guard",
        "must_include_no_registry_sqlite_guard",
        "must_include_no_candidate_acceptance_guard",
    ]:
        if required_next.get(key) is not True:
            failures.append(f"required_next_guard_not_true:{key}:{required_next.get(key)}")

    terminal = decision.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"decision_terminal_type_wrong:{terminal.get('type')}")
    if terminal.get("next_command_goal") != BUILDER_GOAL:
        failures.append(f"decision_terminal_next_goal_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"decision_terminal_stop_not_none:{terminal.get('stop_code')}")

    if proposal.get("proposal_artifact_status") != "PROPOSED_UNAUTHORIZED":
        failures.append(f"proposal_status_wrong:{proposal.get('proposal_artifact_status')}")
    if proposal.get("decision_status") != "HUMAN_BOUNDARY_PENDING":
        failures.append(f"proposal_decision_status_wrong:{proposal.get('decision_status')}")
    if proposal.get("valid_against") != VALID_AGAINST:
        failures.append(f"proposal_valid_against_wrong:{proposal.get('valid_against')}")
    if proposal.get("recommended_default", {}).get("option_id") != SELECTED_OPTION_ID:
        failures.append(f"proposal_recommended_option_wrong:{proposal.get('recommended_default', {}).get('option_id')}")
    if proposal.get("recommended_default", {}).get("status") != "RECOMMENDED_NON_AUTHORIZING":
        failures.append(f"proposal_recommended_status_wrong:{proposal.get('recommended_default', {}).get('status')}")

    proposal_guards = proposal.get("authority_guards") or {}
    if proposal_guards.get("proposal_emitted") is not True:
        failures.append("proposal_not_emitted")
    for key in [
        "proposal_executed",
        "runner_executed",
        "candidate_rows_created",
        "candidate_accepted",
        "scale_mode_authorized",
        "registry_inserted",
        "registry_sqlite_read",
        "full_registry_scan_used",
        "runtime_semantic_changed",
        "runtime_code_changed",
        "runtime_receipt_emission_changed",
        "registry_write_authorized",
        "latest_or_mtime_selection_used",
        "ambient_workspace_inference_used",
        "case_id_or_cycle_n_identity_patch_used",
        "rowid_or_receipt_hash_truth_surface_used",
        "full_occurrence_key_in_signature_payload",
        "audit_or_debug_payload_in_signature_payload",
        "microhash_as_proof_used",
        "synthetic_fake_validation_rows_used",
        "transition_compression_probe_run",
    ]:
        if proposal_guards.get(key) is not False:
            failures.append(f"proposal_guard_not_false:{key}:{proposal_guards.get(key)}")

    return failures


def build_policy(decision_id: str, write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    decision = load_json(DECISION_DIR / f"{decision_id}.json")
    decision_receipt = load_json(DECISION_RECEIPT_DIR / f"{decision_id}.json")
    proposal = load_json(PROPOSAL_DIR / f"{EXPECTED_PROPOSAL_ID}.json")
    proposal_receipt = load_json(PROPOSAL_RECEIPT_DIR / f"{EXPECTED_PROPOSAL_ID}.json")

    failures = verify_decision_and_proposal(decision, decision_receipt, proposal, proposal_receipt)

    runner_recipe = {
        "runner_command_id": "EXISTING_MATRIXLAB_CLI_BOUNDED_RUN_V0",
        "runner_command": [
            "uv",
            "run",
            "python",
            "src/matrixlab/cli.py",
            "run",
            "--families",
            "projection_quotient",
            "--depth-min",
            "3",
            "--depth-max",
            "12",
            "--cycles-per-case",
            "50",
            "--max-cells",
            "50000",
        ],
        "runner_command_string": (
            "uv run python src/matrixlab/cli.py run "
            "--families projection_quotient "
            "--depth-min 3 --depth-max 12 "
            "--cycles-per-case 50 --max-cells 50000"
        ),
        "runner_command_status": "DECLARED_FOR_NEXT_IMPLEMENTATION_PRECHECK_REQUIRED",
        "runner_command_precheck_required": True,
        "if_runner_command_unavailable": "HOLD_APPROVED_RECIPE_RUNNER_COMMAND_UNAVAILABLE",
        "bounded_parameters": {
            "families": ["projection_quotient"],
            "depth_min": 3,
            "depth_max": 12,
            "case_count_expected_max": APPROVED_BOUNDS["max_new_cases_total"],
            "cycles_per_case": APPROVED_BOUNDS["max_cycles_per_case"],
            "max_cells": 50000,
            "max_new_runs": APPROVED_BOUNDS["max_new_runs"],
        },
        "stdout_contract": {
            "must_capture_run_id": True,
            "run_id_source": "runner_stdout_or_explicit_runner_receipt",
            "must_not_select_latest_by_mtime": True,
            "if_run_id_not_captured": "HOLD_APPROVED_RECIPE_RUN_ID_NOT_CAPTURED",
        },
    }

    observer_extractor_contract = {
        "extractor_name": "RAW_DELTA_SIGNATURE_CANDIDATE_NEW_BOUNDED_SURFACE_OBSERVER_EXTRACTOR_V0",
        "extractor_mode": "OUTER_OBSERVER_ONLY",
        "extractor_inputs": {
            "runner_run_id": "explicit_run_id_from_runner_output",
            "receipt_source": "file_backed_receipts_for_explicit_run_only",
            "forbidden_inputs": [
                "registry.sqlite",
                "full_registry_scan",
                "latest_file_by_mtime",
                "ambient_workspace_inventory",
                "synthetic_rows",
            ],
        },
        "candidate_row_schema": {
            "row_type": "RAW_DELTA_SIGNATURE_CANDIDATE_V0_ROW",
            "required_fields": [
                "row_id",
                "source_run_id",
                "source_receipt_ref",
                "full_occurrence_key",
                "candidate_delta_signature",
                "signature_payload",
                "truth_surface",
                "source_surface_id",
                "created_by",
            ],
            "signature_payload_fields": PAYLOAD_FIELDS,
            "truth_surface": "full_occurrence_key_to_candidate_delta_signature",
            "payload_forbidden_fields": [
                "case_id",
                "cycle_n",
                "rowid",
                "receipt_hash",
                "receipt_path",
                "audit_pointer",
                "debug_payload",
                "full_occurrence_key",
                "registry_rowid",
            ],
            "raw_delta_field": "compression_ratio",
            "raw_delta_encoding": "raw_decimal_sig6",
        },
        "candidate_signature_contract": {
            "candidate_delta_signature_fields": PAYLOAD_FIELDS,
            "must_preserve_transition_identity": True,
            "must_include_raw_compression_ratio_sig6": True,
            "must_not_include_debug_or_audit_fields": True,
            "must_not_include_full_occurrence_key": True,
            "must_not_use_microhash_as_proof": True,
        },
        "surface_outputs": {
            "surface_rows_dir": "data/raw_delta_signature_candidate_approved_new_bounded_surface_rows",
            "surface_manifest_dir": "data/raw_delta_signature_candidate_approved_new_bounded_surface_manifests",
            "surface_receipt_dir": "data/raw_delta_signature_candidate_approved_new_bounded_surface_receipts",
            "max_candidate_rows": APPROVED_BOUNDS["max_candidate_rows"],
            "max_new_bands": APPROVED_BOUNDS["max_new_bands"],
            "max_output_files": APPROVED_BOUNDS["max_output_files"],
        },
        "hold_conditions": [
            "HOLD_APPROVED_RECIPE_RUNNER_COMMAND_UNAVAILABLE",
            "HOLD_APPROVED_RECIPE_RUN_ID_NOT_CAPTURED",
            "HOLD_APPROVED_RECIPE_NO_FILE_BACKED_RECEIPTS",
            "HOLD_APPROVED_RECIPE_NO_CANDIDATE_COMPATIBLE_ROWS",
            "HOLD_APPROVED_RECIPE_ROWS_EXCEED_BOUND",
            "HOLD_APPROVED_RECIPE_AMBIGUOUS_SOURCE_SURFACE",
        ],
    }

    policy = {
        "schema_version": "raw_delta_signature_candidate_approved_new_bounded_surface_recipe_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_status": "POLICY_ONLY_APPROVED_RECIPE_NOT_EXECUTED",
        "builder_goal": BUILDER_GOAL,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_decision_id": EXPECTED_DECISION_ID,
        "source_decision_receipt_id": EXPECTED_DECISION_RECEIPT_ID,
        "source_proposal_id": EXPECTED_PROPOSAL_ID,
        "source_proposal_receipt_id": EXPECTED_PROPOSAL_RECEIPT_ID,
        "selected_option_id": SELECTED_OPTION_ID,
        "valid_against": VALID_AGAINST,
        "approved_bounds": APPROVED_BOUNDS,
        "recipe_contract": {
            "recipe_id": "OPTION_A_NARROWED_APPROVED_RECIPE_V0",
            "recipe_status": "APPROVED_FOR_POLICY_IMPLEMENTATION_NOT_EXECUTED",
            "recipe_shape": "existing_cli_fresh_run_plus_observer_extractor",
            "runner_recipe": runner_recipe,
            "observer_extractor_contract": observer_extractor_contract,
            "acceptance_scope": {
                "this_policy_may_authorize_next_implementation": True,
                "implementation_may_execute_runner_under_bounds": True,
                "implementation_may_write_observer_surface_rows": True,
                "implementation_may_write_surface_manifest": True,
                "implementation_may_write_surface_receipt": True,
                "implementation_must_not_accept_candidate": True,
                "implementation_must_not_scale": True,
                "implementation_must_not_write_registry": True,
                "implementation_must_not_change_runtime": True,
            },
        },
        "authority": {
            "observer_only_policy_build": True,
            "authorizes_next_implementation_policy": True,
            "authorized_next_command_goal": NEXT_COMMAND_GOAL,
            "authorizes_runner_command_precheck_in_next_implementation": True,
            "authorizes_existing_bounded_runner_execution_in_next_implementation_only": True,
            "authorizes_observer_extractor_in_next_implementation_only": True,
            "authorizes_candidate_row_write_in_next_implementation_only": True,
            "authorizes_surface_manifest_write_in_next_implementation_only": True,
            "authorizes_surface_receipt_write_in_next_implementation_only": True,
            "authorizes_runner_execution_now": False,
            "authorizes_candidate_rows_creation_now": False,
            "authorizes_candidate_acceptance": False,
            "authorizes_scale_mode": False,
            "authorizes_registry_insertion": False,
            "authorizes_registry_write": False,
            "authorizes_registry_sqlite_read": False,
            "authorizes_full_registry_scan": False,
            "authorizes_runtime_semantic_change": False,
            "authorizes_runtime_code_change": False,
            "authorizes_runtime_receipt_emission_change": False,
            "authorizes_latest_or_mtime_selection": False,
            "authorizes_ambient_workspace_inference": False,
            "authorizes_case_id_or_cycle_n_identity_patch": False,
            "authorizes_rowid_or_receipt_hash_truth_surface": False,
            "authorizes_full_occurrence_key_in_payload": False,
            "authorizes_audit_pointer_in_payload": False,
            "authorizes_debug_payload_in_payload": False,
            "authorizes_microhash_as_proof": False,
            "authorizes_synthetic_fake_validation_rows": False,
            "authorizes_transition_compression_probe": False,
        },
        "forbidden_effects_now": FORBIDDEN_NOW,
        "forbidden_effects_next_implementation": FORBIDDEN_NEXT_IMPLEMENTATION,
        "required_next_implementation_gates": {
            "must_compile": True,
            "must_precheck_runner_command": True,
            "must_execute_at_most_one_new_run": True,
            "must_capture_explicit_run_id": True,
            "must_read_only_explicit_run_receipts": True,
            "must_write_candidate_rows_under_bound": True,
            "must_emit_surface_manifest": True,
            "must_emit_surface_receipt": True,
            "must_not_use_latest_or_mtime": True,
            "must_not_read_registry_sqlite": True,
            "must_not_full_registry_scan": True,
            "must_not_change_runtime_code": True,
            "must_not_change_runtime_receipt_emission": True,
            "must_not_accept_candidate": True,
            "must_not_authorize_scale_mode": True,
            "must_not_write_registry": True,
            "must_not_create_synthetic_rows": True,
            "must_halt_if_no_candidate_compatible_rows": True,
            "must_halt_if_runner_command_unavailable": True,
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_POLICY_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    policy_id = sha8({
        "policy_name": POLICY_NAME,
        "source_decision_id": EXPECTED_DECISION_ID,
        "source_decision_receipt_id": EXPECTED_DECISION_RECEIPT_ID,
        "selected_option_id": SELECTED_OPTION_ID,
        "approved_bounds": APPROVED_BOUNDS,
        "runner_recipe": runner_recipe,
        "observer_extractor_contract": observer_extractor_contract,
        "valid_against": VALID_AGAINST,
        "next_command_goal": NEXT_COMMAND_GOAL,
    })
    policy["policy_id"] = policy_id
    policy["policy_sig8"] = policy_id

    receipt = {
        "schema_version": "raw_delta_signature_candidate_approved_new_bounded_surface_recipe_policy_receipt_v0",
        "receipt_type": "APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_POLICY_RECEIPT",
        "policy_id": policy_id,
        "policy_sig8": policy_id,
        "policy_name": POLICY_NAME,
        "policy_status": policy["policy_status"],
        "policy_path": f"data/raw_delta_signature_candidate_approved_new_bounded_surface_recipe_policies/{policy_id}.json",
        "source_decision_id": EXPECTED_DECISION_ID,
        "source_decision_receipt_id": EXPECTED_DECISION_RECEIPT_ID,
        "source_proposal_id": EXPECTED_PROPOSAL_ID,
        "source_proposal_receipt_id": EXPECTED_PROPOSAL_RECEIPT_ID,
        "selected_option_id": SELECTED_OPTION_ID,
        "approved_bounds": APPROVED_BOUNDS,
        "runner_command": runner_recipe["runner_command"],
        "runner_command_string": runner_recipe["runner_command_string"],
        "runner_command_precheck_required": True,
        "observer_extractor_name": observer_extractor_contract["extractor_name"],
        "candidate_row_schema": observer_extractor_contract["candidate_row_schema"],
        "valid_against": VALID_AGAINST,
        "authority": policy["authority"],
        "forbidden_effects_now": FORBIDDEN_NOW,
        "forbidden_effects_next_implementation": FORBIDDEN_NEXT_IMPLEMENTATION,
        "required_next_implementation_gates": policy["required_next_implementation_gates"],
        "terminal": policy["terminal"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    if write_outputs:
        (OUT_DIR / f"{policy_id}.json").write_text(json.dumps(policy, indent=2, sort_keys=True))
        (OUT_RECEIPT_DIR / f"{policy_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return policy, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision-id", default=EXPECTED_DECISION_ID)
    args = parser.parse_args()

    policy, receipt = build_policy(args.decision_id, write_outputs=True)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"policy_id={policy['policy_id']}")
    print(f"policy_json_path=data/raw_delta_signature_candidate_approved_new_bounded_surface_recipe_policies/{policy['policy_id']}.json")
    print(f"policy_receipt_path=data/raw_delta_signature_candidate_approved_new_bounded_surface_recipe_policy_receipts/{policy['policy_id']}.json")

    return 0 if policy["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
