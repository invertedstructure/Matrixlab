#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_PROVISIONAL_BOUNDED_ACCEPTANCE_POLICY_V0"
NEXT_GOAL = "EMIT_RAW_DELTA_SIGNATURE_CANDIDATE_PROVISIONAL_BOUNDED_ACCEPTANCE_RECORD_V0"

DECISION_ID = "b2fca9d8"
DECISION_RECEIPT_ID = "d0e9f235"
PROPOSAL_ID = "ab545dbf"
PROPOSAL_RECEIPT_ID = "ec67d9dc"

POLICY_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_PROVISIONAL_BOUNDED_ACCEPTANCE_POLICY_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"

EXPECTED_DECISION_OPTION = "OPTION_A_PROVISIONAL_BOUNDED_ACCEPT"

PROPOSAL_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposals" / f"{PROPOSAL_ID}.json"
PROPOSAL_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposal_receipts" / f"{PROPOSAL_ID}.json"
DECISION_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_human_decisions" / f"{DECISION_ID}.json"
DECISION_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_human_decision_receipts" / f"{DECISION_ID}.json"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_policy_receipts"

AUTHORITY_FALSE_REQUIRED = [
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

def validate_inputs(
    proposal: dict[str, Any],
    proposal_receipt: dict[str, Any],
    decision: dict[str, Any],
    decision_receipt: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal_receipt.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_receipt_proposal_id_wrong:{proposal_receipt.get('proposal_id')}")
    if proposal.get("receipt_id") != PROPOSAL_RECEIPT_ID:
        failures.append(f"proposal_receipt_id_wrong:{proposal.get('receipt_id')}")
    if proposal_receipt.get("receipt_id") != PROPOSAL_RECEIPT_ID:
        failures.append(f"proposal_receipt_id_wrong:{proposal_receipt.get('receipt_id')}")

    if decision.get("decision_id") != DECISION_ID:
        failures.append(f"decision_id_wrong:{decision.get('decision_id')}")
    if decision_receipt.get("decision_id") != DECISION_ID:
        failures.append(f"decision_receipt_decision_id_wrong:{decision_receipt.get('decision_id')}")
    if decision.get("receipt_id") != DECISION_RECEIPT_ID:
        failures.append(f"decision_receipt_id_wrong:{decision.get('receipt_id')}")
    if decision_receipt.get("receipt_id") != DECISION_RECEIPT_ID:
        failures.append(f"decision_receipt_id_wrong:{decision_receipt.get('receipt_id')}")

    for label, obj in [
        ("proposal", proposal),
        ("proposal_receipt", proposal_receipt),
        ("decision", decision),
        ("decision_receipt", decision_receipt),
    ]:
        if obj.get("gate") != "PASS":
            failures.append(f"{label}_gate_not_PASS:{obj.get('gate')}")
        if obj.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
            failures.append(f"{label}_candidate_design_id_wrong:{obj.get('candidate_design_id')}")

    if decision.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"decision_proposal_id_wrong:{decision.get('proposal_id')}")
    if decision_receipt.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"decision_receipt_proposal_id_wrong:{decision_receipt.get('proposal_id')}")
    if decision.get("proposal_receipt_id") != PROPOSAL_RECEIPT_ID:
        failures.append(f"decision_proposal_receipt_id_wrong:{decision.get('proposal_receipt_id')}")
    if decision_receipt.get("proposal_receipt_id") != PROPOSAL_RECEIPT_ID:
        failures.append(f"decision_receipt_proposal_receipt_id_wrong:{decision_receipt.get('proposal_receipt_id')}")

    if decision_receipt.get("decision_status") != "HUMAN_DECISION_RECORDED":
        failures.append(f"decision_status_wrong:{decision_receipt.get('decision_status')}")
    if decision_receipt.get("human_decision_option") != EXPECTED_DECISION_OPTION:
        failures.append(f"decision_option_wrong:{decision_receipt.get('human_decision_option')}")
    if decision_receipt.get("recommended_option_accepted") is not True:
        failures.append(f"recommended_option_accepted_not_true:{decision_receipt.get('recommended_option_accepted')}")
    if decision_receipt.get("bounded_scope_preserved") is not True:
        failures.append(f"bounded_scope_preserved_not_true:{decision_receipt.get('bounded_scope_preserved')}")

    for key in [
        "does_not_accept_candidate",
        "does_not_write_registry",
        "does_not_change_runtime",
        "next_policy_required_before_acceptance",
    ]:
        if decision_receipt.get(key) is not True:
            failures.append(f"decision_receipt_{key}_not_true:{decision_receipt.get(key)}")

    terminal = decision_receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"decision_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"decision_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"decision_terminal_stop_code_not_null:{terminal.get('stop_code')}")

    guards = decision_receipt.get("authority_guards") or {}
    for key in AUTHORITY_FALSE_REQUIRED:
        if guards.get(key) is not False:
            failures.append(f"authority_guard_not_false:{key}:{guards.get(key)}")
    if guards.get("candidate_acceptance_proposal_emitted") is not True:
        failures.append(f"proposal_emitted_guard_not_true:{guards.get('candidate_acceptance_proposal_emitted')}")
    if guards.get("human_decision_boundary_emitted") is not True:
        failures.append(f"human_boundary_guard_not_true:{guards.get('human_decision_boundary_emitted')}")
    if guards.get("human_decision_recorded") is not True:
        failures.append(f"human_decision_recorded_guard_not_true:{guards.get('human_decision_recorded')}")

    return failures

def build_policy(write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    proposal = load_json(PROPOSAL_PATH)
    proposal_receipt = load_json(PROPOSAL_RECEIPT_PATH)
    decision = load_json(DECISION_PATH)
    decision_receipt = load_json(DECISION_RECEIPT_PATH)

    failures = validate_inputs(proposal, proposal_receipt, decision, decision_receipt)

    policy_seed = {
        "policy_name": POLICY_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "proposal_id": PROPOSAL_ID,
        "proposal_receipt_id": PROPOSAL_RECEIPT_ID,
        "decision_id": DECISION_ID,
        "decision_receipt_id": DECISION_RECEIPT_ID,
        "human_decision_option": EXPECTED_DECISION_OPTION,
    }
    policy_id = sha8(policy_seed)

    authority_guards = dict(decision_receipt.get("authority_guards") or {})
    authority_guards["provisional_bounded_acceptance_policy_built"] = True
    authority_guards["candidate_accepted"] = False
    authority_guards["registry_written"] = False
    authority_guards["registry_inserted"] = False
    authority_guards["runtime_code_changed"] = False
    authority_guards["runtime_semantic_changed"] = False
    authority_guards["runtime_receipt_emission_changed"] = False
    authority_guards["runner_executed"] = False

    policy = {
        "schema_version": "raw_delta_signature_candidate_provisional_bounded_acceptance_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_id": policy_id,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_receipt_id": PROPOSAL_RECEIPT_ID,
        "source_decision_id": DECISION_ID,
        "source_decision_receipt_id": DECISION_RECEIPT_ID,
        "human_decision_option": EXPECTED_DECISION_OPTION,
        "policy_meaning": "Authorize the next separate unit to emit a provisional bounded acceptance record for RAW_DELTA_SIGNATURE_CANDIDATE_V0 under the cited bounded evidence stack.",
        "acceptance_scope": proposal.get("acceptance_scope"),
        "bounded_acceptance_claim_if_emitted": {
            "candidate_design_id": CANDIDATE_DESIGN_ID,
            "scope": "bounded_evidence_only",
            "allowed_claim": "candidate is provisionally bounded accepted under cited evidence stack",
            "not_claimed": [
                "global correctness",
                "runtime semantic correctness",
                "mathematical finality",
                "irreversibility",
                "authority to change runtime",
            ],
            "reversible_by_later_failure_evidence": True,
        },
        "authorized_operations_next": {
            "read_source_proposal": True,
            "read_source_proposal_receipt": True,
            "read_human_decision": True,
            "read_human_decision_receipt": True,
            "write_provisional_bounded_acceptance_record": True,
            "write_provisional_bounded_acceptance_receipt": True,
        },
        "forbidden_operations": {
            "candidate_registry_insert": True,
            "candidate_registry_write": True,
            "registry_sqlite_read": True,
            "registry_sqlite_write": True,
            "full_registry_scan": True,
            "runner_execution": True,
            "runtime_code_change": True,
            "runtime_semantic_change": True,
            "runtime_receipt_emission_change": True,
            "scale_mode": True,
            "latest_or_mtime_selection": True,
            "ambient_workspace_inference": True,
            "case_id_or_cycle_n_identity_patch": True,
            "rowid_or_receipt_hash_truth_surface": True,
            "full_occurrence_key_in_signature_payload": True,
            "audit_or_debug_payload_in_signature_payload": True,
            "microhash_as_proof": True,
            "synthetic_fake_rows": True,
        },
        "safety_clauses": {
            "policy_only": True,
            "candidate_not_accepted_by_policy": True,
            "registry_not_written_by_policy": True,
            "runtime_not_changed_by_policy": True,
            "bounded_scope_explicit": True,
            "human_decision_recorded": True,
            "separate_acceptance_record_required": True,
        },
        "authority_guards": authority_guards,
        "terminal": {
            "type": "ADVANCE",
            "next_command_goal": NEXT_GOAL,
            "stop_code": None,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt = {
        "schema_version": "raw_delta_signature_candidate_provisional_bounded_acceptance_policy_receipt_v0",
        "receipt_type": "RAW_DELTA_SIGNATURE_CANDIDATE_PROVISIONAL_BOUNDED_ACCEPTANCE_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "policy_name": POLICY_NAME,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_receipt_id": PROPOSAL_RECEIPT_ID,
        "source_decision_id": DECISION_ID,
        "source_decision_receipt_id": DECISION_RECEIPT_ID,
        "human_decision_option": EXPECTED_DECISION_OPTION,
        "authorized_operations_next": policy["authorized_operations_next"],
        "forbidden_operations": policy["forbidden_operations"],
        "safety_clauses": policy["safety_clauses"],
        "authority_guards": authority_guards,
        "terminal": policy["terminal"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id
    policy["policy_receipt_id"] = receipt_id

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / f"{policy_id}.json").write_text(json.dumps(policy, indent=2, sort_keys=True) + "\n")
        (OUT_RECEIPT_DIR / f"{policy_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")

    return policy, receipt

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--decision-id", default=DECISION_ID)
    parser.add_argument("--decision-receipt-id", default=DECISION_RECEIPT_ID)
    args = parser.parse_args()

    if args.decision_id != DECISION_ID:
        raise SystemExit(f"unsupported decision id: {args.decision_id}")
    if args.decision_receipt_id != DECISION_RECEIPT_ID:
        raise SystemExit(f"unsupported decision receipt id: {args.decision_receipt_id}")

    policy, receipt = build_policy(write_outputs=True)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"acceptance_policy_id={policy['policy_id']}")
    print(f"acceptance_policy_receipt_id={receipt['receipt_id']}")
    print(f"acceptance_policy_path=data/raw_delta_signature_candidate_provisional_bounded_acceptance_policies/{policy['policy_id']}.json")
    print(f"acceptance_policy_receipt_path=data/raw_delta_signature_candidate_provisional_bounded_acceptance_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
