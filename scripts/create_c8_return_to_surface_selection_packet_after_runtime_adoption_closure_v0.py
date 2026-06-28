#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_RETURN_TO_SURFACE_SELECTION_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.return_to_surface_selection_packet.after_runtime_adoption_closure.v0"
MILESTONE = "C8_RETURN_TO_SURFACE_SELECTION_PACKET_CREATED_AFTER_RUNTIME_ADOPTION_CLOSURE"
OUTCOME = "C8_RETURN_TO_SURFACE_SELECTION_PACKET_READY_FOR_REVIEW"
STOP_CODE = "STOP_C8_RETURN_TO_SURFACE_SELECTION_PACKET_READY_FOR_REVIEW"

SOURCE_CLOSURE_ACCEPTANCE_RECEIPT_ID = "c8_runtime_adoption_bounded_probe_closure_acceptance_receipt_69984edf"
SOURCE_CLOSURE_ACCEPTANCE_DECISION_ID = "c8_runtime_adoption_bounded_probe_closure_acceptance_decision_a4989fd2"
SOURCE_CLOSURE_ACCEPTANCE_PACKET_ID = "c8_runtime_adoption_bounded_probe_closure_acceptance_packet_31cc313b"
SOURCE_FINAL_CLOSURE_ID = "c8_runtime_adoption_bounded_probe_final_closure_a7db49a5"
SOURCE_CLOSURE_ACCEPTANCE_BOUNDARY_ID = "c8_runtime_adoption_bounded_probe_closure_acceptance_boundary_667c0c3f"

SOURCE_PROBE_EXECUTION_RECEIPT_ID = "c8_runtime_adoption_bounded_probe_execution_receipt_ed8c0509"
SOURCE_PROBE_RESULT_ID = "c8_runtime_adoption_bounded_probe_result_a0ec0ebb"
SOURCE_PROBE_EVIDENCE_ID = "c8_runtime_adoption_bounded_probe_evidence_9ad18624"

SELECTED_SURFACE_ID = "c8_successor_surface_runtime_adoption_after_reentry_v0"
SELECTED_SURFACE_KIND = "RUNTIME_ADOPTION_SURFACE"
SELECTED_SURFACE_LABEL = "C8_RUNTIME_ADOPTION_AFTER_REUSE_AUTHORITY_CLOSURE_SURFACE"

PROBE_ID = "c8_runtime_adoption_surface_bounded_probe_after_reentry_v0"
PROBE_KIND = "RUNTIME_ADOPTION_BOUNDARY_PROBE"
PROBE_OUTPUT_CLASS = "RUNTIME_ADOPTION_BOUNDARY_PROBE_OBSERVED_NO_DEFECTS"

AUTHORIZED_BY_CLOSURE_UNIT = "CREATE_C8_RETURN_TO_SURFACE_SELECTION_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
POTENTIAL_FUTURE_UNIT_IF_ACCEPTED = "SELECT_C8_SUCCESSOR_SURFACE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

OUT_DIR = ROOT / "data/c8_return_to_surface_selection_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_return_to_surface_selection_after_runtime_adoption_closure_v0_receipts"

ACCEPTANCE_RECEIPT = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_acceptance_after_reentry_v0_receipts/c8_runtime_adoption_bounded_probe_closure_acceptance_receipt_69984edf.json"
ACCEPTANCE_DECISION = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_acceptance_after_reentry_v0/c8_runtime_adoption_bounded_probe_closure_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_acceptance_after_reentry_v0/c8_runtime_adoption_bounded_probe_closure_acceptance_packet_v0.json"
FINAL_CLOSURE = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_acceptance_after_reentry_v0/c8_runtime_adoption_bounded_probe_final_closure_v0.json"
ACCEPTANCE_BOUNDARY = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_acceptance_after_reentry_v0/c8_runtime_adoption_bounded_probe_closure_acceptance_boundary_audit_v0.json"
ACCEPTANCE_REPORT = ROOT / "data/c8_runtime_adoption_bounded_probe_closure_acceptance_after_reentry_v0/c8_runtime_adoption_bounded_probe_closure_acceptance_report.json"

RETURN_PACKET = OUT_DIR / "c8_return_to_surface_selection_packet_v0.json"
RETURN_OPTIONS = OUT_DIR / "c8_return_to_surface_selection_options_v0.json"
RETURN_BOUNDARY = OUT_DIR / "c8_return_to_surface_selection_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_return_to_surface_selection_readout_v0.json"
REPORT = OUT_DIR / "c8_return_to_surface_selection_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "surface_selected_count",
    "successor_surface_accepted_count",
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
        "acceptance_receipt": ACCEPTANCE_RECEIPT,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_packet": ACCEPTANCE_PACKET,
        "final_closure": FINAL_CLOSURE,
        "acceptance_boundary": ACCEPTANCE_BOUNDARY,
        "acceptance_report": ACCEPTANCE_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    acceptance_receipt = read_json(ACCEPTANCE_RECEIPT)
    acceptance_decision = read_json(ACCEPTANCE_DECISION)
    acceptance_packet = read_json(ACCEPTANCE_PACKET)
    final_closure = read_json(FINAL_CLOSURE)
    acceptance_boundary = read_json(ACCEPTANCE_BOUNDARY)
    acceptance_report = read_json(ACCEPTANCE_REPORT)
    summary = acceptance_receipt.get("machine_readable_closure_acceptance_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_ACCEPTANCE_PASS",
        "outcome_class": "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSED_NO_NEW_AUTHORITY_RETURN_TO_SURFACE_SELECTION_ALLOWED",
        "receipt_id": SOURCE_CLOSURE_ACCEPTANCE_RECEIPT_ID,
    }

    for key, want in expected_receipt.items():
        chk(failures, f"acceptance_receipt_{key}", acceptance_receipt.get(key), want)

    expected_summary = {
        "runtime_adoption_bounded_probe_closure_acceptance_complete": True,
        "human_decision": "ACCEPT_CLOSURE_NO_NEW_AUTHORITY_RETURN_TO_SURFACE_SELECTION",
        "source_closure_receipt_id": "c8_runtime_adoption_bounded_probe_closure_receipt_11e2b2ad",
        "source_closure_packet_id": "c8_runtime_adoption_bounded_probe_closure_packet_36c8c6d3",
        "source_closure_options_id": "c8_runtime_adoption_bounded_probe_closure_options_e4874557",
        "source_closure_boundary_id": "c8_runtime_adoption_bounded_probe_closure_boundary_579632d6",
        "source_probe_execution_receipt_id": SOURCE_PROBE_EXECUTION_RECEIPT_ID,
        "source_probe_result_id": SOURCE_PROBE_RESULT_ID,
        "source_probe_evidence_id": SOURCE_PROBE_EVIDENCE_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_output_class": PROBE_OUTPUT_CLASS,
        "current_surface_closed": True,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed_after_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_BY_CLOSURE_UNIT,
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
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
        "recommended_review_unit": "REVIEW_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_CLOSURE_ACCEPTANCE_AFTER_REENTRY_V0",
        "next_command_goal": None,
    }

    for key, want in expected_summary.items():
        chk(failures, f"acceptance_summary_{key}", summary.get(key), want)

    expected_acceptance_packet = {
        "runtime_adoption_bounded_probe_closure_acceptance_packet_id": SOURCE_CLOSURE_ACCEPTANCE_PACKET_ID,
        "acceptance_status": "CLOSURE_ACCEPTED_NO_NEW_AUTHORITY",
        "current_surface_closed": True,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed_after_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_BY_CLOSURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "return_to_surface_selection_packet_created_now": False,
        "next_surface_selected_now": False,
        "probe_prep_created_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
    }

    for key, want in expected_acceptance_packet.items():
        chk(failures, f"acceptance_packet_{key}", acceptance_packet.get(key), want)

    expected_final_closure = {
        "runtime_adoption_bounded_probe_final_closure_id": SOURCE_FINAL_CLOSURE_ID,
        "closure_status": "CLOSED_NO_NEW_AUTHORITY",
        "current_surface_closed": True,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed_after_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_BY_CLOSURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "next_surface_selected_now": False,
        "probe_prep_created_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
    }

    for key, want in expected_final_closure.items():
        chk(failures, f"final_closure_{key}", final_closure.get(key), want)

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

    return_options = {
        "schema_version": "c8_return_to_surface_selection_options_v0",
        "c8_return_to_surface_selection_options_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "source_closure_acceptance_receipt_id": SOURCE_CLOSURE_ACCEPTANCE_RECEIPT_ID,
        "source_final_closure_id": SOURCE_FINAL_CLOSURE_ID,
        "return_to_surface_selection_basis": [
            "runtime-adoption bounded probe surface closed",
            "closure accepted with no new authority",
            "return-to-surface-selection allowed after review",
        ],
        "human_decision_options": [
            "ACCEPT_RETURN_TO_SURFACE_SELECTION_PACKET",
            "REJECT_RETURN_TO_SURFACE_SELECTION_PACKET",
            "REQUEST_RETURN_TO_SURFACE_SELECTION_PACKET_REVISION",
        ],
        "recommended_human_decision": "ACCEPT_RETURN_TO_SURFACE_SELECTION_PACKET",
        "if_accepted_authorizes_future_unit": POTENTIAL_FUTURE_UNIT_IF_ACCEPTED,
        "decision_boundary": {
            "accept_return_packet_means": [
                "acknowledge runtime-adoption closure as the return basis",
                "authorize a later successor-surface selection unit",
                "keep next-surface choice outside this packet",
            ],
            "accept_return_packet_does_not_mean": [
                "select next surface now",
                "accept any concrete surface now",
                "create probe prep now",
                "authorize probe execution now",
                "build runtime machinery now",
                "rerun C8 now",
                "promote reusable schema now",
            ],
        },
    }
    return_options["c8_return_to_surface_selection_options_id"] = "c8_return_to_surface_selection_options_" + sig8(return_options)
    write_json(RETURN_OPTIONS, return_options)

    return_packet = {
        "schema_version": "c8_return_to_surface_selection_packet_v0",
        "c8_return_to_surface_selection_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "return_packet_status": "READY_FOR_REVIEW",
        "source_closure_acceptance_receipt_id": SOURCE_CLOSURE_ACCEPTANCE_RECEIPT_ID,
        "source_closure_acceptance_decision_id": SOURCE_CLOSURE_ACCEPTANCE_DECISION_ID,
        "source_closure_acceptance_packet_id": SOURCE_CLOSURE_ACCEPTANCE_PACKET_ID,
        "source_final_closure_id": SOURCE_FINAL_CLOSURE_ID,
        "source_closure_acceptance_boundary_id": SOURCE_CLOSURE_ACCEPTANCE_BOUNDARY_ID,
        "source_return_options_id": return_options["c8_return_to_surface_selection_options_id"],
        "source_probe_execution_receipt_id": SOURCE_PROBE_EXECUTION_RECEIPT_ID,
        "source_probe_result_id": SOURCE_PROBE_RESULT_ID,
        "source_probe_evidence_id": SOURCE_PROBE_EVIDENCE_ID,
        "closed_surface_id": SELECTED_SURFACE_ID,
        "closed_surface_kind": SELECTED_SURFACE_KIND,
        "closed_surface_label": SELECTED_SURFACE_LABEL,
        "closed_probe_id": PROBE_ID,
        "closed_probe_kind": PROBE_KIND,
        "closed_probe_output_class": PROBE_OUTPUT_CLASS,
        "return_to_surface_selection_packet_created": True,
        "return_to_surface_selection_packet_created_count": 1,
        "current_surface_closed": True,
        "closed_with_no_new_authority": True,
        "successor_surface_selection_ready_for_human_decision": True,
        "recommended_human_decision": "ACCEPT_RETURN_TO_SURFACE_SELECTION_PACKET",
        "if_accepted_authorizes_future_unit": POTENTIAL_FUTURE_UNIT_IF_ACCEPTED,
        "surface_selected_now": False,
        "successor_surface_accepted_now": False,
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
        "recommended_review_unit": "REVIEW_C8_RETURN_TO_SURFACE_SELECTION_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
    }
    return_packet["c8_return_to_surface_selection_packet_id"] = "c8_return_to_surface_selection_packet_" + sig8(return_packet)
    write_json(RETURN_PACKET, return_packet)

    return_boundary = {
        "schema_version": "c8_return_to_surface_selection_boundary_audit_v0",
        "c8_return_to_surface_selection_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_return_packet_id": return_packet["c8_return_to_surface_selection_packet_id"],
        "source_return_options_id": return_options["c8_return_to_surface_selection_options_id"],
        "source_closure_acceptance_receipt_id": SOURCE_CLOSURE_ACCEPTANCE_RECEIPT_ID,
        "source_final_closure_id": SOURCE_FINAL_CLOSURE_ID,
        "allowed_now": {
            "create_return_to_surface_selection_packet_for_review": True,
            "present_return_to_surface_selection_decision_options": True,
        },
        "not_allowed_now": {
            "accept_return_to_surface_selection_packet": True,
            "select_surface": True,
            "accept_successor_surface": True,
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
    return_boundary["c8_return_to_surface_selection_boundary_audit_id"] = "c8_return_to_surface_selection_boundary_" + sig8(return_boundary)
    write_json(RETURN_BOUNDARY, return_boundary)

    gate_results = {
        "RETURN_PACKET_0_SOURCE_CLOSURE_ACCEPTANCE_RECEIPT_PASS": acceptance_receipt.get("gate") == "PASS",
        "RETURN_PACKET_1_SURFACE_CLOSED_NO_NEW_AUTHORITY": summary.get("current_surface_closed") is True and summary.get("closed_with_no_new_authority") is True,
        "RETURN_PACKET_2_RETURN_ALLOWED_AFTER_REVIEW": summary.get("return_to_surface_selection_allowed_after_review") is True,
        "RETURN_PACKET_3_THIS_UNIT_AUTHORIZED_BY_CLOSURE": summary.get("authorized_future_unit_after_review") == UNIT_ID,
        "RETURN_PACKET_4_PACKET_CREATED_ONCE": return_packet["return_to_surface_selection_packet_created"] is True and return_packet["return_to_surface_selection_packet_created_count"] == 1,
        "RETURN_PACKET_5_NO_SURFACE_SELECTED_NOW": return_packet["surface_selected_now"] is False and return_packet["successor_surface_accepted_now"] is False,
        "RETURN_PACKET_6_NO_PROBE_OR_EXECUTION_NOW": return_packet["probe_prep_created_now"] is False and return_packet["probe_execution_authorized_now"] is False and return_packet["probe_executed_now"] is False,
        "RETURN_PACKET_7_NO_BUILD_RERUN_SCHEMA": return_packet["instrument_build_authorized_now"] is False and return_packet["c8_rerun_authorized_now"] is False and return_packet["reusable_schema_authorized_now"] is False,
        "RETURN_PACKET_8_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "RETURN_PACKET_9_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "RETURN_PACKET_10_REQUIRES_REVIEW": return_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"return_packet_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_RETURN_TO_SURFACE_SELECTION_PACKET_PASS" if gate == "PASS" else "TYPED_C8_RETURN_TO_SURFACE_SELECTION_PACKET_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_RETURN_TO_SURFACE_SELECTION_PACKET_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_RETURN_TO_SURFACE_SELECTION_PACKET_FAILED"

    readout = {
        "schema_version": "c8_return_to_surface_selection_readout_v0",
        "title": "C8 return-to-surface-selection packet after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "closed_surface_id": SELECTED_SURFACE_ID,
        "closed_surface_kind": SELECTED_SURFACE_KIND,
        "closed_probe_id": PROBE_ID,
        "return_to_surface_selection_packet_created": True,
        "successor_surface_selection_ready_for_human_decision": True,
        "recommended_human_decision": return_packet["recommended_human_decision"],
        "if_accepted_authorizes_future_unit": POTENTIAL_FUTURE_UNIT_IF_ACCEPTED,
        "surface_selected_now": False,
        "successor_surface_accepted_now": False,
        "probe_prep_created_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": return_packet["recommended_review_unit"],
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_return_to_surface_selection_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_closure_acceptance_receipt_id": SOURCE_CLOSURE_ACCEPTANCE_RECEIPT_ID,
        "source_final_closure_id": SOURCE_FINAL_CLOSURE_ID,
        "closed_surface_id": SELECTED_SURFACE_ID,
        "closed_surface_kind": SELECTED_SURFACE_KIND,
        "closed_surface_label": SELECTED_SURFACE_LABEL,
        "closed_probe_id": PROBE_ID,
        "closed_probe_kind": PROBE_KIND,
        "closed_probe_output_class": PROBE_OUTPUT_CLASS,
        "return_to_surface_selection_packet_created": True,
        "return_to_surface_selection_packet_created_count": 1,
        "successor_surface_selection_ready_for_human_decision": True,
        "recommended_human_decision": return_packet["recommended_human_decision"],
        "if_accepted_authorizes_future_unit": POTENTIAL_FUTURE_UNIT_IF_ACCEPTED,
        "surface_selected_now": False,
        "successor_surface_accepted_now": False,
        "probe_prep_created_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "requires_review": True,
        "recommended_review_unit": return_packet["recommended_review_unit"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_return_to_surface_selection_receipt_v0",
        "receipt_type": "TYPED_C8_RETURN_TO_SURFACE_SELECTION_PACKET_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_return_to_surface_selection_summary": {
            "return_to_surface_selection_packet_created": gate == "PASS",
            "source_closure_acceptance_receipt_id": SOURCE_CLOSURE_ACCEPTANCE_RECEIPT_ID,
            "source_closure_acceptance_decision_id": SOURCE_CLOSURE_ACCEPTANCE_DECISION_ID,
            "source_closure_acceptance_packet_id": SOURCE_CLOSURE_ACCEPTANCE_PACKET_ID,
            "source_final_closure_id": SOURCE_FINAL_CLOSURE_ID,
            "source_closure_acceptance_boundary_id": SOURCE_CLOSURE_ACCEPTANCE_BOUNDARY_ID,
            "source_probe_execution_receipt_id": SOURCE_PROBE_EXECUTION_RECEIPT_ID,
            "source_probe_result_id": SOURCE_PROBE_RESULT_ID,
            "source_probe_evidence_id": SOURCE_PROBE_EVIDENCE_ID,
            "closed_surface_id": SELECTED_SURFACE_ID,
            "closed_surface_kind": SELECTED_SURFACE_KIND,
            "closed_surface_label": SELECTED_SURFACE_LABEL,
            "closed_probe_id": PROBE_ID,
            "closed_probe_kind": PROBE_KIND,
            "closed_probe_output_class": PROBE_OUTPUT_CLASS,
            "current_surface_closed": True,
            "closed_with_no_new_authority": True,
            "successor_surface_selection_ready_for_human_decision": True,
            "recommended_human_decision": return_packet["recommended_human_decision"],
            "if_accepted_authorizes_future_unit": POTENTIAL_FUTURE_UNIT_IF_ACCEPTED,
            "surface_selected_now": False,
            "successor_surface_accepted_now": False,
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
            "recommended_review_unit": return_packet["recommended_review_unit"],
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
            "return_packet": rel(RETURN_PACKET),
            "return_options": rel(RETURN_OPTIONS),
            "return_boundary": rel(RETURN_BOUNDARY),
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

    receipt["receipt_id"] = "c8_return_to_surface_selection_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c8_return_to_surface_selection_receipt_id={receipt['receipt_id']}")
    print(f"c8_return_to_surface_selection_receipt_path={rel(receipt_path)}")
    print(f"c8_return_to_surface_selection_packet_path={rel(RETURN_PACKET)}")
    print(f"c8_return_to_surface_selection_options_path={rel(RETURN_OPTIONS)}")
    print(f"c8_return_to_surface_selection_boundary_path={rel(RETURN_BOUNDARY)}")
    print(f"closed_surface_id={SELECTED_SURFACE_ID}")
    print(f"closed_surface_kind={SELECTED_SURFACE_KIND}")
    print(f"closed_probe_id={PROBE_ID}")
    print("return_to_surface_selection_packet_created=true")
    print("successor_surface_selection_ready_for_human_decision=true")
    print(f"recommended_human_decision={return_packet['recommended_human_decision']}")
    print(f"if_accepted_authorizes_future_unit={POTENTIAL_FUTURE_UNIT_IF_ACCEPTED}")
    print("surface_selected_now=false")
    print("successor_surface_accepted_now=false")
    print("probe_prep_created_now=false")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={return_packet['recommended_review_unit']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
