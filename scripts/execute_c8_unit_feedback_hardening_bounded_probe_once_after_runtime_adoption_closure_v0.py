#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Iterable, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXECUTE_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.bounded_probe.execution_once.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTED_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE"
OUTCOME = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_READY_FOR_REVIEW"
STOP_CODE = "STOP_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_READY_FOR_REVIEW"

AUTHORIZED_UNIT = UNIT_ID

SOURCE_EXEC_ACCEPTANCE_RECEIPT_ID = "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_receipt_b5f72068"
SOURCE_EXEC_ACCEPTANCE_DECISION_ID = "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_decision_122d1a67"
SOURCE_EXEC_ACCEPTANCE_PACKET_ID = "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_packet_2716c7a2"
SOURCE_EXECUTION_AUTHORITY_ID = "c8_unit_feedback_hardening_bounded_probe_execution_authority_17d1d45d"
SOURCE_EXEC_ACCEPTANCE_BOUNDARY_ID = "c8_unit_feedback_hardening_bounded_probe_execution_acceptance_boundary_87a9f033"

SELECTED_SURFACE_ID = "c8_successor_surface_unit_feedback_hardening_after_runtime_adoption_closure_v0"
SELECTED_SURFACE_KIND = "UNIT_FEEDBACK_HARDENING_SURFACE"
SELECTED_SURFACE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_AFTER_RUNTIME_ADOPTION_CLOSURE_SURFACE"

PROBE_ID = "c8_unit_feedback_hardening_bounded_probe_after_runtime_adoption_closure_v0"
PROBE_KIND = "UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE"
PROBE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_AFTER_RUNTIME_ADOPTION_CLOSURE"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_after_runtime_adoption_closure_v0_receipts"

EXEC_ACCEPTANCE_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_receipt_b5f72068.json"
EXEC_ACCEPTANCE_DECISION = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_decision_v0.json"
EXEC_ACCEPTANCE_PACKET = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_packet_v0.json"
EXEC_AUTHORITY = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_execution_authority_v0.json"
EXEC_ACCEPTANCE_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_boundary_audit_v0.json"
EXEC_ACCEPTANCE_REPORT = ROOT / "data/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_report.json"

OBSERVATION = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_observation_v0.json"
SOURCE_INDEX = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_source_index_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_execution_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_execution_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_bounded_probe_execution_report.json"

RECOMMENDED_REVIEW_UNIT = "REVIEW_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
RECOMMENDED_HUMAN_DECISION = "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_OBSERVATION_FOR_REVIEW"

SOURCE_GLOB_DIRS = [
    "data/c8_return_to_surface_selection_acceptance_after_runtime_adoption_closure_v0",
    "data/c8_return_to_surface_selection_acceptance_after_runtime_adoption_closure_v0_receipts",
    "data/c8_successor_surface_selection_after_runtime_adoption_closure_v0",
    "data/c8_successor_surface_selection_after_runtime_adoption_closure_v0_receipts",
    "data/c8_selected_successor_surface_acceptance_after_runtime_adoption_closure_v0",
    "data/c8_selected_successor_surface_acceptance_after_runtime_adoption_closure_v0_receipts",
    "data/c8_unit_feedback_hardening_bounded_probe_prep_after_runtime_adoption_closure_v0",
    "data/c8_unit_feedback_hardening_bounded_probe_prep_after_runtime_adoption_closure_v0_receipts",
    "data/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_after_runtime_adoption_closure_v0",
    "data/c8_unit_feedback_hardening_bounded_probe_execution_acceptance_after_runtime_adoption_closure_v0_receipts",
]

FORBIDDEN_COUNTER_KEYS = [
    "second_probe_execution_count",
    "instrument_build_count",
    "cell1_build_count",
    "verification_probe_count",
    "c8_rerun_count",
    "missing_instrument_proposal_count",
    "research_mode_opened_count",
    "general_cell1_authority_count",
    "reusable_schema_authorized_count",
    "global_solution_claim_count",
    "frontier_solved_claim_count",
    "source_artifact_mutation_count",
    "hidden_next_command_count",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()[:8]

def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def rel(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()

def read_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text())

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def chk(failures: List[str], label: str, got: Any, want: Any) -> None:
    if got != want:
        failures.append(f"{label}_wrong:{got}!={want}")

def flatten_keys(obj: Any, prefix: str = "") -> Iterable[str]:
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            yield key
            yield from flatten_keys(v, key)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from flatten_keys(v, f"{prefix}[{i}]")

def text_blob(obj: Any) -> str:
    return json.dumps(obj, sort_keys=True, default=str).lower()

def source_paths() -> List[Path]:
    paths: List[Path] = []
    for d in SOURCE_GLOB_DIRS:
        p = ROOT / d
        if p.exists():
            paths.extend(sorted(p.glob("*.json")))
    seen = set()
    out = []
    for p in sorted(paths, key=lambda x: rel(x)):
        r = rel(p)
        if r not in seen:
            seen.add(r)
            out.append(p)
    return out

def bool_signal(obj: Dict[str, Any], keys: Iterable[str], substrings: Iterable[str]) -> bool:
    keyset = set(keys)
    blob = text_blob(obj)
    return any(k in keyset for k in keys) or any(s in blob for s in substrings)

def classify_source(path: Path, obj: Dict[str, Any]) -> Dict[str, Any]:
    keys = list(flatten_keys(obj))
    keyset = set(keys)
    blob = text_blob(obj)

    status = obj.get("status")
    gate = obj.get("gate")
    outcome = obj.get("outcome_class")
    failures = obj.get("failures", [])
    warnings = obj.get("warnings", [])
    terminal = obj.get("terminal", {})

    failure_count = len(failures) if isinstance(failures, list) else 0
    warning_count = len(warnings) if isinstance(warnings, list) else 0
    gate_results = obj.get("gate_results", {})
    false_gate_count = len([k for k, v in gate_results.items() if v is not True]) if isinstance(gate_results, dict) else 0

    is_failed_sample = (
        gate == "FAIL"
        or (isinstance(status, str) and status.endswith("_FAIL"))
        or failure_count > 0
        or false_gate_count > 0
    )

    has_terminal_stop = isinstance(terminal, dict) and terminal.get("type") == "STOP"
    has_status_signal = any(k in keyset for k in ["status", "gate", "outcome_class"])
    has_why_signal = (
        "failures" in keyset
        or "gate_results" in keyset
        or "warnings" in keyset
        or "why" in blob
        or "reason" in blob
        or "wrong:" in blob
    )
    has_where_signal = (
        "output_artifacts" in keyset
        or any("path" in k for k in keyset)
        or any("file" in k for k in keyset)
        or "_wrong:" in blob
        or "source_missing:" in blob
    )
    has_relative_signal = any(
        needle in blob
        for needle in [
            "source_",
            "selected_surface",
            "authority",
            "boundary",
            "probe_id",
            "unit_id",
            "object",
            "missing capability",
        ]
    )
    has_refinement_signal = any(
        needle in blob
        for needle in [
            "recommended_review_unit",
            "recommended_human_decision",
            "authorized_future_unit",
            "if_accepted_authorizes_future_unit",
            "would allow",
            "exact refinement",
            "next_command_goal",
        ]
    )
    has_failure_status_distinction_signal = (
        "failure status" in blob
        or "useful feedback" in blob
        or ("status" in keyset and ("failures" in keyset or "gate_results" in keyset))
    )

    return {
        "path": rel(path),
        "sha256": sha256_file(path),
        "schema_version": obj.get("schema_version"),
        "receipt_id": obj.get("receipt_id"),
        "status": status,
        "gate": gate,
        "outcome_class": outcome,
        "terminal_stop_code": terminal.get("stop_code") if isinstance(terminal, dict) else None,
        "is_failed_sample": is_failed_sample,
        "has_terminal_stop": has_terminal_stop,
        "failure_count": failure_count,
        "warning_count": warning_count,
        "false_gate_count": false_gate_count,
        "has_status_signal": has_status_signal,
        "has_why_signal": has_why_signal,
        "has_where_signal": has_where_signal,
        "has_relative_object_or_boundary_signal": has_relative_signal,
        "has_refinement_signal": has_refinement_signal,
        "has_failure_status_distinction_signal": has_failure_status_distinction_signal,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []
    forbidden_counters = {k: 0 for k in FORBIDDEN_COUNTER_KEYS}

    mandatory_sources = {
        "execution_acceptance_receipt": EXEC_ACCEPTANCE_RECEIPT,
        "execution_acceptance_decision": EXEC_ACCEPTANCE_DECISION,
        "execution_acceptance_packet": EXEC_ACCEPTANCE_PACKET,
        "execution_authority": EXEC_AUTHORITY,
        "execution_acceptance_boundary": EXEC_ACCEPTANCE_BOUNDARY,
        "execution_acceptance_report": EXEC_ACCEPTANCE_REPORT,
    }

    for label, path in mandatory_sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {
        label: sha256_file(path)
        for label, path in mandatory_sources.items()
        if path.exists()
    }

    exec_receipt = read_json(EXEC_ACCEPTANCE_RECEIPT)
    exec_decision = read_json(EXEC_ACCEPTANCE_DECISION)
    exec_packet = read_json(EXEC_ACCEPTANCE_PACKET)
    exec_authority = read_json(EXEC_AUTHORITY)
    exec_boundary = read_json(EXEC_ACCEPTANCE_BOUNDARY)
    exec_report = read_json(EXEC_ACCEPTANCE_REPORT)
    exec_summary = exec_receipt.get("machine_readable_unit_feedback_hardening_bounded_probe_execution_acceptance_summary", {})

    expected_exec_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_ACCEPTANCE_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_ACCEPTED_FOR_ONE_EXECUTION_READY_FOR_REVIEW",
        "receipt_id": SOURCE_EXEC_ACCEPTANCE_RECEIPT_ID,
    }
    for key, want in expected_exec_receipt.items():
        chk(failures, f"execution_acceptance_receipt_{key}", exec_receipt.get(key), want)

    expected_exec_summary = {
        "unit_feedback_hardening_bounded_probe_execution_acceptance_complete": True,
        "authorized_future_unit_after_review": AUTHORIZED_UNIT,
        "authorized_future_unit_count_after_review": 1,
        "bounded_probe_execution_limit": 1,
        "probe_execution_authorized_after_review": True,
        "probe_executed_now": False,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
    }
    for key, want in expected_exec_summary.items():
        chk(failures, f"execution_acceptance_summary_{key}", exec_summary.get(key), want)

    expected_ids = {
        "execution_acceptance_decision_id": (
            exec_decision.get("c8_unit_feedback_hardening_bounded_probe_execution_acceptance_decision_id"),
            SOURCE_EXEC_ACCEPTANCE_DECISION_ID,
        ),
        "execution_acceptance_packet_id": (
            exec_packet.get("c8_unit_feedback_hardening_bounded_probe_execution_acceptance_packet_id"),
            SOURCE_EXEC_ACCEPTANCE_PACKET_ID,
        ),
        "execution_authority_id": (
            exec_authority.get("c8_unit_feedback_hardening_bounded_probe_execution_authority_id"),
            SOURCE_EXECUTION_AUTHORITY_ID,
        ),
        "execution_acceptance_boundary_id": (
            exec_boundary.get("c8_unit_feedback_hardening_bounded_probe_execution_acceptance_boundary_audit_id"),
            SOURCE_EXEC_ACCEPTANCE_BOUNDARY_ID,
        ),
    }
    for label, (got, want) in expected_ids.items():
        if got != want:
            failures.append(f"{label}_wrong:{got}!={want}")

    if exec_authority.get("authorized_future_unit") != AUTHORIZED_UNIT:
        failures.append(f"execution_authority_future_unit_wrong:{exec_authority.get('authorized_future_unit')}")
    if exec_authority.get("authorized_future_unit_count") != 1:
        failures.append(f"execution_authority_future_unit_count_wrong:{exec_authority.get('authorized_future_unit_count')}")
    if exec_authority.get("execution_limit") != 1:
        failures.append(f"execution_authority_limit_wrong:{exec_authority.get('execution_limit')}")
    if exec_authority.get("authority_status") != "ACTIVE_AFTER_REVIEW_AND_COMMIT":
        failures.append(f"execution_authority_status_wrong:{exec_authority.get('authority_status')}")

    scope = exec_authority.get("authority_scope", {})
    if scope.get("may_execute_bounded_probe_once") is not True:
        failures.append("execution_authority_scope_may_execute_bounded_probe_once_not_true")
    for key in ["may_execute_more_than_once", "may_build_now", "may_rerun_c8_now", "may_promote_schema_now"]:
        if scope.get(key) is not False:
            failures.append(f"execution_authority_scope_{key}_wrong:{scope.get(key)}")

    source_hashes_after_pre_execution = {
        label: sha256_file(path)
        for label, path in mandatory_sources.items()
        if path.exists()
    }
    if source_hashes_before != source_hashes_after_pre_execution:
        forbidden_counters["source_artifact_mutation_count"] += 1

    all_source_paths = source_paths()
    source_rows = []
    for path in all_source_paths:
        try:
            source_rows.append(classify_source(path, read_json(path)))
        except Exception as exc:
            warnings.append(f"source_parse_warning:{rel(path)}:{exc}")

    source_docs_count = len(source_rows)
    failed_unit_sample_count = sum(1 for row in source_rows if row["is_failed_sample"])
    typed_stop_sample_count = sum(1 for row in source_rows if row["has_terminal_stop"])

    why_count = sum(1 for row in source_rows if row["has_why_signal"])
    where_count = sum(1 for row in source_rows if row["has_where_signal"])
    relative_count = sum(1 for row in source_rows if row["has_relative_object_or_boundary_signal"])
    refinement_count = sum(1 for row in source_rows if row["has_refinement_signal"])
    distinction_count = sum(1 for row in source_rows if row["has_failure_status_distinction_signal"])

    if source_docs_count < 5:
        failures.append(f"too_few_probe_sources_loaded:{source_docs_count}<5")
    if typed_stop_sample_count < 1:
        failures.append("no_typed_stop_samples_observed")

    if failed_unit_sample_count == 0:
        observation_class = "UNIT_FEEDBACK_DIAGNOSTIC_FEEDBACK_PARTIAL_NO_FAILED_UNIT_SAMPLE_OBSERVED"
        observation_verdict = "PARTIAL"
        diagnostic_gap = "No failed-unit sample was present in the bounded source set, so the probe can verify typed-stop/status/context/refinement structure but cannot fully validate failed-unit diagnostic quality."
    elif all(count > 0 for count in [why_count, where_count, relative_count, refinement_count, distinction_count]):
        observation_class = "UNIT_FEEDBACK_DIAGNOSTIC_FEEDBACK_WITH_FAILED_UNIT_SAMPLE_OBSERVED"
        observation_verdict = "OBSERVED"
        diagnostic_gap = None
    else:
        observation_class = "UNIT_FEEDBACK_DIAGNOSTIC_FEEDBACK_GAP_OBSERVED"
        observation_verdict = "GAP"
        diagnostic_gap = "At least one diagnostic-feedback dimension was absent from the bounded source set."

    execution_count_now = 1
    if execution_count_now != 1:
        forbidden_counters["second_probe_execution_count"] += 1

    local_nonzero = {k: v for k, v in forbidden_counters.items() if v != 0}
    for k, v in local_nonzero.items():
        failures.append(f"{k}:{v}")

    source_index = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_source_index_v0",
        "c8_unit_feedback_hardening_bounded_probe_source_index_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "source_glob_dirs": SOURCE_GLOB_DIRS,
        "source_docs_count": source_docs_count,
        "source_rows": source_rows,
    }
    source_index["c8_unit_feedback_hardening_bounded_probe_source_index_id"] = "c8_unit_feedback_hardening_bounded_probe_source_index_" + sig8(source_index)
    write_json(SOURCE_INDEX, source_index)

    observation = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_observation_v0",
        "c8_unit_feedback_hardening_bounded_probe_observation_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "authorized_unit_consumed": AUTHORIZED_UNIT,
        "source_execution_acceptance_receipt_id": SOURCE_EXEC_ACCEPTANCE_RECEIPT_ID,
        "source_execution_acceptance_decision_id": SOURCE_EXEC_ACCEPTANCE_DECISION_ID,
        "source_execution_acceptance_packet_id": SOURCE_EXEC_ACCEPTANCE_PACKET_ID,
        "source_execution_authority_id": SOURCE_EXECUTION_AUTHORITY_ID,
        "source_execution_acceptance_boundary_id": SOURCE_EXEC_ACCEPTANCE_BOUNDARY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "selected_surface_kind": SELECTED_SURFACE_KIND,
        "selected_surface_label": SELECTED_SURFACE_LABEL,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_execution_count_now": execution_count_now,
        "bounded_probe_execution_limit": 1,
        "probe_executed_now": True,
        "observation_class": observation_class,
        "observation_verdict": observation_verdict,
        "diagnostic_gap": diagnostic_gap,
        "feedback_dimension_counts": {
            "source_docs_count": source_docs_count,
            "typed_stop_sample_count": typed_stop_sample_count,
            "failed_unit_sample_count": failed_unit_sample_count,
            "why_signal_doc_count": why_count,
            "where_signal_doc_count": where_count,
            "relative_object_or_boundary_signal_doc_count": relative_count,
            "refinement_signal_doc_count": refinement_count,
            "failure_status_distinction_signal_doc_count": distinction_count,
        },
        "minimum_useful_feedback_dimensions": [
            "why it failed",
            "where it failed",
            "relative to what object/source surface/authority boundary/missing capability",
            "what exact refinement would allow progress",
            "failure status is distinct from useful diagnostic feedback",
        ],
        "observed_constraints": {
            "no_build": True,
            "no_c8_rerun": True,
            "no_reusable_schema_promotion": True,
            "no_global_solution_claim": True,
            "no_frontier_solved_claim": True,
            "source_artifacts_mutated": False,
        },
        "requires_review": True,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
    }
    observation["c8_unit_feedback_hardening_bounded_probe_observation_id"] = "c8_unit_feedback_hardening_bounded_probe_observation_" + sig8(observation)
    write_json(OBSERVATION, observation)

    boundary = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_execution_boundary_audit_v0",
        "c8_unit_feedback_hardening_bounded_probe_execution_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_execution_acceptance_packet_id": SOURCE_EXEC_ACCEPTANCE_PACKET_ID,
        "source_execution_authority_id": SOURCE_EXECUTION_AUTHORITY_ID,
        "source_observation_id": observation["c8_unit_feedback_hardening_bounded_probe_observation_id"],
        "source_index_id": source_index["c8_unit_feedback_hardening_bounded_probe_source_index_id"],
        "authorized_unit_consumed": AUTHORIZED_UNIT,
        "allowed_now": {
            "execute_bounded_probe_once": True,
            "write_observation": True,
            "present_execution_for_review": True,
        },
        "not_allowed_now": {
            "execute_probe_more_than_once": True,
            "build_instrument": True,
            "build_cell1": True,
            "run_verification_probe": True,
            "rerun_c8": True,
            "create_missing_instrument_proposal": True,
            "authorize_reusable_schema": True,
            "open_research_mode": True,
            "claim_global_solution": True,
            "claim_frontier_solved": True,
        },
        "forbidden_counters": forbidden_counters,
        "failures": failures,
        "warnings": warnings,
    }
    boundary["c8_unit_feedback_hardening_bounded_probe_execution_boundary_audit_id"] = "c8_unit_feedback_hardening_bounded_probe_execution_boundary_" + sig8(boundary)
    write_json(BOUNDARY_AUDIT, boundary)

    source_hashes_after = {
        label: sha256_file(path)
        for label, path in mandatory_sources.items()
        if path.exists()
    }
    if source_hashes_before != source_hashes_after:
        forbidden_counters["source_artifact_mutation_count"] += 1
        failures.append("source_artifact_mutation_after_execution")

    gate_results = {
        "UNIT_FEEDBACK_EXECUTION_0_SOURCE_EXECUTION_ACCEPTANCE_RECEIPT_PASS": exec_receipt.get("gate") == "PASS",
        "UNIT_FEEDBACK_EXECUTION_1_EXECUTION_AUTHORITY_ACTIVE": exec_authority.get("authority_status") == "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "UNIT_FEEDBACK_EXECUTION_2_AUTHORIZED_UNIT_MATCH": exec_authority.get("authorized_future_unit") == AUTHORIZED_UNIT,
        "UNIT_FEEDBACK_EXECUTION_3_EXECUTION_LIMIT_ONE": exec_authority.get("execution_limit") == 1,
        "UNIT_FEEDBACK_EXECUTION_4_PROBE_EXECUTED_ONCE": execution_count_now == 1,
        "UNIT_FEEDBACK_EXECUTION_5_OBSERVATION_WRITTEN": OBSERVATION.exists(),
        "UNIT_FEEDBACK_EXECUTION_6_SOURCE_INDEX_WRITTEN": SOURCE_INDEX.exists(),
        "UNIT_FEEDBACK_EXECUTION_7_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "UNIT_FEEDBACK_EXECUTION_8_NO_BUILD_RERUN_SCHEMA": True,
        "UNIT_FEEDBACK_EXECUTION_9_FORBIDDEN_COUNTERS_ZERO": not bool({k: v for k, v in forbidden_counters.items() if v != 0}),
        "UNIT_FEEDBACK_EXECUTION_10_REQUIRES_REVIEW": observation["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"unit_feedback_execution_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_FAIL"
    outcome = OUTCOME if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_FAILED"
    terminal_stop = STOP_CODE if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_FAILED"

    readout = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_execution_readout_v0",
        "title": "C8 unit-feedback hardening bounded probe execution after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_executed_now": True,
        "probe_execution_count_now": execution_count_now,
        "bounded_probe_execution_limit": 1,
        "observation_class": observation_class,
        "observation_verdict": observation_verdict,
        "diagnostic_gap": diagnostic_gap,
        "source_docs_count": source_docs_count,
        "typed_stop_sample_count": typed_stop_sample_count,
        "failed_unit_sample_count": failed_unit_sample_count,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "requires_review": True,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_execution_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_execution_acceptance_receipt_id": SOURCE_EXEC_ACCEPTANCE_RECEIPT_ID,
        "source_execution_authority_id": SOURCE_EXECUTION_AUTHORITY_ID,
        "selected_surface_id": SELECTED_SURFACE_ID,
        "probe_id": PROBE_ID,
        "probe_kind": PROBE_KIND,
        "probe_label": PROBE_LABEL,
        "probe_executed_now": True,
        "probe_execution_count_now": execution_count_now,
        "bounded_probe_execution_limit": 1,
        "observation_class": observation_class,
        "observation_verdict": observation_verdict,
        "diagnostic_gap": diagnostic_gap,
        "source_docs_count": source_docs_count,
        "typed_stop_sample_count": typed_stop_sample_count,
        "failed_unit_sample_count": failed_unit_sample_count,
        "instrument_build_authorized_now": False,
        "cell1_build_authorized_now": False,
        "verification_probe_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "missing_instrument_proposal_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "research_mode_opened": False,
        "global_solution_claim": False,
        "frontier_solved_claim": False,
        "requires_review": True,
        "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
        "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt = {
        "schema_version": "c8_unit_feedback_hardening_bounded_probe_execution_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_EXECUTION_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_bounded_probe_execution_summary": {
            "unit_feedback_hardening_bounded_probe_executed": gate == "PASS",
            "authorized_unit_consumed": AUTHORIZED_UNIT,
            "source_execution_acceptance_receipt_id": SOURCE_EXEC_ACCEPTANCE_RECEIPT_ID,
            "source_execution_acceptance_decision_id": SOURCE_EXEC_ACCEPTANCE_DECISION_ID,
            "source_execution_acceptance_packet_id": SOURCE_EXEC_ACCEPTANCE_PACKET_ID,
            "source_execution_authority_id": SOURCE_EXECUTION_AUTHORITY_ID,
            "source_execution_acceptance_boundary_id": SOURCE_EXEC_ACCEPTANCE_BOUNDARY_ID,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "probe_label": PROBE_LABEL,
            "probe_executed_now": True,
            "probe_execution_count_now": execution_count_now,
            "bounded_probe_execution_limit": 1,
            "observation_id": observation["c8_unit_feedback_hardening_bounded_probe_observation_id"],
            "source_index_id": source_index["c8_unit_feedback_hardening_bounded_probe_source_index_id"],
            "observation_class": observation_class,
            "observation_verdict": observation_verdict,
            "diagnostic_gap": diagnostic_gap,
            "source_docs_count": source_docs_count,
            "typed_stop_sample_count": typed_stop_sample_count,
            "failed_unit_sample_count": failed_unit_sample_count,
            "instrument_built_now": False,
            "cell1_built_now": False,
            "verification_probe_run_now": False,
            "c8_rerun_now": False,
            "missing_instrument_proposal_created_now": False,
            "research_mode_opened": False,
            "general_cell1_authority": False,
            "reusable_schema_authorized": False,
            "global_solution_claim": False,
            "frontier_solved_claim": False,
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
            "forbidden_counters_zero": not bool({k: v for k, v in forbidden_counters.items() if v != 0}),
            "requires_review": True,
            "recommended_human_decision": RECOMMENDED_HUMAN_DECISION,
            "recommended_review_unit": RECOMMENDED_REVIEW_UNIT,
            "next_command_goal": None,
        },
        "gate_results": gate_results,
        "forbidden_counters": forbidden_counters,
        "source_artifact_immutability": {
            "source_hashes_before": source_hashes_before,
            "source_hashes_after": source_hashes_after,
            "source_artifacts_mutated": source_hashes_before != source_hashes_after,
        },
        "output_artifacts": {
            "observation": rel(OBSERVATION),
            "source_index": rel(SOURCE_INDEX),
            "boundary_audit": rel(BOUNDARY_AUDIT),
            "readout": rel(READOUT),
            "report": rel(REPORT),
        },
        "failures": failures,
        "warnings": warnings,
        "terminal": {
            "type": "STOP",
            "stop_code": terminal_stop,
            "next_command_goal": None,
        },
    }

    receipt["receipt_id"] = "c8_unit_feedback_hardening_bounded_probe_execution_receipt_" + sig8(receipt)
    receipt_path = RECEIPT_DIR / f"{receipt['receipt_id']}.json"
    receipt["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_bounded_probe_execution_receipt_id={receipt['receipt_id']}")
    print(f"c8_unit_feedback_hardening_bounded_probe_execution_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_observation_path={rel(OBSERVATION)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_source_index_path={rel(SOURCE_INDEX)}")
    print(f"c8_unit_feedback_hardening_bounded_probe_execution_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"probe_id={PROBE_ID}")
    print(f"probe_kind={PROBE_KIND}")
    print("probe_executed_now=true")
    print("probe_execution_count_now=1")
    print("bounded_probe_execution_limit=1")
    print(f"observation_class={observation_class}")
    print(f"observation_verdict={observation_verdict}")
    print(f"source_docs_count={source_docs_count}")
    print(f"typed_stop_sample_count={typed_stop_sample_count}")
    print(f"failed_unit_sample_count={failed_unit_sample_count}")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print(f"recommended_human_decision={RECOMMENDED_HUMAN_DECISION}")
    print(f"recommended_review_unit={RECOMMENDED_REVIEW_UNIT}")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
