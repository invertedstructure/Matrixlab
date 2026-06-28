#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_FOR_ONE_BOUNDED_DISCOVERY_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.failed_unit_sample.discovery_prep.acceptance.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_ACCEPTED_FOR_ONE_BOUNDED_DISCOVERY_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE"
OUTCOME = "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_ACCEPTED_FOR_ONE_BOUNDED_DISCOVERY_EXECUTION"
STOP_CODE = "STOP_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_ACCEPTANCE_READY_FOR_REVIEW"

HUMAN_DECISION = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_FOR_ONE_BOUNDED_DISCOVERY_EXECUTION"
AUTHORIZED_FUTURE_UNIT = "EXECUTE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
RECOMMENDED_REVIEW_UNIT = "REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_ACCEPTANCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

SOURCE_DISCOVERY_PREP_RECEIPT_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_receipt_3e05bd98"
SOURCE_DISCOVERY_PREP_PACKET_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_packet_80abb45c"
SOURCE_DISCOVERY_PREP_OPTIONS_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_options_e69fd27d"
SOURCE_DISCOVERY_PREP_BOUNDARY_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_boundary_ee5732f7"

SOURCE_GAP_RESPONSE_ACCEPTANCE_RECEIPT_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_receipt_a352ace8"
SOURCE_GAP_RESPONSE_ACCEPTANCE_DECISION_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_decision_1d2f3b7c"
SOURCE_GAP_RESPONSE_ACCEPTANCE_PACKET_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_packet_aa5a2900"
SOURCE_DISCOVERY_PREP_AUTHORITY_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_authority_d3369fc7"
SOURCE_GAP_RESPONSE_ACCEPTANCE_BOUNDARY_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_boundary_18de4ed4"

SOURCE_GAP_RESPONSE_RECEIPT_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_receipt_78fa641a"
SOURCE_GAP_RESPONSE_PACKET_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_packet_109ffc4d"
SOURCE_GAP_RESPONSE_OPTIONS_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_options_0b2e001f"
SOURCE_GAP_RESPONSE_BOUNDARY_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_boundary_a299dd48"

SELECTED_SURFACE_ID = "c8_successor_surface_unit_feedback_hardening_after_runtime_adoption_closure_v0"
SELECTED_SURFACE_KIND = "UNIT_FEEDBACK_HARDENING_SURFACE"
SELECTED_SURFACE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_AFTER_RUNTIME_ADOPTION_CLOSURE_SURFACE"

PROBE_ID = "c8_unit_feedback_hardening_bounded_probe_after_runtime_adoption_closure_v0"
PROBE_KIND = "UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE"
PROBE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_AFTER_RUNTIME_ADOPTION_CLOSURE"

GAP_OBJECT = "FAILED_UNIT_SAMPLE_ABSENCE"
OBSERVATION_CLASS = "UNIT_FEEDBACK_DIAGNOSTIC_FEEDBACK_PARTIAL_NO_FAILED_UNIT_SAMPLE_OBSERVED"
OBSERVATION_VERDICT = "PARTIAL"
DIAGNOSTIC_GAP = "No failed-unit sample was present in the bounded source set, so the probe can verify typed-stop/status/context/refinement structure but cannot fully validate failed-unit diagnostic quality."
SELECTED_GAP_RESPONSE_KIND = "BOUNDED_FAILED_UNIT_SAMPLE_DISCOVERY_PREP"
DISCOVERY_TARGET = "ONE_FAILED_UNIT_SAMPLE"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_after_runtime_adoption_closure_v0_receipts"

DISCOVERY_PREP_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_receipt_3e05bd98.json"
DISCOVERY_PREP_PACKET = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_packet_v0.json"
DISCOVERY_PREP_OPTIONS = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_options_v0.json"
DISCOVERY_PREP_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_boundary_audit_v0.json"
DISCOVERY_PREP_READOUT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_readout_v0.json"
DISCOVERY_PREP_REPORT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_report.json"

ACCEPTANCE_DECISION = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_packet_v0.json"
DISCOVERY_EXECUTION_AUTHORITY = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_authority_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "sample_discovery_executed_count",
    "failed_unit_sample_found_count",
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
        "discovery_prep_receipt": DISCOVERY_PREP_RECEIPT,
        "discovery_prep_packet": DISCOVERY_PREP_PACKET,
        "discovery_prep_options": DISCOVERY_PREP_OPTIONS,
        "discovery_prep_boundary": DISCOVERY_PREP_BOUNDARY,
        "discovery_prep_readout": DISCOVERY_PREP_READOUT,
        "discovery_prep_report": DISCOVERY_PREP_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    receipt = read_json(DISCOVERY_PREP_RECEIPT)
    packet = read_json(DISCOVERY_PREP_PACKET)
    options = read_json(DISCOVERY_PREP_OPTIONS)
    boundary = read_json(DISCOVERY_PREP_BOUNDARY)
    readout = read_json(DISCOVERY_PREP_READOUT)
    report = read_json(DISCOVERY_PREP_REPORT)
    summary = receipt.get("machine_readable_unit_feedback_hardening_failed_unit_sample_discovery_prep_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_READY_FOR_REVIEW",
        "receipt_id": SOURCE_DISCOVERY_PREP_RECEIPT_ID,
    }
    for key, want in expected_receipt.items():
        chk(failures, f"discovery_prep_receipt_{key}", receipt.get(key), want)

    expected_summary = {
        "failed_unit_sample_discovery_prep_packet_created": True,
        "authorized_unit_consumed": "CREATE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "source_gap_response_acceptance_receipt_id": SOURCE_GAP_RESPONSE_ACCEPTANCE_RECEIPT_ID,
        "source_gap_response_acceptance_decision_id": SOURCE_GAP_RESPONSE_ACCEPTANCE_DECISION_ID,
        "source_gap_response_acceptance_packet_id": SOURCE_GAP_RESPONSE_ACCEPTANCE_PACKET_ID,
        "source_discovery_prep_authority_id": SOURCE_DISCOVERY_PREP_AUTHORITY_ID,
        "source_gap_response_acceptance_boundary_id": SOURCE_GAP_RESPONSE_ACCEPTANCE_BOUNDARY_ID,
        "source_gap_response_receipt_id": SOURCE_GAP_RESPONSE_RECEIPT_ID,
        "source_gap_response_packet_id": SOURCE_GAP_RESPONSE_PACKET_ID,
        "source_gap_response_options_id": SOURCE_GAP_RESPONSE_OPTIONS_ID,
        "source_gap_response_boundary_id": SOURCE_GAP_RESPONSE_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "gap_object": GAP_OBJECT,
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "failed_unit_sample_count_before_discovery": 0,
        "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
        "discovery_target": DISCOVERY_TARGET,
        "discovery_prep_packet_created_now": True,
        "sample_discovery_authorized_now": False,
        "sample_discovery_executed_now": False,
        "failed_unit_sample_found_now": False,
        "failed_unit_sample_count_now": 0,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized": False,
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
        "recommended_human_decision": HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "recommended_review_unit": "REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "next_command_goal": None,
    }
    for key, want in expected_summary.items():
        chk(failures, f"discovery_prep_summary_{key}", summary.get(key), want)

    expected_ids = {
        "discovery_prep_packet_id": (
            packet.get("c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_packet_id"),
            SOURCE_DISCOVERY_PREP_PACKET_ID,
        ),
        "discovery_prep_options_id": (
            options.get("c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_options_id"),
            SOURCE_DISCOVERY_PREP_OPTIONS_ID,
        ),
        "discovery_prep_boundary_id": (
            boundary.get("c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_boundary_audit_id"),
            SOURCE_DISCOVERY_PREP_BOUNDARY_ID,
        ),
    }
    for label, (got, want) in expected_ids.items():
        if got != want:
            failures.append(f"{label}_wrong:{got}!={want}")

    if options.get("recommended_human_decision") != HUMAN_DECISION:
        failures.append(f"options_recommended_human_decision_wrong:{options.get('recommended_human_decision')}")
    if options.get("if_accepted_authorizes_future_unit") != AUTHORIZED_FUTURE_UNIT:
        failures.append(f"options_future_unit_wrong:{options.get('if_accepted_authorizes_future_unit')}")

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
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_decision_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_decision_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "human_decision": HUMAN_DECISION,
        "human_decision_consumed": True,
        "source_discovery_prep_receipt_id": SOURCE_DISCOVERY_PREP_RECEIPT_ID,
        "source_discovery_prep_packet_id": SOURCE_DISCOVERY_PREP_PACKET_ID,
        "source_discovery_prep_options_id": SOURCE_DISCOVERY_PREP_OPTIONS_ID,
        "source_discovery_prep_boundary_id": SOURCE_DISCOVERY_PREP_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "gap_object": GAP_OBJECT,
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "failed_unit_sample_count_before_discovery": 0,
        "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
        "discovery_target": DISCOVERY_TARGET,
        "discovery_prep_accepted_for_one_bounded_discovery_execution": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "sample_discovery_execution_authorized_now": False,
        "sample_discovery_executed_now": False,
        "failed_unit_sample_found_now": False,
        "failed_unit_sample_count_now": 0,
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
    decision["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_decision_id"] = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_decision_" + sig8(decision)
    write_json(ACCEPTANCE_DECISION, decision)

    execution_authority = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_authority_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_authority_id": None,
        "created_at": now_iso(),
        "source_discovery_prep_acceptance_decision_id": decision["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_decision_id"],
        "source_discovery_prep_packet_id": SOURCE_DISCOVERY_PREP_PACKET_ID,
        "source_discovery_prep_receipt_id": SOURCE_DISCOVERY_PREP_RECEIPT_ID,
        "gap_object": GAP_OBJECT,
        "discovery_target": DISCOVERY_TARGET,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "execution_limit": 1,
        "authority_status": "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "authority_scope": {
            "may_execute_one_bounded_failed_unit_sample_discovery": True,
            "may_return_at_most_one_failed_unit_sample": True,
            "may_authorize_probe_execution_now": False,
            "may_execute_probe_now": False,
            "may_build_now": False,
            "may_rerun_c8_now": False,
            "may_promote_schema_now": False,
        },
    }
    execution_authority["c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_authority_id"] = "c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_authority_" + sig8(execution_authority)
    write_json(DISCOVERY_EXECUTION_AUTHORITY, execution_authority)

    acceptance_packet = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_packet_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "acceptance_status": "FAILED_UNIT_SAMPLE_DISCOVERY_PREP_ACCEPTED_FOR_ONE_BOUNDED_DISCOVERY_EXECUTION",
        "human_decision": HUMAN_DECISION,
        "source_discovery_prep_acceptance_decision_id": decision["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_decision_id"],
        "source_discovery_execution_authority_id": execution_authority["c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_authority_id"],
        "source_discovery_prep_receipt_id": SOURCE_DISCOVERY_PREP_RECEIPT_ID,
        "source_discovery_prep_packet_id": SOURCE_DISCOVERY_PREP_PACKET_ID,
        "source_discovery_prep_options_id": SOURCE_DISCOVERY_PREP_OPTIONS_ID,
        "source_discovery_prep_boundary_id": SOURCE_DISCOVERY_PREP_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "gap_object": GAP_OBJECT,
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "failed_unit_sample_count_before_discovery": 0,
        "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
        "discovery_target": DISCOVERY_TARGET,
        "discovery_prep_accepted_for_one_bounded_discovery_execution": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "execution_limit_after_review": 1,
        "sample_discovery_execution_authorized_now": False,
        "sample_discovery_executed_now": False,
        "failed_unit_sample_found_now": False,
        "failed_unit_sample_count_now": 0,
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
        "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
    }
    acceptance_packet["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_packet_id"] = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_packet_" + sig8(acceptance_packet)
    write_json(ACCEPTANCE_PACKET, acceptance_packet)

    boundary_audit = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_boundary_audit_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_discovery_prep_acceptance_decision_id": decision["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_decision_id"],
        "source_discovery_prep_acceptance_packet_id": acceptance_packet["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_packet_id"],
        "source_discovery_execution_authority_id": execution_authority["c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_authority_id"],
        "source_discovery_prep_receipt_id": SOURCE_DISCOVERY_PREP_RECEIPT_ID,
        "source_discovery_prep_packet_id": SOURCE_DISCOVERY_PREP_PACKET_ID,
        "allowed_now": {
            "accept_discovery_prep_for_one_bounded_discovery_execution": True,
            "authorize_one_bounded_discovery_execution_after_review_and_commit": True,
        },
        "not_allowed_now": {
            "execute_sample_discovery_now": True,
            "claim_failed_unit_sample_found_now": True,
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
    boundary_audit["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_boundary_audit_id"] = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    gate_results = {
        "DISCOVERY_PREP_ACCEPTANCE_0_SOURCE_RECEIPT_PASS": receipt.get("gate") == "PASS",
        "DISCOVERY_PREP_ACCEPTANCE_1_HUMAN_DECISION_MATCH": summary.get("recommended_human_decision") == HUMAN_DECISION,
        "DISCOVERY_PREP_ACCEPTANCE_2_FUTURE_UNIT_MATCH": summary.get("if_accepted_authorizes_future_unit") == AUTHORIZED_FUTURE_UNIT,
        "DISCOVERY_PREP_ACCEPTANCE_3_ONE_SAMPLE_TARGET_PRESERVED": packet.get("discovery_target") == DISCOVERY_TARGET,
        "DISCOVERY_PREP_ACCEPTANCE_4_ACCEPTANCE_RECORDED": acceptance_packet["discovery_prep_accepted_for_one_bounded_discovery_execution"] is True,
        "DISCOVERY_PREP_ACCEPTANCE_5_EXECUTION_LIMIT_ONE": execution_authority["execution_limit"] == 1 and acceptance_packet["execution_limit_after_review"] == 1,
        "DISCOVERY_PREP_ACCEPTANCE_6_DISCOVERY_NOT_EXECUTED_NOW": acceptance_packet["sample_discovery_executed_now"] is False,
        "DISCOVERY_PREP_ACCEPTANCE_7_NO_SAMPLE_FOUND_NOW": acceptance_packet["failed_unit_sample_found_now"] is False and acceptance_packet["failed_unit_sample_count_now"] == 0,
        "DISCOVERY_PREP_ACCEPTANCE_8_NO_PROBE_BUILD_RERUN_SCHEMA": acceptance_packet["probe_execution_authorized_now"] is False and acceptance_packet["instrument_build_authorized_now"] is False and acceptance_packet["c8_rerun_authorized_now"] is False and acceptance_packet["reusable_schema_authorized_now"] is False,
        "DISCOVERY_PREP_ACCEPTANCE_9_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "DISCOVERY_PREP_ACCEPTANCE_10_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "DISCOVERY_PREP_ACCEPTANCE_11_REQUIRES_REVIEW": acceptance_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"discovery_prep_acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_ACCEPTANCE_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_ACCEPTANCE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_ACCEPTANCE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_ACCEPTANCE_FAILED"

    readout_obj = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_readout_v0",
        "title": "C8 unit-feedback hardening failed-unit sample discovery-prep acceptance after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "discovery_prep_accepted_for_one_bounded_discovery_execution": True,
        "gap_object": GAP_OBJECT,
        "discovery_target": DISCOVERY_TARGET,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "execution_limit_after_review": 1,
        "sample_discovery_execution_authorized_now": False,
        "sample_discovery_executed_now": False,
        "failed_unit_sample_found_now": False,
        "failed_unit_sample_count_now": 0,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout_obj)

    report_obj = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "source_discovery_prep_receipt_id": SOURCE_DISCOVERY_PREP_RECEIPT_ID,
        "source_discovery_prep_packet_id": SOURCE_DISCOVERY_PREP_PACKET_ID,
        "source_discovery_prep_options_id": SOURCE_DISCOVERY_PREP_OPTIONS_ID,
        "source_discovery_prep_boundary_id": SOURCE_DISCOVERY_PREP_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "gap_object": GAP_OBJECT,
        "discovery_target": DISCOVERY_TARGET,
        "discovery_prep_accepted_for_one_bounded_discovery_execution": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "execution_limit_after_review": 1,
        "sample_discovery_execution_authorized_now": False,
        "sample_discovery_executed_now": False,
        "failed_unit_sample_found_now": False,
        "failed_unit_sample_count_now": 0,
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
        "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report_obj)

    receipt_obj = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_ACCEPTANCE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_summary": {
            "discovery_prep_acceptance_complete": gate == "PASS",
            "human_decision": HUMAN_DECISION,
            "source_discovery_prep_receipt_id": SOURCE_DISCOVERY_PREP_RECEIPT_ID,
            "source_discovery_prep_packet_id": SOURCE_DISCOVERY_PREP_PACKET_ID,
            "source_discovery_prep_options_id": SOURCE_DISCOVERY_PREP_OPTIONS_ID,
            "source_discovery_prep_boundary_id": SOURCE_DISCOVERY_PREP_BOUNDARY_ID,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "probe_label": PROBE_LABEL,
            "gap_object": GAP_OBJECT,
            "observation_class": OBSERVATION_CLASS,
            "observation_verdict": OBSERVATION_VERDICT,
            "diagnostic_gap": DIAGNOSTIC_GAP,
            "failed_unit_sample_count_before_discovery": 0,
            "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
            "discovery_target": DISCOVERY_TARGET,
            "discovery_prep_accepted_for_one_bounded_discovery_execution": True,
            "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
            "authorized_future_unit_count_after_review": 1,
            "execution_limit_after_review": 1,
            "sample_discovery_execution_authorized_now": False,
            "sample_discovery_executed_now": False,
            "failed_unit_sample_found_now": False,
            "failed_unit_sample_count_now": 0,
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
            "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
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
            "discovery_prep_acceptance_decision": rel(ACCEPTANCE_DECISION),
            "discovery_prep_acceptance_packet": rel(ACCEPTANCE_PACKET),
            "discovery_execution_authority": rel(DISCOVERY_EXECUTION_AUTHORITY),
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

    receipt_obj["receipt_id"] = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_receipt_" + sig8(receipt_obj)
    receipt_path = RECEIPT_DIR / f"{receipt_obj['receipt_id']}.json"
    receipt_obj["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_obj)

    print(json.dumps(receipt_obj, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_receipt_id={receipt_obj['receipt_id']}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_decision_path={rel(ACCEPTANCE_DECISION)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_packet_path={rel(ACCEPTANCE_PACKET)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_authority_path={rel(DISCOVERY_EXECUTION_AUTHORITY)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"human_decision={HUMAN_DECISION}")
    print("discovery_prep_accepted_for_one_bounded_discovery_execution=true")
    print(f"gap_object={GAP_OBJECT}")
    print(f"discovery_target={DISCOVERY_TARGET}")
    print(f"authorized_future_unit_after_review={AUTHORIZED_FUTURE_UNIT}")
    print("authorized_future_unit_count_after_review=1")
    print("execution_limit_after_review=1")
    print("sample_discovery_execution_authorized_now=false")
    print("sample_discovery_executed_now=false")
    print("failed_unit_sample_found_now=false")
    print("failed_unit_sample_count_now=0")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={RECOMMENDED_REVIEW_UNIT}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
