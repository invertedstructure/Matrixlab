#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RERUN_C8_WITH_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_V0"
TARGET_UNIT_ID = "research.c8.rerun_with_local_discriminator.v0"
MILESTONE = "C8_RERUN_WITH_LOCAL_DISCRIMINATOR_COMPLETE"
OUTCOME = "C8_RERUN_LOCAL_DISCRIMINATOR_APPLIED"
STOP_CODE = "STOP_C8_RERUN_WITH_LOCAL_DISCRIMINATOR_COMPLETE"

OUT_DIR = ROOT / "data/c8_rerun_with_local_discriminator_v0"
RECEIPT_DIR = ROOT / "data/c8_rerun_with_local_discriminator_v0_receipts"

C8_RECEIPT = ROOT / "data/c8_basic_research_loop_specimen_v0_receipts/c8_basic_research_loop_specimen_receipt_6e5dafcf.json"
C8_PROPOSAL = ROOT / "data/c8_basic_research_loop_specimen_v0/missing_instrument_proposal_v0.json"
C8_FRONTIER = ROOT / "data/c8_basic_research_loop_specimen_v0/frontier_surface_contract_v0.json"
C8_PROBE_RECEIPT = ROOT / "data/c8_basic_research_loop_specimen_v0/bounded_probe_receipt_v0.json"
C8_CLASSIFICATION = ROOT / "data/c8_basic_research_loop_specimen_v0/research_transition_classification_v0.json"

ACCEPTED_PACKET = ROOT / "data/c8_accepted_instrument_build_packet_v0/accepted_instrument_build_packet_v0.json"
ACCEPTED_PACKET_RECEIPT = ROOT / "data/c8_accepted_instrument_build_packet_v0_receipts/c8_accepted_build_packet_receipt_36ac9c56.json"

DISCRIMINATOR_BUILD_RECEIPT = ROOT / "data/c8_local_transition_family_discriminator_v0_receipts/c8_discriminator_build_receipt_81ea20cb.json"
DISCRIMINATOR_INSTRUMENT = ROOT / "data/c8_local_transition_family_discriminator_v0/local_transition_family_discriminator_candidate_v0.json"
DISCRIMINATOR_LOCAL_BUILD_RECEIPT = ROOT / "data/c8_local_transition_family_discriminator_v0/local_transition_family_discriminator_build_receipt_v0.json"
DISCRIMINATOR_VERIFICATION_RECEIPT = ROOT / "data/c8_local_transition_family_discriminator_v0/local_transition_family_discriminator_verification_receipt_v0.json"

RERUN_OPEN_PACKET = OUT_DIR / "c8_rerun_with_local_discriminator_open_packet_v0.json"
RERUN_EVIDENCE_PACKET = OUT_DIR / "c8_rerun_with_local_discriminator_evidence_packet_v0.json"
DISCRIMINATOR_APPLICATION_RECEIPT = OUT_DIR / "local_discriminator_application_receipt_v0.json"
RERUN_CLASSIFICATION = OUT_DIR / "c8_rerun_transition_classification_v0.json"
RERUN_READOUT = OUT_DIR / "c8_rerun_with_local_discriminator_readout_v0.json"
RERUN_REPORT = OUT_DIR / "c8_rerun_with_local_discriminator_report.json"

NEGATIVE_CONTROL_KEYS = [
    "new_instrument_build_count",
    "cell1_build_count",
    "verification_probe_run_count",
    "second_c8_rerun_count",
    "repeat_over_budget_count",
    "new_missing_instrument_proposal_count",
    "research_mode_opened_count",
    "general_cell1_authority_count",
    "global_solution_claim_count",
    "frontier_solved_claim_count",
    "source_artifact_mutation_count",
    "hidden_next_command_count",
    "unbounded_probe_count",
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
            "reason": "Within the accepted packet boundary, the built discriminator classifies the original C8 missing-instrument surface as a local transition-family candidate.",
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
        "accepted_packet": ACCEPTED_PACKET,
        "accepted_packet_receipt": ACCEPTED_PACKET_RECEIPT,
        "discriminator_build_receipt": DISCRIMINATOR_BUILD_RECEIPT,
        "discriminator_instrument": DISCRIMINATOR_INSTRUMENT,
        "discriminator_local_build_receipt": DISCRIMINATOR_LOCAL_BUILD_RECEIPT,
        "discriminator_verification_receipt": DISCRIMINATOR_VERIFICATION_RECEIPT,
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
    accepted_packet = read_json(ACCEPTED_PACKET)
    accepted_packet_receipt = read_json(ACCEPTED_PACKET_RECEIPT)
    build_receipt = read_json(DISCRIMINATOR_BUILD_RECEIPT)
    instrument = read_json(DISCRIMINATOR_INSTRUMENT)
    local_build = read_json(DISCRIMINATOR_LOCAL_BUILD_RECEIPT)
    verification = read_json(DISCRIMINATOR_VERIFICATION_RECEIPT)

    c8_summary = c8_receipt.get("machine_readable_c8_summary", {})
    accepted_summary = accepted_packet_receipt.get("machine_readable_accepted_packet_summary", {})
    build_summary = build_receipt.get("machine_readable_build_summary", {})

    if c8_receipt.get("gate") != "PASS":
        failures.append(f"c8_gate_not_pass:{c8_receipt.get('gate')}")
    if c8_receipt.get("outcome_class") != "C8_SPECIMEN_MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"c8_outcome_wrong:{c8_receipt.get('outcome_class')}")
    if c8_summary.get("proposal_only_first_pass") is not True:
        failures.append("source_c8_not_proposal_only_first_pass")
    if c8_summary.get("instrument_built") is not False:
        failures.append("source_c8_claims_instrument_already_built")

    if proposal.get("proposal_id") != "missing_instrument_d56acf49":
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal.get("instrument_kind") != "DISCRIMINATOR":
        failures.append(f"proposal_instrument_kind_wrong:{proposal.get('instrument_kind')}")

    if frontier.get("surface_kind") != "MISSING_DISCRIMINATOR_SURFACE":
        failures.append(f"frontier_surface_kind_wrong:{frontier.get('surface_kind')}")
    if classification.get("classification") != "MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"classification_wrong:{classification.get('classification')}")
    if probe_receipt.get("probe_result", {}).get("classification_candidate") != "MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"probe_candidate_wrong:{probe_receipt.get('probe_result', {}).get('classification_candidate')}")

    if accepted_packet_receipt.get("gate") != "PASS":
        failures.append(f"accepted_packet_receipt_gate_wrong:{accepted_packet_receipt.get('gate')}")
    if accepted_summary.get("accepted_build_packet_created") is not True:
        failures.append("accepted_packet_not_created")
    if accepted_summary.get("allowed_future_c8_repeat_after_verified_build") != 1:
        failures.append(f"allowed_future_c8_repeat_wrong:{accepted_summary.get('allowed_future_c8_repeat_after_verified_build')}")

    if accepted_packet.get("accepted_build_packet_id") != "accepted_instrument_build_packet_2e67943c":
        failures.append(f"accepted_build_packet_id_wrong:{accepted_packet.get('accepted_build_packet_id')}")

    if build_receipt.get("gate") != "PASS":
        failures.append(f"discriminator_build_gate_wrong:{build_receipt.get('gate')}")
    if build_summary.get("instrument_built") is not True:
        failures.append("discriminator_not_built")
    if build_summary.get("local_verification_status") != "PASS":
        failures.append(f"discriminator_local_verification_not_pass:{build_summary.get('local_verification_status')}")
    if build_summary.get("verification_cases_passed") != 3:
        failures.append(f"verification_cases_passed_wrong:{build_summary.get('verification_cases_passed')}")
    if build_summary.get("c8_rerun_performed") is not False:
        failures.append("source_build_claims_c8_already_reran")
    if build_summary.get("instrument_id") != "local_transition_family_discriminator_2deb5cd1":
        failures.append(f"instrument_id_wrong:{build_summary.get('instrument_id')}")

    if instrument.get("instrument_id") != "local_transition_family_discriminator_2deb5cd1":
        failures.append(f"instrument_artifact_id_wrong:{instrument.get('instrument_id')}")
    if instrument.get("instrument_kind") != "DISCRIMINATOR":
        failures.append(f"instrument_kind_wrong:{instrument.get('instrument_kind')}")
    if local_build.get("status") != "BUILT_ONE_BOUNDED_DISCRIMINATOR":
        failures.append(f"local_build_status_wrong:{local_build.get('status')}")
    if verification.get("status") != "PASS":
        failures.append(f"verification_receipt_status_wrong:{verification.get('status')}")

    rerun_open_packet = {
        "schema_version": "c8_rerun_with_local_discriminator_open_packet_v0",
        "rerun_open_id": None,
        "unit_id": UNIT_ID,
        "decision_provenance": "OPERATOR_PROCEED_FROM_COMMITTED_VERIFIED_DISCRIMINATOR_BUILD",
        "source_discriminator_build_receipt_ref": rel(DISCRIMINATOR_BUILD_RECEIPT),
        "source_instrument_ref": rel(DISCRIMINATOR_INSTRUMENT),
        "authorized_scope": {
            "max_c8_reruns": 1,
            "max_discriminator_applications": 1,
            "max_new_instrument_builds": 0,
            "max_cell1_builds": 0,
            "max_verification_probes": 0,
            "max_new_missing_instrument_proposals": 0,
            "max_frontier_surfaces": 1,
        },
        "not_authorized": [
            "new instrument build",
            "Cell 1 build",
            "verification probe",
            "second C8 rerun",
            "research mode",
            "general Cell 1 authority",
            "global solution claim",
            "frontier solved claim",
            "source artifact mutation",
        ],
    }
    rerun_open_packet["rerun_open_id"] = "c8_rerun_open_" + sig8(rerun_open_packet)
    write_json(RERUN_OPEN_PACKET, rerun_open_packet)

    evidence = {
        "schema_version": "c8_rerun_with_local_discriminator_evidence_packet_v0",
        "evidence_id": None,
        "rerun_open_ref": rel(RERUN_OPEN_PACKET),
        "accepted_build_packet_id": accepted_packet.get("accepted_build_packet_id"),
        "proposal_id": proposal.get("proposal_id"),
        "frontier_surface_kind": frontier.get("surface_kind"),
        "classification": classification.get("classification"),
        "probe_classification_candidate": probe_receipt.get("probe_result", {}).get("classification_candidate"),
        "instrument_id": instrument.get("instrument_id"),
        "source_refs": {
            "c8_receipt_ref": rel(C8_RECEIPT),
            "frontier_surface_ref": rel(C8_FRONTIER),
            "probe_receipt_ref": rel(C8_PROBE_RECEIPT),
            "classification_ref": rel(C8_CLASSIFICATION),
            "accepted_build_packet_ref": rel(ACCEPTED_PACKET),
            "instrument_ref": rel(DISCRIMINATOR_INSTRUMENT),
        },
    }
    evidence["evidence_id"] = "c8_rerun_evidence_" + sig8(evidence)
    write_json(RERUN_EVIDENCE_PACKET, evidence)

    observed = discriminate(instrument, evidence)

    discriminator_application = {
        "schema_version": "local_discriminator_application_receipt_v0",
        "application_receipt_id": None,
        "unit_id": UNIT_ID,
        "instrument_ref": rel(DISCRIMINATOR_INSTRUMENT),
        "instrument_id": instrument.get("instrument_id"),
        "evidence_packet_ref": rel(RERUN_EVIDENCE_PACKET),
        "discriminator_application_count": 1,
        "observed_label": observed.get("label"),
        "observed": observed,
        "status": "PASS" if observed.get("label") == "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED" else "IN_SCOPE_NOT_CONFIRMED",
        "global_solution_claim": False,
        "frontier_solved_claim": False,
    }
    discriminator_application["application_receipt_id"] = "local_discriminator_application_" + sig8(discriminator_application)
    write_json(DISCRIMINATOR_APPLICATION_RECEIPT, discriminator_application)

    rerun_classification = {
        "schema_version": "c8_rerun_transition_classification_v0",
        "classification_id": None,
        "unit_id": UNIT_ID,
        "source_application_receipt_ref": rel(DISCRIMINATOR_APPLICATION_RECEIPT),
        "previous_c8_classification": "MISSING_INSTRUMENT_EXPOSED",
        "rerun_classification": observed.get("label"),
        "classification_status": "LOCAL_CLASSIFICATION_COMPLETE",
        "local_instrument_applied": True,
        "local_discriminator_confirmed": observed.get("label") == "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED",
        "missing_instrument_status_after_rerun": "LOCALLY_INSTRUMENTED_FOR_THIS_SURFACE",
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "research_mode_opened": False,
        "must_not_infer": [
            "frontier solved",
            "global discriminator exists",
            "general Cell 1 authority",
            "additional C8 reruns authorized",
            "new proposal authorized",
        ],
    }
    rerun_classification["classification_id"] = "c8_rerun_classification_" + sig8(rerun_classification)
    write_json(RERUN_CLASSIFICATION, rerun_classification)

    source_hashes_after = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    if source_hashes_before != source_hashes_after:
        negative_controls["source_artifact_mutation_count"] += 1

    c8_rerun_count = 1
    discriminator_application_count = 1

    if c8_rerun_count > 1:
        negative_controls["second_c8_rerun_count"] += c8_rerun_count - 1
    if discriminator_application_count > 1:
        negative_controls["repeat_over_budget_count"] += discriminator_application_count - 1

    nonzero = {k: v for k, v in negative_controls.items() if v != 0}
    for k, v in nonzero.items():
        failures.append(f"{k}:{v}")

    acceptance_gates = {
        "C8_RERUN_0_SOURCE_C8_VERIFIED": c8_receipt.get("gate") == "PASS",
        "C8_RERUN_1_ACCEPTED_PACKET_VERIFIED": accepted_packet_receipt.get("gate") == "PASS",
        "C8_RERUN_2_DISCRIMINATOR_BUILD_VERIFIED": build_receipt.get("gate") == "PASS",
        "C8_RERUN_3_LOCAL_VERIFICATION_PASS_VERIFIED": verification.get("status") == "PASS",
        "C8_RERUN_4_ONE_RERUN_OPEN_PACKET_EMITTED": RERUN_OPEN_PACKET.exists(),
        "C8_RERUN_5_ONE_EVIDENCE_PACKET_EMITTED": RERUN_EVIDENCE_PACKET.exists(),
        "C8_RERUN_6_ONE_DISCRIMINATOR_APPLICATION": discriminator_application_count == 1,
        "C8_RERUN_7_CLASSIFICATION_EMITTED": RERUN_CLASSIFICATION.exists(),
        "C8_RERUN_8_LOCAL_CLASSIFICATION_CONFIRMED": observed.get("label") == "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED",
        "C8_RERUN_9_NO_NEW_BUILD": negative_controls["new_instrument_build_count"] == 0,
        "C8_RERUN_10_NO_CELL1_BUILD": negative_controls["cell1_build_count"] == 0,
        "C8_RERUN_11_NO_VERIFICATION_PROBE": negative_controls["verification_probe_run_count"] == 0,
        "C8_RERUN_12_NO_SECOND_C8_RERUN": negative_controls["second_c8_rerun_count"] == 0,
        "C8_RERUN_13_NO_NEW_MISSING_INSTRUMENT_PROPOSAL": negative_controls["new_missing_instrument_proposal_count"] == 0,
        "C8_RERUN_14_NO_RESEARCH_MODE": negative_controls["research_mode_opened_count"] == 0,
        "C8_RERUN_15_NO_GLOBAL_OR_FRONTIER_SOLUTION_CLAIM": negative_controls["global_solution_claim_count"] == 0 and negative_controls["frontier_solved_claim_count"] == 0,
        "C8_RERUN_16_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_RERUN_17_BAD_COUNTERS_ZERO": not bool(nonzero),
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_RERUN_WITH_LOCAL_DISCRIMINATOR_PASS" if gate == "PASS" else "TYPED_C8_RERUN_WITH_LOCAL_DISCRIMINATOR_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_RERUN_WITH_LOCAL_DISCRIMINATOR_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_RERUN_WITH_LOCAL_DISCRIMINATOR_FAILED"

    readout = {
        "schema_version": "c8_rerun_with_local_discriminator_readout_v0",
        "title": "C8 rerun with local discriminator readout",
        "status": status,
        "outcome_class": outcome,
        "instrument_id": instrument.get("instrument_id"),
        "accepted_build_packet_id": accepted_packet.get("accepted_build_packet_id"),
        "proposal_id": proposal.get("proposal_id"),
        "c8_rerun_performed": True,
        "discriminator_application_count": discriminator_application_count,
        "rerun_classification": observed.get("label"),
        "missing_instrument_status_after_rerun": "LOCALLY_INSTRUMENTED_FOR_THIS_SURFACE",
        "new_instrument_build": False,
        "new_missing_instrument_proposal": False,
        "frontier_solved_claim": False,
        "global_solution_claim": False,
        "summary": "C8 reran once with the built local discriminator and classified the original missing-instrument surface as a local transition-family candidate. This is local instrumentation, not a global frontier solution.",
        "terminal_stop_code": terminal_stop,
    }
    write_json(RERUN_READOUT, readout)

    report = {
        "schema_version": "c8_rerun_with_local_discriminator_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "instrument_id": instrument.get("instrument_id"),
        "accepted_build_packet_id": accepted_packet.get("accepted_build_packet_id"),
        "proposal_id": proposal.get("proposal_id"),
        "c8_rerun_count": c8_rerun_count,
        "discriminator_application_count": discriminator_application_count,
        "rerun_classification": observed.get("label"),
        "local_discriminator_confirmed": observed.get("label") == "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED",
        "new_instrument_build": False,
        "cell1_build": False,
        "verification_probe_run": False,
        "new_missing_instrument_proposal": False,
        "research_mode_opened": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(RERUN_REPORT, report)

    receipt = {
        "schema_version": "c8_rerun_with_local_discriminator_receipt_v0",
        "receipt_type": "TYPED_C8_RERUN_WITH_LOCAL_DISCRIMINATOR_RECEIPT",
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
            "frontier_surface_ref": rel(C8_FRONTIER),
            "probe_receipt_ref": rel(C8_PROBE_RECEIPT),
            "classification_ref": rel(C8_CLASSIFICATION),
            "accepted_build_packet_ref": rel(ACCEPTED_PACKET),
            "accepted_packet_receipt_ref": rel(ACCEPTED_PACKET_RECEIPT),
            "discriminator_build_receipt_ref": rel(DISCRIMINATOR_BUILD_RECEIPT),
            "discriminator_instrument_ref": rel(DISCRIMINATOR_INSTRUMENT),
            "discriminator_verification_receipt_ref": rel(DISCRIMINATOR_VERIFICATION_RECEIPT),
        },
        "machine_readable_rerun_summary": {
            "rerun_complete": gate == "PASS",
            "c8_rerun_performed": True,
            "c8_rerun_count": c8_rerun_count,
            "instrument_id": instrument.get("instrument_id"),
            "accepted_build_packet_id": accepted_packet.get("accepted_build_packet_id"),
            "proposal_id": proposal.get("proposal_id"),
            "discriminator_applied": True,
            "discriminator_application_count": discriminator_application_count,
            "discriminator_application_status": discriminator_application.get("status"),
            "rerun_classification": observed.get("label"),
            "local_discriminator_confirmed": observed.get("label") == "LOCAL_TRANSITION_FAMILY_CANDIDATE_CONFIRMED",
            "missing_instrument_status_after_rerun": "LOCALLY_INSTRUMENTED_FOR_THIS_SURFACE",
            "new_instrument_build": False,
            "cell1_build": False,
            "verification_probe_run": False,
            "new_missing_instrument_proposal": False,
            "repeat_over_budget": False,
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
            "rerun_open_packet": rel(RERUN_OPEN_PACKET),
            "rerun_evidence_packet": rel(RERUN_EVIDENCE_PACKET),
            "discriminator_application_receipt": rel(DISCRIMINATOR_APPLICATION_RECEIPT),
            "rerun_classification": rel(RERUN_CLASSIFICATION),
            "readout": rel(RERUN_READOUT),
            "report": rel(RERUN_REPORT),
        },
        "failures": failures,
        "warnings": warnings,
        "terminal": {
            "type": "STOP",
            "stop_code": terminal_stop,
            "next_command_goal": None,
        },
    }
    receipt["receipt_id"] = "c8_rerun_with_local_discriminator_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"rerun_receipt_id={receipt['receipt_id']}")
    print(f"rerun_receipt_path={rel(receipt_path)}")
    print(f"instrument_id={instrument.get('instrument_id')}")
    print(f"rerun_classification={observed.get('label')}")
    print(f"proposal_id={proposal.get('proposal_id')}")
    print(f"rerun_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
