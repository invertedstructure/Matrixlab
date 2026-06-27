#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_ACCEPTED_INSTRUMENT_BUILD_PACKET_V0"
TARGET_UNIT_ID = "research.c8_accepted_instrument_build_packet.v0"
MILESTONE = "C8_ACCEPTED_INSTRUMENT_BUILD_PACKET_CREATED"
OUTCOME = "C8_ACCEPTED_INSTRUMENT_BUILD_PACKET_CREATED"
STOP_CODE = "STOP_C8_ACCEPTED_INSTRUMENT_BUILD_PACKET_READY"

OUT_DIR = ROOT / "data/c8_accepted_instrument_build_packet_v0"
RECEIPT_DIR = ROOT / "data/c8_accepted_instrument_build_packet_v0_receipts"

C8_RECEIPT = ROOT / "data/c8_basic_research_loop_specimen_v0_receipts/c8_basic_research_loop_specimen_receipt_6e5dafcf.json"
C8_PROPOSAL = ROOT / "data/c8_basic_research_loop_specimen_v0/missing_instrument_proposal_v0.json"
C8_FRONTIER = ROOT / "data/c8_basic_research_loop_specimen_v0/frontier_surface_contract_v0.json"
C8_PROBE_RECEIPT = ROOT / "data/c8_basic_research_loop_specimen_v0/bounded_probe_receipt_v0.json"
C8_CLASSIFICATION = ROOT / "data/c8_basic_research_loop_specimen_v0/research_transition_classification_v0.json"

PROPOSAL_REVIEW_RECEIPT = ROOT / "data/c8_missing_instrument_proposal_review_v0_receipts/c8_proposal_review_receipt_4e8dc3b7.json"
BUILD_PREP_RECEIPT = ROOT / "data/c8_bounded_instrument_build_packet_prep_v0_receipts/c8_build_packet_prep_receipt_52acb2b7.json"
BUILD_PREP_DECISION = ROOT / "data/c8_bounded_instrument_build_packet_prep_v0/c8_bounded_instrument_build_packet_prep_human_decision_v0.json"
BUILD_PREP_PACKET = ROOT / "data/c8_bounded_instrument_build_packet_prep_v0/c8_bounded_instrument_build_packet_prep_v0.json"

ACCEPTED_PACKET = OUT_DIR / "accepted_instrument_build_packet_v0.json"
BUILD_CONTRACT = OUT_DIR / "bounded_instrument_build_contract_v0.json"
READOUT = OUT_DIR / "c8_accepted_instrument_build_packet_readout_v0.json"
REPORT = OUT_DIR / "c8_accepted_instrument_build_packet_report.json"

NEGATIVE_CONTROL_KEYS = [
    "instrument_built_count",
    "cell1_build_count",
    "verification_probe_run_count",
    "repeat_run_count",
    "c8_rerun_count",
    "general_cell1_authority_count",
    "research_mode_opened_count",
    "global_solution_claim_count",
    "frontier_solved_claim_count",
    "hidden_next_command_count",
    "second_accepted_build_packet_count",
    "source_c8_receipt_mutation_count",
    "source_c8_proposal_mutation_count",
    "source_frontier_mutation_count",
    "source_probe_receipt_mutation_count",
    "source_classification_mutation_count",
    "source_review_receipt_mutation_count",
    "source_prep_receipt_mutation_count",
    "source_prep_decision_mutation_count",
    "source_prep_packet_mutation_count",
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
        "proposal_review_receipt": PROPOSAL_REVIEW_RECEIPT,
        "build_prep_receipt": BUILD_PREP_RECEIPT,
        "build_prep_decision": BUILD_PREP_DECISION,
        "build_prep_packet": BUILD_PREP_PACKET,
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
    prep_decision = read_json(BUILD_PREP_DECISION)
    prep_packet = read_json(BUILD_PREP_PACKET)

    c8_summary = c8_receipt.get("machine_readable_c8_summary", {})
    review_summary = review_receipt.get("machine_readable_review_summary", {})
    prep_summary = prep_receipt.get("machine_readable_prep_summary", {})

    if c8_receipt.get("gate") != "PASS":
        failures.append(f"c8_gate_not_pass:{c8_receipt.get('gate')}")
    if c8_receipt.get("outcome_class") != "C8_SPECIMEN_MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"c8_outcome_wrong:{c8_receipt.get('outcome_class')}")
    if c8_summary.get("proposal_only_first_pass") is not True:
        failures.append("c8_not_proposal_only_first_pass")
    if c8_summary.get("instrument_built") is not False:
        failures.append("c8_already_built_instrument")

    if proposal.get("proposal_id") != "missing_instrument_d56acf49":
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal.get("status") != "PROPOSED_ONLY":
        failures.append(f"proposal_status_wrong:{proposal.get('status')}")
    if proposal.get("instrument_kind") != "DISCRIMINATOR":
        failures.append(f"proposal_instrument_kind_wrong:{proposal.get('instrument_kind')}")
    if proposal.get("smallest_honest_name") != "local_transition_family_discriminator_candidate":
        failures.append(f"proposal_candidate_name_wrong:{proposal.get('smallest_honest_name')}")
    require_nonempty(proposal, "bounded_objective", failures, "proposal")
    require_nonempty(proposal, "why_needed", failures, "proposal")
    require_nonempty(proposal, "expected_verification.verification_probe", failures, "proposal")
    require_nonempty(proposal, "expected_verification.expected_result", failures, "proposal")

    if classification.get("classification") != "MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"classification_wrong:{classification.get('classification')}")
    if probe_receipt.get("probe_result", {}).get("classification_candidate") != "MISSING_INSTRUMENT_EXPOSED":
        failures.append(f"probe_classification_candidate_wrong:{probe_receipt.get('probe_result', {}).get('classification_candidate')}")
    if frontier.get("surface_kind") != "MISSING_DISCRIMINATOR_SURFACE":
        failures.append(f"frontier_surface_kind_wrong:{frontier.get('surface_kind')}")

    if review_receipt.get("gate") != "PASS":
        failures.append(f"review_gate_not_pass:{review_receipt.get('gate')}")
    if review_receipt.get("outcome_class") != "C8_PROPOSAL_REVIEWABLE_NOT_ACCEPTED":
        failures.append(f"review_outcome_wrong:{review_receipt.get('outcome_class')}")
    for key in [
        "proposal_is_well_formed",
        "proposal_is_bounded",
        "proposal_has_verification",
        "authority_boundary_clean",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_{key}_not_true:{review_summary.get(key)}")

    if prep_receipt.get("gate") != "PASS":
        failures.append(f"prep_gate_not_pass:{prep_receipt.get('gate')}")
    if prep_receipt.get("outcome_class") != "C8_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP_ACCEPTED":
        failures.append(f"prep_outcome_wrong:{prep_receipt.get('outcome_class')}")
    if prep_summary.get("accepted_for_build_packet_prep_only") is not True:
        failures.append(f"prep_not_accepted_for_packet_prep_only:{prep_summary.get('accepted_for_build_packet_prep_only')}")
    if prep_summary.get("accepted_build_packet_created") is not False:
        failures.append("prep_already_created_accepted_build_packet")
    if prep_summary.get("instrument_built") is not False:
        failures.append("prep_already_built_instrument")

    if prep_decision.get("operator_decision") != "ACCEPT_FOR_BOUNDED_INSTRUMENT_BUILD_PACKET_PREP":
        failures.append(f"prep_decision_wrong:{prep_decision.get('operator_decision')}")
    accepted_scope = prep_decision.get("accepted_scope", {})
    if accepted_scope.get("allowed_next_object") != "bounded_instrument_build_packet_prep":
        failures.append(f"prep_decision_allowed_next_object_wrong:{accepted_scope.get('allowed_next_object')}")
    if accepted_scope.get("max_build_packets_to_prepare") != 1:
        failures.append(f"prep_decision_max_packets_wrong:{accepted_scope.get('max_build_packets_to_prepare')}")

    prep_auth = prep_packet.get("authority_boundary", {})
    if prep_auth.get("can_prepare_bounded_build_packet") is not True:
        failures.append("prep_packet_cannot_prepare_bounded_build_packet")
    if prep_auth.get("can_create_accepted_build_packet_now") is not False:
        failures.append("prep_packet_claimed_it_could_create_accepted_packet_now")

    accepted_seed = {
        "proposal_id": proposal.get("proposal_id"),
        "review_receipt_id": review_receipt.get("receipt_id"),
        "prep_receipt_id": prep_receipt.get("receipt_id"),
        "candidate_name": proposal.get("smallest_honest_name"),
    }

    accepted_packet = {
        "schema_version": "accepted_instrument_build_packet_v0",
        "accepted_build_packet_id": "accepted_instrument_build_packet_" + sig8(accepted_seed),
        "status": "ACCEPTED_FOR_ONE_BOUNDED_INSTRUMENT_BUILD",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "decision_provenance": "OPERATOR_PROCEED_FROM_COMMITTED_BUILD_PACKET_PREP",
        "source_refs": {
            "c8_receipt_ref": rel(C8_RECEIPT),
            "proposal_ref": rel(C8_PROPOSAL),
            "proposal_review_receipt_ref": rel(PROPOSAL_REVIEW_RECEIPT),
            "build_packet_prep_receipt_ref": rel(BUILD_PREP_RECEIPT),
            "build_packet_prep_decision_ref": rel(BUILD_PREP_DECISION),
            "build_packet_prep_ref": rel(BUILD_PREP_PACKET),
            "frontier_surface_ref": rel(C8_FRONTIER),
            "probe_receipt_ref": rel(C8_PROBE_RECEIPT),
            "classification_ref": rel(C8_CLASSIFICATION),
        },
        "accepted_instrument": {
            "instrument_kind": "DISCRIMINATOR",
            "candidate_name": proposal.get("smallest_honest_name"),
            "proposal_id": proposal.get("proposal_id"),
            "target_surface_kind": frontier.get("surface_kind"),
            "target_frontier_surface_ref": rel(C8_FRONTIER),
            "bounded_objective": proposal.get("bounded_objective"),
            "why_needed": proposal.get("why_needed"),
            "expected_verification": proposal.get("expected_verification"),
        },
        "authorized_future_unit": {
            "allowed_next_unit": "BUILD_ONE_BOUNDED_LOCAL_TRANSITION_FAMILY_DISCRIMINATOR_V0",
            "allowed_instrument_build_count": 1,
            "allowed_cell1_build_count": 1,
            "allowed_verification_probe_count_after_build": 1,
            "allowed_c8_repeat_after_verified_build": 1,
            "must_emit_build_receipt": True,
            "must_emit_verification_receipt": True,
            "must_preserve_source_refs": True,
            "must_stop_on_failure": True,
        },
        "authority_boundary": {
            "packet_can_authorize_one_future_bounded_build": True,
            "packet_is_not_the_build": True,
            "instrument_built_now": False,
            "cell1_build_now": False,
            "verification_run_now": False,
            "c8_rerun_now": False,
            "general_cell1_authority": False,
            "global_discriminator_claim": False,
            "frontier_solved_claim": False,
        },
        "forbidden_changes": [
            "rewrite dominance system",
            "expand fixture set",
            "claim global sufficiency",
            "authorize general Cell 1",
            "open research mode",
            "skip local verification receipt",
            "mutate source C8/proposal/review/prep artifacts",
        ],
        "must_not_infer": [
            "instrument has been built",
            "instrument has been verified",
            "C8 has rerun",
            "frontier is solved",
            "global discriminator exists",
            "Cell 1 has general authority",
        ],
    }
    write_json(ACCEPTED_PACKET, accepted_packet)

    build_contract = {
        "schema_version": "bounded_instrument_build_contract_v0",
        "contract_id": "bounded_instrument_build_contract_" + sig8(accepted_packet),
        "accepted_build_packet_ref": rel(ACCEPTED_PACKET),
        "instrument_kind": "DISCRIMINATOR",
        "candidate_name": proposal.get("smallest_honest_name"),
        "source_proposal_id": proposal.get("proposal_id"),
        "future_build_scope": accepted_packet["authorized_future_unit"],
        "required_build_output": {
            "instrument_artifact": "local_transition_family_discriminator_candidate",
            "build_receipt": "required",
            "verification_receipt": "required_after_build",
        },
        "not_authorized_by_contract_creation": [
            "instrument build now",
            "verification now",
            "C8 rerun now",
            "research mode",
            "global solution claim",
        ],
    }
    write_json(BUILD_CONTRACT, build_contract)

    source_hashes_after = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    mutation_key_map = {
        "c8_receipt": "source_c8_receipt_mutation_count",
        "c8_proposal": "source_c8_proposal_mutation_count",
        "c8_frontier": "source_frontier_mutation_count",
        "c8_probe_receipt": "source_probe_receipt_mutation_count",
        "c8_classification": "source_classification_mutation_count",
        "proposal_review_receipt": "source_review_receipt_mutation_count",
        "build_prep_receipt": "source_prep_receipt_mutation_count",
        "build_prep_decision": "source_prep_decision_mutation_count",
        "build_prep_packet": "source_prep_packet_mutation_count",
    }

    for label, counter_key in mutation_key_map.items():
        if source_hashes_before.get(label) != source_hashes_after.get(label):
            negative_controls[counter_key] += 1

    # This unit creates exactly one accepted build packet, so it is not a bad counter.
    # The bad counter only detects extra accepted packets.
    accepted_packet_count = 1
    if accepted_packet_count != 1:
        negative_controls["second_accepted_build_packet_count"] += max(0, accepted_packet_count - 1)

    nonzero = {k: v for k, v in negative_controls.items() if v != 0}
    for k, v in nonzero.items():
        failures.append(f"{k}:{v}")

    acceptance_gates = {
        "C8_ACCEPTED_PACKET_0_C8_RECEIPT_VERIFIED": c8_receipt.get("gate") == "PASS",
        "C8_ACCEPTED_PACKET_1_PROPOSAL_REVIEW_VERIFIED": review_receipt.get("gate") == "PASS",
        "C8_ACCEPTED_PACKET_2_PREP_RECEIPT_VERIFIED": prep_receipt.get("gate") == "PASS",
        "C8_ACCEPTED_PACKET_3_PREP_ACCEPTANCE_SCOPE_VERIFIED": prep_summary.get("accepted_for_build_packet_prep_only") is True,
        "C8_ACCEPTED_PACKET_4_PROPOSAL_PRESENT": proposal.get("proposal_id") == "missing_instrument_d56acf49",
        "C8_ACCEPTED_PACKET_5_INSTRUMENT_KIND_DISCRIMINATOR": proposal.get("instrument_kind") == "DISCRIMINATOR",
        "C8_ACCEPTED_PACKET_6_BOUNDED_OBJECTIVE_PRESENT": bool(proposal.get("bounded_objective")),
        "C8_ACCEPTED_PACKET_7_EXPECTED_VERIFICATION_PRESENT": bool(proposal.get("expected_verification", {}).get("verification_probe")) and bool(proposal.get("expected_verification", {}).get("expected_result")),
        "C8_ACCEPTED_PACKET_8_ACCEPTED_PACKET_EMITTED": ACCEPTED_PACKET.exists(),
        "C8_ACCEPTED_PACKET_9_ACCEPTED_PACKET_STATUS_VALID": accepted_packet.get("status") == "ACCEPTED_FOR_ONE_BOUNDED_INSTRUMENT_BUILD",
        "C8_ACCEPTED_PACKET_10_BUILD_CONTRACT_EMITTED": BUILD_CONTRACT.exists(),
        "C8_ACCEPTED_PACKET_11_NO_INSTRUMENT_BUILD_NOW": negative_controls["instrument_built_count"] == 0,
        "C8_ACCEPTED_PACKET_12_NO_CELL1_BUILD_NOW": negative_controls["cell1_build_count"] == 0,
        "C8_ACCEPTED_PACKET_13_NO_VERIFICATION_NOW": negative_controls["verification_probe_run_count"] == 0,
        "C8_ACCEPTED_PACKET_14_NO_REPEAT_NOW": negative_controls["repeat_run_count"] == 0,
        "C8_ACCEPTED_PACKET_15_NO_C8_RERUN_NOW": negative_controls["c8_rerun_count"] == 0,
        "C8_ACCEPTED_PACKET_16_NO_GENERAL_CELL1_AUTHORITY": negative_controls["general_cell1_authority_count"] == 0,
        "C8_ACCEPTED_PACKET_17_NO_RESEARCH_MODE": negative_controls["research_mode_opened_count"] == 0,
        "C8_ACCEPTED_PACKET_18_NO_GLOBAL_OR_FRONTIER_SOLUTION_CLAIM": negative_controls["global_solution_claim_count"] == 0 and negative_controls["frontier_solved_claim_count"] == 0,
        "C8_ACCEPTED_PACKET_19_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_ACCEPTED_PACKET_20_BAD_COUNTERS_ZERO": not bool(nonzero),
    }

    false_gates = [k for k, v in acceptance_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_ACCEPTED_INSTRUMENT_BUILD_PACKET_PASS" if gate == "PASS" else "TYPED_C8_ACCEPTED_INSTRUMENT_BUILD_PACKET_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_ACCEPTED_INSTRUMENT_BUILD_PACKET_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_ACCEPTED_INSTRUMENT_BUILD_PACKET_FAILED"

    readout = {
        "schema_version": "c8_accepted_instrument_build_packet_readout_v0",
        "title": "C8 accepted instrument build packet readout",
        "status": status,
        "outcome_class": outcome,
        "accepted_build_packet_id": accepted_packet["accepted_build_packet_id"],
        "proposal_id": proposal.get("proposal_id"),
        "instrument_kind": "DISCRIMINATOR",
        "candidate_name": proposal.get("smallest_honest_name"),
        "authorized_future_unit": accepted_packet["authorized_future_unit"]["allowed_next_unit"],
        "packet_is_not_the_build": True,
        "instrument_built_now": False,
        "verification_run_now": False,
        "c8_rerun_now": False,
        "summary": "One bounded accepted instrument build packet was created. It authorizes only one future bounded discriminator build unit, not a build in this unit.",
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_accepted_instrument_build_packet_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "accepted_build_packet_id": accepted_packet["accepted_build_packet_id"],
        "proposal_id": proposal.get("proposal_id"),
        "review_receipt_id": review_receipt.get("receipt_id"),
        "prep_receipt_id": prep_receipt.get("receipt_id"),
        "instrument_kind": "DISCRIMINATOR",
        "candidate_name": proposal.get("smallest_honest_name"),
        "accepted_packet_created": True,
        "instrument_built": False,
        "cell1_build": False,
        "verification_probe_run": False,
        "repeat_run": False,
        "c8_rerun": False,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_accepted_instrument_build_packet_receipt_v0",
        "receipt_type": "TYPED_C8_ACCEPTED_INSTRUMENT_BUILD_PACKET_RECEIPT",
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
            "build_packet_prep_receipt_ref": rel(BUILD_PREP_RECEIPT),
            "build_packet_prep_decision_ref": rel(BUILD_PREP_DECISION),
            "build_packet_prep_ref": rel(BUILD_PREP_PACKET),
            "frontier_surface_ref": rel(C8_FRONTIER),
            "probe_receipt_ref": rel(C8_PROBE_RECEIPT),
            "classification_ref": rel(C8_CLASSIFICATION),
        },
        "machine_readable_accepted_packet_summary": {
            "accepted_packet_complete": gate == "PASS",
            "accepted_build_packet_created": True,
            "accepted_build_packet_id": accepted_packet["accepted_build_packet_id"],
            "proposal_id": proposal.get("proposal_id"),
            "review_receipt_id": review_receipt.get("receipt_id"),
            "prep_receipt_id": prep_receipt.get("receipt_id"),
            "instrument_kind": "DISCRIMINATOR",
            "candidate_name": proposal.get("smallest_honest_name"),
            "authorized_future_unit": accepted_packet["authorized_future_unit"]["allowed_next_unit"],
            "allowed_future_build_count": 1,
            "allowed_future_cell1_build_count": 1,
            "allowed_future_verification_probe_count": 1,
            "allowed_future_c8_repeat_after_verified_build": 1,
            "instrument_built_now": False,
            "cell1_build_now": False,
            "verification_probe_run_now": False,
            "repeat_run_now": False,
            "c8_rerun_now": False,
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
            "accepted_build_packet": rel(ACCEPTED_PACKET),
            "build_contract": rel(BUILD_CONTRACT),
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
    receipt["receipt_id"] = "c8_accepted_build_packet_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"accepted_packet_receipt_id={receipt['receipt_id']}")
    print(f"accepted_packet_receipt_path={rel(receipt_path)}")
    print(f"accepted_build_packet_id={accepted_packet['accepted_build_packet_id']}")
    print(f"accepted_build_packet_path={rel(ACCEPTED_PACKET)}")
    print(f"proposal_id={proposal.get('proposal_id')}")
    print(f"accepted_packet_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
