#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_RUNTIME_OBSERVABILITY_STATUS_CASE_CONTRACT_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.incremental_suite.observability_status_case_contract_v0"
NEXT_UNIT_ID = "PREPARE_RUNTIME_NON_WRITING_NEGATIVE_CONTROL_PROBE_CONTRACT_V0"

LAYER = "OUTER / RUNTIME_ADOPTION / INCREMENTAL_SUITE_PREFLIGHT"
MODE = "PREPARE_CONTRACT_ONLY / OBSERVABILITY_STATUS_CASES / NO_TEST_RUN"
BUILD_MODE = "RUNTIME_OBSERVABILITY_STATUS_CASE_CONTRACT_ONLY"

SOURCE_EXPECTED_PRESSURE_RECEIPT_ID = "201aad4a"
SOURCE_SIDECAR_RECEIPT_ID = "bee348a1"

EXPECTED_PRESSURE_RECEIPT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0_receipts/201aad4a.json"
EXPECTED_PRESSURE_CONTRACT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_expected_pressure_case_contract_v0.json"
ALLOWED_EXPECTED_PRESSURE_CASES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_allowed_expected_pressure_cases_v0.json"
CASE_MANIFEST_EXPECTED_PRESSURE_RULES_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_case_manifest_expected_pressure_rules_v0.json"
COMPACT_SUITE_AFTER_EXPECTED_PRESSURE_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_compact_suite_shape_after_expected_pressure_contract_v0.json"
OBSERVABILITY_STATUS_TARGET_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_observability_status_case_contract_target_v0.json"

SIDECAR_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0_receipts/bee348a1.json"
SIDECAR_REFERENCE_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/runtime_observability_sidecar_reviewed_reference_v0.json"

REACHABILITY_MAP_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_registry_reachability_map_v0.json"
BRANCH_GAP_INDEX_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_branch_gap_index_v0.json"
SMOKE_RECEIPT_PATH = ROOT / "data/runtime_adoption_smoke_v0_receipts/runtime_smoke_receipt_900b2eae.json"
SMOKE_TRACE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_smoke_trace_v0.jsonl"

OUT_DIR = ROOT / "data/runtime_incremental_suite_preflight_v0"
RECEIPT_DIR = ROOT / "data/runtime_incremental_suite_preflight_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_observability_status_case_contract_basis_v0.json"
CONTRACT_PATH = OUT_DIR / "runtime_observability_status_case_contract_v0.json"
ALLOWED_OBSERVABILITY_CASES_PATH = OUT_DIR / "runtime_allowed_observability_status_cases_v0.json"
FORBIDDEN_CONTROL_CLAIMS_PATH = OUT_DIR / "runtime_forbidden_observability_control_claims_v0.json"
CASE_MANIFEST_OBSERVABILITY_RULES_PATH = OUT_DIR / "runtime_case_manifest_observability_status_rules_v0.json"
COMPACT_SUITE_AFTER_OBSERVABILITY_PATH = OUT_DIR / "runtime_compact_suite_shape_after_observability_status_contract_v0.json"
NEXT_TARGET_PATH = OUT_DIR / "runtime_negative_control_probe_contract_target_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_observability_status_case_contract_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_observability_status_case_contract_profile_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_observability_status_case_contract_transition_trace.json"

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
        EXPECTED_PRESSURE_RECEIPT_PATH,
        EXPECTED_PRESSURE_CONTRACT_PATH,
        ALLOWED_EXPECTED_PRESSURE_CASES_PATH,
        CASE_MANIFEST_EXPECTED_PRESSURE_RULES_PATH,
        COMPACT_SUITE_AFTER_EXPECTED_PRESSURE_PATH,
        OBSERVABILITY_STATUS_TARGET_PATH,
        SIDECAR_RECEIPT_PATH,
        SIDECAR_REFERENCE_PATH,
        REACHABILITY_MAP_PATH,
        BRANCH_GAP_INDEX_PATH,
        SMOKE_RECEIPT_PATH,
        SMOKE_TRACE_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    expected_pressure_receipt = read_json(EXPECTED_PRESSURE_RECEIPT_PATH)
    expected_pressure_summary = expected_pressure_receipt.get("machine_readable_expected_pressure_summary", {})
    expected_pressure_contract = read_json(EXPECTED_PRESSURE_CONTRACT_PATH)
    compact_shape = read_json(COMPACT_SUITE_AFTER_EXPECTED_PRESSURE_PATH)
    target = read_json(OBSERVABILITY_STATUS_TARGET_PATH)
    sidecar_receipt = read_json(SIDECAR_RECEIPT_PATH)
    sidecar_reference = read_json(SIDECAR_REFERENCE_PATH)
    reachability_map = read_json(REACHABILITY_MAP_PATH)
    branch_gap_index = read_json(BRANCH_GAP_INDEX_PATH)
    smoke_receipt = read_json(SMOKE_RECEIPT_PATH)
    smoke_trace = read_jsonl(SMOKE_TRACE_PATH)

    if expected_pressure_receipt.get("receipt_id") != SOURCE_EXPECTED_PRESSURE_RECEIPT_ID:
        failures.append(f"expected_pressure_receipt_id_wrong:{expected_pressure_receipt.get('receipt_id')}")
    if expected_pressure_receipt.get("gate") != "PASS":
        failures.append("expected_pressure_gate_not_pass")
    if expected_pressure_summary.get("ready_for_observability_status_case_contract") is not True:
        failures.append("expected_pressure_not_ready_for_observability_status_contract")
    if expected_pressure_summary.get("ready_for_full_test_batch") is not False:
        failures.append("full_test_batch_should_not_be_ready_yet")
    if expected_pressure_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("expected_pressure_terminal_not_advance")
    if expected_pressure_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("expected_pressure_terminal_next_wrong")

    if target.get("target_status") != "OBSERVABILITY_STATUS_CASE_CONTRACT_NEXT":
        failures.append(f"target_status_wrong:{target.get('target_status')}")
    if target.get("next_unit_id") != UNIT_ID:
        failures.append(f"target_next_unit_wrong:{target.get('next_unit_id')}")

    if sidecar_receipt.get("receipt_id") != SOURCE_SIDECAR_RECEIPT_ID:
        failures.append(f"sidecar_receipt_id_wrong:{sidecar_receipt.get('receipt_id')}")
    if sidecar_receipt.get("gate") != "PASS":
        failures.append("sidecar_gate_not_pass")

    for key in [
        "runtime_adoption_authorized",
        "runtime_patched",
        "live_runtime_hooks_installed",
        "schema_archive_mutated",
        "schema_created",
        "taxonomy_created",
        "fixture_expanded_by_default",
        "architecture_widened",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(expected_pressure_summary, key, failures)

    sidecar_refs_seen = [
        row.get("sidecar_observation_ref")
        for row in smoke_trace
        if row.get("sidecar_observation_ref")
    ]
    if not sidecar_refs_seen:
        failures.append("smoke_trace_sidecar_observation_refs_missing")

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_RUNTIME_OBSERVABILITY_STATUS_CASE_CONTRACT_READY_NEGATIVE_CONTROLS_NEXT" if gate == "PASS" else "TYPED_RUNTIME_OBSERVABILITY_STATUS_CASE_CONTRACT_GATE_FAIL"

    contract = {
        "schema_version": "runtime_observability_status_case_contract_v0",
        "contract_status": "FROZEN_FOR_INCREMENTAL_SUITE_V0" if gate == "PASS" else "NOT_READY",
        "source_expected_pressure_contract_ref": rel(EXPECTED_PRESSURE_CONTRACT_PATH),
        "source_sidecar_reference_ref": rel(SIDECAR_REFERENCE_PATH),
        "core_rule": "Observability status is evidence, not control authority. Control path acts; Sidecar records.",
        "allowed_observability_statuses": [
            "OBSERVED",
            "DEGRADED_NON_BLOCKING",
            "GAP_EXPECTED_PRESSURE",
        ],
        "status_meanings": {
            "OBSERVED": "sidecar observation refs are present and no control claim is made",
            "DEGRADED_NON_BLOCKING": "observation is explicitly degraded but terminal may still be typed if full observability is not required",
            "GAP_EXPECTED_PRESSURE": "full observability was declared required and missing evidence must emit RUNTIME_OBSERVABILITY_GAP",
        },
        "sidecar_may": [
            "record event references",
            "record degraded status",
            "record missing observation as evidence gap",
            "support trace/readout comparison",
        ],
        "sidecar_may_not": [
            "select moves",
            "block moves",
            "advance moves",
            "validate schema",
            "authorize admissibility",
            "patch runtime",
            "install hooks",
            "mutate state",
            "emit hidden next command",
        ],
        "repair_inside_suite_authorized": False,
        "candidate_emission_only": True,
        "full_observability_gap_pressure": {
            "pressure_class": "RUNTIME_OBSERVABILITY_GAP",
            "outcome_class": "RUNTIME_SMOKE_BLOCKED_OBSERVABILITY_GAP",
            "terminal_type": "STOP",
            "repair_authorized": False,
        },
        "must_not_infer": [
            "sidecar has control authority",
            "degraded observation is runtime failure by default",
            "observability gap authorizes repair inside suite",
            "observability status authorizes live hooks",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    allowed_cases = [
        {
            "schema_version": "runtime_allowed_observability_status_case_v0",
            "case_contract_id": "observability_status_normal_observed_v0",
            "tier": "T4",
            "case_role": "normal_observed_event_sequence",
            "observability_required": True,
            "declared_observability_status": "OBSERVED",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
            "expected_trace_receipt_match": True,
            "expected_bad_counters_zero": True,
            "suite_may_continue_if_matched": True,
            "repair_authorized": False,
            "sidecar_control_authority": False,
            "why_allowed": "Clean smoke already produced sidecar observation refs; this case verifies normal observation is receipt-visible.",
        },
        {
            "schema_version": "runtime_allowed_observability_status_case_v0",
            "case_contract_id": "observability_status_degraded_nonblocking_v0",
            "tier": "T4",
            "case_role": "degraded_sidecar_observation_nonblocking",
            "observability_required": False,
            "declared_observability_status": "DEGRADED_NON_BLOCKING",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
            "expected_trace_receipt_match": True,
            "expected_bad_counters_zero": True,
            "suite_may_continue_if_matched": True,
            "repair_authorized": False,
            "sidecar_control_authority": False,
            "why_allowed": "A non-blocking degraded observation should be visible without giving the sidecar control over the runtime path.",
        },
        {
            "schema_version": "runtime_allowed_observability_status_case_v0",
            "case_contract_id": "observability_status_required_gap_pressure_v0",
            "tier": "T4",
            "case_role": "full_observability_required_gap",
            "observability_required": True,
            "declared_observability_status": "GAP_EXPECTED_PRESSURE",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_OBSERVABILITY_GAP",
            "expected_pressure_class": "RUNTIME_OBSERVABILITY_GAP",
            "expected_outcome_class": "RUNTIME_SMOKE_BLOCKED_OBSERVABILITY_GAP",
            "expected_trace_receipt_match": True,
            "expected_bad_counters_zero": True,
            "expected_refinement_candidate_count_min": 1,
            "suite_may_continue_if_matched": True,
            "repair_authorized": False,
            "sidecar_control_authority": False,
            "include_in_first_suite": False,
            "why_not_first_suite": "compact first suite uses normal + degraded observability; required-gap pressure can follow after negative controls",
            "why_allowed_later": "Full-observability-required gap is a typed pressure case, not repair authority.",
        },
    ]

    forbidden_control_claims = {
        "schema_version": "runtime_forbidden_observability_control_claims_v0",
        "catalog_status": "EMITTED",
        "forbidden_count": 9,
        "forbidden": [
            {"forbidden_id": "sidecar_selects_move_fail", "rule": "sidecar may not select a move"},
            {"forbidden_id": "sidecar_blocks_move_fail", "rule": "sidecar may not block a move"},
            {"forbidden_id": "sidecar_advances_move_fail", "rule": "sidecar may not advance a move"},
            {"forbidden_id": "sidecar_validates_schema_fail", "rule": "sidecar may not validate schema"},
            {"forbidden_id": "sidecar_authorizes_admissibility_fail", "rule": "sidecar may not authorize admissibility"},
            {"forbidden_id": "sidecar_patches_runtime_fail", "rule": "sidecar may not patch runtime"},
            {"forbidden_id": "sidecar_installs_live_hook_fail", "rule": "sidecar may not install live hooks"},
            {"forbidden_id": "sidecar_mutates_state_fail", "rule": "sidecar may not mutate runtime state"},
            {"forbidden_id": "sidecar_hidden_next_command_fail", "rule": "sidecar may not emit hidden next command"},
        ],
    }

    case_manifest_rules = {
        "schema_version": "runtime_case_manifest_observability_status_rules_v0",
        "rules_status": "READY",
        "required_fields_for_observability_case": [
            "case_id",
            "tier",
            "case_name",
            "case_role",
            "runtime_state_ref",
            "observability_required",
            "declared_observability_status",
            "expected_terminal_type",
            "expected_stop_code",
            "expected_pressure_class",
            "expected_outcome_class",
            "expected_trace_receipt_match",
            "repair_authorized",
        ],
        "required_false_for_observability_case": [
            "repair_authorized",
            "sidecar_control_authority",
            "runtime_patch_authorized",
            "live_hook_install_authorized",
        ],
        "normal_status_rule": "OBSERVED requires sidecar observation refs in per-case trace/readout.",
        "degraded_status_rule": "DEGRADED_NON_BLOCKING may terminal normally if observability_required is false and degradation is receipt-visible.",
        "gap_status_rule": "GAP_EXPECTED_PRESSURE requires RUNTIME_OBSERVABILITY_GAP and candidate-only refinement record.",
        "continuation_rule": "suite_may_continue only if declared observability status and expected terminal/pressure/outcome match exactly.",
    }

    compact_suite_shape_after = {
        "schema_version": "runtime_compact_suite_shape_after_observability_status_contract_v0",
        "shape_status": "PARTIAL_READY_NEGATIVE_CONTROLS_NEXT" if gate == "PASS" else "NOT_READY",
        "ready_cases_after_this_unit": [
            "T0.baseline_replay",
            "T1.fresh_state_id",
            "T1.empty_history_ref",
            "T2.no_applicable_move_probe",
            "T4.normal_observed_event_sequence",
            "T4.degraded_sidecar_observation_nonblocking",
        ],
        "observability_cases_ready": [
            "T4.normal_observed_event_sequence",
            "T4.degraded_sidecar_observation_nonblocking",
        ],
        "observability_cases_allowed_later": [
            "T4.full_observability_required_gap",
        ],
        "not_ready_until_negative_control_probe_contract": [
            "T5.non_writing_negative_controls",
        ],
        "deferred": [
            "T3.schema_validation_failure",
            "T3.admissibility_block",
            "T6.step_cap_loop_shape",
            "T6.move_tie_unresolved",
        ],
        "recommended_first_suite_total_cases_after_all_preflight": 10,
    }

    next_target = {
        "schema_version": "runtime_negative_control_probe_contract_target_v0",
        "target_status": "NEGATIVE_CONTROL_PROBE_CONTRACT_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "why": "Observability status cases are now contracted; final missing piece before compact suite is non-writing negative-control probe contract for T5.",
        "inputs": [
            rel(CONTRACT_PATH),
            rel(ALLOWED_OBSERVABILITY_CASES_PATH),
            rel(FORBIDDEN_CONTROL_CLAIMS_PATH),
            rel(CASE_MANIFEST_OBSERVABILITY_RULES_PATH),
            rel(COMPACT_SUITE_AFTER_OBSERVABILITY_PATH),
        ],
        "forbidden": [
            "run full suite now",
            "mutate runtime for negative controls",
            "apply forbidden behavior to test it",
            "patch runtime",
            "add moves",
            "invent schemas",
        ],
    }

    basis = {
        "schema_version": "runtime_observability_status_case_contract_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_expected_pressure_receipt_id": SOURCE_EXPECTED_PRESSURE_RECEIPT_ID,
        "source_sidecar_receipt_id": SOURCE_SIDECAR_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "Expected-pressure contract made T2 ready; T4 still required a contract for observability status that keeps the sidecar non-control.",
        "does_not_authorize": [
            "suite execution",
            "sidecar control authority",
            "runtime move addition",
            "schema creation",
            "taxonomy creation",
            "fixture expansion by default",
            "runtime patching",
            "live hook installation",
            "C8 authorization",
        ],
    }

    rollup = {
        "schema_version": "runtime_observability_status_case_contract_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "allowed_observability_case_count": len(allowed_cases),
        "first_suite_observability_case_count": sum(1 for c in allowed_cases if c.get("include_in_first_suite", True) is not False),
        "forbidden_control_claim_count": forbidden_control_claims["forbidden_count"],
        "smoke_sidecar_observation_ref_count": len(sidecar_refs_seen),
        "observability_status_contract_done": gate == "PASS",
        "ready_for_negative_control_probe_contract": gate == "PASS",
        "ready_for_full_test_batch": False,
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "schema_created": False,
        "taxonomy_created": False,
        "fixture_expanded_by_default": False,
        "architecture_widened": False,
        "sidecar_control_authority_granted": False,
        "hidden_next_command": False,
        "c8_authorized": False,
    }

    profile = {
        "schema_version": "runtime_observability_status_case_contract_profile_v0",
        "profile_status": status,
        "core_rule": "Observability cases may vary evidence status, not control authority. Control path acts; Sidecar records.",
        "source_expected_pressure_receipt_ref": rel(EXPECTED_PRESSURE_RECEIPT_PATH),
        "source_sidecar_reference_ref": rel(SIDECAR_REFERENCE_PATH),
        "contract_ref": rel(CONTRACT_PATH),
        "allowed_cases_ref": rel(ALLOWED_OBSERVABILITY_CASES_PATH),
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_RUNTIME_OBSERVABILITY_STATUS_CASE_CONTRACT_V0",
        "must_not_infer": [
            "negative controls are ready",
            "full test batch is ready",
            "sidecar controls runtime",
            "observability gap authorizes repair inside suite",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    trace = {
        "schema_version": "runtime_observability_status_case_contract_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "EXPECTED_PRESSURE_CASE_CONTRACT_READY_OBSERVABILITY_STATUS_NEXT",
                "edge": "consume expected pressure contract and sidecar reference",
                "to": "OBSERVABILITY_STATUS_CASE_CONTRACT_BASIS_ACCEPTED" if gate == "PASS" else "OBSERVABILITY_STATUS_CASE_CONTRACT_GATE_FAIL",
            },
            {
                "from": "OBSERVABILITY_STATUS_CASE_CONTRACT_BASIS_ACCEPTED" if gate == "PASS" else "OBSERVABILITY_STATUS_CASE_CONTRACT_GATE_FAIL",
                "edge": "emit non-control observability status contract",
                "to": "NEGATIVE_CONTROL_PROBE_CONTRACT_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_RUNTIME_OBSERVABILITY_STATUS_CASE_CONTRACT_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (CONTRACT_PATH, contract),
        (ALLOWED_OBSERVABILITY_CASES_PATH, {
            "schema_version": "runtime_allowed_observability_status_cases_v0",
            "catalog_status": "EMITTED",
            "allowed_observability_case_count": len(allowed_cases),
            "first_suite_observability_case_count": rollup["first_suite_observability_case_count"],
            "cases": allowed_cases,
        }),
        (FORBIDDEN_CONTROL_CLAIMS_PATH, forbidden_control_claims),
        (CASE_MANIFEST_OBSERVABILITY_RULES_PATH, case_manifest_rules),
        (COMPACT_SUITE_AFTER_OBSERVABILITY_PATH, compact_suite_shape_after),
        (NEXT_TARGET_PATH, next_target),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_OUT_PATH, trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "EXPECTED_PRESSURE_CONTRACT_CONSUMED",
        "SIDECAR_REFERENCE_CONSUMED",
        "OBSERVABILITY_STATUS_CASE_CONTRACT_EMITTED",
        "NORMAL_OBSERVATION_CASE_READY",
        "DEGRADED_NONBLOCKING_OBSERVATION_CASE_READY",
        "REQUIRED_GAP_OBSERVATION_CASE_ALLOWED_LATER",
        "CONTROL_PATH_ACTS_SIDECAR_RECORDS",
        "NEGATIVE_CONTROL_PROBE_CONTRACT_NEXT",
        "NO_SUITE_RUN",
        "NO_SIDECAR_CONTROL_AUTHORITY",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_HOOK_INSTALL",
        "NO_MOVE_ADDITION",
        "NO_SCHEMA_INVENTION",
        "NO_TAXONOMY_INVENTION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_observability_status_case_contract_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_OBSERVABILITY_STATUS_CASE_CONTRACT_RECEIPT",
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
        "source_expected_pressure_receipt_id": SOURCE_EXPECTED_PRESSURE_RECEIPT_ID,
        "source_sidecar_receipt_id": SOURCE_SIDECAR_RECEIPT_ID,
        "acceptance_gate_results": {
            "OBS_STATUS_0_EXPECTED_PRESSURE_RECEIPT_CONSUMED": gate == "PASS",
            "OBS_STATUS_1_SIDECAR_REFERENCE_CONSUMED": gate == "PASS",
            "OBS_STATUS_2_SMOKE_TRACE_SIDECAR_REFS_SEEN": len(sidecar_refs_seen) > 0,
            "OBS_STATUS_3_CONTRACT_EMITTED": gate == "PASS",
            "OBS_STATUS_4_ALLOWED_CASES_EMITTED": gate == "PASS",
            "OBS_STATUS_5_FORBIDDEN_CONTROL_CLAIMS_EMITTED": gate == "PASS",
            "OBS_STATUS_6_MANIFEST_RULES_EMITTED": gate == "PASS",
            "OBS_STATUS_7_NEGATIVE_CONTROL_CONTRACT_NEXT": gate == "PASS",
            "OBS_STATUS_8_NO_SUITE_RUN": gate == "PASS",
            "OBS_STATUS_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_observability_status_summary": {
            "status": status,
            "observability_status_contract_done": gate == "PASS",
            "allowed_observability_case_count": rollup["allowed_observability_case_count"],
            "first_suite_observability_case_count": rollup["first_suite_observability_case_count"],
            "forbidden_control_claim_count": rollup["forbidden_control_claim_count"],
            "smoke_sidecar_observation_ref_count": rollup["smoke_sidecar_observation_ref_count"],
            "normal_observation_case_ready": gate == "PASS",
            "degraded_nonblocking_case_ready": gate == "PASS",
            "required_gap_case_allowed_later": gate == "PASS",
            "ready_for_negative_control_probe_contract": gate == "PASS",
            "ready_for_full_test_batch": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "runtime_adoption_authorized": False,
            "runtime_patched": False,
            "live_runtime_hooks_installed": False,
            "schema_archive_mutated": False,
            "schema_created": False,
            "taxonomy_created": False,
            "fixture_expanded_by_default": False,
            "architecture_widened": False,
            "sidecar_control_authority_granted": False,
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "observability_status_contract": rel(CONTRACT_PATH),
            "allowed_observability_status_cases": rel(ALLOWED_OBSERVABILITY_CASES_PATH),
            "forbidden_observability_control_claims": rel(FORBIDDEN_CONTROL_CLAIMS_PATH),
            "case_manifest_observability_rules": rel(CASE_MANIFEST_OBSERVABILITY_RULES_PATH),
            "compact_suite_shape_after_observability": rel(COMPACT_SUITE_AFTER_OBSERVABILITY_PATH),
            "next_target": rel(NEXT_TARGET_PATH),
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
    print(f"runtime_observability_status_contract_receipt_id={receipt_id}")
    print(f"runtime_observability_status_contract_receipt_path={rel(receipt_path)}")
    print(f"runtime_observability_status_contract_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
