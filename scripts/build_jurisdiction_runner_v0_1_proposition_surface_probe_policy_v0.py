#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_JURISDICTION_RUNNER_V0_1_PROPOSITION_SURFACE_PROBE_POLICY_V0"
NEXT_GOAL = "RUN_JURISDICTION_RUNNER_V0_1_PROPOSITION_SURFACE_PROBE_V0"

RUNNER_UNIT_ID = "jurisdiction_runner.v0.1"
LOCAL_REGIME_VERSION = "local_regime.v0"
LOCAL_REGIME_HASH = "097d620c"

HALT_SURFACE_PROBE_RUN_RECEIPT_ID = "5030948f"
HALT_SURFACE_PROBE_POLICY_ID = "cfe745b9"
HALT_SURFACE_PROBE_POLICY_RECEIPT_ID = "7bb73d50"
IMPLEMENTATION_RECEIPT_ID = "04c0692d"

RUN_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_run_receipts" / f"{HALT_SURFACE_PROBE_RUN_RECEIPT_ID}.json"
HALT_POLICY_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_policies" / f"{HALT_SURFACE_PROBE_POLICY_ID}.json"
HALT_POLICY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_policy_receipts" / f"{HALT_SURFACE_PROBE_POLICY_ID}.json"
IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_implementation_receipts" / f"{IMPLEMENTATION_RECEIPT_ID}.json"
LOCAL_REGIME_PATH = ROOT / "data" / "local_regime_v0_declarations" / f"{LOCAL_REGIME_HASH}.json"
RUNNER_MODULE_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_1.py"

OUT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_policy_receipts"

PROPOSITION_SURFACE_CASES = {
    "HALT_NO_APPLICABLE_MOVE_WITH_NO_PROPOSAL_BASELINE": {
        "purpose": "Preserve the observed v0.1 baseline where STOP_NO_APPLICABLE_MOVE emits no proposal and no hidden continuation.",
        "source_case": "STOP_NO_APPLICABLE_MOVE",
        "expected": {
            "halt_code": "STOP_NO_APPLICABLE_MOVE",
            "proposal_status": "NONE",
            "no_proposal_reason": "INSUFFICIENT_EVIDENCE",
            "proposal_executed": False,
            "hidden_continuation_authorized": False,
        },
    },
    "PROPOSAL_PRESSURE_DISCOVERY": {
        "purpose": "Determine whether v0.1 has any lawful runtime path that emits halt-with-proposal under local regime pressure.",
        "probe_kind": "capability_discovery",
        "expected_policy_result_class": [
            "PROPOSAL_SURFACE_PRESENT",
            "PROPOSAL_SURFACE_ABSENT_REQUIRES_DELTA_PROPOSAL",
        ],
        "must_not_require_successful_proposal_emission": True,
        "must_record_absence_as_observation_not_failure": True,
    },
    "PROPOSAL_NON_EXECUTION_DISCIPLINE": {
        "purpose": "If any proposal is emitted, prove it is not executed, not promoted, and not allowed to mutate regime, registry, or runtime.",
        "conditional_on": "proposal_status != NONE",
        "required_guards_if_applicable": {
            "proposal_executed": False,
            "proposal_promoted": False,
            "local_regime_runtime_mutated": False,
            "registry_written": False,
            "runner_module_changed": False,
            "hidden_continuation_authorized": False,
        },
    },
    "DUPLICATE_UNRESOLVED_PROPOSAL_GUARD": {
        "purpose": "If the same unresolved proposal pressure is observed twice, require duplicate proposal spam to be blocked or explicitly counted.",
        "probe_kind": "repeat_pressure",
        "allowed_results": {
            "duplicate_unresolved_proposal_count_increases": True,
            "second_proposal_withheld": True,
            "no_surface_present": True,
        },
        "must_not_promote_any_proposal": True,
    },
    "TAXONOMY_DELTA_PROPOSAL_IF_SURFACE_ABSENT": {
        "purpose": "If v0.1 cannot emit lawful proposals, the probe may emit a reviewable taxonomy/regime delta proposal artifact, not apply it.",
        "allowed_proposal_class": "PROPOSITION_SURFACE_DELTA_PROPOSAL",
        "proposal_is_artifact_only": True,
        "proposal_must_require_human_review": True,
        "proposal_must_not_mutate_local_regime": True,
    },
}

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def blob(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

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
    run_receipt: Dict[str, Any],
    halt_policy: Dict[str, Any],
    halt_policy_receipt: Dict[str, Any],
    implementation: Dict[str, Any],
    local_regime: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if run_receipt.get("receipt_id") != HALT_SURFACE_PROBE_RUN_RECEIPT_ID:
        failures.append(f"halt_surface_run_receipt_id_wrong:{run_receipt.get('receipt_id')}")
    if run_receipt.get("gate") != "PASS":
        failures.append(f"halt_surface_run_gate_not_PASS:{run_receipt.get('gate')}")
    if run_receipt.get("coverage_complete") is not True:
        failures.append(f"halt_surface_coverage_not_complete:{run_receipt.get('coverage_complete')}")
    if run_receipt.get("missing_coverage") != []:
        failures.append(f"halt_surface_missing_coverage:{run_receipt.get('missing_coverage')}")
    if run_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append(f"halt_surface_terminal_not_STOP:{run_receipt.get('terminal')}")
    if run_receipt.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append(f"halt_surface_terminal_stop_not_DONE:{run_receipt.get('terminal')}")
    if run_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append(f"halt_surface_terminal_next_not_null:{run_receipt.get('terminal')}")

    expected_halts = [
        "STOP_AUTHORITY_VIOLATION",
        "STOP_DEPENDENCY_MISSING",
        "STOP_DONE",
        "STOP_GATE_FAIL",
        "STOP_NO_APPLICABLE_MOVE",
        "STOP_UNTYPED_OBJECT",
    ]
    if run_receipt.get("covered_halts_after_probe") != expected_halts:
        failures.append(f"covered_halts_wrong:{run_receipt.get('covered_halts_after_probe')}")

    metrics = run_receipt.get("aggregate_metrics") or {}
    expected_metrics = {
        "coverage_goal_count": 6,
        "covered_halt_count": 6,
        "new_probe_case_count": 5,
        "runner_executed_probe_count": 4,
        "wrapper_boundary_probe_count": 1,
        "case_pass_count": 5,
        "case_fail_count": 0,
        "proposal_promoted_count": 0,
        "registry_write_count": 0,
        "controlled_probe_regime_variant_count": 1,
        "controlled_probe_regime_variant_promoted_count": 0,
    }
    for key, expected in expected_metrics.items():
        if metrics.get(key) != expected:
            failures.append(f"halt_surface_metric_wrong:{key}:{metrics.get(key)}")

    guards = run_receipt.get("authority_guards") or {}
    for key in [
        "runner_module_changed",
        "local_regime_replaced",
        "local_regime_runtime_mutated",
        "controlled_probe_regime_variant_promoted",
        "proposal_promoted",
        "registry_written",
        "registry_sqlite_written",
        "proof_claimed",
        "global_taxonomy_claimed",
        "hidden_continuation_authorized",
    ]:
        if guards.get(key) is not False:
            failures.append(f"halt_surface_guard_not_false:{key}:{guards.get(key)}")

    if halt_policy.get("policy_id") != HALT_SURFACE_PROBE_POLICY_ID:
        failures.append(f"halt_policy_id_wrong:{halt_policy.get('policy_id')}")
    if halt_policy_receipt.get("receipt_id") != HALT_SURFACE_PROBE_POLICY_RECEIPT_ID:
        failures.append(f"halt_policy_receipt_id_wrong:{halt_policy_receipt.get('receipt_id')}")
    if halt_policy_receipt.get("gate") != "PASS":
        failures.append(f"halt_policy_receipt_gate_not_PASS:{halt_policy_receipt.get('gate')}")

    if implementation.get("receipt_id") != IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"implementation_receipt_id_wrong:{implementation.get('receipt_id')}")
    if implementation.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{implementation.get('gate')}")

    if local_regime.get("local_regime_hash") != LOCAL_REGIME_HASH:
        failures.append(f"local_regime_hash_wrong:{local_regime.get('local_regime_hash')}")
    if local_regime.get("local_regime_version") != LOCAL_REGIME_VERSION:
        failures.append(f"local_regime_version_wrong:{local_regime.get('local_regime_version')}")

    for path, label in [
        (RUN_RECEIPT_PATH, "halt_surface_run_receipt"),
        (HALT_POLICY_PATH, "halt_surface_policy"),
        (HALT_POLICY_RECEIPT_PATH, "halt_surface_policy_receipt"),
        (IMPLEMENTATION_RECEIPT_PATH, "implementation_receipt"),
        (LOCAL_REGIME_PATH, "local_regime"),
        (RUNNER_MODULE_PATH, "runner_module"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{path.relative_to(ROOT).as_posix()}")

    return failures

def build_policy(write_outputs: bool = True) -> tuple[Dict[str, Any], Dict[str, Any]]:
    run_receipt = read_json(RUN_RECEIPT_PATH)
    halt_policy = read_json(HALT_POLICY_PATH)
    halt_policy_receipt = read_json(HALT_POLICY_RECEIPT_PATH)
    implementation = read_json(IMPLEMENTATION_RECEIPT_PATH)
    local_regime = read_json(LOCAL_REGIME_PATH)

    failures = validate_inputs(run_receipt, halt_policy, halt_policy_receipt, implementation, local_regime)

    policy_seed = {
        "unit_id": UNIT_ID,
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_hash": LOCAL_REGIME_HASH,
        "source_halt_surface_probe_run_receipt_id": HALT_SURFACE_PROBE_RUN_RECEIPT_ID,
        "next_goal": NEXT_GOAL,
        "case_names": sorted(PROPOSITION_SURFACE_CASES),
    }
    policy_id = sha8(policy_seed)

    authority_guards = {
        "proposition_surface_probe_policy_built": True,
        "halt_surface_probe_run_receipt_consumed": True,
        "halt_surface_coverage_complete_required": True,
        "runner_module_read": True,
        "runner_module_changed": False,
        "runner_executed_by_policy": False,
        "probe_fixtures_created_by_policy": False,
        "probe_fixtures_executed_by_policy": False,
        "proposal_surface_probe_executed_by_policy": False,
        "proposal_artifact_emitted_by_policy": False,
        "proposal_promoted": False,
        "local_regime_replaced": False,
        "local_regime_runtime_mutated": False,
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
        "schema_version": "jurisdiction_runner_v0_1_proposition_surface_probe_policy_v0",
        "policy_type": "JURISDICTION_RUNNER_V0_1_PROPOSITION_SURFACE_PROBE_POLICY",
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": LOCAL_REGIME_HASH,
        "source_halt_surface_probe_run_receipt_id": HALT_SURFACE_PROBE_RUN_RECEIPT_ID,
        "source_halt_surface_probe_policy_id": HALT_SURFACE_PROBE_POLICY_ID,
        "source_halt_surface_probe_policy_receipt_id": HALT_SURFACE_PROBE_POLICY_RECEIPT_ID,
        "source_implementation_receipt_id": IMPLEMENTATION_RECEIPT_ID,
        "review_summary": {
            "happy_path_covered": True,
            "halt_surface_covered": True,
            "halt_surface_coverage_complete": run_receipt.get("coverage_complete") is True,
            "covered_halt_count": (run_receipt.get("aggregate_metrics") or {}).get("covered_halt_count"),
            "proposition_surface_not_yet_exercised": True,
            "observed_proposal_status_so_far": "NONE_ONLY",
            "reason_for_next_probe": "v0.1 has happy-path and halt-code coverage, but proposal emission, proposal non-execution, duplicate unresolved proposal guard, and proposal-absence delta behavior are not yet probed.",
        },
        "proposition_surface_probe_plan": {
            "probe_mode": "DISCOVERY_NOT_ACCEPTANCE",
            "cases": PROPOSITION_SURFACE_CASES,
            "success_criteria": {
                "probe_completes_without_runtime_mutation": True,
                "no_proposal_is_executed": True,
                "no_proposal_is_promoted": True,
                "absence_of_proposal_surface_is_recorded_not_treated_as_runtime_failure": True,
                "if_surface_absent_emit_reviewable_delta_proposal_artifact_only": True,
                "duplicate_unresolved_pressure_is_blocked_or_counted": True,
            },
            "non_success_conditions": {
                "runner_executes_proposal": True,
                "proposal_promoted_without_review": True,
                "local_regime_mutated_at_runtime": True,
                "registry_written": True,
                "hidden_continuation_after_stop": True,
                "global_or_final_taxonomy_claimed": True,
            },
        },
        "authorized_operations_next": {
            "read_proposition_surface_probe_policy": True,
            "read_proposition_surface_probe_policy_receipt": True,
            "read_runner_module": True,
            "read_local_regime_v0_declaration": True,
            "read_halt_surface_probe_run_receipt": True,
            "create_proposition_surface_probe_fixtures": True,
            "execute_runner_against_probe_fixtures": True,
            "repeat_unresolved_pressure_probe": True,
            "emit_proposition_surface_probe_receipt": True,
            "emit_reviewable_delta_proposal_if_surface_absent": True,
        },
        "forbidden_operations": {
            "modify_runner_module": True,
            "execute_or_apply_proposal": True,
            "promote_proposal": True,
            "promote_probe_regime_variant": True,
            "replace_local_regime_v0": True,
            "mutate_local_regime_at_runtime": True,
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
            "does_not_execute_or_apply_any_proposal": True,
            "does_not_promote_any_proposal": True,
            "does_not_mutate_local_regime": True,
            "does_not_write_registry": True,
            "does_not_claim_proposition_surface_exists": True,
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
        "schema_version": "jurisdiction_runner_v0_1_proposition_surface_probe_policy_receipt_v0",
        "receipt_type": "JURISDICTION_RUNNER_V0_1_PROPOSITION_SURFACE_PROBE_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": LOCAL_REGIME_HASH,
        "source_halt_surface_probe_run_receipt_id": HALT_SURFACE_PROBE_RUN_RECEIPT_ID,
        "source_halt_surface_probe_policy_id": HALT_SURFACE_PROBE_POLICY_ID,
        "source_halt_surface_probe_policy_receipt_id": HALT_SURFACE_PROBE_POLICY_RECEIPT_ID,
        "source_implementation_receipt_id": IMPLEMENTATION_RECEIPT_ID,
        "review_summary": policy["review_summary"],
        "proposition_surface_probe_plan": policy["proposition_surface_probe_plan"],
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
        write_path = OUT_DIR / f"{policy_id}.json"
        receipt_path = OUT_RECEIPT_DIR / f"{policy_id}.json"
        write_path.write_text(json.dumps(policy, indent=2, sort_keys=True) + "\n")
        receipt_path.write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")

    return policy, receipt

def main() -> int:
    policy, receipt = build_policy(write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"proposition_surface_probe_policy_id={policy['policy_id']}")
    print(f"proposition_surface_probe_policy_receipt_id={receipt['receipt_id']}")
    print(f"proposition_surface_probe_policy_path=data/jurisdiction_runner_v0_1_proposition_surface_probe_policies/{policy['policy_id']}.json")
    print(f"proposition_surface_probe_policy_receipt_path=data/jurisdiction_runner_v0_1_proposition_surface_probe_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
