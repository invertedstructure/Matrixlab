#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_FOR_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP"
TARGET_UNIT_ID = "research.c8_bounded_instrument_build_packet_prep.v0"
MILESTONE = "C8_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP_ACCEPTED"
OUTCOME = "C8_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP_ACCEPTED"
STOP_CODE = "STOP_C8_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP_READY"

OUT_DIR = ROOT / "data/c8_bounded_instrument_build_packet_prep_v0"
RECEIPT_DIR = ROOT / "data/c8_bounded_instrument_build_packet_prep_v0_receipts"

C8_RECEIPT = ROOT / "data/c8_basic_research_loop_specimen_v0_receipts/c8_basic_research_loop_specimen_receipt_6e5dafcf.json"
C8_PROPOSAL = ROOT / "data/c8_basic_research_loop_specimen_v0/missing_instrument_proposal_v0.json"
C8_FRONTIER = ROOT / "data/c8_basic_research_loop_specimen_v0/frontier_surface_contract_v0.json"
C8_PROBE_RECEIPT = ROOT / "data/c8_basic_research_loop_specimen_v0/bounded_probe_receipt_v0.json"
C8_CLASSIFICATION = ROOT / "data/c8_basic_research_loop_specimen_v0/research_transition_classification_v0.json"
C8_ACCEPTED_BUILD_STUB = ROOT / "data/c8_basic_research_loop_specimen_v0/accepted_instrument_build_packet_v0.json"

PROPOSAL_REVIEW_RECEIPT = ROOT / "data/c8_missing_instrument_proposal_review_v0_receipts/c8_proposal_review_receipt_4e8dc3b7.json"
PROPOSAL_REVIEW_PACKET = ROOT / "data/c8_missing_instrument_proposal_review_v0/c8_missing_instrument_proposal_review_packet_v0.json"
PROPOSAL_REVIEW_REPORT = ROOT / "data/c8_missing_instrument_proposal_review_v0/c8_missing_instrument_proposal_review_report.json"

HUMAN_DECISION_PACKET = OUT_DIR / "c8_bounded_instrument_build_packet_prep_human_decision_v0.json"
PREP_PACKET = OUT_DIR / "c8_bounded_instrument_build_packet_prep_v0.json"
PREP_READOUT = OUT_DIR / "c8_bounded_instrument_build_packet_prep_readout_v0.json"
PREP_REPORT = OUT_DIR / "c8_bounded_instrument_build_packet_prep_report.json"

NEGATIVE_CONTROL_KEYS = [
    "accepted_build_packet_created_count",
    "instrument_built_count",
    "cell1_build_count",
    "verification_probe_run_count",
    "repeat_run_count",
    "c8_rerun_count",
    "proposal_self_accepted_count",
    "general_cell1_authority_count",
    "research_mode_opened_count",
    "global_solution_claim_count",
    "frontier_solved_claim_count",
    "hidden_next_command_count",
    "source_c8_receipt_mutation_count",
    "source_c8_proposal_mutation_count",
    "source_frontier_mutation_count",
    "source_probe_receipt_mutation_count",
    "source_classification_mutation_count",
    "source_review_receipt_mutation_count",
    "source_review_packet_mutation_count",
    "source_review_report_mutation_count",
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
        "c8_frontier": C8_FRONTIER,
        "c8_probe_receipt": C8_PROBE_RECEIPT,
        "c8_classification": C8_CLASSIFICATION,
        "c8_accepted_build_stub": C8_ACCEPTED_BUILD_STUB,
        "proposal_review_receipt": PROPOSAL_REVIEW_RECEIPT,
        "proposal_review_packet": PROPOSAL_REVIEW_PACKET,
        "proposal_review_report": PROPOSAL_REVIEW_REPORT,
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
    accepted_stub = read_json(C8_ACCEPTED_BUILD_STUB)
    review_receipt = read_json(PROPOSAL_REVIEW_RECEIPT)
    review_packet = read_json(PROPOSAL_REVIEW_PACKET)
    review_report = read_json(PROPOSAL_REVIEW_REPORT)

    c8_summary = c8_receipt.get("machine_readable_c8_summary", {})
    review_summary = review_receipt.get("machine_readable_review_summary", {})

    if c8_receipt.get("gate") != "PASS":
        failures.append(f"c8_gate_not_pass:{c8_receipt.get('gate')}")
    if c8_receipt.get("outcome_class") != "C8_SPECIMEN_MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"c8_outcome_wrong:{c8_receipt.get('outcome_class')}")
    if c8_summary.get("proposal_only_first_pass") is not True:
        failures.append("c8_not_proposal_only_first_pass")
    if c8_summary.get("instrument_built") is not False:
        failures.append("c8_already_built_instrument")
    if c8_summary.get("proposal_self_accepted") is not False:
        failures.append("c8_proposal_self_accepted")
    if c8_summary.get("bad_counters_zero") is not True:
        failures.append("c8_bad_counters_not_zero")

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

    if classification.get("classification") != "MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"classification_wrong:{classification.get('classification')}")
    if probe_receipt.get("probe_result", {}).get("classification_candidate") != "MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"probe_classification_candidate_wrong:{probe_receipt.get('probe_result', {}).get('classification_candidate')}")
    if frontier.get("surface_kind") != "MISSING_DISCRIMINATOR_SURFACE":
        failures.append(f"frontier_surface_kind_wrong:{frontier.get('surface_kind')}")

    if accepted_stub.get("status") != "NOT_APPLICABLE_NO_ACCEPTED_BUILD_PACKET":
        failures.append(f"accepted_build_stub_status_wrong:{accepted_stub.get('status')}")
    if accepted_stub.get("accepted_for_cell1") is not False:
        failures.append("accepted_build_stub_already_accepted_for_cell1")
    if accepted_stub.get("created_by_runner_as_acceptance") is not False:
        failures.append("accepted_build_stub_created_by_runner_as_acceptance")

    if review_receipt.get("gate") != "PASS":
        failures.append(f"proposal_review_gate_not_pass:{review_receipt.get('gate')}")
    if review_receipt.get("outcome_class") != "C8_PROPOSAL_REVIEWABLE_NOT_ACCEPTED":
        failures.append(f"proposal_review_outcome_wrong:{review_receipt.get('outcome_class')}")
    if review_summary.get("review_decision") != "REVIEWABLE_NOT_ACCEPTED":
        failures.append(f"proposal_review_decision_wrong:{review_summary.get('review_decision')}")
    for key in [
        "proposal_is_well_formed",
        "proposal_is_bounded",
        "proposal_has_verification",
        "authority_boundary_clean",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"proposal_review_{key}_not_true:{review_summary.get(key)}")
    for key in [
        "accepted_build_packet_created",
        "instrument_built",
        "cell1_build",
        "verification_probe_run",
        "repeat_run",
        "research_mode_opened",
        "global_solution_claim",
        "frontier_solved_claim",
        "source_artifacts_mutated",
    ]:
        if review_summary.get(key) is not False:
            failures.append(f"proposal_review_{key}_not_false:{review_summary.get(key)}")

    decision_seed = {
        "operator_decision": "ACCEPT_FOR_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP",
        "proposal_id": proposal.get("proposal_id"),
        "review_receipt_id": review_receipt.get("receipt_id"),
        "instrument_kind": proposal.get("instrument_kind"),
    }

    human_decision = {
        "schema_version": "c8_bounded_instrument_build_packet_prep_human_decision_v0",
        "decision_id": "c8_bounded_instrument_build_prep_decision_" + sig8(decision_seed),
        "operator_decision": "ACCEPT_FOR_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP",
        "decision_provenance": "OPERATOR_DECLARED_CURRENT_COMMAND",
        "source_proposal_ref": rel(C8_PROPOSAL),
        "source_proposal_review_receipt_ref": rel(PROPOSAL_REVIEW_RECEIPT),
        "accepted_scope": {
            "allowed_next_object": "bounded_instrument_build_packet_prep",
            "instrument_kind": "DISCRIMINATOR",
            "candidate_name": proposal.get("smallest_honest_name"),
            "target_frontier_surface_ref": rel(C8_FRONTIER),
            "max_build_packets_to_prepare": 1,
            "max_instruments_to_build": 0,
            "max_cell1_builds": 0,
            "max_verification_probes": 0,
            "max_repeats": 0,
        },
        "not_authorized": [
            "accepted_instrument_build_packet_v0",
            "instrument build",
            "Cell 1 build",
            "verification probe",
            "repeat run",
            "C8 rerun",
            "general Cell 1 authority",
            "research mode",
            "global solution claim",
            "frontier solved claim",
            "future C8 specimen",
        ],
        "must_not_infer": [
            "instrument accepted for build",
            "accepted build packet already exists",
            "builder may patch now",
            "Cell 1 may build now",
            "C8 may rerun now",
            "frontier is solved",
        ],
    }
    write_json(HUMAN_DECISION_PACKET, human_decision)

    prep_seed = {
        "decision_id": human_decision["decision_id"],
        "proposal_id": proposal.get("proposal_id"),
        "review_receipt_id": review_receipt.get("receipt_id"),
    }

    prep_packet = {
        "schema_version": "c8_bounded_instrument_build_packet_prep_v0",
        "prep_packet_id": "c8_bounded_instrument_build_packet_prep_" + sig8(prep_seed),
        "status": "ACCEPTED_FOR_BUILD_PACKET_PREP_ONLY",
        "source_refs": {
            "c8_receipt_ref": rel(C8_RECEIPT),
            "proposal_ref": rel(C8_PROPOSAL),
            "proposal_review_receipt_ref": rel(PROPOSAL_REVIEW_RECEIPT),
            "proposal_review_packet_ref": rel(PROPOSAL_REVIEW_PACKET),
            "frontier_surface_ref": rel(C8_FRONTIER),
            "probe_receipt_ref": rel(C8_PROBE_RECEIPT),
            "classification_ref": rel(C8_CLASSIFICATION),
        },
        "bounded_build_packet_prep": {
            "instrument_kind": "DISCRIMINATOR",
            "candidate_name": proposal.get("smallest_honest_name"),
            "source_proposal_status": proposal.get("status"),
            "target_surface_kind": frontier.get("surface_kind"),
            "target_frontier_surface_ref": rel(C8_FRONTIER),
            "bounded_objective": proposal.get("bounded_objective"),
            "why_needed": proposal.get("why_needed"),
            "expected_verification": proposal.get("expected_verification"),
            "allowed_future_packet_type": "accepted_instrument_build_packet_v0",
            "allowed_future_packet_count": 1,
            "future_packet_must_reference": [
                rel(C8_PROPOSAL),
                rel(PROPOSAL_REVIEW_RECEIPT),
                rel(HUMAN_DECISION_PACKET),
                rel(PREP_PACKET),
            ],
            "future_packet_forbidden_changes": [
                "rewrite dominance system",
                "expand fixture set",
                "claim global sufficiency",
                "authorize general Cell 1",
                "open research mode",
                "skip local verification requirement",
            ],
        },
        "authority_boundary": {
            "can_prepare_bounded_build_packet": True,
            "can_create_accepted_build_packet_now": False,
            "can_build_instrument": False,
            "can_run_verification": False,
            "can_repeat_c8": False,
            "requires_next_review_before_build_packet_creation": True,
        },
        "terminal": {
            "type": "STOP",
            "stop_code": STOP_CODE,
            "next_command_goal": None,
        },
        "must_not_infer": [
            "accepted_instrument_build_packet_v0 exists",
            "instrument is built",
            "instrument is accepted globally",
            "Cell 1 has build authority",
            "verification is authorized",
            "C8 may rerun",
            "frontier is solved",
        ],
    }
    write_json(PREP_PACKET, prep_packet)

    source_hashes_after = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    if source_hashes_before.get("c8_receipt") != source_hashes_after.get("c8_receipt"):
        negative_controls["source_c8_receipt_mutation_count"] += 1
    if source_hashes_before.get("c8_proposal") != source_hashes_after.get("c8_proposal"):
        negative_controls["source_c8_proposal_mutation_count"] += 1
    if source_hashes_before.get("c8_frontier") != source_hashes_after.get("c8_frontier"):
        negative_controls["source_frontier_mutation_count"] += 1
    if source_hashes_before.get("c8_probe_receipt") != source_hashes_after.get("c8_probe_receipt"):
        negative_controls["source_probe_receipt_mutation_count"] += 1
    if source_hashes_before.get("c8_classification") != source_hashes_after.get("c8_classification"):
        negative_controls["source_classification_mutation_count"] += 1
    if source_hashes_before.get("proposal_review_receipt") != source_hashes_after.get("proposal_review_receipt"):
        negative_controls["source_review_receipt_mutation_count"] += 1
    if source_hashes_before.get("proposal_review_packet") != source_hashes_after.get("proposal_review_packet"):
        negative_controls["source_review_packet_mutation_count"] += 1
    if source_hashes_before.get("proposal_review_report") != source_hashes_after.get("proposal_review_report"):
        negative_controls["source_review_report_mutation_count"] += 1

    nonzero = {k: v for k, v in negative_controls.items() if v != 0}
    for k, v in nonzero.items():
        failures.append(f"{k}:{v}")

    acceptance_gates = {
        "C8_BUILD_PREP_0_C8_RECEIPT_VERIFIED": c8_receipt.get("gate") == "PASS",
        "C8_BUILD_PREP_1_C8_OUTCOME_MISSING_INSTRUMENT_EXPOSED": c8_receipt.get("outcome_class") == "C8_SPECIMEN_MISSING_INSTRUMENT_EXPOSED",
        "C8_BUILD_PREP_2_PROPOSAL_PRESENT": C8_PROPOSAL.exists(),
        "C8_BUILD_PREP_3_PROPOSAL_STATUS_PROPOSED_ONLY": proposal.get("status") == "PROPOSED_ONLY",
        "C8_BUILD_PREP_4_PROPOSAL_REVIEW_PASS_VERIFIED": review_receipt.get("gate") == "PASS",
        "C8_BUILD_PREP_5_PROPOSAL_REVIEWABLE_NOT_ACCEPTED": review_receipt.get("outcome_class") == "C8_PROPOSAL_REVIEWABLE_NOT_ACCEPTED",
        "C8_BUILD_PREP_6_HUMAN_DECISION_PACKET_EMITTED": HUMAN_DECISION_PACKET.exists(),
        "C8_BUILD_PREP_7_OPERATOR_DECISION_ACCEPT_PREP_ONLY": human_decision.get("operator_decision") == "ACCEPT_FOR_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP",
        "C8_BUILD_PREP_8_PREP_PACKET_EMITTED": PREP_PACKET.exists(),
        "C8_BUILD_PREP_9_PREP_STATUS_ACCEPTED_FOR_PREP_ONLY": prep_packet.get("status") == "ACCEPTED_FOR_BUILD_PACKET_PREP_ONLY",
        "C8_BUILD_PREP_10_INSTRUMENT_KIND_DISCRIMINATOR": proposal.get("instrument_kind") == "DISCRIMINATOR",
        "C8_BUILD_PREP_11_BOUNDED_OBJECTIVE_PRESENT": bool(proposal.get("bounded_objective")),
        "C8_BUILD_PREP_12_EXPECTED_VERIFICATION_PRESENT": bool(proposal.get("expected_verification", {}).get("verification_probe")) and bool(proposal.get("expected_verification", {}).get("expected_result")),
        "C8_BUILD_PREP_13_NO_ACCEPTED_BUILD_PACKET_CREATED": negative_controls["accepted_build_packet_created_count"] == 0,
        "C8_BUILD_PREP_14_NO_INSTRUMENT_BUILD": negative_controls["instrument_built_count"] == 0,
        "C8_BUILD_PREP_15_NO_CELL1_BUILD": negative_controls["cell1_build_count"] == 0,
        "C8_BUILD_PREP_16_NO_VERIFICATION_PROBE_RUN": negative_controls["verification_probe_run_count"] == 0,
        "C8_BUILD_PREP_17_NO_REPEAT_RUN": negative_controls["repeat_run_count"] == 0,
        "C8_BUILD_PREP_18_NO_C8_RERUN": negative_controls["c8_rerun_count"] == 0,
        "C8_BUILD_PREP_19_NO_GENERAL_CELL1_AUTHORITY": negative_controls["general_cell1_authority_count"] == 0,
        "C8_BUILD_PREP_20_NO_RESEARCH_MODE_OPENED": negative_controls["research_mode_opened_count"] == 0,
        "C8_BUILD_PREP_21_NO_GLOBAL_OR_FRONTIER_SOLUTION_CLAIM": negative_controls["global_solution_claim_count"] == 0 and negative_controls["frontier_solved_claim_count"] == 0,
        "C8_BUILD_PREP_22_NO_HIDDEN_NEXT_COMMAND": negative_controls["hidden_next_command_count"] == 0,
        "C8_BUILD_PREP_23_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_BUILD_PREP_24_BAD_COUNTERS_ZERO": not bool(nonzero),
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP_PASS" if gate == "PASS" else "TYPED_C8_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP_FAILED"

    readout = {
        "schema_version": "c8_bounded_instrument_build_packet_prep_readout_v0",
        "title": "C8 bounded instrument build packet prep readout",
        "decision": human_decision["operator_decision"],
        "status": status,
        "outcome_class": outcome,
        "proposal_id": proposal.get("proposal_id"),
        "instrument_kind": proposal.get("instrument_kind"),
        "candidate_name": proposal.get("smallest_honest_name"),
        "prep_status": prep_packet["status"],
        "authorized_now": [
            "prepare one bounded accepted_instrument_build_packet_v0 candidate in a future unit",
        ],
        "not_authorized_now": human_decision["not_authorized"],
        "summary": "Human decision accepts the reviewed proposal only for bounded build-packet preparation. No accepted build packet, instrument build, Cell 1 build, verification, repeat, or C8 rerun occurred.",
        "terminal_stop_code": terminal_stop,
    }
    write_json(PREP_READOUT, readout)

    report = {
        "schema_version": "c8_bounded_instrument_build_packet_prep_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "proposal_id": proposal.get("proposal_id"),
        "review_receipt_id": review_receipt.get("receipt_id"),
        "decision_id": human_decision["decision_id"],
        "prep_packet_id": prep_packet["prep_packet_id"],
        "accepted_build_packet_created": False,
        "instrument_built": False,
        "cell1_build": False,
        "verification_probe_run": False,
        "repeat_run": False,
        "c8_rerun": False,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(PREP_REPORT, report)

    receipt = {
        "schema_version": "c8_bounded_instrument_build_packet_prep_receipt_v0",
        "receipt_type": "TYPED_C8_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP_RECEIPT",
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
            "proposal_review_packet_ref": rel(PROPOSAL_REVIEW_PACKET),
            "frontier_surface_ref": rel(C8_FRONTIER),
            "probe_receipt_ref": rel(C8_PROBE_RECEIPT),
            "classification_ref": rel(C8_CLASSIFICATION),
            "accepted_build_stub_ref": rel(C8_ACCEPTED_BUILD_STUB),
        },
        "machine_readable_prep_summary": {
            "prep_complete": gate == "PASS",
            "operator_decision": "ACCEPT_FOR_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP",
            "proposal_id": proposal.get("proposal_id"),
            "proposal_status": proposal.get("status"),
            "review_receipt_id": review_receipt.get("receipt_id"),
            "review_outcome": review_receipt.get("outcome_class"),
            "instrument_kind": proposal.get("instrument_kind"),
            "candidate_name": proposal.get("smallest_honest_name"),
            "prep_status": prep_packet["status"],
            "accepted_for_build_packet_prep_only": True,
            "accepted_build_packet_created": False,
            "instrument_built": False,
            "cell1_build": False,
            "verification_probe_run": False,
            "repeat_run": False,
            "c8_rerun": False,
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
            "human_decision_packet": rel(HUMAN_DECISION_PACKET),
            "prep_packet": rel(PREP_PACKET),
            "prep_readout": rel(PREP_READOUT),
            "prep_report": rel(PREP_REPORT),
        },
        "failures": failures,
        "warnings": warnings,
        "terminal": {
            "type": "STOP",
            "stop_code": terminal_stop,
            "next_command_goal": None,
        },
    }
    receipt["receipt_id"] = "c8_build_packet_prep_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"prep_receipt_id={receipt['receipt_id']}")
    print(f"prep_receipt_path={rel(receipt_path)}")
    print(f"decision_id={human_decision['decision_id']}")
    print(f"prep_packet_id={prep_packet['prep_packet_id']}")
    print(f"proposal_id={proposal.get('proposal_id')}")
    print(f"prep_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
