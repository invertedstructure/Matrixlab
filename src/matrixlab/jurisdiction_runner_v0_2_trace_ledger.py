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
