#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_C8_MISSING_INSTRUMENT_PROPOSAL_V0"
TARGET_UNIT_ID = "research.c8_missing_instrument_proposal_review.v0"
MILESTONE = "C8_MISSING_INSTRUMENT_PROPOSAL_REVIEWED"
OUTCOME = "C8_PROPOSAL_REVIEWABLE_NOT_ACCEPTED"
STOP_CODE = "STOP_C8_MISSING_INSTRUMENT_PROPOSAL_REVIEW_READY_FOR_HUMAN_DECISION"

OUT_DIR = ROOT / "data/c8_missing_instrument_proposal_review_v0"
RECEIPT_DIR = ROOT / "data/c8_missing_instrument_proposal_review_v0_receipts"

C8_RECEIPT = ROOT / "data/c8_basic_research_loop_specimen_v0_receipts/c8_basic_research_loop_specimen_receipt_6e5dafcf.json"
C8_PROPOSAL = ROOT / "data/c8_basic_research_loop_specimen_v0/missing_instrument_proposal_v0.json"
C8_CLASSIFICATION = ROOT / "data/c8_basic_research_loop_specimen_v0/research_transition_classification_v0.json"
C8_PROBE_RECEIPT = ROOT / "data/c8_basic_research_loop_specimen_v0/bounded_probe_receipt_v0.json"
C8_FRONTIER = ROOT / "data/c8_basic_research_loop_specimen_v0/frontier_surface_contract_v0.json"
C8_ACCEPTED_STUB = ROOT / "data/c8_basic_research_loop_specimen_v0/accepted_instrument_build_packet_v0.json"

REVIEW_PACKET = OUT_DIR / "c8_missing_instrument_proposal_review_packet_v0.json"
REVIEW_REPORT = OUT_DIR / "c8_missing_instrument_proposal_review_report.json"
REVIEW_READOUT = OUT_DIR / "c8_missing_instrument_proposal_review_readout_v0.json"

NEGATIVE_CONTROL_KEYS = [
    "proposal_self_accepted_count",
    "accepted_build_packet_created_count",
    "accepted_build_packet_mutated_count",
    "instrument_built_count",
    "cell1_build_count",
    "verification_probe_run_count",
    "repeat_run_count",
    "source_c8_receipt_mutation_count",
    "source_c8_proposal_mutation_count",
    "source_classification_mutation_count",
    "source_probe_receipt_mutation_count",
    "source_frontier_mutation_count",
    "global_solution_claim_count",
    "frontier_solved_claim_count",
    "research_mode_opened_count",
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

def require_nonempty(obj: Dict[str, Any], path: str, failures: List[str], label: str) -> None:
    cur: Any = obj
    ok = True
    for part in path.split("."):
        if isinstance(cur, dict) and part in cur:
            cur = cur[part]
        else:
            ok = False
            break
    if (not ok) or cur in (None, "", []):
        failures.append(f"{label}:missing_or_empty:{path}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []
    negative_controls = zero_counters()

    sources = {
        "c8_receipt": C8_RECEIPT,
        "c8_proposal": C8_PROPOSAL,
        "c8_classification": C8_CLASSIFICATION,
        "c8_probe_receipt": C8_PROBE_RECEIPT,
        "c8_frontier": C8_FRONTIER,
        "c8_accepted_stub": C8_ACCEPTED_STUB,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {label: sha256_file(path) for label, path in sources.items() if path.exists()}

    c8_receipt = read_json(C8_RECEIPT)
    proposal = read_json(C8_PROPOSAL)
    classification = read_json(C8_CLASSIFICATION)
    probe_receipt = read_json(C8_PROBE_RECEIPT)
    frontier = read_json(C8_FRONTIER)
    accepted_stub = read_json(C8_ACCEPTED_STUB)

    c8_summary = c8_receipt.get("machine_readable_c8_summary", {})

    if c8_receipt.get("gate") != "PASS":
        failures.append(f"source_c8_gate_not_pass:{c8_receipt.get('gate')}")
    if c8_receipt.get("outcome_class") != "C8_SPECIMEN_MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"source_c8_outcome_wrong:{c8_receipt.get('outcome_class')}")
    if c8_receipt.get("terminal", {}).get("stop_code") != "STOP_C8_SPECIMEN_MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"source_c8_terminal_wrong:{c8_receipt.get('terminal', {}).get('stop_code')}")
    if c8_summary.get("proposal_only_first_pass") is not True:
        failures.append("source_c8_not_proposal_only_first_pass")
    if c8_summary.get("instrument_built") is not False:
        failures.append("source_c8_instrument_was_built")
    if c8_summary.get("proposal_self_accepted") is not False:
        failures.append("source_c8_proposal_self_accepted")
    if c8_summary.get("bad_counters_zero") is not True:
        failures.append("source_c8_bad_counters_not_zero")

    if classification.get("classification") != "MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"classification_not_missing_instrument:{classification.get('classification')}")
    require_nonempty(classification, "why", failures, "classification")

    if proposal.get("schema_version") != "missing_instrument_proposal_v0":
        failures.append(f"proposal_schema_wrong:{proposal.get('schema_version')}")
    if proposal.get("status") != "PROPOSED_ONLY":
        failures.append(f"proposal_status_wrong:{proposal.get('status')}")
    if proposal.get("instrument_kind") != "DISCRIMINATOR":
        failures.append(f"proposal_instrument_kind_wrong:{proposal.get('instrument_kind')}")

    require_nonempty(proposal, "proposal_id", failures, "proposal")
    require_nonempty(proposal, "smallest_honest_name", failures, "proposal")
    require_nonempty(proposal, "why_needed", failures, "proposal")
    require_nonempty(proposal, "bounded_objective", failures, "proposal")
    require_nonempty(proposal, "expected_verification.verification_probe", failures, "proposal")
    require_nonempty(proposal, "expected_verification.expected_result", failures, "proposal")

    auth = proposal.get("authority_boundary", {})
    if auth.get("can_propose") is not True:
        failures.append(f"proposal_can_propose_not_true:{auth.get('can_propose')}")
    if auth.get("can_apply") is not False:
        failures.append(f"proposal_can_apply_not_false:{auth.get('can_apply')}")
    if auth.get("requires_review") is not True:
        failures.append(f"proposal_requires_review_not_true:{auth.get('requires_review')}")

    expected_trigger_refs = {
        "frontier_surface_ref": rel(C8_FRONTIER),
        "probe_receipt_ref": rel(C8_PROBE_RECEIPT),
        "transition_classification_ref": rel(C8_CLASSIFICATION),
    }
    trigger = proposal.get("trigger", {})
    for key, expected in expected_trigger_refs.items():
        actual = trigger.get(key)
        if actual != expected:
            failures.append(f"proposal_trigger_{key}_wrong:{actual}!={expected}")

    for phrase in [
        "instrument accepted",
        "instrument built",
        "schema patched",
        "frontier solved",
        "builder authorized",
    ]:
        if phrase not in proposal.get("must_not_infer", []):
            failures.append(f"proposal_must_not_infer_missing:{phrase}")

    if accepted_stub.get("status") != "NOT_APPLICABLE_NO_ACCEPTED_BUILD_PACKET":
        failures.append(f"accepted_stub_status_wrong:{accepted_stub.get('status')}")
    if accepted_stub.get("created_by_runner_as_acceptance") is not False:
        failures.append("accepted_stub_created_by_runner_as_acceptance_not_false")
    if accepted_stub.get("accepted_for_cell1") is not False:
        failures.append("accepted_stub_accepted_for_cell1_not_false")

    if frontier.get("surface_kind") != "MISSING_DISCRIMINATOR_SURFACE":
        failures.append(f"frontier_surface_kind_wrong:{frontier.get('surface_kind')}")
    require_nonempty(frontier, "active_question", failures, "frontier")
    require_nonempty(frontier, "known_context.known_obstruction", failures, "frontier")

    probe_result = probe_receipt.get("probe_result", {})
    if probe_result.get("classification_candidate") != "MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"probe_classification_candidate_wrong:{probe_result.get('classification_candidate')}")
    if probe_result.get("observed_transition") in (None, "", []):
        failures.append("probe_observed_transition_missing")

    proposal_is_well_formed = not failures
    proposal_is_bounded = (
        proposal.get("instrument_kind") == "DISCRIMINATOR"
        and proposal.get("status") == "PROPOSED_ONLY"
        and auth.get("can_apply") is False
        and frontier.get("surface_kind") == "MISSING_DISCRIMINATOR_SURFACE"
    )
    proposal_has_verification = (
        bool(proposal.get("expected_verification", {}).get("verification_probe"))
        and bool(proposal.get("expected_verification", {}).get("expected_result"))
    )
    authority_boundary_clean = (
        auth.get("can_propose") is True
        and auth.get("can_apply") is False
        and auth.get("requires_review") is True
        and accepted_stub.get("accepted_for_cell1") is False
    )

    review_findings = [
        "Proposal is a bounded local discriminator candidate, not a patch.",
        "Proposal status remains PROPOSED_ONLY.",
        "Proposal may be accepted only by a separate human decision layer.",
        "No accepted build packet exists in the source C8 specimen.",
        "No instrument build, verification probe, repeat, or research-mode continuation is authorized by this review.",
    ]

    review_packet = {
        "schema_version": "c8_missing_instrument_proposal_review_packet_v0",
        "review_id": None,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "created_at": now_iso(),
        "source_refs": {
            "c8_receipt_ref": rel(C8_RECEIPT),
            "proposal_ref": rel(C8_PROPOSAL),
            "classification_ref": rel(C8_CLASSIFICATION),
            "probe_receipt_ref": rel(C8_PROBE_RECEIPT),
            "frontier_surface_ref": rel(C8_FRONTIER),
            "accepted_build_stub_ref": rel(C8_ACCEPTED_STUB),
        },
        "review_gate": "PASS" if not failures else "FAIL",
        "review_status": "TYPED_C8_MISSING_INSTRUMENT_PROPOSAL_REVIEW_PASS" if not failures else "TYPED_C8_MISSING_INSTRUMENT_PROPOSAL_REVIEW_FAIL",
        "decision_class": OUTCOME if not failures else "C8_PROPOSAL_REVIEW_FAILED",
        "proposal_review": {
            "proposal_id": proposal.get("proposal_id"),
            "proposal_status": proposal.get("status"),
            "instrument_kind": proposal.get("instrument_kind"),
            "smallest_honest_name": proposal.get("smallest_honest_name"),
            "proposal_is_well_formed": proposal_is_well_formed,
            "proposal_is_bounded": proposal_is_bounded,
            "proposal_has_verification": proposal_has_verification,
            "authority_boundary_clean": authority_boundary_clean,
            "review_findings": review_findings,
        },
        "human_decision_options": [
            "ACCEPT_FOR_SEPARATE_BUILD_PACKET",
            "REQUEST_REFINEMENT",
            "REJECT_PROPOSAL",
            "PARK_PROPOSAL",
        ],
        "recommended_next_human_decision": "ACCEPT_FOR_SEPARATE_BUILD_PACKET_OR_REQUEST_REFINEMENT",
        "not_authorized_by_this_review": [
            "accepted build packet",
            "instrument build",
            "Cell 1 build",
            "verification probe",
            "repeat run",
            "research mode",
            "global solution claim",
            "frontier solved claim",
            "future C8 specimen",
        ],
        "must_not_infer": [
            "proposal accepted",
            "instrument accepted",
            "instrument built",
            "Cell 1 authorized",
            "C8 may rerun without an accepted build packet",
            "frontier solved",
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": STOP_CODE if not failures else "STOP_C8_MISSING_INSTRUMENT_PROPOSAL_REVIEW_FAILED",
            "next_command_goal": None,
        },
    }
    review_packet["review_id"] = "c8_proposal_review_" + sig8(review_packet)
    write_json(REVIEW_PACKET, review_packet)

    source_hashes_after = {label: sha256_file(path) for label, path in sources.items() if path.exists()}

    if source_hashes_before.get("c8_receipt") != source_hashes_after.get("c8_receipt"):
        negative_controls["source_c8_receipt_mutation_count"] += 1
    if source_hashes_before.get("c8_proposal") != source_hashes_after.get("c8_proposal"):
        negative_controls["source_c8_proposal_mutation_count"] += 1
    if source_hashes_before.get("c8_classification") != source_hashes_after.get("c8_classification"):
        negative_controls["source_classification_mutation_count"] += 1
    if source_hashes_before.get("c8_probe_receipt") != source_hashes_after.get("c8_probe_receipt"):
        negative_controls["source_probe_receipt_mutation_count"] += 1
    if source_hashes_before.get("c8_frontier") != source_hashes_after.get("c8_frontier"):
        negative_controls["source_frontier_mutation_count"] += 1

    nonzero = {k: v for k, v in negative_controls.items() if v != 0}
    for key, value in nonzero.items():
        failures.append(f"{key}:{value}")

    acceptance_gates = {
        "C8_PROPOSAL_REVIEW_0_C8_RECEIPT_VERIFIED": c8_receipt.get("gate") == "PASS",
        "C8_PROPOSAL_REVIEW_1_SOURCE_OUTCOME_MISSING_INSTRUMENT_EXPOSED": c8_receipt.get("outcome_class") == "C8_SPECIMEN_MISSING_INSTRUMENT_EXPOSED",
        "C8_PROPOSAL_REVIEW_2_PROPOSAL_PRESENT": C8_PROPOSAL.exists(),
        "C8_PROPOSAL_REVIEW_3_PROPOSAL_STATUS_PROPOSED_ONLY": proposal.get("status") == "PROPOSED_ONLY",
        "C8_PROPOSAL_REVIEW_4_INSTRUMENT_KIND_DISCRIMINATOR": proposal.get("instrument_kind") == "DISCRIMINATOR",
        "C8_PROPOSAL_REVIEW_5_TRIGGER_REFS_MATCH_SOURCE_ARTIFACTS": trigger == expected_trigger_refs,
        "C8_PROPOSAL_REVIEW_6_AUTHORITY_BOUNDARY_CLEAN": authority_boundary_clean,
        "C8_PROPOSAL_REVIEW_7_BOUNDED_OBJECTIVE_PRESENT": bool(proposal.get("bounded_objective")),
        "C8_PROPOSAL_REVIEW_8_EXPECTED_VERIFICATION_PRESENT": proposal_has_verification,
        "C8_PROPOSAL_REVIEW_9_NO_ACCEPTED_BUILD_PACKET_CREATED": negative_controls["accepted_build_packet_created_count"] == 0,
        "C8_PROPOSAL_REVIEW_10_NO_PROPOSAL_SELF_ACCEPTANCE": negative_controls["proposal_self_accepted_count"] == 0,
        "C8_PROPOSAL_REVIEW_11_NO_INSTRUMENT_BUILD": negative_controls["instrument_built_count"] == 0,
        "C8_PROPOSAL_REVIEW_12_NO_CELL1_BUILD": negative_controls["cell1_build_count"] == 0,
        "C8_PROPOSAL_REVIEW_13_NO_VERIFICATION_PROBE_RUN": negative_controls["verification_probe_run_count"] == 0,
        "C8_PROPOSAL_REVIEW_14_NO_REPEAT_RUN": negative_controls["repeat_run_count"] == 0,
        "C8_PROPOSAL_REVIEW_15_NO_RESEARCH_MODE_OPENED": negative_controls["research_mode_opened_count"] == 0,
        "C8_PROPOSAL_REVIEW_16_NO_GLOBAL_OR_FRONTIER_SOLUTION_CLAIM": negative_controls["global_solution_claim_count"] == 0 and negative_controls["frontier_solved_claim_count"] == 0,
        "C8_PROPOSAL_REVIEW_17_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_PROPOSAL_REVIEW_18_REVIEW_PACKET_EMITTED": REVIEW_PACKET.exists(),
        "C8_PROPOSAL_REVIEW_19_BAD_COUNTERS_ZERO": not bool(nonzero),
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_MISSING_INSTRUMENT_PROPOSAL_REVIEW_PASS" if gate == "PASS" else "TYPED_C8_MISSING_INSTRUMENT_PROPOSAL_REVIEW_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_PROPOSAL_REVIEW_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_MISSING_INSTRUMENT_PROPOSAL_REVIEW_FAILED"

    report = {
        "schema_version": "c8_missing_instrument_proposal_review_report_v0",
        "review_id": review_packet["review_id"],
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_status": proposal.get("status"),
        "instrument_kind": proposal.get("instrument_kind"),
        "review_findings": review_findings,
        "human_decision_options": review_packet["human_decision_options"],
        "recommended_next_human_decision": review_packet["recommended_next_human_decision"],
        "not_authorized_by_this_review": review_packet["not_authorized_by_this_review"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REVIEW_REPORT, report)

    readout = {
        "schema_version": "c8_missing_instrument_proposal_review_readout_v0",
        "title": "C8 missing instrument proposal review readout",
        "review_id": review_packet["review_id"],
        "proposal_id": proposal.get("proposal_id"),
        "proposal_status": proposal.get("status"),
        "instrument_kind": proposal.get("instrument_kind"),
        "smallest_honest_name": proposal.get("smallest_honest_name"),
        "review_gate": gate,
        "outcome_class": outcome,
        "decision": "reviewed, not accepted",
        "summary": "The proposal is reviewable as a bounded local discriminator candidate. This review does not accept, build, verify, repeat, or open research mode.",
        "next_human_decision_options": review_packet["human_decision_options"],
        "terminal_stop_code": terminal_stop,
    }
    write_json(REVIEW_READOUT, readout)

    receipt = {
        "schema_version": "c8_missing_instrument_proposal_review_receipt_v0",
        "receipt_type": "TYPED_C8_MISSING_INSTRUMENT_PROPOSAL_REVIEW_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_refs": review_packet["source_refs"],
        "machine_readable_review_summary": {
            "proposal_review_complete": gate == "PASS",
            "proposal_id": proposal.get("proposal_id"),
            "proposal_status": proposal.get("status"),
            "instrument_kind": proposal.get("instrument_kind"),
            "proposal_is_well_formed": proposal_is_well_formed,
            "proposal_is_bounded": proposal_is_bounded,
            "proposal_has_verification": proposal_has_verification,
            "authority_boundary_clean": authority_boundary_clean,
            "review_decision": "REVIEWABLE_NOT_ACCEPTED" if gate == "PASS" else "REVIEW_FAILED",
            "accepted_build_packet_created": False,
            "instrument_built": False,
            "cell1_build": False,
            "verification_probe_run": False,
            "repeat_run": False,
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
            "review_packet": rel(REVIEW_PACKET),
            "review_report": rel(REVIEW_REPORT),
            "review_readout": rel(REVIEW_READOUT),
        },
        "failures": failures,
        "warnings": warnings,
        "terminal": {
            "type": "STOP",
            "stop_code": terminal_stop,
            "next_command_goal": None,
        },
    }
    receipt["receipt_id"] = "c8_proposal_review_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"review_receipt_id={receipt['receipt_id']}")
    print(f"review_receipt_path={rel(receipt_path)}")
    print(f"review_id={review_packet['review_id']}")
    print(f"proposal_id={proposal.get('proposal_id')}")
    print(f"review_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
