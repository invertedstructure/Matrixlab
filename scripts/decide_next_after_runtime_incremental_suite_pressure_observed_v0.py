#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_RUNTIME_INCREMENTAL_SUITE_PRESSURE_OBSERVED_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.incremental_suite.post_pressure_decision_v0"
NEXT_UNIT_ID = "AUDIT_RUNTIME_NO_APPLICABLE_MOVE_PRESSURE_CANDIDATE_V0"

LAYER = "OUTER / RUNTIME_ADOPTION / POST_SUITE_DECISION"
MODE = "DECISION_ONLY / PRESSURE_OBSERVED / NO_REPAIR"
BUILD_MODE = "DECIDE_FROM_INCREMENTAL_SUITE_RECEIPT_ONLY"

SOURCE_RECEIPT_ID = "5b62e42f"

SUITE_RECEIPT_PATH = ROOT / "data/runtime_incremental_test_suite_v0_receipts/5b62e42f.json"
CANDIDATES_PATH = ROOT / "data/runtime_incremental_test_suite_v0/runtime_suite_refinement_candidates_v0.jsonl"
ROLLUP_PATH = ROOT / "data/runtime_incremental_test_suite_v0/runtime_incremental_suite_rollup_v0.json"
PROFILE_PATH = ROOT / "data/runtime_incremental_test_suite_v0/runtime_incremental_suite_profile_v0.json"
REPORT_PATH = ROOT / "data/runtime_incremental_test_suite_v0/runtime_incremental_suite_report.json"
CASE_RESULTS_PATH = ROOT / "data/runtime_incremental_test_suite_v0/runtime_case_results_v0.jsonl"
CASE_MANIFEST_PATH = ROOT / "data/runtime_incremental_test_suite_v0/runtime_test_case_manifest_v0.jsonl"

OUT_DIR = ROOT / "data/runtime_incremental_suite_decision_v0"
RECEIPT_DIR = ROOT / "data/runtime_incremental_suite_decision_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_incremental_suite_pressure_decision_basis_v0.json"
DECISION_PATH = OUT_DIR / "runtime_incremental_suite_pressure_decision_v0.json"
PRESSURE_INDEX_PATH = OUT_DIR / "runtime_incremental_suite_pressure_candidate_index_v0.json"
NEXT_TARGET_PATH = OUT_DIR / "runtime_no_applicable_move_pressure_audit_target_v0.json"
ROLLUP_OUT_PATH = OUT_DIR / "runtime_incremental_suite_pressure_decision_rollup_v0.json"
PROFILE_OUT_PATH = OUT_DIR / "runtime_incremental_suite_pressure_decision_profile_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_incremental_suite_pressure_decision_transition_trace.json"

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    text = path.read_text().strip()
    return [json.loads(line) for line in text.splitlines() if line.strip()] if text else []

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def require_false(obj: Dict[str, Any], key: str, failures: List[str]) -> None:
    if obj.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{obj.get(key)}")

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        SUITE_RECEIPT_PATH,
        CANDIDATES_PATH,
        ROLLUP_PATH,
        PROFILE_PATH,
        REPORT_PATH,
        CASE_RESULTS_PATH,
        CASE_MANIFEST_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    suite_receipt = read_json(SUITE_RECEIPT_PATH)
    suite_summary = suite_receipt.get("machine_readable_incremental_suite_summary", {})
    candidates = read_jsonl(CANDIDATES_PATH)
    rollup = read_json(ROLLUP_PATH)
    profile = read_json(PROFILE_PATH)
    report = read_json(REPORT_PATH)
    case_results = read_jsonl(CASE_RESULTS_PATH)
    manifest = read_jsonl(CASE_MANIFEST_PATH)

    if suite_receipt.get("receipt_id") != SOURCE_RECEIPT_ID:
        failures.append(f"suite_receipt_id_wrong:{suite_receipt.get('receipt_id')}")
    if suite_receipt.get("gate") != "PASS":
        failures.append("suite_gate_not_pass")
    if suite_summary.get("suite_stop_code") != "STOP_RUNTIME_INCREMENTAL_SUITE_PRESSURE_OBSERVED":
        failures.append(f"suite_stop_code_wrong:{suite_summary.get('suite_stop_code')}")
    if suite_summary.get("refinement_candidates_emitted") != 1:
        failures.append(f"expected_one_candidate_wrong:{suite_summary.get('refinement_candidates_emitted')}")
    if suite_summary.get("next_unit_id") is not None:
        failures.append("suite_next_unit_should_be_none")
    if suite_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append("suite_terminal_not_stop")
    if suite_receipt.get("terminal", {}).get("next_unit_id") is not None:
        failures.append("suite_terminal_next_should_be_none")

    for key in [
        "ready_for_live_runtime_adoption",
        "runtime_adoption_authorized",
        "runtime_patched",
        "live_runtime_hooks_installed",
        "schema_archive_mutated",
        "schema_created",
        "taxonomy_created",
        "fixture_expanded_by_default",
        "architecture_widened",
        "forbidden_action_applied",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(suite_summary, key, failures)

    if len(candidates) != 1:
        failures.append(f"candidate_count_wrong:{len(candidates)}")

    candidate = candidates[0] if candidates else {}
    pressure_class = candidate.get("pressure_class")
    if pressure_class != "NO_APPLICABLE_MOVE":
        failures.append(f"candidate_pressure_wrong:{pressure_class}")
    if candidate.get("candidate_only") is not True:
        failures.append("candidate_not_candidate_only")
    if candidate.get("repair_applied") is not False:
        failures.append("candidate_repair_applied_not_false")

    blocked_cases = [r for r in case_results if r.get("pressure_class") != "STOP_DONE"]
    if len(blocked_cases) != 1:
        failures.append(f"blocked_case_count_wrong:{len(blocked_cases)}")
    elif blocked_cases[0].get("pressure_class") != "NO_APPLICABLE_MOVE":
        failures.append(f"blocked_case_pressure_wrong:{blocked_cases[0].get('pressure_class')}")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_RUNTIME_INCREMENTAL_SUITE_PRESSURE_DECISION_READY_NO_APPLICABLE_MOVE_AUDIT_NEXT" if gate == "PASS" else "TYPED_RUNTIME_INCREMENTAL_SUITE_PRESSURE_DECISION_GATE_FAIL"

    pressure_index = {
        "schema_version": "runtime_incremental_suite_pressure_candidate_index_v0",
        "index_status": "EMITTED" if gate == "PASS" else "PARTIAL",
        "source_suite_receipt_ref": rel(SUITE_RECEIPT_PATH),
        "candidate_count": len(candidates),
        "pressure_classes": sorted({c.get("pressure_class") for c in candidates}),
        "candidates": candidates,
        "blocked_cases": blocked_cases,
        "classification": {
            "NO_APPLICABLE_MOVE": {
                "candidate_count": sum(1 for c in candidates if c.get("pressure_class") == "NO_APPLICABLE_MOVE"),
                "decision": "AUDIT_CANDIDATE_BEFORE_REPAIR",
                "reason": "The suite intentionally declared a no-applicable-move pressure probe. It must be inspected before deciding whether this is real missing move pressure or negative coverage.",
            }
        },
    }

    decision = {
        "schema_version": "runtime_incremental_suite_pressure_decision_v0",
        "decision_status": status,
        "source_suite_receipt_ref": rel(SUITE_RECEIPT_PATH),
        "source_candidate_index_ref": rel(PRESSURE_INDEX_PATH),
        "decision": "OPEN_NO_APPLICABLE_MOVE_PRESSURE_AUDIT" if gate == "PASS" else "STOP_GATE_FAIL",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "decision_law": "Pressure observed does not authorize repair directly. First inspect whether the candidate is a real missing move, expected negative coverage, or underdeclared case construction.",
        "not_authorized": [
            "repair",
            "move addition",
            "schema creation",
            "taxonomy creation",
            "fixture expansion by default",
            "runtime patching",
            "live hook installation",
            "C8 authorization",
            "live runtime adoption",
        ],
    }

    next_target = {
        "schema_version": "runtime_no_applicable_move_pressure_audit_target_v0",
        "target_status": "NO_APPLICABLE_MOVE_PRESSURE_AUDIT_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "source_candidate_id": candidate.get("candidate_id"),
        "source_case_id": candidate.get("source_case_id"),
        "source_pressure_class": candidate.get("pressure_class"),
        "audit_question": "Is the NO_APPLICABLE_MOVE result a real missing move pressure, expected negative coverage, or an underdeclared probe artifact?",
        "allowed_outputs": [
            "classify as expected negative coverage and close",
            "classify as real missing move pressure and prepare smallest move-design discussion target",
            "classify as underdeclared probe and repair the case contract only",
        ],
        "forbidden_outputs": [
            "add move directly",
            "patch runtime directly",
            "invent schema directly",
            "expand fixture by default",
            "authorize live runtime adoption",
            "authorize C8",
        ],
    }

    basis = {
        "schema_version": "runtime_incremental_suite_pressure_decision_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_incremental_suite_receipt_id": SOURCE_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "Incremental suite passed with one expected-pressure candidate and no next unit; a human-declared decision unit chooses the next audit target.",
        "does_not_authorize": [
            "repair",
            "move addition",
            "schema creation",
            "taxonomy creation",
            "fixture expansion by default",
            "runtime patching",
            "live hook installation",
            "C8 authorization",
        ],
    }

    rollup_out = {
        "schema_version": "runtime_incremental_suite_pressure_decision_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "source_suite_receipt_id": SOURCE_RECEIPT_ID,
        "candidate_count": len(candidates),
        "no_applicable_move_candidate_count": sum(1 for c in candidates if c.get("pressure_class") == "NO_APPLICABLE_MOVE"),
        "decision": decision["decision"],
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "ready_for_no_applicable_move_pressure_audit": gate == "PASS",
        "ready_for_live_runtime_adoption": False,
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "schema_created": False,
        "taxonomy_created": False,
        "fixture_expanded_by_default": False,
        "architecture_widened": False,
        "repair_authorized": False,
        "move_addition_authorized": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    profile_out = {
        "schema_version": "runtime_incremental_suite_pressure_decision_profile_v0",
        "profile_status": status,
        "core_rule": "A pressure candidate triggers inspection, not repair.",
        "source_suite_receipt_ref": rel(SUITE_RECEIPT_PATH),
        "pressure_index_ref": rel(PRESSURE_INDEX_PATH),
        "decision_ref": rel(DECISION_PATH),
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_RUNTIME_INCREMENTAL_SUITE_PRESSURE_DECISION_V0",
        "must_not_infer": [
            "NO_APPLICABLE_MOVE is automatically a missing move",
            "NO_APPLICABLE_MOVE authorizes move creation",
            "expected pressure authorizes repair",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    trace_out = {
        "schema_version": "runtime_incremental_suite_pressure_decision_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "STOP_RUNTIME_INCREMENTAL_SUITE_PRESSURE_OBSERVED",
                "edge": "consume suite receipt and candidate-only pressure",
                "to": "PRESSURE_CANDIDATE_INDEXED" if gate == "PASS" else "PRESSURE_DECISION_GATE_FAIL",
            },
            {
                "from": "PRESSURE_CANDIDATE_INDEXED" if gate == "PASS" else "PRESSURE_DECISION_GATE_FAIL",
                "edge": "select smallest lawful inspection target",
                "to": "NO_APPLICABLE_MOVE_PRESSURE_AUDIT_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_RUNTIME_INCREMENTAL_SUITE_PRESSURE_DECISION_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (PRESSURE_INDEX_PATH, pressure_index),
        (DECISION_PATH, decision),
        (NEXT_TARGET_PATH, next_target),
        (ROLLUP_OUT_PATH, rollup_out),
        (PROFILE_OUT_PATH, profile_out),
        (TRACE_OUT_PATH, trace_out),
    ]:
        write_json(path, obj)

    reason_codes = [
        "INCREMENTAL_SUITE_RECEIPT_CONSUMED",
        "PRESSURE_CANDIDATE_INDEXED",
        "NO_APPLICABLE_MOVE_CANDIDATE_FOUND",
        "REPAIR_NOT_AUTHORIZED_DIRECTLY",
        "NO_APPLICABLE_MOVE_PRESSURE_AUDIT_NEXT",
        "NO_MOVE_ADDITION",
        "NO_SCHEMA_INVENTION",
        "NO_TAXONOMY_INVENTION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_HOOK_INSTALL",
        "NO_LIVE_RUNTIME_ADOPTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_incremental_suite_pressure_decision_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_INCREMENTAL_SUITE_PRESSURE_DECISION_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "source_incremental_suite_receipt_id": SOURCE_RECEIPT_ID,
        "acceptance_gate_results": {
            "PRESSURE_DECISION_0_SUITE_RECEIPT_CONSUMED": gate == "PASS",
            "PRESSURE_DECISION_1_CANDIDATES_CONSUMED": gate == "PASS",
            "PRESSURE_DECISION_2_ONE_NO_APPLICABLE_MOVE_CANDIDATE_FOUND": gate == "PASS",
            "PRESSURE_DECISION_3_NO_DIRECT_REPAIR": gate == "PASS",
            "PRESSURE_DECISION_4_AUDIT_TARGET_EMITTED": gate == "PASS",
            "PRESSURE_DECISION_5_NO_MOVE_ADDITION": gate == "PASS",
            "PRESSURE_DECISION_6_NO_RUNTIME_PATCH": gate == "PASS",
            "PRESSURE_DECISION_7_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_pressure_decision_summary": {
            "status": status,
            "decision_done": gate == "PASS",
            "candidate_count": len(candidates),
            "pressure_class": "NO_APPLICABLE_MOVE" if gate == "PASS" else None,
            "decision": decision["decision"],
            "ready_for_no_applicable_move_pressure_audit": gate == "PASS",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "ready_for_live_runtime_adoption": False,
            "runtime_adoption_authorized": False,
            "runtime_patched": False,
            "live_runtime_hooks_installed": False,
            "schema_archive_mutated": False,
            "schema_created": False,
            "taxonomy_created": False,
            "fixture_expanded_by_default": False,
            "architecture_widened": False,
            "repair_authorized": False,
            "move_addition_authorized": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "pressure_candidate_index": rel(PRESSURE_INDEX_PATH),
            "decision": rel(DECISION_PATH),
            "next_target": rel(NEXT_TARGET_PATH),
            "rollup": rel(ROLLUP_OUT_PATH),
            "profile": rel(PROFILE_OUT_PATH),
            "transition_trace": rel(TRACE_OUT_PATH),
        },
        "terminal": trace_out["terminal"],
    }

    receipt_id = sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_pressure_decision_receipt_id={receipt_id}")
    print(f"runtime_pressure_decision_receipt_path={rel(receipt_path)}")
    print(f"runtime_pressure_decision_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
