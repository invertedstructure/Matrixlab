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

UNIT_ID = "RECORD_HUMAN_DECISION_PROVISIONAL_ACCEPT_PROPOSITION_SURFACE_DELTA_V0"
NEXT_GOAL = "BUILD_JURISDICTION_RUNNER_V0_2_PROPOSITION_SURFACE_UPGRADE_POLICY_V0"

RUNNER_UNIT_ID = "jurisdiction_runner.v0.1"
TARGET_RUNNER_UNIT_ID = "jurisdiction_runner.v0.2"
LOCAL_REGIME_VERSION = "local_regime.v0"
TARGET_LOCAL_REGIME_VERSION = "local_regime.v1"
LOCAL_REGIME_HASH = "097d620c"

PROBE_RUN_RECEIPT_ID = "0d2f03d4"
DELTA_PROPOSAL_ID = "6e4ee1ea"
DELTA_PROPOSAL_RECEIPT_ID = "e919d594"
PROBE_POLICY_ID = "c7cb4d9e"
PROBE_POLICY_RECEIPT_ID = "c6dbd7d2"
HALT_SURFACE_PROBE_RUN_RECEIPT_ID = "5030948f"
IMPLEMENTATION_RECEIPT_ID = "04c0692d"

PROBE_RUN_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_run_receipts" / f"{PROBE_RUN_RECEIPT_ID}.json"
DELTA_PROPOSAL_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_delta_proposals" / f"{DELTA_PROPOSAL_ID}.json"
DELTA_PROPOSAL_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_delta_proposal_receipts" / f"{DELTA_PROPOSAL_ID}.json"
PROBE_POLICY_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_policies" / f"{PROBE_POLICY_ID}.json"
PROBE_POLICY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_policy_receipts" / f"{PROBE_POLICY_ID}.json"
HALT_SURFACE_RUN_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_run_receipts" / f"{HALT_SURFACE_PROBE_RUN_RECEIPT_ID}.json"
IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_implementation_receipts" / f"{IMPLEMENTATION_RECEIPT_ID}.json"
LOCAL_REGIME_PATH = ROOT / "data" / "local_regime_v0_declarations" / f"{LOCAL_REGIME_HASH}.json"
RUNNER_MODULE_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_1.py"

OUT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_human_decisions"
OUT_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_human_decision_receipts"

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
    probe_run: Dict[str, Any],
    delta: Dict[str, Any],
    delta_receipt: Dict[str, Any],
    probe_policy: Dict[str, Any],
    probe_policy_receipt: Dict[str, Any],
    halt_surface: Dict[str, Any],
    implementation: Dict[str, Any],
    local_regime: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if probe_run.get("receipt_id") != PROBE_RUN_RECEIPT_ID:
        failures.append(f"probe_run_receipt_id_wrong:{probe_run.get('receipt_id')}")
    if probe_run.get("gate") != "PASS":
        failures.append(f"probe_run_gate_not_PASS:{probe_run.get('gate')}")
    if probe_run.get("probe_result_class") != "PROPOSAL_SURFACE_ABSENT_REQUIRES_DELTA_PROPOSAL":
        failures.append(f"probe_result_class_wrong:{probe_run.get('probe_result_class')}")
    if probe_run.get("proposal_surface_absent") is not True:
        failures.append(f"proposal_surface_absent_not_true:{probe_run.get('proposal_surface_absent')}")
    if probe_run.get("proposal_surface_present") is not False:
        failures.append(f"proposal_surface_present_not_false:{probe_run.get('proposal_surface_present')}")
    if probe_run.get("absence_recorded_as_observation_not_failure") is not True:
        failures.append("absence_not_recorded_as_observation")

    terminal = probe_run.get("terminal") or {}
    if terminal.get("type") != "STOP":
        failures.append(f"probe_terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != "STOP_HUMAN_DECISION_REQUIRED":
        failures.append(f"probe_terminal_stop_not_human_decision:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"probe_terminal_next_not_null:{terminal}")

    delta_ref = probe_run.get("delta_proposal") or {}
    if delta_ref.get("proposal_id") != DELTA_PROPOSAL_ID:
        failures.append(f"probe_delta_proposal_id_wrong:{delta_ref.get('proposal_id')}")
    if delta_ref.get("proposal_receipt_id") != DELTA_PROPOSAL_RECEIPT_ID:
        failures.append(f"probe_delta_proposal_receipt_id_wrong:{delta_ref.get('proposal_receipt_id')}")
    if delta_ref.get("proposal_status") != "REVIEW_REQUIRED_NOT_APPLIED":
        failures.append(f"probe_delta_status_wrong:{delta_ref.get('proposal_status')}")
    if delta_ref.get("artifact_only") is not True:
        failures.append("probe_delta_not_artifact_only")
    if delta_ref.get("not_applied") is not True:
        failures.append("probe_delta_not_applied_false")
    if delta_ref.get("requires_human_review") is not True:
        failures.append("probe_delta_requires_human_review_false")

    metrics = probe_run.get("aggregate_metrics") or {}
    expected_zero_metrics = [
        "runtime_proposal_emitted_count",
        "runtime_proposal_executed_count",
        "runtime_proposal_promoted_count",
        "registry_write_count",
        "local_regime_mutation_count",
        "runner_module_change_count",
    ]
    for key in expected_zero_metrics:
        if metrics.get(key) != 0:
            failures.append(f"probe_metric_not_zero:{key}:{metrics.get(key)}")
    if metrics.get("reviewable_delta_proposal_artifact_count") != 1:
        failures.append(f"delta_artifact_count_wrong:{metrics.get('reviewable_delta_proposal_artifact_count')}")
    if metrics.get("probe_case_count") != 4:
        failures.append(f"probe_case_count_wrong:{metrics.get('probe_case_count')}")
    if metrics.get("probe_case_pass_count") != 4:
        failures.append(f"probe_case_pass_count_wrong:{metrics.get('probe_case_pass_count')}")
    if metrics.get("probe_case_fail_count") != 0:
        failures.append(f"probe_case_fail_count_wrong:{metrics.get('probe_case_fail_count')}")

    guards = probe_run.get("authority_guards") or {}
    for key in [
        "runner_module_changed",
        "local_regime_replaced",
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
            failures.append(f"probe_authority_guard_not_false:{key}:{guards.get(key)}")

    if delta.get("proposal_id") != DELTA_PROPOSAL_ID:
        failures.append(f"delta_proposal_id_wrong:{delta.get('proposal_id')}")
    if delta.get("proposal_class") != "PROPOSITION_SURFACE_DELTA_PROPOSAL":
        failures.append(f"delta_proposal_class_wrong:{delta.get('proposal_class')}")
    if delta.get("proposal_status") != "REVIEW_REQUIRED_NOT_APPLIED":
        failures.append(f"delta_status_wrong:{delta.get('proposal_status')}")
    if delta.get("terminal_effect") != "NONE":
        failures.append(f"delta_terminal_effect_not_NONE:{delta.get('terminal_effect')}")

    delta_safety = delta.get("safety_clauses") or {}
    for key in [
        "artifact_only",
        "not_applied",
        "not_promoted",
        "does_not_modify_runner",
        "does_not_mutate_local_regime",
        "does_not_write_registry",
        "requires_human_review",
        "does_not_claim_global_taxonomy",
        "does_not_claim_final_schema",
        "does_not_claim_proof",
    ]:
        if delta_safety.get(key) is not True:
            failures.append(f"delta_safety_not_true:{key}:{delta_safety.get(key)}")

    requested = delta.get("requested_delta") or {}
    if requested.get("delta_kind") != "ADD_REVIEWABLE_HALT_WITH_PROPOSAL_SURFACE":
        failures.append(f"delta_kind_wrong:{requested.get('delta_kind')}")
    shape = requested.get("minimum_shape") or {}
    for key in [
        "halt_with_proposal",
        "proposal_non_execution",
        "duplicate_unresolved_proposal_guard",
        "human_review_required_before_promotion",
        "proposal_receipt_required",
    ]:
        if shape.get(key) is not True:
            failures.append(f"delta_minimum_shape_missing:{key}:{shape.get(key)}")

    if delta_receipt.get("receipt_id") != DELTA_PROPOSAL_RECEIPT_ID:
        failures.append(f"delta_receipt_id_wrong:{delta_receipt.get('receipt_id')}")
    if delta_receipt.get("proposal_id") != DELTA_PROPOSAL_ID:
        failures.append(f"delta_receipt_proposal_id_wrong:{delta_receipt.get('proposal_id')}")
    if delta_receipt.get("proposal_status") != "REVIEW_REQUIRED_NOT_APPLIED":
        failures.append(f"delta_receipt_status_wrong:{delta_receipt.get('proposal_status')}")
    if delta_receipt.get("gate") != "PASS":
        failures.append(f"delta_receipt_gate_not_PASS:{delta_receipt.get('gate')}")
    for key in [
        "artifact_only",
        "not_applied",
        "not_promoted",
        "requires_human_review",
    ]:
        if delta_receipt.get(key) is not True:
            failures.append(f"delta_receipt_required_true_missing:{key}:{delta_receipt.get(key)}")
    for key in [
        "runner_modified",
        "local_regime_mutated",
        "registry_written",
        "global_taxonomy_claimed",
        "final_schema_claimed",
        "proof_claimed",
    ]:
        if delta_receipt.get(key) is not False:
            failures.append(f"delta_receipt_required_false_wrong:{key}:{delta_receipt.get(key)}")

    if probe_policy.get("policy_id") != PROBE_POLICY_ID:
        failures.append(f"probe_policy_id_wrong:{probe_policy.get('policy_id')}")
    if probe_policy_receipt.get("receipt_id") != PROBE_POLICY_RECEIPT_ID:
        failures.append(f"probe_policy_receipt_id_wrong:{probe_policy_receipt.get('receipt_id')}")
    if probe_policy_receipt.get("gate") != "PASS":
        failures.append(f"probe_policy_receipt_gate_not_PASS:{probe_policy_receipt.get('gate')}")

    if halt_surface.get("receipt_id") != HALT_SURFACE_PROBE_RUN_RECEIPT_ID:
        failures.append(f"halt_surface_receipt_id_wrong:{halt_surface.get('receipt_id')}")
    if halt_surface.get("gate") != "PASS":
        failures.append(f"halt_surface_gate_not_PASS:{halt_surface.get('gate')}")
    if halt_surface.get("coverage_complete") is not True:
        failures.append(f"halt_surface_coverage_not_complete:{halt_surface.get('coverage_complete')}")

    if implementation.get("receipt_id") != IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"implementation_receipt_id_wrong:{implementation.get('receipt_id')}")
    if implementation.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{implementation.get('gate')}")

    if local_regime.get("local_regime_hash") != LOCAL_REGIME_HASH:
        failures.append(f"local_regime_hash_wrong:{local_regime.get('local_regime_hash')}")
    if local_regime.get("local_regime_version") != LOCAL_REGIME_VERSION:
        failures.append(f"local_regime_version_wrong:{local_regime.get('local_regime_version')}")

    for path, label in [
        (PROBE_RUN_RECEIPT_PATH, "proposition_surface_probe_run_receipt"),
        (DELTA_PROPOSAL_PATH, "delta_proposal"),
        (DELTA_PROPOSAL_RECEIPT_PATH, "delta_proposal_receipt"),
        (PROBE_POLICY_PATH, "proposition_surface_probe_policy"),
        (PROBE_POLICY_RECEIPT_PATH, "proposition_surface_probe_policy_receipt"),
        (HALT_SURFACE_RUN_RECEIPT_PATH, "halt_surface_run_receipt"),
        (IMPLEMENTATION_RECEIPT_PATH, "implementation_receipt"),
        (LOCAL_REGIME_PATH, "local_regime"),
        (RUNNER_MODULE_PATH, "runner_module"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{path.relative_to(ROOT).as_posix()}")

    return failures

def build_decision(write_outputs: bool = True) -> tuple[Dict[str, Any], Dict[str, Any]]:
    probe_run = read_json(PROBE_RUN_RECEIPT_PATH)
    delta = read_json(DELTA_PROPOSAL_PATH)
    delta_receipt = read_json(DELTA_PROPOSAL_RECEIPT_PATH)
    probe_policy = read_json(PROBE_POLICY_PATH)
    probe_policy_receipt = read_json(PROBE_POLICY_RECEIPT_PATH)
    halt_surface = read_json(HALT_SURFACE_RUN_RECEIPT_PATH)
    implementation = read_json(IMPLEMENTATION_RECEIPT_PATH)
    local_regime = read_json(LOCAL_REGIME_PATH)

    failures = validate_inputs(
        probe_run,
        delta,
        delta_receipt,
        probe_policy,
        probe_policy_receipt,
        halt_surface,
        implementation,
        local_regime,
    )

    seed = {
        "unit_id": UNIT_ID,
        "human_decision": "PROVISIONAL_ACCEPT",
        "delta_proposal_id": DELTA_PROPOSAL_ID,
        "source_probe_run_receipt_id": PROBE_RUN_RECEIPT_ID,
        "next_goal": NEXT_GOAL,
    }
    decision_id = sha8(seed)

    authority_guards = {
        "human_decision_recorded": True,
        "decision_accepts_delta_provisionally": True,
        "delta_proposal_consumed": True,
        "delta_proposal_applied": False,
        "delta_proposal_promoted": False,
        "runner_module_read": True,
        "runner_module_changed": False,
        "runner_executed": False,
        "local_regime_read": True,
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

    decision = {
        "schema_version": "jurisdiction_runner_v0_1_proposition_surface_human_decision_v0",
        "decision_type": "HUMAN_DECISION_PROVISIONAL_ACCEPT_PROPOSITION_SURFACE_DELTA",
        "decision_id": decision_id,
        "unit_id": UNIT_ID,
        "decision_status": "ACCEPTED_PROVISIONALLY_FOR_POLICY_BUILD_NOT_APPLIED",
        "runner_unit_id": RUNNER_UNIT_ID,
        "target_runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "target_local_regime_version": TARGET_LOCAL_REGIME_VERSION,
        "local_regime_hash": LOCAL_REGIME_HASH,
        "source_proposition_surface_probe_run_receipt_id": PROBE_RUN_RECEIPT_ID,
        "source_delta_proposal_id": DELTA_PROPOSAL_ID,
        "source_delta_proposal_receipt_id": DELTA_PROPOSAL_RECEIPT_ID,
        "source_proposition_surface_probe_policy_id": PROBE_POLICY_ID,
        "source_proposition_surface_probe_policy_receipt_id": PROBE_POLICY_RECEIPT_ID,
        "source_halt_surface_probe_run_receipt_id": HALT_SURFACE_PROBE_RUN_RECEIPT_ID,
        "source_implementation_receipt_id": IMPLEMENTATION_RECEIPT_ID,
        "decision_summary": {
            "observed_runtime_proposition_surface": "ABSENT",
            "accepted_delta_kind": "ADD_REVIEWABLE_HALT_WITH_PROPOSAL_SURFACE",
            "acceptance_scope": "policy-build target only",
            "not_current_runtime_promotion": True,
            "not_current_regime_mutation": True,
            "requires_bounded_upgrade_policy_before_implementation": True,
        },
        "accepted_minimum_shape": {
            "halt_with_proposal": True,
            "proposal_non_execution": True,
            "duplicate_unresolved_proposal_guard": True,
            "human_review_required_before_promotion": True,
            "proposal_receipt_required": True,
        },
        "authorized_operations_next": {
            "read_human_decision": True,
            "read_delta_proposal": True,
            "read_delta_proposal_receipt": True,
            "read_proposition_surface_probe_run_receipt": True,
            "read_local_regime_v0": True,
            "read_jurisdiction_runner_v0_1": True,
            "build_bounded_upgrade_policy": True,
            "target_local_regime_v1_policy_only": True,
            "target_jurisdiction_runner_v0_2_policy_only": True,
        },
        "forbidden_operations": {
            "modify_runner_module_in_decision_unit": True,
            "implement_upgrade_in_decision_unit": True,
            "apply_delta_proposal_in_decision_unit": True,
            "promote_delta_proposal_in_decision_unit": True,
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
            "decision_only": True,
            "does_not_modify_runner": True,
            "does_not_execute_runner": True,
            "does_not_apply_delta": True,
            "does_not_promote_delta": True,
            "does_not_mutate_local_regime": True,
            "does_not_write_registry": True,
            "does_not_claim_global_correctness": True,
            "does_not_claim_final_taxonomy": True,
            "does_not_claim_theorem_closure": True,
            "next_unit_required_for_policy_build": True,
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
        "decision_id": decision_id,
        "decision_status": decision["decision_status"],
        "source_delta_proposal_id": DELTA_PROPOSAL_ID,
        "terminal": decision["terminal"],
    }
    receipt_id = sha8(receipt_seed)

    receipt = {
        "schema_version": "jurisdiction_runner_v0_1_proposition_surface_human_decision_receipt_v0",
        "receipt_type": "JURISDICTION_RUNNER_V0_1_PROPOSITION_SURFACE_HUMAN_DECISION_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "decision_id": decision_id,
        "decision_type": decision["decision_type"],
        "decision_status": decision["decision_status"],
        "runner_unit_id": RUNNER_UNIT_ID,
        "target_runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "target_local_regime_version": TARGET_LOCAL_REGIME_VERSION,
        "local_regime_hash": LOCAL_REGIME_HASH,
        "source_proposition_surface_probe_run_receipt_id": PROBE_RUN_RECEIPT_ID,
        "source_delta_proposal_id": DELTA_PROPOSAL_ID,
        "source_delta_proposal_receipt_id": DELTA_PROPOSAL_RECEIPT_ID,
        "decision_summary": decision["decision_summary"],
        "accepted_minimum_shape": decision["accepted_minimum_shape"],
        "authorized_operations_next": decision["authorized_operations_next"],
        "forbidden_operations": decision["forbidden_operations"],
        "safety_clauses": decision["safety_clauses"],
        "authority_guards": authority_guards,
        "terminal": decision["terminal"],
        "gate": decision["gate"],
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    decision["decision_receipt_id"] = receipt_id

    if write_outputs:
        OUT_DIR.mkdir(parents=True, exist_ok=True)
        OUT_RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
        write_json(OUT_DIR / f"{decision_id}.json", decision)
        write_json(OUT_RECEIPT_DIR / f"{decision_id}.json", receipt)

    return decision, receipt

def main() -> int:
    decision, receipt = build_decision(write_outputs=True)
    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"human_decision_id={decision['decision_id']}")
    print(f"human_decision_receipt_id={receipt['receipt_id']}")
    print(f"human_decision_path=data/jurisdiction_runner_v0_1_proposition_surface_human_decisions/{decision['decision_id']}.json")
    print(f"human_decision_receipt_path=data/jurisdiction_runner_v0_1_proposition_surface_human_decision_receipts/{decision['decision_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
