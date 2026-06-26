#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_C7_SYNTHETIC_RUNTIME_RADIUS_FIXTURES_V0"
TARGET_UNIT_ID = "runtime.practical_radius_expansion.synthetic_fixtures.v0"
NEXT_UNIT_ID = "BUILD_C7_SYNTHETIC_RUNTIME_RADIUS_RUNNER_V0"

LAYER = "RUNTIME / C7 / FIXTURES"
MODE = "BUILD_FIXTURES / NO_RUNTIME_RUN / NO_RUNTIME_ADOPTION"
BUILD_MODE = "C7_SYNTHETIC_RUNTIME_RADIUS_FIXTURES_ONLY"

SOURCE_C7_CONTRACTS_RECEIPT_ID = "2c5d3c62"

C7_CONTRACTS_RECEIPT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0_receipts/2c5d3c62.json"
C7_CONTRACT_INDEX_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/c7_contract_index_v0.json"
C7_FIXTURE_BUILD_TARGET_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/c7_fixture_build_target_v0.json"
STEP_PACKET_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_step_packet_contract_v0.json"
STOP_PACKET_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_stop_packet_contract_v0.json"
BUDGET_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_budget_v0.json"
UNIT_FEEDBACK_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/unit_feedback_record_contract_v0.json"
NEGATIVE_COUNTER_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_negative_counter_contract_v0.json"
ROLLUP_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_rollup_contract_v0.json"
READOUT_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_readout_contract_v0.json"

OUT_DIR = ROOT / "data/c7_synthetic_runtime_radius_fixtures_v0"
RECEIPT_DIR = ROOT / "data/c7_synthetic_runtime_radius_fixtures_v0_receipts"

BASIS_PATH = OUT_DIR / "c7_synthetic_fixture_build_basis_v0.json"
FIXTURE_INDEX_PATH = OUT_DIR / "c7_synthetic_fixture_index_v0.json"
EXPECTED_OUTCOMES_PATH = OUT_DIR / "c7_synthetic_fixture_expected_outcomes_v0.json"
VALIDATION_REPORT_PATH = OUT_DIR / "c7_synthetic_fixture_validation_report_v0.json"
RUNNER_BUILD_TARGET_PATH = OUT_DIR / "c7_synthetic_runner_build_target_v0.json"
ROLLUP_PATH = OUT_DIR / "c7_synthetic_fixture_build_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c7_synthetic_fixture_build_profile_v0.json"
TRACE_PATH = OUT_DIR / "c7_synthetic_fixture_build_transition_trace.json"

FIXTURE_DIR = OUT_DIR / "fixtures"

EXPECTED_CONTRACTS_STATUS = "TYPED_C7_RUNTIME_RADIUS_CONTRACTS_AND_BUDGET_PREPARED_FIXTURES_NEXT"

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

def make_zero_counters(counter_names: List[str]) -> Dict[str, int]:
    return {name: 0 for name in counter_names}

def step_packet(
    *,
    fixture_id: str,
    run_id: str,
    step_index: int,
    active_object: str,
    attempted_move: str,
    schema_result: str,
    cell0_result: str,
    execution_result: str | None,
    terminal: str,
    next_packet_ref: str | None,
    counter_names: List[str],
    feedback_ref: str | None = None,
) -> Dict[str, Any]:
    step_id = f"{fixture_id}__step_{step_index}"
    return {
        "schema_version": "runtime_step_packet_v0",
        "step_id": step_id,
        "run_id": run_id,
        "step_index": step_index,
        "input_packet_ref": f"{fixture_id}__input_packet_{step_index}",
        "active_object": active_object,
        "attempted_move": attempted_move,
        "schema_validation_ref": f"{fixture_id}__schema_validation_{step_index}__{schema_result}",
        "admissibility_ref": f"{fixture_id}__cell0_admissibility_{step_index}__{cell0_result}",
        "execution_ref": None if execution_result is None else f"{fixture_id}__execution_{step_index}__{execution_result}",
        "receipt_ref": f"{fixture_id}__receipt_{step_index}",
        "sidecar_event_ref": f"{fixture_id}__sidecar_event_{step_index}",
        "edge_observation_ref": f"{fixture_id}__edge_observation_{step_index}",
        "unit_feedback_ref": feedback_ref,
        "terminal": terminal,
        "next_packet_ref": next_packet_ref,
        "bad_counters": make_zero_counters(counter_names),
    }

def stop_packet(
    *,
    fixture_id: str,
    run_id: str,
    stop_step_index: int,
    stop_code: str,
    stop_reason: str,
    last_valid_packet_ref: str | None,
    blocked_packet_ref: str | None,
    blocked_move: str | None,
    blocked_by: str,
    lawful_next_handling: List[str],
) -> Dict[str, Any]:
    return {
        "schema_version": "runtime_radius_stop_packet_v0",
        "run_id": run_id,
        "stop_step_index": stop_step_index,
        "stop_code": stop_code,
        "stop_reason": stop_reason,
        "last_valid_packet_ref": last_valid_packet_ref,
        "blocked_packet_ref": blocked_packet_ref,
        "blocked_move": blocked_move,
        "blocked_by": blocked_by,
        "lawful_next_handling": lawful_next_handling,
        "must_not_infer": [
            "runtime failed globally",
            "authority granted",
            "hidden next command exists",
            "step count equals success",
        ],
        "terminal": "STOP_DONE" if stop_code == "STOP_DONE" else "STOP",
    }

def feedback_record(
    *,
    fixture_id: str,
    run_id: str,
    step_id: str,
    failure_kind: str,
    failed_boundary: str,
    blocked_move: str | None,
    missing_object_or_capability: str | None,
    lawful_next_handling: List[str],
    diagnostic_quality: str,
) -> Dict[str, Any]:
    return {
        "schema_version": "unit_feedback_record_v0",
        "unit_feedback_id": f"{fixture_id}__feedback_{sig8([fixture_id, step_id, failure_kind])}",
        "run_id": run_id,
        "step_id": step_id,
        "failure_kind": failure_kind,
        "failed_boundary": failed_boundary,
        "blocked_move": blocked_move,
        "active_object_ref": f"{fixture_id}__active_object",
        "missing_object_or_capability": missing_object_or_capability,
        "observed_evidence_ref": f"{fixture_id}__evidence_{step_id}",
        "lawful_next_handling": lawful_next_handling,
        "diagnostic_quality": diagnostic_quality,
        "must_not_infer": [
            "global runtime failure",
            "authority granted",
            "hidden next command",
        ],
    }

def fixture(
    *,
    fixture_id: str,
    title: str,
    expected_outcome: str,
    purpose: str,
    steps: List[Dict[str, Any]],
    stop: Dict[str, Any],
    feedback_records: List[Dict[str, Any]],
    notes: List[str],
) -> Dict[str, Any]:
    return {
        "schema_version": "c7_synthetic_runtime_radius_fixture_v0",
        "fixture_id": fixture_id,
        "title": title,
        "purpose": purpose,
        "expected_outcome": expected_outcome,
        "runtime_adoption_authorized": False,
        "c7_runtime_run_authorized": False,
        "synthetic_fixture_only": True,
        "steps": steps,
        "stop_packet": stop,
        "unit_feedback_records": feedback_records,
        "notes": notes,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURE_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        C7_CONTRACTS_RECEIPT_PATH,
        C7_CONTRACT_INDEX_PATH,
        C7_FIXTURE_BUILD_TARGET_PATH,
        STEP_PACKET_CONTRACT_PATH,
        STOP_PACKET_CONTRACT_PATH,
        BUDGET_PATH,
        UNIT_FEEDBACK_CONTRACT_PATH,
        NEGATIVE_COUNTER_CONTRACT_PATH,
        ROLLUP_CONTRACT_PATH,
        READOUT_CONTRACT_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    contracts_receipt = read_json(C7_CONTRACTS_RECEIPT_PATH)
    contract_index = read_json(C7_CONTRACT_INDEX_PATH)
    fixture_build_target = read_json(C7_FIXTURE_BUILD_TARGET_PATH)
    step_contract = read_json(STEP_PACKET_CONTRACT_PATH)
    stop_contract = read_json(STOP_PACKET_CONTRACT_PATH)
    budget = read_json(BUDGET_PATH)
    unit_feedback_contract = read_json(UNIT_FEEDBACK_CONTRACT_PATH)
    negative_counter_contract = read_json(NEGATIVE_COUNTER_CONTRACT_PATH)
    rollup_contract = read_json(ROLLUP_CONTRACT_PATH)
    readout_contract = read_json(READOUT_CONTRACT_PATH)

    summary = contracts_receipt.get("machine_readable_c7_contracts_and_budget_summary", {})

    if contracts_receipt.get("receipt_id") != SOURCE_C7_CONTRACTS_RECEIPT_ID:
        failures.append(f"contracts_receipt_id_wrong:{contracts_receipt.get('receipt_id')}")
    if contracts_receipt.get("gate") != "PASS":
        failures.append(f"contracts_gate_wrong:{contracts_receipt.get('gate')}")
    if summary.get("status") != EXPECTED_CONTRACTS_STATUS:
        failures.append(f"contracts_status_wrong:{summary.get('status')}")
    if summary.get("next_unit_id") != UNIT_ID:
        failures.append(f"contracts_next_unit_wrong:{summary.get('next_unit_id')}")
    if contracts_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("contracts_terminal_not_advance")
    if contracts_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("contracts_terminal_next_wrong")
    if summary.get("ready_for_fixture_build") is not True:
        failures.append("not_ready_for_fixture_build")
    if summary.get("ready_for_c7_test_run") is not False:
        failures.append("should_not_be_ready_for_c7_test_run_yet")

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
        if summary.get(key) is not False:
            failures.append(f"required_false_wrong:{key}:{summary.get(key)}")

    if step_contract.get("contract_status") != "FROZEN":
        failures.append("step_packet_contract_not_frozen")
    if stop_contract.get("contract_status") != "FROZEN":
        failures.append("stop_packet_contract_not_frozen")
    if budget.get("budget_status") != "FROZEN":
        failures.append("budget_not_frozen")
    if unit_feedback_contract.get("contract_status") != "FROZEN":
        failures.append("unit_feedback_contract_not_frozen")
    if negative_counter_contract.get("contract_status") != "FROZEN":
        failures.append("negative_counter_contract_not_frozen")
    if rollup_contract.get("contract_status") != "FROZEN":
        failures.append("rollup_contract_not_frozen")
    if readout_contract.get("contract_status") != "FROZEN":
        failures.append("readout_contract_not_frozen")

    counter_names = negative_counter_contract.get("must_be_zero", [])
    if not counter_names:
        failures.append("negative_counter_names_missing")

    required_step_fields = set(step_contract.get("required_fields", []))
    required_stop_fields = set(stop_contract.get("required_fields", []))
    required_feedback_fields = set(unit_feedback_contract.get("required_fields", []))

    run_a = "runtime_run_sequence_A_clean_continuation"
    steps_a = [
        step_packet(
            fixture_id="sequence_A_clean_continuation",
            run_id=run_a,
            step_index=0,
            active_object="accepted_packet_A0",
            attempted_move="bounded_continue",
            schema_result="VALID",
            cell0_result="ALLOW",
            execution_result="EXECUTED",
            terminal="ADVANCE",
            next_packet_ref="sequence_A_clean_continuation__input_packet_1",
            counter_names=counter_names,
        ),
        step_packet(
            fixture_id="sequence_A_clean_continuation",
            run_id=run_a,
            step_index=1,
            active_object="accepted_packet_A1",
            attempted_move="bounded_continue",
            schema_result="VALID",
            cell0_result="ALLOW",
            execution_result="EXECUTED",
            terminal="ADVANCE",
            next_packet_ref="sequence_A_clean_continuation__input_packet_2",
            counter_names=counter_names,
        ),
        step_packet(
            fixture_id="sequence_A_clean_continuation",
            run_id=run_a,
            step_index=2,
            active_object="accepted_packet_A2",
            attempted_move="bounded_close",
            schema_result="VALID",
            cell0_result="ALLOW",
            execution_result="EXECUTED",
            terminal="STOP",
            next_packet_ref=None,
            counter_names=counter_names,
        ),
    ]
    stop_a = stop_packet(
        fixture_id="sequence_A_clean_continuation",
        run_id=run_a,
        stop_step_index=2,
        stop_code="STOP_DONE",
        stop_reason="Clean synthetic continuation completed within budget.",
        last_valid_packet_ref="sequence_A_clean_continuation__input_packet_2",
        blocked_packet_ref=None,
        blocked_move=None,
        blocked_by="BUDGETED_SEQUENCE_COMPLETE",
        lawful_next_handling=["emit rollup", "classify RADIUS_EXPANDED_CLEANLY"],
    )

    run_b = "runtime_run_sequence_B_schema_gap_halt"
    fb_b = feedback_record(
        fixture_id="sequence_B_schema_gap_halt",
        run_id=run_b,
        step_id="sequence_B_schema_gap_halt__step_1",
        failure_kind="SCHEMA_GAP",
        failed_boundary="SCHEMA_VALIDATOR_CELL",
        blocked_move="consume_unknown_packet_type",
        missing_object_or_capability="registered schema for packet_type=unknown_packet_B1",
        lawful_next_handling=["emit schema feedback", "halt", "propose schema contract if needed"],
        diagnostic_quality="USEFUL",
    )
    steps_b = [
        step_packet(
            fixture_id="sequence_B_schema_gap_halt",
            run_id=run_b,
            step_index=0,
            active_object="accepted_packet_B0",
            attempted_move="bounded_continue",
            schema_result="VALID",
            cell0_result="ALLOW",
            execution_result="EXECUTED",
            terminal="ADVANCE",
            next_packet_ref="sequence_B_schema_gap_halt__input_packet_1",
            counter_names=counter_names,
        ),
        step_packet(
            fixture_id="sequence_B_schema_gap_halt",
            run_id=run_b,
            step_index=1,
            active_object="unknown_packet_B1",
            attempted_move="consume_unknown_packet_type",
            schema_result="UNKNOWN_SCHEMA",
            cell0_result="NOT_REACHED",
            execution_result=None,
            terminal="STOP",
            next_packet_ref=None,
            counter_names=counter_names,
            feedback_ref=fb_b["unit_feedback_id"],
        ),
    ]
    stop_b = stop_packet(
        fixture_id="sequence_B_schema_gap_halt",
        run_id=run_b,
        stop_step_index=1,
        stop_code="STOP_SCHEMA_GAP",
        stop_reason="Next packet has no registered schema.",
        last_valid_packet_ref="sequence_B_schema_gap_halt__input_packet_0",
        blocked_packet_ref="sequence_B_schema_gap_halt__input_packet_1",
        blocked_move="consume_unknown_packet_type",
        blocked_by="SCHEMA_VALIDATOR_CELL",
        lawful_next_handling=["emit schema feedback", "halt", "request schema review"],
    )

    run_c = "runtime_run_sequence_C_authority_boundary_halt"
    fb_c = feedback_record(
        fixture_id="sequence_C_authority_boundary_halt",
        run_id=run_c,
        step_id="sequence_C_authority_boundary_halt__step_1",
        failure_kind="AUTHORITY_BOUNDARY",
        failed_boundary="CELL0_LAWFUL_ADMISSIBILITY_SURFACE",
        blocked_move="runtime_patch",
        missing_object_or_capability="explicit runtime patch authority",
        lawful_next_handling=["halt", "emit authority proposal", "request review"],
        diagnostic_quality="USEFUL",
    )
    steps_c = [
        step_packet(
            fixture_id="sequence_C_authority_boundary_halt",
            run_id=run_c,
            step_index=0,
            active_object="accepted_packet_C0",
            attempted_move="bounded_continue",
            schema_result="VALID",
            cell0_result="ALLOW",
            execution_result="EXECUTED",
            terminal="ADVANCE",
            next_packet_ref="sequence_C_authority_boundary_halt__input_packet_1",
            counter_names=counter_names,
        ),
        step_packet(
            fixture_id="sequence_C_authority_boundary_halt",
            run_id=run_c,
            step_index=1,
            active_object="runtime_patch_packet_C1",
            attempted_move="runtime_patch",
            schema_result="VALID",
            cell0_result="AUTHORITY_REQUIRED",
            execution_result=None,
            terminal="STOP",
            next_packet_ref=None,
            counter_names=counter_names,
            feedback_ref=fb_c["unit_feedback_id"],
        ),
    ]
    stop_c = stop_packet(
        fixture_id="sequence_C_authority_boundary_halt",
        run_id=run_c,
        stop_step_index=1,
        stop_code="STOP_AUTHORITY_REQUIRED",
        stop_reason="Packet is schema-valid but move crosses current authority boundary.",
        last_valid_packet_ref="sequence_C_authority_boundary_halt__input_packet_0",
        blocked_packet_ref="sequence_C_authority_boundary_halt__input_packet_1",
        blocked_move="runtime_patch",
        blocked_by="CELL0_LAWFUL_ADMISSIBILITY_SURFACE",
        lawful_next_handling=["request review", "emit authority proposal", "park blocked packet"],
    )

    run_d = "runtime_run_sequence_D_cell1_accepted_build_handoff"
    steps_d = [
        step_packet(
            fixture_id="sequence_D_cell1_accepted_build_handoff",
            run_id=run_d,
            step_index=0,
            active_object="accepted_cell1_packet_D0",
            attempted_move="cell1_intake_accepted_packet",
            schema_result="VALID",
            cell0_result="ALLOW",
            execution_result="EXECUTED",
            terminal="ADVANCE",
            next_packet_ref="sequence_D_cell1_accepted_build_handoff__input_packet_1",
            counter_names=counter_names,
        ),
        step_packet(
            fixture_id="sequence_D_cell1_accepted_build_handoff",
            run_id=run_d,
            step_index=1,
            active_object="cell1_bounded_probe_D1",
            attempted_move="run_bounded_probe",
            schema_result="VALID",
            cell0_result="ALLOW",
            execution_result="EXECUTED",
            terminal="ADVANCE",
            next_packet_ref="sequence_D_cell1_accepted_build_handoff__input_packet_2",
            counter_names=counter_names,
        ),
        step_packet(
            fixture_id="sequence_D_cell1_accepted_build_handoff",
            run_id=run_d,
            step_index=2,
            active_object="verification_return_D2",
            attempted_move="emit_verification_return",
            schema_result="VALID",
            cell0_result="ALLOW",
            execution_result="EXECUTED",
            terminal="ADVANCE",
            next_packet_ref="sequence_D_cell1_accepted_build_handoff__input_packet_3",
            counter_names=counter_names,
        ),
        step_packet(
            fixture_id="sequence_D_cell1_accepted_build_handoff",
            run_id=run_d,
            step_index=3,
            active_object="handoff_packet_D3",
            attempted_move="emit_typed_handoff",
            schema_result="VALID",
            cell0_result="ALLOW",
            execution_result="EXECUTED",
            terminal="STOP",
            next_packet_ref=None,
            counter_names=counter_names,
        ),
    ]
    stop_d = stop_packet(
        fixture_id="sequence_D_cell1_accepted_build_handoff",
        run_id=run_d,
        stop_step_index=3,
        stop_code="STOP_DONE",
        stop_reason="Cell 1 consumed accepted packet, ran bounded probe, verified, and emitted typed handoff.",
        last_valid_packet_ref="sequence_D_cell1_accepted_build_handoff__input_packet_3",
        blocked_packet_ref=None,
        blocked_move=None,
        blocked_by="BUDGETED_SEQUENCE_COMPLETE",
        lawful_next_handling=["emit rollup", "classify RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES"],
    )

    run_e = "runtime_run_sequence_E_missing_capability_feedback"
    fb_e = feedback_record(
        fixture_id="sequence_E_missing_capability_feedback",
        run_id=run_e,
        step_id="sequence_E_missing_capability_feedback__step_1",
        failure_kind="MISSING_CAPABILITY",
        failed_boundary="UNIT_FEEDBACK_BOUNDARY",
        blocked_move="classify_next_runtime_packet_without_discriminator",
        missing_object_or_capability="packet discriminator for next runtime packet family",
        lawful_next_handling=["halt", "emit capability proposal", "add discriminator contract after review"],
        diagnostic_quality="USEFUL",
    )
    steps_e = [
        step_packet(
            fixture_id="sequence_E_missing_capability_feedback",
            run_id=run_e,
            step_index=0,
            active_object="accepted_packet_E0",
            attempted_move="bounded_continue",
            schema_result="VALID",
            cell0_result="ALLOW",
            execution_result="EXECUTED",
            terminal="ADVANCE",
            next_packet_ref="sequence_E_missing_capability_feedback__input_packet_1",
            counter_names=counter_names,
        ),
        step_packet(
            fixture_id="sequence_E_missing_capability_feedback",
            run_id=run_e,
            step_index=1,
            active_object="packet_family_E1",
            attempted_move="classify_next_runtime_packet_without_discriminator",
            schema_result="VALID",
            cell0_result="ALLOW",
            execution_result=None,
            terminal="STOP",
            next_packet_ref=None,
            counter_names=counter_names,
            feedback_ref=fb_e["unit_feedback_id"],
        ),
    ]
    stop_e = stop_packet(
        fixture_id="sequence_E_missing_capability_feedback",
        run_id=run_e,
        stop_step_index=1,
        stop_code="STOP_MISSING_CAPABILITY",
        stop_reason="Runtime reached a move requiring a missing packet discriminator capability.",
        last_valid_packet_ref="sequence_E_missing_capability_feedback__input_packet_0",
        blocked_packet_ref="sequence_E_missing_capability_feedback__input_packet_1",
        blocked_move="classify_next_runtime_packet_without_discriminator",
        blocked_by="UNIT_FEEDBACK_BOUNDARY",
        lawful_next_handling=["emit useful feedback", "halt", "propose capability refinement"],
    )

    fixtures = [
        fixture(
            fixture_id="sequence_A_clean_continuation",
            title="Sequence A — Clean continuation",
            expected_outcome="RADIUS_EXPANDED_CLEANLY",
            purpose="Valid packets continue under schema-valid and Cell0-admissible boundaries.",
            steps=steps_a,
            stop=stop_a,
            feedback_records=[],
            notes=["Positive control; no artificial or real boundary halt."],
        ),
        fixture(
            fixture_id="sequence_B_schema_gap_halt",
            title="Sequence B — Schema gap halt",
            expected_outcome="RADIUS_BLOCKED_BY_SCHEMA_GAP",
            purpose="Unknown schema blocks before admissibility or execution.",
            steps=steps_b,
            stop=stop_b,
            feedback_records=[fb_b],
            notes=["Negative halt; schema invalid advancement counter must remain zero."],
        ),
        fixture(
            fixture_id="sequence_C_authority_boundary_halt",
            title="Sequence C — Authority boundary halt",
            expected_outcome="RADIUS_BLOCKED_BY_AUTHORITY_BOUNDARY",
            purpose="Schema-valid packet is denied by Cell0 authority boundary and does not execute.",
            steps=steps_c,
            stop=stop_c,
            feedback_records=[fb_c],
            notes=["Real boundary halt; admissibility denied executed counter must remain zero."],
        ),
        fixture(
            fixture_id="sequence_D_cell1_accepted_build_handoff",
            title="Sequence D — Cell 1 accepted build handoff",
            expected_outcome="RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES",
            purpose="Accepted Cell 1 packet flows through bounded probe, verification return, and typed handoff.",
            steps=steps_d,
            stop=stop_d,
            feedback_records=[],
            notes=["Inter-cell protocol stress; no proposed-only packet reaches Cell 1."],
        ),
        fixture(
            fixture_id="sequence_E_missing_capability_feedback",
            title="Sequence E — Missing capability feedback",
            expected_outcome="RADIUS_BLOCKED_BY_MISSING_CAPABILITY",
            purpose="Missing capability halts with useful feedback instead of bare failed status.",
            steps=steps_e,
            stop=stop_e,
            feedback_records=[fb_e],
            notes=["O2/unit feedback stress; diagnostic quality must be USEFUL."],
        ),
    ]

    fixture_paths: List[Dict[str, str]] = []
    validation_errors: List[str] = []

    for fx in fixtures:
        fx_path = FIXTURE_DIR / f"{fx['fixture_id']}.json"
        write_json(fx_path, fx)
        fixture_paths.append({
            "fixture_id": fx["fixture_id"],
            "path": rel(fx_path),
            "expected_outcome": fx["expected_outcome"],
        })

        for idx, step in enumerate(fx["steps"]):
            missing = sorted(required_step_fields - set(step.keys()))
            if missing:
                validation_errors.append(f"{fx['fixture_id']}:step_{idx}:missing_step_fields:{','.join(missing)}")
            if step.get("terminal") not in step_contract.get("terminal_values", []):
                validation_errors.append(f"{fx['fixture_id']}:step_{idx}:terminal_invalid:{step.get('terminal')}")
            for counter_name in counter_names:
                if step.get("bad_counters", {}).get(counter_name) != 0:
                    validation_errors.append(f"{fx['fixture_id']}:step_{idx}:counter_not_zero:{counter_name}")

        stop_missing = sorted(required_stop_fields - set(fx["stop_packet"].keys()))
        if stop_missing:
            validation_errors.append(f"{fx['fixture_id']}:stop:missing_stop_fields:{','.join(stop_missing)}")
        if fx["stop_packet"].get("stop_code") not in stop_contract.get("allowed_stop_codes", []):
            validation_errors.append(f"{fx['fixture_id']}:stop_code_invalid:{fx['stop_packet'].get('stop_code')}")

        for j, feedback in enumerate(fx.get("unit_feedback_records", [])):
            missing = sorted(required_feedback_fields - set(feedback.keys()))
            if missing:
                validation_errors.append(f"{fx['fixture_id']}:feedback_{j}:missing_feedback_fields:{','.join(missing)}")
            if feedback.get("diagnostic_quality") not in unit_feedback_contract.get("diagnostic_quality_values", []):
                validation_errors.append(f"{fx['fixture_id']}:feedback_{j}:diagnostic_quality_invalid:{feedback.get('diagnostic_quality')}")

    if validation_errors:
        failures.extend(validation_errors)

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C7_SYNTHETIC_RUNTIME_RADIUS_FIXTURES_BUILT_RUNNER_NEXT" if gate == "PASS" else "TYPED_C7_SYNTHETIC_RUNTIME_RADIUS_FIXTURES_GATE_FAIL"

    source_hash_manifest = {rel(p): file_sha256(p) for p in required}

    basis = {
        "schema_version": "c7_synthetic_fixture_build_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_c7_contracts_receipt_id": SOURCE_C7_CONTRACTS_RECEIPT_ID,
        "source_files": source_hash_manifest,
        "basis_claim": "C7 contracts and budget passed; synthetic fixtures A-E can be built without running C7.",
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

    fixture_index = {
        "schema_version": "c7_synthetic_fixture_index_v0",
        "index_status": "EMITTED" if gate == "PASS" else "NOT_EMITTED",
        "fixture_count": len(fixtures) if gate == "PASS" else 0,
        "fixtures": fixture_paths,
    }

    expected_outcomes = {
        "schema_version": "c7_synthetic_fixture_expected_outcomes_v0",
        "expected_outcomes": {
            item["fixture_id"]: item["expected_outcome"] for item in fixture_paths
        },
        "run_order": [
            "sequence_A_clean_continuation",
            "sequence_B_schema_gap_halt",
            "sequence_C_authority_boundary_halt",
            "sequence_D_cell1_accepted_build_handoff",
            "sequence_E_missing_capability_feedback",
        ],
        "first_actual_test_run_unit": "RUN_C7_SYNTHETIC_RADIUS_SEQUENCE_A_CLEAN_CONTINUATION_V0",
    }

    validation_report = {
        "schema_version": "c7_synthetic_fixture_validation_report_v0",
        "validation_status": "PASS" if gate == "PASS" else "FAIL",
        "validation_errors": validation_errors,
        "checked_against": {
            "step_packet_contract": rel(STEP_PACKET_CONTRACT_PATH),
            "stop_packet_contract": rel(STOP_PACKET_CONTRACT_PATH),
            "unit_feedback_contract": rel(UNIT_FEEDBACK_CONTRACT_PATH),
            "negative_counter_contract": rel(NEGATIVE_COUNTER_CONTRACT_PATH),
        },
        "fixture_count": len(fixtures),
        "step_packet_count": sum(len(fx["steps"]) for fx in fixtures),
        "stop_packet_count": len(fixtures),
        "unit_feedback_record_count": sum(len(fx["unit_feedback_records"]) for fx in fixtures),
    }

    runner_build_target = {
        "schema_version": "c7_synthetic_runner_build_target_v0",
        "target_status": "RUNNER_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "runner_scope": "build synthetic runner over frozen contracts and synthetic fixtures only",
        "runner_inputs": [
            rel(FIXTURE_INDEX_PATH),
            rel(EXPECTED_OUTCOMES_PATH),
            rel(STEP_PACKET_CONTRACT_PATH),
            rel(STOP_PACKET_CONTRACT_PATH),
            rel(BUDGET_PATH),
            rel(UNIT_FEEDBACK_CONTRACT_PATH),
            rel(NEGATIVE_COUNTER_CONTRACT_PATH),
            rel(ROLLUP_CONTRACT_PATH),
            rel(READOUT_CONTRACT_PATH),
        ],
        "runner_must_not": [
            "run live runtime",
            "authorize runtime adoption",
            "patch runtime",
            "install live hooks",
            "route runtime traffic",
            "mutate schema archive",
            "advance hidden next command",
        ],
    }

    rollup = {
        "schema_version": "c7_synthetic_fixture_build_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "source_c7_contracts_receipt_id": SOURCE_C7_CONTRACTS_RECEIPT_ID,
        "fixtures_built": gate == "PASS",
        "fixture_count": len(fixtures) if gate == "PASS" else 0,
        "step_packet_count": validation_report["step_packet_count"] if gate == "PASS" else 0,
        "stop_packet_count": validation_report["stop_packet_count"] if gate == "PASS" else 0,
        "unit_feedback_record_count": validation_report["unit_feedback_record_count"] if gate == "PASS" else 0,
        "ready_for_runner_build": gate == "PASS",
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
        "schema_version": "c7_synthetic_fixture_build_profile_v0",
        "profile_status": status,
        "profile": "C7_SYNTHETIC_RUNTIME_RADIUS_FIXTURES_A_TO_E",
        "what_changed": "Synthetic C7 runtime-radius fixtures A-E were built and validated against frozen contracts.",
        "what_did_not_change": [
            "C7 runtime test has not run",
            "runtime adoption is not authorized",
            "runtime is not patched",
            "live hooks are not installed",
            "schema archive is not mutated",
            "control path authority is not granted",
        ],
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_C7_SYNTHETIC_RUNTIME_RADIUS_FIXTURES_V0",
        "next_command_goal": None,
    }

    trace = {
        "schema_version": "c7_synthetic_fixture_build_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "C7_CONTRACTS_AND_BUDGET_PREPARED_FIXTURES_NEXT",
                "edge": "consume contracts and fixture build target",
                "to": "C7_FIXTURE_BUILD_BASIS_ACCEPTED" if gate == "PASS" else "C7_FIXTURE_BUILD_BASIS_FAIL",
            },
            {
                "from": "C7_FIXTURE_BUILD_BASIS_ACCEPTED" if gate == "PASS" else "C7_FIXTURE_BUILD_BASIS_FAIL",
                "edge": "build synthetic fixtures A-E",
                "to": "C7_SYNTHETIC_RUNNER_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C7_SYNTHETIC_FIXTURES_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (FIXTURE_INDEX_PATH, fixture_index),
        (EXPECTED_OUTCOMES_PATH, expected_outcomes),
        (VALIDATION_REPORT_PATH, validation_report),
        (RUNNER_BUILD_TARGET_PATH, runner_build_target),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_PATH, trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "C7_SYNTHETIC_RUNTIME_RADIUS_FIXTURES_BUILT",
        "CONTRACTS_AND_BUDGET_RECEIPT_CONSUMED",
        "SEQUENCE_A_CLEAN_CONTINUATION_BUILT",
        "SEQUENCE_B_SCHEMA_GAP_HALT_BUILT",
        "SEQUENCE_C_AUTHORITY_BOUNDARY_HALT_BUILT",
        "SEQUENCE_D_CELL1_ACCEPTED_BUILD_HANDOFF_BUILT",
        "SEQUENCE_E_MISSING_CAPABILITY_FEEDBACK_BUILT",
        "FIXTURES_VALIDATE_AGAINST_CONTRACTS",
        "RUNNER_IS_NEXT_TYPED_UNIT",
        "NO_C7_RUNTIME_RUN",
        "NO_RUNTIME_ADOPTION",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_HOOK_INSTALL",
        "NO_SCHEMA_MUTATION",
        "NO_CONTROL_PATH_AUTHORITY",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt_body = {
        "schema_version": "c7_synthetic_runtime_radius_fixtures_receipt_v0",
        "receipt_type": "TYPED_C7_SYNTHETIC_RUNTIME_RADIUS_FIXTURES_RECEIPT",
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
        "source_c7_contracts_receipt_id": SOURCE_C7_CONTRACTS_RECEIPT_ID,
        "acceptance_gate_results": {
            "C7_FIXTURES_0_CONTRACTS_RECEIPT_CONSUMED": gate == "PASS",
            "C7_FIXTURES_1_SEQUENCE_A_BUILT": gate == "PASS",
            "C7_FIXTURES_2_SEQUENCE_B_BUILT": gate == "PASS",
            "C7_FIXTURES_3_SEQUENCE_C_BUILT": gate == "PASS",
            "C7_FIXTURES_4_SEQUENCE_D_BUILT": gate == "PASS",
            "C7_FIXTURES_5_SEQUENCE_E_BUILT": gate == "PASS",
            "C7_FIXTURES_6_FIXTURES_VALIDATE_AGAINST_CONTRACTS": gate == "PASS",
            "C7_FIXTURES_7_RUNNER_NEXT": gate == "PASS",
            "C7_FIXTURES_8_NO_RUNTIME_RUN": gate == "PASS",
            "C7_FIXTURES_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_c7_synthetic_fixture_summary": {
            "status": status,
            "c7_synthetic_fixtures_built": gate == "PASS",
            "source_c7_contracts_receipt_consumed": gate == "PASS",
            "fixture_count": rollup["fixture_count"],
            "step_packet_count": rollup["step_packet_count"],
            "stop_packet_count": rollup["stop_packet_count"],
            "unit_feedback_record_count": rollup["unit_feedback_record_count"],
            "ready_for_runner_build": gate == "PASS",
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
            "fixture_index": rel(FIXTURE_INDEX_PATH),
            "expected_outcomes": rel(EXPECTED_OUTCOMES_PATH),
            "validation_report": rel(VALIDATION_REPORT_PATH),
            "runner_build_target": rel(RUNNER_BUILD_TARGET_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "transition_trace": rel(TRACE_PATH),
            "fixture_dir": rel(FIXTURE_DIR),
        },
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C7_SYNTHETIC_FIXTURES_GATE_FAIL",
        },
    }

    receipt_id = sig8(receipt_body)
    receipt_body["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_body["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_body)

    print(json.dumps(receipt_body, indent=2, sort_keys=True))
    print(f"c7_synthetic_fixtures_receipt_id={receipt_id}")
    print(f"c7_synthetic_fixtures_receipt_path={rel(receipt_path)}")
    print(f"c7_synthetic_fixtures_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
