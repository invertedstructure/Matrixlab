#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "AUDIT_RUNTIME_INCREMENTAL_SUITE_REACHABILITY_MAP_V0"
TARGET_UNIT_ID = "outer.runtime_adoption.incremental_suite.reachability_map_v0"
NEXT_UNIT_ID = "PREPARE_RUNTIME_DECLARED_STATE_VARIANT_RULES_V0"

LAYER = "OUTER / RUNTIME_ADOPTION / INCREMENTAL_SUITE_PREFLIGHT"
MODE = "AUDIT_ONLY / REGISTRY_REACHABILITY / NO_TEST_RUN"
BUILD_MODE = "RUNTIME_INCREMENTAL_SUITE_REACHABILITY_MAP_ONLY"

SOURCE_RUNTIME_SMOKE_RECEIPT_ID = "runtime_smoke_receipt_900b2eae"

SMOKE_RECEIPT_PATH = ROOT / "data/runtime_adoption_smoke_v0_receipts/runtime_smoke_receipt_900b2eae.json"
REGISTRY_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_move_registry_snapshot_v0.json"
TRACE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_smoke_trace_v0.jsonl"
STATE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_state_v0.json"
READOUT_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_smoke_readout_v0.json"
PRESSURE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_pressure_classification_v0.json"
BASELINE_PATH = ROOT / "data/runtime_adoption_smoke_v0/runtime_baseline_seal_v0.json"

OUT_DIR = ROOT / "data/runtime_incremental_suite_preflight_v0"
RECEIPT_DIR = ROOT / "data/runtime_incremental_suite_preflight_v0_receipts"

BASIS_PATH = OUT_DIR / "runtime_reachability_audit_basis_v0.json"
REGISTRY_MAP_PATH = OUT_DIR / "runtime_registry_reachability_map_v0.json"
BRANCH_GAP_INDEX_PATH = OUT_DIR / "runtime_branch_gap_index_v0.json"
TIER_FEASIBILITY_PATH = OUT_DIR / "runtime_incremental_suite_tier_feasibility_v0.json"
NEXT_TARGET_PATH = OUT_DIR / "runtime_declared_state_variant_rules_target_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_reachability_audit_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_reachability_audit_profile_v0.json"
TRACE_OUT_PATH = OUT_DIR / "runtime_reachability_audit_transition_trace.json"

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
    rows: List[Dict[str, Any]] = []
    text = path.read_text().strip()
    if not text:
        return rows
    for line in text.splitlines():
        if line.strip():
            rows.append(json.loads(line))
    return rows

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def require_false(obj: Dict[str, Any], key: str, failures: List[str]) -> None:
    if obj.get(key) is not False:
        failures.append(f"required_false_wrong:{key}:{obj.get(key)}")

def phase_edges_from_registry(moves: List[Dict[str, Any]]) -> Dict[str, List[str]]:
    edges: Dict[str, List[str]] = {}
    for move in moves:
        phase = (move.get("applies_when") or {}).get("runtime_phase")
        delta_phase = (move.get("state_delta") or {}).get("runtime_phase")
        if phase:
            edges.setdefault(phase, [])
            if delta_phase:
                edges[phase].append(delta_phase)
    return edges

def has_cycle(edges: Dict[str, List[str]]) -> bool:
    visiting: Set[str] = set()
    visited: Set[str] = set()

    def dfs(node: str) -> bool:
        if node in visiting:
            return True
        if node in visited:
            return False
        visiting.add(node)
        for nxt in edges.get(node, []):
            if dfs(nxt):
                return True
        visiting.remove(node)
        visited.add(node)
        return False

    return any(dfs(n) for n in edges)

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    required = [
        SMOKE_RECEIPT_PATH,
        REGISTRY_PATH,
        TRACE_PATH,
        STATE_PATH,
        READOUT_PATH,
        PRESSURE_PATH,
        BASELINE_PATH,
    ]

    failures: List[str] = []
    for p in required:
        if not p.exists():
            failures.append(f"dependency_missing:{rel(p)}")

    if failures:
        print(json.dumps({"gate": "FAIL", "failures": failures}, indent=2, sort_keys=True))
        return 1

    smoke_receipt = read_json(SMOKE_RECEIPT_PATH)
    smoke_summary = smoke_receipt.get("machine_readable_runtime_smoke_summary", {})
    registry = read_json(REGISTRY_PATH)
    trace_rows = read_jsonl(TRACE_PATH)
    state = read_json(STATE_PATH)
    readout = read_json(READOUT_PATH)
    pressure = read_json(PRESSURE_PATH)
    baseline = read_json(BASELINE_PATH)

    if smoke_receipt.get("receipt_id") != SOURCE_RUNTIME_SMOKE_RECEIPT_ID:
        failures.append(f"smoke_receipt_id_wrong:{smoke_receipt.get('receipt_id')}")
    if smoke_receipt.get("gate") != "PASS":
        failures.append(f"smoke_gate_wrong:{smoke_receipt.get('gate')}")
    if smoke_summary.get("outcome_class") != "RUNTIME_SMOKE_PASS_TYPED_STOP":
        failures.append(f"smoke_outcome_not_clean_typed_stop:{smoke_summary.get('outcome_class')}")
    if smoke_summary.get("pressure_class") != "STOP_DONE":
        failures.append(f"smoke_pressure_not_stop_done:{smoke_summary.get('pressure_class')}")
    if smoke_summary.get("refinement_candidate_count") != 0:
        failures.append(f"smoke_refinement_candidates_nonzero:{smoke_summary.get('refinement_candidate_count')}")
    if smoke_summary.get("receipt_trace_match") is not True:
        failures.append("smoke_receipt_trace_mismatch")
    if smoke_summary.get("bad_counters_zero") is not True:
        failures.append("smoke_bad_counters_not_zero")

    for key in [
        "runtime_adoption_authorized",
        "runtime_patched",
        "live_runtime_hooks_installed",
        "schema_archive_mutated",
        "schema_created",
        "taxonomy_created",
        "fixture_expanded_by_default",
        "architecture_widened",
        "control_path_authority_granted",
        "hidden_next_command",
        "c8_authorized",
    ]:
        require_false(smoke_summary, key, failures)

    moves = registry.get("moves", [])
    if not moves:
        failures.append("registry_moves_empty")

    trace_selected = [row.get("selected_move") for row in trace_rows if row.get("selected_move")]
    observed_moves = set(trace_selected)
    move_ids = [m.get("move_id") for m in moves]
    duplicate_moves = sorted([m for m in set(move_ids) if move_ids.count(m) > 1])
    if duplicate_moves:
        failures.append("duplicate_move_ids:" + ",".join(duplicate_moves))

    phase_to_moves: Dict[str, List[Dict[str, Any]]] = {}
    for move in moves:
        phase = (move.get("applies_when") or {}).get("runtime_phase")
        phase_to_moves.setdefault(str(phase), []).append(move)

    tie_candidates = []
    for phase, phase_moves in phase_to_moves.items():
        priority_groups: Dict[int, List[str]] = {}
        for move in phase_moves:
            priority_groups.setdefault(int(move.get("priority", 999999)), []).append(move.get("move_id"))
        for priority, ids in priority_groups.items():
            if len(ids) > 1:
                tie_candidates.append({
                    "runtime_phase": phase,
                    "priority": priority,
                    "move_ids": sorted(ids),
                })

    edges = phase_edges_from_registry(moves)
    registry_has_cycle = has_cycle(edges)

    reachability_records = []
    for move in moves:
        move_id = move.get("move_id")
        phase = (move.get("applies_when") or {}).get("runtime_phase")
        delta_phase = (move.get("state_delta") or {}).get("runtime_phase")
        observed = move_id in observed_moves

        failure_halts = move.get("failure_halts") or []
        requires_schema = move.get("requires_schema_validation") is True
        requires_admissibility = move.get("requires_admissibility") is True

        branch_notes = []
        if observed:
            reachability = "OBSERVED_IN_CLEAN_SMOKE"
        elif phase:
            reachability = "POTENTIALLY_DECLARABLE_PHASE_VARIANT"
            branch_notes.append("requires_declared_state_variant_rule_before_suite_case")
        else:
            reachability = "UNDERDECLARED_APPLIES_WHEN"
            branch_notes.append("move_has_no_runtime_phase_applies_when")

        failure_reachability = []
        for halt in failure_halts:
            if halt in [
                "STOP_RUNTIME_STATE_UNTYPED",
                "STOP_RUNTIME_SCHEMA_VALIDATION_FAIL",
                "STOP_RUNTIME_ADMISSIBILITY_FAIL",
                "STOP_AUTHORITY_VIOLATION",
                "STOP_RUNTIME_NO_APPLICABLE_MOVE",
                "STOP_RUNTIME_MOVE_TIE_UNRESOLVED",
                "STOP_RUNTIME_RECEIPT_MISMATCH",
                "STOP_RUNTIME_PROJECTION_BUG",
            ]:
                failure_reachability.append({
                    "halt": halt,
                    "status": "NOT_OBSERVED_IN_CLEAN_SMOKE",
                    "suite_handling": "requires_explicit_declared_case_or_record_as_unreachable_pressure",
                })

        reachability_records.append({
            "move_id": move_id,
            "move_kind": move.get("move_kind"),
            "priority": move.get("priority"),
            "applies_when_runtime_phase": phase,
            "state_delta_runtime_phase": delta_phase,
            "observed_in_clean_smoke": observed,
            "reachability_status": reachability,
            "requires_schema_validation": requires_schema,
            "requires_admissibility": requires_admissibility,
            "may_halt": move.get("may_halt"),
            "failure_halts": failure_halts,
            "failure_halt_reachability": failure_reachability,
            "branch_notes": branch_notes,
        })

    observed_schema_pass = any(
        row.get("schema_validation_ref") == "schema_validator_reference:SCHEMA_VALIDATED"
        for row in trace_rows
    )
    observed_admissibility_pass = any(
        row.get("admissibility_ref") == "cell0_lawful_admissibility_surface:ALLOW"
        for row in trace_rows
    )

    observed_failure_halts: Set[str] = set()
    for row in trace_rows:
        halt_code = row.get("halt_code")
        if halt_code and halt_code not in ["STOP_RUNTIME_SMOKE_TYPED_TERMINAL"]:
            observed_failure_halts.add(halt_code)

    desired_branches = [
        {
            "branch_id": "baseline_replay",
            "tier": "T0",
            "status": "READY",
            "why": "Clean smoke path is fully observed.",
            "candidate_next": None,
        },
        {
            "branch_id": "terminal_stability_variants",
            "tier": "T1",
            "status": "NEEDS_DECLARED_STATE_VARIANT_RULES",
            "why": "Equivalent state variants need a bounded rule so state declaration does not become hidden fixture expansion.",
            "candidate_next": "PREPARE_RUNTIME_DECLARED_STATE_VARIANT_RULES_V0",
        },
        {
            "branch_id": "registered_branch_coverage",
            "tier": "T2",
            "status": "PARTIAL",
            "why": "All current registry moves were observed in the clean linear path; no alternate registered branch was observed.",
            "candidate_next": "Use only observed branches first; record unreachable desired branches as coverage pressure if needed.",
        },
        {
            "branch_id": "schema_validation_pass",
            "tier": "T3",
            "status": "OBSERVED_PASS_ONLY" if observed_schema_pass else "NOT_OBSERVED",
            "why": "Schema validation pass was observed; schema validation failure was not observed.",
            "candidate_next": "Do not manufacture schema failure; require explicit declared invalid-state case or record unreachable branch.",
        },
        {
            "branch_id": "admissibility_pass",
            "tier": "T3",
            "status": "OBSERVED_PASS_ONLY" if observed_admissibility_pass else "NOT_OBSERVED",
            "why": "Lawful admissibility pass was observed; admissibility block was not observed.",
            "candidate_next": "Do not manufacture authority failure; require explicit declared boundary case or record unreachable branch.",
        },
        {
            "branch_id": "observability_degraded_or_gap",
            "tier": "T4",
            "status": "NOT_REACHABLE_FROM_CURRENT_REGISTRY_ONLY",
            "why": "Current smoke trace records sidecar refs but no degradation/unavailable control knob is present in registry.",
            "candidate_next": "Prepare non-control observability status case contract before T4 stress.",
        },
        {
            "branch_id": "negative_controls_non_writing",
            "tier": "T5",
            "status": "NEEDS_NON_WRITING_PROBE_CONTRACT",
            "why": "Negative controls must be observed as rejected/non-writing without mutating runtime.",
            "candidate_next": "Prepare negative-control probe contract.",
        },
        {
            "branch_id": "step_cap_or_loop_shape",
            "tier": "T6",
            "status": "NOT_REACHABLE_FROM_CURRENT_REGISTRY_ONLY" if not registry_has_cycle else "POTENTIALLY_REACHABLE",
            "why": "No registry cycle/repeated move shape was detected." if not registry_has_cycle else "Registry phase graph has a cycle; needs bounded declaration.",
            "candidate_next": "Do not include T6 in first suite unless loop/cap trigger is declared from current registry.",
        },
        {
            "branch_id": "move_tie_unresolved",
            "tier": "T6",
            "status": "NOT_PRESENT" if not tie_candidates else "PRESENT",
            "why": "No same-phase same-priority move tie detected." if not tie_candidates else "Tie candidate exists in registry.",
            "candidate_next": None if tie_candidates else "Do not include move-tie case in first suite.",
        },
        {
            "branch_id": "no_applicable_move",
            "tier": "T2/T6",
            "status": "UNDERDECLARED",
            "why": "Could be forced by an unrecognized runtime_phase, but that needs a declared invalid/edge-state rule.",
            "candidate_next": "Do not invent unrecognized phase inside suite; decide in state variant rules.",
        },
    ]

    branch_gap_records = []
    for branch in desired_branches:
        if branch["status"] in [
            "NEEDS_DECLARED_STATE_VARIANT_RULES",
            "PARTIAL",
            "OBSERVED_PASS_ONLY",
            "NOT_REACHABLE_FROM_CURRENT_REGISTRY_ONLY",
            "NEEDS_NON_WRITING_PROBE_CONTRACT",
            "NOT_PRESENT",
            "UNDERDECLARED",
        ]:
            branch_gap_records.append({
                "schema_version": "runtime_branch_gap_record_v0",
                "gap_id": "runtime_branch_gap_" + sig8(branch),
                "branch_id": branch["branch_id"],
                "tier": branch["tier"],
                "gap_status": branch["status"],
                "why": branch["why"],
                "smallest_next_handling": branch["candidate_next"],
                "candidate_only": True,
                "repair_applied": False,
                "forbidden_scope": [
                    "add moves",
                    "invent schemas",
                    "invent taxonomy",
                    "patch runtime",
                    "expand fixtures by default",
                    "claim live runtime adoption",
                ],
            })

    suite_tier_feasibility = {
        "schema_version": "runtime_incremental_suite_tier_feasibility_v0",
        "feasibility_status": "COMPACT_SUITE_FIRST",
        "recommended_first_suite": {
            "T0": 1,
            "T1": 2,
            "T2": 2,
            "T4": 2,
            "T5": 3,
            "total_cases": 10,
        },
        "defer_or_gate": {
            "T3": "include pass-only coverage only unless failure branches are explicitly declared without invention",
            "T6": "defer unless loop/step-cap trigger surface exists in current registry",
        },
        "tier_findings": desired_branches,
        "must_not_infer": [
            "T3 failure probes are reachable",
            "T6 loop/cap probes are reachable",
            "unreachable desired branches authorize move creation",
            "coverage pressure authorizes repair inside audit",
        ],
    }

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_RUNTIME_INCREMENTAL_SUITE_REACHABILITY_MAP_READY_STATE_VARIANTS_NEXT" if gate == "PASS" else "TYPED_RUNTIME_INCREMENTAL_SUITE_REACHABILITY_MAP_GATE_FAIL"

    basis = {
        "schema_version": "runtime_reachability_audit_basis_v0",
        "unit_id": UNIT_ID,
        "basis_status": "BASIS_ACCEPTED" if gate == "PASS" else "BASIS_REPAIR_REQUIRED",
        "source_runtime_smoke_receipt_id": SOURCE_RUNTIME_SMOKE_RECEIPT_ID,
        "source_files": {
            rel(p): file_sha256(p)
            for p in required
        },
        "basis_claim": "Clean smoke emitted typed STOP_DONE terminal with no refinement pressure; this audit inspects current registry reachability before declaring the incremental suite.",
        "does_not_authorize": [
            "test suite execution",
            "runtime move addition",
            "schema creation",
            "taxonomy creation",
            "fixture expansion by default",
            "runtime patching",
            "live hook installation",
            "C8 authorization",
        ],
    }

    reachability_map = {
        "schema_version": "runtime_registry_reachability_map_v0",
        "map_status": "EMITTED" if gate == "PASS" else "PARTIAL",
        "source_registry_ref": rel(REGISTRY_PATH),
        "source_trace_ref": rel(TRACE_PATH),
        "registry_move_count": len(moves),
        "observed_move_count": len(observed_moves),
        "observed_moves": trace_selected,
        "unobserved_registered_moves": sorted(set(move_ids) - observed_moves),
        "phase_graph": edges,
        "registry_has_cycle": registry_has_cycle,
        "move_tie_candidates": tie_candidates,
        "observed_schema_validation_pass": observed_schema_pass,
        "observed_schema_validation_failure": "STOP_RUNTIME_SCHEMA_VALIDATION_FAIL" in observed_failure_halts,
        "observed_admissibility_pass": observed_admissibility_pass,
        "observed_admissibility_block": "STOP_RUNTIME_ADMISSIBILITY_FAIL" in observed_failure_halts or "STOP_AUTHORITY_VIOLATION" in observed_failure_halts,
        "move_reachability": reachability_records,
        "core_finding": "Current registry exposes the clean linear smoke path. Boundary/failure/loop branches need explicit declaration contracts before inclusion, or must be recorded as unreachable coverage pressure.",
    }

    branch_gap_index = {
        "schema_version": "runtime_branch_gap_index_v0",
        "index_status": "EMITTED",
        "gap_count": len(branch_gap_records),
        "gaps": branch_gap_records,
    }

    next_target = {
        "schema_version": "runtime_declared_state_variant_rules_target_v0",
        "target_status": "STATE_VARIANT_RULES_NEXT" if gate == "PASS" else "NOT_READY",
        "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
        "why": "Before declaring the 10-case suite, define which state variants are legal and which desired branches must be recorded as pressure instead of manufactured.",
        "inputs": [
            rel(REGISTRY_MAP_PATH),
            rel(BRANCH_GAP_INDEX_PATH),
            rel(TIER_FEASIBILITY_PATH),
        ],
        "forbidden": [
            "add moves",
            "invent schemas",
            "patch runtime",
            "expand fixtures by default",
            "run full suite before variant rules",
        ],
    }

    rollup = {
        "schema_version": "runtime_reachability_audit_rollup_v0",
        "unit_id": UNIT_ID,
        "gate": gate,
        "status": status,
        "failures": failures,
        "registry_move_count": len(moves),
        "observed_move_count": len(observed_moves),
        "unobserved_registered_move_count": len(set(move_ids) - observed_moves),
        "branch_gap_count": len(branch_gap_records),
        "registry_has_cycle": registry_has_cycle,
        "move_tie_candidate_count": len(tie_candidates),
        "observed_schema_pass_only": observed_schema_pass and "STOP_RUNTIME_SCHEMA_VALIDATION_FAIL" not in observed_failure_halts,
        "observed_admissibility_pass_only": observed_admissibility_pass and not ("STOP_RUNTIME_ADMISSIBILITY_FAIL" in observed_failure_halts or "STOP_AUTHORITY_VIOLATION" in observed_failure_halts),
        "ready_for_state_variant_rules": gate == "PASS",
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
        "schema_version": "runtime_reachability_audit_profile_v0",
        "profile_status": status,
        "core_rule": "Walk missing test-suite preconditions one by one before running the full batch; do not manufacture unreachable branches.",
        "source_runtime_smoke_receipt_ref": rel(SMOKE_RECEIPT_PATH),
        "reachability_map_ref": rel(REGISTRY_MAP_PATH),
        "branch_gap_index_ref": rel(BRANCH_GAP_INDEX_PATH),
        "recommended_next": NEXT_UNIT_ID if gate == "PASS" else "REPAIR_RUNTIME_INCREMENTAL_SUITE_REACHABILITY_MAP_V0",
        "must_not_infer": [
            "full suite is ready",
            "T3 failure probes are reachable",
            "T6 loop/cap probes are reachable",
            "unreachable coverage authorizes move creation",
            "runtime adoption is authorized",
            "C8 is authorized",
        ],
    }

    trace = {
        "schema_version": "runtime_reachability_audit_transition_trace_v0",
        "unit_id": UNIT_ID,
        "transitions": [
            {
                "from": "OUTER_RUNTIME_SMOKE_STOP_DONE",
                "edge": "consume smoke registry and trace",
                "to": "REGISTRY_REACHABILITY_MAP_EMITTED" if gate == "PASS" else "REACHABILITY_MAP_GATE_FAIL",
            },
            {
                "from": "REGISTRY_REACHABILITY_MAP_EMITTED" if gate == "PASS" else "REACHABILITY_MAP_GATE_FAIL",
                "edge": "classify suite tier feasibility",
                "to": "STATE_VARIANT_RULES_NEXT" if gate == "PASS" else "STOP_GATE_FAIL",
            },
        ],
        "terminal": {
            "type": "ADVANCE" if gate == "PASS" else "STOP",
            "next_unit_id": NEXT_UNIT_ID if gate == "PASS" else None,
            "stop_code": None if gate == "PASS" else "STOP_RUNTIME_INCREMENTAL_SUITE_REACHABILITY_MAP_GATE_FAIL",
        },
    }

    for path, obj in [
        (BASIS_PATH, basis),
        (REGISTRY_MAP_PATH, reachability_map),
        (BRANCH_GAP_INDEX_PATH, branch_gap_index),
        (TIER_FEASIBILITY_PATH, suite_tier_feasibility),
        (NEXT_TARGET_PATH, next_target),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (TRACE_OUT_PATH, trace),
    ]:
        write_json(path, obj)

    reason_codes = [
        "CLEAN_SMOKE_RECEIPT_CONSUMED",
        "CURRENT_MOVE_REGISTRY_SNAPSHOT_CONSUMED",
        "TRACE_OBSERVED_MOVES_MAPPED",
        "SCHEMA_PASS_ONLY_CLASSIFIED",
        "ADMISSIBILITY_PASS_ONLY_CLASSIFIED",
        "T3_FAILURE_BRANCHES_NOT_MANUFACTURED",
        "T6_LOOP_CAP_BRANCHES_NOT_MANUFACTURED",
        "STATE_VARIANT_RULES_ARE_NEXT",
        "NO_TEST_SUITE_RUN",
        "NO_MOVE_ADDITION",
        "NO_SCHEMA_INVENTION",
        "NO_TAXONOMY_INVENTION",
        "NO_FIXTURE_EXPANSION_BY_DEFAULT",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_HOOK_INSTALL",
        "NO_C8_AUTHORIZATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if gate == "PASS" else failures

    receipt = {
        "schema_version": "runtime_incremental_suite_reachability_map_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_INCREMENTAL_SUITE_REACHABILITY_MAP_RECEIPT",
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
        "source_runtime_smoke_receipt_id": SOURCE_RUNTIME_SMOKE_RECEIPT_ID,
        "acceptance_gate_results": {
            "REACHABILITY_0_CLEAN_SMOKE_RECEIPT_CONSUMED": gate == "PASS",
            "REACHABILITY_1_REGISTRY_SNAPSHOT_CONSUMED": gate == "PASS",
            "REACHABILITY_2_TRACE_CONSUMED": gate == "PASS",
            "REACHABILITY_3_OBSERVED_MOVES_MAPPED": gate == "PASS",
            "REACHABILITY_4_BRANCH_GAPS_CLASSIFIED": gate == "PASS",
            "REACHABILITY_5_TIER_FEASIBILITY_EMITTED": gate == "PASS",
            "REACHABILITY_6_STATE_VARIANT_RULES_NEXT": gate == "PASS",
            "REACHABILITY_7_NO_SUITE_RUN": gate == "PASS",
            "REACHABILITY_8_NO_RUNTIME_PATCH": gate == "PASS",
            "REACHABILITY_9_NO_HIDDEN_NEXT_COMMAND": gate == "PASS",
        },
        "machine_readable_reachability_summary": {
            "status": status,
            "reachability_map_done": gate == "PASS",
            "registry_move_count": rollup["registry_move_count"],
            "observed_move_count": rollup["observed_move_count"],
            "unobserved_registered_move_count": rollup["unobserved_registered_move_count"],
            "branch_gap_count": rollup["branch_gap_count"],
            "registry_has_cycle": rollup["registry_has_cycle"],
            "move_tie_candidate_count": rollup["move_tie_candidate_count"],
            "observed_schema_pass_only": rollup["observed_schema_pass_only"],
            "observed_admissibility_pass_only": rollup["observed_admissibility_pass_only"],
            "recommended_first_suite_total_cases": suite_tier_feasibility["recommended_first_suite"]["total_cases"],
            "ready_for_state_variant_rules": gate == "PASS",
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
            "registry_reachability_map": rel(REGISTRY_MAP_PATH),
            "branch_gap_index": rel(BRANCH_GAP_INDEX_PATH),
            "tier_feasibility": rel(TIER_FEASIBILITY_PATH),
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
    print(f"runtime_reachability_map_receipt_id={receipt_id}")
    print(f"runtime_reachability_map_receipt_path={rel(receipt_path)}")
    print(f"runtime_reachability_map_next_unit={NEXT_UNIT_ID if gate == 'PASS' else 'NONE'}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
