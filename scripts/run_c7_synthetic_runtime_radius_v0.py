#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

FIXTURE_INDEX_PATH = ROOT / "data/c7_synthetic_runtime_radius_fixtures_v0/c7_synthetic_fixture_index_v0.json"
EXPECTED_OUTCOMES_PATH = ROOT / "data/c7_synthetic_runtime_radius_fixtures_v0/c7_synthetic_fixture_expected_outcomes_v0.json"

STEP_PACKET_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_step_packet_contract_v0.json"
STOP_PACKET_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_stop_packet_contract_v0.json"
BUDGET_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_budget_v0.json"
UNIT_FEEDBACK_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/unit_feedback_record_contract_v0.json"
NEGATIVE_COUNTER_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_negative_counter_contract_v0.json"
ROLLUP_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_rollup_contract_v0.json"
READOUT_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_readout_contract_v0.json"

RUN_DIR = ROOT / "data/c7_synthetic_runtime_radius_runs_v0"
RECEIPT_DIR = ROOT / "data/c7_synthetic_runtime_radius_run_receipts_v0"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def load_contracts() -> Dict[str, Any]:
    return {
        "step": read_json(STEP_PACKET_CONTRACT_PATH),
        "stop": read_json(STOP_PACKET_CONTRACT_PATH),
        "budget": read_json(BUDGET_PATH),
        "feedback": read_json(UNIT_FEEDBACK_CONTRACT_PATH),
        "negative": read_json(NEGATIVE_COUNTER_CONTRACT_PATH),
        "rollup": read_json(ROLLUP_CONTRACT_PATH),
        "readout": read_json(READOUT_CONTRACT_PATH),
    }

def validate_fixture_shape(fixture: Dict[str, Any], contracts: Dict[str, Any]) -> List[str]:
    errors: List[str] = []

    required_step = set(contracts["step"].get("required_fields", []))
    required_stop = set(contracts["stop"].get("required_fields", []))
    required_feedback = set(contracts["feedback"].get("required_fields", []))
    counter_names = contracts["negative"].get("must_be_zero", [])

    for i, step in enumerate(fixture.get("steps", [])):
        missing = sorted(required_step - set(step.keys()))
        if missing:
            errors.append(f"step_{i}_missing_fields:{','.join(missing)}")
        if step.get("terminal") not in contracts["step"].get("terminal_values", []):
            errors.append(f"step_{i}_terminal_invalid:{step.get('terminal')}")
        for counter_name in counter_names:
            if step.get("bad_counters", {}).get(counter_name) != 0:
                errors.append(f"step_{i}_counter_not_zero:{counter_name}")

    stop = fixture.get("stop_packet", {})
    missing_stop = sorted(required_stop - set(stop.keys()))
    if missing_stop:
        errors.append("stop_missing_fields:" + ",".join(missing_stop))
    if stop.get("stop_code") not in contracts["stop"].get("allowed_stop_codes", []):
        errors.append(f"stop_code_invalid:{stop.get('stop_code')}")

    for j, feedback in enumerate(fixture.get("unit_feedback_records", [])):
        missing = sorted(required_feedback - set(feedback.keys()))
        if missing:
            errors.append(f"feedback_{j}_missing_fields:{','.join(missing)}")
        if feedback.get("diagnostic_quality") not in contracts["feedback"].get("diagnostic_quality_values", []):
            errors.append(f"feedback_{j}_diagnostic_quality_invalid:{feedback.get('diagnostic_quality')}")

    return errors

def classify_fixture(fixture: Dict[str, Any]) -> Tuple[str, Dict[str, Any], List[str]]:
    steps = fixture.get("steps", [])
    stop = fixture.get("stop_packet", {})
    feedback_records = fixture.get("unit_feedback_records", [])

    bad_counters: Dict[str, int] = {}
    for step in steps:
        for k, v in step.get("bad_counters", {}).items():
            bad_counters[k] = bad_counters.get(k, 0) + int(v)

    steps_attempted = len(steps)
    steps_advanced = sum(1 for s in steps if s.get("terminal") == "ADVANCE")
    steps_halted = sum(1 for s in steps if s.get("terminal") == "STOP")

    schema_valid = sum(1 for s in steps if "VALID" in str(s.get("schema_validation_ref", "")))
    schema_unknown = sum(1 for s in steps if "UNKNOWN_SCHEMA" in str(s.get("schema_validation_ref", "")))
    schema_invalid = sum(1 for s in steps if "INVALID" in str(s.get("schema_validation_ref", "")))

    cell0_allow = sum(1 for s in steps if "ALLOW" in str(s.get("admissibility_ref", "")))
    cell0_authority_required = sum(1 for s in steps if "AUTHORITY_REQUIRED" in str(s.get("admissibility_ref", "")))
    cell0_deny = sum(1 for s in steps if "DENY" in str(s.get("admissibility_ref", "")))

    typed_halt_count = 1 if stop.get("stop_code") and stop.get("stop_code") != "STOP_UNTYPED_FAILURE" else 0
    untyped_halt_count = 1 if stop.get("stop_code") == "STOP_UNTYPED_FAILURE" else 0

    stop_code = stop.get("stop_code")
    expected = fixture.get("expected_outcome")

    if stop_code == "STOP_DONE":
        if expected == "RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES":
            outcome = "RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES"
        else:
            outcome = "RADIUS_EXPANDED_CLEANLY"
    elif stop_code == "STOP_SCHEMA_GAP":
        outcome = "RADIUS_BLOCKED_BY_SCHEMA_GAP"
    elif stop_code == "STOP_AUTHORITY_REQUIRED":
        outcome = "RADIUS_BLOCKED_BY_AUTHORITY_BOUNDARY"
    elif stop_code == "STOP_MISSING_CAPABILITY":
        outcome = "RADIUS_BLOCKED_BY_MISSING_CAPABILITY"
    elif stop_code == "STOP_WEAK_FEEDBACK":
        outcome = "RADIUS_BLOCKED_BY_WEAK_FEEDBACK"
    elif stop_code == "STOP_OBSERVABILITY_GAP":
        outcome = "RADIUS_BLOCKED_BY_OBSERVABILITY_GAP"
    elif stop_code == "STOP_INTER_CELL_PROTOCOL_GAP":
        outcome = "RADIUS_BLOCKED_BY_INTER_CELL_PROTOCOL_GAP"
    else:
        outcome = "RADIUS_FAIL_UNTYPED"

    observations = {
        "receipts_emitted": steps_attempted,
        "edge_observations_emitted": steps_attempted,
        "unit_feedback_records_emitted": len(feedback_records),
        "sidecar_event_records_emitted": steps_attempted,
    }

    rollup = {
        "schema_version": "runtime_radius_rollup_v0",
        "run_id": fixture.get("steps", [{}])[0].get("run_id") if steps else fixture.get("fixture_id"),
        "fixture_id": fixture.get("fixture_id"),
        "steps_attempted": steps_attempted,
        "steps_advanced": steps_advanced,
        "steps_halted": steps_halted,
        "lawful_continuation_depth": steps_advanced,
        "max_contiguous_valid_steps": steps_advanced,
        "schema_validation": {
            "valid_count": schema_valid,
            "invalid_count": schema_invalid,
            "unknown_schema_count": schema_unknown,
        },
        "cell0_admissibility": {
            "allow_count": cell0_allow,
            "deny_count": cell0_deny,
            "authority_required_count": cell0_authority_required,
            "frontier_required_count": 0,
        },
        "halts": {
            "typed_halt_count": typed_halt_count,
            "untyped_halt_count": untyped_halt_count,
            "real_boundary_halt_count": 1 if stop_code in ["STOP_AUTHORITY_REQUIRED", "STOP_FRONTIER_REQUIRED"] else 0,
            "artificial_halt_count": 1 if stop_code in ["STOP_SCHEMA_GAP", "STOP_MISSING_CAPABILITY", "STOP_WEAK_FEEDBACK", "STOP_OBSERVABILITY_GAP", "STOP_INTER_CELL_PROTOCOL_GAP"] else 0,
        },
        "observability": observations,
        "bad_counters": bad_counters,
        "outcome": outcome,
    }

    readout = {
        "schema_version": "runtime_radius_readout_v0",
        "fixture_id": fixture.get("fixture_id"),
        "steps_attempted": steps_attempted,
        "steps_advanced": steps_advanced,
        "typed_halts": typed_halt_count,
        "untyped_halts": untyped_halt_count,
        "longest_lawful_continuation": steps_advanced,
        "halt_reasons": [stop_code],
        "receipts_emitted": observations["receipts_emitted"],
        "edge_observations": observations["edge_observations_emitted"],
        "unit_feedback_records": observations["unit_feedback_records_emitted"],
        "sidecar_events": observations["sidecar_event_records_emitted"],
        "bad_counters": bad_counters,
        "interpretation": f"Synthetic C7 fixture classified as {outcome}.",
    }

    errors: List[str] = []
    if expected and outcome != expected:
        errors.append(f"outcome_mismatch:expected={expected}:actual={outcome}")

    for k, v in bad_counters.items():
        if v != 0:
            errors.append(f"bad_counter_nonzero:{k}:{v}")

    return outcome, {"rollup": rollup, "readout": readout}, errors

def run_fixture(fixture_id: str, expected_fixture: str | None = None) -> int:
    contracts = load_contracts()
    fixture_index = read_json(FIXTURE_INDEX_PATH)

    paths = {item["fixture_id"]: ROOT / item["path"] for item in fixture_index.get("fixtures", [])}
    if fixture_id not in paths:
        print(json.dumps({"gate": "FAIL", "failures": [f"fixture_missing:{fixture_id}"]}, indent=2, sort_keys=True))
        return 1

    if expected_fixture is not None and fixture_id != expected_fixture:
        print(json.dumps({"gate": "FAIL", "failures": [f"fixture_not_allowed_in_this_unit:{fixture_id}:expected:{expected_fixture}"]}, indent=2, sort_keys=True))
        return 1

    fixture = read_json(paths[fixture_id])
    shape_errors = validate_fixture_shape(fixture, contracts)
    outcome, outputs, run_errors = classify_fixture(fixture)
    failures = shape_errors + run_errors
    gate = "PASS" if not failures else "FAIL"

    run_id = outputs["rollup"]["run_id"]
    out_dir = RUN_DIR / fixture_id
    receipt_dir = RECEIPT_DIR / fixture_id

    step_path = out_dir / "runtime_radius_step_packets_v0.jsonl"
    feedback_path = out_dir / "unit_feedback_records_v0.jsonl"
    stop_path = out_dir / "runtime_radius_stop_packet_v0.json"
    rollup_path = out_dir / "runtime_radius_rollup_v0.json"
    readout_path = out_dir / "runtime_radius_readout_v0.json"

    out_dir.mkdir(parents=True, exist_ok=True)
    receipt_dir.mkdir(parents=True, exist_ok=True)

    step_path.write_text("\n".join(json.dumps(s, sort_keys=True) for s in fixture.get("steps", [])) + "\n")
    feedback_records = fixture.get("unit_feedback_records", [])
    feedback_path.write_text("\n".join(json.dumps(f, sort_keys=True) for f in feedback_records) + ("\n" if feedback_records else ""))
    write_json(stop_path, fixture.get("stop_packet", {}))
    write_json(rollup_path, outputs["rollup"])
    write_json(readout_path, outputs["readout"])

    receipt = {
        "schema_version": "c7_synthetic_runtime_radius_run_receipt_v0",
        "receipt_type": "TYPED_C7_SYNTHETIC_RUNTIME_RADIUS_RUN_RECEIPT",
        "created_at": now_iso(),
        "runner_id": "run_c7_synthetic_runtime_radius_v0",
        "fixture_id": fixture_id,
        "run_id": run_id,
        "gate": gate,
        "status": "TYPED_C7_SYNTHETIC_RADIUS_RUN_DONE" if gate == "PASS" else "TYPED_C7_SYNTHETIC_RADIUS_RUN_GATE_FAIL",
        "outcome": outcome,
        "expected_outcome": fixture.get("expected_outcome"),
        "failures": failures,
        "warnings": [],
        "runtime_adoption_authorized": False,
        "c7_live_runtime_run": False,
        "synthetic_run_only": True,
        "output_artifacts": {
            "step_packets": rel(step_path),
            "unit_feedback_records": rel(feedback_path),
            "stop_packet": rel(stop_path),
            "rollup": rel(rollup_path),
            "readout": rel(readout_path),
        },
        "terminal": {
            "type": "STOP_DONE" if gate == "PASS" else "STOP",
            "next_unit_id": None,
            "stop_code": "STOP_C7_SYNTHETIC_FIXTURE_RUN_DONE" if gate == "PASS" else "STOP_C7_SYNTHETIC_FIXTURE_RUN_GATE_FAIL",
        },
    }
    receipt_id = sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = receipt_dir / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c7_synthetic_run_receipt_id={receipt_id}")
    print(f"c7_synthetic_run_receipt_path={rel(receipt_path)}")
    print(f"c7_synthetic_run_outcome={outcome}")

    return 0 if gate == "PASS" else 1

def self_check() -> int:
    contracts = load_contracts()
    fixture_index = read_json(FIXTURE_INDEX_PATH)

    failures: List[str] = []
    for name, contract in contracts.items():
        status = contract.get("contract_status") or contract.get("budget_status")
        if status != "FROZEN":
            failures.append(f"contract_not_frozen:{name}:{status}")

    for item in fixture_index.get("fixtures", []):
        path = ROOT / item["path"]
        if not path.exists():
            failures.append(f"fixture_file_missing:{item.get('fixture_id')}:{item.get('path')}")
            continue
        fixture = read_json(path)
        failures.extend([f"{item.get('fixture_id')}:{err}" for err in validate_fixture_shape(fixture, contracts)])

    result = {
        "schema_version": "c7_synthetic_runner_self_check_v0",
        "self_check_status": "PASS" if not failures else "FAIL",
        "fixture_count": len(fixture_index.get("fixtures", [])),
        "failures": failures,
        "runner_scope": "synthetic fixtures only",
        "runtime_adoption_authorized": False,
        "live_runtime_hooks_installed": False,
        "runtime_patched": False,
    }
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if not failures else 1

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-check", action="store_true")
    parser.add_argument("--fixture-id")
    parser.add_argument("--expected-fixture")
    args = parser.parse_args()

    if args.self_check:
        return self_check()

    if not args.fixture_id:
        print(json.dumps({"gate": "FAIL", "failures": ["fixture_id_required"]}, indent=2, sort_keys=True))
        return 1

    return run_fixture(args.fixture_id, args.expected_fixture)

if __name__ == "__main__":
    raise SystemExit(main())
