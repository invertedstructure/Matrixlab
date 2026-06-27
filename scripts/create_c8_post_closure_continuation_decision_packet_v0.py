#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_POST_CLOSURE_CONTINUATION_DECISION_PACKET_V0"
TARGET_UNIT_ID = "research.c8.post_closure_continuation_decision.v0"
MILESTONE = "C8_POST_CLOSURE_CONTINUATION_DECISION_READY"
OUTCOME = "C8_POST_CLOSURE_CONTINUATION_DECISION_PACKET_CREATED"
STOP_CODE = "STOP_C8_POST_CLOSURE_CONTINUATION_DECISION_READY"

OUT_DIR = ROOT / "data/c8_post_closure_continuation_decision_v0"
RECEIPT_DIR = ROOT / "data/c8_post_closure_continuation_decision_v0_receipts"

CLOSURE_RECEIPT = ROOT / "data/c8_local_instrumentation_loop_closure_v0_receipts/c8_local_loop_closure_receipt_cce65018.json"
CLOSURE_PACKET = ROOT / "data/c8_local_instrumentation_loop_closure_v0/c8_local_instrumentation_loop_closure_packet_v0.json"
CLOSURE_TIMELINE = ROOT / "data/c8_local_instrumentation_loop_closure_v0/c8_local_instrumentation_loop_timeline_v0.json"
CLOSURE_BOUNDARY_AUDIT = ROOT / "data/c8_local_instrumentation_loop_closure_v0/c8_local_instrumentation_loop_boundary_audit_v0.json"
CLOSURE_REPORT = ROOT / "data/c8_local_instrumentation_loop_closure_v0/c8_local_instrumentation_loop_closure_report.json"

CONTINUATION_PACKET = OUT_DIR / "c8_post_closure_continuation_decision_packet_v0.json"
ADMISSIBILITY_AUDIT = OUT_DIR / "c8_post_closure_admissibility_audit_v0.json"
NEXT_UNIT_CANDIDATE = OUT_DIR / "c8_post_closure_next_unit_candidate_v0.json"
READOUT = OUT_DIR / "c8_post_closure_continuation_decision_readout_v0.json"
REPORT = OUT_DIR / "c8_post_closure_continuation_decision_report.json"

NEGATIVE_CONTROL_KEYS = [
    "new_frontier_selected_count",
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
        "closure_receipt": CLOSURE_RECEIPT,
        "closure_packet": CLOSURE_PACKET,
        "closure_timeline": CLOSURE_TIMELINE,
        "closure_boundary_audit": CLOSURE_BOUNDARY_AUDIT,
        "closure_report": CLOSURE_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    closure_receipt = read_json(CLOSURE_RECEIPT)
    closure_packet = read_json(CLOSURE_PACKET)
    timeline = read_json(CLOSURE_TIMELINE)
    boundary_audit = read_json(CLOSURE_BOUNDARY_AUDIT)
    closure_report = read_json(CLOSURE_REPORT)

    summary = closure_receipt.get("machine_readable_closure_summary", {})
    final_local = boundary_audit.get("final_local_status", {})
    boundaries = boundary_audit.get("chain_boundaries_preserved", {})
    new_work = boundary_audit.get("new_work_performed_in_closure_unit", {})

    chk(failures, "closure_gate", closure_receipt.get("gate"), "PASS")
    chk(failures, "closure_status", closure_receipt.get("status"), "TYPED_C8_LOCAL_INSTRUMENTATION_LOOP_CLOSURE_PASS")
    chk(failures, "closure_outcome", closure_receipt.get("outcome_class"), "C8_LOCAL_INSTRUMENTATION_LOOP_CLOSED")
    chk(failures, "closure_receipt_id", closure_receipt.get("receipt_id"), "c8_local_loop_closure_receipt_cce65018")

    chk(failures, "closure_complete", summary.get("closure_complete"), True)
    chk(failures, "local_loop_closed", summary.get("local_loop_closed"), True)
    chk(failures, "closure_kind", summary.get("closure_kind"), "LOCAL_C8_BRANCH_INSTRUMENTATION_CLOSURE")
    chk(failures, "proposal_id", summary.get("proposal_id"), "missing_instrument_d56acf49")
    chk(failures, "accepted_build_packet_id", summary.get("accepted_build_packet_id"), "accepted_instrument_build_packet_2e67943c")
    chk(failures, "instrument_id", summary.get("instrument_id"), "local_transition_family_discriminator_2deb5cd1")
    chk(failures, "final_rerun_classification", summary.get("final_rerun_classification"), "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED")
    chk(failures, "missing_instrument_status_after_rerun", summary.get("missing_instrument_status_after_rerun"), "LOCALLY_INSTRUMENTED_FOR_THIS_SURFACE")
    chk(failures, "chain_steps_closed", summary.get("chain_steps_closed"), 6)
    chk(failures, "global_solution_claim", summary.get("global_solution_claim"), False)
    chk(failures, "frontier_solved_claim", summary.get("frontier_solved_claim"), False)
    chk(failures, "general_cell1_authority", summary.get("general_cell1_authority"), False)

    steps = timeline.get("steps", [])
    if len(steps) != 6:
        failures.append(f"timeline_step_count_wrong:{len(steps)}")

    expected_milestones = [
        "C8_BASIC_RESEARCH_LOOP_SPECIMEN",
        "C8_MISSING_INSTRUMENT_PROPOSAL_REVIEWED",
        "C8_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP_ACCEPTED",
        "C8_ACCEPTED_INSTRUMENT_BUILD_PACKET_CREATED",
        "C8_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_BUILT",
        "C8_RERUN_WITH_LOCAL_DISCRIMINATOR_COMPLETE",
    ]
    observed_milestones = [x.get("milestone") for x in steps]
    if observed_milestones != expected_milestones:
        failures.append(f"timeline_milestones_wrong:{observed_milestones}")

    for key, want in {
        "local_loop_closed": True,
        "global_frontier_closed": False,
        "rerun_classification": "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED",
        "missing_instrument_status_after_rerun": "LOCALLY_INSTRUMENTED_FOR_THIS_SURFACE",
    }.items():
        chk(failures, f"final_local_{key}", final_local.get(key), want)

    for key in [
        "proposal_did_not_self_accept",
        "accepted_packet_preceded_build",
        "build_preceded_rerun",
        "local_verification_preceded_rerun",
        "only_one_bounded_instrument_build",
        "only_one_bounded_c8_rerun",
        "global_solution_not_claimed",
        "frontier_solved_not_claimed",
        "general_cell1_authority_not_created",
        "source_artifacts_not_mutated",
    ]:
        chk(failures, f"boundary_{key}", boundaries.get(key), True)

    for key in [
        "new_instrument_build",
        "new_cell1_build",
        "new_verification_probe",
        "new_c8_rerun",
        "new_missing_instrument_proposal",
        "research_mode_opened",
    ]:
        chk(failures, f"closure_new_work_{key}", new_work.get(key), False)

    admissibility_audit = {
        "schema_version": "c8_post_closure_admissibility_audit_v0",
        "audit_id": None,
        "source_closure_receipt_id": closure_receipt.get("receipt_id"),
        "local_loop_closed": True,
        "global_frontier_closed": False,
        "reusable_schema_authorized": False,
        "continuation_basis": [
            "The local missing-instrument branch is sealed.",
            "The result is local instrumentation, not a global frontier solution.",
            "No further automatic build, rerun, schema promotion, or research-mode opening is authorized by closure.",
            "The next lawful continuation must be a bounded selection/review unit, not direct expansion.",
        ],
        "admissible_next_unit_family": "BOUNDED_NEXT_FRONTIER_SURFACE_SELECTION_OR_CONTINUATION_REVIEW",
        "not_admissible_without_new_acceptance": [
            "reuse discriminator as general schema",
            "run new C8 branch automatically",
            "build another Cell 1 instrument",
            "claim global frontier closure",
            "open unbounded research mode",
        ],
        "negative_controls_expected_zero": list(NEGATIVE_CONTROL_KEYS),
    }
    admissibility_audit["audit_id"] = "c8_post_closure_admissibility_audit_" + sig8(admissibility_audit)
    write_json(ADMISSIBILITY_AUDIT, admissibility_audit)

    next_unit_candidate = {
        "schema_version": "c8_post_closure_next_unit_candidate_v0",
        "candidate_id": None,
        "candidate_status": "PROPOSED_ONLY",
        "recommended_next_unit": "SELECT_ONE_BOUNDED_C8_SUCCESSOR_FRONTIER_SURFACE_V0",
        "recommended_next_unit_kind": "SELECTION_REVIEW_PACKET",
        "why_this_is_next": "The closed local C8 branch proves the branch machinery can complete once, but does not authorize automatic reuse or expansion. The next smallest lawful unit is to select exactly one successor frontier surface, or halt if none is admissible.",
        "authorized_now": False,
        "requires_human_review": True,
        "max_frontier_surfaces_to_select": 1,
        "max_new_probes": 0,
        "max_new_builds": 0,
        "max_new_c8_reruns": 0,
        "expected_terminal_after_next_unit": [
            "STOP_NO_ADMISSIBLE_SUCCESSOR_SURFACE",
            "STOP_ONE_SUCCESSOR_SURFACE_SELECTED_FOR_REVIEW",
        ],
        "must_not_infer": [
            "the discriminator is reusable",
            "a second C8 run is authorized",
            "a new instrument build is authorized",
            "the frontier is globally solved",
            "the loop pattern is promoted to general runtime law",
        ],
    }
    next_unit_candidate["candidate_id"] = "c8_successor_surface_selection_candidate_" + sig8(next_unit_candidate)
    write_json(NEXT_UNIT_CANDIDATE, next_unit_candidate)

    continuation_packet = {
        "schema_version": "c8_post_closure_continuation_decision_packet_v0",
        "continuation_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "source_closure_receipt_id": closure_receipt.get("receipt_id"),
        "source_closure_packet_id": closure_packet.get("closure_packet_id"),
        "decision_status": "CONTINUATION_PACKET_CREATED",
        "local_loop_closed": True,
        "global_frontier_closed": False,
        "next_unit_candidate_ref": rel(NEXT_UNIT_CANDIDATE),
        "admissibility_audit_ref": rel(ADMISSIBILITY_AUDIT),
        "recommended_next_unit": next_unit_candidate["recommended_next_unit"],
        "recommended_next_unit_status": "PROPOSED_ONLY_REQUIRES_REVIEW",
        "no_action_taken": {
            "new_frontier_selected": False,
            "new_instrument_built": False,
            "new_cell1_build": False,
            "new_verification_probe": False,
            "new_c8_rerun": False,
            "new_missing_instrument_proposal": False,
            "reusable_schema_authorized": False,
        },
    }
    continuation_packet["continuation_packet_id"] = "c8_post_closure_continuation_" + sig8(continuation_packet)
    write_json(CONTINUATION_PACKET, continuation_packet)

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
        "C8_POST_CLOSURE_0_CLOSURE_RECEIPT_VERIFIED": closure_receipt.get("gate") == "PASS",
        "C8_POST_CLOSURE_1_LOCAL_LOOP_CLOSED": summary.get("local_loop_closed") is True,
        "C8_POST_CLOSURE_2_GLOBAL_FRONTIER_NOT_CLOSED": final_local.get("global_frontier_closed") is False,
        "C8_POST_CLOSURE_3_CHAIN_STEPS_CLOSED_SIX": summary.get("chain_steps_closed") == 6,
        "C8_POST_CLOSURE_4_NO_REUSABLE_SCHEMA_AUTHORIZED": admissibility_audit["reusable_schema_authorized"] is False,
        "C8_POST_CLOSURE_5_NEXT_UNIT_PROPOSED_ONLY": next_unit_candidate["candidate_status"] == "PROPOSED_ONLY",
        "C8_POST_CLOSURE_6_NEXT_UNIT_IS_SELECTION_REVIEW": next_unit_candidate["recommended_next_unit_kind"] == "SELECTION_REVIEW_PACKET",
        "C8_POST_CLOSURE_7_NO_FRONTIER_SELECTED_NOW": negative_controls["new_frontier_selected_count"] == 0,
        "C8_POST_CLOSURE_8_NO_NEW_BUILD_OR_RERUN": negative_controls["new_instrument_build_count"] == 0 and negative_controls["new_c8_rerun_count"] == 0,
        "C8_POST_CLOSURE_9_NO_RESEARCH_OR_GLOBAL_CLAIM": negative_controls["research_mode_opened_count"] == 0 and negative_controls["global_solution_claim_count"] == 0 and negative_controls["frontier_solved_claim_count"] == 0,
        "C8_POST_CLOSURE_10_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_POST_CLOSURE_11_BAD_COUNTERS_ZERO": not bool(nonzero),
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_POST_CLOSURE_CONTINUATION_DECISION_PASS" if gate == "PASS" else "TYPED_C8_POST_CLOSURE_CONTINUATION_DECISION_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_POST_CLOSURE_CONTINUATION_DECISION_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_POST_CLOSURE_CONTINUATION_DECISION_FAILED"

    readout = {
        "schema_version": "c8_post_closure_continuation_decision_readout_v0",
        "title": "C8 post-closure continuation decision readout",
        "status": status,
        "outcome_class": outcome,
        "source_closure_receipt_id": closure_receipt.get("receipt_id"),
        "local_loop_closed": True,
        "global_frontier_closed": False,
        "recommended_next_unit": next_unit_candidate["recommended_next_unit"],
        "recommended_next_unit_status": "PROPOSED_ONLY_REQUIRES_REVIEW",
        "new_frontier_selected_now": False,
        "new_build_now": False,
        "new_rerun_now": False,
        "reusable_schema_authorized": False,
        "summary": "The closed C8 local loop admits only a bounded successor-surface selection/review packet as the next smallest continuation. No new frontier, build, rerun, or reusable schema is authorized by this packet.",
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_post_closure_continuation_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "continuation_packet_ref": rel(CONTINUATION_PACKET),
        "admissibility_audit_ref": rel(ADMISSIBILITY_AUDIT),
        "next_unit_candidate_ref": rel(NEXT_UNIT_CANDIDATE),
        "source_closure_receipt_id": closure_receipt.get("receipt_id"),
        "recommended_next_unit": next_unit_candidate["recommended_next_unit"],
        "recommended_next_unit_status": "PROPOSED_ONLY_REQUIRES_REVIEW",
        "local_loop_closed": True,
        "global_frontier_closed": False,
        "reusable_schema_authorized": False,
        "new_frontier_selected_now": False,
        "new_build_now": False,
        "new_rerun_now": False,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_post_closure_continuation_decision_receipt_v0",
        "receipt_type": "TYPED_C8_POST_CLOSURE_CONTINUATION_DECISION_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_refs": {
            "closure_receipt_ref": rel(CLOSURE_RECEIPT),
            "closure_packet_ref": rel(CLOSURE_PACKET),
            "closure_timeline_ref": rel(CLOSURE_TIMELINE),
            "closure_boundary_audit_ref": rel(CLOSURE_BOUNDARY_AUDIT),
            "closure_report_ref": rel(CLOSURE_REPORT),
        },
        "machine_readable_continuation_summary": {
            "continuation_packet_created": gate == "PASS",
            "local_loop_closed": True,
            "global_frontier_closed": False,
            "source_closure_receipt_id": closure_receipt.get("receipt_id"),
            "source_closure_packet_id": closure_packet.get("closure_packet_id"),
            "recommended_next_unit": next_unit_candidate["recommended_next_unit"],
            "recommended_next_unit_kind": next_unit_candidate["recommended_next_unit_kind"],
            "recommended_next_unit_status": "PROPOSED_ONLY_REQUIRES_REVIEW",
            "new_frontier_selected_now": False,
            "new_instrument_build_now": False,
            "new_cell1_build_now": False,
            "new_verification_probe_now": False,
            "new_c8_rerun_now": False,
            "new_missing_instrument_proposal_now": False,
            "reusable_schema_authorized": False,
            "research_mode_opened": False,
            "general_cell1_authority": False,
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
            "continuation_packet": rel(CONTINUATION_PACKET),
            "admissibility_audit": rel(ADMISSIBILITY_AUDIT),
            "next_unit_candidate": rel(NEXT_UNIT_CANDIDATE),
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

    receipt["receipt_id"] = "c8_post_closure_continuation_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"continuation_receipt_id={receipt['receipt_id']}")
    print(f"continuation_receipt_path={rel(receipt_path)}")
    print(f"continuation_packet_path={rel(CONTINUATION_PACKET)}")
    print(f"next_unit_candidate_path={rel(NEXT_UNIT_CANDIDATE)}")
    print(f"recommended_next_unit={next_unit_candidate['recommended_next_unit']}")
    print(f"recommended_next_unit_status=PROPOSED_ONLY_REQUIRES_REVIEW")
    print(f"local_loop_closed=true")
    print(f"global_frontier_closed=false")
    print(f"reusable_schema_authorized=false")
    print(f"new_frontier_selected_now=false")
    print(f"continuation_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
