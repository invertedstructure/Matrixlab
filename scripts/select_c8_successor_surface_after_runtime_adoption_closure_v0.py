#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "SELECT_C8_SUCCESSOR_SURFACE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.successor_surface_selection.after_runtime_adoption_closure.v0"
MILESTONE = "C8_SUCCESSOR_SURFACE_SELECTED_AFTER_RUNTIME_ADOPTION_CLOSURE"
OUTCOME = "C8_SUCCESSOR_SURFACE_SELECTION_READY_FOR_REVIEW"
STOP_CODE = "STOP_C8_SUCCESSOR_SURFACE_SELECTION_READY_FOR_REVIEW"

SOURCE_ACCEPTANCE_RECEIPT_ID = "c8_return_to_surface_selection_acceptance_receipt_15807948"
SOURCE_ACCEPTANCE_DECISION_ID = "c8_return_to_surface_selection_acceptance_decision_43089b84"
SOURCE_ACCEPTANCE_PACKET_ID = "c8_return_to_surface_selection_acceptance_packet_f7aaaa5b"
SOURCE_AUTHORITY_ID = "c8_successor_surface_selection_authority_984254c6"
SOURCE_BOUNDARY_ID = "c8_return_to_surface_selection_acceptance_boundary_ec1b4c36"

AUTHORIZED_UNIT = "SELECT_C8_SUCCESSOR_SURFACE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

CLOSED_SURFACE_ID = "c8_successor_surface_runtime_adoption_after_reentry_v0"
CLOSED_SURFACE_KIND = "RUNTIME_ADOPTION_SURFACE"
CLOSED_SURFACE_LABEL = "C8_RUNTIME_ADOPTION_AFTER_REUSE_AUTHORITY_CLOSURE_SURFACE"
CLOSED_PROBE_ID = "c8_runtime_adoption_surface_bounded_probe_after_reentry_v0"
CLOSED_PROBE_KIND = "RUNTIME_ADOPTION_BOUNDARY_PROBE"
CLOSED_PROBE_OUTPUT_CLASS = "RUNTIME_ADOPTION_BOUNDARY_PROBE_OBSERVED_NO_DEFECTS"

SELECTED_SURFACE_ID = "c8_successor_surface_unit_feedback_hardening_after_runtime_adoption_closure_v0"
SELECTED_SURFACE_KIND = "UNIT_FEEDBACK_HARDENING_SURFACE"
SELECTED_SURFACE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_AFTER_RUNTIME_ADOPTION_CLOSURE_SURFACE"
SELECTED_SURFACE_QUESTION = (
    "After runtime-adoption closure and successor-surface selection authority activation, "
    "what is the smallest surface that can test whether typed stops and failed units emit useful "
    "diagnostic feedback—why it failed, where it failed, relative to what object/source surface/"
    "authority boundary/missing capability, and what exact refinement would allow progress—"
    "without authorizing probe prep, probe execution, build, C8 rerun, or reusable schema promotion?"
)

OUT_DIR = ROOT / "data/c8_successor_surface_selection_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_successor_surface_selection_after_runtime_adoption_closure_v0_receipts"

ACCEPTANCE_RECEIPT = ROOT / "data/c8_return_to_surface_selection_acceptance_after_runtime_adoption_closure_v0_receipts/c8_return_to_surface_selection_acceptance_receipt_15807948.json"
ACCEPTANCE_DECISION = ROOT / "data/c8_return_to_surface_selection_acceptance_after_runtime_adoption_closure_v0/c8_return_to_surface_selection_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = ROOT / "data/c8_return_to_surface_selection_acceptance_after_runtime_adoption_closure_v0/c8_return_to_surface_selection_acceptance_packet_v0.json"
AUTHORITY = ROOT / "data/c8_return_to_surface_selection_acceptance_after_runtime_adoption_closure_v0/c8_successor_surface_selection_authority_v0.json"
BOUNDARY_AUDIT = ROOT / "data/c8_return_to_surface_selection_acceptance_after_runtime_adoption_closure_v0/c8_return_to_surface_selection_acceptance_boundary_audit_v0.json"
ACCEPTANCE_REPORT = ROOT / "data/c8_return_to_surface_selection_acceptance_after_runtime_adoption_closure_v0/c8_return_to_surface_selection_acceptance_report.json"

SELECTION_PACKET = OUT_DIR / "c8_successor_surface_selection_packet_v0.json"
SELECTION_AUDIT = OUT_DIR / "c8_successor_surface_selection_boundary_audit_v0.json"
SELECTION_READOUT = OUT_DIR / "c8_successor_surface_selection_readout_v0.json"
SELECTION_REPORT = OUT_DIR / "c8_successor_surface_selection_report.json"

FORBIDDEN_COUNTER_KEYS = [
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
        "acceptance_receipt": ACCEPTANCE_RECEIPT,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_packet": ACCEPTANCE_PACKET,
        "authority": AUTHORITY,
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
    acceptance_decision = read_json(ACCEPTANCE_DECISION)
    acceptance_packet = read_json(ACCEPTANCE_PACKET)
    authority = read_json(AUTHORITY)
    boundary = read_json(BOUNDARY_AUDIT)
    acceptance_report = read_json(ACCEPTANCE_REPORT)
    summary = acceptance_receipt.get("machine_readable_return_to_surface_selection_acceptance_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_RETURN_TO_SURFACE_SELECTION_ACCEPTANCE_PASS",
        "outcome_class": "C8_RETURN_TO_SURFACE_SELECTION_ACCEPTED_SUCCESSOR_SURFACE_SELECTION_AUTHORIZED_FOR_REVIEW",
        "receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
    }
    for key, want in expected_receipt.items():
        chk(failures, f"acceptance_receipt_{key}", acceptance_receipt.get(key), want)

    expected_summary = {
        "return_to_surface_selection_acceptance_complete": True,
        "human_decision": "ACCEPT_RETURN_TO_SURFACE_SELECTION_PACKET",
        "closed_surface_id": CLOSED_SURFACE_ID,
        "closed_surface_kind": CLOSED_SURFACE_KIND,
        "closed_surface_label": CLOSED_SURFACE_LABEL,
        "closed_probe_id": CLOSED_PROBE_ID,
        "closed_probe_kind": CLOSED_PROBE_KIND,
        "closed_probe_output_class": CLOSED_PROBE_OUTPUT_CLASS,
        "successor_surface_selection_authorized_after_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "surface_selection_packet_created_now": False,
        "surface_selected_now": False,
        "successor_surface_accepted_now": False,
        "probe_prep_created_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized": False,
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
    }
    for key, want in expected_summary.items():
        chk(failures, f"acceptance_summary_{key}", summary.get(key), want)

    expected_ids = {
        "decision_id": (acceptance_decision.get("c8_return_to_surface_selection_acceptance_decision_id"), SOURCE_ACCEPTANCE_DECISION_ID),
        "packet_id": (acceptance_packet.get("c8_return_to_surface_selection_acceptance_packet_id"), SOURCE_ACCEPTANCE_PACKET_ID),
        "authority_id": (authority.get("c8_successor_surface_selection_authority_id"), SOURCE_AUTHORITY_ID),
        "boundary_id": (boundary.get("c8_return_to_surface_selection_acceptance_boundary_audit_id"), SOURCE_BOUNDARY_ID),
    }
    for label, (got, want) in expected_ids.items():
        if got != want:
            failures.append(f"{label}_wrong:{got}!={want}")

    if authority.get("authorized_future_unit") != AUTHORIZED_UNIT:
        failures.append(f"authority_future_unit_wrong:{authority.get('authorized_future_unit')}")
    if authority.get("authorized_future_unit_count") != 1:
        failures.append(f"authority_future_unit_count_wrong:{authority.get('authorized_future_unit_count')}")
    if authority.get("authority_status") != "ACTIVE_AFTER_REVIEW_AND_COMMIT":
        failures.append(f"authority_status_wrong:{authority.get('authority_status')}")

    scope = authority.get("authority_scope", {})
    if scope.get("may_create_successor_surface_selection_packet") is not True:
        failures.append("authority_scope_may_create_successor_surface_selection_packet_not_true")
    if scope.get("may_select_surface_inside_future_unit") is not True:
        failures.append("authority_scope_may_select_surface_inside_future_unit_not_true")
    for forbidden_scope_key in [
        "may_accept_successor_surface_now",
        "may_create_probe_prep_now",
        "may_authorize_probe_execution_now",
        "may_execute_probe_now",
        "may_build_now",
        "may_rerun_c8_now",
        "may_promote_schema_now",
    ]:
        if scope.get(forbidden_scope_key) is not False:
            failures.append(f"authority_scope_{forbidden_scope_key}_wrong:{scope.get(forbidden_scope_key)}")

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

    selection_packet = {
        "schema_version": "c8_successor_surface_selection_packet_v0",
        "c8_successor_surface_selection_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "selection_status": "SUCCESSOR_SURFACE_SELECTED_READY_FOR_REVIEW",
        "authorized_unit_consumed": AUTHORIZED_UNIT,
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
        "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_successor_surface_selection_authority_id": SOURCE_AUTHORITY_ID,
        "source_acceptance_boundary_id": SOURCE_BOUNDARY_ID,
        "closed_surface_id": CLOSED_SURFACE_ID,
        "closed_surface_kind": CLOSED_SURFACE_KIND,
        "closed_surface_label": CLOSED_SURFACE_LABEL,
        "closed_probe_id": CLOSED_PROBE_ID,
        "closed_probe_kind": CLOSED_PROBE_KIND,
        "closed_probe_output_class": CLOSED_PROBE_OUTPUT_CLASS,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_question": SELECTED_SURFACE_QUESTION,
        "selection_reason": [
            "runtime-adoption bounded probe closed with no defects",
            "typed halts were observed, so feedback quality is now the smallest useful surface",
            "failure status and useful diagnostic feedback remain distinct",
        ],
        "surface_selection_packet_created_now": True,
        "surface_selected_now": True,
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
        "recommended_review_unit": "REVIEW_C8_SUCCESSOR_SURFACE_SELECTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "recommended_human_decision": "ACCEPT_SELECTED_SUCCESSOR_SURFACE_FOR_BOUNDED_PROBE_PREP_REVIEW",
    }
    selection_packet["c8_successor_surface_selection_packet_id"] = "c8_successor_surface_selection_packet_" + sig8(selection_packet)
    write_json(SELECTION_PACKET, selection_packet)

    selection_audit = {
        "schema_version": "c8_successor_surface_selection_boundary_audit_v0",
        "c8_successor_surface_selection_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_selection_packet_id": selection_packet["c8_successor_surface_selection_packet_id"],
        "source_authority_id": SOURCE_AUTHORITY_ID,
        "authorized_unit_consumed": AUTHORIZED_UNIT,
        "allowed_now": {
            "create_successor_surface_selection_packet": True,
            "select_surface_inside_authorized_unit": True,
            "present_selected_surface_for_review": True,
        },
        "not_allowed_now": {
            "accept_successor_surface": True,
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
    selection_audit["c8_successor_surface_selection_boundary_audit_id"] = "c8_successor_surface_selection_boundary_" + sig8(selection_audit)
    write_json(SELECTION_AUDIT, selection_audit)

    gate_results = {
        "SUCCESSOR_SELECTION_0_SOURCE_ACCEPTANCE_RECEIPT_PASS": acceptance_receipt.get("gate") == "PASS",
        "SUCCESSOR_SELECTION_1_AUTHORITY_PRESENT_AND_ACTIVE": authority.get("authority_status") == "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "SUCCESSOR_SELECTION_2_AUTHORIZED_UNIT_MATCH": authority.get("authorized_future_unit") == AUTHORIZED_UNIT,
        "SUCCESSOR_SELECTION_3_SURFACE_SELECTION_ALLOWED": scope.get("may_create_successor_surface_selection_packet") is True and scope.get("may_select_surface_inside_future_unit") is True,
        "SUCCESSOR_SELECTION_4_SELECTED_SURFACE_TYPED": bool(selection_packet["selected_surface_id"] and selection_packet["selected_surface_kind"] and selection_packet["selected_surface_question"]),
        "SUCCESSOR_SELECTION_5_NO_SUCCESSOR_ACCEPTANCE_NOW": selection_packet["successor_surface_accepted_now"] is False,
        "SUCCESSOR_SELECTION_6_NO_PROBE_PREP_OR_EXECUTION_NOW": selection_packet["probe_prep_created_now"] is False and selection_packet["probe_execution_authorized_now"] is False and selection_packet["probe_executed_now"] is False,
        "SUCCESSOR_SELECTION_7_NO_BUILD_RERUN_SCHEMA": selection_packet["instrument_build_authorized_now"] is False and selection_packet["c8_rerun_authorized_now"] is False and selection_packet["reusable_schema_authorized_now"] is False,
        "SUCCESSOR_SELECTION_8_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "SUCCESSOR_SELECTION_9_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "SUCCESSOR_SELECTION_10_REQUIRES_REVIEW": selection_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"successor_selection_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_SUCCESSOR_SURFACE_SELECTION_PASS" if gate == "PASS" else "TYPED_C8_SUCCESSOR_SURFACE_SELECTION_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_SUCCESSOR_SURFACE_SELECTION_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_SUCCESSOR_SURFACE_SELECTION_FAILED"

    readout = {
        "schema_version": "c8_successor_surface_selection_readout_v0",
        "title": "C8 successor surface selection after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "closed_surface_id": CLOSED_SURFACE_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "surface_selected_now": True,
        "successor_surface_accepted_now": False,
        "probe_prep_created_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": selection_packet["recommended_review_unit"],
        "terminal_stop_code": terminal_stop,
    }
    write_json(SELECTION_READOUT, readout)

    report = {
        "schema_version": "c8_successor_surface_selection_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_authority_id": SOURCE_AUTHORITY_ID,
        "closed_surface_id": CLOSED_SURFACE_ID,
        "closed_surface_kind": CLOSED_SURFACE_KIND,
        "closed_surface_label": CLOSED_SURFACE_LABEL,
        "closed_probe_id": CLOSED_PROBE_ID,
        "closed_probe_kind": CLOSED_PROBE_KIND,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_question": SELECTED_SURFACE_QUESTION,
        "surface_selection_packet_created_now": True,
        "surface_selected_now": True,
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
        "recommended_review_unit": selection_packet["recommended_review_unit"],
        "recommended_human_decision": selection_packet["recommended_human_decision"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(SELECTION_REPORT, report)

    receipt = {
        "schema_version": "c8_successor_surface_selection_receipt_v0",
        "receipt_type": "TYPED_C8_SUCCESSOR_SURFACE_SELECTION_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_successor_surface_selection_summary": {
            "successor_surface_selection_complete": gate == "PASS",
            "authorized_unit_consumed": AUTHORIZED_UNIT,
            "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
            "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
            "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
            "source_successor_surface_selection_authority_id": SOURCE_AUTHORITY_ID,
            "source_acceptance_boundary_id": SOURCE_BOUNDARY_ID,
            "closed_surface_id": CLOSED_SURFACE_ID,
            "closed_surface_kind": CLOSED_SURFACE_KIND,
            "closed_surface_label": CLOSED_SURFACE_LABEL,
            "closed_probe_id": CLOSED_PROBE_ID,
            "closed_probe_kind": CLOSED_PROBE_KIND,
            "closed_probe_output_class": CLOSED_PROBE_OUTPUT_CLASS,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "selected_surface_question": SELECTED_SURFACE_QUESTION,
            "surface_selection_packet_created_now": True,
            "surface_selected_now": True,
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
            "recommended_review_unit": selection_packet["recommended_review_unit"],
            "recommended_human_decision": selection_packet["recommended_human_decision"],
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
            "selection_packet": rel(SELECTION_PACKET),
            "selection_boundary_audit": rel(SELECTION_AUDIT),
            "readout": rel(SELECTION_READOUT),
            "report": rel(SELECTION_REPORT),
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
    print(f"c8_successor_surface_selection_receipt_id={receipt['receipt_id']}")
    print(f"c8_successor_surface_selection_receipt_path={rel(receipt_path)}")
    print(f"c8_successor_surface_selection_packet_path={rel(SELECTION_PACKET)}")
    print(f"c8_successor_surface_selection_boundary_path={rel(SELECTION_AUDIT)}")
    print(f"selected_surface_id={SELECTED_SURFACE_ID}")
    print(f"selected_surface_kind={SELECTED_SURFACE_KIND}")
    print(f"selected_surface_label={SELECTED_SURFACE_LABEL}")
    print("surface_selection_packet_created_now=true")
    print("surface_selected_now=true")
    print("successor_surface_accepted_now=false")
    print("probe_prep_created_now=false")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={selection_packet['recommended_review_unit']}")
    print(f"recommended_human_decision={selection_packet['recommended_human_decision']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
