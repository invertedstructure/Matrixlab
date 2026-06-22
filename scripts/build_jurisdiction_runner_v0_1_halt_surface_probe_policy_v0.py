#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_JURISDICTION_RUNNER_V0_1_HALT_SURFACE_PROBE_POLICY_V0"
NEXT_GOAL = "RUN_JURISDICTION_RUNNER_V0_1_HALT_SURFACE_PROBE_V0"

BOOTSTRAP_POLICY_ID = "0fe04fb5"
BOOTSTRAP_POLICY_RECEIPT_ID = "bc448c6d"
IMPLEMENTATION_RECEIPT_ID = "04c0692d"
LOCAL_REGIME_HASH = "097d620c"
DRY_RUN_FIXTURE_ID = "dry_run_apply_registered_transition_v0"
DRY_RUN_RECEIPT_ID = "a85e0cc4"

RUNNER_UNIT_ID = "jurisdiction_runner.v0.1"
LOCAL_REGIME_VERSION = "local_regime.v0"

BOOTSTRAP_POLICY_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_bootstrap_policies" / f"{BOOTSTRAP_POLICY_ID}.json"
BOOTSTRAP_POLICY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_bootstrap_policy_receipts" / f"{BOOTSTRAP_POLICY_ID}.json"
IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_implementation_receipts" / f"{IMPLEMENTATION_RECEIPT_ID}.json"
LOCAL_REGIME_PATH = ROOT / "data" / "local_regime_v0_declarations" / f"{LOCAL_REGIME_HASH}.json"
DRY_RUN_FIXTURE_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_dry_run_fixtures" / f"{DRY_RUN_FIXTURE_ID}.json"
EXPECTED_TRANSCRIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_expected_transcripts" / f"{DRY_RUN_FIXTURE_ID}.json"
DRY_RUN_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_dry_run_receipts" / f"{DRY_RUN_RECEIPT_ID}.json"
RUNNER_MODULE_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_1.py"

OUT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_policy_receipts"

REQUIRED_HALT_CODES = [
    "STOP_DONE",
    "STOP_NO_APPLICABLE_MOVE",
    "STOP_AUTHORITY_VIOLATION",
    "STOP_GATE_FAIL",
    "STOP_UNTYPED_OBJECT",
    "STOP_DEPENDENCY_MISSING",
]

UNCOVERED_HALT_CODES = [
    "STOP_NO_APPLICABLE_MOVE",
    "STOP_AUTHORITY_VIOLATION",
    "STOP_GATE_FAIL",
    "STOP_UNTYPED_OBJECT",
    "STOP_DEPENDENCY_MISSING",
]

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

def blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, default=str, separators=(",", ":")).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(blob(obj)).hexdigest()[:8]

def read_json(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise SystemExit(f"missing required json: {path}")
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

def validate_inputs(
    bootstrap_policy: Dict[str, Any],
    bootstrap_receipt: Dict[str, Any],
    implementation_receipt: Dict[str, Any],
    local_regime: Dict[str, Any],
    dry_fixture: Dict[str, Any],
    expected_transcript: Dict[str, Any],
    dry_receipt: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if bootstrap_policy.get("policy_id") != BOOTSTRAP_POLICY_ID:
        failures.append(f"bootstrap_policy_id_wrong:{bootstrap_policy.get('policy_id')}")
    if bootstrap_policy.get("policy_receipt_id") != BOOTSTRAP_POLICY_RECEIPT_ID:
        failures.append(f"bootstrap_policy_receipt_id_wrong:{bootstrap_policy.get('policy_receipt_id')}")
    if bootstrap_receipt.get("policy_id") != BOOTSTRAP_POLICY_ID:
        failures.append(f"bootstrap_receipt_policy_id_wrong:{bootstrap_receipt.get('policy_id')}")
    if bootstrap_receipt.get("receipt_id") != BOOTSTRAP_POLICY_RECEIPT_ID:
        failures.append(f"bootstrap_receipt_id_wrong:{bootstrap_receipt.get('receipt_id')}")
    if bootstrap_receipt.get("gate") != "PASS":
        failures.append(f"bootstrap_gate_not_PASS:{bootstrap_receipt.get('gate')}")

    if implementation_receipt.get("receipt_id") != IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"implementation_receipt_id_wrong:{implementation_receipt.get('receipt_id')}")
    if implementation_receipt.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{implementation_receipt.get('gate')}")
    if implementation_receipt.get("runner_unit_id") != RUNNER_UNIT_ID:
        failures.append(f"implementation_runner_wrong:{implementation_receipt.get('runner_unit_id')}")
    if implementation_receipt.get("local_regime_version") != LOCAL_REGIME_VERSION:
        failures.append(f"implementation_regime_version_wrong:{implementation_receipt.get('local_regime_version')}")
    if implementation_receipt.get("local_regime_hash") != LOCAL_REGIME_HASH:
        failures.append(f"implementation_regime_hash_wrong:{implementation_receipt.get('local_regime_hash')}")
    if implementation_receipt.get("dry_run_gate") != "PASS":
        failures.append(f"implementation_dry_run_gate_wrong:{implementation_receipt.get('dry_run_gate')}")
    if implementation_receipt.get("dry_run_transcript_matches_expected") is not True:
        failures.append(f"implementation_transcript_match_wrong:{implementation_receipt.get('dry_run_transcript_matches_expected')}")

    terminal = implementation_receipt.get("terminal") or {}
    if terminal.get("type") != "STOP":
        failures.append(f"implementation_terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_DONE":
        failures.append(f"implementation_terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"implementation_terminal_next_not_null:{terminal.get('next_command_goal')}")

    guards = implementation_receipt.get("authority_guards") or {}
    for key in [
        "bootstrap_policy_consumed",
        "runner_implemented",
        "runner_executed",
        "dry_run_fixture_created",
        "dry_run_fixture_executed",
        "expected_transcript_created",
        "local_regime_v0_declared",
    ]:
        if guards.get(key) is not True:
            failures.append(f"implementation_guard_not_true:{key}:{guards.get(key)}")
    for key in [
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
    ]:
        if guards.get(key) is not False:
            failures.append(f"implementation_guard_not_false:{key}:{guards.get(key)}")

    if local_regime.get("local_regime_version") != LOCAL_REGIME_VERSION:
        failures.append(f"local_regime_version_wrong:{local_regime.get('local_regime_version')}")
    if local_regime.get("local_regime_hash") != LOCAL_REGIME_HASH:
        failures.append(f"local_regime_hash_wrong:{local_regime.get('local_regime_hash')}")

    halt_vocab = local_regime.get("halt_vocabulary") or []
    for code in REQUIRED_HALT_CODES:
        if code not in halt_vocab:
            failures.append(f"local_regime_missing_halt:{code}")

    if dry_fixture.get("fixture_id") != DRY_RUN_FIXTURE_ID:
        failures.append(f"dry_fixture_id_wrong:{dry_fixture.get('fixture_id')}")
    if expected_transcript.get("expected_transcript") != EXPECTED_TRANSCRIPT:
        failures.append("expected_transcript_wrong")
    if dry_receipt.get("receipt_id") != DRY_RUN_RECEIPT_ID:
        failures.append(f"dry_receipt_id_wrong:{dry_receipt.get('receipt_id')}")
    if dry_receipt.get("halt_code") != "STOP_DONE":
        failures.append(f"dry_receipt_halt_not_STOP_DONE:{dry_receipt.get('halt_code')}")
    if dry_receipt.get("gate") != "PASS":
        failures.append(f"dry_receipt_gate_not_PASS:{dry_receipt.get('gate')}")

    for path, label in [
        (BOOTSTRAP_POLICY_PATH, "bootstrap_policy"),
        (BOOTSTRAP_POLICY_RECEIPT_PATH, "bootstrap_policy_receipt"),
        (IMPLEMENTATION_RECEIPT_PATH, "implementation_receipt"),
        (LOCAL_REGIME_PATH, "local_regime"),
        (DRY_RUN_FIXTURE_PATH, "dry_run_fixture"),
        (EXPECTED_TRANSCRIPT_PATH, "expected_transcript"),
        (DRY_RUN_RECEIPT_PATH, "dry_run_receipt"),
        (RUNNER_MODULE_PATH, "runner_module"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{path.relative_to(ROOT).as_posix()}")

    return failures

def build_policy(write_outputs: bool = True) -> tuple[Dict[str, Any], Dict[str, Any]]:
    bootstrap_policy = read_json(BOOTSTRAP_POLICY_PATH)
    bootstrap_receipt = read_json(BOOTSTRAP_POLICY_RECEIPT_PATH)
    implementation_receipt = read_json(IMPLEMENTATION_RECEIPT_PATH)
    local_regime = read_json(LOCAL_REGIME_PATH)
    dry_fixture = read_json(DRY_RUN_FIXTURE_PATH)
    expected_transcript = read_json(EXPECTED_TRANSCRIPT_PATH)
    dry_receipt = read_json(DRY_RUN_RECEIPT_PATH)

    failures = validate_inputs(
        bootstrap_policy,
        bootstrap_receipt,
        implementation_receipt,
        local_regime,
        dry_fixture,
        expected_transcript,
        dry_receipt,
    )

    policy_seed = {
        "unit_id": UNIT_ID,
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": LOCAL_REGIME_HASH,
        "implementation_receipt_id": IMPLEMENTATION_RECEIPT_ID,
        "uncovered_halt_codes": UNCOVERED_HALT_CODES,
        "next_goal": NEXT_GOAL,
    }
    policy_id = sha8(policy_seed)

    halt_probe_plan = {
        "already_covered": {
            "STOP_DONE": {
                "source_dry_run_receipt_id": DRY_RUN_RECEIPT_ID,
                "status": "COVERED",
            }
        },
        "required_probe_cases": {
            "STOP_UNTYPED_OBJECT": {
                "fixture_kind": "state_validation",
                "input_state": {
                    "state_id": "untyped_counter_zero",
                    "typed": False,
                    "value": 0,
                },
                "expected": {
                    "halt_code": "STOP_UNTYPED_OBJECT",
                    "move_status": "BLOCKED",
                    "proposal_status": "NONE",
                    "no_proposal_reason": "PRESSURE_ALREADY_TYPED",
                    "runner_executes": True,
                },
            },
            "STOP_GATE_FAIL": {
                "fixture_kind": "state_validation",
                "input_state": {
                    "state_id": "typed_counter_negative",
                    "typed": True,
                    "value": -1,
                },
                "expected": {
                    "halt_code": "STOP_GATE_FAIL",
                    "move_status": "BLOCKED",
                    "proposal_status": "NONE",
                    "no_proposal_reason": "PRESSURE_ALREADY_TYPED",
                    "runner_executes": True,
                },
            },
            "STOP_NO_APPLICABLE_MOVE": {
                "fixture_kind": "selector_boundary",
                "input_state": {
                    "state_id": "typed_counter_already_closed",
                    "typed": True,
                    "value": 1,
                },
                "expected": {
                    "halt_code": "STOP_NO_APPLICABLE_MOVE",
                    "move_status": "BLOCKED",
                    "proposal_status": "NONE",
                    "no_proposal_reason": "INSUFFICIENT_EVIDENCE",
                    "runner_executes": True,
                },
            },
            "STOP_AUTHORITY_VIOLATION": {
                "fixture_kind": "controlled_probe_regime_variant",
                "regime_variant_rule": "copy local_regime.v0, keep move registry unchanged, set jurisdiction_envelope.allowed_move_ids to empty list for this probe only",
                "variant_is_not_promotion": True,
                "variant_must_not_replace_local_regime_v0": True,
                "input_state": {
                    "state_id": "typed_counter_zero_authority_blocked",
                    "typed": True,
                    "value": 0,
                },
                "expected": {
                    "halt_code": "STOP_AUTHORITY_VIOLATION",
                    "move_status": "BLOCKED",
                    "proposal_status": "NONE",
                    "no_proposal_reason": "OUT_OF_SCOPE",
                    "runner_executes": True,
                },
            },
            "STOP_DEPENDENCY_MISSING": {
                "fixture_kind": "wrapper_dependency_boundary",
                "missing_dependency_path": "data/jurisdiction_runner_v0_1_missing_dependency_probe/MISSING.json",
                "expected": {
                    "halt_code": "STOP_DEPENDENCY_MISSING",
                    "move_status": "BLOCKED",
                    "proposal_status": "NONE",
                    "no_proposal_reason": "PRESSURE_ALREADY_TYPED",
                    "runner_executes": False,
                },
            },
        },
        "expected_transcript": EXPECTED_TRANSCRIPT,
        "coverage_goal": REQUIRED_HALT_CODES,
    }

    authority_guards = {
        "halt_surface_probe_policy_built": True,
        "implementation_receipt_consumed": True,
        "runner_module_read": True,
        "runner_module_changed": False,
        "runner_executed_by_policy": False,
        "probe_fixtures_created_by_policy": False,
        "probe_fixtures_executed_by_policy": False,
        "controlled_probe_regime_variant_authorized_for_next_unit": True,
        "controlled_probe_regime_variant_promoted": False,
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

    policy = {
        "schema_version": "jurisdiction_runner_v0_1_halt_surface_probe_policy_v0",
        "policy_type": "JURISDICTION_RUNNER_V0_1_HALT_SURFACE_PROBE_POLICY",
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": LOCAL_REGIME_HASH,
        "source_bootstrap_policy_id": BOOTSTRAP_POLICY_ID,
        "source_bootstrap_policy_receipt_id": BOOTSTRAP_POLICY_RECEIPT_ID,
        "source_implementation_receipt_id": IMPLEMENTATION_RECEIPT_ID,
        "source_dry_run_receipt_id": DRY_RUN_RECEIPT_ID,
        "review_summary": {
            "implementation_valid": True,
            "happy_path_covered": True,
            "covered_halt_codes": ["STOP_DONE"],
            "uncovered_halt_codes": UNCOVERED_HALT_CODES,
            "reason_for_next_probe": "v0.1 declares six halt codes but implementation receipt covered only STOP_DONE",
        },
        "halt_surface_probe_plan": halt_probe_plan,
        "authorized_operations_next": {
            "read_halt_surface_probe_policy": True,
            "read_halt_surface_probe_policy_receipt": True,
            "read_runner_module": True,
            "read_local_regime_v0_declaration": True,
            "create_halt_surface_probe_fixtures": True,
            "create_expected_probe_transcripts": True,
            "execute_runner_against_probe_fixtures": True,
            "execute_wrapper_dependency_missing_probe": True,
            "emit_halt_surface_probe_receipt": True,
        },
        "forbidden_operations": {
            "modify_runner_module": True,
            "promote_probe_regime_variant": True,
            "replace_local_regime_v0": True,
            "mutate_local_regime_at_runtime": True,
            "promote_proposals": True,
            "registry_sqlite_write": True,
            "registry_sqlite_read": True,
            "full_registry_scan": True,
            "global_taxonomy_design": True,
            "final_schema_claim": True,
            "proof_claim": True,
            "hidden_continuation_after_stop": True,
            "ambient_workspace_authority": True,
            "latest_or_mtime_selection": True,
        },
        "safety_clauses": {
            "policy_only": True,
            "does_not_modify_runner": True,
            "does_not_execute_runner": True,
            "does_not_create_probe_fixtures": True,
            "does_not_promote_probe_regime_variant": True,
            "does_not_mutate_local_regime": True,
            "does_not_promote_any_proposal": True,
            "does_not_write_registry": True,
            "does_not_claim_global_correctness": True,
            "does_not_claim_theorem_closure": True,
            "next_unit_required_for_probe_execution": True,
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

    receipt = {
        "schema_version": "jurisdiction_runner_v0_1_halt_surface_probe_policy_receipt_v0",
        "receipt_type": "JURISDICTION_RUNNER_V0_1_HALT_SURFACE_PROBE_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": LOCAL_REGIME_HASH,
        "source_bootstrap_policy_id": BOOTSTRAP_POLICY_ID,
        "source_bootstrap_policy_receipt_id": BOOTSTRAP_POLICY_RECEIPT_ID,
        "source_implementation_receipt_id": IMPLEMENTATION_RECEIPT_ID,
        "source_dry_run_receipt_id": DRY_RUN_RECEIPT_ID,
        "review_summary": policy["review_summary"],
        "halt_surface_probe_plan": halt_probe_plan,
        "authorized_operations_next": policy["authorized_operations_next"],
        "forbidden_operations": policy["forbidden_operations"],
        "safety_clauses": policy["safety_clauses"],
        "authority_guards": authority_guards,
        "terminal": policy["terminal"],
        "gate": policy["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    receipt_id = sha8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt["receipt_sig8"] = receipt_id
    policy["policy_receipt_id"] = receipt_id

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        (OUT_DIR / f"{policy_id}.json").write_text(json.dumps(policy, indent=2, sort_keys=True) + "\n")
        (OUT_RECEIPT_DIR / f"{policy_id}.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")

    return policy, receipt

def main() -> int:
    policy, receipt = build_policy(write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"halt_surface_probe_policy_id={policy['policy_id']}")
    print(f"halt_surface_probe_policy_receipt_id={receipt['receipt_id']}")
    print(f"halt_surface_probe_policy_path=data/jurisdiction_runner_v0_1_halt_surface_probe_policies/{policy['policy_id']}.json")
    print(f"halt_surface_probe_policy_receipt_path=data/jurisdiction_runner_v0_1_halt_surface_probe_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
