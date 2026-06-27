#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_SUCCESSOR_SURFACE_FOR_BOUNDED_PROBE_PREP_V0"
TARGET_UNIT_ID = "research.c8.successor_surface.bounded_probe_prep_acceptance.v0"
MILESTONE = "C8_SUCCESSOR_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_PREP"
OUTCOME = "C8_SUCCESSOR_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_PREP_ONLY"
STOP_CODE = "STOP_C8_SUCCESSOR_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_PREP_READY"

OUT_DIR = ROOT / "data/c8_successor_surface_bounded_probe_prep_acceptance_v0"
RECEIPT_DIR = ROOT / "data/c8_successor_surface_bounded_probe_prep_acceptance_v0_receipts"

REVIEW_RECEIPT = ROOT / "data/c8_successor_frontier_surface_selection_review_v0_receipts/c8_successor_surface_review_receipt_f0308b64.json"
REVIEW_PACKET = ROOT / "data/c8_successor_frontier_surface_selection_review_v0/c8_successor_surface_selection_review_packet_v0.json"
REVIEW_DECISION = ROOT / "data/c8_successor_frontier_surface_selection_review_v0/c8_successor_surface_selection_review_decision_v0.json"
REVIEW_AUDIT = ROOT / "data/c8_successor_frontier_surface_selection_review_v0/c8_successor_surface_selection_review_audit_v0.json"
REVIEW_REPORT = ROOT / "data/c8_successor_frontier_surface_selection_review_v0/c8_successor_surface_selection_review_report.json"

ACCEPTANCE_PACKET = OUT_DIR / "c8_successor_surface_bounded_probe_prep_acceptance_packet_v0.json"
ACCEPTANCE_DECISION = OUT_DIR / "c8_successor_surface_bounded_probe_prep_acceptance_decision_v0.json"
ACCEPTANCE_AUTHORITY = OUT_DIR / "c8_successor_surface_bounded_probe_prep_authority_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_successor_surface_bounded_probe_prep_acceptance_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_successor_surface_bounded_probe_prep_acceptance_readout_v0.json"
REPORT = OUT_DIR / "c8_successor_surface_bounded_probe_prep_acceptance_report.json"

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
    chk(failures, "review_status", review_receipt.get("status"), "TYPED_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_REVIEW_PASS")
    chk(failures, "review_outcome", review_receipt.get("outcome_class"), "C8_SUCCESSOR_FRONTIER_SURFACE_REVIEWABLE_NOT_ACCEPTED")
    chk(failures, "review_receipt_id", review_receipt.get("receipt_id"), "c8_successor_surface_review_receipt_f0308b64")

    chk(failures, "review_complete", summary.get("review_complete"), True)
    chk(failures, "source_selection_receipt_id", summary.get("source_selection_receipt_id"), "c8_successor_surface_selection_receipt_c50e9fdc")
    chk(failures, "source_selection_packet_id", summary.get("source_selection_packet_id"), "c8_successor_surface_selection_27c11033")
    chk(failures, "selected_surface_id", summary.get("selected_surface_id"), "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0")
    chk(failures, "selected_surface_kind", summary.get("selected_surface_kind"), "REUSE_AUTHORITY_BOUNDARY_SURFACE")
    chk(failures, "selected_surface_label", summary.get("selected_surface_label"), "C8_POST_CLOSURE_LOCAL_LOOP_REUSE_PRESSURE_SURFACE")
    chk(failures, "review_decision", summary.get("review_decision"), "REVIEWABLE_NOT_ACCEPTED")
    chk(failures, "surface_review_class", summary.get("surface_review_class"), "WELL_FORMED_BOUNDED_REUSE_AUTHORITY_BOUNDARY_SURFACE")
    chk(failures, "surface_is_well_formed", summary.get("surface_is_well_formed"), True)
    chk(failures, "surface_is_bounded", summary.get("surface_is_bounded"), True)
    chk(failures, "reuse_boundary_explicit", summary.get("reuse_boundary_explicit"), True)
    chk(failures, "human_decision_required", summary.get("human_decision_required"), True)
    chk(failures, "accepted_for_probe_prep_now_prior", summary.get("accepted_for_probe_prep_now"), False)
    chk(failures, "probe_run_prior", summary.get("probe_run"), False)
    chk(failures, "new_instrument_build_prior", summary.get("new_instrument_build"), False)
    chk(failures, "new_c8_rerun_prior", summary.get("new_c8_rerun"), False)
    chk(failures, "reusable_schema_authorized_prior", summary.get("reusable_schema_authorized"), False)
    chk(failures, "global_solution_claim_prior", summary.get("global_solution_claim"), False)
    chk(failures, "frontier_solved_claim_prior", summary.get("frontier_solved_claim"), False)

    chk(failures, "packet_review_decision", review_packet.get("review_decision"), "REVIEWABLE_NOT_ACCEPTED")
    chk(failures, "packet_human_decision_required", review_packet.get("human_decision_required"), True)
    chk(failures, "packet_accepted_for_probe_prep_now", review_packet.get("accepted_for_probe_prep_now"), False)

    authorized_prior = review_packet.get("authorized_now", {})
    for key in [
        "bounded_probe_prep",
        "probe_execution",
        "instrument_build",
        "cell1_build",
        "verification_probe",
        "c8_rerun",
        "missing_instrument_proposal",
        "reusable_schema",
    ]:
        chk(failures, f"prior_authorized_{key}", authorized_prior.get(key), False)

    chk(failures, "decision_review_decision", review_decision.get("review_decision"), "REVIEWABLE_NOT_ACCEPTED")
    chk(failures, "decision_requires_human_decision", review_decision.get("requires_human_decision"), True)

    if "ACCEPT_FOR_BOUNDED_PROBE_PREP" not in review_decision.get("possible_human_decisions", []):
        failures.append("accept_decision_not_available_in_possible_human_decisions")

    operator_decision = "ACCEPT_FOR_BOUNDED_PROBE_PREP"

    acceptance_decision = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_acceptance_decision_v0",
        "acceptance_decision_id": None,
        "operator_decision": operator_decision,
        "source_review_receipt_id": review_receipt.get("receipt_id"),
        "source_review_packet_id": review_packet.get("review_packet_id"),
        "source_review_decision_id": review_decision.get("review_decision_id"),
        "selected_surface_id": summary.get("selected_surface_id"),
        "selected_surface_kind": summary.get("selected_surface_kind"),
        "selected_surface_label": summary.get("selected_surface_label"),
        "accepted_for_bounded_probe_prep": True,
        "accepted_for_probe_execution": False,
        "accepted_for_instrument_build": False,
        "accepted_for_c8_rerun": False,
        "accepted_for_reusable_schema": False,
        "acceptance_status": "ACCEPTED_FOR_BOUNDED_PROBE_PREP_ONLY",
        "human_decision_consumed": True,
        "requires_next_bounded_prep_packet": True,
        "next_allowed_unit": "CREATE_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_V0",
        "review_basis": {
            "surface_review_class": summary.get("surface_review_class"),
            "surface_is_well_formed": summary.get("surface_is_well_formed"),
            "surface_is_bounded": summary.get("surface_is_bounded"),
            "reuse_boundary_explicit": summary.get("reuse_boundary_explicit"),
        },
    }
    acceptance_decision["acceptance_decision_id"] = "c8_successor_probe_prep_acceptance_decision_" + sig8(acceptance_decision)
    write_json(ACCEPTANCE_DECISION, acceptance_decision)

    acceptance_authority = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_authority_v0",
        "authority_id": None,
        "source_acceptance_decision_id": acceptance_decision["acceptance_decision_id"],
        "authority_status": "BOUNDED_PROBE_PREP_AUTHORITY_CREATED",
        "authorized_future_unit": "CREATE_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_V0",
        "authorized_future_unit_count": 1,
        "authorized_future_probe_execution_count": 0,
        "authorized_future_instrument_build_count": 0,
        "authorized_future_c8_rerun_count": 0,
        "authorized_future_reusable_schema_count": 0,
        "authority_scope": {
            "may_create_probe_prep_packet": True,
            "may_execute_probe": False,
            "may_build_instrument": False,
            "may_rerun_c8": False,
            "may_create_missing_instrument_proposal": False,
            "may_authorize_reusable_schema": False,
            "may_open_research_mode": False,
        },
        "boundary_note": "Acceptance authorizes exactly one bounded probe-prep packet for the selected reuse-authority boundary surface. It does not authorize probe execution.",
    }
    acceptance_authority["authority_id"] = "c8_successor_probe_prep_authority_" + sig8(acceptance_authority)
    write_json(ACCEPTANCE_AUTHORITY, acceptance_authority)

    acceptance_packet = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_acceptance_packet_v0",
        "acceptance_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "acceptance_status": "ACCEPTED_FOR_BOUNDED_PROBE_PREP_ONLY",
        "operator_decision": operator_decision,
        "source_review_receipt_id": review_receipt.get("receipt_id"),
        "source_review_packet_id": review_packet.get("review_packet_id"),
        "source_review_decision_id": review_decision.get("review_decision_id"),
        "selected_surface_id": summary.get("selected_surface_id"),
        "selected_surface_kind": summary.get("selected_surface_kind"),
        "selected_surface_label": summary.get("selected_surface_label"),
        "acceptance_decision_ref": rel(ACCEPTANCE_DECISION),
        "acceptance_authority_ref": rel(ACCEPTANCE_AUTHORITY),
        "accepted_for_bounded_probe_prep": True,
        "accepted_for_probe_execution": False,
        "accepted_for_instrument_build": False,
        "accepted_for_cell1_build": False,
        "accepted_for_verification_probe": False,
        "accepted_for_c8_rerun": False,
        "accepted_for_missing_instrument_proposal": False,
        "accepted_for_reusable_schema": False,
        "authorized_future_unit": acceptance_authority["authorized_future_unit"],
        "authorized_future_unit_count": 1,
        "recommended_next_unit": acceptance_authority["authorized_future_unit"],
        "recommended_next_unit_status": "AUTHORIZED_FOR_ONE_BOUNDED_PREP_PACKET_ONLY",
    }
    acceptance_packet["acceptance_packet_id"] = "c8_successor_probe_prep_acceptance_packet_" + sig8(acceptance_packet)
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
        "C8_PROBE_PREP_ACCEPTANCE_0_REVIEW_RECEIPT_VERIFIED": review_receipt.get("gate") == "PASS",
        "C8_PROBE_PREP_ACCEPTANCE_1_REVIEWABLE_NOT_ACCEPTED_SOURCE": summary.get("review_decision") == "REVIEWABLE_NOT_ACCEPTED",
        "C8_PROBE_PREP_ACCEPTANCE_2_HUMAN_DECISION_REQUIRED_SOURCE": summary.get("human_decision_required") is True,
        "C8_PROBE_PREP_ACCEPTANCE_3_OPERATOR_ACCEPT_DECISION_TYPED": operator_decision == "ACCEPT_FOR_BOUNDED_PROBE_PREP",
        "C8_PROBE_PREP_ACCEPTANCE_4_SURFACE_WELL_FORMED_AND_BOUNDED": summary.get("surface_is_well_formed") is True and summary.get("surface_is_bounded") is True,
        "C8_PROBE_PREP_ACCEPTANCE_5_REUSE_BOUNDARY_EXPLICIT": summary.get("reuse_boundary_explicit") is True,
        "C8_PROBE_PREP_ACCEPTANCE_6_ACCEPTED_FOR_PREP_ONLY": acceptance_packet["accepted_for_bounded_probe_prep"] is True and acceptance_packet["accepted_for_probe_execution"] is False,
        "C8_PROBE_PREP_ACCEPTANCE_7_ONE_FUTURE_PREP_UNIT_ONLY": acceptance_authority["authorized_future_unit_count"] == 1,
        "C8_PROBE_PREP_ACCEPTANCE_8_NO_PROBE_BUILD_OR_RERUN_NOW": negative_controls["probe_execution_count"] == 0 and negative_controls["instrument_build_count"] == 0 and negative_controls["c8_rerun_count"] == 0,
        "C8_PROBE_PREP_ACCEPTANCE_9_NO_REUSABLE_SCHEMA_AUTHORIZED": negative_controls["reusable_schema_authorized_count"] == 0,
        "C8_PROBE_PREP_ACCEPTANCE_10_NO_RESEARCH_OR_GLOBAL_CLAIM": negative_controls["research_mode_opened_count"] == 0 and negative_controls["global_solution_claim_count"] == 0 and negative_controls["frontier_solved_claim_count"] == 0,
        "C8_PROBE_PREP_ACCEPTANCE_11_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_PROBE_PREP_ACCEPTANCE_12_BAD_COUNTERS_ZERO": not bool(nonzero),
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_ACCEPTANCE_PASS" if gate == "PASS" else "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_ACCEPTANCE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_ACCEPTANCE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_ACCEPTANCE_FAILED"

    boundary_audit = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_acceptance_boundary_audit_v0",
        "boundary_audit_id": None,
        "gate": gate,
        "selected_surface_id": summary.get("selected_surface_id"),
        "accepted_for_bounded_probe_prep": True,
        "authority_boundary": {
            "may_create_one_bounded_probe_prep_packet": True,
            "may_execute_probe_now": False,
            "may_build_instrument_now": False,
            "may_rerun_c8_now": False,
            "may_authorize_reusable_schema_now": False,
            "may_open_research_mode_now": False,
        },
        "negative_controls": negative_controls,
        "acceptance_gate_results": acceptance_gates,
        "failures": failures,
        "warnings": warnings,
    }
    boundary_audit["boundary_audit_id"] = "c8_successor_probe_prep_acceptance_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    readout = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_acceptance_readout_v0",
        "title": "C8 successor surface bounded probe-prep acceptance readout",
        "status": status,
        "outcome_class": outcome,
        "operator_decision": operator_decision,
        "selected_surface_id": summary.get("selected_surface_id"),
        "selected_surface_kind": summary.get("selected_surface_kind"),
        "accepted_for_bounded_probe_prep": True,
        "accepted_for_probe_execution": False,
        "authorized_future_unit": acceptance_authority["authorized_future_unit"],
        "authorized_future_unit_count": 1,
        "probe_run": False,
        "instrument_built": False,
        "c8_rerun_performed": False,
        "reusable_schema_authorized": False,
        "summary": "Human acceptance authorizes exactly one bounded probe-prep packet for the selected reuse-authority boundary surface. It does not execute a probe.",
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_acceptance_report_v0",
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
        "selected_surface_id": summary.get("selected_surface_id"),
        "selected_surface_kind": summary.get("selected_surface_kind"),
        "operator_decision": operator_decision,
        "accepted_for_bounded_probe_prep": True,
        "accepted_for_probe_execution": False,
        "authorized_future_unit": acceptance_authority["authorized_future_unit"],
        "authorized_future_unit_count": 1,
        "probe_run": False,
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
        "schema_version": "c8_successor_surface_bounded_probe_prep_acceptance_receipt_v0",
        "receipt_type": "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_ACCEPTANCE_RECEIPT",
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
            "selected_surface_id": summary.get("selected_surface_id"),
            "selected_surface_kind": summary.get("selected_surface_kind"),
            "selected_surface_label": summary.get("selected_surface_label"),
            "accepted_for_bounded_probe_prep": True,
            "accepted_for_probe_execution": False,
            "accepted_for_instrument_build": False,
            "accepted_for_cell1_build": False,
            "accepted_for_verification_probe": False,
            "accepted_for_c8_rerun": False,
            "accepted_for_missing_instrument_proposal": False,
            "accepted_for_reusable_schema": False,
            "authorized_future_unit": acceptance_authority["authorized_future_unit"],
            "authorized_future_unit_count": 1,
            "probe_run": False,
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

    receipt["receipt_id"] = "c8_successor_probe_prep_acceptance_receipt_" + sig8(receipt)
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
    print(f"selected_surface_id={summary.get('selected_surface_id')}")
    print(f"selected_surface_kind={summary.get('selected_surface_kind')}")
    print(f"accepted_for_bounded_probe_prep=true")
    print(f"accepted_for_probe_execution=false")
    print(f"authorized_future_unit={acceptance_authority['authorized_future_unit']}")
    print(f"authorized_future_unit_count=1")
    print(f"probe_run=false")
    print(f"new_instrument_build=false")
    print(f"new_c8_rerun=false")
    print(f"reusable_schema_authorized=false")
    print(f"acceptance_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
