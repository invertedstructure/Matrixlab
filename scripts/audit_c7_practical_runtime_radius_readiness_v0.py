#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "AUDIT_C7_PRACTICAL_RUNTIME_RADIUS_READINESS_V0"
TARGET_UNIT_ID = "runtime.practical_radius_expansion.readiness_audit.v0"
NEXT_UNIT_ID = "PREPARE_C7_RUNTIME_RADIUS_CONTRACTS_AND_BUDGET_V0"

LAYER = "RUNTIME / C7 / READINESS"
MODE = "AUDIT_ONLY / ENUMERATE_MISSING_SURFACES / NO_RUNTIME_RUN"
BUILD_MODE = "C7_READINESS_AUDIT_ONLY"

SOURCE_C8_BASIC_BRANCH_CLOSURE_RECEIPT_ID = "52630b77"
SOURCE_C8_BASIC_REFERENCE_RECEIPT_ID = "a4486c76"
SOURCE_C8_TARGET_SHAPE_REFERENCE_RECEIPT_ID = "ea23fd9b"
SOURCE_SCHEMA_VALIDATOR_REFERENCE_RECEIPT_ID = "732016f0"
SOURCE_SIDECAR_REFERENCE_RECEIPT_ID = "bee348a1"

C8_BASIC_BRANCH_CLOSURE_RECEIPT_PATH = ROOT / "data/post_c8_basic_interlock_mechanic_reference_decision_v0_receipts/52630b77.json"
C8_BASIC_BRANCH_CLOSURE_PATH = ROOT / "data/post_c8_basic_interlock_mechanic_reference_decision_v0/c8_basic_interlock_mechanic_reference_branch_closure_v0.json"
C8_BASIC_BRANCH_DECISION_PATH = ROOT / "data/post_c8_basic_interlock_mechanic_reference_decision_v0/post_c8_basic_interlock_mechanic_reference_decision_v0.json"
C8_BASIC_BRANCH_BOUNDARY_PATH = ROOT / "data/post_c8_basic_interlock_mechanic_reference_decision_v0/post_c8_basic_interlock_mechanic_reference_decision_boundary_v0.json"
C8_BASIC_BRANCH_ROLLUP_PATH = ROOT / "data/post_c8_basic_interlock_mechanic_reference_decision_v0/post_c8_basic_interlock_mechanic_reference_decision_rollup_v0.json"
C8_BASIC_BRANCH_PROFILE_PATH = ROOT / "data/post_c8_basic_interlock_mechanic_reference_decision_v0/post_c8_basic_interlock_mechanic_reference_decision_profile_v0.json"

C8_BASIC_REFERENCE_RECEIPT_PATH = ROOT / "data/c8_basic_interlock_mechanic_reviewed_reference_v0_receipts/a4486c76.json"
C8_BASIC_REVIEWED_REFERENCE_PATH = ROOT / "data/c8_basic_interlock_mechanic_reviewed_reference_v0/c8_basic_interlock_mechanic_reviewed_reference_v0.json"

C8_TARGET_SHAPE_REFERENCE_RECEIPT_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0_receipts/ea23fd9b.json"
C8_TARGET_SHAPE_REVIEWED_REFERENCE_PATH = ROOT / "data/c8_target_shape_reviewed_reference_v0/c8_target_shape_reviewed_reference_v0.json"

SCHEMA_VALIDATOR_REFERENCE_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0_receipts/732016f0.json"
SCHEMA_VALIDATOR_REFERENCE_PATH = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0/runtime_schema_validator_reviewed_reference_v0.json"

SIDECAR_REFERENCE_RECEIPT_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0_receipts/bee348a1.json"
SIDECAR_REVIEWED_REFERENCE_PATH = ROOT / "data/runtime_observability_sidecar_reference_closure_v0/runtime_observability_sidecar_reviewed_reference_v0.json"

OUT_DIR = ROOT / "data/c7_practical_runtime_radius_readiness_v0"
RECEIPT_DIR = ROOT / "data/c7_practical_runtime_radius_readiness_v0_receipts"

BASIS_PATH = OUT_DIR / "c7_readiness_audit_basis_v0.json"
SURFACE_INVENTORY_PATH = OUT_DIR / "c7_required_surface_inventory_v0.json"
MISSING_SURFACES_PATH = OUT_DIR / "c7_missing_or_weak_surfaces_v0.json"
SEQUENCE_PLAN_PATH = OUT_DIR / "c7_sequence_to_test_runs_v0.json"
CONTRACT_TARGET_PATH = OUT_DIR / "c7_contract_targets_v0.json"
NEGATIVE_COUNTER_TARGET_PATH = OUT_DIR / "c7_negative_counter_targets_v0.json"
TEST_FIXTURE_PLAN_PATH = OUT_DIR / "c7_test_fixture_plan_v0.json"
ROLLUP_PATH = OUT_DIR / "c7_readiness_audit_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "c7_readiness_audit_profile_v0.json"
TRACE_PATH = OUT_DIR / "c7_readiness_audit_transition_trace.json"

EXPECTED_BRANCH_CLOSURE_STATUS = "TYPED_C8_BASIC_INTERLOCK_REFERENCE_BRANCH_CLOSED_NO_RUNTIME_ADOPTION"
EXPECTED_C8_BASIC_REFERENCE_STATUS = "TYPED_C8_BASIC_INTERLOCK_MECHANIC_FROZEN_AS_REVIEWED_REFERENCE_DECISION_READY"

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
        C8_BASIC_BRANCH_CLOSURE_RECEIPT_PATH,
        C8_BASIC_BRANCH_CLOSURE_PATH,
        C8_BASIC_BRANCH_DECISION_PATH,
        C8_BASIC_BRANCH_BOUNDARY_PATH,
        C8_BASIC_BRANCH_ROLLUP_PATH,
        C8_BASIC_BRANCH_PROFILE_PATH,
        C8_BASIC_REFERENCE_RECEIPT_PATH,
        C8_BASIC_REVIEWED_REFERENCE_PATH,
        C8_TARGET_SHAPE_REFERENCE_RECEIPT_PATH,
        C8_TARGET_SHAPE_REVIEWED_REFERENCE_PATH,
        SCHEMA_VALIDATOR_REFERENCE_RECEIPT_PATH,
        SCHEMA_VALIDATOR_REFERENCE_PATH,
        SIDECAR_REFERENCE_RECEIPT_PATH,
        SIDECAR_REVIEWED_REFERENCE_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    branch_receipt = read_json(C8_BASIC_BRANCH_CLOSURE_RECEIPT_PATH)
    branch_closure = read_json(C8_BASIC_BRANCH_CLOSURE_PATH)
    branch_decision = read_json(C8_BASIC_BRANCH_DECISION_PATH)
    branch_boundary = read_json(C8_BASIC_BRANCH_BOUNDARY_PATH)
    branch_rollup = read_json(C8_BASIC_BRANCH_ROLLUP_PATH)
    branch_profile = read_json(C8_BASIC_BRANCH_PROFILE_PATH)

    c8_basic_receipt = read_json(C8_BASIC_REFERENCE_RECEIPT_PATH)
    c8_basic_reference = read_json(C8_BASIC_REVIEWED_REFERENCE_PATH)

    c8_target_receipt = read_json(C8_TARGET_SHAPE_REFERENCE_RECEIPT_PATH)
    c8_target_reference = read_json(C8_TARGET_SHAPE_REVIEWED_REFERENCE_PATH)

    schema_validator_receipt = read_json(SCHEMA_VALIDATOR_REFERENCE_RECEIPT_PATH)
    schema_validator_reference = read_json(SCHEMA_VALIDATOR_REFERENCE_PATH)

    sidecar_receipt = read_json(SIDECAR_REFERENCE_RECEIPT_PATH)
    sidecar_reference = read_json(SIDECAR_REVIEWED_REFERENCE_PATH)

    branch_summary = branch_receipt.get("machine_readable_post_c8_basic_interlock_mechanic_reference_decision_summary", {})
    c8_basic_summary = c8_basic_receipt.get("machine_readable_c8_basic_interlock_mechanic_reference_summary", {})

    if branch_receipt.get("receipt_id") != SOURCE_C8_BASIC_BRANCH_CLOSURE_RECEIPT_ID:
        failures.append(f"branch_receipt_id_wrong:{branch_receipt.get('receipt_id')}")
    if branch_receipt.get("gate") != "PASS":
        failures.append(f"branch_receipt_gate_wrong:{branch_receipt.get('gate')}")
    if branch_summary.get("status") != EXPECTED_BRANCH_CLOSURE_STATUS:
        failures.append(f"branch_status_wrong:{branch_summary.get('status')}")
    if branch_receipt.get("terminal", {}).get("type") != "STOP_DONE":
        failures.append("branch_terminal_not_stop_done")
    if branch_receipt.get("terminal", {}).get("next_unit_id") is not None:
        failures.append("branch_terminal_has_next_unit")

    if c8_basic_receipt.get("receipt_id") != SOURCE_C8_BASIC_REFERENCE_RECEIPT_ID:
        failures.append(f"c8_basic_reference_receipt_id_wrong:{c8_basic_receipt.get('receipt_id')}")
    if c8_basic_receipt.get("gate") != "PASS":
        failures.append("c8_basic_reference_gate_not_pass")
    if c8_basic_summary.get("status") != EXPECTED_C8_BASIC_REFERENCE_STATUS:
        failures.append(f"c8_basic_reference_status_wrong:{c8_basic_summary.get('status')}")
    if c8_basic_reference.get("reference_status") != "C8_BASIC_INTERLOCK_MECHANIC_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"c8_basic_reviewed_reference_status_wrong:{c8_basic_reference.get('reference_status')}")
    if c8_target_reference.get("reference_status") != "C8_TARGET_SHAPE_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"c8_target_reference_status_wrong:{c8_target_reference.get('reference_status')}")
    if schema_validator_reference.get("reference_status") != "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"schema_validator_reference_status_wrong:{schema_validator_reference.get('reference_status')}")
    if sidecar_reference.get("reference_status") != "RUNTIME_OBSERVABILITY_SIDECAR_REVIEWED_REFERENCE_FROZEN":
        failures.append(f"sidecar_reference_status_wrong:{sidecar_reference.get('reference_status')}")

    for key in [
        "c8_runtime_authorized",
        "c8_execution_authorized",
        "runtime_adoption_authorized",
        "live_runtime_hooks_installed",
        "runtime_patched",
        "runtime_routing_installed",
        "validation_verdict_emitted",
        "admissibility_checked",
        "authorization_verdict_emitted",
        "execution_claimed",
        "schema_archive_mutated",
        "schema_created",
        "control_path_blocked",
        "control_path_advanced",
        "hidden_next_command",
    ]:
        require_false(branch_summary, key, failures)
        require_false(c8_basic_summary, key, failures)

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C7_READINESS_AUDIT_DONE_CONTRACTS_AND_BUDGET_NEXT" if gate == "PASS" else "TYPED_C7_READINESS_AUDIT_GATE_FAIL"

    source_hash_manifest = {rel(p): file_sha256(p) for p in required}

    present_surfaces = [
        {
            "surface_id": "schema_validator_reference",
            "status": "PRESENT_REFERENCE_FROZEN",
            "source_receipt_id": SOURCE_SCHEMA_VALIDATOR_REFERENCE_RECEIPT_ID,
            "role_for_c7": "schema shape validation reference",
        },
        {
            "surface_id": "cell0_lawful_admissibility_surface",
            "status": "PRESENT_AS_CELL0_ROLE_BUT_NOT_YET_C7_PACKETIZED",
            "source_receipt_id": SOURCE_C8_BASIC_BRANCH_CLOSURE_RECEIPT_ID,
            "role_for_c7": "admissibility/authority boundary; Cell 0 named properly, not a new cell",
        },
        {
            "surface_id": "runtime_observability_sidecar_reference",
            "status": "PRESENT_REFERENCE_FROZEN",
            "source_receipt_id": SOURCE_SIDECAR_REFERENCE_RECEIPT_ID,
            "role_for_c7": "load-bearing observation surface",
        },
        {
            "surface_id": "c8_basic_interlock_mechanic_reference",
            "status": "PRESENT_REFERENCE_FROZEN",
            "source_receipt_id": SOURCE_C8_BASIC_REFERENCE_RECEIPT_ID,
            "role_for_c7": "basic interlock shape: proposal/reference, schema boundary, sidecar observation, control-path boundary",
        },
    ]

    missing_or_weak_surfaces = [
        {
            "surface_id": "c7_runtime_step_packet_contract",
            "status": "MISSING",
            "why_needed": "C7 cannot continue by inferred next command; each step must be packetized.",
            "minimum_artifact": "runtime_step_packet_contract_v0.json",
            "next_handling": "define/freeze in C7 contracts unit",
        },
        {
            "surface_id": "c7_runtime_radius_stop_packet_contract",
            "status": "MISSING",
            "why_needed": "C7 stops must be typed and diagnostic, not bare failed status.",
            "minimum_artifact": "runtime_radius_stop_packet_contract_v0.json",
            "next_handling": "define/freeze in C7 contracts unit",
        },
        {
            "surface_id": "c7_runtime_radius_budget",
            "status": "MISSING",
            "why_needed": "C7 must be bounded; radius expansion cannot become keep-going momentum.",
            "minimum_artifact": "runtime_radius_budget_v0.json",
            "next_handling": "define/freeze in C7 contracts unit",
        },
        {
            "surface_id": "c7_unit_feedback_record_contract",
            "status": "MISSING_OR_WEAK",
            "why_needed": "C7 needs useful failure feedback for missing capability, weak feedback, and diagnostic halts.",
            "minimum_artifact": "unit_feedback_record_contract_v0.json",
            "next_handling": "define/freeze in C7 contracts unit",
        },
        {
            "surface_id": "c7_negative_counter_contract",
            "status": "MISSING",
            "why_needed": "C7 must prove hidden continuation, invalid advancement, denied execution, and freebuild counters are zero.",
            "minimum_artifact": "runtime_radius_negative_counter_contract_v0.json",
            "next_handling": "define/freeze in C7 contracts unit",
        },
        {
            "surface_id": "c7_synthetic_runner_harness",
            "status": "MISSING",
            "why_needed": "First C7 test should be bounded/synthetic, not live runtime adoption.",
            "minimum_artifact": "run_c7_runtime_radius_synthetic_v0.py",
            "next_handling": "build after contracts and fixtures",
        },
        {
            "surface_id": "c7_test_fixture_sequences_A_to_E",
            "status": "MISSING",
            "why_needed": "C7 needs bounded tests for clean continuation, schema gap, authority boundary, inter-cell handoff, and missing capability feedback.",
            "minimum_artifact": "c7_runtime_radius_test_fixtures_v0.json",
            "next_handling": "build after contracts",
        },
        {
            "surface_id": "c7_rollup_and_readout",
            "status": "MISSING",
            "why_needed": "C7 success must not be inferred from step count alone.",
            "minimum_artifact": "runtime_radius_rollup_contract_v0.json",
            "next_handling": "define/freeze in C7 contracts unit",
        },
    ]

    sequence_to_test_runs = [
        {
            "order": 0,
            "unit_id": UNIT_ID,
            "status": "CURRENT_UNIT",
            "goal": "audit present/missing surfaces",
        },
        {
            "order": 1,
            "unit_id": "PREPARE_C7_RUNTIME_RADIUS_CONTRACTS_AND_BUDGET_V0",
            "goal": "freeze C7 packet, stop packet, budget, feedback, negative counter, rollup/readout contracts",
        },
        {
            "order": 2,
            "unit_id": "BUILD_C7_SYNTHETIC_RUNTIME_RADIUS_FIXTURES_V0",
            "goal": "create test sequences A-E as packet fixtures",
        },
        {
            "order": 3,
            "unit_id": "BUILD_C7_SYNTHETIC_RUNTIME_RADIUS_RUNNER_V0",
            "goal": "build bounded synthetic runner over frozen contracts and fixtures",
        },
        {
            "order": 4,
            "unit_id": "RUN_C7_SYNTHETIC_RADIUS_SEQUENCE_A_CLEAN_CONTINUATION_V0",
            "goal": "first test run only: clean continuation",
        },
        {
            "order": 5,
            "unit_id": "RUN_C7_SYNTHETIC_RADIUS_NEGATIVE_HALTS_B_C_V0",
            "goal": "schema gap and authority boundary halts",
        },
        {
            "order": 6,
            "unit_id": "RUN_C7_SYNTHETIC_RADIUS_HANDOFF_AND_FEEDBACK_D_E_V0",
            "goal": "inter-cell handoff and missing capability feedback",
        },
        {
            "order": 7,
            "unit_id": "ROLLUP_C7_SYNTHETIC_RUNTIME_RADIUS_TESTS_V0",
            "goal": "emit C7 rollup/readout and classify readiness for later runtime adoption discussion",
        },
    ]

    contract_targets = {
        "schema_version": "c7_contract_targets_v0",
        "contracts_to_prepare_next": [
            "runtime_step_packet_contract_v0",
            "runtime_radius_stop_packet_contract_v0",
            "runtime_radius_budget_v0",
            "unit_feedback_record_contract_v0",
            "runtime_radius_negative_counter_contract_v0",
            "runtime_radius_rollup_contract_v0",
            "runtime_radius_readout_contract_v0",
        ],
        "cell0_naming_law": "Cell 0 is the lawful admissibility surface; do not create a duplicate Lawful Admissibility Cell.",
        "contract_boundary": "contracts only; no C7 runtime run, no live runtime adoption, no execution authority",
    }

    negative_counter_targets = {
        "schema_version": "c7_negative_counter_targets_v0",
        "must_be_zero": [
            "schema_invalid_advanced_count",
            "unknown_schema_accepted_count",
            "admissibility_denied_executed_count",
            "authority_required_ignored_count",
            "proposal_applied_without_review_count",
            "proposed_only_consumed_by_cell1_count",
            "cell1_freebuild_count",
            "cell1_auto_chain_count",
            "receipt_missing_count",
            "sidecar_event_missing_count",
            "edge_observation_missing_count",
            "unit_feedback_missing_count",
            "bare_failed_status_count",
            "hidden_next_command_count",
            "untyped_halt_count",
            "productive_pressure_counted_as_radius_count",
            "higher_radius_treated_as_always_better_count",
            "global_autonomy_claim_count",
            "general_cell1_authority_claim_count",
            "research_lab_readiness_claim_count",
        ],
        "critical": [
            "hidden_next_command_count",
            "schema_invalid_advanced_count",
            "admissibility_denied_executed_count",
            "bare_failed_status_count",
            "higher_radius_treated_as_always_better_count",
        ],
    }

    test_fixture_plan = {
        "schema_version": "c7_test_fixture_plan_v0",
        "fixtures_to_build_after_contracts": [
            {
                "fixture_id": "sequence_A_clean_continuation",
                "expected_outcome": "RADIUS_EXPANDED_CLEANLY",
            },
            {
                "fixture_id": "sequence_B_schema_gap_halt",
                "expected_outcome": "RADIUS_BLOCKED_BY_SCHEMA_GAP",
            },
            {
                "fixture_id": "sequence_C_authority_boundary_halt",
                "expected_outcome": "RADIUS_BLOCKED_BY_AUTHORITY_BOUNDARY",
            },
            {
                "fixture_id": "sequence_D_cell1_accepted_build_handoff",
                "expected_outcome": "RADIUS_EXPANDED_WITH_TYPED_BOUNDARIES",
            },
            {
                "fixture_id": "sequence_E_missing_capability_feedback",
                "expected_outcome": "RADIUS_BLOCKED_BY_MISSING_CAPABILITY",
            },
        ],
    }

    basis = {
        "schema_version": "c7_readiness_audit_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_c8_basic_branch_closure_receipt_id": SOURCE_C8_BASIC_BRANCH_CLOSURE_RECEIPT_ID,
        "source_c8_basic_reference_receipt_id": SOURCE_C8_BASIC_REFERENCE_RECEIPT_ID,
        "source_c8_target_shape_reference_receipt_id": SOURCE_C8_TARGET_SHAPE_REFERENCE_RECEIPT_ID,
        "source_schema_validator_reference_receipt_id": SOURCE_SCHEMA_VALIDATOR_REFERENCE_RECEIPT_ID,
        "source_sidecar_reference_receipt_id": SOURCE_SIDECAR_REFERENCE_RECEIPT_ID,
        "source_files": source_hash_manifest,
        "audit_claim": "C7 readiness can be audited from the frozen schema-validator, sidecar, C8 target-shape, and C8 basic-interlock references.",
        "cell0_law": "Cell 0 is the lawful admissibility surface; do not introduce a duplicate Lawful Admissibility Cell.",
        "audit_does_not_authorize": [
            "C7 runtime run",
            "C8 runtime adoption",
            "C8 execution",
            "live hooks",
            "runtime patching",
            "runtime routing",
            "schema mutation",
            "control path authority",
        ],
    }

    surface_inventory = {
        "schema_version": "c7_required_surface_inventory_v0",
        "inventory_status": "EMITTED" if gate == "PASS" else "NOT_EMITTED",
        "present_surfaces": present_surfaces,
        "missing_or_weak_surfaces": missing_or_weak_surfaces,
    }

    missing_surfaces = {
        "schema_version": "c7_missing_or_weak_surfaces_v0",
        "missing_surface_count": len(missing_or_weak_surfaces) if gate == "PASS" else 0,
        "missing_or_weak_surfaces": missing_or_weak_surfaces,
        "blocking_before_test_run": [
            "c7_runtime_step_packet_contract",
            "c7_runtime_radius_stop_packet_contract",
            "c7_runtime_radius_budget",
            "c7_unit_feedback_record_contract",
            "c7_negative_counter_contract",
            "c7_test_fixture_sequences_A_to_E",
            "c7_synthetic_runner_harness",
        ],
    }

    sequence_plan = {
        "schema_version": "c7_sequence_to_test_runs_v0",
        "sequence_status": "NEXT_UNITS_NAMED" if gate == "PASS" else "NOT_NAMED",
        "sequence_to_first_test_run": sequence_to_test_runs,
        "first_actual_test_run_unit": "RUN_C7_SYNTHETIC_RADIUS_SEQUENCE_A_CLEAN_CONTINUATION_V0",
    }

    rollup = {
        "schema_version": "c7_readiness_audit_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "present_surface_count": len(present_surfaces) if gate == "PASS" else 0,
        "missing_or_weak_surface_count": len(missing_or_weak_surfaces) if gate == "PASS" else 0,
        "cell0_lawful_admissibility_surface_present_as_role": gate == "PASS",
        "schema_validator_reference_present": gate == "PASS",
        "sidecar_reference_present": gate == "PASS",
        "c8_basic_interlock_reference_present": gate == "PASS",
        "ready_for_c7_test_run": False,
        "ready_for_contract_preparation": gate == "PASS",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "c7_runtime_run_authorized": False,
        "runtime_adoption_authorized": False,
        "runtime_patched": False,
        "live_runtime_hooks_installed": False,
        "schema_archive_mutated": False,
        "control_path_authority_granted": False,
        "hidden_next_command": False,
    }

    profile = {
        "schema_version": "c7_readiness_audit_profile_v0",
        "profile_status": status,
        "profile": "C7_READINESS_AUDIT_AFTER_C8_BASIC_INTERLOCK_REFERENCE_BRANCH",
        "what_changed": "C7 required surfaces were inventoried and the sequence to first synthetic test run was named.",
        "what_did_not_change": [
            "C7 runtime test has not run",
            "runtime adoption is not authorized",
            "runtime is not patched",
            "live hooks are not installed",
            "schema archive is not mutated",
            "control path authority is not granted",
        ],
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_C7_READINESS_AUDIT_V0",
        "next_command_goal": None,
    }

    trace = {
        "schema_version": "c7_readiness_audit_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "C8_BASIC_INTERLOCK_REFERENCE_BRANCH_CLOSED",
                "edge": "consume closed reference branch",
                "to": "C7_READINESS_AUDIT_BASIS_ACCEPTED" if gate == "PASS" else "C7_READINESS_AUDIT_BASIS_FAIL",
            },
            {
                "from": "C7_READINESS_AUDIT_BASIS_ACCEPTED" if gate == "PASS" else "C7_READINESS_AUDIT_BASIS_FAIL",
                "edge": "enumerate missing surfaces before test run",
                "to": "C7_CONTRACTS_AND_BUDGET_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C7_READINESS_AUDIT_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (SURFACE_INVENTORY_PATH, surface_inventory),
        (MISSING_SURFACES_PATH, missing_surfaces),
        (SEQUENCE_PLAN_PATH, sequence_plan),
        (CONTRACT_TARGET_PATH, contract_targets),
        (NEGATIVE_COUNTER_TARGET_PATH, negative_counter_targets),
        (TEST_FIXTURE_PLAN_PATH, test_fixture_plan),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_PATH, trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "C7_READINESS_AUDIT_DONE",
        "CELL0_IS_LAWFUL_ADMISSIBILITY_SURFACE_NOT_DUPLICATE_CELL",
        "SCHEMA_VALIDATOR_REFERENCE_PRESENT",
        "RUNTIME_OBSERVABILITY_SIDECAR_REFERENCE_PRESENT",
        "C8_BASIC_INTERLOCK_REFERENCE_PRESENT",
        "C7_CONTRACTS_MISSING",
        "C7_BUDGET_MISSING",
        "C7_UNIT_FEEDBACK_CONTRACT_MISSING_OR_WEAK",
        "C7_FIXTURES_MISSING",
        "C7_SYNTHETIC_RUNNER_MISSING",
        "CONTRACTS_AND_BUDGET_ARE_NEXT_TYPED_UNIT",
        "NO_C7_RUNTIME_RUN",
        "NO_RUNTIME_ADOPTION",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_HOOK_INSTALL",
        "NO_SCHEMA_MUTATION",
        "NO_CONTROL_PATH_AUTHORITY",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt_body = {
        "schema_version": "c7_readiness_audit_receipt_v0",
        "receipt_type": "TYPED_C7_READINESS_AUDIT_RECEIPT",
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
        "source_c8_basic_branch_closure_receipt_id": SOURCE_C8_BASIC_BRANCH_CLOSURE_RECEIPT_ID,
        "source_c8_basic_reference_receipt_id": SOURCE_C8_BASIC_REFERENCE_RECEIPT_ID,
        "source_c8_target_shape_reference_receipt_id": SOURCE_C8_TARGET_SHAPE_REFERENCE_RECEIPT_ID,
        "source_schema_validator_reference_receipt_id": SOURCE_SCHEMA_VALIDATOR_REFERENCE_RECEIPT_ID,
        "source_sidecar_reference_receipt_id": SOURCE_SIDECAR_REFERENCE_RECEIPT_ID,
        "acceptance_gate_results": {
            "C7_READINESS_0_C8_BASIC_BRANCH_CLOSED": gate == "PASS",
            "C7_READINESS_1_SCHEMA_VALIDATOR_REFERENCE_PRESENT": gate == "PASS",
            "C7_READINESS_2_CELL0_ADMISSIBILITY_ROLE_IDENTIFIED": gate == "PASS",
            "C7_READINESS_3_SIDECAR_REFERENCE_PRESENT": gate == "PASS",
            "C7_READINESS_4_BASIC_INTERLOCK_REFERENCE_PRESENT": gate == "PASS",
            "C7_READINESS_5_MISSING_SURFACES_ENUMERATED": gate == "PASS",
            "C7_READINESS_6_SEQUENCE_TO_TEST_RUN_NAMED": gate == "PASS",
            "C7_READINESS_7_NO_RUNTIME_RUN": gate == "PASS",
            "C7_READINESS_8_NO_RUNTIME_ADOPTION": gate == "PASS",
            "C7_READINESS_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_c7_readiness_audit_summary": {
            "status": status,
            "c7_readiness_audit_done": gate == "PASS",
            "cell0_lawful_admissibility_surface_present_as_role": gate == "PASS",
            "schema_validator_reference_present": gate == "PASS",
            "runtime_observability_sidecar_reference_present": gate == "PASS",
            "c8_basic_interlock_reference_present": gate == "PASS",
            "present_surface_count": rollup["present_surface_count"],
            "missing_or_weak_surface_count": rollup["missing_or_weak_surface_count"],
            "ready_for_contract_preparation": gate == "PASS",
            "ready_for_c7_test_run": False,
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "c7_runtime_run_authorized": False,
            "runtime_adoption_authorized": False,
            "live_runtime_hooks_installed": False,
            "runtime_patched": False,
            "runtime_routing_installed": False,
            "validation_verdict_emitted": False,
            "admissibility_checked": False,
            "authorization_verdict_emitted": False,
            "execution_claimed": False,
            "schema_archive_mutated": False,
            "schema_created": False,
            "control_path_blocked": False,
            "control_path_advanced": False,
            "hidden_next_command": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "surface_inventory": rel(SURFACE_INVENTORY_PATH),
            "missing_surfaces": rel(MISSING_SURFACES_PATH),
            "sequence_plan": rel(SEQUENCE_PLAN_PATH),
            "contract_targets": rel(CONTRACT_TARGET_PATH),
            "negative_counter_targets": rel(NEGATIVE_COUNTER_TARGET_PATH),
            "test_fixture_plan": rel(TEST_FIXTURE_PLAN_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_C7_READINESS_AUDIT_GATE_FAIL",
        },
    }

    receipt_id = sig8(receipt_body)
    receipt_body["receipt_id"] = receipt_id
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"
    receipt_body["output_artifacts"]["implementation_receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_body)

    print(json.dumps(receipt_body, indent=2, sort_keys=True))
    print(f"c7_readiness_audit_receipt_id={receipt_id}")
    print(f"c7_readiness_audit_receipt_path={rel(receipt_path)}")
    print(f"c7_readiness_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
