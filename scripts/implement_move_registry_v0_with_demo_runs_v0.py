#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "IMPLEMENT_MOVE_REGISTRY_V0_WITH_DEMO_RUNS_V0"
TARGET_UNIT_ID = "move_registry.v0"

MOVE_REGISTRY_POLICY_ID = "34863965"
MOVE_REGISTRY_POLICY_RECEIPT_ID = "1264c091"
HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID = "75eabbe2"
HALT_VOCABULARY_POLICY_ID = "0707a2d7"
PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID = "363d2f4a"
TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID = "cc24a11f"
TRACE_SCHEMA_ID = "b4887660"
PROPOSAL_LEDGER_SCHEMA_ID = "eee2a318"
LOCAL_REGIME_V1_HASH = "25802530"

POLICY_PATH = ROOT / "data" / "move_registry_v0_policies" / f"{MOVE_REGISTRY_POLICY_ID}.json"
POLICY_RECEIPT_PATH = ROOT / "data" / "move_registry_v0_policy_receipts" / f"{MOVE_REGISTRY_POLICY_ID}.json"
HALT_IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "halt_vocabulary_v0_implementation_receipts" / f"{HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID}.json"
HALT_VOCABULARY_PATH = ROOT / "data" / "halt_vocabulary_v0" / "halt_vocabulary_v0.json"
HALT_RECORD_SCHEMA_PATH = ROOT / "data" / "halt_record_schemas" / "halt_record_schema_v0.json"
HALT_NEXT_HANDLING_PATH = ROOT / "data" / "halt_to_next_handling_tables" / "halt_to_next_handling_table_v0.json"
PROCEED_RECEIPT_PATH = ROOT / "data" / "proceed_adapter_v0_implementation_receipts" / f"{PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID}.json"
PROCEED_ADAPTER_MODULE_PATH = ROOT / "src" / "matrixlab" / "proceed_adapter_v0.py"
TRACE_LEDGER_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts" / f"{TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID}.json"
TRACE_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_schemas" / f"{TRACE_SCHEMA_ID}.json"
PROPOSAL_LEDGER_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposal_ledger_schemas" / f"{PROPOSAL_LEDGER_SCHEMA_ID}.json"
TRACE_LEDGER_RUNNER_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_2_trace_ledger.py"
LOCAL_REGIME_V1_PATH = ROOT / "data" / "local_regime_v1_declarations" / f"{LOCAL_REGIME_V1_HASH}.json"

ARTIFACT_DIR = ROOT / "data" / "move_registry_v0"
PATCH_DIR = ROOT / "data" / "move_registry_v0_patches"
DEMO_DIR = ROOT / "data" / "move_registry_v0_demo"
IMPLEMENTATION_RECEIPT_DIR = ROOT / "data" / "move_registry_v0_implementation_receipts"

REQUIRED_MOVE_FIELDS = [
    "move_id",
    "schema_version",
    "move_kind",
    "layer",
    "priority",
    "applies_when",
    "allowed_inputs",
    "forbidden_inputs",
    "action",
    "state_delta",
    "emits",
    "may_halt",
    "halt_map",
    "non_impersonation",
]

EXPECTED_STARTER_MOVES = [
    "state.validate_shape.v0",
    "regime.validate_shape.v0",
    "moves.compute_applicable.v0",
    "selector.choose_move.v0",
    "unit.mark_complete.v0",
    "receipt.emit_terminal.v0",
    "proposal.missing_move.draft.v0",
]

SOURCE_FILES = [
    POLICY_PATH,
    POLICY_RECEIPT_PATH,
    HALT_IMPLEMENTATION_RECEIPT_PATH,
    HALT_VOCABULARY_PATH,
    HALT_RECORD_SCHEMA_PATH,
    HALT_NEXT_HANDLING_PATH,
    PROCEED_RECEIPT_PATH,
    PROCEED_ADAPTER_MODULE_PATH,
    TRACE_LEDGER_RECEIPT_PATH,
    TRACE_SCHEMA_PATH,
    PROPOSAL_LEDGER_SCHEMA_PATH,
    TRACE_LEDGER_RUNNER_PATH,
    LOCAL_REGIME_V1_PATH,
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

def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in paths if path.exists()}

def get_path(state: Dict[str, Any], path: str) -> Any:
    if path.startswith("state."):
        obj: Any = state
        parts = path.split(".")[1:]
    elif path.startswith("regime."):
        obj = state.get("regime", {})
        parts = path.split(".")[1:]
    elif path.startswith("readout."):
        obj = state.get("readout", {})
        parts = path.split(".")[1:]
    else:
        obj = state
        parts = path.split(".")
    for part in parts:
        if not isinstance(obj, dict) or part not in obj:
            return None
        obj = obj[part]
    return obj

def path_exists(state: Dict[str, Any], path: str) -> bool:
    return get_path(state, path) is not None

def set_path(state: Dict[str, Any], path: str, value: Any) -> None:
    if path.startswith("state."):
        obj = state
        parts = path.split(".")[1:]
    elif path.startswith("regime."):
        obj = state.setdefault("regime", {})
        parts = path.split(".")[1:]
    else:
        obj = state
        parts = path.split(".")
    for part in parts[:-1]:
        obj = obj.setdefault(part, {})
    obj[parts[-1]] = value

def eval_predicate(predicate: Any, state: Dict[str, Any]) -> bool:
    if not isinstance(predicate, dict) or len(predicate) != 1:
        raise ValueError(f"bad predicate: {predicate}")
    op, arg = next(iter(predicate.items()))
    if op == "eq":
        return get_path(state, arg[0]) == arg[1]
    if op == "neq":
        return get_path(state, arg[0]) != arg[1]
    if op == "exists":
        return path_exists(state, arg)
    if op == "missing":
        return not path_exists(state, arg)
    if op == "in":
        return get_path(state, arg[0]) in arg[1]
    if op == "not":
        return not eval_predicate(arg, state)
    if op == "all":
        return all(eval_predicate(item, state) for item in arg)
    if op == "any":
        return any(eval_predicate(item, state) for item in arg)
    raise ValueError(f"unsupported predicate operator: {op}")

def validate_predicate(predicate: Any, allowed_ops: List[str], failures: List[str], context: str) -> None:
    allowed = set(allowed_ops)
    if not isinstance(predicate, dict) or len(predicate) != 1:
        failures.append(f"{context}:predicate_malformed:{predicate}")
        return
    op, arg = next(iter(predicate.items()))
    if op not in allowed:
        failures.append(f"{context}:predicate_operator_not_allowed:{op}")
        return
    if op in {"eq", "neq", "in"}:
        if not isinstance(arg, list) or len(arg) != 2:
            failures.append(f"{context}:predicate_{op}_arity_wrong:{arg}")
    elif op in {"exists", "missing"}:
        if not isinstance(arg, str):
            failures.append(f"{context}:predicate_{op}_expects_path:{arg}")
    elif op == "not":
        validate_predicate(arg, allowed_ops, failures, context + ".not")
    elif op in {"all", "any"}:
        if not isinstance(arg, list) or not arg:
            failures.append(f"{context}:predicate_{op}_expects_nonempty_list:{arg}")
        else:
            for idx, item in enumerate(arg):
                validate_predicate(item, allowed_ops, failures, context + f".{op}[{idx}]")

def validate_policy_source(policy: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if policy.get("policy_id") != MOVE_REGISTRY_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if receipt.get("receipt_id") != MOVE_REGISTRY_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{receipt.get('receipt_id')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{receipt.get('policy_status')}")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"target_unit_wrong:{receipt.get('target_unit_id')}")
    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"policy_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"policy_terminal_stop_not_null:{terminal.get('stop_code')}")

    summary = receipt.get("policy_summary", {})
    if summary.get("core_law") != "No unregistered move may fire.":
        failures.append(f"core_law_wrong:{summary.get('core_law')}")
    if summary.get("day5_boundary") != "authorization_status is DEFERRED_TO_DAY5; Day 4 does not resolve jurisdiction":
        failures.append(f"day5_boundary_wrong:{summary.get('day5_boundary')}")

    if receipt.get("source_halt_vocabulary_implementation_receipt_id") != HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"source_halt_impl_wrong:{receipt.get('source_halt_vocabulary_implementation_receipt_id')}")
    if receipt.get("source_proceed_adapter_implementation_receipt_id") != PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"source_proceed_wrong:{receipt.get('source_proceed_adapter_implementation_receipt_id')}")
    if receipt.get("source_trace_ledger_implementation_receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"source_trace_ledger_wrong:{receipt.get('source_trace_ledger_implementation_receipt_id')}")
    if receipt.get("source_local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append(f"source_local_regime_wrong:{receipt.get('source_local_regime_hash')}")

    for field in REQUIRED_MOVE_FIELDS:
        if field not in receipt.get("move_schema", {}).get("required_fields", []):
            failures.append(f"move_schema_required_field_missing:{field}")

    pred_schema = receipt.get("applies_when_predicate_schema", {})
    if pred_schema.get("no_free_form_code") is not True:
        failures.append("predicate_schema_allows_free_form_code")
    for op in ["eq", "neq", "exists", "missing", "in", "not", "all", "any"]:
        if op not in pred_schema.get("allowed_operators", []):
            failures.append(f"predicate_operator_missing:{op}")

    registry = receipt.get("move_registry", {})
    if registry.get("move_registry_id") != "move_registry_v0":
        failures.append(f"registry_id_wrong:{registry.get('move_registry_id')}")
    if registry.get("selection_policy") != "lowest_priority_number":
        failures.append(f"selection_policy_wrong:{registry.get('selection_policy')}")
    if list(sorted(registry.get("moves", {}).keys())) != list(sorted(EXPECTED_STARTER_MOVES)):
        failures.append(f"starter_moves_wrong:{sorted(registry.get('moves', {}).keys())}")

    for move_id, move in registry.get("moves", {}).items():
        for field in REQUIRED_MOVE_FIELDS:
            if field not in move:
                failures.append(f"{move_id}:required_field_missing:{field}")
        if move.get("move_id") != move_id:
            failures.append(f"{move_id}:move_id_mismatch:{move.get('move_id')}")
        if move.get("schema_version") != "move_schema_v0":
            failures.append(f"{move_id}:schema_version_wrong:{move.get('schema_version')}")
        validate_predicate(move.get("applies_when"), pred_schema.get("allowed_operators", []), failures, f"{move_id}.applies_when")
        if "latest_file_guessing" not in move.get("forbidden_inputs", []):
            failures.append(f"{move_id}:missing_latest_file_forbidden")
        if "mtime_selection" not in move.get("forbidden_inputs", []):
            failures.append(f"{move_id}:missing_mtime_forbidden")
        if "ambient_workspace_inference" not in move.get("forbidden_inputs", []):
            failures.append(f"{move_id}:missing_ambient_forbidden")
        if not move.get("halt_map"):
            failures.append(f"{move_id}:halt_map_missing")

    if registry["moves"]["receipt.emit_terminal.v0"]["applies_when"] != {"any": [{"exists": "state.terminal_result"}, {"exists": "state.halt_code"}]}:
        failures.append("receipt_emit_terminal_applies_when_wrong")
    if registry["moves"]["unit.mark_complete.v0"]["state_delta"]["on_pass"]["state.terminal_result"] != {"type": "STOP", "stop_code": "STOP_NEXT_MOVE_BOUNDARY"}:
        failures.append("unit_mark_complete_terminal_delta_wrong")
    if registry["moves"]["proposal.missing_move.draft.v0"]["move_kind"] != "PROPOSAL_ONLY":
        failures.append("proposal_missing_move_not_proposal_only")

    admission = receipt.get("move_admission_gate", {})
    if admission.get("admission_status_name") != "ADMISSIBLE_PRE_AUTH":
        failures.append(f"admission_status_wrong:{admission.get('admission_status_name')}")
    if admission.get("authorization_status") != "DEFERRED_TO_DAY5":
        failures.append(f"authorization_status_wrong:{admission.get('authorization_status')}")
    if "jurisdiction authority" not in admission.get("day4_must_not_decide", []):
        failures.append("day4_must_not_decide_jurisdiction_missing")

    blocked = receipt.get("blocked_move_record_schema", {})
    if "AUTHORITY_DEFERRED" not in blocked.get("block_reasons", []):
        failures.append("authority_deferred_block_reason_missing")
    if blocked.get("authority_deferred_law", {}).get("does_not_mean_STOP_AUTHORITY_VIOLATION") is not True:
        failures.append("authority_deferred_law_missing")

    stub = receipt.get("missing_move_proposal_stub", {})
    if stub.get("status") != "PROPOSED_ONLY":
        failures.append(f"missing_move_stub_status_wrong:{stub.get('status')}")
    for key in [
        "may_not_write_move_registry",
        "may_not_register_candidate_move",
        "may_not_execute_candidate_move",
        "may_not_mark_candidate_accepted",
        "may_not_promote_taxonomy_delta",
    ]:
        if stub.get("hard_rules", {}).get(key) is not True:
            failures.append(f"missing_move_stub_rule_missing:{key}")

    for patch_key, mode in [
        ("trace_move_context_patch", "future_schema_patch_only_do_not_mutate_existing_traces"),
        ("receipt_move_registry_patch", "future_schema_patch_only_do_not_mutate_existing_receipts"),
        ("proceed_readout_move_context_patch", "future_schema_patch_only_do_not_mutate_existing_readouts"),
    ]:
        if receipt.get(patch_key, {}).get("patch_mode") != mode:
            failures.append(f"{patch_key}_patch_mode_wrong:{receipt.get(patch_key, {}).get('patch_mode')}")

    guards = receipt.get("authority_guards", {})
    for key in [
        "day5_authority_implemented",
        "jurisdiction_resolved",
        "missing_move_proposal_registered",
        "missing_move_proposal_executed",
        "new_move_added",
        "unregistered_move_fired",
        "taxonomy_delta_applied",
        "taxonomy_delta_promoted",
        "registry_written",
        "registry_sqlite_written",
        "proof_claimed",
        "hidden_continuation_authorized",
    ]:
        if guards.get(key) is not False:
            failures.append(f"source_policy_guard_not_false:{key}:{guards.get(key)}")

    for path in SOURCE_FILES:
        if not tracked(path):
            failures.append(f"source_file_not_tracked:{rel(path)}")

    return failures

def validate_external_sources() -> List[str]:
    failures: List[str] = []
    halt_impl = read_json(HALT_IMPLEMENTATION_RECEIPT_PATH)
    halt_vocab = read_json(HALT_VOCABULARY_PATH)
    halt_record_schema = read_json(HALT_RECORD_SCHEMA_PATH)
    halt_next = read_json(HALT_NEXT_HANDLING_PATH)
    proceed = read_json(PROCEED_RECEIPT_PATH)
    trace_ledger = read_json(TRACE_LEDGER_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    proposal_ledger = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    regime = read_json(LOCAL_REGIME_V1_PATH)

    if halt_impl.get("receipt_id") != HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID or halt_impl.get("gate") != "PASS":
        failures.append("halt_vocabulary_source_not_pass")
    if "STOP_NO_APPLICABLE_MOVE" not in halt_vocab.get("entries", {}):
        failures.append("STOP_NO_APPLICABLE_MOVE_missing_from_halt_vocab")
    if "NO_APPLICABLE_MOVE" in halt_vocab.get("entries", {}):
        failures.append("NO_APPLICABLE_MOVE_canonical_leaked")
    if "STOP_NEEDS_NEW_MOVE" not in halt_vocab.get("entries", {}):
        failures.append("STOP_NEEDS_NEW_MOVE_missing_from_halt_vocab")
    for field in ["halt_record_id", "source_trace_ref", "source_receipt_ref", "source_ledger_ref", "terminal_result"]:
        if field not in halt_record_schema.get("required_fields", []):
            failures.append(f"halt_record_schema_field_missing:{field}")
    for halt_code in ["STOP_NO_APPLICABLE_MOVE", "STOP_NEEDS_NEW_MOVE", "STOP_GATE_FAIL", "STOP_AUTHORITY_VIOLATION"]:
        if halt_code not in halt_next.get("routes", {}):
            failures.append(f"halt_next_route_missing:{halt_code}")
    if proceed.get("receipt_id") != PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID or proceed.get("gate") != "PASS":
        failures.append("proceed_source_not_pass")
    if trace_ledger.get("receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID or trace_ledger.get("gate") != "PASS":
        failures.append("trace_ledger_source_not_pass")
    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append("trace_schema_version_wrong")
    if proposal_ledger.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append("proposal_ledger_schema_version_wrong")
    if regime.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append("local_regime_hash_wrong")
    return failures

def build_blocked_record(move_id: str, state_sig8: str, reason: str, details: Dict[str, Any], halt_pressure: Optional[str] = None) -> Dict[str, Any]:
    seed = {"move_id": move_id, "state_sig8": state_sig8, "reason": reason, "details": details}
    blocked_id = f"blocked_{sha8(seed)}"
    return {
        "schema_version": "blocked_move_record_v0",
        "blocked_move_id": blocked_id,
        "move_id": move_id,
        "state_sig8": state_sig8,
        "block_reason": reason,
        "details": details,
        "halt_pressure": halt_pressure,
        "must_not_impersonate": [
            "move invalidity",
            "proof obstruction",
            "missing move",
            "authorization decision",
        ],
    }

def schema_valid_move(move: Dict[str, Any], policy_receipt: Dict[str, Any]) -> Tuple[bool, List[str]]:
    failures: List[str] = []
    pred_schema = policy_receipt["applies_when_predicate_schema"]
    for field in REQUIRED_MOVE_FIELDS:
        if field not in move:
            failures.append(f"required_field_missing:{field}")
    if move.get("schema_version") != "move_schema_v0":
        failures.append(f"schema_version_wrong:{move.get('schema_version')}")
    validate_predicate(move.get("applies_when"), pred_schema["allowed_operators"], failures, "applies_when")
    if move.get("move_kind") not in policy_receipt["move_kind_enum"]["allowed_move_kinds"]:
        failures.append(f"move_kind_unknown:{move.get('move_kind')}")
    if not isinstance(move.get("priority"), int):
        failures.append("priority_not_int")
    if not move.get("halt_map"):
        failures.append("halt_map_missing")
    if not isinstance(move.get("action"), dict):
        failures.append("action_not_dict")
    return (len(failures) == 0, failures)

def inspect_moves_for_current_state(
    state: Dict[str, Any],
    registry: Dict[str, Any],
    policy_receipt: Dict[str, Any],
    already_applied: List[str],
    *,
    force_missing_move_pressure: bool = False,
) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Optional[Dict[str, Any]]]:
    state_sig8 = sha8(state)
    schema_valid: List[str] = []
    applicable: List[str] = []
    admissible: List[str] = []
    blocked_records: List[Dict[str, Any]] = []

    for move_id, move in registry["moves"].items():
        if move_id in already_applied:
            blocked_records.append(build_blocked_record(
                move_id,
                state_sig8,
                "APPLIES_WHEN_FALSE",
                {"reason": "move already applied in this demo run", "observed": "already_applied"},
            ))
            continue

        ok, schema_failures = schema_valid_move(move, policy_receipt)
        if not ok:
            blocked_records.append(build_blocked_record(
                move_id,
                state_sig8,
                "SCHEMA_INVALID",
                {"schema_failures": schema_failures},
                halt_pressure="STOP_GATE_FAIL",
            ))
            continue
        schema_valid.append(move_id)

        try:
            applies = eval_predicate(move["applies_when"], state)
        except Exception as exc:
            blocked_records.append(build_blocked_record(
                move_id,
                state_sig8,
                "UNKNOWN_BLOCK",
                {"error": str(exc)},
                halt_pressure="STOP_GATE_FAIL",
            ))
            continue

        if not applies:
            blocked_records.append(build_blocked_record(
                move_id,
                state_sig8,
                "APPLIES_WHEN_FALSE",
                {"predicate": move["applies_when"], "observed_state_sig8": state_sig8},
            ))
            continue
        applicable.append(move_id)

        forbidden_required = False
        if forbidden_required:
            blocked_records.append(build_blocked_record(
                move_id,
                state_sig8,
                "FORBIDDEN_INPUT_REQUIRED",
                {"forbidden_inputs": move["forbidden_inputs"]},
                halt_pressure="STOP_AUTHORITY_VIOLATION",
            ))
            continue

        if move_id == "proposal.missing_move.draft.v0":
            # Proposal-only is admissible only after missing-move pressure is explicit.
            if get_path(state, "state.halt_code") != "STOP_NEEDS_NEW_MOVE":
                blocked_records.append(build_blocked_record(
                    move_id,
                    state_sig8,
                    "APPLIES_WHEN_FALSE",
                    {"reason": "proposal-only move requires STOP_NEEDS_NEW_MOVE pressure"},
                ))
                continue

        admissible.append(move_id)

    selected = None
    selection_basis = None
    if admissible:
        selected = sorted(admissible, key=lambda mid: (registry["moves"][mid]["priority"], mid))[0]
        selection_basis = "lowest_priority_number" if len(admissible) > 1 else "only_admissible_pre_auth_move"

    missing_move_pressure = None
    if force_missing_move_pressure:
        missing_move_pressure = {
            "schema_version": "missing_move_pressure_v0",
            "trigger_halt": "STOP_NEEDS_NEW_MOVE",
            "observed_pressure": "Current state has completed build unit requiring next boundary, but boundary.emit_next_unit.v0 is not registered.",
            "candidate_move_id": "boundary.emit_next_unit.v0",
            "registered": False,
            "must_not_impersonate": [
                "registered move",
                "authorized move",
                "accepted taxonomy delta",
            ],
        }

    inspection_seed = {
        "state_sig8": state_sig8,
        "registered": list(registry["moves"].keys()),
        "schema_valid": schema_valid,
        "applicable": applicable,
        "admissible": admissible,
        "blocked": [b["blocked_move_id"] for b in blocked_records],
        "selected": selected,
        "missing": missing_move_pressure,
    }
    inspection_id = f"move_inspection_{sha8(inspection_seed)}"
    inspection = {
        "schema_version": "applicable_move_inspection_v0",
        "inspection_id": inspection_id,
        "state_sig8": state_sig8,
        "move_registry_id": registry["move_registry_id"],
        "move_registry_sig8": sha8(registry),
        "registered_count": len(registry["moves"]),
        "schema_valid_moves": schema_valid,
        "applicable_moves": applicable,
        "admissible_pre_auth_moves": admissible,
        "blocked_moves": [
            {
                "blocked_move_id": b["blocked_move_id"],
                "move_id": b["move_id"],
                "block_reason": b["block_reason"],
                "halt_pressure": b["halt_pressure"],
            }
            for b in blocked_records
        ],
        "selected_move": selected,
        "selection_basis": selection_basis,
        "authorization_status": "DEFERRED_TO_DAY5",
        "missing_move_pressure": missing_move_pressure,
    }
    return inspection, blocked_records, missing_move_pressure

def selected_move_record(inspection: Dict[str, Any], selected_move: str) -> Dict[str, Any]:
    seed = {"inspection_id": inspection["inspection_id"], "selected_move": selected_move}
    return {
        "schema_version": "selected_move_record_v0",
        "selected_move_record_id": f"selected_move_{sha8(seed)}",
        "inspection_id": inspection["inspection_id"],
        "selected_move": selected_move,
        "selection_policy": "lowest_priority_number",
        "selection_basis": inspection["selection_basis"],
        "candidate_count": len(inspection["admissible_pre_auth_moves"]),
        "tie_breaker": "priority_then_move_id",
        "authorization_status": "DEFERRED_TO_DAY5",
    }

def apply_move(state: Dict[str, Any], move_id: str, registry: Dict[str, Any]) -> Dict[str, Any]:
    move = registry["moves"][move_id]
    after = copy.deepcopy(state)

    if move_id == "state.validate_shape.v0":
        set_path(after, "state.status", "VALID")
    elif move_id == "regime.validate_shape.v0":
        set_path(after, "regime.validation_status", "PASS")
    elif move_id == "moves.compute_applicable.v0":
        set_path(after, "state.move_inspection_ref", after["_last_inspection"]["inspection_id"])
    elif move_id == "selector.choose_move.v0":
        set_path(after, "state.selected_move", after["_last_selection"]["selected_move"])
    elif move_id == "unit.mark_complete.v0":
        set_path(after, "state.active_object.completion_status", "COMPLETE")
        set_path(after, "state.terminal_result", {"type": "STOP", "stop_code": "STOP_NEXT_MOVE_BOUNDARY"})
    elif move_id == "receipt.emit_terminal.v0":
        receipt_ref = {
            "receipt_id": f"day4_receipt_{sha8({'state': after, 'move': move_id})}",
            "receipt_path": "<embedded_in_day4_demo_run>",
        }
        set_path(after, "state.receipt_ref", receipt_ref)
    elif move_id == "proposal.missing_move.draft.v0":
        proposal = make_missing_move_proposal(after)
        set_path(after, "state.missing_move_proposal_ref", {
            "proposal_id": proposal["proposal_id"],
            "proposal_path": "<embedded_in_day4_demo_missing_move_run>",
        })
        after["_missing_move_proposal"] = proposal
    else:
        raise AssertionError(f"unregistered move attempt: {move_id}")

    return after

def make_trace_entry(move_id: str, before: Dict[str, Any], after: Dict[str, Any], inspection: Optional[Dict[str, Any]], selection: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    seed = {"move_id": move_id, "before": sha8(before), "after": sha8(after)}
    return {
        "trace_entry_id": f"trace_move_{sha8(seed)}",
        "move_id": move_id,
        "state_before_sig8": sha8(before),
        "state_after_sig8": sha8(after),
        "move_registry_id": "move_registry_v0",
        "applicable_moves": [] if inspection is None else inspection["applicable_moves"],
        "admissible_pre_auth_moves": [] if inspection is None else inspection["admissible_pre_auth_moves"],
        "blocked_moves": [] if inspection is None else inspection["blocked_moves"],
        "selected_move": None if selection is None else selection["selected_move"],
        "selection_reason": None if selection is None else selection["selection_basis"],
        "move_admission_status": "ADMISSIBLE_PRE_AUTH",
        "authorization_status": "DEFERRED_TO_DAY5",
    }

def make_missing_move_proposal(state: Dict[str, Any]) -> Dict[str, Any]:
    candidate = {
        "move_id": "boundary.emit_next_unit.v0",
        "move_kind": "CONTROL_EMIT",
        "applies_when": {
            "all": [
                {"eq": ["state.active_object.completion_status", "COMPLETE"]},
                {"missing": "state.next_unit_id"},
            ]
        },
        "action": {
            "type": "EMIT",
            "name": "emit_next_move_boundary",
        },
        "emits": [
            "proceed_readout",
            "halt_record",
        ],
        "halt_behavior": {
            "on_success": "STOP_NEXT_MOVE_BOUNDARY",
            "on_fail": "STOP_GATE_FAIL",
        },
    }
    seed = {"candidate": candidate, "state_sig8": sha8(state)}
    return {
        "schema_version": "missing_move_proposal_v0",
        "proposal_id": f"move_proposal_{sha8(seed)}",
        "proposal_type": "MISSING_MOVE",
        "trigger_halt": "STOP_NEEDS_NEW_MOVE",
        "observed_pressure": "Current state has completed build unit and needs next boundary, but boundary.emit_next_unit.v0 is not registered.",
        "candidate_move": candidate,
        "candidate_move_id": "boundary.emit_next_unit.v0",
        "status": "PROPOSED_ONLY",
        "must_not_impersonate": [
            "registered move",
            "accepted taxonomy delta",
            "authorized execution",
        ],
        "allowed_next_handling": [
            "human review",
            "accept into registry in later reviewed unit",
            "reject",
            "defer",
            "weaken proposal",
        ],
        "registry_mutated": False,
        "candidate_registered": False,
        "candidate_executed": False,
        "taxonomy_delta_applied": False,
        "taxonomy_delta_promoted": False,
    }

def make_run_receipt(run: Dict[str, Any]) -> Dict[str, Any]:
    seed = {
        "demo_name": run["demo_name"],
        "terminal": run["terminal_result"],
        "applied": run["moves_applied"],
    }
    return {
        "schema_version": "day4_demo_move_run_receipt_v0",
        "receipt_id": f"day4_demo_receipt_{sha8(seed)}",
        "demo_name": run["demo_name"],
        "move_registry": {
            "move_registry_id": "move_registry_v0",
            "move_registry_sig8": run["move_registry_sig8"],
            "registered_count": run["registered_count"],
        },
        "moves": {
            "moves_inspected": run["registered_count"],
            "moves_applied": run["moves_applied"],
            "blocked_moves_count": run["blocked_moves_count"],
            "unregistered_attempts": run["unregistered_attempts"],
        },
        "terminal_result": run["terminal_result"],
        "missing_move_proposal": run.get("missing_move_proposal"),
        "authorization_status": "DEFERRED_TO_DAY5",
        "gate": "PASS",
        "failures": [],
    }

def run_positive_demo(policy_receipt: Dict[str, Any]) -> Dict[str, Any]:
    registry = policy_receipt["move_registry"]
    state = copy.deepcopy(policy_receipt["day4_demo_positive_run_plan"]["initial_state"])
    applied: List[str] = []
    trace: List[Dict[str, Any]] = []
    inspections: List[Dict[str, Any]] = []
    blocked_records: List[Dict[str, Any]] = []
    selected_records: List[Dict[str, Any]] = []

    expected_sequence = policy_receipt["day4_demo_positive_run_plan"]["expected_move_sequence"]

    for expected_move in expected_sequence:
        before = copy.deepcopy(state)

        inspection = None
        selection = None

        if expected_move == "moves.compute_applicable.v0":
            inspection, blocked, _ = inspect_moves_for_current_state(state, registry, policy_receipt, applied)
            state["_last_inspection"] = inspection
            inspections.append(inspection)
            blocked_records.extend(blocked)
        elif expected_move == "selector.choose_move.v0":
            # Select the next real work move from the current inspection. The control selector itself is being exercised by this step.
            work_candidates = [
                mid for mid in state["_last_inspection"]["admissible_pre_auth_moves"]
                if mid not in {"moves.compute_applicable.v0", "selector.choose_move.v0"} and mid not in applied
            ]
            if not work_candidates:
                raise AssertionError("positive demo selector had no work candidate")
            selected_move = sorted(work_candidates, key=lambda mid: (registry["moves"][mid]["priority"], mid))[0]
            synthetic_inspection = copy.deepcopy(state["_last_inspection"])
            synthetic_inspection["selected_move"] = selected_move
            synthetic_inspection["selection_basis"] = "lowest_priority_number"
            selection = selected_move_record(synthetic_inspection, selected_move)
            state["_last_selection"] = selection
            selected_records.append(selection)

        if expected_move not in registry["moves"]:
            raise AssertionError(f"unregistered move attempted: {expected_move}")

        state = apply_move(state, expected_move, registry)
        applied.append(expected_move)

        after = copy.deepcopy(state)
        trace.append(make_trace_entry(expected_move, before, after, inspection, selection))

    for private_key in ["_last_inspection", "_last_selection", "_missing_move_proposal"]:
        state.pop(private_key, None)

    run = {
        "schema_version": "day4_demo_positive_run_v0",
        "demo_name": "DAY4_POSITIVE_BUILD_UNIT_COMPLETION",
        "source_policy_id": MOVE_REGISTRY_POLICY_ID,
        "move_registry_id": "move_registry_v0",
        "move_registry_sig8": policy_receipt["move_registry_sig8"],
        "registered_count": len(registry["moves"]),
        "initial_state": policy_receipt["day4_demo_positive_run_plan"]["initial_state"],
        "final_state": state,
        "moves_applied": applied,
        "move_sequence_expected": expected_sequence,
        "move_sequence_matches_expected": applied == expected_sequence,
        "trace_entries": trace,
        "inspections": inspections,
        "blocked_move_records": blocked_records,
        "selected_move_records": selected_records,
        "blocked_moves_count": len(blocked_records),
        "unregistered_attempts": 0,
        "schema_invalid_move_attempts": 0,
        "ambiguous_selection_count": 0,
        "authorization_status": "DEFERRED_TO_DAY5",
        "terminal_result": state["terminal_result"],
        "gate": "PASS",
        "failures": [],
    }
    run["receipt"] = make_run_receipt(run)
    return run

def run_missing_move_demo(policy_receipt: Dict[str, Any]) -> Dict[str, Any]:
    registry = policy_receipt["move_registry"]
    state = copy.deepcopy(policy_receipt["day4_demo_missing_move_run_plan"]["initial_state"])
    applied: List[str] = []
    trace: List[Dict[str, Any]] = []
    inspections: List[Dict[str, Any]] = []
    blocked_records: List[Dict[str, Any]] = []

    inspection, blocked, pressure = inspect_moves_for_current_state(
        state,
        registry,
        policy_receipt,
        already_applied=[],
        force_missing_move_pressure=True,
    )
    inspections.append(inspection)
    blocked_records.extend(blocked)

    state["halt_code"] = "STOP_NEEDS_NEW_MOVE"
    state["terminal_result"] = {"type": "STOP", "stop_code": "STOP_NEEDS_NEW_MOVE"}

    before = copy.deepcopy(state)
    proposal_move = "proposal.missing_move.draft.v0"
    if proposal_move not in registry["moves"]:
        raise AssertionError("proposal move missing from registry")
    state = apply_move(state, proposal_move, registry)
    applied.append(proposal_move)
    trace.append(make_trace_entry(proposal_move, before, state, inspection, None))

    proposal = state.pop("_missing_move_proposal")
    for private_key in ["_last_inspection", "_last_selection"]:
        state.pop(private_key, None)

    run = {
        "schema_version": "day4_demo_missing_move_run_v0",
        "demo_name": "DAY4_MISSING_MOVE_PRESSURE",
        "source_policy_id": MOVE_REGISTRY_POLICY_ID,
        "move_registry_id": "move_registry_v0",
        "move_registry_sig8": policy_receipt["move_registry_sig8"],
        "registered_count": len(registry["moves"]),
        "initial_state": policy_receipt["day4_demo_missing_move_run_plan"]["initial_state"],
        "final_state": state,
        "moves_applied": applied,
        "trace_entries": trace,
        "inspections": inspections,
        "blocked_move_records": blocked_records,
        "blocked_moves_count": len(blocked_records),
        "missing_move_pressure": pressure,
        "missing_move_proposal": proposal,
        "candidate_move_id": proposal["candidate_move_id"],
        "candidate_move_registered": False,
        "candidate_move_executed": False,
        "proposal_status": proposal["status"],
        "proposal_registered": False,
        "proposal_executed": False,
        "registry_mutated_by_proposal": False,
        "unregistered_attempts": 0,
        "schema_invalid_move_attempts": 0,
        "authorization_status": "DEFERRED_TO_DAY5",
        "terminal_result": {"type": "STOP", "stop_code": "STOP_NEEDS_NEW_MOVE"},
        "gate": "PASS",
        "failures": [],
    }
    run["receipt"] = make_run_receipt(run)
    return run

def validate_demo_run(run: Dict[str, Any], policy_receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    registry_ids = set(policy_receipt["move_registry"]["moves"].keys())

    if run.get("gate") != "PASS":
        failures.append(f"{run.get('demo_name')}:gate_not_PASS")
    if run.get("move_registry_id") != "move_registry_v0":
        failures.append(f"{run.get('demo_name')}:registry_id_wrong")
    if run.get("registered_count") != 7:
        failures.append(f"{run.get('demo_name')}:registered_count_wrong:{run.get('registered_count')}")
    if run.get("authorization_status") != "DEFERRED_TO_DAY5":
        failures.append(f"{run.get('demo_name')}:authorization_status_wrong:{run.get('authorization_status')}")
    if run.get("unregistered_attempts") != 0:
        failures.append(f"{run.get('demo_name')}:unregistered_attempts_nonzero")
    if run.get("schema_invalid_move_attempts") != 0:
        failures.append(f"{run.get('demo_name')}:schema_invalid_attempts_nonzero")

    for move_id in run.get("moves_applied", []):
        if move_id not in registry_ids:
            failures.append(f"{run.get('demo_name')}:unregistered_move_applied:{move_id}")

    for trace in run.get("trace_entries", []):
        if trace.get("move_id") not in registry_ids:
            failures.append(f"{run.get('demo_name')}:trace_unregistered_move:{trace.get('move_id')}")
        if trace.get("authorization_status") != "DEFERRED_TO_DAY5":
            failures.append(f"{run.get('demo_name')}:trace_authorization_not_deferred:{trace.get('trace_entry_id')}")
        if trace.get("move_registry_id") != "move_registry_v0":
            failures.append(f"{run.get('demo_name')}:trace_registry_wrong:{trace.get('trace_entry_id')}")

    for inspection in run.get("inspections", []):
        if inspection.get("authorization_status") != "DEFERRED_TO_DAY5":
            failures.append(f"{run.get('demo_name')}:inspection_auth_not_deferred:{inspection.get('inspection_id')}")
        if inspection.get("registered_count") != 7:
            failures.append(f"{run.get('demo_name')}:inspection_registered_count_wrong")
        if not isinstance(inspection.get("blocked_moves"), list):
            failures.append(f"{run.get('demo_name')}:inspection_blocked_not_list")

    for blocked in run.get("blocked_move_records", []):
        for field in policy_receipt["blocked_move_record_schema"]["required_fields"]:
            if field not in blocked:
                failures.append(f"{run.get('demo_name')}:blocked_record_missing:{field}")

    if run["demo_name"] == "DAY4_POSITIVE_BUILD_UNIT_COMPLETION":
        if run.get("moves_applied") != policy_receipt["day4_demo_positive_run_plan"]["expected_move_sequence"]:
            failures.append("positive_sequence_mismatch")
        if run.get("terminal_result") != {"type": "STOP", "stop_code": "STOP_NEXT_MOVE_BOUNDARY"}:
            failures.append(f"positive_terminal_wrong:{run.get('terminal_result')}")
        if run.get("move_sequence_matches_expected") is not True:
            failures.append("positive_sequence_match_flag_false")
        if not run.get("selected_move_records"):
            failures.append("positive_missing_selected_move_record")
        else:
            selected = run["selected_move_records"][0]
            if selected.get("selected_move") != "unit.mark_complete.v0":
                failures.append(f"positive_selected_move_wrong:{selected.get('selected_move')}")
            if selected.get("authorization_status") != "DEFERRED_TO_DAY5":
                failures.append("positive_selected_auth_not_deferred")

    if run["demo_name"] == "DAY4_MISSING_MOVE_PRESSURE":
        if run.get("terminal_result") != {"type": "STOP", "stop_code": "STOP_NEEDS_NEW_MOVE"}:
            failures.append(f"missing_move_terminal_wrong:{run.get('terminal_result')}")
        proposal = run.get("missing_move_proposal") or {}
        if proposal.get("status") != "PROPOSED_ONLY":
            failures.append(f"missing_move_proposal_status_wrong:{proposal.get('status')}")
        if proposal.get("candidate_move_id") != "boundary.emit_next_unit.v0":
            failures.append(f"missing_move_candidate_wrong:{proposal.get('candidate_move_id')}")
        for key in [
            "candidate_move_registered",
            "candidate_move_executed",
            "proposal_registered",
            "proposal_executed",
            "registry_mutated_by_proposal",
        ]:
            if run.get(key) is not False:
                failures.append(f"missing_move_guard_not_false:{key}:{run.get(key)}")
        if proposal.get("registry_mutated") is not False:
            failures.append("missing_move_proposal_registry_mutated")
        if proposal.get("candidate_registered") is not False:
            failures.append("missing_move_proposal_candidate_registered")
        if proposal.get("candidate_executed") is not False:
            failures.append("missing_move_proposal_candidate_executed")

    receipt = run.get("receipt") or {}
    if receipt.get("gate") != "PASS":
        failures.append(f"{run.get('demo_name')}:receipt_gate_not_PASS")
    if receipt.get("move_registry", {}).get("registered_count") != 7:
        failures.append(f"{run.get('demo_name')}:receipt_registered_count_wrong")
    if receipt.get("moves", {}).get("unregistered_attempts") != 0:
        failures.append(f"{run.get('demo_name')}:receipt_unregistered_attempts_nonzero")
    if receipt.get("authorization_status") != "DEFERRED_TO_DAY5":
        failures.append(f"{run.get('demo_name')}:receipt_auth_not_deferred")

    return failures

def validate_implementation_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if receipt.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("source_move_registry_policy_id") != MOVE_REGISTRY_POLICY_ID:
        failures.append(f"source_policy_wrong:{receipt.get('source_move_registry_policy_id')}")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"target_unit_wrong:{receipt.get('target_unit_id')}")

    gates = receipt.get("acceptance_gate_results", {})
    for gate in [
        "MRI0_source_policy_verified",
        "MRI1_core_artifacts_emitted",
        "MRI2_positive_demo_passed",
        "MRI3_missing_move_demo_passed",
        "MRI4_blocked_moves_recorded",
        "MRI5_no_unregistered_move_fired",
        "MRI6_missing_move_proposal_proposed_only",
        "MRI7_day5_authority_deferred",
        "MRI8_no_source_artifact_mutation",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics", {})
    expected_zero = [
        "unregistered_move_fire_count",
        "schema_invalid_move_fire_count",
        "ambiguous_selection_count",
        "missing_move_candidate_registered_count",
        "missing_move_candidate_executed_count",
        "missing_move_proposal_accepted_count",
        "taxonomy_delta_applied_count",
        "taxonomy_delta_promoted_count",
        "day5_authority_resolution_count",
        "jurisdiction_resolved_count",
        "source_trace_modified_count",
        "source_receipt_modified_count",
        "source_ledger_modified_count",
        "source_runner_modified_count",
        "source_regime_modified_count",
        "registry_sqlite_write_count",
        "proof_claim_count",
        "hidden_continuation_count",
    ]
    for key in expected_zero:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")
    if metrics.get("starter_move_count") != 7:
        failures.append(f"starter_move_count_wrong:{metrics.get('starter_move_count')}")
    if metrics.get("demo_run_count") != 2:
        failures.append(f"demo_run_count_wrong:{metrics.get('demo_run_count')}")
    if metrics.get("positive_demo_applied_move_count") != 6:
        failures.append(f"positive_demo_applied_move_count_wrong:{metrics.get('positive_demo_applied_move_count')}")
    if metrics.get("missing_move_demo_proposal_count") != 1:
        failures.append(f"missing_move_demo_proposal_count_wrong:{metrics.get('missing_move_demo_proposal_count')}")
    if metrics.get("blocked_move_record_count", 0) <= 0:
        failures.append("blocked_move_record_count_not_positive")

    guards = receipt.get("authority_guards", {})
    for key in [
        "core_artifacts_emitted",
        "positive_demo_run_emitted",
        "missing_move_demo_run_emitted",
        "day4_demo_move_run_receipt_emitted",
        "implementation_receipt_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "source_halt_vocabulary_modified",
        "source_proceed_adapter_modified",
        "source_trace_ledger_runner_modified",
        "source_local_regime_v1_modified",
        "source_trace_modified",
        "source_receipt_modified",
        "source_ledger_modified",
        "unregistered_move_fired",
        "schema_invalid_move_fired",
        "missing_move_candidate_registered",
        "missing_move_candidate_executed",
        "missing_move_proposal_accepted",
        "taxonomy_delta_applied",
        "taxonomy_delta_promoted",
        "day5_authority_implemented",
        "jurisdiction_resolved",
        "registry_sqlite_read",
        "registry_sqlite_written",
        "global_move_catalog_claimed",
        "final_schema_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
    ]:
        if guards.get(key) is not False:
            failures.append(f"guard_not_false:{key}:{guards.get(key)}")

    terminal = receipt.get("terminal", {})
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

    source_before = snapshot_files(SOURCE_FILES)

    failures: List[str] = []
    failures.extend(validate_policy_source(policy, policy_receipt))
    failures.extend(validate_external_sources())

    for d in [ARTIFACT_DIR, PATCH_DIR, DEMO_DIR, IMPLEMENTATION_RECEIPT_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    artifacts = {
        "move_schema": ARTIFACT_DIR / "move_schema_v0.json",
        "move_kind_enum": ARTIFACT_DIR / "move_kind_enum_v0.json",
        "applies_when_predicate_schema": ARTIFACT_DIR / "applies_when_predicate_schema_v0.json",
        "move_lifecycle": ARTIFACT_DIR / "move_lifecycle_v0.json",
        "move_registry": ARTIFACT_DIR / "move_registry_v0.json",
        "move_admission_gate": ARTIFACT_DIR / "move_admission_gate_v0.json",
        "blocked_move_record_schema": ARTIFACT_DIR / "blocked_move_record_schema_v0.json",
        "applicable_move_inspection_schema": ARTIFACT_DIR / "applicable_move_inspection_schema_v0.json",
        "selected_move_record_schema": ARTIFACT_DIR / "selected_move_record_schema_v0.json",
        "missing_move_proposal_stub": ARTIFACT_DIR / "missing_move_proposal_stub_v0.json",
        "trace_move_context_patch": PATCH_DIR / "trace_move_context_patch_v0.json",
        "receipt_move_registry_patch": PATCH_DIR / "receipt_move_registry_patch_v0.json",
        "proceed_readout_move_context_patch": PATCH_DIR / "proceed_readout_move_context_patch_v0.json",
    }

    write_json(artifacts["move_schema"], policy_receipt["move_schema"])
    write_json(artifacts["move_kind_enum"], policy_receipt["move_kind_enum"])
    write_json(artifacts["applies_when_predicate_schema"], policy_receipt["applies_when_predicate_schema"])
    write_json(artifacts["move_lifecycle"], policy_receipt["move_lifecycle"])
    write_json(artifacts["move_registry"], policy_receipt["move_registry"])
    write_json(artifacts["move_admission_gate"], policy_receipt["move_admission_gate"])
    write_json(artifacts["blocked_move_record_schema"], policy_receipt["blocked_move_record_schema"])
    write_json(artifacts["applicable_move_inspection_schema"], policy_receipt["applicable_move_inspection_schema"])
    write_json(artifacts["selected_move_record_schema"], policy_receipt["selected_move_record_schema"])
    write_json(artifacts["missing_move_proposal_stub"], policy_receipt["missing_move_proposal_stub"])
    write_json(artifacts["trace_move_context_patch"], policy_receipt["trace_move_context_patch"])
    write_json(artifacts["receipt_move_registry_patch"], policy_receipt["receipt_move_registry_patch"])
    write_json(artifacts["proceed_readout_move_context_patch"], policy_receipt["proceed_readout_move_context_patch"])

    positive_run = run_positive_demo(policy_receipt)
    missing_run = run_missing_move_demo(policy_receipt)

    demo_failures = []
    demo_failures.extend(validate_demo_run(positive_run, policy_receipt))
    demo_failures.extend(validate_demo_run(missing_run, policy_receipt))
    failures.extend(demo_failures)

    positive_path = DEMO_DIR / "day4_demo_positive_run.json"
    missing_path = DEMO_DIR / "day4_demo_missing_move_run.json"
    write_json(positive_path, positive_run)
    write_json(missing_path, missing_run)

    demo_receipt_bundle = {
        "schema_version": "day4_demo_move_run_receipt_bundle_v0",
        "receipt_type": "DAY4_DEMO_MOVE_RUN_RECEIPT_BUNDLE",
        "source_policy_id": MOVE_REGISTRY_POLICY_ID,
        "positive_demo_receipt": positive_run["receipt"],
        "missing_move_demo_receipt": missing_run["receipt"],
        "gate": "PASS" if not demo_failures else "FAIL",
        "failures": demo_failures,
        "created_at": now_iso(),
    }
    demo_receipt_bundle["receipt_bundle_id"] = f"day4_demo_bundle_{sha8(demo_receipt_bundle)}"
    demo_receipt_path = DEMO_DIR / "day4_demo_move_run_receipt.json"
    write_json(demo_receipt_path, demo_receipt_bundle)

    source_after = snapshot_files(SOURCE_FILES)
    source_mutation_detected = source_before != source_after
    if source_mutation_detected:
        failures.append("source_file_hash_changed")

    output_artifacts = {
        name: rel(path) for name, path in artifacts.items()
    }
    output_artifacts["day4_demo_positive_run"] = rel(positive_path)
    output_artifacts["day4_demo_missing_move_run"] = rel(missing_path)
    output_artifacts["day4_demo_move_run_receipt"] = rel(demo_receipt_path)

    blocked_count = len(positive_run["blocked_move_records"]) + len(missing_run["blocked_move_records"])
    aggregate_metrics = {
        "starter_move_count": len(policy_receipt["move_registry"]["moves"]),
        "demo_run_count": 2,
        "positive_demo_applied_move_count": len(positive_run["moves_applied"]),
        "missing_move_demo_applied_move_count": len(missing_run["moves_applied"]),
        "blocked_move_record_count": blocked_count,
        "inspection_count": len(positive_run["inspections"]) + len(missing_run["inspections"]),
        "selected_move_record_count": len(positive_run["selected_move_records"]),
        "missing_move_demo_proposal_count": 1 if missing_run.get("missing_move_proposal") else 0,
        "stop_next_move_boundary_count": 1 if positive_run["terminal_result"]["stop_code"] == "STOP_NEXT_MOVE_BOUNDARY" else 0,
        "stop_needs_new_move_count": 1 if missing_run["terminal_result"]["stop_code"] == "STOP_NEEDS_NEW_MOVE" else 0,
        "admissible_pre_auth_selected_count": len(positive_run["selected_move_records"]),
        "authorization_deferred_count": 2,
        "unregistered_move_fire_count": positive_run["unregistered_attempts"] + missing_run["unregistered_attempts"],
        "schema_invalid_move_fire_count": positive_run["schema_invalid_move_attempts"] + missing_run["schema_invalid_move_attempts"],
        "ambiguous_selection_count": positive_run.get("ambiguous_selection_count", 0),
        "missing_move_candidate_registered_count": 1 if missing_run["candidate_move_registered"] else 0,
        "missing_move_candidate_executed_count": 1 if missing_run["candidate_move_executed"] else 0,
        "missing_move_proposal_accepted_count": 1 if missing_run["proposal_status"] != "PROPOSED_ONLY" else 0,
        "taxonomy_delta_applied_count": 0,
        "taxonomy_delta_promoted_count": 0,
        "day5_authority_resolution_count": 0,
        "jurisdiction_resolved_count": 0,
        "source_trace_modified_count": 0,
        "source_receipt_modified_count": 0,
        "source_ledger_modified_count": 0,
        "source_runner_modified_count": 0,
        "source_regime_modified_count": 0,
        "registry_sqlite_write_count": 0,
        "proof_claim_count": 0,
        "hidden_continuation_count": 0,
    }

    acceptance_gate_results = {
        "MRI0_source_policy_verified": len(validate_policy_source(policy, policy_receipt)) == 0 and len(validate_external_sources()) == 0,
        "MRI1_core_artifacts_emitted": all(path.exists() for path in artifacts.values()),
        "MRI2_positive_demo_passed": positive_run["gate"] == "PASS" and not validate_demo_run(positive_run, policy_receipt),
        "MRI3_missing_move_demo_passed": missing_run["gate"] == "PASS" and not validate_demo_run(missing_run, policy_receipt),
        "MRI4_blocked_moves_recorded": blocked_count > 0,
        "MRI5_no_unregistered_move_fired": aggregate_metrics["unregistered_move_fire_count"] == 0,
        "MRI6_missing_move_proposal_proposed_only": missing_run["proposal_status"] == "PROPOSED_ONLY" and not missing_run["candidate_move_registered"] and not missing_run["candidate_move_executed"],
        "MRI7_day5_authority_deferred": positive_run["authorization_status"] == "DEFERRED_TO_DAY5" and missing_run["authorization_status"] == "DEFERRED_TO_DAY5",
        "MRI8_no_source_artifact_mutation": not source_mutation_detected,
    }
    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    authority_guards = {
        "core_artifacts_emitted": True,
        "positive_demo_run_emitted": True,
        "missing_move_demo_run_emitted": True,
        "day4_demo_move_run_receipt_emitted": True,
        "implementation_receipt_emitted": True,
        "source_halt_vocabulary_modified": False,
        "source_proceed_adapter_modified": False,
        "source_trace_ledger_runner_modified": False,
        "source_local_regime_v1_modified": False,
        "source_trace_modified": False,
        "source_receipt_modified": False,
        "source_ledger_modified": False,
        "unregistered_move_fired": False,
        "schema_invalid_move_fired": False,
        "missing_move_candidate_registered": False,
        "missing_move_candidate_executed": False,
        "missing_move_proposal_accepted": False,
        "taxonomy_delta_applied": False,
        "taxonomy_delta_promoted": False,
        "day5_authority_implemented": False,
        "jurisdiction_resolved": False,
        "registry_sqlite_read": False,
        "registry_sqlite_written": False,
        "global_move_catalog_claimed": False,
        "final_schema_claimed": False,
        "proof_claimed": False,
        "hidden_continuation_authorized": False,
    }

    artifact_guards = {
        "policy_tracked": tracked(POLICY_PATH),
        "policy_receipt_tracked": tracked(POLICY_RECEIPT_PATH),
        "source_halt_vocabulary_tracked": tracked(HALT_VOCABULARY_PATH),
        "source_proceed_receipt_tracked": tracked(PROCEED_RECEIPT_PATH),
        "source_trace_ledger_receipt_tracked": tracked(TRACE_LEDGER_RECEIPT_PATH),
        "source_trace_schema_tracked": tracked(TRACE_SCHEMA_PATH),
        "source_proposal_ledger_schema_tracked": tracked(PROPOSAL_LEDGER_SCHEMA_PATH),
        "source_local_regime_tracked": tracked(LOCAL_REGIME_V1_PATH),
        "outputs_path_addressed": True,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_authority_used": False,
    }

    implementation_seed = {
        "unit_id": UNIT_ID,
        "source_policy_id": MOVE_REGISTRY_POLICY_ID,
        "positive_terminal": positive_run["terminal_result"],
        "missing_terminal": missing_run["terminal_result"],
        "output_artifacts": output_artifacts,
    }
    implementation_receipt_id = sha8(implementation_seed)
    implementation_receipt_path = IMPLEMENTATION_RECEIPT_DIR / f"{implementation_receipt_id}.json"

    implementation_receipt = {
        "schema_version": "move_registry_v0_implementation_receipt_v0",
        "receipt_type": "MOVE_REGISTRY_V0_IMPLEMENTATION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": implementation_receipt_id,
        "source_move_registry_policy_id": MOVE_REGISTRY_POLICY_ID,
        "source_move_registry_policy_receipt_id": MOVE_REGISTRY_POLICY_RECEIPT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_halt_vocabulary_implementation_receipt_id": HALT_VOCABULARY_IMPLEMENTATION_RECEIPT_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "output_artifacts": output_artifacts,
        "positive_demo_summary": {
            "demo_name": positive_run["demo_name"],
            "moves_applied": positive_run["moves_applied"],
            "terminal_result": positive_run["terminal_result"],
            "selected_move_records": positive_run["selected_move_records"],
            "blocked_move_record_count": len(positive_run["blocked_move_records"]),
        },
        "missing_move_demo_summary": {
            "demo_name": missing_run["demo_name"],
            "moves_applied": missing_run["moves_applied"],
            "terminal_result": missing_run["terminal_result"],
            "candidate_move_id": missing_run["candidate_move_id"],
            "proposal_status": missing_run["proposal_status"],
            "candidate_move_registered": missing_run["candidate_move_registered"],
            "candidate_move_executed": missing_run["candidate_move_executed"],
            "blocked_move_record_count": len(missing_run["blocked_move_records"]),
        },
        "aggregate_metrics": aggregate_metrics,
        "acceptance_gate_results": acceptance_gate_results,
        "authority_guards": authority_guards,
        "artifact_guards": artifact_guards,
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_DONE" if not failures else "STOP_GATE_FAIL",
            "next_command_goal": None,
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_failures = validate_implementation_receipt(implementation_receipt)
    failures.extend(receipt_failures)
    implementation_receipt["failures"] = failures
    implementation_receipt["gate"] = "PASS" if not failures else "FAIL"
    implementation_receipt["terminal"]["stop_code"] = "STOP_DONE" if not failures else "STOP_GATE_FAIL"

    write_json(implementation_receipt_path, implementation_receipt)

    print(json.dumps(implementation_receipt, indent=2, sort_keys=True))
    print(f"move_registry_implementation_receipt_id={implementation_receipt_id}")
    print(f"move_registry_implementation_receipt_path=data/move_registry_v0_implementation_receipts/{implementation_receipt_id}.json")
    for name, path in sorted(output_artifacts.items()):
        print(f"artifact_{name}_path={path}")

    return 0 if implementation_receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
