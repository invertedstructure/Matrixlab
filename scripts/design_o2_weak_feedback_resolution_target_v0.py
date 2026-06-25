#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DESIGN_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_target.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGN"
MODE = "DESIGN_ONLY / DEFINE_RESOLUTION_TARGET / NO_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGN_ONLY"

WFH_DECISION_RECEIPT_ID = "694e859c"
WFH_DECISION_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0_receipts/694e859c.json"
WFH_DECISION_BASIS_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0/o2_wfh_post_closure_decision_basis_v0.json"
WFH_DECISION_TABLE_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0/o2_wfh_post_closure_decision_table_v0.json"
WFH_SELECTED_BRANCH_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0/o2_wfh_selected_next_branch_v0.json"
WFH_RESOLUTION_AUTH_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0/o2_weak_feedback_resolution_target_authorization_v0.json"
WFH_UNRESOLVED_CONT_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0/o2_weak_feedback_unresolved_block_continuation_v0.json"
WFH_C5_CONT_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0/o2_wfh_c5_block_continuation_v0.json"
WFH_DEFERRED_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0/o2_wfh_deferred_branches_v0.json"
WFH_DECISION_AUTHORITY_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0/o2_wfh_post_closure_decision_authority_boundary_v0.json"
WFH_DECISION_CLASSIFICATION_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0/o2_wfh_post_closure_decision_classification_v0.json"
WFH_DECISION_ROLLUP_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0/o2_wfh_post_closure_decision_rollup_v0.json"
WFH_DECISION_PROFILE_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0/o2_wfh_post_closure_decision_profile_v0.json"
WFH_DECISION_REPORT_PATH = ROOT / "data/o2_weak_feedback_handling_post_closure_decision_v0/o2_wfh_post_closure_decision_report.json"

WFH_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0_receipts/07cfbdec.json"
WFH_REVIEWED_REFERENCE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_handling_reviewed_reference_v0.json"
WFH_UNRESOLVED_FREEZE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_unresolved_status_freeze_v0.json"
WFH_C5_BLOCK_FREEZE_PATH = ROOT / "data/o2_weak_feedback_handling_closure_v0/o2_weak_feedback_c5_block_freeze_v0.json"

WFH_HANDLING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_handling_records_v0.jsonl"
WFH_QUESTION_PACKETS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_question_packets_v0.jsonl"
WFH_SOURCE_REF_REQUESTS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_source_ref_requests_v0.jsonl"
WFH_UNDERTYPED_CANDIDATES_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_under_typed_acceptance_candidates_v0.jsonl"
WFH_PARKING_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_parking_records_v0.jsonl"
WFH_C5_BLOCK_RECORDS_PATH = ROOT / "data/o2_weak_feedback_handling_v0/o2_weak_feedback_c5_block_records_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    WFH_DECISION_RECEIPT_PATH,
    WFH_DECISION_BASIS_PATH,
    WFH_DECISION_TABLE_PATH,
    WFH_SELECTED_BRANCH_PATH,
    WFH_RESOLUTION_AUTH_PATH,
    WFH_UNRESOLVED_CONT_PATH,
    WFH_C5_CONT_PATH,
    WFH_DEFERRED_PATH,
    WFH_DECISION_AUTHORITY_PATH,
    WFH_DECISION_CLASSIFICATION_PATH,
    WFH_DECISION_ROLLUP_PATH,
    WFH_DECISION_PROFILE_PATH,
    WFH_DECISION_REPORT_PATH,
    WFH_CLOSURE_RECEIPT_PATH,
    WFH_REVIEWED_REFERENCE_PATH,
    WFH_UNRESOLVED_FREEZE_PATH,
    WFH_C5_BLOCK_FREEZE_PATH,
    WFH_HANDLING_RECORDS_PATH,
    WFH_QUESTION_PACKETS_PATH,
    WFH_SOURCE_REF_REQUESTS_PATH,
    WFH_UNDERTYPED_CANDIDATES_PATH,
    WFH_PARKING_RECORDS_PATH,
    WFH_C5_BLOCK_RECORDS_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_target_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_target_v0_receipts"

TARGET_DEFINITION_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_definition_v0.json"
INPUT_SURFACE_INVENTORY_PATH = OUT_DIR / "o2_weak_feedback_resolution_input_surface_inventory_v0.json"
RESOLUTION_STATE_ENUM_PATH = OUT_DIR / "o2_weak_feedback_resolution_state_enum_v0.json"
QUESTION_ANSWER_CONTRACT_PATH = OUT_DIR / "o2_question_packet_answer_contract_v0.json"
SOURCE_REF_SATISFACTION_CONTRACT_PATH = OUT_DIR / "o2_source_ref_satisfaction_contract_v0.json"
UNDERTYPED_REVIEW_CONTRACT_PATH = OUT_DIR / "o2_under_typed_acceptance_review_contract_v0.json"
PARKING_CONTINUATION_CONTRACT_PATH = OUT_DIR / "o2_parking_continuation_contract_v0.json"
RESOLUTION_GATE_CONTRACT_PATH = OUT_DIR / "o2_weak_feedback_resolution_gate_contract_v0.json"
C5_RECONSIDERATION_RULE_PATH = OUT_DIR / "o2_c5_reconsideration_rule_v0.json"
NEGATIVE_CONTROLS_PATH = OUT_DIR / "o2_weak_feedback_resolution_negative_controls_v0.json"
ACCEPTANCE_GATES_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_acceptance_gates_v0.json"
TERMINAL_RULES_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_terminal_rules_v0.json"
BUILD_AUTHORIZATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_build_authorization_v0.json"
C5_BLOCK_CONTINUATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_c5_block_continuation_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_report.json"
TRACE_PATH = OUT_DIR / "o2_weak_feedback_resolution_target_transition_trace.json"

EXPECTED_DECISION_STATUS = "TYPED_O2_WFH_POST_CLOSURE_DECISION_SELECTED_WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGN_READY"
EXPECTED_DECISION_STOP = "STOP_TYPED_O2_WFH_POST_CLOSURE_DECISION_SELECTED_WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGN_READY"
EXPECTED_DECISION_NEXT = "DESIGN_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_V0"
AUTHORIZED_BUILD_UNIT = "BUILD_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_V0"

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

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(WFH_DECISION_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_wfh_post_closure_decision_summary", {})
    selected = read_json(WFH_SELECTED_BRANCH_PATH)
    auth = read_json(WFH_RESOLUTION_AUTH_PATH)
    unresolved = read_json(WFH_UNRESOLVED_CONT_PATH)
    c5_cont = read_json(WFH_C5_CONT_PATH)
    authority = read_json(WFH_DECISION_AUTHORITY_PATH)
    rollup = read_json(WFH_DECISION_ROLLUP_PATH)
    profile = read_json(WFH_DECISION_PROFILE_PATH)

    closure_receipt = read_json(WFH_CLOSURE_RECEIPT_PATH)
    reviewed_reference = read_json(WFH_REVIEWED_REFERENCE_PATH)
    unresolved_freeze = read_json(WFH_UNRESOLVED_FREEZE_PATH)
    c5_freeze = read_json(WFH_C5_BLOCK_FREEZE_PATH)

    handling = read_jsonl(WFH_HANDLING_RECORDS_PATH)
    questions = read_jsonl(WFH_QUESTION_PACKETS_PATH)
    source_refs = read_jsonl(WFH_SOURCE_REF_REQUESTS_PATH)
    acceptances = read_jsonl(WFH_UNDERTYPED_CANDIDATES_PATH)
    parking = read_jsonl(WFH_PARKING_RECORDS_PATH)
    c5_blocks = read_jsonl(WFH_C5_BLOCK_RECORDS_PATH)

    if receipt.get("receipt_id") != WFH_DECISION_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("post_closure_decision_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_DECISION_STOP:
        failures.append("post_closure_decision_stop_wrong")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("post_closure_decision_hidden_next_command")
    if summary.get("status") != EXPECTED_DECISION_STATUS:
        failures.append(f"post_closure_decision_status_wrong:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_DECISION_NEXT:
        failures.append(f"post_closure_decision_next_wrong:{summary.get('recommended_next')}")
    if summary.get("selected_next_branch") != "DESIGN_O2_WEAK_FEEDBACK_RESOLUTION_TARGET":
        failures.append("selected_branch_wrong")
    if summary.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("selected_next_unit_wrong")

    for key in ["post_closure_decision_complete", "weak_feedback_handling_reference_closed", "bad_counters_zero"]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    for key in [
        "weak_feedback_resolved",
        "question_packets_answered",
        "source_ref_requests_satisfied",
        "under_typed_acceptance_approved",
        "parking_counted_as_resolution",
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

    expected_counts = {
        "handling_records_available_count": 3,
        "question_packet_candidates_available_count": 3,
        "source_ref_request_candidates_available_count": 2,
        "under_typed_acceptance_candidates_available_count": 2,
        "parking_records_available_count": 3,
        "c5_block_records_available_count": 3,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"available_count_wrong:{key}:{summary.get(key)}")

    if summary.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("summary_c5_not_blocked")
    if selected.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("selected_branch_artifact_wrong")
    if auth.get("authorization_status") != "TARGET_DESIGN_AUTHORIZED":
        failures.append("resolution_target_auth_not_authorized")
    if auth.get("authorized_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("resolution_target_auth_next_wrong")
    if unresolved.get("weak_feedback_resolved") is not False:
        failures.append("unresolved_continuation_resolved")
    if c5_cont.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_cont.get("c5_opened") is not False:
        failures.append("c5_continuation_wrong")
    if authority.get("may_design_o2_weak_feedback_resolution_target_next") is not True:
        failures.append("authority_no_design_resolution_target")
    if authority.get("may_open_c5") is not False:
        failures.append("authority_allows_c5")
    if rollup.get("selected_resolution_target_design_count") != 1:
        failures.append("rollup_selected_target_wrong")
    if profile.get("selected_next_unit") != EXPECTED_DECISION_NEXT:
        failures.append("profile_next_wrong")

    if closure_receipt.get("receipt_id") != "07cfbdec":
        failures.append("closure_receipt_wrong")
    if reviewed_reference.get("weak_feedback_resolved") is not False:
        failures.append("reviewed_reference_resolved")
    if unresolved_freeze.get("weak_feedback_resolved") is not False:
        failures.append("unresolved_freeze_resolved")
    if c5_freeze.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK" or c5_freeze.get("c5_opened") is not False:
        failures.append("c5_freeze_wrong")

    if len(handling) != 3 or len(questions) != 3 or len(source_refs) != 2 or len(acceptances) != 2 or len(parking) != 3 or len(c5_blocks) != 3:
        failures.append("source_artifact_counts_wrong")

    return failures, {
        "summary": summary,
        "handling": handling,
        "questions": questions,
        "source_refs": source_refs,
        "acceptances": acceptances,
        "parking": parking,
        "c5_blocks": c5_blocks,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    summary = src.get("summary", {})
    handling = src.get("handling", [])
    questions = src.get("questions", [])
    source_refs = src.get("source_refs", [])
    acceptances = src.get("acceptances", [])
    parking = src.get("parking", [])
    c5_blocks = src.get("c5_blocks", [])

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    design_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGNED_BUILD_READY" if design_pass else "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGN_BASIS_FAIL"
    recommended_next = AUTHORIZED_BUILD_UNIT if design_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGN_BASIS_V0"

    reason_codes = [
        "WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGNED",
        "WFH_POST_CLOSURE_DECISION_RECEIPT_CONSUMED",
        "REVIEWED_HANDLING_REFERENCE_CONFIRMED",
        "UNRESOLVED_WEAK_FEEDBACK_SURFACE_CONFIRMED",
        "RESOLUTION_STATE_ENUM_FROZEN",
        "QUESTION_ANSWER_CONTRACT_FROZEN",
        "SOURCE_REF_SATISFACTION_CONTRACT_FROZEN",
        "UNDER_TYPED_ACCEPTANCE_REVIEW_CONTRACT_FROZEN",
        "PARKING_CONTINUATION_CONTRACT_FROZEN",
        "RESOLUTION_GATE_CONTRACT_FROZEN",
        "C5_RECONSIDERATION_RULE_FROZEN",
        "BUILD_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_AUTHORIZED_NEXT",
        "NO_WEAK_FEEDBACK_RESOLUTION_ATTEMPTED",
        "NO_QUESTION_PACKET_ANSWERED",
        "NO_SOURCE_REF_REQUEST_SATISFIED",
        "NO_UNDER_TYPED_ACCEPTANCE_APPROVED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_TARGET_SELECTED_FOR_BUILD",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
        "NO_C5_OPENED",
    ] if design_pass else failures

    target_definition = {
        "schema_version": "o2_weak_feedback_resolution_target_definition_v0",
        "target_status": "DESIGNED_BUILD_READY" if design_pass else "NOT_READY",
        "source_wfh_post_closure_decision_receipt_id": WFH_DECISION_RECEIPT_ID,
        "target_unit_to_build_next": AUTHORIZED_BUILD_UNIT if design_pass else None,
        "target_unit_id_to_build": "observation.o2_weak_feedback_resolution_target_build.v0",
        "target_mode_for_build": "STATIC_RESOLUTION_TARGET_BUILD_ONLY",
        "active_object": "reviewed weak-feedback handling reference with unresolved packets/candidates",
        "goal": "Define the bounded machinery that can later decide whether weak feedback is resolved without resolving it in the target-design unit.",
        "resolution_must_be_reviewed": True,
        "c5_unblock_requires_reviewed_resolution_or_explicit_governed_acceptance": True,
        "not_goal": [
            "answer question packets now",
            "satisfy source-ref requests now",
            "approve under-typed acceptance now",
            "count parking as resolution",
            "run live audit now",
            "repair",
            "retry",
            "select build target",
            "patch runtime",
            "mutate sources",
            "open C5",
        ],
    }

    input_surface_inventory = {
        "schema_version": "o2_weak_feedback_resolution_input_surface_inventory_v0",
        "inventory_status": "INPUT_SURFACES_AVAILABLE_FOR_TARGET_BUILD",
        "handling_records_available_count": len(handling),
        "question_packet_candidates_available_count": len(questions),
        "source_ref_request_candidates_available_count": len(source_refs),
        "under_typed_acceptance_candidates_available_count": len(acceptances),
        "parking_records_available_count": len(parking),
        "c5_block_records_available_count": len(c5_blocks),
        "source_refs": {
            "handling_records": rel(WFH_HANDLING_RECORDS_PATH),
            "question_packets": rel(WFH_QUESTION_PACKETS_PATH),
            "source_ref_requests": rel(WFH_SOURCE_REF_REQUESTS_PATH),
            "under_typed_acceptance_candidates": rel(WFH_UNDERTYPED_CANDIDATES_PATH),
            "parking_records": rel(WFH_PARKING_RECORDS_PATH),
            "c5_block_records": rel(WFH_C5_BLOCK_RECORDS_PATH),
        },
    }

    resolution_state_enum = {
        "schema_version": "o2_weak_feedback_resolution_state_enum_v0",
        "enum_status": "RESOLUTION_STATE_ENUM_FROZEN",
        "states": [
            "UNRESOLVED",
            "QUESTION_ANSWER_PROPOSED",
            "QUESTION_ANSWER_REVIEWED",
            "SOURCE_REF_SATISFACTION_PROPOSED",
            "SOURCE_REF_SATISFACTION_REVIEWED",
            "UNDER_TYPED_ACCEPTANCE_REVIEWED_APPROVED",
            "UNDER_TYPED_ACCEPTANCE_REVIEWED_REJECTED",
            "PARKED_UNRESOLVED",
            "RESOLVED_REVIEWED",
            "C5_RECONSIDERATION_READY",
        ],
        "resolution_state": "UNRESOLVED",
        "design_unit_sets_resolution_state": False,
    }

    question_answer_contract = {
        "schema_version": "o2_question_packet_answer_contract_v0",
        "contract_status": "QUESTION_ANSWER_CONTRACT_FROZEN",
        "question_packet_count": len(questions),
        "answer_record_schema": {
            "schema_version": "o2_question_packet_answer_record_v0",
            "answer_id": "question_answer_<sig8>",
            "source_question_packet_ref": None,
            "answer_text_or_ref": None,
            "answered_by": "human | validator | source_trace",
            "answer_evidence_refs": [],
            "review_status": "PROPOSED | REVIEWED_ACCEPTED | REVIEWED_REJECTED",
            "counts_as_resolution_input": False,
        },
        "rule": "A question packet is not answered until an explicit answer record exists and is reviewed.",
        "design_unit_answers_questions": False,
    }

    source_ref_satisfaction_contract = {
        "schema_version": "o2_source_ref_satisfaction_contract_v0",
        "contract_status": "SOURCE_REF_SATISFACTION_CONTRACT_FROZEN",
        "source_ref_request_count": len(source_refs),
        "satisfaction_record_schema": {
            "schema_version": "o2_source_ref_satisfaction_record_v0",
            "satisfaction_id": "source_ref_satisfaction_<sig8>",
            "source_ref_request_ref": None,
            "provided_source_refs": [],
            "evidence_scope": None,
            "review_status": "PROPOSED | REVIEWED_ACCEPTED | REVIEWED_REJECTED",
            "counts_as_resolution_input": False,
        },
        "rule": "A source-ref request is not satisfied until explicit source refs are provided and reviewed.",
        "design_unit_satisfies_source_refs": False,
    }

    undertyped_review_contract = {
        "schema_version": "o2_under_typed_acceptance_review_contract_v0",
        "contract_status": "UNDER_TYPED_ACCEPTANCE_REVIEW_CONTRACT_FROZEN",
        "under_typed_acceptance_candidate_count": len(acceptances),
        "review_record_schema": {
            "schema_version": "o2_under_typed_acceptance_review_record_v0",
            "review_id": "under_typed_acceptance_review_<sig8>",
            "source_acceptance_candidate_ref": None,
            "review_decision": "APPROVE_AS_BLOCKING_REFERENCE | REJECT | KEEP_CANDIDATE_ONLY",
            "review_reason": None,
            "c5_unblock_allowed": False,
            "review_status": "PROPOSED | REVIEWED_ACCEPTED | REVIEWED_REJECTED",
        },
        "rule": "Under-typed acceptance cannot unblock C5 unless a later explicit reviewed rule allows it.",
        "design_unit_approves_under_typed_acceptance": False,
    }

    parking_continuation_contract = {
        "schema_version": "o2_parking_continuation_contract_v0",
        "contract_status": "PARKING_CONTINUATION_CONTRACT_FROZEN",
        "parking_records_count": len(parking),
        "parking_continuation_schema": {
            "schema_version": "o2_parking_continuation_record_v0",
            "parking_continuation_id": "parking_continuation_<sig8>",
            "source_parking_ref": None,
            "continue_parking": True,
            "park_reason": None,
            "counts_as_resolution": False,
            "reopen_conditions": [],
        },
        "rule": "Parking remains explicit unresolved status unless later reviewed rule changes it.",
        "design_unit_counts_parking_as_resolution": False,
    }

    resolution_gate_contract = {
        "schema_version": "o2_weak_feedback_resolution_gate_contract_v0",
        "contract_status": "RESOLUTION_GATE_CONTRACT_FROZEN",
        "resolution_requires": [
            "every weak feedback record has a reviewed resolution route",
            "every question packet is either reviewed answered or explicitly reviewed not required",
            "every source-ref request is either reviewed satisfied or explicitly reviewed not required",
            "every under-typed acceptance candidate is reviewed approved/rejected/kept candidate-only",
            "parking is not counted as resolution unless an explicit reviewed rule allows it",
            "C5 block is not lifted by resolution target design alone",
        ],
        "resolution_output_schema": {
            "schema_version": "o2_weak_feedback_resolution_record_v0",
            "resolution_record_id": "weak_feedback_resolution_<sig8>",
            "source_weak_feedback_ref": None,
            "question_answer_refs": [],
            "source_ref_satisfaction_refs": [],
            "under_typed_acceptance_review_refs": [],
            "parking_continuation_refs": [],
            "resolution_decision": "RESOLVED_REVIEWED | REMAINS_UNRESOLVED | PARKED_UNRESOLVED",
            "review_status": "PROPOSED | REVIEWED_ACCEPTED | REVIEWED_REJECTED",
            "c5_reconsideration_ready": False,
        },
        "design_unit_emits_resolution_records": False,
    }

    c5_reconsideration_rule = {
        "schema_version": "o2_c5_reconsideration_rule_v0",
        "rule_status": "C5_RECONSIDERATION_RULE_FROZEN",
        "current_c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "current_c5_opened": False,
        "c5_reconsideration_requires": [
            "resolution target built",
            "resolution target reviewed",
            "resolution target closed",
            "all weak feedback records have reviewed resolution or explicit governed unresolved acceptance",
            "a post-resolution decision explicitly selects C5 reconsideration",
        ],
        "design_unit_can_unblock_c5": False,
    }

    negative_controls = {
        "schema_version": "o2_weak_feedback_resolution_negative_controls_v0",
        "negative_control_status": "NEGATIVE_CONTROLS_FROZEN",
        "negative_controls": [
            "design_target_resolves_weak_feedback_fail",
            "question_contract_counts_as_answer_fail",
            "source_ref_contract_counts_as_satisfied_fail",
            "under_typed_contract_counts_as_approved_fail",
            "parking_contract_counts_as_resolution_fail",
            "resolution_gate_contract_unblocks_c5_fail",
            "live_audit_executed_fail",
            "repair_applied_fail",
            "retry_executed_fail",
            "target_selected_for_build_fail",
            "runtime_patch_applied_fail",
            "source_mutated_fail",
            "c5_opened_fail",
            "hidden_next_command_fail",
            "latest_or_mtime_selection_fail",
        ],
    }

    acceptance_gates = {
        "schema_version": "o2_weak_feedback_resolution_target_acceptance_gates_v0",
        "gate_status": "ACCEPTANCE_GATES_FROZEN",
        "acceptance_gates": [
            "RT_0_WFH_POST_CLOSURE_DECISION_RECEIPT_CONSUMED",
            "RT_1_REVIEWED_REFERENCE_CONFIRMED",
            "RT_2_INPUT_SURFACE_INVENTORY_EMITTED",
            "RT_3_RESOLUTION_STATE_ENUM_EMITTED",
            "RT_4_QUESTION_ANSWER_CONTRACT_EMITTED",
            "RT_5_SOURCE_REF_SATISFACTION_CONTRACT_EMITTED",
            "RT_6_UNDER_TYPED_ACCEPTANCE_REVIEW_CONTRACT_EMITTED",
            "RT_7_PARKING_CONTINUATION_CONTRACT_EMITTED",
            "RT_8_RESOLUTION_GATE_CONTRACT_EMITTED",
            "RT_9_C5_RECONSIDERATION_RULE_EMITTED",
            "RT_10_BUILD_AUTHORIZATION_EMITTED",
            "RT_11_NO_RESOLUTION_NO_ANSWER_NO_SATISFY_NO_APPROVE",
            "RT_12_NO_LIVE_AUDIT_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION",
            "RT_13_NO_C5_OPENED",
        ],
    }

    terminal_rules = {
        "schema_version": "o2_weak_feedback_resolution_target_terminal_rules_v0",
        "terminal_rules_status": "TERMINAL_RULES_FROZEN",
        "success_terminal": {
            "type": "STOP",
            "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGNED_BUILD_READY",
            "next_command_goal": None,
        },
        "basis_fail_terminal": {
            "type": "STOP",
            "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGN_BASIS_FAIL",
            "next_command_goal": None,
        },
    }

    build_authorization = {
        "schema_version": "o2_weak_feedback_resolution_target_build_authorization_v0",
        "authorization_status": "BUILD_UNIT_AUTHORIZED_NEXT" if design_pass else "NOT_AUTHORIZED",
        "authorized_next_unit": AUTHORIZED_BUILD_UNIT if design_pass else None,
        "authorized_build_mode": "STATIC_RESOLUTION_TARGET_BUILD_ONLY" if design_pass else None,
        "authorized_scope": [
            "materialize resolution target schemas",
            "materialize resolution input mapping",
            "materialize candidate record skeletons for answer/satisfaction/review/parking",
            "materialize resolution gate readout",
            "preserve unresolved weak-feedback status",
            "preserve C5 block",
        ],
        "not_authorized": [
            "answer question packets",
            "satisfy source-ref requests",
            "approve under-typed acceptance",
            "count parking as resolution",
            "emit reviewed resolution",
            "run live audit",
            "repair",
            "retry",
            "patch runtime",
            "mutate sources",
            "open C5",
        ],
    }

    c5_block_continuation = {
        "schema_version": "o2_weak_feedback_resolution_target_c5_block_continuation_v0",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_opened": False,
        "block_continues": True,
        "block_reason": "Resolution target design does not resolve weak feedback or satisfy any unblocking condition.",
    }

    authority_boundary = {
        "schema_version": "o2_weak_feedback_resolution_target_authority_boundary_v0",
        "status": status,
        "may_build_o2_weak_feedback_resolution_target_next": design_pass,
        "may_resolve_weak_feedback_now": False,
        "may_answer_question_packets_now": False,
        "may_satisfy_source_ref_requests_now": False,
        "may_approve_under_typed_acceptance_now": False,
        "may_count_parking_as_resolution": False,
        "may_run_live_feedback_audit_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_select_target_for_build": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_open_c5": False,
    }

    classification = {
        "schema_version": "o2_weak_feedback_resolution_target_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "resolution_target_designed": design_pass,
        "authorized_next_unit": recommended_next,
        "weak_feedback_resolved": False,
        "question_packets_answered": False,
        "source_ref_requests_satisfied": False,
        "under_typed_acceptance_approved": False,
        "parking_counted_as_resolution": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
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
        "schema_version": "o2_weak_feedback_resolution_target_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "resolution_target_design_count": 1 if design_pass else 0,
        "input_surface_inventory_count": 1 if design_pass else 0,
        "resolution_state_enum_count": 1 if design_pass else 0,
        "question_answer_contract_count": 1 if design_pass else 0,
        "source_ref_satisfaction_contract_count": 1 if design_pass else 0,
        "under_typed_acceptance_review_contract_count": 1 if design_pass else 0,
        "parking_continuation_contract_count": 1 if design_pass else 0,
        "resolution_gate_contract_count": 1 if design_pass else 0,
        "c5_reconsideration_rule_count": 1 if design_pass else 0,
        "build_authorized_next_count": 1 if design_pass else 0,
        "weak_feedback_resolved_count": 0,
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
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "weak_feedback_resolved_count",
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
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "o2_weak_feedback_resolution_target_profile_v0",
        "profile_id": "o2_wf_resolution_target_profile_" + sha8(rollup),
        "status": status,
        "resolution_target_designed": design_pass,
        "authorized_next_unit": recommended_next,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Build the weak-feedback resolution target next; do not execute resolution yet.",
        "must_not_infer": [
            "weak feedback resolved",
            "question packet answered",
            "source-ref request satisfied",
            "under-typed acceptance approved",
            "parking resolved weak feedback",
            "live audit complete",
            "C5 opened",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_weak_feedback_resolution_target_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The weak-feedback resolution target was designed. It defines contracts for question answers, source-ref satisfaction, under-typed acceptance review, parking continuation, resolution gates, and C5 reconsideration. This design does not answer, satisfy, approve, resolve, run live audit, repair, retry, select target, patch runtime, mutate sources, or open C5.",
        "authorized_next_unit": recommended_next,
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_weak_feedback_resolution_target_transition_trace_v0",
        "trace": [
            {
                "step": "consume_post_closure_decision",
                "question": "is resolution target design authorized",
                "answer": "yes" if design_pass else "no",
                "taken": "design resolution target",
            },
            {
                "step": "define_resolution_contracts",
                "question": "what must exist before weak feedback can be called resolved",
                "answer": "reviewed answer/satisfaction/acceptance/parking-resolution gate records",
                "taken": "freeze contracts without executing them",
            },
            {
                "step": "preserve_c5_block",
                "question": "does target design unblock C5",
                "answer": "no",
                "taken": "authorize target build next while preserving block",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (TARGET_DEFINITION_PATH, target_definition),
        (INPUT_SURFACE_INVENTORY_PATH, input_surface_inventory),
        (RESOLUTION_STATE_ENUM_PATH, resolution_state_enum),
        (QUESTION_ANSWER_CONTRACT_PATH, question_answer_contract),
        (SOURCE_REF_SATISFACTION_CONTRACT_PATH, source_ref_satisfaction_contract),
        (UNDERTYPED_REVIEW_CONTRACT_PATH, undertyped_review_contract),
        (PARKING_CONTINUATION_CONTRACT_PATH, parking_continuation_contract),
        (RESOLUTION_GATE_CONTRACT_PATH, resolution_gate_contract),
        (C5_RECONSIDERATION_RULE_PATH, c5_reconsideration_rule),
        (NEGATIVE_CONTROLS_PATH, negative_controls),
        (ACCEPTANCE_GATES_PATH, acceptance_gates),
        (TERMINAL_RULES_PATH, terminal_rules),
        (BUILD_AUTHORIZATION_PATH, build_authorization),
        (C5_BLOCK_CONTINUATION_PATH, c5_block_continuation),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, trace),
    ]
    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "RT_DESIGN_0_POST_CLOSURE_DECISION_RECEIPT_CONSUMED": WFH_DECISION_RECEIPT_PATH.exists(),
        "RT_DESIGN_1_TARGET_DEFINITION_EMITTED": TARGET_DEFINITION_PATH.exists(),
        "RT_DESIGN_2_INPUT_SURFACE_INVENTORY_EMITTED": INPUT_SURFACE_INVENTORY_PATH.exists(),
        "RT_DESIGN_3_RESOLUTION_STATE_ENUM_EMITTED": RESOLUTION_STATE_ENUM_PATH.exists(),
        "RT_DESIGN_4_QUESTION_ANSWER_CONTRACT_EMITTED": QUESTION_ANSWER_CONTRACT_PATH.exists(),
        "RT_DESIGN_5_SOURCE_REF_SATISFACTION_CONTRACT_EMITTED": SOURCE_REF_SATISFACTION_CONTRACT_PATH.exists(),
        "RT_DESIGN_6_UNDER_TYPED_ACCEPTANCE_REVIEW_CONTRACT_EMITTED": UNDERTYPED_REVIEW_CONTRACT_PATH.exists(),
        "RT_DESIGN_7_PARKING_CONTINUATION_CONTRACT_EMITTED": PARKING_CONTINUATION_CONTRACT_PATH.exists(),
        "RT_DESIGN_8_RESOLUTION_GATE_CONTRACT_EMITTED": RESOLUTION_GATE_CONTRACT_PATH.exists(),
        "RT_DESIGN_9_C5_RECONSIDERATION_RULE_EMITTED": C5_RECONSIDERATION_RULE_PATH.exists(),
        "RT_DESIGN_10_BUILD_AUTHORIZATION_EMITTED": BUILD_AUTHORIZATION_PATH.exists() and build_authorization["authorized_next_unit"] == AUTHORIZED_BUILD_UNIT,
        "RT_DESIGN_11_NO_RESOLUTION_ANSWER_SATISFY_APPROVE": rollup["weak_feedback_resolved_count"] == 0 and rollup["question_packets_answered_count"] == 0 and rollup["source_ref_requests_satisfied_count"] == 0 and rollup["under_typed_acceptance_approved_count"] == 0,
        "RT_DESIGN_12_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "RT_DESIGN_13_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "RT_DESIGN_14_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "RT_DESIGN_15_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "RT_DESIGN_16_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "RT_DESIGN_17_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGN_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "authorized_next": recommended_next,
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_resolution_target_design_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_RESOLUTION_TARGET_DESIGN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_wfh_post_closure_decision_receipt_id": WFH_DECISION_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_resolution_target_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "resolution_target_designed": design_pass,
            "authorized_next_unit": recommended_next,
            "authorized_build_mode": "STATIC_RESOLUTION_TARGET_BUILD_ONLY" if design_pass else None,
            "input_surface_inventory_emitted": design_pass,
            "resolution_state_enum_frozen": design_pass,
            "question_answer_contract_frozen": design_pass,
            "source_ref_satisfaction_contract_frozen": design_pass,
            "under_typed_acceptance_review_contract_frozen": design_pass,
            "parking_continuation_contract_frozen": design_pass,
            "resolution_gate_contract_frozen": design_pass,
            "c5_reconsideration_rule_frozen": design_pass,
            "handling_records_available_count": len(handling),
            "question_packet_candidates_available_count": len(questions),
            "source_ref_request_candidates_available_count": len(source_refs),
            "under_typed_acceptance_candidates_available_count": len(acceptances),
            "parking_records_available_count": len(parking),
            "c5_block_records_available_count": len(c5_blocks),
            "weak_feedback_resolved": False,
            "question_packets_answered": False,
            "source_ref_requests_satisfied": False,
            "under_typed_acceptance_approved": False,
            "parking_counted_as_resolution": False,
            "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
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
            "target_definition": rel(TARGET_DEFINITION_PATH),
            "input_surface_inventory": rel(INPUT_SURFACE_INVENTORY_PATH),
            "resolution_state_enum": rel(RESOLUTION_STATE_ENUM_PATH),
            "question_answer_contract": rel(QUESTION_ANSWER_CONTRACT_PATH),
            "source_ref_satisfaction_contract": rel(SOURCE_REF_SATISFACTION_CONTRACT_PATH),
            "under_typed_acceptance_review_contract": rel(UNDERTYPED_REVIEW_CONTRACT_PATH),
            "parking_continuation_contract": rel(PARKING_CONTINUATION_CONTRACT_PATH),
            "resolution_gate_contract": rel(RESOLUTION_GATE_CONTRACT_PATH),
            "c5_reconsideration_rule": rel(C5_RECONSIDERATION_RULE_PATH),
            "negative_controls": rel(NEGATIVE_CONTROLS_PATH),
            "acceptance_gates": rel(ACCEPTANCE_GATES_PATH),
            "terminal_rules": rel(TERMINAL_RULES_PATH),
            "build_authorization": rel(BUILD_AUTHORIZATION_PATH),
            "c5_block_continuation": rel(C5_BLOCK_CONTINUATION_PATH),
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
    print(f"weak_feedback_resolution_target_receipt_id={receipt_id}")
    print(f"weak_feedback_resolution_target_receipt_path={rel(receipt_path)}")
    print(f"weak_feedback_resolution_target_definition_path={rel(TARGET_DEFINITION_PATH)}")
    print(f"weak_feedback_resolution_input_surface_inventory_path={rel(INPUT_SURFACE_INVENTORY_PATH)}")
    print(f"weak_feedback_resolution_state_enum_path={rel(RESOLUTION_STATE_ENUM_PATH)}")
    print(f"question_answer_contract_path={rel(QUESTION_ANSWER_CONTRACT_PATH)}")
    print(f"source_ref_satisfaction_contract_path={rel(SOURCE_REF_SATISFACTION_CONTRACT_PATH)}")
    print(f"under_typed_acceptance_review_contract_path={rel(UNDERTYPED_REVIEW_CONTRACT_PATH)}")
    print(f"weak_feedback_resolution_gate_contract_path={rel(RESOLUTION_GATE_CONTRACT_PATH)}")
    print(f"weak_feedback_resolution_target_rollup_path={rel(ROLLUP_PATH)}")
    print(f"weak_feedback_resolution_target_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
