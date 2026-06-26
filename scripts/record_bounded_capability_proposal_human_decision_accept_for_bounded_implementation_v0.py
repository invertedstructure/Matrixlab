#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "RECORD_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_ACCEPT_FOR_BOUNDED_IMPLEMENTATION_V0"
TARGET_UNIT_ID = "bounded_capability_proposal.human_decision_accept_for_bounded_implementation_v0"
NEXT_UNIT_ID = "PREPARE_ACCEPTED_BOUNDED_CAPABILITY_PROPOSAL_IMPLEMENTATION_PATH_V0"

HUMAN_DECISION_REVIEW_RECEIPT_ID = "bounded_capability_proposal_human_decision_packet_review_receipt_0550dc96"
PROPOSAL_ID = "capability_proposal_57dda6e9"
SELECTED_DECISION = "ACCEPT_FOR_BOUNDED_IMPLEMENTATION"

HUMAN_DECISION_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_human_decision_packet_review_v0_receipts/bounded_capability_proposal_human_decision_packet_review_receipt_0550dc96.json"
HUMAN_DECISION_REQUEST_PACKET_PATH = ROOT / "data/bounded_capability_proposal_human_decision_packet_review_v0/bounded_capability_proposal_human_decision_request_packet_v0.json"
DECISION_EFFECTS_MAP_PATH = ROOT / "data/bounded_capability_proposal_human_decision_packet_review_v0/bounded_capability_proposal_human_decision_effects_map_v0.json"
BOUNDARY_REVIEW_PATH = ROOT / "data/bounded_capability_proposal_human_decision_packet_review_v0/bounded_capability_proposal_human_decision_boundary_review_v0.json"

VALIDATION_RUN_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0_receipts/bounded_capability_proposal_validation_path_run_receipt_375954b6.json"
VALIDATION_SUMMARY_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0/bounded_capability_proposal_validation_admissibility_summary_v0.json"

PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
HUMAN_DECISION_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/human_capability_decision_packet_v0.json"
STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"

OUT_DIR = ROOT / "data/bounded_capability_proposal_human_decision_accept_for_bounded_implementation_v0"
RECEIPT_DIR = ROOT / "data/bounded_capability_proposal_human_decision_accept_for_bounded_implementation_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_accept_basis_v0.json"
DECISION_RECORD_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_record_v0.json"
DECISION_EFFECT_APPLIED_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_accept_effect_applied_v0.json"
IMPLEMENTATION_PATH_PREP_TARGET_PATH = OUT_DIR / "accepted_bounded_capability_proposal_implementation_path_prep_target_v0.json"
BOUNDARY_AFTER_DECISION_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_accept_boundary_review_v0.json"
READOUT_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_accept_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_accept_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_accept_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_accept_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_accept_transition_trace.json"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def require_false(obj: Dict[str, Any], key: str, failures: List[str], prefix: str) -> None:
    if obj.get(key) is not False:
        failures.append(f"{prefix}_{key}_not_false:{obj.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        HUMAN_DECISION_REVIEW_RECEIPT_PATH,
        HUMAN_DECISION_REQUEST_PACKET_PATH,
        DECISION_EFFECTS_MAP_PATH,
        BOUNDARY_REVIEW_PATH,
        VALIDATION_RUN_RECEIPT_PATH,
        VALIDATION_SUMMARY_PATH,
        PROPOSAL_PATH,
        HUMAN_DECISION_PACKET_PATH,
        STOP_PACKET_PATH,
    ]

    failures: List[str] = []

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    review_receipt = read_json(HUMAN_DECISION_REVIEW_RECEIPT_PATH)
    request_packet = read_json(HUMAN_DECISION_REQUEST_PACKET_PATH)
    effects_map = read_json(DECISION_EFFECTS_MAP_PATH)
    boundary_review = read_json(BOUNDARY_REVIEW_PATH)
    validation_run = read_json(VALIDATION_RUN_RECEIPT_PATH)
    validation_summary = read_json(VALIDATION_SUMMARY_PATH)
    proposal = read_json(PROPOSAL_PATH)
    human_decision_packet = read_json(HUMAN_DECISION_PACKET_PATH)
    stop_packet = read_json(STOP_PACKET_PATH)

    review_summary = review_receipt.get("machine_readable_bounded_capability_proposal_human_decision_packet_review_summary", {})
    validation_run_summary = validation_run.get("machine_readable_bounded_capability_proposal_validation_path_run_summary", {})

    if review_receipt.get("receipt_id") != HUMAN_DECISION_REVIEW_RECEIPT_ID:
        failures.append(f"review_receipt_id_wrong:{review_receipt.get('receipt_id')}")
    if review_receipt.get("gate") != "PASS":
        failures.append("human_decision_review_gate_not_pass")
    if review_receipt.get("terminal", {}).get("stop_code") != "STOP_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_REQUIRED":
        failures.append(f"review_terminal_stop_wrong:{review_receipt.get('terminal', {}).get('stop_code')}")

    for key in [
        "proposal_validated_by_run",
        "proposal_admissible_for_human_decision",
        "human_decision_required",
        "human_decision_ready",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_summary_{key}_not_true:{review_summary.get(key)}")

    if review_summary.get("selected_decision") is not None:
        failures.append(f"review_already_selected_decision:{review_summary.get('selected_decision')}")

    if review_summary.get("proposal_accepted") is not False:
        failures.append("review_proposal_already_accepted")
    if review_summary.get("human_decision_taken") is not False:
        failures.append("review_human_decision_already_taken")
    if review_summary.get("implementation_authorized") is not False:
        failures.append("review_implementation_already_authorized")

    if request_packet.get("request_status") != "HUMAN_DECISION_REQUIRED":
        failures.append(f"request_status_wrong:{request_packet.get('request_status')}")
    if request_packet.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"request_proposal_id_wrong:{request_packet.get('proposal_id')}")
    if request_packet.get("proposal_validated_by_run") is not True:
        failures.append("request_proposal_not_validated")
    if request_packet.get("proposal_admissible_for_human_decision") is not True:
        failures.append("request_proposal_not_admissible")
    if request_packet.get("does_not_take_decision") is not True:
        failures.append("request_packet_claims_decision_taken")

    available_decisions = request_packet.get("available_decisions") or []
    if SELECTED_DECISION not in available_decisions:
        failures.append(f"selected_decision_not_available:{SELECTED_DECISION}")

    effects = effects_map.get("effects") or {}
    selected_effect = effects.get(SELECTED_DECISION)
    if not isinstance(selected_effect, dict):
        failures.append("selected_decision_effect_missing")
        selected_effect = {}
    else:
        if selected_effect.get("next_lawful_unit_after_decision") != NEXT_UNIT_ID:
            failures.append(f"selected_effect_next_wrong:{selected_effect.get('next_lawful_unit_after_decision')}")
        if selected_effect.get("implementation_authorized_immediately") is not False:
            failures.append("selected_effect_immediate_implementation_unexpected")

    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal.get("proposal_status") != "PROPOSAL_CANDIDATE_ONLY":
        failures.append(f"proposal_status_wrong_before_decision:{proposal.get('proposal_status')}")
    if validation_run.get("gate") != "PASS":
        failures.append("validation_run_gate_not_pass")
    if validation_run_summary.get("proposal_validated_by_run") is not True:
        failures.append("validation_run_proposal_not_validated")
    if validation_run_summary.get("proposal_admissible_for_human_decision") is not True:
        failures.append("validation_run_proposal_not_admissible")
    if validation_summary.get("proposal_validated_by_run") is not True:
        failures.append("validation_summary_proposal_not_validated")
    if validation_summary.get("proposal_admissible_for_human_decision") is not True:
        failures.append("validation_summary_proposal_not_admissible")

    for key in [
        "implementation_authorized",
        "runtime_adoption_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "c8_authorized",
    ]:
        require_false(human_decision_packet, key, failures, "source_human_decision_packet")

    for key in [
        "implementation_authorized",
        "runtime_adoption_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "runtime_patch_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(boundary_review, key, failures, "source_boundary_review")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_ACCEPTED_FOR_BOUNDED_IMPLEMENTATION_PATH_PREP"
        if gate == "PASS"
        else "TYPED_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_ACCEPT_GATE_FAIL"
    )

    decision_record_id = "bounded_capability_proposal_human_decision_accept_" + sig8({
        "proposal_id": proposal.get("proposal_id"),
        "decision_request_id": request_packet.get("decision_request_id"),
        "selected_decision": SELECTED_DECISION,
        "validation_run_id": validation_run_summary.get("validation_run_id"),
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_capability_proposal_human_decision_accept_basis_v0",
        "unit_id": UNIT_ID,
        "decision_record_id": decision_record_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_human_decision_review_receipt_id": HUMAN_DECISION_REVIEW_RECEIPT_ID,
        "source_decision_request_id": request_packet.get("decision_request_id"),
        "source_proposal_id": PROPOSAL_ID,
        "selected_decision": SELECTED_DECISION,
        "basis_claim": "Record explicit human decision ACCEPT_FOR_BOUNDED_IMPLEMENTATION. This accepts the proposal for a later bounded implementation-path preparation unit; it does not implement.",
        "source_file_hashes": source_hashes,
    }

    decision_record = {
        "schema_version": "bounded_capability_proposal_human_decision_record_v0",
        "decision_record_id": decision_record_id,
        "decision_record_status": "HUMAN_DECISION_RECORDED" if gate == "PASS" else "BLOCKED",
        "decision_source": "explicit_human_message",
        "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
        "decision_request_id": request_packet.get("decision_request_id"),
        "proposal_id": proposal.get("proposal_id"),
        "proposal_kind": proposal.get("proposal_kind"),
        "proposed_surface": proposal.get("proposed_surface"),
        "validation_path_id": validation_run_summary.get("validation_path_id"),
        "validation_run_id": validation_run_summary.get("validation_run_id"),
        "proposal_validated_by_run": gate == "PASS",
        "proposal_admissible_for_human_decision": gate == "PASS",
        "proposal_accepted": gate == "PASS",
        "human_decision_taken": gate == "PASS",
        "decision_note": "Accepted for bounded implementation path preparation only.",
        "does_not_implement": True,
    }

    decision_effect_applied = {
        "schema_version": "bounded_capability_proposal_human_decision_accept_effect_applied_v0",
        "decision_record_id": decision_record_id,
        "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
        "effect_status": "APPLIED_TO_NEXT_PATH_TARGET" if gate == "PASS" else "BLOCKED",
        "decision_effect": selected_effect,
        "next_lawful_unit_after_decision": NEXT_UNIT_ID if gate == "PASS" else None,
        "bounded_implementation_path_prep_authorized": gate == "PASS",
        "implementation_authorized_immediately": False,
        "implementation_authorized": False,
        "runtime_adoption_authorized": False,
        "runtime_patch_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "c8_authorized": False,
        "effect_rule": "Acceptance authorizes preparing a bounded implementation path. It does not itself implement or patch runtime.",
    }

    implementation_path_prep_target = {
        "schema_version": "accepted_bounded_capability_proposal_implementation_path_prep_target_v0",
        "target_status": "READY" if gate == "PASS" else "BLOCKED",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "decision_record_id": decision_record_id,
        "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_ref": rel(PROPOSAL_PATH),
        "human_decision_record_ref": rel(DECISION_RECORD_PATH),
        "validation_run_receipt_ref": rel(VALIDATION_RUN_RECEIPT_PATH),
        "source_stop_packet_ref": rel(STOP_PACKET_PATH),
        "path_scope": "Prepare bounded implementation path for the accepted proposal. Do not implement during this decision-recording unit.",
        "required_next_path_guards": [
            "preserve source capability boundary",
            "derive smallest implementation-prep target",
            "do not mutate runtime before implementation path review",
            "emit implementation-path prep receipt",
            "stop before actual implementation unless later explicitly authorized",
        ],
    }

    boundary_after_decision = {
        "schema_version": "bounded_capability_proposal_human_decision_accept_boundary_review_v0",
        "decision_record_id": decision_record_id,
        "review_status": "PASS" if gate == "PASS" else "FAIL",
        "proposal_status_before_decision": proposal.get("proposal_status"),
        "proposal_accepted": gate == "PASS",
        "human_decision_taken": gate == "PASS",
        "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
        "bounded_implementation_path_prep_authorized": gate == "PASS",
        "implementation_authorized": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "runtime_patch_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    rollup = {
        "schema_version": "bounded_capability_proposal_human_decision_accept_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "decision_record_id": decision_record_id,
        "decision_request_id": request_packet.get("decision_request_id"),
        "proposal_id": proposal.get("proposal_id"),
        "proposal_kind": proposal.get("proposal_kind"),
        "proposed_surface": proposal.get("proposed_surface"),
        "proposal_status_before_decision": proposal.get("proposal_status"),
        "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
        "proposal_validated_by_run": gate == "PASS",
        "proposal_admissible_for_human_decision": gate == "PASS",
        "proposal_accepted": gate == "PASS",
        "human_decision_taken": gate == "PASS",
        "bounded_implementation_path_prep_authorized": gate == "PASS",
        "implementation_authorized": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "runtime_patch_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    readout = {
        "schema_version": "bounded_capability_proposal_human_decision_accept_readout_v0",
        "status": status,
        "decision_record_id": decision_record_id,
        "proposal_id": proposal.get("proposal_id"),
        "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
        "interpretation": "Human decision recorded: accept for bounded implementation path preparation. Actual implementation remains unauthorized until a later bounded implementation path unit permits it."
        if gate == "PASS" else "Human accept decision recording failed typed gates.",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
    }

    profile = {
        "schema_version": "bounded_capability_proposal_human_decision_accept_profile_v0",
        "profile_status": status,
        "decision_record_id": decision_record_id,
        "core_rule": "Record human acceptance for bounded implementation-path preparation only; do not implement.",
        "decision_record_ref": rel(DECISION_RECORD_PATH),
        "implementation_path_prep_target_ref": rel(IMPLEMENTATION_PATH_PREP_TARGET_PATH),
        "must_not_infer": [
            "implementation already performed",
            "runtime repaired",
            "runtime adoption authorized",
            "schema mutation authorized",
            "move addition authorized",
            "fixtures may expand by default",
            "C8 authorized",
            "unbounded implementation authority",
        ],
    }

    report = {
        "schema_version": "bounded_capability_proposal_human_decision_accept_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "decision_result": "ACCEPTED_FOR_BOUNDED_IMPLEMENTATION_PATH_PREP" if gate == "PASS" else "ACCEPT_DECISION_GATE_FAIL",
            "decision_record_id": decision_record_id,
            "proposal_id": proposal.get("proposal_id"),
            "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
            "proposal_accepted": gate == "PASS",
            "human_decision_taken": gate == "PASS",
            "bounded_implementation_path_prep_authorized": gate == "PASS",
            "implementation_authorized": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_capability_proposal_human_decision_accept_transition_trace_v0",
        "unit_id": UNIT_ID,
        "decision_record_id": decision_record_id,
        "transitions": [
            {
                "from": "STOP_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_REQUIRED",
                "edge": "human selected ACCEPT_FOR_BOUNDED_IMPLEMENTATION",
                "to": "HUMAN_DECISION_ACCEPTED_FOR_BOUNDED_IMPLEMENTATION_PATH_PREP" if gate == "PASS" else "HUMAN_DECISION_ACCEPT_GATE_FAIL",
            },
            {
                "from": "HUMAN_DECISION_ACCEPTED_FOR_BOUNDED_IMPLEMENTATION_PATH_PREP" if gate == "PASS" else "HUMAN_DECISION_ACCEPT_GATE_FAIL",
                "edge": "emit implementation-path prep target without implementing",
                "to": "IMPLEMENTATION_PATH_PREP_READY" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_ACCEPT_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (DECISION_RECORD_PATH, decision_record),
        (DECISION_EFFECT_APPLIED_PATH, decision_effect_applied),
        (IMPLEMENTATION_PATH_PREP_TARGET_PATH, implementation_path_prep_target),
        (BOUNDARY_AFTER_DECISION_PATH, boundary_after_decision),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "HUMAN_DECISION_REVIEW_RECEIPT_CONSUMED",
        "HUMAN_DECISION_REQUEST_PACKET_CONSUMED",
        "DECISION_EFFECTS_MAP_CONSUMED",
        "VALIDATION_RUN_RECEIPT_CONSUMED",
        "PROPOSAL_VALIDATED_AND_ADMISSIBLE_CONFIRMED",
        "SELECTED_DECISION_ACCEPT_FOR_BOUNDED_IMPLEMENTATION_RECORDED",
        "PROPOSAL_ACCEPTED_FOR_BOUNDED_IMPLEMENTATION_PATH_PREP",
        "IMPLEMENTATION_PATH_PREP_TARGET_EMITTED",
        "NO_IMPLEMENTATION",
        "NO_RUNTIME_REPAIR",
        "NO_SCHEMA_MUTATION",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_RUNTIME_PATCH",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "bounded_capability_proposal_human_decision_accept_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_ACCEPT_FOR_BOUNDED_IMPLEMENTATION_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "decision_record_id": decision_record_id,
        "source_human_decision_review_receipt_id": HUMAN_DECISION_REVIEW_RECEIPT_ID,
        "source_human_decision_review_receipt_ref": rel(HUMAN_DECISION_REVIEW_RECEIPT_PATH),
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "ACCEPT_DECISION_0_HUMAN_DECISION_REVIEW_CONSUMED": gate == "PASS",
            "ACCEPT_DECISION_1_HUMAN_DECISION_REQUIRED_CONFIRMED": review_summary.get("human_decision_required") is True,
            "ACCEPT_DECISION_2_SELECTED_DECISION_AVAILABLE": SELECTED_DECISION in available_decisions,
            "ACCEPT_DECISION_3_PROPOSAL_VALIDATED_BY_RUN": validation_run_summary.get("proposal_validated_by_run") is True,
            "ACCEPT_DECISION_4_PROPOSAL_ADMISSIBLE_FOR_HUMAN_DECISION": validation_run_summary.get("proposal_admissible_for_human_decision") is True,
            "ACCEPT_DECISION_5_DECISION_RECORDED": DECISION_RECORD_PATH.exists() and gate == "PASS",
            "ACCEPT_DECISION_6_PROPOSAL_ACCEPTED_FOR_PATH_PREP": gate == "PASS",
            "ACCEPT_DECISION_7_IMPLEMENTATION_PATH_PREP_TARGET_EMITTED": IMPLEMENTATION_PATH_PREP_TARGET_PATH.exists() and gate == "PASS",
            "ACCEPT_DECISION_8_NO_IMPLEMENTATION": True,
            "ACCEPT_DECISION_9_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "ACCEPT_DECISION_10_NO_SCHEMA_MUTATION": True,
            "ACCEPT_DECISION_11_NO_MOVE_ADDITION": True,
            "ACCEPT_DECISION_12_NO_C8_AUTHORIZATION": True,
            "ACCEPT_DECISION_13_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_capability_proposal_human_decision_accept_summary": {
            "status": status,
            "decision_record_id": decision_record_id,
            "decision_request_id": request_packet.get("decision_request_id"),
            "proposal_id": proposal.get("proposal_id"),
            "proposal_kind": proposal.get("proposal_kind"),
            "proposed_surface": proposal.get("proposed_surface"),
            "proposal_status_before_decision": proposal.get("proposal_status"),
            "validation_path_id": validation_run_summary.get("validation_path_id"),
            "validation_run_id": validation_run_summary.get("validation_run_id"),
            "proposal_validated_by_run": gate == "PASS",
            "proposal_admissible_for_human_decision": gate == "PASS",
            "selected_decision": SELECTED_DECISION if gate == "PASS" else None,
            "proposal_accepted": gate == "PASS",
            "human_decision_taken": gate == "PASS",
            "bounded_implementation_path_prep_authorized": gate == "PASS",
            "implementation_authorized": False,
            "runtime_adoption_authorized": False,
            "schema_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "runtime_patch_authorized": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "decision_record": rel(DECISION_RECORD_PATH),
            "decision_effect_applied": rel(DECISION_EFFECT_APPLIED_PATH),
            "implementation_path_prep_target": rel(IMPLEMENTATION_PATH_PREP_TARGET_PATH),
            "boundary_after_decision": rel(BOUNDARY_AFTER_DECISION_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_capability_proposal_human_decision_accept_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_capability_proposal_human_decision_accept_receipt_id={receipt_id}")
    print(f"bounded_capability_proposal_human_decision_accept_receipt_path={rel(receipt_path)}")
    print(f"bounded_capability_proposal_human_decision_accept_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
