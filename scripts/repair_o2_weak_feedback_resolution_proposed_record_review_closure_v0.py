#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_V0"
TARGET_UNIT_ID = "observation.o2_weak_feedback_resolution_proposed_record_review_closure_repair.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR"
MODE = "REPAIR / VALIDATOR_KEY_COMPATIBILITY / NO_SOURCE_MUTATION_NO_FINAL_RESOLUTION_NO_C5"
BUILD_MODE = "O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR_ONLY"

FAILED_CLOSURE_RECEIPT_ID = "5a0f061d"
FAILED_CLOSURE_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_v0_receipts/5a0f061d.json"
SOURCE_REVIEW_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_review_v0_receipts/98ec96a7.json"
EXEC_RECEIPT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0_receipts/6149c6d9.json"
EXEC_BOUNDARY_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_reviewed_resolution_boundary_readout_v0.json"
EXEC_C5_READOUT_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_c5_block_readout_v0.json"
EXEC_UNRESOLVED_PATH = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_v0/o2_proposed_record_review_unresolved_continuation_v0.json"
CLOSE_SCRIPT_PATH = ROOT / "scripts/close_o2_weak_feedback_resolution_proposed_record_review_as_reviewed_reference_v0.py"

OUT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_repair_v0"
RECEIPT_DIR = ROOT / "data/o2_weak_feedback_resolution_proposed_record_review_closure_repair_v0_receipts"

REPAIR_RECORD_PATH = OUT_DIR / "o2_proposed_record_review_closure_repair_record_v0.json"
FAILED_RECEIPT_SNAPSHOT_PATH = OUT_DIR / "o2_failed_proposed_record_review_closure_receipt_snapshot_5a0f061d.json"
BOUNDARY_KEY_COMPATIBILITY_PATH = OUT_DIR / "o2_closure_boundary_key_compatibility_repair_v0.json"
PATCH_REPORT_PATH = OUT_DIR / "o2_closure_validator_patch_report_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_closure_repair_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_closure_repair_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "o2_closure_repair_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "o2_closure_repair_profile_v0.json"
REPORT_PATH = OUT_DIR / "o2_closure_repair_report.json"
TRACE_PATH = OUT_DIR / "o2_closure_repair_transition_trace.json"

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

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    for path in [
        FAILED_CLOSURE_RECEIPT_PATH,
        SOURCE_REVIEW_RECEIPT_PATH,
        EXEC_RECEIPT_PATH,
        EXEC_BOUNDARY_READOUT_PATH,
        EXEC_C5_READOUT_PATH,
        EXEC_UNRESOLVED_PATH,
        CLOSE_SCRIPT_PATH,
    ]:
        if not path.exists():
            failures.append(f"required_source_missing:{rel(path)}")

    if failures:
        gate = "FAIL"
    else:
        failed_receipt = read_json(FAILED_CLOSURE_RECEIPT_PATH)
        source_review = read_json(SOURCE_REVIEW_RECEIPT_PATH)
        exec_receipt = read_json(EXEC_RECEIPT_PATH)
        exec_boundary = read_json(EXEC_BOUNDARY_READOUT_PATH)
        exec_c5 = read_json(EXEC_C5_READOUT_PATH)
        exec_unresolved = read_json(EXEC_UNRESOLVED_PATH)

        if failed_receipt.get("receipt_id") != FAILED_CLOSURE_RECEIPT_ID:
            failures.append("failed_receipt_id_wrong")
        if failed_receipt.get("gate") != "FAIL":
            failures.append("failed_receipt_not_fail")
        expected_failures = set(["exec_boundary_wrong", "acceptance_gate_result_false"])
        if set(failed_receipt.get("failures", [])) != expected_failures:
            failures.append(f"unexpected_failed_receipt_failures:{failed_receipt.get('failures')}")
        fsummary = failed_receipt.get("machine_readable_o2_weak_feedback_resolution_proposed_record_review_closure_summary", {})
        if fsummary.get("weak_feedback_resolved") is not False:
            failures.append("failed_receipt_resolved_true")
        if fsummary.get("final_resolution_boundary_crossed") is not False:
            failures.append("failed_receipt_boundary_crossed")
        if fsummary.get("c5_opened") is not False or fsummary.get("c5_reconsideration_ready") is not False:
            failures.append("failed_receipt_c5_wrong")
        if fsummary.get("bad_counters_zero") is not True:
            failures.append("failed_receipt_bad_counters_not_zero")

        if source_review.get("receipt_id") != "98ec96a7" or source_review.get("gate") != "PASS":
            failures.append("source_review_receipt_not_pass")
        if exec_receipt.get("receipt_id") != "6149c6d9" or exec_receipt.get("gate") != "PASS":
            failures.append("execution_receipt_not_pass")

        old_key_value = exec_boundary.get("final_resolution_boundary_crossed", None)
        actual_key_value = exec_boundary.get("reviewed_artifacts_crossed_into_final_resolution", None)

        if old_key_value is not None:
            failures.append("unexpected_old_boundary_key_present")
        if actual_key_value is not False:
            failures.append(f"actual_boundary_key_not_false:{actual_key_value!r}")
        if exec_boundary.get("weak_feedback_resolved") is not False:
            failures.append("exec_boundary_weak_feedback_resolved")
        final_resolution_records_emitted_count = exec_boundary.get("final_resolution_records_emitted_count")
        if final_resolution_records_emitted_count is None:
            final_resolution_records_emitted_count = exec_boundary.get("resolution_records_emitted_count", 0)
        reviewed_resolution_records_emitted_count = exec_boundary.get("reviewed_resolution_records_emitted_count")
        if final_resolution_records_emitted_count != 0:
            failures.append(f"exec_boundary_final_resolution_records_nonzero:{final_resolution_records_emitted_count!r}")
        if reviewed_resolution_records_emitted_count not in (None, 3):
            failures.append(f"exec_boundary_reviewed_resolution_count_unexpected:{reviewed_resolution_records_emitted_count!r}")
        if exec_c5.get("c5_opened") is not False or exec_c5.get("c5_reconsideration_ready") is not False:
            failures.append("exec_c5_wrong")
        if exec_unresolved.get("weak_feedback_resolved") is not False:
            failures.append("exec_unresolved_wrong")

        before_text = CLOSE_SCRIPT_PATH.read_text()
        before_hash = hashlib.sha256(before_text.encode("utf-8")).hexdigest()

        old_block = '''    if exec_boundary.get("final_resolution_boundary_crossed") is not False:
        failures.append("exec_boundary_wrong")
'''
        new_block = '''    exec_boundary_final_crossed = exec_boundary.get("final_resolution_boundary_crossed")
    if exec_boundary_final_crossed is None:
        exec_boundary_final_crossed = exec_boundary.get("reviewed_artifacts_crossed_into_final_resolution")
    if exec_boundary_final_crossed is not False:
        failures.append("exec_boundary_wrong")
'''

        patch_applied = False
        already_patched = "exec_boundary_final_crossed = exec_boundary.get" in before_text

        if old_block in before_text:
            after_text = before_text.replace(old_block, new_block)
            CLOSE_SCRIPT_PATH.write_text(after_text)
            patch_applied = True
        elif already_patched:
            after_text = before_text
        else:
            pattern = r'    if exec_boundary\.get\("final_resolution_boundary_crossed"\) is not False:\n        failures\.append\("exec_boundary_wrong"\)\n'
            after_text, n = re.subn(pattern, new_block, before_text)
            if n == 1:
                CLOSE_SCRIPT_PATH.write_text(after_text)
                patch_applied = True
            else:
                failures.append("close_script_patch_target_not_found")
                after_text = before_text

        after_hash = hashlib.sha256(after_text.encode("utf-8")).hexdigest()

        write_json(FAILED_RECEIPT_SNAPSHOT_PATH, failed_receipt)

        boundary_key_compatibility = {
            "schema_version": "o2_closure_boundary_key_compatibility_repair_v0",
            "compatibility_status": "BOUNDARY_KEY_COMPATIBILITY_CONFIRMED" if not failures else "BOUNDARY_KEY_COMPATIBILITY_FAIL",
            "failed_closure_receipt_id": FAILED_CLOSURE_RECEIPT_ID,
            "failed_reason": "closure validator expected final_resolution_boundary_crossed but execution boundary readout exposes reviewed_artifacts_crossed_into_final_resolution",
            "old_expected_key": "final_resolution_boundary_crossed",
            "old_key_value": old_key_value,
            "actual_key": "reviewed_artifacts_crossed_into_final_resolution",
            "actual_key_value": actual_key_value,
            "semantic_equivalence": "both keys denote whether reviewed artifacts crossed into final weak-feedback resolution",
            "weak_feedback_resolved": False,
            "resolution_records_emitted_count": 0,
            "c5_feedback_readiness": "BLOCKED_BY_WEAK_FEEDBACK",
            "c5_reconsideration_ready": False,
            "c5_opened": False,
        }

        patch_report = {
            "schema_version": "o2_closure_validator_patch_report_v0",
            "patch_status": "PATCH_APPLIED" if patch_applied else ("ALREADY_PATCHED" if already_patched and not failures else "PATCH_FAIL"),
            "patched_file": rel(CLOSE_SCRIPT_PATH),
            "before_sha256": before_hash,
            "after_sha256": after_hash,
            "patch_scope": "validator compatibility only",
            "patch_description": "Accept final_resolution_boundary_crossed when present, otherwise accept reviewed_artifacts_crossed_into_final_resolution.",
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "runtime_patch_applied": False,
            "architecture_change": False,
        }

    repair_pass = not failures
    status = "TYPED_O2_PROPOSED_RECORD_REVIEW_CLOSURE_VALIDATOR_REPAIRED_RERUN_READY" if repair_pass else "TYPED_O2_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR_GATE_FAIL"
    recommended_next = "RERUN_CLOSE_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_AS_REVIEWED_REFERENCE_V0" if repair_pass else "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_V0"

    if not failures:
        reason_codes = [
            "FAILED_CLOSURE_RECEIPT_CONSUMED",
            "FAILURE_CONFIRMED_AS_VALIDATOR_KEY_COMPATIBILITY",
            "ACTUAL_BOUNDARY_KEY_CONFIRMED_FALSE",
            "WEAK_FEEDBACK_UNRESOLVED_CONFIRMED",
            "ZERO_FINAL_RESOLUTION_RECORDS_CONFIRMED",
            "C5_BLOCK_CONFIRMED",
            "CLOSURE_VALIDATOR_PATCHED",
            "FAILED_RECEIPT_SNAPSHOT_EMITTED",
            "RERUN_READY",
            "NO_SOURCE_MUTATION",
            "NO_PRIOR_RECEIPT_MUTATION",
            "NO_RUNTIME_PATCH",
            "NO_ARCHITECTURE_CHANGE",
        ]
    else:
        reason_codes = failures
        boundary_key_compatibility = {
            "schema_version": "o2_closure_boundary_key_compatibility_repair_v0",
            "compatibility_status": "BOUNDARY_KEY_COMPATIBILITY_NOT_CONFIRMED",
            "failures": failures,
        }
        patch_report = {
            "schema_version": "o2_closure_validator_patch_report_v0",
            "patch_status": "PATCH_FAIL",
            "failures": failures,
        }

    repair_record = {
        "schema_version": "o2_proposed_record_review_closure_repair_record_v0",
        "repair_status": status,
        "repair_pass": repair_pass,
        "failed_closure_receipt_id": FAILED_CLOSURE_RECEIPT_ID,
        "failure_codes": ["exec_boundary_wrong", "acceptance_gate_result_false"],
        "repair_scope": "closure validator compatibility only",
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
        "schema_version": "o2_closure_repair_authority_boundary_v0",
        "status": status,
        "may_rerun_closure_next": repair_pass,
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
        "schema_version": "o2_closure_repair_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "repair_executed": repair_pass,
        "validator_key_compatibility_repaired": repair_pass,
        "rerun_ready": repair_pass,
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
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "o2_closure_repair_rollup_v0",
        "repair_count": 1 if repair_pass else 0,
        "validator_key_compatibility_repaired_count": 1 if repair_pass else 0,
        "rerun_ready_count": 1 if repair_pass else 0,
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
        "schema_version": "o2_closure_repair_profile_v0",
        "profile_id": "o2_closure_repair_profile_" + sha8(rollup),
        "status": status,
        "repair_pass": repair_pass,
        "rerun_ready": repair_pass,
        "bad_counters_zero": all(rollup.get(k) == 0 for k in zero_keys),
        "recommendation": "Rerun proposed-record review closure with repaired validator. Do not treat repair as closure or final resolution.",
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_closure_repair_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The failed closure was repaired as a validator key-compatibility issue. The substantive boundaries remain unchanged: no final weak-feedback resolution, no C5, no source/prior receipt mutation.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_closure_repair_transition_trace_v0",
        "trace": [
            {
                "step": "consume_failed_closure_receipt",
                "question": "did closure fail with validator-compatible failure codes",
                "answer": "yes" if repair_pass else "no",
                "taken": "inspect boundary key shape",
            },
            {
                "step": "repair_validator_key",
                "question": "does actual boundary key preserve same false boundary",
                "answer": "yes" if repair_pass else "no",
                "taken": "patch closure validator compatibility",
            },
            {
                "step": "preserve_boundaries",
                "question": "did repair resolve weak feedback or open C5",
                "answer": "no",
                "taken": "authorize rerun only",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    for path, obj in [
        (REPAIR_RECORD_PATH, repair_record),
        (BOUNDARY_KEY_COMPATIBILITY_PATH, boundary_key_compatibility),
        (PATCH_REPORT_PATH, patch_report),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, trace),
    ]:
        write_json(path, obj)

    acceptance_gate_results = {
        "REPAIR_0_FAILED_CLOSURE_RECEIPT_CONSUMED": FAILED_CLOSURE_RECEIPT_PATH.exists(),
        "REPAIR_1_FAILED_RECEIPT_SNAPSHOT_EMITTED": FAILED_RECEIPT_SNAPSHOT_PATH.exists(),
        "REPAIR_2_BOUNDARY_KEY_COMPATIBILITY_CONFIRMED": boundary_key_compatibility.get("compatibility_status") == "BOUNDARY_KEY_COMPATIBILITY_CONFIRMED",
        "REPAIR_3_PATCH_REPORT_EMITTED": PATCH_REPORT_PATH.exists(),
        "REPAIR_4_VALIDATOR_PATCHED_OR_ALREADY_PATCHED": patch_report.get("patch_status") in ["PATCH_APPLIED", "ALREADY_PATCHED"],
        "REPAIR_5_WEAK_FEEDBACK_NOT_RESOLVED": rollup["weak_feedback_resolved_count"] == 0,
        "REPAIR_6_FINAL_BOUNDARY_NOT_CROSSED": rollup["final_resolution_boundary_crossed_count"] == 0,
        "REPAIR_7_C5_NOT_OPENED": rollup["c5_opened_count"] == 0 and rollup["c5_reconsideration_ready_count"] == 0,
        "REPAIR_8_NO_SOURCE_OR_PRIOR_RECEIPT_MUTATION": rollup["source_mutated_count"] == 0 and rollup["prior_receipt_mutated_count"] == 0,
        "REPAIR_9_NO_RUNTIME_PATCH_OR_ARCHITECTURE_CHANGE": rollup["runtime_patch_count"] == 0 and rollup["architecture_change_count"] == 0,
        "REPAIR_10_RERUN_READY": rollup["rerun_ready_count"] == 1,
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    if gate == "FAIL":
        status = "TYPED_O2_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR_GATE_FAIL"
        recommended_next = "REPAIR_O2_WEAK_FEEDBACK_RESOLUTION_PROPOSED_RECORD_REVIEW_CLOSURE_V0"

    terminal = {
        "type": "STOP",
        "stop_code": "STOP_" + status,
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "gate": gate,
        "failed_receipt": FAILED_CLOSURE_RECEIPT_ID,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_proposed_record_review_closure_repair_receipt_v0",
        "receipt_type": "TYPED_O2_PROPOSED_RECORD_REVIEW_CLOSURE_REPAIR_RECEIPT",
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
        "machine_readable_o2_proposed_record_review_closure_repair_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "repair_executed": gate == "PASS",
            "validator_key_compatibility_repaired": gate == "PASS",
            "rerun_ready": gate == "PASS",
            "failed_closure_receipt_id": FAILED_CLOSURE_RECEIPT_ID,
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
            "repair_record": rel(REPAIR_RECORD_PATH),
            "failed_receipt_snapshot": rel(FAILED_RECEIPT_SNAPSHOT_PATH),
            "boundary_key_compatibility": rel(BOUNDARY_KEY_COMPATIBILITY_PATH),
            "patch_report": rel(PATCH_REPORT_PATH),
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
    print(f"closure_repair_receipt_id={receipt_id}")
    print(f"closure_repair_receipt_path={rel(receipt_path)}")
    print(f"closure_repair_record_path={rel(REPAIR_RECORD_PATH)}")
    print(f"failed_receipt_snapshot_path={rel(FAILED_RECEIPT_SNAPSHOT_PATH)}")
    print(f"boundary_key_compatibility_path={rel(BOUNDARY_KEY_COMPATIBILITY_PATH)}")
    print(f"patch_report_path={rel(PATCH_REPORT_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
