#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DESIGN_O2_WEAK_FEEDBACK_HANDLING_TARGET_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_handling_target.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_HANDLING_TARGET_DESIGN"
MODE = "DESIGN_ONLY / WEAK_FEEDBACK_HANDLING_TARGET / NO_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_HANDLING_TARGET_DESIGN_ONLY"

POST_O2_DECISION_RECEIPT_ID = "2fef4830"
POST_O2_DECISION_RECEIPT_PATH = ROOT / "data/o2_post_closure_decision_v0_receipts/2fef4830.json"
POST_O2_DECISION_BASIS_PATH = ROOT / "data/o2_post_closure_decision_v0/o2_post_closure_decision_basis_v0.json"
POST_O2_DECISION_TABLE_PATH = ROOT / "data/o2_post_closure_decision_v0/o2_post_closure_decision_table_v0.json"
POST_O2_SELECTED_BRANCH_PATH = ROOT / "data/o2_post_closure_decision_v0/o2_selected_next_branch_v0.json"
POST_O2_WEAK_AUTH_PATH = ROOT / "data/o2_post_closure_decision_v0/o2_weak_feedback_handling_target_authorization_v0.json"
POST_O2_C5_BLOCK_CONTINUATION_PATH = ROOT / "data/o2_post_closure_decision_v0/o2_c5_block_continuation_v0.json"
POST_O2_AUTHORITY_PATH = ROOT / "data/o2_post_closure_decision_v0/o2_post_closure_decision_authority_boundary_v0.json"
POST_O2_CLASSIFICATION_PATH = ROOT / "data/o2_post_closure_decision_v0/o2_post_closure_decision_classification_v0.json"
POST_O2_ROLLUP_PATH = ROOT / "data/o2_post_closure_decision_v0/o2_post_closure_decision_rollup_v0.json"
POST_O2_PROFILE_PATH = ROOT / "data/o2_post_closure_decision_v0/o2_post_closure_decision_profile_v0.json"
POST_O2_REPORT_PATH = ROOT / "data/o2_post_closure_decision_v0/o2_post_closure_decision_report.json"

O2_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0_receipts/bf5163d7.json"
O2_WEAK_FEEDBACK_NOTE_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_weak_feedback_note_v0.json"
O2_C5_BLOCK_STATUS_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_c5_block_status_v0.json"
O2_REVIEWED_REFERENCE_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_unit_feedback_hardening_reviewed_reference_v0.json"
O2_BOUNDARY_LOCK_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_unit_feedback_hardening_boundary_lock_v0.json"
O2_FEEDBACK_RECORDS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_feedback_records_v0.jsonl"
O2_FEEDBACK_QUALITY_ENUM_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_feedback_quality_enum_v0.json"
O2_RETRY_GATE_RECORDS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_retry_gate_records_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    POST_O2_DECISION_RECEIPT_PATH,
    POST_O2_DECISION_BASIS_PATH,
    POST_O2_DECISION_TABLE_PATH,
    POST_O2_SELECTED_BRANCH_PATH,
    POST_O2_WEAK_AUTH_PATH,
    POST_O2_C5_BLOCK_CONTINUATION_PATH,
    POST_O2_AUTHORITY_PATH,
    POST_O2_CLASSIFICATION_PATH,
    POST_O2_ROLLUP_PATH,
    POST_O2_PROFILE_PATH,
    POST_O2_REPORT_PATH,
    O2_CLOSURE_RECEIPT_PATH,
    O2_WEAK_FEEDBACK_NOTE_PATH,
    O2_C5_BLOCK_STATUS_PATH,
    O2_REVIEWED_REFERENCE_PATH,
    O2_BOUNDARY_LOCK_PATH,
    O2_FEEDBACK_RECORDS_PATH,
    O2_FEEDBACK_QUALITY_ENUM_PATH,
    O2_RETRY_GATE_RECORDS_PATH,
]

OUT_DIR = ROOT / "data/o2_weak_feedback_handling_target_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_handling_target_v0_receipts"

TARGET_DEFINITION_PATH = OUT_DIR / "o2_weak_feedback_handling_target_definition_v0.json"
SOURCE_SCOPE_PATH = OUT_DIR / "o2_weak_feedback_handling_source_scope_v0.json"
WEAK_RECORD_INVENTORY_PATH = OUT_DIR / "o2_weak_feedback_record_inventory_v0.json"
HANDLING_POLICY_ENUM_PATH = OUT_DIR / "o2_weak_feedback_handling_policy_enum_v0.json"
QUESTION_PACKET_CONTRACT_PATH = OUT_DIR / "o2_weak_feedback_question_packet_contract_v0.json"
SOURCE_REF_REQUEST_CONTRACT_PATH = OUT_DIR / "o2_weak_feedback_source_ref_request_contract_v0.json"
UNDERTYPED_ACCEPTANCE_CONTRACT_PATH = OUT_DIR / "o2_under_typed_acceptance_contract_v0.json"
PARKING_CONTRACT_PATH = OUT_DIR / "o2_weak_feedback_parking_contract_v0.json"
C5_BLOCK_CONTRACT_PATH = OUT_DIR / "o2_weak_feedback_c5_block_contract_v0.json"
BUILD_AUTHORIZATION_PATH = OUT_DIR / "o2_weak_feedback_handling_build_authorization_v0.json"
ACCEPTANCE_GATES_PATH = OUT_DIR / "o2_weak_feedback_handling_acceptance_gates_v0.json"
NEGATIVE_CONTROLS_PATH = OUT_DIR / "o2_weak_feedback_handling_negative_controls_v0.json"
TERMINAL_RULES_PATH = OUT_DIR / "o2_weak_feedback_handling_terminal_rules_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o2_weak_feedback_handling_target_downstream_decision_table_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_weak_feedback_handling_target_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_weak_feedback_handling_target_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_weak_feedback_handling_target_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_weak_feedback_handling_target_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_weak_feedback_handling_target_report.json"
TRACE_PATH = OUT_DIR / "o2_weak_feedback_handling_target_transition_trace.json"

EXPECTED_POST_DECISION_STATUS = "TYPED_O2_POST_CLOSURE_DECISION_SELECTED_WEAK_FEEDBACK_HANDLING_TARGET_READY"
EXPECTED_POST_DECISION_STOP = "STOP_TYPED_O2_POST_CLOSURE_DECISION_SELECTED_WEAK_FEEDBACK_HANDLING_TARGET_READY"
EXPECTED_POST_DECISION_NEXT = "DESIGN_O2_WEAK_FEEDBACK_HANDLING_TARGET_V0"
AUTHORIZED_BUILD_UNIT = "BUILD_O2_WEAK_FEEDBACK_HANDLING_V0"

WEAK_CLASSES = {"UNDER_TYPED_FEEDBACK", "AMBIGUOUS_REQUIRES_QUESTION"}

HANDLING_POLICIES = [
    "QUESTION_PACKET_REQUIRED",
    "SOURCE_REF_REQUEST_REQUIRED",
    "UNDER_TYPED_ACCEPTANCE_CANDIDATE",
    "PARK_WITH_REASON",
    "LIVE_AUDIT_REQUEST_CANDIDATE_ONLY",
]

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

def feedback_quality(rec: Dict[str, Any]) -> str:
    return rec.get("quality", {}).get("feedback_quality_class")

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    decision_receipt = read_json(POST_O2_DECISION_RECEIPT_PATH)
    decision_summary = decision_receipt.get("machine_readable_o2_post_closure_decision_summary", {})
    selected_branch = read_json(POST_O2_SELECTED_BRANCH_PATH)
    weak_auth = read_json(POST_O2_WEAK_AUTH_PATH)
    c5_continuation = read_json(POST_O2_C5_BLOCK_CONTINUATION_PATH)
    authority = read_json(POST_O2_AUTHORITY_PATH)
    rollup = read_json(POST_O2_ROLLUP_PATH)
    profile = read_json(POST_O2_PROFILE_PATH)
    closure_receipt = read_json(O2_CLOSURE_RECEIPT_PATH)
    weak_note = read_json(O2_WEAK_FEEDBACK_NOTE_PATH)
    c5_block = read_json(O2_C5_BLOCK_STATUS_PATH)
    boundary_lock = read_json(O2_BOUNDARY_LOCK_PATH)
    feedback_records = read_jsonl(O2_FEEDBACK_RECORDS_PATH)
    retry_gates = read_jsonl(O2_RETRY_GATE_RECORDS_PATH)

    if decision_receipt.get("receipt_id") != POST_O2_DECISION_RECEIPT_ID or decision_receipt.get("gate") != "PASS":
        failures.append("post_o2_decision_receipt_not_pass")
    if decision_receipt.get("terminal", {}).get("stop_code") != EXPECTED_POST_DECISION_STOP:
        failures.append("post_o2_decision_terminal_not_expected")
    if decision_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("post_o2_decision_hidden_next_command")
    if decision_summary.get("status") != EXPECTED_POST_DECISION_STATUS:
        failures.append(f"post_o2_decision_status_not_expected:{decision_summary.get('status')}")
    if decision_summary.get("recommended_next") != EXPECTED_POST_DECISION_NEXT:
        failures.append(f"post_o2_decision_next_not_expected:{decision_summary.get('recommended_next')}")

    for key in ["post_closure_decision_complete", "bad_counters_zero"]:
        if decision_summary.get(key) is not True:
            failures.append(f"decision_required_true_missing:{key}")

    for key in [
        "weak_feedback_resolved",
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
            failures.append(f"decision_forbidden_true:{key}")

    if decision_summary.get("selected_next_branch") != "DESIGN_O2_WEAK_FEEDBACK_HANDLING_TARGET":
        failures.append("selected_branch_wrong")
    if decision_summary.get("selected_next_unit") != EXPECTED_POST_DECISION_NEXT:
        failures.append("selected_unit_wrong")
    if decision_summary.get("weak_feedback_count") != 3:
        failures.append("decision_weak_feedback_count_wrong")
    if decision_summary.get("under_typed_feedback_count") != 2:
        failures.append("decision_under_typed_count_wrong")
    if decision_summary.get("ambiguous_requires_question_count") != 1:
        failures.append("decision_ambiguous_count_wrong")
    if decision_summary.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("decision_c5_not_blocked")
    if selected_branch.get("selected_next_unit") != EXPECTED_POST_DECISION_NEXT:
        failures.append("selected_branch_artifact_wrong")
    if weak_auth.get("authorization_status") != "TARGET_DESIGN_AUTHORIZED":
        failures.append("weak_auth_not_authorized")
    if weak_auth.get("authorized_next_unit") != EXPECTED_POST_DECISION_NEXT:
        failures.append("weak_auth_next_wrong")
    if c5_continuation.get("block_continues") is not True:
        failures.append("c5_continuation_not_true")
    if c5_continuation.get("c5_opened") is not False:
        failures.append("c5_continuation_opened")
    if authority.get("may_design_o2_weak_feedback_handling_target_next") is not True:
        failures.append("authority_does_not_allow_target_design")
    if authority.get("may_open_c5") is not False:
        failures.append("authority_allows_c5")
    if rollup.get("selected_weak_feedback_handling_target_count") != 1:
        failures.append("rollup_selected_target_wrong")
    if profile.get("selected_next_unit") != EXPECTED_POST_DECISION_NEXT:
        failures.append("profile_selected_next_wrong")
    if closure_receipt.get("receipt_id") != "bf5163d7":
        failures.append("closure_receipt_wrong")
    if weak_note.get("weak_feedback_count") != 3:
        failures.append("weak_note_count_wrong")
    if c5_block.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("c5_block_not_blocked")
    if boundary_lock.get("weak_feedback_resolved") is not False:
        failures.append("boundary_lock_weak_resolved")
    if len(feedback_records) != 10:
        failures.append(f"feedback_records_count_wrong:{len(feedback_records)}")
    if len(retry_gates) != 10:
        failures.append(f"retry_gate_count_wrong:{len(retry_gates)}")

    weak_records = [r for r in feedback_records if feedback_quality(r) in WEAK_CLASSES]
    weak_counts = Counter(feedback_quality(r) for r in weak_records)
    if len(weak_records) != 3:
        failures.append(f"weak_records_count_wrong:{len(weak_records)}")
    if weak_counts.get("UNDER_TYPED_FEEDBACK", 0) != 2:
        failures.append(f"weak_records_under_typed_wrong:{weak_counts.get('UNDER_TYPED_FEEDBACK', 0)}")
    if weak_counts.get("AMBIGUOUS_REQUIRES_QUESTION", 0) != 1:
        failures.append(f"weak_records_ambiguous_wrong:{weak_counts.get('AMBIGUOUS_REQUIRES_QUESTION', 0)}")

    return failures, {
        "decision_summary": decision_summary,
        "weak_records": weak_records,
        "feedback_records": feedback_records,
        "retry_gates": retry_gates,
    }

def handling_candidate_for(rec: Dict[str, Any]) -> List[str]:
    q = feedback_quality(rec)
    missing = rec.get("missing_capability", {}) or {}
    movement = rec.get("movement", {}) or {}
    policies: List[str] = []
    if q == "AMBIGUOUS_REQUIRES_QUESTION":
        policies.append("QUESTION_PACKET_REQUIRED")
        policies.append("PARK_WITH_REASON")
    elif q == "UNDER_TYPED_FEEDBACK":
        policies.append("SOURCE_REF_REQUEST_REQUIRED")
        policies.append("QUESTION_PACKET_REQUIRED")
        if missing.get("smallest_honest_name") and movement.get("lawful_next_refinements"):
            policies.append("UNDER_TYPED_ACCEPTANCE_CANDIDATE")
    else:
        policies.append("PARK_WITH_REASON")
    return policies

def inventory_from_records(weak_records: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    rows = []
    for idx, rec in enumerate(weak_records, start=1):
        rows.append({
            "inventory_id": "weak_feedback_inventory_" + sha8({"idx": idx, "feedback_id": rec.get("feedback_id")}),
            "source_feedback_ref": rec.get("feedback_id"),
            "source_unit_id": rec.get("source", {}).get("unit_id"),
            "feedback_quality_class": feedback_quality(rec),
            "unit_status": rec.get("unit_status", {}).get("status"),
            "where_failed": rec.get("failure_explanation", {}).get("where_failed"),
            "why_failed": rec.get("failure_explanation", {}).get("why_failed"),
            "failed_relative_to_boundary": rec.get("failure_explanation", {}).get("failed_relative_to_boundary"),
            "missing_capability_name": rec.get("missing_capability", {}).get("smallest_honest_name"),
            "missing_discriminator": rec.get("missing_capability", {}).get("missing_discriminator"),
            "lawful_next_refinements_observed": rec.get("movement", {}).get("lawful_next_refinements", []),
            "handling_candidates": handling_candidate_for(rec),
            "resolution_status": "UNRESOLVED",
            "handling_status": "TARGET_DESIGN_ONLY",
        })
    return rows

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    decision_summary = src.get("decision_summary", {})
    weak_records = src.get("weak_records", [])
    feedback_records = src.get("feedback_records", [])
    inventory = inventory_from_records(weak_records)

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    design_pass = not failures
    status = "TYPED_O2_WEAK_FEEDBACK_HANDLING_TARGET_DESIGNED_BUILD_READY" if design_pass else "TYPED_O2_WEAK_FEEDBACK_HANDLING_TARGET_DESIGN_BASIS_FAIL"
    recommended_next = AUTHORIZED_BUILD_UNIT if design_pass else "REPAIR_O2_WEAK_FEEDBACK_HANDLING_TARGET_DESIGN_BASIS_V0"

    reason_codes = [
        "WEAK_FEEDBACK_HANDLING_TARGET_DESIGNED",
        "POST_O2_DECISION_RECEIPT_CONSUMED",
        "THREE_WEAK_FEEDBACK_RECORDS_INVENTORIED",
        "TWO_UNDER_TYPED_FEEDBACK_RECORDS_CONFIRMED",
        "ONE_AMBIGUOUS_REQUIRES_QUESTION_RECORD_CONFIRMED",
        "QUESTION_PACKET_CONTRACT_FROZEN",
        "SOURCE_REF_REQUEST_CONTRACT_FROZEN",
        "UNDER_TYPED_ACCEPTANCE_CANDIDATE_CONTRACT_FROZEN",
        "PARKING_CONTRACT_FROZEN",
        "HANDLING_POLICY_ENUM_FROZEN",
        "C5_BLOCK_CONTRACT_FROZEN",
        "BUILD_O2_WEAK_FEEDBACK_HANDLING_AUTHORIZED_NEXT",
        "NO_WEAK_FEEDBACK_RESOLUTION_ATTEMPTED",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_TARGET_SELECTED_FOR_BUILD",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
        "NO_C5_OPENED",
    ] if design_pass else failures

    target_definition = {
        "schema_version": "o2_weak_feedback_handling_target_definition_v0",
        "target_status": "DESIGNED_BUILD_READY" if design_pass else "NOT_READY",
        "source_post_o2_decision_receipt_id": POST_O2_DECISION_RECEIPT_ID,
        "target_unit_to_build_next": AUTHORIZED_BUILD_UNIT if design_pass else None,
        "target_unit_id_to_build": "observation.o2_weak_feedback_handling.v0",
        "target_mode_for_build": "STATIC_WEAK_FEEDBACK_HANDLING_ONLY",
        "active_object": "3 weak feedback records from O2 reviewed reference",
        "weak_feedback_count": decision_summary.get("weak_feedback_count"),
        "under_typed_feedback_count": decision_summary.get("under_typed_feedback_count"),
        "ambiguous_requires_question_count": decision_summary.get("ambiguous_requires_question_count"),
        "goal": "Design handling machinery for weak feedback without resolving it inside target design.",
        "core_question": "For each weak feedback record, should the next handling unit emit a question packet, source-ref request, under-typed acceptance candidate, or parked-with-reason record?",
        "not_goal": [
            "resolve weak feedback now",
            "run live feedback audit",
            "repair any source artifact",
            "retry any unit",
            "select a build target",
            "patch runtime",
            "open C5",
        ],
    }

    source_scope = {
        "schema_version": "o2_weak_feedback_handling_source_scope_v0",
        "source_scope_status": "EXPLICIT_REFS_ONLY",
        "consumed_refs": [
            rel(POST_O2_DECISION_RECEIPT_PATH),
            rel(O2_WEAK_FEEDBACK_NOTE_PATH),
            rel(O2_C5_BLOCK_STATUS_PATH),
            rel(O2_FEEDBACK_RECORDS_PATH),
        ],
        "allowed_inputs_for_next_build": [
            "O2 weak feedback inventory emitted by this design",
            "O2 reviewed reference",
            "O2 weak-feedback note",
            "O2 C5 block status",
            "O2 feedback records",
            "O2 retry gates",
        ],
        "forbidden_inputs_for_next_build": [
            "ambient latest files",
            "mtime-selected files",
            "unbounded payload inspection",
            "live feedback audit traces not explicitly authorized",
            "C5 execution artifacts",
        ],
    }

    weak_record_inventory = {
        "schema_version": "o2_weak_feedback_record_inventory_v0",
        "inventory_status": "WEAK_RECORDS_INVENTORIED_FOR_HANDLING_TARGET",
        "weak_feedback_count": len(inventory),
        "records": inventory,
        "resolution_performed": False,
    }

    handling_policy_enum = {
        "schema_version": "o2_weak_feedback_handling_policy_enum_v0",
        "enum_status": "HANDLING_POLICY_ENUM_FROZEN",
        "handling_policy_enum": HANDLING_POLICIES,
        "policy_meanings": {
            "QUESTION_PACKET_REQUIRED": "The weak record needs a machine/human-facing question packet before it can be resolved or accepted.",
            "SOURCE_REF_REQUEST_REQUIRED": "The weak record needs an explicit source-ref or evidence surface request.",
            "UNDER_TYPED_ACCEPTANCE_CANDIDATE": "The weak record may be accepted as under-typed material only by explicit review and only while preserving C5 block status unless later unblocked.",
            "PARK_WITH_REASON": "The weak record should be parked with explicit reason and no repair.",
            "LIVE_AUDIT_REQUEST_CANDIDATE_ONLY": "The weak record may motivate a later live-audit target, but live audit is not run here.",
        },
    }

    question_packet_contract = {
        "schema_version": "o2_weak_feedback_question_packet_contract_v0",
        "contract_status": "QUESTION_PACKET_CONTRACT_FROZEN",
        "record_schema": {
            "schema_version": "o2_weak_feedback_question_packet_v0",
            "question_packet_id": "weak_question_<sig8>",
            "source_feedback_ref": None,
            "question_kind": "MISSING_SOURCE | MISSING_BOUNDARY | MISSING_DISCRIMINATOR | AMBIGUOUS_LABEL | UNKNOWN_UNDER_TYPED",
            "question_text": None,
            "missing_fields": [],
            "acceptable_answer_types": [],
            "blocked_until_answered": True,
            "c5_block_preserved": True,
            "status": "PROPOSED_ONLY",
        },
        "rule": "question packet is not repair, not resolution, and not C5 unblock.",
    }

    source_ref_request_contract = {
        "schema_version": "o2_weak_feedback_source_ref_request_contract_v0",
        "contract_status": "SOURCE_REF_REQUEST_CONTRACT_FROZEN",
        "record_schema": {
            "schema_version": "o2_weak_feedback_source_ref_request_v0",
            "source_ref_request_id": "weak_source_ref_request_<sig8>",
            "source_feedback_ref": None,
            "requested_source_surface": None,
            "requested_evidence_refs": [],
            "why_needed": None,
            "status": "REQUEST_CANDIDATE_ONLY",
        },
        "rule": "source-ref request may name missing evidence but may not fabricate or fetch evidence in this unit.",
    }

    undertyped_acceptance_contract = {
        "schema_version": "o2_under_typed_acceptance_contract_v0",
        "contract_status": "UNDER_TYPED_ACCEPTANCE_CONTRACT_FROZEN",
        "record_schema": {
            "schema_version": "o2_under_typed_acceptance_candidate_v0",
            "acceptance_candidate_id": "under_typed_acceptance_<sig8>",
            "source_feedback_ref": None,
            "acceptance_scope": "LOCAL_REFERENCE_ONLY | C5_BLOCKING | PARKED",
            "acceptance_reason": None,
            "human_or_validator_review_required": True,
            "c5_unblock_allowed": False,
            "status": "CANDIDATE_ONLY",
        },
        "rule": "under-typed acceptance is candidate-only until explicitly reviewed; it does not unblock C5 by itself.",
    }

    parking_contract = {
        "schema_version": "o2_weak_feedback_parking_contract_v0",
        "contract_status": "PARKING_CONTRACT_FROZEN",
        "record_schema": {
            "schema_version": "o2_weak_feedback_parking_record_v0",
            "parking_id": "weak_parking_<sig8>",
            "source_feedback_ref": None,
            "park_reason": None,
            "blocked_moves": [],
            "lawful_reopen_conditions": [],
            "status": "PARKED_WITH_REASON",
        },
        "rule": "parking preserves the weak record without treating it as resolved.",
    }

    c5_block_contract = {
        "schema_version": "o2_weak_feedback_c5_block_contract_v0",
        "contract_status": "C5_BLOCK_CONTRACT_FROZEN",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_opened": False,
        "c5_unblock_requires": [
            "all weak records resolved by reviewed handling record",
            "or all weak records explicitly accepted as under-typed/question material by reviewed authority",
            "or later human-governed bounded decision overrides with receipts",
        ],
        "design_unit_does_not_unblock_c5": True,
        "next_build_unit_does_not_unblock_c5_unless_explicit_reviewed_policy_says_so": True,
    }

    build_authorization = {
        "schema_version": "o2_weak_feedback_handling_build_authorization_v0",
        "authorization_status": "BUILD_UNIT_AUTHORIZED_NEXT" if design_pass else "NOT_AUTHORIZED",
        "authorized_next_unit": AUTHORIZED_BUILD_UNIT if design_pass else None,
        "authorized_build_mode": "STATIC_WEAK_FEEDBACK_HANDLING_ONLY" if design_pass else None,
        "authorized_scope": [
            "consume weak feedback inventory",
            "emit handling records for the 3 weak records",
            "emit question packet candidates where required",
            "emit source-ref request candidates where required",
            "emit under-typed acceptance candidates where applicable",
            "emit parked-with-reason records where applicable",
            "emit rollup/readout/profile/report/receipt",
        ],
        "not_authorized": [
            "resolve weak feedback without explicit handling record",
            "run live feedback audit",
            "repair",
            "retry",
            "select build target",
            "patch runtime",
            "mutate sources",
            "open C5",
        ],
    }

    acceptance_gates = {
        "schema_version": "o2_weak_feedback_handling_acceptance_gates_v0",
        "gate_status": "ACCEPTANCE_GATES_FROZEN",
        "acceptance_gates": [
            "WFH_0_POST_O2_DECISION_RECEIPT_CONSUMED",
            "WFH_1_THREE_WEAK_RECORDS_INVENTORIED",
            "WFH_2_HANDLING_POLICY_ENUM_EMITTED",
            "WFH_3_QUESTION_PACKET_CONTRACT_EMITTED",
            "WFH_4_SOURCE_REF_REQUEST_CONTRACT_EMITTED",
            "WFH_5_UNDER_TYPED_ACCEPTANCE_CONTRACT_EMITTED",
            "WFH_6_PARKING_CONTRACT_EMITTED",
            "WFH_7_C5_BLOCK_CONTRACT_EMITTED",
            "WFH_8_BUILD_AUTHORIZATION_EMITTED",
            "WFH_9_NO_WEAK_FEEDBACK_RESOLUTION",
            "WFH_10_NO_LIVE_AUDIT",
            "WFH_11_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION",
            "WFH_12_NO_C5_OPENED",
            "WFH_13_NO_HIDDEN_NEXT_COMMAND",
        ],
    }

    negative_controls = {
        "schema_version": "o2_weak_feedback_handling_negative_controls_v0",
        "negative_control_status": "NEGATIVE_CONTROLS_FROZEN",
        "negative_controls": [
            "weak_feedback_resolved_by_design_fail",
            "question_packet_counted_as_answer_fail",
            "source_ref_request_counted_as_evidence_fail",
            "under_typed_acceptance_counted_as_c5_ready_fail",
            "parked_record_counted_as_resolved_fail",
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

    terminal_rules = {
        "schema_version": "o2_weak_feedback_handling_terminal_rules_v0",
        "terminal_rules_status": "TERMINAL_RULES_FROZEN",
        "success_terminal": {
            "type": "STOP",
            "stop_code": "STOP_O2_WEAK_FEEDBACK_HANDLING_TARGET_DESIGNED_BUILD_READY",
            "next_command_goal": None,
        },
        "basis_fail_terminal": {
            "type": "STOP",
            "stop_code": "STOP_O2_WEAK_FEEDBACK_HANDLING_TARGET_DESIGN_BASIS_FAIL",
            "next_command_goal": None,
        },
        "authority_violation_terminal": {
            "type": "STOP",
            "stop_code": "STOP_AUTHORITY_VIOLATION",
            "next_command_goal": None,
        },
    }

    downstream_decision_table = {
        "schema_version": "o2_weak_feedback_handling_target_downstream_decision_table_v0",
        "decision_status": "TARGET_BUILD_READY" if design_pass else "TARGET_BUILD_NOT_READY",
        "records": [
            {
                "decision": "BUILD_O2_WEAK_FEEDBACK_HANDLING",
                "selected": design_pass,
                "next_unit": AUTHORIZED_BUILD_UNIT if design_pass else None,
                "why": "The handling target has been designed; the next unit may emit handling records for the 3 weak feedback records.",
            },
            {
                "decision": "RESOLVE_WEAK_FEEDBACK_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Design freezes the handling target; resolution belongs to the later build/review path.",
            },
            {
                "decision": "RUN_LIVE_FEEDBACK_AUDIT_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Live audit remains deferred and requires explicit later objective.",
            },
            {
                "decision": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 remains blocked by weak feedback.",
            },
        ],
    }

    authority_boundary = {
        "schema_version": "o2_weak_feedback_handling_target_authority_boundary_v0",
        "status": status,
        "may_build_o2_weak_feedback_handling_next": design_pass,
        "may_resolve_weak_feedback_now": False,
        "may_run_live_feedback_audit_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_select_target_for_build": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_open_c5": False,
        "may_expand_authority": False,
    }

    classification = {
        "schema_version": "o2_weak_feedback_handling_target_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "target_designed": design_pass,
        "weak_feedback_count": decision_summary.get("weak_feedback_count"),
        "weak_records_inventoried_count": len(inventory),
        "authorized_next_unit": recommended_next,
        "weak_feedback_resolved": False,
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
        "schema_version": "o2_weak_feedback_handling_target_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "target_design_count": 1 if design_pass else 0,
        "weak_record_inventory_count": len(inventory),
        "weak_feedback_count": decision_summary.get("weak_feedback_count"),
        "under_typed_feedback_count": decision_summary.get("under_typed_feedback_count"),
        "ambiguous_requires_question_count": decision_summary.get("ambiguous_requires_question_count"),
        "question_packet_contract_count": 1 if design_pass else 0,
        "source_ref_request_contract_count": 1 if design_pass else 0,
        "under_typed_acceptance_contract_count": 1 if design_pass else 0,
        "parking_contract_count": 1 if design_pass else 0,
        "c5_block_contract_count": 1 if design_pass else 0,
        "build_authorized_next_count": 1 if design_pass else 0,
        "weak_feedback_resolved_count": 0,
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
        "schema_version": "o2_weak_feedback_handling_target_profile_v0",
        "profile_id": "o2_weak_feedback_handling_target_profile_" + sha8(rollup),
        "status": status,
        "target_designed": design_pass,
        "authorized_next_unit": recommended_next,
        "weak_feedback_count": decision_summary.get("weak_feedback_count"),
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Build the weak-feedback handling unit next in STATIC_WEAK_FEEDBACK_HANDLING_ONLY mode.",
        "must_not_infer": [
            "weak feedback resolved",
            "question packet answered",
            "source-ref request satisfied",
            "under-typed acceptance approved",
            "live audit complete",
            "C5 opened",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_weak_feedback_handling_target_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The O2 weak-feedback handling target was designed from the post-O2 closure decision. It inventories the 3 weak records, freezes handling policy options, question packet contract, source-ref request contract, under-typed acceptance candidate contract, parking contract, C5 block contract, acceptance gates, negative controls, terminal rules, and build authorization. It does not resolve weak feedback, run live audit, repair, retry, select target, patch runtime, mutate sources, or open C5.",
        "authorized_next_unit": recommended_next,
        "weak_feedback_count": decision_summary.get("weak_feedback_count"),
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_weak_feedback_handling_target_transition_trace_v0",
        "trace": [
            {
                "step": "consume_post_o2_decision",
                "question": "is weak-feedback handling target design authorized",
                "answer": "yes" if design_pass else "no",
                "taken": "design handling target",
            },
            {
                "step": "inventory_weak_records",
                "question": "which weak records are active",
                "answer": "2 UNDER_TYPED_FEEDBACK and 1 AMBIGUOUS_REQUIRES_QUESTION",
                "taken": "emit unresolved weak-record inventory",
            },
            {
                "step": "freeze_handling_contracts",
                "question": "what handling outputs may the next build emit",
                "answer": "question packets, source-ref requests, under-typed acceptance candidates, parked-with-reason records",
                "taken": "authorize static weak-feedback handling build next",
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
        (SOURCE_SCOPE_PATH, source_scope),
        (WEAK_RECORD_INVENTORY_PATH, weak_record_inventory),
        (HANDLING_POLICY_ENUM_PATH, handling_policy_enum),
        (QUESTION_PACKET_CONTRACT_PATH, question_packet_contract),
        (SOURCE_REF_REQUEST_CONTRACT_PATH, source_ref_request_contract),
        (UNDERTYPED_ACCEPTANCE_CONTRACT_PATH, undertyped_acceptance_contract),
        (PARKING_CONTRACT_PATH, parking_contract),
        (C5_BLOCK_CONTRACT_PATH, c5_block_contract),
        (BUILD_AUTHORIZATION_PATH, build_authorization),
        (ACCEPTANCE_GATES_PATH, acceptance_gates),
        (NEGATIVE_CONTROLS_PATH, negative_controls),
        (TERMINAL_RULES_PATH, terminal_rules),
        (DOWNSTREAM_DECISION_TABLE_PATH, downstream_decision_table),
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
        "WFH_DESIGN_0_POST_O2_DECISION_RECEIPT_CONSUMED": POST_O2_DECISION_RECEIPT_PATH.exists(),
        "WFH_DESIGN_1_TARGET_DEFINITION_EMITTED": TARGET_DEFINITION_PATH.exists(),
        "WFH_DESIGN_2_SOURCE_SCOPE_EMITTED": SOURCE_SCOPE_PATH.exists(),
        "WFH_DESIGN_3_THREE_WEAK_RECORDS_INVENTORIED": len(inventory) == 3,
        "WFH_DESIGN_4_HANDLING_POLICY_ENUM_EMITTED": HANDLING_POLICY_ENUM_PATH.exists() and len(HANDLING_POLICIES) == 5,
        "WFH_DESIGN_5_QUESTION_PACKET_CONTRACT_EMITTED": QUESTION_PACKET_CONTRACT_PATH.exists(),
        "WFH_DESIGN_6_SOURCE_REF_REQUEST_CONTRACT_EMITTED": SOURCE_REF_REQUEST_CONTRACT_PATH.exists(),
        "WFH_DESIGN_7_UNDER_TYPED_ACCEPTANCE_CONTRACT_EMITTED": UNDERTYPED_ACCEPTANCE_CONTRACT_PATH.exists(),
        "WFH_DESIGN_8_PARKING_CONTRACT_EMITTED": PARKING_CONTRACT_PATH.exists(),
        "WFH_DESIGN_9_C5_BLOCK_CONTRACT_EMITTED": C5_BLOCK_CONTRACT_PATH.exists(),
        "WFH_DESIGN_10_BUILD_AUTHORIZATION_EMITTED": BUILD_AUTHORIZATION_PATH.exists() and build_authorization["authorized_next_unit"] == AUTHORIZED_BUILD_UNIT,
        "WFH_DESIGN_11_ACCEPTANCE_GATES_EMITTED": ACCEPTANCE_GATES_PATH.exists(),
        "WFH_DESIGN_12_NEGATIVE_CONTROLS_EMITTED": NEGATIVE_CONTROLS_PATH.exists(),
        "WFH_DESIGN_13_TERMINAL_RULES_EMITTED": TERMINAL_RULES_PATH.exists(),
        "WFH_DESIGN_14_NO_WEAK_FEEDBACK_RESOLUTION": rollup["weak_feedback_resolved_count"] == 0,
        "WFH_DESIGN_15_NO_LIVE_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "WFH_DESIGN_16_NO_REPAIR_RETRY_TARGET_PATCH_SOURCE_MUTATION": rollup["repair_applied_count"] == 0 and rollup["retry_executed_count"] == 0 and rollup["target_selected_for_build_count"] == 0 and rollup["runtime_patch_count"] == 0 and rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "WFH_DESIGN_17_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "WFH_DESIGN_18_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "WFH_DESIGN_19_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "WFH_DESIGN_20_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_WEAK_FEEDBACK_HANDLING_TARGET_DESIGN_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "authorized_next_unit": recommended_next,
        "weak_records": len(inventory),
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_weak_feedback_handling_target_design_receipt_v0",
        "receipt_type": "TYPED_O2_WEAK_FEEDBACK_HANDLING_TARGET_DESIGN_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_post_o2_decision_receipt_id": POST_O2_DECISION_RECEIPT_ID,
        "machine_readable_o2_weak_feedback_target_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "target_designed": design_pass,
            "authorized_next_unit": recommended_next,
            "authorized_build_mode": "STATIC_WEAK_FEEDBACK_HANDLING_ONLY" if design_pass else None,
            "weak_feedback_count": decision_summary.get("weak_feedback_count"),
            "under_typed_feedback_count": decision_summary.get("under_typed_feedback_count"),
            "ambiguous_requires_question_count": decision_summary.get("ambiguous_requires_question_count"),
            "weak_records_inventoried_count": len(inventory),
            "handling_policy_enum_frozen": design_pass,
            "question_packet_contract_frozen": design_pass,
            "source_ref_request_contract_frozen": design_pass,
            "under_typed_acceptance_contract_frozen": design_pass,
            "parking_contract_frozen": design_pass,
            "c5_block_contract_frozen": design_pass,
            "weak_feedback_resolved": False,
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
            "source_scope": rel(SOURCE_SCOPE_PATH),
            "weak_record_inventory": rel(WEAK_RECORD_INVENTORY_PATH),
            "handling_policy_enum": rel(HANDLING_POLICY_ENUM_PATH),
            "question_packet_contract": rel(QUESTION_PACKET_CONTRACT_PATH),
            "source_ref_request_contract": rel(SOURCE_REF_REQUEST_CONTRACT_PATH),
            "under_typed_acceptance_contract": rel(UNDERTYPED_ACCEPTANCE_CONTRACT_PATH),
            "parking_contract": rel(PARKING_CONTRACT_PATH),
            "c5_block_contract": rel(C5_BLOCK_CONTRACT_PATH),
            "build_authorization": rel(BUILD_AUTHORIZATION_PATH),
            "acceptance_gates": rel(ACCEPTANCE_GATES_PATH),
            "negative_controls": rel(NEGATIVE_CONTROLS_PATH),
            "terminal_rules": rel(TERMINAL_RULES_PATH),
            "downstream_decision_table": rel(DOWNSTREAM_DECISION_TABLE_PATH),
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
    print(f"weak_feedback_target_design_receipt_id={receipt_id}")
    print(f"weak_feedback_target_design_receipt_path={rel(receipt_path)}")
    print(f"weak_feedback_target_definition_path={rel(TARGET_DEFINITION_PATH)}")
    print(f"weak_feedback_inventory_path={rel(WEAK_RECORD_INVENTORY_PATH)}")
    print(f"weak_feedback_handling_policy_enum_path={rel(HANDLING_POLICY_ENUM_PATH)}")
    print(f"weak_feedback_question_packet_contract_path={rel(QUESTION_PACKET_CONTRACT_PATH)}")
    print(f"weak_feedback_source_ref_request_contract_path={rel(SOURCE_REF_REQUEST_CONTRACT_PATH)}")
    print(f"under_typed_acceptance_contract_path={rel(UNDERTYPED_ACCEPTANCE_CONTRACT_PATH)}")
    print(f"weak_feedback_build_authorization_path={rel(BUILD_AUTHORIZATION_PATH)}")
    print(f"weak_feedback_target_rollup_path={rel(ROLLUP_PATH)}")
    print(f"weak_feedback_target_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
