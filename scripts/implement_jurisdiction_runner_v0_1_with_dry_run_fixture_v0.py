#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]
SRC_MODULE_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_1.py"

UNIT_ID = "IMPLEMENT_JURISDICTION_RUNNER_V0_1_WITH_DRY_RUN_FIXTURE_V0"
BOOTSTRAP_POLICY_ID = "0fe04fb5"
BOOTSTRAP_POLICY_RECEIPT_ID = "bc448c6d"
BOOTSTRAP_POLICY_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_bootstrap_policies" / f"{BOOTSTRAP_POLICY_ID}.json"
BOOTSTRAP_POLICY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_bootstrap_policy_receipts" / f"{BOOTSTRAP_POLICY_ID}.json"

LOCAL_REGIME_DIR = ROOT / "data" / "local_regime_v0_declarations"
FIXTURE_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_dry_run_fixtures"
TRANSCRIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_expected_transcripts"
DRY_RUN_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_dry_run_receipts"
IMPLEMENTATION_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_implementation_receipts"

RUNNER_UNIT_ID = "jurisdiction_runner.v0.1"
LOCAL_REGIME_VERSION = "local_regime.v0"

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

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def stable_hash(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"STOP_DEPENDENCY_MISSING: missing required file {path}")
    return json.loads(path.read_text())

def run_git_ls_files(path: Path) -> bool:
    rel = path.relative_to(ROOT).as_posix()
    result = subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=ROOT, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

def import_runner():
    spec = importlib.util.spec_from_file_location("jurisdiction_runner_v0_1", SRC_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import jurisdiction runner module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["jurisdiction_runner_v0_1"] = mod
    spec.loader.exec_module(mod)
    return mod

def build_local_regime(policy_receipt: Dict[str, Any]) -> Dict[str, Any]:
    local_regime_hash = policy_receipt["local_regime_hash"]
    return {
        "schema_version": "local_regime_v0_declaration_v0",
        "regime_status": "ACTIVE",
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": local_regime_hash,
        "runner_unit_id": RUNNER_UNIT_ID,
        "jurisdiction_envelope": {
            "allowed_move_ids": [
                "MOVE_APPLY_REGISTERED_TRANSITION"
            ],
            "forbidden_operations": {
                "runtime_regime_mutation": True,
                "registry_sqlite_write": True,
                "registry_sqlite_read": True,
                "full_registry_scan": True,
                "proposal_promotion_inside_run": True,
                "global_taxonomy_design": True,
                "proof_claim": True,
            },
        },
        "state_schema": {
            "schema_id": "jurisdiction_runner_v0_1_state_schema",
            "required_fields": ["state_id", "typed", "value"],
            "field_types": {
                "state_id": "string",
                "typed": "boolean",
                "value": "integer",
            },
        },
        "move_registry": {
            "MOVE_VALIDATE_STATE": {
                "move_type": "MOVE_VALIDATE_STATE",
                "move_priority": 0,
                "applies_when": {"always": True},
                "action": {"op": "validate_state"},
            },
            "MOVE_APPLY_REGISTERED_TRANSITION": {
                "move_type": "MOVE_APPLY_REGISTERED_TRANSITION",
                "move_priority": 10,
                "applies_when": {"field": "value", "operator": "lt", "value": 1},
                "forbidden_if": {"field": "typed", "operator": "ne", "value": True},
                "action": {"op": "increment", "field": "value", "by": 1},
                "expected_state_delta": {"value": "+1"},
                "expected_receipt_delta": "transition field records before/after/delta",
                "expected_metric_delta": "applied_move_count increments",
                "possible_halt_outputs": ["STOP_DONE", "STOP_AUTHORITY_VIOLATION", "STOP_GATE_FAIL"],
            },
            "MOVE_EMIT_METRIC_RECEIPT": {
                "move_type": "MOVE_EMIT_METRIC_RECEIPT",
                "move_priority": 20,
                "applies_when": {"always": True},
                "action": {"op": "emit_metric_receipt"},
            },
        },
        "halt_vocabulary": policy_receipt["required_halt_codes"],
        "receipt_schema": {
            "receipt_type": "JURISDICTION_RUNNER_RECEIPT",
            "required_fields": [
                "receipt_id",
                "receipt_type",
                "run_id",
                "unit_id",
                "local_regime_version",
                "local_regime_hash",
                "input_state_id",
                "input_artifact_paths",
                "state_before_hash",
                "state_after_hash",
                "selector_rule",
                "selected_move_id",
                "move_id",
                "move_status",
                "halt_code",
                "proposal_status",
                "proposal_id",
                "no_proposal_reason",
                "metrics",
                "authority_guards",
                "artifact_guards",
                "terminal",
            ],
        },
        "metric_bundle": policy_receipt["required_metrics"],
        "validation_gates": {
            "state_must_be_typed": True,
            "state_value_must_be_integer": True,
            "state_value_must_be_non_negative": True,
        },
        "taxonomy_surface": {
            "status": "MINIMAL_V0",
            "no_global_taxonomy_claim": True,
        },
        "proposition_envelope": {
            "allowed_proposal_classes": policy_receipt["allowed_proposal_classes"],
            "forbidden_proposal_classes": policy_receipt["forbidden_proposal_classes"],
            "non_executing": True,
            "requires_review_before_promotion": True,
            "duplicate_unresolved_proposal_guard": True,
        },
        "promotion_rules": {
            "review_receipt_required": True,
            "new_regime_version_required": True,
            "must_not_apply_to_current_run": True,
        },
        "artifact_packaging_rules": {
            "input_artifacts_path_addressed": True,
            "output_artifacts_receipt_referenced": True,
            "required_dependencies_verified": True,
            "tracked_when_permanence_required": True,
            "unrelated_untracked_data_not_authority": True,
        },
        "terminal_command_rules": {
            "advance_authorizes_exact_next_command": True,
            "stop_forbids_automatic_command": True,
            "stop_done_closes_lane": True,
            "recommendation_is_not_command_authority": True,
        },
    }

def build_fixture() -> Dict[str, Any]:
    return {
        "schema_version": "jurisdiction_runner_v0_1_dry_run_fixture_v0",
        "fixture_id": "dry_run_apply_registered_transition_v0",
        "fixture_type": "JURISDICTION_RUNNER_V0_1_DRY_RUN_FIXTURE",
        "description": "Typed state with value 0 should select and apply the registered increment transition, then stop done.",
        "input_state": {
            "state_id": "typed_counter_zero",
            "typed": True,
            "value": 0,
        },
        "expected": {
            "state_after": {
                "state_id": "typed_counter_zero",
                "typed": True,
                "value": 1,
            },
            "selected_move_id": "MOVE_APPLY_REGISTERED_TRANSITION",
            "move_status": "APPLIED",
            "halt_code": "STOP_DONE",
            "proposal_status": "NONE",
            "no_proposal_reason": "PRESSURE_ALREADY_TYPED",
            "terminal": {
                "type": "STOP",
                "next_command_goal": None,
                "stop_code": "STOP_DONE",
            },
        },
    }

def validate_bootstrap(policy: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    if policy.get("policy_id") != BOOTSTRAP_POLICY_ID:
        failures.append(f"bootstrap_policy_id_wrong:{policy.get('policy_id')}")
    if policy.get("policy_receipt_id") != BOOTSTRAP_POLICY_RECEIPT_ID:
        failures.append(f"bootstrap_policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if receipt.get("policy_id") != BOOTSTRAP_POLICY_ID:
        failures.append(f"bootstrap_receipt_policy_id_wrong:{receipt.get('policy_id')}")
    if receipt.get("receipt_id") != BOOTSTRAP_POLICY_RECEIPT_ID:
        failures.append(f"bootstrap_receipt_id_wrong:{receipt.get('receipt_id')}")
    if receipt.get("gate") != "PASS":
        failures.append(f"bootstrap_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"bootstrap_policy_status_wrong:{receipt.get('policy_status')}")
    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"bootstrap_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"bootstrap_terminal_next_wrong:{terminal.get('next_command_goal')}")
    authorized = receipt.get("authorized_operations_next") or {}
    for key in [
        "read_bootstrap_policy",
        "read_bootstrap_policy_receipt",
        "create_local_regime_v0_declaration",
        "implement_jurisdiction_runner_v0_1",
        "create_one_dry_run_fixture",
        "create_expected_dry_run_transcript",
        "emit_implementation_receipt",
    ]:
        if authorized.get(key) is not True:
            failures.append(f"authorized_next_not_true:{key}:{authorized.get(key)}")
    guards = receipt.get("authority_guards") or {}
    if guards.get("bootstrap_policy_built") is not True:
        failures.append(f"bootstrap_policy_built_guard_not_true:{guards.get('bootstrap_policy_built')}")
    for key in [
        "runner_implemented",
        "runner_executed",
        "dry_run_fixture_created",
        "dry_run_fixture_executed",
        "registry_written",
        "registry_sqlite_written",
        "proposal_promoted",
        "proof_claimed",
    ]:
        if guards.get(key) is not False:
            failures.append(f"bootstrap_pre_guard_not_false:{key}:{guards.get(key)}")
    return failures

def validate_dry_run(fixture: Dict[str, Any], receipt: Dict[str, Any]) -> List[str]:
    failures: List[str] = []
    expected = fixture["expected"]

    if receipt.get("gate") != "PASS":
        failures.append(f"dry_run_gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("unit_id") != RUNNER_UNIT_ID:
        failures.append(f"dry_run_unit_wrong:{receipt.get('unit_id')}")
    if receipt.get("local_regime_version") != LOCAL_REGIME_VERSION:
        failures.append(f"dry_run_regime_version_wrong:{receipt.get('local_regime_version')}")
    if receipt.get("transcript") != EXPECTED_TRANSCRIPT:
        failures.append("dry_run_transcript_mismatch")
    if receipt.get("transcript_matches_expected") is not True:
        failures.append(f"dry_run_transcript_match_not_true:{receipt.get('transcript_matches_expected')}")
    if receipt.get("state_after") != expected["state_after"]:
        failures.append(f"dry_run_state_after_wrong:{receipt.get('state_after')}")
    if receipt.get("selected_move_id") != expected["selected_move_id"]:
        failures.append(f"dry_run_selected_move_wrong:{receipt.get('selected_move_id')}")
    if receipt.get("move_status") != expected["move_status"]:
        failures.append(f"dry_run_move_status_wrong:{receipt.get('move_status')}")
    if receipt.get("halt_code") != expected["halt_code"]:
        failures.append(f"dry_run_halt_code_wrong:{receipt.get('halt_code')}")
    if receipt.get("proposal_status") != expected["proposal_status"]:
        failures.append(f"dry_run_proposal_status_wrong:{receipt.get('proposal_status')}")
    if receipt.get("no_proposal_reason") != expected["no_proposal_reason"]:
        failures.append(f"dry_run_no_proposal_reason_wrong:{receipt.get('no_proposal_reason')}")
    if receipt.get("terminal") != expected["terminal"]:
        failures.append(f"dry_run_terminal_wrong:{receipt.get('terminal')}")

    metrics = receipt.get("metrics") or {}
    if metrics.get("move_count") != 1:
        failures.append(f"metric_move_count_wrong:{metrics.get('move_count')}")
    if metrics.get("applied_move_count") != 1:
        failures.append(f"metric_applied_move_count_wrong:{metrics.get('applied_move_count')}")
    if metrics.get("blocked_move_count") != 0:
        failures.append(f"metric_blocked_move_count_wrong:{metrics.get('blocked_move_count')}")
    if metrics.get("halt_count_by_code", {}).get("STOP_DONE") != 1:
        failures.append(f"metric_stop_done_count_wrong:{metrics.get('halt_count_by_code')}")
    if metrics.get("local_closure_radius_observed") != 1:
        failures.append(f"metric_local_closure_radius_wrong:{metrics.get('local_closure_radius_observed')}")
    if metrics.get("proposal_emitted_count") != 0:
        failures.append(f"metric_proposal_emitted_wrong:{metrics.get('proposal_emitted_count')}")
    if metrics.get("proposal_withheld_count") != 1:
        failures.append(f"metric_proposal_withheld_wrong:{metrics.get('proposal_withheld_count')}")

    authority = receipt.get("authority_guards") or {}
    for key in [
        "local_regime_fixed",
        "registered_moves_only",
        "deterministic_selector_used",
        "typed_halts_only",
    ]:
        if authority.get(key) is not True:
            failures.append(f"authority_guard_not_true:{key}:{authority.get(key)}")
    for key in [
        "local_regime_runtime_mutated",
        "proposal_promoted",
        "runtime_registry_mutated",
        "registry_written",
        "registry_inserted",
        "registry_sqlite_read",
        "registry_sqlite_written",
        "full_registry_scan_used",
        "proof_claimed",
        "global_taxonomy_claimed",
        "final_schema_claimed",
        "hidden_continuation_authorized",
    ]:
        if authority.get(key) is not False:
            failures.append(f"authority_guard_not_false:{key}:{authority.get(key)}")

    artifact = receipt.get("artifact_guards") or {}
    for key in [
        "input_artifacts_path_addressed",
        "output_artifacts_receipt_referenced",
        "required_dependencies_verified",
        "tracked_when_permanence_required",
        "unrelated_untracked_data_not_authority",
    ]:
        if artifact.get(key) is not True:
            failures.append(f"artifact_guard_not_true:{key}:{artifact.get(key)}")
    for key in [
        "latest_or_mtime_selection_used",
        "ambient_workspace_authority_used",
    ]:
        if artifact.get(key) is not False:
            failures.append(f"artifact_guard_not_false:{key}:{artifact.get(key)}")

    return failures

def main() -> int:
    policy = read_json(BOOTSTRAP_POLICY_PATH)
    policy_receipt = read_json(BOOTSTRAP_POLICY_RECEIPT_PATH)

    failures = validate_bootstrap(policy, policy_receipt)

    if not run_git_ls_files(BOOTSTRAP_POLICY_PATH):
        failures.append("bootstrap_policy_not_tracked")
    if not run_git_ls_files(BOOTSTRAP_POLICY_RECEIPT_PATH):
        failures.append("bootstrap_policy_receipt_not_tracked")

    if not SRC_MODULE_PATH.exists():
        failures.append("runner_module_missing_after_write")

    runner_mod = import_runner()

    regime = build_local_regime(policy_receipt)
    fixture = build_fixture()
    expected_transcript = {
        "schema_version": "jurisdiction_runner_v0_1_expected_transcript_v0",
        "fixture_id": fixture["fixture_id"],
        "expected_transcript": EXPECTED_TRANSCRIPT,
    }

    runner = runner_mod.JurisdictionRunnerV01(regime)
    dry_receipt = runner.run(
        fixture["input_state"],
        fixture_id=fixture["fixture_id"],
        input_artifact_paths=[
            f"data/local_regime_v0_declarations/{regime['local_regime_hash']}.json",
            f"data/jurisdiction_runner_v0_1_dry_run_fixtures/{fixture['fixture_id']}.json",
            f"data/jurisdiction_runner_v0_1_expected_transcripts/{fixture['fixture_id']}.json",
        ],
    )

    failures.extend(validate_dry_run(fixture, dry_receipt))

    implementation_seed = {
        "unit_id": UNIT_ID,
        "bootstrap_policy_id": BOOTSTRAP_POLICY_ID,
        "bootstrap_policy_receipt_id": BOOTSTRAP_POLICY_RECEIPT_ID,
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": regime["local_regime_hash"],
        "fixture_id": fixture["fixture_id"],
        "dry_run_receipt_id": dry_receipt["receipt_id"],
    }
    implementation_receipt_id = sha8(implementation_seed)

    authority_guards = {
        "bootstrap_policy_consumed": True,
        "runner_implemented": True,
        "runner_executed": True,
        "dry_run_fixture_created": True,
        "dry_run_fixture_executed": True,
        "expected_transcript_created": True,
        "local_regime_v0_declared": True,
        "local_regime_runtime_mutated": False,
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

    implementation_receipt = {
        "schema_version": "jurisdiction_runner_v0_1_implementation_receipt_v0",
        "receipt_type": "JURISDICTION_RUNNER_V0_1_IMPLEMENTATION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": implementation_receipt_id,
        "bootstrap_policy_id": BOOTSTRAP_POLICY_ID,
        "bootstrap_policy_receipt_id": BOOTSTRAP_POLICY_RECEIPT_ID,
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": regime["local_regime_hash"],
        "runner_module_path": "src/matrixlab/jurisdiction_runner_v0_1.py",
        "local_regime_path": f"data/local_regime_v0_declarations/{regime['local_regime_hash']}.json",
        "dry_run_fixture_id": fixture["fixture_id"],
        "dry_run_fixture_path": f"data/jurisdiction_runner_v0_1_dry_run_fixtures/{fixture['fixture_id']}.json",
        "expected_transcript_path": f"data/jurisdiction_runner_v0_1_expected_transcripts/{fixture['fixture_id']}.json",
        "dry_run_receipt_id": dry_receipt["receipt_id"],
        "dry_run_receipt_path": f"data/jurisdiction_runner_v0_1_dry_run_receipts/{dry_receipt['receipt_id']}.json",
        "dry_run_gate": dry_receipt["gate"],
        "dry_run_transcript": dry_receipt["transcript"],
        "expected_transcript": EXPECTED_TRANSCRIPT,
        "dry_run_transcript_matches_expected": dry_receipt["transcript_matches_expected"],
        "dry_run_terminal": dry_receipt["terminal"],
        "dry_run_metrics": dry_receipt["metrics"],
        "authority_guards": authority_guards,
        "artifact_guards": {
            "bootstrap_policy_tracked": run_git_ls_files(BOOTSTRAP_POLICY_PATH),
            "bootstrap_policy_receipt_tracked": run_git_ls_files(BOOTSTRAP_POLICY_RECEIPT_PATH),
            "outputs_path_addressed": True,
            "outputs_receipt_referenced": True,
            "unrelated_untracked_data_not_authority": True,
            "latest_or_mtime_selection_used": False,
            "ambient_workspace_authority_used": False,
        },
        "terminal": {
            "type": "STOP",
            "next_command_goal": None,
            "stop_code": "STOP_DONE",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    for d in [
        LOCAL_REGIME_DIR,
        FIXTURE_DIR,
        TRANSCRIPT_DIR,
        DRY_RUN_RECEIPT_DIR,
        IMPLEMENTATION_RECEIPT_DIR,
    ]:
        d.mkdir(parents=True, exist_ok=True)

    regime_path = LOCAL_REGIME_DIR / f"{regime['local_regime_hash']}.json"
    fixture_path = FIXTURE_DIR / f"{fixture['fixture_id']}.json"
    transcript_path = TRANSCRIPT_DIR / f"{fixture['fixture_id']}.json"
    dry_receipt_path = DRY_RUN_RECEIPT_DIR / f"{dry_receipt['receipt_id']}.json"
    implementation_receipt_path = IMPLEMENTATION_RECEIPT_DIR / f"{implementation_receipt_id}.json"

    regime_path.write_text(json.dumps(regime, indent=2, sort_keys=True) + "\n")
    fixture_path.write_text(json.dumps(fixture, indent=2, sort_keys=True) + "\n")
    transcript_path.write_text(json.dumps(expected_transcript, indent=2, sort_keys=True) + "\n")
    dry_receipt_path.write_text(json.dumps(dry_receipt, indent=2, sort_keys=True) + "\n")
    implementation_receipt_path.write_text(json.dumps(implementation_receipt, indent=2, sort_keys=True) + "\n")

    print(json.dumps(implementation_receipt, indent=2, sort_keys=True))
    print(f"implementation_receipt_id={implementation_receipt_id}")
    print(f"implementation_receipt_path=data/jurisdiction_runner_v0_1_implementation_receipts/{implementation_receipt_id}.json")
    print(f"local_regime_path=data/local_regime_v0_declarations/{regime['local_regime_hash']}.json")
    print(f"dry_run_fixture_id={fixture['fixture_id']}")
    print(f"dry_run_fixture_path=data/jurisdiction_runner_v0_1_dry_run_fixtures/{fixture['fixture_id']}.json")
    print(f"expected_transcript_path=data/jurisdiction_runner_v0_1_expected_transcripts/{fixture['fixture_id']}.json")
    print(f"dry_run_receipt_id={dry_receipt['receipt_id']}")
    print(f"dry_run_receipt_path=data/jurisdiction_runner_v0_1_dry_run_receipts/{dry_receipt['receipt_id']}.json")
    return 0 if implementation_receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
