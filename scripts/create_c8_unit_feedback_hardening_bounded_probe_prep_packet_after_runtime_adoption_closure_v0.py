#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.bounded_probe_prep_packet.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_CREATED_AFTER_RUNTIME_ADOPTION_CLOSURE"
OUTCOME = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_READY_FOR_REVIEW"
STOP_CODE = "STOP_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_READY_FOR_REVIEW"

AUTHORIZED_UNIT = UNIT_ID

SOURCE_ACCEPTANCE_RECEIPT_ID = "c8_selected_successor_surface_acceptance_receipt_fcd108ad"
SOURCE_ACCEPTANCE_DECISION_ID = "c8_selected_successor_surface_acceptance_decision_a783ebb2"
SOURCE_ACCEPTANCE_PACKET_ID = "c8_selected_successor_surface_acceptance_packet_d40d679f"
SOURCE_PREP_AUTHORITY_ID = "c8_unit_feedback_hardening_bounded_probe_prep_authority_5bffc675"
SOURCE_ACCEPTANCE_BOUNDARY_ID = "c8_selected_successor_surface_acceptance_boundary_2eb5ac86"

SOURCE_SELECTION_RECEIPT_ID = "c8_successor_surface_selection_receipt_5a63647b"
SOURCE_SELECTION_PACKET_ID = "c8_successor_surface_selection_packet_2168881d"
SOURCE_SELECTION_BOUNDARY_ID = "c8_successor_surface_selection_boundary_ca701b13"

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

RECOMMENDED_HUMAN_DECISION = "ACCEPT_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_FOR_ONE_EXECUTION_REVIEW"
IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_FOR_ONE_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_prep_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_prep_after_runtime_adoption_closure_v0_receipts"

ACCEPTANCE_RECEIPT = ROOT / "data/c8_selected_successor_surface_acceptance_after_runtime_adoption_closure_v0_receipts/c8_selected_successor_surface_acceptance_receipt_fcd108ad.json"
ACCEPTANCE_DECISION = ROOT / "data/c8_selected_successor_surface_acceptance_after_runtime_adoption_closure_v0/c8_selected_successor_surface_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = ROOT / "data/c8_selected_successor_surface_acceptance_after_runtime_adoption_closure_v0/c8_selected_successor_surface_acceptance_packet_v0.json"
PREP_AUTHORITY = ROOT / "data/c8_selected_successor_surface_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_prep_authority_v0.json"
ACCEPTANCE_BOUNDARY = ROOT / "data/c8_selected_successor_surface_acceptance_after_runtime_adoption_closure_v0/c8_selected_successor_surface_acceptance_boundary_audit_v0.json"
ACCEPTANCE_REPORT = ROOT / "data/c8_selected_successor_surface_acceptance_after_runtime_adoption_closure_v0/c8_selected_successor_surface_acceptance_report.json"

PREP_PACKET = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_prep_packet_v0.json"
PREP_OPTIONS = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_prep_options_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_prep_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_prep_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_prep_report.json"

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
        "prep_authority": PREP_AUTHORITY,
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
    prep_authority = read_json(PREP_AUTHORITY)
    acceptance_boundary = read_json(ACCEPTANCE_BOUNDARY)
    acceptance_report = read_json(ACCEPTANCE_REPORT)
    summary = acceptance_receipt.get("machine_readable_selected_successor_surface_acceptance_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_SELECTED_SUCCESSOR_SURFACE_ACCEPTANCE_PASS",
        "outcome_class": "C8_SELECTED_SUCCESSOR_SURFACE_ACCEPTED_FOR_BOUNDED_PROBE_PREP_REVIEW",
        "receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
    }
    for key, want in expected_receipt.items():
        chk(failures, f"acceptance_receipt_{key}", acceptance_receipt.get(key), want)

    expected_summary = {
        "selected_successor_surface_acceptance_complete": True,
        "human_decision": "ACCEPT_SELECTED_SUCCESSOR_SURFACE_FOR_BOUNDED_PROBE_PREP_REVIEW",
        "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
        "source_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
        "source_selection_boundary_id": SOURCE_SELECTION_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "selected_successor_surface_accepted_for_bounded_probe_prep_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "bounded_probe_prep_packet_created_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized": False,
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
    }
    for key, want in expected_summary.items():
        chk(failures, f"acceptance_summary_{key}", summary.get(key), want)

    expected_ids = {
        "decision_id": (acceptance_decision.get("c8_selected_successor_surface_acceptance_decision_id"), SOURCE_ACCEPTANCE_DECISION_ID),
        "packet_id": (acceptance_packet.get("c8_selected_successor_surface_acceptance_packet_id"), SOURCE_ACCEPTANCE_PACKET_ID),
        "prep_authority_id": (prep_authority.get("c8_unit_feedback_hardening_bounded_probe_prep_authority_id"), SOURCE_PREP_AUTHORITY_ID),
        "boundary_id": (acceptance_boundary.get("c8_selected_successor_surface_acceptance_boundary_audit_id"), SOURCE_ACCEPTANCE_BOUNDARY_ID),
    }
    for label, (got, want) in expected_ids.items():
        if got != want:
            failures.append(f"{label}_wrong:{got}!={want}")

    if prep_authority.get("authorized_future_unit") != AUTHORIZED_UNIT:
        failures.append(f"prep_authority_future_unit_wrong:{prep_authority.get('authorized_future_unit')}")
    if prep_authority.get("authorized_future_unit_count") != 1:
        failures.append(f"prep_authority_future_unit_count_wrong:{prep_authority.get('authorized_future_unit_count')}")
    if prep_authority.get("authority_status") != "ACTIVE_AFTER_REVIEW_AND_COMMIT":
        failures.append(f"prep_authority_status_wrong:{prep_authority.get('authority_status')}")

    scope = prep_authority.get("authority_scope", {})
    if scope.get("may_create_bounded_probe_prep_packet") is not True:
        failures.append("prep_authority_scope_may_create_bounded_probe_prep_packet_not_true")
    for forbidden_scope_key in [
        "may_authorize_probe_execution_now",
        "may_execute_probe_now",
        "may_build_now",
        "may_rerun_c8_now",
        "may_promote_schema_now",
    ]:
        if scope.get(forbidden_scope_key) is not False:
            failures.append(f"prep_authority_scope_{forbidden_scope_key}_wrong:{scope.get(forbidden_scope_key)}")

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

    prep_packet = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_prep_packet_v0",
        "c8_unit_feedback_hardening_bounded_probe_prep_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "prep_status": "BOUNDED_PROBE_PREP_PACKET_READY_FOR_REVIEW",
        "authorized_unit_consumed": AUTHORIZED_UNIT,
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
        "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_bounded_probe_prep_authority_id": SOURCE_PREP_AUTHORITY_ID,
        "source_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_question": PROBE_QUESTION,
        "probe_scope": {
            "allowed": [
                "inspect existing C8 proceed/review/commit receipts and readouts for diagnostic feedback shape",
                "classify whether typed stops or failed units explain why they failed",
                "classify whether typed stops or failed units identify where they failed",
                "classify whether typed stops or failed units identify the relevant object, source surface, authority boundary, or missing capability",
                "classify whether typed stops or failed units name the exact refinement that would allow progress",
                "preserve distinction between failure status and useful feedback",
            ],
            "forbidden": [
                "execute the probe now",
                "authorize probe execution now",
                "create or modify runtime machinery",
                "rerun C8",
                "promote any reusable schema",
                "claim global or frontier closure",
            ],
        },
        "bounded_probe_execution_limit_if_later_accepted": 1,
        "probe_execution_requires_separate_human_acceptance": True,
        "bounded_probe_prep_packet_created_now": True,
        "probe_execution_authorized_now": False,
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
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT,
        "recommended_review_unit": "REVIEW_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
    }
    prep_packet["c8_unit_feedback_hardening_bounded_probe_prep_packet_id"] = "c8_unit_feedback_hardening_bounded_probe_prep_packet_" + sig8(prep_packet)
    write_json(PREP_PACKET, prep_packet)

    prep_options = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_prep_options_v0",
        "c8_unit_feedback_hardening_bounded_probe_prep_options_id": None,
        "created_at": now_iso(),
        "source_prep_packet_id": prep_packet["c8_unit_feedback_hardening_bounded_probe_prep_packet_id"],
        "human_decision_options": [
            RECOMMENDED_HUMAN_DECISION,
            "REJECT_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP",
            "REQUEST_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_REVISION",
        ],
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT,
        "decision_boundary": {
            "accept_means": [
                "accept this bounded probe prep packet for later one-execution authorization review",
                "authorize a later acceptance unit that may authorize one bounded probe execution",
                "keep execution outside this prep packet",
            ],
            "accept_does_not_mean": [
                "execute the probe now",
                "authorize execution now",
                "build runtime machinery now",
                "rerun C8 now",
                "promote reusable schema now",
            ],
        },
    }
    prep_options["c8_unit_feedback_hardening_bounded_probe_prep_options_id"] = "c8_unit_feedback_hardening_bounded_probe_prep_options_" + sig8(prep_options)
    write_json(PREP_OPTIONS, prep_options)

    boundary_audit = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_prep_boundary_audit_v0",
        "c8_unit_feedback_hardening_bounded_probe_prep_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_prep_packet_id": prep_packet["c8_unit_feedback_hardening_bounded_probe_prep_packet_id"],
        "source_prep_options_id": prep_options["c8_unit_feedback_hardening_bounded_probe_prep_options_id"],
        "source_bounded_probe_prep_authority_id": SOURCE_PREP_AUTHORITY_ID,
        "authorized_unit_consumed": AUTHORIZED_UNIT,
        "allowed_now": {
            "create_bounded_probe_prep_packet": True,
            "present_probe_prep_for_review": True,
        },
        "not_allowed_now": {
            "accept_probe_prep": True,
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
    boundary_audit["c8_unit_feedback_hardening_bounded_probe_prep_boundary_audit_id"] = "c8_unit_feedback_hardening_bounded_probe_prep_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    gate_results = {
        "UNIT_FEEDBACK_PREP_0_SOURCE_ACCEPTANCE_RECEIPT_PASS": acceptance_receipt.get("gate") == "PASS",
        "UNIT_FEEDBACK_PREP_1_PREP_AUTHORITY_PRESENT_AND_ACTIVE": prep_authority.get("authority_status") == "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "UNIT_FEEDBACK_PREP_2_AUTHORIZED_UNIT_MATCH": prep_authority.get("authorized_future_unit") == AUTHORIZED_UNIT,
        "UNIT_FEEDBACK_PREP_3_SELECTED_SURFACE_MATCH": summary.get("selected_surface_id") == SELECTED_SURFACE_ID,
        "UNIT_FEEDBACK_PREP_4_PREP_PACKET_CREATED_ONCE": prep_packet["bounded_probe_prep_packet_created_now"] is True,
        "UNIT_FEEDBACK_PREP_5_NO_EXECUTION_AUTHORIZATION_NOW": prep_packet["probe_execution_authorized_now"] is False,
        "UNIT_FEEDBACK_PREP_6_NO_PROBE_EXECUTION_NOW": prep_packet["probe_executed_now"] is False,
        "UNIT_FEEDBACK_PREP_7_NO_BUILD_RERUN_SCHEMA": prep_packet["instrument_build_authorized_now"] is False and prep_packet["c8_rerun_authorized_now"] is False and prep_packet["reusable_schema_authorized_now"] is False,
        "UNIT_FEEDBACK_PREP_8_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "UNIT_FEEDBACK_PREP_9_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "UNIT_FEEDBACK_PREP_10_REQUIRES_REVIEW": prep_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"unit_feedback_prep_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_FAILED"

    readout = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_prep_readout_v0",
        "title": "C8 unit-feedback hardening bounded probe prep after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "bounded_probe_prep_packet_created_now": True,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "recommended_review_unit": prep_packet["recommended_review_unit"],
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_prep_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_bounded_probe_prep_authority_id": SOURCE_PREP_AUTHORITY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "bounded_probe_prep_packet_created_now": True,
        "probe_execution_authorized_now": False,
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
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT,
        "recommended_review_unit": prep_packet["recommended_review_unit"],
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_prep_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_PREP_PACKET_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_bounded_probe_prep_summary": {
            "unit_feedback_hardening_bounded_probe_prep_packet_created": gate == "PASS",
            "authorized_unit_consumed": AUTHORIZED_UNIT,
            "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
            "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
            "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
            "source_bounded_probe_prep_authority_id": SOURCE_PREP_AUTHORITY_ID,
            "source_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
            "source_selection_receipt_id": SOURCE_SELECTION_RECEIPT_ID,
            "source_selection_packet_id": SOURCE_SELECTION_PACKET_ID,
            "source_selection_boundary_id": SOURCE_SELECTION_BOUNDARY_ID,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "probe_label": PROBE_LABEL,
            "probe_question": PROBE_QUESTION,
            "bounded_probe_execution_limit_if_later_accepted": 1,
            "probe_execution_requires_separate_human_acceptance": True,
            "bounded_probe_prep_packet_created_now": True,
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
            "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
            "if_accepted_authorizes_future_unit": IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT,
            "recommended_review_unit": prep_packet["recommended_review_unit"],
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
            "prep_packet": rel(PREP_PACKET),
            "prep_options": rel(PREP_OPTIONS),
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

    receipt["receipt_id"] = "c8_unit_feedback_hardening_bounded_probe_prep_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_bounded_probe_prep_receipt_id={receipt['receipt_id']}")
    print(f"c8_unit_feedback_hardening_bounded_probe_prep_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_prep_packet_path={rel(PREP_PACKET)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_prep_options_path={rel(PREP_OPTIONS)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_prep_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"selected_surface_id={SELECTED_SURFACE_ID}")
    print(f"probe_id={PROBE_ID}")
    print(f"probe_kind={PROBE_KIND}")
    print("bounded_probe_prep_packet_created_now=true")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_human_decision={RECOMMENDED_HUMAN_DECISION}")
    print(f"if_accepted_authorizes_future_unit={IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT}")
    print(f"recommended_review_unit={prep_packet['recommended_review_unit']}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
