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

UNIT_ID = "RECORD_RAW_DELTA_SIGNATURE_CANDIDATE_ACCEPTANCE_HUMAN_DECISION_V0"
NEXT_GOAL = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_PROVISIONAL_BOUNDED_ACCEPTANCE_POLICY_V0"

PROPOSAL_ID = "ab545dbf"
PROPOSAL_RECEIPT_ID = "ec67d9dc"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"

EXPECTED_DECISION = "OPTION_A_PROVISIONAL_BOUNDED_ACCEPT"
EXPECTED_RECOMMENDATION = "OPTION_A_PROVISIONAL_BOUNDED_ACCEPTANCE_PROPOSAL"

PROPOSAL_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposals" / f"{PROPOSAL_ID}.json"
PROPOSAL_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposal_receipts" / f"{PROPOSAL_ID}.json"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_acceptance_human_decisions"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_acceptance_human_decision_receipts"

AUTHORITY_GUARDS_FALSE_REQUIRED = [
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

def validate_proposal(proposal: dict[str, Any], receipt: dict[str, Any], decision: str) -> list[str]:
    failures: list[str] = []

    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if receipt.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"receipt_proposal_id_wrong:{receipt.get('proposal_id')}")
    if proposal.get("receipt_id") != PROPOSAL_RECEIPT_ID:
        failures.append(f"proposal_receipt_id_wrong:{proposal.get('receipt_id')}")
    if receipt.get("receipt_id") != PROPOSAL_RECEIPT_ID:
        failures.append(f"receipt_id_wrong:{receipt.get('receipt_id')}")

    if proposal.get("gate") != "PASS":
        failures.append(f"proposal_gate_not_PASS:{proposal.get('gate')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"proposal_receipt_gate_not_PASS:{receipt.get('gate')}")

    if proposal.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"candidate_design_id_wrong:{proposal.get('candidate_design_id')}")
    if receipt.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"receipt_candidate_design_id_wrong:{receipt.get('candidate_design_id')}")

    if proposal.get("proposal_status") != "HUMAN_DECISION_REQUIRED":
        failures.append(f"proposal_status_not_HUMAN_DECISION_REQUIRED:{proposal.get('proposal_status')}")
    if receipt.get("proposal_status") != "HUMAN_DECISION_REQUIRED":
        failures.append(f"receipt_proposal_status_not_HUMAN_DECISION_REQUIRED:{receipt.get('proposal_status')}")

    if proposal.get("recommended_option") != EXPECTED_RECOMMENDATION:
        failures.append(f"proposal_recommendation_wrong:{proposal.get('recommended_option')}")
    if receipt.get("recommended_option") != EXPECTED_RECOMMENDATION:
        failures.append(f"receipt_recommendation_wrong:{receipt.get('recommended_option')}")

    if receipt.get("human_decision_required") is not True:
        failures.append(f"human_decision_required_not_true:{receipt.get('human_decision_required')}")

    if decision != EXPECTED_DECISION:
        failures.append(f"decision_not_expected:{decision}")

    valid_options = set(receipt.get("valid_human_options") or [])
    if decision not in valid_options:
        failures.append(f"decision_not_in_valid_options:{decision}")

    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_HUMAN_DECISION_REQUIRED":
        failures.append(f"terminal_stop_wrong:{terminal.get('stop_code')}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"terminal_next_wrong:{terminal.get('next_command_goal')}")

    safety = receipt.get("safety_clauses") or {}
    expected_safety = {
        "proposal_only": True,
        "candidate_accepted": False,
        "registry_written": False,
        "runtime_changed": False,
        "runner_executed": False,
        "human_decision_required_before_acceptance": True,
    }
    for key, expected in expected_safety.items():
        if safety.get(key) is not expected:
            failures.append(f"safety_clause_wrong:{key}:{safety.get(key)}")

    proposal_boundary = proposal.get("human_decision_boundary") or {}
    if proposal_boundary.get("required") is not True:
        failures.append(f"proposal_boundary_required_not_true:{proposal_boundary.get('required')}")
    if proposal_boundary.get("default_if_no_decision") != "NO_ACCEPTANCE_NO_REGISTRY_WRITE":
        failures.append(f"proposal_boundary_default_wrong:{proposal_boundary.get('default_if_no_decision')}")

    guards = receipt.get("authority_guards") or {}
    for key in AUTHORITY_GUARDS_FALSE_REQUIRED:
        if guards.get(key) is not False:
            failures.append(f"authority_guard_not_false:{key}:{guards.get(key)}")
    if guards.get("candidate_acceptance_proposal_emitted") is not True:
        failures.append(f"proposal_emitted_guard_not_true:{guards.get('candidate_acceptance_proposal_emitted')}")
    if guards.get("human_decision_boundary_emitted") is not True:
        failures.append(f"human_boundary_guard_not_true:{guards.get('human_decision_boundary_emitted')}")

    return failures

def build_decision(decision: str, write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    proposal = load_json(PROPOSAL_PATH)
    proposal_receipt = load_json(PROPOSAL_RECEIPT_PATH)

    failures = validate_proposal(proposal, proposal_receipt, decision)

    decision_seed = {
        "unit_id": UNIT_ID,
        "proposal_id": PROPOSAL_ID,
        "proposal_receipt_id": PROPOSAL_RECEIPT_ID,
        "decision": decision,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
    }
    decision_id = sha8(decision_seed)

    authority_guards = dict(proposal_receipt.get("authority_guards") or {})
    authority_guards["human_decision_recorded"] = True
    authority_guards["candidate_accepted"] = False
    authority_guards["registry_written"] = False
    authority_guards["registry_inserted"] = False
    authority_guards["runtime_code_changed"] = False
    authority_guards["runtime_semantic_changed"] = False
    authority_guards["runtime_receipt_emission_changed"] = False
    authority_guards["runner_executed"] = False

    decision_obj = {
        "schema_version": "raw_delta_signature_candidate_acceptance_human_decision_v0",
        "decision_id": decision_id,
        "unit_id": UNIT_ID,
        "decision_status": "HUMAN_DECISION_RECORDED",
        "human_decision_option": decision,
        "decision_meaning": "Human operator approves proceeding toward a separate provisional bounded acceptance policy for RAW_DELTA_SIGNATURE_CANDIDATE_V0 under the cited bounded evidence stack.",
        "proposal_id": PROPOSAL_ID,
        "proposal_receipt_id": PROPOSAL_RECEIPT_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "recommended_option_accepted": decision == EXPECTED_DECISION,
        "bounded_scope_preserved": True,
        "does_not_accept_candidate": True,
        "does_not_write_registry": True,
        "does_not_change_runtime": True,
        "next_policy_required_before_acceptance": True,
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
        "schema_version": "raw_delta_signature_candidate_acceptance_human_decision_receipt_v0",
        "receipt_type": "RAW_DELTA_SIGNATURE_CANDIDATE_ACCEPTANCE_HUMAN_DECISION_RECEIPT",
        "unit_id": UNIT_ID,
        "decision_id": decision_id,
        "decision_status": decision_obj["decision_status"],
        "human_decision_option": decision,
        "proposal_id": PROPOSAL_ID,
        "proposal_receipt_id": PROPOSAL_RECEIPT_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "recommended_option_accepted": decision_obj["recommended_option_accepted"],
        "bounded_scope_preserved": True,
        "does_not_accept_candidate": True,
        "does_not_write_registry": True,
        "does_not_change_runtime": True,
        "next_policy_required_before_acceptance": True,
        "authority_guards": authority_guards,
        "terminal": decision_obj["terminal"],
        "gate": decision_obj["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id
    decision_obj["receipt_id"] = receipt_id

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / f"{decision_id}.json").write_text(json.dumps(decision_obj, indent=2, sort_keys=True) + "\n")
        (OUT_RECEIPT_DIR / f"{decision_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")

    return decision_obj, receipt

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--proposal-id", default=PROPOSAL_ID)
    parser.add_argument("--proposal-receipt-id", default=PROPOSAL_RECEIPT_ID)
    parser.add_argument("--decision", required=True)
    args = parser.parse_args()

    if args.proposal_id != PROPOSAL_ID:
        raise SystemExit(f"unsupported proposal id: {args.proposal_id}")
    if args.proposal_receipt_id != PROPOSAL_RECEIPT_ID:
        raise SystemExit(f"unsupported proposal receipt id: {args.proposal_receipt_id}")

    decision_obj, receipt = build_decision(args.decision, write_outputs=True)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"decision_id={decision_obj['decision_id']}")
    print(f"decision_receipt_id={receipt['receipt_id']}")
    print(f"decision_path=data/raw_delta_signature_candidate_acceptance_human_decisions/{decision_obj['decision_id']}.json")
    print(f"decision_receipt_path=data/raw_delta_signature_candidate_acceptance_human_decision_receipts/{decision_obj['decision_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
