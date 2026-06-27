#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "SELECT_ONE_BOUNDED_C8_SUCCESSOR_FRONTIER_SURFACE_V0"
TARGET_UNIT_ID = "research.c8.successor_frontier_surface_selection.v0"
MILESTONE = "C8_SUCCESSOR_FRONTIER_SURFACE_SELECTED_FOR_REVIEW"
OUTCOME = "C8_ONE_BOUNDED_SUCCESSOR_FRONTIER_SURFACE_SELECTED"
STOP_CODE = "STOP_C8_ONE_SUCCESSOR_SURFACE_SELECTED_FOR_REVIEW"

OUT_DIR = ROOT / "data/c8_successor_frontier_surface_selection_v0"
RECEIPT_DIR = ROOT / "data/c8_successor_frontier_surface_selection_v0_receipts"

CONTINUATION_RECEIPT = ROOT / "data/c8_post_closure_continuation_decision_v0_receipts/c8_post_closure_continuation_receipt_c2bcd85c.json"
CONTINUATION_PACKET = ROOT / "data/c8_post_closure_continuation_decision_v0/c8_post_closure_continuation_decision_packet_v0.json"
ADMISSIBILITY_AUDIT = ROOT / "data/c8_post_closure_continuation_decision_v0/c8_post_closure_admissibility_audit_v0.json"
NEXT_UNIT_CANDIDATE = ROOT / "data/c8_post_closure_continuation_decision_v0/c8_post_closure_next_unit_candidate_v0.json"
CONTINUATION_REPORT = ROOT / "data/c8_post_closure_continuation_decision_v0/c8_post_closure_continuation_decision_report.json"

SELECTION_PACKET = OUT_DIR / "c8_successor_frontier_surface_selection_packet_v0.json"
SELECTED_SURFACE = OUT_DIR / "c8_selected_successor_frontier_surface_v0.json"
SELECTION_ADMISSIBILITY = OUT_DIR / "c8_successor_surface_selection_admissibility_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_successor_surface_selection_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_successor_frontier_surface_selection_readout_v0.json"
REPORT = OUT_DIR / "c8_successor_frontier_surface_selection_report.json"

NEGATIVE_CONTROL_KEYS = [
    "surfaces_selected_over_budget_count",
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
        "continuation_receipt": CONTINUATION_RECEIPT,
        "continuation_packet": CONTINUATION_PACKET,
        "admissibility_audit": ADMISSIBILITY_AUDIT,
        "next_unit_candidate": NEXT_UNIT_CANDIDATE,
        "continuation_report": CONTINUATION_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    continuation_receipt = read_json(CONTINUATION_RECEIPT)
    continuation_packet = read_json(CONTINUATION_PACKET)
    admissibility_audit = read_json(ADMISSIBILITY_AUDIT)
    next_candidate = read_json(NEXT_UNIT_CANDIDATE)
    continuation_report = read_json(CONTINUATION_REPORT)

    summary = continuation_receipt.get("machine_readable_continuation_summary", {})

    chk(failures, "continuation_gate", continuation_receipt.get("gate"), "PASS")
    chk(failures, "continuation_status", continuation_receipt.get("status"), "TYPED_C8_POST_CLOSURE_CONTINUATION_DECISION_PASS")
    chk(failures, "continuation_outcome", continuation_receipt.get("outcome_class"), "C8_POST_CLOSURE_CONTINUATION_DECISION_PACKET_CREATED")
    chk(failures, "continuation_receipt_id", continuation_receipt.get("receipt_id"), "c8_post_closure_continuation_receipt_c2bcd85c")

    chk(failures, "source_local_loop_closed", summary.get("local_loop_closed"), True)
    chk(failures, "source_global_frontier_closed", summary.get("global_frontier_closed"), False)
    chk(failures, "source_recommended_next_unit", summary.get("recommended_next_unit"), "SELECT_ONE_BOUNDED_C8_SUCCESSOR_FRONTIER_SURFACE_V0")
    chk(failures, "source_next_unit_kind", summary.get("recommended_next_unit_kind"), "SELECTION_REVIEW_PACKET")
    chk(failures, "source_next_unit_status", summary.get("recommended_next_unit_status"), "PROPOSED_ONLY_REQUIRES_REVIEW")
    chk(failures, "source_new_frontier_selected_now", summary.get("new_frontier_selected_now"), False)
    chk(failures, "source_new_build_now", summary.get("new_instrument_build_now"), False)
    chk(failures, "source_new_rerun_now", summary.get("new_c8_rerun_now"), False)
    chk(failures, "source_reusable_schema_authorized", summary.get("reusable_schema_authorized"), False)
    chk(failures, "source_global_solution_claim", summary.get("global_solution_claim"), False)
    chk(failures, "source_frontier_solved_claim", summary.get("frontier_solved_claim"), False)

    chk(failures, "packet_recommended_next_unit", continuation_packet.get("recommended_next_unit"), "SELECT_ONE_BOUNDED_C8_SUCCESSOR_FRONTIER_SURFACE_V0")
    chk(failures, "packet_status", continuation_packet.get("recommended_next_unit_status"), "PROPOSED_ONLY_REQUIRES_REVIEW")
    chk(failures, "audit_family", admissibility_audit.get("admissible_next_unit_family"), "BOUNDED_NEXT_FRONTIER_SURFACE_SELECTION_OR_CONTINUATION_REVIEW")
    chk(failures, "candidate_status", next_candidate.get("candidate_status"), "PROPOSED_ONLY")
    chk(failures, "candidate_recommended_unit", next_candidate.get("recommended_next_unit"), "SELECT_ONE_BOUNDED_C8_SUCCESSOR_FRONTIER_SURFACE_V0")
    chk(failures, "candidate_authorized_now", next_candidate.get("authorized_now"), False)
    chk(failures, "candidate_requires_human_review", next_candidate.get("requires_human_review"), True)
    chk(failures, "candidate_max_surfaces", next_candidate.get("max_frontier_surfaces_to_select"), 1)
    chk(failures, "candidate_max_new_probes", next_candidate.get("max_new_probes"), 0)
    chk(failures, "candidate_max_new_builds", next_candidate.get("max_new_builds"), 0)
    chk(failures, "candidate_max_new_reruns", next_candidate.get("max_new_c8_reruns"), 0)

    selected_surface = {
        "schema_version": "c8_selected_successor_frontier_surface_v0",
        "selected_surface_id": "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0",
        "selected_surface_label": "C8_POST_CLOSURE_LOCAL_LOOP_REUSE_PRESSURE_SURFACE",
        "surface_kind": "REUSE_AUTHORITY_BOUNDARY_SURFACE",
        "selection_status": "SELECTED_FOR_REVIEW_ONLY",
        "source_continuation_receipt_id": continuation_receipt.get("receipt_id"),
        "source_continuation_packet_id": continuation_packet.get("continuation_packet_id"),
        "source_candidate_id": next_candidate.get("candidate_id"),
        "selection_basis": [
            "The local C8 branch closed successfully.",
            "The closure created pressure to continue, reuse, or generalize the branch pattern.",
            "The continuation packet explicitly did not authorize reusable schema, new frontier execution, new build, or rerun.",
            "Therefore the smallest successor surface is the authority boundary around reuse/continuation after one closed local loop.",
        ],
        "bounded_question": "After one closed local C8 instrumentation loop, what exactly may be selected or reviewed next at the reuse boundary without treating the local discriminator or loop pattern as reusable authority?",
        "allowed_next_review_questions": [
            "Is this successor surface well formed?",
            "Is this successor surface bounded enough for one probe-prep packet?",
            "Does selecting this surface preserve the one-time acceptance versus reusable-schema boundary?",
            "Should this surface be accepted for bounded probe prep, rejected, or narrowed?",
        ],
        "not_authorized_by_selection": [
            "probe execution",
            "instrument build",
            "Cell 1 build",
            "C8 rerun",
            "missing-instrument proposal",
            "reusable schema authorization",
            "research mode",
            "global solution claim",
            "frontier solved claim",
        ],
    }
    write_json(SELECTED_SURFACE, selected_surface)

    selected_surfaces_count = 1
    if selected_surfaces_count > 1:
        negative_controls["surfaces_selected_over_budget_count"] += selected_surfaces_count - 1

    selection_admissibility = {
        "schema_version": "c8_successor_surface_selection_admissibility_v0",
        "admissibility_id": None,
        "source_continuation_receipt_id": continuation_receipt.get("receipt_id"),
        "selected_surface_id": selected_surface["selected_surface_id"],
        "selection_count": selected_surfaces_count,
        "max_selection_count": 1,
        "admissibility_status": "ADMISSIBLE_SELECTION_FOR_REVIEW_ONLY",
        "selection_is_bounded": True,
        "selection_is_execution": False,
        "selection_authorizes_probe": False,
        "selection_authorizes_build": False,
        "selection_authorizes_rerun": False,
        "selection_authorizes_reusable_schema": False,
        "selection_requires_review": True,
        "reason": "The selected surface is a review target around continuation/reuse authority after local closure. It does not execute the successor surface.",
    }
    selection_admissibility["admissibility_id"] = "c8_successor_selection_admissibility_" + sig8(selection_admissibility)
    write_json(SELECTION_ADMISSIBILITY, selection_admissibility)

    boundary_audit = {
        "schema_version": "c8_successor_surface_selection_boundary_audit_v0",
        "audit_id": None,
        "selected_surface_id": selected_surface["selected_surface_id"],
        "boundary_results": {
            "exactly_one_surface_selected": selected_surfaces_count == 1,
            "surface_selected_for_review_only": True,
            "no_probe_run": True,
            "no_new_instrument_build": True,
            "no_cell1_build": True,
            "no_verification_probe": True,
            "no_c8_rerun": True,
            "no_missing_instrument_proposal": True,
            "no_research_mode_opened": True,
            "no_general_cell1_authority": True,
            "no_reusable_schema_authorized": True,
            "no_global_solution_claim": True,
            "no_frontier_solved_claim": True,
        },
        "authority_boundary": {
            "selection_may_be_reviewed": True,
            "selection_may_be_executed_now": False,
            "selection_may_trigger_probe_without_review": False,
            "selection_may_trigger_build_without_review": False,
            "selection_promotes_prior_schema": False,
        },
    }
    boundary_audit["audit_id"] = "c8_successor_surface_boundary_audit_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    selection_packet = {
        "schema_version": "c8_successor_frontier_surface_selection_packet_v0",
        "selection_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "selection_status": "ONE_BOUNDED_SUCCESSOR_SURFACE_SELECTED_FOR_REVIEW",
        "source_continuation_receipt_id": continuation_receipt.get("receipt_id"),
        "source_continuation_packet_id": continuation_packet.get("continuation_packet_id"),
        "source_next_unit_candidate_id": next_candidate.get("candidate_id"),
        "selected_surface_ref": rel(SELECTED_SURFACE),
        "selected_surface_id": selected_surface["selected_surface_id"],
        "selected_surface_kind": selected_surface["surface_kind"],
        "selected_surface_label": selected_surface["selected_surface_label"],
        "selected_surfaces_count": selected_surfaces_count,
        "max_selected_surfaces": 1,
        "review_required": True,
        "authorized_now": {
            "surface_selected_for_review": True,
            "probe_execution": False,
            "instrument_build": False,
            "cell1_build": False,
            "verification_probe": False,
            "c8_rerun": False,
            "new_missing_instrument_proposal": False,
            "reusable_schema": False,
        },
        "recommended_review_unit": "REVIEW_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_V0",
        "possible_review_outcomes": [
            "ACCEPT_FOR_BOUNDED_PROBE_PREP",
            "REJECT_SUCCESSOR_SURFACE",
            "NARROW_SUCCESSOR_SURFACE",
        ],
    }
    selection_packet["selection_packet_id"] = "c8_successor_surface_selection_" + sig8(selection_packet)
    write_json(SELECTION_PACKET, selection_packet)

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
        "C8_SUCCESSOR_SELECTION_0_SOURCE_CONTINUATION_VERIFIED": continuation_receipt.get("gate") == "PASS",
        "C8_SUCCESSOR_SELECTION_1_RECOMMENDED_UNIT_MATCHES": summary.get("recommended_next_unit") == UNIT_ID,
        "C8_SUCCESSOR_SELECTION_2_EXACTLY_ONE_SURFACE_SELECTED": selected_surfaces_count == 1,
        "C8_SUCCESSOR_SELECTION_3_SURFACE_SELECTED_FOR_REVIEW_ONLY": selected_surface["selection_status"] == "SELECTED_FOR_REVIEW_ONLY",
        "C8_SUCCESSOR_SELECTION_4_SELECTED_SURFACE_KIND_TYPED": selected_surface["surface_kind"] == "REUSE_AUTHORITY_BOUNDARY_SURFACE",
        "C8_SUCCESSOR_SELECTION_5_NO_PROBE_BUILD_OR_RERUN": negative_controls["new_probe_count"] == 0 and negative_controls["new_instrument_build_count"] == 0 and negative_controls["new_c8_rerun_count"] == 0,
        "C8_SUCCESSOR_SELECTION_6_NO_REUSABLE_SCHEMA_AUTHORIZED": negative_controls["reusable_schema_authorized_count"] == 0,
        "C8_SUCCESSOR_SELECTION_7_NO_RESEARCH_OR_GLOBAL_CLAIM": negative_controls["research_mode_opened_count"] == 0 and negative_controls["global_solution_claim_count"] == 0 and negative_controls["frontier_solved_claim_count"] == 0,
        "C8_SUCCESSOR_SELECTION_8_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_SUCCESSOR_SELECTION_9_BAD_COUNTERS_ZERO": not bool(nonzero),
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_PASS" if gate == "PASS" else "TYPED_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_FAILED"

    readout = {
        "schema_version": "c8_successor_frontier_surface_selection_readout_v0",
        "title": "C8 successor frontier surface selection readout",
        "status": status,
        "outcome_class": outcome,
        "selected_surface_id": selected_surface["selected_surface_id"],
        "selected_surface_kind": selected_surface["surface_kind"],
        "selected_surface_label": selected_surface["selected_surface_label"],
        "selected_surfaces_count": selected_surfaces_count,
        "selection_status": "SELECTED_FOR_REVIEW_ONLY",
        "recommended_review_unit": "REVIEW_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_V0",
        "probe_run": False,
        "instrument_built": False,
        "c8_rerun_performed": False,
        "reusable_schema_authorized": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "summary": "Exactly one successor frontier surface was selected for review: the reuse/continuation authority boundary created by closing one local C8 loop. No execution authority is granted.",
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_successor_frontier_surface_selection_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "selection_packet_ref": rel(SELECTION_PACKET),
        "selected_surface_ref": rel(SELECTED_SURFACE),
        "selection_admissibility_ref": rel(SELECTION_ADMISSIBILITY),
        "boundary_audit_ref": rel(BOUNDARY_AUDIT),
        "selected_surface_id": selected_surface["selected_surface_id"],
        "selected_surface_kind": selected_surface["surface_kind"],
        "selected_surface_label": selected_surface["selected_surface_label"],
        "selected_surfaces_count": selected_surfaces_count,
        "selection_status": "SELECTED_FOR_REVIEW_ONLY",
        "recommended_review_unit": "REVIEW_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_V0",
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
        "schema_version": "c8_successor_frontier_surface_selection_receipt_v0",
        "receipt_type": "TYPED_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_refs": {
            "continuation_receipt_ref": rel(CONTINUATION_RECEIPT),
            "continuation_packet_ref": rel(CONTINUATION_PACKET),
            "admissibility_audit_ref": rel(ADMISSIBILITY_AUDIT),
            "next_unit_candidate_ref": rel(NEXT_UNIT_CANDIDATE),
            "continuation_report_ref": rel(CONTINUATION_REPORT),
        },
        "machine_readable_selection_summary": {
            "selection_complete": gate == "PASS",
            "source_continuation_receipt_id": continuation_receipt.get("receipt_id"),
            "source_continuation_packet_id": continuation_packet.get("continuation_packet_id"),
            "source_candidate_id": next_candidate.get("candidate_id"),
            "selected_surfaces_count": selected_surfaces_count,
            "selected_surface_id": selected_surface["selected_surface_id"],
            "selected_surface_kind": selected_surface["surface_kind"],
            "selected_surface_label": selected_surface["selected_surface_label"],
            "selection_status": "SELECTED_FOR_REVIEW_ONLY",
            "recommended_review_unit": "REVIEW_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_V0",
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
            "selection_packet": rel(SELECTION_PACKET),
            "selected_surface": rel(SELECTED_SURFACE),
            "selection_admissibility": rel(SELECTION_ADMISSIBILITY),
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
    print(f"selection_receipt_id={receipt['receipt_id']}")
    print(f"selection_receipt_path={rel(receipt_path)}")
    print(f"selection_packet_path={rel(SELECTION_PACKET)}")
    print(f"selected_surface_path={rel(SELECTED_SURFACE)}")
    print(f"selected_surface_id={selected_surface['selected_surface_id']}")
    print(f"selected_surface_kind={selected_surface['surface_kind']}")
    print(f"selected_surface_label={selected_surface['selected_surface_label']}")
    print(f"selection_status=SELECTED_FOR_REVIEW_ONLY")
    print(f"recommended_review_unit=REVIEW_C8_SUCCESSOR_FRONTIER_SURFACE_SELECTION_V0")
    print(f"probe_run=false")
    print(f"new_instrument_build=false")
    print(f"new_c8_rerun=false")
    print(f"reusable_schema_authorized=false")
    print(f"selection_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
