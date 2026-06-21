#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_RAW_DELTA_SIGNATURE_CANDIDATE_REGISTRY_WRITE_POLICY_V0"
NEXT_GOAL = "EMIT_RAW_DELTA_SIGNATURE_CANDIDATE_REGISTRY_WRITE_RECORD_V0"

POLICY_NAME = "RAW_DELTA_SIGNATURE_CANDIDATE_REGISTRY_WRITE_POLICY_V0"
CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"

ACCEPTANCE_RECORD_ID = "fe19fa23"
ACCEPTANCE_RECORD_RECEIPT_ID = "f5db8634"
ACCEPTANCE_POLICY_ID = "a371381b"
ACCEPTANCE_POLICY_RECEIPT_ID = "6e1773c8"
DECISION_ID = "b2fca9d8"
DECISION_RECEIPT_ID = "d0e9f235"
PROPOSAL_ID = "ab545dbf"
PROPOSAL_RECEIPT_ID = "ec67d9dc"

ACCEPTANCE_KIND = "PROVISIONAL_BOUNDED"
CANDIDATE_ACCEPTANCE_KIND = "PROVISIONAL_BOUNDED_ONLY"

ACCEPTANCE_RECORD_PATH = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_records" / f"{ACCEPTANCE_RECORD_ID}.json"
ACCEPTANCE_RECORD_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_record_receipts" / f"{ACCEPTANCE_RECORD_ID}.json"
ACCEPTANCE_POLICY_PATH = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_policies" / f"{ACCEPTANCE_POLICY_ID}.json"
ACCEPTANCE_POLICY_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_policy_receipts" / f"{ACCEPTANCE_POLICY_ID}.json"
DECISION_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_human_decisions" / f"{DECISION_ID}.json"
DECISION_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_human_decision_receipts" / f"{DECISION_ID}.json"
PROPOSAL_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposals" / f"{PROPOSAL_ID}.json"
PROPOSAL_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposal_receipts" / f"{PROPOSAL_ID}.json"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_registry_write_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_registry_write_policy_receipts"

REQUIRED_FALSE_GUARDS = [
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

REQUIRED_TRUE_GUARDS = [
    "candidate_acceptance_proposal_emitted",
    "human_decision_boundary_emitted",
    "human_decision_recorded",
    "provisional_bounded_acceptance_policy_built",
    "provisional_bounded_acceptance_record_emitted",
    "candidate_accepted",
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
    acceptance_record: dict[str, Any],
    acceptance_record_receipt: dict[str, Any],
    acceptance_policy: dict[str, Any],
    acceptance_policy_receipt: dict[str, Any],
    decision: dict[str, Any],
    decision_receipt: dict[str, Any],
    proposal: dict[str, Any],
    proposal_receipt: dict[str, Any],
) -> list[str]:
    failures: list[str] = []

    if acceptance_record.get("record_id") != ACCEPTANCE_RECORD_ID:
        failures.append(f"acceptance_record_id_wrong:{acceptance_record.get('record_id')}")
    if acceptance_record_receipt.get("record_id") != ACCEPTANCE_RECORD_ID:
        failures.append(f"acceptance_record_receipt_record_id_wrong:{acceptance_record_receipt.get('record_id')}")
    if acceptance_record.get("receipt_id") != ACCEPTANCE_RECORD_RECEIPT_ID:
        failures.append(f"acceptance_record_receipt_id_wrong:{acceptance_record.get('receipt_id')}")
    if acceptance_record_receipt.get("receipt_id") != ACCEPTANCE_RECORD_RECEIPT_ID:
        failures.append(f"acceptance_record_receipt_id_wrong:{acceptance_record_receipt.get('receipt_id')}")

    if acceptance_policy.get("policy_id") != ACCEPTANCE_POLICY_ID:
        failures.append(f"acceptance_policy_id_wrong:{acceptance_policy.get('policy_id')}")
    if acceptance_policy_receipt.get("policy_id") != ACCEPTANCE_POLICY_ID:
        failures.append(f"acceptance_policy_receipt_policy_id_wrong:{acceptance_policy_receipt.get('policy_id')}")
    if acceptance_policy.get("policy_receipt_id") != ACCEPTANCE_POLICY_RECEIPT_ID:
        failures.append(f"acceptance_policy_receipt_id_wrong:{acceptance_policy.get('policy_receipt_id')}")
    if acceptance_policy_receipt.get("receipt_id") != ACCEPTANCE_POLICY_RECEIPT_ID:
        failures.append(f"acceptance_policy_receipt_id_wrong:{acceptance_policy_receipt.get('receipt_id')}")

    if decision.get("decision_id") != DECISION_ID:
        failures.append(f"decision_id_wrong:{decision.get('decision_id')}")
    if decision_receipt.get("decision_id") != DECISION_ID:
        failures.append(f"decision_receipt_decision_id_wrong:{decision_receipt.get('decision_id')}")
    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal_receipt.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_receipt_proposal_id_wrong:{proposal_receipt.get('proposal_id')}")

    for label, obj in [
        ("acceptance_record", acceptance_record),
        ("acceptance_record_receipt", acceptance_record_receipt),
        ("acceptance_policy", acceptance_policy),
        ("acceptance_policy_receipt", acceptance_policy_receipt),
        ("decision", decision),
        ("decision_receipt", decision_receipt),
        ("proposal", proposal),
        ("proposal_receipt", proposal_receipt),
    ]:
        if obj.get("gate") != "PASS":
            failures.append(f"{label}_gate_not_PASS:{obj.get('gate')}")
        if obj.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
            failures.append(f"{label}_candidate_design_id_wrong:{obj.get('candidate_design_id')}")

    if acceptance_record_receipt.get("record_status") != "PROVISIONAL_BOUNDED_ACCEPTANCE_RECORDED":
        failures.append(f"acceptance_record_status_wrong:{acceptance_record_receipt.get('record_status')}")
    if acceptance_record_receipt.get("acceptance_kind") != ACCEPTANCE_KIND:
        failures.append(f"acceptance_kind_wrong:{acceptance_record_receipt.get('acceptance_kind')}")
    if acceptance_record_receipt.get("accepted_under_bounded_scope") is not True:
        failures.append(f"accepted_under_bounded_scope_not_true:{acceptance_record_receipt.get('accepted_under_bounded_scope')}")

    if acceptance_record_receipt.get("source_policy_id") != ACCEPTANCE_POLICY_ID:
        failures.append(f"record_source_policy_id_wrong:{acceptance_record_receipt.get('source_policy_id')}")
    if acceptance_record_receipt.get("source_policy_receipt_id") != ACCEPTANCE_POLICY_RECEIPT_ID:
        failures.append(f"record_source_policy_receipt_id_wrong:{acceptance_record_receipt.get('source_policy_receipt_id')}")
    if acceptance_record_receipt.get("source_decision_id") != DECISION_ID:
        failures.append(f"record_source_decision_id_wrong:{acceptance_record_receipt.get('source_decision_id')}")
    if acceptance_record_receipt.get("source_decision_receipt_id") != DECISION_RECEIPT_ID:
        failures.append(f"record_source_decision_receipt_id_wrong:{acceptance_record_receipt.get('source_decision_receipt_id')}")
    if acceptance_record_receipt.get("source_proposal_id") != PROPOSAL_ID:
        failures.append(f"record_source_proposal_id_wrong:{acceptance_record_receipt.get('source_proposal_id')}")
    if acceptance_record_receipt.get("source_proposal_receipt_id") != PROPOSAL_RECEIPT_ID:
        failures.append(f"record_source_proposal_receipt_id_wrong:{acceptance_record_receipt.get('source_proposal_receipt_id')}")

    safety = acceptance_record_receipt.get("safety_clauses") or {}
    expected_safety = {
        "provisional_bounded_acceptance_record": True,
        "candidate_provisionally_bounded_accepted": True,
        "registry_written": False,
        "registry_inserted": False,
        "runtime_changed": False,
        "runner_executed": False,
        "bounded_scope_explicit": True,
        "global_correctness_not_claimed": True,
        "registry_write_requires_separate_policy": True,
    }
    for key, expected in expected_safety.items():
        if safety.get(key) is not expected:
            failures.append(f"acceptance_record_safety_wrong:{key}:{safety.get(key)}")
    if safety.get("candidate_acceptance_kind") != CANDIDATE_ACCEPTANCE_KIND:
        failures.append(f"candidate_acceptance_kind_wrong:{safety.get('candidate_acceptance_kind')}")

    terminal = acceptance_record_receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"acceptance_record_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"acceptance_record_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"acceptance_record_terminal_stop_code_not_null:{terminal.get('stop_code')}")

    guards = acceptance_record_receipt.get("authority_guards") or {}
    for key in REQUIRED_FALSE_GUARDS:
        if guards.get(key) is not False:
            failures.append(f"authority_guard_not_false:{key}:{guards.get(key)}")
    for key in REQUIRED_TRUE_GUARDS:
        if guards.get(key) is not True:
            failures.append(f"authority_guard_not_true:{key}:{guards.get(key)}")
    if guards.get("candidate_acceptance_kind") != CANDIDATE_ACCEPTANCE_KIND:
        failures.append(f"authority_candidate_acceptance_kind_wrong:{guards.get('candidate_acceptance_kind')}")

    return failures

def build_policy(write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    acceptance_record = load_json(ACCEPTANCE_RECORD_PATH)
    acceptance_record_receipt = load_json(ACCEPTANCE_RECORD_RECEIPT_PATH)
    acceptance_policy = load_json(ACCEPTANCE_POLICY_PATH)
    acceptance_policy_receipt = load_json(ACCEPTANCE_POLICY_RECEIPT_PATH)
    decision = load_json(DECISION_PATH)
    decision_receipt = load_json(DECISION_RECEIPT_PATH)
    proposal = load_json(PROPOSAL_PATH)
    proposal_receipt = load_json(PROPOSAL_RECEIPT_PATH)

    failures = validate_inputs(
        acceptance_record,
        acceptance_record_receipt,
        acceptance_policy,
        acceptance_policy_receipt,
        decision,
        decision_receipt,
        proposal,
        proposal_receipt,
    )

    policy_seed = {
        "policy_name": POLICY_NAME,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "acceptance_record_id": ACCEPTANCE_RECORD_ID,
        "acceptance_record_receipt_id": ACCEPTANCE_RECORD_RECEIPT_ID,
        "acceptance_kind": ACCEPTANCE_KIND,
        "candidate_acceptance_kind": CANDIDATE_ACCEPTANCE_KIND,
    }
    policy_id = sha8(policy_seed)

    authority_guards = dict(acceptance_record_receipt.get("authority_guards") or {})
    authority_guards["registry_write_policy_built"] = True
    authority_guards["registry_written"] = False
    authority_guards["registry_inserted"] = False
    authority_guards["registry_sqlite_read"] = False
    authority_guards["runtime_code_changed"] = False
    authority_guards["runtime_semantic_changed"] = False
    authority_guards["runtime_receipt_emission_changed"] = False
    authority_guards["runner_executed"] = False

    policy = {
        "schema_version": "raw_delta_signature_candidate_registry_write_policy_v0",
        "policy_name": POLICY_NAME,
        "policy_id": policy_id,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "acceptance_kind": ACCEPTANCE_KIND,
        "candidate_acceptance_kind": CANDIDATE_ACCEPTANCE_KIND,
        "source_acceptance_record_id": ACCEPTANCE_RECORD_ID,
        "source_acceptance_record_receipt_id": ACCEPTANCE_RECORD_RECEIPT_ID,
        "source_acceptance_policy_id": ACCEPTANCE_POLICY_ID,
        "source_acceptance_policy_receipt_id": ACCEPTANCE_POLICY_RECEIPT_ID,
        "source_decision_id": DECISION_ID,
        "source_decision_receipt_id": DECISION_RECEIPT_ID,
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_receipt_id": PROPOSAL_RECEIPT_ID,
        "policy_meaning": "Authorize the next separate unit to emit a bounded registry write record for RAW_DELTA_SIGNATURE_CANDIDATE_V0 after provisional bounded acceptance.",
        "registry_write_scope": {
            "write_kind": "PROVISIONAL_BOUNDED_ACCEPTED_CANDIDATE_REGISTRY_ENTRY",
            "candidate_design_id": CANDIDATE_DESIGN_ID,
            "acceptance_record_id": ACCEPTANCE_RECORD_ID,
            "acceptance_record_receipt_id": ACCEPTANCE_RECORD_RECEIPT_ID,
            "registry_write_is_bounded_metadata_only": True,
            "does_not_execute_candidate": True,
            "does_not_change_runtime": True,
        },
        "authorized_operations_next": {
            "read_acceptance_record": True,
            "read_acceptance_record_receipt": True,
            "read_registry_write_policy": True,
            "write_registry_entry_record": True,
            "write_registry_entry_receipt": True,
        },
        "forbidden_operations": {
            "registry_sqlite_write": True,
            "registry_sqlite_read": True,
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
            "candidate_already_provisionally_bounded_accepted": True,
            "registry_not_written_by_policy": True,
            "runtime_not_changed_by_policy": True,
            "runner_not_executed_by_policy": True,
            "bounded_scope_explicit": True,
            "separate_registry_write_record_required": True,
            "registry_write_must_be_metadata_record_only": True,
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
        "schema_version": "raw_delta_signature_candidate_registry_write_policy_receipt_v0",
        "receipt_type": "RAW_DELTA_SIGNATURE_CANDIDATE_REGISTRY_WRITE_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "policy_name": POLICY_NAME,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "acceptance_kind": ACCEPTANCE_KIND,
        "candidate_acceptance_kind": CANDIDATE_ACCEPTANCE_KIND,
        "source_acceptance_record_id": ACCEPTANCE_RECORD_ID,
        "source_acceptance_record_receipt_id": ACCEPTANCE_RECORD_RECEIPT_ID,
        "source_acceptance_policy_id": ACCEPTANCE_POLICY_ID,
        "source_acceptance_policy_receipt_id": ACCEPTANCE_POLICY_RECEIPT_ID,
        "source_decision_id": DECISION_ID,
        "source_decision_receipt_id": DECISION_RECEIPT_ID,
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_receipt_id": PROPOSAL_RECEIPT_ID,
        "registry_write_scope": policy["registry_write_scope"],
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
    policy, receipt = build_policy(write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"registry_write_policy_id={policy['policy_id']}")
    print(f"registry_write_policy_receipt_id={receipt['receipt_id']}")
    print(f"registry_write_policy_path=data/raw_delta_signature_candidate_registry_write_policies/{policy['policy_id']}.json")
    print(f"registry_write_policy_receipt_path=data/raw_delta_signature_candidate_registry_write_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
