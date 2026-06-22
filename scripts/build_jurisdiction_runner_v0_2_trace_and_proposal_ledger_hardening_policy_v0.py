#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_JURISDICTION_RUNNER_V0_2_TRACE_AND_PROPOSAL_LEDGER_HARDENING_POLICY_V0"
NEXT_GOAL = "IMPLEMENT_JURISDICTION_RUNNER_V0_2_TRACE_AND_PROPOSAL_LEDGER_HARDENING_WITH_FIXTURES_V0"

SOURCE_RUNNER_UNIT_ID = "jurisdiction_runner.v0.2"
TARGET_RUNNER_UNIT_ID = "jurisdiction_runner.v0.2.trace_ledger_hardened"
SOURCE_LOCAL_REGIME_VERSION = "local_regime.v1"
SOURCE_LOCAL_REGIME_HASH = "25802530"

V0_2_IMPLEMENTATION_RECEIPT_ID = "6b90ca5e"
UPGRADE_POLICY_ID = "d76f7ceb"
UPGRADE_POLICY_RECEIPT_ID = "a3b2c208"
HUMAN_DECISION_ID = "cef49876"
DELTA_PROPOSAL_ID = "6e4ee1ea"
SOURCE_LOCAL_REGIME_V0_HASH = "097d620c"

V0_2_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_implementation_receipts" / f"{V0_2_IMPLEMENTATION_RECEIPT_ID}.json"
LOCAL_REGIME_V1_PATH = ROOT / "data" / "local_regime_v1_declarations" / f"{SOURCE_LOCAL_REGIME_HASH}.json"
RUNNER_V0_2_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_2.py"
UPGRADE_POLICY_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_policies" / f"{UPGRADE_POLICY_ID}.json"
UPGRADE_POLICY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_policy_receipts" / f"{UPGRADE_POLICY_ID}.json"
HUMAN_DECISION_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_human_decisions" / f"{HUMAN_DECISION_ID}.json"
DELTA_PROPOSAL_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_delta_proposals" / f"{DELTA_PROPOSAL_ID}.json"
LOCAL_REGIME_V0_PATH = ROOT / "data" / "local_regime_v0_declarations" / f"{SOURCE_LOCAL_REGIME_V0_HASH}.json"

OUT_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_trace_and_proposal_ledger_hardening_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_trace_and_proposal_ledger_hardening_policy_receipts"

TRACE_ENTRY_SCHEMA = {
    "schema_version": "jurisdiction_runner_trace_entry_v0",
    "required_fields": [
        "step_index",
        "state_before_sig8",
        "applicable_moves",
        "selected_move",
        "selection_reason",
        "action_result",
        "state_delta",
        "halt_code",
        "proposal_ref",
        "state_after_sig8",
    ],
    "field_meanings": {
        "step_index": "integer order of runner step",
        "state_before_sig8": "hash of state before selected action",
        "applicable_moves": "registered move ids applicable before selection",
        "selected_move": "selected move id or null if no move applies",
        "selection_reason": "deterministic reason for selection",
        "action_result": "PASS, BLOCKED, HALT, or ERROR",
        "state_delta": "minimal before/after changed fields",
        "halt_code": "typed halt code or null",
        "proposal_ref": "proposal/proposal_receipt refs when emitted or withheld",
        "state_after_sig8": "hash of state after action or halt",
    },
}

TRACE_FILE_SCHEMA = {
    "schema_version": "jurisdiction_runner_trace_file_v0",
    "required_fields": [
        "trace_id",
        "run_id",
        "runner_unit_id",
        "local_regime_hash",
        "source_fixture_id",
        "entries",
        "final_halt_code",
        "receipt_ref",
    ],
    "entry_schema": TRACE_ENTRY_SCHEMA,
    "receipt_consistency_required": True,
}

PROPOSAL_LEDGER_SCHEMA = {
    "schema_version": "unresolved_proposal_ledger_v0",
    "ledger_scope": "path-addressed local artifact only, no registry or sqlite authority",
    "required_fields": [
        "ledger_id",
        "runner_unit_id",
        "local_regime_hash",
        "ledger_entries",
        "created_by_receipt_id",
    ],
    "entry_required_fields": [
        "proposal_key",
        "proposal_id",
        "proposal_type",
        "source_halt_code",
        "source_state_id",
        "source_fixture_id",
        "proposed_delta_kind",
        "status",
        "created_by_case_receipt_id",
        "created_by_proposal_receipt_id",
    ],
    "status_values": [
        "UNRESOLVED",
        "REVIEWED_ACCEPTED",
        "REVIEWED_REJECTED",
        "REVIEWED_REVISED",
    ],
    "duplicate_match_keys": [
        "proposal_type",
        "source_halt_code",
        "source_state_id",
        "proposed_delta_kind",
    ],
}

REQUIRED_HARDENING_CASES = {
    "TRACE_PRESENT_FOR_HALT_WITH_PROPOSAL": {
        "purpose": "A halt-with-proposal run emits a first-class trace file whose entries explain applicable moves, selected move, state delta, halt, and proposal refs.",
        "expected_proposal_status": "EMITTED_REVIEW_REQUIRED",
        "expected_trace_required": True,
        "expected_receipt_trace_consistency": True,
    },
    "TRACE_PRESENT_FOR_NO_PROPOSAL_INSUFFICIENT_EVIDENCE": {
        "purpose": "A no-proposal insufficient-evidence halt emits a trace that explains no proposal was emitted and preserves the typed no_proposal_reason.",
        "expected_proposal_status": "NONE",
        "expected_no_proposal_reason": "INSUFFICIENT_EVIDENCE",
        "expected_trace_required": True,
    },
    "LEDGER_RECORDS_FIRST_UNRESOLVED_PROPOSAL": {
        "purpose": "First emitted review-required proposal is inserted into path-addressed unresolved proposal ledger.",
        "expected_ledger_status": "UNRESOLVED",
        "expected_sqlite_registry_write": False,
    },
    "LEDGER_SUPPRESSES_DUPLICATE_UNRESOLVED_PROPOSAL": {
        "purpose": "Second identical unresolved proposal pressure reads declared ledger artifact and withholds duplicate proposal by key.",
        "expected_proposal_status": "WITHHELD_DUPLICATE_UNRESOLVED",
        "expected_duplicate_unresolved_proposal_count": 1,
    },
    "RECEIPT_TRACE_CONSISTENCY": {
        "purpose": "Receipt final state, moves, halt code, proposal refs, and trace ref agree with trace file.",
        "expected_receipt_trace_consistency": True,
    },
    "REGRESSION_V0_2_NON_EXECUTION_AND_NO_REGISTRY": {
        "purpose": "Hardening must preserve v0.2 non-execution, non-promotion, no registry, no global taxonomy, no hidden continuation.",
        "expected_proposal_executed": False,
        "expected_proposal_promoted": False,
        "expected_registry_written": False,
        "expected_hidden_continuation": False,
    },
}

ACCEPTANCE_GATES = {
    "H0_source_chain_verified": {
        "required": True,
        "description": "v0.2 implementation, local_regime.v1, v0.2 runner, upgrade policy, human decision, and delta proposal are tracked and path-addressed.",
    },
    "H1_trace_schema_declared": {
        "required": True,
        "description": "Trace entry/file schema is declared as implementation artifact.",
    },
    "H2_proposal_ledger_schema_declared": {
        "required": True,
        "description": "Path-addressed unresolved proposal ledger schema is declared.",
    },
    "H3_trace_hardened_runner_implemented": {
        "required": True,
        "description": "Implement separate trace-ledger hardened runner module; do not modify jurisdiction_runner_v0_2.py.",
    },
    "H4_trace_files_emitted_for_cases": {
        "required": True,
        "description": "Every hardening case emits trace file/object with required entries.",
    },
    "H5_receipts_reference_traces": {
        "required": True,
        "description": "Every case receipt references its trace and agrees with final halt/state/proposal refs.",
    },
    "H6_unresolved_proposal_ledger_artifact_used": {
        "required": True,
        "description": "Duplicate unresolved proposal guard uses explicit path-addressed ledger artifact, not only in-memory session state.",
    },
    "H7_v0_2_regression_preserved": {
        "required": True,
        "description": "Proposal non-execution, non-promotion, no registry, no global taxonomy, no hidden continuation remain true.",
    },
}

REQUIRED_IMPLEMENTATION_ARTIFACTS = {
    "trace_schema": "data/jurisdiction_runner_v0_2_trace_schemas/<trace_schema_id>.json",
    "proposal_ledger_schema": "data/jurisdiction_runner_v0_2_proposal_ledger_schemas/<ledger_schema_id>.json",
    "trace_ledger_runner_module": "src/matrixlab/jurisdiction_runner_v0_2_trace_ledger.py",
    "fixtures": "data/jurisdiction_runner_v0_2_trace_ledger_hardening_fixtures/*.json",
    "traces": "data/jurisdiction_runner_v0_2_trace_ledger_hardening_traces/*.json",
    "proposal_ledgers": "data/jurisdiction_runner_v0_2_trace_ledger_hardening_ledgers/*.json",
    "case_receipts": "data/jurisdiction_runner_v0_2_trace_ledger_hardening_case_receipts/*.json",
    "implementation_receipt": "data/jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts/<receipt_id>.json",
}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def tracked(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def validate_inputs(
    implementation_receipt: Dict[str, Any],
    local_regime_v1: Dict[str, Any],
    upgrade_policy: Dict[str, Any],
    upgrade_policy_receipt: Dict[str, Any],
    human_decision: Dict[str, Any],
    delta_proposal: Dict[str, Any],
    local_regime_v0: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if implementation_receipt.get("receipt_id") != V0_2_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"v0_2_implementation_receipt_id_wrong:{implementation_receipt.get('receipt_id')}")
    if implementation_receipt.get("gate") != "PASS":
        failures.append(f"v0_2_implementation_gate_not_PASS:{implementation_receipt.get('gate')}")
    if implementation_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append(f"v0_2_terminal_not_STOP:{implementation_receipt.get('terminal')}")
    if implementation_receipt.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append(f"v0_2_terminal_stop_not_DONE:{implementation_receipt.get('terminal')}")
    if implementation_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append(f"v0_2_terminal_next_not_null:{implementation_receipt.get('terminal')}")

    if implementation_receipt.get("source_runner_unit_id") != "jurisdiction_runner.v0.1":
        failures.append(f"implementation_source_runner_wrong:{implementation_receipt.get('source_runner_unit_id')}")
    if implementation_receipt.get("target_runner_unit_id") != SOURCE_RUNNER_UNIT_ID:
        failures.append(f"implementation_target_runner_wrong:{implementation_receipt.get('target_runner_unit_id')}")
    if implementation_receipt.get("target_local_regime_version") != SOURCE_LOCAL_REGIME_VERSION:
        failures.append(f"implementation_target_regime_wrong:{implementation_receipt.get('target_local_regime_version')}")
    if implementation_receipt.get("local_regime_v1_hash") != SOURCE_LOCAL_REGIME_HASH:
        failures.append(f"implementation_local_regime_v1_hash_wrong:{implementation_receipt.get('local_regime_v1_hash')}")

    gates = implementation_receipt.get("acceptance_gate_results") or {}
    for gate in [
        "S0_source_chain_verified",
        "S1_local_regime_v1_declared",
        "S2_runner_v0_2_implemented",
        "S3_halt_with_proposal_fixture_passes",
        "S4_proposal_non_execution_passes",
        "S5_duplicate_unresolved_proposal_guard_passes",
        "S6_no_hidden_continuation",
        "S7_no_registry_or_global_taxonomy",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"v0_2_acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = implementation_receipt.get("aggregate_metrics") or {}
    if metrics.get("case_count") != 6:
        failures.append(f"v0_2_case_count_wrong:{metrics.get('case_count')}")
    if metrics.get("case_pass_count") != 6:
        failures.append(f"v0_2_case_pass_count_wrong:{metrics.get('case_pass_count')}")
    if metrics.get("case_fail_count") != 0:
        failures.append(f"v0_2_case_fail_count_wrong:{metrics.get('case_fail_count')}")
    if metrics.get("runtime_proposal_emitted_count") < 3:
        failures.append(f"v0_2_runtime_proposal_emitted_too_low:{metrics.get('runtime_proposal_emitted_count')}")
    for key in [
        "runtime_proposal_executed_count",
        "runtime_proposal_promoted_count",
        "registry_write_count",
        "local_regime_mutation_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"v0_2_metric_not_zero:{key}:{metrics.get(key)}")
    if metrics.get("duplicate_unresolved_proposal_count") != 1:
        failures.append(f"v0_2_duplicate_count_wrong:{metrics.get('duplicate_unresolved_proposal_count')}")

    guards = implementation_receipt.get("authority_guards") or {}
    for key in [
        "runner_v0_1_modified",
        "local_regime_v0_replaced",
        "local_regime_runtime_mutated",
        "proposal_executed",
        "proposal_promoted",
        "registry_written",
        "registry_sqlite_written",
        "global_taxonomy_claimed",
        "final_schema_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
    ]:
        if guards.get(key) is not False:
            failures.append(f"v0_2_authority_guard_not_false:{key}:{guards.get(key)}")

    if local_regime_v1.get("local_regime_version") != SOURCE_LOCAL_REGIME_VERSION:
        failures.append(f"local_regime_v1_version_wrong:{local_regime_v1.get('local_regime_version')}")
    if local_regime_v1.get("local_regime_hash") != SOURCE_LOCAL_REGIME_HASH:
        failures.append(f"local_regime_v1_hash_wrong:{local_regime_v1.get('local_regime_hash')}")
    if local_regime_v1.get("source_local_regime_hash") != SOURCE_LOCAL_REGIME_V0_HASH:
        failures.append(f"local_regime_v1_source_hash_wrong:{local_regime_v1.get('source_local_regime_hash')}")

    if upgrade_policy.get("policy_id") != UPGRADE_POLICY_ID:
        failures.append(f"upgrade_policy_id_wrong:{upgrade_policy.get('policy_id')}")
    if upgrade_policy_receipt.get("receipt_id") != UPGRADE_POLICY_RECEIPT_ID:
        failures.append(f"upgrade_policy_receipt_id_wrong:{upgrade_policy_receipt.get('receipt_id')}")
    if upgrade_policy_receipt.get("gate") != "PASS":
        failures.append(f"upgrade_policy_receipt_gate_not_PASS:{upgrade_policy_receipt.get('gate')}")

    if human_decision.get("decision_id") != HUMAN_DECISION_ID:
        failures.append(f"human_decision_id_wrong:{human_decision.get('decision_id')}")
    if human_decision.get("decision_status") != "ACCEPTED_PROVISIONALLY_FOR_POLICY_BUILD_NOT_APPLIED":
        failures.append(f"human_decision_status_wrong:{human_decision.get('decision_status')}")

    if delta_proposal.get("proposal_id") != DELTA_PROPOSAL_ID:
        failures.append(f"delta_proposal_id_wrong:{delta_proposal.get('proposal_id')}")
    if delta_proposal.get("proposal_class") != "PROPOSITION_SURFACE_DELTA_PROPOSAL":
        failures.append(f"delta_class_wrong:{delta_proposal.get('proposal_class')}")

    if local_regime_v0.get("local_regime_hash") != SOURCE_LOCAL_REGIME_V0_HASH:
        failures.append(f"local_regime_v0_hash_wrong:{local_regime_v0.get('local_regime_hash')}")

    for path, label in [
        (V0_2_IMPLEMENTATION_RECEIPT_PATH, "v0_2_implementation_receipt"),
        (LOCAL_REGIME_V1_PATH, "local_regime_v1"),
        (RUNNER_V0_2_PATH, "runner_v0_2"),
        (UPGRADE_POLICY_PATH, "upgrade_policy"),
        (UPGRADE_POLICY_RECEIPT_PATH, "upgrade_policy_receipt"),
        (HUMAN_DECISION_PATH, "human_decision"),
        (DELTA_PROPOSAL_PATH, "delta_proposal"),
        (LOCAL_REGIME_V0_PATH, "local_regime_v0"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{path.relative_to(ROOT).as_posix()}")

    return failures

def build_policy(write_outputs: bool = True) -> tuple[Dict[str, Any], Dict[str, Any]]:
    implementation_receipt = read_json(V0_2_IMPLEMENTATION_RECEIPT_PATH)
    local_regime_v1 = read_json(LOCAL_REGIME_V1_PATH)
    upgrade_policy = read_json(UPGRADE_POLICY_PATH)
    upgrade_policy_receipt = read_json(UPGRADE_POLICY_RECEIPT_PATH)
    human_decision = read_json(HUMAN_DECISION_PATH)
    delta_proposal = read_json(DELTA_PROPOSAL_PATH)
    local_regime_v0 = read_json(LOCAL_REGIME_V0_PATH)

    failures = validate_inputs(
        implementation_receipt,
        local_regime_v1,
        upgrade_policy,
        upgrade_policy_receipt,
        human_decision,
        delta_proposal,
        local_regime_v0,
    )

    policy_seed = {
        "unit_id": UNIT_ID,
        "source_implementation_receipt_id": V0_2_IMPLEMENTATION_RECEIPT_ID,
        "source_local_regime_hash": SOURCE_LOCAL_REGIME_HASH,
        "source_runner_unit_id": SOURCE_RUNNER_UNIT_ID,
        "target_runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "next_goal": NEXT_GOAL,
    }
    policy_id = sha8(policy_seed)

    authority_guards = {
        "hardening_policy_built": True,
        "source_v0_2_implementation_consumed": True,
        "source_local_regime_v1_consumed": True,
        "source_runner_v0_2_read": True,
        "runner_v0_2_modified_by_policy": False,
        "trace_ledger_runner_implemented_by_policy": False,
        "runner_executed_by_policy": False,
        "trace_schema_emitted_by_policy": False,
        "ledger_schema_emitted_by_policy": False,
        "trace_files_emitted_by_policy": False,
        "proposal_ledger_emitted_by_policy": False,
        "local_regime_runtime_mutated": False,
        "proposal_executed": False,
        "proposal_promoted": False,
        "registry_written": False,
        "registry_sqlite_read": False,
        "registry_sqlite_written": False,
        "full_registry_scan_used": False,
        "global_taxonomy_claimed": False,
        "final_schema_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
    }

    policy = {
        "schema_version": "jurisdiction_runner_v0_2_trace_and_proposal_ledger_hardening_policy_v0",
        "policy_type": "JURISDICTION_RUNNER_V0_2_TRACE_AND_PROPOSAL_LEDGER_HARDENING_POLICY",
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "source_runner_unit_id": SOURCE_RUNNER_UNIT_ID,
        "target_runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "source_local_regime_version": SOURCE_LOCAL_REGIME_VERSION,
        "source_local_regime_hash": SOURCE_LOCAL_REGIME_HASH,
        "source_v0_2_implementation_receipt_id": V0_2_IMPLEMENTATION_RECEIPT_ID,
        "source_upgrade_policy_id": UPGRADE_POLICY_ID,
        "source_upgrade_policy_receipt_id": UPGRADE_POLICY_RECEIPT_ID,
        "source_human_decision_id": HUMAN_DECISION_ID,
        "source_delta_proposal_id": DELTA_PROPOSAL_ID,
        "hardening_summary": {
            "hardening_reason": "v0.2 proposal surface works, but audit path should be first-class before expanding behavior.",
            "target": "first-class trace files plus path-addressed unresolved proposal ledger",
            "non_goal": "new intelligence, broader move registry, global registry, final taxonomy, proof, or runtime self-authorization",
        },
        "trace_entry_schema": TRACE_ENTRY_SCHEMA,
        "trace_file_schema": TRACE_FILE_SCHEMA,
        "proposal_ledger_schema": PROPOSAL_LEDGER_SCHEMA,
        "required_hardening_cases": REQUIRED_HARDENING_CASES,
        "required_implementation_artifacts": REQUIRED_IMPLEMENTATION_ARTIFACTS,
        "acceptance_gates": ACCEPTANCE_GATES,
        "required_receipt_trace_consistency": {
            "receipt_final_halt_code_equals_trace_final_halt_code": True,
            "receipt_proposal_ref_equals_trace_proposal_ref_when_present": True,
            "receipt_state_sigs_match_trace_boundary_sigs": True,
            "receipt_trace_ref_path_addressed": True,
            "trace_receipt_ref_path_addressed": True,
        },
        "authorized_operations_next": {
            "read_hardening_policy": True,
            "read_hardening_policy_receipt": True,
            "read_source_v0_2_runner": True,
            "read_source_local_regime_v1": True,
            "write_trace_schema_artifact": True,
            "write_proposal_ledger_schema_artifact": True,
            "write_trace_ledger_hardened_runner_module": True,
            "write_hardening_fixtures": True,
            "execute_trace_ledger_hardened_runner_against_fixtures": True,
            "emit_trace_files": True,
            "emit_unresolved_proposal_ledger_artifacts": True,
            "emit_hardening_case_receipts": True,
            "emit_hardening_implementation_receipt": True,
        },
        "forbidden_operations_next": {
            "modify_jurisdiction_runner_v0_2": True,
            "modify_jurisdiction_runner_v0_1": True,
            "replace_local_regime_v1": True,
            "replace_local_regime_v0": True,
            "mutate_local_regime_at_runtime": True,
            "execute_or_apply_proposal": True,
            "promote_proposal_without_human_review": True,
            "sqlite_registry_write": True,
            "sqlite_registry_read": True,
            "full_registry_scan": True,
            "global_taxonomy_design": True,
            "final_schema_claim": True,
            "proof_claim": True,
            "hidden_continuation_after_stop": True,
            "ambient_workspace_authority": True,
            "latest_or_mtime_selection": True,
        },
        "safety_clauses": {
            "policy_only": True,
            "does_not_modify_runner": True,
            "does_not_execute_runner": True,
            "does_not_emit_trace_schema": True,
            "does_not_emit_ledger_schema": True,
            "does_not_emit_trace_files": True,
            "does_not_emit_ledger_artifacts": True,
            "does_not_apply_or_promote_proposal": True,
            "does_not_mutate_local_regime": True,
            "does_not_write_registry": True,
            "does_not_claim_global_correctness": True,
            "does_not_claim_final_taxonomy": True,
            "does_not_claim_theorem_closure": True,
            "next_unit_required_for_implementation": True,
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

    receipt_seed = {
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "source_v0_2_implementation_receipt_id": V0_2_IMPLEMENTATION_RECEIPT_ID,
        "target_runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "terminal": policy["terminal"],
    }
    receipt_id = sha8(receipt_seed)
    policy["policy_receipt_id"] = receipt_id

    receipt = {
        "schema_version": "jurisdiction_runner_v0_2_trace_and_proposal_ledger_hardening_policy_receipt_v0",
        "receipt_type": "JURISDICTION_RUNNER_V0_2_TRACE_AND_PROPOSAL_LEDGER_HARDENING_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "source_runner_unit_id": SOURCE_RUNNER_UNIT_ID,
        "target_runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "source_local_regime_version": SOURCE_LOCAL_REGIME_VERSION,
        "source_local_regime_hash": SOURCE_LOCAL_REGIME_HASH,
        "source_v0_2_implementation_receipt_id": V0_2_IMPLEMENTATION_RECEIPT_ID,
        "source_upgrade_policy_id": UPGRADE_POLICY_ID,
        "source_upgrade_policy_receipt_id": UPGRADE_POLICY_RECEIPT_ID,
        "hardening_summary": policy["hardening_summary"],
        "trace_entry_schema": policy["trace_entry_schema"],
        "trace_file_schema": policy["trace_file_schema"],
        "proposal_ledger_schema": policy["proposal_ledger_schema"],
        "required_hardening_cases": policy["required_hardening_cases"],
        "required_implementation_artifacts": policy["required_implementation_artifacts"],
        "acceptance_gates": policy["acceptance_gates"],
        "required_receipt_trace_consistency": policy["required_receipt_trace_consistency"],
        "authorized_operations_next": policy["authorized_operations_next"],
        "forbidden_operations_next": policy["forbidden_operations_next"],
        "safety_clauses": policy["safety_clauses"],
        "authority_guards": authority_guards,
        "terminal": policy["terminal"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        write_json(OUT_DIR / f"{policy_id}.json", policy)
        write_json(OUT_RECEIPT_DIR / f"{policy_id}.json", receipt)

    return policy, receipt

def main() -> int:
    policy, receipt = build_policy(write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"trace_ledger_hardening_policy_id={policy['policy_id']}")
    print(f"trace_ledger_hardening_policy_receipt_id={receipt['receipt_id']}")
    print(f"trace_ledger_hardening_policy_path=data/jurisdiction_runner_v0_2_trace_and_proposal_ledger_hardening_policies/{policy['policy_id']}.json")
    print(f"trace_ledger_hardening_policy_receipt_path=data/jurisdiction_runner_v0_2_trace_and_proposal_ledger_hardening_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
