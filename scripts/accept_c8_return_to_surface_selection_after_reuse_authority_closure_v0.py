#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_RETURN_TO_SURFACE_SELECTION_AFTER_REUSE_AUTHORITY_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.return_to_surface_selection.acceptance.after_reuse_authority_closure.v0"
MILESTONE = "C8_RETURN_TO_SURFACE_SELECTION_ACCEPTED_AFTER_REUSE_AUTHORITY_CLOSURE"
OUTCOME = "C8_RETURN_TO_SURFACE_SELECTION_ACCEPTED_FOR_REENTRY_REVIEW"
STOP_CODE = "STOP_C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_READY_FOR_REVIEW"

HUMAN_DECISION = "ACCEPT_RETURN_TO_SURFACE_SELECTION"

PREVIOUS_SURFACE_ID = "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0"
PREVIOUS_SURFACE_KIND = "REUSE_AUTHORITY_BOUNDARY_SURFACE"
PREVIOUS_SURFACE_LABEL = "C8_POST_CLOSURE_LOCAL_LOOP_REUSE_PRESSURE_SURFACE"

OUT_DIR = ROOT / "data/c8_return_to_surface_selection_acceptance_after_reuse_authority_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_return_to_surface_selection_acceptance_after_reuse_authority_closure_v0_receipts"

RETURN_RECEIPT = ROOT / "data/c8_return_to_surface_selection_after_reuse_authority_closure_v0_receipts/c8_return_to_surface_selection_receipt_e1b23af9.json"
RETURN_PACKET = ROOT / "data/c8_return_to_surface_selection_after_reuse_authority_closure_v0/c8_return_to_surface_selection_packet_v0.json"
RETURN_BOUNDARY = ROOT / "data/c8_return_to_surface_selection_after_reuse_authority_closure_v0/c8_return_to_surface_selection_boundary_v0.json"
RETURN_REPORT = ROOT / "data/c8_return_to_surface_selection_after_reuse_authority_closure_v0/c8_return_to_surface_selection_report.json"

ACCEPTANCE_DECISION = OUT_DIR / "c8_return_to_surface_selection_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = OUT_DIR / "c8_return_to_surface_selection_acceptance_packet_v0.json"
REENTRY_BOUNDARY = OUT_DIR / "c8_surface_selection_reentry_boundary_v0.json"
READOUT = OUT_DIR / "c8_return_to_surface_selection_acceptance_readout_v0.json"
REPORT = OUT_DIR / "c8_return_to_surface_selection_acceptance_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "next_surface_selected_count",
    "surface_selection_executed_count",
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
        "return_receipt": RETURN_RECEIPT,
        "return_packet": RETURN_PACKET,
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
    return_boundary = read_json(RETURN_BOUNDARY)
    return_report = read_json(RETURN_REPORT)
    summary = return_receipt.get("machine_readable_return_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_RETURN_TO_SURFACE_SELECTION_PACKET_PASS",
        "outcome_class": "C8_RETURN_TO_SURFACE_SELECTION_PACKET_READY_FOR_REVIEW",
        "receipt_id": "c8_return_to_surface_selection_receipt_e1b23af9",
    }

    for key, want in expected_receipt.items():
        chk(failures, f"return_receipt_{key}", return_receipt.get(key), want)

    expected_summary = {
        "return_to_selection_packet_created": True,
        "source_closure_acceptance_receipt_id": "c8_successor_reuse_authority_probe_closure_acceptance_receipt_2023bce5",
        "source_closure_acceptance_packet_id": "c8_successor_reuse_authority_probe_closure_acceptance_packet_3dc8c613",
        "source_closure_acceptance_decision_id": "c8_successor_reuse_authority_probe_closure_acceptance_decision_71bde511",
        "source_final_closure_id": "c8_successor_reuse_authority_probe_final_closure_e8a1bd0e",
        "source_boundary_audit_id": "c8_successor_reuse_authority_probe_closure_acceptance_boundary_2372ce81",
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "previous_surface_closed": True,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed": True,
        "next_surface_selected_now": False,
        "next_surface_selection_authorized_now": False,
        "next_probe_authorized_now": False,
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
        "human_review_required": True,
        "recommended_review_unit": "REVIEW_C8_RETURN_TO_SURFACE_SELECTION_PACKET_AFTER_REUSE_AUTHORITY_CLOSURE_V0",
        "next_command_goal": None,
    }

    for key, want in expected_summary.items():
        chk(failures, f"return_summary_{key}", summary.get(key), want)

    chk(failures, "return_packet_id", return_packet.get("return_to_selection_packet_id"), "c8_return_to_surface_selection_packet_497f97dd")
    chk(failures, "return_boundary_id", return_boundary.get("boundary_id"), "c8_return_to_surface_selection_boundary_6b7e2995")

    decision_options = return_packet.get("recommended_next_decision_options", [])
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
        "schema_version": "c8_return_to_surface_selection_acceptance_decision_v0",
        "return_to_selection_acceptance_decision_id": None,
        "human_decision": HUMAN_DECISION,
        "source_return_to_selection_receipt_id": return_receipt.get("receipt_id"),
        "source_return_to_selection_packet_id": return_packet.get("return_to_selection_packet_id"),
        "source_return_to_selection_boundary_id": return_boundary.get("boundary_id"),
        "source_closure_acceptance_receipt_id": summary.get("source_closure_acceptance_receipt_id"),
        "source_final_closure_id": summary.get("source_final_closure_id"),
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "return_to_surface_selection_accepted": True,
        "surface_selection_reentry_accepted": True,
        "surface_selection_reentry_ready_after_review": True,
        "human_decision_consumed": True,
        "next_surface_selected_now": False,
        "surface_selection_executed_now": False,
        "next_probe_authorized_now": False,
        "instrument_build_authorized_now": False,
        "cell1_build_authorized_now": False,
        "verification_probe_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "missing_instrument_proposal_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
    }
    acceptance_decision["return_to_selection_acceptance_decision_id"] = "c8_return_to_selection_acceptance_decision_" + sig8(acceptance_decision)
    write_json(ACCEPTANCE_DECISION, acceptance_decision)

    acceptance_packet = {
        "schema_version": "c8_return_to_surface_selection_acceptance_packet_v0",
        "return_to_selection_acceptance_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "acceptance_status": "RETURN_TO_SURFACE_SELECTION_ACCEPTED_FOR_REENTRY_REVIEW",
        "human_decision": HUMAN_DECISION,
        "source_return_to_selection_receipt_id": return_receipt.get("receipt_id"),
        "source_return_to_selection_packet_id": return_packet.get("return_to_selection_packet_id"),
        "source_return_to_selection_boundary_id": return_boundary.get("boundary_id"),
        "source_closure_acceptance_receipt_id": summary.get("source_closure_acceptance_receipt_id"),
        "source_final_closure_id": summary.get("source_final_closure_id"),
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "previous_surface_closed": True,
        "previous_surface_closed_with_no_new_authority": True,
        "return_to_surface_selection_accepted": True,
        "surface_selection_reentry_accepted": True,
        "surface_selection_reentry_ready_after_review": True,
        "next_surface_selected_now": False,
        "surface_selection_executed_now": False,
        "next_probe_authorized_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": "REVIEW_C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_AFTER_REUSE_AUTHORITY_CLOSURE_V0",
    }
    acceptance_packet["return_to_selection_acceptance_packet_id"] = "c8_return_to_selection_acceptance_packet_" + sig8(acceptance_packet)
    write_json(ACCEPTANCE_PACKET, acceptance_packet)

    reentry_boundary = {
        "schema_version": "c8_surface_selection_reentry_boundary_v0",
        "surface_selection_reentry_boundary_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_return_to_selection_acceptance_packet_id": acceptance_packet["return_to_selection_acceptance_packet_id"],
        "source_return_to_selection_acceptance_decision_id": acceptance_decision["return_to_selection_acceptance_decision_id"],
        "human_decision": HUMAN_DECISION,
        "allowed_now": {
            "record_return_to_surface_selection_acceptance": True,
            "prepare_surface_selection_reentry_for_review": True,
        },
        "not_allowed_now": {
            "select_next_surface": True,
            "execute_surface_selection": True,
            "authorize_probe": True,
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
    reentry_boundary["surface_selection_reentry_boundary_id"] = "c8_surface_selection_reentry_boundary_" + sig8(reentry_boundary)
    write_json(REENTRY_BOUNDARY, reentry_boundary)

    gate_results = {
        "RETURN_SELECTION_ACCEPTANCE_0_SOURCE_RECEIPT_PASS": return_receipt.get("gate") == "PASS",
        "RETURN_SELECTION_ACCEPTANCE_1_HUMAN_DECISION_AVAILABLE": HUMAN_DECISION in decision_options,
        "RETURN_SELECTION_ACCEPTANCE_2_PREVIOUS_SURFACE_CLOSED": summary.get("previous_surface_closed") is True,
        "RETURN_SELECTION_ACCEPTANCE_3_CLOSED_WITH_NO_NEW_AUTHORITY": summary.get("closed_with_no_new_authority") is True,
        "RETURN_SELECTION_ACCEPTANCE_4_RETURN_ALLOWED": summary.get("return_to_surface_selection_allowed") is True,
        "RETURN_SELECTION_ACCEPTANCE_5_ACCEPTANCE_RECORDED": acceptance_packet["return_to_surface_selection_accepted"] is True,
        "RETURN_SELECTION_ACCEPTANCE_6_NO_NEXT_SURFACE_SELECTED_NOW": acceptance_packet["next_surface_selected_now"] is False,
        "RETURN_SELECTION_ACCEPTANCE_7_NO_SURFACE_SELECTION_EXECUTED_NOW": acceptance_packet["surface_selection_executed_now"] is False,
        "RETURN_SELECTION_ACCEPTANCE_8_NO_PROBE_BUILD_RERUN_SCHEMA": acceptance_packet["next_probe_authorized_now"] is False and acceptance_packet["instrument_build_authorized_now"] is False and acceptance_packet["c8_rerun_authorized_now"] is False and acceptance_packet["reusable_schema_authorized_now"] is False,
        "RETURN_SELECTION_ACCEPTANCE_9_NO_GLOBAL_OR_FRONTIER_CLAIM": acceptance_decision["global_solution_claim"] is False and acceptance_decision["frontier_solved_claim"] is False,
        "RETURN_SELECTION_ACCEPTANCE_10_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "RETURN_SELECTION_ACCEPTANCE_11_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "RETURN_SELECTION_ACCEPTANCE_12_RESULT_REQUIRES_REVIEW": acceptance_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_PASS" if gate == "PASS" else "TYPED_C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_FAILED"

    readout = {
        "schema_version": "c8_return_to_surface_selection_acceptance_readout_v0",
        "title": "C8 return-to-surface-selection acceptance after reuse-authority closure",
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "return_to_selection_acceptance_packet_id": acceptance_packet["return_to_selection_acceptance_packet_id"],
        "return_to_selection_acceptance_decision_id": acceptance_decision["return_to_selection_acceptance_decision_id"],
        "source_return_to_selection_receipt_id": return_receipt.get("receipt_id"),
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "return_to_surface_selection_accepted": True,
        "surface_selection_reentry_accepted": True,
        "surface_selection_reentry_ready_after_review": True,
        "next_surface_selected_now": False,
        "surface_selection_executed_now": False,
        "next_probe_authorized_now": False,
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
        "source_return_to_selection_receipt_id": return_receipt.get("receipt_id"),
        "source_return_to_selection_packet_id": return_packet.get("return_to_selection_packet_id"),
        "source_return_to_selection_boundary_id": return_boundary.get("boundary_id"),
        "source_closure_acceptance_receipt_id": summary.get("source_closure_acceptance_receipt_id"),
        "source_final_closure_id": summary.get("source_final_closure_id"),
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "human_decision": HUMAN_DECISION,
        "return_to_surface_selection_accepted": True,
        "surface_selection_reentry_accepted": True,
        "surface_selection_reentry_ready_after_review": True,
        "next_surface_selected_now": False,
        "surface_selection_executed_now": False,
        "next_probe_authorized_now": False,
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
        "machine_readable_acceptance_summary": {
            "return_to_selection_acceptance_complete": gate == "PASS",
            "human_decision": HUMAN_DECISION,
            "source_return_to_selection_receipt_id": return_receipt.get("receipt_id"),
            "source_return_to_selection_packet_id": return_packet.get("return_to_selection_packet_id"),
            "source_return_to_selection_boundary_id": return_boundary.get("boundary_id"),
            "source_closure_acceptance_receipt_id": summary.get("source_closure_acceptance_receipt_id"),
            "source_final_closure_id": summary.get("source_final_closure_id"),
            "previous_surface_id": PREVIOUS_SURFACE_ID,
            "previous_surface_kind": PREVIOUS_SURFACE_KIND,
            "previous_surface_label": PREVIOUS_SURFACE_LABEL,
            "previous_surface_closed": True,
            "previous_surface_closed_with_no_new_authority": True,
            "return_to_surface_selection_accepted": True,
            "surface_selection_reentry_accepted": True,
            "surface_selection_reentry_ready_after_review": True,
            "next_surface_selected_now": False,
            "surface_selection_executed_now": False,
            "next_probe_authorized_now": False,
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
            "reentry_boundary": rel(REENTRY_BOUNDARY),
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

    receipt["receipt_id"] = "c8_return_to_selection_acceptance_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"return_to_selection_acceptance_receipt_id={receipt['receipt_id']}")
    print(f"return_to_selection_acceptance_receipt_path={rel(receipt_path)}")
    print(f"return_to_selection_acceptance_packet_path={rel(ACCEPTANCE_PACKET)}")
    print(f"return_to_selection_acceptance_decision_path={rel(ACCEPTANCE_DECISION)}")
    print(f"surface_selection_reentry_boundary_path={rel(REENTRY_BOUNDARY)}")
    print(f"source_return_to_selection_receipt_id={return_receipt.get('receipt_id')}")
    print(f"source_return_to_selection_packet_id={return_packet.get('return_to_selection_packet_id')}")
    print(f"previous_surface_id={PREVIOUS_SURFACE_ID}")
    print("return_to_surface_selection_accepted=true")
    print("surface_selection_reentry_accepted=true")
    print("surface_selection_reentry_ready_after_review=true")
    print("next_surface_selected_now=false")
    print("surface_selection_executed_now=false")
    print("next_probe_authorized_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={acceptance_packet['recommended_review_unit']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
