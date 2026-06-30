#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_FOR_POST_PATCH_SURFACE_DECISION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.local_source_status_field_patch_execution.closure_readiness_packet.acceptance.for_post_patch_surface_decision.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_ACCEPTED_FOR_POST_PATCH_SURFACE_DECISION_AFTER_RUNTIME_ADOPTION_CLOSURE"

SOURCE_CLOSURE_READINESS_COMMIT_SHA = "4df5f80df3856c52812df088e543026e70e68efc"

SOURCE_CLOSURE_RECEIPT_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_receipt_5f8b15fb"
SOURCE_CLOSURE_PACKET_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_fc0907ce"
SOURCE_CLOSURE_OPTIONS_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_options_9a9b1054"
SOURCE_CLOSURE_BOUNDARY_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_boundary_90f89030"

SOURCE_EXECUTION_COMMIT_SHA = "e801c5f7649bfed4b5d3708c94ecccf29499db02"
SOURCE_EXECUTION_RECEIPT_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_once_receipt_13e2733e"
SOURCE_EXECUTION_RESULT_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_result_7d04659d"
SOURCE_EXECUTION_BOUNDARY_ID = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_boundary_044dda6d"

FAILED_UNIT_SAMPLE_ID = "c8_failed_unit_sample_ee4e6092"
FAILED_UNIT_SAMPLE_SOURCE_PATH = "data/a0_current_receipt_chain_frontier_application_v0_receipts/c1d0f615.json"
FAILED_UNIT_SAMPLE_SOURCE_STATUS_BEFORE_PATCH = "MISSING_STATUS_FIELD_WITH_FAILURE_INDICATOR"
FAILED_UNIT_SAMPLE_SOURCE_STATUS_AFTER_PATCH = "FAILED"
LOCAL_GAP_OBJECT = "SOURCE_ARTIFACT_TOP_LEVEL_STATUS_ABSENCE"

PATCH_TARGET_SOURCE_ARTIFACT = FAILED_UNIT_SAMPLE_SOURCE_PATH
PATCH_TARGET_FIELD = "status"
PATCH_TARGET_VALUE = "FAILED"
CURRENT_TARGET_SHA256 = "a2ef7e5ab954f976f44ce49be885f36e7e7999d43bec581a7e65df06af024432"
CLOSURE_READINESS_CLASS = "LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_COMMITTED_REVIEWED_READY_FOR_POST_PATCH_SURFACE_DECISION"

HUMAN_DECISION = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_FOR_POST_PATCH_SURFACE_DECISION"
FUTURE_UNIT = "CREATE_C8_UNIT_FEEDBACK_HARDENING_POST_SOURCE_STATUS_PATCH_SURFACE_DECISION_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
REVIEW_UNIT = "REVIEW_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_ACCEPTANCE_FOR_POST_PATCH_SURFACE_DECISION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_after_runtime_adoption_closure_v0_receipts"

CLOSURE_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_receipt_5f8b15fb.json"
CLOSURE_PACKET = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_v0.json"
CLOSURE_OPTIONS = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_options_v0.json"
CLOSURE_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_boundary_audit_v0.json"
CLOSURE_READOUT = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_readout_v0.json"
CLOSURE_REPORT = ROOT / "data/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_report.json"
TARGET_SOURCE_ARTIFACT = ROOT / PATCH_TARGET_SOURCE_ARTIFACT

DECISION = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_decision_v0.json"
PACKET = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_packet_v0.json"
AUTHORITY = OUT_DIR / "c8_unit_feedback_hardening_post_source_status_patch_surface_decision_authority_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_report.json"

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
    "surface_decision_packet_created_count",
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
        "closure_receipt": CLOSURE_RECEIPT,
        "closure_packet": CLOSURE_PACKET,
        "closure_options": CLOSURE_OPTIONS,
        "closure_boundary": CLOSURE_BOUNDARY,
        "closure_readout": CLOSURE_READOUT,
        "closure_report": CLOSURE_REPORT,
        "target_source_artifact": TARGET_SOURCE_ARTIFACT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {label: sha256_file(path) for label, path in sources.items() if path.exists()}

    closure_receipt = read_json(CLOSURE_RECEIPT)
    closure_packet = read_json(CLOSURE_PACKET)
    closure_options = read_json(CLOSURE_OPTIONS)
    closure_boundary = read_json(CLOSURE_BOUNDARY)
    target = read_json(TARGET_SOURCE_ARTIFACT)
    closure_summary = closure_receipt.get("machine_readable_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_summary", {})

    expected_closure_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_READY_FOR_REVIEW",
        "receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
    }
    for key, want in expected_closure_receipt.items():
        chk(failures, f"source_closure_receipt_{key}", closure_receipt.get(key), want)

    expected_closure_summary = {
        "closure_readiness_packet_created": True,
        "authorized_unit_consumed": "CREATE_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "source_execution_commit_sha": SOURCE_EXECUTION_COMMIT_SHA,
        "source_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
        "source_execution_result_id": SOURCE_EXECUTION_RESULT_ID,
        "source_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "failed_unit_sample_source_status_before_patch": FAILED_UNIT_SAMPLE_SOURCE_STATUS_BEFORE_PATCH,
        "failed_unit_sample_source_status_after_patch": FAILED_UNIT_SAMPLE_SOURCE_STATUS_AFTER_PATCH,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "closure_readiness_class": CLOSURE_READINESS_CLASS,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "current_target_source_artifact_sha256": CURRENT_TARGET_SHA256,
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
        "forbidden_counters_zero": True,
        "requires_review": True,
        "recommended_human_decision": HUMAN_DECISION,
        "if_accepted_authorizes_future_unit": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
    }
    for key, want in expected_closure_summary.items():
        chk(failures, f"source_closure_summary_{key}", closure_summary.get(key), want)

    chk(failures, "source_closure_packet_id", closure_packet.get("c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_id"), SOURCE_CLOSURE_PACKET_ID)
    chk(failures, "source_closure_options_id", closure_options.get("c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_options_id"), SOURCE_CLOSURE_OPTIONS_ID)
    chk(failures, "source_closure_boundary_id", closure_boundary.get("c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_boundary_audit_id"), SOURCE_CLOSURE_BOUNDARY_ID)

    if HUMAN_DECISION not in closure_options.get("human_decision_options", []):
        failures.append("human_decision_not_in_source_options")
    chk(failures, "source_options_recommended_decision", closure_options.get("recommended_human_decision"), HUMAN_DECISION)
    chk(failures, "source_options_future_unit", closure_options.get("if_accepted_authorizes_future_unit"), FUTURE_UNIT)

    target_hash = sha256_file(TARGET_SOURCE_ARTIFACT)
    chk(failures, "target_status", target.get(PATCH_TARGET_FIELD), PATCH_TARGET_VALUE)
    chk(failures, "target_hash", target_hash, CURRENT_TARGET_SHA256)

    false_source_gates = sorted(k for k, v in closure_receipt.get("gate_results", {}).items() if v is not True)
    if false_source_gates:
        failures.append(f"source_closure_gate_results_false:{false_source_gates}")

    source_forbidden_nonzero = {k: v for k, v in closure_receipt.get("forbidden_counters", {}).items() if v != 0}
    boundary_forbidden_nonzero = {k: v for k, v in closure_boundary.get("forbidden_counters", {}).items() if v != 0}
    if source_forbidden_nonzero:
        failures.append(f"source_closure_forbidden_nonzero:{source_forbidden_nonzero}")
    if boundary_forbidden_nonzero:
        failures.append(f"source_boundary_forbidden_nonzero:{boundary_forbidden_nonzero}")

    source_hashes_after = {label: sha256_file(path) for label, path in sources.items() if path.exists()}
    if source_hashes_before != source_hashes_after:
        forbidden_counters["target_source_artifact_mutation_count"] += 1
        failures.append("acceptance_mutated_source_hashes")

    gate_results = {
        "POST_PATCH_SURFACE_DECISION_ACCEPTANCE_0_SOURCE_CLOSURE_READINESS_RECEIPT_PASS": closure_receipt.get("gate") == "PASS",
        "POST_PATCH_SURFACE_DECISION_ACCEPTANCE_1_HUMAN_DECISION_MATCHES_OPTIONS": HUMAN_DECISION in closure_options.get("human_decision_options", []),
        "POST_PATCH_SURFACE_DECISION_ACCEPTANCE_2_FUTURE_UNIT_MATCH": closure_options.get("if_accepted_authorizes_future_unit") == FUTURE_UNIT,
        "POST_PATCH_SURFACE_DECISION_ACCEPTANCE_3_TARGET_STATUS_STILL_FAILED": target.get(PATCH_TARGET_FIELD) == PATCH_TARGET_VALUE,
        "POST_PATCH_SURFACE_DECISION_ACCEPTANCE_4_TARGET_HASH_STABLE": target_hash == CURRENT_TARGET_SHA256,
        "POST_PATCH_SURFACE_DECISION_ACCEPTANCE_5_NO_SOURCE_MUTATION": source_hashes_before == source_hashes_after,
        "POST_PATCH_SURFACE_DECISION_ACCEPTANCE_6_NO_SURFACE_DECISION_PACKET_CREATED_NOW": forbidden_counters["surface_decision_packet_created_count"] == 0,
        "POST_PATCH_SURFACE_DECISION_ACCEPTANCE_7_NO_RERUN_PROBE_BUILD_SCHEMA_OR_MUTATION": all(v == 0 for v in forbidden_counters.values()),
        "POST_PATCH_SURFACE_DECISION_ACCEPTANCE_8_REQUIRES_REVIEW": True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"post_patch_surface_decision_acceptance_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_ACCEPTANCE_FOR_POST_PATCH_SURFACE_DECISION_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_ACCEPTANCE_FOR_POST_PATCH_SURFACE_DECISION_FAIL"
    outcome = "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_ACCEPTED_FOR_POST_PATCH_SURFACE_DECISION" if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_ACCEPTANCE_FOR_POST_PATCH_SURFACE_DECISION_FAILED"
    terminal_stop = "STOP_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_ACCEPTANCE_FOR_POST_PATCH_SURFACE_DECISION_READY_FOR_REVIEW" if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_ACCEPTANCE_FOR_POST_PATCH_SURFACE_DECISION_FAILED"

    decision = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_decision_v0",
        "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_decision_id": None,
        "created_at": now_iso(),
        "human_decision": HUMAN_DECISION,
        "human_decision_consumed": True,
        "source_closure_readiness_commit_sha": SOURCE_CLOSURE_READINESS_COMMIT_SHA,
        "source_closure_readiness_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "source_closure_readiness_packet_id": SOURCE_CLOSURE_PACKET_ID,
        "source_closure_readiness_options_id": SOURCE_CLOSURE_OPTIONS_ID,
        "source_closure_readiness_boundary_id": SOURCE_CLOSURE_BOUNDARY_ID,
        "source_execution_commit_sha": SOURCE_EXECUTION_COMMIT_SHA,
        "source_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
        "source_execution_result_id": SOURCE_EXECUTION_RESULT_ID,
        "source_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "failed_unit_sample_source_status_after_patch": FAILED_UNIT_SAMPLE_SOURCE_STATUS_AFTER_PATCH,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "closure_readiness_class": CLOSURE_READINESS_CLASS,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "current_target_source_artifact_sha256": target_hash,
        "closure_readiness_packet_accepted_for_post_patch_surface_decision": True,
        "authorized_future_unit_after_review": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "surface_decision_packet_created_now": False,
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
        "recommended_review_unit": REVIEW_UNIT,
    }
    decision["c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_decision_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_decision_" + sig8(decision)
    write_json(DECISION, decision)

    authority = {
        "schema_version": "c8_unit_feedback_hardening_post_source_status_patch_surface_decision_authority_v0",
        "c8_unit_feedback_hardening_post_source_status_patch_surface_decision_authority_id": None,
        "created_at": now_iso(),
        "source_acceptance_decision_id": decision["c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_decision_id"],
        "source_closure_readiness_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "source_closure_readiness_packet_id": SOURCE_CLOSURE_PACKET_ID,
        "source_closure_readiness_options_id": SOURCE_CLOSURE_OPTIONS_ID,
        "source_closure_readiness_boundary_id": SOURCE_CLOSURE_BOUNDARY_ID,
        "authorized_future_unit": FUTURE_UNIT,
        "authorized_future_unit_count": 1,
        "authority_status": "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "authority_scope": {
            "may_create_post_source_status_patch_surface_decision_packet_after_review_and_commit": True,
            "may_create_surface_decision_packet_now": False,
            "may_execute_patch": False,
            "may_mutate_source_artifact": False,
            "may_add_status_field": False,
            "may_invent_source_status": False,
            "may_authorize_reusable_schema": False,
            "may_execute_additional_sample_discovery": False,
            "may_authorize_probe_execution": False,
            "may_execute_probe": False,
            "may_build": False,
            "may_rerun_c8": False,
        },
    }
    authority["c8_unit_feedback_hardening_post_source_status_patch_surface_decision_authority_id"] = "c8_unit_feedback_hardening_post_source_status_patch_surface_decision_authority_" + sig8(authority)
    write_json(AUTHORITY, authority)

    packet = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_packet_v0",
        "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_packet_id": None,
        "created_at": now_iso(),
        "source_acceptance_decision_id": decision["c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_decision_id"],
        "source_post_patch_surface_decision_authority_id": authority["c8_unit_feedback_hardening_post_source_status_patch_surface_decision_authority_id"],
        "human_decision": HUMAN_DECISION,
        "source_closure_readiness_commit_sha": SOURCE_CLOSURE_READINESS_COMMIT_SHA,
        "source_closure_readiness_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "source_closure_readiness_packet_id": SOURCE_CLOSURE_PACKET_ID,
        "source_closure_readiness_options_id": SOURCE_CLOSURE_OPTIONS_ID,
        "source_closure_readiness_boundary_id": SOURCE_CLOSURE_BOUNDARY_ID,
        "source_execution_commit_sha": SOURCE_EXECUTION_COMMIT_SHA,
        "source_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
        "source_execution_result_id": SOURCE_EXECUTION_RESULT_ID,
        "source_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
        "failed_unit_sample_source_status_after_patch": FAILED_UNIT_SAMPLE_SOURCE_STATUS_AFTER_PATCH,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "closure_readiness_class": CLOSURE_READINESS_CLASS,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "current_target_source_artifact_sha256": target_hash,
        "acceptance_status": outcome,
        "closure_readiness_packet_accepted_for_post_patch_surface_decision": True,
        "authorized_future_unit_after_review": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "surface_decision_packet_created_now": False,
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
        "recommended_review_unit": REVIEW_UNIT,
    }
    packet["c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_packet_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_packet_" + sig8(packet)
    write_json(PACKET, packet)

    boundary_audit = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_boundary_audit_v0",
        "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_boundary_audit_id": None,
        "gate": gate,
        "source_acceptance_decision_id": decision["c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_decision_id"],
        "source_acceptance_packet_id": packet["c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_packet_id"],
        "source_post_patch_surface_decision_authority_id": authority["c8_unit_feedback_hardening_post_source_status_patch_surface_decision_authority_id"],
        "allowed_now": {
            "accept_closure_readiness_packet_for_post_patch_surface_decision": True,
            "authorize_post_patch_surface_decision_packet_after_review_and_commit": True,
        },
        "not_allowed_now": {
            "create_post_patch_surface_decision_packet_now": True,
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
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "source_hashes_mutated_now": source_hashes_before != source_hashes_after,
        "failures": failures,
        "warnings": warnings,
    }
    boundary_audit["c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_boundary_audit_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_boundary_" + sig8(boundary_audit)
    write_json(BOUNDARY_AUDIT, boundary_audit)

    readout = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_readout_v0",
        "title": "C8 closure-readiness packet acceptance for post-patch surface decision",
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "source_closure_readiness_commit_sha": SOURCE_CLOSURE_READINESS_COMMIT_SHA,
        "source_closure_readiness_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "source_closure_readiness_packet_id": SOURCE_CLOSURE_PACKET_ID,
        "source_post_patch_surface_decision_authority_id": authority["c8_unit_feedback_hardening_post_source_status_patch_surface_decision_authority_id"],
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "current_target_source_artifact_sha256": target_hash,
        "closure_readiness_packet_accepted_for_post_patch_surface_decision": True,
        "authorized_future_unit_after_review": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "surface_decision_packet_created_now": False,
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
        "recommended_review_unit": REVIEW_UNIT,
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "human_decision": HUMAN_DECISION,
        "source_closure_readiness_commit_sha": SOURCE_CLOSURE_READINESS_COMMIT_SHA,
        "source_closure_readiness_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
        "source_closure_readiness_packet_id": SOURCE_CLOSURE_PACKET_ID,
        "source_closure_readiness_options_id": SOURCE_CLOSURE_OPTIONS_ID,
        "source_closure_readiness_boundary_id": SOURCE_CLOSURE_BOUNDARY_ID,
        "source_post_patch_surface_decision_authority_id": authority["c8_unit_feedback_hardening_post_source_status_patch_surface_decision_authority_id"],
        "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
        "local_gap_object": LOCAL_GAP_OBJECT,
        "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
        "patch_target_field": PATCH_TARGET_FIELD,
        "patch_target_value": PATCH_TARGET_VALUE,
        "current_target_source_artifact_sha256": target_hash,
        "closure_readiness_packet_accepted_for_post_patch_surface_decision": True,
        "authorized_future_unit_after_review": FUTURE_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "surface_decision_packet_created_now": False,
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
        "recommended_review_unit": REVIEW_UNIT,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_LOCAL_SOURCE_STATUS_FIELD_PATCH_EXECUTION_CLOSURE_READINESS_PACKET_ACCEPTANCE_FOR_POST_PATCH_SURFACE_DECISION_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_summary": {
            "closure_readiness_packet_acceptance_complete": gate == "PASS",
            "authorized_unit_consumed": UNIT_ID,
            "human_decision": HUMAN_DECISION,
            "source_closure_readiness_commit_sha": SOURCE_CLOSURE_READINESS_COMMIT_SHA,
            "source_closure_readiness_receipt_id": SOURCE_CLOSURE_RECEIPT_ID,
            "source_closure_readiness_packet_id": SOURCE_CLOSURE_PACKET_ID,
            "source_closure_readiness_options_id": SOURCE_CLOSURE_OPTIONS_ID,
            "source_closure_readiness_boundary_id": SOURCE_CLOSURE_BOUNDARY_ID,
            "source_execution_commit_sha": SOURCE_EXECUTION_COMMIT_SHA,
            "source_execution_receipt_id": SOURCE_EXECUTION_RECEIPT_ID,
            "source_execution_result_id": SOURCE_EXECUTION_RESULT_ID,
            "source_execution_boundary_id": SOURCE_EXECUTION_BOUNDARY_ID,
            "failed_unit_sample_id": FAILED_UNIT_SAMPLE_ID,
            "failed_unit_sample_source_path": FAILED_UNIT_SAMPLE_SOURCE_PATH,
            "failed_unit_sample_source_status_after_patch": FAILED_UNIT_SAMPLE_SOURCE_STATUS_AFTER_PATCH,
            "local_gap_object": LOCAL_GAP_OBJECT,
            "closure_readiness_class": CLOSURE_READINESS_CLASS,
            "patch_target_source_artifact_path": PATCH_TARGET_SOURCE_ARTIFACT,
            "patch_target_field": PATCH_TARGET_FIELD,
            "patch_target_value": PATCH_TARGET_VALUE,
            "current_target_source_artifact_sha256": target_hash,
            "closure_readiness_packet_accepted_for_post_patch_surface_decision": True,
            "authorized_future_unit_after_review": FUTURE_UNIT,
            "authorized_future_unit_count_after_review": 1,
            "surface_decision_packet_created_now": False,
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
            "recommended_review_unit": REVIEW_UNIT,
            "next_command_goal": None,
        },
        "gate_results": gate_results,
        "forbidden_counters": forbidden_counters,
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "output_artifacts": {
            "decision": rel(DECISION),
            "packet": rel(PACKET),
            "authority": rel(AUTHORITY),
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

    receipt["receipt_id"] = "c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_receipt_id={receipt['receipt_id']}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_decision_path={rel(DECISION)}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_packet_path={rel(PACKET)}")
    print(f"c8_unit_feedback_hardening_post_source_status_patch_surface_decision_authority_path={rel(AUTHORITY)}")
    print(f"c8_unit_feedback_hardening_local_source_status_field_patch_execution_closure_readiness_packet_acceptance_for_post_patch_surface_decision_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"human_decision={HUMAN_DECISION}")
    print(f"source_closure_readiness_commit_sha={SOURCE_CLOSURE_READINESS_COMMIT_SHA}")
    print(f"source_closure_readiness_receipt_id={SOURCE_CLOSURE_RECEIPT_ID}")
    print(f"source_closure_readiness_packet_id={SOURCE_CLOSURE_PACKET_ID}")
    print(f"source_closure_readiness_options_id={SOURCE_CLOSURE_OPTIONS_ID}")
    print(f"source_closure_readiness_boundary_id={SOURCE_CLOSURE_BOUNDARY_ID}")
    print(f"failed_unit_sample_id={FAILED_UNIT_SAMPLE_ID}")
    print(f"patch_target_source_artifact_path={PATCH_TARGET_SOURCE_ARTIFACT}")
    print(f"patch_target_field={PATCH_TARGET_FIELD}")
    print(f"patch_target_value={PATCH_TARGET_VALUE}")
    print(f"current_target_source_artifact_sha256={target_hash}")
    print("closure_readiness_packet_accepted_for_post_patch_surface_decision=true")
    print(f"authorized_future_unit_after_review={FUTURE_UNIT}")
    print("authorized_future_unit_count_after_review=1")
    print("surface_decision_packet_created_now=false")
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
    print(f"recommended_review_unit={REVIEW_UNIT}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
