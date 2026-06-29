#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.failed_unit_sample.diagnostic_assessment.packet.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_PACKET_CREATED_AFTER_RUNTIME_ADOPTION_CLOSURE"

SOURCE_DISCOVERY_RECEIPT_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_receipt_c9e0fb77"
SOURCE_DISCOVERY_RESULT_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_result_67360c26"
SOURCE_DISCOVERY_BOUNDARY_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_boundary_2ae0e55c"
SOURCE_DISCOVERY_EXECUTION_AUTHORITY_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_authority_f06fa4a1"

FAILED_UNIT_SAMPLE_ID = "c8_failed_unit_sample_ee4e6092"
FAILED_UNIT_SAMPLE_SOURCE_PATH = "data/a0_current_receipt_chain_frontier_application_v0_receipts/c1d0f615.json"
FAILED_UNIT_SAMPLE_SOURCE_STATUS = "MISSING_STATUS_FIELD_WITH_FAILURE_INDICATOR"

GAP_OBJECT = "FAILED_UNIT_SAMPLE_ABSENCE"
DISCOVERY_TARGET = "ONE_FAILED_UNIT_SAMPLE"
SELECTED_SURFACE_ID = "c8_successor_surface_unit_feedback_hardening_after_runtime_adoption_closure_v0"
SELECTED_SURFACE_KIND = "UNIT_FEEDBACK_HARDENING_SURFACE"
SELECTED_SURFACE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_AFTER_RUNTIME_ADOPTION_CLOSURE_SURFACE"
PROBE_ID = "c8_unit_feedback_hardening_bounded_probe_after_runtime_adoption_closure_v0"
PROBE_KIND = "UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE"
PROBE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_AFTER_RUNTIME_ADOPTION_CLOSURE"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_after_runtime_adoption_closure_v0_receipts"

DISCOVERY_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_receipt_c9e0fb77.json"
DISCOVERY_RESULT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_result_v0.json"
DISCOVERY_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_boundary_audit_v0.json"
DISCOVERY_READOUT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_readout_v0.json"
DISCOVERY_REPORT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_report.json"
SAMPLE_SOURCE = ROOT / FAILED_UNIT_SAMPLE_SOURCE_PATH

ASSESSMENT_PACKET = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_packet_v0.json"
OPTIONS = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_options_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_report.json"

REVIEW_UNIT = "REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
HUMAN_DECISION = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_FOR_FEEDBACK_HARDENING_DECISION"
FUTURE_UNIT = "CREATE_C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_FROM_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

FORBIDDEN_COUNTER_KEYS = [
    "additional_sample_discovery_count",
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
        "discovery_receipt": DISCOVERY_RECEIPT,
        "discovery_result": DISCOVERY_RESULT,
        "discovery_boundary": DISCOVERY_BOUNDARY,
        "discovery_readout": DISCOVERY_READOUT,
        "discovery_report": DISCOVERY_REPORT,
        "sample_source": SAMPLE_SOURCE,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    receipt = read_json(DISCOVERY_RECEIPT)
    result = read_json(DISCOVERY_RESULT)
    boundary = read_json(DISCOVERY_BOUNDARY)
    report = read_json(DISCOVERY_REPORT)
    source = read_json(SAMPLE_SOURCE)
    summary = receipt.get("machine_readable_unit_feedback_hardening_failed_unit_sample_discovery_execution_summary", {})
    sample = result.get("failed_unit_sample", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_EXECUTION_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_FOUND_ONE_SAMPLE",
        "receipt_id": SOURCE_DISCOVERY_RECEIPT_ID,
    }
    for key, want in expected_receipt.items():
        chk(failures, f"discovery_receipt_{key}", receipt.get(key), want)

    expected_summary = {
        "authorized_unit_consumed": "EXECUTE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "source_discovery_prep_acceptance_receipt_id": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_receipt_fa84e9db",
        "source_discovery_execution_authority_id": SOURCE_DISCOVERY_EXECUTION_AUTHORITY_ID,
        "gap_object": GAP_OBJECT,
        "discovery_target": DISCOVERY_TARGET,
        "execution_limit": 1,
        "execution_count": 1,
        "failed_unit_sample_found": True,
        "failed_unit_sample_count": 1,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "sample_discovery_executed_now": True,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized": False,
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
    }
    for key, want in expected_summary.items():
        chk(failures, f"discovery_summary_{key}", summary.get(key), want)

    chk(failures, "result_id", result.get("c8_unit_feedback_hardening_failed_unit_sample_discovery_result_id"), SOURCE_DISCOVERY_RESULT_ID)
    chk(failures, "boundary_id", boundary.get("c8_unit_feedback_hardening_failed_unit_sample_discovery_boundary_audit_id"), SOURCE_DISCOVERY_BOUNDARY_ID)

    if not isinstance(sample, dict):
        failures.append("failed_unit_sample_missing")
        sample = {}

    chk(failures, "sample_id", sample.get("failed_unit_sample_id"), FAILED_UNIT_SAMPLE_ID)
    chk(failures, "sample_source_path", sample.get("source_path"), FAILED_UNIT_SAMPLE_SOURCE_PATH)
    chk(failures, "sample_source_status", sample.get("source_status"), FAILED_UNIT_SAMPLE_SOURCE_STATUS)

    diagnostic = sample.get("diagnostic_feedback_fields", {})
    rubric = {
        "why": bool(isinstance(diagnostic, dict) and diagnostic.get("why")),
        "where": bool(isinstance(diagnostic, dict) and diagnostic.get("where")),
        "relative_to": bool(isinstance(diagnostic, dict) and diagnostic.get("relative_to")),
        "refinement_or_next_lawful_step": bool(isinstance(diagnostic, dict) and diagnostic.get("refinement_or_next_lawful_step")),
        "failure_status_vs_useful_feedback_note": bool(isinstance(diagnostic, dict) and diagnostic.get("failure_status_vs_useful_feedback_note")),
        "source_status_explicit": bool(sample.get("source_status")),
        "source_status_is_missing_marker": sample.get("source_status") == FAILED_UNIT_SAMPLE_SOURCE_STATUS,
        "source_status_repair_note_present": bool(sample.get("source_status_repair_note")),
        "source_path_traceable": sample.get("source_path") == FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "failure_indicator_present": bool(sample.get("failure_indicator")),
    }

    useful_feedback_fields_present = all([
        rubric["why"],
        rubric["where"],
        rubric["relative_to"],
        rubric["refinement_or_next_lawful_step"],
        rubric["failure_status_vs_useful_feedback_note"],
        rubric["source_path_traceable"],
        rubric["failure_indicator_present"],
    ])

    diagnostic_status = (
        "FAILED_UNIT_SAMPLE_DIAGNOSTIC_FEEDBACK_USEFUL_WITH_SOURCE_STATUS_GAP_EXPOSED"
        if useful_feedback_fields_present and rubric["source_status_is_missing_marker"]
        else "FAILED_UNIT_SAMPLE_DIAGNOSTIC_FEEDBACK_USEFUL"
        if useful_feedback_fields_present
        else "FAILED_UNIT_SAMPLE_DIAGNOSTIC_FEEDBACK_INSUFFICIENT"
    )

    hardening_observation = (
        "Sample provides the required why/where/relative/refinement/failure-status-vs-feedback fields, "
        "but also exposes that the source artifact itself lacks a top-level status field."
        if diagnostic_status == "FAILED_UNIT_SAMPLE_DIAGNOSTIC_FEEDBACK_USEFUL_WITH_SOURCE_STATUS_GAP_EXPOSED"
        else "Sample provides the required failed-unit diagnostic feedback fields."
        if diagnostic_status == "FAILED_UNIT_SAMPLE_DIAGNOSTIC_FEEDBACK_USEFUL"
        else "Sample does not yet provide all required failed-unit diagnostic feedback fields."
    )

    recommended_decision_class = (
        "ACCEPT_SAMPLE_AS_USEFUL_DIAGNOSTIC_FEEDBACK_WITH_SOURCE_STATUS_GAP"
        if diagnostic_status == "FAILED_UNIT_SAMPLE_DIAGNOSTIC_FEEDBACK_USEFUL_WITH_SOURCE_STATUS_GAP_EXPOSED"
        else "ACCEPT_SAMPLE_AS_USEFUL_DIAGNOSTIC_FEEDBACK"
        if diagnostic_status == "FAILED_UNIT_SAMPLE_DIAGNOSTIC_FEEDBACK_USEFUL"
        else "REQUIRE_UNIT_FEEDBACK_FIELD_REFINEMENT"
    )

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

    packet = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_packet_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "source_discovery_execution_receipt_id": SOURCE_DISCOVERY_RECEIPT_ID,
        "source_discovery_result_id": SOURCE_DISCOVERY_RESULT_ID,
        "source_discovery_boundary_id": SOURCE_DISCOVERY_BOUNDARY_ID,
        "source_discovery_execution_authority_id": SOURCE_DISCOVERY_EXECUTION_AUTHORITY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "gap_object": GAP_OBJECT,
        "discovery_target": DISCOVERY_TARGET,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "failed_unit_sample_source_status": FAILED_UNIT_SAMPLE_SOURCE_STATUS,
        "diagnostic_assessment_status": diagnostic_status,
        "recommended_decision_class": recommended_decision_class,
        "rubric": rubric,
        "hardening_observation": hardening_observation,
        "diagnostic_feedback_fields": diagnostic,
        "source_failure_indicator": sample.get("failure_indicator"),
        "source_status_repair_note": sample.get("source_status_repair_note"),
        "sample_source_has_top_level_status": bool(source.get("status")),
        "sample_source_top_level_status": source.get("status"),
        "sample_source_status_marker_is_not_invented_status": sample.get("source_status") == FAILED_UNIT_SAMPLE_SOURCE_STATUS,
        "sample_diagnostic_assessed_now": True,
        "additional_sample_discovery_now": False,
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
        "recommended_human_decision": HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "recommended_review_unit": REVIEW_UNIT,
    }
    packet["c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_packet_id"] = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_packet_" + sig8(packet)
    write_json(ASSESSMENT_PACKET, packet)

    options = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_options_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_options_id": None,
        "created_at": now_iso(),
        "source_diagnostic_assessment_packet_id": packet["c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_packet_id"],
        "recommended_human_decision": HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "human_decision_options": [
            HUMAN_DECISION,
            "REJECT_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT",
            "REQUEST_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_REVISION",
        ],
    }
    options["c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_options_id"] = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_options_" + sig8(options)
    write_json(OPTIONS, options)

    boundary_audit = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_boundary_audit_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_diagnostic_assessment_packet_id": packet["c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_packet_id"],
        "source_diagnostic_assessment_options_id": options["c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_options_id"],
        "source_discovery_execution_receipt_id": SOURCE_DISCOVERY_RECEIPT_ID,
        "allowed_now": {
            "assess_one_discovered_failed_unit_sample": True,
            "emit_diagnostic_assessment_packet_for_review": True,
        },
        "not_allowed_now": {
            "execute_additional_sample_discovery": True,
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
            "claim_unit_feedback_hardening_complete": True,
        },
        "forbidden_counters": forbidden_counters,
        "failures": failures,
        "warnings": warnings,
    }
    boundary_audit["c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_boundary_audit_id"] = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    gate_results = {
        "DIAGNOSTIC_ASSESSMENT_0_SOURCE_DISCOVERY_RECEIPT_PASS": receipt.get("gate") == "PASS",
        "DIAGNOSTIC_ASSESSMENT_1_SAMPLE_FOUND_ONE": summary.get("failed_unit_sample_found") is True and summary.get("failed_unit_sample_count") == 1,
        "DIAGNOSTIC_ASSESSMENT_2_SAMPLE_ID_MATCH": sample.get("failed_unit_sample_id") == FAILED_UNIT_SAMPLE_ID,
        "DIAGNOSTIC_ASSESSMENT_3_SAMPLE_SOURCE_TRACEABLE": sample.get("source_path") == FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "DIAGNOSTIC_ASSESSMENT_4_RUBRIC_FIELDS_CHECKED": all(k in rubric for k in ["why", "where", "relative_to", "refinement_or_next_lawful_step", "failure_status_vs_useful_feedback_note"]),
        "DIAGNOSTIC_ASSESSMENT_5_NO_ADDITIONAL_DISCOVERY": packet["additional_sample_discovery_now"] is False,
        "DIAGNOSTIC_ASSESSMENT_6_NO_PROBE_BUILD_RERUN_SCHEMA": packet["probe_execution_authorized_now"] is False and packet["instrument_build_authorized_now"] is False and packet["c8_rerun_authorized_now"] is False and packet["reusable_schema_authorized_now"] is False,
        "DIAGNOSTIC_ASSESSMENT_7_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "DIAGNOSTIC_ASSESSMENT_8_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "DIAGNOSTIC_ASSESSMENT_9_REQUIRES_REVIEW": packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"diagnostic_assessment_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_PACKET_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_PACKET_FAIL"
    outcome = "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_PACKET_READY_FOR_REVIEW" if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_PACKET_FAILED"
    terminal_stop = "STOP_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_PACKET_READY_FOR_REVIEW" if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_PACKET_FAILED"

    readout = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_readout_v0",
        "title": "C8 unit-feedback hardening failed-unit sample diagnostic assessment after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "diagnostic_assessment_status": diagnostic_status,
        "recommended_decision_class": recommended_decision_class,
        "sample_diagnostic_assessed_now": True,
        "additional_sample_discovery_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_human_decision": HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "recommended_review_unit": REVIEW_UNIT,
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report_obj = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_discovery_execution_receipt_id": SOURCE_DISCOVERY_RECEIPT_ID,
        "source_discovery_result_id": SOURCE_DISCOVERY_RESULT_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "diagnostic_assessment_status": diagnostic_status,
        "recommended_decision_class": recommended_decision_class,
        "rubric": rubric,
        "hardening_observation": hardening_observation,
        "sample_diagnostic_assessed_now": True,
        "additional_sample_discovery_now": False,
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
        "recommended_human_decision": HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "recommended_review_unit": REVIEW_UNIT,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report_obj)

    receipt_obj = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_PACKET_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_summary": {
            "diagnostic_assessment_packet_created": gate == "PASS",
            "authorized_unit_consumed": UNIT_ID,
            "source_discovery_execution_receipt_id": SOURCE_DISCOVERY_RECEIPT_ID,
            "source_discovery_result_id": SOURCE_DISCOVERY_RESULT_ID,
            "source_discovery_boundary_id": SOURCE_DISCOVERY_BOUNDARY_ID,
            "source_discovery_execution_authority_id": SOURCE_DISCOVERY_EXECUTION_AUTHORITY_ID,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "probe_label": PROBE_LABEL,
            "gap_object": GAP_OBJECT,
            "discovery_target": DISCOVERY_TARGET,
            "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
            "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
            "failed_unit_sample_source_status": FAILED_UNIT_SAMPLE_SOURCE_STATUS,
            "diagnostic_assessment_status": diagnostic_status,
            "recommended_decision_class": recommended_decision_class,
            "rubric": rubric,
            "hardening_observation": hardening_observation,
            "sample_diagnostic_assessed_now": True,
            "additional_sample_discovery_now": False,
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
            "recommended_human_decision": HUMAN_DECISION,
            "if_accepted_authorizes_future_unit": FUTURE_UNIT,
            "authorized_future_unit_count_after_review": 1,
            "recommended_review_unit": REVIEW_UNIT,
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
            "diagnostic_assessment_packet": rel(ASSESSMENT_PACKET),
            "diagnostic_assessment_options": rel(OPTIONS),
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

    receipt_obj["receipt_id"] = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_receipt_" + sig8(receipt_obj)
    receipt_path = RECEIPT_DIR / f"{receipt_obj['receipt_id']}.json"
    receipt_obj["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_obj)

    print(json.dumps(receipt_obj, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_receipt_id={receipt_obj['receipt_id']}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_packet_path={rel(ASSESSMENT_PACKET)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_options_path={rel(OPTIONS)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"failed_unit_sample_id={FAILED_UNIT_SAMPLE_ID}")
    print(f"failed_unit_sample_source_path={FAILED_UNIT_SAMPLE_SOURCE_PATH}")
    print(f"diagnostic_assessment_status={diagnostic_status}")
    print(f"recommended_decision_class={recommended_decision_class}")
    print("sample_diagnostic_assessed_now=true")
    print("additional_sample_discovery_now=false")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_human_decision={HUMAN_DECISION}")
    print(f"if_accepted_authorizes_future_unit={FUTURE_UNIT}")
    print(f"recommended_review_unit={REVIEW_UNIT}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
