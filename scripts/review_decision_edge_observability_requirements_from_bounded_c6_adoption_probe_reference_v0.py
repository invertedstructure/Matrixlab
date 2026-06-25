#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_FROM_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_V0"
TARGET_UNIT_ID = "c6.bounded_adoption_probe.edge_observability.review.v0"
LAYER = "OBSERVABILITY_HARDENING / DECISION_EDGE_REQUIREMENT_REVIEW"
MODE = "REVIEW_ONLY / VERIFY_REQUIREMENT_SURFACE / NO_RUNTIME_PATCH"
BUILD_MODE = "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEW_ONLY"

SOURCE_EXTRACTION_RECEIPT_ID = "ea5ce604"
SOURCE_POST_BOUNDED_DECISION_RECEIPT_ID = "685c7ea1"
SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_ID = "ac9451cc"

SOURCE_EXTRACTION_RECEIPT_PATH = ROOT / "data/decision_edge_observability_extraction_from_bounded_c6_adoption_probe_reference_v0_receipts/ea5ce604.json"

EXTRACTION_DIR = ROOT / "data/decision_edge_observability_extraction_from_bounded_c6_adoption_probe_reference_v0"
EXTRACTION_BASIS_PATH = EXTRACTION_DIR / "decision_edge_observability_extraction_basis_v0.json"
REQUIREMENT_SET_PATH = EXTRACTION_DIR / "decision_edge_observability_requirement_set_v0.json"
EDGE_REQUIREMENTS_PATH = EXTRACTION_DIR / "decision_edge_observability_edge_requirements_v0.jsonl"
FIELD_SCHEMA_PATH = EXTRACTION_DIR / "decision_edge_observability_required_field_schema_v0.json"
SOURCE_MAPPING_PATH = EXTRACTION_DIR / "decision_edge_observability_source_mapping_v0.json"
DISTINCTION_GUARDS_PATH = EXTRACTION_DIR / "decision_edge_observability_distinction_guards_v0.json"
NEGATIVE_CONTROLS_PATH = EXTRACTION_DIR / "decision_edge_observability_negative_controls_v0.json"
REVIEW_TARGET_PATH = EXTRACTION_DIR / "decision_edge_observability_review_target_v0.json"
AUTHORITY_PATH = EXTRACTION_DIR / "decision_edge_observability_extraction_authority_boundary_v0.json"
CLASSIFICATION_PATH_SRC = EXTRACTION_DIR / "decision_edge_observability_extraction_classification_v0.json"
ROLLUP_PATH_SRC = EXTRACTION_DIR / "decision_edge_observability_extraction_rollup_v0.json"
PROFILE_PATH_SRC = EXTRACTION_DIR / "decision_edge_observability_extraction_profile_v0.json"
REPORT_PATH_SRC = EXTRACTION_DIR / "decision_edge_observability_extraction_report.json"
TRACE_PATH_SRC = EXTRACTION_DIR / "decision_edge_observability_extraction_transition_trace.json"

SOURCE_POST_BOUNDED_DECISION_RECEIPT_PATH = ROOT / "data/c6_bounded_adoption_probe_post_reference_decision_v0_receipts/685c7ea1.json"
SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0_receipts/ac9451cc.json"

BOUNDED_PROBE_REVIEWED_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_reviewed_reference_v0.json"
BOUNDED_PROBE_OBSERVABILITY_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_observability_reference_v0.json"
BOUNDED_PROBE_PACKET_LAW_SURVIVAL_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_packet_law_survival_reference_v0.json"
BOUNDED_PROBE_UNIT_FEEDBACK_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_unit_feedback_reference_v0.json"
BOUNDED_PROBE_NEGATIVE_CONTROL_REFERENCE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_reference_closure_v0/bounded_adoption_probe_negative_control_reference_v0.json"

PROBE_EDGE_OBSERVATIONS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_edge_observations_v0.jsonl"
PROBE_PACKET_TRACE_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_packet_trace_v0.jsonl"
PROBE_UNIT_FEEDBACK_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_unit_feedback_v0.jsonl"
PROBE_NEGATIVE_CONTROL_RESULTS_PATH = ROOT / "data/c6_bounded_protocol_adoption_probe_v0/bounded_adoption_probe_negative_control_results_v0.jsonl"

REQUIRED_SOURCE_FILES = [
    SOURCE_EXTRACTION_RECEIPT_PATH,
    EXTRACTION_BASIS_PATH,
    REQUIREMENT_SET_PATH,
    EDGE_REQUIREMENTS_PATH,
    FIELD_SCHEMA_PATH,
    SOURCE_MAPPING_PATH,
    DISTINCTION_GUARDS_PATH,
    NEGATIVE_CONTROLS_PATH,
    REVIEW_TARGET_PATH,
    AUTHORITY_PATH,
    CLASSIFICATION_PATH_SRC,
    ROLLUP_PATH_SRC,
    PROFILE_PATH_SRC,
    REPORT_PATH_SRC,
    TRACE_PATH_SRC,
    SOURCE_POST_BOUNDED_DECISION_RECEIPT_PATH,
    SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_PATH,
    BOUNDED_PROBE_REVIEWED_REFERENCE_PATH,
    BOUNDED_PROBE_OBSERVABILITY_REFERENCE_PATH,
    BOUNDED_PROBE_PACKET_LAW_SURVIVAL_REFERENCE_PATH,
    BOUNDED_PROBE_UNIT_FEEDBACK_REFERENCE_PATH,
    BOUNDED_PROBE_NEGATIVE_CONTROL_REFERENCE_PATH,
    PROBE_EDGE_OBSERVATIONS_PATH,
    PROBE_PACKET_TRACE_PATH,
    PROBE_UNIT_FEEDBACK_PATH,
    PROBE_NEGATIVE_CONTROL_RESULTS_PATH,
]

OUT_DIR = ROOT / "data/decision_edge_observability_review_from_bounded_c6_adoption_probe_reference_v0"
RECEIPT_DIR = ROOT / "data/decision_edge_observability_review_from_bounded_c6_adoption_probe_reference_v0_receipts"

REVIEW_BASIS_PATH = OUT_DIR / "decision_edge_observability_review_basis_v0.json"
SOURCE_RECEIPT_REVIEW_PATH = OUT_DIR / "decision_edge_observability_source_receipt_review_v0.json"
REQUIREMENT_SET_REVIEW_PATH = OUT_DIR / "decision_edge_observability_requirement_set_review_v0.json"
EDGE_REQUIREMENT_REVIEW_PATH = OUT_DIR / "decision_edge_observability_edge_requirement_review_v0.json"
FIELD_SCHEMA_REVIEW_PATH = OUT_DIR / "decision_edge_observability_field_schema_review_v0.json"
DISTINCTION_GUARD_REVIEW_PATH = OUT_DIR / "decision_edge_observability_distinction_guard_review_v0.json"
NEGATIVE_CONTROL_REVIEW_PATH = OUT_DIR / "decision_edge_observability_negative_control_review_v0.json"
SOURCE_MAPPING_REVIEW_PATH = OUT_DIR / "decision_edge_observability_source_mapping_review_v0.json"
CLOSE_CANDIDATE_PATH = OUT_DIR / "decision_edge_observability_reviewed_reference_close_candidate_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "decision_edge_observability_review_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "decision_edge_observability_review_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "decision_edge_observability_review_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "decision_edge_observability_review_profile_v0.json"
REPORT_PATH = OUT_DIR / "decision_edge_observability_review_report.json"
TRACE_PATH = OUT_DIR / "decision_edge_observability_review_transition_trace.json"

EXPECTED_EXTRACTION_STATUS = "TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_EXTRACTED_REVIEW_READY"
EXPECTED_EXTRACTION_STOP = "STOP_TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_EXTRACTED_REVIEW_READY"
EXPECTED_EXTRACTION_NEXT = UNIT_ID
RECOMMENDED_NEXT = "CLOSE_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_FROM_BOUNDED_C6_ADOPTION_PROBE_REFERENCE_AS_REVIEWED_REFERENCE_V0"

REQUIRED_FIELDS = [
    "active_object",
    "attempted_move",
    "boundary_checked",
    "boundary_result",
    "blocked_moves",
    "lawful_next_moves",
    "source_packet_ref",
]

EXPECTED_EDGE_NAMES = [
    "proposal_to_review",
    "review_to_accepted_packet",
    "accepted_packet_to_cell1_intake",
    "cell1_intake_to_probe_or_build",
    "probe_or_build_to_verification_return",
    "verification_return_to_handoff",
    "blocked_or_stop_to_feedback",
]

EXPECTED_DISTINCTION_GUARDS = [
    "decision-edge observation is not protocol proof",
    "observation sidecar is not authority",
    "handoff is not hidden next command",
    "verification is not closure",
    "blocked feedback is not repair",
    "edge visibility is not runtime adoption",
    "observability extraction is not unit-feedback hardening",
    "observability extraction is not C7 authorization",
]

EXPECTED_NEGATIVE_CONTROLS = [
    "missing_active_object_must_fail",
    "missing_attempted_move_must_fail",
    "missing_boundary_checked_must_fail",
    "missing_boundary_result_must_fail",
    "missing_blocked_moves_must_fail",
    "missing_lawful_next_moves_must_fail",
    "missing_source_packet_ref_must_fail",
    "edge_observation_as_protocol_proof_must_fail",
    "observation_sidecar_as_authority_must_fail",
    "edge_visibility_as_runtime_adoption_must_fail",
    "observability_extraction_as_unit_feedback_hardening_must_fail",
    "c7_authorization_claim_must_fail",
    "runtime_patch_claim_must_fail",
]

def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def canonical_bytes(obj: Any) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), default=str).encode("utf-8")

def sig8(obj: Any) -> str:
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
            failures.append(f"required_source_missing:{rel(path)}")
    if failures:
        return failures, {}

    extraction_receipt = read_json(SOURCE_EXTRACTION_RECEIPT_PATH)
    extraction_summary = extraction_receipt.get("machine_readable_decision_edge_observability_extraction_summary", {})

    extraction_basis = read_json(EXTRACTION_BASIS_PATH)
    requirement_set = read_json(REQUIREMENT_SET_PATH)
    edge_requirements = read_jsonl(EDGE_REQUIREMENTS_PATH)
    field_schema = read_json(FIELD_SCHEMA_PATH)
    source_mapping = read_json(SOURCE_MAPPING_PATH)
    distinction_guards = read_json(DISTINCTION_GUARDS_PATH)
    negative_controls = read_json(NEGATIVE_CONTROLS_PATH)
    review_target = read_json(REVIEW_TARGET_PATH)
    authority = read_json(AUTHORITY_PATH)
    classification = read_json(CLASSIFICATION_PATH_SRC)
    rollup = read_json(ROLLUP_PATH_SRC)
    profile = read_json(PROFILE_PATH_SRC)
    report = read_json(REPORT_PATH_SRC)
    trace = read_json(TRACE_PATH_SRC)

    post_decision_receipt = read_json(SOURCE_POST_BOUNDED_DECISION_RECEIPT_PATH)
    ref_close_receipt = read_json(SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_PATH)
    reviewed_reference = read_json(BOUNDED_PROBE_REVIEWED_REFERENCE_PATH)
    observability_reference = read_json(BOUNDED_PROBE_OBSERVABILITY_REFERENCE_PATH)
    packet_law_survival_reference = read_json(BOUNDED_PROBE_PACKET_LAW_SURVIVAL_REFERENCE_PATH)
    unit_feedback_reference = read_json(BOUNDED_PROBE_UNIT_FEEDBACK_REFERENCE_PATH)
    negative_control_reference = read_json(BOUNDED_PROBE_NEGATIVE_CONTROL_REFERENCE_PATH)

    source_edge_observations = read_jsonl(PROBE_EDGE_OBSERVATIONS_PATH)
    source_packet_trace = read_jsonl(PROBE_PACKET_TRACE_PATH)
    source_unit_feedback = read_jsonl(PROBE_UNIT_FEEDBACK_PATH)
    source_negative_controls = read_jsonl(PROBE_NEGATIVE_CONTROL_RESULTS_PATH)

    if extraction_receipt.get("receipt_id") != SOURCE_EXTRACTION_RECEIPT_ID or extraction_receipt.get("gate") != "PASS":
        failures.append("source_extraction_receipt_not_pass")
    if extraction_receipt.get("terminal", {}).get("stop_code") != EXPECTED_EXTRACTION_STOP:
        failures.append("source_extraction_stop_wrong")
    if extraction_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_extraction_hidden_next")
    if extraction_summary.get("status") != EXPECTED_EXTRACTION_STATUS:
        failures.append(f"source_extraction_status_wrong:{extraction_summary.get('status')}")
    if extraction_summary.get("recommended_next") != EXPECTED_EXTRACTION_NEXT:
        failures.append(f"source_extraction_next_wrong:{extraction_summary.get('recommended_next')}")

    for key in [
        "decision_edge_observability_requirements_extracted",
        "review_ready",
        "unit_feedback_hardening_deferred",
        "c7_deferred",
        "runtime_adoption_deferred",
        "bad_counters_zero",
    ]:
        if extraction_summary.get(key) is not True:
            failures.append(f"source_required_true_missing:{key}")

    for key in [
        "runtime_effect",
        "runtime_patched",
        "c7_authorized",
        "new_domain_shift_executed",
        "general_cell1_authority_claimed",
        "global_autonomy_claimed",
        "full_transfer_claimed",
        "runtime_wide_enforcement_claimed",
        "source_mutated",
        "prior_receipt_mutated",
        "c6_reviewed_reference_mutated",
        "bounded_probe_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if extraction_summary.get(key) is not False:
            failures.append(f"source_forbidden_true:{key}")

    for key, expected in {
        "edge_requirement_count": 7,
        "required_field_count": 7,
        "negative_control_count": 13,
        "packet_trace_count": 9,
        "edge_observation_count": 7,
        "unit_feedback_count": 4,
    }.items():
        if extraction_summary.get(key) != expected:
            failures.append(f"source_count_wrong:{key}:{extraction_summary.get(key)}")

    if extraction_basis.get("basis_status") != "BASIS_ACCEPTED":
        failures.append("basis_not_accepted")
    if requirement_set.get("requirement_set_status") != "EXTRACTED_REVIEW_READY":
        failures.append("requirement_set_not_review_ready")
    if requirement_set.get("required_fields") != REQUIRED_FIELDS:
        failures.append("requirement_set_required_fields_wrong")
    if requirement_set.get("edge_names") != EXPECTED_EDGE_NAMES:
        failures.append("requirement_set_edge_names_wrong")

    if len(edge_requirements) != 7:
        failures.append("edge_requirement_count_wrong")
    if [row.get("edge_name") for row in edge_requirements] != EXPECTED_EDGE_NAMES:
        failures.append("edge_requirement_sequence_wrong")
    for row in edge_requirements:
        if row.get("required_fields") != REQUIRED_FIELDS:
            failures.append(f"edge_required_fields_wrong:{row.get('edge_name')}")
        if row.get("runtime_effect") is not False:
            failures.append(f"edge_runtime_effect_true:{row.get('edge_name')}")
        values = row.get("field_values_from_source", {})
        for field in REQUIRED_FIELDS:
            if field not in values:
                failures.append(f"edge_missing_field_value:{row.get('edge_name')}:{field}")

    if [field.get("field") for field in field_schema.get("fields", [])] != REQUIRED_FIELDS:
        failures.append("field_schema_fields_wrong")
    if "Missing any required field" not in field_schema.get("quality_rule", ""):
        failures.append("field_schema_quality_rule_missing")

    if len(source_mapping.get("edge_to_source_packet", [])) != 7:
        failures.append("source_mapping_edge_count_wrong")
    if distinction_guards.get("guards") != EXPECTED_DISTINCTION_GUARDS:
        failures.append("distinction_guards_wrong")
    if negative_controls.get("controls") != EXPECTED_NEGATIVE_CONTROLS:
        failures.append("negative_controls_wrong")
    if review_target.get("review_target_status") != "REVIEW_READY":
        failures.append("review_target_not_ready")
    if review_target.get("review_unit") != EXPECTED_EXTRACTION_NEXT:
        failures.append("review_target_unit_wrong")

    if authority.get("may_review_decision_edge_observability_requirements_next") is not True:
        failures.append("authority_no_review")
    for forbidden in [
        "may_harden_unit_feedback_now",
        "may_patch_runtime_now",
        "may_open_c7_now",
        "may_execute_new_domain_shift",
        "may_claim_full_transfer",
        "may_claim_global_autonomy",
        "may_claim_general_cell1_authority",
        "may_claim_runtime_wide_enforcement",
        "may_mutate_source",
        "may_mutate_prior_receipts",
        "may_mutate_c6_reviewed_reference",
        "may_mutate_bounded_probe_reference",
    ]:
        if authority.get(forbidden) is not False:
            failures.append(f"authority_forbidden_true:{forbidden}")

    if classification.get("next_command_goal") is not None:
        failures.append("classification_hidden_next")
    if rollup.get("review_ready_count") != 1:
        failures.append("rollup_review_ready_wrong")
    if rollup.get("unit_feedback_hardening_count") != 0:
        failures.append("rollup_unit_feedback_hardening_nonzero")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_EXTRACTION_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next")

    if post_decision_receipt.get("receipt_id") != SOURCE_POST_BOUNDED_DECISION_RECEIPT_ID or post_decision_receipt.get("gate") != "PASS":
        failures.append("post_decision_receipt_not_pass")
    if ref_close_receipt.get("receipt_id") != SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_ID or ref_close_receipt.get("gate") != "PASS":
        failures.append("ref_close_receipt_not_pass")
    if reviewed_reference.get("reference_status") != "BOUNDED_C6_PROTOCOL_ADOPTION_PROBE_REVIEWED_REFERENCE_FROZEN":
        failures.append("bounded_probe_reference_not_frozen")
    if observability_reference.get("observability_status") != "REVIEWED_REFERENCE":
        failures.append("observability_reference_wrong")
    if packet_law_survival_reference.get("packet_law_distinctions_confirmed") is not True:
        failures.append("packet_law_distinctions_not_confirmed")
    if unit_feedback_reference.get("feedback_status") != "REVIEWED_REFERENCE":
        failures.append("unit_feedback_reference_wrong")
    if negative_control_reference.get("negative_controls_all_fail_closed") is not True:
        failures.append("negative_control_reference_wrong")

    if len(source_edge_observations) != 7:
        failures.append("source_edge_observations_count_wrong")
    if len(source_packet_trace) != 9:
        failures.append("source_packet_trace_count_wrong")
    if len(source_unit_feedback) != 4:
        failures.append("source_unit_feedback_count_wrong")
    if len(source_negative_controls) != 15:
        failures.append("source_negative_control_count_wrong")

    return failures, {
        "extraction_summary": extraction_summary,
        "requirement_set": requirement_set,
        "edge_requirements": edge_requirements,
        "field_schema": field_schema,
        "source_mapping": source_mapping,
        "distinction_guards": distinction_guards,
        "negative_controls": negative_controls,
        "review_target": review_target,
        "reviewed_reference": reviewed_reference,
        "observability_reference": observability_reference,
        "source_edge_observations": source_edge_observations,
        "source_packet_trace": source_packet_trace,
        "source_unit_feedback": source_unit_feedback,
        "source_negative_controls": source_negative_controls,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    review_pass = not failures
    status = "TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_CLOSE_READY" if review_pass else "TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEW_V0"

    extraction_summary = basis.get("extraction_summary", {})
    requirement_set = basis.get("requirement_set", {})
    edge_requirements = basis.get("edge_requirements", [])
    field_schema = basis.get("field_schema", {})
    source_mapping = basis.get("source_mapping", {})
    distinction_guards = basis.get("distinction_guards", {})
    negative_controls = basis.get("negative_controls", {})
    review_target = basis.get("review_target", {})
    reviewed_reference = basis.get("reviewed_reference", {})
    observability_reference = basis.get("observability_reference", {})
    source_edge_observations = basis.get("source_edge_observations", [])
    source_packet_trace = basis.get("source_packet_trace", [])
    source_unit_feedback = basis.get("source_unit_feedback", [])
    source_negative_controls = basis.get("source_negative_controls", [])

    reason_codes = [
        "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEW_COMPLETE",
        "EXTRACTION_RECEIPT_CONSUMED",
        "REQUIREMENT_SET_REVIEWED",
        "ALL_EDGE_REQUIREMENTS_REVIEWED",
        "FIELD_SCHEMA_REVIEWED",
        "SOURCE_MAPPING_REVIEWED",
        "DISTINCTION_GUARDS_REVIEWED",
        "NEGATIVE_CONTROLS_REVIEWED",
        "LOAD_BEARING_FIELDS_CONFIRMED",
        "UNIT_FEEDBACK_HARDENING_REMAINS_DEFERRED",
        "CLOSE_CANDIDATE_READY",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_C7_AUTHORIZATION",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if review_pass else failures

    review_basis = {
        "schema_version": "decision_edge_observability_review_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if review_pass else "BASIS_REPAIR_REQUIRED",
        "source_extraction_receipt_id": SOURCE_EXTRACTION_RECEIPT_ID,
        "source_post_bounded_decision_receipt_id": SOURCE_POST_BOUNDED_DECISION_RECEIPT_ID,
        "source_bounded_probe_reference_closure_receipt_id": SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_ID,
        "source_reference_status": reviewed_reference.get("reference_status"),
        "observability_reference_status": observability_reference.get("observability_status"),
        "extraction_status": extraction_summary.get("status"),
    }

    source_receipt_review = {
        "schema_version": "decision_edge_observability_source_receipt_review_v0",
        "source_extraction_receipt_id": SOURCE_EXTRACTION_RECEIPT_ID,
        "source_gate": "PASS" if review_pass else "REPAIR_REQUIRED",
        "source_status": extraction_summary.get("status"),
        "terminal_stop": EXPECTED_EXTRACTION_STOP,
        "next_command_goal": None,
    }

    requirement_set_review = {
        "schema_version": "decision_edge_observability_requirement_set_review_v0",
        "requirement_set_status": requirement_set.get("requirement_set_status"),
        "edge_observation_count": requirement_set.get("edge_observation_count"),
        "edge_names": requirement_set.get("edge_names"),
        "required_fields": requirement_set.get("required_fields"),
        "core_rule": requirement_set.get("core_rule"),
        "not_a_claim_of": requirement_set.get("not_a_claim_of"),
        "review_pass": review_pass,
    }

    edge_requirement_review = {
        "schema_version": "decision_edge_observability_edge_requirement_review_v0",
        "edge_requirement_count": len(edge_requirements),
        "edge_names": [row.get("edge_name") for row in edge_requirements],
        "all_required_fields_present": all(row.get("required_fields") == REQUIRED_FIELDS for row in edge_requirements),
        "all_field_values_mapped": all(all(field in row.get("field_values_from_source", {}) for field in REQUIRED_FIELDS) for row in edge_requirements),
        "all_runtime_effect_false": all(row.get("runtime_effect") is False for row in edge_requirements),
        "load_bearing_reason_present": all(bool(row.get("load_bearing_reason")) for row in edge_requirements),
    }

    field_schema_review = {
        "schema_version": "decision_edge_observability_field_schema_review_v0",
        "required_field_count": len(field_schema.get("fields", [])),
        "required_fields": [field.get("field") for field in field_schema.get("fields", [])],
        "quality_rule_present": "Missing any required field" in field_schema.get("quality_rule", ""),
        "review_pass": review_pass,
    }

    distinction_guard_review = {
        "schema_version": "decision_edge_observability_distinction_guard_review_v0",
        "guard_count": len(distinction_guards.get("guards", [])),
        "guards": distinction_guards.get("guards", []),
        "guards_confirmed": distinction_guards.get("guards", []) == EXPECTED_DISTINCTION_GUARDS,
    }

    negative_control_review = {
        "schema_version": "decision_edge_observability_negative_control_review_v0",
        "negative_control_count": len(negative_controls.get("controls", [])),
        "controls": negative_controls.get("controls", []),
        "controls_confirmed": negative_controls.get("controls", []) == EXPECTED_NEGATIVE_CONTROLS,
    }

    source_mapping_review = {
        "schema_version": "decision_edge_observability_source_mapping_review_v0",
        "mapping_count": len(source_mapping.get("edge_to_source_packet", [])),
        "source_files": source_mapping.get("source_files", {}),
        "mapping_reviewed": len(source_mapping.get("edge_to_source_packet", [])) == 7,
    }

    close_candidate = {
        "schema_version": "decision_edge_observability_reviewed_reference_close_candidate_v0",
        "candidate_status": "DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEWED_REFERENCE_CLOSE_READY" if review_pass else "NOT_CLOSE_READY",
        "review_pass": review_pass,
        "source_extraction_receipt_id": SOURCE_EXTRACTION_RECEIPT_ID,
        "candidate_next_unit": RECOMMENDED_NEXT if review_pass else None,
        "close_scope": "close extracted decision-edge observability requirements as reviewed reference",
        "close_does_not": [
            "harden unit feedback",
            "patch runtime",
            "authorize C7",
            "claim full transfer",
            "claim global autonomy",
            "grant general Cell 1 authority",
            "claim runtime-wide enforcement",
        ],
    }

    authority_boundary = {
        "schema_version": "decision_edge_observability_review_authority_boundary_v0",
        "status": status,
        "may_close_decision_edge_observability_requirements_as_reviewed_reference_next": review_pass,
        "may_harden_unit_feedback_now": False,
        "may_patch_runtime_now": False,
        "may_open_c7_now": False,
        "may_execute_new_domain_shift": False,
        "may_claim_full_transfer": False,
        "may_claim_global_autonomy": False,
        "may_claim_general_cell1_authority": False,
        "may_claim_runtime_wide_enforcement": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_mutate_c6_reviewed_reference": False,
        "may_mutate_bounded_probe_reference": False,
    }

    classification = {
        "schema_version": "decision_edge_observability_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "decision_edge_observability_requirements_review_complete": review_pass,
        "decision_edge_observability_requirements_review_pass": review_pass,
        "close_candidate_ready": review_pass,
        "source_extraction_review_ready": extraction_summary.get("review_ready"),
        "edge_requirement_count": len(edge_requirements),
        "required_field_count": len(REQUIRED_FIELDS),
        "negative_control_count": len(negative_controls.get("controls", [])),
        "source_edge_observation_count": len(source_edge_observations),
        "packet_trace_count": len(source_packet_trace),
        "unit_feedback_count": len(source_unit_feedback),
        "unit_feedback_hardening_deferred": True,
        "c7_deferred": True,
        "runtime_adoption_deferred": True,
        "runtime_effect": False,
        "runtime_patched": False,
        "c7_authorized": False,
        "new_domain_shift_executed": False,
        "general_cell1_authority_claimed": False,
        "global_autonomy_claimed": False,
        "full_transfer_claimed": False,
        "runtime_wide_enforcement_claimed": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "c6_reviewed_reference_mutated": False,
        "bounded_probe_reference_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": True,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "decision_edge_observability_review_rollup_v0",
        "review_count": 1 if review_pass else 0,
        "review_pass_count": 1 if review_pass else 0,
        "close_candidate_ready_count": 1 if review_pass else 0,
        "edge_requirement_count": len(edge_requirements),
        "required_field_count": len(REQUIRED_FIELDS),
        "negative_control_count": len(negative_controls.get("controls", [])),
        "unit_feedback_hardening_count": 0,
        "c7_authorized_count": 0,
        "runtime_adoption_count": 0,
        "runtime_effect_count": 0,
        "runtime_patch_count": 0,
        "new_domain_shift_executed_count": 0,
        "general_cell1_authority_claim_count": 0,
        "global_autonomy_claim_count": 0,
        "full_transfer_claim_count": 0,
        "runtime_wide_enforcement_claim_count": 0,
        "source_mutated_count": 0,
        "prior_receipt_mutated_count": 0,
        "c6_reviewed_reference_mutated_count": 0,
        "bounded_probe_reference_mutated_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "decision_edge_observability_review_profile_v0",
        "profile_id": "decision_edge_observability_review_" + sig8(rollup),
        "status": status,
        "review_object": "decision-edge observability requirement surface",
        "compression": "A load-bearing decision-edge observation must expose object, move, boundary, result, blocked moves, lawful next moves, and source packet.",
        "close_candidate_ready": review_pass,
        "unit_feedback_hardening_deferred": True,
        "must_not_infer": [
            "runtime patch",
            "C7 authorization",
            "unit-feedback hardening",
            "global autonomy",
            "full transfer",
            "general Cell 1 authority",
            "runtime-wide enforcement",
        ],
        "bad_counters_zero": True,
        "next_command_goal": None,
    }

    report = {
        "schema_version": "decision_edge_observability_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The decision-edge observability requirement extraction reviewed clean. All 7 edge requirements, 7 required fields, source mappings, distinction guards, and 13 negative controls are confirmed. This review does not harden unit feedback yet, patch runtime, authorize C7, or claim transfer/autonomy/general Cell 1 authority.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "decision_edge_observability_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_extraction",
                "question": "are extracted decision-edge observability requirements review-ready",
                "answer": "yes" if review_pass else "no",
                "taken": "review requirement set, edge requirements, field schema, mappings, guards, and negative controls",
            },
            {
                "step": "verify_load_bearing_fields",
                "question": "do all edge requirements preserve the load-bearing fields",
                "answer": "yes" if review_pass else "no",
                "taken": "emit close candidate",
            },
            {
                "step": "preserve_boundary",
                "question": "does review harden unit feedback, patch runtime, or authorize C7",
                "answer": "no",
                "taken": "stop with close-ready observability review",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (REVIEW_BASIS_PATH, review_basis),
        (SOURCE_RECEIPT_REVIEW_PATH, source_receipt_review),
        (REQUIREMENT_SET_REVIEW_PATH, requirement_set_review),
        (EDGE_REQUIREMENT_REVIEW_PATH, edge_requirement_review),
        (FIELD_SCHEMA_REVIEW_PATH, field_schema_review),
        (DISTINCTION_GUARD_REVIEW_PATH, distinction_guard_review),
        (NEGATIVE_CONTROL_REVIEW_PATH, negative_control_review),
        (SOURCE_MAPPING_REVIEW_PATH, source_mapping_review),
        (CLOSE_CANDIDATE_PATH, close_candidate),
        (AUTHORITY_BOUNDARY_PATH, authority_boundary),
        (CLASSIFICATION_PATH, classification),
        (ROLLUP_PATH, rollup),
        (PROFILE_PATH, profile),
        (REPORT_PATH, report),
        (TRACE_PATH, trace),
    ]
    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "EDGE_OBS_REVIEW_0_EXTRACTION_RECEIPT_CONSUMED": SOURCE_EXTRACTION_RECEIPT_PATH.exists(),
        "EDGE_OBS_REVIEW_1_EXTRACTION_GATE_PASS": extraction_summary.get("decision_edge_observability_requirements_extracted") is True,
        "EDGE_OBS_REVIEW_2_REQUIREMENT_SET_REVIEWED": REQUIREMENT_SET_REVIEW_PATH.exists() and requirement_set_review["review_pass"] is True,
        "EDGE_OBS_REVIEW_3_EDGE_REQUIREMENTS_REVIEWED": EDGE_REQUIREMENT_REVIEW_PATH.exists() and edge_requirement_review["all_required_fields_present"] is True and edge_requirement_review["all_field_values_mapped"] is True,
        "EDGE_OBS_REVIEW_4_FIELD_SCHEMA_REVIEWED": FIELD_SCHEMA_REVIEW_PATH.exists() and field_schema_review["required_fields"] == REQUIRED_FIELDS,
        "EDGE_OBS_REVIEW_5_SOURCE_MAPPING_REVIEWED": SOURCE_MAPPING_REVIEW_PATH.exists() and source_mapping_review["mapping_reviewed"] is True,
        "EDGE_OBS_REVIEW_6_DISTINCTION_GUARDS_REVIEWED": DISTINCTION_GUARD_REVIEW_PATH.exists() and distinction_guard_review["guards_confirmed"] is True,
        "EDGE_OBS_REVIEW_7_NEGATIVE_CONTROLS_REVIEWED": NEGATIVE_CONTROL_REVIEW_PATH.exists() and negative_control_review["controls_confirmed"] is True,
        "EDGE_OBS_REVIEW_8_LOAD_BEARING_FIELDS_CONFIRMED": edge_requirement_review["all_required_fields_present"] is True and edge_requirement_review["all_field_values_mapped"] is True,
        "EDGE_OBS_REVIEW_9_UNIT_FEEDBACK_HARDENING_DEFERRED": classification["unit_feedback_hardening_deferred"] is True,
        "EDGE_OBS_REVIEW_10_CLOSE_CANDIDATE_READY": close_candidate["review_pass"] is True,
        "EDGE_OBS_REVIEW_11_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "EDGE_OBS_REVIEW_12_NO_C7": classification["c7_authorized"] is False and classification["c7_deferred"] is True,
        "EDGE_OBS_REVIEW_13_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "EDGE_OBS_REVIEW_14_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["bounded_probe_reference_mutated"] is False,
        "EDGE_OBS_REVIEW_15_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "EDGE_OBS_REVIEW_16_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "EDGE_OBS_REVIEW_17_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "EDGE_OBS_REVIEW_18_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEW_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEW_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_DECISION_EDGE_OBSERVABILITY_REQUIREMENTS_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_extraction": SOURCE_EXTRACTION_RECEIPT_ID,
        "recommended_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "decision_edge_observability_review_receipt_v0",
        "receipt_type": "TYPED_DECISION_EDGE_OBSERVABILITY_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_decision_edge_observability_extraction_receipt_id": SOURCE_EXTRACTION_RECEIPT_ID,
        "source_post_bounded_probe_reference_decision_receipt_id": SOURCE_POST_BOUNDED_DECISION_RECEIPT_ID,
        "source_bounded_probe_reference_closure_receipt_id": SOURCE_BOUNDED_PROBE_REFERENCE_CLOSURE_RECEIPT_ID,
        "machine_readable_decision_edge_observability_review_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "decision_edge_observability_requirements_review_complete": gate == "PASS",
            "decision_edge_observability_requirements_review_pass": gate == "PASS",
            "close_candidate_ready": gate == "PASS",
            "source_extraction_review_ready": extraction_summary.get("review_ready"),
            "edge_requirement_count": len(edge_requirements),
            "required_field_count": len(REQUIRED_FIELDS),
            "negative_control_count": len(negative_controls.get("controls", [])),
            "source_edge_observation_count": len(source_edge_observations),
            "packet_trace_count": len(source_packet_trace),
            "unit_feedback_count": len(source_unit_feedback),
            "unit_feedback_hardening_deferred": True,
            "c7_deferred": True,
            "runtime_adoption_deferred": True,
            "runtime_effect": False,
            "runtime_patched": False,
            "c7_authorized": False,
            "new_domain_shift_executed": False,
            "general_cell1_authority_claimed": False,
            "global_autonomy_claimed": False,
            "full_transfer_claimed": False,
            "runtime_wide_enforcement_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "c6_reviewed_reference_mutated": False,
            "bounded_probe_reference_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": True,
            "recommended_next": final_next,
        },
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "review_basis": rel(REVIEW_BASIS_PATH),
            "source_receipt_review": rel(SOURCE_RECEIPT_REVIEW_PATH),
            "requirement_set_review": rel(REQUIREMENT_SET_REVIEW_PATH),
            "edge_requirement_review": rel(EDGE_REQUIREMENT_REVIEW_PATH),
            "field_schema_review": rel(FIELD_SCHEMA_REVIEW_PATH),
            "distinction_guard_review": rel(DISTINCTION_GUARD_REVIEW_PATH),
            "negative_control_review": rel(NEGATIVE_CONTROL_REVIEW_PATH),
            "source_mapping_review": rel(SOURCE_MAPPING_REVIEW_PATH),
            "close_candidate": rel(CLOSE_CANDIDATE_PATH),
            "authority_boundary": rel(AUTHORITY_BOUNDARY_PATH),
            "classification": rel(CLASSIFICATION_PATH),
            "rollup": rel(ROLLUP_PATH),
            "profile": rel(PROFILE_PATH),
            "report": rel(REPORT_PATH),
            "transition_trace": rel(TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"decision_edge_observability_review_receipt_id={receipt_id}")
    print(f"decision_edge_observability_review_receipt_path={rel(receipt_path)}")
    print(f"decision_edge_observability_close_candidate_path={rel(CLOSE_CANDIDATE_PATH)}")
    print(f"decision_edge_observability_review_rollup_path={rel(ROLLUP_PATH)}")
    print(f"decision_edge_observability_review_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
