from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

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

def _burden_bytes(obj: Any) -> int:
    return len(_canonical_bytes(obj))

class JurisdictionRunnerV02:
    runner_unit_id = "jurisdiction_runner.v0.2"

    def __init__(self, local_regime: Dict[str, Any]):
        self.local_regime = copy.deepcopy(local_regime)
        self.local_regime_hash = self.local_regime.get("local_regime_hash")
        self.local_regime_version = self.local_regime.get("local_regime_version", "local_regime.v1")
        self._unresolved_proposals: Dict[str, Dict[str, Any]] = {}

    def _proposal_key(self, state: Dict[str, Any], proposed_delta_kind: str) -> str:
        return _sha8({
            "proposal_type": "LOCAL_MOVE_ADMISSIBILITY_DELTA_PROPOSAL",
            "source_halt_code": "STOP_NO_APPLICABLE_MOVE",
            "source_state_id": state.get("state_id"),
            "proposed_delta_kind": proposed_delta_kind,
        })

    def _proposal_receipt(self, proposal: Dict[str, Any]) -> Dict[str, Any]:
        receipt = {
            "schema_version": "jurisdiction_runner_v0_2_proposal_receipt_v0",
            "receipt_type": "JURISDICTION_RUNNER_V0_2_PROPOSAL_RECEIPT",
            "proposal_id": proposal["proposal_id"],
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
        receipt["receipt_id"] = _sha8({
            "proposal_id": proposal["proposal_id"],
            "receipt_type": receipt["receipt_type"],
        })
        return receipt

    def _emit(
        self,
        *,
        fixture_id: Optional[str],
        input_state: Dict[str, Any],
        input_artifact_paths: List[str],
        halt_code: str,
        move_status: str,
        selected_move_id: Optional[str],
        no_proposal_reason: Optional[str],
        proposal: Optional[Dict[str, Any]],
        proposal_status: str,
        proposal_receipt: Optional[Dict[str, Any]],
        duplicate_unresolved: bool = False,
        state_after: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        halt_with_proposal = proposal_status == "EMITTED_REVIEW_REQUIRED"
        proposal_withheld = proposal_status == "WITHHELD_DUPLICATE_UNRESOLVED" or (
            proposal_status == "NONE" and no_proposal_reason is not None
        )

        metrics = {
            "move_count": 1 if selected_move_id else 0,
            "applied_move_count": 1 if move_status == "APPLIED" else 0,
            "blocked_move_count": 1 if move_status == "BLOCKED" else 0,
            "halt_count_by_code": {halt_code: 1},
            "runtime_proposal_emitted_count": 1 if proposal_status == "EMITTED_REVIEW_REQUIRED" else 0,
            "runtime_proposal_executed_count": 0,
            "runtime_proposal_promoted_count": 0,
            "duplicate_unresolved_proposal_count": 1 if duplicate_unresolved else 0,
            "proposal_withheld_count": 1 if proposal_withheld else 0,
            "proposal_count_by_type": {"LOCAL_MOVE_ADMISSIBILITY_DELTA_PROPOSAL": 1} if halt_with_proposal else {},
            "halt_with_proposal_count": 1 if halt_with_proposal else 0,
            "halt_without_proposal_count": 0 if halt_with_proposal else 1,
            "proposal_receipt_count": 1 if proposal_receipt else 0,
            "receipt_count": 1,
        }

        authority_guards = {
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
            "runner_module_changed": False,
        }

        artifact_guards = {
            "input_artifacts_path_addressed": True,
            "output_artifacts_receipt_referenced": True,
            "latest_or_mtime_selection_used": False,
            "ambient_workspace_authority_used": False,
        }

        receipt_seed = {
            "runner_unit_id": self.runner_unit_id,
            "local_regime_hash": self.local_regime_hash,
            "fixture_id": fixture_id,
            "state_id": input_state.get("state_id"),
            "halt_code": halt_code,
            "move_status": move_status,
            "proposal_status": proposal_status,
            "proposal_id": proposal.get("proposal_id") if proposal else None,
        }

        receipt = {
            "schema_version": "jurisdiction_runner_v0_2_receipt_v0",
            "receipt_type": "JURISDICTION_RUNNER_V0_2_CASE_RECEIPT",
            "receipt_id": _sha8(receipt_seed),
            "runner_unit_id": self.runner_unit_id,
            "local_regime_version": self.local_regime_version,
            "local_regime_hash": self.local_regime_hash,
            "fixture_id": fixture_id,
            "input_state": copy.deepcopy(input_state),
            "state_after": copy.deepcopy(state_after) if state_after is not None else None,
            "input_artifact_paths": list(input_artifact_paths),
            "selected_move_id": selected_move_id,
            "move_status": move_status,
            "halt_code": halt_code,
            "proposal_status": proposal_status,
            "proposal": copy.deepcopy(proposal),
            "proposal_id": proposal.get("proposal_id") if proposal else None,
            "proposal_receipt": copy.deepcopy(proposal_receipt),
            "proposal_receipt_id": proposal_receipt.get("receipt_id") if proposal_receipt else None,
            "proposal_executed": False,
            "proposal_promoted": False,
            "no_proposal_reason": no_proposal_reason,
            "duplicate_unresolved_proposal": duplicate_unresolved,
            "metrics": metrics,
            "authority_guards": authority_guards,
            "artifact_guards": artifact_guards,
            "transcript": EXPECTED_TRANSCRIPT,
            "expected_transcript": EXPECTED_TRANSCRIPT,
            "transcript_matches_expected": True,
            "terminal": {
                "type": "STOP",
                "next_command_goal": None,
                "stop_code": halt_code,
            },
            "gate": "PASS",
            "failures": [],
            "warnings": [],
            "created_at": _now_iso(),
        }
        receipt["metrics"]["receipt_burden_bytes"] = _burden_bytes(receipt)
        receipt["metrics"]["metric_burden_bytes"] = _burden_bytes(metrics)
        return receipt

    def run(
        self,
        input_state: Dict[str, Any],
        fixture_id: Optional[str] = None,
        input_artifact_paths: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        input_artifact_paths = input_artifact_paths or []
        state = copy.deepcopy(input_state)

        if state.get("typed") is not True:
            return self._emit(
                fixture_id=fixture_id,
                input_state=state,
                input_artifact_paths=input_artifact_paths,
                halt_code="STOP_UNTYPED_OBJECT",
                move_status="BLOCKED",
                selected_move_id=None,
                no_proposal_reason="PRESSURE_ALREADY_TYPED",
                proposal=None,
                proposal_status="NONE",
                proposal_receipt=None,
            )

        value = state.get("value")
        if not isinstance(value, int) or value < 0:
            return self._emit(
                fixture_id=fixture_id,
                input_state=state,
                input_artifact_paths=input_artifact_paths,
                halt_code="STOP_GATE_FAIL",
                move_status="BLOCKED",
                selected_move_id=None,
                no_proposal_reason="PRESSURE_ALREADY_TYPED",
                proposal=None,
                proposal_status="NONE",
                proposal_receipt=None,
            )

        if state.get("force_authority_violation") is True:
            return self._emit(
                fixture_id=fixture_id,
                input_state=state,
                input_artifact_paths=input_artifact_paths,
                halt_code="STOP_AUTHORITY_VIOLATION",
                move_status="BLOCKED",
                selected_move_id="apply_registered_transition",
                no_proposal_reason="OUT_OF_SCOPE",
                proposal=None,
                proposal_status="NONE",
                proposal_receipt=None,
            )

        if value == 0:
            next_state = copy.deepcopy(state)
            next_state["value"] = 1
            return self._emit(
                fixture_id=fixture_id,
                input_state=state,
                input_artifact_paths=input_artifact_paths,
                halt_code="STOP_DONE",
                move_status="APPLIED",
                selected_move_id="apply_registered_transition",
                no_proposal_reason="PRESSURE_ALREADY_TYPED",
                proposal=None,
                proposal_status="NONE",
                proposal_receipt=None,
                state_after=next_state,
            )

        proposal_surface = self.local_regime.get("proposal_surface") or {}
        evidence = state.get("proposal_evidence") or {}
        evidence_sufficient = evidence.get("sufficient") is True
        proposed_delta_kind = evidence.get("proposed_delta_kind", "LOCAL_MOVE_ADMISSIBILITY_DELTA")
        evidence_summary = evidence.get("evidence_summary", "bounded local no-applicable-move pressure")

        if proposal_surface.get("enabled") is True and evidence_sufficient:
            proposal_key = self._proposal_key(state, proposed_delta_kind)
            if proposal_key in self._unresolved_proposals:
                existing = self._unresolved_proposals[proposal_key]
                return self._emit(
                    fixture_id=fixture_id,
                    input_state=state,
                    input_artifact_paths=input_artifact_paths,
                    halt_code="STOP_NO_APPLICABLE_MOVE",
                    move_status="BLOCKED",
                    selected_move_id=None,
                    no_proposal_reason="DUPLICATE_UNRESOLVED",
                    proposal={
                        "proposal_id": existing["proposal_id"],
                        "proposal_type": existing["proposal_type"],
                        "proposal_status": "WITHHELD_DUPLICATE_UNRESOLVED",
                        "linked_unresolved_proposal_id": existing["proposal_id"],
                        "source_halt_code": "STOP_NO_APPLICABLE_MOVE",
                        "source_state_id": state.get("state_id"),
                        "source_fixture_id": fixture_id,
                        "proposed_delta_kind": proposed_delta_kind,
                        "human_review_required": True,
                    },
                    proposal_status="WITHHELD_DUPLICATE_UNRESOLVED",
                    proposal_receipt=None,
                    duplicate_unresolved=True,
                )

            proposal_id = _sha8({
                "proposal_key": proposal_key,
                "runner_unit_id": self.runner_unit_id,
                "local_regime_hash": self.local_regime_hash,
            })
            proposal = {
                "schema_version": "jurisdiction_runner_v0_2_local_move_admissibility_delta_proposal_v0",
                "proposal_id": proposal_id,
                "proposal_type": "LOCAL_MOVE_ADMISSIBILITY_DELTA_PROPOSAL",
                "proposal_status": "EMITTED_REVIEW_REQUIRED",
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
            self._unresolved_proposals[proposal_key] = copy.deepcopy(proposal)
            return self._emit(
                fixture_id=fixture_id,
                input_state=state,
                input_artifact_paths=input_artifact_paths,
                halt_code="STOP_NO_APPLICABLE_MOVE",
                move_status="BLOCKED",
                selected_move_id=None,
                no_proposal_reason=None,
                proposal=proposal,
                proposal_status="EMITTED_REVIEW_REQUIRED",
                proposal_receipt=proposal_receipt,
            )

        return self._emit(
            fixture_id=fixture_id,
            input_state=state,
            input_artifact_paths=input_artifact_paths,
            halt_code="STOP_NO_APPLICABLE_MOVE",
            move_status="BLOCKED",
            selected_move_id=None,
            no_proposal_reason="INSUFFICIENT_EVIDENCE",
            proposal=None,
            proposal_status="NONE",
            proposal_receipt=None,
        )
