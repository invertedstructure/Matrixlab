#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.failed_unit_sample.discovery_prep.packet.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_CREATED_AFTER_RUNTIME_ADOPTION_CLOSURE"
OUTCOME = "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_READY_FOR_REVIEW"
STOP_CODE = "STOP_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_READY_FOR_REVIEW"

SOURCE_ACCEPTANCE_RECEIPT_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_receipt_a352ace8"
SOURCE_ACCEPTANCE_DECISION_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_decision_1d2f3b7c"
SOURCE_ACCEPTANCE_PACKET_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_packet_aa5a2900"
SOURCE_DISCOVERY_PREP_AUTHORITY_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_authority_d3369fc7"
SOURCE_ACCEPTANCE_BOUNDARY_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_boundary_18de4ed4"

SOURCE_GAP_RESPONSE_RECEIPT_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_receipt_78fa641a"
SOURCE_GAP_RESPONSE_PACKET_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_packet_109ffc4d"
SOURCE_GAP_RESPONSE_OPTIONS_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_options_0b2e001f"
SOURCE_GAP_RESPONSE_BOUNDARY_ID = "c8_unit_feedback_hardening_failed_unit_sample_gap_response_boundary_a299dd48"

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

RECOMMENDED_HUMAN_DECISION = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_FOR_ONE_BOUNDED_DISCOVERY_EXECUTION"
IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT = "EXECUTE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
RECOMMENDED_REVIEW_UNIT = "REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_after_runtime_adoption_closure_v0_receipts"

ACCEPTANCE_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_receipt_a352ace8.json"
ACCEPTANCE_DECISION = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_packet_v0.json"
DISCOVERY_PREP_AUTHORITY = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_authority_v0.json"
ACCEPTANCE_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_boundary_audit_v0.json"
ACCEPTANCE_REPORT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_report.json"

DISCOVERY_PREP_PACKET = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_packet_v0.json"
DISCOVERY_PREP_OPTIONS = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_options_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "failed_unit_sample_found_count",
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
        "acceptance_receipt": ACCEPTANCE_RECEIPT,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_packet": ACCEPTANCE_PACKET,
        "discovery_prep_authority": DISCOVERY_PREP_AUTHORITY,
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
    authority = read_json(DISCOVERY_PREP_AUTHORITY)
    acceptance_boundary = read_json(ACCEPTANCE_BOUNDARY)
    acceptance_report = read_json(ACCEPTANCE_REPORT)
    acceptance_summary = acceptance_receipt.get("machine_readable_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_summary", {})

    expected_acceptance_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_ACCEPTANCE_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_ACCEPTED_FOR_DISCOVERY_PREP_REVIEW",
        "receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
    }
    for key, want in expected_acceptance_receipt.items():
        chk(failures, f"acceptance_receipt_{key}", acceptance_receipt.get(key), want)

    expected_acceptance_summary = {
        "gap_response_acceptance_complete": True,
        "human_decision": "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_FOR_DISCOVERY_PREP_REVIEW",
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
        "authorized_future_unit_after_review": UNIT_ID,
        "authorized_future_unit_count_after_review": 1,
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
        "recommended_review_unit": "REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_GAP_RESPONSE_ACCEPTANCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "next_command_goal": None,
    }
    for key, want in expected_acceptance_summary.items():
        chk(failures, f"acceptance_summary_{key}", acceptance_summary.get(key), want)

    expected_ids = {
        "acceptance_decision_id": (
            acceptance_decision.get("c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_decision_id"),
            SOURCE_ACCEPTANCE_DECISION_ID,
        ),
        "acceptance_packet_id": (
            acceptance_packet.get("c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_packet_id"),
            SOURCE_ACCEPTANCE_PACKET_ID,
        ),
        "discovery_prep_authority_id": (
            authority.get("c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_authority_id"),
            SOURCE_DISCOVERY_PREP_AUTHORITY_ID,
        ),
        "acceptance_boundary_id": (
            acceptance_boundary.get("c8_unit_feedback_hardening_failed_unit_sample_gap_response_acceptance_boundary_audit_id"),
            SOURCE_ACCEPTANCE_BOUNDARY_ID,
        ),
    }
    for label, (got, want) in expected_ids.items():
        if got != want:
            failures.append(f"{label}_wrong:{got}!={want}")

    expected_authority = {
        "source_gap_response_packet_id": SOURCE_GAP_RESPONSE_PACKET_ID,
        "source_gap_response_receipt_id": SOURCE_GAP_RESPONSE_RECEIPT_ID,
        "gap_object": GAP_OBJECT,
        "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
        "authorized_future_unit": UNIT_ID,
        "authorized_future_unit_count": 1,
        "authority_status": "ACTIVE_AFTER_REVIEW_AND_COMMIT",
    }
    for key, want in expected_authority.items():
        chk(failures, f"authority_{key}", authority.get(key), want)

    authority_scope = authority.get("authority_scope", {})
    expected_scope = {
        "may_create_failed_unit_sample_discovery_prep_packet": True,
        "may_authorize_sample_discovery_now": False,
        "may_execute_sample_discovery_now": False,
        "may_authorize_probe_execution_now": False,
        "may_execute_probe_now": False,
        "may_build_now": False,
        "may_rerun_c8_now": False,
        "may_promote_schema_now": False,
    }
    for key, want in expected_scope.items():
        chk(failures, f"authority_scope_{key}", authority_scope.get(key), want)

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

    discovery_prep_packet = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_packet_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "discovery_prep_status": "FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_READY_FOR_REVIEW",
        "authorized_unit_consumed": UNIT_ID,
        "source_gap_response_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_gap_response_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
        "source_gap_response_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_discovery_prep_authority_id": SOURCE_DISCOVERY_PREP_AUTHORITY_ID,
        "source_gap_response_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
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
        "failed_unit_sample_count_before_discovery": 0,
        "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
        "discovery_target": "ONE_FAILED_UNIT_SAMPLE",
        "discovery_goal": (
            "Prepare one bounded discovery execution that may identify at most one failed-unit sample suitable for testing "
            "failed-unit diagnostic feedback quality."
        ),
        "bounded_discovery_question": (
            "Can the existing committed MatrixLab/C8 artifact surface expose one failed-unit sample with enough traceability "
            "to evaluate why it failed, where it failed, relative to what object/source surface/authority boundary/missing capability, "
            "and what exact refinement would allow lawful progress?"
        ),
        "candidate_source_surface_policy": {
            "search_existing_committed_artifacts_only": True,
            "may_inspect_receipts_reports_readouts_boundaries_and_runner_outputs": True,
            "may_create_synthetic_failure": False,
            "may_mutate_source_artifacts": False,
            "may_rerun_c8": False,
            "may_execute_probe": False,
        },
        "bounded_discovery_limits": {
            "max_failed_unit_samples_to_return": 1,
            "stop_after_first_qualified_failed_unit_sample": True,
            "require_source_path": True,
            "require_receipt_or_report_anchor": True,
        },
        "failed_unit_sample_qualification": {
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
            "not_sufficient_by_itself": [
                "mere stop code without failure context",
                "mere status flag without source path",
                "synthetic invented failure",
                "unanchored summary",
            ],
        },
        "future_execution_output_contract": {
            "if_sample_found": {
                "failed_unit_sample_found": True,
                "failed_unit_sample_count": 1,
                "must_emit_sample_id": True,
                "must_emit_source_path": True,
                "must_emit_failure_indicator": True,
                "must_emit_diagnostic_feedback_fields": [
                    "why",
                    "where",
                    "relative_to",
                    "refinement_or_next_lawful_step",
                    "failure_status_vs_useful_feedback_note",
                ],
            },
            "if_no_sample_found": {
                "failed_unit_sample_found": False,
                "failed_unit_sample_count": 0,
                "must_emit_typed_gap": "NO_FAILED_UNIT_SAMPLE_FOUND_IN_BOUNDED_DISCOVERY_SURFACE",
                "must_preserve_partial_observation": True,
            },
        },
        "discovery_prep_packet_created_now": True,
        "sample_discovery_authorized_now": False,
        "sample_discovery_executed_now": False,
        "failed_unit_sample_found_now": False,
        "failed_unit_sample_count_now": 0,
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
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
        "requires_review": True,
    }
    discovery_prep_packet["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_packet_id"] = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_packet_" + sig8(discovery_prep_packet)
    write_json(DISCOVERY_PREP_PACKET, discovery_prep_packet)

    discovery_prep_options = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_options_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_options_id": None,
        "created_at": now_iso(),
        "source_discovery_prep_packet_id": discovery_prep_packet["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_packet_id"],
        "human_decision_options": [
            RECOMMENDED_HUMAN_DECISION,
            "REJECT_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP",
            "REQUEST_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_REVISION",
        ],
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": IF_ACCEPTED_AUTHORIZES_FUTURE_UNIT,
        "acceptance_notes": [
            "Acceptance should authorize exactly one bounded discovery execution.",
            "Acceptance should not authorize build, C8 rerun, reusable schema promotion, or probe execution outside the stated discovery unit.",
        ],
    }
    discovery_prep_options["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_options_id"] = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_options_" + sig8(discovery_prep_options)
    write_json(DISCOVERY_PREP_OPTIONS, discovery_prep_options)

    boundary = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_boundary_audit_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_discovery_prep_packet_id": discovery_prep_packet["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_packet_id"],
        "source_discovery_prep_options_id": discovery_prep_options["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_options_id"],
        "source_discovery_prep_authority_id": SOURCE_DISCOVERY_PREP_AUTHORITY_ID,
        "authorized_unit_consumed": UNIT_ID,
        "allowed_now": {
            "create_failed_unit_sample_discovery_prep_packet": True,
            "present_discovery_prep_for_review": True,
        },
        "not_allowed_now": {
            "authorize_sample_discovery": True,
            "execute_sample_discovery": True,
            "claim_failed_unit_sample_found": True,
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
    boundary["c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_boundary_audit_id"] = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_boundary_" + sig8(boundary)
    write_json(BOUNDARY_AUDIT, boundary)

    gate_results = {
        "DISCOVERY_PREP_0_SOURCE_ACCEPTANCE_RECEIPT_PASS": acceptance_receipt.get("gate") == "PASS",
        "DISCOVERY_PREP_1_AUTHORITY_PRESENT_AND_ACTIVE": authority.get("authority_status") == "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "DISCOVERY_PREP_2_AUTHORIZED_UNIT_MATCH": authority.get("authorized_future_unit") == UNIT_ID,
        "DISCOVERY_PREP_3_GAP_OBJECT_PRESERVED": discovery_prep_packet["gap_object"] == GAP_OBJECT,
        "DISCOVERY_PREP_4_DISCOVERY_TARGET_ONE_SAMPLE": discovery_prep_packet["discovery_target"] == "ONE_FAILED_UNIT_SAMPLE",
        "DISCOVERY_PREP_5_PREP_PACKET_CREATED_NOW": discovery_prep_packet["discovery_prep_packet_created_now"] is True,
        "DISCOVERY_PREP_6_NO_DISCOVERY_NOW": discovery_prep_packet["sample_discovery_authorized_now"] is False and discovery_prep_packet["sample_discovery_executed_now"] is False,
        "DISCOVERY_PREP_7_NO_SAMPLE_FOUND_NOW": discovery_prep_packet["failed_unit_sample_found_now"] is False and discovery_prep_packet["failed_unit_sample_count_now"] == 0,
        "DISCOVERY_PREP_8_NO_PROBE_BUILD_RERUN_SCHEMA": discovery_prep_packet["probe_execution_authorized_now"] is False and discovery_prep_packet["instrument_build_authorized_now"] is False and discovery_prep_packet["c8_rerun_authorized_now"] is False and discovery_prep_packet["reusable_schema_authorized_now"] is False,
        "DISCOVERY_PREP_9_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "DISCOVERY_PREP_10_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "DISCOVERY_PREP_11_REQUIRES_REVIEW": discovery_prep_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"discovery_prep_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_FAILED"

    readout = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_readout_v0",
        "title": "C8 unit-feedback hardening failed-unit sample discovery-prep packet after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "gap_object": GAP_OBJECT,
        "discovery_target": "ONE_FAILED_UNIT_SAMPLE",
        "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
        "discovery_prep_packet_created_now": True,
        "sample_discovery_authorized_now": False,
        "sample_discovery_executed_now": False,
        "failed_unit_sample_found_now": False,
        "failed_unit_sample_count_now": 0,
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
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_gap_response_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_discovery_prep_authority_id": SOURCE_DISCOVERY_PREP_AUTHORITY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "gap_object": GAP_OBJECT,
        "discovery_target": "ONE_FAILED_UNIT_SAMPLE",
        "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
        "discovery_prep_packet_created_now": True,
        "sample_discovery_authorized_now": False,
        "sample_discovery_executed_now": False,
        "failed_unit_sample_found_now": False,
        "failed_unit_sample_count_now": 0,
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
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_PACKET_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_failed_unit_sample_discovery_prep_summary": {
            "failed_unit_sample_discovery_prep_packet_created": gate == "PASS",
            "authorized_unit_consumed": UNIT_ID,
            "source_gap_response_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
            "source_gap_response_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
            "source_gap_response_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
            "source_discovery_prep_authority_id": SOURCE_DISCOVERY_PREP_AUTHORITY_ID,
            "source_gap_response_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
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
            "failed_unit_sample_count_before_discovery": 0,
            "selected_gap_response_kind": SELECTED_GAP_RESPONSE_KIND,
            "discovery_target": "ONE_FAILED_UNIT_SAMPLE",
            "discovery_prep_packet_created_now": True,
            "sample_discovery_authorized_now": False,
            "sample_discovery_executed_now": False,
            "failed_unit_sample_found_now": False,
            "failed_unit_sample_count_now": 0,
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
            "authorized_future_unit_count_after_review": 1,
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
            "discovery_prep_packet": rel(DISCOVERY_PREP_PACKET),
            "discovery_prep_options": rel(DISCOVERY_PREP_OPTIONS),
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

    receipt["receipt_id"] = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_receipt_id={receipt['receipt_id']}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_packet_path={rel(DISCOVERY_PREP_PACKET)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_options_path={rel(DISCOVERY_PREP_OPTIONS)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"gap_object={GAP_OBJECT}")
    print("discovery_target=ONE_FAILED_UNIT_SAMPLE")
    print(f"selected_gap_response_kind={SELECTED_GAP_RESPONSE_KIND}")
    print("discovery_prep_packet_created_now=true")
    print("sample_discovery_authorized_now=false")
    print("sample_discovery_executed_now=false")
    print("failed_unit_sample_found_now=false")
    print("failed_unit_sample_count_now=0")
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
