#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_V0"
TARGET_UNIT_ID = "research.c8.successor_surface.bounded_probe_prep_packet.v0"
MILESTONE = "C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_CREATED"
OUTCOME = "C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_CREATED_FOR_REVIEW"
STOP_CODE = "STOP_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_READY_FOR_REVIEW"

OUT_DIR = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_v0"
RECEIPT_DIR = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_v0_receipts"

ACCEPTANCE_RECEIPT = ROOT / "data/c8_successor_surface_bounded_probe_prep_acceptance_v0_receipts/c8_successor_probe_prep_acceptance_receipt_b1827f29.json"
ACCEPTANCE_PACKET = ROOT / "data/c8_successor_surface_bounded_probe_prep_acceptance_v0/c8_successor_surface_bounded_probe_prep_acceptance_packet_v0.json"
ACCEPTANCE_DECISION = ROOT / "data/c8_successor_surface_bounded_probe_prep_acceptance_v0/c8_successor_surface_bounded_probe_prep_acceptance_decision_v0.json"
ACCEPTANCE_AUTHORITY = ROOT / "data/c8_successor_surface_bounded_probe_prep_acceptance_v0/c8_successor_surface_bounded_probe_prep_authority_v0.json"
ACCEPTANCE_BOUNDARY_AUDIT = ROOT / "data/c8_successor_surface_bounded_probe_prep_acceptance_v0/c8_successor_surface_bounded_probe_prep_acceptance_boundary_audit_v0.json"
ACCEPTANCE_REPORT = ROOT / "data/c8_successor_surface_bounded_probe_prep_acceptance_v0/c8_successor_surface_bounded_probe_prep_acceptance_report.json"

PREP_PACKET = OUT_DIR / "c8_successor_surface_bounded_probe_prep_packet_v0.json"
PROBE_SPEC = OUT_DIR / "c8_successor_surface_bounded_probe_spec_v0.json"
PROBE_CONSTRAINTS = OUT_DIR / "c8_successor_surface_bounded_probe_constraints_v0.json"
PREP_BOUNDARY_AUDIT = OUT_DIR / "c8_successor_surface_bounded_probe_prep_packet_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_successor_surface_bounded_probe_prep_packet_readout_v0.json"
REPORT = OUT_DIR / "c8_successor_surface_bounded_probe_prep_packet_report.json"

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
    "over_budget_prep_packet_count",
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
        "acceptance_receipt": ACCEPTANCE_RECEIPT,
        "acceptance_packet": ACCEPTANCE_PACKET,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_authority": ACCEPTANCE_AUTHORITY,
        "acceptance_boundary_audit": ACCEPTANCE_BOUNDARY_AUDIT,
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
    acceptance_authority = read_json(ACCEPTANCE_AUTHORITY)
    acceptance_audit = read_json(ACCEPTANCE_BOUNDARY_AUDIT)
    acceptance_report = read_json(ACCEPTANCE_REPORT)

    summary = acceptance_receipt.get("machine_readable_acceptance_summary", {})

    chk(failures, "acceptance_gate", acceptance_receipt.get("gate"), "PASS")
    chk(failures, "acceptance_status", acceptance_receipt.get("status"), "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_ACCEPTANCE_PASS")
    chk(failures, "acceptance_outcome", acceptance_receipt.get("outcome_class"), "C8_SUCCESSOR_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_PREP_ONLY")
    chk(failures, "acceptance_receipt_id", acceptance_receipt.get("receipt_id"), "c8_successor_probe_prep_acceptance_receipt_b1827f29")

    chk(failures, "acceptance_complete", summary.get("acceptance_complete"), True)
    chk(failures, "operator_decision", summary.get("operator_decision"), "ACCEPT_FOR_BOUNDED_PROBE_PREP")
    chk(failures, "selected_surface_id", summary.get("selected_surface_id"), "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0")
    chk(failures, "selected_surface_kind", summary.get("selected_surface_kind"), "REUSE_AUTHORITY_BOUNDARY_SURFACE")
    chk(failures, "selected_surface_label", summary.get("selected_surface_label"), "C8_POST_CLOSURE_LOCAL_LOOP_REUSE_PRESSURE_SURFACE")
    chk(failures, "accepted_for_bounded_probe_prep", summary.get("accepted_for_bounded_probe_prep"), True)
    chk(failures, "accepted_for_probe_execution", summary.get("accepted_for_probe_execution"), False)
    chk(failures, "accepted_for_instrument_build", summary.get("accepted_for_instrument_build"), False)
    chk(failures, "accepted_for_c8_rerun", summary.get("accepted_for_c8_rerun"), False)
    chk(failures, "accepted_for_reusable_schema", summary.get("accepted_for_reusable_schema"), False)
    chk(failures, "authorized_future_unit", summary.get("authorized_future_unit"), UNIT_ID)
    chk(failures, "authorized_future_unit_count", summary.get("authorized_future_unit_count"), 1)
    chk(failures, "probe_run_prior", summary.get("probe_run"), False)
    chk(failures, "new_instrument_build_prior", summary.get("new_instrument_build"), False)
    chk(failures, "new_c8_rerun_prior", summary.get("new_c8_rerun"), False)
    chk(failures, "reusable_schema_authorized_prior", summary.get("reusable_schema_authorized"), False)

    chk(failures, "packet_authorized_future_unit", acceptance_packet.get("authorized_future_unit"), UNIT_ID)
    chk(failures, "packet_authorized_future_unit_count", acceptance_packet.get("authorized_future_unit_count"), 1)
    chk(failures, "authority_authorized_future_unit", acceptance_authority.get("authorized_future_unit"), UNIT_ID)
    chk(failures, "authority_authorized_future_unit_count", acceptance_authority.get("authorized_future_unit_count"), 1)

    scope = acceptance_authority.get("authority_scope", {})
    chk(failures, "authority_may_create_probe_prep_packet", scope.get("may_create_probe_prep_packet"), True)
    chk(failures, "authority_may_execute_probe", scope.get("may_execute_probe"), False)
    chk(failures, "authority_may_build_instrument", scope.get("may_build_instrument"), False)
    chk(failures, "authority_may_rerun_c8", scope.get("may_rerun_c8"), False)
    chk(failures, "authority_may_authorize_reusable_schema", scope.get("may_authorize_reusable_schema"), False)
    chk(failures, "authority_may_open_research_mode", scope.get("may_open_research_mode"), False)

    probe_id = "c8_successor_surface_reuse_authority_boundary_probe_v0"

    probe_spec = {
        "schema_version": "c8_successor_surface_bounded_probe_spec_v0",
        "probe_id": probe_id,
        "probe_kind": "REUSE_AUTHORITY_BOUNDARY_PROBE",
        "probe_status": "PREPARED_FOR_REVIEW_ONLY",
        "source_acceptance_receipt_id": acceptance_receipt.get("receipt_id"),
        "source_acceptance_packet_id": acceptance_packet.get("acceptance_packet_id"),
        "source_authority_id": acceptance_authority.get("authority_id"),
        "selected_surface_id": summary.get("selected_surface_id"),
        "selected_surface_kind": summary.get("selected_surface_kind"),
        "selected_surface_label": summary.get("selected_surface_label"),
        "bounded_probe_question": "After one closed local C8 instrumentation loop, what evidence is sufficient to keep the local discriminator and loop pattern non-reusable unless a later authority packet explicitly promotes them?",
        "probe_objective": "Expose whether post-closure reuse pressure is only a local review surface, or whether a missing explicit reuse-authority rule must be proposed.",
        "probe_inputs_required": [
            "c8_local_instrumentation_loop_closure_packet_v0",
            "c8_successor_frontier_surface_selection_packet_v0",
            "c8_successor_surface_selection_review_packet_v0",
            "c8_successor_surface_bounded_probe_prep_acceptance_packet_v0",
        ],
        "probe_output_classes": [
            "REUSE_BOUNDARY_HELD_NO_NEW_AUTHORITY_NEEDED",
            "MISSING_REUSE_AUTHORITY_RULE_EXPOSED",
            "SURFACE_TOO_BROAD_REQUIRES_NARROWING",
            "SOURCE_CONTEXT_MISSING_TYPED_STOP",
        ],
        "probe_must_not_claim": [
            "local_loop_pattern_is_reusable_schema",
            "local_discriminator_is_globally_authorized",
            "frontier_is_solved",
            "probe_result_authorizes_build",
            "probe_result_authorizes_rerun",
        ],
    }
    write_json(PROBE_SPEC, probe_spec)

    probe_constraints = {
        "schema_version": "c8_successor_surface_bounded_probe_constraints_v0",
        "probe_id": probe_id,
        "constraint_status": "BOUNDED_PREP_ONLY",
        "max_probe_surfaces": 1,
        "max_probe_questions": 1,
        "max_probe_execution_count_now": 0,
        "max_future_probe_execution_count_after_separate_acceptance": 1,
        "max_instrument_build_count": 0,
        "max_cell1_build_count": 0,
        "max_verification_probe_count": 0,
        "max_c8_rerun_count": 0,
        "max_missing_instrument_proposal_count_now": 0,
        "max_reusable_schema_authorization_count": 0,
        "requires_review_before_probe_execution": True,
        "recommended_review_unit": "REVIEW_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_V0",
        "authorized_now": {
            "probe_prep_packet_created": True,
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
    write_json(PROBE_CONSTRAINTS, probe_constraints)

    prep_packet = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_packet_v0",
        "prep_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "prep_status": "BOUNDED_PROBE_PREP_PACKET_CREATED_FOR_REVIEW",
        "source_acceptance_receipt_id": acceptance_receipt.get("receipt_id"),
        "source_acceptance_packet_id": acceptance_packet.get("acceptance_packet_id"),
        "source_acceptance_decision_id": acceptance_decision.get("acceptance_decision_id"),
        "source_authority_id": acceptance_authority.get("authority_id"),
        "selected_surface_id": summary.get("selected_surface_id"),
        "selected_surface_kind": summary.get("selected_surface_kind"),
        "selected_surface_label": summary.get("selected_surface_label"),
        "probe_id": probe_id,
        "probe_kind": probe_spec["probe_kind"],
        "probe_spec_ref": rel(PROBE_SPEC),
        "probe_constraints_ref": rel(PROBE_CONSTRAINTS),
        "prepared_for_review_only": True,
        "accepted_for_probe_execution_now": False,
        "probe_executed_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized_now": False,
        "recommended_review_unit": "REVIEW_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_V0",
        "recommended_review_unit_status": "REVIEW_REQUIRED_BEFORE_ANY_PROBE_EXECUTION",
    }
    prep_packet["prep_packet_id"] = "c8_successor_probe_prep_packet_" + sig8(prep_packet)
    write_json(PREP_PACKET, prep_packet)

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
        "C8_PROBE_PREP_PACKET_0_ACCEPTANCE_RECEIPT_VERIFIED": acceptance_receipt.get("gate") == "PASS",
        "C8_PROBE_PREP_PACKET_1_AUTHORIZED_FUTURE_UNIT_MATCHES": summary.get("authorized_future_unit") == UNIT_ID,
        "C8_PROBE_PREP_PACKET_2_AUTHORIZED_FUTURE_UNIT_COUNT_ONE": summary.get("authorized_future_unit_count") == 1,
        "C8_PROBE_PREP_PACKET_3_SELECTED_SURFACE_MATCHES": summary.get("selected_surface_id") == "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0",
        "C8_PROBE_PREP_PACKET_4_PROBE_SPEC_PREPARED_FOR_REVIEW_ONLY": probe_spec["probe_status"] == "PREPARED_FOR_REVIEW_ONLY",
        "C8_PROBE_PREP_PACKET_5_REVIEW_REQUIRED_BEFORE_PROBE_EXECUTION": probe_constraints["requires_review_before_probe_execution"] is True,
        "C8_PROBE_PREP_PACKET_6_NO_PROBE_EXECUTION_NOW": negative_controls["probe_execution_count"] == 0 and prep_packet["probe_executed_now"] is False,
        "C8_PROBE_PREP_PACKET_7_NO_BUILD_OR_RERUN_NOW": negative_controls["instrument_build_count"] == 0 and negative_controls["c8_rerun_count"] == 0,
        "C8_PROBE_PREP_PACKET_8_NO_REUSABLE_SCHEMA_AUTHORIZED": negative_controls["reusable_schema_authorized_count"] == 0 and prep_packet["reusable_schema_authorized_now"] is False,
        "C8_PROBE_PREP_PACKET_9_NO_RESEARCH_OR_GLOBAL_CLAIM": negative_controls["research_mode_opened_count"] == 0 and negative_controls["global_solution_claim_count"] == 0 and negative_controls["frontier_solved_claim_count"] == 0,
        "C8_PROBE_PREP_PACKET_10_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_PROBE_PREP_PACKET_11_BAD_COUNTERS_ZERO": not bool(nonzero),
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_PASS" if gate == "PASS" else "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_FAILED"

    boundary_audit = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_packet_boundary_audit_v0",
        "boundary_audit_id": None,
        "gate": gate,
        "selected_surface_id": summary.get("selected_surface_id"),
        "probe_id": probe_id,
        "prep_packet_created": True,
        "authority_boundary": {
            "may_review_prep_packet": True,
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
    boundary_audit["boundary_audit_id"] = "c8_successor_probe_prep_packet_boundary_" + sig8(boundary_audit)
    write_json(PREP_BOUNDARY_AUDIT, boundary_audit)

    readout = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_packet_readout_v0",
        "title": "C8 successor surface bounded probe-prep packet readout",
        "status": status,
        "outcome_class": outcome,
        "selected_surface_id": summary.get("selected_surface_id"),
        "selected_surface_kind": summary.get("selected_surface_kind"),
        "probe_id": probe_id,
        "probe_kind": probe_spec["probe_kind"],
        "prep_packet_id": prep_packet["prep_packet_id"],
        "prepared_for_review_only": True,
        "recommended_review_unit": prep_packet["recommended_review_unit"],
        "probe_executed_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized_now": False,
        "summary": "A bounded probe-prep packet has been created for review. It defines the reuse-authority boundary probe but does not execute it.",
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_successor_surface_bounded_probe_prep_packet_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "prep_packet_ref": rel(PREP_PACKET),
        "probe_spec_ref": rel(PROBE_SPEC),
        "probe_constraints_ref": rel(PROBE_CONSTRAINTS),
        "boundary_audit_ref": rel(PREP_BOUNDARY_AUDIT),
        "source_acceptance_receipt_id": acceptance_receipt.get("receipt_id"),
        "source_acceptance_packet_id": acceptance_packet.get("acceptance_packet_id"),
        "source_authority_id": acceptance_authority.get("authority_id"),
        "selected_surface_id": summary.get("selected_surface_id"),
        "selected_surface_kind": summary.get("selected_surface_kind"),
        "probe_id": probe_id,
        "prep_packet_id": prep_packet["prep_packet_id"],
        "prepared_for_review_only": True,
        "recommended_review_unit": prep_packet["recommended_review_unit"],
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
        "schema_version": "c8_successor_surface_bounded_probe_prep_packet_receipt_v0",
        "receipt_type": "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_PREP_PACKET_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_refs": {
            "acceptance_receipt_ref": rel(ACCEPTANCE_RECEIPT),
            "acceptance_packet_ref": rel(ACCEPTANCE_PACKET),
            "acceptance_decision_ref": rel(ACCEPTANCE_DECISION),
            "acceptance_authority_ref": rel(ACCEPTANCE_AUTHORITY),
            "acceptance_boundary_audit_ref": rel(ACCEPTANCE_BOUNDARY_AUDIT),
            "acceptance_report_ref": rel(ACCEPTANCE_REPORT),
        },
        "machine_readable_prep_summary": {
            "prep_complete": gate == "PASS",
            "source_acceptance_receipt_id": acceptance_receipt.get("receipt_id"),
            "source_acceptance_packet_id": acceptance_packet.get("acceptance_packet_id"),
            "source_acceptance_decision_id": acceptance_decision.get("acceptance_decision_id"),
            "source_authority_id": acceptance_authority.get("authority_id"),
            "selected_surface_id": summary.get("selected_surface_id"),
            "selected_surface_kind": summary.get("selected_surface_kind"),
            "selected_surface_label": summary.get("selected_surface_label"),
            "probe_id": probe_id,
            "probe_kind": probe_spec["probe_kind"],
            "prep_packet_id": prep_packet["prep_packet_id"],
            "prepared_for_review_only": True,
            "recommended_review_unit": prep_packet["recommended_review_unit"],
            "requires_review_before_probe_execution": True,
            "accepted_for_probe_execution_now": False,
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
            "prep_packet": rel(PREP_PACKET),
            "probe_spec": rel(PROBE_SPEC),
            "probe_constraints": rel(PROBE_CONSTRAINTS),
            "boundary_audit": rel(PREP_BOUNDARY_AUDIT),
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

    receipt["receipt_id"] = "c8_successor_probe_prep_packet_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"prep_receipt_id={receipt['receipt_id']}")
    print(f"prep_receipt_path={rel(receipt_path)}")
    print(f"prep_packet_path={rel(PREP_PACKET)}")
    print(f"probe_spec_path={rel(PROBE_SPEC)}")
    print(f"probe_constraints_path={rel(PROBE_CONSTRAINTS)}")
    print(f"selected_surface_id={summary.get('selected_surface_id')}")
    print(f"selected_surface_kind={summary.get('selected_surface_kind')}")
    print(f"probe_id={probe_id}")
    print(f"probe_kind={probe_spec['probe_kind']}")
    print(f"prep_packet_id={prep_packet['prep_packet_id']}")
    print(f"prepared_for_review_only=true")
    print(f"recommended_review_unit={prep_packet['recommended_review_unit']}")
    print(f"requires_review_before_probe_execution=true")
    print(f"probe_executed_now=false")
    print(f"new_instrument_build=false")
    print(f"new_c8_rerun=false")
    print(f"reusable_schema_authorized=false")
    print(f"prep_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
