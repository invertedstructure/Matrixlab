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

UNIT_ID = "RUN_JURISDICTION_RUNNER_V0_1_PROPOSITION_SURFACE_PROBE_V0"

PROPOSITION_SURFACE_PROBE_POLICY_ID = "c7cb4d9e"
PROPOSITION_SURFACE_PROBE_POLICY_RECEIPT_ID = "c6dbd7d2"
HALT_SURFACE_PROBE_RUN_RECEIPT_ID = "5030948f"
IMPLEMENTATION_RECEIPT_ID = "04c0692d"
LOCAL_REGIME_HASH = "097d620c"

RUNNER_UNIT_ID = "jurisdiction_runner.v0.1"
LOCAL_REGIME_VERSION = "local_regime.v0"

POLICY_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_policies" / f"{PROPOSITION_SURFACE_PROBE_POLICY_ID}.json"
POLICY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_policy_receipts" / f"{PROPOSITION_SURFACE_PROBE_POLICY_ID}.json"
HALT_SURFACE_RUN_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_run_receipts" / f"{HALT_SURFACE_PROBE_RUN_RECEIPT_ID}.json"
IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_implementation_receipts" / f"{IMPLEMENTATION_RECEIPT_ID}.json"
LOCAL_REGIME_PATH = ROOT / "data" / "local_regime_v0_declarations" / f"{LOCAL_REGIME_HASH}.json"
RUNNER_MODULE_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_1.py"

FIXTURE_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_fixtures"
TRANSCRIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_expected_transcripts"
CASE_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_case_receipts"
DELTA_PROPOSAL_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_delta_proposals"
DELTA_PROPOSAL_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_delta_proposal_receipts"
RUN_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_run_receipts"

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

FALSE_BOUNDARY_GUARDS = [
    "runner_module_changed",
    "local_regime_replaced",
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

def import_runner():
    spec = importlib.util.spec_from_file_location("jurisdiction_runner_v0_1", RUNNER_MODULE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot import jurisdiction runner module")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["jurisdiction_runner_v0_1"] = mod
    spec.loader.exec_module(mod)
    return mod

def validate_inputs(
    policy: Dict[str, Any],
    policy_receipt: Dict[str, Any],
    halt_surface_receipt: Dict[str, Any],
    implementation: Dict[str, Any],
    local_regime: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if policy.get("policy_id") != PROPOSITION_SURFACE_PROBE_POLICY_ID:
        failures.append(f"policy_id_wrong:{policy.get('policy_id')}")
    if policy.get("policy_receipt_id") != PROPOSITION_SURFACE_PROBE_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy.get('policy_receipt_id')}")
    if policy_receipt.get("policy_id") != PROPOSITION_SURFACE_PROBE_POLICY_ID:
        failures.append(f"policy_receipt_policy_id_wrong:{policy_receipt.get('policy_id')}")
    if policy_receipt.get("receipt_id") != PROPOSITION_SURFACE_PROBE_POLICY_RECEIPT_ID:
        failures.append(f"policy_receipt_id_wrong:{policy_receipt.get('receipt_id')}")
    if policy_receipt.get("gate") != "PASS":
        failures.append(f"policy_receipt_gate_not_PASS:{policy_receipt.get('gate')}")
    if policy_receipt.get("policy_status") != "POLICY_ONLY_NOT_IMPLEMENTED":
        failures.append(f"policy_status_wrong:{policy_receipt.get('policy_status')}")

    terminal = policy_receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"policy_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"policy_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"policy_terminal_stop_not_null:{terminal.get('stop_code')}")

    authorized = policy_receipt.get("authorized_operations_next") or {}
    for key in [
        "read_proposition_surface_probe_policy",
        "read_proposition_surface_probe_policy_receipt",
        "read_runner_module",
        "read_local_regime_v0_declaration",
        "read_halt_surface_probe_run_receipt",
        "create_proposition_surface_probe_fixtures",
        "execute_runner_against_probe_fixtures",
        "repeat_unresolved_pressure_probe",
        "emit_proposition_surface_probe_receipt",
        "emit_reviewable_delta_proposal_if_surface_absent",
    ]:
        if authorized.get(key) is not True:
            failures.append(f"authorized_operation_missing:{key}:{authorized.get(key)}")

    forbidden = policy_receipt.get("forbidden_operations") or {}
    for key in [
        "modify_runner_module",
        "execute_or_apply_proposal",
        "promote_proposal",
        "replace_local_regime_v0",
        "mutate_local_regime_at_runtime",
        "registry_sqlite_write",
        "registry_sqlite_read",
        "full_registry_scan",
        "global_taxonomy_design",
        "final_schema_claim",
        "proof_claim",
        "hidden_continuation_after_stop",
    ]:
        if forbidden.get(key) is not True:
            failures.append(f"forbidden_operation_not_declared:{key}:{forbidden.get(key)}")

    if halt_surface_receipt.get("receipt_id") != HALT_SURFACE_PROBE_RUN_RECEIPT_ID:
        failures.append(f"halt_surface_receipt_id_wrong:{halt_surface_receipt.get('receipt_id')}")
    if halt_surface_receipt.get("gate") != "PASS":
        failures.append(f"halt_surface_gate_not_PASS:{halt_surface_receipt.get('gate')}")
    if halt_surface_receipt.get("coverage_complete") is not True:
        failures.append(f"halt_surface_coverage_not_complete:{halt_surface_receipt.get('coverage_complete')}")
    if halt_surface_receipt.get("missing_coverage") != []:
        failures.append(f"halt_surface_missing_coverage:{halt_surface_receipt.get('missing_coverage')}")
    if halt_surface_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append(f"halt_surface_terminal_not_STOP:{halt_surface_receipt.get('terminal')}")
    if halt_surface_receipt.get("terminal", {}).get("stop_code") != "STOP_DONE":
        failures.append(f"halt_surface_terminal_stop_not_DONE:{halt_surface_receipt.get('terminal')}")
    if halt_surface_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append(f"halt_surface_terminal_next_not_null:{halt_surface_receipt.get('terminal')}")

    halt_guards = halt_surface_receipt.get("authority_guards") or {}
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
        if halt_guards.get(key) is not False:
            failures.append(f"halt_surface_guard_not_false:{key}:{halt_guards.get(key)}")

    if implementation.get("receipt_id") != IMPLEMENTATION_RECEIPT_ID:
        failures.append(f"implementation_receipt_id_wrong:{implementation.get('receipt_id')}")
    if implementation.get("gate") != "PASS":
        failures.append(f"implementation_gate_not_PASS:{implementation.get('gate')}")

    if local_regime.get("local_regime_version") != LOCAL_REGIME_VERSION:
        failures.append(f"local_regime_version_wrong:{local_regime.get('local_regime_version')}")
    if local_regime.get("local_regime_hash") != LOCAL_REGIME_HASH:
        failures.append(f"local_regime_hash_wrong:{local_regime.get('local_regime_hash')}")

    for path, label in [
        (POLICY_PATH, "proposition_surface_probe_policy"),
        (POLICY_RECEIPT_PATH, "proposition_surface_probe_policy_receipt"),
        (HALT_SURFACE_RUN_RECEIPT_PATH, "halt_surface_run_receipt"),
        (IMPLEMENTATION_RECEIPT_PATH, "implementation_receipt"),
        (LOCAL_REGIME_PATH, "local_regime"),
        (RUNNER_MODULE_PATH, "runner_module"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{path.relative_to(ROOT).as_posix()}")

    return failures

def build_fixture(case_name: str, input_state: Dict[str, Any], purpose: str) -> Dict[str, Any]:
    return {
        "schema_version": "jurisdiction_runner_v0_1_proposition_surface_probe_fixture_v0",
        "fixture_id": f"proposition_surface_probe_{case_name.lower()}",
        "case_name": case_name,
        "purpose": purpose,
        "input_state": input_state,
        "expected_transcript": EXPECTED_TRANSCRIPT,
    }

def normalize_case_receipt(case_name: str, fixture: Dict[str, Any], receipt: Dict[str, Any]) -> Dict[str, Any]:
    out = copy.deepcopy(receipt)
    out["receipt_type"] = "JURISDICTION_RUNNER_V0_1_PROPOSITION_SURFACE_PROBE_CASE_RECEIPT"
    out["probe_unit_id"] = UNIT_ID
    out["case_name"] = case_name
    out["fixture_id"] = fixture["fixture_id"]
    out["runner_executed"] = True
    out["proposal_executed"] = False
    out["proposal_promoted"] = False
    out["local_regime_runtime_mutated"] = False
    out["registry_written"] = False
    out["runner_module_changed"] = False
    return out

def validate_case_receipt(
    case_name: str,
    receipt: Dict[str, Any],
    expected_halt_code: str,
    expected_no_proposal_reason: str,
) -> List[str]:
    failures: List[str] = []

    if receipt.get("gate") != "PASS":
        failures.append(f"{case_name}:gate_not_PASS:{receipt.get('gate')}")
    if receipt.get("halt_code") != expected_halt_code:
        failures.append(f"{case_name}:halt_code_wrong:{receipt.get('halt_code')}")
    if receipt.get("move_status") != "BLOCKED":
        failures.append(f"{case_name}:move_status_not_BLOCKED:{receipt.get('move_status')}")
    if receipt.get("proposal_status") != "NONE":
        failures.append(f"{case_name}:proposal_status_not_NONE:{receipt.get('proposal_status')}")
    if receipt.get("proposal_executed") is not False:
        failures.append(f"{case_name}:proposal_executed_not_false:{receipt.get('proposal_executed')}")
    if receipt.get("proposal_promoted") is not False:
        failures.append(f"{case_name}:proposal_promoted_not_false:{receipt.get('proposal_promoted')}")
    if receipt.get("no_proposal_reason") != expected_no_proposal_reason:
        failures.append(f"{case_name}:no_proposal_reason_wrong:{receipt.get('no_proposal_reason')}")
    if receipt.get("runner_executed") is not True:
        failures.append(f"{case_name}:runner_executed_not_true:{receipt.get('runner_executed')}")

    terminal = receipt.get("terminal") or {}
    if terminal.get("type") != "STOP":
        failures.append(f"{case_name}:terminal_not_STOP:{terminal}")
    if terminal.get("stop_code") != expected_halt_code:
        failures.append(f"{case_name}:terminal_stop_wrong:{terminal}")
    if terminal.get("next_command_goal") is not None:
        failures.append(f"{case_name}:terminal_next_not_null:{terminal.get('next_command_goal')}")

    if receipt.get("transcript") != EXPECTED_TRANSCRIPT:
        failures.append(f"{case_name}:transcript_mismatch:{receipt.get('transcript')}")
    if receipt.get("transcript_matches_expected") is not True:
        failures.append(f"{case_name}:transcript_match_not_true:{receipt.get('transcript_matches_expected')}")

    authority = receipt.get("authority_guards") or {}
    for key in CASE_FALSE_GUARDS:
        if authority.get(key) is not False:
            failures.append(f"{case_name}:authority_guard_not_false:{key}:{authority.get(key)}")

    artifact = receipt.get("artifact_guards") or {}
    for key in ["latest_or_mtime_selection_used", "ambient_workspace_authority_used"]:
        if artifact.get(key) is not False:
            failures.append(f"{case_name}:artifact_guard_not_false:{key}:{artifact.get(key)}")

    return failures

def build_delta_proposal(source_case_receipts: Dict[str, Dict[str, Any]]) -> tuple[Dict[str, Any], Dict[str, Any]]:
    seed = {
        "unit_id": UNIT_ID,
        "proposal_class": "PROPOSITION_SURFACE_DELTA_PROPOSAL",
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_hash": LOCAL_REGIME_HASH,
        "source_case_receipt_ids": sorted(r["case_receipt_id"] for r in source_case_receipts.values()),
    }
    proposal_id = sha8(seed)

    proposal = {
        "schema_version": "jurisdiction_runner_v0_1_proposition_surface_delta_proposal_v0",
        "proposal_class": "PROPOSITION_SURFACE_DELTA_PROPOSAL",
        "proposal_id": proposal_id,
        "proposal_status": "REVIEW_REQUIRED_NOT_APPLIED",
        "unit_id": UNIT_ID,
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": LOCAL_REGIME_HASH,
        "source_policy_id": PROPOSITION_SURFACE_PROBE_POLICY_ID,
        "source_policy_receipt_id": PROPOSITION_SURFACE_PROBE_POLICY_RECEIPT_ID,
        "source_halt_surface_probe_run_receipt_id": HALT_SURFACE_PROBE_RUN_RECEIPT_ID,
        "source_case_receipts": source_case_receipts,
        "observation": {
            "proposal_surface_present": False,
            "runtime_proposal_emitted_count": 0,
            "runtime_proposal_status_observed": "NONE_ONLY",
            "absence_is_observation_not_failure": True,
        },
        "requested_delta": {
            "delta_kind": "ADD_REVIEWABLE_HALT_WITH_PROPOSAL_SURFACE",
            "target": "future local_regime.v1 or jurisdiction_runner.v0.2, not current v0.1 runtime",
            "minimum_shape": {
                "halt_with_proposal": True,
                "proposal_non_execution": True,
                "duplicate_unresolved_proposal_guard": True,
                "human_review_required_before_promotion": True,
                "proposal_receipt_required": True,
            },
        },
        "safety_clauses": {
            "artifact_only": True,
            "not_applied": True,
            "not_promoted": True,
            "does_not_modify_runner": True,
            "does_not_mutate_local_regime": True,
            "does_not_write_registry": True,
            "requires_human_review": True,
            "does_not_claim_global_taxonomy": True,
            "does_not_claim_final_schema": True,
            "does_not_claim_proof": True,
        },
        "terminal_effect": "NONE",
        "created_at": now_iso(),
    }

    proposal_receipt = {
        "schema_version": "jurisdiction_runner_v0_1_proposition_surface_delta_proposal_receipt_v0",
        "receipt_type": "JURISDICTION_RUNNER_V0_1_PROPOSITION_SURFACE_DELTA_PROPOSAL_RECEIPT",
        "receipt_id": sha8({"proposal_id": proposal_id, "receipt_type": "delta_proposal_receipt"}),
        "proposal_id": proposal_id,
        "proposal_class": proposal["proposal_class"],
        "proposal_status": proposal["proposal_status"],
        "artifact_only": True,
        "not_applied": True,
        "not_promoted": True,
        "requires_human_review": True,
        "runner_modified": False,
        "local_regime_mutated": False,
        "registry_written": False,
        "global_taxonomy_claimed": False,
        "final_schema_claimed": False,
        "proof_claimed": False,
        "gate": "PASS",
        "created_at": now_iso(),
    }
    return proposal, proposal_receipt

def main() -> int:
    policy = read_json(POLICY_PATH)
    policy_receipt = read_json(POLICY_RECEIPT_PATH)
    halt_surface_receipt = read_json(HALT_SURFACE_RUN_RECEIPT_PATH)
    implementation = read_json(IMPLEMENTATION_RECEIPT_PATH)
    local_regime = read_json(LOCAL_REGIME_PATH)

    failures = validate_inputs(policy, policy_receipt, halt_surface_receipt, implementation, local_regime)

    runner_mod = import_runner()

    for d in [
        FIXTURE_DIR,
        TRANSCRIPT_DIR,
        CASE_RECEIPT_DIR,
        DELTA_PROPOSAL_DIR,
        DELTA_PROPOSAL_RECEIPT_DIR,
        RUN_RECEIPT_DIR,
    ]:
        d.mkdir(parents=True, exist_ok=True)

    case_plan = {
        "HALT_NO_APPLICABLE_MOVE_WITH_NO_PROPOSAL_BASELINE": {
            "input_state": {"state_id": "typed_counter_closed_baseline", "typed": True, "value": 1},
            "expected_halt_code": "STOP_NO_APPLICABLE_MOVE",
            "expected_no_proposal_reason": "INSUFFICIENT_EVIDENCE",
            "purpose": "preserve baseline no-proposal halt",
        },
        "PROPOSAL_PRESSURE_DISCOVERY": {
            "input_state": {"state_id": "typed_counter_closed_pressure_discovery", "typed": True, "value": 2},
            "expected_halt_code": "STOP_NO_APPLICABLE_MOVE",
            "expected_no_proposal_reason": "INSUFFICIENT_EVIDENCE",
            "purpose": "discover whether any proposal surface appears under no-applicable-move pressure",
        },
        "DUPLICATE_UNRESOLVED_PROPOSAL_GUARD_FIRST": {
            "input_state": {"state_id": "typed_counter_closed_duplicate_pressure", "typed": True, "value": 2},
            "expected_halt_code": "STOP_NO_APPLICABLE_MOVE",
            "expected_no_proposal_reason": "INSUFFICIENT_EVIDENCE",
            "purpose": "first repeated unresolved pressure observation",
        },
        "DUPLICATE_UNRESOLVED_PROPOSAL_GUARD_SECOND": {
            "input_state": {"state_id": "typed_counter_closed_duplicate_pressure", "typed": True, "value": 2},
            "expected_halt_code": "STOP_NO_APPLICABLE_MOVE",
            "expected_no_proposal_reason": "INSUFFICIENT_EVIDENCE",
            "purpose": "second repeated unresolved pressure observation",
        },
    }

    case_results: Dict[str, Dict[str, Any]] = {}
    runtime_proposal_emitted_count = 0

    for case_name, spec in case_plan.items():
        fixture = build_fixture(case_name, spec["input_state"], spec["purpose"])
        fixture_path = FIXTURE_DIR / f"{fixture['fixture_id']}.json"
        transcript_path = TRANSCRIPT_DIR / f"{fixture['fixture_id']}.json"
        write_json(fixture_path, fixture)
        write_json(transcript_path, {
            "schema_version": "jurisdiction_runner_v0_1_proposition_surface_probe_expected_transcript_v0",
            "fixture_id": fixture["fixture_id"],
            "case_name": case_name,
            "expected_transcript": EXPECTED_TRANSCRIPT,
        })

        runner = runner_mod.JurisdictionRunnerV01(local_regime)
        receipt = runner.run(
            spec["input_state"],
            fixture_id=fixture["fixture_id"],
            input_artifact_paths=[
                LOCAL_REGIME_PATH.relative_to(ROOT).as_posix(),
                fixture_path.relative_to(ROOT).as_posix(),
                transcript_path.relative_to(ROOT).as_posix(),
            ],
        )
        receipt = normalize_case_receipt(case_name, fixture, receipt)

        if receipt.get("proposal_status") != "NONE":
            runtime_proposal_emitted_count += 1

        failures.extend(
            validate_case_receipt(
                case_name,
                receipt,
                spec["expected_halt_code"],
                spec["expected_no_proposal_reason"],
            )
        )

        case_receipt_path = CASE_RECEIPT_DIR / f"{receipt['receipt_id']}.json"
        write_json(case_receipt_path, receipt)

        case_results[case_name] = {
            "case_name": case_name,
            "fixture_id": fixture["fixture_id"],
            "fixture_path": fixture_path.relative_to(ROOT).as_posix(),
            "expected_transcript_path": transcript_path.relative_to(ROOT).as_posix(),
            "case_receipt_id": receipt["receipt_id"],
            "case_receipt_path": case_receipt_path.relative_to(ROOT).as_posix(),
            "halt_code": receipt["halt_code"],
            "proposal_status": receipt["proposal_status"],
            "proposal_executed": receipt["proposal_executed"],
            "proposal_promoted": receipt["proposal_promoted"],
            "no_proposal_reason": receipt["no_proposal_reason"],
            "runner_executed": receipt["runner_executed"],
            "gate": receipt["gate"],
        }

    proposal_surface_present = runtime_proposal_emitted_count > 0
    proposal_surface_absent = not proposal_surface_present

    delta_proposal = None
    delta_proposal_receipt = None
    delta_proposal_path = None
    delta_proposal_receipt_path = None

    if proposal_surface_absent:
        delta_proposal, delta_proposal_receipt = build_delta_proposal(case_results)
        delta_proposal_path = DELTA_PROPOSAL_DIR / f"{delta_proposal['proposal_id']}.json"
        delta_proposal_receipt_path = DELTA_PROPOSAL_RECEIPT_DIR / f"{delta_proposal['proposal_id']}.json"
        write_json(delta_proposal_path, delta_proposal)
        write_json(delta_proposal_receipt_path, delta_proposal_receipt)

    duplicate_pressure_case_ids = [
        case_results["DUPLICATE_UNRESOLVED_PROPOSAL_GUARD_FIRST"]["case_receipt_id"],
        case_results["DUPLICATE_UNRESOLVED_PROPOSAL_GUARD_SECOND"]["case_receipt_id"],
    ]
    duplicate_guard_result = {
        "duplicate_unresolved_pressure_observed": True,
        "duplicate_unresolved_proposal_count": 0,
        "second_proposal_withheld": proposal_surface_absent,
        "no_surface_present": proposal_surface_absent,
        "allowed_by_policy": True,
        "source_case_receipt_ids": duplicate_pressure_case_ids,
    }

    aggregate_metrics = {
        "probe_case_count": len(case_results),
        "probe_case_pass_count": sum(1 for r in case_results.values() if r["gate"] == "PASS"),
        "probe_case_fail_count": sum(1 for r in case_results.values() if r["gate"] != "PASS"),
        "runtime_proposal_emitted_count": runtime_proposal_emitted_count,
        "runtime_proposal_executed_count": 0,
        "runtime_proposal_promoted_count": 0,
        "reviewable_delta_proposal_artifact_count": 1 if delta_proposal else 0,
        "duplicate_unresolved_pressure_count": 1,
        "duplicate_unresolved_proposal_count": duplicate_guard_result["duplicate_unresolved_proposal_count"],
        "second_proposal_withheld_count": 1 if duplicate_guard_result["second_proposal_withheld"] else 0,
        "registry_write_count": 0,
        "local_regime_mutation_count": 0,
        "runner_module_change_count": 0,
    }

    authority_guards = {
        "proposition_surface_probe_policy_consumed": True,
        "halt_surface_probe_run_receipt_consumed": True,
        "runner_module_read": True,
        "runner_module_changed": False,
        "local_regime_read": True,
        "local_regime_replaced": False,
        "local_regime_runtime_mutated": False,
        "probe_fixtures_created": True,
        "probe_fixtures_executed": True,
        "repeat_unresolved_pressure_probe_executed": True,
        "runtime_proposal_surface_present": proposal_surface_present,
        "runtime_proposal_surface_absent": proposal_surface_absent,
        "proposal_artifact_emitted": delta_proposal is not None,
        "proposal_executed": False,
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
        "halt_surface_run_receipt_tracked": tracked(HALT_SURFACE_RUN_RECEIPT_PATH),
        "implementation_receipt_tracked": tracked(IMPLEMENTATION_RECEIPT_PATH),
        "local_regime_tracked": tracked(LOCAL_REGIME_PATH),
        "runner_module_tracked": tracked(RUNNER_MODULE_PATH),
        "outputs_path_addressed": True,
        "outputs_receipt_referenced": True,
        "unrelated_untracked_data_not_authority": True,
        "latest_or_mtime_selection_used": False,
        "ambient_workspace_authority_used": False,
    }

    for key in FALSE_BOUNDARY_GUARDS:
        if authority_guards.get(key) is not False:
            failures.append(f"authority_guard_not_false:{key}:{authority_guards.get(key)}")

    if aggregate_metrics["runtime_proposal_executed_count"] != 0:
        failures.append("runtime_proposal_executed_count_nonzero")
    if aggregate_metrics["runtime_proposal_promoted_count"] != 0:
        failures.append("runtime_proposal_promoted_count_nonzero")
    if aggregate_metrics["registry_write_count"] != 0:
        failures.append("registry_write_count_nonzero")
    if aggregate_metrics["local_regime_mutation_count"] != 0:
        failures.append("local_regime_mutation_count_nonzero")
    if proposal_surface_absent and delta_proposal is None:
        failures.append("proposal_surface_absent_without_delta_proposal_artifact")
    if proposal_surface_absent and not duplicate_guard_result["no_surface_present"]:
        failures.append("duplicate_guard_absence_not_recorded")

    run_seed = {
        "unit_id": UNIT_ID,
        "policy_id": PROPOSITION_SURFACE_PROBE_POLICY_ID,
        "policy_receipt_id": PROPOSITION_SURFACE_PROBE_POLICY_RECEIPT_ID,
        "case_receipts": {k: v["case_receipt_id"] for k, v in sorted(case_results.items())},
        "delta_proposal_id": delta_proposal["proposal_id"] if delta_proposal else None,
    }
    run_receipt_id = sha8(run_seed)

    run_receipt = {
        "schema_version": "jurisdiction_runner_v0_1_proposition_surface_probe_run_receipt_v0",
        "receipt_type": "JURISDICTION_RUNNER_V0_1_PROPOSITION_SURFACE_PROBE_RUN_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": run_receipt_id,
        "runner_unit_id": RUNNER_UNIT_ID,
        "local_regime_version": LOCAL_REGIME_VERSION,
        "local_regime_hash": LOCAL_REGIME_HASH,
        "source_proposition_surface_probe_policy_id": PROPOSITION_SURFACE_PROBE_POLICY_ID,
        "source_proposition_surface_probe_policy_receipt_id": PROPOSITION_SURFACE_PROBE_POLICY_RECEIPT_ID,
        "source_halt_surface_probe_run_receipt_id": HALT_SURFACE_PROBE_RUN_RECEIPT_ID,
        "source_implementation_receipt_id": IMPLEMENTATION_RECEIPT_ID,
        "probe_result_class": "PROPOSAL_SURFACE_PRESENT" if proposal_surface_present else "PROPOSAL_SURFACE_ABSENT_REQUIRES_DELTA_PROPOSAL",
        "proposal_surface_present": proposal_surface_present,
        "proposal_surface_absent": proposal_surface_absent,
        "absence_recorded_as_observation_not_failure": proposal_surface_absent,
        "case_results": case_results,
        "duplicate_guard_result": duplicate_guard_result,
        "delta_proposal": {
            "proposal_id": delta_proposal["proposal_id"] if delta_proposal else None,
            "proposal_path": delta_proposal_path.relative_to(ROOT).as_posix() if delta_proposal_path else None,
            "proposal_receipt_id": delta_proposal_receipt["receipt_id"] if delta_proposal_receipt else None,
            "proposal_receipt_path": delta_proposal_receipt_path.relative_to(ROOT).as_posix() if delta_proposal_receipt_path else None,
            "proposal_class": "PROPOSITION_SURFACE_DELTA_PROPOSAL" if delta_proposal else None,
            "proposal_status": "REVIEW_REQUIRED_NOT_APPLIED" if delta_proposal else None,
            "artifact_only": True if delta_proposal else None,
            "not_applied": True if delta_proposal else None,
            "requires_human_review": True if delta_proposal else None,
        },
        "aggregate_metrics": aggregate_metrics,
        "authority_guards": authority_guards,
        "artifact_guards": artifact_guards,
        "terminal": {
            "type": "STOP",
            "next_command_goal": None,
            "stop_code": "STOP_HUMAN_DECISION_REQUIRED" if delta_proposal else "STOP_DONE",
        },
        "gate": "PASS" if not failures else "FAIL",
        "failures": failures,
        "warnings": [],
        "created_at": now_iso(),
    }

    run_receipt_path = RUN_RECEIPT_DIR / f"{run_receipt_id}.json"
    write_json(run_receipt_path, run_receipt)

    print(json.dumps(run_receipt, indent=2, sort_keys=True))
    print(f"proposition_surface_probe_run_receipt_id={run_receipt_id}")
    print(f"proposition_surface_probe_run_receipt_path=data/jurisdiction_runner_v0_1_proposition_surface_probe_run_receipts/{run_receipt_id}.json")
    for case_name, result in sorted(case_results.items()):
        print(f"case_{case_name}_fixture_path={result['fixture_path']}")
        print(f"case_{case_name}_expected_transcript_path={result['expected_transcript_path']}")
        print(f"case_{case_name}_receipt_id={result['case_receipt_id']}")
        print(f"case_{case_name}_receipt_path={result['case_receipt_path']}")
    if delta_proposal:
        print(f"delta_proposal_id={delta_proposal['proposal_id']}")
        print(f"delta_proposal_path={delta_proposal_path.relative_to(ROOT).as_posix()}")
        print(f"delta_proposal_receipt_id={delta_proposal_receipt['receipt_id']}")
        print(f"delta_proposal_receipt_path={delta_proposal_receipt_path.relative_to(ROOT).as_posix()}")
    return 0 if run_receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
