#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_FOR_BOUNDED_PATCH_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.local_source_status_field_patch_plan_packet.acceptance.for_bounded_patch_execution.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_ACCEPTED_FOR_BOUNDED_PATCH_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE"

SOURCE_PATCH_PLAN_RECEIPT_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_receipt_b10148ed"
SOURCE_PATCH_PLAN_PACKET_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_f58c1b51"
SOURCE_PATCH_PLAN_OPTIONS_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_options_77eb834a"
SOURCE_PATCH_PLAN_BOUNDARY_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_boundary_1a3bcee6"

SOURCE_PATCH_PLAN_ACCEPTANCE_RECEIPT_ID = "c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_acceptance_for_local_patch_plan_receipt_396bb17a"
SOURCE_PATCH_PLAN_ACCEPTANCE_DECISION_ID = "c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_acceptance_for_local_patch_plan_decision_9eca13bb"
SOURCE_PATCH_PLAN_ACCEPTANCE_PACKET_ID = "c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_acceptance_for_local_patch_plan_packet_039f01b6"
SOURCE_LOCAL_PATCH_PLAN_AUTHORITY_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_authority_35a09951"
SOURCE_PATCH_PLAN_ACCEPTANCE_BOUNDARY_ID = "c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_acceptance_for_local_patch_plan_boundary_c66dc6ab"

SOURCE_DECISION_RECEIPT_ID = "c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_receipt_30c28230"
SOURCE_DECISION_PACKET_ID = "c8_unit_feedback_hardening_bounded_source_status_field_decision_packet_86280da2"
SOURCE_DECISION_OPTIONS_ID = "c8_unit_feedback_hardening_bounded_source_status_field_decision_options_eb06ad9a"
SOURCE_DECISION_BOUNDARY_ID = "c8_unit_feedback_hardening_bounded_source_status_field_decision_boundary_c7d31912"

SOURCE_ACCEPTANCE_RECEIPT_ID = "c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_receipt_460dce66"
SOURCE_ACCEPTANCE_DECISION_ID = "c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_decision_3dbf6bf3"
SOURCE_ACCEPTANCE_PACKET_ID = "c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_packet_3e27fff9"
SOURCE_BOUNDED_DECISION_AUTHORITY_ID = "c8_unit_feedback_hardening_bounded_source_status_field_decision_authority_06f280f5"
SOURCE_ACCEPTANCE_BOUNDARY_ID = "c8_unit_feedback_hardening_source_status_gap_response_packet_acceptance_for_bounded_status_field_decision_boundary_c8d440fa"

SOURCE_RESPONSE_RECEIPT_ID = "c8_unit_feedback_hardening_source_status_gap_response_packet_receipt_f2a5ee2a"
SOURCE_RESPONSE_PACKET_ID = "c8_unit_feedback_hardening_source_status_gap_response_packet_187fdf77"
SOURCE_RESPONSE_OPTIONS_ID = "c8_unit_feedback_hardening_source_status_gap_response_options_be3d12d9"
SOURCE_RESPONSE_BOUNDARY_ID = "c8_unit_feedback_hardening_source_status_gap_response_boundary_ba38ede6"

FAILED_UNIT_SAMPLE_ID = "c8_failed_unit_sample_ee4e6092"
FAILED_UNIT_SAMPLE_SOURCE_PATH = "data/a0_current_receipt_chain_frontier_application_v0_receipts/c1d0f615.json"
FAILED_UNIT_SAMPLE_SOURCE_STATUS = "MISSING_STATUS_FIELD_WITH_FAILURE_INDICATOR"
LOCAL_GAP_OBJECT = "SOURCE_ARTIFACT_TOP_LEVEL_STATUS_ABSENCE"

LOCAL_PATCH_PLAN_CLASS = "LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_ADD_EXPLICIT_TOP_LEVEL_STATUS_WITH_PROVENANCE_AFTER_ACCEPTANCE"
PATCH_TARGET_SOURCE_ARTIFACT = FAILED_UNIT_SAMPLE_SOURCE_PATH
PATCH_TARGET_FIELD = "status"
PATCH_TARGET_VALUE = "FAILED"
PATCH_STATUS_SOURCE_BASIS = "existing failure indicator plus accepted local source-status gap chain"

HUMAN_DECISION = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_FOR_BOUNDED_PATCH_EXECUTION"
FUTURE_UNIT = "EXECUTE_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
REVIEW_UNIT = "REVIEW_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_ACCEPTANCE_FOR_BOUNDED_PATCH_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_after_runtime_adoption_closure_v0_receipts"

SOURCE_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_receipt_b10148ed.json"
SOURCE_PACKET = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_v0.json"
SOURCE_OPTIONS = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_plan_options_v0.json"
SOURCE_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_plan_boundary_audit_v0.json"
SOURCE_READOUT = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_plan_readout_v0.json"
SOURCE_REPORT = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_plan_report.json"
TARGET_SOURCE_ARTIFACT = ROOT / PATCH_TARGET_SOURCE_ARTIFACT

ACCEPTANCE_DECISION = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_decision_v0.json"
ACCEPTANCE_PACKET = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_packet_v0.json"
PATCH_EXECUTION_AUTHORITY = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_authority_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "patch_execution_count",
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
        "source_receipt": SOURCE_RECEIPT,
        "source_packet": SOURCE_PACKET,
        "source_options": SOURCE_OPTIONS,
        "source_boundary": SOURCE_BOUNDARY,
        "source_readout": SOURCE_READOUT,
        "source_report": SOURCE_REPORT,
        "target_source_artifact": TARGET_SOURCE_ARTIFACT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {label: sha256_file(path) for label, path in sources.items() if path.exists()}

    receipt = read_json(SOURCE_RECEIPT)
    packet = read_json(SOURCE_PACKET)
    options = read_json(SOURCE_OPTIONS)
    boundary = read_json(SOURCE_BOUNDARY)
    target_artifact = read_json(TARGET_SOURCE_ARTIFACT)
    summary = receipt.get("machine_readable_unit_feedback_hardening_local_source_status_field_patch_plan_packet_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_READY_FOR_REVIEW",
        "receipt_id": SOURCE_PATCH_PLAN_RECEIPT_ID,
    }
    for key, want in expected_receipt.items():
        chk(failures, f"source_receipt_{key}", receipt.get(key), want)

    expected_summary = {
        "local_source_status_field_patch_plan_packet_created": True,
        "authorized_unit_consumed": "CREATE_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "failed_unit_sample_source_status": FAILED_UNIT_SAMPLE_SOURCE_STATUS,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "local_source_status_field_patch_plan_class": LOCAL_PATCH_PLAN_CLASS,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "patch_status_source_basis": PATCH_STATUS_SOURCE_BASIS,
        "local_source_status_field_patch_plan_packet_created_now": True,
        "patch_execution_authorized_now": False,
        "patch_executed_now": False,
        "source_artifact_mutated_now": False,
        "source_status_invented_now": False,
        "status_field_added_now": False,
        "reusable_schema_authorized": False,
        "requires_review": True,
        "recommended_human_decision": HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
    }
    for key, want in expected_summary.items():
        chk(failures, f"source_summary_{key}", summary.get(key), want)

    chk(failures, "source_packet_id", packet.get("c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_id"), SOURCE_PATCH_PLAN_PACKET_ID)
    chk(failures, "source_options_id", options.get("c8_unit_feedback_hardening_local_source_status_field_patch_plan_options_id"), SOURCE_PATCH_PLAN_OPTIONS_ID)
    chk(failures, "source_boundary_id", boundary.get("c8_unit_feedback_hardening_local_source_status_field_patch_plan_boundary_audit_id"), SOURCE_PATCH_PLAN_BOUNDARY_ID)
    chk(failures, "options_recommended_human_decision", options.get("recommended_human_decision"), HUMAN_DECISION)
    chk(failures, "options_future_unit", options.get("if_accepted_authorizes_future_unit"), FUTURE_UNIT)

    if HUMAN_DECISION not in options.get("human_decision_options", []):
        failures.append("human_decision_missing_from_options")

    if target_artifact.get(PATCH_TARGET_FIELD) == PATCH_TARGET_VALUE:
        warnings.append("target_already_has_requested_status_failed")
    elif PATCH_TARGET_FIELD in target_artifact:
        warnings.append("target_has_different_status_value")

    decision = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_decision_v0",
        "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_decision_id": None,
        "created_at": now_iso(),
        "human_decision": HUMAN_DECISION,
        "human_decision_consumed": True,
        "source_patch_plan_receipt_id": SOURCE_PATCH_PLAN_RECEIPT_ID,
        "source_patch_plan_packet_id": SOURCE_PATCH_PLAN_PACKET_ID,
        "source_patch_plan_options_id": SOURCE_PATCH_PLAN_OPTIONS_ID,
        "source_patch_plan_boundary_id": SOURCE_PATCH_PLAN_BOUNDARY_ID,
        "source_patch_plan_acceptance_receipt_id": SOURCE_PATCH_PLAN_ACCEPTANCE_RECEIPT_ID,
        "source_patch_plan_acceptance_decision_id": SOURCE_PATCH_PLAN_ACCEPTANCE_DECISION_ID,
        "source_patch_plan_acceptance_packet_id": SOURCE_PATCH_PLAN_ACCEPTANCE_PACKET_ID,
        "source_local_source_status_field_patch_plan_authority_id": SOURCE_LOCAL_PATCH_PLAN_AUTHORITY_ID,
        "source_patch_plan_acceptance_boundary_id": SOURCE_PATCH_PLAN_ACCEPTANCE_BOUNDARY_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "failed_unit_sample_source_status": FAILED_UNIT_SAMPLE_SOURCE_STATUS,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "local_source_status_field_patch_plan_class": LOCAL_PATCH_PLAN_CLASS,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "patch_status_source_basis": PATCH_STATUS_SOURCE_BASIS,
        "local_source_status_field_patch_plan_packet_accepted_for_bounded_patch_execution": True,
        "authorized_future_unit_after_review": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "patch_execution_authorized_now": False,
        "patch_executed_now": False,
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
    }
    decision["c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_decision_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_decision_" + sig8(decision)
    write_json(ACCEPTANCE_DECISION, decision)

    execution_authority = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_authority_v0",
        "c8_unit_feedback_hardening_local_source_status_field_patch_execution_authority_id": None,
        "created_at": now_iso(),
        "source_local_source_status_field_patch_plan_packet_acceptance_decision_id": decision["c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_decision_id"],
        "source_patch_plan_receipt_id": SOURCE_PATCH_PLAN_RECEIPT_ID,
        "source_patch_plan_packet_id": SOURCE_PATCH_PLAN_PACKET_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "authorized_future_unit": FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authority_status": "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "authority_scope": {
            "may_execute_one_local_source_status_field_patch": True,
            "may_execute_patch_now": False,
            "may_mutate_only_target_source_artifact_during_execution": True,
            "may_add_exact_top_level_status_field_during_execution": True,
            "may_set_status_to_exact_target_value_during_execution": True,
            "may_invent_other_source_status": False,
            "may_authorize_reusable_schema": False,
            "may_execute_additional_sample_discovery": False,
            "may_authorize_probe_execution_now": False,
            "may_execute_probe_now": False,
            "may_build_now": False,
            "may_rerun_c8_now": False,
        },
    }
    execution_authority["c8_unit_feedback_hardening_local_source_status_field_patch_execution_authority_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_authority_" + sig8(execution_authority)
    write_json(PATCH_EXECUTION_AUTHORITY, execution_authority)

    acceptance_packet = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_packet_v0",
        "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_packet_id": None,
        "created_at": now_iso(),
        "acceptance_status": "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_ACCEPTED_FOR_BOUNDED_PATCH_EXECUTION",
        "source_local_source_status_field_patch_plan_packet_acceptance_decision_id": decision["c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_decision_id"],
        "source_local_source_status_field_patch_execution_authority_id": execution_authority["c8_unit_feedback_hardening_local_source_status_field_patch_execution_authority_id"],
        "human_decision": HUMAN_DECISION,
        "source_patch_plan_receipt_id": SOURCE_PATCH_PLAN_RECEIPT_ID,
        "source_patch_plan_packet_id": SOURCE_PATCH_PLAN_PACKET_ID,
        "source_patch_plan_options_id": SOURCE_PATCH_PLAN_OPTIONS_ID,
        "source_patch_plan_boundary_id": SOURCE_PATCH_PLAN_BOUNDARY_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_status": FAILED_UNIT_SAMPLE_SOURCE_STATUS,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "local_source_status_field_patch_plan_class": LOCAL_PATCH_PLAN_CLASS,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "patch_status_source_basis": PATCH_STATUS_SOURCE_BASIS,
        "local_source_status_field_patch_plan_packet_accepted_for_bounded_patch_execution": True,
        "authorized_future_unit_after_review": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "patch_execution_authorized_now": False,
        "patch_executed_now": False,
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
        "recommended_review_unit": REVIEW_UNIT,
    }
    acceptance_packet["c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_packet_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_packet_" + sig8(acceptance_packet)
    write_json(ACCEPTANCE_PACKET, acceptance_packet)

    boundary_audit = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_boundary_audit_v0",
        "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_local_source_status_field_patch_plan_packet_acceptance_decision_id": decision["c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_decision_id"],
        "source_local_source_status_field_patch_plan_packet_acceptance_packet_id": acceptance_packet["c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_packet_id"],
        "source_local_source_status_field_patch_execution_authority_id": execution_authority["c8_unit_feedback_hardening_local_source_status_field_patch_execution_authority_id"],
        "allowed_now": {
            "accept_local_source_status_field_patch_plan_for_bounded_patch_execution": True,
            "authorize_one_bounded_patch_execution_after_review_and_commit": True,
        },
        "not_allowed_now": {
            "execute_patch_now": True,
            "mutate_source_artifact_now": True,
            "add_status_field_now": True,
            "invent_source_status": True,
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
    boundary_audit["c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_boundary_audit_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    source_hashes_after = {label: sha256_file(path) for label, path in sources.items() if path.exists()}
    if source_hashes_before != source_hashes_after:
        forbidden_counters["source_artifact_mutation_count"] += 1
        failures.append("source_artifact_mutation_count:1")

    gate_results = {
        "BOUNDED_PATCH_EXECUTION_ACCEPTANCE_0_SOURCE_PATCH_PLAN_RECEIPT_PASS": receipt.get("gate") == "PASS",
        "BOUNDED_PATCH_EXECUTION_ACCEPTANCE_1_HUMAN_DECISION_MATCH": HUMAN_DECISION == options.get("recommended_human_decision"),
        "BOUNDED_PATCH_EXECUTION_ACCEPTANCE_2_FUTURE_UNIT_MATCH": FUTURE_UNIT == options.get("if_accepted_authorizes_future_unit"),
        "BOUNDED_PATCH_EXECUTION_ACCEPTANCE_3_TARGET_ARTIFACT_PRESENT": TARGET_SOURCE_ARTIFACT.exists(),
        "BOUNDED_PATCH_EXECUTION_ACCEPTANCE_4_ACCEPTANCE_RECORDED": acceptance_packet["local_source_status_field_patch_plan_packet_accepted_for_bounded_patch_execution"] is True,
        "BOUNDED_PATCH_EXECUTION_ACCEPTANCE_5_PATCH_NOT_EXECUTED_NOW": acceptance_packet["patch_executed_now"] is False and acceptance_packet["patch_execution_authorized_now"] is False,
        "BOUNDED_PATCH_EXECUTION_ACCEPTANCE_6_NO_SOURCE_MUTATION_STATUS_INVENTION_OR_FIELD_ADDITION_NOW": acceptance_packet["source_artifact_mutated_now"] is False and acceptance_packet["source_status_invented_now"] is False and acceptance_packet["status_field_added_now"] is False,
        "BOUNDED_PATCH_EXECUTION_ACCEPTANCE_7_NO_SCHEMA_DISCOVERY_PROBE_BUILD_RERUN": acceptance_packet["reusable_schema_authorized_now"] is False and acceptance_packet["additional_sample_discovery_now"] is False and acceptance_packet["probe_execution_authorized_now"] is False and acceptance_packet["instrument_build_authorized_now"] is False and acceptance_packet["c8_rerun_authorized_now"] is False,
        "BOUNDED_PATCH_EXECUTION_ACCEPTANCE_8_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "BOUNDED_PATCH_EXECUTION_ACCEPTANCE_9_FORBIDDEN_COUNTERS_ZERO": all(v == 0 for v in forbidden_counters.values()),
        "BOUNDED_PATCH_EXECUTION_ACCEPTANCE_10_REQUIRES_REVIEW": acceptance_packet["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"bounded_patch_execution_acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_ACCEPTANCE_FOR_BOUNDED_PATCH_EXECUTION_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_ACCEPTANCE_FOR_BOUNDED_PATCH_EXECUTION_FAIL"
    outcome = "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_ACCEPTED_FOR_BOUNDED_PATCH_EXECUTION" if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_ACCEPTANCE_FOR_BOUNDED_PATCH_EXECUTION_FAILED"
    terminal_stop = "STOP_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_ACCEPTANCE_FOR_BOUNDED_PATCH_EXECUTION_READY_FOR_REVIEW" if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_ACCEPTANCE_FOR_BOUNDED_PATCH_EXECUTION_FAILED"

    readout = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_readout_v0",
        "title": "C8 local source-status field patch-plan acceptance for bounded patch execution",
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "local_source_status_field_patch_plan_class": LOCAL_PATCH_PLAN_CLASS,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "local_source_status_field_patch_plan_packet_accepted_for_bounded_patch_execution": True,
        "authorized_future_unit_after_review": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "patch_execution_authorized_now": False,
        "patch_executed_now": False,
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
        "recommended_review_unit": REVIEW_UNIT,
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report_obj = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_patch_plan_receipt_id": SOURCE_PATCH_PLAN_RECEIPT_ID,
        "source_patch_plan_packet_id": SOURCE_PATCH_PLAN_PACKET_ID,
        "source_patch_plan_options_id": SOURCE_PATCH_PLAN_OPTIONS_ID,
        "source_patch_plan_boundary_id": SOURCE_PATCH_PLAN_BOUNDARY_ID,
        "human_decision": HUMAN_DECISION,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "local_source_status_field_patch_plan_class": LOCAL_PATCH_PLAN_CLASS,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "local_source_status_field_patch_plan_packet_accepted_for_bounded_patch_execution": True,
        "authorized_future_unit_after_review": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "patch_execution_authorized_now": False,
        "patch_executed_now": False,
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
        "recommended_review_unit": REVIEW_UNIT,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report_obj)

    receipt_obj = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_ACCEPTANCE_FOR_BOUNDED_PATCH_EXECUTION_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_summary": {
            "local_source_status_field_patch_plan_packet_acceptance_complete": gate == "PASS",
            "authorized_unit_consumed": UNIT_ID,
            "human_decision": HUMAN_DECISION,
            "source_patch_plan_receipt_id": SOURCE_PATCH_PLAN_RECEIPT_ID,
            "source_patch_plan_packet_id": SOURCE_PATCH_PLAN_PACKET_ID,
            "source_patch_plan_options_id": SOURCE_PATCH_PLAN_OPTIONS_ID,
            "source_patch_plan_boundary_id": SOURCE_PATCH_PLAN_BOUNDARY_ID,
            "source_patch_plan_acceptance_receipt_id": SOURCE_PATCH_PLAN_ACCEPTANCE_RECEIPT_ID,
            "source_patch_plan_acceptance_decision_id": SOURCE_PATCH_PLAN_ACCEPTANCE_DECISION_ID,
            "source_patch_plan_acceptance_packet_id": SOURCE_PATCH_PLAN_ACCEPTANCE_PACKET_ID,
            "source_local_source_status_field_patch_plan_authority_id": SOURCE_LOCAL_PATCH_PLAN_AUTHORITY_ID,
            "source_patch_plan_acceptance_boundary_id": SOURCE_PATCH_PLAN_ACCEPTANCE_BOUNDARY_ID,
            "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
            "source_decision_packet_id": SOURCE_DECISION_PACKET_ID,
            "source_decision_options_id": SOURCE_DECISION_OPTIONS_ID,
            "source_decision_boundary_id": SOURCE_DECISION_BOUNDARY_ID,
            "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
            "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
            "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
            "source_bounded_source_status_field_decision_authority_id": SOURCE_BOUNDED_DECISION_AUTHORITY_ID,
            "source_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
            "source_response_receipt_id": SOURCE_RESPONSE_RECEIPT_ID,
            "source_response_packet_id": SOURCE_RESPONSE_PACKET_ID,
            "source_response_options_id": SOURCE_RESPONSE_OPTIONS_ID,
            "source_response_boundary_id": SOURCE_RESPONSE_BOUNDARY_ID,
            "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
            "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
            "failed_unit_sample_source_status": FAILED_UNIT_SAMPLE_SOURCE_STATUS,
            "local_gap_object": LOCAL_GAP_OBJECT,
            "local_source_status_field_patch_plan_class": LOCAL_PATCH_PLAN_CLASS,
            "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
            "patch_target_field": PATCH_TARGET_FIELD,
            "patch_target_value": PATCH_TARGET_VALUE,
            "patch_status_source_basis": PATCH_STATUS_SOURCE_BASIS,
            "local_source_status_field_patch_plan_packet_accepted_for_bounded_patch_execution": True,
            "authorized_future_unit_after_review": FUTURE_UNIT,
            "authorized_future_unit_count_after_review": 1,
            "patch_execution_authorized_now": False,
            "patch_executed_now": False,
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
            "bounded_patch_execution_acceptance_decision": rel(ACCEPTANCE_DECISION),
            "bounded_patch_execution_acceptance_packet": rel(ACCEPTANCE_PACKET),
            "bounded_patch_execution_authority": rel(PATCH_EXECUTION_AUTHORITY),
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

    receipt_obj["receipt_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_receipt_" + sig8(receipt_obj)
    receipt_path = RECEIPT_DIR / f"{receipt_obj['receipt_id']}.json"
    receipt_obj["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_obj)

    print(json.dumps(receipt_obj, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_receipt_id={receipt_obj['receipt_id']}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_decision_path={rel(ACCEPTANCE_DECISION)}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_packet_path={rel(ACCEPTANCE_PACKET)}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_authority_path={rel(PATCH_EXECUTION_AUTHORITY)}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"human_decision={HUMAN_DECISION}")
    print(f"failed_unit_sample_id={FAILED_UNIT_SAMPLE_ID}")
    print(f"local_gap_object={LOCAL_GAP_OBJECT}")
    print(f"patch_target_source_artifact_path={PATCH_TARGET_SOURCE_ARTIFACT}")
    print(f"patch_target_field={PATCH_TARGET_FIELD}")
    print(f"patch_target_value={PATCH_TARGET_VALUE}")
    print("local_source_status_field_patch_plan_packet_accepted_for_bounded_patch_execution=true")
    print(f"authorized_future_unit_after_review={FUTURE_UNIT}")
    print("authorized_future_unit_count_after_review=1")
    print("patch_execution_authorized_now=false")
    print("patch_executed_now=false")
    print("source_artifact_mutated_now=false")
    print("source_status_invented_now=false")
    print("status_field_added_now=false")
    print("reusable_schema_authorized=false")
    print("additional_sample_discovery_now=false")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print(f"recommended_review_unit={REVIEW_UNIT}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
