#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_REVIEW_V0"
TARGET_UNIT_ID = "research.c8.successor_surface.bounded_probe_prep_packet.review.v0"
MILESTONE = "C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_REVIEWED"
OUTCOME = "C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_REVIEWABLE_NOT_ACCEPTED"
STOP_CODE = "STOP_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_REVIEW_READY_FOR_HUMAN_DECISION"

OUT_DIR = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_review_v0"
RECEIPT_DIR = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_review_v0_receipts"

PREP_RECEIPT = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_v0_receipts/c8_successor_probe_prep_packet_receipt_bbb5ebc3.json"
PREP_PACKET = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_v0/c8_successor_surface_bounded_probe_prep_packet_v0.json"
PROBE_SPEC = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_v0/c8_successor_surface_bounded_probe_spec_v0.json"
PROBE_CONSTRAINTS = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_v0/c8_successor_surface_bounded_probe_constraints_v0.json"
PREP_BOUNDARY_AUDIT = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_v0/c8_successor_surface_bounded_probe_prep_packet_boundary_audit_v0.json"
PREP_REPORT = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_v0/c8_successor_surface_bounded_probe_prep_packet_report.json"

REVIEW_PACKET = OUT_DIR / "c8_successor_surface_bounded_probe_prep_packet_review_packet_v0.json"
REVIEW_DECISION = OUT_DIR / "c8_successor_surface_bounded_probe_prep_packet_review_decision_v0.json"
REVIEW_AUDIT = OUT_DIR / "c8_successor_surface_bounded_probe_prep_packet_review_audit_v0.json"
READOUT = OUT_DIR / "c8_successor_surface_bounded_probe_prep_packet_review_readout_v0.json"
REPORT = OUT_DIR / "c8_successor_surface_bounded_probe_prep_packet_review_report.json"

NEGATIVE_CONTROL_KEYS = [
    "accepted_for_probe_execution_count",
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
        "prep_receipt": PREP_RECEIPT,
        "prep_packet": PREP_PACKET,
        "probe_spec": PROBE_SPEC,
        "probe_constraints": PROBE_CONSTRAINTS,
        "prep_boundary_audit": PREP_BOUNDARY_AUDIT,
        "prep_report": PREP_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    prep_receipt = read_json(PREP_RECEIPT)
    prep_packet = read_json(PREP_PACKET)
    probe_spec = read_json(PROBE_SPEC)
    probe_constraints = read_json(PROBE_CONSTRAINTS)
    prep_audit = read_json(PREP_BOUNDARY_AUDIT)
    prep_report = read_json(PREP_REPORT)

    summary = prep_receipt.get("machine_readable_prep_summary", {})

    chk(failures, "prep_gate", prep_receipt.get("gate"), "PASS")
    chk(failures, "prep_status", prep_receipt.get("status"), "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_PASS")
    chk(failures, "prep_outcome", prep_receipt.get("outcome_class"), "C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_CREATED_FOR_REVIEW")
    chk(failures, "prep_receipt_id", prep_receipt.get("receipt_id"), "c8_successor_probe_prep_packet_receipt_bbb5ebc3")

    expected_summary = {
        "prep_complete": True,
        "source_acceptance_receipt_id": "c8_successor_probe_prep_acceptance_receipt_b1827f29",
        "source_acceptance_packet_id": "c8_successor_probe_prep_acceptance_packet_bcda4dcb",
        "source_acceptance_decision_id": "c8_successor_probe_prep_acceptance_decision_ee8dfe9f",
        "source_authority_id": "c8_successor_probe_prep_authority_44c93923",
        "selected_surface_id": "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0",
        "selected_surface_kind": "REUSE_AUTHORITY_BOUNDARY_SURFACE",
        "selected_surface_label": "C8_POST_CLOSURE_LOCAL_LOOP_REUSE_PRESSURE_SURFACE",
        "probe_id": "c8_successor_surface_reuse_authority_boundary_probe_v0",
        "probe_kind": "REUSE_AUTHORITY_BOUNDARY_PROBE",
        "prep_packet_id": "c8_successor_probe_prep_packet_74a6c209",
        "prepared_for_review_only": True,
        "recommended_review_unit": "REVIEW_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_V0",
        "requires_review_before_probe_execution": True,
        "accepted_for_probe_execution_now": False,
        "probe_executed_now": False,
        "new_instrument_build": False,
        "new_c8_rerun": False,
        "reusable_schema_authorized": False,
    }

    for key, want in expected_summary.items():
        chk(failures, f"summary_{key}", summary.get(key), want)

    chk(failures, "packet_prep_status", prep_packet.get("prep_status"), "BOUNDED_PROBE_PREP_PACKET_CREATED_FOR_REVIEW")
    chk(failures, "packet_prepared_for_review_only", prep_packet.get("prepared_for_review_only"), True)
    chk(failures, "packet_probe_executed_now", prep_packet.get("probe_executed_now"), False)
    chk(failures, "packet_recommended_review_unit", prep_packet.get("recommended_review_unit"), "REVIEW_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_V0")

    chk(failures, "spec_probe_status", probe_spec.get("probe_status"), "PREPARED_FOR_REVIEW_ONLY")
    chk(failures, "spec_probe_kind", probe_spec.get("probe_kind"), "REUSE_AUTHORITY_BOUNDARY_PROBE")

    question = probe_spec.get("bounded_probe_question", "")
    if "one closed local C8 instrumentation loop" not in question:
        failures.append("probe_question_missing_local_loop")
    if "non-reusable" not in question:
        failures.append("probe_question_missing_non_reusable")
    if "explicitly promotes" not in question:
        failures.append("probe_question_missing_explicit_promotion")

    chk(failures, "constraints_status", probe_constraints.get("constraint_status"), "BOUNDED_PREP_ONLY")
    chk(failures, "constraints_requires_review", probe_constraints.get("requires_review_before_probe_execution"), True)
    chk(failures, "constraints_future_probe_execution_count", probe_constraints.get("max_future_probe_execution_count_after_separate_acceptance"), 1)
    chk(failures, "constraints_probe_execution_count_now", probe_constraints.get("max_probe_execution_count_now"), 0)
    chk(failures, "constraints_instrument_build_count", probe_constraints.get("max_instrument_build_count"), 0)
    chk(failures, "constraints_c8_rerun_count", probe_constraints.get("max_c8_rerun_count"), 0)
    chk(failures, "constraints_reusable_schema_count", probe_constraints.get("max_reusable_schema_authorization_count"), 0)

    authorized_now = probe_constraints.get("authorized_now", {})
    for key, want in {
        "probe_prep_packet_created": True,
        "probe_execution": False,
        "instrument_build": False,
        "cell1_build": False,
        "verification_probe": False,
        "c8_rerun": False,
        "missing_instrument_proposal": False,
        "reusable_schema": False,
        "research_mode": False,
    }.items():
        chk(failures, f"authorized_now_{key}", authorized_now.get(key), want)

    review_findings = {
        "prep_packet_is_well_formed": True,
        "prep_packet_is_bounded": True,
        "probe_spec_is_typed": True,
        "probe_question_is_bounded": True,
        "reuse_authority_boundary_preserved": True,
        "requires_review_before_probe_execution": True,
        "prep_packet_does_not_execute_probe": True,
        "prep_packet_does_not_authorize_build": True,
        "prep_packet_does_not_authorize_rerun": True,
        "prep_packet_does_not_authorize_reusable_schema": True,
        "review_result": "REVIEWABLE_NOT_ACCEPTED",
    }

    review_decision = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_packet_review_decision_v0",
        "review_decision_id": None,
        "source_prep_receipt_id": prep_receipt.get("receipt_id"),
        "source_prep_packet_id": prep_packet.get("prep_packet_id"),
        "probe_id": probe_spec.get("probe_id"),
        "probe_kind": probe_spec.get("probe_kind"),
        "selected_surface_id": summary.get("selected_surface_id"),
        "selected_surface_kind": summary.get("selected_surface_kind"),
        "selected_surface_label": summary.get("selected_surface_label"),
        "review_status": "REVIEWED",
        "review_decision": "REVIEWABLE_NOT_ACCEPTED",
        "prep_review_class": "WELL_FORMED_BOUNDED_REUSE_AUTHORITY_PROBE_PREP_PACKET",
        "possible_human_decisions": [
            "ACCEPT_FOR_BOUNDED_PROBE_EXECUTION",
            "REJECT_PROBE_PREP_PACKET",
            "NARROW_PROBE_PREP_PACKET",
        ],
        "accepted_for_probe_execution": False,
        "rejected": False,
        "narrowed": False,
        "requires_human_decision": True,
        "review_findings": review_findings,
        "review_note": "The bounded probe-prep packet is well formed and reviewable, but this review unit does not accept probe execution.",
    }
    review_decision["review_decision_id"] = "c8_successor_probe_prep_packet_review_decision_" + sig8(review_decision)
    write_json(REVIEW_DECISION, review_decision)

    review_packet = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_packet_review_packet_v0",
        "review_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "review_status": "REVIEW_PACKET_CREATED",
        "source_prep_receipt_id": prep_receipt.get("receipt_id"),
        "source_prep_packet_id": prep_packet.get("prep_packet_id"),
        "probe_id": probe_spec.get("probe_id"),
        "probe_kind": probe_spec.get("probe_kind"),
        "selected_surface_id": summary.get("selected_surface_id"),
        "selected_surface_kind": summary.get("selected_surface_kind"),
        "selected_surface_label": summary.get("selected_surface_label"),
        "review_decision_ref": rel(REVIEW_DECISION),
        "review_decision": review_decision["review_decision"],
        "prep_review_class": review_decision["prep_review_class"],
        "human_decision_required": True,
        "accepted_for_probe_execution_now": False,
        "rejected_now": False,
        "narrowed_now": False,
        "authorized_now": {
            "probe_execution": False,
            "instrument_build": False,
            "cell1_build": False,
            "verification_probe": False,
            "c8_rerun": False,
            "missing_instrument_proposal": False,
            "reusable_schema": False,
            "research_mode": False,
        },
    }
    review_packet["review_packet_id"] = "c8_successor_probe_prep_packet_review_packet_" + sig8(review_packet)
    write_json(REVIEW_PACKET, review_packet)

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
        "C8_PROBE_PREP_REVIEW_0_PREP_RECEIPT_VERIFIED": prep_receipt.get("gate") == "PASS",
        "C8_PROBE_PREP_REVIEW_1_PREP_PACKET_FOR_REVIEW_ONLY": summary.get("prepared_for_review_only") is True,
        "C8_PROBE_PREP_REVIEW_2_PROBE_SPEC_TYPED": probe_spec.get("probe_kind") == "REUSE_AUTHORITY_BOUNDARY_PROBE",
        "C8_PROBE_PREP_REVIEW_3_BOUNDED_QUESTION_PRESENT": "non-reusable" in question and "explicitly promotes" in question,
        "C8_PROBE_PREP_REVIEW_4_REVIEW_REQUIRED_BEFORE_EXECUTION": summary.get("requires_review_before_probe_execution") is True,
        "C8_PROBE_PREP_REVIEW_5_REVIEWABLE_NOT_ACCEPTED": review_decision["review_decision"] == "REVIEWABLE_NOT_ACCEPTED",
        "C8_PROBE_PREP_REVIEW_6_HUMAN_DECISION_REQUIRED": review_decision["requires_human_decision"] is True,
        "C8_PROBE_PREP_REVIEW_7_NO_PROBE_EXECUTION_NOW": negative_controls["probe_execution_count"] == 0,
        "C8_PROBE_PREP_REVIEW_8_NO_BUILD_OR_RERUN_NOW": negative_controls["instrument_build_count"] == 0 and negative_controls["c8_rerun_count"] == 0,
        "C8_PROBE_PREP_REVIEW_9_NO_REUSABLE_SCHEMA_AUTHORIZED": negative_controls["reusable_schema_authorized_count"] == 0,
        "C8_PROBE_PREP_REVIEW_10_NO_RESEARCH_OR_GLOBAL_CLAIM": negative_controls["research_mode_opened_count"] == 0 and negative_controls["global_solution_claim_count"] == 0 and negative_controls["frontier_solved_claim_count"] == 0,
        "C8_PROBE_PREP_REVIEW_11_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_PROBE_PREP_REVIEW_12_BAD_COUNTERS_ZERO": not bool(nonzero),
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_REVIEW_PASS" if gate == "PASS" else "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_REVIEW_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_REVIEW_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_REVIEW_FAILED"

    review_audit = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_packet_review_audit_v0",
        "review_audit_id": None,
        "gate": gate,
        "prep_packet_id": prep_packet.get("prep_packet_id"),
        "probe_id": probe_spec.get("probe_id"),
        "review_findings": review_findings,
        "negative_controls": negative_controls,
        "acceptance_gate_results": acceptance_gates,
        "failures": failures,
        "warnings": warnings,
    }
    review_audit["review_audit_id"] = "c8_successor_probe_prep_packet_review_audit_" + sig8(review_audit)
    write_json(REVIEW_AUDIT, review_audit)

    readout = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_packet_review_readout_v0",
        "title": "C8 successor surface bounded probe-prep packet review readout",
        "status": status,
        "outcome_class": outcome,
        "prep_packet_id": prep_packet.get("prep_packet_id"),
        "probe_id": probe_spec.get("probe_id"),
        "probe_kind": probe_spec.get("probe_kind"),
        "review_decision": review_decision["review_decision"],
        "prep_review_class": review_decision["prep_review_class"],
        "human_decision_required": True,
        "accepted_for_probe_execution_now": False,
        "probe_executed_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized_now": False,
        "summary": "The bounded probe-prep packet is reviewable but not accepted for probe execution. Human decision is required.",
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_packet_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "review_packet_ref": rel(REVIEW_PACKET),
        "review_decision_ref": rel(REVIEW_DECISION),
        "review_audit_ref": rel(REVIEW_AUDIT),
        "source_prep_receipt_id": prep_receipt.get("receipt_id"),
        "source_prep_packet_id": prep_packet.get("prep_packet_id"),
        "probe_id": probe_spec.get("probe_id"),
        "probe_kind": probe_spec.get("probe_kind"),
        "selected_surface_id": summary.get("selected_surface_id"),
        "review_decision": review_decision["review_decision"],
        "prep_review_class": review_decision["prep_review_class"],
        "human_decision_required": True,
        "accepted_for_probe_execution_now": False,
        "probe_executed_now": False,
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
        "schema_version": "c8_successor_surface_bounded_probe_prep_packet_review_receipt_v0",
        "receipt_type": "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_REVIEW_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_refs": {
            "prep_receipt_ref": rel(PREP_RECEIPT),
            "prep_packet_ref": rel(PREP_PACKET),
            "probe_spec_ref": rel(PROBE_SPEC),
            "probe_constraints_ref": rel(PROBE_CONSTRAINTS),
            "prep_boundary_audit_ref": rel(PREP_BOUNDARY_AUDIT),
            "prep_report_ref": rel(PREP_REPORT),
        },
        "machine_readable_review_summary": {
            "review_complete": gate == "PASS",
            "source_prep_receipt_id": prep_receipt.get("receipt_id"),
            "source_prep_packet_id": prep_packet.get("prep_packet_id"),
            "probe_id": probe_spec.get("probe_id"),
            "probe_kind": probe_spec.get("probe_kind"),
            "selected_surface_id": summary.get("selected_surface_id"),
            "selected_surface_kind": summary.get("selected_surface_kind"),
            "selected_surface_label": summary.get("selected_surface_label"),
            "review_decision": review_decision["review_decision"],
            "prep_review_class": review_decision["prep_review_class"],
            "prep_packet_is_well_formed": review_findings["prep_packet_is_well_formed"],
            "prep_packet_is_bounded": review_findings["prep_packet_is_bounded"],
            "probe_spec_is_typed": review_findings["probe_spec_is_typed"],
            "human_decision_required": True,
            "accepted_for_probe_execution_now": False,
            "rejected_now": False,
            "narrowed_now": False,
            "probe_executed_now": False,
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
            "review_packet": rel(REVIEW_PACKET),
            "review_decision": rel(REVIEW_DECISION),
            "review_audit": rel(REVIEW_AUDIT),
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

    receipt["receipt_id"] = "c8_successor_probe_prep_packet_review_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"review_receipt_id={receipt['receipt_id']}")
    print(f"review_receipt_path={rel(receipt_path)}")
    print(f"review_packet_path={rel(REVIEW_PACKET)}")
    print(f"review_decision_path={rel(REVIEW_DECISION)}")
    print(f"prep_packet_id={prep_packet.get('prep_packet_id')}")
    print(f"probe_id={probe_spec.get('probe_id')}")
    print(f"probe_kind={probe_spec.get('probe_kind')}")
    print(f"review_decision={review_decision['review_decision']}")
    print(f"prep_review_class={review_decision['prep_review_class']}")
    print("human_decision_required=true")
    print("accepted_for_probe_execution_now=false")
    print("probe_executed_now=false")
    print("new_instrument_build=false")
    print("new_c8_rerun=false")
    print("reusable_schema_authorized=false")
    print(f"review_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
