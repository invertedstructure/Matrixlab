#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "DECIDE_NEXT_AFTER_RUNTIME_DEFERRED_PRESSURE_TEST_SUITE_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.deferred_pressure_suite_decision_v0"

SOURCE_SUITE_RECEIPT_ID = "be061c52"

SUITE_RECEIPT_PATH = ROOT / "data/runtime_deferred_pressure_test_suite_v0_receipts/be061c52.json"
SUITE_MANIFEST_PATH = ROOT / "data/runtime_deferred_pressure_test_suite_v0/runtime_deferred_pressure_suite_manifest_v0.json"
SUITE_ROLLUP_PATH = ROOT / "data/runtime_deferred_pressure_test_suite_v0/runtime_deferred_pressure_suite_rollup_v0.json"
SUITE_PROFILE_PATH = ROOT / "data/runtime_deferred_pressure_test_suite_v0/runtime_deferred_pressure_suite_profile_v0.json"
SUITE_CASE_RECEIPT_INDEX_PATH = ROOT / "data/runtime_deferred_pressure_test_suite_v0/runtime_deferred_pressure_suite_case_receipt_index_v0.json"
SUITE_DECISION_TARGET_PATH = ROOT / "data/runtime_deferred_pressure_test_suite_v0/runtime_deferred_pressure_suite_decision_target_v0.json"

T6_TIE_AUDIT_RECEIPT_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0_receipts/eb20d76b.json"
T6_TIE_CLASSIFICATION_PATH = ROOT / "data/runtime_deferred_cases_t6_move_tie_surface_audit_v0/runtime_t6_move_tie_surface_classification_v0.json"

OUT_DIR = ROOT / "data/runtime_deferred_pressure_suite_decision_v0"
RECEIPT_DIR = ROOT / "data/runtime_deferred_pressure_suite_decision_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_deferred_pressure_suite_decision_basis_v0.json"
CANDIDATE_CLASSIFICATION_PATH = OUT_DIR / "runtime_deferred_pressure_suite_candidate_classification_v0.json"
CLOSURE_PATH = OUT_DIR / "runtime_deferred_pressure_suite_closure_v0.json"
T6_PRESERVATION_PATH = OUT_DIR / "runtime_t6_later_objective_preservation_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_deferred_pressure_suite_decision_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_deferred_pressure_suite_decision_profile_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_deferred_pressure_suite_decision_transition_trace.json"

READY_CASES = [
    "T3.schema_validation_failure",
    "T3.admissibility_block",
    "T4.full_observability_required_gap",
]

EXCLUDED_CASES = [
    "T6.step_cap_loop_shape",
    "T6.move_tie_unresolved",
]

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
        SUITE_MANIFEST_PATH,
        SUITE_ROLLUP_PATH,
        SUITE_PROFILE_PATH,
        SUITE_CASE_RECEIPT_INDEX_PATH,
        SUITE_DECISION_TARGET_PATH,
        T6_TIE_AUDIT_RECEIPT_PATH,
        T6_TIE_CLASSIFICATION_PATH,
    ]

    failures: List[str] = []
    source_hashes_before = {}

    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")
        else:
            source_hashes_before[rel(p)] = file_sha256(p)

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    suite_receipt = read_json(SUITE_RECEIPT_PATH)
    suite_summary = suite_receipt.get("machine_readable_deferred_pressure_suite_summary", {})
    suite_manifest = read_json(SUITE_MANIFEST_PATH)
    suite_rollup = read_json(SUITE_ROLLUP_PATH)
    suite_profile = read_json(SUITE_PROFILE_PATH)
    case_receipt_index = read_json(SUITE_CASE_RECEIPT_INDEX_PATH)
    decision_target = read_json(SUITE_DECISION_TARGET_PATH)

    t6_receipt = read_json(T6_TIE_AUDIT_RECEIPT_PATH)
    t6_summary = t6_receipt.get("machine_readable_t6_move_tie_surface_audit_summary", {})
    t6_classification = read_json(T6_TIE_CLASSIFICATION_PATH)

    if suite_receipt.get("receipt_id") != SOURCE_SUITE_RECEIPT_ID:
        failures.append(f"suite_receipt_id_wrong:{suite_receipt.get('receipt_id')}")
    if suite_receipt.get("gate") != "PASS":
        failures.append("suite_gate_not_pass")
    if suite_summary.get("deferred_pressure_suite_done") is not True:
        failures.append("suite_not_done")
    if suite_summary.get("status") != "TYPED_RUNTIME_DEFERRED_PRESSURE_TEST_SUITE_PASS_EXPECTED_PRESSURE_OBSERVED":
        failures.append("suite_status_wrong")
    if suite_summary.get("cases_declared") != 3:
        failures.append("cases_declared_not_3")
    if suite_summary.get("cases_run") != 3:
        failures.append("cases_run_not_3")
    if suite_summary.get("cases_passed_expected_terminal") != 3:
        failures.append("cases_passed_not_3")
    if suite_summary.get("cases_typed_stop") != 3:
        failures.append("cases_typed_stop_not_3")
    if suite_summary.get("cases_advance") != 0:
        failures.append("cases_advance_not_0")
    if suite_summary.get("case_receipt_trace_mismatch_count") != 0:
        failures.append("case_receipt_trace_mismatch_not_0")
    if suite_summary.get("ready_cases_run") != READY_CASES:
        failures.append("ready_cases_run_wrong")
    if suite_summary.get("excluded_cases_not_run") != EXCLUDED_CASES:
        failures.append("excluded_cases_not_run_wrong")
    if suite_summary.get("t6_preserved_for_later") is not True:
        failures.append("t6_not_preserved_for_later")
    if suite_summary.get("ready_for_deferred_suite_decision") is not True:
        failures.append("not_ready_for_deferred_suite_decision")
    if suite_summary.get("next_unit_id") != UNIT_ID:
        failures.append(f"suite_next_unit_wrong:{suite_summary.get('next_unit_id')}")

    if suite_receipt.get("terminal", {}).get("type") != "STOP":
        failures.append("suite_terminal_not_stop")
    if suite_receipt.get("terminal", {}).get("stop_code") != "STOP_RUNTIME_DEFERRED_PRESSURE_SUITE_EXPECTED_PRESSURE_OBSERVED":
        failures.append("suite_stop_code_wrong")

    if decision_target.get("next_unit_id") != UNIT_ID:
        failures.append(f"decision_target_next_wrong:{decision_target.get('next_unit_id')}")
    if decision_target.get("source_suite_receipt_ref") != rel(SUITE_RECEIPT_PATH):
        failures.append("decision_target_source_receipt_wrong")

    if case_receipt_index.get("case_receipt_count") != 3:
        failures.append("case_receipt_count_not_3")
    for row in case_receipt_index.get("case_receipts", []):
        if row.get("passed_expected_terminal") is not True:
            failures.append(f"case_not_passed_expected_terminal:{row.get('case_key')}")
        if row.get("case_key") not in READY_CASES:
            failures.append(f"unexpected_case_in_receipt_index:{row.get('case_key')}")

    if t6_summary.get("classification_kind") != "DETECTOR_FALSE_POSITIVE_TEXT_ONLY_TIE_SURFACE":
        failures.append("t6_classification_not_false_positive")
    if t6_summary.get("ready_for_t6_move_tie_contract") is not False:
        failures.append("t6_move_tie_contract_should_not_be_ready")
    if t6_summary.get("loop_trigger_available") is not False:
        failures.append("loop_trigger_should_be_false")
    if t6_summary.get("ready_for_deferred_suite_build") is not True:
        failures.append("t6_summary_not_ready_for_suite_build")

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
        "repair_authorized",
        "move_addition_authorized",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(suite_summary, key, failures)

    gate = "PASS" if not failures else "FAIL"

    candidate_rows = []
    for row in case_receipt_index.get("case_receipts", []):
        candidate_rows.append({
            "case_id": row.get("case_id"),
            "case_key": row.get("case_key"),
            "case_receipt_id": row.get("case_receipt_id"),
            "pressure_class": row.get("pressure_class"),
            "outcome_class": row.get("outcome_class"),
            "classification": "EXPECTED_NEGATIVE_COVERAGE",
            "candidate_closed": gate == "PASS",
            "real_repair_pressure": False,
            "real_move_addition_pressure": False,
            "real_runtime_patch_pressure": False,
            "lawful_handling": "close as expected-pressure coverage; do not repair",
        })

    decision_kind = "CLOSE_DEFERRED_PRESSURE_SUITE_AS_EXPECTED_PRESSURE_COVERAGE" if gate == "PASS" else "DEFERRED_PRESSURE_SUITE_DECISION_GATE_FAIL"
    status = "TYPED_RUNTIME_DEFERRED_PRESSURE_SUITE_DECISION_CLOSED_EXPECTED_PRESSURE_COVERAGE" if gate == "PASS" else "TYPED_RUNTIME_DEFERRED_PRESSURE_SUITE_DECISION_GATE_FAIL"

    candidate_classification = {
        "schema_version": "runtime_deferred_pressure_suite_candidate_classification_v0",
        "classification_status": status,
        "source_suite_receipt_ref": rel(SUITE_RECEIPT_PATH),
        "candidate_count": len(candidate_rows) if gate == "PASS" else 0,
        "closed_expected_negative_coverage_count": len(candidate_rows) if gate == "PASS" else 0,
        "real_repair_pressure_count": 0,
        "real_move_addition_pressure_count": 0,
        "real_runtime_patch_pressure_count": 0,
        "candidates": candidate_rows if gate == "PASS" else [],
        "decision_law": "Expected pressure observed by a declared negative case is not repair pressure.",
    }

    closure = {
        "schema_version": "runtime_deferred_pressure_suite_closure_v0",
        "closure_status": "CLOSED_EXPECTED_PRESSURE_COVERAGE" if gate == "PASS" else "NOT_CLOSED",
        "decision_kind": decision_kind,
        "source_suite_receipt_id": SOURCE_SUITE_RECEIPT_ID,
        "suite_id": suite_summary.get("suite_id"),
        "closed_cases": READY_CASES if gate == "PASS" else [],
        "excluded_cases_preserved_for_later": EXCLUDED_CASES if gate == "PASS" else [],
        "branch_closed": gate == "PASS",
        "next_unit_id": None,
        "ready_for_live_runtime_adoption": False,
        "runtime_adoption_authorized": False,
        "repair_authorized": False,
        "move_addition_authorized": False,
        "runtime_patch_authorized": False,
        "c8_authorized": False,
        "reading": "The deferred pressure suite did what it was designed to do: it observed typed expected pressure for the declared T3/T4 negative cases.",
    }

    t6_preservation = {
        "schema_version": "runtime_t6_later_objective_preservation_v0",
        "preservation_status": "PRESERVED_FOR_LATER_OBJECTIVE" if gate == "PASS" else "NOT_READY",
        "source_t6_audit_receipt_ref": rel(T6_TIE_AUDIT_RECEIPT_PATH),
        "t6_cases": EXCLUDED_CASES,
        "current_reading": {
            "T6.step_cap_loop_shape": "no current loop trigger surface",
            "T6.move_tie_unresolved": "prior tie hit classified as detector false positive / text-only, no structured tie candidate",
        },
        "later_objective_rule": "Open T6 later only as a new bounded registry/trigger objective, not as continuation pressure from this closed deferred suite.",
        "does_not_authorize_now": [
            "T6 case contract",
            "loop trigger invention",
            "move tie invention",
            "move addition",
            "runtime patching",
            "fixture expansion by default",
        ],
    }

    basis = {
        "schema_version": "runtime_deferred_pressure_suite_decision_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_suite_receipt_id": SOURCE_SUITE_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "The deferred pressure suite passed all expected-pressure cases and emitted no mismatch; decision may close the branch as expected negative coverage.",
        "does_not_authorize": [
            "runtime repair",
            "move addition",
            "fixture expansion by default",
            "runtime patching",
            "live runtime adoption",
            "C8 authorization",
            "T6 work inside this closed branch",
        ],
    }

    rollup = {
        "schema_version": "runtime_deferred_pressure_suite_decision_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "decision_kind": decision_kind,
        "suite_id": suite_summary.get("suite_id"),
        "branch_closed": gate == "PASS",
        "closed_case_count": 3 if gate == "PASS" else 0,
        "candidate_count": len(candidate_rows) if gate == "PASS" else 0,
        "closed_expected_negative_coverage_count": len(candidate_rows) if gate == "PASS" else 0,
        "real_repair_pressure_count": 0,
        "real_move_addition_pressure_count": 0,
        "real_runtime_patch_pressure_count": 0,
        "t6_preserved_for_later": gate == "PASS",
        "next_unit_id": None,
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

    profile = {
        "schema_version": "runtime_deferred_pressure_suite_decision_profile_v0",
        "profile_status": status,
        "decision_kind": decision_kind,
        "core_rule": "Expected pressure is coverage when it matches declared negative-case contracts; it is not automatically repair pressure.",
        "candidate_classification_ref": rel(CANDIDATE_CLASSIFICATION_PATH),
        "closure_ref": rel(CLOSURE_PATH),
        "t6_preservation_ref": rel(T6_PRESERVATION_PATH),
        "recommended_next": None,
        "must_not_infer": [
            "runtime should be repaired",
            "moves should be added",
            "live runtime adoption is authorized",
            "C8 is authorized",
            "T6 is solved",
            "T6 should never be revisited",
        ],
    }

    trace = {
        "schema_version": "runtime_deferred_pressure_suite_decision_transition_trace_v0",
        "unit_id": UNIT_ID,
        "suite_id": suite_summary.get("suite_id"),
        "transitions": [
            {
                "from": "DEFERRED_PRESSURE_SUITE_EXPECTED_PRESSURE_OBSERVED",
                "edge": "classify case candidates",
                "to": "EXPECTED_PRESSURE_CANDIDATES_CLOSED_AS_COVERAGE" if gate == "PASS" else "DEFERRED_PRESSURE_SUITE_DECISION_GATE_FAIL",
            },
            {
                "from": "EXPECTED_PRESSURE_CANDIDATES_CLOSED_AS_COVERAGE" if gate == "PASS" else "DEFERRED_PRESSURE_SUITE_DECISION_GATE_FAIL",
                "edge": "close deferred pressure branch and preserve T6 for later",
                "to": "STOP_DEFERRED_PRESSURE_SUITE_BRANCH_COMPLETE" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "STOP",
            "next_unit_id": None,
            "stop_code": (
                "STOP_RUNTIME_DEFERRED_PRESSURE_SUITE_BRANCH_COMPLETE"
                if gate == "PASS"
                else "STOP_RUNTIME_DEFERRED_PRESSURE_SUITE_DECISION_GATE_FAIL"
            ),
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (CANDIDATE_CLASSIFICATION_PATH, candidate_classification),
        (CLOSURE_PATH, closure),
        (T6_PRESERVATION_PATH, t6_preservation),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_OUT_PATH, trace),
    ]:
        write_json(path, obj)

    source_hashes_after = {rel(p): file_sha256(p) for p in required}
    source_mutated = source_hashes_before != source_hashes_after
    if source_mutated:
        gate = "FAIL"
        status = "TYPED_RUNTIME_DEFERRED_PRESSURE_SUITE_DECISION_SOURCE_MUTATION_FAIL"
        failures.append("source_inputs_mutated")

    reason_codes = [
        "DEFERRED_PRESSURE_SUITE_RECEIPT_CONSUMED",
        "ALL_CASES_ALREADY_PASSED_EXPECTED_PRESSURE",
        "EXPECTED_PRESSURE_CLASSIFIED_AS_COVERAGE",
        "CANDIDATES_CLOSED_AS_EXPECTED_NEGATIVE_COVERAGE",
        "NO_REPAIR_PRESSURE",
        "NO_MOVE_ADDITION_PRESSURE",
        "NO_RUNTIME_PATCH_PRESSURE",
        "T6_PRESERVED_FOR_LATER_OBJECTIVE",
        "BRANCH_CLOSED",
        "NO_LIVE_RUNTIME_ADOPTION",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_deferred_pressure_suite_decision_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_DEFERRED_PRESSURE_SUITE_DECISION_RECEIPT",
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": "OUTER / RUNTIME_ADOPTION / DEFERRED_PRESSURE_SUITE / DECISION",
        "mode": "DECIDE_ONLY / EXPECTED_PRESSURE_COVERAGE_CLOSURE / NO_TEST_RUN",
        "build_mode": "DEFERRED_PRESSURE_SUITE_DECISION_ONLY",
        "gate": gate,
        "status": status,
        "failures": failures,
        "warnings": [],
        "source_suite_receipt_id": SOURCE_SUITE_RECEIPT_ID,
        "acceptance_gate_results": {
            "DPSD_0_SUITE_RECEIPT_CONSUMED": gate == "PASS",
            "DPSD_1_ALL_CASES_PASSED_EXPECTED_PRESSURE": gate == "PASS",
            "DPSD_2_CANDIDATES_CLASSIFIED": gate == "PASS",
            "DPSD_3_EXPECTED_PRESSURE_CLOSED_AS_COVERAGE": gate == "PASS",
            "DPSD_4_T6_PRESERVED_FOR_LATER": gate == "PASS",
            "DPSD_5_NO_REPAIR": gate == "PASS",
            "DPSD_6_NO_MOVE_ADDITION": gate == "PASS",
            "DPSD_7_NO_RUNTIME_PATCH": gate == "PASS",
            "DPSD_8_SOURCE_INPUTS_NOT_MUTATED": not source_mutated,
            "DPSD_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_deferred_pressure_suite_decision_summary": {
            "status": status,
            "decision_kind": decision_kind,
            "suite_id": suite_summary.get("suite_id"),
            "branch_closed": gate == "PASS",
            "closed_case_count": 3 if gate == "PASS" else 0,
            "candidate_count": len(candidate_rows) if gate == "PASS" else 0,
            "closed_expected_negative_coverage_count": len(candidate_rows) if gate == "PASS" else 0,
            "real_repair_pressure_count": 0,
            "real_move_addition_pressure_count": 0,
            "real_runtime_patch_pressure_count": 0,
            "t6_preserved_for_later": gate == "PASS",
            "next_unit_id": None,
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
            "candidate_classification": rel(CANDIDATE_CLASSIFICATION_PATH),
            "closure": rel(CLOSURE_PATH),
            "t6_preservation": rel(T6_PRESERVATION_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "transition_trace": rel(TRACE_OUT_PATH),
        },
        "terminal": trace["terminal"],
    }

    receipt_id = sig8(receipt)
    receipt["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_deferred_pressure_suite_decision_receipt_id={receipt_id}")
    print(f"runtime_deferred_pressure_suite_decision_receipt_path={rel(receipt_path)}")
    print(f"runtime_deferred_pressure_suite_decision_next_unit={receipt['machine_readable_deferred_pressure_suite_decision_summary']['next_unit_id'] or 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
