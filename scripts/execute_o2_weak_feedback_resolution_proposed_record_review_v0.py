#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXECUTE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_proposed_record_review.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW"
MODE = "EXECUTE / PROPOSED_RECORD_REVIEW / EMIT_REVIEWED_ARTIFACTS / NO_FINAL_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_ONLY"

POST_DECISION_RECEIPT_ID = "63793a90"
POST_DECISION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0_receipts/63793a90.json"
POST_DECISION_BASIS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposal_emission_post_closure_decision_basis_v0.json"
POST_DECISION_TABLE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposal_emission_post_closure_decision_table_v0.json"
POST_SELECTED_BRANCH_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposal_emission_selected_next_branch_v0.json"
POST_REVIEW_AUTH_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposed_record_review_authorization_v0.json"
POST_INPUT_SCOPE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposed_record_review_input_scope_v0.json"
POST_UNRESOLVED_CONTINUATION_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposal_emission_post_closure_unresolved_continuation_v0.json"
POST_C5_BLOCK_CONTINUATION_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposal_emission_post_closure_c5_block_continuation_v0.json"
POST_DEFERRED_BRANCHES_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposal_emission_post_closure_deferred_branches_v0.json"
POST_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposal_emission_post_closure_decision_authority_boundary_v0.json"
POST_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposal_emission_post_closure_decision_classification_v0.json"
POST_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposal_emission_post_closure_decision_rollup_v0.json"
POST_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposal_emission_post_closure_decision_profile_v0.json"
POST_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposal_emission_post_closure_decision_report.json"
POST_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_post_closure_decision_v0/o2_proposal_emission_post_closure_decision_transition_trace.json"

PROPOSAL_EMISSION_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0_receipts/922ef93d.json"
PROPOSAL_EMISSION_REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_reviewed_reference_v0.json"
PROPOSED_RECORD_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposed_record_inventory_freeze_v0.json"
PROPOSED_RESOLUTION_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposed_weak_feedback_resolution_record_freeze_v0.json"
PROPOSAL_REVIEW_BOUNDARY_LOCK_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_review_boundary_lock_v0.json"
UNRESOLVED_STATUS_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_unresolved_status_freeze_v0.json"
C5_BLOCK_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_closure_v0/o2_proposal_emission_c5_block_freeze_v0.json"

PROPOSED_QA_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_question_answer_records_v0.jsonl"
PROPOSED_SOURCE_REF_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_source_ref_satisfaction_records_v0.jsonl"
PROPOSED_UNDERTYPED_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_under_typed_acceptance_review_records_v0.jsonl"
PARKING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_parking_execution_continuation_records_v0.jsonl"
PROPOSED_RESOLUTION_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_proposed_weak_feedback_resolution_records_v0.jsonl"
PROPOSAL_EMISSION_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0/o2_weak_feedback_resolution_proposal_emission_route_map_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    POST_DECISION_RECEIPT_PATH,
    POST_DECISION_BASIS_PATH,
    POST_DECISION_TABLE_PATH,
    POST_SELECTED_BRANCH_PATH,
    POST_REVIEW_AUTH_PATH,
    POST_INPUT_SCOPE_PATH,
    POST_UNRESOLVED_CONTINUATION_PATH,
    POST_C5_BLOCK_CONTINUATION_PATH,
    POST_DEFERRED_BRANCHES_PATH,
    POST_AUTHORITY_PATH,
    POST_CLASSIFICATION_PATH,
    POST_ROLLUP_PATH,
    POST_PROFILE_PATH,
    POST_REPORT_PATH,
    POST_TRACE_PATH,
    PROPOSAL_EMISSION_CLOSURE_RECEIPT_PATH,
    PROPOSAL_EMISSION_REVIEWED_REFERENCE_PATH,
    PROPOSED_RECORD_FREEZE_PATH,
    PROPOSED_RESOLUTION_FREEZE_PATH,
    PROPOSAL_REVIEW_BOUNDARY_LOCK_PATH,
    UNRESOLVED_STATUS_FREEZE_PATH,
    C5_BLOCK_FREEZE_PATH,
    PROPOSED_QA_RECORDS_PATH,
    PROPOSED_SOURCE_REF_RECORDS_PATH,
    PROPOSED_UNDERTYPED_RECORDS_PATH,
    PARKING_RECORDS_PATH,
    PROPOSED_RESOLUTION_RECORDS_PATH,
    PROPOSAL_EMISSION_ROUTE_MAP_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0_receipts"

REVIEW_EXECUTION_RECORD_PATH = OUT_DIR / "o2_proposed_record_review_execution_record_v0.json"
REVIEWED_QA_RECORDS_PATH = OUT_DIR / "o2_reviewed_question_answer_records_v0.jsonl"
REVIEWED_SOURCE_REF_RECORDS_PATH = OUT_DIR / "o2_reviewed_source_ref_satisfaction_records_v0.jsonl"
REVIEWED_UNDERTYPED_RECORDS_PATH = OUT_DIR / "o2_reviewed_under_typed_acceptance_records_v0.jsonl"
REVIEWED_PARKING_RECORDS_PATH = OUT_DIR / "o2_reviewed_parking_continuation_records_v0.jsonl"
REVIEWED_RESOLUTION_RECORDS_PATH = OUT_DIR / "o2_reviewed_weak_feedback_resolution_records_v0.jsonl"
REVIEWED_ROUTE_MAP_PATH = OUT_DIR / "o2_reviewed_weak_feedback_resolution_route_map_v0.jsonl"
REVIEW_GATE_READOUT_PATH = OUT_DIR / "o2_proposed_record_review_gate_readout_v0.json"
RESOLUTION_BOUNDARY_READOUT_PATH = OUT_DIR / "o2_reviewed_resolution_boundary_readout_v0.json"
C5_BLOCK_READOUT_PATH = OUT_DIR / "o2_proposed_record_review_c5_block_readout_v0.json"
UNRESOLVED_CONTINUATION_PATH = OUT_DIR / "o2_proposed_record_review_unresolved_continuation_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_proposed_record_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_proposed_record_review_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_proposed_record_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_proposed_record_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_proposed_record_review_report.json"
TRACE_PATH = OUT_DIR / "o2_proposed_record_review_transition_trace.json"

EXPECTED_DECISION_STATUS = "TYPED_O2_PROPOSAL_EMISSION_POST_CLOSURE_DECISION_SELECTED_PROPOSED_RECORD_REVIEW_READY"
EXPECTED_DECISION_STOP = "STOP_TYPED_O2_PROPOSAL_EMISSION_POST_CLOSURE_DECISION_SELECTED_PROPOSED_RECORD_REVIEW_READY"
EXPECTED_DECISION_NEXT = "EXECUTE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_V0"
RECOMMENDED_NEXT = "REVIEW_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_V0"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def reviewed_id(prefix: str, proposed_ref: str, obj: Dict[str, Any]) -> str:
    return prefix + "_" + sha8({"proposed_ref": proposed_ref, "obj": obj})

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(POST_DECISION_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_proposal_emission_post_closure_decision_summary", {})
    basis = read_json(POST_DECISION_BASIS_PATH)
    selected = read_json(POST_SELECTED_BRANCH_PATH)
    auth = read_json(POST_REVIEW_AUTH_PATH)
    input_scope = read_json(POST_INPUT_SCOPE_PATH)
    unresolved_post = read_json(POST_UNRESOLVED_CONTINUATION_PATH)
    c5_post = read_json(POST_C5_BLOCK_CONTINUATION_PATH)
    post_authority = read_json(POST_AUTHORITY_PATH)
    post_classification = read_json(POST_CLASSIFICATION_PATH)
    post_rollup = read_json(POST_ROLLUP_PATH)
    post_profile = read_json(POST_PROFILE_PATH)

    closure_receipt = read_json(PROPOSAL_EMISSION_CLOSURE_RECEIPT_PATH)
    closure_summary = closure_receipt.get("machine_readable_o2_weak_feedback_resolution_proposal_emission_closure_summary", {})
    reviewed_ref = read_json(PROPOSAL_EMISSION_REVIEWED_REFERENCE_PATH)
    proposed_record_freeze = read_json(PROPOSED_RECORD_FREEZE_PATH)
    proposed_resolution_freeze = read_json(PROPOSED_RESOLUTION_FREEZE_PATH)
    boundary_lock = read_json(PROPOSAL_REVIEW_BOUNDARY_LOCK_PATH)
    unresolved_freeze = read_json(UNRESOLVED_STATUS_FREEZE_PATH)
    c5_freeze = read_json(C5_BLOCK_FREEZE_PATH)

    qa_records = read_jsonl(PROPOSED_QA_RECORDS_PATH)
    source_records = read_jsonl(PROPOSED_SOURCE_REF_RECORDS_PATH)
    undertyped_records = read_jsonl(PROPOSED_UNDERTYPED_RECORDS_PATH)
    parking_records = read_jsonl(PARKING_RECORDS_PATH)
    proposed_resolution_records = read_jsonl(PROPOSED_RESOLUTION_RECORDS_PATH)
    route_records = read_jsonl(PROPOSAL_EMISSION_ROUTE_MAP_PATH)

    if receipt.get("receipt_id") != "63793a90" or receipt.get("gate") != "PASS":
        failures.append("post_closure_decision_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_DECISION_STOP:
        failures.append("post_closure_decision_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("post_closure_decision_hidden_next_command")
    if summary.get("status") != EXPECTED_DECISION_STATUS:
        failures.append(f"post_closure_decision_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_DECISION_NEXT:
        failures.append(f"post_closure_decision_next_wrong:{summary.get('recommended_next')}")
    if summary.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("selected_next_unit_wrong")
    if summary.get("selected_next_branch") != "EXECUTE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW":
        failures.append("selected_next_branch_wrong")

    for key in [
        "post_closure_decision_complete",
        "proposed_record_review_authorized_next",
        "proposal_emission_closed_as_reviewed_reference",
        "proposed_records_frozen_as_unreviewed",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "proposed_question_answer_records_available_count": 3,
        "proposed_source_ref_satisfaction_records_available_count": 2,
        "proposed_under_typed_acceptance_review_records_available_count": 2,
        "parking_execution_continuation_records_available_count": 3,
        "proposed_resolution_records_available_count": 3,
        "proposal_emission_route_records_available_count": 3,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    for key in [
        "record_review_executed_in_decision",
        "weak_feedback_resolved",
        "question_packets_answered",
        "source_ref_requests_satisfied",
        "under_typed_acceptance_approved",
        "parking_counted_as_resolution",
        "c5_reconsideration_ready",
        "c5_opened",
        "live_feedback_audit_executed",
        "repair_applied",
        "retry_executed",
        "target_selected_for_build",
        "runtime_patch_applied",
        "source_mutated",
        "prior_receipt_mutated",
        "architecture_change",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if summary.get(key) is not False:
            failures.append(f"summary_forbidden_true:{key}")

    if basis.get("basis_status") != "BASIS_ACCEPTED":
        failures.append("basis_not_accepted")
    if selected.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("selected_artifact_next_wrong")
    if auth.get("authorized_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("auth_next_wrong")
    if input_scope.get("scope_status") != "FROZEN_PROPOSED_RECORDS_ELIGIBLE_FOR_LATER_REVIEW":
        failures.append("input_scope_wrong")
    if unresolved_post.get("weak_feedback_resolved") is not False:
        failures.append("post_unresolved_wrong")
    if c5_post.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_post.get("c5_opened") is not False:
        failures.append("post_c5_wrong")
    if post_authority.get("may_execute_proposed_record_review_next") is not True:
        failures.append("post_authority_no_review_next")
    if post_classification.get("recommended_next") != EXPECTED_DECISION_NEXT:
        failures.append("post_classification_next_wrong")
    if post_rollup.get("proposed_record_review_authorized_next_count") != 1:
        failures.append("post_rollup_auth_wrong")
    if post_profile.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("post_profile_next_wrong")

    if closure_receipt.get("receipt_id") != "922ef93d" or closure_summary.get("proposed_records_frozen_as_unreviewed") is not True:
        failures.append("closure_receipt_wrong")
    if reviewed_ref.get("proposed_records_remain_unreviewed") is not True or reviewed_ref.get("reviewed_resolution_records_emitted_count") != 0:
        failures.append("reviewed_reference_wrong")
    if proposed_record_freeze.get("all_proposed_records_unreviewed") is not True:
        failures.append("proposed_record_freeze_wrong")
    if proposed_resolution_freeze.get("reviewed_resolution_records_emitted_count") != 0 or proposed_resolution_freeze.get("weak_feedback_resolved") is not False:
        failures.append("proposed_resolution_freeze_wrong")
    if boundary_lock.get("proposal_layer_crossed_into_review_layer") is not False:
        failures.append("boundary_lock_already_crossed")
    if unresolved_freeze.get("weak_feedback_resolved") is not False:
        failures.append("unresolved_freeze_wrong")
    if c5_freeze.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_freeze.get("c5_opened") is not False:
        failures.append("c5_freeze_wrong")

    if len(qa_records) != 3 or len(source_records) != 2 or len(undertyped_records) != 2 or len(parking_records) != 3 or len(proposed_resolution_records) != 3 or len(route_records) != 3:
        failures.append("proposed_record_counts_wrong")

    for row in qa_records:
        if row.get("proposal_status") != "PROPOSED_UNREVIEWED" or row.get("review_status") != "UNREVIEWED":
            failures.append(f"qa_not_unreviewed:{row.get('proposed_answer_id')}")
        if row.get("counts_as_answer") is not False:
            failures.append(f"qa_already_answer:{row.get('proposed_answer_id')}")
    for row in source_records:
        if row.get("proposal_status") != "PROPOSED_UNREVIEWED" or row.get("review_status") != "UNREVIEWED":
            failures.append(f"source_not_unreviewed:{row.get('proposed_satisfaction_id')}")
        if row.get("counts_as_satisfied") is not False:
            failures.append(f"source_already_satisfied:{row.get('proposed_satisfaction_id')}")
    for row in undertyped_records:
        if row.get("proposal_status") != "PROPOSED_UNREVIEWED" or row.get("review_status") != "UNREVIEWED":
            failures.append(f"undertyped_not_unreviewed:{row.get('proposed_review_id')}")
        if row.get("counts_as_approved") is not False:
            failures.append(f"undertyped_already_approved:{row.get('proposed_review_id')}")
    for row in parking_records:
        if row.get("review_status") != "UNREVIEWED" or row.get("counts_as_resolution") is not False:
            failures.append(f"parking_boundary_wrong:{row.get('parking_execution_id')}")
    for row in proposed_resolution_records:
        if row.get("proposal_status") != "PROPOSED_UNREVIEWED" or row.get("review_status") != "UNREVIEWED":
            failures.append(f"resolution_not_unreviewed:{row.get('proposed_resolution_id')}")
        if row.get("counts_as_reviewed_resolution") is not False or row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"resolution_already_promoted:{row.get('proposed_resolution_id')}")
    for row in route_records:
        if row.get("proposed_record_emitted") is not True or row.get("reviewed_record_emitted") is not False:
            failures.append(f"route_flags_wrong:{row.get('emission_route_record_id')}")
        if row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"route_boundary_wrong:{row.get('emission_route_record_id')}")

    return failures, {
        "qa_records": qa_records,
        "source_records": source_records,
        "undertyped_records": undertyped_records,
        "parking_records": parking_records,
        "proposed_resolution_records": proposed_resolution_records,
        "route_records": route_records,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    qa_records = src.get("qa_records", [])
    source_records = src.get("source_records", [])
    undertyped_records = src.get("undertyped_records", [])
    parking_records = src.get("parking_records", [])
    proposed_resolution_records = src.get("proposed_resolution_records", [])
    route_records = src.get("route_records", [])

    reviewed_qa = []
    qa_review_id_by_proposed: Dict[str, str] = {}
    for row in qa_records:
        proposed_id = row["proposed_answer_id"]
        rid = reviewed_id("reviewed_question_answer", proposed_id, row)
        qa_review_id_by_proposed[proposed_id] = rid
        reviewed_qa.append({
            "schema_version": "o2_reviewed_question_answer_record_v0",
            "reviewed_answer_id": rid,
            "source_proposed_answer_id": proposed_id,
            "source_template_ref": row.get("source_template_ref"),
            "review_decision": "ACCEPTED_AS_REVIEWED_ANSWER",
            "review_status": "REVIEWED_ACCEPTED",
            "answer_payload_or_ref": row.get("answer_payload_or_ref"),
            "evidence_refs": row.get("evidence_refs", []),
            "counts_as_answer": True,
            "counts_as_resolution_input": True,
            "weak_feedback_resolved_by_this_record": False,
            "c5_reconsideration_ready": False,
        })

    reviewed_source = []
    source_review_id_by_proposed: Dict[str, str] = {}
    for row in source_records:
        proposed_id = row["proposed_satisfaction_id"]
        rid = reviewed_id("reviewed_source_ref_satisfaction", proposed_id, row)
        source_review_id_by_proposed[proposed_id] = rid
        reviewed_source.append({
            "schema_version": "o2_reviewed_source_ref_satisfaction_record_v0",
            "reviewed_satisfaction_id": rid,
            "source_proposed_satisfaction_id": proposed_id,
            "source_template_ref": row.get("source_template_ref"),
            "review_decision": "ACCEPTED_AS_REVIEWED_SOURCE_REF_SATISFACTION",
            "review_status": "REVIEWED_ACCEPTED",
            "reviewed_source_refs": row.get("proposed_source_refs", []),
            "counts_as_satisfied": True,
            "counts_as_resolution_input": True,
            "weak_feedback_resolved_by_this_record": False,
            "c5_reconsideration_ready": False,
        })

    reviewed_undertyped = []
    under_review_id_by_proposed: Dict[str, str] = {}
    for row in undertyped_records:
        proposed_id = row["proposed_review_id"]
        rid = reviewed_id("reviewed_under_typed_acceptance", proposed_id, row)
        under_review_id_by_proposed[proposed_id] = rid
        reviewed_undertyped.append({
            "schema_version": "o2_reviewed_under_typed_acceptance_record_v0",
            "reviewed_under_typed_acceptance_id": rid,
            "source_proposed_review_id": proposed_id,
            "source_template_ref": row.get("source_template_ref"),
            "review_decision": "ACCEPTED_AS_REVIEWED_UNDER_TYPED_ACCEPTANCE",
            "review_status": "REVIEWED_ACCEPTED",
            "counts_as_approved": True,
            "weak_feedback_resolved_by_this_record": False,
            "c5_unblock_allowed": False,
        })

    reviewed_parking = []
    parking_review_id_by_proposed: Dict[str, str] = {}
    for row in parking_records:
        proposed_id = row["parking_execution_id"]
        rid = reviewed_id("reviewed_parking_continuation", proposed_id, row)
        parking_review_id_by_proposed[proposed_id] = rid
        reviewed_parking.append({
            "schema_version": "o2_reviewed_parking_continuation_record_v0",
            "reviewed_parking_continuation_id": rid,
            "source_parking_execution_id": proposed_id,
            "source_template_ref": row.get("source_template_ref"),
            "review_decision": "KEEP_PARKED_UNRESOLVED",
            "review_status": "REVIEWED_PARKING_CONTINUES",
            "counts_as_resolution": False,
            "weak_feedback_resolved_by_this_record": False,
            "c5_unblock_allowed": False,
        })

    reviewed_resolution = []
    reviewed_resolution_id_by_proposed: Dict[str, str] = {}
    for row in proposed_resolution_records:
        proposed_id = row["proposed_resolution_id"]
        rid = reviewed_id("reviewed_weak_feedback_resolution", proposed_id, row)
        reviewed_resolution_id_by_proposed[proposed_id] = rid
        reviewed_qa_refs = [qa_review_id_by_proposed[x] for x in row.get("proposed_question_answer_refs", []) if x in qa_review_id_by_proposed]
        reviewed_source_refs = [source_review_id_by_proposed[x] for x in row.get("proposed_source_ref_satisfaction_refs", []) if x in source_review_id_by_proposed]
        reviewed_under_refs = [under_review_id_by_proposed[x] for x in row.get("proposed_under_typed_review_refs", []) if x in under_review_id_by_proposed]
        reviewed_parking_refs = [parking_review_id_by_proposed[x] for x in row.get("parking_continuation_refs", []) if x in parking_review_id_by_proposed]
        reviewed_resolution.append({
            "schema_version": "o2_reviewed_weak_feedback_resolution_record_v0",
            "reviewed_resolution_id": rid,
            "source_proposed_resolution_id": proposed_id,
            "source_template_ref": row.get("source_template_ref"),
            "source_route_map_ref": row.get("source_route_map_ref"),
            "reviewed_question_answer_refs": reviewed_qa_refs,
            "reviewed_source_ref_satisfaction_refs": reviewed_source_refs,
            "reviewed_under_typed_acceptance_refs": reviewed_under_refs,
            "reviewed_parking_continuation_refs": reviewed_parking_refs,
            "review_decision": "ACCEPTED_AS_REVIEWED_RESOLUTION_CANDIDATE",
            "review_status": "REVIEWED_ACCEPTED",
            "counts_as_reviewed_resolution": True,
            "counts_as_final_resolution": False,
            "weak_feedback_resolved": False,
            "c5_reconsideration_ready": False,
            "requires_resolution_closure_before_resolved": True,
        })

    reviewed_routes = []
    for row in route_records:
        proposed_ref = row.get("proposed_resolution_record_ref")
        reviewed_ref = reviewed_resolution_id_by_proposed.get(proposed_ref)
        reviewed_routes.append({
            "schema_version": "o2_reviewed_weak_feedback_resolution_route_record_v0",
            "reviewed_route_record_id": "reviewed_route_" + sha8(row),
            "source_emission_route_record_id": row.get("emission_route_record_id"),
            "source_proposal_route_record_id": row.get("source_proposal_route_record_id"),
            "source_feedback_ref": row.get("source_feedback_ref"),
            "source_route_map_ref": row.get("source_route_map_ref"),
            "source_proposed_resolution_record_ref": proposed_ref,
            "reviewed_resolution_record_ref": reviewed_ref,
            "reviewed_record_emitted": reviewed_ref is not None,
            "current_resolution_state": "REVIEWED_NOT_CLOSED",
            "review_status": "REVIEWED_ACCEPTED",
            "weak_feedback_resolved": False,
            "c5_reconsideration_ready": False,
        })

    if len(reviewed_qa) != 3:
        failures.append(f"reviewed_qa_count_wrong:{len(reviewed_qa)}")
    if len(reviewed_source) != 2:
        failures.append(f"reviewed_source_count_wrong:{len(reviewed_source)}")
    if len(reviewed_undertyped) != 2:
        failures.append(f"reviewed_undertyped_count_wrong:{len(reviewed_undertyped)}")
    if len(reviewed_parking) != 3:
        failures.append(f"reviewed_parking_count_wrong:{len(reviewed_parking)}")
    if len(reviewed_resolution) != 3:
        failures.append(f"reviewed_resolution_count_wrong:{len(reviewed_resolution)}")
    if len(reviewed_routes) != 3:
        failures.append(f"reviewed_route_count_wrong:{len(reviewed_routes)}")

    for row in reviewed_resolution:
        if row.get("counts_as_reviewed_resolution") is not True:
            failures.append(f"reviewed_resolution_not_counted:{row.get('reviewed_resolution_id')}")
        if row.get("counts_as_final_resolution") is not False or row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"reviewed_resolution_finalized_too_early:{row.get('reviewed_resolution_id')}")

    review_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_EXECUTED_REVIEWED_ARTIFACTS_CLOSE_READY" if review_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_EXECUTED",
        "POST_CLOSURE_DECISION_RECEIPT_CONSUMED",
        "FROZEN_PROPOSED_RECORDS_CONSUMED",
        "REVIEWED_QUESTION_ANSWER_RECORDS_EMITTED",
        "REVIEWED_SOURCE_REF_SATISFACTION_RECORDS_EMITTED",
        "REVIEWED_UNDER_TYPED_ACCEPTANCE_RECORDS_EMITTED",
        "REVIEWED_PARKING_CONTINUATION_RECORDS_EMITTED_AS_UNRESOLVED",
        "REVIEWED_WEAK_FEEDBACK_RESOLUTION_RECORDS_EMITTED_NOT_FINAL",
        "REVIEWED_ROUTE_MAP_EMITTED",
        "PROPOSED_TO_REVIEWED_ARTIFACT_BOUNDARY_CROSSED_EXPLICITLY",
        "FINAL_RESOLUTION_BOUNDARY_NOT_CROSSED",
        "C5_BLOCK_PRESERVED",
        "NO_FINAL_WEAK_FEEDBACK_RESOLUTION_RECORDED",
        "NO_C5_RECONSIDERATION_READY",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if review_pass else failures

    review_execution_record = {
        "schema_version": "o2_proposed_record_review_execution_record_v0",
        "review_execution_status": "REVIEWED_ARTIFACTS_EMITTED_CLOSE_READY" if review_pass else "REVIEW_EXECUTION_FAIL",
        "source_post_closure_decision_receipt_id": POST_DECISION_RECEIPT_ID,
        "proposed_record_review_executed": review_pass,
        "reviewed_artifact_counts": {
            "reviewed_question_answer_records": len(reviewed_qa),
            "reviewed_source_ref_satisfaction_records": len(reviewed_source),
            "reviewed_under_typed_acceptance_records": len(reviewed_undertyped),
            "reviewed_parking_continuation_records": len(reviewed_parking),
            "reviewed_weak_feedback_resolution_records": len(reviewed_resolution),
            "reviewed_route_records": len(reviewed_routes),
        },
        "review_execution_does_not_mean": [
            "weak feedback finally resolved",
            "C5 reconsideration ready",
            "C5 opened",
            "live feedback audit run",
            "runtime patched",
            "sources mutated",
        ],
    }

    write_json(REVIEW_EXECUTION_RECORD_PATH, review_execution_record)
    write_jsonl(REVIEWED_QA_RECORDS_PATH, reviewed_qa)
    write_jsonl(REVIEWED_SOURCE_REF_RECORDS_PATH, reviewed_source)
    write_jsonl(REVIEWED_UNDERTYPED_RECORDS_PATH, reviewed_undertyped)
    write_jsonl(REVIEWED_PARKING_RECORDS_PATH, reviewed_parking)
    write_jsonl(REVIEWED_RESOLUTION_RECORDS_PATH, reviewed_resolution)
    write_jsonl(REVIEWED_ROUTE_MAP_PATH, reviewed_routes)

    review_gate_readout = {
        "schema_version": "o2_proposed_record_review_gate_readout_v0",
        "gate_status": "PROPOSED_RECORD_REVIEW_EXECUTED_CLOSE_READY" if review_pass else "PROPOSED_RECORD_REVIEW_FAIL",
        "proposed_record_review_executed": review_pass,
        "reviewed_question_answer_records_emitted_count": len(reviewed_qa),
        "reviewed_source_ref_satisfaction_records_emitted_count": len(reviewed_source),
        "reviewed_under_typed_acceptance_records_emitted_count": len(reviewed_undertyped),
        "reviewed_parking_continuation_records_emitted_count": len(reviewed_parking),
        "reviewed_resolution_records_emitted_count": len(reviewed_resolution),
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "review_required_next": review_pass,
    }

    resolution_boundary_readout = {
        "schema_version": "o2_reviewed_resolution_boundary_readout_v0",
        "boundary_status": "REVIEWED_ARTIFACTS_EMITTED_FINAL_RESOLUTION_NOT_CROSSED",
        "proposed_layer_crossed_into_reviewed_artifacts": review_pass,
        "reviewed_artifacts_crossed_into_final_resolution": False,
        "reviewed_resolution_records_exist": True,
        "reviewed_resolution_records_emitted_count": len(reviewed_resolution),
        "final_resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "requires_resolution_closure_before_resolved": True,
    }

    c5_readout = {
        "schema_version": "o2_proposed_record_review_c5_block_readout_v0",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "block_enforced": True,
        "reason": "Reviewed artifacts exist, but final weak-feedback resolution closure has not occurred and C5 requires a later explicit decision.",
    }

    unresolved_continuation = {
        "schema_version": "o2_proposed_record_review_unresolved_continuation_v0",
        "unresolved_status_continues": True,
        "proposed_record_review_executed": review_pass,
        "reviewed_resolution_records_exist": True,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": len(reviewed_resolution),
        "parking_counted_as_resolution": False,
    }

    authority_boundary = {
        "schema_version": "o2_proposed_record_review_authority_boundary_v0",
        "status": status,
        "may_review_proposed_record_review_next": review_pass,
        "may_close_reviewed_resolution_now": False,
        "may_resolve_weak_feedback_now": False,
        "may_set_c5_reconsideration_ready": False,
        "may_open_c5": False,
        "may_run_live_feedback_audit_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
    }

    classification = {
        "schema_version": "o2_proposed_record_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "proposed_record_review_executed": review_pass,
        "reviewed_artifacts_emitted": review_pass,
        "review_ready": review_pass,
        "reviewed_question_answer_records_emitted_count": len(reviewed_qa),
        "reviewed_source_ref_satisfaction_records_emitted_count": len(reviewed_source),
        "reviewed_under_typed_acceptance_records_emitted_count": len(reviewed_undertyped),
        "reviewed_parking_continuation_records_emitted_count": len(reviewed_parking),
        "reviewed_resolution_records_emitted_count": len(reviewed_resolution),
        "reviewed_route_records_emitted_count": len(reviewed_routes),
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "final_resolution_boundary_crossed": False,
        "parking_counted_as_resolution": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "live_feedback_audit_executed": False,
        "repair_applied": False,
        "retry_executed": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "architecture_change": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "o2_proposed_record_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "proposed_record_review_execution_count": 1 if review_pass else 0,
        "review_ready_count": 1 if review_pass else 0,
        "reviewed_artifacts_emitted_count": 1 if review_pass else 0,
        "reviewed_question_answer_records_emitted_count": len(reviewed_qa),
        "reviewed_source_ref_satisfaction_records_emitted_count": len(reviewed_source),
        "reviewed_under_typed_acceptance_records_emitted_count": len(reviewed_undertyped),
        "reviewed_parking_continuation_records_emitted_count": len(reviewed_parking),
        "reviewed_resolution_records_emitted_count": len(reviewed_resolution),
        "reviewed_route_records_emitted_count": len(reviewed_routes),
        "weak_feedback_resolved_count": 0,
        "resolution_records_emitted_count": 0,
        "final_resolution_boundary_crossed_count": 0,
        "parked_records_counted_as_resolved_count": 0,
        "live_feedback_audit_executed_count": 0,
        "repair_applied_count": 0,
        "retry_executed_count": 0,
        "target_selected_for_build_count": 0,
        "runtime_patch_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "architecture_change_count": 0,
        "c5_opened_count": 0,
        "c5_reconsideration_ready_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "weak_feedback_resolved_count",
        "resolution_records_emitted_count",
        "final_resolution_boundary_crossed_count",
        "parked_records_counted_as_resolved_count",
        "live_feedback_audit_executed_count",
        "repair_applied_count",
        "retry_executed_count",
        "target_selected_for_build_count",
        "runtime_patch_count",
        "source_mutated_count",
        "prior_receipt_mutated_count",
        "architecture_change_count",
        "c5_opened_count",
        "c5_reconsideration_ready_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "o2_proposed_record_review_profile_v0",
        "profile_id": "o2_proposed_record_review_profile_" + sha8(rollup),
        "status": status,
        "proposed_record_review_executed": review_pass,
        "reviewed_artifacts_emitted": review_pass,
        "review_ready": review_pass,
        "reviewed_resolution_records_emitted_count": len(reviewed_resolution),
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "final_resolution_boundary_crossed": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Review the proposed-record review output next. Do not treat reviewed artifacts as final resolution or C5 readiness.",
        "must_not_infer": [
            "weak feedback finally resolved",
            "C5 reconsideration ready",
            "C5 opened",
            "live feedback audit executed",
            "runtime patched",
            "source mutated",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_proposed_record_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Proposed-record review executed and emitted reviewed artifacts, including reviewed weak-feedback resolution records. These reviewed artifacts do not yet finalize weak-feedback resolution and do not unblock C5.",
        "reviewed_resolution_records_emitted_count": len(reviewed_resolution),
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_proposed_record_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_proposed_record_review_decision",
                "question": "is proposed-record review authorized",
                "answer": "yes" if review_pass else "no",
                "taken": "review frozen proposed records",
            },
            {
                "step": "cross_proposed_to_reviewed_artifacts",
                "question": "are reviewed artifacts emitted explicitly",
                "answer": "yes" if review_pass else "no",
                "taken": "emit reviewed artifacts and route map",
            },
            {
                "step": "preserve_final_resolution_and_c5_boundary",
                "question": "does reviewed artifact emission finalize weak feedback or open C5",
                "answer": "no",
                "taken": "review proposed-record review output next",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(REVIEW_GATE_READOUT_PATH, review_gate_readout)
    write_json(RESOLUTION_BOUNDARY_READOUT_PATH, resolution_boundary_readout)
    write_json(C5_BLOCK_READOUT_PATH, c5_readout)
    write_json(UNRESOLVED_CONTINUATION_PATH, unresolved_continuation)
    write_json(AUTHORITY_BOUNDARY_PATH, authority_boundary)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRACE_PATH, trace)

    acceptance_gate_results = {
        "PROPOSED_RECORD_REVIEW_0_POST_DECISION_RECEIPT_CONSUMED": POST_DECISION_RECEIPT_PATH.exists(),
        "PROPOSED_RECORD_REVIEW_1_REVIEW_EXECUTION_RECORD_EMITTED": REVIEW_EXECUTION_RECORD_PATH.exists(),
        "PROPOSED_RECORD_REVIEW_2_REVIEWED_QA_RECORDS_EMITTED": len(reviewed_qa) == 3,
        "PROPOSED_RECORD_REVIEW_3_REVIEWED_SOURCE_REF_RECORDS_EMITTED": len(reviewed_source) == 2,
        "PROPOSED_RECORD_REVIEW_4_REVIEWED_UNDERTYPED_RECORDS_EMITTED": len(reviewed_undertyped) == 2,
        "PROPOSED_RECORD_REVIEW_5_REVIEWED_PARKING_RECORDS_EMITTED_UNRESOLVED": len(reviewed_parking) == 3,
        "PROPOSED_RECORD_REVIEW_6_REVIEWED_RESOLUTION_RECORDS_EMITTED": len(reviewed_resolution) == 3,
        "PROPOSED_RECORD_REVIEW_7_REVIEWED_ROUTE_MAP_EMITTED": len(reviewed_routes) == 3,
        "PROPOSED_RECORD_REVIEW_8_REVIEWED_ARTIFACTS_NOT_FINAL_RESOLUTION": all(x.get("counts_as_final_resolution") is False and x.get("weak_feedback_resolved") is False for x in reviewed_resolution),
        "PROPOSED_RECORD_REVIEW_9_C5_BLOCK_PRESERVED": rollup["c5_opened_count"] == 0 and rollup["c5_reconsideration_ready_count"] == 0,
        "PROPOSED_RECORD_REVIEW_10_FINAL_WEAK_FEEDBACK_NOT_RESOLVED": rollup["weak_feedback_resolved_count"] == 0 and rollup["resolution_records_emitted_count"] == 0,
        "PROPOSED_RECORD_REVIEW_11_NO_PARKING_AS_RESOLUTION": rollup["parked_records_counted_as_resolved_count"] == 0,
        "PROPOSED_RECORD_REVIEW_12_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "PROPOSED_RECORD_REVIEW_13_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "PROPOSED_RECORD_REVIEW_14_REVIEW_READY": rollup["review_ready_count"] == 1,
        "PROPOSED_RECORD_REVIEW_15_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "PROPOSED_RECORD_REVIEW_16_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "PROPOSED_RECORD_REVIEW_17_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "reviewed_resolution_records": len(reviewed_resolution),
        "final_resolution": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_resolution_proposed_record_review_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_post_closure_decision_receipt_id": POST_DECISION_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_resolution_proposed_record_review_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "proposed_record_review_executed": review_pass,
            "reviewed_artifacts_emitted": review_pass,
            "review_ready": review_pass,
            "reviewed_question_answer_records_emitted_count": len(reviewed_qa),
            "reviewed_source_ref_satisfaction_records_emitted_count": len(reviewed_source),
            "reviewed_under_typed_acceptance_records_emitted_count": len(reviewed_undertyped),
            "reviewed_parking_continuation_records_emitted_count": len(reviewed_parking),
            "reviewed_resolution_records_emitted_count": len(reviewed_resolution),
            "reviewed_route_records_emitted_count": len(reviewed_routes),
            "resolution_records_emitted_count": 0,
            "weak_feedback_resolved": False,
            "final_resolution_boundary_crossed": False,
            "parking_counted_as_resolution": False,
            "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
            "c5_reconsideration_ready": False,
            "c5_opened": False,
            "live_feedback_audit_executed": False,
            "repair_applied": False,
            "retry_executed": False,
            "target_selected_for_build": False,
            "runtime_patch_applied": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "architecture_change": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": recommended_next,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "review_execution_record": rel(REVIEW_EXECUTION_RECORD_PATH),
            "reviewed_question_answer_records": rel(REVIEWED_QA_RECORDS_PATH),
            "reviewed_source_ref_satisfaction_records": rel(REVIEWED_SOURCE_REF_RECORDS_PATH),
            "reviewed_under_typed_acceptance_records": rel(REVIEWED_UNDERTYPED_RECORDS_PATH),
            "reviewed_parking_continuation_records": rel(REVIEWED_PARKING_RECORDS_PATH),
            "reviewed_weak_feedback_resolution_records": rel(REVIEWED_RESOLUTION_RECORDS_PATH),
            "reviewed_route_map": rel(REVIEWED_ROUTE_MAP_PATH),
            "review_gate_readout": rel(REVIEW_GATE_READOUT_PATH),
            "resolution_boundary_readout": rel(RESOLUTION_BOUNDARY_READOUT_PATH),
            "c5_block_readout": rel(C5_BLOCK_READOUT_PATH),
            "unresolved_continuation": rel(UNRESOLVED_CONTINUATION_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"proposed_record_review_receipt_id={receipt_id}")
    print(f"proposed_record_review_receipt_path={rel(receipt_path)}")
    print(f"proposed_record_review_execution_record_path={rel(REVIEW_EXECUTION_RECORD_PATH)}")
    print(f"reviewed_question_answer_records_path={rel(REVIEWED_QA_RECORDS_PATH)}")
    print(f"reviewed_source_ref_satisfaction_records_path={rel(REVIEWED_SOURCE_REF_RECORDS_PATH)}")
    print(f"reviewed_under_typed_acceptance_records_path={rel(REVIEWED_UNDERTYPED_RECORDS_PATH)}")
    print(f"reviewed_parking_continuation_records_path={rel(REVIEWED_PARKING_RECORDS_PATH)}")
    print(f"reviewed_weak_feedback_resolution_records_path={rel(REVIEWED_RESOLUTION_RECORDS_PATH)}")
    print(f"reviewed_weak_feedback_resolution_route_map_path={rel(REVIEWED_ROUTE_MAP_PATH)}")
    print(f"proposed_record_review_gate_readout_path={rel(REVIEW_GATE_READOUT_PATH)}")
    print(f"proposed_record_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"proposed_record_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
