#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_O2_UNIT_FEEDBACK_HARDENING_V0"
TARGET_UNIT_ID = "observation.unit_feedback_hardening_review.v0"
LAYER = "OBSERVATION_HARDENING / FAILURE_DIAGNOSTIC_QUALITY / REVIEW"
MODE = "REVIEW / VERIFY_STATIC_SCHEMA_PROBE / NO_REPAIR_NO_C5"
BUILD_MODE = "O2_REVIEW_ONLY"

O2_BUILD_RECEIPT_ID = "131d6837"
O2_BUILD_RECEIPT_PATH = ROOT / "data/o2_unit_feedback_hardening_v0_receipts/131d6837.json"

O2_FAILURE_EVENT_SCHEMA_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_failure_event_schema_v0.json"
O2_FEEDBACK_RECORD_SCHEMA_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_feedback_record_schema_v0.json"
O2_FAILURE_LOCATION_SCHEMA_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_failure_location_schema_v0.json"
O2_QUALITY_ENUM_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_feedback_quality_enum_v0.json"
O2_MISSING_CAPABILITY_SCHEMA_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_missing_capability_record_schema_v0.json"
O2_REFINEMENT_SCHEMA_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_refinement_candidate_schema_v0.json"
O2_RETRY_GATE_SCHEMA_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_retry_gate_schema_v0.json"
O2_EDGE_LINK_SCHEMA_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/edge_feedback_link_schema_v0.json"

O2_DEMO_EVENTS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/o2_demo_failure_events_v0.jsonl"
O2_FAILURE_EVENTS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_failure_events_v0.jsonl"
O2_FEEDBACK_RECORDS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_feedback_records_v0.jsonl"
O2_LOCATION_RECORDS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_failure_location_records_v0.jsonl"
O2_MISSING_CAPABILITY_RECORDS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_missing_capability_records_v0.jsonl"
O2_REFINEMENT_RECORDS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_refinement_candidate_records_v0.jsonl"
O2_RETRY_GATE_RECORDS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_retry_gate_records_v0.jsonl"
O2_EDGE_LINKS_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/edge_feedback_links_v0.jsonl"

O2_ROLLUP_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_feedback_rollup_v0.json"
O2_READOUT_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/unit_feedback_readout_v0.json"
O2_PROFILE_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/o2_feedback_profile_v0.json"
O2_REPORT_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/o2_report.json"
O2_TRACE_PATH = ROOT / "data/o2_unit_feedback_hardening_v0/o2_transition_trace.json"

O2_DESIGN_RECEIPT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0_receipts/e55e60e1.json"
O2_DESIGN_AUTHORIZATION_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_build_unit_authorization_v0.json"
O2_DESIGN_MODE_CONTRACT_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_initial_mode_contract_v0.json"
O2_DESIGN_NONREPAIR_BOUNDARY_PATH = ROOT / "data/o2_unit_feedback_hardening_target_design_v0/o2_nonrepair_nonauthority_boundary_v0.json"

REQUIRED_SOURCE_FILES = [
    O2_BUILD_RECEIPT_PATH,
    O2_FAILURE_EVENT_SCHEMA_PATH,
    O2_FEEDBACK_RECORD_SCHEMA_PATH,
    O2_FAILURE_LOCATION_SCHEMA_PATH,
    O2_QUALITY_ENUM_PATH,
    O2_MISSING_CAPABILITY_SCHEMA_PATH,
    O2_REFINEMENT_SCHEMA_PATH,
    O2_RETRY_GATE_SCHEMA_PATH,
    O2_EDGE_LINK_SCHEMA_PATH,
    O2_DEMO_EVENTS_PATH,
    O2_FAILURE_EVENTS_PATH,
    O2_FEEDBACK_RECORDS_PATH,
    O2_LOCATION_RECORDS_PATH,
    O2_MISSING_CAPABILITY_RECORDS_PATH,
    O2_REFINEMENT_RECORDS_PATH,
    O2_RETRY_GATE_RECORDS_PATH,
    O2_EDGE_LINKS_PATH,
    O2_ROLLUP_PATH,
    O2_READOUT_PATH,
    O2_PROFILE_PATH,
    O2_REPORT_PATH,
    O2_TRACE_PATH,
    O2_DESIGN_RECEIPT_PATH,
    O2_DESIGN_AUTHORIZATION_PATH,
    O2_DESIGN_MODE_CONTRACT_PATH,
    O2_DESIGN_NONREPAIR_BOUNDARY_PATH,
]

OUT_DIR = ROOT / "data/o2_unit_feedback_hardening_review_v0"
RECEIPT_DIR = ROOT / "data/o2_unit_feedback_hardening_review_v0_receipts"

REVIEW_ASSESSMENT_PATH = OUT_DIR / "o2_unit_feedback_hardening_review_assessment_v0.json"
SCHEMA_REVIEW_PATH = OUT_DIR / "o2_schema_artifact_review_v0.json"
FEEDBACK_RECORD_REVIEW_PATH = OUT_DIR / "o2_feedback_record_integrity_review_v0.json"
WEAK_FEEDBACK_REVIEW_PATH = OUT_DIR / "o2_weak_feedback_intentionality_review_v0.json"
EXPECTED_LIMIT_REVIEW_PATH = OUT_DIR / "o2_expected_limit_separation_review_v0.json"
RETRY_GATE_REVIEW_PATH = OUT_DIR / "o2_retry_gate_review_v0.json"
CANDIDATE_ONLY_REVIEW_PATH = OUT_DIR / "o2_candidate_only_boundary_review_v0.json"
C5_READINESS_REVIEW_PATH = OUT_DIR / "o2_c5_feedback_readiness_review_v0.json"
NONAUTHORITY_SAFETY_REVIEW_PATH = OUT_DIR / "o2_nonauthority_safety_review_v0.json"
CLOSURE_CANDIDATE_PATH = OUT_DIR / "o2_unit_feedback_hardening_closure_candidate_v0.json"
DOWNSTREAM_DECISION_TABLE_PATH = OUT_DIR / "o2_review_downstream_decision_table_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "o2_review_classification_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "o2_review_authority_boundary_v0.json"
ROLLUP_OUT_PATH = OUT_DIR / "o2_review_rollup_v0.json"
PROFILE_OUT_PATH = OUT_DIR / "o2_review_profile_v0.json"
REPORT_OUT_PATH = OUT_DIR / "o2_review_report.json"
TRACE_OUT_PATH = OUT_DIR / "o2_review_transition_trace.json"

EXPECTED_BUILD_STATUS = "TYPED_O2_UNIT_FEEDBACK_HARDENING_STATIC_SCHEMA_PROBE_EMITTED_WEAK_FEEDBACK_REMAINS"
EXPECTED_BUILD_STOP = "STOP_O2_WEAK_FEEDBACK_REMAINS"
EXPECTED_BUILD_NEXT = "REVIEW_O2_UNIT_FEEDBACK_HARDENING_V0"

QUALITY_CLASSES = [
    "NO_FEEDBACK",
    "STATUS_ONLY",
    "LOCALIZED_FAILURE",
    "BOUNDARY_AWARE_FAILURE",
    "CAPABILITY_AWARE_FAILURE",
    "REFINEMENT_READY_FAILURE",
    "EXPECTED_LIMIT",
    "AMBIGUOUS_REQUIRES_QUESTION",
    "UNDER_TYPED_FEEDBACK",
]

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

def read_jsonl(path: Path) -> List[Dict[str, Any]]:
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()]

def write_json(path: Path, obj: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")

def snapshot_files(paths: List[Path]) -> Dict[str, str]:
    return {rel(p): file_sha256(p) for p in paths if p.exists()}

def validate_basis() -> Tuple[List[str], Dict[str, Any]]:
    failures: List[str] = []
    for path in REQUIRED_SOURCE_FILES:
        if not path.exists():
            failures.append(f"required_source_missing:{path.as_posix()}")
    if failures:
        return failures, {}

    receipt = read_json(O2_BUILD_RECEIPT_PATH)
    summary = receipt.get("machine_readable_o2_unit_feedback_summary", {})
    schemas = {
        "unit_failure_event_schema": read_json(O2_FAILURE_EVENT_SCHEMA_PATH),
        "unit_feedback_record_schema": read_json(O2_FEEDBACK_RECORD_SCHEMA_PATH),
        "unit_failure_location_schema": read_json(O2_FAILURE_LOCATION_SCHEMA_PATH),
        "unit_feedback_quality_enum": read_json(O2_QUALITY_ENUM_PATH),
        "unit_missing_capability_record_schema": read_json(O2_MISSING_CAPABILITY_SCHEMA_PATH),
        "unit_refinement_candidate_schema": read_json(O2_REFINEMENT_SCHEMA_PATH),
        "unit_retry_gate_schema": read_json(O2_RETRY_GATE_SCHEMA_PATH),
        "edge_feedback_link_schema": read_json(O2_EDGE_LINK_SCHEMA_PATH),
    }
    demo_events = read_jsonl(O2_DEMO_EVENTS_PATH)
    events = read_jsonl(O2_FAILURE_EVENTS_PATH)
    feedback = read_jsonl(O2_FEEDBACK_RECORDS_PATH)
    locations = read_jsonl(O2_LOCATION_RECORDS_PATH)
    missing_caps = read_jsonl(O2_MISSING_CAPABILITY_RECORDS_PATH)
    refinements = read_jsonl(O2_REFINEMENT_RECORDS_PATH)
    retry_gates = read_jsonl(O2_RETRY_GATE_RECORDS_PATH)
    edge_links = read_jsonl(O2_EDGE_LINKS_PATH)
    rollup = read_json(O2_ROLLUP_PATH)
    readout = read_json(O2_READOUT_PATH)
    profile = read_json(O2_PROFILE_PATH)
    report = read_json(O2_REPORT_PATH)
    trace = read_json(O2_TRACE_PATH)
    design_receipt = read_json(O2_DESIGN_RECEIPT_PATH)
    design_auth = read_json(O2_DESIGN_AUTHORIZATION_PATH)
    design_mode = read_json(O2_DESIGN_MODE_CONTRACT_PATH)
    nonrepair = read_json(O2_DESIGN_NONREPAIR_BOUNDARY_PATH)

    if receipt.get("receipt_id") != O2_BUILD_RECEIPT_ID or receipt.get("gate") != "PASS":
        failures.append("o2_build_receipt_not_pass")
    if receipt.get("terminal", {}).get("stop_code") != EXPECTED_BUILD_STOP:
        failures.append(f"o2_build_terminal_not_expected:{receipt.get('terminal', {}).get('stop_code')}")
    if receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("o2_build_hidden_next_command")
    if summary.get("status") != EXPECTED_BUILD_STATUS:
        failures.append(f"o2_build_status_not_expected:{summary.get('status')}")
    if summary.get("recommended_next") != EXPECTED_BUILD_NEXT:
        failures.append(f"o2_build_next_not_expected:{summary.get('recommended_next')}")

    for key in [
        "schemas_emitted",
        "demo_failure_events_emitted",
        "unit_failure_events_emitted",
        "unit_feedback_records_emitted",
        "bad_counters_zero",
    ]:
        if summary.get(key) is not True:
            failures.append(f"summary_required_true_missing:{key}")

    for key in [
        "live_feedback_audit_executed",
        "repair_applied",
        "retry_executed",
        "target_selected_for_build",
        "runtime_patch_applied",
        "source_mutated",
        "prior_receipt_mutated",
        "architecture_change",
        "c5_opened",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if summary.get(key) is not False:
            failures.append(f"summary_forbidden_true:{key}")

    expected_counts = {
        "units_evaluated": 10,
        "feedback_records_emitted_count": 10,
        "weak_feedback_count": 3,
        "bare_failed_status_count": 0,
        "refinement_ready_count": 2,
        "expected_limit_count": 1,
        "retry_blocked_count": 10,
    }
    for key, expected in expected_counts.items():
        if summary.get(key) != expected:
            failures.append(f"summary_count_wrong:{key}:{summary.get(key)}")

    if summary.get("initial_mode") != "STATIC_SCHEMA_AND_PROBE_ONLY":
        failures.append("initial_mode_wrong")
    if summary.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("c5_feedback_readiness_not_blocked_by_weak_feedback")

    if len(schemas) != 8:
        failures.append("schema_count_wrong")
    for name, schema in schemas.items():
        if not schema.get("schema_version"):
            failures.append(f"schema_missing_version:{name}")

    if len(demo_events) != 10 or len(events) != 10 or len(feedback) != 10:
        failures.append("demo_event_or_feedback_count_wrong")
    if len(locations) != 10 or len(missing_caps) != 10 or len(refinements) != 10 or len(retry_gates) != 10:
        failures.append("linked_record_count_wrong")
    if len(edge_links) != 10:
        failures.append("edge_link_count_wrong")

    for idx, rec in enumerate(feedback):
        q = rec.get("quality", {}).get("feedback_quality_class")
        if q == "NO_FEEDBACK" or q == "STATUS_ONLY":
            failures.append(f"accepted_feedback_too_weak:{idx}:{q}")
        if not rec.get("failure_explanation", {}).get("where_failed"):
            failures.append(f"feedback_missing_where:{idx}")
        if not rec.get("failure_explanation", {}).get("why_failed"):
            failures.append(f"feedback_missing_why:{idx}")
        if not rec.get("failure_explanation", {}).get("failed_relative_to_object"):
            failures.append(f"feedback_missing_object:{idx}")
        if not rec.get("failure_explanation", {}).get("failed_relative_to_source_surface"):
            failures.append(f"feedback_missing_source_surface:{idx}")
        if not rec.get("failure_explanation", {}).get("failed_relative_to_boundary"):
            failures.append(f"feedback_missing_boundary:{idx}")
        if not rec.get("movement", {}).get("blocked_next_moves"):
            failures.append(f"feedback_missing_blocked_moves:{idx}")
        if not rec.get("movement", {}).get("lawful_next_refinements"):
            failures.append(f"feedback_missing_lawful_next_refinement:{idx}")
        if not rec.get("missing_capability", {}).get("smallest_honest_name") and not rec.get("missing_capability", {}).get("evidence_for_missing"):
            failures.append(f"feedback_missing_capability_or_evidence:{idx}")
        if rec.get("quality", {}).get("retry_allowed") is not False:
            failures.append(f"feedback_retry_allowed:{idx}")
        for key in ["repair_applied", "target_selected_for_build", "source_mutated", "prior_receipt_mutated", "architecture_change", "c5_opened"]:
            if rec.get("safety", {}).get(key) is not False:
                failures.append(f"feedback_safety_true:{key}:{idx}")

    for idx, cap in enumerate(missing_caps):
        if cap.get("status") != "CANDIDATE_ONLY":
            failures.append(f"missing_cap_not_candidate_only:{idx}:{cap.get('status')}")
    for idx, ref in enumerate(refinements):
        if ref.get("status") != "PROPOSED_ONLY":
            failures.append(f"refinement_not_proposed_only:{idx}:{ref.get('status')}")
    for idx, gate in enumerate(retry_gates):
        if gate.get("retry_allowed") is not False:
            failures.append(f"retry_gate_allowed:{idx}")
        if gate.get("terminal_if_blocked") != "STOP_SAME_FAILURE_RETRY_BLOCKED":
            failures.append(f"retry_gate_terminal_wrong:{idx}")
    for idx, link in enumerate(edge_links):
        if not link.get("unit_feedback_ref") or not link.get("decision_edge_observation_ref"):
            failures.append(f"edge_link_incomplete:{idx}")

    quality_counts = Counter(x.get("quality", {}).get("feedback_quality_class") for x in feedback)
    expected_quality = {
        "NO_FEEDBACK": 0,
        "STATUS_ONLY": 0,
        "LOCALIZED_FAILURE": 1,
        "BOUNDARY_AWARE_FAILURE": 2,
        "CAPABILITY_AWARE_FAILURE": 1,
        "REFINEMENT_READY_FAILURE": 2,
        "EXPECTED_LIMIT": 1,
        "AMBIGUOUS_REQUIRES_QUESTION": 1,
        "UNDER_TYPED_FEEDBACK": 2,
    }
    for key, expected in expected_quality.items():
        if quality_counts.get(key, 0) != expected:
            failures.append(f"quality_count_wrong:{key}:{quality_counts.get(key, 0)}")

    required_zero_rollup_keys = [
        "bare_failed_status_count",
        "retry_allowed_without_refinement_count",
        "repair_applied_by_feedback_unit_count",
        "target_selected_by_feedback_unit_count",
        "architecture_change_by_feedback_unit_count",
        "source_mutated_by_feedback_unit_count",
        "prior_receipt_mutated_by_feedback_unit_count",
        "expected_limit_counted_as_bug_count",
        "productive_pressure_counted_as_success_count",
        "ambiguous_failure_forced_to_repair_count",
        "c5_opened_count",
        "hidden_next_command_count",
        "live_feedback_audit_executed_count",
        "runtime_patch_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]
    for key in required_zero_rollup_keys:
        if rollup.get(key) != 0:
            failures.append(f"rollup_counter_nonzero:{key}:{rollup.get(key)}")

    if rollup.get("weak_feedback_count") != 3:
        failures.append("rollup_weak_feedback_count_wrong")
    if readout.get("c5_feedback_readiness") != "BLOCKED_BY_WEAK_FEEDBACK":
        failures.append("readout_c5_readiness_wrong")
    if profile.get("status") != "O2_WEAK_FEEDBACK_REMAINS":
        failures.append("profile_status_wrong")
    if profile.get("bad_counters_zero") is not True:
        failures.append("profile_bad_counters_not_zero")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next_command")
    if trace.get("terminal", {}).get("stop_code") != EXPECTED_BUILD_STOP:
        failures.append("trace_terminal_wrong")
    if report.get("recommended_next_handling") != EXPECTED_BUILD_NEXT:
        failures.append("report_recommended_next_wrong")
    if design_receipt.get("receipt_id") != "e55e60e1":
        failures.append("design_receipt_wrong")
    if design_auth.get("authorized_initial_mode") != "STATIC_SCHEMA_AND_PROBE_ONLY":
        failures.append("design_auth_mode_wrong")
    if design_mode.get("initial_mode") != "STATIC_SCHEMA_AND_PROBE_ONLY":
        failures.append("design_mode_wrong")
    if nonrepair.get("feedback_record_is_diagnostic_not_repair") is not True:
        failures.append("nonrepair_boundary_not_diagnostic")

    return failures, {
        "summary": summary,
        "schemas": schemas,
        "demo_events": demo_events,
        "events": events,
        "feedback": feedback,
        "locations": locations,
        "missing_caps": missing_caps,
        "refinements": refinements,
        "retry_gates": retry_gates,
        "edge_links": edge_links,
        "rollup": rollup,
        "readout": readout,
        "profile": profile,
        "quality_counts": dict(sorted(quality_counts.items())),
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, src = validate_basis()

    summary = src.get("summary", {})
    schemas = src.get("schemas", {})
    demo_events = src.get("demo_events", [])
    events = src.get("events", [])
    feedback = src.get("feedback", [])
    locations = src.get("locations", [])
    missing_caps = src.get("missing_caps", [])
    refinements = src.get("refinements", [])
    retry_gates = src.get("retry_gates", [])
    edge_links = src.get("edge_links", [])
    rollup = src.get("rollup", {})
    readout = src.get("readout", {})
    profile = src.get("profile", {})
    quality_counts = src.get("quality_counts", {})

    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    review_pass = not failures
    status = "TYPED_O2_UNIT_FEEDBACK_HARDENING_REVIEWED_STATIC_PROBE_CLEAN_WEAK_FEEDBACK_INTENTIONAL_CLOSE_READY" if review_pass else "TYPED_O2_UNIT_FEEDBACK_HARDENING_REVIEW_FAIL"
    reason_codes = [
        "O2_REVIEW_COMPLETE",
        "O2_REVIEW_PASS",
        "STATIC_SCHEMA_AND_PROBE_MODE_CONFIRMED",
        "SCHEMA_ARTIFACTS_PRESENT",
        "TEN_DEMO_FAILURE_EVENTS_REVIEWED",
        "TEN_FEEDBACK_RECORDS_REVIEWED",
        "WEAK_FEEDBACK_INTENTIONAL_AND_TYPED",
        "BARE_FAILURES_DO_NOT_SURVIVE_AS_ACCEPTED_FEEDBACK",
        "EXPECTED_LIMITS_SEPARATED_FROM_BUGS",
        "UNCHANGED_RETRIES_BLOCKED",
        "REFINEMENT_CANDIDATES_PROPOSED_ONLY",
        "MISSING_CAPABILITIES_CANDIDATE_ONLY",
        "C5_BLOCKED_BY_WEAK_FEEDBACK",
        "BAD_COUNTERS_ZERO",
        "NO_LIVE_FEEDBACK_AUDIT",
        "NO_REPAIR_APPLIED",
        "NO_RETRY_EXECUTED",
        "NO_TARGET_SELECTED_FOR_BUILD",
        "NO_RUNTIME_PATCH",
        "NO_SOURCE_MUTATION",
        "NO_C5_OPENED",
        "O2_CLOSURE_CANDIDATE_EMITTED",
    ] if review_pass else failures
    recommended_next = "CLOSE_O2_UNIT_FEEDBACK_HARDENING_AS_REVIEWED_REFERENCE_V0" if review_pass else "REPAIR_O2_UNIT_FEEDBACK_HARDENING_V0"

    schema_review = {
        "schema_version": "o2_schema_artifact_review_v0",
        "review_status": "SCHEMA_ARTIFACTS_PRESENT" if review_pass else "SCHEMA_ARTIFACT_REPAIR_REQUIRED",
        "schema_count": len(schemas),
        "required_schema_versions": sorted(x.get("schema_version") for x in schemas.values()),
    }

    feedback_record_review = {
        "schema_version": "o2_feedback_record_integrity_review_v0",
        "review_status": "FEEDBACK_RECORD_INTEGRITY_PASS" if review_pass else "FEEDBACK_RECORD_INTEGRITY_REPAIR_REQUIRED",
        "events_reviewed": len(events),
        "feedback_records_reviewed": len(feedback),
        "location_records_reviewed": len(locations),
        "missing_capability_records_reviewed": len(missing_caps),
        "refinement_candidate_records_reviewed": len(refinements),
        "retry_gate_records_reviewed": len(retry_gates),
        "edge_feedback_links_reviewed": len(edge_links),
        "every_feedback_has_where": all(x.get("failure_explanation", {}).get("where_failed") for x in feedback),
        "every_feedback_has_why": all(x.get("failure_explanation", {}).get("why_failed") for x in feedback),
        "every_feedback_has_boundary": all(x.get("failure_explanation", {}).get("failed_relative_to_boundary") for x in feedback),
        "every_feedback_has_object": all(x.get("failure_explanation", {}).get("failed_relative_to_object") for x in feedback),
        "every_feedback_has_source_surface": all(x.get("failure_explanation", {}).get("failed_relative_to_source_surface") for x in feedback),
        "every_feedback_has_lawful_next_refinement_or_question": all(bool(x.get("movement", {}).get("lawful_next_refinements")) for x in feedback),
    }

    weak_feedback_review = {
        "schema_version": "o2_weak_feedback_intentionality_review_v0",
        "review_status": "WEAK_FEEDBACK_INTENTIONAL_AND_TYPED" if review_pass else "WEAK_FEEDBACK_REPAIR_REQUIRED",
        "weak_feedback_count": rollup.get("weak_feedback_count"),
        "under_typed_feedback_count": quality_counts.get("UNDER_TYPED_FEEDBACK", 0),
        "ambiguous_requires_question_count": quality_counts.get("AMBIGUOUS_REQUIRES_QUESTION", 0),
        "status_only_count": quality_counts.get("STATUS_ONLY", 0),
        "no_feedback_count": quality_counts.get("NO_FEEDBACK", 0),
        "bare_failed_status_count": rollup.get("bare_failed_status_count"),
        "interpretation": "Weak feedback remains only as typed static-probe signal, not as accepted bare failure.",
        "c5_effect": "C5 remains blocked by weak feedback.",
    }

    expected_limit_review = {
        "schema_version": "o2_expected_limit_separation_review_v0",
        "review_status": "EXPECTED_LIMITS_SEPARATED_FROM_BUGS" if review_pass else "EXPECTED_LIMIT_REPAIR_REQUIRED",
        "expected_limit_count": quality_counts.get("EXPECTED_LIMIT", 0),
        "expected_limit_counted_as_bug_count": rollup.get("expected_limit_counted_as_bug_count"),
        "productive_pressure_counted_as_success_count": rollup.get("productive_pressure_counted_as_success_count"),
    }

    retry_gate_review = {
        "schema_version": "o2_retry_gate_review_v0",
        "review_status": "UNCHANGED_RETRIES_BLOCKED" if review_pass else "RETRY_GATE_REPAIR_REQUIRED",
        "retry_gate_count": len(retry_gates),
        "retry_blocked_count": rollup.get("retry_blocked_count"),
        "retry_allowed_without_refinement_count": rollup.get("retry_allowed_without_refinement_count"),
        "all_retry_allowed_false": all(x.get("retry_allowed") is False for x in retry_gates),
    }

    candidate_only_review = {
        "schema_version": "o2_candidate_only_boundary_review_v0",
        "review_status": "CANDIDATE_ONLY_BOUNDARY_PASS" if review_pass else "CANDIDATE_ONLY_BOUNDARY_REPAIR_REQUIRED",
        "missing_capability_count": len(missing_caps),
        "refinement_candidate_count": len(refinements),
        "all_missing_capabilities_candidate_only": all(x.get("status") == "CANDIDATE_ONLY" for x in missing_caps),
        "all_refinement_candidates_proposed_only": all(x.get("status") == "PROPOSED_ONLY" for x in refinements),
        "missing_capability_record_is_not_authorized_build": True,
        "refinement_candidate_is_not_accepted_proposal": True,
    }

    c5_review = {
        "schema_version": "o2_c5_feedback_readiness_review_v0",
        "review_status": "C5_BLOCKED_BY_WEAK_FEEDBACK",
        "c5_feedback_readiness": readout.get("c5_feedback_readiness"),
        "weak_feedback_count": rollup.get("weak_feedback_count"),
        "c5_opened": False,
        "meaning": "O2 static probe built useful feedback machinery, but C5 remains blocked until weak feedback is resolved or explicitly accepted as under-typed/question-packet material.",
    }

    nonauthority_safety_review = {
        "schema_version": "o2_nonauthority_safety_review_v0",
        "review_status": "NONAUTHORITY_SAFETY_REVIEW_PASS" if review_pass else "NONAUTHORITY_SAFETY_REPAIR_REQUIRED",
        "live_feedback_audit_executed": False,
        "repair_applied": False,
        "retry_executed": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "architecture_change": False,
        "c5_opened": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
    }

    closure_candidate = {
        "schema_version": "o2_unit_feedback_hardening_closure_candidate_v0",
        "closure_candidate_status": "O2_CLOSURE_CANDIDATE_READY_WITH_WEAK_FEEDBACK_NOTE" if review_pass else "O2_CLOSURE_CANDIDATE_NOT_READY",
        "o2_review_pass": review_pass,
        "reviewed_reference_candidate": "o2_unit_feedback_hardening_static_schema_probe_v0",
        "closure_meaning": "O2 static schema/probe feedback machinery can close as reviewed reference with weak feedback intentionally recorded.",
        "closure_does_not_mean": [
            "weak feedback resolved",
            "live audit complete",
            "failure repaired",
            "target selected",
            "retry authorized",
            "C5 opened",
        ],
        "recommended_after_closure": "DECIDE_NEXT_AFTER_O2_FEEDBACK_REFERENCE_CLOSURE_V0",
    }

    downstream_decision_table = {
        "schema_version": "o2_review_downstream_decision_table_v0",
        "decision_status": "O2_REVIEW_DOWNSTREAM_TABLE_EMITTED",
        "records": [
            {
                "decision": "CLOSE_O2_AS_REVIEWED_REFERENCE",
                "selected": review_pass,
                "next_unit": "CLOSE_O2_UNIT_FEEDBACK_HARDENING_AS_REVIEWED_REFERENCE_V0" if review_pass else None,
                "why": "O2 static probe reviewed clean; weak feedback remains typed and intentional.",
            },
            {
                "decision": "RUN_LIVE_FEEDBACK_AUDIT_NOW",
                "selected": False,
                "next_unit": None,
                "why": "Live audit still requires explicit source receipts/traces and is not part of this review.",
            },
            {
                "decision": "OPEN_C5_NOW",
                "selected": False,
                "next_unit": None,
                "why": "C5 remains blocked by weak feedback.",
            },
        ],
    }

    classification = {
        "schema_version": "o2_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "o2_review_complete": review_pass,
        "o2_review_pass": review_pass,
        "schemas_reviewed": len(schemas),
        "events_reviewed": len(events),
        "feedback_records_reviewed": len(feedback),
        "weak_feedback_intentional": review_pass,
        "weak_feedback_count": rollup.get("weak_feedback_count"),
        "c5_feedback_readiness": readout.get("c5_feedback_readiness"),
        "closure_candidate_ready": review_pass,
        "recommended_next": recommended_next,
        "live_feedback_audit_executed": False,
        "repair_applied": False,
        "retry_executed": False,
        "target_selected_for_build": False,
        "runtime_patch_applied": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "architecture_change": False,
        "c5_opened": False,
        "hidden_next_command": False,
        "next_command_goal": None,
    }

    authority_boundary = {
        "schema_version": "o2_review_authority_boundary_v0",
        "status": status,
        "may_close_o2_as_reviewed_reference_next": review_pass,
        "may_run_live_feedback_audit_now": False,
        "may_repair_failure": False,
        "may_retry_unit": False,
        "may_select_target_for_build": False,
        "may_patch_runtime": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_open_c5": False,
        "may_expand_authority": False,
    }

    review_assessment = {
        "schema_version": "o2_unit_feedback_hardening_review_assessment_v0",
        "review_status": status,
        "source_o2_build_receipt_id": O2_BUILD_RECEIPT_ID,
        "o2_review_complete": review_pass,
        "o2_review_pass": review_pass,
        "units_evaluated": rollup.get("units_evaluated"),
        "feedback_records_reviewed": len(feedback),
        "weak_feedback_count": rollup.get("weak_feedback_count"),
        "c5_feedback_readiness": readout.get("c5_feedback_readiness"),
        "closure_candidate_ready": review_pass,
        "recommended_next": recommended_next,
    }

    rollup_out = {
        "schema_version": "o2_review_rollup_v0",
        "build_mode": BUILD_MODE,
        "classification_status": status,
        "o2_review_count": 1,
        "o2_review_pass_count": 1 if review_pass else 0,
        "schema_review_count": len(schemas),
        "event_review_count": len(events),
        "feedback_record_review_count": len(feedback),
        "weak_feedback_count": rollup.get("weak_feedback_count"),
        "bare_failed_status_count": rollup.get("bare_failed_status_count"),
        "retry_blocked_count": rollup.get("retry_blocked_count"),
        "refinement_ready_count": rollup.get("refinement_ready_count"),
        "expected_limit_count": rollup.get("feedback_quality_counts", {}).get("EXPECTED_LIMIT", 0),
        "closure_candidate_count": 1 if review_pass else 0,
        "live_feedback_audit_executed_count": 0,
        "repair_applied_count": 0,
        "retry_executed_count": 0,
        "target_selected_for_build_count": 0,
        "runtime_patch_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "architecture_change_count": 0,
        "c5_opened_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    zero_keys = [
        "live_feedback_audit_executed_count",
        "repair_applied_count",
        "retry_executed_count",
        "target_selected_for_build_count",
        "runtime_patch_count",
        "source_mutated_count",
        "prior_receipt_mutated_count",
        "architecture_change_count",
        "c5_opened_count",
        "hidden_next_command_count",
        "latest_file_guessing_count",
        "mtime_selection_count",
    ]

    profile_out = {
        "schema_version": "o2_review_profile_v0",
        "profile_id": "o2_review_profile_" + sha8(rollup_out),
        "status": status,
        "o2_review_pass": review_pass,
        "weak_feedback_intentional": review_pass,
        "weak_feedback_count": rollup.get("weak_feedback_count"),
        "c5_feedback_readiness": readout.get("c5_feedback_readiness"),
        "closure_candidate_ready": review_pass,
        "recommendation": "Close O2 as reviewed reference with weak feedback note; do not open C5.",
        "bad_counters_zero": all(rollup_out.get(k) == 0 for k in zero_keys),
        "must_not_infer": [
            "weak feedback resolved",
            "live audit complete",
            "repair applied",
            "target selected",
            "retry authorized",
            "C5 opened",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "o2_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "O2 static schema/probe build reviewed clean. Schemas are present; 10 demo failure events have 10 feedback records; weak feedback remains as typed under-typed/question feedback; bare FAILED does not survive as accepted feedback; expected limits are separated from bugs; unchanged retries are blocked; refinement candidates remain PROPOSED_ONLY; missing capabilities remain CANDIDATE_ONLY; C5 remains blocked by weak feedback. No live audit, repair, retry, target selection, runtime patch, source mutation, prior receipt mutation, architecture change, C5 opening, latest-file selection, mtime selection, or hidden command occurred.",
        "weak_feedback_count": rollup.get("weak_feedback_count"),
        "c5_feedback_readiness": readout.get("c5_feedback_readiness"),
        "bad_counters_zero": profile_out["bad_counters_zero"],
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "o2_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_o2_build",
                "question": "did O2 emit the static schema/probe layer",
                "answer": "yes" if review_pass else "no",
                "taken": "review schemas, demo events, feedback records, rollup, readout, profile, and receipt",
            },
            {
                "step": "verify_weak_feedback",
                "question": "does weak feedback remain as typed signal rather than bare failure",
                "answer": "yes" if review_pass else "no",
                "taken": "preserve C5 block by weak feedback",
            },
            {
                "step": "emit_closure_candidate",
                "question": "can O2 close as reviewed reference",
                "answer": "yes" if review_pass else "no",
                "taken": recommended_next,
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (REVIEW_ASSESSMENT_PATH, review_assessment),
        (SCHEMA_REVIEW_PATH, schema_review),
        (FEEDBACK_RECORD_REVIEW_PATH, feedback_record_review),
        (WEAK_FEEDBACK_REVIEW_PATH, weak_feedback_review),
        (EXPECTED_LIMIT_REVIEW_PATH, expected_limit_review),
        (RETRY_GATE_REVIEW_PATH, retry_gate_review),
        (CANDIDATE_ONLY_REVIEW_PATH, candidate_only_review),
        (C5_READINESS_REVIEW_PATH, c5_review),
        (NONAUTHORITY_SAFETY_REVIEW_PATH, nonauthority_safety_review),
        (CLOSURE_CANDIDATE_PATH, closure_candidate),
        (DOWNSTREAM_DECISION_TABLE_PATH, downstream_decision_table),
        (CLASSIFICATION_PATH, classification),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (ROLLUP_OUT_PATH, rollup_out),
        (PROFILE_OUT_PATH, profile_out),
        (REPORT_OUT_PATH, report),
        (TRACE_OUT_PATH, trace),
    ]
    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "O2_REVIEW_0_BUILD_RECEIPT_CONSUMED": O2_BUILD_RECEIPT_PATH.exists(),
        "O2_REVIEW_1_REVIEW_ASSESSMENT_EMITTED": REVIEW_ASSESSMENT_PATH.exists(),
        "O2_REVIEW_2_SCHEMA_ARTIFACTS_PRESENT": schema_review["schema_count"] == 8,
        "O2_REVIEW_3_TEN_DEMO_EVENTS_REVIEWED": len(demo_events) == 10,
        "O2_REVIEW_4_TEN_FEEDBACK_RECORDS_REVIEWED": len(feedback) == 10,
        "O2_REVIEW_5_NO_BARE_FAILURE_SURVIVES": weak_feedback_review["bare_failed_status_count"] == 0 and weak_feedback_review["no_feedback_count"] == 0 and weak_feedback_review["status_only_count"] == 0,
        "O2_REVIEW_6_WEAK_FEEDBACK_INTENTIONAL_TYPED": weak_feedback_review["weak_feedback_count"] == 3 and weak_feedback_review["under_typed_feedback_count"] == 2 and weak_feedback_review["ambiguous_requires_question_count"] == 1,
        "O2_REVIEW_7_EXPECTED_LIMITS_SEPARATED_FROM_BUGS": expected_limit_review["expected_limit_count"] == 1 and expected_limit_review["expected_limit_counted_as_bug_count"] == 0,
        "O2_REVIEW_8_RETRY_GATES_BLOCK_UNCHANGED_RETRY": retry_gate_review["retry_blocked_count"] == 10 and retry_gate_review["retry_allowed_without_refinement_count"] == 0,
        "O2_REVIEW_9_REFINEMENT_CANDIDATES_PROPOSED_ONLY": candidate_only_review["all_refinement_candidates_proposed_only"] is True,
        "O2_REVIEW_10_MISSING_CAPABILITIES_CANDIDATE_ONLY": candidate_only_review["all_missing_capabilities_candidate_only"] is True,
        "O2_REVIEW_11_C5_BLOCKED_BY_WEAK_FEEDBACK": c5_review["c5_feedback_readiness"] == "BLOCKED_BY_WEAK_FEEDBACK",
        "O2_REVIEW_12_NONAUTHORITY_SAFETY_PASS": nonauthority_safety_review["review_status"] == "NONAUTHORITY_SAFETY_REVIEW_PASS",
        "O2_REVIEW_13_NO_LIVE_FEEDBACK_AUDIT": rollup_out["live_feedback_audit_executed_count"] == 0,
        "O2_REVIEW_14_NO_REPAIR_APPLIED": rollup_out["repair_applied_count"] == 0,
        "O2_REVIEW_15_NO_RETRY_EXECUTED": rollup_out["retry_executed_count"] == 0,
        "O2_REVIEW_16_NO_TARGET_SELECTED_FOR_BUILD": rollup_out["target_selected_for_build_count"] == 0,
        "O2_REVIEW_17_NO_RUNTIME_PATCH": rollup_out["runtime_patch_count"] == 0,
        "O2_REVIEW_18_NO_SOURCE_MUTATION": rollup_out["source_mutated_count"] == 0 and rollup_out["prior_receipt_mutated_count"] == 0,
        "O2_REVIEW_19_NO_ARCHITECTURE_CHANGE": rollup_out["architecture_change_count"] == 0,
        "O2_REVIEW_20_NO_C5_OPENED": rollup_out["c5_opened_count"] == 0,
        "O2_REVIEW_21_NO_LATEST_OR_MTIME": rollup_out["latest_file_guessing_count"] == 0 and rollup_out["mtime_selection_count"] == 0,
        "O2_REVIEW_22_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "O2_REVIEW_23_CLOSURE_CANDIDATE_EMITTED": closure_candidate["closure_candidate_status"] == "O2_CLOSURE_CANDIDATE_READY_WITH_WEAK_FEEDBACK_NOTE",
        "O2_REVIEW_24_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_OUT_PATH.exists() and PROFILE_OUT_PATH.exists() and REPORT_OUT_PATH.exists() and TRACE_OUT_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_O2_UNIT_FEEDBACK_HARDENING_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sha8({
        "unit_id": UNIT_ID,
        "status": status,
        "review_pass": review_pass,
        "weak": rollup.get("weak_feedback_count"),
        "c5": readout.get("c5_feedback_readiness"),
        "gate": gate,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "o2_unit_feedback_hardening_review_receipt_v0",
        "receipt_type": "TYPED_O2_UNIT_FEEDBACK_HARDENING_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_o2_build_receipt_id": O2_BUILD_RECEIPT_ID,
        "machine_readable_o2_review_summary": {
            "status": status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "o2_review_complete": review_pass,
            "o2_review_pass": review_pass,
            "schemas_reviewed": len(schemas),
            "demo_events_reviewed": len(demo_events),
            "feedback_records_reviewed": len(feedback),
            "weak_feedback_intentional": review_pass,
            "weak_feedback_count": rollup.get("weak_feedback_count"),
            "bare_failed_status_count": rollup.get("bare_failed_status_count"),
            "no_feedback_count": quality_counts.get("NO_FEEDBACK", 0),
            "status_only_count": quality_counts.get("STATUS_ONLY", 0),
            "under_typed_feedback_count": quality_counts.get("UNDER_TYPED_FEEDBACK", 0),
            "ambiguous_requires_question_count": quality_counts.get("AMBIGUOUS_REQUIRES_QUESTION", 0),
            "expected_limit_count": quality_counts.get("EXPECTED_LIMIT", 0),
            "retry_blocked_count": rollup.get("retry_blocked_count"),
            "refinement_candidates_proposed_only": candidate_only_review["all_refinement_candidates_proposed_only"],
            "missing_capabilities_candidate_only": candidate_only_review["all_missing_capabilities_candidate_only"],
            "c5_feedback_readiness": readout.get("c5_feedback_readiness"),
            "closure_candidate_ready": review_pass,
            "live_feedback_audit_executed": False,
            "repair_applied": False,
            "retry_executed": False,
            "target_selected_for_build": False,
            "runtime_patch_applied": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "architecture_change": False,
            "c5_opened": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": profile_out["bad_counters_zero"],
            "recommended_next": recommended_next,
        },
        "aggregate_metrics": report,
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "review_assessment": rel(REVIEW_ASSESSMENT_PATH),
            "schema_review": rel(SCHEMA_REVIEW_PATH),
            "feedback_record_review": rel(FEEDBACK_RECORD_REVIEW_PATH),
            "weak_feedback_review": rel(WEAK_FEEDBACK_REVIEW_PATH),
            "expected_limit_review": rel(EXPECTED_LIMIT_REVIEW_PATH),
            "retry_gate_review": rel(RETRY_GATE_REVIEW_PATH),
            "candidate_only_review": rel(CANDIDATE_ONLY_REVIEW_PATH),
            "c5_readiness_review": rel(C5_READINESS_REVIEW_PATH),
            "nonauthority_safety_review": rel(NONAUTHORITY_SAFETY_REVIEW_PATH),
            "closure_candidate": rel(CLOSURE_CANDIDATE_PATH),
            "downstream_decision_table": rel(DOWNSTREAM_DECISION_TABLE_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "rollup": rel(ROLLUP_OUT_PATH),
            "profile": rel(PROFILE_OUT_PATH),
            "report": rel(REPORT_OUT_PATH),
            "transition_trace": rel(TRACE_OUT_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"o2_review_receipt_id={receipt_id}")
    print(f"o2_review_receipt_path={rel(receipt_path)}")
    print(f"o2_review_assessment_path={rel(REVIEW_ASSESSMENT_PATH)}")
    print(f"o2_schema_review_path={rel(SCHEMA_REVIEW_PATH)}")
    print(f"o2_feedback_record_review_path={rel(FEEDBACK_RECORD_REVIEW_PATH)}")
    print(f"o2_weak_feedback_review_path={rel(WEAK_FEEDBACK_REVIEW_PATH)}")
    print(f"o2_expected_limit_review_path={rel(EXPECTED_LIMIT_REVIEW_PATH)}")
    print(f"o2_retry_gate_review_path={rel(RETRY_GATE_REVIEW_PATH)}")
    print(f"o2_candidate_only_review_path={rel(CANDIDATE_ONLY_REVIEW_PATH)}")
    print(f"o2_c5_readiness_review_path={rel(C5_READINESS_REVIEW_PATH)}")
    print(f"o2_review_rollup_path={rel(ROLLUP_OUT_PATH)}")
    print(f"o2_review_profile_path={rel(PROFILE_OUT_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
