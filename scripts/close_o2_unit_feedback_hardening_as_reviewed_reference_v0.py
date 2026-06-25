#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_O2_UNIT_FEEDBACK_HARDENING_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "observation.unit_feedback_hardening_closure.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / CLOSURE"
MODE = "CLOSE / FREEZE_REVIEWED_REFERENCE / WEAK_FEEDBACK_NOTE / NO_C5"
BUILD_MODE = "O2_CLOSURE_ONLY"

O2_REVIEW_RECEIPT_ID = "ddf04eb2"
O2_REVIEW_RECEIPT_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0_receipts/ddf04eb2.json"
O2_REVIEW_ASSESSMENT_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_unit_feedback_hardening_review_assessment_v0.json"
O2_SCHEMA_REVIEW_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_schema_artifact_review_v0.json"
O2_FEEDBACK_RECORD_REVIEW_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_feedback_record_integrity_review_v0.json"
O2_WEAK_FEEDBACK_REVIEW_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_weak_feedback_intentionality_review_v0.json"
O2_EXPECTED_LIMIT_REVIEW_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_expected_limit_separation_review_v0.json"
O2_RETRY_GATE_REVIEW_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_retry_gate_review_v0.json"
O2_CANDIDATE_ONLY_REVIEW_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_candidate_only_boundary_review_v0.json"
O2_C5_READINESS_REVIEW_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_c5_feedback_readiness_review_v0.json"
O2_NONAUTHORITY_SAFETY_REVIEW_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_nonauthority_safety_review_v0.json"
O2_CLOSURE_CANDIDATE_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_unit_feedback_hardening_closure_candidate_v0.json"
O2_REVIEW_CLASSIFICATION_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_review_classification_v0.json"
O2_REVIEW_AUTHORITY_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_review_authority_boundary_v0.json"
O2_REVIEW_ROLLUP_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_review_rollup_v0.json"
O2_REVIEW_PROFILE_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_review_profile_v0.json"
O2_REVIEW_REPORT_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_review_report.json"
O2_REVIEW_TRACE_PATH = ROOT / "data/o2_unit_feedback_hardening_review_v0/o2_review_transition_trace.json"

O2_BUILD_RECEIPT_PATH = ROOT / "data/o2_unit_feedback_hardening_v0_receipts/131d6837.json"
O2_FEEDBACK_RECORDS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_feedback_records_v0.jsonl"
O2_ROLLUP_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_feedback_rollup_v0.json"
O2_READOUT_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_feedback_readout_v0.json"
O2_PROFILE_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/o2_feedback_profile_v0.json"
O2_REPORT_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/o2_report.json"

REQUIRED_SOURCE_FILES = [
    O2_REVIEW_RECEIPT_PATH,
    O2_REVIEW_ASSESSMENT_PATH,
    O2_SCHEMA_REVIEW_PATH,
    O2_FEEDBACK_RECORD_REVIEW_PATH,
    O2_WEAK_FEEDBACK_REVIEW_PATH,
    O2_EXPECTED_LIMIT_REVIEW_PATH,
    O2_RETRY_GATE_REVIEW_PATH,
    O2_CANDIDATE_ONLY_REVIEW_PATH,
    O2_C5_READINESS_REVIEW_PATH,
    O2_NONAUTHORITY_SAFETY_REVIEW_PATH,
    O2_CLOSURE_CANDIDATE_PATH,
    O2_REVIEW_CLASSIFICATION_PATH,
    O2_REVIEW_AUTHORITY_PATH,
    O2_REVIEW_ROLLUP_PATH,
    O2_REVIEW_PROFILE_PATH,
    O2_REVIEW_REPORT_PATH,
    O2_REVIEW_TRACE_PATH,
    O2_BUILD_RECEIPT_PATH,
    O2_FEEDBACK_RECORDS_PATH,
    O2_ROLLUP_PATH,
    O2_READOUT_PATH,
    O2_PROFILE_PATH,
    O2_REPORT_PATH,
]

OUT_DIR = ROOT / "data/o2_unit_feedback_hardening_closure_v0"
RECEIPT_DIR = ROOT / "data/o2_unit_feedback_hardening_closure_v0_receipts"

CLOSURE_RECORD_PATH = OUT_DIR / "o2_unit_feedback_hardening_closure_record_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "o2_unit_feedback_hardening_reviewed_reference_v0.json"
WEAK_FEEDBACK_NOTE_PATH = OUT_DIR / "o2_weak_feedback_note_v0.json"
C5_BLOCK_PATH = OUT_DIR / "o2_c5_block_status_v0.json"
REFERENCE_FREEZE_PATH = OUT_DIR / "o2_unit_feedback_hardening_reference_freeze_v0.json"
RECEIPT_CHAIN_PATH = OUT_DIR / "o2_unit_feedback_hardening_receipt_chain_v0.json"
BOUNDARY_LOCK_PATH = OUT_DIR / "o2_unit_feedback_hardening_boundary_lock_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o2_closure_downstream_decision_table_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_closure_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_closure_authority_boundary_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_closure_report.json"
TRACE_PATH = OUT_DIR / "o2_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_O2_UNIT_FEEDBACK_HARDENING_REVIEWED_STATIC_PROBE_CLEAN_WEAK_FEEDBACK_INTENTIONAL_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_O2_UNIT_FEEDBACK_HARDENING_REVIEWED_STATIC_PROBE_CLEAN_WEAK_FEEDBACK_INTENTIONAL_CLOSE_READY"
EXPECTED_REVIEW_NEXT = "CLOSE_O2_UNIT_FEEDBACK_HARDENING_AS_REVIEWED_REFERENCE_V0"

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

    review_receipt = read_json(O2_REVIEW_RECEIPT_PATH)
    review_summary = review_receipt.get("machine_readable_o2_review_summary", {})
    review_assessment = read_json(O2_REVIEW_ASSESSMENT_PATH)
    weak_feedback_review = read_json(O2_WEAK_FEEDBACK_REVIEW_PATH)
    expected_limit_review = read_json(O2_EXPECTED_LIMIT_REVIEW_PATH)
    retry_gate_review = read_json(O2_RETRY_GATE_REVIEW_PATH)
    candidate_only_review = read_json(O2_CANDIDATE_ONLY_REVIEW_PATH)
    c5_review = read_json(O2_C5_READINESS_REVIEW_PATH)
    safety_review = read_json(O2_NONAUTHORITY_SAFETY_REVIEW_PATH)
    closure_candidate = read_json(O2_CLOSURE_CANDIDATE_PATH)
    review_rollup = read_json(O2_REVIEW_ROLLUP_PATH)
    review_profile = read_json(O2_REVIEW_PROFILE_PATH)
    build_receipt = read_json(O2_BUILD_RECEIPT_PATH)
    feedback_records = read_jsonl(O2_FEEDBACK_RECORDS_PATH)
    build_rollup = read_json(O2_ROLLUP_PATH)
    build_readout = read_json(O2_READOUT_PATH)

    if review_receipt.get("receipt_id") != O2_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("o2_review_receipt_not_pass")
    if review_receipt.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("o2_review_terminal_not_expected")
    if review_summary.get("status") != EXPECTED_REVIEW_STATUS:
        failures.append(f"o2_review_status_not_expected:{review_summary.get('status')}")
    if review_summary.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append(f"o2_review_next_not_expected:{review_summary.get('recommended_next')}")

    for key in [
        "o2_review_complete",
        "o2_review_pass",
        "weak_feedback_intentional",
        "refinement_candidates_proposed_only",
        "missing_capabilities_candidate_only",
        "closure_candidate_ready",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_required_true_missing:{key}")

    for key in [
        "live_feedback_audit_executed",
        "repair_applied",
        "retry_executed",
        "target_selected_for_build",
        "runtime_patch_applied",
        "source_mutated",
        "prior_receipt_mutated",
        "architecture_change",
        "c5_opened",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if review_summary.get(key) is not False:
            failures.append(f"review_forbidden_true:{key}")

    expected_counts = {
        "schemas_reviewed": 8,
        "demo_events_reviewed": 10,
        "feedback_records_reviewed": 10,
        "weak_feedback_count": 3,
        "bare_failed_status_count": 0,
        "no_feedback_count": 0,
        "status_only_count": 0,
        "under_typed_feedback_count": 2,
        "ambiguous_requires_question_count": 1,
        "expected_limit_count": 1,
        "retry_blocked_count": 10,
    }
    for key, expected in expected_counts.items():
        if review_summary.get(key) != expected:
            failures.append(f"review_count_wrong:{key}:{review_summary.get(key)}")

    if review_summary.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("review_c5_readiness_not_blocked")
    if review_assessment.get("closure_candidate_ready") is not True:
        failures.append("assessment_closure_not_ready")
    if weak_feedback_review.get("review_status") != "WEAK_FEEDBACK_INTENTIONAL_AND_TYPED":
        failures.append("weak_feedback_review_not_pass")
    if expected_limit_review.get("review_status") != "EXPECTED_LIMITS_SEPARATED_FROM_BUGS":
        failures.append("expected_limit_review_not_pass")
    if retry_gate_review.get("review_status") != "UNCHANGED_RETRIES_BLOCKED":
        failures.append("retry_gate_review_not_pass")
    if candidate_only_review.get("review_status") != "CANDIDATE_ONLY_BOUNDARY_PASS":
        failures.append("candidate_only_review_not_pass")
    if c5_review.get("review_status") != "C5_BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("c5_review_not_blocked")
    if safety_review.get("review_status") != "NONAUTHORITY_SAFETY_REVIEW_PASS":
        failures.append("safety_review_not_pass")
    if closure_candidate.get("closure_candidate_status") != "O2_CLOSURE_CANDIDATE_READY_WITH_WEAK_FEEDBACK_NOTE":
        failures.append("closure_candidate_not_ready")
    if review_rollup.get("closure_candidate_count") != 1:
        failures.append("review_rollup_closure_count_wrong")
    if review_profile.get("weak_feedback_intentional") is not True:
        failures.append("review_profile_weak_feedback_not_intentional")
    if build_receipt.get("receipt_id") != "131d6837":
        failures.append("build_receipt_wrong")
    if len(feedback_records) != 10:
        failures.append(f"feedback_records_count_wrong:{len(feedback_records)}")
    if build_rollup.get("weak_feedback_count") != 3:
        failures.append("build_rollup_weak_feedback_count_wrong")
    if build_readout.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("build_readout_c5_readiness_wrong")

    return failures, {
        "review_summary": review_summary,
        "feedback_records": feedback_records,
        "build_rollup": build_rollup,
        "build_readout": build_readout,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    review_summary = src.get("review_summary", {})
    feedback_records = src.get("feedback_records", [])
    build_rollup = src.get("build_rollup", {})
    build_readout = src.get("build_readout", {})

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    closed = not failures
    status = "TYPED_O2_UNIT_FEEDBACK_HARDENING_CLOSED_AS_REVIEWED_REFERENCE_WEAK_FEEDBACK_NOTE_DECISION_READY" if closed else "TYPED_O2_UNIT_FEEDBACK_HARDENING_CLOSURE_BASIS_FAIL"
    recommended_next = "DECIDE_NEXT_AFTER_O2_FEEDBACK_REFERENCE_CLOSURE_V0" if closed else "REPAIR_O2_UNIT_FEEDBACK_HARDENING_CLOSURE_V0"

    reason_codes = [
        "O2_CLOSED_AS_REVIEWED_REFERENCE",
        "O2_REVIEW_RECEIPT_CONSUMED",
        "STATIC_SCHEMA_PROBE_REFERENCE_FROZEN",
        "TEN_FEEDBACK_RECORDS_FROZEN_AS_REVIEWED_REFERENCE",
        "WEAK_FEEDBACK_NOTE_FROZEN",
        "WEAK_FEEDBACK_INTENTIONAL_AND_TYPED",
        "C5_BLOCK_STATUS_FROZEN",
        "C5_REMAINS_BLOCKED_BY_WEAK_FEEDBACK",
        "MISSING_CAPABILITIES_REMAIN_CANDIDATE_ONLY",
        "REFINEMENT_CANDIDATES_REMAIN_PROPOSED_ONLY",
        "RETRY_GATE_BEHAVIOR_FROZEN",
        "EXPECTED_LIMITS_SEPARATED_FROM_BUGS",
        "NO_LIVE_FEEDBACK_AUDIT_EXECUTED",
        "NO_WEAK_FEEDBACK_RESOLUTION_ATTEMPTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_TARGET_SELECTED_FOR_BUILD",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
        "NO_C5_OPENED",
        "POST_CLOSURE_DECISION_READY",
    ] if closed else failures

    closure_record = {
        "schema_version": "o2_unit_feedback_hardening_closure_record_v0",
        "closure_status": "CLOSED_AS_REVIEWED_REFERENCE_WITH_WEAK_FEEDBACK_NOTE" if closed else "CLOSURE_NOT_RECORDED",
        "source_review_receipt_id": O2_REVIEW_RECEIPT_ID,
        "closed_object": "o2_unit_feedback_hardening_static_schema_probe_v0",
        "closure_basis": {
            "o2_review_pass": closed,
            "schemas_reviewed": review_summary.get("schemas_reviewed"),
            "demo_events_reviewed": review_summary.get("demo_events_reviewed"),
            "feedback_records_reviewed": review_summary.get("feedback_records_reviewed"),
            "weak_feedback_count": review_summary.get("weak_feedback_count"),
            "c5_feedback_readiness": review_summary.get("c5_feedback_readiness"),
        },
        "closure_meaning": "O2 static schema/probe feedback-hardening machinery is frozen as a reviewed reference with weak-feedback note.",
        "closure_does_not_mean": [
            "weak feedback resolved",
            "live feedback audit executed",
            "failure repaired",
            "target selected",
            "retry authorized",
            "runtime patched",
            "C5 opened",
        ],
    }

    reviewed_reference = {
        "schema_version": "o2_unit_feedback_hardening_reviewed_reference_v0",
        "reference_status": "FROZEN_REVIEWED_REFERENCE" if closed else "REFERENCE_NOT_FROZEN",
        "reference_object_id": "o2_feedback_reviewed_reference_" + sha8({
            "source_review_receipt_id": O2_REVIEW_RECEIPT_ID,
            "feedback_records": len(feedback_records),
            "weak_feedback_count": review_summary.get("weak_feedback_count"),
            "c5_feedback_readiness": review_summary.get("c5_feedback_readiness"),
        }),
        "source_review_receipt_id": O2_REVIEW_RECEIPT_ID,
        "source_build_receipt_id": "131d6837",
        "source_design_receipt_id": "e55e60e1",
        "schemas_reviewed": review_summary.get("schemas_reviewed"),
        "feedback_records_frozen": len(feedback_records),
        "weak_feedback_count": review_summary.get("weak_feedback_count"),
        "under_typed_feedback_count": review_summary.get("under_typed_feedback_count"),
        "ambiguous_requires_question_count": review_summary.get("ambiguous_requires_question_count"),
        "expected_limit_count": review_summary.get("expected_limit_count"),
        "retry_blocked_count": review_summary.get("retry_blocked_count"),
        "reference_use": "future units may cite this reviewed O2 static-probe feedback machinery as the unit failure diagnostic reference surface",
        "reference_not_authority_for": [
            "resolving weak feedback",
            "running live audit",
            "repair execution",
            "retry execution",
            "target selection",
            "runtime patch",
            "C5 opening",
        ],
    }

    weak_feedback_note = {
        "schema_version": "o2_weak_feedback_note_v0",
        "note_status": "WEAK_FEEDBACK_NOTE_FROZEN",
        "weak_feedback_count": review_summary.get("weak_feedback_count"),
        "under_typed_feedback_count": review_summary.get("under_typed_feedback_count"),
        "ambiguous_requires_question_count": review_summary.get("ambiguous_requires_question_count"),
        "no_feedback_count": review_summary.get("no_feedback_count"),
        "status_only_count": review_summary.get("status_only_count"),
        "bare_failed_status_count": review_summary.get("bare_failed_status_count"),
        "interpretation": "Weak feedback remains intentionally as typed static-probe signal. It is not bare failure, not accidental weak output, and not C5-ready.",
        "allowed_next_handling": [
            "explicit decision on weak-feedback handling",
            "future question packet design",
            "future live audit target design with explicit source receipts",
        ],
        "forbidden_next_handling": [
            "silently count weak feedback as resolved",
            "open C5",
            "retry without changed evidence",
            "repair inside closure",
        ],
    }

    c5_block = {
        "schema_version": "o2_c5_block_status_v0",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_opened": False,
        "block_reason": "Weak feedback count remains 3 and is intentionally preserved as typed under-typed/question material.",
        "unblock_requires_one_of": [
            "weak feedback resolved by explicit later unit",
            "weak feedback explicitly accepted as under-typed/question-packet material by later decision",
            "live feedback audit design and review with explicit source receipts",
        ],
        "closure_does_not_unblock_c5": True,
    }

    reference_freeze = {
        "schema_version": "o2_unit_feedback_hardening_reference_freeze_v0",
        "freeze_status": "FREEZE_COMPLETE" if closed else "FREEZE_NOT_COMPLETE",
        "frozen_reference_path": rel(REVIEWED_REFERENCE_PATH),
        "weak_feedback_note_path": rel(WEAK_FEEDBACK_NOTE_PATH),
        "c5_block_status_path": rel(C5_BLOCK_PATH),
        "may_mutate_prior_artifacts": False,
        "may_reopen_without_explicit_new_objective": False,
        "may_resolve_weak_feedback_inside_closure": False,
        "may_open_c5": False,
    }

    receipt_chain = {
        "schema_version": "o2_unit_feedback_hardening_receipt_chain_v0",
        "chain_status": "RECEIPT_CHAIN_PRESERVED",
        "receipts": [
            {"stage": "o1_closure", "receipt_id": "e9d2dcf5"},
            {"stage": "o2_target_design", "receipt_id": "e55e60e1"},
            {"stage": "o2_static_probe_build", "receipt_id": "131d6837"},
            {"stage": "o2_review", "receipt_id": O2_REVIEW_RECEIPT_ID},
        ],
        "closure_receipt_pending": True,
    }

    boundary_lock = {
        "schema_version": "o2_unit_feedback_hardening_boundary_lock_v0",
        "boundary_lock_status": "BOUNDARIES_LOCKED_AT_CLOSURE",
        "o2_closed_as_reviewed_reference": closed,
        "static_schema_probe_reference": True,
        "weak_feedback_resolved": False,
        "weak_feedback_intentional": True,
        "live_feedback_audit_executed": False,
        "repair_applied": False,
        "retry_executed": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "architecture_change": False,
        "c5_opened": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
    }

    downstream_decision_table = {
        "schema_version": "o2_closure_downstream_decision_table_v0",
        "decision_status": "O2_CLOSURE_DOWNSTREAM_TABLE_EMITTED",
        "records": [
            {
                "decision": "DECIDE_NEXT_AFTER_O2_FEEDBACK_REFERENCE_CLOSURE",
                "selected": closed,
                "next_unit": "DECIDE_NEXT_AFTER_O2_FEEDBACK_REFERENCE_CLOSURE_V0" if closed else None,
                "why": "O2 is closed as reviewed reference, but weak feedback remains and C5 is blocked.",
            },
            {
                "decision": "RESOLVE_WEAK_FEEDBACK_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Closure freezes weak-feedback note; it does not resolve it.",
            },
            {
                "decision": "RUN_LIVE_FEEDBACK_AUDIT_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Live audit requires explicit later source-receipt/traces objective.",
            },
            {
                "decision": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 remains blocked by weak feedback.",
            },
        ],
    }

    classification = {
        "schema_version": "o2_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "o2_closed_as_reviewed_reference": closed,
        "reviewed_reference_emitted": closed,
        "weak_feedback_note_frozen": closed,
        "weak_feedback_count": review_summary.get("weak_feedback_count"),
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_block_status_frozen": closed,
        "post_closure_decision_ready": closed,
        "recommended_next": recommended_next,
        "live_feedback_audit_executed": False,
        "repair_applied": False,
        "retry_executed": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "architecture_change": False,
        "c5_opened": False,
        "hidden_next_command": False,
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "o2_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_o2_reference_closure": closed,
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

    rollup = {
        "schema_version": "o2_closure_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "o2_closure_count": 1 if closed else 0,
        "reviewed_reference_emitted_count": 1 if closed else 0,
        "weak_feedback_note_frozen_count": 1 if closed else 0,
        "feedback_records_frozen_count": len(feedback_records),
        "weak_feedback_count": review_summary.get("weak_feedback_count"),
        "under_typed_feedback_count": review_summary.get("under_typed_feedback_count"),
        "ambiguous_requires_question_count": review_summary.get("ambiguous_requires_question_count"),
        "expected_limit_count": review_summary.get("expected_limit_count"),
        "retry_blocked_count": review_summary.get("retry_blocked_count"),
        "c5_block_count": 1 if closed else 0,
        "post_closure_decision_ready_count": 1 if closed else 0,
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
        "schema_version": "o2_closure_profile_v0",
        "profile_id": "o2_closure_profile_" + sha8(rollup),
        "status": status,
        "o2_closed_as_reviewed_reference": closed,
        "weak_feedback_note_frozen": closed,
        "weak_feedback_count": review_summary.get("weak_feedback_count"),
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "post_closure_decision_ready": closed,
        "recommendation": "Proceed to a bounded post-O2 decision. Do not open C5 until weak feedback is resolved or explicitly accepted as under-typed/question material.",
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "must_not_infer": [
            "weak feedback resolved",
            "live audit complete",
            "repair applied",
            "retry authorized",
            "target selected",
            "C5 opened",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "O2 was closed as a reviewed reference with weak-feedback note. The static schema/probe feedback machinery, 10 reviewed feedback records, candidate-only missing capabilities, proposed-only refinements, retry-gate behavior, expected-limit separation, and C5 block status are frozen as reference context. Weak feedback remains intentional and typed. Closure does not resolve weak feedback, run live audit, repair, retry, select target, patch runtime, mutate sources, or open C5.",
        "weak_feedback_count": review_summary.get("weak_feedback_count"),
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_o2_review",
                "question": "is O2 reviewed clean and close-ready",
                "answer": "yes" if closed else "no",
                "taken": "close O2 as reviewed reference",
            },
            {
                "step": "freeze_weak_feedback_note",
                "question": "does weak feedback remain",
                "answer": "yes: weak_feedback_count=3",
                "taken": "freeze weak-feedback note and preserve C5 block",
            },
            {
                "step": "authorize_post_closure_decision",
                "question": "what is lawful after O2 closure",
                "answer": recommended_next,
                "taken": "stop at post-closure decision point",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (CLOSURE_RECORD_PATH, closure_record),
        (REVIEWED_REFERENCE_PATH, reviewed_reference),
        (WEAK_FEEDBACK_NOTE_PATH, weak_feedback_note),
        (C5_BLOCK_PATH, c5_block),
        (REFERENCE_FREEZE_PATH, reference_freeze),
        (RECEIPT_CHAIN_PATH, receipt_chain),
        (BOUNDARY_LOCK_PATH, boundary_lock),
        (DOWNSTREAM_DECISION_TABLE_PATH, downstream_decision_table),
        (CLASSIFICATION_PATH, classification),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, trace),
    ]
    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "O2_CLOSE_0_REVIEW_RECEIPT_CONSUMED": O2_REVIEW_RECEIPT_PATH.exists(),
        "O2_CLOSE_1_CLOSURE_RECORD_EMITTED": CLOSURE_RECORD_PATH.exists(),
        "O2_CLOSE_2_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists(),
        "O2_CLOSE_3_WEAK_FEEDBACK_NOTE_FROZEN": WEAK_FEEDBACK_NOTE_PATH.exists() and review_summary.get("weak_feedback_count") == 3,
        "O2_CLOSE_4_C5_BLOCK_STATUS_FROZEN": C5_BLOCK_PATH.exists(),
        "O2_CLOSE_5_REFERENCE_FREEZE_EMITTED": REFERENCE_FREEZE_PATH.exists(),
        "O2_CLOSE_6_RECEIPT_CHAIN_EMITTED": RECEIPT_CHAIN_PATH.exists(),
        "O2_CLOSE_7_BOUNDARY_LOCK_EMITTED": BOUNDARY_LOCK_PATH.exists(),
        "O2_CLOSE_8_TEN_FEEDBACK_RECORDS_FROZEN": len(feedback_records) == 10,
        "O2_CLOSE_9_WEAK_FEEDBACK_NOT_RESOLVED": rollup["weak_feedback_resolved_count"] == 0,
        "O2_CLOSE_10_C5_REMAINS_BLOCKED": rollup["c5_block_count"] == 1 and rollup["c5_opened_count"] == 0,
        "O2_CLOSE_11_NO_LIVE_FEEDBACK_AUDIT": rollup["live_feedback_audit_executed_count"] == 0,
        "O2_CLOSE_12_NO_REPAIR_APPLIED": rollup["repair_applied_count"] == 0,
        "O2_CLOSE_13_NO_RETRY_EXECUTED": rollup["retry_executed_count"] == 0,
        "O2_CLOSE_14_NO_TARGET_SELECTED_FOR_BUILD": rollup["target_selected_for_build_count"] == 0,
        "O2_CLOSE_15_NO_RUNTIME_PATCH": rollup["runtime_patch_count"] == 0,
        "O2_CLOSE_16_NO_SOURCE_MUTATION": rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "O2_CLOSE_17_NO_ARCHITECTURE_CHANGE": rollup["architecture_change_count"] == 0,
        "O2_CLOSE_18_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "O2_CLOSE_19_POST_CLOSURE_DECISION_READY": rollup["post_closure_decision_ready_count"] == 1,
        "O2_CLOSE_20_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_UNIT_FEEDBACK_HARDENING_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "closed": closed,
        "weak": review_summary.get("weak_feedback_count"),
        "c5": "BLOCKED_BY_WEAK_FEEDBACK",
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_unit_feedback_hardening_closure_receipt_v0",
        "receipt_type": "TYPED_O2_UNIT_FEEDBACK_HARDENING_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_o2_review_receipt_id": O2_REVIEW_RECEIPT_ID,
        "machine_readable_o2_closure_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "o2_closed_as_reviewed_reference": closed,
            "reviewed_reference_emitted": closed,
            "weak_feedback_note_frozen": closed,
            "weak_feedback_count": review_summary.get("weak_feedback_count"),
            "under_typed_feedback_count": review_summary.get("under_typed_feedback_count"),
            "ambiguous_requires_question_count": review_summary.get("ambiguous_requires_question_count"),
            "feedback_records_frozen_count": len(feedback_records),
            "weak_feedback_resolved": False,
            "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
            "c5_block_status_frozen": closed,
            "post_closure_decision_ready": closed,
            "live_feedback_audit_executed": False,
            "repair_applied": False,
            "retry_executed": False,
            "target_selected_for_build": False,
            "runtime_patch_applied": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "architecture_change": False,
            "c5_opened": False,
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
            "closure_record": rel(CLOSURE_RECORD_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "weak_feedback_note": rel(WEAK_FEEDBACK_NOTE_PATH),
            "c5_block_status": rel(C5_BLOCK_PATH),
            "reference_freeze": rel(REFERENCE_FREEZE_PATH),
            "receipt_chain": rel(RECEIPT_CHAIN_PATH),
            "boundary_lock": rel(BOUNDARY_LOCK_PATH),
            "downstream_decision_table": rel(DOWNSTREAM_DECISION_TABLE_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
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
    print(f"o2_closure_receipt_id={receipt_id}")
    print(f"o2_closure_receipt_path={rel(receipt_path)}")
    print(f"o2_closure_record_path={rel(CLOSURE_RECORD_PATH)}")
    print(f"o2_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"o2_weak_feedback_note_path={rel(WEAK_FEEDBACK_NOTE_PATH)}")
    print(f"o2_c5_block_status_path={rel(C5_BLOCK_PATH)}")
    print(f"o2_reference_freeze_path={rel(REFERENCE_FREEZE_PATH)}")
    print(f"o2_receipt_chain_path={rel(RECEIPT_CHAIN_PATH)}")
    print(f"o2_boundary_lock_path={rel(BOUNDARY_LOCK_PATH)}")
    print(f"o2_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"o2_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
