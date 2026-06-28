#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_CLOSURE_PACKET_AFTER_REENTRY_V0"
TARGET_UNIT_ID = "research.c8.runtime_adoption_surface.bounded_probe.closure_packet.after_reentry.v0"
MILESTONE = "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_PACKET_CREATED_AFTER_REENTRY"
OUTCOME = "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_PACKET_READY_FOR_HUMAN_DECISION"
STOP_CODE = "STOP_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_PACKET_READY_FOR_REVIEW"

SOURCE_EXEC_RECEIPT_ID = "c8_runtime_adoption_bounded_probe_execution_receipt_ed8c0509"
SOURCE_RESULT_ID = "c8_runtime_adoption_bounded_probe_result_a0ec0ebb"
SOURCE_EVIDENCE_ID = "c8_runtime_adoption_bounded_probe_evidence_9ad18624"
SOURCE_EXEC_BOUNDARY_ID = "c8_runtime_adoption_bounded_probe_execution_boundary_e35341b9"

SELECTED_SURFACE_ID = "c8_successor_surface_runtime_adoption_after_reentry_v0"
SELECTED_SURFACE_KIND = "RUNTIME_ADOPTION_SURFACE"
SELECTED_SURFACE_LABEL = "C8_RUNTIME_ADOPTION_AFTER_REUSE_AUTHORITY_CLOSURE_SURFACE"

PROBE_ID = "c8_runtime_adoption_surface_bounded_probe_after_reentry_v0"
PROBE_KIND = "RUNTIME_ADOPTION_BOUNDARY_PROBE"
PROBE_LABEL = "C8_RUNTIME_ADOPTION_BOUNDED_PROBE_AFTER_REENTRY"
PROBE_OUTPUT_CLASS = "RUNTIME_ADOPTION_BOUNDARY_PROBE_OBSERVED_NO_DEFECTS"

CLOSURE_CLASS = "RUNTIME_ADOPTION_BOUNDARY_PROBE_RESULT_REVIEWED_NO_DEFECTS"
RECOMMENDED_HUMAN_DECISION = "ACCEPT_CLOSURE_NO_NEW_AUTHORITY_RETURN_TO_SURFACE_SELECTION"

OUT_DIR = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_after_reentry_v0"
RECEIPT_DIR = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_after_reentry_v0_receipts"

EXEC_RECEIPT = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_after_reentry_v0_receipts/c8_runtime_adoption_bounded_probe_execution_receipt_ed8c0509.json"
PROBE_RESULT = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_after_reentry_v0/c8_runtime_adoption_bounded_probe_result_v0.json"
PROBE_EVIDENCE = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_after_reentry_v0/c8_runtime_adoption_bounded_probe_evidence_v0.json"
EXEC_BOUNDARY = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_after_reentry_v0/c8_runtime_adoption_bounded_probe_execution_boundary_audit_v0.json"
EXEC_REPORT = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_after_reentry_v0/c8_runtime_adoption_bounded_probe_execution_report.json"

CLOSURE_PACKET = OUT_DIR / "c8_runtime_adoption_bounded_probe_closure_packet_v0.json"
CLOSURE_OPTIONS = OUT_DIR / "c8_runtime_adoption_bounded_probe_closure_options_v0.json"
CLOSURE_AUDIT = OUT_DIR / "c8_runtime_adoption_bounded_probe_closure_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_runtime_adoption_bounded_probe_closure_readout_v0.json"
REPORT = OUT_DIR / "c8_runtime_adoption_bounded_probe_closure_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "next_surface_selected_count",
    "probe_prep_created_count",
    "probe_execution_authorized_count",
    "probe_executed_count",
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
    forbidden_counters = {k: 0 for k in FORBIDDEN_COUNTER_KEYS}

    sources = {
        "exec_receipt": EXEC_RECEIPT,
        "probe_result": PROBE_RESULT,
        "probe_evidence": PROBE_EVIDENCE,
        "exec_boundary": EXEC_BOUNDARY,
        "exec_report": EXEC_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    exec_receipt = read_json(EXEC_RECEIPT)
    probe_result = read_json(PROBE_RESULT)
    probe_evidence = read_json(PROBE_EVIDENCE)
    exec_boundary = read_json(EXEC_BOUNDARY)
    exec_report = read_json(EXEC_REPORT)
    summary = exec_receipt.get("machine_readable_probe_execution_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_EXECUTION_PASS",
        "outcome_class": "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_EXECUTED_RESULT_READY_FOR_REVIEW",
        "receipt_id": SOURCE_EXEC_RECEIPT_ID,
    }

    for key, want in expected_receipt.items():
        chk(failures, f"exec_receipt_{key}", exec_receipt.get(key), want)

    expected_summary = {
        "runtime_adoption_bounded_probe_execution_complete": True,
        "probe_output_class": PROBE_OUTPUT_CLASS,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "bounded_probe_executed": True,
        "bounded_probe_execution_count": 1,
        "typed_halts_observed_count": 2,
        "receipt_mismatch_count": 0,
        "projection_bug_count": 0,
        "missing_move_signal_count": 0,
        "gate_failure_count": 0,
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
        "recommended_review_unit": "REVIEW_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_RESULT_AFTER_REENTRY_V0",
        "next_command_goal": None,
    }

    for key, want in expected_summary.items():
        chk(failures, f"summary_{key}", summary.get(key), want)

    expected_result = {
        "runtime_adoption_bounded_probe_result_id": SOURCE_RESULT_ID,
        "probe_output_class": PROBE_OUTPUT_CLASS,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "bounded_probe_executed": True,
        "bounded_probe_execution_count": 1,
        "typed_halts_observed_count": 2,
        "receipt_mismatch_count": 0,
        "projection_bug_count": 0,
        "missing_move_signal_count": 0,
        "gate_failure_count": 0,
        "runtime_build_authorized_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
    }

    for key, want in expected_result.items():
        chk(failures, f"probe_result_{key}", probe_result.get(key), want)

    expected_evidence = {
        "runtime_adoption_bounded_probe_evidence_id": SOURCE_EVIDENCE_ID,
        "source_probe_result_id": SOURCE_RESULT_ID,
        "source_artifacts_mutated": False,
        "receipt_mismatches": [],
        "projection_bugs": [],
        "missing_move_signals": [],
        "gate_failures": [],
    }

    for key, want in expected_evidence.items():
        chk(failures, f"probe_evidence_{key}", probe_evidence.get(key), want)

    if len(probe_evidence.get("typed_halts_observed", [])) != 2:
        failures.append(f"typed_halts_observed_count_wrong:{len(probe_evidence.get('typed_halts_observed', []))}")

    expected_boundary = {
        "gate": "PASS",
        "runtime_adoption_bounded_probe_execution_boundary_audit_id": SOURCE_EXEC_BOUNDARY_ID,
        "source_probe_result_id": SOURCE_RESULT_ID,
        "source_probe_evidence_id": SOURCE_EVIDENCE_ID,
    }

    for key, want in expected_boundary.items():
        chk(failures, f"exec_boundary_{key}", exec_boundary.get(key), want)

    source_hashes_after = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    if source_hashes_before != source_hashes_after:
        forbidden_counters["source_artifact_mutation_count"] += 1

    local_nonzero = {k: v for k, v in forbidden_counters.items() if v != 0}
    for k, v in local_nonzero.items():
        failures.append(f"{k}:{v}")

    closure_options = {
        "schema_version": "c8_runtime_adoption_bounded_probe_closure_options_v0",
        "runtime_adoption_bounded_probe_closure_options_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "source_probe_result_id": SOURCE_RESULT_ID,
        "source_probe_evidence_id": SOURCE_EVIDENCE_ID,
        "source_probe_execution_receipt_id": SOURCE_EXEC_RECEIPT_ID,
        "closure_class": CLOSURE_CLASS,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "human_decision_options": [
            "ACCEPT_CLOSURE_NO_NEW_AUTHORITY_RETURN_TO_SURFACE_SELECTION",
            "REJECT_CLOSURE_REVIEW_RESULT_AGAIN",
            "REQUEST_FOLLOWUP_PROBE_PREP_PACKET",
        ],
        "decision_boundary": {
            "accept_closure_means": [
                "record runtime-adoption bounded probe result as reviewed clean",
                "close current runtime-adoption probe surface with no new authority",
                "allow later return-to-surface-selection packet after review",
            ],
            "accept_closure_does_not_mean": [
                "select next surface now",
                "authorize another probe now",
                "build runtime machinery now",
                "rerun C8 now",
                "promote reusable schema now",
            ],
        },
    }
    closure_options["runtime_adoption_bounded_probe_closure_options_id"] = "c8_runtime_adoption_bounded_probe_closure_options_" + sig8(closure_options)
    write_json(CLOSURE_OPTIONS, closure_options)

    closure_packet = {
        "schema_version": "c8_runtime_adoption_bounded_probe_closure_packet_v0",
        "runtime_adoption_bounded_probe_closure_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "closure_packet_status": "READY_FOR_HUMAN_DECISION",
        "closure_class": CLOSURE_CLASS,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "source_probe_execution_receipt_id": SOURCE_EXEC_RECEIPT_ID,
        "source_probe_result_id": SOURCE_RESULT_ID,
        "source_probe_evidence_id": SOURCE_EVIDENCE_ID,
        "source_probe_execution_boundary_id": SOURCE_EXEC_BOUNDARY_ID,
        "source_closure_options_id": closure_options["runtime_adoption_bounded_probe_closure_options_id"],
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_output_class": PROBE_OUTPUT_CLASS,
        "bounded_probe_executed": True,
        "bounded_probe_execution_count": 1,
        "typed_halts_observed_count": 2,
        "receipt_mismatch_count": 0,
        "projection_bug_count": 0,
        "missing_move_signal_count": 0,
        "gate_failure_count": 0,
        "closure_ready_for_human_decision": True,
        "current_surface_closed_now": False,
        "return_to_surface_selection_authorized_now": False,
        "next_surface_selected_now": False,
        "probe_prep_created_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
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
        "recommended_review_unit": "REVIEW_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_PACKET_AFTER_REENTRY_V0",
    }
    closure_packet["runtime_adoption_bounded_probe_closure_packet_id"] = "c8_runtime_adoption_bounded_probe_closure_packet_" + sig8(closure_packet)
    write_json(CLOSURE_PACKET, closure_packet)

    closure_audit = {
        "schema_version": "c8_runtime_adoption_bounded_probe_closure_boundary_audit_v0",
        "runtime_adoption_bounded_probe_closure_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_closure_packet_id": closure_packet["runtime_adoption_bounded_probe_closure_packet_id"],
        "source_closure_options_id": closure_options["runtime_adoption_bounded_probe_closure_options_id"],
        "source_probe_result_id": SOURCE_RESULT_ID,
        "allowed_now": {
            "create_closure_packet_for_review": True,
            "present_human_closure_decision_options": True,
        },
        "not_allowed_now": {
            "accept_closure": True,
            "return_to_surface_selection": True,
            "select_next_surface": True,
            "create_probe_prep_packet": True,
            "authorize_probe_execution": True,
            "execute_probe": True,
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
    closure_audit["runtime_adoption_bounded_probe_closure_boundary_audit_id"] = "c8_runtime_adoption_bounded_probe_closure_boundary_" + sig8(closure_audit)
    write_json(CLOSURE_AUDIT, closure_audit)

    gate_results = {
        "CLOSURE_PACKET_0_SOURCE_EXECUTION_RECEIPT_PASS": exec_receipt.get("gate") == "PASS",
        "CLOSURE_PACKET_1_RESULT_NO_DEFECTS": probe_result.get("probe_output_class") == PROBE_OUTPUT_CLASS,
        "CLOSURE_PACKET_2_COUNTS_CLEAN": all([
            probe_result.get("receipt_mismatch_count") == 0,
            probe_result.get("projection_bug_count") == 0,
            probe_result.get("missing_move_signal_count") == 0,
            probe_result.get("gate_failure_count") == 0,
        ]),
        "CLOSURE_PACKET_3_TYPED_HALTS_OBSERVED": probe_result.get("typed_halts_observed_count") == 2,
        "CLOSURE_PACKET_4_CLOSURE_PACKET_READY_FOR_DECISION": closure_packet["closure_ready_for_human_decision"] is True,
        "CLOSURE_PACKET_5_NO_CLOSURE_ACCEPTED_NOW": closure_packet["current_surface_closed_now"] is False,
        "CLOSURE_PACKET_6_NO_NEXT_SURFACE_OR_PROBE_NOW": closure_packet["next_surface_selected_now"] is False and closure_packet["probe_prep_created_now"] is False and closure_packet["probe_execution_authorized_now"] is False,
        "CLOSURE_PACKET_7_NO_BUILD_RERUN_SCHEMA": closure_packet["instrument_build_authorized_now"] is False and closure_packet["c8_rerun_authorized_now"] is False and closure_packet["reusable_schema_authorized_now"] is False,
        "CLOSURE_PACKET_8_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "CLOSURE_PACKET_9_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "CLOSURE_PACKET_10_REQUIRES_REVIEW": closure_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"closure_packet_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_PACKET_PASS" if gate == "PASS" else "TYPED_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_PACKET_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_PACKET_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_PACKET_FAILED"

    readout = {
        "schema_version": "c8_runtime_adoption_bounded_probe_closure_readout_v0",
        "title": "C8 runtime-adoption bounded probe closure packet after reentry",
        "status": status,
        "outcome_class": outcome,
        "closure_class": CLOSURE_CLASS,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "probe_id": PROBE_ID,
        "probe_output_class": PROBE_OUTPUT_CLASS,
        "bounded_probe_execution_count": 1,
        "typed_halts_observed_count": 2,
        "receipt_mismatch_count": 0,
        "projection_bug_count": 0,
        "missing_move_signal_count": 0,
        "gate_failure_count": 0,
        "closure_ready_for_human_decision": True,
        "current_surface_closed_now": False,
        "return_to_surface_selection_authorized_now": False,
        "next_surface_selected_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": closure_packet["recommended_review_unit"],
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_runtime_adoption_bounded_probe_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "closure_class": CLOSURE_CLASS,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "source_probe_execution_receipt_id": SOURCE_EXEC_RECEIPT_ID,
        "source_probe_result_id": SOURCE_RESULT_ID,
        "source_probe_evidence_id": SOURCE_EVIDENCE_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_output_class": PROBE_OUTPUT_CLASS,
        "bounded_probe_execution_count": 1,
        "typed_halts_observed_count": 2,
        "receipt_mismatch_count": 0,
        "projection_bug_count": 0,
        "missing_move_signal_count": 0,
        "gate_failure_count": 0,
        "closure_ready_for_human_decision": True,
        "current_surface_closed_now": False,
        "return_to_surface_selection_authorized_now": False,
        "next_surface_selected_now": False,
        "probe_prep_created_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "requires_review": True,
        "recommended_review_unit": closure_packet["recommended_review_unit"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_runtime_adoption_bounded_probe_closure_receipt_v0",
        "receipt_type": "TYPED_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_PACKET_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_closure_summary": {
            "runtime_adoption_bounded_probe_closure_packet_created": gate == "PASS",
            "closure_class": CLOSURE_CLASS,
            "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
            "source_probe_execution_receipt_id": SOURCE_EXEC_RECEIPT_ID,
            "source_probe_result_id": SOURCE_RESULT_ID,
            "source_probe_evidence_id": SOURCE_EVIDENCE_ID,
            "source_probe_execution_boundary_id": SOURCE_EXEC_BOUNDARY_ID,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "probe_label": PROBE_LABEL,
            "probe_output_class": PROBE_OUTPUT_CLASS,
            "bounded_probe_executed": True,
            "bounded_probe_execution_count": 1,
            "typed_halts_observed_count": 2,
            "receipt_mismatch_count": 0,
            "projection_bug_count": 0,
            "missing_move_signal_count": 0,
            "gate_failure_count": 0,
            "closure_ready_for_human_decision": True,
            "current_surface_closed_now": False,
            "return_to_surface_selection_authorized_now": False,
            "next_surface_selected_now": False,
            "probe_prep_created_now": False,
            "probe_execution_authorized_now": False,
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
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
            "forbidden_counters_zero": not bool(local_nonzero),
            "requires_review": True,
            "recommended_review_unit": closure_packet["recommended_review_unit"],
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
            "closure_packet": rel(CLOSURE_PACKET),
            "closure_options": rel(CLOSURE_OPTIONS),
            "closure_audit": rel(CLOSURE_AUDIT),
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

    receipt["receipt_id"] = "c8_runtime_adoption_bounded_probe_closure_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_adoption_bounded_probe_closure_receipt_id={receipt['receipt_id']}")
    print(f"runtime_adoption_bounded_probe_closure_receipt_path={rel(receipt_path)}")
    print(f"runtime_adoption_bounded_probe_closure_packet_path={rel(CLOSURE_PACKET)}")
    print(f"runtime_adoption_bounded_probe_closure_options_path={rel(CLOSURE_OPTIONS)}")
    print(f"runtime_adoption_bounded_probe_closure_boundary_path={rel(CLOSURE_AUDIT)}")
    print(f"closure_class={CLOSURE_CLASS}")
    print(f"recommended_human_decision={RECOMMENDED_HUMAN_DECISION}")
    print(f"selected_surface_id={SELECTED_SURFACE_ID}")
    print(f"selected_surface_kind={SELECTED_SURFACE_KIND}")
    print(f"probe_id={PROBE_ID}")
    print(f"probe_output_class={PROBE_OUTPUT_CLASS}")
    print("closure_ready_for_human_decision=true")
    print("current_surface_closed_now=false")
    print("return_to_surface_selection_authorized_now=false")
    print("next_surface_selected_now=false")
    print("probe_prep_created_now=false")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={closure_packet['recommended_review_unit']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
