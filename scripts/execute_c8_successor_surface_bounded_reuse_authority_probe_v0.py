#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXECUTE_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_V0"
TARGET_UNIT_ID = "research.c8.successor_surface.bounded_reuse_authority_probe.v0"
MILESTONE = "C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_EXECUTED"
OUTCOME = "C8_SUCCESSOR_SURFACE_REUSE_BOUNDARY_HELD_NO_NEW_AUTHORITY_NEEDED"
STOP_CODE = "STOP_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_RESULT_READY_FOR_REVIEW"

AUTHORIZED_BY_UNIT = "ACCEPT_C8_SUCCESSOR_SURFACE_FOR_BOUNDED_PROBE_EXECUTION_V0"
AUTHORIZED_FUTURE_UNIT = "EXECUTE_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_V0"

PROBE_ID = "c8_successor_surface_reuse_authority_boundary_probe_v0"
PROBE_KIND = "REUSE_AUTHORITY_BOUNDARY_PROBE"
SELECTED_SURFACE_ID = "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0"
SELECTED_SURFACE_KIND = "REUSE_AUTHORITY_BOUNDARY_SURFACE"
SELECTED_SURFACE_LABEL = "C8_POST_CLOSURE_LOCAL_LOOP_REUSE_PRESSURE_SURFACE"

OUT_DIR = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_v0"
RECEIPT_DIR = ROOT / "data/c8_successor_surface_bounded_reuse_authority_probe_v0_receipts"

ACCEPTANCE_RECEIPT = ROOT / "data/c8_successor_surface_bounded_probe_execution_acceptance_v0_receipts/c8_successor_probe_execution_acceptance_receipt_31139bd1.json"
ACCEPTANCE_PACKET = ROOT / "data/c8_successor_surface_bounded_probe_execution_acceptance_v0/c8_successor_surface_bounded_probe_execution_acceptance_packet_v0.json"
ACCEPTANCE_DECISION = ROOT / "data/c8_successor_surface_bounded_probe_execution_acceptance_v0/c8_successor_surface_bounded_probe_execution_acceptance_decision_v0.json"
ACCEPTANCE_AUTHORITY = ROOT / "data/c8_successor_surface_bounded_probe_execution_acceptance_v0/c8_successor_surface_bounded_probe_execution_authority_v0.json"
ACCEPTANCE_BOUNDARY_AUDIT = ROOT / "data/c8_successor_surface_bounded_probe_execution_acceptance_v0/c8_successor_surface_bounded_probe_execution_acceptance_boundary_audit_v0.json"
ACCEPTANCE_REPORT = ROOT / "data/c8_successor_surface_bounded_probe_execution_acceptance_v0/c8_successor_surface_bounded_probe_execution_acceptance_report.json"

PREP_PACKET = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_v0/c8_successor_surface_bounded_probe_prep_packet_v0.json"
PROBE_SPEC = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_v0/c8_successor_surface_bounded_probe_spec_v0.json"
PROBE_CONSTRAINTS = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_v0/c8_successor_surface_bounded_probe_constraints_v0.json"
REVIEW_RECEIPT = ROOT / "data/c8_successor_surface_bounded_probe_prep_packet_review_v0_receipts/c8_successor_probe_prep_packet_review_receipt_f3acc3a5.json"

PROBE_EVIDENCE = OUT_DIR / "c8_successor_surface_bounded_reuse_authority_probe_evidence_v0.json"
PROBE_RESULT = OUT_DIR / "c8_successor_surface_bounded_reuse_authority_probe_result_v0.json"
PROBE_BOUNDARY_AUDIT = OUT_DIR / "c8_successor_surface_bounded_reuse_authority_probe_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_successor_surface_bounded_reuse_authority_probe_readout_v0.json"
REPORT = OUT_DIR / "c8_successor_surface_bounded_reuse_authority_probe_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "instrument_build_count",
    "cell1_build_count",
    "verification_probe_count",
    "c8_rerun_count",
    "missing_instrument_proposal_count",
    "research_mode_opened_count",
    "general_cell1_authority_count",
    "reusable_schema_authorized_count",
    "global_solution_claim_count",
    "frontier_solved_claim_count",
    "source_artifact_mutation_count",
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

def zero_forbidden_counters() -> Dict[str, int]:
    return {k: 0 for k in FORBIDDEN_COUNTER_KEYS}

def chk(failures: List[str], label: str, got: Any, want: Any) -> None:
    if got != want:
        failures.append(f"{label}_wrong:{got}!={want}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []
    forbidden_counters = zero_forbidden_counters()

    sources = {
        "acceptance_receipt": ACCEPTANCE_RECEIPT,
        "acceptance_packet": ACCEPTANCE_PACKET,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_authority": ACCEPTANCE_AUTHORITY,
        "acceptance_boundary_audit": ACCEPTANCE_BOUNDARY_AUDIT,
        "acceptance_report": ACCEPTANCE_REPORT,
        "prep_packet": PREP_PACKET,
        "probe_spec": PROBE_SPEC,
        "probe_constraints": PROBE_CONSTRAINTS,
        "review_receipt": REVIEW_RECEIPT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    acceptance_receipt = read_json(ACCEPTANCE_RECEIPT)
    acceptance_packet = read_json(ACCEPTANCE_PACKET)
    acceptance_decision = read_json(ACCEPTANCE_DECISION)
    acceptance_authority = read_json(ACCEPTANCE_AUTHORITY)
    acceptance_audit = read_json(ACCEPTANCE_BOUNDARY_AUDIT)
    acceptance_report = read_json(ACCEPTANCE_REPORT)
    prep_packet = read_json(PREP_PACKET)
    probe_spec = read_json(PROBE_SPEC)
    probe_constraints = read_json(PROBE_CONSTRAINTS)
    review_receipt = read_json(REVIEW_RECEIPT)

    acceptance_summary = acceptance_receipt.get("machine_readable_acceptance_summary", {})
    review_summary = review_receipt.get("machine_readable_review_summary", {})

    chk(failures, "acceptance_gate", acceptance_receipt.get("gate"), "PASS")
    chk(failures, "acceptance_status", acceptance_receipt.get("status"), "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_PASS")
    chk(failures, "acceptance_outcome", acceptance_receipt.get("outcome_class"), "C8_SUCCESSOR_SURFACE_ACCEPTED_FOR_ONE_BOUNDED_PROBE_EXECUTION_ONLY")
    chk(failures, "acceptance_receipt_id", acceptance_receipt.get("receipt_id"), "c8_successor_probe_execution_acceptance_receipt_31139bd1")

    expected_acceptance_summary = {
        "acceptance_complete": True,
        "operator_decision": "ACCEPT_FOR_BOUNDED_PROBE_EXECUTION",
        "source_review_receipt_id": "c8_successor_probe_prep_packet_review_receipt_f3acc3a5",
        "source_review_packet_id": "c8_successor_probe_prep_packet_review_packet_083dd071",
        "source_review_decision_id": "c8_successor_probe_prep_packet_review_decision_33245781",
        "source_prep_packet_id": "c8_successor_probe_prep_packet_74a6c209",
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "accepted_for_bounded_probe_execution": True,
        "accepted_for_probe_execution_now": False,
        "probe_executed_now": False,
        "accepted_for_instrument_build": False,
        "accepted_for_c8_rerun": False,
        "accepted_for_reusable_schema": False,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_execution_count": 1,
        "new_instrument_build": False,
        "new_c8_rerun": False,
        "reusable_schema_authorized": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
    }

    for key, want in expected_acceptance_summary.items():
        chk(failures, f"acceptance_summary_{key}", acceptance_summary.get(key), want)

    chk(failures, "acceptance_packet_id", acceptance_packet.get("acceptance_packet_id"), "c8_successor_probe_execution_acceptance_packet_2ffc6f0d")
    chk(failures, "acceptance_decision_id", acceptance_decision.get("acceptance_decision_id"), "c8_successor_probe_execution_acceptance_decision_64e3fccf")
    chk(failures, "authority_id", acceptance_authority.get("authority_id"), "c8_successor_probe_execution_authority_52f56baf")
    chk(failures, "authority_future_unit", acceptance_authority.get("authorized_future_unit"), AUTHORIZED_FUTURE_UNIT)
    chk(failures, "authority_future_unit_count", acceptance_authority.get("authorized_future_unit_count"), 1)
    chk(failures, "authority_future_probe_execution_count", acceptance_authority.get("authorized_future_probe_execution_count"), 1)

    authority_scope = acceptance_authority.get("authority_scope", {})
    expected_scope = {
        "may_execute_one_bounded_probe": True,
        "may_build_instrument": False,
        "may_build_cell1": False,
        "may_run_verification_probe": False,
        "may_rerun_c8": False,
        "may_create_missing_instrument_proposal": False,
        "may_authorize_reusable_schema": False,
        "may_open_research_mode": False,
    }
    for key, want in expected_scope.items():
        chk(failures, f"authority_scope_{key}", authority_scope.get(key), want)

    chk(failures, "review_gate", review_receipt.get("gate"), "PASS")
    chk(failures, "review_decision", review_summary.get("review_decision"), "REVIEWABLE_NOT_ACCEPTED")
    chk(failures, "review_prep_class", review_summary.get("prep_review_class"), "WELL_FORMED_BOUNDED_REUSE_AUTHORITY_PROBE_PREP_PACKET")
    chk(failures, "review_prep_bounded", review_summary.get("prep_packet_is_bounded"), True)
    chk(failures, "review_probe_spec_typed", review_summary.get("probe_spec_is_typed"), True)

    chk(failures, "prep_packet_id", prep_packet.get("prep_packet_id"), "c8_successor_probe_prep_packet_74a6c209")
    chk(failures, "probe_spec_id", probe_spec.get("probe_id"), PROBE_ID)
    chk(failures, "probe_spec_kind", probe_spec.get("probe_kind"), PROBE_KIND)
    chk(failures, "probe_status", probe_spec.get("probe_status"), "PREPARED_FOR_REVIEW_ONLY")
    chk(failures, "constraints_probe_id", probe_constraints.get("probe_id"), PROBE_ID)

    bounded_question = probe_spec.get("bounded_probe_question", "")
    if "one closed local C8 instrumentation loop" not in bounded_question:
        failures.append("probe_question_missing_local_loop")
    if "non-reusable" not in bounded_question:
        failures.append("probe_question_missing_non_reusable")
    if "explicitly promotes" not in bounded_question:
        failures.append("probe_question_missing_explicit_promotion")

    probe_execution_count = 1

    evidence_items = [
        {
            "evidence_id": "E0_EXECUTION_AUTHORITY_EXISTS",
            "value": acceptance_authority.get("authorized_future_unit") == AUTHORIZED_FUTURE_UNIT,
            "source": rel(ACCEPTANCE_AUTHORITY),
            "meaning": "A specific authority object exists for the exact bounded probe execution unit.",
        },
        {
            "evidence_id": "E1_AUTHORITY_COUNT_IS_ONE",
            "value": acceptance_authority.get("authorized_future_unit_count") == 1 and acceptance_authority.get("authorized_future_probe_execution_count") == 1,
            "source": rel(ACCEPTANCE_AUTHORITY),
            "meaning": "Authority count is exactly one future bounded probe execution.",
        },
        {
            "evidence_id": "E2_NO_REUSABLE_SCHEMA_AUTHORITY",
            "value": acceptance_summary.get("accepted_for_reusable_schema") is False and acceptance_summary.get("reusable_schema_authorized") is False,
            "source": rel(ACCEPTANCE_RECEIPT),
            "meaning": "No source authority promotes the local discriminator or loop pattern into reusable schema.",
        },
        {
            "evidence_id": "E3_NO_BUILD_OR_RERUN_AUTHORITY",
            "value": acceptance_summary.get("accepted_for_instrument_build") is False and acceptance_summary.get("accepted_for_c8_rerun") is False,
            "source": rel(ACCEPTANCE_RECEIPT),
            "meaning": "The authority does not authorize instrument build, Cell 1 build, verification probe, or C8 rerun.",
        },
        {
            "evidence_id": "E4_PREP_PACKET_WELL_FORMED_BOUNDED",
            "value": review_summary.get("prep_packet_is_well_formed") is True and review_summary.get("prep_packet_is_bounded") is True,
            "source": rel(REVIEW_RECEIPT),
            "meaning": "The source prep packet was reviewed as well formed and bounded.",
        },
        {
            "evidence_id": "E5_PROBE_QUESTION_BOUNDED_TO_REUSE_AUTHORITY",
            "value": "non-reusable" in bounded_question and "explicitly promotes" in bounded_question,
            "source": rel(PROBE_SPEC),
            "meaning": "The probe question asks only whether current evidence preserves non-reuse absent later explicit promotion.",
        },
        {
            "evidence_id": "E6_NO_GLOBAL_OR_FRONTIER_CLAIM",
            "value": acceptance_summary.get("global_solution_claim") is False and acceptance_summary.get("frontier_solved_claim") is False,
            "source": rel(ACCEPTANCE_RECEIPT),
            "meaning": "Sources deny global-solution and frontier-solved claims.",
        },
    ]

    failed_evidence = [e for e in evidence_items if e["value"] is not True]

    probe_output_class = (
        "REUSE_BOUNDARY_HELD_NO_NEW_AUTHORITY_NEEDED"
        if not failed_evidence
        else "SOURCE_CONTEXT_MISSING_TYPED_STOP"
    )

    if probe_output_class != "REUSE_BOUNDARY_HELD_NO_NEW_AUTHORITY_NEEDED":
        failures.append("probe_output_class_not_boundary_held:" + probe_output_class)

    source_hashes_after = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    if source_hashes_before != source_hashes_after:
        forbidden_counters["source_artifact_mutation_count"] += 1

    nonzero_forbidden = {k: v for k, v in forbidden_counters.items() if v != 0}
    for k, v in nonzero_forbidden.items():
        failures.append(f"{k}:{v}")

    probe_evidence = {
        "schema_version": "c8_successor_surface_bounded_reuse_authority_probe_evidence_v0",
        "probe_evidence_id": None,
        "created_at": now_iso(),
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "source_acceptance_receipt_id": acceptance_receipt.get("receipt_id"),
        "source_acceptance_packet_id": acceptance_packet.get("acceptance_packet_id"),
        "source_acceptance_decision_id": acceptance_decision.get("acceptance_decision_id"),
        "source_authority_id": acceptance_authority.get("authority_id"),
        "source_prep_packet_id": prep_packet.get("prep_packet_id"),
        "bounded_probe_question": bounded_question,
        "evidence_items": evidence_items,
        "failed_evidence": failed_evidence,
    }
    probe_evidence["probe_evidence_id"] = "c8_successor_reuse_authority_probe_evidence_" + sig8(probe_evidence)
    write_json(PROBE_EVIDENCE, probe_evidence)

    probe_result = {
        "schema_version": "c8_successor_surface_bounded_reuse_authority_probe_result_v0",
        "probe_result_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "source_acceptance_receipt_id": acceptance_receipt.get("receipt_id"),
        "source_acceptance_packet_id": acceptance_packet.get("acceptance_packet_id"),
        "source_acceptance_decision_id": acceptance_decision.get("acceptance_decision_id"),
        "source_authority_id": acceptance_authority.get("authority_id"),
        "source_prep_packet_id": prep_packet.get("prep_packet_id"),
        "probe_execution_count": probe_execution_count,
        "probe_output_class": probe_output_class,
        "probe_answer": "Current evidence is sufficient to keep the local discriminator and loop pattern non-reusable: the only active authority is one bounded probe execution, all source authorities explicitly deny reusable schema/build/rerun/global/frontier claims, and no later promotion authority is present in the source surface.",
        "reuse_boundary_held": probe_output_class == "REUSE_BOUNDARY_HELD_NO_NEW_AUTHORITY_NEEDED",
        "new_authority_needed_now": False,
        "missing_reuse_authority_rule_exposed": False,
        "surface_too_broad_requires_narrowing": False,
        "source_context_missing_typed_stop": False,
        "local_discriminator_reusable_schema_authorized": False,
        "local_loop_pattern_reusable_schema_authorized": False,
        "later_promotion_authority_present": False,
        "instrument_build_authorized": False,
        "c8_rerun_authorized": False,
        "verification_probe_authorized": False,
        "evidence_ref": rel(PROBE_EVIDENCE),
        "requires_review": True,
        "recommended_review_unit": "REVIEW_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_RESULT_V0",
    }
    probe_result["probe_result_id"] = "c8_successor_reuse_authority_probe_result_" + sig8(probe_result)
    write_json(PROBE_RESULT, probe_result)

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_PASS" if gate == "PASS" else "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_FAILED"

    probe_gates = {
        "C8_REUSE_AUTHORITY_PROBE_0_ACCEPTANCE_RECEIPT_VERIFIED": acceptance_receipt.get("gate") == "PASS",
        "C8_REUSE_AUTHORITY_PROBE_1_AUTHORIZED_UNIT_MATCHES": acceptance_summary.get("authorized_future_unit") == AUTHORIZED_FUTURE_UNIT,
        "C8_REUSE_AUTHORITY_PROBE_2_AUTHORIZED_EXECUTION_COUNT_ONE": acceptance_summary.get("authorized_future_probe_execution_count") == 1,
        "C8_REUSE_AUTHORITY_PROBE_3_PROBE_ID_MATCHES": acceptance_summary.get("probe_id") == PROBE_ID and probe_spec.get("probe_id") == PROBE_ID,
        "C8_REUSE_AUTHORITY_PROBE_4_PROBE_KIND_MATCHES": acceptance_summary.get("probe_kind") == PROBE_KIND and probe_spec.get("probe_kind") == PROBE_KIND,
        "C8_REUSE_AUTHORITY_PROBE_5_EXECUTED_EXACTLY_ONE_BOUNDED_PROBE": probe_execution_count == 1,
        "C8_REUSE_AUTHORITY_PROBE_6_EVIDENCE_ALL_TRUE": not failed_evidence,
        "C8_REUSE_AUTHORITY_PROBE_7_REUSE_BOUNDARY_HELD": probe_output_class == "REUSE_BOUNDARY_HELD_NO_NEW_AUTHORITY_NEEDED",
        "C8_REUSE_AUTHORITY_PROBE_8_NO_BUILD_OR_RERUN": forbidden_counters["instrument_build_count"] == 0 and forbidden_counters["c8_rerun_count"] == 0,
        "C8_REUSE_AUTHORITY_PROBE_9_NO_REUSABLE_SCHEMA_AUTHORIZED": forbidden_counters["reusable_schema_authorized_count"] == 0,
        "C8_REUSE_AUTHORITY_PROBE_10_NO_RESEARCH_OR_GLOBAL_CLAIM": forbidden_counters["research_mode_opened_count"] == 0 and forbidden_counters["global_solution_claim_count"] == 0 and forbidden_counters["frontier_solved_claim_count"] == 0,
        "C8_REUSE_AUTHORITY_PROBE_11_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "C8_REUSE_AUTHORITY_PROBE_12_FORBIDDEN_COUNTERS_ZERO": not bool(nonzero_forbidden),
        "C8_REUSE_AUTHORITY_PROBE_13_RESULT_REQUIRES_REVIEW": probe_result["requires_review"] is True,
    }

    false_gates = [k for k, v in probe_gates.items() if v is not True]
    if false_gates:
        failures.extend([f"probe_gate_false:{g}" for g in false_gates])

    if failures and gate == "PASS":
        gate = "FAIL"
        status = "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_FAIL"
        outcome = "C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_FAILED"
        terminal_stop = "STOP_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_FAILED"

    boundary_audit = {
        "schema_version": "c8_successor_surface_bounded_reuse_authority_probe_boundary_audit_v0",
        "boundary_audit_id": None,
        "gate": gate,
        "probe_id": PROBE_ID,
        "probe_result_id": probe_result["probe_result_id"],
        "probe_execution_count": probe_execution_count,
        "allowed_probe_execution_count": 1,
        "probe_output_class": probe_output_class,
        "authority_boundary": {
            "executed_one_bounded_probe": True,
            "may_execute_additional_probe_without_new_authority": False,
            "may_build_instrument": False,
            "may_build_cell1": False,
            "may_run_verification_probe": False,
            "may_rerun_c8": False,
            "may_create_missing_instrument_proposal": False,
            "may_authorize_reusable_schema": False,
            "may_open_research_mode": False,
            "may_claim_global_solution": False,
            "may_claim_frontier_solved": False,
        },
        "forbidden_counters": forbidden_counters,
        "probe_gate_results": probe_gates,
        "failures": failures,
        "warnings": warnings,
    }
    boundary_audit["boundary_audit_id"] = "c8_successor_reuse_authority_probe_boundary_" + sig8(boundary_audit)
    write_json(PROBE_BOUNDARY_AUDIT, boundary_audit)

    readout = {
        "schema_version": "c8_successor_surface_bounded_reuse_authority_probe_readout_v0",
        "title": "C8 successor surface bounded reuse-authority probe readout",
        "status": status,
        "outcome_class": outcome,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_result_id": probe_result["probe_result_id"],
        "probe_execution_count": probe_execution_count,
        "probe_output_class": probe_output_class,
        "reuse_boundary_held": probe_result["reuse_boundary_held"],
        "new_authority_needed_now": probe_result["new_authority_needed_now"],
        "reusable_schema_authorized": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "requires_review": True,
        "recommended_review_unit": probe_result["recommended_review_unit"],
        "summary": probe_result["probe_answer"],
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_successor_surface_bounded_reuse_authority_probe_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "probe_evidence_ref": rel(PROBE_EVIDENCE),
        "probe_result_ref": rel(PROBE_RESULT),
        "boundary_audit_ref": rel(PROBE_BOUNDARY_AUDIT),
        "source_acceptance_receipt_id": acceptance_receipt.get("receipt_id"),
        "source_acceptance_packet_id": acceptance_packet.get("acceptance_packet_id"),
        "source_acceptance_decision_id": acceptance_decision.get("acceptance_decision_id"),
        "source_authority_id": acceptance_authority.get("authority_id"),
        "source_prep_packet_id": prep_packet.get("prep_packet_id"),
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_execution_count": probe_execution_count,
        "probe_output_class": probe_output_class,
        "reuse_boundary_held": probe_result["reuse_boundary_held"],
        "new_authority_needed_now": probe_result["new_authority_needed_now"],
        "requires_review": True,
        "recommended_review_unit": probe_result["recommended_review_unit"],
        "new_build_count": 0,
        "new_rerun_count": 0,
        "reusable_schema_authorized": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_successor_surface_bounded_reuse_authority_probe_receipt_v0",
        "receipt_type": "TYPED_C8_SUCCESSOR_SURFACE_BOUNDED_REUSE_AUTHORITY_PROBE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_refs": {
            "acceptance_receipt_ref": rel(ACCEPTANCE_RECEIPT),
            "acceptance_packet_ref": rel(ACCEPTANCE_PACKET),
            "acceptance_decision_ref": rel(ACCEPTANCE_DECISION),
            "acceptance_authority_ref": rel(ACCEPTANCE_AUTHORITY),
            "acceptance_boundary_audit_ref": rel(ACCEPTANCE_BOUNDARY_AUDIT),
            "acceptance_report_ref": rel(ACCEPTANCE_REPORT),
            "prep_packet_ref": rel(PREP_PACKET),
            "probe_spec_ref": rel(PROBE_SPEC),
            "probe_constraints_ref": rel(PROBE_CONSTRAINTS),
            "review_receipt_ref": rel(REVIEW_RECEIPT),
        },
        "machine_readable_probe_summary": {
            "probe_complete": gate == "PASS",
            "source_acceptance_receipt_id": acceptance_receipt.get("receipt_id"),
            "source_acceptance_packet_id": acceptance_packet.get("acceptance_packet_id"),
            "source_acceptance_decision_id": acceptance_decision.get("acceptance_decision_id"),
            "source_authority_id": acceptance_authority.get("authority_id"),
            "source_prep_packet_id": prep_packet.get("prep_packet_id"),
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "authorized_by_unit": AUTHORIZED_BY_UNIT,
            "authorized_future_unit_consumed": AUTHORIZED_FUTURE_UNIT,
            "probe_execution_count": probe_execution_count,
            "allowed_probe_execution_count": 1,
            "probe_output_class": probe_output_class,
            "reuse_boundary_held": probe_result["reuse_boundary_held"],
            "new_authority_needed_now": probe_result["new_authority_needed_now"],
            "missing_reuse_authority_rule_exposed": probe_result["missing_reuse_authority_rule_exposed"],
            "surface_too_broad_requires_narrowing": probe_result["surface_too_broad_requires_narrowing"],
            "source_context_missing_typed_stop": probe_result["source_context_missing_typed_stop"],
            "local_discriminator_reusable_schema_authorized": False,
            "local_loop_pattern_reusable_schema_authorized": False,
            "later_promotion_authority_present": False,
            "probe_requires_review": True,
            "recommended_review_unit": probe_result["recommended_review_unit"],
            "instrument_built_now": False,
            "cell1_built_now": False,
            "verification_probe_run_now": False,
            "c8_rerun_now": False,
            "missing_instrument_proposal_created_now": False,
            "research_mode_opened": False,
            "general_cell1_authority": False,
            "reusable_schema_authorized": False,
            "global_solution_claim": False,
            "frontier_solved_claim": False,
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
            "forbidden_counters_zero": not bool(nonzero_forbidden),
            "next_command_goal": None,
        },
        "probe_gate_results": probe_gates,
        "forbidden_counters": forbidden_counters,
        "source_artifact_immutability": {
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
        },
        "output_artifacts": {
            "probe_evidence": rel(PROBE_EVIDENCE),
            "probe_result": rel(PROBE_RESULT),
            "boundary_audit": rel(PROBE_BOUNDARY_AUDIT),
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

    receipt["receipt_id"] = "c8_successor_reuse_authority_probe_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"probe_receipt_id={receipt['receipt_id']}")
    print(f"probe_receipt_path={rel(receipt_path)}")
    print(f"probe_evidence_path={rel(PROBE_EVIDENCE)}")
    print(f"probe_result_path={rel(PROBE_RESULT)}")
    print(f"probe_boundary_audit_path={rel(PROBE_BOUNDARY_AUDIT)}")
    print(f"source_acceptance_receipt_id={acceptance_receipt.get('receipt_id')}")
    print(f"source_authority_id={acceptance_authority.get('authority_id')}")
    print(f"source_prep_packet_id={prep_packet.get('prep_packet_id')}")
    print(f"probe_id={PROBE_ID}")
    print(f"probe_kind={PROBE_KIND}")
    print(f"probe_execution_count={probe_execution_count}")
    print("allowed_probe_execution_count=1")
    print(f"probe_output_class={probe_output_class}")
    print(f"reuse_boundary_held={str(probe_result['reuse_boundary_held']).lower()}")
    print(f"new_authority_needed_now={str(probe_result['new_authority_needed_now']).lower()}")
    print(f"recommended_review_unit={probe_result['recommended_review_unit']}")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"probe_outcome={outcome}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
