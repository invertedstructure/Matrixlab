#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_RETURN_TO_SURFACE_SELECTION_PACKET_AFTER_REUSE_AUTHORITY_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.return_to_surface_selection.after_reuse_authority_closure.v0"
MILESTONE = "C8_RETURN_TO_SURFACE_SELECTION_PACKET_CREATED_AFTER_REUSE_AUTHORITY_CLOSURE"
OUTCOME = "C8_RETURN_TO_SURFACE_SELECTION_PACKET_READY_FOR_REVIEW"
STOP_CODE = "STOP_C8_RETURN_TO_SURFACE_SELECTION_PACKET_READY_FOR_REVIEW"

PREVIOUS_SURFACE_ID = "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0"
PREVIOUS_SURFACE_KIND = "REUSE_AUTHORITY_BOUNDARY_SURFACE"
PREVIOUS_SURFACE_LABEL = "C8_POST_CLOSURE_LOCAL_LOOP_REUSE_PRESSURE_SURFACE"

OUT_DIR = ROOT / "data/c8_return_to_surface_selection_after_reuse_authority_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_return_to_surface_selection_after_reuse_authority_closure_v0_receipts"

ACCEPTANCE_RECEIPT = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_acceptance_v0_receipts/c8_successor_reuse_authority_probe_closure_acceptance_receipt_2023bce5.json"
ACCEPTANCE_PACKET = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_acceptance_v0/c8_successor_surface_reuse_authority_probe_closure_acceptance_packet_v0.json"
ACCEPTANCE_DECISION = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_acceptance_v0/c8_successor_surface_reuse_authority_probe_closure_acceptance_decision_v0.json"
FINAL_CLOSURE = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_acceptance_v0/c8_successor_surface_reuse_authority_probe_final_closure_v0.json"
BOUNDARY_AUDIT = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_acceptance_v0/c8_successor_surface_reuse_authority_probe_closure_acceptance_boundary_audit_v0.json"
ACCEPTANCE_REPORT = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_closure_acceptance_v0/c8_successor_surface_reuse_authority_probe_closure_acceptance_report.json"

RETURN_PACKET = OUT_DIR / "c8_return_to_surface_selection_packet_v0.json"
BOUNDARY = OUT_DIR / "c8_return_to_surface_selection_boundary_v0.json"
READOUT = OUT_DIR / "c8_return_to_surface_selection_readout_v0.json"
REPORT = OUT_DIR / "c8_return_to_surface_selection_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "next_surface_selected_count",
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
        "acceptance_receipt": ACCEPTANCE_RECEIPT,
        "acceptance_packet": ACCEPTANCE_PACKET,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "final_closure": FINAL_CLOSURE,
        "boundary_audit": BOUNDARY_AUDIT,
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
    acceptance_packet = read_json(ACCEPTANCE_PACKET)
    acceptance_decision = read_json(ACCEPTANCE_DECISION)
    final_closure = read_json(FINAL_CLOSURE)
    boundary_audit = read_json(BOUNDARY_AUDIT)
    acceptance_report = read_json(ACCEPTANCE_REPORT)
    summary = acceptance_receipt.get("machine_readable_acceptance_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_CLOSURE_ACCEPTANCE_PASS",
        "outcome_class": "C8_SUCCESSOR_SURFACE_CLOSED_NO_NEW_AUTHORITY",
        "receipt_id": "c8_successor_reuse_authority_probe_closure_acceptance_receipt_2023bce5",
    }

    for key, want in expected_receipt.items():
        chk(failures, f"acceptance_receipt_{key}", acceptance_receipt.get(key), want)

    expected_summary = {
        "closure_acceptance_complete": True,
        "human_decision": "ACCEPT_CLOSURE_NO_NEW_AUTHORITY",
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
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "next_command_goal": None,
    }

    for key, want in expected_summary.items():
        chk(failures, f"acceptance_summary_{key}", summary.get(key), want)

    chk(failures, "selected_surface_id", summary.get("selected_surface_id"), PREVIOUS_SURFACE_ID)
    chk(failures, "selected_surface_kind", summary.get("selected_surface_kind"), PREVIOUS_SURFACE_KIND)
    chk(failures, "selected_surface_label", summary.get("selected_surface_label"), PREVIOUS_SURFACE_LABEL)

    chk(failures, "acceptance_packet_id", acceptance_packet.get("closure_acceptance_packet_id"), "c8_successor_reuse_authority_probe_closure_acceptance_packet_3dc8c613")
    chk(failures, "acceptance_decision_id", acceptance_decision.get("closure_acceptance_decision_id"), "c8_successor_reuse_authority_probe_closure_acceptance_decision_71bde511")
    chk(failures, "final_closure_id", final_closure.get("final_closure_id"), "c8_successor_reuse_authority_probe_final_closure_e8a1bd0e")
    chk(failures, "boundary_audit_id", boundary_audit.get("boundary_audit_id"), "c8_successor_reuse_authority_probe_closure_acceptance_boundary_2372ce81")

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
        "schema_version": "c8_return_to_surface_selection_packet_v0",
        "return_to_selection_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "packet_status": "RETURN_TO_SURFACE_SELECTION_CREATED_FOR_REVIEW",
        "source_closure_acceptance_receipt_id": acceptance_receipt.get("receipt_id"),
        "source_closure_acceptance_packet_id": acceptance_packet.get("closure_acceptance_packet_id"),
        "source_closure_acceptance_decision_id": acceptance_decision.get("closure_acceptance_decision_id"),
        "source_final_closure_id": final_closure.get("final_closure_id"),
        "source_boundary_audit_id": boundary_audit.get("boundary_audit_id"),
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "previous_surface_closed": True,
        "previous_surface_closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed": True,
        "next_surface_selected_now": False,
        "next_surface_selection_authorized_now": False,
        "next_probe_authorized_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "human_review_required": True,
        "recommended_review_unit": "REVIEW_C8_RETURN_TO_SURFACE_SELECTION_PACKET_AFTER_REUSE_AUTHORITY_CLOSURE_V0",
        "recommended_next_decision_options": [
            "ACCEPT_RETURN_TO_SURFACE_SELECTION",
            "REJECT_RETURN_TO_SURFACE_SELECTION_PACKET",
            "REQUEST_NARROWER_RETURN_TO_SELECTION_PACKET",
        ],
    }
    packet["return_to_selection_packet_id"] = "c8_return_to_surface_selection_packet_" + sig8(packet)
    write_json(RETURN_PACKET, packet)

    boundary = {
        "schema_version": "c8_return_to_surface_selection_boundary_v0",
        "boundary_id": None,
        "source_return_to_selection_packet_id": packet["return_to_selection_packet_id"],
        "gate": "PASS" if not failures else "FAIL",
        "allowed_now": {
            "create_return_to_surface_selection_packet": True,
            "mark_previous_surface_closed": True,
        },
        "not_allowed_now": {
            "select_next_surface": True,
            "execute_probe": True,
            "authorize_probe": True,
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
    boundary["boundary_id"] = "c8_return_to_surface_selection_boundary_" + sig8(boundary)
    write_json(BOUNDARY, boundary)

    readout = {
        "schema_version": "c8_return_to_surface_selection_readout_v0",
        "title": "C8 return to surface selection after reuse-authority closure",
        "source_closure_acceptance_receipt_id": acceptance_receipt.get("receipt_id"),
        "return_to_selection_packet_id": packet["return_to_selection_packet_id"],
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_closed": True,
        "previous_surface_closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed": True,
        "next_surface_selected_now": False,
        "next_probe_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "human_review_required": True,
        "recommended_review_unit": packet["recommended_review_unit"],
    }
    write_json(READOUT, readout)

    gate_results = {
        "RETURN_TO_SELECTION_0_SOURCE_ACCEPTANCE_RECEIPT_PASS": acceptance_receipt.get("gate") == "PASS",
        "RETURN_TO_SELECTION_1_SURFACE_CLOSED": summary.get("current_successor_surface_closed") is True,
        "RETURN_TO_SELECTION_2_CLOSED_WITH_NO_NEW_AUTHORITY": summary.get("closed_with_no_new_authority") is True,
        "RETURN_TO_SELECTION_3_RETURN_ALLOWED_AFTER_REVIEW": summary.get("return_to_surface_selection_allowed_after_review") is True,
        "RETURN_TO_SELECTION_4_NO_NEXT_SURFACE_SELECTED_NOW": summary.get("next_surface_selected_now") is False,
        "RETURN_TO_SELECTION_5_NO_PROBE_BUILD_RERUN_SCHEMA": summary.get("additional_probe_authorized_now") is False and summary.get("instrument_built_now") is False and summary.get("c8_rerun_now") is False and summary.get("reusable_schema_authorized") is False,
        "RETURN_TO_SELECTION_6_NO_GLOBAL_OR_FRONTIER_CLAIM": summary.get("global_solution_claim") is False and summary.get("frontier_solved_claim") is False,
        "RETURN_TO_SELECTION_7_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "RETURN_TO_SELECTION_8_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "RETURN_TO_SELECTION_9_PACKET_REQUIRES_REVIEW": packet["human_review_required"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"return_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_RETURN_TO_SURFACE_SELECTION_PACKET_PASS" if gate == "PASS" else "TYPED_C8_RETURN_TO_SURFACE_SELECTION_PACKET_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_RETURN_TO_SURFACE_SELECTION_PACKET_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_RETURN_TO_SURFACE_SELECTION_PACKET_FAILED"

    report = {
        "schema_version": "c8_return_to_surface_selection_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_closure_acceptance_receipt_id": acceptance_receipt.get("receipt_id"),
        "source_closure_acceptance_packet_id": acceptance_packet.get("closure_acceptance_packet_id"),
        "source_final_closure_id": final_closure.get("final_closure_id"),
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "previous_surface_closed": True,
        "closed_with_no_new_authority": True,
        "return_to_surface_selection_allowed": True,
        "next_surface_selected_now": False,
        "next_probe_authorized_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "human_review_required": True,
        "recommended_review_unit": packet["recommended_review_unit"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_return_to_surface_selection_receipt_v0",
        "receipt_type": "TYPED_C8_RETURN_TO_SURFACE_SELECTION_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_return_summary": {
            "return_to_selection_packet_created": gate == "PASS",
            "source_closure_acceptance_receipt_id": acceptance_receipt.get("receipt_id"),
            "source_closure_acceptance_packet_id": acceptance_packet.get("closure_acceptance_packet_id"),
            "source_closure_acceptance_decision_id": acceptance_decision.get("closure_acceptance_decision_id"),
            "source_final_closure_id": final_closure.get("final_closure_id"),
            "source_boundary_audit_id": boundary_audit.get("boundary_audit_id"),
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
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
            "forbidden_counters_zero": not bool(local_nonzero),
            "human_review_required": True,
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
            "return_to_selection_packet": rel(RETURN_PACKET),
            "boundary": rel(BOUNDARY),
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
    print(f"return_to_selection_receipt_id={receipt['receipt_id']}")
    print(f"return_to_selection_receipt_path={rel(receipt_path)}")
    print(f"return_to_selection_packet_path={rel(RETURN_PACKET)}")
    print(f"return_to_selection_boundary_path={rel(BOUNDARY)}")
    print(f"source_closure_acceptance_receipt_id={acceptance_receipt.get('receipt_id')}")
    print(f"source_final_closure_id={final_closure.get('final_closure_id')}")
    print(f"previous_surface_id={PREVIOUS_SURFACE_ID}")
    print("previous_surface_closed=true")
    print("closed_with_no_new_authority=true")
    print("return_to_surface_selection_allowed=true")
    print("next_surface_selected_now=false")
    print("next_probe_authorized_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={packet['recommended_review_unit']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
