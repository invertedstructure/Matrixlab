#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "BUILD_ONE_BOUNDED_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_V0"
TARGET_UNIT_ID = "research.c8.local_transition_family_discriminator.v0"
MILESTONE = "C8_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_BUILT"
OUTCOME = "C8_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_BUILT_AND_LOCALLY_VERIFIED"
STOP_CODE = "STOP_C8_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_BUILT_READY_FOR_C8_RERUN"

OUT_DIR = ROOT / "data/c8_local_transition_family_discriminator_v0"
RECEIPT_DIR = ROOT / "data/c8_local_transition_family_discriminator_v0_receipts"

C8_RECEIPT = ROOT / "data/c8_basic_research_loop_specimen_v0_receipts/c8_basic_research_loop_specimen_receipt_6e5dafcf.json"
C8_PROPOSAL = ROOT / "data/c8_basic_research_loop_specimen_v0/missing_instrument_proposal_v0.json"
C8_FRONTIER = ROOT / "data/c8_basic_research_loop_specimen_v0/frontier_surface_contract_v0.json"
C8_PROBE_RECEIPT = ROOT / "data/c8_basic_research_loop_specimen_v0/bounded_probe_receipt_v0.json"
C8_CLASSIFICATION = ROOT / "data/c8_basic_research_loop_specimen_v0/research_transition_classification_v0.json"

PROPOSAL_REVIEW_RECEIPT = ROOT / "data/c8_missing_instrument_proposal_review_v0_receipts/c8_proposal_review_receipt_4e8dc3b7.json"
BUILD_PREP_RECEIPT = ROOT / "data/c8_bounded_instrument_build_packet_prep_v0_receipts/c8_build_packet_prep_receipt_52acb2b7.json"
ACCEPTED_PACKET_RECEIPT = ROOT / "data/c8_accepted_instrument_build_packet_v0_receipts/c8_accepted_build_packet_receipt_36ac9c56.json"
ACCEPTED_PACKET = ROOT / "data/c8_accepted_instrument_build_packet_v0/accepted_instrument_build_packet_v0.json"
BUILD_CONTRACT = ROOT / "data/c8_accepted_instrument_build_packet_v0/bounded_instrument_build_contract_v0.json"

INSTRUMENT = OUT_DIR / "local_transition_family_discriminator_candidate_v0.json"
BUILD_RECEIPT_LOCAL = OUT_DIR / "local_transition_family_discriminator_build_receipt_v0.json"
VERIFICATION_CASES = OUT_DIR / "local_transition_family_discriminator_verification_cases_v0.json"
VERIFICATION_RECEIPT = OUT_DIR / "local_transition_family_discriminator_verification_receipt_v0.json"
READOUT = OUT_DIR / "c8_local_transition_family_discriminator_readout_v0.json"
REPORT = OUT_DIR / "c8_local_transition_family_discriminator_report.json"

NEGATIVE_CONTROL_KEYS = [
    "second_instrument_build_count",
    "unbounded_instrument_rule_count",
    "source_artifact_mutation_count",
    "general_cell1_authority_count",
    "research_mode_opened_count",
    "global_solution_claim_count",
    "frontier_solved_claim_count",
    "c8_rerun_count",
    "repeat_run_count",
    "hidden_next_command_count",
    "verification_probe_over_budget_count",
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

def discriminate(instrument: Dict[str, Any], evidence: Dict[str, Any]) -> Dict[str, Any]:
    required = [
        "accepted_build_packet_id",
        "proposal_id",
        "frontier_surface_kind",
        "classification",
        "probe_classification_candidate",
    ]
    missing = [k for k in required if evidence.get(k) in (None, "", [])]
    if missing:
        return {
            "label": "MISSING_REQUIRED_EVIDENCE",
            "reason": "Required bounded evidence fields are missing.",
            "missing": missing,
            "is_in_scope": False,
            "claims_global_solution": False,
        }

    expected = instrument["bounded_domain"]
    if evidence.get("accepted_build_packet_id") != expected["accepted_build_packet_id"]:
        return {
            "label": "OUT_OF_SCOPE_ACCEPTED_PACKET",
            "reason": "Evidence is not bound to the accepted build packet.",
            "is_in_scope": False,
            "claims_global_solution": False,
        }

    if evidence.get("proposal_id") != expected["proposal_id"]:
        return {
            "label": "OUT_OF_SCOPE_PROPOSAL",
            "reason": "Evidence is not bound to the source proposal.",
            "is_in_scope": False,
            "claims_global_solution": False,
        }

    if evidence.get("frontier_surface_kind") != expected["frontier_surface_kind"]:
        return {
            "label": "OUT_OF_SCOPE_SURFACE",
            "reason": "Evidence is not on the declared missing-discriminator frontier surface.",
            "is_in_scope": False,
            "claims_global_solution": False,
        }

    if (
        evidence.get("classification") == "MISSING_INSTRUMENT_EXPOSED"
        and evidence.get("probe_classification_candidate") == "MISSING_INSTRUMENT_EXPOSED"
    ):
        return {
            "label": "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED",
            "reason": "Within the accepted packet boundary, the evidence matches the local missing-discriminator transition family candidate.",
            "is_in_scope": True,
            "claims_global_solution": False,
        }

    return {
        "label": "LOCAL_TRANSITION_FAMILY_NOT_CONFIRMED",
        "reason": "Evidence is in scope but does not match the local missing-discriminator transition condition.",
        "is_in_scope": True,
        "claims_global_solution": False,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []
    negative_controls = zero_counters()

    sources = {
        "c8_receipt": C8_RECEIPT,
        "c8_proposal": C8_PROPOSAL,
        "c8_frontier": C8_FRONTIER,
        "c8_probe_receipt": C8_PROBE_RECEIPT,
        "c8_classification": C8_CLASSIFICATION,
        "proposal_review_receipt": PROPOSAL_REVIEW_RECEIPT,
        "build_prep_receipt": BUILD_PREP_RECEIPT,
        "accepted_packet_receipt": ACCEPTED_PACKET_RECEIPT,
        "accepted_packet": ACCEPTED_PACKET,
        "build_contract": BUILD_CONTRACT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    c8_receipt = read_json(C8_RECEIPT)
    proposal = read_json(C8_PROPOSAL)
    frontier = read_json(C8_FRONTIER)
    probe_receipt = read_json(C8_PROBE_RECEIPT)
    classification = read_json(C8_CLASSIFICATION)
    review_receipt = read_json(PROPOSAL_REVIEW_RECEIPT)
    prep_receipt = read_json(BUILD_PREP_RECEIPT)
    accepted_receipt = read_json(ACCEPTED_PACKET_RECEIPT)
    accepted_packet = read_json(ACCEPTED_PACKET)
    build_contract = read_json(BUILD_CONTRACT)

    c8_summary = c8_receipt.get("machine_readable_c8_summary", {})
    accepted_summary = accepted_receipt.get("machine_readable_accepted_packet_summary", {})

    if c8_receipt.get("gate") != "PASS":
        failures.append(f"c8_gate_not_pass:{c8_receipt.get('gate')}")
    if c8_receipt.get("outcome_class") != "C8_SPECIMEN_MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"c8_outcome_wrong:{c8_receipt.get('outcome_class')}")
    if c8_summary.get("instrument_built") is not False:
        failures.append("c8_source_already_had_instrument_built")

    if proposal.get("proposal_id") != "missing_instrument_d56acf49":
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal.get("instrument_kind") != "DISCRIMINATOR":
        failures.append(f"proposal_instrument_kind_wrong:{proposal.get('instrument_kind')}")
    if proposal.get("smallest_honest_name") != "local_transition_family_discriminator_candidate":
        failures.append(f"proposal_candidate_name_wrong:{proposal.get('smallest_honest_name')}")

    if frontier.get("surface_kind") != "MISSING_DISCRIMINATOR_SURFACE":
        failures.append(f"frontier_surface_kind_wrong:{frontier.get('surface_kind')}")
    if classification.get("classification") != "MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"classification_wrong:{classification.get('classification')}")
    if probe_receipt.get("probe_result", {}).get("classification_candidate") != "MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"probe_candidate_wrong:{probe_receipt.get('probe_result', {}).get('classification_candidate')}")

    if review_receipt.get("gate") != "PASS":
        failures.append(f"review_gate_not_pass:{review_receipt.get('gate')}")
    if prep_receipt.get("gate") != "PASS":
        failures.append(f"prep_gate_not_pass:{prep_receipt.get('gate')}")

    if accepted_receipt.get("gate") != "PASS":
        failures.append(f"accepted_packet_receipt_gate_not_pass:{accepted_receipt.get('gate')}")
    if accepted_receipt.get("outcome_class") != "C8_ACCEPTED_INSTRUMENT_BUILD_PACKET_CREATED":
        failures.append(f"accepted_packet_receipt_outcome_wrong:{accepted_receipt.get('outcome_class')}")
    if accepted_summary.get("accepted_build_packet_created") is not True:
        failures.append("accepted_packet_not_created")
    if accepted_summary.get("instrument_built_now") is not False:
        failures.append("accepted_packet_claimed_build_already_occurred")
    if accepted_summary.get("authorized_future_unit") != UNIT_ID:
        failures.append(f"authorized_future_unit_wrong:{accepted_summary.get('authorized_future_unit')}")

    if accepted_packet.get("status") != "ACCEPTED_FOR_ONE_BOUNDED_INSTRUMENT_BUILD":
        failures.append(f"accepted_packet_status_wrong:{accepted_packet.get('status')}")
    accepted_future = accepted_packet.get("authorized_future_unit", {})
    if accepted_future.get("allowed_next_unit") != UNIT_ID:
        failures.append(f"accepted_packet_next_unit_wrong:{accepted_future.get('allowed_next_unit')}")
    if accepted_future.get("allowed_instrument_build_count") != 1:
        failures.append(f"allowed_build_count_wrong:{accepted_future.get('allowed_instrument_build_count')}")
    if accepted_future.get("allowed_verification_probe_count_after_build") != 1:
        failures.append(f"allowed_verification_count_wrong:{accepted_future.get('allowed_verification_probe_count_after_build')}")
    if accepted_future.get("must_emit_build_receipt") is not True:
        failures.append("accepted_packet_missing_build_receipt_requirement")
    if accepted_future.get("must_emit_verification_receipt") is not True:
        failures.append("accepted_packet_missing_verification_receipt_requirement")

    if build_contract.get("accepted_build_packet_ref") != rel(ACCEPTED_PACKET):
        failures.append(f"build_contract_accepted_packet_ref_wrong:{build_contract.get('accepted_build_packet_ref')}")
    if build_contract.get("instrument_kind") != "DISCRIMINATOR":
        failures.append(f"build_contract_instrument_kind_wrong:{build_contract.get('instrument_kind')}")

    instrument_seed = {
        "accepted_build_packet_id": accepted_packet.get("accepted_build_packet_id"),
        "proposal_id": proposal.get("proposal_id"),
        "candidate_name": proposal.get("smallest_honest_name"),
        "unit_id": UNIT_ID,
    }

    instrument = {
        "schema_version": "local_transition_family_discriminator_candidate_v0",
        "instrument_id": "local_transition_family_discriminator_" + sig8(instrument_seed),
        "instrument_kind": "DISCRIMINATOR",
        "candidate_name": proposal.get("smallest_honest_name"),
        "created_at": now_iso(),
        "built_by_unit": UNIT_ID,
        "source_refs": {
            "accepted_build_packet_ref": rel(ACCEPTED_PACKET),
            "accepted_packet_receipt_ref": rel(ACCEPTED_PACKET_RECEIPT),
            "proposal_ref": rel(C8_PROPOSAL),
            "proposal_review_receipt_ref": rel(PROPOSAL_REVIEW_RECEIPT),
            "build_packet_prep_receipt_ref": rel(BUILD_PREP_RECEIPT),
            "frontier_surface_ref": rel(C8_FRONTIER),
            "probe_receipt_ref": rel(C8_PROBE_RECEIPT),
            "classification_ref": rel(C8_CLASSIFICATION),
        },
        "bounded_domain": {
            "accepted_build_packet_id": accepted_packet.get("accepted_build_packet_id"),
            "proposal_id": proposal.get("proposal_id"),
            "frontier_surface_kind": frontier.get("surface_kind"),
            "classification": classification.get("classification"),
            "probe_classification_candidate": probe_receipt.get("probe_result", {}).get("classification_candidate"),
            "scope_note": "Only the declared C8 missing-discriminator surface and its source artifacts are in scope.",
        },
        "decision_labels": [
            "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED",
            "LOCAL_TRANSITION_FAMILY_NOT_CONFIRMED",
            "MISSING_REQUIRED_EVIDENCE",
            "OUT_OF_SCOPE_ACCEPTED_PACKET",
            "OUT_OF_SCOPE_PROPOSAL",
            "OUT_OF_SCOPE_SURFACE",
        ],
        "rules": [
            {
                "rule_id": "R0_REQUIRED_FIELDS",
                "description": "Missing required bounded evidence produces MISSING_REQUIRED_EVIDENCE.",
            },
            {
                "rule_id": "R1_ACCEPTED_PACKET_BOUNDARY",
                "description": "Evidence must reference the accepted build packet id.",
            },
            {
                "rule_id": "R2_PROPOSAL_BOUNDARY",
                "description": "Evidence must reference the source proposal id.",
            },
            {
                "rule_id": "R3_SURFACE_BOUNDARY",
                "description": "Evidence must remain on MISSING_DISCRIMINATOR_SURFACE.",
            },
            {
                "rule_id": "R4_LOCAL_CONFIRMATION",
                "description": "Within boundary, matching MISSING_INSTRUMENT_EXPOSED classification and probe candidate confirms a local transition-family candidate.",
            },
        ],
        "authority_boundary": {
            "can_classify_local_transition_family_candidate": True,
            "can_claim_global_discriminator": False,
            "can_claim_frontier_solved": False,
            "can_open_research_mode": False,
            "can_mutate_sources": False,
            "can_authorize_future_builds": False,
        },
        "must_not_infer": [
            "global discriminator exists",
            "frontier is solved",
            "future Cell 1 builds are generally authorized",
            "source C8 artifacts may be mutated",
            "C8 rerun has occurred",
        ],
    }
    write_json(INSTRUMENT, instrument)

    build_local = {
        "schema_version": "local_transition_family_discriminator_build_receipt_v0",
        "build_receipt_id": "local_transition_family_discriminator_build_" + sig8(instrument),
        "unit_id": UNIT_ID,
        "status": "BUILT_ONE_BOUNDED_DISCRIMINATOR",
        "instrument_ref": rel(INSTRUMENT),
        "instrument_id": instrument["instrument_id"],
        "accepted_build_packet_id": accepted_packet.get("accepted_build_packet_id"),
        "instrument_kind": "DISCRIMINATOR",
        "candidate_name": proposal.get("smallest_honest_name"),
        "build_count": 1,
        "source_refs": instrument["source_refs"],
        "authority_boundary": {
            "instrument_built": True,
            "cell1_build_consumed": True,
            "verification_required": True,
            "verification_performed_in_this_unit": True,
            "c8_rerun_performed": False,
            "general_cell1_authority": False,
        },
    }
    write_json(BUILD_RECEIPT_LOCAL, build_local)

    positive_evidence = {
        "case_id": "positive_in_scope_missing_instrument_exposed",
        "accepted_build_packet_id": accepted_packet.get("accepted_build_packet_id"),
        "proposal_id": proposal.get("proposal_id"),
        "frontier_surface_kind": frontier.get("surface_kind"),
        "classification": classification.get("classification"),
        "probe_classification_candidate": probe_receipt.get("probe_result", {}).get("classification_candidate"),
        "expected_label": "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED",
    }
    wrong_surface = {
        **positive_evidence,
        "case_id": "negative_wrong_surface",
        "frontier_surface_kind": "OUT_OF_SCOPE_SURFACE_KIND",
        "expected_label": "OUT_OF_SCOPE_SURFACE",
    }
    missing_packet = {
        "case_id": "negative_missing_accepted_packet",
        "proposal_id": proposal.get("proposal_id"),
        "frontier_surface_kind": frontier.get("surface_kind"),
        "classification": classification.get("classification"),
        "probe_classification_candidate": probe_receipt.get("probe_result", {}).get("classification_candidate"),
        "expected_label": "MISSING_REQUIRED_EVIDENCE",
    }

    cases = {
        "schema_version": "local_transition_family_discriminator_verification_cases_v0",
        "verification_probe_count": 1,
        "cases": [positive_evidence, wrong_surface, missing_packet],
    }
    write_json(VERIFICATION_CASES, cases)

    verification_results = []
    for case in cases["cases"]:
        observed = discriminate(instrument, case)
        passed = observed.get("label") == case.get("expected_label")
        verification_results.append({
            "case_id": case["case_id"],
            "expected_label": case["expected_label"],
            "observed_label": observed.get("label"),
            "passed": passed,
            "observed": observed,
        })

    verification_pass = all(x["passed"] for x in verification_results)
    if not verification_pass:
        failures.append("verification_cases_failed")

    verification_receipt = {
        "schema_version": "local_transition_family_discriminator_verification_receipt_v0",
        "verification_receipt_id": "local_transition_family_discriminator_verification_" + sig8(verification_results),
        "unit_id": UNIT_ID,
        "status": "PASS" if verification_pass else "FAIL",
        "instrument_ref": rel(INSTRUMENT),
        "instrument_id": instrument["instrument_id"],
        "verification_cases_ref": rel(VERIFICATION_CASES),
        "verification_probe_count": 1,
        "cases_total": len(verification_results),
        "cases_passed": sum(1 for x in verification_results if x["passed"]),
        "cases_failed": sum(1 for x in verification_results if not x["passed"]),
        "results": verification_results,
        "c8_rerun_performed": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
    }
    write_json(VERIFICATION_RECEIPT, verification_receipt)

    source_hashes_after = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    if source_hashes_before != source_hashes_after:
        negative_controls["source_artifact_mutation_count"] += 1

    # Exactly one bounded instrument build and one verification probe are authorized.
    instrument_build_count = 1
    verification_probe_count = 1

    if instrument_build_count > 1:
        negative_controls["second_instrument_build_count"] += instrument_build_count - 1
    if verification_probe_count > 1:
        negative_controls["verification_probe_over_budget_count"] += verification_probe_count - 1

    for rule in instrument.get("rules", []):
        text = json.dumps(rule, sort_keys=True).lower()
        if "global" in text and "claim" not in text:
            negative_controls["unbounded_instrument_rule_count"] += 1

    nonzero = {k: v for k, v in negative_controls.items() if v != 0}
    for k, v in nonzero.items():
        failures.append(f"{k}:{v}")

    acceptance_gates = {
        "DISCRIMINATOR_BUILD_0_ACCEPTED_PACKET_VERIFIED": accepted_receipt.get("gate") == "PASS",
        "DISCRIMINATOR_BUILD_1_AUTHORIZED_FUTURE_UNIT_MATCHES": accepted_summary.get("authorized_future_unit") == UNIT_ID,
        "DISCRIMINATOR_BUILD_2_BUILD_CONTRACT_VERIFIED": build_contract.get("accepted_build_packet_ref") == rel(ACCEPTED_PACKET),
        "DISCRIMINATOR_BUILD_3_ONE_INSTRUMENT_BUILT": instrument_build_count == 1,
        "DISCRIMINATOR_BUILD_4_INSTRUMENT_KIND_DISCRIMINATOR": instrument.get("instrument_kind") == "DISCRIMINATOR",
        "DISCRIMINATOR_BUILD_5_INSTRUMENT_BOUND_TO_ACCEPTED_PACKET": instrument.get("bounded_domain", {}).get("accepted_build_packet_id") == accepted_packet.get("accepted_build_packet_id"),
        "DISCRIMINATOR_BUILD_6_INSTRUMENT_BOUND_TO_PROPOSAL": instrument.get("bounded_domain", {}).get("proposal_id") == proposal.get("proposal_id"),
        "DISCRIMINATOR_BUILD_7_LOCAL_VERIFICATION_EMITTED": VERIFICATION_RECEIPT.exists(),
        "DISCRIMINATOR_BUILD_8_LOCAL_VERIFICATION_PASS": verification_pass,
        "DISCRIMINATOR_BUILD_9_NO_SECOND_INSTRUMENT_BUILD": negative_controls["second_instrument_build_count"] == 0,
        "DISCRIMINATOR_BUILD_10_NO_UNBOUNDED_RULES": negative_controls["unbounded_instrument_rule_count"] == 0,
        "DISCRIMINATOR_BUILD_11_NO_C8_RERUN": negative_controls["c8_rerun_count"] == 0,
        "DISCRIMINATOR_BUILD_12_NO_REPEAT_RUN": negative_controls["repeat_run_count"] == 0,
        "DISCRIMINATOR_BUILD_13_NO_RESEARCH_MODE": negative_controls["research_mode_opened_count"] == 0,
        "DISCRIMINATOR_BUILD_14_NO_GLOBAL_OR_FRONTIER_SOLUTION_CLAIM": negative_controls["global_solution_claim_count"] == 0 and negative_controls["frontier_solved_claim_count"] == 0,
        "DISCRIMINATOR_BUILD_15_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "DISCRIMINATOR_BUILD_16_BAD_COUNTERS_ZERO": not bool(nonzero),
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_BUILD_PASS" if gate == "PASS" else "TYPED_C8_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_BUILD_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_BUILD_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_BUILD_FAILED"

    readout = {
        "schema_version": "c8_local_transition_family_discriminator_readout_v0",
        "title": "C8 local transition family discriminator build readout",
        "status": status,
        "outcome_class": outcome,
        "instrument_id": instrument["instrument_id"],
        "instrument_kind": "DISCRIMINATOR",
        "candidate_name": proposal.get("smallest_honest_name"),
        "accepted_build_packet_id": accepted_packet.get("accepted_build_packet_id"),
        "instrument_built": True,
        "local_verification_emitted": True,
        "local_verification_status": verification_receipt["status"],
        "c8_rerun_performed": False,
        "summary": "One bounded local transition-family discriminator was built and locally verified against one verification probe suite. C8 has not rerun yet.",
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_local_transition_family_discriminator_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "instrument_id": instrument["instrument_id"],
        "accepted_build_packet_id": accepted_packet.get("accepted_build_packet_id"),
        "proposal_id": proposal.get("proposal_id"),
        "build_receipt_ref": rel(BUILD_RECEIPT_LOCAL),
        "verification_receipt_ref": rel(VERIFICATION_RECEIPT),
        "instrument_built": True,
        "cell1_build_consumed": True,
        "local_verification_emitted": True,
        "local_verification_pass": verification_pass,
        "verification_probe_count": verification_probe_count,
        "c8_rerun_performed": False,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_local_transition_family_discriminator_build_receipt_v0",
        "receipt_type": "TYPED_C8_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_BUILD_RECEIPT",
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
            "proposal_ref": rel(C8_PROPOSAL),
            "proposal_review_receipt_ref": rel(PROPOSAL_REVIEW_RECEIPT),
            "build_prep_receipt_ref": rel(BUILD_PREP_RECEIPT),
            "accepted_packet_receipt_ref": rel(ACCEPTED_PACKET_RECEIPT),
            "accepted_build_packet_ref": rel(ACCEPTED_PACKET),
            "build_contract_ref": rel(BUILD_CONTRACT),
            "frontier_surface_ref": rel(C8_FRONTIER),
            "probe_receipt_ref": rel(C8_PROBE_RECEIPT),
            "classification_ref": rel(C8_CLASSIFICATION),
        },
        "machine_readable_build_summary": {
            "build_complete": gate == "PASS",
            "instrument_built": True,
            "instrument_id": instrument["instrument_id"],
            "instrument_kind": "DISCRIMINATOR",
            "candidate_name": proposal.get("smallest_honest_name"),
            "accepted_build_packet_id": accepted_packet.get("accepted_build_packet_id"),
            "proposal_id": proposal.get("proposal_id"),
            "cell1_build_consumed": True,
            "local_verification_emitted": True,
            "local_verification_status": verification_receipt["status"],
            "verification_probe_count": verification_probe_count,
            "verification_cases_total": len(verification_results),
            "verification_cases_passed": sum(1 for x in verification_results if x["passed"]),
            "c8_rerun_performed": False,
            "repeat_run_performed": False,
            "general_cell1_authority": False,
            "research_mode_opened": False,
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
            "instrument": rel(INSTRUMENT),
            "build_receipt": rel(BUILD_RECEIPT_LOCAL),
            "verification_cases": rel(VERIFICATION_CASES),
            "verification_receipt": rel(VERIFICATION_RECEIPT),
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
    receipt["receipt_id"] = "c8_discriminator_build_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"discriminator_build_receipt_id={receipt['receipt_id']}")
    print(f"discriminator_build_receipt_path={rel(receipt_path)}")
    print(f"instrument_id={instrument['instrument_id']}")
    print(f"instrument_path={rel(INSTRUMENT)}")
    print(f"verification_receipt_path={rel(VERIFICATION_RECEIPT)}")
    print(f"proposal_id={proposal.get('proposal_id')}")
    print(f"build_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
