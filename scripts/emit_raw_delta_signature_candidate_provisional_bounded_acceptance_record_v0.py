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

UNIT_ID = "EMIT_RAW_DELTA_SIGNATURE_CANDIDATE_PROVISIONAL_BOUNDED_ACCEPTANCE_RECORD_V0"
NEXT_GOAL = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_REGISTRY_WRITE_POLICY_V0"

POLICY_ID = "a371381b"
POLICY_RECEIPT_ID = "6e1773c8"
DECISION_ID = "b2fca9d8"
DECISION_RECEIPT_ID = "d0e9f235"
PROPOSAL_ID = "ab545dbf"
PROPOSAL_RECEIPT_ID = "ec67d9dc"

CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
EXPECTED_DECISION_OPTION = "OPTION_A_PROVISIONAL_BOUNDED_ACCEPT"

POLICY_PATH = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_policies" / f"{POLICY_ID}.json"
POLICY_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_policy_receipts" / f"{POLICY_ID}.json"
DECISION_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_human_decisions" / f"{DECISION_ID}.json"
DECISION_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_human_decision_receipts" / f"{DECISION_ID}.json"
PROPOSAL_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposals" / f"{PROPOSAL_ID}.json"
PROPOSAL_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposal_receipts" / f"{PROPOSAL_ID}.json"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_records"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_record_receipts"

PRE_RECORD_FALSE_GUARDS = [
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

POST_RECORD_FALSE_GUARDS = [
    "runner_executed",
    "candidate_rows_created",
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
    policy: dict[str, Any],
    policy_receipt: dict[str, Any],
    decision: dict[str, Any],
    decision_receipt: dict[str, Any],
    proposal: dict[str, Any],
    proposal_receipt: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if policy.get("policy_id") != POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy_receipt.get("policy_id") != POLICY_ID:
        failures.append(f"policy_receipt_policy_id_wrong:{policy_receipt.get('policy_id')}")
    if policy.get("policy_receipt_id") != POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if policy_receipt.get("receipt_id") != POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy_receipt.get('receipt_id')}")

    if decision.get("decision_id") != DECISION_ID:
        failures.append(f"decision_id_wrong:{decision.get('decision_id')}")
    if decision_receipt.get("decision_id") != DECISION_ID:
        failures.append(f"decision_receipt_decision_id_wrong:{decision_receipt.get('decision_id')}")
    if decision.get("receipt_id") != DECISION_RECEIPT_ID:
        failures.append(f"decision_receipt_id_wrong:{decision.get('receipt_id')}")
    if decision_receipt.get("receipt_id") != DECISION_RECEIPT_ID:
        failures.append(f"decision_receipt_id_wrong:{decision_receipt.get('receipt_id')}")

    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal_receipt.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_receipt_proposal_id_wrong:{proposal_receipt.get('proposal_id')}")
    if proposal.get("receipt_id") != PROPOSAL_RECEIPT_ID:
        failures.append(f"proposal_receipt_id_wrong:{proposal.get('receipt_id')}")
    if proposal_receipt.get("receipt_id") != PROPOSAL_RECEIPT_ID:
        failures.append(f"proposal_receipt_id_wrong:{proposal_receipt.get('receipt_id')}")

    for label, obj in [
        ("policy", policy),
        ("policy_receipt", policy_receipt),
        ("decision", decision),
        ("decision_receipt", decision_receipt),
        ("proposal", proposal),
        ("proposal_receipt", proposal_receipt),
    ]:
        if obj.get("gate") != "PASS":
            failures.append(f"{label}_gate_not_PASS:{obj.get('gate')}")
        if obj.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
            failures.append(f"{label}_candidate_design_id_wrong:{obj.get('candidate_design_id')}")

    if policy_receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy_receipt.get('policy_status')}")
    if decision_receipt.get("decision_status") != "HUMAN_DECISION_RECORDED":
        failures.append(f"decision_status_wrong:{decision_receipt.get('decision_status')}")
    if decision_receipt.get("human_decision_option") != EXPECTED_DECISION_OPTION:
        failures.append(f"decision_option_wrong:{decision_receipt.get('human_decision_option')}")
    if decision_receipt.get("recommended_option_accepted") is not True:
        failures.append(f"recommended_option_accepted_not_true:{decision_receipt.get('recommended_option_accepted')}")

    if policy_receipt.get("source_decision_id") != DECISION_ID:
        failures.append(f"policy_source_decision_id_wrong:{policy_receipt.get('source_decision_id')}")
    if policy_receipt.get("source_decision_receipt_id") != DECISION_RECEIPT_ID:
        failures.append(f"policy_source_decision_receipt_id_wrong:{policy_receipt.get('source_decision_receipt_id')}")
    if policy_receipt.get("source_proposal_id") != PROPOSAL_ID:
        failures.append(f"policy_source_proposal_id_wrong:{policy_receipt.get('source_proposal_id')}")
    if policy_receipt.get("source_proposal_receipt_id") != PROPOSAL_RECEIPT_ID:
        failures.append(f"policy_source_proposal_receipt_id_wrong:{policy_receipt.get('source_proposal_receipt_id')}")

    authorized = policy_receipt.get("authorized_operations_next") or {}
    for key in [
        "read_source_proposal",
        "read_source_proposal_receipt",
        "read_human_decision",
        "read_human_decision_receipt",
        "write_provisional_bounded_acceptance_record",
        "write_provisional_bounded_acceptance_receipt",
    ]:
        if authorized.get(key) is not True:
            failures.append(f"authorized_next_not_true:{key}:{authorized.get(key)}")

    forbidden = policy_receipt.get("forbidden_operations") or {}
    for key, value in forbidden.items():
        if value is not True:
            failures.append(f"forbidden_operation_not_true:{key}:{value}")

    safety = policy_receipt.get("safety_clauses") or {}
    expected_safety = {
        "policy_only": True,
        "candidate_not_accepted_by_policy": True,
        "registry_not_written_by_policy": True,
        "runtime_not_changed_by_policy": True,
        "bounded_scope_explicit": True,
        "human_decision_recorded": True,
        "separate_acceptance_record_required": True,
    }
    for key, expected in expected_safety.items():
        if safety.get(key) is not expected:
            failures.append(f"policy_safety_wrong:{key}:{safety.get(key)}")

    terminal = policy_receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"policy_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"policy_terminal_stop_code_not_null:{terminal.get('stop_code')}")

    guards = policy_receipt.get("authority_guards") or {}
    for key in PRE_RECORD_FALSE_GUARDS:
        if guards.get(key) is not False:
            failures.append(f"pre_record_authority_guard_not_false:{key}:{guards.get(key)}")
    for key in [
        "candidate_acceptance_proposal_emitted",
        "human_decision_boundary_emitted",
        "human_decision_recorded",
        "provisional_bounded_acceptance_policy_built",
    ]:
        if guards.get(key) is not True:
            failures.append(f"authority_guard_not_true:{key}:{guards.get(key)}")

    return failures

def build_record(write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    policy = load_json(POLICY_PATH)
    policy_receipt = load_json(POLICY_RECEIPT_PATH)
    decision = load_json(DECISION_PATH)
    decision_receipt = load_json(DECISION_RECEIPT_PATH)
    proposal = load_json(PROPOSAL_PATH)
    proposal_receipt = load_json(PROPOSAL_RECEIPT_PATH)

    failures = validate_inputs(policy, policy_receipt, decision, decision_receipt, proposal, proposal_receipt)

    record_seed = {
        "unit_id": UNIT_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "policy_id": POLICY_ID,
        "policy_receipt_id": POLICY_RECEIPT_ID,
        "decision_id": DECISION_ID,
        "decision_receipt_id": DECISION_RECEIPT_ID,
        "proposal_id": PROPOSAL_ID,
        "proposal_receipt_id": PROPOSAL_RECEIPT_ID,
        "acceptance_kind": "PROVISIONAL_BOUNDED",
    }
    record_id = sha8(record_seed)

    authority_guards = dict(policy_receipt.get("authority_guards") or {})
    authority_guards["provisional_bounded_acceptance_record_emitted"] = True
    authority_guards["candidate_accepted"] = True
    authority_guards["candidate_acceptance_kind"] = "PROVISIONAL_BOUNDED_ONLY"
    authority_guards["registry_written"] = False
    authority_guards["registry_inserted"] = False
    authority_guards["registry_sqlite_read"] = False
    authority_guards["runtime_code_changed"] = False
    authority_guards["runtime_semantic_changed"] = False
    authority_guards["runtime_receipt_emission_changed"] = False
    authority_guards["runner_executed"] = False

    acceptance_scope = policy.get("acceptance_scope") or proposal.get("acceptance_scope")

    record = {
        "schema_version": "raw_delta_signature_candidate_provisional_bounded_acceptance_record_v0",
        "record_type": "RAW_DELTA_SIGNATURE_CANDIDATE_PROVISIONAL_BOUNDED_ACCEPTANCE_RECORD",
        "unit_id": UNIT_ID,
        "record_id": record_id,
        "record_status": "PROVISIONAL_BOUNDED_ACCEPTANCE_RECORDED",
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "acceptance_kind": "PROVISIONAL_BOUNDED",
        "accepted_under_bounded_scope": True,
        "source_policy_id": POLICY_ID,
        "source_policy_receipt_id": POLICY_RECEIPT_ID,
        "source_decision_id": DECISION_ID,
        "source_decision_receipt_id": DECISION_RECEIPT_ID,
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_receipt_id": PROPOSAL_RECEIPT_ID,
        "human_decision_option": EXPECTED_DECISION_OPTION,
        "acceptance_scope": acceptance_scope,
        "bounded_acceptance_claim": {
            "claim": "RAW_DELTA_SIGNATURE_CANDIDATE_V0 is provisionally bounded accepted under the cited evidence stack.",
            "scope": "bounded_evidence_only",
            "not_claimed": [
                "global correctness",
                "runtime semantic correctness",
                "mathematical finality",
                "irreversibility",
                "registry insertion",
                "runtime change",
            ],
            "reversible_by_later_failure_evidence": True,
        },
        "safety_clauses": {
            "provisional_bounded_acceptance_record": True,
            "candidate_provisionally_bounded_accepted": True,
            "candidate_acceptance_kind": "PROVISIONAL_BOUNDED_ONLY",
            "registry_written": False,
            "registry_inserted": False,
            "runtime_changed": False,
            "runner_executed": False,
            "bounded_scope_explicit": True,
            "global_correctness_not_claimed": True,
            "registry_write_requires_separate_policy": True,
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
        "schema_version": "raw_delta_signature_candidate_provisional_bounded_acceptance_record_receipt_v0",
        "receipt_type": "RAW_DELTA_SIGNATURE_CANDIDATE_PROVISIONAL_BOUNDED_ACCEPTANCE_RECORD_RECEIPT",
        "unit_id": UNIT_ID,
        "record_id": record_id,
        "record_status": record["record_status"],
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "acceptance_kind": "PROVISIONAL_BOUNDED",
        "accepted_under_bounded_scope": True,
        "source_policy_id": POLICY_ID,
        "source_policy_receipt_id": POLICY_RECEIPT_ID,
        "source_decision_id": DECISION_ID,
        "source_decision_receipt_id": DECISION_RECEIPT_ID,
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_receipt_id": PROPOSAL_RECEIPT_ID,
        "human_decision_option": EXPECTED_DECISION_OPTION,
        "safety_clauses": record["safety_clauses"],
        "authority_guards": authority_guards,
        "terminal": record["terminal"],
        "gate": record["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id
    record["receipt_id"] = receipt_id

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / f"{record_id}.json").write_text(json.dumps(record, indent=2, sort_keys=True) + "\n")
        (OUT_RECEIPT_DIR / f"{record_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")

    return record, receipt

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--policy-id", default=POLICY_ID)
    parser.add_argument("--policy-receipt-id", default=POLICY_RECEIPT_ID)
    args = parser.parse_args()

    if args.policy_id != POLICY_ID:
        raise SystemExit(f"unsupported acceptance policy id: {args.policy_id}")
    if args.policy_receipt_id != POLICY_RECEIPT_ID:
        raise SystemExit(f"unsupported acceptance policy receipt id: {args.policy_receipt_id}")

    record, receipt = build_record(write_outputs=True)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"acceptance_record_id={record['record_id']}")
    print(f"acceptance_record_receipt_id={receipt['receipt_id']}")
    print(f"acceptance_record_path=data/raw_delta_signature_candidate_provisional_bounded_acceptance_records/{record['record_id']}.json")
    print(f"acceptance_record_receipt_path=data/raw_delta_signature_candidate_provisional_bounded_acceptance_record_receipts/{record['record_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
