#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

PROPOSAL_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_proposals"
PROPOSAL_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_receipts"
PROPOSAL_POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_policies"
PROPOSAL_POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_policy_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_human_decisions"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_human_decision_receipts"

EXPECTED_PROPOSAL_ID = "71f1a3f0"
EXPECTED_PROPOSAL_RECEIPT_ID = "d8a7686c"
EXPECTED_PROPOSAL_POLICY_ID = "ab982b44"
EXPECTED_PROPOSAL_POLICY_RECEIPT_ID = "cc0aae89"

DECISION_NAME = "HUMAN_DECISION_RECORD_APPROVE_OPTION_A_NARROWED_V0"
PROPOSAL_NAME = "PROPOSE_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
TRIGGER_HALT = "HOLD_NEW_BOUNDED_SURFACE_REQUIRES_RUNNER_DECISION"

SELECTED_OPTION_ID = "OPTION_A_NARROWED"
DECISION = "APPROVE"
DECISION_STATUS = "APPROVED_SCOPED"
NEXT_COMMAND_GOAL = "BUILD_APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_POLICY_V0"

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

FORBIDDEN_EFFECTS = [
    "immediate_execution",
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


def verify_proposal_surface(
    proposal: dict[str, Any],
    proposal_receipt: dict[str, Any],
    policy: dict[str, Any],
    policy_receipt: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if proposal.get("proposal_id") != EXPECTED_PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal_receipt.get("receipt_id") != EXPECTED_PROPOSAL_RECEIPT_ID:
        failures.append(f"proposal_receipt_id_wrong:{proposal_receipt.get('receipt_id')}")
    if proposal_receipt.get("proposal_id") != EXPECTED_PROPOSAL_ID:
        failures.append(f"proposal_receipt_proposal_id_wrong:{proposal_receipt.get('proposal_id')}")
    if policy.get("policy_id") != EXPECTED_PROPOSAL_POLICY_ID:
        failures.append(f"proposal_policy_id_wrong:{policy.get('policy_id')}")
    if policy_receipt.get("receipt_id") != EXPECTED_PROPOSAL_POLICY_RECEIPT_ID:
        failures.append(f"proposal_policy_receipt_id_wrong:{policy_receipt.get('receipt_id')}")

    if proposal.get("gate") != "PASS":
        failures.append(f"proposal_gate_not_PASS:{proposal.get('gate')}")
    if proposal_receipt.get("gate") != "PASS":
        failures.append(f"proposal_receipt_gate_not_PASS:{proposal_receipt.get('gate')}")
    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if policy_receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{policy_receipt.get('gate')}")

    if proposal.get("proposal_name") != PROPOSAL_NAME:
        failures.append(f"proposal_name_wrong:{proposal.get('proposal_name')}")
    if proposal.get("proposal_artifact_status") != "PROPOSED_UNAUTHORIZED":
        failures.append(f"proposal_status_wrong:{proposal.get('proposal_artifact_status')}")
    if proposal_receipt.get("proposal_status") != "PROPOSED_UNAUTHORIZED":
        failures.append(f"proposal_receipt_status_wrong:{proposal_receipt.get('proposal_status')}")
    if proposal.get("decision_status") != "HUMAN_BOUNDARY_PENDING":
        failures.append(f"proposal_decision_status_wrong:{proposal.get('decision_status')}")
    if proposal_receipt.get("decision_status") != "HUMAN_BOUNDARY_PENDING":
        failures.append(f"proposal_receipt_decision_status_wrong:{proposal_receipt.get('decision_status')}")

    if proposal.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"candidate_design_wrong:{proposal.get('candidate_design_id')}")
    if proposal.get("trigger_halt") != TRIGGER_HALT:
        failures.append(f"trigger_halt_wrong:{proposal.get('trigger_halt')}")
    if proposal.get("valid_against") != VALID_AGAINST:
        failures.append(f"valid_against_wrong:{proposal.get('valid_against')}")
    if proposal_receipt.get("valid_against") != VALID_AGAINST:
        failures.append(f"receipt_valid_against_wrong:{proposal_receipt.get('valid_against')}")
    if "No safe explicit recipe exists" not in str(proposal.get("current_blocker", "")):
        failures.append(f"current_blocker_wrong:{proposal.get('current_blocker')}")

    if proposal.get("proposal_class") != "POLICY_BOUNDARY_CANDIDATE":
        failures.append(f"proposal_class_wrong:{proposal.get('proposal_class')}")
    if proposal.get("authority_impact") != "REQUIRES_HUMAN_BOUNDARY":
        failures.append(f"authority_impact_wrong:{proposal.get('authority_impact')}")
    if proposal.get("human_decision_requested") != ["APPROVE", "REJECT", "NARROW", "RETYPE", "DEFER"]:
        failures.append(f"human_decision_requested_wrong:{proposal.get('human_decision_requested')}")

    recommended = proposal.get("recommended_default") or {}
    if recommended.get("option_id") != SELECTED_OPTION_ID:
        failures.append(f"recommended_option_wrong:{recommended.get('option_id')}")
    if recommended.get("status") != "RECOMMENDED_NON_AUTHORIZING":
        failures.append(f"recommended_status_wrong:{recommended.get('status')}")
    if "does not authorize execution" not in str(recommended.get("claim", "")):
        failures.append("recommended_claim_missing_non_authorizing_text")

    options = proposal.get("candidate_recipe_options") or []
    by_id = {opt.get("option_id"): opt for opt in options}
    if SELECTED_OPTION_ID not in by_id:
        failures.append(f"selected_option_missing:{SELECTED_OPTION_ID}")
    else:
        option = by_id[SELECTED_OPTION_ID]
        if option.get("default_bounds") != APPROVED_BOUNDS:
            failures.append(f"selected_option_bounds_wrong:{option.get('default_bounds')}")
        for field in [
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
            if field not in set(option.get("minimum_required_fields") or []):
                failures.append(f"selected_option_required_field_missing:{field}")

    required_forbidden = {
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
    }
    if set(proposal.get("forbidden_effects") or []) != required_forbidden:
        failures.append(f"proposal_forbidden_effects_wrong:{proposal.get('forbidden_effects')}")

    allowed = proposal.get("allowed_effects") or []
    if allowed != ["human_review", "human_decision_record", "future_policy_build_if_human_approved"]:
        failures.append(f"proposal_allowed_effects_wrong:{allowed}")

    guards = proposal.get("authority_guards") or {}
    if guards.get("proposal_emitted") is not True:
        failures.append(f"proposal_emitted_not_true:{guards.get('proposal_emitted')}")
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
        if guards.get(key) is not False:
            failures.append(f"proposal_guard_not_false:{key}:{guards.get(key)}")

    terminal = proposal.get("terminal") or {}
    if terminal.get("type") != "STOP":
        failures.append(f"proposal_terminal_type_wrong:{terminal.get('type')}")
    if terminal.get("stop_code") != "STOP_HUMAN_BOUNDARY_REQUIRED":
        failures.append(f"proposal_stop_code_wrong:{terminal.get('stop_code')}")
    if terminal.get("next_command_goal") != "HUMAN_DECISION_RECORD_V0":
        failures.append(f"proposal_next_goal_wrong:{terminal.get('next_command_goal')}")

    required_approval = proposal.get("required_receipt_if_approved_later") or {}
    if required_approval.get("receipt_type") != "APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_RECEIPT":
        failures.append(f"required_approval_receipt_type_wrong:{required_approval.get('receipt_type')}")
    for key in [
        "approval_does_not_execute",
        "approval_does_not_insert_registry",
        "approval_does_not_accept_candidate",
    ]:
        if required_approval.get(key) is not True:
            failures.append(f"required_approval_guard_not_true:{key}:{required_approval.get(key)}")
    if required_approval.get("next_policy_after_approval") != NEXT_COMMAND_GOAL:
        failures.append(f"required_approval_next_policy_wrong:{required_approval.get('next_policy_after_approval')}")

    auth = policy.get("authority") or {}
    if auth.get("authorizes_proposal_emission") is not True:
        failures.append("policy_does_not_authorize_proposal_emission")
    for key in [
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
    ]:
        if auth.get(key) is not False:
            failures.append(f"policy_forbidden_authority_not_false:{key}:{auth.get(key)}")

    return failures


def build_decision(proposal_id: str, decision: str, option_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    proposal = load_json(PROPOSAL_DIR / f"{proposal_id}.json")
    proposal_receipt = load_json(PROPOSAL_RECEIPT_DIR / f"{proposal_id}.json")
    policy = load_json(PROPOSAL_POLICY_DIR / f"{EXPECTED_PROPOSAL_POLICY_ID}.json")
    policy_receipt = load_json(PROPOSAL_POLICY_RECEIPT_DIR / f"{EXPECTED_PROPOSAL_POLICY_ID}.json")

    failures = verify_proposal_surface(proposal, proposal_receipt, policy, policy_receipt)

    if decision != DECISION:
        failures.append(f"decision_wrong:{decision}")
    if option_id != SELECTED_OPTION_ID:
        failures.append(f"option_id_wrong:{option_id}")

    approved_recipe_scope = {
        "selected_option_id": SELECTED_OPTION_ID,
        "selected_option_name": "existing_cli_fresh_run_plus_observer_extractor",
        "approval_scope": "RECIPE_SHAPE_ONLY_NOT_EXECUTION",
        "approved_bounds": APPROVED_BOUNDS,
        "approved_required_fields": [
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
        "approved_allowed_effects_for_later_policy": [
            "define_approved_recipe_policy",
            "specify_existing_bounded_cli_or_script_command",
            "specify_observer_only_extractor",
            "specify_surface_manifest_and_receipt_targets",
        ],
        "forbidden_effects_now": FORBIDDEN_EFFECTS,
    }

    decision_record = {
        "schema_version": "raw_delta_signature_candidate_new_bounded_surface_recipe_human_decision_v0",
        "decision_name": DECISION_NAME,
        "decision": DECISION,
        "decision_status": DECISION_STATUS,
        "proposal_id": EXPECTED_PROPOSAL_ID,
        "proposal_receipt_id": EXPECTED_PROPOSAL_RECEIPT_ID,
        "proposal_name": PROPOSAL_NAME,
        "source_policy_id": EXPECTED_PROPOSAL_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_PROPOSAL_POLICY_RECEIPT_ID,
        "valid_against": VALID_AGAINST,
        "decision_scope": {
            "proposal_id": EXPECTED_PROPOSAL_ID,
            "proposal_receipt_id": EXPECTED_PROPOSAL_RECEIPT_ID,
            "trigger_surface_id": VALID_AGAINST["surface_id"],
            "trigger_receipt_id": VALID_AGAINST["receipt_id"],
            "candidate_design_id": CANDIDATE_DESIGN_ID,
            "selected_encoding_id": VALID_AGAINST["selected_encoding_id"],
            "selected_target_raw_delta_field": VALID_AGAINST["selected_target_raw_delta_field"],
        },
        "approved_recipe_scope": approved_recipe_scope,
        "decision_effects": {
            "authorizes_recipe_policy_build": True,
            "authorized_next_command_goal": NEXT_COMMAND_GOAL,
            "approves_option_a_narrowed": True,
            "approval_is_scoped_to_valid_against_surface": True,
            "approval_does_not_execute": True,
            "approval_does_not_run_runner": True,
            "approval_does_not_create_candidate_rows": True,
            "approval_does_not_accept_candidate": True,
            "approval_does_not_authorize_scale_mode": True,
            "approval_does_not_insert_registry": True,
            "approval_does_not_read_registry_sqlite": True,
            "approval_does_not_full_registry_scan": True,
            "approval_does_not_mutate_runtime": True,
            "approval_does_not_change_runtime_code": True,
            "approval_does_not_change_runtime_receipt_emission": True,
            "approval_does_not_use_latest_or_mtime_selection": True,
            "approval_does_not_use_case_id_or_cycle_n_identity_patch": True,
            "approval_does_not_use_rowid_or_receipt_hash_truth_surface": True,
            "approval_does_not_put_full_occurrence_key_in_payload": True,
            "approval_does_not_put_audit_or_debug_in_payload": True,
            "approval_does_not_create_synthetic_fake_rows": True,
            "approval_does_not_run_transition_compression_probe": True,
        },
        "required_next_artifact": {
            "artifact_name": "APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_POLICY_V0",
            "builder_goal": NEXT_COMMAND_GOAL,
            "must_include_runner_command": True,
            "must_include_observer_extractor_contract": True,
            "must_include_candidate_row_schema": True,
            "must_include_bounds": APPROVED_BOUNDS,
            "must_include_no_latest_mtime_guard": True,
            "must_include_no_runtime_mutation_guard": True,
            "must_include_no_registry_sqlite_guard": True,
            "must_include_no_candidate_acceptance_guard": True,
        },
        "human_boundary": {
            "human_approved": True,
            "human_decision_requested": "APPROVE",
            "human_selected_option": SELECTED_OPTION_ID,
            "human_notes": "Approved Option A narrowed as recipe shape only. No execution or candidate acceptance is authorized by this decision record.",
        },
        "terminal": {
            "type": "ADVANCE" if not failures else "STOP",
            "next_command_goal": NEXT_COMMAND_GOAL if not failures else None,
            "stop_code": None if not failures else "STOP_HUMAN_DECISION_RECORD_INVALID",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    decision_id = sha8({
        "decision_name": DECISION_NAME,
        "decision": DECISION,
        "decision_status": DECISION_STATUS,
        "proposal_id": EXPECTED_PROPOSAL_ID,
        "proposal_receipt_id": EXPECTED_PROPOSAL_RECEIPT_ID,
        "selected_option_id": SELECTED_OPTION_ID,
        "approved_bounds": APPROVED_BOUNDS,
        "valid_against": VALID_AGAINST,
        "next_command_goal": NEXT_COMMAND_GOAL,
    })
    decision_record["decision_id"] = decision_id
    decision_record["decision_sig8"] = decision_id

    receipt = {
        "schema_version": "raw_delta_signature_candidate_new_bounded_surface_recipe_human_decision_receipt_v0",
        "receipt_type": "HUMAN_DECISION_RECORD_RECEIPT",
        "decision_id": decision_id,
        "decision_sig8": decision_id,
        "decision_name": DECISION_NAME,
        "decision": DECISION,
        "decision_status": DECISION_STATUS,
        "decision_path": f"data/raw_delta_signature_candidate_new_bounded_surface_recipe_human_decisions/{decision_id}.json",
        "proposal_id": EXPECTED_PROPOSAL_ID,
        "proposal_receipt_id": EXPECTED_PROPOSAL_RECEIPT_ID,
        "proposal_name": PROPOSAL_NAME,
        "selected_option_id": SELECTED_OPTION_ID,
        "valid_against": VALID_AGAINST,
        "approved_bounds": APPROVED_BOUNDS,
        "decision_effects": decision_record["decision_effects"],
        "required_next_artifact": decision_record["required_next_artifact"],
        "human_boundary": decision_record["human_boundary"],
        "terminal": decision_record["terminal"],
        "gate": decision_record["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    (OUT_DIR / f"{decision_id}.json").write_text(json.dumps(decision_record, indent=2, sort_keys=True))
    (OUT_RECEIPT_DIR / f"{decision_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return decision_record, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal-id", default=EXPECTED_PROPOSAL_ID)
    parser.add_argument("--decision", default=DECISION)
    parser.add_argument("--option-id", default=SELECTED_OPTION_ID)
    args = parser.parse_args()

    decision_record, receipt = build_decision(args.proposal_id, args.decision, args.option_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"decision_id={decision_record['decision_id']}")
    print(f"decision_json_path=data/raw_delta_signature_candidate_new_bounded_surface_recipe_human_decisions/{decision_record['decision_id']}.json")
    print(f"decision_receipt_path=data/raw_delta_signature_candidate_new_bounded_surface_recipe_human_decision_receipts/{decision_record['decision_id']}.json")

    return 0 if decision_record["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
