#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_FOR_REVIEW_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.bounded_probe.observation_acceptance.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_ACCEPTED_FOR_REVIEW_AFTER_RUNTIME_ADOPTION_CLOSURE"
OUTCOME = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_ACCEPTED_FOR_REVIEW"
STOP_CODE = "STOP_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_ACCEPTANCE_READY_FOR_REVIEW"

HUMAN_DECISION = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_FOR_REVIEW"
AUTHORIZED_FUTURE_UNIT = "CREATE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

SOURCE_EXECUTION_RECEIPT_ID = "c8_unit_feedback_hardening_bounded_probe_execution_receipt_b35662b1"
SOURCE_OBSERVATION_ID = "c8_unit_feedback_hardening_bounded_probe_observation_dd60017c"
SOURCE_INDEX_ID = "c8_unit_feedback_hardening_bounded_probe_source_index_53ccc16f"
SOURCE_EXECUTION_BOUNDARY_ID = "c8_unit_feedback_hardening_bounded_probe_execution_boundary_49533154"

SELECTED_SURFACE_ID = "c8_successor_surface_unit_feedback_hardening_after_runtime_adoption_closure_v0"
SELECTED_SURFACE_KIND = "UNIT_FEEDBACK_HARDENING_SURFACE"
SELECTED_SURFACE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_AFTER_RUNTIME_ADOPTION_CLOSURE_SURFACE"

PROBE_ID = "c8_unit_feedback_hardening_bounded_probe_after_runtime_adoption_closure_v0"
PROBE_KIND = "UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE"
PROBE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_AFTER_RUNTIME_ADOPTION_CLOSURE"

OBSERVATION_CLASS = "UNIT_FEEDBACK_DIAGNOSTIC_FEEDBACK_PARTIAL_NO_FAILED_UNIT_SAMPLE_OBSERVED"
OBSERVATION_VERDICT = "PARTIAL"
DIAGNOSTIC_GAP = "No failed-unit sample was present in the bounded source set, so the probe can verify typed-stop/status/context/refinement structure but cannot fully validate failed-unit diagnostic quality."

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_observation_acceptance_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_observation_acceptance_after_runtime_adoption_closure_v0_receipts"

EXEC_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_bounded_probe_execution_receipt_b35662b1.json"
OBSERVATION = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_observation_v0.json"
SOURCE_INDEX = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_source_index_v0.json"
EXEC_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_execution_boundary_audit_v0.json"
EXEC_READOUT = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_execution_readout_v0.json"
EXEC_REPORT = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_execution_report.json"

ACCEPTANCE_DECISION = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_packet_v0.json"
GAP_RESPONSE_AUTHORITY = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_gap_response_authority_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_report.json"

FORBIDDEN_COUNTER_KEYS = [
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
        "execution_receipt": EXEC_RECEIPT,
        "observation": OBSERVATION,
        "source_index": SOURCE_INDEX,
        "execution_boundary": EXEC_BOUNDARY,
        "execution_readout": EXEC_READOUT,
        "execution_report": EXEC_REPORT,
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
    observation = read_json(OBSERVATION)
    source_index = read_json(SOURCE_INDEX)
    exec_boundary = read_json(EXEC_BOUNDARY)
    exec_readout = read_json(EXEC_READOUT)
    exec_report = read_json(EXEC_REPORT)
    exec_summary = exec_receipt.get("machine_readable_unit_feedback_hardening_bounded_probe_execution_summary", {})

    expected_execution_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_READY_FOR_REVIEW",
        "receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
    }
    for key, want in expected_execution_receipt.items():
        chk(failures, f"execution_receipt_{key}", exec_receipt.get(key), want)

    expected_execution_summary = {
        "unit_feedback_hardening_bounded_probe_executed": True,
        "authorized_unit_consumed": "EXECUTE_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_executed_now": True,
        "probe_execution_count_now": 1,
        "bounded_probe_execution_limit": 1,
        "observation_id": SOURCE_OBSERVATION_ID,
        "source_index_id": SOURCE_INDEX_ID,
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "source_docs_count": 32,
        "typed_stop_sample_count": 5,
        "failed_unit_sample_count": 0,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized": False,
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
        "recommended_human_decision": HUMAN_DECISION,
        "recommended_review_unit": "REVIEW_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "next_command_goal": None,
    }
    for key, want in expected_execution_summary.items():
        chk(failures, f"execution_summary_{key}", exec_summary.get(key), want)

    if observation.get("c8_unit_feedback_hardening_bounded_probe_observation_id") != SOURCE_OBSERVATION_ID:
        failures.append(f"observation_id_wrong:{observation.get('c8_unit_feedback_hardening_bounded_probe_observation_id')}")
    if source_index.get("c8_unit_feedback_hardening_bounded_probe_source_index_id") != SOURCE_INDEX_ID:
        failures.append(f"source_index_id_wrong:{source_index.get('c8_unit_feedback_hardening_bounded_probe_source_index_id')}")
    if exec_boundary.get("c8_unit_feedback_hardening_bounded_probe_execution_boundary_audit_id") != SOURCE_EXECUTION_BOUNDARY_ID:
        failures.append(f"execution_boundary_id_wrong:{exec_boundary.get('c8_unit_feedback_hardening_bounded_probe_execution_boundary_audit_id')}")

    dimension_counts = observation.get("feedback_dimension_counts", {})
    expected_dimension_counts = {
        "source_docs_count": 32,
        "typed_stop_sample_count": 5,
        "failed_unit_sample_count": 0,
        "why_signal_doc_count": 17,
        "where_signal_doc_count": 5,
        "relative_object_or_boundary_signal_doc_count": 31,
        "refinement_signal_doc_count": 27,
        "failure_status_distinction_signal_doc_count": 12,
    }
    for key, want in expected_dimension_counts.items():
        chk(failures, f"dimension_{key}", dimension_counts.get(key), want)

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

    decision = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_decision_v0",
        "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_decision_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "human_decision": HUMAN_DECISION,
        "human_decision_consumed": True,
        "source_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
        "source_observation_id": SOURCE_OBSERVATION_ID,
        "source_index_id": SOURCE_INDEX_ID,
        "source_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "observation_accepted_for_review": True,
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "failed_unit_sample_count": 0,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "gap_response_packet_created_now": False,
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
    decision["c8_unit_feedback_hardening_bounded_probe_observation_acceptance_decision_id"] = "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_decision_" + sig8(decision)
    write_json(ACCEPTANCE_DECISION, decision)

    gap_response_authority = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_gap_response_authority_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_gap_response_authority_id": None,
        "created_at": now_iso(),
        "source_observation_acceptance_decision_id": decision["c8_unit_feedback_hardening_bounded_probe_observation_acceptance_decision_id"],
        "source_observation_id": SOURCE_OBSERVATION_ID,
        "source_index_id": SOURCE_INDEX_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "probe_id": PROBE_ID,
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authority_status": "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "authority_scope": {
            "may_create_failed_unit_sample_gap_response_packet": True,
            "may_authorize_probe_execution_now": False,
            "may_execute_probe_now": False,
            "may_build_now": False,
            "may_rerun_c8_now": False,
            "may_promote_schema_now": False,
        },
    }
    gap_response_authority["c8_unit_feedback_hardening_failed_unit_sample_gap_response_authority_id"] = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_authority_" + sig8(gap_response_authority)
    write_json(GAP_RESPONSE_AUTHORITY, gap_response_authority)

    packet = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_packet_v0",
        "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "acceptance_status": "BOUNDED_PROBE_OBSERVATION_ACCEPTED_FOR_REVIEW",
        "human_decision": HUMAN_DECISION,
        "source_observation_acceptance_decision_id": decision["c8_unit_feedback_hardening_bounded_probe_observation_acceptance_decision_id"],
        "source_gap_response_authority_id": gap_response_authority["c8_unit_feedback_hardening_failed_unit_sample_gap_response_authority_id"],
        "source_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
        "source_observation_id": SOURCE_OBSERVATION_ID,
        "source_index_id": SOURCE_INDEX_ID,
        "source_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "observation_accepted_for_review": True,
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "source_docs_count": 32,
        "typed_stop_sample_count": 5,
        "failed_unit_sample_count": 0,
        "why_signal_doc_count": 17,
        "where_signal_doc_count": 5,
        "relative_object_or_boundary_signal_doc_count": 31,
        "refinement_signal_doc_count": 27,
        "failure_status_distinction_signal_doc_count": 12,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "gap_response_packet_created_now": False,
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
        "recommended_review_unit": "REVIEW_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_ACCEPTANCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
    }
    packet["c8_unit_feedback_hardening_bounded_probe_observation_acceptance_packet_id"] = "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_packet_" + sig8(packet)
    write_json(ACCEPTANCE_PACKET, packet)

    boundary = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_boundary_audit_v0",
        "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_observation_acceptance_decision_id": decision["c8_unit_feedback_hardening_bounded_probe_observation_acceptance_decision_id"],
        "source_observation_acceptance_packet_id": packet["c8_unit_feedback_hardening_bounded_probe_observation_acceptance_packet_id"],
        "source_gap_response_authority_id": gap_response_authority["c8_unit_feedback_hardening_failed_unit_sample_gap_response_authority_id"],
        "source_observation_id": SOURCE_OBSERVATION_ID,
        "source_index_id": SOURCE_INDEX_ID,
        "allowed_now": {
            "accept_observation_for_review": True,
            "authorize_gap_response_packet_after_review_and_commit": True,
        },
        "not_allowed_now": {
            "create_gap_response_packet_now": True,
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
    boundary["c8_unit_feedback_hardening_bounded_probe_observation_acceptance_boundary_audit_id"] = "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_boundary_" + sig8(boundary)
    write_json(BOUNDARY_AUDIT, boundary)

    gate_results = {
        "OBSERVATION_ACCEPTANCE_0_SOURCE_EXECUTION_RECEIPT_PASS": exec_receipt.get("gate") == "PASS",
        "OBSERVATION_ACCEPTANCE_1_HUMAN_DECISION_MATCH": exec_summary.get("recommended_human_decision") == HUMAN_DECISION,
        "OBSERVATION_ACCEPTANCE_2_OBSERVATION_PARTIAL_MATCH": observation.get("observation_class") == OBSERVATION_CLASS and observation.get("observation_verdict") == OBSERVATION_VERDICT,
        "OBSERVATION_ACCEPTANCE_3_DIAGNOSTIC_GAP_PRESERVED": observation.get("diagnostic_gap") == DIAGNOSTIC_GAP,
        "OBSERVATION_ACCEPTANCE_4_FAILED_UNIT_SAMPLE_COUNT_ZERO_PRESERVED": dimension_counts.get("failed_unit_sample_count") == 0,
        "OBSERVATION_ACCEPTANCE_5_AUTHORIZES_GAP_RESPONSE_ONLY": gap_response_authority["authorized_future_unit"] == AUTHORIZED_FUTURE_UNIT,
        "OBSERVATION_ACCEPTANCE_6_NO_GAP_RESPONSE_PACKET_CREATED_NOW": packet["gap_response_packet_created_now"] is False,
        "OBSERVATION_ACCEPTANCE_7_NO_EXECUTION_NOW": packet["probe_execution_authorized_now"] is False and packet["probe_executed_now"] is False,
        "OBSERVATION_ACCEPTANCE_8_NO_BUILD_RERUN_SCHEMA": packet["instrument_build_authorized_now"] is False and packet["c8_rerun_authorized_now"] is False and packet["reusable_schema_authorized_now"] is False,
        "OBSERVATION_ACCEPTANCE_9_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "OBSERVATION_ACCEPTANCE_10_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "OBSERVATION_ACCEPTANCE_11_REQUIRES_REVIEW": packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"observation_acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_ACCEPTANCE_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_ACCEPTANCE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_ACCEPTANCE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_ACCEPTANCE_FAILED"

    readout = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_readout_v0",
        "title": "C8 unit-feedback hardening bounded probe observation acceptance after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "observation_accepted_for_review": True,
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "failed_unit_sample_count": 0,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "gap_response_packet_created_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": packet["recommended_review_unit"],
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "source_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
        "source_observation_id": SOURCE_OBSERVATION_ID,
        "source_index_id": SOURCE_INDEX_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "observation_accepted_for_review": True,
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "source_docs_count": 32,
        "typed_stop_sample_count": 5,
        "failed_unit_sample_count": 0,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "gap_response_packet_created_now": False,
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
        "recommended_review_unit": packet["recommended_review_unit"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_ACCEPTANCE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_bounded_probe_observation_acceptance_summary": {
            "observation_acceptance_complete": gate == "PASS",
            "human_decision": HUMAN_DECISION,
            "source_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
            "source_observation_id": SOURCE_OBSERVATION_ID,
            "source_index_id": SOURCE_INDEX_ID,
            "source_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "probe_label": PROBE_LABEL,
            "observation_accepted_for_review": True,
            "observation_class": OBSERVATION_CLASS,
            "observation_verdict": OBSERVATION_VERDICT,
            "diagnostic_gap": DIAGNOSTIC_GAP,
            "source_docs_count": 32,
            "typed_stop_sample_count": 5,
            "failed_unit_sample_count": 0,
            "why_signal_doc_count": 17,
            "where_signal_doc_count": 5,
            "relative_object_or_boundary_signal_doc_count": 31,
            "refinement_signal_doc_count": 27,
            "failure_status_distinction_signal_doc_count": 12,
            "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
            "authorized_future_unit_count_after_review": 1,
            "gap_response_packet_created_now": False,
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
            "recommended_review_unit": packet["recommended_review_unit"],
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
            "observation_acceptance_decision": rel(ACCEPTANCE_DECISION),
            "observation_acceptance_packet": rel(ACCEPTANCE_PACKET),
            "gap_response_authority": rel(GAP_RESPONSE_AUTHORITY),
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

    receipt["receipt_id"] = "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_bounded_probe_observation_acceptance_receipt_id={receipt['receipt_id']}")
    print(f"c8_unit_feedback_hardening_bounded_probe_observation_acceptance_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_observation_acceptance_decision_path={rel(ACCEPTANCE_DECISION)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_observation_acceptance_packet_path={rel(ACCEPTANCE_PACKET)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_gap_response_authority_path={rel(GAP_RESPONSE_AUTHORITY)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_observation_acceptance_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"human_decision={HUMAN_DECISION}")
    print(f"observation_accepted_for_review=true")
    print(f"observation_class={OBSERVATION_CLASS}")
    print(f"observation_verdict={OBSERVATION_VERDICT}")
    print(f"failed_unit_sample_count=0")
    print(f"authorized_future_unit_after_review={AUTHORIZED_FUTURE_UNIT}")
    print("authorized_future_unit_count_after_review=1")
    print("gap_response_packet_created_now=false")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={packet['recommended_review_unit']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
