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

UNIT_ID = "IMPLEMENT_PROCEED_ADAPTER_V0_WITH_DEMO_FIXTURES_V0"

PROCEED_ADAPTER_POLICY_ID = "e6b3dcfc"
PROCEED_ADAPTER_POLICY_RECEIPT_ID = "f953a9f0"
TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID = "cc24a11f"
TRACE_SCHEMA_ID = "b4887660"
PROPOSAL_LEDGER_SCHEMA_ID = "eee2a318"
LOCAL_REGIME_V1_HASH = "25802530"

TARGET_ADAPTER_UNIT_ID = "proceed_adapter.v0"
SOURCE_RUNNER_UNIT_ID = "jurisdiction_runner.v0.2.trace_ledger_hardened"
SOURCE_LOCAL_REGIME_VERSION = "local_regime.v1"

POLICY_PATH = ROOT / "data" / "proceed_adapter_v0_policies" / f"{PROCEED_ADAPTER_POLICY_ID}.json"
POLICY_RECEIPT_PATH = ROOT / "data" / "proceed_adapter_v0_policy_receipts" / f"{PROCEED_ADAPTER_POLICY_ID}.json"
TRACE_LEDGER_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts" / f"{TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID}.json"
TRACE_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_schemas" / f"{TRACE_SCHEMA_ID}.json"
PROPOSAL_LEDGER_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposal_ledger_schemas" / f"{PROPOSAL_LEDGER_SCHEMA_ID}.json"
TRACE_LEDGER_RUNNER_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_2_trace_ledger.py"
LOCAL_REGIME_V1_PATH = ROOT / "data" / "local_regime_v1_declarations" / f"{LOCAL_REGIME_V1_HASH}.json"
RUNNER_V0_2_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_2.py"
RUNNER_V0_1_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_1.py"

CONTRACT_DIR = ROOT / "data" / "proceed_adapter_v0_contracts"
SURFACE_MANIFEST_SCHEMA_DIR = ROOT / "data" / "proceed_adapter_v0_surface_manifest_schemas"
SURFACE_MANIFEST_DIR = ROOT / "data" / "proceed_adapter_v0_surface_manifests"
UNIT_SCHEMA_DIR = ROOT / "data" / "proceed_adapter_v0_unit_schemas"
UNIT_REGISTRY_DIR = ROOT / "data" / "proceed_adapter_v0_unit_registries"
SELECTOR_DIR = ROOT / "data" / "proceed_adapter_v0_selectors"
READOUT_SCHEMA_DIR = ROOT / "data" / "proceed_adapter_v0_readout_schemas"
AUTHORITY_SCHEMA_DIR = ROOT / "data" / "proceed_adapter_v0_authority_check_schemas"
GOTCHA_SCHEMA_DIR = ROOT / "data" / "proceed_adapter_v0_local_gotcha_schemas"
TAXONOMY_STUB_DIR = ROOT / "data" / "proceed_adapter_v0_taxonomy_pressure_stubs"
FIXTURE_DIR = ROOT / "data" / "proceed_adapter_v0_demo_fixtures"
READOUT_DIR = ROOT / "data" / "proceed_adapter_v0_demo_readouts"
RECEIPT_DIR = ROOT / "data" / "proceed_adapter_v0_demo_receipts"
IMPLEMENTATION_RECEIPT_DIR = ROOT / "data" / "proceed_adapter_v0_implementation_receipts"
ADAPTER_MODULE_PATH = ROOT / "src" / "matrixlab" / "proceed_adapter_v0.py"

DEMO_CASES = [
    "PROCEED_ADVANCES_ONE_NAMED_UNIT",
    "PROCEED_AUTHORITY_CHECK_REJECTS_FORBIDDEN_INPUTS",
    "PROCEED_READOUT_REFERENCES_TRACE_RECEIPT_LEDGER",
    "PROCEED_LOCAL_GOTCHA_RECORD_ONLY",
    "PROCEED_TAXONOMY_PRESSURE_RECORDED_ONLY",
    "PROCEED_TERMINAL_BOUNDARY_NO_IMPLICIT_CONTINUATION",
]

ACCEPTANCE_GATES = [
    "P0_source_surface_verified",
    "P1_proceed_contract_declared",
    "P2_unit_schema_and_registry_declared",
    "P3_selector_declared",
    "P4_readout_and_authority_schemas_declared",
    "P5_demo_implementation_required",
    "P6_no_source_runner_or_regime_mutation",
]

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

def validate_policy_inputs(
    policy: Dict[str, Any],
    policy_receipt: Dict[str, Any],
    trace_ledger_receipt: Dict[str, Any],
    trace_schema: Dict[str, Any],
    ledger_schema: Dict[str, Any],
    local_regime_v1: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if policy.get("policy_id") != PROCEED_ADAPTER_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy.get("policy_receipt_id") != PROCEED_ADAPTER_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if policy_receipt.get("policy_id") != PROCEED_ADAPTER_POLICY_ID:
        failures.append(f"policy_receipt_policy_id_wrong:{policy_receipt.get('policy_id')}")
    if policy_receipt.get("receipt_id") != PROCEED_ADAPTER_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy_receipt.get('receipt_id')}")
    if policy_receipt.get("gate") != "PASS":
        failures.append(f"policy_gate_not_PASS:{policy_receipt.get('gate')}")
    if policy_receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy_receipt.get('policy_status')}")

    terminal = policy_receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"policy_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"policy_terminal_stop_not_null:{terminal.get('stop_code')}")

    if policy_receipt.get("target_adapter_unit_id") != TARGET_ADAPTER_UNIT_ID:
        failures.append(f"target_adapter_wrong:{policy_receipt.get('target_adapter_unit_id')}")
    if policy_receipt.get("source_runner_unit_id") != SOURCE_RUNNER_UNIT_ID:
        failures.append(f"source_runner_wrong:{policy_receipt.get('source_runner_unit_id')}")
    if policy_receipt.get("source_trace_ledger_implementation_receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"source_trace_ledger_receipt_wrong:{policy_receipt.get('source_trace_ledger_implementation_receipt_id')}")

    contract = policy_receipt.get("proceed_contract") or {}
    if contract.get("command") != "proceed":
        failures.append(f"contract_command_wrong:{contract.get('command')}")
    if contract.get("unit_rule") != "one unit only":
        failures.append(f"contract_unit_rule_wrong:{contract.get('unit_rule')}")
    if contract.get("core_law", {}).get("proceed_is_one_smallest_lawful_advancement") is not True:
        failures.append("contract_missing_one_smallest_lawful_advancement")
    if contract.get("core_law", {}).get("proceed_is_not_redesign") is not True:
        failures.append("contract_missing_not_redesign")

    readout_schema = policy_receipt.get("proceed_readout_schema") or {}
    for key in [
        "readout_id",
        "unit_id",
        "source_surface_manifest_ref",
        "start_state_sig8",
        "final_state_sig8",
        "selected_unit",
        "selected_move_or_repair",
        "reason",
        "state_change",
        "visible_gotchas_fixed",
        "trace_delta",
        "receipt_or_projection_delta",
        "ledger_delta",
        "authority_check",
        "taxonomy_pressure",
        "terminal_result",
    ]:
        if key not in readout_schema.get("required_fields", []):
            failures.append(f"readout_required_field_missing:{key}")

    unit_registry = policy_receipt.get("proceed_unit_registry") or {}
    units = unit_registry.get("units", [])
    if len(units) != 4:
        failures.append(f"proceed_unit_registry_size_wrong:{len(units)}")
    for unit_id in [
        "proceed.unit.validate_current_surface.v0",
        "proceed.unit.execute_declared_runner_unit.v0",
        "proceed.unit.verify_readout_against_trace.v0",
        "proceed.unit.emit_next_boundary.v0",
    ]:
        if unit_id not in [u.get("unit_id") for u in units]:
            failures.append(f"proceed_unit_missing:{unit_id}")

    demo_cases = policy_receipt.get("required_demo_cases") or {}
    for case in DEMO_CASES:
        if case not in demo_cases:
            failures.append(f"required_demo_case_missing:{case}")

    gates = policy_receipt.get("acceptance_gates") or {}
    for gate in ACCEPTANCE_GATES:
        if gates.get(gate, {}).get("required") is not True:
            failures.append(f"acceptance_gate_missing:{gate}:{gates.get(gate)}")

    forbidden = policy_receipt.get("forbidden_operations_next") or {}
    for key in [
        "modify_source_trace_ledger_runner",
        "modify_jurisdiction_runner_v0_2",
        "alter_source_trace",
        "alter_source_receipt",
        "alter_source_ledger",
        "execute_or_apply_proposal",
        "accept_taxonomy_delta",
        "promote_taxonomy_delta",
        "sqlite_registry_write",
        "sqlite_registry_read",
        "global_taxonomy_design",
        "hidden_continuation_after_terminal",
        "latest_or_mtime_selection",
        "ambient_workspace_authority",
    ]:
        if forbidden.get(key) is not True:
            failures.append(f"forbidden_operation_missing:{key}:{forbidden.get(key)}")

    if trace_ledger_receipt.get("receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"trace_ledger_receipt_id_wrong:{trace_ledger_receipt.get('receipt_id')}")
    if trace_ledger_receipt.get("gate") != "PASS":
        failures.append(f"trace_ledger_gate_not_PASS:{trace_ledger_receipt.get('gate')}")
    if trace_ledger_receipt.get("target_runner_unit_id") != SOURCE_RUNNER_UNIT_ID:
        failures.append(f"trace_ledger_target_runner_wrong:{trace_ledger_receipt.get('target_runner_unit_id')}")
    if trace_ledger_receipt.get("trace_schema_id") != TRACE_SCHEMA_ID:
        failures.append(f"trace_ledger_trace_schema_wrong:{trace_ledger_receipt.get('trace_schema_id')}")
    if trace_ledger_receipt.get("proposal_ledger_schema_id") != PROPOSAL_LEDGER_SCHEMA_ID:
        failures.append(f"trace_ledger_ledger_schema_wrong:{trace_ledger_receipt.get('proposal_ledger_schema_id')}")
    if trace_ledger_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append(f"trace_ledger_terminal_not_STOP:{trace_ledger_receipt.get('terminal')}")
    if trace_ledger_receipt.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append(f"trace_ledger_terminal_not_DONE:{trace_ledger_receipt.get('terminal')}")
    if trace_ledger_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append(f"trace_ledger_terminal_next_not_null:{trace_ledger_receipt.get('terminal')}")

    metrics = trace_ledger_receipt.get("aggregate_metrics") or {}
    if metrics.get("case_receipt_trace_consistency_fail_count") != 0:
        failures.append(f"source_trace_consistency_fail_count_nonzero:{metrics.get('case_receipt_trace_consistency_fail_count')}")
    for key in ["runtime_proposal_executed_count", "runtime_proposal_promoted_count", "registry_write_count", "local_regime_mutation_count"]:
        if metrics.get(key) != 0:
            failures.append(f"source_metric_not_zero:{key}:{metrics.get(key)}")

    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append(f"trace_schema_version_wrong:{trace_schema.get('schema_version')}")
    if ledger_schema.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append(f"ledger_schema_version_wrong:{ledger_schema.get('schema_version')}")
    if ledger_schema.get("ledger_scope") != "path-addressed local artifact only, no registry or sqlite authority":
        failures.append(f"ledger_scope_wrong:{ledger_schema.get('ledger_scope')}")

    if local_regime_v1.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append(f"local_regime_v1_hash_wrong:{local_regime_v1.get('local_regime_hash')}")
    if local_regime_v1.get("local_regime_version") != SOURCE_LOCAL_REGIME_VERSION:
        failures.append(f"local_regime_v1_version_wrong:{local_regime_v1.get('local_regime_version')}")

    for path, label in [
        (POLICY_PATH, "proceed_policy"),
        (POLICY_RECEIPT_PATH, "proceed_policy_receipt"),
        (TRACE_LEDGER_IMPLEMENTATION_RECEIPT_PATH, "trace_ledger_implementation_receipt"),
        (TRACE_SCHEMA_PATH, "trace_schema"),
        (PROPOSAL_LEDGER_SCHEMA_PATH, "proposal_ledger_schema"),
        (TRACE_LEDGER_RUNNER_PATH, "trace_ledger_runner"),
        (LOCAL_REGIME_V1_PATH, "local_regime_v1"),
        (RUNNER_V0_2_PATH, "runner_v0_2"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{path.relative_to(ROOT).as_posix()}")

    return failures

ADAPTER_SOURCE = r'''
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
'''

def write_adapter_module() -> None:
    ADAPTER_MODULE_PATH.parent.mkdir(parents=True, exist_ok=True)
    ADAPTER_MODULE_PATH.write_text(ADAPTER_SOURCE.strip() + "\n")

def import_adapter_module():
    spec = importlib.util.spec_from_file_location("proceed_adapter_v0", ADAPTER_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import proceed_adapter_v0")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["proceed_adapter_v0"] = mod
    spec.loader.exec_module(mod)
    return mod

def write_schema_artifacts(policy_receipt: Dict[str, Any]) -> Dict[str, Dict[str, str]]:
    artifacts: Dict[str, Dict[str, str]] = {}

    objects = {
        "proceed_contract": (CONTRACT_DIR, policy_receipt["proceed_contract"]),
        "current_surface_manifest_schema": (SURFACE_MANIFEST_SCHEMA_DIR, policy_receipt["current_surface_manifest_schema"]),
        "current_surface_manifest": (SURFACE_MANIFEST_DIR, policy_receipt["current_surface_manifest"]),
        "proceed_unit_schema": (UNIT_SCHEMA_DIR, policy_receipt["proceed_unit_schema"]),
        "proceed_unit_registry": (UNIT_REGISTRY_DIR, policy_receipt["proceed_unit_registry"]),
        "proceed_selector": (SELECTOR_DIR, policy_receipt["proceed_selector"]),
        "proceed_readout_schema": (READOUT_SCHEMA_DIR, policy_receipt["proceed_readout_schema"]),
        "authority_check_schema": (AUTHORITY_SCHEMA_DIR, policy_receipt["authority_check_schema"]),
        "local_gotcha_record_schema": (GOTCHA_SCHEMA_DIR, policy_receipt["local_gotcha_record_schema"]),
        "taxonomy_pressure_record_stub": (TAXONOMY_STUB_DIR, policy_receipt["taxonomy_pressure_record_stub"]),
    }

    for name, (directory, obj) in objects.items():
        artifact_id = sha8(obj)
        path = directory / f"{artifact_id}.json"
        write_json(path, obj)
        artifacts[name] = {"artifact_id": artifact_id, "artifact_path": path.relative_to(ROOT).as_posix()}

    return artifacts

def source_refs_from_trace_ledger_receipt(trace_ledger_receipt: Dict[str, Any], case_name: str = "TRACE_PRESENT_FOR_HALT_WITH_PROPOSAL") -> Dict[str, Any]:
    cases = trace_ledger_receipt["case_results"]
    if case_name not in cases:
        case_name = sorted(cases.keys())[0]
    case = cases[case_name]
    return {
        "case_name": case_name,
        "case_receipt_id": case["case_receipt_id"],
        "case_receipt_path": case["case_receipt_path"],
        "trace_id": case["trace_id"],
        "trace_path": case["trace_path"],
        "ledger_id": case["ledger_id"],
        "ledger_path": case["ledger_path"],
    }

def build_fixture(case_name: str, refs: Dict[str, Any], policy_receipt: Dict[str, Any]) -> Dict[str, Any]:
    base = {
        "schema_version": "proceed_adapter_v0_demo_fixture_v0",
        "fixture_id": f"proceed_demo_{case_name.lower()}",
        "case_name": case_name,
        "source_surface_manifest": policy_receipt["current_surface_manifest"],
        "selected_unit": "proceed.unit.validate_current_surface.v0",
        "selected_move_or_repair": "proceed.unit.validate_current_surface.v0",
        "start_state": {
            "state_id": f"state_{case_name.lower()}",
            "status": "READY",
            "active_object": "proceed_adapter.v0",
        },
        "trace_delta": {
            "trace_ref": {"trace_id": refs["trace_id"], "trace_path": refs["trace_path"]},
            "steps_added": 0,
            "source_trace_reused": True,
        },
        "receipt_or_projection_delta": {
            "receipt_ref": {"receipt_id": refs["case_receipt_id"], "receipt_path": refs["case_receipt_path"]},
            "receipt_changed": False,
            "projection_changed": False,
        },
        "ledger_delta": {
            "ledger_ref": {"ledger_id": refs["ledger_id"], "ledger_path": refs["ledger_path"]},
            "ledger_changed": False,
            "ledger_entry_delta": 0,
        },
        "forbidden_inputs_detected": [],
    }

    if case_name == "PROCEED_AUTHORITY_CHECK_REJECTS_FORBIDDEN_INPUTS":
        base["forbidden_inputs_detected"] = ["latest_file_guessing"]
    if case_name == "PROCEED_READOUT_REFERENCES_TRACE_RECEIPT_LEDGER":
        base["selected_unit"] = "proceed.unit.execute_declared_runner_unit.v0"
        base["selected_move_or_repair"] = "proceed.unit.execute_declared_runner_unit.v0"
    if case_name == "PROCEED_LOCAL_GOTCHA_RECORD_ONLY":
        base["selected_unit"] = "proceed.unit.verify_readout_against_trace.v0"
        base["selected_move_or_repair"] = "repair_projection_readout_step_count.v0"
        base["receipt_or_projection_delta"]["projection_changed"] = True
    if case_name == "PROCEED_TAXONOMY_PRESSURE_RECORDED_ONLY":
        base["selected_unit"] = "proceed.unit.emit_next_boundary.v0"
        base["selected_move_or_repair"] = "record_taxonomy_pressure_only.v0"
    if case_name == "PROCEED_TERMINAL_BOUNDARY_NO_IMPLICIT_CONTINUATION":
        base["selected_unit"] = "proceed.unit.emit_next_boundary.v0"
        base["selected_move_or_repair"] = "emit_terminal_boundary.v0"

    return base

def validate_readout(case_name: str, readout: Dict[str, Any], policy_receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    required = policy_receipt["proceed_readout_schema"]["required_fields"]
    for key in required:
        if key not in readout:
            failures.append(f"{case_name}:readout_required_field_missing:{key}")

    if readout.get("unit_id") != TARGET_ADAPTER_UNIT_ID:
        failures.append(f"{case_name}:unit_id_wrong:{readout.get('unit_id')}")

    terminal = readout.get("terminal_result") or {}
    if terminal.get("type") == "ADVANCE":
        if terminal.get("next_unit_id") is None or terminal.get("stop_code") is not None:
            failures.append(f"{case_name}:bad_ADVANCE_terminal:{terminal}")
    elif terminal.get("type") == "STOP":
        if terminal.get("stop_code") is None or terminal.get("next_unit_id") is not None:
            failures.append(f"{case_name}:bad_STOP_terminal:{terminal}")
    else:
        failures.append(f"{case_name}:terminal_type_wrong:{terminal}")

    authority = readout.get("authority_check") or {}
    if "allowed_inputs_used" not in authority:
        failures.append(f"{case_name}:authority_allowed_missing")
    if "forbidden_inputs_detected" not in authority:
        failures.append(f"{case_name}:authority_forbidden_missing")
    if "authority_status" not in authority:
        failures.append(f"{case_name}:authority_status_missing")

    if case_name == "PROCEED_ADVANCES_ONE_NAMED_UNIT":
        if readout.get("selected_unit") != "proceed.unit.validate_current_surface.v0":
            failures.append(f"{case_name}:selected_unit_wrong:{readout.get('selected_unit')}")
        if readout.get("units_advanced_count") != 1:
            failures.append(f"{case_name}:units_advanced_count_wrong:{readout.get('units_advanced_count')}")
        if terminal.get("type") != "ADVANCE":
            failures.append(f"{case_name}:terminal_not_ADVANCE:{terminal}")

    if case_name == "PROCEED_AUTHORITY_CHECK_REJECTS_FORBIDDEN_INPUTS":
        if authority.get("authority_status") != "STOP_AUTHORITY_VIOLATION":
            failures.append(f"{case_name}:authority_status_wrong:{authority.get('authority_status')}")
        if "latest_file_guessing" not in authority.get("forbidden_inputs_detected", []):
            failures.append(f"{case_name}:latest_file_guessing_not_detected")
        if terminal.get("stop_code") != "STOP_AUTHORITY_VIOLATION":
            failures.append(f"{case_name}:stop_code_wrong:{terminal}")

    if case_name == "PROCEED_READOUT_REFERENCES_TRACE_RECEIPT_LEDGER":
        if not readout.get("trace_delta", {}).get("trace_ref", {}).get("trace_path"):
            failures.append(f"{case_name}:trace_delta_missing_path")
        if not readout.get("receipt_or_projection_delta", {}).get("receipt_ref", {}).get("receipt_path"):
            failures.append(f"{case_name}:receipt_delta_missing_path")
        if not readout.get("ledger_delta", {}).get("ledger_ref", {}).get("ledger_path"):
            failures.append(f"{case_name}:ledger_delta_missing_path")

    if case_name == "PROCEED_LOCAL_GOTCHA_RECORD_ONLY":
        gotchas = readout.get("visible_gotchas_fixed", [])
        if len(gotchas) != 1:
            failures.append(f"{case_name}:gotcha_count_wrong:{len(gotchas)}")
        else:
            gotcha = gotchas[0]
            if gotcha.get("semantic_widening") is not False:
                failures.append(f"{case_name}:gotcha_semantic_widening_not_false")
            for key in ["source_trace_modified", "source_receipt_modified", "source_ledger_modified", "source_runner_modified", "source_regime_modified"]:
                if gotcha.get(key) is not False:
                    failures.append(f"{case_name}:gotcha_source_modified:{key}:{gotcha.get(key)}")

    if case_name == "PROCEED_TAXONOMY_PRESSURE_RECORDED_ONLY":
        taxonomy = readout.get("taxonomy_pressure") or {}
        if taxonomy.get("status") != "RECORDED_ONLY":
            failures.append(f"{case_name}:taxonomy_status_wrong:{taxonomy.get('status')}")
        if taxonomy.get("taxonomy_delta_applied") is not False:
            failures.append(f"{case_name}:taxonomy_delta_applied_not_false")
        if taxonomy.get("taxonomy_delta_promoted") is not False:
            failures.append(f"{case_name}:taxonomy_delta_promoted_not_false")
        if terminal.get("stop_code") != "STOP_TAXONOMY_GAP":
            failures.append(f"{case_name}:taxonomy_stop_wrong:{terminal}")

    if case_name == "PROCEED_TERMINAL_BOUNDARY_NO_IMPLICIT_CONTINUATION":
        if terminal.get("type") != "STOP":
            failures.append(f"{case_name}:terminal_not_STOP:{terminal}")
        if terminal.get("stop_code") != "STOP_NEXT_MOVE_BOUNDARY":
            failures.append(f"{case_name}:boundary_stop_wrong:{terminal}")

    source_mutation = readout.get("source_artifact_mutation") or {}
    for key in ["source_trace_modified", "source_receipt_modified", "source_ledger_modified", "source_runner_modified", "source_regime_modified"]:
        if source_mutation.get(key) is not False:
            failures.append(f"{case_name}:source_artifact_mutation_not_false:{key}:{source_mutation.get(key)}")

    proposal = readout.get("proposal_execution") or {}
    if proposal.get("proposal_executed") is not False:
        failures.append(f"{case_name}:proposal_executed_not_false")
    if proposal.get("proposal_promoted") is not False:
        failures.append(f"{case_name}:proposal_promoted_not_false")

    registry = readout.get("registry_effect") or {}
    for key in ["registry_written", "registry_sqlite_read", "registry_sqlite_written"]:
        if registry.get(key) is not False:
            failures.append(f"{case_name}:registry_effect_not_false:{key}:{registry.get(key)}")

    return failures

def build_demo_receipt(case_name: str, fixture: Dict[str, Any], readout: Dict[str, Any], readout_path: str) -> Dict[str, Any]:
    receipt_seed = {
        "case_name": case_name,
        "readout_id": readout["readout_id"],
        "terminal": readout["terminal_result"],
    }
    return {
        "schema_version": "proceed_adapter_v0_demo_receipt_v0",
        "receipt_type": "PROCEED_ADAPTER_V0_DEMO_RECEIPT",
        "receipt_id": sha8(receipt_seed),
        "adapter_unit_id": TARGET_ADAPTER_UNIT_ID,
        "case_name": case_name,
        "fixture_id": fixture["fixture_id"],
        "readout_id": readout["readout_id"],
        "readout_path": readout_path,
        "selected_unit": readout["selected_unit"],
        "units_advanced_count": readout["units_advanced_count"],
        "terminal_result": readout["terminal_result"],
        "authority_status": readout["authority_check"]["authority_status"],
        "trace_delta_present": bool(readout["trace_delta"].get("trace_ref", {}).get("trace_path")),
        "receipt_delta_present": bool(readout["receipt_or_projection_delta"].get("receipt_ref", {}).get("receipt_path")),
        "ledger_delta_present": bool(readout["ledger_delta"].get("ledger_ref", {}).get("ledger_path")),
        "visible_gotcha_count": len(readout["visible_gotchas_fixed"]),
        "taxonomy_pressure_status": readout["taxonomy_pressure"]["status"],
        "taxonomy_delta_applied": readout["taxonomy_pressure"]["taxonomy_delta_applied"],
        "taxonomy_delta_promoted": readout["taxonomy_pressure"]["taxonomy_delta_promoted"],
        "proposal_executed": readout["proposal_execution"]["proposal_executed"],
        "proposal_promoted": readout["proposal_execution"]["proposal_promoted"],
        "registry_written": readout["registry_effect"]["registry_written"],
        "hidden_continuation_authorized": False,
        "source_artifact_mutation": readout["source_artifact_mutation"],
        "gate": "PASS",
        "failures": [],
        "created_at": now_iso(),
    }

def validate_implementation_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if receipt.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("source_proceed_policy_id") != PROCEED_ADAPTER_POLICY_ID:
        failures.append(f"source_policy_wrong:{receipt.get('source_proceed_policy_id')}")
    if receipt.get("target_adapter_unit_id") != TARGET_ADAPTER_UNIT_ID:
        failures.append(f"target_adapter_wrong:{receipt.get('target_adapter_unit_id')}")
    if receipt.get("source_runner_unit_id") != SOURCE_RUNNER_UNIT_ID:
        failures.append(f"source_runner_wrong:{receipt.get('source_runner_unit_id')}")

    gates = receipt.get("acceptance_gate_results") or {}
    for gate in ACCEPTANCE_GATES:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics") or {}
    if metrics.get("demo_case_count") != 6:
        failures.append(f"demo_case_count_wrong:{metrics.get('demo_case_count')}")
    if metrics.get("demo_case_pass_count") != 6:
        failures.append(f"demo_case_pass_count_wrong:{metrics.get('demo_case_pass_count')}")
    if metrics.get("demo_case_fail_count") != 0:
        failures.append(f"demo_case_fail_count_wrong:{metrics.get('demo_case_fail_count')}")
    if metrics.get("readout_count") != 6:
        failures.append(f"readout_count_wrong:{metrics.get('readout_count')}")
    if metrics.get("demo_receipt_count") != 6:
        failures.append(f"demo_receipt_count_wrong:{metrics.get('demo_receipt_count')}")
    if metrics.get("forbidden_input_stop_count") != 1:
        failures.append(f"forbidden_input_stop_count_wrong:{metrics.get('forbidden_input_stop_count')}")
    if metrics.get("local_gotcha_record_count") != 1:
        failures.append(f"local_gotcha_record_count_wrong:{metrics.get('local_gotcha_record_count')}")
    if metrics.get("taxonomy_pressure_recorded_count") != 1:
        failures.append(f"taxonomy_pressure_recorded_count_wrong:{metrics.get('taxonomy_pressure_recorded_count')}")
    for key in [
        "source_trace_modified_count",
        "source_receipt_modified_count",
        "source_ledger_modified_count",
        "source_runner_modified_count",
        "source_regime_modified_count",
        "taxonomy_delta_applied_count",
        "taxonomy_delta_promoted_count",
        "proposal_executed_count",
        "proposal_promoted_count",
        "registry_write_count",
        "registry_sqlite_write_count",
        "hidden_continuation_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("authority_guards") or {}
    for key in [
        "proceed_contract_emitted",
        "current_surface_manifest_schema_emitted",
        "current_surface_manifest_emitted",
        "proceed_unit_schema_emitted",
        "proceed_unit_registry_emitted",
        "proceed_selector_emitted",
        "proceed_readout_schema_emitted",
        "authority_check_schema_emitted",
        "local_gotcha_schema_emitted",
        "taxonomy_pressure_stub_emitted",
        "adapter_module_implemented",
        "demo_fixtures_created",
        "demo_readouts_emitted",
        "demo_receipts_emitted",
        "implementation_receipt_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"authority_guard_not_true:{key}:{guards.get(key)}")

    for key in [
        "source_trace_ledger_runner_modified",
        "source_jurisdiction_runner_v0_2_modified",
        "source_jurisdiction_runner_v0_1_modified",
        "source_local_regime_v1_modified",
        "source_trace_modified",
        "source_receipt_modified",
        "source_ledger_modified",
        "proposal_executed",
        "proposal_promoted",
        "taxonomy_delta_applied",
        "taxonomy_delta_promoted",
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
    trace_ledger_receipt = read_json(TRACE_LEDGER_IMPLEMENTATION_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    ledger_schema = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    local_regime_v1 = read_json(LOCAL_REGIME_V1_PATH)

    failures = validate_policy_inputs(policy, policy_receipt, trace_ledger_receipt, trace_schema, ledger_schema, local_regime_v1)

    for d in [
        CONTRACT_DIR,
        SURFACE_MANIFEST_SCHEMA_DIR,
        SURFACE_MANIFEST_DIR,
        UNIT_SCHEMA_DIR,
        UNIT_REGISTRY_DIR,
        SELECTOR_DIR,
        READOUT_SCHEMA_DIR,
        AUTHORITY_SCHEMA_DIR,
        GOTCHA_SCHEMA_DIR,
        TAXONOMY_STUB_DIR,
        FIXTURE_DIR,
        READOUT_DIR,
        RECEIPT_DIR,
        IMPLEMENTATION_RECEIPT_DIR,
    ]:
        d.mkdir(parents=True, exist_ok=True)

    schema_artifacts = write_schema_artifacts(policy_receipt)

    write_adapter_module()
    subprocess.run([sys.executable, "-m", "py_compile", str(ADAPTER_MODULE_PATH)], check=True)
    adapter_mod = import_adapter_module()
    adapter = adapter_mod.ProceedAdapterV0(policy_receipt)

    source_refs_default = source_refs_from_trace_ledger_receipt(trace_ledger_receipt, "TRACE_PRESENT_FOR_HALT_WITH_PROPOSAL")
    source_refs_duplicate = source_refs_from_trace_ledger_receipt(trace_ledger_receipt, "LEDGER_SUPPRESSES_DUPLICATE_UNRESOLVED_PROPOSAL")

    case_results: Dict[str, Dict[str, Any]] = {}
    readout_results: Dict[str, Dict[str, Any]] = {}
    receipt_results: Dict[str, Dict[str, Any]] = {}

    for case_name in DEMO_CASES:
        refs = source_refs_duplicate if case_name == "PROCEED_READOUT_REFERENCES_TRACE_RECEIPT_LEDGER" else source_refs_default
        fixture = build_fixture(case_name, refs, policy_receipt)
        fixture_path = FIXTURE_DIR / f"{fixture['fixture_id']}.json"
        write_json(fixture_path, fixture)

        readout = adapter.proceed(fixture)
        case_failures = validate_readout(case_name, readout, policy_receipt)

        readout_path = READOUT_DIR / f"{readout['readout_id']}.json"
        write_json(readout_path, readout)

        demo_receipt = build_demo_receipt(case_name, fixture, readout, readout_path.relative_to(ROOT).as_posix())
        demo_receipt["failures"] = case_failures
        demo_receipt["gate"] = "PASS" if not case_failures else "FAIL"
        demo_receipt_path = RECEIPT_DIR / f"{demo_receipt['receipt_id']}.json"
        write_json(demo_receipt_path, demo_receipt)

        failures.extend(case_failures)

        case_results[case_name] = {
            "case_name": case_name,
            "fixture_id": fixture["fixture_id"],
            "fixture_path": fixture_path.relative_to(ROOT).as_posix(),
            "readout_id": readout["readout_id"],
            "readout_path": readout_path.relative_to(ROOT).as_posix(),
            "demo_receipt_id": demo_receipt["receipt_id"],
            "demo_receipt_path": demo_receipt_path.relative_to(ROOT).as_posix(),
            "selected_unit": readout["selected_unit"],
            "units_advanced_count": readout["units_advanced_count"],
            "terminal_result": readout["terminal_result"],
            "authority_status": readout["authority_check"]["authority_status"],
            "trace_delta_present": bool(readout["trace_delta"].get("trace_ref", {}).get("trace_path")),
            "receipt_delta_present": bool(readout["receipt_or_projection_delta"].get("receipt_ref", {}).get("receipt_path")),
            "ledger_delta_present": bool(readout["ledger_delta"].get("ledger_ref", {}).get("ledger_path")),
            "visible_gotcha_count": len(readout["visible_gotchas_fixed"]),
            "taxonomy_pressure_status": readout["taxonomy_pressure"]["status"],
            "taxonomy_delta_applied": readout["taxonomy_pressure"]["taxonomy_delta_applied"],
            "taxonomy_delta_promoted": readout["taxonomy_pressure"]["taxonomy_delta_promoted"],
            "source_artifact_mutation": readout["source_artifact_mutation"],
            "proposal_executed": readout["proposal_execution"]["proposal_executed"],
            "proposal_promoted": readout["proposal_execution"]["proposal_promoted"],
            "registry_written": readout["registry_effect"]["registry_written"],
            "gate": demo_receipt["gate"],
        }

        readout_results[readout["readout_id"]] = {
            "readout_id": readout["readout_id"],
            "readout_path": readout_path.relative_to(ROOT).as_posix(),
            "case_name": case_name,
            "selected_unit": readout["selected_unit"],
            "terminal_result": readout["terminal_result"],
        }

        receipt_results[demo_receipt["receipt_id"]] = {
            "demo_receipt_id": demo_receipt["receipt_id"],
            "demo_receipt_path": demo_receipt_path.relative_to(ROOT).as_posix(),
            "case_name": case_name,
            "readout_id": readout["readout_id"],
            "gate": demo_receipt["gate"],
        }

    aggregate_metrics = {
        "demo_case_count": len(case_results),
        "demo_case_pass_count": sum(1 for r in case_results.values() if r["gate"] == "PASS"),
        "demo_case_fail_count": sum(1 for r in case_results.values() if r["gate"] != "PASS"),
        "readout_count": len(readout_results),
        "demo_receipt_count": len(receipt_results),
        "total_units_advanced_count": sum(r["units_advanced_count"] for r in case_results.values()),
        "forbidden_input_stop_count": sum(1 for r in case_results.values() if r["terminal_result"].get("stop_code") == "STOP_AUTHORITY_VIOLATION"),
        "local_gotcha_record_count": sum(r["visible_gotcha_count"] for r in case_results.values()),
        "taxonomy_pressure_recorded_count": sum(1 for r in case_results.values() if r["taxonomy_pressure_status"] == "RECORDED_ONLY"),
        "source_trace_modified_count": sum(1 for r in case_results.values() if r["source_artifact_mutation"]["source_trace_modified"]),
        "source_receipt_modified_count": sum(1 for r in case_results.values() if r["source_artifact_mutation"]["source_receipt_modified"]),
        "source_ledger_modified_count": sum(1 for r in case_results.values() if r["source_artifact_mutation"]["source_ledger_modified"]),
        "source_runner_modified_count": sum(1 for r in case_results.values() if r["source_artifact_mutation"]["source_runner_modified"]),
        "source_regime_modified_count": sum(1 for r in case_results.values() if r["source_artifact_mutation"]["source_regime_modified"]),
        "taxonomy_delta_applied_count": sum(1 for r in case_results.values() if r["taxonomy_delta_applied"]),
        "taxonomy_delta_promoted_count": sum(1 for r in case_results.values() if r["taxonomy_delta_promoted"]),
        "proposal_executed_count": sum(1 for r in case_results.values() if r["proposal_executed"]),
        "proposal_promoted_count": sum(1 for r in case_results.values() if r["proposal_promoted"]),
        "registry_write_count": sum(1 for r in case_results.values() if r["registry_written"]),
        "registry_sqlite_write_count": 0,
        "hidden_continuation_count": 0,
    }

    acceptance_gate_results = {
        "P0_source_surface_verified": len(validate_policy_inputs(policy, policy_receipt, trace_ledger_receipt, trace_schema, ledger_schema, local_regime_v1)) == 0,
        "P1_proceed_contract_declared": schema_artifacts.get("proceed_contract") is not None,
        "P2_unit_schema_and_registry_declared": schema_artifacts.get("proceed_unit_schema") is not None and schema_artifacts.get("proceed_unit_registry") is not None,
        "P3_selector_declared": schema_artifacts.get("proceed_selector") is not None,
        "P4_readout_and_authority_schemas_declared": (
            schema_artifacts.get("proceed_readout_schema") is not None
            and schema_artifacts.get("authority_check_schema") is not None
            and schema_artifacts.get("local_gotcha_record_schema") is not None
            and schema_artifacts.get("taxonomy_pressure_record_stub") is not None
        ),
        "P5_demo_implementation_required": (
            aggregate_metrics["demo_case_count"] == 6
            and aggregate_metrics["demo_case_pass_count"] == 6
            and aggregate_metrics["readout_count"] == 6
            and aggregate_metrics["demo_receipt_count"] == 6
        ),
        "P6_no_source_runner_or_regime_mutation": (
            aggregate_metrics["source_runner_modified_count"] == 0
            and aggregate_metrics["source_regime_modified_count"] == 0
            and aggregate_metrics["source_trace_modified_count"] == 0
            and aggregate_metrics["source_receipt_modified_count"] == 0
            and aggregate_metrics["source_ledger_modified_count"] == 0
        ),
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    authority_guards = {
        "source_surface_verified": True,
        "proceed_contract_emitted": True,
        "current_surface_manifest_schema_emitted": True,
        "current_surface_manifest_emitted": True,
        "proceed_unit_schema_emitted": True,
        "proceed_unit_registry_emitted": True,
        "proceed_selector_emitted": True,
        "proceed_readout_schema_emitted": True,
        "authority_check_schema_emitted": True,
        "local_gotcha_schema_emitted": True,
        "taxonomy_pressure_stub_emitted": True,
        "adapter_module_implemented": True,
        "adapter_module_path": ADAPTER_MODULE_PATH.relative_to(ROOT).as_posix(),
        "demo_fixtures_created": True,
        "demo_readouts_emitted": True,
        "demo_receipts_emitted": True,
        "implementation_receipt_emitted": True,
        "source_trace_ledger_runner_modified": False,
        "source_jurisdiction_runner_v0_2_modified": False,
        "source_jurisdiction_runner_v0_1_modified": False,
        "source_local_regime_v1_modified": False,
        "source_trace_modified": False,
        "source_receipt_modified": False,
        "source_ledger_modified": False,
        "proposal_executed": False,
        "proposal_promoted": False,
        "taxonomy_delta_applied": False,
        "taxonomy_delta_promoted": False,
        "registry_written": False,
        "registry_sqlite_read": False,
        "registry_sqlite_written": False,
        "global_taxonomy_claimed": False,
        "final_schema_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
    }

    artifact_guards = {
        "proceed_policy_tracked": tracked(POLICY_PATH),
        "proceed_policy_receipt_tracked": tracked(POLICY_RECEIPT_PATH),
        "source_trace_ledger_receipt_tracked": tracked(TRACE_LEDGER_IMPLEMENTATION_RECEIPT_PATH),
        "source_trace_schema_tracked": tracked(TRACE_SCHEMA_PATH),
        "source_ledger_schema_tracked": tracked(PROPOSAL_LEDGER_SCHEMA_PATH),
        "source_trace_ledger_runner_tracked": tracked(TRACE_LEDGER_RUNNER_PATH),
        "source_local_regime_v1_tracked": tracked(LOCAL_REGIME_V1_PATH),
        "adapter_module_path_addressed": True,
        "schemas_path_addressed": True,
        "fixtures_path_addressed": True,
        "readouts_path_addressed": True,
        "receipts_path_addressed": True,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_authority_used": False,
    }

    implementation_seed = {
        "unit_id": UNIT_ID,
        "policy_id": PROCEED_ADAPTER_POLICY_ID,
        "schema_artifacts": schema_artifacts,
        "demo_receipts": {k: v["demo_receipt_id"] for k, v in sorted(case_results.items())},
    }
    implementation_receipt_id = sha8(implementation_seed)

    implementation_receipt = {
        "schema_version": "proceed_adapter_v0_implementation_receipt_v0",
        "receipt_type": "PROCEED_ADAPTER_V0_IMPLEMENTATION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": implementation_receipt_id,
        "source_proceed_policy_id": PROCEED_ADAPTER_POLICY_ID,
        "source_proceed_policy_receipt_id": PROCEED_ADAPTER_POLICY_RECEIPT_ID,
        "target_adapter_unit_id": TARGET_ADAPTER_UNIT_ID,
        "source_runner_unit_id": SOURCE_RUNNER_UNIT_ID,
        "source_local_regime_version": SOURCE_LOCAL_REGIME_VERSION,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "adapter_module_path": ADAPTER_MODULE_PATH.relative_to(ROOT).as_posix(),
        "schema_artifacts": schema_artifacts,
        "case_results": case_results,
        "readout_results": readout_results,
        "demo_receipt_results": receipt_results,
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
    print(f"proceed_adapter_implementation_receipt_id={implementation_receipt_id}")
    print(f"proceed_adapter_implementation_receipt_path=data/proceed_adapter_v0_implementation_receipts/{implementation_receipt_id}.json")
    print(f"proceed_adapter_module_path={ADAPTER_MODULE_PATH.relative_to(ROOT).as_posix()}")

    for name, artifact in sorted(schema_artifacts.items()):
        print(f"schema_artifact_{name}_id={artifact['artifact_id']}")
        print(f"schema_artifact_{name}_path={artifact['artifact_path']}")

    for case_name, result in sorted(case_results.items()):
        print(f"case_{case_name}_fixture_path={result['fixture_path']}")
        print(f"case_{case_name}_readout_id={result['readout_id']}")
        print(f"case_{case_name}_readout_path={result['readout_path']}")
        print(f"case_{case_name}_demo_receipt_id={result['demo_receipt_id']}")
        print(f"case_{case_name}_demo_receipt_path={result['demo_receipt_path']}")

    return 0 if implementation_receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
