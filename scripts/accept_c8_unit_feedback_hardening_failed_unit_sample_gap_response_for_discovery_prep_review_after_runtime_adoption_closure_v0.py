#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_FOR_DISCOVERY_PREP_REVIEW_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.failed_unit_sample_gap_response.acceptance.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_ACCEPTED_FOR_DISCOVERY_PREP_REVIEW_AFTER_RUNTIME_ADOPTION_CLOSURE"
OUTCOME = "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_ACCEPTED_FOR_DISCOVERY_PREP_REVIEW"
STOP_CODE = "STOP_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_ACCEPTANCE_READY_FOR_REVIEW"

HUMAN_DECISION = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_FOR_DISCOVERY_PREP_REVIEW"
AUTHORIZED_FUTURE_UNIT = "CREATE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
RECOMMENDED_REVIEW_UNIT = "REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_ACCEPTANCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

SOURCE_GAP_RESPONSE_RECEIPT_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_receipt_78fa641a"
SOURCE_GAP_RESPONSE_PACKET_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_packet_109ffc4d"
SOURCE_GAP_RESPONSE_OPTIONS_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_options_0b2e001f"
SOURCE_GAP_RESPONSE_BOUNDARY_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_boundary_a299dd48"

SOURCE_OBSERVATION_ACCEPTANCE_RECEIPT_ID = "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_receipt_3f4d0cb7"
SOURCE_OBSERVATION_ACCEPTANCE_DECISION_ID = "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_decision_5e0b37de"
SOURCE_OBSERVATION_ACCEPTANCE_PACKET_ID = "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_packet_abb2a707"
SOURCE_GAP_RESPONSE_AUTHORITY_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_authority_40205fb4"
SOURCE_OBSERVATION_ACCEPTANCE_BOUNDARY_ID = "c8_unit_feedback_hardening_bounded_probe_observation_acceptance_boundary_7cf14c9d"

SOURCE_EXECUTION_RECEIPT_ID = "c8_unit_feedback_hardening_bounded_probe_execution_receipt_b35662b1"
SOURCE_OBSERVATION_ID = "c8_unit_feedback_hardening_bounded_probe_observation_dd60017c"
SOURCE_INDEX_ID = "c8_unit_feedback_hardening_bounded_probe_source_index_53ccc16f"
SOURCE_EXECUTION_BOUNDARY_ID = "c8_unit_feedback_hardening_bounded_probe_execution_boundary_49533154"

SELECTED_SURFACE_ID = "c8_successor_surface_unit_feedback_hardening_after_runtime_adoption_closure_v0"
SELECTED_SURFACE_KIND = "UNIT_FEEDBACK_HARDENING_SURFACE"
SELECTED_SURFACE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_AFTER_RUNTIME_ADOPTION_CLOSURE_SURFACE"

PROBE_ID = "c8_unit_feedback_hardening_bounded_probe_after_runtime_adoption_closure_v0"
PROBE_KIND = "UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE"
PROBE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_AFTER_RUNTIME_ADOPTION_CLOSURE"

GAP_OBJECT = "FAILED_UNIT_SAMPLE_ABSENCE"
OBSERVATION_CLASS = "UNIT_FEEDBACK_DIAGNOSTIC_FEEDBACK_PARTIAL_NO_FAILED_UNIT_SAMPLE_OBSERVED"
OBSERVATION_VERDICT = "PARTIAL"
DIAGNOSTIC_GAP = "No failed-unit sample was present in the bounded source set, so the probe can verify typed-stop/status/context/refinement structure but cannot fully validate failed-unit diagnostic quality."
SELECTED_GAP_RESPONSE_KIND = "BOUNDED_FAILED_UNIT_SAMPLE_DISCOVERY_PREP"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_after_runtime_adoption_closure_v0_receipts"

GAP_RESPONSE_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_failed_unit_sample_gap_response_receipt_78fa641a.json"
GAP_RESPONSE_PACKET = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_gap_response_packet_v0.json"
GAP_RESPONSE_OPTIONS = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_gap_response_options_v0.json"
GAP_RESPONSE_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_gap_response_boundary_audit_v0.json"
GAP_RESPONSE_READOUT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_gap_response_readout_v0.json"
GAP_RESPONSE_REPORT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_gap_response_report.json"

ACCEPTANCE_DECISION = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_packet_v0.json"
DISCOVERY_PREP_AUTHORITY = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_authority_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "failed_unit_sample_discovery_prep_packet_created_count",
    "sample_discovery_authorized_count",
    "sample_discovery_executed_count",
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
        "gap_response_receipt": GAP_RESPONSE_RECEIPT,
        "gap_response_packet": GAP_RESPONSE_PACKET,
        "gap_response_options": GAP_RESPONSE_OPTIONS,
        "gap_response_boundary": GAP_RESPONSE_BOUNDARY,
        "gap_response_readout": GAP_RESPONSE_READOUT,
        "gap_response_report": GAP_RESPONSE_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    receipt = read_json(GAP_RESPONSE_RECEIPT)
    packet = read_json(GAP_RESPONSE_PACKET)
    options = read_json(GAP_RESPONSE_OPTIONS)
    boundary = read_json(GAP_RESPONSE_BOUNDARY)
    readout = read_json(GAP_RESPONSE_READOUT)
    report = read_json(GAP_RESPONSE_REPORT)
    summary = receipt.get("machine_readable_unit_feedback_hardening_failed_unit_sample_gap_response_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_READY_FOR_REVIEW",
        "receipt_id": SOURCE_GAP_RESPONSE_RECEIPT_ID,
    }
    for key, want in expected_receipt.items():
        chk(failures, f"gap_response_receipt_{key}", receipt.get(key), want)

    expected_summary = {
        "failed_unit_sample_gap_response_packet_created": True,
        "authorized_unit_consumed": "CREATE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "source_observation_acceptance_receipt_id": SOURCE_OBSERVATION_ACCEPTANCE_RECEIPT_ID,
        "source_observation_acceptance_decision_id": SOURCE_OBSERVATION_ACCEPTANCE_DECISION_ID,
        "source_observation_acceptance_packet_id": SOURCE_OBSERVATION_ACCEPTANCE_PACKET_ID,
        "source_gap_response_authority_id": SOURCE_GAP_RESPONSE_AUTHORITY_ID,
        "source_observation_acceptance_boundary_id": SOURCE_OBSERVATION_ACCEPTANCE_BOUNDARY_ID,
        "source_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
        "source_observation_id": SOURCE_OBSERVATION_ID,
        "source_index_id": SOURCE_INDEX_ID,
        "source_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "gap_object": GAP_OBJECT,
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "source_docs_count": 32,
        "typed_stop_sample_count": 5,
        "failed_unit_sample_count": 0,
        "why_signal_doc_count": 17,
        "where_signal_doc_count": 5,
        "relative_object_or_boundary_signal_doc_count": 31,
        "refinement_signal_doc_count": 27,
        "failure_status_distinction_signal_doc_count": 12,
        "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
        "gap_response_packet_created_now": True,
        "failed_unit_sample_discovery_prep_packet_created_now": False,
        "sample_discovery_authorized_now": False,
        "sample_discovery_executed_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized": False,
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
        "recommended_human_decision": HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": AUTHORIZED_FUTURE_UNIT,
        "recommended_review_unit": "REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "next_command_goal": None,
    }
    for key, want in expected_summary.items():
        chk(failures, f"gap_response_summary_{key}", summary.get(key), want)

    expected_ids = {
        "gap_response_packet_id": (
            packet.get("c8_unit_feedback_hardening_failed_unit_sample_gap_response_packet_id"),
            SOURCE_GAP_RESPONSE_PACKET_ID,
        ),
        "gap_response_options_id": (
            options.get("c8_unit_feedback_hardening_failed_unit_sample_gap_response_options_id"),
            SOURCE_GAP_RESPONSE_OPTIONS_ID,
        ),
        "gap_response_boundary_id": (
            boundary.get("c8_unit_feedback_hardening_failed_unit_sample_gap_response_boundary_audit_id"),
            SOURCE_GAP_RESPONSE_BOUNDARY_ID,
        ),
    }
    for label, (got, want) in expected_ids.items():
        if got != want:
            failures.append(f"{label}_wrong:{got}!={want}")

    for label, obj in [
        ("packet", packet),
        ("readout", readout),
        ("report", report),
    ]:
        chk(failures, f"{label}_gap_object", obj.get("gap_object"), GAP_OBJECT)
        chk(failures, f"{label}_selected_gap_response_kind", obj.get("selected_gap_response_kind"), SELECTED_GAP_RESPONSE_KIND)
        chk(failures, f"{label}_failed_unit_sample_count", obj.get("failed_unit_sample_count"), 0)

    if options.get("recommended_human_decision") != HUMAN_DECISION:
        failures.append(f"options_recommended_human_decision_wrong:{options.get('recommended_human_decision')}")
    if options.get("if_accepted_authorizes_future_unit") != AUTHORIZED_FUTURE_UNIT:
        failures.append(f"options_future_unit_wrong:{options.get('if_accepted_authorizes_future_unit')}")

    for required_option in [
        HUMAN_DECISION,
        "REJECT_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE",
        "REQUEST_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_REVISION",
    ]:
        if required_option not in options.get("human_decision_options", []):
            failures.append(f"human_decision_option_missing:{required_option}")

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
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_decision_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_decision_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "human_decision": HUMAN_DECISION,
        "human_decision_consumed": True,
        "source_gap_response_receipt_id": SOURCE_GAP_RESPONSE_RECEIPT_ID,
        "source_gap_response_packet_id": SOURCE_GAP_RESPONSE_PACKET_ID,
        "source_gap_response_options_id": SOURCE_GAP_RESPONSE_OPTIONS_ID,
        "source_gap_response_boundary_id": SOURCE_GAP_RESPONSE_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "gap_object": GAP_OBJECT,
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "failed_unit_sample_count": 0,
        "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
        "gap_response_accepted_for_discovery_prep_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "failed_unit_sample_discovery_prep_packet_created_now": False,
        "sample_discovery_authorized_now": False,
        "sample_discovery_executed_now": False,
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
    }
    decision["c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_decision_id"] = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_decision_" + sig8(decision)
    write_json(ACCEPTANCE_DECISION, decision)

    discovery_prep_authority = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_authority_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_authority_id": None,
        "created_at": now_iso(),
        "source_gap_response_acceptance_decision_id": decision["c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_decision_id"],
        "source_gap_response_packet_id": SOURCE_GAP_RESPONSE_PACKET_ID,
        "source_gap_response_receipt_id": SOURCE_GAP_RESPONSE_RECEIPT_ID,
        "gap_object": GAP_OBJECT,
        "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
        "authorized_future_unit": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authority_status": "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "authority_scope": {
            "may_create_failed_unit_sample_discovery_prep_packet": True,
            "may_authorize_sample_discovery_now": False,
            "may_execute_sample_discovery_now": False,
            "may_authorize_probe_execution_now": False,
            "may_execute_probe_now": False,
            "may_build_now": False,
            "may_rerun_c8_now": False,
            "may_promote_schema_now": False,
        },
    }
    discovery_prep_authority["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_authority_id"] = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_authority_" + sig8(discovery_prep_authority)
    write_json(DISCOVERY_PREP_AUTHORITY, discovery_prep_authority)

    acceptance_packet = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_packet_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "acceptance_status": "FAILED_UNIT_SAMPLE_GAP_RESPONSE_ACCEPTED_FOR_DISCOVERY_PREP_REVIEW",
        "human_decision": HUMAN_DECISION,
        "source_gap_response_acceptance_decision_id": decision["c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_decision_id"],
        "source_discovery_prep_authority_id": discovery_prep_authority["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_authority_id"],
        "source_gap_response_receipt_id": SOURCE_GAP_RESPONSE_RECEIPT_ID,
        "source_gap_response_packet_id": SOURCE_GAP_RESPONSE_PACKET_ID,
        "source_gap_response_options_id": SOURCE_GAP_RESPONSE_OPTIONS_ID,
        "source_gap_response_boundary_id": SOURCE_GAP_RESPONSE_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "gap_object": GAP_OBJECT,
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "failed_unit_sample_count": 0,
        "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
        "gap_response_accepted_for_discovery_prep_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "failed_unit_sample_discovery_prep_packet_created_now": False,
        "sample_discovery_authorized_now": False,
        "sample_discovery_executed_now": False,
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
        "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
    }
    acceptance_packet["c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_packet_id"] = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_packet_" + sig8(acceptance_packet)
    write_json(ACCEPTANCE_PACKET, acceptance_packet)

    boundary_audit = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_boundary_audit_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_gap_response_acceptance_decision_id": decision["c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_decision_id"],
        "source_gap_response_acceptance_packet_id": acceptance_packet["c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_packet_id"],
        "source_discovery_prep_authority_id": discovery_prep_authority["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_authority_id"],
        "source_gap_response_receipt_id": SOURCE_GAP_RESPONSE_RECEIPT_ID,
        "source_gap_response_packet_id": SOURCE_GAP_RESPONSE_PACKET_ID,
        "allowed_now": {
            "accept_gap_response_for_discovery_prep_review": True,
            "authorize_discovery_prep_packet_after_review_and_commit": True,
        },
        "not_allowed_now": {
            "create_failed_unit_sample_discovery_prep_packet_now": True,
            "authorize_sample_discovery": True,
            "execute_sample_discovery": True,
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
            "claim_unit_feedback_hardening_complete": True,
        },
        "forbidden_counters": forbidden_counters,
        "failures": failures,
        "warnings": warnings,
    }
    boundary_audit["c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_boundary_audit_id"] = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    gate_results = {
        "GAP_RESPONSE_ACCEPTANCE_0_SOURCE_RECEIPT_PASS": receipt.get("gate") == "PASS",
        "GAP_RESPONSE_ACCEPTANCE_1_HUMAN_DECISION_MATCH": summary.get("recommended_human_decision") == HUMAN_DECISION,
        "GAP_RESPONSE_ACCEPTANCE_2_FUTURE_UNIT_MATCH": summary.get("if_accepted_authorizes_future_unit") == AUTHORIZED_FUTURE_UNIT,
        "GAP_RESPONSE_ACCEPTANCE_3_GAP_OBJECT_PRESERVED": packet.get("gap_object") == GAP_OBJECT and report.get("gap_object") == GAP_OBJECT,
        "GAP_RESPONSE_ACCEPTANCE_4_GAP_RESPONSE_KIND_PRESERVED": packet.get("selected_gap_response_kind") == SELECTED_GAP_RESPONSE_KIND,
        "GAP_RESPONSE_ACCEPTANCE_5_DISCOVERY_PREP_PACKET_NOT_CREATED_NOW": acceptance_packet["failed_unit_sample_discovery_prep_packet_created_now"] is False,
        "GAP_RESPONSE_ACCEPTANCE_6_NO_DISCOVERY_OR_PROBE_EXECUTION_NOW": acceptance_packet["sample_discovery_authorized_now"] is False and acceptance_packet["sample_discovery_executed_now"] is False and acceptance_packet["probe_execution_authorized_now"] is False and acceptance_packet["probe_executed_now"] is False,
        "GAP_RESPONSE_ACCEPTANCE_7_NO_BUILD_RERUN_SCHEMA": acceptance_packet["instrument_build_authorized_now"] is False and acceptance_packet["c8_rerun_authorized_now"] is False and acceptance_packet["reusable_schema_authorized_now"] is False,
        "GAP_RESPONSE_ACCEPTANCE_8_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "GAP_RESPONSE_ACCEPTANCE_9_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "GAP_RESPONSE_ACCEPTANCE_10_REQUIRES_REVIEW": acceptance_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"gap_response_acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_ACCEPTANCE_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_ACCEPTANCE_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_ACCEPTANCE_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_ACCEPTANCE_FAILED"

    readout_obj = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_readout_v0",
        "title": "C8 unit-feedback hardening failed-unit sample gap-response acceptance after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "gap_response_accepted_for_discovery_prep_review": True,
        "gap_object": GAP_OBJECT,
        "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "failed_unit_sample_discovery_prep_packet_created_now": False,
        "sample_discovery_authorized_now": False,
        "sample_discovery_executed_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout_obj)

    report_obj = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "source_gap_response_receipt_id": SOURCE_GAP_RESPONSE_RECEIPT_ID,
        "source_gap_response_packet_id": SOURCE_GAP_RESPONSE_PACKET_ID,
        "source_gap_response_options_id": SOURCE_GAP_RESPONSE_OPTIONS_ID,
        "source_gap_response_boundary_id": SOURCE_GAP_RESPONSE_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "gap_object": GAP_OBJECT,
        "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
        "gap_response_accepted_for_discovery_prep_review": True,
        "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "failed_unit_sample_discovery_prep_packet_created_now": False,
        "sample_discovery_authorized_now": False,
        "sample_discovery_executed_now": False,
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
        "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report_obj)

    receipt_obj = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_ACCEPTANCE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_summary": {
            "gap_response_acceptance_complete": gate == "PASS",
            "human_decision": HUMAN_DECISION,
            "source_gap_response_receipt_id": SOURCE_GAP_RESPONSE_RECEIPT_ID,
            "source_gap_response_packet_id": SOURCE_GAP_RESPONSE_PACKET_ID,
            "source_gap_response_options_id": SOURCE_GAP_RESPONSE_OPTIONS_ID,
            "source_gap_response_boundary_id": SOURCE_GAP_RESPONSE_BOUNDARY_ID,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "probe_label": PROBE_LABEL,
            "gap_object": GAP_OBJECT,
            "observation_class": OBSERVATION_CLASS,
            "observation_verdict": OBSERVATION_VERDICT,
            "diagnostic_gap": DIAGNOSTIC_GAP,
            "failed_unit_sample_count": 0,
            "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
            "gap_response_accepted_for_discovery_prep_review": True,
            "authorized_future_unit_after_review": AUTHORIZED_FUTURE_UNIT,
            "authorized_future_unit_count_after_review": 1,
            "failed_unit_sample_discovery_prep_packet_created_now": False,
            "sample_discovery_authorized_now": False,
            "sample_discovery_executed_now": False,
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
            "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
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
            "gap_response_acceptance_decision": rel(ACCEPTANCE_DECISION),
            "gap_response_acceptance_packet": rel(ACCEPTANCE_PACKET),
            "discovery_prep_authority": rel(DISCOVERY_PREP_AUTHORITY),
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

    receipt_obj["receipt_id"] = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_receipt_" + sig8(receipt_obj)
    receipt_path = RECEIPT_DIR / f"{receipt_obj['receipt_id']}.json"
    receipt_obj["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_obj)

    print(json.dumps(receipt_obj, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_receipt_id={receipt_obj['receipt_id']}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_decision_path={rel(ACCEPTANCE_DECISION)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_packet_path={rel(ACCEPTANCE_PACKET)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_authority_path={rel(DISCOVERY_PREP_AUTHORITY)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"human_decision={HUMAN_DECISION}")
    print("gap_response_accepted_for_discovery_prep_review=true")
    print(f"gap_object={GAP_OBJECT}")
    print(f"selected_gap_response_kind={SELECTED_GAP_RESPONSE_KIND}")
    print(f"authorized_future_unit_after_review={AUTHORIZED_FUTURE_UNIT}")
    print("authorized_future_unit_count_after_review=1")
    print("failed_unit_sample_discovery_prep_packet_created_now=false")
    print("sample_discovery_authorized_now=false")
    print("sample_discovery_executed_now=false")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_review_unit={RECOMMENDED_REVIEW_UNIT}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
