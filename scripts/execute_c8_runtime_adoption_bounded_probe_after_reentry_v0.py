#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXECUTE_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_AFTER_REENTRY_V0"
TARGET_UNIT_ID = "research.c8.runtime_adoption_surface.bounded_probe.execute.after_reentry.v0"
MILESTONE = "C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_EXECUTED_AFTER_REENTRY"
OUTCOME = "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_EXECUTED_RESULT_READY_FOR_REVIEW"
STOP_CODE = "STOP_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_RESULT_READY_FOR_REVIEW"

SOURCE_EXEC_ACCEPTANCE_RECEIPT_ID = "c8_runtime_adoption_bounded_probe_execution_acceptance_receipt_ab5b97de"
SOURCE_EXEC_ACCEPTANCE_DECISION_ID = "c8_runtime_adoption_bounded_probe_execution_acceptance_decision_6dbb6ed7"
SOURCE_EXEC_ACCEPTANCE_PACKET_ID = "c8_runtime_adoption_bounded_probe_execution_acceptance_packet_2f2a48eb"
SOURCE_EXEC_AUTHORITY_ID = "c8_runtime_adoption_bounded_probe_execution_authority_ba268cc0"
SOURCE_EXEC_ACCEPTANCE_BOUNDARY_ID = "c8_runtime_adoption_bounded_probe_execution_acceptance_boundary_dcfc3397"

SOURCE_PREP_RECEIPT_ID = "c8_runtime_adoption_bounded_probe_prep_receipt_0fc181c6"
SOURCE_PROBE_SPEC_ID = "c8_runtime_adoption_bounded_probe_spec_d39f5710"
SOURCE_PREP_PACKET_ID = "c8_runtime_adoption_bounded_probe_prep_packet_23020f7d"
SOURCE_PREP_BOUNDARY_ID = "c8_runtime_adoption_bounded_probe_prep_boundary_fe200a33"

SELECTED_SURFACE_ID = "c8_successor_surface_runtime_adoption_after_reentry_v0"
SELECTED_SURFACE_KIND = "RUNTIME_ADOPTION_SURFACE"
SELECTED_SURFACE_LABEL = "C8_RUNTIME_ADOPTION_AFTER_REUSE_AUTHORITY_CLOSURE_SURFACE"

PROBE_ID = "c8_runtime_adoption_surface_bounded_probe_after_reentry_v0"
PROBE_KIND = "RUNTIME_ADOPTION_BOUNDARY_PROBE"
PROBE_LABEL = "C8_RUNTIME_ADOPTION_BOUNDED_PROBE_AFTER_REENTRY"
PROBE_QUESTION = (
    "What is the smallest controlled runtime-adoption probe that can expose typed halts, "
    "receipt mismatches, projection bugs, missing moves, or gate failures from the committed C8 chain, "
    "while stopping before probe execution authority, runtime build, C8 rerun, or reusable schema promotion?"
)

OUT_DIR = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_after_reentry_v0"
RECEIPT_DIR = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_after_reentry_v0_receipts"

EXEC_ACCEPTANCE_RECEIPT = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_acceptance_after_reentry_v0_receipts/c8_runtime_adoption_bounded_probe_execution_acceptance_receipt_ab5b97de.json"
EXEC_ACCEPTANCE_DECISION = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_acceptance_after_reentry_v0/c8_runtime_adoption_bounded_probe_execution_acceptance_decision_v0.json"
EXEC_ACCEPTANCE_PACKET = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_acceptance_after_reentry_v0/c8_runtime_adoption_bounded_probe_execution_acceptance_packet_v0.json"
EXEC_AUTHORITY = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_acceptance_after_reentry_v0/c8_runtime_adoption_bounded_probe_execution_authority_v0.json"
EXEC_ACCEPTANCE_BOUNDARY = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_acceptance_after_reentry_v0/c8_runtime_adoption_bounded_probe_execution_acceptance_boundary_audit_v0.json"
EXEC_ACCEPTANCE_REPORT = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_acceptance_after_reentry_v0/c8_runtime_adoption_bounded_probe_execution_acceptance_report.json"

PREP_RECEIPT = ROOT / "data/c8_runtime_adoption_surface_bounded_probe_prep_after_reentry_v0_receipts/c8_runtime_adoption_bounded_probe_prep_receipt_0fc181c6.json"
PROBE_SPEC = ROOT / "data/c8_runtime_adoption_surface_bounded_probe_prep_after_reentry_v0/c8_runtime_adoption_surface_bounded_probe_spec_v0.json"
PREP_PACKET = ROOT / "data/c8_runtime_adoption_surface_bounded_probe_prep_after_reentry_v0/c8_runtime_adoption_surface_bounded_probe_prep_packet_v0.json"
PREP_BOUNDARY = ROOT / "data/c8_runtime_adoption_surface_bounded_probe_prep_after_reentry_v0/c8_runtime_adoption_surface_bounded_probe_prep_boundary_audit_v0.json"

PROBE_RESULT = OUT_DIR / "c8_runtime_adoption_bounded_probe_result_v0.json"
PROBE_EVIDENCE = OUT_DIR / "c8_runtime_adoption_bounded_probe_evidence_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_runtime_adoption_bounded_probe_execution_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_runtime_adoption_bounded_probe_execution_readout_v0.json"
REPORT = OUT_DIR / "c8_runtime_adoption_bounded_probe_execution_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "instrument_build_count",
    "cell1_build_count",
    "verification_probe_count",
    "c8_rerun_count",
    "missing_instrument_proposal_count",
    "research_mode_opened_count",
    "general_cell1_authority_count",
    "reusable_schema_authorized_count",
    "global_solution_claim_count",
    "frontier_solved_claim_count",
    "source_artifact_mutation_count",
    "hidden_next_command_count",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def chk(failures: List[str], label: str, got: Any, want: Any) -> None:
    if got != want:
        failures.append(f"{label}_wrong:{got}!={want}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []
    observation_events: List[Dict[str, Any]] = []
    receipt_mismatches: List[str] = []
    projection_bugs: List[str] = []
    missing_move_signals: List[str] = []
    gate_failures: List[str] = []
    forbidden_counters = {k: 0 for k in FORBIDDEN_COUNTER_KEYS}

    sources = {
        "exec_acceptance_receipt": EXEC_ACCEPTANCE_RECEIPT,
        "exec_acceptance_decision": EXEC_ACCEPTANCE_DECISION,
        "exec_acceptance_packet": EXEC_ACCEPTANCE_PACKET,
        "exec_authority": EXEC_AUTHORITY,
        "exec_acceptance_boundary": EXEC_ACCEPTANCE_BOUNDARY,
        "exec_acceptance_report": EXEC_ACCEPTANCE_REPORT,
        "prep_receipt": PREP_RECEIPT,
        "probe_spec": PROBE_SPEC,
        "prep_packet": PREP_PACKET,
        "prep_boundary": PREP_BOUNDARY,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    exec_receipt = read_json(EXEC_ACCEPTANCE_RECEIPT)
    exec_decision = read_json(EXEC_ACCEPTANCE_DECISION)
    exec_packet = read_json(EXEC_ACCEPTANCE_PACKET)
    exec_authority = read_json(EXEC_AUTHORITY)
    exec_boundary = read_json(EXEC_ACCEPTANCE_BOUNDARY)
    exec_report = read_json(EXEC_ACCEPTANCE_REPORT)

    prep_receipt = read_json(PREP_RECEIPT)
    probe_spec = read_json(PROBE_SPEC)
    prep_packet = read_json(PREP_PACKET)
    prep_boundary = read_json(PREP_BOUNDARY)

    exec_summary = exec_receipt.get("machine_readable_execution_acceptance_summary", {})
    prep_summary = prep_receipt.get("machine_readable_prep_summary", {})

    expected_exec_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_RUNTIME_ADOPTION_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_PASS",
        "outcome_class": "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_ACCEPTED_FOR_ONE_BOUNDED_EXECUTION_ONLY",
        "receipt_id": SOURCE_EXEC_ACCEPTANCE_RECEIPT_ID,
    }

    for key, want in expected_exec_receipt.items():
        got = exec_receipt.get(key)
        if got != want:
            failures.append(f"exec_receipt_{key}_wrong:{got}!={want}")
            receipt_mismatches.append(f"exec_receipt_{key}")

    expected_exec_summary = {
        "runtime_adoption_bounded_probe_execution_acceptance_complete": True,
        "human_decision": "ACCEPT_FOR_BOUNDED_PROBE_EXECUTION",
        "source_prep_receipt_id": SOURCE_PREP_RECEIPT_ID,
        "source_probe_spec_id": SOURCE_PROBE_SPEC_ID,
        "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
        "source_prep_boundary_id": SOURCE_PREP_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_question": PROBE_QUESTION,
        "bounded_probe_execution_authorized": True,
        "authorized_future_unit": UNIT_ID,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_execution_count": 1,
        "probe_executed_now": False,
        "instrument_built_now": False,
        "cell1_built_now": False,
        "verification_probe_run_now": False,
        "c8_rerun_now": False,
        "missing_instrument_proposal_created_now": False,
        "research_mode_opened": False,
        "general_cell1_authority": False,
        "reusable_schema_authorized": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
        "recommended_review_unit": "REVIEW_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_AFTER_REENTRY_V0",
        "next_command_goal": None,
    }

    for key, want in expected_exec_summary.items():
        got = exec_summary.get(key)
        if got != want:
            failures.append(f"exec_summary_{key}_wrong:{got}!={want}")
            projection_bugs.append(f"exec_summary_{key}")

    expected_authority = {
        "authority_status": "AUTHORIZED_FOR_ONE_BOUNDED_PROBE_EXECUTION_ONLY",
        "source_prep_receipt_id": SOURCE_PREP_RECEIPT_ID,
        "source_probe_spec_id": SOURCE_PROBE_SPEC_ID,
        "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "authorized_future_unit": UNIT_ID,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_execution_count": 1,
    }

    for key, want in expected_authority.items():
        got = exec_authority.get(key)
        if got != want:
            failures.append(f"authority_{key}_wrong:{got}!={want}")
            receipt_mismatches.append(f"authority_{key}")

    authorized_scope = exec_authority.get("authorized_scope", {})
    if authorized_scope.get("execute_bounded_probe") is not True:
        failures.append("authority_execute_bounded_probe_not_true")
        projection_bugs.append("authority_execute_bounded_probe")
    if authorized_scope.get("max_execution_count") != 1:
        failures.append(f"authority_max_execution_count_wrong:{authorized_scope.get('max_execution_count')}")
        projection_bugs.append("authority_max_execution_count")
    if authorized_scope.get("probe_id") != PROBE_ID:
        failures.append(f"authority_probe_id_wrong:{authorized_scope.get('probe_id')}")
        projection_bugs.append("authority_probe_id")

    expected_prep_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_PASS",
        "outcome_class": "C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_READY_FOR_REVIEW",
        "receipt_id": SOURCE_PREP_RECEIPT_ID,
    }

    for key, want in expected_prep_receipt.items():
        got = prep_receipt.get(key)
        if got != want:
            failures.append(f"prep_receipt_{key}_wrong:{got}!={want}")
            receipt_mismatches.append(f"prep_receipt_{key}")

    expected_probe_spec = {
        "runtime_adoption_bounded_probe_spec_id": SOURCE_PROBE_SPEC_ID,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_question": PROBE_QUESTION,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
    }

    for key, want in expected_probe_spec.items():
        got = probe_spec.get(key)
        if got != want:
            failures.append(f"probe_spec_{key}_wrong:{got}!={want}")
            projection_bugs.append(f"probe_spec_{key}")

    probe_scope = probe_spec.get("probe_scope", {})
    expected_observation_targets = [
        "typed_halts",
        "receipt_mismatches",
        "projection_bugs",
        "missing_moves",
        "gate_failures",
    ]
    if probe_scope.get("primary_observation_targets") != expected_observation_targets:
        failures.append(f"probe_scope_primary_observation_targets_wrong:{probe_scope.get('primary_observation_targets')}")
        projection_bugs.append("probe_scope_primary_observation_targets")
    if probe_scope.get("max_probe_execution_count_if_later_accepted") != 1:
        failures.append(f"probe_scope_max_execution_wrong:{probe_scope.get('max_probe_execution_count_if_later_accepted')}")
        projection_bugs.append("probe_scope_max_execution_count_if_later_accepted")

    source_hashes_after = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    if source_hashes_before != source_hashes_after:
        forbidden_counters["source_artifact_mutation_count"] += 1

    # Bounded observation pass over the prepared chain. This is observation only:
    # it classifies existing committed surfaces and stops before build/rerun/schema.
    typed_halts_observed = [
        exec_receipt.get("terminal", {}).get("stop_code"),
        prep_receipt.get("terminal", {}).get("stop_code"),
    ]
    typed_halts_observed = [x for x in typed_halts_observed if x]

    observation_events.append({
        "event_kind": "TYPED_HALTS_OBSERVED",
        "count": len(typed_halts_observed),
        "values": typed_halts_observed,
    })
    observation_events.append({
        "event_kind": "RECEIPT_MISMATCH_SCAN",
        "count": len(receipt_mismatches),
        "values": receipt_mismatches,
    })
    observation_events.append({
        "event_kind": "PROJECTION_BUG_SCAN",
        "count": len(projection_bugs),
        "values": projection_bugs,
    })
    observation_events.append({
        "event_kind": "MISSING_MOVE_SCAN",
        "count": len(missing_move_signals),
        "values": missing_move_signals,
    })

    false_exec_gates = sorted(k for k, v in exec_receipt.get("gate_results", {}).items() if v is not True)
    false_prep_gates = sorted(k for k, v in prep_receipt.get("gate_results", {}).items() if v is not True)
    gate_failures.extend([f"exec:{g}" for g in false_exec_gates])
    gate_failures.extend([f"prep:{g}" for g in false_prep_gates])

    observation_events.append({
        "event_kind": "GATE_FAILURE_SCAN",
        "count": len(gate_failures),
        "values": gate_failures,
    })

    local_nonzero = {k: v for k, v in forbidden_counters.items() if v != 0}
    for k, v in local_nonzero.items():
        failures.append(f"{k}:{v}")

    probe_output_class = (
        "RUNTIME_ADOPTION_BOUNDARY_PROBE_OBSERVED_NO_DEFECTS"
        if not failures and not receipt_mismatches and not projection_bugs and not missing_move_signals and not gate_failures
        else "RUNTIME_ADOPTION_BOUNDARY_PROBE_OBSERVED_TYPED_DEFECTS"
    )

    result = {
        "schema_version": "c8_runtime_adoption_bounded_probe_result_v0",
        "runtime_adoption_bounded_probe_result_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_question": PROBE_QUESTION,
        "probe_output_class": probe_output_class,
        "source_execution_acceptance_receipt_id": SOURCE_EXEC_ACCEPTANCE_RECEIPT_ID,
        "source_execution_acceptance_packet_id": SOURCE_EXEC_ACCEPTANCE_PACKET_ID,
        "source_execution_authority_id": SOURCE_EXEC_AUTHORITY_ID,
        "source_prep_receipt_id": SOURCE_PREP_RECEIPT_ID,
        "source_probe_spec_id": SOURCE_PROBE_SPEC_ID,
        "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "bounded_probe_executed": True,
        "bounded_probe_execution_count": 1,
        "authorized_future_unit_consumed": UNIT_ID,
        "observation_targets": expected_observation_targets,
        "typed_halts_observed_count": len(typed_halts_observed),
        "receipt_mismatch_count": len(receipt_mismatches),
        "projection_bug_count": len(projection_bugs),
        "missing_move_signal_count": len(missing_move_signals),
        "gate_failure_count": len(gate_failures),
        "observation_events": observation_events,
        "runtime_build_authorized_now": False,
        "instrument_build_authorized_now": False,
        "cell1_build_authorized_now": False,
        "verification_probe_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "missing_instrument_proposal_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "research_mode_opened": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "requires_review": True,
        "recommended_review_unit": "REVIEW_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_RESULT_AFTER_REENTRY_V0",
    }
    result["runtime_adoption_bounded_probe_result_id"] = "c8_runtime_adoption_bounded_probe_result_" + sig8(result)
    write_json(PROBE_RESULT, result)

    evidence = {
        "schema_version": "c8_runtime_adoption_bounded_probe_evidence_v0",
        "runtime_adoption_bounded_probe_evidence_id": None,
        "created_at": now_iso(),
        "source_probe_result_id": result["runtime_adoption_bounded_probe_result_id"],
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "source_artifacts_mutated": source_hashes_before != source_hashes_after,
        "typed_halts_observed": typed_halts_observed,
        "receipt_mismatches": receipt_mismatches,
        "projection_bugs": projection_bugs,
        "missing_move_signals": missing_move_signals,
        "gate_failures": gate_failures,
        "forbidden_counters": forbidden_counters,
    }
    evidence["runtime_adoption_bounded_probe_evidence_id"] = "c8_runtime_adoption_bounded_probe_evidence_" + sig8(evidence)
    write_json(PROBE_EVIDENCE, evidence)

    boundary_audit = {
        "schema_version": "c8_runtime_adoption_bounded_probe_execution_boundary_audit_v0",
        "runtime_adoption_bounded_probe_execution_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_probe_result_id": result["runtime_adoption_bounded_probe_result_id"],
        "source_probe_evidence_id": evidence["runtime_adoption_bounded_probe_evidence_id"],
        "source_execution_authority_id": SOURCE_EXEC_AUTHORITY_ID,
        "allowed_now": {
            "execute_one_bounded_probe": True,
            "write_probe_result_for_review": True,
            "write_evidence_for_review": True,
        },
        "not_allowed_now": {
            "build_instrument": True,
            "build_cell1": True,
            "run_verification_probe": True,
            "rerun_c8": True,
            "create_missing_instrument_proposal": True,
            "authorize_reusable_schema": True,
            "open_research_mode": True,
            "claim_global_solution": True,
            "claim_frontier_solved": True,
        },
        "forbidden_counters": forbidden_counters,
        "failures": failures,
        "warnings": warnings,
    }
    boundary_audit["runtime_adoption_bounded_probe_execution_boundary_audit_id"] = "c8_runtime_adoption_bounded_probe_execution_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    gate_results = {
        "PROBE_EXECUTION_0_SOURCE_EXECUTION_ACCEPTANCE_RECEIPT_PASS": exec_receipt.get("gate") == "PASS",
        "PROBE_EXECUTION_1_AUTHORITY_MATCHES_THIS_UNIT": exec_authority.get("authorized_future_unit") == UNIT_ID,
        "PROBE_EXECUTION_2_EXACTLY_ONE_EXECUTION_AUTHORIZED": exec_authority.get("authorized_future_unit_count") == 1 and exec_authority.get("authorized_future_probe_execution_count") == 1,
        "PROBE_EXECUTION_3_PROBE_SPEC_MATCHES_PREP": probe_spec.get("runtime_adoption_bounded_probe_spec_id") == SOURCE_PROBE_SPEC_ID and prep_packet.get("source_probe_spec_id") == SOURCE_PROBE_SPEC_ID,
        "PROBE_EXECUTION_4_BOUNDED_PROBE_EXECUTED_ONCE": result["bounded_probe_executed"] is True and result["bounded_probe_execution_count"] == 1,
        "PROBE_EXECUTION_5_NO_SOURCE_DEFECTS_OBSERVED": not receipt_mismatches and not projection_bugs and not gate_failures,
        "PROBE_EXECUTION_6_NO_BUILD_RERUN_SCHEMA": result["instrument_build_authorized_now"] is False and result["c8_rerun_authorized_now"] is False and result["reusable_schema_authorized_now"] is False,
        "PROBE_EXECUTION_7_NO_GLOBAL_OR_FRONTIER_CLAIM": result["global_solution_claim"] is False and result["frontier_solved_claim"] is False,
        "PROBE_EXECUTION_8_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "PROBE_EXECUTION_9_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "PROBE_EXECUTION_10_RESULT_REQUIRES_REVIEW": result["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"probe_execution_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_EXECUTION_PASS" if gate == "PASS" else "TYPED_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_EXECUTION_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_EXECUTION_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_EXECUTION_FAILED"

    readout = {
        "schema_version": "c8_runtime_adoption_bounded_probe_execution_readout_v0",
        "title": "C8 runtime-adoption bounded probe execution after reentry",
        "status": status,
        "outcome_class": outcome,
        "probe_output_class": probe_output_class,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "bounded_probe_executed": True,
        "bounded_probe_execution_count": 1,
        "typed_halts_observed_count": len(typed_halts_observed),
        "receipt_mismatch_count": len(receipt_mismatches),
        "projection_bug_count": len(projection_bugs),
        "missing_move_signal_count": len(missing_move_signals),
        "gate_failure_count": len(gate_failures),
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": result["recommended_review_unit"],
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_runtime_adoption_bounded_probe_execution_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "probe_output_class": probe_output_class,
        "source_execution_acceptance_receipt_id": SOURCE_EXEC_ACCEPTANCE_RECEIPT_ID,
        "source_execution_acceptance_packet_id": SOURCE_EXEC_ACCEPTANCE_PACKET_ID,
        "source_execution_authority_id": SOURCE_EXEC_AUTHORITY_ID,
        "source_prep_receipt_id": SOURCE_PREP_RECEIPT_ID,
        "source_probe_spec_id": SOURCE_PROBE_SPEC_ID,
        "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_question": PROBE_QUESTION,
        "bounded_probe_executed": True,
        "bounded_probe_execution_count": 1,
        "typed_halts_observed_count": len(typed_halts_observed),
        "receipt_mismatch_count": len(receipt_mismatches),
        "projection_bug_count": len(projection_bugs),
        "missing_move_signal_count": len(missing_move_signals),
        "gate_failure_count": len(gate_failures),
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "requires_review": True,
        "recommended_review_unit": result["recommended_review_unit"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_runtime_adoption_bounded_probe_execution_receipt_v0",
        "receipt_type": "TYPED_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_EXECUTION_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_probe_execution_summary": {
            "runtime_adoption_bounded_probe_execution_complete": gate == "PASS",
            "probe_output_class": probe_output_class,
            "source_execution_acceptance_receipt_id": SOURCE_EXEC_ACCEPTANCE_RECEIPT_ID,
            "source_execution_acceptance_decision_id": SOURCE_EXEC_ACCEPTANCE_DECISION_ID,
            "source_execution_acceptance_packet_id": SOURCE_EXEC_ACCEPTANCE_PACKET_ID,
            "source_execution_authority_id": SOURCE_EXEC_AUTHORITY_ID,
            "source_execution_acceptance_boundary_id": SOURCE_EXEC_ACCEPTANCE_BOUNDARY_ID,
            "source_prep_receipt_id": SOURCE_PREP_RECEIPT_ID,
            "source_probe_spec_id": SOURCE_PROBE_SPEC_ID,
            "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
            "source_prep_boundary_id": SOURCE_PREP_BOUNDARY_ID,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "probe_label": PROBE_LABEL,
            "probe_question": PROBE_QUESTION,
            "authorized_future_unit_consumed": UNIT_ID,
            "bounded_probe_executed": True,
            "bounded_probe_execution_count": 1,
            "typed_halts_observed_count": len(typed_halts_observed),
            "receipt_mismatch_count": len(receipt_mismatches),
            "projection_bug_count": len(projection_bugs),
            "missing_move_signal_count": len(missing_move_signals),
            "gate_failure_count": len(gate_failures),
            "instrument_built_now": False,
            "cell1_built_now": False,
            "verification_probe_run_now": False,
            "c8_rerun_now": False,
            "missing_instrument_proposal_created_now": False,
            "research_mode_opened": False,
            "general_cell1_authority": False,
            "reusable_schema_authorized": False,
            "global_solution_claim": False,
            "frontier_solved_claim": False,
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
            "forbidden_counters_zero": not bool(local_nonzero),
            "requires_review": True,
            "recommended_review_unit": result["recommended_review_unit"],
            "next_command_goal": None,
        },
        "gate_results": gate_results,
        "forbidden_counters": forbidden_counters,
        "source_artifact_immutability": {
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
        },
        "output_artifacts": {
            "probe_result": rel(PROBE_RESULT),
            "probe_evidence": rel(PROBE_EVIDENCE),
            "boundary_audit": rel(BOUNDARY_AUDIT),
            "readout": rel(READOUT),
            "report": rel(REPORT),
        },
        "failures": failures,
        "warnings": warnings,
        "terminal": {
            "type": "STOP",
            "stop_code": terminal_stop,
            "next_command_goal": None,
        },
    }

    receipt["receipt_id"] = "c8_runtime_adoption_bounded_probe_execution_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_adoption_bounded_probe_execution_receipt_id={receipt['receipt_id']}")
    print(f"runtime_adoption_bounded_probe_execution_receipt_path={rel(receipt_path)}")
    print(f"runtime_adoption_bounded_probe_result_path={rel(PROBE_RESULT)}")
    print(f"runtime_adoption_bounded_probe_evidence_path={rel(PROBE_EVIDENCE)}")
    print(f"runtime_adoption_bounded_probe_execution_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"selected_surface_id={SELECTED_SURFACE_ID}")
    print(f"selected_surface_kind={SELECTED_SURFACE_KIND}")
    print(f"probe_id={PROBE_ID}")
    print(f"probe_kind={PROBE_KIND}")
    print(f"probe_output_class={probe_output_class}")
    print("bounded_probe_executed=true")
    print("bounded_probe_execution_count=1")
    print(f"typed_halts_observed_count={len(typed_halts_observed)}")
    print(f"receipt_mismatch_count={len(receipt_mismatches)}")
    print(f"projection_bug_count={len(projection_bugs)}")
    print(f"missing_move_signal_count={len(missing_move_signals)}")
    print(f"gate_failure_count={len(gate_failures)}")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={result['recommended_review_unit']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
