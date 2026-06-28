#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_NO_NEW_AUTHORITY_AFTER_REENTRY_V0"
TARGET_UNIT_ID = "research.c8.runtime_adoption_surface.bounded_probe.closure_acceptance.no_new_authority.after_reentry.v0"
MILESTONE = "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_ACCEPTED_NO_NEW_AUTHORITY_AFTER_REENTRY"
OUTCOME = "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSED_NO_NEW_AUTHORITY_RETURN_TO_SURFACE_SELECTION_ALLOWED"
STOP_CODE = "STOP_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_ACCEPTANCE_READY_FOR_REVIEW"

HUMAN_DECISION = "ACCEPT_CLOSURE_NO_NEW_AUTHORITY_RETURN_TO_SURFACE_SELECTION"
AUTHORIZED_FUTURE_UNIT = "CREATE_C8_RETURN_TO_SURFACE_SELECTION_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

SOURCE_CLOSURE_RECEIPT_ID = "c8_runtime_adoption_bounded_probe_closure_receipt_11e2b2ad"
SOURCE_CLOSURE_PACKET_ID = "c8_runtime_adoption_bounded_probe_closure_packet_36c8c6d3"
SOURCE_CLOSURE_OPTIONS_ID = "c8_runtime_adoption_bounded_probe_closure_options_e4874557"
SOURCE_CLOSURE_BOUNDARY_ID = "c8_runtime_adoption_bounded_probe_closure_boundary_579632d6"

SOURCE_EXECUTION_RECEIPT_ID = "c8_runtime_adoption_bounded_probe_execution_receipt_ed8c0509"
SOURCE_RESULT_ID = "c8_runtime_adoption_bounded_probe_result_a0ec0ebb"
SOURCE_EVIDENCE_ID = "c8_runtime_adoption_bounded_probe_evidence_9ad18624"
SOURCE_EXECUTION_BOUNDARY_ID = "c8_runtime_adoption_bounded_probe_execution_boundary_e35341b9"

SELECTED_SURFACE_ID = "c8_successor_surface_runtime_adoption_after_reentry_v0"
SELECTED_SURFACE_KIND = "RUNTIME_ADOPTION_SURFACE"
SELECTED_SURFACE_LABEL = "C8_RUNTIME_ADOPTION_AFTER_REUSE_AUTHORITY_CLOSURE_SURFACE"

PROBE_ID = "c8_runtime_adoption_surface_bounded_probe_after_reentry_v0"
PROBE_KIND = "RUNTIME_ADOPTION_BOUNDARY_PROBE"
PROBE_LABEL = "C8_RUNTIME_ADOPTION_BOUNDED_PROBE_AFTER_REENTRY"
PROBE_OUTPUT_CLASS = "RUNTIME_ADOPTION_BOUNDARY_PROBE_OBSERVED_NO_DEFECTS"
CLOSURE_CLASS = "RUNTIME_ADOPTION_BOUNDARY_PROBE_RESULT_REVIEWED_NO_DEFECTS"

OUT_DIR = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_acceptance_after_reentry_v0"
RECEIPT_DIR = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_acceptance_after_reentry_v0_receipts"

CLOSURE_RECEIPT = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_after_reentry_v0_receipts/c8_runtime_adoption_bounded_probe_closure_receipt_11e2b2ad.json"
CLOSURE_PACKET = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_after_reentry_v0/c8_runtime_adoption_bounded_probe_closure_packet_v0.json"
CLOSURE_OPTIONS = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_after_reentry_v0/c8_runtime_adoption_bounded_probe_closure_options_v0.json"
CLOSURE_AUDIT = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_after_reentry_v0/c8_runtime_adoption_bounded_probe_closure_boundary_audit_v0.json"
CLOSURE_REPORT = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_after_reentry_v0/c8_runtime_adoption_bounded_probe_closure_report.json"

ACCEPTANCE_DECISION = OUT_DIR / "c8_runtime_adoption_bounded_probe_closure_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = OUT_DIR / "c8_runtime_adoption_bounded_probe_closure_acceptance_packet_v0.json"
FINAL_CLOSURE = OUT_DIR / "c8_runtime_adoption_bounded_probe_final_closure_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_runtime_adoption_bounded_probe_closure_acceptance_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_runtime_adoption_bounded_probe_closure_acceptance_readout_v0.json"
REPORT = OUT_DIR / "c8_runtime_adoption_bounded_probe_closure_acceptance_report.json"

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
        "closure_receipt": CLOSURE_RECEIPT,
        "closure_packet": CLOSURE_PACKET,
        "closure_options": CLOSURE_OPTIONS,
        "closure_audit": CLOSURE_AUDIT,
        "closure_report": CLOSURE_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    closure_receipt = read_json(CLOSURE_RECEIPT)
    closure_packet = read_json(CLOSURE_PACKET)
    closure_options = read_json(CLOSURE_OPTIONS)
    closure_audit = read_json(CLOSURE_AUDIT)
    closure_report = read_json(CLOSURE_REPORT)
    closure_summary = closure_receipt.get("machine_readable_closure_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_PACKET_PASS",
        "outcome_class": "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_PACKET_READY_FOR_HUMAN_DECISION",
        "receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
    }

    for key, want in expected_receipt.items():
        chk(failures, f"closure_receipt_{key}", closure_receipt.get(key), want)

    expected_summary = {
        "runtime_adoption_bounded_probe_closure_packet_created": True,
        "closure_class": CLOSURE_CLASS,
        "recommended_human_decision": HUMAN_DECISION,
        "source_probe_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
        "source_probe_result_id": SOURCE_RESULT_ID,
        "source_probe_evidence_id": SOURCE_EVIDENCE_ID,
        "source_probe_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
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
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
        "recommended_review_unit": "REVIEW_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_PACKET_AFTER_REENTRY_V0",
        "next_command_goal": None,
    }

    for key, want in expected_summary.items():
        chk(failures, f"closure_summary_{key}", closure_summary.get(key), want)

    expected_packet = {
        "runtime_adoption_bounded_probe_closure_packet_id": SOURCE_CLOSURE_PACKET_ID,
        "closure_packet_status": "READY_FOR_HUMAN_DECISION",
        "closure_class": CLOSURE_CLASS,
        "recommended_human_decision": HUMAN_DECISION,
        "source_probe_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
        "source_probe_result_id": SOURCE_RESULT_ID,
        "source_probe_evidence_id": SOURCE_EVIDENCE_ID,
        "source_probe_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_output_class": PROBE_OUTPUT_CLASS,
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
        "requires_review": True,
    }

    for key, want in expected_packet.items():
        chk(failures, f"closure_packet_{key}", closure_packet.get(key), want)

    expected_options = [
        "ACCEPT_CLOSURE_NO_NEW_AUTHORITY_RETURN_TO_SURFACE_SELECTION",
        "REJECT_CLOSURE_REVIEW_RESULT_AGAIN",
        "REQUEST_FOLLOWUP_PROBE_PREP_PACKET",
    ]

    chk(failures, "closure_options_id", closure_options.get("runtime_adoption_bounded_probe_closure_options_id"), SOURCE_CLOSURE_OPTIONS_ID)
    if closure_options.get("human_decision_options") != expected_options:
        failures.append(f"closure_options_wrong:{closure_options.get('human_decision_options')}")
    if HUMAN_DECISION not in closure_options.get("human_decision_options", []):
        failures.append(f"human_decision_not_available:{HUMAN_DECISION}")

    chk(failures, "closure_audit_id", closure_audit.get("runtime_adoption_bounded_probe_closure_boundary_audit_id"), SOURCE_CLOSURE_BOUNDARY_ID)
    chk(failures, "closure_audit_gate", closure_audit.get("gate"), "PASS")

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

    acceptance_decision = {
        "schema_version": "c8_runtime_adoption_bounded_probe_closure_acceptance_decision_v0",
        "runtime_adoption_bounded_probe_closure_acceptance_decision_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "human_decision": HUMAN_DECISION,
        "human_decision_consumed": True,
        "source_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "source_closure_packet_id": SOURCE_CLOSURE_PACKET_ID,
        "source_closure_options_id": SOURCE_CLOSURE_OPTIONS_ID,
        "source_closure_boundary_id": SOURCE_CLOSURE_BOUNDARY_ID,
        "source_probe_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
        "source_probe_result_id": SOURCE_RESULT_ID,
        "source_probe_evidence_id": SOURCE_EVIDENCE_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_output_class": PROBE_OUTPUT_CLASS,
        "closure_class": CLOSURE_CLASS,
        "current_surface_closed": True,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed_after_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
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
    }
    acceptance_decision["runtime_adoption_bounded_probe_closure_acceptance_decision_id"] = "c8_runtime_adoption_bounded_probe_closure_acceptance_decision_" + sig8(acceptance_decision)
    write_json(ACCEPTANCE_DECISION, acceptance_decision)

    final_closure = {
        "schema_version": "c8_runtime_adoption_bounded_probe_final_closure_v0",
        "runtime_adoption_bounded_probe_final_closure_id": None,
        "created_at": now_iso(),
        "closure_status": "CLOSED_NO_NEW_AUTHORITY",
        "source_closure_acceptance_decision_id": acceptance_decision["runtime_adoption_bounded_probe_closure_acceptance_decision_id"],
        "source_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "source_closure_packet_id": SOURCE_CLOSURE_PACKET_ID,
        "source_probe_result_id": SOURCE_RESULT_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_output_class": PROBE_OUTPUT_CLASS,
        "current_surface_closed": True,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed_after_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "next_surface_selected_now": False,
        "probe_prep_created_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
    }
    final_closure["runtime_adoption_bounded_probe_final_closure_id"] = "c8_runtime_adoption_bounded_probe_final_closure_" + sig8(final_closure)
    write_json(FINAL_CLOSURE, final_closure)

    acceptance_packet = {
        "schema_version": "c8_runtime_adoption_bounded_probe_closure_acceptance_packet_v0",
        "runtime_adoption_bounded_probe_closure_acceptance_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "acceptance_status": "CLOSURE_ACCEPTED_NO_NEW_AUTHORITY",
        "human_decision": HUMAN_DECISION,
        "source_closure_acceptance_decision_id": acceptance_decision["runtime_adoption_bounded_probe_closure_acceptance_decision_id"],
        "source_final_closure_id": final_closure["runtime_adoption_bounded_probe_final_closure_id"],
        "source_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "source_closure_packet_id": SOURCE_CLOSURE_PACKET_ID,
        "source_closure_options_id": SOURCE_CLOSURE_OPTIONS_ID,
        "source_closure_boundary_id": SOURCE_CLOSURE_BOUNDARY_ID,
        "source_probe_result_id": SOURCE_RESULT_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_output_class": PROBE_OUTPUT_CLASS,
        "closure_class": CLOSURE_CLASS,
        "current_surface_closed": True,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed_after_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "return_to_surface_selection_packet_created_now": False,
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
        "recommended_review_unit": "REVIEW_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_ACCEPTANCE_AFTER_REENTRY_V0",
    }
    acceptance_packet["runtime_adoption_bounded_probe_closure_acceptance_packet_id"] = "c8_runtime_adoption_bounded_probe_closure_acceptance_packet_" + sig8(acceptance_packet)
    write_json(ACCEPTANCE_PACKET, acceptance_packet)

    boundary_audit = {
        "schema_version": "c8_runtime_adoption_bounded_probe_closure_acceptance_boundary_audit_v0",
        "runtime_adoption_bounded_probe_closure_acceptance_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_closure_acceptance_decision_id": acceptance_decision["runtime_adoption_bounded_probe_closure_acceptance_decision_id"],
        "source_closure_acceptance_packet_id": acceptance_packet["runtime_adoption_bounded_probe_closure_acceptance_packet_id"],
        "source_final_closure_id": final_closure["runtime_adoption_bounded_probe_final_closure_id"],
        "source_closure_packet_id": SOURCE_CLOSURE_PACKET_ID,
        "source_closure_options_id": SOURCE_CLOSURE_OPTIONS_ID,
        "allowed_now": {
            "accept_closure": True,
            "record_final_closure_no_new_authority": True,
            "allow_return_to_surface_selection_after_review": True,
        },
        "not_allowed_now": {
            "create_return_to_surface_selection_packet_now": True,
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
    boundary_audit["runtime_adoption_bounded_probe_closure_acceptance_boundary_audit_id"] = "c8_runtime_adoption_bounded_probe_closure_acceptance_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    gate_results = {
        "CLOSURE_ACCEPTANCE_0_SOURCE_CLOSURE_RECEIPT_PASS": closure_receipt.get("gate") == "PASS",
        "CLOSURE_ACCEPTANCE_1_HUMAN_DECISION_AVAILABLE": HUMAN_DECISION in closure_options.get("human_decision_options", []),
        "CLOSURE_ACCEPTANCE_2_CLOSURE_PACKET_READY": closure_packet.get("closure_ready_for_human_decision") is True,
        "CLOSURE_ACCEPTANCE_3_ACCEPTED_NO_NEW_AUTHORITY": acceptance_packet["current_surface_closed"] is True and acceptance_packet["closed_with_no_new_authority"] is True,
        "CLOSURE_ACCEPTANCE_4_RETURN_TO_SELECTION_ALLOWED_AFTER_REVIEW_ONLY": acceptance_packet["return_to_surface_selection_allowed_after_review"] is True and acceptance_packet["return_to_surface_selection_packet_created_now"] is False,
        "CLOSURE_ACCEPTANCE_5_NO_NEXT_SURFACE_OR_PROBE_NOW": acceptance_packet["next_surface_selected_now"] is False and acceptance_packet["probe_prep_created_now"] is False and acceptance_packet["probe_execution_authorized_now"] is False and acceptance_packet["probe_executed_now"] is False,
        "CLOSURE_ACCEPTANCE_6_NO_BUILD_RERUN_SCHEMA": acceptance_packet["instrument_build_authorized_now"] is False and acceptance_packet["c8_rerun_authorized_now"] is False and acceptance_packet["reusable_schema_authorized_now"] is False,
        "CLOSURE_ACCEPTANCE_7_NO_GLOBAL_OR_FRONTIER_CLAIM": acceptance_packet["global_solution_claim"] is False and acceptance_packet["frontier_solved_claim"] is False,
        "CLOSURE_ACCEPTANCE_8_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "CLOSURE_ACCEPTANCE_9_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "CLOSURE_ACCEPTANCE_10_REQUIRES_REVIEW": acceptance_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"closure_acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_ACCEPTANCE_PASS" if gate == "PASS" else "TYPED_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_ACCEPTANCE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_ACCEPTANCE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_ACCEPTANCE_FAILED"

    readout = {
        "schema_version": "c8_runtime_adoption_bounded_probe_closure_acceptance_readout_v0",
        "title": "C8 runtime-adoption bounded probe closure acceptance after reentry",
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "closure_class": CLOSURE_CLASS,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "probe_id": PROBE_ID,
        "probe_output_class": PROBE_OUTPUT_CLASS,
        "current_surface_closed": True,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed_after_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "return_to_surface_selection_packet_created_now": False,
        "next_surface_selected_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": acceptance_packet["recommended_review_unit"],
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_runtime_adoption_bounded_probe_closure_acceptance_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "source_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "source_closure_packet_id": SOURCE_CLOSURE_PACKET_ID,
        "source_closure_options_id": SOURCE_CLOSURE_OPTIONS_ID,
        "source_probe_result_id": SOURCE_RESULT_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_output_class": PROBE_OUTPUT_CLASS,
        "closure_class": CLOSURE_CLASS,
        "current_surface_closed": True,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed_after_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "return_to_surface_selection_packet_created_now": False,
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
        "recommended_review_unit": acceptance_packet["recommended_review_unit"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_runtime_adoption_bounded_probe_closure_acceptance_receipt_v0",
        "receipt_type": "TYPED_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_ACCEPTANCE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_closure_acceptance_summary": {
            "runtime_adoption_bounded_probe_closure_acceptance_complete": gate == "PASS",
            "human_decision": HUMAN_DECISION,
            "source_closure_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
            "source_closure_packet_id": SOURCE_CLOSURE_PACKET_ID,
            "source_closure_options_id": SOURCE_CLOSURE_OPTIONS_ID,
            "source_closure_boundary_id": SOURCE_CLOSURE_BOUNDARY_ID,
            "source_probe_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
            "source_probe_result_id": SOURCE_RESULT_ID,
            "source_probe_evidence_id": SOURCE_EVIDENCE_ID,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "probe_label": PROBE_LABEL,
            "probe_output_class": PROBE_OUTPUT_CLASS,
            "closure_class": CLOSURE_CLASS,
            "current_surface_closed": True,
            "closed_with_no_new_authority": True,
            "return_to_surface_selection_allowed_after_review": True,
            "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
            "authorized_future_unit_count_after_review": 1,
            "return_to_surface_selection_packet_created_now": False,
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
            "recommended_review_unit": acceptance_packet["recommended_review_unit"],
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
            "acceptance_decision": rel(ACCEPTANCE_DECISION),
            "acceptance_packet": rel(ACCEPTANCE_PACKET),
            "final_closure": rel(FINAL_CLOSURE),
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

    receipt["receipt_id"] = "c8_runtime_adoption_bounded_probe_closure_acceptance_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_adoption_bounded_probe_closure_acceptance_receipt_id={receipt['receipt_id']}")
    print(f"runtime_adoption_bounded_probe_closure_acceptance_receipt_path={rel(receipt_path)}")
    print(f"runtime_adoption_bounded_probe_closure_acceptance_decision_path={rel(ACCEPTANCE_DECISION)}")
    print(f"runtime_adoption_bounded_probe_closure_acceptance_packet_path={rel(ACCEPTANCE_PACKET)}")
    print(f"runtime_adoption_bounded_probe_final_closure_path={rel(FINAL_CLOSURE)}")
    print(f"runtime_adoption_bounded_probe_closure_acceptance_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"human_decision={HUMAN_DECISION}")
    print(f"selected_surface_id={SELECTED_SURFACE_ID}")
    print(f"selected_surface_kind={SELECTED_SURFACE_KIND}")
    print(f"probe_id={PROBE_ID}")
    print(f"probe_output_class={PROBE_OUTPUT_CLASS}")
    print("current_surface_closed=true")
    print("closed_with_no_new_authority=true")
    print("return_to_surface_selection_allowed_after_review=true")
    print(f"authorized_future_unit_after_review={AUTHORIZED_FUTURE_UNIT}")
    print("authorized_future_unit_count_after_review=1")
    print("return_to_surface_selection_packet_created_now=false")
    print("next_surface_selected_now=false")
    print("probe_prep_created_now=false")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={acceptance_packet['recommended_review_unit']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
