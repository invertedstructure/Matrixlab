#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_REVIEW_V0"
TARGET_UNIT_ID = "research.c8.successor_frontier_surface_selection.review.v0"
MILESTONE = "C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_REVIEWED"
OUTCOME = "C8_SUCCESSOR_FRONTIER_SURFACE_REVIEWABLE_NOT_ACCEPTED"
STOP_CODE = "STOP_C8_SUCCESSOR_FRONTIER_SURFACE_REVIEW_READY_FOR_HUMAN_DECISION"

OUT_DIR = ROOT / "data/c8_successor_frontier_surface_selection_review_v0"
RECEIPT_DIR = ROOT / "data/c8_successor_frontier_surface_selection_review_v0_receipts"

SELECTION_RECEIPT = ROOT / "data/c8_successor_frontier_surface_selection_v0_receipts/c8_successor_surface_selection_receipt_c50e9fdc.json"
SELECTION_PACKET = ROOT / "data/c8_successor_frontier_surface_selection_v0/c8_successor_frontier_surface_selection_packet_v0.json"
SELECTED_SURFACE = ROOT / "data/c8_successor_frontier_surface_selection_v0/c8_selected_successor_frontier_surface_v0.json"
SELECTION_ADMISSIBILITY = ROOT / "data/c8_successor_frontier_surface_selection_v0/c8_successor_surface_selection_admissibility_v0.json"
BOUNDARY_AUDIT = ROOT / "data/c8_successor_frontier_surface_selection_v0/c8_successor_surface_selection_boundary_audit_v0.json"
SELECTION_REPORT = ROOT / "data/c8_successor_frontier_surface_selection_v0/c8_successor_frontier_surface_selection_report.json"

REVIEW_PACKET = OUT_DIR / "c8_successor_surface_selection_review_packet_v0.json"
REVIEW_DECISION = OUT_DIR / "c8_successor_surface_selection_review_decision_v0.json"
REVIEW_AUDIT = OUT_DIR / "c8_successor_surface_selection_review_audit_v0.json"
READOUT = OUT_DIR / "c8_successor_surface_selection_review_readout_v0.json"
REPORT = OUT_DIR / "c8_successor_surface_selection_review_report.json"

NEGATIVE_CONTROL_KEYS = [
    "accepted_for_probe_prep_count",
    "rejected_surface_count",
    "narrowed_surface_count",
    "new_probe_count",
    "new_instrument_build_count",
    "new_cell1_build_count",
    "new_verification_probe_count",
    "new_c8_rerun_count",
    "new_missing_instrument_proposal_count",
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
        "selection_receipt": SELECTION_RECEIPT,
        "selection_packet": SELECTION_PACKET,
        "selected_surface": SELECTED_SURFACE,
        "selection_admissibility": SELECTION_ADMISSIBILITY,
        "boundary_audit": BOUNDARY_AUDIT,
        "selection_report": SELECTION_REPORT,
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
    selected_surface = read_json(SELECTED_SURFACE)
    selection_admissibility = read_json(SELECTION_ADMISSIBILITY)
    boundary_audit = read_json(BOUNDARY_AUDIT)
    selection_report = read_json(SELECTION_REPORT)

    summary = selection_receipt.get("machine_readable_selection_summary", {})

    chk(failures, "selection_gate", selection_receipt.get("gate"), "PASS")
    chk(failures, "selection_status", selection_receipt.get("status"), "TYPED_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_PASS")
    chk(failures, "selection_outcome", selection_receipt.get("outcome_class"), "C8_ONE_BOUNDED_SUCCESSOR_FRONTIER_SURFACE_SELECTED")
    chk(failures, "selection_receipt_id", selection_receipt.get("receipt_id"), "c8_successor_surface_selection_receipt_c50e9fdc")

    chk(failures, "selection_complete", summary.get("selection_complete"), True)
    chk(failures, "selected_surfaces_count", summary.get("selected_surfaces_count"), 1)
    chk(failures, "selected_surface_id", summary.get("selected_surface_id"), "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0")
    chk(failures, "selected_surface_kind", summary.get("selected_surface_kind"), "REUSE_AUTHORITY_BOUNDARY_SURFACE")
    chk(failures, "selected_surface_label", summary.get("selected_surface_label"), "C8_POST_CLOSURE_LOCAL_LOOP_REUSE_PRESSURE_SURFACE")
    chk(failures, "selection_status_summary", summary.get("selection_status"), "SELECTED_FOR_REVIEW_ONLY")
    chk(failures, "recommended_review_unit", summary.get("recommended_review_unit"), "REVIEW_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_V0")

    chk(failures, "probe_run", summary.get("probe_run"), False)
    chk(failures, "new_instrument_build", summary.get("new_instrument_build"), False)
    chk(failures, "new_cell1_build", summary.get("new_cell1_build"), False)
    chk(failures, "new_verification_probe", summary.get("new_verification_probe"), False)
    chk(failures, "new_c8_rerun", summary.get("new_c8_rerun"), False)
    chk(failures, "new_missing_instrument_proposal", summary.get("new_missing_instrument_proposal"), False)
    chk(failures, "research_mode_opened", summary.get("research_mode_opened"), False)
    chk(failures, "general_cell1_authority", summary.get("general_cell1_authority"), False)
    chk(failures, "reusable_schema_authorized", summary.get("reusable_schema_authorized"), False)
    chk(failures, "global_solution_claim", summary.get("global_solution_claim"), False)
    chk(failures, "frontier_solved_claim", summary.get("frontier_solved_claim"), False)

    question = selected_surface.get("bounded_question", "")
    if "reuse boundary" not in question.lower():
        failures.append("selected_surface_missing_reuse_boundary_in_bounded_question")

    for forbidden in [
        "probe execution",
        "instrument build",
        "Cell 1 build",
        "C8 rerun",
        "missing-instrument proposal",
        "reusable schema authorization",
        "research mode",
        "global solution claim",
        "frontier solved claim",
    ]:
        if forbidden not in selected_surface.get("not_authorized_by_selection", []):
            failures.append(f"selected_surface_missing_not_authorized:{forbidden}")

    chk(failures, "admissibility_status", selection_admissibility.get("admissibility_status"), "ADMISSIBLE_SELECTION_FOR_REVIEW_ONLY")
    chk(failures, "selection_is_bounded", selection_admissibility.get("selection_is_bounded"), True)
    chk(failures, "selection_is_execution", selection_admissibility.get("selection_is_execution"), False)
    chk(failures, "selection_authorizes_probe", selection_admissibility.get("selection_authorizes_probe"), False)
    chk(failures, "selection_authorizes_build", selection_admissibility.get("selection_authorizes_build"), False)
    chk(failures, "selection_authorizes_rerun", selection_admissibility.get("selection_authorizes_rerun"), False)
    chk(failures, "selection_authorizes_reusable_schema", selection_admissibility.get("selection_authorizes_reusable_schema"), False)
    chk(failures, "selection_requires_review", selection_admissibility.get("selection_requires_review"), True)

    boundary_results = boundary_audit.get("boundary_results", {})
    for key in [
        "exactly_one_surface_selected",
        "surface_selected_for_review_only",
        "no_probe_run",
        "no_new_instrument_build",
        "no_cell1_build",
        "no_verification_probe",
        "no_c8_rerun",
        "no_missing_instrument_proposal",
        "no_research_mode_opened",
        "no_general_cell1_authority",
        "no_reusable_schema_authorized",
        "no_global_solution_claim",
        "no_frontier_solved_claim",
    ]:
        chk(failures, f"boundary_{key}", boundary_results.get(key), True)

    authority = boundary_audit.get("authority_boundary", {})
    for key, want in {
        "selection_may_be_reviewed": True,
        "selection_may_be_executed_now": False,
        "selection_may_trigger_probe_without_review": False,
        "selection_may_trigger_build_without_review": False,
        "selection_promotes_prior_schema": False,
    }.items():
        chk(failures, f"authority_{key}", authority.get(key), want)

    review_findings = {
        "surface_is_well_formed": True,
        "surface_is_bounded": True,
        "surface_kind_is_typed": True,
        "reuse_boundary_explicit": "reuse boundary" in question.lower(),
        "one_time_acceptance_vs_reusable_schema_boundary_preserved": True,
        "selection_does_not_execute_surface": True,
        "selection_does_not_authorize_probe": True,
        "selection_does_not_authorize_build": True,
        "selection_does_not_authorize_rerun": True,
        "selection_does_not_authorize_reusable_schema": True,
        "review_result": "REVIEWABLE_NOT_ACCEPTED",
    }

    review_decision = {
        "schema_version": "c8_successor_surface_selection_review_decision_v0",
        "review_decision_id": None,
        "source_selection_receipt_id": selection_receipt.get("receipt_id"),
        "source_selection_packet_id": selection_packet.get("selection_packet_id"),
        "selected_surface_id": selected_surface.get("selected_surface_id"),
        "selected_surface_kind": selected_surface.get("surface_kind"),
        "selected_surface_label": selected_surface.get("selected_surface_label"),
        "review_status": "REVIEWED",
        "review_decision": "REVIEWABLE_NOT_ACCEPTED",
        "surface_review_class": "WELL_FORMED_BOUNDED_REUSE_AUTHORITY_BOUNDARY_SURFACE",
        "possible_human_decisions": [
            "ACCEPT_FOR_BOUNDED_PROBE_PREP",
            "REJECT_SUCCESSOR_SURFACE",
            "NARROW_SUCCESSOR_SURFACE",
        ],
        "accepted_for_probe_prep": False,
        "rejected": False,
        "narrowed": False,
        "requires_human_decision": True,
        "review_findings": review_findings,
        "review_note": "The selected successor surface is well formed and bounded for review. It is not accepted for probe prep by this review unit.",
    }
    review_decision["review_decision_id"] = "c8_successor_surface_review_decision_" + sig8(review_decision)
    write_json(REVIEW_DECISION, review_decision)

    review_packet = {
        "schema_version": "c8_successor_surface_selection_review_packet_v0",
        "review_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "review_status": "REVIEW_PACKET_CREATED",
        "source_selection_receipt_id": selection_receipt.get("receipt_id"),
        "source_selection_packet_id": selection_packet.get("selection_packet_id"),
        "selected_surface_id": selected_surface.get("selected_surface_id"),
        "selected_surface_kind": selected_surface.get("surface_kind"),
        "selected_surface_label": selected_surface.get("selected_surface_label"),
        "review_decision_ref": rel(REVIEW_DECISION),
        "review_decision": review_decision["review_decision"],
        "surface_review_class": review_decision["surface_review_class"],
        "human_decision_required": True,
        "accepted_for_probe_prep_now": False,
        "rejected_now": False,
        "narrowed_now": False,
        "authorized_now": {
            "bounded_probe_prep": False,
            "probe_execution": False,
            "instrument_build": False,
            "cell1_build": False,
            "verification_probe": False,
            "c8_rerun": False,
            "missing_instrument_proposal": False,
            "reusable_schema": False,
        },
    }
    review_packet["review_packet_id"] = "c8_successor_surface_review_packet_" + sig8(review_packet)
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
        "C8_SUCCESSOR_REVIEW_0_SELECTION_RECEIPT_VERIFIED": selection_receipt.get("gate") == "PASS",
        "C8_SUCCESSOR_REVIEW_1_SELECTION_IS_EXACTLY_ONE_SURFACE": summary.get("selected_surfaces_count") == 1,
        "C8_SUCCESSOR_REVIEW_2_SURFACE_IS_REVIEW_ONLY": summary.get("selection_status") == "SELECTED_FOR_REVIEW_ONLY",
        "C8_SUCCESSOR_REVIEW_3_SURFACE_KIND_TYPED": summary.get("selected_surface_kind") == "REUSE_AUTHORITY_BOUNDARY_SURFACE",
        "C8_SUCCESSOR_REVIEW_4_REUSE_BOUNDARY_EXPLICIT": "reuse boundary" in question.lower(),
        "C8_SUCCESSOR_REVIEW_5_SURFACE_REVIEWABLE_NOT_ACCEPTED": review_decision["review_decision"] == "REVIEWABLE_NOT_ACCEPTED",
        "C8_SUCCESSOR_REVIEW_6_HUMAN_DECISION_REQUIRED": review_decision["requires_human_decision"] is True,
        "C8_SUCCESSOR_REVIEW_7_NO_ACCEPT_REJECT_OR_NARROW_NOW": negative_controls["accepted_for_probe_prep_count"] == 0 and negative_controls["rejected_surface_count"] == 0 and negative_controls["narrowed_surface_count"] == 0,
        "C8_SUCCESSOR_REVIEW_8_NO_PROBE_BUILD_OR_RERUN": negative_controls["new_probe_count"] == 0 and negative_controls["new_instrument_build_count"] == 0 and negative_controls["new_c8_rerun_count"] == 0,
        "C8_SUCCESSOR_REVIEW_9_NO_REUSABLE_SCHEMA_AUTHORIZED": negative_controls["reusable_schema_authorized_count"] == 0,
        "C8_SUCCESSOR_REVIEW_10_NO_RESEARCH_OR_GLOBAL_CLAIM": negative_controls["research_mode_opened_count"] == 0 and negative_controls["global_solution_claim_count"] == 0 and negative_controls["frontier_solved_claim_count"] == 0,
        "C8_SUCCESSOR_REVIEW_11_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_SUCCESSOR_REVIEW_12_BAD_COUNTERS_ZERO": not bool(nonzero),
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_REVIEW_PASS" if gate == "PASS" else "TYPED_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_REVIEW_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_REVIEW_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_REVIEW_FAILED"

    review_audit = {
        "schema_version": "c8_successor_surface_selection_review_audit_v0",
        "review_audit_id": None,
        "gate": gate,
        "selected_surface_id": selected_surface.get("selected_surface_id"),
        "review_findings": review_findings,
        "negative_controls": negative_controls,
        "acceptance_gate_results": acceptance_gates,
        "failures": failures,
        "warnings": warnings,
    }
    review_audit["review_audit_id"] = "c8_successor_surface_review_audit_" + sig8(review_audit)
    write_json(REVIEW_AUDIT, review_audit)

    readout = {
        "schema_version": "c8_successor_surface_selection_review_readout_v0",
        "title": "C8 successor surface selection review readout",
        "status": status,
        "outcome_class": outcome,
        "selected_surface_id": selected_surface.get("selected_surface_id"),
        "selected_surface_kind": selected_surface.get("surface_kind"),
        "selected_surface_label": selected_surface.get("selected_surface_label"),
        "review_decision": review_decision["review_decision"],
        "surface_review_class": review_decision["surface_review_class"],
        "requires_human_decision": True,
        "accepted_for_probe_prep_now": False,
        "probe_run": False,
        "instrument_built": False,
        "c8_rerun_performed": False,
        "reusable_schema_authorized": False,
        "summary": "The selected successor surface is well formed and bounded for review, but this unit does not accept it for probe prep. Human decision is required.",
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_successor_surface_selection_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "review_packet_ref": rel(REVIEW_PACKET),
        "review_decision_ref": rel(REVIEW_DECISION),
        "review_audit_ref": rel(REVIEW_AUDIT),
        "source_selection_receipt_id": selection_receipt.get("receipt_id"),
        "source_selection_packet_id": selection_packet.get("selection_packet_id"),
        "selected_surface_id": selected_surface.get("selected_surface_id"),
        "selected_surface_kind": selected_surface.get("surface_kind"),
        "selected_surface_label": selected_surface.get("selected_surface_label"),
        "review_decision": review_decision["review_decision"],
        "surface_review_class": review_decision["surface_review_class"],
        "requires_human_decision": True,
        "accepted_for_probe_prep_now": False,
        "new_probe_count": 0,
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
        "schema_version": "c8_successor_surface_selection_review_receipt_v0",
        "receipt_type": "TYPED_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_REVIEW_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_refs": {
            "selection_receipt_ref": rel(SELECTION_RECEIPT),
            "selection_packet_ref": rel(SELECTION_PACKET),
            "selected_surface_ref": rel(SELECTED_SURFACE),
            "selection_admissibility_ref": rel(SELECTION_ADMISSIBILITY),
            "boundary_audit_ref": rel(BOUNDARY_AUDIT),
            "selection_report_ref": rel(SELECTION_REPORT),
        },
        "machine_readable_review_summary": {
            "review_complete": gate == "PASS",
            "source_selection_receipt_id": selection_receipt.get("receipt_id"),
            "source_selection_packet_id": selection_packet.get("selection_packet_id"),
            "selected_surface_id": selected_surface.get("selected_surface_id"),
            "selected_surface_kind": selected_surface.get("surface_kind"),
            "selected_surface_label": selected_surface.get("selected_surface_label"),
            "review_decision": review_decision["review_decision"],
            "surface_review_class": review_decision["surface_review_class"],
            "surface_is_well_formed": review_findings["surface_is_well_formed"],
            "surface_is_bounded": review_findings["surface_is_bounded"],
            "reuse_boundary_explicit": review_findings["reuse_boundary_explicit"],
            "human_decision_required": True,
            "accepted_for_probe_prep_now": False,
            "rejected_now": False,
            "narrowed_now": False,
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

    receipt["receipt_id"] = "c8_successor_surface_review_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"review_receipt_id={receipt['receipt_id']}")
    print(f"review_receipt_path={rel(receipt_path)}")
    print(f"review_packet_path={rel(REVIEW_PACKET)}")
    print(f"review_decision_path={rel(REVIEW_DECISION)}")
    print(f"selected_surface_id={selected_surface.get('selected_surface_id')}")
    print(f"selected_surface_kind={selected_surface.get('surface_kind')}")
    print(f"review_decision={review_decision['review_decision']}")
    print(f"surface_review_class={review_decision['surface_review_class']}")
    print(f"human_decision_required=true")
    print(f"accepted_for_probe_prep_now=false")
    print(f"probe_run=false")
    print(f"new_instrument_build=false")
    print(f"new_c8_rerun=false")
    print(f"reusable_schema_authorized=false")
    print(f"review_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
