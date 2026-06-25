#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

ROOT = Path(__file__).resolve().parents[1]

UNIT_ID = "CLOSE_RUNTIME_SCHEMA_VALIDATOR_CELL_AS_REVIEWED_REFERENCE_V0"
TARGET_UNIT_ID = "runtime.schema_validator_cell.reference_closure.v0"
LAYER = "RUNTIME / SIEVE_1 / REFERENCE_CLOSURE"
MODE = "CLOSE_ONLY / FREEZE_REVIEWED_REFERENCE / NO_RUNTIME_PATCH"
BUILD_MODE = "RUNTIME_SCHEMA_VALIDATOR_CELL_REFERENCE_CLOSURE_ONLY"

SOURCE_REVIEW_RECEIPT_ID = "a6e15175"
SOURCE_BUILD_RECEIPT_ID = "3fe3a57f"
SOURCE_REPAIR_RECEIPT_ID = "604607c2"
SOURCE_DESIGN_RECEIPT_ID = "ccbf5723"
SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID = "ac09c2e3"

REVIEW_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_review_v0_receipts/a6e15175.json"
BUILD_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_v0_receipts/3fe3a57f.json"
REPAIR_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_build_repair_v0_receipts/604607c2.json"
DESIGN_RECEIPT_PATH = ROOT / "data/runtime_schema_validator_cell_target_from_reviewed_observability_reference_v0_receipts/ccbf5723.json"
EDGE_OBS_REF_CLOSE_RECEIPT_PATH = ROOT / "data/decision_edge_observability_reference_closure_from_bounded_c6_adoption_probe_reference_v0_receipts/ac09c2e3.json"

REVIEW_DIR = ROOT / "data/runtime_schema_validator_cell_review_v0"
BUILD_DIR = ROOT / "data/runtime_schema_validator_cell_v0"
REPAIR_DIR = ROOT / "data/runtime_schema_validator_cell_build_repair_v0"
DESIGN_DIR = ROOT / "data/runtime_schema_validator_cell_target_from_reviewed_observability_reference_v0"

REVIEW_ARTIFACTS = [
    REVIEW_DIR / "runtime_schema_validator_review_basis_v0.json",
    REVIEW_DIR / "runtime_schema_validator_source_build_receipt_review_v0.json",
    REVIEW_DIR / "runtime_schema_validator_source_repair_receipt_review_v0.json",
    REVIEW_DIR / "runtime_schema_validator_failed_build_review_v0.json",
    REVIEW_DIR / "runtime_schema_validator_artifact_inventory_review_v0.json",
    REVIEW_DIR / "runtime_schema_validator_schema_surface_review_v0.json",
    REVIEW_DIR / "runtime_schema_validator_demo_result_review_v0.json",
    REVIEW_DIR / "runtime_schema_validator_packet_routing_review_v0.json",
    REVIEW_DIR / "runtime_schema_validator_negative_control_review_v0.json",
    REVIEW_DIR / "runtime_schema_validator_boundary_review_v0.json",
    REVIEW_DIR / "runtime_schema_validator_observability_alignment_review_v0.json",
    REVIEW_DIR / "runtime_schema_validator_reviewed_reference_close_candidate_v0.json",
    REVIEW_DIR / "runtime_schema_validator_review_authority_boundary_v0.json",
    REVIEW_DIR / "runtime_schema_validator_review_classification_v0.json",
    REVIEW_DIR / "runtime_schema_validator_review_rollup_v0.json",
    REVIEW_DIR / "runtime_schema_validator_review_profile_v0.json",
    REVIEW_DIR / "runtime_schema_validator_review_report.json",
    REVIEW_DIR / "runtime_schema_validator_review_transition_trace.json",
]

BUILD_ARTIFACTS = [
    BUILD_DIR / "schema_archive_schema_v0.json",
    BUILD_DIR / "schema_archive_v0.json",
    BUILD_DIR / "schema_validation_result_enum_v0.json",
    BUILD_DIR / "schema_validation_result_schema_v0.json",
    BUILD_DIR / "validated_candidate_packet_schema_v0.json",
    BUILD_DIR / "schema_feedback_packet_schema_v0.json",
    BUILD_DIR / "schema_gap_feedback_packet_schema_v0.json",
    BUILD_DIR / "schema_validator_cell_receipt_schema_v0.json",
    BUILD_DIR / "schema_validator_check_table_v0.json",
    BUILD_DIR / "schema_validator_demo_inputs_v0.jsonl",
    BUILD_DIR / "schema_validation_results_v0.jsonl",
    BUILD_DIR / "validated_candidate_packets_v0.jsonl",
    BUILD_DIR / "schema_feedback_packets_v0.jsonl",
    BUILD_DIR / "schema_gap_feedback_packets_v0.jsonl",
    BUILD_DIR / "schema_validator_rollup_v0.json",
    BUILD_DIR / "schema_validator_readout_v0.json",
    BUILD_DIR / "schema_validator_profile_v0.json",
    BUILD_DIR / "schema_validator_report.json",
    BUILD_DIR / "schema_validator_transition_trace.json",
]

REPAIR_ARTIFACTS = [
    REPAIR_DIR / "build_script_patch_record_v0.json",
    REPAIR_DIR / "runtime_schema_validator_build_repair_basis_v0.json",
    REPAIR_DIR / "runtime_schema_validator_build_repair_classification_v0.json",
]

DESIGN_ARTIFACTS = [
    DESIGN_DIR / "runtime_schema_validator_cell_target_spec_v0.json",
    DESIGN_DIR / "runtime_schema_validator_cell_build_target_v0.json",
    DESIGN_DIR / "runtime_observability_sidecar_dependency_park_v0.json",
]

REQUIRED_SOURCE_FILES = [
    REVIEW_RECEIPT_PATH,
    BUILD_RECEIPT_PATH,
    REPAIR_RECEIPT_PATH,
    DESIGN_RECEIPT_PATH,
    EDGE_OBS_REF_CLOSE_RECEIPT_PATH,
] + REVIEW_ARTIFACTS + BUILD_ARTIFACTS + REPAIR_ARTIFACTS + DESIGN_ARTIFACTS

OUT_DIR = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0"
RECEIPT_DIR = ROOT / "data/runtime_schema_validator_cell_reference_closure_v0_receipts"

CLOSURE_BASIS_PATH = OUT_DIR / "runtime_schema_validator_reference_closure_basis_v0.json"
REVIEW_CONSUMPTION_PATH = OUT_DIR / "runtime_schema_validator_review_consumption_v0.json"
REVIEWED_REFERENCE_PATH = OUT_DIR / "runtime_schema_validator_reviewed_reference_v0.json"
FREEZE_MANIFEST_PATH = OUT_DIR / "runtime_schema_validator_reviewed_reference_freeze_manifest_v0.json"
REFERENCE_INDEX_PATH = OUT_DIR / "runtime_schema_validator_reference_index_v0.json"
SCHEMA_SURFACE_REFERENCE_PATH = OUT_DIR / "runtime_schema_validator_schema_surface_reference_v0.json"
DEMO_RESULT_REFERENCE_PATH = OUT_DIR / "runtime_schema_validator_demo_result_reference_v0.json"
PACKET_ROUTING_REFERENCE_PATH = OUT_DIR / "runtime_schema_validator_packet_routing_reference_v0.json"
NEGATIVE_CONTROL_REFERENCE_PATH = OUT_DIR / "runtime_schema_validator_negative_control_reference_v0.json"
OBSERVABILITY_HOOK_REFERENCE_PATH = OUT_DIR / "runtime_schema_validator_observability_hook_reference_v0.json"
SIDECAR_DESIGN_PREREQ_PATH = OUT_DIR / "runtime_observability_sidecar_design_prerequisite_v0.json"
POST_CLOSURE_DECISION_READY_PATH = OUT_DIR / "runtime_schema_validator_reference_post_closure_decision_ready_v0.json"
AUTHORITY_BOUNDARY_PATH = OUT_DIR / "runtime_schema_validator_reference_closure_authority_boundary_v0.json"
CLASSIFICATION_PATH = OUT_DIR / "runtime_schema_validator_reference_closure_classification_v0.json"
ROLLUP_PATH = OUT_DIR / "runtime_schema_validator_reference_closure_rollup_v0.json"
PROFILE_PATH = OUT_DIR / "runtime_schema_validator_reference_closure_profile_v0.json"
REPORT_PATH = OUT_DIR / "runtime_schema_validator_reference_closure_report.json"
TRACE_PATH = OUT_DIR / "runtime_schema_validator_reference_closure_transition_trace.json"

EXPECTED_REVIEW_STATUS = "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_CLOSE_READY"
EXPECTED_REVIEW_STOP = "STOP_TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_CLOSE_READY"
EXPECTED_REVIEW_NEXT = UNIT_ID

RECOMMENDED_NEXT = "DECIDE_NEXT_AFTER_RUNTIME_SCHEMA_VALIDATOR_CELL_REFERENCE_CLOSURE_V0"

EXPECTED_COUNTS = {
    "proposals_evaluated": 16,
    "valid_count": 2,
    "invalid_count": 14,
    "advanced_to_admissibility_count": 2,
    "returned_to_builder_count": 14,
    "hidden_execution_field_count": 1,
}

REQUIRED_EDGE_FIELDS = [
    "active_object",
    "attempted_move",
    "boundary_checked",
    "boundary_result",
    "blocked_moves",
    "lawful_next_moves",
    "source_packet_ref",
]

OBSERVABLE_EVENTS = [
    "schema_validation_started",
    "schema_loaded",
    "schema_validation_check_completed",
    "schema_validation_result",
    "validated_candidate_packet_emitted",
    "schema_feedback_packet_emitted",
    "schema_gap_feedback_packet_emitted",
    "schema_validator_receipt_emitted",
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

    review_receipt = read_json(REVIEW_RECEIPT_PATH)
    build_receipt = read_json(BUILD_RECEIPT_PATH)
    repair_receipt = read_json(REPAIR_RECEIPT_PATH)
    design_receipt = read_json(DESIGN_RECEIPT_PATH)
    edge_obs_receipt = read_json(EDGE_OBS_REF_CLOSE_RECEIPT_PATH)

    review_summary = review_receipt.get("machine_readable_runtime_schema_validator_review_summary", {})
    build_summary = build_receipt.get("machine_readable_schema_validator_build_summary", {})
    repair_summary = repair_receipt.get("repair_summary", {})
    design_summary = design_receipt.get("machine_readable_runtime_schema_validator_cell_design_summary", {})

    close_candidate = read_json(REVIEW_DIR / "runtime_schema_validator_reviewed_reference_close_candidate_v0.json")
    review_authority = read_json(REVIEW_DIR / "runtime_schema_validator_review_authority_boundary_v0.json")
    review_classification = read_json(REVIEW_DIR / "runtime_schema_validator_review_classification_v0.json")
    review_rollup = read_json(REVIEW_DIR / "runtime_schema_validator_review_rollup_v0.json")
    review_profile = read_json(REVIEW_DIR / "runtime_schema_validator_review_profile_v0.json")
    review_report = read_json(REVIEW_DIR / "runtime_schema_validator_review_report.json")
    review_trace = read_json(REVIEW_DIR / "runtime_schema_validator_review_transition_trace.json")
    obs_alignment = read_json(REVIEW_DIR / "runtime_schema_validator_observability_alignment_review_v0.json")

    schema_archive = read_json(BUILD_DIR / "schema_archive_v0.json")
    result_enum = read_json(BUILD_DIR / "schema_validation_result_enum_v0.json")
    check_table = read_json(BUILD_DIR / "schema_validator_check_table_v0.json")
    build_rollup = read_json(BUILD_DIR / "schema_validator_rollup_v0.json")
    validation_results = read_jsonl(BUILD_DIR / "schema_validation_results_v0.jsonl")
    validated_packets = read_jsonl(BUILD_DIR / "validated_candidate_packets_v0.jsonl")
    schema_feedback_packets = read_jsonl(BUILD_DIR / "schema_feedback_packets_v0.jsonl")
    schema_gap_feedback_packets = read_jsonl(BUILD_DIR / "schema_gap_feedback_packets_v0.jsonl")
    sidecar_dependency = read_json(DESIGN_DIR / "runtime_observability_sidecar_dependency_park_v0.json")

    if review_receipt.get("receipt_id") != SOURCE_REVIEW_RECEIPT_ID or review_receipt.get("gate") != "PASS":
        failures.append("review_receipt_not_pass")
    if review_receipt.get("terminal", {}).get("stop_code") != EXPECTED_REVIEW_STOP:
        failures.append("review_stop_wrong")
    if review_receipt.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("review_hidden_next")
    if review_summary.get("status") != EXPECTED_REVIEW_STATUS:
        failures.append(f"review_status_wrong:{review_summary.get('status')}")
    if review_summary.get("recommended_next") != EXPECTED_REVIEW_NEXT:
        failures.append(f"review_next_wrong:{review_summary.get('recommended_next')}")

    for key in [
        "runtime_schema_validator_cell_reviewed",
        "close_ready",
        "source_build_receipt_consumed",
        "source_repair_receipt_consumed",
        "source_failed_build_receipt_consumed_as_context",
        "schema_surface_reviewed",
        "demo_results_reviewed",
        "hidden_execution_classification_confirmed",
        "only_valid_advances_confirmed",
        "invalid_returns_to_builder_confirmed",
        "schema_archive_read_only_confirmed",
        "negative_controls_zero_confirmed",
        "synthetic_demo_build_only",
        "observability_sidecar_deferred",
        "unit_feedback_hardening_deferred",
        "c7_deferred",
        "c8_deferred",
        "runtime_adoption_deferred",
        "bad_counters_zero",
    ]:
        if review_summary.get(key) is not True:
            failures.append(f"review_required_true_missing:{key}")

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
        if review_summary.get(key) is not False:
            failures.append(f"review_forbidden_true:{key}")

    for key, expected in EXPECTED_COUNTS.items():
        if review_summary.get(key) != expected:
            failures.append(f"review_count_wrong:{key}:{review_summary.get(key)}")

    if close_candidate.get("candidate_status") != "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_CLOSE_READY":
        failures.append("close_candidate_not_ready")
    if close_candidate.get("recommended_close_unit") != UNIT_ID:
        failures.append("close_candidate_next_wrong")
    if review_authority.get("may_close_schema_validator_cell_as_reviewed_reference_next") is not True:
        failures.append("review_authority_close_not_allowed")
    if review_classification.get("next_command_goal") is not None:
        failures.append("review_classification_hidden_next")
    if review_rollup.get("review_count") != 1:
        failures.append("review_rollup_count_wrong")
    if review_profile.get("review_result") != "REVIEWED_CLOSE_READY":
        failures.append("review_profile_wrong")
    if review_profile.get("next_command_goal") is not None:
        failures.append("review_profile_hidden_next")
    if review_report.get("recommended_next_handling") != UNIT_ID:
        failures.append("review_report_next_wrong")
    if review_trace.get("terminal", {}).get("next_command_goal") is not None:
        failures.append("review_trace_hidden_next")

    if build_receipt.get("receipt_id") != SOURCE_BUILD_RECEIPT_ID or build_receipt.get("gate") != "PASS":
        failures.append("build_receipt_not_pass")
    if build_summary.get("status") != "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_BUILT_REVIEW_READY":
        failures.append("build_status_wrong")
    if repair_receipt.get("receipt_id") != SOURCE_REPAIR_RECEIPT_ID or repair_receipt.get("gate") != "PASS":
        failures.append("repair_receipt_not_pass")
    if repair_summary.get("from_result") != "FORBIDDEN_FIELD" or repair_summary.get("to_result") != "HIDDEN_EXECUTION_FIELD":
        failures.append("repair_transition_wrong")
    if design_receipt.get("receipt_id") != SOURCE_DESIGN_RECEIPT_ID or design_receipt.get("gate") != "PASS":
        failures.append("design_receipt_not_pass")
    if edge_obs_receipt.get("receipt_id") != SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID or edge_obs_receipt.get("gate") != "PASS":
        failures.append("edge_obs_receipt_not_pass")

    if schema_archive.get("mutation_allowed_by_schema_validator") is not False:
        failures.append("schema_archive_not_read_only")
    if result_enum.get("only_advancing_result") != "VALID":
        failures.append("result_enum_advancing_wrong")
    if check_table.get("only_valid_advances") is not True:
        failures.append("check_table_only_valid_wrong")
    if not all(v == 0 for v in build_rollup.get("negative_controls", {}).values()):
        failures.append("build_negative_controls_not_zero")
    if len(validation_results) != 16:
        failures.append("validation_result_count_wrong")
    if len(validated_packets) != 2:
        failures.append("validated_packet_count_wrong")
    if len(schema_feedback_packets) + len(schema_gap_feedback_packets) != 14:
        failures.append("feedback_packet_count_wrong")
    if obs_alignment.get("schema_validator_surface_observable_events") != OBSERVABLE_EVENTS:
        failures.append("observability_events_wrong")
    if sidecar_dependency.get("park_status") != "PARKED_UNTIL_SCHEMA_VALIDATOR_REFERENCE_EXISTS":
        failures.append("sidecar_dependency_not_parked")

    return failures, {
        "review_summary": review_summary,
        "build_summary": build_summary,
        "repair_summary": repair_summary,
        "design_summary": design_summary,
        "close_candidate": close_candidate,
        "review_rollup": review_rollup,
        "review_profile": review_profile,
        "schema_archive": schema_archive,
        "result_enum": result_enum,
        "check_table": check_table,
        "build_rollup": build_rollup,
        "validation_results": validation_results,
        "validated_packets": validated_packets,
        "schema_feedback_packets": schema_feedback_packets,
        "schema_gap_feedback_packets": schema_gap_feedback_packets,
        "obs_alignment": obs_alignment,
        "sidecar_dependency": sidecar_dependency,
    }

def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPT_DIR.mkdir(parents=True, exist_ok=True)

    source_before = snapshot_files(REQUIRED_SOURCE_FILES)
    failures, basis = validate_basis()
    if source_before != snapshot_files(REQUIRED_SOURCE_FILES):
        failures.append("source_file_hash_changed")

    closure_pass = not failures
    status = "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_CLOSED_AS_REVIEWED_REFERENCE_DECISION_READY" if closure_pass else "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_REFERENCE_CLOSURE_GATE_FAIL"
    recommended_next = RECOMMENDED_NEXT if closure_pass else "REPAIR_RUNTIME_SCHEMA_VALIDATOR_CELL_REFERENCE_CLOSURE_V0"

    review_summary = basis.get("review_summary", {})
    build_summary = basis.get("build_summary", {})
    repair_summary = basis.get("repair_summary", {})
    close_candidate = basis.get("close_candidate", {})
    schema_archive = basis.get("schema_archive", {})
    result_enum = basis.get("result_enum", {})
    check_table = basis.get("check_table", {})
    build_rollup = basis.get("build_rollup", {})
    obs_alignment = basis.get("obs_alignment", {})
    sidecar_dependency = basis.get("sidecar_dependency", {})

    reason_codes = [
        "RUNTIME_SCHEMA_VALIDATOR_CELL_CLOSED_AS_REVIEWED_REFERENCE",
        "REVIEW_RECEIPT_CONSUMED",
        "BUILD_RECEIPT_CONSUMED",
        "REPAIR_RECEIPT_CONSUMED",
        "DESIGN_RECEIPT_CONSUMED",
        "DECISION_EDGE_OBSERVABILITY_REFERENCE_CONSUMED",
        "SCHEMA_SURFACE_FROZEN",
        "DEMO_RESULT_REFERENCE_FROZEN",
        "PACKET_ROUTING_REFERENCE_FROZEN",
        "NEGATIVE_CONTROL_REFERENCE_FROZEN",
        "OBSERVABILITY_HOOK_REFERENCE_FROZEN",
        "SIDECAR_DESIGN_PREREQUISITE_EMITTED",
        "POST_CLOSURE_DECISION_READY",
        "SYNTHETIC_DEMO_BUILD_ONLY_CONFIRMED",
        "NO_LIVE_RUNTIME_ROUTING",
        "NO_RUNTIME_EFFECT",
        "NO_RUNTIME_PATCH",
        "NO_AUTHORITY_CHECK",
        "NO_ADMISSIBILITY_CHECK",
        "NO_EXECUTION_CLAIM",
        "NO_SCHEMA_ARCHIVE_MUTATION",
        "NO_PROPOSAL_REPAIR",
        "NO_SCHEMA_CREATION",
        "NO_BUILDER_COMMAND",
        "NO_SIDECAR_DESIGN_OR_BUILD",
        "NO_C7_AUTHORIZATION",
        "NO_C8_AUTHORIZATION",
        "NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS",
        "NO_SOURCE_OR_REFERENCE_MUTATION",
        "NO_HIDDEN_NEXT_COMMAND",
    ] if closure_pass else failures

    source_hash_manifest = snapshot_files(REQUIRED_SOURCE_FILES)

    closure_basis = {
        "schema_version": "runtime_schema_validator_reference_closure_basis_v0",
        "basis_status": "BASIS_ACCEPTED" if closure_pass else "BASIS_REPAIR_REQUIRED",
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "source_design_receipt_id": SOURCE_DESIGN_RECEIPT_ID,
        "source_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "closure_scope": "freeze synthetic Schema Validator Cell reviewed surface as reference",
        "closure_does_not_mean": [
            "live runtime routing installed",
            "runtime patched",
            "authority checked",
            "admissibility checked",
            "execution allowed",
            "Sidecar designed",
            "C8 authorized",
        ],
    }

    review_consumption = {
        "schema_version": "runtime_schema_validator_review_consumption_v0",
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "review_status": review_summary.get("status"),
        "close_ready": review_summary.get("close_ready"),
        "reviewed_reference_close_candidate": close_candidate.get("candidate_status"),
        "review_consumed_without_mutation": True,
    }

    reviewed_reference = {
        "schema_version": "runtime_schema_validator_reviewed_reference_v0",
        "reference_status": "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_FROZEN" if closure_pass else "NOT_FROZEN",
        "cell_id": "SCHEMA_VALIDATOR_CELL",
        "mode": "VALIDATE / CLASSIFY / FORMATION_ONLY",
        "source_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "source_design_receipt_id": SOURCE_DESIGN_RECEIPT_ID,
        "source_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "core_rule": "Schema Validator Cell validates proposal formation/readability under known schema. Lawful Admissibility Cell validates permission.",
        "valid_advances_only_to": "LAWFUL_ADMISSIBILITY_CELL",
        "invalid_returns_to": "BUILDER_PROPOSAL_CELL",
        "schema_archive_read_only": schema_archive.get("mutation_allowed_by_schema_validator") is False,
        "only_advancing_result": result_enum.get("only_advancing_result"),
        "formation_check_count": len(check_table.get("checks", [])),
        "result_enum_count": len(result_enum.get("closed_results", [])),
        "demo_profile": {
            "proposals_evaluated": review_summary.get("proposals_evaluated"),
            "valid_count": review_summary.get("valid_count"),
            "invalid_count": review_summary.get("invalid_count"),
            "advanced_to_admissibility_count": review_summary.get("advanced_to_admissibility_count"),
            "returned_to_builder_count": review_summary.get("returned_to_builder_count"),
            "hidden_execution_field_count": review_summary.get("hidden_execution_field_count"),
        },
        "result_class_counts": build_summary.get("result_class_counts"),
        "negative_controls": build_rollup.get("negative_controls"),
        "observable_events": obs_alignment.get("schema_validator_surface_observable_events"),
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
    }

    freeze_manifest = {
        "schema_version": "runtime_schema_validator_reviewed_reference_freeze_manifest_v0",
        "freeze_status": "FROZEN" if closure_pass else "NOT_FROZEN",
        "reference_id": "runtime_schema_validator_reviewed_reference_v0",
        "reference_path": rel(REVIEWED_REFERENCE_PATH),
        "source_hash_manifest": source_hash_manifest,
        "frozen_artifacts": {
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "schema_surface_reference": rel(SCHEMA_SURFACE_REFERENCE_PATH),
            "demo_result_reference": rel(DEMO_RESULT_REFERENCE_PATH),
            "packet_routing_reference": rel(PACKET_ROUTING_REFERENCE_PATH),
            "negative_control_reference": rel(NEGATIVE_CONTROL_REFERENCE_PATH),
            "observability_hook_reference": rel(OBSERVABILITY_HOOK_REFERENCE_PATH),
        },
    }

    reference_index = {
        "schema_version": "runtime_schema_validator_reference_index_v0",
        "index_status": "REFERENCE_INDEX_EMITTED" if closure_pass else "NOT_EMITTED",
        "entries": [
            {"name": "reviewed_reference", "path": rel(REVIEWED_REFERENCE_PATH)},
            {"name": "schema_surface_reference", "path": rel(SCHEMA_SURFACE_REFERENCE_PATH)},
            {"name": "demo_result_reference", "path": rel(DEMO_RESULT_REFERENCE_PATH)},
            {"name": "packet_routing_reference", "path": rel(PACKET_ROUTING_REFERENCE_PATH)},
            {"name": "negative_control_reference", "path": rel(NEGATIVE_CONTROL_REFERENCE_PATH)},
            {"name": "observability_hook_reference", "path": rel(OBSERVABILITY_HOOK_REFERENCE_PATH)},
            {"name": "sidecar_design_prerequisite", "path": rel(SIDECAR_DESIGN_PREREQ_PATH)},
            {"name": "post_closure_decision_ready", "path": rel(POST_CLOSURE_DECISION_READY_PATH)},
        ],
    }

    schema_surface_reference = {
        "schema_version": "runtime_schema_validator_schema_surface_reference_v0",
        "reference_status": "REVIEWED_REFERENCE",
        "schema_archive_read_only": schema_archive.get("mutation_allowed_by_schema_validator") is False,
        "schema_archive_schema_path": rel(BUILD_DIR / "schema_archive_schema_v0.json"),
        "schema_archive_path": rel(BUILD_DIR / "schema_archive_v0.json"),
        "result_enum_path": rel(BUILD_DIR / "schema_validation_result_enum_v0.json"),
        "result_schema_path": rel(BUILD_DIR / "schema_validation_result_schema_v0.json"),
        "validated_candidate_packet_schema_path": rel(BUILD_DIR / "validated_candidate_packet_schema_v0.json"),
        "schema_feedback_packet_schema_path": rel(BUILD_DIR / "schema_feedback_packet_schema_v0.json"),
        "schema_gap_feedback_packet_schema_path": rel(BUILD_DIR / "schema_gap_feedback_packet_schema_v0.json"),
        "receipt_schema_path": rel(BUILD_DIR / "schema_validator_cell_receipt_schema_v0.json"),
        "check_table_path": rel(BUILD_DIR / "schema_validator_check_table_v0.json"),
    }

    demo_result_reference = {
        "schema_version": "runtime_schema_validator_demo_result_reference_v0",
        "reference_status": "REVIEWED_REFERENCE",
        "proposals_evaluated": review_summary.get("proposals_evaluated"),
        "valid_count": review_summary.get("valid_count"),
        "invalid_count": review_summary.get("invalid_count"),
        "advanced_to_admissibility_count": review_summary.get("advanced_to_admissibility_count"),
        "returned_to_builder_count": review_summary.get("returned_to_builder_count"),
        "hidden_execution_field_count": review_summary.get("hidden_execution_field_count"),
        "result_class_counts": build_summary.get("result_class_counts"),
        "validation_results_path": rel(BUILD_DIR / "schema_validation_results_v0.jsonl"),
    }

    packet_routing_reference = {
        "schema_version": "runtime_schema_validator_packet_routing_reference_v0",
        "reference_status": "REVIEWED_REFERENCE",
        "only_valid_advances": True,
        "valid_advances_to": "LAWFUL_ADMISSIBILITY_CELL",
        "invalid_returns_to": "BUILDER_PROPOSAL_CELL",
        "authority_status_after_validation": "NOT_CHECKED",
        "admissibility_status_after_validation": "NOT_CHECKED",
        "execution_status_after_validation": "NOT_EXECUTED",
        "validated_candidate_packets_path": rel(BUILD_DIR / "validated_candidate_packets_v0.jsonl"),
        "schema_feedback_packets_path": rel(BUILD_DIR / "schema_feedback_packets_v0.jsonl"),
        "schema_gap_feedback_packets_path": rel(BUILD_DIR / "schema_gap_feedback_packets_v0.jsonl"),
    }

    negative_control_reference = {
        "schema_version": "runtime_schema_validator_negative_control_reference_v0",
        "reference_status": "REVIEWED_REFERENCE",
        "negative_controls": build_rollup.get("negative_controls"),
        "bad_counters_zero": True,
    }

    observability_hook_reference = {
        "schema_version": "runtime_schema_validator_observability_hook_reference_v0",
        "reference_status": "REVIEWED_REFERENCE",
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "load_bearing_edge_fields": REQUIRED_EDGE_FIELDS,
        "schema_validator_surface_observable_events": OBSERVABLE_EVENTS,
        "sidecar_dependency": "Use this reference when designing the Runtime Observability Sidecar.",
    }

    sidecar_design_prereq = {
        "schema_version": "runtime_observability_sidecar_design_prerequisite_v0",
        "prerequisite_status": "SATISFIED" if closure_pass else "NOT_SATISFIED",
        "schema_validator_reviewed_reference_available": closure_pass,
        "schema_validator_reviewed_reference_path": rel(REVIEWED_REFERENCE_PATH),
        "decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "next_candidate_branch": "DESIGN_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_FROM_SCHEMA_VALIDATOR_AND_OBSERVABILITY_REFERENCES",
        "why": "The Sidecar can now consume both the decision-edge observability reference and the Schema Validator reviewed reference.",
        "does_not_authorize": [
            "live runtime instrumentation",
            "runtime patch",
            "C8",
            "runtime-wide enforcement",
        ],
    }

    post_closure_decision_ready = {
        "schema_version": "runtime_schema_validator_reference_post_closure_decision_ready_v0",
        "decision_ready": closure_pass,
        "closed_reference": "runtime_schema_validator_reviewed_reference_v0",
        "recommended_next": recommended_next,
        "strong_candidate": "DESIGN_RUNTIME_OBSERVABILITY_SIDECAR_TARGET_FROM_SCHEMA_VALIDATOR_AND_OBSERVABILITY_REFERENCES_V0",
        "decision_required": True,
        "why_decision_required": "Closure freezes the reference. A separate decision should select the Sidecar design branch before designing it.",
    }

    authority_boundary = {
        "schema_version": "runtime_schema_validator_reference_closure_authority_boundary_v0",
        "status": status,
        "may_decide_next_after_schema_validator_reference_closure": closure_pass,
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
        "may_mutate_schema_validator_reference": False,
        "may_mutate_observability_reference": False,
    }

    classification = {
        "schema_version": "runtime_schema_validator_reference_closure_classification_v0",
        "classification_status": status,
        "reason_codes": reason_codes,
        "runtime_schema_validator_cell_closed_as_reviewed_reference": closure_pass,
        "reviewed_reference_frozen": closure_pass,
        "post_schema_validator_reference_decision_ready": closure_pass,
        "sidecar_design_prerequisite_satisfied": closure_pass,
        "source_review_receipt_consumed": True,
        "source_build_receipt_consumed": True,
        "source_repair_receipt_consumed": True,
        "source_design_receipt_consumed": True,
        "source_edge_observability_reference_consumed": True,
        "schema_surface_frozen": closure_pass,
        "demo_result_reference_frozen": closure_pass,
        "packet_routing_reference_frozen": closure_pass,
        "negative_control_reference_frozen": closure_pass,
        "observability_hook_reference_frozen": closure_pass,
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
        "schema_validator_reference_mutated": False,
        "observability_reference_mutated": False,
        "hidden_next_command": False,
        "latest_file_guessing": False,
        "mtime_selection": False,
        "bad_counters_zero": closure_pass,
        "recommended_next": recommended_next,
        "next_command_goal": None,
    }

    rollup = {
        "schema_version": "runtime_schema_validator_reference_closure_rollup_v0",
        "closure_count": 1 if closure_pass else 0,
        "reviewed_reference_frozen_count": 1 if closure_pass else 0,
        "post_closure_decision_ready_count": 1 if closure_pass else 0,
        "sidecar_design_prerequisite_satisfied_count": 1 if closure_pass else 0,
        "proposals_evaluated": review_summary.get("proposals_evaluated"),
        "valid_count": review_summary.get("valid_count"),
        "invalid_count": review_summary.get("invalid_count"),
        "advanced_to_admissibility_count": review_summary.get("advanced_to_admissibility_count"),
        "returned_to_builder_count": review_summary.get("returned_to_builder_count"),
        "hidden_execution_field_count": review_summary.get("hidden_execution_field_count"),
        "runtime_patch_count": 0,
        "live_runtime_routing_installed_count": 0,
        "authority_checked_count": 0,
        "admissibility_checked_count": 0,
        "execution_claim_count": 0,
        "schema_archive_mutation_count": 0,
        "proposal_repair_count": 0,
        "schema_created_count": 0,
        "builder_command_emitted_count": 0,
        "sidecar_design_count": 0,
        "sidecar_build_count": 0,
        "c7_authorized_count": 0,
        "c8_authorized_count": 0,
        "runtime_wide_enforcement_claim_count": 0,
        "hidden_next_command_count": 0,
        "latest_file_guessing_count": 0,
        "mtime_selection_count": 0,
        "recommended_next": recommended_next,
    }

    profile = {
        "schema_version": "runtime_schema_validator_reference_closure_profile_v0",
        "profile_id": "runtime_schema_validator_reference_closure_" + sig8(rollup),
        "status": status,
        "reference_status": reviewed_reference["reference_status"],
        "cell_id": "SCHEMA_VALIDATOR_CELL",
        "closure_result": "REVIEWED_REFERENCE_FROZEN" if closure_pass else "REPAIR_REQUIRED",
        "next_available_branch": "Runtime Observability Sidecar design, subject to separate decision",
        "synthetic_demo_build_only": True,
        "live_runtime_routing_installed": False,
        "runtime_patched": False,
        "bad_counters_zero": closure_pass,
        "must_not_infer": [
            "Schema Validator is live runtime routing",
            "Runtime was patched",
            "Sidecar was designed",
            "C8 is authorized",
            "VALID means authorized",
            "VALID means admissible",
            "VALID means execute",
        ],
        "next_command_goal": None,
    }

    report = {
        "schema_version": "runtime_schema_validator_reference_closure_report_v0",
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "status": status,
        "reason_codes": reason_codes,
        "receipt_backed_claim": "The Runtime Schema Validator Cell synthetic formation-sieve surface has been closed as a frozen reviewed reference. The frozen reference preserves schema surface, demo result profile, packet routing rule, zero negative controls, and observable event surface for future Sidecar design. Closure does not install live routing, patch runtime, check authority/admissibility, execute, repair proposals, mutate schema archive, design/build the Sidecar, or authorize C8.",
        "recommended_next_handling": recommended_next,
    }

    trace = {
        "schema_version": "runtime_schema_validator_reference_closure_transition_trace_v0",
        "trace": [
            {
                "step": "consume_review",
                "question": "is Schema Validator reviewed close-ready",
                "answer": "yes" if closure_pass else "no",
                "taken": "freeze reviewed reference",
            },
            {
                "step": "emit_reference",
                "question": "what is preserved",
                "answer": "schema surface, demo results, packet routing, negative controls, observable events",
                "taken": "emit reference, manifest, index, and post-closure decision-ready artifact",
            },
            {
                "step": "preserve_boundary",
                "question": "did closure design Sidecar, patch runtime, install routing, or open C8",
                "answer": "no",
                "taken": "stop decision-ready",
            },
        ],
        "terminal": {
            "type": "STOP",
            "stop_code": "STOP_" + status,
            "next_command_goal": None,
        },
    }

    artifacts = [
        (CLOSURE_BASIS_PATH, closure_basis),
        (REVIEW_CONSUMPTION_PATH, review_consumption),
        (REVIEWED_REFERENCE_PATH, reviewed_reference),
        (FREEZE_MANIFEST_PATH, freeze_manifest),
        (REFERENCE_INDEX_PATH, reference_index),
        (SCHEMA_SURFACE_REFERENCE_PATH, schema_surface_reference),
        (DEMO_RESULT_REFERENCE_PATH, demo_result_reference),
        (PACKET_ROUTING_REFERENCE_PATH, packet_routing_reference),
        (NEGATIVE_CONTROL_REFERENCE_PATH, negative_control_reference),
        (OBSERVABILITY_HOOK_REFERENCE_PATH, observability_hook_reference),
        (SIDECAR_DESIGN_PREREQ_PATH, sidecar_design_prereq),
        (POST_CLOSURE_DECISION_READY_PATH, post_closure_decision_ready),
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
        "SCHEMA_VALIDATOR_CLOSURE_0_REVIEW_RECEIPT_CONSUMED": REVIEW_RECEIPT_PATH.exists(),
        "SCHEMA_VALIDATOR_CLOSURE_1_BUILD_RECEIPT_CONSUMED": BUILD_RECEIPT_PATH.exists(),
        "SCHEMA_VALIDATOR_CLOSURE_2_REPAIR_RECEIPT_CONSUMED": REPAIR_RECEIPT_PATH.exists(),
        "SCHEMA_VALIDATOR_CLOSURE_3_DESIGN_RECEIPT_CONSUMED": DESIGN_RECEIPT_PATH.exists(),
        "SCHEMA_VALIDATOR_CLOSURE_4_EDGE_OBSERVABILITY_REFERENCE_CONSUMED": EDGE_OBS_REF_CLOSE_RECEIPT_PATH.exists(),
        "SCHEMA_VALIDATOR_CLOSURE_5_REVIEWED_REFERENCE_EMITTED": REVIEWED_REFERENCE_PATH.exists() and reviewed_reference["reference_status"] == "RUNTIME_SCHEMA_VALIDATOR_CELL_REVIEWED_REFERENCE_FROZEN",
        "SCHEMA_VALIDATOR_CLOSURE_6_FREEZE_MANIFEST_EMITTED": FREEZE_MANIFEST_PATH.exists() and freeze_manifest["freeze_status"] == "FROZEN",
        "SCHEMA_VALIDATOR_CLOSURE_7_REFERENCE_INDEX_EMITTED": REFERENCE_INDEX_PATH.exists(),
        "SCHEMA_VALIDATOR_CLOSURE_8_SCHEMA_SURFACE_REFERENCE_EMITTED": SCHEMA_SURFACE_REFERENCE_PATH.exists(),
        "SCHEMA_VALIDATOR_CLOSURE_9_DEMO_RESULT_REFERENCE_EMITTED": DEMO_RESULT_REFERENCE_PATH.exists(),
        "SCHEMA_VALIDATOR_CLOSURE_10_PACKET_ROUTING_REFERENCE_EMITTED": PACKET_ROUTING_REFERENCE_PATH.exists(),
        "SCHEMA_VALIDATOR_CLOSURE_11_NEGATIVE_CONTROL_REFERENCE_EMITTED": NEGATIVE_CONTROL_REFERENCE_PATH.exists(),
        "SCHEMA_VALIDATOR_CLOSURE_12_OBSERVABILITY_HOOK_REFERENCE_EMITTED": OBSERVABILITY_HOOK_REFERENCE_PATH.exists(),
        "SCHEMA_VALIDATOR_CLOSURE_13_SIDECAR_PREREQ_EMITTED": SIDECAR_DESIGN_PREREQ_PATH.exists() and sidecar_design_prereq["prerequisite_status"] == "SATISFIED",
        "SCHEMA_VALIDATOR_CLOSURE_14_POST_CLOSURE_DECISION_READY": POST_CLOSURE_DECISION_READY_PATH.exists() and post_closure_decision_ready["decision_ready"] is True,
        "SCHEMA_VALIDATOR_CLOSURE_15_NO_SIDECAR_DESIGN_OR_BUILD": classification["observability_sidecar_deferred"] is True and rollup["sidecar_design_count"] == 0 and rollup["sidecar_build_count"] == 0,
        "SCHEMA_VALIDATOR_CLOSURE_16_NO_RUNTIME_EFFECT_OR_PATCH": classification["runtime_effect"] is False and classification["runtime_patched"] is False,
        "SCHEMA_VALIDATOR_CLOSURE_17_NO_LIVE_RUNTIME_ROUTING": classification["live_runtime_routing_installed"] is False,
        "SCHEMA_VALIDATOR_CLOSURE_18_NO_AUTHORITY_ADMISSIBILITY_OR_EXECUTION": classification["authority_checked"] is False and classification["admissibility_checked"] is False and classification["execution_claimed"] is False,
        "SCHEMA_VALIDATOR_CLOSURE_19_NO_SCHEMA_ARCHIVE_MUTATION_OR_CREATION": classification["schema_archive_mutated"] is False and classification["schema_created"] is False,
        "SCHEMA_VALIDATOR_CLOSURE_20_NO_PROPOSAL_REPAIR_OR_BUILDER_COMMAND": classification["proposal_repaired"] is False and classification["builder_command_emitted"] is False,
        "SCHEMA_VALIDATOR_CLOSURE_21_NO_C7_OR_C8": classification["c7_authorized"] is False and classification["c8_authorized"] is False,
        "SCHEMA_VALIDATOR_CLOSURE_22_NO_TRANSFER_AUTONOMY_GENERAL_AUTHORITY_OR_RUNTIME_ENFORCEMENT_CLAIMS": classification["full_transfer_claimed"] is False and classification["global_autonomy_claimed"] is False and classification["general_cell1_authority_claimed"] is False and classification["runtime_wide_enforcement_claimed"] is False,
        "SCHEMA_VALIDATOR_CLOSURE_23_NO_SOURCE_OR_REFERENCE_MUTATION": classification["source_mutated"] is False and classification["prior_receipt_mutated"] is False and classification["schema_validator_reference_mutated"] is False and classification["observability_reference_mutated"] is False,
        "SCHEMA_VALIDATOR_CLOSURE_24_BAD_COUNTERS_ZERO": classification["bad_counters_zero"] is True,
        "SCHEMA_VALIDATOR_CLOSURE_25_NO_HIDDEN_NEXT_COMMAND": classification["next_command_goal"] is None,
        "SCHEMA_VALIDATOR_CLOSURE_26_NO_LATEST_OR_MTIME": classification["latest_file_guessing"] is False and classification["mtime_selection"] is False,
        "SCHEMA_VALIDATOR_CLOSURE_27_ROLLUP_PROFILE_REPORT_TRACE_EMITTED": ROLLUP_PATH.exists() and PROFILE_PATH.exists() and REPORT_PATH.exists() and TRACE_PATH.exists(),
    }

    if not all(acceptance_gate_results.values()):
        failures.append("acceptance_gate_result_false")

    gate = "PASS" if not failures else "FAIL"
    final_status = status if gate == "PASS" else "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_REFERENCE_CLOSURE_GATE_FAIL"
    final_next = recommended_next if gate == "PASS" else "REPAIR_RUNTIME_SCHEMA_VALIDATOR_CELL_REFERENCE_CLOSURE_V0"
    terminal = trace["terminal"] if gate == "PASS" else {
        "type": "STOP",
        "stop_code": "STOP_TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_REFERENCE_CLOSURE_GATE_FAIL",
        "next_command_goal": None,
    }

    receipt_id = sig8({
        "unit_id": UNIT_ID,
        "status": final_status,
        "gate": gate,
        "source_review": SOURCE_REVIEW_RECEIPT_ID,
        "recommended_next": final_next,
        "terminal": terminal,
    })
    receipt_path = RECEIPT_DIR / f"{receipt_id}.json"

    receipt = {
        "schema_version": "runtime_schema_validator_reference_closure_receipt_v0",
        "receipt_type": "TYPED_RUNTIME_SCHEMA_VALIDATOR_CELL_REFERENCE_CLOSURE_RECEIPT",
        "receipt_id": receipt_id,
        "unit_id": UNIT_ID,
        "target_unit_id": TARGET_UNIT_ID,
        "layer": LAYER,
        "mode": MODE,
        "build_mode": BUILD_MODE,
        "gate": gate,
        "failures": failures,
        "warnings": [],
        "source_runtime_schema_validator_cell_review_receipt_id": SOURCE_REVIEW_RECEIPT_ID,
        "source_runtime_schema_validator_cell_build_receipt_id": SOURCE_BUILD_RECEIPT_ID,
        "source_runtime_schema_validator_cell_repair_receipt_id": SOURCE_REPAIR_RECEIPT_ID,
        "source_runtime_schema_validator_cell_design_receipt_id": SOURCE_DESIGN_RECEIPT_ID,
        "source_decision_edge_observability_reference_closure_receipt_id": SOURCE_EDGE_OBS_REF_CLOSE_RECEIPT_ID,
        "machine_readable_runtime_schema_validator_reference_closure_summary": {
            "status": final_status,
            "reason_codes": reason_codes if gate == "PASS" else failures,
            "runtime_schema_validator_cell_closed_as_reviewed_reference": gate == "PASS",
            "reviewed_reference_frozen": gate == "PASS",
            "post_schema_validator_reference_decision_ready": gate == "PASS",
            "sidecar_design_prerequisite_satisfied": gate == "PASS",
            "source_review_receipt_consumed": True,
            "source_build_receipt_consumed": True,
            "source_repair_receipt_consumed": True,
            "source_design_receipt_consumed": True,
            "source_edge_observability_reference_consumed": True,
            "schema_surface_frozen": gate == "PASS",
            "demo_result_reference_frozen": gate == "PASS",
            "packet_routing_reference_frozen": gate == "PASS",
            "negative_control_reference_frozen": gate == "PASS",
            "observability_hook_reference_frozen": gate == "PASS",
            "proposals_evaluated": review_summary.get("proposals_evaluated"),
            "valid_count": review_summary.get("valid_count"),
            "invalid_count": review_summary.get("invalid_count"),
            "advanced_to_admissibility_count": review_summary.get("advanced_to_admissibility_count"),
            "returned_to_builder_count": review_summary.get("returned_to_builder_count"),
            "hidden_execution_field_count": review_summary.get("hidden_execution_field_count"),
            "observable_event_count": len(OBSERVABLE_EVENTS),
            "load_bearing_edge_field_count": len(REQUIRED_EDGE_FIELDS),
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
            "schema_validator_reference_mutated": False,
            "observability_reference_mutated": False,
            "hidden_next_command": False,
            "latest_file_guessing": False,
            "mtime_selection": False,
            "bad_counters_zero": gate == "PASS",
            "recommended_next": final_next,
        },
        "aggregate_metrics": report | {"status": final_status, "recommended_next_handling": final_next},
        "acceptance_gate_results": acceptance_gate_results,
        "output_artifacts": {
            "implementation_receipt": rel(receipt_path),
            "closure_basis": rel(CLOSURE_BASIS_PATH),
            "review_consumption": rel(REVIEW_CONSUMPTION_PATH),
            "reviewed_reference": rel(REVIEWED_REFERENCE_PATH),
            "freeze_manifest": rel(FREEZE_MANIFEST_PATH),
            "reference_index": rel(REFERENCE_INDEX_PATH),
            "schema_surface_reference": rel(SCHEMA_SURFACE_REFERENCE_PATH),
            "demo_result_reference": rel(DEMO_RESULT_REFERENCE_PATH),
            "packet_routing_reference": rel(PACKET_ROUTING_REFERENCE_PATH),
            "negative_control_reference": rel(NEGATIVE_CONTROL_REFERENCE_PATH),
            "observability_hook_reference": rel(OBSERVABILITY_HOOK_REFERENCE_PATH),
            "sidecar_design_prerequisite": rel(SIDECAR_DESIGN_PREREQ_PATH),
            "post_closure_decision_ready": rel(POST_CLOSURE_DECISION_READY_PATH),
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
    print(f"runtime_schema_validator_reference_closure_receipt_id={receipt_id}")
    print(f"runtime_schema_validator_reference_closure_receipt_path={rel(receipt_path)}")
    print(f"runtime_schema_validator_reviewed_reference_path={rel(REVIEWED_REFERENCE_PATH)}")
    print(f"runtime_schema_validator_sidecar_prereq_path={rel(SIDECAR_DESIGN_PREREQ_PATH)}")
    print(f"runtime_schema_validator_post_closure_decision_ready_path={rel(POST_CLOSURE_DECISION_READY_PATH)}")
    print(f"runtime_schema_validator_reference_closure_rollup_path={rel(ROLLUP_PATH)}")
    print(f"runtime_schema_validator_reference_closure_profile_path={rel(PROFILE_PATH)}")
    return 0 if gate == "PASS" else 1

if __name__ == "__main__":
    raise SystemExit(main())
