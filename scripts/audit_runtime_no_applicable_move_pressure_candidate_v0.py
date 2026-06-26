#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "AUDIT_RUNTIME_NO_APPLICABLE_MOVE_PRESSURE_CANDIDATE_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.incremental_suite.no_applicable_move_pressure_audit_v0"

LAYER = "OUTER / RUNTIME_ADOPTION / PRESSURE_AUDIT"
MODE = "AUDIT_ONLY / NO_APPLICABLE_MOVE / NO_REPAIR"
BUILD_MODE = "CLASSIFY_PRESSURE_CANDIDATE_ONLY"

SOURCE_DECISION_RECEIPT_ID = "15f638e8"
SOURCE_SUITE_RECEIPT_ID = "5b62e42f"

DECISION_RECEIPT_PATH = ROOT / "data/runtime_incremental_suite_decision_v0_receipts/15f638e8.json"
DECISION_PATH = ROOT / "data/runtime_incremental_suite_decision_v0/runtime_incremental_suite_pressure_decision_v0.json"
CANDIDATE_INDEX_PATH = ROOT / "data/runtime_incremental_suite_decision_v0/runtime_incremental_suite_pressure_candidate_index_v0.json"
AUDIT_TARGET_PATH = ROOT / "data/runtime_incremental_suite_decision_v0/runtime_no_applicable_move_pressure_audit_target_v0.json"

SUITE_RECEIPT_PATH = ROOT / "data/runtime_incremental_test_suite_v0_receipts/5b62e42f.json"
SUITE_CANDIDATES_PATH = ROOT / "data/runtime_incremental_test_suite_v0/runtime_suite_refinement_candidates_v0.jsonl"
SUITE_CASE_RESULTS_PATH = ROOT / "data/runtime_incremental_test_suite_v0/runtime_case_results_v0.jsonl"
SUITE_MANIFEST_PATH = ROOT / "data/runtime_incremental_test_suite_v0/runtime_test_case_manifest_v0.jsonl"
SUITE_STATE_SET_PATH = ROOT / "data/runtime_incremental_test_suite_v0/runtime_declared_state_set_v0.json"
SUITE_ROLLUP_PATH = ROOT / "data/runtime_incremental_test_suite_v0/runtime_incremental_suite_rollup_v0.json"

EXPECTED_PRESSURE_CONTRACT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_expected_pressure_case_contract_v0.json"
ALLOWED_EXPECTED_PRESSURE_CASES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_expected_pressure_cases_v0.json"
STATE_VARIANT_RULES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_declared_state_variant_rules_v0.json"
ALLOWED_STATE_VARIANTS_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_state_variant_catalog_v0.json"
REACHABILITY_MAP_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_registry_reachability_map_v0.json"
BRANCH_GAP_INDEX_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_branch_gap_index_v0.json"
SMOKE_REGISTRY_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_move_registry_snapshot_v0.json"

OUT_DIR = ROOT / "data/runtime_no_applicable_move_pressure_audit_v0"
RECEIPT_DIR = ROOT / "data/runtime_no_applicable_move_pressure_audit_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_no_applicable_move_pressure_audit_basis_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "runtime_no_applicable_move_pressure_classification_v0.json"
EVIDENCE_PATH = OUT_DIR / "runtime_no_applicable_move_pressure_evidence_v0.json"
CLOSURE_PATH = OUT_DIR / "runtime_no_applicable_move_pressure_candidate_closure_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_no_applicable_move_pressure_audit_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_no_applicable_move_pressure_audit_profile_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_no_applicable_move_pressure_audit_transition_trace.json"

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

def find_one(rows: List[Dict[str, Any]], key: str, value: Any) -> Dict[str, Any]:
    matches = [r for r in rows if r.get(key) == value]
    if len(matches) != 1:
        raise RuntimeError(f"expected one row where {key}={value}, found {len(matches)}")
    return matches[0]

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        DECISION_RECEIPT_PATH,
        DECISION_PATH,
        CANDIDATE_INDEX_PATH,
        AUDIT_TARGET_PATH,
        SUITE_RECEIPT_PATH,
        SUITE_CANDIDATES_PATH,
        SUITE_CASE_RESULTS_PATH,
        SUITE_MANIFEST_PATH,
        SUITE_STATE_SET_PATH,
        SUITE_ROLLUP_PATH,
        EXPECTED_PRESSURE_CONTRACT_PATH,
        ALLOWED_EXPECTED_PRESSURE_CASES_PATH,
        STATE_VARIANT_RULES_PATH,
        ALLOWED_STATE_VARIANTS_PATH,
        REACHABILITY_MAP_PATH,
        BRANCH_GAP_INDEX_PATH,
        SMOKE_REGISTRY_PATH,
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

    decision_receipt = read_json(DECISION_RECEIPT_PATH)
    decision_summary = decision_receipt.get("machine_readable_pressure_decision_summary", {})
    decision = read_json(DECISION_PATH)
    candidate_index = read_json(CANDIDATE_INDEX_PATH)
    audit_target = read_json(AUDIT_TARGET_PATH)

    suite_receipt = read_json(SUITE_RECEIPT_PATH)
    suite_summary = suite_receipt.get("machine_readable_incremental_suite_summary", {})
    candidates = read_jsonl(SUITE_CANDIDATES_PATH)
    case_results = read_jsonl(SUITE_CASE_RESULTS_PATH)
    manifest = read_jsonl(SUITE_MANIFEST_PATH)
    state_set = read_json(SUITE_STATE_SET_PATH)
    suite_rollup = read_json(SUITE_ROLLUP_PATH)

    expected_pressure_contract = read_json(EXPECTED_PRESSURE_CONTRACT_PATH)
    allowed_expected_pressure_cases = read_json(ALLOWED_EXPECTED_PRESSURE_CASES_PATH)
    state_variant_rules = read_json(STATE_VARIANT_RULES_PATH)
    allowed_state_variants = read_json(ALLOWED_STATE_VARIANTS_PATH)
    reachability_map = read_json(REACHABILITY_MAP_PATH)
    branch_gap_index = read_json(BRANCH_GAP_INDEX_PATH)
    smoke_registry = read_json(SMOKE_REGISTRY_PATH)

    if decision_receipt.get("receipt_id") != SOURCE_DECISION_RECEIPT_ID:
        failures.append(f"decision_receipt_id_wrong:{decision_receipt.get('receipt_id')}")
    if decision_receipt.get("gate") != "PASS":
        failures.append("decision_gate_not_pass")
    if decision_summary.get("ready_for_no_applicable_move_pressure_audit") is not True:
        failures.append("decision_not_ready_for_no_applicable_move_audit")
    if decision_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("decision_terminal_not_advance")
    if decision_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("decision_terminal_next_wrong")
    if decision_summary.get("decision") != "OPEN_NO_APPLICABLE_MOVE_PRESSURE_AUDIT":
        failures.append(f"decision_wrong:{decision_summary.get('decision')}")

    if suite_receipt.get("receipt_id") != SOURCE_SUITE_RECEIPT_ID:
        failures.append(f"suite_receipt_id_wrong:{suite_receipt.get('receipt_id')}")
    if suite_receipt.get("gate") != "PASS":
        failures.append("suite_gate_not_pass")
    if suite_summary.get("suite_stop_code") != "STOP_RUNTIME_INCREMENTAL_SUITE_PRESSURE_OBSERVED":
        failures.append(f"suite_stop_code_wrong:{suite_summary.get('suite_stop_code')}")
    if suite_summary.get("refinement_candidates_emitted") != 1:
        failures.append(f"suite_candidate_count_wrong:{suite_summary.get('refinement_candidates_emitted')}")
    if suite_summary.get("next_unit_id") is not None:
        failures.append("suite_next_unit_should_be_none")

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
        if key in decision_summary:
            require_false(decision_summary, key, failures)

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
    candidate_id = candidate.get("candidate_id")
    source_case_id = candidate.get("source_case_id")

    if candidate.get("pressure_class") != "NO_APPLICABLE_MOVE":
        failures.append(f"candidate_pressure_wrong:{candidate.get('pressure_class')}")
    if candidate.get("candidate_only") is not True:
        failures.append("candidate_not_candidate_only")
    if candidate.get("repair_applied") is not False:
        failures.append("candidate_repair_applied_not_false")

    case_result = {}
    manifest_row = {}
    state_row = {}
    if source_case_id:
        try:
            case_result = find_one(case_results, "case_id", source_case_id)
            manifest_row = find_one(manifest, "case_id", source_case_id)
            state_row = find_one(state_set.get("states", []), "case_id", source_case_id)
        except Exception as exc:
            failures.append(str(exc))

    if case_result and case_result.get("pressure_class") != "NO_APPLICABLE_MOVE":
        failures.append(f"case_result_pressure_wrong:{case_result.get('pressure_class')}")
    if case_result and case_result.get("expected_terminal_matched") is not True:
        failures.append("case_result_expected_terminal_not_matched")
    if manifest_row and manifest_row.get("case_role") != "declared_no_applicable_move_pressure":
        failures.append(f"manifest_case_role_wrong:{manifest_row.get('case_role')}")

    allowed_pressure_cases = allowed_expected_pressure_cases.get("cases", [])
    matching_allowed_pressure = [
        c for c in allowed_pressure_cases
        if c.get("case_role") == "declared_no_applicable_move_pressure"
        and c.get("expected_pressure_class") == "NO_APPLICABLE_MOVE"
    ]
    if len(matching_allowed_pressure) != 1:
        failures.append(f"allowed_pressure_contract_match_count_wrong:{len(matching_allowed_pressure)}")

    special_tokens = state_variant_rules.get("special_phase_tokens", [])
    no_applicable_token = [
        t for t in special_tokens
        if t.get("token") == "NO_APPLICABLE_MOVE_PROBE"
        and t.get("status") == "ALLOWED_ONLY_WITH_EXPECTED_PRESSURE_CONTRACT"
    ]
    if len(no_applicable_token) != 1:
        failures.append(f"no_applicable_special_token_count_wrong:{len(no_applicable_token)}")

    allowed_variants = allowed_state_variants.get("variants", [])
    no_applicable_variant = [
        v for v in allowed_variants
        if v.get("variant_id") == "state_variant_no_applicable_move_probe_v0"
        and v.get("requires_expected_pressure_contract") is True
    ]
    if len(no_applicable_variant) != 1:
        failures.append(f"no_applicable_variant_count_wrong:{len(no_applicable_variant)}")

    registry_phases = {
        (move.get("applies_when") or {}).get("runtime_phase")
        for move in smoke_registry.get("moves", [])
        if (move.get("applies_when") or {}).get("runtime_phase")
    }
    token_is_registry_phase = "NO_APPLICABLE_MOVE_PROBE" in registry_phases
    if token_is_registry_phase:
        failures.append("no_applicable_probe_token_unexpectedly_registered_as_real_phase")

    if candidate_index.get("classification", {}).get("NO_APPLICABLE_MOVE", {}).get("decision") != "AUDIT_CANDIDATE_BEFORE_REPAIR":
        failures.append("candidate_index_decision_wrong")

    gate = "PASS" if not failures else "FAIL"

    # Classification law:
    # This specific candidate came from an intentionally declared special probe token,
    # had an expected-pressure contract, matched its expected terminal, and is not a real
    # registered runtime phase. Therefore it is expected negative coverage, not a real
    # missing-move repair pressure.
    classification_kind = "EXPECTED_NEGATIVE_COVERAGE"
    repair_authorized = False
    move_addition_authorized = False
    next_unit_id = None
    terminal_type = "STOP"
    stop_code = "STOP_NO_APPLICABLE_MOVE_PRESSURE_AUDIT_CLOSED_EXPECTED_NEGATIVE_COVERAGE"
    status = "TYPED_NO_APPLICABLE_MOVE_PRESSURE_AUDIT_CLOSED_AS_EXPECTED_NEGATIVE_COVERAGE"

    if gate != "PASS":
        classification_kind = "AUDIT_GATE_FAIL"
        stop_code = "STOP_NO_APPLICABLE_MOVE_PRESSURE_AUDIT_GATE_FAIL"
        status = "TYPED_NO_APPLICABLE_MOVE_PRESSURE_AUDIT_GATE_FAIL"

    evidence = {
        "schema_version": "runtime_no_applicable_move_pressure_evidence_v0",
        "evidence_status": "EMITTED" if gate == "PASS" else "PARTIAL",
        "source_candidate_id": candidate_id,
        "source_case_id": source_case_id,
        "source_case_result": case_result,
        "source_manifest_row": manifest_row,
        "source_state_row": state_row,
        "expected_pressure_contract_match": matching_allowed_pressure[0] if matching_allowed_pressure else None,
        "state_variant_special_token": no_applicable_token[0] if no_applicable_token else None,
        "state_variant_catalog_entry": no_applicable_variant[0] if no_applicable_variant else None,
        "registry_phases": sorted(registry_phases),
        "probe_token_registered_as_real_phase": token_is_registry_phase,
        "evidence_reading": "The NO_APPLICABLE_MOVE case used the special phase token NO_APPLICABLE_MOVE_PROBE, which was allowed only as an expected-pressure probe. It matched the expected terminal and pressure. No real runtime objective requested a missing move.",
    }

    classification = {
        "schema_version": "runtime_no_applicable_move_pressure_classification_v0",
        "classification_status": status,
        "classification_kind": classification_kind,
        "source_candidate_id": candidate_id,
        "source_case_id": source_case_id,
        "pressure_class": "NO_APPLICABLE_MOVE",
        "is_real_missing_move_pressure": False if gate == "PASS" else None,
        "is_expected_negative_coverage": True if gate == "PASS" else None,
        "is_underdeclared_probe_artifact": False if gate == "PASS" else None,
        "repair_authorized": repair_authorized,
        "move_addition_authorized": move_addition_authorized,
        "schema_creation_authorized": False,
        "taxonomy_creation_authorized": False,
        "fixture_expansion_authorized": False,
        "runtime_patch_authorized": False,
        "live_runtime_adoption_authorized": False,
        "c8_authorized": False,
        "decision_law": "A declared no-applicable-move probe that matched its expected-pressure contract is coverage evidence, not repair pressure.",
        "smallest_lawful_next_handling": "close pressure candidate as expected negative coverage" if gate == "PASS" else "repair audit gate inputs",
    }

    closure = {
        "schema_version": "runtime_no_applicable_move_pressure_candidate_closure_v0",
        "closure_status": "CLOSED_EXPECTED_NEGATIVE_COVERAGE" if gate == "PASS" else "NOT_CLOSED",
        "source_candidate_id": candidate_id,
        "source_case_id": source_case_id,
        "candidate_closed": gate == "PASS",
        "closure_reason": "Expected NO_APPLICABLE_MOVE pressure was intentionally declared and matched; no missing runtime move is licensed.",
        "next_unit_id": None,
        "terminal": {
            "type": terminal_type,
            "stop_code": stop_code,
            "next_unit_id": next_unit_id,
        },
    }

    basis = {
        "schema_version": "runtime_no_applicable_move_pressure_audit_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "source_suite_receipt_id": SOURCE_SUITE_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "The post-suite decision opened an audit over the single candidate-only NO_APPLICABLE_MOVE pressure record.",
        "does_not_authorize": [
            "repair",
            "move addition",
            "schema creation",
            "taxonomy creation",
            "fixture expansion by default",
            "runtime patching",
            "live hook installation",
            "live runtime adoption",
            "C8 authorization",
        ],
    }

    rollup = {
        "schema_version": "runtime_no_applicable_move_pressure_audit_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "source_suite_receipt_id": SOURCE_SUITE_RECEIPT_ID,
        "candidate_count": len(candidates),
        "classification_kind": classification_kind,
        "candidate_closed": gate == "PASS",
        "repair_authorized": repair_authorized,
        "move_addition_authorized": move_addition_authorized,
        "next_unit_id": next_unit_id,
        "ready_for_live_runtime_adoption": False,
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "schema_created": False,
        "taxonomy_created": False,
        "fixture_expanded_by_default": False,
        "architecture_widened": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    profile = {
        "schema_version": "runtime_no_applicable_move_pressure_audit_profile_v0",
        "profile_status": status,
        "core_rule": "Expected pressure can close as coverage evidence when it matches a declared probe contract and does not reveal a real missing runtime objective.",
        "source_decision_receipt_ref": rel(DECISION_RECEIPT_PATH),
        "source_suite_receipt_ref": rel(SUITE_RECEIPT_PATH),
        "classification_ref": rel(CLASSIFICATION_PATH),
        "recommended_next": None if gate == "PASS" else "REPAIR_RUNTIME_NO_APPLICABLE_MOVE_PRESSURE_AUDIT_V0",
        "must_not_infer": [
            "NO_APPLICABLE_MOVE automatically means missing move",
            "expected negative coverage authorizes move creation",
            "candidate closure authorizes live runtime adoption",
            "C8 is authorized",
        ],
    }

    trace = {
        "schema_version": "runtime_no_applicable_move_pressure_audit_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "NO_APPLICABLE_MOVE_PRESSURE_AUDIT_NEXT",
                "edge": "consume pressure candidate and expected-pressure contract",
                "to": "NO_APPLICABLE_MOVE_EVIDENCE_INDEXED" if gate == "PASS" else "NO_APPLICABLE_MOVE_AUDIT_GATE_FAIL",
            },
            {
                "from": "NO_APPLICABLE_MOVE_EVIDENCE_INDEXED" if gate == "PASS" else "NO_APPLICABLE_MOVE_AUDIT_GATE_FAIL",
                "edge": "classify candidate",
                "to": "EXPECTED_NEGATIVE_COVERAGE_CLOSED" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": terminal_type,
            "stop_code": stop_code,
            "next_unit_id": next_unit_id,
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (EVIDENCE_PATH, evidence),
        (CLASSIFICATION_PATH, classification),
        (CLOSURE_PATH, closure),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_OUT_PATH, trace),
    ]:
        write_json(path, obj)

    source_hashes_after = {rel(p): file_sha256(p) for p in required}
    source_mutated = source_hashes_before != source_hashes_after
    if source_mutated:
        gate = "FAIL"
        status = "TYPED_NO_APPLICABLE_MOVE_PRESSURE_AUDIT_SOURCE_MUTATION_FAIL"
        failures.append("source_inputs_mutated")

    reason_codes = [
        "DECISION_RECEIPT_CONSUMED",
        "SUITE_CANDIDATE_CONSUMED",
        "NO_APPLICABLE_MOVE_PROBE_CONTRACT_MATCHED",
        "PROBE_TOKEN_NOT_REGISTERED_AS_REAL_RUNTIME_PHASE",
        "CLASSIFIED_AS_EXPECTED_NEGATIVE_COVERAGE",
        "CANDIDATE_CLOSED_NO_REPAIR",
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
        "schema_version": "runtime_no_applicable_move_pressure_audit_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_NO_APPLICABLE_MOVE_PRESSURE_AUDIT_RECEIPT",
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
        "source_decision_receipt_id": SOURCE_DECISION_RECEIPT_ID,
        "source_suite_receipt_id": SOURCE_SUITE_RECEIPT_ID,
        "acceptance_gate_results": {
            "NO_APP_0_DECISION_RECEIPT_CONSUMED": gate == "PASS",
            "NO_APP_1_SUITE_CANDIDATE_CONSUMED": gate == "PASS",
            "NO_APP_2_EXPECTED_PRESSURE_CONTRACT_MATCHED": gate == "PASS",
            "NO_APP_3_PROBE_TOKEN_NOT_REAL_REGISTRY_PHASE": gate == "PASS",
            "NO_APP_4_CLASSIFICATION_EMITTED": gate == "PASS",
            "NO_APP_5_CANDIDATE_CLOSED": gate == "PASS",
            "NO_APP_6_NO_REPAIR": gate == "PASS",
            "NO_APP_7_NO_MOVE_ADDITION": gate == "PASS",
            "NO_APP_8_SOURCE_INPUTS_NOT_MUTATED": not source_mutated,
            "NO_APP_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_no_applicable_move_audit_summary": {
            "status": status,
            "classification_kind": classification_kind,
            "candidate_closed": gate == "PASS",
            "candidate_id": candidate_id,
            "source_case_id": source_case_id,
            "is_real_missing_move_pressure": False if gate == "PASS" else None,
            "is_expected_negative_coverage": True if gate == "PASS" else None,
            "is_underdeclared_probe_artifact": False if gate == "PASS" else None,
            "repair_authorized": False,
            "move_addition_authorized": False,
            "next_unit_id": next_unit_id,
            "ready_for_live_runtime_adoption": False,
            "runtime_adoption_authorized": False,
            "runtime_patched": False,
            "live_runtime_hooks_installed": False,
            "schema_archive_mutated": False,
            "schema_created": False,
            "taxonomy_created": False,
            "fixture_expanded_by_default": False,
            "architecture_widened": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "evidence": rel(EVIDENCE_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "closure": rel(CLOSURE_PATH),
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
    print(f"runtime_no_applicable_move_audit_receipt_id={receipt_id}")
    print(f"runtime_no_applicable_move_audit_receipt_path={rel(receipt_path)}")
    print(f"runtime_no_applicable_move_audit_terminal={stop_code}")
    print("runtime_no_applicable_move_audit_next_unit=NONE")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
