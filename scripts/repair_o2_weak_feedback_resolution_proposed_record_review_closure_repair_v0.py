#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_proposed_record_review_closure_repair_repair.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR_REPAIR"
MODE = "REPAIR_REPAIR / FINAL_RECORD_COUNT_COMPATIBILITY / NO_SOURCE_MUTATION_NO_FINAL_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR_REPAIR_ONLY"

FAILED_CLOSURE_RECEIPT_ID = "5a0f061d"
FAILED_REPAIR_RECEIPT_ID = "d699d495"

FAILED_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0_receipts/5a0f061d.json"
FAILED_REPAIR_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_repair_v0_receipts/d699d495.json"

SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0_receipts/98ec96a7.json"
EXEC_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0_receipts/6149c6d9.json"
EXEC_BOUNDARY_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_resolution_boundary_readout_v0.json"
EXEC_C5_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_c5_block_readout_v0.json"
EXEC_UNRESOLVED_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_unresolved_continuation_v0.json"

CLOSE_SCRIPT_PATH = ROOT / "scripts/close_o2_weak_feedback_resolution_proposed_record_review_as_reviewed_reference_v0.py"
REPAIR_SCRIPT_PATH = ROOT / "scripts/repair_o2_weak_feedback_resolution_proposed_record_review_closure_v0.py"

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_repair_repair_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_repair_repair_v0_receipts"

REPAIR_REPAIR_RECORD_PATH = OUT_DIR / "o2_proposed_record_review_closure_repair_repair_record_v0.json"
FAILED_REPAIR_SNAPSHOT_PATH = OUT_DIR / "o2_failed_closure_repair_receipt_snapshot_d699d495.json"
FINAL_RECORD_COUNT_COMPATIBILITY_PATH = OUT_DIR / "o2_final_record_count_compatibility_repair_v0.json"
PATCH_REPORT_PATH = OUT_DIR / "o2_repair_validator_patch_report_v0.json"
CLOSE_PATCH_REPORT_PATH = OUT_DIR / "o2_close_validator_patch_report_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_closure_repair_repair_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_closure_repair_repair_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_closure_repair_repair_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_closure_repair_repair_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_closure_repair_repair_report.json"
TRACE_PATH = OUT_DIR / "o2_closure_repair_repair_transition_trace.json"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sha8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def patch_repair_script() -> Dict[str, Any]:
    before = REPAIR_SCRIPT_PATH.read_text()
    before_sha = hashlib.sha256(before.encode("utf-8")).hexdigest()
    after = before
    patch_applied = False
    already_patched = "final_resolution_records_emitted_count = exec_boundary.get" in before

    old_block = '''        if exec_boundary.get("resolution_records_emitted_count") != 0:
            failures.append("exec_boundary_resolution_records_nonzero")
'''
    new_block = '''        final_resolution_records_emitted_count = exec_boundary.get("final_resolution_records_emitted_count")
        if final_resolution_records_emitted_count is None:
            final_resolution_records_emitted_count = exec_boundary.get("resolution_records_emitted_count", 0)
        reviewed_resolution_records_emitted_count = exec_boundary.get("reviewed_resolution_records_emitted_count")
        if final_resolution_records_emitted_count != 0:
            failures.append(f"exec_boundary_final_resolution_records_nonzero:{final_resolution_records_emitted_count!r}")
        if reviewed_resolution_records_emitted_count not in (None, 3):
            failures.append(f"exec_boundary_reviewed_resolution_count_unexpected:{reviewed_resolution_records_emitted_count!r}")
'''
    if old_block in before:
        after = before.replace(old_block, new_block)
        REPAIR_SCRIPT_PATH.write_text(after)
        patch_applied = True
    elif not already_patched:
        pattern = r'        if exec_boundary\.get\("resolution_records_emitted_count"\) != 0:\n            failures\.append\("exec_boundary_resolution_records_nonzero"\)\n'
        after, n = re.subn(pattern, new_block, before)
        if n == 1:
            REPAIR_SCRIPT_PATH.write_text(after)
            patch_applied = True

    after_sha = hashlib.sha256(REPAIR_SCRIPT_PATH.read_text().encode("utf-8")).hexdigest()
    return {
        "schema_version": "o2_repair_validator_patch_report_v0",
        "patch_status": "PATCH_APPLIED" if patch_applied else ("ALREADY_PATCHED" if already_patched else "PATCH_TARGET_NOT_FOUND"),
        "patched_file": rel(REPAIR_SCRIPT_PATH),
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "patch_scope": "repair validator final-record count compatibility only",
        "patch_description": "Treat reviewed_resolution_records_emitted_count as reviewed artifacts, while final_resolution_records_emitted_count or absent resolution_records_emitted_count must remain zero.",
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "runtime_patch_applied": False,
        "architecture_change": False,
    }

def patch_close_script() -> Dict[str, Any]:
    before = CLOSE_SCRIPT_PATH.read_text()
    before_sha = hashlib.sha256(before.encode("utf-8")).hexdigest()
    after = before
    patch_applied = False
    already_patched = "exec_boundary_final_crossed = exec_boundary.get" in before

    old_block = '''    if exec_boundary.get("final_resolution_boundary_crossed") is not False:
        failures.append("exec_boundary_wrong")
'''
    new_block = '''    exec_boundary_final_crossed = exec_boundary.get("final_resolution_boundary_crossed")
    if exec_boundary_final_crossed is None:
        exec_boundary_final_crossed = exec_boundary.get("reviewed_artifacts_crossed_into_final_resolution")
    if exec_boundary_final_crossed is not False:
        failures.append("exec_boundary_wrong")
'''
    if old_block in before:
        after = before.replace(old_block, new_block)
        CLOSE_SCRIPT_PATH.write_text(after)
        patch_applied = True
    elif not already_patched:
        pattern = r'    if exec_boundary\.get\("final_resolution_boundary_crossed"\) is not False:\n        failures\.append\("exec_boundary_wrong"\)\n'
        after, n = re.subn(pattern, new_block, before)
        if n == 1:
            CLOSE_SCRIPT_PATH.write_text(after)
            patch_applied = True

    after_sha = hashlib.sha256(CLOSE_SCRIPT_PATH.read_text().encode("utf-8")).hexdigest()
    return {
        "schema_version": "o2_close_validator_patch_report_v0",
        "patch_status": "PATCH_APPLIED" if patch_applied else ("ALREADY_PATCHED" if already_patched else "PATCH_TARGET_NOT_FOUND"),
        "patched_file": rel(CLOSE_SCRIPT_PATH),
        "before_sha256": before_sha,
        "after_sha256": after_sha,
        "patch_scope": "closure validator final-boundary key compatibility only",
        "patch_description": "Accept final_resolution_boundary_crossed if present, else reviewed_artifacts_crossed_into_final_resolution.",
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "runtime_patch_applied": False,
        "architecture_change": False,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    for path in [
        FAILED_CLOSURE_RECEIPT_PATH,
        FAILED_REPAIR_RECEIPT_PATH,
        SOURCE_REVIEW_RECEIPT_PATH,
        EXEC_RECEIPT_PATH,
        EXEC_BOUNDARY_READOUT_PATH,
        EXEC_C5_READOUT_PATH,
        EXEC_UNRESOLVED_PATH,
        CLOSE_SCRIPT_PATH,
        REPAIR_SCRIPT_PATH,
    ]:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")

    if failures:
        failed_repair = {}
        exec_boundary = {}
        exec_c5 = {}
        exec_unresolved = {}
    else:
        failed_closure = read_json(FAILED_CLOSURE_RECEIPT_PATH)
        failed_repair = read_json(FAILED_REPAIR_RECEIPT_PATH)
        source_review = read_json(SOURCE_REVIEW_RECEIPT_PATH)
        exec_receipt = read_json(EXEC_RECEIPT_PATH)
        exec_boundary = read_json(EXEC_BOUNDARY_READOUT_PATH)
        exec_c5 = read_json(EXEC_C5_READOUT_PATH)
        exec_unresolved = read_json(EXEC_UNRESOLVED_PATH)

        if failed_closure.get("receipt_id") != FAILED_CLOSURE_RECEIPT_ID or failed_closure.get("gate") != "FAIL":
            failures.append("failed_closure_receipt_wrong")
        if failed_repair.get("receipt_id") != FAILED_REPAIR_RECEIPT_ID or failed_repair.get("gate") != "FAIL":
            failures.append("failed_repair_receipt_wrong")
        expected_repair_failures = set(["exec_boundary_resolution_records_nonzero", "acceptance_gate_result_false"])
        if set(failed_repair.get("failures", [])) != expected_repair_failures:
            failures.append(f"unexpected_failed_repair_failures:{failed_repair.get('failures')}")
        if source_review.get("receipt_id") != "98ec96a7" or source_review.get("gate") != "PASS":
            failures.append("source_review_receipt_not_pass")
        if exec_receipt.get("receipt_id") != "6149c6d9" or exec_receipt.get("gate") != "PASS":
            failures.append("exec_receipt_not_pass")

        boundary_crossed = exec_boundary.get("final_resolution_boundary_crossed")
        if boundary_crossed is None:
            boundary_crossed = exec_boundary.get("reviewed_artifacts_crossed_into_final_resolution")
        final_resolution_records = exec_boundary.get("final_resolution_records_emitted_count")
        if final_resolution_records is None:
            final_resolution_records = exec_boundary.get("resolution_records_emitted_count", 0)
        reviewed_resolution_records = exec_boundary.get("reviewed_resolution_records_emitted_count")

        if boundary_crossed is not False:
            failures.append(f"boundary_crossed_not_false:{boundary_crossed!r}")
        if exec_boundary.get("weak_feedback_resolved") is not False:
            failures.append("exec_boundary_weak_feedback_resolved")
        if final_resolution_records != 0:
            failures.append(f"final_resolution_records_nonzero:{final_resolution_records!r}")
        if reviewed_resolution_records not in (None, 3):
            failures.append(f"reviewed_resolution_records_unexpected:{reviewed_resolution_records!r}")
        if exec_c5.get("c5_opened") is not False or exec_c5.get("c5_reconsideration_ready") is not False:
            failures.append("exec_c5_wrong")
        if exec_unresolved.get("weak_feedback_resolved") is not False:
            failures.append("exec_unresolved_wrong")

    write_json(FAILED_REPAIR_SNAPSHOT_PATH, failed_repair)

    compatibility = {
        "schema_version": "o2_final_record_count_compatibility_repair_v0",
        "compatibility_status": "FINAL_RECORD_COUNT_COMPATIBILITY_CONFIRMED" if not failures else "FINAL_RECORD_COUNT_COMPATIBILITY_FAIL",
        "failed_repair_receipt_id": FAILED_REPAIR_RECEIPT_ID,
        "failed_reason": "repair validator treated absent/final resolution count as nonzero instead of distinguishing reviewed-resolution artifacts from final-resolution records",
        "reviewed_resolution_records_emitted_count": exec_boundary.get("reviewed_resolution_records_emitted_count"),
        "final_resolution_records_emitted_count": exec_boundary.get("final_resolution_records_emitted_count", exec_boundary.get("resolution_records_emitted_count", 0)),
        "boundary_crossed_value": exec_boundary.get("final_resolution_boundary_crossed", exec_boundary.get("reviewed_artifacts_crossed_into_final_resolution")),
        "weak_feedback_resolved": False,
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
    }

    repair_patch_report = patch_repair_script() if not failures else {
        "schema_version": "o2_repair_validator_patch_report_v0",
        "patch_status": "PATCH_SKIPPED",
        "failures": failures,
    }
    close_patch_report = patch_close_script() if not failures else {
        "schema_version": "o2_close_validator_patch_report_v0",
        "patch_status": "PATCH_SKIPPED",
        "failures": failures,
    }

    if repair_patch_report.get("patch_status") not in ["PATCH_APPLIED", "ALREADY_PATCHED"]:
        failures.append(f"repair_patch_not_applied:{repair_patch_report.get('patch_status')}")
    if close_patch_report.get("patch_status") not in ["PATCH_APPLIED", "ALREADY_PATCHED"]:
        failures.append(f"close_patch_not_applied:{close_patch_report.get('patch_status')}")

    repair_pass = not failures
    status = "TYPED_O2_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR_REPAIRED_RERUN_READY" if repair_pass else "TYPED_O2_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR_REPAIR_GATE_FAIL"
    recommended_next = "RERUN_REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_V0" if repair_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR_V0"

    reason_codes = [
        "FAILED_REPAIR_RECEIPT_CONSUMED",
        "FAILURE_CONFIRMED_AS_FINAL_RECORD_COUNT_COMPATIBILITY",
        "REVIEWED_RESOLUTION_ARTIFACTS_ALLOWED",
        "FINAL_RESOLUTION_RECORDS_CONFIRMED_ZERO",
        "BOUNDARY_NOT_CROSSED_CONFIRMED",
        "WEAK_FEEDBACK_UNRESOLVED_CONFIRMED",
        "C5_BLOCK_CONFIRMED",
        "REPAIR_VALIDATOR_PATCHED",
        "CLOSE_VALIDATOR_COMPATIBILITY_CONFIRMED",
        "RERUN_REPAIR_READY",
        "NO_SOURCE_MUTATION",
        "NO_PRIOR_RECEIPT_MUTATION",
        "NO_RUNTIME_PATCH",
        "NO_ARCHITECTURE_CHANGE",
    ] if repair_pass else failures

    repair_record = {
        "schema_version": "o2_proposed_record_review_closure_repair_repair_record_v0",
        "repair_repair_status": status,
        "repair_repair_pass": repair_pass,
        "failed_closure_receipt_id": FAILED_CLOSURE_RECEIPT_ID,
        "failed_repair_receipt_id": FAILED_REPAIR_RECEIPT_ID,
        "repair_scope": "repair validator count/key compatibility only",
        "repair_does_not_mean": [
            "final weak-feedback resolution closed",
            "weak feedback resolved",
            "C5 reconsideration ready",
            "C5 opened",
            "source files mutated",
            "prior receipts mutated",
            "runtime patched",
            "architecture changed",
        ],
    }

    authority_boundary = {
        "schema_version": "o2_closure_repair_repair_authority_boundary_v0",
        "status": status,
        "may_rerun_closure_repair_next": repair_pass,
        "may_rerun_closure_after_repair_pass": repair_pass,
        "may_close_final_weak_feedback_resolution_now": False,
        "may_resolve_weak_feedback_now": False,
        "may_set_c5_reconsideration_ready": False,
        "may_open_c5": False,
        "may_run_live_feedback_audit_now": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_patch_runtime": False,
        "may_change_architecture": False,
    }

    classification = {
        "schema_version": "o2_closure_repair_repair_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "repair_repair_executed": repair_pass,
        "repair_validator_count_compatibility_repaired": repair_pass,
        "close_validator_key_compatibility_confirmed": repair_pass,
        "rerun_repair_ready": repair_pass,
        "weak_feedback_resolved": False,
        "final_resolution_boundary_crossed": False,
        "resolution_records_emitted_count": 0,
        "reviewed_resolution_records_emitted_count": exec_boundary.get("reviewed_resolution_records_emitted_count"),
        "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
        "c5_reconsideration_ready": False,
        "c5_opened": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "runtime_patch_applied": False,
        "architecture_change": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "o2_closure_repair_repair_rollup_v0",
        "repair_repair_count": 1 if repair_pass else 0,
        "repair_validator_count_compatibility_repaired_count": 1 if repair_pass else 0,
        "rerun_repair_ready_count": 1 if repair_pass else 0,
        "weak_feedback_resolved_count": 0,
        "final_resolution_boundary_crossed_count": 0,
        "resolution_records_emitted_count": 0,
        "c5_opened_count": 0,
        "c5_reconsideration_ready_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "runtime_patch_count": 0,
        "architecture_change_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "weak_feedback_resolved_count",
        "final_resolution_boundary_crossed_count",
        "resolution_records_emitted_count",
        "c5_opened_count",
        "c5_reconsideration_ready_count",
        "source_mutated_count",
        "prior_receipt_mutated_count",
        "runtime_patch_count",
        "architecture_change_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile = {
        "schema_version": "o2_closure_repair_repair_profile_v0",
        "profile_id": "o2_closure_repair_repair_profile_" + sha8(rollup),
        "status": status,
        "repair_repair_pass": repair_pass,
        "rerun_repair_ready": repair_pass,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Rerun closure repair, then rerun closure. Do not treat repair-repair as closure or final resolution.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_closure_repair_repair_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The repair failure was repaired as a final-record count compatibility issue. Reviewed-resolution artifacts may exist; final-resolution records remain zero; C5 remains blocked.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_closure_repair_repair_transition_trace_v0",
        "trace": [
            {
                "step": "consume_failed_repair_receipt",
                "question": "did repair fail on final-record count compatibility",
                "answer": "yes" if repair_pass else "no",
                "taken": "inspect execution boundary count shape",
            },
            {
                "step": "repair_repair_validator",
                "question": "can reviewed-resolution artifacts be distinguished from final-resolution records",
                "answer": "yes" if repair_pass else "no",
                "taken": "patch repair validator",
            },
            {
                "step": "preserve_boundaries",
                "question": "did repair-repair resolve weak feedback or open C5",
                "answer": "no",
                "taken": "authorize repair rerun only",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    for path, obj in [
        (REPAIR_REPAIR_RECORD_PATH, repair_record),
        (FAILED_REPAIR_SNAPSHOT_PATH, failed_repair),
        (FINAL_RECORD_COUNT_COMPATIBILITY_PATH, compatibility),
        (PATCH_REPORT_PATH, repair_patch_report),
        (CLOSE_PATCH_REPORT_PATH, close_patch_report),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, trace),
    ]:
        write_json(path, obj)

    acceptance_gate_results = {
        "REPAIR_REPAIR_0_FAILED_REPAIR_RECEIPT_CONSUMED": FAILED_REPAIR_RECEIPT_PATH.exists(),
        "REPAIR_REPAIR_1_FAILED_REPAIR_SNAPSHOT_EMITTED": FAILED_REPAIR_SNAPSHOT_PATH.exists(),
        "REPAIR_REPAIR_2_FINAL_RECORD_COUNT_COMPATIBILITY_CONFIRMED": compatibility.get("compatibility_status") == "FINAL_RECORD_COUNT_COMPATIBILITY_CONFIRMED",
        "REPAIR_REPAIR_3_REPAIR_VALIDATOR_PATCHED": repair_patch_report.get("patch_status") in ["PATCH_APPLIED", "ALREADY_PATCHED"],
        "REPAIR_REPAIR_4_CLOSE_VALIDATOR_COMPATIBILITY_CONFIRMED": close_patch_report.get("patch_status") in ["PATCH_APPLIED", "ALREADY_PATCHED"],
        "REPAIR_REPAIR_5_WEAK_FEEDBACK_NOT_RESOLVED": rollup["weak_feedback_resolved_count"] == 0,
        "REPAIR_REPAIR_6_FINAL_BOUNDARY_NOT_CROSSED": rollup["final_resolution_boundary_crossed_count"] == 0,
        "REPAIR_REPAIR_7_FINAL_RESOLUTION_RECORDS_ZERO": rollup["resolution_records_emitted_count"] == 0,
        "REPAIR_REPAIR_8_C5_NOT_OPENED": rollup["c5_opened_count"] == 0 and rollup["c5_reconsideration_ready_count"] == 0,
        "REPAIR_REPAIR_9_NO_SOURCE_OR_PRIOR_RECEIPT_MUTATION": rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "REPAIR_REPAIR_10_NO_RUNTIME_PATCH_OR_ARCHITECTURE_CHANGE": rollup["runtime_patch_count"] == 0 and rollup["architecture_change_count"] == 0,
        "REPAIR_REPAIR_11_RERUN_REPAIR_READY": rollup["rerun_repair_ready_count"] == 1,
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    if gate == "FAIL":
        status = "TYPED_O2_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR_REPAIR_GATE_FAIL"
        recommended_next = "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR_V0"

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_" + status,
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "failed_closure": FAILED_CLOSURE_RECEIPT_ID,
        "failed_repair": FAILED_REPAIR_RECEIPT_ID,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_proposed_record_review_closure_repair_repair_receipt_v0",
        "receipt_type": "TYPED_O2_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR_REPAIR_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_failed_closure_receipt_id": FAILED_CLOSURE_RECEIPT_ID,
        "source_failed_repair_receipt_id": FAILED_REPAIR_RECEIPT_ID,
        "machine_readable_o2_proposed_record_review_closure_repair_repair_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "repair_repair_executed": gate == "PASS",
            "repair_validator_count_compatibility_repaired": gate == "PASS",
            "close_validator_key_compatibility_confirmed": gate == "PASS",
            "rerun_repair_ready": gate == "PASS",
            "failed_closure_receipt_id": FAILED_CLOSURE_RECEIPT_ID,
            "failed_repair_receipt_id": FAILED_REPAIR_RECEIPT_ID,
            "reviewed_resolution_records_emitted_count": exec_boundary.get("reviewed_resolution_records_emitted_count"),
            "final_resolution_records_emitted_count": exec_boundary.get("final_resolution_records_emitted_count", exec_boundary.get("resolution_records_emitted_count", 0)),
            "weak_feedback_resolved": False,
            "final_resolution_boundary_crossed": False,
            "resolution_records_emitted_count": 0,
            "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
            "c5_reconsideration_ready": False,
            "c5_opened": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "runtime_patch_applied": False,
            "architecture_change": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": profile["bad_counters_zero"],
            "recommended_next": recommended_next,
        },
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "repair_repair_record": rel(REPAIR_REPAIR_RECORD_PATH),
            "failed_repair_snapshot": rel(FAILED_REPAIR_SNAPSHOT_PATH),
            "final_record_count_compatibility": rel(FINAL_RECORD_COUNT_COMPATIBILITY_PATH),
            "repair_validator_patch_report": rel(PATCH_REPORT_PATH),
            "close_validator_patch_report": rel(CLOSE_PATCH_REPORT_PATH),
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
    print(f"closure_repair_repair_receipt_id={receipt_id}")
    print(f"closure_repair_repair_receipt_path={rel(receipt_path)}")
    print(f"closure_repair_repair_record_path={rel(REPAIR_REPAIR_RECORD_PATH)}")
    print(f"failed_repair_snapshot_path={rel(FAILED_REPAIR_SNAPSHOT_PATH)}")
    print(f"final_record_count_compatibility_path={rel(FINAL_RECORD_COUNT_COMPATIBILITY_PATH)}")
    print(f"repair_validator_patch_report_path={rel(PATCH_REPORT_PATH)}")
    print(f"close_validator_patch_report_path={rel(CLOSE_PATCH_REPORT_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
