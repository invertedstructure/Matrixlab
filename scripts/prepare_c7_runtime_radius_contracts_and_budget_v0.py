#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_C7_RUNTIME_RADIUS_CONTRACTS_AND_BUDGET_V0"
TARGET_UNIT_ID = "runtime.practical_radius_expansion.contracts_and_budget.v0"
NEXT_UNIT_ID = "BUILD_C7_SYNTHETIC_RUNTIME_RADIUS_FIXTURES_V0"

LAYER = "RUNTIME / C7 / CONTRACTS"
MODE = "DEFINE_CONTRACTS / FREEZE_BUDGET / NO_RUNTIME_RUN"
BUILD_MODE = "C7_RUNTIME_RADIUS_CONTRACTS_AND_BUDGET_ONLY"

SOURCE_C7_READINESS_RECEIPT_ID = "49b3f28b"

C7_READINESS_RECEIPT_PATH = ROOT / "data/c7_practical_runtime_radius_readiness_v0_receipts/49b3f28b.json"
C7_CONTRACT_TARGETS_PATH = ROOT / "data/c7_practical_runtime_radius_readiness_v0/c7_contract_targets_v0.json"
C7_MISSING_SURFACES_PATH = ROOT / "data/c7_practical_runtime_radius_readiness_v0/c7_missing_or_weak_surfaces_v0.json"
C7_NEGATIVE_COUNTER_TARGETS_PATH = ROOT / "data/c7_practical_runtime_radius_readiness_v0/c7_negative_counter_targets_v0.json"
C7_SEQUENCE_PLAN_PATH = ROOT / "data/c7_practical_runtime_radius_readiness_v0/c7_sequence_to_test_runs_v0.json"
C7_TEST_FIXTURE_PLAN_PATH = ROOT / "data/c7_practical_runtime_radius_readiness_v0/c7_test_fixture_plan_v0.json"
C7_SURFACE_INVENTORY_PATH = ROOT / "data/c7_practical_runtime_radius_readiness_v0/c7_required_surface_inventory_v0.json"
C7_READINESS_ROLLUP_PATH = ROOT / "data/c7_practical_runtime_radius_readiness_v0/c7_readiness_audit_rollup_v0.json"

OUT_DIR = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0"
RECEIPT_DIR = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0_receipts"

BASIS_PATH = OUT_DIR / "c7_contracts_and_budget_basis_v0.json"
STEP_PACKET_CONTRACT_PATH = OUT_DIR / "runtime_step_packet_contract_v0.json"
STOP_PACKET_CONTRACT_PATH = OUT_DIR / "runtime_radius_stop_packet_contract_v0.json"
BUDGET_PATH = OUT_DIR / "runtime_radius_budget_v0.json"
UNIT_FEEDBACK_CONTRACT_PATH = OUT_DIR / "unit_feedback_record_contract_v0.json"
NEGATIVE_COUNTER_CONTRACT_PATH = OUT_DIR / "runtime_radius_negative_counter_contract_v0.json"
ROLLUP_CONTRACT_PATH = OUT_DIR / "runtime_radius_rollup_contract_v0.json"
READOUT_CONTRACT_PATH = OUT_DIR / "runtime_radius_readout_contract_v0.json"
CONTRACT_INDEX_PATH = OUT_DIR / "c7_contract_index_v0.json"
FIXTURE_BUILD_TARGET_PATH = OUT_DIR / "c7_fixture_build_target_v0.json"
ROLLUP_PATH = OUT_DIR / "c7_contracts_and_budget_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c7_contracts_and_budget_profile_v0.json"
TRACE_PATH = OUT_DIR / "c7_contracts_and_budget_transition_trace.json"

EXPECTED_READINESS_STATUS = "TYPED_C7_READINESS_AUDIT_DONE_CONTRACTS_AND_BUDGET_NEXT"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def require_false(obj: Dict[str, Any], key: str, failures: List[str]) -> None:
    if obj.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{obj.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        C7_READINESS_RECEIPT_PATH,
        C7_CONTRACT_TARGETS_PATH,
        C7_MISSING_SURFACES_PATH,
        C7_NEGATIVE_COUNTER_TARGETS_PATH,
        C7_SEQUENCE_PLAN_PATH,
        C7_TEST_FIXTURE_PLAN_PATH,
        C7_SURFACE_INVENTORY_PATH,
        C7_READINESS_ROLLUP_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    readiness_receipt = read_json(C7_READINESS_RECEIPT_PATH)
    contract_targets_src = read_json(C7_CONTRACT_TARGETS_PATH)
    missing_surfaces_src = read_json(C7_MISSING_SURFACES_PATH)
    negative_counter_targets_src = read_json(C7_NEGATIVE_COUNTER_TARGETS_PATH)
    sequence_plan_src = read_json(C7_SEQUENCE_PLAN_PATH)
    test_fixture_plan_src = read_json(C7_TEST_FIXTURE_PLAN_PATH)
    surface_inventory_src = read_json(C7_SURFACE_INVENTORY_PATH)
    readiness_rollup_src = read_json(C7_READINESS_ROLLUP_PATH)

    readiness_summary = readiness_receipt.get("machine_readable_c7_readiness_audit_summary", {})

    if readiness_receipt.get("receipt_id") != SOURCE_C7_READINESS_RECEIPT_ID:
        failures.append(f"readiness_receipt_id_wrong:{readiness_receipt.get('receipt_id')}")
    if readiness_receipt.get("gate") != "PASS":
        failures.append(f"readiness_gate_wrong:{readiness_receipt.get('gate')}")
    if readiness_summary.get("status") != EXPECTED_READINESS_STATUS:
        failures.append(f"readiness_status_wrong:{readiness_summary.get('status')}")
    if readiness_summary.get("next_unit_id") != UNIT_ID:
        failures.append(f"readiness_next_unit_wrong:{readiness_summary.get('next_unit_id')}")
    if readiness_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("readiness_terminal_not_advance")
    if readiness_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("readiness_terminal_next_wrong")
    if readiness_summary.get("ready_for_contract_preparation") is not True:
        failures.append("readiness_not_ready_for_contract_preparation")
    if readiness_summary.get("ready_for_c7_test_run") is not False:
        failures.append("readiness_should_not_be_ready_for_test_run_yet")
    if readiness_summary.get("cell0_lawful_admissibility_surface_present_as_role") is not True:
        failures.append("cell0_admissibility_role_missing")

    for key in [
        "c7_runtime_run_authorized",
        "runtime_adoption_authorized",
        "live_runtime_hooks_installed",
        "runtime_patched",
        "runtime_routing_installed",
        "validation_verdict_emitted",
        "admissibility_checked",
        "authorization_verdict_emitted",
        "execution_claimed",
        "schema_archive_mutated",
        "schema_created",
        "control_path_blocked",
        "control_path_advanced",
        "hidden_next_command",
    ]:
        require_false(readiness_summary, key, failures)

    expected_contracts = {
        "runtime_step_packet_contract_v0",
        "runtime_radius_stop_packet_contract_v0",
        "runtime_radius_budget_v0",
        "unit_feedback_record_contract_v0",
        "runtime_radius_negative_counter_contract_v0",
        "runtime_radius_rollup_contract_v0",
        "runtime_radius_readout_contract_v0",
    }
    actual_contracts = set(contract_targets_src.get("contracts_to_prepare_next", []))
    missing_contract_targets = sorted(expected_contracts - actual_contracts)
    if missing_contract_targets:
        failures.append("contract_targets_missing:" + ",".join(missing_contract_targets))

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C7_RUNTIME_RADIUS_CONTRACTS_AND_BUDGET_PREPARED_FIXTURES_NEXT" if gate == "PASS" else "TYPED_C7_RUNTIME_RADIUS_CONTRACTS_AND_BUDGET_GATE_FAIL"

    source_hash_manifest = {rel(p): file_sha256(p) for p in required}

    step_packet_contract = {
        "schema_version": "runtime_step_packet_contract_v0",
        "contract_status": "FROZEN" if gate == "PASS" else "NOT_FROZEN",
        "purpose": "Packetize every C7 runtime-radius transition; no inferred next command.",
        "required_fields": [
            "schema_version",
            "step_id",
            "run_id",
            "step_index",
            "input_packet_ref",
            "active_object",
            "attempted_move",
            "schema_validation_ref",
            "admissibility_ref",
            "execution_ref",
            "receipt_ref",
            "sidecar_event_ref",
            "edge_observation_ref",
            "unit_feedback_ref",
            "terminal",
            "next_packet_ref",
            "bad_counters",
        ],
        "terminal_values": [
            "ADVANCE",
            "STOP",
        ],
        "bad_counter_contract_ref": rel(NEGATIVE_COUNTER_CONTRACT_PATH),
        "must_not_infer": [
            "next packet from prose",
            "authority from previous acceptance",
            "runtime adoption from reference freeze",
            "success from step count alone",
        ],
    }

    stop_packet_contract = {
        "schema_version": "runtime_radius_stop_packet_contract_v0",
        "contract_status": "FROZEN" if gate == "PASS" else "NOT_FROZEN",
        "purpose": "Make C7 halts useful and typed.",
        "required_fields": [
            "schema_version",
            "run_id",
            "stop_step_index",
            "stop_code",
            "stop_reason",
            "last_valid_packet_ref",
            "blocked_packet_ref",
            "blocked_move",
            "blocked_by",
            "lawful_next_handling",
            "must_not_infer",
            "terminal",
        ],
        "allowed_stop_codes": [
            "STOP_SCHEMA_GAP",
            "STOP_AUTHORITY_REQUIRED",
            "STOP_FRONTIER_REQUIRED",
            "STOP_MISSING_CAPABILITY",
            "STOP_WEAK_FEEDBACK",
            "STOP_OBSERVABILITY_GAP",
            "STOP_INTER_CELL_PROTOCOL_GAP",
            "STOP_UNTYPED_FAILURE",
            "STOP_BUDGET_EXHAUSTED",
            "STOP_DONE",
        ],
        "terminal_values": [
            "STOP",
            "STOP_DONE",
        ],
    }

    budget = {
        "schema_version": "runtime_radius_budget_v0",
        "budget_status": "FROZEN" if gate == "PASS" else "NOT_FROZEN",
        "max_steps": 25,
        "max_cell1_builds": 2,
        "max_domain_surfaces": 1,
        "max_schema_gap_halts": 3,
        "max_authority_halts": 3,
        "stop_on_first_untyped_failure": True,
        "stop_on_hidden_continuation": True,
        "stop_on_sidecar_failure_if_claim_requires_observability": True,
        "stop_on_schema_invalid_advance": True,
        "stop_on_admissibility_denied_execution": True,
        "budget_law": "C7 radius expansion is bounded practical continuation, not keep-going momentum.",
    }

    unit_feedback_contract = {
        "schema_version": "unit_feedback_record_contract_v0",
        "contract_status": "FROZEN" if gate == "PASS" else "NOT_FROZEN",
        "purpose": "Turn failed or halted units into diagnostic feedback instead of bare status.",
        "required_fields": [
            "schema_version",
            "unit_feedback_id",
            "run_id",
            "step_id",
            "failure_kind",
            "failed_boundary",
            "blocked_move",
            "active_object_ref",
            "missing_object_or_capability",
            "observed_evidence_ref",
            "lawful_next_handling",
            "diagnostic_quality",
            "must_not_infer",
        ],
        "failure_kinds": [
            "SCHEMA_GAP",
            "AUTHORITY_BOUNDARY",
            "FRONTIER_REQUIRED",
            "MISSING_CAPABILITY",
            "WEAK_FEEDBACK",
            "OBSERVABILITY_GAP",
            "INTER_CELL_PROTOCOL_GAP",
            "UNTYPED_FAILURE",
        ],
        "diagnostic_quality_values": [
            "USEFUL",
            "PARTIAL",
            "WEAK",
            "UNTYPED",
        ],
    }

    negative_counter_contract = {
        "schema_version": "runtime_radius_negative_counter_contract_v0",
        "contract_status": "FROZEN" if gate == "PASS" else "NOT_FROZEN",
        "must_be_zero": negative_counter_targets_src.get("must_be_zero", []),
        "critical_must_be_zero": negative_counter_targets_src.get("critical", []),
        "counter_law": "Any nonzero critical counter blocks C7 success classification.",
    }

    rollup_contract = {
        "schema_version": "runtime_radius_rollup_contract_v0",
        "contract_status": "FROZEN" if gate == "PASS" else "NOT_FROZEN",
        "required_fields": [
            "schema_version",
            "run_id",
            "steps_attempted",
            "steps_advanced",
            "steps_halted",
            "lawful_continuation_depth",
            "max_contiguous_valid_steps",
            "schema_validation",
            "cell0_admissibility",
            "halts",
            "observability",
            "bad_counters",
            "outcome",
        ],
        "allowed_outcomes": [
            "RADIUS_EXPANDED_CLEANLY",
            "RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES",
            "RADIUS_BLOCKED_BY_SCHEMA_GAP",
            "RADIUS_BLOCKED_BY_AUTHORITY_BOUNDARY",
            "RADIUS_BLOCKED_BY_MISSING_CAPABILITY",
            "RADIUS_BLOCKED_BY_WEAK_FEEDBACK",
            "RADIUS_BLOCKED_BY_OBSERVABILITY_GAP",
            "RADIUS_BLOCKED_BY_INTER_CELL_PROTOCOL_GAP",
            "RADIUS_REJECTED_UNLAWFUL_CONTINUATION",
            "RADIUS_FAIL_UNTYPED",
        ],
        "success_law": "Radius improvement is not inferred from step count alone.",
    }

    readout_contract = {
        "schema_version": "runtime_radius_readout_contract_v0",
        "contract_status": "FROZEN" if gate == "PASS" else "NOT_FROZEN",
        "human_readout_fields": [
            "steps_attempted",
            "steps_advanced",
            "typed_halts",
            "untyped_halts",
            "longest_lawful_continuation",
            "halt_reasons",
            "receipts_emitted",
            "edge_observations",
            "unit_feedback_records",
            "sidecar_events",
            "bad_counters",
            "interpretation",
        ],
        "readout_law": "Human readout must separate lawful continuation from productive pressure and raw length.",
    }

    basis = {
        "schema_version": "c7_contracts_and_budget_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_c7_readiness_receipt_id": SOURCE_C7_READINESS_RECEIPT_ID,
        "source_files": source_hash_manifest,
        "basis_claim": "C7 readiness audit passed and named contracts/budget as the next typed unit.",
        "cell0_law": "Cell 0 is the lawful admissibility surface; no duplicate Lawful Admissibility Cell is introduced.",
        "does_not_authorize": [
            "C7 runtime run",
            "runtime adoption",
            "runtime patching",
            "live hooks",
            "runtime routing",
            "schema mutation",
            "control path authority",
        ],
    }

    contract_index = {
        "schema_version": "c7_contract_index_v0",
        "index_status": "EMITTED" if gate == "PASS" else "NOT_EMITTED",
        "contracts": [
            {"name": "runtime_step_packet_contract_v0", "path": rel(STEP_PACKET_CONTRACT_PATH)},
            {"name": "runtime_radius_stop_packet_contract_v0", "path": rel(STOP_PACKET_CONTRACT_PATH)},
            {"name": "runtime_radius_budget_v0", "path": rel(BUDGET_PATH)},
            {"name": "unit_feedback_record_contract_v0", "path": rel(UNIT_FEEDBACK_CONTRACT_PATH)},
            {"name": "runtime_radius_negative_counter_contract_v0", "path": rel(NEGATIVE_COUNTER_CONTRACT_PATH)},
            {"name": "runtime_radius_rollup_contract_v0", "path": rel(ROLLUP_CONTRACT_PATH)},
            {"name": "runtime_radius_readout_contract_v0", "path": rel(READOUT_CONTRACT_PATH)},
        ],
    }

    fixture_build_target = {
        "schema_version": "c7_fixture_build_target_v0",
        "target_status": "FIXTURES_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "fixture_sequences_to_build": test_fixture_plan_src.get("fixtures_to_build_after_contracts", []),
        "contract_inputs": contract_index["contracts"],
        "fixture_boundary": "build fixtures only; no C7 runtime run yet",
    }

    rollup = {
        "schema_version": "c7_contracts_and_budget_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "source_c7_readiness_receipt_id": SOURCE_C7_READINESS_RECEIPT_ID,
        "contracts_prepared": gate == "PASS",
        "contract_count": len(contract_index["contracts"]) if gate == "PASS" else 0,
        "budget_prepared": gate == "PASS",
        "negative_counter_count": len(negative_counter_contract["must_be_zero"]) if gate == "PASS" else 0,
        "critical_negative_counter_count": len(negative_counter_contract["critical_must_be_zero"]) if gate == "PASS" else 0,
        "ready_for_fixture_build": gate == "PASS",
        "ready_for_c7_test_run": False,
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "c7_runtime_run_authorized": False,
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "control_path_authority_granted": False,
        "hidden_next_command": False,
    }

    profile = {
        "schema_version": "c7_contracts_and_budget_profile_v0",
        "profile_status": status,
        "profile": "C7_RUNTIME_RADIUS_CONTRACTS_AND_BUDGET",
        "what_changed": "C7 packet, stop, budget, feedback, negative counter, rollup, and readout contracts were prepared.",
        "what_did_not_change": [
            "C7 runtime test has not run",
            "runtime adoption is not authorized",
            "runtime is not patched",
            "live hooks are not installed",
            "schema archive is not mutated",
            "control path authority is not granted",
        ],
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_C7_RUNTIME_RADIUS_CONTRACTS_AND_BUDGET_V0",
        "next_command_goal": None,
    }

    trace = {
        "schema_version": "c7_contracts_and_budget_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "C7_READINESS_AUDIT_DONE_CONTRACTS_AND_BUDGET_NEXT",
                "edge": "consume readiness audit",
                "to": "C7_CONTRACTS_BASIS_ACCEPTED" if gate == "PASS" else "C7_CONTRACTS_BASIS_FAIL",
            },
            {
                "from": "C7_CONTRACTS_BASIS_ACCEPTED" if gate == "PASS" else "C7_CONTRACTS_BASIS_FAIL",
                "edge": "prepare runtime-radius contracts and budget",
                "to": "C7_FIXTURES_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C7_CONTRACTS_AND_BUDGET_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (STEP_PACKET_CONTRACT_PATH, step_packet_contract),
        (STOP_PACKET_CONTRACT_PATH, stop_packet_contract),
        (BUDGET_PATH, budget),
        (UNIT_FEEDBACK_CONTRACT_PATH, unit_feedback_contract),
        (NEGATIVE_COUNTER_CONTRACT_PATH, negative_counter_contract),
        (ROLLUP_CONTRACT_PATH, rollup_contract),
        (READOUT_CONTRACT_PATH, readout_contract),
        (CONTRACT_INDEX_PATH, contract_index),
        (FIXTURE_BUILD_TARGET_PATH, fixture_build_target),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_PATH, trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "C7_RUNTIME_RADIUS_CONTRACTS_AND_BUDGET_PREPARED",
        "READINESS_AUDIT_RECEIPT_CONSUMED",
        "CELL0_LAWFUL_ADMISSIBILITY_SURFACE_PRESERVED_AS_CELL0",
        "RUNTIME_STEP_PACKET_CONTRACT_PREPARED",
        "RUNTIME_RADIUS_STOP_PACKET_CONTRACT_PREPARED",
        "RUNTIME_RADIUS_BUDGET_PREPARED",
        "UNIT_FEEDBACK_RECORD_CONTRACT_PREPARED",
        "NEGATIVE_COUNTER_CONTRACT_PREPARED",
        "ROLLUP_AND_READOUT_CONTRACTS_PREPARED",
        "FIXTURES_ARE_NEXT_TYPED_UNIT",
        "NO_C7_RUNTIME_RUN",
        "NO_RUNTIME_ADOPTION",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_HOOK_INSTALL",
        "NO_SCHEMA_MUTATION",
        "NO_CONTROL_PATH_AUTHORITY",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt_body = {
        "schema_version": "c7_contracts_and_budget_receipt_v0",
        "receipt_type": "TYPED_C7_RUNTIME_RADIUS_CONTRACTS_AND_BUDGET_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "source_c7_readiness_receipt_id": SOURCE_C7_READINESS_RECEIPT_ID,
        "acceptance_gate_results": {
            "C7_CONTRACTS_0_READINESS_RECEIPT_CONSUMED": gate == "PASS",
            "C7_CONTRACTS_1_STEP_PACKET_CONTRACT_PREPARED": gate == "PASS",
            "C7_CONTRACTS_2_STOP_PACKET_CONTRACT_PREPARED": gate == "PASS",
            "C7_CONTRACTS_3_BUDGET_PREPARED": gate == "PASS",
            "C7_CONTRACTS_4_UNIT_FEEDBACK_CONTRACT_PREPARED": gate == "PASS",
            "C7_CONTRACTS_5_NEGATIVE_COUNTER_CONTRACT_PREPARED": gate == "PASS",
            "C7_CONTRACTS_6_ROLLUP_READOUT_CONTRACTS_PREPARED": gate == "PASS",
            "C7_CONTRACTS_7_FIXTURES_NEXT": gate == "PASS",
            "C7_CONTRACTS_8_NO_RUNTIME_RUN": gate == "PASS",
            "C7_CONTRACTS_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_c7_contracts_and_budget_summary": {
            "status": status,
            "c7_contracts_and_budget_prepared": gate == "PASS",
            "source_c7_readiness_receipt_consumed": gate == "PASS",
            "cell0_lawful_admissibility_surface_preserved_as_cell0": gate == "PASS",
            "contract_count": rollup["contract_count"],
            "budget_prepared": gate == "PASS",
            "negative_counter_count": rollup["negative_counter_count"],
            "critical_negative_counter_count": rollup["critical_negative_counter_count"],
            "ready_for_fixture_build": gate == "PASS",
            "ready_for_c7_test_run": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "c7_runtime_run_authorized": False,
            "runtime_adoption_authorized": False,
            "live_runtime_hooks_installed": False,
            "runtime_patched": False,
            "runtime_routing_installed": False,
            "validation_verdict_emitted": False,
            "admissibility_checked": False,
            "authorization_verdict_emitted": False,
            "execution_claimed": False,
            "schema_archive_mutated": False,
            "schema_created": False,
            "control_path_blocked": False,
            "control_path_advanced": False,
            "hidden_next_command": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "step_packet_contract": rel(STEP_PACKET_CONTRACT_PATH),
            "stop_packet_contract": rel(STOP_PACKET_CONTRACT_PATH),
            "budget": rel(BUDGET_PATH),
            "unit_feedback_contract": rel(UNIT_FEEDBACK_CONTRACT_PATH),
            "negative_counter_contract": rel(NEGATIVE_COUNTER_CONTRACT_PATH),
            "rollup_contract": rel(ROLLUP_CONTRACT_PATH),
            "readout_contract": rel(READOUT_CONTRACT_PATH),
            "contract_index": rel(CONTRACT_INDEX_PATH),
            "fixture_build_target": rel(FIXTURE_BUILD_TARGET_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C7_CONTRACTS_AND_BUDGET_GATE_FAIL",
        },
    }

    receipt_id = sig8(receipt_body)
    receipt_body["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_body["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_body)

    print(json.dumps(receipt_body, indent=2, sort_keys=True))
    print(f"c7_contracts_and_budget_receipt_id={receipt_id}")
    print(f"c7_contracts_and_budget_receipt_path={rel(receipt_path)}")
    print(f"c7_contracts_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
