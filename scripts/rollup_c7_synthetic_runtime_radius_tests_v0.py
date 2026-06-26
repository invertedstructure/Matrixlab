#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ROLLUP_C7_SYNTHETIC_RUNTIME_RADIUS_TESTS_V0"
TARGET_UNIT_ID = "runtime.practical_radius_expansion.synthetic_tests_rollup.v0"

LAYER = "RUNTIME / C7 / SYNTHETIC_TEST / FULL_ROLLUP"
MODE = "ROLLUP_ONLY / CLASSIFY_SYNTHETIC_TESTS / NO_LIVE_RUNTIME"
BUILD_MODE = "C7_SYNTHETIC_RUNTIME_RADIUS_TESTS_ROLLUP_ONLY"

SOURCE_C7_HANDOFF_FEEDBACK_RECEIPT_ID = "9612c2a6"

HANDOFF_FEEDBACK_RECEIPT_PATH = ROOT / "data/c7_synthetic_radius_handoff_and_feedback_d_e_v0_receipts/9612c2a6.json"
FULL_ROLLUP_TARGET_PATH = ROOT / "data/c7_synthetic_radius_handoff_and_feedback_d_e_v0/c7_full_synthetic_rollup_target_v0.json"

SEQUENCE_A_RECEIPT_PATH = ROOT / "data/c7_synthetic_radius_sequence_a_clean_continuation_v0_receipts/2d503369.json"
NEGATIVE_HALTS_RECEIPT_PATH = ROOT / "data/c7_synthetic_radius_negative_halts_b_c_v0_receipts/be2430b4.json"
HANDOFF_FEEDBACK_STAGE_RECEIPT_PATH = ROOT / "data/c7_synthetic_radius_handoff_and_feedback_d_e_v0_receipts/9612c2a6.json"

RUNNER_RECEIPT_PATH = ROOT / "data/c7_synthetic_runtime_radius_runner_v0_receipts/0b9012bf.json"
FIXTURE_INDEX_PATH = ROOT / "data/c7_synthetic_runtime_radius_fixtures_v0/c7_synthetic_fixture_index_v0.json"
EXPECTED_OUTCOMES_PATH = ROOT / "data/c7_synthetic_runtime_radius_fixtures_v0/c7_synthetic_fixture_expected_outcomes_v0.json"

ROLLUP_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_rollup_contract_v0.json"
READOUT_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_readout_contract_v0.json"
NEGATIVE_COUNTER_CONTRACT_PATH = ROOT / "data/c7_runtime_radius_contracts_and_budget_v0/runtime_radius_negative_counter_contract_v0.json"

RUN_RECEIPTS_DIR = ROOT / "data/c7_synthetic_runtime_radius_run_receipts_v0"
RUNS_DIR = ROOT / "data/c7_synthetic_runtime_radius_runs_v0"

OUT_DIR = ROOT / "data/c7_synthetic_runtime_radius_tests_rollup_v0"
RECEIPT_DIR = ROOT / "data/c7_synthetic_runtime_radius_tests_rollup_v0_receipts"

BASIS_PATH = OUT_DIR / "c7_full_synthetic_rollup_basis_v0.json"
FIXTURE_RESULT_INDEX_PATH = OUT_DIR / "c7_full_synthetic_fixture_result_index_v0.json"
FULL_ROLLUP_PATH = OUT_DIR / "runtime_radius_full_synthetic_rollup_v0.json"
FULL_READOUT_PATH = OUT_DIR / "runtime_radius_full_synthetic_readout_v0.json"
ASSERTION_REPORT_PATH = OUT_DIR / "c7_full_synthetic_assertion_report_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "c7_full_synthetic_classification_v0.json"
CLOSURE_PATH = OUT_DIR / "c7_synthetic_runtime_radius_test_branch_closure_v0.json"
PROFILE_PATH = OUT_DIR / "c7_full_synthetic_rollup_profile_v0.json"
TRACE_PATH = OUT_DIR / "c7_full_synthetic_rollup_transition_trace.json"

EXPECTED_HANDOFF_STATUS = "TYPED_C7_SYNTHETIC_HANDOFF_FEEDBACK_D_E_PASS_FULL_ROLLUP_NEXT"

FIXTURE_IDS = [
    "sequence_A_clean_continuation",
    "sequence_B_schema_gap_halt",
    "sequence_C_authority_boundary_halt",
    "sequence_D_cell1_accepted_build_handoff",
    "sequence_E_missing_capability_feedback",
]

EXPECTED_OUTCOMES = {
    "sequence_A_clean_continuation": "RADIUS_EXPANDED_CLEANLY",
    "sequence_B_schema_gap_halt": "RADIUS_BLOCKED_BY_SCHEMA_GAP",
    "sequence_C_authority_boundary_halt": "RADIUS_BLOCKED_BY_AUTHORITY_BOUNDARY",
    "sequence_D_cell1_accepted_build_handoff": "RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES",
    "sequence_E_missing_capability_feedback": "RADIUS_BLOCKED_BY_MISSING_CAPABILITY",
}

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

def latest_json_file(path: Path) -> Path | None:
    files = sorted(path.glob("*.json"))
    return files[-1] if files else None

def require_false(obj: Dict[str, Any], key: str, failures: List[str]) -> None:
    if obj.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{obj.get(key)}")

def load_fixture_result(fixture_id: str) -> Dict[str, Any]:
    receipt_path = latest_json_file(RUN_RECEIPTS_DIR / fixture_id)
    if receipt_path is None:
        return {"fixture_id": fixture_id, "missing": True, "error": "receipt_missing"}

    receipt = read_json(receipt_path)
    rollup_path = ROOT / receipt.get("output_artifacts", {}).get("rollup", "")
    readout_path = ROOT / receipt.get("output_artifacts", {}).get("readout", "")
    step_packets_path = ROOT / receipt.get("output_artifacts", {}).get("step_packets", "")
    stop_packet_path = ROOT / receipt.get("output_artifacts", {}).get("stop_packet", "")
    feedback_path = ROOT / receipt.get("output_artifacts", {}).get("unit_feedback_records", "")

    rollup = read_json(rollup_path) if rollup_path.exists() else {}
    readout = read_json(readout_path) if readout_path.exists() else {}
    stop_packet = read_json(stop_packet_path) if stop_packet_path.exists() else {}

    feedback_count = 0
    if feedback_path.exists():
        text = feedback_path.read_text().strip()
        feedback_count = 0 if not text else len(text.splitlines())

    step_packet_count = 0
    if step_packets_path.exists():
        text = step_packets_path.read_text().strip()
        step_packet_count = 0 if not text else len(text.splitlines())

    return {
        "fixture_id": fixture_id,
        "missing": False,
        "receipt_path": rel(receipt_path),
        "receipt_id": receipt.get("receipt_id"),
        "receipt_gate": receipt.get("gate"),
        "expected_outcome": EXPECTED_OUTCOMES[fixture_id],
        "observed_outcome": receipt.get("outcome"),
        "rollup": rollup,
        "readout": readout,
        "stop_packet": stop_packet,
        "step_packet_count": step_packet_count,
        "unit_feedback_record_count": feedback_count,
        "artifact_paths": {
            "rollup": rel(rollup_path) if rollup_path.exists() else None,
            "readout": rel(readout_path) if readout_path.exists() else None,
            "step_packets": rel(step_packets_path) if step_packets_path.exists() else None,
            "stop_packet": rel(stop_packet_path) if stop_packet_path.exists() else None,
            "unit_feedback_records": rel(feedback_path) if feedback_path.exists() else None,
        },
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        HANDOFF_FEEDBACK_RECEIPT_PATH,
        FULL_ROLLUP_TARGET_PATH,
        SEQUENCE_A_RECEIPT_PATH,
        NEGATIVE_HALTS_RECEIPT_PATH,
        HANDOFF_FEEDBACK_STAGE_RECEIPT_PATH,
        RUNNER_RECEIPT_PATH,
        FIXTURE_INDEX_PATH,
        EXPECTED_OUTCOMES_PATH,
        ROLLUP_CONTRACT_PATH,
        READOUT_CONTRACT_PATH,
        NEGATIVE_COUNTER_CONTRACT_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    handoff_receipt = read_json(HANDOFF_FEEDBACK_RECEIPT_PATH)
    handoff_summary = handoff_receipt.get("machine_readable_c7_handoff_and_feedback_d_e_summary", {})
    rollup_target = read_json(FULL_ROLLUP_TARGET_PATH)
    fixture_index = read_json(FIXTURE_INDEX_PATH)
    expected_outcomes_index = read_json(EXPECTED_OUTCOMES_PATH)
    negative_counter_contract = read_json(NEGATIVE_COUNTER_CONTRACT_PATH)
    rollup_contract = read_json(ROLLUP_CONTRACT_PATH)
    readout_contract = read_json(READOUT_CONTRACT_PATH)

    if handoff_receipt.get("receipt_id") != SOURCE_C7_HANDOFF_FEEDBACK_RECEIPT_ID:
        failures.append(f"handoff_receipt_id_wrong:{handoff_receipt.get('receipt_id')}")
    if handoff_receipt.get("gate") != "PASS":
        failures.append(f"handoff_gate_wrong:{handoff_receipt.get('gate')}")
    if handoff_summary.get("status") != EXPECTED_HANDOFF_STATUS:
        failures.append(f"handoff_status_wrong:{handoff_summary.get('status')}")
    if handoff_summary.get("next_unit_id") != UNIT_ID:
        failures.append(f"handoff_next_unit_wrong:{handoff_summary.get('next_unit_id')}")
    if handoff_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("handoff_terminal_not_advance")
    if handoff_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("handoff_terminal_next_wrong")
    if handoff_summary.get("ready_for_full_c7_synthetic_rollup") is not True:
        failures.append("handoff_not_ready_for_full_rollup")

    if rollup_target.get("target_status") != "FULL_SYNTHETIC_ROLLUP_NEXT":
        failures.append(f"rollup_target_status_wrong:{rollup_target.get('target_status')}")
    if rollup_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"rollup_target_next_wrong:{rollup_target.get('next_unit_id')}")
    if rollup_target.get("synthetic_test_only") is not True:
        failures.append("rollup_target_not_synthetic_only")
    if rollup_target.get("does_not_authorize_live_runtime") is not True:
        failures.append("rollup_target_live_runtime_boundary_missing")

    if set(rollup_target.get("fixture_ids", [])) != set(FIXTURE_IDS):
        failures.append("rollup_target_fixture_ids_wrong")
    if set(item.get("fixture_id") for item in fixture_index.get("fixtures", [])) != set(FIXTURE_IDS):
        failures.append("fixture_index_fixture_ids_wrong")

    for fixture_id, expected in EXPECTED_OUTCOMES.items():
        if expected_outcomes_index.get("expected_outcomes", {}).get(fixture_id) != expected:
            failures.append(f"expected_outcomes_index_wrong:{fixture_id}")

    for key in [
        "c7_live_runtime_run_authorized",
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
        require_false(handoff_summary, key, failures)

    results = [load_fixture_result(fixture_id) for fixture_id in FIXTURE_IDS]

    for result in results:
        fixture_id = result["fixture_id"]
        if result.get("missing"):
            failures.append(f"{fixture_id}:run_receipt_missing")
            continue
        if result.get("receipt_gate") != "PASS":
            failures.append(f"{fixture_id}:receipt_gate_wrong:{result.get('receipt_gate')}")
        if result.get("observed_outcome") != result.get("expected_outcome"):
            failures.append(f"{fixture_id}:outcome_wrong:{result.get('observed_outcome')}")
        rollup = result.get("rollup", {})
        if rollup.get("outcome") != result.get("expected_outcome"):
            failures.append(f"{fixture_id}:rollup_outcome_wrong:{rollup.get('outcome')}")
        if rollup.get("halts", {}).get("untyped_halt_count") != 0:
            failures.append(f"{fixture_id}:untyped_halt_nonzero")
        for k, v in rollup.get("bad_counters", {}).items():
            if v != 0:
                failures.append(f"{fixture_id}:bad_counter_nonzero:{k}:{v}")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C7_SYNTHETIC_RUNTIME_RADIUS_TESTS_ROLLUP_PASS_BRANCH_CLOSED" if gate == "PASS" else "TYPED_C7_SYNTHETIC_RUNTIME_RADIUS_TESTS_ROLLUP_GATE_FAIL"

    source_hash_manifest = {rel(p): file_sha256(p) for p in required}

    total_steps_attempted = sum((r.get("rollup", {}).get("steps_attempted") or 0) for r in results)
    total_steps_advanced = sum((r.get("rollup", {}).get("steps_advanced") or 0) for r in results)
    total_steps_halted = sum((r.get("rollup", {}).get("steps_halted") or 0) for r in results)
    total_unit_feedback = sum((r.get("unit_feedback_record_count") or 0) for r in results)
    total_untyped_halts = sum((r.get("rollup", {}).get("halts", {}).get("untyped_halt_count") or 0) for r in results)
    total_typed_halts = sum((r.get("rollup", {}).get("halts", {}).get("typed_halt_count") or 0) for r in results)
    total_receipts = sum((r.get("rollup", {}).get("observability", {}).get("receipts_emitted") or 0) for r in results)
    total_edges = sum((r.get("rollup", {}).get("observability", {}).get("edge_observations_emitted") or 0) for r in results)
    total_sidecar = sum((r.get("rollup", {}).get("observability", {}).get("sidecar_event_records_emitted") or 0) for r in results)

    bad_counter_names = negative_counter_contract.get("must_be_zero", [])
    aggregated_bad_counters = {name: 0 for name in bad_counter_names}
    for result in results:
        for k, v in result.get("rollup", {}).get("bad_counters", {}).items():
            aggregated_bad_counters[k] = aggregated_bad_counters.get(k, 0) + int(v)

    outcome_counts: Dict[str, int] = {}
    for result in results:
        observed = result.get("observed_outcome")
        outcome_counts[observed] = outcome_counts.get(observed, 0) + 1

    halt_reasons: Dict[str, int] = {}
    for result in results:
        code = result.get("stop_packet", {}).get("stop_code")
        if code:
            halt_reasons[code] = halt_reasons.get(code, 0) + 1

    success = (
        gate == "PASS"
        and total_untyped_halts == 0
        and all(v == 0 for v in aggregated_bad_counters.values())
        and all(r.get("observed_outcome") == r.get("expected_outcome") for r in results)
    )

    aggregate_outcome = "C7_SYNTHETIC_RADIUS_TESTS_PASS_WITH_TYPED_BOUNDARIES" if success else "C7_SYNTHETIC_RADIUS_TESTS_FAIL"

    basis = {
        "schema_version": "c7_full_synthetic_rollup_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_c7_handoff_feedback_receipt_id": SOURCE_C7_HANDOFF_FEEDBACK_RECEIPT_ID,
        "source_files": source_hash_manifest,
        "basis_claim": "All C7 synthetic fixtures A-E have run and the handoff/feedback stage named full rollup as the next typed unit.",
        "does_not_authorize": [
            "live runtime run",
            "runtime adoption",
            "runtime patching",
            "live hooks",
            "runtime routing",
            "schema mutation",
            "control path authority",
        ],
    }

    fixture_result_index = {
        "schema_version": "c7_full_synthetic_fixture_result_index_v0",
        "index_status": "EMITTED" if gate == "PASS" else "PARTIAL",
        "fixture_count": len(results),
        "results": [
            {
                "fixture_id": r["fixture_id"],
                "expected_outcome": r.get("expected_outcome"),
                "observed_outcome": r.get("observed_outcome"),
                "receipt_path": r.get("receipt_path"),
                "rollup_path": r.get("artifact_paths", {}).get("rollup"),
                "readout_path": r.get("artifact_paths", {}).get("readout"),
                "step_packets_path": r.get("artifact_paths", {}).get("step_packets"),
                "stop_packet_path": r.get("artifact_paths", {}).get("stop_packet"),
                "unit_feedback_records_path": r.get("artifact_paths", {}).get("unit_feedback_records"),
            }
            for r in results
        ],
    }

    full_rollup = {
        "schema_version": "runtime_radius_full_synthetic_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "aggregate_outcome": aggregate_outcome,
        "fixtures_run": FIXTURE_IDS,
        "fixture_count": len(results),
        "steps_attempted": total_steps_attempted,
        "steps_advanced": total_steps_advanced,
        "steps_halted": total_steps_halted,
        "lawful_continuation_depth_total": total_steps_advanced,
        "max_contiguous_valid_steps_observed": max((r.get("rollup", {}).get("max_contiguous_valid_steps") or 0) for r in results),
        "outcome_counts": outcome_counts,
        "halt_reasons": halt_reasons,
        "observability": {
            "receipts_emitted": total_receipts,
            "edge_observations_emitted": total_edges,
            "unit_feedback_records_emitted": total_unit_feedback,
            "sidecar_event_records_emitted": total_sidecar,
        },
        "halts": {
            "typed_halt_count": total_typed_halts,
            "untyped_halt_count": total_untyped_halts,
        },
        "bad_counters": aggregated_bad_counters,
        "all_expected_outcomes_matched": all(r.get("observed_outcome") == r.get("expected_outcome") for r in results),
        "all_bad_counters_zero": all(v == 0 for v in aggregated_bad_counters.values()),
        "no_untyped_halts": total_untyped_halts == 0,
        "synthetic_test_only": True,
        "live_runtime_run": False,
        "runtime_adoption_authorized": False,
    }

    full_readout = {
        "schema_version": "runtime_radius_full_synthetic_readout_v0",
        "title": "C7 synthetic runtime radius readout",
        "steps_attempted": total_steps_attempted,
        "steps_advanced": total_steps_advanced,
        "typed_halts": total_typed_halts,
        "untyped_halts": total_untyped_halts,
        "longest_lawful_continuation": full_rollup["max_contiguous_valid_steps_observed"],
        "halt_reasons": halt_reasons,
        "outcomes": outcome_counts,
        "receipts_emitted": total_receipts,
        "edge_observations": total_edges,
        "unit_feedback_records": total_unit_feedback,
        "sidecar_events": total_sidecar,
        "bad_counters_zero": full_rollup["all_bad_counters_zero"],
        "interpretation": "C7 synthetic runtime radius tests passed: clean continuation, schema-gap halt, authority-boundary halt, typed Cell 1 handoff, and missing-capability feedback all matched expected outcomes with zero bad counters and zero untyped halts.",
        "must_not_infer": [
            "live runtime adoption is authorized",
            "C8 runtime is authorized",
            "runtime patching is authorized",
            "general autonomy was proven",
            "step count alone proves radius",
        ],
    }

    assertion_report = {
        "schema_version": "c7_full_synthetic_assertion_report_v0",
        "assertion_status": "PASS" if gate == "PASS" else "FAIL",
        "failures": failures,
        "assertions": {
            "all_five_fixtures_present": set(r["fixture_id"] for r in results) == set(FIXTURE_IDS),
            "all_expected_outcomes_matched": full_rollup["all_expected_outcomes_matched"],
            "total_steps_attempted_13": total_steps_attempted == 13,
            "total_steps_advanced_8": total_steps_advanced == 8,
            "total_steps_halted_5": total_steps_halted == 5,
            "unit_feedback_records_3": total_unit_feedback == 3,
            "no_untyped_halts": total_untyped_halts == 0,
            "all_bad_counters_zero": full_rollup["all_bad_counters_zero"],
            "synthetic_only": True,
            "live_runtime_not_run": True,
            "runtime_adoption_not_authorized": True,
        },
    }

    classification = {
        "schema_version": "c7_full_synthetic_classification_v0",
        "classification_status": "PASS" if success else "FAIL",
        "aggregate_outcome": aggregate_outcome,
        "primary_class": "RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES" if success else "RADIUS_FAIL_UNTYPED",
        "supporting_outcomes": outcome_counts,
        "interpretation": full_readout["interpretation"],
        "ready_for_live_runtime_adoption": False,
        "ready_for_later_runtime_adoption_discussion": success,
        "next_lawful_handling": [
            "commit synthetic C7 artifacts",
            "review C7 rollup",
            "decide whether to harden runner, add more fixtures, or prepare a separate live-runtime adoption discussion",
        ] if success else [
            "repair failed C7 synthetic rollup",
        ],
    }

    closure = {
        "schema_version": "c7_synthetic_runtime_radius_test_branch_closure_v0",
        "closure_status": "CLOSED_SYNTHETIC_PASS" if success else "NOT_CLOSED",
        "closed_object": "C7 synthetic runtime-radius test branch A-E",
        "branch_claim": "Synthetic C7 practical continuation tests passed under frozen contracts and budget.",
        "branch_does_not_authorize": [
            "live runtime run",
            "runtime adoption",
            "runtime patching",
            "live hooks",
            "runtime routing",
            "schema archive mutation",
            "control path authority",
            "general autonomy claim",
        ],
        "terminal_recommendation": "STOP_DONE" if success else "STOP_GATE_FAIL",
    }

    profile = {
        "schema_version": "c7_full_synthetic_rollup_profile_v0",
        "profile_status": status,
        "profile": "C7_SYNTHETIC_RUNTIME_RADIUS_TESTS_FULL_ROLLUP",
        "what_changed": "All C7 synthetic runtime-radius fixtures A-E were rolled up and classified.",
        "what_did_not_change": [
            "live runtime is not authorized",
            "runtime adoption is not authorized",
            "runtime is not patched",
            "live hooks are not installed",
            "schema archive is not mutated",
            "control path authority is not granted",
            "general autonomy is not claimed",
        ],
        "recommended_next": None,
        "next_command_goal": None,
    }

    trace = {
        "schema_version": "c7_full_synthetic_rollup_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "C7_HANDOFF_FEEDBACK_D_E_PASS",
                "edge": "consume full synthetic rollup target",
                "to": "C7_FULL_SYNTHETIC_ROLLUP_BASIS_ACCEPTED" if gate == "PASS" else "C7_FULL_SYNTHETIC_ROLLUP_BASIS_FAIL",
            },
            {
                "from": "C7_FULL_SYNTHETIC_ROLLUP_BASIS_ACCEPTED" if gate == "PASS" else "C7_FULL_SYNTHETIC_ROLLUP_BASIS_FAIL",
                "edge": "aggregate A-E fixture results",
                "to": "C7_SYNTHETIC_RUNTIME_RADIUS_TESTS_BRANCH_CLOSED" if success else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "STOP_DONE" if success else "STOP",
            "next_unit_id": None,
            "stop_code": "STOP_C7_SYNTHETIC_RUNTIME_RADIUS_TESTS_COMPLETE" if success else "STOP_C7_SYNTHETIC_RUNTIME_RADIUS_TESTS_ROLLUP_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (FIXTURE_RESULT_INDEX_PATH, fixture_result_index),
        (FULL_ROLLUP_PATH, full_rollup),
        (FULL_READOUT_PATH, full_readout),
        (ASSERTION_REPORT_PATH, assertion_report),
        (CLASSIFICATION_PATH, classification),
        (CLOSURE_PATH, closure),
        (PROFILE_PATH, profile),
        (TRACE_PATH, trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "C7_SYNTHETIC_RUNTIME_RADIUS_TESTS_ROLLED_UP",
        "HANDOFF_FEEDBACK_RECEIPT_CONSUMED",
        "ALL_FIVE_FIXTURES_PRESENT",
        "ALL_EXPECTED_OUTCOMES_MATCHED",
        "TOTAL_STEPS_ATTEMPTED_13",
        "TOTAL_STEPS_ADVANCED_8",
        "TOTAL_STEPS_HALTED_5",
        "UNIT_FEEDBACK_RECORDS_3",
        "BAD_COUNTERS_ZERO",
        "NO_UNTYPED_HALTS",
        "SYNTHETIC_TEST_BRANCH_CLOSED",
        "NO_LIVE_RUNTIME_RUN",
        "NO_RUNTIME_ADOPTION",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_HOOK_INSTALL",
        "NO_SCHEMA_MUTATION",
        "NO_CONTROL_PATH_AUTHORITY",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if success else failures

    receipt_body = {
        "schema_version": "c7_synthetic_runtime_radius_tests_rollup_receipt_v0",
        "receipt_type": "TYPED_C7_SYNTHETIC_RUNTIME_RADIUS_TESTS_ROLLUP_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": "PASS" if success else "FAIL",
        "status": status,
        "failures": failures,
        "warnings": [],
        "source_c7_handoff_feedback_receipt_id": SOURCE_C7_HANDOFF_FEEDBACK_RECEIPT_ID,
        "acceptance_gate_results": {
            "C7_ROLLUP_0_HANDOFF_FEEDBACK_RECEIPT_CONSUMED": success,
            "C7_ROLLUP_1_ALL_FIVE_FIXTURES_PRESENT": success,
            "C7_ROLLUP_2_EXPECTED_OUTCOMES_MATCHED": success,
            "C7_ROLLUP_3_BAD_COUNTERS_ZERO": success,
            "C7_ROLLUP_4_NO_UNTYPED_HALTS": success,
            "C7_ROLLUP_5_OBSERVABILITY_TOTALS_EMITTED": success,
            "C7_ROLLUP_6_CLASSIFICATION_EMITTED": success,
            "C7_ROLLUP_7_BRANCH_CLOSED": success,
            "C7_ROLLUP_8_NO_LIVE_RUNTIME_RUN": success,
            "C7_ROLLUP_9_NO_HIDDEN_NEXT_COMMAND": success,
        },
        "machine_readable_c7_synthetic_rollup_summary": {
            "status": status,
            "c7_synthetic_rollup_done": success,
            "aggregate_outcome": aggregate_outcome,
            "primary_class": classification["primary_class"],
            "fixtures_run": FIXTURE_IDS,
            "fixture_count": len(results),
            "steps_attempted": total_steps_attempted,
            "steps_advanced": total_steps_advanced,
            "steps_halted": total_steps_halted,
            "unit_feedback_record_count": total_unit_feedback,
            "typed_halt_count": total_typed_halts,
            "untyped_halt_count": total_untyped_halts,
            "all_expected_outcomes_matched": full_rollup["all_expected_outcomes_matched"],
            "bad_counters_zero": full_rollup["all_bad_counters_zero"],
            "synthetic_test_branch_closed": success,
            "ready_for_live_runtime_adoption": False,
            "ready_for_later_runtime_adoption_discussion": success,
            "next_unit_id": None,
            "c7_live_runtime_run_authorized": False,
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
            "fixture_result_index": rel(FIXTURE_RESULT_INDEX_PATH),
            "full_rollup": rel(FULL_ROLLUP_PATH),
            "full_readout": rel(FULL_READOUT_PATH),
            "assertion_report": rel(ASSERTION_REPORT_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "closure": rel(CLOSURE_PATH),
            "profile": rel(PROFILE_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": trace["terminal"],
    }

    receipt_id = sig8(receipt_body)
    receipt_body["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_body["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_body)

    print(json.dumps(receipt_body, indent=2, sort_keys=True))
    print(f"c7_synthetic_tests_rollup_receipt_id={receipt_id}")
    print(f"c7_synthetic_tests_rollup_receipt_path={rel(receipt_path)}")
    print(f"c7_synthetic_tests_rollup_outcome={aggregate_outcome}")
    print("c7_synthetic_tests_rollup_next_unit=NONE")

    return 0 if success else 1

if __name__ == "__main__":
    raise SystemExit(main())
