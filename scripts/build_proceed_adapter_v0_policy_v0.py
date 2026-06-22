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

UNIT_ID = "BUILD_PROCEED_ADAPTER_V0_POLICY_V0"
NEXT_GOAL = "IMPLEMENT_PROCEED_ADAPTER_V0_WITH_DEMO_FIXTURES_V0"

SOURCE_RUNNER_UNIT_ID = "jurisdiction_runner.v0.2.trace_ledger_hardened"
TARGET_ADAPTER_UNIT_ID = "proceed_adapter.v0"
SOURCE_LOCAL_REGIME_VERSION = "local_regime.v1"
SOURCE_LOCAL_REGIME_HASH = "25802530"

TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID = "cc24a11f"
TRACE_SCHEMA_ID = "b4887660"
PROPOSAL_LEDGER_SCHEMA_ID = "eee2a318"
TRACE_LEDGER_POLICY_ID = "b98866ad"
V0_2_IMPLEMENTATION_RECEIPT_ID = "6b90ca5e"

TRACE_LEDGER_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts" / f"{TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID}.json"
TRACE_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_schemas" / f"{TRACE_SCHEMA_ID}.json"
PROPOSAL_LEDGER_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposal_ledger_schemas" / f"{PROPOSAL_LEDGER_SCHEMA_ID}.json"
TRACE_LEDGER_RUNNER_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_2_trace_ledger.py"
TRACE_LEDGER_POLICY_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_and_proposal_ledger_hardening_policies" / f"{TRACE_LEDGER_POLICY_ID}.json"
LOCAL_REGIME_V1_PATH = ROOT / "data" / "local_regime_v1_declarations" / f"{SOURCE_LOCAL_REGIME_HASH}.json"
V0_2_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_implementation_receipts" / f"{V0_2_IMPLEMENTATION_RECEIPT_ID}.json"
RUNNER_V0_2_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_2.py"

OUT_DIR = ROOT / "data" / "proceed_adapter_v0_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "proceed_adapter_v0_policy_receipts"

PROCEED_STOP_SET = [
    "STOP_DONE",
    "STOP_NEXT_MOVE_BOUNDARY",
    "STOP_VISIBLE_GOTCHA",
    "STOP_PROJECTION_BUG",
    "STOP_RECEIPT_MISMATCH",
    "STOP_UNTYPED_UNIT",
    "STOP_UNDERTYPED_OBJECT",
    "STOP_TAXONOMY_GAP",
    "STOP_NEEDS_NEW_MOVE",
    "STOP_NEEDS_EXTRACTION",
    "STOP_AUTHORITY_VIOLATION",
    "STOP_LAYER_COLLAPSE",
    "STOP_GATE_FAIL",
]

PROCEED_CONTRACT = {
    "schema_version": "proceed_contract_v0",
    "contract_id": "proceed_contract.v0",
    "command": "proceed",
    "meaning": "advance one smallest lawful unit from the current typed surface",
    "unit_rule": "one unit only",
    "repair_rule": "local visible gotchas only; no semantic widening",
    "output_rule": "emit proceed readout, trace delta, receipt/projection delta, ledger delta, or typed stop",
    "terminal_rule": "ADVANCE(next_unit_id) or STOP(stop_code)",
    "authority_rule": "use only declared current surface manifest",
    "taxonomy_rule": "taxonomy pressure may be recorded but not self-accepted",
    "core_law": {
        "proceed_is_not_continue_forever": True,
        "proceed_is_not_redesign": True,
        "proceed_is_not_missing_architecture_inference": True,
        "proceed_is_not_silent_semantic_repair": True,
        "proceed_is_one_smallest_lawful_advancement": True,
    },
}

CURRENT_SURFACE_MANIFEST_SCHEMA = {
    "schema_version": "current_surface_manifest_schema_v0",
    "required_fields": [
        "source_runner_unit_id",
        "source_runner_module_path",
        "source_local_regime_version",
        "source_local_regime_hash",
        "source_trace_schema_id",
        "source_trace_schema_path",
        "source_proposal_ledger_schema_id",
        "source_proposal_ledger_schema_path",
        "source_implementation_receipt_id",
        "current_receipt_ref",
        "current_trace_ref",
        "current_ledger_ref",
    ],
    "authority_boundary": "all refs must be path-addressed; latest/mtime/ambient inference forbidden",
}

PROCEED_UNIT_SCHEMA = {
    "schema_version": "proceed_unit_schema_v0",
    "required_fields": [
        "unit_id",
        "unit_scope",
        "layer",
        "mode",
        "active_object",
        "current_surface_manifest_ref",
        "allowed_inputs",
        "forbidden_inputs",
        "lawful_move_or_repair_target",
        "expected_readout",
        "terminal_condition",
    ],
    "unit_scope_required_fields": [
        "layer",
        "active_object",
        "may_read",
        "may_write",
        "must_not_touch",
    ],
}

PROCEED_UNIT_REGISTRY = {
    "schema_version": "proceed_unit_registry_v0",
    "registry_id": "proceed_unit_registry.v0",
    "units": [
        {
            "unit_id": "proceed.unit.validate_current_surface.v0",
            "priority": 10,
            "purpose": "Check declared current surface manifest and source artifacts.",
            "advance_on_pass": "proceed.unit.execute_declared_runner_unit.v0",
            "possible_stops": [
                "STOP_UNTYPED_UNIT",
                "STOP_DEPENDENCY_MISSING",
                "STOP_AUTHORITY_VIOLATION",
            ],
        },
        {
            "unit_id": "proceed.unit.execute_declared_runner_unit.v0",
            "priority": 20,
            "purpose": "Execute exactly one declared runner/adapter unit using allowed inputs only.",
            "advance_on_pass": "proceed.unit.verify_readout_against_trace.v0",
            "possible_stops": [
                "STOP_GATE_FAIL",
                "STOP_RECEIPT_MISMATCH",
                "STOP_NEXT_MOVE_BOUNDARY",
            ],
        },
        {
            "unit_id": "proceed.unit.verify_readout_against_trace.v0",
            "priority": 30,
            "purpose": "Verify visible proceed readout agrees with trace, receipt, and ledger deltas.",
            "advance_on_pass": "proceed.unit.emit_next_boundary.v0",
            "possible_stops": [
                "STOP_PROJECTION_BUG",
                "STOP_RECEIPT_MISMATCH",
                "STOP_VISIBLE_GOTCHA",
            ],
        },
        {
            "unit_id": "proceed.unit.emit_next_boundary.v0",
            "priority": 40,
            "purpose": "Emit terminal boundary and prevent implicit continuation.",
            "advance_on_pass": None,
            "possible_stops": [
                "STOP_DONE",
                "STOP_NEXT_MOVE_BOUNDARY",
                "STOP_TAXONOMY_GAP",
                "STOP_NEEDS_NEW_MOVE",
            ],
        },
    ],
}

PROCEED_SELECTOR = {
    "schema_version": "proceed_selector_v0",
    "selector_id": "proceed_selector.smallest_lawful_unit.v0",
    "selection_order": [
        "repair visible projection/readout mismatch",
        "repair visible receipt/trace mismatch",
        "complete already-declared unit",
        "type under-typed object blocking movement",
        "record smallest halt/taxonomy pressure forced by failure",
        "stop if next move is missing",
        "stop at next move boundary or done",
    ],
    "selection_law": [
        "if projection/readout mismatch exists select repair_projection_unit",
        "else if receipt/trace mismatch exists select repair_receipt_unit",
        "else if declared unit is incomplete select declared_unit",
        "else if blocking object is under-typed STOP_UNDERTYPED_OBJECT",
        "else if halt vocabulary cannot classify stop STOP_TAXONOMY_GAP",
        "else if next move is missing STOP_NEEDS_NEW_MOVE",
        "else STOP_NEXT_MOVE_BOUNDARY or STOP_DONE",
    ],
}

AUTHORITY_CHECK_SCHEMA = {
    "schema_version": "authority_check_schema_v0",
    "required_fields": [
        "allowed_inputs_used",
        "forbidden_inputs_detected",
        "authority_status",
    ],
    "allowed_inputs": [
        "declared_current_surface_manifest",
        "declared_runner_module",
        "declared_local_regime",
        "declared_trace_schema",
        "declared_proposal_ledger_schema",
        "declared_receipt_ref",
        "declared_trace_ref",
        "declared_ledger_ref",
        "declared_proceed_unit_registry",
        "declared_halt_vocabulary",
    ],
    "forbidden_inputs": [
        "latest_file_guessing",
        "mtime_selection",
        "ambient_workspace_inference",
        "hidden_memory_authority",
        "prose_only_promotion",
        "unregistered_moves",
        "architecture_widening_by_convenience",
    ],
}

LOCAL_GOTCHA_RECORD_SCHEMA = {
    "schema_version": "local_gotcha_record_schema_v0",
    "required_fields": [
        "gotcha_id",
        "kind",
        "observed",
        "corrected_to",
        "basis",
        "semantic_widening",
        "source_trace_modified",
        "source_receipt_modified",
        "source_ledger_modified",
        "source_runner_modified",
        "source_regime_modified",
    ],
    "law": {
        "may_alter_readout_or_projection_artifact": True,
        "may_alter_source_trace": False,
        "may_alter_source_receipt": False,
        "may_alter_source_ledger": False,
        "may_alter_source_runner": False,
        "may_alter_source_regime": False,
    },
}

TAXONOMY_PRESSURE_RECORD_STUB = {
    "schema_version": "taxonomy_pressure_record_stub_v0",
    "required_fields": [
        "detected",
        "trigger_halt",
        "observed_pressure",
        "status",
        "taxonomy_delta_applied",
        "taxonomy_delta_promoted",
    ],
    "allowed_status": [
        "NONE",
        "RECORDED_ONLY",
    ],
    "law": {
        "may_record_pressure": True,
        "may_accept_taxonomy_delta": False,
        "may_mutate_taxonomy_registry": False,
        "may_add_new_move_automatically": False,
        "may_promote_new_halt_vocab": False,
    },
}

PROCEED_READOUT_SCHEMA = {
    "schema_version": "proceed_readout_schema_v0",
    "required_fields": [
        "readout_id",
        "schema_version",
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
    ],
    "terminal_result_law": {
        "ADVANCE_requires_next_unit_id_non_null_and_stop_code_null": True,
        "STOP_requires_stop_code_non_null_and_next_unit_id_null": True,
    },
}

REQUIRED_DEMO_CASES = {
    "PROCEED_ADVANCES_ONE_NAMED_UNIT": {
        "purpose": "Proceed selects exactly one named unit from the declared current surface.",
        "expected_selected_unit": "proceed.unit.validate_current_surface.v0",
        "expected_units_advanced_count": 1,
    },
    "PROCEED_AUTHORITY_CHECK_REJECTS_FORBIDDEN_INPUTS": {
        "purpose": "Proceed readout records allowed inputs and stops on forbidden latest/mtime/ambient authority.",
        "expected_forbidden_input_stop": "STOP_AUTHORITY_VIOLATION",
    },
    "PROCEED_READOUT_REFERENCES_TRACE_RECEIPT_LEDGER": {
        "purpose": "Proceed readout references trace, receipt/projection, and ledger deltas from declared surface.",
        "expected_trace_delta_present": True,
        "expected_receipt_delta_present": True,
        "expected_ledger_delta_present": True,
    },
    "PROCEED_LOCAL_GOTCHA_RECORD_ONLY": {
        "purpose": "Visible local gotcha can be recorded/fixed only in readout/projection, without changing source trace/receipt/ledger/runner/regime.",
        "expected_semantic_widening": False,
    },
    "PROCEED_TAXONOMY_PRESSURE_RECORDED_ONLY": {
        "purpose": "Taxonomy pressure may be recorded but not accepted, promoted, or applied.",
        "expected_taxonomy_status": "RECORDED_ONLY",
        "expected_taxonomy_delta_applied": False,
    },
    "PROCEED_TERMINAL_BOUNDARY_NO_IMPLICIT_CONTINUATION": {
        "purpose": "Proceed terminates as ADVANCE(next_unit_id) or STOP(stop_code), never hidden continuation.",
        "expected_hidden_continuation": False,
    },
}

ACCEPTANCE_GATES = {
    "P0_source_surface_verified": {
        "required": True,
        "description": "Source trace-ledger implementation, runner, local_regime.v1, trace schema, and ledger schema are tracked and path-addressed.",
    },
    "P1_proceed_contract_declared": {
        "required": True,
        "description": "Proceed contract declares one-unit-only semantics and forbids implicit continuation/architecture widening.",
    },
    "P2_unit_schema_and_registry_declared": {
        "required": True,
        "description": "Proceed unit schema and minimal unit registry are declared.",
    },
    "P3_selector_declared": {
        "required": True,
        "description": "Smallest-lawful-unit selector is declared.",
    },
    "P4_readout_and_authority_schemas_declared": {
        "required": True,
        "description": "Proceed readout, authority check, local gotcha, and taxonomy pressure schemas are declared.",
    },
    "P5_demo_implementation_required": {
        "required": True,
        "description": "Next unit must implement demo fixtures proving one-unit proceed semantics.",
    },
    "P6_no_source_runner_or_regime_mutation": {
        "required": True,
        "description": "Policy does not mutate source runner, source regime, traces, receipts, ledgers, or registry.",
    },
}

REQUIRED_IMPLEMENTATION_ARTIFACTS = {
    "proceed_contract": "data/proceed_adapter_v0_contracts/<contract_id>.json",
    "current_surface_manifest_schema": "data/proceed_adapter_v0_surface_manifest_schemas/<schema_id>.json",
    "proceed_unit_schema": "data/proceed_adapter_v0_unit_schemas/<schema_id>.json",
    "proceed_unit_registry": "data/proceed_adapter_v0_unit_registries/<registry_id>.json",
    "proceed_selector": "data/proceed_adapter_v0_selectors/<selector_id>.json",
    "proceed_readout_schema": "data/proceed_adapter_v0_readout_schemas/<schema_id>.json",
    "authority_check_schema": "data/proceed_adapter_v0_authority_check_schemas/<schema_id>.json",
    "local_gotcha_schema": "data/proceed_adapter_v0_local_gotcha_schemas/<schema_id>.json",
    "taxonomy_pressure_stub": "data/proceed_adapter_v0_taxonomy_pressure_stubs/<stub_id>.json",
    "adapter_module": "src/matrixlab/proceed_adapter_v0.py",
    "demo_fixtures": "data/proceed_adapter_v0_demo_fixtures/*.json",
    "demo_readouts": "data/proceed_adapter_v0_demo_readouts/*.json",
    "demo_receipts": "data/proceed_adapter_v0_demo_receipts/*.json",
    "implementation_receipt": "data/proceed_adapter_v0_implementation_receipts/<receipt_id>.json",
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
    trace_ledger_receipt: Dict[str, Any],
    trace_schema: Dict[str, Any],
    ledger_schema: Dict[str, Any],
    trace_ledger_policy: Dict[str, Any],
    local_regime_v1: Dict[str, Any],
    v0_2_receipt: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if trace_ledger_receipt.get("receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"trace_ledger_receipt_id_wrong:{trace_ledger_receipt.get('receipt_id')}")
    if trace_ledger_receipt.get("gate") != "PASS":
        failures.append(f"trace_ledger_gate_not_PASS:{trace_ledger_receipt.get('gate')}")
    if trace_ledger_receipt.get("source_runner_unit_id") != "jurisdiction_runner.v0.2":
        failures.append(f"trace_ledger_source_runner_wrong:{trace_ledger_receipt.get('source_runner_unit_id')}")
    if trace_ledger_receipt.get("target_runner_unit_id") != SOURCE_RUNNER_UNIT_ID:
        failures.append(f"trace_ledger_target_runner_wrong:{trace_ledger_receipt.get('target_runner_unit_id')}")
    if trace_ledger_receipt.get("source_local_regime_hash") != SOURCE_LOCAL_REGIME_HASH:
        failures.append(f"trace_ledger_source_regime_hash_wrong:{trace_ledger_receipt.get('source_local_regime_hash')}")
    if trace_ledger_receipt.get("trace_schema_id") != TRACE_SCHEMA_ID:
        failures.append(f"trace_schema_id_wrong:{trace_ledger_receipt.get('trace_schema_id')}")
    if trace_ledger_receipt.get("proposal_ledger_schema_id") != PROPOSAL_LEDGER_SCHEMA_ID:
        failures.append(f"proposal_ledger_schema_id_wrong:{trace_ledger_receipt.get('proposal_ledger_schema_id')}")

    terminal = trace_ledger_receipt.get("terminal") or {}
    if terminal.get("type") != "STOP":
        failures.append(f"trace_ledger_terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_DONE":
        failures.append(f"trace_ledger_terminal_stop_not_DONE:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"trace_ledger_terminal_next_not_null:{terminal}")

    gates = trace_ledger_receipt.get("acceptance_gate_results") or {}
    for gate in [
        "H0_source_chain_verified",
        "H1_trace_schema_declared",
        "H2_proposal_ledger_schema_declared",
        "H3_trace_hardened_runner_implemented",
        "H4_trace_files_emitted_for_cases",
        "H5_receipts_reference_traces",
        "H6_unresolved_proposal_ledger_artifact_used",
        "H7_v0_2_regression_preserved",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"trace_ledger_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = trace_ledger_receipt.get("aggregate_metrics") or {}
    if metrics.get("hardening_case_count") != 6:
        failures.append(f"hardening_case_count_wrong:{metrics.get('hardening_case_count')}")
    if metrics.get("hardening_case_pass_count") != 6:
        failures.append(f"hardening_case_pass_count_wrong:{metrics.get('hardening_case_pass_count')}")
    if metrics.get("case_receipt_trace_consistency_fail_count") != 0:
        failures.append(f"trace_consistency_failures_nonzero:{metrics.get('case_receipt_trace_consistency_fail_count')}")
    if metrics.get("duplicate_unresolved_proposal_count") != 1:
        failures.append(f"duplicate_count_wrong:{metrics.get('duplicate_unresolved_proposal_count')}")
    for key in [
        "runtime_proposal_executed_count",
        "runtime_proposal_promoted_count",
        "registry_write_count",
        "local_regime_mutation_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"trace_ledger_metric_not_zero:{key}:{metrics.get(key)}")

    guards = trace_ledger_receipt.get("authority_guards") or {}
    for key in [
        "jurisdiction_runner_v0_1_modified",
        "jurisdiction_runner_v0_2_modified",
        "local_regime_v1_replaced",
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
            failures.append(f"trace_ledger_guard_not_false:{key}:{guards.get(key)}")

    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append(f"trace_schema_version_wrong:{trace_schema.get('schema_version')}")
    if trace_schema.get("receipt_consistency_required") is not True:
        failures.append("trace_schema_receipt_consistency_not_true")

    if ledger_schema.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append(f"ledger_schema_version_wrong:{ledger_schema.get('schema_version')}")
    if ledger_schema.get("ledger_scope") != "path-addressed local artifact only, no registry or sqlite authority":
        failures.append(f"ledger_scope_wrong:{ledger_schema.get('ledger_scope')}")

    if trace_ledger_policy.get("policy_id") != TRACE_LEDGER_POLICY_ID:
        failures.append(f"trace_ledger_policy_id_wrong:{trace_ledger_policy.get('policy_id')}")

    if local_regime_v1.get("local_regime_hash") != SOURCE_LOCAL_REGIME_HASH:
        failures.append(f"local_regime_v1_hash_wrong:{local_regime_v1.get('local_regime_hash')}")
    if local_regime_v1.get("local_regime_version") != SOURCE_LOCAL_REGIME_VERSION:
        failures.append(f"local_regime_v1_version_wrong:{local_regime_v1.get('local_regime_version')}")

    if v0_2_receipt.get("receipt_id") != V0_2_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"v0_2_receipt_id_wrong:{v0_2_receipt.get('receipt_id')}")
    if v0_2_receipt.get("gate") != "PASS":
        failures.append(f"v0_2_gate_not_PASS:{v0_2_receipt.get('gate')}")

    for path, label in [
        (TRACE_LEDGER_IMPLEMENTATION_RECEIPT_PATH, "trace_ledger_implementation_receipt"),
        (TRACE_SCHEMA_PATH, "trace_schema"),
        (PROPOSAL_LEDGER_SCHEMA_PATH, "proposal_ledger_schema"),
        (TRACE_LEDGER_RUNNER_PATH, "trace_ledger_runner"),
        (TRACE_LEDGER_POLICY_PATH, "trace_ledger_policy"),
        (LOCAL_REGIME_V1_PATH, "local_regime_v1"),
        (V0_2_IMPLEMENTATION_RECEIPT_PATH, "v0_2_implementation_receipt"),
        (RUNNER_V0_2_PATH, "runner_v0_2"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{path.relative_to(ROOT).as_posix()}")

    return failures

def build_policy(write_outputs: bool = True) -> tuple[Dict[str, Any], Dict[str, Any]]:
    trace_ledger_receipt = read_json(TRACE_LEDGER_IMPLEMENTATION_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    ledger_schema = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    trace_ledger_policy = read_json(TRACE_LEDGER_POLICY_PATH)
    local_regime_v1 = read_json(LOCAL_REGIME_V1_PATH)
    v0_2_receipt = read_json(V0_2_IMPLEMENTATION_RECEIPT_PATH)

    failures = validate_inputs(
        trace_ledger_receipt,
        trace_schema,
        ledger_schema,
        trace_ledger_policy,
        local_regime_v1,
        v0_2_receipt,
    )

    policy_seed = {
        "unit_id": UNIT_ID,
        "target_adapter_unit_id": TARGET_ADAPTER_UNIT_ID,
        "source_runner_unit_id": SOURCE_RUNNER_UNIT_ID,
        "source_trace_ledger_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "trace_schema_id": TRACE_SCHEMA_ID,
        "proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "next_goal": NEXT_GOAL,
    }
    policy_id = sha8(policy_seed)

    current_surface_manifest = {
        "schema_version": "current_surface_manifest_v0",
        "surface_manifest_id": sha8({
            "runner": SOURCE_RUNNER_UNIT_ID,
            "local_regime_hash": SOURCE_LOCAL_REGIME_HASH,
            "trace_schema_id": TRACE_SCHEMA_ID,
            "proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
            "implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        }),
        "source_runner_unit_id": SOURCE_RUNNER_UNIT_ID,
        "source_runner_module_path": "src/matrixlab/jurisdiction_runner_v0_2_trace_ledger.py",
        "source_local_regime_version": SOURCE_LOCAL_REGIME_VERSION,
        "source_local_regime_hash": SOURCE_LOCAL_REGIME_HASH,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_trace_schema_path": f"data/jurisdiction_runner_v0_2_trace_schemas/{TRACE_SCHEMA_ID}.json",
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_proposal_ledger_schema_path": f"data/jurisdiction_runner_v0_2_proposal_ledger_schemas/{PROPOSAL_LEDGER_SCHEMA_ID}.json",
        "source_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_implementation_receipt_path": f"data/jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts/{TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID}.json",
        "current_receipt_ref": {
            "receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
            "receipt_path": f"data/jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts/{TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID}.json",
        },
        "current_trace_ref": None,
        "current_ledger_ref": None,
        "authority_boundary": {
            "path_addressed_only": True,
            "latest_or_mtime_selection_allowed": False,
            "ambient_workspace_authority_allowed": False,
        },
    }

    authority_guards = {
        "proceed_policy_built": True,
        "source_trace_ledger_surface_consumed": True,
        "source_runner_read": True,
        "source_runner_modified_by_policy": False,
        "source_regime_read": True,
        "source_regime_modified_by_policy": False,
        "adapter_implemented_by_policy": False,
        "adapter_executed_by_policy": False,
        "readout_emitted_by_policy": False,
        "trace_modified_by_policy": False,
        "receipt_modified_by_policy": False,
        "ledger_modified_by_policy": False,
        "taxonomy_delta_applied": False,
        "taxonomy_delta_promoted": False,
        "proposal_executed": False,
        "proposal_promoted": False,
        "registry_written": False,
        "registry_sqlite_read": False,
        "registry_sqlite_written": False,
        "global_taxonomy_claimed": False,
        "final_schema_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
    }

    policy = {
        "schema_version": "proceed_adapter_v0_policy_v0",
        "policy_type": "PROCEED_ADAPTER_V0_POLICY",
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "target_adapter_unit_id": TARGET_ADAPTER_UNIT_ID,
        "source_runner_unit_id": SOURCE_RUNNER_UNIT_ID,
        "source_local_regime_version": SOURCE_LOCAL_REGIME_VERSION,
        "source_local_regime_hash": SOURCE_LOCAL_REGIME_HASH,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "policy_summary": {
            "purpose": "Make proceed a bounded executable adapter command over the hardened trace-ledger runner surface.",
            "core_law": "proceed advances exactly one smallest lawful unit from the current typed surface.",
            "non_goal": "no architecture widening, rich jurisdiction, full taxonomy evolution, hidden authority, or implicit continuation",
        },
        "current_surface_manifest_schema": CURRENT_SURFACE_MANIFEST_SCHEMA,
        "current_surface_manifest": current_surface_manifest,
        "proceed_contract": PROCEED_CONTRACT,
        "proceed_unit_schema": PROCEED_UNIT_SCHEMA,
        "proceed_unit_registry": PROCEED_UNIT_REGISTRY,
        "proceed_selector": PROCEED_SELECTOR,
        "proceed_readout_schema": PROCEED_READOUT_SCHEMA,
        "authority_check_schema": AUTHORITY_CHECK_SCHEMA,
        "local_gotcha_record_schema": LOCAL_GOTCHA_RECORD_SCHEMA,
        "taxonomy_pressure_record_stub": TAXONOMY_PRESSURE_RECORD_STUB,
        "proceed_stop_set": PROCEED_STOP_SET,
        "required_demo_cases": REQUIRED_DEMO_CASES,
        "required_implementation_artifacts": REQUIRED_IMPLEMENTATION_ARTIFACTS,
        "acceptance_gates": ACCEPTANCE_GATES,
        "authorized_operations_next": {
            "read_proceed_policy": True,
            "read_proceed_policy_receipt": True,
            "read_current_surface_manifest": True,
            "read_source_trace_ledger_runner": True,
            "read_source_local_regime_v1": True,
            "write_proceed_contract": True,
            "write_current_surface_manifest_schema": True,
            "write_proceed_unit_schema": True,
            "write_proceed_unit_registry": True,
            "write_proceed_selector": True,
            "write_proceed_readout_schema": True,
            "write_authority_check_schema": True,
            "write_local_gotcha_record_schema": True,
            "write_taxonomy_pressure_record_stub": True,
            "write_proceed_adapter_module": True,
            "write_demo_fixtures": True,
            "execute_proceed_adapter_demo_fixtures": True,
            "emit_demo_readouts": True,
            "emit_demo_receipts": True,
            "emit_implementation_receipt": True,
        },
        "forbidden_operations_next": {
            "modify_source_trace_ledger_runner": True,
            "modify_jurisdiction_runner_v0_2": True,
            "modify_jurisdiction_runner_v0_1": True,
            "replace_local_regime_v1": True,
            "mutate_local_regime_at_runtime": True,
            "alter_source_trace": True,
            "alter_source_receipt": True,
            "alter_source_ledger": True,
            "execute_or_apply_proposal": True,
            "promote_proposal_without_human_review": True,
            "accept_taxonomy_delta": True,
            "promote_taxonomy_delta": True,
            "sqlite_registry_write": True,
            "sqlite_registry_read": True,
            "full_registry_scan": True,
            "global_taxonomy_design": True,
            "final_schema_claim": True,
            "proof_claim": True,
            "hidden_continuation_after_terminal": True,
            "latest_or_mtime_selection": True,
            "ambient_workspace_authority": True,
        },
        "safety_clauses": {
            "policy_only": True,
            "does_not_implement_adapter": True,
            "does_not_execute_adapter": True,
            "does_not_emit_readout": True,
            "does_not_modify_source_runner": True,
            "does_not_modify_source_regime": True,
            "does_not_modify_source_trace_receipt_or_ledger": True,
            "does_not_apply_or_promote_proposal": True,
            "does_not_accept_or_promote_taxonomy_delta": True,
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
        "unit_id": UNIT_ID,
        "policy_id": policy_id,
        "target_adapter_unit_id": TARGET_ADAPTER_UNIT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "terminal": policy["terminal"],
    }
    receipt_id = sha8(receipt_seed)
    policy["policy_receipt_id"] = receipt_id

    receipt = {
        "schema_version": "proceed_adapter_v0_policy_receipt_v0",
        "receipt_type": "PROCEED_ADAPTER_V0_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "target_adapter_unit_id": TARGET_ADAPTER_UNIT_ID,
        "source_runner_unit_id": SOURCE_RUNNER_UNIT_ID,
        "source_local_regime_version": SOURCE_LOCAL_REGIME_VERSION,
        "source_local_regime_hash": SOURCE_LOCAL_REGIME_HASH,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "policy_summary": policy["policy_summary"],
        "current_surface_manifest_schema": policy["current_surface_manifest_schema"],
        "current_surface_manifest": policy["current_surface_manifest"],
        "proceed_contract": policy["proceed_contract"],
        "proceed_unit_schema": policy["proceed_unit_schema"],
        "proceed_unit_registry": policy["proceed_unit_registry"],
        "proceed_selector": policy["proceed_selector"],
        "proceed_readout_schema": policy["proceed_readout_schema"],
        "authority_check_schema": policy["authority_check_schema"],
        "local_gotcha_record_schema": policy["local_gotcha_record_schema"],
        "taxonomy_pressure_record_stub": policy["taxonomy_pressure_record_stub"],
        "proceed_stop_set": policy["proceed_stop_set"],
        "required_demo_cases": policy["required_demo_cases"],
        "required_implementation_artifacts": policy["required_implementation_artifacts"],
        "acceptance_gates": policy["acceptance_gates"],
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
    print(f"proceed_adapter_policy_id={policy['policy_id']}")
    print(f"proceed_adapter_policy_receipt_id={receipt['receipt_id']}")
    print(f"proceed_adapter_policy_path=data/proceed_adapter_v0_policies/{policy['policy_id']}.json")
    print(f"proceed_adapter_policy_receipt_path=data/proceed_adapter_v0_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
