#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXECUTE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_proposal_emission.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION"
MODE = "PROPOSAL_EMISSION_ONLY / FROM_REVIEWED_TEMPLATES / NO_REVIEWED_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_ONLY"

POST_DECISION_RECEIPT_ID = "1982e56e"
POST_DECISION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0_receipts/1982e56e.json"
POST_DECISION_BASIS_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_exec_target_post_closure_decision_basis_v0.json"
POST_DECISION_TABLE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_exec_target_post_closure_decision_table_v0.json"
POST_SELECTED_BRANCH_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_exec_target_selected_next_branch_v0.json"
POST_PROPOSAL_AUTH_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_weak_feedback_resolution_proposal_emission_authorization_v0.json"
POST_INPUT_SCOPE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_proposal_emission_input_scope_v0.json"
POST_UNRESOLVED_CONTINUATION_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_exec_target_post_closure_unresolved_continuation_v0.json"
POST_C5_BLOCK_CONTINUATION_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_exec_target_post_closure_c5_block_continuation_v0.json"
POST_DEFERRED_BRANCHES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_exec_target_post_closure_deferred_branches_v0.json"
POST_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_exec_target_post_closure_decision_authority_boundary_v0.json"
POST_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_exec_target_post_closure_decision_classification_v0.json"
POST_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_exec_target_post_closure_decision_rollup_v0.json"
POST_PROFILE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_exec_target_post_closure_decision_profile_v0.json"
POST_REPORT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_exec_target_post_closure_decision_report.json"
POST_TRACE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_post_closure_decision_v0/o2_exec_target_post_closure_decision_transition_trace.json"

EXEC_TARGET_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0_receipts/ab47a30d.json"
EXEC_TARGET_REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_target_reviewed_reference_v0.json"
EXEC_TEMPLATE_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_template_freeze_v0.json"
EXEC_ROUTE_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_weak_feedback_resolution_execution_proposal_route_freeze_v0.json"
EXEC_ZERO_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_resolution_execution_zero_record_freeze_v0.json"
EXEC_C5_FREEZE_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_closure_v0/o2_resolution_execution_c5_block_freeze_v0.json"

QA_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_question_answer_record_templates_v0.jsonl"
SOURCE_REF_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_source_ref_satisfaction_record_templates_v0.jsonl"
UNDERTYPED_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_under_typed_acceptance_review_record_templates_v0.jsonl"
PARKING_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_parking_execution_continuation_record_templates_v0.jsonl"
RESOLUTION_TEMPLATES_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_proposed_weak_feedback_resolution_record_templates_v0.jsonl"
PROPOSAL_ROUTE_MAP_PATH = ROOT / "data/o2_weak_feedback_resolution_execution_target_build_v0/o2_weak_feedback_resolution_execution_proposal_route_map_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    POST_DECISION_RECEIPT_PATH,
    POST_DECISION_BASIS_PATH,
    POST_DECISION_TABLE_PATH,
    POST_SELECTED_BRANCH_PATH,
    POST_PROPOSAL_AUTH_PATH,
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
    EXEC_TARGET_CLOSURE_RECEIPT_PATH,
    EXEC_TARGET_REVIEWED_REFERENCE_PATH,
    EXEC_TEMPLATE_FREEZE_PATH,
    EXEC_ROUTE_FREEZE_PATH,
    EXEC_ZERO_FREEZE_PATH,
    EXEC_C5_FREEZE_PATH,
    QA_TEMPLATES_PATH,
    SOURCE_REF_TEMPLATES_PATH,
    UNDERTYPED_TEMPLATES_PATH,
    PARKING_TEMPLATES_PATH,
    RESOLUTION_TEMPLATES_PATH,
    PROPOSAL_ROUTE_MAP_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposal_emission_v0_receipts"

EMISSION_RECORD_PATH = OUT_DIR / "o2_weak_feedback_resolution_proposal_emission_record_v0.json"
PROPOSED_QA_RECORDS_PATH = OUT_DIR / "o2_proposed_question_answer_records_v0.jsonl"
PROPOSED_SOURCE_REF_RECORDS_PATH = OUT_DIR / "o2_proposed_source_ref_satisfaction_records_v0.jsonl"
PROPOSED_UNDERTYPED_RECORDS_PATH = OUT_DIR / "o2_proposed_under_typed_acceptance_review_records_v0.jsonl"
PARKING_RECORDS_PATH = OUT_DIR / "o2_parking_execution_continuation_records_v0.jsonl"
PROPOSED_RESOLUTION_RECORDS_PATH = OUT_DIR / "o2_proposed_weak_feedback_resolution_records_v0.jsonl"
EMISSION_ROUTE_MAP_PATH = OUT_DIR / "o2_weak_feedback_resolution_proposal_emission_route_map_v0.jsonl"
EMISSION_GATE_READOUT_PATH = OUT_DIR / "o2_weak_feedback_resolution_proposal_emission_gate_readout_v0.json"
PROPOSAL_REVIEW_BOUNDARY_READOUT_PATH = OUT_DIR / "o2_proposal_emission_review_boundary_readout_v0.json"
C5_BLOCK_READOUT_PATH = OUT_DIR / "o2_proposal_emission_c5_block_readout_v0.json"
UNRESOLVED_CONTINUATION_PATH = OUT_DIR / "o2_proposal_emission_unresolved_continuation_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_proposal_emission_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_proposal_emission_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_proposal_emission_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_proposal_emission_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_proposal_emission_report.json"
TRACE_PATH = OUT_DIR / "o2_proposal_emission_transition_trace.json"

EXPECTED_DECISION_STATUS = "TYPED_O2_EXEC_TARGET_POST_CLOSURE_DECISION_SELECTED_PROPOSAL_EMISSION_EXECUTION_READY"
EXPECTED_DECISION_STOP = "STOP_TYPED_O2_EXEC_TARGET_POST_CLOSURE_DECISION_SELECTED_PROPOSAL_EMISSION_EXECUTION_READY"
EXPECTED_DECISION_NEXT = "EXECUTE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_V0"
RECOMMENDED_NEXT = "REVIEW_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_V0"

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

def record_id(prefix: str, template: Dict[str, Any]) -> str:
    return prefix + "_" + sha8(template)

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(POST_DECISION_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_exec_target_post_closure_decision_summary", {})
    basis = read_json(POST_DECISION_BASIS_PATH)
    selected = read_json(POST_SELECTED_BRANCH_PATH)
    auth = read_json(POST_PROPOSAL_AUTH_PATH)
    input_scope = read_json(POST_INPUT_SCOPE_PATH)
    unresolved = read_json(POST_UNRESOLVED_CONTINUATION_PATH)
    c5_block = read_json(POST_C5_BLOCK_CONTINUATION_PATH)
    post_authority = read_json(POST_AUTHORITY_PATH)
    post_classification = read_json(POST_CLASSIFICATION_PATH)
    post_rollup = read_json(POST_ROLLUP_PATH)
    post_profile = read_json(POST_PROFILE_PATH)

    closure_receipt = read_json(EXEC_TARGET_CLOSURE_RECEIPT_PATH)
    reviewed_ref = read_json(EXEC_TARGET_REVIEWED_REFERENCE_PATH)
    template_freeze = read_json(EXEC_TEMPLATE_FREEZE_PATH)
    route_freeze = read_json(EXEC_ROUTE_FREEZE_PATH)
    zero_freeze = read_json(EXEC_ZERO_FREEZE_PATH)
    c5_freeze = read_json(EXEC_C5_FREEZE_PATH)

    qa_templates = read_jsonl(QA_TEMPLATES_PATH)
    source_templates = read_jsonl(SOURCE_REF_TEMPLATES_PATH)
    undertyped_templates = read_jsonl(UNDERTYPED_TEMPLATES_PATH)
    parking_templates = read_jsonl(PARKING_TEMPLATES_PATH)
    resolution_templates = read_jsonl(RESOLUTION_TEMPLATES_PATH)
    proposal_routes = read_jsonl(PROPOSAL_ROUTE_MAP_PATH)

    if receipt.get("receipt_id") != POST_DECISION_RECEIPT_ID or receipt.get("gate") != "PASS":
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
    if summary.get("selected_next_branch") != "EXECUTE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION":
        failures.append("selected_branch_wrong")

    for key in [
        "post_closure_decision_complete",
        "proposal_emission_authorized_next",
        "execution_target_reference_closed",
        "templates_frozen_as_templates_only",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    expected_counts = {
        "question_answer_templates_available_count": 3,
        "source_ref_satisfaction_templates_available_count": 2,
        "under_typed_acceptance_review_templates_available_count": 2,
        "parking_execution_continuation_templates_available_count": 3,
        "proposed_resolution_record_templates_available_count": 3,
        "proposal_route_map_records_available_count": 3,
        "resolution_records_emitted_count": 0,
        "proposed_resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    for key in [
        "decision_unit_emitted_records",
        "execution_attempted",
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
    if input_scope.get("scope_status") != "FROZEN_TEMPLATES_ELIGIBLE_FOR_LATER_PROPOSAL_EMISSION":
        failures.append("input_scope_wrong")
    if unresolved.get("weak_feedback_resolved") is not False:
        failures.append("unresolved_continuation_wrong")
    if c5_block.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_block.get("c5_opened") is not False:
        failures.append("c5_block_wrong")
    if post_authority.get("may_execute_proposal_emission_next") is not True:
        failures.append("post_authority_no_emit_next")
    if post_authority.get("may_emit_records_now_in_decision_unit") is not False:
        failures.append("post_authority_allowed_decision_records")
    if post_classification.get("recommended_next") != EXPECTED_DECISION_NEXT:
        failures.append("post_classification_next_wrong")
    if post_rollup.get("proposal_emission_authorized_next_count") != 1:
        failures.append("post_rollup_auth_wrong")
    if post_profile.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("post_profile_next_wrong")

    if closure_receipt.get("receipt_id") != "ab47a30d":
        failures.append("closure_receipt_wrong")
    if reviewed_ref.get("templates_are_not_proposed_records") is not True or reviewed_ref.get("proposed_records_are_not_reviewed_records") is not True:
        failures.append("reviewed_reference_boundary_wrong")
    if template_freeze.get("templates_are_not_proposed_records") is not True:
        failures.append("template_freeze_wrong")
    if route_freeze.get("all_unresolved") is not True or route_freeze.get("proposed_records_emitted_count") != 0:
        failures.append("route_freeze_wrong")
    if zero_freeze.get("proposed_resolution_records_emitted_count") != 0 or zero_freeze.get("reviewed_resolution_records_emitted_count") != 0:
        failures.append("zero_freeze_wrong")
    if c5_freeze.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_freeze.get("c5_opened") is not False:
        failures.append("c5_freeze_wrong")

    if len(qa_templates) != 3 or len(source_templates) != 2 or len(undertyped_templates) != 2 or len(parking_templates) != 3 or len(resolution_templates) != 3 or len(proposal_routes) != 3:
        failures.append("template_counts_wrong")
    for row in resolution_templates:
        if row.get("proposal_status") != "TEMPLATE_ONLY":
            failures.append(f"resolution_template_not_template_only:{row.get('template_id')}")
        if row.get("review_status") != "UNREVIEWED":
            failures.append(f"resolution_template_not_unreviewed:{row.get('template_id')}")
        if row.get("counts_as_reviewed_resolution") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"resolution_template_counts_or_c5:{row.get('template_id')}")
    for row in proposal_routes:
        if row.get("current_resolution_state") != "UNRESOLVED":
            failures.append(f"proposal_route_not_unresolved:{row.get('proposal_route_record_id')}")
        if row.get("proposed_record_emitted") is not False or row.get("reviewed_record_emitted") is not False:
            failures.append(f"proposal_route_already_emitted:{row.get('proposal_route_record_id')}")
        if row.get("c5_reconsideration_ready") is not False:
            failures.append(f"proposal_route_c5_ready:{row.get('proposal_route_record_id')}")

    return failures, {
        "qa_templates": qa_templates,
        "source_templates": source_templates,
        "undertyped_templates": undertyped_templates,
        "parking_templates": parking_templates,
        "resolution_templates": resolution_templates,
        "proposal_routes": proposal_routes,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    qa_templates = src.get("qa_templates", [])
    source_templates = src.get("source_templates", [])
    undertyped_templates = src.get("undertyped_templates", [])
    parking_templates = src.get("parking_templates", [])
    resolution_templates = src.get("resolution_templates", [])
    proposal_routes = src.get("proposal_routes", [])

    qa_records = []
    qa_id_by_template: Dict[str, str] = {}
    for tmpl in qa_templates:
        rid = record_id("proposed_question_answer", tmpl)
        qa_id_by_template[tmpl.get("template_id")] = rid
        qa_records.append({
            "schema_version": "o2_proposed_question_answer_record_v0",
            "proposed_answer_id": rid,
            "source_template_ref": tmpl.get("template_id"),
            "source_answer_skeleton_ref": tmpl.get("source_answer_skeleton_ref"),
            "source_question_packet_ref": tmpl.get("source_question_packet_ref"),
            "answer_payload_or_ref": tmpl.get("answer_payload_or_ref"),
            "evidence_refs": tmpl.get("evidence_refs", []),
            "proposal_status": "PROPOSED_UNREVIEWED",
            "review_status": "UNREVIEWED",
            "counts_as_answer": False,
            "counts_as_resolution_input": False,
        })

    source_records = []
    source_id_by_template: Dict[str, str] = {}
    for tmpl in source_templates:
        rid = record_id("proposed_source_ref_satisfaction", tmpl)
        source_id_by_template[tmpl.get("template_id")] = rid
        source_records.append({
            "schema_version": "o2_proposed_source_ref_satisfaction_record_v0",
            "proposed_satisfaction_id": rid,
            "source_template_ref": tmpl.get("template_id"),
            "source_satisfaction_skeleton_ref": tmpl.get("source_satisfaction_skeleton_ref"),
            "source_ref_request_ref": tmpl.get("source_ref_request_ref"),
            "proposed_source_refs": tmpl.get("proposed_source_refs", []),
            "proposal_status": "PROPOSED_UNREVIEWED",
            "review_status": "UNREVIEWED",
            "counts_as_satisfied": False,
            "counts_as_resolution_input": False,
        })

    undertyped_records = []
    undertyped_id_by_template: Dict[str, str] = {}
    for tmpl in undertyped_templates:
        rid = record_id("proposed_under_typed_acceptance_review", tmpl)
        undertyped_id_by_template[tmpl.get("template_id")] = rid
        undertyped_records.append({
            "schema_version": "o2_proposed_under_typed_acceptance_review_record_v0",
            "proposed_review_id": rid,
            "source_template_ref": tmpl.get("template_id"),
            "source_review_skeleton_ref": tmpl.get("source_review_skeleton_ref"),
            "proposed_decision": tmpl.get("proposed_decision", "KEEP_CANDIDATE_ONLY"),
            "proposal_status": "PROPOSED_UNREVIEWED",
            "review_status": "UNREVIEWED",
            "counts_as_approved": False,
            "c5_unblock_allowed": False,
        })

    parking_records = []
    parking_id_by_template: Dict[str, str] = {}
    for tmpl in parking_templates:
        rid = record_id("parking_execution_continuation", tmpl)
        parking_id_by_template[tmpl.get("template_id")] = rid
        parking_records.append({
            "schema_version": "o2_parking_execution_continuation_record_v0",
            "parking_execution_id": rid,
            "source_template_ref": tmpl.get("template_id"),
            "source_parking_skeleton_ref": tmpl.get("source_parking_skeleton_ref"),
            "continue_parking": True,
            "proposal_status": "PARKED_UNRESOLVED_UNREVIEWED",
            "review_status": "UNREVIEWED",
            "counts_as_resolution": False,
            "c5_unblock_allowed": False,
        })

    resolution_records = []
    resolution_id_by_template: Dict[str, str] = {}
    for tmpl in resolution_templates:
        rid = record_id("proposed_weak_feedback_resolution", tmpl)
        resolution_id_by_template[tmpl.get("template_id")] = rid
        qa_refs = [qa_id_by_template[x] for x in tmpl.get("proposed_question_answer_template_refs", []) if x in qa_id_by_template]
        source_refs = [source_id_by_template[x] for x in tmpl.get("proposed_source_ref_satisfaction_template_refs", []) if x in source_id_by_template]
        undertyped_refs = [undertyped_id_by_template[x] for x in tmpl.get("proposed_under_typed_review_template_refs", []) if x in undertyped_id_by_template]
        parking_refs = [parking_id_by_template[x] for x in tmpl.get("parking_continuation_template_refs", []) if x in parking_id_by_template]
        resolution_records.append({
            "schema_version": "o2_proposed_weak_feedback_resolution_record_v0",
            "proposed_resolution_id": rid,
            "source_template_ref": tmpl.get("template_id"),
            "source_route_map_ref": tmpl.get("source_route_map_ref"),
            "proposed_question_answer_refs": qa_refs,
            "proposed_source_ref_satisfaction_refs": source_refs,
            "proposed_under_typed_review_refs": undertyped_refs,
            "parking_continuation_refs": parking_refs,
            "proposed_resolution_decision": "REMAINS_UNRESOLVED_PENDING_REVIEW",
            "proposal_status": "PROPOSED_UNREVIEWED",
            "review_status": "UNREVIEWED",
            "counts_as_reviewed_resolution": False,
            "weak_feedback_resolved": False,
            "c5_reconsideration_ready": False,
        })

    emission_routes = []
    for route in proposal_routes:
        proposal_template_ref = route.get("proposal_template_ref")
        emission_routes.append({
            "schema_version": "o2_weak_feedback_resolution_proposal_emission_route_record_v0",
            "emission_route_record_id": "emission_route_" + sha8(route),
            "source_proposal_route_record_id": route.get("proposal_route_record_id"),
            "source_feedback_ref": route.get("source_feedback_ref"),
            "source_route_map_ref": route.get("source_route_map_ref"),
            "current_resolution_state": "UNRESOLVED",
            "proposal_template_ref": proposal_template_ref,
            "proposed_resolution_record_ref": resolution_id_by_template.get(proposal_template_ref),
            "proposed_record_emitted": proposal_template_ref in resolution_id_by_template,
            "reviewed_record_emitted": False,
            "review_status": "UNREVIEWED",
            "weak_feedback_resolved": False,
            "c5_reconsideration_ready": False,
        })

    if len(qa_records) != 3:
        failures.append(f"qa_records_count_wrong:{len(qa_records)}")
    if len(source_records) != 2:
        failures.append(f"source_records_count_wrong:{len(source_records)}")
    if len(undertyped_records) != 2:
        failures.append(f"undertyped_records_count_wrong:{len(undertyped_records)}")
    if len(parking_records) != 3:
        failures.append(f"parking_records_count_wrong:{len(parking_records)}")
    if len(resolution_records) != 3:
        failures.append(f"resolution_records_count_wrong:{len(resolution_records)}")
    if len(emission_routes) != 3:
        failures.append(f"emission_routes_count_wrong:{len(emission_routes)}")

    for row in qa_records:
        if row.get("review_status") != "UNREVIEWED" or row.get("counts_as_answer") is not False:
            failures.append(f"qa_record_bad_boundary:{row.get('proposed_answer_id')}")
    for row in source_records:
        if row.get("review_status") != "UNREVIEWED" or row.get("counts_as_satisfied") is not False:
            failures.append(f"source_record_bad_boundary:{row.get('proposed_satisfaction_id')}")
    for row in undertyped_records:
        if row.get("review_status") != "UNREVIEWED" or row.get("counts_as_approved") is not False:
            failures.append(f"undertyped_record_bad_boundary:{row.get('proposed_review_id')}")
    for row in parking_records:
        if row.get("review_status") != "UNREVIEWED" or row.get("counts_as_resolution") is not False:
            failures.append(f"parking_record_bad_boundary:{row.get('parking_execution_id')}")
    for row in resolution_records:
        if row.get("review_status") != "UNREVIEWED":
            failures.append(f"resolution_record_not_unreviewed:{row.get('proposed_resolution_id')}")
        if row.get("counts_as_reviewed_resolution") is not False or row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"resolution_record_bad_boundary:{row.get('proposed_resolution_id')}")
    for row in emission_routes:
        if row.get("current_resolution_state") != "UNRESOLVED":
            failures.append(f"emission_route_state_wrong:{row.get('emission_route_record_id')}")
        if row.get("proposed_record_emitted") is not True or row.get("reviewed_record_emitted") is not False:
            failures.append(f"emission_route_emission_flags_wrong:{row.get('emission_route_record_id')}")
        if row.get("weak_feedback_resolved") is not False or row.get("c5_reconsideration_ready") is not False:
            failures.append(f"emission_route_resolution_or_c5_wrong:{row.get('emission_route_record_id')}")

    emission_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_EXECUTED_PROPOSED_RECORDS_REVIEW_READY" if emission_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if emission_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_EXECUTED",
        "POST_CLOSURE_DECISION_RECEIPT_CONSUMED",
        "REVIEWED_TEMPLATE_SURFACE_CONSUMED",
        "PROPOSED_QUESTION_ANSWER_RECORDS_EMITTED_UNREVIEWED",
        "PROPOSED_SOURCE_REF_SATISFACTION_RECORDS_EMITTED_UNREVIEWED",
        "PROPOSED_UNDER_TYPED_ACCEPTANCE_REVIEW_RECORDS_EMITTED_UNREVIEWED",
        "PARKING_CONTINUATION_RECORDS_EMITTED_UNRESOLVED",
        "PROPOSED_WEAK_FEEDBACK_RESOLUTION_RECORDS_EMITTED_UNREVIEWED",
        "PROPOSAL_EMISSION_ROUTE_MAP_EMITTED",
        "PROPOSAL_REVIEW_BOUNDARY_PRESERVED",
        "C5_BLOCK_PRESERVED",
        "NO_REVIEWED_RESOLUTION_RECORDS_EMITTED",
        "NO_WEAK_FEEDBACK_RESOLUTION_RECORDED",
        "NO_QUESTION_PACKET_ANSWERED_AS_REVIEWED",
        "NO_SOURCE_REF_REQUEST_SATISFIED_AS_REVIEWED",
        "NO_UNDER_TYPED_ACCEPTANCE_APPROVED_AS_REVIEWED",
        "NO_PARKING_COUNTED_AS_RESOLUTION",
        "NO_C5_RECONSIDERATION_READY",
        "NO_C5_OPENED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
    ] if emission_pass else failures

    emission_record = {
        "schema_version": "o2_weak_feedback_resolution_proposal_emission_record_v0",
        "emission_status": "PROPOSED_RECORDS_EMITTED_REVIEW_READY" if emission_pass else "EMISSION_FAIL",
        "source_post_closure_decision_receipt_id": POST_DECISION_RECEIPT_ID,
        "proposal_emission_executed": emission_pass,
        "emission_counts": {
            "proposed_question_answer_records": len(qa_records),
            "proposed_source_ref_satisfaction_records": len(source_records),
            "proposed_under_typed_acceptance_review_records": len(undertyped_records),
            "parking_execution_continuation_records": len(parking_records),
            "proposed_weak_feedback_resolution_records": len(resolution_records),
            "proposal_emission_route_records": len(emission_routes),
        },
        "emission_does_not_mean": [
            "reviewed resolution records emitted",
            "weak feedback resolved",
            "question packets answered as reviewed answers",
            "source-ref requests satisfied as reviewed satisfaction",
            "under-typed acceptance approved as reviewed approval",
            "parking counted as resolution",
            "C5 reconsideration ready",
            "C5 opened",
        ],
    }

    gate_readout = {
        "schema_version": "o2_weak_feedback_resolution_proposal_emission_gate_readout_v0",
        "gate_status": "PROPOSAL_EMISSION_EXECUTED_REVIEW_REQUIRED" if emission_pass else "PROPOSAL_EMISSION_FAIL",
        "proposal_emission_executed": emission_pass,
        "proposed_question_answer_records_emitted_count": len(qa_records),
        "proposed_source_ref_satisfaction_records_emitted_count": len(source_records),
        "proposed_under_typed_acceptance_review_records_emitted_count": len(undertyped_records),
        "parking_execution_continuation_records_emitted_count": len(parking_records),
        "proposed_resolution_records_emitted_count": len(resolution_records),
        "reviewed_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "review_required_next": emission_pass,
    }

    boundary_readout = {
        "schema_version": "o2_proposal_emission_review_boundary_readout_v0",
        "boundary_status": "PROPOSAL_LAYER_OPEN_REVIEW_LAYER_NOT_CROSSED",
        "template_layer_crossed_into_proposal_layer": emission_pass,
        "proposal_layer_crossed_into_review_layer": False,
        "all_proposed_records_unreviewed": True,
        "proposed_records_are_not_reviewed_records": True,
        "review_required_next": emission_pass,
    }

    c5_readout = {
        "schema_version": "o2_proposal_emission_c5_block_readout_v0",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "block_enforced": True,
        "reason": "Proposal emission produced unreviewed proposed records only. Reviewed resolution does not exist.",
    }

    unresolved_continuation = {
        "schema_version": "o2_proposal_emission_unresolved_continuation_v0",
        "unresolved_status_continues": True,
        "proposal_emission_executed": emission_pass,
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
    }

    write_json(EMISSION_RECORD_PATH, emission_record)
    write_jsonl(PROPOSED_QA_RECORDS_PATH, qa_records)
    write_jsonl(PROPOSED_SOURCE_REF_RECORDS_PATH, source_records)
    write_jsonl(PROPOSED_UNDERTYPED_RECORDS_PATH, undertyped_records)
    write_jsonl(PARKING_RECORDS_PATH, parking_records)
    write_jsonl(PROPOSED_RESOLUTION_RECORDS_PATH, resolution_records)
    write_jsonl(EMISSION_ROUTE_MAP_PATH, emission_routes)
    write_json(EMISSION_GATE_READOUT_PATH, gate_readout)
    write_json(PROPOSAL_REVIEW_BOUNDARY_READOUT_PATH, boundary_readout)
    write_json(C5_BLOCK_READOUT_PATH, c5_readout)
    write_json(UNRESOLVED_CONTINUATION_PATH, unresolved_continuation)

    authority_boundary = {
        "schema_version": "o2_proposal_emission_authority_boundary_v0",
        "status": status,
        "may_review_proposal_emission_next": emission_pass,
        "may_emit_proposed_records_now": False,
        "may_emit_reviewed_resolution_records_now": False,
        "may_resolve_weak_feedback_now": False,
        "may_answer_question_packets_as_reviewed_now": False,
        "may_satisfy_source_ref_requests_as_reviewed_now": False,
        "may_approve_under_typed_acceptance_as_reviewed_now": False,
        "may_count_parking_as_resolution": False,
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
        "schema_version": "o2_proposal_emission_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "proposal_emission_executed": emission_pass,
        "proposal_records_emitted": emission_pass,
        "review_ready": emission_pass,
        "proposed_question_answer_records_emitted_count": len(qa_records),
        "proposed_source_ref_satisfaction_records_emitted_count": len(source_records),
        "proposed_under_typed_acceptance_review_records_emitted_count": len(undertyped_records),
        "parking_execution_continuation_records_emitted_count": len(parking_records),
        "proposed_resolution_records_emitted_count": len(resolution_records),
        "proposal_emission_route_records_count": len(emission_routes),
        "weak_feedback_resolved": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
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
        "schema_version": "o2_proposal_emission_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "proposal_emission_execution_count": 1 if emission_pass else 0,
        "review_ready_count": 1 if emission_pass else 0,
        "proposed_question_answer_records_emitted_count": len(qa_records),
        "proposed_source_ref_satisfaction_records_emitted_count": len(source_records),
        "proposed_under_typed_acceptance_review_records_emitted_count": len(undertyped_records),
        "parking_execution_continuation_records_emitted_count": len(parking_records),
        "proposed_resolution_records_emitted_count": len(resolution_records),
        "proposal_emission_route_records_count": len(emission_routes),
        "weak_feedback_resolved_count": 0,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": 0,
        "question_packets_answered_count": 0,
        "source_ref_requests_satisfied_count": 0,
        "under_typed_acceptance_approved_count": 0,
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
        "reviewed_resolution_records_emitted_count",
        "question_packets_answered_count",
        "source_ref_requests_satisfied_count",
        "under_typed_acceptance_approved_count",
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
        "schema_version": "o2_proposal_emission_profile_v0",
        "profile_id": "o2_proposal_emission_profile_" + sha8(rollup),
        "status": status,
        "proposal_emission_executed": emission_pass,
        "proposal_records_emitted": emission_pass,
        "review_ready": emission_pass,
        "proposed_resolution_records_emitted_count": len(resolution_records),
        "reviewed_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Review the emitted proposal records next. Do not count proposed records as reviewed resolution.",
        "must_not_infer": [
            "reviewed resolution records emitted",
            "weak feedback resolved",
            "question packet answered as reviewed",
            "source-ref request satisfied as reviewed",
            "under-typed acceptance approved as reviewed",
            "parking resolved weak feedback",
            "C5 reconsideration ready",
            "C5 opened",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_proposal_emission_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Proposal emission executed from the reviewed execution-target template surface. Proposed records were emitted and remain unreviewed. No reviewed resolution records were emitted; weak feedback remains unresolved; C5 remains blocked.",
        "proposal_emission_executed": emission_pass,
        "proposed_resolution_records_emitted_count": len(resolution_records),
        "reviewed_resolution_records_emitted_count": 0,
        "resolution_records_emitted_count": 0,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_proposal_emission_transition_trace_v0",
        "trace": [
            {
                "step": "consume_post_closure_decision",
                "question": "is proposal emission authorized",
                "answer": "yes" if emission_pass else "no",
                "taken": "emit proposed records from reviewed templates",
            },
            {
                "step": "cross_template_to_proposal_boundary",
                "question": "are emitted records reviewed records",
                "answer": "no",
                "taken": "mark all emitted records UNREVIEWED",
            },
            {
                "step": "preserve_resolution_and_c5_boundary",
                "question": "does proposal emission resolve weak feedback or unblock C5",
                "answer": "no",
                "taken": "review emitted proposals next",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    write_json(AUTHORITY_BOUNDARY_PATH, authority_boundary)
    write_json(CLASSIFICATION_PATH, classification)
    write_json(ROLLUP_PATH, rollup)
    write_json(PROFILE_PATH, profile)
    write_json(REPORT_PATH, report)
    write_json(TRACE_PATH, trace)

    acceptance_gate_results = {
        "PROPOSAL_EMISSION_0_POST_DECISION_RECEIPT_CONSUMED": POST_DECISION_RECEIPT_PATH.exists(),
        "PROPOSAL_EMISSION_1_EMISSION_RECORD_EMITTED": EMISSION_RECORD_PATH.exists(),
        "PROPOSAL_EMISSION_2_PROPOSED_QA_RECORDS_EMITTED": len(qa_records) == 3,
        "PROPOSAL_EMISSION_3_PROPOSED_SOURCE_REF_RECORDS_EMITTED": len(source_records) == 2,
        "PROPOSAL_EMISSION_4_PROPOSED_UNDERTYPED_RECORDS_EMITTED": len(undertyped_records) == 2,
        "PROPOSAL_EMISSION_5_PARKING_RECORDS_EMITTED_UNRESOLVED": len(parking_records) == 3,
        "PROPOSAL_EMISSION_6_PROPOSED_RESOLUTION_RECORDS_EMITTED": len(resolution_records) == 3,
        "PROPOSAL_EMISSION_7_EMISSION_ROUTE_MAP_EMITTED": len(emission_routes) == 3,
        "PROPOSAL_EMISSION_8_ALL_PROPOSALS_UNREVIEWED": all(x.get("review_status") == "UNREVIEWED" for x in qa_records + source_records + undertyped_records + parking_records + resolution_records),
        "PROPOSAL_EMISSION_9_NO_REVIEWED_RESOLUTION_RECORDS": rollup["reviewed_resolution_records_emitted_count"] == 0 and rollup["resolution_records_emitted_count"] == 0,
        "PROPOSAL_EMISSION_10_WEAK_FEEDBACK_NOT_RESOLVED": rollup["weak_feedback_resolved_count"] == 0,
        "PROPOSAL_EMISSION_11_NO_ANSWER_SATISFY_APPROVE": rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "PROPOSAL_EMISSION_12_NO_PARKING_AS_RESOLUTION": rollup["parked_records_counted_as_resolved_count"] == 0,
        "PROPOSAL_EMISSION_13_C5_BLOCK_PRESERVED": rollup["c5_opened_count"] == 0 and rollup["c5_reconsideration_ready_count"] == 0,
        "PROPOSAL_EMISSION_14_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "PROPOSAL_EMISSION_15_NO_REPAIR_RETRY_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "PROPOSAL_EMISSION_16_REVIEW_READY": rollup["review_ready_count"] == 1,
        "PROPOSAL_EMISSION_17_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "PROPOSAL_EMISSION_18_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "PROPOSAL_EMISSION_19_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "proposed_resolution_records": len(resolution_records),
        "reviewed_records": 0,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_resolution_proposal_emission_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSAL_EMISSION_RECEIPT",
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
        "machine_readable_o2_weak_feedback_resolution_proposal_emission_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "proposal_emission_executed": emission_pass,
            "proposal_records_emitted": emission_pass,
            "review_ready": emission_pass,
            "proposed_question_answer_records_emitted_count": len(qa_records),
            "proposed_source_ref_satisfaction_records_emitted_count": len(source_records),
            "proposed_under_typed_acceptance_review_records_emitted_count": len(undertyped_records),
            "parking_execution_continuation_records_emitted_count": len(parking_records),
            "proposed_resolution_records_emitted_count": len(resolution_records),
            "proposal_emission_route_records_count": len(emission_routes),
            "all_proposed_records_unreviewed": True,
            "proposal_review_boundary_crossed": False,
            "weak_feedback_resolved": False,
            "resolution_records_emitted_count": 0,
            "reviewed_resolution_records_emitted_count": 0,
            "question_packets_answered": False,
            "source_ref_requests_satisfied": False,
            "under_typed_acceptance_approved": False,
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
            "emission_record": rel(EMISSION_RECORD_PATH),
            "proposed_question_answer_records": rel(PROPOSED_QA_RECORDS_PATH),
            "proposed_source_ref_satisfaction_records": rel(PROPOSED_SOURCE_REF_RECORDS_PATH),
            "proposed_under_typed_acceptance_review_records": rel(PROPOSED_UNDERTYPED_RECORDS_PATH),
            "parking_execution_continuation_records": rel(PARKING_RECORDS_PATH),
            "proposed_weak_feedback_resolution_records": rel(PROPOSED_RESOLUTION_RECORDS_PATH),
            "emission_route_map": rel(EMISSION_ROUTE_MAP_PATH),
            "emission_gate_readout": rel(EMISSION_GATE_READOUT_PATH),
            "proposal_review_boundary_readout": rel(PROPOSAL_REVIEW_BOUNDARY_READOUT_PATH),
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
    print(f"proposal_emission_receipt_id={receipt_id}")
    print(f"proposal_emission_receipt_path={rel(receipt_path)}")
    print(f"proposal_emission_record_path={rel(EMISSION_RECORD_PATH)}")
    print(f"proposed_question_answer_records_path={rel(PROPOSED_QA_RECORDS_PATH)}")
    print(f"proposed_source_ref_satisfaction_records_path={rel(PROPOSED_SOURCE_REF_RECORDS_PATH)}")
    print(f"proposed_under_typed_acceptance_review_records_path={rel(PROPOSED_UNDERTYPED_RECORDS_PATH)}")
    print(f"parking_execution_continuation_records_path={rel(PARKING_RECORDS_PATH)}")
    print(f"proposed_weak_feedback_resolution_records_path={rel(PROPOSED_RESOLUTION_RECORDS_PATH)}")
    print(f"proposal_emission_route_map_path={rel(EMISSION_ROUTE_MAP_PATH)}")
    print(f"proposal_emission_gate_readout_path={rel(EMISSION_GATE_READOUT_PATH)}")
    print(f"proposal_emission_rollup_path={rel(ROLLUP_PATH)}")
    print(f"proposal_emission_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
