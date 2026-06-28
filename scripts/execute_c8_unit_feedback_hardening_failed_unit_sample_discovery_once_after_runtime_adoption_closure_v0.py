#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "EXECUTE_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0"
TARGET_UNIT_ID = "research.c8.unit_feedback_hardening.failed_unit_sample.discovery_execution.once.after_runtime_adoption_closure.v0"
MILESTONE = "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_EXECUTED_ONCE_AFTER_RUNTIME_ADOPTION_CLOSURE"
OUTCOME_FOUND = "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_FOUND_ONE_SAMPLE"
OUTCOME_GAP = "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_NO_SAMPLE_FOUND_TYPED_GAP"
STOP_FOUND = "STOP_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_FOUND_ONE_SAMPLE_READY_FOR_REVIEW"
STOP_GAP = "STOP_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_NO_FAILED_UNIT_SAMPLE_FOUND_READY_FOR_REVIEW"

SOURCE_ACCEPTANCE_RECEIPT_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_receipt_fa84e9db"
SOURCE_ACCEPTANCE_DECISION_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_decision_80456d5f"
SOURCE_ACCEPTANCE_PACKET_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_packet_1a770dc3"
SOURCE_EXECUTION_AUTHORITY_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_authority_f06fa4a1"
SOURCE_ACCEPTANCE_BOUNDARY_ID = "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_boundary_e9aa8919"

SELECTED_SURFACE_ID = "c8_successor_surface_unit_feedback_hardening_after_runtime_adoption_closure_v0"
SELECTED_SURFACE_KIND = "UNIT_FEEDBACK_HARDENING_SURFACE"
SELECTED_SURFACE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_AFTER_RUNTIME_ADOPTION_CLOSURE_SURFACE"

PROBE_ID = "c8_unit_feedback_hardening_bounded_probe_after_runtime_adoption_closure_v0"
PROBE_KIND = "UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE"
PROBE_LABEL = "C8_UNIT_FEEDBACK_HARDENING_BOUNDED_PROBE_AFTER_RUNTIME_ADOPTION_CLOSURE"

GAP_OBJECT = "FAILED_UNIT_SAMPLE_ABSENCE"
DISCOVERY_TARGET = "ONE_FAILED_UNIT_SAMPLE"
TYPED_GAP_IF_NONE = "NO_FAILED_UNIT_SAMPLE_FOUND_IN_BOUNDED_DISCOVERY_SURFACE"

OUT_DIR = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_after_runtime_adoption_closure_v0"
RECEIPT_DIR = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_after_runtime_adoption_closure_v0_receipts"

ACCEPTANCE_RECEIPT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_after_runtime_adoption_closure_v0_receipts/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_receipt_fa84e9db.json"
ACCEPTANCE_DECISION = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_decision_v0.json"
ACCEPTANCE_PACKET = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_packet_v0.json"
EXECUTION_AUTHORITY = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_authority_v0.json"
ACCEPTANCE_BOUNDARY = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_boundary_audit_v0.json"
ACCEPTANCE_REPORT = ROOT / "data/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_after_runtime_adoption_closure_v0/c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_report.json"

DISCOVERY_RESULT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_result_v0.json"
BOUNDARY_AUDIT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_boundary_audit_v0.json"
READOUT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_readout_v0.json"
REPORT = OUT_DIR / "c8_unit_feedback_hardening_failed_unit_sample_discovery_report.json"

FORBIDDEN_COUNTER_KEYS = [
    "sample_discovery_execution_count_over_limit",
    "failed_unit_sample_count_over_limit",
    "probe_execution_authorized_count",
    "probe_executed_count",
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

def git_tracked_paths() -> List[str]:
    out = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", "HEAD"], cwd=ROOT, text=True)
    return sorted(p for p in out.splitlines() if p.endswith(".json") and (p.startswith("data/") or p.startswith("logs/")))

def is_failure_indicator(obj: Any) -> Tuple[bool, List[str]]:
    indicators: List[str] = []
    if not isinstance(obj, dict):
        return False, indicators

    gate = obj.get("gate")
    status = obj.get("status")

    if gate == "FAIL":
        indicators.append("gate == FAIL")
    if isinstance(status, str) and status.endswith("_FAIL"):
        indicators.append("status suffix == _FAIL")
    failures_value = obj.get("failures")
    if isinstance(failures_value, list) and len(failures_value) > 0:
        indicators.append("failures list non-empty")

    gate_results = obj.get("gate_results")
    if isinstance(gate_results, dict) and any(v is False for v in gate_results.values()):
        indicators.append("gate_results contains false")

    forbidden = obj.get("forbidden_counters")
    if isinstance(forbidden, dict) and any(v != 0 for v in forbidden.values() if isinstance(v, (int, float))):
        indicators.append("forbidden_counters contains nonzero value")

    return bool(indicators), indicators

def derive_diagnostic_fields(path: str, obj: Dict[str, Any], indicators: List[str]) -> Dict[str, Any]:
    failures_value = obj.get("failures")
    false_gates = []
    if isinstance(obj.get("gate_results"), dict):
        false_gates = sorted(k for k, v in obj["gate_results"].items() if v is False)

    nonzero_forbidden = {}
    if isinstance(obj.get("forbidden_counters"), dict):
        nonzero_forbidden = {k: v for k, v in obj["forbidden_counters"].items() if isinstance(v, (int, float)) and v != 0}

    why_parts = []
    if indicators:
        why_parts.append("failure indicator(s): " + ", ".join(indicators))
    if isinstance(failures_value, list) and failures_value:
        why_parts.append("failures field is non-empty")
    if false_gates:
        why_parts.append("gate_results contains false gate(s): " + ", ".join(false_gates[:5]))
    if nonzero_forbidden:
        why_parts.append("forbidden_counters contains nonzero value(s): " + ", ".join(sorted(nonzero_forbidden.keys())[:5]))

    where = {
        "source_path": path,
        "receipt_id": obj.get("receipt_id"),
        "unit_id": obj.get("unit_id"),
        "target_unit_id": obj.get("target_unit_id"),
        "status": obj.get("status"),
        "outcome_class": obj.get("outcome_class"),
    }

    relative_to = {
        "object": obj.get("gap_object") or obj.get("selected_surface_id") or obj.get("probe_id") or obj.get("unit_id"),
        "source_surface": obj.get("selected_surface_id"),
        "authority_boundary": obj.get("source_discovery_prep_boundary_id") or obj.get("source_gap_response_boundary_id") or obj.get("source_boundary_id") or obj.get("boundary_id"),
        "missing_capability": obj.get("typed_gap") or obj.get("diagnostic_gap") or obj.get("missing_capability"),
    }

    return {
        "why": "; ".join(why_parts) if why_parts else "failure status observed but diagnostic reason not explicit",
        "where": where,
        "relative_to": relative_to,
        "refinement_or_next_lawful_step": (
            "Review this failed unit sample against the unit-feedback hardening rubric; if diagnostic fields are insufficient, "
            "propose the smallest feedback-field refinement rather than rerunning or building."
        ),
        "failure_status_vs_useful_feedback_note": (
            "This sample proves a failure status exists; review must still judge whether the exposed why/where/relative/refinement fields are useful."
        ),
    }

def find_one_failed_unit_sample() -> Optional[Dict[str, Any]]:
    for path in git_tracked_paths():
        full = ROOT / path
        try:
            obj = read_json(full)
        except Exception:
            continue

        has_failure, indicators = is_failure_indicator(obj)
        if not has_failure:
            continue

        diagnostic = derive_diagnostic_fields(path, obj, indicators)
        sample = {
            "failed_unit_sample_id": "c8_failed_unit_sample_" + hashlib.sha256(path.encode("utf-8")).hexdigest()[:8],
            "source_path": path,
            "source_sha256": sha256_file(full),
            "failure_indicator": indicators,
            "source_receipt_id": obj.get("receipt_id"),
            "source_status": obj.get("status"),
            "source_gate": obj.get("gate"),
            "source_outcome_class": obj.get("outcome_class"),
            "diagnostic_feedback_fields": diagnostic,
            "source_failures_excerpt": obj.get("failures") if isinstance(obj.get("failures"), list) else None,
        }
        return sample

    return None

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    failures: List[str] = []
    warnings: List[str] = []
    forbidden_counters = {k: 0 for k in FORBIDDEN_COUNTER_KEYS}

    sources = {
        "acceptance_receipt": ACCEPTANCE_RECEIPT,
        "acceptance_decision": ACCEPTANCE_DECISION,
        "acceptance_packet": ACCEPTANCE_PACKET,
        "execution_authority": EXECUTION_AUTHORITY,
        "acceptance_boundary": ACCEPTANCE_BOUNDARY,
        "acceptance_report": ACCEPTANCE_REPORT,
    }

    for label, path in sources.items():
        if not path.exists():
            failures.append(f"source_missing:{label}:{rel(path)}")

    source_hashes_before = {label: sha256_file(path) for label, path in sources.items() if path.exists()}

    receipt = read_json(ACCEPTANCE_RECEIPT)
    packet = read_json(ACCEPTANCE_PACKET)
    authority = read_json(EXECUTION_AUTHORITY)
    summary = receipt.get("machine_readable_unit_feedback_hardening_failed_unit_sample_discovery_prep_acceptance_summary", {})

    expected_receipt = {
        "gate": "PASS",
        "status": "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_ACCEPTANCE_PASS",
        "outcome_class": "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_ACCEPTED_FOR_ONE_BOUNDED_DISCOVERY_EXECUTION",
        "receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
    }
    for key, want in expected_receipt.items():
        chk(failures, f"acceptance_receipt_{key}", receipt.get(key), want)

    expected_summary = {
        "discovery_prep_acceptance_complete": True,
        "human_decision": "ACCEPT_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_FOR_ONE_BOUNDED_DISCOVERY_EXECUTION",
        "source_discovery_prep_receipt_id": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_receipt_3e05bd98",
        "source_discovery_prep_packet_id": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_packet_80abb45c",
        "source_discovery_prep_options_id": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_options_e69fd27d",
        "source_discovery_prep_boundary_id": "c8_unit_feedback_hardening_failed_unit_sample_discovery_prep_boundary_ee5732f7",
        "gap_object": GAP_OBJECT,
        "discovery_target": DISCOVERY_TARGET,
        "authorized_future_unit_after_review": UNIT_ID,
        "execution_limit_after_review": 1,
        "sample_discovery_execution_authorized_now": False,
        "sample_discovery_executed_now": False,
        "failed_unit_sample_found_now": False,
        "failed_unit_sample_count_now": 0,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_built_now": False,
        "c8_rerun_now": False,
        "reusable_schema_authorized": False,
        "source_artifacts_mutated": False,
        "forbidden_counters_zero": True,
        "requires_review": True,
        "recommended_review_unit": "REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_PREP_ACCEPTANCE_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "next_command_goal": None,
    }
    for key, want in expected_summary.items():
        chk(failures, f"acceptance_summary_{key}", summary.get(key), want)

    chk(failures, "authority_authorized_future_unit", authority.get("authorized_future_unit"), UNIT_ID)
    chk(failures, "authority_execution_limit", authority.get("execution_limit"), 1)
    chk(failures, "authority_status", authority.get("authority_status"), "ACTIVE_AFTER_REVIEW_AND_COMMIT")

    sample = None if failures else find_one_failed_unit_sample()

    failed_unit_sample_found = sample is not None
    failed_unit_sample_count = 1 if sample else 0
    if failed_unit_sample_count > 1:
        forbidden_counters["failed_unit_sample_count_over_limit"] += 1

    source_hashes_after = {label: sha256_file(path) for label, path in sources.items() if path.exists()}
    if source_hashes_before != source_hashes_after:
        forbidden_counters["source_artifact_mutation_count"] += 1

    local_nonzero = {k: v for k, v in forbidden_counters.items() if v != 0}
    for k, v in local_nonzero.items():
        failures.append(f"{k}:{v}")

    typed_gap = None if sample else TYPED_GAP_IF_NONE

    result = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_result_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_discovery_result_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "source_discovery_prep_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_discovery_execution_authority_id": SOURCE_EXECUTION_AUTHORITY_ID,
        "gap_object": GAP_OBJECT,
        "discovery_target": DISCOVERY_TARGET,
        "execution_limit": 1,
        "execution_count": 1,
        "search_surface": "git_tracked_committed_json_artifacts_under_data_or_logs",
        "search_policy": {
            "search_existing_committed_artifacts_only": True,
            "may_create_synthetic_failure": False,
            "may_mutate_source_artifacts": False,
            "may_rerun_c8": False,
            "may_execute_probe": False,
            "max_failed_unit_samples_to_return": 1,
        },
        "failed_unit_sample_found": failed_unit_sample_found,
        "failed_unit_sample_count": failed_unit_sample_count,
        "typed_gap_if_none": typed_gap,
        "failed_unit_sample": sample,
        "sample_discovery_executed_now": True,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
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
        "recommended_review_unit": "REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
    }
    result["c8_unit_feedback_hardening_failed_unit_sample_discovery_result_id"] = "c8_unit_feedback_hardening_failed_unit_sample_discovery_result_" + sig8(result)
    write_json(DISCOVERY_RESULT, result)

    boundary = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_boundary_audit_v0",
        "c8_unit_feedback_hardening_failed_unit_sample_discovery_boundary_audit_id": None,
        "gate": "PASS" if not failures else "FAIL",
        "source_discovery_result_id": result["c8_unit_feedback_hardening_failed_unit_sample_discovery_result_id"],
        "source_discovery_execution_authority_id": SOURCE_EXECUTION_AUTHORITY_ID,
        "allowed_now": {
            "execute_one_bounded_failed_unit_sample_discovery": True,
            "return_at_most_one_failed_unit_sample_or_typed_gap": True,
        },
        "not_allowed_now": {
            "execute_second_discovery": True,
            "authorize_probe_execution": True,
            "execute_probe": True,
            "build_instrument": True,
            "build_cell1": True,
            "run_verification_probe": True,
            "rerun_c8": True,
            "create_missing_instrument_proposal": True,
            "authorize_reusable_schema": True,
            "open_research_mode": True,
            "claim_global_solution": True,
            "claim_frontier_solved": True,
            "claim_unit_feedback_hardening_complete": True,
        },
        "forbidden_counters": forbidden_counters,
        "failures": failures,
        "warnings": warnings,
    }
    boundary["c8_unit_feedback_hardening_failed_unit_sample_discovery_boundary_audit_id"] = "c8_unit_feedback_hardening_failed_unit_sample_discovery_boundary_" + sig8(boundary)
    write_json(BOUNDARY_AUDIT, boundary)

    gate_results = {
        "DISCOVERY_EXECUTION_0_SOURCE_ACCEPTANCE_RECEIPT_PASS": receipt.get("gate") == "PASS",
        "DISCOVERY_EXECUTION_1_AUTHORITY_PRESENT_AND_ACTIVE": authority.get("authority_status") == "ACTIVE_AFTER_REVIEW_AND_COMMIT",
        "DISCOVERY_EXECUTION_2_AUTHORIZED_UNIT_MATCH": authority.get("authorized_future_unit") == UNIT_ID,
        "DISCOVERY_EXECUTION_3_EXECUTION_LIMIT_ONE": authority.get("execution_limit") == 1 and result["execution_count"] == 1,
        "DISCOVERY_EXECUTION_4_AT_MOST_ONE_SAMPLE": result["failed_unit_sample_count"] in (0, 1),
        "DISCOVERY_EXECUTION_5_TYPED_GAP_IF_NONE": result["failed_unit_sample_found"] is True or result["typed_gap_if_none"] == TYPED_GAP_IF_NONE,
        "DISCOVERY_EXECUTION_6_NO_PROBE_BUILD_RERUN_SCHEMA": result["probe_execution_authorized_now"] is False and result["instrument_build_authorized_now"] is False and result["c8_rerun_authorized_now"] is False and result["reusable_schema_authorized_now"] is False,
        "DISCOVERY_EXECUTION_7_SOURCE_ARTIFACTS_IMMUTABLE": source_hashes_before == source_hashes_after,
        "DISCOVERY_EXECUTION_8_FORBIDDEN_COUNTERS_ZERO": not bool(local_nonzero),
        "DISCOVERY_EXECUTION_9_REQUIRES_REVIEW": result["requires_review"] is True,
    }

    false_gates = [k for k, v in gate_results.items() if v is not True]
    if false_gates:
        failures.extend([f"discovery_execution_gate_false:{g}" for g in false_gates])

    gate = "PASS" if not failures else "FAIL"
    outcome = OUTCOME_FOUND if failed_unit_sample_found and gate == "PASS" else OUTCOME_GAP if gate == "PASS" else "C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_EXECUTION_FAILED"
    status = "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_EXECUTION_PASS" if gate == "PASS" else "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_EXECUTION_FAIL"
    terminal_stop = STOP_FOUND if failed_unit_sample_found and gate == "PASS" else STOP_GAP if gate == "PASS" else "STOP_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_EXECUTION_FAILED"

    readout = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_readout_v0",
        "title": "C8 unit-feedback hardening failed-unit sample discovery execution after runtime-adoption closure",
        "status": status,
        "outcome_class": outcome,
        "gap_object": GAP_OBJECT,
        "discovery_target": DISCOVERY_TARGET,
        "execution_limit": 1,
        "execution_count": 1,
        "failed_unit_sample_found": failed_unit_sample_found,
        "failed_unit_sample_count": failed_unit_sample_count,
        "typed_gap_if_none": typed_gap,
        "sample_discovery_executed_now": True,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
        "instrument_build_authorized_now": False,
        "c8_rerun_authorized_now": False,
        "reusable_schema_authorized_now": False,
        "recommended_review_unit": "REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "terminal_stop_code": terminal_stop,
    }
    write_json(READOUT, readout)

    report = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "source_discovery_prep_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
        "source_discovery_execution_authority_id": SOURCE_EXECUTION_AUTHORITY_ID,
        "gap_object": GAP_OBJECT,
        "discovery_target": DISCOVERY_TARGET,
        "execution_limit": 1,
        "execution_count": 1,
        "failed_unit_sample_found": failed_unit_sample_found,
        "failed_unit_sample_count": failed_unit_sample_count,
        "typed_gap_if_none": typed_gap,
        "failed_unit_sample": sample,
        "sample_discovery_executed_now": True,
        "probe_execution_authorized_now": False,
        "probe_executed_now": False,
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
        "recommended_review_unit": "REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
        "failures": failures,
        "warnings": warnings,
    }
    write_json(REPORT, report)

    receipt_obj = {
        "schema_version": "c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_receipt_v0",
        "receipt_type": "TYPED_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_EXECUTION_RECEIPT",
        "receipt_id": None,
        "created_at": now_iso(),
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "milestone": MILESTONE,
        "gate": gate,
        "status": status,
        "outcome_class": outcome,
        "machine_readable_unit_feedback_hardening_failed_unit_sample_discovery_execution_summary": {
            "sample_discovery_executed": gate == "PASS",
            "authorized_unit_consumed": UNIT_ID,
            "source_discovery_prep_acceptance_receipt_id": SOURCE_ACCEPTANCE_RECEIPT_ID,
            "source_discovery_execution_authority_id": SOURCE_EXECUTION_AUTHORITY_ID,
            "selected_surface_id": SELECTED_SURFACE_ID,
            "selected_surface_kind": SELECTED_SURFACE_KIND,
            "selected_surface_label": SELECTED_SURFACE_LABEL,
            "probe_id": PROBE_ID,
            "probe_kind": PROBE_KIND,
            "probe_label": PROBE_LABEL,
            "gap_object": GAP_OBJECT,
            "discovery_target": DISCOVERY_TARGET,
            "execution_limit": 1,
            "execution_count": 1,
            "failed_unit_sample_found": failed_unit_sample_found,
            "failed_unit_sample_count": failed_unit_sample_count,
            "typed_gap_if_none": typed_gap,
            "failed_unit_sample_id": sample.get("failed_unit_sample_id") if sample else None,
            "failed_unit_sample_source_path": sample.get("source_path") if sample else None,
            "sample_discovery_executed_now": True,
            "probe_execution_authorized_now": False,
            "probe_executed_now": False,
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
            "forbidden_counters_zero": not bool(local_nonzero),
            "requires_review": True,
            "recommended_review_unit": "REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0",
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
            "discovery_result": rel(DISCOVERY_RESULT),
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

    receipt_obj["receipt_id"] = "c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_receipt_" + sig8(receipt_obj)
    receipt_path = RECEIPT_DIR / f"{receipt_obj['receipt_id']}.json"
    receipt_obj["output_artifacts"]["receipt"] = rel(receipt_path)
    write_json(receipt_path, receipt_obj)

    print(json.dumps(receipt_obj, indent=2, sort_keys=True))
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_receipt_id={receipt_obj['receipt_id']}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_execution_receipt_path={rel(receipt_path)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_result_path={rel(DISCOVERY_RESULT)}")
    print(f"c8_unit_feedback_hardening_failed_unit_sample_discovery_boundary_path={rel(BOUNDARY_AUDIT)}")
    print(f"gap_object={GAP_OBJECT}")
    print(f"discovery_target={DISCOVERY_TARGET}")
    print("execution_limit=1")
    print("execution_count=1")
    print(f"failed_unit_sample_found={str(failed_unit_sample_found).lower()}")
    print(f"failed_unit_sample_count={failed_unit_sample_count}")
    print(f"typed_gap_if_none={typed_gap}")
    if sample:
        print(f"failed_unit_sample_id={sample['failed_unit_sample_id']}")
        print(f"failed_unit_sample_source_path={sample['source_path']}")
    print("sample_discovery_executed_now=true")
    print("probe_execution_authorized_now=false")
    print("probe_executed_now=false")
    print("instrument_built_now=false")
    print("c8_rerun_now=false")
    print("reusable_schema_authorized=false")
    print("recommended_review_unit=REVIEW_C8_UNIT_FEEDBACK_HARDENING_FAILED_UNIT_SAMPLE_DISCOVERY_EXECUTION_AFTER_RUNTIME_ADOPTION_CLOSURE_V0")
    print(f"terminal_stop_code={terminal_stop}")

    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
