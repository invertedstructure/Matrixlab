#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_FOR_EXECUTION_AFTER_REENTRY_V0"
TARGET_UNIT_ID = "research.c8.runtime_adoption_surface.bounded_probe.accept_for_execution.after_reentry.v0"
MILESTONE = "C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_ACCEPTED_FOR_ONE_EXECUTION_AFTER_REENTRY"
OUTCOME = "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_ACCEPTED_FOR_ONE_BOUNDED_EXECUTION_ONLY"
STOP_CODE = "STOP_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_EXECUTION_ACCEPTANCE_READY_FOR_REVIEW"

HUMAN_DECISION = "ACCEPT_FOR_BOUNDED_PROBE_EXECUTION"
AUTHORIZED_FUTURE_UNIT = "EXECUTE_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_AFTER_REENTRY_V0"

SOURCE_PREP_RECEIPT_ID = "c8_runtime_adoption_bounded_probe_prep_receipt_0fc181c6"
SOURCE_PROBE_SPEC_ID = "c8_runtime_adoption_bounded_probe_spec_d39f5710"
SOURCE_PREP_PACKET_ID = "c8_runtime_adoption_bounded_probe_prep_packet_23020f7d"
SOURCE_PREP_BOUNDARY_ID = "c8_runtime_adoption_bounded_probe_prep_boundary_fe200a33"

SOURCE_ACCEPTANCE_RECEIPT_ID = "c8_runtime_adoption_probe_prep_acceptance_receipt_6928390f"
SOURCE_ACCEPTANCE_DECISION_ID = "c8_runtime_adoption_probe_prep_acceptance_decision_5054ed94"
SOURCE_ACCEPTANCE_PACKET_ID = "c8_runtime_adoption_probe_prep_acceptance_packet_85d617c2"
SOURCE_AUTHORITY_ID = "c8_runtime_adoption_probe_prep_authority_ae554f5e"
SOURCE_ACCEPTANCE_BOUNDARY_ID = "c8_runtime_adoption_probe_prep_acceptance_boundary_2783c3e7"

SOURCE_SELECTION_RECEIPT_ID = "c8_successor_surface_selection_receipt_7da4fd41"
SOURCE_SELECTION_DECISION_ID = "c8_successor_surface_selection_decision_4f336833"
SOURCE_SELECTION_PACKET_ID = "c8_successor_surface_selection_packet_f7874bf3"
SOURCE_SELECTION_BOUNDARY_ID = "c8_successor_surface_selection_boundary_ee54442b"

PREVIOUS_SURFACE_ID = "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0"
PREVIOUS_SURFACE_KIND = "REUSE_AUTHORITY_BOUNDARY_SURFACE"
PREVIOUS_SURFACE_LABEL = "C8_POST_CLOSURE_LOCAL_LOOP_REUSE_PRESSURE_SURFACE"

SELECTED_SURFACE_ID = "c8_successor_surface_runtime_adoption_after_reentry_v0"
SELECTED_SURFACE_KIND = "RUNTIME_ADOPTION_SURFACE"
SELECTED_SURFACE_LABEL = "C8_RUNTIME_ADOPTION_AFTER_REUSE_AUTHORITY_CLOSURE_SURFACE"
SELECTED_SURFACE_QUESTION = (
    "After the reuse-authority boundary held and surface-selection reentry was accepted, "
    "what is the smallest runtime-adoption surface that can expose typed halts, receipt mismatches, "
    "projection bugs, missing moves, or gate failures without pre-authorizing build, probe execution, "
    "C8 rerun, or reusable schema promotion?"
)

PROBE_ID = "c8_runtime_adoption_surface_bounded_probe_after_reentry_v0"
PROBE_KIND = "RUNTIME_ADOPTION_BOUNDARY_PROBE"
PROBE_LABEL = "C8_RUNTIME_ADOPTION_BOUNDED_PROBE_AFTER_REENTRY"
PROBE_QUESTION = (
    "What is the smallest controlled runtime-adoption probe that can expose typed halts, "
    "receipt mismatches, projection bugs, missing moves, or gate failures from the committed C8 chain, "
    "while stopping before probe execution authority, runtime build, C8 rerun, or reusable schema promotion?"
)

OUT_DIR = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_acceptance_after_reentry_v0"
RECEIPT_DIR = ROOT / "data/c8_runtime_adoption_bounded_probe_execution_acceptance_after_reentry_v0_receipts"

PREP_RECEIPT = ROOT / "data/c8_runtime_adoption_surface_bounded_probe_prep_after_reentry_v0_receipts/c8_runtime_adoption_bounded_probe_prep_receipt_0fc181c6.json"
PROBE_SPEC = ROOT / "data/c8_runtime_adoption_surface_bounded_probe_prep_after_reentry_v0/c8_runtime_adoption_surface_bounded_probe_spec_v0.json"
PREP_PACKET = ROOT / "data/c8_runtime_adoption_surface_bounded_probe_prep_after_reentry_v0/c8_runtime_adoption_surface_bounded_probe_prep_packet_v0.json"
PREP_BOUNDARY = ROOT / "data/c8_runtime_adoption_surface_bounded_probe_prep_after_reentry_v0/c8_runtime_adoption_surface_bounded_probe_prep_boundary_audit_v0.json"
PREP_REPORT = ROOT / "data/c8_runtime_adoption_surface_bounded_probe_prep_after_reentry_v0/c8_runtime_adoption_surface_bounded_probe_prep_report.json"

EXECUTION_ACCEPTANCE_DECISION = OUT_DIR / "c8_runtime_adoption_bounded_probe_execution_acceptance_decision_v0.json"
EXECUTION_ACCEPTANCE_PACKET = OUT_DIR / "c8_runtime_adoption_bounded_probe_execution_acceptance_packet_v0.json"
EXECUTION_AUTHORITY = OUT_DIR / "c8_runtime_adoption_bounded_probe_execution_authority_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_runtime_adoption_bounded_probe_execution_acceptance_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_runtime_adoption_bounded_probe_execution_acceptance_readout_v0.json"
REPORT = OUT_DIR / "c8_runtime_adoption_bounded_probe_execution_acceptance_report.json"

FORBIDDEN_COUNTER_KEYS = [
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
        "prep_receipt": PREP_RECEIPT,
        "probe_spec": PROBE_SPEC,
        "prep_packet": PREP_PACKET,
        "prep_boundary": PREP_BOUNDARY,
        "prep_report": PREP_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    prep_receipt = read_json(PREP_RECEIPT)
    probe_spec = read_json(PROBE_SPEC)
    prep_packet = read_json(PREP_PACKET)
    prep_boundary = read_json(PREP_BOUNDARY)
    prep_report = read_json(PREP_REPORT)
    prep_summary = prep_receipt.get("machine_readable_prep_summary", {})

    expected_prep_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_PASS",
        "outcome_class": "C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_READY_FOR_REVIEW",
        "receipt_id": SOURCE_PREP_RECEIPT_ID,
    }

    for key, want in expected_prep_receipt.items():
        chk(failures, f"prep_receipt_{key}", prep_receipt.get(key), want)

    expected_prep_summary = {
        "runtime_adoption_bounded_probe_prep_packet_created": True,
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
        "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_authority_id": SOURCE_AUTHORITY_ID,
        "source_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_selection_decision_id": SOURCE_SELECTION_DECISION_ID,
        "source_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
        "source_selection_boundary_id": SOURCE_SELECTION_BOUNDARY_ID,
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_question": SELECTED_SURFACE_QUESTION,
        "authorized_future_unit_consumed": "CREATE_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_AFTER_REENTRY_V0",
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_question": PROBE_QUESTION,
        "probe_prep_packet_created": True,
        "probe_prepared_for_review": True,
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
        "recommended_review_unit": "REVIEW_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_AFTER_REENTRY_V0",
        "next_command_goal": None,
    }

    for key, want in expected_prep_summary.items():
        chk(failures, f"prep_summary_{key}", prep_summary.get(key), want)

    expected_options = [
        "ACCEPT_FOR_BOUNDED_PROBE_EXECUTION",
        "REJECT_PROBE_PREP_PACKET",
        "NARROW_PROBE_PREP_PACKET",
    ]

    if prep_summary.get("recommended_next_decision_options") != expected_options:
        failures.append(f"prep_summary_options_wrong:{prep_summary.get('recommended_next_decision_options')}")
    if HUMAN_DECISION not in prep_summary.get("recommended_next_decision_options", []):
        failures.append(f"human_decision_not_available:{HUMAN_DECISION}")

    chk(failures, "probe_spec_id", probe_spec.get("runtime_adoption_bounded_probe_spec_id"), SOURCE_PROBE_SPEC_ID)
    chk(failures, "prep_packet_id", prep_packet.get("runtime_adoption_bounded_probe_prep_packet_id"), SOURCE_PREP_PACKET_ID)
    chk(failures, "prep_boundary_id", prep_boundary.get("runtime_adoption_bounded_probe_prep_boundary_audit_id"), SOURCE_PREP_BOUNDARY_ID)

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
        "schema_version": "c8_runtime_adoption_bounded_probe_execution_acceptance_decision_v0",
        "runtime_adoption_bounded_probe_execution_acceptance_decision_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "human_decision": HUMAN_DECISION,
        "human_decision_consumed": True,
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
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_execution_count": 1,
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
    acceptance_decision["runtime_adoption_bounded_probe_execution_acceptance_decision_id"] = "c8_runtime_adoption_bounded_probe_execution_acceptance_decision_" + sig8(acceptance_decision)
    write_json(EXECUTION_ACCEPTANCE_DECISION, acceptance_decision)

    execution_authority = {
        "schema_version": "c8_runtime_adoption_bounded_probe_execution_authority_v0",
        "runtime_adoption_bounded_probe_execution_authority_id": None,
        "created_at": now_iso(),
        "authority_status": "AUTHORIZED_FOR_ONE_BOUNDED_PROBE_EXECUTION_ONLY",
        "source_execution_acceptance_decision_id": acceptance_decision["runtime_adoption_bounded_probe_execution_acceptance_decision_id"],
        "source_prep_receipt_id": SOURCE_PREP_RECEIPT_ID,
        "source_probe_spec_id": SOURCE_PROBE_SPEC_ID,
        "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_execution_count": 1,
        "authorized_scope": {
            "execute_bounded_probe": True,
            "max_execution_count": 1,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "surface_id": SELECTED_SURFACE_ID,
            "surface_kind": SELECTED_SURFACE_KIND,
        },
        "not_authorized": {
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
    }
    execution_authority["runtime_adoption_bounded_probe_execution_authority_id"] = "c8_runtime_adoption_bounded_probe_execution_authority_" + sig8(execution_authority)
    write_json(EXECUTION_AUTHORITY, execution_authority)

    acceptance_packet = {
        "schema_version": "c8_runtime_adoption_bounded_probe_execution_acceptance_packet_v0",
        "runtime_adoption_bounded_probe_execution_acceptance_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "acceptance_status": "RUNTIME_ADOPTION_BOUNDED_PROBE_ACCEPTED_FOR_ONE_EXECUTION_ONLY",
        "human_decision": HUMAN_DECISION,
        "source_prep_receipt_id": SOURCE_PREP_RECEIPT_ID,
        "source_probe_spec_id": SOURCE_PROBE_SPEC_ID,
        "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
        "source_prep_boundary_id": SOURCE_PREP_BOUNDARY_ID,
        "source_execution_acceptance_decision_id": acceptance_decision["runtime_adoption_bounded_probe_execution_acceptance_decision_id"],
        "source_execution_authority_id": execution_authority["runtime_adoption_bounded_probe_execution_authority_id"],
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_question": PROBE_QUESTION,
        "bounded_probe_execution_authorized": True,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_execution_count": 1,
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
        "recommended_review_unit": "REVIEW_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_AFTER_REENTRY_V0",
    }
    acceptance_packet["runtime_adoption_bounded_probe_execution_acceptance_packet_id"] = "c8_runtime_adoption_bounded_probe_execution_acceptance_packet_" + sig8(acceptance_packet)
    write_json(EXECUTION_ACCEPTANCE_PACKET, acceptance_packet)

    boundary_audit = {
        "schema_version": "c8_runtime_adoption_bounded_probe_execution_acceptance_boundary_audit_v0",
        "runtime_adoption_bounded_probe_execution_acceptance_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_execution_acceptance_packet_id": acceptance_packet["runtime_adoption_bounded_probe_execution_acceptance_packet_id"],
        "source_execution_acceptance_decision_id": acceptance_decision["runtime_adoption_bounded_probe_execution_acceptance_decision_id"],
        "source_execution_authority_id": execution_authority["runtime_adoption_bounded_probe_execution_authority_id"],
        "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
        "source_probe_spec_id": SOURCE_PROBE_SPEC_ID,
        "allowed_now": {
            "record_probe_execution_acceptance": True,
            "authorize_one_future_bounded_probe_execution": True,
        },
        "not_allowed_now": {
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
    boundary_audit["runtime_adoption_bounded_probe_execution_acceptance_boundary_audit_id"] = "c8_runtime_adoption_bounded_probe_execution_acceptance_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    gate_results = {
        "EXECUTION_ACCEPTANCE_0_SOURCE_PREP_RECEIPT_PASS": prep_receipt.get("gate") == "PASS",
        "EXECUTION_ACCEPTANCE_1_PROBE_PREP_READY_FOR_REVIEW": prep_packet.get("prep_packet_status") == "BOUNDED_PROBE_PREP_PACKET_READY_FOR_REVIEW",
        "EXECUTION_ACCEPTANCE_2_HUMAN_DECISION_AVAILABLE": HUMAN_DECISION in prep_summary.get("recommended_next_decision_options", []),
        "EXECUTION_ACCEPTANCE_3_EXACTLY_ONE_EXECUTION_AUTHORIZED": acceptance_packet["authorized_future_unit_count"] == 1 and acceptance_packet["authorized_future_unit"] == AUTHORIZED_FUTURE_UNIT,
        "EXECUTION_ACCEPTANCE_4_EXECUTION_NOT_RUN_NOW": acceptance_packet["probe_executed_now"] is False,
        "EXECUTION_ACCEPTANCE_5_NO_BUILD_RERUN_SCHEMA": acceptance_packet["instrument_build_authorized_now"] is False and acceptance_packet["c8_rerun_authorized_now"] is False and acceptance_packet["reusable_schema_authorized_now"] is False,
        "EXECUTION_ACCEPTANCE_6_NO_GLOBAL_OR_FRONTIER_CLAIM": acceptance_packet["global_solution_claim"] is False and acceptance_packet["frontier_solved_claim"] is False,
        "EXECUTION_ACCEPTANCE_7_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "EXECUTION_ACCEPTANCE_8_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "EXECUTION_ACCEPTANCE_9_RESULT_REQUIRES_REVIEW": acceptance_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"execution_acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_RUNTIME_ADOPTION_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_PASS" if gate == "PASS" else "TYPED_C8_RUNTIME_ADOPTION_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_EXECUTION_ACCEPTANCE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_RUNTIME_ADOPTION_BOUNDARY_PROBE_EXECUTION_ACCEPTANCE_FAILED"

    readout = {
        "schema_version": "c8_runtime_adoption_bounded_probe_execution_acceptance_readout_v0",
        "title": "C8 runtime-adoption bounded probe execution acceptance after reentry",
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "bounded_probe_execution_authorized": True,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_execution_count": 1,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": acceptance_packet["recommended_review_unit"],
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_runtime_adoption_bounded_probe_execution_acceptance_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
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
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_execution_count": 1,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "requires_review": True,
        "recommended_review_unit": acceptance_packet["recommended_review_unit"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_runtime_adoption_bounded_probe_execution_acceptance_receipt_v0",
        "receipt_type": "TYPED_C8_RUNTIME_ADOPTION_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_execution_acceptance_summary": {
            "runtime_adoption_bounded_probe_execution_acceptance_complete": gate == "PASS",
            "human_decision": HUMAN_DECISION,
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
            "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
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
            "execution_acceptance_decision": rel(EXECUTION_ACCEPTANCE_DECISION),
            "execution_acceptance_packet": rel(EXECUTION_ACCEPTANCE_PACKET),
            "execution_authority": rel(EXECUTION_AUTHORITY),
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

    receipt["receipt_id"] = "c8_runtime_adoption_bounded_probe_execution_acceptance_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_adoption_bounded_probe_execution_acceptance_receipt_id={receipt['receipt_id']}")
    print(f"runtime_adoption_bounded_probe_execution_acceptance_receipt_path={rel(receipt_path)}")
    print(f"runtime_adoption_bounded_probe_execution_acceptance_packet_path={rel(EXECUTION_ACCEPTANCE_PACKET)}")
    print(f"runtime_adoption_bounded_probe_execution_acceptance_decision_path={rel(EXECUTION_ACCEPTANCE_DECISION)}")
    print(f"runtime_adoption_bounded_probe_execution_authority_path={rel(EXECUTION_AUTHORITY)}")
    print(f"runtime_adoption_bounded_probe_execution_acceptance_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"selected_surface_id={SELECTED_SURFACE_ID}")
    print(f"selected_surface_kind={SELECTED_SURFACE_KIND}")
    print(f"probe_id={PROBE_ID}")
    print(f"probe_kind={PROBE_KIND}")
    print("bounded_probe_execution_authorized=true")
    print(f"authorized_future_unit={AUTHORIZED_FUTURE_UNIT}")
    print("authorized_future_unit_count=1")
    print("authorized_future_probe_execution_count=1")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={acceptance_packet['recommended_review_unit']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
