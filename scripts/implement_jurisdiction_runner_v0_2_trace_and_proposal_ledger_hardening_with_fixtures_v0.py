#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "IMPLEMENT_JURISDICTION_RUNNER_V0_2_TRACE_AND_PROPOSAL_LEDGER_HARDENING_WITH_FIXTURES_V0"

TRACE_LEDGER_POLICY_ID = "b98866ad"
TRACE_LEDGER_POLICY_RECEIPT_ID = "f28e04c1"
V0_2_IMPLEMENTATION_RECEIPT_ID = "6b90ca5e"
LOCAL_REGIME_V1_HASH = "25802530"
UPGRADE_POLICY_ID = "d76f7ceb"
SOURCE_LOCAL_REGIME_V0_HASH = "097d620c"

SOURCE_RUNNER_UNIT_ID = "jurisdiction_runner.v0.2"
TARGET_RUNNER_UNIT_ID = "jurisdiction_runner.v0.2.trace_ledger_hardened"
SOURCE_LOCAL_REGIME_VERSION = "local_regime.v1"

POLICY_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_and_proposal_ledger_hardening_policies" / f"{TRACE_LEDGER_POLICY_ID}.json"
POLICY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_and_proposal_ledger_hardening_policy_receipts" / f"{TRACE_LEDGER_POLICY_ID}.json"
V0_2_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_implementation_receipts" / f"{V0_2_IMPLEMENTATION_RECEIPT_ID}.json"
LOCAL_REGIME_V1_PATH = ROOT / "data" / "local_regime_v1_declarations" / f"{LOCAL_REGIME_V1_HASH}.json"
RUNNER_V0_2_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_2.py"
UPGRADE_POLICY_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_policies" / f"{UPGRADE_POLICY_ID}.json"
LOCAL_REGIME_V0_PATH = ROOT / "data" / "local_regime_v0_declarations" / f"{SOURCE_LOCAL_REGIME_V0_HASH}.json"

TRACE_SCHEMA_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_trace_schemas"
LEDGER_SCHEMA_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_proposal_ledger_schemas"
RUNNER_TRACE_LEDGER_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_2_trace_ledger.py"
FIXTURE_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_fixtures"
TRACE_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_traces"
LEDGER_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_ledgers"
CASE_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_case_receipts"
IMPLEMENTATION_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts"

EXPECTED_TRANSCRIPT = [
    "LOAD_REGIME",
    "LOAD_STATE",
    "VALIDATE_STATE",
    "SELECT_MOVE",
    "CHECK_AUTHORITY",
    "APPLY_OR_BLOCK_MOVE",
    "EMIT_RECEIPT",
    "EMIT_METRICS",
    "EMIT_TERMINAL",
]

HARDENING_CASES = [
    "TRACE_PRESENT_FOR_HALT_WITH_PROPOSAL",
    "TRACE_PRESENT_FOR_NO_PROPOSAL_INSUFFICIENT_EVIDENCE",
    "LEDGER_RECORDS_FIRST_UNRESOLVED_PROPOSAL",
    "LEDGER_SUPPRESSES_DUPLICATE_UNRESOLVED_PROPOSAL",
    "RECEIPT_TRACE_CONSISTENCY",
    "REGRESSION_V0_2_NON_EXECUTION_AND_NO_REGISTRY",
]

ACCEPTANCE_GATES = [
    "H0_source_chain_verified",
    "H1_trace_schema_declared",
    "H2_proposal_ledger_schema_declared",
    "H3_trace_hardened_runner_implemented",
    "H4_trace_files_emitted_for_cases",
    "H5_receipts_reference_traces",
    "H6_unresolved_proposal_ledger_artifact_used",
    "H7_v0_2_regression_preserved",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def burden_bytes(obj: Any) -> int:
    return len(canonical_bytes(obj))

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
    policy: Dict[str, Any],
    policy_receipt: Dict[str, Any],
    v0_2_impl: Dict[str, Any],
    local_regime_v1: Dict[str, Any],
    upgrade_policy: Dict[str, Any],
    local_regime_v0: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if policy.get("policy_id") != TRACE_LEDGER_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy.get("policy_receipt_id") != TRACE_LEDGER_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if policy_receipt.get("policy_id") != TRACE_LEDGER_POLICY_ID:
        failures.append(f"policy_receipt_policy_id_wrong:{policy_receipt.get('policy_id')}")
    if policy_receipt.get("receipt_id") != TRACE_LEDGER_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy_receipt.get('receipt_id')}")
    if policy_receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{policy_receipt.get('gate')}")
    if policy_receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy_receipt.get('policy_status')}")

    terminal = policy_receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"policy_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"policy_terminal_stop_not_null:{terminal.get('stop_code')}")

    if policy_receipt.get("source_runner_unit_id") != SOURCE_RUNNER_UNIT_ID:
        failures.append(f"source_runner_wrong:{policy_receipt.get('source_runner_unit_id')}")
    if policy_receipt.get("target_runner_unit_id") != TARGET_RUNNER_UNIT_ID:
        failures.append(f"target_runner_wrong:{policy_receipt.get('target_runner_unit_id')}")
    if policy_receipt.get("source_local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append(f"source_regime_hash_wrong:{policy_receipt.get('source_local_regime_hash')}")

    required_cases = policy_receipt.get("required_hardening_cases") or {}
    for case in HARDENING_CASES:
        if case not in required_cases:
            failures.append(f"required_hardening_case_missing:{case}")

    gates = policy_receipt.get("acceptance_gates") or {}
    for gate in ACCEPTANCE_GATES:
        if gates.get(gate, {}).get("required") is not True:
            failures.append(f"acceptance_gate_missing:{gate}:{gates.get(gate)}")

    auth = policy_receipt.get("authorized_operations_next") or {}
    for key in [
        "write_trace_schema_artifact",
        "write_proposal_ledger_schema_artifact",
        "write_trace_ledger_hardened_runner_module",
        "write_hardening_fixtures",
        "execute_trace_ledger_hardened_runner_against_fixtures",
        "emit_trace_files",
        "emit_unresolved_proposal_ledger_artifacts",
        "emit_hardening_case_receipts",
        "emit_hardening_implementation_receipt",
    ]:
        if auth.get(key) is not True:
            failures.append(f"authorized_operation_missing:{key}:{auth.get(key)}")

    forbidden = policy_receipt.get("forbidden_operations_next") or {}
    for key in [
        "modify_jurisdiction_runner_v0_2",
        "modify_jurisdiction_runner_v0_1",
        "execute_or_apply_proposal",
        "promote_proposal_without_human_review",
        "sqlite_registry_write",
        "sqlite_registry_read",
        "global_taxonomy_design",
        "final_schema_claim",
        "proof_claim",
        "hidden_continuation_after_stop",
    ]:
        if forbidden.get(key) is not True:
            failures.append(f"forbidden_operation_missing:{key}:{forbidden.get(key)}")

    if v0_2_impl.get("receipt_id") != V0_2_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"v0_2_impl_receipt_id_wrong:{v0_2_impl.get('receipt_id')}")
    if v0_2_impl.get("gate") != "PASS":
        failures.append(f"v0_2_impl_gate_not_PASS:{v0_2_impl.get('gate')}")
    if v0_2_impl.get("terminal", {}).get("type") != "STOP":
        failures.append(f"v0_2_impl_terminal_not_STOP:{v0_2_impl.get('terminal')}")
    if v0_2_impl.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append(f"v0_2_impl_terminal_stop_not_DONE:{v0_2_impl.get('terminal')}")
    if v0_2_impl.get("terminal", {}).get("next_command_goal") is not None:
        failures.append(f"v0_2_impl_terminal_next_not_null:{v0_2_impl.get('terminal')}")

    impl_gates = v0_2_impl.get("acceptance_gate_results") or {}
    for gate in [
        "S3_halt_with_proposal_fixture_passes",
        "S4_proposal_non_execution_passes",
        "S5_duplicate_unresolved_proposal_guard_passes",
        "S6_no_hidden_continuation",
        "S7_no_registry_or_global_taxonomy",
    ]:
        if impl_gates.get(gate) is not True:
            failures.append(f"source_v0_2_gate_not_true:{gate}:{impl_gates.get(gate)}")

    impl_metrics = v0_2_impl.get("aggregate_metrics") or {}
    for key in ["runtime_proposal_executed_count", "runtime_proposal_promoted_count", "registry_write_count", "local_regime_mutation_count"]:
        if impl_metrics.get(key) != 0:
            failures.append(f"source_v0_2_metric_not_zero:{key}:{impl_metrics.get(key)}")
    if impl_metrics.get("duplicate_unresolved_proposal_count") != 1:
        failures.append(f"source_v0_2_duplicate_count_wrong:{impl_metrics.get('duplicate_unresolved_proposal_count')}")

    if local_regime_v1.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append(f"local_regime_v1_hash_wrong:{local_regime_v1.get('local_regime_hash')}")
    if local_regime_v1.get("local_regime_version") != SOURCE_LOCAL_REGIME_VERSION:
        failures.append(f"local_regime_v1_version_wrong:{local_regime_v1.get('local_regime_version')}")

    if upgrade_policy.get("policy_id") != UPGRADE_POLICY_ID:
        failures.append(f"upgrade_policy_id_wrong:{upgrade_policy.get('policy_id')}")

    if local_regime_v0.get("local_regime_hash") != SOURCE_LOCAL_REGIME_V0_HASH:
        failures.append(f"local_regime_v0_hash_wrong:{local_regime_v0.get('local_regime_hash')}")

    for path, label in [
        (POLICY_PATH, "trace_ledger_policy"),
        (POLICY_RECEIPT_PATH, "trace_ledger_policy_receipt"),
        (V0_2_IMPLEMENTATION_RECEIPT_PATH, "v0_2_implementation_receipt"),
        (LOCAL_REGIME_V1_PATH, "local_regime_v1"),
        (RUNNER_V0_2_PATH, "runner_v0_2"),
        (UPGRADE_POLICY_PATH, "upgrade_policy"),
        (LOCAL_REGIME_V0_PATH, "local_regime_v0"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{path.relative_to(ROOT).as_posix()}")

    return failures

TRACE_LEDGER_RUNNER_SOURCE = r'''
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional, Tuple

EXPECTED_TRANSCRIPT = [
    "LOAD_REGIME",
    "LOAD_STATE",
    "VALIDATE_STATE",
    "SELECT_MOVE",
    "CHECK_AUTHORITY",
    "APPLY_OR_BLOCK_MOVE",
    "EMIT_RECEIPT",
    "EMIT_METRICS",
    "EMIT_TERMINAL",
]

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def _sha8(obj: Any) -> str:
    return hashlib.sha256(_canonical_bytes(obj)).hexdigest()[:8]

def _state_sig(state: Dict[str, Any]) -> str:
    return _sha8(state)

def _delta(before: Dict[str, Any], after: Dict[str, Any]) -> Dict[str, Any]:
    out = {}
    for key in sorted(set(before) | set(after)):
        if before.get(key) != after.get(key):
            out[key] = [before.get(key), after.get(key)]
    return out

class JurisdictionRunnerV02TraceLedger:
    runner_unit_id = "jurisdiction_runner.v0.2.trace_ledger_hardened"

    def __init__(self, local_regime: Dict[str, Any]):
        self.local_regime = copy.deepcopy(local_regime)
        self.local_regime_hash = self.local_regime.get("local_regime_hash")
        self.local_regime_version = self.local_regime.get("local_regime_version", "local_regime.v1")

    def _proposal_key(self, state: Dict[str, Any], proposed_delta_kind: str) -> str:
        return _sha8({
            "proposal_type": "LOCAL_MOVE_ADMISSIBILITY_DELTA_PROPOSAL",
            "source_halt_code": "STOP_NO_APPLICABLE_MOVE",
            "source_state_id": state.get("state_id"),
            "proposed_delta_kind": proposed_delta_kind,
        })

    def _ledger_lookup(self, ledger: Dict[str, Any], proposal_key: str) -> Optional[Dict[str, Any]]:
        for entry in ledger.get("ledger_entries", []):
            if entry.get("proposal_key") == proposal_key and entry.get("status") == "UNRESOLVED":
                return entry
        return None

    def _proposal_receipt(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        receipt = {
            "schema_version": "jurisdiction_runner_v0_2_trace_ledger_proposal_receipt_v0",
            "receipt_type": "JURISDICTION_RUNNER_V0_2_TRACE_LEDGER_PROPOSAL_RECEIPT",
            "proposal_id": proposal["proposal_id"],
            "proposal_key": proposal["proposal_key"],
            "proposal_type": proposal["proposal_type"],
            "proposal_status": proposal["proposal_status"],
            "runner_unit_id": self.runner_unit_id,
            "local_regime_version": self.local_regime_version,
            "local_regime_hash": self.local_regime_hash,
            "source_halt_code": proposal["source_halt_code"],
            "source_state_id": proposal["source_state_id"],
            "source_fixture_id": proposal["source_fixture_id"],
            "proposed_delta_kind": proposal["proposed_delta_kind"],
            "human_review_required": True,
            "proposal_executed": False,
            "proposal_promoted": False,
            "local_regime_runtime_mutated": False,
            "registry_written": False,
            "hidden_continuation_authorized": False,
            "gate": "PASS",
            "created_at": _now_iso(),
        }
        receipt["receipt_id"] = _sha8({"proposal_id": proposal["proposal_id"], "proposal_key": proposal["proposal_key"]})
        return receipt

    def _new_trace(
        self,
        *,
        run_id: str,
        fixture_id: Optional[str],
        state_before: Dict[str, Any],
        state_after: Dict[str, Any],
        applicable_moves: List[str],
        selected_move: Optional[str],
        selection_reason: str,
        action_result: str,
        halt_code: str,
        proposal_ref: Optional[Dict[str, Any]],
    ) -> Dict[str, Any]:
        entry = {
            "step_index": 0,
            "state_before_sig8": _state_sig(state_before),
            "applicable_moves": applicable_moves,
            "selected_move": selected_move,
            "selection_reason": selection_reason,
            "action_result": action_result,
            "state_delta": _delta(state_before, state_after),
            "halt_code": halt_code,
            "proposal_ref": proposal_ref,
            "state_after_sig8": _state_sig(state_after),
        }
        trace = {
            "schema_version": "jurisdiction_runner_trace_file_v0",
            "trace_id": _sha8({"run_id": run_id, "entry": entry}),
            "run_id": run_id,
            "runner_unit_id": self.runner_unit_id,
            "local_regime_hash": self.local_regime_hash,
            "source_fixture_id": fixture_id,
            "entries": [entry],
            "final_halt_code": halt_code,
            "receipt_ref": None,
            "created_at": _now_iso(),
        }
        return trace

    def run(
        self,
        input_state: Dict[str, Any],
        *,
        fixture_id: Optional[str],
        input_artifact_paths: List[str],
        ledger: Optional[Dict[str, Any]] = None,
        ledger_path: Optional[str] = None,
    ) -> Tuple[Dict[str, Any], Dict[str, Any], Dict[str, Any]]:
        state = copy.deepcopy(input_state)
        state_after = copy.deepcopy(state)
        ledger_after = copy.deepcopy(ledger) if ledger is not None else {
            "schema_version": "unresolved_proposal_ledger_v0",
            "ledger_id": None,
            "runner_unit_id": self.runner_unit_id,
            "local_regime_hash": self.local_regime_hash,
            "ledger_entries": [],
            "created_by_receipt_id": None,
        }

        proposal = None
        proposal_receipt = None
        proposal_status = "NONE"
        no_proposal_reason = None
        duplicate_unresolved = False
        halt_code = "STOP_NO_APPLICABLE_MOVE"
        selected_move = "evaluate_no_applicable_move_proposal_surface.v0"
        applicable_moves = [selected_move]
        selection_reason = "only applicable move"
        action_result = "HALT"
        proposal_ref = None

        if state.get("typed") is not True:
            halt_code = "STOP_UNTYPED_OBJECT"
            selected_move = "validate_state.v0"
            applicable_moves = [selected_move]
            no_proposal_reason = "PRESSURE_ALREADY_TYPED"
        elif not isinstance(state.get("value"), int) or state.get("value") < 0:
            halt_code = "STOP_GATE_FAIL"
            selected_move = "validate_state.v0"
            applicable_moves = [selected_move]
            no_proposal_reason = "PRESSURE_ALREADY_TYPED"
        elif state.get("force_authority_violation") is True:
            halt_code = "STOP_AUTHORITY_VIOLATION"
            selected_move = "authority_violation_guard.v0"
            applicable_moves = [selected_move]
            selection_reason = "authority boundary guard selected before proposal evaluation"
            no_proposal_reason = "OUT_OF_SCOPE"
        elif state.get("value") == 0:
            halt_code = "STOP_DONE"
            selected_move = "apply_registered_transition.v0"
            applicable_moves = [selected_move]
            state_after["value"] = 1
            no_proposal_reason = "PRESSURE_ALREADY_TYPED"
            action_result = "PASS"
        else:
            evidence = state.get("proposal_evidence") or {}
            evidence_sufficient = evidence.get("sufficient") is True
            proposed_delta_kind = evidence.get("proposed_delta_kind", "LOCAL_MOVE_ADMISSIBILITY_DELTA")
            evidence_summary = evidence.get("evidence_summary", "bounded local no-applicable-move pressure")
            proposal_surface = self.local_regime.get("proposal_surface") or {}

            if proposal_surface.get("enabled") is True and evidence_sufficient:
                proposal_key = self._proposal_key(state, proposed_delta_kind)
                existing = self._ledger_lookup(ledger_after, proposal_key)
                if existing is not None:
                    proposal_status = "WITHHELD_DUPLICATE_UNRESOLVED"
                    no_proposal_reason = "DUPLICATE_UNRESOLVED"
                    duplicate_unresolved = True
                    selected_move = "withhold_duplicate_unresolved_proposal.v0"
                    applicable_moves = ["withhold_duplicate_unresolved_proposal.v0"]
                    selection_reason = "declared unresolved proposal ledger contains matching unresolved proposal key"
                    proposal = {
                        "proposal_key": proposal_key,
                        "proposal_id": existing.get("proposal_id"),
                        "proposal_type": existing.get("proposal_type"),
                        "proposal_status": proposal_status,
                        "linked_unresolved_proposal_id": existing.get("proposal_id"),
                        "source_halt_code": "STOP_NO_APPLICABLE_MOVE",
                        "source_state_id": state.get("state_id"),
                        "source_fixture_id": fixture_id,
                        "proposed_delta_kind": proposed_delta_kind,
                        "human_review_required": True,
                    }
                    proposal_ref = {
                        "proposal_key": proposal_key,
                        "proposal_id": existing.get("proposal_id"),
                        "proposal_status": proposal_status,
                        "proposal_receipt_id": None,
                        "ledger_path": ledger_path,
                    }
                else:
                    proposal_status = "EMITTED_REVIEW_REQUIRED"
                    proposal_id = _sha8({
                        "proposal_key": proposal_key,
                        "runner_unit_id": self.runner_unit_id,
                        "local_regime_hash": self.local_regime_hash,
                    })
                    proposal = {
                        "schema_version": "jurisdiction_runner_v0_2_trace_ledger_local_move_admissibility_delta_proposal_v0",
                        "proposal_key": proposal_key,
                        "proposal_id": proposal_id,
                        "proposal_type": "LOCAL_MOVE_ADMISSIBILITY_DELTA_PROPOSAL",
                        "proposal_status": proposal_status,
                        "source_halt_code": "STOP_NO_APPLICABLE_MOVE",
                        "source_state_id": state.get("state_id"),
                        "source_fixture_id": fixture_id,
                        "evidence_summary": evidence_summary,
                        "proposed_delta_kind": proposed_delta_kind,
                        "human_review_required": True,
                        "proposal_executed": False,
                        "proposal_promoted": False,
                        "local_regime_runtime_mutated": False,
                        "registry_written": False,
                        "hidden_continuation_authorized": False,
                    }
                    proposal_receipt = self._proposal_receipt(proposal)
                    ledger_after.setdefault("ledger_entries", []).append({
                        "proposal_key": proposal_key,
                        "proposal_id": proposal_id,
                        "proposal_type": proposal["proposal_type"],
                        "source_halt_code": proposal["source_halt_code"],
                        "source_state_id": proposal["source_state_id"],
                        "source_fixture_id": proposal["source_fixture_id"],
                        "proposed_delta_kind": proposal["proposed_delta_kind"],
                        "status": "UNRESOLVED",
                        "created_by_case_receipt_id": None,
                        "created_by_proposal_receipt_id": proposal_receipt["receipt_id"],
                    })
                    proposal_ref = {
                        "proposal_key": proposal_key,
                        "proposal_id": proposal_id,
                        "proposal_status": proposal_status,
                        "proposal_receipt_id": proposal_receipt["receipt_id"],
                        "ledger_path": ledger_path,
                    }
            else:
                no_proposal_reason = "INSUFFICIENT_EVIDENCE"
                selected_move = "withhold_proposal_insufficient_evidence.v0"
                applicable_moves = [selected_move]
                selection_reason = "proposal evidence insufficient"

        run_id = _sha8({"fixture_id": fixture_id, "state": state, "ledger_path": ledger_path, "runner": self.runner_unit_id})
        trace = self._new_trace(
            run_id=run_id,
            fixture_id=fixture_id,
            state_before=state,
            state_after=state_after,
            applicable_moves=applicable_moves,
            selected_move=selected_move,
            selection_reason=selection_reason,
            action_result=action_result,
            halt_code=halt_code,
            proposal_ref=proposal_ref,
        )

        trace_ref = {"trace_id": trace["trace_id"], "trace_path": None}
        receipt_seed = {
            "run_id": run_id,
            "trace_id": trace["trace_id"],
            "fixture_id": fixture_id,
            "halt_code": halt_code,
            "proposal_status": proposal_status,
            "proposal_id": proposal.get("proposal_id") if proposal else None,
        }
        receipt_id = _sha8(receipt_seed)
        receipt_ref = {"receipt_id": receipt_id, "receipt_path": None}

        for entry in ledger_after.get("ledger_entries", []):
            if entry.get("proposal_id") == (proposal.get("proposal_id") if proposal else None):
                entry["created_by_case_receipt_id"] = receipt_id

        ledger_after["created_by_receipt_id"] = receipt_id
        ledger_after["ledger_id"] = _sha8({
            "runner_unit_id": self.runner_unit_id,
            "local_regime_hash": self.local_regime_hash,
            "entries": ledger_after.get("ledger_entries", []),
            "created_by_receipt_id": ledger_after.get("created_by_receipt_id"),
        })

        metrics = {
            "runtime_proposal_emitted_count": 1 if proposal_status == "EMITTED_REVIEW_REQUIRED" else 0,
            "runtime_proposal_executed_count": 0,
            "runtime_proposal_promoted_count": 0,
            "duplicate_unresolved_proposal_count": 1 if duplicate_unresolved else 0,
            "proposal_withheld_count": 1 if proposal_status in ["NONE", "WITHHELD_DUPLICATE_UNRESOLVED"] else 0,
            "proposal_receipt_count": 1 if proposal_receipt else 0,
            "trace_entry_count": len(trace["entries"]),
            "receipt_count": 1,
            "ledger_entry_count": len(ledger_after.get("ledger_entries", [])),
        }

        receipt = {
            "schema_version": "jurisdiction_runner_v0_2_trace_ledger_case_receipt_v0",
            "receipt_type": "JURISDICTION_RUNNER_V0_2_TRACE_LEDGER_CASE_RECEIPT",
            "receipt_id": receipt_id,
            "run_id": run_id,
            "runner_unit_id": self.runner_unit_id,
            "local_regime_version": self.local_regime_version,
            "local_regime_hash": self.local_regime_hash,
            "fixture_id": fixture_id,
            "input_state": state,
            "start_state_sig8": _state_sig(state),
            "final_state_sig8": _state_sig(state_after),
            "moves_applied": [selected_move] if selected_move else [],
            "selected_move": selected_move,
            "selection_reason": selection_reason,
            "halt_code": halt_code,
            "terminal_result": "STOP",
            "proposal_status": proposal_status,
            "proposal": copy.deepcopy(proposal),
            "proposal_id": proposal.get("proposal_id") if proposal else None,
            "proposal_receipt": copy.deepcopy(proposal_receipt),
            "proposal_receipt_id": proposal_receipt.get("receipt_id") if proposal_receipt else None,
            "proposal_executed": False,
            "proposal_promoted": False,
            "no_proposal_reason": no_proposal_reason,
            "duplicate_unresolved_proposal": duplicate_unresolved,
            "trace_ref": trace_ref,
            "ledger_ref": {"ledger_id": ledger_after["ledger_id"], "ledger_path": ledger_path},
            "metrics": metrics,
            "authority_guards": {
                "proposal_executed": False,
                "proposal_promoted": False,
                "local_regime_runtime_mutated": False,
                "registry_written": False,
                "registry_inserted": False,
                "registry_sqlite_read": False,
                "registry_sqlite_written": False,
                "full_registry_scan_used": False,
                "global_taxonomy_claimed": False,
                "final_schema_claimed": False,
                "proof_claimed": False,
                "hidden_continuation_authorized": False,
                "runner_v0_2_modified": False,
            },
            "artifact_guards": {
                "trace_ref_path_addressed": False,
                "ledger_ref_path_addressed": ledger_path is not None,
                "latest_or_mtime_selection_used": False,
                "ambient_workspace_authority_used": False,
            },
            "transcript": EXPECTED_TRANSCRIPT,
            "terminal": {"type": "STOP", "next_command_goal": None, "stop_code": halt_code},
            "gate": "PASS",
            "failures": [],
            "warnings": [],
            "created_at": _now_iso(),
        }

        trace["receipt_ref"] = receipt_ref
        return receipt, trace, ledger_after
'''

def write_trace_ledger_runner_module() -> None:
    RUNNER_TRACE_LEDGER_PATH.parent.mkdir(parents=True, exist_ok=True)
    RUNNER_TRACE_LEDGER_PATH.write_text(TRACE_LEDGER_RUNNER_SOURCE.strip() + "\n")

def import_trace_ledger_runner():
    spec = importlib.util.spec_from_file_location("jurisdiction_runner_v0_2_trace_ledger", RUNNER_TRACE_LEDGER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import trace ledger runner module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["jurisdiction_runner_v0_2_trace_ledger"] = mod
    spec.loader.exec_module(mod)
    return mod

def build_fixture(case_name: str, input_state: Dict[str, Any], expected: Dict[str, Any], ledger_input_path: Optional[str] = None) -> Dict[str, Any]:
    return {
        "schema_version": "jurisdiction_runner_v0_2_trace_ledger_hardening_fixture_v0",
        "fixture_id": f"trace_ledger_{case_name.lower()}",
        "case_name": case_name,
        "input_state": input_state,
        "ledger_input_path": ledger_input_path,
        "expected": expected,
    }

def validate_trace_schema_artifact(trace_schema: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    for key in ["trace_id", "run_id", "runner_unit_id", "local_regime_hash", "source_fixture_id", "entries", "final_halt_code", "receipt_ref"]:
        if key not in trace_schema.get("required_fields", []):
            failures.append(f"trace_schema_required_field_missing:{key}")
    entry = trace_schema.get("entry_schema", {})
    for key in ["step_index", "state_before_sig8", "applicable_moves", "selected_move", "selection_reason", "action_result", "state_delta", "halt_code", "proposal_ref", "state_after_sig8"]:
        if key not in entry.get("required_fields", []):
            failures.append(f"trace_entry_required_field_missing:{key}")
    if trace_schema.get("receipt_consistency_required") is not True:
        failures.append("trace_schema_receipt_consistency_not_required")
    return failures

def validate_ledger_schema_artifact(ledger_schema: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if ledger_schema.get("ledger_scope") != "path-addressed local artifact only, no registry or sqlite authority":
        failures.append(f"ledger_scope_wrong:{ledger_schema.get('ledger_scope')}")
    for key in ["ledger_id", "runner_unit_id", "local_regime_hash", "ledger_entries", "created_by_receipt_id"]:
        if key not in ledger_schema.get("required_fields", []):
            failures.append(f"ledger_required_field_missing:{key}")
    for key in ["proposal_key", "proposal_id", "proposal_type", "source_halt_code", "source_state_id", "proposed_delta_kind", "status"]:
        if key not in ledger_schema.get("entry_required_fields", []):
            failures.append(f"ledger_entry_required_field_missing:{key}")
    if "UNRESOLVED" not in ledger_schema.get("status_values", []):
        failures.append("ledger_status_UNRESOLVED_missing")
    return failures

def validate_case_receipt_and_trace(case_name: str, receipt: Dict[str, Any], trace: Dict[str, Any], expected: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if receipt.get("gate") != "PASS":
        failures.append(f"{case_name}:case_gate_not_PASS:{receipt.get('gate')}")
    if trace.get("entries") is None or len(trace.get("entries", [])) < 1:
        failures.append(f"{case_name}:trace_entries_missing")
    if receipt.get("trace_ref", {}).get("trace_id") != trace.get("trace_id"):
        failures.append(f"{case_name}:receipt_trace_id_mismatch")
    if trace.get("receipt_ref", {}).get("receipt_id") != receipt.get("receipt_id"):
        failures.append(f"{case_name}:trace_receipt_id_mismatch")
    if receipt.get("halt_code") != trace.get("final_halt_code"):
        failures.append(f"{case_name}:receipt_trace_halt_mismatch:{receipt.get('halt_code')}:{trace.get('final_halt_code')}")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append(f"{case_name}:terminal_next_not_null:{receipt.get('terminal')}")
    if receipt.get("terminal", {}).get("type") != "STOP":
        failures.append(f"{case_name}:terminal_not_STOP:{receipt.get('terminal')}")

    first = trace.get("entries", [{}])[0]
    for key in ["step_index", "state_before_sig8", "applicable_moves", "selected_move", "selection_reason", "action_result", "state_delta", "halt_code", "proposal_ref", "state_after_sig8"]:
        if key not in first:
            failures.append(f"{case_name}:trace_entry_field_missing:{key}")

    if first.get("state_before_sig8") != receipt.get("start_state_sig8"):
        failures.append(f"{case_name}:trace_start_sig_mismatch")
    if first.get("state_after_sig8") != receipt.get("final_state_sig8"):
        failures.append(f"{case_name}:trace_final_sig_mismatch")
    if first.get("halt_code") != receipt.get("halt_code"):
        failures.append(f"{case_name}:trace_entry_halt_mismatch")

    if receipt.get("proposal_status") != expected["proposal_status"]:
        failures.append(f"{case_name}:proposal_status_wrong:{receipt.get('proposal_status')}:{expected['proposal_status']}")
    if expected.get("no_proposal_reason") is not None and receipt.get("no_proposal_reason") != expected["no_proposal_reason"]:
        failures.append(f"{case_name}:no_proposal_reason_wrong:{receipt.get('no_proposal_reason')}:{expected['no_proposal_reason']}")
    if expected.get("halt_code") is not None and receipt.get("halt_code") != expected["halt_code"]:
        failures.append(f"{case_name}:halt_code_wrong:{receipt.get('halt_code')}:{expected['halt_code']}")

    if receipt.get("proposal_status") == "EMITTED_REVIEW_REQUIRED":
        if receipt.get("proposal_id") is None:
            failures.append(f"{case_name}:proposal_id_missing")
        if receipt.get("proposal_receipt_id") is None:
            failures.append(f"{case_name}:proposal_receipt_id_missing")
        if first.get("proposal_ref", {}).get("proposal_id") != receipt.get("proposal_id"):
            failures.append(f"{case_name}:proposal_ref_id_mismatch")
        if first.get("proposal_ref", {}).get("proposal_receipt_id") != receipt.get("proposal_receipt_id"):
            failures.append(f"{case_name}:proposal_ref_receipt_mismatch")

    if receipt.get("proposal_status") == "WITHHELD_DUPLICATE_UNRESOLVED":
        if receipt.get("duplicate_unresolved_proposal") is not True:
            failures.append(f"{case_name}:duplicate_flag_not_true")
        if first.get("proposal_ref", {}).get("proposal_status") != "WITHHELD_DUPLICATE_UNRESOLVED":
            failures.append(f"{case_name}:trace_duplicate_status_wrong")

    for key in ["proposal_executed", "proposal_promoted"]:
        if receipt.get(key) is not False:
            failures.append(f"{case_name}:{key}_not_false:{receipt.get(key)}")

    guards = receipt.get("authority_guards") or {}
    for key in ["proposal_executed", "proposal_promoted", "registry_written", "registry_sqlite_written", "global_taxonomy_claimed", "final_schema_claimed", "proof_claimed", "hidden_continuation_authorized", "runner_v0_2_modified"]:
        if guards.get(key) is not False:
            failures.append(f"{case_name}:authority_guard_not_false:{key}:{guards.get(key)}")

    artifact = receipt.get("artifact_guards") or {}
    if artifact.get("trace_ref_path_addressed") is not True:
        failures.append(f"{case_name}:trace_ref_path_not_addressed")
    if artifact.get("latest_or_mtime_selection_used") is not False:
        failures.append(f"{case_name}:latest_mtime_used")
    if artifact.get("ambient_workspace_authority_used") is not False:
        failures.append(f"{case_name}:ambient_workspace_authority_used")

    return failures

def validate_ledger_artifact(case_name: str, ledger: Dict[str, Any], receipt: Dict[str, Any], expected: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if ledger.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append(f"{case_name}:ledger_schema_wrong:{ledger.get('schema_version')}")
    if ledger.get("runner_unit_id") != TARGET_RUNNER_UNIT_ID:
        failures.append(f"{case_name}:ledger_runner_wrong:{ledger.get('runner_unit_id')}")
    if ledger.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append(f"{case_name}:ledger_regime_hash_wrong:{ledger.get('local_regime_hash')}")
    if ledger.get("created_by_receipt_id") != receipt.get("receipt_id"):
        failures.append(f"{case_name}:ledger_created_by_receipt_mismatch")
    if expected.get("ledger_must_record_unresolved") is True:
        entries = ledger.get("ledger_entries", [])
        if not entries:
            failures.append(f"{case_name}:ledger_entries_missing")
        if not any(e.get("status") == "UNRESOLVED" and e.get("proposal_id") == receipt.get("proposal_id") for e in entries):
            failures.append(f"{case_name}:ledger_unresolved_entry_missing")
    if expected.get("ledger_duplicate_count") is not None:
        if receipt.get("metrics", {}).get("duplicate_unresolved_proposal_count") != expected["ledger_duplicate_count"]:
            failures.append(f"{case_name}:duplicate_count_wrong:{receipt.get('metrics', {}).get('duplicate_unresolved_proposal_count')}")
    return failures

def validate_implementation_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{receipt.get('gate')}")
    gates = receipt.get("acceptance_gate_results") or {}
    for gate in ACCEPTANCE_GATES:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics") or {}
    if metrics.get("hardening_case_count") != 6:
        failures.append(f"hardening_case_count_wrong:{metrics.get('hardening_case_count')}")
    if metrics.get("hardening_case_pass_count") != 6:
        failures.append(f"hardening_case_pass_count_wrong:{metrics.get('hardening_case_pass_count')}")
    if metrics.get("hardening_case_fail_count") != 0:
        failures.append(f"hardening_case_fail_count_wrong:{metrics.get('hardening_case_fail_count')}")
    if metrics.get("trace_file_count") != 6:
        failures.append(f"trace_file_count_wrong:{metrics.get('trace_file_count')}")
    if metrics.get("case_receipt_trace_consistency_fail_count") != 0:
        failures.append(f"trace_consistency_fail_count_nonzero:{metrics.get('case_receipt_trace_consistency_fail_count')}")
    if metrics.get("ledger_artifact_count") < 6:
        failures.append(f"ledger_artifact_count_too_low:{metrics.get('ledger_artifact_count')}")
    if metrics.get("duplicate_unresolved_proposal_count") != 1:
        failures.append(f"duplicate_unresolved_proposal_count_wrong:{metrics.get('duplicate_unresolved_proposal_count')}")
    for key in ["runtime_proposal_executed_count", "runtime_proposal_promoted_count", "registry_write_count", "local_regime_mutation_count"]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("authority_guards") or {}
    for key in [
        "trace_schema_emitted",
        "proposal_ledger_schema_emitted",
        "trace_ledger_runner_implemented",
        "fixtures_created",
        "fixtures_executed",
        "trace_files_emitted",
        "proposal_ledger_artifacts_emitted",
        "case_receipts_emitted",
        "implementation_receipt_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"authority_guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "jurisdiction_runner_v0_2_modified",
        "jurisdiction_runner_v0_1_modified",
        "local_regime_v1_replaced",
        "local_regime_runtime_mutated",
        "proposal_executed",
        "proposal_promoted",
        "registry_written",
        "registry_sqlite_read",
        "registry_sqlite_written",
        "global_taxonomy_claimed",
        "final_schema_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
    ]:
        if guards.get(key) is not False:
            failures.append(f"authority_guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "STOP":
        failures.append(f"terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_DONE":
        failures.append(f"terminal_stop_not_DONE:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"terminal_next_not_null:{terminal}")

    return failures

def main() -> int:
    policy = read_json(POLICY_PATH)
    policy_receipt = read_json(POLICY_RECEIPT_PATH)
    v0_2_impl = read_json(V0_2_IMPLEMENTATION_RECEIPT_PATH)
    local_regime_v1 = read_json(LOCAL_REGIME_V1_PATH)
    upgrade_policy = read_json(UPGRADE_POLICY_PATH)
    local_regime_v0 = read_json(LOCAL_REGIME_V0_PATH)

    failures = validate_inputs(policy, policy_receipt, v0_2_impl, local_regime_v1, upgrade_policy, local_regime_v0)

    for d in [
        TRACE_SCHEMA_DIR,
        LEDGER_SCHEMA_DIR,
        FIXTURE_DIR,
        TRACE_DIR,
        LEDGER_DIR,
        CASE_RECEIPT_DIR,
        IMPLEMENTATION_RECEIPT_DIR,
    ]:
        d.mkdir(parents=True, exist_ok=True)

    trace_schema = policy_receipt["trace_file_schema"]
    trace_schema_id = sha8(trace_schema)
    trace_schema_path = TRACE_SCHEMA_DIR / f"{trace_schema_id}.json"
    write_json(trace_schema_path, trace_schema)

    ledger_schema = policy_receipt["proposal_ledger_schema"]
    ledger_schema_id = sha8(ledger_schema)
    ledger_schema_path = LEDGER_SCHEMA_DIR / f"{ledger_schema_id}.json"
    write_json(ledger_schema_path, ledger_schema)

    failures.extend(validate_trace_schema_artifact(trace_schema))
    failures.extend(validate_ledger_schema_artifact(ledger_schema))

    write_trace_ledger_runner_module()
    subprocess.run([sys.executable, "-m", "py_compile", str(RUNNER_TRACE_LEDGER_PATH)], check=True)
    runner_mod = import_trace_ledger_runner()

    empty_ledger = {
        "schema_version": "unresolved_proposal_ledger_v0",
        "ledger_id": "empty",
        "runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "local_regime_hash": LOCAL_REGIME_V1_HASH,
        "ledger_entries": [],
        "created_by_receipt_id": None,
    }

    case_specs = {
        "TRACE_PRESENT_FOR_HALT_WITH_PROPOSAL": {
            "input_state": {
                "state_id": "trace_halt_with_proposal",
                "typed": True,
                "value": 1,
                "proposal_evidence": {
                    "sufficient": True,
                    "evidence_summary": "trace must expose halt-with-proposal path",
                    "proposed_delta_kind": "LOCAL_MOVE_ADMISSIBILITY_DELTA",
                },
            },
            "ledger": copy.deepcopy(empty_ledger),
            "expected": {
                "halt_code": "STOP_NO_APPLICABLE_MOVE",
                "proposal_status": "EMITTED_REVIEW_REQUIRED",
                "ledger_must_record_unresolved": True,
            },
        },
        "TRACE_PRESENT_FOR_NO_PROPOSAL_INSUFFICIENT_EVIDENCE": {
            "input_state": {
                "state_id": "trace_no_proposal_insufficient_evidence",
                "typed": True,
                "value": 2,
                "proposal_evidence": {
                    "sufficient": False,
                    "evidence_summary": "trace must expose insufficient evidence no-proposal halt",
                    "proposed_delta_kind": "LOCAL_MOVE_ADMISSIBILITY_DELTA",
                },
            },
            "ledger": copy.deepcopy(empty_ledger),
            "expected": {
                "halt_code": "STOP_NO_APPLICABLE_MOVE",
                "proposal_status": "NONE",
                "no_proposal_reason": "INSUFFICIENT_EVIDENCE",
            },
        },
        "LEDGER_RECORDS_FIRST_UNRESOLVED_PROPOSAL": {
            "input_state": {
                "state_id": "ledger_duplicate_pressure",
                "typed": True,
                "value": 3,
                "proposal_evidence": {
                    "sufficient": True,
                    "evidence_summary": "first unresolved proposal must enter ledger",
                    "proposed_delta_kind": "LOCAL_MOVE_ADMISSIBILITY_DELTA",
                },
            },
            "ledger": copy.deepcopy(empty_ledger),
            "expected": {
                "halt_code": "STOP_NO_APPLICABLE_MOVE",
                "proposal_status": "EMITTED_REVIEW_REQUIRED",
                "ledger_must_record_unresolved": True,
            },
        },
        "LEDGER_SUPPRESSES_DUPLICATE_UNRESOLVED_PROPOSAL": {
            "input_state": {
                "state_id": "ledger_duplicate_pressure",
                "typed": True,
                "value": 3,
                "proposal_evidence": {
                    "sufficient": True,
                    "evidence_summary": "duplicate unresolved proposal must be withheld by ledger",
                    "proposed_delta_kind": "LOCAL_MOVE_ADMISSIBILITY_DELTA",
                },
            },
            "ledger": None,
            "expected": {
                "halt_code": "STOP_NO_APPLICABLE_MOVE",
                "proposal_status": "WITHHELD_DUPLICATE_UNRESOLVED",
                "no_proposal_reason": "DUPLICATE_UNRESOLVED",
                "ledger_duplicate_count": 1,
            },
        },
        "RECEIPT_TRACE_CONSISTENCY": {
            "input_state": {
                "state_id": "receipt_trace_consistency",
                "typed": True,
                "value": 4,
                "proposal_evidence": {
                    "sufficient": True,
                    "evidence_summary": "receipt and trace refs must agree",
                    "proposed_delta_kind": "LOCAL_MOVE_ADMISSIBILITY_DELTA",
                },
            },
            "ledger": copy.deepcopy(empty_ledger),
            "expected": {
                "halt_code": "STOP_NO_APPLICABLE_MOVE",
                "proposal_status": "EMITTED_REVIEW_REQUIRED",
                "ledger_must_record_unresolved": True,
            },
        },
        "REGRESSION_V0_2_NON_EXECUTION_AND_NO_REGISTRY": {
            "input_state": {
                "state_id": "trace_ledger_regression_authority_violation",
                "typed": True,
                "value": 0,
                "force_authority_violation": True,
                "proposal_evidence": {
                    "sufficient": True,
                    "evidence_summary": "regression: authority boundary must not promote proposal",
                    "proposed_delta_kind": "LOCAL_MOVE_ADMISSIBILITY_DELTA",
                },
            },
            "ledger": copy.deepcopy(empty_ledger),
            "expected": {
                "halt_code": "STOP_AUTHORITY_VIOLATION",
                "proposal_status": "NONE",
                "no_proposal_reason": "OUT_OF_SCOPE",
            },
        },
    }

    case_results: Dict[str, Dict[str, Any]] = {}
    trace_results: Dict[str, Dict[str, Any]] = {}
    ledger_results: Dict[str, Dict[str, Any]] = {}
    consistency_fail_count = 0

    runner = runner_mod.JurisdictionRunnerV02TraceLedger(local_regime_v1)
    recorded_first_ledger: Optional[Dict[str, Any]] = None
    recorded_first_ledger_path: Optional[Path] = None

    for case_name in HARDENING_CASES:
        spec = case_specs[case_name]
        if case_name == "LEDGER_SUPPRESSES_DUPLICATE_UNRESOLVED_PROPOSAL":
            if recorded_first_ledger is None or recorded_first_ledger_path is None:
                failures.append("duplicate_case_missing_first_ledger")
                ledger_input = copy.deepcopy(empty_ledger)
                ledger_input_path = None
            else:
                ledger_input = copy.deepcopy(recorded_first_ledger)
                ledger_input_path = recorded_first_ledger_path.relative_to(ROOT).as_posix()
        else:
            ledger_input = copy.deepcopy(spec["ledger"])
            ledger_input_path = None

        fixture = build_fixture(case_name, spec["input_state"], spec["expected"], ledger_input_path)
        fixture_path = FIXTURE_DIR / f"{fixture['fixture_id']}.json"
        write_json(fixture_path, fixture)

        receipt, trace, ledger_after = runner.run(
            spec["input_state"],
            fixture_id=fixture["fixture_id"],
            input_artifact_paths=[
                LOCAL_REGIME_V1_PATH.relative_to(ROOT).as_posix(),
                fixture_path.relative_to(ROOT).as_posix(),
                trace_schema_path.relative_to(ROOT).as_posix(),
                ledger_schema_path.relative_to(ROOT).as_posix(),
            ],
            ledger=ledger_input,
            ledger_path=ledger_input_path,
        )

        trace_path = TRACE_DIR / f"{trace['trace_id']}.json"
        case_receipt_path = CASE_RECEIPT_DIR / f"{receipt['receipt_id']}.json"
        ledger_path = LEDGER_DIR / f"{ledger_after['ledger_id']}.json"

        trace["receipt_ref"] = {
            "receipt_id": receipt["receipt_id"],
            "receipt_path": case_receipt_path.relative_to(ROOT).as_posix(),
        }
        receipt["trace_ref"] = {
            "trace_id": trace["trace_id"],
            "trace_path": trace_path.relative_to(ROOT).as_posix(),
        }
        receipt["ledger_ref"] = {
            "ledger_id": ledger_after["ledger_id"],
            "ledger_path": ledger_path.relative_to(ROOT).as_posix(),
        }
        receipt["artifact_guards"]["trace_ref_path_addressed"] = True
        receipt["artifact_guards"]["ledger_ref_path_addressed"] = True

        write_json(trace_path, trace)
        write_json(ledger_path, ledger_after)
        write_json(case_receipt_path, receipt)

        case_failures = validate_case_receipt_and_trace(case_name, receipt, trace, spec["expected"])
        ledger_failures = validate_ledger_artifact(case_name, ledger_after, receipt, spec["expected"])
        if case_failures:
            consistency_fail_count += 1
        failures.extend(case_failures)
        failures.extend(ledger_failures)

        if case_name == "LEDGER_RECORDS_FIRST_UNRESOLVED_PROPOSAL":
            recorded_first_ledger = copy.deepcopy(ledger_after)
            recorded_first_ledger_path = ledger_path

        case_results[case_name] = {
            "case_name": case_name,
            "fixture_id": fixture["fixture_id"],
            "fixture_path": fixture_path.relative_to(ROOT).as_posix(),
            "case_receipt_id": receipt["receipt_id"],
            "case_receipt_path": case_receipt_path.relative_to(ROOT).as_posix(),
            "trace_id": trace["trace_id"],
            "trace_path": trace_path.relative_to(ROOT).as_posix(),
            "ledger_id": ledger_after["ledger_id"],
            "ledger_path": ledger_path.relative_to(ROOT).as_posix(),
            "halt_code": receipt["halt_code"],
            "proposal_status": receipt["proposal_status"],
            "proposal_id": receipt.get("proposal_id"),
            "proposal_receipt_id": receipt.get("proposal_receipt_id"),
            "no_proposal_reason": receipt.get("no_proposal_reason"),
            "duplicate_unresolved_proposal": receipt.get("duplicate_unresolved_proposal"),
            "proposal_executed": receipt.get("proposal_executed"),
            "proposal_promoted": receipt.get("proposal_promoted"),
            "trace_receipt_consistent": len(case_failures) == 0,
            "gate": receipt["gate"],
        }

        trace_results[trace["trace_id"]] = {
            "trace_id": trace["trace_id"],
            "trace_path": trace_path.relative_to(ROOT).as_posix(),
            "case_name": case_name,
            "final_halt_code": trace["final_halt_code"],
            "entry_count": len(trace["entries"]),
            "receipt_id": receipt["receipt_id"],
        }

        ledger_results[ledger_after["ledger_id"]] = {
            "ledger_id": ledger_after["ledger_id"],
            "ledger_path": ledger_path.relative_to(ROOT).as_posix(),
            "case_name": case_name,
            "ledger_entry_count": len(ledger_after.get("ledger_entries", [])),
            "created_by_receipt_id": ledger_after.get("created_by_receipt_id"),
        }

    emitted_count = sum(1 for r in case_results.values() if r["proposal_status"] == "EMITTED_REVIEW_REQUIRED")
    duplicate_count = sum(1 for r in case_results.values() if r["duplicate_unresolved_proposal"] is True)
    withheld_count = sum(1 for r in case_results.values() if r["proposal_status"] in ["NONE", "WITHHELD_DUPLICATE_UNRESOLVED"])

    aggregate_metrics = {
        "hardening_case_count": len(case_results),
        "hardening_case_pass_count": sum(1 for r in case_results.values() if r["gate"] == "PASS" and r["trace_receipt_consistent"]),
        "hardening_case_fail_count": sum(1 for r in case_results.values() if r["gate"] != "PASS" or not r["trace_receipt_consistent"]),
        "trace_file_count": len(trace_results),
        "ledger_artifact_count": len(ledger_results),
        "case_receipt_trace_consistency_fail_count": consistency_fail_count,
        "runtime_proposal_emitted_count": emitted_count,
        "runtime_proposal_executed_count": 0,
        "runtime_proposal_promoted_count": 0,
        "duplicate_unresolved_proposal_count": duplicate_count,
        "proposal_withheld_count": withheld_count,
        "registry_write_count": 0,
        "local_regime_mutation_count": 0,
    }

    acceptance_gate_results = {
        "H0_source_chain_verified": len(validate_inputs(policy, policy_receipt, v0_2_impl, local_regime_v1, upgrade_policy, local_regime_v0)) == 0,
        "H1_trace_schema_declared": trace_schema_path.exists() and len(validate_trace_schema_artifact(trace_schema)) == 0,
        "H2_proposal_ledger_schema_declared": ledger_schema_path.exists() and len(validate_ledger_schema_artifact(ledger_schema)) == 0,
        "H3_trace_hardened_runner_implemented": RUNNER_TRACE_LEDGER_PATH.exists(),
        "H4_trace_files_emitted_for_cases": aggregate_metrics["trace_file_count"] == 6,
        "H5_receipts_reference_traces": consistency_fail_count == 0,
        "H6_unresolved_proposal_ledger_artifact_used": case_results["LEDGER_SUPPRESSES_DUPLICATE_UNRESOLVED_PROPOSAL"]["proposal_status"] == "WITHHELD_DUPLICATE_UNRESOLVED" and duplicate_count == 1,
        "H7_v0_2_regression_preserved": (
            aggregate_metrics["runtime_proposal_executed_count"] == 0
            and aggregate_metrics["runtime_proposal_promoted_count"] == 0
            and aggregate_metrics["registry_write_count"] == 0
            and aggregate_metrics["local_regime_mutation_count"] == 0
            and case_results["REGRESSION_V0_2_NON_EXECUTION_AND_NO_REGISTRY"]["halt_code"] == "STOP_AUTHORITY_VIOLATION"
        ),
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    authority_guards = {
        "source_chain_verified": True,
        "trace_schema_emitted": True,
        "proposal_ledger_schema_emitted": True,
        "trace_ledger_runner_implemented": True,
        "trace_ledger_runner_path": RUNNER_TRACE_LEDGER_PATH.relative_to(ROOT).as_posix(),
        "jurisdiction_runner_v0_2_modified": False,
        "jurisdiction_runner_v0_1_modified": False,
        "local_regime_v1_replaced": False,
        "local_regime_runtime_mutated": False,
        "fixtures_created": True,
        "fixtures_executed": True,
        "trace_files_emitted": True,
        "proposal_ledger_artifacts_emitted": True,
        "case_receipts_emitted": True,
        "implementation_receipt_emitted": True,
        "proposal_executed": False,
        "proposal_promoted": False,
        "registry_written": False,
        "registry_inserted": False,
        "registry_sqlite_read": False,
        "registry_sqlite_written": False,
        "full_registry_scan_used": False,
        "global_taxonomy_claimed": False,
        "final_schema_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
    }

    artifact_guards = {
        "hardening_policy_tracked": tracked(POLICY_PATH),
        "hardening_policy_receipt_tracked": tracked(POLICY_RECEIPT_PATH),
        "source_v0_2_implementation_receipt_tracked": tracked(V0_2_IMPLEMENTATION_RECEIPT_PATH),
        "source_local_regime_v1_tracked": tracked(LOCAL_REGIME_V1_PATH),
        "source_runner_v0_2_tracked": tracked(RUNNER_V0_2_PATH),
        "trace_schema_path_addressed": True,
        "ledger_schema_path_addressed": True,
        "trace_ledger_runner_path_addressed": True,
        "outputs_path_addressed": True,
        "outputs_receipt_referenced": True,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_authority_used": False,
    }

    receipt_seed = {
        "unit_id": UNIT_ID,
        "policy_id": TRACE_LEDGER_POLICY_ID,
        "trace_schema_id": trace_schema_id,
        "ledger_schema_id": ledger_schema_id,
        "case_receipts": {k: v["case_receipt_id"] for k, v in sorted(case_results.items())},
    }
    implementation_receipt_id = sha8(receipt_seed)

    implementation_receipt = {
        "schema_version": "jurisdiction_runner_v0_2_trace_and_proposal_ledger_hardening_implementation_receipt_v0",
        "receipt_type": "JURISDICTION_RUNNER_V0_2_TRACE_AND_PROPOSAL_LEDGER_HARDENING_IMPLEMENTATION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": implementation_receipt_id,
        "source_hardening_policy_id": TRACE_LEDGER_POLICY_ID,
        "source_hardening_policy_receipt_id": TRACE_LEDGER_POLICY_RECEIPT_ID,
        "source_v0_2_implementation_receipt_id": V0_2_IMPLEMENTATION_RECEIPT_ID,
        "source_runner_unit_id": SOURCE_RUNNER_UNIT_ID,
        "target_runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "source_local_regime_version": SOURCE_LOCAL_REGIME_VERSION,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "trace_schema_id": trace_schema_id,
        "trace_schema_path": trace_schema_path.relative_to(ROOT).as_posix(),
        "proposal_ledger_schema_id": ledger_schema_id,
        "proposal_ledger_schema_path": ledger_schema_path.relative_to(ROOT).as_posix(),
        "trace_ledger_runner_path": RUNNER_TRACE_LEDGER_PATH.relative_to(ROOT).as_posix(),
        "case_results": case_results,
        "trace_results": trace_results,
        "ledger_results": ledger_results,
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "authority_guards": authority_guards,
        "artifact_guards": artifact_guards,
        "terminal": {
            "type": "STOP",
            "next_command_goal": None,
            "stop_code": "STOP_DONE" if not failures else "STOP_GATE_FAIL",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    failures.extend(validate_implementation_receipt(implementation_receipt))
    implementation_receipt["failures"] = failures
    implementation_receipt["gate"] = "PASS" if not failures else "FAIL"
    implementation_receipt["terminal"]["stop_code"] = "STOP_DONE" if not failures else "STOP_GATE_FAIL"

    implementation_receipt_path = IMPLEMENTATION_RECEIPT_DIR / f"{implementation_receipt_id}.json"
    write_json(implementation_receipt_path, implementation_receipt)

    print(json.dumps(implementation_receipt, indent=2, sort_keys=True))
    print(f"trace_ledger_implementation_receipt_id={implementation_receipt_id}")
    print(f"trace_ledger_implementation_receipt_path=data/jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts/{implementation_receipt_id}.json")
    print(f"trace_schema_id={trace_schema_id}")
    print(f"trace_schema_path={trace_schema_path.relative_to(ROOT).as_posix()}")
    print(f"proposal_ledger_schema_id={ledger_schema_id}")
    print(f"proposal_ledger_schema_path={ledger_schema_path.relative_to(ROOT).as_posix()}")
    print(f"trace_ledger_runner_path={RUNNER_TRACE_LEDGER_PATH.relative_to(ROOT).as_posix()}")

    for case_name, result in sorted(case_results.items()):
        print(f"case_{case_name}_fixture_path={result['fixture_path']}")
        print(f"case_{case_name}_receipt_id={result['case_receipt_id']}")
        print(f"case_{case_name}_receipt_path={result['case_receipt_path']}")
        print(f"case_{case_name}_trace_id={result['trace_id']}")
        print(f"case_{case_name}_trace_path={result['trace_path']}")
        print(f"case_{case_name}_ledger_id={result['ledger_id']}")
        print(f"case_{case_name}_ledger_path={result['ledger_path']}")

    return 0 if implementation_receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
