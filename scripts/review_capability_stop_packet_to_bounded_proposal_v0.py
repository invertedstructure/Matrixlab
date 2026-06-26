#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_CAPABILITY_STOP_PACKET_TO_BOUNDED_PROPOSAL_V0"
TARGET_UNIT_ID = "capability_stop_packet_to_bounded_proposal.review_v0"
NEXT_UNIT_ID = "REPAIR_CAPABILITY_PROPOSAL_ADAPTER_NEGATIVE_CONTROL_PARITY_V0"
SOURCE_ADAPTER_RECEIPT_ID = "capability_adapter_receipt_8c7f0905"

SOURCE_ADAPTER_RECEIPT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0_receipts/capability_adapter_receipt_8c7f0905.json"
SOURCE_INTAKE_REVIEW_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_intake_review_v0.json"
SOURCE_NORMALIZED_STOP_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_stop_packet_v0.json"
SOURCE_PROPOSAL_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/bounded_capability_proposal_v0.json"
SOURCE_HUMAN_DECISION_PACKET_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/human_capability_decision_packet_v0.json"
SOURCE_TRACE_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_proposal_adapter_trace_v0.jsonl"
SOURCE_READOUT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_proposal_adapter_readout_v0.json"
SOURCE_ROLLUP_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_proposal_adapter_rollup_v0.json"
SOURCE_PROFILE_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_proposal_adapter_profile_v0.json"
SOURCE_REPORT_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_proposal_adapter_report.json"
SOURCE_TRANSITION_TRACE_PATH = ROOT / "data/capability_stop_packet_to_bounded_proposal_v0/capability_proposal_adapter_transition_trace.json"

OUT_DIR = ROOT / "data/capability_stop_packet_to_bounded_proposal_review_v0"
RECEIPT_DIR = ROOT / "data/capability_stop_packet_to_bounded_proposal_review_v0_receipts"

BASIS_PATH = OUT_DIR / "capability_proposal_adapter_review_basis_v0.json"
SHAPE_REVIEW_PATH = OUT_DIR / "capability_proposal_adapter_shape_review_v0.json"
BOUNDARY_REVIEW_PATH = OUT_DIR / "capability_proposal_adapter_boundary_review_v0.json"
NEGATIVE_CONTROL_PARITY_REVIEW_PATH = OUT_DIR / "capability_proposal_adapter_negative_control_parity_review_v0.json"
REPAIR_TARGET_PATH = OUT_DIR / "capability_proposal_adapter_negative_control_parity_repair_target_v0.json"
REVIEW_READOUT_PATH = OUT_DIR / "capability_proposal_adapter_review_readout_v0.json"
REVIEW_ROLLUP_PATH = OUT_DIR / "capability_proposal_adapter_review_rollup_v0.json"
REVIEW_PROFILE_PATH = OUT_DIR / "capability_proposal_adapter_review_profile_v0.json"
REVIEW_REPORT_PATH = OUT_DIR / "capability_proposal_adapter_review_report.json"
REVIEW_TRANSITION_TRACE_PATH = OUT_DIR / "capability_proposal_adapter_review_transition_trace.json"

REQUIRED_RECEIPT_NEGATIVE_CONTROLS = [
    "implementation_started_count",
    "runtime_repaired_count",
    "schema_mutated_count",
    "move_added_count",
    "fixture_expanded_count",
    "runtime_patched_count",
    "live_hook_installed_count",
    "runtime_adoption_authority_count",
    "c8_authorized_count",
    "proposal_accepted_count",
    "hidden_next_command_count",
    "latest_file_selection_count",
    "mtime_selection_count",
    "ambient_workspace_inference_count",
    "prior_receipt_mutation_count",
]

REQUIRED_ROLLUP_NEGATIVE_CONTROLS = REQUIRED_RECEIPT_NEGATIVE_CONTROLS[:]

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
        SOURCE_ADAPTER_RECEIPT_PATH,
        SOURCE_INTAKE_REVIEW_PATH,
        SOURCE_NORMALIZED_STOP_PACKET_PATH,
        SOURCE_PROPOSAL_PATH,
        SOURCE_HUMAN_DECISION_PACKET_PATH,
        SOURCE_TRACE_PATH,
        SOURCE_READOUT_PATH,
        SOURCE_ROLLUP_PATH,
        SOURCE_PROFILE_PATH,
        SOURCE_REPORT_PATH,
        SOURCE_TRANSITION_TRACE_PATH,
    ]

    failures: List[str] = []
    source_hashes_before = {}

    for p in required_files:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")
        else:
            source_hashes_before[rel(p)] = file_sha256(p)

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    receipt = read_json(SOURCE_ADAPTER_RECEIPT_PATH)
    intake = read_json(SOURCE_INTAKE_REVIEW_PATH)
    stop_packet = read_json(SOURCE_NORMALIZED_STOP_PACKET_PATH)
    proposal = read_json(SOURCE_PROPOSAL_PATH)
    human_decision = read_json(SOURCE_HUMAN_DECISION_PACKET_PATH)
    readout = read_json(SOURCE_READOUT_PATH)
    rollup = read_json(SOURCE_ROLLUP_PATH)
    profile = read_json(SOURCE_PROFILE_PATH)
    report = read_json(SOURCE_REPORT_PATH)
    transition_trace = read_json(SOURCE_TRANSITION_TRACE_PATH)
    trace_text = SOURCE_TRACE_PATH.read_text()

    summary = receipt.get("machine_readable_capability_proposal_adapter_summary", {})

    hard_failures: List[str] = []
    review_findings: List[Dict[str, Any]] = []

    if receipt.get("receipt_id") != SOURCE_ADAPTER_RECEIPT_ID:
        hard_failures.append(f"adapter_receipt_id_wrong:{receipt.get('receipt_id')}")
    if receipt.get("gate") != "PASS":
        hard_failures.append("adapter_gate_not_pass")
    if summary.get("proposal_emitted") is not True:
        hard_failures.append("proposal_not_emitted")
    if summary.get("proposal_status") != "PROPOSAL_CANDIDATE_ONLY":
        hard_failures.append("proposal_status_not_candidate_only")
    if summary.get("validation_status") != "NOT_VALIDATED_BY_ADAPTER":
        hard_failures.append("validation_status_wrong")
    if summary.get("proposal_kind") != "BOUNDED_TRIGGER_SURFACE_CAPABILITY_PROPOSAL":
        hard_failures.append("proposal_kind_wrong")
    if summary.get("proposed_surface") != "bounded_structured_t6_trigger_surface_capability_v0":
        hard_failures.append("proposed_surface_wrong")
    if summary.get("missing_objects") != ["loop_trigger_surface_missing", "structured_tie_evidence_missing"]:
        hard_failures.append("missing_objects_not_preserved")
    if summary.get("required_capability") != "bounded_structured_t6_trigger_surface_capability":
        hard_failures.append("required_capability_not_preserved")
    if receipt.get("terminal", {}).get("stop_code") != "STOP_CAPABILITY_PROPOSAL_CANDIDATE_EMITTED":
        hard_failures.append("terminal_stop_code_wrong")

    for key in [
        "implementation_authorized",
        "runtime_adoption_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "runtime_patch_authorized",
        "proposal_accepted",
        "hidden_next_command",
        "latest_file_selection_used",
        "mtime_selection_used",
        "ambient_workspace_inference_used",
        "prior_receipt_mutation",
        "c8_authorized",
    ]:
        require_false(summary, key, hard_failures)

    if human_decision.get("decision_required") is not True:
        hard_failures.append("human_decision_not_required")
    if human_decision.get("default_decision") != "DEFER":
        hard_failures.append("human_default_decision_not_defer")
    for key in [
        "implementation_authorized",
        "runtime_adoption_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "c8_authorized",
    ]:
        require_false(human_decision, key, hard_failures)

    proposal_guards = proposal.get("boundary_guards", {})
    for key in [
        "implementation_authorized",
        "runtime_patch_authorized",
        "schema_mutation_authorized",
        "move_addition_authorized",
        "fixture_expansion_authorized",
        "c8_authorized",
    ]:
        require_false(proposal_guards, key, hard_failures)

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
    missing_trace_terms = [t for t in required_trace_terms if t not in trace_text]
    if missing_trace_terms:
        hard_failures.extend([f"trace_term_missing:{t}" for t in missing_trace_terms])

    receipt_neg = receipt.get("negative_controls", {})
    rollup_neg = rollup.get("negative_controls", {})

    receipt_neg_missing = [k for k in REQUIRED_RECEIPT_NEGATIVE_CONTROLS if k not in receipt_neg]
    rollup_neg_missing = [k for k in REQUIRED_ROLLUP_NEGATIVE_CONTROLS if k not in rollup_neg]

    receipt_neg_nonzero = {k: v for k, v in receipt_neg.items() if v != 0}
    rollup_neg_nonzero = {k: v for k, v in rollup_neg.items() if v != 0}

    if receipt_neg_missing:
        review_findings.append({
            "finding_id": "CAPABILITY_ADAPTER_REVIEW_FINDING_NEGATIVE_CONTROL_RECEIPT_PARITY_GAP",
            "severity": "LOCAL_TIGHTENING_REQUIRED",
            "finding_kind": "NEGATIVE_CONTROL_PARITY_GAP",
            "missing_keys": receipt_neg_missing,
            "source": rel(SOURCE_ADAPTER_RECEIPT_PATH),
            "repairable_locally": True,
            "requires_runtime_repair": False,
            "requires_schema_mutation": False,
            "requires_move_addition": False,
            "blocks_reference_freeze": True,
        })

    if rollup_neg_missing:
        review_findings.append({
            "finding_id": "CAPABILITY_ADAPTER_REVIEW_FINDING_NEGATIVE_CONTROL_ROLLUP_PARITY_GAP",
            "severity": "LOCAL_TIGHTENING_REQUIRED",
            "finding_kind": "NEGATIVE_CONTROL_PARITY_GAP",
            "missing_keys": rollup_neg_missing,
            "source": rel(SOURCE_ROLLUP_PATH),
            "repairable_locally": True,
            "requires_runtime_repair": False,
            "requires_schema_mutation": False,
            "requires_move_addition": False,
            "blocks_reference_freeze": True,
        })

    if receipt_neg_nonzero:
        hard_failures.append(f"receipt_negative_controls_nonzero:{receipt_neg_nonzero}")
    if rollup_neg_nonzero:
        hard_failures.append(f"rollup_negative_controls_nonzero:{rollup_neg_nonzero}")

    shape_review = {
        "schema_version": "capability_proposal_adapter_shape_review_v0",
        "review_status": "PASS" if not hard_failures else "FAIL",
        "adapter_receipt_id": receipt.get("receipt_id"),
        "proposal_id": proposal.get("proposal_id"),
        "proposal_kind": proposal.get("proposal_kind"),
        "proposal_status": proposal.get("proposal_status"),
        "human_decision_required": human_decision.get("decision_required"),
        "default_human_decision": human_decision.get("default_decision"),
        "trace_reconstructable": not missing_trace_terms,
        "hard_failures": hard_failures,
    }

    boundary_review = {
        "schema_version": "capability_proposal_adapter_boundary_review_v0",
        "review_status": "PASS" if not hard_failures else "FAIL",
        "proposal_candidate_only": proposal.get("proposal_status") == "PROPOSAL_CANDIDATE_ONLY",
        "validation_status": summary.get("validation_status"),
        "proposal_accepted": summary.get("proposal_accepted"),
        "implementation_authorized": summary.get("implementation_authorized"),
        "runtime_adoption_authorized": summary.get("runtime_adoption_authorized"),
        "schema_mutation_authorized": summary.get("schema_mutation_authorized"),
        "move_addition_authorized": summary.get("move_addition_authorized"),
        "fixture_expansion_authorized": summary.get("fixture_expansion_authorized"),
        "runtime_patch_authorized": summary.get("runtime_patch_authorized"),
        "c8_authorized": summary.get("c8_authorized"),
        "hidden_next_command": summary.get("hidden_next_command"),
        "authority_boundary_clean": not hard_failures,
    }

    parity_review = {
        "schema_version": "capability_proposal_adapter_negative_control_parity_review_v0",
        "review_status": "LOCAL_REPAIR_REQUIRED" if review_findings else "PASS",
        "required_receipt_negative_controls": REQUIRED_RECEIPT_NEGATIVE_CONTROLS,
        "required_rollup_negative_controls": REQUIRED_ROLLUP_NEGATIVE_CONTROLS,
        "receipt_negative_controls_present": sorted(receipt_neg.keys()),
        "rollup_negative_controls_present": sorted(rollup_neg.keys()),
        "receipt_missing_keys": receipt_neg_missing,
        "rollup_missing_keys": rollup_neg_missing,
        "receipt_nonzero": receipt_neg_nonzero,
        "rollup_nonzero": rollup_neg_nonzero,
        "parity_gap_count": len(receipt_neg_missing) + len(rollup_neg_missing),
    }

    review_gate = "PASS" if not hard_failures else "FAIL"
    local_repair_required = bool(review_findings) and review_gate == "PASS"
    reference_freeze_ready = review_gate == "PASS" and not local_repair_required

    status = (
        "TYPED_CAPABILITY_PROPOSAL_ADAPTER_REVIEW_PASS_LOCAL_REPAIR_REQUIRED"
        if local_repair_required
        else "TYPED_CAPABILITY_PROPOSAL_ADAPTER_REVIEW_PASS_REFERENCE_FREEZE_READY"
        if reference_freeze_ready
        else "TYPED_CAPABILITY_PROPOSAL_ADAPTER_REVIEW_GATE_FAIL"
    )

    terminal = {
        "type": "ADVANCE" if local_repair_required else "ADVANCE" if reference_freeze_ready else "STOP",
        "next_unit_id": NEXT_UNIT_ID if local_repair_required else "CLOSE_CAPABILITY_PROPOSAL_ADAPTER_AS_REVIEWED_REFERENCE_V0" if reference_freeze_ready else None,
        "stop_code": None if review_gate == "PASS" else "STOP_CAPABILITY_PROPOSAL_ADAPTER_REVIEW_GATE_FAIL",
    }

    repair_target = {
        "schema_version": "capability_proposal_adapter_negative_control_parity_repair_target_v0",
        "target_status": "READY" if local_repair_required else "NOT_REQUIRED",
        "next_unit_id": NEXT_UNIT_ID if local_repair_required else None,
        "repair_scope": "LOCAL_NEGATIVE_CONTROL_PARITY_ONLY",
        "source_adapter_receipt_ref": rel(SOURCE_ADAPTER_RECEIPT_PATH),
        "source_rollup_ref": rel(SOURCE_ROLLUP_PATH),
        "missing_receipt_negative_control_keys": receipt_neg_missing,
        "missing_rollup_negative_control_keys": rollup_neg_missing,
        "required_action": "Add missing negative-control keys at zero where absent, preserving all source semantics and without accepting, validating, implementing, or freezing the proposal.",
        "forbidden": [
            "proposal acceptance",
            "implementation",
            "runtime repair",
            "runtime patch",
            "schema mutation",
            "move addition",
            "fixture expansion",
            "C8 authorization",
            "prior source receipt mutation without explicit repair receipt",
            "hidden next command",
        ],
    }

    basis = {
        "schema_version": "capability_proposal_adapter_review_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if review_gate == "PASS" else "BASIS_FAIL",
        "source_adapter_receipt_id": SOURCE_ADAPTER_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required_files},
        "basis_claim": "Review the capability proposal adapter as a proposal bridge; do not validate, accept, implement, or freeze unless local schema parity is clean.",
    }

    rollup_out = {
        "schema_version": "capability_proposal_adapter_review_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": review_gate,
        "status": status,
        "hard_failure_count": len(hard_failures),
        "review_finding_count": len(review_findings),
        "local_repair_required": local_repair_required,
        "reference_freeze_ready": reference_freeze_ready,
        "proposal_bridge_valid": review_gate == "PASS",
        "proposal_candidate_only": True,
        "proposal_accepted": False,
        "implementation_authorized": False,
        "runtime_adoption_authorized": False,
        "schema_mutation_authorized": False,
        "move_addition_authorized": False,
        "fixture_expansion_authorized": False,
        "runtime_patch_authorized": False,
        "c8_authorized": False,
        "hidden_next_command": False,
        "next_unit_id": terminal["next_unit_id"],
    }

    readout_out = {
        "schema_version": "capability_proposal_adapter_review_readout_v0",
        "status": status,
        "adapter_receipt_id": receipt.get("receipt_id"),
        "proposal_id": proposal.get("proposal_id"),
        "review_verdict": "VALID_PROPOSAL_BRIDGE_NEEDS_LOCAL_PARITY_REPAIR" if local_repair_required else "VALID_PROPOSAL_BRIDGE_FREEZE_READY" if reference_freeze_ready else "REVIEW_GATE_FAIL",
        "local_repair_required": local_repair_required,
        "repair_target_ref": rel(REPAIR_TARGET_PATH) if local_repair_required else None,
        "reference_freeze_ready": reference_freeze_ready,
        "hard_failures": hard_failures,
        "review_findings": review_findings,
        "interpretation": "Adapter bridge is structurally valid, but reference freeze is blocked until negative-control parity is repaired." if local_repair_required else "Adapter bridge is structurally valid and reference-freeze ready." if reference_freeze_ready else "Adapter review failed hard gates.",
    }

    profile_out = {
        "schema_version": "capability_proposal_adapter_review_profile_v0",
        "profile_status": status,
        "core_rule": "Review adapter output without accepting, validating, implementing, or freezing the proposal unless local parity is clean.",
        "proposal_bridge_valid": review_gate == "PASS",
        "local_repair_required": local_repair_required,
        "reference_freeze_ready": reference_freeze_ready,
        "next_unit_id": terminal["next_unit_id"],
        "must_not_infer": [
            "proposal accepted",
            "capability implementation authorized",
            "runtime repaired",
            "runtime adoption authorized",
            "schema mutation authorized",
            "move addition authorized",
            "fixtures may expand by default",
            "C8 authorized",
        ],
    }

    report_out = {
        "schema_version": "capability_proposal_adapter_review_report_v0",
        "unit_id": UNIT_ID,
        "status": status,
        "summary": {
            "adapter_result": "VALID_AS_PROPOSAL_BRIDGE" if review_gate == "PASS" else "INVALID_AS_PROPOSAL_BRIDGE",
            "freeze_ready": reference_freeze_ready,
            "needs_tightening": local_repair_required,
            "tightening_kind": "negative_control_parity" if local_repair_required else None,
            "implementation_ready": False,
            "human_acceptance_ready": False,
            "validation_path_ready": review_gate == "PASS",
        },
        "findings": review_findings,
        "hard_failures": hard_failures,
    }

    transition_trace_out = {
        "schema_version": "capability_proposal_adapter_review_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "CAPABILITY_PROPOSAL_CANDIDATE_EMITTED",
                "edge": "review proposal bridge shape and authority guards",
                "to": "VALID_PROPOSAL_BRIDGE" if review_gate == "PASS" else "REVIEW_GATE_FAIL",
            },
            {
                "from": "VALID_PROPOSAL_BRIDGE" if review_gate == "PASS" else "REVIEW_GATE_FAIL",
                "edge": "check negative-control schema parity",
                "to": "LOCAL_PARITY_REPAIR_REQUIRED" if local_repair_required else "REFERENCE_FREEZE_READY" if reference_freeze_ready else "STOP_GATE_FAIL",
            },
        ],
        "terminal": terminal,
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (SHAPE_REVIEW_PATH, shape_review),
        (BOUNDARY_REVIEW_PATH, boundary_review),
        (NEGATIVE_CONTROL_PARITY_REVIEW_PATH, parity_review),
        (REPAIR_TARGET_PATH, repair_target),
        (REVIEW_READOUT_PATH, readout_out),
        (REVIEW_ROLLUP_PATH, rollup_out),
        (REVIEW_PROFILE_PATH, profile_out),
        (REVIEW_REPORT_PATH, report_out),
        (REVIEW_TRANSITION_TRACE_PATH, transition_trace_out),
    ]:
        write_json(path, obj)

    source_hashes_after = {rel(p): file_sha256(p) for p in required_files}
    source_mutated = source_hashes_before != source_hashes_after
    if source_mutated:
        review_gate = "FAIL"
        status = "TYPED_CAPABILITY_PROPOSAL_ADAPTER_REVIEW_SOURCE_MUTATION_FAIL"
        hard_failures.append("source_inputs_mutated")
        terminal = {"type": "STOP", "next_unit_id": None, "stop_code": "STOP_CAPABILITY_PROPOSAL_ADAPTER_REVIEW_SOURCE_MUTATION_FAIL"}

    reason_codes = [
        "ADAPTER_RECEIPT_CONSUMED",
        "PROPOSAL_BRIDGE_SHAPE_REVIEWED",
        "AUTHORITY_BOUNDARY_REVIEWED",
        "PROPOSAL_CANDIDATE_ONLY_CONFIRMED",
        "HUMAN_DECISION_PACKET_CONFIRMED",
        "NO_PROPOSAL_ACCEPTANCE",
        "NO_IMPLEMENTATION",
        "NO_RUNTIME_REPAIR",
        "NO_SCHEMA_MUTATION",
        "NO_MOVE_ADDITION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_RUNTIME_PATCH",
        "NO_RUNTIME_ADOPTION_AUTHORITY",
        "NO_C8_AUTHORIZATION",
        "NEGATIVE_CONTROL_PARITY_GAP_FOUND",
        "LOCAL_REPAIR_TARGET_EMITTED",
        "REFERENCE_FREEZE_BLOCKED_UNTIL_REPAIR",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if local_repair_required else [
        "ADAPTER_RECEIPT_CONSUMED",
        "PROPOSAL_BRIDGE_SHAPE_REVIEWED",
        "AUTHORITY_BOUNDARY_REVIEWED",
        "PROPOSAL_CANDIDATE_ONLY_CONFIRMED",
        "NEGATIVE_CONTROL_PARITY_CLEAN",
        "REFERENCE_FREEZE_READY",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if reference_freeze_ready else hard_failures

    receipt_out = {
        "schema_version": "capability_proposal_adapter_review_receipt_v0",
        "receipt_type": "TYPED_CAPABILITY_PROPOSAL_ADAPTER_REVIEW_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "source_adapter_receipt_id": SOURCE_ADAPTER_RECEIPT_ID,
        "source_adapter_receipt_ref": rel(SOURCE_ADAPTER_RECEIPT_PATH),
        "gate": review_gate,
        "status": status,
        "failures": hard_failures,
        "warnings": [],
        "review_findings": review_findings,
        "acceptance_gate_results": {
            "REVIEW_0_ADAPTER_RECEIPT_CONSUMED": review_gate == "PASS",
            "REVIEW_1_PROPOSAL_EMITTED": summary.get("proposal_emitted") is True,
            "REVIEW_2_PROPOSAL_CANDIDATE_ONLY": summary.get("proposal_status") == "PROPOSAL_CANDIDATE_ONLY",
            "REVIEW_3_HUMAN_DECISION_PACKET_EMITTED": summary.get("human_decision_packet_emitted") is True,
            "REVIEW_4_NO_IMPLEMENTATION_AUTHORITY": summary.get("implementation_authorized") is False,
            "REVIEW_5_NO_RUNTIME_REPAIR": summary.get("runtime_patch_authorized") is False,
            "REVIEW_6_NO_SCHEMA_MUTATION": summary.get("schema_mutation_authorized") is False,
            "REVIEW_7_NO_MOVE_ADDITION": summary.get("move_addition_authorized") is False,
            "REVIEW_8_NO_C8_AUTHORIZATION": summary.get("c8_authorized") is False,
            "REVIEW_9_TRACE_RECONSTRUCTABLE": not missing_trace_terms,
            "REVIEW_10_NEGATIVE_CONTROL_PARITY_CHECKED": True,
            "REVIEW_11_LOCAL_REPAIR_TARGET_EMITTED_IF_REQUIRED": (local_repair_required and REPAIR_TARGET_PATH.exists()) or not local_repair_required,
            "REVIEW_12_SOURCE_INPUTS_NOT_MUTATED": not source_mutated,
            "REVIEW_13_NO_HIDDEN_NEXT_COMMAND": summary.get("hidden_next_command") is False,
        },
        "machine_readable_capability_proposal_adapter_review_summary": {
            "status": status,
            "adapter_receipt_id": receipt.get("receipt_id"),
            "proposal_id": proposal.get("proposal_id"),
            "proposal_kind": proposal.get("proposal_kind"),
            "proposed_surface": proposal.get("proposed_surface"),
            "proposal_bridge_valid": review_gate == "PASS",
            "review_verdict": readout_out["review_verdict"],
            "local_repair_required": local_repair_required,
            "repair_target_unit_id": NEXT_UNIT_ID if local_repair_required else None,
            "reference_freeze_ready": reference_freeze_ready,
            "negative_control_parity_gap_count": parity_review["parity_gap_count"],
            "missing_receipt_negative_control_keys": receipt_neg_missing,
            "missing_rollup_negative_control_keys": rollup_neg_missing,
            "implementation_authorized": False,
            "runtime_adoption_authorized": False,
            "schema_mutation_authorized": False,
            "move_addition_authorized": False,
            "fixture_expansion_authorized": False,
            "runtime_patch_authorized": False,
            "proposal_accepted": False,
            "human_acceptance_ready": False,
            "validation_path_ready": review_gate == "PASS",
            "hidden_next_command": False,
            "c8_authorized": False,
            "next_unit_id": terminal["next_unit_id"],
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "shape_review": rel(SHAPE_REVIEW_PATH),
            "boundary_review": rel(BOUNDARY_REVIEW_PATH),
            "negative_control_parity_review": rel(NEGATIVE_CONTROL_PARITY_REVIEW_PATH),
            "repair_target": rel(REPAIR_TARGET_PATH),
            "readout": rel(REVIEW_READOUT_PATH),
            "rollup": rel(REVIEW_ROLLUP_PATH),
            "profile": rel(REVIEW_PROFILE_PATH),
            "report": rel(REVIEW_REPORT_PATH),
            "transition_trace": rel(REVIEW_TRANSITION_TRACE_PATH),
        },
        "terminal": terminal,
    }

    receipt_id = "capability_adapter_review_receipt_" + sig8(receipt_out)
    receipt_out["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_out["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_out)

    print(json.dumps(receipt_out, indent=2, sort_keys=True))
    print(f"capability_proposal_adapter_review_receipt_id={receipt_id}")
    print(f"capability_proposal_adapter_review_receipt_path={rel(receipt_path)}")
    print(f"capability_proposal_adapter_review_next_unit={terminal['next_unit_id'] or 'NONE'}")

    return 0 if review_gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
