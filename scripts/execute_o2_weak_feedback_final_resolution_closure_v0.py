#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXECUTE_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_final_resolution_closure.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE"
MODE = "EXECUTE / FINAL_RESOLUTION_CLOSURE / WEAK_FEEDBACK_RESOLVED / NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_ONLY"

SOURCE_DECISION_RECEIPT_ID = "34bab59d"

SOURCE_DECISION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0_receipts/34bab59d.json"
DECISION_BASIS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_post_review_reference_closure_decision_basis_v0.json"
DECISION_TABLE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_post_review_reference_closure_decision_table_v0.json"
SELECTED_BRANCH_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_final_resolution_closure_selected_branch_v0.json"
FINAL_AUTH_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_final_resolution_closure_authorization_v0.json"
INPUT_SCOPE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_final_resolution_closure_input_scope_v0.json"
DECISION_UNRESOLVED_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_post_review_reference_closure_unresolved_continuation_v0.json"
DECISION_C5_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_post_review_reference_closure_c5_block_continuation_v0.json"
DECISION_DEFERRED_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_post_review_reference_closure_deferred_branches_v0.json"
DECISION_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_post_review_reference_closure_decision_authority_boundary_v0.json"
DECISION_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_post_review_reference_closure_decision_classification_v0.json"
DECISION_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_post_review_reference_closure_decision_rollup_v0.json"
DECISION_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_post_review_reference_closure_decision_profile_v0.json"
DECISION_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_post_review_reference_closure_decision_report.json"
DECISION_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_post_closure_decision_v0/o2_post_review_reference_closure_decision_transition_trace.json"

SOURCE_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0_receipts/2f793867.json"
REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_reviewed_reference_v0.json"
REVIEWED_ARTIFACT_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_reviewed_artifact_inventory_freeze_v0.json"
REVIEWED_RESOLUTION_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_reviewed_weak_feedback_resolution_record_freeze_v0.json"
REVIEWED_ROUTE_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_reviewed_route_map_freeze_v0.json"
FINAL_BOUNDARY_LOCK_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_final_resolution_boundary_lock_v0.json"
UNRESOLVED_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_unresolved_status_freeze_v0.json"
C5_BLOCK_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0/o2_proposed_record_review_c5_block_freeze_v0.json"

REVIEWED_QA_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_question_answer_records_v0.jsonl"
REVIEWED_SOURCE_REF_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_source_ref_satisfaction_records_v0.jsonl"
REVIEWED_UNDERTYPED_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_under_typed_acceptance_records_v0.jsonl"
REVIEWED_PARKING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_parking_continuation_records_v0.jsonl"
REVIEWED_RESOLUTION_RECORDS_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_weak_feedback_resolution_records_v0.jsonl"
REVIEWED_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_weak_feedback_resolution_route_map_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    SOURCE_DECISION_RECEIPT_PATH,
    DECISION_BASIS_PATH,
    DECISION_TABLE_PATH,
    SELECTED_BRANCH_PATH,
    FINAL_AUTH_PATH,
    INPUT_SCOPE_PATH,
    DECISION_UNRESOLVED_PATH,
    DECISION_C5_PATH,
    DECISION_DEFERRED_PATH,
    DECISION_AUTHORITY_PATH,
    DECISION_CLASSIFICATION_PATH,
    DECISION_ROLLUP_PATH,
    DECISION_PROFILE_PATH,
    DECISION_REPORT_PATH,
    DECISION_TRACE_PATH,
    SOURCE_CLOSURE_RECEIPT_PATH,
    REVIEWED_REFERENCE_PATH,
    REVIEWED_ARTIFACT_FREEZE_PATH,
    REVIEWED_RESOLUTION_FREEZE_PATH,
    REVIEWED_ROUTE_FREEZE_PATH,
    FINAL_BOUNDARY_LOCK_PATH,
    UNRESOLVED_FREEZE_PATH,
    C5_BLOCK_FREEZE_PATH,
    REVIEWED_QA_RECORDS_PATH,
    REVIEWED_SOURCE_REF_RECORDS_PATH,
    REVIEWED_UNDERTYPED_RECORDS_PATH,
    REVIEWED_PARKING_RECORDS_PATH,
    REVIEWED_RESOLUTION_RECORDS_PATH,
    REVIEWED_ROUTE_MAP_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_final_resolution_closure_v0_receipts"

EXECUTION_RECORD_PATH = OUT_DIR / "o2_final_resolution_closure_execution_record_v0.json"
FINAL_QA_CLOSURE_RECORDS_PATH = OUT_DIR / "o2_final_question_answer_closure_records_v0.jsonl"
FINAL_SOURCE_REF_CLOSURE_RECORDS_PATH = OUT_DIR / "o2_final_source_ref_satisfaction_closure_records_v0.jsonl"
FINAL_UNDERTYPED_CLOSURE_RECORDS_PATH = OUT_DIR / "o2_final_under_typed_acceptance_closure_records_v0.jsonl"
FINAL_PARKING_CLOSURE_RECORDS_PATH = OUT_DIR / "o2_final_parking_continuation_closure_records_v0.jsonl"
FINAL_RESOLUTION_RECORDS_PATH = OUT_DIR / "o2_final_weak_feedback_resolution_records_v0.jsonl"
FINAL_ROUTE_CLOSURE_RECORDS_PATH = OUT_DIR / "o2_final_resolution_route_closure_records_v0.jsonl"
RESOLVED_STATUS_PATH = OUT_DIR / "o2_weak_feedback_resolved_status_v0.json"
FINAL_BOUNDARY_CROSSING_PATH = OUT_DIR / "o2_final_resolution_boundary_crossing_v0.json"
C5_BLOCK_AFTER_FINAL_CLOSURE_PATH = OUT_DIR / "o2_c5_block_after_final_resolution_closure_v0.json"
CLOSURE_INPUT_CONFIRMATION_PATH = OUT_DIR / "o2_final_resolution_closure_input_confirmation_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_final_resolution_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_final_resolution_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_final_resolution_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_final_resolution_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_final_resolution_closure_report.json"
TRACE_PATH = OUT_DIR / "o2_final_resolution_closure_transition_trace.json"

EXPECTED_DECISION_STATUS = "TYPED_O2_PROPOSED_RECORD_REVIEW_POST_CLOSURE_DECISION_SELECTED_FINAL_RESOLUTION_CLOSURE_READY"
EXPECTED_DECISION_STOP = "STOP_TYPED_O2_PROPOSED_RECORD_REVIEW_POST_CLOSURE_DECISION_SELECTED_FINAL_RESOLUTION_CLOSURE_READY"
EXPECTED_DECISION_NEXT = "EXECUTE_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_V0"
RECOMMENDED_NEXT = "REVIEW_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_V0"

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

def final_id(prefix: str, src_id: str, obj: Dict[str, Any]) -> str:
    return prefix + "_" + sha8({"src_id": src_id, "obj": obj})

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []

    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    decision_receipt = read_json(SOURCE_DECISION_RECEIPT_PATH)
    decision_summary = decision_receipt.get("machine_readable_o2_post_review_reference_closure_decision_summary", {})
    decision_basis = read_json(DECISION_BASIS_PATH)
    selected_branch = read_json(SELECTED_BRANCH_PATH)
    final_auth = read_json(FINAL_AUTH_PATH)
    input_scope = read_json(INPUT_SCOPE_PATH)
    decision_unresolved = read_json(DECISION_UNRESOLVED_PATH)
    decision_c5 = read_json(DECISION_C5_PATH)
    decision_authority = read_json(DECISION_AUTHORITY_PATH)
    decision_classification = read_json(DECISION_CLASSIFICATION_PATH)
    decision_rollup = read_json(DECISION_ROLLUP_PATH)
    decision_profile = read_json(DECISION_PROFILE_PATH)

    closure_receipt = read_json(SOURCE_CLOSURE_RECEIPT_PATH)
    reviewed_reference = read_json(REVIEWED_REFERENCE_PATH)
    artifact_freeze = read_json(REVIEWED_ARTIFACT_FREEZE_PATH)
    resolution_freeze = read_json(REVIEWED_RESOLUTION_FREEZE_PATH)
    route_freeze = read_json(REVIEWED_ROUTE_FREEZE_PATH)
    boundary_lock = read_json(FINAL_BOUNDARY_LOCK_PATH)
    unresolved_freeze = read_json(UNRESOLVED_FREEZE_PATH)
    c5_freeze = read_json(C5_BLOCK_FREEZE_PATH)

    qa = read_jsonl(REVIEWED_QA_RECORDS_PATH)
    source = read_jsonl(REVIEWED_SOURCE_REF_RECORDS_PATH)
    undertyped = read_jsonl(REVIEWED_UNDERTYPED_RECORDS_PATH)
    parking = read_jsonl(REVIEWED_PARKING_RECORDS_PATH)
    reviewed_resolution = read_jsonl(REVIEWED_RESOLUTION_RECORDS_PATH)
    reviewed_routes = read_jsonl(REVIEWED_ROUTE_MAP_PATH)

    if decision_receipt.get("receipt_id") != SOURCE_DECISION_RECEIPT_ID or decision_receipt.get("gate") != "PASS":
        failures.append("source_decision_receipt_not_pass")
    if decision_receipt.get("terminal", {}).get("stop_code") != EXPECTED_DECISION_STOP:
        failures.append("source_decision_stop_wrong")
    if decision_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_decision_hidden_next")
    if decision_summary.get("status") != EXPECTED_DECISION_STATUS:
        failures.append(f"source_decision_status_wrong:{decision_summary.get('status')}")
    if decision_summary.get("recommended_next") != EXPECTED_DECISION_NEXT:
        failures.append(f"source_decision_next_wrong:{decision_summary.get('recommended_next')}")

    for key in [
        "post_closure_decision_complete",
        "final_resolution_closure_authorized_next",
        "reviewed_resolution_records_exist",
        "bad_counters_zero",
    ]:
        if decision_summary.get(key) is not True:
            failures.append(f"decision_summary_required_true_missing:{key}")

    for key in [
        "final_resolution_closure_executed_in_decision",
        "weak_feedback_resolved",
        "final_resolution_boundary_crossed",
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
        if decision_summary.get(key) is not False:
            failures.append(f"decision_summary_forbidden_true:{key}")

    if decision_summary.get("reviewed_resolution_records_frozen_count") != 3:
        failures.append("decision_reviewed_resolution_count_wrong")
    if decision_summary.get("resolution_records_emitted_count") != 0:
        failures.append("decision_resolution_records_nonzero")
    if decision_summary.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("decision_selected_next_wrong")
    if selected_branch.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("selected_branch_next_wrong")
    if final_auth.get("authorization_status") != "FINAL_RESOLUTION_CLOSURE_AUTHORIZED_NEXT":
        failures.append("final_auth_status_wrong")
    if final_auth.get("authorized_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("final_auth_next_wrong")
    if input_scope.get("scope_status") != "FROZEN_REVIEWED_REFERENCE_ELIGIBLE_FOR_FINAL_CLOSURE_EXECUTION":
        failures.append("input_scope_wrong")
    if decision_unresolved.get("weak_feedback_resolved") is not False:
        failures.append("decision_unresolved_wrong")
    if decision_c5.get("c5_opened") is not False or decision_c5.get("c5_reconsideration_ready") is not False:
        failures.append("decision_c5_wrong")
    if decision_authority.get("may_execute_final_resolution_closure_next") is not True:
        failures.append("decision_authority_no_execute")
    if decision_authority.get("may_resolve_weak_feedback_now") is not False or decision_authority.get("may_open_c5") is not False:
        failures.append("decision_authority_allows_now")
    if decision_classification.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("decision_classification_next_wrong")
    if decision_rollup.get("selected_final_resolution_closure_count") != 1:
        failures.append("decision_rollup_selection_wrong")
    if decision_profile.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("decision_profile_next_wrong")

    closure_summary = closure_receipt.get("machine_readable_o2_weak_feedback_resolution_proposed_record_review_closure_summary", {})
    if closure_receipt.get("receipt_id") != "2f793867" or closure_receipt.get("gate") != "PASS":
        failures.append("source_closure_receipt_not_pass")
    if closure_summary.get("proposed_record_review_closed_as_reviewed_reference") is not True:
        failures.append("closure_not_closed")
    if reviewed_reference.get("reviewed_resolution_records_exist") is not True:
        failures.append("reviewed_reference_resolution_missing")
    if reviewed_reference.get("weak_feedback_resolved") is not False:
        failures.append("reviewed_reference_already_resolved")
    if artifact_freeze.get("reviewed_weak_feedback_resolution_records_frozen_count") != 3:
        failures.append("artifact_freeze_count_wrong")
    if resolution_freeze.get("reviewed_resolution_records_frozen_count") != 3:
        failures.append("resolution_freeze_count_wrong")
    if resolution_freeze.get("final_resolution_records_emitted_count") != 0 or resolution_freeze.get("weak_feedback_resolved") is not False:
        failures.append("resolution_freeze_final_wrong")
    if route_freeze.get("all_reviewed_not_closed") is not True:
        failures.append("route_freeze_wrong")
    if boundary_lock.get("final_resolution_boundary_crossed") is not False or boundary_lock.get("weak_feedback_resolved") is not False:
        failures.append("boundary_lock_wrong")
    if boundary_lock.get("requires_decision_before_final_resolution_closure") is not True:
        failures.append("boundary_lock_missing_decision_gate")
    if unresolved_freeze.get("weak_feedback_resolved") is not False:
        failures.append("unresolved_freeze_wrong")
    if c5_freeze.get("c5_opened") is not False or c5_freeze.get("c5_reconsideration_ready") is not False:
        failures.append("c5_freeze_wrong")

    if len(qa) != 3 or len(source) != 2 or len(undertyped) != 2 or len(parking) != 3 or len(reviewed_resolution) != 3 or len(reviewed_routes) != 3:
        failures.append("reviewed_record_counts_wrong")

    for row in qa:
        if row.get("review_status") != "REVIEWED_ACCEPTED" or row.get("counts_as_answer") is not True:
            failures.append(f"qa_not_reviewed_answer:{row.get('reviewed_answer_id')}")
    for row in source:
        if row.get("review_status") != "REVIEWED_ACCEPTED" or row.get("counts_as_satisfied") is not True:
            failures.append(f"source_not_reviewed_satisfied:{row.get('reviewed_satisfaction_id')}")
    for row in undertyped:
        if row.get("review_status") != "REVIEWED_ACCEPTED" or row.get("counts_as_approved") is not True:
            failures.append(f"undertyped_not_reviewed_approved:{row.get('reviewed_under_typed_acceptance_id')}")
    for row in parking:
        if row.get("counts_as_resolution") is not False:
            failures.append(f"parking_counts_as_resolution:{row.get('reviewed_parking_continuation_id')}")
    for row in reviewed_resolution:
        if row.get("review_status") != "REVIEWED_ACCEPTED" or row.get("counts_as_reviewed_resolution") is not True:
            failures.append(f"reviewed_resolution_status_wrong:{row.get('reviewed_resolution_id')}")
        if row.get("counts_as_final_resolution") is not False or row.get("weak_feedback_resolved") is not False:
            failures.append(f"reviewed_resolution_already_final:{row.get('reviewed_resolution_id')}")
        if row.get("requires_resolution_closure_before_resolved") is not True:
            failures.append(f"reviewed_resolution_missing_closure_gate:{row.get('reviewed_resolution_id')}")
    for row in reviewed_routes:
        if row.get("reviewed_record_emitted") is not True or row.get("current_resolution_state") != "REVIEWED_NOT_CLOSED":
            failures.append(f"route_not_reviewed_not_closed:{row.get('reviewed_route_record_id')}")

    return failures, {
        "qa": qa,
        "source": source,
        "undertyped": undertyped,
        "parking": parking,
        "reviewed_resolution": reviewed_resolution,
        "reviewed_routes": reviewed_routes,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    qa = src.get("qa", [])
    source = src.get("source", [])
    undertyped = src.get("undertyped", [])
    parking = src.get("parking", [])
    reviewed_resolution = src.get("reviewed_resolution", [])
    reviewed_routes = src.get("reviewed_routes", [])

    execute_pass = not failures

    final_qa = []
    for row in qa:
        src_id = row.get("reviewed_answer_id")
        final_qa.append({
            "schema_version": "o2_final_question_answer_closure_record_v0",
            "final_question_answer_closure_id": final_id("final_question_answer_closure", src_id, row),
            "source_reviewed_answer_id": src_id,
            "closure_status": "FINAL_CLOSURE_ACCEPTED",
            "counts_as_final_answer_basis": True,
            "weak_feedback_resolved_by_this_record": False,
            "c5_reconsideration_ready": False,
        })

    final_source = []
    for row in source:
        src_id = row.get("reviewed_satisfaction_id")
        final_source.append({
            "schema_version": "o2_final_source_ref_satisfaction_closure_record_v0",
            "final_source_ref_closure_id": final_id("final_source_ref_closure", src_id, row),
            "source_reviewed_satisfaction_id": src_id,
            "closure_status": "FINAL_CLOSURE_ACCEPTED",
            "counts_as_final_source_ref_basis": True,
            "weak_feedback_resolved_by_this_record": False,
            "c5_reconsideration_ready": False,
        })

    final_undertyped = []
    for row in undertyped:
        src_id = row.get("reviewed_under_typed_acceptance_id")
        final_undertyped.append({
            "schema_version": "o2_final_under_typed_acceptance_closure_record_v0",
            "final_under_typed_acceptance_closure_id": final_id("final_under_typed_acceptance_closure", src_id, row),
            "source_reviewed_under_typed_acceptance_id": src_id,
            "closure_status": "FINAL_CLOSURE_ACCEPTED",
            "counts_as_final_under_typed_acceptance_basis": True,
            "weak_feedback_resolved_by_this_record": False,
            "c5_reconsideration_ready": False,
        })

    final_parking = []
    for row in parking:
        src_id = row.get("reviewed_parking_continuation_id")
        final_parking.append({
            "schema_version": "o2_final_parking_continuation_closure_record_v0",
            "final_parking_continuation_closure_id": final_id("final_parking_continuation_closure", src_id, row),
            "source_reviewed_parking_continuation_id": src_id,
            "closure_status": "FINAL_PARKING_CONTINUES",
            "counts_as_final_resolution": False,
            "weak_feedback_resolved_by_this_record": False,
            "c5_reconsideration_ready": False,
        })

    final_resolution = []
    final_id_by_reviewed: Dict[str, str] = {}
    for row in reviewed_resolution:
        src_id = row.get("reviewed_resolution_id")
        fid = final_id("final_weak_feedback_resolution", src_id, row)
        final_id_by_reviewed[src_id] = fid
        final_resolution.append({
            "schema_version": "o2_final_weak_feedback_resolution_record_v0",
            "final_resolution_id": fid,
            "source_reviewed_resolution_id": src_id,
            "source_route_map_ref": row.get("source_route_map_ref"),
            "source_template_ref": row.get("source_template_ref"),
            "closure_status": "FINAL_RESOLUTION_CLOSED",
            "counts_as_final_resolution": True,
            "counts_as_reviewed_resolution": True,
            "weak_feedback_resolved": True,
            "final_resolution_boundary_crossed": True,
            "c5_reconsideration_ready": False,
            "c5_opened": False,
            "review_required_next": True,
        })

    final_routes = []
    for row in reviewed_routes:
        src_route_id = row.get("reviewed_route_record_id")
        reviewed_ref = row.get("reviewed_resolution_record_ref")
        final_ref = final_id_by_reviewed.get(reviewed_ref)
        final_routes.append({
            "schema_version": "o2_final_resolution_route_closure_record_v0",
            "final_route_closure_id": final_id("final_route_closure", src_route_id, row),
            "source_reviewed_route_record_id": src_route_id,
            "source_reviewed_resolution_record_ref": reviewed_ref,
            "final_resolution_record_ref": final_ref,
            "closure_status": "FINAL_ROUTE_CLOSED",
            "final_resolution_record_emitted": final_ref is not None,
            "weak_feedback_resolved": final_ref is not None,
            "c5_reconsideration_ready": False,
            "c5_opened": False,
        })

    if len(final_qa) != 3:
        failures.append(f"final_qa_count_wrong:{len(final_qa)}")
    if len(final_source) != 2:
        failures.append(f"final_source_count_wrong:{len(final_source)}")
    if len(final_undertyped) != 2:
        failures.append(f"final_undertyped_count_wrong:{len(final_undertyped)}")
    if len(final_parking) != 3:
        failures.append(f"final_parking_count_wrong:{len(final_parking)}")
    if len(final_resolution) != 3:
        failures.append(f"final_resolution_count_wrong:{len(final_resolution)}")
    if len(final_routes) != 3:
        failures.append(f"final_route_count_wrong:{len(final_routes)}")

    execute_pass = not failures

    status = "TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_EXECUTED_RESOLUTION_RECORDS_REVIEW_READY" if execute_pass else "TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if execute_pass else "REPAIR_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_V0"

    reason_codes = [
        "FINAL_RESOLUTION_CLOSURE_EXECUTED",
        "POST_REVIEW_REFERENCE_CLOSURE_DECISION_RECEIPT_CONSUMED",
        "FINAL_RESOLUTION_CLOSURE_AUTHORIZATION_CONSUMED",
        "FROZEN_REVIEWED_REFERENCE_CONSUMED",
        "REVIEWED_QA_RECORDS_CLOSED_AS_FINAL_BASIS",
        "REVIEWED_SOURCE_REF_RECORDS_CLOSED_AS_FINAL_BASIS",
        "REVIEWED_UNDER_TYPED_ACCEPTANCE_RECORDS_CLOSED_AS_FINAL_BASIS",
        "PARKING_CONFIRMED_NOT_COUNTED_AS_RESOLUTION",
        "FINAL_WEAK_FEEDBACK_RESOLUTION_RECORDS_EMITTED",
        "FINAL_RESOLUTION_BOUNDARY_CROSSED",
        "WEAK_FEEDBACK_RESOLVED",
        "C5_BLOCK_PRESERVED_PENDING_C5_DECISION",
        "NO_C5_RECONSIDERATION_READY",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if execute_pass else failures

    execution_record = {
        "schema_version": "o2_final_resolution_closure_execution_record_v0",
        "execution_status": "FINAL_RESOLUTION_CLOSURE_EXECUTED_REVIEW_READY" if execute_pass else "FINAL_RESOLUTION_CLOSURE_EXECUTION_FAIL",
        "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "final_resolution_closure_executed": execute_pass,
        "review_required_next": execute_pass,
        "final_resolution_records_emitted_count": len(final_resolution),
        "weak_feedback_resolved": execute_pass,
        "final_resolution_boundary_crossed": execute_pass,
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    write_json(EXECUTION_RECORD_PATH, execution_record)
    write_jsonl(FINAL_QA_CLOSURE_RECORDS_PATH, final_qa)
    write_jsonl(FINAL_SOURCE_REF_CLOSURE_RECORDS_PATH, final_source)
    write_jsonl(FINAL_UNDERTYPED_CLOSURE_RECORDS_PATH, final_undertyped)
    write_jsonl(FINAL_PARKING_CLOSURE_RECORDS_PATH, final_parking)
    write_jsonl(FINAL_RESOLUTION_RECORDS_PATH, final_resolution)
    write_jsonl(FINAL_ROUTE_CLOSURE_RECORDS_PATH, final_routes)

    resolved_status = {
        "schema_version": "o2_weak_feedback_resolved_status_v0",
        "resolved_status": "WEAK_FEEDBACK_RESOLVED_BY_FINAL_RESOLUTION_CLOSURE" if execute_pass else "WEAK_FEEDBACK_NOT_RESOLVED",
        "weak_feedback_resolved": execute_pass,
        "final_resolution_records_emitted_count": len(final_resolution),
        "resolution_records_emitted_count": len(final_resolution),
        "review_required_next": execute_pass,
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    boundary_crossing = {
        "schema_version": "o2_final_resolution_boundary_crossing_v0",
        "boundary_status": "FINAL_RESOLUTION_BOUNDARY_CROSSED" if execute_pass else "FINAL_RESOLUTION_BOUNDARY_NOT_CROSSED",
        "reviewed_resolution_records_consumed_count": len(reviewed_resolution),
        "final_resolution_records_emitted_count": len(final_resolution),
        "resolution_records_emitted_count": len(final_resolution),
        "final_resolution_boundary_crossed": execute_pass,
        "weak_feedback_resolved": execute_pass,
        "parking_counted_as_resolution": False,
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    c5_block = {
        "schema_version": "o2_c5_block_after_final_resolution_closure_v0",
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "block_enforced": True,
        "block_reason": "Weak feedback final-resolution closure was executed, but C5 requires a later explicit decision.",
    }

    input_confirmation = {
        "schema_version": "o2_final_resolution_closure_input_confirmation_v0",
        "input_status": "FROZEN_REVIEWED_REFERENCE_CONSUMED",
        "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "source_closure_receipt_id": "2f793867",
        "reviewed_question_answer_records_count": len(qa),
        "reviewed_source_ref_satisfaction_records_count": len(source),
        "reviewed_under_typed_acceptance_records_count": len(undertyped),
        "reviewed_parking_continuation_records_count": len(parking),
        "reviewed_resolution_records_count": len(reviewed_resolution),
        "reviewed_route_records_count": len(reviewed_routes),
    }

    authority_boundary = {
        "schema_version": "o2_final_resolution_closure_authority_boundary_v0",
        "status": status,
        "may_review_final_resolution_closure_next": execute_pass,
        "may_set_c5_reconsideration_ready_now": False,
        "may_open_c5_now": False,
        "may_run_live_feedback_audit_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_change_architecture": False,
    }

    classification = {
        "schema_version": "o2_final_resolution_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "final_resolution_closure_executed": execute_pass,
        "review_ready": execute_pass,
        "question_packets_answered": execute_pass,
        "source_ref_requests_satisfied": execute_pass,
        "under_typed_acceptance_approved": execute_pass,
        "final_question_answer_closure_records_emitted_count": len(final_qa),
        "final_source_ref_closure_records_emitted_count": len(final_source),
        "final_under_typed_acceptance_closure_records_emitted_count": len(final_undertyped),
        "final_parking_closure_records_emitted_count": len(final_parking),
        "final_resolution_records_emitted_count": len(final_resolution),
        "resolution_records_emitted_count": len(final_resolution),
        "final_route_closure_records_emitted_count": len(final_routes),
        "weak_feedback_resolved": execute_pass,
        "final_resolution_boundary_crossed": execute_pass,
        "parking_counted_as_resolution": False,
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
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
        "schema_version": "o2_final_resolution_closure_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "final_resolution_closure_executed_count": 1 if execute_pass else 0,
        "review_ready_count": 1 if execute_pass else 0,
        "question_packets_answered_count": 1 if execute_pass else 0,
        "source_ref_requests_satisfied_count": 1 if execute_pass else 0,
        "under_typed_acceptance_approved_count": 1 if execute_pass else 0,
        "final_question_answer_closure_records_emitted_count": len(final_qa),
        "final_source_ref_closure_records_emitted_count": len(final_source),
        "final_under_typed_acceptance_closure_records_emitted_count": len(final_undertyped),
        "final_parking_closure_records_emitted_count": len(final_parking),
        "final_resolution_records_emitted_count": len(final_resolution),
        "resolution_records_emitted_count": len(final_resolution),
        "final_route_closure_records_emitted_count": len(final_routes),
        "weak_feedback_resolved_count": 1 if execute_pass else 0,
        "final_resolution_boundary_crossed_count": 1 if execute_pass else 0,
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
        "schema_version": "o2_final_resolution_closure_profile_v0",
        "profile_id": "o2_final_resolution_closure_profile_" + sha8(rollup),
        "status": status,
        "final_resolution_closure_executed": execute_pass,
        "review_ready": execute_pass,
        "final_resolution_records_emitted_count": len(final_resolution),
        "resolution_records_emitted_count": len(final_resolution),
        "weak_feedback_resolved": execute_pass,
        "final_resolution_boundary_crossed": execute_pass,
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Review final-resolution closure next. Do not treat this as C5 authorization.",
        "must_not_infer": [
            "C5 reconsideration ready",
            "C5 opened",
            "live feedback audit executed",
            "runtime patched",
            "source mutated",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_final_resolution_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Final weak-feedback resolution closure executed from the frozen reviewed reference. Weak feedback is resolved by final-resolution records, while C5 remains blocked pending a later explicit C5 decision.",
        "final_resolution_records_emitted_count": len(final_resolution),
        "resolution_records_emitted_count": len(final_resolution),
        "weak_feedback_resolved": execute_pass,
        "final_resolution_boundary_crossed": execute_pass,
        "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_final_resolution_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_final_resolution_closure_decision",
                "question": "is final-resolution closure authorized",
                "answer": "yes" if execute_pass else "no",
                "taken": "consume frozen reviewed reference",
            },
            {
                "step": "emit_final_resolution_records",
                "question": "can reviewed resolution records be promoted to final resolution",
                "answer": "yes" if execute_pass else "no",
                "taken": "emit final weak-feedback resolution records",
            },
            {
                "step": "preserve_c5_decision_gate",
                "question": "does final resolution closure open C5",
                "answer": "no",
                "taken": "keep C5 blocked pending explicit decision",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    for path, obj in [
        (RESOLVED_STATUS_PATH, resolved_status),
        (FINAL_BOUNDARY_CROSSING_PATH, boundary_crossing),
        (C5_BLOCK_AFTER_FINAL_CLOSURE_PATH, c5_block),
        (CLOSURE_INPUT_CONFIRMATION_PATH, input_confirmation),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, trace),
    ]:
        write_json(path, obj)

    acceptance_gate_results = {
        "FINAL_CLOSURE_0_DECISION_RECEIPT_CONSUMED": SOURCE_DECISION_RECEIPT_PATH.exists(),
        "FINAL_CLOSURE_1_AUTHORIZATION_CONSUMED": FINAL_AUTH_PATH.exists(),
        "FINAL_CLOSURE_2_FROZEN_REVIEWED_REFERENCE_CONSUMED": REVIEWED_REFERENCE_PATH.exists(),
        "FINAL_CLOSURE_3_FINAL_QA_CLOSURE_RECORDS_EMITTED": len(final_qa) == 3,
        "FINAL_CLOSURE_4_FINAL_SOURCE_REF_CLOSURE_RECORDS_EMITTED": len(final_source) == 2,
        "FINAL_CLOSURE_5_FINAL_UNDERTYPED_CLOSURE_RECORDS_EMITTED": len(final_undertyped) == 2,
        "FINAL_CLOSURE_6_PARKING_NOT_COUNTED_AS_RESOLUTION": all(x.get("counts_as_final_resolution") is False for x in final_parking),
        "FINAL_CLOSURE_7_FINAL_RESOLUTION_RECORDS_EMITTED": len(final_resolution) == 3 and all(x.get("weak_feedback_resolved") is True for x in final_resolution),
        "FINAL_CLOSURE_8_FINAL_ROUTE_RECORDS_EMITTED": len(final_routes) == 3 and all(x.get("final_resolution_record_emitted") is True for x in final_routes),
        "FINAL_CLOSURE_9_WEAK_FEEDBACK_RESOLVED": resolved_status["weak_feedback_resolved"] is True,
        "FINAL_CLOSURE_10_FINAL_BOUNDARY_CROSSED": boundary_crossing["final_resolution_boundary_crossed"] is True,
        "FINAL_CLOSURE_11_C5_NOT_READY_NOT_OPEN": rollup["c5_opened_count"] == 0 and rollup["c5_reconsideration_ready_count"] == 0,
        "FINAL_CLOSURE_12_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "FINAL_CLOSURE_13_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "FINAL_CLOSURE_14_REVIEW_READY": rollup["review_ready_count"] == 1,
        "FINAL_CLOSURE_15_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "FINAL_CLOSURE_16_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "FINAL_CLOSURE_17_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "final_resolution_records": len(final_resolution),
        "weak_feedback_resolved": execute_pass,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_final_resolution_closure_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_FINAL_RESOLUTION_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_post_review_reference_closure_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_final_resolution_closure_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "final_resolution_closure_executed": execute_pass,
            "review_ready": execute_pass,
            "question_packets_answered": execute_pass,
            "source_ref_requests_satisfied": execute_pass,
            "under_typed_acceptance_approved": execute_pass,
            "final_question_answer_closure_records_emitted_count": len(final_qa),
            "final_source_ref_closure_records_emitted_count": len(final_source),
            "final_under_typed_acceptance_closure_records_emitted_count": len(final_undertyped),
            "final_parking_closure_records_emitted_count": len(final_parking),
            "final_resolution_records_emitted_count": len(final_resolution),
            "resolution_records_emitted_count": len(final_resolution),
            "final_route_closure_records_emitted_count": len(final_routes),
            "weak_feedback_resolved": execute_pass,
            "final_resolution_boundary_crossed": execute_pass,
            "parking_counted_as_resolution": False,
            "c5_feedback_readiness": "BLOCKED_PENDING_C5_DECISION",
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
            "execution_record": rel(EXECUTION_RECORD_PATH),
            "final_question_answer_closure_records": rel(FINAL_QA_CLOSURE_RECORDS_PATH),
            "final_source_ref_satisfaction_closure_records": rel(FINAL_SOURCE_REF_CLOSURE_RECORDS_PATH),
            "final_under_typed_acceptance_closure_records": rel(FINAL_UNDERTYPED_CLOSURE_RECORDS_PATH),
            "final_parking_continuation_closure_records": rel(FINAL_PARKING_CLOSURE_RECORDS_PATH),
            "final_weak_feedback_resolution_records": rel(FINAL_RESOLUTION_RECORDS_PATH),
            "final_resolution_route_closure_records": rel(FINAL_ROUTE_CLOSURE_RECORDS_PATH),
            "resolved_status": rel(RESOLVED_STATUS_PATH),
            "final_boundary_crossing": rel(FINAL_BOUNDARY_CROSSING_PATH),
            "c5_block_after_final_closure": rel(C5_BLOCK_AFTER_FINAL_CLOSURE_PATH),
            "input_confirmation": rel(CLOSURE_INPUT_CONFIRMATION_PATH),
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
    print(f"final_resolution_closure_receipt_id={receipt_id}")
    print(f"final_resolution_closure_receipt_path={rel(receipt_path)}")
    print(f"final_resolution_closure_execution_record_path={rel(EXECUTION_RECORD_PATH)}")
    print(f"final_weak_feedback_resolution_records_path={rel(FINAL_RESOLUTION_RECORDS_PATH)}")
    print(f"weak_feedback_resolved_status_path={rel(RESOLVED_STATUS_PATH)}")
    print(f"final_resolution_boundary_crossing_path={rel(FINAL_BOUNDARY_CROSSING_PATH)}")
    print(f"c5_block_after_final_resolution_closure_path={rel(C5_BLOCK_AFTER_FINAL_CLOSURE_PATH)}")
    print(f"final_resolution_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"final_resolution_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
