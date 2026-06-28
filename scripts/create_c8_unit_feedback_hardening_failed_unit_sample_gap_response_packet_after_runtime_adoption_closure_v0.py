#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.failed_unit_sample_gap_response.packet.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_CREATED_AFTER_RUNTIME_ADOPTION_CLOSURE"
OUTCOME = "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_READY_FOR_REVIEW"
STOP_CODE = "STOP_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_READY_FOR_REVIEW"

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

OBSERVATION_CLASS = "UNIT_FEEDBACK_DIAGNOSTIC_FEEDBACK_PARTIAL_NO_FAILED_UNIT_SAMPLE_OBSERVED"
OBSERVATION_VERDICT = "PARTIAL"
DIAGNOSTIC_GAP = "No failed-unit sample was present in the bounded source set, so the probe can verify typed-stop/status/context/refinement structure but cannot fully validate failed-unit diagnostic quality."

RECOMMENDED_HUMAN_DECISION = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_FOR_DISCOVERY_PREP_REVIEW"
IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT = "CREATE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
RECOMMENDED_REVIEW_UNIT = "REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_after_runtime_adoption_closure_v0_receipts"

OBS_ACCEPTANCE_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_observation_acceptance_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_bounded_probe_observation_acceptance_receipt_3f4d0cb7.json"
OBS_ACCEPTANCE_DECISION = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_observation_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_observation_acceptance_decision_v0.json"
OBS_ACCEPTANCE_PACKET = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_observation_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_observation_acceptance_packet_v0.json"
GAP_AUTHORITY = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_observation_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_gap_response_authority_v0.json"
OBS_ACCEPTANCE_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_observation_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_observation_acceptance_boundary_audit_v0.json"
OBS_ACCEPTANCE_REPORT = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_observation_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_observation_acceptance_report.json"

GAP_RESPONSE_PACKET = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_gap_response_packet_v0.json"
GAP_RESPONSE_OPTIONS = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_gap_response_options_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_gap_response_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_gap_response_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_gap_response_report.json"

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
        "observation_acceptance_receipt": OBS_ACCEPTANCE_RECEIPT,
        "observation_acceptance_decision": OBS_ACCEPTANCE_DECISION,
        "observation_acceptance_packet": OBS_ACCEPTANCE_PACKET,
        "gap_response_authority": GAP_AUTHORITY,
        "observation_acceptance_boundary": OBS_ACCEPTANCE_BOUNDARY,
        "observation_acceptance_report": OBS_ACCEPTANCE_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in sources.items()
        if path.exists()
    }

    obs_receipt = read_json(OBS_ACCEPTANCE_RECEIPT)
    obs_decision = read_json(OBS_ACCEPTANCE_DECISION)
    obs_packet = read_json(OBS_ACCEPTANCE_PACKET)
    gap_authority = read_json(GAP_AUTHORITY)
    obs_boundary = read_json(OBS_ACCEPTANCE_BOUNDARY)
    obs_report = read_json(OBS_ACCEPTANCE_REPORT)
    obs_summary = obs_receipt.get("machine_readable_unit_feedback_hardening_bounded_probe_observation_acceptance_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_ACCEPTANCE_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_ACCEPTED_FOR_REVIEW",
        "receipt_id": SOURCE_OBSERVATION_ACCEPTANCE_RECEIPT_ID,
    }
    for key, want in expected_receipt.items():
        chk(failures, f"observation_acceptance_receipt_{key}", obs_receipt.get(key), want)

    expected_summary = {
        "observation_acceptance_complete": True,
        "human_decision": "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_FOR_REVIEW",
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
        "observation_accepted_for_review": True,
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
        "authorized_future_unit_after_review": UNIT_ID,
        "authorized_future_unit_count_after_review": 1,
        "gap_response_packet_created_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized": False,
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
        "recommended_review_unit": "REVIEW_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_ACCEPTANCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "next_command_goal": None,
    }
    for key, want in expected_summary.items():
        chk(failures, f"observation_acceptance_summary_{key}", obs_summary.get(key), want)

    expected_ids = {
        "observation_acceptance_decision_id": (
            obs_decision.get("c8_unit_feedback_hardening_bounded_probe_observation_acceptance_decision_id"),
            SOURCE_OBSERVATION_ACCEPTANCE_DECISION_ID,
        ),
        "observation_acceptance_packet_id": (
            obs_packet.get("c8_unit_feedback_hardening_bounded_probe_observation_acceptance_packet_id"),
            SOURCE_OBSERVATION_ACCEPTANCE_PACKET_ID,
        ),
        "gap_response_authority_id": (
            gap_authority.get("c8_unit_feedback_hardening_failed_unit_sample_gap_response_authority_id"),
            SOURCE_GAP_RESPONSE_AUTHORITY_ID,
        ),
        "observation_acceptance_boundary_id": (
            obs_boundary.get("c8_unit_feedback_hardening_bounded_probe_observation_acceptance_boundary_audit_id"),
            SOURCE_OBSERVATION_ACCEPTANCE_BOUNDARY_ID,
        ),
    }
    for label, (got, want) in expected_ids.items():
        if got != want:
            failures.append(f"{label}_wrong:{got}!={want}")

    if gap_authority.get("authorized_future_unit") != UNIT_ID:
        failures.append(f"gap_response_authority_future_unit_wrong:{gap_authority.get('authorized_future_unit')}")
    if gap_authority.get("authorized_future_unit_count") != 1:
        failures.append(f"gap_response_authority_count_wrong:{gap_authority.get('authorized_future_unit_count')}")
    if gap_authority.get("authority_status") != "ACTIVE_AFTER_REVIEW_AND_COMMIT":
        failures.append(f"gap_response_authority_status_wrong:{gap_authority.get('authority_status')}")

    authority_scope = gap_authority.get("authority_scope", {})
    expected_scope = {
        "may_create_failed_unit_sample_gap_response_packet": True,
        "may_authorize_probe_execution_now": False,
        "may_execute_probe_now": False,
        "may_build_now": False,
        "may_rerun_c8_now": False,
        "may_promote_schema_now": False,
    }
    for key, want in expected_scope.items():
        got = authority_scope.get(key)
        if got != want:
            failures.append(f"gap_response_authority_scope_{key}_wrong:{got}!={want}")

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

    gap_response_packet = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_gap_response_packet_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_gap_response_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "gap_response_status": "FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_READY_FOR_REVIEW",
        "authorized_unit_consumed": UNIT_ID,
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
        "gap_object": "FAILED_UNIT_SAMPLE_ABSENCE",
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
        "selected_gap_response_kind": "BOUNDED_FAILED_UNIT_SAMPLE_DISCOVERY_PREP",
        "gap_response_question": (
            "What is the smallest lawful next packet that can prepare bounded discovery of at least one failed-unit sample "
            "so failed-unit diagnostic quality can be tested, while preserving the existing partial observation and without "
            "authorizing discovery execution, probe execution, build, C8 rerun, or reusable schema promotion now?"
        ),
        "failed_unit_sample_requirements": {
            "must_have_failure_status": True,
            "acceptable_failure_indicators": [
                "gate == FAIL",
                "status suffix == _FAIL",
                "failures list non-empty",
                "gate_results contains false",
                "forbidden_counters contains nonzero value",
            ],
            "must_be_traceable_to_source_path": True,
            "must_expose_or_allow_checking": [
                "why it failed",
                "where it failed",
                "relative object/source surface/authority boundary/missing capability",
                "exact refinement or next lawful step",
                "distinction between failure status and useful feedback",
            ],
        },
        "gap_response_scope": {
            "allowed": [
                "preserve the partial observation as partial",
                "preserve failed_unit_sample_count == 0",
                "create a reviewed gap-response packet",
                "recommend a future failed-unit sample discovery prep packet",
                "define minimum requirements for a failed-unit sample",
            ],
            "forbidden": [
                "create failed-unit sample discovery prep packet now",
                "authorize sample discovery now",
                "execute sample discovery now",
                "authorize or execute another probe now",
                "build instrument or Cell 1 now",
                "rerun C8 now",
                "promote reusable schema now",
                "claim unit-feedback hardening complete",
            ],
        },
        "if_accepted_authorizes_future_unit": IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
        "gap_response_packet_created_now": True,
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
    }
    gap_response_packet["c8_unit_feedback_hardening_failed_unit_sample_gap_response_packet_id"] = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_packet_" + sig8(gap_response_packet)
    write_json(GAP_RESPONSE_PACKET, gap_response_packet)

    gap_response_options = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_gap_response_options_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_gap_response_options_id": None,
        "created_at": now_iso(),
        "source_gap_response_packet_id": gap_response_packet["c8_unit_feedback_hardening_failed_unit_sample_gap_response_packet_id"],
        "human_decision_options": [
            RECOMMENDED_HUMAN_DECISION,
            "REJECT_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE",
            "REQUEST_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_REVISION",
        ],
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT,
        "acceptance_notes": [
            "Acceptance should authorize only creation of a failed-unit sample discovery prep packet after review.",
            "Acceptance should not authorize sample discovery execution, probe execution, build, C8 rerun, or reusable schema promotion.",
        ],
    }
    gap_response_options["c8_unit_feedback_hardening_failed_unit_sample_gap_response_options_id"] = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_options_" + sig8(gap_response_options)
    write_json(GAP_RESPONSE_OPTIONS, gap_response_options)

    boundary = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_gap_response_boundary_audit_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_gap_response_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_gap_response_packet_id": gap_response_packet["c8_unit_feedback_hardening_failed_unit_sample_gap_response_packet_id"],
        "source_gap_response_options_id": gap_response_options["c8_unit_feedback_hardening_failed_unit_sample_gap_response_options_id"],
        "source_gap_response_authority_id": SOURCE_GAP_RESPONSE_AUTHORITY_ID,
        "authorized_unit_consumed": UNIT_ID,
        "allowed_now": {
            "create_failed_unit_sample_gap_response_packet": True,
            "present_gap_response_for_review": True,
        },
        "not_allowed_now": {
            "create_failed_unit_sample_discovery_prep_packet": True,
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
    boundary["c8_unit_feedback_hardening_failed_unit_sample_gap_response_boundary_audit_id"] = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_boundary_" + sig8(boundary)
    write_json(BOUNDARY_AUDIT, boundary)

    gate_results = {
        "GAP_RESPONSE_0_SOURCE_OBSERVATION_ACCEPTANCE_RECEIPT_PASS": obs_receipt.get("gate") == "PASS",
        "GAP_RESPONSE_1_AUTHORITY_PRESENT_AND_ACTIVE": gap_authority.get("authority_status") == "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "GAP_RESPONSE_2_AUTHORIZED_UNIT_MATCH": gap_authority.get("authorized_future_unit") == UNIT_ID,
        "GAP_RESPONSE_3_OBSERVATION_PARTIAL_PRESERVED": gap_response_packet["observation_class"] == OBSERVATION_CLASS and gap_response_packet["observation_verdict"] == OBSERVATION_VERDICT,
        "GAP_RESPONSE_4_FAILED_UNIT_SAMPLE_GAP_PRESERVED": gap_response_packet["failed_unit_sample_count"] == 0 and gap_response_packet["diagnostic_gap"] == DIAGNOSTIC_GAP,
        "GAP_RESPONSE_5_GAP_RESPONSE_PACKET_CREATED_ONCE": gap_response_packet["gap_response_packet_created_now"] is True,
        "GAP_RESPONSE_6_NO_DISCOVERY_PREP_PACKET_NOW": gap_response_packet["failed_unit_sample_discovery_prep_packet_created_now"] is False,
        "GAP_RESPONSE_7_NO_DISCOVERY_OR_PROBE_EXECUTION_NOW": gap_response_packet["sample_discovery_authorized_now"] is False and gap_response_packet["probe_execution_authorized_now"] is False and gap_response_packet["probe_executed_now"] is False,
        "GAP_RESPONSE_8_NO_BUILD_RERUN_SCHEMA": gap_response_packet["instrument_build_authorized_now"] is False and gap_response_packet["c8_rerun_authorized_now"] is False and gap_response_packet["reusable_schema_authorized_now"] is False,
        "GAP_RESPONSE_9_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "GAP_RESPONSE_10_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "GAP_RESPONSE_11_REQUIRES_REVIEW": gap_response_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"gap_response_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_FAILED"

    readout = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_gap_response_readout_v0",
        "title": "C8 unit-feedback hardening failed-unit sample gap-response packet after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "gap_object": "FAILED_UNIT_SAMPLE_ABSENCE",
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "failed_unit_sample_count": 0,
        "selected_gap_response_kind": "BOUNDED_FAILED_UNIT_SAMPLE_DISCOVERY_PREP",
        "gap_response_packet_created_now": True,
        "failed_unit_sample_discovery_prep_packet_created_now": False,
        "sample_discovery_authorized_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT,
        "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_gap_response_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_observation_acceptance_receipt_id": SOURCE_OBSERVATION_ACCEPTANCE_RECEIPT_ID,
        "source_gap_response_authority_id": SOURCE_GAP_RESPONSE_AUTHORITY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "observation_class": OBSERVATION_CLASS,
        "observation_verdict": OBSERVATION_VERDICT,
        "diagnostic_gap": DIAGNOSTIC_GAP,
        "failed_unit_sample_count": 0,
        "selected_gap_response_kind": "BOUNDED_FAILED_UNIT_SAMPLE_DISCOVERY_PREP",
        "gap_response_packet_created_now": True,
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
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT,
        "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_gap_response_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_PACKET_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_failed_unit_sample_gap_response_summary": {
            "failed_unit_sample_gap_response_packet_created": gate == "PASS",
            "authorized_unit_consumed": UNIT_ID,
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
            "gap_object": "FAILED_UNIT_SAMPLE_ABSENCE",
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
            "selected_gap_response_kind": "BOUNDED_FAILED_UNIT_SAMPLE_DISCOVERY_PREP",
            "gap_response_packet_created_now": True,
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
            "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
            "if_accepted_authorizes_future_unit": IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT,
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
            "gap_response_packet": rel(GAP_RESPONSE_PACKET),
            "gap_response_options": rel(GAP_RESPONSE_OPTIONS),
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

    receipt["receipt_id"] = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_failed_unit_sample_gap_response_receipt_id={receipt['receipt_id']}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_gap_response_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_gap_response_packet_path={rel(GAP_RESPONSE_PACKET)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_gap_response_options_path={rel(GAP_RESPONSE_OPTIONS)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_gap_response_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"gap_object=FAILED_UNIT_SAMPLE_ABSENCE")
    print(f"observation_class={OBSERVATION_CLASS}")
    print(f"observation_verdict={OBSERVATION_VERDICT}")
    print("failed_unit_sample_count=0")
    print("selected_gap_response_kind=BOUNDED_FAILED_UNIT_SAMPLE_DISCOVERY_PREP")
    print("gap_response_packet_created_now=true")
    print("failed_unit_sample_discovery_prep_packet_created_now=false")
    print("sample_discovery_authorized_now=false")
    print("sample_discovery_executed_now=false")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_human_decision={RECOMMENDED_HUMAN_DECISION}")
    print(f"if_accepted_authorizes_future_unit={IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT}")
    print(f"recommended_review_unit={RECOMMENDED_REVIEW_UNIT}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
