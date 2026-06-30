#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXECUTE_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.local_source_status_field_patch.execution.once.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTED_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE"

SOURCE_ACCEPTANCE_RECEIPT_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_receipt_a2a22d84"
SOURCE_ACCEPTANCE_DECISION_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_decision_7eeafa59"
SOURCE_ACCEPTANCE_PACKET_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_packet_ad68af1c"
SOURCE_PATCH_EXECUTION_AUTHORITY_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_authority_91f9e460"
SOURCE_ACCEPTANCE_BOUNDARY_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_boundary_a7198aa1"

SOURCE_PATCH_PLAN_RECEIPT_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_receipt_b10148ed"
SOURCE_PATCH_PLAN_PACKET_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_f58c1b51"
SOURCE_PATCH_PLAN_OPTIONS_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_options_77eb834a"
SOURCE_PATCH_PLAN_BOUNDARY_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_plan_boundary_1a3bcee6"

FAILED_UNIT_SAMPLE_ID = "c8_failed_unit_sample_ee4e6092"
FAILED_UNIT_SAMPLE_SOURCE_PATH = "data/a0_current_receipt_chain_frontier_application_v0_receipts/c1d0f615.json"
FAILED_UNIT_SAMPLE_SOURCE_STATUS = "MISSING_STATUS_FIELD_WITH_FAILURE_INDICATOR"
LOCAL_GAP_OBJECT = "SOURCE_ARTIFACT_TOP_LEVEL_STATUS_ABSENCE"

PATCH_PLAN_CLASS = "LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_ADD_EXPLICIT_TOP_LEVEL_STATUS_WITH_PROVENANCE_AFTER_ACCEPTANCE"
PATCH_TARGET_SOURCE_ARTIFACT = FAILED_UNIT_SAMPLE_SOURCE_PATH
PATCH_TARGET_FIELD = "status"
PATCH_TARGET_VALUE = "FAILED"
PATCH_STATUS_SOURCE_BASIS = "existing failure indicator plus accepted local source-status gap chain"

REVIEW_UNIT = "REVIEW_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_after_runtime_adoption_closure_v0_receipts"

ACCEPTANCE_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_receipt_a2a22d84.json"
ACCEPTANCE_DECISION = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_decision_v0.json"
ACCEPTANCE_PACKET = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_packet_v0.json"
PATCH_EXECUTION_AUTHORITY = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_execution_authority_v0.json"
ACCEPTANCE_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_boundary_audit_v0.json"
ACCEPTANCE_READOUT = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_readout_v0.json"
ACCEPTANCE_REPORT = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_report.json"
TARGET_SOURCE_ARTIFACT = ROOT / PATCH_TARGET_SOURCE_ARTIFACT

PATCH_RESULT = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_result_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_report.json"

FORBIDDEN_COUNTER_KEYS = [
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
    "non_target_source_artifact_mutation_count",
    "wrong_field_mutation_count",
    "wrong_value_mutation_count",
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

def exactly_before_plus_status(before: Dict[str, Any], after: Dict[str, Any]) -> bool:
    expected = copy.deepcopy(before)
    expected[PATCH_TARGET_FIELD] = PATCH_TARGET_VALUE
    return after == expected

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []
    forbidden_counters = {k: 0 for k in FORBIDDEN_COUNTER_KEYS}
    allowed_counters = {
        "patch_execution_count": 0,
        "target_source_artifact_mutation_count": 0,
        "status_field_added_count": 0,
    }

    sources = {
        "acceptance_receipt": ACCEPTANCE_RECEIPT,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_packet": ACCEPTANCE_PACKET,
        "patch_execution_authority": PATCH_EXECUTION_AUTHORITY,
        "acceptance_boundary": ACCEPTANCE_BOUNDARY,
        "acceptance_readout": ACCEPTANCE_READOUT,
        "acceptance_report": ACCEPTANCE_REPORT,
        "target_source_artifact": TARGET_SOURCE_ARTIFACT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {label: sha256_file(path) for label, path in sources.items() if path.exists()}

    receipt = read_json(ACCEPTANCE_RECEIPT)
    decision = read_json(ACCEPTANCE_DECISION)
    packet = read_json(ACCEPTANCE_PACKET)
    authority = read_json(PATCH_EXECUTION_AUTHORITY)
    boundary = read_json(ACCEPTANCE_BOUNDARY)
    before_target = read_json(TARGET_SOURCE_ARTIFACT)
    summary = receipt.get("machine_readable_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_ACCEPTANCE_FOR_BOUNDED_PATCH_EXECUTION_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_ACCEPTED_FOR_BOUNDED_PATCH_EXECUTION",
        "receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
    }
    for key, want in expected_receipt.items():
        chk(failures, f"acceptance_receipt_{key}", receipt.get(key), want)

    expected_summary = {
        "local_source_status_field_patch_plan_packet_acceptance_complete": True,
        "authorized_unit_consumed": "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_FOR_BOUNDED_PATCH_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "human_decision": "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_PACKET_FOR_BOUNDED_PATCH_EXECUTION",
        "source_patch_plan_receipt_id": SOURCE_PATCH_PLAN_RECEIPT_ID,
        "source_patch_plan_packet_id": SOURCE_PATCH_PLAN_PACKET_ID,
        "source_patch_plan_options_id": SOURCE_PATCH_PLAN_OPTIONS_ID,
        "source_patch_plan_boundary_id": SOURCE_PATCH_PLAN_BOUNDARY_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "failed_unit_sample_source_status": FAILED_UNIT_SAMPLE_SOURCE_STATUS,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "local_source_status_field_patch_plan_class": PATCH_PLAN_CLASS,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "patch_status_source_basis": PATCH_STATUS_SOURCE_BASIS,
        "local_source_status_field_patch_plan_packet_accepted_for_bounded_patch_execution": True,
        "authorized_future_unit_after_review": UNIT_ID,
        "authorized_future_unit_count_after_review": 1,
        "patch_execution_authorized_now": False,
        "patch_executed_now": False,
        "source_artifact_mutated_now": False,
        "source_status_invented_now": False,
        "status_field_added_now": False,
        "reusable_schema_authorized": False,
        "requires_review": True,
    }
    for key, want in expected_summary.items():
        chk(failures, f"acceptance_summary_{key}", summary.get(key), want)

    chk(failures, "acceptance_decision_id", decision.get("c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_decision_id"), SOURCE_ACCEPTANCE_DECISION_ID)
    chk(failures, "acceptance_packet_id", packet.get("c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_packet_id"), SOURCE_ACCEPTANCE_PACKET_ID)
    chk(failures, "acceptance_boundary_id", boundary.get("c8_unit_feedback_hardening_local_source_status_field_patch_plan_packet_acceptance_for_bounded_patch_execution_boundary_audit_id"), SOURCE_ACCEPTANCE_BOUNDARY_ID)
    chk(failures, "patch_execution_authority_id", authority.get("c8_unit_feedback_hardening_local_source_status_field_patch_execution_authority_id"), SOURCE_PATCH_EXECUTION_AUTHORITY_ID)
    chk(failures, "authority_status", authority.get("authority_status"), "ACTIVE_AFTER_REVIEW_AND_COMMIT")
    chk(failures, "authority_future_unit", authority.get("authorized_future_unit"), UNIT_ID)
    chk(failures, "authority_future_unit_count", authority.get("authorized_future_unit_count"), 1)
    chk(failures, "authority_patch_target", authority.get("patch_target_source_artifact_path"), PATCH_TARGET_SOURCE_ARTIFACT)
    chk(failures, "authority_patch_field", authority.get("patch_target_field"), PATCH_TARGET_FIELD)
    chk(failures, "authority_patch_value", authority.get("patch_target_value"), PATCH_TARGET_VALUE)

    scope = authority.get("authority_scope", {})
    chk(failures, "scope_may_execute_one_patch", scope.get("may_execute_one_local_source_status_field_patch"), True)
    chk(failures, "scope_may_mutate_only_target", scope.get("may_mutate_only_target_source_artifact_during_execution"), True)
    chk(failures, "scope_may_add_exact_status_field", scope.get("may_add_exact_top_level_status_field_during_execution"), True)
    chk(failures, "scope_may_set_status_exact_value", scope.get("may_set_status_to_exact_target_value_during_execution"), True)
    chk(failures, "scope_may_invent_other_status", scope.get("may_invent_other_source_status"), False)
    chk(failures, "scope_may_authorize_reusable_schema", scope.get("may_authorize_reusable_schema"), False)

    target_status_before = before_target.get(PATCH_TARGET_FIELD, None)
    target_status_field_present_before = PATCH_TARGET_FIELD in before_target

    if target_status_field_present_before:
        failures.append(f"target_status_field_already_present:{target_status_before}")

    after_target = copy.deepcopy(before_target)
    after_target[PATCH_TARGET_FIELD] = PATCH_TARGET_VALUE

    if not failures:
        write_json(TARGET_SOURCE_ARTIFACT, after_target)
        allowed_counters["patch_execution_count"] += 1
        allowed_counters["target_source_artifact_mutation_count"] += 1
        allowed_counters["status_field_added_count"] += 1

    source_hashes_after = {label: sha256_file(path) for label, path in sources.items() if path.exists()}
    observed_after_target = read_json(TARGET_SOURCE_ARTIFACT)

    non_target_labels = [k for k in sources if k != "target_source_artifact"]
    non_target_mutations = [
        k for k in non_target_labels
        if source_hashes_before.get(k) != source_hashes_after.get(k)
    ]
    if non_target_mutations:
        forbidden_counters["non_target_source_artifact_mutation_count"] += len(non_target_mutations)
        failures.append(f"non_target_source_artifact_mutations:{non_target_mutations}")

    if not exactly_before_plus_status(before_target, observed_after_target):
        failures.append("target_semantic_delta_not_exactly_before_plus_status")
        if observed_after_target.get(PATCH_TARGET_FIELD) != PATCH_TARGET_VALUE:
            forbidden_counters["wrong_value_mutation_count"] += 1
        if set(observed_after_target.keys()) != set(before_target.keys()) | {PATCH_TARGET_FIELD}:
            forbidden_counters["wrong_field_mutation_count"] += 1

    target_hash_changed = source_hashes_before.get("target_source_artifact") != source_hashes_after.get("target_source_artifact")
    if not target_hash_changed and not failures:
        failures.append("target_source_artifact_hash_did_not_change")

    gate_results = {
        "LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_0_ACCEPTANCE_RECEIPT_PASS": receipt.get("gate") == "PASS",
        "LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_1_AUTHORITY_ACTIVE": authority.get("authority_status") == "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_2_AUTHORIZED_UNIT_MATCH": authority.get("authorized_future_unit") == UNIT_ID,
        "LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_3_TARGET_STATUS_FIELD_ABSENT_BEFORE": target_status_field_present_before is False,
        "LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_4_TARGET_PATCHED_TO_EXACT_STATUS_VALUE": observed_after_target.get(PATCH_TARGET_FIELD) == PATCH_TARGET_VALUE,
        "LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_5_TARGET_DELTA_EXACTLY_ONE_TOP_LEVEL_STATUS_FIELD": exactly_before_plus_status(before_target, observed_after_target),
        "LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_6_ONLY_TARGET_SOURCE_ARTIFACT_MUTATED": not non_target_mutations and target_hash_changed,
        "LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_7_NO_SOURCE_STATUS_INVENTION_OR_SCHEMA_AUTHORIZATION": forbidden_counters["source_status_invented_count"] == 0 and forbidden_counters["reusable_schema_authorized_count"] == 0,
        "LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_8_NO_DISCOVERY_PROBE_BUILD_RERUN": forbidden_counters["additional_sample_discovery_count"] == 0 and forbidden_counters["probe_executed_count"] == 0 and forbidden_counters["instrument_build_count"] == 0 and forbidden_counters["c8_rerun_count"] == 0,
        "LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_9_FORBIDDEN_COUNTERS_ZERO": all(v == 0 for v in forbidden_counters.values()),
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"local_source_status_field_patch_execution_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_ONCE_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_ONCE_FAIL"
    outcome = "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTED_ONCE_READY_FOR_REVIEW" if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_ONCE_FAILED"
    terminal_stop = "STOP_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_ONCE_READY_FOR_REVIEW" if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_ONCE_FAILED"

    patch_result = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_result_v0",
        "c8_unit_feedback_hardening_local_source_status_field_patch_execution_result_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
        "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
        "source_patch_execution_authority_id": SOURCE_PATCH_EXECUTION_AUTHORITY_ID,
        "source_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
        "source_patch_plan_receipt_id": SOURCE_PATCH_PLAN_RECEIPT_ID,
        "source_patch_plan_packet_id": SOURCE_PATCH_PLAN_PACKET_ID,
        "source_patch_plan_options_id": SOURCE_PATCH_PLAN_OPTIONS_ID,
        "source_patch_plan_boundary_id": SOURCE_PATCH_PLAN_BOUNDARY_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "failed_unit_sample_source_status": FAILED_UNIT_SAMPLE_SOURCE_STATUS,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "local_source_status_field_patch_plan_class": PATCH_PLAN_CLASS,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "patch_status_source_basis": PATCH_STATUS_SOURCE_BASIS,
        "target_status_field_present_before": target_status_field_present_before,
        "target_status_value_before": target_status_before,
        "target_status_value_after": observed_after_target.get(PATCH_TARGET_FIELD),
        "target_source_artifact_sha256_before": source_hashes_before.get("target_source_artifact"),
        "target_source_artifact_sha256_after": source_hashes_after.get("target_source_artifact"),
        "target_source_artifact_mutated": target_hash_changed,
        "semantic_delta": "ADD_TOP_LEVEL_STATUS_FIELD_ONLY",
        "patch_executed_now": gate == "PASS",
        "source_artifact_mutated_now": gate == "PASS",
        "status_field_added_now": gate == "PASS",
        "source_status_invented_now": False,
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
    patch_result["c8_unit_feedback_hardening_local_source_status_field_patch_execution_result_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_result_" + sig8(patch_result)
    write_json(PATCH_RESULT, patch_result)

    boundary_audit = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_boundary_audit_v0",
        "c8_unit_feedback_hardening_local_source_status_field_patch_execution_boundary_audit_id": None,
        "gate": gate,
        "source_patch_execution_result_id": patch_result["c8_unit_feedback_hardening_local_source_status_field_patch_execution_result_id"],
        "source_patch_execution_authority_id": SOURCE_PATCH_EXECUTION_AUTHORITY_ID,
        "allowed_now": {
            "execute_one_local_source_status_field_patch": True,
            "mutate_only_target_source_artifact": True,
            "add_exact_top_level_status_field": True,
            "set_status_to_exact_target_value": True,
        },
        "not_allowed_now": {
            "mutate_non_target_source_artifacts": True,
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
        "allowed_counters": allowed_counters,
        "forbidden_counters": forbidden_counters,
        "failures": failures,
        "warnings": warnings,
    }
    boundary_audit["c8_unit_feedback_hardening_local_source_status_field_patch_execution_boundary_audit_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    readout = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_readout_v0",
        "title": "C8 local source-status field patch execution once",
        "status": status,
        "outcome_class": outcome,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "target_source_artifact_sha256_before": source_hashes_before.get("target_source_artifact"),
        "target_source_artifact_sha256_after": source_hashes_after.get("target_source_artifact"),
        "patch_executed_now": gate == "PASS",
        "source_artifact_mutated_now": gate == "PASS",
        "status_field_added_now": gate == "PASS",
        "source_status_invented_now": False,
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
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_patch_execution_authority_id": SOURCE_PATCH_EXECUTION_AUTHORITY_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "patch_executed_now": gate == "PASS",
        "source_artifact_mutated_now": gate == "PASS",
        "status_field_added_now": gate == "PASS",
        "source_status_invented_now": False,
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
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_ONCE_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_local_source_status_field_patch_execution_once_summary": {
            "local_source_status_field_patch_execution_complete": gate == "PASS",
            "authorized_unit_consumed": UNIT_ID,
            "source_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
            "source_acceptance_decision_id": SOURCE_ACCEPTANCE_DECISION_ID,
            "source_acceptance_packet_id": SOURCE_ACCEPTANCE_PACKET_ID,
            "source_patch_execution_authority_id": SOURCE_PATCH_EXECUTION_AUTHORITY_ID,
            "source_acceptance_boundary_id": SOURCE_ACCEPTANCE_BOUNDARY_ID,
            "source_patch_plan_receipt_id": SOURCE_PATCH_PLAN_RECEIPT_ID,
            "source_patch_plan_packet_id": SOURCE_PATCH_PLAN_PACKET_ID,
            "source_patch_plan_options_id": SOURCE_PATCH_PLAN_OPTIONS_ID,
            "source_patch_plan_boundary_id": SOURCE_PATCH_PLAN_BOUNDARY_ID,
            "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
            "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
            "failed_unit_sample_source_status": FAILED_UNIT_SAMPLE_SOURCE_STATUS,
            "local_gap_object": LOCAL_GAP_OBJECT,
            "local_source_status_field_patch_plan_class": PATCH_PLAN_CLASS,
            "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
            "patch_target_field": PATCH_TARGET_FIELD,
            "patch_target_value": PATCH_TARGET_VALUE,
            "patch_status_source_basis": PATCH_STATUS_SOURCE_BASIS,
            "target_status_field_present_before": target_status_field_present_before,
            "target_status_value_before": target_status_before,
            "target_status_value_after": observed_after_target.get(PATCH_TARGET_FIELD),
            "target_source_artifact_sha256_before": source_hashes_before.get("target_source_artifact"),
            "target_source_artifact_sha256_after": source_hashes_after.get("target_source_artifact"),
            "semantic_delta": "ADD_TOP_LEVEL_STATUS_FIELD_ONLY",
            "patch_executed_now": gate == "PASS",
            "source_artifact_mutated_now": gate == "PASS",
            "status_field_added_now": gate == "PASS",
            "source_status_invented_now": False,
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
            "non_target_source_artifacts_mutated": bool(non_target_mutations),
            "forbidden_counters_zero": all(v == 0 for v in forbidden_counters.values()),
            "allowed_counters": allowed_counters,
            "requires_review": True,
            "recommended_review_unit": REVIEW_UNIT,
            "next_command_goal": None,
        },
        "gate_results": gate_results,
        "allowed_counters": allowed_counters,
        "forbidden_counters": forbidden_counters,
        "source_artifact_hashes": {
            "before": source_hashes_before,
            "after": source_hashes_after,
            "target_source_artifact_mutated": target_hash_changed,
            "non_target_source_artifacts_mutated": non_target_mutations,
        },
        "output_artifacts": {
            "patch_execution_result": rel(PATCH_RESULT),
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

    receipt_obj["receipt_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_receipt_" + sig8(receipt_obj)
    receipt_path = RECEIPT_DIR / f"{receipt_obj['receipt_id']}.json"
    receipt_obj["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_obj)

    print(json.dumps(receipt_obj, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_receipt_id={receipt_obj['receipt_id']}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_result_path={rel(PATCH_RESULT)}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"failed_unit_sample_id={FAILED_UNIT_SAMPLE_ID}")
    print(f"local_gap_object={LOCAL_GAP_OBJECT}")
    print(f"patch_target_source_artifact_path={PATCH_TARGET_SOURCE_ARTIFACT}")
    print(f"patch_target_field={PATCH_TARGET_FIELD}")
    print(f"patch_target_value={PATCH_TARGET_VALUE}")
    print(f"target_source_artifact_sha256_before={source_hashes_before.get('target_source_artifact')}")
    print(f"target_source_artifact_sha256_after={source_hashes_after.get('target_source_artifact')}")
    print(f"target_status_field_present_before={target_status_field_present_before}")
    print(f"target_status_value_after={observed_after_target.get(PATCH_TARGET_FIELD)}")
    print(f"patch_executed_now={str(gate == 'PASS').lower()}")
    print(f"source_artifact_mutated_now={str(gate == 'PASS').lower()}")
    print(f"status_field_added_now={str(gate == 'PASS').lower()}")
    print("source_status_invented_now=false")
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
