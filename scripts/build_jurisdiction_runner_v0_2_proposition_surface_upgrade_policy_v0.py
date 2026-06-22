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

UNIT_ID = "BUILD_JURISDICTION_RUNNER_V0_2_PROPOSITION_SURFACE_UPGRADE_POLICY_V0"
NEXT_GOAL = "IMPLEMENT_JURISDICTION_RUNNER_V0_2_PROPOSITION_SURFACE_UPGRADE_WITH_FIXTURES_V0"

SOURCE_RUNNER_UNIT_ID = "jurisdiction_runner.v0.1"
TARGET_RUNNER_UNIT_ID = "jurisdiction_runner.v0.2"
SOURCE_LOCAL_REGIME_VERSION = "local_regime.v0"
TARGET_LOCAL_REGIME_VERSION = "local_regime.v1"
SOURCE_LOCAL_REGIME_HASH = "097d620c"

HUMAN_DECISION_ID = "cef49876"
HUMAN_DECISION_RECEIPT_ID = "b80f0f1f"
DELTA_PROPOSAL_ID = "6e4ee1ea"
DELTA_PROPOSAL_RECEIPT_ID = "e919d594"
PROPOSITION_SURFACE_PROBE_RUN_RECEIPT_ID = "0d2f03d4"
PROPOSITION_SURFACE_PROBE_POLICY_ID = "c7cb4d9e"
PROPOSITION_SURFACE_PROBE_POLICY_RECEIPT_ID = "c6dbd7d2"
HALT_SURFACE_PROBE_RUN_RECEIPT_ID = "5030948f"
IMPLEMENTATION_RECEIPT_ID = "04c0692d"

HUMAN_DECISION_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_human_decisions" / f"{HUMAN_DECISION_ID}.json"
HUMAN_DECISION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_human_decision_receipts" / f"{HUMAN_DECISION_ID}.json"
DELTA_PROPOSAL_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_delta_proposals" / f"{DELTA_PROPOSAL_ID}.json"
DELTA_PROPOSAL_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_delta_proposal_receipts" / f"{DELTA_PROPOSAL_ID}.json"
PROBE_RUN_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_run_receipts" / f"{PROPOSITION_SURFACE_PROBE_RUN_RECEIPT_ID}.json"
PROBE_POLICY_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_policies" / f"{PROPOSITION_SURFACE_PROBE_POLICY_ID}.json"
PROBE_POLICY_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_proposition_surface_probe_policy_receipts" / f"{PROPOSITION_SURFACE_PROBE_POLICY_ID}.json"
HALT_SURFACE_RUN_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_halt_surface_probe_run_receipts" / f"{HALT_SURFACE_PROBE_RUN_RECEIPT_ID}.json"
IMPLEMENTATION_RECEIPT_PATH = ROOT / "data" / "jurisdiction_runner_v0_1_implementation_receipts" / f"{IMPLEMENTATION_RECEIPT_ID}.json"
LOCAL_REGIME_PATH = ROOT / "data" / "local_regime_v0_declarations" / f"{SOURCE_LOCAL_REGIME_HASH}.json"
RUNNER_MODULE_PATH = ROOT / "src" / "matrixlab" / "jurisdiction_runner_v0_1.py"

OUT_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_policies"
OUT_RECEIPT_DIR = ROOT / "data" / "jurisdiction_runner_v0_2_proposition_surface_upgrade_policy_receipts"

ACCEPTED_MINIMUM_SHAPE = {
    "halt_with_proposal": True,
    "proposal_non_execution": True,
    "duplicate_unresolved_proposal_guard": True,
    "human_review_required_before_promotion": True,
    "proposal_receipt_required": True,
}

V0_2_ACCEPTANCE_GATES = {
    "S0_source_chain_verified": {
        "required": True,
        "description": "Human decision, delta proposal, probe run, halt-surface run, implementation receipt, local_regime.v0, and runner v0.1 are path-addressed and tracked.",
    },
    "S1_local_regime_v1_declared": {
        "required": True,
        "description": "Emit local_regime.v1 declaration as a new artifact derived from v0, without replacing or mutating v0.",
    },
    "S2_runner_v0_2_implemented": {
        "required": True,
        "description": "Implement jurisdiction_runner.v0.2 as a separate module; do not modify v0.1.",
    },
    "S3_halt_with_proposal_fixture_passes": {
        "required": True,
        "description": "Under allowed proposal pressure, runner halts with proposal artifact and receipt.",
    },
    "S4_proposal_non_execution_passes": {
        "required": True,
        "description": "Proposal is never executed, never applied, and never promoted by runner.",
    },
    "S5_duplicate_unresolved_proposal_guard_passes": {
        "required": True,
        "description": "Repeated unresolved proposal pressure is blocked, counted, or linked to existing unresolved proposal without spam.",
    },
    "S6_no_hidden_continuation": {
        "required": True,
        "description": "All proposal halts terminate with STOP and no next command unless human decision artifact authorizes later unit.",
    },
    "S7_no_registry_or_global_taxonomy": {
        "required": True,
        "description": "No SQLite registry read/write, no global taxonomy claim, no final schema claim, no proof claim.",
    },
}

REQUIRED_IMPLEMENTATION_ARTIFACTS = {
    "local_regime_v1_declaration": "data/local_regime_v1_declarations/<local_regime_v1_hash>.json",
    "runner_v0_2_module": "src/matrixlab/jurisdiction_runner_v0_2.py",
    "implementation_receipt": "data/jurisdiction_runner_v0_2_proposition_surface_upgrade_implementation_receipts/<receipt_id>.json",
    "proposal_fixtures": "data/jurisdiction_runner_v0_2_proposition_surface_upgrade_fixtures/*.json",
    "expected_transcripts": "data/jurisdiction_runner_v0_2_proposition_surface_upgrade_expected_transcripts/*.json",
    "case_receipts": "data/jurisdiction_runner_v0_2_proposition_surface_upgrade_case_receipts/*.json",
    "proposal_receipts": "data/jurisdiction_runner_v0_2_proposition_surface_upgrade_proposal_receipts/*.json",
}

REQUIRED_FIXTURE_CASES = {
    "HALT_WITH_PROPOSAL_ON_NO_APPLICABLE_MOVE": {
        "purpose": "When a typed object has no applicable move and enough bounded evidence exists, runner emits a proposal artifact and halts.",
        "expected_halt_code": "STOP_NO_APPLICABLE_MOVE",
        "expected_proposal_status": "EMITTED_REVIEW_REQUIRED",
        "expected_proposal_type": "LOCAL_MOVE_ADMISSIBILITY_DELTA_PROPOSAL",
        "must_execute_proposal": False,
        "must_promote_proposal": False,
    },
    "PROPOSAL_NON_EXECUTION_GUARD": {
        "purpose": "A proposal cannot cause runtime state transition, registry write, local regime mutation, or hidden continuation.",
        "expected_proposal_executed": False,
        "expected_proposal_promoted": False,
        "expected_local_regime_mutated": False,
        "expected_registry_written": False,
    },
    "DUPLICATE_UNRESOLVED_PROPOSAL_GUARD_FIRST": {
        "purpose": "First unresolved proposal pressure may emit one review-required proposal.",
        "expected_duplicate_unresolved_proposal_count": 0,
    },
    "DUPLICATE_UNRESOLVED_PROPOSAL_GUARD_SECOND": {
        "purpose": "Second identical unresolved pressure must not emit a duplicate proposal; it must withhold, link, or increment duplicate count.",
        "allowed_results": [
            "SECOND_PROPOSAL_WITHHELD_LINKED_TO_EXISTING",
            "DUPLICATE_UNRESOLVED_PROPOSAL_COUNT_INCREMENTED",
        ],
    },
    "NO_PROPOSAL_WHEN_INSUFFICIENT_EVIDENCE": {
        "purpose": "If proposal evidence is insufficient, preserve v0.1 no-proposal behavior.",
        "expected_proposal_status": "NONE",
        "expected_no_proposal_reason": "INSUFFICIENT_EVIDENCE",
    },
    "AUTHORITY_VIOLATION_NO_PROPOSAL_PROMOTION": {
        "purpose": "Authority-boundary halts may not promote proposal or mutate the local regime.",
        "expected_halt_code": "STOP_AUTHORITY_VIOLATION",
        "expected_proposal_promoted": False,
    },
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
    human_decision: Dict[str, Any],
    human_decision_receipt: Dict[str, Any],
    delta: Dict[str, Any],
    delta_receipt: Dict[str, Any],
    probe_run: Dict[str, Any],
    probe_policy: Dict[str, Any],
    probe_policy_receipt: Dict[str, Any],
    halt_surface: Dict[str, Any],
    implementation: Dict[str, Any],
    local_regime: Dict[str, Any],
) -> List[str]:
    failures: List[str] = []

    if human_decision.get("decision_id") != HUMAN_DECISION_ID:
        failures.append(f"human_decision_id_wrong:{human_decision.get('decision_id')}")
    if human_decision.get("decision_receipt_id") != HUMAN_DECISION_RECEIPT_ID:
        failures.append(f"human_decision_receipt_id_wrong:{human_decision.get('decision_receipt_id')}")
    if human_decision_receipt.get("decision_id") != HUMAN_DECISION_ID:
        failures.append(f"human_decision_receipt_decision_id_wrong:{human_decision_receipt.get('decision_id')}")
    if human_decision_receipt.get("receipt_id") != HUMAN_DECISION_RECEIPT_ID:
        failures.append(f"human_decision_receipt_id_wrong:{human_decision_receipt.get('receipt_id')}")
    if human_decision_receipt.get("gate") != "PASS":
        failures.append(f"human_decision_receipt_gate_not_PASS:{human_decision_receipt.get('gate')}")
    if human_decision_receipt.get("decision_status") != "ACCEPTED_PROVISIONALLY_FOR_POLICY_BUILD_NOT_APPLIED":
        failures.append(f"human_decision_status_wrong:{human_decision_receipt.get('decision_status')}")

    terminal = human_decision_receipt.get("terminal") or {}
    if terminal.get("type") != "ADVANCE":
        failures.append(f"human_decision_terminal_not_ADVANCE:{terminal}")
    if terminal.get("next_command_goal") != UNIT_ID:
        failures.append(f"human_decision_terminal_next_wrong:{terminal.get('next_command_goal')}")
    if terminal.get("stop_code") is not None:
        failures.append(f"human_decision_terminal_stop_not_null:{terminal.get('stop_code')}")

    summary = human_decision_receipt.get("decision_summary") or {}
    if summary.get("observed_runtime_proposition_surface") != "ABSENT":
        failures.append(f"decision_summary_surface_wrong:{summary.get('observed_runtime_proposition_surface')}")
    if summary.get("accepted_delta_kind") != "ADD_REVIEWABLE_HALT_WITH_PROPOSAL_SURFACE":
        failures.append(f"decision_summary_delta_kind_wrong:{summary.get('accepted_delta_kind')}")
    if summary.get("acceptance_scope") != "policy-build target only":
        failures.append(f"decision_scope_wrong:{summary.get('acceptance_scope')}")
    for key in [
        "not_current_runtime_promotion",
        "not_current_regime_mutation",
        "requires_bounded_upgrade_policy_before_implementation",
    ]:
        if summary.get(key) is not True:
            failures.append(f"decision_summary_guard_missing:{key}:{summary.get(key)}")

    shape = human_decision_receipt.get("accepted_minimum_shape") or {}
    for key, expected in ACCEPTED_MINIMUM_SHAPE.items():
        if shape.get(key) is not expected:
            failures.append(f"accepted_shape_wrong:{key}:{shape.get(key)}")

    decision_guards = human_decision_receipt.get("authority_guards") or {}
    for key in [
        "delta_proposal_applied",
        "delta_proposal_promoted",
        "runner_executed",
        "runner_module_changed",
        "local_regime_replaced",
        "local_regime_runtime_mutated",
        "registry_written",
        "registry_sqlite_written",
        "global_taxonomy_claimed",
        "final_schema_claimed",
        "proof_claimed",
        "hidden_continuation_authorized",
    ]:
        if decision_guards.get(key) is not False:
            failures.append(f"decision_guard_not_false:{key}:{decision_guards.get(key)}")

    if delta.get("proposal_id") != DELTA_PROPOSAL_ID:
        failures.append(f"delta_proposal_id_wrong:{delta.get('proposal_id')}")
    if delta.get("proposal_class") != "PROPOSITION_SURFACE_DELTA_PROPOSAL":
        failures.append(f"delta_class_wrong:{delta.get('proposal_class')}")
    if delta.get("proposal_status") != "REVIEW_REQUIRED_NOT_APPLIED":
        failures.append(f"delta_status_wrong:{delta.get('proposal_status')}")
    if delta.get("terminal_effect") != "NONE":
        failures.append(f"delta_terminal_effect_wrong:{delta.get('terminal_effect')}")

    requested = delta.get("requested_delta") or {}
    if requested.get("delta_kind") != "ADD_REVIEWABLE_HALT_WITH_PROPOSAL_SURFACE":
        failures.append(f"requested_delta_kind_wrong:{requested.get('delta_kind')}")
    minimum = requested.get("minimum_shape") or {}
    for key, expected in ACCEPTED_MINIMUM_SHAPE.items():
        if minimum.get(key) is not expected:
            failures.append(f"requested_minimum_shape_wrong:{key}:{minimum.get(key)}")

    if delta_receipt.get("receipt_id") != DELTA_PROPOSAL_RECEIPT_ID:
        failures.append(f"delta_receipt_id_wrong:{delta_receipt.get('receipt_id')}")
    if delta_receipt.get("proposal_id") != DELTA_PROPOSAL_ID:
        failures.append(f"delta_receipt_proposal_id_wrong:{delta_receipt.get('proposal_id')}")
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

    if probe_run.get("receipt_id") != PROPOSITION_SURFACE_PROBE_RUN_RECEIPT_ID:
        failures.append(f"probe_run_receipt_id_wrong:{probe_run.get('receipt_id')}")
    if probe_run.get("gate") != "PASS":
        failures.append(f"probe_run_gate_not_PASS:{probe_run.get('gate')}")
    if probe_run.get("probe_result_class") != "PROPOSAL_SURFACE_ABSENT_REQUIRES_DELTA_PROPOSAL":
        failures.append(f"probe_result_class_wrong:{probe_run.get('probe_result_class')}")
    if probe_run.get("proposal_surface_absent") is not True:
        failures.append(f"probe_surface_absent_not_true:{probe_run.get('proposal_surface_absent')}")
    if probe_run.get("proposal_surface_present") is not False:
        failures.append(f"probe_surface_present_not_false:{probe_run.get('proposal_surface_present')}")

    metrics = probe_run.get("aggregate_metrics") or {}
    if metrics.get("runtime_proposal_emitted_count") != 0:
        failures.append(f"runtime_proposal_emitted_count_not_zero:{metrics.get('runtime_proposal_emitted_count')}")
    if metrics.get("reviewable_delta_proposal_artifact_count") != 1:
        failures.append(f"delta_artifact_count_wrong:{metrics.get('reviewable_delta_proposal_artifact_count')}")

    if probe_policy.get("policy_id") != PROPOSITION_SURFACE_PROBE_POLICY_ID:
        failures.append(f"probe_policy_id_wrong:{probe_policy.get('policy_id')}")
    if probe_policy_receipt.get("receipt_id") != PROPOSITION_SURFACE_PROBE_POLICY_RECEIPT_ID:
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

    if local_regime.get("local_regime_hash") != SOURCE_LOCAL_REGIME_HASH:
        failures.append(f"local_regime_hash_wrong:{local_regime.get('local_regime_hash')}")
    if local_regime.get("local_regime_version") != SOURCE_LOCAL_REGIME_VERSION:
        failures.append(f"local_regime_version_wrong:{local_regime.get('local_regime_version')}")

    for path, label in [
        (HUMAN_DECISION_PATH, "human_decision"),
        (HUMAN_DECISION_RECEIPT_PATH, "human_decision_receipt"),
        (DELTA_PROPOSAL_PATH, "delta_proposal"),
        (DELTA_PROPOSAL_RECEIPT_PATH, "delta_proposal_receipt"),
        (PROBE_RUN_RECEIPT_PATH, "proposition_surface_probe_run_receipt"),
        (PROBE_POLICY_PATH, "proposition_surface_probe_policy"),
        (PROBE_POLICY_RECEIPT_PATH, "proposition_surface_probe_policy_receipt"),
        (HALT_SURFACE_RUN_RECEIPT_PATH, "halt_surface_run_receipt"),
        (IMPLEMENTATION_RECEIPT_PATH, "implementation_receipt"),
        (LOCAL_REGIME_PATH, "local_regime"),
        (RUNNER_MODULE_PATH, "runner_module_v0_1"),
    ]:
        if not tracked(path):
            failures.append(f"required_artifact_not_tracked:{label}:{path.relative_to(ROOT).as_posix()}")

    return failures

def build_policy(write_outputs: bool = True) -> tuple[Dict[str, Any], Dict[str, Any]]:
    human_decision = read_json(HUMAN_DECISION_PATH)
    human_decision_receipt = read_json(HUMAN_DECISION_RECEIPT_PATH)
    delta = read_json(DELTA_PROPOSAL_PATH)
    delta_receipt = read_json(DELTA_PROPOSAL_RECEIPT_PATH)
    probe_run = read_json(PROBE_RUN_RECEIPT_PATH)
    probe_policy = read_json(PROBE_POLICY_PATH)
    probe_policy_receipt = read_json(PROBE_POLICY_RECEIPT_PATH)
    halt_surface = read_json(HALT_SURFACE_RUN_RECEIPT_PATH)
    implementation = read_json(IMPLEMENTATION_RECEIPT_PATH)
    local_regime = read_json(LOCAL_REGIME_PATH)

    failures = validate_inputs(
        human_decision,
        human_decision_receipt,
        delta,
        delta_receipt,
        probe_run,
        probe_policy,
        probe_policy_receipt,
        halt_surface,
        implementation,
        local_regime,
    )

    policy_seed = {
        "unit_id": UNIT_ID,
        "source_human_decision_id": HUMAN_DECISION_ID,
        "source_delta_proposal_id": DELTA_PROPOSAL_ID,
        "source_local_regime_hash": SOURCE_LOCAL_REGIME_HASH,
        "target_runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "target_local_regime_version": TARGET_LOCAL_REGIME_VERSION,
        "next_goal": NEXT_GOAL,
    }
    policy_id = sha8(policy_seed)

    local_regime_v1_required_delta = {
        "schema_version": "local_regime_v1_required_delta_policy_v0",
        "source_local_regime_version": SOURCE_LOCAL_REGIME_VERSION,
        "target_local_regime_version": TARGET_LOCAL_REGIME_VERSION,
        "source_local_regime_hash": SOURCE_LOCAL_REGIME_HASH,
        "delta_kind": "ADD_REVIEWABLE_HALT_WITH_PROPOSAL_SURFACE",
        "proposal_surface": {
            "enabled": True,
            "scope": "local only, bounded to jurisdiction_runner.v0.2 fixtures",
            "eligible_halts": [
                "STOP_NO_APPLICABLE_MOVE",
            ],
            "proposal_types": [
                "LOCAL_MOVE_ADMISSIBILITY_DELTA_PROPOSAL",
            ],
            "proposal_status_values": [
                "NONE",
                "EMITTED_REVIEW_REQUIRED",
                "WITHHELD_DUPLICATE_UNRESOLVED",
            ],
            "proposal_must_reference": [
                "source_halt_code",
                "source_state_id",
                "source_fixture_id",
                "evidence_summary",
                "proposed_delta_kind",
                "human_review_required",
            ],
            "no_proposal_reasons_preserved": [
                "INSUFFICIENT_EVIDENCE",
                "PRESSURE_ALREADY_TYPED",
                "OUT_OF_SCOPE",
            ],
        },
        "duplicate_unresolved_proposal_guard": {
            "enabled": True,
            "match_keys": [
                "proposal_type",
                "source_halt_code",
                "source_state_id",
                "proposed_delta_kind",
            ],
            "allowed_second_observation_results": [
                "WITHHELD_DUPLICATE_UNRESOLVED",
                "DUPLICATE_UNRESOLVED_PROPOSAL_COUNT_INCREMENTED",
            ],
        },
        "non_execution_contract": {
            "proposal_executed": False,
            "proposal_promoted": False,
            "local_regime_runtime_mutated": False,
            "registry_written": False,
            "hidden_continuation_authorized": False,
        },
    }

    runner_v0_2_required_delta = {
        "schema_version": "jurisdiction_runner_v0_2_required_delta_policy_v0",
        "source_runner_unit_id": SOURCE_RUNNER_UNIT_ID,
        "target_runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "implementation_mode": "separate_module_not_patch_v0_1",
        "required_runtime_behavior": {
            "preserve_v0_1_transcript_shape": True,
            "add_proposal_evaluation_after_no_applicable_move": True,
            "emit_proposal_receipt_when_evidence_sufficient": True,
            "withhold_proposal_when_evidence_insufficient": True,
            "link_or_count_duplicate_unresolved_proposal": True,
            "never_execute_or_apply_proposal": True,
            "terminal_remains_STOP": True,
            "next_command_goal_remains_null_without_later_human_decision": True,
        },
        "required_metrics": {
            "runtime_proposal_emitted_count": True,
            "runtime_proposal_executed_count": True,
            "runtime_proposal_promoted_count": True,
            "duplicate_unresolved_proposal_count": True,
            "proposal_withheld_count": True,
            "proposal_count_by_type": True,
            "halt_with_proposal_count": True,
            "halt_without_proposal_count": True,
            "proposal_receipt_count": True,
        },
    }

    authority_guards = {
        "upgrade_policy_built": True,
        "human_decision_consumed": True,
        "delta_proposal_consumed": True,
        "proposal_surface_upgrade_authorized_for_next_unit": True,
        "runner_module_read": True,
        "runner_module_changed": False,
        "runner_executed_by_policy": False,
        "local_regime_v0_read": True,
        "local_regime_v0_replaced": False,
        "local_regime_v1_declared_by_policy": False,
        "local_regime_runtime_mutated": False,
        "implementation_not_performed_by_policy": True,
        "proposal_promoted": False,
        "delta_proposal_applied": False,
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
        "schema_version": "jurisdiction_runner_v0_2_proposition_surface_upgrade_policy_v0",
        "policy_type": "JURISDICTION_RUNNER_V0_2_PROPOSITION_SURFACE_UPGRADE_POLICY",
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "policy_status": "POLICY_ONLY_NOT_IMPLEMENTED",
        "source_runner_unit_id": SOURCE_RUNNER_UNIT_ID,
        "target_runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "source_local_regime_version": SOURCE_LOCAL_REGIME_VERSION,
        "target_local_regime_version": TARGET_LOCAL_REGIME_VERSION,
        "source_local_regime_hash": SOURCE_LOCAL_REGIME_HASH,
        "source_human_decision_id": HUMAN_DECISION_ID,
        "source_human_decision_receipt_id": HUMAN_DECISION_RECEIPT_ID,
        "source_delta_proposal_id": DELTA_PROPOSAL_ID,
        "source_delta_proposal_receipt_id": DELTA_PROPOSAL_RECEIPT_ID,
        "source_proposition_surface_probe_run_receipt_id": PROPOSITION_SURFACE_PROBE_RUN_RECEIPT_ID,
        "source_halt_surface_probe_run_receipt_id": HALT_SURFACE_PROBE_RUN_RECEIPT_ID,
        "upgrade_summary": {
            "upgrade_reason": "v0.1 can halt but cannot lawfully halt-with-proposal through runtime behavior.",
            "human_decision": "accepted provisionally for policy build only",
            "target": "bounded local_regime.v1 plus jurisdiction_runner.v0.2",
            "non_goal": "global autonomy, final taxonomy, proof, registry promotion, or mutation of v0.1/v0",
        },
        "accepted_minimum_shape": ACCEPTED_MINIMUM_SHAPE,
        "local_regime_v1_required_delta": local_regime_v1_required_delta,
        "runner_v0_2_required_delta": runner_v0_2_required_delta,
        "required_implementation_artifacts": REQUIRED_IMPLEMENTATION_ARTIFACTS,
        "required_fixture_cases": REQUIRED_FIXTURE_CASES,
        "acceptance_gates": V0_2_ACCEPTANCE_GATES,
        "authorized_operations_next": {
            "read_upgrade_policy": True,
            "read_upgrade_policy_receipt": True,
            "read_human_decision": True,
            "read_delta_proposal": True,
            "read_delta_proposal_receipt": True,
            "read_source_local_regime_v0": True,
            "read_source_runner_v0_1": True,
            "write_local_regime_v1_declaration": True,
            "write_runner_v0_2_module": True,
            "write_v0_2_upgrade_fixtures": True,
            "write_v0_2_expected_transcripts": True,
            "execute_runner_v0_2_against_fixtures": True,
            "emit_v0_2_case_receipts": True,
            "emit_v0_2_proposal_receipts": True,
            "emit_v0_2_implementation_receipt": True,
        },
        "forbidden_operations_next": {
            "modify_runner_v0_1_module": True,
            "replace_local_regime_v0": True,
            "mutate_local_regime_at_runtime": True,
            "execute_or_apply_proposal": True,
            "promote_proposal_without_human_review": True,
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
            "does_not_declare_local_regime_v1": True,
            "does_not_apply_delta": True,
            "does_not_promote_delta": True,
            "does_not_mutate_local_regime": True,
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
        "policy_id": policy_id,
        "unit_id": UNIT_ID,
        "source_human_decision_id": HUMAN_DECISION_ID,
        "target_runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "target_local_regime_version": TARGET_LOCAL_REGIME_VERSION,
        "terminal": policy["terminal"],
    }
    receipt_id = sha8(receipt_seed)
    policy["policy_receipt_id"] = receipt_id

    receipt = {
        "schema_version": "jurisdiction_runner_v0_2_proposition_surface_upgrade_policy_receipt_v0",
        "receipt_type": "JURISDICTION_RUNNER_V0_2_PROPOSITION_SURFACE_UPGRADE_POLICY_RECEIPT",
        "unit_id": UNIT_ID,
        "receipt_id": receipt_id,
        "policy_id": policy_id,
        "policy_status": policy["policy_status"],
        "source_runner_unit_id": SOURCE_RUNNER_UNIT_ID,
        "target_runner_unit_id": TARGET_RUNNER_UNIT_ID,
        "source_local_regime_version": SOURCE_LOCAL_REGIME_VERSION,
        "target_local_regime_version": TARGET_LOCAL_REGIME_VERSION,
        "source_local_regime_hash": SOURCE_LOCAL_REGIME_HASH,
        "source_human_decision_id": HUMAN_DECISION_ID,
        "source_human_decision_receipt_id": HUMAN_DECISION_RECEIPT_ID,
        "source_delta_proposal_id": DELTA_PROPOSAL_ID,
        "source_delta_proposal_receipt_id": DELTA_PROPOSAL_RECEIPT_ID,
        "upgrade_summary": policy["upgrade_summary"],
        "accepted_minimum_shape": policy["accepted_minimum_shape"],
        "local_regime_v1_required_delta": policy["local_regime_v1_required_delta"],
        "runner_v0_2_required_delta": policy["runner_v0_2_required_delta"],
        "required_implementation_artifacts": policy["required_implementation_artifacts"],
        "required_fixture_cases": policy["required_fixture_cases"],
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
    print(f"upgrade_policy_id={policy['policy_id']}")
    print(f"upgrade_policy_receipt_id={receipt['receipt_id']}")
    print(f"upgrade_policy_path=data/jurisdiction_runner_v0_2_proposition_surface_upgrade_policies/{policy['policy_id']}.json")
    print(f"upgrade_policy_receipt_path=data/jurisdiction_runner_v0_2_proposition_surface_upgrade_policy_receipts/{policy['policy_id']}.json")
    return 0 if receipt["gate"] == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
