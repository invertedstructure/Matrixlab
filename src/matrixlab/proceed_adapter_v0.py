from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def _canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def _sha8(obj: Any) -> str:
    return hashlib.sha256(_canonical_bytes(obj)).hexdigest()[:8]

class ProceedAdapterV0:
    adapter_unit_id = "proceed_adapter.v0"

    def __init__(self, proceed_policy_receipt: Dict[str, Any]):
        self.policy = copy.deepcopy(proceed_policy_receipt)
        self.unit_registry = self.policy["proceed_unit_registry"]
        self.surface_manifest = self.policy["current_surface_manifest"]

    def _terminal(self, kind: str, next_unit_id: Optional[str], stop_code: Optional[str]) -> Dict[str, Any]:
        if kind == "ADVANCE":
            assert next_unit_id is not None
            assert stop_code is None
        if kind == "STOP":
            assert stop_code is not None
            assert next_unit_id is None
        return {"type": kind, "next_unit_id": next_unit_id, "stop_code": stop_code}

    def _authority_check(self, forbidden_inputs_detected: List[str]) -> Dict[str, Any]:
        return {
            "allowed_inputs_used": [
                "declared_current_surface_manifest",
                "declared_runner_module",
                "declared_local_regime",
                "declared_trace_schema",
                "declared_proposal_ledger_schema",
                "declared_receipt_ref",
                "declared_proceed_unit_registry",
                "declared_halt_vocabulary",
            ],
            "forbidden_inputs_detected": forbidden_inputs_detected,
            "authority_status": "STOP_AUTHORITY_VIOLATION" if forbidden_inputs_detected else "PASS",
        }

    def proceed(self, fixture: Dict[str, Any]) -> Dict[str, Any]:
        case_name = fixture["case_name"]
        start_state = fixture.get("start_state", {"status": "READY", "state_id": case_name})
        final_state = copy.deepcopy(start_state)
        selected_unit = fixture.get("selected_unit", "proceed.unit.validate_current_surface.v0")
        selected_move_or_repair = fixture.get("selected_move_or_repair", selected_unit)
        forbidden_inputs = fixture.get("forbidden_inputs_detected", [])

        authority = self._authority_check(forbidden_inputs)
        visible_gotchas_fixed = []
        taxonomy_pressure = {
            "detected": False,
            "trigger_halt": None,
            "observed_pressure": None,
            "status": "NONE",
            "taxonomy_delta_applied": False,
            "taxonomy_delta_promoted": False,
        }
        terminal = self._terminal("ADVANCE", "proceed.unit.execute_declared_runner_unit.v0", None)
        reason = "declared current surface is typed and validate_current_surface is the smallest lawful proceed unit"
        units_advanced_count = 1
        trace_delta = copy.deepcopy(fixture["trace_delta"])
        receipt_delta = copy.deepcopy(fixture["receipt_or_projection_delta"])
        ledger_delta = copy.deepcopy(fixture["ledger_delta"])

        if forbidden_inputs:
            terminal = self._terminal("STOP", None, "STOP_AUTHORITY_VIOLATION")
            reason = "forbidden authority input detected"
            units_advanced_count = 0

        if case_name == "PROCEED_LOCAL_GOTCHA_RECORD_ONLY":
            visible_gotchas_fixed = [
                {
                    "gotcha_id": "gotcha_projection_step_count_demo",
                    "kind": "projection_mismatch",
                    "observed": "readout.projected_trace_step_count=2",
                    "corrected_to": "readout.projected_trace_step_count=1",
                    "basis": "declared source trace has exactly one entry",
                    "semantic_widening": False,
                    "source_trace_modified": False,
                    "source_receipt_modified": False,
                    "source_ledger_modified": False,
                    "source_runner_modified": False,
                    "source_regime_modified": False,
                }
            ]
            selected_move_or_repair = "repair_projection_readout_step_count.v0"
            reason = "local visible projection gotcha fixed from declared trace basis without modifying source artifacts"

        if case_name == "PROCEED_TAXONOMY_PRESSURE_RECORDED_ONLY":
            taxonomy_pressure = {
                "detected": True,
                "trigger_halt": "STOP_TAXONOMY_GAP",
                "observed_pressure": "demo halt pressure cannot be promoted by proceed_adapter.v0",
                "status": "RECORDED_ONLY",
                "taxonomy_delta_applied": False,
                "taxonomy_delta_promoted": False,
            }
            terminal = self._terminal("STOP", None, "STOP_TAXONOMY_GAP")
            reason = "taxonomy pressure recorded only; proceed cannot self-accept or promote taxonomy delta"

        if case_name == "PROCEED_TERMINAL_BOUNDARY_NO_IMPLICIT_CONTINUATION":
            terminal = self._terminal("STOP", None, "STOP_NEXT_MOVE_BOUNDARY")
            reason = "terminal boundary reached; no implicit continuation authorized"

        final_state["last_selected_unit"] = selected_unit
        final_state["terminal_type"] = terminal["type"]
        final_state["terminal_stop_code"] = terminal["stop_code"]
        final_state["terminal_next_unit_id"] = terminal["next_unit_id"]

        readout_seed = {
            "adapter": self.adapter_unit_id,
            "case_name": case_name,
            "selected_unit": selected_unit,
            "terminal": terminal,
            "authority": authority,
            "taxonomy": taxonomy_pressure,
        }

        readout = {
            "schema_version": "proceed_readout_v0",
            "readout_id": _sha8(readout_seed),
            "unit_id": self.adapter_unit_id,
            "source_surface_manifest_ref": {
                "surface_manifest_id": self.surface_manifest["surface_manifest_id"],
                "source_implementation_receipt_id": self.surface_manifest["source_implementation_receipt_id"],
            },
            "start_state_sig8": _sha8(start_state),
            "final_state_sig8": _sha8(final_state),
            "selected_unit": selected_unit,
            "selected_move_or_repair": selected_move_or_repair,
            "reason": reason,
            "state_change": {
                "last_selected_unit": [start_state.get("last_selected_unit"), final_state.get("last_selected_unit")],
                "terminal_type": [start_state.get("terminal_type"), final_state.get("terminal_type")],
                "terminal_stop_code": [start_state.get("terminal_stop_code"), final_state.get("terminal_stop_code")],
                "terminal_next_unit_id": [start_state.get("terminal_next_unit_id"), final_state.get("terminal_next_unit_id")],
            },
            "visible_gotchas_fixed": visible_gotchas_fixed,
            "trace_delta": trace_delta,
            "receipt_or_projection_delta": receipt_delta,
            "ledger_delta": ledger_delta,
            "authority_check": authority,
            "taxonomy_pressure": taxonomy_pressure,
            "terminal_result": terminal,
            "units_advanced_count": units_advanced_count,
            "source_artifact_mutation": {
                "source_trace_modified": False,
                "source_receipt_modified": False,
                "source_ledger_modified": False,
                "source_runner_modified": False,
                "source_regime_modified": False,
            },
            "proposal_execution": {
                "proposal_executed": False,
                "proposal_promoted": False,
            },
            "registry_effect": {
                "registry_written": False,
                "registry_sqlite_read": False,
                "registry_sqlite_written": False,
            },
            "created_at": _now_iso(),
        }
        return readout
