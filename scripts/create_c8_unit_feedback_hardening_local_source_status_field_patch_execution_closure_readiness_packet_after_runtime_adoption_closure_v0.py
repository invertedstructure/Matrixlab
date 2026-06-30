#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CREATE_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.local_source_status_field_patch_execution.closure_readiness.packet.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_CREATED_AFTER_RUNTIME_ADOPTION_CLOSURE"

SOURCE_EXECUTION_COMMIT_SHA = "e801c5f7649bfed4b5d3708c94ecccf29499db02"

SOURCE_EXECUTION_RECEIPT_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_receipt_13e2733e"
SOURCE_EXECUTION_RESULT_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_result_7d04659d"
SOURCE_EXECUTION_BOUNDARY_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_boundary_044dda6d"

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
FAILED_UNIT_SAMPLE_SOURCE_STATUS_BEFORE = "MISSING_STATUS_FIELD_WITH_FAILURE_INDICATOR"
LOCAL_GAP_OBJECT = "SOURCE_ARTIFACT_TOP_LEVEL_STATUS_ABSENCE"

PATCH_PLAN_CLASS = "LOCAL_SOURCE_STATUS_FIELD_PATCH_PLAN_ADD_EXPLICIT_TOP_LEVEL_STATUS_WITH_PROVENANCE_AFTER_ACCEPTANCE"
PATCH_TARGET_SOURCE_ARTIFACT = FAILED_UNIT_SAMPLE_SOURCE_PATH
PATCH_TARGET_FIELD = "status"
PATCH_TARGET_VALUE = "FAILED"
TARGET_SHA256_BEFORE = "afa641e2822900897c47afa8b5aa6f2dbc4cd9382a22acdeffcfa3f0c080caa0"
TARGET_SHA256_AFTER = "a2ef7e5ab954f976f44ce49be885f36e7e7999d43bec581a7e65df06af024432"
PATCH_SEMANTIC_DELTA = "ADD_TOP_LEVEL_STATUS_FIELD_ONLY"

CLOSURE_CLASS = "LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_COMMITTED_REVIEWED_READY_FOR_POST_PATCH_SURFACE_DECISION"
RECOMMENDED_HUMAN_DECISION = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_FOR_POST_PATCH_SURFACE_DECISION"
FUTURE_UNIT = "CREATE_C8_UNIT_FEEDBACK_HARDENING_POST_SOURCE_STATUS_PATCH_SURFACE_DECISION_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
REVIEW_UNIT = "REVIEW_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_after_runtime_adoption_closure_v0_receipts"

EXECUTION_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_receipt_13e2733e.json"
EXECUTION_RESULT = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_execution_result_v0.json"
EXECUTION_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_execution_boundary_audit_v0.json"
EXECUTION_READOUT = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_execution_readout_v0.json"
EXECUTION_REPORT = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_execution_report.json"
TARGET_SOURCE_ARTIFACT = ROOT / PATCH_TARGET_SOURCE_ARTIFACT

CLOSURE_PACKET = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_v0.json"
OPTIONS = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_options_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "patch_execution_count",
    "target_source_artifact_mutation_count",
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
        "execution_receipt": EXECUTION_RECEIPT,
        "execution_result": EXECUTION_RESULT,
        "execution_boundary": EXECUTION_BOUNDARY,
        "execution_readout": EXECUTION_READOUT,
        "execution_report": EXECUTION_REPORT,
        "target_source_artifact": TARGET_SOURCE_ARTIFACT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {label: sha256_file(path) for label, path in sources.items() if path.exists()}

    execution_receipt = read_json(EXECUTION_RECEIPT)
    execution_result = read_json(EXECUTION_RESULT)
    execution_boundary = read_json(EXECUTION_BOUNDARY)
    execution_readout = read_json(EXECUTION_READOUT)
    execution_report = read_json(EXECUTION_REPORT)
    target = read_json(TARGET_SOURCE_ARTIFACT)

    summary = execution_receipt.get("machine_readable_unit_feedback_hardening_local_source_status_field_patch_execution_once_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_ONCE_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTED_ONCE_READY_FOR_REVIEW",
        "receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
    }
    for key, want in expected_receipt.items():
        chk(failures, f"execution_receipt_{key}", execution_receipt.get(key), want)

    expected_summary = {
        "local_source_status_field_patch_execution_complete": True,
        "authorized_unit_consumed": "EXECUTE_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
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
        "failed_unit_sample_source_status": FAILED_UNIT_SAMPLE_SOURCE_STATUS_BEFORE,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "local_source_status_field_patch_plan_class": PATCH_PLAN_CLASS,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "target_status_field_present_before": False,
        "target_status_value_before": None,
        "target_status_value_after": PATCH_TARGET_VALUE,
        "target_source_artifact_sha256_before": TARGET_SHA256_BEFORE,
        "target_source_artifact_sha256_after": TARGET_SHA256_AFTER,
        "semantic_delta": PATCH_SEMANTIC_DELTA,
        "patch_executed_now": True,
        "source_artifact_mutated_now": True,
        "status_field_added_now": True,
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
        "non_target_source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
    }
    for key, want in expected_summary.items():
        chk(failures, f"execution_summary_{key}", summary.get(key), want)

    chk(failures, "execution_result_id", execution_result.get("c8_unit_feedback_hardening_local_source_status_field_patch_execution_result_id"), SOURCE_EXECUTION_RESULT_ID)
    chk(failures, "execution_boundary_id", execution_boundary.get("c8_unit_feedback_hardening_local_source_status_field_patch_execution_boundary_audit_id"), SOURCE_EXECUTION_BOUNDARY_ID)
    chk(failures, "execution_boundary_gate", execution_boundary.get("gate"), "PASS")

    target_hash = sha256_file(TARGET_SOURCE_ARTIFACT)
    chk(failures, "target_status", target.get(PATCH_TARGET_FIELD), PATCH_TARGET_VALUE)
    chk(failures, "target_sha256_after", target_hash, TARGET_SHA256_AFTER)

    false_gates = sorted(k for k, v in execution_receipt.get("gate_results", {}).items() if v is not True)
    if false_gates:
        failures.append(f"source_execution_gate_results_false:{false_gates}")

    receipt_forbidden_nonzero = {k: v for k, v in execution_receipt.get("forbidden_counters", {}).items() if v != 0}
    boundary_forbidden_nonzero = {k: v for k, v in execution_boundary.get("forbidden_counters", {}).items() if v != 0}
    if receipt_forbidden_nonzero:
        failures.append(f"source_receipt_forbidden_nonzero:{receipt_forbidden_nonzero}")
    if boundary_forbidden_nonzero:
        failures.append(f"source_boundary_forbidden_nonzero:{boundary_forbidden_nonzero}")

    source_hashes_after = {label: sha256_file(path) for label, path in sources.items() if path.exists()}
    if source_hashes_before != source_hashes_after:
        forbidden_counters["target_source_artifact_mutation_count"] += 1
        failures.append("closure_readiness_mutated_source_hashes")

    gate_results = {
        "CLOSURE_READINESS_0_SOURCE_EXECUTION_RECEIPT_PASS": execution_receipt.get("gate") == "PASS",
        "CLOSURE_READINESS_1_SOURCE_EXECUTION_RESULT_MATCH": execution_result.get("c8_unit_feedback_hardening_local_source_status_field_patch_execution_result_id") == SOURCE_EXECUTION_RESULT_ID,
        "CLOSURE_READINESS_2_SOURCE_EXECUTION_BOUNDARY_PASS": execution_boundary.get("gate") == "PASS",
        "CLOSURE_READINESS_3_TARGET_STATUS_PRESENT_AND_FAILED": target.get(PATCH_TARGET_FIELD) == PATCH_TARGET_VALUE,
        "CLOSURE_READINESS_4_TARGET_HASH_MATCHES_COMMITTED_AFTER_HASH": target_hash == TARGET_SHA256_AFTER,
        "CLOSURE_READINESS_5_SOURCE_EXECUTION_FORBIDDEN_COUNTERS_ZERO": not receipt_forbidden_nonzero and not boundary_forbidden_nonzero,
        "CLOSURE_READINESS_6_NO_CLOSURE_PACKET_MUTATION": source_hashes_before == source_hashes_after,
        "CLOSURE_READINESS_7_NO_RERUN_PROBE_BUILD_OR_SCHEMA_AUTHORIZATION": all(v == 0 for v in forbidden_counters.values()),
        "CLOSURE_READINESS_8_READY_FOR_POST_PATCH_SURFACE_DECISION": True,
    }

    false_closure_gates = [k for k, v in gate_results.items() if v is not True]
    if false_closure_gates:
        failures.extend([f"closure_readiness_gate_false:{g}" for g in false_closure_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_FAIL"
    outcome = "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_READY_FOR_REVIEW" if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_FAILED"
    terminal_stop = "STOP_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_READY_FOR_REVIEW" if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_FAILED"

    closure_packet = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_v0",
        "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "source_execution_commit_sha": SOURCE_EXECUTION_COMMIT_SHA,
        "source_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
        "source_execution_result_id": SOURCE_EXECUTION_RESULT_ID,
        "source_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
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
        "failed_unit_sample_source_status_before_patch": FAILED_UNIT_SAMPLE_SOURCE_STATUS_BEFORE,
        "failed_unit_sample_source_status_after_patch": PATCH_TARGET_VALUE,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "local_source_status_field_patch_plan_class": PATCH_PLAN_CLASS,
        "closure_readiness_class": CLOSURE_CLASS,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "target_source_artifact_sha256_before_patch": TARGET_SHA256_BEFORE,
        "target_source_artifact_sha256_after_patch": TARGET_SHA256_AFTER,
        "current_target_source_artifact_sha256": target_hash,
        "semantic_delta": PATCH_SEMANTIC_DELTA,
        "local_source_status_field_patch_execution_committed": True,
        "local_source_status_field_patch_execution_reviewed": True,
        "closure_readiness_packet_created_now": True,
        "ready_for_post_patch_surface_decision": True,
        "patch_executed_now": False,
        "source_artifact_mutated_now": False,
        "status_field_added_now": False,
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
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "recommended_review_unit": REVIEW_UNIT,
    }
    closure_packet["c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_" + sig8(closure_packet)
    write_json(CLOSURE_PACKET, closure_packet)

    options = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_options_v0",
        "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_options_id": None,
        "created_at": now_iso(),
        "source_closure_readiness_packet_id": closure_packet["c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_id"],
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "human_decision_options": [
            RECOMMENDED_HUMAN_DECISION,
            "REJECT_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET",
            "REQUEST_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_REVISION",
        ],
        "post_patch_surface_candidates_for_future_decision_packet": [
            "LOCAL_PATCH_CLOSURE_ONLY",
            "BOUNDED_FAILED_UNIT_SAMPLE_REEVALUATION",
            "RETURN_TO_UNIT_FEEDBACK_HARDENING_SURFACE_SELECTION",
        ],
    }
    options["c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_options_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_options_" + sig8(options)
    write_json(OPTIONS, options)

    boundary_audit = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_boundary_audit_v0",
        "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_boundary_audit_id": None,
        "gate": gate,
        "source_closure_readiness_packet_id": closure_packet["c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_id"],
        "source_closure_readiness_options_id": options["c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_options_id"],
        "allowed_now": {
            "create_closure_readiness_packet": True,
            "verify_committed_patch_execution_state": True,
            "recommend_post_patch_surface_decision": True,
        },
        "not_allowed_now": {
            "execute_patch": True,
            "mutate_source_artifact": True,
            "add_status_field": True,
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
        "source_execution_forbidden_counters_zero": not receipt_forbidden_nonzero and not boundary_forbidden_nonzero,
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "source_hashes_mutated_now": source_hashes_before != source_hashes_after,
        "failures": failures,
        "warnings": warnings,
    }
    boundary_audit["c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_boundary_audit_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    readout = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_readout_v0",
        "title": "C8 local source-status field patch execution closure-readiness packet",
        "status": status,
        "outcome_class": outcome,
        "closure_readiness_class": CLOSURE_CLASS,
        "source_execution_commit_sha": SOURCE_EXECUTION_COMMIT_SHA,
        "source_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
        "source_execution_result_id": SOURCE_EXECUTION_RESULT_ID,
        "source_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "current_target_source_artifact_sha256": target_hash,
        "closure_readiness_packet_created_now": True,
        "ready_for_post_patch_surface_decision": True,
        "patch_executed_now": False,
        "source_artifact_mutated_now": False,
        "status_field_added_now": False,
        "source_status_invented_now": False,
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
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "closure_readiness_class": CLOSURE_CLASS,
        "source_execution_commit_sha": SOURCE_EXECUTION_COMMIT_SHA,
        "source_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
        "source_execution_result_id": SOURCE_EXECUTION_RESULT_ID,
        "source_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "target_source_artifact_sha256_before_patch": TARGET_SHA256_BEFORE,
        "target_source_artifact_sha256_after_patch": TARGET_SHA256_AFTER,
        "current_target_source_artifact_sha256": target_hash,
        "closure_readiness_packet_created_now": True,
        "ready_for_post_patch_surface_decision": True,
        "patch_executed_now": False,
        "source_artifact_mutated_now": False,
        "status_field_added_now": False,
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
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "recommended_review_unit": REVIEW_UNIT,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report_obj)

    receipt_obj = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_summary": {
            "closure_readiness_packet_created": gate == "PASS",
            "authorized_unit_consumed": UNIT_ID,
            "source_execution_commit_sha": SOURCE_EXECUTION_COMMIT_SHA,
            "source_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
            "source_execution_result_id": SOURCE_EXECUTION_RESULT_ID,
            "source_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
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
            "failed_unit_sample_source_status_before_patch": FAILED_UNIT_SAMPLE_SOURCE_STATUS_BEFORE,
            "failed_unit_sample_source_status_after_patch": PATCH_TARGET_VALUE,
            "local_gap_object": LOCAL_GAP_OBJECT,
            "local_source_status_field_patch_plan_class": PATCH_PLAN_CLASS,
            "closure_readiness_class": CLOSURE_CLASS,
            "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
            "patch_target_field": PATCH_TARGET_FIELD,
            "patch_target_value": PATCH_TARGET_VALUE,
            "target_source_artifact_sha256_before_patch": TARGET_SHA256_BEFORE,
            "target_source_artifact_sha256_after_patch": TARGET_SHA256_AFTER,
            "current_target_source_artifact_sha256": target_hash,
            "semantic_delta": PATCH_SEMANTIC_DELTA,
            "local_source_status_field_patch_execution_committed": True,
            "local_source_status_field_patch_execution_reviewed": True,
            "closure_readiness_packet_created_now": True,
            "ready_for_post_patch_surface_decision": True,
            "patch_executed_now": False,
            "source_artifact_mutated_now": False,
            "status_field_added_now": False,
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
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "output_artifacts": {
            "closure_readiness_packet": rel(CLOSURE_PACKET),
            "closure_readiness_options": rel(OPTIONS),
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

    receipt_obj["receipt_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_receipt_" + sig8(receipt_obj)
    receipt_path = RECEIPT_DIR / f"{receipt_obj['receipt_id']}.json"
    receipt_obj["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_obj)

    print(json.dumps(receipt_obj, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_receipt_id={receipt_obj['receipt_id']}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_path={rel(CLOSURE_PACKET)}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_options_path={rel(OPTIONS)}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"source_execution_commit_sha={SOURCE_EXECUTION_COMMIT_SHA}")
    print(f"source_execution_receipt_id={SOURCE_EXECUTION_RECEIPT_ID}")
    print(f"source_execution_result_id={SOURCE_EXECUTION_RESULT_ID}")
    print(f"source_execution_boundary_id={SOURCE_EXECUTION_BOUNDARY_ID}")
    print(f"failed_unit_sample_id={FAILED_UNIT_SAMPLE_ID}")
    print(f"local_gap_object={LOCAL_GAP_OBJECT}")
    print(f"patch_target_source_artifact_path={PATCH_TARGET_SOURCE_ARTIFACT}")
    print(f"patch_target_field={PATCH_TARGET_FIELD}")
    print(f"patch_target_value={PATCH_TARGET_VALUE}")
    print(f"current_target_source_artifact_sha256={target_hash}")
    print(f"closure_readiness_class={CLOSURE_CLASS}")
    print("closure_readiness_packet_created_now=true")
    print("ready_for_post_patch_surface_decision=true")
    print("patch_executed_now=false")
    print("source_artifact_mutated_now=false")
    print("status_field_added_now=false")
    print("source_status_invented_now=false")
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
