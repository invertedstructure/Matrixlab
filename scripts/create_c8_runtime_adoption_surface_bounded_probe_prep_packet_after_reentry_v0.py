#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_AFTER_REENTRY_V0"
TARGET_UNIT_ID = "research.c8.runtime_adoption_surface.bounded_probe_prep_packet.after_reentry.v0"
MILESTONE = "C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_CREATED_AFTER_REENTRY"
OUTCOME = "C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_READY_FOR_REVIEW"
STOP_CODE = "STOP_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_READY_FOR_REVIEW"

SOURCE_ACCEPTANCE_RECEIPT_ID = "c8_runtime_adoption_probe_prep_acceptance_receipt_6928390f"
SOURCE_ACCEPTANCE_DECISION_ID = "c8_runtime_adoption_probe_prep_acceptance_decision_5054ed94"
SOURCE_ACCEPTANCE_PACKET_ID = "c8_runtime_adoption_probe_prep_acceptance_packet_85d617c2"
SOURCE_AUTHORITY_ID = "c8_runtime_adoption_probe_prep_authority_ae554f5e"
SOURCE_ACCEPTANCE_BOUNDARY_ID = "c8_runtime_adoption_probe_prep_acceptance_boundary_2783c3e7"

SOURCE_SELECTION_RECEIPT_ID = "c8_successor_surface_selection_receipt_7da4fd41"
SOURCE_SELECTION_DECISION_ID = "c8_successor_surface_selection_decision_4f336833"
SOURCE_SELECTION_PACKET_ID = "c8_successor_surface_selection_packet_f7874bf3"
SOURCE_SELECTION_BOUNDARY_ID = "c8_successor_surface_selection_boundary_ee54442b"

PREVIOUS_SURFACE_ID = "c8_successor_surface_reuse_authority_boundary_after_local_closure_v0"
PREVIOUS_SURFACE_KIND = "REUSE_AUTHORITY_BOUNDARY_SURFACE"
PREVIOUS_SURFACE_LABEL = "C8_POST_CLOSURE_LOCAL_LOOP_REUSE_PRESSURE_SURFACE"

SELECTED_SURFACE_ID = "c8_successor_surface_runtime_adoption_after_reentry_v0"
SELECTED_SURFACE_KIND = "RUNTIME_ADOPTION_SURFACE"
SELECTED_SURFACE_LABEL = "C8_RUNTIME_ADOPTION_AFTER_REUSE_AUTHORITY_CLOSURE_SURFACE"
SELECTED_SURFACE_QUESTION = (
    "After the reuse-authority boundary held and surface-selection reentry was accepted, "
    "what is the smallest runtime-adoption surface that can expose typed halts, receipt mismatches, "
    "projection bugs, missing moves, or gate failures without pre-authorizing build, probe execution, "
    "C8 rerun, or reusable schema promotion?"
)

PROBE_ID = "c8_runtime_adoption_surface_bounded_probe_after_reentry_v0"
PROBE_KIND = "RUNTIME_ADOPTION_BOUNDARY_PROBE"
PROBE_LABEL = "C8_RUNTIME_ADOPTION_BOUNDED_PROBE_AFTER_REENTRY"
PROBE_QUESTION = (
    "What is the smallest controlled runtime-adoption probe that can expose typed halts, "
    "receipt mismatches, projection bugs, missing moves, or gate failures from the committed C8 chain, "
    "while stopping before probe execution authority, runtime build, C8 rerun, or reusable schema promotion?"
)

AUTHORIZED_FUTURE_UNIT = UNIT_ID

OUT_DIR = ROOT / "data/c8_runtime_adoption_surface_bounded_probe_prep_after_reentry_v0"
RECEIPT_DIR = ROOT / "data/c8_runtime_adoption_surface_bounded_probe_prep_after_reentry_v0_receipts"

ACCEPTANCE_RECEIPT = ROOT / "data/c8_runtime_adoption_surface_probe_prep_acceptance_after_reentry_v0_receipts/c8_runtime_adoption_probe_prep_acceptance_receipt_6928390f.json"
ACCEPTANCE_DECISION = ROOT / "data/c8_runtime_adoption_surface_probe_prep_acceptance_after_reentry_v0/c8_runtime_adoption_surface_probe_prep_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = ROOT / "data/c8_runtime_adoption_surface_probe_prep_acceptance_after_reentry_v0/c8_runtime_adoption_surface_probe_prep_acceptance_packet_v0.json"
AUTHORITY_PACKET = ROOT / "data/c8_runtime_adoption_surface_probe_prep_acceptance_after_reentry_v0/c8_runtime_adoption_surface_probe_prep_authority_v0.json"
ACCEPTANCE_BOUNDARY = ROOT / "data/c8_runtime_adoption_surface_probe_prep_acceptance_after_reentry_v0/c8_runtime_adoption_surface_probe_prep_acceptance_boundary_audit_v0.json"
ACCEPTANCE_REPORT = ROOT / "data/c8_runtime_adoption_surface_probe_prep_acceptance_after_reentry_v0/c8_runtime_adoption_surface_probe_prep_acceptance_report.json"

PROBE_SPEC = OUT_DIR / "c8_runtime_adoption_surface_bounded_probe_spec_v0.json"
PREP_PACKET = OUT_DIR / "c8_runtime_adoption_surface_bounded_probe_prep_packet_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_runtime_adoption_surface_bounded_probe_prep_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_runtime_adoption_surface_bounded_probe_prep_readout_v0.json"
REPORT = OUT_DIR / "c8_runtime_adoption_surface_bounded_probe_prep_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "probe_execution_authorized_count",
    "probe_executed_count",
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

def chk(failures: List[str], label: str, got: Any, want: Any) -> None:
    if got != want:
        failures.append(f"{label}_wrong:{got}!={want}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []
    forbidden_counters = {k: 0 for k in FORBIDDEN_COUNTER_KEYS}

    sources = {
        "acceptance_receipt": ACCEPTANCE_RECEIPT,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_packet": ACCEPTANCE_PACKET,
        "authority_packet": AUTHORITY_PACKET,
        "acceptance_boundary": ACCEPTANCE_BOUNDARY,
        "acceptance_report": ACCEPTANCE_REPORT,
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
    acceptance_decision = read_json(ACCEPTANCE_DECISION)
    acceptance_packet = read_json(ACCEPTANCE_PACKET)
    authority_packet = read_json(AUTHORITY_PACKET)
    acceptance_boundary = read_json(ACCEPTANCE_BOUNDARY)
    acceptance_report = read_json(ACCEPTANCE_REPORT)
    acceptance_summary = acceptance_receipt.get("machine_readable_acceptance_summary", {})

    expected_acceptance_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_RUNTIME_ADOPTION_SURFACE_PROBE_PREP_ACCEPTANCE_PASS",
        "outcome_class": "C8_RUNTIME_ADOPTION_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_PREP_ONLY",
        "receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
    }

    for key, want in expected_acceptance_receipt.items():
        chk(failures, f"acceptance_receipt_{key}", acceptance_receipt.get(key), want)

    expected_acceptance_summary = {
        "runtime_adoption_surface_probe_prep_acceptance_complete": True,
        "human_decision": "ACCEPT_SURFACE_FOR_BOUNDED_PROBE_PREP",
        "source_surface_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_surface_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
        "source_surface_selection_decision_id": SOURCE_SELECTION_DECISION_ID,
        "source_surface_selection_boundary_audit_id": SOURCE_SELECTION_BOUNDARY_ID,
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_question": SELECTED_SURFACE_QUESTION,
        "selected_surface_accepted_for_bounded_probe_prep": True,
        "bounded_probe_prep_authorized": True,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authorized_future_probe_prep_packet_creation_count": 1,
        "probe_prep_packet_created_now": False,
        "probe_authorized_now": False,
        "probe_executed_now": False,
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
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
        "recommended_review_unit": "REVIEW_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_ACCEPTANCE_AFTER_REENTRY_V0",
        "next_command_goal": None,
    }

    for key, want in expected_acceptance_summary.items():
        chk(failures, f"acceptance_summary_{key}", acceptance_summary.get(key), want)

    chk(failures, "acceptance_decision_id", acceptance_decision.get("runtime_adoption_probe_prep_acceptance_decision_id"), SOURCE_ACCEPTANCE_DECISION_ID)
    chk(failures, "acceptance_packet_id", acceptance_packet.get("runtime_adoption_probe_prep_acceptance_packet_id"), SOURCE_ACCEPTANCE_PACKET_ID)
    chk(failures, "authority_id", authority_packet.get("runtime_adoption_probe_prep_authority_id"), SOURCE_AUTHORITY_ID)
    chk(failures, "acceptance_boundary_id", acceptance_boundary.get("runtime_adoption_probe_prep_acceptance_boundary_audit_id"), SOURCE_ACCEPTANCE_BOUNDARY_ID)

    expected_authority = {
        "authority_status": "AUTHORIZED_FOR_ONE_BOUNDED_PROBE_PREP_PACKET_CREATION_ONLY",
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
    }

    for key, want in expected_authority.items():
        chk(failures, f"authority_{key}", authority_packet.get(key), want)

    authorized_scope = authority_packet.get("authorized_scope", {})
    if authorized_scope.get("create_bounded_probe_prep_packet") is not True:
        failures.append("authority_create_bounded_probe_prep_packet_not_true")
    if authorized_scope.get("surface_id") != SELECTED_SURFACE_ID:
        failures.append(f"authority_surface_id_wrong:{authorized_scope.get('surface_id')}")

    source_hashes_after = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    if source_hashes_before != source_hashes_after:
        forbidden_counters["source_artifact_mutation_count"] += 1

    local_nonzero = {k: v for k, v in forbidden_counters.items() if v != 0}
    for k, v in local_nonzero.items():
        failures.append(f"{k}:{v}")

    probe_spec = {
        "schema_version": "c8_runtime_adoption_surface_bounded_probe_spec_v0",
        "runtime_adoption_bounded_probe_spec_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_question": PROBE_QUESTION,
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_authority_id": SOURCE_AUTHORITY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_question": SELECTED_SURFACE_QUESTION,
        "probe_scope": {
            "max_probe_execution_count_if_later_accepted": 1,
            "proposal_only_first_pass": True,
            "runtime_adoption_target": "smallest_controlled_runtime_adoption_pass",
            "primary_observation_targets": [
                "typed_halts",
                "receipt_mismatches",
                "projection_bugs",
                "missing_moves",
                "gate_failures",
            ],
            "source_surfaces": [
                SOURCE_ACCEPTANCE_RECEIPT_ID,
                SOURCE_SELECTION_RECEIPT_ID,
                PREVIOUS_SURFACE_ID,
            ],
        },
        "probe_limits": {
            "execution_authorized_now": False,
            "probe_executed_now": False,
            "build_authorized_now": False,
            "c8_rerun_authorized_now": False,
            "reusable_schema_authorized_now": False,
            "global_solution_claim": False,
            "frontier_solved_claim": False,
        },
        "expected_probe_outputs_if_later_executed": [
            "typed_runtime_adoption_observation",
            "typed_halt_or_pass_classification",
            "missing_move_or_missing_instrument_signal_if_exposed",
            "no_authority_leak_audit",
            "review_required_stop",
        ],
    }
    probe_spec["runtime_adoption_bounded_probe_spec_id"] = "c8_runtime_adoption_bounded_probe_spec_" + sig8(probe_spec)
    write_json(PROBE_SPEC, probe_spec)

    prep_packet = {
        "schema_version": "c8_runtime_adoption_surface_bounded_probe_prep_packet_v0",
        "runtime_adoption_bounded_probe_prep_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "prep_packet_status": "BOUNDED_PROBE_PREP_PACKET_READY_FOR_REVIEW",
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
        "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_authority_id": SOURCE_AUTHORITY_ID,
        "source_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
        "source_selection_decision_id": SOURCE_SELECTION_DECISION_ID,
        "source_selection_boundary_id": SOURCE_SELECTION_BOUNDARY_ID,
        "previous_surface_id": PREVIOUS_SURFACE_ID,
        "previous_surface_kind": PREVIOUS_SURFACE_KIND,
        "previous_surface_label": PREVIOUS_SURFACE_LABEL,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_surface_question": SELECTED_SURFACE_QUESTION,
        "source_probe_spec_id": probe_spec["runtime_adoption_bounded_probe_spec_id"],
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_question": PROBE_QUESTION,
        "authorized_future_unit_consumed": UNIT_ID,
        "probe_prep_packet_created": True,
        "probe_prepared_for_review": True,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "cell1_build_authorized_now": False,
        "verification_probe_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "missing_instrument_proposal_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "research_mode_opened": False,
        "general_cell1_authority": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "requires_review": True,
        "recommended_review_unit": "REVIEW_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_AFTER_REENTRY_V0",
        "recommended_next_decision_options": [
            "ACCEPT_FOR_BOUNDED_PROBE_EXECUTION",
            "REJECT_PROBE_PREP_PACKET",
            "NARROW_PROBE_PREP_PACKET",
        ],
    }
    prep_packet["runtime_adoption_bounded_probe_prep_packet_id"] = "c8_runtime_adoption_bounded_probe_prep_packet_" + sig8(prep_packet)
    write_json(PREP_PACKET, prep_packet)

    boundary_audit = {
        "schema_version": "c8_runtime_adoption_surface_bounded_probe_prep_boundary_audit_v0",
        "runtime_adoption_bounded_probe_prep_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_probe_prep_packet_id": prep_packet["runtime_adoption_bounded_probe_prep_packet_id"],
        "source_probe_spec_id": probe_spec["runtime_adoption_bounded_probe_spec_id"],
        "source_authority_id": SOURCE_AUTHORITY_ID,
        "allowed_now": {
            "create_bounded_probe_prep_packet": True,
            "write_probe_spec_for_review": True,
            "record_probe_limits": True,
        },
        "not_allowed_now": {
            "authorize_probe_execution": True,
            "execute_probe": True,
            "build_instrument": True,
            "build_cell1": True,
            "run_verification_probe": True,
            "rerun_c8": True,
            "create_missing_instrument_proposal": True,
            "authorize_reusable_schema": True,
            "open_research_mode": True,
            "claim_global_solution": True,
            "claim_frontier_solved": True,
        },
        "forbidden_counters": forbidden_counters,
        "failures": failures,
        "warnings": warnings,
    }
    boundary_audit["runtime_adoption_bounded_probe_prep_boundary_audit_id"] = "c8_runtime_adoption_bounded_probe_prep_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    gate_results = {
        "BOUNDED_PROBE_PREP_0_SOURCE_ACCEPTANCE_RECEIPT_PASS": acceptance_receipt.get("gate") == "PASS",
        "BOUNDED_PROBE_PREP_1_AUTHORITY_MATCHES_THIS_UNIT": authority_packet.get("authorized_future_unit") == UNIT_ID,
        "BOUNDED_PROBE_PREP_2_EXACTLY_ONE_PREP_CREATION_AUTHORIZED": authority_packet.get("authorized_future_unit_count") == 1,
        "BOUNDED_PROBE_PREP_3_RUNTIME_ADOPTION_SURFACE_MATCHES": acceptance_summary.get("selected_surface_id") == SELECTED_SURFACE_ID and acceptance_summary.get("selected_surface_kind") == SELECTED_SURFACE_KIND,
        "BOUNDED_PROBE_PREP_4_PREP_PACKET_CREATED_FOR_REVIEW": prep_packet["probe_prep_packet_created"] is True and prep_packet["probe_prepared_for_review"] is True,
        "BOUNDED_PROBE_PREP_5_NO_EXECUTION_AUTHORIZED_OR_RUN": prep_packet["probe_execution_authorized_now"] is False and prep_packet["probe_executed_now"] is False,
        "BOUNDED_PROBE_PREP_6_NO_BUILD_RERUN_SCHEMA": prep_packet["instrument_build_authorized_now"] is False and prep_packet["c8_rerun_authorized_now"] is False and prep_packet["reusable_schema_authorized_now"] is False,
        "BOUNDED_PROBE_PREP_7_NO_GLOBAL_OR_FRONTIER_CLAIM": prep_packet["global_solution_claim"] is False and prep_packet["frontier_solved_claim"] is False,
        "BOUNDED_PROBE_PREP_8_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "BOUNDED_PROBE_PREP_9_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "BOUNDED_PROBE_PREP_10_RESULT_REQUIRES_REVIEW": prep_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"bounded_probe_prep_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_PASS" if gate == "PASS" else "TYPED_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_PACKET_FAILED"

    readout = {
        "schema_version": "c8_runtime_adoption_surface_bounded_probe_prep_readout_v0",
        "title": "C8 runtime-adoption bounded probe-prep packet after reentry",
        "status": status,
        "outcome_class": outcome,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_prep_packet_created": True,
        "probe_prepared_for_review": True,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": prep_packet["recommended_review_unit"],
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_runtime_adoption_surface_bounded_probe_prep_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_authority_id": SOURCE_AUTHORITY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_question": PROBE_QUESTION,
        "probe_prep_packet_created": True,
        "probe_prepared_for_review": True,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "requires_review": True,
        "recommended_review_unit": prep_packet["recommended_review_unit"],
        "recommended_next_decision_options": prep_packet["recommended_next_decision_options"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_runtime_adoption_surface_bounded_probe_prep_receipt_v0",
        "receipt_type": "TYPED_C8_RUNTIME_ADOPTION_SURFACE_BOUNDED_PROBE_PREP_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_prep_summary": {
            "runtime_adoption_bounded_probe_prep_packet_created": gate == "PASS",
            "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
            "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
            "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
            "source_authority_id": SOURCE_AUTHORITY_ID,
            "source_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
            "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
            "source_selection_decision_id": SOURCE_SELECTION_DECISION_ID,
            "source_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
            "source_selection_boundary_id": SOURCE_SELECTION_BOUNDARY_ID,
            "previous_surface_id": PREVIOUS_SURFACE_ID,
            "previous_surface_kind": PREVIOUS_SURFACE_KIND,
            "previous_surface_label": PREVIOUS_SURFACE_LABEL,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "selected_surface_question": SELECTED_SURFACE_QUESTION,
            "authorized_future_unit_consumed": UNIT_ID,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "probe_label": PROBE_LABEL,
            "probe_question": PROBE_QUESTION,
            "probe_prep_packet_created": True,
            "probe_prepared_for_review": True,
            "probe_execution_authorized_now": False,
            "probe_executed_now": False,
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
            "forbidden_counters_zero": not bool(local_nonzero),
            "requires_review": True,
            "recommended_review_unit": prep_packet["recommended_review_unit"],
            "recommended_next_decision_options": prep_packet["recommended_next_decision_options"],
            "next_command_goal": None,
        },
        "gate_results": gate_results,
        "forbidden_counters": forbidden_counters,
        "source_artifact_immutability": {
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
        },
        "output_artifacts": {
            "probe_spec": rel(PROBE_SPEC),
            "prep_packet": rel(PREP_PACKET),
            "boundary_audit": rel(BOUNDARY_AUDIT),
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

    receipt["receipt_id"] = "c8_runtime_adoption_bounded_probe_prep_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_adoption_bounded_probe_prep_receipt_id={receipt['receipt_id']}")
    print(f"runtime_adoption_bounded_probe_prep_receipt_path={rel(receipt_path)}")
    print(f"runtime_adoption_bounded_probe_prep_packet_path={rel(PREP_PACKET)}")
    print(f"runtime_adoption_bounded_probe_spec_path={rel(PROBE_SPEC)}")
    print(f"runtime_adoption_bounded_probe_prep_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"selected_surface_id={SELECTED_SURFACE_ID}")
    print(f"selected_surface_kind={SELECTED_SURFACE_KIND}")
    print(f"probe_id={PROBE_ID}")
    print(f"probe_kind={PROBE_KIND}")
    print("probe_prep_packet_created=true")
    print("probe_prepared_for_review=true")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={prep_packet['recommended_review_unit']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
