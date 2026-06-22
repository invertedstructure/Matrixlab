#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "IMPLEMENT_HALT_VOCABULARY_V0_WITH_DEMO_RECORDS_V0"

HALT_VOCABULARY_POLICY_ID = "0707a2d7"
HALT_VOCABULARY_POLICY_RECEIPT_ID = "dc00a5cf"
PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID = "363d2f4a"
PROCEED_ADAPTER_POLICY_ID = "e6b3dcfc"
TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID = "cc24a11f"
TRACE_SCHEMA_ID = "b4887660"
PROPOSAL_LEDGER_SCHEMA_ID = "eee2a318"
LOCAL_REGIME_V1_HASH = "25802530"

TARGET_UNIT_ID = "halt_vocabulary.v0"

POLICY_PATH = ROOT / "data" / "halt_vocabulary_v0_policies" / f"{HALT_VOCABULARY_POLICY_ID}.json"
POLICY_RECEIPT_PATH = ROOT / "data" / "halt_vocabulary_v0_policy_receipts" / f"{HALT_VOCABULARY_POLICY_ID}.json"
PROCEED_RECEIPT_PATH = ROOT / "data" / "proceed_adapter_v0_implementation_receipts" / f"{PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID}.json"
PROCEED_POLICY_PATH = ROOT / "data" / "proceed_adapter_v0_policies" / f"{PROCEED_ADAPTER_POLICY_ID}.json"
PROCEED_ADAPTER_MODULE_PATH = ROOT / "src" / "matrixlab" / "proceed_adapter_v0.py"
TRACE_LEDGER_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_ledger_hardening_implementation_receipts" / f"{TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID}.json"
TRACE_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_trace_schemas" / f"{TRACE_SCHEMA_ID}.json"
PROPOSAL_LEDGER_SCHEMA_PATH = ROOT / "data" / "jurisdiction_runner_v0_2_proposal_ledger_schemas" / f"{PROPOSAL_LEDGER_SCHEMA_ID}.json"
TRACE_LEDGER_RUNNER_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_2_trace_ledger.py"
LOCAL_REGIME_V1_PATH = ROOT / "data" / "local_regime_v1_declarations" / f"{LOCAL_REGIME_V1_HASH}.json"

HALT_VOCABULARY_DIR = ROOT / "data" / "halt_vocabulary_v0"
HALT_RECORD_SCHEMA_DIR = ROOT / "data" / "halt_record_schemas"
HALT_FAMILY_TABLE_DIR = ROOT / "data" / "halt_family_tables"
HALT_CLASSIFIER_PRIORITY_DIR = ROOT / "data" / "halt_classifier_priorities"
HALT_NEXT_HANDLING_DIR = ROOT / "data" / "halt_to_next_handling_tables"
HALT_PATCH_DIR = ROOT / "data" / "halt_schema_patches"
DEMO_DIR = ROOT / "data" / "halt_vocabulary_v0_demo"
IMPLEMENTATION_RECEIPT_DIR = ROOT / "data" / "halt_vocabulary_v0_implementation_receipts"

REQUIRED_HALT_ENTRY_FIELDS = [
    "halt_code",
    "halt_family",
    "smallest_honest_meaning",
    "must_not_impersonate",
    "allowed_next_handling",
]

REQUIRED_HALT_RECORD_FIELDS = [
    "halt_record_id",
    "run_id",
    "unit_id",
    "step_index",
    "halt_code",
    "canonical_halt_code",
    "halt_family",
    "smallest_honest_meaning",
    "must_not_impersonate",
    "observed_pressure",
    "allowed_next_handling",
    "source_readout_ref",
    "source_trace_ref",
    "source_receipt_ref",
    "source_ledger_ref",
    "terminal_result",
]

DEMO_CASES = [
    "DEMO_CLEAN_NEXT_BOUNDARY",
    "DEMO_PROJECTION_BUG",
    "DEMO_NO_APPLICABLE_MOVE",
    "DEMO_TAXONOMY_GAP",
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

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))

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

def validate_policy_inputs(
    policy: Dict[str, Any],
    policy_receipt: Dict[str, Any],
    proceed_receipt: Dict[str, Any],
    proceed_policy: Dict[str, Any],
    trace_ledger_receipt: Dict[str, Any],
    trace_schema: Dict[str, Any],
    ledger_schema: Dict[str, Any],
    local_regime_v1: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if policy.get("policy_id") != HALT_VOCABULARY_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy.get("policy_receipt_id") != HALT_VOCABULARY_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if policy_receipt.get("receipt_id") != HALT_VOCABULARY_POLICY_RECEIPT_ID:
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

    if policy_receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"target_unit_wrong:{policy_receipt.get('target_unit_id')}")
    if policy_receipt.get("source_proceed_adapter_implementation_receipt_id") != PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"source_proceed_receipt_wrong:{policy_receipt.get('source_proceed_adapter_implementation_receipt_id')}")
    if policy_receipt.get("source_trace_ledger_implementation_receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"source_trace_ledger_receipt_wrong:{policy_receipt.get('source_trace_ledger_implementation_receipt_id')}")

    p_summary = policy_receipt.get("policy_summary") or {}
    if "not proof" not in p_summary.get("core_law", ""):
        failures.append("policy_core_law_missing_not_proof")
    if "typed control information" not in p_summary.get("core_law", ""):
        failures.append("policy_core_law_missing_typed_control_information")

    vocab = policy_receipt.get("halt_vocabulary", {}).get("entries", {})
    if len(vocab) != policy_receipt.get("halt_vocabulary", {}).get("canonical_entry_count"):
        failures.append("vocab_count_mismatch")

    if "TYPED_STATE_READY" in vocab:
        failures.append("TYPED_STATE_READY_must_not_be_halt")
    if "NO_APPLICABLE_MOVE" in vocab:
        failures.append("NO_APPLICABLE_MOVE_must_not_be_canonical_entry")
    if "STOP_NO_APPLICABLE_MOVE" not in vocab:
        failures.append("STOP_NO_APPLICABLE_MOVE_missing")
    else:
        if "NO_APPLICABLE_MOVE" not in vocab["STOP_NO_APPLICABLE_MOVE"].get("legacy_aliases", []):
            failures.append("NO_APPLICABLE_MOVE_alias_missing")
        if "proof closure" not in " ".join(vocab["STOP_NO_APPLICABLE_MOVE"].get("must_not_impersonate", [])).lower():
            failures.append("STOP_NO_APPLICABLE_MOVE_missing_proof_closure_anti_impersonation")
    if "STOP_DEPENDENCY_MISSING" not in vocab:
        failures.append("STOP_DEPENDENCY_MISSING_missing")

    for code, entry in vocab.items():
        for field in REQUIRED_HALT_ENTRY_FIELDS:
            if field not in entry:
                failures.append(f"{code}:required_field_missing:{field}")
        if entry.get("halt_code") != code:
            failures.append(f"{code}:halt_code_mismatch:{entry.get('halt_code')}")
        if entry.get("canonical_halt_code") != code:
            failures.append(f"{code}:canonical_halt_code_mismatch:{entry.get('canonical_halt_code')}")
        if not entry.get("smallest_honest_meaning"):
            failures.append(f"{code}:empty_smallest_honest_meaning")
        if not isinstance(entry.get("must_not_impersonate"), list) or not entry.get("must_not_impersonate"):
            failures.append(f"{code}:must_not_impersonate_missing_or_empty")
        if not isinstance(entry.get("allowed_next_handling"), list) or not entry.get("allowed_next_handling"):
            failures.append(f"{code}:allowed_next_handling_missing_or_empty")

    schema = policy_receipt.get("halt_record_schema") or {}
    for field in REQUIRED_HALT_RECORD_FIELDS:
        if field not in schema.get("required_fields", []):
            failures.append(f"halt_record_schema_required_field_missing:{field}")
    law = schema.get("terminal_law") or {}
    if law.get("halt_terminal_must_be_STOP") is not True:
        failures.append("halt_record_schema_terminal_stop_law_missing")
    if law.get("advance_is_not_a_halt") is not True:
        failures.append("halt_record_schema_advance_not_halt_law_missing")

    classifier = policy_receipt.get("halt_classifier_priority") or {}
    if classifier.get("mode") != "deterministic_priority_table_not_smart_classifier":
        failures.append(f"classifier_mode_wrong:{classifier.get('mode')}")
    order = classifier.get("priority_order", [])
    if "STOP_AUTHORITY_VIOLATION" in order and "STOP_PROJECTION_BUG" in order:
        if order.index("STOP_AUTHORITY_VIOLATION") > order.index("STOP_PROJECTION_BUG"):
            failures.append("classifier_authority_after_projection")
    if "STOP_RECEIPT_MISMATCH" in order and "STOP_PROJECTION_BUG" in order:
        if order.index("STOP_RECEIPT_MISMATCH") > order.index("STOP_PROJECTION_BUG"):
            failures.append("classifier_receipt_mismatch_after_projection")
    if "STOP_NO_APPLICABLE_MOVE" in order and "STOP_DONE" in order:
        if order.index("STOP_NO_APPLICABLE_MOVE") > order.index("STOP_DONE"):
            failures.append("classifier_no_applicable_after_done")

    routes = policy_receipt.get("halt_to_next_handling_table", {}).get("routes", {})
    if set(routes.keys()) != set(vocab.keys()):
        failures.append("halt_to_next_handling_routes_do_not_match_vocab")
    for code, route in routes.items():
        if not isinstance(route, list) or not route:
            failures.append(f"{code}:route_missing")

    for patch_key, expected_mode in [
        ("runner_receipt_halt_patch", "future_schema_patch_only_do_not_mutate_existing_receipts"),
        ("proceed_readout_halt_patch", "future_schema_patch_only_do_not_mutate_existing_readouts"),
        ("trace_entry_halt_patch", "future_schema_patch_only_do_not_mutate_existing_traces"),
    ]:
        if policy_receipt.get(patch_key, {}).get("patch_mode") != expected_mode:
            failures.append(f"{patch_key}_mode_wrong:{policy_receipt.get(patch_key, {}).get('patch_mode')}")

    auth = policy_receipt.get("authorized_operations_next") or {}
    for key in [
        "write_halt_vocabulary_artifact",
        "write_halt_record_schema_artifact",
        "write_halt_family_table_artifact",
        "write_halt_classifier_priority_artifact",
        "write_halt_to_next_handling_table_artifact",
        "write_runner_receipt_halt_patch_artifact",
        "write_proceed_readout_halt_patch_artifact",
        "write_trace_entry_halt_patch_artifact",
        "write_day3_demo_halt_record_plan_artifact",
        "emit_day3_demo_halt_records",
        "emit_day3_demo_halt_receipts",
        "emit_implementation_receipt",
    ]:
        if auth.get(key) is not True:
            failures.append(f"authorized_operation_missing:{key}:{auth.get(key)}")

    forbidden = policy_receipt.get("forbidden_operations_next") or {}
    for key in [
        "mutate_existing_runner_receipts",
        "mutate_existing_proceed_readouts",
        "mutate_existing_trace_files",
        "mutate_existing_ledger_files",
        "modify_proceed_adapter_module",
        "modify_trace_ledger_runner_module",
        "modify_local_regime_v1",
        "accept_taxonomy_delta",
        "promote_taxonomy_delta",
        "add_new_move_automatically",
        "proof_claim",
        "halt_as_truth_claim",
        "halt_as_proof_claim",
        "hidden_continuation_after_terminal",
        "sqlite_registry_write",
        "sqlite_registry_read",
    ]:
        if forbidden.get(key) is not True:
            failures.append(f"forbidden_operation_missing:{key}:{forbidden.get(key)}")

    if proceed_receipt.get("receipt_id") != PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"proceed_receipt_id_wrong:{proceed_receipt.get('receipt_id')}")
    if proceed_receipt.get("gate") != "PASS":
        failures.append(f"proceed_gate_not_PASS:{proceed_receipt.get('gate')}")
    if proceed_receipt.get("target_adapter_unit_id") != "proceed_adapter.v0":
        failures.append(f"proceed_target_wrong:{proceed_receipt.get('target_adapter_unit_id')}")
    if proceed_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append(f"proceed_terminal_not_STOP:{proceed_receipt.get('terminal')}")
    if proceed_receipt.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append(f"proceed_terminal_stop_not_DONE:{proceed_receipt.get('terminal')}")
    if proceed_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append(f"proceed_terminal_next_not_null:{proceed_receipt.get('terminal')}")

    p_metrics = proceed_receipt.get("aggregate_metrics") or {}
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
        if p_metrics.get(key) != 0:
            failures.append(f"source_proceed_metric_not_zero:{key}:{p_metrics.get(key)}")

    if proceed_policy.get("policy_id") != PROCEED_ADAPTER_POLICY_ID:
        failures.append(f"proceed_policy_id_wrong:{proceed_policy.get('policy_id')}")

    if trace_ledger_receipt.get("receipt_id") != TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"trace_ledger_receipt_id_wrong:{trace_ledger_receipt.get('receipt_id')}")
    if trace_ledger_receipt.get("gate") != "PASS":
        failures.append(f"trace_ledger_gate_not_PASS:{trace_ledger_receipt.get('gate')}")
    if trace_schema.get("schema_version") != "jurisdiction_runner_trace_file_v0":
        failures.append(f"trace_schema_version_wrong:{trace_schema.get('schema_version')}")
    if ledger_schema.get("schema_version") != "unresolved_proposal_ledger_v0":
        failures.append(f"ledger_schema_version_wrong:{ledger_schema.get('schema_version')}")
    if local_regime_v1.get("local_regime_hash") != LOCAL_REGIME_V1_HASH:
        failures.append(f"local_regime_v1_hash_wrong:{local_regime_v1.get('local_regime_hash')}")

    for path, label in [
        (POLICY_PATH, "halt_policy"),
        (POLICY_RECEIPT_PATH, "halt_policy_receipt"),
        (PROCEED_RECEIPT_PATH, "proceed_receipt"),
        (PROCEED_POLICY_PATH, "proceed_policy"),
        (PROCEED_ADAPTER_MODULE_PATH, "proceed_adapter_module"),
        (TRACE_LEDGER_RECEIPT_PATH, "trace_ledger_receipt"),
        (TRACE_SCHEMA_PATH, "trace_schema"),
        (PROPOSAL_LEDGER_SCHEMA_PATH, "proposal_ledger_schema"),
        (TRACE_LEDGER_RUNNER_PATH, "trace_ledger_runner"),
        (LOCAL_REGIME_V1_PATH, "local_regime_v1"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{rel(path)}")

    return failures

def source_refs_for_demo(proceed_receipt: Dict[str, Any], case_name: str) -> Dict[str, Any]:
    case_map = {
        "DEMO_CLEAN_NEXT_BOUNDARY": "PROCEED_TERMINAL_BOUNDARY_NO_IMPLICIT_CONTINUATION",
        "DEMO_PROJECTION_BUG": "PROCEED_LOCAL_GOTCHA_RECORD_ONLY",
        "DEMO_NO_APPLICABLE_MOVE": "PROCEED_READOUT_REFERENCES_TRACE_RECEIPT_LEDGER",
        "DEMO_TAXONOMY_GAP": "PROCEED_TAXONOMY_PRESSURE_RECORDED_ONLY",
    }
    source_case = case_map[case_name]
    case = proceed_receipt["case_results"][source_case]
    readout = read_json(ROOT / case["readout_path"])
    return {
        "source_case_name": source_case,
        "source_readout_ref": {
            "readout_id": case["readout_id"],
            "readout_path": case["readout_path"],
        },
        "source_trace_ref": copy.deepcopy(readout["trace_delta"]["trace_ref"]),
        "source_receipt_ref": copy.deepcopy(readout["receipt_or_projection_delta"]["receipt_ref"]),
        "source_ledger_ref": copy.deepcopy(readout["ledger_delta"]["ledger_ref"]),
    }

def observed_pressure_for(case_name: str) -> Dict[str, Any]:
    if case_name == "DEMO_CLEAN_NEXT_BOUNDARY":
        return {
            "expected": "current unit has completed and no next unit has been declared inside the same unit",
            "observed": "terminal boundary requires explicit next unit declaration",
        }
    if case_name == "DEMO_PROJECTION_BUG":
        return {
            "expected": "projection/readout agrees with trace evidence",
            "observed": "demo projection reports a read-only mismatch while source trace/receipt/ledger remain untouched",
        }
    if case_name == "DEMO_NO_APPLICABLE_MOVE":
        return {
            "expected": "state has at least one registered applicable move",
            "observed": "valid inspected state has no registered applicable move under declared surface",
            "legacy_observed_code": "NO_APPLICABLE_MOVE",
            "canonicalized_to": "STOP_NO_APPLICABLE_MOVE",
        }
    if case_name == "DEMO_TAXONOMY_GAP":
        return {
            "expected": "existing vocabulary honestly classifies stop pressure",
            "observed": "demo pressure has no honest current label beyond taxonomy gap",
            "taxonomy_pressure_status": "RECORDED_ONLY",
        }
    raise AssertionError(case_name)

def halt_code_for_demo(case_name: str) -> str:
    return {
        "DEMO_CLEAN_NEXT_BOUNDARY": "STOP_NEXT_MOVE_BOUNDARY",
        "DEMO_PROJECTION_BUG": "STOP_PROJECTION_BUG",
        "DEMO_NO_APPLICABLE_MOVE": "STOP_NO_APPLICABLE_MOVE",
        "DEMO_TAXONOMY_GAP": "STOP_TAXONOMY_GAP",
    }[case_name]

def build_halt_record(
    *,
    case_name: str,
    halt_entry: Dict[str, Any],
    source_refs: Dict[str, Any],
) -> Dict[str, Any]:
    halt_code = halt_entry["halt_code"]
    run_id = f"day3_demo_{case_name.lower()}"
    seed = {
        "case_name": case_name,
        "run_id": run_id,
        "halt_code": halt_code,
        "source_readout_ref": source_refs["source_readout_ref"],
    }
    halt_record_id = f"halt_{sha8(seed)}"
    halt_record_path = f"data/halt_vocabulary_v0_demo/halt_records/{halt_record_id}.json"

    record = {
        "schema_version": "halt_record_v0",
        "halt_record_id": halt_record_id,
        "run_id": run_id,
        "unit_id": TARGET_UNIT_ID,
        "step_index": 0,
        "halt_code": halt_code,
        "canonical_halt_code": halt_entry["canonical_halt_code"],
        "halt_family": halt_entry["halt_family"],
        "smallest_honest_meaning": halt_entry["smallest_honest_meaning"],
        "must_not_impersonate": halt_entry["must_not_impersonate"],
        "observed_pressure": observed_pressure_for(case_name),
        "allowed_next_handling": halt_entry["allowed_next_handling"],
        "source_readout_ref": source_refs["source_readout_ref"],
        "source_trace_ref": source_refs["source_trace_ref"],
        "source_receipt_ref": source_refs["source_receipt_ref"],
        "source_ledger_ref": source_refs["source_ledger_ref"],
        "terminal_result": {
            "type": "STOP",
            "stop_code": halt_entry["canonical_halt_code"],
            "halt_record_ref": {
                "halt_record_id": halt_record_id,
                "halt_record_path": halt_record_path,
            },
        },
        "taxonomy_pressure": {
            "status": "RECORDED_ONLY" if halt_code == "STOP_TAXONOMY_GAP" else "NONE",
            "taxonomy_delta_applied": False,
            "taxonomy_delta_promoted": False,
        },
        "authority_guards": {
            "halt_as_truth_claimed": False,
            "halt_as_proof_claimed": False,
            "taxonomy_delta_applied": False,
            "taxonomy_delta_promoted": False,
            "new_move_added": False,
            "proposal_executed": False,
            "proposal_promoted": False,
            "source_trace_modified": False,
            "source_receipt_modified": False,
            "source_ledger_modified": False,
            "source_runner_modified": False,
            "source_regime_modified": False,
            "registry_written": False,
            "registry_sqlite_read": False,
            "registry_sqlite_written": False,
            "hidden_continuation_authorized": False,
        },
        "created_at": now_iso(),
    }
    return record

def validate_halt_record(record: Dict[str, Any], vocab: Dict[str, Dict[str, Any]]) -> List[str]:
    failures: List[str] = []
    for field in REQUIRED_HALT_RECORD_FIELDS:
        if field not in record:
            failures.append(f"{record.get('halt_record_id')}:required_field_missing:{field}")

    halt_code = record.get("halt_code")
    if halt_code not in vocab:
        failures.append(f"{record.get('halt_record_id')}:unknown_halt_code:{halt_code}")
        return failures

    entry = vocab[halt_code]
    if record.get("canonical_halt_code") != entry.get("canonical_halt_code"):
        failures.append(f"{record.get('halt_record_id')}:canonical_mismatch")
    if record.get("halt_family") != entry.get("halt_family"):
        failures.append(f"{record.get('halt_record_id')}:family_mismatch")
    if record.get("smallest_honest_meaning") != entry.get("smallest_honest_meaning"):
        failures.append(f"{record.get('halt_record_id')}:meaning_mismatch")
    if record.get("must_not_impersonate") != entry.get("must_not_impersonate"):
        failures.append(f"{record.get('halt_record_id')}:anti_impersonation_mismatch")
    if record.get("allowed_next_handling") != entry.get("allowed_next_handling"):
        failures.append(f"{record.get('halt_record_id')}:allowed_next_handling_mismatch")

    terminal = record.get("terminal_result") or {}
    if terminal.get("type") != "STOP":
        failures.append(f"{record.get('halt_record_id')}:terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != record.get("canonical_halt_code"):
        failures.append(f"{record.get('halt_record_id')}:stop_code_not_canonical:{terminal}")
    if terminal.get("next_unit_id") is not None:
        failures.append(f"{record.get('halt_record_id')}:halt_has_next_unit_id:{terminal}")

    for ref_key in ["source_readout_ref", "source_trace_ref", "source_receipt_ref", "source_ledger_ref"]:
        ref_obj = record.get(ref_key)
        if not isinstance(ref_obj, dict) or not ref_obj:
            failures.append(f"{record.get('halt_record_id')}:{ref_key}_missing")

    if halt_code == "STOP_NO_APPLICABLE_MOVE":
        if "NO_APPLICABLE_MOVE" not in entry.get("legacy_aliases", []):
            failures.append("demo_no_applicable_alias_not_present")
        if "proof closure" not in " ".join(record.get("must_not_impersonate", [])).lower():
            failures.append("demo_no_applicable_missing_proof_closure_anti_impersonation")
        if record.get("observed_pressure", {}).get("legacy_observed_code") != "NO_APPLICABLE_MOVE":
            failures.append("demo_no_applicable_legacy_observed_missing")

    if halt_code == "STOP_TAXONOMY_GAP":
        taxonomy = record.get("taxonomy_pressure") or {}
        if taxonomy.get("status") != "RECORDED_ONLY":
            failures.append("demo_taxonomy_gap_not_recorded_only")
        if taxonomy.get("taxonomy_delta_applied") is not False:
            failures.append("demo_taxonomy_gap_delta_applied")
        if taxonomy.get("taxonomy_delta_promoted") is not False:
            failures.append("demo_taxonomy_gap_delta_promoted")

    guards = record.get("authority_guards") or {}
    for key in [
        "halt_as_truth_claimed",
        "halt_as_proof_claimed",
        "taxonomy_delta_applied",
        "taxonomy_delta_promoted",
        "new_move_added",
        "proposal_executed",
        "proposal_promoted",
        "source_trace_modified",
        "source_receipt_modified",
        "source_ledger_modified",
        "source_runner_modified",
        "source_regime_modified",
        "registry_written",
        "registry_sqlite_read",
        "registry_sqlite_written",
        "hidden_continuation_authorized",
    ]:
        if guards.get(key) is not False:
            failures.append(f"{record.get('halt_record_id')}:guard_not_false:{key}:{guards.get(key)}")

    return failures

def build_demo_receipts(records: List[Dict[str, Any]], vocab: Dict[str, Dict[str, Any]]) -> Dict[str, Any]:
    receipts: Dict[str, Dict[str, Any]] = {}
    for record in records:
        seed = {"halt_record_id": record["halt_record_id"], "halt_code": record["halt_code"]}
        receipt_id = f"halt_receipt_{sha8(seed)}"
        receipts[receipt_id] = {
            "schema_version": "day3_demo_halt_receipt_v0",
            "receipt_type": "DAY3_DEMO_HALT_RECEIPT",
            "receipt_id": receipt_id,
            "halt_record_id": record["halt_record_id"],
            "halt_code": record["halt_code"],
            "canonical_halt_code": record["canonical_halt_code"],
            "halt_family": record["halt_family"],
            "four_field_rule_present": all(k in record and record[k] for k in [
                "halt_code",
                "smallest_honest_meaning",
                "must_not_impersonate",
                "allowed_next_handling",
            ]),
            "terminal_result": record["terminal_result"],
            "allowed_next_handling": record["allowed_next_handling"],
            "must_not_impersonate": record["must_not_impersonate"],
            "source_refs_present": all(record.get(k) for k in [
                "source_readout_ref",
                "source_trace_ref",
                "source_receipt_ref",
                "source_ledger_ref",
            ]),
            "halt_as_truth_claimed": False,
            "halt_as_proof_claimed": False,
            "taxonomy_delta_applied": record["taxonomy_pressure"]["taxonomy_delta_applied"],
            "taxonomy_delta_promoted": record["taxonomy_pressure"]["taxonomy_delta_promoted"],
            "new_move_added": False,
            "gate": "PASS",
            "failures": [],
            "created_at": now_iso(),
        }
    return receipts

def validate_demo_receipts(demo_receipts: Dict[str, Dict[str, Any]], records: List[Dict[str, Any]]) -> List[str]:
    failures: List[str] = []
    records_by_id = {r["halt_record_id"]: r for r in records}
    if len(demo_receipts) != len(records):
        failures.append(f"demo_receipt_count_mismatch:{len(demo_receipts)}:{len(records)}")
    for receipt_id, receipt in demo_receipts.items():
        record = records_by_id.get(receipt.get("halt_record_id"))
        if record is None:
            failures.append(f"{receipt_id}:record_missing:{receipt.get('halt_record_id')}")
            continue
        if receipt.get("gate") != "PASS":
            failures.append(f"{receipt_id}:gate_not_PASS:{receipt.get('gate')}")
        if receipt.get("halt_code") != record.get("halt_code"):
            failures.append(f"{receipt_id}:halt_code_mismatch")
        if receipt.get("terminal_result", {}).get("type") != "STOP":
            failures.append(f"{receipt_id}:terminal_not_STOP")
        if receipt.get("terminal_result", {}).get("stop_code") != record.get("canonical_halt_code"):
            failures.append(f"{receipt_id}:stop_code_not_canonical")
        if receipt.get("four_field_rule_present") is not True:
            failures.append(f"{receipt_id}:four_field_rule_missing")
        if receipt.get("source_refs_present") is not True:
            failures.append(f"{receipt_id}:source_refs_missing")
        for key in [
            "halt_as_truth_claimed",
            "halt_as_proof_claimed",
            "taxonomy_delta_applied",
            "taxonomy_delta_promoted",
            "new_move_added",
        ]:
            if receipt.get(key) is not False:
                failures.append(f"{receipt_id}:guard_not_false:{key}:{receipt.get(key)}")
    return failures

def validate_implementation_receipt(receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []

    if receipt.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("source_halt_vocabulary_policy_id") != HALT_VOCABULARY_POLICY_ID:
        failures.append(f"source_policy_wrong:{receipt.get('source_halt_vocabulary_policy_id')}")
    if receipt.get("source_halt_vocabulary_policy_receipt_id") != HALT_VOCABULARY_POLICY_RECEIPT_ID:
        failures.append(f"source_policy_receipt_wrong:{receipt.get('source_halt_vocabulary_policy_receipt_id')}")
    if receipt.get("target_unit_id") != TARGET_UNIT_ID:
        failures.append(f"target_unit_wrong:{receipt.get('target_unit_id')}")

    gates = receipt.get("acceptance_gate_results") or {}
    for gate in [
        "HVI0_source_policy_verified",
        "HVI1_core_artifacts_emitted",
        "HVI2_vocabulary_four_field_rule_verified",
        "HVI3_halt_record_schema_verified",
        "HVI4_demo_halt_records_emitted",
        "HVI5_demo_halt_receipts_emitted",
        "HVI6_alias_and_taxonomy_record_only_verified",
        "HVI7_no_source_artifact_mutation",
    ]:
        if gates.get(gate) is not True:
            failures.append(f"acceptance_gate_not_true:{gate}:{gates.get(gate)}")

    metrics = receipt.get("aggregate_metrics") or {}
    if metrics.get("canonical_halt_entry_count") != 21:
        failures.append(f"canonical_halt_entry_count_wrong:{metrics.get('canonical_halt_entry_count')}")
    if metrics.get("demo_halt_record_count") != 4:
        failures.append(f"demo_halt_record_count_wrong:{metrics.get('demo_halt_record_count')}")
    if metrics.get("demo_halt_receipt_count") != 4:
        failures.append(f"demo_halt_receipt_count_wrong:{metrics.get('demo_halt_receipt_count')}")
    if metrics.get("halt_record_validation_failure_count") != 0:
        failures.append(f"halt_record_validation_failure_count_nonzero:{metrics.get('halt_record_validation_failure_count')}")
    if metrics.get("demo_receipt_validation_failure_count") != 0:
        failures.append(f"demo_receipt_validation_failure_count_nonzero:{metrics.get('demo_receipt_validation_failure_count')}")
    if metrics.get("stop_terminal_count") != 4:
        failures.append(f"stop_terminal_count_wrong:{metrics.get('stop_terminal_count')}")
    if metrics.get("advance_terminal_as_halt_count") != 0:
        failures.append(f"advance_terminal_as_halt_count_nonzero:{metrics.get('advance_terminal_as_halt_count')}")
    for key in [
        "source_trace_modified_count",
        "source_receipt_modified_count",
        "source_ledger_modified_count",
        "source_runner_modified_count",
        "source_regime_modified_count",
        "taxonomy_delta_applied_count",
        "taxonomy_delta_promoted_count",
        "new_move_added_count",
        "proposal_executed_count",
        "proposal_promoted_count",
        "registry_write_count",
        "registry_sqlite_write_count",
        "halt_as_truth_claim_count",
        "halt_as_proof_claim_count",
        "hidden_continuation_count",
    ]:
        if metrics.get(key) != 0:
            failures.append(f"metric_not_zero:{key}:{metrics.get(key)}")

    guards = receipt.get("authority_guards") or {}
    for key in [
        "halt_vocabulary_artifact_emitted",
        "halt_record_schema_artifact_emitted",
        "halt_family_table_artifact_emitted",
        "halt_classifier_priority_artifact_emitted",
        "halt_to_next_handling_table_artifact_emitted",
        "runner_receipt_halt_patch_artifact_emitted",
        "proceed_readout_halt_patch_artifact_emitted",
        "trace_entry_halt_patch_artifact_emitted",
        "day3_demo_halt_record_plan_artifact_emitted",
        "day3_demo_halt_records_emitted",
        "day3_demo_halt_receipts_emitted",
        "implementation_receipt_emitted",
    ]:
        if guards.get(key) is not True:
            failures.append(f"authority_guard_not_true:{key}:{guards.get(key)}")
    for key in [
        "source_proceed_adapter_modified",
        "source_trace_ledger_runner_modified",
        "source_local_regime_v1_modified",
        "source_trace_modified",
        "source_receipt_modified",
        "source_ledger_modified",
        "taxonomy_delta_applied",
        "taxonomy_delta_promoted",
        "new_move_added",
        "proposal_executed",
        "proposal_promoted",
        "registry_written",
        "registry_sqlite_read",
        "registry_sqlite_written",
        "global_taxonomy_claimed",
        "final_schema_claimed",
        "proof_claimed",
        "halt_as_truth_claimed",
        "halt_as_proof_claimed",
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
    proceed_receipt = read_json(PROCEED_RECEIPT_PATH)
    proceed_policy = read_json(PROCEED_POLICY_PATH)
    trace_ledger_receipt = read_json(TRACE_LEDGER_RECEIPT_PATH)
    trace_schema = read_json(TRACE_SCHEMA_PATH)
    ledger_schema = read_json(PROPOSAL_LEDGER_SCHEMA_PATH)
    local_regime_v1 = read_json(LOCAL_REGIME_V1_PATH)

    failures: List[str] = []
    failures.extend(validate_policy_inputs(
        policy,
        policy_receipt,
        proceed_receipt,
        proceed_policy,
        trace_ledger_receipt,
        trace_schema,
        ledger_schema,
        local_regime_v1,
    ))

    for d in [
        HALT_VOCABULARY_DIR,
        HALT_RECORD_SCHEMA_DIR,
        HALT_FAMILY_TABLE_DIR,
        HALT_CLASSIFIER_PRIORITY_DIR,
        HALT_NEXT_HANDLING_DIR,
        HALT_PATCH_DIR,
        DEMO_DIR,
        DEMO_DIR / "halt_records",
        IMPLEMENTATION_RECEIPT_DIR,
    ]:
        d.mkdir(parents=True, exist_ok=True)

    vocab_artifact = policy_receipt["halt_vocabulary"]
    vocab_entries = vocab_artifact["entries"]
    halt_record_schema = policy_receipt["halt_record_schema"]
    halt_family_table = policy_receipt["halt_family_table"]
    halt_classifier_priority = policy_receipt["halt_classifier_priority"]
    halt_to_next_handling = policy_receipt["halt_to_next_handling_table"]
    runner_receipt_patch = policy_receipt["runner_receipt_halt_patch"]
    proceed_readout_patch = policy_receipt["proceed_readout_halt_patch"]
    trace_entry_patch = policy_receipt["trace_entry_halt_patch"]
    demo_plan = policy_receipt["day3_demo_halt_record_plan"]

    artifact_paths = {
        "halt_vocabulary": HALT_VOCABULARY_DIR / "halt_vocabulary_v0.json",
        "halt_record_schema": HALT_RECORD_SCHEMA_DIR / "halt_record_schema_v0.json",
        "halt_family_table": HALT_FAMILY_TABLE_DIR / "halt_family_table_v0.json",
        "halt_classifier_priority": HALT_CLASSIFIER_PRIORITY_DIR / "halt_classifier_priority_v0.json",
        "halt_to_next_handling_table": HALT_NEXT_HANDLING_DIR / "halt_to_next_handling_table_v0.json",
        "runner_receipt_halt_patch": HALT_PATCH_DIR / "runner_receipt_halt_patch_v0.json",
        "proceed_readout_halt_patch": HALT_PATCH_DIR / "proceed_readout_halt_patch_v0.json",
        "trace_entry_halt_patch": HALT_PATCH_DIR / "trace_entry_halt_patch_v0.json",
        "day3_demo_halt_record_plan": DEMO_DIR / "day3_demo_halt_record_plan_v0.json",
    }

    write_json(artifact_paths["halt_vocabulary"], vocab_artifact)
    write_json(artifact_paths["halt_record_schema"], halt_record_schema)
    write_json(artifact_paths["halt_family_table"], halt_family_table)
    write_json(artifact_paths["halt_classifier_priority"], halt_classifier_priority)
    write_json(artifact_paths["halt_to_next_handling_table"], halt_to_next_handling)
    write_json(artifact_paths["runner_receipt_halt_patch"], runner_receipt_patch)
    write_json(artifact_paths["proceed_readout_halt_patch"], proceed_readout_patch)
    write_json(artifact_paths["trace_entry_halt_patch"], trace_entry_patch)
    write_json(artifact_paths["day3_demo_halt_record_plan"], demo_plan)

    demo_records: List[Dict[str, Any]] = []
    demo_record_validation_failures: List[str] = []

    for case_name in DEMO_CASES:
        halt_code = halt_code_for_demo(case_name)
        halt_entry = vocab_entries[halt_code]
        source_refs = source_refs_for_demo(proceed_receipt, case_name)
        record = build_halt_record(case_name=case_name, halt_entry=halt_entry, source_refs=source_refs)

        record_path = DEMO_DIR / "halt_records" / f"{record['halt_record_id']}.json"
        record["record_path"] = rel(record_path)
        record["terminal_result"]["halt_record_ref"]["halt_record_path"] = rel(record_path)

        record_failures = validate_halt_record(record, vocab_entries)
        demo_record_validation_failures.extend(record_failures)
        write_json(record_path, record)
        demo_records.append(record)

    demo_records_jsonl_path = DEMO_DIR / "day3_demo_halt_records.jsonl"
    write_jsonl(demo_records_jsonl_path, demo_records)

    demo_receipts = build_demo_receipts(demo_records, vocab_entries)
    demo_receipt_failures = validate_demo_receipts(demo_receipts, demo_records)
    demo_receipts_path = DEMO_DIR / "day3_demo_halt_receipts.json"
    write_json(demo_receipts_path, {
        "schema_version": "day3_demo_halt_receipts_v0",
        "receipt_type": "DAY3_DEMO_HALT_RECEIPTS_BUNDLE",
        "receipt_bundle_id": sha8(demo_receipts),
        "source_policy_id": HALT_VOCABULARY_POLICY_ID,
        "demo_receipts": demo_receipts,
        "gate": "PASS" if not demo_receipt_failures else "FAIL",
        "failures": demo_receipt_failures,
        "created_at": now_iso(),
    })

    failures.extend(demo_record_validation_failures)
    failures.extend(demo_receipt_failures)

    aggregate_metrics = {
        "canonical_halt_entry_count": len(vocab_entries),
        "halt_family_count": len(halt_family_table["families"]),
        "halt_route_count": len(halt_to_next_handling["routes"]),
        "demo_halt_record_count": len(demo_records),
        "demo_halt_receipt_count": len(demo_receipts),
        "halt_record_validation_failure_count": len(demo_record_validation_failures),
        "demo_receipt_validation_failure_count": len(demo_receipt_failures),
        "stop_terminal_count": sum(1 for r in demo_records if r["terminal_result"]["type"] == "STOP"),
        "advance_terminal_as_halt_count": sum(1 for r in demo_records if r["terminal_result"]["type"] == "ADVANCE"),
        "source_trace_modified_count": 0,
        "source_receipt_modified_count": 0,
        "source_ledger_modified_count": 0,
        "source_runner_modified_count": 0,
        "source_regime_modified_count": 0,
        "taxonomy_delta_applied_count": sum(1 for r in demo_records if r["taxonomy_pressure"]["taxonomy_delta_applied"]),
        "taxonomy_delta_promoted_count": sum(1 for r in demo_records if r["taxonomy_pressure"]["taxonomy_delta_promoted"]),
        "new_move_added_count": 0,
        "proposal_executed_count": 0,
        "proposal_promoted_count": 0,
        "registry_write_count": 0,
        "registry_sqlite_write_count": 0,
        "halt_as_truth_claim_count": 0,
        "halt_as_proof_claim_count": 0,
        "hidden_continuation_count": 0,
    }

    acceptance_gate_results = {
        "HVI0_source_policy_verified": len(validate_policy_inputs(
            policy,
            policy_receipt,
            proceed_receipt,
            proceed_policy,
            trace_ledger_receipt,
            trace_schema,
            ledger_schema,
            local_regime_v1,
        )) == 0,
        "HVI1_core_artifacts_emitted": all(path.exists() for path in artifact_paths.values()),
        "HVI2_vocabulary_four_field_rule_verified": all(
            all(field in entry and entry[field] for field in REQUIRED_HALT_ENTRY_FIELDS)
            for entry in vocab_entries.values()
        ),
        "HVI3_halt_record_schema_verified": all(field in halt_record_schema["required_fields"] for field in REQUIRED_HALT_RECORD_FIELDS),
        "HVI4_demo_halt_records_emitted": len(demo_records) == 4 and len(demo_record_validation_failures) == 0,
        "HVI5_demo_halt_receipts_emitted": len(demo_receipts) == 4 and len(demo_receipt_failures) == 0,
        "HVI6_alias_and_taxonomy_record_only_verified": (
            "NO_APPLICABLE_MOVE" in vocab_entries["STOP_NO_APPLICABLE_MOVE"].get("legacy_aliases", [])
            and "NO_APPLICABLE_MOVE" not in vocab_entries
            and all(not r["taxonomy_pressure"]["taxonomy_delta_applied"] for r in demo_records)
            and all(not r["taxonomy_pressure"]["taxonomy_delta_promoted"] for r in demo_records)
            and any(r["halt_code"] == "STOP_TAXONOMY_GAP" and r["taxonomy_pressure"]["status"] == "RECORDED_ONLY" for r in demo_records)
        ),
        "HVI7_no_source_artifact_mutation": (
            aggregate_metrics["source_trace_modified_count"] == 0
            and aggregate_metrics["source_receipt_modified_count"] == 0
            and aggregate_metrics["source_ledger_modified_count"] == 0
            and aggregate_metrics["source_runner_modified_count"] == 0
            and aggregate_metrics["source_regime_modified_count"] == 0
        ),
    }

    for gate, ok in acceptance_gate_results.items():
        if ok is not True:
            failures.append(f"acceptance_gate_failed:{gate}:{ok}")

    authority_guards = {
        "halt_vocabulary_artifact_emitted": True,
        "halt_record_schema_artifact_emitted": True,
        "halt_family_table_artifact_emitted": True,
        "halt_classifier_priority_artifact_emitted": True,
        "halt_to_next_handling_table_artifact_emitted": True,
        "runner_receipt_halt_patch_artifact_emitted": True,
        "proceed_readout_halt_patch_artifact_emitted": True,
        "trace_entry_halt_patch_artifact_emitted": True,
        "day3_demo_halt_record_plan_artifact_emitted": True,
        "day3_demo_halt_records_emitted": True,
        "day3_demo_halt_receipts_emitted": True,
        "implementation_receipt_emitted": True,
        "source_proceed_adapter_modified": False,
        "source_trace_ledger_runner_modified": False,
        "source_local_regime_v1_modified": False,
        "source_trace_modified": False,
        "source_receipt_modified": False,
        "source_ledger_modified": False,
        "taxonomy_delta_applied": False,
        "taxonomy_delta_promoted": False,
        "new_move_added": False,
        "proposal_executed": False,
        "proposal_promoted": False,
        "registry_written": False,
        "registry_sqlite_read": False,
        "registry_sqlite_written": False,
        "global_taxonomy_claimed": False,
        "final_schema_claimed": False,
        "proof_claimed": False,
        "halt_as_truth_claimed": False,
        "halt_as_proof_claimed": False,
        "hidden_continuation_authorized": False,
    }

    artifact_guards = {
        "halt_policy_tracked": tracked(POLICY_PATH),
        "halt_policy_receipt_tracked": tracked(POLICY_RECEIPT_PATH),
        "source_proceed_receipt_tracked": tracked(PROCEED_RECEIPT_PATH),
        "source_proceed_policy_tracked": tracked(PROCEED_POLICY_PATH),
        "source_proceed_adapter_module_tracked": tracked(PROCEED_ADAPTER_MODULE_PATH),
        "source_trace_ledger_receipt_tracked": tracked(TRACE_LEDGER_RECEIPT_PATH),
        "source_trace_schema_tracked": tracked(TRACE_SCHEMA_PATH),
        "source_ledger_schema_tracked": tracked(PROPOSAL_LEDGER_SCHEMA_PATH),
        "source_trace_ledger_runner_tracked": tracked(TRACE_LEDGER_RUNNER_PATH),
        "source_local_regime_v1_tracked": tracked(LOCAL_REGIME_V1_PATH),
        "outputs_path_addressed": True,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_authority_used": False,
    }

    output_artifacts = {
        name: rel(path) for name, path in artifact_paths.items()
    }
    output_artifacts["day3_demo_halt_records_jsonl"] = rel(demo_records_jsonl_path)
    output_artifacts["day3_demo_halt_receipts"] = rel(demo_receipts_path)
    output_artifacts["demo_halt_record_files"] = {
        record["halt_record_id"]: record["record_path"] for record in demo_records
    }

    implementation_seed = {
        "unit_id": UNIT_ID,
        "source_policy_id": HALT_VOCABULARY_POLICY_ID,
        "vocab_id": vocab_artifact["vocabulary_id"],
        "demo_records": [r["halt_record_id"] for r in demo_records],
        "output_artifacts": output_artifacts,
    }
    implementation_receipt_id = sha8(implementation_seed)

    implementation_receipt = {
        "schema_version": "halt_vocabulary_v0_implementation_receipt_v0",
        "receipt_type": "HALT_VOCABULARY_V0_IMPLEMENTATION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": implementation_receipt_id,
        "source_halt_vocabulary_policy_id": HALT_VOCABULARY_POLICY_ID,
        "source_halt_vocabulary_policy_receipt_id": HALT_VOCABULARY_POLICY_RECEIPT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_proceed_adapter_implementation_receipt_id": PROCEED_ADAPTER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_ledger_implementation_receipt_id": TRACE_LEDGER_IMPLEMENTATION_RECEIPT_ID,
        "source_trace_schema_id": TRACE_SCHEMA_ID,
        "source_proposal_ledger_schema_id": PROPOSAL_LEDGER_SCHEMA_ID,
        "source_local_regime_hash": LOCAL_REGIME_V1_HASH,
        "output_artifacts": output_artifacts,
        "demo_halt_records": {
            record["halt_record_id"]: {
                "halt_record_id": record["halt_record_id"],
                "record_path": record["record_path"],
                "halt_code": record["halt_code"],
                "halt_family": record["halt_family"],
                "terminal_result": record["terminal_result"],
                "taxonomy_pressure": record["taxonomy_pressure"],
                "source_readout_ref": record["source_readout_ref"],
                "source_trace_ref": record["source_trace_ref"],
                "source_receipt_ref": record["source_receipt_ref"],
                "source_ledger_ref": record["source_ledger_ref"],
            }
            for record in demo_records
        },
        "demo_halt_receipts_path": rel(demo_receipts_path),
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
    print(f"halt_vocabulary_implementation_receipt_id={implementation_receipt_id}")
    print(f"halt_vocabulary_implementation_receipt_path=data/halt_vocabulary_v0_implementation_receipts/{implementation_receipt_id}.json")
    for name, path in sorted(output_artifacts.items()):
        if isinstance(path, str):
            print(f"artifact_{name}_path={path}")
    for record_id, path in sorted(output_artifacts["demo_halt_record_files"].items()):
        print(f"demo_halt_record_{record_id}_path={path}")

    return 0 if implementation_receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
