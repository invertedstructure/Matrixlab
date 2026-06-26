#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "PREPARE_RUNTIME_DECLARED_STATE_VARIANT_RULES_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.incremental_suite.state_variant_rules_v0"
NEXT_UNIT_ID = "PREPARE_RUNTIME_INCREMENTAL_EXPECTED_PRESSURE_CASE_CONTRACT_V0"

LAYER = "OUTER / RUNTIME_ADOPTION / INCREMENTAL_SUITE_PREFLIGHT"
MODE = "PREPARE_RULES_ONLY / DECLARED_STATE_VARIANTS / NO_TEST_RUN"
BUILD_MODE = "RUNTIME_DECLARED_STATE_VARIANT_RULES_ONLY"

SOURCE_REACHABILITY_RECEIPT_ID = "de9b179a"

REACHABILITY_RECEIPT_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0_receipts/de9b179a.json"
REGISTRY_REACHABILITY_MAP_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_registry_reachability_map_v0.json"
BRANCH_GAP_INDEX_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_branch_gap_index_v0.json"
TIER_FEASIBILITY_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_incremental_suite_tier_feasibility_v0.json"
STATE_VARIANT_RULES_TARGET_PATH = ROOT / "data/runtime_incremental_suite_preflight_v0/runtime_declared_state_variant_rules_target_v0.json"

SMOKE_RECEIPT_PATH = ROOT / "data/runtime_adoption_smoke_v0_receipts/runtime_smoke_receipt_900b2eae.json"
SMOKE_STATE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_state_v0.json"
SMOKE_STATE_SCHEMA_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_state_schema_v0.json"
SMOKE_REGISTRY_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_move_registry_snapshot_v0.json"
SMOKE_TRACE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_smoke_trace_v0.jsonl"

OUT_DIR = ROOT / "data/runtime_incremental_suite_preflight_v0"
RECEIPT_DIR = ROOT / "data/runtime_incremental_suite_preflight_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_state_variant_rules_basis_v0.json"
RULES_PATH = OUT_DIR / "runtime_declared_state_variant_rules_v0.json"
VARIANT_CATALOG_PATH = OUT_DIR / "runtime_allowed_state_variant_catalog_v0.json"
FORBIDDEN_VARIANTS_PATH = OUT_DIR / "runtime_forbidden_state_variant_catalog_v0.json"
STATE_DERIVATION_TEMPLATE_PATH = OUT_DIR / "runtime_state_derivation_template_v0.json"
COMPACT_SUITE_SHAPE_PATH = OUT_DIR / "runtime_compact_suite_shape_after_state_rules_v0.json"
NEXT_TARGET_PATH = OUT_DIR / "runtime_expected_pressure_case_contract_target_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_state_variant_rules_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_state_variant_rules_profile_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_state_variant_rules_transition_trace.json"

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

def make_case_id(seed: Dict[str, Any]) -> str:
    return "runtime_case_" + sig8(seed)

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        REACHABILITY_RECEIPT_PATH,
        REGISTRY_REACHABILITY_MAP_PATH,
        BRANCH_GAP_INDEX_PATH,
        TIER_FEASIBILITY_PATH,
        STATE_VARIANT_RULES_TARGET_PATH,
        SMOKE_RECEIPT_PATH,
        SMOKE_STATE_PATH,
        SMOKE_STATE_SCHEMA_PATH,
        SMOKE_REGISTRY_PATH,
        SMOKE_TRACE_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    reachability_receipt = read_json(REACHABILITY_RECEIPT_PATH)
    reachability_summary = reachability_receipt.get("machine_readable_reachability_summary", {})
    reachability_map = read_json(REGISTRY_REACHABILITY_MAP_PATH)
    branch_gap_index = read_json(BRANCH_GAP_INDEX_PATH)
    tier_feasibility = read_json(TIER_FEASIBILITY_PATH)
    target = read_json(STATE_VARIANT_RULES_TARGET_PATH)

    smoke_receipt = read_json(SMOKE_RECEIPT_PATH)
    smoke_summary = smoke_receipt.get("machine_readable_runtime_smoke_summary", {})
    smoke_state = read_json(SMOKE_STATE_PATH)
    smoke_state_schema = read_json(SMOKE_STATE_SCHEMA_PATH)
    smoke_registry = read_json(SMOKE_REGISTRY_PATH)
    smoke_trace = read_jsonl(SMOKE_TRACE_PATH)

    if reachability_receipt.get("receipt_id") != SOURCE_REACHABILITY_RECEIPT_ID:
        failures.append(f"reachability_receipt_id_wrong:{reachability_receipt.get('receipt_id')}")
    if reachability_receipt.get("gate") != "PASS":
        failures.append(f"reachability_gate_wrong:{reachability_receipt.get('gate')}")
    if reachability_summary.get("ready_for_state_variant_rules") is not True:
        failures.append("reachability_not_ready_for_state_variant_rules")
    if reachability_summary.get("ready_for_full_test_batch") is not False:
        failures.append("full_test_batch_should_not_be_ready_yet")
    if reachability_receipt.get("terminal", {}).get("type") != "ADVANCE":
        failures.append("reachability_terminal_not_advance")
    if reachability_receipt.get("terminal", {}).get("next_unit_id") != UNIT_ID:
        failures.append("reachability_terminal_next_wrong")

    if target.get("target_status") != "STATE_VARIANT_RULES_NEXT":
        failures.append(f"target_status_wrong:{target.get('target_status')}")
    if target.get("next_unit_id") != UNIT_ID:
        failures.append(f"target_next_unit_wrong:{target.get('next_unit_id')}")

    if smoke_receipt.get("gate") != "PASS":
        failures.append("smoke_gate_not_pass")
    if smoke_summary.get("outcome_class") != "RUNTIME_SMOKE_PASS_TYPED_STOP":
        failures.append(f"smoke_outcome_wrong:{smoke_summary.get('outcome_class')}")
    if smoke_summary.get("pressure_class") != "STOP_DONE":
        failures.append(f"smoke_pressure_wrong:{smoke_summary.get('pressure_class')}")

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
        require_false(reachability_summary, key, failures)
        require_false(smoke_summary, key, failures)

    required_state_fields = set(smoke_state_schema.get("required_fields", []))
    smoke_state_fields = set(smoke_state.keys())
    missing_state_fields = sorted(required_state_fields - smoke_state_fields)
    if missing_state_fields:
        failures.append("smoke_state_missing_required_fields:" + ",".join(missing_state_fields))

    registry_phases = sorted(
        {
            (move.get("applies_when") or {}).get("runtime_phase")
            for move in smoke_registry.get("moves", [])
            if (move.get("applies_when") or {}).get("runtime_phase")
        }
    )

    observed_phases = []
    for row in smoke_trace:
        delta = row.get("state_delta") or {}
        if delta.get("runtime_phase"):
            observed_phases.append(delta["runtime_phase"])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_RUNTIME_DECLARED_STATE_VARIANT_RULES_READY_EXPECTED_PRESSURE_NEXT" if gate == "PASS" else "TYPED_RUNTIME_DECLARED_STATE_VARIANT_RULES_GATE_FAIL"

    mutable_fields_allowed = [
        {
            "field": "state_id",
            "rule": "may be regenerated from canonical state bytes",
            "reason": "T1 fresh state-id stability",
            "semantic_change": False,
        },
        {
            "field": "history_ref",
            "rule": "may be null, empty-equivalent, or point to declared prior trace/readout refs",
            "reason": "T1 history stability",
            "semantic_change": False,
        },
        {
            "field": "runtime_phase",
            "rule": "may only be one of registry phases or the explicit underdeclared edge token NO_APPLICABLE_MOVE_PROBE",
            "reason": "phase is selector input; unrecognized phase must be declared as expected pressure, not hidden behavior",
            "semantic_change": True,
            "requires_expected_pressure_contract": True,
        },
        {
            "field": "status",
            "rule": "may remain READY or be TERMINAL_MARKER_ONLY for explicit prior-terminal marker case",
            "reason": "T1 prior terminal marker stability",
            "semantic_change": False,
        },
    ]

    immutable_fields = [
        "schema_version",
        "active_object_ref",
        "active_object_kind",
        "regime_ref",
        "move_registry_ref",
        "schema_archive_ref",
        "admissibility_surface_ref",
        "observability_sidecar_ref",
        "receipt_surface_ref",
        "readout_surface_ref",
        "halt_vocabulary_ref",
        "declared_by",
        "must_not_infer",
    ]

    forbidden_mutations = [
        {
            "field_or_scope": "active_object_ref",
            "reason": "changing active object would become fixture/object expansion",
        },
        {
            "field_or_scope": "move_registry_ref",
            "reason": "changing registry would become move addition or registry swap",
        },
        {
            "field_or_scope": "schema_archive_ref",
            "reason": "changing schema archive would become schema mutation or authority swap",
        },
        {
            "field_or_scope": "admissibility_surface_ref",
            "reason": "changing admissibility surface would become authority widening/substitution",
        },
        {
            "field_or_scope": "observability_sidecar_ref",
            "reason": "changing sidecar ref belongs to later observability-status contract, not state variant rules",
        },
        {
            "field_or_scope": "runtime moves / actions / priorities",
            "reason": "state variant rules may not alter runtime behavior",
        },
        {
            "field_or_scope": "new state schema fields",
            "reason": "would create schema expansion before receipt pressure",
        },
    ]

    allowed_variants = [
        {
            "variant_id": "state_variant_baseline_replay_v0",
            "tier": "T0",
            "case_role": "baseline_replay",
            "description": "Exact clean smoke runtime state replay.",
            "allowed_mutations": [],
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
            "requires_expected_pressure_contract": False,
            "include_in_first_suite": True,
        },
        {
            "variant_id": "state_variant_fresh_state_id_v0",
            "tier": "T1",
            "case_role": "terminal_stability_fresh_state_id",
            "description": "Same fixed refs with regenerated state_id only.",
            "allowed_mutations": ["state_id"],
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
            "requires_expected_pressure_contract": False,
            "include_in_first_suite": True,
        },
        {
            "variant_id": "state_variant_empty_history_ref_v0",
            "tier": "T1",
            "case_role": "terminal_stability_empty_history",
            "description": "Same fixed refs with history_ref explicitly null/empty-equivalent.",
            "allowed_mutations": ["history_ref"],
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
            "requires_expected_pressure_contract": False,
            "include_in_first_suite": True,
        },
        {
            "variant_id": "state_variant_populated_history_ref_v0",
            "tier": "T1",
            "case_role": "terminal_stability_populated_history",
            "description": "Same fixed refs with history_ref pointing to the clean smoke trace.",
            "allowed_mutations": ["history_ref"],
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
            "requires_expected_pressure_contract": False,
            "include_in_first_suite": False,
            "why_not_first_suite": "compact suite uses two T1 cases first",
        },
        {
            "variant_id": "state_variant_prior_terminal_marker_v0",
            "tier": "T1",
            "case_role": "terminal_stability_prior_terminal_marker",
            "description": "Same fixed refs with explicit prior terminal marker status only.",
            "allowed_mutations": ["status", "history_ref"],
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_SMOKE_TYPED_TERMINAL",
            "expected_pressure_class": "STOP_DONE",
            "expected_outcome_class": "RUNTIME_SMOKE_PASS_TYPED_STOP",
            "requires_expected_pressure_contract": False,
            "include_in_first_suite": False,
            "why_not_first_suite": "compact suite keeps T1 minimal first",
        },
        {
            "variant_id": "state_variant_no_applicable_move_probe_v0",
            "tier": "T2/T6",
            "case_role": "declared_no_applicable_move_pressure",
            "description": "Explicit phase token that should select no registered move and emit expected NO_APPLICABLE_MOVE pressure.",
            "allowed_mutations": ["runtime_phase"],
            "runtime_phase_value": "NO_APPLICABLE_MOVE_PROBE",
            "expected_terminal_type": "STOP",
            "expected_stop_code": "STOP_RUNTIME_NO_APPLICABLE_MOVE",
            "expected_pressure_class": "NO_APPLICABLE_MOVE",
            "expected_outcome_class": "RUNTIME_SMOKE_BLOCKED_NO_APPLICABLE_MOVE",
            "requires_expected_pressure_contract": True,
            "include_in_first_suite": False,
            "why_not_first_suite": "requires expected-pressure case contract first",
        },
    ]

    forbidden_variants = [
        {
            "variant_id": "forbidden_variant_new_active_object_v0",
            "forbidden_mutation": "active_object_ref",
            "why": "would be fixture/object expansion, not state variant",
        },
        {
            "variant_id": "forbidden_variant_registry_swap_v0",
            "forbidden_mutation": "move_registry_ref",
            "why": "would bypass current registry only rule",
        },
        {
            "variant_id": "forbidden_variant_schema_archive_swap_v0",
            "forbidden_mutation": "schema_archive_ref",
            "why": "would be schema/archive mutation or authority swap",
        },
        {
            "variant_id": "forbidden_variant_admissibility_surface_swap_v0",
            "forbidden_mutation": "admissibility_surface_ref",
            "why": "would be authority widening/substitution",
        },
        {
            "variant_id": "forbidden_variant_new_runtime_phase_semantics_v0",
            "forbidden_mutation": "runtime_phase with new behavior semantics",
            "why": "only NO_APPLICABLE_MOVE_PROBE is allowed as expected pressure; no new behavior semantics",
        },
        {
            "variant_id": "forbidden_variant_move_priority_or_action_change_v0",
            "forbidden_mutation": "move priority/action/applies_when",
            "why": "would patch runtime behavior",
        },
    ]

    rules = {
        "schema_version": "runtime_declared_state_variant_rules_v0",
        "rules_status": "FROZEN_FOR_INCREMENTAL_SUITE_V0" if gate == "PASS" else "NOT_READY",
        "source_clean_smoke_state_ref": rel(SMOKE_STATE_PATH),
        "source_clean_smoke_receipt_ref": rel(SMOKE_RECEIPT_PATH),
        "source_reachability_map_ref": rel(REGISTRY_REACHABILITY_MAP_PATH),
        "selection_rule": "variants must be human-declared, bounded, derived from clean smoke fixed refs, and listed in the allowed catalog before execution",
        "allowed_mutable_fields": mutable_fields_allowed,
        "immutable_fields": immutable_fields,
        "forbidden_mutations": forbidden_mutations,
        "registry_phases": registry_phases,
        "observed_phase_path": observed_phases,
        "special_phase_tokens": [
            {
                "token": "NO_APPLICABLE_MOVE_PROBE",
                "status": "ALLOWED_ONLY_WITH_EXPECTED_PRESSURE_CONTRACT",
                "pressure_class": "NO_APPLICABLE_MOVE",
                "outcome_class": "RUNTIME_SMOKE_BLOCKED_NO_APPLICABLE_MOVE",
            }
        ],
        "must_not_infer": [
            "new active objects may be introduced",
            "new moves may be introduced",
            "state variants authorize schema changes",
            "state variants authorize runtime patching",
            "unrecognized phase creates behavior",
            "T3/T6 failure branches are ready",
            "C8 is authorized",
        ],
    }

    variant_catalog = {
        "schema_version": "runtime_allowed_state_variant_catalog_v0",
        "catalog_status": "EMITTED",
        "allowed_variant_count": len(allowed_variants),
        "first_suite_variant_count": sum(1 for v in allowed_variants if v.get("include_in_first_suite")),
        "variants": allowed_variants,
    }

    forbidden_catalog = {
        "schema_version": "runtime_forbidden_state_variant_catalog_v0",
        "catalog_status": "EMITTED",
        "forbidden_variant_count": len(forbidden_variants),
        "variants": forbidden_variants,
    }

    derivation_template = {
        "schema_version": "runtime_state_derivation_template_v0",
        "template_status": "READY",
        "source_state_ref": rel(SMOKE_STATE_PATH),
        "derivation_steps": [
            "copy clean smoke runtime_state_v0",
            "apply only catalog-listed allowed mutations",
            "regenerate state_id from canonical mutated state",
            "record derivation_ref and source_variant_id in case manifest, not as new schema fields unless already allowed",
            "validate required runtime_state_v0 fields remain present",
            "run through current registry only",
        ],
        "forbidden_steps": [
            "change active_object_ref",
            "change move_registry_ref",
            "change schema_archive_ref",
            "change admissibility_surface_ref",
            "add runtime moves",
            "add schema fields",
            "select latest/mtime file",
            "patch runtime",
        ],
    }

    compact_suite_shape = {
        "schema_version": "runtime_compact_suite_shape_after_state_rules_v0",
        "shape_status": "PARTIAL_READY_EXPECTED_PRESSURE_CONTRACT_NEXT" if gate == "PASS" else "NOT_READY",
        "ready_cases_after_this_unit": [
            "T0.baseline_replay",
            "T1.fresh_state_id",
            "T1.empty_history_ref",
        ],
        "not_ready_until_expected_pressure_contract": [
            "T2.no_applicable_move_probe",
            "any case with expected non-STOP_DONE pressure",
        ],
        "not_ready_until_observability_status_contract": [
            "T4.observability_degraded_or_gap",
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
        "schema_version": "runtime_expected_pressure_case_contract_target_v0",
        "target_status": "EXPECTED_PRESSURE_CASE_CONTRACT_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "why": "State variants now permit clean stability cases and identify expected-pressure variants; before the suite can include those, expected pressure must be explicitly contracted.",
        "inputs": [
            rel(RULES_PATH),
            rel(VARIANT_CATALOG_PATH),
            rel(FORBIDDEN_VARIANTS_PATH),
            rel(COMPACT_SUITE_SHAPE_PATH),
        ],
        "forbidden": [
            "run full suite now",
            "add moves",
            "invent schemas",
            "patch runtime",
            "treat expected pressure as repair authorization",
        ],
    }

    basis = {
        "schema_version": "runtime_state_variant_rules_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_reachability_receipt_id": SOURCE_REACHABILITY_RECEIPT_ID,
        "source_files": {rel(p): file_sha256(p) for p in required},
        "basis_claim": "Reachability audit identified state variant rules as the next required preflight before declaring the incremental suite.",
        "does_not_authorize": [
            "suite execution",
            "runtime move addition",
            "schema creation",
            "taxonomy creation",
            "fixture expansion by default",
            "runtime patching",
            "C8 authorization",
        ],
    }

    rollup = {
        "schema_version": "runtime_state_variant_rules_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "allowed_variant_count": len(allowed_variants),
        "first_suite_variant_count": sum(1 for v in allowed_variants if v.get("include_in_first_suite")),
        "forbidden_variant_count": len(forbidden_variants),
        "special_expected_pressure_variant_count": sum(1 for v in allowed_variants if v.get("requires_expected_pressure_contract")),
        "ready_for_expected_pressure_case_contract": gate == "PASS",
        "ready_for_full_test_batch": False,
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
        "schema_version": "runtime_state_variant_rules_profile_v0",
        "profile_status": status,
        "core_rule": "Declared runtime state variants may vary only bounded non-semantic fields or explicitly contracted expected-pressure fields; they may not create new runtime behavior.",
        "source_reachability_receipt_ref": rel(REACHABILITY_RECEIPT_PATH),
        "rules_ref": rel(RULES_PATH),
        "variant_catalog_ref": rel(VARIANT_CATALOG_PATH),
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_RUNTIME_DECLARED_STATE_VARIANT_RULES_V0",
        "must_not_infer": [
            "expected pressure cases are ready before their contract",
            "observability stress is ready",
            "negative controls are ready",
            "T3/T6 failure branches are reachable",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    trace = {
        "schema_version": "runtime_state_variant_rules_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "REACHABILITY_MAP_READY_STATE_VARIANTS_NEXT",
                "edge": "consume reachability map and branch gap index",
                "to": "STATE_VARIANT_RULES_BASIS_ACCEPTED" if gate == "PASS" else "STATE_VARIANT_RULES_GATE_FAIL",
            },
            {
                "from": "STATE_VARIANT_RULES_BASIS_ACCEPTED" if gate == "PASS" else "STATE_VARIANT_RULES_GATE_FAIL",
                "edge": "emit allowed/forbidden state variant catalogs",
                "to": "EXPECTED_PRESSURE_CASE_CONTRACT_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_RUNTIME_DECLARED_STATE_VARIANT_RULES_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (RULES_PATH, rules),
        (VARIANT_CATALOG_PATH, variant_catalog),
        (FORBIDDEN_VARIANTS_PATH, forbidden_catalog),
        (STATE_DERIVATION_TEMPLATE_PATH, derivation_template),
        (COMPACT_SUITE_SHAPE_PATH, compact_suite_shape),
        (NEXT_TARGET_PATH, next_target),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_OUT_PATH, trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "REACHABILITY_MAP_CONSUMED",
        "STATE_VARIANT_RULES_EMITTED",
        "ALLOWED_VARIANT_CATALOG_EMITTED",
        "FORBIDDEN_VARIANT_CATALOG_EMITTED",
        "T0_T1_VARIANTS_READY",
        "NO_APPLICABLE_MOVE_PROBE_REQUIRES_EXPECTED_PRESSURE_CONTRACT",
        "NO_NEW_ACTIVE_OBJECTS",
        "NO_REGISTRY_SWAP",
        "NO_SCHEMA_ARCHIVE_SWAP",
        "NO_ADMISSIBILITY_SURFACE_SWAP",
        "NO_SUITE_RUN",
        "NO_MOVE_ADDITION",
        "NO_SCHEMA_INVENTION",
        "NO_TAXONOMY_INVENTION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_RUNTIME_PATCH",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_declared_state_variant_rules_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_DECLARED_STATE_VARIANT_RULES_RECEIPT",
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
        "source_reachability_receipt_id": SOURCE_REACHABILITY_RECEIPT_ID,
        "acceptance_gate_results": {
            "STATE_VARIANTS_0_REACHABILITY_RECEIPT_CONSUMED": gate == "PASS",
            "STATE_VARIANTS_1_CLEAN_SMOKE_STATE_CONSUMED": gate == "PASS",
            "STATE_VARIANTS_2_RULES_EMITTED": gate == "PASS",
            "STATE_VARIANTS_3_ALLOWED_CATALOG_EMITTED": gate == "PASS",
            "STATE_VARIANTS_4_FORBIDDEN_CATALOG_EMITTED": gate == "PASS",
            "STATE_VARIANTS_5_DERIVATION_TEMPLATE_EMITTED": gate == "PASS",
            "STATE_VARIANTS_6_EXPECTED_PRESSURE_CONTRACT_NEXT": gate == "PASS",
            "STATE_VARIANTS_7_NO_SUITE_RUN": gate == "PASS",
            "STATE_VARIANTS_8_NO_RUNTIME_PATCH": gate == "PASS",
            "STATE_VARIANTS_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_state_variant_rules_summary": {
            "status": status,
            "state_variant_rules_done": gate == "PASS",
            "allowed_variant_count": rollup["allowed_variant_count"],
            "first_suite_variant_count": rollup["first_suite_variant_count"],
            "forbidden_variant_count": rollup["forbidden_variant_count"],
            "special_expected_pressure_variant_count": rollup["special_expected_pressure_variant_count"],
            "ready_for_expected_pressure_case_contract": gate == "PASS",
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
            "hidden_next_command": False,
            "c8_authorized": False,
            "reason_codes": reason_codes,
        },
        "output_artifacts": {
            "basis": rel(BASIS_PATH),
            "rules": rel(RULES_PATH),
            "allowed_variant_catalog": rel(VARIANT_CATALOG_PATH),
            "forbidden_variant_catalog": rel(FORBIDDEN_VARIANTS_PATH),
            "state_derivation_template": rel(STATE_DERIVATION_TEMPLATE_PATH),
            "compact_suite_shape": rel(COMPACT_SUITE_SHAPE_PATH),
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
    print(f"runtime_state_variant_rules_receipt_id={receipt_id}")
    print(f"runtime_state_variant_rules_receipt_path={rel(receipt_path)}")
    print(f"runtime_state_variant_rules_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
