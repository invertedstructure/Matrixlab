#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_FOR_ONE_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.bounded_probe.execution_acceptance.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_ACCEPTED_FOR_ONE_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE"
OUTCOME = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_ACCEPTED_FOR_ONE_EXECUTION_READY_FOR_REVIEW"
STOP_CODE = "STOP_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_READY_FOR_REVIEW"

HUMAN_DECISION = "ACCEPT_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_FOR_ONE_EXECUTION_REVIEW"
AUTHORIZED_FUTURE_UNIT = "EXECUTE_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

SOURCE_PREP_RECEIPT_ID = "c8_unit_feedback_hardening_bounded_probe_prep_receipt_d20aeb99"
SOURCE_PREP_PACKET_ID = "c8_unit_feedback_hardening_bounded_probe_prep_packet_591a64d9"
SOURCE_PREP_OPTIONS_ID = "c8_unit_feedback_hardening_bounded_probe_prep_options_7d79408e"
SOURCE_PREP_BOUNDARY_ID = "c8_unit_feedback_hardening_bounded_probe_prep_boundary_8f0ca352"

SOURCE_ACCEPTANCE_RECEIPT_ID = "c8_selected_successor_surface_acceptance_receipt_fcd108ad"
SOURCE_ACCEPTANCE_DECISION_ID = "c8_selected_successor_surface_acceptance_decision_a783ebb2"
SOURCE_ACCEPTANCE_PACKET_ID = "c8_selected_successor_surface_acceptance_packet_d40d679f"
SOURCE_BOUNDED_PROBE_PREP_AUTHORITY_ID = "c8_unit_feedback_hardening_bounded_probe_prep_authority_5bffc675"
SOURCE_ACCEPTANCE_BOUNDARY_ID = "c8_selected_successor_surface_acceptance_boundary_2eb5ac86"

SELECTED_SURFACE_ID = "c8_successor_surface_unit_feedback_hardening_after_runtime_adoption_closure_v0"
SELECTED_SURFACE_KIND = "UNIT_FEEDBACK_HARDENING_SURFACE"
SELECTED_SURFACE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_AFTER_RUNTIME_ADOPTION_CLOSURE_SURFACE"

PROBE_ID = "c8_unit_feedback_hardening_bounded_probe_after_runtime_adoption_closure_v0"
PROBE_KIND = "UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE"
PROBE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_AFTER_RUNTIME_ADOPTION_CLOSURE"
PROBE_QUESTION = (
    "Does the current C8 proceed/review chain expose useful diagnostic feedback for typed stops "
    "and failed units, beyond status alone: why it failed, where it failed, relative to what "
    "object/source surface/authority boundary/missing capability, and what exact refinement "
    "would allow lawful progress?"
)

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_after_runtime_adoption_closure_v0_receipts"

PREP_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_prep_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_bounded_probe_prep_receipt_d20aeb99.json"
PREP_PACKET = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_prep_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_prep_packet_v0.json"
PREP_OPTIONS = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_prep_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_prep_options_v0.json"
PREP_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_prep_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_prep_boundary_audit_v0.json"
PREP_REPORT = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_prep_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_prep_report.json"

ACCEPTANCE_DECISION = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_packet_v0.json"
EXECUTION_AUTHORITY = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_execution_authority_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_report.json"

FORBIDDEN_COUNTER_KEYS = [
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
        "prep_receipt": PREP_RECEIPT,
        "prep_packet": PREP_PACKET,
        "prep_options": PREP_OPTIONS,
        "prep_boundary": PREP_BOUNDARY,
        "prep_report": PREP_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    prep_receipt = read_json(PREP_RECEIPT)
    prep_packet = read_json(PREP_PACKET)
    prep_options = read_json(PREP_OPTIONS)
    prep_boundary = read_json(PREP_BOUNDARY)
    prep_report = read_json(PREP_REPORT)
    prep_summary = prep_receipt.get("machine_readable_unit_feedback_hardening_bounded_probe_prep_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_READY_FOR_REVIEW",
        "receipt_id": SOURCE_PREP_RECEIPT_ID,
    }
    for key, want in expected_receipt.items():
        chk(failures, f"prep_receipt_{key}", prep_receipt.get(key), want)

    expected_summary = {
        "unit_feedback_hardening_bounded_probe_prep_packet_created": True,
        "authorized_unit_consumed": "CREATE_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
        "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_bounded_probe_prep_authority_id": SOURCE_BOUNDED_PROBE_PREP_AUTHORITY_ID,
        "source_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "bounded_probe_execution_limit_if_later_accepted": 1,
        "probe_execution_requires_separate_human_acceptance": True,
        "bounded_probe_prep_packet_created_now": True,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized": False,
        "requires_review": True,
        "recommended_human_decision": HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": UNIT_ID,
        "next_command_goal": None,
    }
    for key, want in expected_summary.items():
        chk(failures, f"prep_summary_{key}", prep_summary.get(key), want)

    expected_prep_ids = {
        "prep_packet_id": (prep_packet.get("c8_unit_feedback_hardening_bounded_probe_prep_packet_id"), SOURCE_PREP_PACKET_ID),
        "prep_options_id": (prep_options.get("c8_unit_feedback_hardening_bounded_probe_prep_options_id"), SOURCE_PREP_OPTIONS_ID),
        "prep_boundary_id": (prep_boundary.get("c8_unit_feedback_hardening_bounded_probe_prep_boundary_audit_id"), SOURCE_PREP_BOUNDARY_ID),
    }
    for label, (got, want) in expected_prep_ids.items():
        if got != want:
            failures.append(f"{label}_wrong:{got}!={want}")

    if prep_options.get("recommended_human_decision") != HUMAN_DECISION:
        failures.append(f"prep_options_recommended_human_decision_wrong:{prep_options.get('recommended_human_decision')}")
    if prep_options.get("if_accepted_authorizes_future_unit") != UNIT_ID:
        failures.append(f"prep_options_future_unit_wrong:{prep_options.get('if_accepted_authorizes_future_unit')}")

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

    decision = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_decision_v0",
        "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_decision_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "human_decision": HUMAN_DECISION,
        "human_decision_consumed": True,
        "source_prep_receipt_id": SOURCE_PREP_RECEIPT_ID,
        "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
        "source_prep_options_id": SOURCE_PREP_OPTIONS_ID,
        "source_prep_boundary_id": SOURCE_PREP_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "bounded_probe_accepted_for_one_execution": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "bounded_probe_execution_limit": 1,
        "probe_execution_authorized_after_review": True,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "cell1_build_authorized_now": False,
        "verification_probe_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "missing_instrument_proposal_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "research_mode_opened": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
    }
    decision["c8_unit_feedback_hardening_bounded_probe_execution_acceptance_decision_id"] = "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_decision_" + sig8(decision)
    write_json(ACCEPTANCE_DECISION, decision)

    execution_authority = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_execution_authority_v0",
        "c8_unit_feedback_hardening_bounded_probe_execution_authority_id": None,
        "created_at": now_iso(),
        "source_execution_acceptance_decision_id": decision["c8_unit_feedback_hardening_bounded_probe_execution_acceptance_decision_id"],
        "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "execution_limit": 1,
        "authority_status": "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "authority_scope": {
            "may_execute_bounded_probe_once": True,
            "may_execute_more_than_once": False,
            "may_build_now": False,
            "may_rerun_c8_now": False,
            "may_promote_schema_now": False,
        },
    }
    execution_authority["c8_unit_feedback_hardening_bounded_probe_execution_authority_id"] = "c8_unit_feedback_hardening_bounded_probe_execution_authority_" + sig8(execution_authority)
    write_json(EXECUTION_AUTHORITY, execution_authority)

    packet = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_packet_v0",
        "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "acceptance_status": "BOUNDED_PROBE_ACCEPTED_FOR_ONE_EXECUTION_REVIEW",
        "human_decision": HUMAN_DECISION,
        "source_execution_acceptance_decision_id": decision["c8_unit_feedback_hardening_bounded_probe_execution_acceptance_decision_id"],
        "source_execution_authority_id": execution_authority["c8_unit_feedback_hardening_bounded_probe_execution_authority_id"],
        "source_prep_receipt_id": SOURCE_PREP_RECEIPT_ID,
        "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
        "source_prep_options_id": SOURCE_PREP_OPTIONS_ID,
        "source_prep_boundary_id": SOURCE_PREP_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "bounded_probe_accepted_for_one_execution": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "bounded_probe_execution_limit": 1,
        "probe_execution_authorized_after_review": True,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "cell1_build_authorized_now": False,
        "verification_probe_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "missing_instrument_proposal_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "research_mode_opened": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "requires_review": True,
        "recommended_review_unit": "REVIEW_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
    }
    packet["c8_unit_feedback_hardening_bounded_probe_execution_acceptance_packet_id"] = "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_packet_" + sig8(packet)
    write_json(ACCEPTANCE_PACKET, packet)

    boundary = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_boundary_audit_v0",
        "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_execution_acceptance_decision_id": decision["c8_unit_feedback_hardening_bounded_probe_execution_acceptance_decision_id"],
        "source_execution_acceptance_packet_id": packet["c8_unit_feedback_hardening_bounded_probe_execution_acceptance_packet_id"],
        "source_execution_authority_id": execution_authority["c8_unit_feedback_hardening_bounded_probe_execution_authority_id"],
        "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
        "allowed_now": {
            "accept_bounded_probe_for_one_execution_review": True,
            "authorize_one_execution_after_review_and_commit": True,
        },
        "not_allowed_now": {
            "execute_probe_now": True,
            "execute_more_than_once": True,
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
    boundary["c8_unit_feedback_hardening_bounded_probe_execution_acceptance_boundary_audit_id"] = "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_boundary_" + sig8(boundary)
    write_json(BOUNDARY_AUDIT, boundary)

    gate_results = {
        "EXECUTION_ACCEPTANCE_0_SOURCE_PREP_RECEIPT_PASS": prep_receipt.get("gate") == "PASS",
        "EXECUTION_ACCEPTANCE_1_HUMAN_DECISION_MATCH": prep_options.get("recommended_human_decision") == HUMAN_DECISION,
        "EXECUTION_ACCEPTANCE_2_FUTURE_UNIT_MATCH": prep_options.get("if_accepted_authorizes_future_unit") == UNIT_ID,
        "EXECUTION_ACCEPTANCE_3_PROBE_MATCH": prep_packet.get("probe_id") == PROBE_ID,
        "EXECUTION_ACCEPTANCE_4_ONE_EXECUTION_LIMIT": packet["bounded_probe_execution_limit"] == 1,
        "EXECUTION_ACCEPTANCE_5_EXECUTION_NOT_RUN_NOW": packet["probe_executed_now"] is False,
        "EXECUTION_ACCEPTANCE_6_NO_BUILD_RERUN_SCHEMA": packet["instrument_build_authorized_now"] is False and packet["c8_rerun_authorized_now"] is False and packet["reusable_schema_authorized_now"] is False,
        "EXECUTION_ACCEPTANCE_7_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "EXECUTION_ACCEPTANCE_8_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "EXECUTION_ACCEPTANCE_9_REQUIRES_REVIEW": packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"execution_acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_FAILED"

    readout = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_readout_v0",
        "title": "C8 unit-feedback hardening bounded probe execution acceptance after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "bounded_probe_accepted_for_one_execution": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "bounded_probe_execution_limit": 1,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": packet["recommended_review_unit"],
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "source_prep_receipt_id": SOURCE_PREP_RECEIPT_ID,
        "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
        "source_prep_options_id": SOURCE_PREP_OPTIONS_ID,
        "source_prep_boundary_id": SOURCE_PREP_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "bounded_probe_accepted_for_one_execution": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "bounded_probe_execution_limit": 1,
        "probe_execution_authorized_after_review": True,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "cell1_build_authorized_now": False,
        "verification_probe_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "missing_instrument_proposal_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "research_mode_opened": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "requires_review": True,
        "recommended_review_unit": packet["recommended_review_unit"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_bounded_probe_execution_acceptance_summary": {
            "unit_feedback_hardening_bounded_probe_execution_acceptance_complete": gate == "PASS",
            "human_decision": HUMAN_DECISION,
            "source_prep_receipt_id": SOURCE_PREP_RECEIPT_ID,
            "source_prep_packet_id": SOURCE_PREP_PACKET_ID,
            "source_prep_options_id": SOURCE_PREP_OPTIONS_ID,
            "source_prep_boundary_id": SOURCE_PREP_BOUNDARY_ID,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "probe_label": PROBE_LABEL,
            "bounded_probe_accepted_for_one_execution": True,
            "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
            "authorized_future_unit_count_after_review": 1,
            "bounded_probe_execution_limit": 1,
            "probe_execution_authorized_after_review": True,
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
            "recommended_review_unit": packet["recommended_review_unit"],
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
            "execution_acceptance_decision": rel(ACCEPTANCE_DECISION),
            "execution_acceptance_packet": rel(ACCEPTANCE_PACKET),
            "execution_authority": rel(EXECUTION_AUTHORITY),
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

    receipt["receipt_id"] = "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_bounded_probe_execution_acceptance_receipt_id={receipt['receipt_id']}")
    print(f"c8_unit_feedback_hardening_bounded_probe_execution_acceptance_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_execution_acceptance_decision_path={rel(ACCEPTANCE_DECISION)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_execution_acceptance_packet_path={rel(ACCEPTANCE_PACKET)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_execution_authority_path={rel(EXECUTION_AUTHORITY)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_execution_acceptance_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"human_decision={HUMAN_DECISION}")
    print(f"probe_id={PROBE_ID}")
    print(f"probe_kind={PROBE_KIND}")
    print("bounded_probe_accepted_for_one_execution=true")
    print(f"authorized_future_unit_after_review={AUTHORIZED_FUTURE_UNIT}")
    print("authorized_future_unit_count_after_review=1")
    print("bounded_probe_execution_limit=1")
    print("probe_execution_authorized_after_review=true")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={packet['recommended_review_unit']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
