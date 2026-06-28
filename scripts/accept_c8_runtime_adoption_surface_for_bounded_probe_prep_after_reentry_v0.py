#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_RUNTIME_ADOPTION_SUCCESSOR_SURFACE_FOR_BOUNDED_PROBE_PREP_AFTER_REENTRY_V0"
TARGET_UNIT_ID = "research.c8.runtime_adoption_successor_surface.accept_for_bounded_probe_prep.after_reentry.v0"
MILESTONE = "C8_RUNTIME_ADOPTION_SUCCESSOR_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_PREP_AFTER_REENTRY"
OUTCOME = "C8_RUNTIME_ADOPTION_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_PREP_ONLY"
STOP_CODE = "STOP_C8_RUNTIME_ADOPTION_SURFACE_PROBE_PREP_ACCEPTANCE_READY_FOR_REVIEW"

HUMAN_DECISION = "ACCEPT_SURFACE_FOR_BOUNDED_PROBE_PREP"
AUTHORIZED_FUTURE_UNIT = "CREATE_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_AFTER_REENTRY_V0"

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

OUT_DIR = ROOT / "data/c8_runtime_adoption_surface_probe_prep_acceptance_after_reentry_v0"
RECEIPT_DIR = ROOT / "data/c8_runtime_adoption_surface_probe_prep_acceptance_after_reentry_v0_receipts"

SELECTION_RECEIPT = ROOT / "data/c8_successor_surface_selection_after_reentry_v0_receipts/c8_successor_surface_selection_receipt_7da4fd41.json"
SELECTION_PACKET = ROOT / "data/c8_successor_surface_selection_after_reentry_v0/c8_successor_surface_selection_packet_v0.json"
SELECTION_DECISION = ROOT / "data/c8_successor_surface_selection_after_reentry_v0/c8_successor_surface_selection_decision_v0.json"
SELECTION_BOUNDARY = ROOT / "data/c8_successor_surface_selection_after_reentry_v0/c8_successor_surface_selection_boundary_audit_v0.json"
SELECTION_REPORT = ROOT / "data/c8_successor_surface_selection_after_reentry_v0/c8_successor_surface_selection_report.json"

ACCEPTANCE_DECISION = OUT_DIR / "c8_runtime_adoption_surface_probe_prep_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = OUT_DIR / "c8_runtime_adoption_surface_probe_prep_acceptance_packet_v0.json"
AUTHORITY_PACKET = OUT_DIR / "c8_runtime_adoption_surface_probe_prep_authority_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_runtime_adoption_surface_probe_prep_acceptance_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_runtime_adoption_surface_probe_prep_acceptance_readout_v0.json"
REPORT = OUT_DIR / "c8_runtime_adoption_surface_probe_prep_acceptance_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "probe_prep_packet_created_count",
    "probe_authorized_count",
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
        "selection_receipt": SELECTION_RECEIPT,
        "selection_packet": SELECTION_PACKET,
        "selection_decision": SELECTION_DECISION,
        "selection_boundary": SELECTION_BOUNDARY,
        "selection_report": SELECTION_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    selection_receipt = read_json(SELECTION_RECEIPT)
    selection_packet = read_json(SELECTION_PACKET)
    selection_decision = read_json(SELECTION_DECISION)
    selection_boundary = read_json(SELECTION_BOUNDARY)
    selection_report = read_json(SELECTION_REPORT)
    selection_summary = selection_receipt.get("machine_readable_selection_summary", {})

    expected_question = SELECTED_SURFACE_QUESTION

    expected_selection_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_SUCCESSOR_SURFACE_SELECTION_AFTER_REENTRY_PASS",
        "outcome_class": "C8_SUCCESSOR_SURFACE_SELECTION_REVIEWABLE_NOT_ACCEPTED",
        "receipt_id": SOURCE_SELECTION_RECEIPT_ID,
    }

    for key, want in expected_selection_receipt.items():
        chk(failures, f"selection_receipt_{key}", selection_receipt.get(key), want)

    expected_selection_summary = {
        "surface_selection_after_reentry_complete": True,
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "previous_surface_closed": True,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_question": expected_question,
        "selected_surface_status": "REVIEWABLE_NOT_ACCEPTED",
        "selected_surface_active": False,
        "selected_surface_accepted_now": False,
        "probe_prep_authorized_now": False,
        "probe_authorized_now": False,
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
        "recommended_review_unit": "REVIEW_C8_SUCCESSOR_SURFACE_SELECTION_AFTER_REENTRY_V0",
        "next_command_goal": None,
    }

    for key, want in expected_selection_summary.items():
        chk(failures, f"selection_summary_{key}", selection_summary.get(key), want)

    chk(failures, "selection_decision_id", selection_decision.get("surface_selection_decision_id"), SOURCE_SELECTION_DECISION_ID)
    chk(failures, "selection_packet_id", selection_packet.get("surface_selection_packet_id"), SOURCE_SELECTION_PACKET_ID)
    chk(failures, "selection_boundary_id", selection_boundary.get("surface_selection_boundary_audit_id"), SOURCE_SELECTION_BOUNDARY_ID)

    decision_options = selection_packet.get("recommended_next_decision_options", [])
    if HUMAN_DECISION not in decision_options:
        failures.append(f"human_decision_not_available:{HUMAN_DECISION}")

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
        "schema_version": "c8_runtime_adoption_surface_probe_prep_acceptance_decision_v0",
        "runtime_adoption_probe_prep_acceptance_decision_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "human_decision": HUMAN_DECISION,
        "human_decision_consumed": True,
        "source_surface_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_surface_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
        "source_surface_selection_decision_id": SOURCE_SELECTION_DECISION_ID,
        "source_surface_selection_boundary_audit_id": SOURCE_SELECTION_BOUNDARY_ID,
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_question": SELECTED_SURFACE_QUESTION,
        "selected_surface_accepted_for_bounded_probe_prep": True,
        "bounded_probe_prep_authorized": True,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_prep_packet_creation_count": 1,
        "probe_prep_packet_created_now": False,
        "probe_authorized_now": False,
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
    acceptance_decision["runtime_adoption_probe_prep_acceptance_decision_id"] = "c8_runtime_adoption_probe_prep_acceptance_decision_" + sig8(acceptance_decision)
    write_json(ACCEPTANCE_DECISION, acceptance_decision)

    authority_packet = {
        "schema_version": "c8_runtime_adoption_surface_probe_prep_authority_v0",
        "runtime_adoption_probe_prep_authority_id": None,
        "created_at": now_iso(),
        "authority_status": "AUTHORIZED_FOR_ONE_BOUNDED_PROBE_PREP_PACKET_CREATION_ONLY",
        "source_acceptance_decision_id": acceptance_decision["runtime_adoption_probe_prep_acceptance_decision_id"],
        "source_surface_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authorized_scope": {
            "create_bounded_probe_prep_packet": True,
            "surface_id": SELECTED_SURFACE_ID,
            "surface_kind": SELECTED_SURFACE_KIND,
            "surface_label": SELECTED_SURFACE_LABEL,
        },
        "not_authorized": {
            "execute_probe": True,
            "authorize_probe_execution": True,
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
    authority_packet["runtime_adoption_probe_prep_authority_id"] = "c8_runtime_adoption_probe_prep_authority_" + sig8(authority_packet)
    write_json(AUTHORITY_PACKET, authority_packet)

    acceptance_packet = {
        "schema_version": "c8_runtime_adoption_surface_probe_prep_acceptance_packet_v0",
        "runtime_adoption_probe_prep_acceptance_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "acceptance_status": "RUNTIME_ADOPTION_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_PREP_ONLY",
        "human_decision": HUMAN_DECISION,
        "source_surface_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_surface_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
        "source_surface_selection_decision_id": SOURCE_SELECTION_DECISION_ID,
        "source_surface_selection_boundary_audit_id": SOURCE_SELECTION_BOUNDARY_ID,
        "source_acceptance_decision_id": acceptance_decision["runtime_adoption_probe_prep_acceptance_decision_id"],
        "source_probe_prep_authority_id": authority_packet["runtime_adoption_probe_prep_authority_id"],
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_question": SELECTED_SURFACE_QUESTION,
        "selected_surface_accepted_for_bounded_probe_prep": True,
        "bounded_probe_prep_authorized": True,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_prep_packet_creation_count": 1,
        "probe_prep_packet_created_now": False,
        "probe_authorized_now": False,
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
        "recommended_review_unit": "REVIEW_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_ACCEPTANCE_AFTER_REENTRY_V0",
    }
    acceptance_packet["runtime_adoption_probe_prep_acceptance_packet_id"] = "c8_runtime_adoption_probe_prep_acceptance_packet_" + sig8(acceptance_packet)
    write_json(ACCEPTANCE_PACKET, acceptance_packet)

    boundary_audit = {
        "schema_version": "c8_runtime_adoption_surface_probe_prep_acceptance_boundary_audit_v0",
        "runtime_adoption_probe_prep_acceptance_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_acceptance_packet_id": acceptance_packet["runtime_adoption_probe_prep_acceptance_packet_id"],
        "source_acceptance_decision_id": acceptance_decision["runtime_adoption_probe_prep_acceptance_decision_id"],
        "source_authority_id": authority_packet["runtime_adoption_probe_prep_authority_id"],
        "allowed_now": {
            "record_surface_acceptance_for_bounded_probe_prep": True,
            "authorize_one_future_bounded_probe_prep_packet_creation": True,
        },
        "not_allowed_now": {
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
    boundary_audit["runtime_adoption_probe_prep_acceptance_boundary_audit_id"] = "c8_runtime_adoption_probe_prep_acceptance_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    gate_results = {
        "PROBE_PREP_ACCEPTANCE_0_SOURCE_SELECTION_RECEIPT_PASS": selection_receipt.get("gate") == "PASS",
        "PROBE_PREP_ACCEPTANCE_1_SELECTED_SURFACE_MATCHES_RUNTIME_ADOPTION": selection_summary.get("selected_surface_id") == SELECTED_SURFACE_ID and selection_summary.get("selected_surface_kind") == SELECTED_SURFACE_KIND,
        "PROBE_PREP_ACCEPTANCE_2_SELECTED_SURFACE_REVIEWABLE_NOT_ACCEPTED": selection_summary.get("selected_surface_status") == "REVIEWABLE_NOT_ACCEPTED" and selection_summary.get("selected_surface_accepted_now") is False,
        "PROBE_PREP_ACCEPTANCE_3_HUMAN_DECISION_AVAILABLE": HUMAN_DECISION in decision_options,
        "PROBE_PREP_ACCEPTANCE_4_ACCEPTANCE_RECORDED": acceptance_packet["selected_surface_accepted_for_bounded_probe_prep"] is True,
        "PROBE_PREP_ACCEPTANCE_5_EXACTLY_ONE_FUTURE_PREP_UNIT_AUTHORIZED": acceptance_packet["authorized_future_unit_count"] == 1 and acceptance_packet["authorized_future_unit"] == AUTHORIZED_FUTURE_UNIT,
        "PROBE_PREP_ACCEPTANCE_6_PREP_PACKET_NOT_CREATED_NOW": acceptance_packet["probe_prep_packet_created_now"] is False,
        "PROBE_PREP_ACCEPTANCE_7_NO_PROBE_BUILD_RERUN_SCHEMA": acceptance_packet["probe_authorized_now"] is False and acceptance_packet["probe_executed_now"] is False and acceptance_packet["instrument_build_authorized_now"] is False and acceptance_packet["c8_rerun_authorized_now"] is False and acceptance_packet["reusable_schema_authorized_now"] is False,
        "PROBE_PREP_ACCEPTANCE_8_NO_GLOBAL_OR_FRONTIER_CLAIM": acceptance_packet["global_solution_claim"] is False and acceptance_packet["frontier_solved_claim"] is False,
        "PROBE_PREP_ACCEPTANCE_9_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "PROBE_PREP_ACCEPTANCE_10_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "PROBE_PREP_ACCEPTANCE_11_RESULT_REQUIRES_REVIEW": acceptance_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"probe_prep_acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_RUNTIME_ADOPTION_SURFACE_PROBE_PREP_ACCEPTANCE_PASS" if gate == "PASS" else "TYPED_C8_RUNTIME_ADOPTION_SURFACE_PROBE_PREP_ACCEPTANCE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_RUNTIME_ADOPTION_SURFACE_PROBE_PREP_ACCEPTANCE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_RUNTIME_ADOPTION_SURFACE_PROBE_PREP_ACCEPTANCE_FAILED"

    readout = {
        "schema_version": "c8_runtime_adoption_surface_probe_prep_acceptance_readout_v0",
        "title": "C8 runtime-adoption surface bounded probe-prep acceptance after reentry",
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_accepted_for_bounded_probe_prep": True,
        "bounded_probe_prep_authorized": True,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "probe_prep_packet_created_now": False,
        "probe_authorized_now": False,
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
        "schema_version": "c8_runtime_adoption_surface_probe_prep_acceptance_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "source_surface_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_surface_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
        "source_surface_selection_decision_id": SOURCE_SELECTION_DECISION_ID,
        "source_surface_selection_boundary_audit_id": SOURCE_SELECTION_BOUNDARY_ID,
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_question": SELECTED_SURFACE_QUESTION,
        "selected_surface_accepted_for_bounded_probe_prep": True,
        "bounded_probe_prep_authorized": True,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_prep_packet_creation_count": 1,
        "probe_prep_packet_created_now": False,
        "probe_authorized_now": False,
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
        "schema_version": "c8_runtime_adoption_surface_probe_prep_acceptance_receipt_v0",
        "receipt_type": "TYPED_C8_RUNTIME_ADOPTION_SURFACE_PROBE_PREP_ACCEPTANCE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_acceptance_summary": {
            "runtime_adoption_surface_probe_prep_acceptance_complete": gate == "PASS",
            "human_decision": HUMAN_DECISION,
            "source_surface_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
            "source_surface_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
            "source_surface_selection_decision_id": SOURCE_SELECTION_DECISION_ID,
            "source_surface_selection_boundary_audit_id": SOURCE_SELECTION_BOUNDARY_ID,
            "previous_surface_id": PREVIOUS_SURFACE_ID,
            "previous_surface_kind": PREVIOUS_SURFACE_KIND,
            "previous_surface_label": PREVIOUS_SURFACE_LABEL,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "selected_surface_question": SELECTED_SURFACE_QUESTION,
            "selected_surface_accepted_for_bounded_probe_prep": True,
            "bounded_probe_prep_authorized": True,
            "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
            "authorized_future_unit_count": 1,
            "authorized_future_probe_prep_packet_creation_count": 1,
            "probe_prep_packet_created_now": False,
            "probe_authorized_now": False,
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
            "authority_packet": rel(AUTHORITY_PACKET),
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

    receipt["receipt_id"] = "c8_runtime_adoption_probe_prep_acceptance_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_adoption_probe_prep_acceptance_receipt_id={receipt['receipt_id']}")
    print(f"runtime_adoption_probe_prep_acceptance_receipt_path={rel(receipt_path)}")
    print(f"runtime_adoption_probe_prep_acceptance_packet_path={rel(ACCEPTANCE_PACKET)}")
    print(f"runtime_adoption_probe_prep_acceptance_decision_path={rel(ACCEPTANCE_DECISION)}")
    print(f"runtime_adoption_probe_prep_authority_path={rel(AUTHORITY_PACKET)}")
    print(f"runtime_adoption_probe_prep_acceptance_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"selected_surface_id={SELECTED_SURFACE_ID}")
    print(f"selected_surface_kind={SELECTED_SURFACE_KIND}")
    print("selected_surface_accepted_for_bounded_probe_prep=true")
    print("bounded_probe_prep_authorized=true")
    print(f"authorized_future_unit={AUTHORIZED_FUTURE_UNIT}")
    print("authorized_future_unit_count=1")
    print("probe_prep_packet_created_now=false")
    print("probe_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={acceptance_packet['recommended_review_unit']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
