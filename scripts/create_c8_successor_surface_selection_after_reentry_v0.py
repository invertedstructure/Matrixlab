#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_SUCCESSOR_SURFACE_SELECTION_AFTER_REENTRY_V0"
TARGET_UNIT_ID = "research.c8.successor_surface.selection.after_reentry.v0"
MILESTONE = "C8_SUCCESSOR_SURFACE_SELECTION_CREATED_AFTER_REENTRY"
OUTCOME = "C8_SUCCESSOR_SURFACE_SELECTION_REVIEWABLE_NOT_ACCEPTED"
STOP_CODE = "STOP_C8_SUCCESSOR_SURFACE_SELECTION_AFTER_REENTRY_READY_FOR_REVIEW"

SOURCE_ACCEPTANCE_RECEIPT_ID = "c8_return_to_selection_acceptance_receipt_0144408e"
SOURCE_ACCEPTANCE_PACKET_ID = "c8_return_to_selection_acceptance_packet_6b51e7bf"
SOURCE_ACCEPTANCE_DECISION_ID = "c8_return_to_selection_acceptance_decision_581d0092"
SOURCE_REENTRY_BOUNDARY_ID = "c8_surface_selection_reentry_boundary_e02a5882"

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

OUT_DIR = ROOT / "data/c8_successor_surface_selection_after_reentry_v0"
RECEIPT_DIR = ROOT / "data/c8_successor_surface_selection_after_reentry_v0_receipts"

ACCEPTANCE_RECEIPT = ROOT / "data/c8_return_to_surface_selection_acceptance_after_reuse_authority_closure_v0_receipts/c8_return_to_selection_acceptance_receipt_0144408e.json"
ACCEPTANCE_PACKET = ROOT / "data/c8_return_to_surface_selection_acceptance_after_reuse_authority_closure_v0/c8_return_to_surface_selection_acceptance_packet_v0.json"
ACCEPTANCE_DECISION = ROOT / "data/c8_return_to_surface_selection_acceptance_after_reuse_authority_closure_v0/c8_return_to_surface_selection_acceptance_decision_v0.json"
REENTRY_BOUNDARY = ROOT / "data/c8_return_to_surface_selection_acceptance_after_reuse_authority_closure_v0/c8_surface_selection_reentry_boundary_v0.json"
ACCEPTANCE_REPORT = ROOT / "data/c8_return_to_surface_selection_acceptance_after_reuse_authority_closure_v0/c8_return_to_surface_selection_acceptance_report.json"

SELECTION_PACKET = OUT_DIR / "c8_successor_surface_selection_packet_v0.json"
SELECTION_DECISION = OUT_DIR / "c8_successor_surface_selection_decision_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_successor_surface_selection_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_successor_surface_selection_readout_v0.json"
REPORT = OUT_DIR / "c8_successor_surface_selection_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "selected_surface_accepted_count",
    "surface_activated_count",
    "probe_prep_authorized_count",
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
        "reentry_boundary": REENTRY_BOUNDARY,
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
    reentry_boundary = read_json(REENTRY_BOUNDARY)
    acceptance_report = read_json(ACCEPTANCE_REPORT)
    summary = acceptance_receipt.get("machine_readable_acceptance_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_PASS",
        "outcome_class": "C8_RETURN_TO_SURFACE_SELECTION_ACCEPTED_FOR_REENTRY_REVIEW",
        "receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
    }

    for key, want in expected_receipt.items():
        chk(failures, f"acceptance_receipt_{key}", acceptance_receipt.get(key), want)

    expected_summary = {
        "return_to_selection_acceptance_complete": True,
        "human_decision": "ACCEPT_RETURN_TO_SURFACE_SELECTION",
        "source_return_to_selection_receipt_id": "c8_return_to_surface_selection_receipt_e1b23af9",
        "source_return_to_selection_packet_id": "c8_return_to_surface_selection_packet_497f97dd",
        "source_return_to_selection_boundary_id": "c8_return_to_surface_selection_boundary_6b7e2995",
        "source_closure_acceptance_receipt_id": "c8_successor_reuse_authority_probe_closure_acceptance_receipt_2023bce5",
        "source_final_closure_id": "c8_successor_reuse_authority_probe_final_closure_e8a1bd0e",
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
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
        "next_command_goal": None,
    }

    for key, want in expected_summary.items():
        chk(failures, f"acceptance_summary_{key}", summary.get(key), want)

    chk(failures, "acceptance_packet_id", acceptance_packet.get("return_to_selection_acceptance_packet_id"), SOURCE_ACCEPTANCE_PACKET_ID)
    chk(failures, "acceptance_decision_id", acceptance_decision.get("return_to_selection_acceptance_decision_id"), SOURCE_ACCEPTANCE_DECISION_ID)
    chk(failures, "reentry_boundary_id", reentry_boundary.get("surface_selection_reentry_boundary_id"), SOURCE_REENTRY_BOUNDARY_ID)

    source_hashes_after = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    if source_hashes_before != source_hashes_after:
        forbidden_counters["source_artifact_mutation_count"] += 1

    candidate_surfaces = [
        {
            "surface_id": SELECTED_SURFACE_ID,
            "surface_kind": SELECTED_SURFACE_KIND,
            "surface_label": SELECTED_SURFACE_LABEL,
            "surface_question": SELECTED_SURFACE_QUESTION,
            "selection_rank": 1,
            "selection_reason": (
                "Runtime adoption is the next smallest lawful surface after the reuse-authority boundary held: "
                "it can expose typed runtime halts and failure modes without pre-authorizing any build, probe, or rerun."
            ),
        },
        {
            "surface_id": "c8_successor_surface_unit_feedback_hardening_after_reentry_v0",
            "surface_kind": "UNIT_FEEDBACK_HARDENING_SURFACE",
            "surface_label": "C8_UNIT_FEEDBACK_HARDENING_AFTER_REENTRY_SURFACE",
            "surface_question": (
                "What minimum feedback-hardening surface would make failed units report why, where, relative to what object, "
                "and what refinement would allow progress?"
            ),
            "selection_rank": 2,
            "selection_reason": "Important but secondary; best opened from concrete runtime-observed failures rather than before runtime reentry.",
        },
        {
            "surface_id": "c8_successor_surface_receipt_projection_hygiene_after_reentry_v0",
            "surface_kind": "RECEIPT_PROJECTION_HYGIENE_SURFACE",
            "surface_label": "C8_RECEIPT_PROJECTION_HYGIENE_AFTER_REENTRY_SURFACE",
            "surface_question": (
                "What minimum projection-hygiene surface would reduce report/readout mismatch without expanding authority?"
            ),
            "selection_rank": 3,
            "selection_reason": "Relevant due the repaired report projection bug, but narrower than the runtime-adoption surface.",
        },
    ]

    local_nonzero = {k: v for k, v in forbidden_counters.items() if v != 0}
    for k, v in local_nonzero.items():
        failures.append(f"{k}:{v}")

    selection_decision = {
        "schema_version": "c8_successor_surface_selection_decision_v0",
        "surface_selection_decision_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "source_return_to_selection_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_return_to_selection_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_return_to_selection_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
        "source_surface_selection_reentry_boundary_id": SOURCE_REENTRY_BOUNDARY_ID,
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "selection_basis": "SURFACE_SELECTION_REENTRY_ACCEPTED_AFTER_REUSE_AUTHORITY_CLOSURE",
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_question": SELECTED_SURFACE_QUESTION,
        "selected_surface_status": "REVIEWABLE_NOT_ACCEPTED",
        "selected_surface_active": False,
        "selected_surface_accepted_now": False,
        "probe_prep_authorized_now": False,
        "probe_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "candidate_surfaces": candidate_surfaces,
        "recommended_next_decision_options": [
            "ACCEPT_SURFACE_FOR_BOUNDED_PROBE_PREP",
            "REJECT_SELECTED_SURFACE",
            "REQUEST_NARROWER_SURFACE_SELECTION",
        ],
        "requires_review": True,
    }
    selection_decision["surface_selection_decision_id"] = "c8_successor_surface_selection_decision_" + sig8(selection_decision)
    write_json(SELECTION_DECISION, selection_decision)

    selection_packet = {
        "schema_version": "c8_successor_surface_selection_packet_v0",
        "surface_selection_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "packet_status": "SELECTED_SURFACE_REVIEWABLE_NOT_ACCEPTED",
        "source_return_to_selection_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_return_to_selection_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_surface_selection_decision_id": selection_decision["surface_selection_decision_id"],
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "previous_surface_closed": True,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_question": SELECTED_SURFACE_QUESTION,
        "selected_surface_status": "REVIEWABLE_NOT_ACCEPTED",
        "selected_surface_active": False,
        "selected_surface_accepted_now": False,
        "probe_prep_authorized_now": False,
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
        "recommended_review_unit": "REVIEW_C8_SUCCESSOR_SURFACE_SELECTION_AFTER_REENTRY_V0",
        "recommended_next_decision_options": selection_decision["recommended_next_decision_options"],
    }
    selection_packet["surface_selection_packet_id"] = "c8_successor_surface_selection_packet_" + sig8(selection_packet)
    write_json(SELECTION_PACKET, selection_packet)

    boundary_audit = {
        "schema_version": "c8_successor_surface_selection_boundary_audit_v0",
        "surface_selection_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_surface_selection_packet_id": selection_packet["surface_selection_packet_id"],
        "source_surface_selection_decision_id": selection_decision["surface_selection_decision_id"],
        "allowed_now": {
            "select_surface_for_review": True,
            "record_candidate_surface_set": True,
        },
        "not_allowed_now": {
            "accept_selected_surface": True,
            "activate_selected_surface": True,
            "authorize_probe_prep": True,
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
    boundary_audit["surface_selection_boundary_audit_id"] = "c8_successor_surface_selection_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    gate_results = {
        "SURFACE_SELECTION_0_SOURCE_ACCEPTANCE_RECEIPT_PASS": acceptance_receipt.get("gate") == "PASS",
        "SURFACE_SELECTION_1_REENTRY_ACCEPTED": summary.get("surface_selection_reentry_accepted") is True,
        "SURFACE_SELECTION_2_REENTRY_READY_AFTER_REVIEW": summary.get("surface_selection_reentry_ready_after_review") is True,
        "SURFACE_SELECTION_3_PREVIOUS_SURFACE_CLOSED": summary.get("previous_surface_closed") is True,
        "SURFACE_SELECTION_4_SELECTED_SURFACE_REVIEWABLE_ONLY": selection_packet["selected_surface_status"] == "REVIEWABLE_NOT_ACCEPTED" and selection_packet["selected_surface_active"] is False,
        "SURFACE_SELECTION_5_NO_ACCEPTANCE_OR_ACTIVATION": selection_packet["selected_surface_accepted_now"] is False and selection_packet["selected_surface_active"] is False,
        "SURFACE_SELECTION_6_NO_PROBE_BUILD_RERUN_SCHEMA": selection_packet["probe_prep_authorized_now"] is False and selection_packet["probe_authorized_now"] is False and selection_packet["instrument_build_authorized_now"] is False and selection_packet["c8_rerun_authorized_now"] is False and selection_packet["reusable_schema_authorized_now"] is False,
        "SURFACE_SELECTION_7_NO_GLOBAL_OR_FRONTIER_CLAIM": selection_packet["global_solution_claim"] is False and selection_packet["frontier_solved_claim"] is False,
        "SURFACE_SELECTION_8_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "SURFACE_SELECTION_9_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "SURFACE_SELECTION_10_RESULT_REQUIRES_REVIEW": selection_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"surface_selection_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_SUCCESSOR_SURFACE_SELECTION_AFTER_REENTRY_PASS" if gate == "PASS" else "TYPED_C8_SUCCESSOR_SURFACE_SELECTION_AFTER_REENTRY_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_SUCCESSOR_SURFACE_SELECTION_AFTER_REENTRY_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_SUCCESSOR_SURFACE_SELECTION_AFTER_REENTRY_FAILED"

    readout = {
        "schema_version": "c8_successor_surface_selection_readout_v0",
        "title": "C8 successor surface selection after reentry",
        "status": status,
        "outcome_class": outcome,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_status": "REVIEWABLE_NOT_ACCEPTED",
        "selected_surface_active": False,
        "selected_surface_accepted_now": False,
        "probe_prep_authorized_now": False,
        "probe_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": selection_packet["recommended_review_unit"],
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_successor_surface_selection_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_return_to_selection_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_return_to_selection_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_question": SELECTED_SURFACE_QUESTION,
        "selected_surface_status": "REVIEWABLE_NOT_ACCEPTED",
        "selected_surface_active": False,
        "selected_surface_accepted_now": False,
        "probe_prep_authorized_now": False,
        "probe_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "requires_review": True,
        "recommended_review_unit": selection_packet["recommended_review_unit"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_successor_surface_selection_after_reentry_receipt_v0",
        "receipt_type": "TYPED_C8_SUCCESSOR_SURFACE_SELECTION_AFTER_REENTRY_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_selection_summary": {
            "surface_selection_after_reentry_complete": gate == "PASS",
            "source_return_to_selection_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
            "source_return_to_selection_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
            "source_return_to_selection_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
            "source_surface_selection_reentry_boundary_id": SOURCE_REENTRY_BOUNDARY_ID,
            "previous_surface_id": PREVIOUS_SURFACE_ID,
            "previous_surface_kind": PREVIOUS_SURFACE_KIND,
            "previous_surface_label": PREVIOUS_SURFACE_LABEL,
            "previous_surface_closed": True,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "selected_surface_question": SELECTED_SURFACE_QUESTION,
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
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
            "forbidden_counters_zero": not bool(local_nonzero),
            "requires_review": True,
            "recommended_review_unit": selection_packet["recommended_review_unit"],
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
            "selection_decision": rel(SELECTION_DECISION),
            "selection_packet": rel(SELECTION_PACKET),
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

    receipt["receipt_id"] = "c8_successor_surface_selection_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"successor_surface_selection_receipt_id={receipt['receipt_id']}")
    print(f"successor_surface_selection_receipt_path={rel(receipt_path)}")
    print(f"successor_surface_selection_packet_path={rel(SELECTION_PACKET)}")
    print(f"successor_surface_selection_decision_path={rel(SELECTION_DECISION)}")
    print(f"successor_surface_selection_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"selected_surface_id={SELECTED_SURFACE_ID}")
    print(f"selected_surface_kind={SELECTED_SURFACE_KIND}")
    print(f"selected_surface_label={SELECTED_SURFACE_LABEL}")
    print("selected_surface_status=REVIEWABLE_NOT_ACCEPTED")
    print("selected_surface_active=false")
    print("selected_surface_accepted_now=false")
    print("probe_prep_authorized_now=false")
    print("probe_authorized_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={selection_packet['recommended_review_unit']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
