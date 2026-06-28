#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_RETURN_TO_SURFACE_SELECTION_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.return_to_surface_selection_packet.acceptance.after_runtime_adoption_closure.v0"
MILESTONE = "C8_RETURN_TO_SURFACE_SELECTION_PACKET_ACCEPTED_AFTER_RUNTIME_ADOPTION_CLOSURE"
OUTCOME = "C8_RETURN_TO_SURFACE_SELECTION_ACCEPTED_SUCCESSOR_SURFACE_SELECTION_AUTHORIZED_FOR_REVIEW"
STOP_CODE = "STOP_C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_READY_FOR_REVIEW"

HUMAN_DECISION = "ACCEPT_RETURN_TO_SURFACE_SELECTION_PACKET"
AUTHORIZED_FUTURE_UNIT = "SELECT_C8_SUCCESSOR_SURFACE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

SOURCE_RETURN_RECEIPT_ID = "c8_return_to_surface_selection_receipt_b697ee8c"
SOURCE_RETURN_PACKET_ID = "c8_return_to_surface_selection_packet_251c29e8"
SOURCE_RETURN_OPTIONS_ID = "c8_return_to_surface_selection_options_bdbb1aad"
SOURCE_RETURN_BOUNDARY_ID = "c8_return_to_surface_selection_boundary_d4a6f794"

SOURCE_CLOSURE_ACCEPTANCE_RECEIPT_ID = "c8_runtime_adoption_bounded_probe_closure_acceptance_receipt_69984edf"
SOURCE_CLOSURE_ACCEPTANCE_DECISION_ID = "c8_runtime_adoption_bounded_probe_closure_acceptance_decision_a4989fd2"
SOURCE_CLOSURE_ACCEPTANCE_PACKET_ID = "c8_runtime_adoption_bounded_probe_closure_acceptance_packet_31cc313b"
SOURCE_FINAL_CLOSURE_ID = "c8_runtime_adoption_bounded_probe_final_closure_a7db49a5"
SOURCE_CLOSURE_ACCEPTANCE_BOUNDARY_ID = "c8_runtime_adoption_bounded_probe_closure_acceptance_boundary_667c0c3f"

CLOSED_SURFACE_ID = "c8_successor_surface_runtime_adoption_after_reentry_v0"
CLOSED_SURFACE_KIND = "RUNTIME_ADOPTION_SURFACE"
CLOSED_SURFACE_LABEL = "C8_RUNTIME_ADOPTION_AFTER_REUSE_AUTHORITY_CLOSURE_SURFACE"
CLOSED_PROBE_ID = "c8_runtime_adoption_surface_bounded_probe_after_reentry_v0"
CLOSED_PROBE_KIND = "RUNTIME_ADOPTION_BOUNDARY_PROBE"
CLOSED_PROBE_OUTPUT_CLASS = "RUNTIME_ADOPTION_BOUNDARY_PROBE_OBSERVED_NO_DEFECTS"

OUT_DIR = ROOT / "data/c8_return_to_surface_selection_acceptance_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_return_to_surface_selection_acceptance_after_runtime_adoption_closure_v0_receipts"

RETURN_RECEIPT = ROOT / "data/c8_return_to_surface_selection_after_runtime_adoption_closure_v0_receipts/c8_return_to_surface_selection_receipt_b697ee8c.json"
RETURN_PACKET = ROOT / "data/c8_return_to_surface_selection_after_runtime_adoption_closure_v0/c8_return_to_surface_selection_packet_v0.json"
RETURN_OPTIONS = ROOT / "data/c8_return_to_surface_selection_after_runtime_adoption_closure_v0/c8_return_to_surface_selection_options_v0.json"
RETURN_BOUNDARY = ROOT / "data/c8_return_to_surface_selection_after_runtime_adoption_closure_v0/c8_return_to_surface_selection_boundary_audit_v0.json"
RETURN_REPORT = ROOT / "data/c8_return_to_surface_selection_after_runtime_adoption_closure_v0/c8_return_to_surface_selection_report.json"

ACCEPTANCE_DECISION = OUT_DIR / "c8_return_to_surface_selection_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = OUT_DIR / "c8_return_to_surface_selection_acceptance_packet_v0.json"
AUTHORITY = OUT_DIR / "c8_successor_surface_selection_authority_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_return_to_surface_selection_acceptance_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_return_to_surface_selection_acceptance_readout_v0.json"
REPORT = OUT_DIR / "c8_return_to_surface_selection_acceptance_report.json"

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
        "return_receipt": RETURN_RECEIPT,
        "return_packet": RETURN_PACKET,
        "return_options": RETURN_OPTIONS,
        "return_boundary": RETURN_BOUNDARY,
        "return_report": RETURN_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    return_receipt = read_json(RETURN_RECEIPT)
    return_packet = read_json(RETURN_PACKET)
    return_options = read_json(RETURN_OPTIONS)
    return_boundary = read_json(RETURN_BOUNDARY)
    return_report = read_json(RETURN_REPORT)
    summary = return_receipt.get("machine_readable_return_to_surface_selection_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_RETURN_TO_SURFACE_SELECTION_PACKET_PASS",
        "outcome_class": "C8_RETURN_TO_SURFACE_SELECTION_PACKET_READY_FOR_REVIEW",
        "receipt_id": SOURCE_RETURN_RECEIPT_ID,
    }

    for key, want in expected_receipt.items():
        chk(failures, f"return_receipt_{key}", return_receipt.get(key), want)

    expected_summary = {
        "return_to_surface_selection_packet_created": True,
        "source_closure_acceptance_receipt_id": SOURCE_CLOSURE_ACCEPTANCE_RECEIPT_ID,
        "source_closure_acceptance_decision_id": SOURCE_CLOSURE_ACCEPTANCE_DECISION_ID,
        "source_closure_acceptance_packet_id": SOURCE_CLOSURE_ACCEPTANCE_PACKET_ID,
        "source_final_closure_id": SOURCE_FINAL_CLOSURE_ID,
        "source_closure_acceptance_boundary_id": SOURCE_CLOSURE_ACCEPTANCE_BOUNDARY_ID,
        "closed_surface_id": CLOSED_SURFACE_ID,
        "closed_surface_kind": CLOSED_SURFACE_KIND,
        "closed_surface_label": CLOSED_SURFACE_LABEL,
        "closed_probe_id": CLOSED_PROBE_ID,
        "closed_probe_kind": CLOSED_PROBE_KIND,
        "closed_probe_output_class": CLOSED_PROBE_OUTPUT_CLASS,
        "current_surface_closed": True,
        "closed_with_no_new_authority": True,
        "successor_surface_selection_ready_for_human_decision": True,
        "recommended_human_decision": HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": AUTHORIZED_FUTURE_UNIT,
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
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
        "recommended_review_unit": "REVIEW_C8_RETURN_TO_SURFACE_SELECTION_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "next_command_goal": None,
    }

    for key, want in expected_summary.items():
        chk(failures, f"return_summary_{key}", summary.get(key), want)

    chk(failures, "return_packet_id", return_packet.get("c8_return_to_surface_selection_packet_id"), SOURCE_RETURN_PACKET_ID)
    chk(failures, "return_options_id", return_options.get("c8_return_to_surface_selection_options_id"), SOURCE_RETURN_OPTIONS_ID)
    chk(failures, "return_boundary_id", return_boundary.get("c8_return_to_surface_selection_boundary_audit_id"), SOURCE_RETURN_BOUNDARY_ID)

    if HUMAN_DECISION not in return_options.get("human_decision_options", []):
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
        "schema_version": "c8_return_to_surface_selection_acceptance_decision_v0",
        "c8_return_to_surface_selection_acceptance_decision_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "human_decision": HUMAN_DECISION,
        "human_decision_consumed": True,
        "source_return_receipt_id": SOURCE_RETURN_RECEIPT_ID,
        "source_return_packet_id": SOURCE_RETURN_PACKET_ID,
        "source_return_options_id": SOURCE_RETURN_OPTIONS_ID,
        "source_return_boundary_id": SOURCE_RETURN_BOUNDARY_ID,
        "source_final_closure_id": SOURCE_FINAL_CLOSURE_ID,
        "closed_surface_id": CLOSED_SURFACE_ID,
        "closed_surface_kind": CLOSED_SURFACE_KIND,
        "closed_surface_label": CLOSED_SURFACE_LABEL,
        "closed_probe_id": CLOSED_PROBE_ID,
        "closed_probe_kind": CLOSED_PROBE_KIND,
        "closed_probe_output_class": CLOSED_PROBE_OUTPUT_CLASS,
        "successor_surface_selection_authorized_after_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
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
    }
    acceptance_decision["c8_return_to_surface_selection_acceptance_decision_id"] = "c8_return_to_surface_selection_acceptance_decision_" + sig8(acceptance_decision)
    write_json(ACCEPTANCE_DECISION, acceptance_decision)

    authority = {
        "schema_version": "c8_successor_surface_selection_authority_v0",
        "c8_successor_surface_selection_authority_id": None,
        "created_at": now_iso(),
        "source_acceptance_decision_id": acceptance_decision["c8_return_to_surface_selection_acceptance_decision_id"],
        "source_return_packet_id": SOURCE_RETURN_PACKET_ID,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authority_status": "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "authority_scope": {
            "may_create_successor_surface_selection_packet": True,
            "may_select_surface_inside_future_unit": True,
            "may_accept_successor_surface_now": False,
            "may_create_probe_prep_now": False,
            "may_authorize_probe_execution_now": False,
            "may_execute_probe_now": False,
            "may_build_now": False,
            "may_rerun_c8_now": False,
            "may_promote_schema_now": False,
        },
    }
    authority["c8_successor_surface_selection_authority_id"] = "c8_successor_surface_selection_authority_" + sig8(authority)
    write_json(AUTHORITY, authority)

    acceptance_packet = {
        "schema_version": "c8_return_to_surface_selection_acceptance_packet_v0",
        "c8_return_to_surface_selection_acceptance_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "acceptance_status": "RETURN_TO_SURFACE_SELECTION_PACKET_ACCEPTED",
        "human_decision": HUMAN_DECISION,
        "source_acceptance_decision_id": acceptance_decision["c8_return_to_surface_selection_acceptance_decision_id"],
        "source_successor_surface_selection_authority_id": authority["c8_successor_surface_selection_authority_id"],
        "source_return_receipt_id": SOURCE_RETURN_RECEIPT_ID,
        "source_return_packet_id": SOURCE_RETURN_PACKET_ID,
        "source_return_options_id": SOURCE_RETURN_OPTIONS_ID,
        "source_return_boundary_id": SOURCE_RETURN_BOUNDARY_ID,
        "closed_surface_id": CLOSED_SURFACE_ID,
        "closed_surface_kind": CLOSED_SURFACE_KIND,
        "closed_surface_label": CLOSED_SURFACE_LABEL,
        "closed_probe_id": CLOSED_PROBE_ID,
        "closed_probe_kind": CLOSED_PROBE_KIND,
        "closed_probe_output_class": CLOSED_PROBE_OUTPUT_CLASS,
        "successor_surface_selection_authorized_after_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "surface_selection_packet_created_now": False,
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
        "recommended_review_unit": "REVIEW_C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
    }
    acceptance_packet["c8_return_to_surface_selection_acceptance_packet_id"] = "c8_return_to_surface_selection_acceptance_packet_" + sig8(acceptance_packet)
    write_json(ACCEPTANCE_PACKET, acceptance_packet)

    boundary_audit = {
        "schema_version": "c8_return_to_surface_selection_acceptance_boundary_audit_v0",
        "c8_return_to_surface_selection_acceptance_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_acceptance_decision_id": acceptance_decision["c8_return_to_surface_selection_acceptance_decision_id"],
        "source_acceptance_packet_id": acceptance_packet["c8_return_to_surface_selection_acceptance_packet_id"],
        "source_successor_surface_selection_authority_id": authority["c8_successor_surface_selection_authority_id"],
        "source_return_packet_id": SOURCE_RETURN_PACKET_ID,
        "allowed_now": {
            "accept_return_to_surface_selection_packet": True,
            "authorize_successor_surface_selection_after_review": True,
        },
        "not_allowed_now": {
            "create_surface_selection_packet_now": True,
            "select_surface_now": True,
            "accept_successor_surface_now": True,
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
    boundary_audit["c8_return_to_surface_selection_acceptance_boundary_audit_id"] = "c8_return_to_surface_selection_acceptance_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    gate_results = {
        "RETURN_ACCEPTANCE_0_SOURCE_RETURN_RECEIPT_PASS": return_receipt.get("gate") == "PASS",
        "RETURN_ACCEPTANCE_1_HUMAN_DECISION_AVAILABLE": HUMAN_DECISION in return_options.get("human_decision_options", []),
        "RETURN_ACCEPTANCE_2_RETURN_PACKET_READY": return_packet.get("return_packet_status") == "READY_FOR_REVIEW",
        "RETURN_ACCEPTANCE_3_FUTURE_UNIT_MATCH": return_packet.get("if_accepted_authorizes_future_unit") == AUTHORIZED_FUTURE_UNIT,
        "RETURN_ACCEPTANCE_4_SELECTION_AUTHORIZED_AFTER_REVIEW": acceptance_packet["successor_surface_selection_authorized_after_review"] is True,
        "RETURN_ACCEPTANCE_5_NO_SURFACE_SELECTED_NOW": acceptance_packet["surface_selected_now"] is False and acceptance_packet["successor_surface_accepted_now"] is False,
        "RETURN_ACCEPTANCE_6_NO_PROBE_OR_EXECUTION_NOW": acceptance_packet["probe_prep_created_now"] is False and acceptance_packet["probe_execution_authorized_now"] is False and acceptance_packet["probe_executed_now"] is False,
        "RETURN_ACCEPTANCE_7_NO_BUILD_RERUN_SCHEMA": acceptance_packet["instrument_build_authorized_now"] is False and acceptance_packet["c8_rerun_authorized_now"] is False and acceptance_packet["reusable_schema_authorized_now"] is False,
        "RETURN_ACCEPTANCE_8_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "RETURN_ACCEPTANCE_9_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "RETURN_ACCEPTANCE_10_REQUIRES_REVIEW": acceptance_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"return_acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_PASS" if gate == "PASS" else "TYPED_C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_FAILED"

    readout = {
        "schema_version": "c8_return_to_surface_selection_acceptance_readout_v0",
        "title": "C8 return-to-surface-selection acceptance after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "closed_surface_id": CLOSED_SURFACE_ID,
        "closed_surface_kind": CLOSED_SURFACE_KIND,
        "successor_surface_selection_authorized_after_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "surface_selection_packet_created_now": False,
        "surface_selected_now": False,
        "successor_surface_accepted_now": False,
        "probe_prep_created_now": False,
        "probe_execution_authorized_now": False,
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
        "schema_version": "c8_return_to_surface_selection_acceptance_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "source_return_receipt_id": SOURCE_RETURN_RECEIPT_ID,
        "source_return_packet_id": SOURCE_RETURN_PACKET_ID,
        "source_return_options_id": SOURCE_RETURN_OPTIONS_ID,
        "closed_surface_id": CLOSED_SURFACE_ID,
        "closed_surface_kind": CLOSED_SURFACE_KIND,
        "closed_surface_label": CLOSED_SURFACE_LABEL,
        "closed_probe_id": CLOSED_PROBE_ID,
        "closed_probe_kind": CLOSED_PROBE_KIND,
        "successor_surface_selection_authorized_after_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "surface_selection_packet_created_now": False,
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
        "recommended_review_unit": acceptance_packet["recommended_review_unit"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_return_to_surface_selection_acceptance_receipt_v0",
        "receipt_type": "TYPED_C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_return_to_surface_selection_acceptance_summary": {
            "return_to_surface_selection_acceptance_complete": gate == "PASS",
            "human_decision": HUMAN_DECISION,
            "source_return_receipt_id": SOURCE_RETURN_RECEIPT_ID,
            "source_return_packet_id": SOURCE_RETURN_PACKET_ID,
            "source_return_options_id": SOURCE_RETURN_OPTIONS_ID,
            "source_return_boundary_id": SOURCE_RETURN_BOUNDARY_ID,
            "source_closure_acceptance_receipt_id": SOURCE_CLOSURE_ACCEPTANCE_RECEIPT_ID,
            "source_final_closure_id": SOURCE_FINAL_CLOSURE_ID,
            "closed_surface_id": CLOSED_SURFACE_ID,
            "closed_surface_kind": CLOSED_SURFACE_KIND,
            "closed_surface_label": CLOSED_SURFACE_LABEL,
            "closed_probe_id": CLOSED_PROBE_ID,
            "closed_probe_kind": CLOSED_PROBE_KIND,
            "closed_probe_output_class": CLOSED_PROBE_OUTPUT_CLASS,
            "successor_surface_selection_authorized_after_review": True,
            "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
            "authorized_future_unit_count_after_review": 1,
            "surface_selection_packet_created_now": False,
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
            "authority": rel(AUTHORITY),
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

    receipt["receipt_id"] = "c8_return_to_surface_selection_acceptance_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c8_return_to_surface_selection_acceptance_receipt_id={receipt['receipt_id']}")
    print(f"c8_return_to_surface_selection_acceptance_receipt_path={rel(receipt_path)}")
    print(f"c8_return_to_surface_selection_acceptance_decision_path={rel(ACCEPTANCE_DECISION)}")
    print(f"c8_return_to_surface_selection_acceptance_packet_path={rel(ACCEPTANCE_PACKET)}")
    print(f"c8_successor_surface_selection_authority_path={rel(AUTHORITY)}")
    print(f"c8_return_to_surface_selection_acceptance_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"human_decision={HUMAN_DECISION}")
    print(f"closed_surface_id={CLOSED_SURFACE_ID}")
    print(f"closed_surface_kind={CLOSED_SURFACE_KIND}")
    print(f"successor_surface_selection_authorized_after_review=true")
    print(f"authorized_future_unit_after_review={AUTHORIZED_FUTURE_UNIT}")
    print("authorized_future_unit_count_after_review=1")
    print("surface_selection_packet_created_now=false")
    print("surface_selected_now=false")
    print("successor_surface_accepted_now=false")
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
