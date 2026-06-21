#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_policy_receipts"

SOURCE_SURFACE_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_validation_surfaces"
SOURCE_SURFACE_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_validation_surface_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_proposals"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_receipts"

EXPECTED_POLICY_ID = "ab982b44"
EXPECTED_POLICY_RECEIPT_ID = "cc0aae89"
EXPECTED_SOURCE_SURFACE_ID = "40e5f5b4"
EXPECTED_SOURCE_SURFACE_RECEIPT_ID = "065849ef"

PROPOSAL_NAME = "PROPOSE_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
TRIGGER_HALT = "HOLD_NEW_BOUNDED_SURFACE_REQUIRES_RUNNER_DECISION"
SELECTED_ENCODING_ID = "raw_decimal_sig6"
TARGET_RAW_DELTA_FIELD = "compression_ratio"

PROPOSAL_STATUS = "PROPOSED_UNAUTHORIZED"
DECISION_STATUS = "HUMAN_BOUNDARY_PENDING"

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

REQUIRED_FORBIDDEN_EFFECTS = [
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


def verify_policy_and_source(
    policy: dict[str, Any],
    policy_receipt: dict[str, Any],
    source_surface: dict[str, Any],
    source_receipt: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy_receipt.get("receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy_receipt.get('receipt_id')}")
    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if policy_receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{policy_receipt.get('gate')}")
    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy.get('policy_status')}")
    if policy.get("proposal_name") != PROPOSAL_NAME:
        failures.append(f"policy_proposal_name_wrong:{policy.get('proposal_name')}")
    if policy.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"policy_candidate_design_wrong:{policy.get('candidate_design_id')}")
    if policy.get("source_surface_id") != EXPECTED_SOURCE_SURFACE_ID:
        failures.append(f"policy_source_surface_wrong:{policy.get('source_surface_id')}")
    if policy.get("source_surface_receipt_id") != EXPECTED_SOURCE_SURFACE_RECEIPT_ID:
        failures.append(f"policy_source_receipt_wrong:{policy.get('source_surface_receipt_id')}")
    if policy.get("trigger_halt") != TRIGGER_HALT:
        failures.append(f"policy_trigger_halt_wrong:{policy.get('trigger_halt')}")
    if policy.get("terminal", {}).get("next_command_goal") != "EMIT_PROPOSE_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_V0":
        failures.append(f"policy_next_goal_wrong:{policy.get('terminal', {}).get('next_command_goal')}")

    contract = policy.get("proposal_contract") or {}
    if contract.get("proposal_name") != PROPOSAL_NAME:
        failures.append(f"contract_proposal_name_wrong:{contract.get('proposal_name')}")
    if contract.get("proposal_status_if_emitted") != PROPOSAL_STATUS:
        failures.append(f"contract_proposal_status_wrong:{contract.get('proposal_status_if_emitted')}")
    if contract.get("decision_status_if_emitted") != DECISION_STATUS:
        failures.append(f"contract_decision_status_wrong:{contract.get('decision_status_if_emitted')}")
    if contract.get("trigger_halt") != TRIGGER_HALT:
        failures.append(f"contract_trigger_halt_wrong:{contract.get('trigger_halt')}")
    if contract.get("proposal_class") != "POLICY_BOUNDARY_CANDIDATE":
        failures.append(f"contract_class_wrong:{contract.get('proposal_class')}")
    if contract.get("authority_impact") != "REQUIRES_HUMAN_BOUNDARY":
        failures.append(f"contract_authority_impact_wrong:{contract.get('authority_impact')}")
    if contract.get("human_decision_requested") != ["APPROVE", "REJECT", "NARROW", "RETYPE", "DEFER"]:
        failures.append(f"human_decision_requested_wrong:{contract.get('human_decision_requested')}")

    valid_against = contract.get("valid_against") or {}
    expected_valid_against = {
        "surface_id": EXPECTED_SOURCE_SURFACE_ID,
        "receipt_id": EXPECTED_SOURCE_SURFACE_RECEIPT_ID,
        "policy_id": "7050f196",
        "policy_receipt_id": "2c061175",
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "selected_encoding_id": SELECTED_ENCODING_ID,
        "selected_target_raw_delta_field": TARGET_RAW_DELTA_FIELD,
    }
    if valid_against != expected_valid_against:
        failures.append(f"valid_against_wrong:{valid_against}")

    if "No safe explicit recipe exists" not in str(contract.get("current_blocker", "")):
        failures.append(f"current_blocker_wrong:{contract.get('current_blocker')}")

    recommended = contract.get("recommended_default") or {}
    if recommended.get("option_id") != "OPTION_A_NARROWED":
        failures.append(f"recommended_option_wrong:{recommended.get('option_id')}")
    if recommended.get("status") != "RECOMMENDED_NON_AUTHORIZING":
        failures.append(f"recommended_status_wrong:{recommended.get('status')}")

    options = contract.get("candidate_recipe_options") or []
    option_ids = {opt.get("option_id") for opt in options}
    for option_id in [
        "OPTION_A_NARROWED",
        "OPTION_B_EXISTING_RECEIPT_SURFACE_EXTRACTOR",
        "OPTION_C_DEFINE_FIXTURE_RADIUS_DEPTH_RECIPE_FIRST",
        "OPTION_D_DEFER_GENERIC_PROCEED_HALT_PROPOSAL_RUNNER",
    ]:
        if option_id not in option_ids:
            failures.append(f"recipe_option_missing:{option_id}")

    for opt in options:
        forbidden = set(opt.get("forbidden_effects") or [])
        for effect in REQUIRED_FORBIDDEN_EFFECTS:
            if effect not in forbidden:
                failures.append(f"option_forbidden_effect_missing:{opt.get('option_id')}:{effect}")

    gate = contract.get("proposal_gate") or {}
    for key in [
        "requires_trigger_halt",
        "requires_trigger_receipt",
        "requires_valid_against_surface_lock",
        "requires_current_blocker",
        "requires_candidate_recipe_options",
        "requires_recommended_option_non_authorizing",
        "requires_authority_impact",
        "requires_forbidden_effects",
        "requires_required_receipt_if_approved",
        "requires_human_decision_request",
        "proposal_must_not_execute",
        "proposal_must_not_register",
        "proposal_must_not_accept",
        "proposal_must_not_patch",
        "proposal_must_not_authorize_itself",
    ]:
        if gate.get(key) is not True:
            failures.append(f"proposal_gate_not_true:{key}:{gate.get(key)}")

    required_emit = contract.get("required_receipt_if_emitted") or {}
    if required_emit.get("receipt_type") != "PROPOSAL_EMISSION_RECEIPT":
        failures.append(f"required_emit_receipt_type_wrong:{required_emit.get('receipt_type')}")
    for field in [
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
    ]:
        if field not in set(required_emit.get("must_record") or []):
            failures.append(f"required_emit_field_missing:{field}")

    required_approval = contract.get("required_receipt_if_approved_later") or {}
    if required_approval.get("receipt_type") != "APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_RECEIPT":
        failures.append(f"approval_receipt_type_wrong:{required_approval.get('receipt_type')}")
    for key in [
        "approval_does_not_execute",
        "approval_does_not_insert_registry",
        "approval_does_not_accept_candidate",
    ]:
        if required_approval.get(key) is not True:
            failures.append(f"approval_guard_not_true:{key}:{required_approval.get(key)}")
    if required_approval.get("next_policy_after_approval") != "BUILD_APPROVED_NEW_BOUNDED_VALIDATION_SURFACE_RECIPE_POLICY_V0":
        failures.append(f"approval_next_policy_wrong:{required_approval.get('next_policy_after_approval')}")

    auth = policy.get("authority") or {}
    if auth.get("observer_only") is not True:
        failures.append("policy_not_observer_only")
    for key in [
        "authorizes_proposal_emission",
        "authorizes_human_boundary_request",
        "authorizes_recipe_options_listing",
        "authorizes_recommended_option_label",
        "authorizes_required_receipt_specification",
    ]:
        if auth.get(key) is not True:
            failures.append(f"required_authority_not_true:{key}:{auth.get(key)}")
    for key in FORBIDDEN_AUTHORITY_FLAGS:
        if auth.get(key) is not False:
            failures.append(f"forbidden_authority_not_false:{key}:{auth.get(key)}")

    constraints = policy.get("implementation_constraints") or {}
    if constraints.get("must_touch_only_files") != ["scripts/emit_propose_new_bounded_validation_surface_recipe_v0.py"]:
        failures.append(f"touch_scope_wrong:{constraints.get('must_touch_only_files')}")
    for key in [
        "must_start_from_hold_surface",
        "must_lock_valid_against_surface",
        "must_emit_proposed_unauthorized_only",
        "must_set_decision_status_human_boundary_pending",
        "must_not_execute_runner",
        "must_not_create_candidate_rows",
        "must_not_accept_candidate",
        "must_not_insert_registry",
        "must_not_read_registry_sqlite",
        "must_not_full_registry_scan",
        "must_not_use_latest_or_mtime_selection",
        "must_not_change_runtime",
        "must_not_change_runtime_code",
        "must_not_change_runtime_receipt_emission",
        "must_not_write_registry",
    ]:
        if key == "must_start_from_hold_surface":
            if constraints.get(key) != EXPECTED_SOURCE_SURFACE_ID:
                failures.append(f"constraint_start_surface_wrong:{constraints.get(key)}")
        elif constraints.get(key) is not True:
            failures.append(f"constraint_not_true:{key}:{constraints.get(key)}")

    if source_surface.get("surface_id") != EXPECTED_SOURCE_SURFACE_ID:
        failures.append(f"source_surface_id_wrong:{source_surface.get('surface_id')}")
    if source_receipt.get("receipt_id") != EXPECTED_SOURCE_SURFACE_RECEIPT_ID:
        failures.append(f"source_receipt_id_wrong:{source_receipt.get('receipt_id')}")
    if source_surface.get("gate") != "PASS":
        failures.append(f"source_surface_gate_not_PASS:{source_surface.get('gate')}")
    if source_receipt.get("gate") != "PASS":
        failures.append(f"source_receipt_gate_not_PASS:{source_receipt.get('gate')}")
    if source_surface.get("terminal_class") != TRIGGER_HALT:
        failures.append(f"source_terminal_class_wrong:{source_surface.get('terminal_class')}")
    if source_surface.get("terminal", {}).get("type") != "HOLD":
        failures.append(f"source_terminal_type_wrong:{source_surface.get('terminal', {}).get('type')}")
    if source_surface.get("terminal", {}).get("stop_code") != TRIGGER_HALT:
        failures.append(f"source_terminal_stop_wrong:{source_surface.get('terminal', {}).get('stop_code')}")

    discovery = source_receipt.get("runner_discovery_summary") or {}
    if discovery.get("safe_recipe_candidates_total") != 0:
        failures.append(f"source_safe_recipe_candidates_not_zero:{discovery.get('safe_recipe_candidates_total')}")
    if discovery.get("registry_sqlite_read") is not False:
        failures.append(f"source_registry_sqlite_read_not_false:{discovery.get('registry_sqlite_read')}")
    if discovery.get("full_registry_scan_used") is not False:
        failures.append(f"source_full_registry_scan_not_false:{discovery.get('full_registry_scan_used')}")
    if discovery.get("runtime_code_changed") is not False:
        failures.append(f"source_runtime_code_changed_not_false:{discovery.get('runtime_code_changed')}")

    source_decision = source_receipt.get("decision") or {}
    if source_decision.get("safe_runner_recipe_found") is not False:
        failures.append(f"source_safe_recipe_found_not_false:{source_decision.get('safe_runner_recipe_found')}")
    if source_decision.get("new_surface_created") is not False:
        failures.append(f"source_new_surface_created_not_false:{source_decision.get('new_surface_created')}")

    return failures


def build_proposal(policy_id: str) -> tuple[dict[str, Any], dict[str, Any]]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")
    source_surface = load_json(SOURCE_SURFACE_DIR / f"{EXPECTED_SOURCE_SURFACE_ID}.json")
    source_receipt = load_json(SOURCE_SURFACE_RECEIPT_DIR / f"{EXPECTED_SOURCE_SURFACE_ID}.json")

    failures = verify_policy_and_source(policy, policy_receipt, source_surface, source_receipt)
    contract = policy.get("proposal_contract") or {}

    proposal = {
        "schema_version": "raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_v0",
        "proposal_name": PROPOSAL_NAME,
        "proposal_artifact_status": PROPOSAL_STATUS,
        "decision_status": DECISION_STATUS,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "trigger_halt": TRIGGER_HALT,
        "valid_against": contract.get("valid_against"),
        "current_blocker": contract.get("current_blocker"),
        "proposal_class": contract.get("proposal_class"),
        "candidate_class": contract.get("proposal_class"),
        "authority_impact": contract.get("authority_impact"),
        "human_decision_requested": contract.get("human_decision_requested"),
        "recommended_default": contract.get("recommended_default"),
        "candidate_recipe_options": contract.get("candidate_recipe_options"),
        "forbidden_effects": REQUIRED_FORBIDDEN_EFFECTS,
        "allowed_effects": [
            "human_review",
            "human_decision_record",
            "future_policy_build_if_human_approved",
        ],
        "must_not_impersonate": [
            "authorization",
            "execution",
            "runner execution",
            "candidate row creation",
            "registry insertion",
            "candidate acceptance",
            "scale mode authorization",
            "runtime semantic change",
            "runtime code change",
            "runtime receipt emission change",
            "proof",
            "global admissibility",
        ],
        "proposal_gate": contract.get("proposal_gate"),
        "required_receipt_if_approved_later": contract.get("required_receipt_if_approved_later"),
        "post_proposal_next_steps": contract.get("post_proposal_next_steps"),
        "metrics": {
            "typedness": "HIGH",
            "authority_clarity": "HIGH",
            "scope_bound": "HIGH",
            "semantic_drift_risk": "MED",
            "reversibility": "HIGH",
            "blast_radius": "LOW",
            "novelty": "MED",
            "next_unit_clarity": "HIGH",
            "ambiguity_count": 1,
            "stop_reason_class": TRIGGER_HALT,
            "human_boundary_required": True,
            "artifact_delta_class": "PROPOSAL_ARTIFACT_ONLY",
        },
        "authority_guards": {
            "proposal_emitted": True,
            "proposal_executed": False,
            "runner_executed": False,
            "candidate_rows_created": False,
            "candidate_accepted": False,
            "scale_mode_authorized": False,
            "registry_inserted": False,
            "registry_sqlite_read": False,
            "full_registry_scan_used": False,
            "runtime_semantic_changed": False,
            "runtime_code_changed": False,
            "runtime_receipt_emission_changed": False,
            "registry_write_authorized": False,
            "latest_or_mtime_selection_used": False,
            "ambient_workspace_inference_used": False,
            "case_id_or_cycle_n_identity_patch_used": False,
            "rowid_or_receipt_hash_truth_surface_used": False,
            "full_occurrence_key_in_signature_payload": False,
            "audit_or_debug_payload_in_signature_payload": False,
            "microhash_as_proof_used": False,
            "synthetic_fake_validation_rows_used": False,
            "transition_compression_probe_run": False,
        },
        "source_refs": {
            "source_policy_id": EXPECTED_POLICY_ID,
            "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
            "source_surface_id": EXPECTED_SOURCE_SURFACE_ID,
            "source_surface_receipt_id": EXPECTED_SOURCE_SURFACE_RECEIPT_ID,
            "source_trigger_halt": TRIGGER_HALT,
        },
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_HUMAN_BOUNDARY_REQUIRED",
            "next_command_goal": "HUMAN_DECISION_RECORD_V0",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    proposal_id = sha8({
        "proposal_name": PROPOSAL_NAME,
        "valid_against": proposal["valid_against"],
        "current_blocker": proposal["current_blocker"],
        "candidate_recipe_options": proposal["candidate_recipe_options"],
        "recommended_default": proposal["recommended_default"],
        "trigger_halt": TRIGGER_HALT,
        "status": PROPOSAL_STATUS,
    })
    proposal["proposal_id"] = proposal_id
    proposal["proposal_sig8"] = proposal_id

    receipt = {
        "schema_version": "raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_receipt_v0",
        "receipt_type": "PROPOSAL_EMISSION_RECEIPT",
        "proposal_id": proposal_id,
        "proposal_sig8": proposal_id,
        "proposal_name": PROPOSAL_NAME,
        "proposal_status": PROPOSAL_STATUS,
        "decision_status": DECISION_STATUS,
        "proposal_path": f"data/raw_delta_signature_candidate_new_bounded_surface_recipe_proposals/{proposal_id}.json",
        "source_policy_id": EXPECTED_POLICY_ID,
        "source_policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "trigger_surface_id": EXPECTED_SOURCE_SURFACE_ID,
        "trigger_receipt_id": EXPECTED_SOURCE_SURFACE_RECEIPT_ID,
        "trigger_halt": TRIGGER_HALT,
        "valid_against": proposal["valid_against"],
        "current_blocker": proposal["current_blocker"],
        "candidate_recipe_options": [
            opt.get("option_id") for opt in proposal["candidate_recipe_options"] or []
        ],
        "recommended_option": proposal["recommended_default"]["option_id"],
        "recommended_status": proposal["recommended_default"]["status"],
        "authority_impact": proposal["authority_impact"],
        "forbidden_effects": proposal["forbidden_effects"],
        "required_receipt_if_approved": proposal["required_receipt_if_approved_later"],
        "human_decision_requested": proposal["human_decision_requested"],
        "metrics": proposal["metrics"],
        "authority_guards": proposal["authority_guards"],
        "must_not_impersonate": proposal["must_not_impersonate"],
        "terminal": proposal["terminal"],
        "gate": proposal["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id

    (OUT_DIR / f"{proposal_id}.json").write_text(json.dumps(proposal, indent=2, sort_keys=True))
    (OUT_RECEIPT_DIR / f"{proposal_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return proposal, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-id", default=EXPECTED_POLICY_ID)
    args = parser.parse_args()

    proposal, receipt = build_proposal(args.policy_id)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"proposal_id={proposal['proposal_id']}")
    print(f"proposal_json_path=data/raw_delta_signature_candidate_new_bounded_surface_recipe_proposals/{proposal['proposal_id']}.json")
    print(f"proposal_receipt_path=data/raw_delta_signature_candidate_new_bounded_surface_recipe_proposal_receipts/{proposal['proposal_id']}.json")

    return 0 if proposal["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
