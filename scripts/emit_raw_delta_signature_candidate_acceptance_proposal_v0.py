#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

PROPOSAL_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_ACCEPTANCE_PROPOSAL_V0"
POLICY_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_ACCEPTANCE_PROPOSAL_POLICY_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"

EXPECTED_POLICY_ID = "b420b784"
EXPECTED_POLICY_RECEIPT_ID = "aff60f48"

SOURCE_REVIEW_ID = "2946b241"
SOURCE_REVIEW_RECEIPT_ID = "79333614"
SOURCE_PROBE_ID = "87b4a010"
SOURCE_PROBE_RECEIPT_ID = "812ae591"
SOURCE_SURFACE_ID = "4427ba4b"
SOURCE_SURFACE_RECEIPT_ID = "e5022cd2"
PRIOR_PROBE_ID = "6a33c978"
PRIOR_PROBE_RECEIPT_ID = "99c90fe3"
SCALE_OUT_ID = "2b44b1fd"
SCALE_OUT_RECEIPT_ID = "f67b629b"

POLICY_DIR = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposal_policies"
POLICY_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposal_policy_receipts"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposals"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposal_receipts"

HUMAN_DECISION_GOAL = "RECORD_RAW_DELTA_SIGNATURE_CANDIDATE_ACCEPTANCE_HUMAN_DECISION_V0"

FORBIDDEN_AUTHORITY_TRUE_BEFORE_EMISSION = [
    "runner_executed",
    "candidate_rows_created",
    "candidate_accepted",
    "scale_mode_authorized",
    "registry_inserted",
    "registry_written",
    "registry_sqlite_read",
    "full_registry_scan_used",
    "runtime_semantic_changed",
    "runtime_code_changed",
    "runtime_receipt_emission_changed",
    "latest_or_mtime_selection_used",
    "ambient_workspace_inference_used",
    "case_id_or_cycle_n_identity_patch_used",
    "rowid_or_receipt_hash_truth_surface_used",
    "full_occurrence_key_in_signature_payload",
    "audit_or_debug_payload_in_signature_payload",
    "microhash_as_proof_used",
    "synthetic_fake_validation_rows_used",
    "transition_compression_probe_run",
    "candidate_acceptance_proposal_emitted",
    "human_decision_boundary_emitted",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")


def sha8(obj: Any) -> str:
    return hashlib.sha256(blob(obj)).hexdigest()[:8]


def load_json(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required json: {path}")
    return json.loads(path.read_text())


def validate_policy(policy: dict[str, Any], receipt: dict[str, Any]) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy.get("policy_receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if receipt.get("policy_id") != EXPECTED_POLICY_ID:
        failures.append(f"receipt_policy_id_wrong:{receipt.get('policy_id')}")
    if receipt.get("receipt_id") != EXPECTED_POLICY_RECEIPT_ID:
        failures.append(f"receipt_id_wrong:{receipt.get('receipt_id')}")

    if policy.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy.get('gate')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{receipt.get('gate')}")
    if policy.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy.get('policy_status')}")
    if receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_receipt_status_wrong:{receipt.get('policy_status')}")

    if policy.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"candidate_design_id_wrong:{policy.get('candidate_design_id')}")
    if receipt.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"receipt_candidate_design_id_wrong:{receipt.get('candidate_design_id')}")

    if receipt.get("source_review_id") != SOURCE_REVIEW_ID:
        failures.append(f"source_review_id_wrong:{receipt.get('source_review_id')}")
    if receipt.get("source_review_receipt_id") != SOURCE_REVIEW_RECEIPT_ID:
        failures.append(f"source_review_receipt_id_wrong:{receipt.get('source_review_receipt_id')}")
    if receipt.get("source_probe_id") != SOURCE_PROBE_ID:
        failures.append(f"source_probe_id_wrong:{receipt.get('source_probe_id')}")
    if receipt.get("source_probe_receipt_id") != SOURCE_PROBE_RECEIPT_ID:
        failures.append(f"source_probe_receipt_id_wrong:{receipt.get('source_probe_receipt_id')}")
    if receipt.get("source_surface_id") != SOURCE_SURFACE_ID:
        failures.append(f"source_surface_id_wrong:{receipt.get('source_surface_id')}")
    if receipt.get("source_surface_receipt_id") != SOURCE_SURFACE_RECEIPT_ID:
        failures.append(f"source_surface_receipt_id_wrong:{receipt.get('source_surface_receipt_id')}")
    if receipt.get("prior_probe_id") != PRIOR_PROBE_ID:
        failures.append(f"prior_probe_id_wrong:{receipt.get('prior_probe_id')}")
    if receipt.get("prior_probe_receipt_id") != PRIOR_PROBE_RECEIPT_ID:
        failures.append(f"prior_probe_receipt_id_wrong:{receipt.get('prior_probe_receipt_id')}")
    if receipt.get("scale_out_id") != SCALE_OUT_ID:
        failures.append(f"scale_out_id_wrong:{receipt.get('scale_out_id')}")
    if receipt.get("scale_out_receipt_id") != SCALE_OUT_RECEIPT_ID:
        failures.append(f"scale_out_receipt_id_wrong:{receipt.get('scale_out_receipt_id')}")

    classification = receipt.get("pre_proposal_classification") or {}
    for key in [
        "source_review_pass_clean",
        "review_decision_is_acceptance_proposal_next",
        "all_evidence_decision_conditions_true",
        "candidate_acceptance_not_authorized_here",
        "proposal_only",
        "human_boundary_required",
    ]:
        if classification.get(key) is not True:
            failures.append(f"classification_not_true:{key}:{classification.get(key)}")

    recommendation = receipt.get("proposal_recommendation") or {}
    if recommendation.get("recommended_option") != "OPTION_A_PROVISIONAL_BOUNDED_ACCEPTANCE_PROPOSAL":
        failures.append(f"recommended_option_wrong:{recommendation.get('recommended_option')}")
    for key in [
        "human_boundary_required",
        "does_not_accept_candidate",
        "does_not_write_registry",
        "does_not_change_runtime",
    ]:
        if recommendation.get(key) is not True:
            failures.append(f"recommendation_safety_not_true:{key}:{recommendation.get(key)}")

    contract = policy.get("proposal_contract") or {}
    if contract.get("human_boundary") != "REQUIRED_BEFORE_ANY_ACCEPTANCE_OR_REGISTRY_WRITE":
        failures.append(f"human_boundary_wrong:{contract.get('human_boundary')}")
    safety = contract.get("required_safety_clauses") or {}
    for key in [
        "proposal_only",
        "candidate_not_accepted",
        "registry_not_written",
        "runtime_not_changed",
        "bounded_scope_explicit",
        "human_decision_required",
    ]:
        if safety.get(key) is not True:
            failures.append(f"safety_clause_not_true:{key}:{safety.get(key)}")

    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != "EMIT_RAW_DELTA_SIGNATURE_CANDIDATE_ACCEPTANCE_PROPOSAL_V0":
        failures.append(f"terminal_next_wrong:{terminal.get('next_command_goal')}")

    forbidden = policy.get("forbidden_operations") or {}
    for key, value in forbidden.items():
        if value is not True:
            failures.append(f"forbidden_operation_not_true:{key}:{value}")

    authorized = policy.get("authorized_operations_next") or {}
    for key in [
        "read_source_review_result",
        "read_source_review_receipt",
        "write_acceptance_proposal",
        "write_acceptance_proposal_receipt",
        "emit_human_decision_boundary",
    ]:
        if authorized.get(key) is not True:
            failures.append(f"authorized_next_not_true:{key}:{authorized.get(key)}")

    guards = receipt.get("authority_guards") or {}
    for key in FORBIDDEN_AUTHORITY_TRUE_BEFORE_EMISSION:
        if guards.get(key) is not False:
            failures.append(f"policy_authority_guard_not_false_before_emission:{key}:{guards.get(key)}")

    return failures


def build_proposal(policy_id: str, write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    if policy_id != EXPECTED_POLICY_ID:
        raise SystemExit(f"unsupported acceptance proposal policy id: {policy_id}")

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    policy = load_json(POLICY_DIR / f"{policy_id}.json")
    policy_receipt = load_json(POLICY_RECEIPT_DIR / f"{policy_id}.json")

    failures = validate_policy(policy, policy_receipt)

    recommendation = policy_receipt.get("proposal_recommendation") or {}
    evidence_stack = policy.get("evidence_stack") or {}

    proposal_seed = {
        "proposal_name": PROPOSAL_NAME,
        "policy_id": policy_id,
        "policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "source_review_id": SOURCE_REVIEW_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "recommended_option": recommendation.get("recommended_option"),
    }
    proposal_id = sha8(proposal_seed)

    human_options = {
        "OPTION_A_PROVISIONAL_BOUNDED_ACCEPT": {
            "meaning": "Approve provisional bounded acceptance of RAW_DELTA_SIGNATURE_CANDIDATE_V0 under the cited evidence stack.",
            "would_allow_next": "Build a separate human-decision record, then a separate candidate-acceptance/registry policy.",
            "does_not_happen_in_this_proposal": True,
        },
        "OPTION_B_MORE_SCALE_BEFORE_ACCEPTANCE": {
            "meaning": "Do not accept yet; request additional bounded scale or inventory before acceptance.",
            "would_allow_next": "Build additional scale policy or proposal.",
            "does_not_happen_in_this_proposal": True,
        },
        "OPTION_C_REJECT_OR_DIAGNOSE": {
            "meaning": "Do not accept; reject, revise, or diagnose the candidate/evidence stack.",
            "would_allow_next": "Build diagnostic/revision policy.",
            "does_not_happen_in_this_proposal": True,
        },
    }

    proposal = {
        "schema_version": "raw_delta_signature_candidate_acceptance_proposal_v0",
        "proposal_name": PROPOSAL_NAME,
        "proposal_id": proposal_id,
        "proposal_status": "HUMAN_DECISION_REQUIRED",
        "policy_id": policy_id,
        "policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "recommended_option": recommendation.get("recommended_option"),
        "proposal_recommendation": recommendation,
        "human_decision_boundary": {
            "required": True,
            "reason": "Candidate acceptance and any registry write remain outside proposal authority.",
            "decision_required_from": "human_operator",
            "valid_options": human_options,
            "default_if_no_decision": "NO_ACCEPTANCE_NO_REGISTRY_WRITE",
        },
        "evidence_stack": {
            "source_review": {
                "review_id": SOURCE_REVIEW_ID,
                "review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
            },
            "current_approved_new_bounded_surface_probe": evidence_stack.get("current_approved_new_bounded_surface_probe"),
            "prior_raw_delta_candidate_bounded_probe": evidence_stack.get("prior_raw_delta_candidate_bounded_probe"),
            "bounded_scale_out_replay": evidence_stack.get("bounded_scale_out_replay"),
        },
        "bounded_acceptance_claim_if_approved": {
            "claim": "RAW_DELTA_SIGNATURE_CANDIDATE_V0 is provisionally bounded-accepted under the cited evidence stack.",
            "scope": "bounded_evidence_only",
            "not_claimed": [
                "global correctness",
                "runtime semantic correctness",
                "mathematical finality",
                "irreversibility",
                "authority to change runtime",
            ],
            "reversible_by_later_failure_evidence": True,
        },
        "safety_clauses": {
            "proposal_only": True,
            "candidate_accepted": False,
            "registry_written": False,
            "runtime_changed": False,
            "runner_executed": False,
            "human_decision_required_before_acceptance": True,
        },
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_HUMAN_DECISION_REQUIRED",
            "next_command_goal": HUMAN_DECISION_GOAL,
        },
        "authority_guards": {
            "runner_executed": False,
            "candidate_rows_created": False,
            "candidate_accepted": False,
            "scale_mode_authorized": False,
            "registry_inserted": False,
            "registry_written": False,
            "registry_sqlite_read": False,
            "full_registry_scan_used": False,
            "runtime_semantic_changed": False,
            "runtime_code_changed": False,
            "runtime_receipt_emission_changed": False,
            "latest_or_mtime_selection_used": False,
            "ambient_workspace_inference_used": False,
            "case_id_or_cycle_n_identity_patch_used": False,
            "rowid_or_receipt_hash_truth_surface_used": False,
            "full_occurrence_key_in_signature_payload": False,
            "audit_or_debug_payload_in_signature_payload": False,
            "microhash_as_proof_used": False,
            "synthetic_fake_validation_rows_used": False,
            "transition_compression_probe_run": False,
            "candidate_acceptance_proposal_emitted": True,
            "human_decision_boundary_emitted": True,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt = {
        "schema_version": "raw_delta_signature_candidate_acceptance_proposal_receipt_v0",
        "receipt_type": "RAW_DELTA_SIGNATURE_CANDIDATE_ACCEPTANCE_PROPOSAL_RECEIPT",
        "proposal_name": PROPOSAL_NAME,
        "proposal_id": proposal_id,
        "proposal_status": proposal["proposal_status"],
        "policy_id": policy_id,
        "policy_receipt_id": EXPECTED_POLICY_RECEIPT_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_review_id": SOURCE_REVIEW_ID,
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_probe_id": SOURCE_PROBE_ID,
        "source_probe_receipt_id": SOURCE_PROBE_RECEIPT_ID,
        "source_surface_id": SOURCE_SURFACE_ID,
        "source_surface_receipt_id": SOURCE_SURFACE_RECEIPT_ID,
        "prior_probe_id": PRIOR_PROBE_ID,
        "prior_probe_receipt_id": PRIOR_PROBE_RECEIPT_ID,
        "scale_out_id": SCALE_OUT_ID,
        "scale_out_receipt_id": SCALE_OUT_RECEIPT_ID,
        "recommended_option": recommendation.get("recommended_option"),
        "human_decision_required": True,
        "valid_human_options": list(human_options.keys()),
        "safety_clauses": proposal["safety_clauses"],
        "terminal": proposal["terminal"],
        "authority_guards": proposal["authority_guards"],
        "gate": proposal["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id
    proposal["receipt_id"] = receipt_id

    if write_outputs:
        (OUT_DIR / f"{proposal_id}.json").write_text(json.dumps(proposal, indent=2, sort_keys=True))
        (OUT_RECEIPT_DIR / f"{proposal_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True))

    return proposal, receipt


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-id", default=EXPECTED_POLICY_ID)
    args = parser.parse_args()

    proposal, receipt = build_proposal(args.policy_id, write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"proposal_id={proposal['proposal_id']}")
    print(f"proposal_receipt_id={receipt['receipt_id']}")
    print(f"proposal_path=data/raw_delta_signature_candidate_acceptance_proposals/{proposal['proposal_id']}.json")
    print(f"proposal_receipt_path=data/raw_delta_signature_candidate_acceptance_proposal_receipts/{proposal['proposal_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
