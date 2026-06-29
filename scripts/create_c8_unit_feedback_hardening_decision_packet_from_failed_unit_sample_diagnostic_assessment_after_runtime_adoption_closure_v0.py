#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_FROM_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.decision_packet.from_failed_unit_sample_diagnostic_assessment.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_FROM_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_CREATED_AFTER_RUNTIME_ADOPTION_CLOSURE"

SOURCE_ACCEPTANCE_RECEIPT_ID = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_receipt_4674eec7"
SOURCE_ACCEPTANCE_DECISION_ID = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_decision_3b948309"
SOURCE_ACCEPTANCE_PACKET_ID = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_packet_455f0bc2"
SOURCE_DECISION_PACKET_AUTHORITY_ID = "c8_unit_feedback_hardening_decision_packet_authority_253cc837"
SOURCE_ACCEPTANCE_BOUNDARY_ID = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_boundary_72f694c3"

SOURCE_ASSESSMENT_RECEIPT_ID = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_receipt_2b262320"
SOURCE_ASSESSMENT_PACKET_ID = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_packet_4e6c1747"
SOURCE_ASSESSMENT_OPTIONS_ID = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_options_373a4f21"
SOURCE_ASSESSMENT_BOUNDARY_ID = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_boundary_987942ec"

SOURCE_DISCOVERY_RECEIPT_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_receipt_c9e0fb77"
SOURCE_DISCOVERY_RESULT_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_result_67360c26"
SOURCE_DISCOVERY_BOUNDARY_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_boundary_2ae0e55c"
SOURCE_DISCOVERY_AUTHORITY_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_authority_f06fa4a1"

SELECTED_SURFACE_ID = "c8_successor_surface_unit_feedback_hardening_after_runtime_adoption_closure_v0"
SELECTED_SURFACE_KIND = "UNIT_FEEDBACK_HARDENING_SURFACE"
SELECTED_SURFACE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_AFTER_RUNTIME_ADOPTION_CLOSURE_SURFACE"

PROBE_ID = "c8_unit_feedback_hardening_bounded_probe_after_runtime_adoption_closure_v0"
PROBE_KIND = "UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE"
PROBE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_AFTER_RUNTIME_ADOPTION_CLOSURE"

GAP_OBJECT = "FAILED_UNIT_SAMPLE_ABSENCE"
DISCOVERY_TARGET = "ONE_FAILED_UNIT_SAMPLE"
FAILED_UNIT_SAMPLE_ID = "c8_failed_unit_sample_ee4e6092"
FAILED_UNIT_SAMPLE_SOURCE_PATH = "data/a0_current_receipt_chain_frontier_application_v0_receipts/c1d0f615.json"
FAILED_UNIT_SAMPLE_SOURCE_STATUS = "MISSING_STATUS_FIELD_WITH_FAILURE_INDICATOR"

DIAGNOSTIC_ASSESSMENT_STATUS = "FAILED_UNIT_SAMPLE_DIAGNOSTIC_FEEDBACK_USEFUL_WITH_SOURCE_STATUS_GAP_EXPOSED"
RECOMMENDED_DECISION_CLASS = "ACCEPT_SAMPLE_AS_USEFUL_DIAGNOSTIC_FEEDBACK_WITH_SOURCE_STATUS_GAP"

FEEDBACK_HARDENING_DECISION_CLASS = "UNIT_FEEDBACK_HARDENING_DECISION_USEFUL_DIAGNOSTIC_FEEDBACK_WITH_LOCAL_SOURCE_STATUS_GAP"
LOCAL_GAP_OBJECT = "SOURCE_ARTIFACT_TOP_LEVEL_STATUS_ABSENCE"
RECOMMENDED_HUMAN_DECISION = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_FOR_SOURCE_STATUS_GAP_RESPONSE"
FUTURE_UNIT = "CREATE_C8_UNIT_FEEDBACK_HARDENING_SOURCE_STATUS_GAP_RESPONSE_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
REVIEW_UNIT = "REVIEW_C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_FROM_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_decision_packet_from_failed_unit_sample_diagnostic_assessment_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_decision_packet_from_failed_unit_sample_diagnostic_assessment_after_runtime_adoption_closure_v0_receipts"

ACCEPTANCE_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_receipt_4674eec7.json"
ACCEPTANCE_DECISION = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_packet_v0.json"
DECISION_AUTHORITY = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_decision_packet_authority_v0.json"
ACCEPTANCE_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_boundary_audit_v0.json"
ACCEPTANCE_READOUT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_readout_v0.json"
ACCEPTANCE_REPORT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_report.json"

DECISION_PACKET = OUT_DIR / "c8_unit_feedback_hardening_decision_packet_v0.json"
DECISION_OPTIONS = OUT_DIR / "c8_unit_feedback_hardening_decision_options_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_decision_packet_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_decision_packet_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_decision_packet_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "source_status_gap_response_created_count",
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
        "acceptance_receipt": ACCEPTANCE_RECEIPT,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_packet": ACCEPTANCE_PACKET,
        "decision_packet_authority": DECISION_AUTHORITY,
        "acceptance_boundary": ACCEPTANCE_BOUNDARY,
        "acceptance_readout": ACCEPTANCE_READOUT,
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

    receipt = read_json(ACCEPTANCE_RECEIPT)
    decision = read_json(ACCEPTANCE_DECISION)
    packet = read_json(ACCEPTANCE_PACKET)
    authority = read_json(DECISION_AUTHORITY)
    boundary = read_json(ACCEPTANCE_BOUNDARY)
    summary = receipt.get("machine_readable_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_ACCEPTANCE_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT_ACCEPTED_FOR_FEEDBACK_HARDENING_DECISION",
        "receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
    }
    for key, want in expected_receipt.items():
        chk(failures, f"acceptance_receipt_{key}", receipt.get(key), want)

    expected_summary = {
        "diagnostic_assessment_acceptance_complete": True,
        "source_diagnostic_assessment_receipt_id": SOURCE_ASSESSMENT_RECEIPT_ID,
        "source_diagnostic_assessment_packet_id": SOURCE_ASSESSMENT_PACKET_ID,
        "source_diagnostic_assessment_options_id": SOURCE_ASSESSMENT_OPTIONS_ID,
        "source_diagnostic_assessment_boundary_id": SOURCE_ASSESSMENT_BOUNDARY_ID,
        "source_discovery_execution_receipt_id": SOURCE_DISCOVERY_RECEIPT_ID,
        "source_discovery_result_id": SOURCE_DISCOVERY_RESULT_ID,
        "source_discovery_boundary_id": SOURCE_DISCOVERY_BOUNDARY_ID,
        "source_discovery_execution_authority_id": SOURCE_DISCOVERY_AUTHORITY_ID,
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
        "diagnostic_assessment_status": DIAGNOSTIC_ASSESSMENT_STATUS,
        "recommended_decision_class": RECOMMENDED_DECISION_CLASS,
        "diagnostic_assessment_accepted_for_feedback_hardening_decision": True,
        "authorized_future_unit_after_review": UNIT_ID,
        "authorized_future_unit_count_after_review": 1,
        "feedback_hardening_decision_packet_created_now": False,
        "additional_sample_discovery_now": False,
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
        chk(failures, f"acceptance_summary_{key}", summary.get(key), want)

    chk(failures, "acceptance_decision_id", decision.get("c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_decision_id"), SOURCE_ACCEPTANCE_DECISION_ID)
    chk(failures, "acceptance_packet_id", packet.get("c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_packet_id"), SOURCE_ACCEPTANCE_PACKET_ID)
    chk(failures, "acceptance_boundary_id", boundary.get("c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_acceptance_boundary_audit_id"), SOURCE_ACCEPTANCE_BOUNDARY_ID)

    chk(failures, "decision_packet_authority_id", authority.get("c8_unit_feedback_hardening_decision_packet_authority_id"), SOURCE_DECISION_PACKET_AUTHORITY_ID)
    chk(failures, "authority_authorized_future_unit", authority.get("authorized_future_unit"), UNIT_ID)
    chk(failures, "authority_authorized_future_unit_count", authority.get("authorized_future_unit_count"), 1)
    chk(failures, "authority_status", authority.get("authority_status"), "ACTIVE_AFTER_REVIEW_AND_COMMIT")

    scope = authority.get("authority_scope", {})
    chk(failures, "scope_may_create_one_feedback_hardening_decision_packet", scope.get("may_create_one_feedback_hardening_decision_packet"), True)
    chk(failures, "scope_may_create_feedback_hardening_decision_packet_now", scope.get("may_create_feedback_hardening_decision_packet_now"), False)
    chk(failures, "scope_may_execute_additional_sample_discovery", scope.get("may_execute_additional_sample_discovery"), False)
    chk(failures, "scope_may_authorize_probe_execution_now", scope.get("may_authorize_probe_execution_now"), False)
    chk(failures, "scope_may_execute_probe_now", scope.get("may_execute_probe_now"), False)
    chk(failures, "scope_may_build_now", scope.get("may_build_now"), False)
    chk(failures, "scope_may_rerun_c8_now", scope.get("may_rerun_c8_now"), False)
    chk(failures, "scope_may_promote_schema_now", scope.get("may_promote_schema_now"), False)

    decision_packet = {
        "schema_version": "c8_unit_feedback_hardening_decision_packet_v0",
        "c8_unit_feedback_hardening_decision_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "source_diagnostic_assessment_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_diagnostic_assessment_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
        "source_diagnostic_assessment_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_feedback_hardening_decision_packet_authority_id": SOURCE_DECISION_PACKET_AUTHORITY_ID,
        "source_diagnostic_assessment_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
        "source_diagnostic_assessment_receipt_id": SOURCE_ASSESSMENT_RECEIPT_ID,
        "source_diagnostic_assessment_packet_id": SOURCE_ASSESSMENT_PACKET_ID,
        "source_diagnostic_assessment_options_id": SOURCE_ASSESSMENT_OPTIONS_ID,
        "source_diagnostic_assessment_boundary_id": SOURCE_ASSESSMENT_BOUNDARY_ID,
        "source_discovery_execution_receipt_id": SOURCE_DISCOVERY_RECEIPT_ID,
        "source_discovery_result_id": SOURCE_DISCOVERY_RESULT_ID,
        "source_discovery_boundary_id": SOURCE_DISCOVERY_BOUNDARY_ID,
        "source_discovery_execution_authority_id": SOURCE_DISCOVERY_AUTHORITY_ID,
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
        "diagnostic_assessment_status": DIAGNOSTIC_ASSESSMENT_STATUS,
        "input_recommended_decision_class": RECOMMENDED_DECISION_CLASS,
        "feedback_hardening_decision_class": FEEDBACK_HARDENING_DECISION_CLASS,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "decision_read": (
            "Failed-unit diagnostic feedback is useful under the required why/where/relative/refinement rubric, "
            "while the sample also exposes a local source artifact status-field gap."
        ),
        "decision_consequence": (
            "Treat unit-feedback hardening as having obtained a useful failed-unit sample, and route the exposed "
            "source-status absence into one bounded gap-response packet rather than pretending the status exists."
        ),
        "source_status_gap_is_not_schema_promotion": True,
        "source_status_gap_response_created_now": False,
        "feedback_hardening_decision_packet_created_now": True,
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
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "recommended_review_unit": REVIEW_UNIT,
    }
    decision_packet["c8_unit_feedback_hardening_decision_packet_id"] = "c8_unit_feedback_hardening_decision_packet_" + sig8(decision_packet)
    write_json(DECISION_PACKET, decision_packet)

    options = {
        "schema_version": "c8_unit_feedback_hardening_decision_options_v0",
        "c8_unit_feedback_hardening_decision_options_id": None,
        "created_at": now_iso(),
        "source_feedback_hardening_decision_packet_id": decision_packet["c8_unit_feedback_hardening_decision_packet_id"],
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "human_decision_options": [
            RECOMMENDED_HUMAN_DECISION,
            "REJECT_C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_FROM_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT",
            "REQUEST_C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_REVISION_FROM_FAILED_UNIT_SAMPLE_DIAGNOSTIC_ASSESSMENT",
        ],
    }
    options["c8_unit_feedback_hardening_decision_options_id"] = "c8_unit_feedback_hardening_decision_options_" + sig8(options)
    write_json(DECISION_OPTIONS, options)

    boundary_audit = {
        "schema_version": "c8_unit_feedback_hardening_decision_packet_boundary_audit_v0",
        "c8_unit_feedback_hardening_decision_packet_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_feedback_hardening_decision_packet_id": decision_packet["c8_unit_feedback_hardening_decision_packet_id"],
        "source_feedback_hardening_decision_options_id": options["c8_unit_feedback_hardening_decision_options_id"],
        "source_feedback_hardening_decision_packet_authority_id": SOURCE_DECISION_PACKET_AUTHORITY_ID,
        "allowed_now": {
            "create_one_feedback_hardening_decision_packet": True,
            "emit_decision_packet_for_review": True,
        },
        "not_allowed_now": {
            "create_source_status_gap_response_now": True,
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
    boundary_audit["c8_unit_feedback_hardening_decision_packet_boundary_audit_id"] = "c8_unit_feedback_hardening_decision_packet_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    source_hashes_after = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }
    if source_hashes_before != source_hashes_after:
        forbidden_counters["source_artifact_mutation_count"] += 1
        failures.append("source_artifact_mutation_count:1")

    gate_results = {
        "FEEDBACK_HARDENING_DECISION_0_SOURCE_ACCEPTANCE_RECEIPT_PASS": receipt.get("gate") == "PASS",
        "FEEDBACK_HARDENING_DECISION_1_AUTHORITY_PRESENT_AND_ACTIVE": authority.get("authority_status") == "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "FEEDBACK_HARDENING_DECISION_2_AUTHORIZED_UNIT_MATCH": authority.get("authorized_future_unit") == UNIT_ID,
        "FEEDBACK_HARDENING_DECISION_3_ONE_DECISION_PACKET_CREATED": decision_packet["feedback_hardening_decision_packet_created_now"] is True,
        "FEEDBACK_HARDENING_DECISION_4_SOURCE_STATUS_GAP_RESPONSE_NOT_CREATED_NOW": decision_packet["source_status_gap_response_created_now"] is False,
        "FEEDBACK_HARDENING_DECISION_5_NO_DISCOVERY_PROBE_BUILD_RERUN_SCHEMA": decision_packet["additional_sample_discovery_now"] is False and decision_packet["probe_execution_authorized_now"] is False and decision_packet["instrument_build_authorized_now"] is False and decision_packet["c8_rerun_authorized_now"] is False and decision_packet["reusable_schema_authorized_now"] is False,
        "FEEDBACK_HARDENING_DECISION_6_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "FEEDBACK_HARDENING_DECISION_7_FORBIDDEN_COUNTERS_ZERO": all(v == 0 for v in forbidden_counters.values()),
        "FEEDBACK_HARDENING_DECISION_8_REQUIRES_REVIEW": decision_packet["requires_review"] is True,
        "FEEDBACK_HARDENING_DECISION_9_LOCAL_GAP_PRESERVED": decision_packet["local_gap_object"] == LOCAL_GAP_OBJECT and decision_packet["source_status_gap_is_not_schema_promotion"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"feedback_hardening_decision_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_FAIL"
    outcome = "C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_READY_FOR_REVIEW" if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_FAILED"
    terminal_stop = "STOP_C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_READY_FOR_REVIEW" if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_FAILED"

    readout = {
        "schema_version": "c8_unit_feedback_hardening_decision_packet_readout_v0",
        "title": "C8 unit-feedback hardening decision packet from failed-unit sample diagnostic assessment",
        "status": status,
        "outcome_class": outcome,
        "feedback_hardening_decision_class": FEEDBACK_HARDENING_DECISION_CLASS,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "diagnostic_assessment_status": DIAGNOSTIC_ASSESSMENT_STATUS,
        "decision_packet_created_now": True,
        "source_status_gap_response_created_now": False,
        "additional_sample_discovery_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "recommended_review_unit": REVIEW_UNIT,
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report_obj = {
        "schema_version": "c8_unit_feedback_hardening_decision_packet_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_diagnostic_assessment_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_feedback_hardening_decision_packet_authority_id": SOURCE_DECISION_PACKET_AUTHORITY_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "diagnostic_assessment_status": DIAGNOSTIC_ASSESSMENT_STATUS,
        "feedback_hardening_decision_class": FEEDBACK_HARDENING_DECISION_CLASS,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "decision_packet_created_now": True,
        "source_status_gap_response_created_now": False,
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
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "recommended_review_unit": REVIEW_UNIT,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report_obj)

    receipt_obj = {
        "schema_version": "c8_unit_feedback_hardening_decision_packet_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_DECISION_PACKET_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_decision_packet_summary": {
            "feedback_hardening_decision_packet_created": gate == "PASS",
            "authorized_unit_consumed": UNIT_ID,
            "source_diagnostic_assessment_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
            "source_diagnostic_assessment_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
            "source_diagnostic_assessment_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
            "source_feedback_hardening_decision_packet_authority_id": SOURCE_DECISION_PACKET_AUTHORITY_ID,
            "source_diagnostic_assessment_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
            "source_diagnostic_assessment_receipt_id": SOURCE_ASSESSMENT_RECEIPT_ID,
            "source_diagnostic_assessment_packet_id": SOURCE_ASSESSMENT_PACKET_ID,
            "source_diagnostic_assessment_options_id": SOURCE_ASSESSMENT_OPTIONS_ID,
            "source_diagnostic_assessment_boundary_id": SOURCE_ASSESSMENT_BOUNDARY_ID,
            "source_discovery_execution_receipt_id": SOURCE_DISCOVERY_RECEIPT_ID,
            "source_discovery_result_id": SOURCE_DISCOVERY_RESULT_ID,
            "source_discovery_boundary_id": SOURCE_DISCOVERY_BOUNDARY_ID,
            "source_discovery_execution_authority_id": SOURCE_DISCOVERY_AUTHORITY_ID,
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
            "diagnostic_assessment_status": DIAGNOSTIC_ASSESSMENT_STATUS,
            "input_recommended_decision_class": RECOMMENDED_DECISION_CLASS,
            "feedback_hardening_decision_class": FEEDBACK_HARDENING_DECISION_CLASS,
            "local_gap_object": LOCAL_GAP_OBJECT,
            "decision_packet_created_now": True,
            "source_status_gap_response_created_now": False,
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
            "forbidden_counters_zero": all(v == 0 for v in forbidden_counters.values()),
            "requires_review": True,
            "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
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
            "feedback_hardening_decision_packet": rel(DECISION_PACKET),
            "feedback_hardening_decision_options": rel(DECISION_OPTIONS),
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

    receipt_obj["receipt_id"] = "c8_unit_feedback_hardening_decision_packet_receipt_" + sig8(receipt_obj)
    receipt_path = RECEIPT_DIR / f"{receipt_obj['receipt_id']}.json"
    receipt_obj["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_obj)

    print(json.dumps(receipt_obj, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_decision_packet_receipt_id={receipt_obj['receipt_id']}")
    print(f"c8_unit_feedback_hardening_decision_packet_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_decision_packet_path={rel(DECISION_PACKET)}")
    print(f"c8_unit_feedback_hardening_decision_options_path={rel(DECISION_OPTIONS)}")
    print(f"c8_unit_feedback_hardening_decision_packet_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"failed_unit_sample_id={FAILED_UNIT_SAMPLE_ID}")
    print(f"diagnostic_assessment_status={DIAGNOSTIC_ASSESSMENT_STATUS}")
    print(f"feedback_hardening_decision_class={FEEDBACK_HARDENING_DECISION_CLASS}")
    print(f"local_gap_object={LOCAL_GAP_OBJECT}")
    print("decision_packet_created_now=true")
    print("source_status_gap_response_created_now=false")
    print("additional_sample_discovery_now=false")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_human_decision={RECOMMENDED_HUMAN_DECISION}")
    print(f"if_accepted_authorizes_future_unit={FUTURE_UNIT}")
    print(f"recommended_review_unit={REVIEW_UNIT}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
