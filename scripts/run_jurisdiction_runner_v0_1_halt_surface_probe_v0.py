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
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RUN_JURISDICTION_RUNNER_V0_1_HALT_SURFACE_PROBE_V0"

HALT_SURFACE_PROBE_POLICY_ID = "cfe745b9"
HALT_SURFACE_PROBE_POLICY_RECEIPT_ID = "7bb73d50"
IMPLEMENTATION_RECEIPT_ID = "04c0692d"
LOCAL_REGIME_HASH = "097d620c"

RUNNER_UNIT_ID = "jurisdiction_runner.v0.1"
LOCAL_REGIME_VERSION = "local_regime.v0"

POLICY_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_policies" / f"{HALT_SURFACE_PROBE_POLICY_ID}.json"
POLICY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_policy_receipts" / f"{HALT_SURFACE_PROBE_POLICY_ID}.json"
IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_implementation_receipts" / f"{IMPLEMENTATION_RECEIPT_ID}.json"
LOCAL_REGIME_PATH = ROOT / "data" / "local_regime_v0_declarations" / f"{LOCAL_REGIME_HASH}.json"
RUNNER_MODULE_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_1.py"

FIXTURE_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_fixtures"
TRANSCRIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_expected_transcripts"
REGIME_VARIANT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_regime_variants"
CASE_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_case_receipts"
RUN_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_run_receipts"

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

COVERAGE_GOAL = [
    "STOP_DONE",
    "STOP_NO_APPLICABLE_MOVE",
    "STOP_AUTHORITY_VIOLATION",
    "STOP_GATE_FAIL",
    "STOP_UNTYPED_OBJECT",
    "STOP_DEPENDENCY_MISSING",
]

IMPLEMENTATION_TRUE_GUARDS = [
    "bootstrap_policy_consumed",
    "runner_implemented",
    "runner_executed",
    "dry_run_fixture_created",
    "dry_run_fixture_executed",
    "expected_transcript_created",
    "local_regime_v0_declared",
]

IMPLEMENTATION_FALSE_GUARDS = [
    "local_regime_runtime_mutated",
    "proposal_promoted",
    "registry_written",
    "registry_inserted",
    "registry_sqlite_read",
    "registry_sqlite_written",
    "full_registry_scan_used",
    "global_taxonomy_claimed",
    "final_schema_claimed",
    "proof_claimed",
    "hidden_continuation_authorized",
]

CASE_FALSE_GUARDS = [
    "local_regime_runtime_mutated",
    "proposal_promoted",
    "registry_written",
    "registry_inserted",
    "registry_sqlite_read",
    "registry_sqlite_written",
    "full_registry_scan_used",
    "proof_claimed",
    "global_taxonomy_claimed",
    "final_schema_claimed",
    "hidden_continuation_authorized",
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

def tracked(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    result = subprocess.run(
        ["git", "ls-files", "--error-unmatch", rel],
        cwd=ROOT,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0

def import_runner():
    spec = importlib.util.spec_from_file_location("jurisdiction_runner_v0_1", RUNNER_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import jurisdiction runner module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["jurisdiction_runner_v0_1"] = mod
    spec.loader.exec_module(mod)
    return mod

def validate_policy_inputs(
    policy: Dict[str, Any],
    receipt: Dict[str, Any],
    implementation: Dict[str, Any],
    local_regime: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if policy.get("policy_id") != HALT_SURFACE_PROBE_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy.get("policy_receipt_id") != HALT_SURFACE_PROBE_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if receipt.get("policy_id") != HALT_SURFACE_PROBE_POLICY_ID:
        failures.append(f"receipt_policy_id_wrong:{receipt.get('policy_id')}")
    if receipt.get("receipt_id") != HALT_SURFACE_PROBE_POLICY_RECEIPT_ID:
        failures.append(f"receipt_id_wrong:{receipt.get('receipt_id')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{receipt.get('policy_status')}")

    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"policy_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"policy_terminal_stop_not_null:{terminal.get('stop_code')}")

    authorized = receipt.get("authorized_operations_next") or {}
    for key in [
        "read_halt_surface_probe_policy",
        "read_halt_surface_probe_policy_receipt",
        "read_runner_module",
        "read_local_regime_v0_declaration",
        "create_halt_surface_probe_fixtures",
        "create_expected_probe_transcripts",
        "execute_runner_against_probe_fixtures",
        "execute_wrapper_dependency_missing_probe",
        "emit_halt_surface_probe_receipt",
    ]:
        if authorized.get(key) is not True:
            failures.append(f"authorized_operation_missing:{key}:{authorized.get(key)}")

    forbidden = receipt.get("forbidden_operations") or {}
    for key in [
        "modify_runner_module",
        "promote_probe_regime_variant",
        "replace_local_regime_v0",
        "mutate_local_regime_at_runtime",
        "promote_proposals",
        "registry_sqlite_write",
        "registry_sqlite_read",
        "full_registry_scan",
        "global_taxonomy_design",
        "final_schema_claim",
        "proof_claim",
    ]:
        if forbidden.get(key) is not True:
            failures.append(f"forbidden_operation_not_declared:{key}:{forbidden.get(key)}")

    if implementation.get("receipt_id") != IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"implementation_receipt_id_wrong:{implementation.get('receipt_id')}")
    if implementation.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{implementation.get('gate')}")
    if implementation.get("terminal", {}).get("type") != "STOP":
        failures.append(f"implementation_terminal_not_STOP:{implementation.get('terminal')}")
    if implementation.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append(f"implementation_terminal_stop_not_STOP_DONE:{implementation.get('terminal')}")
    if implementation.get("local_regime_hash") != LOCAL_REGIME_HASH:
        failures.append(f"implementation_regime_hash_wrong:{implementation.get('local_regime_hash')}")

    implementation_guards = implementation.get("authority_guards") or {}
    for key in IMPLEMENTATION_TRUE_GUARDS:
        if implementation_guards.get(key) is not True:
            failures.append(f"implementation_guard_not_true:{key}:{implementation_guards.get(key)}")
    for key in IMPLEMENTATION_FALSE_GUARDS:
        if implementation_guards.get(key) is not False:
            failures.append(f"implementation_guard_not_false:{key}:{implementation_guards.get(key)}")

    if local_regime.get("local_regime_version") != LOCAL_REGIME_VERSION:
        failures.append(f"local_regime_version_wrong:{local_regime.get('local_regime_version')}")
    if local_regime.get("local_regime_hash") != LOCAL_REGIME_HASH:
        failures.append(f"local_regime_hash_wrong:{local_regime.get('local_regime_hash')}")
    for halt in COVERAGE_GOAL:
        if halt not in local_regime.get("halt_vocabulary", []):
            failures.append(f"local_regime_missing_halt:{halt}")

    for path, label in [
        (POLICY_PATH, "halt_surface_probe_policy"),
        (POLICY_RECEIPT_PATH, "halt_surface_probe_policy_receipt"),
        (IMPLEMENTATION_RECEIPT_PATH, "implementation_receipt"),
        (LOCAL_REGIME_PATH, "local_regime"),
        (RUNNER_MODULE_PATH, "runner_module"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{path.relative_to(ROOT).as_posix()}")

    return failures

def build_case_fixture(case_name: str, case_spec: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "schema_version": "jurisdiction_runner_v0_1_halt_surface_probe_fixture_v0",
        "fixture_id": f"halt_surface_probe_{case_name.lower()}",
        "case_name": case_name,
        "fixture_kind": case_spec["fixture_kind"],
        "input_state": case_spec.get("input_state"),
        "missing_dependency_path": case_spec.get("missing_dependency_path"),
        "expected": case_spec["expected"],
        "expected_transcript": EXPECTED_TRANSCRIPT if case_spec["expected"]["runner_executes"] else [],
    }

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def make_dependency_missing_receipt(fixture: Dict[str, Any], missing_path: str) -> Dict[str, Any]:
    case_name = fixture["case_name"]
    seed = {
        "unit_id": UNIT_ID,
        "case_name": case_name,
        "missing_dependency_path": missing_path,
        "halt_code": "STOP_DEPENDENCY_MISSING",
    }
    receipt_id = sha8(seed)
    metrics = {
        "move_count": 0,
        "applied_move_count": 0,
        "blocked_move_count": 1,
        "halt_count_by_code": {"STOP_DEPENDENCY_MISSING": 1},
        "typed_object_count": 0,
        "untyped_object_count": 0,
        "missing_dependency_count": 1,
        "receipt_count": 1,
        "authority_violation_count": 0,
        "gate_fail_count": 0,
        "proposal_emitted_count": 0,
        "proposal_withheld_count": 1,
        "proposal_count_by_type": {},
        "duplicate_unresolved_proposal_count": 0,
        "halt_with_proposal_count": 0,
        "halt_without_proposal_count": 1,
        "local_closure_radius_observed": 0,
        "receipt_burden_bytes": 0,
        "metric_burden_bytes": 0,
        "artifact_burden_bytes": len(missing_path.encode("utf-8")),
    }
    receipt: Dict[str, Any] = {
        "receipt_id": receipt_id,
        "receipt_type": "JURISDICTION_RUNNER_V0_1_HALT_SURFACE_PROBE_CASE_RECEIPT",
        "unit_id": UNIT_ID,
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": LOCAL_REGIME_HASH,
        "case_name": case_name,
        "fixture_id": fixture["fixture_id"],
        "fixture_kind": fixture["fixture_kind"],
        "runner_executed": False,
        "missing_dependency_path": missing_path,
        "dependency_exists": False,
        "selected_move_id": None,
        "move_status": "BLOCKED",
        "halt_code": "STOP_DEPENDENCY_MISSING",
        "halt_reason": f"required dependency missing before runner execution: {missing_path}",
        "proposal_status": "NONE",
        "proposal_id": None,
        "no_proposal_reason": "PRESSURE_ALREADY_TYPED",
        "metrics": metrics,
        "authority_guards": {
            "runner_executed": False,
            "local_regime_runtime_mutated": False,
            "proposal_promoted": False,
            "registry_written": False,
            "registry_inserted": False,
            "registry_sqlite_read": False,
            "registry_sqlite_written": False,
            "full_registry_scan_used": False,
            "proof_claimed": False,
            "global_taxonomy_claimed": False,
            "final_schema_claimed": False,
            "hidden_continuation_authorized": False,
        },
        "artifact_guards": {
            "missing_dependency_detected_before_runner": True,
            "input_artifacts_path_addressed": True,
            "output_artifacts_receipt_referenced": True,
            "unrelated_untracked_data_not_authority": True,
            "latest_or_mtime_selection_used": False,
            "ambient_workspace_authority_used": False,
        },
        "transcript": [],
        "expected_transcript": [],
        "transcript_matches_expected": True,
        "terminal": {
            "type": "STOP",
            "next_command_goal": None,
            "stop_code": "STOP_DEPENDENCY_MISSING",
        },
        "gate": "PASS",
        "failures": [],
        "warnings": [],
        "created_at": now_iso(),
    }
    receipt["metrics"]["receipt_burden_bytes"] = burden_bytes(receipt)
    receipt["metrics"]["metric_burden_bytes"] = burden_bytes(receipt["metrics"])
    return receipt

def normalize_runner_receipt(case_name: str, fixture: Dict[str, Any], receipt: Dict[str, Any]) -> Dict[str, Any]:
    out = copy.deepcopy(receipt)
    out["receipt_type"] = "JURISDICTION_RUNNER_V0_1_HALT_SURFACE_PROBE_CASE_RECEIPT"
    out["probe_unit_id"] = UNIT_ID
    out["case_name"] = case_name
    out["fixture_kind"] = fixture["fixture_kind"]
    out["runner_executed"] = True
    return out

def validate_case_receipt(case_name: str, fixture: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    expected = fixture["expected"]

    if receipt.get("gate") != "PASS":
        failures.append(f"{case_name}:gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("halt_code") != expected["halt_code"]:
        failures.append(f"{case_name}:halt_code_wrong:{receipt.get('halt_code')}")
    if receipt.get("move_status") != expected["move_status"]:
        failures.append(f"{case_name}:move_status_wrong:{receipt.get('move_status')}")
    if receipt.get("proposal_status") != expected["proposal_status"]:
        failures.append(f"{case_name}:proposal_status_wrong:{receipt.get('proposal_status')}")
    if receipt.get("no_proposal_reason") != expected["no_proposal_reason"]:
        failures.append(f"{case_name}:no_proposal_reason_wrong:{receipt.get('no_proposal_reason')}")
    if receipt.get("runner_executed") != expected["runner_executes"]:
        failures.append(f"{case_name}:runner_executes_wrong:{receipt.get('runner_executed')}")

    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "STOP":
        failures.append(f"{case_name}:terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != expected["halt_code"]:
        failures.append(f"{case_name}:terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"{case_name}:terminal_next_not_null:{terminal.get('next_command_goal')}")

    metrics = receipt.get("metrics") or {}
    if metrics.get("halt_count_by_code", {}).get(expected["halt_code"]) != 1:
        failures.append(f"{case_name}:halt_metric_missing:{metrics.get('halt_count_by_code')}")
    if expected["runner_executes"]:
        if receipt.get("transcript") != EXPECTED_TRANSCRIPT:
            failures.append(f"{case_name}:transcript_mismatch:{receipt.get('transcript')}")
        if receipt.get("transcript_matches_expected") is not True:
            failures.append(f"{case_name}:transcript_match_not_true:{receipt.get('transcript_matches_expected')}")
    else:
        if metrics.get("missing_dependency_count") != 1:
            failures.append(f"{case_name}:missing_dependency_metric_wrong:{metrics.get('missing_dependency_count')}")

    authority = receipt.get("authority_guards") or {}
    for key in CASE_FALSE_GUARDS:
        if authority.get(key) is not False:
            failures.append(f"{case_name}:authority_guard_not_false:{key}:{authority.get(key)}")

    artifact = receipt.get("artifact_guards") or {}
    for key in [
        "latest_or_mtime_selection_used",
        "ambient_workspace_authority_used",
    ]:
        if artifact.get(key) is not False:
            failures.append(f"{case_name}:artifact_guard_not_false:{key}:{artifact.get(key)}")

    return failures

def main() -> int:
    policy = read_json(POLICY_PATH)
    policy_receipt = read_json(POLICY_RECEIPT_PATH)
    implementation = read_json(IMPLEMENTATION_RECEIPT_PATH)
    local_regime = read_json(LOCAL_REGIME_PATH)

    failures = validate_policy_inputs(policy, policy_receipt, implementation, local_regime)

    runner_mod = import_runner()

    plan = policy_receipt["halt_surface_probe_plan"]
    case_specs = plan["required_probe_cases"]

    for d in [FIXTURE_DIR, TRANSCRIPT_DIR, REGIME_VARIANT_DIR, CASE_RECEIPT_DIR, RUN_RECEIPT_DIR]:
        d.mkdir(parents=True, exist_ok=True)

    case_results: Dict[str, Dict[str, Any]] = {}
    covered_halts = set(plan["already_covered"].keys())

    for case_name in sorted(case_specs.keys()):
        case_spec = case_specs[case_name]
        fixture = build_case_fixture(case_name, case_spec)
        fixture_path = FIXTURE_DIR / f"{fixture['fixture_id']}.json"
        transcript_path = TRANSCRIPT_DIR / f"{fixture['fixture_id']}.json"

        write_json(fixture_path, fixture)
        write_json(transcript_path, {
            "schema_version": "jurisdiction_runner_v0_1_halt_surface_probe_expected_transcript_v0",
            "fixture_id": fixture["fixture_id"],
            "case_name": case_name,
            "expected_transcript": EXPECTED_TRANSCRIPT if case_spec["expected"]["runner_executes"] else [],
        })

        if case_name == "STOP_DEPENDENCY_MISSING":
            missing_path = case_spec["missing_dependency_path"]
            if (ROOT / missing_path).exists():
                failures.append(f"{case_name}:missing_dependency_unexpectedly_exists:{missing_path}")
            receipt = make_dependency_missing_receipt(fixture, missing_path)
        else:
            regime_for_case = copy.deepcopy(local_regime)
            regime_variant_path = None

            if case_name == "STOP_AUTHORITY_VIOLATION":
                regime_for_case["schema_version"] = "local_regime_v0_controlled_probe_variant_v0"
                regime_for_case["regime_status"] = "CONTROLLED_PROBE_VARIANT_NOT_PROMOTED"
                regime_for_case["jurisdiction_envelope"]["allowed_move_ids"] = []
                regime_for_case["variant_of_local_regime_hash"] = LOCAL_REGIME_HASH
                regime_for_case["variant_is_not_promotion"] = True
                regime_for_case["variant_must_not_replace_local_regime_v0"] = True
                regime_for_case["local_regime_hash"] = sha8({
                    "variant": "authority_violation_empty_allowed_moves",
                    "base": LOCAL_REGIME_HASH,
                    "case": case_name,
                })
                regime_variant_path = REGIME_VARIANT_DIR / f"{regime_for_case['local_regime_hash']}.json"
                write_json(regime_variant_path, regime_for_case)

            runner = runner_mod.JurisdictionRunnerV01(regime_for_case)
            receipt = runner.run(
                case_spec["input_state"],
                fixture_id=fixture["fixture_id"],
                input_artifact_paths=[
                    LOCAL_REGIME_PATH.relative_to(ROOT).as_posix() if regime_variant_path is None else regime_variant_path.relative_to(ROOT).as_posix(),
                    fixture_path.relative_to(ROOT).as_posix(),
                    transcript_path.relative_to(ROOT).as_posix(),
                ],
            )
            receipt = normalize_runner_receipt(case_name, fixture, receipt)
            if regime_variant_path is not None:
                receipt["controlled_probe_regime_variant_path"] = regime_variant_path.relative_to(ROOT).as_posix()
                receipt["controlled_probe_regime_variant_promoted"] = False
                receipt["base_local_regime_hash"] = LOCAL_REGIME_HASH

        failures.extend(validate_case_receipt(case_name, fixture, receipt))

        case_receipt_path = CASE_RECEIPT_DIR / f"{receipt['receipt_id']}.json"
        write_json(case_receipt_path, receipt)

        covered_halts.add(receipt["halt_code"])
        case_results[case_name] = {
            "case_name": case_name,
            "fixture_id": fixture["fixture_id"],
            "fixture_path": fixture_path.relative_to(ROOT).as_posix(),
            "expected_transcript_path": transcript_path.relative_to(ROOT).as_posix(),
            "case_receipt_id": receipt["receipt_id"],
            "case_receipt_path": case_receipt_path.relative_to(ROOT).as_posix(),
            "halt_code": receipt["halt_code"],
            "move_status": receipt["move_status"],
            "proposal_status": receipt["proposal_status"],
            "no_proposal_reason": receipt["no_proposal_reason"],
            "runner_executed": receipt["runner_executed"],
            "gate": receipt["gate"],
        }

    missing_coverage = [halt for halt in COVERAGE_GOAL if halt not in covered_halts]
    if missing_coverage:
        failures.append(f"coverage_missing:{missing_coverage}")

    aggregate_metrics = {
        "coverage_goal_count": len(COVERAGE_GOAL),
        "covered_halt_count": len([halt for halt in COVERAGE_GOAL if halt in covered_halts]),
        "new_probe_case_count": len(case_results),
        "runner_executed_probe_count": sum(1 for r in case_results.values() if r["runner_executed"]),
        "wrapper_boundary_probe_count": sum(1 for r in case_results.values() if not r["runner_executed"]),
        "case_receipt_count": len(case_results),
        "case_pass_count": sum(1 for r in case_results.values() if r["gate"] == "PASS"),
        "case_fail_count": sum(1 for r in case_results.values() if r["gate"] != "PASS"),
        "proposal_promoted_count": 0,
        "registry_write_count": 0,
        "controlled_probe_regime_variant_count": 1,
        "controlled_probe_regime_variant_promoted_count": 0,
    }

    authority_guards = {
        "halt_surface_probe_policy_consumed": True,
        "runner_module_read": True,
        "runner_module_changed": False,
        "local_regime_read": True,
        "local_regime_replaced": False,
        "local_regime_runtime_mutated": False,
        "probe_fixtures_created": True,
        "probe_fixtures_executed": True,
        "wrapper_dependency_missing_probe_executed": True,
        "controlled_probe_regime_variant_created": True,
        "controlled_probe_regime_variant_promoted": False,
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
        "policy_tracked": tracked(POLICY_PATH),
        "policy_receipt_tracked": tracked(POLICY_RECEIPT_PATH),
        "implementation_receipt_tracked": tracked(IMPLEMENTATION_RECEIPT_PATH),
        "local_regime_tracked": tracked(LOCAL_REGIME_PATH),
        "runner_module_tracked": tracked(RUNNER_MODULE_PATH),
        "outputs_path_addressed": True,
        "outputs_receipt_referenced": True,
        "unrelated_untracked_data_not_authority": True,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_authority_used": False,
    }

    run_seed = {
        "unit_id": UNIT_ID,
        "policy_id": HALT_SURFACE_PROBE_POLICY_ID,
        "policy_receipt_id": HALT_SURFACE_PROBE_POLICY_RECEIPT_ID,
        "implementation_receipt_id": IMPLEMENTATION_RECEIPT_ID,
        "covered_halts": sorted(covered_halts),
        "case_receipts": {k: v["case_receipt_id"] for k, v in sorted(case_results.items())},
    }
    run_receipt_id = sha8(run_seed)

    run_receipt = {
        "schema_version": "jurisdiction_runner_v0_1_halt_surface_probe_run_receipt_v0",
        "receipt_type": "JURISDICTION_RUNNER_V0_1_HALT_SURFACE_PROBE_RUN_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": run_receipt_id,
        "source_halt_surface_probe_policy_id": HALT_SURFACE_PROBE_POLICY_ID,
        "source_halt_surface_probe_policy_receipt_id": HALT_SURFACE_PROBE_POLICY_RECEIPT_ID,
        "source_implementation_receipt_id": IMPLEMENTATION_RECEIPT_ID,
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": LOCAL_REGIME_HASH,
        "coverage_goal": COVERAGE_GOAL,
        "previously_covered_halts": sorted(plan["already_covered"].keys()),
        "newly_probed_halts": sorted([r["halt_code"] for r in case_results.values()]),
        "covered_halts_after_probe": sorted([halt for halt in COVERAGE_GOAL if halt in covered_halts]),
        "coverage_complete": len(missing_coverage) == 0,
        "missing_coverage": missing_coverage,
        "case_results": case_results,
        "aggregate_metrics": aggregate_metrics,
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

    run_receipt_path = RUN_RECEIPT_DIR / f"{run_receipt_id}.json"
    write_json(run_receipt_path, run_receipt)

    print(json.dumps(run_receipt, indent=2, sort_keys=True))
    print(f"halt_surface_probe_run_receipt_id={run_receipt_id}")
    print(f"halt_surface_probe_run_receipt_path=data/jurisdiction_runner_v0_1_halt_surface_probe_run_receipts/{run_receipt_id}.json")
    for case_name, result in sorted(case_results.items()):
        print(f"case_{case_name}_fixture_path={result['fixture_path']}")
        print(f"case_{case_name}_expected_transcript_path={result['expected_transcript_path']}")
        print(f"case_{case_name}_receipt_id={result['case_receipt_id']}")
        print(f"case_{case_name}_receipt_path={result['case_receipt_path']}")
    return 0 if run_receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
