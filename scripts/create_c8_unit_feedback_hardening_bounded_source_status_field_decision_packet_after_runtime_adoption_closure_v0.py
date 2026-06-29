#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_STATUS_FIELD_DECISION_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.bounded_source_status_field_decision.packet.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_STATUS_FIELD_DECISION_PACKET_CREATED_AFTER_RUNTIME_ADOPTION_CLOSURE"

SOURCE_ACCEPTANCE_RECEIPT_ID = "c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_receipt_460dce66"
SOURCE_ACCEPTANCE_DECISION_ID = "c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_decision_3dbf6bf3"
SOURCE_ACCEPTANCE_PACKET_ID = "c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_packet_3e27fff9"
SOURCE_BOUNDED_DECISION_AUTHORITY_ID = "c8_unit_feedback_hardening_bounded_source_status_field_decision_authority_06f280f5"
SOURCE_ACCEPTANCE_BOUNDARY_ID = "c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_boundary_c8d440fa"

SOURCE_RESPONSE_RECEIPT_ID = "c8_unit_feedback_hardening_source_status_gap_response_packet_receipt_f2a5ee2a"
SOURCE_RESPONSE_PACKET_ID = "c8_unit_feedback_hardening_source_status_gap_response_packet_187fdf77"
SOURCE_RESPONSE_OPTIONS_ID = "c8_unit_feedback_hardening_source_status_gap_response_options_be3d12d9"
SOURCE_RESPONSE_BOUNDARY_ID = "c8_unit_feedback_hardening_source_status_gap_response_boundary_ba38ede6"

SOURCE_DECISION_PACKET_ACCEPTANCE_RECEIPT_ID = "c8_unit_feedback_hardening_decision_packet_acceptance_for_source_status_gap_response_receipt_0f04cacc"
SOURCE_DECISION_PACKET_ACCEPTANCE_DECISION_ID = "c8_unit_feedback_hardening_decision_packet_acceptance_for_source_status_gap_response_decision_7b8218ab"
SOURCE_DECISION_PACKET_ACCEPTANCE_PACKET_ID = "c8_unit_feedback_hardening_decision_packet_acceptance_for_source_status_gap_response_packet_f8e56829"
SOURCE_STATUS_GAP_RESPONSE_AUTHORITY_ID = "c8_unit_feedback_hardening_source_status_gap_response_authority_716573d0"
SOURCE_DECISION_PACKET_ACCEPTANCE_BOUNDARY_ID = "c8_unit_feedback_hardening_decision_packet_acceptance_for_source_status_gap_response_boundary_9ac0ca5d"

SOURCE_DECISION_RECEIPT_ID = "c8_unit_feedback_hardening_decision_packet_receipt_8565c071"
SOURCE_DECISION_PACKET_ID = "c8_unit_feedback_hardening_decision_packet_033976d2"
SOURCE_DECISION_OPTIONS_ID = "c8_unit_feedback_hardening_decision_options_54d847bd"
SOURCE_DECISION_BOUNDARY_ID = "c8_unit_feedback_hardening_decision_packet_boundary_5336d87a"

SOURCE_ASSESSMENT_RECEIPT_ID = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_receipt_2b262320"
SOURCE_ASSESSMENT_PACKET_ID = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_packet_4e6c1747"
SOURCE_ASSESSMENT_OPTIONS_ID = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_options_373a4f21"
SOURCE_ASSESSMENT_BOUNDARY_ID = "c8_unit_feedback_hardening_failed_unit_sample_diagnostic_assessment_boundary_987942ec"

SOURCE_DISCOVERY_RECEIPT_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_receipt_c9e0fb77"
SOURCE_DISCOVERY_RESULT_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_result_67360c26"
SOURCE_DISCOVERY_BOUNDARY_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_boundary_2ae0e55c"
SOURCE_DISCOVERY_AUTHORITY_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_authority_f06fa4a1"

SELECTED_SURFACE_ID = "c8_successor_surface_unit_feedback_hardening_after_runtime_adoption_closure_v0"
SELECTED_SURFACE_KIND = "UNIT_FEEDBACK_HARDENING_SURFACE"
SELECTED_SURFACE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_AFTER_RUNTIME_ADOPTION_CLOSURE_SURFACE"

PROBE_ID = "c8_unit_feedback_hardening_bounded_probe_after_runtime_adoption_closure_v0"
PROBE_KIND = "UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE"
PROBE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_AFTER_RUNTIME_ADOPTION_CLOSURE"

GAP_OBJECT = "FAILED_UNIT_SAMPLE_ABSENCE"
DISCOVERY_TARGET = "ONE_FAILED_UNIT_SAMPLE"
FAILED_UNIT_SAMPLE_ID = "c8_failed_unit_sample_ee4e6092"
FAILED_UNIT_SAMPLE_SOURCE_PATH = "data/a0_current_receipt_chain_frontier_application_v0_receipts/c1d0f615.json"
FAILED_UNIT_SAMPLE_SOURCE_STATUS = "MISSING_STATUS_FIELD_WITH_FAILURE_INDICATOR"

DIAGNOSTIC_ASSESSMENT_STATUS = "FAILED_UNIT_SAMPLE_DIAGNOSTIC_FEEDBACK_USEFUL_WITH_SOURCE_STATUS_GAP_EXPOSED"
FEEDBACK_HARDENING_DECISION_CLASS = "UNIT_FEEDBACK_HARDENING_DECISION_USEFUL_DIAGNOSTIC_FEEDBACK_WITH_LOCAL_SOURCE_STATUS_GAP"
LOCAL_GAP_OBJECT = "SOURCE_ARTIFACT_TOP_LEVEL_STATUS_ABSENCE"
SOURCE_STATUS_GAP_RESPONSE_CLASS = "SOURCE_STATUS_GAP_RESPONSE_PRESERVE_MISSING_STATUS_MARKER_AND_PREPARE_BOUNDED_STATUS_FIELD_DECISION"

BOUNDED_STATUS_FIELD_DECISION_CLASS = "BOUNDED_SOURCE_STATUS_FIELD_DECISION_CREATE_LOCAL_PATCH_PLAN_WITHOUT_SOURCE_MUTATION"
RECOMMENDED_HUMAN_DECISION = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_STATUS_FIELD_DECISION_PACKET_FOR_LOCAL_STATUS_FIELD_PATCH_PLAN"
FUTURE_UNIT = "CREATE_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
REVIEW_UNIT = "REVIEW_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_STATUS_FIELD_DECISION_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_after_runtime_adoption_closure_v0_receipts"

ACCEPTANCE_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_receipt_460dce66.json"
ACCEPTANCE_DECISION = ROOT / "data/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_decision_v0.json"
ACCEPTANCE_PACKET = ROOT / "data/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_packet_v0.json"
BOUNDED_DECISION_AUTHORITY = ROOT / "data/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_source_status_field_decision_authority_v0.json"
ACCEPTANCE_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_boundary_audit_v0.json"
ACCEPTANCE_READOUT = ROOT / "data/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_readout_v0.json"
ACCEPTANCE_REPORT = ROOT / "data/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_report.json"

DECISION_PACKET = OUT_DIR / "c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_v0.json"
OPTIONS = OUT_DIR / "c8_unit_feedback_hardening_bounded_source_status_field_decision_options_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_bounded_source_status_field_decision_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_bounded_source_status_field_decision_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_bounded_source_status_field_decision_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "local_source_status_field_patch_plan_packet_created_count",
    "source_artifact_mutation_count",
    "status_field_added_count",
    "source_status_invented_count",
    "reusable_schema_authorized_count",
    "additional_sample_discovery_count",
    "probe_execution_authorized_count",
    "probe_executed_count",
    "instrument_build_count",
    "cell1_build_count",
    "verification_probe_count",
    "c8_rerun_count",
    "missing_instrument_proposal_count",
    "research_mode_opened_count",
    "general_cell1_authority_count",
    "global_solution_claim_count",
    "frontier_solved_claim_count",
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
        "bounded_decision_authority": BOUNDED_DECISION_AUTHORITY,
        "acceptance_boundary": ACCEPTANCE_BOUNDARY,
        "acceptance_readout": ACCEPTANCE_READOUT,
        "acceptance_report": ACCEPTANCE_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {label: sha256_file(path) for label, path in sources.items() if path.exists()}

    receipt = read_json(ACCEPTANCE_RECEIPT)
    decision = read_json(ACCEPTANCE_DECISION)
    packet = read_json(ACCEPTANCE_PACKET)
    authority = read_json(BOUNDED_DECISION_AUTHORITY)
    boundary = read_json(ACCEPTANCE_BOUNDARY)
    summary = receipt.get("machine_readable_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_SOURCE_STATUS_GAP_RESPONSE_PACKET_ACCEPTANCE_FOR_BOUNDED_STATUS_FIELD_DECISION_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_SOURCE_STATUS_GAP_RESPONSE_PACKET_ACCEPTED_FOR_BOUNDED_STATUS_FIELD_DECISION",
        "receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
    }
    for key, want in expected_receipt.items():
        chk(failures, f"acceptance_receipt_{key}", receipt.get(key), want)

    expected_summary = {
        "source_status_gap_response_packet_acceptance_complete": True,
        "authorized_unit_consumed": "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_SOURCE_STATUS_GAP_RESPONSE_PACKET_FOR_BOUNDED_STATUS_FIELD_DECISION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "human_decision": "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_SOURCE_STATUS_GAP_RESPONSE_PACKET_FOR_BOUNDED_STATUS_FIELD_DECISION",
        "source_response_receipt_id": SOURCE_RESPONSE_RECEIPT_ID,
        "source_response_packet_id": SOURCE_RESPONSE_PACKET_ID,
        "source_response_options_id": SOURCE_RESPONSE_OPTIONS_ID,
        "source_response_boundary_id": SOURCE_RESPONSE_BOUNDARY_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_status": FAILED_UNIT_SAMPLE_SOURCE_STATUS,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "source_status_gap_response_class": SOURCE_STATUS_GAP_RESPONSE_CLASS,
        "source_status_gap_response_packet_accepted_for_bounded_status_field_decision": True,
        "authorized_future_unit_after_review": UNIT_ID,
        "authorized_future_unit_count_after_review": 1,
        "bounded_source_status_field_decision_packet_created_now": False,
        "source_artifact_mutated_now": False,
        "source_status_invented_now": False,
        "status_field_added_now": False,
        "additional_sample_discovery_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized": False,
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
    }
    for key, want in expected_summary.items():
        chk(failures, f"acceptance_summary_{key}", summary.get(key), want)

    chk(failures, "acceptance_decision_id", decision.get("c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_decision_id"), SOURCE_ACCEPTANCE_DECISION_ID)
    chk(failures, "acceptance_packet_id", packet.get("c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_packet_id"), SOURCE_ACCEPTANCE_PACKET_ID)
    chk(failures, "acceptance_boundary_id", boundary.get("c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_boundary_audit_id"), SOURCE_ACCEPTANCE_BOUNDARY_ID)

    chk(failures, "bounded_decision_authority_id", authority.get("c8_unit_feedback_hardening_bounded_source_status_field_decision_authority_id"), SOURCE_BOUNDED_DECISION_AUTHORITY_ID)
    chk(failures, "authority_authorized_future_unit", authority.get("authorized_future_unit"), UNIT_ID)
    chk(failures, "authority_authorized_future_unit_count", authority.get("authorized_future_unit_count"), 1)
    chk(failures, "authority_status", authority.get("authority_status"), "ACTIVE_AFTER_REVIEW_AND_COMMIT")

    scope = authority.get("authority_scope", {})
    chk(failures, "scope_may_create_one_bounded_source_status_field_decision_packet", scope.get("may_create_one_bounded_source_status_field_decision_packet"), True)
    chk(failures, "scope_may_create_bounded_source_status_field_decision_packet_now", scope.get("may_create_bounded_source_status_field_decision_packet_now"), False)
    chk(failures, "scope_may_mutate_source_artifact", scope.get("may_mutate_source_artifact"), False)
    chk(failures, "scope_may_invent_source_status", scope.get("may_invent_source_status"), False)
    chk(failures, "scope_may_add_status_field_now", scope.get("may_add_status_field_now"), False)
    chk(failures, "scope_may_promote_schema_now", scope.get("may_promote_schema_now"), False)

    decision_packet = {
        "schema_version": "c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_v0",
        "c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
        "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_bounded_source_status_field_decision_authority_id": SOURCE_BOUNDED_DECISION_AUTHORITY_ID,
        "source_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
        "source_response_receipt_id": SOURCE_RESPONSE_RECEIPT_ID,
        "source_response_packet_id": SOURCE_RESPONSE_PACKET_ID,
        "source_response_options_id": SOURCE_RESPONSE_OPTIONS_ID,
        "source_response_boundary_id": SOURCE_RESPONSE_BOUNDARY_ID,
        "source_decision_packet_acceptance_receipt_id": SOURCE_DECISION_PACKET_ACCEPTANCE_RECEIPT_ID,
        "source_decision_packet_acceptance_decision_id": SOURCE_DECISION_PACKET_ACCEPTANCE_DECISION_ID,
        "source_decision_packet_acceptance_packet_id": SOURCE_DECISION_PACKET_ACCEPTANCE_PACKET_ID,
        "source_status_gap_response_authority_id": SOURCE_STATUS_GAP_RESPONSE_AUTHORITY_ID,
        "source_decision_packet_acceptance_boundary_id": SOURCE_DECISION_PACKET_ACCEPTANCE_BOUNDARY_ID,
        "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "source_decision_packet_id": SOURCE_DECISION_PACKET_ID,
        "source_decision_options_id": SOURCE_DECISION_OPTIONS_ID,
        "source_decision_boundary_id": SOURCE_DECISION_BOUNDARY_ID,
        "source_diagnostic_assessment_receipt_id": SOURCE_ASSESSMENT_RECEIPT_ID,
        "source_diagnostic_assessment_packet_id": SOURCE_ASSESSMENT_PACKET_ID,
        "source_diagnostic_assessment_options_id": SOURCE_ASSESSMENT_OPTIONS_ID,
        "source_diagnostic_assessment_boundary_id": SOURCE_ASSESSMENT_BOUNDARY_ID,
        "source_discovery_execution_receipt_id": SOURCE_DISCOVERY_RECEIPT_ID,
        "source_discovery_result_id": SOURCE_DISCOVERY_RESULT_ID,
        "source_discovery_boundary_id": SOURCE_DISCOVERY_BOUNDARY_ID,
        "source_discovery_execution_authority_id": SOURCE_DISCOVERY_AUTHORITY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "gap_object": GAP_OBJECT,
        "discovery_target": DISCOVERY_TARGET,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "failed_unit_sample_source_status": FAILED_UNIT_SAMPLE_SOURCE_STATUS,
        "diagnostic_assessment_status": DIAGNOSTIC_ASSESSMENT_STATUS,
        "feedback_hardening_decision_class": FEEDBACK_HARDENING_DECISION_CLASS,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "source_status_gap_response_class": SOURCE_STATUS_GAP_RESPONSE_CLASS,
        "bounded_source_status_field_decision_class": BOUNDED_STATUS_FIELD_DECISION_CLASS,
        "decision_read": (
            "The bounded decision is to keep the discovered source-status absence explicit, "
            "not to invent a status for the old source artifact, and not to promote a reusable schema here."
        ),
        "decision_consequence": (
            "If accepted, authorize one local source-status field patch-plan packet that can specify the exact bounded patch route. "
            "This packet itself does not mutate any source artifact and does not add a status field."
        ),
        "bounded_source_status_field_decision_packet_created_now": True,
        "local_source_status_field_patch_plan_packet_created_now": False,
        "source_artifact_mutated_now": False,
        "source_status_invented_now": False,
        "status_field_added_now": False,
        "reusable_schema_authorized_now": False,
        "additional_sample_discovery_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "cell1_build_authorized_now": False,
        "verification_probe_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "missing_instrument_proposal_authorized_now": False,
        "research_mode_opened": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "requires_review": True,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "recommended_review_unit": REVIEW_UNIT,
    }
    decision_packet["c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_id"] = "c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_" + sig8(decision_packet)
    write_json(DECISION_PACKET, decision_packet)

    options = {
        "schema_version": "c8_unit_feedback_hardening_bounded_source_status_field_decision_options_v0",
        "c8_unit_feedback_hardening_bounded_source_status_field_decision_options_id": None,
        "created_at": now_iso(),
        "source_bounded_source_status_field_decision_packet_id": decision_packet["c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_id"],
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "human_decision_options": [
            RECOMMENDED_HUMAN_DECISION,
            "REJECT_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_STATUS_FIELD_DECISION_PACKET",
            "REQUEST_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_STATUS_FIELD_DECISION_PACKET_REVISION",
        ],
    }
    options["c8_unit_feedback_hardening_bounded_source_status_field_decision_options_id"] = "c8_unit_feedback_hardening_bounded_source_status_field_decision_options_" + sig8(options)
    write_json(OPTIONS, options)

    boundary_audit = {
        "schema_version": "c8_unit_feedback_hardening_bounded_source_status_field_decision_boundary_audit_v0",
        "c8_unit_feedback_hardening_bounded_source_status_field_decision_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_bounded_source_status_field_decision_packet_id": decision_packet["c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_id"],
        "source_bounded_source_status_field_decision_options_id": options["c8_unit_feedback_hardening_bounded_source_status_field_decision_options_id"],
        "source_bounded_source_status_field_decision_authority_id": SOURCE_BOUNDED_DECISION_AUTHORITY_ID,
        "allowed_now": {
            "create_one_bounded_source_status_field_decision_packet": True,
            "emit_bounded_source_status_field_decision_for_review": True,
        },
        "not_allowed_now": {
            "create_local_source_status_field_patch_plan_packet_now": True,
            "mutate_source_artifact": True,
            "invent_source_status": True,
            "add_status_field_now": True,
            "authorize_reusable_schema": True,
            "execute_additional_sample_discovery": True,
            "authorize_probe_execution": True,
            "execute_probe": True,
            "build_instrument": True,
            "build_cell1": True,
            "run_verification_probe": True,
            "rerun_c8": True,
            "create_missing_instrument_proposal": True,
            "open_research_mode": True,
            "claim_global_solution": True,
            "claim_frontier_solved": True,
            "claim_unit_feedback_hardening_complete": True,
        },
        "forbidden_counters": forbidden_counters,
        "failures": failures,
        "warnings": warnings,
    }
    boundary_audit["c8_unit_feedback_hardening_bounded_source_status_field_decision_boundary_audit_id"] = "c8_unit_feedback_hardening_bounded_source_status_field_decision_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    source_hashes_after = {label: sha256_file(path) for label, path in sources.items() if path.exists()}
    if source_hashes_before != source_hashes_after:
        forbidden_counters["source_artifact_mutation_count"] += 1
        failures.append("source_artifact_mutation_count:1")

    gate_results = {
        "BOUNDED_SOURCE_STATUS_FIELD_DECISION_0_SOURCE_ACCEPTANCE_RECEIPT_PASS": receipt.get("gate") == "PASS",
        "BOUNDED_SOURCE_STATUS_FIELD_DECISION_1_AUTHORITY_PRESENT_AND_ACTIVE": authority.get("authority_status") == "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "BOUNDED_SOURCE_STATUS_FIELD_DECISION_2_AUTHORIZED_UNIT_MATCH": authority.get("authorized_future_unit") == UNIT_ID,
        "BOUNDED_SOURCE_STATUS_FIELD_DECISION_3_ONE_DECISION_PACKET_CREATED": decision_packet["bounded_source_status_field_decision_packet_created_now"] is True,
        "BOUNDED_SOURCE_STATUS_FIELD_DECISION_4_PATCH_PLAN_NOT_CREATED_NOW": decision_packet["local_source_status_field_patch_plan_packet_created_now"] is False,
        "BOUNDED_SOURCE_STATUS_FIELD_DECISION_5_NO_SOURCE_MUTATION_STATUS_INVENTION_OR_FIELD_ADDITION": decision_packet["source_artifact_mutated_now"] is False and decision_packet["source_status_invented_now"] is False and decision_packet["status_field_added_now"] is False,
        "BOUNDED_SOURCE_STATUS_FIELD_DECISION_6_NO_SCHEMA_DISCOVERY_PROBE_BUILD_RERUN": decision_packet["reusable_schema_authorized_now"] is False and decision_packet["additional_sample_discovery_now"] is False and decision_packet["probe_execution_authorized_now"] is False and decision_packet["instrument_build_authorized_now"] is False and decision_packet["c8_rerun_authorized_now"] is False,
        "BOUNDED_SOURCE_STATUS_FIELD_DECISION_7_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "BOUNDED_SOURCE_STATUS_FIELD_DECISION_8_FORBIDDEN_COUNTERS_ZERO": all(v == 0 for v in forbidden_counters.values()),
        "BOUNDED_SOURCE_STATUS_FIELD_DECISION_9_REQUIRES_REVIEW": decision_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"bounded_source_status_field_decision_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_STATUS_FIELD_DECISION_PACKET_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_STATUS_FIELD_DECISION_PACKET_FAIL"
    outcome = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_STATUS_FIELD_DECISION_PACKET_READY_FOR_REVIEW" if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_STATUS_FIELD_DECISION_PACKET_FAILED"
    terminal_stop = "STOP_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_STATUS_FIELD_DECISION_PACKET_READY_FOR_REVIEW" if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_STATUS_FIELD_DECISION_PACKET_FAILED"

    readout = {
        "schema_version": "c8_unit_feedback_hardening_bounded_source_status_field_decision_readout_v0",
        "title": "C8 bounded source-status field decision packet",
        "status": status,
        "outcome_class": outcome,
        "bounded_source_status_field_decision_class": BOUNDED_STATUS_FIELD_DECISION_CLASS,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "bounded_source_status_field_decision_packet_created_now": True,
        "local_source_status_field_patch_plan_packet_created_now": False,
        "source_artifact_mutated_now": False,
        "source_status_invented_now": False,
        "status_field_added_now": False,
        "reusable_schema_authorized_now": False,
        "additional_sample_discovery_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "requires_review": True,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "recommended_review_unit": REVIEW_UNIT,
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report_obj = {
        "schema_version": "c8_unit_feedback_hardening_bounded_source_status_field_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_bounded_source_status_field_decision_authority_id": SOURCE_BOUNDED_DECISION_AUTHORITY_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "bounded_source_status_field_decision_class": BOUNDED_STATUS_FIELD_DECISION_CLASS,
        "bounded_source_status_field_decision_packet_created_now": True,
        "local_source_status_field_patch_plan_packet_created_now": False,
        "source_artifact_mutated_now": False,
        "source_status_invented_now": False,
        "status_field_added_now": False,
        "reusable_schema_authorized_now": False,
        "additional_sample_discovery_now": False,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "cell1_build_authorized_now": False,
        "verification_probe_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "missing_instrument_proposal_authorized_now": False,
        "research_mode_opened": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "requires_review": True,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "recommended_review_unit": REVIEW_UNIT,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report_obj)

    receipt_obj = {
        "schema_version": "c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_SOURCE_STATUS_FIELD_DECISION_PACKET_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_bounded_source_status_field_decision_packet_summary": {
            "bounded_source_status_field_decision_packet_created": gate == "PASS",
            "authorized_unit_consumed": UNIT_ID,
            "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
            "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
            "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
            "source_bounded_source_status_field_decision_authority_id": SOURCE_BOUNDED_DECISION_AUTHORITY_ID,
            "source_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
            "source_response_receipt_id": SOURCE_RESPONSE_RECEIPT_ID,
            "source_response_packet_id": SOURCE_RESPONSE_PACKET_ID,
            "source_response_options_id": SOURCE_RESPONSE_OPTIONS_ID,
            "source_response_boundary_id": SOURCE_RESPONSE_BOUNDARY_ID,
            "source_decision_packet_acceptance_receipt_id": SOURCE_DECISION_PACKET_ACCEPTANCE_RECEIPT_ID,
            "source_decision_packet_acceptance_decision_id": SOURCE_DECISION_PACKET_ACCEPTANCE_DECISION_ID,
            "source_decision_packet_acceptance_packet_id": SOURCE_DECISION_PACKET_ACCEPTANCE_PACKET_ID,
            "source_status_gap_response_authority_id": SOURCE_STATUS_GAP_RESPONSE_AUTHORITY_ID,
            "source_decision_packet_acceptance_boundary_id": SOURCE_DECISION_PACKET_ACCEPTANCE_BOUNDARY_ID,
            "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
            "source_decision_packet_id": SOURCE_DECISION_PACKET_ID,
            "source_decision_options_id": SOURCE_DECISION_OPTIONS_ID,
            "source_decision_boundary_id": SOURCE_DECISION_BOUNDARY_ID,
            "source_diagnostic_assessment_receipt_id": SOURCE_ASSESSMENT_RECEIPT_ID,
            "source_diagnostic_assessment_packet_id": SOURCE_ASSESSMENT_PACKET_ID,
            "source_diagnostic_assessment_options_id": SOURCE_ASSESSMENT_OPTIONS_ID,
            "source_diagnostic_assessment_boundary_id": SOURCE_ASSESSMENT_BOUNDARY_ID,
            "source_discovery_execution_receipt_id": SOURCE_DISCOVERY_RECEIPT_ID,
            "source_discovery_result_id": SOURCE_DISCOVERY_RESULT_ID,
            "source_discovery_boundary_id": SOURCE_DISCOVERY_BOUNDARY_ID,
            "source_discovery_execution_authority_id": SOURCE_DISCOVERY_AUTHORITY_ID,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "probe_label": PROBE_LABEL,
            "gap_object": GAP_OBJECT,
            "discovery_target": DISCOVERY_TARGET,
            "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
            "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
            "failed_unit_sample_source_status": FAILED_UNIT_SAMPLE_SOURCE_STATUS,
            "diagnostic_assessment_status": DIAGNOSTIC_ASSESSMENT_STATUS,
            "feedback_hardening_decision_class": FEEDBACK_HARDENING_DECISION_CLASS,
            "local_gap_object": LOCAL_GAP_OBJECT,
            "source_status_gap_response_class": SOURCE_STATUS_GAP_RESPONSE_CLASS,
            "bounded_source_status_field_decision_class": BOUNDED_STATUS_FIELD_DECISION_CLASS,
            "bounded_source_status_field_decision_packet_created_now": True,
            "local_source_status_field_patch_plan_packet_created_now": False,
            "source_artifact_mutated_now": False,
            "source_status_invented_now": False,
            "status_field_added_now": False,
            "reusable_schema_authorized": False,
            "additional_sample_discovery_now": False,
            "probe_execution_authorized_now": False,
            "probe_executed_now": False,
            "instrument_built_now": False,
            "cell1_built_now": False,
            "verification_probe_run_now": False,
            "c8_rerun_now": False,
            "missing_instrument_proposal_created_now": False,
            "research_mode_opened": False,
            "general_cell1_authority": False,
            "global_solution_claim": False,
            "frontier_solved_claim": False,
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
            "forbidden_counters_zero": all(v == 0 for v in forbidden_counters.values()),
            "requires_review": True,
            "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
            "if_accepted_authorizes_future_unit": FUTURE_UNIT,
            "authorized_future_unit_count_after_review": 1,
            "recommended_review_unit": REVIEW_UNIT,
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
            "bounded_source_status_field_decision_packet": rel(DECISION_PACKET),
            "bounded_source_status_field_decision_options": rel(OPTIONS),
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

    receipt_obj["receipt_id"] = "c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_receipt_" + sig8(receipt_obj)
    receipt_path = RECEIPT_DIR / f"{receipt_obj['receipt_id']}.json"
    receipt_obj["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_obj)

    print(json.dumps(receipt_obj, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_receipt_id={receipt_obj['receipt_id']}")
    print(f"c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_path={rel(DECISION_PACKET)}")
    print(f"c8_unit_feedback_hardening_bounded_source_status_field_decision_options_path={rel(OPTIONS)}")
    print(f"c8_unit_feedback_hardening_bounded_source_status_field_decision_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"failed_unit_sample_id={FAILED_UNIT_SAMPLE_ID}")
    print(f"local_gap_object={LOCAL_GAP_OBJECT}")
    print(f"bounded_source_status_field_decision_class={BOUNDED_STATUS_FIELD_DECISION_CLASS}")
    print("bounded_source_status_field_decision_packet_created_now=true")
    print("local_source_status_field_patch_plan_packet_created_now=false")
    print("source_artifact_mutated_now=false")
    print("source_status_invented_now=false")
    print("status_field_added_now=false")
    print("reusable_schema_authorized=false")
    print("additional_sample_discovery_now=false")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print(f"recommended_human_decision={RECOMMENDED_HUMAN_DECISION}")
    print(f"if_accepted_authorizes_future_unit={FUTURE_UNIT}")
    print(f"recommended_review_unit={REVIEW_UNIT}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
