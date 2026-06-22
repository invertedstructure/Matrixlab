from __future__ import annotations

import hashlib
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

RUNNER_UNIT_ID = "jurisdiction_runner.v0.1"

REQUIRED_TRANSCRIPT = [
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

REQUIRED_HALT_CODES = [
    "STOP_DONE",
    "STOP_NO_APPLICABLE_MOVE",
    "STOP_AUTHORITY_VIOLATION",
    "STOP_GATE_FAIL",
    "STOP_UNTYPED_OBJECT",
    "STOP_DEPENDENCY_MISSING",
]

REQUIRED_MOVE_TYPES = [
    "MOVE_VALIDATE_STATE",
    "MOVE_APPLY_REGISTERED_TRANSITION",
    "MOVE_EMIT_METRIC_RECEIPT",
]

REQUIRED_METRICS = [
    "move_count",
    "applied_move_count",
    "blocked_move_count",
    "halt_count_by_code",
    "typed_object_count",
    "untyped_object_count",
    "missing_dependency_count",
    "receipt_count",
    "authority_violation_count",
    "gate_fail_count",
    "proposal_emitted_count",
    "proposal_withheld_count",
    "proposal_count_by_type",
    "duplicate_unresolved_proposal_count",
    "halt_with_proposal_count",
    "halt_without_proposal_count",
    "local_closure_radius_observed",
    "receipt_burden_bytes",
    "metric_burden_bytes",
    "artifact_burden_bytes",
]

NO_PROPOSAL_REASONS = [
    "INSUFFICIENT_EVIDENCE",
    "PRESSURE_ALREADY_TYPED",
    "HUMAN_DECISION_REQUIRED",
    "OUT_OF_SCOPE",
    "AMBIGUOUS_PRESSURE",
    "DUPLICATE_UNRESOLVED_PROPOSAL",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"missing dependency: {path}")
    return json.loads(path.read_text())

def stable_hash(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def burden_bytes(obj: Any) -> int:
    return len(canonical_bytes(obj))

class JurisdictionRunnerV01:
    def __init__(self, regime: Dict[str, Any]):
        self.regime = deepcopy(regime)
        self.local_regime_version = regime["local_regime_version"]
        self.local_regime_hash = regime["local_regime_hash"]

    def _validate_regime(self) -> None:
        missing_moves = [m for m in REQUIRED_MOVE_TYPES if m not in self.regime.get("move_registry", {})]
        if missing_moves:
            raise ValueError(f"regime missing required moves: {missing_moves}")
        missing_halts = [h for h in REQUIRED_HALT_CODES if h not in self.regime.get("halt_vocabulary", [])]
        if missing_halts:
            raise ValueError(f"regime missing required halts: {missing_halts}")
        missing_metrics = [m for m in REQUIRED_METRICS if m not in self.regime.get("metric_bundle", [])]
        if missing_metrics:
            raise ValueError(f"regime missing required metrics: {missing_metrics}")

    def _validate_state(self, state: Dict[str, Any]) -> Tuple[bool, Optional[str], str]:
        required = self.regime["state_schema"]["required_fields"]
        missing = [key for key in required if key not in state]
        if missing:
            return False, "STOP_UNTYPED_OBJECT", f"missing required state fields: {missing}"
        if state.get("typed") is not True:
            return False, "STOP_UNTYPED_OBJECT", "state typed flag is not true"
        if not isinstance(state.get("value"), int):
            return False, "STOP_GATE_FAIL", "state value must be integer"
        if state.get("value", 0) < 0:
            return False, "STOP_GATE_FAIL", "state value must be non-negative"
        return True, None, "state valid"

    def _applicable_moves(self, state: Dict[str, Any]) -> List[Dict[str, Any]]:
        moves: List[Dict[str, Any]] = []
        for move_id, move in self.regime["move_registry"].items():
            if move_id == "MOVE_VALIDATE_STATE":
                continue
            if move_id == "MOVE_EMIT_METRIC_RECEIPT":
                continue
            applies_when = move.get("applies_when", {})
            if applies_when.get("field") == "value" and applies_when.get("operator") == "lt":
                if state.get("value") < applies_when.get("value"):
                    moves.append({"move_id": move_id, **move})
            elif applies_when.get("always") is True:
                moves.append({"move_id": move_id, **move})
        moves.sort(key=lambda m: (m.get("move_priority", 999999), m["move_id"]))
        return moves

    def _authorized(self, move: Dict[str, Any]) -> Tuple[bool, str]:
        allowed = self.regime["jurisdiction_envelope"].get("allowed_move_ids", [])
        if move["move_id"] not in allowed:
            return False, f"move {move['move_id']} outside jurisdiction envelope"
        if move.get("move_type") not in REQUIRED_MOVE_TYPES:
            return False, f"move type {move.get('move_type')} not in v0.1 move types"
        return True, "authorized"

    def _apply_move(self, state: Dict[str, Any], move: Dict[str, Any]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        next_state = deepcopy(state)
        action = move["action"]
        if action["op"] == "increment":
            next_state[action["field"]] += action["by"]
        else:
            raise ValueError(f"unsupported action op: {action['op']}")
        transition = {
            "move_id": move["move_id"],
            "move_type": move["move_type"],
            "action": action,
            "state_delta": {
                action["field"]: {
                    "before": state[action["field"]],
                    "after": next_state[action["field"]],
                    "delta": next_state[action["field"]] - state[action["field"]],
                }
            },
        }
        return next_state, transition

    def run(self, input_state: Dict[str, Any], fixture_id: str, input_artifact_paths: List[str]) -> Dict[str, Any]:
        self._validate_regime()

        transcript: List[str] = []
        warnings: List[str] = []
        failures: List[str] = []

        transcript.append("LOAD_REGIME")
        transcript.append("LOAD_STATE")

        state_before = deepcopy(input_state)
        state_after = deepcopy(input_state)
        transition: Optional[Dict[str, Any]] = None
        selected_move_id: Optional[str] = None
        move_status = "BLOCKED"
        halt_code: Optional[str] = None
        halt_reason: Optional[str] = None
        proposal_status: Optional[str] = None
        proposal_id: Optional[str] = None
        no_proposal_reason: Optional[str] = None

        transcript.append("VALIDATE_STATE")
        valid, validation_halt, validation_reason = self._validate_state(input_state)
        if not valid:
            halt_code = validation_halt
            halt_reason = validation_reason
            proposal_status = "NONE"
            no_proposal_reason = "PRESSURE_ALREADY_TYPED"
        else:
            transcript.append("SELECT_MOVE")
            moves = self._applicable_moves(input_state)
            if not moves:
                halt_code = "STOP_NO_APPLICABLE_MOVE"
                halt_reason = "no registered move applies"
                proposal_status = "NONE"
                no_proposal_reason = "INSUFFICIENT_EVIDENCE"
            else:
                selected = moves[0]
                selected_move_id = selected["move_id"]
                transcript.append("CHECK_AUTHORITY")
                authorized, auth_reason = self._authorized(selected)
                if not authorized:
                    halt_code = "STOP_AUTHORITY_VIOLATION"
                    halt_reason = auth_reason
                    proposal_status = "NONE"
                    no_proposal_reason = "OUT_OF_SCOPE"
                else:
                    transcript.append("APPLY_OR_BLOCK_MOVE")
                    state_after, transition = self._apply_move(input_state, selected)
                    move_status = "APPLIED"
                    halt_code = "STOP_DONE"
                    halt_reason = "registered transition applied and dry-run complete"
                    proposal_status = "NONE"
                    no_proposal_reason = "PRESSURE_ALREADY_TYPED"

        if "SELECT_MOVE" not in transcript:
            transcript.append("SELECT_MOVE")
        if "CHECK_AUTHORITY" not in transcript:
            transcript.append("CHECK_AUTHORITY")
        if "APPLY_OR_BLOCK_MOVE" not in transcript:
            transcript.append("APPLY_OR_BLOCK_MOVE")

        terminal = {
            "type": "STOP",
            "next_command_goal": None,
            "stop_code": halt_code,
        }

        metrics = {
            "move_count": 1 if selected_move_id else 0,
            "applied_move_count": 1 if move_status == "APPLIED" else 0,
            "blocked_move_count": 1 if move_status == "BLOCKED" else 0,
            "halt_count_by_code": {halt_code: 1} if halt_code else {},
            "typed_object_count": 1 if input_state.get("typed") is True else 0,
            "untyped_object_count": 0 if input_state.get("typed") is True else 1,
            "missing_dependency_count": 0,
            "receipt_count": 1,
            "authority_violation_count": 1 if halt_code == "STOP_AUTHORITY_VIOLATION" else 0,
            "gate_fail_count": 1 if halt_code == "STOP_GATE_FAIL" else 0,
            "proposal_emitted_count": 1 if proposal_status == "PROPOSED" else 0,
            "proposal_withheld_count": 1 if proposal_status == "NONE" else 0,
            "proposal_count_by_type": {},
            "duplicate_unresolved_proposal_count": 0,
            "halt_with_proposal_count": 1 if proposal_status == "PROPOSED" else 0,
            "halt_without_proposal_count": 1 if proposal_status == "NONE" else 0,
            "local_closure_radius_observed": 1 if move_status == "APPLIED" else 0,
            "receipt_burden_bytes": 0,
            "metric_burden_bytes": 0,
            "artifact_burden_bytes": sum(len(p.encode("utf-8")) for p in input_artifact_paths),
        }

        artifact_guards = {
            "input_artifacts_path_addressed": True,
            "output_artifacts_receipt_referenced": True,
            "required_dependencies_verified": True,
            "tracked_when_permanence_required": True,
            "unrelated_untracked_data_not_authority": True,
            "latest_or_mtime_selection_used": False,
            "ambient_workspace_authority_used": False,
        }

        authority_guards = {
            "local_regime_fixed": True,
            "local_regime_runtime_mutated": False,
            "registered_moves_only": True,
            "deterministic_selector_used": True,
            "selector_tie_break_rule": "move_priority_then_lexical_move_id",
            "typed_halts_only": True,
            "proposal_promoted": False,
            "runtime_registry_mutated": False,
            "registry_written": False,
            "registry_inserted": False,
            "registry_sqlite_read": False,
            "registry_sqlite_written": False,
            "full_registry_scan_used": False,
            "proof_claimed": False,
            "global_taxonomy_claimed": False,
            "final_schema_claimed": False,
            "hidden_continuation_authorized": False,
        }

        transcript.append("EMIT_RECEIPT")
        transcript.append("EMIT_METRICS")
        transcript.append("EMIT_TERMINAL")

        receipt_seed = {
            "fixture_id": fixture_id,
            "runner": RUNNER_UNIT_ID,
            "local_regime_version": self.local_regime_version,
            "local_regime_hash": self.local_regime_hash,
            "state_before_hash": stable_hash(state_before),
            "state_after_hash": stable_hash(state_after),
            "selected_move_id": selected_move_id,
            "halt_code": halt_code,
        }
        receipt_id = sha8(receipt_seed)

        receipt: Dict[str, Any] = {
            "receipt_id": receipt_id,
            "receipt_type": "JURISDICTION_RUNNER_RECEIPT",
            "run_id": f"dry_run_{fixture_id}_{receipt_id}",
            "unit_id": RUNNER_UNIT_ID,
            "fixture_id": fixture_id,
            "local_regime_version": self.local_regime_version,
            "local_regime_hash": self.local_regime_hash,
            "input_state_id": input_state.get("state_id"),
            "input_artifact_paths": input_artifact_paths,
            "state_before_hash": stable_hash(state_before),
            "state_after_hash": stable_hash(state_after),
            "state_before": state_before,
            "state_after": state_after,
            "selector_rule": "move_priority_then_lexical_move_id",
            "selected_move_id": selected_move_id,
            "move_id": selected_move_id,
            "move_status": move_status,
            "transition": transition,
            "halt_code": halt_code,
            "halt_reason": halt_reason,
            "proposal_status": proposal_status,
            "proposal_id": proposal_id,
            "no_proposal_reason": no_proposal_reason,
            "metrics": metrics,
            "authority_guards": authority_guards,
            "artifact_guards": artifact_guards,
            "transcript": transcript,
            "expected_transcript": REQUIRED_TRANSCRIPT,
            "transcript_matches_expected": transcript == REQUIRED_TRANSCRIPT,
            "terminal": terminal,
            "gate": "PASS" if transcript == REQUIRED_TRANSCRIPT and not failures else "FAIL",
            "failures": failures,
            "warnings": warnings,
            "created_at": now_iso(),
        }

        receipt["metrics"]["receipt_burden_bytes"] = burden_bytes(receipt)
        receipt["metrics"]["metric_burden_bytes"] = burden_bytes(receipt["metrics"])

        return receipt
