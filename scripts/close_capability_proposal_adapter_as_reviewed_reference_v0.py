#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_CAPABILITY_PROPOSAL_ADAPTER_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "capability_proposal_adapter.reference_closure_v0"
FOLLOWUP_PROPOSAL_REVIEW_UNIT_ID = "REVIEW_BOUNDED_CAPABILITY_PROPOSAL_CANDIDATE_V0"

PACKAGING_REPAIR_RECEIPT_ID = "capability_adapter_packaging_repair_receipt_603b2ec4"
PARITY_REPAIR_RECEIPT_ID = "capability_adapter_parity_repair_receipt_947614d6"
REVIEW_RECEIPT_ID = "capability_adapter_review_receipt_9c306ed5"
ADAPTER_RECEIPT_ID = "capability_adapter_receipt_8c7f0905"

PACKAGING_REPAIR_RECEIPT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_parity_repair_packaging_v0_receipts/capability_adapter_packaging_repair_receipt_603b2ec4.json"
PARITY_REPAIR_RECEIPT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_negative_control_parity_repair_v0_receipts/capability_adapter_parity_repair_receipt_947614d6.json"
REVIEW_RECEIPT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_review_v0_receipts/capability_adapter_review_receipt_9c306ed5.json"
ADAPTER_RECEIPT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0_receipts/capability_adapter_receipt_8c7f0905.json"

PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
HUMAN_DECISION_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/human_capability_decision_packet_v0.json"
STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"
ADAPTER_READOUT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_proposal_adapter_readout_v0.json"
ADAPTER_ROLLUP_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_proposal_adapter_rollup_v0.json"
ADAPTER_PROFILE_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_proposal_adapter_profile_v0.json"
ADAPTER_REPORT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_proposal_adapter_report.json"
ADAPTER_TRACE_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_proposal_adapter_trace_v0.jsonl"
ADAPTER_TRANSITION_TRACE_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_proposal_adapter_transition_trace.json"

ADAPTER_SCRIPT_PATH = ROOT / "scripts/build_capability_stop_packet_to_bounded_proposal_v0.py"
REVIEW_SCRIPT_PATH = ROOT / "scripts/review_capability_stop_packet_to_bounded_proposal_v0.py"
PARITY_REPAIR_SCRIPT_PATH = ROOT / "scripts/repair_capability_proposal_adapter_negative_control_parity_v0.py"
PACKAGING_REPAIR_SCRIPT_PATH = ROOT / "scripts/repair_capability_proposal_adapter_parity_repair_packaging_v0.py"

OUT_DIR = ROOT / "data/capability_proposal_adapter_reference_closure_v0"
RECEIPT_DIR = ROOT / "data/capability_proposal_adapter_reference_closure_v0_receipts"

BASIS_PATH = OUT_DIR / "capability_proposal_adapter_reference_closure_basis_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "capability_proposal_adapter_reviewed_reference_index_v0.json"
FREEZE_MANIFEST_PATH = OUT_DIR / "capability_proposal_adapter_reference_freeze_manifest_v0.json"
PROPOSAL_PENDING_REVIEW_POINTER_PATH = OUT_DIR / "bounded_capability_proposal_pending_review_pointer_v0.json"
CLOSURE_READOUT_PATH = OUT_DIR / "capability_proposal_adapter_reference_closure_readout_v0.json"
CLOSURE_ROLLUP_PATH = OUT_DIR / "capability_proposal_adapter_reference_closure_rollup_v0.json"
CLOSURE_PROFILE_PATH = OUT_DIR / "capability_proposal_adapter_reference_closure_profile_v0.json"
CLOSURE_REPORT_PATH = OUT_DIR / "capability_proposal_adapter_reference_closure_report.json"
CLOSURE_TRANSITION_TRACE_PATH = OUT_DIR / "capability_proposal_adapter_reference_closure_transition_trace.json"

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

def require_false(obj: Dict[str, Any], key: str, failures: List[str]) -> None:
    if obj.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{obj.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required_files = [
        PACKAGING_REPAIR_RECEIPT_PATH,
        PARITY_REPAIR_RECEIPT_PATH,
        REVIEW_RECEIPT_PATH,
        ADAPTER_RECEIPT_PATH,
        PROPOSAL_PATH,
        HUMAN_DECISION_PACKET_PATH,
        STOP_PACKET_PATH,
        ADAPTER_READOUT_PATH,
        ADAPTER_ROLLUP_PATH,
        ADAPTER_PROFILE_PATH,
        ADAPTER_REPORT_PATH,
        ADAPTER_TRACE_PATH,
        ADAPTER_TRANSITION_TRACE_PATH,
        ADAPTER_SCRIPT_PATH,
        REVIEW_SCRIPT_PATH,
        PARITY_REPAIR_SCRIPT_PATH,
        PACKAGING_REPAIR_SCRIPT_PATH,
    ]

    failures: List[str] = []

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    packaging = read_json(PACKAGING_REPAIR_RECEIPT_PATH)
    parity = read_json(PARITY_REPAIR_RECEIPT_PATH)
    review = read_json(REVIEW_RECEIPT_PATH)
    adapter = read_json(ADAPTER_RECEIPT_PATH)
    proposal = read_json(PROPOSAL_PATH)
    human_decision = read_json(HUMAN_DECISION_PACKET_PATH)
    stop_packet = read_json(STOP_PACKET_PATH)
    adapter_readout = read_json(ADAPTER_READOUT_PATH)
    adapter_rollup = read_json(ADAPTER_ROLLUP_PATH)
    adapter_profile = read_json(ADAPTER_PROFILE_PATH)
    adapter_report = read_json(ADAPTER_REPORT_PATH)
    adapter_transition_trace = read_json(ADAPTER_TRANSITION_TRACE_PATH)
    adapter_trace_text = ADAPTER_TRACE_PATH.read_text()

    packaging_summary = packaging.get("machine_readable_capability_proposal_adapter_parity_repair_packaging_summary", {})
    parity_summary = parity.get("machine_readable_capability_proposal_adapter_negative_control_parity_repair_summary", {})
    review_summary = review.get("machine_readable_capability_proposal_adapter_review_summary", {})
    adapter_summary = adapter.get("machine_readable_capability_proposal_adapter_summary", {})
    adapter_neg = adapter.get("negative_controls", {})

    # Source receipt identity and terminal checks.
    if packaging.get("receipt_id") != PACKAGING_REPAIR_RECEIPT_ID:
        failures.append(f"packaging_receipt_id_wrong:{packaging.get('receipt_id')}")
    if parity.get("receipt_id") != PARITY_REPAIR_RECEIPT_ID:
        failures.append(f"parity_receipt_id_wrong:{parity.get('receipt_id')}")
    if review.get("receipt_id") != REVIEW_RECEIPT_ID:
        failures.append(f"review_receipt_id_wrong:{review.get('receipt_id')}")
    if adapter.get("receipt_id") != ADAPTER_RECEIPT_ID:
        failures.append(f"adapter_receipt_id_wrong:{adapter.get('receipt_id')}")

    for name, obj in [
        ("packaging", packaging),
        ("parity", parity),
        ("review", review),
        ("adapter", adapter),
    ]:
        if obj.get("gate") != "PASS":
            failures.append(f"{name}_gate_not_pass")

    if packaging_summary.get("reference_freeze_ready") is not True:
        failures.append("packaging_reference_freeze_ready_false")
    if packaging.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append(f"packaging_terminal_next_wrong:{packaging.get('terminal', {}).get('next_unit_id')}")
    if parity_summary.get("reference_freeze_ready") is not True:
        failures.append("parity_reference_freeze_ready_false")
    if review_summary.get("proposal_bridge_valid") is not True:
        failures.append("review_proposal_bridge_valid_false")

    # Adapter branch facts.
    if adapter_summary.get("proposal_emitted") is not True:
        failures.append("adapter_proposal_not_emitted")
    if adapter_summary.get("proposal_status") != "PROPOSAL_CANDIDATE_ONLY":
        failures.append("adapter_proposal_status_wrong")
    if adapter_summary.get("validation_status") != "NOT_VALIDATED_BY_ADAPTER":
        failures.append("adapter_validation_status_wrong")
    if adapter_summary.get("proposal_kind") != "BOUNDED_TRIGGER_SURFACE_CAPABILITY_PROPOSAL":
        failures.append("adapter_proposal_kind_wrong")
    if adapter_summary.get("proposed_surface") != "bounded_structured_t6_trigger_surface_capability_v0":
        failures.append("adapter_proposed_surface_wrong")
    if adapter_summary.get("missing_objects") != ["loop_trigger_surface_missing", "structured_tie_evidence_missing"]:
        failures.append("adapter_missing_objects_wrong")
    if adapter_summary.get("required_capability") != "bounded_structured_t6_trigger_surface_capability":
        failures.append("adapter_required_capability_wrong")
    if adapter_neg.get("runtime_adoption_authority_count") != 0:
        failures.append("adapter_runtime_adoption_authority_count_not_zero")

    # Proposal is intentionally not accepted/reviewed here.
    if proposal.get("proposal_id") != adapter_summary.get("proposal_id"):
        failures.append("proposal_id_mismatch")
    if proposal.get("proposal_status") != "PROPOSAL_CANDIDATE_ONLY":
        failures.append("proposal_artifact_status_wrong")
    if human_decision.get("decision_required") is not True:
        failures.append("human_decision_not_required")
    if human_decision.get("default_decision") != "DEFER":
        failures.append("human_default_not_defer")

    for key in [
        "proposal_accepted",
        "implementation_authorized",
        "runtime_adoption_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "runtime_patch_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(adapter_summary, key, failures)
        if key in packaging_summary:
            require_false(packaging_summary, key, failures)
        if key in parity_summary:
            require_false(parity_summary, key, failures)
        if key in review_summary:
            require_false(review_summary, key, failures)

    required_trace_terms = [
        "LOAD_SOURCE_STOP_PACKET",
        "VALIDATE_STOP_PACKET_SHAPE",
        "VERIFY_CAPABILITY_BOUNDARY_STOP",
        "EXTRACT_MISSING_OBJECTS",
        "EXTRACT_REQUIRED_CAPABILITY",
        "FORM_BOUNDED_PROPOSAL_CANDIDATE",
        "EMIT_HUMAN_DECISION_PACKET",
        "EMIT_ADAPTER_RECEIPT",
    ]
    missing_trace_terms = [t for t in required_trace_terms if t not in adapter_trace_text]
    if missing_trace_terms:
        failures.extend([f"adapter_trace_term_missing:{t}" for t in missing_trace_terms])

    gate = "PASS" if not failures else "FAIL"
    status = (
        "TYPED_CAPABILITY_PROPOSAL_ADAPTER_REFERENCE_BRANCH_CLOSED"
        if gate == "PASS"
        else "TYPED_CAPABILITY_PROPOSAL_ADAPTER_REFERENCE_CLOSURE_GATE_FAIL"
    )

    source_file_hashes = {rel(p): file_sha256(p) for p in required_files}

    reference_id = "capability_proposal_adapter_reviewed_reference_" + sig8({
        "adapter_receipt_id": adapter.get("receipt_id"),
        "review_receipt_id": review.get("receipt_id"),
        "parity_repair_receipt_id": parity.get("receipt_id"),
        "packaging_repair_receipt_id": packaging.get("receipt_id"),
        "proposal_id": proposal.get("proposal_id"),
        "adapter_script": file_sha256(ADAPTER_SCRIPT_PATH),
    })

    basis = {
        "schema_version": "capability_proposal_adapter_reference_closure_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_FAIL",
        "source_packaging_repair_receipt_id": PACKAGING_REPAIR_RECEIPT_ID,
        "source_parity_repair_receipt_id": PARITY_REPAIR_RECEIPT_ID,
        "source_review_receipt_id": REVIEW_RECEIPT_ID,
        "source_adapter_receipt_id": ADAPTER_RECEIPT_ID,
        "basis_claim": "Close the capability proposal adapter mechanism as a reviewed reference after adapter review, local parity repair, and packaging repair. Do not review or accept the proposal content in this unit.",
        "source_file_hashes": source_file_hashes,
    }

    reference_index = {
        "schema_version": "capability_proposal_adapter_reviewed_reference_index_v0",
        "reference_id": reference_id if gate == "PASS" else None,
        "reference_status": "REVIEWED_REFERENCE_CLOSED" if gate == "PASS" else "NOT_CLOSED",
        "reference_kind": "CAPABILITY_STOP_PACKET_TO_BOUNDED_PROPOSAL_ADAPTER",
        "adapter_unit_id": "BUILD_CAPABILITY_STOP_PACKET_TO_BOUNDED_PROPOSAL_V0",
        "review_unit_id": "REVIEW_CAPABILITY_STOP_PACKET_TO_BOUNDED_PROPOSAL_V0",
        "parity_repair_unit_id": "REPAIR_CAPABILITY_PROPOSAL_ADAPTER_NEGATIVE_CONTROL_PARITY_V0",
        "packaging_repair_unit_id": "REPAIR_CAPABILITY_PROPOSAL_ADAPTER_PARITY_REPAIR_PACKAGING_V0",
        "closure_unit_id": UNIT_ID,
        "source_stop_packet_schema_version": stop_packet.get("schema_version"),
        "proposal_schema_version": proposal.get("schema_version"),
        "human_decision_packet_schema_version": human_decision.get("schema_version"),
        "adapter_receipt_ref": rel(ADAPTER_RECEIPT_PATH),
        "review_receipt_ref": rel(REVIEW_RECEIPT_PATH),
        "parity_repair_receipt_ref": rel(PARITY_REPAIR_RECEIPT_PATH),
        "packaging_repair_receipt_ref": rel(PACKAGING_REPAIR_RECEIPT_PATH),
        "adapter_script_ref": rel(ADAPTER_SCRIPT_PATH),
        "review_script_ref": rel(REVIEW_SCRIPT_PATH),
        "parity_repair_script_ref": rel(PARITY_REPAIR_SCRIPT_PATH),
        "packaging_repair_script_ref": rel(PACKAGING_REPAIR_SCRIPT_PATH),
        "use_as_reference_for": [
            "capability-boundary typed stops",
            "structured capability stop packets",
            "bounded capability proposal candidate emission",
            "human decision packet emission after proposal candidate",
        ],
        "does_not_authorize": [
            "proposal acceptance",
            "proposal validation",
            "capability implementation",
            "runtime repair",
            "runtime patch",
            "schema archive mutation",
            "move addition",
            "fixture expansion by default",
            "runtime adoption",
            "C8 authorization",
        ],
    }

    freeze_manifest = {
        "schema_version": "capability_proposal_adapter_reference_freeze_manifest_v0",
        "reference_id": reference_id if gate == "PASS" else None,
        "freeze_status": "FROZEN_AS_REVIEWED_REFERENCE" if gate == "PASS" else "FREEZE_BLOCKED",
        "closed_branch": "CAPABILITY_PROPOSAL_ADAPTER_REFERENCE_BRANCH",
        "included_artifacts": {
            "adapter_receipt": rel(ADAPTER_RECEIPT_PATH),
            "adapter_readout": rel(ADAPTER_READOUT_PATH),
            "adapter_rollup": rel(ADAPTER_ROLLUP_PATH),
            "adapter_profile": rel(ADAPTER_PROFILE_PATH),
            "adapter_report": rel(ADAPTER_REPORT_PATH),
            "adapter_trace": rel(ADAPTER_TRACE_PATH),
            "adapter_transition_trace": rel(ADAPTER_TRANSITION_TRACE_PATH),
            "review_receipt": rel(REVIEW_RECEIPT_PATH),
            "parity_repair_receipt": rel(PARITY_REPAIR_RECEIPT_PATH),
            "packaging_repair_receipt": rel(PACKAGING_REPAIR_RECEIPT_PATH),
            "adapter_script": rel(ADAPTER_SCRIPT_PATH),
            "review_script": rel(REVIEW_SCRIPT_PATH),
            "parity_repair_script": rel(PARITY_REPAIR_SCRIPT_PATH),
            "packaging_repair_script": rel(PACKAGING_REPAIR_SCRIPT_PATH),
        },
        "proposal_artifacts_linked_but_not_accepted": {
            "bounded_capability_proposal": rel(PROPOSAL_PATH),
            "human_capability_decision_packet": rel(HUMAN_DECISION_PACKET_PATH),
        },
        "proposal_review_pending": True,
        "followup_proposal_review_unit_id": FOLLOWUP_PROPOSAL_REVIEW_UNIT_ID,
    }

    proposal_pending_review_pointer = {
        "schema_version": "bounded_capability_proposal_pending_review_pointer_v0",
        "proposal_id": proposal.get("proposal_id"),
        "proposal_kind": proposal.get("proposal_kind"),
        "proposal_status": proposal.get("proposal_status"),
        "proposed_surface": proposal.get("proposed_surface"),
        "source_stop_packet_id": proposal.get("source_stop_packet_id"),
        "pending_review": True,
        "pending_review_unit_id": FOLLOWUP_PROPOSAL_REVIEW_UNIT_ID,
        "adapter_reference_id": reference_id if gate == "PASS" else None,
        "human_decision_required": human_decision.get("decision_required"),
        "default_human_decision": human_decision.get("default_decision"),
        "proposal_accepted": False,
        "implementation_authorized": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "runtime_patch_authorized": False,
        "c8_authorized": False,
    }

    rollup = {
        "schema_version": "capability_proposal_adapter_reference_closure_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "reference_id": reference_id if gate == "PASS" else None,
        "adapter_reference_branch_closed": gate == "PASS",
        "adapter_reference_freeze_ready": gate == "PASS",
        "adapter_reviewed": gate == "PASS",
        "local_parity_repaired": gate == "PASS",
        "packaging_repaired": gate == "PASS",
        "proposal_review_pending": True,
        "proposal_accepted": False,
        "proposal_validated": False,
        "implementation_authorized": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "runtime_patch_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
        "followup_proposal_review_unit_id": FOLLOWUP_PROPOSAL_REVIEW_UNIT_ID,
    }

    readout = {
        "schema_version": "capability_proposal_adapter_reference_closure_readout_v0",
        "status": status,
        "reference_id": reference_id if gate == "PASS" else None,
        "closed_object": "Capability Proposal Adapter v0",
        "closure_meaning": "Adapter mechanism is closed as a reviewed reference for converting capability stop packets into bounded proposal candidates.",
        "proposal_id": proposal.get("proposal_id"),
        "proposal_status": proposal.get("proposal_status"),
        "proposal_review_pending": True,
        "followup_proposal_review_unit_id": FOLLOWUP_PROPOSAL_REVIEW_UNIT_ID,
        "interpretation": "The adapter branch is closed. The bounded proposal remains a candidate only and must be reviewed separately before any human acceptance or implementation.",
    }

    profile = {
        "schema_version": "capability_proposal_adapter_reference_closure_profile_v0",
        "profile_status": status,
        "reference_id": reference_id if gate == "PASS" else None,
        "core_rule": "Freeze the adapter mechanism as reviewed reference only; leave proposal content pending later review.",
        "reference_index_ref": rel(REFERENCE_INDEX_PATH),
        "freeze_manifest_ref": rel(FREEZE_MANIFEST_PATH),
        "proposal_pending_review_pointer_ref": rel(PROPOSAL_PENDING_REVIEW_POINTER_PATH),
        "must_not_infer": [
            "proposal accepted",
            "proposal validated",
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
        "schema_version": "capability_proposal_adapter_reference_closure_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "adapter_result": "CLOSED_AS_REVIEWED_REFERENCE" if gate == "PASS" else "CLOSURE_GATE_FAIL",
            "proposal_result": "PENDING_REVIEW_CANDIDATE_ONLY",
            "proposal_id": proposal.get("proposal_id"),
            "followup_proposal_review_unit_id": FOLLOWUP_PROPOSAL_REVIEW_UNIT_ID,
            "proposal_accepted": False,
            "proposal_validated": False,
            "implementation_authorized": False,
        },
        "failures": failures,
    }

    transition_trace = {
        "schema_version": "capability_proposal_adapter_reference_closure_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "CAPABILITY_PROPOSAL_ADAPTER_PARITY_REPAIR_PACKAGING_READY_REFERENCE_FREEZE_NEXT",
                "edge": "consume packaging repair receipt and reviewed adapter basis",
                "to": "ADAPTER_REFERENCE_CLOSURE_READY" if gate == "PASS" else "REFERENCE_CLOSURE_GATE_FAIL",
            },
            {
                "from": "ADAPTER_REFERENCE_CLOSURE_READY" if gate == "PASS" else "REFERENCE_CLOSURE_GATE_FAIL",
                "edge": "freeze adapter mechanism only; leave proposal pending review",
                "to": "ADAPTER_REFERENCE_BRANCH_CLOSED" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_CAPABILITY_PROPOSAL_ADAPTER_REFERENCE_BRANCH_CLOSED" if gate == "PASS" else "STOP_CAPABILITY_PROPOSAL_ADAPTER_REFERENCE_CLOSURE_GATE_FAIL",
            "next_command_goal": FOLLOWUP_PROPOSAL_REVIEW_UNIT_ID if gate == "PASS" else None,
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (REFERENCE_INDEX_PATH, reference_index),
        (FREEZE_MANIFEST_PATH, freeze_manifest),
        (PROPOSAL_PENDING_REVIEW_POINTER_PATH, proposal_pending_review_pointer),
        (CLOSURE_READOUT_PATH, readout),
        (CLOSURE_ROLLUP_PATH, rollup),
        (CLOSURE_PROFILE_PATH, profile),
        (CLOSURE_REPORT_PATH, report),
        (CLOSURE_TRANSITION_TRACE_PATH, transition_trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "PACKAGING_REPAIR_RECEIPT_CONSUMED",
        "PARITY_REPAIR_RECEIPT_CONSUMED",
        "ADAPTER_REVIEW_RECEIPT_CONSUMED",
        "ADAPTER_RECEIPT_CONSUMED",
        "REFERENCE_FREEZE_READY_CONFIRMED",
        "ADAPTER_BRANCH_CLOSED_AS_REVIEWED_REFERENCE",
        "PROPOSAL_LEFT_PENDING_REVIEW",
        "NO_PROPOSAL_REVIEW_PERFORMED",
        "NO_PROPOSAL_VALIDATION",
        "NO_PROPOSAL_ACCEPTANCE",
        "NO_IMPLEMENTATION",
        "NO_RUNTIME_REPAIR",
        "NO_SCHEMA_MUTATION",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_RUNTIME_PATCH",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_C8_AUTHORIZATION",
        "FOLLOWUP_PROPOSAL_REVIEW_DECLARED",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "capability_proposal_adapter_reference_closure_receipt_v0",
        "receipt_type": "TYPED_CAPABILITY_PROPOSAL_ADAPTER_REFERENCE_CLOSURE_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "source_receipts": {
            "adapter_receipt_id": ADAPTER_RECEIPT_ID,
            "adapter_receipt_ref": rel(ADAPTER_RECEIPT_PATH),
            "review_receipt_id": REVIEW_RECEIPT_ID,
            "review_receipt_ref": rel(REVIEW_RECEIPT_PATH),
            "parity_repair_receipt_id": PARITY_REPAIR_RECEIPT_ID,
            "parity_repair_receipt_ref": rel(PARITY_REPAIR_RECEIPT_PATH),
            "packaging_repair_receipt_id": PACKAGING_REPAIR_RECEIPT_ID,
            "packaging_repair_receipt_ref": rel(PACKAGING_REPAIR_RECEIPT_PATH),
        },
        "acceptance_gate_results": {
            "CLOSURE_0_PACKAGING_REPAIR_RECEIPT_CONSUMED": gate == "PASS",
            "CLOSURE_1_PACKAGING_REPAIR_GATE_PASS": packaging.get("gate") == "PASS",
            "CLOSURE_2_REFERENCE_FREEZE_READY_CONFIRMED": packaging_summary.get("reference_freeze_ready") is True,
            "CLOSURE_3_PARITY_REPAIR_CLEAN": parity_summary.get("negative_control_parity_clean") is True,
            "CLOSURE_4_ADAPTER_REVIEW_PASS": review.get("gate") == "PASS",
            "CLOSURE_5_ADAPTER_RECEIPT_PASS": adapter.get("gate") == "PASS",
            "CLOSURE_6_PROPOSAL_CANDIDATE_ONLY": proposal.get("proposal_status") == "PROPOSAL_CANDIDATE_ONLY",
            "CLOSURE_7_PROPOSAL_NOT_ACCEPTED": adapter_summary.get("proposal_accepted") is False,
            "CLOSURE_8_NO_IMPLEMENTATION": adapter_summary.get("implementation_authorized") is False,
            "CLOSURE_9_NO_RUNTIME_ADOPTION_AUTHORITY": adapter_summary.get("runtime_adoption_authorized") is False,
            "CLOSURE_10_NO_SCHEMA_MUTATION": adapter_summary.get("schema_mutation_authorized") is False,
            "CLOSURE_11_NO_MOVE_ADDITION": adapter_summary.get("move_addition_authorized") is False,
            "CLOSURE_12_NO_C8_AUTHORIZATION": adapter_summary.get("c8_authorized") is False,
            "CLOSURE_13_PROPOSAL_REVIEW_PENDING_POINTER_EMITTED": PROPOSAL_PENDING_REVIEW_POINTER_PATH.exists(),
            "CLOSURE_14_NO_HIDDEN_NEXT_COMMAND": adapter_summary.get("hidden_next_command") is False,
        },
        "machine_readable_capability_proposal_adapter_reference_closure_summary": {
            "status": status,
            "reference_id": reference_id if gate == "PASS" else None,
            "adapter_reference_branch_closed": gate == "PASS",
            "closed_object": "Capability Proposal Adapter v0",
            "proposal_id": proposal.get("proposal_id"),
            "proposal_kind": proposal.get("proposal_kind"),
            "proposed_surface": proposal.get("proposed_surface"),
            "proposal_status": proposal.get("proposal_status"),
            "proposal_review_pending": True,
            "followup_proposal_review_unit_id": FOLLOWUP_PROPOSAL_REVIEW_UNIT_ID,
            "proposal_accepted": False,
            "proposal_validated": False,
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
            "reference_index": rel(REFERENCE_INDEX_PATH),
            "freeze_manifest": rel(FREEZE_MANIFEST_PATH),
            "proposal_pending_review_pointer": rel(PROPOSAL_PENDING_REVIEW_POINTER_PATH),
            "readout": rel(CLOSURE_READOUT_PATH),
            "rollup": rel(CLOSURE_ROLLUP_PATH),
            "profile": rel(CLOSURE_PROFILE_PATH),
            "report": rel(CLOSURE_REPORT_PATH),
            "transition_trace": rel(CLOSURE_TRANSITION_TRACE_PATH),
        },
        "terminal": transition_trace["terminal"],
    }

    receipt_id = "capability_adapter_reference_closure_receipt_" + sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"capability_proposal_adapter_reference_closure_receipt_id={receipt_id}")
    print(f"capability_proposal_adapter_reference_closure_receipt_path={rel(receipt_path)}")
    print(f"capability_proposal_adapter_reference_id={reference_id if gate == 'PASS' else 'NONE'}")
    print(f"capability_proposal_adapter_followup_proposal_review_unit={FOLLOWUP_PROPOSAL_REVIEW_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
