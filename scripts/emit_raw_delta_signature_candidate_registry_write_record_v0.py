#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EMIT_RAW_DELTA_SIGNATURE_CANDIDATE_REGISTRY_WRITE_RECORD_V0"

POLICY_ID = "c2dd4cd7"
POLICY_RECEIPT_ID = "f722069f"
ACCEPTANCE_RECORD_ID = "fe19fa23"
ACCEPTANCE_RECORD_RECEIPT_ID = "f5db8634"
ACCEPTANCE_POLICY_ID = "a371381b"
ACCEPTANCE_POLICY_RECEIPT_ID = "6e1773c8"
DECISION_ID = "b2fca9d8"
DECISION_RECEIPT_ID = "d0e9f235"
PROPOSAL_ID = "ab545dbf"
PROPOSAL_RECEIPT_ID = "ec67d9dc"

CANDIDATE_DESIGN_ID = "RAW_DELTA_SIGNATURE_CANDIDATE_V0"
ACCEPTANCE_KIND = "PROVISIONAL_BOUNDED"
CANDIDATE_ACCEPTANCE_KIND = "PROVISIONAL_BOUNDED_ONLY"
REGISTRY_WRITE_KIND = "PROVISIONAL_BOUNDED_ACCEPTED_CANDIDATE_REGISTRY_ENTRY"

POLICY_PATH = ROOT / "data" / "raw_delta_signature_candidate_registry_write_policies" / f"{POLICY_ID}.json"
POLICY_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_registry_write_policy_receipts" / f"{POLICY_ID}.json"
ACCEPTANCE_RECORD_PATH = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_records" / f"{ACCEPTANCE_RECORD_ID}.json"
ACCEPTANCE_RECORD_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_record_receipts" / f"{ACCEPTANCE_RECORD_ID}.json"
ACCEPTANCE_POLICY_PATH = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_policies" / f"{ACCEPTANCE_POLICY_ID}.json"
ACCEPTANCE_POLICY_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_provisional_bounded_acceptance_policy_receipts" / f"{ACCEPTANCE_POLICY_ID}.json"
DECISION_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_human_decisions" / f"{DECISION_ID}.json"
DECISION_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_human_decision_receipts" / f"{DECISION_ID}.json"
PROPOSAL_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposals" / f"{PROPOSAL_ID}.json"
PROPOSAL_RECEIPT_PATH = ROOT / "data" / "raw_delta_signature_candidate_acceptance_proposal_receipts" / f"{PROPOSAL_ID}.json"

OUT_DIR = ROOT / "data" / "raw_delta_signature_candidate_registry_write_records"
OUT_RECEIPT_DIR = ROOT / "data" / "raw_delta_signature_candidate_registry_write_record_receipts"

FALSE_GUARDS_BEFORE_RECORD = [
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

TRUE_GUARDS_REQUIRED = [
    "candidate_acceptance_proposal_emitted",
    "human_decision_boundary_emitted",
    "human_decision_recorded",
    "provisional_bounded_acceptance_policy_built",
    "provisional_bounded_acceptance_record_emitted",
    "registry_write_policy_built",
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
    policy: dict[str, Any],
    policy_receipt: dict[str, Any],
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

    if policy.get("policy_id") != POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy_receipt.get("policy_id") != POLICY_ID:
        failures.append(f"policy_receipt_policy_id_wrong:{policy_receipt.get('policy_id')}")
    if policy.get("policy_receipt_id") != POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if policy_receipt.get("receipt_id") != POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy_receipt.get('receipt_id')}")

    ids = [
        ("acceptance_record", acceptance_record, "record_id", ACCEPTANCE_RECORD_ID),
        ("acceptance_record_receipt", acceptance_record_receipt, "record_id", ACCEPTANCE_RECORD_ID),
        ("acceptance_policy", acceptance_policy, "policy_id", ACCEPTANCE_POLICY_ID),
        ("acceptance_policy_receipt", acceptance_policy_receipt, "policy_id", ACCEPTANCE_POLICY_ID),
        ("decision", decision, "decision_id", DECISION_ID),
        ("decision_receipt", decision_receipt, "decision_id", DECISION_ID),
        ("proposal", proposal, "proposal_id", PROPOSAL_ID),
        ("proposal_receipt", proposal_receipt, "proposal_id", PROPOSAL_ID),
    ]
    for label, obj, key, expected in ids:
        if obj.get(key) != expected:
            failures.append(f"{label}_{key}_wrong:{obj.get(key)}")

    for label, obj in [
        ("policy", policy),
        ("policy_receipt", policy_receipt),
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

    if policy_receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy_receipt.get('policy_status')}")
    if policy_receipt.get("acceptance_kind") != ACCEPTANCE_KIND:
        failures.append(f"policy_acceptance_kind_wrong:{policy_receipt.get('acceptance_kind')}")
    if policy_receipt.get("candidate_acceptance_kind") != CANDIDATE_ACCEPTANCE_KIND:
        failures.append(f"policy_candidate_acceptance_kind_wrong:{policy_receipt.get('candidate_acceptance_kind')}")

    if policy_receipt.get("source_acceptance_record_id") != ACCEPTANCE_RECORD_ID:
        failures.append(f"policy_source_acceptance_record_id_wrong:{policy_receipt.get('source_acceptance_record_id')}")
    if policy_receipt.get("source_acceptance_record_receipt_id") != ACCEPTANCE_RECORD_RECEIPT_ID:
        failures.append(f"policy_source_acceptance_record_receipt_id_wrong:{policy_receipt.get('source_acceptance_record_receipt_id')}")

    scope = policy_receipt.get("registry_write_scope") or {}
    if scope.get("write_kind") != REGISTRY_WRITE_KIND:
        failures.append(f"registry_write_kind_wrong:{scope.get('write_kind')}")
    if scope.get("candidate_design_id") != CANDIDATE_DESIGN_ID:
        failures.append(f"registry_write_scope_candidate_wrong:{scope.get('candidate_design_id')}")
    if scope.get("acceptance_record_id") != ACCEPTANCE_RECORD_ID:
        failures.append(f"registry_write_scope_record_wrong:{scope.get('acceptance_record_id')}")
    if scope.get("acceptance_record_receipt_id") != ACCEPTANCE_RECORD_RECEIPT_ID:
        failures.append(f"registry_write_scope_record_receipt_wrong:{scope.get('acceptance_record_receipt_id')}")
    for key in [
        "registry_write_is_bounded_metadata_only",
        "does_not_execute_candidate",
        "does_not_change_runtime",
    ]:
        if scope.get(key) is not True:
            failures.append(f"registry_write_scope_not_true:{key}:{scope.get(key)}")

    authorized = policy_receipt.get("authorized_operations_next") or {}
    for key in [
        "read_acceptance_record",
        "read_acceptance_record_receipt",
        "read_registry_write_policy",
        "write_registry_entry_record",
        "write_registry_entry_receipt",
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
        "candidate_already_provisionally_bounded_accepted": True,
        "registry_not_written_by_policy": True,
        "runtime_not_changed_by_policy": True,
        "runner_not_executed_by_policy": True,
        "bounded_scope_explicit": True,
        "separate_registry_write_record_required": True,
        "registry_write_must_be_metadata_record_only": True,
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

    acc_safety = acceptance_record_receipt.get("safety_clauses") or {}
    if acc_safety.get("registry_write_requires_separate_policy") is not True:
        failures.append(f"acceptance_record_registry_write_policy_required_not_true:{acc_safety.get('registry_write_requires_separate_policy')}")
    if acc_safety.get("registry_written") is not False:
        failures.append(f"acceptance_record_registry_written_not_false:{acc_safety.get('registry_written')}")
    if acc_safety.get("registry_inserted") is not False:
        failures.append(f"acceptance_record_registry_inserted_not_false:{acc_safety.get('registry_inserted')}")

    guards = policy_receipt.get("authority_guards") or {}
    for key in FALSE_GUARDS_BEFORE_RECORD:
        if guards.get(key) is not False:
            failures.append(f"pre_record_authority_guard_not_false:{key}:{guards.get(key)}")
    for key in TRUE_GUARDS_REQUIRED:
        if guards.get(key) is not True:
            failures.append(f"authority_guard_not_true:{key}:{guards.get(key)}")
    if guards.get("candidate_acceptance_kind") != CANDIDATE_ACCEPTANCE_KIND:
        failures.append(f"authority_candidate_acceptance_kind_wrong:{guards.get('candidate_acceptance_kind')}")

    return failures

def build_record(write_outputs: bool = True) -> tuple[dict[str, Any], dict[str, Any]]:
    policy = load_json(POLICY_PATH)
    policy_receipt = load_json(POLICY_RECEIPT_PATH)
    acceptance_record = load_json(ACCEPTANCE_RECORD_PATH)
    acceptance_record_receipt = load_json(ACCEPTANCE_RECORD_RECEIPT_PATH)
    acceptance_policy = load_json(ACCEPTANCE_POLICY_PATH)
    acceptance_policy_receipt = load_json(ACCEPTANCE_POLICY_RECEIPT_PATH)
    decision = load_json(DECISION_PATH)
    decision_receipt = load_json(DECISION_RECEIPT_PATH)
    proposal = load_json(PROPOSAL_PATH)
    proposal_receipt = load_json(PROPOSAL_RECEIPT_PATH)

    failures = validate_inputs(
        policy,
        policy_receipt,
        acceptance_record,
        acceptance_record_receipt,
        acceptance_policy,
        acceptance_policy_receipt,
        decision,
        decision_receipt,
        proposal,
        proposal_receipt,
    )

    record_seed = {
        "unit_id": UNIT_ID,
        "policy_id": POLICY_ID,
        "policy_receipt_id": POLICY_RECEIPT_ID,
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "acceptance_record_id": ACCEPTANCE_RECORD_ID,
        "acceptance_record_receipt_id": ACCEPTANCE_RECORD_RECEIPT_ID,
        "write_kind": REGISTRY_WRITE_KIND,
        "bounded_metadata_only": True,
    }
    record_id = sha8(record_seed)

    authority_guards = dict(policy_receipt.get("authority_guards") or {})
    authority_guards["registry_write_record_emitted"] = True
    authority_guards["registry_metadata_record_written"] = True
    authority_guards["registry_written"] = False
    authority_guards["registry_inserted"] = False
    authority_guards["registry_sqlite_read"] = False
    authority_guards["registry_sqlite_written"] = False
    authority_guards["full_registry_scan_used"] = False
    authority_guards["runtime_code_changed"] = False
    authority_guards["runtime_semantic_changed"] = False
    authority_guards["runtime_receipt_emission_changed"] = False
    authority_guards["runner_executed"] = False

    registry_entry = {
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "candidate_acceptance_kind": CANDIDATE_ACCEPTANCE_KIND,
        "acceptance_kind": ACCEPTANCE_KIND,
        "acceptance_record_id": ACCEPTANCE_RECORD_ID,
        "acceptance_record_receipt_id": ACCEPTANCE_RECORD_RECEIPT_ID,
        "registry_write_policy_id": POLICY_ID,
        "registry_write_policy_receipt_id": POLICY_RECEIPT_ID,
        "write_kind": REGISTRY_WRITE_KIND,
        "bounded_metadata_only": True,
    }

    record = {
        "schema_version": "raw_delta_signature_candidate_registry_write_record_v0",
        "record_type": "RAW_DELTA_SIGNATURE_CANDIDATE_REGISTRY_WRITE_RECORD",
        "unit_id": UNIT_ID,
        "record_id": record_id,
        "record_status": "REGISTRY_METADATA_RECORD_EMITTED",
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "acceptance_kind": ACCEPTANCE_KIND,
        "candidate_acceptance_kind": CANDIDATE_ACCEPTANCE_KIND,
        "write_kind": REGISTRY_WRITE_KIND,
        "registry_entry": registry_entry,
        "source_registry_write_policy_id": POLICY_ID,
        "source_registry_write_policy_receipt_id": POLICY_RECEIPT_ID,
        "source_acceptance_record_id": ACCEPTANCE_RECORD_ID,
        "source_acceptance_record_receipt_id": ACCEPTANCE_RECORD_RECEIPT_ID,
        "source_acceptance_policy_id": ACCEPTANCE_POLICY_ID,
        "source_acceptance_policy_receipt_id": ACCEPTANCE_POLICY_RECEIPT_ID,
        "source_decision_id": DECISION_ID,
        "source_decision_receipt_id": DECISION_RECEIPT_ID,
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_receipt_id": PROPOSAL_RECEIPT_ID,
        "registry_write_scope": policy_receipt.get("registry_write_scope"),
        "safety_clauses": {
            "registry_write_record": True,
            "registry_metadata_record_written": True,
            "registry_write_kind": REGISTRY_WRITE_KIND,
            "bounded_metadata_only": True,
            "candidate_already_provisionally_bounded_accepted": True,
            "candidate_acceptance_kind": CANDIDATE_ACCEPTANCE_KIND,
            "registry_sqlite_written": False,
            "registry_inserted": False,
            "registry_sqlite_read": False,
            "full_registry_scan_used": False,
            "runtime_changed": False,
            "runner_executed": False,
            "candidate_executed": False,
            "global_correctness_not_claimed": True,
        },
        "authority_guards": authority_guards,
        "terminal": {
            "type": "STOP",
            "next_command_goal": None,
            "stop_code": "STOP_DONE",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt = {
        "schema_version": "raw_delta_signature_candidate_registry_write_record_receipt_v0",
        "receipt_type": "RAW_DELTA_SIGNATURE_CANDIDATE_REGISTRY_WRITE_RECORD_RECEIPT",
        "unit_id": UNIT_ID,
        "record_id": record_id,
        "record_status": record["record_status"],
        "candidate_design_id": CANDIDATE_DESIGN_ID,
        "acceptance_kind": ACCEPTANCE_KIND,
        "candidate_acceptance_kind": CANDIDATE_ACCEPTANCE_KIND,
        "write_kind": REGISTRY_WRITE_KIND,
        "registry_entry": registry_entry,
        "source_registry_write_policy_id": POLICY_ID,
        "source_registry_write_policy_receipt_id": POLICY_RECEIPT_ID,
        "source_acceptance_record_id": ACCEPTANCE_RECORD_ID,
        "source_acceptance_record_receipt_id": ACCEPTANCE_RECORD_RECEIPT_ID,
        "registry_write_scope": record["registry_write_scope"],
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
    record, receipt = build_record(write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"registry_write_record_id={record['record_id']}")
    print(f"registry_write_record_receipt_id={receipt['receipt_id']}")
    print(f"registry_write_record_path=data/raw_delta_signature_candidate_registry_write_records/{record['record_id']}.json")
    print(f"registry_write_record_receipt_path=data/raw_delta_signature_candidate_registry_write_record_receipts/{record['record_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
