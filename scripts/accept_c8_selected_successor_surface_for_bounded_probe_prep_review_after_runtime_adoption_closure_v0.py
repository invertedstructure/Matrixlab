#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_SELECTED_SUCCESSOR_SURFACE_FOR_BOUNDED_PROBE_PREP_REVIEW_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.selected_successor_surface.acceptance_for_bounded_probe_prep_review.after_runtime_adoption_closure.v0"
MILESTONE = "C8_SELECTED_SUCCESSOR_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_PREP_REVIEW_AFTER_RUNTIME_ADOPTION_CLOSURE"
OUTCOME = "C8_SELECTED_SUCCESSOR_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_PREP_REVIEW"
STOP_CODE = "STOP_C8_SELECTED_SUCCESSOR_SURFACE_ACCEPTANCE_READY_FOR_REVIEW"

HUMAN_DECISION = "ACCEPT_SELECTED_SUCCESSOR_SURFACE_FOR_BOUNDED_PROBE_PREP_REVIEW"
AUTHORIZED_FUTURE_UNIT = "CREATE_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

SOURCE_SELECTION_RECEIPT_ID = "c8_successor_surface_selection_receipt_5a63647b"
SOURCE_SELECTION_PACKET_ID = "c8_successor_surface_selection_packet_2168881d"
SOURCE_SELECTION_BOUNDARY_ID = "c8_successor_surface_selection_boundary_ca701b13"

SOURCE_ACCEPTANCE_RECEIPT_ID = "c8_return_to_surface_selection_acceptance_receipt_15807948"
SOURCE_ACCEPTANCE_DECISION_ID = "c8_return_to_surface_selection_acceptance_decision_43089b84"
SOURCE_ACCEPTANCE_PACKET_ID = "c8_return_to_surface_selection_acceptance_packet_f7aaaa5b"
SOURCE_SUCCESSOR_SURFACE_SELECTION_AUTHORITY_ID = "c8_successor_surface_selection_authority_984254c6"
SOURCE_ACCEPTANCE_BOUNDARY_ID = "c8_return_to_surface_selection_acceptance_boundary_ec1b4c36"

CLOSED_SURFACE_ID = "c8_successor_surface_runtime_adoption_after_reentry_v0"
CLOSED_SURFACE_KIND = "RUNTIME_ADOPTION_SURFACE"
CLOSED_SURFACE_LABEL = "C8_RUNTIME_ADOPTION_AFTER_REUSE_AUTHORITY_CLOSURE_SURFACE"
CLOSED_PROBE_ID = "c8_runtime_adoption_surface_bounded_probe_after_reentry_v0"
CLOSED_PROBE_KIND = "RUNTIME_ADOPTION_BOUNDARY_PROBE"
CLOSED_PROBE_OUTPUT_CLASS = "RUNTIME_ADOPTION_BOUNDARY_PROBE_OBSERVED_NO_DEFECTS"

SELECTED_SURFACE_ID = "c8_successor_surface_unit_feedback_hardening_after_runtime_adoption_closure_v0"
SELECTED_SURFACE_KIND = "UNIT_FEEDBACK_HARDENING_SURFACE"
SELECTED_SURFACE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_AFTER_RUNTIME_ADOPTION_CLOSURE_SURFACE"

OUT_DIR = ROOT / "data/c8_selected_successor_surface_acceptance_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_selected_successor_surface_acceptance_after_runtime_adoption_closure_v0_receipts"

SELECTION_RECEIPT = ROOT / "data/c8_successor_surface_selection_after_runtime_adoption_closure_v0_receipts/c8_successor_surface_selection_receipt_5a63647b.json"
SELECTION_PACKET = ROOT / "data/c8_successor_surface_selection_after_runtime_adoption_closure_v0/c8_successor_surface_selection_packet_v0.json"
SELECTION_BOUNDARY = ROOT / "data/c8_successor_surface_selection_after_runtime_adoption_closure_v0/c8_successor_surface_selection_boundary_audit_v0.json"
SELECTION_REPORT = ROOT / "data/c8_successor_surface_selection_after_runtime_adoption_closure_v0/c8_successor_surface_selection_report.json"
SELECTION_READOUT = ROOT / "data/c8_successor_surface_selection_after_runtime_adoption_closure_v0/c8_successor_surface_selection_readout_v0.json"

ACCEPTANCE_DECISION = OUT_DIR / "c8_selected_successor_surface_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = OUT_DIR / "c8_selected_successor_surface_acceptance_packet_v0.json"
PROBE_PREP_AUTHORITY = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_prep_authority_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_selected_successor_surface_acceptance_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_selected_successor_surface_acceptance_readout_v0.json"
REPORT = OUT_DIR / "c8_selected_successor_surface_acceptance_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "bounded_probe_prep_packet_created_count",
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
        "selection_receipt": SELECTION_RECEIPT,
        "selection_packet": SELECTION_PACKET,
        "selection_boundary": SELECTION_BOUNDARY,
        "selection_report": SELECTION_REPORT,
        "selection_readout": SELECTION_READOUT,
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
    selection_boundary = read_json(SELECTION_BOUNDARY)
    selection_report = read_json(SELECTION_REPORT)
    selection_summary = selection_receipt.get("machine_readable_successor_surface_selection_summary", {})

    expected_selection_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_SUCCESSOR_SURFACE_SELECTION_PASS",
        "outcome_class": "C8_SUCCESSOR_SURFACE_SELECTION_READY_FOR_REVIEW",
        "receipt_id": SOURCE_SELECTION_RECEIPT_ID,
    }
    for key, want in expected_selection_receipt.items():
        chk(failures, f"selection_receipt_{key}", selection_receipt.get(key), want)

    expected_selection_summary = {
        "successor_surface_selection_complete": True,
        "authorized_unit_consumed": "SELECT_C8_SUCCESSOR_SURFACE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
        "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_successor_surface_selection_authority_id": SOURCE_SUCCESSOR_SURFACE_SELECTION_AUTHORITY_ID,
        "source_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
        "closed_surface_id": CLOSED_SURFACE_ID,
        "closed_surface_kind": CLOSED_SURFACE_KIND,
        "closed_surface_label": CLOSED_SURFACE_LABEL,
        "closed_probe_id": CLOSED_PROBE_ID,
        "closed_probe_kind": CLOSED_PROBE_KIND,
        "closed_probe_output_class": CLOSED_PROBE_OUTPUT_CLASS,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "surface_selection_packet_created_now": True,
        "surface_selected_now": True,
        "successor_surface_accepted_now": False,
        "probe_prep_created_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized": False,
        "requires_review": True,
        "recommended_human_decision": HUMAN_DECISION,
        "next_command_goal": None,
    }
    for key, want in expected_selection_summary.items():
        chk(failures, f"selection_summary_{key}", selection_summary.get(key), want)

    chk(failures, "selection_packet_id", selection_packet.get("c8_successor_surface_selection_packet_id"), SOURCE_SELECTION_PACKET_ID)
    chk(failures, "selection_boundary_id", selection_boundary.get("c8_successor_surface_selection_boundary_audit_id"), SOURCE_SELECTION_BOUNDARY_ID)

    if HUMAN_DECISION != selection_packet.get("recommended_human_decision"):
        failures.append(f"recommended_human_decision_wrong:{selection_packet.get('recommended_human_decision')}")

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
        "schema_version": "c8_selected_successor_surface_acceptance_decision_v0",
        "c8_selected_successor_surface_acceptance_decision_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "human_decision": HUMAN_DECISION,
        "human_decision_consumed": True,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
        "source_selection_boundary_id": SOURCE_SELECTION_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_successor_surface_accepted_for_bounded_probe_prep_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "bounded_probe_prep_packet_created_now": False,
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
    acceptance_decision["c8_selected_successor_surface_acceptance_decision_id"] = "c8_selected_successor_surface_acceptance_decision_" + sig8(acceptance_decision)
    write_json(ACCEPTANCE_DECISION, acceptance_decision)

    probe_prep_authority = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_prep_authority_v0",
        "c8_unit_feedback_hardening_bounded_probe_prep_authority_id": None,
        "created_at": now_iso(),
        "source_acceptance_decision_id": acceptance_decision["c8_selected_successor_surface_acceptance_decision_id"],
        "source_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authority_status": "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "authority_scope": {
            "may_create_bounded_probe_prep_packet": True,
            "may_authorize_probe_execution_now": False,
            "may_execute_probe_now": False,
            "may_build_now": False,
            "may_rerun_c8_now": False,
            "may_promote_schema_now": False,
        },
    }
    probe_prep_authority["c8_unit_feedback_hardening_bounded_probe_prep_authority_id"] = "c8_unit_feedback_hardening_bounded_probe_prep_authority_" + sig8(probe_prep_authority)
    write_json(PROBE_PREP_AUTHORITY, probe_prep_authority)

    acceptance_packet = {
        "schema_version": "c8_selected_successor_surface_acceptance_packet_v0",
        "c8_selected_successor_surface_acceptance_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "acceptance_status": "SELECTED_SUCCESSOR_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_PREP_REVIEW",
        "human_decision": HUMAN_DECISION,
        "source_acceptance_decision_id": acceptance_decision["c8_selected_successor_surface_acceptance_decision_id"],
        "source_bounded_probe_prep_authority_id": probe_prep_authority["c8_unit_feedback_hardening_bounded_probe_prep_authority_id"],
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
        "source_selection_boundary_id": SOURCE_SELECTION_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_successor_surface_accepted_for_bounded_probe_prep_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "bounded_probe_prep_packet_created_now": False,
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
        "recommended_review_unit": "REVIEW_C8_SELECTED_SUCCESSOR_SURFACE_ACCEPTANCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
    }
    acceptance_packet["c8_selected_successor_surface_acceptance_packet_id"] = "c8_selected_successor_surface_acceptance_packet_" + sig8(acceptance_packet)
    write_json(ACCEPTANCE_PACKET, acceptance_packet)

    boundary_audit = {
        "schema_version": "c8_selected_successor_surface_acceptance_boundary_audit_v0",
        "c8_selected_successor_surface_acceptance_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_acceptance_decision_id": acceptance_decision["c8_selected_successor_surface_acceptance_decision_id"],
        "source_acceptance_packet_id": acceptance_packet["c8_selected_successor_surface_acceptance_packet_id"],
        "source_bounded_probe_prep_authority_id": probe_prep_authority["c8_unit_feedback_hardening_bounded_probe_prep_authority_id"],
        "source_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
        "allowed_now": {
            "accept_selected_successor_surface_for_bounded_probe_prep_review": True,
            "authorize_bounded_probe_prep_packet_after_review": True,
        },
        "not_allowed_now": {
            "create_bounded_probe_prep_packet_now": True,
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
    boundary_audit["c8_selected_successor_surface_acceptance_boundary_audit_id"] = "c8_selected_successor_surface_acceptance_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    gate_results = {
        "SELECTED_SURFACE_ACCEPTANCE_0_SOURCE_SELECTION_RECEIPT_PASS": selection_receipt.get("gate") == "PASS",
        "SELECTED_SURFACE_ACCEPTANCE_1_HUMAN_DECISION_MATCH": selection_packet.get("recommended_human_decision") == HUMAN_DECISION,
        "SELECTED_SURFACE_ACCEPTANCE_2_SELECTED_SURFACE_MATCH": selection_packet.get("selected_surface_id") == SELECTED_SURFACE_ID,
        "SELECTED_SURFACE_ACCEPTANCE_3_ACCEPTANCE_AUTHORIZES_PREP_ONLY": acceptance_packet["authorized_future_unit_after_review"] == AUTHORIZED_FUTURE_UNIT,
        "SELECTED_SURFACE_ACCEPTANCE_4_NO_PREP_PACKET_CREATED_NOW": acceptance_packet["bounded_probe_prep_packet_created_now"] is False,
        "SELECTED_SURFACE_ACCEPTANCE_5_NO_EXECUTION_NOW": acceptance_packet["probe_execution_authorized_now"] is False and acceptance_packet["probe_executed_now"] is False,
        "SELECTED_SURFACE_ACCEPTANCE_6_NO_BUILD_RERUN_SCHEMA": acceptance_packet["instrument_build_authorized_now"] is False and acceptance_packet["c8_rerun_authorized_now"] is False and acceptance_packet["reusable_schema_authorized_now"] is False,
        "SELECTED_SURFACE_ACCEPTANCE_7_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "SELECTED_SURFACE_ACCEPTANCE_8_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "SELECTED_SURFACE_ACCEPTANCE_9_REQUIRES_REVIEW": acceptance_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"selected_surface_acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_SELECTED_SUCCESSOR_SURFACE_ACCEPTANCE_PASS" if gate == "PASS" else "TYPED_C8_SELECTED_SUCCESSOR_SURFACE_ACCEPTANCE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_SELECTED_SUCCESSOR_SURFACE_ACCEPTANCE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_SELECTED_SUCCESSOR_SURFACE_ACCEPTANCE_FAILED"

    readout = {
        "schema_version": "c8_selected_successor_surface_acceptance_readout_v0",
        "title": "C8 selected successor surface acceptance after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_successor_surface_accepted_for_bounded_probe_prep_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "bounded_probe_prep_packet_created_now": False,
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
        "schema_version": "c8_selected_successor_surface_acceptance_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
        "source_selection_boundary_id": SOURCE_SELECTION_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_successor_surface_accepted_for_bounded_probe_prep_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "bounded_probe_prep_packet_created_now": False,
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
        "schema_version": "c8_selected_successor_surface_acceptance_receipt_v0",
        "receipt_type": "TYPED_C8_SELECTED_SUCCESSOR_SURFACE_ACCEPTANCE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_selected_successor_surface_acceptance_summary": {
            "selected_successor_surface_acceptance_complete": gate == "PASS",
            "human_decision": HUMAN_DECISION,
            "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
            "source_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
            "source_selection_boundary_id": SOURCE_SELECTION_BOUNDARY_ID,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "selected_successor_surface_accepted_for_bounded_probe_prep_review": True,
            "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
            "authorized_future_unit_count_after_review": 1,
            "bounded_probe_prep_packet_created_now": False,
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
            "probe_prep_authority": rel(PROBE_PREP_AUTHORITY),
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

    receipt["receipt_id"] = "c8_selected_successor_surface_acceptance_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c8_selected_successor_surface_acceptance_receipt_id={receipt['receipt_id']}")
    print(f"c8_selected_successor_surface_acceptance_receipt_path={rel(receipt_path)}")
    print(f"c8_selected_successor_surface_acceptance_decision_path={rel(ACCEPTANCE_DECISION)}")
    print(f"c8_selected_successor_surface_acceptance_packet_path={rel(ACCEPTANCE_PACKET)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_prep_authority_path={rel(PROBE_PREP_AUTHORITY)}")
    print(f"c8_selected_successor_surface_acceptance_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"human_decision={HUMAN_DECISION}")
    print(f"selected_surface_id={SELECTED_SURFACE_ID}")
    print(f"selected_surface_kind={SELECTED_SURFACE_KIND}")
    print(f"selected_surface_label={SELECTED_SURFACE_LABEL}")
    print("selected_successor_surface_accepted_for_bounded_probe_prep_review=true")
    print(f"authorized_future_unit_after_review={AUTHORIZED_FUTURE_UNIT}")
    print("authorized_future_unit_count_after_review=1")
    print("bounded_probe_prep_packet_created_now=false")
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
