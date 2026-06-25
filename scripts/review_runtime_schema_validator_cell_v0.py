#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "REVIEW_RUNTIME_SCHEMA_VALIDATOR_CELL_V0"
TARGET_UNIT_ID = "runtime.schema_validator_cell.review.v0"
LAYER = "RUNTIME / SIEVE_1 / REVIEW"
MODE = "REVIEW_ONLY / SYNTHETIC_FORMATION_SIEVE / NO_RUNTIME_PATCH"
BUILD_MODE = "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEW_ONLY"

SOURCE_BUILD_RECEIPT_ID = "3fe3a57f"
SOURCE_REPAIR_RECEIPT_ID = "604607c2"
SOURCE_FAILED_BUILD_RECEIPT_ID = "008f621c"
SOURCE_DESIGN_RECEIPT_ID = "ccbf5723"
SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID = "ac09c2e3"

BUILD_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_v0_receipts/3fe3a57f.json"
REPAIR_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_build_repair_v0_receipts/604607c2.json"
FAILED_BUILD_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_v0_receipts/008f621c.json"
DESIGN_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_target_from_reviewed_observability_reference_v0_receipts/ccbf5723.json"
EDGE_OBS_REF_CLOSE_RECEIPT_PATH = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0_receipts/ac09c2e3.json"

SRC_DIR = ROOT / "data/runtime_schema_validator_cell_v0"
REPAIR_DIR = ROOT / "data/runtime_schema_validator_cell_build_repair_v0"
DESIGN_DIR = ROOT / "data/runtime_schema_validator_cell_target_from_reviewed_observability_reference_v0"

SOURCE_ARTIFACTS = [
    SRC_DIR / "schema_archive_schema_v0.json",
    SRC_DIR / "schema_archive_v0.json",
    SRC_DIR / "schema_validation_result_enum_v0.json",
    SRC_DIR / "schema_validation_result_schema_v0.json",
    SRC_DIR / "validated_candidate_packet_schema_v0.json",
    SRC_DIR / "schema_feedback_packet_schema_v0.json",
    SRC_DIR / "schema_gap_feedback_packet_schema_v0.json",
    SRC_DIR / "schema_validator_cell_receipt_schema_v0.json",
    SRC_DIR / "schema_validator_check_table_v0.json",
    SRC_DIR / "schema_validator_demo_inputs_v0.jsonl",
    SRC_DIR / "schema_validation_results_v0.jsonl",
    SRC_DIR / "validated_candidate_packets_v0.jsonl",
    SRC_DIR / "schema_feedback_packets_v0.jsonl",
    SRC_DIR / "schema_gap_feedback_packets_v0.jsonl",
    SRC_DIR / "schema_validator_rollup_v0.json",
    SRC_DIR / "schema_validator_readout_v0.json",
    SRC_DIR / "schema_validator_profile_v0.json",
    SRC_DIR / "schema_validator_report.json",
    SRC_DIR / "schema_validator_transition_trace.json",
    REPAIR_DIR / "build_script_patch_record_v0.json",
    REPAIR_DIR / "runtime_schema_validator_build_repair_basis_v0.json",
    REPAIR_DIR / "runtime_schema_validator_build_repair_classification_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_target_spec_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_build_target_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_dependency_park_v0.json",
]

REQUIRED_SOURCE_FILES = [
    BUILD_RECEIPT_PATH,
    REPAIR_RECEIPT_PATH,
    FAILED_BUILD_RECEIPT_PATH,
    DESIGN_RECEIPT_PATH,
    EDGE_OBS_REF_CLOSE_RECEIPT_PATH,
] + SOURCE_ARTIFACTS

OUT_DIR = ROOT / "data/runtime_schema_validator_cell_review_v0"
RECEIPT_DIR = ROOT / "data/runtime_schema_validator_cell_review_v0_receipts"

REVIEW_BASIS_PATH = OUT_DIR / "runtime_schema_validator_review_basis_v0.json"
SOURCE_BUILD_RECEIPT_REVIEW_PATH = OUT_DIR / "runtime_schema_validator_source_build_receipt_review_v0.json"
SOURCE_REPAIR_RECEIPT_REVIEW_PATH = OUT_DIR / "runtime_schema_validator_source_repair_receipt_review_v0.json"
SOURCE_FAILED_BUILD_REVIEW_PATH = OUT_DIR / "runtime_schema_validator_failed_build_review_v0.json"
ARTIFACT_INVENTORY_PATH = OUT_DIR / "runtime_schema_validator_artifact_inventory_review_v0.json"
SCHEMA_SURFACE_REVIEW_PATH = OUT_DIR / "runtime_schema_validator_schema_surface_review_v0.json"
DEMO_RESULT_REVIEW_PATH = OUT_DIR / "runtime_schema_validator_demo_result_review_v0.json"
PACKET_ROUTING_REVIEW_PATH = OUT_DIR / "runtime_schema_validator_packet_routing_review_v0.json"
NEGATIVE_CONTROL_REVIEW_PATH = OUT_DIR / "runtime_schema_validator_negative_control_review_v0.json"
BOUNDARY_REVIEW_PATH = OUT_DIR / "runtime_schema_validator_boundary_review_v0.json"
OBSERVABILITY_ALIGNMENT_REVIEW_PATH = OUT_DIR / "runtime_schema_validator_observability_alignment_review_v0.json"
REVIEWED_REFERENCE_CLOSE_CANDIDATE_PATH = OUT_DIR / "runtime_schema_validator_reviewed_reference_close_candidate_v0.json"
REVIEW_AUTHORITY_BOUNDARY_PATH = OUT_DIR / "runtime_schema_validator_review_authority_boundary_v0.json"
REVIEW_CLASSIFICATION_PATH = OUT_DIR / "runtime_schema_validator_review_classification_v0.json"
REVIEW_ROLLUP_PATH = OUT_DIR / "runtime_schema_validator_review_rollup_v0.json"
REVIEW_PROFILE_PATH = OUT_DIR / "runtime_schema_validator_review_profile_v0.json"
REVIEW_REPORT_PATH = OUT_DIR / "runtime_schema_validator_review_report.json"
REVIEW_TRACE_PATH = OUT_DIR / "runtime_schema_validator_review_transition_trace.json"

EXPECTED_BUILD_STATUS = "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_BUILT_REVIEW_READY"
EXPECTED_BUILD_STOP = "STOP_TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_BUILT_REVIEW_READY"
EXPECTED_BUILD_NEXT = UNIT_ID

EXPECTED_REPAIR_STOP = "STOP_RUNTIME_SCHEMA_VALIDATOR_BUILD_REPAIR_PATCHED_RERUN_READY"

RECOMMENDED_NEXT = "CLOSE_RUNTIME_SCHEMA_VALIDATOR_CELL_AS_REVIEWED_REFERENCE_V0"

REQUIRED_EDGE_FIELDS = [
    "active_object",
    "attempted_move",
    "boundary_checked",
    "boundary_result",
    "blocked_moves",
    "lawful_next_moves",
    "source_packet_ref",
]

EXPECTED_RESULT_COUNTS = {
    "VALID": 2,
    "UNRESOLVED_REFERENCE": 3,
    "BOUNDARY_CONFLICT": 1,
    "BOUNDARY_MISSING": 1,
    "DISTINGUISHABILITY_INSUFFICIENT": 1,
    "HIDDEN_EXECUTION_FIELD": 1,
    "LAYER_COLLAPSE_IN_PAYLOAD": 1,
    "MISSING_FIELD": 1,
    "RECEIPT_CONTRACT_INSUFFICIENT": 1,
    "SCHEMA_VERSION_MISMATCH": 1,
    "TYPE_MISMATCH": 1,
    "UNKNOWN_MOVE_TYPE": 1,
    "UNKNOWN_SCHEMA": 1,
}

EXPECTED_DEMO_TOTAL = 16
EXPECTED_VALID = 2
EXPECTED_INVALID = 14
EXPECTED_ADVANCED = 2
EXPECTED_RETURNED = 14

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

    build_receipt = read_json(BUILD_RECEIPT_PATH)
    build_summary = build_receipt.get("machine_readable_schema_validator_build_summary", {})
    repair_receipt = read_json(REPAIR_RECEIPT_PATH)
    failed_receipt = read_json(FAILED_BUILD_RECEIPT_PATH)
    design_receipt = read_json(DESIGN_RECEIPT_PATH)
    edge_obs_receipt = read_json(EDGE_OBS_REF_CLOSE_RECEIPT_PATH)

    schema_archive_schema = read_json(SRC_DIR / "schema_archive_schema_v0.json")
    schema_archive = read_json(SRC_DIR / "schema_archive_v0.json")
    result_enum = read_json(SRC_DIR / "schema_validation_result_enum_v0.json")
    result_schema = read_json(SRC_DIR / "schema_validation_result_schema_v0.json")
    validated_packet_schema = read_json(SRC_DIR / "validated_candidate_packet_schema_v0.json")
    schema_feedback_schema = read_json(SRC_DIR / "schema_feedback_packet_schema_v0.json")
    schema_gap_feedback_schema = read_json(SRC_DIR / "schema_gap_feedback_packet_schema_v0.json")
    receipt_schema = read_json(SRC_DIR / "schema_validator_cell_receipt_schema_v0.json")
    check_table = read_json(SRC_DIR / "schema_validator_check_table_v0.json")
    rollup = read_json(SRC_DIR / "schema_validator_rollup_v0.json")
    readout = read_json(SRC_DIR / "schema_validator_readout_v0.json")
    profile = read_json(SRC_DIR / "schema_validator_profile_v0.json")
    report = read_json(SRC_DIR / "schema_validator_report.json")
    trace = read_json(SRC_DIR / "schema_validator_transition_trace.json")
    demo_inputs = read_jsonl(SRC_DIR / "schema_validator_demo_inputs_v0.jsonl")
    validation_results = read_jsonl(SRC_DIR / "schema_validation_results_v0.jsonl")
    validated_packets = read_jsonl(SRC_DIR / "validated_candidate_packets_v0.jsonl")
    schema_feedback_packets = read_jsonl(SRC_DIR / "schema_feedback_packets_v0.jsonl")
    schema_gap_feedback_packets = read_jsonl(SRC_DIR / "schema_gap_feedback_packets_v0.jsonl")

    patch_record = read_json(REPAIR_DIR / "build_script_patch_record_v0.json")
    repair_basis = read_json(REPAIR_DIR / "runtime_schema_validator_build_repair_basis_v0.json")
    repair_classification = read_json(REPAIR_DIR / "runtime_schema_validator_build_repair_classification_v0.json")
    design_target = read_json(DESIGN_DIR / "runtime_schema_validator_cell_target_spec_v0.json")
    sidecar_dependency_park = read_json(DESIGN_DIR / "runtime_observability_sidecar_dependency_park_v0.json")

    if build_receipt.get("receipt_id") != SOURCE_BUILD_RECEIPT_ID or build_receipt.get("gate") != "PASS":
        failures.append("source_build_receipt_not_pass")
    if build_receipt.get("terminal", {}).get("stop_code") != EXPECTED_BUILD_STOP:
        failures.append("source_build_stop_wrong")
    if build_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("source_build_hidden_next")
    if build_summary.get("status") != EXPECTED_BUILD_STATUS:
        failures.append(f"source_build_status_wrong:{build_summary.get('status')}")
    if build_summary.get("recommended_next") != EXPECTED_BUILD_NEXT:
        failures.append(f"source_build_next_wrong:{build_summary.get('recommended_next')}")

    for key in [
        "runtime_schema_validator_cell_built",
        "review_ready",
        "synthetic_demo_build_only",
        "source_design_consumed",
        "schema_archive_schema_emitted",
        "schema_archive_emitted",
        "schema_archive_read_only",
        "schema_validation_result_enum_emitted",
        "schema_validation_result_schema_emitted",
        "validated_candidate_packet_schema_emitted",
        "schema_feedback_packet_schema_emitted",
        "schema_gap_feedback_packet_schema_emitted",
        "schema_validator_receipt_schema_emitted",
        "check_table_emitted",
        "demo_inputs_emitted",
        "validation_results_emitted",
        "validated_candidate_packets_emitted",
        "schema_feedback_packets_emitted",
        "schema_gap_feedback_packets_emitted",
        "observability_sidecar_deferred",
        "unit_feedback_hardening_deferred",
        "c7_deferred",
        "c8_deferred",
        "runtime_adoption_deferred",
        "bad_counters_zero",
    ]:
        if build_summary.get(key) is not True:
            failures.append(f"build_required_true_missing:{key}")

    for key in [
        "live_runtime_routing_installed",
        "runtime_effect",
        "runtime_patched",
        "authority_checked",
        "admissibility_checked",
        "execution_claimed",
        "schema_archive_mutated",
        "proposal_repaired",
        "schema_created",
        "builder_command_emitted",
        "c7_authorized",
        "c8_authorized",
        "new_domain_shift_executed",
        "general_cell1_authority_claimed",
        "global_autonomy_claimed",
        "full_transfer_claimed",
        "runtime_wide_enforcement_claimed",
        "source_mutated",
        "prior_receipt_mutated",
        "observability_reference_mutated",
        "hidden_next_command",
        "latest_file_guessing",
        "mtime_selection",
    ]:
        if build_summary.get(key) is not False:
            failures.append(f"build_forbidden_true:{key}")

    for key, expected in {
        "proposals_evaluated": EXPECTED_DEMO_TOTAL,
        "valid_count": EXPECTED_VALID,
        "invalid_count": EXPECTED_INVALID,
        "advanced_to_admissibility_count": EXPECTED_ADVANCED,
        "returned_to_builder_count": EXPECTED_RETURNED,
        "formation_check_count": 15,
        "result_enum_count": 19,
        "acceptance_gate_count": 33,
        "negative_control_count": 19,
    }.items():
        if build_summary.get(key) != expected:
            failures.append(f"build_count_wrong:{key}:{build_summary.get(key)}")

    if build_summary.get("result_class_counts") != EXPECTED_RESULT_COUNTS:
        failures.append("result_class_counts_wrong")

    if repair_receipt.get("receipt_id") != SOURCE_REPAIR_RECEIPT_ID or repair_receipt.get("gate") != "PASS":
        failures.append("repair_receipt_not_pass")
    if repair_receipt.get("terminal", {}).get("stop_code") != EXPECTED_REPAIR_STOP:
        failures.append("repair_stop_wrong")
    repair_summary = repair_receipt.get("repair_summary", {})
    if repair_summary.get("from_result") != "FORBIDDEN_FIELD" or repair_summary.get("to_result") != "HIDDEN_EXECUTION_FIELD":
        failures.append("repair_classification_wrong")
    if repair_summary.get("repair_applied") is not True:
        failures.append("repair_not_applied")

    failed_summary = failed_receipt.get("machine_readable_schema_validator_build_summary", {})
    if failed_receipt.get("receipt_id") != SOURCE_FAILED_BUILD_RECEIPT_ID or failed_receipt.get("gate") != "FAIL":
        failures.append("failed_build_receipt_wrong")
    if "demo_case_expected_HIDDEN_EXECUTION_FIELD_got_FORBIDDEN_FIELD:hidden_execution_field" not in failed_receipt.get("failures", []):
        failures.append("failed_build_target_failure_missing")

    if design_receipt.get("receipt_id") != SOURCE_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("design_receipt_not_pass")
    if edge_obs_receipt.get("receipt_id") != SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID or edge_obs_receipt.get("gate") != "PASS":
        failures.append("edge_observability_receipt_not_pass")

    if schema_archive_schema.get("mutation_allowed_by_schema_validator") is not False:
        failures.append("schema_archive_schema_allows_mutation")
    if schema_archive.get("mutation_allowed_by_schema_validator") is not False:
        failures.append("schema_archive_allows_mutation")
    if len(schema_archive.get("schemas", [])) != 1:
        failures.append("schema_archive_schema_count_wrong")
    if result_enum.get("closed_results") and len(result_enum.get("closed_results", [])) != 19:
        failures.append("result_enum_count_wrong")
    if result_enum.get("only_advancing_result") != "VALID":
        failures.append("result_enum_advancing_wrong")
    if len(check_table.get("checks", [])) != 15:
        failures.append("check_table_count_wrong")
    if check_table.get("only_valid_advances") is not True:
        failures.append("check_table_only_valid_wrong")

    if rollup.get("proposals_evaluated") != EXPECTED_DEMO_TOTAL:
        failures.append("rollup_demo_total_wrong")
    if rollup.get("valid_count") != EXPECTED_VALID or rollup.get("invalid_count") != EXPECTED_INVALID:
        failures.append("rollup_valid_invalid_wrong")
    if rollup.get("advanced_to_admissibility_count") != EXPECTED_ADVANCED or rollup.get("returned_to_builder_count") != EXPECTED_RETURNED:
        failures.append("rollup_routing_wrong")
    if rollup.get("result_class_counts") != EXPECTED_RESULT_COUNTS:
        failures.append("rollup_result_counts_wrong")
    if not all(v == 0 for v in rollup.get("negative_controls", {}).values()):
        failures.append("rollup_negative_controls_not_zero")

    if readout.get("bad_counters_zero") is not True:
        failures.append("readout_bad_counters_not_zero")
    if profile.get("status") != "SCHEMA_VALIDATOR_STABLE":
        failures.append(f"profile_status_wrong:{profile.get('status')}")
    if profile.get("schema_archive_mutation_allowed") is not False:
        failures.append("profile_schema_archive_mutation_allowed")
    if profile.get("authority_checked") is not False or profile.get("execution_allowed") is not False:
        failures.append("profile_boundary_wrong")
    if profile.get("next_command_goal") is not None:
        failures.append("profile_hidden_next")
    if report.get("recommended_next_handling") != EXPECTED_BUILD_NEXT:
        failures.append("report_next_wrong")
    if trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("trace_hidden_next")

    if len(demo_inputs) != EXPECTED_DEMO_TOTAL:
        failures.append("demo_input_count_wrong")
    if len(validation_results) != EXPECTED_DEMO_TOTAL:
        failures.append("validation_result_count_wrong")
    if len(validated_packets) != EXPECTED_VALID:
        failures.append("validated_packet_count_wrong")
    if len(schema_feedback_packets) + len(schema_gap_feedback_packets) != EXPECTED_INVALID:
        failures.append("feedback_packet_count_wrong")

    hidden_results = [r for r in validation_results if r.get("input_proposal_ref") == "proposal_hidden_execution_field"]
    if not hidden_results or hidden_results[0].get("result") != "HIDDEN_EXECUTION_FIELD":
        failures.append("hidden_execution_demo_not_classified_correctly")

    valid_results = [r for r in validation_results if r.get("result") == "VALID"]
    if any(r.get("return_to") != "LAWFUL_ADMISSIBILITY_CELL" for r in valid_results):
        failures.append("valid_result_did_not_advance_to_admissibility")
    invalid_results = [r for r in validation_results if r.get("result") != "VALID"]
    if any(r.get("return_to") != "BUILDER_PROPOSAL_CELL" for r in invalid_results):
        failures.append("invalid_result_did_not_return_to_builder")

    if patch_record.get("repair_status") != "PATCH_APPLIED":
        failures.append("patch_record_not_applied")
    if repair_basis.get("repair_target") != "hidden_execution classification precedence":
        failures.append("repair_basis_target_wrong")
    if repair_classification.get("classification_status") != "PATCHED_RERUN_READY":
        failures.append("repair_classification_status_wrong")
    if design_target.get("mode") != "VALIDATE / CLASSIFY / FORMATION_ONLY":
        failures.append("design_target_mode_wrong")
    if sidecar_dependency_park.get("park_status") != "PARKED_UNTIL_SCHEMA_VALIDATOR_REFERENCE_EXISTS":
        failures.append("sidecar_dependency_park_wrong")

    return failures, {
        "build_receipt": build_receipt,
        "build_summary": build_summary,
        "repair_receipt": repair_receipt,
        "failed_receipt": failed_receipt,
        "design_receipt": design_receipt,
        "edge_obs_receipt": edge_obs_receipt,
        "schema_archive": schema_archive,
        "result_enum": result_enum,
        "check_table": check_table,
        "rollup": rollup,
        "readout": readout,
        "profile": profile,
        "report": report,
        "trace": trace,
        "validation_results": validation_results,
        "validated_packets": validated_packets,
        "schema_feedback_packets": schema_feedback_packets,
        "schema_gap_feedback_packets": schema_gap_feedback_packets,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    review_pass = not failures
    status = "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_CLOSE_READY" if review_pass else "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEW_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if review_pass else "REPAIR_RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEW_V0"

    build_summary = basis.get("build_summary", {})
    repair_receipt = basis.get("repair_receipt", {})
    failed_receipt = basis.get("failed_receipt", {})
    rollup = basis.get("rollup", {})
    readout = basis.get("readout", {})
    profile = basis.get("profile", {})
    validation_results = basis.get("validation_results", [])
    validated_packets = basis.get("validated_packets", [])
    schema_feedback_packets = basis.get("schema_feedback_packets", [])
    schema_gap_feedback_packets = basis.get("schema_gap_feedback_packets", [])

    reason_codes = [
        "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED",
        "BUILD_RECEIPT_CONSUMED",
        "REPAIR_RECEIPT_CONSUMED",
        "FAILED_BUILD_RECEIPT_CONSUMED_AS_REPAIR_CONTEXT",
        "SCHEMA_SURFACE_REVIEWED",
        "DEMO_RESULTS_REVIEWED",
        "HIDDEN_EXECUTION_CLASSIFICATION_REPAIRED_AND_CONFIRMED",
        "ONLY_VALID_ADVANCES_CONFIRMED",
        "INVALID_RETURNS_TO_BUILDER_CONFIRMED",
        "UNKNOWN_SCHEMA_STOP_CONFIRMED",
        "SCHEMA_ARCHIVE_READ_ONLY_CONFIRMED",
        "NEGATIVE_CONTROLS_ZERO_CONFIRMED",
        "SYNTHETIC_DEMO_BUILD_ONLY_CONFIRMED",
        "SIDE_CAR_DEFERRED_UNTIL_SCHEMA_VALIDATOR_REFERENCE_EXISTS",
        "C8_DEFERRED",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_LIVE_RUNTIME_ROUTING",
        "NO_AUTHORITY_CHECK",
        "NO_ADMISSIBILITY_CHECK",
        "NO_EXECUTION_CLAIM",
        "NO_SCHEMA_ARCHIVE_MUTATION",
        "NO_PROPOSAL_REPAIR",
        "NO_SCHEMA_CREATION",
        "NO_BUILDER_COMMAND",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if review_pass else failures

    artifact_inventory = {
        "schema_version": "runtime_schema_validator_artifact_inventory_review_v0",
        "inventory_status": "COMPLETE" if review_pass else "REPAIR_REQUIRED",
        "source_artifact_count": len(SOURCE_ARTIFACTS),
        "source_artifacts": [
            {"path": rel(path), "sha256": file_sha256(path)}
            for path in SOURCE_ARTIFACTS
        ],
    }

    review_basis = {
        "schema_version": "runtime_schema_validator_review_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if review_pass else "BASIS_REPAIR_REQUIRED",
        "source_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "source_failed_build_receipt_id": SOURCE_FAILED_BUILD_RECEIPT_ID,
        "source_design_receipt_id": SOURCE_DESIGN_RECEIPT_ID,
        "source_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "review_scope": "review synthetic Schema Validator Cell build surface for close readiness",
    }

    source_build_receipt_review = {
        "schema_version": "runtime_schema_validator_source_build_receipt_review_v0",
        "source_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_gate": "PASS" if review_pass else "REPAIR_REQUIRED",
        "status": build_summary.get("status"),
        "synthetic_demo_build_only": build_summary.get("synthetic_demo_build_only"),
        "review_ready": build_summary.get("review_ready"),
        "recommended_next": build_summary.get("recommended_next"),
        "terminal_hidden_next": False,
    }

    source_repair_receipt_review = {
        "schema_version": "runtime_schema_validator_source_repair_receipt_review_v0",
        "source_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "source_gate": repair_receipt.get("gate"),
        "repair_applied": repair_receipt.get("repair_summary", {}).get("repair_applied"),
        "from_result": repair_receipt.get("repair_summary", {}).get("from_result"),
        "to_result": repair_receipt.get("repair_summary", {}).get("to_result"),
        "boundary_clean": repair_receipt.get("repair_summary", {}).get("bad_counters_zero") is True,
    }

    failed_build_review = {
        "schema_version": "runtime_schema_validator_failed_build_review_v0",
        "source_failed_build_receipt_id": SOURCE_FAILED_BUILD_RECEIPT_ID,
        "source_gate": failed_receipt.get("gate"),
        "repair_context_only": True,
        "target_failure": "demo_case_expected_HIDDEN_EXECUTION_FIELD_got_FORBIDDEN_FIELD:hidden_execution_field",
        "target_failure_present": "demo_case_expected_HIDDEN_EXECUTION_FIELD_got_FORBIDDEN_FIELD:hidden_execution_field" in failed_receipt.get("failures", []),
        "superseded_by_pass_receipt_id": SOURCE_BUILD_RECEIPT_ID,
    }

    schema_surface_review = {
        "schema_version": "runtime_schema_validator_schema_surface_review_v0",
        "schema_surface_status": "REVIEWED_OK" if review_pass else "REPAIR_REQUIRED",
        "schema_archive_read_only": build_summary.get("schema_archive_read_only"),
        "schema_archive_schema_emitted": build_summary.get("schema_archive_schema_emitted"),
        "schema_archive_emitted": build_summary.get("schema_archive_emitted"),
        "schema_validation_result_enum_emitted": build_summary.get("schema_validation_result_enum_emitted"),
        "schema_validation_result_schema_emitted": build_summary.get("schema_validation_result_schema_emitted"),
        "validated_candidate_packet_schema_emitted": build_summary.get("validated_candidate_packet_schema_emitted"),
        "schema_feedback_packet_schema_emitted": build_summary.get("schema_feedback_packet_schema_emitted"),
        "schema_gap_feedback_packet_schema_emitted": build_summary.get("schema_gap_feedback_packet_schema_emitted"),
        "schema_validator_receipt_schema_emitted": build_summary.get("schema_validator_receipt_schema_emitted"),
        "check_table_emitted": build_summary.get("check_table_emitted"),
        "formation_check_count": build_summary.get("formation_check_count"),
        "result_enum_count": build_summary.get("result_enum_count"),
    }

    demo_result_review = {
        "schema_version": "runtime_schema_validator_demo_result_review_v0",
        "demo_result_status": "REVIEWED_OK" if review_pass else "REPAIR_REQUIRED",
        "proposals_evaluated": build_summary.get("proposals_evaluated"),
        "valid_count": build_summary.get("valid_count"),
        "invalid_count": build_summary.get("invalid_count"),
        "advanced_to_admissibility_count": build_summary.get("advanced_to_admissibility_count"),
        "returned_to_builder_count": build_summary.get("returned_to_builder_count"),
        "result_class_counts": build_summary.get("result_class_counts"),
        "hidden_execution_demo_result": "HIDDEN_EXECUTION_FIELD",
        "validated_packet_count": len(validated_packets),
        "schema_feedback_packet_count": len(schema_feedback_packets),
        "schema_gap_feedback_packet_count": len(schema_gap_feedback_packets),
    }

    packet_routing_review = {
        "schema_version": "runtime_schema_validator_packet_routing_review_v0",
        "routing_status": "REVIEWED_OK" if review_pass else "REPAIR_REQUIRED",
        "only_valid_advances": True if review_pass else False,
        "valid_advances_to": "LAWFUL_ADMISSIBILITY_CELL",
        "invalid_returns_to": "BUILDER_PROPOSAL_CELL",
        "valid_count": EXPECTED_VALID,
        "advanced_count": EXPECTED_ADVANCED,
        "invalid_count": EXPECTED_INVALID,
        "returned_count": EXPECTED_RETURNED,
        "authority_status_after_validation": "NOT_CHECKED",
        "admissibility_status_after_validation": "NOT_CHECKED",
        "execution_status_after_validation": "NOT_EXECUTED",
    }

    negative_control_review = {
        "schema_version": "runtime_schema_validator_negative_control_review_v0",
        "negative_control_status": "ZERO_CONFIRMED" if review_pass else "REPAIR_REQUIRED",
        "negative_controls": rollup.get("negative_controls", {}),
        "bad_counters_zero": readout.get("bad_counters_zero"),
    }

    boundary_review = {
        "schema_version": "runtime_schema_validator_boundary_review_v0",
        "boundary_status": "BOUNDARY_HELD" if review_pass else "REPAIR_REQUIRED",
        "synthetic_demo_build_only": build_summary.get("synthetic_demo_build_only"),
        "live_runtime_routing_installed": build_summary.get("live_runtime_routing_installed"),
        "runtime_effect": build_summary.get("runtime_effect"),
        "runtime_patched": build_summary.get("runtime_patched"),
        "authority_checked": build_summary.get("authority_checked"),
        "admissibility_checked": build_summary.get("admissibility_checked"),
        "execution_claimed": build_summary.get("execution_claimed"),
        "schema_archive_mutated": build_summary.get("schema_archive_mutated"),
        "proposal_repaired": build_summary.get("proposal_repaired"),
        "schema_created": build_summary.get("schema_created"),
        "builder_command_emitted": build_summary.get("builder_command_emitted"),
        "c7_authorized": build_summary.get("c7_authorized"),
        "c8_authorized": build_summary.get("c8_authorized"),
        "observability_sidecar_deferred": build_summary.get("observability_sidecar_deferred"),
        "runtime_adoption_deferred": build_summary.get("runtime_adoption_deferred"),
        "hidden_next_command": build_summary.get("hidden_next_command"),
    }

    observability_alignment_review = {
        "schema_version": "runtime_schema_validator_observability_alignment_review_v0",
        "alignment_status": "REVIEWED_OK" if review_pass else "REPAIR_REQUIRED",
        "source_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "preserved_load_bearing_edge_fields": REQUIRED_EDGE_FIELDS,
        "schema_validator_surface_observable_events": [
            "schema_validation_started",
            "schema_loaded",
            "schema_validation_check_completed",
            "schema_validation_result",
            "validated_candidate_packet_emitted",
            "schema_feedback_packet_emitted",
            "schema_gap_feedback_packet_emitted",
            "schema_validator_receipt_emitted",
        ],
        "sidecar_dependency": "Observability Sidecar remains deferred until Schema Validator reviewed reference exists.",
    }

    close_candidate = {
        "schema_version": "runtime_schema_validator_reviewed_reference_close_candidate_v0",
        "candidate_status": "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_CLOSE_READY" if review_pass else "NOT_READY",
        "source_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "source_design_receipt_id": SOURCE_DESIGN_RECEIPT_ID,
        "recommended_close_unit": RECOMMENDED_NEXT if review_pass else None,
        "close_meaning": "freeze synthetic Schema Validator Cell surface as reviewed reference; not live runtime adoption",
    }

    review_authority = {
        "schema_version": "runtime_schema_validator_review_authority_boundary_v0",
        "status": status,
        "may_close_schema_validator_cell_as_reviewed_reference_next": review_pass,
        "may_build_or_patch_schema_validator_now": False,
        "may_design_observability_sidecar_now": False,
        "may_build_observability_sidecar_now": False,
        "may_install_live_runtime_routing": False,
        "may_patch_runtime_now": False,
        "may_check_authority": False,
        "may_check_admissibility": False,
        "may_execute": False,
        "may_repair_proposal": False,
        "may_mutate_schema_archive": False,
        "may_create_schema": False,
        "may_emit_builder_command": False,
        "may_open_c7_now": False,
        "may_open_c8_now": False,
        "may_execute_new_domain_shift": False,
        "may_claim_full_transfer": False,
        "may_claim_global_autonomy": False,
        "may_claim_general_cell1_authority": False,
        "may_claim_runtime_wide_enforcement": False,
        "may_mutate_source": False,
        "may_mutate_prior_receipts": False,
        "may_mutate_observability_reference": False,
    }

    classification = {
        "schema_version": "runtime_schema_validator_review_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "runtime_schema_validator_cell_reviewed": review_pass,
        "close_ready": review_pass,
        "source_build_receipt_consumed": True,
        "source_repair_receipt_consumed": True,
        "source_failed_build_receipt_consumed_as_context": True,
        "schema_surface_reviewed": review_pass,
        "demo_results_reviewed": review_pass,
        "hidden_execution_classification_confirmed": review_pass,
        "only_valid_advances_confirmed": review_pass,
        "invalid_returns_to_builder_confirmed": review_pass,
        "schema_archive_read_only_confirmed": review_pass,
        "negative_controls_zero_confirmed": review_pass,
        "synthetic_demo_build_only": True,
        "live_runtime_routing_installed": False,
        "observability_sidecar_deferred": True,
        "unit_feedback_hardening_deferred": True,
        "c7_deferred": True,
        "c8_deferred": True,
        "runtime_adoption_deferred": True,
        "runtime_effect": False,
        "runtime_patched": False,
        "authority_checked": False,
        "admissibility_checked": False,
        "execution_claimed": False,
        "schema_archive_mutated": False,
        "proposal_repaired": False,
        "schema_created": False,
        "builder_command_emitted": False,
        "c7_authorized": False,
        "c8_authorized": False,
        "new_domain_shift_executed": False,
        "general_cell1_authority_claimed": False,
        "global_autonomy_claimed": False,
        "full_transfer_claimed": False,
        "runtime_wide_enforcement_claimed": False,
        "source_mutated": False,
        "prior_receipt_mutated": False,
        "observability_reference_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": review_pass,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    review_rollup = {
        "schema_version": "runtime_schema_validator_review_rollup_v0",
        "review_count": 1 if review_pass else 0,
        "source_build_pass_count": 1 if review_pass else 0,
        "source_repair_pass_count": 1 if review_pass else 0,
        "schema_surface_reviewed_count": 1 if review_pass else 0,
        "demo_results_reviewed_count": 1 if review_pass else 0,
        "proposals_evaluated": build_summary.get("proposals_evaluated"),
        "valid_count": build_summary.get("valid_count"),
        "invalid_count": build_summary.get("invalid_count"),
        "advanced_to_admissibility_count": build_summary.get("advanced_to_admissibility_count"),
        "returned_to_builder_count": build_summary.get("returned_to_builder_count"),
        "hidden_execution_field_count": build_summary.get("result_class_counts", {}).get("HIDDEN_EXECUTION_FIELD"),
        "negative_controls_zero": readout.get("bad_counters_zero"),
        "runtime_patch_count": 0,
        "live_runtime_routing_installed_count": 0,
        "authority_checked_count": 0,
        "admissibility_checked_count": 0,
        "execution_claim_count": 0,
        "schema_archive_mutation_count": 0,
        "proposal_repair_count": 0,
        "schema_created_count": 0,
        "builder_command_emitted_count": 0,
        "c7_authorized_count": 0,
        "c8_authorized_count": 0,
        "sidecar_design_count": 0,
        "sidecar_build_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    review_profile = {
        "schema_version": "runtime_schema_validator_review_profile_v0",
        "profile_id": "runtime_schema_validator_review_" + sig8(review_rollup),
        "status": status,
        "cell_id": "SCHEMA_VALIDATOR_CELL",
        "review_result": "REVIEWED_CLOSE_READY" if review_pass else "REPAIR_REQUIRED",
        "core_rule": "Schema Validator Cell validates form. Lawful Admissibility Cell validates permission.",
        "valid_advances_only_to": "LAWFUL_ADMISSIBILITY_CELL",
        "invalid_returns_to": "BUILDER_PROPOSAL_CELL",
        "schema_archive_mutation_allowed": False,
        "authority_checked": False,
        "admissibility_checked": False,
        "execution_allowed": False,
        "synthetic_demo_build_only": True,
        "live_runtime_routing_installed": False,
        "bad_counters_zero": review_pass,
        "must_not_infer": [
            "Schema Validator is live runtime routing",
            "VALID means authorized",
            "VALID means admissible",
            "VALID means true",
            "VALID means useful",
            "VALID means execute",
            "feedback hint means repair applied",
            "Sidecar is designed",
            "C8 is authorized",
        ],
        "next_command_goal": None,
    }

    review_report = {
        "schema_version": "runtime_schema_validator_review_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The Runtime Schema Validator Cell synthetic surface has been reviewed and is close-ready. The review consumed the passing build receipt and the repair receipt, confirmed the hidden-execution classification repair, confirmed only VALID demo packets advance to Lawful Admissibility, confirmed invalid proposals return to Builder / Proposal Cell, confirmed read-only schema archive and zero negative controls, and confirmed no live routing, runtime patch, authority/admissibility/execution, proposal repair, schema mutation, Sidecar design, or C8 authorization.",
        "recommended_next_handling": recommended_next,
    }

    review_trace = {
        "schema_version": "runtime_schema_validator_review_transition_trace_v0",
        "trace": [
            {
                "step": "consume_schema_validator_build",
                "question": "did the repaired synthetic build pass",
                "answer": "yes" if review_pass else "no",
                "taken": "review emitted schema surface, demo results, packets, rollup, readout, profile",
            },
            {
                "step": "verify_repair",
                "question": "was hidden_execution classified as HIDDEN_EXECUTION_FIELD",
                "answer": "yes" if review_pass else "no",
                "taken": "confirm repair context and passing build supersedes failed build",
            },
            {
                "step": "verify_boundary",
                "question": "did review preserve no-live-runtime/no-authority/no-execution boundary",
                "answer": "yes" if review_pass else "no",
                "taken": "mark close-ready, not closed",
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
        (SOURCE_BUILD_RECEIPT_REVIEW_PATH, source_build_receipt_review),
        (SOURCE_REPAIR_RECEIPT_REVIEW_PATH, source_repair_receipt_review),
        (SOURCE_FAILED_BUILD_REVIEW_PATH, failed_build_review),
        (ARTIFACT_INVENTORY_PATH, artifact_inventory),
        (SCHEMA_SURFACE_REVIEW_PATH, schema_surface_review),
        (DEMO_RESULT_REVIEW_PATH, demo_result_review),
        (PACKET_ROUTING_REVIEW_PATH, packet_routing_review),
        (NEGATIVE_CONTROL_REVIEW_PATH, negative_control_review),
        (BOUNDARY_REVIEW_PATH, boundary_review),
        (OBSERVABILITY_ALIGNMENT_REVIEW_PATH, observability_alignment_review),
        (REVIEWED_REFERENCE_CLOSE_CANDIDATE_PATH, close_candidate),
        (REVIEW_AUTHORITY_BOUNDARY_PATH, review_authority),
        (REVIEW_CLASSIFICATION_PATH, classification),
        (REVIEW_ROLLUP_PATH, review_rollup),
        (REVIEW_PROFILE_PATH, review_profile),
        (REVIEW_REPORT_PATH, review_report),
        (REVIEW_TRACE_PATH, review_trace),
    ]

    for path, obj in artifacts:
        write_json(path, obj)

    acceptance_gate_results = {
        "SCHEMA_VALIDATOR_REVIEW_0_BUILD_RECEIPT_CONSUMED": BUILD_RECEIPT_PATH.exists(),
        "SCHEMA_VALIDATOR_REVIEW_1_REPAIR_RECEIPT_CONSUMED": REPAIR_RECEIPT_PATH.exists(),
        "SCHEMA_VALIDATOR_REVIEW_2_FAILED_BUILD_RECEIPT_CONSUMED_AS_CONTEXT": FAILED_BUILD_RECEIPT_PATH.exists(),
        "SCHEMA_VALIDATOR_REVIEW_3_SCHEMA_SURFACE_REVIEWED": schema_surface_review["schema_surface_status"] == "REVIEWED_OK",
        "SCHEMA_VALIDATOR_REVIEW_4_DEMO_RESULTS_REVIEWED": demo_result_review["demo_result_status"] == "REVIEWED_OK",
        "SCHEMA_VALIDATOR_REVIEW_5_HIDDEN_EXECUTION_CLASSIFICATION_CONFIRMED": demo_result_review["hidden_execution_demo_result"] == "HIDDEN_EXECUTION_FIELD",
        "SCHEMA_VALIDATOR_REVIEW_6_ONLY_VALID_ADVANCES_CONFIRMED": packet_routing_review["only_valid_advances"] is True,
        "SCHEMA_VALIDATOR_REVIEW_7_INVALID_RETURNS_TO_BUILDER_CONFIRMED": packet_routing_review["returned_count"] == EXPECTED_RETURNED,
        "SCHEMA_VALIDATOR_REVIEW_8_SCHEMA_ARCHIVE_READ_ONLY_CONFIRMED": schema_surface_review["schema_archive_read_only"] is True,
        "SCHEMA_VALIDATOR_REVIEW_9_NEGATIVE_CONTROLS_ZERO_CONFIRMED": negative_control_review["bad_counters_zero"] is True,
        "SCHEMA_VALIDATOR_REVIEW_10_OBSERVABILITY_ALIGNMENT_REVIEWED": observability_alignment_review["alignment_status"] == "REVIEWED_OK",
        "SCHEMA_VALIDATOR_REVIEW_11_CLOSE_CANDIDATE_EMITTED": close_candidate["candidate_status"] == "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_CLOSE_READY",
        "SCHEMA_VALIDATOR_REVIEW_12_NO_BUILD_OR_REPAIR_NOW": review_authority["may_build_or_patch_schema_validator_now"] is False,
        "SCHEMA_VALIDATOR_REVIEW_13_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "SCHEMA_VALIDATOR_REVIEW_14_NO_LIVE_RUNTIME_ROUTING": classification["live_runtime_routing_installed"] is False,
        "SCHEMA_VALIDATOR_REVIEW_15_NO_AUTHORITY_ADMISSIBILITY_OR_EXECUTION": classification["authority_checked"] is False and classification["admissibility_checked"] is False and classification["execution_claimed"] is False,
        "SCHEMA_VALIDATOR_REVIEW_16_NO_SCHEMA_ARCHIVE_MUTATION_OR_CREATION": classification["schema_archive_mutated"] is False and classification["schema_created"] is False,
        "SCHEMA_VALIDATOR_REVIEW_17_NO_PROPOSAL_REPAIR_OR_BUILDER_COMMAND": classification["proposal_repaired"] is False and classification["builder_command_emitted"] is False,
        "SCHEMA_VALIDATOR_REVIEW_18_NO_SIDECAR_DESIGN_OR_BUILD": review_authority["may_design_observability_sidecar_now"] is False and review_authority["may_build_observability_sidecar_now"] is False,
        "SCHEMA_VALIDATOR_REVIEW_19_NO_C7_OR_C8": classification["c7_authorized"] is False and classification["c8_authorized"] is False,
        "SCHEMA_VALIDATOR_REVIEW_20_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "SCHEMA_VALIDATOR_REVIEW_21_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["observability_reference_mutated"] is False,
        "SCHEMA_VALIDATOR_REVIEW_22_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "SCHEMA_VALIDATOR_REVIEW_23_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "SCHEMA_VALIDATOR_REVIEW_24_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "SCHEMA_VALIDATOR_REVIEW_25_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": REVIEW_ROLLUP_PATH.exists() and REVIEW_PROFILE_PATH.exists() and REVIEW_REPORT_PATH.exists() and REVIEW_TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEW_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEW_V0"
    terminal = review_trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEW_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_build": SOURCE_BUILD_RECEIPT_ID,
        "source_repair": SOURCE_REPAIR_RECEIPT_ID,
        "recommended_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "runtime_schema_validator_review_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEW_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_runtime_schema_validator_cell_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_runtime_schema_validator_cell_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "source_runtime_schema_validator_cell_failed_build_receipt_id": SOURCE_FAILED_BUILD_RECEIPT_ID,
        "source_runtime_schema_validator_cell_design_receipt_id": SOURCE_DESIGN_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "machine_readable_runtime_schema_validator_review_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "runtime_schema_validator_cell_reviewed": gate == "PASS",
            "close_ready": gate == "PASS",
            "source_build_receipt_consumed": True,
            "source_repair_receipt_consumed": True,
            "source_failed_build_receipt_consumed_as_context": True,
            "schema_surface_reviewed": gate == "PASS",
            "demo_results_reviewed": gate == "PASS",
            "hidden_execution_classification_confirmed": gate == "PASS",
            "only_valid_advances_confirmed": gate == "PASS",
            "invalid_returns_to_builder_confirmed": gate == "PASS",
            "schema_archive_read_only_confirmed": gate == "PASS",
            "negative_controls_zero_confirmed": gate == "PASS",
            "proposals_evaluated": build_summary.get("proposals_evaluated"),
            "valid_count": build_summary.get("valid_count"),
            "invalid_count": build_summary.get("invalid_count"),
            "advanced_to_admissibility_count": build_summary.get("advanced_to_admissibility_count"),
            "returned_to_builder_count": build_summary.get("returned_to_builder_count"),
            "hidden_execution_field_count": build_summary.get("result_class_counts", {}).get("HIDDEN_EXECUTION_FIELD"),
            "synthetic_demo_build_only": True,
            "live_runtime_routing_installed": False,
            "observability_sidecar_deferred": True,
            "unit_feedback_hardening_deferred": True,
            "c7_deferred": True,
            "c8_deferred": True,
            "runtime_adoption_deferred": True,
            "runtime_effect": False,
            "runtime_patched": False,
            "authority_checked": False,
            "admissibility_checked": False,
            "execution_claimed": False,
            "schema_archive_mutated": False,
            "proposal_repaired": False,
            "schema_created": False,
            "builder_command_emitted": False,
            "c7_authorized": False,
            "c8_authorized": False,
            "new_domain_shift_executed": False,
            "general_cell1_authority_claimed": False,
            "global_autonomy_claimed": False,
            "full_transfer_claimed": False,
            "runtime_wide_enforcement_claimed": False,
            "source_mutated": False,
            "prior_receipt_mutated": False,
            "observability_reference_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": gate == "PASS",
            "recommended_next": final_next,
        },
        "aggregate_metrics": review_report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "review_basis": rel(REVIEW_BASIS_PATH),
            "source_build_receipt_review": rel(SOURCE_BUILD_RECEIPT_REVIEW_PATH),
            "source_repair_receipt_review": rel(SOURCE_REPAIR_RECEIPT_REVIEW_PATH),
            "source_failed_build_review": rel(SOURCE_FAILED_BUILD_REVIEW_PATH),
            "artifact_inventory": rel(ARTIFACT_INVENTORY_PATH),
            "schema_surface_review": rel(SCHEMA_SURFACE_REVIEW_PATH),
            "demo_result_review": rel(DEMO_RESULT_REVIEW_PATH),
            "packet_routing_review": rel(PACKET_ROUTING_REVIEW_PATH),
            "negative_control_review": rel(NEGATIVE_CONTROL_REVIEW_PATH),
            "boundary_review": rel(BOUNDARY_REVIEW_PATH),
            "observability_alignment_review": rel(OBSERVABILITY_ALIGNMENT_REVIEW_PATH),
            "reviewed_reference_close_candidate": rel(REVIEWED_REFERENCE_CLOSE_CANDIDATE_PATH),
            "review_authority_boundary": rel(REVIEW_AUTHORITY_BOUNDARY_PATH),
            "classification": rel(REVIEW_CLASSIFICATION_PATH),
            "rollup": rel(REVIEW_ROLLUP_PATH),
            "profile": rel(REVIEW_PROFILE_PATH),
            "report": rel(REVIEW_REPORT_PATH),
            "transition_trace": rel(REVIEW_TRACE_PATH),
        },
        "terminal": terminal,
        "created_at": now_iso(),
    }

    write_json(receipt_path, receipt)

    print(json.dumps(receipt, indent=2, sort_keys=True))
    print(f"runtime_schema_validator_review_receipt_id={receipt_id}")
    print(f"runtime_schema_validator_review_receipt_path={rel(receipt_path)}")
    print(f"runtime_schema_validator_review_close_candidate_path={rel(REVIEWED_REFERENCE_CLOSE_CANDIDATE_PATH)}")
    print(f"runtime_schema_validator_review_rollup_path={rel(REVIEW_ROLLUP_PATH)}")
    print(f"runtime_schema_validator_review_profile_path={rel(REVIEW_PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
