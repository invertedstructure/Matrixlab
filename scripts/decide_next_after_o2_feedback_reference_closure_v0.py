#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_O2_FEEDBACK_REFERENCE_CLOSURE_V0"
TARGET_UNIT_ID = "observation.o2_post_closure_decision.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / POST_CLOSURE_DECISION"
MODE = "DECIDE_ONLY / SELECT_NEXT_BRANCH / NO_EXECUTION"
BUILD_MODE = "O2_POST_CLOSURE_DECISION_ONLY"

O2_CLOSURE_RECEIPT_ID = "bf5163d7"
O2_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0_receipts/bf5163d7.json"
O2_CLOSURE_RECORD_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_unit_feedback_hardening_closure_record_v0.json"
O2_REVIEWED_REFERENCE_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_unit_feedback_hardening_reviewed_reference_v0.json"
O2_WEAK_FEEDBACK_NOTE_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_weak_feedback_note_v0.json"
O2_C5_BLOCK_STATUS_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_c5_block_status_v0.json"
O2_REFERENCE_FREEZE_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_unit_feedback_hardening_reference_freeze_v0.json"
O2_RECEIPT_CHAIN_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_unit_feedback_hardening_receipt_chain_v0.json"
O2_BOUNDARY_LOCK_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_unit_feedback_hardening_boundary_lock_v0.json"
O2_CLOSURE_CLASSIFICATION_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_closure_classification_v0.json"
O2_CLOSURE_AUTHORITY_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_closure_authority_boundary_v0.json"
O2_CLOSURE_ROLLUP_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_closure_rollup_v0.json"
O2_CLOSURE_PROFILE_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_closure_profile_v0.json"
O2_CLOSURE_REPORT_PATH = ROOT / "data/o2_unit_feedback_hardening_closure_v0/o2_closure_report.json"
O2_FEEDBACK_RECORDS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_feedback_records_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    O2_CLOSURE_RECEIPT_PATH,
    O2_CLOSURE_RECORD_PATH,
    O2_REVIEWED_REFERENCE_PATH,
    O2_WEAK_FEEDBACK_NOTE_PATH,
    O2_C5_BLOCK_STATUS_PATH,
    O2_REFERENCE_FREEZE_PATH,
    O2_RECEIPT_CHAIN_PATH,
    O2_BOUNDARY_LOCK_PATH,
    O2_CLOSURE_CLASSIFICATION_PATH,
    O2_CLOSURE_AUTHORITY_PATH,
    O2_CLOSURE_ROLLUP_PATH,
    O2_CLOSURE_PROFILE_PATH,
    O2_CLOSURE_REPORT_PATH,
    O2_FEEDBACK_RECORDS_PATH,
]

OUT_DIR = ROOT / "data/o2_post_closure_decision_v0"
RECEIPT_DIR = ROOT / "data/o2_post_closure_decision_v0_receipts"

DECISION_BASIS_PATH = OUT_DIR / "o2_post_closure_decision_basis_v0.json"
DECISION_TABLE_PATH = OUT_DIR / "o2_post_closure_decision_table_v0.json"
SELECTED_BRANCH_PATH = OUT_DIR / "o2_selected_next_branch_v0.json"
WEAK_FEEDBACK_HANDLING_TARGET_AUTH_PATH = OUT_DIR / "o2_weak_feedback_handling_target_authorization_v0.json"
C5_BLOCK_CONTINUATION_PATH = OUT_DIR / "o2_c5_block_continuation_v0.json"
DEFERRED_BRANCHES_PATH = OUT_DIR / "o2_deferred_branches_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_post_closure_decision_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_post_closure_decision_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_post_closure_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_post_closure_decision_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_post_closure_decision_report.json"
TRACE_PATH = OUT_DIR / "o2_post_closure_decision_transition_trace.json"

EXPECTED_CLOSURE_STATUS = "TYPED_O2_UNIT_FEEDBACK_HARDENING_CLOSED_AS_REVIEWED_REFERENCE_WEAK_FEEDBACK_NOTE_DECISION_READY"
EXPECTED_CLOSURE_STOP = "STOP_TYPED_O2_UNIT_FEEDBACK_HARDENING_CLOSED_AS_REVIEWED_REFERENCE_WEAK_FEEDBACK_NOTE_DECISION_READY"
EXPECTED_CLOSURE_NEXT = "DECIDE_NEXT_AFTER_O2_FEEDBACK_REFERENCE_CLOSURE_V0"

SELECTED_NEXT_UNIT = "DESIGN_O2_WEAK_FEEDBACK_HANDLING_TARGET_V0"

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

    closure_receipt = read_json(O2_CLOSURE_RECEIPT_PATH)
    summary = closure_receipt.get("machine_readable_o2_closure_summary", {})
    weak_note = read_json(O2_WEAK_FEEDBACK_NOTE_PATH)
    c5_block = read_json(O2_C5_BLOCK_STATUS_PATH)
    boundary_lock = read_json(O2_BOUNDARY_LOCK_PATH)
    authority = read_json(O2_CLOSURE_AUTHORITY_PATH)
    rollup = read_json(O2_CLOSURE_ROLLUP_PATH)
    profile = read_json(O2_CLOSURE_PROFILE_PATH)
    report = read_json(O2_CLOSURE_REPORT_PATH)
    feedback_records = read_jsonl(O2_FEEDBACK_RECORDS_PATH)

    if closure_receipt.get("receipt_id") != O2_CLOSURE_RECEIPT_ID or closure_receipt.get("gate") != "PASS":
        failures.append("o2_closure_receipt_not_pass")
    if closure_receipt.get("terminal", {}).get("stop_code") != EXPECTED_CLOSURE_STOP:
        failures.append("o2_closure_terminal_not_expected")
    if closure_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("o2_closure_hidden_next_command")
    if summary.get("status") != EXPECTED_CLOSURE_STATUS:
        failures.append(f"o2_closure_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_CLOSURE_NEXT:
        failures.append(f"o2_closure_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "o2_closed_as_reviewed_reference",
        "reviewed_reference_emitted",
        "weak_feedback_note_frozen",
        "c5_block_status_frozen",
        "post_closure_decision_ready",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"closure_required_true_missing:{key}")

    for key in [
        "weak_feedback_resolved",
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
        if summary.get(key) is not False:
            failures.append(f"closure_forbidden_true:{key}")

    expected_counts = {
        "weak_feedback_count": 3,
        "under_typed_feedback_count": 2,
        "ambiguous_requires_question_count": 1,
        "feedback_records_frozen_count": 10,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"closure_count_wrong:{key}:{summary.get(key)}")

    if summary.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("closure_c5_readiness_not_blocked")
    if weak_note.get("note_status") != "WEAK_FEEDBACK_NOTE_FROZEN":
        failures.append("weak_feedback_note_not_frozen")
    if weak_note.get("weak_feedback_count") != 3:
        failures.append("weak_feedback_note_count_wrong")
    if c5_block.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("c5_block_readiness_wrong")
    if c5_block.get("closure_does_not_unblock_c5") is not True:
        failures.append("closure_does_not_unblock_c5_flag_wrong")
    if boundary_lock.get("weak_feedback_resolved") is not False:
        failures.append("boundary_lock_weak_feedback_resolved")
    if boundary_lock.get("c5_opened") is not False:
        failures.append("boundary_lock_c5_opened")
    if authority.get("may_decide_next_after_o2_reference_closure") is not True:
        failures.append("authority_does_not_allow_post_closure_decision")
    if authority.get("may_open_c5") is not False:
        failures.append("authority_allows_c5")
    if rollup.get("post_closure_decision_ready_count") != 1:
        failures.append("rollup_decision_ready_wrong")
    if rollup.get("c5_opened_count") != 0:
        failures.append("rollup_c5_opened_nonzero")
    if profile.get("post_closure_decision_ready") is not True:
        failures.append("profile_decision_ready_not_true")
    if report.get("recommended_next_handling") != EXPECTED_CLOSURE_NEXT:
        failures.append("report_recommended_next_wrong")
    if len(feedback_records) != 10:
        failures.append(f"feedback_records_count_wrong:{len(feedback_records)}")

    return failures, {
        "summary": summary,
        "weak_note": weak_note,
        "c5_block": c5_block,
        "feedback_records": feedback_records,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    summary = src.get("summary", {})
    weak_note = src.get("weak_note", {})
    c5_block = src.get("c5_block", {})
    feedback_records = src.get("feedback_records", [])

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    decision_pass = not failures
    status = "TYPED_O2_POST_CLOSURE_DECISION_SELECTED_WEAK_FEEDBACK_HANDLING_TARGET_READY" if decision_pass else "TYPED_O2_POST_CLOSURE_DECISION_BASIS_FAIL"
    recommended_next = SELECTED_NEXT_UNIT if decision_pass else "REPAIR_O2_POST_CLOSURE_DECISION_BASIS_V0"

    reason_codes = [
        "O2_POST_CLOSURE_DECISION_EMITTED",
        "O2_CLOSURE_RECEIPT_CONSUMED",
        "WEAK_FEEDBACK_UNRESOLVED_CONFIRMED",
        "C5_BLOCKED_BY_WEAK_FEEDBACK_CONFIRMED",
        "WEAK_FEEDBACK_HANDLING_SELECTED_NEXT",
        "QUESTION_UNDERTYPED_HANDLING_TARGET_DESIGN_AUTHORIZED",
        "LIVE_FEEDBACK_AUDIT_DEFERRED",
        "WEAK_FEEDBACK_RESOLUTION_DEFERRED_TO_DESIGN_TARGET",
        "C5_DEFERRED",
        "NO_LIVE_AUDIT_EXECUTED",
        "NO_WEAK_FEEDBACK_RESOLUTION_ATTEMPTED",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_TARGET_SELECTED_FOR_BUILD",
        "NO_RUNTIME_PATCH_APPLIED",
        "NO_SOURCE_MUTATION",
        "NO_C5_OPENED",
    ] if decision_pass else failures

    decision_basis = {
        "schema_version": "o2_post_closure_decision_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if decision_pass else "BASIS_REPAIR_REQUIRED",
        "source_o2_closure_receipt_id": O2_CLOSURE_RECEIPT_ID,
        "o2_closed_as_reviewed_reference": summary.get("o2_closed_as_reviewed_reference"),
        "weak_feedback_count": summary.get("weak_feedback_count"),
        "under_typed_feedback_count": summary.get("under_typed_feedback_count"),
        "ambiguous_requires_question_count": summary.get("ambiguous_requires_question_count"),
        "weak_feedback_resolved": summary.get("weak_feedback_resolved"),
        "c5_feedback_readiness": summary.get("c5_feedback_readiness"),
        "c5_opened": summary.get("c5_opened"),
        "feedback_records_available": len(feedback_records),
    }

    decision_table = {
        "schema_version": "o2_post_closure_decision_table_v0",
        "decision_status": "NEXT_BRANCH_SELECTED" if decision_pass else "NO_BRANCH_SELECTED",
        "records": [
            {
                "branch": "DESIGN_O2_WEAK_FEEDBACK_HANDLING_TARGET",
                "selected": decision_pass,
                "next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
                "why": "Weak feedback remains unresolved and typed; C5 is blocked until weak feedback is handled or explicitly accepted as under-typed/question material.",
            },
            {
                "branch": "RUN_LIVE_FEEDBACK_AUDIT_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Live feedback audit requires a later explicit source-receipt/traces objective and is not authorized by closure.",
            },
            {
                "branch": "RESOLVE_WEAK_FEEDBACK_NOW",
                "selected": False,
                "next_unit": None,
                "why": "This unit decides the next branch only; weak-feedback resolution belongs to a separate target design/build path.",
            },
            {
                "branch": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 remains blocked by weak feedback.",
            },
            {
                "branch": "DEFER_WEAK_FEEDBACK_AND_PICK_OTHER_PRE_C5_HARDENING",
                "selected": False,
                "next_unit": None,
                "why": "Weak feedback is the active blocker exposed by O2 closure; handle it first unless a later human decision overrides.",
            },
        ],
    }

    selected_branch = {
        "schema_version": "o2_selected_next_branch_v0",
        "selected_branch": "DESIGN_O2_WEAK_FEEDBACK_HANDLING_TARGET" if decision_pass else None,
        "selected_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "selection_reason": "Weak feedback remains typed and intentional, but unresolved; C5 remains blocked by that condition.",
        "selection_scope": "design target only",
        "selected_branch_does_not": [
            "resolve weak feedback now",
            "run live audit",
            "repair failure",
            "retry unit",
            "select build target",
            "patch runtime",
            "open C5",
        ],
    }

    weak_feedback_auth = {
        "schema_version": "o2_weak_feedback_handling_target_authorization_v0",
        "authorization_status": "TARGET_DESIGN_AUTHORIZED" if decision_pass else "NOT_AUTHORIZED",
        "authorized_next_unit": SELECTED_NEXT_UNIT if decision_pass else None,
        "target_goal": "Design a bounded weak-feedback handling target for the 2 UNDER_TYPED_FEEDBACK and 1 AMBIGUOUS_REQUIRES_QUESTION records preserved by O2 closure.",
        "target_should_define": [
            "whether each weak feedback record needs a question packet, source-ref request, or under-typed acceptance",
            "minimum evidence needed to resolve or park weak feedback",
            "how to preserve C5 block until weak feedback is resolved or explicitly accepted",
            "how to avoid treating weak feedback as failure, success, or repair",
        ],
        "target_may_not": [
            "resolve weak feedback during design",
            "run live feedback audit",
            "repair source artifacts",
            "retry failed units",
            "select target for build",
            "open C5",
        ],
    }

    c5_block_continuation = {
        "schema_version": "o2_c5_block_continuation_v0",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_opened": False,
        "block_continues": True,
        "block_reason": "weak_feedback_count=3 remains unresolved after O2 closure",
        "c5_may_be_reconsidered_only_after": [
            "weak-feedback handling design/build/review/closure resolves or explicitly accepts the weak records",
            "or a later human-governed decision explicitly authorizes another bounded pre-C5 path",
        ],
    }

    deferred_branches = {
        "schema_version": "o2_deferred_branches_v0",
        "deferred": [
            "LIVE_FEEDBACK_AUDIT",
            "WEAK_FEEDBACK_RESOLUTION_EXECUTION",
            "REPAIR",
            "RETRY",
            "TARGET_SELECTION",
            "RUNTIME_PATCH",
            "C5",
        ],
        "why": "The post-closure decision selects only the next target-design branch.",
    }

    authority_boundary = {
        "schema_version": "o2_post_closure_decision_authority_boundary_v0",
        "status": status,
        "may_design_o2_weak_feedback_handling_target_next": decision_pass,
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
        "schema_version": "o2_post_closure_decision_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "post_closure_decision_complete": decision_pass,
        "selected_next_unit": recommended_next,
        "weak_feedback_count": summary.get("weak_feedback_count"),
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
        "schema_version": "o2_post_closure_decision_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "decision_count": 1 if decision_pass else 0,
        "selected_weak_feedback_handling_target_count": 1 if decision_pass else 0,
        "weak_feedback_count": summary.get("weak_feedback_count"),
        "under_typed_feedback_count": summary.get("under_typed_feedback_count"),
        "ambiguous_requires_question_count": summary.get("ambiguous_requires_question_count"),
        "feedback_records_available_count": len(feedback_records),
        "c5_block_continuation_count": 1 if decision_pass else 0,
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
        "schema_version": "o2_post_closure_decision_profile_v0",
        "profile_id": "o2_post_closure_decision_profile_" + sha8(rollup),
        "status": status,
        "selected_next_unit": recommended_next,
        "decision": "handle weak feedback before C5",
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "weak_feedback_count": summary.get("weak_feedback_count"),
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
        "schema_version": "o2_post_closure_decision_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "Post-O2 decision selected weak-feedback handling target design as the next branch. O2 is closed as reviewed reference, weak feedback remains unresolved, and C5 remains blocked by weak feedback. This decision does not resolve weak feedback, run live audit, repair, retry, select a build target, patch runtime, mutate sources, or open C5.",
        "selected_next_unit": recommended_next,
        "weak_feedback_count": summary.get("weak_feedback_count"),
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "bad_counters_zero": profile["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_post_closure_decision_transition_trace_v0",
        "trace": [
            {
                "step": "consume_o2_closure",
                "question": "is O2 closed and post-closure decision ready",
                "answer": "yes" if decision_pass else "no",
                "taken": "evaluate next branch table",
            },
            {
                "step": "check_active_blocker",
                "question": "what blocks C5",
                "answer": "weak_feedback_count=3",
                "taken": "preserve C5 block",
            },
            {
                "step": "select_next_branch",
                "question": "what next branch is lawful",
                "answer": SELECTED_NEXT_UNIT if decision_pass else recommended_next,
                "taken": "authorize weak-feedback handling target design next",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (DECISION_BASIS_PATH, decision_basis),
        (DECISION_TABLE_PATH, decision_table),
        (SELECTED_BRANCH_PATH, selected_branch),
        (WEAK_FEEDBACK_HANDLING_TARGET_AUTH_PATH, weak_feedback_auth),
        (C5_BLOCK_CONTINUATION_PATH, c5_block_continuation),
        (DEFERRED_BRANCHES_PATH, deferred_branches),
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
        "O2_DECIDE_0_CLOSURE_RECEIPT_CONSUMED": O2_CLOSURE_RECEIPT_PATH.exists(),
        "O2_DECIDE_1_DECISION_BASIS_EMITTED": DECISION_BASIS_PATH.exists(),
        "O2_DECIDE_2_DECISION_TABLE_EMITTED": DECISION_TABLE_PATH.exists(),
        "O2_DECIDE_3_WEAK_FEEDBACK_UNRESOLVED_CONFIRMED": summary.get("weak_feedback_resolved") is False and summary.get("weak_feedback_count") == 3,
        "O2_DECIDE_4_C5_BLOCK_CONFIRMED": summary.get("c5_feedback_readiness") == "BLOCKED_BY_WEAK_FEEDBACK",
        "O2_DECIDE_5_WEAK_FEEDBACK_HANDLING_SELECTED": selected_branch["selected_next_unit"] == SELECTED_NEXT_UNIT,
        "O2_DECIDE_6_NEXT_TARGET_DESIGN_AUTHORIZED": weak_feedback_auth["authorized_next_unit"] == SELECTED_NEXT_UNIT,
        "O2_DECIDE_7_LIVE_AUDIT_DEFERRED": "LIVE_FEEDBACK_AUDIT" in deferred_branches["deferred"],
        "O2_DECIDE_8_WEAK_FEEDBACK_NOT_RESOLVED": rollup["weak_feedback_resolved_count"] == 0,
        "O2_DECIDE_9_NO_REPAIR_APPLIED": rollup["repair_applied_count"] == 0,
        "O2_DECIDE_10_NO_RETRY_EXECUTED": rollup["retry_executed_count"] == 0,
        "O2_DECIDE_11_NO_TARGET_SELECTED_FOR_BUILD": rollup["target_selected_for_build_count"] == 0,
        "O2_DECIDE_12_NO_RUNTIME_PATCH": rollup["runtime_patch_count"] == 0,
        "O2_DECIDE_13_NO_SOURCE_MUTATION": rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "O2_DECIDE_14_NO_C5_OPENED": rollup["c5_opened_count"] == 0,
        "O2_DECIDE_15_NO_LATEST_OR_MTIME": rollup["latest_file_guessing_count"] == 0 and rollup["mtime_selection_count"] == 0,
        "O2_DECIDE_16_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "O2_DECIDE_17_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_POST_CLOSURE_DECISION_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "selected": recommended_next,
        "weak": summary.get("weak_feedback_count"),
        "c5": "BLOCKED_BY_WEAK_FEEDBACK",
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_post_closure_decision_receipt_v0",
        "receipt_type": "TYPED_O2_POST_CLOSURE_DECISION_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_o2_closure_receipt_id": O2_CLOSURE_RECEIPT_ID,
        "machine_readable_o2_post_closure_decision_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "post_closure_decision_complete": decision_pass,
            "selected_next_branch": "DESIGN_O2_WEAK_FEEDBACK_HANDLING_TARGET" if decision_pass else None,
            "selected_next_unit": recommended_next,
            "weak_feedback_count": summary.get("weak_feedback_count"),
            "under_typed_feedback_count": summary.get("under_typed_feedback_count"),
            "ambiguous_requires_question_count": summary.get("ambiguous_requires_question_count"),
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
            "decision_basis": rel(DECISION_BASIS_PATH),
            "decision_table": rel(DECISION_TABLE_PATH),
            "selected_branch": rel(SELECTED_BRANCH_PATH),
            "weak_feedback_handling_target_authorization": rel(WEAK_FEEDBACK_HANDLING_TARGET_AUTH_PATH),
            "c5_block_continuation": rel(C5_BLOCK_CONTINUATION_PATH),
            "deferred_branches": rel(DEFERRED_BRANCHES_PATH),
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
    print(f"o2_post_closure_decision_receipt_id={receipt_id}")
    print(f"o2_post_closure_decision_receipt_path={rel(receipt_path)}")
    print(f"o2_post_closure_decision_basis_path={rel(DECISION_BASIS_PATH)}")
    print(f"o2_post_closure_decision_table_path={rel(DECISION_TABLE_PATH)}")
    print(f"o2_selected_next_branch_path={rel(SELECTED_BRANCH_PATH)}")
    print(f"o2_weak_feedback_handling_target_authorization_path={rel(WEAK_FEEDBACK_HANDLING_TARGET_AUTH_PATH)}")
    print(f"o2_c5_block_continuation_path={rel(C5_BLOCK_CONTINUATION_PATH)}")
    print(f"o2_post_closure_decision_rollup_path={rel(ROLLUP_PATH)}")
    print(f"o2_post_closure_decision_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
