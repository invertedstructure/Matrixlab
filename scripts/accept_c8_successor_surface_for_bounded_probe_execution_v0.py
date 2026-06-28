#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_SUCCESSOR_SURFACE_FOR_BOUNDED_PROBE_EXECUTION_V0"
TARGET_UNIT_ID = "research.c8.successor_surface.bounded_probe_execution_acceptance.v0"
MILESTONE = "C8_SUCCESSOR_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_EXECUTION"
OUTCOME = "C8_SUCCESSOR_SURFACE_ACCEPTED_FOR_ONE_BOUNDED_PROBE_EXECUTION_ONLY"
STOP_CODE = "STOP_C8_SUCCESSOR_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_EXECUTION_READY"

AUTHORIZED_FUTURE_UNIT = "EXECUTE_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_V0"

OUT_DIR = ROOT / "data/c8_successor_surface_bounded_probe_execution_acceptance_v0"
RECEIPT_DIR = ROOT / "data/c8_successor_surface_bounded_probe_execution_acceptance_v0_receipts"

REVIEW_RECEIPT = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_review_v0_receipts/c8_successor_probe_prep_packet_review_receipt_f3acc3a5.json"
REVIEW_PACKET = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_review_v0/c8_successor_surface_bounded_probe_prep_packet_review_packet_v0.json"
REVIEW_DECISION = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_review_v0/c8_successor_surface_bounded_probe_prep_packet_review_decision_v0.json"
REVIEW_AUDIT = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_review_v0/c8_successor_surface_bounded_probe_prep_packet_review_audit_v0.json"
REVIEW_REPORT = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_review_v0/c8_successor_surface_bounded_probe_prep_packet_review_report.json"

ACCEPTANCE_PACKET = OUT_DIR / "c8_successor_surface_bounded_probe_execution_acceptance_packet_v0.json"
ACCEPTANCE_DECISION = OUT_DIR / "c8_successor_surface_bounded_probe_execution_acceptance_decision_v0.json"
ACCEPTANCE_AUTHORITY = OUT_DIR / "c8_successor_surface_bounded_probe_execution_authority_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_successor_surface_bounded_probe_execution_acceptance_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_successor_surface_bounded_probe_execution_acceptance_readout_v0.json"
REPORT = OUT_DIR / "c8_successor_surface_bounded_probe_execution_acceptance_report.json"

NEGATIVE_CONTROL_KEYS = [
    "probe_execution_count",
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

def zero_counters() -> Dict[str, int]:
    return {k: 0 for k in NEGATIVE_CONTROL_KEYS}

def chk(failures: List[str], label: str, got: Any, want: Any) -> None:
    if got != want:
        failures.append(f"{label}_wrong:{got}!={want}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []
    negative_controls = zero_counters()

    sources = {
        "review_receipt": REVIEW_RECEIPT,
        "review_packet": REVIEW_PACKET,
        "review_decision": REVIEW_DECISION,
        "review_audit": REVIEW_AUDIT,
        "review_report": REVIEW_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    review_receipt = read_json(REVIEW_RECEIPT)
    review_packet = read_json(REVIEW_PACKET)
    review_decision = read_json(REVIEW_DECISION)
    review_audit = read_json(REVIEW_AUDIT)
    review_report = read_json(REVIEW_REPORT)

    summary = review_receipt.get("machine_readable_review_summary", {})

    chk(failures, "review_gate", review_receipt.get("gate"), "PASS")
    chk(failures, "review_status", review_receipt.get("status"), "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_REVIEW_PASS")
    chk(failures, "review_outcome", review_receipt.get("outcome_class"), "C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_REVIEWABLE_NOT_ACCEPTED")
    chk(failures, "review_receipt_id", review_receipt.get("receipt_id"), "c8_successor_probe_prep_packet_review_receipt_f3acc3a5")

    expected_summary = {
        "review_complete": True,
        "source_prep_receipt_id": "c8_successor_probe_prep_packet_receipt_bbb5ebc3",
        "source_prep_packet_id": "c8_successor_probe_prep_packet_74a6c209",
        "probe_id": "c8_successor_surface_reuse_authority_boundary_probe_v0",
        "probe_kind": "REUSE_AUTHORITY_BOUNDARY_PROBE",
        "selected_surface_id": "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0",
        "selected_surface_kind": "REUSE_AUTHORITY_BOUNDARY_SURFACE",
        "selected_surface_label": "C8_POST_CLOSURE_LOCAL_LOOP_REUSE_PRESSURE_SURFACE",
        "review_decision": "REVIEWABLE_NOT_ACCEPTED",
        "prep_review_class": "WELL_FORMED_BOUNDED_REUSE_AUTHORITY_PROBE_PREP_PACKET",
        "prep_packet_is_well_formed": True,
        "prep_packet_is_bounded": True,
        "probe_spec_is_typed": True,
        "human_decision_required": True,
        "accepted_for_probe_execution_now": False,
        "probe_executed_now": False,
        "new_instrument_build": False,
        "new_c8_rerun": False,
        "reusable_schema_authorized": False,
    }

    for key, want in expected_summary.items():
        chk(failures, f"summary_{key}", summary.get(key), want)

    chk(failures, "packet_review_decision", review_packet.get("review_decision"), "REVIEWABLE_NOT_ACCEPTED")
    chk(failures, "packet_human_decision_required", review_packet.get("human_decision_required"), True)
    chk(failures, "packet_accepted_for_probe_execution_now", review_packet.get("accepted_for_probe_execution_now"), False)

    authorized_now = review_packet.get("authorized_now", {})
    for key in [
        "probe_execution",
        "instrument_build",
        "cell1_build",
        "verification_probe",
        "c8_rerun",
        "missing_instrument_proposal",
        "reusable_schema",
        "research_mode",
    ]:
        chk(failures, f"prior_authorized_{key}", authorized_now.get(key), False)

    chk(failures, "decision_review_decision", review_decision.get("review_decision"), "REVIEWABLE_NOT_ACCEPTED")
    chk(failures, "decision_requires_human_decision", review_decision.get("requires_human_decision"), True)
    chk(failures, "decision_accepted_for_probe_execution", review_decision.get("accepted_for_probe_execution"), False)

    if "ACCEPT_FOR_BOUNDED_PROBE_EXECUTION" not in review_decision.get("possible_human_decisions", []):
        failures.append("accept_for_bounded_probe_execution_not_available_in_possible_human_decisions")

    operator_decision = "ACCEPT_FOR_BOUNDED_PROBE_EXECUTION"

    acceptance_decision = {
        "schema_version": "c8_successor_surface_bounded_probe_execution_acceptance_decision_v0",
        "acceptance_decision_id": None,
        "operator_decision": operator_decision,
        "source_review_receipt_id": review_receipt.get("receipt_id"),
        "source_review_packet_id": review_packet.get("review_packet_id"),
        "source_review_decision_id": review_decision.get("review_decision_id"),
        "source_prep_packet_id": summary.get("source_prep_packet_id"),
        "probe_id": summary.get("probe_id"),
        "probe_kind": summary.get("probe_kind"),
        "selected_surface_id": summary.get("selected_surface_id"),
        "selected_surface_kind": summary.get("selected_surface_kind"),
        "selected_surface_label": summary.get("selected_surface_label"),
        "accepted_for_bounded_probe_execution": True,
        "accepted_for_probe_execution_now": False,
        "probe_executed_now": False,
        "accepted_for_instrument_build": False,
        "accepted_for_cell1_build": False,
        "accepted_for_verification_probe": False,
        "accepted_for_c8_rerun": False,
        "accepted_for_missing_instrument_proposal": False,
        "accepted_for_reusable_schema": False,
        "acceptance_status": "ACCEPTED_FOR_ONE_BOUNDED_PROBE_EXECUTION_AUTHORITY_ONLY",
        "human_decision_consumed": True,
        "requires_next_bounded_execution_unit": True,
        "next_allowed_unit": AUTHORIZED_FUTURE_UNIT,
        "review_basis": {
            "prep_review_class": summary.get("prep_review_class"),
            "prep_packet_is_well_formed": summary.get("prep_packet_is_well_formed"),
            "prep_packet_is_bounded": summary.get("prep_packet_is_bounded"),
            "probe_spec_is_typed": summary.get("probe_spec_is_typed"),
        },
    }
    acceptance_decision["acceptance_decision_id"] = "c8_successor_probe_execution_acceptance_decision_" + sig8(acceptance_decision)
    write_json(ACCEPTANCE_DECISION, acceptance_decision)

    acceptance_authority = {
        "schema_version": "c8_successor_surface_bounded_probe_execution_authority_v0",
        "authority_id": None,
        "source_acceptance_decision_id": acceptance_decision["acceptance_decision_id"],
        "authority_status": "BOUNDED_PROBE_EXECUTION_AUTHORITY_CREATED",
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_execution_count": 1,
        "authorized_future_instrument_build_count": 0,
        "authorized_future_cell1_build_count": 0,
        "authorized_future_verification_probe_count": 0,
        "authorized_future_c8_rerun_count": 0,
        "authorized_future_missing_instrument_proposal_count": 0,
        "authorized_future_reusable_schema_count": 0,
        "authority_scope": {
            "may_execute_one_bounded_probe": True,
            "may_build_instrument": False,
            "may_build_cell1": False,
            "may_run_verification_probe": False,
            "may_rerun_c8": False,
            "may_create_missing_instrument_proposal": False,
            "may_authorize_reusable_schema": False,
            "may_open_research_mode": False,
        },
        "boundary_note": "Acceptance authorizes exactly one future bounded reuse-authority probe execution. It does not execute the probe in this unit and does not authorize build, rerun, proposal, or reusable schema.",
    }
    acceptance_authority["authority_id"] = "c8_successor_probe_execution_authority_" + sig8(acceptance_authority)
    write_json(ACCEPTANCE_AUTHORITY, acceptance_authority)

    acceptance_packet = {
        "schema_version": "c8_successor_surface_bounded_probe_execution_acceptance_packet_v0",
        "acceptance_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "acceptance_status": "ACCEPTED_FOR_ONE_BOUNDED_PROBE_EXECUTION_AUTHORITY_ONLY",
        "operator_decision": operator_decision,
        "source_review_receipt_id": review_receipt.get("receipt_id"),
        "source_review_packet_id": review_packet.get("review_packet_id"),
        "source_review_decision_id": review_decision.get("review_decision_id"),
        "source_prep_packet_id": summary.get("source_prep_packet_id"),
        "probe_id": summary.get("probe_id"),
        "probe_kind": summary.get("probe_kind"),
        "selected_surface_id": summary.get("selected_surface_id"),
        "selected_surface_kind": summary.get("selected_surface_kind"),
        "selected_surface_label": summary.get("selected_surface_label"),
        "acceptance_decision_ref": rel(ACCEPTANCE_DECISION),
        "acceptance_authority_ref": rel(ACCEPTANCE_AUTHORITY),
        "accepted_for_bounded_probe_execution": True,
        "accepted_for_probe_execution_now": False,
        "probe_executed_now": False,
        "accepted_for_instrument_build": False,
        "accepted_for_cell1_build": False,
        "accepted_for_verification_probe": False,
        "accepted_for_c8_rerun": False,
        "accepted_for_missing_instrument_proposal": False,
        "accepted_for_reusable_schema": False,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_execution_count": 1,
        "recommended_next_unit": AUTHORIZED_FUTURE_UNIT,
        "recommended_next_unit_status": "AUTHORIZED_FOR_ONE_BOUNDED_PROBE_EXECUTION_ONLY",
    }
    acceptance_packet["acceptance_packet_id"] = "c8_successor_probe_execution_acceptance_packet_" + sig8(acceptance_packet)
    write_json(ACCEPTANCE_PACKET, acceptance_packet)

    source_hashes_after = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    if source_hashes_before != source_hashes_after:
        negative_controls["source_artifact_mutation_count"] += 1

    nonzero = {k: v for k, v in negative_controls.items() if v != 0}
    for k, v in nonzero.items():
        failures.append(f"{k}:{v}")

    acceptance_gates = {
        "C8_PROBE_EXECUTION_ACCEPTANCE_0_REVIEW_RECEIPT_VERIFIED": review_receipt.get("gate") == "PASS",
        "C8_PROBE_EXECUTION_ACCEPTANCE_1_REVIEWABLE_NOT_ACCEPTED_SOURCE": summary.get("review_decision") == "REVIEWABLE_NOT_ACCEPTED",
        "C8_PROBE_EXECUTION_ACCEPTANCE_2_HUMAN_DECISION_REQUIRED_SOURCE": summary.get("human_decision_required") is True,
        "C8_PROBE_EXECUTION_ACCEPTANCE_3_OPERATOR_ACCEPT_DECISION_TYPED": operator_decision == "ACCEPT_FOR_BOUNDED_PROBE_EXECUTION",
        "C8_PROBE_EXECUTION_ACCEPTANCE_4_PREP_WELL_FORMED_AND_BOUNDED": summary.get("prep_packet_is_well_formed") is True and summary.get("prep_packet_is_bounded") is True,
        "C8_PROBE_EXECUTION_ACCEPTANCE_5_PROBE_SPEC_TYPED": summary.get("probe_spec_is_typed") is True and summary.get("probe_kind") == "REUSE_AUTHORITY_BOUNDARY_PROBE",
        "C8_PROBE_EXECUTION_ACCEPTANCE_6_ACCEPTED_FOR_FUTURE_EXECUTION_ONLY": acceptance_packet["accepted_for_bounded_probe_execution"] is True and acceptance_packet["probe_executed_now"] is False,
        "C8_PROBE_EXECUTION_ACCEPTANCE_7_ONE_FUTURE_EXECUTION_UNIT_ONLY": acceptance_authority["authorized_future_unit_count"] == 1 and acceptance_authority["authorized_future_probe_execution_count"] == 1,
        "C8_PROBE_EXECUTION_ACCEPTANCE_8_NO_PROBE_EXECUTION_NOW": negative_controls["probe_execution_count"] == 0,
        "C8_PROBE_EXECUTION_ACCEPTANCE_9_NO_BUILD_OR_RERUN_NOW": negative_controls["instrument_build_count"] == 0 and negative_controls["c8_rerun_count"] == 0,
        "C8_PROBE_EXECUTION_ACCEPTANCE_10_NO_REUSABLE_SCHEMA_AUTHORIZED": negative_controls["reusable_schema_authorized_count"] == 0,
        "C8_PROBE_EXECUTION_ACCEPTANCE_11_NO_RESEARCH_OR_GLOBAL_CLAIM": negative_controls["research_mode_opened_count"] == 0 and negative_controls["global_solution_claim_count"] == 0 and negative_controls["frontier_solved_claim_count"] == 0,
        "C8_PROBE_EXECUTION_ACCEPTANCE_12_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_PROBE_EXECUTION_ACCEPTANCE_13_BAD_COUNTERS_ZERO": not bool(nonzero),
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_PASS" if gate == "PASS" else "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_FAILED"

    boundary_audit = {
        "schema_version": "c8_successor_surface_bounded_probe_execution_acceptance_boundary_audit_v0",
        "boundary_audit_id": None,
        "gate": gate,
        "source_prep_packet_id": summary.get("source_prep_packet_id"),
        "probe_id": summary.get("probe_id"),
        "probe_kind": summary.get("probe_kind"),
        "accepted_for_future_bounded_probe_execution": True,
        "authority_boundary": {
            "may_execute_one_bounded_probe_in_future_unit": True,
            "may_execute_probe_now": False,
            "may_build_instrument_now": False,
            "may_rerun_c8_now": False,
            "may_create_missing_instrument_proposal_now": False,
            "may_authorize_reusable_schema_now": False,
            "may_open_research_mode_now": False,
        },
        "negative_controls": negative_controls,
        "acceptance_gate_results": acceptance_gates,
        "failures": failures,
        "warnings": warnings,
    }
    boundary_audit["boundary_audit_id"] = "c8_successor_probe_execution_acceptance_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    readout = {
        "schema_version": "c8_successor_surface_bounded_probe_execution_acceptance_readout_v0",
        "title": "C8 successor surface bounded probe-execution acceptance readout",
        "status": status,
        "outcome_class": outcome,
        "operator_decision": operator_decision,
        "source_prep_packet_id": summary.get("source_prep_packet_id"),
        "probe_id": summary.get("probe_id"),
        "probe_kind": summary.get("probe_kind"),
        "accepted_for_bounded_probe_execution": True,
        "probe_executed_now": False,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized_now": False,
        "summary": "Human acceptance authorizes exactly one future bounded reuse-authority probe execution. This unit does not execute the probe.",
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_successor_surface_bounded_probe_execution_acceptance_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "acceptance_packet_ref": rel(ACCEPTANCE_PACKET),
        "acceptance_decision_ref": rel(ACCEPTANCE_DECISION),
        "acceptance_authority_ref": rel(ACCEPTANCE_AUTHORITY),
        "boundary_audit_ref": rel(BOUNDARY_AUDIT),
        "source_review_receipt_id": review_receipt.get("receipt_id"),
        "source_review_packet_id": review_packet.get("review_packet_id"),
        "source_review_decision_id": review_decision.get("review_decision_id"),
        "source_prep_packet_id": summary.get("source_prep_packet_id"),
        "probe_id": summary.get("probe_id"),
        "probe_kind": summary.get("probe_kind"),
        "selected_surface_id": summary.get("selected_surface_id"),
        "operator_decision": operator_decision,
        "accepted_for_bounded_probe_execution": True,
        "probe_executed_now": False,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
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
        "schema_version": "c8_successor_surface_bounded_probe_execution_acceptance_receipt_v0",
        "receipt_type": "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_refs": {
            "review_receipt_ref": rel(REVIEW_RECEIPT),
            "review_packet_ref": rel(REVIEW_PACKET),
            "review_decision_ref": rel(REVIEW_DECISION),
            "review_audit_ref": rel(REVIEW_AUDIT),
            "review_report_ref": rel(REVIEW_REPORT),
        },
        "machine_readable_acceptance_summary": {
            "acceptance_complete": gate == "PASS",
            "operator_decision": operator_decision,
            "source_review_receipt_id": review_receipt.get("receipt_id"),
            "source_review_packet_id": review_packet.get("review_packet_id"),
            "source_review_decision_id": review_decision.get("review_decision_id"),
            "source_prep_packet_id": summary.get("source_prep_packet_id"),
            "probe_id": summary.get("probe_id"),
            "probe_kind": summary.get("probe_kind"),
            "selected_surface_id": summary.get("selected_surface_id"),
            "selected_surface_kind": summary.get("selected_surface_kind"),
            "selected_surface_label": summary.get("selected_surface_label"),
            "accepted_for_bounded_probe_execution": True,
            "accepted_for_probe_execution_now": False,
            "probe_executed_now": False,
            "accepted_for_instrument_build": False,
            "accepted_for_cell1_build": False,
            "accepted_for_verification_probe": False,
            "accepted_for_c8_rerun": False,
            "accepted_for_missing_instrument_proposal": False,
            "accepted_for_reusable_schema": False,
            "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
            "authorized_future_unit_count": 1,
            "authorized_future_probe_execution_count": 1,
            "new_instrument_build": False,
            "new_cell1_build": False,
            "new_verification_probe": False,
            "new_c8_rerun": False,
            "new_missing_instrument_proposal": False,
            "research_mode_opened": False,
            "general_cell1_authority": False,
            "reusable_schema_authorized": False,
            "global_solution_claim": False,
            "frontier_solved_claim": False,
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
            "bad_counters_zero": not bool(nonzero),
            "next_command_goal": None,
        },
        "acceptance_gate_results": acceptance_gates,
        "negative_controls": negative_controls,
        "source_artifact_immutability": {
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
        },
        "output_artifacts": {
            "acceptance_packet": rel(ACCEPTANCE_PACKET),
            "acceptance_decision": rel(ACCEPTANCE_DECISION),
            "acceptance_authority": rel(ACCEPTANCE_AUTHORITY),
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

    receipt["receipt_id"] = "c8_successor_probe_execution_acceptance_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"acceptance_receipt_id={receipt['receipt_id']}")
    print(f"acceptance_receipt_path={rel(receipt_path)}")
    print(f"acceptance_packet_path={rel(ACCEPTANCE_PACKET)}")
    print(f"acceptance_decision_path={rel(ACCEPTANCE_DECISION)}")
    print(f"acceptance_authority_path={rel(ACCEPTANCE_AUTHORITY)}")
    print(f"operator_decision={operator_decision}")
    print(f"source_prep_packet_id={summary.get('source_prep_packet_id')}")
    print(f"probe_id={summary.get('probe_id')}")
    print(f"probe_kind={summary.get('probe_kind')}")
    print("accepted_for_bounded_probe_execution=true")
    print("accepted_for_probe_execution_now=false")
    print("probe_executed_now=false")
    print(f"authorized_future_unit={AUTHORIZED_FUTURE_UNIT}")
    print("authorized_future_unit_count=1")
    print("authorized_future_probe_execution_count=1")
    print("new_instrument_build=false")
    print("new_c8_rerun=false")
    print("reusable_schema_authorized=false")
    print(f"acceptance_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
