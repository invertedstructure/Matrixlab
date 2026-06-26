#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_PACKET_REVIEW_V0"
TARGET_UNIT_ID = "bounded_capability_proposal.human_decision_packet_review_v0"

VALIDATION_SCOPE_REPAIR_RECEIPT_ID = "bounded_capability_proposal_validation_scope_classifier_repair_receipt_c69a3d7a"
VALIDATION_RUN_RECEIPT_ID = "bounded_capability_proposal_validation_path_run_receipt_375954b6"
PROPOSAL_ID = "capability_proposal_57dda6e9"

VALIDATION_SCOPE_REPAIR_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_validation_scope_binding_classifier_repair_v0_receipts/bounded_capability_proposal_validation_scope_classifier_repair_receipt_c69a3d7a.json"
VALIDATION_RUN_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0_receipts/bounded_capability_proposal_validation_path_run_receipt_375954b6.json"

VALIDATION_SUMMARY_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0/bounded_capability_proposal_validation_admissibility_summary_v0.json"
HUMAN_DECISION_PREP_TARGET_PATH = ROOT / "data/bounded_capability_proposal_validation_path_run_v0/bounded_capability_proposal_human_decision_prep_target_v0.json"

PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
HUMAN_DECISION_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/human_capability_decision_packet_v0.json"
STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"

ADAPTER_CLOSURE_RECEIPT_PATH = ROOT / "data/capability_proposal_adapter_reference_closure_v0_receipts/capability_adapter_reference_closure_receipt_b02a18a5.json"
PROPOSAL_REVIEW_RECEIPT_PATH = ROOT / "data/bounded_capability_proposal_review_v0_receipts/bounded_capability_proposal_review_receipt_804a23ab.json"

OUT_DIR = ROOT / "data/bounded_capability_proposal_human_decision_packet_review_v0"
RECEIPT_DIR = ROOT / "data/bounded_capability_proposal_human_decision_packet_review_v0_receipts"

BASIS_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_packet_review_basis_v0.json"
DECISION_PACKET_SHAPE_REVIEW_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_packet_shape_review_v0.json"
VALIDATION_STATUS_REVIEW_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_validation_status_review_v0.json"
DECISION_OPTIONS_REVIEW_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_options_review_v0.json"
DECISION_EFFECTS_MAP_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_effects_map_v0.json"
BOUNDARY_REVIEW_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_boundary_review_v0.json"
HUMAN_DECISION_REQUEST_PACKET_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_request_packet_v0.json"
READOUT_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_packet_review_readout_v0.json"
ROLLUP_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_packet_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_packet_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_packet_review_report.json"
TRANSITION_TRACE_PATH = OUT_DIR / "bounded_capability_proposal_human_decision_packet_review_transition_trace.json"

REQUIRED_DECISIONS = [
    "ACCEPT_FOR_BOUNDED_IMPLEMENTATION",
    "REJECT",
    "EDIT_AND_RESUBMIT",
    "DEFER",
    "FREEZE_AS_REFERENCE_ONLY",
    "REQUEST_NARROWER_PROPOSAL",
    "REQUEST_ALTERNATE_PROPOSAL",
    "CLOSE_SOURCE_BRANCH_FOR_CURRENT_REGISTRY_ONLY",
]

DECISION_EFFECTS = {
    "ACCEPT_FOR_BOUNDED_IMPLEMENTATION": {
        "decision_meaning": "Accept the validated/admissible proposal for a later bounded implementation-prep path.",
        "next_lawful_unit_after_decision": "PREPARE_ACCEPTED_BOUNDED_CAPABILITY_PROPOSAL_IMPLEMENTATION_PATH_V0",
        "implementation_authorized_immediately": False,
        "notes": "Acceptance does not itself implement. It authorizes a later bounded implementation-prep unit."
    },
    "REJECT": {
        "decision_meaning": "Reject the proposal candidate.",
        "next_lawful_unit_after_decision": "CLOSE_REJECTED_BOUNDED_CAPABILITY_PROPOSAL_BRANCH_V0",
        "implementation_authorized_immediately": False,
        "notes": "No repair or implementation follows unless a new human command opens a new proposal."
    },
    "EDIT_AND_RESUBMIT": {
        "decision_meaning": "Request proposal edit and resubmission.",
        "next_lawful_unit_after_decision": "PREPARE_BOUNDED_CAPABILITY_PROPOSAL_EDIT_PACKET_V0",
        "implementation_authorized_immediately": False,
        "notes": "Edits require a new typed edit packet and re-review/revalidation."
    },
    "DEFER": {
        "decision_meaning": "Defer decision without closing the proposal.",
        "next_lawful_unit_after_decision": "FREEZE_BOUNDED_CAPABILITY_PROPOSAL_AS_DEFERRED_DECISION_V0",
        "implementation_authorized_immediately": False,
        "notes": "Default safe decision; preserves proposal as validated/admissible but undecided."
    },
    "FREEZE_AS_REFERENCE_ONLY": {
        "decision_meaning": "Freeze the proposal as a reference object only.",
        "next_lawful_unit_after_decision": "CLOSE_BOUNDED_CAPABILITY_PROPOSAL_AS_REFERENCE_ONLY_V0",
        "implementation_authorized_immediately": False,
        "notes": "Reference-only closure forbids implementation from this branch."
    },
    "REQUEST_NARROWER_PROPOSAL": {
        "decision_meaning": "Ask for a narrower proposal.",
        "next_lawful_unit_after_decision": "PREPARE_NARROWER_BOUNDED_CAPABILITY_PROPOSAL_REQUEST_V0",
        "implementation_authorized_immediately": False,
        "notes": "Creates a new narrower proposal request; current proposal remains not accepted."
    },
    "REQUEST_ALTERNATE_PROPOSAL": {
        "decision_meaning": "Ask for an alternate proposal.",
        "next_lawful_unit_after_decision": "PREPARE_ALTERNATE_BOUNDED_CAPABILITY_PROPOSAL_REQUEST_V0",
        "implementation_authorized_immediately": False,
        "notes": "Creates alternate proposal request; current proposal remains not accepted."
    },
    "CLOSE_SOURCE_BRANCH_FOR_CURRENT_REGISTRY_ONLY": {
        "decision_meaning": "Close this source branch for the current registry only.",
        "next_lawful_unit_after_decision": "CLOSE_T6_CAPABILITY_SOURCE_BRANCH_FOR_CURRENT_REGISTRY_ONLY_V0",
        "implementation_authorized_immediately": False,
        "notes": "Does not claim global impossibility; closes this branch under current registry state."
    },
}

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
        VALIDATION_SCOPE_REPAIR_RECEIPT_PATH,
        VALIDATION_RUN_RECEIPT_PATH,
        VALIDATION_SUMMARY_PATH,
        HUMAN_DECISION_PREP_TARGET_PATH,
        PROPOSAL_PATH,
        HUMAN_DECISION_PACKET_PATH,
        STOP_PACKET_PATH,
        ADAPTER_CLOSURE_RECEIPT_PATH,
        PROPOSAL_REVIEW_RECEIPT_PATH,
    ]

    failures: List[str] = []

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    validation_scope_repair = read_json(VALIDATION_SCOPE_REPAIR_RECEIPT_PATH)
    validation_run = read_json(VALIDATION_RUN_RECEIPT_PATH)
    validation_summary = read_json(VALIDATION_SUMMARY_PATH)
    human_decision_prep_target = read_json(HUMAN_DECISION_PREP_TARGET_PATH)
    proposal = read_json(PROPOSAL_PATH)
    human_decision_packet = read_json(HUMAN_DECISION_PACKET_PATH)
    stop_packet = read_json(STOP_PACKET_PATH)
    adapter_closure = read_json(ADAPTER_CLOSURE_RECEIPT_PATH)
    proposal_review = read_json(PROPOSAL_REVIEW_RECEIPT_PATH)

    repair_summary = validation_scope_repair.get("machine_readable_bounded_capability_proposal_validation_scope_binding_classifier_repair_summary", {})
    validation_run_summary = validation_run.get("machine_readable_bounded_capability_proposal_validation_path_run_summary", {})
    closure_summary = adapter_closure.get("machine_readable_capability_proposal_adapter_reference_closure_summary", {})
    proposal_review_summary = proposal_review.get("machine_readable_bounded_capability_proposal_review_summary", {})

    if validation_scope_repair.get("receipt_id") != VALIDATION_SCOPE_REPAIR_RECEIPT_ID:
        failures.append(f"validation_scope_repair_receipt_id_wrong:{validation_scope_repair.get('receipt_id')}")
    if validation_scope_repair.get("gate") != "PASS":
        failures.append("validation_scope_repair_gate_not_pass")
    if repair_summary.get("classifier_repaired") is not True:
        failures.append("validation_scope_classifier_not_repaired")
    if repair_summary.get("proposal_validated_by_run") is not True:
        failures.append("repair_summary_proposal_not_validated_by_run")
    if repair_summary.get("proposal_admissible_for_human_decision") is not True:
        failures.append("repair_summary_proposal_not_admissible")
    if repair_summary.get("human_decision_prep_target_ready") is not True:
        failures.append("repair_summary_human_decision_prep_not_ready")
    if validation_scope_repair.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"validation_scope_repair_terminal_next_wrong:{validation_scope_repair.get('terminal', {}).get('next_unit_id')}")

    if validation_run.get("receipt_id") != VALIDATION_RUN_RECEIPT_ID:
        failures.append(f"validation_run_receipt_id_wrong:{validation_run.get('receipt_id')}")
    if validation_run.get("gate") != "PASS":
        failures.append("validation_run_gate_not_pass")
    for key in [
        "schema_validation_pass",
        "source_linkage_pass",
        "lawful_admissibility_pass",
        "boundary_guard_pass",
        "negative_control_pass",
        "human_decision_gate_pass",
        "proposal_validated_by_run",
        "proposal_admissible_for_human_decision",
        "human_decision_prep_target_ready",
    ]:
        if validation_run_summary.get(key) is not True:
            failures.append(f"validation_run_{key}_not_true:{validation_run_summary.get(key)}")

    if validation_summary.get("proposal_validated_by_run") is not True:
        failures.append("validation_summary_proposal_not_validated")
    if validation_summary.get("proposal_admissible_for_human_decision") is not True:
        failures.append("validation_summary_proposal_not_admissible")
    if validation_summary.get("proposal_accepted") is not False:
        failures.append("validation_summary_proposal_accepted_unexpected")
    if validation_summary.get("human_decision_taken") is not False:
        failures.append("validation_summary_human_decision_taken_unexpected")
    if validation_summary.get("implementation_authorized") is not False:
        failures.append("validation_summary_implementation_authorized_unexpected")

    if human_decision_prep_target.get("target_status") != "READY":
        failures.append(f"human_decision_prep_target_status_wrong:{human_decision_prep_target.get('target_status')}")
    if human_decision_prep_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"human_decision_prep_target_next_wrong:{human_decision_prep_target.get('next_unit_id')}")
    if human_decision_prep_target.get("proposal_id") != PROPOSAL_ID:
        failures.append("human_decision_prep_target_proposal_id_wrong")

    if proposal.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"proposal_id_wrong:{proposal.get('proposal_id')}")
    if proposal.get("proposal_status") != "PROPOSAL_CANDIDATE_ONLY":
        failures.append(f"proposal_status_wrong:{proposal.get('proposal_status')}")

    if human_decision_packet.get("proposal_id") != PROPOSAL_ID:
        failures.append(f"human_decision_packet_proposal_id_wrong:{human_decision_packet.get('proposal_id')}")
    if human_decision_packet.get("decision_required") is not True:
        failures.append("human_decision_packet_decision_required_not_true")
    if human_decision_packet.get("default_decision") != "DEFER":
        failures.append(f"human_decision_packet_default_wrong:{human_decision_packet.get('default_decision')}")
    available_decisions = human_decision_packet.get("available_decisions") or []
    missing_decisions = [d for d in REQUIRED_DECISIONS if d not in available_decisions]
    if missing_decisions:
        failures.append(f"human_decision_packet_missing_decisions:{missing_decisions}")

    for key in [
        "implementation_authorized",
        "runtime_adoption_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "c8_authorized",
    ]:
        require_false(human_decision_packet, key, failures, "human_decision_packet")

    for obj_name, obj in [
        ("validation_run_summary", validation_run_summary),
        ("repair_summary", repair_summary),
        ("proposal_review_summary", proposal_review_summary),
        ("closure_summary", closure_summary),
    ]:
        for key in [
            "proposal_accepted",
            "human_decision_taken",
            "implementation_authorized",
            "runtime_adoption_authorized",
            "schema_mutation_authorized",
            "move_addition_authorized",
            "fixture_expansion_authorized",
            "runtime_patch_authorized",
            "hidden_next_command",
            "c8_authorized",
        ]:
            if key in obj and obj.get(key) is not False:
                failures.append(f"{obj_name}_{key}_not_false:{obj.get(key)}")

    proposal_guards = proposal.get("boundary_guards", {})
    for key in [
        "implementation_authorized",
        "runtime_patch_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "c8_authorized",
    ]:
        require_false(proposal_guards, key, failures, "proposal_boundary_guard")

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_PACKET_REVIEW_PASS_DECISION_REQUIRED"
        if gate == "PASS"
        else "TYPED_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_PACKET_REVIEW_GATE_FAIL"
    )

    decision_request_id = "bounded_capability_proposal_human_decision_request_" + sig8({
        "proposal_id": proposal.get("proposal_id"),
        "validation_run_id": validation_run_summary.get("validation_run_id"),
        "available_decisions": available_decisions,
        "default_decision": human_decision_packet.get("default_decision"),
    })

    source_hashes = {rel(p): file_sha256(p) for p in required_files}

    basis = {
        "schema_version": "bounded_capability_proposal_human_decision_packet_review_basis_v0",
        "unit_id": UNIT_ID,
        "decision_request_id": decision_request_id,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_validation_scope_repair_receipt_id": VALIDATION_SCOPE_REPAIR_RECEIPT_ID,
        "source_validation_run_receipt_id": VALIDATION_RUN_RECEIPT_ID,
        "source_proposal_id": PROPOSAL_ID,
        "basis_claim": "Review and prepare the human decision packet for a validated/admissible proposal. Stop at the human decision boundary. Do not choose a decision.",
        "source_file_hashes": source_hashes,
    }

    validation_status_review = {
        "schema_version": "bounded_capability_proposal_human_decision_validation_status_review_v0",
        "decision_request_id": decision_request_id,
        "review_status": "PASS" if gate == "PASS" else "FAIL",
        "validation_path_id": validation_run_summary.get("validation_path_id"),
        "validation_run_id": validation_run_summary.get("validation_run_id"),
        "proposal_validated_by_run": validation_run_summary.get("proposal_validated_by_run") is True,
        "proposal_admissible_for_human_decision": validation_run_summary.get("proposal_admissible_for_human_decision") is True,
        "human_decision_prep_target_ready": validation_run_summary.get("human_decision_prep_target_ready") is True,
        "source_validation_run_receipt_ref": rel(VALIDATION_RUN_RECEIPT_PATH),
        "source_validation_summary_ref": rel(VALIDATION_SUMMARY_PATH),
    }

    decision_packet_shape_review = {
        "schema_version": "bounded_capability_proposal_human_decision_packet_shape_review_v0",
        "decision_request_id": decision_request_id,
        "review_status": "PASS" if gate == "PASS" else "FAIL",
        "packet_ref": rel(HUMAN_DECISION_PACKET_PATH),
        "proposal_id_matches": human_decision_packet.get("proposal_id") == PROPOSAL_ID,
        "decision_required": human_decision_packet.get("decision_required"),
        "default_decision": human_decision_packet.get("default_decision"),
        "available_decisions": available_decisions,
        "missing_decisions": missing_decisions,
        "packet_complete": not missing_decisions and human_decision_packet.get("decision_required") is True,
    }

    decision_options_review = {
        "schema_version": "bounded_capability_proposal_human_decision_options_review_v0",
        "decision_request_id": decision_request_id,
        "review_status": "PASS" if gate == "PASS" else "FAIL",
        "default_decision": human_decision_packet.get("default_decision"),
        "available_decisions": available_decisions,
        "decision_options": [
            {
                "decision": d,
                **DECISION_EFFECTS.get(d, {
                    "decision_meaning": "Unmapped decision",
                    "next_lawful_unit_after_decision": None,
                    "implementation_authorized_immediately": False,
                    "notes": "Decision effect mapping missing."
                })
            }
            for d in available_decisions
        ],
        "all_required_decisions_present": not missing_decisions,
    }

    decision_effects_map = {
        "schema_version": "bounded_capability_proposal_human_decision_effects_map_v0",
        "decision_request_id": decision_request_id,
        "proposal_id": proposal.get("proposal_id"),
        "validation_run_id": validation_run_summary.get("validation_run_id"),
        "effects": {d: DECISION_EFFECTS[d] for d in REQUIRED_DECISIONS},
        "global_rule": "No listed decision directly implements. Even ACCEPT_FOR_BOUNDED_IMPLEMENTATION only authorizes a later bounded implementation-prep path.",
    }

    boundary_review = {
        "schema_version": "bounded_capability_proposal_human_decision_boundary_review_v0",
        "decision_request_id": decision_request_id,
        "review_status": "PASS" if gate == "PASS" else "FAIL",
        "proposal_status": proposal.get("proposal_status"),
        "proposal_validated_by_run": True if gate == "PASS" else False,
        "proposal_admissible_for_human_decision": True if gate == "PASS" else False,
        "human_decision_ready": True if gate == "PASS" else False,
        "human_decision_taken": False,
        "selected_decision": None,
        "proposal_accepted": False,
        "implementation_authorized": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "runtime_patch_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    human_decision_request_packet = {
        "schema_version": "bounded_capability_proposal_human_decision_request_packet_v0",
        "decision_request_id": decision_request_id,
        "request_status": "HUMAN_DECISION_REQUIRED" if gate == "PASS" else "BLOCKED",
        "proposal_id": proposal.get("proposal_id"),
        "proposal_kind": proposal.get("proposal_kind"),
        "proposed_surface": proposal.get("proposed_surface"),
        "proposal_status": proposal.get("proposal_status"),
        "validation_path_id": validation_run_summary.get("validation_path_id"),
        "validation_run_id": validation_run_summary.get("validation_run_id"),
        "proposal_validated_by_run": gate == "PASS",
        "proposal_admissible_for_human_decision": gate == "PASS",
        "default_decision": human_decision_packet.get("default_decision"),
        "available_decisions": available_decisions,
        "decision_prompt": "Human decision required: choose exactly one available decision for this validated/admissible bounded capability proposal.",
        "allowed_reply_shape": {
            "decision": "one of available_decisions",
            "optional_note": "free text",
        },
        "safe_default": "DEFER",
        "decision_effects_map_ref": rel(DECISION_EFFECTS_MAP_PATH),
        "proposal_ref": rel(PROPOSAL_PATH),
        "human_decision_packet_ref": rel(HUMAN_DECISION_PACKET_PATH),
        "does_not_take_decision": True,
    }

    rollup = {
        "schema_version": "bounded_capability_proposal_human_decision_packet_review_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "decision_request_id": decision_request_id,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_kind": proposal.get("proposal_kind"),
        "proposed_surface": proposal.get("proposed_surface"),
        "proposal_status": proposal.get("proposal_status"),
        "proposal_validated_by_run": gate == "PASS",
        "proposal_admissible_for_human_decision": gate == "PASS",
        "human_decision_ready": gate == "PASS",
        "human_decision_required": gate == "PASS",
        "default_decision": human_decision_packet.get("default_decision"),
        "available_decision_count": len(available_decisions),
        "proposal_accepted": False,
        "human_decision_taken": False,
        "selected_decision": None,
        "implementation_authorized": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "runtime_patch_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    readout = {
        "schema_version": "bounded_capability_proposal_human_decision_packet_review_readout_v0",
        "status": status,
        "decision_request_id": decision_request_id,
        "proposal_id": proposal.get("proposal_id"),
        "proposal_status": proposal.get("proposal_status"),
        "human_decision_required": gate == "PASS",
        "default_decision": human_decision_packet.get("default_decision"),
        "available_decisions": available_decisions,
        "interpretation": "Human decision packet is ready. Stop here for human choice; no decision was taken by this unit."
        if gate == "PASS" else "Human decision packet review failed typed gates.",
    }

    profile = {
        "schema_version": "bounded_capability_proposal_human_decision_packet_review_profile_v0",
        "profile_status": status,
        "decision_request_id": decision_request_id,
        "core_rule": "Prepare and review human decision packet only. The machine must not choose the decision.",
        "human_decision_request_packet_ref": rel(HUMAN_DECISION_REQUEST_PACKET_PATH),
        "decision_effects_map_ref": rel(DECISION_EFFECTS_MAP_PATH),
        "must_not_infer": [
            "proposal accepted",
            "human decision taken",
            "selected decision exists",
            "capability implementation authorized",
            "runtime repaired",
            "runtime adoption authorized",
            "schema mutation authorized",
            "move addition authorized",
            "fixtures may expand by default",
            "C8 authorized",
        ],
    }

    report = {
        "schema_version": "bounded_capability_proposal_human_decision_packet_review_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "review_result": "HUMAN_DECISION_REQUIRED" if gate == "PASS" else "HUMAN_DECISION_PACKET_REVIEW_GATE_FAIL",
            "decision_request_id": decision_request_id,
            "proposal_id": proposal.get("proposal_id"),
            "proposal_validated_by_run": gate == "PASS",
            "proposal_admissible_for_human_decision": gate == "PASS",
            "available_decisions": available_decisions,
            "default_decision": human_decision_packet.get("default_decision"),
            "proposal_accepted": False,
            "human_decision_taken": False,
            "implementation_authorized": False,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "bounded_capability_proposal_human_decision_packet_review_transition_trace_v0",
        "unit_id": UNIT_ID,
        "decision_request_id": decision_request_id,
        "transitions": [
            {
                "from": "VALIDATED_ADMISSIBLE_PROPOSAL_HUMAN_DECISION_PREP_READY",
                "edge": "review validation state and human decision packet",
                "to": "HUMAN_DECISION_PACKET_READY" if gate == "PASS" else "HUMAN_DECISION_PACKET_REVIEW_GATE_FAIL",
            },
            {
                "from": "HUMAN_DECISION_PACKET_READY" if gate == "PASS" else "HUMAN_DECISION_PACKET_REVIEW_GATE_FAIL",
                "edge": "emit decision request packet and stop at human boundary",
                "to": "STOP_HUMAN_DECISION_REQUIRED" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "STOP",
            "next_unit_id": None,
            "stop_code": "STOP_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_REQUIRED" if gate == "PASS" else "STOP_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_PACKET_REVIEW_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (DECISION_PACKET_SHAPE_REVIEW_PATH, decision_packet_shape_review),
        (VALIDATION_STATUS_REVIEW_PATH, validation_status_review),
        (DECISION_OPTIONS_REVIEW_PATH, decision_options_review),
        (DECISION_EFFECTS_MAP_PATH, decision_effects_map),
        (BOUNDARY_REVIEW_PATH, boundary_review),
        (HUMAN_DECISION_REQUEST_PACKET_PATH, human_decision_request_packet),
        (READOUT_PATH, readout),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "VALIDATION_SCOPE_REPAIR_RECEIPT_CONSUMED",
        "VALIDATION_RUN_RECEIPT_CONSUMED",
        "VALIDATION_SUMMARY_CONSUMED",
        "HUMAN_DECISION_PREP_TARGET_CONSUMED",
        "PROPOSAL_VALIDATED_AND_ADMISSIBLE_FOR_HUMAN_DECISION",
        "HUMAN_DECISION_PACKET_REVIEWED_COMPLETE",
        "DECISION_OPTIONS_REVIEWED",
        "DECISION_EFFECTS_MAP_EMITTED",
        "HUMAN_DECISION_REQUEST_PACKET_EMITTED",
        "STOP_HUMAN_DECISION_REQUIRED",
        "NO_DECISION_SELECTED",
        "NO_PROPOSAL_ACCEPTANCE",
        "NO_HUMAN_DECISION_TAKEN",
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
        "schema_version": "bounded_capability_proposal_human_decision_packet_review_receipt_v0",
        "receipt_type": "TYPED_BOUNDED_CAPABILITY_PROPOSAL_HUMAN_DECISION_PACKET_REVIEW_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "decision_request_id": decision_request_id,
        "source_validation_scope_repair_receipt_id": VALIDATION_SCOPE_REPAIR_RECEIPT_ID,
        "source_validation_scope_repair_receipt_ref": rel(VALIDATION_SCOPE_REPAIR_RECEIPT_PATH),
        "source_validation_run_receipt_id": VALIDATION_RUN_RECEIPT_ID,
        "source_validation_run_receipt_ref": rel(VALIDATION_RUN_RECEIPT_PATH),
        "source_proposal_id": PROPOSAL_ID,
        "source_proposal_ref": rel(PROPOSAL_PATH),
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "acceptance_gate_results": {
            "HUMAN_DECISION_REVIEW_0_VALIDATION_SCOPE_REPAIR_CONSUMED": gate == "PASS",
            "HUMAN_DECISION_REVIEW_1_VALIDATION_RUN_CONSUMED": gate == "PASS",
            "HUMAN_DECISION_REVIEW_2_PROPOSAL_VALIDATED_BY_RUN": validation_run_summary.get("proposal_validated_by_run") is True,
            "HUMAN_DECISION_REVIEW_3_PROPOSAL_ADMISSIBLE_FOR_HUMAN_DECISION": validation_run_summary.get("proposal_admissible_for_human_decision") is True,
            "HUMAN_DECISION_REVIEW_4_HUMAN_DECISION_PREP_TARGET_READY": validation_run_summary.get("human_decision_prep_target_ready") is True,
            "HUMAN_DECISION_REVIEW_5_DECISION_PACKET_COMPLETE": not missing_decisions and human_decision_packet.get("decision_required") is True,
            "HUMAN_DECISION_REVIEW_6_DEFAULT_DECISION_DEFER": human_decision_packet.get("default_decision") == "DEFER",
            "HUMAN_DECISION_REVIEW_7_DECISION_REQUEST_PACKET_EMITTED": HUMAN_DECISION_REQUEST_PACKET_PATH.exists() and gate == "PASS",
            "HUMAN_DECISION_REVIEW_8_NO_DECISION_SELECTED": True,
            "HUMAN_DECISION_REVIEW_9_NO_PROPOSAL_ACCEPTANCE": True,
            "HUMAN_DECISION_REVIEW_10_NO_HUMAN_DECISION_TAKEN": True,
            "HUMAN_DECISION_REVIEW_11_NO_IMPLEMENTATION": True,
            "HUMAN_DECISION_REVIEW_12_NO_RUNTIME_ADOPTION_AUTHORITY": True,
            "HUMAN_DECISION_REVIEW_13_NO_SCHEMA_MUTATION": True,
            "HUMAN_DECISION_REVIEW_14_NO_MOVE_ADDITION": True,
            "HUMAN_DECISION_REVIEW_15_NO_C8_AUTHORIZATION": True,
            "HUMAN_DECISION_REVIEW_16_NO_HIDDEN_NEXT_COMMAND": True,
        },
        "machine_readable_bounded_capability_proposal_human_decision_packet_review_summary": {
            "status": status,
            "decision_request_id": decision_request_id,
            "proposal_id": proposal.get("proposal_id"),
            "proposal_kind": proposal.get("proposal_kind"),
            "proposed_surface": proposal.get("proposed_surface"),
            "proposal_status": proposal.get("proposal_status"),
            "validation_path_id": validation_run_summary.get("validation_path_id"),
            "validation_run_id": validation_run_summary.get("validation_run_id"),
            "proposal_validated_by_run": gate == "PASS",
            "proposal_admissible_for_human_decision": gate == "PASS",
            "human_decision_required": gate == "PASS",
            "human_decision_ready": gate == "PASS",
            "default_decision": human_decision_packet.get("default_decision"),
            "available_decisions": available_decisions,
            "selected_decision": None,
            "next_unit_id": None,
            "proposal_accepted": False,
            "human_decision_taken": False,
            "implementation_authorized": False,
            "runtime_adoption_authorized": False,
            "schema_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "runtime_patch_authorized": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "decision_packet_shape_review": rel(DECISION_PACKET_SHAPE_REVIEW_PATH),
            "validation_status_review": rel(VALIDATION_STATUS_REVIEW_PATH),
            "decision_options_review": rel(DECISION_OPTIONS_REVIEW_PATH),
            "decision_effects_map": rel(DECISION_EFFECTS_MAP_PATH),
            "boundary_review": rel(BOUNDARY_REVIEW_PATH),
            "human_decision_request_packet": rel(HUMAN_DECISION_REQUEST_PACKET_PATH),
            "readout": rel(READOUT_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "bounded_capability_proposal_human_decision_packet_review_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"bounded_capability_proposal_human_decision_packet_review_receipt_id={receipt_id}")
    print(f"bounded_capability_proposal_human_decision_packet_review_receipt_path={rel(receipt_path)}")
    print(f"bounded_capability_proposal_human_decision_request_id={decision_request_id if gate == 'PASS' else 'NONE'}")
    print("bounded_capability_proposal_human_decision_packet_review_next_unit=NONE")
    print("bounded_capability_proposal_human_decision_packet_review_stop_code=" + transition_trace["terminal"]["stop_code"])

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
