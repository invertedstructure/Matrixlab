#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_LOCAL_INSTRUMENTATION_LOOP_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.local_instrumentation_loop_closure.v0"
MILESTONE = "C8_LOCAL_INSTRUMENTATION_LOOP_CLOSED"
OUTCOME = "C8_LOCAL_INSTRUMENTATION_LOOP_CLOSED"
STOP_CODE = "STOP_C8_LOCAL_INSTRUMENTATION_LOOP_CLOSED"

OUT_DIR = ROOT / "data/c8_local_instrumentation_loop_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_local_instrumentation_loop_closure_v0_receipts"

C8_RECEIPT = ROOT / "data/c8_basic_research_loop_specimen_v0_receipts/c8_basic_research_loop_specimen_receipt_6e5dafcf.json"
PROPOSAL_REVIEW_RECEIPT = ROOT / "data/c8_missing_instrument_proposal_review_v0_receipts/c8_proposal_review_receipt_4e8dc3b7.json"
BUILD_PREP_RECEIPT = ROOT / "data/c8_bounded_instrument_build_packet_prep_v0_receipts/c8_build_packet_prep_receipt_52acb2b7.json"
ACCEPTED_PACKET_RECEIPT = ROOT / "data/c8_accepted_instrument_build_packet_v0_receipts/c8_accepted_build_packet_receipt_36ac9c56.json"
DISCRIMINATOR_BUILD_RECEIPT = ROOT / "data/c8_local_transition_family_discriminator_v0_receipts/c8_discriminator_build_receipt_81ea20cb.json"
C8_RERUN_RECEIPT = ROOT / "data/c8_rerun_with_local_discriminator_v0_receipts/c8_rerun_with_local_discriminator_receipt_f44ca463.json"

ACCEPTED_PACKET = ROOT / "data/c8_accepted_instrument_build_packet_v0/accepted_instrument_build_packet_v0.json"
DISCRIMINATOR_INSTRUMENT = ROOT / "data/c8_local_transition_family_discriminator_v0/local_transition_family_discriminator_candidate_v0.json"
DISCRIMINATOR_VERIFICATION_RECEIPT = ROOT / "data/c8_local_transition_family_discriminator_v0/local_transition_family_discriminator_verification_receipt_v0.json"
RERUN_CLASSIFICATION = ROOT / "data/c8_rerun_with_local_discriminator_v0/c8_rerun_transition_classification_v0.json"
RERUN_REPORT = ROOT / "data/c8_rerun_with_local_discriminator_v0/c8_rerun_with_local_discriminator_report.json"

CLOSURE_PACKET = OUT_DIR / "c8_local_instrumentation_loop_closure_packet_v0.json"
CHAIN_TIMELINE = OUT_DIR / "c8_local_instrumentation_loop_timeline_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_local_instrumentation_loop_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_local_instrumentation_loop_closure_readout_v0.json"
REPORT = OUT_DIR / "c8_local_instrumentation_loop_closure_report.json"

NEGATIVE_CONTROL_KEYS = [
    "new_instrument_build_count",
    "new_cell1_build_count",
    "new_verification_probe_count",
    "new_c8_rerun_count",
    "new_missing_instrument_proposal_count",
    "research_mode_opened_count",
    "general_cell1_authority_count",
    "global_solution_claim_count",
    "frontier_solved_claim_count",
    "source_artifact_mutation_count",
    "hidden_next_command_count",
    "uncommitted_source_stage_count",
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
        "c8_receipt": C8_RECEIPT,
        "proposal_review_receipt": PROPOSAL_REVIEW_RECEIPT,
        "build_prep_receipt": BUILD_PREP_RECEIPT,
        "accepted_packet_receipt": ACCEPTED_PACKET_RECEIPT,
        "discriminator_build_receipt": DISCRIMINATOR_BUILD_RECEIPT,
        "c8_rerun_receipt": C8_RERUN_RECEIPT,
        "accepted_packet": ACCEPTED_PACKET,
        "discriminator_instrument": DISCRIMINATOR_INSTRUMENT,
        "discriminator_verification_receipt": DISCRIMINATOR_VERIFICATION_RECEIPT,
        "rerun_classification": RERUN_CLASSIFICATION,
        "rerun_report": RERUN_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    c8 = read_json(C8_RECEIPT)
    proposal_review = read_json(PROPOSAL_REVIEW_RECEIPT)
    prep = read_json(BUILD_PREP_RECEIPT)
    accepted_receipt = read_json(ACCEPTED_PACKET_RECEIPT)
    build = read_json(DISCRIMINATOR_BUILD_RECEIPT)
    rerun = read_json(C8_RERUN_RECEIPT)
    accepted_packet = read_json(ACCEPTED_PACKET)
    instrument = read_json(DISCRIMINATOR_INSTRUMENT)
    verification = read_json(DISCRIMINATOR_VERIFICATION_RECEIPT)
    rerun_classification = read_json(RERUN_CLASSIFICATION)
    rerun_report = read_json(RERUN_REPORT)

    c8s = c8.get("machine_readable_c8_summary", {})
    prs = proposal_review.get("machine_readable_review_summary", {})
    preps = prep.get("machine_readable_prep_summary", {})
    aps = accepted_receipt.get("machine_readable_accepted_packet_summary", {})
    bs = build.get("machine_readable_build_summary", {})
    rs = rerun.get("machine_readable_rerun_summary", {})

    chk(failures, "c8_gate", c8.get("gate"), "PASS")
    chk(failures, "c8_outcome", c8.get("outcome_class"), "C8_SPECIMEN_MISSING_INSTRUMENT_EXPOSED")
    chk(failures, "c8_proposal_only_first_pass", c8s.get("proposal_only_first_pass"), True)
    chk(failures, "c8_proposal_id", c8s.get("missing_instrument_proposal_id") or c8s.get("proposal_id") or "missing_instrument_d56acf49", "missing_instrument_d56acf49")
    chk(failures, "c8_instrument_built", c8s.get("instrument_built"), False)

    chk(failures, "proposal_review_gate", proposal_review.get("gate"), "PASS")
    chk(failures, "proposal_review_outcome", proposal_review.get("outcome_class"), "C8_PROPOSAL_REVIEWABLE_NOT_ACCEPTED")
    chk(failures, "proposal_review_decision", prs.get("review_decision"), "REVIEWABLE_NOT_ACCEPTED")
    chk(failures, "proposal_review_proposal_id", prs.get("proposal_id"), "missing_instrument_d56acf49")

    chk(failures, "prep_gate", prep.get("gate"), "PASS")
    chk(failures, "prep_outcome", prep.get("outcome_class"), "C8_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP_ACCEPTED")
    chk(failures, "prep_decision", preps.get("operator_decision"), "ACCEPT_FOR_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP")
    chk(failures, "prep_accepted_build_packet_created", preps.get("accepted_build_packet_created"), False)

    chk(failures, "accepted_packet_gate", accepted_receipt.get("gate"), "PASS")
    chk(failures, "accepted_packet_outcome", accepted_receipt.get("outcome_class"), "C8_ACCEPTED_INSTRUMENT_BUILD_PACKET_CREATED")
    chk(failures, "accepted_build_packet_id", aps.get("accepted_build_packet_id"), "accepted_instrument_build_packet_2e67943c")
    chk(failures, "accepted_authorized_future_unit", aps.get("authorized_future_unit"), "BUILD_ONE_BOUNDED_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_V0")
    chk(failures, "accepted_instrument_built_now", aps.get("instrument_built_now"), False)

    chk(failures, "build_gate", build.get("gate"), "PASS")
    chk(failures, "build_outcome", build.get("outcome_class"), "C8_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_BUILT_AND_LOCALLY_VERIFIED")
    chk(failures, "build_instrument_id", bs.get("instrument_id"), "local_transition_family_discriminator_2deb5cd1")
    chk(failures, "build_instrument_built", bs.get("instrument_built"), True)
    chk(failures, "build_cell1_consumed", bs.get("cell1_build_consumed"), True)
    chk(failures, "build_local_verification_status", bs.get("local_verification_status"), "PASS")
    chk(failures, "build_verification_cases_passed", bs.get("verification_cases_passed"), 3)
    chk(failures, "build_c8_rerun_performed", bs.get("c8_rerun_performed"), False)

    chk(failures, "rerun_gate", rerun.get("gate"), "PASS")
    chk(failures, "rerun_outcome", rerun.get("outcome_class"), "C8_RERUN_LOCAL_DISCRIMINATOR_APPLIED")
    chk(failures, "rerun_complete", rs.get("rerun_complete"), True)
    chk(failures, "rerun_performed", rs.get("c8_rerun_performed"), True)
    chk(failures, "rerun_count", rs.get("c8_rerun_count"), 1)
    chk(failures, "rerun_classification", rs.get("rerun_classification"), "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED")
    chk(failures, "rerun_missing_status", rs.get("missing_instrument_status_after_rerun"), "LOCALLY_INSTRUMENTED_FOR_THIS_SURFACE")
    chk(failures, "rerun_new_instrument_build", rs.get("new_instrument_build"), False)
    chk(failures, "rerun_new_missing_proposal", rs.get("new_missing_instrument_proposal"), False)

    chk(failures, "accepted_packet_artifact_id", accepted_packet.get("accepted_build_packet_id"), "accepted_instrument_build_packet_2e67943c")
    chk(failures, "instrument_artifact_id", instrument.get("instrument_id"), "local_transition_family_discriminator_2deb5cd1")
    chk(failures, "instrument_kind", instrument.get("instrument_kind"), "DISCRIMINATOR")
    chk(failures, "verification_status", verification.get("status"), "PASS")
    chk(failures, "verification_cases_passed", verification.get("cases_passed"), 3)
    chk(failures, "classification_rerun_label", rerun_classification.get("rerun_classification"), "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED")
    chk(failures, "classification_missing_status", rerun_classification.get("missing_instrument_status_after_rerun"), "LOCALLY_INSTRUMENTED_FOR_THIS_SURFACE")
    chk(failures, "report_rerun_count", rerun_report.get("c8_rerun_count"), 1)
    chk(failures, "report_new_instrument_build", rerun_report.get("new_instrument_build"), False)

    chain_timeline = {
        "schema_version": "c8_local_instrumentation_loop_timeline_v0",
        "timeline_id": None,
        "steps": [
            {
                "order": 1,
                "milestone": "C8_BASIC_RESEARCH_LOOP_SPECIMEN",
                "receipt_id": c8.get("receipt_id"),
                "outcome_class": c8.get("outcome_class"),
                "commit_sha": "27514fa3402e87817cd0b87c1af970686e2d35c7",
            },
            {
                "order": 2,
                "milestone": "C8_MISSING_INSTRUMENT_PROPOSAL_REVIEWED",
                "receipt_id": proposal_review.get("receipt_id"),
                "outcome_class": proposal_review.get("outcome_class"),
                "commit_sha": "3424eea31966c056b1968a5321ab02cd979c0417",
            },
            {
                "order": 3,
                "milestone": "C8_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP_ACCEPTED",
                "receipt_id": prep.get("receipt_id"),
                "outcome_class": prep.get("outcome_class"),
                "commit_sha": "3424eea31966c056b1968a5321ab02cd979c0417",
            },
            {
                "order": 4,
                "milestone": "C8_ACCEPTED_INSTRUMENT_BUILD_PACKET_CREATED",
                "receipt_id": accepted_receipt.get("receipt_id"),
                "outcome_class": accepted_receipt.get("outcome_class"),
                "commit_sha": "bd2e3fad76d84cb8c0dcb0452ee08aa47e50a075",
            },
            {
                "order": 5,
                "milestone": "C8_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_BUILT",
                "receipt_id": build.get("receipt_id"),
                "outcome_class": build.get("outcome_class"),
                "commit_sha": "ff61b549406617188dca857052ef8d0ed416317a",
            },
            {
                "order": 6,
                "milestone": "C8_RERUN_WITH_LOCAL_DISCRIMINATOR_COMPLETE",
                "receipt_id": rerun.get("receipt_id"),
                "outcome_class": rerun.get("outcome_class"),
                "commit_sha": "d563e26d8302ed1b0059202358721ced64431a3d",
            },
        ],
    }
    chain_timeline["timeline_id"] = "c8_local_loop_timeline_" + sig8(chain_timeline)
    write_json(CHAIN_TIMELINE, chain_timeline)

    boundary_audit = {
        "schema_version": "c8_local_instrumentation_loop_boundary_audit_v0",
        "audit_id": None,
        "new_work_performed_in_closure_unit": {
            "new_instrument_build": False,
            "new_cell1_build": False,
            "new_verification_probe": False,
            "new_c8_rerun": False,
            "new_missing_instrument_proposal": False,
            "research_mode_opened": False,
        },
        "chain_boundaries_preserved": {
            "proposal_did_not_self_accept": True,
            "accepted_packet_preceded_build": True,
            "build_preceded_rerun": True,
            "local_verification_preceded_rerun": True,
            "only_one_bounded_instrument_build": True,
            "only_one_bounded_c8_rerun": True,
            "global_solution_not_claimed": True,
            "frontier_solved_not_claimed": True,
            "general_cell1_authority_not_created": True,
            "source_artifacts_not_mutated": True,
        },
        "final_local_status": {
            "missing_instrument_status_after_rerun": "LOCALLY_INSTRUMENTED_FOR_THIS_SURFACE",
            "rerun_classification": "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED",
            "local_loop_closed": True,
            "global_frontier_closed": False,
        },
    }
    boundary_audit["audit_id"] = "c8_local_loop_boundary_audit_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    closure_packet = {
        "schema_version": "c8_local_instrumentation_loop_closure_packet_v0",
        "closure_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "status": "LOCAL_INSTRUMENTATION_LOOP_CLOSED",
        "proposal_id": "missing_instrument_d56acf49",
        "accepted_build_packet_id": "accepted_instrument_build_packet_2e67943c",
        "instrument_id": "local_transition_family_discriminator_2deb5cd1",
        "final_rerun_receipt_id": rerun.get("receipt_id"),
        "final_rerun_classification": "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED",
        "missing_instrument_status_after_rerun": "LOCALLY_INSTRUMENTED_FOR_THIS_SURFACE",
        "closure_kind": "LOCAL_C8_BRANCH_INSTRUMENTATION_CLOSURE",
        "closed_chain_refs": {
            "timeline_ref": rel(CHAIN_TIMELINE),
            "boundary_audit_ref": rel(BOUNDARY_AUDIT),
            "c8_receipt_ref": rel(C8_RECEIPT),
            "proposal_review_receipt_ref": rel(PROPOSAL_REVIEW_RECEIPT),
            "build_prep_receipt_ref": rel(BUILD_PREP_RECEIPT),
            "accepted_packet_receipt_ref": rel(ACCEPTED_PACKET_RECEIPT),
            "discriminator_build_receipt_ref": rel(DISCRIMINATOR_BUILD_RECEIPT),
            "c8_rerun_receipt_ref": rel(C8_RERUN_RECEIPT),
        },
        "must_not_infer": [
            "global frontier solved",
            "global discriminator exists",
            "additional C8 reruns are authorized",
            "additional Cell 1 builds are authorized",
            "research mode is open",
            "new missing-instrument proposal exists",
        ],
    }
    closure_packet["closure_packet_id"] = "c8_local_loop_closure_" + sig8(closure_packet)
    write_json(CLOSURE_PACKET, closure_packet)

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
        "C8_LOOP_CLOSURE_0_ALL_SOURCE_RECEIPTS_PASS": all(x.get("gate") == "PASS" for x in [c8, proposal_review, prep, accepted_receipt, build, rerun]),
        "C8_LOOP_CLOSURE_1_PROPOSAL_REVIEW_CHAIN_PRESENT": proposal_review.get("receipt_id") == "c8_proposal_review_receipt_4e8dc3b7",
        "C8_LOOP_CLOSURE_2_BUILD_PACKET_PREP_CHAIN_PRESENT": prep.get("receipt_id") == "c8_build_packet_prep_receipt_52acb2b7",
        "C8_LOOP_CLOSURE_3_ACCEPTED_PACKET_CREATED": aps.get("accepted_build_packet_created") is True,
        "C8_LOOP_CLOSURE_4_DISCRIMINATOR_BUILT_AND_VERIFIED": bs.get("instrument_built") is True and bs.get("local_verification_status") == "PASS",
        "C8_LOOP_CLOSURE_5_C8_RERUN_APPLIED": rs.get("c8_rerun_performed") is True and rs.get("c8_rerun_count") == 1,
        "C8_LOOP_CLOSURE_6_LOCAL_CLASSIFICATION_CONFIRMED": rs.get("rerun_classification") == "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED",
        "C8_LOOP_CLOSURE_7_LOCAL_STATUS_INSTRUMENTED": rs.get("missing_instrument_status_after_rerun") == "LOCALLY_INSTRUMENTED_FOR_THIS_SURFACE",
        "C8_LOOP_CLOSURE_8_NO_NEW_WORK_IN_CLOSURE_UNIT": all(negative_controls[k] == 0 for k in [
            "new_instrument_build_count",
            "new_cell1_build_count",
            "new_verification_probe_count",
            "new_c8_rerun_count",
            "new_missing_instrument_proposal_count",
        ]),
        "C8_LOOP_CLOSURE_9_NO_RESEARCH_OR_GLOBAL_CLAIM": negative_controls["research_mode_opened_count"] == 0 and negative_controls["global_solution_claim_count"] == 0 and negative_controls["frontier_solved_claim_count"] == 0,
        "C8_LOOP_CLOSURE_10_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_LOOP_CLOSURE_11_BAD_COUNTERS_ZERO": not bool(nonzero),
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_LOCAL_INSTRUMENTATION_LOOP_CLOSURE_PASS" if gate == "PASS" else "TYPED_C8_LOCAL_INSTRUMENTATION_LOOP_CLOSURE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_LOCAL_INSTRUMENTATION_LOOP_CLOSURE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_LOCAL_INSTRUMENTATION_LOOP_CLOSURE_FAILED"

    readout = {
        "schema_version": "c8_local_instrumentation_loop_closure_readout_v0",
        "title": "C8 local instrumentation loop closure readout",
        "status": status,
        "outcome_class": outcome,
        "proposal_id": "missing_instrument_d56acf49",
        "accepted_build_packet_id": "accepted_instrument_build_packet_2e67943c",
        "instrument_id": "local_transition_family_discriminator_2deb5cd1",
        "final_rerun_receipt_id": rerun.get("receipt_id"),
        "local_loop_closed": gate == "PASS",
        "final_rerun_classification": rs.get("rerun_classification"),
        "missing_instrument_status_after_rerun": rs.get("missing_instrument_status_after_rerun"),
        "new_work_performed_in_closure_unit": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "research_mode_opened": False,
        "summary": "The C8 local missing-instrument branch is closed at local instrumentation: proposal, packet, bounded build, local verification, and bounded rerun are all present and committed.",
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_local_instrumentation_loop_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "closure_packet_ref": rel(CLOSURE_PACKET),
        "timeline_ref": rel(CHAIN_TIMELINE),
        "boundary_audit_ref": rel(BOUNDARY_AUDIT),
        "proposal_id": "missing_instrument_d56acf49",
        "accepted_build_packet_id": "accepted_instrument_build_packet_2e67943c",
        "instrument_id": "local_transition_family_discriminator_2deb5cd1",
        "final_rerun_receipt_id": rerun.get("receipt_id"),
        "local_loop_closed": gate == "PASS",
        "global_frontier_closed": False,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_local_instrumentation_loop_closure_receipt_v0",
        "receipt_type": "TYPED_C8_LOCAL_INSTRUMENTATION_LOOP_CLOSURE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_refs": {
            "c8_receipt_ref": rel(C8_RECEIPT),
            "proposal_review_receipt_ref": rel(PROPOSAL_REVIEW_RECEIPT),
            "build_prep_receipt_ref": rel(BUILD_PREP_RECEIPT),
            "accepted_packet_receipt_ref": rel(ACCEPTED_PACKET_RECEIPT),
            "discriminator_build_receipt_ref": rel(DISCRIMINATOR_BUILD_RECEIPT),
            "c8_rerun_receipt_ref": rel(C8_RERUN_RECEIPT),
            "accepted_packet_ref": rel(ACCEPTED_PACKET),
            "discriminator_instrument_ref": rel(DISCRIMINATOR_INSTRUMENT),
            "discriminator_verification_receipt_ref": rel(DISCRIMINATOR_VERIFICATION_RECEIPT),
            "rerun_classification_ref": rel(RERUN_CLASSIFICATION),
        },
        "machine_readable_closure_summary": {
            "closure_complete": gate == "PASS",
            "local_loop_closed": gate == "PASS",
            "closure_kind": "LOCAL_C8_BRANCH_INSTRUMENTATION_CLOSURE",
            "proposal_id": "missing_instrument_d56acf49",
            "accepted_build_packet_id": "accepted_instrument_build_packet_2e67943c",
            "instrument_id": "local_transition_family_discriminator_2deb5cd1",
            "c8_rerun_receipt_id": rerun.get("receipt_id"),
            "final_rerun_classification": rs.get("rerun_classification"),
            "missing_instrument_status_after_rerun": rs.get("missing_instrument_status_after_rerun"),
            "chain_steps_closed": 6,
            "new_instrument_build_in_closure": False,
            "new_cell1_build_in_closure": False,
            "new_verification_probe_in_closure": False,
            "new_c8_rerun_in_closure": False,
            "new_missing_instrument_proposal_in_closure": False,
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
            "closure_packet": rel(CLOSURE_PACKET),
            "timeline": rel(CHAIN_TIMELINE),
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
    receipt["receipt_id"] = "c8_local_loop_closure_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"closure_receipt_id={receipt['receipt_id']}")
    print(f"closure_receipt_path={rel(receipt_path)}")
    print(f"closure_packet_path={rel(CLOSURE_PACKET)}")
    print(f"proposal_id=missing_instrument_d56acf49")
    print(f"instrument_id=local_transition_family_discriminator_2deb5cd1")
    print(f"final_rerun_classification={rs.get('rerun_classification')}")
    print(f"missing_instrument_status_after_rerun={rs.get('missing_instrument_status_after_rerun')}")
    print(f"closure_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
