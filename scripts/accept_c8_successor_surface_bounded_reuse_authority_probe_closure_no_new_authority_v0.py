#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_NO_NEW_AUTHORITY_V0"
TARGET_UNIT_ID = "research.c8.successor_surface.bounded_reuse_authority_probe.closure_acceptance.v0"
MILESTONE = "C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_ACCEPTED"
OUTCOME = "C8_SUCCESSOR_SURFACE_CLOSED_NO_NEW_AUTHORITY"
STOP_CODE = "STOP_C8_SUCCESSOR_SURFACE_CLOSED_NO_NEW_AUTHORITY_READY_FOR_REVIEW"

HUMAN_DECISION = "ACCEPT_CLOSURE_NO_NEW_AUTHORITY"

PROBE_ID = "c8_successor_surface_reuse_authority_boundary_probe_v0"
PROBE_KIND = "REUSE_AUTHORITY_BOUNDARY_PROBE"
SELECTED_SURFACE_ID = "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0"
SELECTED_SURFACE_KIND = "REUSE_AUTHORITY_BOUNDARY_SURFACE"
SELECTED_SURFACE_LABEL = "C8_POST_CLOSURE_LOCAL_LOOP_REUSE_PRESSURE_SURFACE"

OUT_DIR = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_acceptance_v0"
RECEIPT_DIR = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_acceptance_v0_receipts"

CLOSURE_RECEIPT = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_v0_receipts/c8_successor_reuse_authority_probe_closure_receipt_c7e8a286.json"
CLOSURE_PACKET = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_v0/c8_successor_surface_bounded_reuse_authority_probe_closure_packet_v0.json"
CLOSURE_DECISION_OPTIONS = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_v0/c8_successor_surface_bounded_reuse_authority_probe_closure_decision_options_v0.json"
CLOSURE_AUDIT = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_v0/c8_successor_surface_bounded_reuse_authority_probe_closure_audit_v0.json"
CLOSURE_REPORT = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_v0/c8_successor_surface_bounded_reuse_authority_probe_closure_report.json"

ACCEPTANCE_DECISION = OUT_DIR / "c8_successor_surface_reuse_authority_probe_closure_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = OUT_DIR / "c8_successor_surface_reuse_authority_probe_closure_acceptance_packet_v0.json"
FINAL_CLOSURE = OUT_DIR / "c8_successor_surface_reuse_authority_probe_final_closure_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_successor_surface_reuse_authority_probe_closure_acceptance_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_successor_surface_reuse_authority_probe_closure_acceptance_readout_v0.json"
REPORT = OUT_DIR / "c8_successor_surface_reuse_authority_probe_closure_acceptance_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "additional_probe_authorized_count",
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
    "next_surface_selected_count",
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
        "closure_decision_options": CLOSURE_DECISION_OPTIONS,
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
    decision_options = read_json(CLOSURE_DECISION_OPTIONS)
    closure_audit = read_json(CLOSURE_AUDIT)
    closure_report = read_json(CLOSURE_REPORT)
    summary = closure_receipt.get("machine_readable_closure_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_PACKET_PASS",
        "outcome_class": "C8_SUCCESSOR_SURFACE_REUSE_AUTHORITY_PROBE_CLOSURE_READY_FOR_HUMAN_DECISION",
        "receipt_id": "c8_successor_reuse_authority_probe_closure_receipt_c7e8a286",
    }

    for key, want in expected_receipt.items():
        chk(failures, f"closure_receipt_{key}", closure_receipt.get(key), want)

    expected_summary = {
        "closure_packet_created": True,
        "closure_class": "BOUNDED_PROBE_RESULT_REVIEWED_REUSE_BOUNDARY_HELD",
        "source_probe_receipt_id": "c8_successor_reuse_authority_probe_receipt_803165de",
        "source_probe_evidence_id": "c8_successor_reuse_authority_probe_evidence_4f51ca49",
        "source_probe_result_id": "c8_successor_reuse_authority_probe_result_3260762c",
        "source_probe_boundary_audit_id": "c8_successor_reuse_authority_probe_boundary_72e5fd07",
        "source_acceptance_receipt_id": "c8_successor_probe_execution_acceptance_receipt_31139bd1",
        "source_authority_id": "c8_successor_probe_execution_authority_52f56baf",
        "source_prep_packet_id": "c8_successor_probe_prep_packet_74a6c209",
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_execution_count": 1,
        "allowed_probe_execution_count": 1,
        "probe_output_class": "REUSE_BOUNDARY_HELD_NO_NEW_AUTHORITY_NEEDED",
        "reuse_boundary_held": True,
        "new_authority_needed_now": False,
        "evidence_items_count": 7,
        "failed_evidence_count": 0,
        "recommended_human_decision": HUMAN_DECISION,
        "human_decision_required": True,
        "closure_accepted_now": False,
        "additional_probe_authorized_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
    }

    for key, want in expected_summary.items():
        chk(failures, f"closure_summary_{key}", summary.get(key), want)

    possible = summary.get("possible_human_decisions", [])
    if HUMAN_DECISION not in possible:
        failures.append(f"human_decision_not_available:{HUMAN_DECISION}")

    chk(failures, "closure_packet_id", closure_packet.get("closure_packet_id"), "c8_successor_reuse_authority_probe_closure_packet_bfa70151")
    chk(failures, "decision_options_id", decision_options.get("closure_decision_options_id"), "c8_successor_reuse_authority_probe_closure_options_d6633e1d")
    chk(failures, "closure_audit_id", closure_audit.get("closure_audit_id"), "c8_successor_reuse_authority_probe_closure_audit_ed03e30a")

    decision_boundary = decision_options.get("decision_boundary", {})
    expected_decision_boundary = {
        "accept_closure_authorizes_new_probe": False,
        "accept_closure_authorizes_build": False,
        "accept_closure_authorizes_rerun": False,
        "accept_closure_authorizes_reusable_schema": False,
        "accept_closure_may_return_to_surface_selection": True,
    }
    for key, want in expected_decision_boundary.items():
        chk(failures, f"decision_boundary_{key}", decision_boundary.get(key), want)

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
        "schema_version": "c8_successor_surface_reuse_authority_probe_closure_acceptance_decision_v0",
        "closure_acceptance_decision_id": None,
        "human_decision": HUMAN_DECISION,
        "source_closure_receipt_id": closure_receipt.get("receipt_id"),
        "source_closure_packet_id": closure_packet.get("closure_packet_id"),
        "source_closure_decision_options_id": decision_options.get("closure_decision_options_id"),
        "source_closure_audit_id": closure_audit.get("closure_audit_id"),
        "source_probe_receipt_id": summary.get("source_probe_receipt_id"),
        "source_probe_result_id": summary.get("source_probe_result_id"),
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "closure_accepted": True,
        "current_successor_surface_closed": True,
        "closed_with_no_new_authority": True,
        "human_decision_consumed": True,
        "return_to_surface_selection_allowed_after_review": True,
        "next_surface_selected_now": False,
        "additional_probe_authorized_now": False,
        "instrument_build_authorized_now": False,
        "cell1_build_authorized_now": False,
        "verification_probe_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "missing_instrument_proposal_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
    }
    acceptance_decision["closure_acceptance_decision_id"] = "c8_successor_reuse_authority_probe_closure_acceptance_decision_" + sig8(acceptance_decision)
    write_json(ACCEPTANCE_DECISION, acceptance_decision)

    acceptance_packet = {
        "schema_version": "c8_successor_surface_reuse_authority_probe_closure_acceptance_packet_v0",
        "closure_acceptance_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "acceptance_status": "CLOSURE_ACCEPTED_NO_NEW_AUTHORITY",
        "human_decision": HUMAN_DECISION,
        "source_closure_receipt_id": closure_receipt.get("receipt_id"),
        "source_closure_packet_id": closure_packet.get("closure_packet_id"),
        "source_closure_decision_options_id": decision_options.get("closure_decision_options_id"),
        "source_closure_audit_id": closure_audit.get("closure_audit_id"),
        "source_probe_receipt_id": summary.get("source_probe_receipt_id"),
        "source_probe_evidence_id": summary.get("source_probe_evidence_id"),
        "source_probe_result_id": summary.get("source_probe_result_id"),
        "source_probe_boundary_audit_id": summary.get("source_probe_boundary_audit_id"),
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "closure_class": summary.get("closure_class"),
        "probe_output_class": summary.get("probe_output_class"),
        "reuse_boundary_held": summary.get("reuse_boundary_held"),
        "new_authority_needed_now": summary.get("new_authority_needed_now"),
        "closure_accepted": True,
        "current_successor_surface_closed": True,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed_after_review": True,
        "next_surface_selected_now": False,
        "additional_probe_authorized_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": "REVIEW_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_ACCEPTANCE_V0",
    }
    acceptance_packet["closure_acceptance_packet_id"] = "c8_successor_reuse_authority_probe_closure_acceptance_packet_" + sig8(acceptance_packet)
    write_json(ACCEPTANCE_PACKET, acceptance_packet)

    final_closure = {
        "schema_version": "c8_successor_surface_reuse_authority_probe_final_closure_v0",
        "final_closure_id": None,
        "created_at": now_iso(),
        "source_closure_acceptance_packet_id": acceptance_packet["closure_acceptance_packet_id"],
        "source_closure_acceptance_decision_id": acceptance_decision["closure_acceptance_decision_id"],
        "source_closure_receipt_id": closure_receipt.get("receipt_id"),
        "source_closure_packet_id": closure_packet.get("closure_packet_id"),
        "probe_id": PROBE_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "final_closure_status": "SUCCESSOR_SURFACE_CLOSED_NO_NEW_AUTHORITY",
        "reuse_boundary_held": True,
        "new_authority_needed_now": False,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed_after_review": True,
        "additional_probe_authorized": False,
        "instrument_build_authorized": False,
        "c8_rerun_authorized": False,
        "reusable_schema_authorized": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
    }
    final_closure["final_closure_id"] = "c8_successor_reuse_authority_probe_final_closure_" + sig8(final_closure)
    write_json(FINAL_CLOSURE, final_closure)

    acceptance_gates = {
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_0_CLOSURE_RECEIPT_VERIFIED": closure_receipt.get("gate") == "PASS",
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_1_HUMAN_DECISION_AVAILABLE": HUMAN_DECISION in possible,
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_2_RECOMMENDED_DECISION_MATCHES": summary.get("recommended_human_decision") == HUMAN_DECISION,
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_3_REUSE_BOUNDARY_HELD": summary.get("reuse_boundary_held") is True,
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_4_NO_NEW_AUTHORITY_NEEDED": summary.get("new_authority_needed_now") is False,
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_5_CLOSURE_ACCEPTED_NOW": acceptance_packet["closure_accepted"] is True,
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_6_SURFACE_CLOSED_NO_NEW_AUTHORITY": final_closure["closed_with_no_new_authority"] is True,
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_7_NO_ADDITIONAL_PROBE": forbidden_counters["additional_probe_authorized_count"] == 0 and acceptance_packet["additional_probe_authorized_now"] is False,
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_8_NO_BUILD_RERUN_OR_SCHEMA": forbidden_counters["instrument_build_count"] == 0 and forbidden_counters["c8_rerun_count"] == 0 and forbidden_counters["reusable_schema_authorized_count"] == 0,
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_9_NO_GLOBAL_OR_FRONTIER_CLAIM": forbidden_counters["global_solution_claim_count"] == 0 and forbidden_counters["frontier_solved_claim_count"] == 0,
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_10_NO_NEXT_SURFACE_SELECTED_NOW": forbidden_counters["next_surface_selected_count"] == 0 and acceptance_packet["next_surface_selected_now"] is False,
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_11_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_12_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "C8_REUSE_AUTHORITY_CLOSURE_ACCEPTANCE_13_RESULT_REQUIRES_REVIEW": acceptance_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_ACCEPTANCE_PASS" if gate == "PASS" else "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_ACCEPTANCE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_SUCCESSOR_SURFACE_CLOSURE_ACCEPTANCE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_SUCCESSOR_SURFACE_CLOSURE_ACCEPTANCE_FAILED"

    boundary_audit = {
        "schema_version": "c8_successor_surface_reuse_authority_probe_closure_acceptance_boundary_audit_v0",
        "boundary_audit_id": None,
        "gate": gate,
        "source_closure_acceptance_packet_id": acceptance_packet["closure_acceptance_packet_id"],
        "source_closure_acceptance_decision_id": acceptance_decision["closure_acceptance_decision_id"],
        "final_closure_id": final_closure["final_closure_id"],
        "human_decision": HUMAN_DECISION,
        "closure_accepted": True,
        "current_successor_surface_closed": True,
        "closed_with_no_new_authority": True,
        "closure_boundary": {
            "may_mark_current_successor_surface_closed": True,
            "may_return_to_surface_selection_after_review": True,
            "may_select_next_surface_now": False,
            "may_execute_additional_probe_now": False,
            "may_build_instrument_now": False,
            "may_build_cell1_now": False,
            "may_run_verification_probe_now": False,
            "may_rerun_c8_now": False,
            "may_create_missing_instrument_proposal_now": False,
            "may_authorize_reusable_schema_now": False,
            "may_claim_global_solution": False,
            "may_claim_frontier_solved": False,
        },
        "acceptance_gate_results": acceptance_gates,
        "forbidden_counters": forbidden_counters,
        "failures": failures,
        "warnings": warnings,
    }
    boundary_audit["boundary_audit_id"] = "c8_successor_reuse_authority_probe_closure_acceptance_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    readout = {
        "schema_version": "c8_successor_surface_reuse_authority_probe_closure_acceptance_readout_v0",
        "title": "C8 successor surface reuse-authority probe closure acceptance readout",
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "closure_acceptance_packet_id": acceptance_packet["closure_acceptance_packet_id"],
        "closure_acceptance_decision_id": acceptance_decision["closure_acceptance_decision_id"],
        "final_closure_id": final_closure["final_closure_id"],
        "source_closure_receipt_id": closure_receipt.get("receipt_id"),
        "probe_id": PROBE_ID,
        "reuse_boundary_held": summary.get("reuse_boundary_held"),
        "new_authority_needed_now": summary.get("new_authority_needed_now"),
        "closure_accepted": True,
        "current_successor_surface_closed": True,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed_after_review": True,
        "additional_probe_authorized_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized_now": False,
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_successor_surface_reuse_authority_probe_closure_acceptance_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "closure_acceptance_packet_ref": rel(ACCEPTANCE_PACKET),
        "closure_acceptance_decision_ref": rel(ACCEPTANCE_DECISION),
        "final_closure_ref": rel(FINAL_CLOSURE),
        "boundary_audit_ref": rel(BOUNDARY_AUDIT),
        "source_closure_receipt_id": closure_receipt.get("receipt_id"),
        "source_closure_packet_id": closure_packet.get("closure_packet_id"),
        "source_closure_decision_options_id": decision_options.get("closure_decision_options_id"),
        "source_closure_audit_id": closure_audit.get("closure_audit_id"),
        "source_probe_receipt_id": summary.get("source_probe_receipt_id"),
        "source_probe_result_id": summary.get("source_probe_result_id"),
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "human_decision": HUMAN_DECISION,
        "closure_accepted": True,
        "current_successor_surface_closed": True,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed_after_review": True,
        "next_surface_selected_now": False,
        "additional_probe_authorized_now": False,
        "new_build_count": 0,
        "new_rerun_count": 0,
        "reusable_schema_authorized": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_successor_surface_reuse_authority_probe_closure_acceptance_receipt_v0",
        "receipt_type": "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_ACCEPTANCE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_refs": {
            "closure_receipt_ref": rel(CLOSURE_RECEIPT),
            "closure_packet_ref": rel(CLOSURE_PACKET),
            "closure_decision_options_ref": rel(CLOSURE_DECISION_OPTIONS),
            "closure_audit_ref": rel(CLOSURE_AUDIT),
            "closure_report_ref": rel(CLOSURE_REPORT),
        },
        "machine_readable_acceptance_summary": {
            "closure_acceptance_complete": gate == "PASS",
            "human_decision": HUMAN_DECISION,
            "source_closure_receipt_id": closure_receipt.get("receipt_id"),
            "source_closure_packet_id": closure_packet.get("closure_packet_id"),
            "source_closure_decision_options_id": decision_options.get("closure_decision_options_id"),
            "source_closure_audit_id": closure_audit.get("closure_audit_id"),
            "source_probe_receipt_id": summary.get("source_probe_receipt_id"),
            "source_probe_result_id": summary.get("source_probe_result_id"),
            "source_probe_evidence_id": summary.get("source_probe_evidence_id"),
            "source_probe_boundary_audit_id": summary.get("source_probe_boundary_audit_id"),
            "source_acceptance_receipt_id": summary.get("source_acceptance_receipt_id"),
            "source_authority_id": summary.get("source_authority_id"),
            "source_prep_packet_id": summary.get("source_prep_packet_id"),
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "closure_class": summary.get("closure_class"),
            "probe_output_class": summary.get("probe_output_class"),
            "reuse_boundary_held": summary.get("reuse_boundary_held"),
            "new_authority_needed_now": summary.get("new_authority_needed_now"),
            "closure_accepted": True,
            "current_successor_surface_closed": True,
            "closed_with_no_new_authority": True,
            "return_to_surface_selection_allowed_after_review": True,
            "next_surface_selected_now": False,
            "additional_probe_authorized_now": False,
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
            "recommended_review_unit": "REVIEW_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_ACCEPTANCE_V0",
            "next_command_goal": None,
        },
        "acceptance_gate_results": acceptance_gates,
        "forbidden_counters": forbidden_counters,
        "source_artifact_immutability": {
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
        },
        "output_artifacts": {
            "closure_acceptance_decision": rel(ACCEPTANCE_DECISION),
            "closure_acceptance_packet": rel(ACCEPTANCE_PACKET),
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

    receipt["receipt_id"] = "c8_successor_reuse_authority_probe_closure_acceptance_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"closure_acceptance_receipt_id={receipt['receipt_id']}")
    print(f"closure_acceptance_receipt_path={rel(receipt_path)}")
    print(f"closure_acceptance_packet_path={rel(ACCEPTANCE_PACKET)}")
    print(f"closure_acceptance_decision_path={rel(ACCEPTANCE_DECISION)}")
    print(f"final_closure_path={rel(FINAL_CLOSURE)}")
    print(f"boundary_audit_path={rel(BOUNDARY_AUDIT)}")
    print(f"human_decision={HUMAN_DECISION}")
    print(f"source_closure_receipt_id={closure_receipt.get('receipt_id')}")
    print(f"source_closure_packet_id={closure_packet.get('closure_packet_id')}")
    print(f"source_probe_receipt_id={summary.get('source_probe_receipt_id')}")
    print(f"source_probe_result_id={summary.get('source_probe_result_id')}")
    print(f"probe_id={PROBE_ID}")
    print(f"probe_kind={PROBE_KIND}")
    print("closure_accepted=true")
    print("current_successor_surface_closed=true")
    print("closed_with_no_new_authority=true")
    print("return_to_surface_selection_allowed_after_review=true")
    print("next_surface_selected_now=false")
    print("additional_probe_authorized_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print("global_solution_claim=false")
    print("frontier_solved_claim=false")
    print(f"closure_acceptance_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
